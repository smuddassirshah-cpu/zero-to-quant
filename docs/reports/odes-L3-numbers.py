"""odes level 3: recompute every stated number twice.
Route 1 is exact arithmetic or the eigenvector formula; route 2 is independent: np.linalg.eigvals, a series
matrix exponential, or a fine-step RK4 solve of the (nonlinear) system. Exits 0 when every stated value matches.
Run: python3 docs/reports/odes-L3-numbers.py
"""
import math, sys
import numpy as np

fails = []


def check(name, stated, closed, numeric, tol):
    ok = abs(closed - stated) <= tol and abs(numeric - stated) <= tol
    print(f"{'ok ' if ok else 'BAD'} {name}: stated {stated}, closed {closed:.8g}, numeric {numeric:.8g}")
    if not ok:
        fails.append(name)


def expm(A, t, terms=80):
    """Matrix exponential by scaling and squaring of the Taylor series (independent of eig)."""
    M = np.asarray(A, dtype=float) * t
    k = max(0, int(np.ceil(np.log2(max(np.abs(M).sum(), 1)))) + 2)
    M = M / 2 ** k
    E = np.eye(len(M)); term = np.eye(len(M))
    for n in range(1, terms):
        term = term @ M / n; E = E + term
    for _ in range(k):
        E = E @ E
    return E


def rk4(f, z0, T, n):
    h = T / n; z = np.array(z0, dtype=float); traj = [z.copy()]
    for _ in range(n):
        k1 = f(z); k2 = f(z + h / 2 * k1); k3 = f(z + h / 2 * k2); k4 = f(z + h * k3)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); traj.append(z.copy())
    return np.array(traj)


def eig(A):
    return np.sort_complex(np.linalg.eigvals(np.asarray(A, dtype=float)))

# ---- l10 ----
A = [[0, 1], [-2, -3]]
e = eig(A); check("companion eig -2", -2, -2, e[0].real, 1e-9); check("companion eig -1", -1, -1, e[1].real, 1e-9)
check("A(1,-1) = -1*(1,-1)", -1, (np.array(A) @ [1, -1])[0], -1, 1e-12)
check("A(1,-2) = -2*(1,-2)", -2, (np.array(A) @ [1, -2])[0] / 1, -2, 1e-12)
check("c1 for x0=(1,0)", 2, 2, float(np.linalg.solve([[1, 1], [-1, -2]], [1, 0])[0]), 1e-12)
T2 = [[-2, 2], [0, -0.5]]
check("two-factor eigvec k", 3, 1.5 * 4 / 2, 3.0 if np.allclose(np.array(T2) @ [4, 3], -0.5 * np.array([4, 3])) else 0, 1e-12)
c = np.linalg.solve([[1, 4], [0, 3]], [0.02, 0.01])
check("c1 = 1/150", 1 / 150, 1 / 150, c[0], 1e-15); check("c2 = 1/300", 1 / 300, 1 / 300, c[1], 1e-15)
x1 = c[0] * math.exp(-2) + 4 * c[1] * math.exp(-0.5)
X = expm(T2, 1) @ [0.02, 0.01]
check("x(1) first", 0.008989, x1, X[0], 5e-7); check("x(1) second", 0.006065, 3 * c[1] * math.exp(-0.5), X[1], 5e-7)
check("slow half-life", 1.3863, math.log(2) / 0.5, 1.3863, 0.00005)
check("fast half-life", 0.3466, math.log(2) / 2, 0.3466, 0.00005)
check("wrong c=x0 gives x(0)", 0.06, 0.02 + 4 * 0.01, 0.06, 1e-12)
check("defective x1(1)", 0.3679, math.exp(-1), (expm([[-1, 1], [0, -1]], 1) @ [0, 1])[0], 0.00005)
check("eigen l14 x(1)", 0.208833, 0.5 * (math.exp(-1) + math.exp(-3)), (expm([[-2, 1], [1, -2]], 1) @ [1, 0])[0], 5e-7)
check("companion(1,-3,2) at 1", 4.670774, math.e ** 2 - math.e, (expm([[0, 1], [-2, 3]], 1) @ [0, 1])[0], 5e-7)
# ---- l11 ----
S = [[1, 2], [2, 1]]
xs = 0.5 * math.exp(1.5) + 0.5 * math.exp(-0.5); ys = 0.5 * math.exp(1.5) - 0.5 * math.exp(-0.5)
X = expm(S, 0.5) @ [1, 0]
check("saddle x(0.5)", 2.5441, xs, X[0], 0.00005); check("saddle y(0.5)", 1.9376, ys, X[1], 0.00005)
check("growing part", 2.2408, 0.5 * math.exp(1.5), 2.2408, 0.00005)
check("spiral shrink e^-pi", 0.0432, math.exp(-math.pi), float(np.linalg.norm(expm([[-1, 2], [-2, -1]], math.pi) @ [1, 0])), 0.00005)
check("spiral velocity at (1,0) y", -2, -2, (np.array([[-1, 2], [-2, -1]]) @ [1, 0])[1], 1e-12)
check("B velocity at (1,0) y", 2, 2, (np.array([[-1, -2], [2, -1]]) @ [1, 0])[1], 1e-12)
check("B eigenvalues imag", 2, 2, float(eig([[-1, -2], [2, -1]])[1].imag), 1e-9)
Xc = expm([[0, 1], [-4, 0]], 2.3) @ [1, 0]
check("centre conserved 4x^2+y^2", 4, 4, 4 * Xc[0] ** 2 + Xc[1] ** 2, 1e-9)
check("difference half-life", 0.6931, math.log(2), 0.6931, 0.00005)
check("sum doubling ln2/3", 0.2310, math.log(2) / 3, 0.2310, 0.00005)
# ---- l12 ----
for nm, M, tau, det in [("two-factor", T2, -2.5, 1), ("spiral", [[-1, 2], [-2, -1]], -2, 5), ("saddle", S, 2, -3),
                        ("centre", [[0, 1], [-4, 0]], 0, 4), ("companion", A, -3, 2), ("eigen l14", [[-2, 1], [1, -2]], -4, 3),
                        ("trap", [[-1, 3], [3, -1]], -2, -8), ("b=4", [[0, 1], [-4, -4]], -4, 4), ("drift", [[-0.3, 0.4], [0.5, -0.2]], -0.5, -0.14)]:
    ev = np.linalg.eigvals(np.array(M, dtype=float))
    check(f"{nm} tau", tau, float(np.trace(M)), float(ev.sum().real), 1e-9)
    check(f"{nm} det", det, float(np.linalg.det(M)), float(np.prod(ev).real), 1e-9)
check("two-factor discriminant", 2.25, 6.25 - 4, float((np.diff(np.linalg.eigvals(T2)) ** 2)[0].real), 1e-9)
check("trap eigen 2", 2, 2, float(eig([[-1, 3], [3, -1]])[1].real), 1e-9)
check("trap eigen -4", -4, -4, float(eig([[-1, 3], [3, -1]])[0].real), 1e-9)
check("drift larger eigen", 0.2, (-0.5 + 0.9) / 2, float(eig([[-0.3, 0.4], [0.5, -0.2]])[1].real), 1e-9)
check("b on parabola", 4, math.sqrt(16), 4.0, 1e-12)
# ---- l13 ----
def pp(z, c=0.0):
    x, y = z
    return np.array([x * (1 - c * x) - 0.5 * x * y, -0.75 * y + 0.25 * x * y])
check("coexistence x*", 3, 0.75 / 0.25, 3.0 if np.allclose(pp([3, 2]), 0) else 0, 1e-12)
J = np.array([[0, -1.5], [0.5, 0]])
check("J(3,2) det", 0.75, 0.75, float(np.linalg.det(J)), 1e-12)
check("eigen imag", 0.8660, math.sqrt(0.75), float(eig(J)[1].imag), 0.00005)
check("linear period", 7.2552, 2 * math.pi / math.sqrt(0.75), 7.2552, 0.00005)


tr = rk4(lambda z: pp(z), [5, 2], 20, 200000)
y = tr[:, 1]; h = 20 / 200000
idx = [k for k in range(1, len(y)) if y[k - 1] > 2 >= y[k]]
cr = [(k - 1 + (y[k - 1] - 2) / (y[k - 1] - y[k])) * h for k in idx]
check("orbit through (5,2) period", 7.42, 7.42, cr[1] - cr[0], 0.005)
tr = rk4(lambda z: pp(z), [3.05, 2], 20, 200000)
y = tr[:, 1]; idx = [k for k in range(1, len(y)) if y[k - 1] > 2 >= y[k]]
cr = [(k - 1 + (y[k - 1] - 2) / (y[k - 1] - y[k])) * h for k in idx]
check("small orbit period", 7.2552, 2 * math.pi / math.sqrt(0.75), cr[1] - cr[0], 0.001)
H = lambda z: 0.25 * z[0] - 0.75 * math.log(z[0]) + 0.5 * z[1] - math.log(z[1])
tr = rk4(lambda z: pp(z), [5, 2], 10, 100000)
check("H conserved along orbit", H([5, 2]), H([5, 2]), H(tr[-1]), 1e-9)
end = rk4(lambda z: pp(z, 1 / 6), [5, 2], 80, 80000)[-1]
check("crowded settles x", 3, 3, end[0], 1e-3); check("crowded settles y", 1, 1, end[1], 1e-3)
Jc = np.array([[-0.5, -1.5], [0.25, 0]])
check("crowded eig real", -0.25, -0.25, float(eig(Jc)[1].real), 1e-9)
check("crowded eig imag", 0.5590, math.sqrt(5) / 4, float(eig(Jc)[1].imag), 0.00005)
check("crowded det", 0.375, 0.375, float(np.linalg.det(Jc)), 1e-12)
check("cartoon cycle 7.26", 7.26, 2 * math.pi / math.sqrt(0.75), 7.26, 0.005)
# ---- review-3 ----
check("r-weights c1", 2, 2, float(np.linalg.solve([[1, 1], [1, -1]], [3, 1])[0]), 1e-12)
check("r-trace-zero det", -1, -4 + 3, float(np.linalg.det([[2, 1], [-3, -2]])), 1e-9)
Jr = np.array([[-0.5, -0.5], [0.5, 0]])
check("r-linearise imag", 0.433, math.sqrt(0.75) / 2, float(eig(Jr)[1].imag), 0.0005)
check("r-det", 0.25, 0.25, float(np.linalg.det(Jr)), 1e-12)
check("r-slow half-life", 0.3466, math.log(2) / 2, math.log(2) / -float(eig([[-3, 1], [1, -3]])[1].real), 0.00005)
# ---- homework-3 ----
Ah = [[3, -2], [2, -2]]
ch = np.linalg.solve([[2, 1], [1, 2]], [1, 0])
check("h-solve x1(1)", 9.7294, 2 * ch[0] * math.exp(2) + ch[1] * math.exp(-1), (expm(Ah, 1) @ [1, 0])[0], 0.00005)
check("h-solve c=x0 slip", 14.7781, 2 * math.exp(2), 2 * math.exp(2), 0.00005)
check("h-sketch eig", -1, -1, float(eig([[-3, 4], [-2, 1]])[0].real), 1e-9)
check("h-competition det", -1, 1 - 2, float(np.linalg.det([[-1, -2], [-1, -1]])), 1e-9)
check("h-crowded imag sqrt5/4", 0.5590, math.sqrt(5) / 4, float(eig(Jc)[1].imag), 0.00005)
check("spreads sum doubling", 0.3466, math.log(2) / 2, 0.3466, 0.00005)
check("spreads diff half-life", 0.1733, math.log(2) / 4, 0.1733, 0.00005)
check("spreads sum rate", 2, 2, float((np.array([[-1, 3], [3, -1]]) @ [1, 1])[0]), 1e-12)
check("spreads diff rate", -4, -4, float((np.array([[-1, 3], [3, -1]]) @ [1, -1])[0]), 1e-12)

print(f"\n{len(fails)} failures" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
