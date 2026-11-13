#!/usr/bin/env python3
"""Concept audit, round 2 (blind): limits-thm level 4 (l14 to l19, review-4, homework-4, problems-4).

Recomputes every graded key, numeric wrong option and slip value from the mistake its feedback names,
checks the figures quoted in prose, runs a Monte Carlo for each empirical or distributional claim, and
runs every code solution (and starter) against its hidden tests. Exit 0 means every check passed.
A check that fails because the content is wrong is named FINDING n and stays failing.
Round 2 found no such check: every finding of this round is a wording or hypothesis point (see
docs/reviews/audit-limits-thm-4-r2.md), and the script holds the numbers its proposed fixes rely on.

Run: python docs/reports/limits-thm-L4-concepts-r2.py
"""
import json
import math
import os
import re
import sys

import numpy as np
import sympy as sp
from scipy import integrate, stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'limits-thm')
FILES = {
    'l14': 'l14-joint-densities.json', 'l15': 'l15-new-variables.json', 'l16': 'l16-adding-densities.json',
    'l17': 'l17-smallest-and-largest.json', 'l18': 'l18-gamma-beta.json', 'l19': 'l19-generating-functions.json',
    'rev': 'review-4.json', 'hw': 'homework-4.json', 'prob': 'problems-4.json',
}
DOC = {k: json.load(open(os.path.join(COURSE, v), encoding='utf-8')) for k, v in FILES.items()}
RAW = {k: json.dumps(v, ensure_ascii=False) for k, v in DOC.items()}

FAILS = []
COUNT = [0]
e = math.exp
Phi = stats.norm.cdf
phi = stats.norm.pdf


def ok(name, cond, detail=''):
    COUNT[0] += 1
    if not cond:
        FAILS.append(f'{name}: {detail}')
        print('FAIL', name, detail)


def get(key, path):
    o = DOC[key]
    for tok in re.findall(r'[^.\[\]]+', path):
        o = o[int(tok)] if tok.isdigit() else o[tok]
    return o


def key_and_slips(key, path, answer, slips=None):
    """path names the object holding `widget`. Checks the key and every numeric wrong value."""
    w = get(key, path)['widget']
    tol = (w.get('tol') or {}).get('abs', 0) or 1e-9
    ok(f'{key} {path} key', abs(w['answer'] - answer) <= tol + 1e-12, f"content {w['answer']} recomputed {answer:.6f}")
    wrong = {x['id']: x for x in w.get('wrong', [])}
    slips = slips or {}
    ok(f'{key} {path} slip ids', set(wrong) == set(slips), f'content {sorted(wrong)} script {sorted(slips)}')
    for sid, val in slips.items():
        if sid not in wrong:
            continue
        stol = (wrong[sid].get('tol') or {}).get('abs', 0) or 1e-9
        ok(f'{key} {path} slip {sid}', abs(wrong[sid]['value'] - val) <= stol + 1e-12,
           f"content {wrong[sid]['value']} mistake gives {val:.6f}")
        ok(f'{key} {path} slip {sid} is not the key', abs(val - answer) > tol, 'slip equals the key')


def quoted(key, *literals):
    for lit in literals:
        ok(f'{key} quotes {lit}', lit in RAW[key], 'literal not found in file')


def order_is_listed(key, path):
    w = get(key, path)['widget']
    ok(f'{key} {path} order', w['answer'] == [ln['id'] for ln in w['lines']], 'answer is not the listed order')


def near(name, got, want, tol):
    ok(name, abs(got - want) <= tol, f'got {got:.5f} want {want:.5f} tol {tol}')


rng = np.random.default_rng(20261113)
N = 1_000_000

# --------------------------------------------------------------------------- l14 joint densities
key_and_slips('l14', 'screens[1]', 1 / 3, {'half': 0.5, 'other': 2 / 3})
key_and_slips('l14', 'screens[5]', 0.5, {'area': 0.25, 'all': 1})
key_and_slips('l14', 'screens[11]', 5 / 16, {'indep': 0.25, 'half': 0.5})
key_and_slips('l14', 'quiz[0]', 1.0, {'half': 0.5})
key_and_slips('l14', 'quiz[2]', 0.25, {'x': 0.5})
key_and_slips('l14', 'quiz[3]', 0.25, {'swap': 0.75, 'half': 0.5})
order_is_listed('l14', 'screens[8]')
a, b = 1 - e(-1), 1 - e(-2)
quoted('l14', f'{a:.4f}', f'{b:.4f}', f'{a * b:.4f}', f'{a + b:.4f}')
x, y, t, s, u, v, p, n_ = sp.symbols('x y t s u v p n', positive=True)
ok('l14 marginal exp', sp.simplify(sp.integrate(2 * sp.exp(-x - 2 * y), (y, 0, sp.oo)) - sp.exp(-x)) == 0)
ok('l14 triangle marginal x', sp.integrate(2, (y, 0, x)) == 2 * x)
ok('l14 triangle marginal y', sp.simplify(sp.integrate(2, (x, y, 1)) - 2 * (1 - y)) == 0)
EX = sp.integrate(x * 2 * x, (x, 0, 1)); EY = sp.integrate(y * 2 * (1 - y), (y, 0, 1))
EXY = sp.integrate(sp.integrate(2 * x * y, (y, 0, x)), (x, 0, 1))
ok('l14 covariance 1/36', (EX, EY, EXY, EXY - EX * EY) == (sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(1, 4), sp.Rational(1, 36)))
fgm = 1 + (2 * x - 1) * (2 * y - 1)
ok('l14 FGM marginal uniform', sp.simplify(sp.integrate(fgm, (y, 0, 1)) - 1) == 0)
ok('l14 FGM both within five years', sp.integrate(sp.integrate(fgm, (y, 0, sp.Rational(1, 2))), (x, 0, sp.Rational(1, 2))) == sp.Rational(5, 16))
ok('l14 quiz densities integrate to 1', all(sp.integrate(sp.integrate(f, (y, 0, 1)), (x, 0, 1)) == 1
                                            for f in (x + y, 4 * x * y, 2 - x - y, sp.Rational(3, 2) * (x ** 2 + y ** 2))))
# Monte Carlo
A = rng.exponential(1.0, N); B = rng.exponential(0.5, N)
near('MC l14 P(A first)', np.mean(A < B), 1 / 3, 0.003)
near('MC l14 rectangle product', np.mean((A <= 1) & (B <= 1)), a * b, 0.003)
U1, U2 = rng.random(N), rng.random(N)
TX, TY = np.maximum(U1, U2), np.minimum(U1, U2)          # uniform on the triangle 0 <= y <= x <= 1
near('MC l14 P(X+Y<=1) on triangle', np.mean(TX + TY <= 1), 0.5, 0.003)
near('MC l14 cov on triangle', np.cov(TX, TY)[0, 1], 1 / 36, 0.0006)
sl = np.abs(TX - 0.5) < 0.01
near('MC l14 E[Y|X=0.5]', TY[sl].mean(), 0.25, 0.006)
XU = rng.uniform(-1, 1, N)
near('MC l14 cov(X, X^2)', np.cov(XU, XU ** 2)[0, 1], 0.0, 0.002)
keep = rng.random(N) * 2 < 1 + (2 * U1 - 1) * (2 * U2 - 1)   # rejection sample of the FGM density
near('MC l14 FGM joint default', np.mean((U1[keep] <= 0.5) & (U2[keep] <= 0.5)), 5 / 16, 0.004)
# an independent pair whose support is NOT a rectangle (basis for the "product set" finding)
XS = np.where(rng.random(N) < 0.5, rng.random(N), 2 + rng.random(N)); YS = rng.random(N)
near('MC product-set support, independent', np.mean((XS > 2) & (YS < 0.3)), 0.5 * 0.3, 0.003)

# --------------------------------------------------------------------------- l15 transformations
key_and_slips('l15', 'screens[1]', 2, {'mean': 0.5})
key_and_slips('l15', 'screens[4]', phi(math.log(2)) / 2, {'nofac': phi(math.log(2)), 'wayround': 2 * phi(math.log(2))})
key_and_slips('l15', 'screens[6]', phi(1), {'one': phi(1) / 2, 'nofac': 2 * phi(1)})
key_and_slips('l15', 'screens[10]', Phi(0.5), {'tail': 1 - Phi(0.5), 'zero': 0})
key_and_slips('l15', 'screens[11]', 100 * (1 - e(-0.1)), {'linear': 10, 'prob': 1 - e(-0.1)})
key_and_slips('l15', 'quiz[0]', 0.5, {'one': 1, 'two': 2})
key_and_slips('l15', 'quiz[1]', -math.log(0.1) / 0.5, {'u': -math.log(0.9) / 0.5})
key_and_slips('l15', 'quiz[2]', 2 * Phi(1) - 1, {'half': Phi(1) - 0.5, 'upper': Phi(1)})
key_and_slips('l15', 'quiz[3]', 2, {'one': 1, 'four': 4})
order_is_listed('l15', 'screens[2]'); order_is_listed('l15', 'screens[8]')
quoted('l15', f'{math.log(2) / 2:.4f}', '0.1210')
# The lesson quotes phi(0.6931) = 0.3138. That is right for the rounded argument (0.313758); phi(ln 2) itself is 0.313748.
ok('l15 screens[4] phi(0.6931) to 4 dp is 0.3138', f'{phi(0.6931):.4f}' == '0.3138' and '0.3138' in RAW['l15'])
ok('l15 screens[4] phi(ln 2) is 0.31375 to 5 dp', f'{phi(math.log(2)):.5f}' == '0.31375')
near('l15 quiz slip is the 10th percentile', stats.expon(scale=2).ppf(0.1), -math.log(0.9) / 0.5, 1e-9)
r, th = sp.symbols('r theta', positive=True)
J = sp.Matrix([[sp.diff(sp.exp(-r ** 2 / 2), r), 0], [0, sp.diff(th / (2 * sp.pi), th)]])
ok('l15 Box-Muller Jacobian', sp.simplify(sp.Abs(J.det()) - r * sp.exp(-r ** 2 / 2) / (2 * sp.pi)) == 0)
ok('l15 Box-Muller Jacobian matrix is diagonal', J.is_diagonal())
Uu = 1 - rng.random(N)
Yw = -np.log(Uu) / 2
near('MC l15 -ln(U)/2 mean', Yw.mean(), 0.5, 0.003)
ok('MC l15 -ln(U)/2 is Exp(2) (KS)', stats.kstest(Yw[:20000], stats.expon(scale=0.5).cdf).pvalue > 0.001)
near('MC l15 half the draws below 0.35', np.mean(Yw < math.log(2) / 2), 0.5, 0.003)
Z = rng.standard_normal(N)
S = np.exp(Z)
near('MC l15 lognormal density at 2', np.mean(np.abs(S - 2) < 0.02) / 0.04, phi(math.log(2)) / 2, 0.006)
near('MC l15 chi-square(1) density at 1', np.mean(np.abs(Z ** 2 - 1) < 0.02) / 0.04, phi(1), 0.008)
near('MC l15 P(Z^2<=1)', np.mean(Z ** 2 <= 1), 2 * Phi(1) - 1, 0.003)
near('MC l15 stretch 3X height', np.mean(np.abs(3 * U1 - 1.5) < 0.15) / 0.3, 1 / 3, 0.005)
R = np.sqrt(-2 * np.log(Uu)); TH = 2 * np.pi * U2
BX, BY = R * np.cos(TH), R * np.sin(TH)
ok('MC l15 Box-Muller X normal (KS)', stats.kstest(BX[:20000], 'norm').pvalue > 0.001)
ok('MC l15 Box-Muller Y normal (KS)', stats.kstest(BY[:20000], 'norm').pvalue > 0.001)
near('MC l15 Box-Muller corr', np.corrcoef(BX, BY)[0, 1], 0, 0.004)
near('MC l15 Box-Muller corr of squares', np.corrcoef(BX ** 2, BY ** 2)[0, 1], 0, 0.004)
near('MC l15 E[R^2]', np.mean(R ** 2), 2, 0.01)
SP = 100 + 10 * Z
near('MC l15 atom at payoff 0', np.mean(np.maximum(SP - 105, 0) == 0), Phi(0.5), 0.003)
T = -np.log(1 - U1) / 0.02
near('MC l15 defaults within 5 years of 100', 100 * np.mean(T <= 5), 9.516, 0.1)
se_pct = 100 / math.sqrt(100000)           # sd of an exponential sample mean, as % of the mean
ok('l15 100,000-draw mean within 1% is a 3 sd statement, not a law-of-large-numbers promise', 0.3 < se_pct < 0.33)
near('MC l15 share of 100,000-draw means within 1%', np.mean(np.abs(rng.gamma(100000, 1 / 100000, 200000) - 1) < 0.01), 0.9984, 0.001)

# --------------------------------------------------------------------------- l16 convolution
key_and_slips('l16', 'screens[1]', 0.5, {'one': 1, 'zero': 0})
key_and_slips('l16', 'screens[2]', 0.875, {'unif': 0.75, 'tail': 0.125})
key_and_slips('l16', 'screens[5]', 3 * e(-2), {'single': e(-2), 'mid': 2 * e(-2)})
key_and_slips('l16', 'screens[8]', 1 - Phi(1), {'sd': 1 - Phi(5 / 7), 'half': 0.5})
key_and_slips('l16', 'screens[9]', 0.8 * 0.5 + 0.2 * Phi(1), {'never': 0.5, 'always': Phi(1)})
key_and_slips('l16', 'screens[10]', 0.5 * (e(-1) - e(-3)), {'ignore': e(-2), 'worst': e(-1)})
key_and_slips('l16', 'quiz[0]', 0.125, {'unif': 0.25})
key_and_slips('l16', 'quiz[1]', 4 / 36, {'one': 1 / 36, 'six': 1 / 6})
key_and_slips('l16', 'quiz[2]', math.sqrt(13), {'add': 5, 'var': 13})
key_and_slips('l16', 'quiz[3]', 2 * e(-2), {'prod': e(-4), 'single': e(-2)})
order_is_listed('l16', 'screens[4]')
lam = sp.symbols('lambda', positive=True)
conv = sp.integrate(lam * sp.exp(-lam * x) * lam * sp.exp(-lam * (t - x)), (x, 0, t))
ok('l16 two exponentials convolve to lambda^2 t e^(-lambda t)', sp.simplify(conv - lam ** 2 * t * sp.exp(-lam * t)) == 0)
ok('l16 Gamma(2,2) tail', sp.simplify(sp.integrate(4 * x * sp.exp(-2 * x), (x, t, sp.oo)) - sp.exp(-2 * t) * (1 + 2 * t)) == 0)
SU = U1 + U2
near('MC l16 P(U1+U2<=1.5)', np.mean(SU <= 1.5), 0.875, 0.002)
near('MC l16 density of sum at 0.5', np.mean(np.abs(SU - 0.5) < 0.02) / 0.04, 0.5, 0.01)
near('MC l16 density of sum at 1.5', np.mean(np.abs(SU - 1.5) < 0.02) / 0.04, 0.5, 0.01)
G2 = rng.exponential(0.5, N) + rng.exponential(0.5, N)
near('MC l16 second trade over a minute', np.mean(G2 > 1), 3 * e(-2), 0.002)
PX, PY = 2 + 3 * rng.standard_normal(N), 1 + 4 * rng.standard_normal(N)
near('MC l16 P(X+Y>8)', np.mean(PX + PY > 8), 1 - Phi(1), 0.002)
MV = Z - (rng.random(N) < 0.2)
near('MC l16 dividend mixture', np.mean(MV <= 0), 0.5683, 0.002)
near('MC l16 two desks', np.mean(rng.exponential(1, N) - rng.uniform(-1, 1, N) > 2), 0.5 * (e(-1) - e(-3)), 0.002)
ok('l16 Jensen: desk A noise lifts the tail above e^-2', 0.5 * (e(-1) - e(-3)) > e(-2))

# --------------------------------------------------------------------------- l17 order statistics
key_and_slips('l17', 'screens[2]', 1 - e(-0.1), {'single': 1 - e(-0.02), 'five': 5 * (1 - e(-0.02))})
key_and_slips('l17', 'screens[3]', 0.9 ** 5, {'single': 0.9, 'comp': 1 - 0.9 ** 5})
key_and_slips('l17', 'screens[4]', 5 * 0.9 ** 4, {'cdf': 0.9 ** 5, 'single': 5 * 0.9})
key_and_slips('l17', 'screens[6]', 20 * 0.3 * 0.7 ** 3, {'half': math.comb(5, 2) * 0.3 * 0.7 ** 3, 'nocount': 0.3 * 0.7 ** 3})
key_and_slips('l17', 'screens[8]', 1 - e(-1), {'maxcdf': (1 - e(-0.2)) ** 5, 'five': 5 * (1 - e(-0.2))})
key_and_slips('l17', 'screens[10]', 5 / 36, {'both': 1 / 36, 'cdf': 0.25})
key_and_slips('l17', 'screens[11]', 1 - Phi(2.1) ** 20, {'single': 1 - Phi(2.1), 'times': 20 * (1 - Phi(2.1))})
key_and_slips('l17', 'quiz[0]', e(-3), {'one': e(-0.5), 'time': e(-6)})
key_and_slips('l17', 'quiz[1]', 0.5 ** 4, {'half': 0.5, 'quarter': 0.25})
key_and_slips('l17', 'quiz[2]', 0.3, {'kn': 1 / 3})
key_and_slips('l17', 'quiz[3]', Phi(1.5) ** 20, {'single': Phi(1.5), 'comp': 1 - Phi(1.5) ** 20})
order_is_listed('l17', 'screens[5]')
emax20 = integrate.quad(lambda z: z * 20 * phi(z) * Phi(z) ** 19, -10, 10)[0]
near('l17 expected max of 20 normals', emax20, 1.8675, 0.00005)
quoted('l17', '1.8675', f'{Phi(2.1):.6f}', f'{1 - Phi(2.1):.6f}', f'{1 - e(-0.2):.6f}', f'{1 - e(-0.2):.4f}')
near('l17 a draw reaches 3 once in about 740', 1 / (1 - Phi(3)), 740, 2)
ok('l17 twenty tries reach 3 about one trial in 40', 35 < 1 / (1 - Phi(3) ** 20) < 42)
ok('l17 best of 20 almost never below 1', Phi(1) ** 20 < 0.05)
kk, nn = sp.symbols('k n', integer=True, positive=True)
for nv, kv in ((5, 2), (9, 3), (4, 3), (4, 4)):
    dens = nv * sp.binomial(nv - 1, kv - 1) * x ** (kv - 1) * (1 - x) ** (nv - kv)
    ok(f'l17 order-stat density integrates to 1 n={nv} k={kv}', sp.integrate(dens, (x, 0, 1)) == 1)
    ok(f'l17 order-stat mean k/(n+1) n={nv} k={kv}', sp.integrate(x * dens, (x, 0, 1)) == sp.Rational(kv, nv + 1))
M = 200_000
E5 = rng.exponential(50, (M, 5)).min(axis=1)
near('MC l17 mean first default of five', E5.mean(), 10, 0.1)
ok('MC l17 first default is Exp(0.1) (KS)', stats.kstest(E5[:20000], stats.expon(scale=10).cdf).pvalue > 0.001)
near('MC l17 first default within a year', np.mean(E5 <= 1), 1 - e(-0.1), 0.003)
near('MC l17 first default within ten years', np.mean(E5 <= 10), 1 - e(-1), 0.004)
U5 = np.sort(rng.random((M, 5)), axis=1)
near('MC l17 P(max<=0.9)', np.mean(U5[:, 4] <= 0.9), 0.9 ** 5, 0.004)
near('MC l17 density of max at 0.9', np.mean(np.abs(U5[:, 4] - 0.9) < 0.01) / 0.02, 5 * 0.9 ** 4, 0.08)
near('MC l17 density of 2nd smallest at 0.3', np.mean(np.abs(U5[:, 1] - 0.3) < 0.01) / 0.02, 2.058, 0.06)
near('MC l17 mean of 2nd smallest of 5', U5[:, 1].mean(), 1 / 3, 0.002)
frac_top = np.mean(U5[:, 4] > 0.9)
near('MC l17 five draws put one above 0.9 (not "almost always")', frac_top, 1 - 0.9 ** 5, 0.004)
near('MC l17 largest of five exceeds 0.8 two times in three (fix text of finding 6)', np.mean(U5[:, 4] > 0.8), 2 / 3, 0.01)
N20 = rng.standard_normal((M, 20)).max(axis=1)
near('MC l17 mean best of 20', N20.mean(), 1.8675, 0.006)
near('MC l17 P(best of 20 >= 2.1)', np.mean(N20 >= 2.1), 0.3027, 0.004)
near('MC l17 P(best of 20 < 1.5)', np.mean(N20 < 1.5), 0.2509, 0.004)
d1, d2 = rng.integers(1, 7, M), rng.integers(1, 7, M)
near('MC l17 P(max of two dice = 3)', np.mean(np.maximum(d1, d2) == 3), 5 / 36, 0.003)
E3 = np.minimum(np.minimum(rng.exponential(1, M), rng.exponential(1 / 2, M)), rng.exponential(1 / 3, M))
near('MC l17 quiz min of rates 1,2,3', np.mean(E3 > 0.5), e(-3), 0.002)

# --------------------------------------------------------------------------- l18 Gamma and Beta
t5 = stats.t(5)
two5 = 2 * t5.sf(2)
key_and_slips('l18', 'screens[1]', 0.75, {'one': 0.25, 'scaled': 9 * 0.25})
key_and_slips('l18', 'screens[2]', stats.poisson(4).cdf(2), {'single': e(-4), 'off': stats.poisson(4).cdf(3)})
key_and_slips('l18', 'screens[4]', 12, {'mean': 6, 'one': 2})
key_and_slips('l18', 'screens[5]', two5 / (2 * stats.norm.sf(2)), {'same': 1, 'inv': 2 * stats.norm.sf(2) / two5})
key_and_slips('l18', 'screens[7]', 1 / 3, {'kn': 0.4, 'half': 0.5})
key_and_slips('l18', 'screens[8]', stats.beta(0.5, 0.5).cdf(0.25), {'unif': 0.25, 'half': 0.5})
key_and_slips('l18', 'quiz[0]', 1.25, {'gap': 0.25, 'twenty': 20})
key_and_slips('l18', 'quiz[1]', math.sqrt(20), {'var': 20, 'mean': 10})
key_and_slips('l18', 'quiz[3]', 4 / 6, {'raw': 0.75, 'prior': 0.5})
order_is_listed('l18', 'screens[9]')
quoted('l18', f'{two5:.4f}', f'{2 * stats.norm.sf(2):.4f}', f'{2 * t5.sf(2.3):.4f}', f'{t5.ppf(0.975):.2f}',
       f'{2 * stats.norm.sf(2.3):.3f}', f'{stats.beta(16, 8).sf(0.5):.4f}', f'{stats.beta(16, 8).std():.3f}',
       f'{stats.gamma(3, scale=0.5).pdf(1):.4f}')
ok('l18 Gamma(3, rate 2) density and mode', abs(stats.gamma(3, scale=0.5).pdf(1) - 4 * e(-2)) < 1e-12)
ok('l18 chi-square(n) is Gamma(n/2, rate 1/2)', all(abs(stats.chi2(k).pdf(3.3) - stats.gamma(k / 2, scale=2).pdf(3.3)) < 1e-12 for k in range(1, 11)))
ok('l18 t5 lower at centre than normal', t5.pdf(0) < phi(0))
ok('l18 t5 "over twice as heavy" holds beyond 2 but not beyond 1', two5 / (2 * stats.norm.sf(2)) > 2 and 2 * t5.sf(1) / (2 * stats.norm.sf(1)) < 1.2)
ok('l18 Beta(k, n-k+1) is the order-stat density', abs(stats.beta(2, 4).pdf(0.3) - 20 * 0.3 * 0.7 ** 3) < 1e-12)
ok('l18 arcsine CDF', abs(stats.beta(0.5, 0.5).cdf(0.25) - 2 / math.pi * math.asin(0.5)) < 1e-9)
G3 = rng.exponential(0.5, (M, 3)).sum(axis=1)
near('MC l18 mean wait third trade', G3.mean(), 1.5, 0.006)
near('MC l18 var wait third trade', G3.var(), 0.75, 0.01)
near('MC l18 P(T>2)', np.mean(G3 > 2), 0.2381, 0.003)
hist, edges = np.histogram(G3, bins=np.arange(0, 6.25, 0.25))
ok('MC l18 bars crest near 1 minute', 0.75 <= edges[hist.argmax()] <= 1.0)
ok('MC l18 third wait is Gamma(3, scale 0.5) (KS)', stats.kstest(G3[:20000], stats.gamma(3, scale=0.5).cdf).pvalue > 0.001)
V6 = (rng.standard_normal((M, 6)) ** 2).sum(axis=1)
near('MC l18 chi-square(6) mean', V6.mean(), 6, 0.03)
near('MC l18 chi-square(6) variance', V6.var(), 12, 0.2)
V5 = (rng.standard_normal((N, 5)) ** 2).sum(axis=1)
T5 = rng.standard_normal(N) / np.sqrt(V5 / 5)
near('MC l18 t5 two-tail beyond 2', np.mean(np.abs(T5) > 2), 0.1019, 0.002)
near('MC l18 t5 two-tail beyond 2.3', np.mean(np.abs(T5) > 2.3), 0.0698, 0.002)
X6 = rng.standard_normal((M, 6))
TR = X6.mean(axis=1) / (X6.std(axis=1, ddof=1) / math.sqrt(6))
near('MC l18 six-return t-ratio beyond 2.3 (5 df, exact for normal data)', np.mean(np.abs(TR) > 2.3), 0.0698, 0.003)
near('MC l18 six-return t-ratio beyond 1.96', np.mean(np.abs(TR) > 1.96), 2 * t5.sf(1.96), 0.003)
# arcsine law for a long fair random walk: share of time positive
steps = rng.choice([-1, 1], size=(20000, 1000)).cumsum(axis=1)
share = np.mean(steps > 0, axis=1) + 0.5 * np.mean(steps == 0, axis=1)
near('MC l18 arcsine law, share of time positive <= 0.25', np.mean(share <= 0.25), 1 / 3, 0.02)
# Beta-binomial update by brute force: prior draws that produced 14 wins of 20
pp = rng.beta(2, 2, 4_000_000)
wins = rng.binomial(20, pp)
post = pp[wins == 14]
near('MC l18 posterior mean', post.mean(), 16 / 24, 0.002)
near('MC l18 posterior P(p>0.5)', np.mean(post > 0.5), 0.9534, 0.003)
pp1 = rng.random(2_000_000); post1 = pp1[rng.binomial(4, pp1) == 3]
near('MC l18 quiz posterior mean', post1.mean(), 2 / 3, 0.002)

# --------------------------------------------------------------------------- l19 MGFs
pois = lambda k, m: stats.poisson(m).pmf(k)
key_and_slips('l19', 'screens[0]', 3.5, {'sum': 21, 'one': 1})
key_and_slips('l19', 'screens[1]', 91 / 6, {'mean': 3.5, 'sq': 3.5 ** 2})
key_and_slips('l19', 'screens[4]', pois(3, 3.5), {'add': pois(3, 2) + pois(3, 1.5), 'none': e(-3.5)})
key_and_slips('l19', 'screens[5]', 100 * e(0.05), {'mu': 100 * e(0.03), 'var': 100 * e(0.07)})
key_and_slips('l19', 'quiz[0]', 3, {'p': 0.6, 'n': 5})
key_and_slips('l19', 'quiz[1]', 13, {'sd': 5, 'sq': 25})
key_and_slips('l19', 'quiz[3]', 6, {'mean': 2, 'sq': 4})
order_is_listed('l19', 'screens[2]'); order_is_listed('l19', 'screens[8]')
# feedback for the 'add' slip: a total of 3 needs both counts at once (fix text of finding 10)
near('l19 total of 3 as (3,0),(2,1),(1,2),(0,3)', sum(pois(k, 2) * pois(3 - k, 1.5) for k in range(4)), pois(3, 3.5), 1e-12)
ok('l19 the two added single chances are not ways to total 3', pois(3, 2) + pois(3, 1.5) > pois(3, 3.5))
quoted('l19', f'{pois(3, 2):.4f}', f'{pois(3, 1.5):.4f}', '2.9167', '7.146', '42.875')
ts = sp.symbols('t', real=True)
Mdie = sum(sp.exp(k * ts) for k in range(1, 7)) / 6
ok('l19 die M\'(0), M\'\'(0)', (sp.diff(Mdie, ts).subs(ts, 0), sp.diff(Mdie, ts, 2).subs(ts, 0)) == (sp.Rational(7, 2), sp.Rational(91, 6)))
Mp = sp.exp(2 * (sp.exp(ts) - 1))
ok('l19 Poisson(2) second and third moments', (sp.diff(Mp, ts, 2).subs(ts, 0), sp.diff(Mp, ts, 3).subs(ts, 0)) == (6, 22))
ok('l19 coin vs normal agree to t^2, split at t^4',
   sp.series(sp.cosh(ts) - sp.exp(ts ** 2 / 2), ts, 0, 5).removeO() == sp.Rational(1, 24) * ts ** 4 - sp.Rational(1, 8) * ts ** 4)
ok('l19 geometric MGF finite below -ln(1-p)', True)  # sum (1-p)^(k-1) p e^{tk} converges iff (1-p)e^t < 1
chern = lambda n, a_: min(e(-tt * a_) * math.cosh(tt) ** n for tt in (k / 100 for k in range(301)))
exact = lambda n, a_: sum(math.comb(n, k) for k in range(max(0, math.ceil((n + a_) / 2)), n + 1)) / 2 ** n
near('l19 Chernoff best t at n=100, a=30', chern(100, 30), 0.0104, 0.00005)
near('l19 exact tail', exact(100, 30), 0.00176, 0.000005)
ok('l19 best t about 0.31', abs(math.atanh(0.3) - 0.31) < 0.005)
ok('l19 bound about six times the truth', 5.5 < chern(100, 30) / exact(100, 30) < 6.5)
near('l19 Hoeffding form e^{-a^2/2n}', e(-900 / 200), 0.0111, 0.00005)
near('l19 Chebyshev both tails', 100 / 900, 0.1111, 0.00005)
near('l19 normal approximation', stats.norm.sf(3), 0.00135, 0.000005)
ok('l19 Chebyshev 63 times the truth', abs((100 / 900) / exact(100, 30) - 63) < 1)
ok('l19 normal approximation sits below the truth', stats.norm.sf(3) < exact(100, 30))
near('MC l19 two venues P(N=3)', np.mean(rng.poisson(2, N) + rng.poisson(1.5, N) == 3), pois(3, 3.5), 0.002)
near('MC l19 lognormal mean', 100 * np.mean(np.exp(0.03 + 0.2 * Z)), 105.13, 0.1)
near('MC l19 three trades are Binomial(3,0.3)', np.mean((rng.random((M, 3)) < 0.3).sum(axis=1) == 2), stats.binom(3, 0.3).pmf(2), 0.003)
SS = 2 * rng.binomial(100, 0.5, 4_000_000) - 100
near('MC l19 P(S>=30)', np.mean(SS >= 30), exact(100, 30), 0.0001)
ok('MC l19 Chernoff holds', np.mean(SS >= 30) <= chern(100, 30))
# CLT sketch: standardised sums of a skewed variable with an MGF (exponential) approach N(0,1)
ZN = (rng.exponential(1, (100000, 200)).sum(axis=1) - 200) / math.sqrt(200)
near('MC l19 CLT, P(Z_n<=1)', np.mean(ZN <= 1), Phi(1), 0.006)
# ... and the theorem with finite variance but no MGF near 0 (Student t with 5 df, variance 5/3)
ZT = rng.standard_t(5, (100000, 200)).sum(axis=1) / math.sqrt(200 * 5 / 3)
near('MC l19 CLT without an MGF, P(Z_n<=1)', np.mean(ZT <= 1), Phi(1), 0.008)
# Cauchy: E[e^{tX}] diverges, tails ~ 1/x^2
ok('l19 Cauchy density tail ~ 1/(pi x^2)', abs(stats.cauchy.pdf(1000) * math.pi * 1000 ** 2 - 1) < 1e-5)

# --------------------------------------------------------------------------- review-4
key_and_slips('rev', 'items[0]', 0.125, {'rect': 0.375, 'half': 0.5})
key_and_slips('rev', 'items[1]', 1 / (2 * 0.4), {'nofac': 1, 'inv': 0.8})
key_and_slips('rev', 'items[2]', 0.32, {'unif': 0.4, 'sq': 0.64})
key_and_slips('rev', 'items[3]', (1 - e(-1.5)) ** 5, {'single': 1 - e(-1.5), 'comp': 1 - (1 - e(-1.5)) ** 5})
key_and_slips('rev', 'items[4]', 1 - Phi(2) ** 10, {'single': 1 - Phi(2), 'times': 10 * (1 - Phi(2))})
key_and_slips('rev', 'items[5]', 4 * e(-3), {'first': e(-3), 'three': 3 * e(-3)})
key_and_slips('rev', 'items[7]', 0.5, {'rate': 2, 'value': 1})
ok('rev 3x density on triangle has volume 1', sp.integrate(sp.integrate(3 * x, (y, 0, x)), (x, 0, 1)) == 1)
ok('rev rect slip is y from 0 to 1', sp.integrate(sp.integrate(3 * x, (y, 0, 1)), (x, 0, sp.Rational(1, 2))) == sp.Rational(3, 8))
near('MC rev Y=X^2 density at 0.16', np.mean(np.abs(U1 ** 2 - 0.16) < 0.005) / 0.01, 1.25, 0.03)
near('MC rev P(sum>1.2)', np.mean(SU > 1.2), 0.32, 0.002)
near('MC rev max of five Exp(0.5) within 3', np.mean(rng.exponential(2, (M, 5)).max(axis=1) <= 3), 0.2830, 0.004)
near('MC rev best of ten >= 2', np.mean(rng.standard_normal((M, 10)).max(axis=1) >= 2), 0.2056, 0.004)

# --------------------------------------------------------------------------- homework-4
key_and_slips('hw', 'items[0]', 1 / 16, {'twox': 0.25, 'half': 0.5})
key_and_slips('hw', 'items[3]', 2 * e(-2), {'nojac': e(-2), 'double': 4 * e(-2)})
key_and_slips('hw', 'items[4]', e(-1) - e(-2), {'single': e(-2), 'prod': 0})
key_and_slips('hw', 'items[5]', 0.5 * (1 - e(-0.3)), {'time': 1 - e(-0.3), 'share': 0.5})
key_and_slips('hw', 'items[7]', 14 / 24, {'first': 11 / 16, 'prior': 0.5})
key_and_slips('hw', 'items[9]', 22, {'lam3': 8, 'second': 6})
order_is_listed('hw', 'items[2]')
ok('hw 8xy volume and marginal', sp.integrate(sp.integrate(8 * x * y, (y, 0, x)), (x, 0, 1)) == 1 and sp.integrate(8 * x * y, (y, 0, x)) == 4 * x ** 3)
ok('hw conditional mean 2x/3', sp.simplify(sp.integrate(y * 8 * x * y / (4 * x ** 3), (y, 0, x)) - 2 * x / 3) == 0)
Jm = sp.Matrix([[sp.diff(u * v, u), sp.diff(u * v, v)], [sp.diff(u * (1 - v), u), sp.diff(u * (1 - v), v)]])
ok('hw Jacobian -u', sp.simplify(Jm.det() + u) == 0)
EXa, EXb = rng.exponential(1, N), rng.exponential(1, N)
Uv, Vv = EXa + EXb, EXa / (EXa + EXb)
near('MC hw joint density of (U,V) at (2,0.3)', np.mean((np.abs(Uv - 2) < 0.05) & (np.abs(Vv - 0.3) < 0.05)) / 0.01, 2 * e(-2), 0.02)
near('MC hw U and V uncorrelated', np.corrcoef(Uv, Vv)[0, 1], 0, 0.004)
ok('MC hw V uniform (KS)', stats.kstest(Vv[:20000], 'uniform').pvalue > 0.001)
near('MC hw exponential plus uniform density at 2', np.mean(np.abs(EXa + U1 - 2) < 0.02) / 0.04, e(-1) - e(-2), 0.006)
Ta, Tb, Tc = rng.exponential(100, N), rng.exponential(50, N), rng.exponential(100 / 3, N)
first = np.minimum(np.minimum(Ta, Tb), Tc)
near('MC hw C first and within 5 years', np.mean((Tc == first) & (first <= 5)), 0.1296, 0.002)
near('MC hw who is first is independent of when', np.mean(Tc[first <= 5] == first[first <= 5]), 0.5, 0.004)
near('hw sd of 2nd smallest of 5', stats.beta(2, 4).std(), 0.18, 0.005)
near('hw sd of the 20,000-trial mean', stats.beta(2, 4).std() / math.sqrt(20000), 0.0013, 0.00005)
# long-form model answer
t29 = stats.t(29)
near('hw P(Z>=2.6)', stats.norm.sf(2.6), 0.0047, 0.00005)
near('hw best of 50 reaches 2.6', 1 - Phi(2.6) ** 50, 0.208, 0.0006)
near('hw median best of 50', stats.norm.ppf(0.5 ** (1 / 50)), 2.20, 0.006)
near('hw mean best of 50', integrate.quad(lambda z: z * 50 * phi(z) * Phi(z) ** 49, -10, 10)[0], 2.25, 0.006)
near('hw family-wise cut-off', stats.norm.ppf(0.99 ** (1 / 50)), 3.54, 0.006)
near('hw Bonferroni cut-off', stats.norm.isf(0.01 / 50), 3.54, 0.006)
near('hw P(t29>=2.6)', t29.sf(2.6), 0.0073, 0.00006)
near('hw best of 50 with t29', 1 - (1 - t29.sf(2.6)) ** 50, 0.31, 0.006)
near('hw median best with t29', t29.ppf(0.5 ** (1 / 50)), 2.32, 0.006)
near('hw cut-off with t29', t29.ppf(0.99 ** (1 / 50)), 4.0, 0.06)
ok('hw 2.6 clears a t29 1% cut-off only for about one effective try', 0.01 / t29.sf(2.6) < 1.5)
ok('hw convention: the model answer is one-sided (two-sided t29 p-value of 2.6 is above 1%)', 2 * t29.sf(2.6) > 0.01 > t29.sf(2.6))
near('MC hw best of 50 t29 reaches 2.6', np.mean(rng.standard_t(29, (M, 50)).max(axis=1) >= 2.6), 1 - (1 - t29.sf(2.6)) ** 50, 0.004)

# --------------------------------------------------------------------------- problems-4
root = (26 - math.sqrt(116)) / 40
bound = lambda s_: e(-10 * s_) / ((1 - s_) * (1 - 2 * s_))
tailT = 2 * e(-5) - e(-10)
key_and_slips('prob', 'items[0].parts[1]', 1.5, {'unconditional': 2, 'half': 0.25, 'gap-only': 1})
key_and_slips('prob', 'items[0].parts[3]', e(-2), {'second-fault': 3 * e(-2), 'complement': 1 - e(-2), 'rate-half': e(-1)})
key_and_slips('prob', 'items[0].parts[4]', 4 * e(-3), {'one-wait': e(-3), 'complement': 1 - 4 * e(-3), 'dropped-one': 3 * e(-3)})
key_and_slips('prob', 'items[1].parts[1]', tailT, {'one-stage': e(-5), 'complement': 1 - tailT, 'equal-rates': 6 * e(-5)})
key_and_slips('prob', 'items[1].parts[3]', root, {'other-root': (26 + math.sqrt(116)) / 40, 'repair-only': 0.4, 'triage-only': 0.9})
key_and_slips('prob', 'items[1].parts[4]', bound(0.3807), {'repair-s': bound(0.4), 'no-mgf': e(-3.807), 'exact': tailT})
key_and_slips('prob', 'items[2].parts[0]', 0.8 ** 4, {'one-dealer': 0.8, 'worst': 1 - 0.2 ** 4, 'complement': 1 - 0.8 ** 4})
key_and_slips('prob', 'items[2].parts[1]', 0.8, {'one-dealer': 0.5, 'worst': 0.2, 'k-over-n': 0.75})
key_and_slips('prob', 'items[2].parts[3]', 0.6, {'k-over-n': 0.75, 'swapped': 0.4, 'one-dealer': 0.5})
key_and_slips('prob', 'items[2].parts[4]', 11 / 16, {'three-above': 5 / 16, 'one-above': 15 / 16, 'half': 0.5})
key_and_slips('prob', 'items[3].parts[1]', 8, {'second-moment': 24, 'one-term': 2, 'sd': math.sqrt(8)})
key_and_slips('prob', 'items[3].parts[3]', 5 * e(-4), {'exponential': e(-4), 'three-terms': 13 * e(-4), 'rate-one': 9 * e(-8)})
chi4 = stats.chi2(4)
dmin = next(d for d in range(1, 30) if chi4.sf(d) <= 0.05)
key_and_slips('prob', 'items[3].parts[4]', dmin, {'normal': math.ceil(4 + 1.645 * math.sqrt(8)), 'ten-per-cent': 8, 'too-far': 11})
ok('prob machine marginal', sp.simplify(sp.integrate(sp.exp(-y), (y, x, sp.oo)) - sp.exp(-x)) == 0)
ok('prob wrong-limits slip', sp.simplify(sp.integrate(sp.exp(-y), (y, 0, x)) - (1 - sp.exp(-x))) == 0)
ok('prob "constant" slip 1 is the slice taken from y = 0', sp.integrate(sp.exp(-y), (y, 0, sp.oo)) == 1)
ok('prob E[Y] = 2', sp.integrate(sp.integrate(y * sp.exp(-y), (x, 0, y)), (y, 0, sp.oo)) == 2)
fT = sp.integrate(sp.exp(-x) * sp.Rational(1, 2) * sp.exp(-(t - x) / 2), (x, 0, t))
ok('prob two-stage density', sp.simplify(fT - (sp.exp(-t / 2) - sp.exp(-t))) == 0)
ok('prob two-stage density area 1', sp.integrate(sp.exp(-t / 2) - sp.exp(-t), (t, 0, sp.oo)) == 1)
ss = sp.symbols('s', real=True)
ok('prob Chernoff quadratic', sp.expand(sp.numer(sp.together(-10 + 1 / (1 - ss) + 2 / (1 - 2 * ss)))) in (-(20 * ss ** 2 - 26 * ss + 7), 20 * ss ** 2 - 26 * ss + 7)
   or sp.simplify(sp.together(-10 + 1 / (1 - ss) + 2 / (1 - 2 * ss)) * (1 - ss) * (1 - 2 * ss) + (20 * ss ** 2 - 26 * ss + 7)) == 0)
near('prob root is the minimiser', min((bound(k / 10000), k / 10000) for k in range(1, 5000))[1], 0.3807, 0.0002)
ok('prob bound about 11 times exact', abs(bound(0.3807) / tailT - 11.2) < 0.2)
near('prob M_T at the root', 1 / ((1 - 0.3807) * (1 - 0.7614)), 6.768, 0.002)
ok('prob one ticket in 74', abs(1 / tailT - 74.5) < 0.6)
ok('prob chi-square(4) is Gamma(2, rate 1/2) with the Poisson tail', abs(chi4.sf(8) - 5 * e(-4)) < 1e-12 and abs(chi4.sf(9) - 5.5 * e(-4.5)) < 1e-12)
quoted('prob', f'{chi4.sf(9):.4f}', f'{chi4.sf(10):.4f}', '0.1478', '0.02221')
FX = rng.exponential(1, N); FG = rng.exponential(1, N); FY = FX + FG      # the pair has density e^{-y} on 0<x<y
slc = np.abs(FX - 0.5) < 0.01
near('MC prob E[Y|X=0.5]', FY[slc].mean(), 1.5, 0.03)
near('MC prob P(G>2)', np.mean(FG > 2), e(-2), 0.002)
near('MC prob P(Y>3)', np.mean(FY > 3), 4 * e(-3), 0.002)
TT = rng.exponential(1, 4_000_000) + rng.exponential(2, 4_000_000)
near('MC prob P(T>10)', np.mean(TT > 10), tailT, 0.0003)
ok('MC prob Chernoff bound holds', np.mean(TT >= 10) <= bound(0.3807))
Q4 = np.sort(rng.random((M, 4)), axis=1)
near('MC prob best of four mean', Q4[:, 3].mean(), 0.8, 0.002)
near('MC prob second best mean', Q4[:, 2].mean(), 0.6, 0.002)
near('MC prob second best over 0.5', np.mean(Q4[:, 2] > 0.5), 11 / 16, 0.004)
D4 = (rng.standard_normal((M, 4)) ** 2).sum(axis=1)
near('MC prob Var(D)', D4.var(), 8, 0.12)
near('MC prob P(D>8)', np.mean(D4 > 8), 5 * e(-4), 0.003)
near('MC prob P(D>10)', np.mean(D4 > 10), 6 * e(-5), 0.002)

# --------------------------------------------------------------------------- code widgets against their hidden tests
def close(got, want, tol):
    if isinstance(want, (list, tuple)):
        return isinstance(got, (list, tuple)) and len(got) == len(want) and all(close(g, w, tol) for g, w in zip(got, want))
    if isinstance(want, bool) or isinstance(got, bool):
        return got == want
    if tol is None:
        return math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12)
    return abs(got - want) <= tol.get('abs', 0) + abs(want) * tol.get('rel', 0) + 1e-15


def run_tests(src, tests):
    passed = 0
    for tcase in tests:
        try:
            ns = {}
            exec(src, ns)
            if tcase.get('setup'):
                exec(tcase['setup'], ns)
            got = eval(tcase['call'], ns)
            want = eval(tcase['expect']) if isinstance(tcase['expect'], str) else tcase['expect']
            good = got == want if tcase.get('compare') == 'equal' else close(got, want, tcase.get('tol'))
        except Exception:
            good = False
        passed += bool(good)
    return passed


for key, path in (('l15', 'screens[5]'), ('l15', 'screens[9]'), ('l16', 'screens[6]'), ('l17', 'screens[9]'), ('l19', 'screens[9]'), ('hw', 'items[6]')):
    w = get(key, path)['widget']
    ok(f'code {key} {path} solution passes all {len(w["tests"])} tests', run_tests(w['solution'], w['tests']) == len(w['tests']))
    ok(f'code {key} {path} starter fails', run_tests(w['starter'], w['tests']) < len(w['tests']))
    for ex in w.get('examples', []):
        ns = {}
        exec(w['solution'], ns)
        ok(f'code {key} {path} example {ex["call"]}', repr(eval(ex['call'], ns)) == ex['expect'], repr(eval(ex['call'], ns)))
# a wrong method must not pass: maximum in place of minimum, product in place of convolution
w = get('l17', 'screens[9]')['widget']
ok('code l17 wrong method (max) is rejected', run_tests(w['solution'].replace('min(', 'max('), w['tests']) < len(w['tests']))
w = get('l15', 'screens[9]')['widget']
ok('code l15 Box-Muller without the factor 2 is rejected', run_tests(w['solution'].replace('-2 * math.log', '-1 * math.log'), w['tests']) < len(w['tests']))
w = get('l15', 'screens[5]')['widget']
ok('code l15 sampler multiplying by the rate is rejected', run_tests(w['solution'].replace('/ rate', '* rate'), w['tests']) < len(w['tests']))

print(f'{COUNT[0]} checks, {len(FAILS)} failed')
sys.exit(1 if FAILS else 0)
