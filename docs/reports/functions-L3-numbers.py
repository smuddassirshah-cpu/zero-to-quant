"""Number recompute for functions level 3 (Curves and what they tell you): l10 to l13, review-3, homework-3.
Second reader, session V (no author script existed).

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations
are recomputed a second way (exact arithmetic, bisection for the one transcendental root, brute force for drawdowns).
Checks tied to a sentence (lv.stated) fail while a false sentence is in the text and pass once a fix rewords it.
    python3 docs/reports/functions-L3-numbers.py
Failing checks on the current content are findings in docs/reviews/review-functions-3-4.md.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("functions", 3)
E = lv.expect


def roots_quad(a, b, c):
    d = b * b - 4 * a * c
    r = d ** 0.5
    return sorted([(-b - r) / (2 * a), (-b + r) / (2 * a)])


def bisect(f, lo, hi, n=80):
    for _ in range(n):
        m = (lo + hi) / 2
        if (f(lo) < 0) == (f(m) < 0):
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def max_drawdown(v):
    best, peak, pk_i, out = 0, v[0], 0, None
    for i, x in enumerate(v):
        if x > peak:
            peak, pk_i = x, i
        if peak - x > best:
            best, out = peak - x, (pk_i, i)
    return best, out


# ---------------- l10 curves from tables ----------------
E("l10", "screens[1].widget.points[0].target", (-2) ** 2)
E("l10", "screens[1].hints[2].text", 4)
E("l10", "screens[1].widget.wrong[0].region", -4.5)            # region around -4 = -(2^2)
E("l10", "screens[2].widget.answer", 0.5 ** 2)
E("l10", "screens[2].widget.wrong[0].value", 0.5)              # straight join (0,0)-(1,1) at x = 0.5
E("l10", "screens[3].widget.rows[0][1].answer", (-2) ** 3)
E("l10", "screens[3].widget.rows[1][1].answer", (-1) ** 3)
E("l10", "screens[3].hints[2].text", (-2) * (-2))
E("l10", "screens[4].hints[1].text", 1 / 0.25)
E("l10", "screens[4].hints[1].text", 1 / 0.1)
E("l10", "screens[5].widget.answer", 2 ** -1)
E("l10", "screens[5].widget.wrong[0].value", 2 * -1)
E("l10", "screens[5].explain.text", 2 ** -2)
E("l10", "screens[5].explain.text", 2 ** -3)
c = lambda x: x ** 3 - 4 * x
E("l10", "screens[6].explain.text", c(1))
E("l10", "screens[6].hints[2].text", c(1))
lv.claim(roots_quad(1, 0, -4) == [-2, 2], "l10 s6 quad option x^2 - 4 crosses at -2 and 2, as the cubic does")
lv.claim(c(-2) == 0 and c(2) == 0 and c(0) == 0, "l10 s6 cubic crosses at -2, 0, 2")
E("l10", "screens[7].widget.options[1].why", 1 / 0.5)          # rule at 0.5
E("l10", "screens[7].widget.options[1].why", 0.5)              # segment y = x at 0.5
E("l10", "screens[7].hints[2].text", 1 / -0.5)
price = lambda yld: 100 / (1 + yld) ** 10
p2, p4, p6, p8 = (round(price(r / 100), 2) for r in (2, 4, 6, 8))
for p in (p2, p4, p6, p8):
    E("l10", "screens[9].canvas", p)
lv.claim((p2, p4, p6, p8) == (82.03, 67.56, 55.84, 46.32), f"l10 s9 bond prices {p2} {p4} {p6} {p8}")
E("l10", "screens[9].question", round(p2 - p4, 2))
E("l10", "screens[9].widget.answer", round(p6 - p8, 2))
E("l10", "screens[9].widget.wrong[0].value", round(p2 - p4, 2))
E("l10", "quiz[0].widget.answer", (-3) ** 2 - 3)
E("l10", "quiz[0].widget.wrong[0].value", -9 - 3)
E("l10", "quiz[2].widget.answer", round(3 ** -2, 4))
E("l10", "quiz[2].widget.wrong[0].value", 3 * -2)
E("l10", "quiz[2].widget.wrong[1].value", -(3 ** 2))
E("l10", "quiz[3].explain.text", 2 ** 0 + 1)
# Coverage claims in the summary: true only for a positive leading coefficient and a base above 1.
lv.stated("l10", "summary.ideas", "Quadratics make a U, cubics run bottom left to top right", False)

# ---------------- l11 reading a graph ----------------
f = lambda x: x * x - 2 * x - 3
E("l11", "screens[1].canvas", f(-2))
E("l11", "screens[1].widget.points[0].target", f(1))
E("l11", "screens[1].hints[2].text", f(1))
lv.claim(roots_quad(1, -2, -3) == [-1, 3], "l11 f roots -1 and 3")
E("l11", "screens[3].widget.points[1].target", 3)
E("l11", "screens[3].canvas", f(4))
E("l11", "screens[4].widget.answer", f(0))
E("l11", "screens[4].widget.wrong[2].value", f(1))
g = lambda x: 4 * x - x * x
lv.claim(g(2) == 4 and g(0) == 0 and g(4) == 0, "l11 s5 g turning (2, 4), roots 0 and 4")
h = lambda x: x ** 3 - 3 * x ** 2 + 4
lv.claim(h(0) == 4 and h(2) == 0 and h(-1) == 0, "l11 s6 h(0) = 4, h(2) = 0, h(-1) = 0")
lv.claim(all(3 * x * x - 6 * x == 0 for x in (0, 2)), "l11 s6 turning points at x = 0 and 2")
above = [x / 100 for x in range(-200, 351) if h(x / 100) > 0]
lv.stated("l11", "screens[6].widget.options[1].why", "You picked where the curve sits above the x-axis",
          max(above) < 2)                      # h > 0 also for every x > 2 on the canvas, so -1 < x < 2 is not "where it sits above"
k = lambda x: x * x - x - 2
lv.claim(roots_quad(1, -1, -2) == [-1, 2], "l11 s7 roots -1 and 2")
lv.claim(k(1) == -2 and k(-2) == 4, "l11 s7 option d: f(1) = -2, not 0 (and f(-2) = 4)")
E("l11", "screens[7].widget.options[3].why", k(1))
E("l11", "screens[7].explain.text", k(0))
E("l11", "screens[8].widget.options[0].text", (0 - 5) * (0 + 2))
E("l11", "screens[8].widget.options[3].text", -5 + 2)
sm = lambda s: 0.01 * (s - 105) ** 2 + 18
E("l11", "screens[9].canvas", sm(85))
E("l11", "screens[9].widget.answer", 105)
E("l11", "screens[9].widget.wrong[1].value", sm(105))
q = lambda x: x * x + 2 * x - 3
lv.claim(roots_quad(1, 2, -3) == [-3, 1] and q(-1) == -4 and q(0) == -3, "l11 quiz0 roots -3, 1; turning (-1, -4); f(0) = -3")
q1 = lambda x: x * x - 6 * x + 8
E("l11", "quiz[1].widget.answer", q1(0))
E("l11", "quiz[1].widget.wrong[0].value", 2)
E("l11", "quiz[1].widget.wrong[1].value", 4)
E("l11", "quiz[1].widget.wrong[2].value", q1(3))
lv.claim(roots_quad(1, -6, 8) == [2, 4], "l11 quiz1 roots 2 and 4")
lv.claim(q1(0) not in roots_quad(1, -6, 5), "l11 quiz1 the key (y-intercept 5) is not also a root",
         f"roots are {roots_quad(1, -6, 5)}: a learner who answers the root 5 is marked right")
q3 = lambda x: (x - 2) * (x - 6)
E("l11", "quiz[3].widget.answer", q3(4))
E("l11", "quiz[3].widget.wrong[1].value", q3(0))

# ---------------- l12 graphs that tell stories ----------------
sam = lambda t: min(80 * t, 800, 800 - 80 * (t - 15))
lv.claim(sam(10) == 800 and sam(15) == 800 and sam(25) == 0, "l12 Sam at the shop 10 to 15 min, home at 25")
E("l12", "screens[4].widget.answer", (0 - 800) / (25 - 15))
E("l12", "screens[4].widget.wrong[1].value", 0 - 800)
for t, gr in ((1, 2), (5, 10), (3, 6)):
    lv.claim(2 * t == gr, f"l12 gradient of t^2 at {t} is {gr}")
E("l12", "screens[3].widget.answer", 2 * 3)
E("l12", "screens[3].widget.wrong[0].value", 3 ** 2 / 3)
E("l12", "screens[3].widget.wrong[1].value", 3 ** 2)
bill = lambda u: min(0.3 * u, 10 + 0.2 * u)
lv.claim(abs(bill(100) - 30) < 1e-9 and abs(bill(200) - 50) < 1e-9, "l12 s5 bill A (100, 30), B (200, 50)")
E("l12", "screens[5].widget.answer", (bill(200) - bill(100)) / 100)
E("l12", "screens[5].widget.wrong[0].value", bill(200) / 200)
jo = lambda t: min(100 * t, 200, 200 - 100 * (t - 3))
lv.claim([jo(t) for t in range(6)] == [0, 100, 200, 200, 100, 0], "l12 s6 Jo heights 0,100,200,200,100,0")
sh = lambda t: 100 + 6 * t - t * t
lv.claim(sh(3) == 109 and sh(1) == 105 and 6 - 2 * 0 == 6, "l12 s7 high 109 at 3; P start 105; steepest 6 at the open")
pl = [0, 120, 260, 310, 240, 150, 90, 180, 300, 420]
dd, (pi, ti) = max_drawdown(pl)
E("l12", "screens[9].widget.answer", dd)
lv.claim((pi, ti) == (3, 6), "l12 s9 peak day 3, trough day 6")
E("l12", "screens[9].widget.wrong[0].value", max(pl) - pl[ti])
lv.stated("l12", "screens[9].feedback.byKey.max-min", "You took the lowest value from the highest",
          max(pl) - min(pl) == 330)            # highest minus lowest is 420 - 0 = 420; 330 is 420 - 90 (the trough)
E("l12", "quiz[1].widget.answer", (240 - 600) / 12)
E("l12", "quiz[1].widget.wrong[1].value", 240 - 600)
v = [0, 150, 200, 120, 100, 160]
ch = [b - a for a, b in zip(v, v[1:])]
lv.claim(ch == [150, 50, -80, -20, 60], "l12 quiz2 daily changes")
lv.claim(ch.index(min(ch)) == 2, "l12 quiz2 steepest fall days 2 to 3")
E("l12", "quiz[3].widget.answer", 4 ** 2 / 4)
E("l12", "quiz[3].widget.wrong[0].value", 2 * 4)

# ---------------- l13 solving with graphs ----------------
lv.claim(roots_quad(1, 0, -4) == [-2, 2] and roots_quad(1, 0, -1) == [-1, 1] and roots_quad(1, 0, -9) == [-3, 3], "l13 x^2 = 4, 1, 9")
lv.claim(roots_quad(1, -1, -2) == [-1, 2], "l13 s3 x^2 = x + 2 at -1 and 2")
E("l13", "screens[3].canvas", (-2.5) ** 2)
lv.claim(roots_quad(1, -2, -3) == [-1, 3], "l13 s4 x^2 - 3 = 2x at -1 and 3")
E("l13", "screens[4].widget.answer", 3)
E("l13", "screens[4].widget.wrong[0].value", 2 * 3)
E("l13", "screens[4].explain.text", 2 * -1)
r = bisect(lambda x: 2 ** x - x - 2, -3, 0)
E("l13", "screens[5].widget.answer", round(r, 1))
E("l13", "screens[5].widget.accept", round(r, 2))
E("l13", "screens[5].explain.text", round(r + 2, 2))
E("l13", "screens[5].hints[2].text", round(2 ** -1.7, 2))
lv.claim(2 ** 2 == 2 + 2, "l13 s5 x = 2 solves 2^x = x + 2")
lv.claim(roots_quad(1, -2, -8) == [-2, 4], "l13 s6 x^2 - 2x - 3 = 5 at -2 and 4")
lv.claim(roots_quad(1, 1, -6) == [-3, 2], "l13 s8 x^2 + x - 6 = 0 at -3 and 2")
E("l13", "screens[8].widget.lines[2].text", (-3) ** 2)
prem = 4.5 + 3.5
E("l13", "screens[9].prose", prem)
lv.claim((100 - prem, 100 + prem) == (92, 108), "l13 s9 straddle breakevens 92 and 108")
E("l13", "screens[9].widget.options[2].text", 100 - prem / 2)
E("l13", "screens[9].widget.options[3].text", 100 - 3.5)
E("l13", "screens[9].widget.options[3].text", 100 + 4.5)
lv.claim(roots_quad(1, -2, -3) == [-1, 3] and 3 ** 2 - 4 == 5, "l13 quiz1 crossings x = -1, 3; height 5")
E("l13", "quiz[3].widget.options[0].text", 50 - 6)
E("l13", "quiz[3].widget.options[1].text", 50 - 3)

# ---------------- review-3 ----------------
E("review", "items[0].widget.answer", (-2) ** 3 + 5)
E("review", "items[0].widget.wrong[0].value", 2 ** 3 + 5)
E("review", "items[0].widget.wrong[1].value", -2 * 3 + 5)
E("review", "items[0].widget.wrong[2].value", (-2) ** 2 + 5)
E("review", "items[0].feedback.correct", (-2) ** 3)
lv.claim(roots_quad(1, -4, 0) == [0, 4], "review-3 items[1] roots 0 and 4, turning x = 2")
E("review", "items[1].explain.text", 2 * 2 - 4 * 2)
E("review", "items[2].widget.answer", (18 - 3) / 6)
E("review", "items[2].widget.wrong[0].value", 18 / 6)
lv.claim(roots_quad(1, -3, -4) == [-1, 4], "review-3 items[3] x^2 - 2x = x + 4 at -1 and 4")
E("review", "items[3].widget.answer", -1)
E("review", "items[3].widget.wrong[0].value", (-1) ** 2 - 2 * (-1))
E("review", "items[3].widget.wrong[1].value", 4)
lv.claim(4 ** 2 - 2 * 4 == 4 + 4, "review-3 items[3] larger crossing (4, 8)")
E("review", "items[4].widget.options[0].text", 12 / 4)
E("review", "items[5].widget.answer", (0 + 4) * (0 - 2))
sh2 = lambda x: 100 + 8 * x - x * x
for x in (1, 4, 6):
    E("review", "items[6].explain.text", 8 - 2 * x)
    E("review", "items[6].canvas", sh2(x))
lv.claim(sh2(1) < sh2(6) < sh2(4), "review-3 items[6] A lowest of the three, B highest")
lv.claim(2 ** 1 == 3 - 1, "review-3 items[7] crossing at x = 1")

# ---------------- homework-3 ----------------
E("homework", "items[0].widget.answer", 6 / -4)
E("homework", "items[0].widget.wrong[1].value", round(-4 / 6, 4))
hf = lambda x: x * x - 10 * x + 16
lv.claim(roots_quad(1, -10, 16) == [2, 8], "homework-3 items[1] roots 2 and 8")
E("homework", "items[1].widget.answer", hf(5))
E("homework", "items[1].widget.wrong[0].value", 5)
E("homework", "items[1].widget.wrong[1].value", hf(0))
lv.claim([4 - x * x for x in range(-3, 4)] == [-5, 0, 3, 4, 3, 0, -5], "homework-3 items[2] heights")
v3 = [0, 200, 150, 380, 300, 180, 260, 410, 350]
E("homework", "items[3].widget.answer", max_drawdown(v3)[0])
E("homework", "items[3].widget.wrong[0].value", 380 - 150)
E("homework", "items[3].widget.wrong[1].value", 410 - 350)
E("homework", "items[3].widget.wrong[2].value", 200 - 150)
E("homework", "items[4].widget.answer", 60 - (3 + 2) - 4)
E("homework", "items[4].widget.wrong[0].value", 60 - 4)
E("homework", "items[4].widget.wrong[1].value", 60 - (3 + 2))
E("homework", "items[5].widget.lines[4].text", 2 ** 3 - 2 - 6)
lv.claim(2 * 2 - 4 * 3 < 0, "homework-3 items[5] x^2 + 2x + 3 has no real root, so (2, 8) is the only crossing")
E("homework", "items[6].widget.points[0].target", 4 / 2)
E("homework", "items[6].feedback.byKey.end", 2 * 4)
lv.claim(2 * 2 == 4, "homework-3 items[6] gradient 2t is 4 at t = 2 (true, but 2t is never taught: a continuity finding, not a number)")
P = lambda yld: 100 / (1 + yld) ** 5
for r_, pr, fac in ((0.02, 90.57, 1.10408), (0.04, 82.19, 1.21665), (0.06, 74.73, 1.33823)):
    E("homework", "items[7].model", round(P(r_), 2))
    E("homework", "items[7].model", round((1 + r_) ** 5, 5))
E("homework", "items[7].model", round(100 - P(0.02), 2))
E("homework", "items[7].model", round(round(P(0.04), 2) - round(P(0.06), 2), 2))
frac = (82.19 - 80) / (82.19 - 74.73)
E("homework", "items[7].model", round(frac, 2))
E("homework", "items[7].model", round(4 + frac * 2, 1))
E("homework", "items[7].model", round(1.046 ** 5, 4))
exact = (100 / 80) ** 0.2 - 1
E("homework", "items[7].model", round(exact * 100, 2))
lv.claim(exact < 0.04 + frac * 0.02, "homework-3 items[7] straight-line reading overestimates the yield")
lv.claim(round(100 / 1.2522, 2) == 79.86 and "100 \\div 1.252 \\approx" not in lv.text("homework", "items[7].model"), "homework items[7] 100 / 1.2522 = 79.86, old 1.252 wording gone")

lv.check_wrongs()
lv.report()
