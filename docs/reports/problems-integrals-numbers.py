"""Recompute every number in app/content/courses/integrals/problems-<n>.json twice.

Method 1 is exact: fractions.Fraction and sympy (closed forms, symbolic sums, limits and integrals).
Method 2 is independent: a fine numerical Riemann sum or scipy quad, a brute-force search, or a
derivative check of an antiderivative. For each numeric part the script checks that the two methods
agree, that the JSON key matches them within its tol, that the value the feedback prints is accepted
by that tol, that every `wrong` value is the slip it names, and (lv.check_wrongs) that each wrong
value lies outside the key's band. Expression parts are parsed from their TeX and compared with
sympy; each wrong form is shown not to be equivalent. Choice parts check the keyed option.
Stated numbers in feedback and explanations are tied to their text with lv.expect.

Run: <scratchpad>/venv/bin/python docs/reports/problems-integrals-numbers.py   (exit 0 when all pass)
"""
import math
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp
from scipy.integrate import quad
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

x, t, n, b = sp.symbols('x t n b', positive=True)
TR = standard_transformations + (implicit_multiplication_application, convert_xor)


# ---------------------------------------------------------------- helpers
def tex2sp(s):
    """Translate the small TeX subset used in these answers into sympy."""
    def frac(s):
        while '\\frac' in s:
            i = s.index('\\frac')
            j = i + 5
            args = []
            for _ in range(2):
                assert s[j] == '{', s
                d, k = 0, j
                while True:
                    d += {'{': 1, '}': -1}.get(s[k], 0)
                    if d == 0:
                        break
                    k += 1
                args.append(s[j + 1:k])
                j = k + 1
            s = s[:i] + f'(({args[0]})/({args[1]}))' + s[j:]
        return s
    s = frac(s)
    s = re.sub(r'e\^\{', ' exp{', s)
    s = s.replace('\\ln', ' log').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict={'x': x, 't': t, 'n': n, 'exp': sp.exp, 'log': sp.log}, transformations=TR)


def W(lv, i, j):
    return lv.files[f'problems-{lv.n}']['items'][i]['parts'][j]['widget']


def num(lv, i, j, exact, second, slips=None, printed=None, agree=1e-7):
    """Numeric part j (0-based) of item i."""
    tag = f'problems-{lv.n} item {i} part {j + 1}'
    w = W(lv, i, j)
    ex = float(exact)
    lv.claim(abs(ex - float(second)) <= agree * max(1, abs(ex)), f'{tag}: two methods agree {ex:.8g} vs {float(second):.8g}')
    tol = w['tol']['abs']
    lv.claim(abs(w['answer'] - ex) <= tol + 1e-12, f'{tag}: key {w["answer"]} matches {ex:.8g} within {tol}')
    if printed is not None:
        lv.claim(abs(printed - w['answer']) <= tol + 1e-12, f'{tag}: printed value {printed} is accepted by the tol')
    slips = slips or {}
    got = {d['id']: d for d in w.get('wrong', [])}
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} all recomputed')
    for k, v in slips.items():
        if k in got:
            wt = got[k]['tol']['abs']
            lv.claim(abs(got[k]['value'] - float(v)) <= max(wt, 1e-9), f'{tag}: wrong "{k}" = {got[k]["value"]} is the slip {float(v):.6g}')


def numset(lv, i, j, roots, second, slips):
    tag = f'problems-{lv.n} item {i} part {j + 1}'
    w = W(lv, i, j)
    lv.claim(sorted(float(r) for r in roots) == sorted(float(r) for r in second), f'{tag}: roots agree')
    lv.claim(sorted(w['answers']) == sorted(float(r) for r in roots), f'{tag}: key {w["answers"]}')
    got = {d['id']: d['value'] for d in w.get('wrong', [])}
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids recomputed')
    for k, v in slips.items():
        vals = sorted(float(a) for a in got[k].split(','))
        lv.claim(vals == sorted(float(a) for a in v) and vals != sorted(w['answers']), f'{tag}: wrong set "{k}" {vals}')


def expr(lv, i, j, exact, integrand=None, var=None, slips=None):
    """Expression part: the JSON answer equals `exact`; with `integrand`, its derivative is the integrand (method 2)."""
    tag = f'problems-{lv.n} item {i} part {j + 1}'
    w = W(lv, i, j)
    key = tex2sp(w['answer'])
    up = w.get('upToConstant', False)
    diff = sp.simplify(key - exact)
    lv.claim(diff == 0 or (up and diff.free_symbols == set()), f'{tag}: key {w["answer"]} equals {exact}')
    if integrand is not None:
        lv.claim(sp.simplify(sp.diff(key, var) - integrand) == 0, f'{tag}: derivative of the key is the integrand')
    for a in w.get('accept', []):
        d = sp.simplify(tex2sp(a) - exact)
        lv.claim(d == 0 or (up and d.free_symbols == set()), f'{tag}: accept {a} is equivalent')
    slips = slips or {}
    got = {d['id']: d['tex'] for d in w.get('wrong', [])}
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} all recomputed')
    for k, v in slips.items():
        g = tex2sp(got[k])
        lv.claim(sp.simplify(g - v) == 0, f'{tag}: wrong "{k}" is the slip {v}')
        d = sp.simplify(g - exact)
        lv.claim(d != 0 and not (up and d.free_symbols == set()), f'{tag}: wrong "{k}" is not equivalent to the key')


def pick(lv, i, j, cid):
    w = W(lv, i, j)
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    lv.claim(keyed == [cid], f'problems-{lv.n} item {i} part {j + 1}: keyed option {keyed}')


def say(lv, i, j, where, value, fmt=None):
    lv.expect('problems', f'items[{i}].parts[{j}].{where}', value, fmt)


def riemann(f, a, c, m=200000):
    h = (c - a) / m
    return h * sum(f(a + (k + 0.5) * h) for k in range(m))


def trap(f, a, c, m):
    h = (c - a) / m
    return h * (0.5 * f(a) + 0.5 * f(c) + sum(f(a + k * h) for k in range(1, m)))


# ====================================================================== level 1
lv = Level('integrals', 1)

# p-falling-parabola: f(x) = 9 - x^2 on [0, 3]
fF = lambda q: 9 - q * q
h6 = F(1, 2)
R6 = sum(fF(h6 * k) for k in range(1, 7)) * h6
L6 = sum(fF(h6 * k) for k in range(0, 6)) * h6
Rn = sp.summation((9 - 9 * sp.Symbol('k') ** 2 / n ** 2) * 3 / n, (sp.Symbol('k'), 1, n))
Rn_closed = 18 - sp.Rational(27, 2) / n - sp.Rational(9, 2) / n ** 2
lv.claim(sp.simplify(Rn - Rn_closed) == 0, 'L1 p-falling-parabola: symbolic sum equals 18 - 27/(2n) - 9/(2n^2)')
num(lv, 0, 0, R6, Rn_closed.subs(n, 6), {'left-ends': L6, 'no-width': R6 / h6}, printed=15.625)
for v in (8.75, 8, 6.75, 5, 2.75, 31.25, 15.625):
    say(lv, 0, 0, 'feedback.correct', v)
gap6 = abs(fF(3) - fF(0)) * F(3, 6)
num(lv, 0, 1, R6 + gap6, L6, {'subtracted': R6 - gap6, 'no-length': R6 + 9 * F(1, 6)}, printed=20.125)
say(lv, 0, 1, 'feedback.correct', 4.5)
nmin = next(m for m in range(1, 10000) if F(27, m) <= F(1, 10))
num(lv, 0, 2, nmin, math.ceil(27 / 0.1 - 1e-9), {'no-length': next(m for m in range(1, 10000) if F(9, m) <= F(1, 10)), 'strict': nmin + 1})
expr(lv, 0, 3, Rn_closed, slips={
    'left-ends': Rn_closed + 27 / n,
    'nine': 9 - 9 * (n + 1) * (2 * n + 1) / (2 * n ** 2),
    'no-width': sp.expand(sp.summation(9 - 9 * sp.Symbol('k') ** 2 / n ** 2, (sp.Symbol('k'), 1, n)))})
lv.claim(Rn_closed.subs(n, 6) == sp.Rational(125, 8), 'L1 p-falling-parabola part 4: R_6 from the formula is 15.625')
num(lv, 0, 4, sp.limit(Rn_closed, n, sp.oo), riemann(fF, 0, 3), {
    'no-squares': 27, 'stopped': R6, 'nine': sp.limit(9 - 9 * (n + 1) * (2 * n + 1) / (2 * n ** 2), n, sp.oo)})

# p-subscriptions: s(t) = 12 - 4t
s1 = lambda q: 12 - 4 * q
peak = F(12, 4)
num(lv, 1, 0, peak, sp.solve(12 - 4 * t, t)[0], {'rate-highest': 0, 'zero-total': 6})
tri = F(1, 2) * 3 * 12
num(lv, 1, 1, tri, riemann(s1, 0, 3), {'rectangle': 3 * 12, 'rate': s1(0)})
out = F(1, 2) * 2 * 8
num(lv, 1, 2, tri - out, riemann(s1, 0, 5), {'gross': tri + out, 'peak': tri, 'only-outflow': -out})
num(lv, 1, 3, -(tri - out), -riemann(s1, 0, 5), {'no-flip': tri - out, 'gross': -(tri + out)})
T0 = sp.solve(sp.Eq(2 * (t - 3) ** 2, 18), t)
T0 = [r for r in T0 if r > 3][0]
num(lv, 1, 4, T0, sp.nsolve(12 * t - 2 * t ** 2, t, 5.5), {'no-half': 3 + math.sqrt(4.5), 'rate-zero': 3})

# p-desk-session: r(t) = t^2 - 4
r1 = lambda q: q * q - 4
M3 = sum(r1(F(2 * k + 1, 2)) for k in range(3))
num(lv, 2, 0, M3, sum(r1(k + 0.5) for k in range(3)), {
    'right-ends': sum(r1(k) for k in (1, 2, 3)), 'left-ends': sum(r1(k) for k in (0, 1, 2)),
    'unsigned': sum(abs(r1(F(2 * k + 1, 2))) for k in range(3))}, printed=-3.25)
for v in (-3.75, -1.75, 2.25):
    say(lv, 2, 0, 'feedback.correct', v)
I3 = sp.integrate(t ** 2 - 4, (t, 0, 3))
lv.claim(sp.limit(b ** 3 * (n + 1) * (2 * n + 1) / (6 * n ** 2), n, sp.oo) == b ** 3 / 3, 'L1 p-desk-session prose: right sums of t^2 on [0, b] tend to b^3/3')
num(lv, 2, 1, I3, riemann(r1, 0, 3), {'once': 9 - 4, 'squares-only': 9})
say(lv, 2, 1, 'explain.text', 0.25)
lv.claim(abs(float(M3 - I3)) == 0.25, 'L1 p-desk-session part 2: midpoint error 0.25')
num(lv, 2, 2, sp.solve(t ** 2 - 4, t)[0], min((riemann(r1, 0, k / 100, 400), k / 100) for k in range(0, 301))[1], {'rate-lowest': 0, 'end': 3})
low = sp.Rational(8, 3) - 8
num(lv, 2, 3, low, riemann(r1, 0, 2), {'sign': 5.33, 'squares-only': 2.67, 'rect-only': -8}, printed=-5.33)
lv.claim(abs(-low - 5.33) < 0.005 and abs(sp.Rational(8, 3) - 2.67) < 0.005, 'L1 p-desk-session part 4: slips 5.33 and 2.67 are -low and 8/3 rounded')
num(lv, 2, 4, I3 - low, riemann(r1, 2, 3), {'added': -8.33, 'reversed': -2.33, 'rate-end': r1(3)}, printed=2.33)
lv.claim(abs((I3 + low) - (-8.33)) < 0.005 and abs(-(I3 - low) + 2.33) < 0.005, 'L1 p-desk-session part 5: added and reversed slips')
lv.claim(sp.Rational(27 - 8, 3) - 4 == sp.Rational(7, 3), 'L1 p-desk-session part 5 explain: (27 - 8)/3 - 4 = 7/3')

lv.check_wrongs()
lv1 = lv

# ====================================================================== level 2
lv = Level('integrals', 2)

# p-area-function: f(t) = t^2 - 6t + 8, A(x) = int_0^x f
f2 = t ** 2 - 6 * t + 8
Ff = sp.integrate(f2, t)
A = lambda q: Ff.subs(t, q) - Ff.subs(t, 0)
fl = sp.lambdify(t, f2)
num(lv, 0, 0, f2.subs(t, 3), (riemann(fl, 0, 3 + 1e-4, 20000) - riemann(fl, 0, 3 - 1e-4, 20000)) / 2e-4,
    {'area': A(3), 'derivative-of-f': sp.diff(f2, t).subs(t, 3)}, agree=1e-5)
crit = sp.solve(f2, t)
locmax = [c for c in crit if sp.diff(f2, t).subs(t, c) < 0][0]
num(lv, 0, 1, locmax, max((riemann(fl, 0, k / 100, 400), k / 100) for k in range(0, 401))[1],
    {'min': [c for c in crit if c != locmax][0], 'vertex': sp.solve(sp.diff(f2, t), t)[0]})
expr(lv, 0, 2, Ff, integrand=f2, var=t, slips={'old-power': t ** 3 / 2 - 6 * t ** 2 + 8 * t, 'no-divide': t ** 3 - 6 * t ** 2 + 8 * t,
                                              'derivative': sp.diff(f2, t)})
oldF = t ** 3 / 2 - 6 * t ** 2 + 8 * t
num(lv, 0, 3, A(2), riemann(fl, 0, 2), {'at-four': A(4), 'at-three': A(3), 'old-power': oldF.subs(t, 2)}, printed=6.667)
num(lv, 0, 4, max(A(0), A(2), A(6)), max(riemann(fl, 0, k / 50, 2000) for k in range(1, 301)),
    {'local': A(2), 'unsigned': sp.integrate(sp.Abs(f2), (t, 0, 6))}, agree=1e-4)
say(lv, 0, 4, 'feedback.correct', 72)
say(lv, 0, 4, 'feedback.correct', 108)

# p-turnover-decay: v(t) = 8 e^{-0.5t}
k = sp.Rational(-1, 2)
v = 8 * sp.exp(k * t)
expr(lv, 1, 0, sp.integrate(v, t), integrand=v, var=t, slips={'times-k': 8 * k * sp.exp(k * t), 'no-k': 8 * sp.exp(k * t), 'sign': 16 * sp.exp(k * t)})
Cc = sp.solve(sp.Eq(-16 * sp.exp(0) + sp.Symbol('C'), 0))[0]
num(lv, 1, 1, Cc, 16 * (1 - math.exp(0)) + 16, {'zero': 0, 'minus': -16})
T4 = 16 - 16 * sp.exp(-2)
vl = lambda q: 8 * math.exp(-0.5 * q)
num(lv, 1, 2, T4, riemann(vl, 0, 4), {'no-c': -16 * sp.exp(-2), 'times-k': 4 * (1 - sp.exp(-2)), 'rate': vl(4)}, printed=13.83)
say(lv, 1, 2, 'feedback.correct', 2.17)
tq = sp.solve(sp.Eq(16 - 16 * sp.exp(-t / 2), 12), t)[0]
lo, hi = 0.0, 10.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if riemann(vl, 0, mid, 4000) < 12 else (lo, mid)
num(lv, 1, 3, tq, lo, {'divided': sp.log(4) / 2, 'wrong-share': 2 * sp.log(sp.Rational(4, 3))}, printed=2.77, agree=1e-6)

# p-line-and-parabola: y = 2x^2, y = x + 3
X = sp.Symbol('X', real=True)
roots = sp.solve(2 * X ** 2 - X - 3, X)
numset(lv, 2, 0, roots, [r for r in (-1, 1.5) if abs(2 * r * r - r - 3) < 1e-12], {'signs': sp.solve(2 * X ** 2 + X - 3, X)})
gap = X + 3 - 2 * X ** 2
gl = sp.lambdify(X, gap)
A1 = sp.integrate(gap, (X, -1, sp.Rational(3, 2)))
num(lv, 2, 1, A1, riemann(gl, -1, 1.5), {'bottom-top': -A1, 'signs': sp.integrate(gap, (X, sp.Rational(-3, 2), 1)),
                                         'line-only': sp.integrate(X + 3, (X, -1, sp.Rational(3, 2)))}, printed=5.208)
G = sp.integrate(gap, X)
lv.claim(G.subs(X, 1.5) == 3.375 and G.subs(X, -1) == sp.Rational(-11, 6), 'L2 p-line-and-parabola part 2: antiderivative values 3.375 and -11/6')
A2 = sp.integrate(-gap, (X, -2, -1))
num(lv, 2, 2, A2, -riemann(gl, -2, -1), {'signed': -A2, 'parabola-only': sp.integrate(2 * X ** 2, (X, -2, -1))}, printed=3.167)
H = sp.integrate(-gap, X)
lv.claim(H.subs(X, -1) == sp.Rational(11, 6) and H.subs(X, -2) == sp.Rational(-4, 3), 'L2 p-line-and-parabola part 3: values 11/6 and -4/3')
lv.claim(2 * (-2) ** 2 == 8 and -2 + 3 == 1, 'L2 p-line-and-parabola part 3: at x = -2 the curves are at 8 and 1')
num(lv, 2, 3, A1 + A2, riemann(lambda q: abs(gl(q)), -2, 1.5), {'one-integral': A1 - A2, 'negative': A2 - A1}, printed=8.375)
lv.claim(A2 == sp.Rational(76, 24) and A1 - A2 == sp.Rational(49, 24), 'L2 p-line-and-parabola part 4: 19/6 = 76/24 and the single integral is 49/24')

# p-etf-units: f(t) = 12t - 3t^2, redemptions 9
fe = 12 * t - 3 * t ** 2
g = fe - 9
Gx = sp.integrate(g, (t, 0, x))
gl2 = sp.lambdify(t, g)
num(lv, 3, 0, g.subs(t, 2), (riemann(gl2, 0, 2 + 1e-4, 20000) - riemann(gl2, 0, 2 - 1e-4, 20000)) / 2e-4,
    {'no-redeem': fe.subs(t, 2), 'value': Gx.subs(x, 2)}, agree=1e-5)
expr(lv, 3, 1, Gx.subs(x, x), slips={'no-redeem': sp.integrate(fe, (t, 0, x)), 'old-power': -sp.Rational(3, 2) * x ** 3 + 12 * x ** 2 - 9 * x})
lv.claim(sp.expand(-3 * (t - 1) * (t - 3) - g) == 0, 'L2 p-etf-units part 3: f - 9 = -3(t - 1)(t - 3)')
num(lv, 3, 2, Gx.subs(x, 1), riemann(gl2, 0, 1), {'no-redeem': sp.integrate(fe, (t, 0, 1)), 'at-three': Gx.subs(x, 3)})
num(lv, 3, 3, Gx.subs(x, 5), riemann(gl2, 0, 5), {'sign': -Gx.subs(x, 5), 'no-redeem': sp.integrate(fe, (t, 0, 5)), 'level': Gx.subs(x, 3)})
area = sp.integrate(sp.Abs(g), (t, 0, 5))
num(lv, 3, 4, area, riemann(lambda q: abs(gl2(q)), 0, 5), {'net': Gx.subs(x, 5), 'unsigned-net': abs(Gx.subs(x, 5)),
                                                            'missed-middle': area - (Gx.subs(x, 3) - Gx.subs(x, 1))})

lv.check_wrongs()
lv2 = lv

# ====================================================================== level 3
lv = Level('integrals', 3)
E_ = math.e

# p-order-size-tail: f(x) = 2x/(1+x^2)^2
fo = 2 * x / (1 + x ** 2) ** 2
expr(lv, 0, 0, sp.integrate(fo, x), integrand=fo, var=x, slips={
    'sign': 1 / (1 + x ** 2), 'log': sp.log(1 + x ** 2), 'power-down': -1 / (3 * (1 + x ** 2) ** 3)})
fol = sp.lambdify(x, fo)
lv.claim(sp.integrate(fo, (x, 0, sp.oo)) == 1, 'L3 p-order-size-tail: the density integrates to 1')
tail = lambda q: sp.integrate(fo, (x, q, sp.oo))
num(lv, 0, 1, tail(2), quad(fol, 2, math.inf)[0], {'below': 1 - tail(2), 'x-limits': sp.integrate(x ** -2, (x, 2, sp.oo))}, printed=0.2)
m = sp.Symbol('m', positive=True)
lv.claim(sp.simplify(tail(m) - 1 / (1 + m ** 2)) == 0, 'L3 p-order-size-tail part 3: P(X > m) = 1/(1 + m^2)')
med = sp.solve(sp.Eq(1 / (1 + m ** 2), sp.Rational(1, 2)), m)[0]
lo, hi = 0.0, 10.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if quad(fol, mid, math.inf)[0] > 0.5 else (lo, mid)
num(lv, 0, 2, med, lo, {'drop-one': sp.sqrt(2)}, agree=1e-6)
q99 = sp.solve(sp.Eq(1 / (1 + m ** 2), sp.Rational(1, 100)), m)[0]
lo, hi = 0.0, 100.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if quad(fol, mid, math.inf)[0] > 0.01 else (lo, mid)
num(lv, 0, 3, q99, lo, {'drop-one': 10, 'no-root': 99, 'wrong-tail': sp.sqrt(1 / sp.Rational(99, 100) - 1)}, printed=9.95, agree=1e-6)

# p-time-to-fill: f(x) = x e^{-x}
ft = x * sp.exp(-x)
expr(lv, 1, 0, sp.integrate(ft, x), integrand=ft, var=x, slips={
    'minus-sign': -(x - 1) * sp.exp(-x), 'uv-only': -x * sp.exp(-x), 'v-sign': (x + 1) * sp.exp(-x)})
ftl = lambda q: q * math.exp(-q)
p2 = sp.integrate(ft, (x, 2, sp.oo))
num(lv, 1, 1, p2, quad(ftl, 2, math.inf)[0], {'dropped-x': sp.exp(-2), 'dropped-one': 2 * sp.exp(-2), 'complement': 1 - p2}, printed=0.406)
EX = sp.integrate(x * ft, (x, 0, sp.oo))
num(lv, 1, 2, EX, quad(lambda q: q * ftl(q), 0, math.inf)[0], {'no-factor': sp.integrate(ft, (x, 0, sp.oo))})
EV = 100 * sp.integrate(sp.exp(-x) * ft, (x, 0, sp.oo))
num(lv, 1, 3, EV, 100 * quad(lambda q: math.exp(-q) * ftl(q), 0, math.inf)[0],
    {'mean-wait': 100 * sp.exp(-EX), 'half': 100 * sp.Rational(1, 2), 'one': 100 * 1})
lv.claim(abs(100 * math.exp(-2) - 13.53) < 0.005, 'L3 p-time-to-fill part 5: 100e^{-2} is about £13.53')
pick(lv, 1, 4, 'a')

# p-log-return: X uniform on [0.5, 1.5]
ln = math.log
T2 = trap(ln, 0.5, 1.5, 2)
T2x = sp.Rational(1, 2) * (sp.log(sp.Rational(1, 2)) / 2 + sp.log(sp.Rational(3, 2)) / 2)
num(lv, 2, 0, T2x, T2, {'full-ends': 0.5 * (ln(0.5) + ln(1) + ln(1.5)), 'midpoint': 0.5 * (ln(0.75) + ln(1.25)),
                        'lost-strip': 0.5 * (0.5 * ln(0.5) + ln(1))}, printed=-0.0719)
lv.claim(round(0.5 * (-0.3466 + 0 + 0.2027), 4) in (-0.0719, -0.072) and abs(ln(0.5) / 2 + 0.3466) < 5e-5 and abs(ln(1.5) / 2 - 0.2027) < 5e-5,
         'L3 p-log-return part 1 explain: half-heights -0.3466 and 0.2027')
Eln = sp.integrate(sp.log(x), (x, sp.Rational(1, 2), sp.Rational(3, 2)))
num(lv, 2, 1, Eln, quad(ln, 0.5, 1.5)[0], {'plus-x': (1.5 * ln(1.5) + 1.5) - (0.5 * ln(0.5) + 0.5),
                                           'uv-only': 1.5 * ln(1.5) - 0.5 * ln(0.5), 'estimate': T2}, printed=-0.0452)
err2 = float(T2x - Eln)
lv.claim(abs(abs(err2) - 0.0267) < 5e-5, f'L3 p-log-return part 3: stated error 0.0267 vs {abs(err2):.5f}')
num(lv, 2, 2, F('0.0267') / 16, 0.0267 / ((0.5 / 0.125) ** 2), {'linear': 0.0267 / 4, 'eight-squared': 0.0267 / 64}, printed=0.0017)
lv.claim(abs(abs(trap(ln, 0.5, 1.5, 8) - float(Eln)) - 0.0017) < 0.00005, 'L3 p-log-return part 3: the true T_8 error is 0.0017 to 4 places')
pick(lv, 2, 3, 'a')
lv.claim(float(Eln) < math.log(1), 'L3 p-log-return part 4: E[ln X] < ln E[X]')

# p-signal-average: s(t) = t e^{-t^2/8}
sx = t * sp.exp(-t ** 2 / 8)
expr(lv, 3, 0, sp.integrate(sx, t), integrand=sx, var=t, slips={
    'quarter': -sp.exp(-t ** 2 / 8) / 4, 'sign': 4 * sp.exp(-t ** 2 / 8), 'no-fix': -sp.exp(-t ** 2 / 8)})
sl = lambda q: q * math.exp(-q * q / 8)
I4 = sp.integrate(sx, (t, 0, 4))
num(lv, 3, 1, I4, quad(sl, 0, 4)[0], {'x-limits': 4 * (1 - sp.exp(-4)), 'quarter': (1 - sp.exp(-2)) / 4, 'sign': -I4}, printed=3.459)
num(lv, 3, 2, I4 / 4, riemann(sl, 0, 4) / 4, {'no-divide': I4, 'halved': I4 / 2, 'x-limits': (1 - sp.exp(-4))}, printed=0.865)
lv.claim(abs(3.459 / 4 - float(I4 / 4)) < 0.0005, 'L3 p-signal-average part 3: 3.459 / 4 is accepted too')
T2s = trap(sl, 0, 4, 2)
num(lv, 3, 3, 2 * (2 * sp.exp(-sp.Rational(1, 2)) + 2 * sp.exp(-2)), T2s, {
    'full-ends': 2 * (sl(0) + sl(2) + sl(4)), 'no-h': 0.5 * sl(0) + sl(2) + 0.5 * sl(4), 'midpoint': 2 * (sl(1) + sl(3))}, printed=2.967)
lv.claim(abs(sl(2) - 1.2131) < 5e-5 and abs(sl(4) - 0.5413) < 5e-5, 'L3 p-signal-average part 4: s(2) and s(4) as printed')
e0 = float(I4) - T2s
lv.claim(abs(e0 - 0.49) < 0.005, f'L3 p-signal-average part 5: error of T_2 is about 0.49 ({e0:.4f})')
pred = {m_: 0.49 / (m_ / 2) ** 2 for m_ in (2, 4, 8, 16, 32)}
first = next(m_ for m_ in (2, 4, 8, 16, 32) if pred[m_] < 0.01)
true_first = next(m_ for m_ in (2, 4, 8, 16, 32) if abs(float(I4) - trap(sl, 0, 4, m_)) < 0.01)
lin = next(m_ for m_ in (2 ** j for j in range(1, 12)) if 0.49 / (m_ / 2) < 0.01)
num(lv, 3, 4, first, true_first, {'linear': lin, 'one-short': first // 2})
lv.claim(abs(pred[4] - 0.12) < 0.005 and abs(pred[8] - 0.031) < 0.0005 and abs(pred[16] - 0.0077) < 0.00005, 'L3 p-signal-average part 5: printed predictions 0.12, 0.031, 0.0077')

lv.check_wrongs()

# ---------------------------------------------------------------- report
bad = []
for L in (lv1, lv2, lv):
    bad += [r for r in L.results if not r[0]]
total = sum(len(L.results) for L in (lv1, lv2, lv))
print(f'integrals problems: {total - len(bad)} of {total} checks passed')
for r in bad:
    print('BAD', r[1], r[2])
sys.exit(1 if bad else 0)
