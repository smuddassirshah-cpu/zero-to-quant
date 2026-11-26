#!/usr/bin/env python3
"""Concept audit, integrals levels 1 to 3 (round 1): independent recomputation of every stated number with
sympy and scipy.integrate, plus Monte Carlo checks of the empirical claims.

Exit 0 means every check that should pass on correct content passes. Checks listed in EXPECTED_FAIL are
content defects (audit findings): they stay failing until the content is fixed, and the script exits 1
while any of them fails. Run: python docs/reports/integrals-L1-3-concepts.py [--quiet]
"""
import math, sys
import numpy as np
import sympy as sp
from scipy import integrate, stats

QUIET = '--quiet' in sys.argv
fails, npass = [], 0
def chk(name, got, want, tol=5e-4, rel=False):
    global npass
    ok = abs(got - want) <= (tol * abs(want) if rel else tol)
    if ok: npass += 1
    else: fails.append(name)
    if not QUIET or not ok: print(('ok   ' if ok else 'FAIL ') + f'{name}: got {got:.8g}, content {want:.8g}')
def truth(name, cond):
    global npass
    if cond: npass += 1
    else: fails.append(name)
    if not QUIET or not cond: print(('ok   ' if cond else 'FAIL ') + name)

x, t, n, k, b, p, r, u, s = sp.symbols('x t n k b p r u s', real=True)
I = lambda f, a, c, v=x: float(sp.integrate(f, (v, a, c)))
Q = lambda f, a, c: integrate.quad(f, a, c, epsabs=1e-12, epsrel=1e-12)[0]

def riemann(f, a, c, m, rule):
    h = (c - a) / m
    if rule == 'left': pts = [a + i * h for i in range(m)]
    elif rule == 'right': pts = [a + (i + 1) * h for i in range(m)]
    elif rule == 'mid': pts = [a + (i + 0.5) * h for i in range(m)]
    elif rule == 'trap': return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, m)) + f(c) / 2)
    return h * sum(f(q) for q in pts)
sq = lambda v: v * v
phi = lambda v: math.exp(-v * v / 2) / math.sqrt(2 * math.pi)

# ---------------- Level 1 ----------------
# l1
under = sum(1 for i in range(4) for j in range(4) if (j + 1) * 0.25 <= (i * 0.25) ** 2 + 1e-12)
cut = sum(1 for i in range(4) for j in range(4) if (i * 0.25) ** 2 < (j + 1) * 0.25 - 1e-12 and ((i + 1) * 0.25) ** 2 > j * 0.25 + 1e-12)
chk('l1.s0 squares wholly under x^2', under, 3, 0); chk('l1.s0 squares cut', cut, 6, 0)
chk('l1.s1 R7', riemann(sq, 0, 1, 7, 'right'), 0.408); chk('l1.s1 R8', riemann(sq, 0, 1, 8, 'right'), 0.398)
chk('l1.s2 R4', riemann(sq, 0, 1, 4, 'right'), 15 / 32, 1e-12); chk('l1.s3 L4', riemann(sq, 0, 1, 4, 'left'), 7 / 32, 1e-12)
chk('l1.s3 slip three', (14 / 16) / 3, 0.29167, 1e-4); chk('l1.s4 M4', riemann(sq, 0, 1, 4, 'mid'), 21 / 64, 1e-12)
chk('l1.s4 slip average', (7 / 32 + 15 / 32) / 2, 0.34375, 1e-12)
chk('l1.s6 L4 on [1,2]', riemann(sq, 1, 2, 4, 'left'), 1.96875, 1e-12); chk('l1.s6 R4', riemann(sq, 1, 2, 4, 'right'), 2.71875, 1e-12)
chk('l1.s6 five heights', 0.25 * sum(sq(1 + i / 4) for i in range(5)), 2.96875, 1e-12); chk('l1.s6 area', I(x**2, 1, 2), 7 / 3, 1e-12)
chk('l1.s7 strip 4 start', 2 + 3 * 0.5, 3.5, 0)
for q, hgt in zip([0.125, 0.375, 0.625, 0.875], [0.3958, 0.3719, 0.3282, 0.2721]): chk(f'l1.s9 phi({q})', phi(q), hgt, 6e-5)
chk('l1.s9 M4 normal', riemann(phi, 0, 1, 4, 'mid'), 0.342, 5e-4); chk('l1.s9 exact', stats.norm.cdf(1) - 0.5, 0.3413, 5e-5)
truth('l1.s9 four strips within 0.001', abs(riemann(phi, 0, 1, 4, 'mid') - (stats.norm.cdf(1) - 0.5)) < 0.001)
lin = lambda v: 2 * v + 1
chk('l1.q0 R4', riemann(lin, 0, 2, 4, 'right'), 7, 1e-12); chk('l1.q0 left', riemann(lin, 0, 2, 4, 'left'), 5, 1e-12); chk('l1.q0 exact', I(2 * x + 1, 0, 2), 6, 1e-12)
chk('l1.q1 R2', riemann(sq, 0, 1, 2, 'right'), 0.625, 1e-12); chk('l1.q1 L2', riemann(sq, 0, 1, 2, 'left'), 0.125, 1e-12)
cube = lambda v: v ** 3
chk('l1.q2 M2', riemann(cube, 0, 2, 2, 'mid'), 3.5, 1e-12); chk('l1.q2 avg L,R', (riemann(cube, 0, 2, 2, 'left') + riemann(cube, 0, 2, 2, 'right')) / 2, 5, 1e-12)
# l2
Rn = sp.simplify(sp.summation((k / n) ** 2 / n, (k, 1, n))); Ln = sp.simplify(sp.summation((k / n) ** 2 / n, (k, 0, n - 1)))
truth('l2.s3 R_n closed form', sp.simplify(Rn - (n + 1) * (2 * n + 1) / (6 * n**2)) == 0)
truth('l2.s3 R_n expansion', sp.simplify(Rn - (sp.Rational(1, 3) + 1 / (2 * n) + 1 / (6 * n**2))) == 0)
truth('l2.s7 L_n expansion', sp.simplify(Ln - (sp.Rational(1, 3) - 1 / (2 * n) + 1 / (6 * n**2))) == 0)
truth('l2.s1 gap 1/n', sp.simplify(Rn - Ln - 1 / n) == 0)
chk('l2.s0 L20', float(Ln.subs(n, 20)), 0.309); chk('l2.s0 R20', float(Rn.subs(n, 20)), 0.359); chk('l2.s0 gap n=19', 1 / 19, 0.0526, 5e-5)
chk('l2.s2 gap', riemann(sq, 1, 3, 10, 'right') - riemann(sq, 1, 3, 10, 'left'), 1.6, 1e-9)
chk('l2.s4 R100', float(Rn.subs(n, 100)), 0.33835, 5e-6); chk('l2.s4 L100', float(Ln.subs(n, 100)), 0.32835, 5e-6)
g = lambda v: 1 - v * v
chk('l2.s5 L4', riemann(g, 0, 1, 4, 'left'), 0.78125, 1e-12); chk('l2.s5 R4', riemann(g, 0, 1, 4, 'right'), 0.53125, 1e-12); chk('l2.s5 area', I(1 - x**2, 0, 1), 2 / 3, 1e-12)
chk('l2.s6 gap sqrt', riemann(math.sqrt, 0, 4, 50, 'right') - riemann(math.sqrt, 0, 4, 50, 'left'), 0.16, 1e-9)
D = lambda v: math.exp(-0.05 * v)
chk('l2.s8 D(10)', D(10), 0.6065, 5e-5); chk('l2.s8 n', math.ceil((1 - D(10)) * 10 / 0.01), 394, 0)
chk('l2.s8 gap at 393', riemann(D, 0, 10, 393, 'left') - riemann(D, 0, 10, 393, 'right'), 0.01001, 5e-6)
truth('l2.s8 gap at 394 <= 0.01', riemann(D, 0, 10, 394, 'left') - riemann(D, 0, 10, 394, 'right') <= 0.01)
chk('l2.s8 value', Q(D, 0, 10), 7.87, 5e-3)
chk('l2.q0 gap', riemann(lambda v: 3 * v, 0, 2, 6, 'right') - riemann(lambda v: 3 * v, 0, 2, 6, 'left'), 2, 1e-9)
chk('l2.q1 L10', float(Ln.subs(n, 10)), 0.285, 1e-12)
truth('l2.q3 R_n for x', sp.simplify(sp.summation(k / n / n, (k, 1, n)) - (n + 1) / (2 * n)) == 0)
# l3
f1 = lambda v: v - 1
chk('l3.s0 M6', riemann(f1, 0, 3, 6, 'mid'), 1.5, 1e-12); chk('l3.s0 area', Q(lambda v: abs(v - 1), 0, 3), 2.5, 1e-9)
chk('l3.s1 zero at b=2', I(x - 1, 0, 2), 0, 1e-12); chk('l3.s2 four humps', I(2 * sp.sin(sp.pi * x / 2), 0, 8), 0, 1e-12)
chk('l3.s3 integral', I(2 - x, 0, 5), -2.5, 1e-12); chk('l3.s3 area', Q(lambda v: abs(2 - v), 0, 5), 6.5, 1e-9)
chk('l3.s4 reversed', I(x - 1, 3, 0), -1.5, 1e-12); chk('l3.s5 sin half', I(sp.sin(x), 0, sp.pi / 2), 1, 1e-12)
chk('l3.s5 midpoint n=1000', riemann(math.sin, 0, math.pi, 1000, 'mid'), 2.000, 5e-4)
chk('l3.s6 area two humps', Q(lambda v: abs(math.sin(v)), 0, 2 * math.pi), 4, 1e-9)
chk('l3.s9 inventory', I(400 - 100 * t, 0, 6, t), 600, 1e-9); chk('l3.s9 traded', Q(lambda v: abs(400 - 100 * v), 0, 6), 1000, 1e-6)
chk('l3.q0', I(x, -2, 2), 0, 1e-12); chk('l3.q3 area', Q(lambda v: abs(v - 1), 0, 3), 2.5, 1e-9)
# l3.s7.ex claims a negative integral means f "spends more of [2, 5] below the axis than above it". Counterexample:
fx = sp.Piecewise((-10, x < sp.Rational(5, 2)), (1, True))   # below the axis on [2, 2.5), above on [2.5, 5]
neg, time_below, time_above = I(fx, 2, 5), 0.5, 2.5
truth('l3.s7.ex negative integral => more of the interval below the axis (FINDING 1)', not (neg < 0 and time_below < time_above))
# l4
chk('l4.s0 week', 120 + 80 + 150 + 60 + 90, 500, 0); chk('l4.s1 half time', math.sqrt(18), 4.24, 5e-3); chk('l4.s2 A(5)', I(20 * t, 0, 5, t), 250, 1e-9)
chk('l4.s3 van', Q(lambda v: min(2 * v, 20), 0, 30), 500, 1e-6); chk('l4.s4 P&L', I(400 - 200 * t, 0, 3, t), 300, 1e-9); chk('l4.s5 back to 0', I(400 - 200 * t, 0, 4, t), 0, 1e-9)
d1, d2 = 1e7 * 0.04 / 365, 1e7 * 0.045 / 365
chk('l4.s8 daily 4%', d1, 1095.89, 5e-3); chk('l4.s8 daily 4.5%', d2, 1232.88, 5e-3); chk('l4.s8 total', 30 * d1 + 60 * d2, 106849.32, 5e-3)
chk('l4.s8 first piece', 30 * d1, 32876.71, 5e-3); chk('l4.s8 second piece', 60 * d2, 73972.60, 5e-3)
truth('l4.s8.ex "60 x 1,232.88 = 73,972.60" as printed arithmetic (FINDING 7)', abs(60 * 1232.88 - 73972.60) < 0.005)
chk('l4.s8 slip average', 1e7 * 0.0425 * 90 / 365, 104794.52, 5e-3); chk('l4.s8 slip 4%', 1e7 * 0.04 * 90 / 365, 98630.14, 5e-3); chk('l4.s8 slip 4.5%', 1e7 * 0.045 * 90 / 365, 110958.90, 5e-3)
chk('l4.q0', 2000 * 15 + 500 * 30, 45000, 0); chk('l4.q1', I(3 * t, 0, 4, t), 24, 1e-9); chk('l4.q2', -50 * 6 + 80 * 2, -140, 0); chk('l4.q3', 1e6 * 0.06 * 73 / 365, 12000, 1e-6)
# review-1, homework-1, problems-1
chk('rev1.i0 L4', riemann(cube, 0, 2, 4, 'left'), 2.25, 1e-12); chk('rev1.i0 right', riemann(cube, 0, 2, 4, 'right'), 6.25, 1e-12)
chk('rev1.i1', I(x, -1, 2), 1.5, 1e-12); chk('rev1.i2 gap', (8 - 0) * 2 / 40, 0.4, 1e-12); chk('rev1.i4', I(sp.sin(x), 0, 3 * sp.pi), 2, 1e-12)
truth('rev1.i5 L_n', sp.simplify(sp.summation(k / n / n, (k, 0, n - 1)) - (n - 1) / (2 * n)) == 0)
chk('rev1.i6', I(300 - 100 * t, 0, 5, t), 250, 1e-9); chk('rev1.i7 M2', riemann(math.sqrt, 0, 4, 2, 'mid'), 5.46, 5e-3); chk('rev1.i7 true', I(sp.sqrt(x), 0, 4), 16 / 3, 1e-9)
chk('rev1.i8 low', I(-300 + 100 * t, 0, 3, t), -450, 1e-9); chk('rev1.i8 end', I(-300 + 100 * t, 0, 6, t), 0, 1e-9)
inv = lambda v: 1 / v
chk('hw1.i0 R4', riemann(inv, 1, 3, 4, 'right'), 0.950, 5e-4); chk('hw1.i0 left', riemann(inv, 1, 3, 4, 'left'), 1.2833, 5e-5); chk('hw1.i0 exact', math.log(3), 1.0986, 5e-5)
truth('hw1.i1 cubes', sp.simplify(sp.summation((k / n) ** 3 / n, (k, 1, n)) - sp.Rational(1, 4) * (1 + 1 / n) ** 2) == 0)
truth('hw1.i2 R_n on [0,2]', sp.simplify(sp.summation((2 * k / n) ** 2 * 2 / n, (k, 1, n)) - 4 * (n + 1) * (2 * n + 1) / (3 * n**2)) == 0)
chk('hw1.i3 integral', Q(lambda v: abs(v) - 1, -3, 2), 1.5, 1e-9); chk('hw1.i3 area', Q(lambda v: abs(abs(v) - 1), -3, 2), 3.5, 1e-6)
chk('hw1.i5', 30 * (2400 + 1600 + 1200 + 1000 + 900 + 1100 + 1500 + 2800), 375000, 0); chk('hw1.i6', I(300 * t**2, 0, 10, t), 100000, 1e-6)
qf = lambda v: 600 - 200 * v
chk('hw1.i7 L5', riemann(qf, 0, 5, 5, 'left'), 1000, 1e-9); chk('hw1.i7 R5', riemann(qf, 0, 5, 5, 'right'), 0, 1e-9); chk('hw1.i7 net', I(600 - 200 * t, 0, 5, t), 500, 1e-9)
chk('hw1.i7 traded', Q(lambda v: abs(qf(v)), 0, 5), 1300, 1e-6); chk('hw1.i7 peak', I(600 - 200 * t, 0, 3, t), 900, 1e-9)
RnH = sp.simplify(sp.summation((9 - (1 + 2 * k / n) ** 2) * 2 / n, (k, 1, n))); LnH = sp.simplify(sp.summation((9 - (1 + 2 * k / n) ** 2) * 2 / n, (k, 0, n - 1)))
truth('hw1.i8 R_n', sp.simplify(RnH - (sp.Rational(28, 3) - 8 / n - 4 / (3 * n**2))) == 0); truth('hw1.i8 L_n', sp.simplify(LnH - (sp.Rational(28, 3) + 8 / n - 4 / (3 * n**2))) == 0)
chk('hw1.i8 exact', I(9 - x**2, 1, 3), 28 / 3, 1e-12); chk('hw1.i8 R4', float(RnH.subs(n, 4)), 7.25, 1e-12); chk('hw1.i8 L4', float(LnH.subs(n, 4)), 11.25, 1e-12)
fp = lambda v: 12 - 3 * v * v
chk('p1.i0 R4', riemann(fp, 0, 2, 4, 'right'), 12.75, 1e-12); chk('p1.i0 L4', riemann(fp, 0, 2, 4, 'left'), 18.75, 1e-12)
truth('p1.i0 R_n', sp.simplify(sp.summation((12 - 3 * (2 * k / n) ** 2) * 2 / n, (k, 1, n)) - (16 - 12 / n - 4 / n**2)) == 0); chk('p1.i0 area', I(12 - 3 * x**2, 0, 2), 16, 1e-12)
chk('p1.i1 by week 3', I(12 - 4 * t, 0, 3, t), 18, 1e-12); chk('p1.i1 5 weeks', I(12 - 4 * t, 0, 5, t), 10, 1e-12); chk('p1.i1 back to zero', I(12 - 4 * t, 0, 6, t), 0, 1e-12)
rf = lambda v: v * v - 4
chk('p1.i2 M3', riemann(rf, 0, 3, 3, 'mid'), -3.25, 1e-12); chk('p1.i2 right', riemann(rf, 0, 3, 3, 'right'), 2, 1e-12); chk('p1.i2 left', riemann(rf, 0, 3, 3, 'left'), -7, 1e-12)
chk('p1.i2 exact', I(t**2 - 4, 0, 3, t), -3, 1e-12); chk('p1.i2 low', I(t**2 - 4, 0, 2, t), -16 / 3, 1e-12); chk('p1.i2 last hour', I(t**2 - 4, 2, 3, t), 7 / 3, 1e-12)

# ---------------- Level 2 ----------------
A = sp.integrate(t * (4 - t), (t, 0, x))
truth('l5 A(x)', sp.simplify(A - (2 * x**2 - x**3 / 3)) == 0)
chk('l5.s0 step 1.75->2', float(A.subs(x, 2) - A.subs(x, 1.75)), 0.99, 6e-3); chk('l5.s0 step 3.75->4', float(A.subs(x, 4) - A.subs(x, 3.75)), 0.12, 5e-3)
chk('l5.s2 rise', float(A.subs(x, 2.25) - A.subs(x, 2)), 0.995, 5e-4); chk('l5.s2 A(2.25)', float(A.subs(x, 2.25)), 6.33, 5e-3)
h = sp.symbols('h'); truth('l5.s3 ratio', sp.simplify((A.subs(x, 2 + h) - A.subs(x, 2)) / h - (4 - h**2 / 3)) == 0)
chk('l5.s4 A(4)', float(A.subs(x, 4)), 10.67, 5e-3); chk('l5.s4 A(5)', float(A.subs(x, 5)), 8.33, 5e-3); chk('l5.s5 A(3)', float(A.subs(x, 3)), 9, 1e-12); chk('l5.s7 A(1)', float(A.subs(x, 1)), 5 / 3, 1e-12)
chk('l5.s8 C(4)', I(4 - t, 0, 4, t), 8, 1e-12); chk('l5.s8 C(8)', I(4 - t, 0, 8, t), 0, 1e-12); chk('l5.q3 C(5)', I(6 - 2 * t, 0, 5, t), 5, 1e-12)
truth('l5.q1 G\'', sp.simplify(sp.diff(sp.Integral(sp.exp(t**2), (t, 1, x)), x) - sp.exp(x**2)) == 0)
truth('l6 e^{kx}', sp.simplify(sp.diff(sp.exp(k * x) / k, x) - sp.exp(k * x)) == 0); truth('l6 ln(-x)', sp.simplify(sp.diff(sp.log(-x), x) - 1 / x) == 0)
chk('l6.s9 P(4)', float((3 * t - t**2 / 4 + 2).subs(t, 4)), 10, 1e-12); chk('l6.s9 slip', float((3 * t - t**2 / 2 + 2).subs(t, 4)), 6, 1e-12); chk('l6.q2', 2 * 8 + 3, 19, 0)
chk('l7.s0', I(2 * x, 1, 3), 8, 1e-12); chk('l7.s2', I(3 * x**2, 1, 2), 7, 1e-12); chk('l7.s3', I(sp.sin(x), 0, sp.pi), 2, 1e-12); chk('l7.s5', I(2 * x, 3, 1), -8, 1e-12); chk('l7.s7', I(x**2, -1, 2), 3, 1e-12)
truth('l7.s6 integral of 1/x^2 over [-1,1] diverges', sp.integrate(1 / x**2, (x, -1, 1)) == sp.oo)
pv = lambda c, rr, T: c * (1 - math.exp(-rr * T)) / rr
chk('l7.s9 PV', pv(10000, 0.04, 5), 45317.31, 5e-3); chk('l7.s9 quad', Q(lambda v: 10000 * math.exp(-0.04 * v), 0, 5), 45317.31, 5e-3)
chk('l7.s9 F(5)', -250000 * math.exp(-0.2), -204682.69, 5e-3); chk('l7.s9 end-discount', 50000 * math.exp(-0.2), 40936.54, 5e-3); chk('l7.s9 cost', 50000 - pv(10000, 0.04, 5), 4683, 0.5)
chk('l7.s10 expected payoff', Q(lambda v: max(v - 100, 0) / 20, 90, 110), 2.5, 1e-6); chk('l7.q0', math.e**2 - 1, 6.389, 5e-4)
r1 = 1 / math.sqrt(2); chk('l7.q2 lower piece', I(4 * x**3 - 2 * x, 0, sp.sqrt(2) / 2), -0.25, 1e-12); chk('l7.q2 area', Q(lambda v: abs(4 * v**3 - 2 * v), 0, 1), 0.5, 1e-6)
chk('l7.q3 PV', pv(2000, 0.05, 10), 15738.77, 5e-3); chk('l7.q3 slip', 20000 * math.exp(-0.5), 12130.61, 5e-3); chk('l7.q3 share', pv(2000, 0.05, 10) / 20000, 0.79, 5e-3)
chk('l8.s2', I(x + 2 - x**2, -1, 2), 4.5, 1e-12); chk('l8.s2 line', I(x + 2, -1, 2), 7.5, 1e-12); chk('l8.s2 parabola', I(x**2, -1, 2), 3, 1e-12)
chk('l8.s4', I(8 - 2 * x**2, -2, 2), 64 / 3, 1e-12); chk('l8.s5', Q(lambda v: abs(v - v**3), -1, 1), 0.5, 1e-6)
chk('l8.s6 area', Q(lambda v: abs(math.sin(v) - math.cos(v)), 0, math.pi), 2 * math.sqrt(2), 1e-6); chk('l8.s6 unsplit', I(sp.sin(x) - sp.cos(x), 0, sp.pi), 2, 1e-12)
chk('l8.q2 one piece', I(sp.sin(x) - sp.cos(x), sp.pi / 4, sp.pi), 2.414, 5e-4)
net, area = I(30 - 2 * t - 20, 0, 12, t), Q(lambda v: abs(10 - 2 * v), 0, 12)
chk('l8.s8 net gap', net, -24, 1e-12); chk('l8.s8 enclosed area', area, 74, 1e-6); chk('l8.s8 lead', I(10 - 2 * t, 0, 5, t), 25, 1e-12)
truth('l8.s8.pr "the area between the rate curves is the gap between the equity curves" (FINDING 2)', abs(area - net) < 1e-6)
chk('l8.q0', I(x - x**2, 0, 1), 0.167, 5e-4); chk('l8.q1', I(4 - x**2, -2, 2), 10.67, 5e-3)
chk('rev2.i2', I(sp.sqrt(x), 1, 4), 4.67, 5e-3); chk('rev2.i3', I(2 * x - x**2, 0, 2), 1.33, 5e-3); chk('rev2.i4', I(5 - t, 0, 5, t), 12.5, 1e-12); chk('rev2.i4 end', I(5 - t, 0, 10, t), 0, 1e-12)
chk('rev2.i6', I(x**3, -2, 0), -4, 1e-12); chk('rev2.i8', pv(5000, 0.06, 3), 13727.48, 5e-3); chk('rev2.i8 slip', 15000 * math.exp(-0.18), 12529.05, 5e-3)
truth('rev2.i0', sp.simplify(sp.diff(sp.Integral(sp.cos(t**2), (t, 0, x)), x) - sp.cos(x**2)) == 0)
chk('hw2.i1', I(x**2 + 1, -2, 1), 6, 1e-12); chk('hw2.i2', math.sin(math.pi / 6) + 2, 2.5, 1e-12); chk('hw2.i4', float(sp.diff(sp.integrate(sp.exp(t), (t, 0, x**3)), x).subs(x, 1)), 8.155, 5e-4)
chk('hw2.i5', Q(lambda v: abs(v - (v**3 - 3 * v)), -2, 2), 8, 1e-6)
tri = lambda v: max(10 - abs(v - 100), 0) / 100
chk('hw2.i6 density total', Q(tri, 90, 110), 1, 1e-6); chk('hw2.i6', integrate.quad(lambda v: max(v - 100, 0) * tri(v), 90, 110, points=[100])[0], 1.67, 5e-3)
chk('hw2.i6 given pays', integrate.quad(lambda v: max(v - 100, 0) * tri(v), 100, 110)[0] / 0.5, 3.33, 5e-3)
kk = sp.symbols('kk', positive=True); truth('hw2.i7 area k^3/6', sp.simplify(sp.integrate(kk * x - x**2, (x, 0, kk)) - kk**3 / 6) == 0); chk('hw2.i7 slips', (72) ** (1 / 3), 4.16, 5e-3); chk('hw2.i7 slip 2', 108 ** (1 / 3), 4.762, 5e-4)
chk('hw2.i8 lease', pv(12000, 0.04, 5), 54381, 0.5); chk('hw2.i8 lower bound', 60000 * math.exp(-0.2), 49124, 0.5)
xs = math.sqrt(2 * math.log(2) / 3); G = lambda v: stats.norm.cdf(2 * v) - stats.norm.cdf(v)
chk('hw2.i9 x*', xs, 0.680, 5e-4); truth('hw2.i9 is a maximum', G(xs) > G(xs - 0.01) and G(xs) > G(xs + 0.01) and abs(2 * phi(2 * xs) - phi(xs)) < 1e-12)
f2 = t**2 - 6 * t + 8; A2 = sp.integrate(f2, (t, 0, x))
chk('p2.i0 A(3)', float(A2.subs(x, 3)), 6, 1e-12); chk('p2.i0 A(2)', float(A2.subs(x, 2)), 20 / 3, 1e-12); chk('p2.i0 A(4)', float(A2.subs(x, 4)), 16 / 3, 1e-12); chk('p2.i0 A(6)', float(A2.subs(x, 6)), 12, 1e-12)
chk('p2.i0 unsigned', Q(lambda v: abs(v * v - 6 * v + 8), 0, 6), 14.666666666666666, 1e-6)
chk('p2.i1 T(4)', 16 * (1 - math.exp(-2)), 13.834635468214197, 1e-12); chk('p2.i1 t', 2 * math.log(4), 2.772588722239781, 1e-12); chk('p2.i1 slip', 2 * math.log(4 / 3), 0.58, 5e-3); chk('p2.i1 v(4)', 8 * math.exp(-2), 1.08, 5e-3)
chk('p2.i2 enclosed', I(x + 3 - 2 * x**2, -1, sp.Rational(3, 2)), 125 / 24, 1e-12); chk('p2.i2 outer', I(2 * x**2 - x - 3, -2, -1), 19 / 6, 1e-12)
chk('p2.i2 slip crossings', I(x + 3 - 2 * x**2, sp.Rational(-3, 2), 1), 3.9583333333333335, 1e-12); chk('p2.i2 one integral', I(x + 3 - 2 * x**2, -2, sp.Rational(3, 2)), 49 / 24, 1e-12)
Gp = sp.integrate(12 * t - 3 * t**2 - 9, (t, 0, x)); truth('p2.i3 G', sp.expand(Gp - (-x**3 + 6 * x**2 - 9 * x)) == 0)
chk('p2.i3 area', Q(lambda v: abs(12 * v - 3 * v * v - 9), 0, 5), 28, 1e-6); chk('p2.i3 G(5)', float(Gp.subs(x, 5)), -20, 1e-12); chk('p2.i3 G(2)', float(Gp.subs(x, 2)), -2, 1e-12)

# ---------------- Level 3 ----------------
truth('l9.s0 g1', sp.simplify(sp.diff(x**2 * sp.exp(x**2), x) - (2 * x * sp.exp(x**2) + 2 * x**3 * sp.exp(x**2))) == 0)
truth('l9.s5 quotient', sp.simplify(sp.diff(sp.exp(x**2) / (2 * x), x) - (sp.exp(x**2) - sp.exp(x**2) / (2 * x**2))) == 0)
chk('l9.s0 slope', 2 * math.e, 5.44, 5e-3); chk('l9.s6', Q(lambda v: 2 * v * math.exp(v * v), 0, 2), 53.598, 5e-4); chk('l9.s6 slip', math.e**2 - 1, 6.389, 5e-4)
chk('l9.s8', math.log(1.25), 0.2231, 5e-5); chk('l9.q1', I(x * (x**2 + 1) ** 3, 0, 1), 1.875, 1e-12); chk('l9.q2', I(2 * x * (x**2 + 1) ** 2, 0, 1), 7 / 3, 1e-12)
# l9.s8: integral of S'/S along the drawn path (wiggles included) equals ln(S1/S0)
Sp = lambda v: 100 * 1.25**v + 6 * math.sin(3 * math.pi * v); dS = lambda v: 100 * math.log(1.25) * 1.25**v + 18 * math.pi * math.cos(3 * math.pi * v)
chk('l9.s8 path integral', Q(lambda v: dS(v) / Sp(v), 0, 1), math.log(Sp(1) / Sp(0)), 1e-9)
# substitution without g'(x) "present up to a constant": u = x + 1 on x*sqrt(x+1); and x = e^s (homework-3 i9 model)
truth('l9 substitution works without g\' present (FINDING 4, informational)', abs(Q(lambda v: v * math.sqrt(v + 1), 0, 3) - Q(lambda w: (w - 1) * math.sqrt(w), 1, 4)) < 1e-9)
truth('l10 parts x cos x', sp.simplify(sp.diff(x * sp.sin(x) + sp.cos(x), x) - x * sp.cos(x)) == 0); truth('l10 x^2 e^x', sp.simplify(sp.diff((x**2 - 2 * x + 2) * sp.exp(x), x) - x**2 * sp.exp(x)) == 0)
chk('l10.s4', Q(lambda v: v * math.log(v), 1, math.e), 2.0973, 5e-5); chk('l10.s4 slips', math.e**2 / 4, 1.8473, 5e-5)
chk('l10.s9 PV', Q(lambda v: 10 * v * math.exp(-0.05 * v), 0, 2), 18.715, 5e-4); chk('l10.s9 F(2)', -4400 * math.exp(-0.1), -3981.28, 5e-3)
chk('l10.s9 slips', 20 * math.exp(-0.1), 18.097, 5e-4); chk('l10.s9 slip mid', 20 * math.exp(-0.05), 19.025, 5e-4)
chk('l10.q2', Q(lambda v: v * math.exp(v), 0, 2), 8.389, 5e-4); chk('l10.q3', Q(math.log, 1, math.e), 1, 1e-9)
truth('l10.q0', sp.simplify(sp.diff(x * sp.exp(2 * x) / 2 - sp.exp(2 * x) / 4, x) - x * sp.exp(2 * x)) == 0)
pp = sp.symbols('pp', positive=True)
truth('l11 p-test value', sp.simplify(sp.integrate(x ** (-pp - 1), (x, 1, sp.oo)) - 1 / pp) == 0)   # p = pp + 1 > 1
truth('l11 p=1 diverges', sp.integrate(1 / x, (x, 1, sp.oo)) == sp.oo); truth('l11 p=1/2 diverges', sp.integrate(1 / sp.sqrt(x), (x, 1, sp.oo)) == sp.oo)
chk('l11.s2', float(sp.integrate(x**-3, (x, 1, sp.oo))), 0.5, 1e-12); chk('l11.s7', float(sp.integrate(sp.exp(-sp.Rational(4, 100) * t), (t, 0, sp.oo))), 25, 1e-9)
chk('l11.s8', float(sp.integrate(sp.exp(-sp.Rational(2, 100) * t), (t, 0, sp.oo))), 50, 1e-9); chk('l11.q0', float(sp.integrate(3 / x**4, (x, 1, sp.oo))), 1, 1e-12); chk('l11.q1', 1 / 0.01, 100, 1e-9)
chk('l12.s0 T1', riemann(sq, 0, 1, 1, 'trap'), 0.5, 1e-12); chk('l12.s1 T2', riemann(sq, 0, 1, 2, 'trap'), 0.375, 1e-12); chk('l12.s3 T4', riemann(sq, 0, 1, 4, 'trap'), 0.34375, 1e-12)
for m, e in [(4, 0.010417), (8, 0.002604), (16, 0.000651), (32, 0.000163)]: chk(f'l12.s4 error n={m}', riemann(sq, 0, 1, m, 'trap') - 1 / 3, e, 6e-7)
chk('l12.s3 test 6', riemann(cube, -1, 2, 3, 'trap'), 4.5, 1e-12); chk('l12.s3 test 7', riemann(inv, 1, 2, 10, 'trap'), 0.693771403175428, 1e-12)
jo = lambda f, a, c, m: (lambda hh, xs: hh * ((f(xs[0]) + f(xs[-1])) / 2 + sum(f(v) for v in xs[1:-1])))((c - a) / m, [a + i * (c - a) / m for i in range(m)])
chk('l12.s5 Jo', jo(sq, 0, 1, 4), 0.1484, 5e-5)
chk('l12.s8 n=1000', riemann(phi, -1.96, 1.96, 1000, 'trap'), 0.9500039163481595, 1e-12); chk('l12.s8 exact', 2 * stats.norm.cdf(1.96) - 1, 0.950004, 5e-7)
chk('l12.s8 n=10', riemann(phi, -1.96, 1.96, 10, 'trap'), 0.9470772208544286, 1e-12); chk('l12.s8 z=1', riemann(phi, -1, 1, 1000, 'trap'), 0.6826893308232487, 1e-12); chk('l12.s8 z=3', riemann(phi, -3, 3, 2000, 'trap'), 0.997300183993443, 1e-12)
chk('l12.q0 T2', riemann(cube, 0, 2, 2, 'trap'), 5, 1e-12); chk('l12.q3 T1', riemann(lambda v: 3 * v + 2, 0, 4, 1, 'trap'), 32, 1e-12)
# empirical order of the trapezium rule: h^2 for a smooth integrand; NOT h^2 for sqrt(x) on [0, 1] (unbounded f'')
order = lambda f, a, c, ex: math.log2(abs(riemann(f, a, c, 512, 'trap') - ex) / abs(riemann(f, a, c, 1024, 'trap') - ex))
chk('l12.s6 order for x^2', order(sq, 0, 1, 1 / 3), 2, 1e-3); chk('l12.s6 order for exp', order(math.exp, 0, 1, math.e - 1), 2, 1e-3)
truth('l12.s6 "error shrinks like h^2" needs a bounded f\'\': order for sqrt on [0,1] is 1.5 (FINDING 5, informational)', abs(order(math.sqrt, 0, 1, 2 / 3) - 1.5) < 0.02)
chk('l13.s0 balance', float(sp.integrate(x**2, (x, 0, 3)) / 3), 3, 1e-12); chk('l13.s0 areas', 2 * 3**1.5 / 3, 3.46, 5e-3); chk('l13.s1', I(6 * x**2, 0, 2) / 2, 8, 1e-12); chk('l13.s2', 2 / math.pi, 0.6366, 5e-5)
chk('l13.s3', I(x / 20, 90, 110), 100, 1e-9); chk('l13.s4 total', I(x / 2, 0, 2), 1, 1e-12); chk('l13.s4 mean', I(x * x / 2, 0, 2), 4 / 3, 1e-12)
chk('l13.s7 TWAP', I(100 + 4 * t - t**2, 0, 4, t) / 4, 102.67, 5e-3); chk('l13.s8', integrate.quad(lambda v: max(v - 100, 0) * tri(v), 100, 110)[0], 1.67, 5e-3)
chk('l13.q2', I(x * 3 * x**2, 0, 1), 0.75, 1e-12); chk('l13.q3', Q(lambda v: max(100 - v, 0) / 20, 90, 110), 2.5, 1e-6)
chk('rev3.i0', Q(lambda v: v / (v * v + 1), 0, 2), 0.8047, 5e-5); chk('rev3.i2', float(sp.integrate(1 / x**2, (x, 2, sp.oo))), 0.5, 1e-12); chk('rev3.i3', riemann(inv, 1, 3, 2, 'trap'), 1.1667, 5e-5)
chk('rev3.i5', float(sp.integrate(x * sp.exp(-x**2), (x, 0, sp.oo))), 0.5, 1e-12); chk('rev3.i6', float(sp.integrate(t * sp.exp(-t), (t, 0, sp.oo))), 1, 1e-12); chk('rev3.i8', Q(lambda v: max(v - 105, 0) / 20, 90, 110), 0.625, 1e-6)
truth('hw3.i2', sp.simplify(sp.diff(sp.exp(x) * (sp.sin(x) - sp.cos(x)) / 2, x) - sp.exp(x) * sp.sin(x)) == 0)
chk('hw3.i3', float(sp.integrate(t * sp.exp(-sp.Rational(5, 100) * t), (t, 0, sp.oo))), 400, 1e-9)
def n_needed(f, a, c, exact, tol):
    m = 1
    while abs(riemann(f, a, c, m, 'trap') - exact) >= tol: m *= 2
    return m
def n_successive(f, a, c, exact, tol):   # a wrong program: ignores `exact`
    m = 1
    while abs(riemann(f, a, c, 2 * m, 'trap') - riemann(f, a, c, m, 'trap')) >= tol: m *= 2
    return m
T7 = [(sq, 0, 1, 1 / 3, 1e-4, 64), (lambda v: v, 0, 1, 0.5, 1e-9, 1), (cube, 0, 2, 4, 0.01, 32), (math.sin, 0, math.pi, 2, 1e-3, 64), (math.exp, 0, 1, math.e - 1, 1e-5, 128)]
for i, (f, a, c, ex, tol, want) in enumerate(T7): chk(f'hw3.i4 n_needed test {i + 3}', n_needed(f, a, c, ex, tol), want, 0)
chk('hw3.i4 T3', riemann(sq, 0, 1, 3, 'trap'), 0.35185185185185186, 1e-12); chk('hw3.i4 T16 cube', riemann(cube, 0, 2, 16, 'trap'), 4.015625, 1e-12)
truth('hw3.i4 hidden tests reject the "successive estimates" program that ignores exact (FINDING 9)', any(n_successive(f, a, c, ex, tol) != want for f, a, c, ex, tol, want in T7))
truth('hw3.i4 proposed extra test separates them', n_needed(sq, 0, 1, 1 / 3, 1.5e-4) == 64 and n_successive(sq, 0, 1, 1 / 3, 1.5e-4) == 32)
chk('hw3.i5', integrate.quad(lambda v: max(v - 104, 0) * tri(v), 104, 110)[0], 0.36, 1e-6); chk('hw3.i5 uniform', Q(lambda v: max(v - 104, 0) / 20, 104, 110), 0.90, 1e-6)
truth('hw3.i6 diverges', sp.integrate(sp.log(x) / x, (x, 1, sp.oo)) == sp.oo); chk('hw3.i7 fall', (1 / 0.04 - 1 / 0.041) / 25 * 100, 2.44, 5e-3)
eh = lambda v: math.exp(-v * v)
chk('hw3.i8 T4', riemann(eh, 0, 1, 4, 'trap'), 0.7430, 5e-5); chk('hw3.i8 true', Q(eh, 0, 1), 0.7468, 5e-5); chk('hw3.i8 no halves', 0.25 * sum(eh(i / 4) for i in range(5)), 0.914, 5e-4)
chk('hw3.i9', float(sp.integrate(sp.log(x) / x**3, (x, 1, sp.oo))), 0.25, 1e-12)
truth('hw3.i9 finite form', sp.simplify(sp.integrate(sp.log(x) / x**3, (x, 1, b)) - (sp.Rational(1, 4) - 1 / (4 * b**2) - sp.log(b) / (2 * b**2))) == 0)
fd = lambda v: 2 * v / (1 + v * v) ** 2
chk('p3.i0 total', Q(fd, 0, np.inf), 1, 1e-9); chk('p3.i0 tail', Q(fd, 2, np.inf), 0.2, 1e-9); chk('p3.i0 q', math.sqrt(99), 9.9498743710662, 1e-12)
gd = lambda v: v * math.exp(-v)
chk('p3.i1 total', Q(gd, 0, np.inf), 1, 1e-9); chk('p3.i1 tail', Q(gd, 2, np.inf), 0.4060058497098381, 1e-9); chk('p3.i1 mean', Q(lambda v: v * gd(v), 0, np.inf), 2, 1e-9)
chk('p3.i1 quote', Q(lambda v: 100 * math.exp(-v) * gd(v), 0, np.inf), 25, 1e-8); chk('p3.i1 at mean', 100 * math.exp(-2), 13.53, 5e-3)
chk('p3.i2 T2', riemann(math.log, 0.5, 1.5, 2, 'trap'), -0.07192051811294523, 1e-12); chk('p3.i2 exact', Q(math.log, 0.5, 1.5), -0.045228747557780724, 1e-12)
chk('p3.i2 mid', riemann(math.log, 0.5, 1.5, 2, 'mid'), -0.0323, 5e-5); chk('p3.i2 predicted error n=8', 0.0267 / 16, 0.00166875, 1e-12)
chk('p3.i2 actual error n=8 (prediction within 0.0001)', abs(riemann(math.log, 0.5, 1.5, 8, 'trap') - Q(math.log, 0.5, 1.5)), 0.0017, 1.5e-4)
sg = lambda v: v * math.exp(-v * v / 8)
chk('p3.i3 integral', Q(sg, 0, 4), 3.458658867053549, 1e-10); chk('p3.i3 average', Q(sg, 0, 4) / 4, 0.8646647167633873, 1e-10); chk('p3.i3 T2', riemann(sg, 0, 4, 2, 'trap'), 2.9674637717969845, 1e-12)
chk('p3.i3 mid', riemann(sg, 0, 4, 2, 'mid'), 3.713, 5e-4); chk('p3.i3 slip limits', 4 * (1 - math.exp(-4)), 3.927, 5e-4)
errs = {m: abs(riemann(sg, 0, 4, m, 'trap') - Q(sg, 0, 4)) for m in (2, 4, 8, 16)}
truth(f'p3.i3 smallest doubling n with actual error < 0.01 is 16 (actual errors {errs[4]:.4f}, {errs[8]:.4f}, {errs[16]:.4f})', errs[8] >= 0.01 > errs[16])

# ---------------- Fluency families (symbolic, all parameter values at once) ----------------
a_, k_, c_, m_, v = sp.symbols('a_ k_ c_ m_ v', nonzero=True, real=True); nn = sp.symbols('nn', positive=True, integer=True)
D0 = lambda F, f: sp.simplify(sp.diff(F, v) - f) == 0
truth('fl10.f0 a v e^{kv}', D0(a_ / k_ * v * sp.exp(k_ * v) - a_ / k_**2 * sp.exp(k_ * v), a_ * v * sp.exp(k_ * v)))
truth('fl10.f1 a v cos(kv)', D0(a_ / k_ * v * sp.sin(k_ * v) + a_ / k_**2 * sp.cos(k_ * v), a_ * v * sp.cos(k_ * v)))
truth('fl10.f2 a v sin(kv)', D0(-a_ / k_ * v * sp.cos(k_ * v) + a_ / k_**2 * sp.sin(k_ * v), a_ * v * sp.sin(k_ * v)))
vp = sp.symbols('vp', positive=True)
truth('fl10.f3 a v^n ln v', sp.simplify(sp.diff(a_ / (nn + 1) * vp ** (nn + 1) * sp.log(vp) - a_ / (nn + 1) ** 2 * vp ** (nn + 1), vp) - a_ * vp**nn * sp.log(vp)) == 0)
truth('fl6.f0 power', sp.simplify(sp.diff(a_ / (nn + 1) * vp ** (nn + 1), vp) - a_ * vp**nn) == 0)
truth('fl6.f2 negative power', sp.simplify(sp.diff(-m_ * vp ** (1 - nn), vp) - m_ * (nn - 1) * vp ** (-nn)) == 0)
truth('fl9.f0', sp.simplify(sp.diff(k_ / (2 * (nn + 1)) * (v**2 + c_) ** (nn + 1), v) - k_ * v * (v**2 + c_) ** nn) == 0)
truth('fl9.f1', D0(k_ / (2 * a_) * sp.exp(a_ * v**2), k_ * v * sp.exp(a_ * v**2)))
truth('fl9.f2', sp.simplify(sp.diff(k_ / 2 * sp.log(v**2 + 3), v) - k_ * v / (v**2 + 3)) == 0)
ok = True
for mm in range(1, 5):
    for bb in (-3, -2, -1, 1, 2, 3, 4):
        for e in (1, 2, 3):
            for (p0, q0) in ((0, 1), (0, 2), (1, 2)):
                ok &= abs(I(2 * mm * x * (x**2 + bb) ** e, p0, q0) - mm * ((q0**2 + bb) ** (e + 1) - (p0**2 + bb) ** (e + 1)) / (e + 1)) < 1e-9
truth('fl9.f3 definite substitution, every parameter set', ok)
ok = True
for cc in (1, 5, 12):
    for p0 in range(1, 6):
        for q0 in range(p0 + 1, 7): ok &= abs(I(cc / x**2, p0, q0) - cc * (1 / p0 - 1 / q0)) < 1e-12
truth('fl7.f2 c/x^2', ok)
ok = all(abs(Q(lambda w: cc * math.exp(kq[0] * w), 0, kq[1]) - cc / kq[0] * (math.exp(kq[0] * kq[1]) - 1)) < 1e-8 for cc in (1, 9) for kq in [(1, 2), (1, 3), (-1, 1), (-1, 2), (-1, 3), (2, 1), (2, 2), (-2, 1), (-2, 2), (0.5, 3), (0.5, 4), (-0.5, 2), (-0.5, 3), (-0.5, 4)])
truth('fl7.f3 exponentials', ok)
ok = all(abs(I(aa * x**2 + 2 * hh * x + c0, p0, q0) - (aa * (q0**3 - p0**3) / 3 + hh * (q0**2 - p0**2) + c0 * (q0 - p0))) < 1e-9 for aa in (-3, 2) for hh in (-3, 0, 3) for c0 in (-5, 4) for p0 in (-2, 0) for q0 in (1, 3))
truth('fl7.f1 quadratics', ok)

# ---------------- Monte Carlo (seeded; 2e6 draws; standard errors noted) ----------------
rng = np.random.default_rng(20261126); N = 2_000_000
z = rng.standard_normal(N)
chk('MC l1.s9 P(0<Z<1)', np.mean((z > 0) & (z < 1)), 0.3413, 1.5e-3)                         # se 3.4e-4
chk('MC l12.s8 P(|Z|<1.96)', np.mean(np.abs(z) < 1.96), 0.95, 8e-4); chk('MC l12.s8 one day in 20 outside', 1 / np.mean(np.abs(z) >= 1.96), 20, 0.4)
U = rng.uniform(90, 110, N)
chk('MC l7.s10/l13.s5 call under uniform', np.mean(np.maximum(U - 100, 0)), 2.5, 0.01); chk('MC call given it pays', np.mean((U - 100)[U > 100]), 5, 0.02)
chk('MC rev3.i8 call K=105', np.mean(np.maximum(U - 105, 0)), 0.625, 0.006); chk('MC l13.q3 put', np.mean(np.maximum(100 - U, 0)), 2.5, 0.01)
Tr = rng.triangular(90, 100, 110, N)
chk('MC l13.s8/hw2.i6 call under triangle', np.mean(np.maximum(Tr - 100, 0)), 5 / 3, 0.008); chk('MC hw3.i5 call K=104', np.mean(np.maximum(Tr - 104, 0)), 0.36, 0.004)
truth('MC l13.s8 uniform (fatter tails) is worth more than triangle', np.mean(np.maximum(U - 100, 0)) > np.mean(np.maximum(Tr - 100, 0)) + 0.5)
chk('MC l13.s4 mean of density x/2', np.mean(2 * np.sqrt(rng.uniform(0, 1, N))), 4 / 3, 0.003); chk('MC l13.q2 mean of density 3x^2', np.mean(rng.uniform(0, 1, N) ** (1 / 3)), 0.75, 0.002)
chk('MC rev3.i6 exponential mean', np.mean(rng.exponential(1, N)), 1, 0.004)
X0 = np.sqrt(1 / rng.uniform(0, 1, N) - 1)        # inverse of the tail 1 / (1 + m^2)
chk('MC p3.i0 P(X>2)', np.mean(X0 > 2), 0.2, 1.5e-3); chk('MC p3.i0 median', np.median(X0), 1, 0.005); chk('MC p3.i0 1% size', np.quantile(X0, 0.99), 9.95, 0.25)
Gm = rng.gamma(2, 1, N)
chk('MC p3.i1 P(X>2)', np.mean(Gm > 2), 0.406, 1.5e-3); chk('MC p3.i1 mean', np.mean(Gm), 2, 0.005); chk('MC p3.i1 E[100 e^-X]', np.mean(100 * np.exp(-Gm)), 25, 0.08)
truth('MC p3.i1 value at the mean wait undervalues', 100 * math.exp(-np.mean(Gm)) < np.mean(100 * np.exp(-Gm)) - 10)
R = rng.uniform(0.5, 1.5, (200_000, 50)); W = R.prod(axis=1)
chk('MC p3.i2 E[ln X]', np.mean(np.log(R)), -0.0452, 1e-3); chk('MC p3.i2 mean gross return', np.mean(R), 1, 1e-3)
truth(f'MC p3.i2 compounded wealth tends to shrink: after 50 years median {np.median(W):.3f}, share below 1 {np.mean(W < 1):.3f}', np.median(W) < 0.2 and np.mean(W < 1) > 0.8)
truth(f'MC p3.i2 ... although mean wealth stays near 1 ({np.mean(W):.2f}): the typical path shrinks, not the mean (FINDING 11, informational)', abs(np.mean(W) - 1) < 0.15)

EXPECTED_FAIL = {
    'l3.s7.ex negative integral => more of the interval below the axis (FINDING 1)',
    'l8.s8.pr "the area between the rate curves is the gap between the equity curves" (FINDING 2)',
    'l4.s8.ex "60 x 1,232.88 = 73,972.60" as printed arithmetic (FINDING 7)',
    'hw3.i4 hidden tests reject the "successive estimates" program that ignores exact (FINDING 9)',
}
unexpected = [f for f in fails if f not in EXPECTED_FAIL]
print(f'\n{npass} checks pass, {len(fails)} fail ({len(fails) - len(unexpected)} are content findings, {len(unexpected)} unexpected).')
for f in fails: print('  failing:', f)
sys.exit(1 if fails else 0)
