"""Reader recomputation for the eight derivation items of review-perf-retrofit-10 (integrals L1 to L3, linear-maps
L1 to L3, options L3, trees L1). Every number in each model and rubric by two routes: exact (Fractions or sympy)
and a second, independent route (direct sums, quadrature, matrices as vectors, brute force). Also the claims the
findings rest on (integrals L3's other split, trees L1's lend reason). Run from this folder with the venv Python, -I.
Exits 1 on any mismatch."""
import sys, math, random
from fractions import Fraction as F
import sympy as sp
from scipy import integrate, optimize, stats
import numpy as np

bad = 0


def check(name, ok, info=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    bad += 0 if ok else 1


# ===================== integrals L1 =====================
print("integrals L1 h-derive-falling-area")
f = lambda x: 9 - x * x
R = lambda n: sum(f(1 + F(2 * k, n)) * F(2, n) for k in range(1, n + 1))
L = lambda n: sum(f(1 + F(2 * k, n)) * F(2, n) for k in range(0, n))
check("R_n = 28/3 - 8/n - 4/(3n^2) for n < 150", all(R(n) == F(28, 3) - F(8, n) - F(4, 3 * n * n) for n in range(1, 150)))
check("L_n = 28/3 + 8/n - 4/(3n^2) for n < 150", all(L(n) == F(28, 3) + F(8, n) - F(4, 3 * n * n) for n in range(1, 150)))
check("gap L_n - R_n = 16/n = |f(3) - f(1)| 2/n", all(L(n) - R(n) == F(16, n) == abs(f(3) - f(1)) * F(2, n) for n in range(1, 60)))
x = sp.symbols("x")
check("area 28/3 by antiderivative", sp.integrate(9 - x ** 2, (x, 1, 3)) == sp.Rational(28, 3))
check("area by quad", abs(integrate.quad(lambda t: 9 - t * t, 1, 3)[0] - 28 / 3) < 1e-12)
check("R_4 = 7.25, L_4 = 11.25 from heights", R(4) == F(29, 4) and L(4) == F(45, 4) and [f(F(k, 2)) for k in (3, 4, 5, 6)] == [F(27, 4), 5, F(11, 4), 0])
check("formula at n = 4: 28/3 - 2 - 1/12 = 7.25", F(28, 3) - 2 - F(1, 12) == F(29, 4) and F(28, 3) + 2 - F(1, 12) == F(45, 4))
# the split route: right sums of x^2 on [0, 3] and [0, 1], n strips each; it never gives R_n of 9 - x^2 on [1, 3]
Rx2 = lambda a, b, n: sum((a + F((b - a) * k, n)) ** 2 * F(b - a, n) for k in range(1, n + 1))
split4 = 18 - (Rx2(0, 3, 4) - Rx2(0, 1, 4))
check("split route: 18 - (R_4[x^2, 0..3] - R_4[x^2, 0..1]) = 5.8125, not R_4 = 7.25 (finding IN1-2)", split4 == F(93, 16) and split4 != R(4), str(float(split4)))
k, n = sp.symbols("k n", positive=True, integer=True)
Sx2 = sp.summation((3 * k / n) ** 2 * 3 / n, (k, 1, n))
check("split route uses only sum k^2 on [0, 3] (no sum k term)", sp.simplify(Sx2 - 9 * (n + 1) * (2 * n + 1) / (2 * n ** 2)) == 0)

# ===================== integrals L2 =====================
print("integrals L2 h-derive-window")
phi = lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi)
G = lambda x: stats.norm.cdf(2 * x) - stats.norm.cdf(x)
xs = math.sqrt(2 * math.log(2) / 3)
check("x* = sqrt(2 ln 2 / 3) = 0.680 (3 dp); 0.4621 and 0.6798", round(xs, 3) == 0.680 and round(2 * 0.6931 / 3, 4) == 0.4621 and round(xs, 4) == 0.6798, f"{xs:.6f}")
opt = optimize.minimize_scalar(lambda x: -G(x), bounds=(0.01, 3), method="bounded", options={"xatol": 1e-10})
check("maximiser of Phi(2x) - Phi(x) by numerical search", abs(opt.x - xs) < 1e-6, f"{opt.x:.8f}")
check("G'(x*) = 2 phi(2x*) - phi(x*) = 0", abs(2 * phi(2 * xs) - phi(xs)) < 1e-15)
grid = np.linspace(0.01, 3, 3000)
gp = 2 * np.exp(-2 * grid ** 2) - np.exp(-grid ** 2 / 2)
check("G' > 0 below x*, < 0 above, on a grid", all(gp[grid < xs - 1e-9] > 0) and all(gp[grid > xs + 1e-9] < 0))
Gpp = -8 * xs * phi(2 * xs) + xs * phi(xs)
check("G''(x*) = -6 x* phi(2x*) < 0", abs(Gpp - (-6 * xs * phi(2 * xs))) < 1e-15 and Gpp < 0)
fs = sp.Function("f")
t = sp.symbols("t")
check("Leibniz: d/dx int_x^2x f = 2 f(2x) - f(x) (sympy)", sp.simplify(sp.diff(sp.Integral(fs(t), (t, x, 2 * x)), x).doit() - (2 * fs(2 * x) - fs(x))) == 0)
# (a) bounds for h < 0 on a test function
for fn in (math.cos, lambda s: s ** 3 - s, math.exp):
    for x0 in (0.3, -1.2):
        for h in (-0.1, -0.01, 0.05):
            a, b = sorted((x0, x0 + h))
            vals = [fn(a + (b - a) * i / 2000) for i in range(2001)]
            ratio = integrate.quad(fn, x0, x0 + h)[0] / h
            if not (min(vals) - 1e-9 <= ratio <= max(vals) + 1e-9):
                check("rectangle bounds for both signs of h", False, f"{x0} {h}")
check("rectangle bounds m_h <= ratio <= M_h hold for both signs of h (3 functions, 2 points, 3 h)", True)

# ===================== integrals L3 =====================
print("integrals L3 h-derive-parts-tail")
b = sp.symbols("b", positive=True)
I_b = sp.integrate(sp.log(x) / x ** 3, (x, 1, b))
closed = sp.Rational(1, 4) - 1 / (4 * b ** 2) - sp.log(b) / (2 * b ** 2)
check("int_1^b ln x / x^3 = 1/4 - 1/(4b^2) - ln b/(2b^2)", sp.simplify(I_b - closed) == 0)
check("limit 1/4 (sympy) and quad on [1, inf)", sp.limit(closed, b, sp.oo) == sp.Rational(1, 4) and abs(integrate.quad(lambda s: math.log(s) / s ** 3, 1, np.inf)[0] - 0.25) < 1e-10)
check("ln b <= b - 1 and ln b/(2b^2) < 1/(2b) on a grid", all(math.log(v) <= v - 1 and math.log(v) / (2 * v * v) < 1 / (2 * v) for v in np.linspace(1.0001, 1e4, 20000)))
B = sp.symbols("B", positive=True)
sub = sp.integrate(sp.Symbol("s") * sp.exp(-2 * sp.Symbol("s")), (sp.Symbol("s"), 0, B))
check("substitution: int_0^B s e^{-2s} = 1/4 - e^{-2B}/4 - B e^{-2B}/2, equal at B = ln b", sp.simplify(sub - (sp.Rational(1, 4) - sp.exp(-2 * B) / 4 - B * sp.exp(-2 * B) / 2)) == 0 and sp.simplify(closed.subs(b, sp.exp(B)) - sub) == 0)
check("e^{2B} > 2B^2 for B > 0 on a grid", all(math.exp(2 * v) > 2 * v * v for v in np.linspace(1e-4, 40, 4000)))
# the other split: u = x^-3, v' = ln x, v = x ln x - x; I appears again with factor 3 and can be solved (finding IN3-2)
I = sp.symbols("I")
v = x * sp.log(x) - x
boundary = (v / x ** 3).subs(x, b) - (v / x ** 3).subs(x, 1)
rest = sp.integrate(3 * x ** -3, (x, 1, b))
# I = boundary - int(-3x^-4 v) = boundary + 3 int (ln x / x^3) - 3 int x^-3 = boundary + 3 I - rest
solved = sp.solve(sp.Eq(I, boundary + 3 * I - rest), I)[0]
check("the other split gives I = [v/x^3] + 3I - 3 int x^-3, which solves to the same closed form", sp.simplify(solved - closed) == 0)

# ===================== linear-maps L1 =====================
print("linear-maps L1 h-prove-extend-basis")
P = sp.Poly
q1, q2 = x ** 2 - 2 * x, x ** 3 - 3 * x ** 2 + 2 * x
inU = lambda p: sp.simplify(p.subs(x, 0) - p.subs(x, 2)) == 0
check("q1, q2, 1, x^3 - 4x in U; x not in U", inU(q1) and inU(q2) and inU(sp.Integer(1)) and inU(x ** 3 - 4 * x) and not inU(x))
check("x^3 - 4x = q2 + 3 q1", sp.expand(q2 + 3 * q1 - (x ** 3 - 4 * x)) == 0)
coef = lambda p: [sp.Poly(p, x).coeff_monomial(x ** i) for i in range(4)]
M = sp.Matrix([coef(q1), coef(q2), coef(sp.Integer(1))])
check("(q1, q2, 1) has rank 3", M.rank() == 3)
row = sp.Matrix([[0, 2, 4, 8]])  # p(2) - p(0) in coefficients
check("U = null space of (0, 2, 4, 8), dimension 3, and M's rows lie in it", len(row.nullspace()) == 3 and all((row * M.row(i).T)[0] == 0 for i in range(3)))
check("(q1, q2, 1, x) has rank 4: P3 = U + span(x), direct", sp.Matrix([coef(q1), coef(q2), coef(sp.Integer(1)), coef(x)]).rank() == 4)
check("p(2) - p(0) = 2a1 + 4a2 + 8a3", sp.expand(sum(sp.Symbol(f"a{i}") * (2 ** i - 0 ** i if i else 0) for i in range(4)) - (2 * sp.Symbol("a1") + 4 * sp.Symbol("a2") + 8 * sp.Symbol("a3"))) == 0)

# ===================== linear-maps L2 =====================
print("linear-maps L2 h-prove-commutator-rank")
A = sp.Matrix([[1, 1], [0, 2]])
a_, b_, c_, d_ = sp.symbols("a b c d")
X = sp.Matrix([[a_, b_], [c_, d_]])
TX = A * X - X * A
check("T(X) = [[c, d - a - b], [c, -c]]", sp.simplify(TX - sp.Matrix([[c_, d_ - a_ - b_], [c_, -c_]])) == sp.zeros(2))
Tmat = sp.Matrix([[sp.diff(TX[i, j], s) for s in (a_, b_, c_, d_)] for i in range(2) for j in range(2)])
check("rank 2, nullity 2 (4 x 4 matrix of T)", Tmat.rank() == 2 and len(Tmat.nullspace()) == 2)
I2 = sp.eye(2)
T = lambda Y: A * Y - Y * A
check("T(I) = T(A) = 0; (a - b) I + b A = [[a, b], [0, a + b]]", T(I2) == sp.zeros(2) and T(A) == sp.zeros(2) and sp.expand((a_ - b_) * I2 + b_ * A) == sp.Matrix([[a_, b_], [0, a_ + b_]]))
E12, E21 = sp.Matrix([[0, 1], [0, 0]]), sp.Matrix([[0, 0], [1, 0]])
check("T(E12) = [[0, -1], [0, 0]], T(E21) = [[1, 0], [1, -1]]", T(E12) == sp.Matrix([[0, -1], [0, 0]]) and T(E21) == sp.Matrix([[1, 0], [1, -1]]))
vec = lambda Y: list(Y)
check("(I, A, E12, E21) is a basis of R^{2x2}", sp.Matrix([vec(I2), vec(A), vec(E12), vec(E21)]).det() != 0)
B1, B2 = sp.Matrix([[2, 3], [2, -2]]), sp.Matrix([[1, 0], [0, -1]])
s_, t_ = sp.symbols("s t")
Xs = sp.Matrix([[s_ + t_, t_], [2, 3 + s_ + 2 * t_]])
check("T(X_p) = B1 and the family X_p + sI + tA solves T(X) = B1 for all s, t", T(sp.Matrix([[0, 0], [2, 3]])) == B1 and sp.simplify(T(Xs) - B1) == sp.zeros(2))
sol = sp.solve(list(TX - B1), [a_, b_, c_, d_], dict=True)
check("every solution of T(X) = B1 has two free parameters", len(sol) == 1 and len(set(sol[0].keys())) == 2)
check("T(X) = B2 has no solution", sp.solve(list(TX - B2), [a_, b_, c_, d_], dict=True) == [])
check("trace of T(X) is 0; trace-0 space has dimension 3", sp.simplify(TX.trace()) == 0 and len(sp.Matrix([[1, 0, 0, 1]]).nullspace()) == 3)

# ===================== linear-maps L3 =====================
print("linear-maps L3 h-prove-nearest-symmetric")
C = sp.Matrix([[4, 3, 0], [1, 9, 1], [2, -3, 1]])
S0 = (C + C.T) / 2
check("S0 = [[4, 2, 1], [2, 9, -1], [1, -1, 1]]", S0 == sp.Matrix([[4, 2, 1], [2, 9, -1], [1, -1, 1]]))
nrm2 = lambda Y: sum(v ** 2 for v in Y)
S1 = sp.Matrix([[4, 3, 0], [3, 9, 1], [0, 1, 1]])
check("|C - S0|^2 = 12, |C - S1|^2 = 24, |S0 - S1|^2 = 12", nrm2(C - S0) == 12 and nrm2(C - S1) == 24 and nrm2(S0 - S1) == 12)
check("sqrt 12 = 3.464, sqrt 24 = 4.899", round(math.sqrt(12), 3) == 3.464 and round(math.sqrt(24), 3) == 4.899)
Cn = np.array(C.tolist(), dtype=float)
# second route: least squares over the 6 free entries of a symmetric matrix
basis = []
for i in range(3):
    for j in range(i, 3):
        Eij = np.zeros((3, 3)); Eij[i, j] = 1; Eij[j, i] = 1
        basis.append(Eij.ravel())
Bm = np.array(basis).T
coef_ls = np.linalg.lstsq(Bm, Cn.ravel(), rcond=None)[0]
check("least squares over symmetric matrices gives S0", np.allclose((Bm @ coef_ls).reshape(3, 3), np.array(S0.tolist(), dtype=float)))
check("S0 is positive definite (minors 4, 32, 15)", [S0[:k, :k].det() for k in (1, 2, 3)] == [4, 32, 15])
check("dim U = n(n+1)/2, dim U-perp = n(n-1)/2, sum n^2 (n = 1..6; 6 + 3 = 9)", all(n_ * (n_ + 1) // 2 + n_ * (n_ - 1) // 2 == n_ * n_ for n_ in range(1, 7)) and 6 + 3 == 9)

# ===================== options L3 =====================
print("options L3 h-derive-box")
pay = lambda ST, K1=90, K2=110: max(ST - K1, 0) - max(ST - K2, 0) + max(K2 - ST, 0) - max(K1 - ST, 0)
check("box pays K2 - K1 = 20 at every price 0..300 (step 0.5)", all(pay(s / 2) == 20 for s in range(0, 601)))
fair = F(20) / F(104, 100)
cost = F("16.20") - F("5.60") + F("10.90") - F("2.80")
check("fair 20/1.04 = 19.2308, box cost 18.70, cheap by 0.5308", round(float(fair), 4) == 19.2308 and cost == F("18.70") and round(float(fair - cost), 4) == 0.5308)
today = -F("16.20") - F("10.90") + F("5.60") + F("2.80") + fair
check("cash today 0.5308 = £0.53; expiry: box 20 less loan fair x 1.04 = 0", round(float(today), 4) == 0.5308 and pay(100) - fair * F(104, 100) == 0)
g90 = F("16.20") + F(90) / F("1.04") - F("2.80") - 100
g110 = F("5.60") + F(110) / F("1.04") - F("10.90") - 100
check("parity gaps -0.06 at 90 and +0.47 at 110; difference 0.53", round(float(g90), 2) == -0.06 and round(float(g110), 2) == 0.47 and g110 - g90 == fair - cost, f"{float(g90):.4f}, {float(g110):.4f}")
check("the other form of the trade: borrow £18.70, nothing today, 20 - 18.70 x 1.04 = £0.55 at expiry (finding OP3-1)", round(float(20 - cost * F(104, 100)), 2) == 0.55 and 20 - cost * F(104, 100) == (fair - cost) * F(104, 100))
for tt in (F(1, 4), F(1, 2), F(9, 10)):
    owed = fair * F(104, 100) ** 0  # placeholder for type
    owed = float(fair) * 1.04 ** float(tt)
    check(f"early exercise at t = {tt}: loan owes {owed:.4f} = 20/1.04^(1-t) <= 20", abs(owed - 20 / 1.04 ** (1 - float(tt))) < 1e-12 and owed <= 20)

# ===================== trees L1 =====================
print("trees L1 h-derive-one-step")
S, u, d, r, dt = 64, 1.25, 0.8, 0.06, 0.25
fu, fd = abs(u * S - 64), abs(d * S - 64)
g = math.exp(r * dt)
Delta = (fu - fd) / (S * (u - d))
Bg = (u * fd - d * fu) / (u - d)
Bv = Bg / g
V_copy = Delta * S + Bv
q = (g - d) / (u - d)
V_q = (q * fu + (1 - q) * fd) / g
check("f_u = 16, f_d = 12.8, e^0.015 = 1.015113", (fu, round(fd, 10)) == (16, 12.8) and round(g, 6) == 1.015113)
check("Delta = 1/9 (solve 2 x 2 by numpy as well)", abs(Delta - 1 / 9) < 1e-15 and np.allclose(np.linalg.solve([[u * S, g], [d * S, g]], [fu, fd]), [Delta, Bv]))
check("B e^{r dt} = 7.1111, B = 7.0052 (lends £7.01)", round(Bg, 4) == 7.1111 and round(Bv, 4) == 7.0052 and round(Bv, 2) == 7.01)
check("V0 = £14.12 by the copy and by q; q = 0.478029; 14.329693; 0.985112", round(V_copy, 2) == round(V_q, 2) == 14.12 and abs(V_copy - V_q) < 1e-12 and round(q, 6) == 0.478029 and round(q * fu + (1 - q) * fd, 6) == 14.329693 and round(1 / g, 6) == 0.985112)
check("bounds £12.61 <= £14.12 <= £15.76", round(fd / g, 2) == 12.61 and round(fu / g, 2) == 15.76)
check("copy check: 80/9 + 7.1111 = 16 and 51.2/9 + 7.1111 = 12.8", abs(80 / 9 + Bg - 16) < 1e-12 and abs(51.2 / 9 + Bg - 12.8) < 1e-12)
# the lend reason: B > 0 exactly when u f_d > d f_u, not whenever both payoffs are positive (finding TR1-2)
check("lend here because u f_d = 16 > d f_u = 12.8", u * fd > d * fu)
cf = (u * 1 - d * 100) / (u - d)
check("counterexample: f_u = 100, f_d = 1 pays in both states yet the copy borrows (B < 0)", cf < 0, f"B e^(r dt) = {cf:.2f}")
# (c) the failing trades
for gg in (1.25, 1.3):
    check(f"e^(r dt) = {gg} >= u: short and bank nets {S * (gg - u):.2f} up, {S * (gg - d):.2f} down", S * (gg - u) >= 0 and S * (gg - d) > 0)
for gg in (0.8, 0.7):
    check(f"e^(r dt) = {gg} <= d: borrow and buy nets {S * (u - gg):.2f} up, {S * (d - gg):.2f} down", S * (u - gg) > 0 and S * (d - gg) >= 0)

print("failures:", bad)
sys.exit(1 if bad else 0)
