"""Recompute every number stated in app/content/exams/topic-1.10.json by a second route and assert it at its path.

Route A is build.py (closed forms). Route B here is independent: exact Fractions, brute-force loops and searches,
NumPy linear algebra, numerical integration and differentiation, matrices built from their Jordan blocks, and the
rearranged series summed term by term. Expression keys are evaluated from their LaTeX at sample points and compared
with the route-B function; every accepted form must agree and every wrong form must differ.
A last pass reads every number in every learner-visible string of each item. Whole numbers 0 to 10 are taken as
structure (indices, exponents, "4 decimal places"); every other number must match a route-B value for that item
to its printed precision. Exits 1 on any failure.
Run: python3 docs/briefs/exam-1.10-scripts/check_numbers.py
"""
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

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.10.json')


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
ALLOW = {}          # iid -> route-B values that may appear in its text


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None, tol=None):
    w = node(W(iid, part))
    t = tol if tol is not None else max(w['tol']['abs'] / 10, 1e-9)
    ok = abs(w['answer'] - value) <= t
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if ok else 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {value!r}', '' if ok else f'found {hit}')
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


# ------------------------------------------------------------------ LaTeX evaluation for expression keys
def _group(s, i):
    """s[i] == '{': return (inside, index after the matching brace)."""
    depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError(s)


def tex_py(s):
    s = s.replace('\\varepsilon', 'e').replace('\\left', '').replace('\\right', '').replace(' ', '')
    out, i = '', 0
    while i < len(s):
        if s.startswith('\\frac', i):
            a, i = _group(s, i + 5)
            b, i = _group(s, i)
            out += f'(({tex_py(a)})/({tex_py(b)}))'
        elif s.startswith('\\sqrt', i):
            a, i = _group(s, i + 5)
            out += f'@(({tex_py(a)}))'
        else:
            out += s[i]
            i += 1
    out = re.sub(r'(?<=[\d)xyne])(?=[xyne@(])', '*', out)
    return out.replace('@', 'sqrt').replace('^', '**')


def tex_val(s, **v):
    if s.startswith('\\begin{pmatrix}'):
        body = s[len('\\begin{pmatrix}'):-len('\\end{pmatrix}')]
        return np.array([[float(eval(tex_py(c), {'sqrt': math.sqrt}, v)) for c in row.split('&')] for row in body.split('\\\\')])
    if s.startswith('[['):
        return np.array(eval(s))
    val = eval(tex_py(s), {'sqrt': math.sqrt}, v)
    return np.array(val, dtype=float)


def expr_check(iid, fn, pts, part=None, wrong_ids=()):
    """fn(**pt) is route B. The answer and every accept must equal it at every point; every wrong must differ."""
    w = node(W(iid, part))
    lab = f'{iid}{"" if part is None else f" part {part}"}'
    for form in [w['answer']] + w.get('accept', []):
        ok = all(np.allclose(tex_val(form, **p), fn(**p), rtol=1e-9, atol=1e-12) for p in pts)
        ex._rec(ok, f'{lab} expression {form!r} = route B at {len(pts)} points', '')
    for x in w.get('wrong', []):
        diff = any(not np.allclose(tex_val(x['tex'], **p), fn(**p), rtol=1e-6) for p in pts)
        ex._rec(diff, f'{lab} wrong "{x["id"]}" {x["tex"]!r} differs from the key', '')
    ex._rec(sorted(x['id'] for x in w.get('wrong', [])) == sorted(wrong_ids), f'{lab} wrong ids {sorted(wrong_ids)}', '')


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------ the file
ex._rec(len(items) == 30, '30 items', '')
ramp = Counter(i['difficulty'] for i in items)
ex._rec(dict(ramp) == {2: 6, 3: 15, 4: 6, 5: 3}, f'ramp {dict(ramp)} = 6, 15, 6, 3', '')
pace = sum(i['pace'] for i in items)
ex._rec(pace / 60 < doc['minutes'], f'pace {pace} s inside {doc["minutes"]} minutes', '')
by_course = Counter('analysis' if all(s.startswith('an-') for s in i['skills']) else 'linear-maps' for i in items)
ex._rec(by_course == {'analysis': 17, 'linear-maps': 13}, f'by course {dict(by_course)}', '')
ex._rec(all(all(s.startswith('an-') for s in i['skills']) or all(s.startswith('lx-') for s in i['skills']) for i in items),
        'no item mixes the two courses', '')
for s in doc['skills']:
    ex._rec(any(s in i['skills'] for i in items if i.get('kind') != 'longform'), f'skill {s} tested by an auto item', '')
for it in items:
    for w in [it.get('widget')] + [p['widget'] for p in it.get('parts', [])]:
        if isinstance(w, dict) and w.get('kind') in ('choice', 'multi'):
            ex._rec(w.get('shuffle') is True, f'{it["id"]}: {w["kind"]} has shuffle true', '')

# ================================================================== difficulty 2
# e-sup-rising: terms by Fractions, increasing, below 2, within eps of 2
terms = [F(2 * n + 1, n + 4) for n in range(1, 5001)]
ex._rec(all(a < b for a, b in zip(terms, terms[1:])) and all(t < 2 for t in terms), 'e-sup-rising: terms rise and stay below 2', '')
for e_ in (F(1, 10), F(1, 1000)):
    n_need = next(n for n in range(1, 10 ** 6) if F(2 * n + 1, n + 4) > 2 - e_)
    ex._rec(n_need <= 7 / e_ + 1, f'e-sup-rising: a term above 2 - {e_} by n = {n_need} <= 7/eps', '')
ex._rec(terms[:4] == [F(3, 5), F(5, 6), F(1), F(9, 8)], 'e-sup-rising: first terms 3/5, 5/6, 1, 9/8', '')
ex._rec(all(2 - t == F(7, n + 4) for n, t in zip(range(1, 200), terms)), 'e-sup-rising: 2 - a_n = 7/(n + 4)', '')
correct_id('e-sup-rising', 'ok')
allow('e-sup-rising', 2, 7)

# e-diagonal-digits: build x digit by digit from the strings in the prose
rows = re.findall(r'x_\d = 0\.(\d{4})', node(P('e-diagonal-digits'))['prose'])
ex._rec(len(rows) == 4, 'e-diagonal-digits: four list entries read from the prose', '')
xd = ''.join({'5': '4'}.get(rows[k][k], '5') for k in range(4))
key('e-diagonal-digits', float('0.' + xd))
wrong('e-diagonal-digits', 'copied', float('0.' + ''.join(rows[k][k] for k in range(4))))
wrong('e-diagonal-digits', 'row', float('0.' + ''.join({'5': '4'}.get(c, '5') for c in rows[0])))
ex._rec(all(xd[k] != rows[k][k] for k in range(4)), 'e-diagonal-digits: x differs from each x_k at digit k', '')
allow('e-diagonal-digits', *[float('0.' + r_) for r_ in rows], 0.4999, 0.5)
say('e-diagonal-digits', 'explain.text', 0.4554)

# e-telescope-gap-three: exact partial sums, then the limit by the tail bound
S = F(0)
for n in range(1, 3001):
    S += F(1, n * (n + 3))
ex._rec(abs(float(S) - 11 / 18) < 1 / 3000, f'e-telescope-gap-three: S_3000 = {float(S):.6f} within 1/3000 of the key', '')
ex._rec(S == F(1, 3) * (1 + F(1, 2) + F(1, 3) - F(1, 3001) - F(1, 3002) - F(1, 3003)), 'e-telescope-gap-three: S_n closed form', '')
key('e-telescope-gap-three', float(F(11, 18)))
wrong('e-telescope-gap-three', 'no-third', float(3 * F(11, 18)))
wrong('e-telescope-gap-three', 'one-term', 1 / 3)
say('e-telescope-gap-three', 'explain.text', 0.6111)
allow('e-telescope-gap-three', 11, 18, 0.6111, float(3 * F(11, 18)))

# e-halvings-width: halve until the width is below 0.001
w_, k_ = F(3), 0
while w_ >= F(1, 1000):
    w_, k_ = w_ / 2, k_ + 1
key('e-halvings-width', k_, tol=0)
w1, k1 = F(1), 0
while w1 >= F(1, 1000):
    w1, k1 = w1 / 2, k1 + 1
wrong('e-halvings-width', 'unit-width', k1)
wrong('e-halvings-width', 'floor', math.floor(math.log(3000) / math.log(2)))
allow('e-halvings-width', 0.001, 3000, 2048, 4096, 11.55, float(F(3, 4096)), float(F(3, 2048)), 11, 12)
ex._rec(round(float(F(3, 4096)), 5) == 0.00073 and round(float(F(3, 2048)), 4) == 0.0015, 'e-halvings-width: 0.00073 and 0.0015', '')
say('e-halvings-width', 'explain.text', 12)

# e-gram-schmidt-step: orthonormalise with QR, and project by least squares; then both wrong routes
gv1, gv2 = np.array([1.0, -2.0, 2.0]), np.array([3.0, 0.0, 3.0])
Qg, Rg = np.linalg.qr(np.column_stack([gv1, gv2]))
coef_ls = np.linalg.lstsq(gv1.reshape(3, 1), gv2, rcond=None)[0][0]
f2 = gv2 - coef_ls * gv1
ex._rec(abs(coef_ls - 1) < 1e-12 and np.allclose(f2, [2, 2, 1]) and abs(f2 @ gv1) < 1e-12,
        'e-gram-schmidt-step: coefficient 9/9 = 1, f2 = (2, 2, 1), orthogonal to v1', '')
key('e-gram-schmidt-step', float(abs(Rg[1, 1])), tol=1e-9)
key('e-gram-schmidt-step', float(np.linalg.norm(f2)), tol=1e-9)
wrong('e-gram-schmidt-step', 'root-norm', float(np.linalg.norm(gv2 - (gv2 @ gv1 / np.linalg.norm(gv1)) * gv1)))
wrong('e-gram-schmidt-step', 'no-sub', float(np.linalg.norm(gv2)))
allow('e-gram-schmidt-step', 9, 3, 18, 6.71, 4, 1)

# e-subspace-r3: random closure tests on each set
rng = np.random.default_rng(110)
sets = {'ok': lambda x: abs(x[0] - 2 * x[2]) < 1e-9, 'product': lambda x: abs(x[0] * x[1]) < 1e-9,
        'affine': lambda x: abs(x[0] + x[1] - 1) < 1e-9, 'half': lambda x: x[0] >= 0}
samples = {'ok': lambda: (lambda a, b: np.array([2 * b, a, b]))(*rng.normal(size=2)),
           'product': lambda: np.array([0, rng.normal(), rng.normal()]) if rng.random() < 0.5 else np.array([rng.normal(), 0, rng.normal()]),
           'affine': lambda: (lambda a, c: np.array([a, 1 - a, c]))(*rng.normal(size=2)),
           'half': lambda: np.array([abs(rng.normal()), rng.normal(), rng.normal()])}
closed = {}
for name in sets:
    ok = sets[name](np.zeros(3))
    for _ in range(200):
        u, v, c = samples[name](), samples[name](), rng.normal() * 3
        ok = ok and sets[name](u + v) and sets[name](c * u)
    closed[name] = ok
ex._rec(closed == {'ok': True, 'product': False, 'affine': False, 'half': False}, f'e-subspace-r3: closure tests {closed}', '')
ex._rec(not sets['product'](np.array([1, 0, 0]) + np.array([0, 1, 0])), 'e-subspace-r3: (1,0,0)+(0,1,0) leaves the product set', '')
correct_id('e-subspace-r3', 'ok')

# ================================================================== difficulty 3
# e-rational-between: exact search for the smallest n with n(b - a) > 1, then m
a, b = F(47, 100), F(495, 1000)
n_ = next(n for n in range(1, 10 ** 4) if n * (b - a) > 1)
m_ = math.floor(n_ * a) + 1
key('e-rational-between', n_, part=0, tol=0)
wrong('e-rational-between', 'at-bound', int(1 / (b - a)), part=0)
key('e-rational-between', m_, part=1, tol=0)
wrong('e-rational-between', 'no-plus', m_ - 1, part=1)
ex._rec(a < F(m_, n_) < b and not (a < F(m_ - 1, n_)), 'e-rational-between: a < m/n < b and (m-1)/n <= a', '')
allow('e-rational-between', 0.47, 0.495, 0.025, 40, 41, 19, 20, float(n_ * a), round(float(F(m_, n_)), 4),
      round(float(F(m_ - 1, n_)), 4), 1)
say('e-rational-between', 'explain.text', 0.4878)

# e-n-for-quotient: |a_n - 2| exactly, smallest N by search, threshold by bisection
ex._rec(all(abs(F(4 * n + 3, 2 * n - 1) - 2) == F(5, 2 * n - 1) for n in range(1, 500)), 'e-n-for-quotient: |a_n - 2| = 5/(2n - 1)', '')
e_ = F(2, 100)
N_ = next(N for N in range(1, 10 ** 4) if all(abs(F(4 * n + 3, 2 * n - 1) - 2) < e_ for n in range(N, N + 400)))
key('e-n-for-quotient', N_, part=1, tol=0)
wrong('e-n-for-quotient', 'floor', N_ - 1, part=1)
wrong('e-n-for-quotient', 'no-half', math.floor(5 / e_ + 1) + 1, part=1)
expr_check('e-n-for-quotient', lambda e: bisect(lambda n: 5 / (2 * n - 1) - e, 0.5 + 1e-12, 1e7),
           [{'e': v} for v in (0.3, 0.7, 1.3, 2.9)], part=0, wrong_ids=['minus', 'no-half'])
thr = bisect(lambda n: 5 / (2 * n - 1) - 0.02, 1, 1e6)
allow('e-n-for-quotient', 0.02, 0.04, thr, 251, 249, round(5 / 249, 4), 125, 126)
say('e-n-for-quotient', 'explain.text', 125.5)
say('e-n-for-quotient', 'explain.text', 126)

# e-root-recursion: iterate, check monotone and bounded, and both roots
seq = [1.0]
for _ in range(200):
    seq.append(math.sqrt(3 * seq[-1] + 10))
ex._rec(all(x < y < 5 for x, y in zip(seq[:15], seq[1:16])), 'e-root-recursion: rises below 5', '')
key('e-root-recursion', seq[-1], part=1)
roots = sorted(np.roots([1, -3, -10]).real)
wrong('e-root-recursion', 'neg-root', roots[0], part=1)
ex._rec(abs(roots[1] - 5) < 1e-12, 'e-root-recursion: roots -2 and 5', '')
correct_id('e-root-recursion', 'ok', part=0)
say('e-root-recursion', 'prose', round(seq[1], 3), fmt='{:.3f}')
say('e-root-recursion', 'prose', round(seq[2], 3), fmt='{:.3f}')
allow('e-root-recursion', seq[1], seq[2], 25, 10, 5)

# e-which-converge: partial sums and ratios
n_arr = np.arange(1, 200001, dtype=float)
s_ratio = np.cumsum(n_arr[:200] ** 3 / 2.0 ** n_arr[:200])
s_cos = np.cumsum(np.cos(n_arr) ** 2 / n_arr ** 1.5)
s_root = np.cumsum(1 / np.sqrt(n_arr))
ex._rec(abs(s_ratio[-1] - 26) < 1e-9, f'e-which-converge: sum n^3/2^n = {s_ratio[-1]:.6f} (26)', '')
ex._rec(s_cos[-1] < 2.62 and s_cos[-1] - s_cos[100000] < 2 / math.sqrt(100000), 'e-which-converge: cosine series bounded by the p = 3/2 series', '')
ex._rec(s_root[-1] > 800, 'e-which-converge: sum 1/sqrt n passes 800 by n = 200000', '')
ex._rec(abs(2 * 10 ** 6 / (5 * 10 ** 6 + 1) - 0.4) < 1e-6, 'e-which-converge: 2n/(5n + 1) -> 2/5', '')
rat = [math.factorial(n + 2) / 4 ** (n + 1) / (math.factorial(n + 1) / 4 ** n) for n in range(1, 30)]
ex._rec(all(abs(r_ - (n + 2) / 4) < 1e-9 for n, r_ in zip(range(1, 30), rat)) and rat[0] < 1 and rat[1] <= 1,
        'e-which-converge: ratio (n + 2)/4, first ratios at most 1', '')
ex._rec(abs(((51 / 50) ** 3) / 2 - 0.5) < 0.04, 'e-which-converge: n^3/2^n ratio tends to 1/2', '')
correct_id('e-which-converge', ['ratio', 'comp'])

# e-cube-delta: the factor on a fine grid of (1, 3), then delta checked by brute force
g = np.linspace(1, 3, 200001)[1:-1]
fac = g ** 2 + 2 * g + 4
ex._rec(fac.max() < 19 and 19 - fac.max() < 1e-3, f'e-cube-delta: sup of the factor on (1, 3) = 19 (grid max {fac.max():.5f})', '')
key('e-cube-delta', round(float(fac.max())), part=0, tol=0)
wrong('e-cube-delta', 'at-a', 2 ** 2 + 2 * 2 + 4, part=0)
wrong('e-cube-delta', 'at-left', float(fac.min().round()), part=0)
dlt = min(1, 0.38 / 19)
key('e-cube-delta', dlt, part=1)
wrong('e-cube-delta', 'at-a', 0.38 / 12, part=1)
_a = [x_ for x_ in node(W('e-cube-delta', 1))['wrong'] if x_['id'] == 'at-a'][0]
ex._rec(all(abs(v_ - _a['value']) <= _a['tol']['abs'] for v_ in (0.0317, 0.032, 0.031667)), 'e-cube-delta: at-a band catches 0.0317 and 0.032', '')
wrong('e-cube-delta', 'max', max(1, 0.38 / 19), part=1)
xs = np.linspace(2 - dlt, 2 + dlt, 100001)[1:-1]
ex._rec(np.all(np.abs(xs ** 3 - 8) < 0.38), 'e-cube-delta: |x^3 - 8| < 0.38 on (1.98, 2.02)', '')
allow('e-cube-delta', 19, 0.38, 12, dlt, 25, 9)
say('e-cube-delta', 'explain.text', 0.02)

# e-mvt-quartic: bisection for c on a numerical derivative, grid max for M
fM = lambda x: x ** 4 + x  # noqa: E731
dfM = lambda x, h=1e-6: (fM(x + h) - fM(x - h)) / (2 * h)  # noqa: E731
slope = (fM(2) - fM(0)) / 2
c_ = bisect(lambda x: dfM(x) - slope, 0, 2)
key('e-mvt-quartic', c_, part=0, tol=1e-6)
wrong('e-mvt-quartic', 'mid', 1.0, part=0)
wrong('e-mvt-quartic', 'no-root', round(c_ ** 3, 6), part=0)
gg = np.linspace(0, 2, 20001)
Mx = float(np.max(np.abs(dfM(gg))))
key('e-mvt-quartic', round(Mx, 6), part=1, tol=0)
wrong('e-mvt-quartic', 'mean-slope', slope, part=1)
wrong('e-mvt-quartic', 'no-plus', round(Mx, 6) - 1, part=1)
pairs = rng.uniform(0, 2, size=(2000, 2))
ex._rec(np.all(np.abs(fM(pairs[:, 0]) - fM(pairs[:, 1])) <= Mx * np.abs(pairs[:, 0] - pairs[:, 1]) + 1e-9), 'e-mvt-quartic: Lipschitz bound 33 holds', '')
allow('e-mvt-quartic', slope, 18, c_, fM(2), 33, 32, 8)
say('e-mvt-quartic', 'explain.text', 1.2599)

# e-upper-sum-square: x^3 on [0, 2]; sup and inf on each piece by dense sampling; exact gap search
def sums(n, f=lambda x: x ** 3, a0=0.0, b0=2.0, k=2001):
    U = L_ = 0.0
    edges = np.linspace(a0, b0, n + 1)
    for lo, hi in zip(edges, edges[1:]):
        v = f(np.linspace(lo, hi, k))
        U += v.max() * (hi - lo)
        L_ += v.min() * (hi - lo)
    return U, L_


U4, L4 = sums(4)
key('e-upper-sum-square', U4, part=0)
wrong('e-upper-sum-square', 'lower', L4, part=0)
wrong('e-upper-sum-square', 'mid', sum((0.25 + 0.5 * k) ** 3 * 0.5 for k in range(4)), part=0)


def gap(n):
    return sum((F(2 * k, n) ** 3 - F(2 * (k - 1), n) ** 3) * F(2, n) for k in range(1, n + 1))


ex._rec(gap(4) == F(4) and abs(float(gap(4)) - (U4 - L4)) < 1e-9, 'e-upper-sum-square: U - L = 4 at n = 4, both routes', '')
n_ul = next(n for n in range(1590, 1700) if gap(n) < F(1, 100))
key('e-upper-sum-square', n_ul, part=1, tol=0)
wrong('e-upper-sum-square', 'at-bound', n_ul - 1, part=1)
ex._rec(gap(1600) == F(1, 100) and gap(n_ul) < F(1, 100), 'e-upper-sum-square: gap exactly 0.01 at n = 1600', '')
wrong('e-upper-sum-square', 'no-width', next(n for n in range(1, 1700) if F(8, n) < F(1, 100)), part=1)
allow('e-upper-sum-square', 0.5, 0.125, 3.375, 2.25, U4, L4, 0.01, 1600, 1601, 16, 1)
say('e-upper-sum-square', 'explain.text', 6.25)

# e-ftc-both-limits: F(x) = integral from x to x^3, by composite Simpson, then a central difference
def simpson(f, lo, hi, n=2000):
    h = (hi - lo) / n
    s = f(lo) + f(hi) + sum((4 if k % 2 else 2) * f(lo + k * h) for k in range(1, n))
    return s * h / 3


Ff = lambda x: simpson(lambda t: 1 / (1 + t * t), x, x ** 3)  # noqa: E731
hh = 1e-4
dF = (Ff(2 + hh) - Ff(2 - hh)) / (2 * hh)
key('e-ftc-both-limits', dF, tol=1e-6)
ex._rec(abs(dF + 1 / 65) < 1e-7, f'e-ftc-both-limits: numerical F\'(2) = {dF:.8f} = -1/65', '')
wrong('e-ftc-both-limits', 'no-chain', 1 / (1 + 8 ** 2) - 1 / (1 + 2 ** 2))
wrong('e-ftc-both-limits', 'upper-only', 12 / 65)
# negative-key pass: `sign` is the absolute value of the computed key (negative, so it differs); its byKey line uses 12/65, 1/5 = 13/65
ex._rec(dF < 0 and abs(1 / 5 - 12 / 65 - 1 / 65) < 1e-12, 'e-ftc-both-limits: the computed key is negative, 12/65 - 1/5 = -1/65', '')
wrong('e-ftc-both-limits', 'sign', abs(dF))
allow('e-ftc-both-limits', 1 / 65, 12 / 65, 12, 65, 5, 3, 13)
say('e-ftc-both-limits', 'explain.text', '0.0154')

# e-closed-sets: a sequence check for each set that is not closed
ex._rec(1 / 10 ** 6 > 0 and all(0 < 1 / n <= 1 for n in range(1, 1000)), 'e-closed-sets: 1/n lies in (0, 1] and tends to 0', '')
ex._rec(all(-1 / n < 0 and 1 < 1 + 1 / n for n in range(1, 1000)), 'e-closed-sets: 0 and 1 lie in every (-1/n, 1 + 1/n)', '')
cf = [F(1)]
for _ in range(30):
    cf.append(1 + 1 / (1 + cf[-1]))          # rationals tending to sqrt 2
ex._rec(abs(float(cf[-1]) / 2 - math.sqrt(2) / 2) < 1e-12 and all(0 <= x / 2 <= 1 for x in cf), 'e-closed-sets: rationals in [0, 1] tend to sqrt2/2', '')
correct_id('e-closed-sets', ['z', 'powers', 'meet'])

# e-coords-new-basis: solve the 3 x 3 system
Bm = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]], dtype=float)   # columns: 1 + x, x + x^2, x^2 in (1, x, x^2)
coords = np.linalg.solve(Bm, [3, 2, 5])
expr_check('e-coords-new-basis', lambda: coords, [{}], wrong_ids=['std', 'rev'])

# e-antisym-map: the 16 x 16 matrix of T, its rank and nullity
Tm = np.zeros((16, 16))
for k in range(16):
    E = np.zeros(16)
    E[k] = 1
    A = E.reshape(4, 4)
    Tm[:, k] = (A - A.T).ravel()
rk = np.linalg.matrix_rank(Tm)
key('e-antisym-map', 16 - rk, part=0, tol=0)
key('e-antisym-map', rk, part=1, tol=0)
wrong('e-antisym-map', 'skew', rk, part=0)
wrong('e-antisym-map', 'diag', 4, part=0)
wrong('e-antisym-map', 'full', 16, part=1)
allow('e-antisym-map', 16, 16 - rk, rk, 4)
say('e-antisym-map', 'explain.text', 16 - rk)

# e-matrix-of-map: apply T to each basis polynomial with numpy's polynomial class
Poly = np.polynomial.Polynomial
cols = []
for k in range(3):
    p = Poly([1 if j == k else 0 for j in range(3)])
    tp = p.deriv() + p(0) * Poly([0, 0, 1])
    c = np.zeros(3)
    c[:len(tp.coef)] = tp.coef
    cols.append(c)
Mt = np.array(cols).T
expr_check('e-matrix-of-map', lambda: Mt, [{}], wrong_ids=['rows', 'no-eval'])

# e-dual-basis-pair: B^{-1} by numpy, the dual map by composition at sample points
Bd = np.array([[2, 3], [1, 2]], dtype=float)
rowsB = np.linalg.inv(Bd)
phi1 = lambda x, y: rowsB[0] @ np.array([x, y])  # noqa: E731
ex._rec(np.allclose([phi1(2, 1), phi1(3, 2)], [1, 0]), 'e-dual-basis-pair: phi1(v1) = 1, phi1(v2) = 0', '')
pts2 = [{'x': 0.3, 'y': 1.7}, {'x': 2.9, 'y': 0.4}, {'x': 1.1, 'y': 2.3}]
expr_check('e-dual-basis-pair', lambda x, y: phi1(x, y), pts2, part=0, wrong_ids=['col', 'self'])
Tfun = lambda x, y: (x + y, 2 * x - y)  # noqa: E731
expr_check('e-dual-basis-pair', lambda x, y: phi1(*Tfun(x, y)), pts2, part=1, wrong_ids=['unapplied', 'transpose'])
ex._rec(abs(np.array([2, 1]) @ np.array([2, 1]) - 5) < 1e-12, 'e-dual-basis-pair: (2, 1) . (2, 1) = 5', '')

# e-weighted-adjoint: <Tx, y> = <x, Ty> at random vectors, for each option
Wt = np.diag([3.0, 1.0])
opts = {'ok': [[1, 1], [3, 2]], 'sym': [[1, 3], [3, 2]], 'tw': [[1, 3], [1, 2]], 'real': [[2, 1], [0, 5]]}
adj = {}
for k, T_ in opts.items():
    T_ = np.array(T_, dtype=float)
    xs_ = rng.normal(size=(50, 2))
    ys_ = rng.normal(size=(50, 2))
    adj[k] = bool(np.allclose([(T_ @ x) @ Wt @ y for x, y in zip(xs_, ys_)], [x @ Wt @ (T_ @ y) for x, y in zip(xs_, ys_)]))
ex._rec(adj == {'ok': True, 'sym': False, 'tw': False, 'real': False}, f'e-weighted-adjoint: self-adjoint {adj}', '')
ex._rec(np.allclose(sorted(np.linalg.eigvals(np.array(opts['real'], dtype=float)).real), [2, 5]), 'e-weighted-adjoint: eigenvalues 2 and 5', '')
ex._rec(np.allclose(Wt @ np.array(opts['ok']), [[3, 3], [3, 2]]), 'e-weighted-adjoint: WT = [[3, 3], [3, 2]]', '')
correct_id('e-weighted-adjoint', 'ok')


# e-jordan-from-kernels: build each option's matrix from blocks and compute kernel dimensions
def jordan(sizes, lam=-1.0):
    n = sum(sizes)
    J = lam * np.eye(n)
    at = 0
    for s in sizes:
        for i in range(s - 1):
            J[at + i, at + i + 1] = 1
        at += s
    return J


def kdims(J, lam=-1.0):
    N = J - lam * np.eye(len(J))
    return [len(J) - np.linalg.matrix_rank(np.linalg.matrix_power(N, k)) for k in (1, 2, 3, 4)]


given = [int(x) for x in re.findall(r'are (\d), (\d), (\d) and (\d)', node(P('e-jordan-from-kernels'))['prose'])[0]]
dims = {k: kdims(jordan(s)) for k, s in {'ok': [3, 2], 'diffs': [2, 2, 1], 'one': [5], 'four': [4, 1]}.items()}
ex._rec(dims['ok'] == given and all(dims[k] != given for k in dims if k != 'ok'), f'e-jordan-from-kernels: dims {dims}, given {given}', '')
correct_id('e-jordan-from-kernels', 'ok')

# ================================================================== difficulty 4
# e-uniform-peak: the sup by a fine grid, the smallest n by exact comparison
def sup_fn(n):
    """Ternary search for the maximum of x / (1 + n x^2) on [0, 10]: the function rises then falls."""
    f = lambda x: x / (1 + n * x * x)  # noqa: E731
    lo, hi = 0.0, 10.0
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        lo, hi = (m1, hi) if f(m1) < f(m2) else (lo, m2)
    return f((lo + hi) / 2)


expr_check('e-uniform-peak', sup_fn, [{'n': v} for v in (0.3, 1.0, 2.2, 3.0)], part=0, wrong_ids=['one', 'no-half'])
ex._rec(all(abs(sup_fn(n) - 1 / (2 * math.sqrt(n))) < 1e-9 for n in (1, 7, 50, 2500)), 'e-uniform-peak: grid sup = 1/(2 sqrt n)', '')
n_u = next(n for n in range(1, 10 ** 5) if 1 < F(1, 100) ** 2 * 4 * n)       # 1/(2 sqrt n) < 1/100  <=>  4n/10^4 > 1
key('e-uniform-peak', n_u, part=1, tol=0)
wrong('e-uniform-peak', 'at-bound', n_u - 1, part=1)
wrong('e-uniform-peak', 'no-square', next(n for n in range(1, 10 ** 5) if n > 50), part=1)
ex._rec(abs(sup_fn(2500) - 0.01) < 1e-9, 'e-uniform-peak: sup exactly 0.01 at n = 2500', '')
allow('e-uniform-peak', 0.01, 50, 2500, 2501)
say('e-uniform-peak', 'explain.text', 2501)

# e-compact-bounded, e-idempotent-split, e-contraction-proof: order answers
for iid in ('e-compact-bounded', 'e-idempotent-split', 'e-contraction-proof'):
    w = node(W(iid))
    ids = [l_['id'] for l_ in w['lines']]
    ex._rec(w['answer'] == [i for i in ids if i not in w['distractors']] and len(w['distractors']) == 2
            and all(l_.get('why') for l_ in w['lines'] if l_['id'] in w['distractors']),
            f'{iid}: answer is every non-distractor line in order, two distractors with a why', '')

# e-idempotent-split: a projection that is neither 0 nor I, and the nilpotent counter-example
Pj = np.array([[1.0, 1.0], [0.0, 0.0]])
ex._rec(np.allclose(Pj @ Pj, Pj) and not np.allclose(Pj, 0) and not np.allclose(Pj, np.eye(2)), 'e-idempotent-split: a projection that is neither 0 nor I', '')
Nn = np.array([[0.0, 1.0], [0.0, 0.0]])               # N(x, y) = (y, 0)
ex._rec(np.allclose(Nn @ np.array([1, 0]), 0) and np.allclose(Nn @ np.array([0, 1]), [1, 0]), 'e-idempotent-split: N has kernel and image span(e1)', '')

# e-hedge-residual: vectors with the stated Gram matrix by Cholesky, then project and measure
G = np.array([[0.0010, 0.0004], [0.0004, 0.0005]])
Lc = np.linalg.cholesky(G)
Rv, Mv = Lc[0], Lc[1]
bt = (Rv @ Mv) / (Mv @ Mv)
resid = Rv - bt * Mv
key('e-hedge-residual', bt, part=0)
wrong('e-hedge-residual', 'reverse', (Rv @ Mv) / (Rv @ Rv), part=0)
wrong('e-hedge-residual', 'corr', (Rv @ Mv) / (np.linalg.norm(Rv) * np.linalg.norm(Mv)), part=0)
ex._rec(abs(resid @ Mv) < 1e-15, 'e-hedge-residual: residual orthogonal to M', '')
key('e-hedge-residual', float(np.linalg.norm(resid)), part=1)
wrong('e-hedge-residual', 'sub-cov', math.sqrt(Rv @ Rv - Rv @ Mv), part=1)
wrong('e-hedge-residual', 'sub-sd', float(np.linalg.norm(Rv) - bt * np.linalg.norm(Mv)), part=1)
allow('e-hedge-residual', 0.0010, 0.0005, 0.0004, bt, float(resid @ resid), 100 * float(np.linalg.norm(resid)),
      100 * math.sqrt(Rv @ Rv - Rv @ Mv), 100 * float(np.linalg.norm(Rv) - bt * np.linalg.norm(Mv)))
say('e-hedge-residual', 'explain.text', 2.61, fmt='2.61%')
say('e-hedge-residual', 'explain.text', 0.00068)

# e-symmetric-power: integer matrix power and numpy eigenvalues
As = np.array([[7, 2], [2, 4]], dtype=np.int64)
ev = sorted(np.linalg.eigvalsh(As.astype(float)))
key('e-symmetric-power', ev[-1], part=0, tol=1e-9)
wrong('e-symmetric-power', 'trace', float(np.trace(As)), part=0)
wrong('e-symmetric-power', 'entry', float(As.max()), part=0)
A6 = np.linalg.matrix_power(As, 6)
key('e-symmetric-power', float(A6[0, 1]), part=1, tol=0)
wrong('e-symmetric-power', 'no-small', 0.4 * ev[-1] ** 6, part=1)
wrong('e-symmetric-power', 'entrywise', float(As[0, 1] ** 6), part=1)
wrong('e-symmetric-power', 'plus', 0.4 * (ev[-1] ** 6 + ev[0] ** 6), part=1)
q1 = np.array([2, 1]) / math.sqrt(5)
ex._rec(np.allclose(As @ (q1 * math.sqrt(5)), [16, 8]), 'e-symmetric-power: A(2, 1) = (16, 8)', '')
ex._rec(round(ev[-1] ** 6) == 262144 and round(ev[0] ** 6) == 729 and 262144 - 729 == 261415, 'e-symmetric-power: 262,144 - 729 = 261,415', '')
allow('e-symmetric-power', 16, 11, 104566, 261415, 262144, 729, 0.4 * ev[-1] ** 6, 64, 0.4 * (ev[-1] ** 6 + ev[0] ** 6))
say('e-symmetric-power', 'explain.text', 104566)

# e-chain-response: powers of J directly
J = np.array([[0.85, 1.0], [0.0, 0.85]])
xt = [np.linalg.matrix_power(J, t) @ np.array([0.0, 1.0]) for t in range(0, 80)]
first = [v[0] for v in xt]
tp = int(np.argmax(first))
ex._rec(all(abs(np.linalg.matrix_power(J, t)[0, 1] - t * 0.85 ** (t - 1)) < 1e-12 for t in range(1, 40)), 'e-chain-response: top-right of J^t = t 0.85^(t-1)', '')
correct_id('e-chain-response', 'ok', part=0)
key('e-chain-response', first[tp], part=1)
ex._rec(tp == 6, f'e-chain-response: peak at t = {tp}', '')
wrong('e-chain-response', 'tpow', max(t * 0.85 ** t for t in range(1, 80)), part=1)
wrong('e-chain-response', 'decay', first[1], part=1)
cross = bisect(lambda t: 0.85 * (t + 1) / t - 1, 1, 50)
ex._rec(abs(cross - 17 / 3) < 1e-9, f'e-chain-response: ratio above 1 exactly for t < {cross:.4f}', '')
allow('e-chain-response', 0.85, cross, first[tp], 1, max(t * 0.85 ** t for t in range(1, 80)))
say('e-chain-response', 'explain.text', 2.662)
say('e-chain-response', 'explain.text', 5.67)

# ================================================================== difficulty 5
# e-three-one-rearrange: sum the rearranged series term by term
mblk = 400000
odd = 1.0 / (2 * np.arange(1, 3 * mblk + 1) - 1)
even = 1.0 / (2 * np.arange(1, mblk + 1))
blocks = odd.reshape(mblk, 3).sum(axis=1) - even
S_m = math.fsum(blocks)
ex._rec(abs(S_m - (math.log(2) + 0.5 * math.log(3))) < 5e-6, f'e-three-one-rearrange: {mblk} blocks sum to {S_m:.7f}', '')
key('e-three-one-rearrange', S_m, part=1, tol=1e-5)
wrong('e-three-one-rearrange', 'same', math.fsum(((-1) ** (k + 1)) / k for k in range(1, 2 * 10 ** 6 + 1)), part=1)
two_one = math.fsum((1 / (4 * j - 3) + 1 / (4 * j - 1) - 1 / (2 * j)) for j in range(1, 10 ** 6 + 1))
wrong('e-three-one-rearrange', 'two-one', two_one, part=1)
H = lambda n: math.fsum(1 / k for k in range(1, n + 1))  # noqa: E731
for mm in (1, 2, 5, 40):
    ex._rec(abs(math.fsum(1 / (2 * j - 1) for j in range(1, 3 * mm + 1)) - (H(6 * mm) - H(3 * mm) / 2)) < 1e-12,
            f'e-three-one-rearrange: odd sum = H_6m - H_3m/2 at m = {mm}', '')
correct_id('e-three-one-rearrange', 'ok', part=0)
_w = node(W('e-three-one-rearrange', 1))
ex._rec(all(abs(v_ - _w['answer']) <= _w['tol']['abs'] for v_ in (1.2424, 1.2425)) and abs(1.2426 - _w['answer']) > _w['tol']['abs']
        and abs(round(math.log(2), 4) + round(0.5 * math.log(3), 4) - _w['answer']) <= _w['tol']['abs'],
        'e-three-one-rearrange: 4-place intermediate logs (1.2424) and 1.2425 are inside the band, 1.2426 is not', '')
allow('e-three-one-rearrange', S_m, 11, 1, two_one)
say('e-three-one-rearrange', 'explain.text', 1.2425)

# e-contraction-proof: the counter-example iterates are not monotone; a contraction's iterates are Cauchy
it_ = [0.0]
for _ in range(10):
    it_.append(1 - it_[-1] / 2)
ex._rec(any(b_ > a_ for a_, b_ in zip(it_, it_[1:])) and any(b_ < a_ for a_, b_ in zip(it_, it_[1:])) and abs(it_[-1] - 2 / 3) < 1e-3,
        'e-contraction-proof: 1 - x/2 iterates jump from side to side and tend to 2/3', '')

# e-rayleigh-proof: random symmetric matrices, then part (b)
for _ in range(5):
    Z = rng.normal(size=(4, 4))
    Sy = Z + Z.T
    xs_ = rng.normal(size=(20000, 4))
    xs_ /= np.linalg.norm(xs_, axis=1, keepdims=True)
    q = np.einsum('ij,jk,ik->i', xs_, Sy, xs_)
    lam_max = np.linalg.eigvalsh(Sy)[-1]
    ex._rec(q.max() <= lam_max + 1e-12 and lam_max - q.max() < 0.2, 'e-rayleigh-proof: unit quadratic forms stay at or below the top eigenvalue', '')
Sig_ev = [0.04, 0.01, 0.005]
say('e-rayleigh-proof', 'model', max(Sig_ev))
say('e-rayleigh-proof', 'model', round(100 * math.sqrt(max(Sig_ev))), fmt='20%')
ex._rec(sum(r_['points'] for r_ in node(P('e-rayleigh-proof'))['rubric']) == 10, 'e-rayleigh-proof: rubric sums to 10', '')
allow('e-rayleigh-proof', *Sig_ev, 20)


# ------------------------------------------------------------------ every level has an item on a skill first met there
LEVEL = {   # item -> (course, level of the lesson it is pitched at)
    'e-sup-rising': ('analysis', 1), 'e-diagonal-digits': ('analysis', 1), 'e-rational-between': ('analysis', 1),
    'e-n-for-quotient': ('analysis', 2), 'e-root-recursion': ('analysis', 2), 'e-contraction-proof': ('analysis', 2),
    'e-telescope-gap-three': ('analysis', 3), 'e-which-converge': ('analysis', 3), 'e-three-one-rearrange': ('analysis', 3),
    'e-halvings-width': ('analysis', 4), 'e-cube-delta': ('analysis', 4), 'e-mvt-quartic': ('analysis', 4),
    'e-uniform-peak': ('analysis', 4),
    'e-upper-sum-square': ('analysis', 5), 'e-ftc-both-limits': ('analysis', 5), 'e-gram-schmidt-step': ('linear-maps', 3),
    'e-closed-sets': ('analysis', 5), 'e-compact-bounded': ('analysis', 5),
    'e-subspace-r3': ('linear-maps', 1), 'e-coords-new-basis': ('linear-maps', 1),
    'e-antisym-map': ('linear-maps', 2), 'e-matrix-of-map': ('linear-maps', 2), 'e-idempotent-split': ('linear-maps', 2),
    'e-dual-basis-pair': ('linear-maps', 3), 'e-hedge-residual': ('linear-maps', 3),
    'e-weighted-adjoint': ('linear-maps', 4), 'e-jordan-from-kernels': ('linear-maps', 4),
    'e-symmetric-power': ('linear-maps', 4), 'e-chain-response': ('linear-maps', 4), 'e-rayleigh-proof': ('linear-maps', 4),
}
ex._rec(sorted(LEVEL) == sorted(idx), 'every item has a level', '')
CDIR = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
for course in ('analysis', 'linear-maps'):
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
        hits = [i for i, (c, n) in LEVEL.items() if c == course and n == lv['n'] and set(node(P(i))['skills']) & new]
        auto = [i for i in hits if node(P(i)).get('kind') != 'longform']
        ex._rec(bool(auto), f'{course} L{lv["n"]}: new skills {sorted(new)} tested by auto items {auto}', '')
print('items per level:', dict(sorted(Counter(LEVEL.values()).items())))


# ------------------------------------------------------------------ every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t else 0), t


for it in items:
    iid = it['id']
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings(it):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    ex._rec(not bad, f'{iid}: every stated number matches route B', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
