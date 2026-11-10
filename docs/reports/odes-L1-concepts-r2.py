#!/usr/bin/env python3
"""Round-2 concept checks for odes level 1 (l1 to l5, review-1, homework-1).

Independent of docs/reports/odes-L1-concepts.py (not opened while writing this).
Each check tests a claim made in the lesson text, not its arithmetic alone.
Exit 0 when every ordinary check passes. A check that fails because the content
is wrong or imprecise is EXPECTED_FAIL: it is reported, the corrected assert sits
beside it in a comment, and the exit code is unchanged.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

FAILS, XFAILS, COUNT = [], [], [0]


def check(name, cond, note=""):
    COUNT[0] += 1
    if not bool(cond):
        FAILS.append(name)
        print("FAIL", name, note)


def expected_fail(name, claim_holds, note):
    """claim_holds is the content's claim as written; it should be False."""
    if claim_holds:
        print("XPASS", name, "(the content claim now holds; retire this marker)")
    else:
        XFAILS.append(name)
        print("EXPECTED_FAIL", name, "|", note)


def close(a, b, tol=1e-4):
    return abs(float(a) - float(b)) <= tol


t, y, C, k, K = sp.symbols("t y C k K")
Y = sp.Function("y")


def solves(expr, rhs_of, var=t):
    """True when d(expr)/dvar == rhs_of(var, expr) identically."""
    return sp.simplify(sp.diff(expr, var) - rhs_of(var, expr)) == 0


# ---------------------------------------------------------------- l1
B = 1000 * sp.exp(sp.Rational(5, 100) * t)
check("l1_continuous_solves", solves(B, lambda s, v: sp.Rational(5, 100) * v))
check("l1_line_fails", not solves(1000 + 50 * t, lambda s, v: sp.Rational(5, 100) * v))
yearly = 1000 * sp.Rational(105, 100) ** t
check("l1_yearly_slope_is_ln105_B", sp.simplify(sp.diff(yearly, t) / yearly - sp.log(sp.Rational(105, 100))) == 0)
check("l1_ln105", close(math.log(1.05), 0.0488, 5e-5))
check("l1_B1_B10", close(1000 * math.exp(0.05), 1051.27, 0.005) and close(1000 * math.exp(0.5), 1648.72, 0.005))
check("l1_3e2t_solves", solves(3 * sp.exp(2 * t), lambda s, v: 2 * v))
check("l1_family_C", solves(C * sp.exp(t / 2), lambda s, v: v / 2) and close(5.4366 / math.e, 2, 1e-4))
L = 200000 - 100000 * sp.exp(sp.Rational(6, 100) * t)
check("l1_loan_curve_solves", solves(L, lambda s, v: sp.Rational(6, 100) * v - 12000) and L.subs(t, 0) == 100000)
check("l1_loan_about_11_6", close(math.log(2) / 0.06, 11.6, 0.05))
r = sp.Rational(4, 100) + sp.Rational(2, 100) * sp.exp(-t / 2)
check("l1_rate_curve_solves", solves(r, lambda s, v: sp.Rational(1, 2) * (sp.Rational(4, 100) - v)))
check("l1_rprime0", close(0.5 * (0.04 - 0.06), -0.01, 1e-12))


def is_linear(F, deps):
    """F(t, y, y', ...) = 0 is linear when every second partial in the deps vanishes."""
    return all(sp.simplify(sp.diff(F, a, b)) == 0 for a in deps for b in deps)


y1, y2 = sp.symbols("y1 y2")
check("l1_linear_examples", is_linear(t * y1 + y - sp.sin(t), [y, y1]) and is_linear(y1 - t**2 * y - sp.exp(t), [y, y1])
      and is_linear(y1 - sp.Rational(6, 100) * y + 12000, [y, y1]) and is_linear(y2 + y, [y, y1, y2]))
check("l1_nonlinear_examples", not is_linear(y1 - y**2, [y, y1]) and not is_linear(y * y1 - t, [y, y1])
      and not is_linear(y1 - sp.sin(y), [y, y1]))
# one point is not enough: 1 + 2t matches y' = 2y only at t = 0
res = sp.diff(1 + 2 * t, t) - 2 * (1 + 2 * t)
check("l1_tangent_line_only_t0", sp.solve(res, t) == [0] and sp.series(sp.exp(2 * t), t, 0, 2).removeO() == 1 + 2 * t)
check("l1_generalise_options", solves(2 * sp.exp(-3 * t), lambda s, v: -3 * v) and not solves(sp.exp(-3 * t) + 1, lambda s, v: -3 * v)
      and not solves(2 - 3 * t, lambda s, v: -3 * v))
# uniqueness needs f_y continuous: y' = 3 y^(2/3), y(0) = 0 has two solutions (0 and t^3)
check("l1_uniqueness_hypothesis_matters", sp.simplify(sp.diff(t**3, t) - 3 * (t**3) ** sp.Rational(2, 3)).subs(t, 2) == 0)
n = sp.symbols("n", positive=True)
check("l1_compounding_limit", sp.limit((1 + sp.Rational(5, 100) / n) ** n, n, sp.oo) == sp.exp(sp.Rational(1, 20)))
check("l1_compounding_rows", close(1000 * (1 + 0.05 / 12) ** 12, 1051.16, 0.005) and close(1000 * (1 + 0.05 / 365) ** 365, 1051.27, 0.005))
check("l1_discount", close(math.exp(-0.2), 0.8187, 5e-5) and close(1.04 ** -5, 0.8219, 5e-5))
check("l1_constant_solution", sp.solve(0 - 2 * C, C) == [0])
# residual on a grid: zero at grid points does not prove a solution (the lesson's own test 2)
ts1 = np.array([0.0])
check("l1_grid_residual_can_be_zero_for_non_solution", np.max(np.abs((2 + 0 * ts1) - 2 * (1 + 2 * ts1))) == 0.0)
check("l1_console_residuals", np.allclose((2 + 0 * np.array([0, .5, 1])) - 2 * (1 + 2 * np.array([0, .5, 1])), [0, -2, -4]))

# ---------------------------------------------------------------- l2
T, rr = sp.symbols("T r")
check("l2_discount_factor", solves(sp.exp(-rr * T), lambda s, v: -rr * v, T))
Bv = 1000 * sp.exp(sp.Rational(3, 100) * t + sp.Rational(5, 1000) * t**2)
check("l2_varying_rate", solves(Bv, lambda s, v: (sp.Rational(3, 100) + sp.Rational(1, 100) * s) * v) and close(Bv.subs(t, 2), 1083.29, 0.005))
P, P0 = sp.symbols("P P0", positive=True)
check("l2_partial_fractions", sp.simplify(1 / (P * (1 - P / K)) - (1 / P + 1 / (K - P))) == 0)
Pt = K / (1 + (K - P0) / P0 * sp.exp(-k * t))
check("l2_logistic_solves", sp.simplify(sp.diff(Pt, t) - k * Pt * (1 - Pt / K)) == 0 and sp.simplify(Pt.subs(t, 0) - P0) == 0)
check("l2_integral_sign", sp.simplify(sp.diff(-sp.log(K - P), P) - 1 / (K - P)) == 0)
check("l2_P3", close(10000 / (1 + 9 * math.exp(-2.4)), 5505.21, 0.005))
check("l2_fastest_at_half_K", sp.solve(sp.diff(k * P * (1 - P / K), P), P) == [K / 2])
check("l2_constant_solutions", set(sp.solve(k * P * (1 - P / K), P)) == {K} or set(sp.solve(k * y * (1 - y / K), y)) == {0, K})
check("l2_formula_gives_K_not_0", sp.simplify(Pt.subs(P0, K) - K) == 0 and sp.limit(Pt, P0, 0, "+") == 0)
check("l2_blowup", solves(1 / (1 - t), lambda s, v: v**2) and solves(2 / (1 - 2 * t), lambda s, v: v**2))
w = sp.exp(t / 2) + 2
check("l2_added_constant_fails_by_one", sp.simplify(sp.diff(w, t) - (w / 2 - 1)) == 0)


def separable(f):
    """f(t, y) = g(t) h(y) on a region where f != 0 iff f f_ty = f_t f_y."""
    return sp.simplify(f * sp.diff(f, t, y) - sp.diff(f, t) * sp.diff(f, y)) == 0


check("l2_separable_quiz", separable(t * y**2) and separable(sp.exp(t + y)) and separable(3 * y) and not separable(t + y))
check("l2_half_K_time", close(math.log(9) / 0.8, 2.7465, 5e-5))
f_ = sp.symbols("f", positive=True)
tt = sp.log(f_ * (K - P0) / ((1 - f_) * P0)) / k
check("l2_time_to_fraction", sp.simplify(Pt.subs(t, tt) - f_ * K) == 0)
check("l2_exponential_overshoots", close(1000 * math.exp(2.4), 11023.18, 0.01) and 1000 * math.exp(2.4) > 10000)
check("l2_df_two_years", close(math.exp(-0.08), 0.9231, 5e-5))

# ---------------------------------------------------------------- l3
Bs = 24000 * (sp.exp(t / 20) - 1)
check("l3_savings", solves(Bs, lambda s, v: v / 20 + 1200) and close(Bs.subs(t, 10), 15569.31, 0.005))
mu = sp.exp(-t / 20)
Bf = sp.Function("B")(t)
check("l3_product_rule_backwards", sp.simplify(sp.diff(mu * Bf, t) - mu * (sp.diff(Bf, t) - Bf / 20)) == 0)
yv = sp.Rational(1, 2) + sp.Rational(1, 2) * sp.exp(-t**2)
check("l3_varying_coefficient", solves(yv, lambda s, v: s - 2 * s * v) and yv.subs(t, 0) == 1 and close(yv.subs(t, 1), 0.6839, 5e-5))
w1 = t / 2 - sp.Rational(1, 4) + sp.Rational(5, 4) * sp.exp(-2 * t)
w2 = (t**2 / 2 + 1) * sp.exp(-t**2)
check("l3_wrong_workings", sp.simplify(sp.diff(sp.exp(2 * t) * w1, t) - t * sp.exp(2 * t)) == 0 and w1.subs(t, 0) == 1
      and sp.simplify(sp.diff(sp.exp(t**2) * w2, t) - t) == 0 and close(w1.subs(t, 1), 0.4192, 5e-5) and close(w2.subs(t, 1), 0.5518, 5e-5))
check("l3_wrong_curves_are_not_solutions", not solves(w1, lambda s, v: s - 2 * s * v) and not solves(w2, lambda s, v: s - 2 * s * v))
a, q, y0 = sp.symbols("a q y0")
yc = (y0 + q / a) * sp.exp(a * t) - q / a
check("l3_const_coeff_formula", solves(yc, lambda s, v: a * v + q) and sp.simplify(yc.subs(t, 0) - y0) == 0
      and sp.simplify(yc - (y0 * sp.exp(a * t) + (q / a) * (sp.exp(a * t) - 1))) == 0)
check("l3_a_to_zero_limit", sp.simplify(sp.limit(yc, a, 0) - (y0 + q * t)) == 0)
p_, q_ = sp.Function("p")(t), sp.Function("q")(t)
mug = sp.exp(sp.Integral(p_, t))
check("l3_mu_prime", sp.simplify(sp.diff(mug, t) - p_ * mug) == 0)
check("l3_e_to_p_is_wrong", sp.simplify(sp.diff(sp.exp(p_), t) - p_ * sp.exp(p_)) != 0)
L0, pay, r_ = sp.symbols("L0 pay r", positive=True)
Lt = (L0 - pay / r_) * sp.exp(r_ * t) + pay / r_
check("l3_payoff_time", sp.simplify(Lt.subs(t, sp.log(pay / (pay - r_ * L0)) / r_)) == 0 and close(math.log(2) / 0.06, 11.55, 0.005))
check("l3_perpetuity", sp.solve(sp.Rational(4, 100) * y - 5, y) == [125]
      and solves(125 + 5 * sp.exp(t / 25), lambda s, v: v / 25 - 5) and solves(125 - 5 * sp.exp(t / 25), lambda s, v: v / 25 - 5))
check("l3_quiz", solves(sp.exp(t) / 4 + C * sp.exp(-3 * t), lambda s, v: sp.exp(s) - 3 * v) and solves(sp.exp(-t**2), lambda s, v: -2 * s * v))

# ---------------------------------------------------------------- l4
check("l4_line_family", solves(t - 1 + C * sp.exp(-t), lambda s, v: s - v))
f1 = (y - 1) * (y - 3)
check("l4_equilibria_and_test", set(sp.solve(f1, y)) == {1, 3} and sp.diff(f1, y).subs(y, 1) == -2 and sp.diff(f1, y).subs(y, 3) == 2)
sol = solve_ivp(lambda s, v: (v - 1) * (v - 3), [0, 5], [2.9], rtol=1e-11, atol=1e-13)
cexp = (-0.1 / 1.9) * math.exp(10)
check("l4_y5_from_2_9", close(sol.y[0, -1], 1.0017, 5e-5) and close((3 - cexp) / (1 - cexp), 1.0017, 5e-5))
check("l4_logistic_fprime", sp.diff(sp.Rational(8, 10) * y * (1 - y / 10000), y).subs(y, 10000) == sp.Rational(-8, 10))
fq = y * (1 - y) * (y - sp.Rational(3, 10))
check("l4_tipping", [sp.diff(fq, y).subs(y, v) for v in (0, 1, sp.Rational(3, 10))] == [sp.Rational(-3, 10), sp.Rational(-7, 10), sp.Rational(21, 100)])
check("l4_roots_code", sorted(np.round(np.roots([-1, 1.3, -0.3, 0]).real, 6).tolist()) == [0.0, 0.3, 1.0])
check("l4_quiz_cubic", [sp.diff(y**3 - y, y).subs(y, v) for v in (-1, 0, 1)] == [2, -1, 2])


def flow(f, start, T_end):
    s = solve_ivp(lambda s_, v: f(v), [0, T_end], [start], rtol=1e-10, atol=1e-12)
    return s.y[0, -1]


# semi-stable y' = (y - 2)^2: attracts from below, repels above
below, above = flow(lambda v: (v - 2) ** 2, 1.9, 200), flow(lambda v: (v - 2) ** 2, 2.01, 99)
check("l4_semi_stable_behaviour", 1.99 < below < 2 and above > 2.5)
# Lyapunov: stable means starts within delta stay within epsilon. Starts above 2 leave any
# small band however close they begin, so y = 2 is unstable in the standard sense
# (Boyce and DiPrima sec. 9.2; the course's own l12 screens[7] uses this sense of stable).
leaves = all(flow(lambda v: (v - 2) ** 2, 2 + d, 1 / d - 2.0) > 2.4 for d in (1e-1, 1e-2, 1e-3))
check("l4_semi_stable_is_lyapunov_unstable", leaves)
expected_fail("l4_quiz0_option_unstable_is_wrong", not leaves,
              "quiz[0] marks 'It is unstable' wrong, yet y = 2 is not Lyapunov stable; corrected assert: assert leaves")
hw = solve_ivp(lambda s, v: v**2 * (1 - v), [0, 2000], [-0.5], rtol=1e-10, atol=1e-13)
check("l4_hw_semi_from_below", -0.01 < hw.y[0, -1] < 0 and np.all(np.diff(hw.y[0]) > 0))
check("l4_hw_phase", [sp.diff(y * (y - 1) * (y - 3), y).subs(y, v) for v in (0, 1, 3)] == [3, -2, 6])

# ---------------------------------------------------------------- l5
kap, th, r0 = sp.symbols("kappa theta r0", positive=True)
rv = th + (r0 - th) * sp.exp(-kap * t)
check("l5_solution", solves(rv, lambda s, v: kap * (th - v)) and rv.subs(t, 0) == r0)
check("l5_half_life", sp.simplify((rv.subs(t, sp.log(2) / kap) - th) / (r0 - th)) == sp.Rational(1, 2))
check("l5_half_life_values", close(math.log(2) / 0.5, 1.3863, 5e-5) and close(math.log(2) / 2, 0.3466, 5e-5))
Tt = sp.symbols("T", positive=True)
avg = sp.integrate(rv, (t, 0, Tt)) / Tt
check("l5_average_formula", sp.simplify(avg - (th + (r0 - th) * (1 - sp.exp(-kap * Tt)) / (kap * Tt))) == 0)
check("l5_average_value", close(0.04 + 0.02 * (1 - math.exp(-2.5)) / 2.5, 0.047343, 5e-7))
phi = math.exp(-0.5 / 252)
check("l5_phi", close(phi, 0.998018, 5e-7) and close(phi**252, math.exp(-0.5), 1e-12))
# Monte Carlo: mean-zero shocks do not move the mean of a linear drift
rng = np.random.default_rng(20261110)
paths = np.full(200000, 0.06)
for _ in range(252):
    paths = 0.04 + phi * (paths - 0.04) + 0.0006 * rng.standard_normal(paths.size)
se = paths.std() / math.sqrt(paths.size)
check("l5_vasicek_mean_is_ode", abs(paths.mean() - 0.052131) < 4 * se and abs(0.06 - 0.052131) > 100 * se, f"mean {paths.mean():.6f} se {se:.2e}")
check("l5_wrong_sign_runs_away", solves(sp.Rational(4, 100) + sp.Rational(2, 100) * sp.exp(t / 2), lambda s, v: (v - sp.Rational(4, 100)) / 2)
      and close(0.04 + 0.02 * 2, 0.08, 1e-12))
check("l5_two_half_lives", close(math.log(4) / 0.5, 2.7726, 5e-5) and close(0.04 + 0.02 / 4, 0.045, 1e-12))
check("l5_calibration", close(math.log(3) / 2, 0.5493, 5e-5) and close(math.log(2) / (math.log(3) / 2), 1.26, 0.005))
check("l5_negative_kappa_doubling", close(math.log(2) / 0.2, 3.47, 0.005))
check("l5_trading_days", close(0.3466 * 252, 87, 0.5) and close(math.log(2) / 1.5 * 252, 116, 0.5))

# ---------------------------------------------------------------- review-1, homework-1
check("r1_sep", solves(2 * sp.exp(t**3), lambda s, v: 3 * s**2 * v) and close(2 * math.e, 5.4366, 5e-5))
check("r1_if", solves(2 * (1 - sp.exp(-t)), lambda s, v: 2 - v) and close(2 * (1 - math.exp(-1)), 1.2642, 5e-5))
check("r1_stab", sp.diff(y**2 - y - 2, y).subs(y, -1) == -3 and sp.diff(y**2 - y - 2, y).subs(y, 2) == 3)
check("r1_logistic_time", close(math.log(3) / 0.5, 2.1972, 5e-5) and close(math.log(3) / 0.25, 4.3944, 5e-5))
check("r1_fund_steady", close(2 / 0.07, 28.6, 0.05))
check("h1_cos", solves(sp.exp(sp.sin(t)), lambda s, v: v * sp.cos(s)))
check("h1_if_t", sp.simplify(t * sp.diff(t**2 + t**-2, t) + 2 * (t**2 + t**-2) - 4 * t**2) == 0 and (t**2 + t**-2).subs(t, 2) == sp.Rational(17, 4))
check("h1_tan", solves(sp.tan(t), lambda s, v: 1 + v**2) and close(math.pi / 2, 1.5708, 5e-5))
check("h1_drawdown", close(math.log(1.6) / 0.03, 15.67, 0.005) and close(8000 / 0.03, 266667, 1))
tg = np.linspace(0, 5, 11)
slope = np.polyfit(tg, np.log(np.abs(0.04 + 0.02 * np.exp(-0.5 * tg) - 0.04)), 1)[0]
check("h1_fit_kappa", close(-slope, 0.5, 1e-9))

print(f"odes L1 concepts r2: {COUNT[0]} checks, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL")
sys.exit(1 if FAILS else 0)
