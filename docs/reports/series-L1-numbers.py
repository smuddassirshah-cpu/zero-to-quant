"""Second read of series level 1 (l1 to l4, review-1, homework-1): every graded key, every wrong[] value and the
numbers stated in prose, hints and feedback, each computed two ways (method 1: generate the terms one by one;
method 2: the closed form u_n = a + (n - 1)d, ar^(n-1), or the fixed-point formula), and checked against the JSON
with app/tools/numbers_lib.py. Claims that are not one number use lv.stated / lv.claim.
Checks that fail mark content that is wrong (see docs/reviews/review-series-1-3.md); they pass once it is fixed.
Run: python3 docs/reports/series-L1-numbers.py
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("series", 1)
bad = []


def two(name, a, b, tol=1e-9):
    if abs(a - b) > tol * max(1, abs(a)):
        bad.append(f'{name}: {a} != {b}')
    return a


def gen(a, step, n):            # method 1: term n by repeated steps
    u = a
    for _ in range(n - 1):
        u = step(u)
    return u


arith = lambda a, d, n: a + (n - 1) * d
geom = lambda a, r, n: a * r ** (n - 1)
r2 = lambda x: round(x + 1e-12, 2)

# ---------------- l1 ----------------
lv.expect("l1", "screens[0].widget.answer", two('l1 s0', gen(5, lambda u: u + 4, 5), arith(5, 4, 5)))
lv.expect("l1", "screens[0].widget.wrong[0].from", 17 + 5)
lv.expect("l1", "screens[0].widget.wrong[2].from", 17 + 3)
lv.expect("l1", "screens[1].widget.answer", two('l1 s1', (2 + 5 * 4) - (2 + 5 * 3), 6 - 1))
lv.expect("l1", "screens[2].widget.answer", two('l1 s2', gen(10, lambda u: u - 3, 6), arith(10, -3, 6)))
lv.expect("l1", "screens[2].widget.wrong[0].value", arith(10, -3, 5))
lv.expect("l1", "screens[2].widget.wrong[3].value", arith(10, -3, 7))
lv.expect("l1", "screens[3].widget.answer", two('l1 s3', 4 * 50 + 3, arith(7, 4, 50)))
lv.expect("l1", "screens[3].widget.wrong[1].value", 7 + 50 * 4)
lv.expect("l1", "screens[3].widget.wrong[2].value", 50 + 4)
lv.expect("l1", "screens[4].widget.answer", two('l1 s4', 12 * 12, sum(2 * k - 1 for k in range(1, 13))))
lv.expect("l1", "screens[4].widget.wrong[2].value", 25 + 11)
lv.expect("l1", "screens[5].widget.options[3].text", two('l1 s5', gen(3, lambda u: 2 * u, 5), geom(3, 2, 5)))
lv.expect("l1", "screens[5].widget.options[0].text", 24 + 3)
lv.expect("l1", "screens[5].widget.options[1].text", 24 + 6)
lv.expect("l1", "screens[5].widget.options[2].text", 24 + 12)
lv.expect("l1", "screens[6].explain.text", 10 - 2 * 100)
# the option "10, 8, 6, 4, ..." is offered as "the sequence itself" of term = 10 - 2n, which starts 8, 6, 4, 2
seq = [10 - 2 * n for n in range(1, 5)]
lv.stated("l1", "screens[6].widget.options[3].text", "10, 8, 6, 4", seq[:4] == [10, 8, 6, 4])
lv.expect("l1", "screens[7].widget.answer", two('l1 s7', r2(gen(50.0, lambda u: u - 0.25, 8)), r2(arith(50, -0.25, 8))))
lv.expect("l1", "screens[7].widget.wrong[0].value", 50 - 8 * 0.25)
lv.expect("l1", "screens[7].widget.wrong[1].value", 50 + 7 * 0.25)
lv.expect("l1", "screens[7].widget.wrong[2].value", 50 + 8 * 0.25)
lv.expect("l1", "screens[8].widget.answer", two('l1 s8', gen(8000, lambda u: u / 2, 4), geom(8000, 0.5, 4)))
lv.expect("l1", "screens[8].widget.wrong[0].value", 2000 - 4000)
lv.expect("l1", "screens[8].widget.wrong[2].value", 2000 / 4)
lv.expect("l1", "quiz[0].widget.answer", two('l1 q0', 23 + 7, arith(2, 7, 5)))
lv.expect("l1", "quiz[2].widget.answer", 10 - 3 * 5)
lv.expect("l1", "quiz[2].widget.wrong[0].value", (10 - 3) * 5)
lv.expect("l1", "quiz[2].widget.wrong[2].value", 10 - 3 * 4)
lv.expect("l1", "quiz[3].widget.options[2].text", two('l1 q3', 45 * 3, geom(5, 3, 4)))
lv.expect("l1", "quiz[3].widget.options[0].text", 45 + 10)
lv.expect("l1", "quiz[3].widget.options[1].text", 45 + 30)
lv.expect("l1", "quiz[3].widget.options[3].text", 45 * 2)

# ---------------- l2 ----------------
lv.expect("l2", "screens[0].widget.answer", two('l2 s0', (19 - 4) // 3, 6 - 1))
lv.expect("l2", "screens[1].widget.answer", two('l2 s1', arith(4, 3, 40), gen(4, lambda u: u + 3, 40)))
lv.expect("l2", "screens[1].widget.wrong[0].value", 4 + 40 * 3)
lv.expect("l2", "screens[1].widget.wrong[2].value", 40 + 3)
lv.expect("l2", "screens[1].explain.canvas.caption", arith(4, 3, 12))
lv.expect("l2", "screens[2].widget.answer", two('l2 s2', arith(11, 6, 10), gen(11, lambda u: u + 6, 10)))
lv.expect("l2", "screens[2].widget.wrong[0].value", 11 + 10 * 6)
lv.expect("l2", "screens[2].widget.wrong[2].value", 6 + 9 * 11)
lv.expect("l2", "screens[2].explain.text", arith(11, 6, 4))
lv.expect("l2", "screens[3].widget.answer", two('l2 s3', arith(50, -4, 15), gen(50, lambda u: u - 4, 15)))
for i, v in enumerate([50 - 60, 50 + 56, 50 + 60, 6]):
    lv.expect("l2", f"screens[3].widget.wrong[{i}].value", v)
n100 = (100 - 2) / 3
lv.claim(n100 != int(n100) and 3 * 32 + 2 == 98 and 3 * 33 + 2 == 101, 'l2 s4: 100 lies strictly between u32 = 98 and u33 = 101')
lv.expect("l2", "screens[4].widget.options[2].why", 3 * 20 + 2)
lv.expect("l2", "screens[5].widget.answer", two('l2 s5', (39 - 14) / (8 - 3), 5))
lv.expect("l2", "screens[5].widget.wrong[1].value", round(25 / 6, 4))
lv.expect("l2", "screens[5].widget.wrong[2].value", 25 / 8)
lv.expect("l2", "screens[5].explain.text", 34)
lv.claim([3 * n + 1 for n in range(1, 5)] == [4, 7, 10, 13] and [4 + 3 * n for n in range(1, 5)] == [7, 10, 13, 16], 'l2 s6: 3n + 1 fits, 4 + 3n is one step ahead')
lv.expect("l2", "screens[8].widget.answer", two('l2 s8', arith(1500, 200, 24), gen(1500, lambda u: u + 200, 24)))
for i, v in enumerate([1500 + 24 * 200, 24 * 200, 23 * 200]):
    lv.expect("l2", f"screens[8].widget.wrong[{i}].value", v)
first = next(n for n in range(1, 200) if arith(1500, 200, n) > 10000)
lv.expect("l2", "screens[9].widget.answer", two('l2 s9', first, math.floor((10000 - 1500) / 200) + 2))
lv.expect("l2", "screens[9].feedback.byKey.m43", arith(1500, 200, 43))
lv.expect("l2", "screens[9].widget.wrong[1].value", 10000 / 200)
lv.expect("l2", "quiz[0].feedback.correct", 4)
lv.claim(all(9 + 5 * (n - 1) == 5 * n + 4 for n in range(1, 9)), 'l2 q0: 9 + 5(n - 1) = 5n + 4')
lv.expect("l2", "quiz[1].widget.answer", two('l2 q1', arith(20, -3, 12), gen(20, lambda u: u - 3, 12)))
lv.expect("l2", "quiz[1].widget.wrong[0].value", 20 - 36)
lv.expect("l2", "quiz[1].widget.wrong[1].value", 20 + 33)
lv.expect("l2", "quiz[2].widget.answer", (50 - 30) / (9 - 5))
lv.expect("l2", "quiz[3].widget.answer", two('l2 q3', (102 - 2) / 5, next(n for n in range(1, 50) if 5 * n + 2 == 102)))
lv.expect("l2", "quiz[3].feedback.byKey.over", 5 * 21 + 2)

# ---------------- l3 ----------------
lv.expect("l3", "screens[0].widget.answer", two('l3 s0', 54 * 3, geom(2, 3, 5)))
lv.expect("l3", "screens[0].widget.wrong[0].from", 54 + 36)
lv.expect("l3", "screens[0].widget.wrong[1].from", 54 * 2)
lv.claim([4 * 1.5 ** k - 4 * 1.5 ** (k - 1) for k in (1, 2, 3)] == [2, 3, 4.5], 'l3 s1: rises 2, 3, 4.5 at r = 1.5')
lv.expect("l3", "screens[3].widget.answer", two('l3 s3', 3 / 2, 6.75 / 4.5))
lv.expect("l3", "screens[3].widget.wrong[1].value", round(2 / 3, 4))
lv.expect("l3", "screens[4].widget.answer", two('l3 s4', geom(3, 2, 8), gen(3, lambda u: 2 * u, 8)))
lv.expect("l3", "screens[4].widget.wrong[0].value", 3 * 2 ** 8)
lv.expect("l3", "screens[4].widget.wrong[1].value", geom(3, 2, 7))
lv.expect("l3", "screens[4].widget.wrong[2].value", arith(3, 3, 8))
lv.expect("l3", "screens[5].widget.answer", two('l3 s5', geom(16, -0.5, 6), gen(16, lambda u: -0.5 * u, 6)))
# wrong[2] "add" (-26) and wrong[3] "times-two" (-32) match no stated slip for u6: the fixed values are below
lv.expect("l3", "screens[5].widget.wrong[2].value", -2 - 6 - 6)          # subtract the last gap, 6, twice
lv.expect("l3", "screens[5].widget.wrong[3].value", -2 * (-2) * (-2))     # multiply u4 by -2 twice
lv.expect("l3", "screens[6].widget.options[1].why", (3 * 2) ** 4)
lv.expect("l3", "screens[6].widget.options[2].why", 3 * 2 ** 5)
lv.expect("l3", "screens[6].widget.options[3].why", 3 + 4 * 2)
lv.expect("l3", "screens[6].feedback.correct", geom(3, 2, 5))
lv.claim(all(5 * 3 ** (n - 1) == gen(5, lambda u: 3 * u, n) for n in range(1, 10)), 'l3 s7: u_n = 5 x 3^(n-1)')
d8 = 1.20 * 1.05 ** 7
lv.expect("l3", "screens[8].widget.answer", two('l3 s8', r2(d8), r2(gen(1.20, lambda u: u * 1.05, 8))))
lv.expect("l3", "screens[8].widget.accept", round(d8, 4))
lv.expect("l3", "screens[8].widget.wrong[0].value", r2(1.20 * 1.05 ** 8))
lv.expect("l3", "screens[8].widget.wrong[1].value", r2(1.20 + 7 * 0.06))
lv.expect("l3", "screens[8].canvas.params.rows[2][1]", "£1.32")
B = 20000 * 1.01 ** 12; A = 20000 + 12 * 200
lv.expect("l3", "screens[9].widget.answer", two('l3 s9', r2(B - A), r2(gen(20000.0, lambda u: u * 1.01, 13) - arith(20000, 200, 13))))
lv.expect("l3", "screens[9].widget.accept", r2(B))
lv.expect("l3", "screens[9].widget.wrong[1].value", r2(B - 20000))
lv.claim(abs(20000 * 0.01 - 200) < 1e-9, 'l3 s9: both plans gain £200.00 in month 1')
lv.expect("l3", "quiz[0].widget.answer", two('l3 q0', 8000 * 0.5 ** 4, gen(8000, lambda u: u / 2, 5)))
lv.expect("l3", "quiz[1].widget.answer", two('l3 q1', 48 / 64, 36 / 48))
lv.expect("l3", "quiz[1].widget.wrong[1].value", round(64 / 48, 4))
lv.expect("l3", "quiz[2].explain.text", geom(10, -0.5, 5))
# "curving means multiply": the squares 1, 4, 9, 16 curve but have no common ratio (quiz[3] option "squares")
sq = [1, 4, 9, 16]
lv.stated("l3", "screens[2].explain.text", "curving means multiply", len({sq[i + 1] / sq[i] for i in range(3)}) == 1)

# ---------------- l4 ----------------
lv.claim([gen(100, lambda u: u / 2 + 10, n) for n in (2, 3, 4)] == [60, 40, 30], 'l4 s0: 100, 60, 40, 30')
lv.expect("l4", "screens[1].widget.answer", two('l4 s1', 10 / (1 - 0.5), gen(100, lambda u: u / 2 + 10, 60)))
lv.expect("l4", "screens[2].widget.answer", two('l4 s2', gen(5, lambda u: 2 * u - 3, 4), 3 + 2 ** 3 * (5 - 3)))
lv.expect("l4", "screens[2].widget.wrong[1].value", 2 * 3 - 3)
# wrong[2] "order": subtract 3 before doubling, applied as a rule, gives 4, 2, -2, so u4 = -2 (4 is u2)
lv.expect("l4", "screens[2].widget.wrong[2].value", gen(5, lambda u: 2 * (u - 3), 4))
lv.expect("l4", "screens[2].widget.wrong[3].value", gen(5, lambda u: 2 * u - 3, 5))
lv.expect("l4", "screens[3].widget.options[2].why", 4 * 7 + 3)
L4 = 12 / (1 - 0.6)
lv.expect("l4", "screens[4].widget.answer", two('l4 s4', L4, gen(0.0, lambda u: 0.6 * u + 12, 200)))
t10 = gen(0.0, lambda u: 0.6 * u + 12, 10)
lv.claim(abs(t10 - 29.6) <= 0.2 and t10 < 30, f'l4 s4: term 10 = {t10:.4f}, inside the "last" band 29.6 +- 0.2')
lv.expect("l4", "screens[4].feedback.byKey.divide", 0.6 * 20 + 12)
lv.claim([gen(12, lambda u: 2 * u - 10, n) - 10 for n in range(1, 6)] == [2, 4, 8, 16, 32], 'l4 s5: gaps from 10 double')
lv.expect("l4", "screens[6].widget.answer", two('l4 s6', gen(4, lambda u: 3 * u - 1, 3), 0.5 + 3 ** 2 * (4 - 0.5)))
lv.expect("l4", "screens[6].widget.wrong[0].value", 3 * 2 - 1)
lv.expect("l4", "screens[6].widget.wrong[2].value", 3 * (3 * 4) - 1)
b2 = gen(5000.0, lambda b: 1.01 * b - 200, 3)
lv.expect("l4", "screens[8].widget.answer", two('l4 s8', r2(b2), r2(20000 - 15000 * 1.01 ** 2)))
lv.expect("l4", "screens[8].widget.wrong[1].value", 5000 + 2 * 50 - 400)
lv.expect("l4", "screens[8].widget.wrong[2].value", r2(gen(5000.0, lambda b: 1.01 * (b - 200), 3)))
lv.expect("l4", "screens[9].widget.answer", two('l4 s9', 200 / 0.01, 200 / (1.01 - 1)))
lv.expect("l4", "screens[9].widget.wrong[1].value", 200 / 0.1)
lv.expect("l4", "screens[9].widget.wrong[2].value", 200 / 0.001)
lv.claim(abs(gen(15000.0, lambda b: 1.01 * b - 200, 5) - 14796.98) < 0.01, 'l4 s9: lo4 point 14796.98')
lv.expect("l4", "quiz[0].widget.answer", two('l4 q0', gen(2, lambda u: u + 6, 4), arith(2, 6, 4)))
lv.expect("l4", "quiz[1].widget.answer", two('l4 q1', 4 / 0.5, gen(0.0, lambda u: 0.5 * u + 4, 80)))
lv.expect("l4", "quiz[1].feedback.byKey.add", 0.5 * 4 + 4)
lv.expect("l4", "quiz[2].widget.answer", gen(3, lambda u: 2 * u + 1, 3))
lv.expect("l4", "quiz[3].feedback.correct", 1 / (1 - 0.9))
# "must lie between -1 and 1 for terms to settle": a start at the fixed point settles for any multiplier (l4 s1 says so)
lv.stated("l4", "quiz[3].explain.text", "must lie between", gen(10, lambda u: 2 * u - 10, 20) != 10)

# ---------------- review-1 ----------------
lv.expect("review", "items[0].widget.answer", arith(31, -5, 5))
lv.expect("review", "items[1].widget.options[0].text", 12 + 8)
lv.expect("review", "items[1].widget.options[0].text", 12 * 3)
lv.claim(all(12 - 3 * (n - 1) == 15 - 3 * n for n in range(1, 9)), 'review-1 i2: 15 - 3n')
lv.expect("review", "items[3].widget.answer", two('r1 i3', math.log(486 / 2, 3) + 1, next(n for n in range(1, 20) if 2 * 3 ** (n - 1) == 486)))
lv.expect("review", "items[4].widget.answer", gen(20, lambda u: 0.5 * u + 6, 3))
lv.expect("review", "items[4].explain.text", 6 / 0.5)
lv.expect("review", "items[5].widget.answer", two('r1 i5', 5 / 0.25, gen(0.0, lambda u: 0.75 * u + 5, 300)))
lv.expect("review", "items[5].widget.wrong[1].value", round(5 / 0.75, 4))
lv.expect("review", "items[6].widget.answer", two('r1 i6', round(geom(50, -0.8, 4), 6), round(gen(50, lambda u: -0.8 * u, 4), 6)))
lv.expect("review", "items[6].widget.wrong[1].value", round(geom(50, -0.8, 5), 6))
m = next(n for n in range(1, 100) if arith(350, 125, n) > 2000)
lv.expect("review", "items[7].widget.answer", two('r1 i7', m, math.floor((2000 - 350) / 125) + 2))
lv.expect("review", "items[7].feedback.byKey.m14", arith(350, 125, 14))
lv.expect("review", "items[7].widget.wrong[1].value", 2000 / 125)
y = next(n for n in range(1, 50) if 0.80 * 1.04 ** (n - 1) > 1)
lv.expect("review", "items[8].widget.answer", two('r1 i8', y, math.ceil(math.log(1 / 0.8) / math.log(1.04)) + 1))
lv.expect("review", "items[8].widget.accept", round(0.80 * 1.04 ** 6, 4))
lv.expect("review", "items[8].widget.wrong[1].value", next(n for n in range(1, 50) if 0.80 + 0.032 * (n - 1) > 1))

# ---------------- homework-1 ----------------
lv.claim(all(21 - 4 * n == arith(17, -4, n) for n in range(1, 9)), 'homework-1 i0: 21 - 4n')
lv.claim(all(abs(96 * 0.5 ** (n - 1) - 192 / 2 ** n) < 1e-12 for n in range(1, 9)), 'homework-1 i1: 96 x 0.5^(n-1) = 192/2^n')
lv.expect("homework", "items[2].widget.answer", 11 + 5)
d = (2 - 23) / (11 - 4)
lv.expect("homework", "items[3].widget.answer", two('h1 i3', 2 + 9 * d, 23 + 16 * d))
lv.expect("homework", "items[3].widget.wrong[0].value", 2 + 10 * d)
lv.expect("homework", "items[3].widget.wrong[1].value", 2 + 8 * d)
r = round((324 / 12) ** (1 / 3))
lv.expect("homework", "items[4].widget.answer", two('h1 i4', 324 * r ** 2, geom(12 / r, r, 7)))
lv.expect("homework", "items[4].widget.wrong[0].value", 324 * r ** 3)
lv.expect("homework", "items[4].widget.wrong[1].value", 324 * r)
lv.expect("homework", "items[4].widget.wrong[2].value", 324 + 2 * (324 - 12) / 3)
b3 = gen(12000.0, lambda b: 1.005 * b - 150, 4)
lv.expect("homework", "items[5].widget.answer", two('h1 i5', r2(b3), r2(30000 - 18000 * 1.005 ** 3)))
lv.expect("homework", "items[5].widget.accept", r2(gen(12000.0, lambda b: 1.005 * b - 150, 3)))
lv.expect("homework", "items[5].widget.wrong[1].value", 12000 + 3 * 60 - 450)
A = lambda n: 10000 + 300 * n; Bp = lambda n: 10000 * 1.02 ** n
mo = next(n for n in range(1, 200) if Bp(n) > A(n))
lv.expect("homework", "items[7].widget.answer", mo)
lv.expect("homework", "items[7].widget.accept", r2(Bp(40)))
lv.expect("homework", "items[7].feedback.byKey.before", r2(Bp(39)))
lv.expect("homework", "items[7].feedback.byKey.before", r2(A(39) - Bp(39)))
g = next(n for n in range(1, 100) if Bp(n - 1) * 0.02 > 300)
lv.expect("homework", "items[7].widget.wrong[0].value", g)
lv.expect("homework", "items[7].feedback.byKey.gain", r2(A(g) - Bp(g)))
lv.expect("homework", "items[8].model", r2(gen(10000.0, lambda b: 1.01 * b - 120, 4)))
lv.expect("homework", "items[8].model", two('h1 i8 B12', r2(12000 - 2000 * 1.01 ** 12), r2(gen(10000.0, lambda b: 1.01 * b - 120, 13))))
lv.expect("homework", "items[8].model", 120 / 0.01)

lv.claim(not bad, 'every number agrees by both methods', '; '.join(bad))
lv.check_wrongs()
lv.report()
