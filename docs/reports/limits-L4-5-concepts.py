#!/usr/bin/env python3
"""Concept checks for limits L4 and L5 (blind audit limits-4-5, round 1).

Recomputes every stated number, key, slip value and rule in
l13 to l20, review-4/5, homework-4/5, problems-4/5 and fluency-l13 with
sympy, NumPy and SciPy, and brute-forces the four fluency families over
their whole variable range. Exits 0 when every check passes. A check
named FINDING n fails because the content is wrong; it stays failing
until the content is fixed.

Run: python docs/reports/limits-L4-5-concepts.py   (from the repo root)
"""
import itertools
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import stats

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "app", "content", "courses", "limits")
FAIL, N = [], 0


def check(name, cond):
    global N
    N += 1
    if not cond:
        FAIL.append(name)
        print("FAIL", name)


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol


def load(name):
    with open(os.path.join(ROOT, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


x, y, t, s, q, r, u, w, f, L = sp.symbols("x y t s q r u w f L", real=True)

# ---------------------------------------------------------------- l13
g = x**3 - 6*x**2 + 9*x + 1
f0 = x**3 - 3*x
check("l13 s0 slopes", sp.diff(f0, x).subs(x, -1.5) == 3.75 and sp.diff(f0, x).subs(x, -0.5) == -2.25)
check("l13 s1 flat at +-1", set(sp.solve(sp.diff(f0, x), x)) == {-1, 1})
check("l13 s1 slopes A C E", [sp.diff(f0, x).subs(x, v) for v in (-2, 0, 2)] == [9, -3, 9])
check("l13 s2 stationary", set(sp.solve(sp.diff(g, x), x)) == {1, 3} and g.subs(x, 1) == 5 and g.subs(x, 3) == 1)
check("l13 s3 slopes", sp.diff(g, x).subs(x, sp.Rational(1, 2)) == sp.Rational(15, 4)
      and sp.diff(g, x).subs(x, sp.Rational(3, 2)) == -sp.Rational(9, 4))
check("l13 s4 g''", sp.diff(g, x, 2).subs(x, 3) == 6 and sp.diff(g, x, 2).subs(x, 1) == -6)
check("l13 s6 ends", [g.subs(x, v) for v in (0, 1, 3, 5)] == [1, 5, 1, 21])
V = sp.Rational(4, 100)*w**2 + sp.Rational(9, 100)*(1 - w)**2
wst = sp.solve(sp.diff(V, w), w)[0]
check("l13 s9 w*", wst == sp.Rational(9, 13) and close(V.subs(w, wst), 0.02769, 1e-5)
      and close(sp.sqrt(V.subs(w, wst)), 0.166, 5e-4))
check("l13 s9 slips", close(sp.diff(V, w).subs(w, 1), 0.08, 1e-12) and close(V.subs(w, 0.5), 0.0325, 1e-12)
      and close(sp.diff(V, w).subs(w, 0.5), -0.05, 1e-12) and close((1/0.2)/(1/0.2 + 1/0.3), 0.6, 1e-12))
check("l13 q0", sp.diff(x**3 - 12*x, x, 2).subs(x, -2) == -12 and (x**3 - 12*x).subs(x, -2) == 16)
fq = x**4 - 4*x**3
check("l13 q1", sp.expand(sp.diff(fq, x) - 4*x**2*(x - 3)) == 0 and sp.diff(fq, x, 2).subs(x, 3) == 36
      and sp.diff(fq, x).subs(x, -0.1) < 0 and sp.diff(fq, x).subs(x, 0.1) < 0)
check("l13 q2", [(x**2 - 4*x).subs(x, v) for v in (0, 2, 5)] == [0, -4, 5])
check("l13 q3", sp.solve(sp.diff(x*sp.exp(-x), x), x) == [1] and close(sp.exp(-1), 0.3679, 5e-5))
# l13 s8 d2: f''(a) > 0 at one point does not make f' increasing NEAR a.
# f'(x) = x/2 + x^2 sin(1/x), f'(0) = 0, f''(0) = 1/2, yet f'' < 0 arbitrarily near 0.
xs = 1/(2*np.pi*np.arange(1, 2000))          # cos(1/x) = 1 there
fpp = 0.5 + 2*xs*np.sin(1/xs) - np.cos(1/xs)
check("l13 s8 note: f''(a)>0 does not give f' monotone near a (imprecise)", np.all(fpp < 0))

# ---------------------------------------------------------------- l14
A = w*(40 - 2*w)
check("l14 s0", sp.solve(sp.diff(A, w), w) == [10] and A.subs(w, 10) == 200
      and close(A.subs(w, sp.Rational(40, 3)), 177.8, 0.05))
Vb = x*(30 - 2*x)**2
check("l14 s2", sp.simplify(sp.diff(Vb, x) - (30 - 2*x)*(30 - 6*x)) == 0 and Vb.subs(x, 5) == 2000
      and Vb.subs(x, sp.Rational(15, 2)) == sp.Rational(3375, 2))
S = x**2 + 128000/x
check("l14 s4", sp.solve(sp.diff(S, x), x) == [40] and S.subs(x, 40) == 4800
      and sp.diff(S, x, 2).subs(x, 40) == 6 and close(128000**(1/3), 50.4, 0.01))
check("l14 s6", A.subs(w, 12) == 192)
check("l14 s8", sp.solve(sp.diff(w*(L - 2*w), w), w) == [L/4]
      and sp.simplify((w*(L - 2*w)).subs(w, L/4) - L**2/8) == 0)
G = sp.Rational(6, 10)*sp.log(1 + f) + sp.Rational(4, 10)*sp.log(1 - f)
check("l14 s9 kelly", sp.solve(sp.diff(G, f), f) == [sp.Rational(1, 5)]
      and close(G.subs(f, 0.2), 0.020136, 1e-6) and close(G.subs(f, 0.05), 0.008757, 1e-6)
      and G.subs(f, 0.6) < 0 and G.subs(f, 0.4) < 0 and sp.diff(G, f).subs(f, 0.3) < 0)
p_, b_ = sp.symbols("p b", positive=True)
Gg = p_*sp.log(1 + b_*f) + (1 - p_)*sp.log(1 - f)
check("l14 kelly general", sp.simplify(sp.solve(sp.diff(Gg, f), f)[0] - (p_ - (1 - p_)/b_)) == 0)
pi_ = sp.Rational(5, 100)*q - sp.Rational(2, 10**6)*q**2
check("l14 q1", sp.solve(sp.diff(pi_, q), q) == [12500] and pi_.subs(q, 12500) == sp.Rational(625, 2)
      and pi_.subs(q, 25000) == 0)
check("l14 q2", close(0.55 - 0.45/2, 0.325, 1e-12) and close(0.55*2 - 0.45, 0.65, 1e-12))
C = x + 100/x
check("l14 q3", C.subs(x, 5) == 25 and C.subs(x, 1) == 101 and C.subs(x, 10) == 20)
check("l14 q0", (w*(60 - 2*w)).subs(w, 15) == 450)

# ---------------------------------------------------------------- l15
P = sum(4/(1 + y)**k for k in range(1, 6)) + 100/(1 + y)**5
Pf = sp.lambdify(y, P)
dP = sp.lambdify(y, sp.diff(P, y))
d2P = sp.lambdify(y, sp.diff(P, y, 2))
for yy, pv in ((0.02, 109.4269), (0.05, 95.6705), (0.06, 91.5753), (0.08, 84.0292), (0.10, 77.2553)):
    check(f"l15 P({yy})", close(Pf(yy), pv, 6e-5))
check("l15 slopes", close(dP(0.02), -498.7, 0.05) and close(dP(0.10), -321.0, 0.05) and close(dP(0.05), -420.98, 0.005))
check("l15 s1", close(Pf(0.05) - Pf(0.06), 4.0953, 5e-5) and close(4.0953/95.6705, 0.043, 5e-4))
check("l15 s3", close(dP(0.05)*0.01, -4.2098, 5e-5) and close(4.2098 - 4.0953, 0.11, 0.005))
tan08 = Pf(0.05) + dP(0.05)*0.03
check("l15 s4", close(tan08, 83.0411, 1e-4) and close(Pf(0.08) - tan08, 0.988, 1e-3)
      and close(3*(4.2098 - 4.0953), 0.34, 0.005))
check("l15 s5", close(Pf(0.05) - Pf(0.08), 11.64, 0.005) and close(Pf(0.02) - Pf(0.05), 13.76, 0.005)
      and close(Pf(0.05) - dP(0.05)*0.03, 108.30, 0.005))
D = -dP(0.05)/Pf(0.05)
cf = [4, 4, 4, 4, 104]
mac = sum((k + 1)*c/1.05**(k + 1) for k, c in enumerate(cf))/Pf(0.05)
check("l15 s6/s7", close(D, 4.40, 0.005) and close(mac, 4.62, 0.005) and close(mac/1.05, D, 1e-9))
check("l15 s8", close((Pf(0.051)/Pf(0.05) - 1)*1e6, -4388, 1) and close(D*100, 440, 0.5))
check("l15 s9", close(-100000/1.25**2*0.01, -640, 1e-9) and close(100000/1.26 - 80000, -634.92, 0.005))
check("l15 q3", close(-200000/1.15**2, -151228.73, 0.005) and close(-200000/1.15**2*0.02, -3024.57, 0.005)
      and close(-200000/1.15*0.02, -3478.26, 0.005))
check("l15 convex", all(d2P(v) > 0 for v in np.linspace(0, 0.5, 200)))
check("hw4 second-order", close(d2P(0.05), 2341.29, 0.005)
      and close(95.6705 - 12.6294 + 0.5*2341.29*0.0009, 84.09, 0.005)
      and close(95.67 - 12.63 + 2341.29*0.0009, 85.15, 0.006))

# ---------------------------------------------------------------- l16
check("l16 table", close(math.sin(0.1)/0.1, 0.998334, 5e-7) and close((math.exp(0.1) - 1)/0.1, 1.051709, 5e-7)
      and close((math.exp(-0.1) - 1)/-0.1, 0.951626, 5e-7) and close((math.exp(0.01) - 1)/0.01, 1.005017, 5e-7)
      and close((math.exp(-0.01) - 1)/-0.01, 0.995017, 5e-7) and close(math.sin(0.01)/0.01, 0.999983, 5e-7))
check("FINDING 1: l16 s0 hint 'both columns within 0.005 of 1 at x = +-0.01'",
      max(abs((math.exp(0.01) - 1)/0.01 - 1), abs((math.exp(-0.01) - 1)/-0.01 - 1)) <= 0.005)
rat = lambda h: (math.exp(2*h) - 1)/math.sin(h)
check("l16 s1", close(rat(0.5), 3.58, 0.005) and close(rat(0.1), 2.22, 0.005) and close(rat(0.01), 2.020, 0.0005))
lims = [((x**2 - 4)/(x - 2), 2, 4), ((sp.exp(3*x) - 1)/sp.sin(2*x), 0, sp.Rational(3, 2)),
        ((1 - sp.cos(x))/x**2, 0, sp.Rational(1, 2)), (sp.log(x)/x, sp.oo, 0),
        ((x + sp.cos(x))/(x + 2), 0, sp.Rational(1, 2)), (sp.sin(x)/(x**2 + x), 0, 1),
        (sp.log(x)/x, 1, 0), (sp.exp(x)/(x + 1), 0, 1), ((sp.exp(4*x) - 1)/x, 0, 4),
        ((x**2 - 9)/(x - 3), 3, 6), ((sp.exp(x) + x)/(sp.exp(x) + 1), 0, sp.Rational(1, 2)),
        ((sp.exp(sp.Rational(6, 100)*x) - 1)/x, 0, sp.Rational(6, 100)), (sp.sin(5*x)/x, 0, 5),
        ((1 - sp.cos(2*x))/x**2, 0, 2), ((x - sp.sin(x))/x**3, 0, sp.Rational(1, 6))]
for i, (e, a, v) in enumerate(lims):
    check(f"l16/review/hw limit {i}", sp.limit(e, x, a) == v)
check("l16 s6 misuse gives 1", (sp.diff(x + sp.cos(x), x)/sp.diff(x + 2, x)).subs(x, 0) == 1)
check("l16 q2 misuse gives 2", (sp.diff(sp.exp(x) + x, x)/sp.diff(sp.exp(x) + 1, x)).subs(x, 0) == 2)
check("l16 s7 cos x / x has no limit", sp.limit(sp.cos(x)/x, x, 0, "+") == sp.oo and sp.limit(sp.cos(x)/x, x, 0, "-") == -sp.oo)
# summary.trap 'gives a wrong answer' is too strong: (x+1)/(2x+2) at 0 is not 0/0, the rule still gives 1/2.
check("l16 trap note: misuse can be right by accident (imprecise)",
      sp.limit((x + 1)/(2*x + 2), x, 0) == sp.Rational(1, 2) and sp.diff(x + 1, x)/sp.diff(2*x + 2, x) == sp.Rational(1, 2))
check("l16 s5", close(math.log(100)/100, 0.04605, 5e-6) and close(math.log(1e6), 13.8, 0.05)
      and close(math.log(1e6)/1e6, 0.0000138, 5e-8))
for n, v in ((1, 1050.00), (2, 1050.63), (4, 1050.95), (12, 1051.16)):
    check(f"l16 s9 n={n}", close(1000*(1 + 0.05/n)**n, v, 0.0051))
check("l16 s9 limit", close(1000*math.exp(0.05), 1051.27, 0.005)
      and sp.limit(sp.log(1 + sp.Rational(5, 100)*u)/u, u, 0) == sp.Rational(5, 100))
check("review4 r9", close(math.exp(0.1), 1.10517, 5e-6))
check("hw4 xlnx", sp.limit(x*sp.log(x), x, 0, "+") == 0 and close(0.001*math.log(0.001), -0.0069, 5e-5))

# ---------------------------------------------------------------- l17
price = 100 + 2*x + sp.Rational(8, 10)*sp.sin(2*sp.pi*x/3)
check("l17 s0", sp.diff(price, x).subs(x, sp.Rational(3, 4)) == 2 and sp.diff(price, x).subs(x, sp.Rational(9, 4)) == 2
      and close(price.subs(x, 0.75), 102.3, 1e-9) and close(price.subs(x, 2.25), 103.7, 1e-9)
      and close(price.subs(x, 0.2), 100.7254, 5e-5))
check("l17 s1", sp.diff(f0, x).subs(x, sp.sqrt(3)) == 6 and f0.subs(x, sp.sqrt(3)) == 0)
c = 2/sp.sqrt(3)
check("l17 s3", sp.diff(f0, x).subs(x, c) == 1 and close(c, 1.1547, 5e-5) and close(f0.subs(x, c), -1.9245, 5e-5)
      and close(sp.sqrt(sp.Rational(1, 3)), 0.5774, 5e-5))
check("l17 s7 key", 5 + 3*(3 - 1) == 11 and 5 - 3*2 == -1)
dbl = [v for v in load("l17-somewhere-in-between")["screens"][7]["widget"]["wrong"] if v["id"] == "double"][0]
check("FINDING 2: l17 s7 slip 'double' value is 5 + 3*3 (the full 3 units from x = 0)", dbl["value"] == 5 + 3*3)
check("l17 s8", sp.diff(f0, x).subs(x, 1) == 0 and sp.diff(f0, x).subs(x, 0) == -3)
check("l17 s8 parabola midpoint", sp.simplify(sp.diff(x**2, x).subs(x, (s + t)/2) - (t**2 - s**2)/(t - s)) == 0)
check("l17 q0", close(sp.sqrt(sp.Rational(13, 3)), 2.0817, 5e-5) and 3*2**2 == 12)
for fn in (x**2, sp.sin(x), sp.exp(x)):
    m = (fn.subs(x, 2) - fn.subs(x, 0))/2
    root = sp.nsolve(sp.diff(fn, x) - m, x, 1)
    check(f"l17 q1 {fn} has c", 0 < root < 2)
check("l17 q3", 1 + 2*4 == 9)
# MVT hypotheses: 'continuous, no gaps' alone does not give a moment at the average rate.
# P&L rising 2,000 -> 2,900 over 6 h at 100 an hour then 200 an hour: continuous, never 150.
tt = np.linspace(0, 6, 60001)
pnl = np.where(tt <= 3, 2000 + 100*tt, 2300 + 200*(tt - 3))
rates = np.diff(pnl)/np.diff(tt)
check("l17 q2/s4 note: continuity alone is not enough (imprecise)",
      close(pnl[0], 2000, 1e-9) and close(pnl[-1], 2900, 1e-9) and not np.any(np.isclose(rates, 150, atol=1)))
check("review5 r0", sp.diff(1/x, x).subs(x, 2) == -sp.Rational(1, 4) and close(-1/2.5**2, -0.16, 1e-12))
check("hw5 sqrt101", close(1/(2*math.sqrt(101)), 0.04975, 5e-6) and close(math.sqrt(101) - 10, 0.049876, 5e-7))

# ---------------------------------------------------------------- l18
top = lambda tm: math.sqrt(25 - (0.5*tm)**2)
check("l18 s0", close(top(5), 4.330, 5e-4) and close(top(7), 3.571, 5e-4) and close(top(5.8), 4.073, 5e-4)
      and close(top(6.2), 3.923, 5e-4) and close((top(5.8) - top(6.2))/0.4, 0.375, 1e-3) and close(top(2), 4.899, 5e-4))
check("l18 s2", -3*0.5/4 == -0.375 and close(-4*0.5/3, -0.6667, 5e-5))
check("l18 s3", -50*20 + 1000*0.01 == -990)
check("l18 s4", close(0.004/(2*0.2), 0.01, 1e-12) and close(0.004/0.2, 0.02, 1e-12) and close(0.004/(2*0.04), 0.05, 1e-12))
check("l18 s5", close(100*1.04**-5, 82.19, 0.005) and close(-500*1.04**-6, -395.16, 0.005)
      and close(-500*1.04**-6*0.0002, -0.0790, 5e-5))
check("l18 s6/s7", close(-5/12, -0.4167, 5e-5) and close(-math.sqrt(25 - 0.01)*0.5/0.1, -25, 0.01))
check("l18 s10", close(-7*1e7*0.0003, -21000, 1e-6))
check("l18 quiz", close(40*math.pi, 125.66, 0.005) and -6*1.5/8 == -1.125 and close(0.006/0.6, 0.01, 1e-12))
check("review5 rates", -100*95 + 10000*-0.20 == -11500 and close(-12*300/13, -276.92, 0.005) and -13*300/12 == -325)
check("hw5 cone", close(2/(math.pi*16/4), 0.1592, 5e-5) and close(2/(3*math.pi*16/4), 0.0531, 5e-5)
      and close(math.pi*16/(4*2), 6.2832, 5e-5))
T_ = sp.solve(sp.Eq(t/5, (t - x)/sp.Rational(18, 10)), t)[0]
check("hw5 shadow", sp.simplify(T_ - 5*x/sp.Rational(32, 10)) == 0 and close(5/3.2*1.2, 1.875, 1e-12)
      and close(5/3.2*1.2 - 1.2, 0.675, 1e-12))
check("hw5 risk", close(-(0.08*0.3*0.01)/(0.02*0.4), -0.03, 1e-12) and close(0.04*0.09 + 0.01*0.16, 0.0052, 1e-12)
      and close(-(0.02*0.4)/(0.08*0.3)*0.01, -0.0033, 5e-5))

# ---------------------------------------------------------------- l19
fi = x**3 + x
check("l19 s1/s2", sp.diff(fi, x).subs(x, 1) == 4 and fi.subs(x, 2) == 10 and sp.diff(fi, x).subs(x, 2) == 13
      and sp.diff(fi, x).subs(x, 10) == 301)
# numeric inverse slope
inv = lambda yv: float(sp.nsolve(fi - yv, x, 1))
check("l19 s1 numeric", close((inv(2.0001) - inv(1.9999))/0.0002, 0.25, 1e-6))
check("l19 arctan", sp.simplify(sp.diff(sp.atan(x), x) - 1/(1 + x**2)) == 0 and sp.sec(sp.pi/4)**2 == 2)
check("l19 arcsin", sp.simplify(sp.diff(sp.asin(x), x) - 1/sp.sqrt(1 - x**2)) == 0 and close(1/math.sqrt(1.36), 0.8575, 5e-5)
      and close(1/0.64, 1.5625, 1e-12) and sp.simplify(sp.diff(sp.acos(x), x) + 1/sp.sqrt(1 - x**2)) == 0)
check("l19 s7", sp.simplify(sp.diff(sp.atan(2*x), x) - 2/(1 + 4*x**2)) == 0)
check("l19 s8", close(1/(1 + math.e), 0.2689, 5e-5))
vega = [v for v in load("l19-running-backwards")["screens"][10]["widget"]["wrong"] if v["id"] == "wrong-units"][0]
check("l19 s10 key", close(0.10/0.40, 0.25, 1e-12))
check("FINDING 3: l19 s10 slip 'wrong-units' value is 1/0.04, as its feedback says", close(vega["value"], 1/0.04, 0.05))
qn = stats.norm.ppf(0.99)
check("l19 s11", close(qn, 2.3263, 5e-5) and close(stats.norm.pdf(qn), 0.02665, 5e-6) and close(1/stats.norm.pdf(qn), 37.5, 0.05)
      and close(stats.norm.ppf(0.991) - qn, 0.04, 0.005) and close(1/stats.norm.pdf(0), 2.5, 0.01)
      and close(37.5/2.5, 15, 1e-9))
check("l19 quiz", close(1/29, 0.0345, 5e-5) and sp.simplify(sp.diff(sp.asin(x/2), x) - 1/sp.sqrt(4 - x**2)) == 0
      and sp.simplify(sp.diff(1/sp.sin(x), x) + sp.csc(x)*sp.cot(x)) == 0)
check("review5 inverse/arctan", close(1/81, 0.0123, 5e-5) and sp.simplify(sp.diff(sp.atan(x/3), x) - 3/(9 + x**2)) == 0)
check("hw5 arctan(1/x)", sp.simplify(sp.diff(sp.atan(1/x), x) + 1/(1 + x**2)) == 0
      and close(math.atan(1/0.7) + math.atan(0.7), math.pi/2, 1e-12))

# ---------------------------------------------------------------- l20
fx = x*sp.exp(-x)
check("l20 s1/s2", sp.simplify(sp.diff(fx, x, 2) - (x - 2)*sp.exp(-x)) == 0 and close(fx.subs(x, 0.8), 0.3595, 5e-5)
      and close(sp.diff(fx, x, 2).subs(x, 0.8), -0.5392, 5e-5) and close(2*math.exp(-2), 0.2707, 5e-5)
      and close(-math.exp(-1), -0.37, 0.005) and sp.solve(sp.diff(fx, x, 3), x) == [3])
gg = x**2/(x**2 - 1)
check("l20 g", sp.simplify(sp.diff(gg, x) + 2*x/(x**2 - 1)**2) == 0
      and sp.simplify(sp.diff(gg, x, 2) - 2*(3*x**2 + 1)/(x**2 - 1)**3) == 0 and sp.diff(gg, x, 2).subs(x, 0) == -2)
check("l20 s6 points", all(close(gg.subs(x, a), b, 0.006) for a, b in ((0.8, -1.78), (0.6, -0.56), (0.4, -0.19), (0.2, -0.04))))
cr = sp.Symbol("c", positive=True)
check("l20 s8", sp.simplify(sp.diff(cr**sp.Rational(1, 3), cr, 2) + sp.Rational(2, 9)*cr**sp.Rational(-5, 3)) == 0)
check("l20 s10", close(0.5*math.log(120) + 0.5*math.log(80), 4.5848, 5e-5) and close(math.sqrt(9600), 97.98, 0.005)
      and close(math.log(100), 4.6052, 5e-5) and close(math.log(80), 4.382, 5e-4))
bell = sp.exp(-x**2/2)
check("l20 s11", sp.simplify(sp.diff(bell, x, 2) - (x**2 - 1)*bell) == 0)
check("l20 quiz", sp.expand(sp.diff(x**3 - 6*x**2, x, 2) - (6*x - 12)) == 0 and sp.expand(sp.diff(x**4 - 4*x**3, x, 2) - 12*x*(x - 2)) == 0)
check("review5 r7", sp.expand(sp.diff(x**5 - 5*x**4, x, 2) - 20*x**2*(x - 3)) == 0)
hh = x*sp.exp(-x**2/2)
check("hw5 tap", sp.simplify(sp.diff(hh, x) - (1 - x**2)*bell) == 0 and sp.simplify(sp.diff(hh, x, 2) - x*(x**2 - 3)*bell) == 0
      and close(hh.subs(x, sp.sqrt(3)), 0.3865, 5e-5) and close(hh.subs(x, 1), 0.6065, 5e-5))
hs = x/(1 + x**2)
check("hw5 sketch", sp.simplify(sp.diff(hs, x) - (1 - x**2)/(1 + x**2)**2) == 0
      and sp.simplify(sp.diff(hs, x, 2) - 2*x*(x**2 - 3)/(1 + x**2)**3) == 0)

# ---------------------------------------------------------------- review-4, homework-4
fr = 2*x**3 - 3*x**2 - 12*x + 5
check("review4 r0", sp.expand(sp.diff(fr, x) - 6*(x - 2)*(x + 1)) == 0 and fr.subs(x, 2) == -15 and sp.diff(fr, x, 2).subs(x, 2) == 18)
check("review4 r2/r3/r6", close(250/98, 2.551, 5e-4) and close(98/250, 0.392, 1e-9)
      and close(0.03*10000 - 0.0000015*1e8, 150, 1e-9) and close(0.3 - 0.7/3, 0.0667, 5e-5))
check("review4 r8", [f0.subs(x, v) for v in (-2, -1, 1, 3)] == [-2, 2, -2, 18])
check("hw4 h0/h1/h2", close(4*math.exp(-2), 0.5413, 5e-5) and (3*x**4 - 4*x**3).subs(x, 1) == -1
      and sp.simplify((x*(L - 2*x)**2).subs(x, L/6) - 2*L**3/27) == 0)
Pp = 6/(1 + y) + 6/(1 + y)**2 + 106/(1 + y)**3
check("hw4 par duration", close(Pp.subs(y, 0.06), 100, 1e-9) and close(-sp.diff(Pp, y).subs(y, 0.06), 267.30, 0.005)
      and close(2.673*1.06, 2.833, 5e-4))
Gk = 0.55*sp.log(1 + f) + 0.45*sp.log(1 - f)
check("hw4 long kelly", close(Gk.subs(f, 0.1), 0.0050, 5e-5) and close(Gk.subs(f, 0.2), -0.00014, 5e-6)
      and close(math.exp(5.0), 150, 2))
# Monte Carlo: Kelly growth claims (median growth over 1,000 bets, twice Kelly does not grow, Kelly beats other stakes)
rng = np.random.default_rng(20261126)
wins = rng.random((20000, 1000)) < 0.55
def mean_log(fr_):
    return np.where(wins, math.log(1 + fr_), math.log(1 - fr_)).sum(axis=1)
lg = {fr_: mean_log(fr_) for fr_ in (0.05, 0.1, 0.15, 0.2)}
se = lg[0.1].std()/math.sqrt(20000)
check("MC kelly: mean log growth over 1,000 bets is about 5.0 at f = 0.1", abs(lg[0.1].mean() - 5.008) < 4*se)
check("MC kelly: median growth factor about 150", 120 < math.exp(np.median(lg[0.1])) < 185)
check("MC kelly: f = 0.1 beats 0.05, 0.15 and 0.2 (paired)",
      all((lg[0.1] - lg[o]).mean() > 4*(lg[0.1] - lg[o]).std()/math.sqrt(20000) for o in (0.05, 0.15, 0.2)))
check("MC kelly: twice Kelly has no growth", abs(lg[0.2].mean() + 0.139) < 4*lg[0.2].std()/math.sqrt(20000))
Cc = 500*sp.sqrt(9 + x**2) + 300*(8 - x)
check("hw4 cable", sp.solve(sp.diff(Cc, x), x) == [sp.Rational(9, 4)] and Cc.subs(x, sp.Rational(9, 4)) == 3600
      and Cc.subs(x, 0) == 3900 and close(Cc.subs(x, 8), 4272, 0.5) and close(500*math.sqrt(13), 1802.8, 0.05))

# ---------------------------------------------------------------- problems-4
R = 900*s/(2 + s)**2
check("p4 spread", sp.simplify(sp.diff(R, s) - 900*(2 - s)/(2 + s)**3) == 0 and R.subs(s, 2) == sp.Rational(225, 2)
      and R.subs(s, 1) == 100 and close(sp.diff(R, s).subs(s, 1)*0.25, 8.3333, 5e-5)
      and close(R.subs(s, 1.25) - 100, 6.5089, 5e-5) and sp.diff(R, s, 2).subs(s, 1) < 0)
Nn = 60*sp.log(1 + t) - 3*t
check("p4 signal", sp.limit(Nn/t, t, 0) == 57 and sp.limit(Nn/t, t, sp.oo) == -3 and sp.solve(sp.diff(Nn, t), t) == [19]
      and close(Nn.subs(t, 19), 122.7439, 5e-5) and close(Nn.subs(t, 20), 122.6713, 5e-5)
      and close(60*math.log10(20) - 57, 21.0618, 5e-5))
Vv = 50*sp.exp(-2*u) + 50*sp.exp(-8*u) - 100*sp.exp(-5*u)
check("p4 barbell", sp.diff(Vv, u).subs(u, 0) == 0 and sp.diff(Vv, u, 2).subs(u, 0) == 900
      and close(1000*Vv.subs(u, 0.01), 42.81, 0.005) and close(1000*Vv.subs(u, -0.01), 47.31, 0.005)
      and all(Vv.subs(u, v) >= -1e-12 for v in np.linspace(-0.5, 0.5, 101)))
An = (1 - sp.exp(-10*r))/r
check("p4 annuity", sp.limit(An, r, 0) == 10 and sp.limit(sp.diff(An, r), r, 0) == -50
      and close(An.subs(r, 0.02), 9.0635, 5e-5) and close((1 - math.exp(-0.02))/0.02, 0.9901, 5e-5)
      and sp.limit(sp.diff(An, r, 2), r, 0) > 0)

# ---------------------------------------------------------------- problems-5
th = sp.atan(x/30)
check("p5 camera", sp.simplify(sp.diff(th, x) - 30/(900 + x**2)) == 0 and close(30/2500*20, 0.24, 1e-12)
      and close(math.pi/6, 0.5236, 5e-5) and close(math.sqrt(3600/math.pi - 900), 15.6817, 5e-5)
      and close(math.sqrt(7200/math.pi - 900), 37.3073, 5e-5))
Nl = 1000/(1 + 9*sp.exp(-t))
check("p5 logistic", sp.simplify(sp.diff(Nl, t) - Nl*(1000 - Nl)/1000) == 0 and Nl.subs(t, 0) == 100
      and sp.simplify(Nl.subs(t, sp.log(9)) - 500) == 0 and sp.simplify(Nl.subs(t, sp.log(81)) - 900) == 0
      and 160*600/1000 == 96 and close(math.log(81), 4.3944, 5e-5) and 800/250 == 3.2)
pq = 2*sp.atan(q/500)
q1 = 500*math.tan(0.5)
check("p5 impact", sp.simplify(sp.diff(pq, q) - 1000/(250000 + q**2)) == 0
      and sp.simplify(sp.diff(pq, q, 2) + 2000*q/(250000 + q**2)**2) == 0 and close(q1, 273.15, 0.005)
      and close((250000 + q1**2)/1000, 324.6116, 5e-4) and close(1000/(250000 + q1**2), 0.0031, 5e-5))

# ---------------------------------------------------------------- fluency-l13, whole range
def cubic(ka, r_, g_, d_):
    kb = sp.Rational(-3*ka*(2*r_ + g_), 2)
    kc = 3*ka*r_*(r_ + g_)
    return ka*x**3 + kb*x**2 + kc*x + d_, kb


def classify(poly):
    out = {}
    for root in sp.solve(sp.diff(poly, x), x):
        out[root] = "max" if sp.diff(poly, x, 2).subs(x, root) < 0 else "min"
    return out


def fl_sign(ka):
    return 1 if ka > 0 else -1


cases = {"max": 0, "min": 0, "val": 0, "closed": 0}
bad = []
for ka, r_, g_ in itertools.product((1, -1, 2, -2), range(-4, 4), range(1, 5)):
    if (ka*(2*r_ + g_)) % 2 != 0 or r_ + g_ > 4:
        continue
    poly, kb = cubic(ka, r_, g_, 0)           # d shifts values only
    cl = classify(poly)
    mx = sp.Rational(2*r_ + g_ - fl_sign(ka)*g_, 2)
    mn = sp.Rational(2*r_ + g_ + fl_sign(ka)*g_, 2)
    if kb.q != 1:
        bad.append(("non-integer coefficient", ka, r_, g_))
    if mx != 0 and mn != -mx:                # family local-maximum
        cases["max"] += 1
        if cl.get(mx) != "max" or cl.get(mn) != "min" or mn == mx or -mx == mx:
            bad.append(("local-maximum", ka, r_, g_))
        fpp = 6*ka*mx - 3*ka*(2*r_ + g_)
        if not fpp < 0:
            bad.append(("local-maximum fpp sign", ka, r_, g_))
    if mn != 0 and mx != -mn:                # family local-minimum
        cases["min"] += 1
        if cl.get(mn) != "min" or cl.get(mx) != "max":
            bad.append(("local-minimum", ka, r_, g_))
        fpp = 6*ka*mn - 3*ka*(2*r_ + g_)
        if not fpp > 0:
            bad.append(("local-minimum fpp sign", ka, r_, g_))
for ka, r_, g_, d_ in itertools.product((1, -1), range(-3, 2), (2, 4), range(-9, 10)):
    poly, kb = cubic(ka, r_, g_, d_)
    cl = classify(poly)
    mx = sp.Rational(2*r_ + g_ - ka*g_, 2)
    mn = sp.Rational(2*r_ + g_ + ka*g_, 2)
    fmn, fmx = poly.subs(x, mn), poly.subs(x, mx)
    if r_ + g_ <= 3 and fmn != mn and fmx != mn:      # family minimum-value
        cases["val"] += 1
        if cl.get(mn) != "min" or fmx == fmn or mn == fmn:
            bad.append(("minimum-value", ka, r_, g_, d_))
    for e1, e2 in itertools.product((1, 2), (1, 2, 3)):
        lo, hi, s_ = r_ - e1, r_ + g_ + e2, r_ + g_
        vals = {lo: poly.subs(x, lo), r_: poly.subs(x, r_), s_: poly.subs(x, s_), hi: poly.subs(x, hi)}
        ans, fmin = max(vals.values()), min(vals.values())
        mxx = r_ if ka > 0 else s_
        fmx2 = vals[mxx]
        xa = hi if vals[hi] == ans else (lo if vals[lo] == ans else mxx)
        if not (hi <= 5 and xa != fmin and (fmx2 == ans or xa != fmx2)):
            continue
        cases["closed"] += 1
        grid_max = max(poly.subs(x, sp.Rational(k, 8)) for k in range(8*lo, 8*hi + 1))
        if grid_max != ans or vals[xa] != ans or cl.get(mxx) != "max" or fmin == ans:
            bad.append(("closed-interval key", ka, r_, g_, d_, e1, e2))
        shown = []
        if fmx2 != ans:
            shown.append(fmx2)
        if xa != ans:
            shown.append(xa)
        shown.append(fmin)
        if ans in shown or len(set(shown)) != len(shown):
            bad.append(("closed-interval slip collision", ka, r_, g_, d_, e1, e2, [int(v) for v in shown]))
print("fluency cases", cases)
check("fluency-l13 every case of all four families", not bad and min(cases.values()) > 20)
if bad:
    print("  fluency problems:", bad[:12], "... total", len(bad))

print(f"{N} checks, {len(FAIL)} failing")
for name in FAIL:
    print("  -", name)
sys.exit(1 if FAIL else 0)
