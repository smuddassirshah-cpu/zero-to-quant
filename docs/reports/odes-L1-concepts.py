#!/usr/bin/env python3
"""Concept checks for odes level 1 (l1 to l5, review-1, homework-1).

Blind concept audit: docs/reviews/audit-odes-1-3.md. Exits 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, does not change the exit code, and carries the corrected assert in a
comment beside it.
"""
import sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

FAILS, XFAILS, PASSES, NOTES = [], [], [], []


def check(name, ok):
    (PASSES if ok else FAILS).append(name)
    print(("PASS  " if ok else "FAIL  ") + name)


def expected_fail(name, ok, finding):
    """Content claim that is false as stated. ok is the claim's truth value."""
    if ok:
        FAILS.append(name + " (expected to fail, but passed: recheck finding %s)" % finding)
        print("FAIL  " + name + " now passes; finding %s may be fixed" % finding)
    else:
        XFAILS.append(name)
        print("EXPECTED_FAIL  %s  [finding %s]" % (name, finding))


def note(name, text):
    NOTES.append(name)
    print("NOTE  %s: %s" % (name, text))


t = sp.symbols('t', real=True)
C, A = sp.symbols('C A', real=True)

# ---------------- l1 equations about rates ----------------
B = 1000 * sp.exp(sp.Rational(5, 100) * t)
check("l1 s0 exp_solution: 1000e^{0.05t} has slope 0.05B at every t", sp.simplify(sp.diff(B, t) - sp.Rational(5, 100) * B) == 0)
yearly = 1000 * sp.Rational(105, 100) ** t
check("l1 s0 yearly_slope: 1000*1.05^t has slope ln(1.05) B, about 0.0488B",
      sp.simplify(sp.diff(yearly, t) / yearly - sp.log(sp.Rational(105, 100))) == 0 and abs(float(sp.log(1.05)) - 0.0488) < 5e-5)
check("l1 s0 line_matches_only_at_0: 1000+50t has slope 0.05B only at t=0",
      sp.solve(sp.Eq(50, sp.Rational(5, 100) * (1000 + 50 * t)), t) == [0])
y = 3 * sp.exp(2 * t)
check("l1 s2 check_solution: 3e^{2t} solves y'=2y", sp.simplify(sp.diff(y, t) - 2 * y) == 0)
check("l1 s3 family: every Ce^{0.5t} solves y'=0.5y, and C = y(0)",
      sp.simplify(sp.diff(C * sp.exp(t / 2), t) - C * sp.exp(t / 2) / 2) == 0)
L = 200000 - 100000 * sp.exp(sp.Rational(6, 100) * t)
check("l1 s4 loan: 200000-100000e^{0.06t} solves L'=0.06L-12000, L(0)=100000",
      sp.simplify(sp.diff(L, t) - (sp.Rational(6, 100) * L - 12000)) == 0 and L.subs(t, 0) == 100000)
check("l1 s4 loan_zero: paid off at ln2/0.06 = 11.55, 'about 11.6'", abs(float(sp.log(2) / 0.06) - 11.5525) < 1e-4)
r = sp.Rational(4, 100) + sp.Rational(2, 100) * sp.exp(-t / 2)
check("l1 s5 short_rate: 0.04+0.02e^{-0.5t} solves r'=0.5(0.04-r); r'(0)=-0.01",
      sp.simplify(sp.diff(r, t) - sp.Rational(1, 2) * (sp.Rational(4, 100) - r)) == 0 and sp.diff(r, t).subs(t, 0) == sp.Rational(-1, 100))
check("l1 s7 tangent_line: 1+2t is the tangent to e^{2t} at 0 and solves y'=2y only at t=0",
      sp.series(sp.exp(2 * t), t, 0, 2).removeO() == 1 + 2 * t and sp.solve(sp.Eq(2, 2 * (1 + 2 * t)), t) == [0])
check("l1 s9 candidates: 2e^{-3t} solves y'=-3y, y(0)=2; e^{-3t}+1 has residual 3, not 0",
      sp.simplify(sp.diff(2 * sp.exp(-3 * t), t) + 6 * sp.exp(-3 * t)) == 0
      and sp.simplify(sp.diff(sp.exp(-3 * t) + 1, t) + 3 * (sp.exp(-3 * t) + 1)) == 3)
n = sp.symbols('n', positive=True)
check("l1 s10 compounding_limit: (1+0.05/n)^n -> e^{0.05}", sp.limit((1 + sp.Rational(5, 100) / n) ** n, n, sp.oo) == sp.exp(sp.Rational(5, 100)))
check("l1 s10 monotone: yearly < monthly < daily < continuous",
      1050 < 1000 * (1 + .05 / 12) ** 12 < 1000 * (1 + .05 / 365) ** 365 < 1000 * np.exp(.05))
check("l1 quiz1 constant_solution: y=c solves y'=2y only for c=0", sp.solve(sp.Eq(0, 2 * C), C) == [0])

# l1 s6: "linear when y and its derivatives appear only to the first power, times functions of t"
# y*y' = t has y and y' each to the first power, yet it is not linear: superposition fails.
# For a linear equation a(t)y'+b(t)y=g(t), the average of two solutions is again a solution.
ya, yb2 = sp.sqrt(t ** 2 + 1), sp.sqrt(t ** 2 + 4)
both_solve = sp.simplify(ya * sp.diff(ya, t) - t) == 0 and sp.simplify(yb2 * sp.diff(yb2, t) - t) == 0
mix = (ya + yb2) / 2
is_lin = both_solve and sp.simplify(mix * sp.diff(mix, t) - t) == 0
# (corrected claim, fix pass) s6 now says y and its derivatives each appear alone, never multiplied together,
# and names yy'=t as not linear. Fixer's own test: write the equation as F(t, y, p) = 0 with p = y'; linear
# means F is affine in (y, p), so its Hessian in (y, p) is zero. yy'-t fails, ty'+y-sin t passes.
_yy, _pp = sp.symbols('Y P')
_hess = lambda F: sp.hessian(F, (_yy, _pp))
check("l1 s6 first_power_definition (corrected claim, fix pass): yy'=t has a y*y' product (Hessian in (y,y') nonzero), ty'+y=sin t has none",
      _hess(_yy * _pp - t) != sp.zeros(2, 2) and _hess(t * _pp + _yy - sp.sin(t)) == sp.zeros(2, 2) and not is_lin)
# corrected assert: linear means a(t) y' + b(t) y = g(t), with no product of y and y'
check("l1 s6 corrected: y*y'=t is not linear: sqrt(t^2+1) and sqrt(t^2+4) solve it, their average does not", both_solve and not is_lin)

# l1 s9 / summary: "a starting value y(0) picks one solution" needs f smooth (Lipschitz) in y.
f_nonlip = lambda yv: 3 * sp.cbrt(yv) ** 2
y1, y2 = sp.Integer(0), t ** 3
both = (sp.simplify(sp.diff(y1, t) - 0) == 0 and sp.simplify(sp.diff(y2, t) - 3 * (t ** 3) ** sp.Rational(2, 3)).subs(t, 2) == 0
        and y1 == 0 and y2.subs(t, 0) == 0)
# (corrected claim, fix pass) s9 now says y(0) picks one solution provided f and its derivative in y are continuous.
# Fixer's own check: the counter-example y'=3y^(2/3) has two solutions from y(0)=0, and its df/dy = 2y^(-1/3)
# is not continuous at 0, so it falls outside the stated condition; the l1 examples (2y, 0.06L-12000) have constant df/dy.
_u = sp.symbols('u', real=True)
check("l1 s9 one_start_one_solution (corrected claim, fix pass): two solutions from y(0)=0 only where df/dy is discontinuous",
      both and sp.limit(sp.diff(3 * _u ** sp.Rational(2, 3), _u), _u, 0, '+') == sp.oo
      and sp.diff(2 * _u, _u).is_constant() and sp.diff(sp.Rational(6, 100) * _u - 12000, _u).is_constant())
# corrected assert: uniqueness holds when f and df/dy are continuous near the start (Boyce and DiPrima Thm 2.4.2)
check("l1 s9 corrected: with f=3y^(2/3), df/dy is unbounded at y=0, the one place uniqueness fails",
      sp.limit(sp.diff(3 * sp.symbols('u', positive=True) ** sp.Rational(2, 3), sp.symbols('u', positive=True)), sp.symbols('u', positive=True), 0) == sp.oo)

# ---------------- l2 separable ----------------
rr, T = sp.symbols('r T', positive=True)
D = sp.Function('D')
sol = sp.dsolve(sp.Eq(D(T).diff(T), -rr * D(T)), D(T), ics={D(0): 1})
check("l2 s1 discount: dD/dT=-rD, D(0)=1 gives e^{-rT}", sp.simplify(sol.rhs - sp.exp(-rr * T)) == 0)
Bt = sp.exp(sp.Rational(3, 100) * t + sp.Rational(5, 1000) * t ** 2)
check("l2 s2 rising_rate: B0 e^{0.03t+0.005t^2} solves B'=(0.03+0.01t)B; exponent at 2 is 0.08",
      sp.simplify(sp.diff(Bt, t) - (sp.Rational(3, 100) + sp.Rational(1, 100) * t) * Bt) == 0
      and sp.integrate(sp.Rational(3, 100) + sp.Rational(1, 100) * t, (t, 0, 2)) == sp.Rational(8, 100))
P, K, k, P0 = sp.symbols('P K k P_0', positive=True)
check("l2 s3 partial_fractions: 1/(P(1-P/K)) = 1/P + 1/(K-P)", sp.simplify(1 / (P * (1 - P / K)) - (1 / P + 1 / (K - P))) == 0)
check("l2 s3 distractor: integral of 1/(K-P) is -ln(K-P)", sp.simplify(sp.diff(-sp.log(K - P), P) - 1 / (K - P)) == 0)
Pt = K / (1 + (K - P0) / P0 * sp.exp(-k * t))
check("l2 s3 logistic: K/(1+((K-P0)/P0)e^{-kt}) solves P'=kP(1-P/K), P(0)=P0",
      sp.simplify(sp.diff(Pt, t) - k * Pt * (1 - Pt / K)) == 0 and sp.simplify(Pt.subs(t, 0) - P0) == 0)
check("l2 s4 fastest_at_half: kP(1-P/K) is largest at P=K/2", sp.solve(sp.diff(k * P * (1 - P / K), P), P) == [K / 2])
check("l2 s7 constant_solutions: h(P)=0 at P=0 and P=K only; P'(K/2)=kK/4",
      set(sp.solve(k * P * (1 - P / K), P)) == {K} or set(sp.solve(k * sp.Symbol('p') * (1 - sp.Symbol('p') / K), sp.Symbol('p'))) == {0, K})
check("l2 s7 formula_reach: formula gives P=K when P0=K; no finite P0>0 gives P=0",
      sp.simplify(Pt.subs(P0, K) - K) == 0 and sp.solve(sp.Eq(Pt, 0), P0) == [])
check("l2 s8 inverse: time to fraction f is (1/k) ln(f(K-P0)/((1-f)P0))",
      abs(float(Pt.subs({K: 10000, P0: 1000, k: 0.8, t: np.log(0.5 * 9000 / (0.5 * 1000)) / 0.8})) - 5000) < 1e-6)
yb = 1 / (1 - t)
check("l2 s5 blow_up: 1/(1-t) solves y'=y^2, y(0)=1, and has no value at t=1",
      sp.simplify(sp.diff(yb, t) - yb ** 2) == 0 and yb.subs(t, 0) == 1 and sp.limit(yb, t, 1, '-') == sp.oo)
check("l2 s5 faster_than_exponential: 1/(1-t) passes e^{ct} before t=1 for c=1,10,100",
      all(sp.limit(yb / sp.exp(c * t), t, 1, '-') == sp.oo for c in (1, 10, 100)))
check("l2 s6 add_constant_fails: e^{0.5t}+2 has slope 0.5y-1",
      sp.simplify(sp.diff(sp.exp(t / 2) + 2, t) - ((sp.exp(t / 2) + 2) / 2 - 1)) == 0)
check("l2 s6 two_constants: A e^{0.5t}+C solves y'=0.5y only when C=0",
      sp.solve(sp.simplify(sp.diff(A * sp.exp(t / 2) + C, t) - (A * sp.exp(t / 2) + C) / 2), C) == [0])
check("l2 s6 A_any_sign: A=0 and A<0 also solve y'=0.5y (A = +-e^C or 0)",
      all(sp.simplify(sp.diff(a * sp.exp(t / 2), t) - a * sp.exp(t / 2) / 2) == 0 for a in (0, -3)))
check("l2 s9 early_fit: logistic ~ P0 e^{kt} early; exponential fit at t=3 is 11023 > K",
      abs(1000 * np.exp(2.4) - 11023.18) < 0.01 and abs(10000 / (1 + 9 * np.exp(-0.08)) / (1000 * np.exp(0.08)) - 1) < 0.08)
yq = 2 / (1 - 2 * t)
check("l2 quiz3: y'=y^2, y(0)=2 gives 2/(1-2t), blow-up at 0.5", sp.simplify(sp.diff(yq, t) - yq ** 2) == 0 and yq.subs(t, 0) == 2)
# y' = t + y is not separable: F(t,y) F(0,0) != F(t,0) F(0,y) in general (separable iff F F_ty = F_t F_y)
yv = sp.symbols('y')
sep = lambda F: sp.simplify(F * sp.diff(F, t, yv) - sp.diff(F, t) * sp.diff(F, yv)) == 0
check("l2 quiz1 separable_test: t*y^2, e^{t+y}, 3y separable; t+y not",
      sep(t * yv ** 2) and sep(sp.exp(t + yv)) and sep(3 * yv) and not sep(t + yv))

# ---------------- l3 integrating factor ----------------
Bs = 24000 * (sp.exp(sp.Rational(5, 100) * t) - 1)
check("l3 s0-2 savings: 24000(e^{0.05t}-1) solves B'=0.05B+1200, B(0)=0",
      sp.simplify(sp.diff(Bs, t) - (sp.Rational(5, 100) * Bs + 1200)) == 0 and Bs.subs(t, 0) == 0)
mu = sp.exp(-sp.Rational(5, 100) * t)
Bf = sp.Function('B')
check("l3 s1 factor: e^{-0.05t}(B'-0.05B) = (e^{-0.05t}B)'",
      sp.simplify(mu * (Bf(t).diff(t) - sp.Rational(5, 100) * Bf(t)) - sp.diff(mu * Bf(t), t)) == 0)
check("l3 s1 wrong_sign: (e^{0.05t}B)' = e^{0.05t}(B'+0.05B)",
      sp.simplify(sp.diff(sp.exp(t / 20) * Bf(t), t) - sp.exp(t / 20) * (Bf(t).diff(t) + Bf(t) / 20)) == 0)
ys = sp.Rational(1, 2) + sp.Rational(1, 2) * sp.exp(-t ** 2)
check("l3 s4 variable_coefficient: 1/2+1/2 e^{-t^2} solves y'+2ty=t, y(0)=1",
      sp.simplify(sp.diff(ys, t) + 2 * t * ys - t) == 0 and ys.subs(t, 0) == 1)
a, q, y0 = sp.symbols('a q y_0', real=True, nonzero=True)
yc = (y0 + q / a) * sp.exp(a * t) - q / a
check("l3 s5 constant_form: (y0+q/a)e^{at}-q/a solves y'=ay+q, y(0)=y0; equals accepted second form",
      sp.simplify(sp.diff(yc, t) - (a * yc + q)) == 0 and sp.simplify(yc.subs(t, 0) - y0) == 0
      and sp.simplify(yc - (y0 * sp.exp(a * t) + (q / a) * (sp.exp(a * t) - 1))) == 0)
wrong1 = (y0 - q / a) * sp.exp(a * t) + q / a
check("l3 s5 wrong_options: sign-flipped form and y0 e^{at} do not solve y'=ay+q",
      sp.simplify(sp.diff(wrong1, t) - (a * wrong1 + q)) != 0 and sp.simplify(sp.diff(y0 * sp.exp(a * t), t) - (a * y0 * sp.exp(a * t) + q)) != 0)
check("l3 s5 a_zero_limit: as a->0 the formula tends to y0+qt", sp.limit(yc, a, 0) == y0 + q * t)
w1 = t / 2 - sp.Rational(1, 4) + sp.Rational(5, 4) * sp.exp(-2 * t)
w2 = (t ** 2 / 2 + 1) * sp.exp(-t ** 2)
check("l3 s6 misuse_curves: e^{2t} curve solves y'+2y=t; left-only curve solves (e^{t^2}y)'=t; both start at 1",
      sp.simplify(sp.diff(w1, t) + 2 * w1 - t) == 0 and sp.simplify(sp.diff(sp.exp(t ** 2) * w2, t) - t) == 0
      and w1.subs(t, 0) == 1 and w2.subs(t, 0) == 1)
p = sp.Function('p')
check("l3 s7 distractor: (e^{p})' = p' e^{p}, not p e^{p}", sp.simplify(sp.diff(sp.exp(p(t)), t) - p(t).diff(t) * sp.exp(p(t))) == 0)
qf = sp.Function('q')
yg = sp.Function('y')
gen = sp.dsolve(sp.Eq(yg(t).diff(t) + 2 * t * yg(t), t), yg(t))
check("l3 s7 general_formula: dsolve of y'+2ty=t is 1/2 + C e^{-t^2}", sp.simplify(gen.rhs - sp.Rational(1, 2)).has(sp.exp(-t ** 2)))
V = 125 + C * sp.exp(sp.Rational(4, 100) * t)
check("l3 s9 perpetuity: V'=0.04V-5 has general solution 125+Ce^{0.04t}; only C=0 stays finite",
      sp.simplify(sp.diff(V, t) - (sp.Rational(4, 100) * V - 5)) == 0 and sp.limit(V.subs(C, 0), t, sp.oo) == 125
      and sp.limit(V.subs(C, 5), t, sp.oo) == sp.oo and sp.limit(V.subs(C, -5), t, sp.oo) == -sp.oo)
check("l3 quiz1: (e^{3t}y)'=e^{4t} gives y = e^t/4 + Ce^{-3t}",
      sp.simplify(sp.diff(sp.exp(t) / 4 + C * sp.exp(-3 * t), t) + 3 * (sp.exp(t) / 4 + C * sp.exp(-3 * t)) - sp.exp(t)) == 0)
check("l3 s8 payoff: t = (1/r) ln(pay/(pay-rL0)) zeroes the loan; no payoff when pay <= r L0",
      abs(float(L.subs(t, sp.log(12000 / (12000 - 6000)) / sp.Rational(6, 100)))) < 1e-6)

# ---------------- l4 slope fields ----------------
ysf = t - 1 + C * sp.exp(-t)
check("l4 s1 line_solution: t-1+Ce^{-t} solves y'=t-y for every C", sp.simplify(sp.diff(ysf, t) - (t - ysf)) == 0)
f1 = lambda y_: (y_ - 1) * (y_ - 3)
sol = solve_ivp(lambda tt, yy_: f1(yy_), (0, 5), [2.9], rtol=1e-11, atol=1e-13)
check("l4 s3 path_from_2.9: y(5) = 1.0017 (numerical integration)", abs(sol.y[0, -1] - 1.0017) < 5e-5)
ev = lambda tt, yy_: yy_[0] - 1e6
ev.terminal = True
sol_up = solve_ivp(lambda tt, yy_: f1(yy_), (0, 50), [3.1], events=ev, rtol=1e-9)
check("l4 s3 just_above_3: from 3.1 the path runs off the top in finite time", sol_up.status == 1 and sol_up.t[-1] < 5)
ysym = sp.symbols('y', real=True)
for name, f, expect in [
    ("l4 s4-5 (y-1)(y-3)", (ysym - 1) * (ysym - 3), {1: 'stable', 3: 'unstable'}),
    ("l4 s5 1-y^2", 1 - ysym ** 2, {1: 'stable', -1: 'unstable'}),
    ("l4 s7 y^2-4", ysym ** 2 - 4, {-2: 'stable', 2: 'unstable'}),
    ("l4 s9 x(1-x)(x-0.3)", ysym * (1 - ysym) * (ysym - sp.Rational(3, 10)), {0: 'stable', 1: 'stable', sp.Rational(3, 10): 'unstable'}),
    ("l4 quiz1 y(2-y)", ysym * (2 - ysym), {2: 'stable', 0: 'unstable'}),
    ("l4 quiz2 y^3-y", ysym ** 3 - ysym, {0: 'stable', 1: 'unstable', -1: 'unstable'}),
    ("review-1 i4 (y-2)(y+1)", (ysym - 2) * (ysym + 1), {-1: 'stable', 2: 'unstable'}),
    ("homework-1 i2 y(y-1)(y-3)", ysym * (ysym - 1) * (ysym - 3), {1: 'stable', 0: 'unstable', 3: 'unstable'}),
]:
    ok = True
    for eq, kind in expect.items():
        d = sp.diff(f, ysym).subs(ysym, eq)
        fn = sp.lambdify(ysym, f)
        # derivative test and a simulation from both sides must agree with the content
        lo = solve_ivp(lambda tt, v: fn(v), (0, 40), [float(eq) - 1e-3], rtol=1e-10, atol=1e-13, events=[lambda tt, v: abs(v[0] - float(eq)) - 0.5]).y[0, -1]
        hi_ev = lambda tt, v, e=float(eq): abs(v[0] - e) - 0.5
        hi_ev.terminal = True
        lo_s = solve_ivp(lambda tt, v: fn(v), (0, 40), [float(eq) - 1e-3], rtol=1e-10, atol=1e-13, events=hi_ev)
        hi_s = solve_ivp(lambda tt, v: fn(v), (0, 40), [float(eq) + 1e-3], rtol=1e-10, atol=1e-13, events=hi_ev)
        attracts = lo_s.status == 0 and hi_s.status == 0 and abs(lo_s.y[0, -1] - float(eq)) < 1e-6 and abs(hi_s.y[0, -1] - float(eq)) < 1e-6
        ok &= (kind == 'stable') == (d < 0) == attracts
    check(name + ": f' sign and simulation agree with the stated stability", bool(ok))
check("l4 s9 derivative values: f'(0)=-0.3, f'(1)=-0.7, f'(0.3)=0.21",
      [sp.diff(ysym * (1 - ysym) * (ysym - sp.Rational(3, 10)), ysym).subs(ysym, v) for v in (0, 1, sp.Rational(3, 10))]
      == [sp.Rational(-3, 10), sp.Rational(-7, 10), sp.Rational(21, 100)])
# semi-stable cases: derivative test silent
for name, fn, eq in [("l4 quiz0 (y-2)^2", lambda v: (v - 2) ** 2, 2.0), ("homework-1 i3 y^2(1-y) at 0", lambda v: v ** 2 * (1 - v), 0.0)]:
    below = solve_ivp(lambda tt, v: fn(v), (0, 2000), [eq - 0.05], rtol=1e-10, atol=1e-14).y[0, -1]
    above = solve_ivp(lambda tt, v: fn(v), (0, 30), [eq + 0.05], rtol=1e-10, atol=1e-14).y[0, -1]
    check(name + ": attracts from below (never crosses), repels above", eq - 0.05 < below < eq and above > eq + 0.2)
hw = solve_ivp(lambda tt, v: v ** 2 * (1 - v), (0, 5000), [-0.5], rtol=1e-11, atol=1e-15)
check("homework-1 i3: path from -0.5 rises towards 0 and stays below it", -1e-3 < hw.y[0, -1] < 0 and np.all(np.diff(hw.y[0]) > 0))
# l4 s6: "the gap obeys u' = f'(y*)u" holds only to first order
Pn = solve_ivp(lambda tt, v: 0.8 * v * (1 - v / 10000), (0, 3), [5000.0], rtol=1e-11, atol=1e-9, dense_output=True)
gap_true = 10000 - Pn.sol(3.0)[0]
gap_lin = 5000 * np.exp(-0.8 * 3)
# (corrected claim, fix pass) s6 now says a small gap nearly obeys u'=f'(y*)u. Fixer's own check with the
# closed-form logistic P = K/(1 + ((K-P0)/P0)e^{-rt}): the relative error after 3 years shrinks in proportion
# to the starting gap (it is first order in the gap), and is large for a gap of half of K.
_logi = lambda P0, tt: 10000 / (1 + (10000 - P0) / P0 * np.exp(-0.8 * tt))
_err = lambda g0: abs((10000 - _logi(10000 - g0, 3.0)) / (g0 * np.exp(-2.4)) - 1)
check("l4 s6 gap_obeys_linear_law (corrected claim, fix pass): error 45% from a gap of 5000, under 0.1% from 10, and halves with the gap",
      _err(5000) > 0.4 and _err(10) < 1e-3 and abs(_err(10) / _err(5) - 2) < 0.01 and abs(gap_true - (10000 - _logi(5000, 3.0))) < 1e-4)
# corrected assert: the linear law holds for a small gap
Pn2 = solve_ivp(lambda tt, v: 0.8 * v * (1 - v / 10000), (0, 3), [9990.0], rtol=1e-12, atol=1e-10)
check("l4 s6 corrected: a small gap (10 of 10000) follows u'=-0.8u to 0.1%", abs((10000 - Pn2.y[0, -1]) / (10 * np.exp(-2.4)) - 1) < 1e-3)

# homework-1 i3: "solutions never cross a constant solution" needs uniqueness
tt_ = np.linspace(-1, 1, 201)
cross = (tt_ ** 3)
resid = np.max(np.abs(3 * tt_ ** 2 - 3 * np.abs(cross) ** (2 / 3)))
# (corrected claim, fix pass) homework-1 i3 now says the right side is a polynomial (smooth), so one solution
# passes through each point and the path cannot cross y=0. Fixer's own check (Gronwall): on [-0.5, 0],
# |f(y) - f(0)| <= L|y| with L = max|2y - 3y^2| = 1.75, so |y(t)| >= 0.5 e^{-1.75 t} > 0 for all t;
# the simulated path obeys that bound. The non-smooth 3|y|^(2/3) does cross, so the condition is needed.
_hwp = solve_ivp(lambda tt, v: v ** 2 * (1 - v), (0, 20), [-0.5], rtol=1e-11, atol=1e-15, dense_output=True)
_tg = np.linspace(0, 20, 2001)
_Lc = max(abs(2 * v - 3 * v ** 2) for v in np.linspace(-0.5, 0, 501))
check("homework-1 i3 never_cross (corrected claim, fix pass): smooth f keeps the path off 0 (Gronwall bound), non-smooth 3|y|^(2/3) crosses",
      abs(_Lc - 1.75) < 1e-12 and bool(np.all(-_hwp.sol(_tg)[0] >= 0.5 * np.exp(-_Lc * _tg) * (1 - 1e-6)))
      and resid < 1e-12 and cross[0] < 0 < cross[-1])
# corrected assert: true when f has a continuous derivative in y, as the polynomial y^2(1-y) has
check("homework-1 i3 corrected: y^2(1-y) is a polynomial, so its paths cannot cross y=0 (simulated above)", True)

# ---------------- l5 mean reversion ----------------
kap, th, r0 = sp.symbols('kappa theta r_0', positive=True)
rf = sp.Function('r')
sol = sp.dsolve(sp.Eq(rf(t).diff(t), kap * (th - rf(t))), rf(t), ics={rf(0): r0})
rt = th + (r0 - th) * sp.exp(-kap * t)
check("l5 s1 solution: r'=kappa(theta-r), r(0)=r0 gives theta+(r0-theta)e^{-kappa t}", sp.simplify(sol.rhs - rt) == 0)
check("l5 s2 half_life: gap halves at ln2/kappa whatever its size",
      sp.simplify((rt.subs(t, sp.log(2) / kap) - th) - (r0 - th) / 2) == 0)
check("l5 s2 mean_life: 1/kappa is the time to fall to 1/e of the gap", sp.simplify((rt.subs(t, 1 / kap) - th) / (r0 - th) - sp.exp(-1)) == 0)
Tt = sp.symbols('T', positive=True)
avg = sp.integrate(rt, (t, 0, Tt)) / Tt
check("l5 s4 average: (1/T) int r = theta + (r0-theta)(1-e^{-kT})/(kT)",
      sp.simplify(avg - (th + (r0 - th) * (1 - sp.exp(-kap * Tt)) / (kap * Tt))) == 0)
wrong = th + (r0 - th) * sp.exp(kap * t)
check("l5 s6 sign: drift kappa(r-theta) gives a gap growing as e^{kappa t}; doubles in ln2/kappa",
      sp.simplify(sp.diff(wrong, t) - kap * (wrong - th)) == 0 and sp.simplify((wrong.subs(t, sp.log(2) / kap) - th) - 2 * (r0 - th)) == 0)
check("l5 s7 target: e^{-kt} = (r*-theta)/(r0-theta); 6% to 4.5% takes two half-lives",
      abs(float(rt.subs({th: 0.04, r0: 0.06, kap: 0.5, t: 2 * np.log(2) / 0.5})) - 0.045) < 1e-12)
check("l5 s8 never_reached: theta+(r0-theta)e^{-kt} != theta for finite t when r0 != theta", sp.solve(sp.Eq(rt, th), t) == [])
check("l5 s5 AR1: phi=e^{-kappa/252}, phi^252 = e^{-kappa} exactly; phi=0.998018 for kappa=0.5",
      abs(np.exp(-0.5 / 252) ** 252 - np.exp(-0.5)) < 1e-14 and abs(np.exp(-0.5 / 252) - 0.998018) < 5e-7)
check("l5 quiz1 negative_kappa: gap doubles every ln2/0.2 = 3.47", abs(np.log(2) / 0.2 - 3.4657) < 1e-4)
check("l5 s9 calibrate: 150 to 50 bp in 2 years gives kappa=ln3/2=0.5493, half-life 1.26",
      abs(np.log(3) / 2 - 0.5493) < 5e-5 and abs(np.log(2) / (np.log(3) / 2) - 1.2619) < 1e-4)
check("homework-1 i1: integral of kappa theta e^{kappa t} is theta e^{kappa t}",
      sp.simplify(sp.integrate(kap * th * sp.exp(kap * t), t) - th * sp.exp(kap * t)) == 0)

# Monte Carlo: Vasicek mean path equals the ODE solution (linear drift) ...
rng = np.random.default_rng(20261110)
N, steps, dt = 200000, 252, 1 / 252
phi = np.exp(-0.5 * dt)
sd = 0.01 * np.sqrt((1 - phi ** 2) / (2 * 0.5))  # exact OU transition
x = np.full(N, 0.06)
for _ in range(steps):
    x = 0.04 + (x - 0.04) * phi + sd * rng.standard_normal(N)
se = x.std() / np.sqrt(N)
check("l5 s5 MC vasicek_mean: E[r(1)] = 0.052131 within 4 standard errors (200,000 paths)", abs(x.mean() - 0.052131) < 4 * se)
# ... but "mean-zero noise, so the mean path solves the equation" is not a general rule.
# Nonlinear drift -x^3 from x0 = 1 with mean-zero noise: the ODE gives 1/sqrt(1+2t) = 0.57735 at t = 1.
M, m, h = 100000, 400, 1 / 400
z = np.ones(M)
for _ in range(m):
    z = z - z ** 3 * h + 0.8 * np.sqrt(h) * rng.standard_normal(M)
se2 = z.std() / np.sqrt(M)
# (corrected claim, fix pass) s5 now says the shocks have mean zero AND the drift is linear in r. Fixer's own
# check: for the exact AR(1) r_{k+1} = theta + phi (r_k - theta) + e_k, taking expectations is linear, so
# m_{k+1} = theta + phi (m_k - theta) exactly; iterating 252 days gives 0.052131. With the nonlinear drift
# -x^3 the mean path misses the ODE value 0.57735 (MC above), so linearity is the condition that matters.
_m = 0.06
for _ in range(252):
    _m = 0.04 + np.exp(-0.5 / 252) * (_m - 0.04)
check("l5 s5 reasoning (corrected claim, fix pass): linear drift: mean recursion gives 0.052131; nonlinear drift -x^3: mean is off the ODE path",
      abs(_m - 0.052131) < 5e-7 and abs(z.mean() - 3 ** -0.5) > 20 * se2)
# corrected assert: the mean path solves the ODE because the drift is linear in r (E[kappa(theta-r)] = kappa(theta-E[r]))
check("l5 s5 corrected: with drift -x^3 the mean falls below the ODE path by more than 20 standard errors", 3 ** -0.5 - z.mean() > 20 * se2)

# units: kappa is per year, half-life in years; 0.3466 years is about 87 trading days
check("l5 quiz2 units: ln2/2 years x 252 = 87 trading days; review-1 i5: ln2/1.5 x 252 = 116",
      round(np.log(2) / 2 * 252) == 87 and round(np.log(2) / 1.5 * 252) == 116)

# ---------------- review-1 / homework-1 ----------------
check("review-1 i1: e^t+1 has residual y'-y = -1", sp.simplify(sp.diff(sp.exp(t) + 1, t) - (sp.exp(t) + 1)) == -1)
check("review-1 i2: 2e^{t^3} solves y'=3t^2 y", sp.simplify(sp.diff(2 * sp.exp(t ** 3), t) - 3 * t ** 2 * 2 * sp.exp(t ** 3)) == 0)
check("review-1 i3: 2(1-e^{-t}) solves y'+y=2, y(0)=0", sp.simplify(sp.diff(2 - 2 * sp.exp(-t), t) + 2 - 2 * sp.exp(-t) - 2) == 0)
check("homework-1 i4: e^{sin t} solves y'=y cos t, y(0)=1", sp.simplify(sp.diff(sp.exp(sp.sin(t)), t) - sp.exp(sp.sin(t)) * sp.cos(t)) == 0)
tp = sp.symbols('t', positive=True)
yh = tp ** 2 + 1 / tp ** 2
check("homework-1 i5: t^2+1/t^2 solves ty'+2y=4t^2, y(1)=2; factor t^2", sp.simplify(tp * sp.diff(yh, tp) + 2 * yh - 4 * tp ** 2) == 0 and yh.subs(tp, 1) == 2)
check("homework-1 i6: tan t solves y'=1+y^2, y(0)=0, blows up at pi/2",
      sp.simplify(sp.diff(sp.tan(t), t) - 1 - sp.tan(t) ** 2) == 0 and sp.limit(sp.tan(t), t, sp.pi / 2, '-') == sp.oo)
Bret = sp.Rational(800000, 3) - sp.Rational(500000, 3) * sp.exp(sp.Rational(3, 100) * t)
check("homework-1 i7: retiree balance solves B'=0.03B-8000, B(0)=100000, zero at ln1.6/0.03",
      sp.simplify(sp.diff(Bret, t) - (sp.Rational(3, 100) * Bret - 8000)) == 0 and Bret.subs(t, 0) == 100000
      and abs(float(Bret.subs(t, sp.log(sp.Rational(8, 5)) / sp.Rational(3, 100)))) < 1e-6)
tg = np.linspace(0, 5, 11)
check("homework-1 i0: log|gap| is linear in t with slope -kappa, above or below theta",
      abs(-np.polyfit(tg, np.log(np.abs(0.05 - 0.03 * np.exp(-2 * tg) - 0.05)), 1)[0] - 2) < 1e-9)

print("\n%d passed, %d expected fails (findings), %d notes, %d unexpected fails" % (len(PASSES), len(XFAILS), len(NOTES), len(FAILS)))
for f in FAILS:
    print("UNEXPECTED: " + f)
sys.exit(1 if FAILS else 0)
