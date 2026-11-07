#!/usr/bin/env python3
"""Concept checks for mental-pressure level 3 (l9 to l12, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/mental-pressure-L3-concepts.py
Each check names its ledger row (docs/reports/audit-mental-pressure-1-3-ledger.md).
Exit 0 means every checked claim holds.
"""
import itertools
import math
import random
from fractions import Fraction as F


def check(name, cond, msg):
    assert cond, f"{name}: {msg}"
    print(f"ok  {name}")


# ---- l9: pacing and checkpoints
def checkpoints():
    check("pace", 480 / 80 == 6 and 540 / 60 == 9 and 600 / 50 == 12 and 600 / 60 == 10 and abs(8 / 80 * 60 - 6) < 1e-12,
          "l9 screens[0], [10], review-3 items[0], homework-3 items[6], screens[8] d1")
    check("checkpoints", [480 * k / 80 for k in (20, 40, 60)] == [120, 240, 360] and [9 * k for k in (15, 30, 45)] == [135, 270, 405],
          "l9 screens[2], [7], [10]: t_k = (T/N) k")
    check("sam", 3 + (480 - 42) // 6 == 76 and (30 - 6) / 6 == 4, "l9 screens[6]: 24 s over its share is four questions")
    check("behind_pace", 10 * 5 - 44 == 6 and 6 * 6 == 36 and 240 // 10 - 20 == 4, "l9 quiz[1], homework-3 items[6]")
    check("slow_perfect", abs(660 / 80 - 8.25) < 1e-12 and math.floor(480 / 8.25) == 58, "l12 quiz[0]")
    check("block_times", 115 + 130 + 150 - 360 == 35 and 115 + 130 + 150 + 100 - 480 == 15, "l12 quiz[3]")
    check("behind_at_two", 15 / 6 == 2.5 and 12 / 6 == 2, "homework-3 items[7].model: 15 s is 2.5 questions, 12 s two questions' worth")


# ---- l9 screens[3], [9]: cheapest first maximises the count (brute force against greedy)
def greedy(costs, budget):
    used = count = 0
    for c in sorted(costs):
        if used + c > budget:
            break
        used += c
        count += 1
    return count


def brute(costs, budget):
    best = 0
    for r in range(len(costs) + 1):
        for comb in itertools.combinations(costs, r):
            if sum(comb) <= budget:
                best = max(best, r)
    return best


def greedy_optimal():
    rng = random.Random(9)
    for _ in range(2000):
        n = rng.randint(0, 11)
        costs = [rng.randint(1, 30) for _ in range(n)]
        budget = rng.randint(0, 120)
        assert greedy(costs, budget) == brute(costs, budget), f"greedy not optimal on {costs} budget {budget}"
    check("greedy_optimal", greedy([22, 25, 4, 14, 3, 5, 14, 8, 4, 6], 60) == 8 and greedy([4, 5, 6, 18, 7, 25], 60) == 5
          and greedy([6, 12, 5, 20, 7, 4, 9], 45) == 6, "l9 screens[3], quiz[3], review-3 items[4]")
    check("greedy_sums", sum(sorted([22, 25, 4, 14, 3, 5, 14, 8, 4, 6])[:8]) == 58 and 4 + 5 + 6 + 7 + 18 == 40 and 4 + 5 + 6 + 7 + 9 + 12 == 43,
          "l9 screens[3].explain, quiz[3], review-3 items[4]")


# ---- l9 screens[5], quiz[2], homework-3 items[5]: expected mark of a guess under +1 / -1
def guess_value():
    rng = random.Random(5)
    reps = 400000
    for k, expect in ((4, -0.5), (3, -1 / 3), (2, 0.0)):
        total = 0
        for _ in range(reps):
            total += 1 if rng.randrange(k) == 0 else -1
        mean = total / reps
        se = math.sqrt((1 - expect ** 2) / reps)
        assert abs(mean - expect) < 4 * se + 1e-9, f"guess among {k}: {mean:.4f} against {expect:.4f}"
        assert abs((1 / k) * 1 + ((k - 1) / k) * (-1) - expect) < 1e-12
    check("guess_value", abs(5 * (1 / 3 - 2 / 3) + 5 / 3) < 1e-12, "homework-3 items[5]: five guesses among three are worth -5/3")
    print("    Monte Carlo with 400,000 guesses each: -0.5, -1/3, 0 within four standard errors")
    check("guess_sign", (1 / 3 - 2 / 3) < 0 == (1 / 2 - 1 / 2), "homework-3 items[7].model: guess only after removing two options")


# ---- l10 and homework-3 items[3]: difference tables, polynomials, ratios, affine rules
def difference_table(seq):
    rows = [list(seq)]
    while len(rows[-1]) > 1 and len(set(rows[-1])) > 1:
        row = rows[-1]
        rows.append([b - a for a, b in zip(row, row[1:])])
    return rows


def next_by_differences(seq):
    rows = difference_table(seq)
    if len(rows[-1]) < 2:
        return None
    return sum(row[-1] for row in rows)


def next_term(seq):
    t = [F(x) for x in seq]
    rows = [t]
    while len(rows[-1]) > 1 and len(set(rows[-1])) > 1:
        r = rows[-1]
        rows.append([b - a for a, b in zip(r, r[1:])])
    if len(rows[-1]) >= 2:
        return sum(r[-1] for r in rows)
    if len(t) >= 3 and 0 not in t[:-1]:
        ratios = {b / a for a, b in zip(t, t[1:])}
        if len(ratios) == 1:
            return t[-1] * ratios.pop()
    if len(t) >= 4 and t[1] != t[0]:
        k = (t[2] - t[1]) / (t[1] - t[0])
        c = t[1] - k * t[0]
        if all(b == k * a + c for a, b in zip(t, t[1:])):
            return k * t[-1] + c
    return None


def difference_checks():
    rng = random.Random(10)
    for _ in range(3000):
        deg = rng.randint(0, 4)
        coef = [rng.randint(-5, 5) for _ in range(deg + 1)]
        if deg and coef[-1] == 0:
            coef[-1] = 1
        terms = deg + 2 + rng.randint(0, 2)
        seq = [sum(c * n ** i for i, c in enumerate(coef)) for n in range(1, terms + 1)]
        expect = sum(c * (terms + 1) ** i for i, c in enumerate(coef))
        got = next_by_differences(seq)
        assert got == expect, f"polynomial of degree {deg}: {seq} -> {got}, expected {expect}"
        # the (deg)-th differences are constant and equal deg! times the leading coefficient
        rows = difference_table(seq)
        assert len(rows) - 1 <= deg, "a polynomial of degree d settles by the d-th differences"
        if deg == 2:
            assert rows[2][0] == 2 * coef[2], "half the second difference is the n^2 coefficient (l10 screens[5])"
    check("difference_table", next_by_differences([2, 6, 12, 20, 30]) == 42 and next_by_differences([3, 7, 11, 15]) == 19
          and next_by_differences([7, 7, 7, 7]) == 7 and next_by_differences([3, 6, 12, 24, 48]) is None
          and next_by_differences([1, 1, 2, 3, 5, 8]) is None and next_by_differences([5, 9]) is None
          and next_by_differences([2, 9, 28, 65]) is None,
          "l10 screens[9]: polynomials settle, doubling and Fibonacci and two terms do not; cubes plus 1 with four terms does not settle")
    # geometric sequences never settle: their differences are geometric with the same ratio
    for a in range(1, 8):
        for r in (2, 3):
            for terms in range(3, 9):
                seq = [a * r ** i for i in range(terms)]
                assert next_by_differences(seq) is None, f"geometric {seq} must not settle"
    print("ok  geometric_never_settles")


def next_term_checks():
    cases = [([3, 7, 11, 15], 19), ([2, 6, 12, 20, 30], 42), ([7, 7, 7], 7), ([3, 6, 12, 24], 48), ([5, 15, 45, 135], 405),
             ([64, 32, 16, 8], 4), ([4, 6, 9], F(27, 2)), ([9, 6, 4], F(8, 3)), ([3, 5, 9, 17, 33], 65), ([150, 250, 450, 850], 1650),
             ([1, 1, 2, 3, 5, 8], None), ([2, 3, 5, 7, 11], None), ([1, 2], None)]
    for seq, expect in cases:
        assert next_term(seq) == expect, f"next_term({seq}) = {next_term(seq)}, expected {expect}"
    rng = random.Random(11)
    for _ in range(2000):
        k, c, a = rng.choice([2, 3]), rng.randint(-5, 5), rng.randint(1, 9)
        terms = rng.randint(4, 7)
        seq = [a]
        for _ in range(terms - 1):
            seq.append(k * seq[-1] + c)
        if len(set(seq)) < 2:
            continue
        assert next_term(seq) == k * seq[-1] + c, f"affine {seq}"
    check("next_term", True, "homework-3 items[3]: the thirteen cases and 2,000 affine sequences")


SEQUENCES = [  # (shown terms, key, rule, where)
    ([3, 6, 12, 24], 48, "geom", "l9 Q2"), ([7, 10, 16, 28, 52], 100, "affine", "l9 Q8"),
    ([3, 7, 11, 15], 19, "poly", "l10 screens[0]"), ([1, 3, 6, 10, 15], 21, "poly", "l10 screens[1] B"),
    ([2, 6, 12, 20, 30], 42, "poly", "l10 screens[2]"), ([3, 6, 12, 24], 48, "geom", "l10 screens[3]"),
    ([5, 15, 45, 135], 405, "geom", "l10 screens[3]"), ([3, 5, 9, 17, 33], 65, "affine", "l10 screens[3]"),
    ([1, 4, 9, 16], 25, "poly", "l10 screens[4]"), ([1, 8, 27], 64, "list", "l10 screens[4] cubes"),
    ([2, 3, 5, 7, 11], 13, "list", "primes"), ([1, 1, 2, 3, 5, 8], 13, "fib", "l10 screens[4]"),
    ([1, 10, 2, 20, 3, 30], 4, "woven", "l10 screens[4]"), ([1, 2, 4, 7, 11], 16, "poly", "l10 screens[6]"),
    ([7, 7, 7, 7], 7, "poly", "l10 screens[7]"), ([4, 9, 14, 19], 24, "poly", "drill"), ([50, 44, 38, 32], 26, "poly", "drill"),
    ([1, 3, 9, 27], 81, "geom", "drill"), ([2, 5, 10, 17, 26], 37, "poly", "drill"), ([1, 4, 9, 16, 25], 36, "poly", "drill"),
    ([2, 3, 5, 8, 13], 21, "fib", "drill"), ([64, 32, 16, 8], 4, "geom", "drill"), ([1, 8, 27, 64], 125, "list", "drill cubes"),
    ([2, 2, 4, 6, 10], 16, "fib", "drill"), ([5, 6, 8, 12, 20], 36, "affine", "drill"), ([2, 20, 4, 40, 6, 60], 8, "woven", "drill"),
    ([2, 3, 5, 7, 11, 13], 17, "list", "drill primes"), ([150, 250, 450, 850], 1650, "affine", "l10 screens[11]"),
    ([41, 35, 29, 23], 17, "poly", "l10 quiz[0]"), ([2, 9, 28, 65], 126, "list", "l10 quiz[1] cubes plus 1"),
    ([2, 5, 4, 10, 8, 20], 16, "woven", "l10 quiz[2]"), ([3, 4, 7, 11, 18], 29, "fib", "l10 quiz[3]"),
    ([66, 57, 48, 39], 30, "poly", "l12 Q2"), ([2, 8, 20, 44, 92], 188, "affine", "l12 Q30"), ([75, 63, 51, 39], 27, "poly", "l12 Q31"),
    ([2, 7, 17, 37, 77], 157, "affine", "l12 Q32"), ([6, 12, 24, 48], 96, "geom", "l12 Q34"), ([35, 43, 51, 59], 67, "poly", "l12 Q62"),
    ([8, 9, 11, 14, 18], 23, "poly", "l12 Q67"), ([4, 10, 17, 25, 34], 44, "poly", "l12 Q72"),
    ([3, 6, 11, 18, 27], 38, "poly", "review-3 items[1]"), ([4, 7, 13, 25, 49], 97, "affine", "review-3 items[5]"),
    ([3, 100, 6, 90, 12, 80], 24, "woven", "review-3 items[8]"), ([7, 8, 10, 13, 17], 22, "poly", "homework-3 Q3"),
    ([6, 12, 24, 48], 96, "geom", "homework-3 Q14"), ([7, 12, 17, 22], 27, "poly", "homework-3 drill"),
    ([81, 27, 9, 3], 1, "geom", "homework-3 drill"), ([1, 4, 10, 19, 31], 46, "poly", "homework-3 drill"),
    ([2, 6, 18, 54], 162, "geom", "homework-3 drill"), ([1, 3, 4, 7, 11], 18, "fib", "homework-3 drill"),
    ([0, 3, 8, 15, 24], 35, "poly", "homework-3 drill"), ([6, 11, 21, 41], 81, "affine", "homework-3 drill"),
    ([1, 20, 3, 40, 5, 60], 7, "woven", "homework-3 drill"), ([125, 64, 27, 8], 1, "list", "homework-3 drill cubes falling"),
    ([100, 93, 86, 79], 72, "poly", "homework-3 drill")]


def sequence_keys():
    for seq, key, rule, where in SEQUENCES:
        if rule == "poly":
            got = next_by_differences(seq)
        elif rule in ("geom", "affine"):
            got = next_term(seq)
            if rule == "geom":
                r = F(seq[1], seq[0])
                assert all(F(b, a) == r for a, b in zip(seq, seq[1:])), f"{where}: not geometric"
                got = seq[-1] * r
        elif rule == "fib":
            assert all(seq[i] == seq[i - 1] + seq[i - 2] for i in range(2, len(seq))), f"{where}: not Fibonacci-like"
            got = seq[-1] + seq[-2]
        elif rule == "woven":
            odd, even = seq[0::2], seq[1::2]
            got = next_term(odd) if len(seq) % 2 == 0 else next_term(even)
        else:
            got = None
            if where.endswith("cubes"):
                got = (len(seq) + 1) ** 3
            elif "cubes plus 1" in where:
                got = (len(seq) + 1) ** 3 + 1
            elif "cubes falling" in where:
                got = (5 - len(seq)) ** 3
            elif "primes" in where:
                p = seq[-1] + 1
                while any(p % q == 0 for q in range(2, int(p ** 0.5) + 1)):
                    p += 1
                got = p
        assert got == key, f"sequence_keys: {where} {seq} by rule {rule} gives {got}, key {key}"
        # the stated rule must fit every term shown, and a polynomial key must be the difference-table key
        if rule == "poly":
            assert next_by_differences(seq) == key
        if rule in ("affine",):
            assert next_by_differences(seq) is None, f"{where}: an affine sequence must not settle by differences"
    check("sequence_keys", True, f"{len(SEQUENCES)} sequence items: each key follows its stated rule, which fits every term shown")
    # 1, 2, 4, 8, 16: the single fourth difference taken as constant gives 31, the circle-regions count
    by_diff = sum(row[-1] for row in difference_table([1, 2, 4, 8, 16]))
    check("ambiguity_noted", by_diff == 31 and next_by_differences([1, 2, 4, 8, 16]) is None
          and [math.comb(n, 4) + math.comb(n, 2) + 1 for n in range(1, 7)] == [1, 2, 4, 8, 16, 31],
          "l10 screens[6].explain: 1, 2, 4, 8, 16 goes to 31 as the circle-regions count (OEIS A000127); doubling gives 32")
    check("tenth_term", 10 * 11 == 110 and all(n * (n + 1) == v for n, v in enumerate([2, 6, 12, 20, 30], 1)), "l10 screens[5]")


# ---- l11: one-line models
def word_problems():
    check("profit_line", abs(300 * (4.40 - 4.25) - (300 * 4.40 - 300 * 4.25)) < 1e-9 and abs(300 * 0.15 - 45) < 1e-9, "l11 screens[0]")
    check("return_on_cost", abs(0.15 / 4.25 - 45 / 1275) < 1e-12 and abs(0.15 / 4.25 - 0.0353) < 1e-4 and 0.15 / 4.5 < 0.15 / 4.25,
          "l11 screens[5]: the share count cancels; a little over 3.33%")
    check("simple_interest", F(1250 * 4 * 9, 1200) == F(75, 2) and 2400 * 0.05 * 6 / 12 == 60 and 3600 * 0.05 * 4 / 12 == 60
          and abs(800 * 0.03 * 6 / 12 - 12) < 1e-12 and abs(2000 * 0.06 * 3 / 12 - 30) < 1e-12,
          "l11 screens[3], [7], [8], review-3 items[6], homework-3 drill")

    def minutes_between(t1, t2):
        h1, m1 = map(int, t1.split(":"))
        h2, m2 = map(int, t2.split(":"))
        return (h2 * 60 + m2 - h1 * 60 - m1) % 1440
    check("clock", minutes_between("14:47", "17:25") == 158 == 2 * 60 + 38 and minutes_between("22:35", "02:25") == 230 == 3 * 60 + 50
          and minutes_between("09:50", "11:15") == 85 and minutes_between("09:38", "11:25") == 107 == 60 + 47
          and minutes_between("13:52", "17:16") == 204 == 3 * 60 + 24 and minutes_between("08:45", "10:20") == 95,
          "l11 screens[1], [9], quiz[1], review-3 items[9], homework-3 drill")
    check("fills", 0.35 * 2400 == 840 and 0.65 * 2400 == 1560 and 0.35 * 3600 == 1260 and 0.35 * 4800 == 1680,
          "l11 screens[6], quiz[2], review-3 items[2]")
    check("vat", 84 / 1.2 == 70 and 1200 / 1.2 == 1000 and 0.8 * 84 != 70, "l11 quiz[3], homework-3 drill: divide by 1.2")
    check("short_pnl", abs(1500 * (12.52 - 12.60) + 120) < 1e-9 and 1500 * (12.52 - 12.60) < 0, "l11 screens[11]: short, price up, loss")
    check("compensation", abs((3 + 4.5 + 8) - 0.03 - 15.47) < 1e-9, "l11 screens[4]")


# ---- l12: net score, the three-type sort applied consistently, block data
ROWS_12 = [("Q8", 5.3, False, "S"), ("Q13", 7.1, False, "M"), ("Q14", 7.5, False, "M"), ("Q19", 6.2, False, "M"),
           ("Q21", 4.4, False, "S"), ("Q24", 7.0, False, "M"), ("Q26", 7.9, False, "M"), ("Q27", 7.4, False, "M"),
           ("Q30", 16.9, True, "T"), ("Q31", 21.8, True, "T"), ("Q34", 8.4, False, "M"), ("Q38", 6.8, False, "M"),
           ("Q40", 15.8, True, "T"), ("Q55", 18.6, True, "T"), ("Q60", 17.0, False, "M")]


def sort_rule(seconds, right):
    if not right:
        return "S" if seconds <= 6 else "M"
    return "T" if seconds > 12 else None


def mock_review():
    for q, s, right, key in ROWS_12:
        assert sort_rule(s, right) == key, f"l12 screens[6]/[8]: {q} sorts as {sort_rule(s, right)}, key {key}"
    check("sort_rule", sort_rule(11.8, True) is None and sort_rule(3.5, False) == "S" and sort_rule(9, False) == "M" and sort_rule(15, True) == "T",
          "l12 screens[8] Q49, quiz[2], review-3 items[7]")
    check("net", (16 - 4, 14 - 6, 19 - 1, 8 - 0) == (12, 8, 18, 8) and 57 - 11 == 46 == 2 * 57 - 68 and 66 - 9 - 9 == 48
          and 2 * 60 - 74 == 46 and 2 * 58 - 71 == 45, "l12 screens[5], [9], [10], quiz[1], review-3 items[3]")
    check("net_identity", all(r - (a - r) == 2 * r - a for a in range(0, 81) for r in range(0, a + 1)), "l12 screens[10]: net = 2r - a")
    m_rows = [q for q, s, r, k in ROWS_12 if k == "M" and q != "Q60"]
    fractions = {"Q14", "Q19", "Q24", "Q26", "Q38"}
    check("fraction_gaps", len(m_rows) == 8 and len(fractions & set(m_rows)) == 5 and len([1 for q, s, r, k in ROWS_12 if k == "T" and q != "Q55"]) == 3,
          "l12 screens[6].explain: five of eight method gaps are fractions, three time losses")
    check("block3_overrun", abs((18.6 - 6) + (17.0 - 6) - 23.6) < 1e-9 and 23.6 > 19, "l12 screens[8].explain")
    # finding 9: a guessed answer in a forward-only test is fast and wrong two times in three, so the rule reads it as a slip
    guess_secs = 3
    check("guess_reads_as_slip", sort_rule(guess_secs, False) == "S", "finding 9: the seconds rule cannot tell a guess from a slip (documented, not a failure of arithmetic)")


# ---- homework-3 items[2]: the mock generator's own guarantees, with the answers recomputed
def mock_generator_checks():
    import re
    ns = {}
    import json
    with open("app/content/courses/mental-pressure/homework-3.json", encoding="utf-8") as fh:
        hw = json.load(fh)
    item = next(i for i in hw["items"] if i["id"] == "h-mock-generator")
    exec(item["widget"]["solution"], ns)
    paper = ns["mock_generator"](80)
    assert len(paper) == 80

    def value(text):
        return F(text.replace(",", ""))

    def recompute(text):
        text = text.replace("−", "-")
        m = re.fullmatch(r"(\S+) ([+\-×÷]) (\S+)", text)
        if m:
            a, op, b = m.groups()
            if "/" in a:
                a, b = F(a), F(b)
            else:
                a, b = value(a), value(b)
            return {"+": a + b, "-": a - b, "×": a * b, "÷": a / b}[op]
        m = re.fullmatch(r"(\S+)% of (\S+)", text)
        if m:
            return value(m.group(1)) * value(m.group(2)) / 100
        m = re.fullmatch(r"(.*), \?", text)
        if m:
            seq = [int(v.replace(",", "")) for v in m.group(1).split(", ")]
            return next_term(seq)
        raise ValueError(text)
    def fr(v):   # options and answers arrive as int, float or Fraction; str() of a float is its shortest decimal
        return v if isinstance(v, F) else F(str(v))
    for text, opts, ans in paper:
        exp = recompute(text)
        assert F(exp) == fr(ans), f"mock answer {text}: {ans} against {exp}"
        assert len(opts) == 4 and len(set(fr(o) for o in opts)) == 4 and sum(fr(o) == fr(ans) for o in opts) == 1
        lo, hi = float(ans) / 10 * (1 - 1e-9), float(ans) * 10 * (1 + 1e-9)   # options arrive as floats
        assert all(float(o) > 0 and lo <= float(o) <= hi for o in opts), f"option out of range for {text}: {opts}"
    check("mock_generator", ns["mock_generator"](5) == ns["mock_generator"](5) and ns["mock_generator"](5) != ns["mock_generator"](6),
          "homework-3 items[2]: 80 answers recompute by the stated rules; four distinct near options; a seed fixes a paper")


if __name__ == "__main__":
    checkpoints()
    greedy_optimal()
    guess_value()
    difference_checks()
    next_term_checks()
    sequence_keys()
    word_problems()
    mock_review()
    mock_generator_checks()
    print("L3 concepts: all checks passed")
