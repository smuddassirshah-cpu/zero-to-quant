"""functions level 2 (Straight lines): every graded key, wrong[] value and stated number, recomputed (second read, session V).
Run: python3 docs/reports/functions-L2-numbers.py   (exit 0 on correct content)
Checks marked FINDING in docs/reviews/review-functions-1-2.md fail while the content is wrong and pass once it is fixed."""
import math
import os
import re
import sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("functions", 2)
E = lv.expect


def W(f, sect, i, k, v):
    E(f, f"{sect}[{i}].widget.wrong[{k}].value", v)


def grad(p, q):
    return F(q[1] - p[1]) / F(q[0] - p[0])


def line(p, q):
    m = grad(p, q)
    return m, F(p[1]) - m * p[0]


# ---------- l5 plotting ----------
lv.claim(2 * 2 - 1 == 3 and 2 * 2 == 4 and 2 * 2 + 1 == 5, "l5 screens[3] y = 3; slips 4 and 5")
lv.claim([2 * x - 1 for x in (-1, 0, 1)] == [-3, -1, 1], "l5 screens[3] table -3, -1, 1")
lv.claim(3 - (-1) == 4 and 3 - 4 == -1 and 3 - 1 == 2 and 4 - 3 == 1, "l5 screens[4] P (-1, 4), Q (4, -1); slips 2 and 1")
E("l5", "screens[5].widget.answer", (4 + 1) / 2)
W("l5", "screens", 5, 0, 2 * 4 - 1)        # in-as-x
W("l5", "screens", 5, 1, (4 - 1) / 2)      # minus
# the placeholder must be neither the key (2.5) nor a slip (7, 1.5)
E("l5", "screens[5].widget.placeholder", "For example 0.5")
_w = lv.files['l5-plotting']['screens'][5]['widget']
_ph = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', _w.get('placeholder', ''))]
lv.claim(not any(abs(p - w['value']) <= 0.01 for p in _ph for w in _w['wrong']) and not any(abs(p - _w['answer']) <= 0.01 for p in _ph),
         "l5 screens[5] placeholder is neither the key nor a slip", f"placeholder {_w.get('placeholder')!r}")
fee = lambda n: F(5) + F("0.02") * n
lv.claim(fee(250) == 10 and fee(500) == 15 and fee(750) == 20 and F("0.02") * 750 == 15 and 3 * fee(250) == 30, "l5 screens[8] fees 10, 15, 20; slips 15 and 30")
E("l5", "quiz[1].widget.answer", 3 * -2 + 2)
W("l5", "quiz", 1, 0, 3 * 2 + 2)
W("l5", "quiz", 1, 1, 3 * -2 - 2)
lv.claim(2 * 4 + 3 == 11 and 2 * (4 + 3) == 14, "l5 quiz[2] (4, 11); slip 14")
lv.claim(F(3) + F("0.01") * 400 == 7 and F("0.01") * 400 == 4, "l5 quiz[3] (400, £7.00); slip £4.00")

# ---------- l6 how steep ----------
lv.claim(F(3, 6) == F("0.5") and round(2 / 3, 2) == 0.67 and F(2, 3) > F(1, 2), "l6 screens[0] A 0.5, B 0.67: B steeper")
lv.claim(grad((1, 1), (3, 5)) == 2 and grad((0, 3), (1, 5)) == 2 and grad((1, 1), (3, 3)) == 1, "l6 screens[1] B (3, 5) matches gradient 2; slip (3, 3)")
E("l6", "screens[2].widget.answer", float(grad((1, 1), (7, 4))))
W("l6", "screens", 2, 0, 6 / 3)
W("l6", "screens", 2, 1, 3)
W("l6", "screens", 2, 2, 6)
E("l6", "screens[3].widget.answer", float(grad((1, 5), (4, -1))))
W("l6", "screens", 3, 0, 2)
W("l6", "screens", 3, 1, -0.5)
lv.claim(1.5 * 0 - 1 == -1 and 1.5 * 4 - 1 == 5 and grad((0, -1), (4, 5)) == F(3, 2), "l6 screens[4] A (0, -1), B (4, 5) on 1.5x - 1; gradient 1.5")
E("l6", "screens[4].widget.answer", 1.5)
W("l6", "screens", 4, 0, round(4 / 6, 4))
W("l6", "screens", 4, 1, -1)
lv.claim(grad((-2, 3), (4, 3)) == 0 and 4 - (-2) == 6, "l6 screens[5] gradient 0, run 6")
lv.claim(4 * 1 + 6 == 10 and 4 * 6 + 6 == 30 and grad((1, 10), (6, 30)) == 4 and F(5, 20) == F("0.25"), "l6 screens[6] P, Q on 4x + 6; gradient 4; slip 0.25")
lv.claim(grad((2, 7), (5, 1)) == -2, "l6 screens[7] (2, 7), (5, 1): -2")
lv.claim(all(grad(p, q) == grad(q, p) for p, q in [((1, 2), (4, 11)), ((-3, 5), (2, -1))]), "l6 screens[8] either order gives the same gradient")
d = grad((5, F("42.75")), (25, F("45.75")))
E("l6", "screens[9].widget.answer", float(d))
W("l6", "screens", 9, 0, round(20 / 3, 4))
W("l6", "screens", 9, 1, 3)
W("l6", "screens", 9, 2, 3 / 30)
lv.claim(42 + F("0.15") * 5 == F("42.75") and 42 + F("0.15") * 25 == F("45.75"), "l6 screens[9] canvas line 42 + 0.15x passes both points")
E("l6", "screens[9].explain.text", 37.5)
lv.claim(250 * F("0.15") == F("37.5"), "l6 screens[9] 250 x 0.15 = 37.50")
E("l6", "quiz[0].widget.answer", float(grad((2, 1), (6, 9))))
W("l6", "quiz", 0, 0, 0.5)
W("l6", "quiz", 0, 1, 8)
E("l6", "quiz[2].widget.answer", float(grad((-2, 5), (4, -4))))
W("l6", "quiz", 2, 0, 1.5)
W("l6", "quiz", 2, 1, round(6 / -9, 4))
W("l6", "quiz", 2, 2, -9 / (4 - 2))
lv.claim(F(6, 4) == F("1.5") and round(4 / 6, 2) == 0.67, "l6 quiz[3] £1.50 per day; slip £0.67")

# ---------- l7 slope and start ----------
lv.claim(2 * 0 + 1 == 1 and 2 * -0.5 + 1 == 0, "l7 screens[0] crosses the vertical axis at 1, the horizontal at -0.5")
lv.claim(-2 * 0 + 3 == 3 and -2 * 1 + 3 == 1, "l7 screens[2] (0, 3), (1, 1) on -2x + 3")
E("l7", "screens[3].widget.answer", 1 - 0.5 * 4)
lv.claim(0.5 * 4 + 1 == 3, "l7 screens[3] slip c = 1 lands at 3 above T; slip added gives c = 3")
lv.claim(all(5 - 2 * x == -2 * x + 5 for x in range(-3, 6)), "l7 screens[5] 5 - 2x = -2x + 5")
# fb.first must not ask for m = 5: the m slider stops at 3
_c = lv.files['l7-slope-and-start']['screens'][5]['canvas']['controls']
lv.claim(any(c['bind'] == 'm' and c['max'] == 3 for c in _c), "l7 screens[5] the m slider stops at 3")
E("l7", "screens[5].feedback.byKey.first", "With $m = 5$ the line would climb steeply instead of falling.")
lv.stated("l7", "screens[5].feedback.byKey.first", "on the slider", False)
m8, c8 = line((200, F("6.95")), (800, F("12.95")))
E("l7", "screens[8].widget.answer", float(c8))
W("l7", "screens", 8, 0, 6.95)
W("l7", "screens", 8, 1, float(m8))
lv.claim(m8 == F("0.01") and 200 * m8 == 2, "l7 screens[8] m = 0.01, 200 shares = £2.00")
lv.claim((F("4.95") / F("0.05")).denominator == 1 and 0 <= F("4.95") <= 10, "l7 screens[8] c = 4.95 is reachable on the 0.05 slider")
E("l7", "quiz[1].widget.answer", -3 * 4 + 2)
W("l7", "quiz", 1, 0, 3 * 4 + 2)
W("l7", "quiz", 1, 1, -3 * 4 - 2)
lv.claim(abs(-4) > abs(3) > abs(2), "l7 quiz[2] steepest is |m| = 4")
E("l7", "quiz[3].widget.answer", float(F("0.12") * 20 + F("38.40")))
W("l7", "quiz", 3, 0, float(F("0.12") * 20))
W("l7", "quiz", 3, 1, float(F("0.12") + F("38.40")))

# ---------- l8 line through two points ----------
lv.claim(line((1, 3), (3, 7)) == (2, 1), "l8 screens[0] y = 2x + 1 through A, B; P at (0, 1)")
lv.claim(line((2, 5), (6, 7)) == (F(1, 2), 4), "l8 screens[2] y = 0.5x + 4")
lv.claim(5 - 2 * 2 == 1, "l8 screens[2] slip flipped: m = 2 through A gives 2x + 1")
lv.claim(line((-1, 6), (3, -2)) == (-2, 4) and 6 - 2 == 4 and 6 + 2 == 8 and 6 - F(1, 2) == F(11, 2), "l8 screens[3] y = -2x + 4; slips -2x + 8 and -0.5x + 5.5")
lv.claim(-1 - 5 * 3 == -16, "l8 screens[4] slip run-one: m = 5 through (3, -1) gives c = -16")
lv.claim(line((2, 7), (5, 13)) == (2, 3) and 2 * 2 + 7 == 11 and 11 - 7 == 4, "l8 screens[5] y = 2x + 3; Sam's line is 4 above A")
lv.claim(all(F(1, 2) * x + 4 == 5 + F(1, 2) * (x - 2) for x in range(-3, 4)), "l8 screens[7] y - 5 = 0.5(x - 2) is y = 0.5x + 4")
m88, c88 = line((4, F("38.20")), (16, F("40.60")))
E("l8", "screens[8].widget.answer", float(m88 * 30 + c88))
W("l8", "screens", 8, 0, float(F("38.20") + 30 * m88))         # from-day4
W("l8", "screens", 8, 1, float(F("40.60") * 30 / 16))          # proportional from day 16
lv.claim(m88 == F("0.2") and c88 == F("37.4"), "l8 screens[8] m = 0.20, c = 37.40")
lv.claim(line((0, 3), (2, 11)) == (4, 3), "l8 quiz[0] y = 4x + 3")
m81, c81 = line((1, 2), (3, 8))
E("l8", "quiz[1].widget.answer", float(c81))
W("l8", "quiz", 1, 0, 2)
W("l8", "quiz", 1, 1, 2 + 3)
lv.claim(8 * 4 + 1 != 1 and 1 - 8 * 4 == -31, "l8 quiz[2] option 8x + 1 does not pass (4, 1); with m = 8 the point gives c = -31")
m83, c83 = line((1000, 13), (3000, 21))
E("l8", "quiz[3].widget.answer", float(c83))
W("l8", "quiz", 3, 0, 13)
W("l8", "quiz", 3, 1, float(m83))

# ---------- l9 parallel and perpendicular ----------
lv.claim((2 * 0 + 1) - (2 * 0 - 3) == 4, "l9 screens[0] gap 4")
lv.claim(2 - (-1) == 3, "l9 screens[1] gap 3")
lv.claim(5 - (-2) == 7, "l9 screens[2] 3x + 5 is 7 above 3x - 2")
ang = lambda m: math.degrees(math.atan(m))
lv.claim(abs((180 - (ang(2) - ang(-2))) - 53.13) < 0.01, "l9 screens[3] y = 2x and y = -2x meet at about 53 degrees (the acute angle)")
lv.claim(2 * F(-1, 2) == -1, "l9 screens[3] 2 x (-0.5) = -1")
lv.claim(F(2, 3) * F(-3, 1) / 2 == -1 and grad((-2, 3), (F(8, 3), -4)) == F(-3, 2), "l9 screens[4] OB gradient -3/2; explain segment has gradient -1.5")
# every horizontal line with every vertical line is a perpendicular pair, so the text says "kind of pair", not "the one pair"
E("l9", "screens[5].explain.text", "This is the one kind of perpendicular pair the rule does not cover.")
lv.stated("l9", "screens[5].explain.text", "the one perpendicular pair", False)
lv.claim(-0.5 * 6 + 5 == 2, "l9 screens[6] point (6, 2) lies on y = -0.5x + 5")
_p = lv.files['l9-parallel-perpendicular']['screens'][6]['canvas']
lv.claim(_p['state']['points'][0]['x'] == 6 and _p['state']['points'][0]['y'] == 2 and 'label' not in _p['params']['functions'][1], "l9 screens[6] the label is a point at (6, 2), not a line label")
lv.claim(2 * F(-1, 2) == -1, "l9 screens[6] product -1")
E("l9", "screens[7].widget.answer", 0.25)
W("l9", "screens", 7, 0, 4)
W("l9", "screens", 7, 1, -0.25)
lv.claim(F(1, 3) * 3 == 1 and F(-1, 1) * (F(-1, 1) / -1) == -1, "l9 screens[8] product of b/a and -a/b is -1")
be = lambda a1, b1, a2, b2: F(a2 - a1) / F(b1 - b2)
x9 = be(2, F("0.01"), 8, F("0.004"))
lv.claim(x9 == 1000 and 2 + F("0.01") * 1000 == 12 and 2 + F("0.01") * 600 == 8 and 8 + F("0.004") * 600 == F("10.40"), "l9 screens[9] 1,000 shares at £12.00; at 600 A is £8.00 and B £10.40")
lv.claim(-2 - 1 == -3 and 7 - (-1) == 8, "l9 quiz[0] y = -2x - 1 is 8 below")
E("l9", "quiz[1].widget.answer", round(-4 / 3, 4))
W("l9", "quiz", 1, 0, round(4 / 3, 4))
W("l9", "quiz", 1, 1, -0.75)
lv.claim(grad((1, 2), (3, 8)) == 3 and grad((0, 5), (6, 3)) == F(-1, 3), "l9 quiz[2] gradients 3 and -1/3")
x93 = be(5, F("0.008"), 9, F("0.006"))
E("l9", "quiz[3].widget.answer", float(x93))
W("l9", "quiz", 3, 0, float(F(4) / F("0.008")))
lv.claim(5 + F("0.008") * 2000 == 21, "l9 quiz[3] both £21.00")

# ---------- review-2 ----------
E("review", "items[1].widget.answer", float(grad((-1, -4), (3, 8))))
W("review", "items", 1, 0, round(1 / 3, 4))
W("review", "items", 1, 1, (8 - 4) / (3 - 1))
lv.claim(line((-2, 1), (2, 9)) == (2, 5) and 1 + 2 * -2 == -3, "review items[3] y = 2x + 5; slip c = -3")
E("review", "items[4].widget.answer", -1 / 0.2)
W("review", "items", 4, 0, 5)
W("review", "items", 4, 1, -0.2)
lv.claim(F(101 - 100, 10) == F("0.1") and F(10, 1) == 10 / F(1), "review items[5] £0.10 per month; slips 10 and 1")
E("review", "items[5].widget.options[0].text", "£0.10 per month")
E("review", "items[5].widget.options[2].text", "£10.00 per month")
E("review", "items[5].widget.options[3].text", "£1.00 per month")
E("review", "items[5].explain.text", "$1 \\div 10 = 0.10$ pounds per month")
E("review", "items[6].widget.answer", float(F("1.50") * 4 + F("3.50")))
W("review", "items", 6, 0, float(F("1.50") * 4))
E("review", "items[6].explain.text", "$1.50 \\times 4 = 6.00$")
E("review", "items[6].feedback.correct", "$1.50 \\times 4 + 3.50 = 9.50$.")
lv.claim(1 - 3 * 2 == -5 and 3 * 2 + 1 == 7 and F(-1, 3) * 2 + F(5, 3) == 1 and 3 * 2 - 1 == 5, "review items[7] c = -5; distractor checks 7, 1, 5")
x28 = be(50, F("0.30"), 42, F("0.80"))
E("review", "items[8].widget.answer", float(x28))
W("review", "items", 8, 0, round(8 / 0.3, 4))
W("review", "items", 8, 1, 8 / 0.8)
lv.claim(F("0.30") * 16 + 50 == F("54.80") == F("0.80") * 16 + 42, "review items[8] both £54.80")

# ---------- homework-2 ----------
E("homework", "items[1].widget.answer", float(grad((-3, F("2.5")), (1, F("-3.5")))))
W("homework", "items", 1, 0, 1.5)
W("homework", "items", 1, 1, round(4 / -6, 4))
lv.claim(line((-4, 0), (2, 3)) == (F(1, 2), 2) and 0 + F(1, 2) * -4 == -2 and 0 - 2 * -4 == 8, "homework items[2] y = 0.5x + 2; slips 0.5x - 2 and 2x + 8")
c23 = -3 - F(-5, 2) * 4
E("homework", "items[3].widget.answer", float(c23 / F(5, 2)))
W("homework", "items", 3, 0, float(c23))
W("homework", "items", 3, 1, -2.8)
c24 = 3 - F(-1, 2) * 4
E("homework", "items[4].widget.answer", float(c24))
W("homework", "items", 4, 0, 3 - 2 * 4)
W("homework", "items", 4, 1, 3 - (-2) * 4)
W("homework", "items", 4, 2, float(3 + F(-1, 2) * 4))
E("homework", "items[5].widget.answer", float((30 - F("24.60")) / F("0.18")))
W("homework", "items", 5, 0, round(30 / 0.18, 4))
# With b1 = b2 the lines are parallel only if a1 != a2 (a1 = a2 makes one line and every x breaks even)
lv.claim(all(a1 + 2 * x != a2 + 2 * x for a1, a2 in [(1, 3), (4, 0)] for x in range(-3, 4)) and all(a + 2 * x == a + 2 * x for a in (1, 3) for x in range(-3, 4)), "homework items[6] b1 = b2: no break-even if a1 != a2, every x if a1 = a2")
E("homework", "items[6].widget.lines[4].text", "If $b_1 = b_2$ and $a_1 \\neq a_2$, the fee lines are parallel and there is no break-even")
mA, cA = line((200, F("5.40")), (600, F("7.80")))
x27 = be(cA, mA, 9, F("0.002"))
E("homework", "items[7].widget.answer", float(x27))
W("homework", "items", 7, 0, float(be(F("5.40"), mA, 9, F("0.002"))))   # first-fee as fixed charge
W("homework", "items", 7, 1, float(F("4.80") / mA))                   # a-rate
lv.claim(mA == F("0.006") and cA == F("4.20") and cA + mA * 1200 == F("11.40") == 9 + F("0.002") * 1200, "homework items[7] A = 4.20 + 0.006x; both £11.40")
m8h, c8h = line((3, F("52.40")), (12, F("55.10")))
lv.claim(m8h == F("0.3") and c8h == F("51.5") and m8h * 12 + c8h == F("55.10"), "homework items[8] model y = 0.30x + 51.50")
lv.claim(m8h * 30 + c8h == F("60.5"), "homework items[8] model day 30 = £60.50")
xc = be(c8h, m8h, F("57"), F("0.1"))
lv.claim(xc == F("27.5") and m8h * xc + c8h == F("59.75") == F("0.1") * xc + 57, "homework items[8] model meet on day 27.5 at £59.75")
lv.claim(57 - c8h == F("5.5"), "homework items[8] model gap £5.50")
E("homework", "items[8].model", 59.75)
E("homework", "items[8].model", 27.5)

lv.check_wrongs()
lv.report()
