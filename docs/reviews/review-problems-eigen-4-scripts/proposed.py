"""Second read, eigen problems-4: the reuse the findings name, and the numbers of the proposed fixes, each by two routes.
Run from the repo root:  <scratchpad>/venv/bin/python docs/reviews/review-problems-eigen-4-scripts/proposed.py"""
import glob
import json
import math
import re
import sys

import numpy as np
import sympy as sp

n_ok = n_bad = 0


def ok(c, msg):
    global n_ok, n_bad
    n_ok += bool(c); n_bad += not c
    print(('ok   ' if c else 'FAIL ') + msg)


R = sp.Rational
# ---- finding 1: the lagoons item stands on l13's own M and M^-1 (read from the lesson file, not typed)
l13 = json.load(open('app/content/courses/eigen/l13-same-map-new-basis.json'))
mats = {m['id']: m['rows'] for m in l13['screens'][0]['canvas']['params']['matrices']}
ok(mats['M'] == [[1, 1], [0, 1]] and mats['Mi'] == [[1, -1], [0, 1]], 'l13 screen 0 uses M = (1 1; 0 1) and M^-1 = (1 -1; 0 1), the pair of p-linked-lagoons')
A13, B13 = sp.Matrix(mats['A']), sp.Matrix(mats['B'])
ok(A13.eigenvals() == {5: 1, 2: 1} and A13.trace() == 7 and A13.det() == 10 and B13[0, 1] == 0, 'l13: eigenvalues 5 and 2, trace 7, determinant 10, B lower triangular')
A = sp.Matrix([[-4, 2], [1, -3]])
ok(A.eigenvals() == {-5: 1, -2: 1} and A.trace() == -7 and A.det() == 10, 'lagoons: eigenvalues -5 and -2, trace -7, determinant 10 (l13 with the signs turned)')
# the fix: M = (1 0; 1 1), so w2 = u2 - u1
M = sp.Matrix([[1, 0], [1, 1]]); Mi = M.inv()
ok(Mi == sp.Matrix([[1, 0], [-1, 1]]), 'fix 1: M^-1 = (1 0; -1 1)')
u1, u2 = sp.symbols('u1 u2')
ok(list(Mi * sp.Matrix([u1, u2])) == [u1, u2 - u1], 'fix 1: w = (u1, u2 - u1)')
ok(A * M == sp.Matrix([[-2, 2], [-2, -3]]), 'fix 1: AM = (-2 2; -2 -3)')
B = Mi * A * M
ok(B == sp.Matrix([[-2, 2], [0, -5]]), 'fix 1: B = (-2 2; 0 -5), key of part 1 (bottom-right) stays -5')
ok(np.allclose(np.linalg.solve(np.array(M, float), np.array(A * M, float)), [[-2, 2], [0, -5]]), 'fix 1: route 2')
ok(A[1, 1] == -3 and (M * A * Mi)[1, 1] == -1, 'fix 1: wrong values unchanged -3, reversed -1 (sign stays 5)')
y = sp.Matrix([2, -3])
ok(B * y == -5 * y and M * y == sp.Matrix([2, -1]), 'fix 1: y = (2, -3) is an eigenvector of B for -5, My = (2, -1), key of part 3 stays')
ok(list(Mi * y) == [2, -5], 'fix 1: wrong inverse (2, -5), unmoved (2, -3)')
ok(list(Mi * sp.Matrix([5, 2])) == [5, -3], 'fix 1: wrong w-coords of part 4 becomes (5, -3)')
texts = {f: re.sub(r'\s+', '', open(f).read().replace('\\\\', '\\')) for f in glob.glob('app/content/courses/eigen/*.json')}
hits = sorted(f.split('/')[-1] for f, t in texts.items() if re.search(r'-2&2\\\\0&-5|\[\[-2,2\],\[0,-5\]\]', t))
ok(not hits, f'fix 1: the new B stands nowhere in the eigen course {hits}')

# ---- finding 2: the machine generator is twice l14's credit generator
src = open('app/content/courses/eigen/l14-continuous-time.json').read()
ok('[[-0.1, 0.3], [0.1, -0.3]]' in src, "l14 uses the generator (-0.1 0.3; 0.1 -0.3) in its solver tests, the credit generator of its transfer screen")
Q14 = sp.Matrix([[-R(1, 10), R(3, 10)], [R(1, 10), -R(3, 10)]])
Q = sp.Matrix([[-R(1, 5), R(3, 5)], [R(1, 5), -R(3, 5)]])
ok(Q == 2 * Q14, 'machine: Q = 2 x the l14 generator, so the steady state (0.75, 0.25) and the eigenvectors (3, 1), (1, -1) are the lesson\'s')
ok('0.75 + 0.25*exp(-0.4*x)' in src, 'l14 screen 10 plots 0.75 + 0.25 e^{-0.4t}; the item has 0.75 + 0.25 e^{-2.4} and 0.25 + 0.75 e^{-0.8t}')
# the fix: stops at rate 0.1, restarts at rate 0.4, part 4 asks for 5 hours
a, b = R(1, 10), R(2, 5)
Qn = sp.Matrix([[-a, b], [a, -b]])
ok(Qn.eigenvals() == {0: 1, -R(1, 2): 1} and Qn.det() == 0 and a * b == R(4, 100), 'fix 2: eigenvalues 0 and -0.5, det 0.04 - 0.04 = 0, trace -0.5')
lam = sp.Symbol('lam')
ok(sp.expand((Qn - lam * sp.eye(2)).det() - lam * (lam + R(1, 2))) == 0, 'fix 2: characteristic polynomial lam^2 + 0.5 lam')
ns = Qn.nullspace()[0]; st = ns / sum(ns)
ok(list(st) == [R(4, 5), R(1, 5)] and a * st[0] == R(8, 100) and b * st[1] == R(8, 100), 'fix 2: steady state (0.8, 0.2), direction (4, 1), both flows 0.08')
P = sp.Matrix([[0, 1], [1, 0]]); Qp = P * Qn * P
ok(Qp == sp.Matrix([[-b, a], [b, -a]]) and Qp * sp.Matrix([1, -1]) == -R(1, 2) * sp.Matrix([1, -1]), "fix 2: Q' = (-0.4 0.1; 0.4 -0.1), eigenvector (1, -1) for -0.5")
ok(sp.Matrix([1, 0]) == sp.Matrix([R(1, 5), R(4, 5)]) + R(4, 5) * sp.Matrix([1, -1]), 'fix 2: (1, 0) = (0.2, 0.8) + 0.8 (1, -1)')
p5 = 0.2 + 0.8 * math.exp(-2.5)
ok(abs(float((Qp * 5).exp()[0, 0]) - p5) < 1e-12, 'fix 2: route 2, matrix exponential entry at t = 5')
vals = {
    'part 4 key': (p5, 0.266), 'printed e^-2.5': (math.exp(-2.5), 0.0821), 'printed working 0.2 + 0.8 x 0.0821': (0.2 + 0.8 * 0.0821, 0.266),
    'running-chance': (0.8 + 0.2 * math.exp(-2.5), 0.816), 'no-steady': (0.8 * math.exp(-2.5), 0.066),
    'restart-rate': (0.2 + 0.8 * math.exp(-0.4 * 5), 0.308), 'one-hour': (0.2 + 0.8 * math.exp(-0.5), 0.685),
    'part 5 key': (math.log(80) / 0.5, 8.76), 'printed ln 80': (math.log(80), 4.382), 'printed working 4.382 / 0.5': (4.382 / 0.5, 8.76),
    'p5 running-start': (math.log(20) / 0.5, 5.99), 'p5 no-coefficient': (math.log(100) / 0.5, 9.21),
    'p5 restart-rate': (math.log(80) / 0.4, 10.96), 'p5 multiplied': (math.log(80) * 0.5, 2.19),
}
for name, (v, shown) in vals.items():
    places = len(str(shown).split('.')[1])
    frac = abs(v * 10 ** places % 1 - 0.5)
    keyish = name.startswith(('part', 'printed'))  # a slip's band (tol = one unit of the last place) holds both roundings
    ok(round(v, places) == shown and (frac > 0.02 or not keyish), f'fix 2: {name} = {v:.6f} -> {shown}' + (' (not near a rounding tie)' if keyish else ''))
k4 = sorted([0.266, 0.816, 0.066, 0.308, 0.685]); k5 = sorted([8.76, 5.99, 9.21, 10.96, 2.19])
ok(min(q - p for p, q in zip(k4, k4[1:])) > 0.002 and min(q - p for p, q in zip(k5, k5[1:])) > 0.02, 'fix 2: no two bands touch at tol 0.001 and 0.01')
ts = np.arange(0, 15, 1e-5)
ok(abs(ts[np.argmax(0.8 * np.exp(-0.5 * ts) <= 0.01)] - math.log(80) / 0.5) < 1e-4, 'fix 2: route 2, scan in t for part 5')
hits = sorted(f.split('/')[-1] for f, t in texts.items() if re.search(r'-0\.1&0\.4\\\\0\.1&-0\.4|\(0\.8,0\.2\)|\[\[-0\.1,0\.4\]', t) and 'problems-4' not in f)
print(f'note fix 2: eigen files holding the new generator or the pair (0.8, 0.2): {hits}')

# ---- finding 4: what the `carried` band of wind part 2 holds
ok(abs(-6 / 9 - (-1.029)) <= 0.5 and abs(-6 / math.sqrt(14) - (-1.029)) > 0.5, 'wind 2: -6/9 (L22 = 9 carried) is in the carried band; -6/sqrt 14 is not')

# ---- read and accepted: homework-4 h-pinv1 has the same answer as p-track-laps part 3
Ah, bh = sp.Matrix([[1, 2], [2, 4]]), sp.Matrix([5, 10])
ok(list(Ah.T * bh / 25) == [1, 2] and list(Ah.pinv() * bh) == [1, 2], 'homework-4 h-pinv1: x = (1, 2), the answer of p-track-laps part 3')
print(f'\nproposed.py: {n_ok + n_bad} checks, {n_bad} failures')
sys.exit(1 if n_bad else 0)
