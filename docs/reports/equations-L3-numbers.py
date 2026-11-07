"""Second-reader number script for equations Level 3 (l10 to l13, review-3, homework-3).

Every graded key, every wrong[] value and every number stated in prose, hints, feedback and explanations is
recomputed here, most of them two ways. Claims that are not single numbers (which side a bar runs, which integers
pass, what a slip produces) are checked with claim() or stated(). A stated() check that fails marks a finding in
docs/reviews/review-equations-3-4.md: it fails while the false sentence is in the content and passes once the
fix rewords it. Checks on the review's proposed replacement items are claim()s and pass now.
"""
import json
import math
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("equations", 3)
E = lv.expect


def ints(lo, hi, lo_in, hi_in, span=range(-50, 51)):
    """Integers in an interval, by brute force (the second method beside each formula)."""
    return [k for k in span if (k > lo or (lo_in and k == lo)) and (k < hi or (hi_in and k == hi))]


# ---------------- l10 ----------------
lv.claim([n for n in range(9) if n > 3] == [4, 5, 6, 7, 8], "l10 s0: dots 4 to 8 pass x > 3")
for n in (4, 5, 6, 7, 8):
    E("l10", "screens[0].feedback.correct", n)
lv.claim(3.5 > 3 and 3.1 > 3 and 3.01 > 3 and not 3 > 3, "l10 s1: 3.5, 3.1, 3.01 pass, 3 fails")
lv.claim(-2 < -1 and -3 < -1, "l10 s3: -2 and -3 lie in x < -1")
lv.claim(math.ceil(-2.5) == -2 and -3 < -2.5, "l10 s4: smallest integer with x >= -2.5 is -2; -3 is off")
E("l10", "screens[4].widget.points[0].target", -2)
lv.claim(-3.2 <= -3 <= -2.8 and -2.7 <= -2.5 <= -2.3 and -1.2 <= -1, "l10 s4: wrong regions hold -3, -2.5 and -1 upwards")
lv.claim(not (-2 < -4), "l10 s5 hint: -2 < -4 is false, so bar A fails")
lv.claim(22.00 <= 22.00 and 24.50 > 22.00, "l10 s7: 22.00 triggers, the 24.50 entry does not")
E("l10", "screens[8].widget.answer", round(22.00 - 0.01, 2))
E("l10", "screens[8].widget.wrong[1].value", round(22.00 - 0.10, 2))
E("l10", "screens[8].widget.wrong[0].value", 22.0)
lv.claim(all(x >= -3 for x in (-3, -2.5, 0)) and not any(x >= -3 for x in (-3.5, -4)), "l10 quiz[0]: -3, -2.5, 0 pass; -3.5, -4 fail")
lv.claim(1.5 <= 1.5 and round(1.5) == 2, "l10 quiz[1]: boundary 1.5 kept; rounding gives 2")
lv.claim(all((7 > x) == (x < 7) for x in range(-20, 21)), "l10 quiz[2]: 7 > x is x < 7")
lv.claim(400 <= 400 and not 400 < 400, "l10 quiz[3]: at most 400 keeps 400")
# finding 4: x <= a has not appeared as a solution set before screen 6, and the learner has drawn nothing
lv.stated("l10", "screens[6].prose", "You have now drawn all four kinds", False)

# ---------------- l11 ----------------
lv.claim([n for n in range(11) if n + 4 > 9] == [6, 7, 8, 9, 10], "l11 s0: 6 to 10 pass x + 4 > 9")
E("l11", "screens[0].hints[1].text", 5 + 4)
E("l11", "screens[0].feedback.byKey.n4", 4 + 4)
lv.claim(F(10, 3) + F(2, 3) == 4 and F(12, 3) == 4, "l11 s1: 10/3 + 2/3 = 4 = 12/3")
E("l11", "screens[1].widget.states.s0w.tex", 10 - 2)
E("l11", "screens[1].widget.states.s1w.tex", 12 - 3)
E("l11", "screens[1].explain.text", 3 * 4 - 2)
E("l11", "screens[2].widget.points[0].target", -1 * 2)
E("l11", "screens[2].widget.points[1].target", -1 * 5)
E("l11", "screens[3].widget.options", -3 * 2)
E("l11", "screens[3].widget.options", -3 * 5)
lv.claim(-6 > -15 and not 6 > 15, "l11 s3: -6 > -15 true, 6 > 15 false")
lv.claim(F(12, -3) == -4 and all((-3 * x > 12) == (x < -4) for x in range(-20, 21)), "l11 s4: -3x > 12 is x < -4 (brute force)")
lv.claim(-3 * -5 == 15 and 15 > 12 and not (-3 * 0 > 12) and 0 > -4, "l11 s4: x = -5 passes; x = 0 fits x > -4 but fails")
E("l11", "screens[4].widget.states.s0c.tex", -12)
E("l11", "screens[4].widget.states.s0d.tex", F(-12, 3))
E("l11", "screens[5].widget.states.s1.tex", 1 - 5)
E("l11", "screens[5].widget.states.s2.tex", (1 - 5) / 2)
lv.claim(2 * (-3) + 5 == -1 and -1 < 1, "l11 s5: x = -3 check")
lv.claim(all((5 - F(x, 2) >= 3) == (x <= 4) for x in range(-20, 21)), "l11 s6: 5 - x/2 >= 3 is x <= 4 (brute force)")
lv.claim(5 - 6 / 2 == 2 and 2 < 3 and 6 >= 4, "l11 s6 kept: x = 6 fits x >= 4 but 5 - 3 = 2 < 3")
lv.claim(5 - 2 / 2 == 4 and 4 >= 3, "l11 s6 feedback: x = 2 gives 4 >= 3")
lv.claim(-2 * -2 == 4, "l11 s6: -2 x -2 = 4")
# finding 6: what each slip on s6 really produces (from -x/2 >= -2)
lv.claim(F(-2, -2) == 1 and F(-2, 2) == -1, "l11 s6: x <= 1 comes from -2 / -2 = 1, not -2 / 2 = -1")
lv.stated("l11", "screens[6].widget.options[2].why", "You divided $-2$ by 2.", F(-2, 2) == 1)
lv.claim(-2 * 2 == -4, "l11 s6: x <= -4 comes from -2 x 2 = -4 (multiplier 2, not -2)")
lv.stated("l11", "screens[6].widget.options[3].why", "You multiplied only the left side by $-2$.", False)
lv.claim(all((7 - 2 * x <= 1) == (x >= 3) for x in range(-20, 21)), "l11 s7: 7 - 2x <= 1 is x >= 3 (brute force)")
E("l11", "screens[7].widget.lines[2].text", 7 - 1)
E("l11", "screens[7].widget.lines[3].text", 6 / 2)
E("l11", "screens[7].explain.text", 1 - 7)
for n, pl in ((100, -250), (200, -500), (240, -600), (300, -750)):
    lv.claim(-2.5 * n == pl, f"l11 s8 table: {n} short loses {pl}")
    E("l11", "screens[8].canvas.params.rows", pl)
E("l11", "screens[8].widget.options[0].text", -600 / -2.5)
lv.claim(all((-2.5 * n >= -600) == (n <= 240) for n in range(0, 500)), "l11 s8: -2.5n >= -600 is n <= 240")
E("l11", "quiz[0].widget.options[0].text", (13 - 1) / 4)
E("l11", "quiz[0].widget.options[1].text", 13 / 4 - 1)
E("l11", "quiz[0].widget.options[3].text", 13 - 1)
E("l11", "quiz[1].widget.options[0].text", 20 / -5)
lv.claim(-5 * -5 == 25 and 25 > 20 and -5 <= -4, "l11 quiz[1] b: x = -5 fits x <= -4 but -5x = 25 > 20")
lv.claim(min(x for x in range(-20, 21) if 10 - 3 * x < 4) == 3, "l11 quiz[3]: smallest integer with 10 - 3x < 4 is 3")
lv.claim(10 - 3 * 2 == 4 and not (4 < 4), "l11 quiz[3] boundary: 10 - 6 = 4 is not < 4")
lv.claim(max(x for x in range(-20, 21) if x < 2) == 1, "l11 quiz[3] kept: 1 is the largest integer in x < 2 (not the smallest)")

# ---------------- l12 ----------------
lv.claim(ints(-2, 3, False, True) == [-1, 0, 1, 2, 3], "l12 s0: -1 to 3 pass both tests")
lv.claim(all((1 < 2 * x + 3 <= 11) == (-1 < x <= 4) for x in [F(k, 4) for k in range(-40, 41)]), "l12 s3: 1 < 2x+3 <= 11 is -1 < x <= 4")
E("l12", "screens[3].widget.states.s1.tex", 1 - 3)
E("l12", "screens[3].widget.states.s1.tex", 11 - 3)
E("l12", "screens[3].feedback.correct", 2 * 4 + 3)
lv.claim(len(ints(-1, 4, False, True)) == 5 == 4 - (-1), "l12 s4: five integers, 4 - (-1) = 5")
lv.claim(len(ints(-1, 4, True, True)) == 6 and len(ints(-1, 4, False, False)) == 4 and 4 - 1 == 3, "l12 s4 wrongs: 6, 4 and 3")
lv.claim(all((-3 <= 1 - 2 * x < 7) == (-3 < x <= 2) for x in [F(k, 4) for k in range(-40, 41)]), "l12 s5: -3 <= 1-2x < 7 is -3 < x <= 2")
E("l12", "screens[5].prose", -3 - 1)
E("l12", "screens[5].prose", 7 - 1)
E("l12", "screens[5].widget.states.s2.tex", F(-4, -2))
E("l12", "screens[5].widget.states.s2.tex", F(6, -2))
lv.claim(-3 <= 1 - 0 < 7, "l12 s5 feedback: x = 0 gives 1, inside")
lv.claim(all(len(ints(a, b, False, True)) == b - a for a in range(-6, 6) for b in range(a + 1, 8)), "l12 s6: a < x <= b holds b - a integers when a, b are integers")
# finding 7: the summary drops the whole-number condition
lv.claim(len(ints(-2.5, 3, False, True)) == 6 and 3 - (-2.5) == 5.5, "l12 summary: with a = -2.5, b = 3 there are 6 integers, not b - a = 5.5")
lv.stated("l12", "summary.ideas[2]", "Count whole numbers from the ends: $a < x \\le b$ holds $b - a$ of them", False)
lv.claim(all((-200 <= 120 - n <= 200) == (-80 <= n <= 320) for n in range(-400, 401)), "l12 s7: -80 <= n <= 320")
E("l12", "screens[7].widget.answer", 200 + 120)
E("l12", "screens[7].hints[2].text", -200 - 120)
E("l12", "screens[7].hints[2].text", 200 - 120)
E("l12", "screens[7].widget.wrong[2].value", 200 - 120)
lv.claim(max(n for n in range(30) if 5000 - 450 * n >= 800) == 9, "l12 s8: 9 contracts (brute force)")
lv.claim(F(4200, 450) == F(28, 3) and round(4200 / 450, 2) == 9.33, "l12 s8: 4200/450 = 28/3 = 9 1/3, about 9.33")
for n, used, free in ((8, 3600, 1400), (9, 4050, 950), (10, 4500, 500)):
    lv.claim(450 * n == used and 5000 - used == free, f"l12 s8 table: {n} contracts use {used}, leave {free}")
    E("l12", "screens[8]", free)
E("l12", "screens[8].widget.wrong[1].value", 5000 // 450)
E("l12", "screens[8].widget.wrong[2].value", 5800 // 450)
# finding 8: 4200 / 450 is 9.333..., stated with "="
lv.stated("l12", "screens[8].hints[2].text", "= 9.33$", 4200 / 450 == 9.33)
E("l12", "quiz[0].widget.options[0].text", 5 - 3)
E("l12", "quiz[0].widget.options[0].text", 9 - 3)
E("l12", "quiz[0].widget.options[2].text", 5 + 3)
E("l12", "quiz[0].widget.options[2].text", 9 + 3)
lv.claim(ints(-3, 2, True, False) == [-3, -2, -1, 0, 1], "l12 quiz[1]: -3 to 1, five integers")
lv.claim(all((-1 < -x <= 4) == (-4 <= x < 1) for x in [F(k, 4) for k in range(-40, 41)]), "l12 quiz[2]: -4 <= x < 1")
lv.claim(not any(5 < x < 2 for x in range(-50, 51)), "l12 quiz[3]: 5 < x < 2 is empty")

# ---------------- l13 ----------------
for row, (P, r, t, I, yr) in enumerate(((2000, F('0.05'), 3, 300, 100), (1500, F('0.04'), 2, 120, 60), (800, F('0.025'), 4, 80, 20))):
    lv.claim(P * r * t == I and P * r == yr, f"l13 s0 row {row}: I = {I}, a year {yr}")
    E("l13", f"screens[0].widget.rows[{row}][3].answer", I)
    E("l13", "screens[0].feedback.byKey", yr)
E("l13", "screens[1].widget.answer", 250 / (2000 * 0.05))
E("l13", "screens[1].widget.wrong[0].value", 250 / 2000)
E("l13", "screens[1].widget.wrong[1].value", 250 / 0.05)
E("l13", "screens[2].explain.text", 2.5)
lv.claim(240 / 80 == 3, "l13 s3 feedback: 240 km at 80 km/h is 3 hours")
p, c, Fx = 8.50, 5.50, 1200
E("l13", "screens[4].widget.answer", Fx / (p - c))
lv.claim(round(Fx / (p - c)) == 400 and 400 * (p - c) - Fx == 0, "l13 s4: break-even 400 (two ways)")
for q, prof in ((100, -900), (200, -600), (500, 300)):
    lv.claim(q * (p - c) - Fx == prof, f"l13 s4 table: {q} mugs give {prof}")
    E("l13", "screens[4].canvas.params.rows", prof)
E("l13", "screens[4].widget.wrong[0].value", round(Fx / p, 2))
E("l13", "screens[4].widget.wrong[1].value", round(Fx / c, 2))
E("l13", "screens[4].widget.wrong[2].value", round(Fx / (p + c), 2))
# finding 21: l9 screens[6] already found 1200 / (3.40 - 0.40) = 400
l9 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'equations', 'l9-story-to-equation.json')))
lv.claim('1,200.00' in l9['screens'][6]['prose'] and round(1200 / (3.40 - 0.40)) == 400, "l13 s4 repeats l9 s6: both 1200 / 3 = 400")
# proposed l13 s4 numbers: p = 9.50
p2 = 9.50
lv.claim(Fx / (p2 - c) == 300 and [q * (p2 - c) - Fx for q in (100, 200, 500)] == [-800, -400, 800], "proposed l13 s4: 300 mugs; table -800, -400, 800")
lv.claim((round(Fx / p2, 2), round(Fx / c, 2), round(Fx / (p2 + c), 2)) == (126.32, 218.18, 80.0), "proposed l13 s4 wrongs: 126.32, 218.18, 80")
lv.claim(all(F(C - 5, 2) == n for n, C in ((0, 5), (1, 7), (3, 11), (10, 25))), "l13 s5 table fits n = (C - 5)/2")
E("l13", "screens[5].feedback.byKey.one-term", F(11, 2) - 5)
E("l13", "screens[5].widget.options[2].why", F(11 + 5, 2))
E("l13", "screens[5].widget.options[3].why", 11 - F(5, 2))
E("l13", "screens[6].explain.text", F(55) / F('1.1'))
for row, (P1, r, P0) in enumerate(((F('52.50'), F('0.05'), 50), (F('38.40'), F('-0.04'), 40), (F('121.00'), F('0.10'), 110))):
    lv.claim(P1 / (1 + r) == P0 and P0 * (1 + r) == P1, f"l13 s7 row {row}: entry {P0} (two ways)")
    E("l13", f"screens[7].widget.rows[{row}][3].answer", P0)
lv.claim(F('52.50') * F('0.95') == F('49.875'), "l13 s7: 52.50 x 0.95 = 49.875, shown as 49.88")
E("l13", "screens[7].feedback.byKey.r0c3", 49.88)
E("l13", "screens[7].feedback.byKey.r2c3", 110 * 0.10)
M, m, pr = 6000, F('0.25'), 48
lv.claim(M / (m * pr) == 500 and m * pr == 12, "l13 s8: 500 shares at 12 margin each")
E("l13", "screens[8].widget.wrong[0].value", M / pr)
E("l13", "screens[8].widget.wrong[1].value", float(M * m / pr))
E("l13", "screens[8].widget.wrong[2].value", float(M * m * pr))
lv.claim(F(66) / F('1.10') == 60 and 60 * F('1.10') == 66, "l13 quiz[2]: entry 60 (two ways)")
E("l13", "quiz[2].widget.wrong[0].value", float(66 * F('0.9')))
E("l13", "quiz[2].widget.wrong[1].value", float(66 * F('1.1')))
lv.claim(all(abs(F(Fv) / q + cv - pv) == 0 for Fv, q, cv, pv in ((1200, 400, F('5.5'), F('8.5')), (900, 180, 7, 12))), "l13 quiz[3]: p = F/q + c on two rows")

# ---------------- review-3 ----------------
lv.claim(all((6 - 2 * x > 14) == (x < -4) for x in range(-30, 30)), "review-3 [1]: 6 - 2x > 14 is x < -4")
E("review", "items[1].widget.options[2].text", F(20, -2))
lv.claim(6 + 10 == 16 and 16 > 14 and not (6 > 14), "review-3 [1]: checks at -5 and 0")
lv.claim(150 / 50 == 3, "review-3 [2]: 150 km at 50 km/h is 3 hours")
lv.claim(ints(-1, 3, True, False) == [-1, 0, 1, 2] and all((-2 <= 3 * x + 1 < 10) == (-1 <= x < 3) for x in range(-20, 20)), "review-3 [3]: four integers")
E("review", "items[3].widget.wrong[0].value", len(ints(-1, 3, True, True)))
E("review", "items[3].widget.wrong[1].value", len(ints(-1, 3, False, False)))
lv.claim(F('45.60') / F('0.95') == 48 and 48 * F('0.05') == F('2.40'), "review-3 [5]: entry 48, a 2.40 fall")
E("review", "items[5].widget.wrong[0].value", float(F('45.60') * F('1.05')))
E("review", "items[5].widget.wrong[1].value", float(F('45.60') * F('0.95')))
lv.claim(all((-500 <= -150 + n <= 500) == (-350 <= n <= 650) for n in range(-1000, 1000)), "review-3 [6]: -350 <= n <= 650")
E("review", "items[6].widget.wrong[1].value", 500 - 150)
lv.claim(min(q for q in range(1000) if 8 * q - 2000 > 0) == 251 and 8 * 250 - 2000 == 0, "review-3 [7]: 251; 250 breaks even")
# proposed replacements for review-3 items 2, 4, 6 (finding 25)
lv.claim(F(20 - 2 * 6, 2) == 4 and 2 * (6 + 4) == 20 and F(20, 2) + 6 == 16 and 20 - 2 * 6 == 8 and F(20, 2) - 2 * 6 == -2, "proposed review-3 [2]: P = 20, l = 6 gives w = 4; slips give 16, 8, -2")
lv.claim(all((80 <= 100 - 4 * y <= 92) == (2 <= y <= 5) for y in [F(k, 4) for k in range(-40, 60)]), "proposed review-3 [6]: 2 <= y <= 5")
lv.claim(100 - 4 * 5 == 80 and 100 - 4 * 2 == 92 and F(-20, 4) == -5 and F(-8, 4) == -2, "proposed review-3 [6]: ends 80 and 92; dividing by 4 gives -5 and -2")

# ---------------- homework-3 ----------------
lv.claim(all((F(3 - x, 4) >= -2) == (x <= 11) for x in range(-30, 30)), "homework-3 [0]: x <= 11")
lv.claim(F(3 - 15, 4) == -3 and F(3 - 11, 4) == -2 and all((3 - x >= -2) == (x <= 5) for x in range(-30, 30)), "homework-3 [0]: -3 at 15, -2 at 11; slip gives x <= 5")
lv.claim(F('52.00') * F('0.94') == F('48.88') and 52 * F('0.06') == F('3.12'), "homework-3 [1]: stop 48.88, drop 3.12")
E("homework", "items[1].widget.wrong[0].value", 52 - 6)
E("homework", "items[1].widget.wrong[1].value", float(F('52') * F('1.06')))
lv.claim([x for x in range(-30, 30) if 2 * x - 3 < 9 and 5 - x <= 7] == list(range(-2, 6)), "homework-3 [2]: -2 to 5, eight integers")
E("homework", "items[2].widget.answer", len(range(-2, 6)))
lv.claim([n for n in range(0, 20) if 12000 - 1500 * n >= 3000 and n >= 2] == [2, 3, 4, 5, 6], "homework-3 [3]: sizes 2 to 6")
lv.claim(len(range(2, 12000 // 1500 + 1)) == 7 and 6 - 2 == 4 and len(range(1, 7)) == 6, "homework-3 [3] wrongs 7, 4, 6")
lv.claim(F(4 + 2, 4 - 1) == 2 and F(2 + 2, 2 - 1) == 4, "homework-3 [4]: x = 4 gives y = 2, and back")
for row, (Fv, pv, cv, q) in enumerate(((900, 12, 7, 180), (2400, F('15.5'), F('9.5'), 400), (750, F('4.25'), F('2.75'), 500))):
    lv.claim(Fv / (pv - cv) == q, f"homework-3 [5] row {row}: {q}")
    E("homework", f"items[5].widget.rows[{row}][3].answer", q)
lv.claim(all((F(2 * x - 1, 3) < F(x + 4, -2)) == (x < F(-10, 7)) for x in [F(k, 7) for k in range(-70, 70)]), "homework-3 [6]: x < -10/7")
lv.claim(max(x for x in range(-30, 30) if F(2 * x - 1, 3) < F(x + 4, -2)) == -2 and round(-10 / 7, 2) == -1.43, "homework-3 [6]: largest integer -2; boundary -1.43")
lv.claim(max(x for x in range(-30, 30) if F(2 * x - 1, 3) < F(x + 4, 2)) == 13, "homework-3 [6] dropped-minus gives 13")
lv.claim(all((40 * (75 - p) >= -400) == (p <= 85) for p in range(0, 200)), "homework-3 [7]: p <= 85")
lv.claim(40 * (75 - 80) == -200 and 40 * (75 - 90) == -600 and 75 + F(400, 40) == 85, "homework-3 [7] model checks and L = 400")
lv.claim(sum(r['points'] for r in json.loads(json.dumps(lv.files['homework-3']['items'][7]['rubric']))) == 10, "homework-3 [7] rubric sums to 10")

lv.check_wrongs()
lv.report()
