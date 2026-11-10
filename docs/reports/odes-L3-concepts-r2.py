#!/usr/bin/env python3
"""Round-2 concept checks for odes level 3 (l10 to l13, review-3, homework-3).

Independent of docs/reports/odes-L3-concepts.py (not opened while writing this).
Exit 0 when every ordinary check passes. EXPECTED_FAIL marks a check that fails
because the content is wrong or imprecise; the corrected assert is in a comment.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

FAILS, XFAILS, COUNT = [], [], [0]


def check(name, cond, note=""):
    COUNT[0] += 1
    if not bool(cond):
        FAILS.append(name)
        print("FAIL", name, note)


def expected_fail(name, claim_holds, note):
    if claim_holds:
        print("XPASS", name, "(the content claim now holds; retire this marker)")
    else:
        XFAILS.append(name)
        print("EXPECTED_FAIL", name, "|", note)


def close(a, b, tol=1e-4):
    return abs(float(a) - float(b)) <= tol


rng = np.random.default_rng(20261110)
np.seterr(over="ignore", invalid="ignore")  # expm of a growing flow overflows by design in one check
M = lambda rows: np.array(rows, dtype=float)
flow = lambda A, x0, s: expm(M(A) * s) @ np.array(x0, dtype=float)

# ---------------------------------------------------------------- l10
A0 = M([[0, 1], [-2, -3]])
check("l10_eigenvectors", np.allclose(A0 @ [1, -1], [-1, 1]) and np.allclose(A0 @ [1, -2], [-2, 4]) and np.allclose(A0 @ [1, 1], [1, -5]))
lam, p, q = sp.symbols("lambda p q")
check("l10_companion_charpoly", sp.expand(sp.Matrix([[0, 1], [-q, -p]]).charpoly(lam).as_expr() - (lam**2 + p * lam + q)) == 0)
check("l10_companion_56", sorted(np.linalg.eigvals(M([[0, 1], [-6, -5]])).real.round(9).tolist()) == [-3.0, -2.0])
c = np.linalg.solve(M([[1, 1], [-1, -2]]), [1, 0])
check("l10_weights", np.allclose(c, [2, -1]) and close(flow(A0, [1, 0], 0.7)[0], 2 * math.exp(-0.7) - math.exp(-1.4), 1e-10))
A2 = M([[-2, 2], [0, -0.5]])
check("l10_two_factor_eigen", np.allclose(A2 @ [4, 3], [-2, -1.5]) and np.allclose(A2 @ [1, 0], [-2, 0]))
c2 = np.linalg.solve(M([[1, 4], [0, 3]]), [0.02, 0.01])
x1 = flow(A2, [0.02, 0.01], 1.0)
check("l10_two_factor_solution", np.allclose(c2, [1 / 150, 1 / 300]) and close(x1[0], 0.008989, 5e-7) and close(x1[1], 0.006065, 5e-7))
check("l10_c_equals_x0_only_if_V_is_I", close(0.02 + 4 * 0.01, 0.06, 1e-12) and np.allclose(np.linalg.solve(np.eye(2), [5, 2]), [5, 2]))
Ad = M([[-1, 1], [0, -1]])
check("l10_defective", np.linalg.matrix_rank(Ad + np.eye(2)) == 1 and close(flow(Ad, [0, 1], 1.0)[0], math.exp(-1), 1e-10)
      and np.linalg.matrix_rank(M([[2, 1], [0, 2]]) - 2 * np.eye(2)) == 1)
A3 = M([[0, 1, 0], [0, 0, 1], [-5, 1, -2]])
check("l10_third_order", np.allclose(sorted(np.linalg.eigvals(A3), key=lambda v: (v.real, v.imag)), sorted(np.roots([1, 2, -1, 5]), key=lambda v: (v.real, v.imag))))


def solve_linear_system(A, x0, s):
    vals, V = np.linalg.eig(np.asarray(A, dtype=float))
    cc = np.linalg.solve(V, np.asarray(x0, dtype=float))
    return np.real(V @ (cc * np.exp(vals * s)))


for A_, x0_, s_ in [([[-2, 2], [0, -0.5]], [0.02, 0.01], 1), ([[0, 1], [-5, -2]], [1, 0], 1), ([[-2, 1], [1, -2]], [1, 0], 1), ([[0, 1], [-2, 3]], [0, 1], 1)]:
    check(f"l10_eigen_solver_matches_expm_{A_}", np.allclose(solve_linear_system(A_, x0_, s_), flow(A_, x0_, s_), atol=1e-10))
check("l10_solver_values", np.allclose(solve_linear_system([[-2, 1], [1, -2]], [1, 0], 1), [0.208833, 0.159046], atol=5e-7))
check("l10_half_lives", close(math.log(2) / 2, 0.3466, 5e-5) and close(math.log(2) / 0.5, 1.3863, 5e-5) and close(0.3466 * 12, 4.2, 0.1))

# ---------------------------------------------------------------- l11
As = M([[1, 2], [2, 1]])
check("l11_saddle", np.allclose(As @ [1, 1], [3, 3]) and np.allclose(As @ [1, -1], [-1, 1]))
check("l11_saddle_point", np.allclose(flow(As, [1, 0], 0.5), [2.5441, 1.9376], atol=5e-5))
# a stable node arrives tangent to the slow eigenvector, unless it starts on the fast one
dirs = []
for _ in range(200):
    x0 = rng.uniform(-3, 3, 2)
    if abs(x0[1]) < 0.05:
        continue
    xl = flow(A2, x0, 25.0)
    dirs.append(abs(xl[1] / xl[0] - 0.75))
check("l11_node_arrives_on_slow_eigenvector", max(dirs) < 1e-9 and abs(flow(A2, [1, 0], 5.0)[1]) < 1e-15)
# an unstable node leaves tangent to the eigenvector of the smaller eigenvalue
Au = M([[2, 0], [0, 5]])
back = flow(Au, [1.0, 1.0], -6.0)
check("l11_unstable_node_leaves_on_slow", abs(back[1] / back[0]) < 1e-7)
Asp = M([[-1, 2], [-2, -1]])
check("l11_spiral", np.allclose(sorted(np.linalg.eigvals(Asp), key=lambda v: v.imag), [-1 - 2j, -1 + 2j])
      and np.allclose(flow(Asp, [2.5, 0], math.pi), [2.5 * math.exp(-math.pi), 0], atol=1e-12) and close(math.exp(-math.pi), 0.0432, 5e-5))


def angular_sign(A, n=40):
    """Sign of x y' - y x' on a ring of points: +1 anticlockwise everywhere, -1 clockwise, 0 mixed."""
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    pts = np.stack([np.cos(ang), np.sin(ang)])
    v = A @ pts
    cr = pts[0] * v[1] - pts[1] * v[0]
    return 1 if np.all(cr > 0) else (-1 if np.all(cr < 0) else 0)


# Monte Carlo over random matrices with complex eigenvalues: the bottom-left entry is never 0,
# its sign is the turning direction for every path, and the transpose turns the other way
ok_sign, ok_transpose, n_complex = True, True, 0
while n_complex < 5000:
    A = rng.normal(size=(2, 2)) * 3
    if np.trace(A) ** 2 - 4 * np.linalg.det(A) >= -1e-6:
        continue
    n_complex += 1
    sgn = angular_sign(A)
    ok_sign &= (sgn != 0 and A[1, 0] != 0 and sgn == np.sign(A[1, 0]))
    ok_transpose &= (angular_sign(A.T) == -sgn)
check("l11_turning_is_sign_of_bottom_left", ok_sign)
check("l11_transpose_reverses_turning", ok_transpose)
check("l11_same_eigenvalues_opposite_turning", angular_sign(Asp) == -1 and angular_sign(Asp.T) == 1
      and np.allclose(sorted(np.linalg.eigvals(Asp.T), key=lambda v: v.imag), [-1 - 2j, -1 + 2j]))
Ac = M([[0, 1], [-4, 0]])
orb = np.array([flow(Ac, [1, 0.3], s) for s in np.linspace(0, 9, 200)])
check("l11_centre_conserves_H", np.allclose(4 * orb[:, 0] ** 2 + orb[:, 1] ** 2, 4.09, atol=1e-9) and angular_sign(Ac) == -1)
Az = M([[0, 0], [0, -1]])
check("l11_zero_eigenvalue_line", np.allclose(Az @ [2, 0], 0) and np.allclose(flow(Az, [1, 2], 30), [1, 0], atol=1e-12))
check("l11_sum_and_difference", np.allclose(np.array([1, 1]) @ As, 3 * np.array([1, 1])) and np.allclose(np.array([1, -1]) @ As, -1 * np.array([1, -1]))
      and close(math.log(2) / 3, 0.231, 5e-4))
check("l11_review_turn", angular_sign(M([[0, 3], [-1, 0]])) == -1 and angular_sign(M([[-3, 4], [-2, 1]])) == -1)

# ---------------------------------------------------------------- l12


def classify(A, tol=1e-9):
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


def by_eigenvalues(A):
    """Name the picture from the eigenvalues alone (lesson 11's table)."""
    ev = np.linalg.eigvals(A)
    if np.all(np.abs(ev.imag) < 1e-9):
        a, b = ev.real
        if a * b < 0:
            return "saddle"
        return ("stable" if a < 0 else "unstable") + " node"
    return ("stable" if ev.real[0] < 0 else "unstable") + " spiral"


agree, total, counts = 0, 0, {}
for _ in range(20000):
    A = rng.normal(size=(2, 2)) * 2
    tau, det = np.trace(A), np.linalg.det(A)
    if min(abs(det), abs(tau), abs(tau * tau - 4 * det)) < 1e-3:
        continue  # stay off the edges of the map
    total += 1
    name = classify(A)
    counts[name] = counts.get(name, 0) + 1
    agree += name == by_eigenvalues(A)
check("l12_map_agrees_with_eigenvalues", agree == total and len(counts) == 5 and min(counts.values()) > 200, str(counts))
check("l12_vieta", all(np.isclose(np.prod(np.linalg.eigvals(A)), np.linalg.det(A)) and np.isclose(np.sum(np.linalg.eigvals(A)), np.trace(A))
                       for A in rng.normal(size=(200, 2, 2))))
pts = {"saddle": (As, (2, -3)), "centre": (Ac, (0, 4)), "lesson10": (A0, (-3, 2)), "two": (A2, (-2.5, 1)), "spiral": (Asp, (-2, 5)),
       "eigen14": (M([[-2, 1], [1, -2]]), (-4, 3))}
check("l12_points_on_map", all(np.isclose(np.trace(A), td[0]) and np.isclose(np.linalg.det(A), td[1]) for A, td in pts.values()))
check("l12_two_factor_from_tau_det", np.allclose(sorted([(-2.5 + 1.5) / 2, (-2.5 - 1.5) / 2]), sorted(np.linalg.eigvals(A2).real)))
# screens[2].prose, read sentence by sentence: "tau^2 > 4 Delta gives a node" and "tau = 0 a centre"
# hold only with Delta > 0. Counterexamples: lesson 11's saddle and review-3's trace-zero saddle.
unconditional = (by_eigenvalues(As) == "stable node" or by_eigenvalues(As) == "unstable node") and np.trace(As) ** 2 > 4 * np.linalg.det(As)
expected_fail("l12_node_and_centre_rules_without_delta_positive", unconditional,
              "screens[2].prose: tau^2 > 4*Delta with Delta < 0 is a saddle, and tau = 0 with Delta < 0 is a saddle; "
              "corrected assert: for Delta > 0 only, tau^2 > 4*Delta is a node and tau = 0 a centre")
check("l12_trace_zero_saddle", classify(M([[2, 1], [-3, -2]])) == "saddle" and np.allclose(sorted(np.linalg.eigvals(M([[2, 1], [-3, -2]])).real), [-1, 1]))
# damping regimes are regions of the map
check("l12_damping_on_map", [classify(M([[0, 1], [-4, -b]])) for b in (1, 4, 5)] == ["stable spiral", "stable node", "stable node"]
      and classify(M([[0, 1], [-4, 0]])) == "centre")
# continuous against discrete
Ad2 = np.diag([0.9, -0.5])
check("l12_chain_stable_flow_not", np.linalg.norm(np.linalg.matrix_power(Ad2, 400)) < 1e-15 and np.linalg.norm(expm(Ad2 * 40)) > 1e15)
grow, used = 0, 0
for _ in range(2000):
    A = rng.normal(size=(2, 2))
    top = np.max(np.linalg.eigvals(A).real)
    if abs(top) < 0.1:
        continue
    used += 1
    decays = np.linalg.norm(expm(A * 150)) < 1e-3
    grow += (top < 0) != decays
check("l12_decay_iff_real_parts_negative", grow == 0 and used > 1500, f"{grow}/{used}")
Aneg = M([[-1, 3], [3, -1]])
check("l12_negative_diagonal_saddle", classify(Aneg) == "saddle" and np.allclose(Aneg @ [1, 1], [2, 2]) and np.allclose(Aneg @ [1, -1], [-4, 4]))
check("l12_nudged_centre", classify(M([[0, 1], [-4, -0.01]])) == "stable spiral" and classify(M([[0, 1], [-4, 0.01]])) == "unstable spiral")
# a centre is Lyapunov stable but not asymptotically stable
far = max(np.linalg.norm(flow(Ac, [0.01, 0.0], s)) for s in np.linspace(0, 50, 2001))
check("l12_centre_stable_not_asymptotic", far <= 0.02 + 1e-12 and np.linalg.norm(flow(Ac, [0.01, 0.0], 50 * math.pi)) > 0.0099)
# same tau and Delta on the parabola, different pictures (one eigenvector or two)
star, improper = M([[-2, 0], [0, -2]]), M([[-2, 1], [0, -2]])
check("l12_parabola_one_or_two_eigenvectors", np.trace(star) == np.trace(improper) and np.isclose(np.linalg.det(star), np.linalg.det(improper))
      and np.linalg.matrix_rank(star + 2 * np.eye(2)) == 0 and np.linalg.matrix_rank(improper + 2 * np.eye(2)) == 1)
tests = [([[-2, 2], [0, -0.5]], "stable node"), ([[1, 2], [2, 1]], "saddle"), ([[-1, 2], [-2, -1]], "stable spiral"), ([[0, 1], [-4, 0]], "centre"),
         ([[0, 1], [-4, -4]], "stable node"), ([[1, -1], [1, 1]], "unstable spiral"), ([[2, 0], [0, 5]], "unstable node"), ([[0, 0], [0, -1]], "degenerate")]
check("l12_classify_cases", all(classify(a) == n for a, n in tests))
Adr = M([[-0.3, 0.4], [0.5, -0.2]])
check("l12_drift", np.allclose(sorted(np.linalg.eigvals(Adr).real), [-0.7, 0.2]) and close(np.linalg.det(Adr), -0.14, 1e-12))

# ---------------------------------------------------------------- l13
x, y, cs = sp.symbols("x y c")
f1, f2 = x - sp.Rational(1, 2) * x * y, -sp.Rational(3, 4) * y + sp.Rational(1, 4) * x * y
check("l13_equilibria", {tuple(s) for s in sp.solve([f1, f2], [x, y])} == {(0, 0), (3, 2)})
J = sp.Matrix([f1, f2]).jacobian([x, y])
check("l13_jacobian", J.subs({x: 3, y: 2}) == sp.Matrix([[0, sp.Rational(-3, 2)], [sp.Rational(1, 2), 0]])
      and J.subs({x: 0, y: 0}) == sp.Matrix([[1, 0], [0, sp.Rational(-3, 4)]])
      and J.subs({x: 2, y: 3}) == sp.Matrix([[sp.Rational(-1, 2), -1], [sp.Rational(3, 4), sp.Rational(-1, 4)]]))
check("l13_linear_centre", set(J.subs({x: 3, y: 2}).eigenvals()) == {sp.sqrt(3) * sp.I / 2, -sp.sqrt(3) * sp.I / 2}
      and close(2 * math.pi / math.sqrt(0.75), 7.2552, 5e-5))
pp = lambda s, z, c_=0.0: [z[0] * (1 - c_ * z[0]) - 0.5 * z[0] * z[1], -0.75 * z[1] + 0.25 * z[0] * z[1]]


def period(start):
    """Time to return to the start's height, crossing y = 2 from above for the second time... one full loop."""
    ev = lambda s, z: z[1] - 2.0
    ev.direction = 1  # the start (x > 3, y = 2) moves up through y = 2
    s = solve_ivp(pp, [0, 40], start, events=ev, rtol=1e-11, atol=1e-13)
    times = [te for te in s.t_events[0] if te > 1e-6]
    return times[0]


check("l13_true_period_at_5_2", close(period([5.0, 2.0]), 7.42, 0.006), str(period([5.0, 2.0])))
check("l13_small_orbit_period_tends_to_linear", close(period([3.01, 2.0]), 7.2552, 2e-4) and period([3.4, 2.0]) < period([5.0, 2.0]))
H = sp.Rational(1, 4) * x - sp.Rational(3, 4) * sp.log(x) + sp.Rational(1, 2) * y - sp.log(y)
check("l13_H_conserved", sp.simplify(sp.diff(H, x) * f1 + sp.diff(H, y) * f2) == 0)
check("l13_H_minimum", sp.solve([sp.diff(H, x), sp.diff(H, y)], [x, y], dict=True) == [{x: 3, y: 2}]
      and all(v > 0 for v in sp.hessian(H, [x, y]).subs({x: 3, y: 2}).eigenvals()))
orbit = solve_ivp(pp, [0, 60], [5.0, 2.0], rtol=1e-11, atol=1e-13, dense_output=True).sol(np.linspace(0, 60, 3000))
check("l13_orbit_stays_positive_and_closed", orbit.min() > 0.3 and np.ptp(0.25 * orbit[0] - 0.75 * np.log(orbit[0]) + 0.5 * orbit[1] - np.log(orbit[1])) < 1e-8)
g1 = x * (1 - x / 6) - sp.Rational(1, 2) * x * y
Jc = sp.Matrix([g1, f2]).jacobian([x, y]).subs({x: 3, y: 1})
check("l13_crowded", g1.subs({x: 3, y: 1}) == 0 and f2.subs({x: 3, y: 1}) == 0
      and Jc == sp.Matrix([[sp.Rational(-1, 2), sp.Rational(-3, 2)], [sp.Rational(1, 4), 0]])
      and set(Jc.eigenvals()) == {-sp.Rational(1, 4) + sp.sqrt(5) * sp.I / 4, -sp.Rational(1, 4) - sp.sqrt(5) * sp.I / 4}
      and close(math.sqrt(5) / 4, 0.5590, 5e-5))
end = solve_ivp(lambda s, z: pp(s, z, 1 / 6), [0, 120], [5.0, 2.0], rtol=1e-10, atol=1e-12).y[:, -1]
check("l13_crowded_path_settles", np.allclose(end, [3, 1], atol=1e-5))
# a linear centre that the nonlinear terms turn into a (slow) inward spiral
cub = solve_ivp(lambda s, z: [-z[1] - z[0] ** 3, z[0] - z[1] ** 3], [0, 400], [0.5, 0.0], rtol=1e-10, atol=1e-13, dense_output=True)
rad = np.linalg.norm(cub.sol(np.linspace(0, 400, 4001)), axis=0)
check("l13_linear_centre_can_spiral_in", np.all(np.diff(rad) <= 1e-12) and rad[-1] < 0.06)
# and the mirror image spirals out: the linear centre decides neither way
cub2 = solve_ivp(lambda s, z: [-z[1] + z[0] ** 3, z[0] + z[1] ** 3], [0, 1.5], [0.5, 0.0], rtol=1e-10, atol=1e-13)
check("l13_linear_centre_can_spiral_out", np.linalg.norm(cub2.y[:, -1]) > 0.55)
# zero eigenvalue with the other negative: x' = x^2, y' = -y attracts from the left, repels on the right
left = solve_ivp(lambda s, z: [z[0] ** 2, -z[1]], [0, 2000], [-0.5, 0.5], rtol=1e-10, atol=1e-13).y[:, -1]
right = solve_ivp(lambda s, z: [z[0] ** 2, -z[1]], [0, 1.9], [0.5, 0.5], rtol=1e-10, atol=1e-13).y[:, -1]
check("l13_zero_eigenvalue_example", abs(left[0]) < 1e-3 and left[0] < 0 and right[0] > 5)
# summary.ideas[1]: "a zero eigenvalue decides nothing". With the other eigenvalue positive the
# linearisation does decide: unstable, whatever the nonlinear terms (here they even pull x in).
runs = [np.linalg.norm(solve_ivp(lambda s, z: [-z[0] ** 3, z[1]], [0, 12], [d, d], rtol=1e-10, atol=1e-13).y[:, -1]) for d in (1e-2, 1e-3, 1e-4)]
zero_decides_nothing = not all(rn > 1 for rn in runs)
expected_fail("l13_zero_eigenvalue_decides_nothing", zero_decides_nothing,
              "summary.ideas[1]: eigenvalues 0 and +1 (x' = -x^3, y' = y) are unstable from the linearisation alone; "
              "corrected assert: a zero eigenvalue leaves stability open only when no eigenvalue has positive real part")
# hyperbolic equilibria: stability carries over under small smooth nonlinear terms (Monte Carlo)
carried, tried = 0, 0
while tried < 150:
    A = rng.normal(size=(2, 2))
    ev = np.linalg.eigvals(A)
    if np.min(np.abs(ev.real)) < 0.3:
        continue
    tried += 1
    B = rng.normal(size=(2, 3))
    rhs = lambda s, z, A=A, B=B: A @ z + B @ np.array([z[0] ** 2, z[0] * z[1], z[1] ** 2])
    z0 = rng.normal(size=2)
    z0 *= 1e-4 / np.linalg.norm(z0)
    if np.all(ev.real < 0):
        zT = solve_ivp(rhs, [0, 20], z0, rtol=1e-9, atol=1e-15).y[:, -1]
        carried += np.linalg.norm(zT) < 1e-5
    else:
        hit = lambda s, z: np.linalg.norm(z) - 1e-2
        hit.terminal = True
        s = solve_ivp(rhs, [0, 80], z0, rtol=1e-9, atol=1e-15, events=hit)
        carried += len(s.t_events[0]) > 0
check("l13_hyperbolic_stability_carries_over", carried == tried, f"{carried}/{tried}")


def jacobian(f, z, h=1e-6):
    z = np.asarray(z, dtype=float)
    Jn = np.zeros((len(z), len(z)))
    for k_ in range(len(z)):
        e = np.zeros(len(z))
        e[k_] = h
        Jn[:, k_] = (np.asarray(f(z + e)) - np.asarray(f(z - e))) / (2 * h)
    return Jn


ppl = lambda z: pp(0, z)
check("l13_numeric_jacobian", np.allclose(jacobian(ppl, [3, 2]), [[0, -1.5], [0.5, 0]], atol=1e-7)
      and classify(jacobian(ppl, [3, 2]), 1e-6) == "centre" and classify(jacobian(ppl, [0, 0]), 1e-6) == "saddle"
      and classify(jacobian(lambda z: pp(0, z, 1 / 6), [3, 1]), 1e-6) == "stable spiral")
check("l13_quiz_eq", {tuple(s) for s in sp.solve([x * (2 - y), y * (x - 1)], [x, y])} == {(0, 0), (1, 2)})

# ---------------------------------------------------------------- review-3, homework-3
check("r3_companion", sorted(np.linalg.eigvals(M([[0, 1], [-3, -4]])).real.round(9).tolist()) == [-3.0, -1.0])
check("r3_weights", np.allclose(np.linalg.solve(M([[1, 1], [1, -1]]), [3, 1]), [2, 1]))
h1, h2 = x * (1 - x) - x * y, y * (x - sp.Rational(1, 2))
Jr = sp.Matrix([h1, h2]).jacobian([x, y]).subs({x: sp.Rational(1, 2), y: sp.Rational(1, 2)})
check("r3_linearise", Jr == sp.Matrix([[-sp.Rational(1, 2), -sp.Rational(1, 2)], [sp.Rational(1, 2), 0]]) and Jr.det() == sp.Rational(1, 4)
      and classify(np.array(Jr, dtype=float)) == "stable spiral" and close(math.sqrt(0.1875), 0.433, 5e-4))
rs = solve_ivp(lambda s, z: [z[0] * (1 - z[0]) - z[0] * z[1], z[1] * (z[0] - 0.5)], [0, 150], [0.6, 0.4], rtol=1e-10, atol=1e-12).y[:, -1]
check("r3_spiral_trusted_for_nonlinear", np.allclose(rs, [0.5, 0.5], atol=1e-6))
check("r3_slow_mode", sorted(np.linalg.eigvals(M([[-3, 1], [1, -3]])).real.round(9).tolist()) == [-4.0, -2.0])
Ah = M([[3, -2], [2, -2]])
check("h3_solve", np.allclose(Ah @ [2, 1], [4, 2]) and np.allclose(Ah @ [1, 2], [-1, -2]) and close(flow(Ah, [1, 0], 1.0)[0], 9.7294, 5e-5)
      and close(2 * math.e**2, 14.7781, 5e-5))
check("h3_sketch", classify(M([[-3, 4], [-2, 1]])) == "stable spiral" and angular_sign(M([[-3, 4], [-2, 1]])) == -1)
k1, k2 = x * (3 - x - 2 * y), y * (2 - x - y)
Jk = sp.Matrix([k1, k2]).jacobian([x, y]).subs({x: 1, y: 1})
check("h3_competition", Jk == sp.Matrix([[-1, -2], [-1, -1]]) and set(Jk.eigenvals()) == {-1 + sp.sqrt(2), -1 - sp.sqrt(2)})
wins = 0
for _ in range(60):
    z0 = np.array([1.0, 1.0]) + rng.normal(size=2) * 0.05
    zT = solve_ivp(lambda s, z: [z[0] * (3 - z[0] - 2 * z[1]), z[1] * (2 - z[0] - z[1])], [0, 80], z0, rtol=1e-9, atol=1e-12).y[:, -1]
    wins += np.allclose(zT, [3, 0], atol=1e-4) or np.allclose(zT, [0, 2], atol=1e-4)
check("h3_competition_one_wins", wins == 60, str(wins))
check("h3_sum_difference", np.allclose(np.array([1, 1]) @ Aneg, 2 * np.array([1, 1])) and np.allclose(np.array([1, -1]) @ Aneg, -4 * np.array([1, -1]))
      and close(math.log(2) / 4, 0.1733, 5e-5))
pl = lambda z: [z[0] ** 2 - 1, z[1]]
check("h3_newton_types", classify(jacobian(pl, [-1, 0]), 1e-6) == "saddle" and classify(jacobian(pl, [1, 0]), 1e-6) == "unstable node"
      and abs(np.linalg.det(jacobian(pl, [0.0, 0.5]))) < 1e-14)

print(f"odes L3 concepts r2: {COUNT[0]} checks, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL")
sys.exit(1 if FAILS else 0)
