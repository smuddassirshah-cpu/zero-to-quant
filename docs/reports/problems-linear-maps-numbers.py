"""Recompute every stated number in linear-maps problems-1 to problems-4.

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

# Fix pass (second read, finding 1, 2, 6, 8, 11)
_s, _t = 1, -1  # w = (2s, t, -3s - t, s)
vcheck("FP-1 hedge basis b1 = (s,t)=(1,-1)", [2 * _s, _t, -3 * _s - _t, _s], [2, -1, -2, 1])
vcheck("FP-1 (s,t)=(0,1)", [0, 1, -1, 0], [0, 1, -1, 0])
vcheck("FP-2 u (+) (-4,-30)", add(u, np.array([-4, -30])), [-3, -40]); vcheck("FP-2 alt", np.array([0, 0]) - cc, [-3, -40])
_Pm = sp.Matrix([[1, 2], [1, 3]]); _Ti = sp.Matrix([[F(1, 3), -F(2, 3)], [0, F(1, 2)]])
vcheck("FP-8 entrywise slip coords", list(sp.Matrix([[F(1, 3), F(1, 4)], [0, F(1, 2)]]) * sp.Matrix([7, 2])), [F(17, 6), 1])
vcheck("FP-8 entrywise slip position", list(_Pm * sp.Matrix([[F(1, 3), F(1, 4)], [0, F(1, 2)]]) * sp.Matrix([7, 2])), [F(29, 6), F(35, 6)])
vcheck("FP-8 key", list(_Pm * _Ti * sp.Matrix([7, 2])), [3, 4])
vcheck("FP-11 carried-three", [5 * 11 + 2, 4 * 11 + 2], [57, 46]); vcheck("FP-11 key", [5 * 11 + 12, 4 * 11 + 12], [67, 56])
_pp = sp.symbols("tt"); _p0 = 3 * _pp - 1 + 2 * (_pp - 2) ** 2
check("FP-6 deg<=2 line: p(0)=7 gives lambda 2", _p0.subs(_pp, 0), 7)

# ---------------------------------------------------------------- level 4
# problems-4: route 1 exact (sympy, complex where needed), route 2 numpy.
I_ = sp.I


def ccheck(name, a, b):
    """Exact equality of sympy (possibly complex) vectors or scalars."""
    a = sp.Matrix(a) if isinstance(a, (list, tuple)) else a
    b = sp.Matrix(b) if isinstance(b, (list, tuple)) else b
    ok = sp.simplify(a - b) == (sp.zeros(*a.shape) if hasattr(a, "shape") else 0)
    if not ok:
        fails.append(name)
    print(("ok  " if ok else "FAIL"), name, a, b)


def cdiffers(name, key, wrongs):
    for w in wrongs:
        if sp.simplify(sp.Matrix(key) - sp.Matrix(w)) == sp.zeros(len(key), 1):
            fails.append(name + " wrong==key " + str(w))
    print("ok   wrongs differ:", name)


# p-footbridge-modes
S4 = sp.Matrix([[6, 2 + I_], [2 - I_, 2]])
ccheck("L4 S self-adjoint", S4.H, S4)
v4 = sp.Matrix([1, 0])
Sv = S4 * v4; S2v = S4 * Sv
ccheck("L4 Sv", Sv, [6, 2 - I_]); ccheck("L4 S^2 v", S2v, [41, 16 - 8 * I_])
aa, bb = sp.symbols("aa bb")
sol4 = sp.solve(list(S2v - aa * Sv - bb * v4), [aa, bb], dict=True)[0]
ccheck("L4 (a,b) exact", [sol4[aa], sol4[bb]], [8, -7])
Sn = np.array([[6, 2 + 1j], [2 - 1j, 2]]); vn = np.array([1, 0])
abn = np.linalg.lstsq(np.column_stack([Sn @ vn, vn]), Sn @ Sn @ vn, rcond=None)[0]
vcheck("L4 (a,b) numpy lstsq", abn.real, [8, -7]); check("L4 (a,b) imag 0", np.abs(abn.imag).max(), 0, 1e-12)
# slips: (2+i)(2-i) taken as 3 -> first entry 39 -> b = 39 - 48; sign slip b = +7
vcheck("L4 slip i-squared", [8, 39 - 48], [8, -9]); cdiffers("L4 part1", [8, -7], [[8, -9], [8, 7]])
zz = sp.symbols("zz")
roots4 = sorted(sp.solve(zz**2 - 8 * zz + 7, zz))
vcheck("L4 roots exact", roots4, [1, 7]); vcheck("L4 eigvals numpy", sorted(np.linalg.eigvalsh(Sn)), [1, 7])
vcheck("L4 roots of z^2+8z+7 (signs slip)", sorted(sp.solve(zz**2 + 8 * zz + 7, zz)), [-7, -1])
w4 = (S4 - sp.eye(2)) * v4
ccheck("L4 w = (S-I)v", w4, [5, 2 - I_]); ccheck("L4 S w = 7 w", S4 * w4, 7 * w4)
ccheck("L4 (S-7I)(S-I)v = 0", (S4 - 7 * sp.eye(2)) * w4, [0, 0])
ccheck("L4 slip other-factor (S-7I)v", (S4 - 7 * sp.eye(2)) * v4, [-1, 2 - I_])
ccheck("L4 slip plus (S+I)v", (S4 + sp.eye(2)) * v4, [7, 2 - I_])
cdiffers("L4 part3", [5, 2 - I_], [[-1, 2 - I_], [7, 2 - I_]])
u1 = sp.symbols("u1")
ipc = lambda p, q: sum(pi * sp.conjugate(qi) for pi, qi in zip(p, q))
u4 = sp.Matrix([sp.solve(ipc([u1, 5], list(w4)), u1)[0], 5])
ccheck("L4 u perpendicular, second entry 5", u4, [-2 - I_, 5]); ccheck("L4 S u = u", S4 * u4, u4)
null1 = (S4 - sp.eye(2)).nullspace()[0]; null1 = null1 * 5 / null1[1]
ccheck("L4 u by kernel of S - I (route 2)", null1, u4)
u_nc = sp.Matrix([sp.solve(u1 * w4[0] + 5 * w4[1], u1)[0], 5])
ccheck("L4 slip no-conjugate", u_nc, [-2 + I_, 5]); check("L4 slip no-conjugate is not eigen", int((S4 * u_nc - u_nc).norm() == 0), 0)
cdiffers("L4 part4", [-2 - I_, 5], [[-2 + I_, 5], [2 + I_, 5]])
nw2 = sp.simplify(ipc(list(w4), list(w4))); nu2 = sp.simplify(ipc(list(u4), list(u4)))
check("L4 |w|^2", nw2, 30); check("L4 |u|^2", nu2, 30)
frac = sp.Rational(7) * sp.Abs(w4[0])**2 / nw2 / S4[0, 0]
check("L4 fraction exact 35/36", frac, sp.Rational(35, 36))
vals, vecs = np.linalg.eigh(Sn)
check("L4 fraction numpy eigh", vals[1] * abs(vecs[0, 1])**2 / Sn[0, 0].real, 35 / 36)
check("L4 decomposition S11", 7 * sp.Rational(25, 30) + 1 * sp.Abs(u4[0])**2 / nu2, 6)
check("L4 key band takes 0.972", int(abs(0.972 - 0.9722) <= 0.0005 and abs(35 / 36 - 0.9722) <= 0.0005), 1)
for nm, wv, true in [("weight", 0.833, 5 / 6), ("trace-share", 0.875, 7 / 8), ("power", 5.833, 35 / 6)]:
    check("L4 slip " + nm + " band holds its slip", int(abs(wv - true) <= 0.001), 1)
    check("L4 slip " + nm + " outside key band", int(abs(wv - 0.9722) > 0.0005 + 0.001), 1)

# p-spring-linkage
K4 = sp.Matrix([[4, -2, 2], [-2, 5, 0], [2, 0, 3]])
ccheck("L4 K symmetric", K4.T, K4)
qa, qb, qc = sp.Matrix([1, 2, 2]), sp.Matrix([2, 1, -2]), sp.Matrix([2, -2, 1])
ccheck("L4 K a = 4a", K4 * qa, 4 * qa); ccheck("L4 K b = b", K4 * qb, qb); ccheck("L4 K c = 7c", K4 * qc, 7 * qc)
Kn = np.array(K4.tolist(), dtype=float)
vcheck("L4 K eigenvalues numpy", np.linalg.eigvalsh(Kn), [1, 4, 7])
nb = (K4 - sp.eye(3)).nullspace(); check("L4 dim ker(K-I) = 1", len(nb), 1)
ccheck("L4 eigvec for 1, first entry 2", nb[0] * 2 / nb[0][0], qb)
vcheck("L4 slip entry K(1,2,2)[1]", [(K4 * qa)[1]], [8]); check("L4 trace", K4.trace(), 12)
ccheck("L4 K(2,-1,0)", K4 * sp.Matrix([2, -1, 0]), [10, -9, 4]); check("L4 (2,-1,0) in plane", qa.dot(sp.Matrix([2, -1, 0])), 0)
cdiffers("L4 spring part2", [2, 1, -2], [[2, -1, 0], [2, -1, -2]])
cr = qa.cross(qb); ccheck("L4 cross product", cr, [-6, 6, -3]); ccheck("L4 third eigvec scaled", cr * 2 / cr[0], qc)
check("L4 (1,2,2).(2,2,1)", qa.dot(sp.Matrix([2, 2, 1])), 8)
cdiffers("L4 spring part3", [2, -2, 1], [[2, 2, 1], [-6, 6, -3]])
ccheck("L4 K(2,-2,1)", K4 * qc, [14, -14, 7]); check("L4 trace route", 12 - 4 - 1, 7)
F4 = sp.Matrix([28, 0, 0])
x_sp = sum([((F4.dot(q / 3)) / lam) * (q / 3) for q, lam in [(qa, 4), (qb, 1), (qc, 7)]], sp.zeros(3, 1))
ccheck("L4 x spectral sum", x_sp, [15, 6, -10]); ccheck("L4 x = K^-1 F (route 2)", K4.LUsolve(F4), [15, 6, -10])
vcheck("L4 x numpy solve", np.linalg.solve(Kn, [28, 0, 0]), [15, 6, -10])
vcheck("L4 coefficients <F,q_i>", [F4.dot(q / 3) for q in (qa, qb, qc)], [F(28, 3), F(56, 3), F(56, 3)])
ccheck("L4 slip times = K F", K4 * F4, [112, -56, 56])
ccheck("L4 slip unit (no 1/3)", sum([((F4.dot(q)) / lam) * q for q, lam in [(qa, 4), (qb, 1), (qc, 7)]], sp.zeros(3, 1)), [135, 54, -90])
ccheck("L4 explain K x", K4 * sp.Matrix([15, 6, -10]), [28, 0, 0])
cdiffers("L4 spring part5", [15, 6, -10], [[112, -56, 56], [135, 54, -90]])

# p-curvature-operator: T p = p + p'' on P_3, basis (1, x, x^2, x^3)
basis4 = [sp.Integer(1), x, x**2, x**3]
Tp4 = lambda p: sp.expand(p + sp.diff(p, x, 2))
coords = lambda p: [sp.Poly(p, x).coeff_monomial(x**k) for k in range(4)]
MT4 = sp.Matrix([coords(Tp4(b)) for b in basis4]).T
vcheck("L4 coords T(x^3)", coords(Tp4(x**3)), [0, 6, 0, 1])
vcheck("L4 slip one-derivative", coords(sp.expand(x**3 + sp.diff(x**3, x))), [0, 0, 3, 1])
cdiffers("L4 curv part1", [0, 6, 0, 1], [[0, 0, 3, 1], [0, 3, 0, 1]])
N4 = MT4 - sp.eye(4)
d1, d2, d3 = [4 - (N4**k).rank() for k in (1, 2, 3)]
vcheck("L4 (d1, d2) exact", [d1, d2], [2, 4]); check("L4 d3", d3, 4)
Nn = np.array(N4.tolist(), dtype=float)
vcheck("L4 (d1, d2) numpy", [4 - np.linalg.matrix_rank(np.linalg.matrix_power(Nn, k)) for k in (1, 2)], [2, 4])
check("L4 dim ker by hand: p''=0 iff p in span(1,x)", len([b for b in basis4 if sp.diff(b, x, 2) == 0]), 2)
cdiffers("L4 curv part2", [2, 4], [[1, 2], [4, 4]])
dd = [0, d1, d2, d3]; atleast = [dd[k] - dd[k - 1] for k in (1, 2, 3)]
sizes = sorted([k for k in (1, 2, 3) for _ in range(atleast[k - 1] - (atleast[k] if k < 3 else 0))])
vcheck("L4 block sizes", sizes, [2, 2])
J4 = sp.Matrix(sp.BlockDiagMatrix(sp.Matrix([[1, 1], [0, 1]]), sp.Matrix([[1, 1], [0, 1]])))
Pj, Jj = MT4.jordan_form(); ccheck("L4 sympy jordan_form", Jj, J4)
# J_3(1)+J_1(1): d = (2, 3), so the slip 3,1 is refused by d2 = 4
J31 = sp.Matrix(sp.BlockDiagMatrix(sp.Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]]), sp.Matrix([[1]])))
vcheck("L4 slip three-one has d=(2,3)", [4 - (J31 - sp.eye(4)).rank(), 4 - ((J31 - sp.eye(4))**2).rank()], [2, 3])
vcheck("L4 (alg, geom)", [sum(sizes), len(sizes)], [4, 2])
check("L4 char poly", sp.expand(MT4.charpoly(zz).as_expr() - (zz - 1)**4), 0)
Pc = sp.Matrix([coords(6 * x), coords(x**3), coords(sp.Integer(2)), coords(x**2)]).T
ccheck("L4 chain basis (6x, x^3, 2, x^2) gives J", Pc.inv() * MT4 * Pc, J4)
tt = sp.symbols("tt", integer=True, positive=True)
pw = sp.expand(x**3 + tt * 6 * x)
for tv in range(1, 7):
    p_ = x**3
    for _ in range(tv):
        p_ = Tp4(p_)
    check(f"L4 T^{tv}(x^3) by repeated T", sp.expand(p_ - pw.subs(tt, tv)), 0)
    vcheck(f"L4 T^{tv} by matrix power", list((MT4**tv) * sp.Matrix([0, 0, 0, 1])), [0, 6 * tv, 0, 1])
check("L4 slip no-t differs at t=2", int(sp.expand((x**3 + 6 * x) - pw.subs(tt, 2)) != 0), 1)
check("L4 slip power differs at t=2", int(sp.expand((x**3 + 6**2 * x) - pw.subs(tt, 2)) != 0), 1)

# keys stored in problems-4.json read back
d4 = json.load(open(os.path.join(CDIR, "problems-4.json")))
want4 = {
    "p-footbridge-modes": [[8, -7], [1, 7], [5, 2 - I_], [-2 - I_, 5], 35 / 36],
    "p-spring-linkage": [4, [2, 1, -2], [2, -2, 1], 7, [15, 6, -10]],
    "p-curvature-operator": [[0, 6, 0, 1], [2, 4], [2, 2], [4, 2], pw],
}
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
TR = standard_transformations + (implicit_multiplication_application,)
for it in d4["items"]:
    for k, (part, want) in enumerate(zip(it["parts"], want4[it["id"]]), 1):
        wd = part["widget"]; name = f"key problems-4 {it['id']} part {k}"
        if "answers" in wd:
            vcheck(name, sorted(wd["answers"]), sorted(want))
        elif isinstance(wd["answer"], (int, float)):
            check(name, wd["answer"], want, wd["tol"]["abs"] + 1e-12)
        else:
            s_ = wd["answer"].strip()
            if s_.startswith("("):
                ents = [parse_expr(e.replace("i", "I"), transformations=TR) for e in s_[1:-1].split(",")]
                ccheck(name, ents, want)
            else:
                got = parse_expr(s_.replace("^", "**").replace("6tx", "6*tt*x"), local_dict={"x": x, "tt": tt}, transformations=TR)
                check(name, sp.expand(got - want), 0)
check("L4 every part keyed", sum(len(i["parts"]) for i in d4["items"]), 15)

print("\n%d failures" % len(fails))
for f_ in fails:
    print("  ", f_)
sys.exit(1 if fails else 0)
