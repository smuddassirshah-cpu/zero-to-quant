#!/usr/bin/env python3
"""Concept audit round 3, odes level 1 (l1 to l5, review-1, homework-1).

Independent sympy, numerical and Monte Carlo checks of the claims in the ledger
(docs/reports/audit-odes-1-3-r3-ledger.md). Exit 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

import json as _json
import pathlib as _pl
_ODES = _pl.Path(__file__).resolve().parents[2] / "app" / "content" / "courses" / "odes"
def _txt(f):
    return _json.dumps(_json.load(open(_ODES / f, encoding="utf-8")), ensure_ascii=False)

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


t, y, C, k, K, P0 = sp.symbols("t y C k K P0", positive=True)
a, q, y0 = sp.symbols("a q y0", real=True)

# ---- l1: what a solution is -------------------------------------------------
B = 1000 * sp.exp(sp.Rational(5, 100) * t)
check("exp_solves_B'=0.05B", sp.simplify(sp.diff(B, t) - sp.Rational(5, 100) * B) == 0)
yearly = 1000 * sp.Rational(105, 100) ** t
check("yearly_curve_slope_is_ln1.05_B",
      sp.simplify(sp.diff(yearly, t) / yearly - sp.log(sp.Rational(105, 100))) == 0
      and abs(math.log(1.05) - 0.0488) < 5e-5)
check("line_1+2t_matches_y'=2y_only_at_0",
      sp.solve(sp.Eq(sp.diff(1 + 2 * t, t), 2 * (1 + 2 * sp.Symbol("s"))), sp.Symbol("s")) == [0])
check("compounding_limit", abs(1000 * (1 + 0.05 / 365) ** 365 - 1051.27) < 0.005
      and abs(1000 * (1 + 0.05 / 12) ** 12 - 1051.16) < 0.005
      and sp.limit((1 + sp.Rational(5, 100) / sp.Symbol("n")) ** sp.Symbol("n"), sp.Symbol("n"), sp.oo)
      == sp.exp(sp.Rational(1, 20)))
# uniqueness needs f and df/dy continuous: y' = 3 y^(2/3), y(0) = 0 has two solutions
s = sp.Symbol("s", positive=True)
check("uniqueness_hypothesis_is_needed",
      sp.simplify(sp.diff(s ** 3, s) - 3 * (s ** 3) ** sp.Rational(2, 3)) == 0)  # y = t^3 and y = 0 both solve
check("loan_paid_off_11.55", abs(math.log(2) / 0.06 - 11.5525) < 5e-5)

# ---- l2: separable ----------------------------------------------------------
P = K / (1 + (K - P0) / P0 * sp.exp(-k * t))
check("logistic_closed_form", sp.simplify(sp.diff(P, t) - k * P * (1 - P / K)) == 0
      and sp.simplify(P.subs(t, 0) - P0) == 0)
check("logistic_formula_gives_K_when_P0=K", sp.simplify(P.subs(P0, K) - K) == 0)
check("logistic_formula_cannot_give_P=0", sp.limit(P, P0, 0, "+") == 0 and P.subs(t, 0).has(P0))
Ps = sp.Symbol("P")
check("partial_fractions", sp.simplify(1 / (Ps * (1 - Ps / K)) - (1 / Ps + 1 / (K - Ps))) == 0)
check("fastest_growth_at_K/2",
      sp.solve(sp.diff(k * Ps * (1 - Ps / K), Ps), Ps) == [K / 2])
check("blow_up_y'=y^2", sp.simplify(sp.diff(1 / (1 - t), t) - (1 / (1 - t)) ** 2) == 0)
check("blow_up_time_from_y0=2", sp.solve(1 - 2 * t, t) == [sp.Rational(1, 2)])
check("added_constant_fails_by_1",
      sp.simplify(sp.diff(sp.exp(t / 2) + 2, t) - (sp.Rational(1, 2) * (sp.exp(t / 2) + 2) - 1)) == 0)


def separable(F, tt, yy):
    """F(t, y) = g(t) h(y) on a region where F != 0 iff F * F_ty = F_t * F_y."""
    return sp.simplify(F * sp.diff(F, tt, yy) - sp.diff(F, tt) * sp.diff(F, yy)) == 0


tt, yy = sp.symbols("tt yy", real=True)
check("t+y_not_separable", not separable(tt + yy, tt, yy))
check("t*y^2_and_exp(t+y)_separable", separable(tt * yy ** 2, tt, yy) and separable(sp.exp(tt + yy), tt, yy))
# l2 quiz[1].feedback.correct: "t + y is a sum, not a product, so it cannot be split".
# The stated reason would make every sum non-separable. 1 + y^2 (homework-1 items[6]) is a sum and separable.
# FINDING_1 (corrected claim, fix pass): the feedback now reads "No product $g(t)h(y)$ equals $t + y$".
# (log F)_ty = (F F_ty - F_t F_y) / F^2 is -1/(t+y)^2 for t + y, but 0 for the sums 1 + y^2 and t + ty.
check("FINDING_1 no_product_equals_t+y, while sums 1+y^2 and t+ty separate (corrected claim, fix pass)",
      not separable(tt + yy, tt, yy) and separable(1 + yy ** 2, tt, yy) and separable(tt + tt * yy, tt, yy)
      and sp.simplify(sp.diff(sp.log(tt + yy), tt, yy) + 1 / (tt + yy) ** 2) == 0
      and "No product $g(t)h(y)$ equals $t + y$, so it cannot be split." in _txt("l2-separable.json"))

# l2 screens[9]: "first few months, where the two curves agree" / "1 - P/K is about 1"
rate0 = 0.8 * (1 - 1000 / 10000)
# FINDING_2 (corrected claim, fix pass): "At the start 1 - P/K is 0.9, close to 1, so P grows almost as P0 e^{kt}";
# "the two curves are still close" over the first few months: gap 2.2% at 3 months, 4.7% at 6 months.
lg0 = lambda x: 10000 / (1 + 9 * math.exp(-0.8 * x))
gaps = [1 - lg0(x) / (1000 * math.exp(0.8 * x)) for x in (0.25, 0.5)]
check("FINDING_2 start_factor_0.9_rate_0.72_curves_close_early (corrected claim, fix pass)",
      abs((1 - 1000 / 10000) - 0.9) < 1e-12 and abs(rate0 - 0.72) < 1e-12
      and abs(gaps[0] - 0.0217) < 5e-4 and abs(gaps[1] - 0.0469) < 5e-4
      and "where the two curves are still close" in _txt("l2-separable.json")
      and "At the start $1 - P/K$ is 0.9, close to 1" in _txt("l2-separable.json"))
lg = lambda x: 10000 / (1 + 9 * math.exp(-0.8 * x))
check("exp_fit_year3_overshoots", abs(1000 * math.exp(2.4) - 11023.18) < 0.01 and abs(lg(3) - 5505.21) < 0.01)
check("quarter_year_gap_is_2pc", abs(1000 * math.exp(0.2) / lg(0.25) - 1.022) < 0.002)

# ---- l3: integrating factor -------------------------------------------------
yf = sp.Function("y")
sol = sp.dsolve(sp.Eq(yf(t).diff(t) + 2 * t * yf(t), t), yf(t), ics={yf(0): 1}).rhs
check("IF_varying_coefficient", sp.simplify(sol - (sp.Rational(1, 2) + sp.exp(-t ** 2) / 2)) == 0)
w1 = t / 2 - sp.Rational(1, 4) + sp.Rational(5, 4) * sp.exp(-2 * t)
w2 = (t ** 2 / 2 + 1) * sp.exp(-t ** 2)
check("trap_curves", abs(float(w1.subs(t, 1)) - 0.4192) < 5e-5 and abs(float(w2.subs(t, 1)) - 0.5518) < 5e-5
      and sp.simplify(sp.diff(sp.exp(2 * t) * w1, t) - t * sp.exp(2 * t)) == 0
      and sp.simplify(sp.diff(sp.exp(t ** 2) * w2, t) - t) == 0)
ts = sp.Symbol("t", real=True)
gen = (y0 + q / a) * sp.exp(a * ts) - q / a
check("const_coeff_formula", sp.simplify(sp.diff(gen, ts) - (a * gen + q)) == 0 and sp.simplify(gen.subs(ts, 0) - y0) == 0)
check("const_coeff_limit_a_to_0", sp.simplify(sp.limit(gen, a, 0) - (y0 + q * ts)) == 0)
r, pay, L0 = sp.symbols("r pay L0", positive=True)
L = (L0 - pay / r) * sp.exp(r * t) + pay / r
check("payoff_time_formula", sp.simplify(L.subs(t, sp.log(pay / (pay - r * L0)) / r)) == 0)
check("perpetuity_steady_c/r_is_unstable", sp.diff(0.04 * Ps - 5, Ps) > 0 and abs(5 / 0.04 - 125) < 1e-12)

# ---- l4: slope fields and equilibria ---------------------------------------
check("y'=t-y_general_solution",
      sp.simplify(sp.diff(t - 1 + C * sp.exp(-t), t) - (t - (t - 1 + C * sp.exp(-t)))) == 0)
s = solve_ivp(lambda u, v: (v - 1) * (v - 3), [0, 5], [2.9], rtol=1e-12, atol=1e-14)
check("y(5)_from_2.9", abs(s.y[0, -1] - 1.0017) < 5e-5)
f = lambda v: v * (1 - v) * (v - 0.3)
df = lambda v, h=1e-6: (f(v + h) - f(v - h)) / (2 * h)
check("tipping_point_derivatives", abs(df(0) + 0.3) < 1e-6 and abs(df(1) + 0.7) < 1e-6 and abs(df(0.3) - 0.21) < 1e-6)
# semi-stable (y-2)^2: from below it rises into 2, from above it leaves
lo = solve_ivp(lambda u, v: (v - 2) ** 2, [0, 200], [1.5], rtol=1e-10, atol=1e-12).y[0, -1]
hi = solve_ivp(lambda u, v: (v - 2) ** 2, [0, 1.9], [2.5], rtol=1e-10, atol=1e-12).y[0, -1]
check("semi_stable_(y-2)^2", 1.99 < lo < 2 and hi > 10)
# homework-1 items[3]: y' = y^2(1-y) from -0.5 rises and approaches 0 from below
hv = solve_ivp(lambda u, v: v * v * (1 - v), [0, 2000], [-0.5], rtol=1e-10, atol=1e-13).y[0, -1]
check("hw1_semi_stable_from_below", -0.001 < hv < 0)

# ---- l5: mean reversion -----------------------------------------------------
kap, th, r0 = sp.symbols("kappa theta r0", positive=True)
rt = th + (r0 - th) * sp.exp(-kap * t)
check("vasicek_mean_path", sp.simplify(sp.diff(rt, t) - kap * (th - rt)) == 0)
T = sp.Symbol("T", positive=True)
avg = sp.integrate(rt, (t, 0, T)) / T
check("average_rate_formula", sp.simplify(avg - (th + (r0 - th) * (1 - sp.exp(-kap * T)) / (kap * T))) == 0)
check("average_5y", abs(float(avg.subs({th: 0.04, r0: 0.06, kap: 0.5, T: 5})) - 0.047343) < 5e-7)
phi = math.exp(-0.5 / 252)
check("daily_phi", abs(phi - 0.998018) < 5e-7 and abs(phi ** 252 - math.exp(-0.5)) < 1e-12)
# Monte Carlo: the AR(1) mean after 252 days is the ODE value, not the start and not theta
rng = np.random.default_rng(20261110)
n = 200000
x = np.full(n, 0.06)
for _ in range(252):
    x = 0.04 + phi * (x - 0.04) + 0.0006 * rng.standard_normal(n)
se = x.std(ddof=1) / math.sqrt(n)
target = 0.04 + 0.02 * math.exp(-0.5)
check("MC_vasicek_mean_252_days (200k paths, within 4 se; start and theta rejected)",
      abs(x.mean() - target) < 4 * se and abs(x.mean() - 0.06) > 50 * se and abs(x.mean() - 0.04) > 50 * se)
check("half_life_and_two_half_lives", abs(math.log(2) / 0.5 - 1.3863) < 5e-5 and abs(math.log(4) / 0.5 - 2.7726) < 5e-5)
check("calibrated_kappa", abs(math.log(3) / 2 - 0.5493) < 5e-5 and abs(math.log(2) / (math.log(3) / 2) - 1.26) < 0.005)
check("negative_kappa_doubles_every_3.47", abs(math.log(2) / 0.2 - 3.47) < 0.005)

# ---- review-1, homework-1 ---------------------------------------------------
check("hw1_ty'+2y=4t^2", sp.simplify(sp.dsolve(sp.Eq(t * yf(t).diff(t) + 2 * yf(t), 4 * t ** 2), yf(t),
                                               ics={yf(1): 2}).rhs - (t ** 2 + 1 / t ** 2)) == 0)
check("hw1_tan_blow_up", sp.simplify(sp.diff(sp.tan(t), t) - (1 + sp.tan(t) ** 2)) == 0)
check("hw1_retiree", abs(math.log(1.6) / 0.03 - 15.67) < 0.005 and abs(math.log(8000 / 0.03 / 100000) / 0.03 - 32.69) < 0.005)
fh = lambda v: v * (v - 1) * (v - 3)
dfh = lambda v, h=1e-6: (fh(v + h) - fh(v - h)) / (2 * h)
check("hw1_three_equilibria", abs(dfh(0) - 3) < 1e-5 and abs(dfh(1) + 2) < 1e-5 and abs(dfh(3) - 6) < 1e-5)
check("rev1_logistic_time", abs(math.log(3) / 0.5 - 2.1972) < 5e-5)
check("rev1_time_to_4pc", abs(4 * math.log(3) - 4.3944) < 5e-5 and abs(math.log(1.5) / 0.25 - 1.6219) < 5e-5)

print()
print("expected fails (findings):", len(NOTES))
print("unexpected fails:", len(FAILS))
sys.exit(1 if FAILS else 0)
