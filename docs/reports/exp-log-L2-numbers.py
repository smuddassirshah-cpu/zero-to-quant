"""Second-read number checks for exp-log level 2 (Logarithms): l5 to l8, review-2, homework-2.
Written by the second reader (docs/reviews/review-exp-log-1-3.md). Fix pass applied: every check now asserts the corrected value or wording."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("exp-log", 2)
E = lv.expect


def N(ref, path):
    return _walk(lv._file(ref)[1], path)[0]

log, ln, l2 = math.log10, math.log, math.log2


def r2(x):  # round half up to 2 places, as money is shown
    return math.floor(x * 100 + 0.5) / 100


# ---- l5 how many doublings
E("l5", "screens[0].widget.answer", round(l2(1024)))
E("l5", "screens[0].widget.wrong[2].value", 1024 / 2)
E("l5", "screens[1].explain.text", round(l2(100), 2))
lv.claim(2 ** 6 < 100 < 2 ** 7, "l5 s1: 64 < 100 < 128")
E("l5", "screens[1].widget.options[1].why", 2 ** 7)
E("l5", "screens[2].widget.answer", round(l2(32)))
E("l5", "screens[2].widget.wrong[0].value", 32 / 2)
E("l5", "screens[4].widget.options[2].why", round(2 ** (1 / 3), 2))
E("l5", "screens[5].explain.text", round(l2(5000), 2))
lv.claim(2 ** 12 < 5000 < 2 ** 13, "l5 s5: 4096 < 5000 < 8192")
lv.claim(2 ** 32 > 4e9, "l5 s6: 2^32 is over four billion")
E("l5", "screens[7].widget.options[1].why", 3 ** 5)
E("l5", "screens[7].widget.options[3].why", 125 / 5)
E("l5", "screens[9].widget.answer", next(n for n in range(30) if 1000 / 2 ** n < 10))
E("l5", "screens[9].feedback.correct", r2(1000 / 2 ** 7))
E("l5", "screens[9].feedback.byKey.equal", r2(1000 / 2 ** 6))
E("l5", "screens[9].explain.text", round(l2(100), 2))
E("l5", "quiz[0].widget.answer", round(math.log(81, 3)))
E("l5", "quiz[2].explain.text", round(l2(50), 2))
E("l5", "quiz[3].widget.options[3].why", round(4 ** 0.25, 2))
lv.claim(abs(math.log(2, 4) * l2(4) - 1) < 1e-12 and math.log(2, 4) == 0.5 and l2(4) == 2 and "turns the log into its reciprocal" in lv.text("l5", "quiz[3].explain.text")
         and "turns 2 into" not in lv.text("l5", "quiz[3].explain.text"), "l5 quiz[3]: log_4 2 = 1/2 and log_2 4 = 2 are reciprocal logs (finding 16)")

# ---- l6 products into sums
E("l6", "screens[0].feedback.correct", 32 * 128)
lv.claim(2 ** 5 * 2 ** 7 == 2 ** 12, "l6 s0: row 5 plus row 7 is row 12")
lv.claim(256 == 128 * 2 and 2 ** (7 - 5) == 4 and "256 is $128 \\times 2$" in lv.text("l6", "screens[0].feedback.byKey.r8c1") and "2^{7 - 5}" in lv.text("l6", "screens[0].feedback.byKey.r2c1"),
         "l6 s0: 256 is one doubling of 128 (r8c1); 4 is 2^(7-5), the subtraction slip (r2c1) (finding 17)")
E("l6", "screens[0].feedback.byKey.r8c1", 128 * 2)
E("l6", "screens[0].feedback.byKey.r2c1", 2 ** (7 - 5))
E("l6", "screens[1].widget.options[1].why", 128 - 16)
E("l6", "screens[2].widget.answer", 5 + 3)
E("l6", "screens[2].widget.wrong[0].value", 5 * 3)
E("l6", "screens[2].widget.wrong[1].value", 32 + 8)
E("l6", "screens[2].widget.wrong[3].value", 2 ** 8)
E("l6", "screens[3].widget.answer", 8 - 3)
E("l6", "screens[3].widget.wrong[2].value", round(8 / 3, 3))
E("l6", "screens[4].widget.answer", 4 * 3)
E("l6", "screens[4].widget.wrong[1].value", 3 ** 4)
E("l6", "screens[4].widget.wrong[2].value", 8 ** 4)
E("l6", "screens[5].prose", round(l2(3), 3))
E("l6", "screens[5].widget.answer", round(l2(12), 3))
E("l6", "screens[5].widget.wrong[0].value", round(2 * round(l2(3), 3), 2))
E("l6", "screens[5].widget.wrong[1].value", round(4 * round(l2(3), 3), 2))
lv.claim(abs(4 * 1.585 - l2(81)) < 0.01, "l6 s5: 4 x 1.585 is log2 81")
E("l6", "screens[5].explain.text", round(2 ** 3.585, 1))
E("l6", "screens[10].canvas.params.rows[0][2]", round(l2(1.5), 4), fmt="{:.4f}")
E("l6", "screens[10].canvas.params.rows[1][2]", round(-l2(1 / 0.8), 4))
E("l6", "screens[10].canvas.params.rows[2][2]", round(l2(1.25), 4))
E("l6", "screens[10].widget.answer", round(l2(1.5 * 0.8 * 1.25), 3))
E("l6", "screens[10].widget.wrong[0].value", round(0.5850 + 0.3219 + 0.3219, 4))
E("l6", "screens[10].widget.wrong[1].value", round(0.5850 * -0.3219 * 0.3219, 4))
E("l6", "screens[10].widget.wrong[2].value", 1.5 + 0.8 + 1.25)
E("l6", "screens[10].explain.text", 20000 * 1.5)
E("l6", "quiz[0].widget.answer", round(l2(40), 3))
E("l6", "quiz[0].widget.wrong[0].value", round(3 * 2.322, 3))
E("l6", "quiz[1].explain.text", 243 / 9)
# quiz[3]: the test values x = 8, y = 4 break every wrong statement, the power one at k = 2 included
lv.claim("$x = 8$ and $y = 4$" in lv.text("l6", "quiz[3].feedback.generic") and "$x = 4$" not in lv.text("l6", "quiz[3].feedback.generic"),
         "l6 quiz[3]: the hint names x = 8 and y = 4 (finding 18)")
lv.claim(l2(8 * 4) == 5 == l2(8) + l2(4) and l2(8 + 4) != 5 and l2(8 / 4) != l2(8) / l2(4) and l2(8 ** 2) != l2(8) ** 2,
         "l6 quiz[3]: with b = 2, x = 8, y = 4 only the product law holds (finding 18)")
E("l6", "quiz[3].explain.text", 6)
E("l6", "quiz[3].explain.text", 9)
E("l6", "quiz[3].explain.text", round(l2(12), 3))
E("l6", "quiz[3].explain.text", 1.5)

# ---- l7 changing base
E("l7", "screens[0].widget.answer", round(log(100000 / 100)))
E("l7", "screens[0].widget.wrong[1].value", 100000 - 100)
E("l7", "screens[1].widget.options[1].why", round(10 ** 0.11, 2))
E("l7", "screens[1].widget.options[2].why", round(10 ** 0.2, 2))
E("l7", "screens[1].widget.options[3].why", round(10 ** 0.5, 2))
E("l7", "screens[2].widget.answer", round(log(20), 3))
E("l7", "screens[2].widget.wrong[2].value", round(log(4), 3))
E("l7", "screens[2].explain.text", round(log(200), 3))
E("l7", "screens[3].explain.text", round(log(3), 3))
E("l7", "screens[4].feedback.byKey.halfway", round(10 ** -0.5, 2))
E("l7", "screens[5].widget.answer", round(l2(1e6), 2))
E("l7", "screens[5].widget.wrong[0].value", round(6 * 0.301, 3))
E("l7", "screens[5].feedback.byKey.tens", round(1 / log(2), 1))
E("l7", "screens[5].explain.text", 2 ** 20)
E("l7", "screens[7].feedback.correct", round(math.log(200, 5), 2))
E("l7", "screens[7].explain.text", round(log(5), 3))
lv.claim(log(5) < 1 and "Converting to a new unit means dividing by its size" in lv.text("l7", "screens[7].widget.options[3].why") and "bigger unit" not in lv.text("l7", "screens[7].widget.options[3].why"),
         "l7 s7: a base-5 unit is smaller than a tenfold step (log 5 = 0.699), so the why does not say bigger (finding 19)")
E("l7", "screens[9].explain.text", round(log(1.25), 3))
E("l7", "screens[9].widget.answer", 12 * 1.25)
E("l7", "screens[9].feedback.correct", 12 * 1.25)
E("l7", "screens[9].explain.text", 12 * 1.25)
lv.claim(abs(log(12) - 1.079) < 5e-4 and abs(log(12) + log(1.25) - log(15)) < 1e-12 and abs(log(15) - 1.176) < 5e-4 and abs(log(20) - 1.301) < 5e-4 and abs(log(25) - 1.398) < 5e-4,
         "l7 s9: B starts at £12.00 (log 1.079) and ends at £15.00 (log 1.176); A is log 20 to log 25, so £20.00 is no longer on the canvas (finding 21)")
lv.claim([p["label"] for p in N("l7", "screens[9].canvas.state.points")] == ["£12.00", "£20.00", "£25.00"], "l7 s9: the canvas has no £15.00 label (finding 21)")
E("l7", "screens[9].widget.wrong[1].value", round(12 + log(1.25), 1))
E("l7", "screens[9].widget.wrong[0].value", 12 + 5)
E("l7", "quiz[1].widget.wrong[0].value", round(log(2) / log(3), 3))
E("l7", "quiz[1].widget.wrong[1].value", round(log(1.5), 3))
lv.claim("exactly" not in lv.text("l7", "quiz[1].widget.accept") and "1.58496" in lv.text("l7", "quiz[1].widget.accept") and abs(l2(3) - 1.58496) < 5e-6 and round(l2(3), 2) == 1.58,
         "l7 quiz[1]: log2 3 = 1.58496..., accept 1.58 (and 1.59) (finding 20)")
E("l7", "quiz[2].explain.text", round(log(1.5), 3))
lv.claim(abs(55 / 30 - 1 - 0.83) < 0.005, "l7 quiz[2]: £30 to £55 is +83%")
E("l7", "quiz[3].widget.options[2].text", round(log(9) / log(27), 3))
E("l7", "quiz[3].widget.options[3].text", round(log(3), 3))

# ---- l8 solving for the power
E("l8", "screens[0].feedback.correct", r2(500 * 1.1 ** 4))
E("l8", "screens[0].feedback.correct", r2(500 * 1.1 ** 5))
E("l8", "screens[0].widget.answer", next(n for n in range(30) if 500 * 1.1 ** n > 800))
lv.claim("about £798" in lv.text("l8", "screens[1].feedback.correct") and round(500 * 1.1 ** 4.9) == 798 and "£796" not in lv.text("l8", "screens[1].feedback.correct"),
         "l8 s1: the balance at 4.9 years is 500 x 1.1^4.9 = 797.62, about £798 (finding 22)")
E("l8", "screens[1].explain.text", round(ln(1.6) / ln(1.1), 2))
E("l8", "screens[2].widget.answer", round(0.2041 / 0.0414, 2))
E("l8", "screens[2].widget.wrong[0].value", round(0.0414 / 0.2041, 3))
E("l8", "screens[2].widget.wrong[1].value", round(0.2041 * 0.0414, 4))
lv.claim(N("l8", "screens[2].widget.wrong[1].value") == 0.0084 and round(0.2041 * 0.0414, 4) == 0.0084, "l8 s2: 0.2041 x 0.0414 = 0.0084, not 0.0085 (finding 23)")
for i_, v_ in ((1, 0.2041 * 0.0414), (2, 0.2041 - 0.0414)):   # the slip typed to 2 dp falls inside its band
    lv.claim(abs(round(v_, 2) - N("l8", f"screens[2].widget.wrong[{i_}].value")) <= N("l8", f"screens[2].widget.wrong[{i_}].tol")["abs"],
             f"l8 s2 wrong[{i_}]: the slip rounded to 2 dp ({round(v_, 2)}) is inside its band (finding 23)")
lv.claim(abs(round(log(1.2) / log(3), 2) - N("review", "items[5].widget.wrong[1].value")) <= N("review", "items[5].widget.wrong[1].tol")["abs"],
         "review-2 items[5] wrong flip: the slip rounded to 2 dp (0.17) is inside its band (finding 23)")
E("l8", "screens[2].widget.wrong[2].value", round(0.2041 - 0.0414, 4))
E("l8", "screens[3].widget.answer", round(log(50) / log(3), 3))
E("l8", "screens[3].widget.wrong[0].value", round(50 / 3, 2))
E("l8", "screens[3].widget.wrong[1].value", round(log(3) / log(50), 3))
E("l8", "screens[3].widget.wrong[2].value", round(log(50 / 3), 3))
E("l8", "screens[3].explain.text", round(3 ** 3.56, 1))
E("l8", "screens[4].widget.states.s3.tex", round(log(1.5) / log(1.05), 2))
E("l8", "screens[4].widget.states.s1b.tex", round(1.5 / 1.05, 4))
E("l8", "screens[6].widget.options[1].text", round(log(800) / log(550), 2))
E("l8", "screens[6].widget.options[2].text", round(log(800) / log(1.1), 2))
E("l8", "screens[7].feedback.correct", 48 / 3)
E("l8", "screens[9].widget.answer", round(log(2) / log(1.07), 2))
E("l8", "screens[9].widget.wrong[0].value", round(1000 / 70, 2))
E("l8", "screens[9].widget.wrong[1].value", round(2 / 0.07, 2))
E("l8", "screens[9].widget.wrong[2].value", round(2 / 1.07, 2))
E("l8", "screens[9].widget.wrong[3].value", round(log(1.07) / log(2), 3))
E("l8", "screens[9].hints[2].text", round(log(1.07), 5))
E("l8", "screens[9].explain.text", r2(1000 * 1.07 ** 11))
E("l8", "screens[9].explain.text", r2(1000 * 1.07 ** 10))
E("l8", "quiz[0].widget.answer", round(l2(12), 3))
lv.claim("exactly" not in lv.text("l8", "quiz[0].widget.accept") and "3.58496" in lv.text("l8", "quiz[0].widget.accept") and abs(l2(12) - 3.58496) < 5e-6 and round(l2(12), 2) == 3.58,
         "l8 quiz[0]: log2 12 = 3.58496..., accept 3.58 (and 3.59) (finding 20)")
E("l8", "quiz[1].feedback.correct", 202.5 / 40)
lv.claim(abs(1.5 ** 4 - 5.0625) < 1e-12, "l8 quiz[1]: 1.5^4 = 5.0625")
E("l8", "quiz[1].widget.wrong[0].value", round(log(202.5) / log(60), 3))
E("l8", "quiz[2].feedback.correct", r2(2500 / 256))
E("l8", "quiz[2].feedback.byKey.short", r2(2500 / 128))
E("l8", "quiz[2].explain.text", round(l2(250), 2))
E("l8", "quiz[3].widget.answer", round(log(0.5) / log(0.8), 3))
E("l8", "quiz[3].widget.wrong[1].value", round(log(0.8) / log(0.5), 3))
E("l8", "quiz[3].explain.text", round(log(0.8), 4))

# ---- review-2
E("review", "items[2].explain.text", round(math.log(200, 3), 2))
first3 = next(h for h in range(1, 20) if 3 ** h > 200)
lv.claim(first3 == 5 and 3 ** 4 == 81 and 3 ** 5 == 243 and 3 ** 4 < 200 < 3 ** 5, "review-2 items[2]: a colony tripling hourly first passes 200 cells in hour 5 (81 < 200 < 243) (finding 43)")
E("review", "items[2].widget.answer", first3)
E("review", "items[2].widget.wrong[0].value", 4)
E("review", "items[2].widget.wrong[1].value", round(200 / 3))
E("review", "items[2].widget.wrong[2].value", len(str(200)))
E("review", "items[2].feedback.correct", 81)
E("review", "items[2].feedback.correct", 243)
E("review", "items[2].feedback.byKey.low", 81)
E("review", "items[3].widget.answer", round(math.log(20, 4), 3))
E("review", "items[3].widget.wrong[0].value", round(log(4) / log(20), 3))
E("review", "items[3].widget.wrong[1].value", round(log(5), 3))
E("review", "items[5].widget.answer", round(log(3) / log(1.2), 3))
E("review", "items[5].widget.wrong[1].value", round(log(1.2) / log(3), 3))
E("review", "items[6].feedback.byKey.short", r2(5000 * 1.06 ** 8))
E("review", "items[6].explain.text", r2(5000 * 1.06 ** 9))
E("review", "items[6].explain.text", round(log(1.6) / log(1.06), 2))
E("review", "items[7].widget.answer", 10 ** ((63 - 43) / 10))
E("review", "items[7].widget.wrong[1].value", round(63 / 43, 3))

# ---- homework-2
E("homework", "items[0].widget.answer", round(math.log(2, 8), 4))
E("homework", "items[2].widget.answer", 24 * 60 / 80)
E("homework", "items[2].explain.text", round(log(0.75), 3))
lv.claim(round(20 / 24 * 100) == 83, "homework-2 items[2]: £20 off £24 is an 83% fall")
E("homework", "items[3].widget.answer", next(n for n in range(30) if 12000 * 0.85 ** n < 3000))
E("homework", "items[3].feedback.byKey.short", r2(12000 * 0.85 ** 8))
E("homework", "items[3].widget.wrong[2].value", round(log(0.25) / log(0.85), 2))
E("homework", "items[3].explain.text", round(log(0.85), 4))
E("homework", "items[4].explain.text", round(log(25), 3))
E("homework", "items[6].widget.answer", next(n for n in range(60) if 400 * 1.09 ** n > 1000 * 1.03 ** n))
E("homework", "items[6].widget.wrong[1].value", round(log(2.5) / log(1.09 / 1.03), 2))
E("homework", "items[6].feedback.byKey.short", r2(400 * 1.09 ** 16))
E("homework", "items[6].feedback.byKey.short", r2(1000 * 1.03 ** 16))
E("homework", "items[6].explain.text", r2(400 * 1.09 ** 17))
E("homework", "items[6].explain.text", r2(1000 * 1.03 ** 17))
E("homework", "items[7].model", round(log(1.07), 5))
E("homework", "items[7].model", round(log(2) / log(1.07), 2))
E("homework", "items[7].model", round(log(1.14), 5))
E("homework", "items[7].model", round(log(2) / log(1.14), 2))
E("homework", "items[7].model", round(1.07 ** 2, 4))

lv.check_wrongs()
lv.report()
