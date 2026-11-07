"""Second-read number checks for exp-log level 1 (Exponential growth): l1 to l4, review-1, homework-1.
Written by the second reader (docs/reviews/review-exp-log-1-3.md). Each value is computed here, then matched in the text.
Checks marked "content wrong" fail on purpose until the fix pass lands; each is a finding in the review."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("exp-log", 1)
E = lv.expect


def N(ref, path):
    return _walk(lv._file(ref)[1], path)[0]


# ---- l1 doubling
E("l1", "screens[0].feedback.correct", 2 ** 10)
E("l1", "screens[0].feedback.correct", 1 + 10 * 10)
lv.claim(9.5 < 2 ** 10 / 101 < 10.5, "l1 s0: B holds about ten times A on day 10")
for day, a, b in ((6, 61, 64), (5, 51, 32), (4, 41, 16)):
    E("l1", "screens[1].feedback", 1 + 10 * day)
    E("l1", "screens[1].feedback", 2 ** day)
lv.claim(next(n for n in range(20) if 2 ** n > 1 + 10 * n and n > 0) == 6, "l1 s1: B first ahead on day 6")
E("l1", "screens[1].widget.answer", 6)
E("l1", "screens[1].explain.text", 64 - 61)
E("l1", "screens[1].explain.text", 2 ** 8)
E("l1", "screens[1].explain.text", 1 + 10 * 8)
E("l1", "screens[2].widget.options[1].why", 2 * 6)
E("l1", "screens[2].widget.options[2].why", 6 ** 2)
E("l1", "screens[3].widget.answer", 64 * 2)
lv.claim(65.5 <= 64 + 2 <= 66.5 and 73.5 <= 64 + 10 <= 74.5, "l1 s3: slider wrong bands hold 66 and 74")
E("l1", "screens[5].widget.answer", 5 * 2 ** 4)
E("l1", "screens[5].widget.wrong[0].value", (5 * 2) ** 4)
E("l1", "screens[5].widget.wrong[1].value", 5 + 2 ** 4)
E("l1", "screens[5].widget.wrong[2].value", 5 * 2 ** 3)
lv.claim(3 <= 100 / 2 ** 5 < 3.5, "l1 s6: day 25 cover is about 3% (3.125%)")
E("l1", "screens[8].widget.lines[3].text", 32 * 32)
E("l1", "screens[9].widget.answer", 2 ** 10)
E("l1", "screens[9].widget.wrong[0].value", 2 ** 11)
E("l1", "screens[9].widget.wrong[1].value", 2 ** 9)
E("l1", "screens[9].widget.wrong[2].value", 2 * 10)
E("l1", "screens[9].explain.text", sum(2 ** k for k in range(10)))
E("l1", "quiz[0].widget.answer", 3 ** 4)
E("l1", "quiz[0].widget.wrong[0].value", 3 * 4)
E("l1", "quiz[0].widget.wrong[1].value", 4 ** 3)
E("l1", "quiz[1].widget.options[0].text", 32 * 32)
E("l1", "quiz[1].widget.options[1].text", 64)
E("l1", "quiz[1].widget.options[2].text", 32 + 10)
E("l1", "quiz[2].feedback.correct", 2 ** 20)
E("l1", "quiz[2].explain.text", 100 * 20)
first_b = next(n for n in range(1, 40) if 2 ** n > 100 * n)
lv.claim(first_b == 10, "l1 quiz[2]: plan B first beats plan A at step 10 (1,024 > 1,000)")
t_q2 = lv.text("l1", "quiz[2].explain.text")
lv.claim("passed A at step 10, when $2^{10} = 1024$ beat 1,000" in t_q2 and "step 11" not in t_q2 and first_b == 10 and 2 ** 10 == 1024 and 2 ** 9 < 100 * 9,
         "l1 quiz[2] explain says B passed A at step 10 (1,024 > 1,000; at step 9 it is 512 < 900) (finding 1)")
E("l1", "quiz[2].explain.text", 2 ** 10)
E("l1", "quiz[2].explain.text", 1000)
t_q3 = lv.text("l1", "quiz[3].prose")
lv.claim("multiplied by 7 zero times, starting from 1" in t_q3 and "£7.00" not in t_q3 and 7 ** 0 == 1,
         "l1 quiz[3] story: 7 zero times from 1 gives 7^0 = 1, so the key and the story agree (finding 2)")

# ---- l2 growth factors
E("l2", "screens[0].widget.answer", round(100 * 1.1 * 0.9, 2))
E("l2", "screens[0].explain.text", 99)
E("l2", "screens[2].widget.answer", 1.05)
E("l2", "screens[2].feedback.byKey.five", (5 - 1) * 100)
E("l2", "screens[3].widget.answer", 0.85)
E("l2", "screens[4].widget.answer", round(2000 * 0.8 ** 3, 2))
E("l2", "screens[4].widget.wrong[0].value", 2000 - 3 * 400)
E("l2", "screens[4].widget.wrong[1].value", round(2000 * 0.8 ** 2, 2))
E("l2", "screens[4].widget.wrong[2].value", round(2000 * 0.2 ** 3, 6))
for loss in (400, 320, 256):
    E("l2", "screens[4].explain.text", loss)
lv.claim([round(2000 * 0.8 ** k - 2000 * 0.8 ** (k + 1), 6) for k in range(3)] == [400, 320, 256], "l2 s4: losses 400, 320, 256")
E("l2", "screens[5].feedback.byKey.hundred", (100 - 1) * 100)
E("l2", "screens[6].widget.options[2].text", round(100 * 0.9 ** 10, 2))
E("l2", "screens[6].feedback.byKey.zero", round(0.9 ** 10, 3))
E("l2", "screens[6].explain.text", round(0.9 ** 10, 4))
lv.claim(100 * 0.1 ** 10 < 0.01, "l2 s6: 0.1^10 of £100 is less than 1p")
v20 = 1000 * 1.05 ** 20
v10 = 1000 * 1.05 ** 10
E("l2", "screens[9].widget.answer", round(v20, 1))
E("l2", "screens[9].widget.wrong[0].value", 2000)
E("l2", "screens[9].widget.wrong[1].value", round(1000 * 1.05 * 20))
E("l2", "screens[9].widget.wrong[2].value", round(2 * round(v10, 2), 2))   # doubles the shown year-10 value
E("l2", "screens[9].widget.wrong[3].value", round(1000 + 2 * (round(v10, 2) - 1000), 2))
E("l2", "screens[9].hints[1].text", round(v10, 2))
E("l2", "screens[9].hints[2].text", round(1.05 ** 20, 4))
E("l2", "screens[9].feedback.byKey.double10", round(1.05 ** 10, 4))
E("l2", "screens[9].feedback.byKey.gain2", round(round(v20, 2) - round(v10, 2), 2))   # from the shown values
E("l2", "screens[9].explain.text", round(1.05 ** 20, 3))
E("l2", "quiz[1].widget.answer", round(20000 * 0.85 ** 2, 2))
E("l2", "quiz[1].widget.wrong[0].value", 14000)
E("l2", "quiz[1].widget.wrong[1].value", 17000)
E("l2", "quiz[1].explain.text", round(17000 * 0.15, 2))
lv.claim(1.25 * 0.8 == 1.0, "l2 quiz[2]: +25% then -20% multiply to exactly 1 (finding 6)")
E("l2", "quiz[2].feedback.correct", 1.25)
E("l2", "quiz[2].feedback.correct", 0.8)
E("l2", "quiz[2].feedback.correct", 1)
E("l2", "quiz[2].widget.options[1].why", 1.25 * 0.8)
E("l2", "quiz[2].widget.options[2].why", 1.25 * 0.8)
E("l2", "quiz[2].explain.text", 1.25 * 0.8)
E("l2", "quiz[2].prose", 25)
E("l2", "quiz[2].prose", 20)
lv.claim(next(o for o in N("l2", "quiz[2].widget.options") if o.get("correct"))["id"] == "flat",
         "l2 quiz[2]: the correct option is 'back where it started'")

# ---- l3 strange powers
E("l3", "screens[0].widget.answer", 0.5)
E("l3", "screens[1].widget.answer", 2 ** -3)
E("l3", "screens[1].widget.wrong[1].value", -6)
E("l3", "screens[2].explain.text", 5 ** -2)
E("l3", "screens[3].widget.answer", 9 ** 0.5)
E("l3", "screens[3].widget.wrong[0].value", 4.5)
E("l3", "screens[3].widget.wrong[1].value", (1 + 9) / 2)
E("l3", "screens[3].explain.text", round(9 ** 1.5))
E("l3", "screens[4].widget.answer", round(8 ** (1 / 3)))
E("l3", "screens[4].widget.wrong[0].value", round(8 / 3, 4))
E("l3", "screens[4].widget.wrong[1].value", round(math.sqrt(8), 4))
E("l3", "screens[4].explain.text", round(8 ** (2 / 3)))
E("l3", "screens[5].widget.answer", 16 ** -0.5)
E("l3", "screens[5].widget.wrong[2].value", 16 * -0.5)
E("l3", "screens[6].widget.options[2].text", round(math.sqrt(2), 3))
E("l3", "screens[6].feedback.byKey.avg", 1.5 * 1.5)
E("l3", "screens[7].widget.options[0].text", round(27 ** (2 / 3)))
E("l3", "screens[7].widget.options[1].text", 27 * 2 / 3)
E("l3", "screens[7].explain.text", 9 ** 3)
lv.claim(9 ** 3 == 27 ** 2, "l3 s7: 9^3 = 27^2")
E("l3", "screens[9].widget.answer", round(math.sqrt(12100 / 10000), 4))
E("l3", "screens[9].widget.wrong[1].value", 1.21 / 2)
E("l3", "screens[9].feedback.byKey.halved", round(1.105 ** 2, 3))
E("l3", "screens[9].explain.text", 11000)
t_s8 = lv.text("l3", "screens[8].explain.text")
lv.claim("Nothing was assumed" not in t_s8 and "not $-\\sqrt{a}$" in t_s8 and (-3) ** 2 == 3 ** 2,
         "l3 s8 explain admits the positive-root step: (-3)^2 = 3^2, so the law alone gives only b^2 = a (finding 7)")
E("l3", "quiz[0].widget.answer", 0.01)
E("l3", "quiz[1].widget.answer", 5)
E("l3", "quiz[2].explain.text", 2)
E("l3", "quiz[3].widget.answer", round(8 ** (2 / 3)))
E("l3", "quiz[3].widget.wrong[0].value", round(8 * 2 / 3, 4))

# ---- l4 exponential curves
E("l4", "screens[2].widget.answer", 0.5 ** -2)
E("l4", "screens[3].feedback.byKey.same", 0.5 ** 3)
E("l4", "screens[4].widget.wrong[0].value", 8 * 4)
E("l4", "screens[4].widget.wrong[1].value", 24)
E("l4", "screens[5].widget.accept", round(10000 * 0.9 ** 6))
E("l4", "screens[5].widget.accept", round(10000 * 0.9 ** 7))
E("l4", "screens[5].hints[2].text", round(0.9 ** 6, 3))
E("l4", "screens[5].hints[2].text", round(0.9 ** 7, 3))
lv.claim(next(n for n in range(30) if 0.9 ** n < 0.5) == 7, "l4 s5: first day under half is 7")
E("l4", "screens[5].explain.text", round(math.log(0.5) / math.log(0.9), 1))
f = lambda x: 2 ** x - 100 * x
lo, hi = 9.0, 10.0
for _ in range(60):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if f(m) < 0 else (lo, m)
lv.claim(9.9 < lo < 10, "l4 s6: 2^x passes 100x just before x = 10 (9.96)")
E("l4", "screens[6].hints[2].text", 2 ** 9)
E("l4", "screens[6].hints[2].text", 2 ** 10)
E("l4", "screens[6].widget.options[2].why", 2 ** 7)
lv.claim(3 < math.log(0.5) / math.log(0.8) < 3.2, "l4 s7: half-life of 0.8^x a little over 3 steps (3.11)")
E("l4", "screens[7].explain.text", round(0.8 ** 3, 3))
a60 = 10000 * 1.01 ** 60
E("l4", "screens[9].widget.answer", round(a60, 2))
E("l4", "screens[9].widget.wrong[0].value", 10000 + 100 * 60)
E("l4", "screens[9].widget.wrong[1].value", round(10000 * 1.12 ** 5, 2))
E("l4", "screens[9].feedback.byKey.yearly", round(1.01 ** 12, 4))
E("l4", "screens[9].hints[2].text", round(1.01 ** 60, 4))
E("l4", "screens[9].explain.text", round(a60 - 16000, 2))
lv.claim(10000 * 1.01 ** 120 - (10000 + 100 * 120) > 11000, "l4 s9: A leads by over £11,000 after 10 years")
E("l4", "screens[9].widget.wrong[2].value", round(10000 * 1.01 * 60))
E("l4", "screens[9].feedback.byKey.times", round(10000 * 1.01 * 60))
lv.claim(N("l4", "screens[9].widget.wrong[2].value") == 606000 == round(10000 * 1.01 * 60) and "added it on" not in lv.text("l4", "screens[9].feedback.byKey.times"),
         "l4 s9 wrong times: 606000 is 10000 x 1.01 x 60, the slip the line names (finding 9)")
E("l4", "screens[10].prose", round(1.08 ** 9, 3))
E("l4", "screens[10].widget.answer", round(1000 * 1.06 ** 12, 1))
E("l4", "screens[10].widget.wrong[0].value", 1000 + 60 * 12)
E("l4", "screens[10].feedback.byKey.simple", round(100 / 6, 1))
E("l4", "screens[10].hints[2].text", round(1.06 ** 12, 4))
E("l4", "screens[10].explain.text", round(1000 * 1.06 ** 12, 2))
E("l4", "screens[10].explain.text", round(1.06 ** 12, 3))
lv.claim(abs(1000 * 1.06 ** 12 - 2012.20) < 0.005 and 2.0115 < 1.06 ** 12 < 2.0125, "l4 s10: £1,000.00 at 6% is £2,012.20 after 12 years (finding 10)")
lv.claim(next(d for d in range(1, 30) if 0.9 ** d < 0.5) == 7 and abs(math.log(0.5) / math.log(0.9) - 6.58) < 0.005,
         "l4 s5: half-life 6.58 days, so day 7 is the first whole day under half (finding 11)")
E("l4", "screens[5].explain.text", 7)
g = lambda x: x * math.log(1.01) - math.log(1000 * x)
lv.claim(next(n for n in range(2, 5000) if 1.01 ** n > 1000 * n) == 1424, "l4 quiz[3]: 1.01^x first beats 1000x at x = 1,424")
E("l4", "quiz[3].explain.text", 1424)
E("l4", "quiz[2].widget.answer", 8000 * 0.5 ** 3)
E("l4", "quiz[2].widget.wrong[0].value", round(8000 / 3))

# ---- review-1
E("review", "items[0].widget.answer", 2 ** 8)
E("review", "items[0].widget.wrong[0].value", 16)
E("review", "items[0].widget.wrong[1].value", 8 ** 2)
E("review", "items[0].widget.wrong[2].value", 2 ** 7)
E("review", "items[1].widget.answer", 0.93)
E("review", "items[2].widget.answer", 0.25)
E("review", "items[3].widget.answer", 0.25 ** -1)
b3 = 5000 * 1.04 ** 3
E("review", "items[4].widget.answer", round(b3 - 5000, 2))
E("review", "items[4].widget.wrong[1].value", round(b3, 2))
E("review", "items[4].feedback.byKey.simple", 200)
E("review", "items[4].feedback.byKey.two", round(b3, 2))
lv.claim(abs((b3 - 5000) - 624.32) < 0.005, "review-1 items[4]: interest after 3 years is £624.32 (finding 14)")
E("review", "items[4].widget.wrong[0].value", 3 * 200)
E("review", "items[4].widget.wrong[2].value", round(5000 * 1.04 ** 2 - 5000, 2))
E("review", "items[4].explain.text", round(1.04 ** 3, 6))
E("review", "items[4].explain.text", round(b3 - 5600, 2))
E("review", "items[4].explain.text", round(b3 - 5000, 2))
E("review", "items[4].explain.text", 600)
E("review", "items[5].widget.answer", round(32 ** 0.6))
E("review", "items[5].widget.wrong[0].value", 32 * 3 / 5)
E("review", "items[6].widget.wrong[0].value", 6 * 60 / 20)
E("review", "items[7].feedback.correct", 1000)
E("review", "items[7].explain.text", 2 ** 20)
E("review", "items[8].widget.answer", next(n for n in range(100) if 0.98 ** n < 0.5))
E("review", "items[8].widget.accept", round(100 * 0.98 ** 34, 1))
E("review", "items[8].widget.accept", round(100 * 0.98 ** 35, 1))
E("review", "items[8].widget.wrong[0].value", 25)
E("review", "items[9].widget.answer", round(27 * 1.5 ** -3, 2))
E("review", "items[9].widget.wrong[0].value", 27 / (1.5 * 3))
E("review", "items[9].widget.wrong[1].value", math.floor(27 * 1.5 ** 3 * 100 + 0.5) / 100)   # 91.125 rounds half up
E("review", "items[9].widget.wrong[2].value", 27 * 0.5 ** 3)
E("review", "items[9].feedback.byKey.subtract", 27 * 0.5 ** 3)
lv.claim(N("review", "items[9].widget.wrong[2].value") == 3.375 == 27 * 0.5 ** 3 and abs((1 - 1 / 1.5) - 1 / 3) < 1e-12,
         "review-1 items[9] wrong subtract 3.375: three 50% falls (finding 13)")

# ---- homework-1
E("homework", "items[0].explain.text", 2500 * 1.06)
E("homework", "items[1].widget.answer", round(1.09 ** 8, 2))
E("homework", "items[1].widget.wrong[0].value", 1 + 8 * 0.09)
E("homework", "items[1].explain.text", round(1.09 ** 8, 4))
E("homework", "items[2].widget.answer", round(1.1268 ** (1 / 12) - 1, 4))
E("homework", "items[2].widget.wrong[0].value", round(0.1268 / 12, 6))
E("homework", "items[3].widget.accept", round(100 * 0.8 ** 3, 1))
E("homework", "items[3].widget.accept", round(100 * 0.8 ** 4, 2))
E("homework", "items[3].explain.text", 0.5 / 0.2)
A = lambda n: 10000 * 1.01 ** n
B = lambda n: 10000 + 150 * n
E("homework", "items[6].widget.answer", next(n for n in range(2, 300) if A(n) > B(n)))
for n in (77, 78):
    E("homework", "items[6].explain.text", round(A(n), 2))
    E("homework", "items[6].explain.text", B(n))
E("homework", "items[6].feedback.byKey.before", round(B(77) - A(77), 2))
E("homework", "items[6].feedback.byKey.gain", round(B(41) - A(41), 2))
lv.claim(next(n for n in range(1, 200) if A(n) > 15000) == 41, "homework-1 items[6]: balance passes £15,000 in month 41")
E("homework", "items[5].feedback.correct", 2 ** 30)
E("homework", "items[7].model", round(5000 * 1.05 ** 10, 2))
E("homework", "items[7].model", round(5000 * 1.05 ** 20, 2))
E("homework", "items[7].model", round(5000 * 1.05 ** 14, 2))
E("homework", "items[7].model", round(5000 * 1.05 ** 15, 2))
E("homework", "items[7].model", round(5000 * 1.05 ** 20 - 10000, 2))
t_m = lv.text("homework", "items[7].model")
lv.claim("5000 \\times 2.6532977 = 13266.49" in t_m and abs(5000 * 2.6532977 - 13266.49) < 0.005 and abs(1.05 ** 20 - 2.6532977) < 5e-8,
         "homework-1 items[7] model: printed factor 2.6532977 gives 13266.49 (finding 15)")
lv.claim("5000 \\times 1.6288946 = 8144.47" in t_m and abs(5000 * 1.6288946 - 8144.47) < 0.005 and abs(1.05 ** 10 - 1.6288946) < 5e-8,
         "homework-1 items[7] model: printed factor 1.6288946 gives 8144.47 (finding 15)")
lv.claim("multiplying law" not in t_m and "index laws" in t_m, "homework-1 items[7] model (e) says index laws (finding 8)")

lv.check_wrongs()
lv.report()
