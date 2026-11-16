"""Recompute every number in app/content/courses/coint/problems-<n>.json twice (docs/briefs/chained.md check 1).

Method 1 is exact where it can be (fractions, sympy, the closed form the lessons teach). Method 2 takes another
route: an OLS fit with statsmodels on data built to have the stated moments, a long simulation, a loop that applies
the trading rule day by day, a bisection, an enumeration of every sequence of checks, numpy's eigen solver. For
each numeric part the script checks: the two methods agree; the key is within its tol of the value; every `wrong`
value matches its named slip, lies outside the key's band and does not overlap another; byKey covers the wrongs.
Choice parts check the keyed option and that every distractor has a byKey line. Printed numbers in feedback and
explain are checked with `said`. Exit 0 when all pass.

Run from anywhere: <scratchpad>/venv/bin/python docs/reports/problems-coint-numbers.py
"""
import itertools
import json
import math
import os
import sys
import warnings
from fractions import Fraction as F

import numpy as np
import sympy as sp
import statsmodels.api as sm
from scipy.optimize import brentq
from statsmodels.tsa.adfvalues import mackinnoncrit

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'coint')
fails, checks = [], 0
rng = np.random.default_rng(20261116)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    d = json.load(open(os.path.join(COURSE, f'problems-{n}.json')))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'coint', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: no difficulty 5')
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for it in d['items'] for p in it['parts'])
    total = sum(len(it['parts']) for it in d['items'])
    ok(3 * typed >= 2 * total, f'problems-{n}: typed parts {typed} of {total}')
    for it in d['items']:
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: part count')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def num(items, iid, k, exact, alt, slips, agree=1e-9):
    """exact: method 1; alt: method 2; slips: {wrong id: value the slip gives}."""
    p = part(items, iid, k)
    w = p['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= wt + 1e-12, f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    bk = p['feedback'].get('byKey', {})
    ok(set(bk) == set(wrongs), f'{tag}: byKey {sorted(bk)} vs wrongs {sorted(wrongs)}')


def cho(items, iid, k, key):
    p = part(items, iid, k)
    w = p['widget']
    tag = f'{iid} p{k}'
    right = [o['id'] for o in w['options'] if o.get('correct')]
    ok(right == [key], f'{tag}: keyed {right} vs {key}')
    for o in w['options']:
        if not o.get('correct'):
            ok(bool(o.get('why')) and o['id'] in p['feedback'].get('byKey', {}), f'{tag}: {o["id"]} lacks why/byKey')


def said(items, iid, k, token):
    p = part(items, iid, k)
    txt = json.dumps([p['question'], p['feedback'], p['explain'], items[iid]['prose']], ensure_ascii=False)
    txt = txt.replace('{,}', ',')
    ok(token in txt, f'{iid} p{k}: "{token}" not printed')


def r(x, d):
    return round(float(x) + 0.0, d)


def ols_t_with_r(n, rho):
    """Build x, y of length n whose sample correlation is exactly rho; return |t| of the slope from statsmodels."""
    x = rng.standard_normal(n)
    z = rng.standard_normal(n)
    x = (x - x.mean()) / x.std()
    z = z - z.mean()
    z = z - (z @ x) / (x @ x) * x
    z = z / z.std()
    y = rho * x + math.sqrt(1 - rho ** 2) * z
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    return abs(fit.tvalues[1])


def hl(b):
    return math.log(0.5) / math.log(1 + b)


# ------------------------------------------------------------------ level 1
P = load(1)

# p-paper-mill-multiple (fix pass, review finding 1: part 1 is now the walk part's daily variance)
it = 'p-paper-mill-multiple'
var_u = F(1, 4)                                        # the prose states a long-run sd of 0.50
slope = F(15, 100) ** 2 * F(16, 100)                   # 0.0036 a day
day_moves = 0.15 * rng.normal(0, 0.40, 2_000_000)
num(P, it, 1, slope, day_moves.var(), {'sd-not-squared': 0.15 ** 2 * 0.40, 'multiple-not-squared': 0.15 * 0.16, 'neither-squared': 0.15 * 0.40}, agree=3e-5)
said(P, it, 1, '0.0225'); said(P, it, 1, '0.16'); said(P, it, 1, '£0.06')
v500 = slope * 500 + var_u
mc = 0.15 * rng.normal(0, 0.40, (20000, 500)).sum(axis=1) + rng.normal(0, 0.5, 20000)
num(P, it, 2, math.sqrt(v500), mc.std(), {'no-u': math.sqrt(1.8), 'variance': v500, 'sd-not-squared': math.sqrt(0.0225 * 0.4 * 500 + 0.25),
                                          'multiple-not-squared': math.sqrt(0.15 * 0.16 * 500 + 0.25)}, agree=0.03)
said(P, it, 2, '0.0036'); said(P, it, 2, '0.25')
ok(slope == F(36, 10000), 'p1 walk slope 0.0036')
day = next(t for t in itertools.count(1) if slope * t + var_u > 4 * var_u)
t_exact = math.floor((4 * var_u - var_u) / slope) + 1
num(P, it, 3, t_exact, day, {'no-subtract': math.ceil(1 / 0.0036), 'doubled-variance': next(t for t in itertools.count(1) if slope * t + var_u > 2 * var_u),
                             'round-down': t_exact - 1})
ok(slope * 208 + var_u < 1 and abs(float(slope * 208 + var_u) - 0.9988) < 1e-9, 'p1 day 208 variance 0.9988')
said(P, it, 3, '208.3')
cho(P, it, 4, 'near-true')
ok(float(slope * 1600 + var_u) == 6.01, 'p1 day 1,600 variance 6.01')
said(P, it, 4, '6.01')

# p-cocoa-chip-levels
it = 'p-cocoa-chip-levels'
tx = lambda rr, n: abs(rr) * math.sqrt((n - 2) / (1 - rr ** 2))
num(P, it, 1, tx(0.45, 750), ols_t_with_r(750, -0.45), {'no-root': 0.45 * 748 / 0.7975, 'r-squared': 0.2025 * math.sqrt(748 / 0.7975),
                                                       'one-minus-r': 0.45 * math.sqrt(748 / 0.55)}, agree=1e-6)
said(P, it, 1, '937.9'); said(P, it, 1, '30.63')
r_star = math.sqrt(1.96 ** 2 / (748 + 1.96 ** 2))
num(P, it, 2, r_star, brentq(lambda q: tx(q, 750) - 1.96, 1e-6, 0.5), {'r-squared': r_star ** 2, 'drop-one-minus': 1.96 / math.sqrt(748)}, agree=1e-9)
said(P, it, 2, '0.00511')
num(P, it, 3, tx(0.45, 1500), ols_t_with_r(1500, -0.45), {'doubled': 2 * r(tx(0.45, 750), 2), 'unchanged': tx(0.45, 750)}, agree=1e-6)
said(P, it, 3, '43.34')
said(P, it, 1, '30.63')
ok(r(13.78 / 1.96, 2) == 7.03, 'p2 13.78 clears 1.96 seven times over')
ok(r(13.78 * math.sqrt(1498 / 748), 2) == 19.50, 'p2 part 3 from the restated 13.78 gives 19.50')
said(P, it, 3, '13.78')
cho(P, it, 4, 'spurious')
crit500 = mackinnoncrit(N=2, regression='c', nobs=499)
ok(abs(crit500[0] + 3.90) < 0.03 and abs(crit500[1] + 3.34) < 0.02 and abs(crit500[2] + 3.04) < 0.02, f'MacKinnon 500 {crit500}')
ok(-2.41 > crit500[2], 'p2 -2.41 above the 10% value')

# p-cable-sample-length
it = 'p-cable-sample-length'
ph = sp.Rational(96, 100)
gam = ph - 1
num(P, it, 1, gam, np.polyfit(*(lambda u_: (u_[:-1], np.diff(u_)))(
    (lambda e: np.array(list(itertools.accumulate(e, lambda a_, b_: 0.96 * a_ + b_))))(rng.standard_normal(200000))), 1)[0],
    {'phi': 0.96, 'sign': 0.04}, agree=0.003)
nn = sp.symbols('n', positive=True)
t_exp = lambda g_, p_, n_: g_ / sp.sqrt((1 - p_ ** 2) / n_)
# method 2: the same standard error from the AR(1)'s information, sigma_eta / sqrt(n Var(u)) with sigma_eta = 1
se_info = 1 / math.sqrt(250 * (1 / (1 - 0.96 ** 2)))


def eg_reject_share(phi_, n_, sims=400):
    """Share of simulated tied pairs (y = x + u, u an AR(1)) whose Engle-Granger t_gamma is below -3.34."""
    e = rng.standard_normal((sims, n_ + 1))
    u_ = np.zeros((sims, n_ + 1))
    u_[:, 0] = e[:, 0] / math.sqrt(1 - phi_ ** 2)
    for t in range(1, n_ + 1):
        u_[:, t] = phi_ * u_[:, t - 1] + e[:, t]
    x_ = np.cumsum(rng.standard_normal((sims, n_ + 1)), axis=1)
    y_ = x_ + u_
    hits = 0
    for i in range(sims):
        X = np.c_[np.ones(n_ + 1), x_[i]]
        res = y_[i] - X @ np.linalg.lstsq(X, y_[i], rcond=None)[0]
        a_, d_ = res[:-1], np.diff(res)
        g_ = (a_ @ d_) / (a_ @ a_)
        s_ = math.sqrt(((d_ - g_ * a_) ** 2).sum() / (n_ - 1))
        hits += g_ / (s_ / math.sqrt(a_ @ a_)) < -3.34
    return hits / sims


ok(eg_reject_share(0.96, 250) < 0.5 and eg_reject_share(0.98, 250) < 0.5, 'p3 one year usually misses both ties')
ok(eg_reject_share(0.96, 547) > 0.5 and eg_reject_share(0.98, 1105) > 0.5, 'p3 the guide is cautious: the real test usually rejects at its days')
num(P, it, 2, t_exp(gam, ph, 250), -0.04 / se_info, {'one-minus-phi': -0.04 / math.sqrt(0.04 / 250), 'no-root': -0.04 / (0.0784 / 250), 'sign': 2.26}, agree=1e-9)
said(P, it, 2, '0.0177'); said(P, it, 2, '0.0784')
ok(r(-0.04 / 0.0177, 2) == -2.26, 'p3 printed -0.04/0.0177 = -2.26')
n_exact = sp.solve(sp.Eq(-t_exp(gam, ph, nn), sp.Rational(334, 100)), nn)[0]
n_loop = next(k for k in itertools.count(1) if 0.04 * math.sqrt(k / 0.0784) >= 3.34)
num(P, it, 3, sp.ceiling(n_exact), n_loop, {'linear': math.ceil(250 * 3.34 / (0.04 / math.sqrt(0.0784 / 250))), 'adf': math.ceil((2.86 * 0.28 / 0.04) ** 2), 'round-down': n_loop - 1})
ok(abs(float(n_exact) - 546.6244) < 1e-6, 'p3 n = 546.62'); said(P, it, 3, '546.6'); said(P, it, 3, '23.38'); said(P, it, 3, '0.1429')
ok(f'{0.04 / 0.28 * math.sqrt(546):.3f}' == '3.338', 'p3 day 546 statistic -3.338')
ph2 = sp.Rational(98, 100)
n2 = sp.solve(sp.Eq(-t_exp(ph2 - 1, ph2, nn), sp.Rational(334, 100)), nn)[0]
n2_loop = next(k for k in itertools.count(1) if 0.02 * math.sqrt(k / (1 - 0.98 ** 2)) >= 3.34)
num(P, it, 4, sp.ceiling(n2), n2_loop, {'doubled': 2 * n_loop, 'phi-unchanged': math.ceil((3.34 * 0.28 / 0.02) ** 2), 'one-minus-phi': math.ceil((3.34 * math.sqrt(0.02) / 0.02) ** 2)})
said(P, it, 4, '0.1990'); said(P, it, 4, '1,104.4'); said(P, it, 4, '0.1005')
ok(n2_loop / 252 > 4, 'p3 over four years')

# p-screen-real-share (re-authored for p-utility-step-two, review findings 4 and 5)
it = 'p-screen-real-share'
n_pairs, n_tied = 1200, 36
n_free = n_pairs - n_tied
ok(n_free == 1164 and F(n_tied, n_pairs) == F(3, 100), 'p4 36 tied pairs are 3% of 1,200; 1,164 untied')
pw2, pw4, pw4_1 = F(40, 100), F(85, 100), F(65, 100)
# method 2: 20,000 simulated screens, pooled counts
S = 20000
tied2 = rng.binomial(n_tied, 0.40, S); free5 = rng.binomial(n_free, 0.05, S)
tied4 = rng.binomial(n_tied, 0.85, S); tied41 = rng.binomial(n_tied, 0.65, S); free1 = rng.binomial(n_free, 0.01, S)
num(P, it, 1, n_tied * pw2, tied2.mean(), {'no-power': 36, 'miss-rate': 36 * 0.6, 'all-pairs': 1200 * 0.4}, agree=0.05)
tot2 = n_tied * pw2 + n_free * F(5, 100)
num(P, it, 2, tot2, (tied2 + free5).mean(), {'all-untied': 1200 * 0.05 + 14.4, 'false-only': 1164 * 0.05, 'no-power': 36 + 58.2}, agree=0.1)
said(P, it, 2, '58.2')
share = lambda pw, lev: (F(3, 100) * pw) / (F(3, 100) * pw + F(97, 100) * lev)   # Bayes on one pair
s2 = n_tied * pw2 / tot2
ok(s2 == share(pw2, F(5, 100)), 'p4 count route and Bayes route agree, two years')
num(P, it, 3, s2, tied2.sum() / (tied2 + free5).sum(), {'all-untied': 14.4 / 74.4, 'power': 0.40, 'false-share': 58.2 / 72.6, 'over-false': 14.4 / 58.2}, agree=0.003)
ok(abs(1164 / 36 - 32) < 0.5, 'p4 untied outnumber tied about 32 to 1')
s4 = n_tied * pw4 / (n_tied * pw4 + n_free * F(5, 100))
ok(s4 == share(pw4, F(5, 100)), 'p4 Bayes route, four years')
num(P, it, 4, s4, tied4.sum() / (tied4 + free5).sum(), {'power': 0.85, 'all-untied': 30.6 / 90.6, 'old-total': 30.6 / 72.6, 'false-share': 58.2 / 88.8}, agree=0.003)
ok(30.6 / 14.4 > 2, 'p4 more than doubles')
s41 = n_tied * pw4_1 / (n_tied * pw4_1 + n_free * F(1, 100))
ok(s41 == share(pw4_1, F(1, 100)), 'p4 Bayes route, 1% level')
num(P, it, 5, s41, tied41.sum() / (tied41 + free1).sum(), {'old-power': 30.6 / (30.6 + 11.64), 'five-percent': 23.4 / (23.4 + 58.2), 'false-share': 11.64 / 35.04}, agree=0.004)
ok(r(30.6 - 23.4, 2) == 7.2 and r(58.2 - 11.64, 2) == 46.56, 'p4 gives up 7.2, removes 46.56')
for k, tok in ((3, '19.8'), (4, '34.5'), (5, '66.8'), (5, '35.04'), (4, '88.8')):
    said(P, it, k, tok)
for k in (3, 4, 5):
    ok(part(P, it, k)['widget'].get('unit') == '%', f'p4 part {k} unit %')

# ------------------------------------------------------------------ level 2
Q = load(2)

# p-smelter-tls (re-authored for p-cement-three-ratios, review finding 6)
it = 'p-smelter-tls'
sxx, syy, sxy = F(625, 100), F(4), F(46, 10)
Cm = np.array([[6.25, 4.6], [4.6, 4.0]])
ok(abs(float(sxy) / math.sqrt(float(sxx * syy)) - 0.92) < 1e-12, 'q1 correlation 0.92, not the exam e-hedge-flip 0.85')
# method 2: 200 days built with exactly these sample moments (ddof 1)
n = 200
Z = rng.standard_normal((n, 2)); Z = Z - Z.mean(axis=0)
Lz = np.linalg.cholesky(np.cov(Z.T)); Z = Z @ np.linalg.inv(Lz).T
XY = Z @ np.linalg.cholesky(Cm).T + np.array([30.0, 22.0])
x_, y_ = XY[:, 0], XY[:, 1]
ok(np.allclose(np.cov(XY.T), Cm) and np.allclose(XY.mean(axis=0), [30, 22]), 'q1 built data have the stated moments')
lam = sp.symbols('lam')
lmax = max(sp.solve(lam ** 2 - (sxx + syy) * lam + (sxx * syy - sxy ** 2), lam), key=lambda z: float(z))
wv, vv = np.linalg.eigh(np.cov(XY.T))
lmin_ = min(wv)
num(Q, it, 1, lmax, max(wv), {'smaller': lmin_, 'trace': 10.25, 'no-square': 5.125 + math.sqrt(2.25 ** 2 / 4 + 4.6)}, agree=1e-9)
ok(sxx * syy - sxy ** 2 == F(384, 100) and (sxx + syy) ** 2 - 4 * (sxx * syy - sxy ** 2) == F(897025, 10000), 'q1 det 3.84, discriminant 89.7025')
ok(f'{float(lmin_):.2f}' == '0.39', 'q1 smaller eigenvalue 0.39')
vmax = vv[:, np.argmax(wv)]
tls_r = (F(986, 100) - sxx) / sxy                      # from the rounded 9.86 the part gives
ok(abs(float((lmax - sxx) / sxy) - 0.7849) < 0.0001 and r(float(tls_r), 3) == 0.785, 'q1 exact and rounded eigenvalues both give 0.785')
num(Q, it, 2, tls_r, vmax[1] / vmax[0], {'ols': 4.6 / 6.25, 'other-ratio': (9.86 - 4.0) / 4.6, 'smaller': (lmin_ - 6.25) / 4.6}, agree=2e-4)
ok(r(1 / 0.785, 3) == 1.274, 'q1 other way up is 1/0.785')
said(Q, it, 2, '3.61'); said(Q, it, 2, '0.736')
b = 0.785
v_sp = 4.0 - 2 * b * 4.6 + b ** 2 * 6.25
num(Q, it, 3, math.sqrt(v_sp), np.std(y_ - b * x_, ddof=1), {'variance': v_sp, 'no-cross': math.sqrt(4 + b ** 2 * 6.25), 'plus-cross': math.sqrt(4 + 2 * b * 4.6 + b ** 2 * 6.25)}, agree=1e-9)
ok(r(2 * b * 4.6, 3) == 7.222 and r(b ** 2 * 6.25, 3) == 3.851 and r(v_sp, 3) == 0.629, 'q1 printed 7.222, 3.851, 0.629')
v_ols = 4.0 - 4.6 ** 2 / 6.25
ok(r(math.sqrt(v_ols), 3) == 0.784 and math.sqrt(v_sp) - math.sqrt(v_ols) < 0.01, 'q1 least squares sd 0.784, under a penny less')
ok(abs(np.std(y_ - 0.736 * x_, ddof=1) - math.sqrt(v_ols)) < 1e-9, 'q1 least squares sd from the data')
said(Q, it, 3, '0.784')
s_today = 24.50 - b * 31.00
s_mean = 22.00 - b * 30.00
ok(r(s_today, 3) == 0.165 and r(s_mean, 2) == -1.55 and r(s_today - s_mean, 3) == 1.715, 'q1 spread 0.165, mean -1.55, distance 1.715')
spr = y_ - b * x_
num(Q, it, 4, (s_today - s_mean) / 0.793, (s_today - spr.mean()) / np.std(spr, ddof=1), {'no-mean': 0.165 / 0.793, 'variance': 1.715 / 0.629, 'no-hedge': (24.50 - 22.00) / 0.793}, agree=0.002)
ok(abs(1.715 / 0.62940625 - 2.725) <= 0.005, 'q1 variance slip with the unrounded variance also lands in its band')
said(Q, it, 4, '1.715')

it = 'p-lessor-window'
a, b = 0.04, -0.08
num(Q, it, 1, hl(b), brentq(lambda h: 0.92 ** h - 0.5, 1, 50), {'one-over-b': 12.5, 'rough': math.log(2) / 0.08, 'b-as-phi': math.log(0.5) / math.log(0.08)})
win = math.ceil(5 * r(hl(b), 2))
num(Q, it, 2, win, next(k for k in itertools.count(1) if k >= 5 * 8.31), {'round-down': 41})
said(Q, it, 2, '41.6')
num(Q, it, 3, F(-80, 35), (-0.18 - 0.62) / 0.35, {'sign': 0.80 / 0.35, 'no-mean': -0.18 / 0.35, 'added-mean': (-0.18 + 0.62) / 0.35})
mu = -a / b
s = -0.18
for _ in range(5):
    s = a + (1 + b) * s                                # expected path, day by day
num(Q, it, 4, mu + (-0.18 - mu) * 0.92 ** 5, s, {'window-mean': 0.62 + (-0.80) * 0.92 ** 5, 'zero-mean': -0.18 * 0.92 ** 5}, agree=1e-9)
said(Q, it, 4, '0.448'); said(Q, it, 4, '0.659')

it = 'p-three-distributors'
trace, crit = [41.7, 9.8, 1.6], [29.80, 15.49, 3.84]
rank = next((i for i, (tr, cv) in enumerate(zip(trace, crit)) if tr < cv), 3)
num(Q, it, 1, rank, sum(itertools.takewhile(lambda z: z, (tr > cv for tr, cv in zip(trace, crit)))), {'trends': 2, 'series': 3, 'none': 0})
v = np.array([0.36, -0.54, 0.27])
vn = v / v[0]
num(Q, it, 2, F(27, 36), vn[2], {'raw': 0.27, 'inverted': 0.36 / 0.27, 'sign': -0.75}, agree=1e-12)
ok(abs(vn[1] + 1.5) < 1e-12, 'q3 Q weight -1.5')
px = np.array([12.40, 9.80, 6.20])
num(Q, it, 3, F(1240, 100) - F(3, 2) * F(980, 100) + F(3, 4) * F(620, 100), px @ vn, {'r-sign': 12.40 - 14.70 - 4.65, 'no-weights': 12.40 - 9.80 + 6.20, 'q-sign': 12.40 + 14.70 + 4.65}, agree=1e-9)
num(Q, it, 4, F(30, 20), (px @ vn - 2.05) / 0.20, {'no-mean': 2.35 / 0.20, 'variance': 0.30 / 0.04}, agree=1e-9)
# rank 1 and a vector with every weight non-zero: no combination with one zero weight lies in the span
ok(all(abs(c) > 0 for c in vn), 'q3 every weight non-zero')
cho(Q, it, 5, 'no-pair')
# statsmodels' 95% trace values for three series and det_order 0
from statsmodels.tsa.coint_tables import c_sjt
ok(all(abs(c_sjt(k, 0)[1] - cv) < 0.01 for k, cv in zip([3, 2, 1], crit)), 'q3 critical values 29.80, 15.49, 3.84')

it = 'p-tyre-vecm'
gap = 1.5
dy, dx_ = -0.06 * gap, 0.02 * gap
num(Q, it, 1, F(-6, 100) * F(3, 2), dy, {'sign': 0.09, 'x-speed': 0.03})
dg = dy - 1.5 * dx_
# method 2: one step of the VECM on prices, then the gap
y0, x0 = 30.0, (30.0 - gap) / 1.5
y1, x1 = y0 - 0.06 * gap, x0 + 0.02 * gap
num(Q, it, 2, F(-6, 100) * F(3, 2) - F(3, 2) * F(2, 100) * F(3, 2), (y1 - 1.5 * x1) - gap, {'no-ratio': dy - dx_, 'x-sign': dy + 1.5 * dx_, 'y-only': dy, 'sign': -dg}, agree=1e-9)
bg = dg / gap
gpath = [gap]
while gpath[-1] > gap / 2:
    gpath.append(gpath[-1] * (1 + bg))
k = len(gpath) - 1
h_interp = (k - 1) + math.log(0.5 * gap / gpath[k - 1]) / math.log(1 + bg)
num(Q, it, 3, hl(-0.09), h_interp, {'y-only': hl(-0.06), 'rough': math.log(2) / 0.09, 'one-over-b': 1 / 0.09}, agree=1e-9)
said(Q, it, 3, '0.09')
cho(Q, it, 4, 'slower')
ok(r(hl(-0.06), 2) == 11.20, 'q4 alpha_x = 0 half-life 11.20')

# ------------------------------------------------------------------ level 3
R = load(3)

# p-glassmaker-borrow (re-authored for p-packaging-stop-reopen, review finding 12)
it = 'p-glassmaker-borrow'
h, py, px_, unit_z = F(115, 100), F(48), F(36), F(1, 2)
fee_y, fee_x, days, year = F(5, 1000), F(6, 100), 21, 252
borrow_long = h * px_
# method 2: the pounds in the sold leg of a long, share by share
num(R, it, 1, borrow_long, sum([36.0] * 115) / 100, {'y-leg': 48, 'no-hedge': 36, 'hedge-on-y': 1.15 * 48}, agree=1e-9)
fee_long = borrow_long * fee_x * days / year
acc = 0.0
for _ in range(days):                                  # method 2: accrue the fee day by day
    acc += 41.40 * 0.06 / 252
num(R, it, 2, fee_long, acc, {'calendar-days': 41.40 * 0.06 * 21 / 365, 'one-day': 41.40 * 0.06 / 252, 'annual': 41.40 * 0.06, 'y-rate': 41.40 * 0.005 * 21 / 252}, agree=1e-9)
ok(F(days, year) == F(1, 12) and fee_long == F(207, 1000), 'r1 21/252 = 1/12, long fee 0.207')
fee_short = py * fee_y * days / year
ok(fee_short == F(2, 100), 'r1 short fee 0.020')
acc_s = sum(48.0 * 0.005 / 252 for _ in range(days))
num(R, it, 3, fee_long - fee_short, acc - acc_s, {'short-only': 0.02, 'sum': 0.227, 'x-rate-both': 0.207 - 48 * 0.06 / 12}, agree=1e-9)
cho(R, it, 4, 'flatters-long')
ok(fee_long / fee_short > 10, 'r1 the long fee is over ten times the short fee')
net_short = 2 * unit_z - fee_short
ok(net_short == F(98, 100), 'r1 short nets 0.98')
entry = -(net_short + fee_long) / unit_z               # long nets |e| * unit - fee_long
num(R, it, 5, entry, -brentq(lambda e: e * 0.5 - 0.207 - 0.98, 0, 10), {'sign': 2.374, 'shift-only': -0.374, 'pounds': -2.187, 'wrong-way': -1.626}, agree=1e-9)
ok(entry == -2 - (fee_long - fee_short) / unit_z, 'r1 entry from the fee gap: -2 - 0.187/0.50')
ok(r(float(-entry * unit_z), 3) == 1.187, 'r1 long earns 1.187 from -2.374')
said(R, it, 5, '0.374'); said(R, it, 5, '1.187')

it = 'p-stop-edge'
unit, cost, STOP = F(6, 10), F(1, 10), F(34, 10)
up = STOP - 2
win_, loss_ = 2 * unit - cost, -(up * unit + cost)
num(R, it, 1, win_, 2 * 0.6 - 0.1, {'no-cost': 1.2, 'cost-added': 1.3, 'z-units': 2 - 0.1})
num(R, it, 2, loss_, -(1.4 * 0.6) - 0.1, {'no-cost': -0.84, 'stop-four': -(2 * 0.6 + 0.1), 'sign': 0.94, 'cost-wrong-way': -0.74})
pbe = -loss_ / (win_ - loss_)
num(R, it, 3, pbe, brentq(lambda q: q * 1.1 - (1 - q) * 0.94, 0, 1), {'swapped': 1.1 / 2.04, 'no-cost': 0.84 / 2.04, 'even': 0.5})
p_exit = up / STOP
# method 2: a simple random walk on a grid of 0.05 between 0 and 3.4, started at 2: exact hitting probability by linear solve
h = 0.05
M = int(round(3.4 / h))
A = np.zeros((M + 1, M + 1)); rhs = np.zeros(M + 1)
A[0, 0] = 1; rhs[0] = 1                               # at the exit: reached it first
A[M, M] = 1                                           # at the stop: did not
for i in range(1, M):
    A[i, i] = 1; A[i, i - 1] = -0.5; A[i, i + 1] = -0.5
hit = np.linalg.solve(A, rhs)[int(round(2 / h))]
num(R, it, 4, p_exit, hit, {'swapped': 2 / 3.4, 'even': 0.5}, agree=1e-9)
ev = p_exit * win_ + (1 - p_exit) * loss_
paths = rng.choice([-0.05, 0.05], size=(4000, 4000))
zs = 2 + np.cumsum(paths, axis=1)
first_exit = np.argmax(zs <= 1e-9, axis=1); first_stop = np.argmax(zs >= 3.4 - 1e-9, axis=1)
done = (zs <= 1e-9).any(axis=1) | (zs >= 3.4 - 1e-9).any(axis=1)
fe = np.where((zs <= 1e-9).any(axis=1), first_exit, 10 ** 9)
fs = np.where((zs >= 3.4 - 1e-9).any(axis=1), first_stop, 10 ** 9)
mc_ev = np.where(fe < fs, 1.1, -0.94)[done].mean()
num(R, it, 5, ev, 0.412 * 1.10 - 0.588 * 0.94, {'no-cost': p_exit * 2 * unit - (1 - p_exit) * up * unit, 'sign': -ev, 'even': 0.5 * 1.1 - 0.5 * 0.94}, agree=0.002)
ok(abs(mc_ev - float(ev)) < 0.05, f'r2 simulated expected P&L {mc_ev}')
ok(p_exit * 2 * unit - (1 - p_exit) * up * unit == 0, 'r2 fair before costs')
ok(abs(0.412 * 1.20 - 0.588 * 0.84) < 0.001, 'r2 printed fair bet with rounded chances is 0 to 3 places')

it = 'p-half-life-alarms'
pH = F(14, 100)
pA = 1 - (1 - pH) ** 4
encA = sum(np.prod([0.14 if c else 0.86 for c in seq]) for seq in itertools.product([0, 1], repeat=4) if any(seq))
num(R, it, 1, pA, encA, {'added': 4 * 0.14, 'escape': 0.86 ** 4, 'all-four': 0.14 ** 4}, agree=1e-12)
said(R, it, 1, '0.5470')
pB = pH ** 2 * (1 + 2 * (1 - pH))
encB = sum(np.prod([0.14 if c else 0.86 for c in seq]) for seq in itertools.product([0, 1], repeat=4)
           if any(seq[i] and seq[i + 1] for i in range(3)))
num(R, it, 2, pB, encB, {'three-pairs': 3 * 0.0196, 'one-pair': 0.0196, 'overlap': 1 - (1 - 0.0196) ** 3}, agree=1e-12)
said(R, it, 2, '2.72')
simA = (rng.random((400000, 4)) < 0.14)
simB = (simA[:, :-1] & simA[:, 1:]).any(axis=1).mean()
ok(abs(simB - float(pB)) < 0.002 and abs(simA.any(axis=1).mean() - float(pA)) < 0.003, 'r3 simulated chances')
gap = 40 * (pA - pB)
num(R, it, 3, gap, 40 * encA - 40 * encB, {'a-only': 40 * pA, 'all-43': 43 * (pA - pB), 'b-only': 40 * pB}, agree=1e-9)
ok(r(40 * 0.4530, 2) == 18.12 and r(40 * 0.0533, 2) == 2.13 and r(18.12 - 2.13, 2) == 15.99, 'r3 printed 18.12, 2.13, 15.99')
save = gap * F(175, 100)
num(R, it, 4, save - 3 * 5, 15.99 * 1.75 - 15, {'no-delay': save, 'one-broken': save - 5, 'sign': -(save - 15)}, agree=0.01)
said(R, it, 4, '27.98'); ok(r(15.99 * 1.75, 2) == 27.98, 'r3 15.99 x 1.75 = 27.98')
num(R, it, 5, save / 3, brentq(lambda c: 3 * c - 27.98, 0, 50), {'no-split': 27.98, 'margin': 12.98 / 3}, agree=0.005)
ok(r(5 + 12.98 / 3, 2) == 9.33, 'r3 5.00 + 4.33 = 9.33')

it = 'p-housebuilder-trading-years'
mean = F(1890, 100) / 504
num(R, it, 1, mean, 18.90 / 504, {'all-days': 18.90 / (4 * 252 + 504), 'per-252': 18.90 / 252})
sh = float(mean) / 0.55 * math.sqrt(252)
pnl_days = rng.standard_normal(504)
pnl_days = (pnl_days - pnl_days.mean()) / pnl_days.std() * 0.55 + 0.0375
num(R, it, 2, sh, pnl_days.mean() / pnl_days.std() * math.sqrt(252), {'daily': 0.0375 / 0.55, 'times-252': 0.0375 / 0.55 * 252, 'variance': 0.0375 / 0.3025 * math.sqrt(252)}, agree=1e-9)
said(R, it, 2, '0.0682'); said(R, it, 2, '15.87')
num(R, it, 3, 1.08 * math.sqrt(504 / 252), 1.08 / (1 / math.sqrt(2)), {'times-t': 2.16, 'divided': 1.08 / math.sqrt(2), 'all-years': 1.08 * math.sqrt(6)})
ok(r(sh * math.sqrt(2), 2) == 1.53, 'r4 unrounded Sharpe gives 1.53 too'); said(R, it, 3, '0.707')
Tn = (F(2) / F(108, 100)) ** 2
num(R, it, 4, Tn, brentq(lambda T: 1.08 * math.sqrt(T) - 2, 0.1, 50), {'no-square': 2 / 1.08, 'inverted': (1.08 / 2) ** 2, 'four-over': 4 / 1.08}, agree=1e-9)
said(R, it, 4, '1.852')
more = math.ceil(3.43 * 252 - 504)
num(R, it, 5, more, next(k for k in itertools.count(1) if 504 + k >= 3.43 * 252), {'total': math.ceil(3.43 * 252), 'round-down': more - 1})
ok(math.ceil(float(Tn) * 252 - 504) == 361, 'r4 unrounded T also gives 361 days')
said(R, it, 5, '864.4'); said(R, it, 5, '360.4')
tol4 = part(R, it, 4)['widget']['tol']['abs']
ok(abs(1.85 ** 2 - 3.43) <= tol4, 'r4 the band takes 1.85 squared, 3.4225 (review finding 16)')

# ------------------------------------------------------------------ fix-pass lines (review findings 7, 9, 14)
ok(r(0.92 ** 8, 3) == 0.513 and r(0.92 ** 9, 3) == 0.472, 'q2 0.92^8 = 0.513, 0.92^9 = 0.472')
said(Q, 'p-lessor-window', 1, '0.513'); said(Q, 'p-lessor-window', 1, '0.472')
ok(r(41.7 - 29.80, 2) == 11.9 and r(15.49 - 9.8, 2) == 5.69, 'q3 margins 11.9 and 5.69')
said(Q, 'p-three-distributors', 1, '11.9'); said(Q, 'p-three-distributors', 1, '5.69')
ok(r(1.08 * 0.707, 2) == 0.76 and r(1.08 * math.sqrt(6), 2) == 2.65, 'r4 lines 0.76 and 2.65')
said(R, 'p-housebuilder-trading-years', 3, '2.65')

# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
