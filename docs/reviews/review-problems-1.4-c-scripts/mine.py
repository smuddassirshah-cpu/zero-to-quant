"""Second read, eigen problems-1 to -3: the reader's own keys, slips and stated numbers.

Imports nothing from the author's script. Every matrix and vector is typed here from the prose. Route 1 is exact (sympy or
fractions), route 2 is NumPy or a direct iteration. Each key and each `wrong` value is then compared with the content file.
CLAIM lines are statements the reader holds to be false or loose (findings, not failures).

Run from the repo root:  <scratchpad>/venv/bin/python docs/reviews/review-problems-1.4-c-scripts/mine.py
"""
import json
import math
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

checks = fails = 0
SETS = {n: json.load(open(f'app/content/courses/eigen/problems-{n}.json')) for n in (1, 2, 3)}


def part(n, item, k):
    it = next(i for i in SETS[n]['items'] if i['id'] == item)
    return it['parts'][k - 1]


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def near(a, b, tol=1e-9):
    return abs(float(np.asarray(a, float).reshape(-1)[0]) - float(b)) <= tol


def vec(tex):
    """'(\\frac{3}{5}, 2/5)' -> list of Fractions or floats"""
    t = tex.strip().strip('()[]')
    t = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'\1/\2', t)
    return [sp.nsimplify(x.strip()) for x in t.split(',')]


def key(n, item, k, mine, tol=None):
    """the stored key equals mine; for numeric parts mine also sits inside the stored band"""
    w = part(n, item, k)['widget']
    where = f'{n} {item} {k}'
    if w['kind'] == 'numeric' and 'answers' in w:
        ok(sorted(map(float, w['answers'])) == sorted(map(float, mine)), f'{where}: answers {w["answers"]} vs mine {mine}')
    elif w['kind'] == 'numeric':
        band = w['tol'].get('abs', 0)
        ok(abs(float(w['answer']) - float(mine)) <= band + 1e-12, f'{where}: key {w["answer"]} vs mine {float(mine)} (band {band})')
        if tol is not None:
            ok(abs(round(float(mine), tol) - float(w['answer'])) < 1e-12, f'{where}: mine rounded to {tol} places is the key')
    elif w['kind'] == 'expression':
        if isinstance(mine, (list, tuple)):
            ok([sp.nsimplify(x) for x in mine] == vec(w['answer']), f'{where}: key {w["answer"]} vs mine {mine}')
            for a in w.get('accept', []):
                if re.match(r'^[(\[]', a):
                    ok(vec(a) == [sp.nsimplify(x) for x in mine], f'{where}: accept {a} equals the key')
        else:
            r = sp.Symbol('r')
            ok(sp.simplify(sp.sympify(w['answer'].replace('^', '**').replace('r**2', '*r**2').replace('-*', '-').replace('1.28r', '1.28*r'), {'r': r}) - mine) == 0, f'{where}: key {w["answer"]}')


def wrong(n, item, k, wid, mine):
    """the stored slip value equals what the named slip gives"""
    w = part(n, item, k)['widget']
    x = next((x for x in w.get('wrong', []) if x['id'] == wid), None)
    where = f'{n} {item} {k} wrong {wid}'
    if x is None:
        ok(False, f'{where}: no such entry')
        return
    ok(wid in (part(n, item, k)['feedback'].get('byKey') or {}), f'{where}: has a line')
    if 'tex' in x:
        ok(vec(x['tex']) == [sp.nsimplify(v) for v in mine], f'{where}: {x["tex"]} vs mine {mine}')
    elif isinstance(x['value'], str):
        ok(sorted(float(v) for v in x['value'].split(',')) == sorted(map(float, mine)), f'{where}: {x["value"]} vs mine {mine}')
    else:
        band = x.get('tol', {}).get('abs', 0)
        ok(abs(float(x['value']) - float(mine)) <= band + 1e-12, f'{where}: {x["value"]} vs mine {float(mine)} (band {band})')
        a = w.get('answer')
        if a is not None:
            ok(abs(float(x['value']) - float(a)) > band + w['tol'].get('abs', 0), f'{where}: band clear of the key band')


def all_wrongs_seen(seen):
    for n, d in SETS.items():
        for it in d['items']:
            for k, p in enumerate(it['parts'], 1):
                for x in p['widget'].get('wrong', []):
                    ok((n, it['id'], k, x['id']) in seen, f'{n} {it["id"]} {k}: wrong {x["id"]} not rebuilt by the reader')


SEEN = set()
_wrong = wrong


def wrong(n, item, k, wid, mine):  # noqa: F811
    SEEN.add((n, item, k, wid))
    _wrong(n, item, k, wid, mine)


M = sp.Matrix
# ---------------------------------------------------------------- problems-1
# p-sketch-warp: A = [[4, b], [1, -1]], v = (3, 1)
b = sp.Symbol('b')
A = M([[4, b], [1, -1]]); v = M([3, 1])
lam = (A * v)[1] / v[1]
key(1, 'p-sketch-warp', 1, lam)
wrong(1, 'p-sketch-warp', 1, 'sign', 1 * 3 + 1 * 1)
bsol = sp.solve(sp.Eq((A * v)[0], lam * v[0]), b)[0]
key(1, 'p-sketch-warp', 2, bsol)
wrong(1, 'p-sketch-warp', 2, 'dropped-sign', -bsol)
wrong(1, 'p-sketch-warp', 2, 'wrong-entry', sp.solve(sp.Eq(12 + b, lam * v[1]), b)[0])
wrong(1, 'p-sketch-warp', 2, 'carried', sp.solve(sp.Eq(12 + b, 4 * 3), b)[0])
A = A.subs(b, bsol)
ev = sorted(A.eigenvals().keys())
ok(ev == [1, 2], 'warp: eigenvalues 1 and 2')
ok(sorted(np.linalg.eigvals(np.array(A.tolist(), float)).round(9)) == [1, 2], 'warp: NumPy agrees')
key(1, 'p-sketch-warp', 3, A.trace() - 2)
wrong(1, 'p-sketch-warp', 3, 'added', A.trace() + 2)
wrong(1, 'p-sketch-warp', 3, 'trace-sign', (4 + 1) - 2)
wrong(1, 'p-sketch-warp', 3, 'det-sign', sp.Rational(4 * (-1) - 6 * 1, 2))
ok(A.det() == 2, 'warp: det 2')
ns = (A - sp.eye(2)).nullspace()[0]; e1 = ns / ns[1]
key(1, 'p-sketch-warp', 4, list(e1))
wrong(1, 'p-sketch-warp', 4, 'other', [3, 1]); wrong(1, 'p-sketch-warp', 4, 'sign', [-2, 1]); wrong(1, 'p-sketch-warp', 4, 'swapped', [1, 2])
ok(A * M([2, 1]) == M([2, 1]), 'warp: A(2,1) = (2,1)')
w = M([5, 2])
key(1, 'p-sketch-warp', 5, list(A**4 * w))
ok(np.allclose(np.linalg.matrix_power(np.array(A.tolist(), float), 4) @ [5, 2], [50, 17]), 'warp: NumPy A^4 w')
wrong(1, 'p-sketch-warp', 5, 'one-warp', list(A * w))
wrong(1, 'p-sketch-warp', 5, 'times-four', list(8 * M([3, 1]) + 4 * M([2, 1])))
c = M([[3, -2], [1, 1]]).LUsolve(w)
wrong(1, 'p-sketch-warp', 5, 'carried', list(c[0] * 16 * M([3, 1]) + c[1] * M([-2, 1])))
ok(A * M([-2, 1]) == M([-14, -3]), 'warp: A(-2,1) = (-14,-3) as the carried line says')

# p-garden-path: t_{n+1} = t_n + 6 t_{n-1}, t_0 = t_1 = 1
t = [1, 1]
for _ in range(12):
    t.append(t[-1] + 6 * t[-2])
# brute force: count pavings of a 1 by n strip with squares (1 kind) and 1 by 2 slabs (6 colours)


def pave(n):
    return 1 if n <= 0 and n == 0 else 0 if n < 0 else pave(n - 1) + 6 * pave(n - 2)


ok([pave(n) for n in range(8)] == t[:8], 'path: the recurrence counts the pavings')
G = M([[1, 6], [1, 0]])
ok(sorted(G.eigenvals().keys()) == [-2, 3], 'path: eigenvalues')
key(1, 'p-garden-path', 1, [3, -2])
wrong(1, 'p-garden-path', 1, 'sign', sp.solve(sp.Symbol('x')**2 + sp.Symbol('x') - 6))
wrong(1, 'p-garden-path', 1, 'dropped-sign', [3, 2]); wrong(1, 'p-garden-path', 1, 'diagonal', [G[0, 0], G[1, 1]])
ns = (G - 3 * sp.eye(2)).nullspace()[0]
key(1, 'p-garden-path', 2, list(ns / ns[1]))
ns2 = (G + 2 * sp.eye(2)).nullspace()[0]
wrong(1, 'p-garden-path', 2, 'other', list(ns2 / ns2[1])); wrong(1, 'p-garden-path', 2, 'sign', [-3, 1])
cc = M([[3, -2], [1, 1]]).LUsolve(M([1, 1]))
key(1, 'p-garden-path', 3, list(cc))
wrong(1, 'p-garden-path', 3, 'swapped', [cc[1], cc[0]]); wrong(1, 'p-garden-path', 3, 'not-split', [1, 1])
wrong(1, 'p-garden-path', 3, 'carried', list(M([[-3, -2], [1, 1]]).LUsolve(M([1, 1]))))
ok(cc[1] * M([3, 1]) + cc[0] * M([-2, 1]) == M([0, 1]), 'path: the swapped line, (0, 1)')
closed = lambda n: cc[0] * 3**n + cc[1] * (-2)**n
ok(all(closed(n) == t[n] for n in range(13)), 'path: closed form equals the recurrence')
key(1, 'p-garden-path', 4, t[10])
ok((G**10 * M([1, 1]))[1] == 35839, 'path: A^10 u0')
wrong(1, 'p-garden-path', 4, 'sign', cc[0] * 3**10 - cc[1] * 2**10)
wrong(1, 'p-garden-path', 4, 'first-entry', t[11]); wrong(1, 'p-garden-path', 4, 'one-short', t[9])
wrong(1, 'p-garden-path', 4, 'swapped', cc[1] * 3**10 + cc[0] * 2**10)
ok(cc[0] * 3**10 == sp.Rational(354294, 10) and cc[1] * 2**10 == sp.Rational(4096, 10) and t[2] == 7, 'path: 35429.4, 409.6, t_2 = 7')

# p-hill-bikes
p = sp.Symbol('p')
psol = sp.solve(sp.Eq(200 * p, sp.Rational(15, 100) * 400), p)[0]
key(1, 'p-hill-bikes', 1, psol)
wrong(1, 'p-hill-bikes', 1, 'swapped', sp.solve(sp.Eq(400 * p, sp.Rational(15, 100) * 200), p)[0])
wrong(1, 'p-hill-bikes', 1, 'total', sp.solve(sp.Eq(200 * p, sp.Rational(15, 100) * 600), p)[0])
H = M([[sp.Rational(7, 10), sp.Rational(15, 100)], [sp.Rational(3, 10), sp.Rational(85, 100)]])
ok(H * M([200, 400]) == M([200, 400]), 'bikes: (200, 400) is steady')
lam2 = H.trace() - 1
key(1, 'p-hill-bikes', 2, lam2)
ok(H.det() == lam2 and H * M([1, -1]) == lam2 * M([1, -1]), 'bikes: det 0.55, (1,-1) eigenvector')
wrong(1, 'p-hill-bikes', 2, 'trace', H.trace())
wrong(1, 'p-hill-bikes', 2, 'det-sign', sp.Rational(595, 1000) + sp.Rational(45, 1000))
wrong(1, 'p-hill-bikes', 2, 'carried', (1 - sp.Rational(75, 1000)) + sp.Rational(85, 100) - 1)
s2 = H**2 * M([600, 0])
key(1, 'p-hill-bikes', 3, s2[0])
ok(H * M([600, 0]) == M([420, 180]), 'bikes: night 1 (420, 180)')
wrong(1, 'p-hill-bikes', 3, 'one-night', 420); wrong(1, 'p-hill-bikes', 3, 'no-steady', 600 * lam2**2)
wrong(1, 'p-hill-bikes', 3, 'river', s2[1]); wrong(1, 'p-hill-bikes', 3, 'carried', 200 + 400 * sp.Rational(775, 1000)**2)
x = np.array([600.0, 0.0]); Hn = np.array(H.tolist(), float); first = None
for k in range(1, 12):
    x = Hn @ x
    if first is None and x[0] < 230:
        first = k
key(1, 'p-hill-bikes', 4, first)
ok(near(200 + 400 * 0.55**4, 236.6, 0.05) and near(400 * 0.55**5, 20.1, 0.05) and near(math.log(0.075) / math.log(0.55), 4.33, 0.005), 'bikes: 236.6, 20.1, 4.33')
ok(near(0.55**4, 0.0915, 5e-5) and near(0.55**5, 0.0503, 5e-5) and near(400 * 0.0915, 36.6, 0.05), 'bikes: 0.0915, 0.0503, 36.6')
wrong(1, 'p-hill-bikes', 4, 'rounded-down', first - 1)
wrong(1, 'p-hill-bikes', 4, 'no-steady', next(k for k in range(1, 20) if 600 * 0.55**k < 30))

# p-lazy-frog
h = sp.Rational(1, 2)
F = M([[0, h, 0], [1, 0, 1], [0, h, 0]])
ns = (F - sp.eye(3)).nullspace(); ok(len(ns) == 1, 'frog: one steady direction')
s = ns[0] / sum(ns[0])
key(1, 'p-lazy-frog', 1, list(s))
wrong(1, 'p-lazy-frog', 1, 'unscaled', [1, 2, 1]); wrong(1, 'p-lazy-frog', 1, 'uniform', [sp.Rational(1, 3)] * 3)
ok(F * M([1, 1, 1]) / 3 == M([sp.Rational(1, 6), sp.Rational(2, 3), sp.Rational(1, 6)]), 'frog: even split sends 2/3 to pad 2')
ok(F * M([1, -2, 1]) == -M([1, -2, 1]) and F * M([1, 0, -1]) == sp.zeros(3, 1), 'frog: eigenvalues -1 and 0')
ok(sorted(F.eigenvals().keys()) == [-1, 0, 1], 'frog: eigenvalues of M')
key(1, 'p-lazy-frog', 2, -1)
wrong(1, 'p-lazy-frog', 2, 'dropped-sign', 1); wrong(1, 'p-lazy-frog', 2, 'middle-entry', -2)
e = M([1, 0, 0])
ok(e == s + h * M([1, 0, -1]) + sp.Rational(1, 4) * M([1, -2, 1]), 'frog: the split of (1, 0, 0)')
ok(all((F**k * e)[1] == (1 if k % 2 else 0) for k in range(1, 9)), 'frog: on pad 2 after every odd minute, never after an even one')
L = h * (sp.eye(3) + F)
ok(L * M([1, -2, 1]) == sp.zeros(3, 1) and L * M([1, 0, -1]) == h * M([1, 0, -1]), 'frog: lazy eigenvalues 0 and 0.5')
key(1, 'p-lazy-frog', 4, [0, h])
wrong(1, 'p-lazy-frog', 4, 'kept-m', [-1, 0]); wrong(1, 'p-lazy-frog', 4, 'no-half', [0, 1]); wrong(1, 'p-lazy-frog', 4, 'halved-only', [-h, 0])
key(1, 'p-lazy-frog', 5, (L**3 * e)[0])
ok(near(np.linalg.matrix_power(np.array(L.tolist(), float), 3)[0, 0], 0.3125), 'frog: NumPy L^3')
wrong(1, 'p-lazy-frog', 5, 'half-dropped', s[0] + h**3); ok(s[0] + h * h**2 == sp.Rational(3, 8), 'frog: 0.5 squared also gives 0.375')
wrong(1, 'p-lazy-frog', 5, 'steady-only', s[0]); wrong(1, 'p-lazy-frog', 5, 'not-lazy', (F**3 * e)[0])
wrong(1, 'p-lazy-frog', 5, 'carried', s[0] + h * 1**3)
ch = next(o for o in part(1, 'p-lazy-frog', 3)['widget']['options'] if o.get('correct'))
ok(ch['id'] == 'flips', 'frog: the chain does not settle')

# ---------------------------------------------------------------- problems-2
# p-oval-pond: 5x^2 + 4xy + 8y^2 = 36
x, y = sp.symbols('x y')
P = M([[5, 2], [2, 8]])
ok(sp.expand((M([[x, y]]) * P * M([x, y]))[0]) == 5 * x**2 + 4 * x * y + 8 * y**2, 'pond: the form')
key(2, 'p-oval-pond', 1, P[0, 1]); wrong(2, 'p-oval-pond', 1, 'whole-cross', 4)
ok(sorted(P.eigenvals().keys()) == [4, 9] and P.trace() == 13 and P.det() == 36, 'pond: eigenvalues, trace, det')
key(2, 'p-oval-pond', 2, [4, 9]); wrong(2, 'p-oval-pond', 2, 'diagonal', [5, 8]); wrong(2, 'p-oval-pond', 2, 'sign', [-4, -9])
ns = (P - 4 * sp.eye(2)).nullspace()[0]
key(2, 'p-oval-pond', 3, list(2 * ns / ns[0]))
n9 = (P - 9 * sp.eye(2)).nullspace()[0]
wrong(2, 'p-oval-pond', 3, 'big', list(2 * n9 / n9[0])); wrong(2, 'p-oval-pond', 3, 'sign', [2, 1])
tt = sp.Symbol('t', positive=True)
q = M([2, -1]) / sp.sqrt(5)
half = sp.solve(sp.Eq((q.T * P * q)[0] * tt**2, 36), tt)[0]
key(2, 'p-oval-pond', 4, half)
ok(near(max(np.linalg.norm(np.linalg.solve(np.linalg.cholesky(np.array(P.tolist(), float) / 36).T, [math.cos(a), math.sin(a)])) for a in np.linspace(0, math.pi, 200001)), 3, 1e-6), 'pond: the farthest edge point is 3 m away (scan of the curve)')
wrong(2, 'p-oval-pond', 4, 'short', sp.sqrt(sp.Rational(36, 9))); wrong(2, 'p-oval-pond', 4, 'no-root', sp.Rational(36, 4)); wrong(2, 'p-oval-pond', 4, 'full-axis', 2 * half)
key(2, 'p-oval-pond', 5, math.pi * 3 * 2, 2)
ok(near(36 * math.pi / math.sqrt(36), 6 * math.pi), 'pond: 36 pi / sqrt(det)')
wrong(2, 'p-oval-pond', 5, 'no-root', math.pi * 9 * 4); wrong(2, 'p-oval-pond', 5, 'full-axes', math.pi * 6 * 4); wrong(2, 'p-oval-pond', 5, 'one-axis', math.pi * 9)

# p-river-gauges
r = sp.Symbol('r')
C = M([[1, sp.Rational(8, 10), r], [sp.Rational(8, 10), 1, sp.Rational(8, 10)], [r, sp.Rational(8, 10), 1]])
key(2, 'p-river-gauges', 1, C[:2, :2].det())
wrong(2, 'p-river-gauges', 1, 'plus', 1 + sp.Rational(64, 100)); wrong(2, 'p-river-gauges', 1, 'no-square', 1 - sp.Rational(8, 10))
detC = sp.expand(C.det())
key(2, 'p-river-gauges', 2, detC)
ok(detC == -r**2 + sp.Rational(128, 100) * r - sp.Rational(28, 100), 'gauges: det C')
poly = lambda tex: sp.sympify(re.sub(r'(\d)r', r'\1*r', tex).replace('^', '**'), {'r': r})
for wid, mine_ in (('cross-sign', 1 * sp.Rational(36, 100) - sp.Rational(8, 10) * (sp.Rational(8, 10) + sp.Rational(8, 10) * r) + r * (-sp.Rational(64, 100) - r)),
                   ('no-square', sp.Rational(36, 100) - sp.Rational(64, 100) + sp.Rational(64, 100) * r + sp.Rational(64, 100) * r)):
    xw = next(v for v in part(2, 'p-river-gauges', 2)['widget']['wrong'] if v['id'] == wid)
    SEEN.add((2, 'p-river-gauges', 2, wid))
    ok(sp.expand(sp.nsimplify(poly(xw['tex']), rational=True) - mine_) == 0, f'gauges 2 wrong {wid}: {xw["tex"]} vs mine {sp.expand(mine_)}')
    ok(wid in part(2, 'p-river-gauges', 2)['feedback']['byKey'], f'gauges 2 wrong {wid}: has a line')
for a in part(2, 'p-river-gauges', 2)['widget']['accept']:
    ok(sp.expand(sp.nsimplify(poly(re.sub(r'\)\(', ')*(', a)), rational=True) - detC) == 0, f'gauges 2: accept {a} equals the key')
roots = sorted(sp.solve(detC, r))
ok(roots == [sp.Rational(28, 100), 1], 'gauges: roots 0.28 and 1')
key(2, 'p-river-gauges', 3, roots[0])
for rv in (0.27, 0.29, 0.99):
    ok((np.linalg.eigvalsh(np.array(C.subs(r, rv).tolist(), float)).min() > 0) == (0.28 < rv < 1), f'gauges: definiteness at r = {rv} by NumPy')
ok(np.linalg.eigvalsh(np.array(C.subs(r, 1.01).tolist(), float)).min() < 0, 'gauges: not definite above r = 1')
wrong(2, 'p-river-gauges', 3, 'other-root', roots[1])
wrong(2, 'p-river-gauges', 3, 'carried', max(sp.solve(-r**2 - sp.Rational(128, 100) * r - sp.Rational(28, 100), r)))
ok(sp.sqrt(sp.Rational(16384, 10000) - sp.Rational(112, 100)) == sp.Rational(72, 100), 'gauges: root of the discriminant 0.72')
C0 = C.subs(r, roots[0]); ns = C0.nullspace(); ok(len(ns) == 1, 'gauges: one null direction')
wv = ns[0] / ns[0][0]
ok(wv[2] == 1, 'gauges: the null vector has the form (1, a, 1)')
key(2, 'p-river-gauges', 4, wv[1])
wrong(2, 'p-river-gauges', 4, 'dropped-sign', -wv[1]); wrong(2, 'p-river-gauges', 4, 'no-r', sp.Rational(-10, 8))
C2 = C.subs(r, sp.Rational(2, 10))
var = (wv.T * C2 * wv)[0]
key(2, 'p-river-gauges', 5, var)
ok(sp.expand((wv.T * C * wv)[0]) == 2 * r - sp.Rational(56, 100), 'gauges: w^T C w = 2r - 0.56')
ok(near(np.array(wv.tolist(), float).T @ np.array(C2.tolist(), float) @ np.array(wv.tolist(), float), -0.16), 'gauges: NumPy variance')
wrong(2, 'p-river-gauges', 5, 'dropped-sign', -var); wrong(2, 'p-river-gauges', 5, 'bound', 0)
wrong(2, 'p-river-gauges', 5, 'no-double', sum(wv[i]**2 for i in range(3)) + sum(wv[i] * wv[j] * C2[i, j] for i in range(3) for j in range(i + 1, 3)))

# p-tank-thermometers
S = M([[3, 1, 1], [1, 3, 1], [1, 1, 3]])
ok(S * M([1, 1, 1]) == 5 * M([1, 1, 1]) and S * M([1, -1, 0]) == 2 * M([1, -1, 0]), 'tank: eigenvalues 5 and 2')
ok(S.eigenvals() == {5: 1, 2: 2}, 'tank: 5 once and 2 twice')
key(2, 'p-tank-thermometers', 1, 5); wrong(2, 'p-tank-thermometers', 1, 'diagonal', 3); wrong(2, 'p-tank-thermometers', 1, 'all-entries', 15)
key(2, 'p-tank-thermometers', 2, 2); wrong(2, 'p-tank-thermometers', 2, 'added', 3 + 1); wrong(2, 'p-tank-thermometers', 2, 'sign', -2)
key(2, 'p-tank-thermometers', 3, S.trace() - 5 - 2); wrong(2, 'p-tank-thermometers', 3, 'no-second', 9 - 5); wrong(2, 'p-tank-thermometers', 3, 'no-first', 9 - 2)
wa = M([1, 1, 1]) / 3
key(2, 'p-tank-thermometers', 4, (wa.T * S * wa)[0], 3)
wrong(2, 'p-tank-thermometers', 4, 'no-length', 5); wrong(2, 'p-tank-thermometers', 4, 'ninth', sp.Rational(5, 9))
wt = M([sp.Rational(5, 10), sp.Rational(3, 10), sp.Rational(2, 10)])
d = wt - wa
ok(list(d) == [sp.Rational(1, 6), sp.Rational(-1, 30), sp.Rational(-2, 15)] and d.dot(d) == sp.Rational(42, 900), 'tank: d and its squared length')
full = (wt.T * S * wt)[0]
key(2, 'p-tank-thermometers', 5, full, 2)
ok(full == sp.Rational(5, 3) + 2 * d.dot(d) == sp.Rational(176, 100), 'tank: 5/3 + 2|d|^2 = 1.76 exactly')
wrong(2, 'p-tank-thermometers', 5, 'no-eigenvalue', sp.Rational(5, 3) + d.dot(d)); wrong(2, 'p-tank-thermometers', 5, 'd-only', 2 * d.dot(d))
wrong(2, 'p-tank-thermometers', 5, 'no-cov', 3 * wt.dot(wt))
ok(3 * wt.dot(wt) == sp.Rational(114, 100) and 2 * (wt[0] * wt[1] + wt[0] * wt[2] + wt[1] * wt[2]) == sp.Rational(62, 100), 'tank: 1.14 and 0.62')

# ---------------------------------------------------------------- problems-3
# p-branch-sales
B = M([[4, 4], [3, 3], [2, -2]])
BtB = B.T * B
ok(BtB == M([[29, 21], [21, 29]]), 'sales: A^T A')
key(3, 'p-branch-sales', 1, BtB[0, 1]); wrong(3, 'p-branch-sales', 1, 'diagonal-or-sign', 16 + 9 + 4); wrong(3, 'p-branch-sales', 1, 'aat', (B * B.T)[0, 1])
key(3, 'p-branch-sales', 2, list(BtB.eigenvals().keys()))
wrong(3, 'p-branch-sales', 2, 'entries', [29, 21]); wrong(3, 'p-branch-sales', 2, 'carried', list(M([[29, 29], [29, 29]]).eigenvals().keys()))
U, sv, Vt = np.linalg.svd(np.array(B.tolist(), float), full_matrices=False)
ok(np.allclose(sv**2, [50, 8]), 'sales: NumPy singular values squared')
u1 = B * M([1, 1]) / (sp.sqrt(2) * sp.sqrt(50))
key(3, 'p-branch-sales', 3, list(u1))
ok(np.allclose(np.abs(U[:, 0]), [0.8, 0.6, 0]), 'sales: NumPy u1 up to sign')
wrong(3, 'p-branch-sales', 3, 'unscaled', list(B * M([1, 1]))); wrong(3, 'p-branch-sales', 3, 'no-root', list(B * M([1, 1]) / 50))
A1 = sp.sqrt(50) * u1 * (M([[1, 1]]) / sp.sqrt(2))
ok(np.allclose(np.array(A1.tolist(), float), sv[0] * np.outer(U[:, 0], Vt[0])), 'sales: A_1 by NumPy')
key(3, 'p-branch-sales', 4, list(A1[:, 0]))
wrong(3, 'p-branch-sales', 4, 'u-only', list(u1)); wrong(3, 'p-branch-sales', 4, 'carried', list(5 * B * M([1, 1])))
en = lambda X: sum(v**2 for v in X)
key(3, 'p-branch-sales', 5, sp.Rational(en(A1), en(B)), 3)
ok(en(A1) == 50 and en(B) == 58 and (B - A1).tolist() == [[0, 0], [0, 0], [2, -2]], 'sales: energies 50, 58 and the error rows')
wrong(3, 'p-branch-sales', 5, 'unsquared', math.sqrt(50) / (math.sqrt(50) + math.sqrt(8))); wrong(3, 'p-branch-sales', 5, 'error-share', 8 / 58); wrong(3, 'p-branch-sales', 5, 'half', 0.5)

# p-crab-sizes
W = [68, 74, 60, 46, 52]; Cl = [59, 42, 40, 38, 21]
ok(Fr(sum(W), 5) == 60 and Fr(sum(Cl), 5) == 40, 'crabs: means 60 and 40')
dw = [a - 60 for a in W]; dc = [a - 40 for a in Cl]
ok(list(zip(dw, dc)) == [(8, 19), (14, 2), (0, 0), (-14, -2), (-8, -19)], 'crabs: demeaned pairs')
sxy = sum(a * c for a, c in zip(dw, dc))
key(3, 'p-crab-sizes', 1, Fr(sxy, 4))
wrong(3, 'p-crab-sizes', 1, 'over-n', Fr(sxy, 5)); wrong(3, 'p-crab-sizes', 1, 'no-divide', sxy); wrong(3, 'p-crab-sizes', 1, 'raw', Fr(sum(a * c for a, c in zip(W, Cl)), 4))
Sg = M([[sp.Rational(sum(a * a for a in dw), 4), sp.Rational(sxy, 4)], [sp.Rational(sxy, 4), sp.Rational(sum(a * a for a in dc), 4)]])
ok(Sg == M([[130, 90], [90, sp.Rational(365, 2)]]) and np.allclose(np.cov(W, Cl), np.array(Sg.tolist(), float)), 'crabs: covariance matrix, np.cov agrees')
ok(Sg.trace() == sp.Rational(625, 2) and Sg.det() == 15625 and 130 * sp.Rational(365, 2) == 23725, 'crabs: trace, det, 23725')
key(3, 'p-crab-sizes', 2, list(Sg.eigenvals().keys()))
wrong(3, 'p-crab-sizes', 2, 'diagonal', [130, 182.5]); wrong(3, 'p-crab-sizes', 2, 'over-n', [v * sp.Rational(4, 5) for v in Sg.eigenvals().keys()])
vals, vecs = np.linalg.eigh(np.array(Sg.tolist(), float))
ok(np.allclose(vals, [62.5, 250]), 'crabs: eigh values, smallest first')
ok(np.allclose(np.abs(vecs), [[0.8, 0.6], [0.6, 0.8]]), 'crabs: eigh vectors up to sign')
printed = np.array([[0.8, -0.6], [-0.6, -0.8]])
ok(np.allclose(np.array(Sg.tolist(), float) @ printed, printed * [62.5, 250]), 'crabs: the printed columns are eigenvectors for 62.5 and 250')
if not np.allclose(vecs, printed):
    print('CLAIM crabs part 3: NumPy here returns vecs =', vecs.round(4).tolist(), 'not the printed [[0.8, -0.6], [-0.6, -0.8]] (signs are free; see the review)')
pc1 = printed[:, -1]; pc1 = pc1 * np.sign(pc1[np.argmax(np.abs(pc1))])
key(3, 'p-crab-sizes', 3, [sp.nsimplify(v, rational=True) for v in pc1.round(12)])
wrong(3, 'p-crab-sizes', 3, 'first-column', [sp.Rational(8, 10), sp.Rational(-6, 10)]); wrong(3, 'p-crab-sizes', 3, 'no-flip', [sp.Rational(-6, 10), sp.Rational(-8, 10)])
score = Fr(6, 10) * dw[0] + Fr(8, 10) * dc[0]
key(3, 'p-crab-sizes', 4, score)
wrong(3, 'p-crab-sizes', 4, 'no-flip', -score); wrong(3, 'p-crab-sizes', 4, 'raw', Fr(6, 10) * W[0] + Fr(8, 10) * Cl[0]); wrong(3, 'p-crab-sizes', 4, 'pc2', Fr(8, 10) * dw[0] - Fr(6, 10) * dc[0])
scores = [Fr(6, 10) * a + Fr(8, 10) * c for a, c in zip(dw, dc)]
ok(sum(scores) == 0 and Fr(sum(v * v for v in scores), 4) == 250, 'crabs: scores have mean 0 and variance 250')
key(3, 'p-crab-sizes', 5, 20 / math.sqrt(250), 2)
wrong(3, 'p-crab-sizes', 5, 'variance', 20 / 250); wrong(3, 'p-crab-sizes', 5, 'total', 20 / math.sqrt(312.5)); wrong(3, 'p-crab-sizes', 5, 'pc2-sd', 20 / math.sqrt(62.5))
ok(round(math.sqrt(250), 2) == 15.81, 'crabs: sqrt 250 = 15.81')
w5 = part(3, 'p-crab-sizes', 5)['widget']
via_print = round(20 / 15.81, 2)
if abs(via_print - w5['answer']) > w5['tol']['abs']:
    print(f'CLAIM crabs part 5: the feedback prints 20/15.81; that is {20 / 15.81:.6f}, which rounds to {via_print}, outside the band {w5["answer"]} +/- {w5["tol"]["abs"]}')

# p-site-anomalies
sv = [30, 15, 6, 3]; n = 31
lam = [Fr(v * v, n - 1) for v in sv]
ok(lam == [30, Fr(15, 2), Fr(6, 5), Fr(3, 10)] and sum(v * v for v in sv) == 1170, 'sites: variances 30, 7.5, 1.2, 0.3 and 1170')
key(3, 'p-site-anomalies', 1, sum(lam))
wrong(3, 'p-site-anomalies', 1, 'no-divide', 1170); wrong(3, 'p-site-anomalies', 1, 'over-n', Fr(1170, 31)); wrong(3, 'p-site-anomalies', 1, 'unsquared', Fr(sum(sv), 30))
key(3, 'p-site-anomalies', 2, (lam[0] + lam[1]) / sum(lam), 3)
wrong(3, 'p-site-anomalies', 2, 'unsquared', Fr(45, 54)); wrong(3, 'p-site-anomalies', 2, 'pc1-only', lam[0] / sum(lam)); wrong(3, 'p-site-anomalies', 2, 'carried', (lam[0] + lam[1]) / 1170)
run = [sum(lam[:k]) / sum(lam) for k in range(1, 5)]
ok([round(float(v), 3) for v in run] == [0.769, 0.962, 0.992, 1.0], 'sites: running shares')
keep = next(k for k, v in enumerate(run, 1) if v >= Fr(99, 100))
key(3, 'p-site-anomalies', 3, keep); wrong(3, 'p-site-anomalies', 3, 'two', 2); wrong(3, 'p-site-anomalies', 3, 'all', 4)
rng = np.random.default_rng(7)
Q1, _ = np.linalg.qr(rng.standard_normal((31, 31))); Uc = Q1[:, :4] - Q1[:, :4].mean(axis=0)
Uo, _ = np.linalg.qr(Uc); Vo, _ = np.linalg.qr(rng.standard_normal((4, 4)))
Xc = Uo @ np.diag(sv) @ Vo.T
Xc = Xc - Xc.mean(axis=0)
Us, ss, Vts = np.linalg.svd(Xc, full_matrices=False)
ok(np.allclose(ss, sv), 'sites: a real demeaned 31 by 4 matrix has these singular values')
ok(near(np.var(Xc, axis=0, ddof=1).sum(), 39, 1e-9), 'sites: the sites\' variances add to 39')
Xk = Us[:, :keep] * ss[:keep] @ Vts[:keep]
key(3, 'p-site-anomalies', 4, round(float(((Xc - Xk)**2).sum()), 9))
wrong(3, 'p-site-anomalies', 4, 'unsquared', 3); wrong(3, 'p-site-anomalies', 4, 'rank-two', 36 + 9); wrong(3, 'p-site-anomalies', 4, 'kept', 900 + 225 + 36)
ok(round(9 / 1170 * 100, 1) == 0.8, 'sites: 0.8% of 1170')

# ---------------------------------------------------------------- claims
# "Only a triangular matrix shows its eigenvalues there" (problems-1 p-garden-path part 1, diagonal): false beyond 2 by 2
T3 = M([[5, 1, 1], [1, 2, 0], [-1, 0, 2]])
if T3.eigenvals() == {5: 1, 2: 2}:
    print('CLAIM garden path part 1 `diagonal`: [[5,1,1],[1,2,0],[-1,0,2]] is not triangular and has its eigenvalues 5, 2, 2 on its diagonal; "only a triangular matrix" holds for 2 by 2 alone')

# ---------------------------------------------------------------- set shape
for n, dset in SETS.items():
    items = dset['items']
    ok(3 <= len(items) <= 5, f'set {n}: 3 to 5 problems')
    ok(any(i['difficulty'] == 5 for i in items) and all(3 <= i['difficulty'] <= 5 for i in items), f'set {n}: difficulties')
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for i in items for p in i['parts'])
    total = sum(len(i['parts']) for i in items)
    ok(typed * 3 >= total * 2, f'set {n}: two thirds typed')
    for i in items:
        ok(3 <= len(i['parts']) <= 5, f'{i["id"]}: 3 to 5 parts')
        for k, pp in enumerate(i['parts'], 1):
            ex = pp['explain']['text'] if isinstance(pp['explain'], dict) else pp['explain']
            sents = [s for s in re.split(r'(?<=[.?])\s+(?=[A-Z$`])', re.sub(r'\$[^$]*\$', '$m$', ex)) if s.strip()]
            ok(len(sents) <= 3, f'{i["id"]} {k}: explanation has {len(sents)} sentences')
            ok(pp['feedback'].get('correct') and pp['feedback'].get('generic'), f'{i["id"]} {k}: feedback lines')
            if pp['widget']['kind'] == 'numeric':
                ok(re.search(r'Give|Type them|whole number|decimal', pp['question']), f'{i["id"]} {k}: states its form')
all_wrongs_seen(SEEN)
print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
