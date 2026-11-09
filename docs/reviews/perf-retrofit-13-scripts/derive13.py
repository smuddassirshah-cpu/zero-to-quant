"""Second read, the five derivations of batch 13: every number in each prompt, model and rubric recomputed by two
routes (exact Fractions or SymPy, and floats or mpmath / brute force), and the model's claims that are checkable by
computation. Run: <venv>/bin/python -I derive13.py (exit 0 when every check holds)."""
import math, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


def r4(x):
    """exact rounding of a Fraction to 4 decimal places (Fraction.__round__ is exact)"""
    return round(Fr(x), 4)


# ------------------------------------------------------------ least-squares L3 h-derive-hedge
print("least-squares L3 h-derive-hedge")
a1, a2, b = [-1, 1, 1, -1], [-4, 4, -3, 3], [-13, 15, -7, 7]
dot = lambda u, v: sum(Fr(x) * Fr(y) for x, y in zip(u, v))
check((dot(a1, a1), dot(a1, a2), dot(a2, a2), dot(a1, b), dot(a2, b)) == (4, 2, 50, 14, 154), "A'A = [[4, 2], [2, 50]], A'b = (14, 154)")
x1, x2 = sp.symbols("x1 x2")
s = sp.solve([4 * x1 + 2 * x2 - 14, 2 * x1 + 50 * x2 - 154], [x1, x2])
xl = np.linalg.lstsq(np.array([a1, a2], float).T, np.array(b, float), rcond=None)[0]
check(s == {x1: 2, x2: 3} and np.allclose(xl, [2, 3]), "hedge x = (2, 3) by SymPy solve and by NumPy lstsq")
p = [2 * u + 3 * v for u, v in zip(a1, a2)]
e = [x - y for x, y in zip(b, p)]
check(p == [-14, 14, -7, 7] and e == [1, 1, 0, 0], "p = (-14, 14, -7, 7), e = (1, 1, 0, 0)")
check(dot(a1, e) == 0 and dot(a2, e) == 0, "e perpendicular to both columns")
check(dot(b, b) == 492 and dot(e, e) == 2, "|b|^2 = 492, |e|^2 = 2")
grid = min(sum((bb - u * c1 - v * c2) ** 2 for bb, c1, c2 in zip(b, a1, a2)) for u in np.linspace(0, 4, 401) for v in np.linspace(1, 5, 401))
check(abs(grid - 2) < 1e-9, f"grid search of the squared hedged P&L: minimum {grid:.6f} at the hedge")
check(a1[0] == -a1[1] and a2[0] == -a2[1], "each future makes opposite amounts in the two parallel moves, so (1, 1, 0, 0) is out of reach")
a3 = [u + v for u, v in zip(a1, a2)]
A3 = sp.Matrix([a1, a2, a3]).T
check(a3 == [-5, 5, -2, 2] and (A3.T * A3) * sp.Matrix([1, 1, -1]) == sp.zeros(3, 1) and (A3.T * A3).det() == 0, "bundle a3 = (-5, 5, -2, 2), A'A z = 0 for z = (1, 1, -1)")
t = sp.symbols("t")
xt = sp.Matrix([2 - t, 3 - t, t])
check(sp.simplify(A3.T * A3 * xt - A3.T * sp.Matrix(b)) == sp.zeros(3, 1) and sp.simplify(sp.Matrix(b) - A3 * xt) == sp.Matrix(e), "every (2 - t, 3 - t, t) solves the normal equations and leaves e = (1, 1, 0, 0)")
# (a) the expansion |b - q|^2 = |e|^2 - 2tc + t^2|a_j|^2 used in 'only if'
E = sp.Matrix(sp.symbols("e1:5")); Aj = sp.Matrix(sp.symbols("c1:5"))
lhs = ((E - t * Aj).T * (E - t * Aj))[0]
rhs = (E.T * E)[0] - 2 * t * (Aj.T * E)[0] + t ** 2 * (Aj.T * Aj)[0]
check(sp.expand(lhs - rhs) == 0, "(a) only if: |e - t a_j|^2 = |e|^2 - 2tc + t^2|a_j|^2, and t = c/|a_j|^2 lowers it by c^2/|a_j|^2")

# ------------------------------------------------------------ taylor L1 h-prove-newton-error
print("\ntaylor L1 h-prove-newton-error")
r = mp.log(3)
K = mp.e ** mp.mpf("1.2") / (2 * mp.e)
check(abs(K - mp.e ** mp.mpf("0.2") / 2) < 1e-30 and abs(float(K) - 0.611) < 5e-4, f"K = e^1.2/(2e) = e^0.2/2 = {mp.nstr(K, 6)}")
step = lambda x: x - 1 + 3 * mp.e ** (-x)
x0 = mp.mpf(1); x1 = step(x0); x2 = step(x1)
check(abs(x1 - 3 / mp.e) < 1e-35 and abs(float(x1) - 1.103638) < 5e-7, f"x1 = 3/e = {mp.nstr(x1, 8)}")
e0, e1, e2 = x0 - r, x1 - r, x2 - r
check(abs(float(e0) + 0.098612) < 5e-7 and abs(float(e0 ** 2) - 0.009724) < 5e-7 and abs(float(e1) - 0.005026) < 5e-7, f"e0 = {mp.nstr(e0, 6)}, e0^2 = {mp.nstr(e0 ** 2, 5)}, e1 = {mp.nstr(e1, 5)}")
check(abs(float(0.611 * e0 ** 2) - 0.00594) < 5e-6 and 0 < e1 < K * e0 ** 2, f"bound 0.611 e0^2 = {float(0.611 * e0 ** 2):.6f}; 0 < e1 < K e0^2 = {mp.nstr(K * e0 ** 2, 5)}")
check(abs(float(x2) - 1.0986249) < 5e-8 and abs(float(e2) - 1.26e-5) < 5e-8 and abs(float(0.611 * e1 ** 2) - 1.54e-5) < 5e-8 and 0 < e2 < K * e1 ** 2, f"x2 = {mp.nstr(x2, 9)}, e2 = {mp.nstr(e2, 4)}, bound {mp.nstr(K * e1 ** 2, 4)}")
check(abs(float(x2) - 1.09862) < 5e-6 and abs(float(e2) - 1.3e-5) < 5e-7 and abs(float(K * e1 ** 2) - 1.5e-5) < 5e-7, "rubric (d) roundings 1.09862, 1.3e-5, 1.5e-5")
# c exists between x_n and r: solve e_{n+1} = e^c e_n^2 / (2 e^{x_n}) for c
for xn in (x0, x1, mp.mpf("1.2"), mp.mpf("1.05")):
    en, en1 = xn - r, step(xn) - r
    c = mp.log(2 * mp.e ** xn * en1 / en ** 2)
    check(min(xn, r) < c < max(xn, r), f"(b) c from the exact recurrence at x_n = {mp.nstr(xn, 6)}: c = {mp.nstr(c, 8)} lies between x_n and ln 3")
xs = [mp.mpf(1) + mp.mpf(i) / 1000 for i in range(201)]
check(all(step(x) - r >= 0 and step(x) - r <= K * (x - r) ** 2 + mp.mpf(10) ** -35 for x in xs), "(c) on a grid of 201 starts in [1, 1.2]: 0 <= e_{n+1} <= K e_n^2")
check(all(r <= step(x) <= x for x in xs if x >= r), "optional: from [ln 3, 1.2] the next guess stays in [ln 3, x_n]")
check(abs(float(K * (mp.mpf("1.2") - r)) - 0.062) < 5e-4 and abs(float(mp.mpf("1.2") - r) - 0.101) < 5e-4, "optional: 1.2 - ln 3 = 0.101, 0.611 x 0.101 = 0.062")
ratio = [float((step(x) - r) / (x - r) ** 2) for x in (r + mp.mpf("1e-6"), r - mp.mpf("1e-6"))]
check(all(abs(q - 0.5) < 1e-5 for q in ratio), f"e_(n+1)/e_n^2 -> f''(r)/(2f'(r)) = 1/2 (near the root: {ratio})")
X = sp.symbols("x")
check(sp.simplify(X - (sp.exp(X) - 3) / sp.exp(X) - (X - 1 + 3 * sp.exp(-X))) == 0, "update for e^x - 3 is x - 1 + 3e^{-x} (SymPy)")
# the 'tangent sign rule' needs f' > 0 as well as f'' > 0: f(x) = e^{-x} - 1/3 has f'' > 0, f' < 0, and Newton lands at or left of the root
f2 = lambda x: x + (mp.e ** (-x) - mp.mpf(1) / 3) / mp.e ** (-x)
rr = mp.log(3)
check(all(f2(x) <= rr + mp.mpf(10) ** -30 for x in (mp.mpf("0.9"), mp.mpf("1.3"))), "finding TY1-2: with f'' > 0 but f' < 0 (e^{-x} - 1/3) the next guess falls at or LEFT of the root, so the rule needs f' > 0")

# ------------------------------------------------------------ taylor L2 h2-prove-perpetuity-series
print("\ntaylor L2 h2-prove-perpetuity-series")
y, h = sp.symbols("y h", positive=True)
Pfun = 5 / y
check(all(sp.simplify(sp.diff(Pfun, y, k) - (-1) ** k * sp.factorial(k) * 5 * y ** (-(k + 1))) == 0 for k in range(13)), "P^(k)(y) = (-1)^k k! 5 y^-(k+1) for k = 0..12 (SymPy diff)")
hs = sp.symbols("hs")
ser = sp.series(5 / (sp.Rational(1, 20) + hs), hs, 0, 8).removeO()
check(all(ser.coeff(hs, k) == 100 * (-20) ** k for k in range(8)), "Maclaurin coefficients c_k = 100(-20)^k, k = 0..7")
c0, c1, c2 = 100, -2000, 40000
D, C = Fr(-c1, c0), Fr(2 * c2, c0)
check(D == 20 and C == 800 and D == 1 / Fr(1, 20) and C == 2 / Fr(1, 20) ** 2, "D = 20 = 1/y0, C = 800 = 2/y0^2")
y0 = Fr(1, 20)
Pp = lambda yy: 5 / Fr(yy)
check(abs(float((Pp(y0 - Fr(1, 10 ** 6)) - Pp(y0 + Fr(1, 10 ** 6))) / (2 * Fr(1, 10 ** 6))) / 100 - 20) < 1e-6, "D = 20 by a central difference of the price")
check(abs(float((Pp(y0 + Fr(1, 10 ** 5)) - 2 * Pp(y0) + Pp(y0 - Fr(1, 10 ** 5))) / Fr(1, 10 ** 10)) / 100 - 800) < 1e-3, "C = 800 by a second difference")
u = sp.symbols("u")
check(sp.expand((1 - u + u ** 2) * (1 + u)) == 1 + u ** 3, "(1 - u + u^2)(1 + u) = 1 + u^3")
err = sp.simplify(5 / (sp.Rational(1, 20) + hs) - (100 - 2000 * hs + 40000 * hs ** 2))
check(sp.simplify(err - (-800000 * hs ** 3 / (1 + 20 * hs))) == 0 and sp.limit(err / hs ** 3, hs, 0) == -800000, "error = -800,000 h^3/(1 + 20h); error/h^3 -> -800,000")
for hh, rule, true, er in ((Fr(1, 100), 84, Fr(250, 3), Fr(-2, 3)), (Fr(-1, 100), 124, 125, 1)):
    q = 100 - 2000 * hh + 40000 * hh ** 2
    tp = 5 / (y0 + hh)
    check(q == rule and tp == true and tp - q == er and -800000 * hh ** 3 / (1 + 20 * hh) == er, f"h = {hh}: rule {q}, true {float(tp):.4f}, error {float(tp - q):+.4f} by Fractions and the closed form")
check(round(float(Fr(250, 3)), 2) == 83.33 and round(abs(float(Fr(-2, 3))) * 100) == 67, "£83.33 and 67p")
check(Fr(800000) * Fr(1, 100) ** 3 == Fr(4, 5), "dropped cubic term 80p in size at |h| = 1%")
part = float(sum(100 * (-20 * 0.049) ** k for k in range(3000)))
check(abs(part - 5 / 0.099) < 1e-6 and abs(sum(100 * (-20 * 0.051) ** k for k in range(400))) > 1e3, "series converges at h = 0.049 to 5/0.099, diverges at h = 0.051")
check(abs(5 / 0.11 - 45.45) < 5e-3, "5/0.11 = 45.45")

# ------------------------------------------------------------ limits L2 h-prove-negative-powers
print("\nlimits L2 h-prove-negative-powers")
xx, hh = sp.symbols("x h")
check(all(sp.limit(((xx + hh) ** -n - xx ** -n) / hh, hh, 0) == -n * xx ** (-n - 1) for n in range(1, 9)), "limit of the quotient of x^-n is -n x^-(n+1), n = 1..8 (SymPy)")
check(all(sp.expand((xx + hh) ** n - xx ** n - n * xx ** (n - 1) * hh).subs(hh, 0) == 0 and sp.rem(sp.expand((xx + hh) ** n - xx ** n - n * xx ** (n - 1) * hh), hh ** 2, hh) == 0 for n in range(1, 9)), "(x+h)^n - x^n - n x^(n-1) h is divisible by h^2, n = 1..8")
g = lambda z: Fr(1) / Fr(z) ** 4
gq = lambda hv: (g(2 + Fr(hv)) - g(2)) / Fr(hv)
qp, qm = gq(Fr(1, 100)), gq(Fr(-1, 100))
check(r4(qp) == Fr("-0.1235") and r4(qm) == Fr("-0.1266"), f"quotients {float(qp):.7f} -> -0.1235 and {float(qm):.7f} -> -0.1266 (exact Fractions, rounded to 4 dp)")
check(abs((2.01 ** -4 - 0.0625) / 0.01 - float(qp)) < 1e-12 and abs((1.99 ** -4 - 0.0625) / -0.01 - float(qm)) < 1e-12, "same quotients by floats")
check(abs(2.01 ** -4 - 0.061265) < 5e-7 and abs(1.99 ** -4 - 0.063766) < 5e-7, "2.01^-4 = 0.061265, 1.99^-4 = 0.063766")
check(qp > Fr(-1, 8) > qm and abs(qp + Fr(1, 8)) < Fr(2, 1000) and abs(qm + Fr(1, 8)) < Fr(2, 1000), "-0.125 lies between them, each within 0.002")
check(r4(gq(Fr(1, 1000))) == Fr("-0.1248") and r4(gq(Fr(-1, 1000))) == Fr("-0.1252"), "h = +-0.001 give -0.1248 and -0.1252")
check(Fr(-4) / Fr(-2) ** 5 == Fr(1, 8) and Fr(-4) / Fr(2) ** 5 == Fr(-1, 8), "g'(-2) = 0.125, g'(2) = -0.125")

# ------------------------------------------------------------ limits L4 h-build-cable-route
print("\nlimits L4 h-build-cable-route")
X = sp.symbols("x", real=True)
Cx = 500 * sp.sqrt(9 + X ** 2) + 300 * (8 - X)
dC = sp.diff(Cx, X)
check(sp.simplify(dC - (500 * X / sp.sqrt(9 + X ** 2) - 300)) == 0, "C'(x) = 500x/sqrt(9 + x^2) - 300")
check(sp.solve(sp.Eq(dC, 0), X) == [sp.Rational(9, 4)], "only stationary point x = 9/4")
check(sp.diff(Cx, X, 2).subs(X, sp.Rational(9, 4)) > 0, "C''(2.25) > 0")
check(Cx.subs(X, sp.Rational(9, 4)) == 3600 and sp.sqrt(sp.Rational(225, 16)) == sp.Rational(15, 4), "C(2.25) = 1,875 + 1,725 = 3,600, water run 3.75 km")
check(Cx.subs(X, 0) == 3900 and abs(float(Cx.subs(X, 8)) - 4272) < 0.5, f"ends C(0) = 3,900, C(8) = {float(Cx.subs(X, 8)):.2f}")
xs = np.linspace(-5, 13, 180001)
costs = 500 * np.sqrt(9 + xs ** 2) + 300 * np.abs(8 - xs)
check(abs(xs[np.argmin(costs)] - 2.25) < 1e-3 and abs(costs.min() - 3600) < 1e-3, "brute force over landings -5 to 13 km (bank run |8 - x|): best x = 2.25, cost 3,600")
check(all(np.sign(500 * x / np.sqrt(9 + x * x) - 300) == np.sign(16 * x * x - 81) for x in np.linspace(0, 8, 8001) if abs(16 * x * x - 81) > 1e-9), "sign of C' equals the sign of 16x^2 - 81 on [0, 8]")
C2 = 500 * sp.sqrt(9 + X ** 2) + 300 * (2 - X)
check(abs(float(C2.subs(X, 2)) - 1802.776) < 1e-3 and round(float(C2.subs(X, 2))) == 1803 and C2.subs(X, 0) == 2100, f"(c) C(2) = 500 sqrt 13 = {float(C2.subs(X, 2)):.3f} -> £1,803,000; C(0) = 2,100")
xs2 = np.linspace(-3, 5, 80001)
c2 = 500 * np.sqrt(9 + xs2 ** 2) + 300 * np.abs(2 - xs2)
check(abs(xs2[np.argmin(c2)] - 2) < 1e-3, "(c) brute force: best landing is B' itself")
ok = True
for d in np.linspace(0.25, 10, 40):
    xg = np.linspace(0, d, 20001)
    best = xg[np.argmin(500 * np.sqrt(9 + xg ** 2) + 300 * (d - xg))]
    ok &= (abs(best - 2.25) < 1e-3) if d > 2.25 else (abs(best - d) < 1e-3)
check(ok, "optional: for 40 values of d, the cable reaches the bank first exactly when d > 2.25")

print("\nfailures:", len(BAD))
sys.exit(1 if BAD else 0)
