"""Second-read number checks for exp-log level 3 (The natural base): l9 to l13, review-3, homework-3.
Written by the second reader (docs/reviews/review-exp-log-1-3.md). Fix pass applied: every check now asserts the corrected value or wording."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("exp-log", 3)
E = lv.expect


def N(ref, path):
    return _walk(lv._file(ref)[1], path)[0]

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
t_q3 = lv.text("l9", "quiz[3].explain.text")
lv.claim(exp(0.079) > 1.08 and 1.02 ** 4 > exp(0.079) and "It is not a rule: 7.9% continuous beats 8% paid once" in t_q3 and "$1.0822 > 1.08$" in t_q3,
         "l9 quiz[3]: the higher rate wins here, but 7.9% continuous (1.0822) beats 8% paid once (1.08), so it is not a rule (finding 24)")
t_s6 = lv.text("l9", "screens[6].explain.text")
lv.claim("matters more than how often" not in t_s6 and "Compare the yearly factors" in t_s6 and exp(0.079) > 1.08,
         "l9 s6: the 'rate matters more' rule is gone: 7.9% continuous beats 8% yearly (finding 24)")
E("l9", "screens[6].explain.text", round(exp(0.06), 4))
lv.claim("AER (annual equivalent rate)" in lv.text("l9", "screens[9].prose") and abs(exp(0.05) - 1 - 0.05127) < 1e-5,
         "l9 s9: the once-a-year equivalent of 5.00% continuous (5.127%) is named the AER (finding 25)")

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
lv.claim(round(100 / 92.31, 5) == 1.08331 and "1.08333" not in lv.text("l10", "screens[10]"), "l10 s10: 100 / 92.31 = 1.08331 to five places and 1.08333 is gone (finding 29)")
E("l10", "screens[10].hints[1].text", 1.08331)
lv.claim("\\sqrt{1.08331}" in lv.text("l10", "screens[10].feedback.byKey.yearly"), "l10 s10 byKey yearly uses 1.08331 (finding 29)")
E("l10", "screens[10].explain.text", 1.08331)
lv.claim(round(ln(1.08331), 5) == 0.08002 and round(math.sqrt(1.08331) - 1, 5) == 0.04082, "l10 s10: ln 1.08331 = 0.08002 and sqrt(1.08331) - 1 = 4.082% (finding 29)")
lv.claim("$\\ln x = \\log_e x$" in lv.text("l10", "screens[3].prose") and "`math.log` is ln" in lv.text("l10", "screens[3].prose") and round(ln(5), 3) == 1.609,
         "l10 s3: ln x = log_e x, ln 5 = 1.609, Python's math.log is ln (finding 26)")
lv.claim("log laws from l6" in lv.text("l10", "screens[5].prose") and "from base 10" not in lv.text("l10", "screens[5].prose") and round(L2, 4) == 0.6931 and round(ln(3), 4) == 1.0986,
         "l10 s5: the log laws are cited from l6, not from base 10 (finding 28)")
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
lv.claim("matching the true 21% only at £100 or £121" in lv.text("l11", "screens[2].explain.text") and "none equal" not in lv.text("l11", "screens[2].explain.text") and sols == [100, 121],
         "l11 s2 explain: the simple sum matches 21% only at B = 100 or 121 (finding 30)")
lv.claim(all(abs(b ** 2 - 221 * b + 12100) < 1e-9 for b in (100, 121)), "l11 s2: B^2 - 221B + 12100 = (B - 100)(B - 121) (finding 30)")
E("l11", "screens[3].widget.answer", round(ln(1.05), 4))
E("l11", "screens[3].widget.wrong[2].value", round(ln(52.5), 4))
P = [80.0, 81.2, 79.9, 82.3, 83.1]
lr = [ln(P[i + 1] / P[i]) for i in range(4)]
for i in range(3):
    E("l11", f"screens[4].canvas.state.markers[{i + 1}].label", round(lr[i], 4))
E("l11", "screens[4].widget.answer", round(ln(83.1 / 80), 3))
E("l11", "screens[4].explain.text", round(sum(round(x, 4) for x in lr), 4))
E("l11", "screens[4].explain.text", round(lr[3], 4))
lv.claim(sum(1 for m in lv.text("l11", "screens[4].canvas.state.markers").split("\n") if m.startswith(("+", "−", "-"))) == 3
         and "The first three daily log returns are marked" in lv.text("l11", "screens[4].prose") and "four" not in lv.text("l11", "screens[4].prose"),
         "l11 s4: three daily log returns are marked and the prose says the first three (finding 31)")
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
for rate in (4, 2, 10, 5):
    E("l12", "screens[2]", round(L2 / (rate / 100), 2))
E("l12", "screens[2]", round(L2 / 0.12, 3))
lv.claim("12 \\times 5.776 = 69.3" in lv.text("l12", "screens[2].widget.options[2].why") and abs(12 * round(L2 / 0.12, 3) - 69.3) < 0.05 and abs(2 * round(L2 / 0.02, 2) - 69.3) < 0.05,
         "l12 s2: 12 x 5.776 = 69.3 and 2 x 34.66 = 69.3 (finding 32)")
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
lv.claim("$\\ln 1.02 = 0.019803$, and $0.69315 \\div 0.019803 = 35.00$" in lv.text("l12", "screens[5].feedback.byKey.r0c2") and round(ln(1.02), 6) == 0.019803 and round(0.69315 / 0.019803, 2) == 35.00,
         "l12 s5 r0c2: ln 1.02 = 0.019803 and 0.69315 / 0.019803 = 35.00 (finding 33)")
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
lv.claim("You put $2 \\times 3$ underneath" in lv.text("l12", "quiz[1].widget.options[3].why") and "added them" not in lv.text("l12", "quiz[1].widget.options[3].why") and 1 / (2 * 3) == 1 / 6 and 0.5 ** 3 == 1 / 8,
         "l12 quiz[1] sixth: 1/(2 x 3) = 1/6 and three halvings give 1/8 (finding 35)")
E("l12", "quiz[1].widget.options[3].why", 1 / 8)
for i_, v_ in ((2, 0.1386), (2, 0.1386)):
    lv.claim(abs(round(L2 / 5, 4) - N("l12", "screens[3].widget.wrong[2].value")) < 1e-9 and abs(round(L2 / 5, 2) - 0.14) < 1e-9 and abs(0.14 - N("l12", "screens[3].widget.wrong[2].value")) <= N("l12", "screens[3].widget.wrong[2].tol")["abs"],
             "l12 s3 wrong pct: 0.1386 typed as 0.14 is inside its band (finding 34)")
    break
lv.claim(abs(0.05 - N("l12", "screens[9].widget.wrong[2].value")) <= N("l12", "screens[9].widget.wrong[2].tol")["abs"] and round(L2 / 15, 4) == 0.0462,
         "l12 s9 wrong pct: 0.0462 typed as 0.05 is inside its band (finding 34)")
lv.claim("$\\tfrac{\\ln 2}{0.1} = 6.93$" in lv.text("l12", "quiz[0].feedback.byKey") and round(L2 / 0.1, 2) == 6.93 and "exactly" not in lv.text("l12", "quiz[0].feedback.byKey"),
         "l12 quiz[0] 72 line: ln 2 / 0.1 = 6.93, not 'exactly 69.3 / 10' (finding 36)")
lv.claim("At 1% it runs more than 2 years long" in lv.text("l12", "quiz[3].feedback.byKey") and 72 - L2 / ln(1.01) > 2 and abs(72 / 2 - L2 / ln(1.02)) < 1.01 and 36 - L2 / ln(1.02) < 1.01,
         "l12 quiz[3] 72 line: the rule runs 2.3 years long at 1% (finding 37)")
lv.claim(abs((1 - exp(-0.15)) - 0.139) < 5e-4 and abs((1 - exp(-0.2)) - 0.181) < 5e-4 and "15% of what is left" not in lv.text("l12", "screens[9].feedback.byKey.linear") and "20% of what is left" not in lv.text("review", "items[3].feedback.byKey.linear"),
         "l12 s9 and review-3 items[3] linear lines: a continuous rate k sells 13.9% (k = 0.15) and loses 18.1% (k = 0.2) a day, so 'of what is left' is gone (finding 38)")

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
dA, dB = 6000 * exp(0.28), 6000 * 1.035 ** 8
lv.claim(abs(dA - dB - 37.92) < 0.005 and abs(round(dA, 2) - round(dB, 2) - 37.93) < 1e-9, "review-3 items[0]: A holds £37.92 more than B (37.93 from rounded values) (finding 41)")
E("review", "items[0].widget.answer", round(dA - dB, 2))
E("review", "items[0].widget.wrong[0].value", r2(dA))
E("review", "items[0].widget.wrong[1].value", r2(dA - 6000 * (1 + 0.035 * 8)))
E("review", "items[0].feedback.correct", r2(dA))
E("review", "items[0].feedback.correct", r2(dB))
E("review", "items[0].feedback.byKey.simple", 6000 * (1 + 0.035 * 8))
E("review", "items[0].explain.text", round(exp(0.28), 5))
E("review", "items[0].explain.text", round(1.035 ** 8, 5))
E("review", "items[0].explain.text", round(dA - dB, 2))
E("review", "items[1].widget.answer", round(ln(40) / 3, 4))
E("review", "items[1].widget.wrong[0].value", round(ln(40 / 3), 4))
E("review", "items[2].widget.answer", round(ln(80 / 64), 4))
E("review", "items[3].widget.answer", round(L2 / 0.2, 2))
lv.claim(20 * 16 ** 0.25 == 40 and 16 ** 0.25 == 2 and 20 + (320 - 20) / 4 == 95, "review-3 items[4]: a quarter of the way up from £20 to £320 is 20 x 16^(1/4) = £40.00 (the pounds slip is 95) (finding 42)")
E("review", "items[4].widget.answer", 20 * 16 ** 0.25)
E("review", "items[4].widget.wrong[0].value", 20 + (320 - 20) / 4)
E("review", "items[4].feedback.byKey.mid", 20 + (320 - 20) / 4)
E("review", "items[4].explain.text", 16)
E("review", "items[4].prose", 320)
E("review", "items[5].explain.text", round(100 * (exp(0.05) - 1), 3))
E("review", "items[6].widget.answer", round(ln(0.6), 4))
E("review", "items[6].widget.wrong[1].value", round(ln(0.4), 4))
E("review", "items[7].widget.answer", round(ln(1.64) / 6, 5))
E("review", "items[7].widget.wrong[0].value", round(0.64 / 6, 5))
E("review", "items[7].widget.wrong[1].value", round(1.64 ** (1 / 6) - 1, 5))
E("review", "items[8].explain.text", round(100 * ln(3) / 10, 2))

# ---- homework-3
zc = 1000 * exp(-0.042 * 5)
lv.claim(abs(zc - 810.58) < 0.005 and abs(1000 / 1.042 ** 5 - 814.07) < 0.005 and abs(1000 / 1.21 - 826.45) < 0.005 and abs(1000 * exp(-0.042) - 958.87) < 0.005 and abs(0.042 * 5 - 0.21) < 1e-12,
         "homework-3 items[0]: 1000 e^(-0.21) = £810.58; slips 814.07 (yearly), 826.45 (simple), 958.87 (one year) (finding 48)")
E("homework", "items[0].widget.answer", round(zc, 2))
E("homework", "items[0].widget.wrong[0].value", round(1000 / 1.042 ** 5, 2))
E("homework", "items[0].widget.wrong[1].value", round(1000 / 1.21, 2))
E("homework", "items[0].widget.wrong[2].value", round(1000 * exp(-0.042), 2))
E("homework", "items[0].feedback.correct", round(zc, 2))
E("homework", "items[0].explain.text", round(zc, 2))
lrs = [0.012, -0.004, 0.009, -0.015, 0.006, 0.011, -0.002, 0.008]
E("homework", "items[1].widget.answer", r2(45 * exp(sum(lrs))))
E("homework", "items[1].widget.wrong[1].value", r2(45 * exp(sum(lrs) / 8)))
hs = N("homework", "items[1].widget.wrong[0]")
lv.claim(hs["value"] == 46.125 and hs["tol"]["abs"] == 0.006 and all(abs(45 * 1.025 - x) <= hs["tol"]["abs"] + 1e-9 for x in (46.12, 46.125, 46.13)),
         "homework-3 items[1]: the simple slip 45 x 1.025 = 46.125 (typed 46.12, 46.125 or 46.13) lies in its band (finding 44)")
E("homework", "items[2].widget.answer", round(0.012 * math.sqrt(252), 5))
lv.claim("a standard deviation is the square root of its variance" in lv.text("homework", "items[2].prose") and N("homework", "items[2].widget")["over100"] is True
         and N("homework", "items[2].widget.wrong[0].value") == 3.024 and N("homework", "items[2].widget.wrong[1].value") == 19.2064,
         "homework-3 items[2]: the prose defines the standard deviation and the over-100% slips (302.4%, 1,920.6%) are flagged (finding 45)")
E("homework", "items[2].widget.wrong[1].value", round(1.012 ** 252 - 1, 4))
E("homework", "items[2].widget.wrong[2].value", round(0.012 * math.sqrt(365), 5))
E("homework", "items[3].widget.answer", round(L2 / 3, 3))
E("homework", "items[5].explain.text", round(ln(4) / 0.08, 2))
lv.claim("a decimal such as 17.33 is not exact" in lv.text("homework", "items[5].feedback.generic") and round(ln(4) / 0.08, 2) == 17.33
         and N("homework", "items[5].widget.wrong")[2] == {"id": "pct", "tex": "\\frac{\\ln 4}{8}"} and "pct" in N("homework", "items[5].feedback.byKey"),
         "homework-3 items[5]: generic line warns against decimals; the percent slip ln 4 / 8 has its own wrong entry (finding 46)")
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
t_m9 = lv.text("homework", "items[9].model")
S9 = sum(mlr)
lv.claim("or 0.13294 before rounding" in t_m9 and round(S9, 5) == 0.13294 and "e^{0.13294} - 1 = 0.1422" in t_m9 and round(exp(round(S9, 5)) - 1, 4) == 0.1422,
         "homework-3 items[9] (b): the sum is 0.13294 unrounded and e^0.13294 - 1 = 0.1422 (finding 47)")
lv.claim("\\tfrac{0.13294}{6} = 0.02216" in t_m9 and round(S9 / 6, 5) == 0.02216 and "{0.1329}{6}" not in t_m9,
         "homework-3 items[9] (d): 0.13294 / 6 = 0.02216 (finding 47)")
lv.claim(round(exp(0.1329) - 1, 4) == 0.1421, "homework-3 items[9] (b): from the rounded 0.1329 the simple return is 0.1421, which is why the text carries the unrounded sum 0.13294 (finding 47)")

lv.check_wrongs()
lv.report()
