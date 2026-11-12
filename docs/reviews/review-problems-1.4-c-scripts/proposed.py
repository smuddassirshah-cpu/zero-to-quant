"""Second read, eigen problems-1 to -3: the numbers of the proposed fixes, each by two routes, and where the reused numbers stand.

Run from the repo root:  <scratchpad>/venv/bin/python docs/reviews/review-problems-1.4-c-scripts/proposed.py
"""
import glob
import json
import math
import re
import sys

import numpy as np
import sympy as sp

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails += 1


norm = lambda s: re.sub(r'\s+', '', s)
ALL = {f.replace('app/content/', ''): norm(open(f).read().replace('\\\\', '\\')) for f in glob.glob('app/content/**/*.json', recursive=True) if 'manifest' not in f}
where = lambda s: sorted(f for f, t in ALL.items() if norm(s) in t)
R = sp.Rational

# ---- finding 1 (crabs part 5): three places instead of two
exact = 20 / math.sqrt(250)
ok(round(exact, 3) == 1.265 and round(20 / 15.81, 3) == 1.265 and round(20 / 15.811, 3) == 1.265, f'crabs 5: exact {exact:.6f}, by 15.81 {20 / 15.81:.6f}, by 15.811 {20 / 15.811:.6f}: all 1.265 to 3 places')
ok(round(20 / 15.81, 2) == 1.27 and round(exact, 2) == 1.26, 'crabs 5 as it stands: 1.27 by the printed 15.81, 1.26 exactly')
ok(abs(exact - 1.265) < 0.0005 and abs(20 / 15.81 - 1.265) < 0.0005, 'crabs 5: both sit inside 1.265 +/- 0.0005')
ok(round(math.sqrt(250), 3) == 15.811, 'crabs 5: sqrt 250 = 15.811')
for name, val, want in (('variance', 20 / 250, 0.08), ('total', 20 / math.sqrt(312.5), 1.131), ('pc2-sd', 20 / math.sqrt(62.5), 2.53)):
    ok(round(val, 3) == want and abs(want - 1.265) > 0.001, f'crabs 5 slip {name}: {val:.5f} -> {want}')
sc = np.array([[8, 19], [14, 2], [0, 0], [-14, -2], [-8, -19]]) @ [0.6, 0.8]
ok(abs(sc[0] / sc.std(ddof=1) - exact) < 1e-12, 'crabs 5: score over the sample sd of the five scores (NumPy)')

# ---- finding 5 (gauges): reported r = 0.15 in place of 0.2
r = sp.Symbol('r')
C = sp.Matrix([[1, R(8, 10), r], [R(8, 10), 1, R(8, 10)], [r, R(8, 10), 1]])
w = sp.Matrix([1, R(-16, 10), 1])
form = sp.expand((w.T * C * w)[0])
ok(form == 2 * r - R(56, 100), 'gauges: w^T C w = 2r - 0.56')
v = form.subs(r, R(15, 100))
ok(v == R(-26, 100), f'gauges 5 at r = 0.15: {float(v)}')
Cn = np.array(C.subs(r, 0.15).tolist(), float); wn = np.array([1, -1.6, 1])
ok(abs(wn @ Cn @ wn + 0.26) < 1e-12 and np.linalg.eigvalsh(Cn).min() < 0, 'gauges 5: NumPy agrees, and C is not semidefinite at r = 0.15')
nd = sum(x * x for x in w) + sum(w[i] * w[j] * C[i, j] for i in range(3) for j in range(i + 1, 3)).subs(r, R(15, 100))
ok(nd == R(215, 100), f'gauges 5 slip no-double: 4.56 + (-2.41) = {float(nd)}')
ok(R(456, 100) + 2 * R(-241, 100) == R(-26, 100), 'gauges 5: 4.56 + 2(-2.41) = -0.26')
print('     0.15 beside 0.8 in the eigen course:', [f for f in where('0.15') if f.startswith('courses/eigen/') and '0.8&' in ALL[f]][:6])
h4 = json.dumps(next(i for i in json.load(open('app/content/courses/eigen/homework-4.json'))['items'] if i.get('id') == 'h-long-psd'), ensure_ascii=False)
ok('0.9' in h4 and '0.2' in h4 and '-0.2' in h4 and '0.62' in h4, 'homework-4 h-long-psd: correlations 0.9, 0.9, 0.2, a variance of -0.2 and the bound 0.62')
ok(abs((0.9 * 0.9 - (1 - 0.81)) - 0.62) < 1e-12 and abs((0.8 * 0.8 - (1 - 0.64)) - 0.28) < 1e-12, 'the same bound formula gives 0.62 there and 0.28 here')

# ---- finding 6 (tank part 5): weights in no other file
S = sp.Matrix([[3, 1, 1], [1, 3, 1], [1, 1, 3]])
print('     (0.5, 0.3, 0.2) stands in:', where('(0.5,0.3,0.2)'))
for cand in ('(0.5, 0.4, 0.1)', '(0.6, 0.3, 0.1)', '(0.6, 0.25, 0.15)'):
    print(f'     {cand} stands in:', where(cand))
wt = sp.Matrix([R(6, 10), R(25, 100), R(15, 100)])
d = wt - sp.Matrix([1, 1, 1]) / 3
ok(sum(wt) == 1 and sum(d) == 0, 'tank 5: weights add to 1, d adds to 0')
ok(list(d) == [R(4, 15), R(-1, 12), R(-11, 60)], f'tank 5: d = {list(d)}')
dd = d.dot(d)
ok(dd == R(67, 600), f'tank 5: |d|^2 = {dd} = {float(dd):.4f}')
full = (wt.T * S * wt)[0]
ok(full == R(5, 3) + 2 * dd == R(189, 100), f'tank 5: 5/3 + 2|d|^2 = {float(full)}')
wn = np.array([0.6, 0.25, 0.15])
ok(abs(wn @ np.array(S.tolist(), float) @ wn - 1.89) < 1e-12, 'tank 5: NumPy 1.89')
ok(3 * wt.dot(wt) == R(1335, 1000) and 2 * (wt[0] * wt[1] + wt[0] * wt[2] + wt[1] * wt[2]) == R(555, 1000), 'tank 5: direct, 3(0.445) + 2(0.2775) = 1.335 + 0.555')
ok(round(float(R(5, 3) + dd), 2) == 1.78 and round(float(2 * dd), 2) == 0.22 and 3 * wt.dot(wt) == R(1335, 1000), 'tank 5 slips: no-eigenvalue 1.78, d-only 0.22, no-cov 1.335')
print(f'     no-eigenvalue {float(R(5, 3) + dd):.4f}, d-only {float(2 * dd):.4f}, no-cov {float(3 * wt.dot(wt)):.4f}; 1.667 + 2 x {float(dd):.4f} = {1.667 + 2 * round(float(dd), 4):.4f}')

# ---- finding 2: the two general statements
T3 = sp.Matrix([[5, 1, 1], [1, 2, 0], [-1, 0, 2]])
ok(T3.eigenvals() == {5: 1, 2: 2} and not T3.is_upper and not T3.is_lower, 'a 3 by 3 matrix that is not triangular with its eigenvalues on its diagonal')
T2 = sp.Matrix([[5, 2], [0, 8]])
ok(sorted(T2.eigenvals()) == [5, 8] and not T2.is_diagonal(), 'a 2 by 2 matrix that is not diagonal with its eigenvalues on its diagonal (it is not symmetric)')
a, b_, dsym, lam = sp.symbols('a b d lambda')
cp = sp.expand((sp.Matrix([[a, b_], [b_, dsym]]) - lam * sp.eye(2)).det() - (a - lam) * (dsym - lam))
ok(cp == -b_**2, 'symmetric 2 by 2: the eigenvalues are the diagonal entries only when b = 0')

# ---- finding 8 (garden path part 4): the recurrence alone gives the key
t = [1, 1]
while len(t) < 11:
    t.append(t[-1] + 6 * t[-2])
ok(t[10] == 35839, f'garden path: nine additions give t_10 = {t[10]} with no eigenvalue')
ok(R(3, 5) * 3**10 + R(2, 5) * (-2)**10 == 35839, 'garden path: the closed form with 3 and -2 restated')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
