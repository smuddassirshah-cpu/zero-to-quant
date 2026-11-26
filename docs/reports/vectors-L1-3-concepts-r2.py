#!/usr/bin/env python3
"""Concept audit, round 2, of the `vectors` course, levels 1 to 3 (audit vectors-1-3-r2).

Recomputes the stated figures, keys and slips the audit relied on, checks each empirical claim by simulation, and runs
the hidden tests of the Python widgets against natural wrong programs in CPython. A check that fails because the content
is wrong stays failing: the script exits 1 while any finding marked FAIL below is open, and 0 on correct content.

    python docs/reports/vectors-L1-3-concepts-r2.py [--pyodide <pkgs>]

--pyodide runs the companion sweep (vectors-L1-3-concepts-r2-sweep.mjs) under the page's Pyodide 0.27.7 as well; without it
the floating-point checks use this interpreter's NumPy (values that differ between builds are marked BUILD).
"""
import itertools
import json
import math
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'vectors')
J = lambda name: json.load(open(os.path.join(CDIR, name + '.json'), encoding='utf-8'))
rng = np.random.default_rng(20261126)
fails, passed = [], 0


def check(tag, cond, what):
    global passed
    if cond:
        passed += 1
    else:
        fails.append((tag, what))
        print(f'FAIL [{tag}] {what}')


close = lambda a, b, tol=1e-9: bool(np.allclose(a, b, atol=tol, rtol=0))

# ---------------------------------------------------------------------------------------------------------------
# Level 1: combinations, dot product, length, angle, projection, portfolio return
# ---------------------------------------------------------------------------------------------------------------
u, v = np.array([2., 1]), np.array([1., 2])
check('l1', close(np.linalg.solve(np.column_stack([u, v]), [7, 8]), [2, 3]), 'l1 s3 weights (2, 3)')
check('l1', close(np.linalg.solve(np.column_stack([u, v]), [1, -1]), [1, -1]), 'l1 s4 weights (1, -1)')
x, y = 0.37, -1.9
check('l1', close(np.linalg.solve(np.column_stack([u, v]), [x, y]), [(2 * x - y) / 3, (2 * y - x) / 3]), 'l1 s7 a = (2x - y)/3, b = (2y - x)/3')
check('l1', close(np.linalg.solve([[1, 0.2], [0.2, 1]], [0.68, 0.52]), [0.6, 0.4]), 'l1 s8 fund weights 0.6 and 0.4')
check('l1', close(np.linalg.solve([[3, 1], [1, -1]], [5, 3]), [2, -1]), 'l1 quiz weights (2, -1)')
# span claim: two arrows reach the plane exactly when neither is a multiple of the other (rank 2), 20,000 random integer pairs
ok = True
for _ in range(20000):
    a, b = rng.integers(-4, 5, 2), rng.integers(-4, 5, 2)
    parallel = a[0] * b[1] - a[1] * b[0] == 0
    ok &= (np.linalg.matrix_rank(np.column_stack([a, b]).astype(float)) < 2) == parallel
check('l1', ok, 'l1 s6: a pair fails to span exactly when one arrow is a multiple of the other')

check('l2', np.dot([3, 1], [-2, 5]) == -1 and 3 * 5 + 1 * -2 == 13 and (3 + 1) * (-2 + 5) == 12, 'l2 s1 key -1 and slips 13, 12')
ang = math.degrees(math.acos(-1 / math.sqrt(10 * 29)))
check('l2', 90 < ang < 95, 'l2 s1: (3,1) and (-2,5) are a little more than a right angle apart')
check('l2', [np.dot([2, 1], w) for w in ([-1, 3], [1, -3], [-2, 1], [2, -1], [-1, -2])] == [1, -1, -3, 3, -4], 'l2 s4 five dot products')
check('l2', np.dot([1, 2, 3], [4, -5, 6]) == 12 and 4 + 10 + 18 == 32 and 1 + 2 + 3 + 4 - 5 + 6 == 11, 'l2 s6 key and slips')
check('l2', close(np.dot([4, 2, -5], [1.2, 0.5, 0.8]), 1.8) and close(1.8e6 * 0.01, 18000), 'l2 s8 exposure 1.8 and 18,000 per 1%')
check('l2', close(np.dot([3, -2], [0.9, 1.5]), -0.3), 'l2 quiz book exposure -0.3')
# sign of the dot product follows the angle (the law is exact; 100,000 random pairs)
A = rng.normal(size=(100000, 2)); B = rng.normal(size=(100000, 2))
dots = (A * B).sum(1); angs = np.degrees(np.abs(np.arctan2(A[:, 0] * B[:, 1] - A[:, 1] * B[:, 0], dots)))
check('l2', bool(np.all((dots > 0) == (angs < 90))), 'l2: dot product positive exactly within 90 degrees')

check('l3', close(np.array([6, -8]) / 10, [0.6, -0.8]), 'l3 s2 unit vector')
uu, vv = np.array([1., 2]), np.array([3., 1])
check('l3', close(math.degrees(math.acos(uu @ vv / math.sqrt(uu @ uu * (vv @ vv)))), 45), 'l3 s4 angle 45 degrees')
uu, vv = np.array([3., 4]), np.array([2., 1]); k = uu @ vv / (vv @ vv)
check('l3', k == 2 and (uu - k * vv) @ vv == 0, 'l3 s5 foot (4, 2), residual perpendicular')
uu, vv = np.array([2., 6]), np.array([3., 4]); k = uu @ vv / (vv @ vv)
check('l3', close(k, 1.2) and close(k * vv, [3.6, 4.8]) and close(np.linalg.norm(k * vv), 6) and close(25 / 30, 0.8333, 1e-4), 'l3 s6 k = 1.2 and slips')
# Cauchy-Schwarz and triangle inequality, equality only for same direction or a zero arrow (200,000 random pairs in 2 to 6 dimensions)
ok = True
for n in range(2, 7):
    P, Q = rng.normal(size=(40000, n)), rng.normal(size=(40000, n))
    ok &= bool(np.all(np.abs((P * Q).sum(1)) <= np.linalg.norm(P, axis=1) * np.linalg.norm(Q, axis=1) + 1e-12))
    ok &= bool(np.all(np.linalg.norm(P + Q, axis=1) < np.linalg.norm(P, axis=1) + np.linalg.norm(Q, axis=1)))
check('l3', ok, 'l3 s7/s8: u.v <= |u||v| and |u+v| <= |u|+|v| (strict for random pairs)')
check('l3', close(np.linalg.norm([6, 3]), 3 * math.sqrt(5)), 'l3 quiz: equal lengths when v = 2u')
# correlation as a cosine and beta as a projection, against NumPy's own estimators
Ar, Br = np.array([2., -1, 3, 0, 1]), np.array([1., 0, 2, -2, 4])
a, b = Ar - Ar.mean(), Br - Br.mean()
cosab = a @ b / math.sqrt(a @ a * (b @ b))
check('l3', Ar.mean() == 1 and Br.mean() == 1 and a @ b == 7 and a @ a == 10 and b @ b == 20, 'l3 s9 demeaned vectors, 7, 10, 20')
check('l3', close(cosab, np.corrcoef(Ar, Br)[0, 1]) and abs(cosab - 0.495) < 0.0005, 'l3 s9 correlation 0.495 equals the corrcoef value')
check('l3', close(Ar @ Br / math.sqrt(Ar @ Ar * (Br @ Br)), 0.6197, 1e-4), 'l3 s9 raw slip 0.6197')
check('l3', close(a @ b / (a @ a), np.polyfit(Ar, Br, 1)[0]) and close(a @ b / (a @ a), 0.7), 'l3 s10 beta 0.7 is the regression slope of B on A')
ok = True
for _ in range(2000):  # the identities hold for any sample, sizes 3 to 40
    n = int(rng.integers(3, 41)); X, Y = rng.normal(size=n), rng.normal(size=n) * 2 + 0.3
    xd, yd = X - X.mean(), Y - Y.mean()
    ok &= close(xd @ yd / math.sqrt(xd @ xd * (yd @ yd)), np.corrcoef(X, Y)[0, 1]) and close(xd @ yd / (xd @ xd), np.polyfit(X, Y, 1)[0], 1e-8)
check('l3', ok, 'l3: correlation = cosine of demeaned vectors, beta = projection coefficient = OLS slope (2,000 samples)')

check('l4', close(np.dot([0.5, 0.3, 0.2], [0.10, 0.02, -0.04]), 0.048), 'l4 s0 return 4.8%')
check('l4', close(0.10 * 0.5 + 0.04 * 0.25 - 0.02 * 0.25, 0.055), 'l4 s1 slider 0.5 gives 5.5%')
check('l4', close(np.dot([0.2, 0.5, 0.3], [0.06, -0.02, 0.03]), 0.011), 'l4 s2 1.1%')
check('l4', close(np.dot([0.45, 0.35, 0.20], [0.04, 0.01, -0.05]), 0.0115), 'l4 s3 1.15%')
check('l4', close(np.dot([0.8, 0.5, -0.3], [0.05, 0.02, 0.06]), 0.032), 'l4 s4 3.2%')
check('l4', close(np.dot([0.9, 0.6, -0.5], [0.04, 0.02, 0.01]), 0.043) and close((0.6 * 0.04 + 0.4 * 0.02), 0.032), 'l4 s5 4.3% and rescaled slip')
check('l4', close(np.dot([0.9, 0.1], [0.02, 0.20]), 0.038) and close(np.dot([0.1, 0.9], [0.02, 0.20]), 0.182), 'l4 s6 3.8% and swap slip')
check('l4', close(np.dot([1200, -800, 500], [25.45 - 24.60, 12.40 - 12.80, 42.30 - 41.15]), 1915), 'l4 s9 P&L 1,915')
check('l4', close(np.dot([1.5, -0.5], [0.08, 0.03]), 0.105) and close(np.dot([100, -50], [2.10, 3.40]), 40), 'l4 quiz leverage 10.5% and P&L 40')
# review, homework, problems of level 1
check('L1', close(np.linalg.solve([[3, -1], [1, 2]], [3, 8]), [2, 3]), 'homework-1 weights (2, 3)')
X, Y = np.array([3., -1, 2, 0]), np.array([1., 2, -1, 2]); xd, yd = X - 1, Y - 1
check('L1', xd @ yd == -5 and close(np.corrcoef(X, Y)[0, 1], -5 / math.sqrt(60)) and close(xd @ yd / (xd @ xd), -0.5) and close(X @ Y / math.sqrt(X @ X * (Y @ Y)), -0.0845, 1e-4), 'homework-1 correlation -0.6455, beta -0.5, raw slip')
check('L1', close(np.dot([1.5, -0.5], [0.06, 0.04]), 0.07) and close(np.dot([2500, -1200, 800], [0.42, -0.15, -1.36]), 142), 'homework-1 long-short 7% and P&L 142')
check('L1', close(np.linalg.solve([[1, 0.2], [0.2, 1]], [0.8, 0.4]), [0.75, 0.25]) and close(np.dot([0.8, 0.4], [0.05, 0.01]), 0.044) and close(0.75 * 0.052 + 0.25 * 0.02, 0.044), 'homework-1 longform (a), (b)')
check('L1', close(math.degrees(math.acos(-6 / 10)), 126.87, 0.01) and close(np.dot([0.7, 0.6, -0.3], [0.04, -0.01, 0.05]), 0.007) and close(np.dot([2, -3, 1], [1.1, 0.6, -0.4]), 0) and close(np.dot([300, -200, 150], [-0.6, -1.1, 0.8]), 160), 'review-1 angle, return, neutral book, P&L')
l1a, l1b = 2 * np.array([4., 1]), 3 * np.array([1., 3])
check('L1', l1a @ l1b == 42 and round(math.degrees(math.acos(42 / math.sqrt(68 * 90)))) == 58 and close(math.sqrt(68) + math.sqrt(90) - math.sqrt(242), 2.18, 0.005), 'problems-1 robot: 42, 58 degrees, 2.18 m')
aw = np.array([0.4, 0.45, 0.15]) - np.array([0.5, 0.3, 0.2]); r = np.array([0.02, -0.01, 0.04])
check('L1', close(aw @ r, -0.0055) and close(np.linalg.norm(aw), 0.1871, 1e-4) and round(math.degrees(math.acos(aw @ r / np.linalg.norm(aw) / np.linalg.norm(r)))) == 130, 'problems-1 active bets')
w = np.array([-8., 1]); d = np.array([0.6, 0.8])
check('L1', close(w @ d, -4) and close(math.sqrt(w @ w - 16), 7) and close(math.sqrt(625 - 49), 24) and close(20 / (24 - 4) * 60, 60), 'problems-1 drone: -4, 7, 24, 60 minutes')
wf, c, s = np.array([0.6, 0.3, 0.1]), np.array([0.01, -0.12, 0.08]), np.array([-0.03, 0.04, -0.02]); wh = wf + 0.11 * np.array([0, -1, 1])
check('L1', close(wf @ c, -0.022) and close(wh @ c, 0) and close(wh @ s, -0.0146) and close(wh @ (c + s) / 2, -0.0073) and close(wf @ (c + s) / 2, -0.015), 'problems-1 stress hedge')

# ---------------------------------------------------------------------------------------------------------------
# Level 2: matrix times vector, transformations, products, identity, transpose
# ---------------------------------------------------------------------------------------------------------------
check('l5', close(np.array([[2, -1], [1, 2]]) @ [1, -1], [3, -1]) and close(np.array([[2, -1], [1, 2]]) @ [-1, 1], [-3, 1]) and close(np.array([[2, 1], [0, 1]]) @ [1, 2], [4, 2]), 'l5 s1, s4, s6 products')
check('l5', close(np.array([[1.2, 0.8], [0.6, -1.5], [1.5, -0.4]]) @ [1.5, -0.5], [1.4, 1.65, 2.45]), 'l5 s8 factor model returns')
R = lambda t: np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
S = lambda k: np.array([[1., k], [0, 1]])
check('l6', close(R(math.pi / 2), [[0, -1], [1, 0]]) and close(R(math.pi), -np.eye(2)), 'l6 quarter and half turn')
check('l6', close(S(1.5) @ [0, 2], [3, 2]) and close(np.array([[0.5, 0.5], [1, -1]]) @ [3, -1], [1, 4]), 'l6 s3 shear image, s9 factors (1, 4)')
# when a shear and a turn commute: only k = 0 or sin(theta) = 0 (the slider grid of l7 s1, then 100,000 random settings)
ok = True
for t in range(0, 181, 15):
    for k in np.arange(-1.5, 1.51, 0.5):
        same = close(R(math.radians(t)) @ S(k), S(k) @ R(math.radians(t)))
        ok &= same == (k == 0 or t in (0, 180))
for _ in range(100000):
    t, k = rng.uniform(0, 2 * math.pi), rng.uniform(-3, 3)
    ok &= not close(R(t) @ S(k), S(k) @ R(t)) or abs(k * math.sin(t)) < 1e-9
check('l7', ok, 'l7 s1: shear and turn commute only when k = 0 or the turn is 0 or 180 degrees')
# scalar multiples of I commute with everything; a non-scalar matrix fails to commute with some matrix (10,000 random)
ok = True
for _ in range(10000):
    M, c = rng.normal(size=(2, 2)), rng.normal()
    ok &= close(c * np.eye(2) @ M, M @ (c * np.eye(2)))
check('l7', ok, 'l7 s1 explain: a half turn (-I) commutes with any matrix')
A, B = np.array([[2, 1], [0, 3]]), np.array([[1, 4], [2, -1]])
check('l7', (A @ B).tolist() == [[4, 7], [6, -3]] and (B @ A)[0, 1] == 13, 'l7 s3 AB and the BA slip 13')
F, Rq = np.array([[1, 0], [0, -1]]), np.array([[0, -1], [1, 0]])
check('l7', (Rq @ F).tolist() == [[0, 1], [1, 0]] and (F @ Rq).tolist() == [[0, -1], [-1, 0]] and (Rq @ np.array([[1, 1], [0, 1]])).tolist() == [[0, -1], [1, 1]], 'l7 s0, s2, s5 products')
Lm, Mm = np.array([[1.1, 0.6], [1.3, -0.5]]), np.array([[2.0, -1.0], [0.5, 0.8]])
check('l7', close(Lm @ Mm, [[2.5, -0.62], [2.35, -1.7]]) and close((Mm @ Lm)[1, 1], -0.1), 'l7 s8 LM and the ML slip')
ok = True
for _ in range(5000):
    m, n, p = rng.integers(1, 5, 3); A_, B_ = rng.normal(size=(m, n)), rng.normal(size=(n, p))
    ok &= close((A_ @ B_).T, B_.T @ A_.T) and close((A_.T @ A_).T, A_.T @ A_)
check('l8', ok, 'l8: (AB)^T = B^T A^T and A^T A symmetric (5,000 random shapes)')
A, B = np.array([[1, 2], [0, 1]]), np.array([[1, 0], [3, 1]])
check('l8', (A @ B).tolist() == [[7, 2], [3, 1]] and (B.T @ A.T).tolist() == [[7, 3], [2, 1]] and (A.T @ B.T).tolist() == [[1, 3], [2, 7]] and (B @ A).tolist() == [[1, 2], [3, 7]], 'l8 s4, s5 matrices')
Sg = np.array([[0.04, 0.006], [0.006, 0.01]]); w = np.array([0.6, 0.4])
check('l8', close(w @ Sg @ w, 0.01888) and close(math.sqrt(w @ Sg @ w), 0.1374, 1e-4) and close(w @ np.array([[0.04, 0.3], [0.3, 0.01]]) @ w, 0.16), 'l8 s8 variance 0.01888, volatility 13.74%')
# portfolio variance formula against simulated returns (400,000 draws separate 0.01888 from the no-covariance 0.016)
sim = rng.multivariate_normal([0, 0], Sg, size=400000) @ w
check('l8', abs(sim.var() - 0.01888) < 0.0003, 'l8 s8: simulated portfolio variance matches w^T Sigma w')
w5 = np.array([0.5, 0.5]); S2 = np.array([[0.09, -0.009], [-0.009, 0.0225]])
check('L2', close(math.sqrt(w5 @ S2 @ w5), 0.1537, 1e-4), 'review-2 volatility 15.37%')
S3 = np.array([[0.0324, -0.0027], [-0.0027, 0.0036]]); w7 = np.array([0.7, 0.3])
check('L2', close(w7 @ S3 @ w7, 0.015066) and close(math.sqrt(w7 @ S3 @ w7), 0.1227, 1e-4) and close(np.linalg.matrix_power(R(math.radians(15)), 6), [[0, -1], [1, 0]]), 'homework-2 equity/bond 12.27%, six turns')
Bm = np.array([[1.1, 0.3], [0.9, -0.2], [1.4, 0.6]]); Fm = np.array([[0.0144, 0.003], [0.003, 0.0049]]); e = Bm.T @ [0.4, 0.35, 0.25]; e2 = e - 0.605 * np.array([1, 0.25])
check('L2', close(e, [1.105, 0.2]) and close(e2, [0.5, 0.04875]) and abs(e2 @ Fm @ e2 - 0.00376) < 1e-5 and abs(e @ Fm @ e - 0.01910) < 1e-5 and abs(1 - 0.00376 / 0.01910 - 0.803) < 5e-4, 'problems-2 factor risk')
Q = np.array([[0.5, 0.3], [0.1, 0.2], [0.05, 0.2]]); p = np.array([0.8, 1.5, 6.0])
check('L2', close(Q @ [40, 12], [23.6, 6.4, 4.4]) and close(p @ Q @ [40, 12], 54.88) and close(Q.T @ p, [0.85, 1.74]) and close(Q.T @ p @ [50, 20], 77.3), 'problems-2 bakery')
Rs = np.array([[0.8, -0.6], [0.6, 0.8]])
check('L2', close(Rs.T @ Rs, np.eye(2)) and close(Rs.T @ [11, 2], [10, -5]) and close(math.degrees(math.acos((Rs @ [0, 10])[0] / 10)), 126.87, 0.01), 'problems-2 site plan')

# ---------------------------------------------------------------------------------------------------------------
# Level 3: systems, inverses, singular matrices, NumPy
# ---------------------------------------------------------------------------------------------------------------
G = np.array([[0.50, 0.25], [0.20, 0.30]])
check('l10', close(np.linalg.inv(G), [[3, -2.5], [-2, 5]]) and close(np.linalg.solve(G, [200, 150]), [225, 350]) and close(np.linalg.solve(G, [0, 60]), [-150, 300]) and close(np.linalg.solve(G, [100, 100]), [50, 300]), 'l10 s9, s10 and review-3 hedges')
ok = True
for _ in range(5000):
    a, b, c, d = rng.normal(size=4)
    if abs(a * d - b * c) < 1e-3: continue
    M = np.array([[a, b], [c, d]]); N = rng.normal(size=(2, 2))
    ok &= close(np.linalg.inv(M), np.array([[d, -b], [-c, a]]) / (a * d - b * c), 1e-7) and close(np.linalg.inv(M @ N), np.linalg.inv(N) @ np.linalg.inv(M), 1e-5)
check('l10', ok, 'l10: the 2 by 2 inverse rule and (AB)^-1 = B^-1 A^-1 (5,000 random matrices)')
# determinant = signed area factor of the unit square's image (shoelace), 20,000 random matrices
ok = True
for _ in range(20000):
    M = rng.normal(size=(2, 2)); P = np.array([[0, 0], [1, 0], [1, 1], [0, 1.]]) @ M.T
    area = 0.5 * sum(P[i, 0] * P[(i + 1) % 4, 1] - P[(i + 1) % 4, 0] * P[i, 1] for i in range(4))
    ok &= close(area, np.linalg.det(M))
check('l11', ok, 'l11: det A is the signed area of the image of the unit square')
check('l11', all(close(abs(2 - k), abs(np.linalg.det(np.array([[2, 1], [k, 1.]])))) for k in np.arange(-1, 4.01, 0.25)), 'l11 s0/s1 caption: area |2 - k|')
check('l11', close(0.50 * 0.24 - 0.60 * 0.20, 0) and close(np.array([0.6, 0.4]) @ np.full((2, 2), 0.0625) @ [0.6, 0.4], 0.0625), 'l11 s9, s10')
# l12 floating-point claims (this interpreter; BUILD marks values that depend on the BLAS/LAPACK build)
check('l12', repr(float(np.linalg.det(np.array([[2, 3], [1, 4]])))) == '5.000000000000001', 'l12 s1 console: det prints 5.000000000000001 (BUILD: same under Pyodide 0.27.7)')
n = 10; Hb = np.array([[1 / (i + j + 1) for j in range(n)] for i in range(n)]); bb = Hb @ np.ones(n)
r1 = np.abs(Hb @ np.linalg.solve(Hb, bb) - bb).max(); r2 = np.abs(Hb @ (np.linalg.inv(Hb) @ bb) - bb).max()
check('l12', r1 < 1e-14 and 1e-6 < r2 < 1e-3, f'l12 s5 console: residuals {r1:.1e} (solve) and {r2:.1e} (inv); the page prints 4.4e-16 and 5.2e-05 (BUILD)')
# solve beats inv on the residual: 300 random ill-conditioned systems (condition 1e8 to 1e13), right-hand sides from a known x
wins = 0
for _ in range(300):
    n = int(rng.integers(6, 16)); U, _r = np.linalg.qr(rng.normal(size=(n, n))); V, _r = np.linalg.qr(rng.normal(size=(n, n)))
    M = U @ np.diag(np.logspace(0, -rng.uniform(8, 13), n)) @ V.T; bvec = M @ rng.normal(size=n)
    wins += np.abs(M @ np.linalg.solve(M, bvec) - bvec).max() < np.abs(M @ (np.linalg.inv(M) @ bvec) - bvec).max()
check('l12', wins >= 285, f'l12 s5: solve leaves the smaller residual in {wins} of 300 ill-conditioned systems')
print(f'note: solve had the smaller residual in {wins} of 300 systems')
import time
M = rng.normal(size=(300, 300)); bvec = rng.normal(size=300); ts, ti = [], []
for _ in range(7):  # best of 7 batches of 40 calls each, after a warm-up call
    np.linalg.solve(M, bvec); np.linalg.inv(M)
    t0 = time.perf_counter(); [np.linalg.solve(M, bvec) for _ in range(40)]; ts.append(time.perf_counter() - t0)
    t0 = time.perf_counter(); [np.linalg.inv(M) @ bvec for _ in range(40)]; ti.append(time.perf_counter() - t0)
ratio = min(ti) / min(ts)
check('l12-timing', ratio > 1.2, f'l12 s5 (TIMING-DEPENDENT): inv(A) @ b takes {ratio:.1f} times as long as solve at n = 300 (best of 7 batches)')
# the operation count behind "about three times the arithmetic": multiplications and divisions, counted term by term
def mults(n):
    lu = sum((n - k - 1) + (n - k - 1) ** 2 for k in range(n))            # factorise
    one = sum(i for i in range(n)) + sum(n - i for i in range(n))            # one forward and one back substitution
    fwd_unit = sum(sum(i - j for i in range(j + 1, n)) for j in range(n))    # forward substitution on e_j skips its leading zeros
    back = n * sum(n - i for i in range(n))                                  # n full back substitutions
    return lu + one, lu + fwd_unit + back + n * n                            # solve; inverse, then the product with b
ms, mi = mults(400)
check('l12', 2.9 < mi / ms < 3.1, f'l12 s5: inv(A) @ b costs {mi / ms:.2f} times the multiplications of solve at n = 400 (n^3 against n^3/3)')
G3 = np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]])
check('l12', close(G3 @ [200, 300, 100], [235, 140, 19]) and close(np.linalg.solve(G3, [0, 100, 0]), [-250, 500, 0], 1e-6) and close(np.linalg.solve(G3, [100, 50, 5]), [2500, -1000, -1500], 1e-6) and close(np.linalg.solve([[1, 0.5, 0.4], [0, 0.2, 0.3], [0, 0.01, 0.04]], [300, 120, 9]), [42, 420, 120], 1e-6), 'l12 s0, s8 test values')
check('l12', abs(np.linalg.det(G3 * 1e-4) - 2e-16) < 1e-18 and np.linalg.matrix_rank(G3 * 1e-4) == 3, 'l12 s9 test 6: scaled hedge has determinant 2e-16 and rank 3')
T7 = np.array([[0.04, 0.06], [0.06, 0.09]])
check('l12', 0 < abs(np.linalg.det(T7)) < 1e-17 and np.linalg.matrix_rank(T7) == 1 and np.all(np.isfinite(np.linalg.solve(T7, [1., 1]))) and np.abs(np.linalg.solve(T7, [1., 1])).max() > 1e15, 'l12 s9 test 7: det near 4e-19, rank 1, solve returns huge finite numbers')
raised = False
try:
    np.linalg.solve(np.array([[0.50, 0.25, 0.75], [0.20, 0.30, 0.50], [0.04, 0.02, 0.06]]), [235., 140, 19])
except np.linalg.LinAlgError:
    raised = True
check('l12', raised, 'l12 s9 prose: desktop NumPy raises LinAlgError for the P, Q, T matrix (BUILD: Pyodide returns nan)')
# a healthy daily covariance matrix of four assets has a determinant near 1e-16
vd = np.array([0.01, 0.012, 0.015, 0.02]); V4 = np.outer(vd, vd) * (np.full((4, 4), 0.3) + 0.7 * np.eye(4))
check('l12', 1e-16 < np.linalg.det(V4) < 1e-15 and abs(np.linalg.det(V4) - 8.446e-16) < 1e-18 and np.linalg.matrix_rank(V4) == 4, 'l12 s9 explain and homework-3 test 8: determinant about 8e-16, rank 4')
# minimum-variance weights: Sigma^-1 1 normalised minimises w^T Sigma w among fully invested mixes (50,000 random mixes each)
ok = True
for Sm in ([[0.04, 0.03], [0.03, 0.09]], [[0.04, -0.02], [-0.02, 0.09]], [[0.04, 0.006, 0.002], [0.006, 0.09, 0.012], [0.002, 0.012, 0.0225]], V4):
    Sm = np.array(Sm); z = np.linalg.solve(Sm, np.ones(len(Sm))); ws = z / z.sum()
    W = rng.normal(size=(50000, len(Sm))); W = W / W.sum(1, keepdims=True)
    ok &= bool(np.all(np.einsum('ij,jk,ik->i', W, Sm, W) >= ws @ Sm @ ws - 1e-15))
check('L3', ok, 'homework-3 h-min-var: the formula gives the minimum-variance fully invested mix')
check('L3', close(np.linalg.solve([[0.04, 0.03], [0.03, 0.09]], [1, 1]) / np.linalg.solve([[0.04, 0.03], [0.03, 0.09]], [1, 1]).sum(), [6 / 7, 1 / 7]), 'homework-3 test 2 weights')
C = np.array([[5, 5, 5, 105], [100, 0, 0, 0], [3.5, 103.5, 0, 0], [4.25, 4.25, 104.25, 0.]]); dd = np.linalg.solve(C, [101.2, 96.5, 99.3, 100.15])
check('L3', close(dd, [0.965, 0.926787439613527, 0.883548233876667, 0.831650682214753]) and close([6 * dd.sum() + 100 * dd[3], 100 * dd[3], 102 * dd[0]], [104.806986355705, 83.1650682214753, 98.43]), 'homework-3 bond curve, four-year case')
check('L3', close(np.linalg.solve([[0.40, 0.25], [0.16, 0.30]], [200, 100]), [437.5, 100]) and close(np.linalg.solve([[0.2, 0.1], [0.4, 0.7]], [10, 40]), [30, 40]) and close(np.linalg.solve([[12, 8], [3, 5]], [64, 22]), [4, 2]), 'homework-3 longform (e), problems-3 feed and paint')
Cc = np.array([[2, 0], [0, 1]]) @ np.array([[0.7, 0.2], [0.1, 0.6]])
check('L3', close(Cc, [[1.4, 0.4], [0.1, 0.6]]) and close(np.linalg.det(Cc), 0.8) and close(np.linalg.inv(Cc), [[0.75, -0.5], [-0.125, 1.75]]) and close(np.linalg.solve(Cc, [200, 60]), [120, 80]), 'problems-3 sensor')
kk = 1; Ck = np.array([[2, kk], [1, 1]]) @ np.array([[3, 1], [2, 1]])
check('L3', Ck.tolist() == [[8, 3], [5, 2]] and close(np.linalg.solve(Ck, [19, 12]), [2, 1]), 'problems-3 engraver')

# ---------------------------------------------------------------------------------------------------------------
# Findings: each check below fails while its finding is open
# ---------------------------------------------------------------------------------------------------------------
l6, l7, l10, l12, hw3 = J('l6-moving-the-plane'), J('l7-one-after-another'), J('l10-undoing'), J('l12-numpy-matrices'), J('homework-3')


def run_tests(widget, src):
    """The widget's hidden tests against `src` in CPython; returns the 1-based number of the first failing test, or 0."""
    for i, t in enumerate(widget['tests'], 1):
        env = {'np': np}
        try:
            exec(src, env)
            if t.get('setup'):
                exec(t['setup'], env)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], env)
                    return i
                except Exception as ex:  # noqa: BLE001
                    if type(ex).__name__ != t['expect']:
                        return i
                continue
            got = eval(t['call'], env)
        except Exception:  # noqa: BLE001
            return i
        if t.get('compare') == 'isclose':
            if not np.allclose(np.array(got, dtype=float), np.array(eval(t['expect']), dtype=float), atol=t.get('tol', {}).get('abs', 1e-9), rtol=0):
                return i
        elif repr(got) != t['expect'] and str(got) != t['expect']:
            return i
    return 0


# Finding 1: l12 screens[2] accepts an exact comparison with np.linalg.inv(A)
w2 = l12['screens'][2]['widget']
exact = 'import numpy as np\n\ndef is_inverse(A, B):\n    A = np.array(A, dtype=float)\n    B = np.array(B, dtype=float)\n    return bool((B == np.linalg.inv(A)).all())\n'
check('F1', run_tests(w2, w2['solution']) == 0, 'l12 screens[2]: the authored solution passes its tests in CPython')
exec(exact, (envx := {}))
check('F1', not envx['is_inverse']([[2, 3], [1, 4]], [[0.8, -0.6], [-0.2, 0.4]]), 'the exact comparison returns False for the true inverse of [[2, 3], [1, 4]] in decimals (inv gives -0.6000000000000001)')
check('F1', run_tests(w2, exact) != 0, 'FINDING 1: l12 screens[2] hidden tests pass `(B == np.linalg.inv(A)).all()`, an exact comparison that rejects a true inverse')

# Finding 2: l6 screens[1] has two options that are quarter turns
def mat(tex):
    m = re.search(r'begin\{pmatrix\}(.*?)\\end\{pmatrix\}', tex, re.S)
    return np.array([[float(x.replace(' ', '')) for x in row.split('&')] for row in m.group(1).split('\\\\')])
s1 = l6['screens'][1]
quarter = [o['id'] for o in s1['widget']['options'] if any(close(mat(o['text']), R(t)) for t in (math.pi / 2, -math.pi / 2))]
check('F2', len(quarter) == 1 or 'anticlockwise' in s1['question'], f'FINDING 2: l6 screens[1] asks for "a quarter turn" and options {quarter} are both quarter turns; the question does not say anticlockwise')

# Finding 3: l6 screens[5] "turn" why refutes only the anticlockwise quarter turn
Mswap = np.array([[0., 1], [1, 0]])
why = next(o['why'] for o in l6['screens'][5]['widget']['options'] if o['id'] == 'turn')
check('F3', close(R(-math.pi / 2) @ [0, 1], Mswap @ [0, 1]) and not close(R(-math.pi / 2), Mswap), 'a clockwise quarter turn also sends e2 to (1, 0), as M does, but is not M')
check('F3', 'clockwise' in why, 'FINDING 3: l6 screens[5] option "turn": "A quarter turn sends e2 to (-1, 0)" holds only anticlockwise; the clockwise one sends e2 to (1, 0)')

# Finding 4: l7 screens[1] "same shape": at 90 degrees the two images are congruent
def sides(Mx):
    a, b = Mx[:, 0], Mx[:, 1]
    return sorted([round(float(np.linalg.norm(a)), 9), round(float(np.linalg.norm(b)), 9)]), round(abs(float(a @ b)), 9), round(abs(float(np.linalg.det(Mx))), 9)
t90 = math.pi / 2
congruent = sides(R(t90) @ S(1)) == sides(S(1) @ R(t90)) and not close(R(t90) @ S(1), S(1) @ R(t90))
q4 = l7['screens'][1]['question']
check('F4', not (congruent and 'same shape' in q4), 'FINDING 4: l7 screens[1] asks when the orders "give the same shape"; at its start state (90 degrees, k = 1) the two parallelograms are congruent, in different places')

# Finding 5: l12 screens[8] test-3 line
t3 = l12['screens'][8]['feedback']['byKey']['test-3']
ratios = G3[2] / G3[0]
check('F5', 0.079 < ratios.min() and ratios.max() < 0.084 and 5 / 100 < ratios.min(), 'every option has gamma between 0.080 and 0.0834 of its delta; the test-3 target has 0.05')
check('F5', 'little delta' not in t3, 'FINDING 5: l12 screens[8] test-3 line says "a small gamma target with little delta"; the trades are large because gamma is small for that much delta')

# Finding 6: homework-3 h-min-var accepts an exact == 0 test on a hand determinant
mv = next(i for i in hw3['items'] if i['id'] == 'h-min-var')['widget']
hand = ('import numpy as np\n\ndef min_var_weights(cov):\n    S = np.array(cov, dtype=float)\n    ones = np.ones(len(S))\n'
        '    if S[0, 0] * S[1, 1] - S[0, 1] * S[1, 0] == 0:\n        raise np.linalg.LinAlgError("singular")\n    z = np.linalg.solve(S, ones)\n    return z / z.sum()\n')
check('F6', run_tests(mv, mv['solution']) == 0, 'homework-3 h-min-var: the authored solution passes its tests in CPython')
Z = np.array([[0.04, 0.044], [0.044, 0.0484]])
check('F6', 0.04 * 0.0484 - 0.044 * 0.044 != 0 and np.linalg.det(Z) != 0 and np.linalg.matrix_rank(Z) == 1, 'proposed test matrix [[0.04, 0.044], [0.044, 0.0484]]: rank 1, hand and LAPACK determinants both non-zero')
check('F6', run_tests(mv, hand) != 0, 'FINDING 6: homework-3 h-min-var hidden tests pass a hand `ad - bc == 0` test (both singular tests are 2 by 2 and cancel exactly)')
check('F6', 'rounding' in mv_line if (mv_line := next(i for i in hw3['items'] if i['id'] == 'h-min-var')['feedback']['byKey']['test-7'].lower()) else False, 'FINDING 6: homework-3 h-min-var test-7 line gives "det = 0.0036 - 0.0036" to a learner whose `np.linalg.det(S) == 0` failed because the computed value is 4e-19')

# Finding 7: l7 screens[0] "turn-first" region fires for either arrow but names e2
w0 = l7['screens'][0]['widget']
reg = next(w for w in w0['wrong'] if w['id'] == 'turn-first')
line = l7['screens'][0]['feedback']['byKey']['turn-first']
check('F7', 'point' in reg or 'For $\\mathbf{e}_1$' in line or 'e_1' in line, 'FINDING 7: l7 screens[0] region turn-first matches either arrow (drag-point.js tests every point), yet its line says "you turned e2 first"')

# Finding 8: l10 screens[0] "on-target" region holds nine snap points, eight of them off T
w10 = l10['screens'][0]; rg = next(w for w in w10['widget']['wrong'] if w['id'] == 'on-target')['region']; snap = w10['canvas']['params']['snap']
pts = [(xx, yy) for xx in np.arange(-1, 8.01, snap) for yy in np.arange(-1, 8.01, snap) if rg['x'][0] <= xx <= rg['x'][1] and rg['y'][0] <= yy <= rg['y'][1]]
check('F8', len(pts) == 1, f'FINDING 8: l10 screens[0] region on-target holds {len(pts)} snap points; "You put u itself on T ... to (12, 18)" is true at (6, 6) only')

# Finding 9: `error` lines describe an unreplaced `...`, which never produces the key `error`
starters_error = 0
for scr in (0, 3, 8):
    wdg = l12['screens'][scr]['widget']
    try:
        exec(wdg['starter'], {})  # loads without error: the page then reports test-1, not error
    except Exception:  # noqa: BLE001
        starters_error += 1
lines9 = [l12['screens'][i]['feedback']['byKey']['error'] for i in (0, 2, 3, 8, 9)]
check('F9', starters_error == 0, 'the starters load cleanly, so an unreplaced `...` gives key test-1')
check('F9', not any('Replace the `...`' in x or 'order of the arguments' in x for x in lines9), 'FINDING 9: l12 `error` lines tell the learner to replace the `...` or reorder arguments; the key fires only when the code fails to load')

# fluency-l5 taller-columns: the two slips coincide in under 0.01% of draws (enumerated in the audit scratch; a 300,000-draw sample here)
hit = tot = 0
while tot < 300000:
    a, b, c, d, e_, f = rng.integers(-4, 5, 6); x1, x2 = rng.choice([-3, -2, -1, 1, 2, 3], 2)
    if x1 == x2 or (a == b and c == d and e_ == f) or (a == 0 and c == 0 and e_ == 0) or (b == 0 and d == 0 and f == 0): continue
    rr = (a * x1 + b * x2, c * x1 + d * x2, e_ * x1 + f * x2); nn = (a + b, c + d, e_ + f)
    if nn == rr: continue
    tot += 1; hit += (a * x2 + b * x1, c * x2 + d * x1, e_ * x2 + f * x1) == nn
check('fluency', hit / tot < 0.001, f'fluency-l5 taller-columns: amounts-swapped equals added-columns in {hit} of {tot} draws')

if '--pyodide' in sys.argv:
    pk = sys.argv[sys.argv.index('--pyodide') + 1]
    out = subprocess.run(['node', os.path.join(HERE, 'vectors-L1-3-concepts-r2-sweep.mjs'), ROOT, pk], capture_output=True, text=True)
    tail = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else out.stderr[-300:]
    print('pyodide sweep:', tail)
    check('pyodide', out.returncode == 0, 'Pyodide sweep: every byKey line and mutant behaves as the audit recorded')

open_findings = sorted({t for t, _ in fails if t.startswith('F')})
print(f'{passed} checks passed, {len(fails)} failed; open findings: {", ".join(open_findings) or "none"}')
sys.exit(1 if fails else 0)
