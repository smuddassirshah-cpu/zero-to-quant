"""Concept checks for the blind audit of `vectors` levels 1 to 3 (audit vectors-1-3, round 1).

Each check names the ledger rows it backs (docs/reports/audit-vectors-1-3-ledger.md). The script exits 0 only when
every check passes. A check that fails because the content is wrong stays failing: see the audit findings.
Fix pass (docs/reviews/audit-vectors-1-3.md): the two checks that encoded the old text of findings 1 and 2 ("L3:q3", "L3:numpy l12
s2 test 3") are re-pointed to the fixed text, and checks for the hidden tests added under findings 3 and 4 are added. NOTE lines
for findings fixed in the pass say so; they still print, so the run shows what was imprecise before.
NOTE lines record imprecise content that is not false as stated; they do not fail the run.

Run: python docs/reports/vectors-L1-3-concepts.py   (NumPy only; written against NumPy 2.5, the page runs 2.0.2)
The code-widget feedback sweep under the page's Pyodide is docs/reports/vectors-L1-3-concepts-sweep.mjs.
"""
import itertools
import math
import sys

import numpy as np

rng = np.random.default_rng(20261126)
FAILS, NOTES, N = [], [], 0


def check(name, ok, detail=""):
    global N
    N += 1
    if not ok:
        FAILS.append(name)
    print(("ok   " if ok else "FAIL ") + name + ((" | " + detail) if detail and not ok else ""))


def note(name, text):
    NOTES.append(name)
    print("NOTE " + name + " | " + text)


def close(a, b, tol=1e-9):
    return bool(np.allclose(a, b, atol=tol, rtol=0))


def R(deg):
    t = math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


def angle(u, v):
    u, v = np.array(u, float), np.array(v, float)
    return math.degrees(math.acos(u @ v / (np.linalg.norm(u) * np.linalg.norm(v))))


# ------------------------------------------------------------------ Level 1
# L1:span  two arrows reach the whole plane exactly when neither is a multiple of the other (l1 s5, s6, q1, q3; review-1 i2)
def spans(u, v):
    return abs(u[0] * v[1] - u[1] * v[0]) > 1e-12


def multiple(u, v):  # one is a multiple of the other (zero vector included)
    return np.linalg.matrix_rank(np.array([u, v], float)) < 2


ok = True
for u in itertools.product(range(-3, 4), repeat=2):
    for v in itertools.product(range(-3, 4), repeat=2):
        ok &= spans(u, v) == (not multiple(u, v))
check("L1:span every integer pair in [-3, 3]: spans the plane iff not multiples", ok)
check("L1:span l1 s6 keys", spans((1, 2), (2, 1)) and spans((1, 0), (0, -3)) and not spans((1, 2), (-2, -4)) and not spans((3, 6), (1, 2)))
check("L1:span l1 q1, q3, review-1 i2 keys", not spans((1, -2), (-3, 6)) and spans((1, 0), (0, 1)) and spans((1, 1), (1, -1)) and spans((2, 3), (3, 2))
      and not spans((2, -1), (-6, 3)) and spans((2, -1), (1, 2)) and spans((1, 0), (1, 1)) and spans((3, 1), (1, 3)))
# l1 s7 general weights a = (2x - y)/3, b = (2y - x)/3 for u = (2, 1), v = (1, 2)
ok = True
for _ in range(2000):
    x, y = rng.uniform(-9, 9, 2)
    a, b = (2 * x - y) / 3, (2 * y - x) / 3
    ok &= close(a * np.array([2, 1]) + b * np.array([1, 2]), [x, y])
check("L1:weights l1 s7 formulas reach every (x, y)", ok)
check("L1:weights l1 s8, homework-1 i8 fund weights", close(0.6 * np.array([1, .2]) + 0.4 * np.array([.2, 1]), [.68, .52]) and close(0.75 * np.array([1, .2]) + 0.25 * np.array([.2, 1]), [.8, .4]))

# L1:sign  sign of the dot product follows the angle (l2 s0, s4, s6, q1; summary)
ok = True
for _ in range(100000):
    d = rng.integers(2, 6)
    u, v = rng.normal(size=d), rng.normal(size=d)
    th = angle(u, v)
    ok &= (u @ v > 0) == (th < 90)
check("L1:sign 100,000 random pairs in 2 to 5 dimensions: dot > 0 iff angle < 90", ok)
u = np.array([2, 1])
neg = [n for n, v in dict(p=(-1, 3), q=(1, -3), r=(-2, 1), s=(2, -1), t=(-1, -2)).items() if u @ np.array(v) < 0]
check("L1:sign l2 s4 key q, r, t", neg == ["q", "r", "t"])

# L1:cs  Cauchy-Schwarz and "pointing along u gives the biggest score for its length" (l2 s0 explain, l3 s8 explain)
ok = True
for _ in range(100000):
    d = rng.integers(2, 7)
    u, v = rng.normal(size=d), rng.normal(size=d)
    ok &= abs(u @ v) <= np.linalg.norm(u) * np.linalg.norm(v) * (1 + 1e-12)
check("L1:cs |u.v| <= |u||v| on 100,000 random pairs", ok)
u = np.array([3., 1.])
best = max((u @ (2 * np.array([math.cos(t), math.sin(t)])), t) for t in np.linspace(0, 2 * math.pi, 7201))
check("L1:cs among arrows of length 2 the score with u = (3, 1) peaks along u", abs(best[1] - math.atan2(1, 3)) < 1e-3)

# L1:dist  dot products spread over sums (l2 s7; homework-1 i8; problems-1 i1, i3)
ok = True
for _ in range(20000):
    u, v, w = rng.normal(size=(3, 4))
    ok &= close(u @ (v + w), u @ v + u @ w) and close(u @ v, v @ u)
check("L1:dist u.(v + w) = u.v + u.w and u.v = v.u", ok)

# L1:tri  triangle inequality and its equality case (l3 s7, summary trap, q3)
ok, eq_only_same_way = True, True
for _ in range(50000):
    u, v = rng.normal(size=(2, 3))
    lhs, rhs = np.linalg.norm(u + v), np.linalg.norm(u) + np.linalg.norm(v)
    ok &= lhs <= rhs + 1e-12
    eq_only_same_way &= lhs < rhs - 1e-9  # random arrows never point exactly the same way
    k = rng.uniform(0.1, 5)
    ok &= close(np.linalg.norm(u + k * u), np.linalg.norm(u) + np.linalg.norm(k * u))
    ok &= np.linalg.norm(u - k * u) < np.linalg.norm(u) + np.linalg.norm(k * u) - 1e-9
check("L1:tri |u + v| <= |u| + |v|; equal for positive multiples, strict for opposite or non-parallel arrows", ok and eq_only_same_way)
z = np.zeros(2)
if close(np.linalg.norm(np.array([3., 4.]) + z), 5 + 0):
    note("L1:tri-zero", "equality also holds when one arrow is the zero vector, which points no way (finding 9; fixed: l3 s7 and the trap now add 'or one of them is zero')")

# L1:angle  cosine formula against the cosine rule and atan2 (l3 s3, s4, s8, q2; review-1 i5; problems-1 i0, i1)
ok = True
for _ in range(50000):
    u, v = rng.normal(size=(2, 2))
    a1 = angle(u, v)
    a2 = abs(math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u @ v)))
    lu, lv, lw = np.linalg.norm(u), np.linalg.norm(v), np.linalg.norm(u - v)
    a3 = math.degrees(math.acos((lu ** 2 + lv ** 2 - lw ** 2) / (2 * lu * lv)))
    ok &= abs(a1 - a2) < 1e-6 and abs(a1 - a3) < 1e-6 and 0 <= a1 <= 180
check("L1:angle formula = cosine rule = atan2 angle, always in [0, 180]", ok)
check("L1:angle keys 45, 135, 126.87, 58, 130", abs(angle((1, 2), (3, 1)) - 45) < 1e-9 and abs(angle((1, 0), (-1, 1)) - 135) < 1e-9 and abs(angle((1, 2), (2, -4)) - 126.87) < 0.005
      and round(angle((8, 2), (3, 9))) == 58 and round(angle((-.1, .15, -.05), (.02, -.01, .04))) == 130)
note("L1:angle-domain", "the formula needs non-zero arrows and gives an angle in [0, 180]; the lesson stated neither (finding 8; fixed in l3 summary note and s8 line c4)")

# L1:proj  projection k = u.v / v.v, residual perpendicular, closest point on the line (l3 s5, s6, summary; review-1 i6; homework-1 i7; fluency)
ok = True
for _ in range(50000):
    d = rng.integers(2, 5)
    u, v = rng.normal(size=(2, d))
    k = (u @ v) / (v @ v)
    ok &= abs((u - k * v) @ v) < 1e-9
    ok &= np.linalg.norm(u - k * v) <= np.linalg.norm(u - (k + rng.normal()) * v)
check("L1:proj residual perpendicular to v and kv is the nearest multiple of v", ok)
check("L1:proj l3 s5 (4, 2), s6 k = 1.2 and length 6, review-1 i6 (1, 3)", close(10 / 5 * np.array([2, 1]), [4, 2]) and close((np.array([2, 6]) @ np.array([3, 4])) / 25, 1.2)
      and close(np.linalg.norm(1.2 * np.array([3, 4])), 6) and close((np.array([4, 2]) @ np.array([1, 3])) / 10 * np.array([1, 3]), [1, 3]))

# L1:corr  correlation is the cosine of the centred vectors; beta is the projection coefficient and the regression slope (l3 s9, s10; homework-1 i3, i4)
ok = True
for _ in range(5000):
    n = rng.integers(4, 30)
    x, y = rng.normal(size=(2, n))
    a, b = x - x.mean(), y - y.mean()
    ok &= close(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)), np.corrcoef(x, y)[0, 1])
    ok &= close(a @ b / (a @ a), np.polyfit(x, y, 1)[0], 1e-8)
check("L1:corr cosine of centred vectors = np.corrcoef; a.b/a.a = least-squares slope with intercept (5,000 samples)", ok)
A_, B_ = np.array([2., -1, 3, 0, 1]), np.array([1., 0, 2, -2, 4])
a, b = A_ - 1, B_ - 1
check("L1:corr l3 s9 0.495, raw slip 0.6197, s10 beta 0.7 and slips 0.35, 2.2136", close(a @ b / math.sqrt((a @ a) * (b @ b)), 7 / math.sqrt(200)) and abs(A_ @ B_ / math.sqrt((A_ @ A_) * (B_ @ B_)) - .6197) < 5e-5
      and close(a @ b / (a @ a), .7) and close(a @ b / (b @ b), .35) and abs(a @ b / math.sqrt(a @ a) - 2.2136) < 5e-5)
X_, Y_ = np.array([3., -1, 2, 0]), np.array([1., 2, -1, 2])
x, y = X_ - 1, Y_ - 1
check("L1:corr homework-1 i3 -0.6455, raw -0.0845, i4 beta -0.5", abs(np.corrcoef(X_, Y_)[0, 1] + .6455) < 5e-5 and abs(X_ @ Y_ / math.sqrt((X_ @ X_) * (Y_ @ Y_)) + .0845) < 5e-5 and close(x @ y / (x @ x), -.5))

# L1:port  portfolio return = weights . simple returns, weights as shares of own money (l4 s0 to s9; review-1 i7; homework-1 i5)
ok, log_differs = True, False
for _ in range(20000):
    n = rng.integers(2, 6)
    V = rng.uniform(1e3, 1e6)
    w = rng.normal(size=n)
    w = w / w.sum() if abs(w.sum()) > 0.2 else np.ones(n) / n  # shorts and leverage allowed, weights sum to 1
    r = rng.uniform(-.3, .3, n)
    end = (V * w * (1 + r)).sum()
    ok &= close(end / V - 1, w @ r)
    if n >= 2 and abs(w @ np.log1p(r) - math.log(max(end / V, 1e-12))) > 1e-6:
        log_differs = True
check("L1:port w.r equals (end value - start value) / start value for random long, short and leveraged books", ok)
check("L1:port the identity is for simple returns: weights dotted with log returns do not give the log return", log_differs)
check("L1:port l4 keys 4.8%, 5.5%, 1.1%, 1.15%, 3.2%, 4.3%, 3.8%, q2 10.5%, homework-1 i5 7%", all(close(a, b) for a, b in [
    (np.array([.5, .3, .2]) @ np.array([.1, .02, -.04]), .048), (np.array([.5, .25, .25]) @ np.array([.1, .04, -.02]), .055), (np.array([.2, .5, .3]) @ np.array([.06, -.02, .03]), .011),
    (np.array([.45, .35, .2]) @ np.array([.04, .01, -.05]), .0115), (np.array([.8, .5, -.3]) @ np.array([.05, .02, .06]), .032), (np.array([.9, .6, -.5]) @ np.array([.04, .02, .01]), .043),
    (np.array([.9, .1]) @ np.array([.02, .2]), .038), (np.array([1.5, -.5]) @ np.array([.08, .03]), .105), (np.array([1.5, -.5]) @ np.array([.06, .04]), .07)]))
check("L1:port leverage in pounds: l4 s5 430 on 10,000; homework-1 i5 1,400 on 20,000", close(9000 * .04 + 6000 * .02 - 5000 * .01, 430) and close(30000 * .06 - 10000 * .04, 1400))
check("L1:pnl q.dp keys 1915, 40, 160, 142", close(np.array([1200, -800, 500]) @ np.array([.85, -.40, 1.15]), 1915) and close(np.array([100, -50]) @ np.array([2.1, 3.4]), 40)
      and close(np.array([300, -200, 150]) @ np.array([-.6, -1.1, .8]), 160) and close(np.array([2500, -1200, 800]) @ np.array([8.78 - 8.36, 15.05 - 15.20, 32.54 - 33.90]), 142, 1e-6))
check("L1:expo exposures 1.8, -0.3, 0 (market neutral)", close(np.array([4, 2, -5]) @ np.array([1.2, .5, .8]), 1.8) and close(np.array([3, -2]) @ np.array([.9, 1.5]), -.3) and close(np.array([2, -3, 1]) @ np.array([1.1, .6, -.4]), 0))
# problems-1
check("L1:p1 robot: (2, 3), 42, straight line 2.18 m shorter; drone: -4, 7, 24, 60 min", close(np.linalg.solve([[4, 1], [1, 3]], [11, 11]), [2, 3]) and close(np.array([8, 2]) @ np.array([3, 9]), 42)
      and abs(math.sqrt(68) + math.sqrt(90) - math.sqrt(242) - 2.18) < .005 and close(np.array([-8, 1]) @ np.array([.6, .8]), -4) and close(math.sqrt(65 - 16), 7) and close(math.sqrt(625 - 49), 24) and close(20 / (24 - 4) * 60, 60))
w_, c_, s_ = np.array([.6, .3, .1]), np.array([.01, -.12, .08]), np.array([-.03, .04, -.02])
w2 = np.array([.6, .19, .21])
check("L1:p1 fund: active -0.55%, |a| 0.1871; scenarios -2.2%, h = 0.11, -1.46%, -0.73%", close((np.array([.4, .45, .15]) - np.array([.5, .3, .2])) @ np.array([.02, -.01, .04]), -.0055) and abs(math.sqrt(.035) - .1871) < 5e-5
      and close(w_ @ c_, -.022) and close(w2 @ c_, 0) and close(w2 @ s_, -.0146) and close(w2 @ (c_ + s_) / 2, -.0073))

# ------------------------------------------------------------------ Level 2
# L2:views  Ax as a combination of columns = rows dotted with x; A e_j is column j; m x n takes n entries to m (l5)
ok = True
for _ in range(20000):
    m, n = rng.integers(1, 5, 2)
    A, x = rng.normal(size=(m, n)), rng.normal(size=n)
    ok &= close(A @ x, sum(x[j] * A[:, j] for j in range(n))) and close(A @ x, [A[i] @ x for i in range(m)]) and (A @ x).shape == (m,)
    j = rng.integers(n)
    ok &= close(A @ np.eye(n)[j], A[:, j])
check("L2:views column view = row view; A e_j = column j; output has m entries", ok)
check("L2:views l5 s8 factor model 1.4, 1.65, 2.45; review-2 i3 -3.5; homework-2 i0 -1.9, 0, -2.35", close(np.array([[1.2, .8], [.6, -1.5], [1.5, -.4]]) @ [1.5, -.5], [1.4, 1.65, 2.45])
      and close(np.array([1.1, -.8]) @ [-1, 3], -3.5) and close(np.array([[1.1, .2], [1.2, 1.6], [.8, -.5]]) @ [-2, 1.5], [-1.9, 0, -2.35]))

# L2:maps  rotation convention, shear, reflections, flattening (l6; review-2 i1, i4, i5; homework-2 i5, i6)
check("L2:maps R(90) = [[0, -1], [1, 0]] turns e1 to (0, 1): anticlockwise", close(R(90), [[0, -1], [1, 0]]) and close(R(90) @ [1, 0], [0, 1]))
ok = True
for _ in range(20000):
    a, b = rng.uniform(-360, 360, 2)
    ok &= close(R(a) @ R(b), R(a + b)) and close(R(a) @ R(a), [[math.cos(2 * math.radians(a)), -math.sin(2 * math.radians(a))], [math.sin(2 * math.radians(a)), math.cos(2 * math.radians(a))]])
    ok &= close(R(a).T @ R(a), np.eye(2)) and close(np.linalg.inv(R(a)), R(-a))
    p = rng.normal(size=2)
    ok &= abs(math.remainder(math.degrees(math.atan2(*(R(a) @ p)[::-1]) - math.atan2(*p[::-1])) - a, 360)) < 1e-6
check("L2:maps R(a)R(b) = R(a + b); double angle; R^T R = I; R(-a) undoes R(a); R turns every point by +a", ok)
check("L2:maps reflections: [[0,1],[1,0]] swaps coordinates; diag(1,-1) flips y; diag(-1,1) flips x; -I is R(180)", close(np.array([[0, 1], [1, 0]]) @ [3, 1], [1, 3]) and close(np.diag([1, -1]) @ [3, 1], [3, -1]) and close(np.diag([-1, 1]) @ [3, 1], [-3, 1]) and close(R(180), -np.eye(2)))
check("L2:maps N = [[1,2],[2,4]] sends every point to the line y = 2x; homework-2 i6 to y = -2x", all(close((np.array([[1, 2], [2, 4]]) @ p)[1], 2 * (np.array([[1, 2], [2, 4]]) @ p)[0]) and close((np.array([[2, -1], [-4, 2]]) @ p)[1], -2 * (np.array([[2, -1], [-4, 2]]) @ p)[0]) for p in rng.normal(size=(500, 2))))
check("L2:maps homework-2 i5 R(15)^6 entry (1, 2) = -1; l7 q3 0.866", close(np.linalg.matrix_power(R(15), 6)[0, 1], -1) and abs((R(30) @ R(30))[1, 0] - .866) < 5e-4)

# L2:order  shear then turn against turn then shear: equal only for k = 0 or theta in {0, 180} (l7 s1), over the slider grid
def S(k):
    return np.array([[1., k], [0, 1]])


def image(M):  # the image of the unit square as a set of corners
    return sorted(tuple(np.round(M @ c, 9) + 0.0) for c in ([0, 0], [1, 0], [1, 1], [0, 1]))


ok = True
for t in range(0, 181, 15):
    for k in np.arange(-1.5, 1.51, .5):
        same_matrix = close(R(t) @ S(k), S(k) @ R(t))
        same_shape = image(R(t) @ S(k)) == image(S(k) @ R(t))
        ok &= same_matrix == same_shape == (abs(k) < 1e-12 or t in (0, 180))
check("L2:order l7 s1 on every slider setting: same shape iff k = 0 or theta in {0, 180}", ok)
ok = True
for _ in range(20000):
    A, B = rng.normal(size=(2, 2, 2))
    x = rng.normal(size=2)
    ok &= close((A @ B) @ x, A @ (B @ x)) and close((A @ B)[:, 0], A @ B[:, 0])
check("L2:order (AB)x = A(Bx); column j of AB is A times column j of B", ok)
F, Rq = np.diag([1., -1]), R(90)
check("L2:order l7 s0 RS columns (0, 1), (-1, 1); s5 RF = reflection in y = x, FR sends (2, 1) to (-1, -2)", close(Rq @ S(1), [[0, -1], [1, 1]]) and close(Rq @ F, [[0, 1], [1, 0]]) and close(F @ Rq @ [2, 1], [-1, -2]))
A3, B3 = np.array([[2, 1], [0, 3]]), np.array([[1, 4], [2, -1]])
L_, M_ = np.array([[1.1, .6], [1.3, -.5]]), np.array([[2., -1], [.5, .8]])
check("L2:order l7 s3 AB and slips 6, 13, 9; s8 LM and slips -0.1, -0.9", close(A3 @ B3, [[4, 7], [6, -3]]) and (B3 @ A3)[0, 1] == 13 and close(L_ @ M_, [[2.5, -.62], [2.35, -1.7]]) and close((M_ @ L_)[1, 1], -.1))
ok = True
for _ in range(2000):
    m, n, p = rng.integers(1, 5, 3)
    ok &= (rng.normal(size=(m, n)) @ rng.normal(size=(n, p))).shape == (m, p)
check("L2:order (m x n)(n x p) is m x p", ok)

# L2:transpose  (AB)^T = B^T A^T, also for non-square; A^T A symmetric; u^T v = u.v (l8; review-2 i6, i7; homework-2 i7; problems-2 i3)
ok = True
for _ in range(20000):
    m, n, p = rng.integers(1, 5, 3)
    A, B = rng.normal(size=(m, n)), rng.normal(size=(n, p))
    ok &= close((A @ B).T, B.T @ A.T) and close(A.T @ A, (A.T @ A).T)
    u, v = rng.normal(size=(2, n))
    ok &= close(u.reshape(1, -1) @ v.reshape(-1, 1), u @ v) and (u.reshape(-1, 1) @ v.reshape(1, -1)).shape == (n, n)
check("L2:transpose (AB)^T = B^T A^T; A^T A symmetric; row times column is the dot product", ok)
A8, B8 = np.array([[1, 2], [0, 1]]), np.array([[1, 0], [3, 1]])
check("L2:transpose l8 s4, s5 numbers", close(A8 @ B8, [[7, 2], [3, 1]]) and close(B8.T @ A8.T, [[7, 3], [2, 1]]) and close(A8.T @ B8.T, [[1, 3], [2, 7]]) and close(B8 @ A8, [[1, 2], [3, 7]]))
ok = False
for _ in range(100):
    A, B = rng.integers(-3, 4, size=(2, 2, 2))
    if not close((A @ B).T, A.T @ B.T):
        ok = True
check("L2:transpose A^T B^T is not (AB)^T in general", ok)

# L2:var  portfolio variance w^T Sigma w, by simulation and by formula (l8 s7, s8, q2; review-2 i8; homework-2 i4, i8)
def cov2(s1, s2, rho):
    return np.array([[s1 * s1, rho * s1 * s2], [rho * s1 * s2, s2 * s2]])


Sg = cov2(.2, .1, .3)
w = np.array([.6, .4])
rets = rng.multivariate_normal([0, 0], Sg, size=2_000_000)
sim = (rets @ w).var()
check("L2:var simulation, 2,000,000 draws: variance of the 60/40 mix is w^T Sigma w = 0.01888 (within 1%)", abs(sim / .01888 - 1) < .01 and close(w @ Sg @ w, .01888), f"sim {sim:.6f}")
check("L2:var the simulation separates 0.01888 from the one-cross slip 0.01744 and the no-cross slip 0.016", abs(sim - .01888) < abs(sim - .01744) / 5)
check("L2:var keys: vol 13.74%; review-2 i8 15.37%; homework-2 i4 12.27%, i8(d) 0.01312 and 11.45%", abs(math.sqrt(w @ Sg @ w) - .1374) < 5e-5 and abs(math.sqrt(np.array([.5, .5]) @ cov2(.3, .15, -.2) @ [.5, .5]) - .1537) < 5e-5
      and abs(math.sqrt(np.array([.7, .3]) @ cov2(.18, .06, -.25) @ [.7, .3]) - .1227) < 5e-5 and close(w @ cov2(.2, .1, -.3) @ w, .01312) and abs(math.sqrt(.01312) - .1145) < 5e-5)
ok = True
for _ in range(20000):
    s1, s2 = rng.uniform(.01, .6, 2)
    rho = rng.uniform(-1, .999)
    a = rng.uniform(0, 1)
    ww = np.array([a, 1 - a])
    ok &= math.sqrt(ww @ cov2(s1, s2, rho) @ ww) <= a * s1 + (1 - a) * s2 + 1e-12
    ok &= close(cov2(s1, s2, rho), cov2(s1, s2, rho).T)
check("L2:var long-only mix volatility never exceeds the weighted average of volatilities; covariance matrices are symmetric", ok)
# problems-2
Rp = np.array([[.8, -.6], [.6, .8]])
e = np.array([[1.1, .3], [.9, -.2], [1.4, .6]]).T @ [.4, .35, .25]
Fm = np.array([[.0144, .003], [.003, .0049]])
e2 = e - .605 * np.array([1, .25])
Q, p = np.array([[.5, .3], [.1, .2], [.05, .2]]), np.array([.8, 1.5, 6.])
check("L2:p2 font (6, 8) against (5, 8); site (10, -5), 126.9; hedge 0.00376, 80.3%; bakery 54.88, (0.85, 1.74), 77.30", close(np.diag([1.5, 1]) @ S(.25) @ [2, 8], [6, 8]) and close(S(.25) @ np.diag([1.5, 1]) @ [2, 8], [5, 8])
      and close(Rp.T @ [11, 2], [10, -5]) and abs(angle(Rp @ [0, 10], [1, 0]) - 126.9) < .05 and close(e, [1.105, .2]) and close(e2, [.5, .04875]) and abs(e2 @ Fm @ e2 - .00376) < 5e-6 and abs(e @ Fm @ e - .0191) < 5e-6
      and abs(1 - (e2 @ Fm @ e2) / (e @ Fm @ e) - .803) < 5e-4 and close(p @ (Q @ [40, 12]), 54.88) and close(Q.T @ p, [.85, 1.74]) and close((Q.T @ p) @ [50, 20], 77.3))

# ------------------------------------------------------------------ Level 3
# L3:inv  the 2 x 2 inverse rule; a left inverse of a square matrix is a right inverse; (AB)^-1 = B^-1 A^-1 (l10; review-3 i2 to i4; homework-3 i1, i2)
def inv2(M):
    (a, b), (c, d) = M
    return np.array([[d, -b], [-c, a]]) / (a * d - b * c)


ok = True
for _ in range(50000):
    A, B = rng.normal(size=(2, 2, 2))
    if abs(np.linalg.det(A)) < 1e-3 or abs(np.linalg.det(B)) < 1e-3:
        continue
    ok &= close(inv2(A) @ A, np.eye(2), 1e-6) and close(A @ inv2(A), np.eye(2), 1e-6) and close(inv2(A @ B), inv2(B) @ inv2(A), 1e-5)
    b = rng.normal(size=2)
    ok &= close(A @ (inv2(A) @ b), b, 1e-6)
check("L3:inv swap a and d, negate b and c, divide by ad - bc; it works on both sides; (AB)^-1 = B^-1 A^-1; x = A^-1 b solves", ok)
ok = False
for _ in range(100):
    A, B = rng.normal(size=(2, 2, 2))
    if not close(inv2(A @ B), inv2(A) @ inv2(B), 1e-6):
        ok = True
check("L3:inv A^-1 B^-1 is not (AB)^-1 in general (l10 s5 same-order option; problems-3 i2 part 5)", ok)
note("L3:inv-sides", "the course defines the inverse by A^-1 A = I only; homework-3 i2 uses A A^-1 = I and B B^-1 = I, never stated (finding 6; fixed: the proof now shows (B^-1 A^-1)(AB) = I)")
note("L3:inv-hypothesis", "l10 s7 and the summary give the 2 x 2 rule without ad - bc != 0; l11 supplies it (finding 7; fixed: both now say ad - bc != 0)")
Ad = np.array([[.5, .25], [.2, .3]])
check("L3:inv hedge keys (225, 350), (-150, 300), (50, 300), (-25, 50); homework-3 i8 (437.5, 100)", close(inv2(Ad), [[3, -2.5], [-2, 5]]) and close(inv2(Ad) @ [200, 150], [225, 350]) and close(inv2(Ad) @ [0, 60], [-150, 300])
      and close(inv2(Ad) @ [100, 100], [50, 300]) and close(inv2(Ad) @ [0, 10], [-25, 50]) and close(np.linalg.solve([[.4, .25], [.16, .3]], [200, 100]), [437.5, 100]))
check("L3:inv l10 s5: R^-1 S^-1 sends (-1, 2) to (2, 0.5); S^-1 R^-1 sends it to (1, 1)", close(R(-90) @ np.diag([.5, 1]) @ [-1, 2], [2, .5]) and close(np.diag([.5, 1]) @ R(-90) @ [-1, 2], [1, 1]))

# L3:q3  l10 quiz 3, fixed text: "first rotates by 30 degrees and then stretches x by 3". The old text stretched
# everything by 3, which is 3I and commutes with every matrix, so the option marked wrong also undid it (finding 1).
T = np.diag([3., 1]) @ R(30)
Si = np.diag([1 / 3, 1])
keyed = R(-30) @ Si                         # shrink x, then rotate back (the key "right")
same_order = Si @ R(-30)                    # rotate back, then shrink x (option "same-order")
negate = R(-30) @ np.diag([-3., 1])         # stretch x by -3, then rotate back (option "negate")
repeat = Si @ R(30)                         # rotate by 30 again, then shrink x (option "repeat")
check("L3:q3 the keyed steps undo the transform", close(keyed @ T, np.eye(2)))
check("L3:q3 same-order, negate and repeat do not undo it: exactly one option is right",
      not close(same_order @ T, np.eye(2)) and not close(negate @ T, np.eye(2)) and not close(repeat @ T, np.eye(2)))
T_old = (3 * np.eye(2)) @ R(30)
check("L3:q3 why the old text was wrong: with 3I the same-order option also undoes it", close((np.eye(2) / 3) @ R(-30) @ T_old, np.eye(2)))

# L3:det  |det| is the area factor and the sign is orientation; det(AB) = det A det B; det 0 iff parallel columns iff no inverse (l11; homework-3 i5, i6; problems-3)
def shoelace(P):
    x, y = np.array(P).T
    return 0.5 * (x @ np.roll(y, -1) - y @ np.roll(x, -1))  # signed: positive when anticlockwise


sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1.]])
tri = np.array([[0.3, -1], [2, .4], [-.7, 1.9]])
ok = True
for _ in range(20000):
    A, B = rng.normal(size=(2, 2, 2))
    d = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
    ok &= close(shoelace(sq @ A.T), d) and close(shoelace(tri @ A.T), d * shoelace(tri)) and close(np.linalg.det(A @ B), np.linalg.det(A) * np.linalg.det(B), 1e-8)
check("L3:det signed area of the image = (ad - bc) x signed area, for the unit square and a triangle; det(AB) = det A det B", ok)
ok = True
for a, b, c, d in itertools.product(range(-4, 5), repeat=4):
    Mx = np.array([[a, b], [c, d]], float)
    ok &= ((a * d - b * c) == 0) == (np.linalg.matrix_rank(Mx) < 2)
check("L3:det every integer matrix with entries in [-4, 4]: ad - bc = 0 iff the columns lie on one line", ok)
note("L3:det-proof", "l11 s8 writes column 2 = t x column 1; that misses a zero first column with a non-zero second (finding 10; fixed: the set-up now assumes column 2 is a multiple of column 1)")
check("L3:det keys: l11 s0 k = 2, s3 area 5, s7 k = 4, q0 11, q2 k = 2; review-3 i5 k = 4; homework-3 i3 k = 4, i5 0.0027", close(2 * 1 - 1 * 2, 0) and abs(np.linalg.det([[1, 3], [2, 1]])) - 5 < 1e-9 and close(4 * 3 - 12, 0)
      and close(np.linalg.det([[3, -2], [4, 1]]), 11) and close(2 * 6 - 12, 0) and close(24 - 6 * 4, 0) and close(16 - 16, 0) and close(.04 * .09 - .03 ** 2, .0027) and close(.04 * .09 * (1 - .25), .0027))


def n_solutions(A, b):
    A, b = np.array(A, float), np.array(b, float)
    ra, rab = np.linalg.matrix_rank(A), np.linalg.matrix_rank(np.column_stack([A, b]))
    return "none" if rab > ra else ("one" if ra == A.shape[1] else "many")


check("L3:sing solution counts: l11 s4 none, s5 many, q3 many; review-3 i6 many; q2 of l12 many; problems-3 i1 none; l9 s0 one", n_solutions([[1, 3], [2, 6]], [6, 6]) == "none" and n_solutions([[1, 3], [2, 6]], [6, 12]) == "many"
      and n_solutions([[1, 1], [3, 3]], [2, 6]) == "many" and n_solutions([[1, -2], [-2, 4]], [3, -6]) == "many" and n_solutions([[1, 2], [2, 4]], [1, 2]) == "many" and n_solutions([[12, 8], [3, 2]], [60, 18]) == "none"
      and n_solutions([[1, 1], [2, -1]], [5, 1]) == "one" and n_solutions([[.5, .6], [.2, .24]], [200, 150]) == "none" and n_solutions([[.4, .6], [.16, .24]], [200, 80]) == "many")
ok = True
for a, b, c, d in itertools.product(range(-3, 4), repeat=4):
    if a * d - b * c == 0:
        for b1, b2 in itertools.product(range(-2, 3), repeat=2):
            ok &= n_solutions([[a, b], [c, d]], [b1, b2]) != "one"
check("L3:sing a singular 2 x 2 system never has exactly one solution (every integer case in a small box)", ok)
C3 = np.diag([2., 1]) @ np.array([[.7, .2], [.1, .6]])
check("L3:p3 pellets (30, 40); paint k = 2, (4, 2); sensor C, det 0.8, (120, 80); engraver det 2 - k, (2, 1)", close(np.linalg.solve([[.2, .1], [.4, .7]], [10, 40]), [30, 40]) and close(np.linalg.solve([[12, 8], [3, 5]], [64, 22]), [4, 2])
      and close(C3, [[1.4, .4], [.1, .6]]) and close(np.linalg.det(C3), .8) and close(np.linalg.solve(C3, [200, 60]), [120, 80]) and all(close(np.linalg.det(np.array([[2., k], [1, 1]]) @ np.array([[3, 1], [2, 1]])), 2 - k) for k in range(-3, 4))
      and close(np.linalg.solve(np.array([[2., 1], [1, 1]]) @ np.array([[3, 1], [2, 1]]), [19, 12]), [2, 1]))

# L3:minvar  minimum-variance weights are proportional to Sigma^-1 1; singular Sigma (l11 s10; homework-3 i7)
ok = True
for _ in range(200):
    n = rng.integers(2, 6)
    G = rng.normal(size=(n + 3, n))
    Sg_ = G.T @ G / 100
    z = np.linalg.solve(Sg_, np.ones(n))
    wm = z / z.sum()
    for _ in range(200):
        d = rng.normal(size=n)
        d -= d.mean()  # stays fully invested
        ok &= (wm + .1 * d) @ Sg_ @ (wm + .1 * d) >= wm @ Sg_ @ wm - 1e-12
check("L3:minvar 200 random covariance matrices, 200 fully invested rivals each: none beats Sigma^-1 1 scaled to sum to 1", ok)
Ss = np.full((2, 2), .0625)
check("L3:minvar l11 s10: every fully invested split has variance 0.0625; long one class, short the other has variance 0", all(close(np.array([a, 1 - a]) @ Ss @ [a, 1 - a], .0625) for a in np.linspace(-2, 3, 51)) and close(np.array([1, -1]) @ Ss @ [1, -1], 0))


def mvw(S_):
    z = np.linalg.solve(np.array(S_, float), np.ones(len(S_)))
    return z / z.sum()


v4 = np.array([.01, .012, .015, .02])
S4 = np.outer(v4, v4) * (np.full((4, 4), .3) + .7 * np.eye(4))
check("L3:minvar homework-3 i7 expected weights", close(mvw([[.04, 0], [0, .09]]), [.692308, .307692], 1e-6) and close(mvw([[.04, .03], [.03, .09]]), [.857143, .142857], 1e-6) and close(mvw([[.04, -.02], [-.02, .09]]), [.647059, .352941], 1e-6)
      and close(mvw([[.04, .006, .002], [.006, .09, .012], [.002, .012, .0225]]), [.334608, .063821, .60157], 1e-6) and close(mvw(S4), [.543807, .309668, .132931, .013595], 1e-6))
check("L3:minvar homework-3 i7 test 8: the healthy 4 x 4 matrix has determinant about 8e-16 and rank 4", abs(np.linalg.det(S4) / 8.446e-16 - 1) < 1e-3 and np.linalg.matrix_rank(S4) == 4)
dets = []
for _ in range(200):  # l12 s9 explain: four assets' daily returns, volatility near 1% (0.7% to 1.3%), a healthy sample covariance matrix
    vol = rng.uniform(.007, .013, 4)
    Cc = np.full((4, 4), rng.uniform(.1, .5)) + np.eye(4)
    Cc = Cc / Cc[0, 0]
    dd = rng.multivariate_normal(np.zeros(4), np.outer(vol, vol) * Cc, size=1000)
    dets.append(np.linalg.det(np.cov(dd.T)))
check("L3:scale daily covariance matrices of four assets with volatility near 1%: every determinant between 1e-18 and 1e-14, median within a factor 10 of 1e-16", 1e-18 < min(dets) and max(dets) < 1e-14 and 1e-17 < np.median(dets) < 1e-15, f"min {min(dets):.1e} median {np.median(dets):.1e} max {max(dets):.1e}")
G3 = np.array([[.5, .25, .6], [.2, .3, .1], [.04, .02, .05]])
check("L3:scale det(sA) = s^n det A: the desk matrix scaled by 1e-4 has determinant 2e-16, rank 3, and the same solution", abs(np.linalg.det(G3 * 1e-4) / 2e-16 - 1) < 1e-6 and np.linalg.matrix_rank(G3 * 1e-4) == 3
      and close(np.linalg.solve(G3 * 1e-4, np.array([235, 140, 19]) * 1e-4), [200, 300, 100], 1e-6))

# L3:numpy  what the lesson says NumPy does (l12). Desktop behaviour here; the page's Pyodide behaviour is in the sweep file.
check("L3:numpy l12 s1: det of [[2, 3], [1, 4]] prints 5.000000000000001", str(np.linalg.det(np.array([[2, 3], [1, 4]]))) == "5.000000000000001")
check("L3:numpy l12 s4: A * x is elementwise (4 numbers), A @ x = [200, 150], x @ A = [182.5, 161.25]", close(Ad * np.array([225, 350]), [[112.5, 87.5], [45, 105]]) and close(Ad @ [225, 350], [200, 150]) and close(np.array([225, 350]) @ Ad, [182.5, 161.25]))
check("L3:numpy keys: l12 q0 [3, 7], x @ A [4, 6]; review-3 i7 [2, 7] and [4, 6]; s0 test 4; s8 tests", close(np.array([[1, 2], [3, 4]]) @ [1, 1], [3, 7]) and close(np.array([1, 1]) @ np.array([[1, 2], [3, 4]]), [4, 6])
      and close(np.array([[2, 0], [1, 3]]) @ [1, 2], [2, 7]) and close(np.array([[2, 0], [1, 3]]).T @ [1, 2], [4, 6]) and close(G3 @ [200, 300, 100], [235, 140, 19]) and close(np.linalg.solve(G3, [0, 100, 0]), [-250, 500, 0], 1e-6)
      and close(np.linalg.solve(G3, [100, 50, 5]), [2500, -1000, -1500], 1e-6) and close(np.linalg.solve([[1, .5, .4], [0, .2, .3], [0, .01, .04]], [300, 120, 9]), [42, 420, 120], 1e-6))
# np.allclose(a, b) accepts |a - b| <= atol + rtol |b| with atol 1e-8, rtol 1e-5 (l12 s2 explain, q3 explain)
check("L3:numpy np.allclose tolerance is 1e-8 + 1e-5 |b|", np.allclose(1 + .99e-5, 1.0) and not np.allclose(1 + 1.2e-5, 1.0) and np.allclose(.9e-8, 0.0) and not np.allclose(1.2e-8, 0.0))


def raises(M, b):
    try:
        np.linalg.solve(np.array(M, float), np.array(b, float))
    except np.linalg.LinAlgError:
        return True
    return False


S9 = [[.5, .25, .75], [.2, .3, .5], [.04, .02, .06]]
check("L3:numpy desktop NumPy raises LinAlgError for the exactly singular systems of l12 s9 and q2 and homework-3 i7 test 6", raises(S9, [235, 140, 19]) and raises([[1, 2], [2, 4]], [1, 2]) and raises([[.5, .6], [.2, .24]], [200, 150]) and raises(Ss, [1, 1]))
check("L3:numpy rank: P, Q, T matrix 2; proportional greeks 1; three three-year bonds 2; paint matrix 1", np.linalg.matrix_rank(np.array(S9)) == 2 and np.linalg.matrix_rank(np.array([[.5, .6], [.2, .24]])) == 1
      and np.linalg.matrix_rank(np.array([[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]])) == 2 and np.linalg.matrix_rank(np.array([[12., 8], [3, 2]])) == 1)
check("L3:numpy a singular matrix whose computed determinant is not 0 does not raise: [[0.04, 0.06], [0.06, 0.09]] and the three-year bonds", not raises([[.04, .06], [.06, .09]], [1, 1]) and np.linalg.det(np.array([[.04, .06], [.06, .09]])) != 0
      and not raises([[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]], [94.859, 98.207, 102.113]))
note("L3:numpy-s9-tests", "l12 s9 had no such case, so `if np.linalg.det(A) == 0` and a nan check after solve passed all six hidden tests (sweep; finding 3; fixed: hidden test 7 is [[0.04, 0.06], [0.06, 0.09]])")
# l12 s5: solve against inv on the 10 x 10 Hilbert matrix
H = np.array([[1 / (i + j + 1) for j in range(10)] for i in range(10)])
bh = H @ np.ones(10)
r1, r2 = np.abs(H @ np.linalg.solve(H, bh) - bh).max(), np.abs(H @ (np.linalg.inv(H) @ bh) - bh).max()
check("L3:numpy l12 s5: Hilbert 10 x 10, residual of solve at rounding level, residual of inv at least 1e8 times larger", r1 < 1e-14 and r2 > 1e8 * r1, f"{r1:.1e} {r2:.1e}")
ratios = []
for _ in range(300):  # a well-conditioned 10 x 10 matrix: three times the arithmetic does not cost accuracy
    Mw = rng.normal(size=(10, 10)) + 10 * np.eye(10)
    bw = Mw @ np.ones(10)
    ratios.append(np.abs(Mw @ (np.linalg.inv(Mw) @ bw) - bw).max() / max(np.abs(Mw @ np.linalg.solve(Mw, bw) - bw).max(), 1e-16))
check("L3:numpy on 300 well-conditioned 10 x 10 matrices inv's residual stays within 100 times solve's: the Hilbert gap comes from conditioning", np.median(ratios) < 100 and np.linalg.cond(H) > 1e12)
note("L3:numpy-s5-reason", "the keyed option explains the gap by 'fewer steps'; the step count differs by 3, the residual by 1e11 (finding 5; fixed: the key now says solve never multiplies a rounded inverse into b)")
# l12 s2 feedback test-3: "With == the rounding error in np.linalg.inv can break the test." Test 3 is A = [[2, 3], [1, 4]].
A23 = np.array([[2., 3], [1, 4]])
check("L3:numpy l12 s2 test 3: B is np.linalg.inv(A) itself, so the key True holds (the fixed line says so; finding 2)", np.allclose(np.linalg.inv(A23) @ A23, np.eye(2)))
check("L3:numpy l12 s2 test 6: an == comparison fails on the 3 x 3 desk matrix (the == line now sits on test 6)", not bool((np.linalg.inv(G3) @ G3 == np.eye(3)).all()))
# l12 s2 tests 7 and 8 (finding 4): the key False, and the lax checks they catch
B7A = np.eye(2) @ np.array([[1., 1], [0, 1]])
B8A = np.array([[.6, 0], [0, .6]]) @ np.array([[2., 0], [0, 2]])
check("L3:numpy l12 s2 test 7: BA has a unit diagonal and a 1 off it, so not I; a diagonal-only or trace check says True",
      not np.allclose(B7A, np.eye(2)) and np.allclose(np.diag(B7A), 1) and np.isclose(np.trace(B7A), 2))
check("L3:numpy l12 s2 test 8: BA = 1.2 I, so not I; rounding first or atol 0.5 says True",
      close(B8A, 1.2 * np.eye(2)) and not np.allclose(B8A, np.eye(2)) and bool(np.all(np.round(B8A) == np.eye(2))) and np.allclose(B8A, np.eye(2), atol=.5))
# l12 s9 test 7 (finding 3): singular in exact arithmetic (row 2 = 1.5 x row 1), rank 1 in floating point, determinant not 0
N7 = np.array([[.04, .06], [.06, .09]])
check("L3:numpy l12 s9 test 7: rank 1 so the solution raises; the computed determinant is non-zero and below 1e-18; solve gives huge finite numbers",
      np.linalg.matrix_rank(N7) == 1 and 0 < abs(np.linalg.det(N7)) < 1e-18 and abs(.04 * 1.5 - .06) < 1e-15 and abs(.06 * 1.5 - .09) < 1e-15
      and (raises(N7, [1, 1]) or np.all(np.isfinite(np.linalg.solve(N7, [1., 1]))) and np.abs(np.linalg.solve(N7, [1., 1])).max() > 1e15))

# L3:bonds  homework-3 i9: prices = cash flows x discount factors; expected values of the hidden tests
def rows(bonds, years):
    C = np.zeros((len(bonds), years))
    for i, (c, m) in enumerate(bonds):
        C[i, :m] = c
        C[i, m - 1] += 100
    return C


def curve(bonds, prices):
    return np.linalg.solve(rows(bonds, max(m for _, m in bonds)), np.array(prices, float))


d1 = curve([[4, 1], [5, 2], [3, 3]], [99.84, 101.4, 96.28])
d2 = curve([[2, 2], [6, 2], [4, 3]], [96.8, 104.4, 100.16])
d3 = curve([[5, 4], [0, 1], [3.5, 2], [4.25, 3]], [101.2, 96.5, 99.3, 100.15])
check("L3:bonds curves and target prices of tests 1 to 7", close(d1, [.96, .92, .88]) and close(rows([[6, 3], [0, 2], [5, 2]], 3) @ d1, [104.56, 92, 101.4]) and close(d2, [.97, .93, .89]) and close(rows([[0, 1], [3, 2]], 3) @ d2, [97, 98.7])
      and close(d3, [.965, .926787439613527, .883548233876667, .831650682214753]) and close(rows([[6, 4], [0, 4], [2, 1]], 4) @ d3, [104.806986355705, 83.1650682214753, 98.43]) and close(100 * 99.5 / 103, 96.6019417475728))
check("L3:bonds tests 8 and 9 are rank deficient; test 9 has a non-zero computed determinant", np.linalg.matrix_rank(rows([[2, 1], [5, 1], [4, 3]], 3)) == 2 and np.linalg.matrix_rank(rows([[2.1, 3], [3.3, 3], [4.7, 3]], 3)) == 2
      and np.linalg.det(rows([[2.1, 3], [3.3, 3], [4.7, 3]], 3)) != 0)

print(f"\n{N} checks, {len(FAILS)} failing, {len(NOTES)} notes")
for f in FAILS:
    print("  failing: " + f)
sys.exit(1 if FAILS else 0)
