"""Number recompute for functions level 4 (Building new functions): l14 to l18, review-4, homework-4.
Second reader, session V (no author script existed).

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations
are recomputed a second way (direct evaluation of each transformed rule, exact logs from math.log).
Expression keys are checked here only for equality with their accepted forms; what the live grader accepts
(y = ... and f(x) = ... forms) was tested separately with app/js/engine/grade.js and is reported in the review.
    python3 docs/reports/functions-L4-numbers.py
Failing checks on the current content are findings in docs/reviews/review-functions-3-4.md.
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("functions", 4)
E = lv.expect
PTS = [0.3, 0.7, 1.1, 1.9, 2.4, 3.0, -1.3]


def same(f, g):
    return all(abs(f(x) - g(x)) < 1e-9 for x in PTS)


def top(f, lo, hi, step=0.001, low=False):
    xs = [lo + i * step for i in range(int((hi - lo) / step) + 1)]
    best = min(xs, key=f) if low else max(xs, key=f)
    return round(best, 3), round(f(best), 3)


# ---------------- l14 sliding ----------------
sq = lambda x: x * x
E("l14", "screens[0].widget.points[0].target", sq(0) + 3)
E("l14", "screens[2].widget.options[0].text", abs(-2) - 3)
E("l14", "screens[3].widget.answer", top(lambda x: (x + 3) ** 2, -6, 6, low=True)[0])
E("l14", "screens[3].widget.wrong[1].value", (0 + 3) ** 2)
lv.claim([(x + 3) ** 2 for x in (-5, -3, 0)] == [4, 0, 9], "l14 s4 table 4, 0, 9")
hill = lambda x: 4 - (x - 1) ** 2
lv.claim(top(lambda x: hill(x + 4), -6, 7) == (-3.0, 4.0), "l14 s5 f(x + 4) peaks at (-3, 4)")
E("l14", "screens[5].widget.options[0].why", 5 + 4)
lv.claim(same(lambda x: 2 * (x + 1), lambda x: 2 * x + 2), "l14 s6 2(x + 1) = 2x + 2")
E("l14", "screens[6].widget.answer", 2 * (0 + 1) - 2 * 0)
lv.claim(same(lambda x: (x - 3) ** 2 + 2, lambda x: x * x - 6 * x + 11), "l14 s8 accept x^2 - 6x + 11 equals (x - 3)^2 + 2")
E("l14", "screens[9].widget.answer", 100 + 3.5)
E("l14", "screens[9].widget.wrong[1].value", 100 - 3.5)
E("l14", "quiz[0].widget.options[0].text", 7 + 5)
E("l14", "quiz[1].widget.options[3].text", (0 - 5) ** 2)
E("l14", "quiz[2].widget.answer", 6 - 2)
E("l14", "quiz[2].widget.wrong[0].value", 6 + 2)
lv.claim(same(lambda x: 3 * (x - 2), lambda x: 3 * x - 6), "l14 quiz3 3(x - 2) = 3x - 6")
E("l14", "quiz[3].widget.answer", 6)

# ---------------- l15 stretching ----------------
f = lambda x: 4 - (x - 2) ** 2
lv.claim(top(f, -2, 6) == (2.0, 4.0), "l15 f top (2, 4)")
E("l15", "screens[0].widget.points[0].target", 2 * f(2))
E("l15", "screens[0].widget.wrong[0].region", f(2) + 2 - 0.3)
lv.claim(f(0) == 0 and f(4) == 0, "l15 s1 f meets the x-axis at 0 and 4")
lv.claim(f(1) == 3, "l15 s2 (1, 3) on f")
E("l15", "screens[2].widget.options[0].text", 3 * f(1))
E("l15", "screens[3].widget.points[0].target", -f(2))
E("l15", "screens[3].widget.wrong[1].region", f(2) - 1 - 0.3)
lv.claim(top(lambda x: f(-x), -6, 6) == (-2.0, 4.0), "l15 s4 f(-x) top (-2, 4)")
lv.claim(top(lambda x: f(2 * x), -1, 9)[0] == 1.0 and top(lambda x: f(0.5 * x), -1, 9)[0] == 4.0, "l15 s5 f(2x) top x = 1, f(x/2) top x = 4")
E("l15", "screens[5].feedback.byKey.half", 2 / 0.5)
lv.claim(f(0.5 * 8) == 0 and f(0.5 * 0) == 0, "l15 s6 f(x/2) stands on 0 and 8, twice as wide")
d = lambda t: t / 5
lv.claim(d(25) == 5, "l15 s7 first runner 5 km at 25 min")
E("l15", "screens[7].widget.answer", 25 / 2)
E("l15", "screens[7].widget.wrong[0].value", 25 * 2)
fx = lambda x: x * x - 4 * x
lv.claim(same(lambda x: fx(-x), lambda x: x * x + 4 * x), "l15 s9 f(-x) = x^2 + 4x")
lv.claim(same(lambda x: -fx(x), lambda x: -x * x + 4 * x), "l15 s9 wrong 'outside' is -f(x)")
E("l15", "screens[9].explain.text", fx(2))
lv.claim(fx(2) == (-2) ** 2 + 4 * (-2), "l15 s9 check f(2) = new rule at -2")
P = lambda s: 100 * (s - 24.5)
E("l15", "screens[10].hints[2].text", round(P(26.10), 6))
E("l15", "screens[10].widget.answer", round(2 * P(26.10), 6))
E("l15", "screens[10].widget.wrong[1].value", 2 * 26.10)
E("l15", "quiz[1].widget.options[0].text", 6 / 3)
E("l15", "quiz[1].widget.options[1].text", 6 * 3)
lv.claim(9 - 9 == 0, "l15 quiz2 5f(x) = 0 at x = 3")
E("l15", "quiz[3].widget.answer", 60 / 3)
E("l15", "quiz[3].widget.wrong[0].value", 60 * 3)

# ---------------- l16 machine after machine ----------------
E("l16", "screens[0].widget.answer", 2 * (5 + 3))
E("l16", "screens[0].widget.wrong[0].value", 2 * 5 + 3)
E("l16", "screens[0].widget.wrong[1].value", 2 * 5)
E("l16", "screens[1].widget.options[1].why", 2 * (0 + 3))
F_, G_ = (lambda x: x + 3), (lambda x: 2 * x)
E("l16", "screens[2].widget.answer", F_(G_(4)))
E("l16", "screens[2].widget.wrong[0].value", G_(F_(4)))
E("l16", "screens[2].widget.wrong[1].value", F_(4))
lv.claim([G_(F_(x)) for x in (0, 1, 2, 5)] == [6, 8, 10, 16], "l16 s3 table 6, 8, 10, 16")
lv.claim(same(lambda x: F_(x) * G_(x), lambda x: 2 * x * x + 6 * x), "l16 s3 product option 2x^2 + 6x")
s, h = (lambda x: x * x), (lambda x: x - 4)
E("l16", "screens[4].widget.answer", s(h(1)))
E("l16", "screens[4].widget.wrong[0].value", h(s(1)))
f5, g5 = (lambda x: x * x), (lambda x: x + 1)
E("l16", "screens[5].widget.options[0].text", g5(f5(3)))
E("l16", "screens[5].widget.options[1].text", f5(g5(3)))
E("l16", "screens[5].widget.options[2].text", g5(3) * f5(3))
lv.claim(same(lambda x: (x + 3) - 5, lambda x: (x - 5) + 3), "l16 s6 add 3 and subtract 5 commute")
E("l16", "screens[7].widget.answer", 3 * 4 - 2)
E("l16", "screens[7].widget.wrong[0].value", 3 * (4 - 2))
lv.claim(same(lambda x: 3 * x * x - 1, lambda x: 3 * (x * x) - 1), "l16 s8 f(g(x)) = 3x^2 - 1")
prices = [100 * 1.1 ** n for n in range(5)]
logs = [round(math.log(p), 4) for p in prices]
for L in logs[:4]:
    E("l16", "screens[9].canvas", L)
E("l16", "screens[9].widget.answer", logs[4])
E("l16", "screens[9].hints[2].text", round(math.log(1.1), 4))
E("l16", "screens[9].widget.wrong[0].value", round(logs[3] * 1.1, 4))
E("l16", "screens[9].canvas", round(prices[4], 2))
E("l16", "quiz[0].widget.answer", 4 * (10 - 7))
E("l16", "quiz[0].widget.wrong[0].value", 4 * 10 - 7)
E("l16", "quiz[2].widget.answer", 4 + 3)
E("l16", "quiz[2].widget.wrong[1].value", -4 + 3)
E("l16", "quiz[3].explain.text", round(math.log(0.8), 4))

# ---------------- l17 running backwards ----------------
E("l17", "screens[0].widget.answer", (17 - 3) / 2)
E("l17", "screens[0].widget.wrong[0].value", 2 * 17 + 3)
E("l17", "screens[0].widget.wrong[1].value", 17 / 2 - 3)
E("l17", "screens[0].widget.wrong[2].value", 17 / 2)
E("l17", "screens[1].widget.points[0].target", -3)
lv.claim(2 * -3 + 3 == -3, "l17 s1 2x + 3 meets y = x at (-3, -3)")
E("l17", "screens[2].widget.answer", (11 - 3) / 2)
E("l17", "screens[2].widget.wrong[0].value", 2 * 11 + 3)
E("l17", "screens[2].widget.wrong[1].value", 11 / 2 - 3)
E("l17", "screens[2].widget.wrong[2].value", 1 / (2 * 11 + 3))
lv.claim(0.5 * 4 + 1 == 3 and 2 * 3 - 2 == 4, "l17 s3 g(4) = 3 and g^-1(x) = 2x - 2 sends 3 to 4")
E("l17", "screens[4].widget.answer", 6 - 4)
E("l17", "screens[4].widget.wrong[0].value", 1 / (6 + 4))
E("l17", "screens[4].widget.wrong[1].value", round(1 / 6, 4))
lv.claim(same(lambda x: (5 * x - 2 + 2) / 5, lambda x: x), "l17 s7 (x + 2)/5 undoes 5x - 2")
lv.claim(same(lambda x: (x + 2) / 5, lambda x: 0.2 * x + 0.4), "l17 s7 accept 0.2x + 0.4")
PL = lambda S: 250 * (S - 8.40) - 12.50
E("l17", "screens[8].widget.answer", round(8.40 + (300 + 12.50) / 250, 6))
E("l17", "screens[8].widget.wrong[0].value", round(8.40 + 300 / 250, 6))
E("l17", "screens[8].widget.wrong[1].value", round(8.40 + (300 - 12.50) / 250, 6))
lv.claim(abs(PL(9.65) - 300) < 1e-9, "l17 s8 P(9.65) = 300")
lv.claim(abs(lv.files['l17-running-backwards']['screens'][8]['widget']['wrong'][2]['value'] - PL(300)) <= 0.5,
         "l17 s8 wrong 'forward' (fed 300 into P) equals P(300)",
         f"P(300) = {PL(300)}, but the wrong value is 74987.5 (that is 250 x 300 - 12.50, which drops the 8.40)")
E("l17", "quiz[0].widget.answer", (13 + 5) / 3)
E("l17", "quiz[0].widget.wrong[0].value", 3 * 13 - 5)
E("l17", "quiz[0].widget.wrong[1].value", round(13 / 3 + 5, 4))
E("l17", "quiz[3].widget.answer", (10 - 6) * 4)
E("l17", "quiz[3].widget.wrong[0].value", 10 / 4 + 6)
E("l17", "quiz[3].widget.wrong[1].value", 10 * 4 - 6)

# ---------------- l18 payoff is a function ----------------
call = lambda S, K=100: max(S - K, 0)
put = lambda S, K=100: max(K - S, 0)
E("l18", "screens[0].widget.answer", call(93))
E("l18", "screens[0].widget.wrong[0].value", 93 - 100)
E("l18", "screens[1].widget.answer", call(112, 105))
E("l18", "screens[1].widget.wrong[0].value", call(112))
lv.claim([put(S) for S in (80, 90, 100, 110, 120)] == [20, 10, 0, 0, 0], "l18 s3 put control points")
lv.claim(all(put(S) == call(200 - S) for S in range(80, 121)), "l18 s3 put is the call reflected in S = 100")
E("l18", "screens[4].widget.answer", 100 + 4)
E("l18", "screens[4].widget.wrong[1].value", 100 - 4)
E("l18", "screens[5].widget.options[0].text", call(60) - 4)
E("l18", "screens[5].widget.options[1].text", 60 - 104)
E("l18", "screens[5].widget.options[3].text", 60 - 100)
E("l18", "screens[7].explain.text", -3)
E("l18", "screens[8].widget.lines[3].text", 100 - 3)
E("l18", "screens[9].widget.answer", round(9.95 / 0.001, 6))
E("l18", "screens[9].widget.wrong[0].value", round(9.95 / 0.01, 6))
E("l18", "screens[9].explain.text", max(9.95, 0.001 * 15000))
E("l18", "quiz[0].widget.answer", call(56, 50) - 2.5)
E("l18", "quiz[0].widget.wrong[1].value", call(56, 50) + 2.5)
E("l18", "quiz[1].widget.answer", put(86, 80))
E("l18", "quiz[2].widget.options[0].text", 10 - 3)
E("l18", "quiz[2].widget.options[1].text", 2 * 3)
E("l18", "quiz[3].widget.answer", max(5, 0.002 * 1800))
E("l18", "quiz[3].widget.wrong[0].value", 0.002 * 1800)

# ---------------- review-4 ----------------
E("review", "items[1].widget.answer", -3 * 5)
E("review", "items[1].widget.wrong[1].value", 5 - 3)
E("review", "items[2].widget.answer", (-3) ** 2 - 2)
E("review", "items[2].widget.wrong[0].value", (-3 - 2) ** 2)
E("review", "items[2].widget.wrong[1].value", -9 - 2)
E("review", "items[3].widget.answer", 5 * 4 - 1)
E("review", "items[3].widget.wrong[0].value", (5 + 1) / 4)
E("review", "items[3].widget.wrong[1].value", (5 - 1) * 4)
E("review", "items[3].widget.wrong[2].value", round(4 / 6, 4))
E("review", "items[4].widget.answer", put(108, 120) - 5)
E("review", "items[4].widget.wrong[1].value", put(108, 120) + 5)
E("review", "items[5].widget.options[0].text", 1 + 4)
E("review", "items[5].widget.options[0].text", 2 * 3)
E("review", "items[6].widget.answer", 6 * 3)
E("review", "items[7].widget.answer", 2 * (call(110) - 3))
E("review", "items[7].widget.wrong[1].value", 2 * call(110) - 3)
E("review", "items[8].feedback.correct", round(200 * 1.05 * 0.95, 2))
E("review", "items[8].explain.text", round(200 * 1.05 * 0.95, 2))
E("review", "items[8].explain.text", round((1 - 1.05 * 0.95) * 100, 2))
lv.claim(math.log(1.05 * 0.95) < 0, "review-4 items[8] log ends lower")

# ---------------- homework-4 ----------------
lv.claim(same(lambda x: -x * x + 5, lambda x: 5 - x * x), "homework-4 items[0] -x^2 + 5 = 5 - x^2")
lv.claim(same(lambda x: -(x * x + 5), lambda x: -x * x - 5), "homework-4 items[0] wrong 'order' is -(x^2 + 5)")
E("homework", "items[1].widget.answer", 3 - 2)
E("homework", "items[1].widget.wrong[0].value", -3 - 2)
lv.claim(top(lambda x: f(2 * x) + 1, -2, 6) == (1.0, 5.0), "homework-4 items[2] top of f(2x) + 1 is (1, 5)")
E("homework", "items[3].widget.answer", math.sqrt((17 + 1) / 2))
E("homework", "items[3].widget.wrong[1].value", round((math.sqrt(17) + 1) / 2, 4))
lv.claim((3 * 6 + 2) / 5 == 4 and (5 * 4 - 2) / 3 == 6, "homework-4 items[4] f(6) = 4 and f^-1(4) = 6")
E("homework", "items[5].widget.answer", 100 * 0.5 + 160 * 0.3)
E("homework", "items[5].widget.wrong[0].value", 260 * 0.3)
E("homework", "items[5].widget.wrong[1].value", 260 * 0.5)
net = 7 - 2.5
E("homework", "items[6].widget.answer", 95 + net)
E("homework", "items[6].widget.wrong[1].value", 95 + 7)
E("homework", "items[6].widget.wrong[2].value", 95 + 2.5)
E("homework", "items[6].explain.text", 10 - net)
E("homework", "items[7].widget.answer", round(math.log(45 / 50), 4))
E("homework", "items[7].widget.wrong[2].value", round(math.log(1.2), 4))
E("homework", "items[7].explain.text", round(math.log(0.75), 4))
lv.claim(round(math.log(1.2) + math.log(0.75), 4) == round(math.log(0.9), 4), "homework-4 items[7] log moves add to ln 0.9")
pos = lambda S: 50 * (call(S) - 4)
lv.claim(pos(60) == -200 and pos(104) == 0 and pos(110) == 300 and pos(114) == 500, "homework-4 items[8] -200, 104, 300, 114")
E("homework", "items[8].model", 2 * 200)
E("homework", "items[8].model", 2 * 300)

lv.check_wrongs()
lv.report()
