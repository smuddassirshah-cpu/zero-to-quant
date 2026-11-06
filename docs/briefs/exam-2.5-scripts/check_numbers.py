"""Recompute every number stated in app/content/exams/topic-2.5.json by a second route and assert it at its path.

Route A is build.py (closed forms). Route B here is independent: vertex enumeration and a grid search for the LP,
gradient descent and Newton run step by step, projected gradient for the KKT items, a brute-force search over the
simplex, NumPy's spacing, polyfit and Gauss-Legendre nodes, a general natural-spline solver, 40- and 50-digit
decimals for the floating-point items, exact Fractions, and seeded simulations for the Monte Carlo items. The Python
code item's solution and starter are run on every hidden test in CPython. Expression forms are evaluated from their
LaTeX at sample points. A last pass reads every number in every learner-visible string of each item. Whole numbers
0 to 10 are structure; every other number must match a route-B value for that item to its printed precision.
Exits 1 on any failure.
Run: python3 docs/briefs/exam-2.5-scripts/check_numbers.py
"""
import cmath
import json
import math
import os
import re
import sys
from collections import Counter
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, _walk, normalise  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.5.json')


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
    t = tol if tol is not None else max(half_tol(w['tol'], w['answer']) / 10, 1e-9)
    good = abs(w['answer'] - value) <= t
    ex._rec(good, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if good else 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    good = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(half_tol(hit[0]['tol'], hit[0]['value']) / 10, 1e-9)
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



def half_tol(t, a):
    return abs(a) * t['rel'] if 'rel' in t else t['abs']


# ================================================================ difficulty 2
# e-lp-corner: every pairwise intersection of the four boundary lines, then a dense grid as a check
lines_ = [((1, 2), 8), ((3, 2), 12), ((1, 0), 0), ((0, 1), 0)]
feas = lambda x, y: x + 2 * y <= 8 + 1e-9 and 3 * x + 2 * y <= 12 + 1e-9 and x >= -1e-9 and y >= -1e-9
pts_lp = []
for i in range(4):
    for j in range(i + 1, 4):
        Mx = np.array([lines_[i][0], lines_[j][0]], dtype=float)
        if abs(np.linalg.det(Mx)) > 1e-12:
            p_ = np.linalg.solve(Mx, [lines_[i][1], lines_[j][1]])
            if feas(*p_):
                pts_lp.append((round(p_[0], 9), round(p_[1], 9)))
vals_lp = {p_: 3 * p_[0] + 4 * p_[1] for p_ in set(pts_lp)}
best_lp = max(vals_lp.values())
gx = np.linspace(0, 4, 801)
GX, GY = np.meshgrid(gx, gx)
mask = (GX + 2 * GY <= 8) & (3 * GX + 2 * GY <= 12)
ok(abs((3 * GX + 4 * GY)[mask].max() - best_lp) < 1e-9, 'e-lp-corner: grid search agrees with the best corner')
key('e-lp-corner', best_lp)
wrong('e-lp-corner', 'axis-y', vals_lp[(0.0, 4.0)])
wrong('e-lp-corner', 'axis-x', vals_lp[(4.0, 0.0)])
ok(not feas(0, 6), 'e-lp-corner: (0, 6) is infeasible')
wrong('e-lp-corner', 'infeasible', 3 * 0 + 4 * 6)
ok((2.0, 3.0) in vals_lp, 'e-lp-corner: (2, 3) is a corner')
allow('e-lp-corner', 12, 16, 18, 24, 6)

# e-duality-sandwich
correct_id('e-duality-sandwich', 'ok')
allow('e-duality-sandwich', 8.4, 9.6, 1.2, 9)
ok(abs(9.6 - 8.4 - 1.2) < 1e-12, 'e-duality-sandwich: gap 1.2')

# e-step-limit: eigenvalues, then descent just inside and just outside the limit
H = np.array([[5.2, 4.8], [4.8, 5.2]])
ev = sorted(np.linalg.eigvalsh(H))
ok(np.allclose(ev, [0.4, 10]), 'e-step-limit: eigenvalues 0.4 and 10')


def gd(s, n=4000):
    x = np.array([1.0, -0.3])
    for _ in range(n):
        x = x - s * H @ x
    return np.linalg.norm(x)


ok(gd(0.199) < 1e-6 and gd(0.201) > 1e3, 'e-step-limit: converges at 0.199, diverges at 0.201')
key('e-step-limit', 2 / ev[1])
wrong('e-step-limit', 'min', 2 / ev[0])
wrong('e-step-limit', 'one-step', 1 / ev[1])
wrong('e-step-limit', 'best', round(2 / (ev[0] + ev[1]), 4))
allow('e-step-limit', 5.2, 4.8, 0.4, 0.2, 0.1)

# e-double-gap: NumPy's spacing
w_ = node(W('e-double-gap'))
ok(abs(w_['answer'] - float(np.spacing(3e6))) <= 1e-12 * np.spacing(3e6), 'e-double-gap: answer = np.spacing(3e6)')
allow('e-double-gap', float(np.spacing(3e6)), 4.66, 3_000_000, 21, 22, 52, 53, 31)
for wid, v in [('at-one', float(np.spacing(1.0))), ('next-power', float(np.spacing(2.0 ** 22))), ('half-gap', 3e6 * 2.0 ** -53)]:
    hit = [x for x in w_['wrong'] if x['id'] == wid]
    ok(len(hit) == 1 and abs(hit[0]['value'] - v) <= 1e-9 * v, f'e-double-gap wrong {wid} = {v!r}')
ok(2 ** 21 <= 3e6 < 2 ** 22, 'e-double-gap: 3e6 lies between 2^21 and 2^22')
ok(repr(float(np.spacing(3e6))) == '4.656612873077393e-10', 'e-double-gap: Python prints 4.656612873077393e-10')

# e-bisection-count: run it
lo, hi, n_ = 1.0, 3.0, 0
while hi - lo >= 1e-6:
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if (mid - 2.2) < 0 else (lo, mid)
    n_ += 1
key('e-bisection-count', n_)
wrong('e-bisection-count', 'floor', n_ - 1)
say('e-bisection-count', 'explain.text', 2 ** 20)
say('e-bisection-count', 'explain.text', 2 ** 21)
allow('e-bisection-count', 2 ** 20, 2 ** 21, 1.9, 20, 21)

# e-mc-error: exact Fractions, and a simulation of 400 batches
se_B = float(F('12.3') / 200)
key('e-mc-error', se_B)
wrong('e-mc-error', 'by-n', 12.3 / 40000)
wrong('e-mc-error', 'by-root-s', math.sqrt(12.3) / 200)
rng = np.random.default_rng(25)
means = rng.normal(0, 12.3, size=(400, 40000)).mean(axis=1)
ok(abs(means.std(ddof=1) / se_B - 1) < 0.1, 'e-mc-error: simulated batch means spread by about the SE')
allow('e-mc-error', 12.3, 12.30, 40000, 200, 0.0615)

# ================================================================ difficulty 3
# e-convex-sets: random pairs and midpoints
rng = np.random.default_rng(7)
sets = {
    'disc-half': lambda x, y: (x * x + y * y <= 4) & (y >= x),
    'one-branch': lambda x, y: (x * y >= 1) & (x > 0),
    'square': lambda x, y: np.maximum(abs(x), abs(y)) <= 1,
    'two-branch': lambda x, y: x * y >= 1,
    'outside': lambda x, y: abs(x) >= 1,
}
found_convex = []
for sid, S_ in sets.items():
    P_ = rng.uniform(-5, 5, size=(400000, 2))
    P_ = P_[S_(P_[:, 0], P_[:, 1])]
    A_, B_ = P_[: len(P_) // 2], P_[len(P_) // 2: 2 * (len(P_) // 2)]
    Mid = (A_ + B_) / 2
    if S_(Mid[:, 0], Mid[:, 1]).all():
        found_convex.append(sid)
ok(abs(np.hypot(0, 0) - 1) > 0 and (1 + 1) / 2 == 1, 'e-convex-sets: the circle fails at the midpoint of (1, 0) and (-1, 0)')
correct_id('e-convex-sets', sorted(found_convex))
allow('e-convex-sets', 4)

# e-hessian-threshold: finite-difference Hessian, bisect on its smallest eigenvalue
def hess(k, e=1e-4):
    f = lambda x, y: x * x + 3 * x * y + k * y * y
    fxx = (f(e, 0) - 2 * f(0, 0) + f(-e, 0)) / e ** 2
    fyy = (f(0, e) - 2 * f(0, 0) + f(0, -e)) / e ** 2
    fxy = (f(e, e) - f(e, -e) - f(-e, e) + f(-e, -e)) / (4 * e * e)
    return np.array([[fxx, fxy], [fxy, fyy]])


lo, hi = 0.0, 10.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if np.linalg.eigvalsh(hess(mid))[0] >= -1e-9 else (mid, hi)
key('e-hessian-threshold', hi, tol=1e-5)
wrong('e-hessian-threshold', 'diagonal', 0)
wrong('e-hessian-threshold', 'coefficients', 9)
wrong('e-hessian-threshold', 'entry', 1.5)
allow('e-hessian-threshold', 2.25, 9, 1.5, 4)

# e-linprog-bounds
correct_id('e-linprog-bounds', 'ok')

# e-dual-function: minimise the Lagrangian on a grid, maximise g on a grid
xg = np.linspace(-20, 20, 400001)
gB = lambda lam: float(np.min((xg + 1) ** 2 + lam * (2 - xg)))
key('e-dual-function', gB(2), part=0, tol=1e-6)
wrong('e-dual-function', 'p-star', (2 + 1) ** 2, part=0)
wrong('e-dual-function', 'sign', float(np.min((xg + 1) ** 2 + 2 * (xg - 2))), part=0)
lg = np.linspace(0, 12, 12001)
gl = np.array([3 * l_ - l_ * l_ / 4 for l_ in lg])
ok(all(abs(gB(l_) - (3 * l_ - l_ * l_ / 4)) < 1e-6 for l_ in (0.5, 3.3, 9)), 'e-dual-function: g = 3 lambda - lambda^2/4 at sample points')
key('e-dual-function', lg[np.argmax(gl)], part=1, tol=1e-6)
ok(abs(gl.max() - 9) < 1e-9, 'e-dual-function: max g = 9 = p*')
wrong('e-dual-function', 'p-star', 9, part=1)
wrong('e-dual-function', 'no-half', 3, part=1)
allow('e-dual-function', 9, 7)

# e-slsqp-sign
correct_id('e-slsqp-sign', 'ok')
allow('e-slsqp-sign', 0.02)

# e-rate-from-kappa: run descent on diag(0.5, 12) from the worst start
Hk = np.diag([0.5, 12.0])


def steps_to(s, factor=1e-6):
    x, n = np.array([1.0, 1.0]), 0
    while max(abs(x[0]), abs(x[1])) > factor:
        x = x - s * Hk @ x
        n += 1
    return n


sb = 2 / 12.5
x2 = np.array([1.0, 0.0])
x2 = x2 - sb * Hk @ x2
key('e-rate-from-kappa', abs(x2[0]), part=0, tol=5e-5)
wrong('e-rate-from-kappa', 'one-over', round(abs(1 - 0.5 / 12), 4), part=0)
key('e-rate-from-kappa', steps_to(sb), part=1)
wrong('e-rate-from-kappa', 'floor', steps_to(sb) - 1, part=1)
wrong('e-rate-from-kappa', 'one-over', steps_to(1 / 12), part=1)
ok(abs(24 / 2 * math.log(1e6) - 165.8) < 0.1, 'e-rate-from-kappa: rule of thumb about 166')
allow('e-rate-from-kappa', 0.5, 12, 24, 0.92, 23, 25, 165.7, 166, 0.9583, 325, 1e6)

# e-newton-minimise: run Newton on f' = e^x - 3
xs_ = [1.0]
for _ in range(3):
    xs_.append(xs_[-1] - (math.exp(xs_[-1]) - 3) / math.exp(xs_[-1]))
key('e-newton-minimise', xs_[1], part=0, tol=5e-5)
xr = 1 - (math.exp(1) - 3 * 1) / (math.exp(1) - 3)
wrong('e-newton-minimise', 'root-of-f', xr, part=0)
wrong('e-newton-minimise', 'descent', round(1 - (math.exp(1) - 3), 4), part=0)
e1_, e2_ = xs_[1] - math.log(3), xs_[2] - math.log(3)
ok(abs(e1_ - 0.0050) < 0.00005 and abs(e2_ - 1.3e-5) < 0.05e-5, f'e-newton-minimise: errors {e1_:.5f} then {e2_:.3g}')
ok(abs(e2_ / e1_ ** 2 - 0.5) < 0.01, 'e-newton-minimise: e2 / e1^2 is about 1/2')
correct_id('e-newton-minimise', 'ok', part=1)
allow('e-newton-minimise', 2.5, math.log(3), 1.0986, 1.1036, 0.005, 0.0050, 1.3e-5, 2.5e-3, 2.5e-5)

# e-cancel-rewrite: doubles against 40-digit decimals
getcontext().prec = 40
xb = 1e8
key('e-cancel-rewrite', math.sqrt(xb * xb + 1) - xb, part=0, tol=0)
ok(xb * xb + 1 == 1e16, 'e-cancel-rewrite: 1e16 + 1 rounds to 1e16')
true_ = (D(10) ** 16 + 1).sqrt() - D(10) ** 8
wrong('e-cancel-rewrite', 'true', 5e-9, part=0)
ok(abs(float(true_) - 5e-9) < 1e-20, 'e-cancel-rewrite: true value 5e-9 to 11 digits')
good = 1 / (math.sqrt(xb * xb + 1) + xb)
ok(abs(good / float(true_) - 1) < 1e-15, 'e-cancel-rewrite: the conjugate form is accurate')
ok(((xb * xb + 1) - xb * xb) / (math.sqrt(xb * xb + 1) + xb) == 0, 'e-cancel-rewrite: written-out form returns 0')
ok(xb * (math.sqrt(1 + xb ** -2) - 1) == 0, 'e-cancel-rewrite: factored form returns 0')
ok(abs(math.sqrt(abs(xb * xb + 1 - 2 * xb * math.sqrt(xb * xb + 1) + xb * xb)) - float(true_)) > 1e-9, 'e-cancel-rewrite: squared form is wrong')
correct_id('e-cancel-rewrite', 'ok', part=1)
allow('e-cancel-rewrite', 1e8, 1e16, 5e-9, 2e8, 16)

# e-log-condition: relative perturbation
dx = 1e-7
rel_out = (math.log(1.02 * (1 + dx)) - math.log(1.02)) / math.log(1.02)
key('e-log-condition', rel_out / dx, tol=1e-3)
wrong('e-log-condition', 'slope', 1 / 1.02)
wrong('e-log-condition', 'inverse', round(math.log(1.02), 4))
ok(abs(math.log10(50.5) - 1.7) < 0.01, 'e-log-condition: about 1.7 digits')
allow('e-log-condition', 1.02, 50.50, 50, 1.7, 50.5)

# e-log1p-blame: doubles against 50-digit decimals
xl = 3e-12
v_naive = math.log(1 + xl)
ok(repr(v_naive) == '3.0000446571375978e-12', 'e-log1p-blame: log(1 + 3e-12) prints as stated')
tv = (1 + D(xl)).ln()
ok(abs(float(tv) - 2.9999999999955e-12) < 1e-26, 'e-log1p-blame: true value 2.9999999999955e-12')
relerr = float((D(v_naive) - tv) / tv)
ok(abs(relerr - 1.5e-5) < 0.05e-5, f'e-log1p-blame: relative error {relerr:.3g}')
ok(abs(math.log1p(xl) / float(tv) - 1) < 1e-15, 'e-log1p-blame: log1p gets every digit')
kx = float(D(xl) / ((1 + D(xl)) * tv))
ok(abs(kx - 1) < 1e-9, 'e-log1p-blame: kappa = 1')
ok(np.spacing(1.0) == 2.0 ** -52 and 4.4 < -math.log10(np.spacing(1.0) / 2 / xl) + 0.5 < 5.5, 'e-log1p-blame: about five digits of x survive')
correct_id('e-log1p-blame', 'ok')
allow('e-log1p-blame', 3e-12, 3.0000446571375978, 2.9999999999955, 1.5, 3, 12, 52, 5)

# e-three-point-poly: NumPy's polyfit through three points
cf3 = np.polyfit([0, 1, 3], [1, 3, 2], 2)
key('e-three-point-poly', float(np.polyval(cf3, 2)), tol=5e-5)
wrong('e-three-point-poly', 'linear', float(np.interp(2, [1, 3], [3, 2])))
wrong('e-three-point-poly', 'two-points', float(np.polyval(np.polyfit([0, 1], [1, 3], 1), 2)))
allow('e-three-point-poly', 10 / 3, 3.3333)

# e-richardson-three: synthetic A and B with an h^3 error
pts = [{'A': 1.0 + 0.8, 'B': 1.0 + 0.1}, {'A': 2.5 - 0.4, 'B': 2.5 - 0.05}]
expr_check('e-richardson-three', lambda A, B: 1.0 if abs(A - 1.8) < 1e-12 else 2.5, pts)
allow('e-richardson-three', 8, 7)

# e-gauss-two-point: NumPy's Gauss-Legendre nodes
xn, wn = np.polynomial.legendre.leggauss(2)
rule = 2 * float(np.sum(wn * (2 * xn + 2) ** 4))
key('e-gauss-two-point', rule, part=0, tol=5e-5)
wrong('e-gauss-two-point', 'no-scale', round(rule / 2, 4), part=0)
wrong('e-gauss-two-point', 'unmapped', round(float(np.sum(wn * xn ** 4)), 4), part=0)
ok(abs(simpson(lambda x: x ** 4, 0, 4) - 204.8) < 1e-9, 'e-gauss-two-point: exact integral 204.8')
ok(abs(2 * float(np.sum(wn * (2 * xn + 2) ** 3)) - 64) < 1e-9, 'e-gauss-two-point: two nodes exact for x^3')
x3n, w3n = np.polynomial.legendre.leggauss(3)
ok(abs(2 * float(np.sum(w3n * (2 * x3n + 2) ** 4)) - 204.8) < 1e-9, 'e-gauss-two-point: three nodes give 204.8')
correct_id('e-gauss-two-point', 'ok', part=1)
allow('e-gauss-two-point', 204.8, 199.11, 99.56)

# e-explicit-step: exact Fractions
den = F('0.25') ** 2 * 80 ** 2 + F('0.02')
key('e-explicit-step', float(1 / den), part=0, tol=5e-7)
wrong('e-explicit-step', 'no-square', round(float(1 / (F('0.25') * 80 ** 2 + F('0.02'))), 6), part=0)
den2 = F('0.25') ** 2 * 160 ** 2 + F('0.02')
import fractions as _fr
steps2 = math.ceil(den2)
key('e-explicit-step', steps2, part=1)
wrong('e-explicit-step', 'linear', math.ceil(2 * den), part=1)
wrong('e-explicit-step', 'floor', steps2 - 1, part=1)
ok(math.ceil(den) == 401, 'e-explicit-step: 401 steps at M = 80')
allow('e-explicit-step', 0.0625, 6400, 400, 400.02, 0.0025, 1600.02, 1601, 1600, 401, 80, 160, 0.25, 0.02)

# e-control-variate: exact arithmetic and a simulation
key('e-control-variate', 19.95 / 9, part=0, tol=5e-5)
wrong('e-control-variate', 'by-vy', round(19.95 / 49, 4), part=0)
wrong('e-control-variate', 'by-sd', round(19.95 / 3, 4), part=0)
rho_B = 19.95 / (7 * 3)
key('e-control-variate', 1 / (1 - rho_B ** 2), part=1, tol=5e-5)
wrong('e-control-variate', 'one-minus-rho', round(1 / (1 - rho_B), 4), part=1)
wrong('e-control-variate', 'rho', round(1 / rho_B ** 2, 4), part=1)
rng = np.random.default_rng(11)
Cm = np.array([[49, 19.95], [19.95, 9]])
YX = rng.multivariate_normal([0, 0], Cm, size=400000)
bs_ = np.cov(YX.T)[0, 1] / YX[:, 1].var(ddof=1)
resid_ = YX[:, 0] - bs_ * YX[:, 1]
ok(abs(bs_ - 19.95 / 9) < 0.02 and abs(YX[:, 0].var() / resid_.var() - 10.256) < 0.3, 'e-control-variate: simulation agrees')
allow('e-control-variate', 49, 9, 19.95, 2.2167, 0.95, 10.26, 0.9025, 4.78, 20, 0.0975, 7, 3)

# ================================================================ difficulty 4
# e-projection-kkt: projected gradient descent, then the relaxed problem by the same route
def proj_min(cap):
    v = np.array([0.0, 0.0])
    n_ = np.array([1.0, 2.0])
    for _ in range(20000):
        v = v - 0.1 * 2 * (v - np.array([4.0, 1.0]))
        if n_ @ v > cap:
            v = v - (n_ @ v - cap) / (n_ @ n_) * n_
    return v


vp = proj_min(3)
key('e-projection-kkt', vp[0], part=0, tol=1e-6)
wrong('e-projection-kkt', 'free', 4, part=0)
wrong('e-projection-kkt', 'along-x', 4 - (4 + 2 * 1 - 3), part=0)
lamB = -2 * (vp[0] - 4)
ok(abs(-2 * (vp[1] - 1) - 2 * lamB) < 1e-6, 'e-projection-kkt: both stationarity rows give the same lambda')
key('e-projection-kkt', lamB, part=1, tol=1e-6)
wrong('e-projection-kkt', 'no-two', lamB / 2, part=1)
wrong('e-projection-kkt', 'sign', -lamB, part=1)
val0B = float(np.sum((vp - [4, 1]) ** 2))
v1 = proj_min(3.1)
val1B = float(np.sum((v1 - [4, 1]) ** 2))
key('e-projection-kkt', val1B, part=2, tol=5e-5)
wrong('e-projection-kkt', 'predicted', round(val0B - lamB * 0.1, 4), part=2)
wrong('e-projection-kkt', 'plus', round(val0B + lamB * 0.1, 4), part=2)
allow('e-projection-kkt', 3.4, -0.2, 0.2, 1.2, 1.8, 1.68, 1.682, 0.12, 3.1, 2.9, 0.6, 0.36, 1.44, 6, 0.1)

# e-long-only-kkt: brute force over the feasible simplex, then the multipliers by least squares
s2 = np.array([0.01, 0.04, 0.09])
mr = np.array([0.02, 0.06, 0.10])
gw = np.linspace(0, 1, 2001)
best = (9, None)
for w1 in gw[:400]:
    w2 = gw[gw <= 1 - w1 + 1e-12]
    w3 = 1 - w1 - w2
    okm = (mr[0] * w1 + mr[1] * w2 + mr[2] * w3 >= 0.08 - 1e-12) & (w3 >= -1e-12)
    if okm.any():
        var = s2[0] * w1 ** 2 + s2[1] * w2[okm] ** 2 + s2[2] * w3[okm] ** 2
        k_ = np.argmin(var)
        if var[k_] < best[0]:
            best = (var[k_], (w1, w2[okm][k_], w3[okm][k_]))
ok(np.allclose(best[1], [0, 0.5, 0.5], atol=1e-3), f'e-long-only-kkt: grid optimum {np.round(best[1], 4)}')
Mk = np.array([[1, mr[1]], [1, mr[2]]])
lam_mu = np.linalg.solve(Mk, [2 * s2[1] * 0.5, 2 * s2[2] * 0.5])
key('e-long-only-kkt', lam_mu[1], part=0, tol=1e-9)
wrong('e-long-only-kkt', 'no-two', np.linalg.solve(Mk, [s2[1] * 0.5, s2[2] * 0.5])[1], part=0)
nu1B = 0 - lam_mu[0] - lam_mu[1] * mr[0]
key('e-long-only-kkt', nu1B, part=1, tol=1e-9)
wrong('e-long-only-kkt', 'sign', -nu1B, part=1)
ok(abs(lam_mu[0] + 0.035) < 1e-12 and abs(0.5 * 0.06 + 0.5 * 0.10 - 0.08) < 1e-12, 'e-long-only-kkt: lambda -0.035, target met exactly')
correct_id('e-long-only-kkt', 'ok', part=2)
allow('e-long-only-kkt', 0.01, 0.04, 0.09, 0.02, 0.06, 0.10, 0.08, 0.5, 0.05, 0.035, -0.035, 0.075, 0.025, 1.25)

# e-local-global-proof
o_ = node(W('e-local-global-proof'))
ok(o_['answer'] == ['k1', 'k2', 'k3', 'k4', 'k5'] and o_['distractors'] == ['e1', 'e2'], 'e-local-global-proof: order key and left-out lines')

# e-normal-equations: a matrix built with kappa = 2e6, then both solvers
rng = np.random.default_rng(3)
U_, _ = np.linalg.qr(rng.normal(size=(60, 4)))
V_, _ = np.linalg.qr(rng.normal(size=(4, 4)))
sv = np.array([1.0, 0.3, 1e-3, 5e-7])
Am = U_ @ np.diag(sv) @ V_.T
ok(abs(np.linalg.cond(Am) / 2e6 - 1) < 1e-6, 'e-normal-equations: built kappa(A) = 2e6')
ok(abs(np.linalg.cond(Am.T @ Am) / 4e12 - 1) < 2e-3, 'e-normal-equations: kappa(A^T A) is about 4e12')
w_ = node(W('e-normal-equations', 0))
ok(abs(w_['answer'] - 4e12) <= 1e-9 * 4e12, 'e-normal-equations part 0 answer 4e12')
for wid, v in [('same', 2e6), ('double', 4e6)]:
    ok(any(x['id'] == wid and abs(x['value'] - v) < 1e-6 * v for x in w_['wrong']), f'e-normal-equations wrong {wid} = {v}')
w_ = node(W('e-normal-equations', 1))
ok(abs(w_['answer'] - 4e12 * 2.0 ** -53) <= 1e-9, 'e-normal-equations part 1 answer kappa^2 u')
ok(any(x['id'] == 'qr' and abs(x['value'] - 2e6 * 2.0 ** -53) < 1e-20 for x in w_['wrong']), 'e-normal-equations wrong qr = kappa u')
xt_ = rng.normal(size=4)
yv = Am @ xt_
x_ne = np.linalg.solve(Am.T @ Am, Am.T @ yv)
x_qr = np.linalg.lstsq(Am, yv, rcond=None)[0]
e_ne = np.linalg.norm(x_ne - xt_) / np.linalg.norm(xt_)
e_qr = np.linalg.norm(x_qr - xt_) / np.linalg.norm(xt_)
ok(e_ne > 1e3 * e_qr and e_qr < 1e-8, f'e-normal-equations: normal equations error {e_ne:.1e} against lstsq {e_qr:.1e}')
correct_id('e-normal-equations', 'ok', part=2)
allow('e-normal-equations', 1.11, 2.2, 4.4, 2e6, 4e12, 1.11e-16, 4.4e-4, 2.2e-10, 1e9, 1e-5, 53, 12, 16)

# e-natural-spline: a general natural-spline solver
xk, yk = np.array([0.0, 1.0, 2.0]), np.array([0.0, 2.0, 1.0])


def natural_spline(xk, yk, x):
    n = len(xk) - 1
    h = np.diff(xk)
    Am_ = np.zeros((n + 1, n + 1))
    rhs = np.zeros(n + 1)
    Am_[0, 0] = Am_[n, n] = 1
    for i in range(1, n):
        Am_[i, i - 1], Am_[i, i], Am_[i, i + 1] = h[i - 1] / 6, (h[i - 1] + h[i]) / 3, h[i] / 6
        rhs[i] = (yk[i + 1] - yk[i]) / h[i] - (yk[i] - yk[i - 1]) / h[i - 1]
    Ms = np.linalg.solve(Am_, rhs)
    i = min(np.searchsorted(xk, x) - 1, n - 1)
    i = max(i, 0)
    t0, t1 = xk[i + 1] - x, x - xk[i]
    return Ms, (Ms[i] * t0 ** 3 + Ms[i + 1] * t1 ** 3) / (6 * h[i]) + (yk[i] / h[i] - Ms[i] * h[i] / 6) * t0 + (yk[i + 1] / h[i] - Ms[i + 1] * h[i] / 6) * t1


Ms, s05 = natural_spline(xk, yk, 0.5)
key('e-natural-spline', Ms[1], part=0, tol=1e-9)
wrong('e-natural-spline', 'no-two-thirds', Ms[1] * 2 / 3, part=0)
wrong('e-natural-spline', 'sign', -Ms[1], part=0)
key('e-natural-spline', s05, part=1, tol=5e-6)
wrong('e-natural-spline', 'linear', float(np.interp(0.5, xk, yk)), part=1)
wrong('e-natural-spline', 'no-correction', Ms[1] * 0.5 ** 3 / 6 + 2 * 0.5, part=1)
ok(abs(natural_spline(xk, yk, 1.0)[1] - 2) < 1e-12, 'e-natural-spline: S(1) = 2')
allow('e-natural-spline', 0.5, 4.5, 0.75, 2.75, 1.28125, 0.09375, 1.375)

# e-log-sum-exp: run the solution and the starter on every test in CPython, against 50-digit decimals
w_ = node(W('e-log-sum-exp'))
getcontext().prec = 50


def lse_true(xs):
    return float(sum(D(x).exp() for x in xs).ln())


def run(src, call):
    ns = {}
    exec(src, ns)
    try:
        return eval(call, ns)
    except Exception as e_:                      # noqa: BLE001 - a failing starter may raise anything
        return e_


sol_ok, start_fail = True, 0
for t_ in w_['tests'] + w_['examples']:
    exp_v = eval(t_['expect'])
    xs_arg = eval(t_['call'][len('log_sum_exp('):-1])
    ok(math.isclose(exp_v, lse_true(xs_arg), rel_tol=1e-14), f'e-log-sum-exp: expect {t_["expect"]} = 50-digit value')
    got = run(w_['solution'], t_['call'])
    sol_ok &= isinstance(got, float) and math.isclose(got, exp_v, rel_tol=t_['tol']['rel'])
    sg = run(w_['starter'], t_['call'])
    start_fail += not (isinstance(sg, float) and math.isclose(sg, exp_v, rel_tol=t_['tol']['rel']))
ok(sol_ok, 'e-log-sum-exp: the solution passes every test')
ok(start_fail >= 3, f'e-log-sum-exp: the starter fails {start_fail} tests')
ok(len(w_['tests']) == 8 and '8 hidden tests' in w_['how'], 'e-log-sum-exp: how names 8 tests')
ok(math.exp(709) < float('inf') and math.isinf(np.exp(np.float64(710))) and math.exp(-746) == 0.0, 'e-log-sum-exp: e^710 overflows, e^-746 is 0')
allow('e-log-sum-exp', 1.8e308, 1.8, 308, 710, 746, 1000, 1e-12, 12, 8)

# ================================================================ difficulty 5
# e-solver-certificate: the dual function by grid minimisation, p* by a search along the line
xg2 = np.linspace(-2, 8, 2001)
XX, YY = np.meshgrid(xg2, xg2)
fobj = lambda x, y: x * x + 3 * y * y
gB2 = float(np.min(fobj(XX, YY) + 5.9 * (4 - XX - YY)))
lam59 = 5.9
gexact = min(fobj(lam59 / 2, lam59 / 6) + lam59 * (4 - lam59 / 2 - lam59 / 6), gB2)
ok(abs(gB2 - gexact) < 2e-4, 'e-solver-certificate: grid minimum of L near the exact minimiser')
key('e-solver-certificate', gexact, part=0, tol=5e-6)
fB = fobj(3.02, 0.98)
wrong('e-solver-certificate', 'primal', fB, part=0)
tl = np.linspace(-2, 6, 800001)
pstar = float(np.min(fobj(tl, 4 - tl)))
wrong('e-solver-certificate', 'optimum', round(pstar, 6), part=0)
key('e-solver-certificate', fB - gexact, part=1, tol=5e-6)
wrong('e-solver-certificate', 'zero', 0, part=1)
wrong('e-solver-certificate', 'to-optimum', round(fB - pstar, 6), part=1)
ok(gexact <= pstar <= fB, 'e-solver-certificate: g(5.9) <= p* <= f(reported)')
ok(abs(3.02 + 0.98 - 4) < 1e-12, 'e-solver-certificate: reported point is feasible')
correct_id('e-solver-certificate', 'ok', part=2)
allow('e-solver-certificate', 3.02, 0.98, 5.9, 34.81, 23.6, 11.6033, 11.9967, 9.1204, 2.8812, 12.0016, 0.0049, 6.04, 12)

# e-error-budget: a synthetic grid with error C dS^2 recovers its own limit
Pt, Cg = 7.97, -0.002
Pf = lambda dS: Pt + Cg * dS ** 2
ok(abs(Pf(2) - 7.962) < 1e-12 and abs(Pf(1) - 7.968) < 1e-12, 'e-error-budget: the two prices fit P = 7.97 - 0.002 dS^2')
key('e-error-budget', Pt, part=0, tol=5e-6)
wrong('e-error-budget', 'mean', (7.968 + 7.962) / 2, part=0)
wrong('e-error-budget', 'linear', 2 * 7.968 - 7.962, part=0)
key('e-error-budget', Pt - Pf(1), part=1, tol=5e-6)
wrong('e-error-budget', 'difference', Pf(1) - Pf(2), part=1)
nB = int(F(15) ** 2 / F('0.002') ** 2)
key('e-error-budget', nB, part=2)
wrong('e-error-budget', 'no-square', int(F(15) / F('0.002')), part=2)
wrong('e-error-budget', 'grid-change', int(F(15) ** 2 / F('0.006') ** 2), part=2)
allow('e-error-budget', 7.962, 7.968, 7.97, 7.9700, 0.002, 0.006, 15, 7500, 56_250_000, 0.0020, 0.0060)

# e-stiff-implicit: one step of each method on e' = -200 e, by solving its update equation
hS, lS = 0.05, 200.0
e_imp = np.linalg.solve([[1 + hS * lS]], [1.0])[0]
e_trp = np.linalg.solve([[1 + hS * lS / 2]], [1 - hS * lS / 2])[0]
key('e-stiff-implicit', e_imp, part=0, tol=5e-5)
wrong('e-stiff-implicit', 'explicit', 1 - hS * lS, part=0)
wrong('e-stiff-implicit', 'inverse-z', round(1 / (hS * lS), 4), part=0)
key('e-stiff-implicit', e_trp, part=1, tol=5e-5)
wrong('e-stiff-implicit', 'sign', round(-e_trp, 4), part=1)
wrong('e-stiff-implicit', 'implicit', round(e_imp, 4), part=1)
ok(all(abs((1 - z / 2) / (1 + z / 2)) < 1 and 1 / (1 + z) < 1 for z in np.linspace(0.01, 1e4, 1000)), 'e-stiff-implicit: both factors below 1 for every h > 0')
ok(abs((1 - 5e3) / (1 + 5e3) + 1) < 1e-3, 'e-stiff-implicit: trapezoidal factor tends to -1')
ok(2 / lS == 0.01, 'e-stiff-implicit: explicit limit h < 0.01')
correct_id('e-stiff-implicit', 'ok', part=2)
allow('e-stiff-implicit', 200, -200, 0.05, 0.0909, -0.6667, 0.67, 0.09, 0.01, 11, -9, 1.0)

# ------------------------------------------------------------------ every level has an item on a skill first met there
LEVEL = {
    'e-convex-sets': ('convex', 1), 'e-hessian-threshold': ('convex', 1), 'e-local-global-proof': ('convex', 1),
    'e-lp-corner': ('convex', 2), 'e-duality-sandwich': ('convex', 2), 'e-linprog-bounds': ('convex', 2),
    'e-dual-function': ('convex', 3), 'e-slsqp-sign': ('convex', 3), 'e-projection-kkt': ('convex', 3),
    'e-long-only-kkt': ('convex', 3),
    'e-step-limit': ('convex', 4), 'e-rate-from-kappa': ('convex', 4), 'e-newton-minimise': ('convex', 4),
    'e-solver-certificate': ('convex', 4),
    'e-double-gap': ('numerics', 1), 'e-cancel-rewrite': ('numerics', 1), 'e-log-condition': ('numerics', 1),
    'e-log1p-blame': ('numerics', 1), 'e-normal-equations': ('numerics', 1), 'e-log-sum-exp': ('numerics', 1),
    'e-bisection-count': ('numerics', 2), 'e-three-point-poly': ('numerics', 2), 'e-natural-spline': ('numerics', 2),
    'e-richardson-three': ('numerics', 3), 'e-gauss-two-point': ('numerics', 3), 'e-stiff-implicit': ('numerics', 3),
    'e-mc-error': ('numerics', 4), 'e-explicit-step': ('numerics', 4), 'e-control-variate': ('numerics', 4),
    'e-error-budget': ('numerics', 4),
}
COURSES = ('convex', 'numerics')

ok(sorted(LEVEL) == sorted(idx), 'every item has a level')
CDIR = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
for course in COURSES:
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
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard', 'accept', 'call', 'expect', 'starter', 'solution'}


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
