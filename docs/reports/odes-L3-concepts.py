#!/usr/bin/env python3
"""Concept checks for odes level 3 (l10 to l13, review-3, homework-3).

Blind concept audit: docs/reviews/audit-odes-1-3.md. Exits 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, does not change the exit code, and carries the corrected assert in a
comment beside it.
"""
import sys
import warnings
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

warnings.filterwarnings('ignore', category=RuntimeWarning)
FAILS, XFAILS, PASSES = [], [], []


def check(name, ok):
    (PASSES if ok else FAILS).append(name)
    print(("PASS  " if ok else "FAIL  ") + name)


def expected_fail(name, ok, finding):
    if ok:
        FAILS.append(name + " (expected to fail, but passed: recheck finding %s)" % finding)
        print("FAIL  " + name + " now passes; finding %s may be fixed" % finding)
    else:
        XFAILS.append(name)
        print("EXPECTED_FAIL  %s  [finding %s]" % (name, finding))


t = sp.symbols('t', real=True)
rng = np.random.default_rng(13)


def classify(A, tol=1e-9):
    """The content's rule (l12 s8)."""
    A = np.asarray(A, dtype=float)
    tau, det = float(np.trace(A)), float(np.linalg.det(A))
    if abs(det) <= tol:
        return "degenerate"
    if det < 0:
        return "saddle"
    if abs(tau) <= tol:
        return "centre"
    side = "stable" if tau < 0 else "unstable"
    return side + (" node" if tau * tau - 4 * det >= -tol else " spiral")


def by_eigen(A):
    """Independent classification straight from the eigenvalues (Strogatz 5.2)."""
    l1, l2 = np.linalg.eigvals(np.asarray(A, dtype=float))
    if abs(l1.imag) > 1e-9:
        if abs(l1.real) < 1e-9:
            return "centre"
        return ("stable" if l1.real < 0 else "unstable") + " spiral"
    l1, l2 = l1.real, l2.real
    if abs(l1 * l2) < 1e-9:
        return "degenerate"
    if l1 * l2 < 0:
        return "saddle"
    return ("stable" if l1 < 0 else "unstable") + " node"


# ---------------- l10 systems ----------------
A0 = sp.Matrix([[0, 1], [-2, -3]])
check("l10 s0 eigenvectors: A(1,-1)=-(1,-1), A(1,-2)=-2(1,-2); (1,0),(1,1) are not eigenvectors",
      A0 * sp.Matrix([1, -1]) == -sp.Matrix([1, -1]) and A0 * sp.Matrix([1, -2]) == -2 * sp.Matrix([1, -2])
      and A0 * sp.Matrix([1, 0]) == sp.Matrix([0, -2]) and A0 * sp.Matrix([1, 1]) == sp.Matrix([1, -5]))
lam = sp.symbols('lambda')
p, q = sp.symbols('p q')
check("l10 s1/quiz0 companion: char poly of [[0,1],[-q,-p]] is lambda^2+p lambda+q (the equation's own)",
      sp.expand(sp.Matrix([[0, 1], [-q, -p]]).charpoly(lam).as_expr() - (lam ** 2 + p * lam + q)) == 0)
x = sp.exp(A0 * t) * sp.Matrix([1, 0])
check("l10 s2 eigenvector solution: x(0)=(1,0) gives x1 = 2e^{-t}-e^{-2t} (matrix exponential agrees), c=(2,-1)",
      sp.simplify(x[0] - (2 * sp.exp(-t) - sp.exp(-2 * t))) == 0 and sp.simplify(x[1] - (-2 * sp.exp(-t) + 2 * sp.exp(-2 * t))) == 0)
A2 = sp.Matrix([[-2, 2], [0, sp.Rational(-1, 2)]])
check("l10 s3 two-factor: triangular, eigenvalues -2 and -0.5; A(4,3)=-0.5(4,3); A(1,0)=-2(1,0)",
      A2.eigenvals() == {-2: 1, sp.Rational(-1, 2): 1} and A2 * sp.Matrix([4, 3]) == sp.Rational(-1, 2) * sp.Matrix([4, 3]))
xx = sp.exp(A2 * t) * sp.Matrix([sp.Rational(2, 100), sp.Rational(1, 100)])
check("l10 s4-5: x(t) = (1/150)e^{-2t}(1,0) + (1/300)e^{-0.5t}(4,3) (matrix exponential agrees)",
      sp.simplify(xx[0] - (sp.exp(-2 * t) / 150 + 4 * sp.exp(-t / 2) / 300)) == 0 and sp.simplify(xx[1] - 3 * sp.exp(-t / 2) / 300) == 0)
check("l10 s6: c = x(0) is right only when V = I: with V=[[1,4],[0,3]] it gives x(0)=6%", 0.02 + 4 * 0.01 == 0.06)
Ad = sp.Matrix([[-1, 1], [0, -1]])
xd = sp.exp(Ad * t) * sp.Matrix([0, 1])
check("l10 s7 defective: one eigenvector; x1 = t e^{-t}", len(Ad.eigenvects()[0][2]) == 1 and sp.simplify(xd[0] - t * sp.exp(-t)) == 0)
check("l10 quiz3: [[2,1],[0,2]] has one independent eigenvector; every eigenvalue has at least one",
      len(sp.Matrix([[2, 1], [0, 2]]).eigenvects()[0][2]) == 1)
A3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [-5, 1, -2]])
check("l10 s8 third order: char poly of the companion is lambda^3+2lambda^2-lambda+5",
      sp.expand(A3.charpoly(lam).as_expr() - (lam ** 3 + 2 * lam ** 2 - lam + 5)) == 0)
ok = True
for _ in range(200):
    A = rng.normal(size=(2, 2))
    x0 = rng.normal(size=2)
    vals, V = np.linalg.eig(A)
    c = np.linalg.solve(V, x0)
    xt = V @ (c * np.exp(vals * 0.7))
    ok &= np.allclose(xt.imag, 0, atol=1e-10) and np.allclose(xt.real, expm(0.7 * A) @ x0, atol=1e-9)
check("l10 s9 code claim: for real A and x0 the imaginary parts cancel and the eigen-sum equals expm(At)x0 (200 random matrices)", bool(ok))
check("l10 s10 / review-3 i8: the slow eigenvalue sets the long-run half-life ln2/|lambda|",
      abs(np.log(2) / 2 - 0.3466) < 5e-5 and abs(np.log(2) / 0.5 - 1.3863) < 5e-5)

# ---------------- l11 phase plane ----------------
As = sp.Matrix([[1, 2], [2, 1]])
check("l11 s0 saddle: eigenvalue 3 on (1,1), -1 on (1,-1)", As * sp.Matrix([1, 1]) == 3 * sp.Matrix([1, 1]) and As * sp.Matrix([1, -1]) == -sp.Matrix([1, -1]))
xs = sp.exp(As * t) * sp.Matrix([1, 0])
check("l11 s1: from (1,0), x = (e^{3t}+e^{-t})/2, y = (e^{3t}-e^{-t})/2",
      sp.simplify(xs[0] - (sp.exp(3 * t) + sp.exp(-t)) / 2) == 0 and sp.simplify(xs[1] - (sp.exp(3 * t) - sp.exp(-t)) / 2) == 0)
# node: arrival along the slow eigenvector
An = np.array([[-2, 2], [0, -0.5]])
ok = True
for _ in range(100):
    x0 = rng.normal(size=2)
    if abs(x0[1]) < 0.05:
        continue
    xe = expm(12 * An) @ x0
    ok &= abs(abs(xe @ np.array([4, 3]) / 5 / np.linalg.norm(xe)) - 1) < 1e-6
check("l11 s2 stable node: every start off the fast eigenvector arrives tangent to the slow one (4,3)", bool(ok))
xf = expm(12 * An) @ np.array([1.0, 0.0])
check("l11 s2: a start on the fast eigenvector (1,0) stays on it", abs(xf[1]) < 1e-15)
Au = np.array([[2.0, 0.0], [0.0, 5.0]])
xb = expm(-6 * Au) @ np.array([1.0, 1.0])
check("l11 quiz1 unstable node 2, 5: paths leave tangent to the eigenvector of the smaller eigenvalue", abs(xb[1] / xb[0]) < 1e-6)
Asp = np.array([[-1, 2], [-2, -1]])
check("l11 s3 spiral: eigenvalues -1+-2i; distance shrinks by exactly e^{-t} (e^{-pi} per turn of time pi)",
      np.allclose(sorted(np.linalg.eigvals(Asp).imag), [-2, 2]) and abs(np.linalg.norm(expm(np.pi * Asp) @ np.array([1.0, 0.0])) - np.exp(-np.pi)) < 1e-12
      and np.allclose(expm(np.pi * Asp) @ np.array([1.0, 0.0]) / np.exp(-np.pi), [1, 0], atol=1e-9))
# turning direction rule: sign of the bottom-left entry, for every matrix with complex eigenvalues
ok, n = True, 0
while n < 2000:
    A = rng.normal(size=(2, 2))
    if np.trace(A) ** 2 - 4 * np.linalg.det(A) >= 0:
        continue
    n += 1
    ok &= A[1, 0] != 0
    for x0 in rng.normal(size=(3, 2)):
        v = A @ x0
        ang = x0[0] * v[1] - x0[1] * v[0]  # > 0 means anticlockwise
        ok &= (ang > 0) == (A[1, 0] > 0)
check("l11 s4/s9 turning: with complex eigenvalues the bottom-left entry is nonzero and its sign gives the direction at every point (2,000 random matrices)", bool(ok))
check("l11 s6 transpose: same eigenvalues, opposite turning", np.allclose(sorted(np.linalg.eigvals(Asp.T).imag), [-2, 2]) and Asp.T[1, 0] > 0 > Asp[1, 0])
X, Y = sp.symbols('x y', real=True)
H = 4 * X ** 2 + Y ** 2
check("l11 s5 centre: H=4x^2+y^2 is conserved by x'=y, y'=-4x", sp.simplify(sp.diff(H, X) * Y + sp.diff(H, Y) * (-4 * X)) == 0)
check("l11 s7 zero eigenvalue: x'=0, y'=-y has the whole x axis as equilibria", sp.Matrix([[0, 0], [0, -1]]).nullspace()[0] == sp.Matrix([1, 0]))
# the four-picture table against eigenvalue classification, and the l12 trace-determinant rule
ok, kinds = True, set()
for _ in range(20000):
    A = rng.integers(-4, 5, size=(2, 2)).astype(float)
    a, b = classify(A), by_eigen(A)
    kinds.add(a)
    tau, det = np.trace(A), np.linalg.det(A)
    on_parabola = abs(tau * tau - 4 * det) < 1e-9
    ok &= (a == b) or on_parabola  # on the parabola both say node, guarded for rounding
check("l11 s8 / l12 s0-s2-s8 map: trace-determinant rule agrees with the eigenvalues on 20,000 integer matrices; all 7 names occur",
      bool(ok) and kinds == {"saddle", "stable node", "unstable node", "stable spiral", "unstable spiral", "centre", "degenerate"})
check("l11 s10: s=x+y obeys s'=3s, d=x-y obeys d'=-d",
      sp.simplify((X + 2 * Y) + (2 * X + Y) - 3 * (X + Y)) == 0 and sp.simplify((X + 2 * Y) - (2 * X + Y) + (X - Y)) == 0)

# l11 quiz0 feedback: "each point has one velocity, so one path"
# y' = 3|y|^(2/3), t' = 1 has one velocity at every point, yet two paths pass through (0, 0).
tt = np.linspace(-1, 1, 401)
two_paths = np.max(np.abs(3 * tt ** 2 - 3 * np.abs(tt ** 3) ** (2 / 3))) < 1e-12  # y = t^3 solves it; so does y = 0
# (corrected claim, fix pass) quiz0 now keys "A linear system has one path per point" with feedback "a smooth system
# has one path through each point". Fixer's own check: one velocity per point is not enough (3|y|^(2/3) has two
# paths through 0), but for x'=Ax two solutions from one point differ by e^{At}0 = 0 (the difference solves x'=Ax).
_Aq = np.array([[1.0, 2.0], [2.0, 1.0]])
_d = solve_ivp(lambda u, z: _Aq @ z, (0, 2), [0.0, 0.0], rtol=1e-12, atol=1e-14)
check("l11 quiz0 reasoning (corrected claim, fix pass): non-smooth field has two paths through 0; for x'=Ax the difference of two paths from one point stays 0",
      two_paths and np.max(np.abs(_d.y)) == 0.0 and np.allclose(expm(2.0 * _Aq) @ np.zeros(2), 0))
# corrected assert: one path through each point when the velocity field is smooth (Lipschitz); linear fields are
check("l11 quiz0 corrected: x'=Ax is Lipschitz with constant ||A||, so its paths never cross",
      all(np.linalg.norm(As_ @ u - As_ @ v) <= np.linalg.norm(As_, 2) * np.linalg.norm(u - v) + 1e-12
          for As_ in [np.array([[1.0, 2.0], [2.0, 1.0]])] for u, v in rng.normal(size=(200, 2, 2))))

# ---------------- l12 stability ----------------
tau, Dl = sp.symbols('tau Delta', real=True)
a_, b_, c_, d_ = sp.symbols('a b c d', real=True)
Ag = sp.Matrix([[a_, b_], [c_, d_]])
check("l12 s2: char poly is lambda^2 - tau lambda + Delta; product Delta, sum tau",
      sp.expand(Ag.charpoly(lam).as_expr() - (lam ** 2 - (a_ + d_) * lam + (a_ * d_ - b_ * c_))) == 0)
for name, M, kind in [
    ("l12 s1 two-factor", [[-2, 2], [0, -0.5]], "stable node"), ("l12 s1 spiral", [[-1, 2], [-2, -1]], "stable spiral"),
    ("l12 s1 saddle", [[1, 2], [2, 1]], "saddle"), ("l12 s1 centre", [[0, 1], [-4, 0]], "centre"),
    ("l12 s3 eigen l14", [[-2, 1], [1, -2]], "stable node"), ("l12 s6 spreads", [[-1, 3], [3, -1]], "saddle"),
    ("l12 s7 nudged centre", [[0, 1], [-4, -0.01]], "stable spiral"), ("l12 s9 drift", [[-0.3, 0.4], [0.5, -0.2]], "saddle"),
    ("l12 quiz0", [[1, -1], [1, 1]], "unstable spiral"), ("l12 s8 b=4", [[0, 1], [-4, -4]], "stable node"),
    ("review-3 i2", [[0, 3], [-1, 0]], "centre"), ("review-3 i4", [[2, 1], [-3, -2]], "saddle"),
    ("review-3 i5", [[0, 1], [-5, -2]], "stable spiral"), ("review-3 i6", [[-0.5, -0.5], [0.5, 0]], "stable spiral"),
    ("homework-3 i3", [[-3, 4], [-2, 1]], "stable spiral"), ("homework-3 i4", [[-1, -2], [-1, -1]], "saddle"),
    ("l13 s2 J(0,0)", [[1, 0], [0, -0.75]], "saddle"), ("l13 s3 J(3,2)", [[0, -1.5], [0.5, 0]], "centre"),
    ("l13 s6 J(3,1)", [[-0.5, -1.5], [0.25, 0]], "stable spiral"),
]:
    check(name + ": " + kind + " by the map and by the eigenvalues", classify(M, 1e-9) == kind and (by_eigen(M) == kind or kind.endswith("node")))
check("l12 s9 eigenvalues 0.2 and -0.7; l12 s6 eigenvalues 2 on (1,1), -4 on (1,-1)",
      np.allclose(sorted(np.linalg.eigvals(np.array([[-0.3, 0.4], [0.5, -0.2]]))), [-0.7, 0.2])
      and np.allclose(np.array([[-1, 3], [3, -1]]) @ [1, 1], [2, 2]) and np.allclose(np.array([[-1, 3], [3, -1]]) @ [1, -1], [-4, 4]))
bb = sp.symbols('b', positive=True)
check("l12 s4: the oscillator [[0,1],[-4,-b]] has tau=-b, Delta=4; on the parabola at b=4",
      sp.Matrix([[0, 1], [-4, -bb]]).trace() == -bb and sp.Matrix([[0, 1], [-4, -bb]]).det() == 4 and sp.solve(sp.Eq(bb ** 2, 16), bb) == [4])
Ac = np.diag([0.9, -0.5])
check("l12 s5 continuous vs discrete: eigenvalues 0.9, -0.5: A^k -> 0 but e^{At} grows",
      np.linalg.norm(np.linalg.matrix_power(Ac, 400)) < 1e-15 and np.linalg.norm(expm(40 * Ac)) > 1e15)
# l12 s5: "stability needs every eigenvalue in the left half-plane"; l12 s7: "a centre is stable"
Acen = np.array([[0.0, 1.0], [-4.0, 0.0]])
re_max = np.linalg.eigvals(Acen).real.max()
stays_near = max(np.linalg.norm(expm(s_ * Acen) @ np.array([0.01, 0.0])) for s_ in np.linspace(0, 200, 4001)) <= 0.021
centre_is_stable = stays_near           # s7's sense (Lyapunov): starts near, stays near
passes_s5_test = re_max < -1e-12        # s5's test
# (corrected claim, fix pass) s5 now says "every path decays to the origin exactly when every real part is below 0:
# that is asymptotic stability", and s7 says a centre is stable (nearby paths stay near) but not asymptotically
# stable. Fixer's own check: the centre [[0,1],[-4,0]] conserves 4x^2 + y^2 (sympy), so paths stay near and never
# decay, while it fails the real-part test; these are two different properties, as the text now names them.
_xc, _yc = sp.symbols('xc yc')
_Hc = 4 * _xc ** 2 + _yc ** 2
check("l12 s5 vs s7 (corrected claim, fix pass): centre conserves 4x^2+y^2 (stable, not asymptotically stable) and fails the real-part test",
      sp.simplify(sp.diff(_Hc, _xc) * _yc + sp.diff(_Hc, _yc) * (-4 * _xc)) == 0 and centre_is_stable and not passes_s5_test)
# corrected assert: real parts below 0 is the test for ASYMPTOTIC stability; a centre is stable but not asymptotically stable
decays = np.linalg.norm(expm(200 * Acen) @ np.array([0.01, 0.0])) < 1e-6
check("l12 s5 corrected: centre is stable (stays within 2x its start) and not asymptotically stable (does not decay); real parts < 0 is the asymptotic test",
      stays_near and not decays and not passes_s5_test)
ok = True
for _ in range(2000):
    A = rng.normal(size=(2, 2))
    asym = np.linalg.norm(expm(60 * A)) < 1e-6
    blow = np.linalg.norm(expm(60 * A)) > 1e6
    rm = np.linalg.eigvals(A).real.max()
    if abs(rm) < 0.3:
        continue
    ok &= (asym == (rm < 0)) and (blow == (rm > 0))
check("l12 s5: every path decays to the origin exactly when every real part is below 0 (2,000 random matrices)", bool(ok))
ok = True
for _ in range(2000):
    A = rng.normal(size=(2, 2))
    rho = np.abs(np.linalg.eigvals(A)).max()
    if abs(rho - 1) < 0.1:
        continue
    ok &= (np.linalg.norm(np.linalg.matrix_power(A, 400)) < 1e-6) == (rho < 1)
check("l12 s5/quiz3 chain: A^k -> 0 exactly when every |lambda| < 1 (2,000 random matrices)", bool(ok))
# l12 summary: "tau and Delta fix the eigenvalues, so they fix the picture"
cr = lambda u, v: u[0] * v[1] - u[1] * v[0]
star, improper = -np.eye(2), np.array([[-1.0, 1.0], [0.0, -1.0]])
same_td = np.trace(star) == np.trace(improper) and abs(np.linalg.det(star) - np.linalg.det(improper)) < 1e-12
straight_star = all(abs(cr(expm(1.0 * star) @ v, v)) < 1e-12 for v in rng.normal(size=(50, 2)))
straight_improper = all(abs(cr(expm(1.0 * improper) @ v, v)) < 1e-9 for v in rng.normal(size=(50, 2)))
# (corrected claim, fix pass) summary now says tau and Delta fix the picture except on the parabola, where a node may
# have one eigenvector or two. Fixer's own check: both matrices sit on tau^2 = 4 Delta, and their eigenvector counts
# are 2 - rank(A + I) = 2 and 1.
check("l12 summary tau_Delta_fix_picture (corrected claim, fix pass): -I and [[-1,1],[0,-1]] share tau=-2, Delta=1 on the parabola, with 2 and 1 eigenvectors",
      same_td and straight_star and not straight_improper and np.trace(star) ** 2 == 4 * round(np.linalg.det(star))
      and 2 - np.linalg.matrix_rank(star + np.eye(2)) == 2 and 2 - np.linalg.matrix_rank(improper + np.eye(2)) == 1)
# corrected assert: they fix the picture except on the parabola, where a star node and a one-eigenvector node share tau and Delta
check("l12 summary corrected: off the parabola (and off Delta=0) tau and Delta give distinct eigenvalues, hence one picture",
      all(classify(A) == by_eigen(A) for A in rng.integers(-4, 5, size=(3000, 2, 2)).astype(float)
          if abs(np.trace(A) ** 2 - 4 * np.linalg.det(A)) > 1e-9))

# ---------------- l13 linearising ----------------
fx = X - sp.Rational(1, 2) * X * Y
fy = -sp.Rational(3, 4) * Y + sp.Rational(1, 4) * X * Y
eqs = sp.solve([fx, fy], [X, Y], dict=True)
J = sp.Matrix([fx, fy]).jacobian([X, Y])
check("l13 s0-1: equilibria (0,0) and (3,2); Jacobian as stated; J(3,2)=[[0,-1.5],[0.5,0]], J(0,0)=diag(1,-0.75)",
      {(e[X], e[Y]) for e in eqs} == {(0, 0), (3, 2)}
      and J.subs({X: 3, Y: 2}) == sp.Matrix([[0, sp.Rational(-3, 2)], [sp.Rational(1, 2), 0]]) and J.subs({X: 0, Y: 0}) == sp.diag(1, sp.Rational(-3, 4)))
Hh = sp.Rational(1, 4) * X - sp.Rational(3, 4) * sp.log(X) + sp.Rational(1, 2) * Y - sp.log(Y)
check("l13 s5 conserved: H' = 0 along orbits; H has a strict minimum at (3,2)",
      sp.simplify(sp.diff(Hh, X) * fx + sp.diff(Hh, Y) * fy) == 0
      and sp.solve([sp.diff(Hh, X), sp.diff(Hh, Y)], [X, Y]) == {X: 3, Y: 2} and sp.hessian(Hh, [X, Y]).subs({X: 3, Y: 2}).is_positive_definite)


def lv(c):
    return lambda s_, z: [z[0] * (1 - c * z[0]) - 0.5 * z[0] * z[1], -0.75 * z[1] + 0.25 * z[0] * z[1]]


def period(x0):
    ev = lambda s_, z: z[1] - 2.0
    ev.direction = 1
    s = solve_ivp(lv(0), (0, 40), x0, events=ev, rtol=1e-11, atol=1e-13)
    te = s.t_events[0]
    te = te[te > 1e-6]
    return te[0] if abs(x0[1] - 2.0) < 1e-12 else te[1] - te[0]


check("l13 s3-4 small orbits have the linear period 2pi/sqrt(0.75)=7.2552", abs(period([3.01, 2.0]) - 7.2552) < 1e-3)
check("l13 s4 true orbit through (5,2) takes about 7.42 and closes", abs(period([5.0, 2.0]) - 7.42) < 0.01)
s = solve_ivp(lv(0), (0, 200), [5.0, 2.0], rtol=1e-11, atol=1e-13)
Hn = 0.25 * s.y[0] - 0.75 * np.log(s.y[0]) + 0.5 * s.y[1] - np.log(s.y[1])
check("l13 s9: orbits with x,y>0 keep their size (H constant over 27 cycles), and capital stays above zero",
      np.ptp(Hn) < 1e-8 and s.y[1].min() > 0.3)
fxc = X * (1 - X / 6) - sp.Rational(1, 2) * X * Y
Jc = sp.Matrix([fxc, fy]).jacobian([X, Y]).subs({X: 3, Y: 1})
check("l13 s6 crowded: equilibrium (3,1); J=[[-0.5,-1.5],[0.25,0]]; eigenvalues -0.25+-0.5590i",
      fxc.subs({X: 3, Y: 1}) == 0 and fy.subs({X: 3, Y: 1}) == 0 and Jc == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(-3, 2)], [sp.Rational(1, 4), 0]])
      and abs(complex(list(Jc.eigenvals())[0]).imag) - 0.5590 < 5e-5)
s = solve_ivp(lv(1 / 6), (0, 40), [5.0, 2.0], rtol=1e-10, atol=1e-12)
check("l13 s6 simulation: with c=1/6 the path from (5,2) settles at (3,1)", np.hypot(s.y[0, -1] - 3, s.y[1, -1] - 1) < 2e-3)

# Hartman-Grobman: hyperbolic linear pictures are shared by the nonlinear system near the point
# (a) saddle at the origin of predator-prey: starts near it leave unless on the stable manifold (the y axis)
s = solve_ivp(lv(0), (0, 6), [1e-3, 1e-3], rtol=1e-10, atol=1e-14)
check("l13 s2 saddle trusted: from (0.001, 0.001) prey grow away while predators die", s.y[0, -1] > 0.3 and s.y[1, -1] < 1e-3)
# (b) review-3 i6 stable spiral at (0.5, 0.5) and homework-3 i4 saddle at (1,1): simulate the nonlinear systems
s = solve_ivp(lambda u, z: [z[0] * (1 - z[0]) - z[0] * z[1], z[1] * (z[0] - 0.5)], (0, 80), [0.6, 0.4], rtol=1e-10, atol=1e-13)
dx = s.y[0] - 0.5
check("review-3 i6 trusted: nonlinear path spirals into (0.5,0.5) (sign changes of x-0.5, distance to 0)",
      np.hypot(s.y[0, -1] - 0.5, s.y[1, -1] - 0.5) < 1e-6 and np.sum(np.diff(np.sign(dx[np.abs(dx) > 1e-9])) != 0) >= 4)
ends = []
for x0 in rng.uniform(0.9, 1.1, size=(40, 2)):
    s = solve_ivp(lambda u, z: [z[0] * (3 - z[0] - 2 * z[1]), z[1] * (2 - z[0] - z[1])], (0, 400), x0, rtol=1e-9, atol=1e-12)
    ends.append((round(s.y[0, -1], 3), round(s.y[1, -1], 3)))
check("homework-3 i4 saddle trusted: 40 random starts near (1,1) all leave, to (3,0) or (0,2): one strategy wins",
      set(ends) <= {(3.0, 0.0), (0.0, 2.0)} and len(set(ends)) == 2)

# (c) the borderline centre: linearisation is inconclusive
Xs = sp.Matrix([-Y - X ** 3, X - Y ** 3])
J0 = Xs.jacobian([X, Y]).subs({X: 0, Y: 0})
s = solve_ivp(lambda u, z: [-z[1] - z[0] ** 3, z[0] - z[1] ** 3], (0, 400), [0.5, 0.0], rtol=1e-10, atol=1e-13)
check("l13 s6/summary linear centre inconclusive: x'=-y-x^3, y'=x-y^3 has J(0)=[[0,-1],[1,0]] (centre) yet spirals in",
      classify(np.array(J0, dtype=float)) == "centre" and np.hypot(*s.y[:, -1]) < 0.06 and sp.simplify(X * Xs[0] + Y * Xs[1] + X ** 4 + Y ** 4) == 0)
s = solve_ivp(lambda u, z: [-z[1] + z[0] ** 3, z[0] + z[1] ** 3], (0, 3.5), [0.5, 0.0], rtol=1e-10, atol=1e-13)
check("l13 linear centre inconclusive, other way: x'=-y+x^3, y'=x+y^3 spirals out from the same Jacobian", np.hypot(*s.y[:, -1]) > 1.0)
# l13 s6 presents the crowded model as the case of an untrusted linear centre.
tau_c = float(Jc.trace())
# (corrected claim, fix pass) s6 now says crowding moved the trace of J to -0.5, so the linear picture is itself a spiral,
# and uses x'=-y-x^3, y'=x-y^3 for the untrusted linear centre. Fixer's own check: differentiate the crowded field by
# hand in sympy at (3,1), c=1/6, and check the cubic example's d/dt(x^2+y^2) = -2(x^4+y^4) < 0.
_cx = sp.Rational(1, 6)
_Jh = sp.Matrix([[1 - 2 * _cx * 3 - sp.Rational(1, 2) * 1, -sp.Rational(1, 2) * 3], [sp.Rational(1, 4) * 1, -sp.Rational(3, 4) + sp.Rational(1, 4) * 3]])
check("l13 s6 example (corrected claim, fix pass): crowded J at (3,1) has trace -1/2 (a spiral), and the cubic centre example spirals in",
      _Jh == sp.Matrix([[-sp.Rational(1, 2), -sp.Rational(3, 2)], [sp.Rational(1, 4), 0]]) and _Jh.trace() == -sp.Rational(1, 2)
      and _Jh.trace() ** 2 < 4 * _Jh.det() and classify(np.array(Jc, dtype=float)) != "centre"
      and sp.expand(2 * X * (-Y - X ** 3) + 2 * Y * (X - Y ** 3)) == -2 * X ** 4 - 2 * Y ** 4)
# corrected assert: crowding moves the trace of the Jacobian to -0.5, so the linearisation itself is a (trusted) stable spiral
check("l13 s6 corrected: at c=1/6 the linearisation is a stable spiral (tau=-0.5), which Hartman-Grobman trusts", classify(np.array(Jc, dtype=float)) == "stable spiral" and tau_c == -0.5)

# (d) quiz2 / s6: "a node in the linearisation is shared by the nonlinear system"
# star node -I with r' = -r, theta' = 1/ln r: the linear part is still -I but paths wind round the origin without end.
def starspiral(u, z):
    r = np.hypot(z[0], z[1])
    w = 1 / np.log(r)
    return [-z[0] - w * z[1], -z[1] + w * z[0]]


s = solve_ivp(starspiral, (0, 30), [0.5, 0.0], rtol=1e-10, atol=1e-30)
theta = np.unwrap(np.arctan2(s.y[1], s.y[0]))
# exact: r = 0.5 e^{-t}, theta(t) = -ln((t - ln 0.5)/(-ln 0.5)), which is unbounded: the path winds round for ever
theta_exact = lambda u: -np.log((u + np.log(2)) / np.log(2))
sim_ok = abs(theta[-1] - theta_exact(30.0)) < 1e-5 and abs(np.hypot(*s.y[:, -1]) - 0.5 * np.exp(-30)) < 1e-18
fd = lambda f, z, h: np.array([[(f(0, [z[0] + h, z[1]])[i] - f(0, [z[0] - h, z[1]])[i]) / (2 * h) for i in range(2)],
                               [(f(0, [z[0], z[1] + h])[i] - f(0, [z[0], z[1] - h])[i]) / (2 * h) for i in range(2)]]).T
J_near = fd(starspiral, [1e-30, 1e-30], 1e-32)
# (corrected claim, fix pass) quiz2 now keys "a stable node with two distinct eigenvalues" and its explain says a node
# with two equal eigenvalues can turn into a spiral. Fixer's own check: the star -I (equal eigenvalues) gives a
# system whose angle is unbounded; the angle integral of dt/(ln r0 - t) diverges like ln t (sympy).
_T, _r0 = sp.symbols('T r0', positive=True)
_ang = sp.integrate(1 / (sp.log(sp.Rational(1, 2)) - t), (t, 0, _T))
check("l13 quiz2 node (corrected claim, fix pass): equal-eigenvalue node -I becomes a spiral (angle integral unbounded)",
      sp.limit(sp.Abs(_ang), _T, sp.oo) == sp.oo and abs(theta_exact(1e6)) > np.pi
      and len(set(np.round(np.linalg.eigvals(-np.eye(2)), 12))) == 1)
# corrected assert: stability carries over (Hartman-Grobman); a node with two equal eigenvalues may become a spiral (Strogatz 6.3)
check("l13 quiz2 corrected: r'=-r, theta'=1/ln r is asymptotically stable with Jacobian near -I at the origin, yet turns without bound (simulation matches the exact angle)",
      sim_ok and np.allclose(J_near, -np.eye(2), atol=0.05) and abs(theta_exact(1e6)) > 4 * np.pi)

# (e) zero eigenvalue: x' = x^2, y' = -y
sl = solve_ivp(lambda u, z: [z[0] ** 2, -z[1]], (0, 500), [-0.1, 0.1], rtol=1e-10, atol=1e-14)
ev = lambda u, z: z[0] - 5
ev.terminal = True
sr = solve_ivp(lambda u, z: [z[0] ** 2, -z[1]], (0, 500), [0.1, 0.1], events=ev, rtol=1e-10, atol=1e-14)
check("l13 s7 zero eigenvalue: x'=x^2, y'=-y attracts from the left and repels on the right",
      -0.003 < sl.y[0, -1] < 0 and abs(sl.y[1, -1]) < 1e-9 and sr.status == 1)
# central-difference Jacobian
pp = lambda z: [z[0] - 0.5 * z[0] * z[1], -0.75 * z[1] + 0.25 * z[0] * z[1]]
Jn = np.array([[(pp([3 + 1e-6, 2])[i] - pp([3 - 1e-6, 2])[i]) / 2e-6 for i in range(2)], [(pp([3, 2 + 1e-6])[i] - pp([3, 2 - 1e-6])[i]) / 2e-6 for i in range(2)]]).T
check("l13 s8 central differences reproduce J(3,2) to 1e-6", np.allclose(Jn, [[0, -1.5], [0.5, 0]], atol=1e-6))
check("l13 quiz3: x'=x(2-y), y'=y(x-1) has positive equilibrium (1,2)",
      {(e[X], e[Y]) for e in sp.solve([X * (2 - Y), Y * (X - 1)], [X, Y], dict=True)} == {(0, 0), (1, 2)})
A7 = sp.Matrix([[3, -2], [2, -2]])
x7 = sp.exp(A7 * t) * sp.Matrix([1, 0])
check("homework-3 i2: x1(t) = (4/3)e^{2t} - (1/3)e^{-t}", sp.simplify(x7[0] - (sp.Rational(4, 3) * sp.exp(2 * t) - sp.exp(-t) / 3)) == 0)
check("homework-3 i6-7: spreads matrix: s'=2s, d'=-4d",
      sp.simplify((-X + 3 * Y) + (3 * X - Y) - 2 * (X + Y)) == 0 and sp.simplify((-X + 3 * Y) - (3 * X - Y) + 4 * (X - Y)) == 0)

print("\n%d passed, %d expected fails (findings), %d unexpected fails" % (len(PASSES), len(XFAILS), len(FAILS)))
for f in FAILS:
    print("UNEXPECTED: " + f)
sys.exit(1 if FAILS else 0)
