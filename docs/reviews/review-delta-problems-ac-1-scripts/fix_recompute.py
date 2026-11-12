"""Fix pass c1: recompute every new key and wrong value of p-river-gauges by two routes."""
from fractions import Fraction as F
import numpy as np, sympy as sp


def ok(c, m):
    assert c, m
    print("ok", m)


# route 1: exact fractions by hand elimination
K = [[F(8), F(4), F(4)], [F(4), F(7), F(3)], [F(4), F(3), F(5, 2)]]
m21 = K[1][0] / K[0][0]
p2 = K[1][1] - m21 * K[0][1]
ok(p2 == 5 and m21 == F(1, 2), "part 1 key: second pivot 5")
ok(K[1][1] - 1 * K[0][1] == 3, "multiplier-one slip 3")
ok(K[1][1] - K[1][0] * K[0][1] == -9, "multiplier-two slip -9")
r2 = [K[1][j] - m21 * K[0][j] for j in range(3)]
ok(r2 == [0, 5, 1], "row 2 leaves (0, 5, 1)")
ok(8 * 7 - 16 == 40 and 8 * 5 == 40, "corner determinant 40")
# part 2: third pivot c - d
m31 = F(4) / 8
t = [K[2][1] - m31 * K[0][1], K[2][2] - m31 * K[0][2]]  # (1, c - 2) at c = 5/2
ok(t[0] == 1 and t[1] == F(5, 2) - 2, "row 3 after step 1 is (0, 1, c - 2)")
m32 = t[0] / p2
ok(m32 == F(1, 5), "second multiplier 0.2")
d = 2 + m32 * 1
ok(d == F(11, 5), "part 2 key d = 2.2")
ok(2 + 1 * 1 == 3, "slips one-step 2, big-multiplier 3")
ok(2 - F(1, 5) == F(9, 5) and 2 + F(1, 5) == d, "added slip: c - 2 + 0.2 gives d = 1.8")
ok(40 * d == 88, "det = 40c - 88")


def Kw(c, w):
    M = [[8, 4, 4], [4, 7, 3], [4, 3, c]]
    return [sum(M[i][j] * w[j] for j in range(3)) for i in range(3)]


# part 3: null vector at c = 2.2
b = F(-1, 5)
a = (-4 * b - 4) / 8
ok((a, b) == (F(-2, 5), F(-1, 5)), "part 3 key (-0.4, -0.2, 1)")
ok(Kw(d, [a, b, F(1)]) == [0, 0, 0], "K0 w = 0, row 3 checks")
ok(abs(-1.6 - 0.6 + 2.2) < 1e-12, "row 3 check -1.6 - 0.6 + 2.2")
ok(F(-4) / 8 == F(-1, 2), "no-b: 8a + 4 = 0 gives a = -0.5, so (-0.5, -0.2, 1)")
ok(Kw(d, [F(-1, 5), F(-2, 5), F(1)]) != [0, 0, 0], "swapped is not null")
# part 4
w = [F(-2, 5), F(-1, 5), F(1)]
kw = Kw(F(5, 2), w)
ok(kw == [0, 0, F(3, 10)], "Kw = (0, 0, 0.3)")
ok(sum(x * y for x, y in zip(w, kw)) == F(3, 10), "part 4 key 0.3")
ws = [F(2, 5), F(1, 5), F(1)]
kws = Kw(F(5, 2), ws)
ok(kws == [8, 6, F(47, 10)], "K(0.4, 0.2, 1) = (8, 6, 4.7)")
ok(sum(x * y for x, y in zip(ws, kws)) == F(91, 10), "sign slip 9.1")
ok(F(5, 2) - d == F(3, 10), "c-only 2.5, boundary 2.2, c - 2.2 = 0.3")
# part 5
ok(F(3, 10) / F(5, 2) == F(3, 25) and 1 - F(3, 25) == F(22, 25), "part 5 key 0.88, unexplained 0.12")
ok(1 - F(3, 10) == F(7, 10), "not-scaled 0.7")
ok(F(5, 2) - F(3, 10) == F(11, 5) and F(11, 5) / F(5, 2) == F(22, 25), "2.2/2.5 = 0.88")

# route 2: NumPy / sympy
Kn = np.array([[8, 4, 4], [4, 7, 3], [4, 3, 2.5]])
L = np.linalg.cholesky(Kn)
ok(np.allclose(np.diag(L) ** 2, [8, 5, 0.3]), "Cholesky pivots 8, 5, 0.3 (= c - 2.2)")
ok(np.isclose(np.linalg.det(Kn), 40 * 2.5 - 88), "det K = 12")
c = sp.symbols("c")
Ks = sp.Matrix([[8, 4, 4], [4, 7, 3], [4, 3, c]])
ok(sp.expand(Ks.det()) == 40 * c - 88, "sympy det 40c - 88")
ok(sp.solve(Ks.det(), c) == [sp.Rational(11, 5)], "sympy root 2.2")
K0n = Ks.subs(c, sp.Rational(11, 5))
ns = K0n.nullspace()[0]
ok(list(ns / ns[2]) == [sp.Rational(-2, 5), sp.Rational(-1, 5), 1], "sympy null vector")
for cv, pd in ((2.0, False), (2.2, False), (2.5, True)):
    ev = np.linalg.eigvalsh(np.array([[8, 4, 4], [4, 7, 3], [4, 3, cv]]))
    ok((ev.min() > 1e-12) == pd, f"eigvalsh positive definite at c={cv}: {pd}")
wn = np.array([-0.4, -0.2, 1.0])
ok(np.isclose(wn @ Kn @ wn, 0.3) and np.allclose(Kn @ wn, [0, 0, 0.3]), "numpy w'Kw = 0.3")
wsn = np.array([0.4, 0.2, 1.0])
ok(np.isclose(wsn @ Kn @ wsn, 9.1), "numpy sign slip 9.1")
beta = np.linalg.solve(Kn[:2, :2], Kn[:2, 2])
ok(np.allclose(beta, [0.4, 0.2]), "regression slopes (0.4, 0.2)")
res = Kn[2, 2] - Kn[2, :2] @ beta
ok(np.isclose(res, 0.3) and np.isclose(1 - res / 2.5, 0.88), "residual 0.3, R^2 0.88")
K0f = np.array(K0n.evalf().tolist(), float)
sv = np.linalg.svd(K0f)[2][-1]
ok(np.allclose(sv / sv[2], [-0.4, -0.2, 1]), "SVD null vector")
print("ALL OK")
