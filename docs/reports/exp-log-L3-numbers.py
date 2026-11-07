"""Second-read number checks for exp-log level 3 (The natural base): l9 to l13, review-3, homework-3.
Written by the second reader (docs/reviews/review-exp-log-1-3.md). Checks marked "content wrong" fail until the fix pass."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("exp-log", 3)
E = lv.expect
ln, exp, log = math.log, math.exp, math.log10
L2 = ln(2)


def r2(x):
    return math.floor(x * 100 + 0.5) / 100


# ---- l9 compounding more often
lv.claim(365 * 24 * 3600 == 31536000, "l9 s1: a year has 31,536,000 seconds")
E("l9", "screens[1].hints[2].text", round((13 / 12) ** 12, 2))
lv.claim(2.25 < (1 + 1 / 31536000) ** 31536000 < 3, "l9 s1: payments every second give between £2.25 and £3.00")
E("l9", "screens[1].explain.text", round((1 + 1 / 31536000) ** 31536000, 2))
E("l9", "screens[2].widget.options[3].why", round((1 + 1 / 52) ** 52, 2))
lv.claim((1 + 1 / 52) ** 52 - (1 + 1 / 51) ** 51 < 0.01, "l9 s2: from 51 to 52 the gain is under 1p")
E("l9", "screens[3].widget.rows[2][1].answer", round(1.25 ** 4, 4))
E("l9", "screens[3].widget.rows[3][1].answer", round((13 / 12) ** 12, 3))
E("l9", "screens[3].widget.rows[4][1]", round((1 + 1 / 365) ** 365, 4))
E("l9", "screens[3].widget.rows[5][1]", round((1 + 1e-6) ** 1e6, 4))
E("l9", "screens[3].feedback.byKey.r3c1", round(1.0833 ** 12, 4))
E("l9", "screens[4].canvas.state.values.12", r2(100 * (1 + 0.1 / 12) ** 12))
E("l9", "screens[4].canvas.state.values.365", r2(100 * (1 + 0.1 / 365) ** 365))
E("l9", "screens[4].widget.options[0].text", r2(100 * exp(0.1)))
E("l9", "screens[4].widget.options[1].text", r2(100 * math.e))
E("l9", "screens[4].widget.options[2].text", r2(10 * math.e))
E("l9", "screens[4].hints[2].text", round(exp(0.1), 5))
E("l9", "screens[5].canvas.state.values.Yearly", r2(1000 * 1.05 ** 10))
E("l9", "screens[5].canvas.state.values.Monthly", r2(1000 * (1 + 0.05 / 12) ** 120))
E("l9", "screens[5].canvas.state.values.Daily", r2(1000 * (1 + 0.05 / 365) ** 3650))
E("l9", "screens[5].widget.answer", r2(1000 * exp(0.5)))
E("l9", "screens[5].widget.wrong[1].value", r2(1000 * exp(0.05)))
E("l9", "screens[5].widget.wrong[2].value", r2(10000 * exp(0.05)))
E("l9", "screens[5].explain.text", round(100 * (r2(1000 * exp(0.5)) - r2(1000 * (1 + 0.05 / 365) ** 3650))))
E("l9", "screens[6].widget.options[0].why", r2(10000 * exp(0.06)))
E("l9", "screens[6].explain.text", round(10620 - r2(10000 * exp(0.06)), 2))
E("l9", "screens[7].widget.options[1].why", round(exp(4), 1))
E("l9", "screens[7].explain.text", round(exp(0.04), 4))
E("l9", "screens[9].widget.answer", round(exp(0.05) - 1, 5))
E("l9", "screens[9].widget.wrong[1].value", round(0.05 * math.e, 4))
E("l9", "screens[9].explain.text", r2(2e6 * (exp(0.05) - 1)))
E("l9", "quiz[0].widget.answer", r2(2500 * exp(0.12)))
E("l9", "quiz[0].widget.wrong[0].value", r2(2500 * 1.04 ** 3))
E("l9", "quiz[0].widget.wrong[1].value", r2(2500 * exp(0.04)))
E("l9", "quiz[1].feedback.correct", round(1.001 ** 1000, 5))
E("l9", "quiz[2].widget.answer", r2(5000 * exp(-0.01)))
E("l9", "quiz[2].widget.wrong[0].value", r2(5000 * exp(0.01)))
E("l9", "quiz[3].explain.text", round(1.02 ** 4, 5))
E("l9", "quiz[3].explain.text", round(exp(0.079), 5))
# coverage claims: "the higher rate wins" is not a rule; 7.9% continuous beats 8% paid once
lv.stated("l9", "quiz[3].explain.text", "The higher rate wins, even with fewer payments", exp(0.079) < 1.08)   # content wrong (finding 24)
lv.stated("l9", "screens[6].explain.text", "The rate itself matters more than how often it is paid", exp(0.079) < 1.08)  # content wrong (finding 24)

# ---- l10 natural log
E("l10", "screens[1].widget.points[0].target[0]", round(ln(5), 3))
E("l10", "screens[2].widget.options[1].why", round(exp(2), 2))
E("l10", "screens[3].prose", round(ln(5), 3))
E("l10", "screens[4].canvas.state.points[0].x", round(exp(-1), 4))
E("l10", "screens[5].widget.rows[0][1].answer", round(ln(6), 4))
E("l10", "screens[5].widget.rows[1][1].answer", round(ln(8), 4))
E("l10", "screens[5].widget.rows[2][1].answer", round(ln(1.5), 4))
E("l10", "screens[6].widget.states.s3.tex", round(ln(1.5) / 0.04, 2))
E("l10", "screens[6].widget.states.bad2.tex", round(ln(1500) / 40, 2))
E("l10", "screens[6].widget.states.bad3.tex", round(1.5 / math.e, 4))
E("l10", "screens[7].widget.options[0].text", round(ln(3), 4))
E("l10", "screens[7].widget.options[1].why", round(exp(3), 1))
E("l10", "screens[10].widget.answer", round(ln(100 / 92.31) / 2, 2))
E("l10", "screens[10].widget.wrong[0].value", round((100 / 92.31 - 1) / 2, 5))
E("l10", "screens[10].widget.wrong[2].value", round(math.sqrt(100 / 92.31) - 1, 5))
E("l10", "screens[10].hints[2].text", round(ln(100 / 92.31), 5))
lv.claim_text("l10", "screens[10].hints[1].text", "1.08333", abs(100 / 92.31 - 1.08333) < 5e-6,
              "l10 s10: 100 / 92.31 is 1.08333 to five places")                          # content wrong (finding 29)
E("l10", "quiz[0].widget.answer", round(ln(20), 4))
E("l10", "quiz[0].widget.wrong[0].value", round(20 / math.e, 3))
E("l10", "quiz[0].widget.wrong[1].value", round(log(20), 3))
E("l10", "quiz[0].explain.text", round(exp(3), 1))
E("l10", "quiz[1].explain.text", round(ln(25), 4))
E("l10", "quiz[2].widget.answer", round(ln(2.5) / 0.06, 2))
E("l10", "quiz[2].widget.wrong[0].value", round(6000 / 240))
E("l10", "quiz[2].widget.wrong[1].value", round(ln(6000) / 0.06))
E("l10", "quiz[3].widget.options[3].why", round(exp(0.5), 2))

# ---- l11 log returns
E("l11", "screens[2].widget.options[1].why", round(140 / 100 - 1 + 121 / 140 - 1, 4))
E("l11", "screens[2].widget.options[2].why", round(80 / 100 - 1 + 121 / 80 - 1, 4))
E("l11", "screens[2].feedback.correct", round(ln(1.21), 4))
sols = [b for b in range(70, 151) if abs(b / 100 - 1 + 121 / b - 1 - 0.21) < 1e-9]
lv.claim(sols == [100, 121], "l11 s2: the simple sum is 0.21 exactly at B = 100 and B = 121")
lv.stated("l11", "screens[2].explain.text", "none equal to the true 21%", sols == [])   # content wrong (finding 30)
E("l11", "screens[3].widget.answer", round(ln(1.05), 4))
E("l11", "screens[3].widget.wrong[2].value", round(ln(52.5), 4))
P = [80.0, 81.2, 79.9, 82.3, 83.1]
lr = [ln(P[i + 1] / P[i]) for i in range(4)]
for i in range(3):
    E("l11", f"screens[4].canvas.state.markers[{i + 1}].label", round(lr[i], 4))
E("l11", "screens[4].widget.answer", round(ln(83.1 / 80), 3))
E("l11", "screens[4].explain.text", round(sum(round(x, 4) for x in lr), 4))
E("l11", "screens[4].explain.text", round(lr[3], 4))
lv.claim(sum(1 for m in lv.text("l11", "screens[4].canvas.state.markers").split("\n") if m.startswith(("+", "−", "-"))) == 4,
         "l11 s4: four daily log returns are marked, as the prose says")               # content wrong (finding 31)
E("l11", "screens[5].widget.answer", round(exp(0.08) - 1, 5))
E("l11", "screens[5].widget.wrong[1].value", round(ln(1.08), 5))
E("l11", "screens[5].explain.text", r2(200 * exp(0.08)))
E("l11", "screens[6].widget.options[3].text", -round(ln(20), 2))
E("l11", "screens[6].feedback.byKey.minus-one", round(ln(0.1), 2))
E("l11", "screens[7].prose", round(ln(1.01), 5))
E("l11", "screens[7].widget.options[0].text", round(ln(1.5), 4))
E("l11", "screens[7].widget.options[3].text", round(log(1.5), 4))
E("l11", "screens[7].feedback.byKey.approx", round(ln(0.5), 2))
E("l11", "screens[8].widget.options[0].text", round(exp(-0.03), 4))
E("l11", "screens[8].explain.text", round(100 * (1 - exp(-0.03)), 2))
cum = [0.0124, -0.0131, 0.0222, 0.0136, -0.0106]
E("l11", "screens[10].widget.answer", r2(1e6 * exp(round(sum(cum), 4))))
E("l11", "screens[10].feedback.byKey.simple", r2(1e6 * exp(0.0245) - 1024500))
E("l11", "quiz[0].widget.answer", round(ln(0.95), 4))
E("l11", "quiz[1].widget.options[1].text", round(1.02 * 0.99 * 1.03 - 1, 4))
E("l11", "quiz[1].explain.text", round(exp(0.04), 4))
E("l11", "quiz[2].widget.answer", round(ln(0.96), 4))
E("l11", "quiz[2].feedback.correct", round(ln(1.2), 4))
E("l11", "quiz[3].widget.answer", round(exp(0.25) - 1, 5))
E("l11", "quiz[3].widget.wrong[1].value", round(ln(1.25), 5))

# ---- l12 doubling time
E("l12", "screens[1].widget.points[0].target[0]", round(L2 / 0.07, 1))
for rate in (4, 2, 12, 10, 5):
    E("l12", "screens[2]", round(L2 / (rate / 100), 2))
lv.claim_text("l12", "screens[2].widget.options[2].why", "12 \\times 5.78 = 69.3", abs(12 * 5.78 - 69.3) < 0.05,
              "l12 s2: 12 x 5.78 = 69.3")                                                   # content wrong (finding 32)
E("l12", "screens[3].widget.answer", round(L2 / 0.05, 2))
E("l12", "screens[3].widget.wrong[1].value", 72 / 5)
E("l12", "screens[3].widget.wrong[2].value", round(0.6931 / 5, 4))
E("l12", "screens[4].widget.answer", round(L2 / 0.03, 1))
E("l12", "screens[4].widget.wrong[0].value", round(500 / 30, 2))
for row, r in ((0, 0.02), (1, 0.08), (2, 0.24)):
    E("l12", f"screens[5].widget.rows[{row}][2].answer", round(L2 / ln(1 + r), 2))
for pt, r in ((0, 2), (1, 8), (2, 24)):
    E("l12", f"screens[5].canvas.state.points[{pt}].y", round(72 / r - L2 / ln(1 + r / 100), 4))
lo, hi = 7.0, 8.0
for _ in range(60):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if 72 / m - L2 / ln(1 + m / 100) > 0 else (lo, m)
lv.claim(7.5 < lo < 8.2, "l12 s5: the rule of 72 error crosses zero near 8% (7.85%)")
lv.claim_text("l12", "screens[5].feedback.byKey.r0c2", "0.6931 \\div 0.0198 = 35.00", abs(0.6931 / 0.0198 - 35.00) < 0.005,
              "l12 s5 r0c2: 0.6931 / 0.0198 = 35.00")                                    # content wrong (finding 33)
E("l12", "screens[5].feedback.byKey.r2c2", round(0.6931 / 0.24, 2))
E("l12", "screens[7].widget.options[0].text", round(L2 / 0.035, 2))
E("l12", "screens[7].widget.options[1].text", round(100 / 3.5, 2))
E("l12", "screens[7].widget.options[2].text", round(72 / 3.5, 2))
E("l12", "screens[9].widget.answer", round(L2 / 0.15, 2))
E("l12", "screens[9].widget.wrong[0].value", round(0.5 / 0.15, 2))
E("l12", "screens[9].widget.wrong[1].value", 72 / 15)
E("l12", "screens[9].explain.text", round(2 * round(L2 / 0.15, 2), 2))
E("l12", "quiz[0].widget.answer", round(L2 / 0.1, 2))
E("l12", "quiz[2].widget.answer", round(L2 / 12, 5))
E("l12", "quiz[3].widget.answer", round(L2 / ln(1.01), 2))
E("l12", "quiz[3].explain.text", round(72 - round(L2 / ln(1.01), 2), 2))
lv.claim_text("l12", "quiz[1].widget.options[3].why", "added them", abs(0.5 + 0.5 + 0.5 - 1 / 6) < 1e-9,
              "l12 quiz[1]: adding three halves gives 1/6")                                 # content wrong (finding 35)

# ---- l13 log scale
E("l13", "screens[1].canvas.params.series[0].values[20]", r2(10 * 1.15 ** 20))
E("l13", "screens[1].widget.options[1].why", round(r2(10 * 1.15 ** 20) - r2(10 * 1.15 ** 15), 2))
E("l13", "screens[1].explain.text", round(1.15 ** 5, 2))
E("l13", "screens[2].explain.text", round(ln(1.15 ** 5), 2))
E("l13", "screens[5].widget.answer", r2(100 * math.sqrt(2)))
E("l13", "screens[6].widget.points[0].target[1]", round(ln(300), 4))
E("l13", "screens[6].feedback.byKey.halfway", r2(200 * math.sqrt(2)))
E("l13", "screens[6].explain.text", round(ln(1.5) / L2, 2))
E("l13", "screens[9].widget.answer", round(ln(4) / 10, 5))
E("l13", "screens[9].widget.wrong[1].value", round(4 ** 0.1 - 1, 4))
E("l13", "screens[9].widget.wrong[2].value", round(log(4) / 10, 5))
E("l13", "quiz[1].widget.answer", r2(10 * math.sqrt(10)))
E("l13", "quiz[2].widget.answer", round(ln(4) / 4, 5))
E("l13", "quiz[2].widget.wrong[1].value", round(4 ** 0.25 - 1, 5))

# ---- review-3
E("review", "items[0].widget.answer", r2(6000 * exp(0.28)))
E("review", "items[0].widget.wrong[0].value", r2(6000 * 1.035 ** 8))
E("review", "items[0].widget.wrong[1].value", r2(6000 * exp(0.035)))
E("review", "items[1].widget.answer", round(ln(40) / 3, 4))
E("review", "items[1].widget.wrong[0].value", round(ln(40 / 3), 4))
E("review", "items[2].widget.answer", round(ln(80 / 64), 4))
E("review", "items[3].widget.answer", round(L2 / 0.2, 2))
E("review", "items[5].explain.text", round(100 * (exp(0.05) - 1), 3))
E("review", "items[6].widget.answer", round(ln(0.6), 4))
E("review", "items[6].widget.wrong[1].value", round(ln(0.4), 4))
E("review", "items[7].widget.answer", round(ln(1.64) / 6, 5))
E("review", "items[7].widget.wrong[0].value", round(0.64 / 6, 5))
E("review", "items[7].widget.wrong[1].value", round(1.64 ** (1 / 6) - 1, 5))
E("review", "items[8].explain.text", round(100 * ln(3) / 10, 2))

# ---- homework-3
E("homework", "items[0].widget.answer", round(ln(1000 / 810) / 5, 5))
E("homework", "items[0].widget.wrong[0].value", round((1000 / 810 - 1) / 5, 5))
E("homework", "items[0].widget.wrong[1].value", round((1000 / 810) ** 0.2 - 1, 5))
lrs = [0.012, -0.004, 0.009, -0.015, 0.006, 0.011, -0.002, 0.008]
E("homework", "items[1].widget.answer", r2(45 * exp(sum(lrs))))
E("homework", "items[1].widget.wrong[1].value", r2(45 * exp(sum(lrs) / 8)))
lv.claim(abs(45 * 1.025 - 46.12) <= 0.004, "homework-3 items[1]: the simple slip 45 x 1.025 lies in the 46.12 band")   # content wrong (finding 44)
E("homework", "items[2].widget.answer", round(0.012 * math.sqrt(252), 5))
E("homework", "items[2].widget.wrong[1].value", round(1.012 ** 252 - 1, 4))
E("homework", "items[2].widget.wrong[2].value", round(0.012 * math.sqrt(365), 5))
E("homework", "items[3].widget.answer", round(L2 / 3, 3))
E("homework", "items[5].explain.text", round(ln(4) / 0.08, 2))
E("homework", "items[5].explain.text", round(L2 / 0.08, 2))
E("homework", "items[6].widget.answer", round(ln(0.91), 4))
E("homework", "items[7].widget.answer", r2(100 * 10 ** 0.3))
E("homework", "items[7].canvas.state.points[0].y", round(ln(100) + 0.3 * ln(10), 4))
yA, yB = ln(100 / 88) / 3, ln(1.043)
E("homework", "items[8].widget.answer", round((yA - yB) * 1e4, 1))
E("homework", "items[8].widget.wrong[0].value", round(((100 / 88) ** (1 / 3) - 1.043) * 1e4, 2))
E("homework", "items[8].widget.wrong[1].value", round((yA - 0.043) * 1e4, 1))
mr = [0.12, -0.08, 0.05, -0.10, 0.15, 0.02]
mlr = [ln(1 + r) for r in mr]
for x in mlr:
    E("homework", "items[9].model", round(x, 4))
prod = 1
for r in mr:
    prod *= 1 + r
E("homework", "items[9].model", round(prod, 4))
E("homework", "items[9].model", round(16 - 100 * (prod - 1), 2))
E("homework", "items[9].model", round(L2 / round(sum(mlr) / 6, 5), 2))
E("homework", "items[9].model", round(12 * round(sum(mlr) / 6, 5), 4))
E("homework", "items[9].model", round(exp(0.2659) - 1, 4))
lv.claim_text("homework", "items[9].model", "e^{0.1329} - 1 = 0.1422", abs(exp(0.1329) - 1 - 0.1422) < 5e-5,
              "homework-3 items[9]: e^0.1329 - 1 = 0.1422")                                  # content wrong (finding 47)
lv.claim_text("homework", "items[9].model", "\\tfrac{0.1329}{6} = 0.02216", abs(0.1329 / 6 - 0.02216) < 5e-6,
              "homework-3 items[9]: 0.1329 / 6 = 0.02216")                                   # content wrong (finding 47)

lv.check_wrongs()
lv.report()
