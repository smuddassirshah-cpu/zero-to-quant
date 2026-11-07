"""Second read of series level 2 (l5 to l8, review-2, homework-2): every graded key, every wrong[] value and the
numbers stated in prose, hints and feedback, each computed two ways (method 1: add the terms one by one, with
Fractions where exact; method 2: the closed forms n/2(a + l), a(r^n - 1)/(r - 1), a/(1 - r), C/r), checked against
the JSON with app/tools/numbers_lib.py. Convergence claims are checked numerically (partial sums at n = 10, 200).
Checks that fail mark content that is wrong (see docs/reviews/review-series-1-3.md); they pass once it is fixed.
Run: python3 docs/reports/series-L2-numbers.py
"""
import math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("series", 2)
bad = []


def two(name, a, b, tol=1e-9):
    if abs(a - b) > tol * max(1, abs(a)):
        bad.append(f'{name}: {a} != {b}')
    return a


r2 = lambda x: round(x + 1e-12, 2)
asum = lambda a, d, n: F(n, 2) * (2 * a + (n - 1) * d)
gsum = lambda a, r, n: a * (1 - r ** n) / (1 - r)
brute = lambda f, lo, hi: sum(f(k) for k in range(lo, hi + 1))
partial = lambda a, r, n: sum(a * r ** k for k in range(n))

# ---------------- l5 ----------------
lv.expect("l5", "screens[1].widget.answer", two('l5 s1', brute(lambda k: 2 * k + 1, 1, 3), asum(3, 2, 3)))
for i, v in enumerate([7, 3 * 7, 3 + 7, brute(lambda k: 2 * k + 1, 1, 4)]):
    lv.expect("l5", f"screens[1].widget.wrong[{i}].value", v)
lv.expect("l5", "screens[1].explain.text", brute(lambda k: 2 * k + 1, 1, 5))
lv.expect("l5", "screens[4].explain.text", two('l5 s4', brute(lambda k: 3 * k + 1, 1, 6), asum(4, 3, 6)))
lv.expect("l5", "screens[5].widget.answer", two('l5 s5', brute(lambda k: k * k, 1, 4), 4 * 5 * 9 // 6))
for i, v in enumerate([10 ** 2, 16, 10, 20]):
    lv.expect("l5", f"screens[5].widget.wrong[{i}].value", v)
lv.expect("l5", "screens[6].widget.answer", two('l5 s6', brute(lambda k: 5, 4, 12), 5 * (12 - 4 + 1)))
for i, v in enumerate([5 * 8, 5 * 12, 5, 5 * 11]):
    lv.expect("l5", f"screens[6].widget.wrong[{i}].value", v)
lv.expect("l5", "screens[7].widget.answer", two('l5 s7', len(range(7, 21)), 20 - 7 + 1))
p = [40.0, 41.2, 40.7, 42.8, 42.0, 42.4]
lv.claim(abs(sum(p[k] - p[k - 1] for k in range(1, 6)) - (p[5] - p[0]) ) < 1e-9 and abs(p[5] - p[0] - 2.40) < 1e-9, 'l5 s8: telescoping 42.40 - 40.00 = 2.40')
d = [1200, -450, 800, -1500, 350]
cum = [sum(d[:k]) for k in range(1, 6)]
lv.expect("l5", "screens[9].widget.answer", two('l5 s9', cum[3], 1200 - 450 + 800 - 1500))
lv.claim(cum == [1200, 750, 1550, 50, 400], 'l5 s9: cumulative 1200, 750, 1550, 50, 400')
lv.expect("l5", "screens[9].widget.wrong[1].value", sum(abs(x) for x in d[:4]))
lv.expect("l5", "quiz[0].widget.answer", two('l5 q0', brute(lambda k: 10 - k, 1, 4), 40 - 10))
lv.expect("l5", "quiz[0].widget.wrong[0].value", brute(lambda k: 10 + k, 1, 4))
lv.expect("l5", "quiz[3].widget.answer", 50 - 41)
lv.expect("l5", "quiz[3].widget.wrong[2].value", round(50 / 6, 2))

# ---------------- l6 ----------------
lv.claim(brute(lambda k: k, 1, 5) * 2 == 5 * 6 and brute(lambda k: k, 1, 4) * 2 == 4 * 5, 'l6 s1, s2: two staircases fill the rectangle')
lv.expect("l6", "screens[3].explain.text", two('l6 s3', brute(lambda k: k, 1, 6), F(6 * 7, 2)))
lv.expect("l6", "screens[4].widget.answer", two('l6 s4', brute(lambda k: k, 1, 100), F(100 * 101, 2)))
for i, v in enumerate([100 * 101, 50 * 100, 51 * 100, 101]):
    lv.expect("l6", f"screens[4].widget.wrong[{i}].value", v)
lv.expect("l6", "screens[5].widget.answer", two('l6 s5', brute(lambda k: 3 * k, 1, 5), F(5, 2) * 18))
for i, v in enumerate([2 * 18, 3 * 18, 5 * 18]):
    lv.expect("l6", f"screens[5].widget.wrong[{i}].value", v)
n6 = (50 - 5) // 3 + 1
lv.expect("l6", "screens[6].widget.answer", two('l6 s6', brute(lambda k: 5 + 3 * k, 0, 15), F(n6, 2) * 55))
for i, v in enumerate([F(15, 2) * 55, 16 * 55, F(17, 2) * 55, 15 * 55]):
    lv.expect("l6", f"screens[6].widget.wrong[{i}].value", float(v))
lv.expect("l6", "screens[8].widget.answer", two('l6 s8', brute(lambda k: 4 + 3 * (k - 1), 1, 20), asum(4, 3, 20)))
lv.expect("l6", "screens[8].widget.wrong[0].value", 10 * (8 + 20 * 3))
lv.expect("l6", "screens[8].widget.wrong[2].value", 4 + 19 * 3)
asks = [200 + 150 * k for k in range(8)]
lv.claim(asks[-1] == 1250, 'l6 s9: the best ask holds 200 and £100.07 holds 1,250 shares')
lv.expect("l6", "screens[9].widget.answer", two('l6 s9', sum(asks), 4 * (200 + 1250)))
for i, v in enumerate([F(7, 2) * 1450, 2 * 5800, 4 * (200 + 200 + 8 * 150), 8 * 200]):
    lv.expect("l6", f"screens[9].widget.wrong[{i}].value", float(v))
lv.expect("l6", "quiz[0].widget.answer", two('l6 q0', brute(lambda k: k, 1, 50), 25 * 51))
lv.expect("l6", "quiz[1].widget.answer", two('l6 q1', brute(lambda k: 2 * k - 1, 1, 10), 10 ** 2))
lv.claim(all(brute(lambda k: 2 * k - 1, 1, n) == n * n for n in range(1, 60)), 'l6 q1: the first n odd numbers always add to n^2')
lv.expect("l6", "quiz[1].widget.wrong[1].value", F(9, 2) * 20)
lv.expect("l6", "quiz[1].widget.wrong[2].value", brute(lambda k: 2 * k, 1, 10))
lv.expect("l6", "quiz[2].widget.options[0].text", two('l6 q2', len(range(12, 61, 3)), (60 - 12) // 3 + 1))
lv.expect("l6", "quiz[3].widget.answer", F(25, 2) * 88)
lv.expect("l6", "quiz[3].widget.wrong[1].value", F(25, 2) * 72)

# ---------------- l7 ----------------
lv.expect("l7", "screens[0].widget.answer", two('l7 s0', brute(lambda k: 2 ** k, 0, 7), 2 ** 8 - 1))
lv.expect("l7", "screens[0].widget.wrong[3].value", 128 * 8)
lv.claim(all(brute(lambda k: a1 * 2 ** k, 0, 5) == a1 * 2 ** 6 - a1 for a1 in range(1, 6)), 'l7 s1: total of six = seventh minus first, every slider value')
lv.expect("l7", "screens[1].explain.text", brute(lambda k: 3 * 2 ** k, 0, 5))
lv.expect("l7", "screens[2].feedback.correct", two('l7 s2', brute(lambda k: 2 ** k, 0, 4), 32 - 1))
lv.expect("l7", "screens[3].widget.answer", two('l7 s3', brute(lambda k: 2 * 3 ** k, 0, 4), gsum(2, 3, 5)))
lv.expect("l7", "screens[3].widget.wrong[2].value", 3 * 242)
lv.expect("l7", "screens[4].widget.answer", two('l7 s4', brute(lambda k: 48 * F(1, 2) ** k, 0, 4), gsum(48, F(1, 2), 5)))
lv.expect("l7", "screens[4].widget.wrong[1].value", 48 / (1 - 0.5))
lv.expect("l7", "screens[4].widget.wrong[2].value", 48 + 1.5)
lv.expect("l7", "screens[5].widget.answer", two('l7 s5', brute(lambda k: 3 * 2 ** k, 0, 8), 3 * (2 ** 9 - 1)))
lv.claim(3 * 2 ** 8 == 768, 'l7 s5: 768 = 3 x 2^8')
for i, v in enumerate([3 * (2 ** 8 - 1), 2 * 768, 3 * (2 ** 10 - 1), 768]):
    lv.expect("l7", f"screens[5].widget.wrong[{i}].value", v)
lv.expect("l7", "screens[7].widget.options[0].text", 12 * 5)
pv = lambda C, i, n: sum(C / (1 + i) ** k for k in range(1, n + 1))
ann = pv(500, 0.04, 10)
lv.expect("l7", "screens[8].widget.answer", two('l7 s8', r2(ann), r2(500 / 0.04 * (1 - 1.04 ** -10))))
lv.expect("l7", "screens[8].widget.wrong[1].value", r2(ann * 1.04))
lv.expect("l7", "screens[8].widget.wrong[2].value", r2(pv(500, 0.04, 9)))
lv.expect("l7", "screens[8].widget.wrong[3].value", r2(5000 / 1.04 ** 10))
# finding 14: the step hint shows a/(1 - r) = 500/0.04 = 12500, then 12500(1 - 1/1.04^10)
two_ann = 12500 * (1 - 1 / 1.04 ** 10)
lv.claim(abs((500 / 1.04) / (1 - 1 / 1.04) - 12500) < 1e-9 and abs(500 / 0.04 - 12500) < 1e-9 and r2(two_ann) == r2(ann) == 4055.45, 'l7 s8: a/(1 - r) = 12500 and 12500(1 - 1/1.04^10) = 4055.45 by both methods')
lv.expect("l7", "screens[8].hints[2].text", 12500)
lv.expect("l7", "screens[8].hints[2].text", r2(ann))
lv.expect("l7", "screens[8].feedback.correct", r2(ann))
lv.claim('^{-10}' not in lv.text("l7", "screens[8].hints[2].text") + lv.text("l7", "screens[8].feedback.correct"), 'l7 s8: no negative index in the hint or the correct line')
lv.claim(all(abs(round(500 / 1.04 ** k, 2) - v) < 1e-9 for k, v in zip(range(1, 11), [480.77, 462.28, 444.5, 427.4, 410.96, 395.16, 379.96, 365.35, 351.29, 337.78])), 'l7 s8: the ten bar values')
lv.expect("l7", "quiz[0].widget.answer", two('l7 q0', brute(lambda k: 3 ** k, 0, 5), (3 ** 6 - 1) // 2))
lv.expect("l7", "quiz[0].widget.wrong[1].value", (3 ** 7 - 1) // 2)
q1 = brute(lambda k: F(1, 2 ** k), 0, 5)
lv.claim(q1 == F(63, 32) and brute(lambda k: F(1, 2 ** k), 0, 4) == F(31, 16) and brute(lambda k: F(1, 2 ** k), 0, 6) == F(127, 64), 'l7 q1: 63/32, 31/16, 127/64')
lv.expect("l7", "quiz[2].widget.answer", two('l7 q2', brute(lambda k: 2 ** k, 0, 9), 2 ** 10 - 1))
lv.expect("l7", "quiz[3].widget.answer", two('l7 q3', brute(lambda k: 4 * (-2) ** k, 0, 4), gsum(4, -2, 5)))
lv.expect("l7", "quiz[3].widget.wrong[0].value", brute(lambda k: 4 * 2 ** k, 0, 4))
lv.expect("l7", "quiz[3].widget.wrong[1].value", 4 * ((-2) ** 5 - 1))
# "96 is what the halving terms approach": the terms approach 0; the total approaches 96
lv.stated("l7", "screens[4].feedback.byKey.forever", "halving terms approach", abs(48 * 0.5 ** 200 - 96) < 1e-6)
lv.stated("l7", "quiz[1].widget.options[1].why", "2 is what the halves approach", abs(0.5 ** 200 - 2) < 1e-6)

# ---------------- l8 ----------------
lv.claim(brute(lambda k: F(1, 2 ** k), 1, 4) == F(15, 16), 'l8 s0: four steps shade 15/16')
lv.claim(all(abs(partial(1, r, 400) - 1 / (1 - r)) < 1e-6 for r in (0.5, 0.9, -0.5, -0.9)) and partial(1, 1, 10) == 10, 'l8 s1: settle for -1 < r < 1; climb at r = 1')
s10 = partial(1, 0.9, 10)
# "You saw the sums settle for r = 0.5, 0.9": at 0.9 the tenth dot is 6.51, far from the limit 10
lv.stated("l8", "screens[1].explain.text", "settle for $r = 0.5$, $0.9$", abs(s10 - 10) < 0.5)
# finding 15: r = 0.5 and -0.5 level off by the tenth dot; r = 0.9 is still climbing (6.51 of 10)
lv.claim(abs(partial(1, 0.5, 10) - 2) < 0.01 and abs(partial(1, -0.5, 10) - 2 / 3) < 0.001 and partial(1, 0.9, 10) < partial(1, 0.9, 11) and round(s10, 2) == 6.51 and abs((1 - 0.9 ** 10) / 0.1 - s10) < 1e-9,
         'l8 s1: S_10 is 1.998 (r = 0.5), 0.666 (r = -0.5) and 6.51 (r = 0.9, still climbing towards 10)')
lv.claim([partial(1, -1, n) for n in range(1, 7)] == [1, 0, 1, 0, 1, 0], 'l8 s1: at r = -1 the sums flip between 1 and 0')
lv.expect("l8", "screens[1].explain.text", 10)
lv.claim('0.5$ and $-0.5$' in lv.text("l8", "screens[1].explain.text") and 'settle for $r = 0.5$, $0.9$' not in lv.text("l8", "screens[1].explain.text"), 'l8 s1: only 0.5 and -0.5 are said to level off')
lv.expect("l8", "screens[1].widget.options[2].why", round(1 / 1.5, 3))
lv.expect("l8", "screens[2].widget.answer", two('l8 s2', 1 / (1 - 1 / 3), partial(1, 1 / 3, 200)))
lv.expect("l8", "screens[2].widget.wrong[1].value", 1 / (1 / 3))
lv.expect("l8", "screens[2].widget.wrong[2].value", round(1 * 2 / 3, 4))
lv.expect("l8", "screens[3].widget.answer", two('l8 s3', 6 / (1 - 1 / 3), partial(6, 1 / 3, 200)))
lv.expect("l8", "screens[3].widget.wrong[0].value", 6 / (1 / 3))
lv.expect("l8", "screens[3].widget.wrong[1].value", 6 / (1 + 1 / 3))
lv.expect("l8", "screens[4].widget.answer", two('l8 s4', round(8 / 1.5, 4), round(partial(8, -0.5, 200), 4)))
lv.expect("l8", "screens[4].widget.wrong[0].value", 8 / 0.5)
lv.expect("l8", "screens[4].widget.wrong[2].value", partial(8, -0.5, 2))
lv.claim(all(partial(1, 2, n) == 2 ** n - 1 for n in range(1, 30)), 'l8 s5: partial sums 2^n - 1 grow without limit')
lv.expect("l8", "screens[6].explain.text", two('l8 s6a', 5 / (1 - 0.8), partial(5, 0.8, 300)))
lv.expect("l8", "screens[6].explain.text", round(10 / 1.9, 2))
lv.claim(abs(4 / 5 - 0.8) < 1e-12 and abs(-9 / 10 + 0.9) < 1e-12 and 4.5 / 3 == 1.5, 'l8 s6: ratios 0.8, -0.9, 1.5')
perp = 5 / 0.04
lv.expect("l8", "screens[8].widget.answer", two('l8 s8', perp, sum(5 / 1.04 ** k for k in range(1, 3000))))
lv.expect("l8", "screens[8].widget.wrong[0].value", perp + 5)
lv.expect("l8", "screens[8].widget.wrong[1].value", r2(5 / 1.04))
lv.expect("l8", "screens[8].widget.wrong[2].value", r2(perp / 1.04))
lv.claim(all(abs(round(5 / 1.04 ** k, 2) - v) < 1e-9 for k, v in zip(range(1, 11), [4.81, 4.62, 4.44, 4.27, 4.11, 3.95, 3.8, 3.65, 3.51, 3.38])), 'l8 s8: the ten bar values')
# "Outside that range the formula gives a number": at r = 1 it divides by 0
lv.stated("l8", "summary.formula.note", "the formula gives a number", False)
lv.claim(lv.text("l8", "summary.formula.note").startswith("Outside that range the formula may still give a number"), 'l8 summary note: "may still give a number" (r = 2 gives -1 for a series with no sum; r = 1 divides by 0)')
lv.expect("l8", "quiz[0].widget.answer", two('l8 q0', 12 / 0.5, partial(12, 0.5, 200)))
lv.expect("l8", "quiz[0].widget.wrong[0].value", 12 / 1.5)
lv.claim(F(3, 10) / (1 - F(1, 10)) == F(1, 3) and F(3, 10) / (1 + F(1, 10)) == F(3, 11), 'l8 q1: 1/3, and 3/11 from 1 + r')
lv.claim([partial(1, -1, n) for n in range(1, 7)] == [1, 0, 1, 0, 1, 0], 'l8 q2: partial sums flip 1, 0')
lv.expect("l8", "quiz[3].widget.answer", two('l8 q3', round(20 / 1.5, 4), round(partial(20, -0.5, 200), 4)))
lv.expect("l8", "quiz[3].widget.wrong[0].value", 20 / 0.5)
# "A recurring decimal is a geometric series": 0.1666... = 1/10 + a geometric series, not one series
lv.stated("l8", "quiz[1].explain.text", "A recurring decimal is a geometric series", False)

# ---------------- review-2 ----------------
lv.expect("review", "items[0].widget.answer", two('r2 i0', brute(lambda k: k * k + 1, 2, 5), 54 + 4))
for i, v in enumerate([brute(lambda k: k * k + 1, 1, 5), 54, 55]):
    lv.expect("review", f"items[0].widget.wrong[{i}].value", v)
lv.expect("review", "items[1].widget.answer", 30 - 5 + 1)
lv.expect("review", "items[2].widget.answer", two('r2 i2', brute(lambda k: 2 * k, 1, 100), 50 * 202))
lv.expect("review", "items[3].widget.answer", two('r2 i3', brute(lambda k: 7 + 5 * k, 0, 19), asum(7, 5, 20)))
for i, v in enumerate([F(19, 2) * 109, 2180, F(21, 2) * 109]):
    lv.expect("review", f"items[3].widget.wrong[{i}].value", float(v))
lv.expect("review", "items[4].widget.answer", two('r2 i4', brute(lambda k: 5 * 3 ** k, 0, 6), gsum(5, 3, 7)))
for i, v in enumerate([gsum(5, 3, 6), 2 * 5465, gsum(5, 3, 8)]):
    lv.expect("review", f"items[4].widget.wrong[{i}].value", v)
mi = sum(100 * 1.01 ** (k - 1) for k in range(1, 13))
lv.expect("review", "items[5].widget.answer", two('r2 i5', r2(mi), r2(10000 * 1.01 ** 12 - 10000)))
lv.expect("review", "items[5].widget.wrong[1].value", r2(10000 + mi))
lv.expect("review", "items[5].widget.wrong[2].value", r2(10000 * 1.01 ** 11 - 10000))
lv.claim(F(9, 10) / (1 - F(1, 10)) == 1, 'review-2 i6: 0.999... = 1')
lv.expect("review", "items[7].widget.answer", two('r2 i7', 2.5 / 0.4, partial(2.5, 0.6, 300)))
lv.expect("review", "items[7].widget.wrong[0].value", 2.5 + 1.5)
lv.expect("review", "items[7].widget.wrong[1].value", round(2.5 / 0.6, 4))
# wrong[2] "plus" says "You divided by 1 + 0.6": 2.5 / 1.6 = 1.5625, not 1.7857 (= 2.5 / 1.4)
lv.expect("review", "items[7].widget.wrong[2].value", 2.5 / 1.6)
lv.claim(4.5 / 3 == 1.5 and 3 / (1 - 1.5) == -6, 'review-2 i8: r = 1.5; formula gives -6')

# ---------------- homework-2 ----------------
lv.claim(all(4 * k + 1 == 5 + 4 * (k - 1) for k in range(1, 11)) and 4 * 10 + 1 == 41, 'homework-2 i0: f(k) = 4k + 1')
lv.expect("homework", "items[1].widget.answer", two('h2 i1', float(brute(lambda k: F(1, k * (k + 1)), 1, 99)), 1 - 1 / 100))
lv.expect("homework", "items[1].widget.wrong[1].value", round(1 - 1 / 101, 6))
S = lambda n: sum(4 * k - 1 for k in range(1, n + 1))
first = next(n for n in range(1, 100) if S(n) > 1000)
lv.expect("homework", "items[2].widget.answer", two('h2 i2', first, math.ceil((-1 + math.sqrt(1 + 8000)) / 4)))
lv.expect("homework", "items[2].feedback.correct", S(22))
lv.expect("homework", "items[2].feedback.correct", S(23))
lv.claim(all(S(n) == n * (2 * n + 1) for n in range(1, 40)), 'homework-2 i2: S_n = n(2n + 1)')
# finding 24: the explanation no longer solves a quadratic; it says 2n^2 = 1000 puts n near 22 and checks S_22, S_23
lv.claim(math.floor(math.sqrt(1000 / 2)) == 22 and first == 23 and S(22) < 1000 < S(23) and 22 < math.sqrt(500) < 23, 'homework-2 i2: 2n^2 = 1000 puts n near 22 (sqrt 500 = 22.36)')
lv.expect("homework", "items[2].explain.text", 22)
lv.expect("homework", "items[2].explain.text", S(22))
lv.expect("homework", "items[2].explain.text", S(23))
lv.expect("homework", "items[2].explain.text", 2 * 500)
lv.claim('22.1' not in lv.text("homework", "items[2].explain.text") and 'quadratic' not in lv.text("homework", "items[2].explain.text"), 'homework-2 i2: no quadratic formula in the explanation')
lv.expect("homework", "items[2].widget.wrong[1].value", math.floor((1000 + 1) / 4))
cost = lambda n: 5 * (2 ** n - 1)
lv.expect("homework", "items[3].widget.answer", two('h2 i3', max(n for n in range(1, 30) if cost(n) <= 5000), math.floor(math.log2(5000 / 5 + 1))))
lv.expect("homework", "items[3].widget.accept", cost(9))
lv.expect("homework", "items[3].explain.text", max(n for n in range(1, 30) if cost(n) <= 5000))   # the answer 9 as a figure (finding 31)
lv.expect("homework", "items[3].feedback.correct", cost(10))
lv.expect("homework", "items[3].feedback.byKey.eight", cost(8))
lv.expect("homework", "items[3].feedback.byKey.eight", 5 * 2 ** 8)
P = 10000 * 0.005 / (1 - 1.005 ** -24)
lv.expect("homework", "items[4].widget.answer", two('h2 i4', r2(P), r2(10000 / sum(1.005 ** -k for k in range(1, 25)))))
lv.expect("homework", "items[4].widget.wrong[0].value", r2(10000 / 24))
lv.expect("homework", "items[4].widget.wrong[1].value", r2((10000 + 24 * 50) / 24))
lv.expect("homework", "items[4].widget.wrong[2].value", r2(P / 1.005))
lv.expect("homework", "items[4].explain.text", round((1 - 1.005 ** -24) / 0.005, 4))
lv.expect("homework", "items[4].explain.text", r2(24 * r2(P)))
lv.claim(F(27, 100) / (1 - F(1, 100)) == F(3, 11) and F(27, 100) / (1 + F(1, 100)) == F(27, 101), 'homework-2 i6: 3/11, and 27/101')
V30 = 1000 / 0.05 * (1 - 1.05 ** -30)
lv.expect("homework", "items[7].model", two('h2 i7 A', r2(V30), r2(sum(1000 / 1.05 ** k for k in range(1, 31)))))
lv.expect("homework", "items[7].model", r2(20000 - V30))
lv.expect("homework", "items[7].model", round(1.05 ** -30, 6))

lv.claim(not bad, 'every number agrees by both methods', '; '.join(bad))
lv.check_wrongs()
lv.report()
