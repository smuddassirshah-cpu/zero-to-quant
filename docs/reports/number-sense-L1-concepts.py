#!/usr/bin/env python3
"""Concept checks for number-sense level 1 (l1 to l5, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/number-sense-L1-concepts.py
Each check names its ledger row (docs/reports/audit-number-sense-1-3-ledger.md).
Exit 0 means every checked claim holds on the domain the lesson uses. A line
starting "note" records where a claim stops holding outside that domain; those
are the `imprecise` findings of docs/reviews/audit-number-sense-1-3.md and are
not asserted. A failing assert names the claim.

Fix pass: the three notes (findings 1 to 3) are now checks marked "(corrected
claim, fix pass)"; each recomputes the corrected claim and asserts the content
states it and no longer states the old wording.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

COURSE = Path("app/content/courses/number-sense")
N = 0


def txt(file, *path):
    d = json.loads((COURSE / file).read_text(encoding="utf-8"))
    for p in path:
        d = d[p]
    return d


def check(name, cond, msg):
    global N
    assert cond, f"{name}: {msg}"
    N += 1
    print(f"ok  {name}")


def note(name, msg):
    print(f"note {name}: {msg}")


R = range(1, 13)


# ---- l1: a fraction as a count of equal pieces, a distance from 0, top > bottom
def reading_a_fraction():
    check("unit_fraction_order", all(F(1, a) > F(1, b) for a in R for b in R if a < b),
          "l1 screens[1], quiz[2]: more pieces from the same whole means smaller pieces")
    check("top_bigger_than_bottom", all((F(a, b) > 1) == (a > b) for a in R for b in R),
          "l1 screens[6], summary.ideas[2]: the amount passes one whole exactly when the top is bigger")
    check("bar_a_vs_bar_b", F(3, 4) == F(6, 8) and F(3, 4) > F(3, 8), "l1 screens[1]: 3 quarters cover 6 eighths")
    check("unequal_pieces", F(2, 2 + 1 + 1) == F(1, 2) and F(1, 1 + 1 + 2) == F(1, 4),
          "l1 screens[7] (colSizes 2,1,1) is a half; review-1 items[8] (1,1,2) is a quarter")
    check("fraction_of_amount", F(3, 4) * 12 == 9 and F(2, 5) * 20 == 8 and F(3, 5) * 20 == 12,
          "l1 screens[9], quiz[3]; l4 quiz[1]: a fraction of an amount is a count of equal shares")


# ---- l2: equivalent fractions
def equivalence():
    ok = all(F(a * k, b * k) == F(a, b) for a in R for b in R for k in range(1, 30))
    check("equivalent_multiply", ok, "l2 screens[6]: multiplying top and bottom by the same non-zero number keeps the amount")
    try:
        F(2 * 0, 3 * 0)
        zero_ok = True
    except ZeroDivisionError:
        zero_ok = False
    prose6 = txt("l2-same-amount.json", "screens", 6, "prose")
    fnote = txt("l2-same-amount.json", "summary", "formula", "note")
    check("equivalent_zero", not zero_ok and ok and "same number, as long as it is not 0" in prose6
          and fnote.startswith("Any number except 0 works") and "Any number works" not in fnote,
          "(corrected claim, fix pass) l2 screens[6].prose, summary.formula.note: the same number, other than 0 "
          "(2x0/3x0 = 0/0 has no value) (finding 1)")
    # adding the same k to both: equal only when k = 0 or the fraction is 1
    same = [(a, b, k) for a in R for b in R for k in range(1, 13) if F(a + k, b + k) == F(a, b)]
    check("adding_changes_unless_one", all(a == b for a, b, k in same),
          "l2 screens[6] options, summary.ideas[1]: adding k > 0 to both changes the amount whenever top != bottom")
    ones = [(a, b, k) for a in R for b in R for k in range(1, 13) if a == b]
    idea1 = txt("l2-same-amount.json", "summary", "ideas", 1)
    check("adding_same_number", sorted(same) == sorted(ones) and F(3 + 1, 3 + 1) == F(3, 3)
          and idea1.endswith("changes the amount, unless the fraction is exactly one whole."),
          f"(corrected claim, fix pass) l2 summary.ideas[1]: adding k > 0 to both leaves the amount unchanged in exactly "
          f"the {len(ones)} cases with top = bottom, e.g. 3/3 -> 4/4 (finding 2)")
    check("one_piece_short", all(F(n - 1, n) < F(n, n + 1) for n in range(2, 60)),
          "l2 screens[5], quiz[2]: one piece short of a whole is bigger when the missing piece is smaller")
    check("compare_common_size", F(2, 3) > F(3, 5) and F(3, 8) < F(2, 5) and F(5, 6) < F(7, 8) and F(5, 8) > F(3, 5),
          "l2 screens[4], screens[8], quiz[2]; review-1 items[5]")
    check("lowest_terms", F(9, 12) == F(3, 4) and F(3, 4).denominator == 4 and F(6, 9) != F(3, 4),
          "l2 quiz[3]: simplest form of 9/12 is 3/4; 6/9 is a different amount")
    check("order_hw1", sorted([F(3, 4), F(1, 2), F(2, 3), F(3, 5)]) == [F(1, 2), F(3, 5), F(2, 3), F(3, 4)],
          "homework-1 items[8]")


# ---- l3: adding with a common size; tops-and-bottoms is the mediant
def addition():
    ok = True
    for a, b, c, d in product(range(1, 9), repeat=4):
        s = F(a, b) + F(c, d)
        for m in (b * d, 2 * b * d, 3 * b * d):          # any common size gives the same amount
            ok &= F(a * (m // b) + c * (m // d), m) == s
    check("any_common_size", ok, "l3 screens[4].explain, summary.formula.note: any common size gives the same total")
    med_ok = True
    for a, b, c, d in product(range(1, 9), repeat=4):
        x, y, med = F(a, b), F(c, d), F(a + c, b + d)
        med_ok &= min(x, y) <= med <= max(x, y) and med < x + y
    check("tops_and_bottoms_is_too_small", med_ok,
          "l3 screens[6], summary.trap: adding tops and bottoms never exceeds the larger part, so it is never the total")
    check("l3_totals", F(1, 2) + F(1, 3) == F(5, 6) and F(1, 3) + F(1, 4) == F(7, 12)
          and F(3, 4) - F(1, 3) == F(5, 12) and F(3, 4) + F(1, 2) == F(5, 4) and F(2, 3) + F(1, 5) == F(13, 15),
          "l3 screens[1] to [8]")
    check("l3_alt_readings", F(2, 7) != F(7, 12) and F(4, 3) != F(1, 2) and F(6, 8) != F(3, 2),
          "l3 wrong[] values are not correct under any valid method")


# ---- l4: multiplying fractions
def multiplication():
    ok = True
    for a, b, c, d in product(range(1, 9), repeat=4):
        # area model: a of b rows, c of d columns share a*c of b*d cells
        cells = sum(1 for r in range(b) for k in range(d) if r < min(a, b) and k < min(c, d))
        if a <= b and c <= d:
            ok &= F(cells, b * d) == F(a, b) * F(c, d)
        ok &= F(a, b) * F(c, d) == F(c, d) * F(a, b)
    check("area_model_rule", ok, "l4 screens[6], summary.formula: top times top over bottom times bottom; order does not matter")
    proper = [F(a, b) for b in range(2, 13) for a in range(1, b)]
    check("part_of_a_part", all(x * y < x and x * y < y for x in proper for y in proper),
          "l4 screens[5], summary.ideas[2]: the product of two amounts between 0 and 1 is smaller than both")
    whole = [(m, n) for m in range(0, 13) for n in range(0, 13) if not (m * n > m and m * n > n)]
    check("whole_number_bigger_needs_gt_one", all(m <= 1 or n <= 1 for m, n in whole),
          "l4 screens[5].prose: the product exceeds both factors exactly when both exceed 1")
    p5 = txt("l4-fraction-of-fraction.json", "screens", 5, "prose")
    gt1 = all(m * n > m and m * n > n for m in range(2, 13) for n in range(2, 13))
    check("whole_number_multiplying", gt1 and 1 * 4 == 4 and 0 * 4 == 0
          and p5.startswith("With whole numbers bigger than 1, multiplying makes things bigger"),
          "(corrected claim, fix pass) l4 screens[5].prose: for whole numbers bigger than 1 the product beats both; "
          "1 x 4 = 4 and 0 x 4 = 0 do not (finding 3)")
    check("l4_keys", F(2, 3) * F(3, 4) == F(1, 2) and F(1, 2) * F(3, 5) == F(3, 10) and F(3, 4) * 2 == F(3, 2)
          and F(1, 4) * F(2, 3) * 1200 == 200 and F(1, 3) * F(4, 5) * 2400 == 640 and F(3, 4) * F(2, 3) * 900 == 450,
          "l4 screens[1] to [8]; homework-1 items[3], items[7]")


# ---- l5: dividing by a fraction
def division():
    ok = True
    for a in range(1, 13):
        for c, d in product(range(1, 9), repeat=2):
            q = F(a) / F(c, d)
            ok &= q == a * F(d, c)                     # turn over and multiply
            ok &= q * F(c, d) == a                     # q portions of c/d make a
    check("turn_over_and_multiply", ok, "l5 screens[6], summary.formula: a / (c/d) = a x d/c")
    check("one_whole_holds", all(1 / F(c, d) == F(d, c) for c in range(1, 9) for d in range(1, 9)),
          "l5 screens[6], [7]: one whole holds the fraction turned upside down")
    proper = [F(a, b) for b in range(2, 13) for a in range(1, b)]
    check("divide_by_proper_is_bigger", all(F(n) / p > n for n in range(1, 13) for p in proper),
          "l5 screens[2], [5], summary.ideas[2]: a positive amount divided by a fraction between 0 and 1 gets bigger")
    check("leftover_counts", 1 / F(2, 3) == 1 + F(1, 3) / F(2, 3) == F(3, 2),
          "l5 screens[3]: the third left over is half a portion")
    check("divide_two_vs_half", 6 / F(1, 2) == 12 and F(6, 2) == 3, "l5 screens[5], summary.trap")
    check("l5_keys", 3 / F(3, 4) == 4 and F(3, 4) / F(1, 8) == 6 and 4 / F(2, 5) == 10
          and F(5, 2) / F(5, 8) == 4 and F(3, 4) / F(3, 8) == 2 and F(3, 4) / F(2, 3) == F(9, 8),
          "l5 screens[2], [4], [6]; homework-1 items[4], items[5]; review-1 items[7]")


# ---- homework-1 items[6]: a rise of 1/n undone by a fall of 1/(n+1)
def rise_and_fall():
    check("rise_fall_cancel", all((1 + F(1, n)) * (1 - F(1, n + 1)) == 1 for n in range(1, 50)),
          "homework-1 items[6].explain: up a quarter then down a fifth of the new price returns to the start")
    check("rise_fall_keys", 40 * F(5, 4) * F(4, 5) - 40 == 0 and 40 * (F(1, 4) - F(1, 5)) == 2,
          "homework-1 items[6]: key 0; the slip value 2 comes from taking both fractions of 40")


if __name__ == "__main__":
    reading_a_fraction()
    equivalence()
    addition()
    multiplication()
    division()
    rise_and_fall()
    print(f"L1 concepts: all {N} checks passed")
