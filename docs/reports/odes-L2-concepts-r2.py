#!/usr/bin/env python3
"""Round-2 concept checks for odes level 2 (l6 to l9, review-2, homework-2).

Independent of docs/reports/odes-L2-concepts.py (not opened while writing this).
Exit 0 when every ordinary check passes. EXPECTED_FAIL marks a check that fails
because the content is wrong or imprecise; the corrected assert is in a comment.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

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


t, c1, c2, r, A, B, w = sp.symbols("t c1 c2 r A B omega")


def L(expr, p, q):
    """y'' + p y' + q y for the expression."""
    return sp.simplify(sp.diff(expr, t, 2) + p * sp.diff(expr, t) + q * expr)


# ---------------------------------------------------------------- l6
gen = c1 * sp.cos(t) + c2 * sp.sin(t)
check("l6_spring_general", L(gen, 0, 1) == 0 and gen.subs(t, 0) == c1 and sp.diff(gen, t).subs(t, 0) == c2)
yf = sp.Function("y")
ds = sp.dsolve(yf(t).diff(t, 2) + yf(t), yf(t)).rhs
check("l6_every_solution_has_that_form", sp.simplify(sp.diff(ds, t, 2) + ds) == 0 and len(ds.free_symbols - {t}) == 2)
check("l6_target", (sp.cos(t) + 2 * sp.sin(t)).subs(t, sp.pi / 2) == 2 and (sp.cos(t) + 2 * sp.sin(t)).subs(t, sp.pi) == -1)
check("l6_substitution", [sp.simplify(L(sp.exp(k_ * t), -3, 2) / sp.exp(k_ * t)) for k_ in (1, 2, 3, -1)] == [0, 0, 2, 6])
check("l6_superposition", L(c1 * sp.exp(t) + c2 * sp.exp(2 * t), -3, 2) == 0)
s_ = sp.solve([c1 + c2, c1 + 2 * c2 - 1], [c1, c2])
check("l6_fit", s_[c1] == -1 and s_[c2] == 1)
# boundary value problems: many, or none
check("l6_bvp_many", sp.solve([gen.subs(t, 0), gen.subs(t, sp.pi)], [c1, c2], dict=True) == [{c1: 0}])
check("l6_bvp_none", sp.solve([gen.subs(t, 0), gen.subs(t, sp.pi) - 1], [c1, c2], dict=True) == [])
y1, y2 = sp.exp(t), sp.exp(2 * t)
W = sp.simplify(y1 * sp.diff(y2, t) - sp.diff(y1, t) * y2)
check("l6_wronskian", W.subs(t, 0) == 1 and sp.simplify(W - sp.exp(3 * t)) == 0)
p, q = sp.symbols("p q")
Acomp = sp.Matrix([[0, 1], [-q, -p]])
lam = sp.symbols("lambda")
check("l6_companion_charpoly", sp.expand(Acomp.charpoly(lam).as_expr() - (lam**2 + p * lam + q)) == 0)
inv_a = 1000 * sp.exp(-t / 2) * (sp.cos(t) + sp.sin(t) / 2)
inv_b = sp.exp(-t / 2) * (1000 * sp.cos(t) + 900 * sp.sin(t))
check("l6_inventory_curves", L(inv_a, 1, sp.Rational(5, 4)) == 0 and L(inv_b, 1, sp.Rational(5, 4)) == 0
      and sp.diff(inv_a, t).subs(t, 0) == 0 and sp.diff(inv_b, t).subs(t, 0) == 400 and inv_a.subs(t, 0) == inv_b.subs(t, 0) == 1000)
ya, yb = 1 + sp.cos(t), 1 + sp.sin(t)
check("l6_forced_sum_and_difference", L(ya + yb, 0, 1) == 2 and L(ya - yb, 0, 1) == 0)

# ---------------------------------------------------------------- l7
check("l7_exponential_trial", sp.factor(sp.simplify(L(sp.exp(r * t), -3, 2) / sp.exp(r * t))) == (r - 1) * (r - 2))
check("l7_y1", close(math.e**2 - math.e, 4.6708, 5e-5))
rep = (c1 + c2 * t) * sp.exp(-2 * t)
check("l7_repeated_root", L(rep, 4, 4) == 0 and L(t * sp.exp(-2 * t), 4, 4) == 0)
sr = sp.solve([rep.subs(t, 0) - 1, sp.diff(rep, t).subs(t, 0)], [c1, c2])
check("l7_repeated_fit", sr[c1] == 1 and sr[c2] == 2 and close(3 * math.exp(-2), 0.4060, 5e-5))
check("l7_te_rt_needs_double_root", L(t * sp.exp(-2 * t), 5, 6) != 0)  # -2 is a single root of r^2 + 5r + 6
check("l7_te_derivatives", sp.simplify(sp.diff(t * sp.exp(-2 * t), t) - (1 - 2 * t) * sp.exp(-2 * t)) == 0
      and sp.simplify(sp.diff(t * sp.exp(-2 * t), t, 2) - (4 * t - 4) * sp.exp(-2 * t)) == 0)
check("l7_complex_roots", set(sp.solve(r**2 + 2 * r + 5, r)) == {-1 + 2 * sp.I, -1 - 2 * sp.I})
cx = sp.exp(-t) * (c1 * sp.cos(2 * t) + c2 * sp.sin(2 * t))
check("l7_complex_solution", L(cx, 2, 5) == 0 and sp.simplify(sp.diff(cx, t).subs(t, 0) - (-c1 + 2 * c2)) == 0)
z = sp.exp((-1 + 2 * sp.I) * t)
re_part, im_part = sp.exp(-t) * sp.cos(2 * t), sp.exp(-t) * sp.sin(2 * t)
check("l7_real_and_imag_parts_solve", sp.simplify((z - (re_part + sp.I * im_part)).rewrite(sp.cos)) == 0
      and L(re_part, 2, 5) == 0 and L(im_part, 2, 5) == 0 and sp.simplify(sp.diff(z, t) - (-1 + 2 * sp.I) * z) == 0)
yw = lambda s: math.exp(-s) * (math.cos(2 * s) + 0.5 * math.sin(2 * s))
check("l7_wave_value", close(yw(1), 0.014164, 5e-7))
grid = np.linspace(0, 12, 240001)
env = np.abs(np.cos(2 * grid) + 0.5 * np.sin(2 * grid))
check("l7_envelope_is_sqrt_sum_squares", close(env.max(), math.sqrt(5) / 2, 1e-8) and close(math.hypot(1, 0.5), 1.118034, 5e-7))
bs = np.linspace(0, 3.99, 400)
roots = [np.roots([1, b_, 4]) for b_ in bs]
check("l7_roots_on_circle", all(np.allclose(np.abs(rt), 2) for rt in roots) and np.allclose(np.roots([1, 4, 4]), [-2, -2]))
check("l7_one_constant", sp.solve([(c1 + c2) - 1, -2 * (c1 + c2)], [c1, c2], dict=True) == [])
# all three branches of the solver against a numerical solve
for name, (a_, b_, c_, y0, v0), expect in [("two_real", (1, -3, 2, 0, 1), 4.670774), ("double", (1, 4, 4, 1, 0), 0.406006),
                                           ("complex", (1, 2, 5, 1, 0), 0.014164), ("zero_root", (1, 1, 0, 3, -2), 1.270671)]:
    s = solve_ivp(lambda s_, v: [v[1], -(b_ * v[1] + c_ * v[0]) / a_], [0, 2 if name == "zero_root" else 1], [y0, v0], rtol=1e-11, atol=1e-13)
    check("l7_solver_" + name, close(s.y[0, -1], expect, 2e-6))
# perpetual put
S, m, sig, rf, Kk = sp.symbols("S m sigma r K", positive=True)
ode = lambda V: sp.Rational(1, 2) * sig**2 * S**2 * sp.diff(V, S, 2) + rf * S * sp.diff(V, S) - rf * V
check("l7_put_power_trial", sp.simplify(ode(S**m) / S**m - (sp.Rational(1, 2) * sig**2 * m * (m - 1) + rf * m - rf)) == 0)
check("l7_put_roots", set(sp.solve(sp.Rational(2, 100) * m * (m - 1) + sp.Rational(5, 100) * m - sp.Rational(5, 100), m)) == {1}
      or set(sp.solve(sp.Rational(2, 100) * r * (r - 1) + sp.Rational(5, 100) * r - sp.Rational(5, 100), r)) == {1, sp.Rational(-5, 2)})
Sst = sp.Rational(100 * 25, 35)
V = (100 - Sst) * (S / Sst) ** sp.Rational(-5, 2)
check("l7_put_value_matching_and_smooth_pasting", V.subs(S, Sst) == 100 - Sst and sp.diff(V, S).subs(S, Sst) == -1)
check("l7_put_numbers", close(Sst, 71.43, 0.005) and close(V.subs(S, 100), 12.32, 0.005) and sp.limit(V, S, sp.oo) == 0)
check("l7_zero_root", L(c1 + c2 * sp.exp(-t), 1, 0) == 0)

# ---------------------------------------------------------------- l8
check("l8_constant_particular", L(sp.Integer(2), 3, 2) == 4)
check("l8_general_forced", L(c1 * sp.exp(-t) + c2 * sp.exp(-2 * t) + 2, 3, 2) == 4)
check("l8_exponential_forcing", sp.simplify(L(sp.exp(3 * t) / 20, 3, 2) - sp.exp(3 * t)) == 0)
yp = -3 * sp.cos(t) + sp.sin(t)
check("l8_sinusoid", sp.simplify(L(yp, 3, 2) - 10 * sp.sin(t)) == 0)
full = 5 * sp.exp(-t) - 2 * sp.exp(-2 * t) + yp
check("l8_ivp", sp.simplify(L(full, 3, 2) - 10 * sp.sin(t)) == 0 and full.subs(t, 0) == 0 and sp.diff(full, t).subs(t, 0) == 0
      and close(full.subs(t, 1), 0.7893, 5e-5))
check("l8_fit_too_early_starts_at_minus_3", yp.subs(t, 0) == -3 and sp.diff(yp, t).subs(t, 0) == 1)
check("l8_plain_guess_fails", L(A * sp.exp(-t), 3, 2) == 0)
check("l8_t_times_guess", sp.simplify(L(t * sp.exp(-t), 3, 2) - sp.exp(-t)) == 0)
pp_, qq_ = sp.symbols("p q")
guess = A * sp.cos(w * t) + B * sp.sin(w * t)
resid = sp.expand(L(guess, pp_, qq_))
M = sp.Matrix([[resid.coeff(sp.cos(w * t)).coeff(A), resid.coeff(sp.cos(w * t)).coeff(B)],
               [resid.coeff(sp.sin(w * t)).coeff(A), resid.coeff(sp.sin(w * t)).coeff(B)]])
check("l8_matrix", sp.simplify(M - sp.Matrix([[qq_ - w**2, pp_ * w], [-pp_ * w, qq_ - w**2]])) == sp.zeros(2, 2)
      and sp.simplify(M.det() - ((qq_ - w**2) ** 2 + pp_**2 * w**2)) == 0)
check("l8_undamped_resonant_guess_fails", L(A * sp.cos(2 * t) + B * sp.sin(2 * t), 0, 4) == 0)
check("l8_ramp", sp.simplify(L(t - sp.Rational(3, 2), 3, 2) - 2 * t) == 0)
# modification rule: t^2 at a double root; t for a polynomial when 0 is a root
check("l8_double_root_needs_t2", L(A * t * sp.exp(-2 * t), 4, 4) == 0 and sp.simplify(L(t**2 * sp.exp(-2 * t) / 2, 4, 4) - sp.exp(-2 * t)) == 0)
check("l8_polynomial_with_zero_root", sp.simplify(L(t**2 - 2 * t, 1, 0) - 2 * t) == 0 and sp.diff(L(A * t + B, 1, 0), t) == 0)
# "multiply the whole guess by t" fails when the forcing has two parts and only one clashes:
# y'' + 3y' + 2y = e^{-t} + e^{3t}, guess t (A e^{-t} + B e^{3t}).
whole = sp.expand(L(t * (A * sp.exp(-t) + B * sp.exp(3 * t)), 3, 2) - sp.exp(-t) - sp.exp(3 * t))
whole_ok = sp.solve([whole.coeff(sp.exp(-t)), whole.coeff(sp.exp(3 * t)).coeff(t, 0), whole.coeff(sp.exp(3 * t)).coeff(t, 1)], [A, B], dict=True) != []
part = sp.simplify(L(t * sp.exp(-t) + sp.exp(3 * t) / 20, 3, 2) - sp.exp(-t) - sp.exp(3 * t))
check("l8_multiply_only_the_clashing_part", part == 0)
expected_fail("l8_whole_guess_times_t_for_mixed_forcing", whole_ok,
              "screens[8]: 'multiply the whole guess by t' has no solution for e^{-t} + e^{3t}; corrected assert: assert part == 0 (multiply only the clashing part)")
# smoother lag
zeta, om = sp.symbols("zeta omega", positive=True)
c_ = sp.symbols("c")
lagc = sp.solve(sp.simplify(sp.diff(100 + t + c_, t, 2) + 2 * zeta * om * sp.diff(100 + t + c_, t) + om**2 * (100 + t + c_) - om**2 * (100 + t)), c_)
check("l8_lag", lagc == [-2 * zeta / om] and close(2 * 1 / 0.5, 4, 1e-12))
exact = lambda s: 96 + s + (4 + s) * math.exp(-0.5 * s)
check("l8_smoother_chart", close(exact(1), 100.03, 0.006) and close(exact(5), 101.74, 0.006) and close(exact(20), 116.0, 0.006))
# feedback.correct of the transfer screen prints 2 zeta w + w^2 (t + c) = w^2 (100 + t): not an identity for any c
printed = sp.simplify(2 * zeta * om + om**2 * (t + c_) - om**2 * (100 + t))
expected_fail("l8_lag_feedback_equation_as_printed", sp.solve(printed, c_) == [-2 * zeta / om],
              "screens[10].feedback.correct drops the 100 on the left; corrected: 2*zeta*w + w^2*(100 + t + c) = w^2*(100 + t)")
check("l8_quiz", sp.simplify(L(sp.exp(2 * t) / 6, 1, 0) - sp.exp(2 * t)) == 0 and sp.simplify(L(t * sp.exp(t) / 2, 0, -1) - sp.exp(t)) == 0)
check("l8_t2_guess_fails_at_single_root", sp.solve(sp.Poly(sp.simplify((L(A * t**2 * sp.exp(t), 0, -1) - sp.exp(t)) / sp.exp(t)), t).coeffs(), A) == [])

# ---------------------------------------------------------------- l9


def free(b_, s):
    """y(s) for y'' + b y' + 4y = 0 from y(0) = 1 at rest (closed forms)."""
    s = np.asarray(s, dtype=float)
    if abs(b_ - 4) < 1e-12:
        return (1 + 2 * s) * np.exp(-2 * s)
    if b_ < 4:
        wd = math.sqrt(4 - b_ * b_ / 4)
        return np.exp(-b_ * s / 2) * (np.cos(wd * s) + (b_ / 2) / wd * np.sin(wd * s))
    k_ = math.sqrt(b_ * b_ / 4 - 4)
    r1, r2 = -b_ / 2 + k_, -b_ / 2 - k_
    return (r2 * np.exp(r1 * s) - r1 * np.exp(r2 * s)) / (r2 - r1)


fine = np.linspace(0, 40, 400001)
for b_ in (0.5, 1, 2, 3, 3.9, 4, 4.1, 5, 6, 8):
    num = solve_ivp(lambda s_, v: [v[1], -b_ * v[1] - 4 * v[0]], [0, 3], [1, 0], rtol=1e-11, atol=1e-13).y[0, -1]
    check(f"l9_closed_form_b{b_}", close(free(b_, 3.0), num, 1e-7))
    check(f"l9_crosses_zero_only_if_under_b{b_}", (free(b_, fine).min() < 0) == (b_ < 4))
check("l9_zeta", close(1 / (2 * 2), 0.25, 1e-12))
wd1 = math.sqrt(3.75)
check("l9_root_and_envelope", close(wd1, 1.9365, 5e-5) and close(math.hypot(1, 0.5 / wd1), 1.0328, 5e-5)
      and close(np.abs(free(1, fine) * np.exp(0.5 * fine)).max(), 1.032796, 1e-5))
check("l9_period_and_decay", close(2 * math.pi / wd1, 3.2446, 5e-5) and close(math.exp(-0.5 * 2 * math.pi / wd1), 0.197, 5e-4))


def settle(b_, band=0.05):
    yv = np.abs(free(b_, fine))
    last = np.nonzero(yv >= band)[0][-1]
    return fine[last + 1]


check("l9_settling_table", all(close(settle(b_), v, 0.006) for b_, v in [(1, 5.39), (3, 1.56), (4, 2.37), (5, 3.28), (8, 5.73)]),
      str([round(settle(b_), 3) for b_ in (1, 3, 4, 5, 8)]))
check("l9_b3_first_undershoot", close(free(3, fine).min(), -0.028, 6e-4))
check("l9_critical_fastest_without_overshoot", all(settle(4) < settle(b_) for b_ in np.linspace(4.05, 12, 60)))


def step(z_, w_, s):
    s = np.asarray(s, dtype=float)
    wd = w_ * math.sqrt(1 - z_ * z_)
    return 1 - np.exp(-z_ * w_ * s) * (np.cos(wd * s) + z_ / math.sqrt(1 - z_ * z_) * np.sin(wd * s))


for z_, pct in [(0.25, 0.4443), (0.5, 0.1630), (0.75, 0.0284)]:
    check(f"l9_overshoot_formula_zeta{z_}", close(step(z_, 2, fine).max() - 1, math.exp(-z_ * math.pi / math.sqrt(1 - z_ * z_)), 1e-6)
          and close(math.exp(-z_ * math.pi / math.sqrt(1 - z_ * z_)), pct, 5e-5))
check("l9_peak_time", close(fine[np.argmax(step(0.25, 2, fine))], math.pi / wd1, 2e-4) and close(math.pi / wd1, 1.62, 0.005))
y5 = (4 * sp.exp(-t) - sp.exp(-4 * t)) / 3
check("l9_b5_solution", L(y5, 5, 4) == 0 and y5.subs(t, 0) == 1 and sp.diff(y5, t).subs(t, 0) == 0)
yr = t / 4 * sp.sin(2 * t)
check("l9_resonance", sp.simplify(L(yr, 0, 4) - sp.cos(2 * t)) == 0
      and sp.simplify(sp.diff(yr, t) - (sp.sin(2 * t) / 4 + t / 2 * sp.cos(2 * t))) == 0)
# steady amplitude from undetermined coefficients, then its peak
bb, w0 = sp.symbols("b omega0", positive=True)
sol = sp.solve(sp.Matrix([[w0**2 - w**2, bb * w], [-bb * w, w0**2 - w**2]]) * sp.Matrix([A, B]) - sp.Matrix([1, 0]), [A, B])
amp2 = sp.simplify(sol[A] ** 2 + sol[B] ** 2)
check("l9_amplitude_formula", sp.simplify(amp2 - 1 / ((w0**2 - w**2) ** 2 + bb**2 * w**2)) == 0)
ampf = lambda w_, b_=1.0, w0_=2.0: 1 / math.sqrt((w0_**2 - w_**2) ** 2 + (b_ * w_) ** 2)
pk = minimize_scalar(lambda w_: -ampf(w_), bounds=(0.1, 4), method="bounded", options={"xatol": 1e-10})
check("l9_damped_peak_below_natural", close(pk.x, 2 * math.sqrt(1 - 2 * 0.25**2), 1e-5) and close(pk.x, 1.8708, 5e-5)
      and close(-pk.fun, 0.5164, 5e-5) and pk.x < 2 and ampf(2.0) < -pk.fun)
check("l9_amplitude_values", close(ampf(0), 0.25) and close(ampf(1), 0.3162, 5e-5) and close(ampf(2), 0.5))
# forced response simulated: steady amplitude at w = 1.8708 really is 0.5164
wp = 2 * math.sqrt(0.875)
sim = solve_ivp(lambda s_, v: [v[1], math.cos(wp * s_) - v[1] - 4 * v[0]], [0, 80], [0, 0], rtol=1e-10, atol=1e-12, dense_output=True)
check("l9_simulated_steady_amplitude", close(np.abs(sim.sol(np.linspace(60, 80, 40001))[0]).max(), 0.5164, 2e-4))
# the float example on screens[9]: 0.2**2 - 4*0.1*0.1 is exactly 0.0 (0.4 and 0.1 are 2 x and half of the
# same double 0.2, so both products are the same real number before rounding)
printed_value = 0.2**2 - 4 * 0.1 * 0.1
expected_fail("l9_float_example_not_exactly_zero", printed_value != 0.0,
              "screens[9] says 0.2**2 - 4*0.1*0.1 is not exactly 0 and prints 6.938893903907228e-18; it is 0.0. "
              "corrected assert: assert 0.2**2 - 4*0.5*0.02 == 6.938893903907228e-18")
check("l9_float_example_corrected", 0.2**2 - 4 * 0.5 * 0.02 == 6.938893903907228e-18 and 0.2 * 0.2 - 4 * 0.5 * 0.02 == 6.938893903907228e-18)
check("l9_hidden_test_does_not_need_the_tolerance", 0.2 * 0.2 - 4 * 0.1 * 0.1 == 0.0)
check("l9_negative_damping", close(math.sqrt(4 - 0.0625), math.sqrt(3.9375), 1e-12) and np.allclose(np.roots([1, -0.5, 4]).real, 0.25))
check("l9_quiz_classify", np.allclose(sorted(np.roots([1, 2, 10]), key=lambda v: v.imag), [-1 - 3j, -1 + 3j]))

# ---------------------------------------------------------------- review-2, homework-2
check("r2_roots", set(sp.solve(r**2 - r - 6, r)) == {3, -2} and set(sp.solve(r**2 + 2 * r + 2, r)) == {-1 + sp.I, -1 - sp.I})
check("r2_ramp", sp.simplify(L(-2 * t - 1, 1, -2) - 4 * t) == 0)
check("r2_resonant", sp.simplify(L(-t / 6 * sp.cos(3 * t), 0, 9) - sp.sin(3 * t)) == 0 and L(A * sp.cos(3 * t) + B * sp.sin(3 * t), 0, 9) == 0)
check("r2_critical_and_cosh", sp.solve(r**2 - 36, r) == [-6, 6] and close(math.cosh(2), 3.7622, 5e-5) and L(sp.cosh(2 * t), 0, -4) == 0)
for z_, w_, at, expect in [(0.25, 2, 1, 1.070645), (0.5, 1, 2, 0.849426)]:
    num = solve_ivp(lambda s_, v: [v[1], w_ * w_ - 2 * z_ * w_ * v[1] - w_ * w_ * v[0]], [0, at], [0, 0], rtol=1e-11, atol=1e-13).y[0, -1]
    check(f"h2_step_response_{z_}", close(step(z_, w_, at), expect, 1e-6) and close(num, expect, 1e-6))
for z_, w_, at, expect in [(1, 2, 1, 0.593994), (1.25, 2, 1, 0.515599), (3, 1, 40, 0.998922)]:
    num = solve_ivp(lambda s_, v: [v[1], w_ * w_ - 2 * z_ * w_ * v[1] - w_ * w_ * v[0]], [0, at], [0, 0], rtol=1e-11, atol=1e-13).y[0, -1]
    check(f"h2_step_response_{z_}", close(num, expect, 2e-6))
rr = sp.symbols("rr")
check("h2_repeated_general", sp.simplify(sp.diff(t * sp.exp(rr * t), t, 2) - 2 * rr * sp.diff(t * sp.exp(rr * t), t) + rr**2 * t * sp.exp(rr * t)) == 0)
check("h2_ivp", L(sp.exp(-t) * sp.sin(t), 2, 2) == 0 and close(math.exp(-math.pi / 2), 0.2079, 5e-5))
check("h2_resonant_exp", sp.simplify(L(-t * sp.exp(t), -3, 2) - sp.exp(t)) == 0)
pk2 = minimize_scalar(lambda w_: -ampf(w_, 0.4), bounds=(0.1, 4), method="bounded", options={"xatol": 1e-10})
check("h2_peak", close(pk2.x, 1.9799, 5e-5) and close(-pk2.fun, 1.2563, 5e-5) and close(ampf(2, 0.4), 1.25))
check("h2_slow_root", np.allclose(sorted(np.roots([1, 8.5, 4])), [-8, -0.5]))
check("h2_longform", close(math.pi / (0.5 * math.sqrt(1 - 0.0625)), 6.49, 0.005) and close(2 * 0.25 / 0.5, 1) and close(2 * 1 / 0.5, 4))

print(f"odes L2 concepts r2: {COUNT[0]} checks, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL")
sys.exit(1 if FAILS else 0)
