"""Delta read of the fix passes of problems 1.3 a and b: every changed answer,
band and `wrong` value recomputed by two routes (exact with sympy or
fractions, then numerically: a loop, a difference quotient, mpmath, a grid),
and compared with the file. Also, for every numeric part of the nine changed
files: no `wrong` value inside the answer band, no two bands that meet, a
`byKey` line for every `wrong` id.

Run from the repo root with the scratchpad venv: python recompute.py
"""
import json
import math
import sys
from fractions import Fraction as F

import mpmath as mp
import numpy as np
import sympy as sp

checks = fails = 0


def chk(name, cond, detail=''):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', name, detail)


def close(a, b, eps=1e-9):
    return abs(float(a) - float(b)) <= eps


SETS = {}


def part(course, n, iid, k):
    key = (course, n)
    if key not in SETS:
        SETS[key] = json.load(open(f'app/content/courses/{course}/problems-{n}.json'))
    it = [i for i in SETS[key]['items'] if i['id'] == iid][0]
    return it['parts'][k - 1]


def band(v, tol):
    t = tol.get('abs', 0)
    return float(v) - t - 1e-9, float(v) + t + 1e-9


def inside(x, v, tol):
    lo, hi = band(v, tol)
    return lo <= float(x) <= hi


def numeric(course, n, iid, k, exact, second, wrong, key_places=None, takes=(), refuses=()):
    """exact and second: the answer by two routes. wrong: {id: (route 1, route 2)}.
    key_places: the stored key is the answer rounded to this many places (None: stored to full precision).
    takes / refuses: values the band must accept / refuse."""
    w = part(course, n, iid, k)['widget']
    where = f'{course} {n} {iid} part {k}'
    chk(where + ' two routes agree', close(exact, second, 1e-7), f'{float(exact)} {float(second)}')
    key = float(w['answer'])
    if key_places is None:
        chk(where + ' key', close(key, exact, 1e-9), f'{key} {float(exact)}')
    else:
        chk(where + ' key', close(key, round(float(exact), key_places), 1e-12), f'{key} {float(exact)}')
    chk(where + ' wrong ids', sorted(x['id'] for x in w.get('wrong', [])) == sorted(wrong), str([x['id'] for x in w.get('wrong', [])]))
    for x in w.get('wrong', []):
        if x['id'] not in wrong:
            continue
        a, b = wrong[x['id']]
        chk(f'{where} wrong {x["id"]} two routes', close(a, b, 1e-7), f'{float(a)} {float(b)}')
        chk(f'{where} wrong {x["id"]} value holds the slip', inside(a, x['value'], x['tol']), f'{x["value"]} {float(a)}')
        chk(f'{where} wrong {x["id"]} outside the answer band', not inside(a, key, w['tol']) and not inside(x['value'], key, w['tol']))
    for v in takes:
        chk(f'{where} takes {v}', inside(v, key, w['tol']))
    for v in refuses:
        chk(f'{where} refuses {v}', not inside(v, key, w['tol']))


# ---------------------------------------------------------------- limits 2, p-perpetuity-slope part 2
P = lambda r: F(5) / r
ex = (P(F(49, 1000)) - 100) / (F(49, 1000) - F(50, 1000))
nu = (5 / 0.049 - 5 / 0.05) / (0.049 - 0.05)
four = (round(5 / 0.049, 4) - 100) / -0.001      # P kept to 4 places, as the question now says
penny = (round(5 / 0.049, 2) - 100) / -0.001     # P kept to the penny
numeric('limits', 2, 'p-perpetuity-slope', 2, ex, nu,
        {'sign': (-ex, -nu), 'no-divide': (P(F(49, 1000)) - 100, 5 / 0.049 - 100)}, key_places=2,
        takes=(four, round(four), penny, -2041, -2040, -2040.82, -2040.8), refuses=(-2042, -2039, 2041, 2040.82, 2, -2000, -2500))
chk('perpetuity routes', round(four) == -2041 and round(penny) == -2040, f'{four} {penny}')

# ---------------------------------------------------------------- limits 3, p-relative-strength
t = sp.symbols('t')
Pt, It = 30 * sp.exp(sp.Rational(7, 100) * t), 1500 * sp.exp(sp.Rational(5, 100) * t)
R = Pt / It
dq = lambda f, h=1e-6: (f(h) - f(-h)) / (2 * h)
p_ = lambda x: 30 * math.exp(0.07 * x)
i_ = lambda x: 1500 * math.exp(0.05 * x)
chk('R(0)', R.subs(t, 0) == sp.Rational(1, 50))
numeric('limits', 3, 'p-relative-strength', 1, sp.diff(Pt, t).subs(t, 0), dq(p_),
        {'no-chain': (Pt.subs(t, 0), p_(0)), 'no-thirty': (sp.Rational(7, 100), 0.07)}, takes=(2.1, 2.10))
chk("I'(0)", sp.diff(It, t).subs(t, 0) == 75 and close(dq(i_), 75, 1e-5))
u, du, v, dv = 30, F(21, 10), 1500, 75
numeric('limits', 3, 'p-relative-strength', 2, sp.diff(R, t).subs(t, 0), dq(lambda x: p_(x) / i_(x)),
        {'swapped': ((u * dv - du * v) / F(v * v), -dq(lambda x: p_(x) / i_(x))),
         'no-square': ((du * v - u * dv) / v, 900 / 1500),
         'rates': (du / dv, 2.1 / 75),
         'no-chain': ((30 * v - u * dv) / F(v * v), (30 * 1500 - 30 * 75) / 1500 ** 2)},
        takes=(0.0004, F(900, 2250000)))
chk('quotient top', du * v - u * dv == 900 and du * v == 3150 and u * dv == 2250)
g = sp.diff(sp.log(R), t)
numeric('limits', 3, 'p-relative-strength', 3, sp.simplify(g), dq(lambda x: math.log(p_(x) / i_(x))),
        {'added': (F(7, 100) + F(5, 100), 0.07 + 0.05), 'raw': (F(4, 10000), 0.0004),
         'share-only': (F(7, 100), 0.07), 'decimal': (F(2, 100) / 100, 0.02 / 100)})

# ---------------------------------------------------------------- integrals 1, p-falling-parabola
x, n, k = sp.symbols('x n k', positive=True)
f = 12 - 3 * x ** 2
fn = lambda z: 12 - 3 * z * z
hs = [f.subs(x, sp.Rational(j, 2)) for j in (1, 2, 3, 4)]
chk('heights', hs == [sp.Rational(45, 4), 9, sp.Rational(21, 4), 0], str(hs))
R4 = sum(hs) / 2
L4 = sum(f.subs(x, sp.Rational(j, 2)) for j in (0, 1, 2, 3)) / 2
r4n = sum(fn(0.5 * j) for j in (1, 2, 3, 4)) * 0.5
l4n = sum(fn(0.5 * j) for j in (0, 1, 2, 3)) * 0.5
numeric('integrals', 1, 'p-falling-parabola', 1, R4, r4n, {'left-ends': (L4, l4n), 'no-width': (sum(hs), r4n / 0.5)}, takes=(12.75,))
gap = abs(f.subs(x, 2) - f.subs(x, 0)) * sp.Rational(2, 4)
chk('gap 6', gap == 6 and L4 - R4 == 6)
numeric('integrals', 1, 'p-falling-parabola', 2, R4 + gap, l4n,
        {'subtracted': (R4 - gap, r4n - 6), 'no-length': (R4 + 12 * sp.Rational(1, 4), r4n + 3)}, takes=(18.75,))
smallest = min(m for m in range(1, 1000) if F(24, m) <= F(1, 10))
strict = min(m for m in range(1, 1000) if F(24, m) < F(1, 10))
nolen = min(m for m in range(1, 1000) if F(12, m) <= F(1, 10))
numeric('integrals', 1, 'p-falling-parabola', 3, smallest, sp.ceiling(sp.Rational(24) / sp.Rational(1, 10)),
        {'no-length': (nolen, 120), 'strict': (strict, 241)}, refuses=(239, 241))
Rn = sp.simplify(sp.summation(f.subs(x, 2 * k / n) * 2 / n, (k, 1, n)))
Ln = sp.simplify(sp.summation(f.subs(x, 2 * k / n) * 2 / n, (k, 0, n - 1)))
# The file's own TeX for part 4 is graded by the engine in grade.mjs; here the forms are typed by hand.
chk('R_n', sp.simplify(Rn - (16 - 12 / n - 4 / n ** 2)) == 0, str(Rn))
chk('R_n accept forms', sp.simplify(Rn - (16 * n ** 2 - 12 * n - 4) / n ** 2) == 0 and sp.simplify(Rn - (24 - 4 * (n + 1) * (2 * n + 1) / n ** 2)) == 0)
chk('L_n (left-ends)', sp.simplify(Ln - (16 + 12 / n - 4 / n ** 2)) == 0, str(Ln))
chk('no-width', sp.simplify(sp.summation(f.subs(x, 2 * k / n), (k, 1, n)) - (12 * n - 2 * (n + 1) * (2 * n + 1) / n)) == 0)
for m in (1, 4, 10, 240):  # second route: the sums by a loop
    chk(f'R_{m} loop', close(sum(fn(2 * j / m) * 2 / m for j in range(1, m + 1)), Rn.subs(n, m), 1e-9))
    chk(f'L_{m} loop', close(sum(fn(2 * j / m) * 2 / m for j in range(0, m)), Ln.subs(n, m), 1e-9))
chk('R_4 from the formula', Rn.subs(n, 4) == R4)
chk('L_n - R_n = 24/n', sp.simplify(Ln - Rn - 24 / n) == 0)
area = sp.integrate(f, (x, 0, 2))
numeric('integrals', 1, 'p-falling-parabola', 5, sp.limit(Rn, n, sp.oo), float(mp.quad(fn, [0, 2])),
        {'no-squares': (2 * 12, 24.0), 'stopped': (R4, r4n), 'once': (sp.limit(12 - 4 * (n + 1) * (2 * n + 1) / n ** 2, n, sp.oo), 12 - 8)})
chk('area by antiderivative', area == 16)
chk('R_4 < 16 < L_4', R4 < 16 < L4)

# ---------------------------------------------------------------- integrals 2, p-turnover-decay parts 3, 4
T = lambda z: 16 - 16 * math.exp(-0.5 * z)
tt = sp.symbols('tt')
ex = sp.integrate(8 * sp.exp(-tt / 2), (tt, 0, 4))
numeric('integrals', 2, 'p-turnover-decay', 3, ex, float(mp.quad(lambda z: 8 * mp.e ** (-0.5 * z), [0, 4])),
        {'no-c': (-16 * sp.exp(-2), -16 * math.exp(-2)), 'times-k': (4 - 4 * sp.exp(-2), -4 * math.exp(-2) + 4),
         'rate': (8 * sp.exp(-2), 8 * math.exp(-2))},
        takes=(13.83, 13.84, 13.8352, 16 - 2.17, 13.835), refuses=(13.82, 13.85, 13.76, 13.8))
numeric('integrals', 2, 'p-turnover-decay', 4, 2 * sp.log(4), float(mp.findroot(lambda z: T(z) - 12, 2)),
        {'divided': (sp.log(4) / 2, math.log(4) / 2), 'wrong-share': (-2 * sp.log(sp.Rational(3, 4)), -2 * math.log(0.75))}, takes=(2.77,))

# ---------------------------------------------------------------- integrals 3
s = lambda z: z * math.exp(-z * z / 8)
T2 = 2 * (0.5 * s(0) + s(2) + 0.5 * s(4))
T2x = 2 * (sp.Integer(0) + 2 * sp.exp(-sp.Rational(1, 2)) + 2 * sp.exp(-2))
numeric('integrals', 3, 'p-signal-average', 4, T2x, T2,
        {'full-ends': (2 * (2 * sp.exp(-sp.Rational(1, 2)) + 4 * sp.exp(-2)), 2 * (s(0) + s(2) + s(4))),
         'no-h': (T2x / 2, T2 / 2), 'midpoint': (2 * (sp.exp(-sp.Rational(1, 8)) + 3 * sp.exp(-sp.Rational(9, 8))), 2 * (s(1) + s(3)))},
        takes=(2.967, 2.968, 2.9675, 2 * (1.2131 + 0.2707), 2 * (1.21306 + 0.27067), 2 * (1.213 + 0.2705)), refuses=(2.966, 2.969, 2.97, 3.0))
chk('signal printed figures', round(s(2), 4) == 1.2131 and round(s(4), 4) == 0.5413 and round(s(2), 5) == 1.21306 and round(s(4) / 2, 5) == 0.27067)
ex = sp.integrate(tt * sp.exp(-tt ** 2 / 8), (tt, 0, 4))
numeric('integrals', 3, 'p-signal-average', 2, ex, float(mp.quad(s, [0, 4])), {'x-limits': (4 - 4 * sp.exp(-4), 4 - 4 * math.exp(-4)),
        'quarter': (ex / 16, float(mp.quad(s, [0, 4])) / 16), 'sign': (-ex, -float(mp.quad(s, [0, 4])))}, takes=(3.459,))
numeric('integrals', 3, 'p-signal-average', 3, ex / 4, float(mp.quad(s, [0, 4])) / 4, {'no-divide': (ex, 3.4586588670535), 'halved': (ex / 2, 3.4586588670535 / 2),
        'x-limits': (1 - sp.exp(-4), 1 - math.exp(-4))}, takes=(0.865,))
lnx = lambda z: math.log(z)
Tl = 0.5 * (0.5 * lnx(0.5) + lnx(1) + 0.5 * lnx(1.5))
Tlx = sp.Rational(1, 2) * (sp.log(sp.Rational(1, 2)) / 2 + sp.log(sp.Rational(3, 2)) / 2)
numeric('integrals', 3, 'p-log-return', 1, Tlx, Tl,
        {'full-ends': (sp.Rational(1, 2) * (sp.log(sp.Rational(1, 2)) + sp.log(sp.Rational(3, 2))), 0.5 * (lnx(0.5) + lnx(1.5))),
         'midpoint': (sp.Rational(1, 2) * (sp.log(sp.Rational(3, 4)) + sp.log(sp.Rational(5, 4))), 0.5 * (lnx(0.75) + lnx(1.25))),
         'lost-strip': (sp.Rational(1, 2) * sp.log(sp.Rational(1, 2)) / 2, 0.5 * 0.5 * lnx(0.5))},
        takes=(-0.0719, -0.0720, -0.07195, 0.5 * (-0.3466 + 0.2027), 0.5 * (-0.34657 + 0.20273)), refuses=(-0.0718, -0.0721, -0.072 - 0.0001))
chk('log-return printed figures', round(0.5 * lnx(0.5), 5) == -0.34657 and round(0.5 * lnx(1.5), 5) == 0.20273)
chk('log-return part 3 stands', abs(abs(Tl - float(sp.integrate(sp.log(x), (x, sp.Rational(1, 2), sp.Rational(3, 2))))) - 0.0267) < 5e-5)
numeric('integrals', 3, 'p-order-size-tail', 4, sp.sqrt(99), float(mp.findroot(lambda q: 1 / (1 + q * q) - 0.01, 9)),
        {'drop-one': (10, 10.0), 'no-root': (99, 99.0), 'wrong-tail': (sp.sqrt(sp.Rational(1, 99)), math.sqrt(1 / 0.99 - 1))}, takes=(9.95,))
numeric('integrals', 3, 'p-time-to-fill', 2, 3 * sp.exp(-2), float(mp.quad(lambda z: z * mp.e ** (-z), [2, mp.inf])),
        {'dropped-x': (sp.exp(-2), math.exp(-2)), 'dropped-one': (2 * sp.exp(-2), 2 * math.exp(-2)),
         'complement': (1 - 3 * sp.exp(-2), float(mp.quad(lambda z: z * mp.e ** (-z), [0, 2])))}, takes=(0.406,))

# ---------------------------------------------------------------- taylor 1, p-cube-root-27 (the fourth root about 16)
fx = x ** sp.Rational(1, 4)
a = 16
slope = sp.diff(fx, x).subs(x, a)
chk('slope 1/32', slope == sp.Rational(1, 32) and close(dq(lambda h_: (16 + h_) ** 0.25), 1 / 32, 1e-8))
L = lambda z: 2 + (z - 16) * F(1, 32)
numeric('taylor', 1, 'p-cube-root-27', 2, L(F(1632, 100)), 2 + 0.32 / 32,
        {'eighth': (2 + F(32, 100) / 8, 2.04), 'quarter': (2 + F(32, 100) / 4, 2.08), 'whole-x': (2 + F(1632, 100) / 32, 2 + 16.32 / 32)},
        takes=(2.01, 2.0100))
f2 = sp.diff(fx, x, 2).subs(x, a)
chk("f''(16)", f2 == -sp.Rational(3, 2048))
h = sp.Rational(32, 100)
err = f2 * h ** 2 / 2
d2 = (17 ** 0.25 - 2 * 2 + 15 ** 0.25)  # second difference, step 1: a rough check on the size and sign of f''
chk("f'' by a second difference", abs(d2 - float(f2)) < 2e-5 and d2 < 0, str(d2))
mp.mp.dps = 30
true = mp.mpf('16.32') ** mp.mpf('0.25')
numeric('taylor', 1, 'p-cube-root-27', 3, err, -0.5 * 3 / 2048 * 0.32 ** 2,
        {'no-half': (f2 * h ** 2, -3 / 2048 * 0.1024), 'h-not-squared': (f2 * h / 2, -0.5 * 3 / 2048 * 0.32), 'sign': (-err, 0.000075)},
        takes=(-0.000075,), refuses=(-0.000074, -0.000076, -0.00008, -0.0001))
chk('true error is near the prediction', abs(float(true - mp.mpf('2.01')) - float(err)) < 1e-6, str(true - mp.mpf('2.01')))
numeric('taylor', 1, 'p-cube-root-27', 4, L(F(1632, 100)) + F(-75, 1000000), 2.01 - 0.000075,
        {'sign': (F(201, 100) + F(75, 1000000), 2.010075), 'no-half': (F(201, 100) - F(15, 100000), 2.00985),
         'eighth-carried': (F(204, 100) - F(75, 1000000), 2.039925)}, takes=(2.009925,), refuses=(2.009926, 2.0099, 2.01))
chk('true value 2.009926 to 6 places', mp.nstr(true, 7) == '2.009926', mp.nstr(true, 12))
chk('corrected estimate within 0.000001', abs(true - mp.mpf('2.009925')) < mp.mpf('0.000001'), mp.nstr(true - mp.mpf('2.009925'), 5))

# taylor 1: printed terms, and the one-lot band
terms = [tt_ * c / 1.04 ** (tt_ + 1) for tt_, c in ((1, 3), (2, 3), (3, 3), (4, 103))]
chk('loss-limit terms', [round(z, 4) for z in terms] == [2.7737, 5.3340, 7.6932, 338.6340], str(terms))
chk('loss-limit sum', round(sum(terms), 2) == 354.43 and round(2.7737 + 5.3340 + 7.6932 + 338.6340, 2) == 354.43)
y = sp.symbols('y')
Pb = sum(3 / (1 + y) ** j for j in (1, 2, 3)) + 103 / (1 + y) ** 4
chk('loss-limit slope by sympy', abs(float(sp.diff(Pb, y).subs(y, sp.Rational(4, 100))) + sum(terms)) < 1e-9)
onelot = sum(terms) * 0.0001
w = part('taylor', 1, 'p-loss-limit', 3)['widget']
ol = [z for z in w['wrong'] if z['id'] == 'one-lot'][0]
chk('one-lot holds its value', inside(onelot, ol['value'], ol['tol']) and inside(0.04, ol['value'], ol['tol']) and inside(0.035, ol['value'], ol['tol']))
chk('one-lot refuses 0.35, 0.14 and the price slip', not any(inside(z, ol['value'], ol['tol']) for z in (0.35, 0.14, 0.0096, 0.01, 0.1)))
chk('one-lot misses the slip rounded to the nearest pound (finding)', not inside(0, ol['value'], ol['tol']))
terms = [j / 1.05 ** (j + 1) for j in (1, 2, 3)]
chk('loan-rate terms', [round(z, 6) for z in terms] == [0.907029, 1.727675, 2.468107] and round(sum(terms), 5) == 5.10281, str(terms))
chk('loan-rate slope', round(-3700 * sum(terms), 2) == -18880.40)

# taylor 1, p-newton-cubic part 3: the reworded `why`
fc = lambda z: z ** 3 + z - 3
fc1 = lambda z: 3 * z * z + 1
root = float(mp.findroot(fc, 1.2))
x0 = 1.0
x1 = x0 - fc(x0) / fc1(x0)
x2 = x1 - fc(x1) / fc1(x1)
chk('newton: the step from x0 crosses the root, the step from x1 does not', x0 < root < x2 < x1, f'{root} {x1} {x2}')
grid = np.linspace(0.5, 2, 301)
for b in (x0, x1):
    chk(f'newton: tangent at {b} lies under the curve', all(fc(z) - (fc(b) + fc1(b) * (z - b)) >= -1e-12 for z in grid))
chk('newton: from the right no step crosses', all((z - fc(z) / fc1(z)) >= root - 1e-12 for z in np.linspace(root, 2, 200)))
chk('newton: from the left every step crosses', all((z - fc(z) / fc1(z)) >= root - 1e-12 for z in np.linspace(0.6, root, 200)))

# ---------------------------------------------------------------- taylor 3
r = sp.Rational(8, 100)
b1 = r ** 3 / 3
numeric('taylor', 3, 'p-two-months', 2, b1 * 10 ** 5, 0.08 ** 3 / 3 * 1e5,
        {'factorial': (r ** 3 / 6 * 10 ** 5, 0.08 ** 3 / 6 * 1e5), 'no-divide': (r ** 3 * 10 ** 5, 51.2),
         'kept-term': (r ** 2 / 2 * 10 ** 5, 320.0), 'unscaled': (b1, 0.08 ** 3 / 3)}, key_places=2, takes=(17.1, 17.07, 17.067), refuses=(17.0, 17.2, 16.1))
e1 = mp.log(mp.mpf('1.08')) - mp.mpf('0.0768')
e2 = mp.log(mp.mpf('0.95')) + mp.mpf('0.05125')
chk('true errors +16.10 and -4.33', mp.nstr(e1 * 1e5, 4) == '16.1' and round(float(e1) * 1e5, 2) == 16.10 and round(float(e2) * 1e5, 2) == -4.33, f'{e1} {e2}')
M = 2 / sp.Rational(95, 100) ** 3
b2 = M * sp.Rational(5, 100) ** 3 / 6
Mn = max(2 / (1 + z) ** 3 for z in np.linspace(-0.05, 0, 501))
numeric('taylor', 3, 'p-two-months', 4, b2 * 10 ** 5, Mn * 0.05 ** 3 / 6 * 1e5,
        {'wrong-end': (2 * sp.Rational(5, 100) ** 3 / 6 * 10 ** 5, 2 * 0.05 ** 3 / 6 * 1e5),
         'two-factorial': (M * sp.Rational(5, 100) ** 3 / 2 * 10 ** 5, Mn * 0.05 ** 3 / 2 * 1e5),
         'no-m': (sp.Rational(5, 100) ** 3 / 6 * 10 ** 5, 0.05 ** 3 / 6 * 1e5), 'unscaled': (b2, Mn * 0.05 ** 3 / 6)},
        key_places=2, takes=(4.86, 4.85, 2.33 * 0.000125 / 6 * 1e5, 2.3327 * 0.000125 / 6 * 1e5, 4.87), refuses=(4.84, 4.88, 4.17, 4.33, 4.9))
chk('Lagrange bound holds the true error', abs(e2) < float(b2) and abs(e1) < float(b1))
numeric('taylor', 3, 'p-two-months', 5, sp.Rational(1707, 100) + sp.Rational(486, 100), 17.07 + 4.86,
        {'subtracted': (sp.Rational(1707, 100) - sp.Rational(486, 100), 17.07 - 4.86), 'wrong-end': (sp.Rational(1707, 100) + sp.Rational(417, 100), 17.07 + 4.17),
         'first-only': (sp.Rational(1707, 100), 17.07), 'unscaled': (sp.Rational(2193, 10 ** 7), 21.93e-5)},
        takes=(21.9, 21.93, float((b1 + b2) * 10 ** 5)), refuses=(21.8, 22.0, 17.1, 12.2, 11.8))
tot = mp.log(mp.mpf('1.08') * mp.mpf('0.95'))
chk('two-month figures', mp.nstr(tot, 5) == '0.025668' and round(float(tot - mp.mpf('0.02555')) * 1e5, 1) == 11.8 and abs(e1 + e2 - (tot - mp.mpf('0.02555'))) < 1e-20)
chk('with the signs the total is out by less than the larger bound', 0 < float(e1 + e2) < float(b1))
for kk, vals in ((2, (0.0001707, 0.000171, 0.00017, float(b1))), (4, (0.0000486, 0.00004860, 0.000049, float(b2), 0.0000485)), (5, (0.0002193, 0.000219, 0.00022))):
    w = part('taylor', 3, 'p-two-months', kk)['widget']
    un = [z for z in w['wrong'] if z['id'] == 'unscaled'][0]
    for v in vals:
        chk(f'two-months part {kk} unscaled takes {v}', inside(v, un['value'], un['tol']))
    others = [float(z['value']) * 1e-5 for z in w['wrong'] if z['id'] != 'unscaled'] + [0, 0.00001, 0.0001, 0.001, 0.0000853, 0.0000417, 0.000512, 0.0032, 0.0001221]
    for v in others:
        chk(f'two-months part {kk} unscaled refuses {v}', not inside(v, un['value'], un['tol']))
a4 = sp.Rational(4, 10) ** 4 / 24
tail = a4 / (1 - sp.Rational(8, 100))
series = sum(float(a4) * 0.08 ** j for j in range(200))
true_tail = mp.e ** mp.mpf('0.4') - (1 + mp.mpf('0.4') + mp.mpf('0.08') + mp.mpf('0.064') / 6)
numeric('taylor', 3, 'p-tail-bound', 4, tail * 10 ** 4, series * 1e4,
        {'first-term': (a4 * 10 ** 4, 0.0256 / 24 * 1e4), 'over-four': (a4 / (1 - sp.Rational(1, 10)) * 10 ** 4, 0.0256 / 24 / 0.9 * 1e4),
         'lagrange': (sp.Rational(3, 2) * a4 * 10 ** 4, 1.5 * 0.0256 / 24 * 1e4), 'unscaled': (tail, series)},
        key_places=3, takes=(11.59, 11.60, 10.67 / 0.92, 10.667 / 0.92, 11.594), refuses=(11.58, 11.61, float(true_tail) * 1e4, 11.6 + 0.005))
chk('true error 11.58', round(float(true_tail) * 1e4, 2) == 11.58 and float(true_tail) < float(tail))
w = part('taylor', 3, 'p-tail-bound', 4)['widget']
un = [z for z in w['wrong'] if z['id'] == 'unscaled'][0]
chk('tail unscaled takes its forms', all(inside(v, un['value'], un['tol']) for v in (0.0011594, 0.001159, 0.00116, float(tail))))
chk('tail unscaled refuses the other slips unscaled', not any(inside(v, un['value'], un['tol']) for v in (0.0010667, 0.0011852, 0.0016, 0.0011, 0.0012, 0.001158 - 0.000005)))

# ---------------------------------------------------------------- multivar 3, p-min-variance-pair
wv = sp.symbols('w')
sa, sb, rho = sp.Rational(40, 100), sp.Rational(25, 100), sp.Rational(3, 10)
var = sa ** 2 * wv ** 2 + sb ** 2 * (1 - wv) ** 2 + 2 * rho * sa * sb * wv * (1 - wv)
chk('prose formula', sp.expand(var - (sp.Rational(16, 100) * wv ** 2 + sp.Rational(625, 10000) * (1 - wv) ** 2 + sp.Rational(6, 100) * wv * (1 - wv))) == 0)
quad = sp.expand(var)
chk('quadratic', sp.expand(quad - (sp.Rational(1625, 10000) * wv ** 2 - sp.Rational(65, 1000) * wv + sp.Rational(625, 10000))) == 0, str(quad))
chk('quadratic accept form', sp.expand(quad - (13 * wv ** 2 / 80 - 13 * wv / 200 + sp.Rational(1, 16))) == 0)
chk('no-cross', sp.expand(sa ** 2 * wv ** 2 + sb ** 2 * (1 - wv) ** 2 - (sp.Rational(2225, 10000) * wv ** 2 - sp.Rational(125, 1000) * wv + sp.Rational(625, 10000))) == 0)
chk('half-cross', sp.expand(sa ** 2 * wv ** 2 + sb ** 2 * (1 - wv) ** 2 + rho * sa * sb * wv * (1 - wv) - (sp.Rational(1925, 10000) * wv ** 2 - sp.Rational(95, 1000) * wv + sp.Rational(625, 10000))) == 0)
# second route: fit a parabola through three computed variances
Sig = np.array([[0.16, 0.3 * 0.4 * 0.25], [0.3 * 0.4 * 0.25, 0.0625]])
pv = lambda z: float(np.array([z, 1 - z]) @ Sig @ np.array([z, 1 - z]))
co = np.polyfit([0, 0.5, 1], [pv(0), pv(0.5), pv(1)], 2)
chk('quadratic by a fit', np.allclose(co, [0.1625, -0.065, 0.0625]))
wstar = sp.solve(sp.diff(quad, wv), wv)[0]
gridw = np.linspace(0, 1, 100001)
wgrid = gridw[np.argmin([pv(z) for z in gridw])]
nocross = sp.expand(sa ** 2 * wv ** 2 + sb ** 2 * (1 - wv) ** 2)
numeric('multivar', 3, 'p-min-variance-pair', 2, wstar, wgrid,
        {'no-two': (sp.Rational(65, 1000) / sp.Rational(1625, 10000), 0.065 / 0.1625), 'gave-b': (1 - wstar, 1 - wgrid),
         'carried': (sp.solve(sp.diff(nocross, wv), wv)[0], 0.125 / 0.445)}, takes=(0.2, 0.20))
vmin = quad.subs(wv, wstar)
chk('variance 0.056', vmin == sp.Rational(56, 1000) and close(pv(0.2), 0.056, 1e-12))
chk('variance terms', sp.Rational(1625, 10000) * wstar ** 2 == sp.Rational(65, 10000) and sp.Rational(65, 1000) * wstar == sp.Rational(13, 1000))
numeric('multivar', 3, 'p-min-variance-pair', 3, sp.sqrt(vmin), math.sqrt(pv(wgrid)),
        {'variance': (vmin, pv(0.2)), 'weighted': (wstar * sa + (1 - wstar) * sb, 0.2 * 0.4 + 0.8 * 0.25),
         'carried-half': (sp.sqrt(quad.subs(wv, sp.Rational(4, 10))), math.sqrt(pv(0.4)))}, key_places=4, takes=(0.2366,), refuses=(0.2367, 0.2365, 0.237, 0.24))
a1, a2, lam = sp.symbols('a1 a2 lam')
V2 = sa ** 2 * a1 ** 2 + sb ** 2 * a2 ** 2 + 2 * rho * sa * sb * a1 * a2
chk('partials', sp.expand(sp.diff(V2, a1) - (sp.Rational(32, 100) * a1 + sp.Rational(6, 100) * a2)) == 0
    and sp.expand(sp.diff(V2, a2) - (sp.Rational(125, 1000) * a2 + sp.Rational(6, 100) * a1)) == 0)
sol = sp.solve([sp.diff(V2, a1) - lam, sp.diff(V2, a2) - lam, a1 + a2 - 1], [a1, a2, lam], dict=True)[0]
chk('Lagrange solution', sol[a1] == sp.Rational(1, 5) and sol[a2] == sp.Rational(4, 5))
lam_n = (0.32 * 0.2 + 0.06 * 0.8, 0.125 * 0.8 + 0.06 * 0.2)
chk('both partials give lambda', close(lam_n[0], lam_n[1], 1e-12) and close(lam_n[1], 0.1 + 0.012, 1e-12) and close(lam_n[0], 0.064 + 0.048, 1e-12))
numeric('multivar', 3, 'p-min-variance-pair', 4, sol[lam], lam_n[0],
        {'variance': (vmin, 0.056), 'no-cross': (sp.Rational(32, 100) * sol[a1], 0.064)}, takes=(0.112,), refuses=(0.11, 0.1))
chk('lambda = 2 variance', sol[lam] == 2 * vmin)
bud = sp.symbols('bud')
solb = sp.solve([sp.diff(V2, a1) - lam, sp.diff(V2, a2) - lam, a1 + a2 - bud], [a1, a2, lam], dict=True)[0]
Vb = sp.simplify(V2.subs({a1: solb[a1], a2: solb[a2]}))
exact = Vb.subs(bud, sp.Rational(102, 100))
gridw = np.linspace(0, 1.02, 102001)
vgrid = min(float(np.array([z, 1.02 - z]) @ Sig @ np.array([z, 1.02 - z])) for z in gridw)
chk('exact smallest variance at 1.02', exact == sp.Rational(56, 1000) * sp.Rational(10404, 10000) and close(vgrid, exact, 1e-9), str(exact))
chk('dV*/dbudget = lambda at 1', sp.diff(Vb, bud).subs(bud, 1) == sol[lam])
numeric('multivar', 3, 'p-min-variance-pair', 5, vmin + sol[lam] * sp.Rational(2, 100), 0.056 + 0.112 * 0.02,
        {'sigma-lambda': (vmin + vmin * sp.Rational(2, 100), 0.056 * 1.02), 'no-change': (vmin, 0.056), 'whole-lambda': (vmin + sol[lam], 0.168)},
        takes=(0.05824, 0.0582, 0.0583, float(exact), 0.05826), refuses=(0.058, 0.0584, 0.0581, 0.06))

# ---------------------------------------------------------------- findings (printed, not failures)
def finding(n_, text, cond):
    global checks
    checks += 1
    if cond:
        print(f'FINDING {n_}: {text}')


p3 = part('taylor', 1, 'p-cube-root-27', 3)
finding(3, "p-cube-root-27 part 3 generic still names the old base point: " + p3['feedback']['generic'], '27' in p3['feedback']['generic'])
f27 = float(sp.diff(fx, x, 2).subs(x, 27))
chk("f''(27) would give an error the band refuses", not inside(0.5 * f27 * 0.1024, -0.000075, {'abs': 5e-7}), str(0.5 * f27 * 0.1024))
p5 = part('multivar', 3, 'p-min-variance-pair', 5)
finding(4, 'p-min-variance-pair part 5 explain prints 0.0582, not the 5-place key 0.05824', '0.05824' not in p5['explain']['text'])
finding(4, 'p-min-variance-pair part 5 feedback prints the exact value as 0.0583 "too"; to 5 places it is ' + str(round(float(exact), 5)), '0.0583$ too' in p5['feedback']['correct'])
for (c_, m_, i_d, k_, edge) in (('integrals', 2, 'p-turnover-decay', 3, 13.82), ('integrals', 3, 'p-log-return', 1, -0.0718), ('integrals', 3, 'p-signal-average', 4, 2.966)):
    w_ = part(c_, m_, i_d, k_)['widget']
    finding(1, f'{i_d} part {k_}: accept line "{w_["accept"]}" holds {edge}, which the band refuses', not inside(edge, w_['answer'], w_['tol']))

# ---------------------------------------------------------------- every numeric part of the nine files: bands and byKey
FILES = [('limits', 2), ('limits', 3), ('integrals', 1), ('integrals', 2), ('integrals', 3),
         ('taylor', 1), ('taylor', 3), ('multivar', 2), ('multivar', 3)]
parts = 0
for course, m in FILES:
    d = json.load(open(f'app/content/courses/{course}/problems-{m}.json'))
    for it in d['items']:
        for j, p in enumerate(it['parts']):
            w = p['widget']
            where = f'{course} {m} {it["id"]} part {j + 1}'
            ids = [z['id'] for z in w.get('wrong', [])]
            chk(where + ' byKey for every wrong id', all(i in p['feedback'].get('byKey', {}) for i in ids), str(ids))
            if w['kind'] != 'numeric' or 'answers' in w:
                continue
            parts += 1
            bands = [('answer',) + band(w['answer'], w['tol'])] + [(z['id'],) + band(z['value'], z['tol']) for z in w.get('wrong', [])]
            for i in range(len(bands)):
                for q in range(i + 1, len(bands)):
                    chk(f'{where} bands {bands[i][0]} / {bands[q][0]} apart', bands[i][2] < bands[q][1] or bands[q][2] < bands[i][1], f'{bands[i]} {bands[q]}')
print(f'bands checked on {parts} numeric parts of 9 files')
print(f'recompute.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
