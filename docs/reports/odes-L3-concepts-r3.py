#!/usr/bin/env python3
"""Concept audit round 3, odes level 3 (l10 to l13, review-3, homework-3).

Independent sympy, numerical and random-matrix checks of the claims in the ledger
(docs/reports/audit-odes-1-3-r3-ledger.md). Exit 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

FAILS = []
NOTES = []


def check(name, ok, expected_fail=False):
    if ok:
        print("PASS         ", name)
    elif expected_fail:
        print("EXPECTED_FAIL", name)
        NOTES.append(name)
    else:
        print("FAIL         ", name)
        FAILS.append(name)


rng = np.random.default_rng(20261110)
t = sp.Symbol("t", real=True)

# ---- l10: systems -----------------------------------------------------------
lam = sp.Symbol("lambda")
p, q = sp.symbols("p q")
comp = sp.Matrix([[0, 1], [-q, -p]])
check("companion_char_poly", sp.expand(comp.charpoly(lam).as_expr() - (lam ** 2 + p * lam + q)) == 0)
c3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [-5, 1, -2]])
check("third_order_companion", sp.expand(c3.charpoly(lam).as_expr() - (lam ** 3 + 2 * lam ** 2 - lam + 5)) == 0)
A2 = sp.Matrix([[-2, 2], [0, sp.Rational(-1, 2)]])
check("two_factor_eigenvector", A2 * sp.Matrix([4, 3]) == sp.Rational(-1, 2) * sp.Matrix([4, 3]) and A2 * sp.Matrix([1, 0]) == -2 * sp.Matrix([1, 0]))
xt = sp.Rational(1, 150) * sp.exp(-2 * t) * sp.Matrix([1, 0]) + sp.Rational(1, 300) * sp.exp(-t / 2) * sp.Matrix([4, 3])
check("two_factor_solution", sp.simplify(sp.diff(xt, t) - A2 * xt) == sp.zeros(2, 1) and xt.subs(t, 0) == sp.Matrix([sp.Rational(1, 50), sp.Rational(1, 100)])
      and abs(float(xt[0].subs(t, 1)) - 0.008989) < 5e-7 and abs(float(xt[1].subs(t, 1)) - 0.006065) < 5e-7)
Ad = sp.Matrix([[-1, 1], [0, -1]])
check("defective_one_eigenvector", len(Ad.eigenvects()) == 1 and Ad.eigenvects()[0][1] == 2 and len(Ad.eigenvects()[0][2]) == 1)
check("defective_solution_te^-t", sp.simplify((Ad * t).exp() * sp.Matrix([0, 1]) - sp.Matrix([t * sp.exp(-t), sp.exp(-t)])) == sp.zeros(2, 1))
# c = x(0) only when V = I: random check that V c = x0 reproduces expm
ok = True
for _ in range(200):
    A = rng.normal(size=(2, 2)); x0 = rng.normal(size=2)
    vals, V = np.linalg.eig(A)
    c = np.linalg.solve(V, x0.astype(complex))
    ok &= np.allclose(np.real(V @ (c * np.exp(vals * 0.7))), expm(0.7 * A) @ x0, atol=1e-8)
check("eigenvector_solution_matches_expm (200 random matrices)", ok)
check("hw3_saddle_solution", abs(4 / 3 * math.exp(2) - math.exp(-1) / 3 - 9.7294) < 5e-5
      and np.allclose(expm(np.array([[3.0, -2.0], [2.0, -2.0]])) @ [1, 0], [4 / 3 * math.exp(2) - math.exp(-1) / 3, 2 / 3 * math.exp(2) - 2 / 3 * math.exp(-1)]))

# ---- l11: phase plane -------------------------------------------------------
S = np.array([[1.0, 2.0], [2.0, 1.0]])
check("saddle_point_at_0.5", np.allclose(expm(0.5 * S) @ [1, 0], [2.5441, 1.9376], atol=5e-5))
# stable node: paths off the fast eigenvector arrive tangent to the slow one (4, 3)
An = np.array([[-2.0, 2.0], [0.0, -0.5]])
ok = True
for _ in range(200):
    x0 = rng.normal(size=2)
    if abs(x0[1]) < 1e-3:
        continue
    v = expm(12 * An) @ x0
    ok &= abs(abs(v @ np.array([4, 3])) / (5 * np.linalg.norm(v)) - 1) < 1e-6
check("node_arrives_along_slow_eigenvector (random starts)", ok)
# unstable node 2, 5: paths leave tangent to the eigenvector of 2
Au = np.diag([2.0, 5.0])
v = expm(-6 * Au) @ np.array([1.0, 1.0])
check("unstable_node_leaves_along_smaller_eigenvalue", abs(v[1] / v[0]) < 1e-6)
# direction of turning: sign of the bottom-left entry, for every matrix with complex eigenvalues
ok = True; n = 0
while n < 5000:
    A = rng.normal(size=(2, 2))
    if np.trace(A) ** 2 - 4 * np.linalg.det(A) >= 0:
        continue
    n += 1
    ok &= A[1, 0] != 0
    for _ in range(4):
        x = rng.normal(size=2); v = A @ x
        ok &= np.sign(x[0] * v[1] - x[1] * v[0]) == np.sign(A[1, 0])   # sign of the angular velocity
check("turning_is_sign_of_bottom_left_entry (5000 random spirals, 4 points each)", bool(ok))
Asp = np.array([[-1.0, 2.0], [-2.0, -1.0]])
check("spiral_shrinks_e^-pi_per_turn", np.allclose(expm(math.pi * Asp) @ [1, 0], [math.exp(-math.pi), 0], atol=1e-12)
      and abs(math.exp(-math.pi) - 0.0432) < 5e-5)
check("transpose_same_eigenvalues", np.allclose(sorted(np.linalg.eigvals(Asp), key=np.imag), sorted(np.linalg.eigvals(Asp.T), key=np.imag)))
x, y = sp.symbols("x y", real=True)
check("centre_conserves_4x^2+y^2", sp.simplify(8 * x * y + 2 * y * (-4 * x)) == 0)
check("sum_and_difference_modes", np.allclose(np.array([1, 1]) @ S, 3 * np.array([1, 1])) and np.allclose(np.array([1, -1]) @ S, -1 * np.array([1, -1])))

# ---- l12: trace and determinant --------------------------------------------
def classify(A, tol=1e-9):
    tau, det = np.trace(A), np.linalg.det(A)
    if abs(det) <= tol:
        return "degenerate"
    if det < 0:
        return "saddle"
    if abs(tau) <= tol:
        return "centre"
    side = "stable" if tau < 0 else "unstable"
    return side + (" node" if tau * tau - 4 * det >= -tol else " spiral")


def from_eigs(A):
    l1, l2 = np.linalg.eigvals(A)
    if abs(l1.imag) > 1e-12:
        return ("stable" if l1.real < 0 else "unstable") + " spiral"
    if l1.real * l2.real < 0:
        return "saddle"
    return ("stable" if l1.real < 0 else "unstable") + " node"


check("map_agrees_with_eigenvalues (20000 random matrices)", all(classify(A) == from_eigs(A) for A in rng.normal(size=(20000, 2, 2))))
# asymptotic stability iff every real part < 0; chain iff every |lambda| < 1
ok = True
with np.errstate(all="ignore"):
    for A in rng.normal(size=(300, 2, 2)):
        ev = np.linalg.eigvals(A)
        big = expm(400 * A)
        flow = bool(np.all(np.isfinite(big)) and np.linalg.norm(big) < 1e-6)
        pw = np.linalg.matrix_power(A, 4000)
        chain = bool(np.all(np.isfinite(pw)) and np.linalg.norm(pw) < 1e-6)
        if min(abs(ev.real)) > 0.1:
            ok &= flow == bool(np.all(ev.real < 0))
        if abs(max(abs(ev)) - 1) > 0.05:
            ok &= chain == bool(np.all(abs(ev) < 1))
check("continuous_vs_discrete_tests (300 random matrices)", bool(ok))
Dg = np.diag([0.9, -0.5])
check("0.9_and_-0.5", np.linalg.norm(np.linalg.matrix_power(Dg, 500)) < 1e-12 and np.linalg.norm(expm(50 * Dg)) > 1e12)
Asd = np.array([[-1.0, 3.0], [3.0, -1.0]])
check("negative_diagonal_saddle", sorted(np.linalg.eigvals(Asd).real.round(9)) == [-4.0, 2.0] and classify(Asd) == "saddle")
# a centre is Lyapunov stable but not asymptotically stable
orb = np.array([expm(s * np.array([[0.0, 1.0], [-4.0, 0.0]])) @ [0.1, 0.0] for s in np.linspace(0, 50, 2001)])
check("centre_stays_near_never_settles", np.linalg.norm(orb, axis=1).max() <= 0.2 + 1e-9 and np.linalg.norm(orb, axis=1).min() >= 0.1 - 1e-9)
check("nudged_centre_is_stable_spiral", classify(np.array([[0.0, 1.0], [-4.0, -0.01]])) == "stable spiral")
# on the parabola: same tau, Delta, different pictures (one eigenvector or two)
star, degn = sp.Matrix([[-2, 0], [0, -2]]), sp.Matrix([[0, 1], [-4, -4]])
check("parabola_one_or_two_eigenvectors", star.trace() == degn.trace() and star.det() == degn.det()
      and len(star.eigenvects()[0][2]) == 2 and len(degn.eigenvects()[0][2]) == 1)
check("drift_matrix_eigs", np.allclose(sorted(np.linalg.eigvals(np.array([[-0.3, 0.4], [0.5, -0.2]]))), [-0.7, 0.2]))

# ---- l13: linearising -------------------------------------------------------
c = sp.Symbol("c", nonnegative=True)
f1, f2 = x * (1 - c * x) - x * y / 2, -sp.Rational(3, 4) * y + x * y / 4
J = sp.Matrix([f1, f2]).jacobian([x, y])
eq0 = sp.solve([f1.subs(c, 0), f2], [x, y], dict=True)
check("lv_equilibria", sorted((e[x], e[y]) for e in eq0) == [(0, 0), (3, 2)])
J32 = J.subs({c: 0, x: 3, y: 2})
check("lv_jacobians", J32 == sp.Matrix([[0, sp.Rational(-3, 2)], [sp.Rational(1, 2), 0]])
      and J.subs({c: 0, x: 0, y: 0}) == sp.diag(1, sp.Rational(-3, 4))
      and J.subs({c: sp.Rational(1, 6), x: 3, y: 1}) == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(-3, 2)], [sp.Rational(1, 4), 0]]))
H = x / 4 - sp.Rational(3, 4) * sp.log(x) + y / 2 - sp.log(y)
check("lv_H_conserved", sp.simplify(sp.diff(H, x) * f1.subs(c, 0) + sp.diff(H, y) * f2) == 0)
check("lv_H_minimum_at_(3,2)", sp.solve([sp.diff(H, x), sp.diff(H, y)], [x, y], dict=True) == [{x: 3, y: 2}]
      and sp.hessian(H, [x, y]).subs({x: 3, y: 2}).is_positive_definite)
lv = lambda s, u: [u[0] - 0.5 * u[0] * u[1], -0.75 * u[1] + 0.25 * u[0] * u[1]]
ev = lambda s, u: u[1] - 2.0
ev.direction = 1
per = lambda x0: solve_ivp(lv, [0, 20], [x0, 2.0], events=ev, rtol=1e-12, atol=1e-14).t_events[0][1]
check("lv_periods", abs(per(5.0) - 7.42) < 0.005 and abs(per(3.01) - 2 * math.pi / math.sqrt(0.75)) < 1e-3
      and abs(2 * math.pi / math.sqrt(0.75) - 7.2552) < 5e-5)
cr = lambda s, u: [u[0] * (1 - u[0] / 6) - 0.5 * u[0] * u[1], -0.75 * u[1] + 0.25 * u[0] * u[1]]
end = solve_ivp(cr, [0, 200], [5.0, 2.0], rtol=1e-10, atol=1e-12).y[:, -1]
check("crowded_settles_at_(3,1)", np.allclose(end, [3, 1], atol=1e-6)
      and np.allclose(np.linalg.eigvals(np.array([[-0.5, -1.5], [0.25, 0.0]])).imag.max(), math.sqrt(5) / 4))
# a linear centre decides nothing: x' = -y - x^3, y' = x - y^3 spirals in
check("cubic_centre_spirals_in", sp.simplify(x * (-y - x ** 3) + y * (x - y ** 3) + (x ** 4 + y ** 4)) == 0)
rr = solve_ivp(lambda s, u: [-u[1] - u[0] ** 3, u[0] - u[1] ** 3], [0, 400], [0.5, 0.0], rtol=1e-10, atol=1e-12)
check("cubic_centre_spirals_in_numeric", np.hypot(*rr.y[:, -1]) < 0.06 and np.unwrap(np.arctan2(rr.y[1], rr.y[0]))[-1] > 300)
# a node with equal eigenvalues may become a spiral (Boyce and DiPrima 9.3, table 9.3.1):
# x' = -x - y/ln r, y' = -y + x/ln r has theta' = 1/ln r, so the angle is unbounded as r -> 0
rs = sp.sqrt(x ** 2 + y ** 2)
sx, sy = -x - y / sp.log(rs), -y + x / sp.log(rs)
check("equal_eigenvalue_node_can_spiral", sp.simplify(x * sx + y * sy + rs ** 2) == 0            # r' = -r
      and sp.simplify((x * sy - y * sx) / rs ** 2 - 1 / sp.log(rs)) == 0                          # theta' = 1/ln r
      and sp.integrate(1 / (sp.log(sp.Rational(1, 2)) - t), (t, 0, sp.oo)) == -sp.oo)             # the angle is unbounded
# a node with distinct eigenvalues stays a node: x' = -x + y^2, y' = -2y + x^2 (bounded angle)
nd = solve_ivp(lambda s, u: [-u[0] + u[1] ** 2, -2 * u[1] + u[0] ** 2], [0, 60], [0.3, 0.3], rtol=1e-12, atol=1e-300, method="DOP853")
angn = np.unwrap(np.arctan2(nd.y[1], nd.y[0]))
check("distinct_node_stays_node", np.ptp(angn) < math.pi and abs(nd.y[1, -1] / nd.y[0, -1]) < 1e-6)
# zero eigenvalue: x' = x^2, y' = -y
check("zero_eigenvalue_semi_stable", solve_ivp(lambda s, u: [u[0] ** 2, -u[1]], [0, 200], [-0.5, 0.5], rtol=1e-10, atol=1e-13).y[0, -1] > -0.01
      and solve_ivp(lambda s, u: [u[0] ** 2, -u[1]], [0, 1.9], [0.5, 0.5], rtol=1e-10, atol=1e-13).y[0, -1] > 5)
# zero eigenvalue with the other positive: unstable whatever the nonlinear terms (x' = -x^3, y' = y)
check("zero_plus_positive_is_unstable", abs(solve_ivp(lambda s, u: [-u[0] ** 3, u[1]], [0, 20], [0.0, 1e-6], rtol=1e-10, atol=1e-15).y[1, -1]) > 100)
# l13 screens[7].widget.options[2].why answers "a line of equilibria" with "only the origin is still".
# The question is about the LINEARISATION, and the linearised system does have a line of equilibria.
J0 = sp.Matrix([x ** 2, -y]).jacobian([x, y]).subs({x: 0, y: 0})
check("FINDING_6 linearisation_at_origin_has_only_the_origin_still (l13 screens[7] options[2].why)",
      len(J0.nullspace()) == 0, expected_fail=True)
# corrected assert: assert J0.nullspace() == [sp.Matrix([1, 0])]   (the linear system has the whole x axis still)
# competing strategies (homework-3 items[4])
g1, g2 = x * (3 - x - 2 * y), y * (2 - x - y)
Jc = sp.Matrix([g1, g2]).jacobian([x, y])
check("competition_saddle", Jc.subs({x: 1, y: 1}) == sp.Matrix([[-1, -2], [-1, -1]]) and Jc.subs({x: 1, y: 1}).det() == -1
      and all(sp.re(e) < 0 for e in Jc.subs({x: 3, y: 0}).eigenvals()) and all(sp.re(e) < 0 for e in Jc.subs({x: 0, y: 2}).eigenvals()))
wins = set()
for x0 in rng.uniform(0.1, 3, size=(40, 2)):
    e = solve_ivp(lambda s, u: [u[0] * (3 - u[0] - 2 * u[1]), u[1] * (2 - u[0] - u[1])], [0, 400], x0, rtol=1e-9, atol=1e-12).y[:, -1]
    wins.add((round(e[0]), round(e[1])))
check("competition_one_strategy_wins (40 random starts)", wins <= {(3, 0), (0, 2)} and len(wins) == 2)
g = sp.Matrix([x * (1 - x) - x * y, y * (x - sp.Rational(1, 2))]).jacobian([x, y]).subs({x: sp.Rational(1, 2), y: sp.Rational(1, 2)})
check("rev3_jacobian", g == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(-1, 2)], [sp.Rational(1, 2), 0]]) and g.det() == sp.Rational(1, 4))

print()
print("expected fails (findings):", len(NOTES))
print("unexpected fails:", len(FAILS))
sys.exit(1 if FAILS else 0)
