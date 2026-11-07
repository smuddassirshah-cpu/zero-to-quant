"""Second-reader number script for equations Level 4 (l14 to l17, review-4, homework-4).

Every pair is solved two ways: by Cramer's rule in exact fractions, then checked by substituting back into both
equations. Every wrong[] value is rebuilt from the slip its feedback names. A stated() check that fails marks a
finding in docs/reviews/review-equations-3-4.md and passes once the fix rewords it. Checks on the review's proposed
replacement items are claim()s and pass now.
"""
import json
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("equations", 4)
E = lv.expect


def solve(a1, b1, c1, a2, b2, c2):
    """a1 x + b1 y = c1, a2 x + b2 y = c2. Cramer, then a substitution check (the second method)."""
    a1, b1, c1, a2, b2, c2 = map(F, map(str, (a1, b1, c1, a2, b2, c2)))
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    x, y = (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det
    assert a1 * x + b1 * y == c1 and a2 * x + b2 * y == c2
    return x, y


def pair(label, sys_, want):
    got = solve(*sys_)
    lv.claim(got == tuple(F(str(w)) for w in want), f"{label}: solution {want}", f"got {got}")


def roots(f, lo=-50, hi=50):
    return [x for x in range(lo, hi + 1) if f(x) == 0]


# ---------------- l14 ----------------
pair("l14 s0-s3 cinema", (2, 1, 11, 3, 1, 15), (4, 3))
lv.claim(4 * 4 + 3 == 19 and F(19 - 11, 2) == 4, "l14 s1: third order fits, 8 / 2 = 4")
E("l14", "screens[0].widget.wrong[0].value", F(15, 3))
E("l14", "screens[0].widget.wrong[1].value", F(11, 2))
lv.claim(abs(26 / 7 - 3.71) <= 0.02, "l14 s0 per-item: 26/7 = 3.714 within 0.02 of 3.71")
E("l14", "screens[2].widget.wrong[0].value", 11 - 4)
E("l14", "screens[2].widget.wrong[1].value", 15 - 4)
E("l14", "screens[2].explain.text", 3 * 4 + 3)
E("l14", "screens[3].widget.states.m-add.tex", 11 + 15)
pair("l14 s4", (3, 2, 16, 5, -2, 16), (4, 2))
E("l14", "screens[4].widget.states.s1.tex", 32)
lv.claim((5 - 3, -2 - 2, 16 - 16) == (2, -4, 0), "l14 s4 m-sub: second minus first is 2x - 4y = 0")
pair("l14 s5 cafe", (4, 2, 13, 2, 3, 10.5), (2.25, 2))
E("l14", "screens[5].widget.states.s1.tex", 2 * 10.5)
lv.claim((4 - 2, 2 - 3, 13 - 10.5) == (2, -1, 2.5) and (4 + 4, 2 + 6, 13 + 21) == (8, 8, 34) and 21 - 13 == 8, "l14 s5 states m-early, m-add, 4k = 8")
pair("l14 s6 trap", (5, 2, 31.5, 3, 2, 20.5), (5.5, 2))
E("l14", "screens[6].widget.options[1].text", 31.5 - 20.5)
E("l14", "screens[6].widget.options[2].text", 31.5 + 20.5)
pair("l14 s7", (4, 3, 18, 1, -3, -3), (3, 2))
E("l14", "screens[7].explain.text", 4 * 3 + 3 * 2)
pair("l14 s8", (3, 2, 23, 1, 2, 13), (5, 4))
pair("l14 s9", (3, 2, 62.5, 5, 2, 92.5), (15, 8.75))
E("l14", "screens[9].widget.wrong[1].value", 62.5 / 2)
E("l14", "screens[9].widget.wrong[2].value", 92.5 - 62.5)
E("l14", "screens[9].explain.text", 5 * 15 + 2 * 8.75)
pair("l14 quiz[0]", (1, 1, 12, 1, -1, 2), (7, 5))
pair("l14 quiz[1]", (4, 3, 25, 2, 3, 17), (4, 3))
lv.claim(solve(2, 1, 11, 2, 1, 12) is None and 12 - 11 == 1, "l14 quiz[2]: no solution, 0 = 1")
pair("l14 quiz[3]", (2, 5, 20, 3, -5, 5), (5, 2))

# ---------------- l15 ----------------
pair("l15 s0-s2 ticket and drink", (1, 1, 10, -1, 1, 2), (4, 6))
E("l15", "screens[0].widget.wrong[1].value", 10 - 2)
pair("l15 s3", (-3, 1, -1, 2, 1, 14), (3, 8))
lv.claim(F(14, 5) * 3 - 1 == F('7.4'), "l15 s3 lost-one: 5x = 14, y = 3(2.8) - 1 = 7.4")
pair("l15 s4", (1, 1, 9, 3, 2, 22), (4, 5))
lv.claim(roots(lambda x: 3 * x + 18 - x - 22) == [2], "l15 s4 half-bracket: 3x + 18 - x = 22 gives 2")
lv.claim(roots(lambda x: x * x - 2 * x) == [0, 2] and 2 * 2 == 4 and 1 * 1 != 2 * 1, "l15 s5: x = 0, 2; height 4; x = 1 fails")
pair("l15 s6 trap", (-2, 1, -1, 3, -1, 5), (4, 7))
lv.claim(roots(lambda x: 3 * x - 2 * x - 1 - 5) == [6] and 2 * 6 - 1 == 11, "l15 s6 six: x = 6 on y = 2x - 1 at 11")
lv.claim(F(6, 5) == F('1.2'), "l15 s6 plus: 5x - 1 = 5 gives 1.2")
pair("l15 s7", (-1, 1, -3, 4, 2, 30), (6, 3))
lv.claim(4 * 6 + 2 * 3 == 30 and 6 * 6 - 6 == 30, "l15 s7: 6p - 6 = 30 and 24 + 6 = 30")
lv.claim(roots(lambda x: x * x - 3 * x) == [0, 3] and 3 * 3 == 9, "l15 s8: (0, 0) and (3, 9)")
pair("l15 s9", (2, -1, 0, 12.5, 8.25, 2900), (100, 200))
E("l15", "screens[9].widget.wrong[1].value", round(2900 / (12.5 * 2 + 8.25), 2))
E("l15", "screens[9].widget.wrong[2].value", round(2900 / (12.5 + 8.25), 2))
E("l15", "screens[9].explain.text", 12.5 * 100)
E("l15", "screens[9].explain.text", 8.25 * 200)
pair("l15 quiz[0]", (-4, 1, 0, 1, 1, 15), (3, 12))
lv.claim(F(15 - 4, 2) + 4 == F('9.5'), "l15 quiz[0] plus: y = x + 4 gives y = 9.5")
pair("l15 quiz[1]", (-1, 1, -3, 2, -1, 10), (7, 4))
lv.claim(roots(lambda x: 2 * x - x - 3 - 10) == [13], "l15 quiz[1] no-brackets: 13")
lv.claim(roots(lambda x: x * x - 4) == [-2, 2] and 4 * 4 == 16, "l15 quiz[2]: x = -2, 2; slips 16")
pair("l15 quiz[3]", (1, -2, 0, 3, 1, 21), (6, 3))

# ---------------- l16 ----------------
E("l16", "screens[0].widget.points[0].target", 11 - 2 * 2.5)
E("l16", "screens[0].widget.wrong[0].region", 11 - 2.5 - 0.2)
pair("l16 s1", (2, 1, 11, 3, 1, 15), (4, 3))
pair("l16 s2", (-1, 1, 1, 2, 1, 7), (2, 3))
lv.claim(7 - 2 * 0 == 7 and 7 - 2 * 3.5 == 0 and 3.5 + 1 == 4.5 and 7 - 2 * 3 == 1 and 3 + 1 == 4, "l16 s2 whys")
x3 = solve(-2, 1, 0, 1, 1, 5)
lv.claim(x3 == (F(5, 3), F(10, 3)) and abs(1.6667 - 5 / 3) < 0.005 and abs(1.67 - 5 / 3) < 0.005, "l16 s3: (5/3, 10/3), 1.67 inside the tolerance")
lv.claim(solve(-2, 1, 1, -2, 1, 4) is None and 4 - 1 == 3 and solve(-2, 1, 1, 0, 1, 4)[0] == F(3, 2), "l16 s4: m = 2 parallel 3 apart; m = 0 crosses at 1.5")
# finding 16: with m = 4 the steeper line starts higher and crosses to the left, at x = -1.5
xm4 = solve(-2, 1, 1, -4, 1, 4)[0]
lv.claim(xm4 == F(-3, 2), "l16 s4 steep: 2x + 1 = 4x + 4 at x = -1.5")
lv.stated("l16", "screens[4].feedback.byKey.steep", "so it overtakes the first and crosses it", 4 < 1)
lv.claim(all(2 * x + y == 5 and 4 * x + 2 * y == 10 for x, y in ((0, 5), (1, 3), (2, 1))), "l16 s5: three points on both")
lv.claim(all(x + 2 * y == 4 and 2 * x + 4 * y == 8 for x, y in ((0, 2), (2, 1), (4, 0))) and 0 + 2 * 0 != 4, "l16 s6: points on the line; (0, 0) off")
random.seed(7)
for _ in range(5):
    a, b = random.randint(1, 20), random.randint(1, 5)
    c = b + random.randint(1, 5)
    n = F(a, c - b)
    lv.claim(a + b * n == c * n, f"l16 s8: n = a/(c - b) solves a + bn = cn at a={a}, b={b}, c={c}")
pair("l16 s9", (-1.5, 1, 10, -2.5, 1, 0), (10, 25))
lv.claim(10 / 2.5 == 4 and 2.5 * 5 < 10 + 1.5 * 5 and 2.5 * 15 > 10 + 1.5 * 15, "l16 s9: four slip; B cheaper below 10, A above")
pair("l16 quiz[0]", (-1, 1, 3, 1, 1, 9), (3, 6))
lv.claim(9 - 0 == 9 and 6 + 3 == 9 and 9 + 3 == 12, "l16 quiz[0] whys")
lv.claim(solve(-4, 1, -1, -4, 1, 2) is None and 2 - (-1) == 3, "l16 quiz[1]: parallel, 3 apart")
lv.claim(solve(3, 1, 6, 6, 2, 12) is None, "l16 quiz[2]: same line")
lv.claim(F(15 - 5, F('0.3') - F('0.1')) == 50 and 15 + F('0.1') * 50 == 20 == 5 + F('0.3') * 50, "l16 quiz[3]: 50, both 20")
E("l16", "quiz[3].widget.wrong[0].value", 10 / 0.4)
E("l16", "quiz[3].widget.wrong[1].value", 10 / 0.1)

# ---------------- l17 ----------------
pair("l17 s2", (4, 3, 71, 2, 5, 60), (12.5, 7))
lv.claim((4, 10, 120) == (2 * 2, 2 * 5, 2 * 60) and 120 - 71 == 49 and 49 / 7 == 7, "l17 s2 explain: 4a + 10b = 120, 7b = 49")
pair("l17 s3", (1, -1, 3, 2, 3, 41), (10, 7))
pair("l17 s4", (1, 1, 30, 4, 6, 152), (14, 16))
E("l17", "screens[4].widget.wrong[1].value", round(152 / 6, 2))
lv.claim(4 * 15 + 6 * 15 == 150 and 4 * 14 + 6 * 16 == 152, "l17 s4: even split costs 150; 56 + 96 = 152")
lv.claim(solve(2, 1, 20, 4, 2, 40) is None and 2 * 5 + 10 == 20 and 2 * 8 + 4 == 20, "l17 s5: dependent; (5, 10) and (8, 4) fit")
lv.claim(F(10, 4) == F('2.5') and 10 + 4 == 14 and 4 * 10 == 40, "l17 s6 slips at x = 10: 2.5, 14; true 40")
lv.claim(F(10, 2) == 5 and 10 - 2 == 8, "l17 s7: half of 10 is 5; a - 2 = 8")
pair("l17 s8", (1, 1, 50, 2, 3.5, 145), (20, 30))
lv.claim(2 * 50 == 100 and 145 - 100 == 45 and 45 / 1.5 == 30 and 2 * 20 + 3.5 * 30 == 145, "l17 s8 lines")
pair("l17 s9", (6, 2, 1000, 5, 2, 900), (100, 200))
lv.claim(1000 / 2 == 500 and 500 * 2 == 1000 and 900 / 2 == 450 and 450 * 2 == 900, "l17 s9 slips: 500 B costs 1000; 450 B gives delta 900")
pair("l17 quiz[0]", (5, 2, 60, 3, 2, 44), (8, 10))
E("l17", "quiz[0].widget.wrong[2].value", 60 / 5)
lv.claim(10 - 2.5 == 7.5 and F(10, 2) == 5 and 10 + 2 == 12, "l17 quiz[1], quiz[2] tests")
pair("l17 quiz[3]", (1, 1, 20, 3, 5, 76), (12, 8))
E("l17", "quiz[3].widget.wrong[1].value", 76 / 5)

# ---------------- review-4 ----------------
pair("review-4 [0]", (3, 2, 19, 1, 2, 9), (5, 2))
pair("review-4 [1]", (-3, 1, -4, 5, -2, 6), (2, 2))
lv.claim(roots(lambda x: 5 * x - 6 * x - 4 - 6) == [-10] and roots(lambda x: 5 * x - 6 * x - 8 - 6) == [-14], "review-4 [1] slips -10 and -14")
lv.claim(solve(2, 1, 3, 4, 2, 10) is None, "review-4 [2]: parallel")
# finding 31: substituting y = -2x + 3 into 4x + 2y = 10 gives 6 = 10; 3 = 5 comes from setting the two y's equal
lv.claim(4 * 0 + 2 * 3 == 6 and 4 * 7 + 2 * (-2 * 7 + 3) == 6, "review-4 [2]: substitution leaves 6 = 10 at every x")
lv.stated("review", "items[2].explain.text", "Substituting gives $3 = 5$", False)
pair("review-4 [3]", (-1, 1, 4, 3, 2, 33), (5, 9))
lv.claim(F(33 - 12, 5) == F('4.2'), "review-4 [3] reversed: 5y = 21, y = 4.2")
pair("review-4 [4]", (4, -3, 9, 2, 3, 9), (3, 1))
lv.claim(roots(lambda x: x * x - 5 * x) == [0, 5] and 5 * 5 == 25, "review-4 [5]: (0, 0) and (5, 25)")
lv.claim(F(40, F('0.08')) == 500 and 40 + F('0.02') * 500 == 50 == F('0.1') * 500, "review-4 [6]: 500, both 50")
E("review", "items[6].widget.wrong[0].value", 40 / 0.1)
E("review", "items[6].widget.wrong[1].value", 40 / 0.02)
E("review", "items[6].widget.wrong[2].value", round(40 / 0.12, 2))
pair("review-4 [7]", (7, 3, 44.5, 4, 3, 28), (5.5, 2))
E("review", "items[7].widget.wrong[0].value", round(44.5 / 3, 2))
E("review", "items[7].widget.wrong[1].value", round((44.5 + 28) / 3, 2))
lv.claim(solve(3, 2, 7, 6, 4, 1) is None and solve(3, 2, 7, 6, 2, 1) is not None and 14 - 1 == 13, "review-4 [8]: k = 4 none; k = 2 one; 0 = 13")
lv.claim(F(-3, 2) == F('-1.5') and F(-6, 2) == -3, "review-4 [8] same-k slopes -1.5 and -3")
# proposed replacements (finding 32)
pair("proposed review-4 [3] equal spends", (-1, 1, 4, 9, -5, 0), (5, 9))
lv.claim(solve(1, -1, 4, 9, -5, 0)[1] == -9, "proposed review-4 [3] reversed x = y + 4 gives y = -9")
lv.claim(F(200 - 50, 25 - 15) == 15 and 200 + 15 * 15 == 425 == 50 + 25 * 15, "proposed review-4 [6]: 15 days, both 425")
lv.claim((F(150, 25), F(150, 40), F(250, 10)) == (6, F('3.75'), 25), "proposed review-4 [6] wrongs 6, 3.75, 25")
pair("proposed review-4 [7]", (7, -3, 32.5, 4, -3, 16), (5.5, 2))
lv.claim((round(32.5 / 3, 2), round((32.5 + 16) / 3, 2)) == (10.83, 16.17), "proposed review-4 [7] wrongs 10.83, 16.17")

# ---------------- homework-4 ----------------
pair("homework-4 [0]", (3, 2, 12.30, 2, 3, 12.45), (2.40, 2.55))
lv.claim((F('24.6'), F('37.35'), F('12.75'), F('7.2'), F('5.1')) == (2 * F('12.30'), 3 * F('12.45'), F('37.35') - F('24.6'), F('12.3') - F('5.1'), 2 * F('2.55')), "homework-4 [0] explain numbers")
lv.claim(F('2.40') - F('2.55') == F('-0.15') and F('12.30') / 2 == F('6.15'), "homework-4 [0] slips -0.15 (typed 0.15) and 6.15")
pair("homework-4 [1]", (1, -2, 1, 3, -4, 9), (7, 3))
lv.claim(roots(lambda y: 6 * y + 1 - 4 * y - 9) == [4] and 2 * 4 + 1 == 9, "homework-4 [1] no-brackets: y = 4, x = 9")
lv.claim(solve(2, 3, 6, 4, 6, 12) is None and 2 * 6 == 12 and 12 - 6 == 6, "homework-4 [2]: c = 12; c = 6 leaves 0 = 6")
pair("homework-4 [3]", (1, 1, 250, 4, 6.5, 1325), (120, 130))
E("homework", "items[3].widget.wrong[1].value", round(1325 / 6.5, 2))
lv.claim(125 * 4 + 125 * 6.5 == 1312.5 and 4 * 120 == 480 and 6.5 * 130 == 845, "homework-4 [3]: 1312.50; 480 + 845")
lv.claim(roots(lambda x: 2 * x * x - 6 * x) == [0, 3] and 6 * 3 == 18 and 3 * 3 == 9 and roots(lambda x: x * x - 6 * x) == [0, 6] and 6 * 6 == 36, "homework-4 [4] points and slips")
lv.claim(solve(3, 6, 105, 2, 4, 72) is None and F(3, 2) * 72 == 108 and 3 * 5 + 6 * 15 == 105 and 2 * 5 + 4 * 15 == 70 and 105 - 108 == -3, "homework-4 [5]: clash at 108 vs 105")
a, b, e, c, d, f = 3, 2, 16, 5, -2, 16
lv.claim((e * d - b * f, a * d - b * c) == (-64, -16) and F(-64, -16) == 4, "homework-4 [6]: check gives 4 (l14 s4)")
for _ in range(5):
    a, b, c, d, e, f = (random.randint(-9, 9) for _ in range(6))
    if a * d - b * c:
        x = F(e * d - b * f, a * d - b * c)
        lv.claim(x == solve(a, b, e, c, d, f)[0], f"homework-4 [6]: general x matches Cramer at {a, b, c, d, e, f}")
pair("homework-4 [7]", (0.5, 0.25, 650, 4.2, 1.6, 5200), (1040, 520))
lv.claim(650 / 0.25 == 2600 and 2600 * F('1.6') == 4160 and F(5200) / F('1.6') == 3250 and 3250 * F('0.25') == F('812.5'), "homework-4 [7] slips")
lv.claim(F('4.2') * 1040 == F('4368') and F('1.6') * 520 == 832, "homework-4 [7]: 4368 + 832")
lv.claim(F(12, F('0.8')) == 15 and 12 + F('0.4') * 15 == 18 == F('1.2') * 15, "homework-4 [8]: 15 trades, 18")
lv.claim((12 + 4, F('1.2') * 10, 12 + 12, F('1.2') * 30) == (16, 12, 24, 36), "homework-4 [8] advice numbers")
lv.claim(sum(r['points'] for r in lv.files['homework-4']['items'][8]['rubric']) == 10, "homework-4 [8] rubric sums to 10")

lv.check_wrongs()
lv.report()
