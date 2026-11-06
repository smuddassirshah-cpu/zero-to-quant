#!/usr/bin/env python3
"""Concept checks for mental-pressure level 1 (l1 to l4, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/mental-pressure-L1-concepts.py
Each check names its ledger row (docs/reports/audit-mental-pressure-1-3-ledger.md).
Exit 0 means every checked claim holds. A failing assert names the claim.
"""
import math
from fractions import Fraction as F
from decimal import Decimal


def check(name, cond, msg):
    assert cond, f"{name}: {msg}"
    print(f"ok  {name}")


# ---- l1 screens[1].explain: near 50 a tenth of a second is worth about two points
def pace_derivative():
    deriv = 120 / 2.4 ** 2            # points per second at a 2.4 s pace
    fd = 120 / 2.3 - 120 / 2.4        # one tenth faster
    check("pace_derivative", 1.8 <= deriv / 10 <= 2.3 and 1.8 <= fd <= 2.3,
          f"l1 screens[1].explain: {deriv/10:.2f} points per tenth, finite difference {fd:.2f}")
    check("pace_steps", abs((120 / 30 - 120 / 40) - 1) < 1e-12 and abs((120 / 40 - 120 / 50) - 0.6) < 1e-12,
          "l1 screens[1].explain: 30 to 40 costs 1 s, 40 to 50 costs 0.6 s")


# ---- l1 screens[5] to [8], quiz, homework-1 items[1]: weighted pace and floor score
def score(pace_by_op, mix, seconds=120):
    pace = sum(share * pace_by_op[op] for op, share in mix.items())
    return math.floor(seconds / pace), pace


def weighted_pace():
    q = dict(add=0.25, sub=0.25, mul=0.25, div=0.25)
    s40, p = score(dict(add=2, sub=2, mul=2, div=6), q)
    check("weighted_pace", s40 == 40 and abs(p - 3) < 1e-12, "l1 screens[5]: pace 3 s, score 40")
    s53, p = score(dict(add=2, sub=2, mul=2, div=3), q)
    check("weighted_pace_53", s53 == 53 and abs(p - 2.25) < 1e-12, "l1 screens[6]: pace 2.25 s, score 53")
    ana, pa = score(dict(add=1.6, sub=2, mul=2, div=6), q)
    ben, pb = score(dict(add=2, sub=2, mul=2, div=4.8), q)
    check("trap_ana_ben", ana == 41 and ben == 44 and abs(pa - 2.9) < 1e-12 and abs(pb - 2.7) < 1e-12,
          "l1 screens[7]: Ana 2.9 s and 41, Ben 2.7 s and 44")
    # saving per question = share x seconds saved
    check("saving_rule", abs((3 - 2.9) - 0.25 * 0.4) < 1e-12 and abs((3 - 2.7) - 0.25 * 1.2) < 1e-12,
          "l1 screens[7].explain: Ana saves 0.1 s a question, Ben 0.3 s")
    q32, p = score(dict(add=2, sub=2.5, mul=4, div=6.5), q)
    check("quiz_plain_mean", q32 == 32 and abs(p - 3.75) < 1e-12, "l1 quiz[0]: equal shares make the plain mean")
    # work backwards: 0.25 d + 0.75 t = 120 / target
    d = (120 / 50 - 0.75 * 2) / 0.25
    d2 = (120 / 40 - 0.75 * 2.5) / 0.25
    check("work_backwards", abs(d - 3.6) < 1e-12 and abs(d2 - 4.5) < 1e-12, "l1 screens[9], quiz[3]: d = 3.6 and 4.5")


def option_scores():
    q = dict(add=0.25, sub=0.25, mul=0.25, div=0.25)
    base = score(dict(add=2, sub=2, mul=2, div=7), q)[0]
    div5 = score(dict(add=2, sub=2, mul=2, div=5), q)[0]
    three = score(dict(add=1.5, sub=1.5, mul=1.5, div=7), q)[0]
    add1 = score(dict(add=1, sub=2, mul=2, div=7), q)[0]
    check("option_scores", (base, div5, three, add1) == (36, 43, 41, 40),
          f"l1 screens[8] options: expected 36, 43, 41, 40, got {(base, div5, three, add1)}")
    check("largest_saving_wins", 0.25 * 2 > 0.75 * 0.5 > 0.25 * 1,
          "l1 screens[8].explain: 0.5 > 0.375 > 0.25 seconds a question")


# ---- l1 quiz[2]: expected time with a wrong first try
def expected_time():
    check("expected_time", abs(2 + 0.25 * 3 - 2.75) < 1e-12, "l1 quiz[2]: 2 + 0.25 x 3 = 2.75")


# ---- l2: cross multiplication identity over every two-digit pair; near-100 shortcut
def cross_identity():
    for x in range(10, 100):
        a, b = divmod(x, 10)
        for y in range(10, 100):
            c, d = divmod(y, 10)
            assert 100 * a * c + 10 * (a * d + b * c) + b * d == x * y, f"cross_identity fails at {x} x {y}"
    print("ok  cross_identity (8,100 pairs)")
    # squares either side of a round number, ends in 5, factor 25
    check("diff_of_squares", 52 * 48 == 50 ** 2 - 2 ** 2 and 73 * 67 == 70 ** 2 - 3 ** 2 and 34 * 26 == 30 ** 2 - 4 ** 2,
          "l2 screens[5], quiz[1], review-1 items[5]")
    check("ends_in_five", all((10 * n + 5) ** 2 == 100 * n * (n + 1) + 25 for n in range(1, 10)), "l2 quiz[2] rule")


def near100_pad():
    # (100-g)(100-h) = 100 (100-g-h) + g h: the gap product is the last two digits only when 10 <= gh < 100
    pad_needed, carry_needed = [], []
    for x in range(90, 100):
        for y in range(90, 100):
            g, h = 100 - x, 100 - y
            assert x * y == 100 * (x - h) + g * h, f"near100 identity at {x} x {y}"
            if g * h < 10:
                pad_needed.append((x, y))
            if g * h >= 100:
                carry_needed.append((x, y))
    drill_rows = [(97, 94), (98, 93), (98, 96), (95, 97), (96, 97)]
    pads = [r for r in drill_rows if r in pad_needed]
    check("near100_pad", (98, 96) in pads and (90, 90) in carry_needed,
          "l2 screens[5], quiz[3], drill row 98 x 96 = 94 then 08 needs the two-digit padding the prose never states (finding 2)")
    print(f"    near 100 on 90..99: {len(pad_needed)} pairs need a leading zero, {len(carry_needed)} need a carry")


# ---- l3: estimate and correct, one digit per round, divmod over 10,000 pairs
def estimate_and_correct(n, d):
    trials, q, r = [], 0, n
    while r >= d:
        p = 1
        while d * p * 10 <= r:
            p *= 10
        digit = r // (d * p)
        assert 1 <= digit <= 9, f"estimate_and_correct: step is not one digit at {n} / {d}"
        step = digit * p
        q += step
        r -= step * d
        trials.append(q)
    return trials, q, r


def estimate_correct():
    for n in range(0, 3000, 7):
        for d in range(11, 100, 4):
            assert estimate_and_correct(n, d)[1:] == divmod(n, d), f"estimate_correct at {n} / {d}"
    check("estimate_correct", estimate_and_correct(5016, 24) == ([200, 209], 209, 0)
          and estimate_and_correct(6048, 24) == ([200, 250, 252], 252, 0)
          and estimate_and_correct(18, 24) == ([], 0, 18),
          "l3 screens[9].explain: a zero digit skips its round; n < d gives no rounds")
    # n/d = q + (n - q d)/d and the sign of the leftover
    check("leftover_identity", F(864, 24) == 30 + F(864 - 30 * 24, 24) and (864 - 40 * 24) < 0,
          "l3 screens[7] formula; screens[1].explain: a trial above the answer leaves a negative amount")
    check("factor_tricks", 1350 * 4 // 100 == 54 and 1008 // 4 // 3 == 84 and 1170 * 2 // 30 == 78
          and F(1, 24) != F(1, 20) + F(1, 4),
          "l3 screens[3] tricks; screens[8] d1: 1/24 is not 1/20 + 1/4")
    check("sizing", 24 * 100 < 6048 < 24 * 1000 and 36 * 100 < 7236 < 36 * 1000, "l3 screens[6], quiz[3]: three digits")
    check("one_over_37", F(1, 37) == F(27, 999) and 69 ** 2 == 70 ** 2 - 2 * 70 + 1, "l3 screens[5] and [4]")


# ---- l4: places add; scaling both keeps the ratio
def decimal_places():
    import random
    rng = random.Random(4)
    for _ in range(5000):
        p, q = rng.randint(0, 4), rng.randint(0, 4)
        A, B = rng.randint(1, 999), rng.randint(1, 999)
        a, b = Decimal(A).scaleb(-p), Decimal(B).scaleb(-q)
        prod = Decimal(A * B).scaleb(-(p + q))
        assert a * b == prod, f"places add fails for {a} x {b}"
        k = max(p, q)
        if B:
            assert F(A * 10 ** (k - p), B * 10 ** (k - q)) == F(A, 10 ** p) / F(B, 10 ** q), "scale both fails"
    check("decimal_places", Decimal("0.25") * Decimal("0.4") == Decimal("0.100")
          and Decimal("0.48") / Decimal("0.012") == 40 and Decimal("0.006") * Decimal("0.5") == Decimal("0.0030"),
          "l4 screens[3], [6], [7]: count with 100 before trimming; 480 / 12 = 40")
    check("below_one_product", all(F(a, 10) * F(b, 10) < min(F(a, 10), F(b, 10)) for a in range(1, 10) for b in range(1, 10)),
          "l4 screens[0].explain: a product of two numbers below 1 is smaller than both")
    check("basis_points", abs(0.0035 * 12000 - 42) < 1e-9 and abs(0.00125 * 48000 - 60) < 1e-9,
          "l4 screens[11], homework-1 items[5]")


# ---- homework-1 items[7]: the longform model's numbers from the seed-54 table
ROUND = [("131 − 58", "sub", 1.9, True), ("240 ÷ 8", "div", 4.5, True), ("470 ÷ 5", "div", 3.4, True),
         ("143 ÷ 11", "div", 4.9, True), ("426 ÷ 6", "div", 3.1, True), ("6 × 58", "mul", 6.5, False),
         ("6 × 2", "mul", 5.9, False), ("83 − 50", "sub", 4.7, False), ("264 ÷ 11", "div", 6.9, True),
         ("84 + 64", "add", 2.3, True), ("448 ÷ 8", "div", 4.2, True), ("62 + 61", "add", 1.9, True),
         ("3 × 9", "mul", 4.1, True), ("260 ÷ 4", "div", 5.2, True), ("6 × 100", "mul", 4.5, True),
         ("14 + 79", "add", 2.0, True), ("228 ÷ 4", "div", 4.1, True), ("20 + 70", "add", 2.3, True),
         ("11 × 86", "mul", 2.8, True), ("166 − 100", "sub", 2.3, True), ("6 × 15", "mul", 3.7, True),
         ("94 − 77", "sub", 1.7, True), ("110 − 73", "sub", 4.3, False), ("7 × 29", "mul", 2.9, True),
         ("68 + 96", "add", 4.3, False), ("9 × 62", "mul", 4.7, True), ("31 + 6", "add", 2.8, True),
         ("45 − 29", "sub", 2.1, True), ("51 + 87", "add", 2.4, True), ("2 × 72", "mul", 4.1, True)]


def hw1_longform():
    tot, cnt, bad = {}, {}, {}
    for _, op, s, right in ROUND:
        tot[op] = tot.get(op, 0) + s
        cnt[op] = cnt.get(op, 0) + 1
        bad[op] = bad.get(op, 0) + (not right)
    total = sum(tot.values())
    means = {op: tot[op] / cnt[op] for op in tot}
    shares = {op: tot[op] / total for op in tot}
    check("hw1_total", abs(total - 110.5) < 1e-9, "homework-1 items[7].model: 110.5 seconds")
    check("hw1_means", abs(means["add"] - 2.571) < 0.005 and abs(means["sub"] - 2.833) < 0.005
          and abs(means["mul"] - 4.356) < 0.005 and abs(means["div"] - 4.5375) < 0.005,
          f"homework-1 items[7].model means {means}")
    check("hw1_shares", round(shares["add"] * 100) == 16 and round(shares["sub"] * 100) == 15
          and round(shares["mul"] * 100) == 35 and round(shares["div"] * 100) == 33,
          f"homework-1 items[7].model shares {shares}")
    check("hw1_slowest", max(means, key=means.get) == "div" and max(shares, key=shares.get) == "mul",
          "homework-1 items[7].model: division slowest by mean, multiplication the largest share")
    rates = {op: bad[op] / cnt[op] for op in cnt}
    check("hw1_errors", bad == dict(sub=2, mul=2, add=1, div=0) and rates["sub"] >= 0.25
          and max(rates, key=rates.get) == "sub",
          "homework-1 items[7].model: subtraction wrong 2 in 6 is flagged by the 0.25 rule")
    wrong_secs = sum(s for _, _, s, r in ROUND if not r)
    check("hw1_wrong_seconds", abs(wrong_secs - 25.7) < 1e-9, "homework-1 items[7].model: the five wrong rows took 25.7 s")
    target = tot["add"] + tot["sub"] + cnt["mul"] * 3 + cnt["div"] * 3.5
    check("hw1_target", abs(target - 90) < 1e-9 and math.floor(120 / (target / 30)) == 40,
          "homework-1 items[7].model: 3 s and 3.5 s targets give 90 s, pace 3 s, score 40")
    # the content-based sort in the model against the level-3 seconds rule (finding 9)
    by_seconds = {q: ("S" if s <= 6 else "M") for q, _, s, r in ROUND if not r}
    model = {"6 × 58": "M", "6 × 2": "S", "83 − 50": "S", "68 + 96": "S", "110 − 73": "M"}
    disagree = [q for q in model if model[q] != by_seconds[q]]
    print(f"    hw1 sort: the l12 seconds rule disagrees with the model on {disagree} (finding 9, not asserted)")


# ---- the score model: a wrong answer costs two marks against a right one; net scores
def net_scores():
    check("net_score", 59 - 5 == 54 and (58 - 12, 57 - 3) == (46, 54), "l1 screens[2], review-1 items[9]")
    check("net_two_marks", (60 - 0) - (59 - 1) == 2, "l1 screens[2].explain: a wrong answer costs two marks against a right one")


if __name__ == "__main__":
    pace_derivative()
    weighted_pace()
    option_scores()
    expected_time()
    cross_identity()
    near100_pad()
    estimate_correct()
    decimal_places()
    hw1_longform()
    net_scores()
    print("L1 concepts: all checks passed")
