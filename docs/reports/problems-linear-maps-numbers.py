"""Recompute every stated number in linear-maps problems-1 to problems-3.

Each answer is found twice: exactly (sympy) and by a second, independent
route (numpy least squares, direct substitution, or brute-force search).
Each wrong value is shown to differ from its key. Exit 0 when all hold.
"""
import sys
from fractions import Fraction as F
import numpy as np
import sympy as sp

fails = []


def check(name, a, b, tol=1e-9):
    ok = abs(float(a) - float(b)) <= tol
    if not ok:
        fails.append(name)
    print(("ok  " if ok else "FAIL"), name, a, b)


def vcheck(name, a, b, tol=1e-9):
    a = np.array(a, dtype=float); b = np.array(b, dtype=float)
    ok = a.shape == b.shape and np.allclose(a, b, atol=tol)
    if not ok:
        fails.append(name)
    print(("ok  " if ok else "FAIL"), name, a.tolist(), b.tolist())


def differs(name, key, wrongs, tol=0.0):
    for w in wrongs:
        k = np.array(key, dtype=float); v = np.array(w, dtype=float)
        same = k.shape == v.shape and np.allclose(k, v, atol=tol + 1e-12)
        if same:
            fails.append(name + " wrong==key " + str(w))
    print("ok   wrongs differ:", name)


x, t = sp.symbols("x t")

# ===================== Level 1 =====================
# P1-1 hedge baskets
M = sp.Matrix([[1, 1, 1, 1], [1, 0, 0, -2]])          # cash-neutral, w1 = 2 w4
check("P1-1 dim U (4 - rank)", 4 - M.rank(), 4 - np.linalg.matrix_rank(np.array(M, float)))
b1 = sp.Matrix([2, -1, -2, 1]); b2 = sp.Matrix([0, 1, -1, 0])
vcheck("P1-1 b1,b2 in U", list(M * b1) + list(M * b2), [0, 0, 0, 0])
w = sp.Matrix([4, 3, -9, 2])
sol = sp.Matrix.hstack(b1, b2).solve_least_squares(w)
lst = np.linalg.lstsq(np.array([[2, 0], [-1, 1], [-2, -1], [1, 0]], float), np.array([4, 3, -9, 2], float), rcond=None)[0]
vcheck("P1-1 coords of w", list(sol), lst); vcheck("P1-1 coords exact", list(sol), [2, 5])
vcheck("P1-1 w in span", list(2 * b1 + 5 * b2), list(w))
differs("P1-1 p3", [2, 5], [[5, 2], [4, 3]])
# rule options: only w1 = 2 w4 keeps zero / sums / multiples
z = np.zeros(4)
check("P1-1 opt const fails zero", float(z[0] - (2 * z[3] + 0.1)) != 0, 1)
p, q = np.array([1, -1, 0, 0]), np.array([0, 1, 0, -1])
check("P1-1 opt product: sum breaks", (p + q)[0] * (p + q)[3], -1)
Mw = sp.Matrix([[1, 1, 1, 1], [1, 0, 0, -2], [0, 1, -1, 0]])  # U cap W
ns = Mw.nullspace()[0]; ns = ns / ns[3] * 2
vcheck("P1-1 U cap W, w4 = 2", list(ns), [4, -3, -3, 2])
wv = np.array([4, -3, -3, 2]); check("P1-1 sum zero", wv.sum(), 0)
differs("P1-1 p4", [4, -3, -3, 2], [[4, -2, -2, 2], [1, -1.5, -1.5, 2]])
MW = sp.Matrix([[1, 1, 1, 1], [0, 1, -1, 0]])
dimU, dimW, dimI = 4 - M.rank(), 4 - MW.rank(), 4 - Mw.rank()
basisU = M.nullspace(); basisW = MW.nullspace()
dimSum = sp.Matrix.hstack(*(basisU + basisW)).rank()
check("P1-1 dim(U+W) formula", dimU + dimW - dimI, 3); check("P1-1 dim(U+W) span", dimSum, 3)
differs("P1-1 p5", [3], [[4], [5], [1]]); differs("P1-1 p2", [2], [[3], [4], [1]])

# P1-2 hedge curves
p1, p2, p3 = 3 + x + x**2, x - 2 * x**2, 1 + x**2
a, b, c, k = sp.symbols("a b c k")
s = sp.solve(sp.Poly(p1 - a * p2 - b * p3, x).all_coeffs(), [a, b])
vcheck("P1-2 p1 = a p2 + b p3", [s[a], s[b]], [1, 3]); check("P1-2 direct", sp.expand(p2 + 3 * p3 - p1), 0)
differs("P1-2 p1", [1, 3], [[3, 1], [-1, -3]])
C = np.array([[3, 0, 1], [1, 1, 0], [1, -2, 1]], float)   # columns p1,p2,p3 coefficients (1,x,x^2)
check("P1-2 dim span", np.linalg.matrix_rank(C), 2); check("P1-2 dim span exact", sp.Matrix(C.astype(int)).rank(), 2)
differs("P1-2 p2", [2], [[3], [1]])
ks = sp.solve(sp.Poly(4 + k * x + 6 * x**2 - a * p2 - b * p3, x).all_coeffs(), [a, b, k])
check("P1-2 k", ks[k], -1)
found = [kk for kk in range(-10, 11) if np.linalg.matrix_rank(np.column_stack([C[:, 1], C[:, 2], [4, kk, 6]])) == 2]
check("P1-2 k search", found[0], -1); check("P1-2 k unique", len(found), 1)
differs("P1-2 p3", [-1], [[1], [-2], [2]])
for cand, inspan in [(2 + x, True), (x**2, False), (x, False), (1 + x, False)]:
    co = sp.Poly(cand, x).all_coeffs()[::-1] + [0] * 3
    r = np.linalg.matrix_rank(np.column_stack([C[:, 1], C[:, 2], [float(v) for v in co[:3]]]))
    check(f"P1-2 option {cand} in span", r == 2, inspan)
check("P1-2 2+x = p2 + 2 p3", sp.expand(p2 + 2 * p3 - (2 + x)), 0)
q = 5 - x + 4 * x**2
s5 = sp.solve(sp.Poly(q - a * p2 - b * p3 - c * x**2, x).all_coeffs(), [a, b, c])
vcheck("P1-2 coords q", [s5[a], s5[b], s5[c]], [-1, 5, -3])
B3 = np.array([[0, 1, 0], [1, 0, 0], [-2, 1, 1]], float)
vcheck("P1-2 coords q numeric", np.linalg.solve(B3, [5, -1, 4]), [-1, 5, -3])
differs("P1-2 p5", [-1, 5, -3], [[5, -1, 4], [5, -1, -3], [-1, 5, -1]])

# P1-3 scenario space with origin c
cc = np.array([3, 40]); u = np.array([4, 30]); v = np.array([5, 60])
add = lambda p, q: cc + (p - cc) + (q - cc)
smul = lambda l, p: cc + l * (p - cc)
vcheck("P1-3 u+v", add(u, v), [6, 50]); vcheck("P1-3 u+v alt", u + v - cc, [6, 50])
differs("P1-3 p1", [6, 50], [[9, 90], [3, 10]])
vcheck("P1-3 zero", add(u, cc), u); vcheck("P1-3 zero other", add(v, cc), v)
differs("P1-3 p2", [3, 40], [[0, 0]])
inv = 2 * cc - u; vcheck("P1-3 inverse", inv, [2, 50]); vcheck("P1-3 inverse = (-1).u", smul(-1, u), [2, 50])
vcheck("P1-3 inverse check", add(u, inv), cc); differs("P1-3 p3", [2, 50], [[-4, -30], [-1, 10]])
vcheck("P1-3 option s>=... (-1).u", smul(-1, u), [2, 50])
vcheck("P1-3 option union sum", add(np.array([4, 40]), np.array([3, 50])), [4, 50])
Am = sp.Matrix([[1, 2], [-10, 20]]); sab = Am.solve(sp.Matrix([5, 30]))
vcheck("P1-3 coords", list(sab), [1, 2]); vcheck("P1-3 coords check", add(smul(1, u), smul(2, v)), [8, 70])
vcheck("P1-3 2.v", smul(2, v), [7, 80])
usual = sp.Matrix([[4, 5], [30, 60]]).solve(sp.Matrix([8, 70]))
vcheck("P1-3 usual slip", list(usual), [F(13, 9), F(4, 9)])
differs("P1-3 p5", [1, 2], [[13 / 9, 4 / 9], [2, 1]])

# ===================== Level 2 =====================
# P2-1 T(p) = (p(2), p'(2)) on P3
T = lambda pp: (pp.subs(t, 2), sp.diff(pp, t).subs(t, 2))
vcheck("P2-1 T(t^3)", T(t**3), [8, 12]); vcheck("P2-1 T(t^3) alt", [2**3, 3 * 2**2], [8, 12])
differs("P2-1 p1", [8, 12], [[8, 6], [12, 8]])
Mat = sp.Matrix([[T(t**j)[i] for j in range(4)] for i in range(2)])
vcheck("P2-1 matrix", np.array(Mat, float).ravel(), [1, 2, 4, 8, 0, 1, 4, 12])
for name, wm in [("unevaluated", [1, 2, 4, 8, 0, 1, 2, 3]), ("rows", [0, 1, 4, 12, 1, 2, 4, 8]), ("carried", [1, 2, 4, 8, 0, 1, 4, 6])]:
    differs("P2-1 p2 " + name, [1, 2, 4, 8, 0, 1, 4, 12], [wm])
check("P2-1 nullity", 4 - Mat.rank(), 2); check("P2-1 nullity numeric", len(Mat.nullspace()), 2)
vcheck("P2-1 null basis", list(T((t - 2)**2)) + list(T(t * (t - 2)**2)), [0, 0, 0, 0])
differs("P2-1 p3", [2], [[1], [4]])
a0, a1, lam = sp.symbols("a0 a1 lam")
s4 = sp.solve([e - r for e, r in zip(T(a0 + a1 * t), (5, 3))], [a0, a1])
vcheck("P2-1 p0", [s4[a0], s4[a1]], [-1, 3]); vcheck("P2-1 p0 check", T(3 * t - 1), [5, 3])
check("P2-1 slip 3t+5 level", T(3 * t + 5)[0], 11)
lv = sp.solve((3 * t - 1 + lam * (t - 2)**2).subs(t, 0) - 7, lam)[0]
check("P2-1 lambda", lv, 2)
pfin = sp.expand(3 * t - 1 + 2 * (t - 2)**2)
check("P2-1 final poly", sp.expand(pfin - (2 * t**2 - 5 * t + 7)), 0); vcheck("P2-1 final T", T(pfin), [5, 3])
check("P2-1 final p(0)", pfin.subs(t, 0), 7)
pn = np.polyfit([0, 1, 2, 3], [float(pfin.subs(t, s_)) for s_ in range(4)], 2)
vcheck("P2-1 final numeric", pn, [2, -5, 7], 1e-8)
check("P2-1 slip no-p0 p(0)", (3 * t - 1 + sp.Rational(7, 4) * (t - 2)**2).subs(t, 0), 6)
check("P2-1 slip 3t+7 level", T(3 * t + 7)[0], 13)

# P2-2 futures exposure
A = sp.Matrix([[1, 2], [-1, 4]]); P = sp.Matrix([[1, 2], [1, 3]])
vcheck("P2-2 T b1", list(A * P[:, 0]), [3, 3])
vcheck("P2-2 T b2", list(A * P[:, 1]), [8, 10])
cb2 = P.solve(A * P[:, 1]); vcheck("P2-2 [T b2]_B", list(cb2), [4, 2])
vcheck("P2-2 [T b2]_B numeric", np.linalg.solve(np.array(P, float), np.array(A * P[:, 1], float).ravel()), [4, 2])
differs("P2-2 p1", [4, 2], [[8, 10], [2, 4]])
TB = P.inv() * A * P; vcheck("P2-2 [T]_B", list(TB), [3, 4, 0, 2])
vcheck("P2-2 [T]_B numeric", (np.linalg.inv(np.array(P, float)) @ np.array(A, float) @ np.array(P, float)).ravel(), [3, 4, 0, 2])
differs("P2-2 p2", [3, 4, 0, 2], [[1, 2, -1, 4], [3, 0, 4, 2]])
check("P2-2 det", TB.det(), 6); check("P2-2 det A", A.det(), 6)
TBi = TB.inv(); vcheck("P2-2 [T^-1]_B", list(TBi), [F(1, 3), F(-2, 3), 0, F(1, 2)])
vcheck("P2-2 [T^-1]_B numeric", np.linalg.inv(np.array(TB, float)).ravel(), [1 / 3, -2 / 3, 0, 1 / 2])
differs("P2-2 p3", [1 / 3, -2 / 3, 0, 1 / 2], [[1 / 3, 1 / 4, 0, 1 / 2], [1 / 3, 2 / 3, 0, 1 / 2]])
wv2 = sp.Matrix([11, 13]); vB = P.solve(wv2); vcheck("P2-2 [(11,13)]_B", list(vB), [7, 2])
xB = TBi * vB; vcheck("P2-2 [T^-1 w]_B", list(xB), [1, 1])
pos = P * xB; vcheck("P2-2 position", list(pos), [3, 4])
vcheck("P2-2 position numeric", np.linalg.solve(np.array(A, float), [11, 13]), [3, 4])
vcheck("P2-2 slip A(11,13)", list(A * wv2), [37, 41])
slip = P * (sp.Matrix([[F(1, 3), F(2, 3)], [0, F(1, 2)]]) * vB); vcheck("P2-2 slip carried-sign", list(slip), [F(17, 3), F(20, 3)])
differs("P2-2 p4", [3, 4], [[1, 1], [37, 41], [17 / 3, 20 / 3]])

# P2-3 T p = p - p' on P2
Tp = lambda pp: sp.expand(pp - sp.diff(pp, x))
check("P2-3 T(x^2)", sp.expand(Tp(x**2) - (x**2 - 2 * x)), 0)
check("P2-3 T(3x^2 + x)", sp.expand(Tp(3 * x**2 + x) - (3 * x**2 - 5 * x - 1)), 0)
vcheck("P2-3 T(3x^2 + x) by basis images", [3 * 0 + 0 - 1, 3 * (-2) + 1, 3], [-1, -5, 3])  # 3T(x^2) + T(x): coeffs of 1, x, x^2
check("P2-3 slip power", sp.expand(3 * x**2 + x - (3 * x + 1) - (3 * x**2 - 2 * x - 1)), 0)
MT = sp.Matrix([[sp.Poly(Tp(x**j), x).coeff_monomial(x**i) for j in range(3)] for i in range(3)])
check("P2-3 nullity", 3 - MT.rank(), 0); check("P2-3 rank", np.linalg.matrix_rank(np.array(MT, float)), 3)
check("P2-3 option p(0) kills x", (x).subs(x, 0), 0)
vcheck("P2-3 option (a+b,a+b) kills (1,-1)", [1 - 1, 1 - 1], [0, 0])
differs("P2-3 p3", [3], [[2], [0]])
cs = MT.solve(sp.Matrix([3, 0, 1])); vcheck("P2-3 solve", list(cs), [5, 2, 1])
check("P2-3 solve check", sp.expand(Tp(x**2 + 2 * x + 5) - (x**2 + 3)), 0)
q3 = x**2 + 3; check("P2-3 T^-1 = I + D + D^2", sp.expand(q3 + sp.diff(q3, x) + sp.diff(q3, x, 2) - (x**2 + 2 * x + 5)), 0)
check("P2-3 slip one-step", sp.expand(Tp(x**2 + 2 * x + 3) - (x**2 + 1)), 0)
check("P2-3 slip applied-T", sp.expand(Tp(q3) - (x**2 - 2 * x + 3)), 0)

# ===================== Level 3 =====================
# P3-1 duals
V = sp.Matrix([[5, 4], [1, 1]]); Vi = V.inv()
vcheck("P3-1 V^-1", list(Vi), [1, -4, -1, 5])
vcheck("P3-1 phi_j(v_k)", list(Vi * V), [1, 0, 0, 1])
vcheck("P3-1 phi1 numeric", np.linalg.solve(np.array(V.T, float), [1, 0]), [1, -4])
vcheck("P3-1 phi2 numeric", np.linalg.solve(np.array(V.T, float), [0, 1]), [-1, 5])
check("P3-1 slip 5x+y on v2", 5 * 4 + 1, 21); check("P3-1 slip 4x+y on v1", 4 * 5 + 1, 21)
check("P3-1 phi1+phi2 = y on v1, v2", (1 - 1) * 5 + (-4 + 5) * 1, 1)
y = sp.symbols("y")
psi = 3 * x + 5 * y
Tpsi = sp.expand(psi.subs({x: 2 * x - y, y: x + 3 * y}, simultaneous=True))
check("P3-1 T'psi", sp.expand(Tpsi - (11 * x + 12 * y)), 0)
AT = np.array([[2, -1], [1, 3]], float)
vcheck("P3-1 T'psi = A^T(3,5)", AT.T @ [3, 5], [11, 12]); vcheck("P3-1 slip A(3,5)", AT @ [3, 5], [1, 18])
vcheck("P3-1 slip dropped-three", [3 * 2 + 5, -3 + 5], [11, 2])
c1 = Tpsi.subs({x: 5, y: 1}); c2 = Tpsi.subs({x: 4, y: 1})
vcheck("P3-1 dual coords", [c1, c2], [67, 56])
vcheck("P3-1 dual coords alt", np.linalg.solve(np.array(Vi.T, float), [11, 12]), [67, 56])
check("P3-1 dual coords check", sp.expand(67 * (x - 4 * y) + 56 * (5 * y - x) - Tpsi), 0)
vcheck("P3-1 carried slip", [1 * 5 + 18, 1 * 4 + 18], [23, 22])
differs("P3-1 p4", [67, 56], [[11, 12], [56, 67], [23, 22]])
G = np.diag([2.0, 1.0]); ur = np.linalg.solve(G, [11, 12])
vcheck("P3-1 Riesz", ur, [5.5, 12]); vcheck("P3-1 Riesz exact", list(sp.diag(2, 1).solve(sp.Matrix([11, 12]))), [F(11, 2), 12])
differs("P3-1 p5", [5.5, 12], [[11, 12], [22, 12]])

# P3-2 index beta
av = np.array([1, -1, 0, 1, -1]); bv = np.array([3, 0, -2, 2, -3])
check("P3-2 means zero", abs(av.sum()) + abs(bv.sum()), 0)
ip = lambda p, q: F(int(np.dot(p, q)), 4)
check("P3-2 cov", ip(av, bv), 2); check("P3-2 cov numpy", np.cov(av, bv)[0, 1], 2)
differs("P3-2 p1", [2], [[8], [1.6]])
rho = float(ip(av, bv)) / np.sqrt(float(ip(av, av) * ip(bv, bv)))
check("P3-2 corr", round(rho, 3), 0.784); check("P3-2 corr numpy", round(np.corrcoef(av, bv)[0, 1], 3), 0.784)
check("P3-2 var b", ip(bv, bv), F(13, 2))
check("P3-2 slip squared", round(rho**2, 3), 0.615); check("P3-2 slip one-norm", round(2 / 6.5, 3), 0.308)
beta = ip(bv, av) / ip(av, av); check("P3-2 beta", beta, 2)
check("P3-2 beta polyfit", np.polyfit(av, bv, 1)[0], 2)
r = bv - 2 * av; vcheck("P3-2 residual", r, [1, 2, -2, 0, -1]); check("P3-2 residual orth", np.dot(r, av), 0)
differs("P3-2 p3", [1, 2, -2, 0, -1], [[2, 1, -2, 1, -2], [-5, 8, -2, -6, 5], [-1, -2, 2, 0, 1]])
vcheck("P3-2 slip b-8a", bv - 8 * av, [-5, 8, -2, -6, 5])
share = 1 - ip(r, r) / ip(bv, bv); check("P3-2 share exact", share, F(8, 13))
check("P3-2 share 3dp", round(float(share), 3), 0.615); check("P3-2 share = rho^2", float(share), rho**2, 1e-12)
check("P3-2 Pythagoras", ip(bv, bv), 4 * ip(av, av) + ip(r, r))
check("P3-2 slip residual share", round(1 - float(share), 3), 0.385)
check("P3-2 0.784^2 printed", round(0.784**2, 3), 0.615)

# P3-3 two-signal fit
u1 = np.array([1, 1, 0, 1]); u2 = np.array([2, 1, 1, 3]); vv = np.array([4, 2, 5, 3])
bt = F(int(u2 @ u1), int(u1 @ u1)); check("P3-3 beta", bt, 2)
f2 = u2 - 2 * u1; vcheck("P3-3 f2", f2, [0, -1, 1, 1]); check("P3-3 f2 orth", f2 @ u1, 0)
Q, _ = np.linalg.qr(np.column_stack([u1, u2]).astype(float))
vcheck("P3-3 f2 direction (QR)", Q[:, 1] * np.sign(Q[2, 1]), f2 / np.linalg.norm(f2))
differs("P3-3 p1", [0, -1, 1, 1], [[-4, -5, 1, -3], [1, 0, 1, 2]])
proj = F(int(vv @ u1), 3) * u1 + F(int(vv @ f2), 3) * f2
vcheck("P3-3 projection", [float(e) for e in proj], [3, 1, 2, 5])
Ux = np.column_stack([u1, u2]).astype(float)
coef = np.linalg.lstsq(Ux, vv.astype(float), rcond=None)[0]
vcheck("P3-3 projection lstsq", Ux @ coef, [3, 1, 2, 5]); vcheck("P3-3 loadings", coef, [-1, 2])
vcheck("P3-3 loadings exact", list(sp.Matrix(Ux.astype(int)).solve_least_squares(sp.Matrix(vv))), [-1, 2])
vcheck("P3-3 slip not-orthogonal", 3 * u1 + F(int(vv @ u2), int(u2 @ u2)) * u2, [6.2, 4.6, 1.6, 7.8])
vcheck("P3-3 slip no-norm", 3 * u1 + 6 * f2, [3, -3, 6, 9])
differs("P3-3 p3", [-1, 2], [[3, 2], [2, -1]])
res = vv - np.array([3, 1, 2, 5]); vcheck("P3-3 residual", res, [1, 1, 3, -2])
check("P3-3 residual orth", abs(res @ u1) + abs(res @ u2), 0)
check("P3-3 distance", round(float(np.sqrt(res @ res)), 3), 3.873); check("P3-3 distance exact", sp.sqrt(15).evalf(8), 3.8729833, 1e-6)
# minimisation by brute search over a grid of U
best = min(np.linalg.norm(vv - (a_ * u1 + b_ * u2)) for a_ in np.linspace(-3, 1, 401) for b_ in np.linspace(0, 4, 401))
check("P3-3 distance grid search", round(best, 3), 3.873)
check("P3-3 slip one-signal", round(float(np.linalg.norm(vv - 3 * u1)), 3), 5.196)
differs("P3-3 p4", [3.873], [[15], [5.196]], 0.001)
check("P3-3 squared slip", res @ res, 15)

# ===================== the stored keys match the values computed above =====================
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, "..", "..", "app", "content", "courses", "linear-maps")


def parse_key(s):
    s = s.strip()
    if s[:1] in "([" and s[-1:] in ")]":
        s = s[1:-1]
    s = s.replace("\\\\", ";")
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", s)
    s = s.replace("\\begin{pmatrix}", "").replace("\\end{pmatrix}", "").replace("&", ",").replace(";", ",")
    try:
        return [float(sp.sympify(e)) for e in s.split(",")]
    except Exception:
        from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
        return parse_expr(s.replace("^", "**"), local_dict={"x": x, "y": y, "t": t},
                          transformations=standard_transformations + (implicit_multiplication_application,))


computed = {
    ("problems-1", "p-hedge-baskets"): [None, dimU, list(sol), list(ns), dimSum],
    ("problems-1", "p-hedge-curves"): [[s[a], s[b]], 2, ks[k], None, [s5[a], s5[b], s5[c]]],
    ("problems-1", "p-scenario-space"): [add(u, v), cc, inv, None, list(sab)],
    ("problems-2", "p-curve-report"): [T(t**3), list(Mat), 4 - Mat.rank(), 3 * t - 1, pfin],
    ("problems-2", "p-futures-exposure"): [list(cb2), list(TB), list(TBi), list(pos)],
    ("problems-2", "p-slope-adjusted"): [Tp(3 * x**2 + x), None, MT.rank(), x**2 + 2 * x + 5],
    ("problems-3", "p-currency-duals"): [x - 4 * y, 5 * y - x, Tpsi, [c1, c2], list(ur)],
    ("problems-3", "p-index-beta"): [ip(av, bv), round(rho, 3), list(r), round(float(share), 3)],
    ("problems-3", "p-two-signal-fit"): [list(f2), [float(e) for e in proj], list(coef), round(float(np.sqrt(res @ res)), 3)],
}
for (fid, iid), vals in computed.items():
    d = json.load(open(os.path.join(CDIR, fid + ".json")))
    item = next(i for i in d["items"] if i["id"] == iid)
    for k, (part, want) in enumerate(zip(item["parts"], vals), 1):
        if want is None:
            continue
        key = part["widget"]["answer"]
        name = f"key {fid} {iid} part {k}"
        if isinstance(key, (int, float)):
            check(name, key, want, 1e-9)
        else:
            got = parse_key(key)
            if isinstance(got, list):
                vcheck(name, got, [float(w) for w in want], 1e-9)
            else:
                check(name, sp.simplify(got - want) == 0, True)

print("\n%d failures" % len(fails))
for f_ in fails:
    print("  ", f_)
sys.exit(1 if fails else 0)
