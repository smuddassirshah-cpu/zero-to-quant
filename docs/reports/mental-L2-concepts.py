#!/usr/bin/env python3
"""Concept checks for mental level 2 (l5 to l8, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/mental-L2-concepts.py
Each check names its ledger row (docs/reports/audit-mental-1-3-ledger.md).
Exit 0 means every checked claim holds. A check that fails because the content is
wrong would be marked EXPECTED_FAIL and kept failing; this level has none.
Claims that are true only under a hypothesis the text drops are demonstrated and
printed as "note" lines (findings in docs/reviews/audit-mental-1-3.md), not asserted.
After the fix pass the corrected claims are asserted, marked "(corrected claim, fix pass)".
"""
import json
import math
import os
from fractions import Fraction as F

BASE = os.path.join("app", "content", "courses", "mental")


def load(name):
    with open(os.path.join(BASE, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def check(name, cond, msg):
    assert cond, f"{name}: {msg}"
    print(f"ok  {name}")


def note(name, msg):
    print(f"note {name}: {msg}")


def wrongs(widget):
    return {w["id"]: w["value"] for w in widget.get("wrong", []) if "value" in w}


def cells(value, n=12):
    return sorted(f"r{r}c{c}" for r in range(1, n + 1) for c in range(1, n + 1) if r * c == value)


def digit_sum(n):
    return sum(int(c) for c in str(n))


# ---- l5: the 12 by 12 table
def tables():
    d = load("l5-tables")
    check("l5_cells_24", cells(24) == sorted(d["screens"][0]["widget"]["answer"]) and len(cells(24)) == 6,
          "l5 screens[0]: six cells hold 24")
    check("l5_cells_56", cells(56) == sorted(d["screens"][5]["widget"]["answer"]) == ["r7c8", "r8c7"],
          "l5 screens[5]: 56 appears only as 7 x 8 and 8 x 7")
    pairs = {(min(a, b), max(a, b)) for a in range(1, 13) for b in range(1, 13)}
    check("l5_78_facts", len(pairs) == 78 == 12 + 132 // 2 and d["quiz"][3]["widget"]["answer"] == 78,
          "l5 screens[0].explain, summary.ideas[0], quiz[3]: 144 cells, 78 unordered facts")
    stated = [d["screens"][6]["prose"], d["objectives"][2]]
    check("l5_halves", len(pairs) == 78 and 144 // 2 == 72 == wrongs(d["quiz"][3]["widget"])["halved"]
          and all("144 cells" in s and "78 facts" in s and "halve" not in s for s in stated),
          "(corrected claim, fix pass) l5 screens[6].prose and objectives[2]: symmetry cuts 144 cells to 78 facts, not 72")
    # nines row: digit sums
    row = [9 * n for n in range(1, 13)]
    not9 = [p for p in row if digit_sum(p) != 9]
    check("l5_nines_digit_sum", not9 == [99] and d["screens"][1]["widget"]["answer"] == ["r1c11"],
          "l5 screens[1]: 99 is the one product in the 9 row whose digits do not add to 9")
    check("l5_digit_sum_multiple_of_9", all(digit_sum(9 * n) % 9 == 0 for n in range(1, 100000)),
          "l5 summary.formula.note, screens[1].explain: the digits of 9n add to a multiple of 9")
    check("l5_slips_caught", digit_sum(62) != 9 and digit_sum(118) != 9 and 9 * 7 == 63 and 9 * 12 == 108,
          "l5 screens[2].explain: the digit sum catches 62 and 118")
    ok = all(9 * n == 10 * n - n and 11 * n == 10 * n + n and 12 * n == 10 * n + 2 * n for n in range(0, 1000))
    check("l5_row_rules", ok, "l5 screens[6].prose: 9n, 11n and 12n rules for any whole n")
    check("l5_eleven_repeat", all(11 * n == int(f"{n}{n}") for n in range(1, 10)) and 11 * 12 != 1212,
          "l5 screens[3]: 11 x n repeats the digit up to 9 only")
    check("l5_options", 120 - 12 == 108 == 9 * 12 and 90 + 12 == 102 and 120 - 9 == 111 and 99 + 12 == 111,
          "l5 screens[6]: only 120 - 12 is 9 x 12")
    vals = [r[3]["answer"] for r in d["screens"][8]["widget"]["rows"]]
    check("l5_transfer", vals == [7 * 8, 9 * 12, 12 * 11, 56 + 108 + 132], "l5 screens[8]: £296")


# ---- l6: splitting and the grid method
def splitting():
    ok = all((a + b) * c == a * c + b * c for a in range(0, 100, 10) for b in range(10) for c in range(13))
    check("l6_distributive", ok, "l6 screens[7].prose: (a + b) x c = a x c + b x c")
    ok = all((a + b) * (c + e) == a * c + a * e + b * c + b * e for a in range(0, 100, 10) for b in range(10) for c in (0, 10) for e in range(10))
    check("l6_four_pieces", ok, "l6 summary.formula.note, screens[6].explain: two splits give four pieces")
    # 11 shortcut: digits apart, sum between, carrying when the sum is 10 or more
    def eleven(n):
        a, b = divmod(n, 10)
        return 100 * a + 10 * (a + b) + b
    check("l6_eleven_shortcut", all(eleven(n) == 11 * n for n in range(10, 100)),
          "l6 screens[5]: 11 x (two-digit) = digits apart with their sum between, carried as a number")
    no_carry = [n for n in range(10, 100) if sum(divmod(n, 10)) <= 9]
    check("l6_eleven_no_carry", all(str(11 * n) == f"{n // 10}{n // 10 + n % 10}{n % 10}" for n in no_carry) and len(no_carry) == 45,
          "l6 screens[5]: written as three digits the shortcut is literal only when the digits add to 9 or less (45 of 90)")
    d = load("l6-splitting")
    w = d["screens"][3]["widget"]
    check("l6_79x8", w["answer"] == 79 * 8 == 560 + 72 and wrongs(w)["dropped-carry"] == 532 and wrongs(w)["rounded"] == 80 * 8,
          "l6 screens[3]: 632")
    check("l6_12x87", [r[1]["answer"] for r in d["screens"][4]["widget"]["rows"]] == [800, 70, 160, 14, 12 * 87] and 870 + 174 == 1044,
          "l6 screens[4]: 1044")
    check("l6_trap", 12 * 47 == 564 == 400 + 70 + 80 + 14 and 10 * 40 + 2 * 7 == 414 and 414 + 70 == 484 and 414 + 80 == 494,
          "l6 screens[6]: 564; one-strip options 484 and 494")
    check("l6_transfer", 8 * F("36.25") == 290 == d["screens"][8]["widget"]["answer"] and 8 * 36 == 288, "l6 screens[8]: £290.00")
    check("l6_quiz", 7 * 86 == 602 and 12 * 34 == 408 and 11 * 79 == 869 and 9 * 58 == 522 == 450 + 72, "l6 quiz[0..3]")
    # screens[1]: is "both pieces are table facts" enough to single out the cut at 20? (finding 5)
    table = {a * b for a in range(1, 13) for b in range(1, 13)}
    both = [(a, 23 - a) for a in range(1, 23) if a <= 12 and 23 - a <= 12]
    assert 84 in table and 77 in table
    # (corrected claim, fix pass) the key is justified by a carry-free addition, which the 12 and 11 cut lacks
    def carries(x, y):
        return any((x // 10 ** i) % 10 + (y // 10 ** i) % 10 > 9 for i in range(4))
    s1 = d["screens"][1]
    texts = [s1["widget"]["options"][1]["why"], s1["feedback"]["generic"], s1["explain"]["text"]]
    check("l6_cut_criterion", both == [(11, 12), (12, 11)] and carries(84, 77) and not carries(140, 21)
          and 84 + 77 == 140 + 21 == 161 and all("carry" in t for t in texts)
          and not any("both pieces are table facts" in t for t in texts),
          "(corrected claim, fix pass) l6 screens[1]: 140 + 21 adds without a carry, 84 + 77 needs one")


# ---- l7: compensating, halving and doubling
def near_round():
    ok = all(n * (100 - k) == 100 * n - k * n for n in range(0, 200) for k in range(0, 20))
    check("l7_compensate", ok, "l7 summary.formula: n(100 - k) = 100n - kn")
    ok = all(2 * (5 * n) == 10 * n and 4 * (25 * n) == 100 * n and 4 * n == 2 * (2 * n) for n in range(0, 1000))
    check("l7_halving_rules", ok, "l7 screens[7].prose: 5n = 10n / 2, 25n = 100n / 4; screens[5]: 4n is two doublings")
    d = load("l7-near-round")
    keys = [(0, 7 * 99), (1, 7 * 97), (2, 9 * 46), (3, 5 * 68), (4, 7 * 25), (5, 4 * 87), (8, 250 * 12)]
    check("l7_keys", all(d["screens"][i]["widget"]["answer"] == v for i, v in keys), "l7 screens[0..5], [8]: keyed products")
    check("l7_trap", 8 * 98 == 784 == 800 - 16 and 800 - 2 == 798 and 800 - 8 == 792 and 800 + 16 == 816, "l7 screens[6]: 784")
    check("l7_quiz", 6 * 99 == 594 and 5 * 86 == 430 and F("0.99") * 6400 == 6336 and F("0.9") * 6400 == 5760 and 8 * 51 == 408,
          "l7 quiz[0..3]")
    check("l7_derive", F(12 * 100, 4) == F(600, 2) == 300 == 12 * 25, "l7 screens[7]: 12 x 25 = 300")


# ---- l8: squares, stepping, difference of two squares
def squaring():
    ok = all((a + b) ** 2 == a * a + 2 * a * b + b * b for a in range(0, 100, 10) for b in range(10))
    check("l8_square_of_sum", ok, "l8 screens[2].prose, summary.formula")
    check("l8_step", all((n + 1) ** 2 == n * n + 2 * n + 1 for n in range(0, 1000)), "l8 screens[3].prose: (n + 1)^2 = n^2 + 2n + 1")
    d = load("l8-squaring")
    sq = [r[1]["answer"] for r in d["screens"][3]["widget"]["rows"][1:5]]
    check("l8_squares_16_19", sq == [256, 289, 324, 361] and [b - a for a, b in zip([225] + sq, sq + [400])] == [31, 33, 35, 37, 39],
          "l8 screens[3]: 256, 289, 324, 361; steps 31, 33, 35, 37, 39")
    check("l8_diff_squares", all((a - b) * (a + b) == a * a - b * b for a in range(0, 100) for b in range(0, 100)),
          "l8 screens[6].prose: (a - b)(a + b) = a^2 - b^2")
    # "For two numbers either side of a round number, the strips always cancel" (finding 6)
    total, cancel = 0, 0
    for r in range(20, 100, 10):
        for lo in range(r - 9, r):
            for hi in range(r + 1, r + 10):
                total += 1
                g, h = r - lo, hi - r
                # strips are +r*h and -r*g; they cancel only when g == h
                if lo * hi == r * r - g * h and r * h - r * g == 0:
                    cancel += 1
    check("l8_equal_gaps_only", cancel == 8 * 9 and total == 8 * 81,
          "strips cancel exactly when the two gaps are equal")
    assert 18 * 21 == 378 != 400 - 4 and 18 * 21 != 400 - 1
    # (corrected claim, fix pass) every general statement now says "the same distance either side"
    general = [d["screens"][4]["explain"]["text"], d["screens"][6]["prose"], d["summary"]["ideas"][2], d["objectives"][2]]
    check("l8_either_side", all("the same distance either side" in s for s in general)
          and "always cancel" not in d["screens"][6]["explain"]["text"],
          "(corrected claim, fix pass) l8 screens[4].explain, screens[6].prose, summary.ideas[2], objectives[2]: equal gaps named")
    gaps = [(load("l8-squaring")["quiz"][1]["prose"], 18, 22, 20), (load("review-2")["items"][9]["prose"], 17, 23, 20),
            (load("homework-2")["items"][5]["prose"], 37, 43, 40)]
    check("l8_gap_named", all(f"sit {r - lo} either side of {r}" in p and r - lo == hi - r for p, lo, hi, r in gaps),
          "(corrected claim, fix pass) l8 quiz[1], review-2 items[9], homework-2 items[5]: the equal gap is stated")
    keys = {0: 169, 2: 289, 4: 399}
    check("l8_keys", all(d["screens"][i]["widget"]["answer"] == v for i, v in keys.items()) and 13 * 13 == 169 and 17 * 17 == 289 and 19 * 21 == 399,
          "l8 screens[0], [2], [4]")
    check("l8_19x21_slips", 361 + 2 * 19 == 399 and 441 - 2 * 21 == 399, "l8 screens[4] byKey: from 19^2 add two 19s; from 21^2 take two 21s")
    check("l8_trap", 14 * 14 == 196 and 100 + 16 == 116 and 116 + 40 == 156 and 100 + 80 + 8 == 188, "l8 screens[5]")
    w = d["screens"][7]["widget"]
    check("l8_variance", F(str(w["answer"])) == F("0.18") ** 2 and F(str(wrongs(w)["each-part"])) == F("0.1") ** 2 + F("0.08") ** 2
          and F("0.1") * F("0.08") == F("0.008"), "l8 screens[7]: 0.18^2 = 0.0324; the dropped strips are 0.008 each")
    # variances of independent risks add, volatilities do not (seeded simulation and exact algebra)
    import random
    rng = random.Random(8)
    n = 200000
    xs = [rng.gauss(0, 0.18) for _ in range(n)]
    ys = [rng.gauss(0, 0.24) for _ in range(n)]
    var = lambda v: sum(t * t for t in v) / len(v) - (sum(v) / len(v)) ** 2
    vs = var([a + b for a, b in zip(xs, ys)])
    check("l8_variances_add", abs(vs - (0.18 ** 2 + 0.24 ** 2)) < 0.002 and abs(math.sqrt(vs) - 0.30) < 0.005 and abs(math.sqrt(vs) - 0.42) > 0.1,
          "l8 screens[7].explain: independent variances add (0.0324 + 0.0576 = 0.09, vol 0.30), volatilities do not (0.18 + 0.24 = 0.42)")
    check("l8_root_252", round(math.sqrt(252)) == 16 and 16 ** 2 - 252 == 4 and 252 - 15 ** 2 == 27 and abs(0.01 * math.sqrt(252) - 0.16) < 0.002,
          "l8 quiz[2]: sqrt(252) is nearest 16; 1% a day is about 16% a year")
    # the nearest square gives the nearest whole root for every whole n (no integer lies between k^2 + k + 1/4 and k^2 + k + 1/2)
    ok = all(min((abs(k * k - n), k) for k in range(1, 40))[1] == int(math.sqrt(n) + 0.5) for n in range(1, 1000))
    check("l8_nearest_square", ok, "l8 quiz[2].explain: comparing 252 with 15^2 and 16^2 is a valid way to find the nearest whole root")
    check("l8_quiz", 16 ** 2 == 256 == 225 + 31 and 18 * 22 == 396 and 21 ** 2 == 441, "l8 quiz[0], [1], [3]")


# ---- review-2 and homework-2
def review_homework():
    r = load("review-2")
    ans = {it["id"]: it["widget"].get("answer") for it in r["items"]}
    check("review2_keys", ans["rv-six-eight"] == 48 and ans["rv-twelve-nine"] == 108 and ans["rv-eight-sixty-seven"] == 8 * 67
          and 11 * 57 == 627 and 12 * 63 == 756 == 630 + 126 and ans["rv-four-ninety-eight"] == 4 * 98
          and ans["rv-fee"] == F(3, 100) * 1200 and ans["rv-return-notional"] == F("0.025") * 400000
          and ans["rv-eighteen-squared"] == 18 ** 2 == 400 - 40 - 40 + 4 and ans["rv-seventeen-twenty-three"] == 17 * 23 == 400 - 9,
          "review-2 items[0..9]")
    h = load("homework-2")
    ans = {it["id"]: it.get("widget", {}).get("answer") for it in h["items"]}
    check("hw2_keys", F(str(ans["hw-nine-shares"])) == 9 * F("47.80") and ans["hw-twelve-ninety-six"] == 12 * 96 == 1200 - 48 == 960 + 192
          and ans["hw-hedge"] == F("0.98") * 8400 and ans["hw-notional"] == F("0.0025") * 4800000
          and ans["hw-thirty-seven-forty-three"] == 37 * 43 == 1600 - 9 and ans["hw-eighty-five"] == 85 ** 2
          and F(str(ans["hw-variance"])) == F("0.24") ** 2, "homework-2 items[1..8]")
    check("hw2_ends_in_5", all((10 * n + 5) ** 2 == 100 * n * (n + 1) + 25 for n in range(0, 1000)),
          "homework-2 items[7].explain: (10n + 5)^2 = 100n(n + 1) + 25 for any number ending in 5")
    check("hw2_derive", all((10 + b) ** 2 == 100 + 20 * b + b * b for b in range(10)), "homework-2 items[6]: (10 + b)^2 = 100 + 20b + b^2")
    check("hw2_longform", 12 * 49 == 588 == 600 - 12 == 490 + 98 == 400 + 90 + 80 + 18 and 600 - 1 == 599 and 400 + 18 == 418,
          "homework-2 items[9] model: £588 three ways; slips 599 and 418")


if __name__ == "__main__":
    tables()
    splitting()
    near_round()
    squaring()
    review_homework()
    print("L2 concepts: all checks passed")
