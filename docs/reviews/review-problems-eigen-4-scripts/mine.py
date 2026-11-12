"""Second read, eigen problems-4: the reader's own recompute. Imports nothing from the author's script.
Every matrix, vector and data column is typed here from the prose. Route 1 is exact (sympy), route 2 is another
method (NumPy eig, cholesky, solve, pinv, lstsq, a stepped ODE, a simulation of the two-state chain, a scan in t).
Every key, every `wrong` value (rebuilt from the slip its line names) and every number printed in a feedback or
explain string is checked against the file. Exit 0 when all agree.
Run from the repo root:  <scratchpad>/venv/bin/python docs/reviews/review-problems-eigen-4-scripts/mine.py"""
import json
import math
import re
import sys

import numpy as np
import sympy as sp

D = json.load(open('app/content/courses/eigen/problems-4.json'))
IT = {it['id']: it for it in D['items']}
n_ok = n_bad = 0


def ok(cond, msg):
    global n_ok, n_bad
    if cond:
        n_ok += 1
    else:
        n_bad += 1
        print('FAIL', msg)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def part(item, k):
    return IT[item]['parts'][k - 1]


def key(item, k, mine, places=None):
    """the file's key equals mine (rounded as the part asks), and its band holds the unrounded value"""
    w = part(item, k)['widget']
    if 'answers' in w:
        ok(sorted(w['answers']) == sorted(float(x) for x in mine), f'{item} {k}: key set {w["answers"]} vs mine {mine}')
        return
    a, tol = w['answer'], w.get('tol', {}).get('abs', 0)
    ok(close(a, round(float(mine), places) if places is not None else mine), f'{item} {k}: key {a} vs mine {mine}')
    ok(abs(a - float(mine)) <= tol + 1e-12, f'{item} {k}: band {a}+-{tol} holds the exact value {float(mine)}')


def wrong(item, k, wid, mine, places=None):
    w = part(item, k)['widget']
    x = [e for e in w['wrong'] if e['id'] == wid]
    ok(len(x) == 1, f'{item} {k}: wrong id {wid} present')
    if not x:
        return
    x = x[0]
    if 'tex' in x:
        ok(re.sub(r'\s', '', x['tex']) == re.sub(r'\s', '', mine), f'{item} {k}: wrong {wid} tex {x["tex"]} vs mine {mine}')
    elif isinstance(x['value'], str):
        got = sorted(float(v) for v in x['value'].split(','))
        ok(got == sorted(float(v) for v in mine), f'{item} {k}: wrong {wid} {x["value"]} vs mine {mine}')
    else:
        r = round(float(mine), places) if places is not None else float(mine)
        ok(close(x['value'], r), f'{item} {k}: wrong {wid} {x["value"]} vs mine {mine}')
        ok(part(item, k)['feedback']['byKey'].get(wid), f'{item} {k}: wrong {wid} has a line')


def bands(item, k):
    """no wrong band holds the key or touches another wrong band; the key band holds no wrong value"""
    w = part(item, k)['widget']
    if w['kind'] != 'numeric' or 'answers' in w:
        return
    a, t = w['answer'], w['tol']['abs']
    ws = [(e['id'], e['value'], e['tol']['abs']) for e in w.get('wrong', [])]
    for i, (wid, v, wt) in enumerate(ws):
        ok(abs(v - a) > t + wt, f'{item} {k}: band of {wid} ({v}+-{wt}) clear of the key band ({a}+-{t})')
        for wid2, v2, wt2 in ws[i + 1:]:
            ok(abs(v - v2) > wt + wt2, f'{item} {k}: bands of {wid} and {wid2} do not touch')


def says(item, k, where, *needles):
    """each needle stands in the named string of the part (prose numbers the reader recomputed)"""
    p = IT[item] if k == 0 else part(item, k)
    s = p
    for step in where.split('.'):
        s = s[step] if not isinstance(s, list) else s[int(step)]
    if isinstance(s, dict):
        s = s.get('text', '')
    for nd in needles:
        ok(nd in s, f'{item} {k} {where}: expected to print "{nd}"')


# ---------------------------------------------------------------- p-linked-lagoons
I = 'p-linked-lagoons'
A = sp.Matrix([[-4, 2], [1, -3]])
M = sp.Matrix([[1, 0], [1, 1]])
Mi = M.inv()
ok(Mi == sp.Matrix([[1, 0], [-1, 1]]), 'lagoons: stated inverse of M')
ok(Mi * sp.Matrix(sp.symbols('u1 u2')) == sp.Matrix([sp.Symbol('u1'), sp.Symbol('u2') - sp.Symbol('u1')]), 'lagoons: w2 = u2 - u1')
B = Mi * A * M
ok(A * M == sp.Matrix([[-2, 2], [-2, -3]]), 'lagoons 1: AM as the correct line prints it')
ok(B == sp.Matrix([[-2, 2], [0, -5]]), 'lagoons 1: B as the explain prints it')
key(I, 1, B[1, 1])
ok(close(np.linalg.solve(np.array(M, float), np.array(A * M, float))[1, 1], -5), 'lagoons 1: route 2, solve M B = A M')
wrong(I, 1, 'sign', 5); wrong(I, 1, 'unchanged', A[1, 1]); wrong(I, 1, 'reversed', (M * A * Mi)[1, 1])
ev = A.eigenvals()
ok(ev == {-5: 1, -2: 1} and B.eigenvals() == ev, 'lagoons 2: eigenvalues of A and B, exact')
ok(np.allclose(sorted(np.linalg.eigvals(np.array(A, float)).real), [-5, -2]), 'lagoons 2: route 2, NumPy eigvals')
key(I, 2, [-5, -2])
wrong(I, 2, 'sign', [5, 2]); wrong(I, 2, 'trace-det', [A.trace(), A.det()]); wrong(I, 2, 'a-diagonal', [A[0, 0], A[1, 1]])
ok(A.trace() == -7 and A.det() == 10, 'lagoons 2: trace -7 and determinant 12 - 2 = 10')
lam = sp.Symbol('lam')
ok(sp.expand((A - lam * sp.eye(2)).det() - (lam + 5) * (lam + 2)) == 0, 'lagoons 2: characteristic polynomial factors as the explain says')
y = sp.Matrix([2, -3])
ok(B * y == -5 * y, 'lagoons 3: (2, -3) is an eigenvector of B for -5')
x = M * y
ok(x == sp.Matrix([2, -1]) and A * x == sp.Matrix([-10, 5]) and A * x == -5 * x, 'lagoons 3: x = My = (2, -1), A x = (-10, 5)')
ok(part(I, 3)['widget']['answer'] == '(2, -1)', 'lagoons 3: key')
wrong(I, 3, 'inverse', '(%s,%s)' % tuple(Mi * y)); wrong(I, 3, 'unmoved', '(2,-3)')
ok(A * sp.Matrix([1, 1]) == -2 * sp.Matrix([1, 1]), 'lagoons 4: (1, 1) is an eigenvector of A for -2')
c = sp.Matrix([[1, 2], [1, -1]]).LUsolve(sp.Matrix([5, 2]))
ok(list(c) == [3, 1], 'lagoons 4: (c1, c2) = (3, 1)')
ok(np.allclose(np.linalg.lstsq(np.array([[1, 2], [1, -1]], float), np.array([5, 2.]), rcond=None)[0], [3, 1]), 'lagoons 4: route 2')
ok(part(I, 4)['widget']['answer'] == '(3, 1)', 'lagoons 4: key')
wrong(I, 4, 'swapped', '(1,3)'); wrong(I, 4, 'w-coords', '(%s,%s)' % tuple(Mi * sp.Matrix([5, 2])))
tot = 6 * sp.exp(-2) + sp.exp(-5)
key(I, 5, tot, 3)
# route 2: step u' = Au with RK4 from (5, 2) to t = 1
u, h, An = np.array([5., 2.]), 1e-4, np.array(A, float)
for _ in range(10000):
    k1 = An @ u; k2 = An @ (u + h / 2 * k1); k3 = An @ (u + h / 2 * k2); k4 = An @ (u + h * k3)
    u = u + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
ok(close(u.sum(), float(tot), 1e-8), f'lagoons 5: route 2, RK4 total {u.sum()}')
ok(close(u[0], float(3 * sp.exp(-2) + 2 * sp.exp(-5)), 1e-8), 'lagoons 5: u1(1) from the stepped system')
wrong(I, 5, 'coefficients-only', 3 * sp.exp(-2) + sp.exp(-5), 3)
wrong(I, 5, 'u1-only', 3 * sp.exp(-2) + 2 * sp.exp(-5), 3)
wrong(I, 5, 'rates-swapped', 6 * sp.exp(-5) + sp.exp(-2), 3)
wrong(I, 5, 'carried', 2 * sp.exp(-2) + 3 * sp.exp(-5), 3)
ok(round(math.exp(-2), 4) == 0.1353 and round(math.exp(-5), 4) == 0.0067, 'lagoons 5: e^-2 = 0.1353, e^-5 = 0.0067')
says(I, 5, 'feedback.correct', '0.1353', '0.0067', '0.819'); says(I, 5, 'explain', '0.0067', '0.819')
# CLAIM (finding): the generic line's rounded constants give 0.8185, a tie at 3 places
printed = round(6 * 0.1353 + 0.0067, 4)
print(f'CLAIM lagoons 5: the working the feedback prints gives 6 x 0.1353 + 0.0067 = {printed}; half-down 0.818 is {abs(0.818 - 0.819):.4f} from the key, tol 0.001')

# ---------------------------------------------------------------- p-wind-pair
I = 'p-wind-pair'
S = sp.Matrix([[16, 20], [20, 34]])
L = S.cholesky()
ok(L == sp.Matrix([[4, 0], [5, 3]]), 'wind 1: exact Cholesky factor')
ok(np.allclose(np.linalg.cholesky(np.array(S, float)), [[4, 0], [5, 3]]), 'wind 1: route 2, NumPy cholesky')
key(I, 1, L[1, 1])
wrong(I, 1, 'no-subtract', sp.sqrt(34), 3); wrong(I, 1, 'subtract-sigma', sp.sqrt(34 - 20), 3); wrong(I, 1, 'no-root', 34 - 25)
xv = sp.Matrix([8, 4])
w = L.LUsolve(xv)
ok(list(w) == [2, -2], 'wind 2: w = (2, -2)')
ok(np.allclose(np.linalg.solve(np.array(L, float), [8., 4.]), [2, -2]), 'wind 2: route 2')
key(I, 2, w[1])
wrong(I, 2, 'sign', 2); wrong(I, 2, 'used-x1', sp.Rational(4 - 5 * 8, 3)); wrong(I, 2, 'no-subtract', sp.Rational(4, 3), 3)
wrong(I, 2, 'carried', (4 - 10) / sp.sqrt(34), 3)
d2 = (xv.T * S.inv() * xv)[0]
ok(d2 == 8 and w.dot(w) == 8, 'wind 3: d^2 = 8 by both formulas')
key(I, 3, sp.sqrt(8), 3)
wrong(I, 3, 'squared', 8); wrong(I, 3, 'ignore-correlation', sp.sqrt(sp.Rational(8, 4) ** 2 + sp.Rational(16, 34)), 3)
wrong(I, 3, 'carried', sp.sqrt(2 ** 2 + 12 ** 2), 3)
key(I, 4, sp.exp(-4), 4)
rng = np.random.default_rng(20261112)
z = rng.standard_normal((2_000_000, 2))
xs = z @ np.array(L, float).T
q = np.einsum('ij,jk,ik->i', xs, np.linalg.inv(np.array(S, float)), xs)
ok(abs((q >= 8).mean() - math.exp(-4)) < 0.0005, f'wind 4: route 2, simulated tail {(q >= 8).mean():.5f} against e^-4 = {math.exp(-4):.5f}')
wrong(I, 4, 'used-d', sp.exp(-sp.sqrt(8) / 2), 4); wrong(I, 4, 'no-half', sp.exp(-8), 4)
wrong(I, 4, 'carried', sp.exp(-(4 + sp.Rational(16, 34)) / 2), 4)
ok(round(1 / math.exp(-4)) == 55, 'wind 4: about one hour in 55')
ok(sp.Rational(20, 16) * 8 == 10 and sp.sqrt(34 - sp.Rational(400, 16)) == 3, 'wind 2 explain: turbine 1 points to +10, conditional sd 3')
ok(8 / 4 == 2 and 4 / math.sqrt(34) < 2, 'wind 4 explain: each turbine alone at most 2 sd out')
says(I, 3, 'feedback.byKey.ignore-correlation', '8/4', '4/\\sqrt{34}')

# ---------------------------------------------------------------- p-track-laps
I = 'p-track-laps'
X = sp.Matrix([[2, 4], [1, 2], [2, 4]])
yv = sp.Matrix([11, 5, 9])
G = X.T * X
ok(G == sp.Matrix([[9, 18], [18, 36]]), 'track 1: X^T X')
L11 = sp.sqrt(G[0, 0]); L21 = G[1, 0] / L11; L22 = sp.sqrt(G[1, 1] - L21 ** 2)
ok((L11, L21, L22) == (3, 6, 0), 'track 1: L11 = 3, L21 = 6, L22 = 0')
key(I, 1, L22)
wrong(I, 1, 'root-36', sp.sqrt(36)); wrong(I, 1, 'subtract-entry', sp.sqrt(36 - 18), 3)
ok(G.rank() == 1 and G.eigenvals() == {45: 1, 0: 1}, 'track 2: rank 1, eigenvalues 45 and 0')
ok(np.allclose(sorted(np.linalg.eigvalsh(np.array(G, float))), [0, 45]), 'track 2: route 2')
key(I, 2, 45)
wrong(I, 2, 'diagonal', 36); wrong(I, 2, 'first-entry', 9)
ok(G * sp.Matrix([1, 2]) == sp.Matrix([45, 90]), 'track 2 explain: X^T X (1, 2) = (45, 90)')
v1 = sp.Matrix([1, 2]) / sp.sqrt(5); s1 = sp.sqrt(45)
u1 = sp.simplify(X * v1 / s1)
ok(u1 == sp.Matrix([2, 1, 2]) / 3, 'track 3: u1 = (2, 1, 2)/3')
ok(u1.dot(yv) == 15 and sp.simplify(sp.sqrt(5) * sp.sqrt(45)) == 15, 'track 3: u1.y = 15, sqrt5 sqrt45 = 15')
beta = sp.simplify(v1 * u1.dot(yv) / s1)
ok(list(beta) == [1, 2], 'track 3: beta+ = (1, 2)')
Xn, yn = np.array(X, float), np.array(yv, float).ravel()
ok(np.allclose(np.linalg.pinv(Xn) @ yn, [1, 2]) and np.allclose(np.linalg.lstsq(Xn, yn, rcond=None)[0], [1, 2]), 'track 3: route 2, pinv and lstsq')
ok(part(I, 3)['widget']['answer'] == '(1, 2)', 'track 3: key')
res = lambda b: float(np.sum((Xn @ np.array(b, float) - yn) ** 2))
ok(close(res([1, 2]), res([5, 0])) and close(res([1, 2]), res([0, 2.5])) and res([1, 2]) < res([1.1, 2]), 'track 3: (5, 0) and (0, 2.5) fit as well')
wrong(I, 3, 'all-km', '(5,0)'); wrong(I, 3, 'all-laps', '(0,2.5)')
ok(math.hypot(5, 0) == 5 and close(math.hypot(1, 2), math.sqrt(5)), 'track 3: lengths 5 and sqrt 5')
key(I, 4, 1 * 3 + 2 * 6)
ok(5 * 3 == 15, 'track 4: (5, 0) predicts 15 too')
wrong(I, 4, 'laps-as-km', 1 * 3 + 2 * 3); wrong(I, 4, 'km-only', 1 * 3)

# ---------------------------------------------------------------- p-machine-stops
I = 'p-machine-stops'
Q = sp.Matrix([[-sp.Rational(1, 10), sp.Rational(2, 5)], [sp.Rational(1, 10), -sp.Rational(2, 5)]])
ok(Q.eigenvals() == {0: 1, -sp.Rational(1, 2): 1}, 'machine 1: eigenvalues 0 and -0.5')
ok(np.allclose(sorted(np.linalg.eigvals(np.array(Q, float)).real), [-0.5, 0]), 'machine 1: route 2')
key(I, 1, [0, -0.5])
wrong(I, 1, 'sign', [0, 0.5]); wrong(I, 1, 'diagonal', [-0.1, -0.4])
ok(Q.det() == 0 and Q.trace() == -sp.Rational(1, 2), 'machine 1: det 0.04 - 0.04 = 0 and trace -0.5')
ok(sp.expand((Q - lam * sp.eye(2)).det() - lam * (lam + sp.Rational(1, 2))) == 0, 'machine 1: characteristic polynomial')
ns = Q.nullspace()[0]; st = ns / sum(ns)
ok(list(st) == [sp.Rational(4, 5), sp.Rational(1, 5)], 'machine 2: steady state (0.8, 0.2)')
ok(part(I, 2)['widget']['answer'] == '(0.8, 0.2)', 'machine 2: key')
wrong(I, 2, 'swapped', '(0.2,0.8)'); wrong(I, 2, 'unscaled', '(4,1)')
ok(close(0.1 * 0.8, 0.08) and close(0.4 * 0.2, 0.08), 'machine 2 explain: both flows 0.08')
P = sp.Matrix([[0, 1], [1, 0]])
Qp = P.inv() * Q * P
ok(Qp == sp.Matrix([[-sp.Rational(2, 5), sp.Rational(1, 10)], [sp.Rational(2, 5), -sp.Rational(1, 10)]]), "machine 3: Q' as the explain prints it")
ok(Qp.eigenvals() == Q.eigenvals() and P.inv() * st == sp.Matrix([sp.Rational(1, 5), sp.Rational(4, 5)]), 'machine 3: same eigenvalues, steady state (0.2, 0.8)')
opts = part(I, 3)['widget']['options']
ok([o['id'] for o in opts if o.get('correct')] == ['moved'], 'machine 3: key option')
ok(Qp * sp.Matrix([1, -1]) == -sp.Rational(1, 2) * sp.Matrix([1, -1]), "machine 4: (1, -1) is an eigenvector of Q' for -0.5")
ok(sp.Matrix([1, 0]) == sp.Matrix([sp.Rational(1, 5), sp.Rational(4, 5)]) + sp.Rational(4, 5) * sp.Matrix([1, -1]), 'machine 4: the split of (1, 0)')
p3 = sp.Rational(1, 5) + sp.Rational(4, 5) * sp.exp(-sp.Rational(5, 2))
key(I, 4, p3, 3)
E3 = (Qp * 5).exp()
ok(close(sp.N(E3[0, 0]), sp.N(p3), 1e-12), 'machine 4: route 2, exact matrix exponential entry (Stopped, Stopped)')
# route 3: simulate the two-state chain (state 0 = Stopped leaves at rate 0.4, Running at rate 0.1)
rng = np.random.default_rng(7)
N = 400_000
state = np.zeros(N, int); t = np.zeros(N)
alive = np.ones(N, bool)
while alive.any():
    rate = np.where(state == 0, 0.4, 0.1)
    t_next = t + rng.exponential(1 / rate)
    jump = alive & (t_next <= 5)
    state = np.where(jump, 1 - state, state); t = np.where(jump, t_next, t); alive = jump
ok(abs((state == 0).mean() - float(p3)) < 0.003, f'machine 4: simulated chance {(state == 0).mean():.4f} against {float(p3):.4f}')
wrong(I, 4, 'running-chance', 0.8 + 0.2 * math.exp(-2.5), 3); wrong(I, 4, 'no-steady', 0.8 * math.exp(-2.5), 3)
wrong(I, 4, 'restart-rate', 0.2 + 0.8 * math.exp(-0.4 * 5), 3); wrong(I, 4, 'one-hour', 0.2 + 0.8 * math.exp(-0.5), 3)
ok(round(math.exp(-2.5), 4) == 0.0821, 'machine 4: e^-2.5 = 0.0821'); says(I, 4, 'feedback.correct', '0.0821', '0.266')
t5 = sp.log(80) / sp.Rational(1, 2)
key(I, 5, t5, 2)
ts = np.arange(0, 14, 1e-5)
first = ts[np.argmax(0.8 * np.exp(-0.5 * ts) <= 0.01)]
ok(abs(first - float(t5)) < 1e-4, f'machine 5: route 2, scan in t gives {first:.4f}')
ok(round(math.log(80), 3) == 4.382, 'machine 5: ln 80 = 4.382'); says(I, 5, 'feedback.correct', '4.382', '8.76')
wrong(I, 5, 'running-start', math.log(20) / 0.5, 2); wrong(I, 5, 'no-coefficient', math.log(100) / 0.5, 2)
wrong(I, 5, 'restart-rate', math.log(80) / 0.4, 2); wrong(I, 5, 'multiplied', math.log(80) * 0.5, 2)

# ---------------------------------------------------------------- shape of the set, bands, voice
for it in D['items']:
    for k in range(1, len(it['parts']) + 1):
        bands(it['id'], k)
        p = part(it['id'], k)
        ex = p['explain']['text']
        ok(len(re.findall(r'[.?](?:\s|$)', re.sub(r'\$[^$]*\$', 'M', ex))) <= 3, f'{it["id"]} {k}: explain at most three sentences')
        blob = json.dumps(p, ensure_ascii=False) + it['prose']
        ok('!' not in re.sub(r'\$[^$]*\$', '', blob) and '—' not in blob, f'{it["id"]} {k}: no exclamation mark or em-dash')
        if k > 1 and p['widget']['kind'] != 'choice':
            ok('part' in p['question'].lower(), f'{it["id"]} {k}: names the part it builds on')
parts = [p for it in D['items'] for p in it['parts']]
typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
ok(len(D['items']) == 4 and len(parts) == 18 and typed * 3 >= 2 * len(parts), f'set shape: 4 items, 18 parts, {typed} typed')
ok(all(3 <= len(it['parts']) <= 5 and 3 <= it['difficulty'] <= 5 for it in D['items']) and any(it['difficulty'] == 5 for it in D['items']), 'parts 3 to 5, difficulty 3 to 5, one 5')

# CLAIM rows for wide wrong bands (findings): values other than the named slip that fall in a +-0.5 band
print('CLAIM wind 1: band subtract-sigma 3.742+-0.5 holds 4 = L11 and 3.5; no-subtract 5.831+-0.5 holds 6')
print(f'CLAIM wind 2: band carried -1.029+-0.5 holds -6/9 = {-6/9:.3f} (L22 = 9 carried, the no-root slip) and -1')
print(f'CLAIM track 1: band subtract-entry 4.243+-0.5 holds 4 and 4.5')
print(f'\nmine.py: {n_ok + n_bad} checks, {n_bad} failures')
sys.exit(1 if n_bad else 0)
