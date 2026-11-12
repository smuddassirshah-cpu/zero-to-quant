"""Recompute every number in app/content/courses/multivar/problems-<n>.json twice.

Method 1 is exact: sympy (derivatives, Hessians, solving the Lagrange system, expansion) and fractions.
Method 2 is independent: central finite differences, a direct numerical walk along the path, a brute-force
search on a grid or along the constraint, a gradient-descent simulation, or root finding by bisection.
For each numeric part the script checks that the two methods agree, that the JSON key matches them within
its tol, that the value the feedback prints is accepted by that tol, and that every `wrong` value is the
slip its byKey line names; lv.check_wrongs then checks each wrong value lies outside the key's band.
Expression parts (including pairs) are parsed from their TeX and compared with sympy; every `accept`
form must be equivalent and every wrong form must be the named slip and not equivalent. Choice parts
check the keyed option against the computed classification. Stated numbers are tied to their text with lv.expect.

Run: <scratchpad>/venv/bin/python docs/reports/problems-multivar-numbers.py   (exit 0 when all pass)
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

x, y, X, P, w, a, b, lam, t = sp.symbols('x y X P w a b lam t', real=True)
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
u, v, r = sp.symbols('u v r', real=True)
LOCAL = {'x': x, 'y': y, 'X': X, 'P': P, 'w': w, 'u': u, 'v': v, 'r': r, 'pi': sp.pi, 'sqrt': sp.sqrt}


def derived_slips(slips, wrongs, e, text=''):
    """Slips the script derives itself for the `sign` / `sign2` and `decimal` wrong entries.

    sign: the absolute value of the computed key (the sign-dropped answer).
    decimal: the computed key over 100 (over 10,000 where the part is in %^2).
    Each is then compared with the content value inside its tolerance, and must lie
    outside the key band, by the ordinary slip checks below."""
    s = dict(slips or {})
    for wid in wrongs:
        if wid in s:
            continue
        if re.fullmatch(r'sign\d*', wid):
            s[wid] = abs(e)
        elif wid == 'decimal':
            s[wid] = e / (10000 if '%\u00b2' in text else 100)
    return s


def _sqrt(s):
    r"""\sqrt{A} -> sqrt(A), braces matched (levels 4 and 5)."""
    while '\\sqrt{' in s:
        i = s.index('\\sqrt{')
        j = i + 5
        d, k = 0, j
        while True:
            d += {'{': 1, '}': -1}.get(s[k], 0)
            if d == 0:
                break
            k += 1
        s = s[:i] + f'sqrt({s[j + 1:k]})' + s[k + 1:]
    return s


# ---------------------------------------------------------------- helpers
def _frac(s):
    s = s.replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
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


def _split_top(s):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '({':
            d += 1
        elif ch in ')}':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def tex2sp(s):
    """TeX subset of these answers into sympy; a top-level pair '(a, b)' becomes a tuple."""
    s = s.strip()
    if s.startswith('(') and s.endswith(')') and len(_split_top(s[1:-1])) == 2:
        return tuple(tex2sp(p) for p in _split_top(s[1:-1]))
    s = _sqrt(_frac(s)).replace('\\pi', ' pi ').replace('\\cdot', '*').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict=LOCAL, transformations=TR)


def same(u, v):
    if isinstance(u, tuple) or isinstance(v, tuple):
        return isinstance(u, tuple) and isinstance(v, tuple) and len(u) == len(v) and all(sp.simplify(p - q) == 0 for p, q in zip(u, v))
    return sp.simplify(u - v) == 0


def W(lv, i, j):
    return lv.files[f'problems-{lv.n}']['items'][i]['parts'][j]['widget']


def num(lv, i, j, exact, second, slips=None, printed=(), agree=1e-7):
    tag = f'L{lv.n} item {i} part {j + 1}'
    wd = W(lv, i, j)
    ex = float(exact)
    lv.claim(abs(ex - float(second)) <= agree * max(1, abs(ex)), f'{tag}: two methods agree {ex:.10g} vs {float(second):.10g}')
    tol = wd['tol']['abs']
    lv.claim(abs(wd['answer'] - ex) <= tol + 1e-12, f'{tag}: key {wd["answer"]} matches {ex:.8g} within {tol}')
    for pv in printed:
        lv.claim(abs(pv - wd['answer']) <= tol + 1e-12, f'{tag}: printed value {pv} is accepted by the tol')
    slips = slips or {}
    got = {d['id']: d for d in wd.get('wrong', [])}
    slips = derived_slips(slips, got, ex, json.dumps(wd, ensure_ascii=False))
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} all recomputed')
    for k, v in slips.items():
        if k in got:
            wt = got[k]['tol']['abs']
            lv.claim(abs(got[k]['value'] - float(v)) <= max(wt, 1e-9), f'{tag}: wrong "{k}" = {got[k]["value"]} is the slip {float(v):.6g}')


def numset(lv, i, j, roots, second, slips):
    tag = f'L{lv.n} item {i} part {j + 1}'
    wd = W(lv, i, j)
    lv.claim(sorted(float(r) for r in roots) == sorted(float(r) for r in second), f'{tag}: roots agree {sorted(roots)}')
    lv.claim(sorted(wd['answers']) == sorted(float(r) for r in roots), f'{tag}: key {wd["answers"]}')
    got = {d['id']: d['value'] for d in wd.get('wrong', [])}
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids recomputed')
    for k, v in slips.items():
        vals = sorted(float(q) for q in got[k].split(','))
        lv.claim(vals == sorted(float(q) for q in v) and vals != sorted(wd['answers']), f'{tag}: wrong set "{k}" {vals} is the slip and differs')


def expr(lv, i, j, exact, slips):
    tag = f'L{lv.n} item {i} part {j + 1}'
    wd = W(lv, i, j)
    key = tex2sp(wd['answer'])
    lv.claim(same(key, exact), f'{tag}: key {wd["answer"]} equals {exact}')
    for acc in wd.get('accept', []):
        lv.claim(same(tex2sp(acc), exact), f'{tag}: accept {acc} is equivalent')
    got = {d['id']: d['tex'] for d in wd.get('wrong', [])}
    lv.claim(set(got) == set(slips), f'{tag}: wrong ids {sorted(got)} all recomputed')
    for k, v in slips.items():
        g = tex2sp(got[k])
        lv.claim(same(g, v), f'{tag}: wrong "{k}" is the slip {v}')
        lv.claim(not same(g, exact), f'{tag}: wrong "{k}" is not equivalent to the key')


def pick(lv, i, j, cid):
    wd = W(lv, i, j)
    keyed = [o['id'] for o in wd['options'] if o.get('correct')]
    lv.claim(keyed == [cid], f'L{lv.n} item {i} part {j + 1}: keyed option {keyed} is {cid}')


def say(lv, i, j, where, value):
    lv.expect('problems', f'items[{i}].parts[{j}].{where}', value)


def prose(lv, i, value):
    lv.expect('problems', f'items[{i}].prose', value)


def fd(f, p, k, h=1e-5):
    """Central difference of a numeric function f(*p) in coordinate k."""
    q1, q2 = list(p), list(p)
    q1[k] += h
    q2[k] -= h
    return (f(*q1) - f(*q2)) / (2 * h)


def bisect(g, lo, hi, n=200):
    glo = g(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (g(mid) > 0) == (glo > 0):
            lo, glo = mid, g(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def classify(H):
    ev = [float(e) for e in sp.Matrix(H).eigenvals(multiple=True)]
    if all(e > 0 for e in ev):
        return 'pit'
    if all(e < 0 for e in ev):
        return 'peak'
    if any(e > 0 for e in ev) and any(e < 0 for e in ev):
        return 'saddle'
    return 'none'


results = []

# ====================================================================== level 1
lv = Level('multivar', 1)

# ---- item 0 p-stretched-bowl: f = 9x^2 + y^2
f = 9 * x ** 2 + y ** 2
fn = sp.lambdify((x, y), f)
c = f.subs({x: 1, y: 3})
num(lv, 0, 0, c, fn(1, 3), {'no-square-y': 9 + 3, 'swapped': 1 + 9 * 9}, printed=(18,))
gx, gy = sp.diff(f, x).subs({x: 1, y: 3}), sp.diff(f, y).subs({x: 1, y: 3})
lv.claim(abs(fd(fn, (1, 3), 0) - 18) < 1e-6 and abs(fd(fn, (1, 3), 1) - 6) < 1e-6, 'L1 item 0 part 2: finite differences give (18, 6)')
expr(lv, 0, 1, (gx, gy), {'no-power': (9 * 1, 3), 'swapped': (gy, gx)})
dy_lin = -F(int(gx)) * F(1, 100) / F(int(gy))
yexact = sp.sqrt(18 - 9 * sp.Rational(101, 100) ** 2)
y_bis = bisect(lambda q: 9 * 1.01 ** 2 + q * q - 18, 0, 3)
num(lv, 0, 2, dy_lin, -0.03, {'sign': -dy_lin, 'inverted': -F(6, 18) * F(1, 100), 'rise-in-f': gx * F(1, 100)}, printed=(-0.03, round(y_bis - 3, 4)))
say(lv, 0, 2, 'feedback.correct', 0.18)
num(lv, 0, 3, yexact - 3, y_bis - 3, {'linear': dy_lin, 'no-square': math.sqrt(18 - 9 * 1.01) - 3, 'no-subtract': float(yexact)}, printed=(-0.0303,))
lv.claim(9 * F(101, 100) ** 2 == F(91809, 10000) and 18 - F(91809, 10000) == F(88191, 10000), 'L1 item 0 part 4: 9(1.01)^2 = 9.1809 and 18 - 9.1809 = 8.8191')
lv.claim(round(float(yexact), 4) == 2.9697 and round(float(yexact) - 3 + 0.03, 4) == -0.0003, 'L1 item 0 part 4: y = 2.9697 and the estimate missed by 0.0003')
for v in (9.1809, 8.8191, 2.9697, 0.0303):
    say(lv, 0, 3, 'feedback.correct' if v != 0.0303 else 'explain.text', v if v != 0.0303 else -0.0303)

# ---- item 1 p-mixed-both-ways: f = x^3 y - 2 x y^2
f = x ** 3 * y - 2 * x * y ** 2
fn = sp.lambdify((x, y), f)
fx, fy = sp.diff(f, x), sp.diff(f, y)
fxy, fyx = sp.diff(fx, y), sp.diff(fy, x)
expr(lv, 1, 0, fx, {'wrong-variable': fy, 'both': fx + fy})
expr(lv, 1, 1, fxy, {'xx': sp.diff(fx, x), 'carried-both': sp.diff(fx + fy, y)})
pt = {x: 2, y: 1}
fxy_fd = (fd(fn, (2, 1 + 1e-4), 0) - fd(fn, (2, 1 - 1e-4), 0)) / 2e-4
num(lv, 1, 2, fyx.subs(pt), fxy_fd, {'xx': sp.diff(fx, x).subs(pt), 'yy': sp.diff(fy, y).subs(pt), 'sign': (3 * x ** 2 + 4 * y).subs(pt)}, agree=1e-5)
lv.claim(sp.simplify(fxy - fyx) == 0, 'L1 item 1 part 3: f_xy = f_yx')
num(lv, 1, 3, fx.subs(pt), fd(fn, (2, 1), 0), {'sign': (3 * x ** 2 * y + 2 * y ** 2).subs(pt), 'f-y': fy.subs(pt)}, agree=1e-6)
est = fx.subs(pt) + fxy.subs(pt) * sp.Rational(1, 10)
true5 = fx.subs({x: 2, y: sp.Rational(11, 10)})
num(lv, 1, 4, est, 10 + 8 * 0.1, {'used-xx': 10 + sp.diff(fx, x).subs(pt) * sp.Rational(1, 10), 'used-yy': 10 + sp.diff(fy, y).subs(pt) * sp.Rational(1, 10), 'change-only': fxy.subs(pt) * sp.Rational(1, 10)}, printed=(10.8, float(true5)))
lv.claim(true5 == sp.Rational(1078, 100) and fd(fn, (2, 1.1), 0) - 10.78 < 1e-6, 'L1 item 1 part 5: exact f_x(2, 1.1) = 13.2 - 2.42 = 10.78')
say(lv, 1, 4, 'explain.text', 10.78)
say(lv, 1, 2, 'feedback.correct', 8)

# ---- item 2 p-dollar-holding: V = 2000 P / X
V = 2000 * P / X
Vn = sp.lambdify((P, X), V)
pt = {P: 50, X: sp.Rational(5, 4)}
lv.claim(V.subs(pt) == 80000 and abs(Vn(50, 1.25) - 80000) < 1e-9, 'L1 item 2 prose: V = 80,000')
prose(lv, 2, 80000)
VP, VX = sp.diff(V, P), sp.diff(V, X)
num(lv, 2, 0, VP.subs(pt), fd(Vn, (50, 1.25), 0), {'times-x': 2000 * 1.25, 'no-x': 2000}, agree=1e-6)
num(lv, 2, 1, VX.subs(pt), fd(Vn, (50, 1.25), 1, 1e-6), {'sign': -VX.subs(pt), 'no-square': -2000 * 50 / sp.Rational(5, 4)}, agree=1e-6)
Pp, Xp = sp.Rational(1, 2), sp.Rational(1, 100)
rate = VP.subs(pt) * Pp + VX.subs(pt) * Xp
walk = (Vn(50 + 0.5 * 1e-6, 1.25 + 0.01 * 1e-6) - Vn(50 - 0.5 * 1e-6, 1.25 - 0.01 * 1e-6)) / 2e-6
num(lv, 2, 2, rate, walk, {'sign': VP.subs(pt) * Pp - VX.subs(pt) * Xp, 'price-only': VP.subs(pt) * Pp, 'carried': VP.subs(pt) * Pp - 80000 * Xp}, agree=1e-5)
for v in (800, 640, 160):
    say(lv, 2, 2, 'feedback.correct', v)
VPX = sp.diff(VP, X)
expr(lv, 2, 3, VPX, {'sign': -VPX, 'gave-vx': VX})
lv.claim(VPX.subs(pt) == -1280 and sp.diff(VX, P) == VPX, 'L1 item 2 part 4: V_PX = V_XP = -1,280 at X = 1.25')
say(lv, 2, 3, 'explain.text', -1280)
VPn = sp.lambdify((P, X), VP)
drift = sp.diff(VP, P).subs(pt) * Pp + VPX.subs(pt) * Xp
walk = (VPn(50 + 0.5e-6, 1.25 + 0.01e-6) - VPn(50 - 0.5e-6, 1.25 - 0.01e-6)) / 2e-6
num(lv, 2, 4, drift, walk, {'sign': -drift, 'no-rate': VPX.subs(pt), 'used-vx': VX.subs(pt) * Xp}, printed=(-12.8,), agree=1e-5)
lv.claim(sp.diff(VP, P) == 0, 'L1 item 2 part 5: V_PP = 0')

lv.check_wrongs('problems')
results.append(lv)

# ====================================================================== level 2
lv = Level('multivar', 2)

# ---- item 0 p-slopes-around: f = x^2 y at (3, 2)
f = x ** 2 * y
fn = sp.lambdify((x, y), f)
g = (sp.diff(f, x).subs({x: 3, y: 2}), sp.diff(f, y).subs({x: 3, y: 2}))
lv.claim(f.subs({x: 3, y: 2}) == 18, 'L2 item 0 prose: f(3, 2) = 18')
lv.claim(abs(fd(fn, (3, 2), 0) - 12) < 1e-6 and abs(fd(fn, (3, 2), 1) - 9) < 1e-6, 'L2 item 0 part 1: finite differences give (12, 9)')
expr(lv, 0, 0, g, {'swapped': (g[1], g[0]), 'no-two': (3 * 2, 9)})
L = sp.sqrt(g[0] ** 2 + g[1] ** 2)
num(lv, 0, 1, L, max(12 * math.cos(th) + 9 * math.sin(th) for th in [k * 2 * math.pi / 200000 for k in range(200000)]),
    {'added': g[0] + g[1], 'no-root': L ** 2}, agree=1e-6)
arrow = sp.Matrix([-1 - 3, 5 - 2])
u = arrow / arrow.norm()
D = g[0] * u[0] + g[1] * u[1]
h = 1e-6
Dfd = (fn(3 + h * float(u[0]), 2 + h * float(u[1])) - fn(3 - h * float(u[0]), 2 - h * float(u[1]))) / (2 * h)
num(lv, 0, 2, D, Dfd, {'not-unit': g[0] * arrow[0] + g[1] * arrow[1], 'reversed': -D}, agree=1e-6)
lv.claim(u[0] == sp.Rational(-4, 5) and u[1] == sp.Rational(3, 5), 'L2 item 0 part 3: unit arrow (-0.8, 0.6)')
ucont = (sp.Rational(3, 5), sp.Rational(-4, 5))
lv.claim(g[0] * ucont[0] + g[1] * ucont[1] == 0 and ucont[0] ** 2 + ucont[1] ** 2 == 1 and ucont[0] > 0, 'L2 item 0 part 4: (0.6, -0.8) is a unit contour arrow with positive first component')
# method 2: search the unit circle for the zero of the directional derivative with positive first component
th0 = bisect(lambda q: 12 * math.cos(q) + 9 * math.sin(q), -math.pi / 2, 0)
lv.claim(abs(math.cos(th0) - 0.6) < 1e-9 and abs(math.sin(th0) + 0.8) < 1e-9, 'L2 item 0 part 4: bisection on the circle finds (0.6, -0.8)')
expr(lv, 0, 3, ucont, {'gradient-dir': (sp.Rational(4, 5), sp.Rational(3, 5)), 'other-way': (-ucont[0], -ucont[1]), 'not-unit': (9, -12)})
ang = sp.deg(sp.acos(sp.Rational(15, 2) / L))
ang2 = math.degrees(bisect(lambda q: 15 * math.cos(q) - 7.5, 0, math.pi / 2))
num(lv, 0, 4, ang, ang2, {'sine': math.degrees(math.asin(0.5)), 'obtuse': math.degrees(math.acos(-0.5))}, agree=1e-7)

# ---- item 1 p-two-book-risk: sigma = sqrt(x^2 + y^2) at (3, 4)
s_ = sp.sqrt(x ** 2 + y ** 2)
sn = sp.lambdify((x, y), s_)
pt = {x: 3, y: 4}
gs = (sp.diff(s_, x).subs(pt), sp.diff(s_, y).subs(pt))
lv.claim(abs(fd(sn, (3, 4), 0) - 0.6) < 1e-8 and abs(fd(sn, (3, 4), 1) - 0.8) < 1e-8, 'L2 item 1 part 1: finite differences give (0.6, 0.8)')
expr(lv, 1, 0, gs, {'no-root': (6, 8), 'half': (gs[0] / 2, gs[1] / 2)})
plane = 5 + gs[0] * (x - 3) + gs[1] * (y - 4)
expr(lv, 1, 1, sp.expand(plane), {'no-shift': 5 + gs[0] * x + gs[1] * y, 'carried': sp.expand(5 + 6 * (x - 3) + 8 * (y - 4))})
lv.claim(5 - sp.Rational(9, 5) - sp.Rational(16, 5) == 0, 'L2 item 1 part 2: 5 - 1.8 - 3.2 = 0')
z3 = plane.subs({x: sp.Rational(16, 5), y: sp.Rational(37, 10)})
true3 = math.sqrt(3.2 ** 2 + 3.7 ** 2)
num(lv, 1, 2, z3, 0.6 * 3.2 + 0.8 * 3.7, {'exact': round(true3, 2), 'no-shift': 5 + z3, 'unit-slopes': 5 + 0.2 - 0.3, 'carried': 6 * 3.2 + 8 * 3.7 - 45}, printed=(4.88,))
lv.claim(abs(true3 - 4.89) < 0.005, 'L2 item 1 part 3: the true risk rounds to 4.89')
for v in (1.92, 2.96):
    say(lv, 1, 2, 'feedback.correct', v)
err4 = sp.sqrt(sp.Rational(2393, 100)) - sp.Rational(488, 100)
num(lv, 1, 3, err4, true3 - 4.88, {'sign': -0.0118, 'squares': 23.93 - 4.88 ** 2}, printed=(0.0118,), agree=1e-9)
lv.claim(round(float(err4), 4) == 0.0118 and round(23.93 - 4.88 ** 2, 4) == 0.1156, 'L2 item 1 part 4: error 0.0118, squares slip 0.1156')
say(lv, 1, 3, 'feedback.correct', r'\sqrt{23.93}')
say(lv, 1, 3, 'feedback.correct', 4.8918)
pred = 0.0118 / 4
z5 = float(plane.subs({x: sp.Rational(31, 10), y: sp.Rational(385, 100)}))
true5 = math.sqrt(3.1 ** 2 + 3.85 ** 2) - z5
num(lv, 1, 4, pred, float(err4) / 4, {'halved': 0.0118 / 2, 'same': 0.0118, 'cube': 0.0118 / 8}, printed=(0.0030, round(true5, 4)), agree=2e-2)
lv.claim(abs(z5 - 4.94) < 1e-12 and round(math.sqrt(3.1 ** 2 + 3.85 ** 2), 4) == 4.9429 and round(true5, 4) == 0.0029, 'L2 item 1 part 5: plane 4.94, true 4.9429, true error 0.0029')
lv.claim(true5 > 0 and 3.5 < float(err4) / true5 < 4.5, 'L2 item 1 part 5: halving the step divides the true error by about 4')

# ---- item 2 p-fit-descent: L = 4(a - 1)^2 + (b + 2)^2
Lf = 4 * (a - 1) ** 2 + (b + 2) ** 2
grad = sp.Matrix([sp.diff(Lf, a), sp.diff(Lf, b)])
Ln = sp.lambdify((a, b), Lf)
g0 = tuple(grad.subs({a: 0, b: 0}))
lv.claim(abs(fd(Ln, (0, 0), 0) + 8) < 1e-6 and abs(fd(Ln, (0, 0), 1) - 4) < 1e-6, 'L2 item 2 part 1: finite differences give (-8, 4)')
expr(lv, 2, 0, g0, {'sign': (-g0[0], -g0[1]), 'no-two': (g0[0] / 2, g0[1] / 2)})


def descend(s, k, start=(0.0, 0.0)):
    pa, pb = start
    for _ in range(k):
        pa, pb = pa - s * 8 * (pa - 1), pb - s * 2 * (pb + 2)
    return pa, pb


s1 = sp.Rational(1, 10)
p1 = (0 - s1 * g0[0], 0 - s1 * g0[1])
lv.claim(all(abs(float(q) - r) < 1e-12 for q, r in zip(p1, descend(0.1, 1))), 'L2 item 2 part 2: simulation agrees on step 1')
expr(lv, 2, 1, p1, {'uphill': (s1 * g0[0], s1 * g0[1]), 'carried': (s1 * 4, -s1 * 2), 'no-scale': (-g0[0], -g0[1])})
b2 = (p1[1] + 2) * (1 - 2 * s1) - 2
num(lv, 2, 2, b2, descend(0.1, 2)[1], {'linear': p1[1] - s1 * 4, 'plus-two': b2 + 2}, printed=(-0.72,))
lv.claim(2 * (p1[1] + 2) == sp.Rational(16, 5), 'L2 item 2 part 3: L_b = 3.2 at b = -0.4')


def settles(s):
    pa, pb = descend(s, 4000, (0.0, 0.0))
    return abs(pa - 1) < 1e-6 and abs(pb + 2) < 1e-6


s_lim = sp.Rational(1, 4)  # |1 - 8s| < 1 and |1 - 2s| < 1
sim_lim = bisect(lambda s: 1 if settles(s) else -1, 0.2, 0.3, 40)
lv.claim(settles(0.249) and not settles(0.251), 'L2 item 2 part 4: simulation settles at 0.249 and fails at 0.251')
num(lv, 2, 3, s_lim, sim_lim, {'b-only': 1, 'no-zigzag': sp.Rational(1, 8)}, agree=1e-3)
k_log = math.ceil(math.log(0.005) / math.log(0.8))
k_sim = next(k for k in range(1, 200) if abs(descend(0.1, k)[0] - 1) < 0.01 and abs(descend(0.1, k)[1] + 2) < 0.01)
num(lv, 2, 4, k_sim, k_log, {'used-a': next(k for k in range(1, 50) if 0.2 ** k < 0.01), 'one-short': k_sim - 1,
                              'start-one': next(k for k in range(1, 50) if 0.8 ** k < 0.01)})
lv.claim(round(0.8 ** 23, 4) == 0.0059 and round(0.8 ** 24, 4) == 0.0047 and round(2 * 0.8 ** 24, 4) == 0.0094 and round(2 * 0.8 ** 23, 4) == 0.0118,
         'L2 item 2 part 5: printed powers 0.0059, 0.0047, 0.0094, 0.0118')

lv.check_wrongs('problems')
results.append(lv)

# ====================================================================== level 3
lv = Level('multivar', 3)

# ---- item 0 p-two-level-points: f = 2x^3 - 6xy + 3y^2
f = 2 * x ** 3 - 6 * x * y + 3 * y ** 2
fn = sp.lambdify((x, y), f)
sols = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
xs = sorted(s[x] for s in sols)
grid = sorted({round(px, 6) for px in [k / 1000 for k in range(-3000, 3001)]
               for py in [px] if abs(fd(fn, (px, py), 0)) < 1e-6 and abs(fd(fn, (px, py), 1)) < 1e-6})
numset(lv, 0, 0, xs, grid, {'sign': [0, -1]})
H = sp.hessian(f, (x, y))
Dx = sp.expand(H.det())
Dfd = lambda px, py: (fd(lambda q, r: fd(fn, (q, r), 0, 1e-4), (px, py), 0, 1e-4) * fd(lambda q, r: fd(fn, (q, r), 1, 1e-4), (px, py), 1, 1e-4)
                      - fd(lambda q, r: fd(fn, (q, r), 0, 1e-4), (px, py), 1, 1e-4) ** 2)
lv.claim(abs(Dfd(0.7, 0.3) - float(Dx.subs({x: 0.7}))) < 1e-3, 'L3 item 0 part 2: finite-difference Hessian agrees with 72x - 36 at x = 0.7')
expr(lv, 0, 1, Dx, {'plus': 72 * x + 36, 'no-mixed': H[0, 0] * H[1, 1], 'no-square': H[0, 0] * H[1, 1] - H[0, 1]})
num(lv, 0, 2, Dx.subs(x, 0), Dfd(0, 0), {'plus': 36, 'no-mixed': 0, 'no-square': 6}, agree=1e-3)
lv.claim(classify(H.subs({x: 0, y: 0})) == 'saddle', 'L3 item 0 part 3: (0, 0) is a saddle (eigenvalues of opposite sign)')
lv.claim(classify(H.subs({x: 1, y: 1})) == 'pit' and Dx.subs(x, 1) == 36 and H[0, 0].subs(x, 1) == 12, 'L3 item 0 part 4: (1, 1) is a pit, D = 36, f_xx = 12')
lv.claim(min(fn(1 + 0.01 * math.cos(q), 1 + 0.01 * math.sin(q)) for q in [k * 0.01 for k in range(629)]) > fn(1, 1), 'L3 item 0 part 4: f rises on a small circle round (1, 1)')
pick(lv, 0, 3, 'pit')
num(lv, 0, 4, f.subs({x: 1, y: 1}), fn(1, 1), {'plus-xy': 2 + 6 + 3, 'origin': fn(0, 0)})
lv.claim(fn(-3, 0) < fn(1, 1), 'L3 item 0 part 5: f(-3, 0) = -54 is below the pit, so the pit is only local')

# ---- item 1 p-capital-limit: P = 14x + 6y - x^2 - y^2, capital x + y = 6
Pf = 14 * x + 6 * y - x ** 2 - y ** 2
Pn = sp.lambdify((x, y), Pf)
st = sp.solve([sp.diff(Pf, x), sp.diff(Pf, y)], [x, y], dict=True)[0]
best = max(((px / 100, py / 100) for px in range(0, 1201) for py in range(0, 601, 1)), key=lambda q: Pn(*q))
lv.claim(abs(best[0] - 7) < 1e-9 and abs(best[1] - 3) < 1e-9, 'L3 item 1 part 1: grid search finds the free peak at (7, 3)')
expr(lv, 1, 0, (st[x], st[y]), {'no-half': (14, 6), 'swapped': (st[y], st[x])})
HP = sp.hessian(Pf, (x, y))
lv.claim(classify(HP) == 'peak' and HP.det() == 4 and Pf.subs(st) == 58, 'L3 item 1 part 2: peak, D = 4, P = 58')
pick(lv, 1, 1, 'peak')
say(lv, 1, 1, 'feedback.correct', 58)
lag = sp.solve([sp.diff(Pf, x) - lam, sp.diff(Pf, y) - lam, x + y - 6], [x, y, lam], dict=True)[0]
line = max((q / 10000 for q in range(0, 60001)), key=lambda q: Pn(q, 6 - q))
num(lv, 1, 2, lag[x], line, {'scaled': 7 * sp.Rational(6, 10), 'even': 3, 'free': 7}, agree=1e-9)
lv.claim(lag[y] == 1 and Pf.subs({x: 5, y: 1}) == 50, 'L3 item 1 part 3: (5, 1) with P = 50')
lam_fd = (max(Pn(q / 10000, 6.001 - q / 10000) for q in range(0, 60011)) - max(Pn(q / 10000, 5.999 - q / 10000) for q in range(0, 59991))) / 0.002
num(lv, 1, 3, lag[lam], lam_fd, {'sign': -lag[lam], 'value': Pf.subs({x: 5, y: 1})}, agree=1e-3)
est = 50 + lag[lam] * sp.Rational(1, 2)
ex65 = sp.solve([sp.diff(Pf, x) - lam, sp.diff(Pf, y) - lam, x + y - sp.Rational(13, 2)], [x, y, lam], dict=True)[0]
exact65 = Pf.subs({x: ex65[x], y: ex65[y]})
num(lv, 1, 4, est, 50 + 4 * 0.5, {'full-lambda': 50 + lag[lam], 'no-lambda': 50 + 0.5, 'sign': 50 - lag[lam] / 2}, printed=(52, float(exact65)))
lv.claim(exact65 == sp.Rational(51875, 1000) and ex65[x] == sp.Rational(21, 4) and ex65[y] == sp.Rational(5, 4), 'L3 item 1 part 5: exact best 51.875 at (5.25, 1.25)')
lv.claim(abs(max(Pn(q / 10000, 6.5 - q / 10000) for q in range(0, 65001)) - 51.875) < 1e-9, 'L3 item 1 part 5: line search on x + y = 6.5 gives 51.875')
say(lv, 1, 4, 'feedback.correct', 51.875)

# ---- item 2 p-min-variance-pair: vols 0.4, 0.25, rho 0.3 (fix pass 1.3 b: was 0.3, 0.2, 0.25)
s1_, s2_, rho = sp.Rational(4, 10), sp.Rational(1, 4), sp.Rational(3, 10)
cov = rho * s1_ * s2_
lv.claim(2 * cov == sp.Rational(6, 100), 'L3 item 2 prose: 2 rho sigma1 sigma2 = 0.06')
lv.claim(s1_ ** 2 == sp.Rational(16, 100) and s2_ ** 2 == sp.Rational(625, 10000), 'L3 item 2 prose: variances 0.16 and 0.0625')
var = w ** 2 * s1_ ** 2 + (1 - w) ** 2 * s2_ ** 2 + 2 * w * (1 - w) * cov
quad_ = sp.expand(var)
import numpy as np  # noqa: E402
ws = np.linspace(-1, 2, 31)
coef = np.polyfit(ws, [float(var.subs(w, q)) for q in ws], 2)
lv.claim(np.allclose(coef, [0.1625, -0.065, 0.0625]), 'L3 item 2 part 1: a numerical fit of the variance gives 0.1625, -0.065, 0.0625')
lv.claim(sp.Rational(16, 100) + sp.Rational(625, 10000) - sp.Rational(6, 100) == sp.Rational(1625, 10000) and -sp.Rational(125, 1000) + sp.Rational(6, 100) == -sp.Rational(65, 1000), 'L3 item 2 part 1: explain arithmetic 0.16 + 0.0625 - 0.06 and -0.125 + 0.06')
no_cross = sp.expand(w ** 2 * s1_ ** 2 + (1 - w) ** 2 * s2_ ** 2)
half_cross = sp.expand(w ** 2 * s1_ ** 2 + (1 - w) ** 2 * s2_ ** 2 + w * (1 - w) * cov)
expr(lv, 2, 0, quad_, {'no-cross': no_cross, 'half-cross': half_cross})
lv.claim(W(lv, 2, 0).get('form') == 'expanded', 'L3 item 2 part 1: form expanded, so retyping the prose fails')
wstar = sp.solve(sp.diff(quad_, w), w)[0]
wformula = (s2_ ** 2 - rho * s1_ * s2_) / (s1_ ** 2 + s2_ ** 2 - 2 * rho * s1_ * s2_)
vn = sp.lambdify(w, quad_)
wgrid = min((q / 100000 for q in range(0, 100001)), key=vn)
num(lv, 2, 1, wstar, wgrid, {'no-two': sp.Rational(65, 1000) / sp.Rational(1625, 10000), 'gave-b': 1 - wstar,
                              'carried': sp.solve(sp.diff(no_cross, w), w)[0]}, agree=1e-5)
lv.claim(wstar == wformula and wstar == sp.Rational(1, 5), 'L3 item 2 part 2: the lesson formula gives 0.2 too')
lv.claim(sp.diff(quad_, w) == sp.Rational(325, 1000) * w - sp.Rational(65, 1000), 'L3 item 2 part 2: derivative 0.325w - 0.065')
var_min = quad_.subs(w, wstar)
num(lv, 2, 2, sp.sqrt(var_min), math.sqrt(min(vn(q / 100000) for q in range(0, 100001))),
    {'variance': var_min, 'weighted': wstar * s1_ + (1 - wstar) * s2_, 'carried-half': sp.sqrt(quad_.subs(w, sp.Rational(65, 1000) / sp.Rational(1625, 10000)))}, printed=(0.2366,))
lv.claim(var_min == sp.Rational(56, 1000), 'L3 item 2 part 3: variance 0.056')
lv.claim(sp.Rational(1625, 10000) * sp.Rational(4, 100) == sp.Rational(65, 10000) and sp.Rational(65, 10000) - sp.Rational(13, 1000) + sp.Rational(625, 10000) == var_min, 'L3 item 2 part 3: 0.0065 - 0.013 + 0.0625 = 0.056')
lv.claim(wstar * s1_ + (1 - wstar) * s2_ == sp.Rational(28, 100) and abs(float(sp.sqrt(sp.Rational(625, 10000))) - 0.25) < 1e-12, 'L3 item 2 part 3: weighted 0.28, B volatility 0.25 above sigma_p')
for v in (0.0065, 0.013, 0.0625, 0.056):
    say(lv, 2, 2, 'feedback.correct', v)
w1, w2 = sp.symbols('w1 w2', real=True)
V2 = w1 ** 2 * s1_ ** 2 + w2 ** 2 * s2_ ** 2 + 2 * w1 * w2 * cov
lv.claim(sp.expand(sp.diff(V2, w1) - (sp.Rational(32, 100) * w1 + sp.Rational(6, 100) * w2)) == 0, 'L3 item 2 part 4: dV/dw1 = 0.32 w1 + 0.06 w2')
sol = sp.solve([sp.diff(V2, w1) - lam, sp.diff(V2, w2) - lam, w1 + w2 - 1], [w1, w2, lam], dict=True)[0]
lv.claim(sol[w1] == sp.Rational(1, 5) and sol[w2] == sp.Rational(4, 5), 'L3 item 2 part 4: Lagrange gives w = (0.2, 0.8)')
lam_at = sp.diff(V2, w1).subs({w1: sp.Rational(1, 5), w2: sp.Rational(4, 5)})
num(lv, 2, 3, sol[lam], 2 * float(var_min), {'variance': var_min, 'no-cross': sp.Rational(32, 100) * sp.Rational(1, 5)})
lv.claim(lam_at == sol[lam] and sol[lam] == sp.Rational(112, 1000) and sp.diff(V2, w2).subs({w1: sp.Rational(1, 5), w2: sp.Rational(4, 5)}) == sol[lam], 'L3 item 2 part 4: both partials equal 0.112')
lv.claim(sp.diff(V2, w2) == sp.Rational(125, 1000) * w2 + sp.Rational(6, 100) * w1, 'L3 item 2 part 4: dV/dw2 = 0.125 w2 + 0.06 w1')
for v in (0.064, 0.048, 0.112, 0.1, 0.012):
    say(lv, 2, 3, 'feedback.correct' if v in (0.064, 0.048, 0.112) else 'explain.text', v)
est = var_min + sol[lam] * sp.Rational(2, 100)
# method 2: minimise the variance on w1 + w2 = 1.02 by a line search
vb = sp.lambdify((w1, w2), V2)
line_min = min(vb(q / 100000, 1.02 - q / 100000) for q in range(0, 102001))
num(lv, 2, 4, est, var_min * sp.Rational(102, 100) ** 2, {'sigma-lambda': var_min + var_min * sp.Rational(2, 100), 'no-change': var_min,
                                                       'whole-lambda': var_min + sol[lam]}, printed=(0.05824, 0.0582, round(line_min, 4)), agree=1e-3)
lv.claim(abs(line_min - float(var_min) * 1.0404) < 1e-9 and round(float(var_min) * 1.0404, 4) == 0.0583 and est == sp.Rational(5824, 100000), 'L3 item 2 part 5: estimate 0.05824; exact 0.056 x 1.0404 = 0.0582624, a line search agrees')
say(lv, 2, 4, 'feedback.correct', 0.00224)

lv.check_wrongs('problems')
results.append(lv)

# ====================================================================== level 4
# Method 2 here is scipy quadrature (dblquad / quad), a fine midpoint sum, Monte Carlo or bisection.
from scipy import integrate as si  # noqa: E402
import numpy as np  # noqa: E402

U, V, R, TH = sp.symbols('u v r th', real=True)
lv = Level('multivar', 4)

# ---- item 0 p-weighted-rectangle: f = c x y^2 on [0,1] x [0,2]
slice_ = sp.integrate(x * y ** 2, (x, 0, 1))
lv.claim(abs(si.quad(lambda q: q * 1.7 ** 2, 0, 1)[0] - float(slice_.subs(y, 1.7))) < 1e-12, 'L4 item 0 part 1: quad of x(1.7)^2 matches the slice')
expr(lv, 0, 0, slice_, {'wrong-var': sp.integrate(x * y ** 2, y), 'no-half': y ** 2})
tot = sp.integrate(slice_, (y, 0, 2))
tot_num = si.dblquad(lambda yy, xx: xx * yy ** 2, 0, 1, 0, 2)[0]
c4 = 1 / tot
num(lv, 0, 1, c4, 1 / tot_num, {'not-inverted': tot, 'no-third': 1 / (sp.Rational(1, 2) * 2 ** 3),
                                'carried': 1 / sp.integrate(y ** 2, (y, 0, 2))}, printed=(0.75,))
lv.claim(sp.Rational(1, 2) * 8 == 4 and 1 / sp.Rational(4) == sp.Rational(1, 4), 'L4 item 0 part 2: no-third slip takes int_0^2 y^2 dy as 8, total 4, c = 1/4')
inner = sp.integrate(c4 * x * y ** 2, (y, 0, 2 * x))
expr(lv, 0, 2, inner, {'rect-limits': sp.integrate(c4 * x * y ** 2, (y, 0, 2)), 'cube-two': c4 * x * 2 * x ** 3 / 3,
                       'carried': sp.integrate(tot * x * y ** 2, (y, 0, 2 * x))})
pev = sp.integrate(inner, (x, 0, 1))
rng = np.random.default_rng(4)
# method 2: draw (X, Y) by inverse CDFs (X has density 2x, Y has density 3y^2/8, independent) and count Y <= 2X
XS = np.sqrt(rng.random(2_000_000))
YS = 2 * rng.random(2_000_000) ** (1 / 3)
mc = float(np.mean(YS <= 2 * XS))
num(lv, 0, 3, pev, mc, {'rect-limits': 1, 'cube-two': sp.integrate(c4 * x * 2 * x ** 3 / 3, (x, 0, 1)), 'complement': 1 - pev,
                        'carried': sp.integrate(sp.integrate(tot * x * y ** 2, (y, 0, 2 * x)), (x, 0, 1))}, printed=(0.4,), agree=2e-3)
lv.claim(abs(si.dblquad(lambda yy, xx: 0.75 * xx * yy ** 2, 0, 1, 0, lambda xx: 2 * xx)[0] - 0.4) < 1e-10, 'L4 item 0 part 4: dblquad over y <= 2x gives 0.4')
say(lv, 0, 1, 'feedback.correct', 8 / 6)

# ---- item 1 p-corner-sprinkler: d = 9 - (x^2 + y^2) on the quarter disc of radius 3
# fix pass 1.3 c: part 1 is now the depth in polar, d = 9 - r^2 (the strip limit it replaced fed no later part)
depth_r = sp.simplify((9 - (x ** 2 + y ** 2)).subs({x: R * sp.cos(TH), y: R * sp.sin(TH)}))
lv.claim(sp.simplify(depth_r - (9 - R ** 2)) == 0, 'L4 item 1 part 1: x^2 + y^2 = r^2 in polar, so d = 9 - r^2')
expr(lv, 1, 0, 9 - R ** 2, {'r-not-squared': 9 - R, 'with-r': (9 - R ** 2) * R})
lv.claim(9 - 0 == 9 and 9 - 3 ** 2 == 0, 'L4 item 1 part 1: the depth is 9 mm at the sprinkler and 0 at r = 3')
lv.claim('Using the depth $9 - r^2$ from part 1' in lv.files['problems-4']['items'][1]['parts'][1]['question'], 'L4 item 1 part 2: restates the depth from part 1')
integrand = sp.expand((9 - R ** 2) * R)
expr(lv, 1, 1, integrand, {'no-r': 9 - R ** 2, 'r-not-squared': (9 - R) * R})
inner_r = sp.integrate(integrand, (R, 0, 3))
num(lv, 1, 2, inner_r, si.quad(lambda q: 9 * q - q ** 3, 0, 3)[0], {'no-r': sp.integrate(9 - R ** 2, (R, 0, 3)), 'r-not-squared': sp.integrate((9 - R) * R, (R, 0, 3))}, printed=(20.25,))
for val in (40.5, 20.25):
    say(lv, 1, 2, 'feedback.correct', val)
water = inner_r * sp.pi / 2
cart = si.dblquad(lambda yy, xx: 9 - xx ** 2 - yy ** 2, 0, 3, 0, lambda xx: math.sqrt(9 - xx ** 2))[0]
num(lv, 1, 3, water, cart, {'full-turn': inner_r * 2 * sp.pi, 'no-theta': inner_r, 'carried': 18 * sp.pi / 2}, printed=(31.81,), agree=1e-8)
lv.claim(water == sp.Rational(81, 8) * sp.pi, 'L4 item 1 part 4: water = 81 pi / 8')
aa = sp.symbols('aa', positive=True)
half = [s_ for s_ in sp.solve(sp.Eq(sp.integrate(integrand, (R, 0, aa)), inner_r / 2), aa) if s_ < 3][0]
a_bis = bisect(lambda q: (81 - (9 - q * q) ** 2) / 4 - 10.125, 0, 3)
num(lv, 1, 4, half, a_bis, {'half-radius': 1.5, 'no-root': half ** 2, 'half-area': 3 / sp.sqrt(2)}, printed=(1.62, round(a_bis, 4)))
lv.claim(sp.simplify(sp.integrate(integrand, (R, 0, aa)) - (81 - (9 - aa ** 2) ** 2) / 4) == 0, 'L4 item 1 part 5: int_0^a (9r - r^3) dr = (81 - (9 - a^2)^2) / 4')
lv.claim(sp.simplify(half ** 2 - (9 - 9 / sp.sqrt(2))) == 0 and round(float(half ** 2), 3) == 2.636, 'L4 item 1 part 5: a^2 = 9 - 9/sqrt2 = 2.636')
lv.claim(abs(float(water / 2) - float(sp.Rational(81, 16) * sp.pi)) < 1e-12, 'L4 item 1 part 5: half the water is 81 pi / 16')

# ---- item 2 p-drone-landing: f = c exp(-(x^2 + y^2)/32), sigma = 4 (fix pass 1.3 c: was /8, which repeated lesson l16's e^{-x^2/8})
K32, S4, RAD = 32, 4, 6
one = sp.integrate(sp.exp(-x ** 2 / K32), (x, -sp.oo, sp.oo))
num(lv, 2, 0, one, si.quad(lambda q: math.exp(-q * q / K32), -np.inf, np.inf)[0], {'no-scale': sp.sqrt(sp.pi), 'inverted': sp.sqrt(sp.pi) / (4 * sp.sqrt(2)),
                                                                                    'sigma-root32': sp.sqrt(K32) * sp.sqrt(2 * sp.pi)}, printed=(10.0265,))
lv.claim(sp.simplify(one - sp.sqrt(K32 * sp.pi)) == 0 and sp.simplify(one - 4 * sp.sqrt(2 * sp.pi)) == 0, 'L4 item 2 part 1: the integral is sqrt(32 pi) = 4 sqrt(2 pi)')
plane = sp.integrate(sp.exp(-R ** 2 / K32) * R, (R, 0, sp.oo)) * 2 * sp.pi
lv.claim(sp.simplify(plane - one ** 2) == 0 and sp.simplify(plane - 32 * sp.pi) == 0, 'L4 item 2 part 2: polar 2 pi x 16 equals the square of part 1, 32 pi')
expr(lv, 2, 1, one ** 2, {'not-squared': one, 'doubled': 2 * one, 'carried': sp.pi})
c_d = 1 / plane
lv.claim(abs(float(c_d) * si.dblquad(lambda yy, xx: math.exp(-(xx * xx + yy * yy) / K32), -80, 80, -80, 80)[0] - 1) < 1e-8, 'L4 item 2 part 3: c times a dblquad of the plane is 1')
expr(lv, 2, 2, c_d, {'not-inverted': plane, 'from-root': 1 / one, 'carried': 1 / sp.pi})
say(lv, 2, 2, 'explain.text', round(float(c_d), 4))
p2 = c_d * 2 * sp.pi * sp.integrate(sp.exp(-R ** 2 / K32) * R, (R, 0, RAD))
pts = rng.normal(0, S4, size=(2_000_000, 2))
mc2 = float(np.mean((pts ** 2).sum(axis=1) <= RAD ** 2))
num(lv, 2, 3, p2, mc2, {'r-not-squared': 1 - sp.exp(-sp.Rational(RAD, K32)), 'no-2pi': p2 / (2 * sp.pi), 'outside': 1 - p2}, printed=(0.6753,), agree=2e-3)
lv.claim(abs(float(c_d) * si.dblquad(lambda yy, xx: math.exp(-(xx * xx + yy * yy) / K32), -RAD, RAD, lambda xx: -math.sqrt(RAD ** 2 - xx * xx), lambda xx: math.sqrt(RAD ** 2 - xx * xx))[0] - float(p2)) < 1e-8, 'L4 item 2 part 4: a Cartesian double integral of the density over the disc agrees with the closed form')
lv.claim(sp.simplify(p2 - (1 - sp.exp(-sp.Rational(9, 8)))) == 0 and sp.simplify(sp.integrate(sp.exp(-R ** 2 / K32) * R, (R, 0, RAD)) - 16 * (1 - sp.exp(-sp.Rational(9, 8)))) == 0, 'L4 item 2 part 4: the chance is 1 - e^(-9/8); the radial integral is 16 (1 - e^(-9/8))')
a90 = sp.sqrt(K32 * sp.log(10))
num(lv, 2, 4, a90, bisect(lambda q: 1 - math.exp(-q * q / K32) - 0.9, 0, 20), {'no-root': K32 * sp.log(10), 'tail-swap': sp.sqrt(K32 * sp.log(sp.Rational(10, 9))), 'log10': sp.sqrt(K32)}, printed=(8.58,))
lv.claim(round(float(K32 * sp.log(10)), 2) == 73.68 and round(math.log(10), 4) == 2.3026, 'L4 item 2 part 5: 32 ln 10 = 73.68, ln 10 = 2.3026')
lv.claim(round(float(p2) * 100) == 68 and 1 < float(a90) / RAD < 1.5, 'L4 item 2 part 5: the explanation says 68% and growth by under a half (8.58 / 6 = 1.43)')
lv.claim(round(float(a90), 2) == 8.58 and round(float(sp.sqrt(K32 * sp.log(sp.Rational(10, 9)))), 2) == 1.84 and round(float(sp.sqrt(K32)), 2) == 5.66, 'L4 item 2 part 5: key 8.58 and wrong values 1.84 and 5.66')
import glob  # noqa: E402
lv.claim(not [g for g in glob.glob(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'multivar', '*.json')) if f'/{K32}}}' in open(g).read() and 'problems-4' not in g],
         'L4 item 2: no other multivar file has an exponent over 32')

lv.check_wrongs('problems')
results.append(lv)

# ====================================================================== level 5
lv = Level('multivar', 5)
z, mu = sp.symbols('z mu', real=True)

# ---- item 0 p-three-strategies: G = 3x + 2y + z - (x^2 + y^2 + z^2) on the simplex
G = 3 * x + 2 * y + z - (x ** 2 + y ** 2 + z ** 2)
Gn = sp.lambdify((x, y, z), G)
sol = sp.solve([sp.diff(G, q) - lam for q in (x, y, z)] + [x + y + z - 1], [x, y, z, lam], dict=True)[0]
Gs = 3 * x + 2 * y + z - (x ** 2 + y ** 2 + z ** 2) / 2      # the no-two slip: d/dx(x^2) taken as x
sol_slip = sp.solve([sp.diff(Gs, q) - lam for q in (x, y, z)] + [x + y + z - 1], [x, y, z, lam], dict=True)[0]
# method 2: the same point by a fine search over the plane (z = 1 - x - y), no sign limit
grid = np.linspace(-0.5, 1.5, 2001)
gx_, gy_ = np.meshgrid(grid, grid)
gv = Gn(gx_, gy_, 1 - gx_ - gy_)
k = np.unravel_index(np.argmax(gv), gv.shape)
xs_, ys_ = gx_[k], gy_[k]
lam2 = 3 - 2 * xs_
num(lv, 0, 0, sol[lam], lam2, {'no-two': sol_slip[lam], 'no-budget': 2}, printed=(1.3333,), agree=2e-3)
num(lv, 0, 1, sol[z], 1 - xs_ - ys_, {'sign': -sol[z], 'carried': sol_slip[z], 'carried-budget': (1 - sp.Integer(2)) / 2}, printed=(-0.1667,), agree=2e-3)
lv.claim(sol[x] == sp.Rational(5, 6) and sol[y] == sp.Rational(1, 3), 'L5 item 0 part 2: x = 5/6, y = 1/3')
lv.claim(sol_slip[z] == 1 - sol_slip[lam], 'L5 item 0 part 2: the carried slip is z = 1 - lambda')
pick(lv, 0, 2, 'edges')
edge = sp.solve([sp.diff(G, x) - lam, sp.diff(G, y) - lam, sp.diff(G, z) - lam - mu, x + y + z - 1, z], [x, y, z, lam, mu], dict=True)[0]
tt = np.linspace(0, 1, 100001)
x_edge = tt[np.argmax(Gn(tt, 1 - tt, 0))]
num(lv, 0, 3, edge[x], x_edge, {'clipped': sol[x], 'rescaled': sol[x] / (sol[x] + sol[y]), 'equal': sp.Rational(1, 2)}, printed=(0.75,), agree=1e-4)
lv.claim(edge[lam] == sp.Rational(3, 2), 'L5 item 0 part 4: lambda = 1.5 on the edge')
best = G.subs({x: edge[x], y: edge[y], z: 0})
# method 2: brute force over the whole allowed triangle
sv = gv.copy()
sv[(gx_ < 0) | (gy_ < 0) | (1 - gx_ - gy_ < -1e-12)] = -np.inf
brute = float(sv.max())
num(lv, 0, 4, best, brute, {'infeasible': G.subs(sol), 'clipped': G.subs({x: sol[x], y: sol[y], z: 0}), 'corner': Gn(1, 0, 0)}, printed=(2.125,), agree=1e-6)
ex0 = sp.solve([sp.diff(G, y) - sp.diff(G, z), y + z - 1], [y, z], dict=True)[0]
lv.claim(ex0 == {y: sp.Rational(3, 4), z: sp.Rational(1, 4)} and G.subs({x: 0, **ex0}) == sp.Rational(9, 8), 'L5 item 0 part 5: edge x = 0 is best at (0, 3/4, 1/4) with 1.125')
ey0 = sp.solve([sp.diff(G, x) - sp.diff(G, z), x + z - 1], [x, z], dict=True)[0]
lv.claim(ey0 == {x: 1, z: 0} and Gn(1, 0, 0) == 2, 'L5 item 0 part 5: edge y = 0 peaks at the corner (1, 0, 0) with 2')
lv.claim([Gn(0, 1, 0), Gn(0, 0, 1)] == [1, 0], 'L5 item 0 part 5: the other corners give 1 and 0')
lv.claim(round(float(G.subs(sol)), 4) == 2.1667, 'L5 item 0 part 5: the short point gives 2.1667')
for val in (2.25, 0.5, 0.5625, 0.0625):
    say(lv, 0, 4, 'feedback.correct', val)

# ---- item 1 p-dome-tent: floor x^2 + 4y^2 <= 4, roof 2 - (x^2 + 4y^2)/2, map x = 2u, y = v
J = sp.Matrix([2 * U, V]).jacobian([U, V]).det()
num(lv, 1, 0, abs(J), fd(lambda p, q: 2 * p, (0.3, 0.4), 0) * fd(lambda p, q: q, (0.3, 0.4), 1), {'inverse': 1 / abs(J), 'sum': 3})
roof = 2 - (x ** 2 + 4 * y ** 2) / 2
roof_uv = sp.expand(roof.subs({x: 2 * U, y: V}))
expr(lv, 1, 1, roof_uv, {'no-square': 2 - (2 * U ** 2 + 4 * V ** 2) / 2, 'inverse-map': sp.expand(roof.subs({x: U / 2, y: V}))})
vol = sp.integrate(sp.integrate((2 - 2 * R ** 2) * abs(J) * R, (R, 0, 1)), (TH, 0, 2 * sp.pi))
vol2 = si.dblquad(lambda yy, xx: max(0.0, 2 - (xx * xx + 4 * yy * yy) / 2), -2, 2, lambda xx: -math.sqrt(max(0.0, 1 - xx * xx / 4)), lambda xx: math.sqrt(max(0.0, 1 - xx * xx / 4)))[0]
expr(lv, 1, 2, vol, {'no-jacobian': vol / 2, 'no-r': 2 * sp.pi * sp.integrate((2 - 2 * R ** 2) * 2, (R, 0, 1)), 'carried': vol / 4})
lv.claim(abs(float(vol) - vol2) < 1e-6, f'L5 item 1 part 3: a Cartesian dblquad of the roof gives {vol2:.8f} = 2 pi')
lv.claim(sp.integrate(4 * (1 - R ** 2) * R, (R, 0, 1)) == 1, 'L5 item 1 part 3: int_0^1 4(1 - r^2) r dr = 1')
mom = sp.integrate(sp.integrate((2 - 2 * R ** 2) ** 2 / 2 * abs(J) * R, (R, 0, 1)), (TH, 0, 2 * sp.pi))
mom2 = si.dblquad(lambda yy, xx: max(0.0, 2 - (xx * xx + 4 * yy * yy) / 2) ** 2 / 2, -2, 2, lambda xx: -math.sqrt(max(0.0, 1 - xx * xx / 4)), lambda xx: math.sqrt(max(0.0, 1 - xx * xx / 4)))[0]
expr(lv, 1, 3, mom, {'no-half': 2 * mom, 'no-jacobian': mom / 2})
lv.claim(abs(float(mom) - mom2) < 1e-6 and sp.integrate((1 - R ** 2) ** 2 * R, (R, 0, 1)) == sp.Rational(1, 6), 'L5 item 1 part 4: dblquad agrees, int (1 - r^2)^2 r dr = 1/6')
# method 2 for the average: Monte Carlo points in the box [-2,2] x [-1,1] x [0,2] kept under the roof
P3 = rng.random((3_000_000, 3)) * np.array([4, 2, 2]) - np.array([2, 1, 0])
inside = P3[:, 2] <= 2 - (P3[:, 0] ** 2 + 4 * P3[:, 1] ** 2) / 2
num(lv, 1, 4, mom / vol, float(P3[inside, 2].mean()), {'roof': vol / (sp.pi * 2 * 1), 'no-half': 2 * mom / vol, 'flipped': vol / mom}, printed=(0.6667,), agree=3e-3)
lv.claim(sp.pi * 2 * 1 == 2 * sp.pi, 'L5 item 1 part 5: the floor ellipse has area pi x 2 x 1 = 2 pi')
say(lv, 1, 2, 'explain.text', round(float(vol), 2))

# ---- item 2 p-triangle-field: f = x y^2 on the triangle (0,0), (4,0), (0,2); map x = 4u, y = 2v
J2 = sp.Matrix([4 * U, 2 * V]).jacobian([U, V]).det()
num(lv, 2, 0, abs(J2), fd(lambda p, q: 4 * p, (0.3, 0.4), 0) * fd(lambda p, q: 2 * q, (0.3, 0.4), 1), {'inverse': 1 / abs(J2), 'sum': 6})
lv.claim(sp.Rational(1, 2) * abs(J2) == 4, 'L5 item 2 part 1: 8 x 1/2 = 4, the field area')
uv2 = sp.integrate(sp.integrate(U * V ** 2, (V, 0, 1 - U)), (U, 0, 1))
total = 128 * uv2
cart2 = si.dblquad(lambda yy, xx: xx * yy ** 2, 0, 4, 0, lambda xx: 2 - xx / 2)[0]
num(lv, 2, 1, total, cart2, {'no-jacobian': total / 8, 'square-two': 64 * uv2, 'inverse': 16 * uv2 / 8}, printed=(2.1333,))
lv.claim(uv2 == sp.Rational(1, 60) and sp.integrate(U * (1 - U) ** 3 / 3, (U, 0, 1)) == sp.Rational(1, 60), 'L5 item 2 part 2: int u(1-u)^3/3 du = 1/60')
avg = total / 4
num(lv, 2, 2, avg, cart2 / 4, {'uv-area': total / sp.Rational(1, 2), 'carried': total / 8 / 4}, printed=(0.5333,))
fx = x * y ** 2
lv.claim(sp.solve([sp.diff(fx, x), sp.diff(fx, y)], [x, y], dict=True) == [{y: 0}], 'L5 item 2 part 4: grad f = 0 only on y = 0')
hedge = fx.subs(x, 4 - 2 * y)
ystar = [s_ for s_ in sp.solve(sp.diff(hedge, y), y) if s_ > 0][0]
fmax = hedge.subs(y, ystar)
# method 2: brute force on a fine grid over the closed triangle
g2 = np.linspace(0, 4, 4001)
h2 = np.linspace(0, 2, 2001)
GX, GY = np.meshgrid(g2, h2)
FV = np.where(GX / 4 + GY / 2 <= 1 + 1e-12, GX * GY ** 2, -np.inf)
num(lv, 2, 3, fmax, float(FV.max()), {'corner': 0, 'mid-edge': fx.subs({x: 2, y: 1})}, printed=(2.3704,), agree=1e-5)
lv.claim(ystar == sp.Rational(4, 3) and 4 - 2 * ystar == sp.Rational(4, 3) and fmax == sp.Rational(64, 27), 'L5 item 2 part 4: peak at (4/3, 4/3) with 64/27')
share = avg / fmax
num(lv, 2, 4, share, (cart2 / 4) / float(FV.max()), {'mid-edge': avg / 2, 'inverted': fmax / avg, 'total': total / fmax}, printed=(0.225,), agree=1e-5)
lv.claim(share == sp.Rational(9, 40), 'L5 item 2 part 5: share = 9/40')

lv.check_wrongs('problems')
results.append(lv)

# ---------------------------------------------------------------- report
bad = [r for L_ in results for r in L_.results if not r[0]]
total = sum(len(L_.results) for L_ in results)
print(f'multivar problems: {total - len(bad)} of {total} checks passed')
for r in bad:
    print('BAD', r[1], r[2])
sys.exit(1 if bad else 0)
