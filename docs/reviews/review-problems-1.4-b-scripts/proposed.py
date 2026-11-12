"""Second read, elimination and least-squares problem sets: the numbers of the fixes the review proposes, each computed
here (sympy exact; NumPy as a second route for the fits). Exit 0 when every figure quoted in the review holds.

Run from the repo root:  <venv>/bin/python docs/reviews/review-problems-1.4-b-scripts/proposed.py
"""
import sys

import numpy as np
import sympy as sp

M = sp.Matrix
R = sp.Rational
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


t = lambda v: tuple(v)

# finding 1: p-courier-rounds on new rounds, same minutes (2, 4, 3)
A = M([[0, 3, 2], [4, 1, 1], [0, 6, 7]]); x = M([2, 4, 3]); b = A * x
ok(t(b) == (18, 15, 45), 'courier: b = (18, 15, 45)')
P = M([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
PA = P * A
ok(PA[0, 0] != 0 and A[2, 0] == 0, 'courier: only the swap of rows 1 and 2 works')
l32 = PA[2, 1] / PA[1, 1]
U = PA.copy(); U[2, :] = U[2, :] - l32 * U[1, :]
ok(l32 == 2 and tuple(map(tuple, U.tolist())) == ((4, 1, 1), (0, 3, 2), (0, 0, 3)), 'courier: l32 = 2, U = (4, 1, 1), (0, 3, 2), (0, 0, 3)')
Pb = P * b
c = M([Pb[0], Pb[1], Pb[2] - 2 * Pb[1]])
ok(t(Pb) == (15, 18, 45) and t(c) == (15, 18, 9), 'courier: Pb = (15, 18, 45), c = (15, 18, 9)')
ok((b[0], b[1], b[2] - 2 * b[1]) == (18, 15, 15), 'courier: unswapped slip (18, 15, 15)')
ok(Pb[2] + 2 * Pb[1] == 81, 'courier: signs slip c3 = 81')
z = c[2] / 3; y = (c[1] - 2 * z) / 3; xx = (c[0] - y - z) / 4
ok((xx, y, z) == (2, 4, 3), 'courier: back substitution gives (2, 4, 3)')
nz = c[2]; ny = c[1] - 2 * nz; nx = c[0] - ny - nz
ok((nx, ny, nz) == (6, 0, 9), 'courier: no-divide slip (6, 0, 9)')
ok(5 * 2 + 2 * 4 + 4 * 3 == 30 and 5 * 3 + 2 * 4 + 4 * 2 == 31, 'courier: part 5 unchanged, 30 and 31')

# finding 2: p-vinyl-cutter part 1 at k = 2
T = M([[3, 2], [2, 4]])
ok(T.det() == 8 and 5 * T.det() == 40 and 5 * (12 + 4) == 80 and 5 * 12 == 60, 'vinyl: det 8, area 40, slips 80 and 60')

# finding 3: p-tilted-gantry on the target (6, 2, c)
m1, m2, m3 = M([1, 0, 2]), M([1, 1, 0]), M([0, 2, -4])
cs = sp.Symbol('c')
cc = sp.solve(m1.row_join(m2).row_join(M([6, 2, cs])).det(), cs)[0]
ok(cc == 8, 'gantry: c = 8')
ok(sp.solve(cs - 2 * 6, cs)[0] == 12 and sp.solve(cs - 12 + 2 * 2, cs)[0] == 8, 'gantry: half-step slip 12, then c - 8 = 0')
Mk = m1.row_join(m2).row_join(m3)
ok(t(Mk * M([4, 2, 0])) == (6, 2, 8) and t(Mk * M([6, 0, 1])) == (6, 2, 8), 'gantry: (4, 2, 0) and (6, 0, 1) both reach (6, 2, 8)')
ok(t(M([4, 2, 0]) + M([-2, 2, 1])) == (2, 4, 1) and t(Mk * M([2, 4, 1])) != (6, 2, 8), 'gantry: sign slip (2, 4, 1) misses')
# finding 3: p-futures-packages on the target (5, -2, c)
S = M([[1, 0, 1], [-1, 1, -2], [0, -1, 1]])
ok(sp.solve(M([[1, 0, 5], [-1, 1, -2], [0, -1, cs]]).det(), cs)[0] == -3, 'futures: c = -3')
ok(-2 + 5 == 3 and sp.solve(cs + (-2), cs)[0] == 2 and 5 - 2 + 3 == 6, 'futures: row 2 becomes 3; stale-rhs slip 2; entries sum 6 at c = 3')
ok(t(S * M([5, 3, 0])) == (5, -2, -3) and (S * M([5, -3, 0]))[1] == -8, 'futures: (5, 3, 0) builds it; (5, -3, 0) gives June -8')
ok(t(M([5, 3, 0]) + 2 * M([-1, 1, 1])) == (3, 5, 2) and t(S * M([3, 5, 2])) == (5, -2, -3), 'futures: two butterflies (3, 5, 2)')
ok(t(M([5, 3, 0]) + 2 * M([1, -1, 1])) == (7, 1, 2) and t(S * M([7, 1, 2])) == (9, -10, 1), 'futures: sign slip (7, 1, 2) gives (9, -10, 1)')

# finding 9: p-hall-drone part 2, the slip solved
ok(sp.solve(4 + 6 + cs, cs)[0] == -10, 'hall-drone: 4 + 6 + c = 0 gives -10')

# finding 12: the unit vectors
for v, n in ((M([2, -2, -1]), 3), (M([1, 2, -2]), 3), (M([-1, 1, -1, 1]), 2)):
    ok(v.norm() == n, f'normalised: |{t(v)}| = {n}')

# finding 14: p-gas-hubs on t = (0, 1, 2, 3, 4)
tt = M([0, 1, 2, 3, 4]); yN = M([R(7, 2), 0, R(-1, 2), -3, -5]); yS = M([2, 1, -2, -2, -4])
A = sp.ones(5, 1).row_join(tt)
ATA = A.T * A
ok(tuple(map(tuple, ATA.tolist())) == ((5, 10), (10, 30)), 'gas: A.T @ A = [[5, 10], [10, 30]]')
ok(t(A.T * yN) == (-5, -30) and t(A.T * yS) == (-5, -25), 'gas: right-hand sides (-5, -30) and (-5, -25)')
fN = ATA.inv() * A.T * yN; fS = ATA.inv() * A.T * yS; fD = ATA.inv() * A.T * (yN - yS)
ok(t(fN) == (3, -2) and t(fS) == (2, R(-3, 2)) and t(fD) == (1, R(-1, 2)), 'gas: fits (3, -2), (2, -1.5), spread (1, -0.5)')
ok(t(fN + fS) == (5, R(-7, 2)) and t(fS - fN) == (-1, R(1, 2)), 'gas: part 4 slips (5, -3.5) and (-1, 0.5)')
ok((R(-5, 5), R(-30, 30)) == (-1, -1) and (R(-5, 5), R(-25, 30)) == (-1, R(-5, 6)), 'gas: diagonal slips (-1, -1) and (-1, -5/6)')
ok(ATA[0, 1] ** 2 == 100, 'gas: sum-squared slip 100')
d = yN - yS
e = d - A * fD
ok(t(A * fD) == (1, R(1, 2), 0, R(-1, 2), -1) and e.dot(e) == 5 and d.dot(d) == R(15, 2) and 1 - e.dot(e) / d.dot(d) == R(1, 3), 'gas: fitted spread, SSE 5, R2 = 1/3 unchanged')
eN = yN - A * fN; eS = yS - A * fS
ok(eN.dot(eN) == R(3, 2) and eS.dot(eS) == R(3, 2), 'gas: hub SSEs unchanged at 1.5')
ok(np.allclose(np.polyfit([0, 1, 2, 3, 4], [3.5, 0, -0.5, -3, -5], 1), [-2, 3]) and np.allclose(np.polyfit([0, 1, 2, 3, 4], [2, 1, -2, -2, -4], 1), [-1.5, 2]), 'gas: polyfit agrees')

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
