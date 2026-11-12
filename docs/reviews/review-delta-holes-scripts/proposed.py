"""Delta read: the numbers of every fix the review proposes, each by two routes.
<scratchpad>/venv/bin/python docs/reviews/review-delta-holes-scripts/proposed.py      (from the repo root)"""
import math
from fractions import Fraction as F

import sympy as sp

n = 0


def ok(c, msg):
    global n
    n += 1
    assert c, msg
    print('ok  ', msg)


def prob(o):
    return o / (1 + o)


# finding 2: e-odds-update on a new setting (an order's fill probability)
odds0 = F(2, 5) / F(3, 5)
odds1 = float(odds0) * math.exp(-0.6 * 2)
p1 = prob(odds1)
p1b = 1 / (1 + math.exp(-(math.log(0.4 / 0.6) - 1.2)))
ok(abs(p1 - p1b) < 1e-12 and round(p1, 3) == 0.167, f'fill: probability 3 ticks away {p1:.5f}, 16.7%')
ok(round(float(odds0), 3) == 0.667 and round(math.exp(-1.2), 3) == 0.301 and round(odds1, 3) == 0.201, f'fill: odds 0.667 x 0.301 = {odds1:.4f}')
r = 0.667 * 0.301
ok(abs(prob(r) - 0.167) <= 0.0015, 'fill: the rounded figures land inside a band of 0.0015 about 0.167')
w = {'prob-times': 0.4 * math.exp(-1.2), 'odds-as-prob': odds1, 'sign': prob(float(odds0) * math.exp(1.2)), 'one-tick': prob(float(odds0) * math.exp(-0.6))}
print('     wrong values:', {k: round(v, 3) for k, v in w.items()})
ok({k: round(v, 3) for k, v in w.items()} == {'prob-times': 0.12, 'odds-as-prob': 0.201, 'sign': 0.689, 'one-tick': 0.268}, 'fill: wrong values 0.120, 0.201, 0.689, 0.268')
vals = [0.167] + [round(v, 3) for v in w.values()]
ok(all(abs(a - b) > 0.004 for i, a in enumerate(vals) for b in vals[i + 1:]), 'fill: every band (0.0015 and 0.002) is clear of the others')

# finding 3: e-diameter-ends on the 8-15-17 triangle
A, B = (-7, -9), (9, 21)
C = (F(A[0] + B[0], 2), F(A[1] + B[1], 2))
ok(C == (1, 6), 'circle: centre (1, 6)')
r2 = (A[0] - 1) ** 2 + (A[1] - 6) ** 2
ok(r2 == 289 == 17 ** 2 == (B[0] - 1) ** 2 + (B[1] - 6) ** 2 and (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2 == 34 ** 2 == 1156, 'circle: radius 17, r squared 289, diameter 34, 34 squared 1,156')
x, y = sp.symbols('x y')
ok(sp.expand((x - 1) ** 2 + (y - 6) ** 2 - 289) == x ** 2 + y ** 2 - 2 * x - 12 * y - 252, 'circle: accept form x^2 + y^2 - 2x - 12y - 252 = 0')

# finding 5: two-by-two, the slip of dividing by the observed counts
a, b, c, d = 62, 68, 16, 56
N = a + b + c + d
gap = abs(a * d - b * c) / N
obs = gap ** 2 * (1 / a + 1 / b + 1 / c + 1 / d)
E = [(a + b) * (a + c) / N, (a + b) * (b + d) / N, (c + d) * (a + c) / N, (c + d) * (b + d) / N]
ok(abs(obs - sum((o - e) ** 2 / o for o, e in zip([a, b, c, d], E))) < 1e-9, f'two-by-two: sum of (O - E)^2/O is gap^2 (1/a + 1/b + 1/c + 1/d) = {obs:.3f} for the table 62, 68, 16, 56')

# finding 8: p-disk-failures part 5, the smallest n
ok(min(k for k in range(3, 1000) if F(k - 2, k) >= F(99, 100)) == 200, 'disk: smallest n is 200')
print(f'proposed: {n} checks, all passed')
