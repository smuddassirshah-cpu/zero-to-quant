#!/usr/bin/env python3
"""Concept audit round 3, odes level 2 (l6 to l9, review-2, homework-2).

Independent sympy and numerical checks of the claims in the ledger
(docs/reports/audit-odes-1-3-r3-ledger.md). Exit 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

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


t = sp.Symbol("t", real=True)
y = sp.Function("y")
c1, c2 = sp.symbols("c1 c2")


def L(expr, a, b, c):
    return sp.simplify(a * sp.diff(expr, t, 2) + b * sp.diff(expr, t) + c * expr)


# ---- l6: second order -------------------------------------------------------
check("spring_family", L(c1 * sp.cos(t) + c2 * sp.sin(t), 1, 0, 1) == 0)
check("wronskian_e^t_e^2t", sp.simplify(sp.wronskian([sp.exp(t), sp.exp(2 * t)], t)).subs(t, 0) == 1)
# Abel: for solutions the Wronskian is never 0 or always 0, so "W != 0" needs no "at which t"
W = sp.simplify(sp.wronskian([sp.exp(t), sp.exp(2 * t)], t))
check("wronskian_never_zero_for_solutions", sp.solve(W, t) == [])
# two independent solutions give EVERY solution: needs existence and uniqueness, not superposition alone
sol = sp.dsolve(sp.Eq(y(t).diff(t, 2) - 3 * y(t).diff(t) + 2 * y(t), 0), y(t), ics={y(0): 0, y(t).diff(t).subs(t, 0): 1}).rhs
check("ivp_fits_c1=-1_c2=1", sp.simplify(sol - (sp.exp(2 * t) - sp.exp(t))) == 0)
# boundary value problems: y'' + y = 0, y(0) = 0: y = c sin t; y(pi) = 0 for every c, y(pi) = 1 for none
check("bvp_many_or_none", sp.sin(sp.pi) == 0 and sp.solve(sp.Eq(c2 * sp.sin(sp.pi), 1), c2) == [])
check("sum_of_forced_solutions_doubles_rhs", L((1 + sp.cos(t)) + (1 + sp.sin(t)), 1, 0, 1) == 2)
x1 = 1000 * sp.exp(-t / 2) * (sp.cos(t) + sp.sin(t) / 2)
x2 = sp.exp(-t / 2) * (1000 * sp.cos(t) + 900 * sp.sin(t))
check("inventory_curves", L(x1, 1, 1, sp.Rational(5, 4)) == 0 and L(x2, 1, 1, sp.Rational(5, 4)) == 0
      and sp.diff(x1, t).subs(t, 0) == 0 and sp.diff(x2, t).subs(t, 0) == 400)

# ---- l7: characteristic equation -------------------------------------------
check("double_root_t_e^-2t", L(t * sp.exp(-2 * t), 1, 4, 4) == 0 and L(t * sp.exp(-2 * t), 1, 3, 2) != 0)
r = sp.Symbol("r")
check("te^rt_needs_double_root", L(t * sp.exp(r * t), 1, -2 * r, r ** 2) == 0)
yc = sp.exp(-t) * (sp.cos(2 * t) + sp.sin(2 * t) / 2)
check("complex_roots_fit", L(yc, 1, 2, 5) == 0 and yc.subs(t, 0) == 1 and sp.diff(yc, t).subs(t, 0) == 0
      and abs(float(yc.subs(t, 1)) - 0.014164) < 5e-7)
tt = np.linspace(0, 6, 60001)
yv = np.exp(-tt) * (np.cos(2 * tt) + 0.5 * np.sin(2 * tt))
check("envelope_sqrt5/2", np.all(np.abs(yv) <= math.sqrt(5) / 2 * np.exp(-tt) + 1e-12)
      and np.max(np.abs(yv) / np.exp(-tt)) > math.sqrt(5) / 2 - 1e-6)
check("roots_of_r^2+br+4_on_circle_2", all(abs(abs(z) - 2) < 1e-12 for b in (0.5, 1, 3) for z in np.roots([1, b, 4])))
# perpetual put
S, sig, rr, Kk, m = sp.symbols("S sigma r K m", positive=True)
ode = lambda V: sp.simplify(sig ** 2 * S ** 2 * sp.diff(V, S, 2) / 2 + rr * S * sp.diff(V, S) - rr * V)
gam = 2 * rr / sig ** 2
check("put_power_solutions", ode(S) == 0 and ode(S ** (-gam)) == 0)
Sst = Kk * gam / (1 + gam)
V = (Kk - Sst) * (S / Sst) ** (-gam)
check("put_smooth_pasting", sp.simplify(V.subs(S, Sst) - (Kk - Sst)) == 0 and sp.simplify(sp.diff(V, S).subs(S, Sst) + 1) == 0)
num = {rr: 0.05, sig: 0.2, Kk: 100}
check("put_numbers", abs(float(gam.subs(num)) - 2.5) < 1e-12 and abs(float(Sst.subs(num)) - 71.43) < 0.005
      and abs(float(V.subs(num).subs(S, 100)) - 12.32) < 0.005)
# l7 screens[9].prose says the value V(S) obeys the equation, with no region. Below S* the value is K - S.
check("FINDING_4 put_value_obeys_the_ODE_at_every_S (l7 screens[9].prose)", ode(Kk - S) == 0, expected_fail=True)
# corrected assert: assert ode(Kk - S) == -rr * Kk   (the equation holds only for S above S*)

# ---- l8: forcing ------------------------------------------------------------
check("yp_sin_forcing", L(-3 * sp.cos(t) + sp.sin(t), 1, 3, 2) == 10 * sp.sin(t))
full = 5 * sp.exp(-t) - 2 * sp.exp(-2 * t) - 3 * sp.cos(t) + sp.sin(t)
check("full_ivp", sp.simplify(L(full, 1, 3, 2) - 10 * sp.sin(t)) == 0 and full.subs(t, 0) == 0 and sp.diff(full, t).subs(t, 0) == 0
      and abs(float(full.subs(t, 1)) - 0.7893) < 5e-5)
check("modification_rule_single_root", sp.simplify(L(t * sp.exp(-t), 1, 3, 2) - sp.exp(-t)) == 0 and L(sp.exp(-t), 1, 3, 2) == 0)
# at a double root t e^{rt} is homogeneous too, so t^2 is needed
check("modification_rule_double_root", L(t * sp.exp(-2 * t), 1, 4, 4) == 0
      and sp.simplify(L(t ** 2 * sp.exp(-2 * t) / 2, 1, 4, 4) - sp.exp(-2 * t)) == 0)
check("quiz_t^2_guess_fails_at_single_root", sp.simplify(L(t ** 2 * sp.exp(t), 1, 0, -1) / sp.exp(t)).has(t)
      and sp.simplify(L(t * sp.exp(t) / 2, 1, 0, -1) - sp.exp(t)) == 0)
p, q, w = sp.symbols("p q omega", real=True)
M = sp.Matrix([[q - w ** 2, p * w], [-p * w, q - w ** 2]])
check("sinusoid_system_det", sp.simplify(M.det() - ((q - w ** 2) ** 2 + p ** 2 * w ** 2)) == 0)
A_, B_ = sp.symbols("A B")
res = sp.expand(sp.diff(A_ * sp.cos(w * t) + B_ * sp.sin(w * t), t, 2) + p * sp.diff(A_ * sp.cos(w * t) + B_ * sp.sin(w * t), t)
                + q * (A_ * sp.cos(w * t) + B_ * sp.sin(w * t)))
check("sinusoid_system_rows", sp.simplify(res.coeff(sp.cos(w * t)) - (M[0, 0] * A_ + M[0, 1] * B_)) == 0
      and sp.simplify(res.coeff(sp.sin(w * t)) - (M[1, 0] * A_ + M[1, 1] * B_)) == 0)
try:
    np.linalg.solve(np.zeros((2, 2)), [0.0, 1.0])
    cpy = "no error"
except np.linalg.LinAlgError:
    cpy = "LinAlgError"
print("NOTE          CPython NumPy on a singular solve:", cpy, "(Pyodide 0.27.7 NumPy 2.0.2 returns array([nan, nan]); run under node, see audit)")
z, om = sp.symbols("zeta omega0", positive=True)
cc = sp.Symbol("c")
lag = sp.solve(sp.Eq(2 * z * om + om ** 2 * (100 + t + cc), om ** 2 * (100 + t)), cc)[0]
check("trend_lag_2zeta/omega", sp.simplify(lag + 2 * z / om) == 0)
ks = np.arange(31)
sm = 96 + ks + (4 + ks) * np.exp(-0.5 * ks)
check("smoother_series_and_gap", abs(sm[1] - 100.03) < 0.005 and abs(sm[9] - 105.14) < 0.005 and abs((100 + 20) - sm[20] - 4.00) < 0.005)

# ---- l9: damping and resonance ---------------------------------------------
def free(b, T=30.0, n=300001):
    tg = np.linspace(0, T, n)
    s = solve_ivp(lambda u, v: [v[1], -b * v[1] - 4 * v[0]], [0, T], [1, 0], t_eval=tg, rtol=1e-11, atol=1e-13)
    return tg, s.y[0]


def settle(b):
    tg, yy = free(b)
    return tg[np.where(np.abs(yy) >= 0.05)[0][-1] + 1]


table = {1: 5.39, 3: 1.56, 4: 2.37, 5: 3.28, 8: 5.73}
check("settling_table", all(abs(settle(b) - v) < 0.006 for b, v in table.items()))
def exact_over(b, tg):
    """Closed form from y(0) = 1 at rest for b >= 4 (solver noise near 0 would hide the sign)."""
    if b == 4:
        return (1 + 2 * tg) * np.exp(-2 * tg)
    ra, rb = sorted(np.roots([1, b, 4]).real)
    return (rb * np.exp(ra * tg) - ra * np.exp(rb * tg)) / (rb - ra)


grid = np.linspace(0, 30, 30001)
check("crosses_zero_only_when_b<4", all(free(b)[1].min() < 0 for b in (0.2, 1, 3, 3.9))
      and all(exact_over(b, grid).min() > 0 for b in (4, 4.1, 5, 8)))
best = minimize_scalar(settle, bounds=(4, 10), method="bounded").x
check("critical_is_fastest_without_overshoot", abs(best - 4) < 0.01)
check("b=3_overshoot_2.8pc", abs(-free(3)[1].min() - 0.028) < 0.0005
      and abs(math.exp(-0.75 * math.pi / math.sqrt(1 - 0.75 ** 2)) - 0.0284) < 5e-5)
wd = math.sqrt(4 - 0.25)
check("ringing_numbers", abs(wd - 1.9365) < 5e-5 and abs(2 * math.pi / wd - 3.2446) < 5e-5
      and abs(math.sqrt(1 + (0.5 / wd) ** 2) - 1.0328) < 5e-5 and abs(math.exp(-0.5 * 2 * math.pi / wd) - 0.197) < 5e-4)
tg = np.linspace(0, 8, 800001)
step = 1 - np.exp(-0.5 * tg) * (np.cos(wd * tg) + 0.5 / wd * np.sin(wd * tg))
check("step_overshoot_formula", abs(step.max() - 1 - math.exp(-0.25 * math.pi / math.sqrt(1 - 0.0625))) < 1e-6
      and abs(tg[step.argmax()] - math.pi / wd) < 1e-4 and abs(step.max() - 1.4443) < 5e-5)
check("resonant_particular", sp.simplify(L(t * sp.sin(2 * t) / 4, 1, 0, 4) - sp.cos(2 * t)) == 0)
check("rev2_resonant_particular", sp.simplify(L(-t * sp.cos(3 * t) / 6, 1, 0, 9) - sp.sin(3 * t)) == 0)
amp = lambda x, b=1.0: 1 / math.sqrt((4 - x * x) ** 2 + (b * x) ** 2)
pk = minimize_scalar(lambda x: -amp(x), bounds=(0.1, 3.9), method="bounded").x
check("damped_peak_frequency", abs(pk - 2 * math.sqrt(1 - 2 * 0.25 ** 2)) < 1e-5 and abs(pk - 1.8708) < 5e-5 and abs(amp(pk) - 0.5164) < 5e-5)
pk2 = minimize_scalar(lambda x: -amp(x, 0.4), bounds=(0.1, 3.9), method="bounded").x
check("hw2_peak", abs(pk2 ** 2 - 3.92) < 1e-4 and abs(amp(pk2, 0.4) - 1.2563) < 5e-5 and abs(amp(2, 0.4) - 1.25) < 1e-12)
# steady amplitude really is the long-run size of the forced response
s = solve_ivp(lambda u, v: [v[1], math.cos(u) - v[1] - 4 * v[0]], [0, 80], [0, 0], t_eval=np.linspace(60, 80, 20001), rtol=1e-10, atol=1e-12)
check("steady_amplitude_simulated", abs(np.abs(s.y[0]).max() - 1 / math.sqrt(10)) < 1e-4)
check("negative_damping_grows", abs(np.roots([1, -0.5, 4])[0].real - 0.25) < 1e-12)
check("float_discriminant", 0.2 ** 2 - 4 * 0.5 * 0.02 == 6.938893903907228e-18)

# ---- homework-2 -------------------------------------------------------------
check("hw2_peak_time_and_lags", abs(math.pi / (0.5 * math.sqrt(1 - 0.0625)) - 6.49) < 0.005 and 2 * 0.25 / 0.5 == 1 and 2 * 1 / 0.5 == 4)
check("hw2_slow_root", sorted(np.roots([1, 8.5, 4]).tolist()) == [-8.0, -0.5])
r1, r2 = sp.symbols("r1 r2", negative=True)
over = 1 + (r2 * sp.exp(r1 * t) - r1 * sp.exp(r2 * t)) / (r1 - r2)
check("hw2_overdamped_step_from_rest", sp.simplify(over.subs(t, 0)) == 0 and sp.simplify(sp.diff(over, t).subs(t, 0)) == 0)

print()
print("expected fails (findings):", len(NOTES))
print("unexpected fails:", len(FAILS))
sys.exit(1 if FAILS else 0)
