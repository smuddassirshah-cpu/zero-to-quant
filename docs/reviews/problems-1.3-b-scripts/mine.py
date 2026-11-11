"""Second read, problems 1.3 (b): the reader's own answers and named-slip values for the taylor and multivar sets 1 to 3.

Each numeric part was solved from its text before its answer was read. MINE holds, per part, the reader's value of the answer and of
each wrong[] entry (the value the slip its feedback names gives). Exact values come from sympy (Rational, diff, solve); a second route
(mpmath at 30 digits, a brute-force scan, a Newton loop, an enumeration) is checked beside it under "second route" and "claims".
The content is then read: the answer must sit inside its own band around MINE, and each wrong value inside that entry's own band.
A check that fails because the content is wrong stays failing.

Run from the repo root with the scratchpad venv python. Exit 0 when every check holds.
"""
import json
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
R = sp.Rational
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def near(a, b, tol, msg):
    ok(abs(float(a) - float(b)) <= tol, f'{msg}: {float(a)!r} against {float(b)!r} (tol {tol})')


x, y, w, k, n = sp.symbols('x y w k n')

# ---------------------------------------------------------------- taylor 1
cb = x ** R(1, 3)
f2 = sp.diff(cb, x, 2).subs(x, 27)                       # -2/2187
L = lambda v: 3 + (v - 27) / R(27)
err = R(1, 2) * f2 * R(81, 100) ** 2                     # -3/10000 exactly
nf = x ** 3 + x - 3
step = lambda v, f=nf: v - f.subs(x, v) / sp.diff(f, x).subs(x, v)
x1 = step(sp.Integer(1)); x2 = step(x1); x3 = step(x2)
root = sp.nsolve(nf, 1.2, prec=30)
flows = {1: 3, 2: 3, 3: 3, 4: 103}
P = lambda yv, fl=flows: sum(c / (1 + yv) ** t for t, c in fl.items())
dP = lambda yv, fl=flows: -sum(t * c / (1 + yv) ** (t + 1) for t, c in fl.items())
d2P = lambda yv, fl=flows: sum(t * (t + 1) * c / (1 + yv) ** (t + 2) for t, c in fl.items())
y4 = R(4, 100)
loan = {1: 3700, 2: 3700, 3: 3700}
y5 = R(5, 100)
V5 = P(y5, loan); dV5 = dP(y5, loan)
y1_ = R(5, 100) + R(7602, 100) / R(1888040, 100)

MINE = {
    ('taylor', 1, 'p-cube-root-27', 2): (L(R(2781, 100)), {'ninth': 3 + R(81, 100) / 9, 'third': 3 + R(81, 100) / 3, 'whole-x': 3 + R(2781, 100) / 27}),
    ('taylor', 1, 'p-cube-root-27', 3): (err, {'no-half': 2 * err, 'h-not-squared': R(1, 2) * f2 * R(81, 100), 'sign': -err}),
    ('taylor', 1, 'p-cube-root-27', 4): (R(303, 100) + err, {'sign': R(303, 100) - err, 'no-half': R(303, 100) + 2 * err, 'ninth-carried': R(309, 100) + err}),
    ('taylor', 1, 'p-newton-cubic', 1): (x1, {'sign': 1 + R(-1, 4), 'no-plus-one': 1 + R(1, 3), 'no-step': 1}),
    ('taylor', 1, 'p-newton-cubic', 2): (x2, {'sign': x1 + nf.subs(x, x1) / (3 * x1 ** 2 + 1), 'no-plus-one': x1 - nf.subs(x, x1) / (3 * x1 ** 2)}),
    ('taylor', 1, 'p-newton-cubic', 4): (x3, {'sign': x2 + (x2 - x3), 'no-plus-one': x2 - nf.subs(x, x2) / (3 * x2 ** 2), 'stop': x2}),
    ('taylor', 1, 'p-loss-limit', 1): (P(y4), {'par': 100, 'face-only': 103 / R(104, 100) ** 4, 'no-discount': 112}),
    ('taylor', 1, 'p-loss-limit', 2): (dP(y4), {'no-t': -sum(c / R(104, 100) ** (t + 1) for t, c in flows.items()),
                                                'power-t': -sum(t * c / R(104, 100) ** t for t, c in flows.items()), 'positive': -dP(y4)}),
    ('taylor', 1, 'p-loss-limit', 3): (R(35443, 100) * R(1, 10000) * 40000, {'one-lot': R(35443, 100) / 10000, 'hundredfold': R(35443, 100) * R(1, 100) * 40000,
                                                                               'price-not-slope': R(9637, 100) * R(1, 10000) * 40000}),
    ('taylor', 1, 'p-loss-limit', 4): (50000 / R(141772, 100), {'hundredfold': 50000 / R(141772), 'price-not-slope': 50000 / R(38548, 100)}),
    ('taylor', 1, 'p-loan-rate', 1): (V5, {'no-discount': 11100, 'one-year': 11100 / R(105, 100), 'last-only': 3700 / R(105, 100) ** 3}),
    ('taylor', 1, 'p-loan-rate', 2): (dV5, {'no-t': -sum(3700 / R(105, 100) ** (t + 1) for t in (1, 2, 3)),
                                            'power-t': -sum(t * 3700 / R(105, 100) ** t for t in (1, 2, 3)), 'positive': -dV5}),
    ('taylor', 1, 'p-loan-rate', 3): (R(1888040, 100) / R(1007602, 100), {'upside-down': R(1007602) / R(1888040), 'macaulay': R(105, 100) * R(1888040) / R(1007602),
                                                                          'negative': -R(1888040) / R(1007602)}),
    ('taylor', 1, 'p-loan-rate', 4): (y1_, {'sign': R(1, 10) - y1_, 'step-only': y1_ - R(5, 100)}),
    ('taylor', 1, 'p-loan-rate', 5): (R(5403, 100000) + R(41, 100) / R(1864289, 100), {'sign': R(5403, 100000) - R(41, 100) / R(1864289, 100),
                                                                                       'step-only': R(41, 100) / R(1864289, 100), 'stop': R(5403, 100000)}),
}

# ---------------------------------------------------------------- taylor 2
th = x ** R(3, 2)
c2 = sp.diff(th, x, 2).subs(x, 4) / 2
c3 = sp.diff(th, x, 3).subs(x, 4) / 6
h = R(4, 10)
Q = 8 + 3 * h + c2 * h ** 2
sg = (1 - x) ** -2
b8 = {1: 8, 2: 8, 3: 8, 4: 108}
y7 = R(7, 100)
P7 = R(10339, 100); D7 = R(33502, 10000); C7 = R(1506, 100); dy = R(15, 1000)
dur = P7 * (1 - D7 * dy)
est2 = sum(R(1, 2) ** j / j for j in range(1, 6))
lx = sp.log(x)
l2, l3 = sp.diff(lx, x, 2).subs(x, 2) / 2, sp.diff(lx, x, 3).subs(x, 2) / 6
e2 = R(68854, 100000)
cubic = lambda base, a2=l2, a3=l3: base + R(1, 2) * R(1, 10) + a2 * R(1, 100) + a3 * R(1, 1000)
MINE.update({
    ('taylor', 2, 'p-three-halves', 1): (sp.diff(th, x).subs(x, 4), {'no-root': R(3, 2), 'up-power': R(3, 2) * 4 ** R(5, 2)}),
    ('taylor', 2, 'p-three-halves', 2): (c2, {'no-half': 2 * c2, 'root-up': R(3, 4) * 2 / 2}),
    ('taylor', 2, 'p-three-halves', 3): (Q, {'no-half': 8 + 3 * h + 2 * c2 * h ** 2, 'root-up': 8 + 3 * h + R(3, 4) * h ** 2, 'tangent': 8 + 3 * h}),
    ('taylor', 2, 'p-three-halves', 4): (c3, {'no-factorial': 6 * c3, 'divide-three': 2 * c3, 'sign': -c3}),
    ('taylor', 2, 'p-three-halves', 5): (Q + c3 * h ** 3, {'divide-three': Q + 2 * c3 * h ** 3, 'no-factorial': Q + 6 * c3 * h ** 3, 'sign': Q - c3 * h ** 3}),
    ('taylor', 2, 'p-square-geometric', 1): (sp.diff(sg, x, 3).subs(x, 0), {'geometric': sp.diff(1 / (1 - x), x, 3).subs(x, 0), 'sign': -24}),
    ('taylor', 2, 'p-square-geometric', 2): (4, {'no-factorial': 24, 'divide-three': 8, 'geometric': 1}),
    ('taylor', 2, 'p-square-geometric', 5): (sum((j + 1) * R(1, 10) ** j for j in range(4)), {'c3-24': 1 + R(2, 10) + R(3, 100) + R(24, 1000),
                                             'geometric': sum(R(1, 10) ** j for j in range(4)), 'k-only': sum(j * R(1, 10) ** j for j in range(4))}),
    ('taylor', 2, 'p-eight-coupon', 1): (P(y7, b8), {'par': 100, 'face-only': 108 / R(107, 100) ** 4, 'no-discount': 132}),
    ('taylor', 2, 'p-eight-coupon', 2): (d2P(y7, b8), {'power-t': sum(t * (t + 1) * c / R(107, 100) ** t for t, c in b8.items()),
                                                       't-squared': sum(t * t * c / R(107, 100) ** (t + 2) for t, c in b8.items()),
                                                       'one-term': 20 * 108 / R(107, 100) ** 6}),
    ('taylor', 2, 'p-eight-coupon', 3): (R(155743, 100) / P7, {'power-t': R(178310, 100) / P7, 't-squared': R(123372, 100) / P7, 'upside-down': P7 / R(155743, 100)}),
    ('taylor', 2, 'p-eight-coupon', 4): (dur, {'sign': P7 * (1 + D7 * dy), 'percent': P7 * (1 - D7 * R(3, 2)), 'no-price': P7 - D7 * dy}),
    ('taylor', 2, 'p-eight-coupon', 5): (R(9819, 100) + R(1, 2) * C7 * P7 * dy ** 2, {'subtract': R(9819, 100) - R(1, 2) * C7 * P7 * dy ** 2,
                                         'no-half': R(9819, 100) + C7 * P7 * dy ** 2, 'not-squared': R(9819, 100) + R(1, 2) * C7 * P7 * dy}),
    ('taylor', 2, 'p-log-two', 2): (est2, {'four-terms': est2 - R(1, 160), 'alternating': sum((-1) ** (j + 1) * R(1, 2) ** j / j for j in range(1, 6)),
                                           'x-one': sum(R((-1) ** (j + 1), j) for j in range(1, 6))}),
    ('taylor', 2, 'p-log-two', 3): (l2, {'no-half': 2 * l2, 'centre-one': R(-1, 2), 'sign': -l2}),
    ('taylor', 2, 'p-log-two', 4): (l3, {'no-factorial': 6 * l3, 'divide-three': 2 * l3, 'centre-one': R(1, 3)}),
    ('taylor', 2, 'p-log-two', 5): (cubic(e2), {'no-cubic': cubic(e2) - l3 / 1000, 'no-half': cubic(e2, 2 * l2), 'four-terms': cubic(R(68229, 100000)),
                                                'x-one': cubic(R(78333, 100000))}),
})

# ---------------------------------------------------------------- taylor 3
c = lambda m: R(2 ** m, m ** 2)
r8 = R(8, 100); r5 = R(-5, 100)
b2 = r8 ** 3 / 3 * 10 ** 5
M4 = 2 / R(95, 100) ** 3
b4 = M4 * R(5, 100) ** 3 / 6 * 10 ** 5
T3 = 1 + R(4, 10) + R(4, 10) ** 2 / 2 + R(4, 10) ** 3 / 6
a4 = R(4, 10) ** 4 / 24
ln14 = sum((-1) ** (j + 1) * R(4, 10) ** j / j for j in range(1, 5))
MINE.update({
    ('taylor', 3, 'p-doubling-coefficients', 1): (c(5) / c(4), {'upside-down': c(4) / c(5), 'no-square': 2 * R(4, 5), 'powers-only': 2}),
    ('taylor', 3, 'p-doubling-coefficients', 2): (sp.limit(2 * n ** 2 / (n + 1) ** 2, n, sp.oo), {'lost-two': 1, 'radius': R(1, 2), 'part-one': c(5) / c(4)}),
    ('taylor', 3, 'p-doubling-coefficients', 3): (R(1, 2), {'no-flip': 2, 'one': 1}),
    ('taylor', 3, 'p-doubling-coefficients', 4): (R(8, 10) / (1 - R(8, 10)), {'from-zero': 1 / (1 - R(8, 10)), 'first-term': R(8, 10), 'flipped': 1 / R(8, 10)}),
    ('taylor', 3, 'p-two-months', 1): (r8 - r8 ** 2 / 2, {'no-half': r8 - r8 ** 2, 'plus': r8 + r8 ** 2 / 2, 'just-r': r8}),
    ('taylor', 3, 'p-two-months', 2): (b2, {'factorial': b2 / 2, 'no-divide': 3 * b2, 'kept-term': r8 ** 2 / 2 * 10 ** 5, 'unscaled': b2 / 10 ** 5}),
    ('taylor', 3, 'p-two-months', 3): (r5 - r5 ** 2 / 2, {'sign': r5 + r5 ** 2 / 2, 'just-r': r5, 'no-half': r5 - r5 ** 2}),
    ('taylor', 3, 'p-two-months', 4): (b4, {'wrong-end': 2 * R(5, 100) ** 3 / 6 * 10 ** 5, 'two-factorial': 3 * b4, 'no-m': R(5, 100) ** 3 / 6 * 10 ** 5, 'unscaled': b4 / 10 ** 5}),
    ('taylor', 3, 'p-two-months', 5): (R(1707, 100) + R(486, 100), {'subtracted': R(1707, 100) - R(486, 100), 'wrong-end': R(1707, 100) + R(417, 100),
                                                                     'first-only': R(1707, 100), 'unscaled': R(2193, 100) / 10 ** 5}),
    ('taylor', 3, 'p-tail-bound', 1): (T3, {'quadratic': T3 - R(4, 10) ** 3 / 6, 'cube-over-three': T3 + R(4, 10) ** 3 / 6, 'no-half': T3 + R(4, 10) ** 2 / 2}),
    ('taylor', 3, 'p-tail-bound', 2): (R(3, 2) * a4, {'m-one': a4, 'power-three': R(3, 2) * R(4, 10) ** 3 / 6, 'no-factorial': R(3, 2) * R(4, 10) ** 4}),
    ('taylor', 3, 'p-tail-bound', 3): (R(4, 10) / 5, {'over-four': R(1, 10), 'x-only': R(4, 10), 'upside-down': 5 / R(4, 10)}),
    ('taylor', 3, 'p-tail-bound', 4): (a4 / (1 - R(8, 100)) * 10 ** 4, {'first-term': a4 * 10 ** 4, 'over-four': a4 / (1 - R(1, 10)) * 10 ** 4,
                                                                        'lagrange': 16, 'unscaled': a4 / (1 - R(8, 100))}),
    ('taylor', 3, 'p-tail-bound', 5): (R(1490667, 10 ** 6) + R(11594, 10 ** 7), {'lagrange': R(1490667, 10 ** 6) + R(16, 10 ** 4), 'lower': T3 + a4,
                                                                                'over-four': T3 + a4 / (1 - R(1, 10))}),
    ('taylor', 3, 'p-big-gain', 1): (sp.limit(R(18, 10) * n / (n + 1), n, sp.oo), {'upside-down': 1 / R(18, 10), 'radius': 1}),
    ('taylor', 3, 'p-big-gain', 2): (ln14, {'three-terms': ln14 + R(4, 10) ** 4 / 4, 'all-plus': sum(R(4, 10) ** j / j for j in range(1, 5)),
                                            'factorials': sum((-1) ** (j + 1) * R(4, 10) ** j / sp.factorial(j) for j in range(1, 5))}),
    ('taylor', 3, 'p-big-gain', 3): (R(4, 10) ** 5 / 5, {'last-kept': R(4, 10) ** 4 / 4, 'factorial': R(4, 10) ** 5 / 120, 'no-divide': R(4, 10) ** 5}),
    ('taylor', 3, 'p-big-gain', 4): (R(693147, 10 ** 6) + R(334933, 10 ** 6), {'three-terms': R(693147, 10 ** 6) + R(341333, 10 ** 6),
                                                                              'multiplied': R(693147, 10 ** 6) * R(334933, 10 ** 6), 'simple': R(18, 10)}),
})

# ---------------------------------------------------------------- multivar 1
bowl = 9 * x ** 2 + y ** 2
ynew = sp.sqrt(18 - 9 * R(101, 100) ** 2)
mb = x ** 3 * y - 2 * x * y ** 2
at = lambda e, a, b: e.subs({x: a, y: b})
Pp, X = sp.symbols('P X')
Vh = 2000 * Pp / X
td = {Pp: 50, X: R(5, 4)}
VP, VX = sp.diff(Vh, Pp).subs(td), sp.diff(Vh, X).subs(td)
VPX = sp.diff(Vh, Pp, X).subs(td)
MINE.update({
    ('multivar', 1, 'p-stretched-bowl', 1): (at(bowl, 1, 3), {'no-square-y': 9 + 3, 'swapped': 1 + 9 * 9}),
    ('multivar', 1, 'p-stretched-bowl', 3): (-R(18) * R(1, 100) / 6, {'sign': R(3, 100), 'inverted': -R(6) * R(1, 100) / 18, 'rise-in-f': R(18, 100)}),
    ('multivar', 1, 'p-stretched-bowl', 4): (ynew - 3, {'linear': R(-3, 100), 'no-square': sp.sqrt(18 - 9 * R(101, 100)) - 3, 'no-subtract': ynew}),
    ('multivar', 1, 'p-mixed-both-ways', 3): (at(sp.diff(mb, y, x), 2, 1), {'xx': at(sp.diff(mb, x, 2), 2, 1), 'yy': at(sp.diff(mb, y, 2), 2, 1), 'sign': 12 + 4}),
    ('multivar', 1, 'p-mixed-both-ways', 4): (at(sp.diff(mb, x), 2, 1), {'sign': 12 + 2, 'f-y': at(sp.diff(mb, y), 2, 1)}),
    ('multivar', 1, 'p-mixed-both-ways', 5): (10 + 8 * R(1, 10), {'used-xx': 10 + 12 * R(1, 10), 'used-yy': 10 - 8 * R(1, 10), 'change-only': R(8, 10)}),
    ('multivar', 1, 'p-dollar-holding', 1): (VP, {'times-x': 2000 * R(5, 4), 'no-x': 2000}),
    ('multivar', 1, 'p-dollar-holding', 2): (VX, {'sign': -VX, 'no-square': -100000 / R(5, 4)}),
    ('multivar', 1, 'p-dollar-holding', 3): (VP * R(1, 2) + VX * R(1, 100), {'sign': VP * R(1, 2) - VX * R(1, 100), 'price-only': VP * R(1, 2), 'carried': VP * R(1, 2) - 80000 * R(1, 100)}),
    ('multivar', 1, 'p-dollar-holding', 5): (sp.diff(Vh, Pp, 2).subs(td) * R(1, 2) + VPX * R(1, 100), {'sign': -VPX / 100, 'no-rate': VPX, 'used-vx': VX / 100}),
})

# ---------------------------------------------------------------- multivar 2
sa = x ** 2 * y
gx, gy = at(sp.diff(sa, x), 3, 2), at(sp.diff(sa, y), 3, 2)
norm = sp.sqrt(gx ** 2 + gy ** 2)
u = (R(-4, 5), R(3, 5))
sig = sp.sqrt(x ** 2 + y ** 2)
sx, sy = at(sp.diff(sig, x), 3, 4), at(sp.diff(sig, y), 3, 4)
plane = lambda a, b: 5 + sx * (a - 3) + sy * (b - 4)
true1 = sp.sqrt(R(32, 10) ** 2 + R(37, 10) ** 2)
first = lambda r0, fac, lim: next(j for j in range(1, 200) if abs(r0) * fac ** j < lim)
MINE.update({
    ('multivar', 2, 'p-slopes-around', 2): (norm, {'added': gx + gy, 'no-root': norm ** 2}),
    ('multivar', 2, 'p-slopes-around', 3): (gx * u[0] + gy * u[1], {'not-unit': gx * -4 + gy * 3, 'reversed': -(gx * u[0] + gy * u[1])}),
    ('multivar', 2, 'p-slopes-around', 5): (sp.deg(sp.acos(R(15, 2) / norm)), {'sine': sp.deg(sp.asin(R(1, 2))), 'obtuse': sp.deg(sp.acos(R(-1, 2)))}),
    ('multivar', 2, 'p-two-book-risk', 3): (plane(R(32, 10), R(37, 10)), {'exact': true1, 'no-shift': 5 + sx * R(32, 10) + sy * R(37, 10), 'unit-slopes': 5 + R(2, 10) - R(3, 10),
                                                                        'carried': 6 * R(32, 10) + 8 * R(37, 10) - 45}),
    ('multivar', 2, 'p-two-book-risk', 4): (true1 - R(488, 100), {'sign': R(488, 100) - true1, 'squares': R(2393, 100) - R(488, 100) ** 2}),
    ('multivar', 2, 'p-two-book-risk', 5): (R(118, 10000) / 4, {'halved': R(118, 10000) / 2, 'same': R(118, 10000), 'cube': R(118, 10000) / 8}),
    ('multivar', 2, 'p-fit-descent', 3): (R(8, 10) * R(16, 10) - 2, {'linear': R(-4, 10) - R(1, 10) * 4, 'plus-two': R(8, 10) * R(16, 10)}),
    ('multivar', 2, 'p-fit-descent', 4): (min(sp.solve(sp.Eq(1 - 8 * x, -1), x)[0], sp.solve(sp.Eq(1 - 2 * x, -1), x)[0]), {'b-only': 1, 'no-zigzag': R(1, 8)}),
    ('multivar', 2, 'p-fit-descent', 5): (max(first(1, R(2, 10), R(1, 100)), first(2, R(8, 10), R(1, 100))), {'used-a': first(1, R(2, 10), R(1, 100)), 'one-short': 23,
                                                                                                        'start-one': first(1, R(8, 10), R(1, 100))}),
})

# ---------------------------------------------------------------- multivar 3
tl = 2 * x ** 3 - 6 * x * y + 3 * y ** 2
Dd = sp.diff(tl, x, 2) * sp.diff(tl, y, 2) - sp.diff(tl, x, y) ** 2
Pr = 14 * x + 6 * y - x ** 2 - y ** 2
lam = sp.symbols('lam')
con = lambda cap: sp.solve([sp.diff(Pr, x) - lam, sp.diff(Pr, y) - lam, x + y - cap], [x, y, lam], dict=True)[0]
s6 = con(6)
var = R(9, 100) * w ** 2 + R(4, 100) * (1 - w) ** 2 + 2 * R(1, 4) * R(3, 10) * R(2, 10) * w * (1 - w)
wmin = sp.solve(sp.diff(var, w), w)[0]
vmin = var.subs(w, wmin)
nocross = R(9, 100) * w ** 2 + R(4, 100) * (1 - w) ** 2
w1, w2 = sp.symbols('w1 w2')
v2 = R(9, 100) * w1 ** 2 + R(4, 100) * w2 ** 2 + R(3, 100) * w1 * w2
lamv = sp.diff(v2, w1).subs({w1: R(1, 4), w2: R(3, 4)})
MINE.update({
    ('multivar', 3, 'p-two-level-points', 3): (Dd.subs(x, 0), {'plus': 36, 'no-mixed': 0, 'no-square': 0 - (-6)}),
    ('multivar', 3, 'p-two-level-points', 5): (at(tl, 1, 1), {'plus-xy': 2 + 6 + 3, 'origin': at(tl, 0, 0)}),
    ('multivar', 3, 'p-capital-limit', 3): (s6[x], {'scaled': 7 * R(6, 10), 'even': 3, 'free': 7}),
    ('multivar', 3, 'p-capital-limit', 4): (s6[lam], {'sign': -s6[lam], 'value': Pr.subs(s6)}),
    ('multivar', 3, 'p-capital-limit', 5): (50 + s6[lam] * R(1, 2), {'full-lambda': 50 + s6[lam], 'no-lambda': 50 + R(1, 2), 'sign': 50 - s6[lam] * R(1, 2)}),
    ('multivar', 3, 'p-min-variance-pair', 2): (wmin, {'no-two': R(5, 100) / R(1, 10), 'gave-b': 1 - wmin, 'carried': sp.solve(sp.diff(nocross, w), w)[0]}),
    ('multivar', 3, 'p-min-variance-pair', 3): (sp.sqrt(vmin), {'variance': vmin, 'weighted': R(1, 4) * R(3, 10) + R(3, 4) * R(2, 10), 'carried-half': sp.sqrt(var.subs(w, R(1, 2)))}),
    ('multivar', 3, 'p-min-variance-pair', 4): (lamv, {'variance': vmin, 'no-cross': R(18, 100) * R(1, 4)}),
    ('multivar', 3, 'p-min-variance-pair', 5): (vmin + lamv * R(2, 100), {'sigma-lambda': vmin + vmin * R(2, 100), 'no-change': vmin, 'whole-lambda': vmin + lamv}),
})

# ---------------------------------------------------------------- read the content against MINE
seen = set()
for course in ('taylor', 'multivar'):
    for s in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{course}/problems-{s}.json'))
        for it in d['items']:
            for i, p in enumerate(it['parts'], 1):
                wd = p['widget']
                if wd['kind'] != 'numeric' or 'answers' in wd:
                    continue
                key = (course, s, it['id'], i)
                ok(key in MINE, f'{key}: no reader value')
                if key not in MINE:
                    continue
                seen.add(key)
                mine, slips = MINE[key]
                tol = wd['tol'].get('abs', 0) + 1e-9
                near(wd['answer'], mine, tol, f'{key} answer')
                ids = {e['id'] for e in wd.get('wrong', [])}
                ok(ids == set(slips), f'{key}: wrong ids {sorted(ids)} against reader {sorted(slips)}')
                for e in wd.get('wrong', []):
                    if e['id'] in slips:
                        near(e['value'], slips[e['id']], e.get('tol', {}).get('abs', 0) + 1e-9, f'{key} wrong {e["id"]}')
                        ok(abs(float(slips[e['id']]) - float(mine)) > tol, f'{key} wrong {e["id"]}: reader slip value inside the answer band')
ok(seen == set(MINE), 'a reader value has no part')

# ---------------------------------------------------------------- second route and claims in prose, feedback, explanations
# taylor 1
near(mp.cbrt(mp.mpf('27.81')), 3.02970, 5e-6, 'cube root of 27.81 is 3.02970 to 5 places')
near(mp.cbrt(mp.mpf('27.81')) - mp.mpf('3.03'), -0.0003, 5e-6, 'true error of the tangent against the predicted -0.0003')
ok(x2 == R(17, 14) and nf.subs(x, x2) == R(13, 2744) and sp.diff(nf, x).subs(x, x2) == R(1063, 196), 'x2 = 17/14, f = 13/2744, f\' = 1063/196')
near(x1 - root, 0.037, 5e-4, 'Newton error 1'); near(x2 - root, 0.00087, 5e-6, 'Newton error 2'); near(x3 - root, 0.0000005, 5e-8, 'Newton error 3')
near(root, 1.213412, 5e-7, 'the root to 6 places')
ok(1 < root < x3 < x2 < x1, 'x0 = 1 is below the root; x1, x2, x3 are above it: the first step crossed the root')
for t_, pv, dd in ((1, 2.8846, 2.7737), (2, 2.7737, 5.3340), (3, 2.6670, 7.6932), (4, 88.0448, 338.6338)):
    near(flows[t_] / 1.04 ** t_, pv, 5e-5, f'loss-limit PV {t_}'); near(t_ * flows[t_] / 1.04 ** (t_ + 1), dd, 5e-5, f'loss-limit slope term {t_}')
loss = lambda bp: 40000 * float(P(y4) - P(y4 + R(bp, 10000)))
near(loss(R(353, 10)), 49600, 60, 'true loss at 35.3 bp is about 49,600')
bp_true = mp.findroot(lambda b: 40000 * (mp.mpf(float(P(y4))) - sum(c_ / (1.04 + b / 10000) ** t_ for t_, c_ in flows.items())) - 50000, 35.5)
near(bp_true, 35.6, 0.05, 'the limit is reached near 35.6 bp')
near(float(P(y4) - P(y4 + R(35, 10000))), 1.25, 0.02, 'a lot loses about 1.25 on 35 bp')
for t_, df, tm in ((1, 0.952381, 0.907029), (2, 0.907029, 1.727675), (3, 0.863838, 2.468108)):
    near(1.05 ** -t_, df, 5e-7, f'loan DF {t_}'); near(t_ / 1.05 ** (t_ + 1), tm, 5e-7, f'loan slope term {t_}')
near(P(R(5403, 100000), loan), 10000.41, 0.005, 'V(0.05403) = 10,000.41')
near(dP(R(5403, 100000), loan), -18642.89, 0.02, 'V\'(0.05403) = -18,642.89')
irr = mp.findroot(lambda r: 3700 / (1 + r) + 3700 / (1 + r) ** 2 + 3700 / (1 + r) ** 3 - 10000, 0.05)
near(irr, 0.054052, 6e-7, 'the loan rate to 6 places')
ok(float(y1_) < irr, 'the first Newton step fell short of the rate')
# taylor 2
near(mp.mpf('4.4') ** 1.5, 9.22952, 5e-6, '4.4^1.5')
ok(sp.simplify(sp.diff(sg, x, k).subs(x, 0) - sp.factorial(k + 1)) == 0 or all(sp.diff(sg, x, j).subs(x, 0) == sp.factorial(j + 1) for j in range(8)), 'f^(k)(0) = (k+1)!')
near(1 / 0.81, 1.234568, 5e-7, '1/0.81'); near(sum((j + 1) * (-0.5) ** j for j in range(200)), 1 / 2.25, 1e-9, 'series at -0.5 gives 1/2.25')
near(-dP(y7, b8) / P(y7, b8), 3.3502, 5e-5, 'modified duration 3.3502')
for t_, pv, cc in ((1, 7.4766, 13.0608), (2, 6.9875, 36.6190), (3, 6.5304, 68.4467), (4, 82.3927, 1439.2992)):
    near(b8[t_] / 1.07 ** t_, pv, 5e-5, f'eight-coupon PV {t_}'); near(t_ * (t_ + 1) * b8[t_] / 1.07 ** (t_ + 2), cc, 5e-5, f'eight-coupon bend term {t_}')
near(P(R(85, 1000), b8), 98.36, 0.005, 'true price at 8.5% is 98.36')
near(float(P(R(85, 1000), b8)) - 98.19, 0.17, 0.006, 'duration alone is 17p out')
near(mp.log(2), 0.6931, 5e-5, 'ln 2'); near(mp.log('2.1'), 0.74194, 5e-6, 'ln 2.1'); near(mp.log(2) - mp.mpf('0.68854'), 0.0046, 5e-5, 'error in ln 2')
# taylor 3
near((mp.log('1.08') - mp.mpf('0.0768')) * 1e5, 16.10, 0.005, 'true error, +8% month')
near((mp.mpf('-0.05125') - mp.log('0.95')) * 1e5, 4.33, 0.005, 'true error, -5% month')
near(mp.log(mp.mpf('1.08') * mp.mpf('0.95')), 0.025668, 5e-7, 'two-month log return')
near((mp.log(mp.mpf('1.026')) - mp.mpf('0.02555')) * 1e5, 11.8, 0.05, 'two-month gap')
near(mp.e ** mp.mpf('0.4'), 1.49182, 5e-6, 'e^0.4'); near((mp.e ** mp.mpf('0.4') - mp.mpf(float(T3))) * 1e4, 11.58, 0.005, 'true tail')
ok(float(T3 + a4) <= float(mp.e ** mp.mpf('0.4')) <= float(T3) + 0.0011594 and mp.e ** mp.mpf('0.4') < 1.5, 'the two bounds hold and e^c < 1.5')
near(mp.log('1.4'), 0.336472, 5e-7, 'ln 1.4'); near(mp.log('1.4') - mp.mpf(float(ln14)), 0.00154, 5e-6, 'ln 1.4 gap')
near(mp.log('2.8'), 1.029619, 5e-7, 'ln 2.8'); near(mp.nsum(lambda j: 1 / j ** 2, [1, mp.inf]), mp.pi ** 2 / 6, 1e-12, 'sum 1/n^2 converges')
ok(float(mp.nsum(lambda j: mp.mpf('0.8') ** j / j ** 2, [1, mp.inf])) < 4, 'series at 0.4 is below 4')
# multivar 1
near(float(ynew), 2.9697, 5e-5, 'new y'); near(at(sp.diff(mb, x), 2, R(11, 10)), 10.78, 1e-9, 'f_x(2, 1.1)')
ok(sp.diff(mb, x, y) == sp.diff(mb, y, x), 'mixed partials agree'); ok(Vh.subs(td) == 80000 and VPX == -1280, 'V = 80,000 and V_PX = -1,280')
# multivar 2
ok(gx * R(6, 10) - gy * R(8, 10) == 0, 'contour arrow'); near(sp.sqrt(R(31, 10) ** 2 + R(385, 100) ** 2) - plane(R(31, 10), R(385, 100)), 0.0029, 5e-5, 'true half-step error')
near(float(sp.sqrt(R(31, 10) ** 2 + R(385, 100) ** 2)), 4.9429, 5e-5, 'true risk, half step'); ok(plane(R(31, 10), R(385, 100)) == R(494, 100), 'plane, half step')
near(0.8 ** 23, 0.0059, 5e-5, '0.8^23'); near(0.8 ** 24, 0.0047, 5e-5, '0.8^24'); near(2 * 0.8 ** 23, 0.0118, 5e-5, '2 x 0.8^23'); near(2 * 0.8 ** 24, 0.0094, 5e-5, '2 x 0.8^24')
# multivar 3
ok(sp.solve([sp.diff(tl, x), sp.diff(tl, y)], [x, y]) == [(0, 0), (1, 1)], 'stationary points'); ok(sp.expand(Dd) == 72 * x - 36, 'D')
ok(Pr.subs({x: 7, y: 3}) == 58 and Pr.subs(s6) == 50 and Pr.subs(con(R(13, 2))) == R(415, 8), 'P = 58, 50 and 51.875')
grid = max(((14 * a / 100 + 6 * (6.5 - a / 100) - (a / 100) ** 2 - (6.5 - a / 100) ** 2), a / 100) for a in range(0, 651))
near(grid[0], 51.875, 1e-9, 'grid search on x + y = 6.5'); near(grid[1], 5.25, 1e-9, 'grid search x')
ok(sp.expand(var) == R(1, 10) * w ** 2 - R(1, 20) * w + R(1, 25), 'variance quadratic'); ok(lamv == 2 * vmin, 'lambda = twice the variance')
near(vmin * R(102, 100) ** 2, 0.0351, 5e-5, 'exact smallest variance at budget 1.02')

print(f'mine.py: {len(MINE)} numeric parts, {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
