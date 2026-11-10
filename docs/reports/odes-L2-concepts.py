#!/usr/bin/env python3
"""Concept checks for odes level 2 (l6 to l9, review-2, homework-2).

Blind concept audit: docs/reviews/audit-odes-1-3.md. Exits 0 on correct content.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it is
reported, does not change the exit code, and carries the corrected assert in a
comment beside it.
"""
import sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

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
c1, c2, A, B = sp.symbols('c1 c2 A B', real=True)
y = sp.Function('y')


def L(expr, a, b, c):
    return sp.simplify(a * sp.diff(expr, t, 2) + b * sp.diff(expr, t) + c * expr)


# ---------------- l6 second-order ----------------
check("l6 s1 spring: every solution of y''=-y is c1 cos t + c2 sin t, with y(0)=c1, y'(0)=c2",
      sp.simplify(sp.dsolve(y(t).diff(t, 2) + y(t), y(t), ics={y(0): c1, y(t).diff(t).subs(t, 0): c2}).rhs - (c1 * sp.cos(t) + c2 * sp.sin(t))) == 0)
check("l6 s2 substitution: e^t and 5e^{2t} solve y''-3y'+2y=0; e^{3t} leaves 2, e^{-t} leaves 6",
      L(sp.exp(t), 1, -3, 2) == 0 and L(5 * sp.exp(2 * t), 1, -3, 2) == 0
      and sp.simplify(L(sp.exp(3 * t), 1, -3, 2) / sp.exp(3 * t)) == 2 and sp.simplify(L(sp.exp(-t), 1, -3, 2) / sp.exp(-t)) == 6)
check("l6 s4 superposition: c1 e^t + c2 e^{2t} solves it for any constants; y(0)=0, y'(0)=1 gives c1=-1, c2=1",
      L(c1 * sp.exp(t) + c2 * sp.exp(2 * t), 1, -3, 2) == 0 and sp.solve([c1 + c2, c1 + 2 * c2 - 1], [c1, c2]) == {c1: -1, c2: 1})
check("l6 s5 BVP many: y''+y=0, y(0)=0, y(pi)=0 is solved by every c sin t",
      L(c1 * sp.sin(t), 1, 0, 1) == 0 and (c1 * sp.sin(t)).subs(t, 0) == 0 and (c1 * sp.sin(t)).subs(t, sp.pi) == 0)
check("l6 s5/quiz1 BVP none: y(0)=0, y(pi)=1 has no solution", sp.solve([c1, -c1 - 1], [c1, c2]) == [])
check("l6 quiz1 BVP one: y(0)=0, y(pi/2)=1 has exactly one solution (none, one or many)",
      sp.solve([c1, c2 - 1], [c1, c2]) == {c1: 0, c2: 1})
W = sp.simplify(sp.Matrix([[sp.exp(t), sp.exp(2 * t)], [sp.exp(t), 2 * sp.exp(2 * t)]]).det())
check("l6 s7 wronskian: W(e^t, e^{2t}) = e^{3t}, 1 at t=0, never 0", sp.simplify(W - sp.exp(3 * t)) == 0)
check("l6 s7 wronskian of dependent pair e^{-2t}, e^{-2t} is 0",
      sp.simplify(sp.Matrix([[sp.exp(-2 * t), sp.exp(-2 * t)], [-2 * sp.exp(-2 * t), -2 * sp.exp(-2 * t)]]).det()) == 0)
p, q = sp.symbols('p q', real=True)
check("l6 s8 companion: char poly of [[0,1],[-q,-p]] is r^2+pr+q",
      sp.expand(sp.Matrix([[0, 1], [-q, -p]]).charpoly(sp.symbols('r')).as_expr() - (sp.symbols('r') ** 2 + p * sp.symbols('r') + q)) == 0)
x1 = 1000 * sp.exp(-t / 2) * (sp.cos(t) + sp.sin(t) / 2)
x2 = sp.exp(-t / 2) * (1000 * sp.cos(t) + 900 * sp.sin(t))
check("l6 s9 inventory: both curves solve x''+x'+1.25x=0 from 1000, with x'(0)=0 and 400",
      L(x1, 1, 1, sp.Rational(5, 4)) == 0 and L(x2, 1, 1, sp.Rational(5, 4)) == 0
      and sp.diff(x1, t).subs(t, 0) == 0 and sp.diff(x2, t).subs(t, 0) == 400 and x1.subs(t, 0) == x2.subs(t, 0) == 1000)
check("l6 quiz0: if y1, y2 solve y''+y=1 then y1+y2 solves y''+y=2 and y1-y2 the homogeneous one",
      L((1 + sp.cos(t)) + (1 + sp.sin(t)), 1, 0, 1) == 2 and L((1 + sp.cos(t)) - (1 + sp.sin(t)), 1, 0, 1) == 0)

# homework-2 i6 option: "two starting values y(0), y'(0) fix one solution" of y''+p(t)y'+q(t)y=g(t)
tp = sp.symbols('t', positive=True)
fam = c1 * tp ** 2
solves = sp.simplify(sp.diff(fam, tp, 2) - (2 / tp) * sp.diff(fam, tp) + (2 / tp ** 2) * fam) == 0
same_start = sp.limit(fam, tp, 0) == 0 and sp.limit(sp.diff(fam, tp), tp, 0) == 0
expected_fail("homework-2 i6 two_values_fix_one_solution for any p(t), q(t): y''-(2/t)y'+(2/t^2)y=0, y(0)=y'(0)=0",
              not (solves and same_start), "9")
# corrected assert: one solution when p, q and g are continuous on an interval containing the start (Boyce and DiPrima Thm 3.2.1)
check("homework-2 i6 corrected: with constant (continuous) coefficients the two starting values fix c1 and c2",
      len(sp.solve([c1 + c2 - 1, c1 + 2 * c2], [c1, c2])) == 2)

# ---------------- l7 characteristic equation ----------------
r = sp.symbols('r')
check("l7 s0: e^{rt} solves y''-3y'+2y=0 exactly when r^2-3r+2=0; bracket is -0.25 at 1.5 and 2 at 0",
      sp.solve(r ** 2 - 3 * r + 2, r) == [1, 2] and (r ** 2 - 3 * r + 2).subs(r, sp.Rational(3, 2)) == sp.Rational(-1, 4))
yr = (1 + 2 * t) * sp.exp(-2 * t)
check("l7 s2 repeated: (1+2t)e^{-2t} solves y''+4y'+4y=0, y(0)=1, y'(0)=0",
      L(yr, 1, 4, 4) == 0 and yr.subs(t, 0) == 1 and sp.diff(yr, t).subs(t, 0) == 0)
check("l7 s3: t e^{-2t} has y'=(1-2t)e^{-2t}, y''=(4t-4)e^{-2t}",
      sp.simplify(sp.diff(t * sp.exp(-2 * t), t) - (1 - 2 * t) * sp.exp(-2 * t)) == 0
      and sp.simplify(sp.diff(t * sp.exp(-2 * t), t, 2) - (4 * t - 4) * sp.exp(-2 * t)) == 0)
check("l7 s3 only_double_root: t e^{-2t} does not solve y''+5y'+6y=0 (root -2 single)", L(t * sp.exp(-2 * t), 1, 5, 6) != 0)
rr = sp.symbols('rho', real=True)
check("homework-2 i1: t e^{rt} solves y''-2ry'+r^2 y=0 for every r", L(t * sp.exp(rr * t), 1, -2 * rr, rr ** 2) == 0)
yc = sp.exp(-t) * (sp.cos(2 * t) + sp.sin(2 * t) / 2)
check("l7 s4-5 complex: roots of r^2+2r+5 are -1+-2i; e^{-t}(cos2t+0.5 sin2t) solves it with y(0)=1, y'(0)=0",
      set(sp.solve(r ** 2 + 2 * r + 5, r)) == {-1 + 2 * sp.I, -1 - 2 * sp.I} and L(yc, 1, 2, 5) == 0
      and yc.subs(t, 0) == 1 and sp.diff(yc, t).subs(t, 0) == 0)
z = sp.exp((-1 + 2 * sp.I) * t)
check("l7 s4 real_and_imaginary_parts each solve the real equation",
      L(sp.exp(-t) * sp.cos(2 * t), 1, 2, 5) == 0 and L(sp.exp(-t) * sp.sin(2 * t), 1, 2, 5) == 0
      and sp.simplify(sp.diff(z, t) - (-1 + 2 * sp.I) * z) == 0)
check("l7 s5 zero_crossing: first zero of the wave is at t=1.017, just after 1",
      abs(float((sp.pi - sp.atan(2)) / 2) - 1.0172) < 1e-4)
# l7 s5 explain: "The envelope e^{-t} bounds it throughout"
ts = np.linspace(0, 6, 60001)
wave = np.exp(-ts) * (np.cos(2 * ts) + 0.5 * np.sin(2 * ts))
expected_fail("l7 s5 envelope: |e^{-t}(cos2t+0.5 sin2t)| <= e^{-t} for all t", bool(np.all(np.abs(wave) <= np.exp(-ts) + 1e-12)), "5")
# corrected assert: the envelope is R e^{-t} with R = sqrt(c1^2+c2^2) = sqrt(5)/2
R = np.sqrt(1 + 0.25)
check("l7 s5 corrected: |y| <= (sqrt5/2) e^{-t}, touched once per half-turn; y(0.2318)=0.887 > e^{-0.2318}=0.793",
      bool(np.all(np.abs(wave) <= R * np.exp(-ts) + 1e-12)) and np.max(np.abs(wave) / np.exp(-ts)) > R - 1e-6
      and np.exp(-0.2318) * (np.cos(0.4636) + 0.5 * np.sin(0.4636)) > np.exp(-0.2318) + 0.09)
ts9 = np.linspace(0, 12, 120001)
wd = np.sqrt(3.75)
wave9 = np.exp(-0.5 * ts9) * (np.cos(wd * ts9) + 0.5 / wd * np.sin(wd * ts9))
expected_fail("l9 s2 envelope: the b=1 curve stays inside +-e^{-0.5t} as the chart draws it", bool(np.all(np.abs(wave9) <= np.exp(-0.5 * ts9) + 1e-12)), "5")
# corrected assert: envelope (1/sqrt(1-zeta^2)) e^{-0.5t} = 1.0328 e^{-0.5t}
check("l9 s2 corrected: |y| <= 1.0328 e^{-0.5t}", bool(np.all(np.abs(wave9) <= np.sqrt(1 + 0.25 / 3.75) * np.exp(-0.5 * ts9) + 1e-12)))
check("l7 s6 discriminant: r^2+br+4 has a complex pair for 0<=b<4, double root -2 at b=4, two real roots for b>4; |r|=2 while complex",
      sp.solve(r ** 2 + 4 * r + 4, r) == [-2] and all(abs(abs(complex(v)) - 2) < 1e-12 for v in sp.solve(r ** 2 + 1 * r + 4, r)))
y0, v0, al, be = sp.symbols('y_0 v_0 alpha beta', real=True, nonzero=True)
yf = sp.exp(al * t) * (y0 * sp.cos(be * t) + (v0 - al * y0) / be * sp.sin(be * t))
check("l7 s8 complex fit formula: y(0)=y0, y'(0)=v0", yf.subs(t, 0) == y0 and sp.simplify(sp.diff(yf, t).subs(t, 0) - v0) == 0)
yd = (y0 + (v0 - rr * y0) * t) * sp.exp(rr * t)
check("l7 s8 double-root fit formula", yd.subs(t, 0) == y0 and sp.simplify(sp.diff(yd, t).subs(t, 0) - v0) == 0 and L(yd, 1, -2 * rr, rr ** 2) == 0)
m, S = sp.symbols('m S', positive=True)
Vm = S ** m
ode = sp.simplify((sp.Rational(1, 2) * sp.Rational(4, 100) * S ** 2 * sp.diff(Vm, S, 2) + sp.Rational(5, 100) * S * sp.diff(Vm, S) - sp.Rational(5, 100) * Vm) / Vm)
ms = sp.symbols('m_', real=True)
check("l7 s9 perpetual put: S^m gives 0.02m(m-1)+0.05m-0.05=0, roots 1 and -2.5",
      set(sp.solve(sp.Rational(2, 100) * ms * (ms - 1) + sp.Rational(5, 100) * ms - sp.Rational(5, 100), ms)) == {1, sp.Rational(-5, 2)}
      and sp.simplify(ode - (sp.Rational(2, 100) * m * (m - 1) + sp.Rational(5, 100) * m - sp.Rational(5, 100))) == 0)
Sst, Kk = sp.symbols('S_star K', positive=True)
Vp = (Kk - Sst) * (S / Sst) ** sp.Rational(-5, 2)
smooth = sp.solve(sp.Eq(sp.diff(Vp, S).subs(S, Sst), -1), Sst)
check("l7 s9 exercise level: smooth pasting V'(S*)=-1 gives S* = K*2.5/3.5; V(S*)=K-S*; V->0 as S grows",
      sp.simplify(smooth[0] - Kk * sp.Rational(5, 7)) == 0 and Vp.subs(S, Sst) == Kk - Sst and sp.limit(Vp, S, sp.oo) == 0)
check("l7 s9 value: with S*=71.43 the optimal S* maximises V(100) (12.32)",
      abs(minimize_scalar(lambda s: -(100 - s) * (100 / s) ** -2.5, bounds=(1, 99), method='bounded').x - 500 / 7) < 1e-3)
check("l7 quiz0: y''+y'=0 has general solution c1+c2 e^{-t}", L(c1 + c2 * sp.exp(-t), 1, 1, 0) == 0)

# ---------------- l8 forcing ----------------
yg = c1 * sp.exp(-t) + c2 * sp.exp(-2 * t) + 2
check("l8 s0-1: c1 e^{-t}+c2 e^{-2t}+2 solves y''+3y'+2y=4 and tends to 2", L(yg, 1, 3, 2) == 4 and sp.limit(yg, t, sp.oo) == 2)
check("l8 s2: e^{3t}/20 solves y''+3y'+2y=e^{3t}", sp.simplify(L(sp.exp(3 * t) / 20, 1, 3, 2) - sp.exp(3 * t)) == 0)
check("l8 s3: -3cos t+sin t solves y''+3y'+2y=10 sin t", sp.simplify(L(-3 * sp.cos(t) + sp.sin(t), 1, 3, 2) - 10 * sp.sin(t)) == 0)
yi = 5 * sp.exp(-t) - 2 * sp.exp(-2 * t) - 3 * sp.cos(t) + sp.sin(t)
check("l8 s4-5 IVP: 5e^{-t}-2e^{-2t}-3cos t+sin t starts at rest; fitting y_h first leaves y(0)=-3",
      sp.simplify(L(yi, 1, 3, 2) - 10 * sp.sin(t)) == 0 and yi.subs(t, 0) == 0 and sp.diff(yi, t).subs(t, 0) == 0
      and (-3 * sp.cos(t) + sp.sin(t)).subs(t, 0) == -3)
check("l8 s6: A e^{-t} gives 0; t e^{-t} solves y''+3y'+2y=e^{-t}",
      L(A * sp.exp(-t), 1, 3, 2) == 0 and sp.simplify(L(t * sp.exp(-t), 1, 3, 2) - sp.exp(-t)) == 0)
w = sp.symbols('omega', positive=True)
gp = A * sp.cos(w * t) + B * sp.sin(w * t)
res = sp.expand(sp.diff(gp, t, 2) + p * sp.diff(gp, t) + q * gp)
M = sp.Matrix([[q - w ** 2, p * w], [-p * w, q - w ** 2]])
check("l8 s7/s9 matrix: cos and sin parts give [[q-w^2, pw],[-pw, q-w^2]](A,B)",
      sp.simplify(res.coeff(sp.cos(w * t)) - (M[0, 0] * A + M[0, 1] * B)) == 0 and sp.simplify(res.coeff(sp.sin(w * t)) - (M[1, 0] * A + M[1, 1] * B)) == 0)
check("l8 s7 determinant (q-w^2)^2+p^2w^2 vanishes (w>0) only for p=0 and q=w^2",
      sp.simplify(M.det() - ((q - w ** 2) ** 2 + p ** 2 * w ** 2)) == 0 and M.subs({p: 0, q: 4, w: 2}) == sp.zeros(2, 2))
check("l8 s8: t-1.5 solves y''+3y'+2y=2t", sp.simplify(L(t - sp.Rational(3, 2), 1, 3, 2) - 2 * t) == 0)
ze, om = sp.symbols('zeta omega_', positive=True)
check("l8 s10 trend lag: 100+t-2zeta/omega solves y''+2 zeta w y'+w^2 y = w^2(100+t)",
      sp.simplify(L(100 + t - 2 * ze / om, 1, 2 * ze * om, om ** 2) - om ** 2 * (100 + t)) == 0)
smo = solve_ivp(lambda tt, v: [v[1], 0.25 * (100 + tt) - 1.0 * v[1] - 0.25 * v[0]], (0, 20), [100.0, 0.0], rtol=1e-10, atol=1e-12)
check("l8 s10 chart: with zeta=1, omega=0.5 the gap is 4.00 by day 20 (integration from y=100 at rest)", abs((120 - smo.y[0, -1]) - 4) < 0.005)
check("l8 quiz2: t e^t/2 solves y''-y=e^t (A = 1/2 at a single root)", sp.simplify(L(t * sp.exp(t) / 2, 1, 0, -1) - sp.exp(t)) == 0)
check("homework-2 i3: -t e^t solves y''-3y'+2y=e^t", sp.simplify(L(-t * sp.exp(t), 1, -3, 2) - sp.exp(t)) == 0)
# homework-2 i3 byKey.half: "A half appears only for a double root"
half_at_single_root = sp.simplify(L(t * sp.exp(t) / 2, 1, 0, -1) - sp.exp(t)) == 0 and sp.solve(r ** 2 - 1, r) == [-1, 1]
expected_fail("homework-2 i3 half_only_double_root: no single-root case has A = 1/2", not half_at_single_root, "7")
# corrected assert: at a single root r of P, y_p = t e^{rt}/P'(r); at a double root, t^2 e^{rt}/P''(r)
check("homework-2 i3 corrected: A = 1/P'(r) at a single root: y''-y gives 1/2, y''-3y'+2y gives -1; double root y''-2y'+y gives t^2 e^t/2",
      sp.Rational(1, 2) == 1 / sp.diff(r ** 2 - 1, r).subs(r, 1) and -1 == 1 / sp.diff(r ** 2 - 3 * r + 2, r).subs(r, 1)
      and sp.simplify(L(t ** 2 * sp.exp(t) / 2, 1, -2, 1) - sp.exp(t)) == 0)
# l8 s8 rule: "If the guess solves the homogeneous equation, multiply it by t."
a_, b_ = sp.symbols('a b', real=True)
plain = sp.solve(sp.Poly(sp.expand(L(a_ * t + b_, 1, 1, 0) - t), t).coeffs(), [a_, b_])
guess_is_homogeneous = L(a_ * t + b_, 1, 1, 0) == 0  # the guess at+b as a whole does not solve y''+y'=0
expected_fail("l8 s8 rule on y''+y'=t: the guess at+b does not solve the homogeneous equation, so the rule says use it as it stands, and it should work",
              (not guess_is_homogeneous) and plain not in ([], {}), "6")
# corrected assert: multiply by t when ANY TERM of the guess is homogeneous (here the constant b), and by t again at a double root
fix = sp.solve(sp.Poly(sp.expand(L(t * (a_ * t + b_), 1, 1, 0) - t), t).coeffs(), [a_, b_])
check("l8 s8 corrected: t(at+b) works for y''+y'=t with a=1/2, b=-1", fix == {a_: sp.Rational(1, 2), b_: -1})
once = sp.solve(sp.simplify((L(A * t * sp.exp(t), 1, -2, 1) - sp.exp(t)) / sp.exp(t)), A)
expected_fail("l8 s8 rule on y''-2y'+y=e^t: one factor of t is enough", once != [], "6")
check("l8 s8 corrected: the double root needs t^2: A t^2 e^t with A=1/2", sp.solve(sp.simplify((L(A * t ** 2 * sp.exp(t), 1, -2, 1) - sp.exp(t)) / sp.exp(t)), A) == [sp.Rational(1, 2)])

# ---------------- l9 damping and resonance ----------------
def free(b, tmax=40, n=400001):
    tt = np.linspace(0, tmax, n)
    s = solve_ivp(lambda u, v: [v[1], -b * v[1] - 4 * v[0]], (0, tmax), [1.0, 0.0], t_eval=tt, rtol=1e-11, atol=1e-13)
    return tt, s.y[0]


def settle(b, band=0.05):
    tt, yy = free(b)
    out = np.where(np.abs(yy) >= band)[0]
    return tt[out[-1]]


tt_ = np.linspace(0, 40, 400001)
over = lambda b: (lambda s_: np.exp(-b * tt_ / 2) * (np.cosh(s_ * tt_) + (b / 2) / s_ * np.sinh(s_ * tt_)))(np.sqrt(b * b / 4 - 4))
check("l9 s0 crossing: from rest at 1 the curve goes below zero only when b<4 (first trough -exp(-zeta pi/sqrt(1-zeta^2)) < 0 for every zeta<1; closed forms positive for b>=4)",
      all(free(b)[1].min() < -1e-4 for b in (0.5, 1, 2, 3)) and np.exp(-0.975 * np.pi / np.sqrt(1 - 0.975 ** 2)) > 0
      and bool(np.all((1 + 2 * tt_) * np.exp(-2 * tt_) > 0)) and all(bool(np.all(over(b) > 0)) for b in (4.1, 5, 6, 8)))
st = {b: settle(b) for b in (1, 3, 4, 5, 8)}
check("l9 s4 table: settling times 1.56 (b=3), 2.37 (b=4), 3.28 (b=5); b=3 soonest, b=8 slowest of the five",
      abs(st[3] - 1.56) < 0.01 and abs(st[4] - 2.37) < 0.01 and abs(st[5] - 3.28) < 0.01 and min(st, key=st.get) == 3 and max(st, key=st.get) == 8)
check("l9 s4 b=3 overshoot is 2.8%, inside the band", abs(-free(3)[1].min() - np.exp(-0.75 * np.pi / np.sqrt(1 - 0.75 ** 2))) < 1e-6 and -free(3)[1].min() < 0.05)
grid = np.arange(4.0, 9.01, 0.25)
times = [settle(b) for b in grid]
check("l9 s4/s6/summary critical_fastest_without_overshoot: among b>=4 (no overshoot) the settling time is smallest at b=4 and rises with b",
      int(np.argmin(times)) == 0 and bool(np.all(np.diff(times) > 0)))
check("l9 s6: b=5 solution is (4e^{-t}-e^{-4t})/3 from rest", L((4 * sp.exp(-t) - sp.exp(-4 * t)) / 3, 1, 5, 4) == 0
      and sp.diff((4 * sp.exp(-t) - sp.exp(-4 * t)) / 3, t).subs(t, 0) == 0)
check("l9 s2 period: 2pi/sqrt(3.75)=3.2446, longer than pi; shrink per period 0.197",
      abs(2 * np.pi / np.sqrt(3.75) - 3.2446) < 5e-5 and abs(np.exp(-0.5 * 2 * np.pi / np.sqrt(3.75)) - 0.197) < 5e-4)
# step response overshoot formula, by integration
for zeta in (0.25, 0.5):
    s = solve_ivp(lambda u, v: [v[1], 4 - 4 * zeta * v[1] - 4 * v[0]], (0, 20), [0.0, 0.0], max_step=1e-3, rtol=1e-10, atol=1e-12)
    check("l9 s5 / review-2 i6 overshoot zeta=%.2f: peak - 1 = exp(-zeta pi/sqrt(1-zeta^2))" % zeta,
          abs(s.y[0].max() - 1 - np.exp(-zeta * np.pi / np.sqrt(1 - zeta ** 2))) < 1e-5)
for zeta in (1.0, 1.25, 2.0):
    s = solve_ivp(lambda u, v: [v[1], 4 - 4 * zeta * v[1] - 4 * v[0]], (0, 40), [0.0, 0.0], max_step=1e-2, rtol=1e-10, atol=1e-12)
    check("l9 s10 no overshoot for zeta=%.2f" % zeta, s.y[0].max() <= 1 + 1e-9)
t90 = {}
for zeta in (1.0, 1.25):
    s = solve_ivp(lambda u, v: [v[1], 4 - 4 * zeta * v[1] - 4 * v[0]], (0, 40), [0.0, 0.0], max_step=1e-3, rtol=1e-10, atol=1e-12)
    t90[zeta] = s.t[np.argmax(s.y[0] >= 0.9)]
check("l9 s10: zeta=1 reaches 90% of the level sooner than zeta=1.25", t90[1.0] < t90[1.25])
yres = t * sp.sin(2 * t) / 4
check("l9 s7 resonance: (t/4) sin 2t solves y''+4y=cos 2t; amplitude t/4 unbounded",
      sp.simplify(L(yres, 1, 0, 4) - sp.cos(2 * t)) == 0)
check("review-2 i4: -(t/6)cos 3t solves y''+9y=sin 3t", sp.simplify(L(-t * sp.cos(3 * t) / 6, 1, 0, 9) - sp.sin(3 * t)) == 0)
# steady amplitude and where it peaks: NOT at the natural frequency
amp = lambda om_, b=1.0, w0=2.0: 1 / np.sqrt((w0 ** 2 - om_ ** 2) ** 2 + (b * om_) ** 2)
pk = minimize_scalar(lambda o: -amp(o), bounds=(0.1, 4), method='bounded', options={'xatol': 1e-10}).x
check("l9 s8 damped peak: at 2 sqrt(1-2 zeta^2)=1.8708 (below the natural 2), amplitude 0.5164 > 0.5 at omega=2",
      abs(pk - 1.8708) < 1e-4 and abs(amp(pk) - 0.5164) < 5e-5 and amp(pk) > amp(2.0) == 0.5)
# simulate the forced equation and measure the steady amplitude
s = solve_ivp(lambda u, v: [v[1], np.cos(1.0 * u) - v[1] - 4 * v[0]], (0, 80), [0.0, 0.0], t_eval=np.linspace(60, 80, 20001), rtol=1e-10, atol=1e-12)
check("l9 s8/quiz3 steady amplitude at omega=1 is 1/sqrt(10) (simulation)", abs(np.abs(s.y[0]).max() - 10 ** -0.5) < 1e-4)
pk2 = minimize_scalar(lambda o: -amp(o, b=0.4), bounds=(0.1, 4), method='bounded', options={'xatol': 1e-10}).x
check("homework-2 i4: zeta=0.1 peak at omega^2=3.92, amplitude 1.2563, against 1.25 at omega=2",
      abs(pk2 ** 2 - 3.92) < 1e-5 and abs(amp(pk2, b=0.4) - 1.2563) < 5e-5 and abs(amp(2.0, b=0.4) - 1.25) < 1e-12)
check("l9 quiz1 negative damping: roots of r^2-0.5r+4 have real part +0.25",
      all(abs(sp.re(v) - sp.Rational(1, 4)) == 0 for v in sp.solve(r ** 2 - sp.Rational(1, 2) * r + 4, r)))
check("l9 s1 zeta: b/(2 w0) = 1 exactly where the discriminant b^2-4w0^2 is 0", sp.solve(sp.Eq(sp.symbols('b_', positive=True) ** 2 - 16, 0)) == [4])
zz, ww = sp.symbols('zeta w', positive=True)
st_over = lambda r1, r2: 1 + (r2 * sp.exp(r1 * t) - r1 * sp.exp(r2 * t)) / (r1 - r2)
so = st_over(-1, -4)
check("homework-2 i0 over-damped step formula: 0 with slope 0 at t=0 and solves y''+5y'+4y=4",
      so.subs(t, 0) == 0 and sp.diff(so, t).subs(t, 0) == 0 and sp.simplify(L(so, 1, 5, 4) - 4) == 0)
sc = 1 - (1 + ww * t) * sp.exp(-ww * t)
check("homework-2 i0/i7 critical step: 1-(1+wt)e^{-wt} solves y''+2wy'+w^2y=w^2 from rest and never exceeds 1",
      sp.simplify(L(sc, 1, 2 * ww, ww ** 2) - ww ** 2) == 0 and sc.subs(t, 0) == 0 and sp.simplify(sp.diff(sc, t) - ww ** 2 * t * sp.exp(-ww * t)) == 0)
check("homework-2 i7: peak time pi/(omega sqrt(1-zeta^2)) = 6.49 days; lags 1 and 4 days",
      abs(np.pi / (0.5 * np.sqrt(1 - 0.0625)) - 6.49) < 0.005 and 2 * 0.25 / 0.5 == 1 and 2 * 1 / 0.5 == 4)
check("review-2 i8: cosh 2t solves y''-4y=0 from (1, 0)", L(sp.cosh(2 * t), 1, 0, -4) == 0)
check("homework-2 i5: slow root -0.5 needs b=8.5; other root -8", sp.solve(r ** 2 + sp.Rational(17, 2) * r + 4, r) == [-8, sp.Rational(-1, 2)])

print("\n%d passed, %d expected fails (findings), %d unexpected fails" % (len(PASSES), len(XFAILS), len(FAILS)))
for f in FAILS:
    print("UNEXPECTED: " + f)
sys.exit(1 if FAILS else 0)
