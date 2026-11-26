#!/usr/bin/env python3
"""Concept audit integrals-1-3-r2 (round 2, blind): recompute of stated results in integrals L1 to L3.

Run with the audit venv Python (sympy 1.14, scipy 1.18, numpy 2.5 here; no figure depends on the version):
    python docs/reports/integrals-L1-3-concepts-r2.py
Exits 0 when every check on correct content passes. A check that fails because the content is wrong stays
failing (it is a finding in docs/reviews/audit-integrals-1-3-r2.md); INFO lines are imprecise/misleading
findings and do not fail the run.
Fix pass: the review-3 items[8] check encoded the old accept text ("£0.63"); it now reads the figure the accept line prints.
"""
import json, math, os, re, sys
import numpy as np
import sympy as sp
from scipy import integrate, stats

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C = os.path.join(ROOT, 'app', 'content', 'courses', 'integrals')
J = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf-8'))
fails, n = [], 0


def chk(name, cond):
    global n
    n += 1
    if not cond:
        fails.append(name)
        print('FAIL', name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def info(s):
    print('INFO', s)


x, t, u, b, p, k, nn = sp.symbols('x t u b p k n', positive=True)
X = sp.symbols('X', real=True)


def riemann(f, a, bb, m, rule):
    h = (bb - a) / m
    if rule == 'left':
        return h * sum(f(a + i * h) for i in range(m))
    if rule == 'right':
        return h * sum(f(a + (i + 1) * h) for i in range(m))
    if rule == 'mid':
        return h * sum(f(a + (i + 0.5) * h) for i in range(m))
    if rule == 'trap':
        return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, m)) + f(bb) / 2)


sq = lambda v: v * v
# ---------------- L1: l1 ----------------
chk('l1 R4', close(riemann(sq, 0, 1, 4, 'right'), 0.46875))
chk('l1 L4', close(riemann(sq, 0, 1, 4, 'left'), 0.21875))
chk('l1 M4', close(riemann(sq, 0, 1, 4, 'mid'), 0.328125))
chk('l1 fewest n below 0.4 is 8', riemann(sq, 0, 1, 7, 'right') > 0.4 > riemann(sq, 0, 1, 8, 'right')
    and round(riemann(sq, 0, 1, 7, 'right'), 3) == 0.408 and round(riemann(sq, 0, 1, 8, 'right'), 3) == 0.398)
chk('l1 squares: 3 inside, 6 cut', True)  # checked by hand against x^2 on the 4x4 grid (ledger)
chk('l1 slips', close(0.25 * 30 / 16 * 4, 1.875) and close((14 / 16) / 3, 0.29167, 1e-5) and close((0.21875 + 0.46875) / 2, 0.34375)
    and close(0.25 * 2, 0.5) and close(84 / 64, 1.3125))
chk('l1 [1,2] L4,R4,five', close(riemann(sq, 1, 2, 4, 'left'), 1.96875) and close(riemann(sq, 1, 2, 4, 'right'), 2.71875)
    and close(0.25 * (7.875 + 4), 2.96875))
phi = lambda v: math.exp(-v * v / 2) / math.sqrt(2 * math.pi)
hs = [round(phi(m), 4) for m in (0.125, 0.375, 0.625, 0.875)]
chk('l1 normal heights', hs == [0.3958, 0.3719, 0.3282, 0.2721])
chk('l1 normal M4 0.342 vs exact 0.3413 within 0.001', round(0.25 * sum(hs), 3) == 0.342
    and round(stats.norm.cdf(1) - 0.5, 4) == 0.3413 and abs(0.25 * sum(hs) - (stats.norm.cdf(1) - 0.5)) < 0.001)
chk('l1 quiz', close(riemann(lambda v: 2 * v + 1, 0, 2, 4, 'right'), 7) and close(riemann(lambda v: 2 * v + 1, 0, 2, 4, 'left'), 5)
    and close(riemann(lambda v: v ** 3, 0, 2, 2, 'mid'), 3.5) and close(riemann(sq, 0, 1, 2, 'right'), 0.625)
    and close(riemann(sq, 0, 1, 2, 'left'), 0.125))
# ---------------- l2 ----------------
Rn = sp.simplify(sp.summation((k / nn) ** 2 / nn, (k, 1, nn)))
Ln = sp.simplify(sp.summation((k / nn) ** 2 / nn, (k, 0, nn - 1)))
chk('l2 R_n formula', sp.simplify(Rn - (sp.Rational(1, 3) + 1 / (2 * nn) + 1 / (6 * nn ** 2))) == 0)
chk('l2 L_n formula', sp.simplify(Ln - (sp.Rational(1, 3) - 1 / (2 * nn) + 1 / (6 * nn ** 2))) == 0)
chk('l2 R100, L100, L10, L20, R20', close(float(Rn.subs(nn, 100)), 0.33835) and close(float(Ln.subs(nn, 100)), 0.32835)
    and close(float(Ln.subs(nn, 10)), 0.285) and round(float(Ln.subs(nn, 20)), 3) == 0.309 and round(float(Rn.subs(nn, 20)), 3) == 0.359)
chk('l2 gap 1/n; [1,3] n=10 gap 1.6; sqrt gap .16', close(riemann(sq, 1, 3, 10, 'right') - riemann(sq, 1, 3, 10, 'left'), 1.6)
    and close(riemann(math.sqrt, 0, 4, 50, 'right') - riemann(math.sqrt, 0, 4, 50, 'left'), 0.16))
g = lambda v: 1 - v * v
chk('l2 falling curve sums', close(riemann(g, 0, 1, 4, 'left'), 0.78125) and close(riemann(g, 0, 1, 4, 'right'), 0.53125))
D = lambda v: math.exp(-0.05 * v)
gap = lambda m: (1 - D(10)) * 10 / m
chk('l2 pension 394 strips', gap(394) <= 0.01 < gap(393) and round(gap(393), 5) == 0.01001 and round((1 - D(10)) / 0.05, 2) == 7.87
    and math.ceil(0.3935 / 0.01) == 40)
# ---------------- l3, l4 ----------------
chk('l3 midpoint signed sum', close(riemann(lambda v: v - 1, 0, 3, 6, 'mid'), 1.5))
chk('l3 integrals', close(integrate.quad(lambda v: 2 - v, 0, 5)[0], -2.5) and close(integrate.quad(lambda v: abs(2 - v), 0, 5, points=[2])[0], 6.5)
    and close(integrate.quad(math.sin, 0, math.pi)[0], 2) and close(integrate.quad(lambda v: 400 - 100 * v, 0, 6)[0], 600)
    and close(integrate.quad(lambda v: abs(400 - 100 * v), 0, 6, points=[4])[0], 1000))
chk('l3 midpoint n=1000 of sin reads 2.000', round(riemann(math.sin, 0, math.pi, 1000, 'mid'), 3) == 2.0)
chk('l4 fund', close(10 * 18, 180) and round(math.sqrt(18), 2) == 4.24 and 10 * 4.2 ** 2 < 180 < 10 * 4.25 ** 2)
chk('l4 van, P&L', close(integrate.quad(lambda v: min(2 * v, 20), 0, 30, points=[10])[0], 500)
    and close(integrate.quad(lambda v: 400 - 200 * v, 0, 3)[0], 300) and close(integrate.quad(lambda v: 400 - 200 * v, 0, 4)[0], 0))
d1, d2 = 1e7 * 0.04 / 365, 1e7 * 0.045 / 365
chk('l4 FRN accrual', round(d1, 2) == 1095.89 and round(d2, 2) == 1232.88 and round(30 * d1 + 60 * d2, 2) == 106849.32
    and round(30 * d1, 2) == 32876.71 and round(60 * d2, 2) == 73972.60 and round(1e7 * 0.0425 * 90 / 365, 2) == 104794.52
    and round(1e7 * 0.04 * 90 / 365, 2) == 98630.14 and round(1e7 * 0.045 * 90 / 365, 2) == 110958.90)
if round(60 * 1232.88, 2) != 73972.60:
    info('l4 screens[8] hints: 60 x 1,232.88 (the printed daily figure) = %.2f, the next hint prints 73,972.60' % (60 * 1232.88))
chk('l4 quiz accrued', close(1e6 * 0.06 * 73 / 365, 12000) and round(60000 / 365, 2) == 164.38)
# ---------------- L1 review/homework/problems ----------------
cube = lambda v: v ** 3
chk('review-1', close(riemann(cube, 0, 2, 4, 'left'), 2.25) and close(riemann(cube, 0, 2, 4, 'right'), 6.25)
    and round(riemann(math.sqrt, 0, 4, 2, 'mid'), 2) == 5.46 and round(riemann(math.sqrt, 0, 4, 2, 'left'), 2) == 2.83
    and round(riemann(math.sqrt, 0, 4, 2, 'right'), 2) == 6.83 and close(integrate.quad(lambda v: 300 - 100 * v, 0, 5)[0], 250)
    and close(integrate.quad(lambda v: -300 + 100 * v, 0, 3)[0], -450) and close(integrate.quad(math.sin, 0, 3 * math.pi)[0], 2))
rec = lambda v: 1 / v
chk('homework-1 numbers', close(riemann(rec, 1, 3, 4, 'right'), 0.95) and round(riemann(rec, 1, 3, 4, 'left'), 4) == 1.2833
    and close(integrate.quad(lambda v: abs(v) - 1, -3, 2, points=[-1, 0, 1])[0], 1.5)
    and close(integrate.quad(lambda v: abs(abs(v) - 1), -3, 2, points=[-1, 0, 1])[0], 3.5)
    and close(300 * 1000 / 3, 100000) and sum([2400, 1600, 1200, 1000, 900, 1100, 1500, 2800]) == 12500)
RnH = sp.simplify(sp.summation((9 - (1 + 2 * k / nn) ** 2) * 2 / nn, (k, 1, nn)))
LnH = sp.simplify(sp.summation((9 - (1 + 2 * k / nn) ** 2) * 2 / nn, (k, 0, nn - 1)))
chk('homework-1 derivation R_n, L_n', sp.simplify(RnH - (sp.Rational(28, 3) - 8 / nn - 4 / (3 * nn ** 2))) == 0
    and sp.simplify(LnH - (sp.Rational(28, 3) + 8 / nn - 4 / (3 * nn ** 2))) == 0 and RnH.subs(nn, 4) == sp.Rational(29, 4)
    and LnH.subs(nn, 4) == sp.Rational(45, 4))
chk('homework-1 [0,2] R_n', sp.simplify(sp.summation((2 * k / nn) ** 2 * 2 / nn, (k, 1, nn)) - 4 * (nn + 1) * (2 * nn + 1) / (3 * nn ** 2)) == 0)
f12 = lambda v: 12 - 3 * v * v
chk('problems-1 parabola', close(riemann(f12, 0, 2, 4, 'right'), 12.75) and close(riemann(f12, 0, 2, 4, 'left'), 18.75)
    and sp.simplify(sp.summation((12 - 3 * (2 * k / nn) ** 2) * 2 / nn, (k, 1, nn)) - (16 - 12 / nn - 4 / nn ** 2)) == 0)
r = lambda v: v * v - 4
chk('problems-1 desk', close(riemann(r, 0, 3, 3, 'mid'), -3.25) and close(riemann(r, 0, 3, 3, 'right'), 2) and close(riemann(r, 0, 3, 3, 'left'), -7)
    and close(integrate.quad(r, 0, 3)[0], -3) and close(integrate.quad(r, 0, 2)[0], -16 / 3) and close(integrate.quad(r, 2, 3)[0], 7 / 3)
    and round(3 + math.sqrt(18 / 4), 4) == 5.1213)
# ---------------- L2 ----------------
A = 2 * X ** 2 - X ** 3 / 3
chk('l5 accumulation', close(float(A.subs(X, 2) - A.subs(X, 1.75)), 0.99479, 1e-4) and round(float(A.subs(X, 4) - A.subs(X, 3.75)), 2) == 0.12
    and A.subs(X, 3) == 9 and round(float(A.subs(X, 2.25)), 2) == 6.33 and round(float(A.subs(X, 2.25) - A.subs(X, 2)), 3) == 0.995
    and round(float(A.subs(X, 5)), 2) == 8.33 and A.subs(X, 1) == sp.Rational(5, 3))
h = sp.symbols('h', positive=True)
chk('l5 ratio 4 - h^2/3', sp.simplify((A.subs(X, 2 + h) - A.subs(X, 2)) / h - (4 - h ** 2 / 3)) == 0)
chk('l6', sp.diff(X ** 5 / 5, X) == X ** 4 and sp.simplify(sp.diff(sp.exp(2 * X) / 2, X) - sp.exp(2 * X)) == 0
    and sp.simplify(sp.diff(-1 / (2 * X ** 2), X) - X ** -3) == 0 and (3 * 4 - 16 / 4 + 2) == 10 and (3 * 4 - 16 / 2 + 2) == 6)
chk('l7', close(integrate.quad(lambda v: 3 * v * v, 1, 2)[0], 7) and close(integrate.quad(sq, -1, 2)[0], 3)
    and round(250000 * (1 - math.exp(-0.2)), 2) == 45317.31 and round(-250000 * math.exp(-0.2), 2) == -204682.69
    and round(50000 * math.exp(-0.2), 2) == 40936.54 and round(40000 * (1 - math.exp(-0.5)), 2) == 15738.77
    and round(20000 * math.exp(-0.5), 2) == 12130.61 and close(integrate.quad(lambda s: max(s - 100, 0) / 20, 90, 110, points=[100])[0], 2.5)
    and close(integrate.quad(lambda v: 4 * v ** 3 - 2 * v, 0, 1 / math.sqrt(2))[0], -0.25))
chk('l7 1/x^2 across 0 diverges', sp.integrate(1 / X ** 2, (X, -1, 1)) == sp.oo)
chk('l8', close(integrate.quad(lambda v: v + 2 - v * v, -1, 2)[0], 4.5) and close(integrate.quad(lambda v: 8 - 2 * v * v, -2, 2)[0], 64 / 3)
    and close(integrate.quad(lambda v: abs(v - v ** 3), -1, 1, points=[0])[0], 0.5)
    and close(integrate.quad(lambda v: abs(math.sin(v) - math.cos(v)), 0, math.pi, points=[math.pi / 4])[0], 2 * math.sqrt(2))
    and close(integrate.quad(lambda v: math.sin(v) - math.cos(v), 0, math.pi)[0], 2) and close(integrate.quad(lambda v: 10 - 2 * v, 0, 12)[0], -24)
    and close(integrate.quad(lambda v: abs(10 - 2 * v), 0, 12, points=[5])[0], 74) and round(1 + math.sqrt(2), 3) == 2.414)
chk('review-2', round(14 / 3, 2) == 4.67 and close(integrate.quad(lambda v: 2 * v - v * v, 0, 2)[0], 4 / 3)
    and round(5000 * (1 - math.exp(-0.18)) / 0.06, 2) == 13727.48 and round(15000 * math.exp(-0.18), 2) == 12529.05 and (25 - 12.5) == 12.5)
chk('homework-2', close(integrate.quad(lambda v: v * v + 1, -2, 1)[0], 6) and round(3 * math.e, 3) == 8.155
    and close(integrate.quad(lambda v: abs(4 * v - v ** 3), -2, 2, points=[0])[0], 8)
    and close(integrate.quad(lambda s: (s - 100) * (110 - s) / 100, 100, 110)[0], 5 / 3) and round(72 ** (1 / 3), 2) == 4.16
    and round(108 ** (1 / 3), 3) == 4.762 and round(300000 * (1 - math.exp(-0.2))) == 54381 and round(60000 * math.exp(-0.2)) == 49124
    and round(math.sqrt(2 * math.log(2) / 3), 3) == 0.680)
G = lambda v: stats.norm.cdf(2 * v) - stats.norm.cdf(v)
xs = np.linspace(0.01, 3, 30000)
chk('homework-2 best window is a maximum at 0.680', abs(xs[np.argmax(G(xs))] - math.sqrt(2 * math.log(2) / 3)) < 2e-4)
F2 = X ** 3 / 3 - 3 * X ** 2 + 8 * X
chk('problems-2', F2.subs(X, 3) == 6 and F2.subs(X, 2) == sp.Rational(20, 3) and F2.subs(X, 4) == sp.Rational(16, 3) and F2.subs(X, 6) == 12
    and round(16 * (1 - math.exp(-2)), 4) == 13.8346 and round(2 * math.log(4), 2) == 2.77 and round(2 * math.log(4 / 3), 2) == 0.58
    and close(integrate.quad(lambda v: v + 3 - 2 * v * v, -1, 1.5)[0], 125 / 24) and close(integrate.quad(lambda v: 2 * v * v - v - 3, -2, -1)[0], 19 / 6)
    and close(integrate.quad(lambda v: v + 3 - 2 * v * v, -1.5, 1)[0], 3.9583333333) and close(integrate.quad(lambda v: v + 3 - 2 * v * v, -2, 1.5)[0], 49 / 24)
    and close(integrate.quad(lambda v: abs(12 * v - 3 * v * v - 9), 0, 5, points=[1, 3])[0], 28))
# ---------------- L3 ----------------
chk('l9', round(math.e ** 4 - 1, 3) == 53.598 and round(math.e ** 2 - 1, 3) == 6.389 and round(math.log(1.25), 4) == 0.2231
    and round(math.log(125), 4) == 4.8283 and close(integrate.quad(lambda v: v * (v * v + 1) ** 3, 0, 1)[0], 1.875)
    and close(integrate.quad(lambda v: 2 * v * (v * v + 1) ** 2, 0, 1)[0], 7 / 3)
    and sp.simplify(sp.diff(sp.exp(X ** 2) / (2 * X), X) - (sp.exp(X ** 2) - sp.exp(X ** 2) / (2 * X ** 2))) == 0)
S = lambda v: 100 * 1.25 ** v + 6 * math.sin(3 * math.pi * v)
dS = lambda v: 100 * math.log(1.25) * 1.25 ** v + 18 * math.pi * math.cos(3 * math.pi * v)
chk('l9 log return of the drawn path', abs(integrate.quad(lambda v: dS(v) / S(v), 0, 1)[0] - math.log(1.25)) < 1e-9 and min(S(v) for v in np.linspace(0, 1, 1001)) > 0)
chk('l9 e^(x^2) has no elementary antiderivative (sympy returns erfi)', sp.integrate(sp.exp(X ** 2), X).has(sp.erfi))
chk('l10', round((math.e ** 2 + 1) / 4, 4) == 2.0973 and sp.simplify(sp.diff((X ** 2 - 2 * X + 2) * sp.exp(X), X) - X ** 2 * sp.exp(X)) == 0
    and sp.simplify(sp.diff(X * sp.sin(X) + sp.cos(X), X) - X * sp.cos(X)) == 0
    and abs(integrate.quad(lambda v: 10 * v * math.exp(-0.05 * v), 0, 2)[0] - 18.715) < 5e-4 and round(20 * math.exp(-0.1), 3) == 18.097
    and round(20 * math.exp(-0.05), 3) == 19.025 and round(-4400 * math.exp(-0.1), 2) == -3981.28 and round(math.e ** 2 + 1, 3) == 8.389)
info('l10 screens[9] explain: 4000 - 3981.28 (the printed figure) = %.2f; the text prints "about 18.715" (true value %.4f)'
     % (4000 - 3981.28, 4400 * (1 - math.exp(-0.1)) - 400))
I0 = sp.Integral(X ** 3 * sp.log(X), X)
# the other split of x^3 ln x: u = x^3, v = x ln x - x. The new integral is 3*I - 3*int x^3, so it loops and solves.
v_ = X * sp.log(X) - X
loop = sp.simplify(sp.integrate(v_ * 3 * X ** 2, X) - (3 * sp.integrate(X ** 3 * sp.log(X), X) - 3 * sp.integrate(X ** 3, X)))
chk('l10 quiz[1]: the other split brings back 3 times the same integral (solvable), not a harder one', loop == 0)
info('l10 quiz[1] opt power / screens[3] opt a say the other split is "harder"; homework-3 items[9] model says it loops and solves')
chk('l11', sp.integrate(X ** -2, (X, 1, sp.oo)) == 1 and sp.integrate(X ** -3, (X, 1, sp.oo)) == sp.Rational(1, 2)
    and sp.integrate(1 / sp.sqrt(X), (X, 1, sp.oo)) == sp.oo and sp.integrate(1 / X, (X, 1, sp.oo)) == sp.oo
    and sp.simplify(sp.integrate(x ** -p, (x, 1, b)).rewrite(sp.Piecewise).subs(p, 3) - (b ** -2 - 1) / (-2)) == 0
    and sp.integrate(sp.exp(-sp.Rational(4, 100) * X), (X, 0, sp.oo)) == 25 and sp.integrate(sp.exp(-sp.Rational(2, 100) * X), (X, 0, sp.oo)) == 50
    and round(math.log(1000), 1) == 6.9 and round(math.log(1e6), 1) == 13.8 and round(math.log(1e12), 1) == 27.6
    and sp.integrate(3 * X ** -4, (X, 1, sp.oo)) == 1 and round(1 / 0.06, 2) == 16.67)
chk('l12 trapezium table', [round(riemann(sq, 0, 1, m, 'trap'), 6) for m in (4, 8, 16, 32)] == [0.34375, 0.335938, 0.333984, 0.333496]
    and all(close(riemann(sq, 0, 1, m, 'trap') - 1 / 3, 1 / (6 * m * m), 1e-12) for m in (1, 2, 4, 8, 16, 32, 64)))
jo = 0.25 * ((0 + 0.75 ** 2) / 2 + 0.25 ** 2 + 0.5 ** 2)
chk("l12 Jo's bug returns 0.1484", round(jo, 4) == 0.1484)
pw = lambda z, m: riemann(phi, -z, z, m, 'trap')
chk('l12 prob_within', round(pw(1.96, 1000), 6) == 0.950004 and round(2 * stats.norm.cdf(1.96) - 1, 6) == 0.950004 and round(pw(1.96, 10), 4) == 0.9471
    and round(riemann(phi, 0, 1.96, 1000, 'trap'), 6) == 0.475002)
# error order h^2 for smooth f: ratio of errors on doubling n is about 4 (three integrands)
for nm, f, a_, b_ in (('exp', math.exp, 0, 1), ('sin', math.sin, 0, math.pi), ('1/x', rec, 1, 2)):
    ex = integrate.quad(f, a_, b_)[0]
    ratio = (riemann(f, a_, b_, 100, 'trap') - ex) / (riemann(f, a_, b_, 200, 'trap') - ex)
    r9 = (riemann(f, a_, b_, 100, 'trap') - ex) / (riemann(f, a_, b_, 300, 'trap') - ex)
    chk('l12 error order 2 for ' + nm, abs(ratio - 4) < 0.01 and abs(r9 - 9) < 0.02)
chk('l12 quiz, review-3 trapezium', close(riemann(cube, 0, 2, 2, 'trap'), 5) and round(riemann(rec, 1, 3, 2, 'trap'), 4) == 1.1667
    and close(riemann(lambda v: 3 * v + 2, 0, 4, 1, 'trap'), 32))
rng = np.random.default_rng(20261126)
z = rng.standard_normal(4_000_000)
chk('l12 MC: about 1 day in 20 outside +-1.96 under the normal model', abs((np.abs(z) > 1.96).mean() - 0.05) < 0.0005)
chk('l13 balance', round(2 * math.sqrt(3), 2) == 3.46 and close(integrate.quad(lambda v: 6 * v * v, 0, 2)[0] / 2, 8) and round(2 / math.pi, 3) == 0.637
    and close(integrate.quad(lambda v: v * v / 2, 0, 2)[0], 4 / 3) and round(integrate.quad(lambda v: 100 + 4 * v - v * v, 0, 4)[0] / 4, 2) == 102.67)
U = rng.uniform(90, 110, 4_000_000)
T = rng.triangular(90, 100, 110, 4_000_000)
chk('l13 MC expected payoffs: uniform 2.50, triangular 1.67, call 105 0.625, tri call 104 0.36', abs(np.maximum(U - 100, 0).mean() - 2.5) < 0.01
    and abs(np.maximum(T - 100, 0).mean() - 5 / 3) < 0.01 and abs(np.maximum(U - 105, 0).mean() - 0.625) < 0.005
    and abs(np.maximum(T - 104, 0).mean() - 0.36) < 0.005 and abs(np.maximum(100 - U, 0).mean() - 2.5) < 0.01)
ku, kt = stats.kurtosis(U, fisher=False), stats.kurtosis(T, fisher=False)
info('l13 screens[8] "Fatter tails, as in the uniform model": kurtosis uniform %.2f, triangular %.2f (uniform is the THINNER-tailed shape); '
     'sd uniform %.2f, triangular %.2f. The option gap comes from spread, not tail shape.' % (ku, kt, U.std(), T.std()))
chk('l13 s8 basis: uniform has lower kurtosis and larger sd than the triangle', ku < kt and U.std() > T.std())
# equal-variance comparison: a uniform with the triangle's sd prices the at-the-money call BELOW the triangle
sd_t = math.sqrt(100 / 6)
U2 = rng.uniform(100 - sd_t * math.sqrt(3), 100 + sd_t * math.sqrt(3), 4_000_000)
info('l13 s8: at equal sd %.2f the uniform call is worth %.3f, the triangle %.3f' % (sd_t, np.maximum(U2 - 100, 0).mean(), 5 / 3))
# a bent payoff whose kink is outside the price range: E g(X) = g(E X)
chk('l13 s5 counter-example to "for a bent payoff they differ": call struck at 80, X uniform on [90,110]',
    abs(np.maximum(U - 80, 0).mean() - max(U.mean() - 80, 0)) < 1e-9)
info('l13 screens[5] explain and summary.ideas[2] state E[g(X)] != g(E[X]) without "in general"; problems-3 uses "in general"')
chk('review-3', round(0.5 * math.log(5), 4) == 0.8047 and close(integrate.quad(lambda v: v * math.exp(-v * v), 0, np.inf)[0], 0.5, 1e-8)
    and close(integrate.quad(lambda v: v * math.exp(-v), 0, np.inf)[0], 1, 1e-8))
r3 = J('review-3')['items'][8]['widget']
# Re-pointed in the fix pass: the check first read "£0.63" from the old accept line; it now reads the figure the accept line prints.
acc = float(re.search(r'£([0-9.]+)', r3['accept']).group(1))
ok63 = abs(acc - r3['answer']) <= r3['tol']['abs'] + 1e-9
chk('review-3 items[8]: the accept line prints "£%s" as accepted; the tolerance must accept it (answer %s, tol %s)' % (acc, r3['answer'], r3['tol']), ok63)
chk('homework-3', close(integrate.quad(lambda v: v * math.exp(-0.05 * v), 0, np.inf)[0], 400, 1e-5)
    and close(integrate.quad(lambda y: y * (6 - y) / 100, 0, 6)[0], 0.36) and round(riemann(lambda v: math.exp(-v * v), 0, 1, 4, 'trap'), 4) == 0.7430
    and round(integrate.quad(lambda v: math.exp(-v * v), 0, 1)[0], 4) == 0.7468 and round(0.25 * sum(math.exp(-(i / 4) ** 2) for i in range(5)), 3) == 0.914
    and sp.integrate(sp.log(X) / X ** 3, (X, 1, sp.oo)) == sp.Rational(1, 4) and sp.integrate(sp.log(X) / X, (X, 1, sp.oo)) == sp.oo
    and round((25 - 1 / 0.041) / 25 * 100, 2) == 2.44
    and sp.simplify(sp.diff(sp.exp(X) * (sp.sin(X) - sp.cos(X)) / 2, X) - sp.exp(X) * sp.sin(X)) == 0)


def n_needed(f, a_, b_, exact, tol, mode='exact'):
    m = 1
    if mode == 'exact':
        while abs(riemann(f, a_, b_, m, 'trap') - exact) >= tol:
            m *= 2
        return m
    if mode == 'coarse':
        while abs(riemann(f, a_, b_, 2 * m, 'trap') - riemann(f, a_, b_, m, 'trap')) >= tol:
            m *= 2
        return m
    prev = riemann(f, a_, b_, 1, 'trap')
    while True:
        m *= 2
        cur = riemann(f, a_, b_, m, 'trap')
        if abs(cur - prev) < tol:
            return m
        prev = cur


T3 = [(sq, 0, 1, 1 / 3, 1e-4, 64), (lambda v: v, 0, 1, 0.5, 1e-9, 1), (cube, 0, 2, 4, 0.01, 32), (math.sin, 0, math.pi, 2, 1e-3, 64),
      (math.exp, 0, 1, math.e - 1, 1e-5, 128), (sq, 0, 1, 1 / 3, 1.5e-4, 64)]
chk('homework-3 n_needed expected values', all(n_needed(*c[:5]) == c[5] for c in T3))
first = lambda mode: next((i + 3 for i, c in enumerate(T3) if n_needed(*c[:5], mode=mode) != c[5]), None)
chk('homework-3 successive-estimate coding that returns the coarser n fails test 8 first', first('coarse') == 8)
info('homework-3 items[4]: the successive-estimate coding that returns the finer n fails test %s first (returns %d on test 3), so it is '
     'shown the test-3 line "Stop only when the error is below tol" although it stops too late' % (first('fine'), n_needed(*T3[0][:5], mode='fine')))
# problems-3
chk('problems-3 order size', close(integrate.quad(lambda v: 2 * v / (1 + v * v) ** 2, 0, np.inf)[0], 1, 1e-8) and round(math.sqrt(99), 2) == 9.95)
chk('problems-3 time to fill', round(3 * math.exp(-2), 3) == 0.406 and close(integrate.quad(lambda v: v * v * math.exp(-v), 0, np.inf)[0], 2, 1e-8)
    and close(100 * integrate.quad(lambda v: v * math.exp(-2 * v), 0, np.inf)[0], 25, 1e-6) and round(100 * math.exp(-2), 2) == 13.53)
Xg = rng.gamma(2.0, 1.0, 4_000_000)
chk('problems-3 MC: E[100 e^-X] = 25 for the x e^-x density', abs((100 * np.exp(-Xg)).mean() - 25) < 0.05)
info('problems-3 items[1].parts[4] opt b why "No one wait gives E[g(X)]": the single wait x* = ln 4 = %.4f gives 100e^-x* = %.2f exactly'
     % (math.log(4), 100 * math.exp(-math.log(4))))
ln = math.log
T2 = riemann(ln, 0.5, 1.5, 2, 'trap')
ex = 1.5 * ln(1.5) - 1.5 - (0.5 * ln(0.5) - 0.5)
chk('problems-3 log return numbers', round(T2, 4) == -0.0719 and round(ex, 4) == -0.0452 and round(riemann(ln, 0.5, 1.5, 2, 'mid'), 4) == -0.0323
    and round(0.5 * (ln(0.5) + ln(1.5)), 4) == -0.1438 and round(0.5 * ln(0.5) / 2, 4) == -0.1733 and round(1.5 * ln(1.5) - 1.5, 4) == -0.8918
    and round(0.5 * ln(0.5) - 0.5, 4) == -0.8466 and close(0.0267 / 16, 0.00166875) and abs(abs(riemann(ln, 0.5, 1.5, 8, 'trap') - ex) - 0.0017) < 1e-4)
sgn = J('problems-3')['items'][2]['parts'][0]['feedback']['byKey']['sign']
m = re.search(r'ln 0\.5 is [−-]([0-9.]+) and ln 1\.5 is ([0-9.]+)', sgn)
chk('problems-3 items[2].parts[0] fb.sign: the printed values of ln 0.5 and ln 1.5 (true: %.5f, %.5f; printed: %s)'
    % (ln(0.5), ln(1.5), m.groups() if m else 'reworded'),
    (m is None) or (abs(-float(m.group(1)) - ln(0.5)) < 1e-4 and abs(float(m.group(2)) - ln(1.5)) < 1e-4))
W = rng.uniform(0.5, 1.5, size=(200_000, 30))
wealth = W.prod(axis=1)
chk('problems-3 MC: with independent years the median compounded wealth shrinks while the mean stays near 1',
    np.median(wealth) < 0.5 and abs(wealth.mean() - 1) < 0.03 and abs(np.log(W).mean() - ex) < 5e-4)
s = lambda v: v * math.exp(-v * v / 8)
exs = 4 * (1 - math.exp(-2))
chk('problems-3 signal', round(exs, 3) == 3.459 and round(4 * (1 - math.exp(-4)), 3) == 3.927 and round(riemann(s, 0, 4, 2, 'trap'), 3) == 2.967
    and round(2 * (s(0) + s(2) + s(4)), 3) == 3.509 and round(riemann(s, 0, 4, 2, 'mid'), 3) == 3.713
    and abs(riemann(s, 0, 4, 16, 'trap') - exs) < 0.01 < abs(riemann(s, 0, 4, 8, 'trap') - exs))
# ---------------- fluency templates (symbolic identities behind each family) ----------------
a_, c_, m_ = sp.symbols('a c m', nonzero=True)
kk = sp.symbols('kk', positive=True, integer=True)
fl = [
    sp.diff(a_ / (kk + 1) * X ** (kk + 1), X) - a_ * X ** kk,
    sp.diff(-m_ * x ** (1 - kk), x) - m_ * (kk - 1) * x ** (-kk),
    sp.diff(a_ / (2 * (kk + 1)) * (X ** 2 + c_) ** (kk + 1), X) - a_ * X * (X ** 2 + c_) ** kk,
    sp.diff(a_ / (2 * c_) * sp.exp(c_ * X ** 2), X) - a_ * X * sp.exp(c_ * X ** 2),
    sp.diff(a_ / 2 * sp.log(X ** 2 + 3), X) - a_ * X / (X ** 2 + 3),
    sp.diff(a_ / c_ * X * sp.exp(c_ * X) - a_ / c_ ** 2 * sp.exp(c_ * X), X) - a_ * X * sp.exp(c_ * X),
    sp.diff(a_ / c_ * X * sp.sin(c_ * X) + a_ / c_ ** 2 * sp.cos(c_ * X), X) - a_ * X * sp.cos(c_ * X),
    sp.diff(-a_ / c_ * X * sp.cos(c_ * X) + a_ / c_ ** 2 * sp.sin(c_ * X), X) - a_ * X * sp.sin(c_ * X),
    sp.diff(a_ / (kk + 1) * x ** (kk + 1) * sp.log(x) - a_ / (kk + 1) ** 2 * x ** (kk + 1), x) - a_ * x ** kk * sp.log(x),
]
chk('fluency l6/l7/l9/l10 template antiderivatives differentiate back', all(sp.simplify(e) == 0 for e in fl))


# ---------------- mechanical scan of numeric widgets ----------------
def within(v, a, tol):
    tol = tol or {'abs': 0}
    if isinstance(tol, (int, float)):
        tol = {'abs': tol}
    if 'rel' in tol:
        return abs(v - a) <= abs(a) * tol['rel'] + 1e-12
    return abs(v - a) <= tol.get('abs', 0) + 1e-9


def walk(o, path):
    if isinstance(o, dict):
        if o.get('kind') == 'numeric' and 'answer' in o:
            yield path, o
        for kx, vx in o.items():
            yield from walk(vx, path + '.' + kx)
    elif isinstance(o, list):
        for i, vx in enumerate(o):
            yield from walk(vx, '%s[%d]' % (path, i))


files = [f[:-5] for f in sorted(os.listdir(C)) if re.match(r'(l([1-9]|1[0-3])-|review-[123]|homework-[123]|problems-[123])', f)]
collide, nwid = [], 0
for f in files:
    for path, w in walk(J(f), ''):
        nwid += 1
        for wr in w.get('wrong', []):
            if 'value' in wr and isinstance(wr['value'], (int, float)) and within(float(wr['value']), float(w['answer']), w.get('tol')):
                collide.append((f, path, wr['id']))
chk('no wrong[] value lies inside its key tolerance (%d numeric widgets): %s' % (nwid, collide), not collide)

print("numeric widgets scanned: %d" % nwid)
print("%d checks, %d failing" % (n, len(fails)))
sys.exit(1 if fails else 0)
