"""Recompute every number stated in app/content/exams/topic-1.11.json by a second route and assert it at its path.

Route A is build.py (closed forms). Route B here is independent: exact Fractions, numerical contour, line, surface
and real integrals (trapezoid on circles, Simpson elsewhere), RK4 with fine steps for every ODE value, NumPy
eigenvalues and a series matrix exponential, numerical Laplace transforms, and the Carr-Madan integral against
Black-Scholes. Expression keys are evaluated from their LaTeX at sample points against route B; every accepted form
must agree and every wrong form must differ. A last pass reads every number in every learner-visible string of each
item. Whole numbers 0 to 10 are structure; every other number must match a route-B value for that item to its
printed precision. Exits 1 on any failure.
Run: python3 docs/briefs/exam-1.11-scripts/check_numbers.py
"""
import cmath
import json
import math
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, _walk, normalise  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.11.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def ok(cond, label):
    ex._rec(bool(cond), label, '')


def key(iid, value, part=None, tol=None):
    w = node(W(iid, part))
    t = tol if tol is not None else max(w['tol']['abs'] / 10, 1e-9)
    good = abs(w['answer'] - value) <= t
    ex._rec(good, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if good else 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    good = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9)
    ex._rec(good, f'{iid} wrong "{wid}" = {value!r}', '' if good else f'found {hit}')
    allow(iid, value)


def say(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


def correct_id(iid, want, part=None):
    w = node(W(iid, part))
    got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    want = sorted(want if isinstance(want, list) else [want])
    ex._rec(got == want, f'{iid}{"" if part is None else f" part {part}"} correct options {got} = {want}', '')
    ex._rec(w.get('shuffle') is True, f'{iid} shuffle true', '')
    ex._rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} every distractor has a why', '')


def simpson(f, a, b, n=20000):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / (3 * n) * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


def rk4(f, t0, y0, t1, n=20000):
    h = (t1 - t0) / n
    t, y = t0, np.array(y0, dtype=float)
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h / 2 * k1)
        k3 = f(t + h / 2, y + h / 2 * k2)
        k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
    return y


def circle_integral(f, c, rad, n=4096):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    z = c + rad * np.exp(1j * t)
    return np.sum(f(z) * 1j * rad * np.exp(1j * t)) * (2 * np.pi / n)


def loop_work(P_, Q_, xs, ys, dxs, dys, a=0.0, b=1.0, n=40000):
    return simpson(lambda t: P_(xs(t), ys(t)) * dxs(t) + Q_(xs(t), ys(t)) * dys(t), a, b, n)


def expm(M):
    M = np.array(M, dtype=float)
    s = max(0, int(np.ceil(np.log2(max(np.abs(M).sum(), 1)))) + 2)
    A = M / 2 ** s
    out, term = np.eye(len(M)), np.eye(len(M))
    for k in range(1, 30):
        term = term @ A / k
        out = out + term
    for _ in range(s):
        out = out @ out
    return out


# ------------------------------------------------------------------ LaTeX evaluation for expression keys
def _group(s, i):
    depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError(s)


def tex_py(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace(' ', '')
    s = re.sub(r'\\sin([a-z])', r'@(\1)', s)
    s = s.replace('\\sin', '@').replace('sin', '@')
    out, i = '', 0
    while i < len(s):
        if s.startswith('\\frac', i):
            a, i = _group(s, i + 5)
            b, i = _group(s, i)
            out += f'(({tex_py(a)})/({tex_py(b)}))'
        elif s.startswith('e^{', i):
            a, i = _group(s, i + 2)
            out += f'#(({tex_py(a)}))'
        elif s.startswith('e^', i):
            out += f'#({s[i + 2]})'
            i += 3
        elif s[i] == '^' and i + 1 < len(s) and s[i + 1] == '{':
            a, i = _group(s, i + 1)
            out += f'**({tex_py(a)})'
        else:
            out += s[i]
            i += 1
    out = out.replace('^', '**').replace('i', 'I')
    out = re.sub(r'(?<=[\dA-Za-z)])(?=[A-Za-z(@#])', '*', out)
    return out.replace('@', 'np.sin').replace('#', 'np.exp')


def tex_val(src, **v):
    return complex(eval(tex_py(src), {"np": np, "I": 1j}, v))


def expr_check(iid, fn, points, part=None, label=''):
    w = node(W(iid, part))
    forms = [w['answer']] + w['accept']
    for form in forms:
        good = all(abs(tex_val(form, **p) - fn(**p)) < 1e-9 * max(1, abs(fn(**p))) for p in points)
        ex._rec(good, f'{iid} form {form!r} agrees with route B{label}', '')
    for wr in w.get('wrong', []):
        bad = any(abs(tex_val(wr['tex'], **p) - fn(**p)) > 1e-6 for p in points)
        ex._rec(bad, f'{iid} wrong {wr["id"]} {wr["tex"]!r} differs from the key', '')


# ================================================================ difficulty 2
# e-divide-conjugate: exact Fractions, (a + bi)/(c + di) by hand
a, b, c, d = F(4), F(7), F(2), F(-3)
den = c * c + d * d
re_, im_ = (a * c + b * d) / den, (b * c - a * d) / den
ok(re_ == -1 and im_ == 2, 'e-divide-conjugate: (4 + 7i)/(2 - 3i) = -1 + 2i exactly')
key('e-divide-conjugate', float(re_), part=0)
key('e-divide-conjugate', float(im_), part=1)
top_plus = (a * c + b * (-d), a * (-d) + b * c)        # (4 + 7i)(2 + 3i) with i^2 = +1: 8 + 21, 12 + 14
ok(top_plus == (29, 26), 'e-divide-conjugate: i^2 = +1 gives top 29 + 26i')
wrong('e-divide-conjugate', 'plus-one', float(F(top_plus[0], 13)), part=0)
z_self = complex(4, 7) * complex(2, -3)
ok(abs(z_self - complex(29, 2)) < 1e-12, 'e-divide-conjugate: (4 + 7i)(2 - 3i) = 29 + 2i')
wrong('e-divide-conjugate', 'times-bottom', z_self.imag / 13, part=1)
ok(abs(complex(-1, 2) * complex(2, -3) - complex(4, 7)) < 1e-12, 'e-divide-conjugate: check line (-1 + 2i)(2 - 3i) = 4 + 7i')
ok(abs(complex(4, 7) / complex(2, -3) - complex(-1, 2)) < 1e-12, 'e-divide-conjugate: complex division agrees')
ok(not any('tex' in x for x in node(W('e-divide-conjugate', 0)).get('wrong', [])), 'e-divide-conjugate: both parts numeric, no retypable expression')
allow('e-divide-conjugate', 13, 26, 21, 29, -13, 8)

# e-arg-quadrant
zq = complex(-2 * math.sqrt(3), -2)
key('e-arg-quadrant', math.hypot(zq.real, zq.imag), part=0)
wrong('e-arg-quadrant', 'no-root', zq.real ** 2 + zq.imag ** 2, part=0)
ok(abs(math.atan2(-2, -2 * math.sqrt(3)) + 5 * math.pi / 6) < 1e-12, 'e-arg-quadrant: atan2 gives -5pi/6')
ok(abs(math.atan(zq.imag / zq.real) - math.pi / 6) < 1e-12, 'e-arg-quadrant: arctan(y/x) gives pi/6 (the arctan slip)')
ok(abs(cmath.exp(1j * 7 * math.pi / 6) - cmath.exp(-5j * math.pi / 6)) < 1e-12 and 7 * math.pi / 6 > math.pi, 'e-arg-quadrant: 7pi/6 is the same direction, outside (-pi, pi]')
ok(math.sin(5 * math.pi / 6) > 0, 'e-arg-quadrant: 5pi/6 points above the real axis')
correct_id('e-arg-quadrant', 'ok', part=1)
allow('e-arg-quadrant', 12, 16)

# e-wire-mass: Simpson along the segment
L = math.hypot(3, 4)
m_ = simpson(lambda t: (2 * (1 + 3 * t) + 4 * t) * L, 0, 1)
key('e-wire-mass', m_)
wrong('e-wire-mass', 'no-speed', simpson(lambda t: 2 * (1 + 3 * t) + 4 * t, 0, 1))
wrong('e-wire-mass', 'far-end', (2 * 4 + 4) * L)
allow('e-wire-mass', 12, 35, 7)

# e-rate-pull: RK4 on r' = 0.25(0.045 - r)
rr = rk4(lambda t, y: 0.25 * (0.045 - y), 0, [0.07], 4)[0]
key('e-rate-pull', rr, tol=1e-6)
wrong('e-rate-pull', 'sign', 0.045 - (rr - 0.045))
wrong('e-rate-pull', 'no-t', rk4(lambda t, y: 0.25 * (0.045 - y), 0, [0.07], 1)[0])
say('e-rate-pull', 'feedback.correct', round(rr, 4), fmt='{:.4f}')
say('e-rate-pull', 'explain.text', round(math.exp(-1), 4), fmt='{:.4f}')
allow('e-rate-pull', 0.25, 0.045, 0.07, 0.025, rr - 0.045, math.exp(-1), round(rr, 4), 100 * rr)

# e-char-roots
rts = sorted(np.roots([1, -2, -15]).real)
ok(np.allclose(rts, [-3, 5]), 'e-char-roots: roots of r^2 - 2r - 15 are -3 and 5')
ok(np.allclose(sorted(np.roots([1, 2, -15]).real), [-5, 3]), 'e-char-roots: flipped middle term gives -5 and 3')
cr_ = np.roots([1, -2, 15])
ok(np.allclose(sorted(cr_.imag), [-math.sqrt(14), math.sqrt(14)]) and np.allclose(cr_.real, 1), 'e-char-roots: +15 gives 1 +- i sqrt14')
ok((-2) ** 2 - 4 * (-15) == 64, 'e-char-roots: discriminant 64')
correct_id('e-char-roots', 'ok')
allow('e-char-roots', 15, 14, 60, 64)

# e-laplace-shift: numerical Laplace transform at sample s
def lap(f, s, T=60, n=200000):
    return simpson(lambda t: np.exp(-s * t) * f(t), 0, T, n)


pts = [{'s': sv} for sv in (0.3, 1.1, 2.7)]
vals = {p['s']: lap(lambda t: np.exp(-2 * t) * np.sin(3 * t), p['s']) for p in pts}
w_ = node(W('e-laplace-shift'))
for form in [w_['answer']] + w_['accept']:
    ok(all(abs(tex_val(form, s=sv) - vals[sv]) < 1e-8 for sv in vals), f'e-laplace-shift form {form!r} = numerical transform')
for wr in w_['wrong']:
    ok(any(abs(tex_val(wr['tex'], s=sv) - vals[sv]) > 1e-4 for sv in vals), f'e-laplace-shift wrong {wr["id"]} differs')
allow('e-laplace-shift', 13)

# ================================================================ difficulty 3
# e-fifth-roots: each option's value raised to the fifth power
optval = {'minus-two': -2, 'pi-fifth': 2 * cmath.exp(1j * math.pi / 5), 'seven': 2 * cmath.exp(7j * math.pi / 5),
          'two': 2, 'zero-arg': 2 * cmath.exp(2j * math.pi / 5), 'half-pi': 2 * cmath.exp(1j * math.pi / 10)}
roots_ok = sorted(k for k, v in optval.items() if abs(v ** 5 + 32) < 1e-9)
correct_id('e-fifth-roots', roots_ok)
ok(abs(optval['zero-arg'] ** 5 - 32) < 1e-9 and abs(optval['half-pi'] ** 5 - 32j) < 1e-9 and optval['two'] ** 5 == 32, 'e-fifth-roots: distractors give 32, 32 and 32i')
args = sorted((cmath.phase(w) % (2 * math.pi)) / math.pi for w in np.roots([1, 0, 0, 0, 0, 32]))
ok(np.allclose(args, [0.2, 0.6, 1.0, 1.4, 1.8]), 'e-fifth-roots: arguments pi/5, 3pi/5, pi, 7pi/5, 9pi/5')
allow('e-fifth-roots', 32, -32)

# e-harmonic-partner: Cauchy-Riemann by finite differences
def u_h(x, y):
    return np.exp(x) * np.cos(y) + 2 * x * y


def cr_ok(vf, pts_):
    e = 1e-5
    for x, y in pts_:
        ux = (u_h(x + e, y) - u_h(x - e, y)) / (2 * e)
        uy = (u_h(x, y + e) - u_h(x, y - e)) / (2 * e)
        vx = (vf(x + e, y) - vf(x - e, y)) / (2 * e)
        vy = (vf(x, y + e) - vf(x, y - e)) / (2 * e)
        if abs(ux - vy) > 1e-6 or abs(uy + vx) > 1e-6:
            return False
    return abs(vf(0, 0)) < 1e-12


hp = [(0.3, 0.7), (1.2, -0.4), (-0.8, 2.1)]
lap_u = [(u_h(x + 1e-4, y) + u_h(x - 1e-4, y) + u_h(x, y + 1e-4) + u_h(x, y - 1e-4) - 4 * u_h(x, y)) / 1e-8 for x, y in hp]
ok(max(abs(v) for v in lap_u) < 1e-3, 'e-harmonic-partner: u is harmonic (five-point Laplacian)')
w_ = node(W('e-harmonic-partner'))
for form in [w_['answer']] + w_['accept']:
    ok(cr_ok(lambda x, y, f=form: tex_val(f, x=x, y=y).real, hp), f'e-harmonic-partner form {form!r} satisfies Cauchy-Riemann with v(0,0) = 0')
for wr in w_['wrong']:
    ok(not cr_ok(lambda x, y, f=wr['tex']: tex_val(f, x=x, y=y).real, hp), f'e-harmonic-partner wrong {wr["id"]} fails Cauchy-Riemann')
zt = complex(0.6, -1.3)
ok(abs((cmath.exp(zt) - 1j * zt * zt).imag - tex_val(w_['answer'], x=0.6, y=-1.3).real) < 1e-12, 'e-harmonic-partner: v = Im(e^z - iz^2)')

# e-log-square
zl = complex(-1, math.sqrt(3))
ok(abs(zl * zl - complex(-2, -2 * math.sqrt(3))) < 1e-12, 'e-log-square: z^2 = -2 - 2sqrt3 i')
ok(abs(cmath.phase(zl) - 2 * math.pi / 3) < 1e-12, 'e-log-square: Arg z = 2pi/3')
key('e-log-square', cmath.log(zl * zl).imag, part=0, tol=1e-4)
wrong('e-log-square', 'doubled', 2 * cmath.phase(zl), part=0)
lg2, lg1 = cmath.log(zl * zl), cmath.log(zl)
ok(abs(lg2 - (2 * lg1 - 2j * math.pi)) < 1e-12, 'e-log-square: Log(z^2) = 2 Log z - 2 pi i')
ok(abs(lg2.real - math.log(4)) < 1e-12 and abs((2 * lg1).real - math.log(4)) < 1e-12, 'e-log-square: both real parts ln 4')
correct_id('e-log-square', 'ok', part=1)
allow('e-log-square', -2.094, 3)

# e-separable-slow: RK4 on y' = t e^{-y}, and the slips by their own formulas
ys = rk4(lambda t, y: np.array([t * math.exp(-y[0])]), 0, [0.0], 2)[0]
key('e-separable-slow', ys, tol=5e-5)
wrong('e-separable-slow', 'frozen', rk4(lambda t, y: np.array([t * 1.0]), 0, [0.0], 2)[0])
wrong('e-separable-slow', 'no-half', math.log(1 + 2 ** 2))
ok(all(abs(math.exp(math.log(1 + t * t / 2)) - (1 + t * t / 2)) < 1e-12 for t in (0.5, 2)), 'e-separable-slow: e^y = 1 + t^2/2')
ok(abs(rk4(lambda t, y: np.array([t * math.exp(-y[0])]), 0, [0.0], 1)[0] - math.log(1.5)) < 1e-9, 'e-separable-slow: y(1) = ln 1.5 by RK4')
allow('e-separable-slow', 2, 3, 5, 1)

# e-cauchy-plus-normal: numerical Fourier integrals of the two densities
u0 = 0.8
xs_ = np.linspace(-4000, 4000, 8_000_001)
dx_ = xs_[1] - xs_[0]
phiX = np.sum(np.cos(u0 * xs_) / (np.pi * (1 + xs_ ** 2))) * dx_
xn = np.linspace(-12, 12, 240001)
phiY = simpson(lambda x: np.cos(u0 * x) * np.exp(-x * x / 2) / math.sqrt(2 * math.pi), -12, 12, 240000)
ok(abs(phiX - math.exp(-u0)) < 2e-4, f'e-cauchy-plus-normal: Cauchy cf at 0.8 numerically {phiX:.5f}')
key('e-cauchy-plus-normal', phiX * phiY, tol=2e-4)
wrong('e-cauchy-plus-normal', 'added', math.exp(-u0) + phiY)
wrong('e-cauchy-plus-normal', 'no-half', math.exp(-u0) * phiY ** 2)
say('e-cauchy-plus-normal', 'explain.text', 0.3263)
allow('e-cauchy-plus-normal', 0.8, 0.32, 1.12, 0.3263, 1.1755, 0.2369)

# e-potential-work: Simpson along a winding path from (1, 0) to (2, 1)
P1 = lambda x, y: 2 * x * y + y ** 3
Q1 = lambda x, y: x * x + 3 * x * y * y + 2 * y
xs1 = lambda t: 1 + t + 0.3 * np.sin(5 * np.pi * t)
ys1 = lambda t: t + 0.4 * np.sin(3 * np.pi * t)
dx1 = lambda t: 1 + 1.5 * np.pi * np.cos(5 * np.pi * t)
dy1 = lambda t: 1 + 1.2 * np.pi * np.cos(3 * np.pi * t)
wk = loop_work(P1, Q1, xs1, ys1, dx1, dy1)
key('e-potential-work', wk, part=1)
wrong('e-potential-work', 'no-g', wk - (1 ** 2 - 0 ** 2), part=1)
e_ = 1e-6
ok(all(abs((P1(x, y + e_) - P1(x, y - e_)) / (2 * e_) - (Q1(x + e_, y) - Q1(x - e_, y)) / (2 * e_)) < 1e-6 for x, y in [(0.3, 1.7), (-2, 0.5)]), 'e-potential-work: P_y = Q_x')
ok(abs((P1(1.3, 0.7 + e_) - P1(1.3, 0.7 - e_)) / (2 * e_) - (2 * 1.3 + 3 * 0.49)) < 1e-6, 'e-potential-work: P_y = 2x + 3y^2')
correct_id('e-potential-work', 'ok', part=0)

# e-circulation-flux: line integrals round the circle of radius 3
Pc = lambda x, y: 2 * x - 5 * y
Qc = lambda x, y: 3 * x + y
cx, cy = (lambda t: 3 * np.cos(2 * np.pi * t)), (lambda t: 3 * np.sin(2 * np.pi * t))
cdx, cdy = (lambda t: -6 * np.pi * np.sin(2 * np.pi * t)), (lambda t: 6 * np.pi * np.cos(2 * np.pi * t))
circ = loop_work(Pc, Qc, cx, cy, cdx, cdy)
flux = simpson(lambda t: Pc(cx(t), cy(t)) * cdy(t) - Qc(cx(t), cy(t)) * cdx(t), 0, 1, 40000)
key('e-circulation-flux', circ / math.pi, part=0, tol=1e-6)
key('e-circulation-flux', flux / math.pi, part=1, tol=1e-6)
wrong('e-circulation-flux', 'sign', -circ / math.pi, part=0)
wrong('e-circulation-flux', 'div', flux / math.pi, part=0)
wrong('e-circulation-flux', 'curl', circ / math.pi, part=1)
wrong('e-circulation-flux', 'radius', flux / math.pi / 3, part=1)
allow('e-circulation-flux', 72, 27, 9, 3, 8)

# e-tilted-patch: surface area from a finite-difference cross product on a grid
uu, vv = np.meshgrid(np.linspace(0, 2, 401), np.linspace(0, 1, 201), indexing='ij')
R = np.stack([uu, vv, 3 * uu - vv])
Ru = np.gradient(R, 2 / 400, axis=1)
Rv = np.gradient(R, 1 / 200, axis=2)
crs = np.cross(Ru, Rv, axis=0)
dA = np.linalg.norm(crs, axis=0)
area_B = np.trapezoid(np.trapezoid(dA, dx=1 / 200, axis=1), dx=2 / 400)
key('e-tilted-patch', area_B, tol=1e-4)
wrong('e-tilted-patch', 'no-factor', 1 * 2)
wrong('e-tilted-patch', 'lengths', np.linalg.norm([1, 0, 3]) * np.linalg.norm([0, 1, -1]) * 2)
ok(np.allclose(np.cross([1, 0, 3], [0, 1, -1]), [-3, 1, 1]), 'e-tilted-patch: r_u x r_v = (-3, 1, 1)')
allow('e-tilted-patch', 11, 6.633, 3.317, 8.944, 10, 20)

# e-cube-outflow: the six faces directly, no divergence theorem
g = np.linspace(0, 2, 401)
A1, B1 = np.meshgrid(g, g, indexing='ij')
def face(vals):
    return np.trapezoid(np.trapezoid(vals, g, axis=1), g)
Fx = lambda x, y, z: x * z ** 2
Fy = lambda x, y, z: y * x ** 2
Fz = lambda x, y, z: z * y ** 2
fl = (face(Fx(2, A1, B1)) - face(Fx(0, A1, B1)) + face(Fy(A1, 2, B1)) - face(Fy(A1, 0, B1))
      + face(Fz(A1, B1, 2)) - face(Fz(A1, B1, 0)))
key('e-cube-outflow', fl, tol=1e-3)
wrong('e-cube-outflow', 'centre', (1 + 1 + 1) * 8)
wrong('e-cube-outflow', 'one-term', 2 * 2 * simpson(lambda x: x * x, 0, 2))
allow('e-cube-outflow', 32, 8 / 3, 32 / 3)

# e-integrating-factor: RK4
yi = rk4(lambda t, y: -4 * y + 9 * np.exp(-t), 0, [5.0], 1)[0]
key('e-integrating-factor', yi, tol=1e-4)
wrong('e-integrating-factor', 'const-add', yi - 2 * math.exp(-4) + 2)
wrong('e-integrating-factor', 'no-fit', rk4(lambda t, y: -4 * y + 9 * np.exp(-t), 0, [8.0], 1)[0])
allow('e-integrating-factor', 1.1403, 3.1036, 1.1952)

# e-resonant-guess: y_p = A t^2 e^{2t} by finite differences; the slip by taking (t^2)'' = 1
def resid(A, t, slip=False):
    f_ = lambda u: A * u * u * math.exp(2 * u)
    e = 1e-4
    y1 = (f_(t + e) - f_(t - e)) / (2 * e)
    y2 = (f_(t + e) - 2 * f_(t) + f_(t - e)) / e ** 2
    if slip:
        y2 = A * (1 + 8 * t + 4 * t * t) * math.exp(2 * t)      # constant 2 read as 1
    return y2 - 4 * y1 + 4 * f_(t) - 6 * math.exp(2 * t)


Ab = 6 / ((resid(1, 0.4) + 6 * math.exp(0.8)) / math.exp(0.8))
key('e-resonant-guess', Ab, tol=1e-4)
ok(abs(resid(3, 0.4)) < 1e-3 and abs(resid(3, 1.3)) < 1e-2, 'e-resonant-guess: 3t^2e^{2t} solves the equation')
As = 6 / ((resid(1, 0.4, True) + 6 * math.exp(0.8)) / math.exp(0.8))
wrong('e-resonant-guess', 'no-two', As)
ok(np.allclose(np.roots([1, -4, 4]), [2, 2]), 'e-resonant-guess: 2 is a double root of r^2 - 4r + 4')
allow('e-resonant-guess', 6)

# e-damping-rate
r4 = np.roots([1, 4, 16])
ok(np.allclose(r4.real, -2), 'e-damping-rate: b = 4 has real part -2')
key('e-damping-rate', abs(r4.imag[0]), part=0, tol=5e-5)
wrong('e-damping-rate', 'full-disc', math.sqrt(abs(4 ** 2 - 4 * 16)), part=0)
wrong('e-damping-rate', 'natural', math.sqrt(16), part=0)
r10 = sorted(np.roots([1, 10, 16]).real)
key('e-damping-rate', -r10[1], part=1)
wrong('e-damping-rate', 'fast', -r10[0], part=1)
wrong('e-damping-rate', 'half-b', 10 / 2, part=1)
ok(np.allclose(np.roots([1, 8, 16]), [-4, -4]), 'e-damping-rate: b = 8 gives the double root -4')
slow = [max(np.roots([1, bb, 16]).real) for bb in np.linspace(0.5, 20, 400)]
ok(np.argmin(slow) == int(np.argmin(np.abs(np.linspace(0.5, 20, 400) - 8))), 'e-damping-rate: the slow mode decays fastest near b = 8')
allow('e-damping-rate', 16, 64, 48, 12, 2 * math.sqrt(3), 4, 10, 8)

# e-saddle-solution: series matrix exponential
A_s = np.array([[1, 4], [1, 1]])
ev = sorted(np.linalg.eigvals(A_s).real)
ok(np.allclose(ev, [-1, 3]), 'e-saddle-solution: eigenvalues -1 and 3')
ok(np.allclose(A_s @ [2, 1], [6, 3]) and np.allclose(A_s @ [2, -1], [-2, 1]), 'e-saddle-solution: eigenvectors (2, 1) and (2, -1)')
cc = np.linalg.solve(np.array([[2, 2], [1, -1]]), [6, 1])
key('e-saddle-solution', cc[0], part=0)
wrong('e-saddle-solution', 'swap', cc[1], part=0)
xh = expm(0.5 * A_s) @ np.array([6, 1])
key('e-saddle-solution', xh[0], part=1, tol=1e-4)
wrong('e-saddle-solution', 'swap-rates', cc[0] * 2 * math.exp(-0.5) + cc[1] * 2 * math.exp(1.5), part=1)
wrong('e-saddle-solution', 'no-vector', cc[0] * math.exp(1.5) + cc[1] * math.exp(-0.5), part=1)
allow('e-saddle-solution', 19.14, 11.39, 9.57, 1.5, 0.5)

# e-spiral-turn
A_t = np.array([[-1, -4], [2, -3]])
evt = np.linalg.eigvals(A_t)
ok(np.allclose(sorted(evt.imag), [-math.sqrt(7), math.sqrt(7)]) and np.allclose(evt.real, -2), 'e-spiral-turn: eigenvalues -2 +- i sqrt7')
ok(np.trace(A_t) == -4 and round(np.linalg.det(A_t)) == 11 and np.trace(A_t) ** 2 - 4 * round(np.linalg.det(A_t)) == -28, 'e-spiral-turn: tau -4, Delta 11, tau^2 - 4 Delta = -28')
ok(np.allclose(A_t @ [1, 0], [-1, 2]), 'e-spiral-turn: A(1, 0) = (-1, 2)')
xt = rk4(lambda t, y: A_t @ y, 0, [1.0, 0.0], 0.05, 500)
ok(xt[1] > 0, 'e-spiral-turn: from (1, 0) the path moves up (anticlockwise)')
correct_id('e-spiral-turn', 'ok')
allow('e-spiral-turn', 11, 28, -28)

# e-euler-by-hand
yy, t_ = 1.0, 0.0
for _ in range(2):
    yy, t_ = yy + 0.25 * (yy - t_ ** 2), t_ + 0.25
key('e-euler-by-hand', yy, tol=1e-9)
wrong('e-euler-by-hand', 'one-step', 1 + 0.5 * (1 - 0))
wrong('e-euler-by-hand', 'stale-t', 1.25 + 0.25 * 1.25)
yex = rk4(lambda t, y: y - t * t, 0, [1.0], 0.5)[0]
say('e-euler-by-hand', 'explain.text', round(yex, 4), fmt='{:.4f}')
say('e-euler-by-hand', 'explain.text', round(yex - yy, 3), fmt='{:.3f}')
allow('e-euler-by-hand', 0.25, 1.25, 0.0625, 0.5, 3.25, yex, yex - yy, 1.5, 1.5625)

# ================================================================ difficulty 4
# e-upper-pole: residue by a small circle, integral by sinh substitution
pole = complex(-3, 2)
res_B = circle_integral(lambda z: 1 / (z * z + 6 * z + 13), pole, 0.5) / (2j * math.pi)
key('e-upper-pole', res_B.imag, part=0, tol=1e-6)
ok(abs(res_B.real) < 1e-9, 'e-upper-pole: residue is purely imaginary')
wrong('e-upper-pole', 'no-i', -res_B.imag, part=0)
Ib = simpson(lambda u: np.cosh(u) / (np.sinh(u) ** 2 + 6 * np.sinh(u) + 13), -40, 40, 400000)
key('e-upper-pole', Ib, part=1, tol=5e-5)
wrong('e-upper-pole', 'both', 0, part=1)
wrong('e-upper-pole', 'no-2pi', res_B.imag, part=1)
wrong('e-upper-pole', 'lower', -Ib, part=1)
ok(np.allclose(sorted(np.roots([1, 6, 13]).imag), [-2, 2]), 'e-upper-pole: poles -3 +- 2i')
allow('e-upper-pole', 13, 1.571, 0.25)

# e-third-power-pole: trapezoid round |z| = 4
Ic = circle_integral(lambda z: np.cos(z) / (z - math.pi) ** 3, 0, 4)
key('e-third-power-pole', Ic.imag / math.pi, tol=5e-5)
ok(abs(Ic.real) < 1e-9, 'e-third-power-pole: real part 0')
wrong('e-third-power-pole', 'no-fact', 2 * Ic.imag / math.pi)
wrong('e-third-power-pole', 'three-fact', Ic.imag / math.pi / 3)
wrong('e-third-power-pole', 'sign', -Ic.imag / math.pi)
ok(math.pi < 4, 'e-third-power-pole: the point pi is inside |z| = 4')
ok(abs(-math.cos(math.pi) - 1) < 1e-12, 'e-third-power-pole: f\'\'(pi) = -cos(pi) = 1')
allow('e-third-power-pole', 1, 2, 4, 1 / 3)

# e-damped-call: Carr-Madan integral against Black-Scholes, two damping factors
S0, K0, rr_, sg, T_ = 100.0, 105.0, 0.03, 0.25, 0.75


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


d1 = (math.log(S0 / K0) + (rr_ + sg * sg / 2) * T_) / (sg * math.sqrt(T_))
bs = S0 * ncdf(d1) - K0 * math.exp(-rr_ * T_) * ncdf(d1 - sg * math.sqrt(T_))


def carr_madan(alpha, k):
    m = math.log(S0) + (rr_ - sg * sg / 2) * T_
    phi = lambda u: np.exp(1j * u * m - 0.5 * sg * sg * u * u * T_)
    v = np.linspace(0, 200, 400001)
    psi = math.exp(-rr_ * T_) * phi(v - (alpha + 1) * 1j) / (alpha ** 2 + alpha - v ** 2 + 1j * (2 * alpha + 1) * v)
    integrand = np.real(np.exp(-1j * v * k) * psi)
    return math.exp(-alpha * k) / math.pi * np.trapezoid(integrand, v)


cm1, cm2 = carr_madan(0.75, math.log(K0)), carr_madan(1.5, math.log(K0))
ok(abs(cm1 - bs) < 1e-6 and abs(cm2 - bs) < 1e-6, f'e-damped-call: price {bs:.6f} the same for alpha 0.75 and 1.5')
deep = S0 * ncdf((math.log(S0 / 1e-6) + (rr_ + sg * sg / 2) * T_) / (sg * math.sqrt(T_))) - 1e-6 * math.exp(-rr_ * T_)
ok(abs(deep - S0) < 1e-5, 'e-damped-call: C(k) tends to S_0 as k falls')
correct_id('e-damped-call', 'ok')

# e-hemisphere-curl: curl by finite differences, flux over the dome on a (theta, phi) grid
def Fv(x, y, z):
    return np.array([z - y, x + z, x * y])


def curl(x, y, z, e=1e-5):
    dF = lambda i, j: (Fv(*[c + (e if k == j else 0) for k, c in enumerate((x, y, z))])[i]
                       - Fv(*[c - (e if k == j else 0) for k, c in enumerate((x, y, z))])[i]) / (2 * e)
    return np.array([dF(2, 1) - dF(1, 2), dF(0, 2) - dF(2, 0), dF(1, 0) - dF(0, 1)])


th = np.linspace(0, np.pi / 2, 801)
ph = np.linspace(0, 2 * np.pi, 1601)
TH, PH = np.meshgrid(th, ph, indexing='ij')
X, Y, Z = np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)
Cu = curl(X, Y, Z)
dome = np.trapezoid(np.trapezoid((Cu[0] * X + Cu[1] * Y + Cu[2] * Z) * np.sin(TH), ph, axis=1), th)
key('e-hemisphere-curl', dome, part=0, tol=1e-4)
circ_h = loop_work(lambda x, y: Fv(x, y, 0)[0], lambda x, y: Fv(x, y, 0)[1], lambda t: np.cos(2 * np.pi * t),
                   lambda t: np.sin(2 * np.pi * t), lambda t: -2 * np.pi * np.sin(2 * np.pi * t), lambda t: 2 * np.pi * np.cos(2 * np.pi * t))
ok(abs(circ_h - dome) < 1e-4, 'e-hemisphere-curl: Stokes, dome flux = boundary circulation')
wrong('e-hemisphere-curl', 'closed', 0, part=0)
wrong('e-hemisphere-curl', 'area', 2 * 2 * math.pi, part=0)
rr2 = np.linspace(0, 1, 801)
RR, PP = np.meshgrid(rr2, ph, indexing='ij')
Cd = curl(RR * np.cos(PP), RR * np.sin(PP), 0 * RR)
disc = np.trapezoid(np.trapezoid(-Cd[2] * RR, ph, axis=1), rr2)
key('e-hemisphere-curl', dome + disc, part=1, tol=1e-4)
wrong('e-hemisphere-curl', 'double', dome - disc, part=1)
allow('e-hemisphere-curl', 6.283)

# e-crowded-prey: Newton for the equilibrium, finite-difference Jacobian, a short orbit
fx = lambda v: np.array([v[0] * (4 - v[0] - 2 * v[1]), v[1] * (v[0] - 2)])
v = np.array([1.5, 1.5])
def jac(v, e=1e-6):
    return np.column_stack([(fx(v + e * np.eye(2)[k]) - fx(v - e * np.eye(2)[k])) / (2 * e) for k in range(2)])
for _ in range(30):
    v = v - np.linalg.solve(jac(v), fx(v))
key('e-crowded-prey', v[1], part=0, tol=1e-6)
wrong('e-crowded-prey', 'crowd', 4 / 2, part=0)
Jb = jac(v)
key('e-crowded-prey', np.linalg.det(Jb), part=1, tol=1e-5)
wrong('e-crowded-prey', 'sign', Jb[0, 0] * Jb[1, 1] + Jb[0, 1] * Jb[1, 0], part=1)
wrong('e-crowded-prey', 'trace', np.trace(Jb), part=1)
evp = np.linalg.eigvals(Jb)
ok(np.allclose(evp.real, -1, atol=1e-5) and np.allclose(sorted(evp.imag), [-math.sqrt(3), math.sqrt(3)], atol=1e-5), 'e-crowded-prey: eigenvalues -1 +- i sqrt3')
ok(abs(np.trace(Jb) ** 2 - 4 * np.linalg.det(Jb) + 12) < 1e-5, 'e-crowded-prey: tau^2 - 4 Delta = -12')
orb = rk4(lambda t, y: fx(y), 0, [2.05, 1.0], 6, 6000)
ok(np.linalg.norm(orb - v) < 0.05 * 0.05, 'e-crowded-prey: the true system spirals in near (2, 1)')
correct_id('e-crowded-prey', 'ok', part=2)
allow('e-crowded-prey', 12, -12)

# e-laplace-rebound: RK4 on the system, partial fractions at sample s, line checks
sys2 = lambda t, y: np.array([y[1], -6 * y[1] - 5 * y[0]])
yb = rk4(sys2, 0, [1.0, 3.0], 1)[0]
key('e-laplace-rebound', yb, part=1, tol=1e-4)
# the e1 slip gives (s^2 + 6s + 5)Y = 3s + 7, the transform of the problem with y(0) = 3, y'(0) + 6y(0) = 7
wrong('e-laplace-rebound', 'swapped', rk4(sys2, 0, [3.0, 7.0 - 18.0], 1)[0], part=1)
for sv in (0.4, 2.2, 7.5):
    ok(abs((sv + 9) / ((sv + 1) * (sv + 5)) - (2 / (sv + 1) - 1 / (sv + 5))) < 1e-12, f'e-laplace-rebound: partial fractions at s = {sv}')
    yl = lap(lambda t: 2 * np.exp(-t) - np.exp(-5 * t), sv)
    ok(abs((sv * sv * yl - sv - 3) + 6 * (sv * yl - 1) + 5 * yl) < 1e-7, f'e-laplace-rebound: the transformed equation holds at s = {sv}')
o_ = node(W('e-laplace-rebound', 0))
ok(o_['answer'] == ['k1', 'k2', 'k3', 'k4', 'k5'] and o_['distractors'] == ['e1', 'e2'], 'e-laplace-rebound: order key and left-out lines')
ok(abs(rk4(sys2, 0, [1.0, 3.0], 1)[0] - (2 * math.exp(-1) - math.exp(-5))) < 1e-9, 'e-laplace-rebound: y = 2e^{-t} - e^{-5t}')
allow('e-laplace-rebound', 0.73576, 0.00674, 0.72902, 0.729, 0.3814)

# ================================================================ difficulty 5
# e-semicircle-proof: the arc bound with two degrees of decay, and its failure with one
def arc(f, Rr, n=20000):
    t = np.linspace(0, np.pi, n + 1)
    z = Rr * np.exp(1j * t)
    y = f(z) * 1j * z
    return np.sum((y[1:] + y[:-1]) / 2) * (np.pi / n)


ok(abs(arc(lambda z: 1 / (z * z + 6 * z + 13), 200)) < math.pi * 1.2 / 200, 'e-semicircle-proof: degree gap 2, the arc is under pi M / R')
ok(abs(arc(lambda z: z / (z * z + 1), 200) - 1j * math.pi) < 0.01, 'e-semicircle-proof: degree gap 1, the arc tends to pi i, not 0')
o_ = node(W('e-semicircle-proof'))
ok(o_['answer'] == ['k1', 'k2', 'k3', 'k4', 'k5', 'k6'] and o_['distractors'] == ['e1', 'e2'], 'e-semicircle-proof: order key and left-out lines')
# dependencies: k2 needs k1 (the contour), k3 needs k2, k4 needs only C_R from k1, k5 needs k3 and k4, k6 needs k5
DEPS = {'k1': set(), 'k2': {'k1'}, 'k3': {'k2'}, 'k4': {'k1'}, 'k5': {'k3', 'k4'}, 'k6': {'k5'}}


def valid_order(seq):
    done = set()
    for x in seq:
        if not DEPS[x] <= done:
            return False
        done.add(x)
    return True


swapped = ['k1', 'k2', 'k4', 'k3', 'k5', 'k6']
ok(o_.get('same') == [['k3', 'k4']], 'e-semicircle-proof: k3 and k4 are interchangeable')
ok(valid_order(o_['answer']) and valid_order(swapped), 'e-semicircle-proof: the key and the k3/k4 swap are both valid proofs')
ok(not valid_order(['k1', 'k3', 'k2', 'k4', 'k5', 'k6']) and not valid_order(['k1', 'k2', 'k3', 'k5', 'k4', 'k6']), 'e-semicircle-proof: other swaps are not valid')

# e-vortex-square: Simpson round the square (four sides), the off-centre circle, and G
Pv = lambda x, y: -y / (x * x + y * y)
Qv = lambda x, y: x / (x * x + y * y)


def square(Pf, Qf):
    sides = [((lambda t: 2 + 0 * t), (lambda t: -2 + 4 * t), (lambda t: 0 * t), (lambda t: 4 + 0 * t)),
             ((lambda t: 2 - 4 * t), (lambda t: 2 + 0 * t), (lambda t: -4 + 0 * t), (lambda t: 0 * t)),
             ((lambda t: -2 + 0 * t), (lambda t: 2 - 4 * t), (lambda t: 0 * t), (lambda t: -4 + 0 * t)),
             ((lambda t: -2 + 4 * t), (lambda t: -2 + 0 * t), (lambda t: 4 + 0 * t), (lambda t: 0 * t))]
    return sum(loop_work(Pf, Qf, *s) for s in sides)


sq = square(Pv, Qv)
key('e-vortex-square', sq, part=0, tol=5e-5)
wrong('e-vortex-square', 'green', 0, part=0)
off = loop_work(Pv, Qv, lambda t: 4 + np.cos(2 * np.pi * t), lambda t: 1 + np.sin(2 * np.pi * t),
                lambda t: -2 * np.pi * np.sin(2 * np.pi * t), lambda t: 2 * np.pi * np.cos(2 * np.pi * t))
key('e-vortex-square', off, part=1, tol=1e-6)
wrong('e-vortex-square', 'always', sq, part=1)
gq = square(lambda x, y: Pv(x, y) + y * y, lambda x, y: Qv(x, y) + 3 * x)
key('e-vortex-square', gq, part=2, tol=1e-4)
smooth = square(lambda x, y: y * y + 0 * x, lambda x, y: 3 * x + 0 * y)
wrong('e-vortex-square', 'no-vortex', smooth, part=2)
wrong('e-vortex-square', 'sign', sq - smooth, part=2)
ok(abs(math.hypot(4, 1) - math.sqrt(17)) < 1e-12 and math.sqrt(17) > 1, 'e-vortex-square: the origin is sqrt17 from (4, 1), outside T')
allow('e-vortex-square', 6.283, 48, 54.28, 17)

# e-stiff-steps: stability boundaries by bisection on the amplification factors
def bound(Rf):
    lo, hi = 1e-6, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if abs(Rf(-mid)) <= 1:
            lo = mid
        else:
            hi = mid
    return lo


eu_b = bound(lambda z: 1 + z)
rk_b = bound(lambda z: 1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24)
ok(abs(rk_b - 2.7853) < 5e-5, f'e-stiff-steps: RK4 boundary {rk_b:.5f} = 2.7853')
key('e-stiff-steps', eu_b / 80, part=0, tol=1e-6)
wrong('e-stiff-steps', 'one-over', 1 / 80, part=0)
wrong('e-stiff-steps', 'rk4', rk_b / 80, part=0)
n_rk4 = next(n for n in range(1, 500) if 1 / n < rk_b / 80)     # smallest n with h = 1/n inside the stable interval
n_eul = next(n for n in range(1, 500) if 1 / n < eu_b / 80)
ok(n_rk4 == 29 and n_eul == 41 and 1 / 28 > rk_b / 80, 'e-stiff-steps: 29 RK4 steps, 41 Euler steps, 28 unstable')
key('e-stiff-steps', 4 * n_rk4, part=1, tol=0)
wrong('e-stiff-steps', 'steps', n_rk4, part=1)
wrong('e-stiff-steps', 'floor', 4 * (n_rk4 - 1), part=1)
wrong('e-stiff-steps', 'euler', n_eul, part=1)
ok(abs(1 / 28 - 0.0357) < 5e-5 and 80 / rk_b > 28 and 80 / rk_b < 29, 'e-stiff-steps: 80 / 2.7853 = 28.72')
e0, h_ = 1e-3, 0.03
e1 = e0 + h_ * (-80 * e0)
key('e-stiff-steps', e1 / e0, part=2, tol=1e-9)
wrong('e-stiff-steps', 'abs', -e1 / e0, part=2)
wrong('e-stiff-steps', 'no-one', -80 * 0.03, part=2)
ys_ = [1.0]
for _ in range(3):
    ys_.append(ys_[-1] * (1 - 80 * h_))
ok(ys_[1] < 0 < ys_[2] and abs(ys_[3]) > abs(ys_[2]) > abs(ys_[1]) > 1, 'e-stiff-steps: errors flip sign and grow at h = 0.03')
rkR = 1 - 2.4 + 2.4 ** 2 / 2 - 2.4 ** 3 / 6 + 2.4 ** 4 / 24
ok(abs(rkR) < 1, f'e-stiff-steps: RK4 factor at h = 0.03 is {rkR:.4f}, stable')
ok(abs(-e1 / e0 - 1) - 0.4 < 1e-12, 'e-stiff-steps: errors grow by 40% a step')
allow('e-stiff-steps', 80, -80, 2.7853, rk_b / 80, eu_b / 80, 1 / 80, 0.1, 0.03, 2.4, 1.4, 40, 28, 29, 41, 116, 1 / 28, 4 * n_rk4)

# ------------------------------------------------------------------ every level has an item on a skill first met there
LEVEL = {
    'e-divide-conjugate': ('complex', 1), 'e-arg-quadrant': ('complex', 1), 'e-fifth-roots': ('complex', 1),
    'e-harmonic-partner': ('complex', 2), 'e-log-square': ('complex', 2),
    'e-cauchy-plus-normal': ('complex', 3), 'e-upper-pole': ('complex', 3),
    'e-third-power-pole': ('complex', 3), 'e-damped-call': ('complex', 3), 'e-semicircle-proof': ('complex', 3),
    'e-wire-mass': ('vector-calc', 1), 'e-potential-work': ('vector-calc', 1),
    'e-circulation-flux': ('vector-calc', 2), 'e-vortex-square': ('vector-calc', 2),
    'e-tilted-patch': ('vector-calc', 3), 'e-cube-outflow': ('vector-calc', 3), 'e-hemisphere-curl': ('vector-calc', 3),
    'e-rate-pull': ('odes', 1), 'e-integrating-factor': ('odes', 1), 'e-separable-slow': ('odes', 1),
    'e-char-roots': ('odes', 2), 'e-resonant-guess': ('odes', 2), 'e-damping-rate': ('odes', 2),
    'e-saddle-solution': ('odes', 3), 'e-spiral-turn': ('odes', 3), 'e-crowded-prey': ('odes', 3),
    'e-laplace-shift': ('odes', 4), 'e-euler-by-hand': ('odes', 4), 'e-laplace-rebound': ('odes', 4),
    'e-stiff-steps': ('odes', 4),
}
ok(sorted(LEVEL) == sorted(idx), 'every item has a level')
CDIR = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
for course in ('complex', 'vector-calc', 'odes'):
    with open(os.path.join(CDIR, course, 'course.json'), encoding='utf8') as f:
        cj = json.load(f)
    seen = set()
    for lv in cj['levels']:
        sk = set()
        for lid in lv['lessons']:
            with open(os.path.join(CDIR, course, lid + '.json'), encoding='utf8') as f:
                sk |= set(json.load(f)['skills'])
        new = sk - seen
        seen |= sk
        target = new or sk          # a level with no new skill (odes L3) is covered through its own skills
        hits = [i for i, (c_, n_) in LEVEL.items() if c_ == course and n_ == lv['n'] and set(node(P(i))['skills']) & target]
        ex._rec(bool(hits), f'{course} L{lv["n"]}: {"new" if new else "no new skill; level"} skills {sorted(target)} tested by {hits}', '')
print('items per level:', dict(sorted(Counter(LEVEL.values()).items())))
allskills = set(doc['skills'])
covered = {s for it in items for s in it['skills']}
ok(covered == allskills, f'every skill of the topic is on an item ({len(allskills)})')
ok(Counter(it['difficulty'] for it in items) == Counter({2: 6, 3: 15, 4: 6, 5: 3}), 'ramp 6, 15, 6, 3')


# ------------------------------------------------------------------ every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard', 'accept'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, vv in o.items():
            if kk not in SKIP:
                yield from strings(vv, kk)
    elif isinstance(o, list):
        for vv in o:
            yield from strings(vv, k)


def tokens(s):
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t else 0), t


for it in items:
    iid = it['id']
    vals = [abs(x) for x in ALLOW.get(iid, [])]
    bad = []
    for s in strings(it):
        if '—' in s or '–' in s or '!' in re.sub(r'\$[^$]*\$', '', s):
            bad.append('dash-or-bang')
        for val, dec, t in tokens(s):
            if dec == 0 and val == int(val) and val <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(val - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    ex._rec(not bad, f'{iid}: every stated number matches route B', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
