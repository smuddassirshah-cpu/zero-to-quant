"""Fix-pass read of commit b94bc48c (vectors l6, l7, l10, l12, homework-3): the figures the changed lines state.

Run with the venv Python from the repository root. Exits 0 when every stated figure holds.
Values marked (page) differ between desktop NumPy and the page's Pyodide 0.27.7 (NumPy 2.0.2); those
were read under Pyodide and are quoted in docs/reviews/audit-vectors-1-3-r2.md, not asserted here.
"""
import itertools
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'vectors')
n = 0


def ok(cond, what):
    global n
    n += 1
    if not cond:
        raise SystemExit('FAIL: ' + what)


# ---- l12 screen 3, hidden test 9: the typed decimal inverse of [[2, 3], [1, 4]]
A = np.array([[2, 3], [1, 4]], dtype=float)
B = np.array([[0.8, -0.6], [-0.2, 0.4]])
ok(np.allclose(B @ A, np.eye(2)) and np.allclose(A @ B, np.eye(2)), 'test 9 expects True')
ok(abs(np.linalg.det(A) - 5) < 1e-12, 'det is 5, so the inverse is (1/5)[[4,-3],[-1,2]]')
inv = np.linalg.inv(A)
ok(repr(float(inv[0, 1])) == '-0.6000000000000001', 'inv gives -0.6000000000000001')
ok(not (inv == B).all() and (inv == B).sum() == 3, 'exact comparison with inv fails in one entry')
ok(not (B @ A == np.eye(2)).all(), 'exact comparison of the product fails too')
# test 1 is a true inverse; tests 1, 3 and 5 survive an exact comparison with inv, so those codings first fail test 9
for T, Bt in (([[2, 1], [1, 1]], [[1, -1], [-1, 2]]), ([[4, 1], [2, 1]], [[0.5, -0.5], [-1, 2]])):
    ok((np.linalg.inv(np.array(T, dtype=float)) == np.array(Bt)).all(), 'exact inverse of %r' % T)

# ---- l12 screen 9, test-3 line: gamma near 0.08 of delta for every option, 0.05 for the target
G = np.array([[0.50, 0.25, 0.60], [0.20, 0.30, 0.10], [0.04, 0.02, 0.05]])
ratio = G[2] / G[0]
ok(all(abs(r - 0.08) < 0.005 for r in ratio), 'gamma over delta is 0.08, 0.08, 0.0833')
ok(5 / 100 == 0.05, 'target ratio 0.05')
x = np.linalg.solve(G, [100, 50, 5])
ok(np.allclose(x, [2500, -1000, -1500]), 'test 3 answer')
# second way: Cramer's rule by cofactors
det = np.linalg.det(G)
cr = []
for j in range(3):
    M = G.copy()
    M[:, j] = [100, 50, 5]
    cr.append(np.linalg.det(M) / det)
ok(np.allclose(cr, [2500, -1000, -1500]), 'test 3 answer by Cramer')

# ---- homework-3 h-min-var
S1 = np.array([[0.04, 0.0], [0.0, 0.09]])
z = np.linalg.solve(S1, np.ones(2))
ok(abs(z[0] - 25) < 1e-9 and abs(z[1] - 11.1111111) < 1e-6, '1/variance is 25 and 11.1')
ok(np.allclose(np.round(z / z.sum(), 3), [0.692, 0.308]), 'weights 0.692 and 0.308')
ok(abs(9 / 13 - 0.692308) < 1e-6 and abs(4 / 13 - 0.307692) < 1e-6, 'second way: 9/13 and 4/13')

S7 = np.array([[0.04, 0.06], [0.06, 0.09]])
S9 = np.array([[0.04, 0.044], [0.044, 0.0484]])
ok(math.isclose(math.sqrt(0.04), 0.2) and math.isclose(math.sqrt(0.0484), 0.22) and math.isclose(0.2 * 0.22, 0.044), 'test 9 is 20% and 22% at correlation 1')
ok(4 * 484 == 44 * 44, 'test 9 is exactly singular in exact arithmetic (in units of 1e-4)')
ok(4 * 9 == 6 * 6, 'test 7 is exactly singular in exact arithmetic')
for S in (S7, S9):
    ok(np.linalg.matrix_rank(S) == 1, 'rank 1')
    zz = np.linalg.solve(S, np.ones(2))          # no LinAlgError: a huge, finite answer
    ok(np.isfinite(zz).all() and np.abs(zz).min() > 1e15, 'solve returns huge finite numbers, not nan')
    ii = np.linalg.inv(S)                        # no LinAlgError either
    ok(np.isfinite(ii).all() and np.abs(ii).min() > 1e16, 'inv returns a huge finite inverse')
ok(3.5e-19 < np.linalg.det(S7) < 4.5e-19, 'computed det of test 7 is near 4e-19')
ok(S7[0, 0] * S7[1, 1] - S7[0, 1] * S7[1, 0] == 0.0, 'hand ad - bc is exactly 0 on test 7')
hand9 = S9[0, 0] * S9[1, 1] - S9[0, 1] * S9[1, 0]
ok(1.5e-19 < hand9 < 2.5e-19, 'hand ad - bc is about 2e-19 on test 9')
ok(hand9 == 2.0 ** -62, 'the two products differ by one unit in the last place')
ok(S9[0, 0] * S9[1, 1] != S9[0, 1] ** 2, 'the squared-covariance test misses test 9 too')
ok(np.linalg.det(S9) != 0, 'np.linalg.det is not 0 on test 9 either')
# the rank decision has room: the second singular value sits well under the cut-off
for S in (S7, S9):
    sv = np.linalg.svd(S, compute_uv=False)
    ok(sv[1] < 0.1 * sv[0] * 2 * np.finfo(float).eps, 'second singular value at least 10 times under the rank cut-off')
v = np.array([0.01, 0.012, 0.015, 0.02])
S8 = np.outer(v, v) * (np.full((4, 4), 0.3) + 0.7 * np.eye(4))
ok(7e-16 < np.linalg.det(S8) < 9e-16 and np.linalg.matrix_rank(S8) == 4, 'test 8: det about 8e-16, rank 4')
hw = json.load(open(os.path.join(VEC, 'homework-3.json')))
tests = [it for it in hw['items'] if it.get('id') == 'h-min-var'][0]['widget']['tests']
ok(len(tests) == 9 and sum(t.get('compare') == 'raises' for t in tests) == 3, '9 tests, three expect LinAlgError')
l12 = json.load(open(os.path.join(VEC, 'l12-numpy-matrices.json')))
ok(len(l12['screens'][2]['widget']['tests']) == 9, 'l12 is_inverse has 9 tests')

# ---- l6: the quarter turn and the swap
R = np.array([[0, -1], [1, 0]])
ok((R @ [1, 0] == [0, 1]).all() and (R @ [0, 1] == [-1, 0]).all(), 'anticlockwise quarter turn: e1 to (0,1), e2 to (-1,0)')
Rc = R.T
ok((Rc @ [1, 0] == [0, -1]).all() and (Rc @ [0, 1] == [1, 0]).all(), 'clockwise quarter turn sends e1 to (0,-1)')
th = math.pi / 2
ok(np.allclose([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]], R), 'R(90) is [[0,-1],[1,0]]')
ok(np.allclose([[math.cos(math.pi), -math.sin(math.pi)], [math.sin(math.pi), math.cos(math.pi)]], -np.eye(2)), 'the third option is the half turn')
Msw = np.array([[0, 1], [1, 0]])
ok((Msw >= 0).all() and round(np.linalg.det(Msw)) == -1, 'M has no minus sign and is a reflection, not a turn')

# ---- l7 screen 1: every route to (-1, 0), and screen 2 over the whole slider grid
S = np.array([[1, 1], [0, 1]])
e1, e2 = np.array([1, 0]), np.array([0, 1])
ok((R @ e2 == [-1, 0]).all(), 'e2: the turn alone')
ok((S @ R @ e2 == [-1, 0]).all(), 'e2: turn, then shear')
ok((R @ R @ e1 == [-1, 0]).all(), 'e1: two turns')
ok((S @ e1 == e1).all() and (R @ S @ e1 == [0, 1]).all(), 'the shear keeps e1 and one turn takes it to (0,1)')
ok(not any((W @ e1 == [-1, 0]).all() for W in (R, S, R @ S, S @ R)), 'no single use of the two moves puts e1 on (-1,0)')


def rot(t):
    c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
    return np.array([[c, -s], [s, c]])


def same_place(M1, M2):
    """The unit square lands on the same parallelogram: same matrix, or the same with columns swapped."""
    return np.allclose(M1, M2, atol=1e-9) or np.allclose(M1, M2[:, ::-1], atol=1e-9)


for t, k in itertools.product(range(0, 181, 15), [i * 0.5 for i in range(-3, 4)]):
    Sk = np.array([[1, k], [0, 1]])
    coincide = same_place(rot(t) @ Sk, Sk @ rot(t))
    ok(coincide == (k == 0 or t in (0, 180)), 'slider grid t=%s k=%s' % (t, k))
M1, M2 = rot(90) @ S, S @ rot(90)
sides = lambda M: sorted([np.linalg.norm(M[:, 0]), np.linalg.norm(M[:, 1])])
ang = lambda M: abs(M[:, 0] @ M[:, 1]) / (np.linalg.norm(M[:, 0]) * np.linalg.norm(M[:, 1]))
ok(np.allclose(sides(M1), sides(M2)) and math.isclose(ang(M1), ang(M2)), 'at 90 and 1: same sides and angles')
ok(not same_place(M1, M2), 'at 90 and 1: different places')

# ---- l10 screen 1: snap points inside each wrong region
l10 = json.load(open(os.path.join(VEC, 'l10-undoing.json')))
w = l10['screens'][0]['widget']
snap = l10['screens'][0]['canvas']['params']['snap']
grid = [i * snap for i in range(-2, 17)]
for reg in w['wrong']:
    r = reg['region']
    pts = [(x, y) for x in grid for y in grid if r['x'][0] <= x <= r['x'][1] and r['y'][0] <= y <= r['y'][1]]
    want = {'on-target': [(6.0, 6.0)], 'swapped': [(2.0, 3.0)]}[reg['id']]
    ok(pts == want, '%s holds exactly the snap point %r' % (reg['id'], want))
ok((2 * 6, 3 * 6) == (12, 18), 'u on T is sent to (12, 18)')
ok((6 / 3, 6 / 2) == (2, 3), 'swapped: x by 3 and y by 2')
l7 = json.load(open(os.path.join(VEC, 'l7-one-after-another.json')))
for reg in l7['screens'][0]['widget']['wrong']:
    r = reg['region']
    pts = [(x, y) for x in range(-3, 4) for y in range(-2, 4) if r['x'][0] <= x <= r['x'][1] and r['y'][0] <= y <= r['y'][1]]
    ok(pts == {'at-1-1': [(1, 1)], 'turn-first': [(-1, 0)]}[reg['id']], 'l7 %s holds one snap point' % reg['id'])

print('vectors-L1-3-r2-fixread: %d checks passed' % n)
