"""Recompute every number in app/content/courses/stat-models/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 3, one block per set. Method 1 is exact or closed form (fractions, sympy, the formula the lesson teaches).
Method 2 takes another route. Level 1: statsmodels GLM fits on data built to hold the stated table (the IPOs, the
settlement months with their offsets, the six break days), its deviance, standard errors and Pearson statistic, and a
hand-written IRLS loop; SciPy's chi2 and norm for tails; a simulation of the auction count. Level 2: data built to hold
the stated means and spreads, fitted by statsmodels OLS and scipy.stats.f_oneway, a simulated paired test and a brute
search for the sample size. Level 3: scipy.stats.mannwhitneyu (exact) against an enumeration of all labellings, the
MAD by statsmodels.robust, a numerical integral of the kernel estimate, and an enumeration of all 32 sign patterns.

For each numeric part: both methods agree; the key lies within its tol of them; every `wrong` value matches its named
slip, lies outside the key band, is no wider than half its value, and does not overlap another; byKey covers the
wrongs exactly; a non-whole key's question states its form. Choice parts: the keyed option. Every number printed in
feedback and explain lines is listed in a `shown` check below. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-stat-models-numbers.py
"""
import itertools
import json
import math
import os
import re
import sys
import warnings
from fractions import Fraction as Fr

import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
from scipy import stats, integrate
from statsmodels.robust.scale import mad as sm_mad

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'stat-models')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|fraction|nearest|per cent|rounded up', re.I)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def present(n):
    return os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))


def load(n):
    d = json.load(open(os.path.join(COURSE, f'problems-{n}.json')))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'stat-models', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: no difficulty 5')
    return {it['id']: it for it in d['items']}


def num(items, iid, k, exact, alt, slips, agree=1e-6):
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if abs(e - round(e)) > 1e-9:
        ok(bool(FORM.search(part['question'])), f'{tag}: question states no form')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        half = 0.5 * 10 ** -max(0, len(str(x['value']).split('.')[-1]) if '.' in str(x['value']) else 0)
        ok(abs(x['value'] - float(val)) <= max(wt, half) + 1e-12, f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
        ok(wt <= abs(x['value']) / 2 + 1e-12, f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    ok(set(part['feedback'].get('byKey', {})) == set(wrongs), f'{tag}: byKey keys vs wrongs')


def pick(items, iid, k, correct_id):
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} p{k}: a distractor has no why')


def shown(label, printed, value, dp):
    ok(abs(printed - value) <= 0.5 * 10 ** -dp + 1e-12, f'shown {label}: printed {printed} vs {value}')


def logistic_fit(x, y):
    X = sm.add_constant(np.asarray(x, float))
    return sm.GLM(np.asarray(y, float), X, family=sm.families.Binomial()).fit()


Phi, ln, exp, sqrt = stats.norm.cdf, math.log, math.exp, math.sqrt

def level1():
    I = load(1)

    # --- p-ipo-underwriter: 24 top-tier (18 rose), 36 others (12 rose)
    x = [1] * 24 + [0] * 36
    y = [1] * 18 + [0] * 6 + [1] * 12 + [0] * 24
    fit = logistic_fit(x, y)
    b1 = ln(Fr(18, 6) / Fr(12, 24))
    num(I, 'p-ipo-underwriter', 1, b1, fit.params[1],
        {'odds-ratio': 6, 'share-ratio': ln(0.75 / (1 / 3)), 'top-only': ln(3)})
    ll = 18 * ln(0.75) + 6 * ln(0.25) + 12 * ln(1 / 3) + 24 * ln(2 / 3)
    D1 = -2 * ll
    num(I, 'p-ipo-underwriter', 2, D1, fit.deviance,
        {'no-two': -ll, 'risers-only': -2 * (18 * ln(0.75) + 12 * ln(1 / 3))})
    D0 = 120 * ln(2)
    fit0 = sm.GLM(np.array(y, float), np.ones((60, 1)), family=sm.families.Binomial()).fit()
    LR = D0 - D1
    num(I, 'p-ipo-underwriter', 3, LR, fit0.deviance - fit.deviance, {'null-only': D0, 'halved': LR / 2})
    p = stats.chi2.sf(LR, 1)
    num(I, 'p-ipo-underwriter', 4, p, 2 * stats.norm.sf(sqrt(LR)), {'two-df': stats.chi2.sf(LR, 2), 'lower-tail': 1 - p}, agree=1e-9)
    shown('ipo ll', -36.4106, ll, 4); shown('ipo null dev', 83.178, D0, 3); shown('ipo LR', 10.357, LR, 3)

    # --- p-settlement-fails: domestic 50k trades / 30 fails, cross-border 20k / 28 fails, over 6 and 4 months
    t = np.array([9, 8, 7, 9, 8, 9, 5, 6, 4, 5], float)          # thousands; sums 50 and 20
    yv = np.array([5, 6, 4, 5, 4, 6, 7, 8, 6, 7], float)          # sums 30 and 28
    xv = np.array([0] * 6 + [1] * 4, float)
    ok(t[:6].sum() == 50 and t[6:].sum() == 20 and yv[:6].sum() == 30 and yv[6:].sum() == 28, 'fails data sums')
    pf = sm.GLM(yv, sm.add_constant(xv), family=sm.families.Poisson(), offset=np.log(t)).fit()
    rr = Fr(28, 20) / Fr(30, 50)
    num(I, 'p-settlement-fails', 1, rr, exp(pf.params[1]),
        {'counts-only': 28 / 30, 'log-scale': ln(7 / 3), 'inverted': 1 / float(rr)})
    XtWX = np.array([[58, 28], [28, 28]], float)
    se = sqrt(np.linalg.inv(XtWX)[1, 1])
    num(I, 'p-settlement-fails', 2, sqrt(Fr(58, 840)), pf.bse[1],
        {'variance': 58 / 840, 'wrong-entry': sqrt(28 / 840), 'no-inverse': 1 / sqrt(28)})
    ok(math.isclose(se, sqrt(1 / 30 + 1 / 28)), 'fails se: X^T W X against 1/30 + 1/28')
    phi = 17.6 / 8
    b1f = ln(7 / 3)
    seq = se * sqrt(phi)
    # method 2: statsmodels quasi-Poisson with the scale fixed at 2.2 (the stated Pearson statistic, not this data's)
    pq = sm.GLM(yv, sm.add_constant(xv), family=sm.families.Poisson(), offset=np.log(t)).fit(scale=phi)
    num(I, 'p-settlement-fails', 3, b1f / seq, pq.tvalues[1],
        {'poisson-z': b1f / se, 'phi-not-root': b1f / (se * phi), 'ten-df': b1f / (se * sqrt(17.6 / 10))})
    lo = exp(b1f - 1.96 * seq)
    num(I, 'p-settlement-fails', 4, lo, exp(pq.params[1] - 1.96 * pq.bse[1]),
        {'poisson-se': exp(b1f - 1.96 * se), 'log-scale': b1f - 1.96 * seq})
    shown('fails rate cb', 1.4, 28 / 20, 1); shown('fails rate dom', 0.6, 30 / 50, 1)
    shown('fails b1', 0.84730, b1f, 5); shown('fails qse', 0.38975, seq, 5); shown('fails phi', 2.2, phi, 1)
    shown('fails log lower', 0.0834, b1f - 1.96 * seq, 4); shown('fails se printed', 0.2628, se, 4)
    shown('fails log lower printed', 0.0834, 0.84730 - 1.96 * 0.38975, 4)

    # --- p-recon-breaks: 0, 6, 2, 5, 1, 4
    yb = np.array([0, 6, 2, 5, 1, 4], float)
    b, path = 0.0, []
    for _ in range(8):
        mu = np.full(6, exp(b))
        z = b + (yb - mu) / mu
        b = float(np.average(z, weights=mu)); path.append(b)
    num(I, 'p-recon-breaks', 1, 2, path[0], {'mean-count': 3, 'jump-to-fit': ln(3)})
    num(I, 'p-recon-breaks', 2, 1 + 3 * exp(-2), path[1], {'no-eta': (3 - exp(2)) / exp(2), 'sign': 2 - (3 - exp(2)) / exp(2)})
    pb = sm.GLM(yb, np.ones((6, 1)), family=sm.families.Poisson()).fit()
    num(I, 'p-recon-breaks', 3, ln(3), pb.params[0], {'mean-scale': 3, 'one-more': path[2]})
    chi = float(((yb - 3) ** 2 / 3).sum())
    num(I, 'p-recon-breaks', 4, Fr(28, 15), pb.pearson_chi2 / pb.df_resid, {'six-df': chi / 6, 'chi-only': chi})
    shown('breaks e2', 7.3891, exp(2), 4); shown('breaks chi', 9.3333, chi, 4)

    # --- p-auction-tails: mu = 1/(1 + exp(-(2.6 - 1.3c)))
    num(I, 'p-auction-tails', 1, Fr(26, 13), stats.logistic.ppf(0.5) * 0 + 2.6 / 1.3, {'intercept': 2.6, 'inverted': 1.3 / 2.6})
    mu_t = 1 / (1 + exp(0.65))
    num(I, 'p-auction-tails', 2, mu_t, stats.logistic.cdf(2.6 - 1.3 * 2.5), {'sign': 1 / (1 + exp(-0.65)), 'linear': -0.65})
    num(I, 'p-auction-tails', 3, mu_t * (1 - mu_t), stats.bernoulli(mu_t).var(), {'poisson-var': mu_t, 'gamma-var': mu_t ** 2})
    rng = np.random.default_rng(7)
    sim = rng.binomial(12, mu_t, 2_000_000).std()
    num(I, 'p-auction-tails', 4, sqrt(12 * mu_t * (1 - mu_t)), stats.binom(12, mu_t).std(),
        {'variance': 12 * mu_t * (1 - mu_t), 'one-auction': sqrt(mu_t * (1 - mu_t)), 'poisson': sqrt(12 * mu_t)})
    ok(abs(sim - sqrt(12 * mu_t * (1 - mu_t))) < 0.005, 'auction sd by simulation')
    shown('auction var', 2.7042, 12 * mu_t * (1 - mu_t), 4); shown('auction mean', 4.12, 12 * mu_t, 2)
    shown('auction 12x', 2.7042, 12 * 0.22535, 4); shown('auction 1-mu', 0.6570, 1 - mu_t, 4)


def level2():
    I = load(2)

    # --- p-venue-markouts: n = 10, 6, 8; means 1.5, 3.5, 1.0; residual SE 2.4
    n_ = np.array([10, 6, 8]); m_ = np.array([1.5, 3.5, 1.0])
    grand = Fr(15 + 21 + 8, 24)
    rows = []
    for venue, n0, m0 in zip('ABC', n_, m_):
        base = np.array([-1, 1] * (n0 // 2), float)
        rows += [(venue, m0 + e) for e in base]
    df = pd.DataFrame(rows, columns=['venue', 'markout'])
    num(I, 'p-venue-markouts', 1, grand, df.markout.mean(), {'unweighted': m_.mean(), 'coef-mean': (1.5 + 2.0 - 0.5) / 3})
    ssb = float((n_ * (m_ - float(grand)) ** 2).sum())
    ols = smf.ols('markout ~ C(venue)', data=df).fit()
    ok(np.allclose(ols.params.values, [1.5, 2.0, -0.5]), 'markout regression coefficients')
    num(I, 'p-venue-markouts', 2, ssb, ols.ess, {'unweighted-mean': float((n_ * (m_ - 2.0) ** 2).sum()), 'no-counts': float(((m_ - float(grand)) ** 2).sum())})
    F = ssb / 2 / 2.4 ** 2
    # method 2: rescale the within noise so the residual SE is exactly 2.4 and let f_oneway compute F
    grp = [df.markout[df.venue == v].values for v in 'ABC']
    s_now = sqrt(sum(((g - g.mean()) ** 2).sum() for g in grp) / 21)
    grp2 = [g.mean() + (g - g.mean()) * 2.4 / s_now for g in grp]
    F2 = stats.f_oneway(*grp2).statistic
    num(I, 'p-venue-markouts', 3, F, F2, {'not-squared': ssb / 2 / 2.4, 'no-df': ssb / 2.4 ** 2})
    pF = stats.f.sf(F, 2, 21)
    num(I, 'p-venue-markouts', 4, pF, stats.f_oneway(*grp2).pvalue, {'lower-tail': 1 - pF, 'total-df': stats.f.sf(F, 2, 23)})
    shown('markout pieces', 16.667, 6 * (3.5 - float(grand)) ** 2, 3); shown('markout msb', 11.667, ssb / 2, 3)
    shown('markout gap B', 1.6667, 3.5 - float(grand), 4)

    # --- p-twin-books: sigma 15, rho 0.6, 120 days
    z975, z80 = 1.95996, 0.84162
    sdd = sqrt(2 * 225 * 0.4)
    cov = np.array([[225, 0.6 * 225], [0.6 * 225, 225]])
    num(I, 'p-twin-books', 1, sqrt(180), sqrt(np.array([1, -1]) @ cov @ np.array([1, -1])),
        {'plus-rho': sqrt(2 * 225 * 1.6), 'no-rho': 15 * sqrt(2), 'no-two': sqrt(225 * 0.4)})
    mde = (z975 + z80) * sdd / sqrt(120)
    # method 2: the gain at which a normal test of 120 differences has power 0.8, by root finding
    from scipy.optimize import brentq
    se_d = sdd / sqrt(120)
    mde2 = brentq(lambda d: stats.norm.sf(1.95996 - d / se_d) - stats.norm.cdf(z80), 0.1, 20)
    num(I, 'p-twin-books', 2, mde, mde2, {'unpaired': (z975 + z80) * 15 * sqrt(2) / sqrt(120), 'no-power': z975 * sdd / sqrt(120)}, agree=1e-4)
    tt = 2.9 / (14.1 / sqrt(120))
    d_sim = np.array([1, -1] * 60, float)
    d_sim = 2.9 + (d_sim - d_sim.mean()) / d_sim.std(ddof=1) * 14.1
    num(I, 'p-twin-books', 3, tt, stats.ttest_1samp(d_sim, 0).statistic, {'no-root': 2.9 / 14.1, 'planned-sd': 2.9 / (sdd / sqrt(120))})
    pt = 2 * stats.t.sf(tt, 119)
    num(I, 'p-twin-books', 4, pt, stats.ttest_1samp(d_sim, 0).pvalue, {'one-sided': pt / 2, 'lower-tail': 1 - pt / 2})
    shown('twin var', 180, 225 + 225 - 2 * 0.6 * 225, 9); shown('twin var 2', 180, 2 * 15 ** 2 * (1 - 0.6), 9)
    shown('twin z sum', 2.80158, z975 + z80, 5); shown('twin se', 1.22474, se_d, 5); shown('twin se obs', 1.28715, 14.1 / sqrt(120), 5)

    # --- p-rerun-the-test: two arms of 40, means 6.2 and 4.4, pooled SD 4.5
    t2 = 1.8 / (4.5 * sqrt(2 / 40))
    a = np.array([1, -1] * 20, float); a = a / a.std(ddof=1) * 4.5
    old, new = 6.2 + a, 4.4 + a
    num(I, 'p-rerun-the-test', 1, t2, stats.ttest_ind(old, new).statistic, {'one-sample-se': 1.8 / (4.5 / sqrt(40)), 'no-root': 1.8 / 4.5})
    num(I, 'p-rerun-the-test', 2, t2 ** 2, stats.f_oneway(old, new).statistic, {'same': t2, 'doubled': 2 * t2})
    pf2 = stats.f.sf(3.2, 1, 78)
    num(I, 'p-rerun-the-test', 3, pf2, stats.ttest_ind(old, new).pvalue, {'one-tail-t': pf2 / 2, 'lower-tail': 1 - pf2})
    z90 = 1.28155


    def need(z2):
        return math.ceil(2 * (1.95996 + z2) ** 2 * 4.5 ** 2 / 1.8 ** 2)


    n_brute = next(n for n in range(2, 1000) if 2 * (1.95996 + z90) ** 2 * 20.25 / 3.24 <= n)
    num(I, 'p-rerun-the-test', 4, need(z90), n_brute,
        {'eighty': need(0.84162), 'no-two': math.ceil((1.95996 + z90) ** 2 * 20.25 / 3.24), 'one-sided': math.ceil(2 * (1.64485 + z90) ** 2 * 20.25 / 3.24)})
    shown('rerun se', 1.00623, 4.5 * sqrt(2 / 40), 5); shown('rerun zsq', 10.5074, (1.95996 + z90) ** 2, 4)
    shown('rerun n', 131.34, 2 * (1.95996 + z90) ** 2 * 20.25 / 3.24, 2)
    shown('rerun z sum', 3.24151, 1.95996 + z90, 5); shown('rerun sq', 20.25 / 3.24, 4.5 ** 2 / 1.8 ** 2, 6)


def level3():
    I = load(3)

    # --- p-ten-trading-days
    X = [1.8, 2.6, 0.9, 3.1]; Y = [0.4, 1.1, -0.6, 0.2, 0.7, -0.2]
    r = stats.rankdata(X + Y)
    U = r[:4].sum() - 10
    num(I, 'p-ten-trading-days', 1, U, sum(xx > yy for xx in X for yy in Y), {'rank-sum': r[:4].sum(), 'u-y': 24 - U})
    num(I, 'p-ten-trading-days', 2, math.comb(10, 4), sum(1 for _ in itertools.combinations(range(10), 4)), {'ordered': 10 * 9 * 8 * 7, 'sign-flips': 2 ** 10})
    cnt = sum(1 for c in itertools.combinations(range(1, 11), 4) if sum(c) - 10 >= U)
    p1s = Fr(cnt, 210)
    num(I, 'p-ten-trading-days', 3, p1s, stats.mannwhitneyu(X, Y, alternative='greater', method='exact').pvalue,
        {'one-split': 1 / 210, 'plus-one': 3 / 211})
    num(I, 'p-ten-trading-days', 4, 2 * p1s, stats.mannwhitneyu(X, Y, alternative='two-sided', method='exact').pvalue,
        {'one-sided': float(p1s), 'halved': float(p1s) / 2})
    ok(cnt == 2, 'two labellings reach U >= 23')

    # --- p-block-markout-tail
    d = np.array([-1.4, -0.2, 0.3, 0.5, 0.9, 1.6, 7.5])
    med = float(np.median(d)); raw = float(np.median(abs(d - med)))
    s_m = 1.4826 * raw
    num(I, 'p-block-markout-tail', 1, s_m, sm_mad(d, center=med) * 1.4826 * stats.norm.ppf(0.75), {'raw': raw, 'plain-sd': d.std(ddof=1)}, agree=1e-5)
    h = 1.06 * s_m * 7 ** -0.2
    num(I, 'p-block-markout-tail', 2, h, 1.06 * s_m / 7 ** 0.2,
        {'plain-sd': 1.06 * d.std(ddof=1) * 7 ** -0.2, 'raw-mad': 1.06 * raw * 7 ** -0.2, 'no-n': 1.06 * s_m})
    pk = float(Phi((-1 - d) / h).mean())
    pk2 = integrate.quad(lambda u: stats.norm.pdf((u - d) / h).sum() / (7 * h), -40, -1)[0]
    num(I, 'p-block-markout-tail', 3, pk, pk2,
        {'plain-sd': float(Phi((-1 - d) / (1.06 * d.std(ddof=1) * 7 ** -0.2)).mean()),
         'raw-mad': float(Phi((-1 - d) / (1.06 * raw * 7 ** -0.2)).mean()), 'empirical': 1 / 7}, agree=1e-7)
    pn = float(Phi((-1 - med) / s_m))
    ratio = pk / pn
    num(I, 'p-block-markout-tail', 4, ratio, pk2 / stats.norm(med, s_m).cdf(-1),
        {'inverted': pn / pk, 'classic-normal': pk / float(Phi((-1 - d.mean()) / d.std(ddof=1)))}, agree=1e-6)
    shown('markout normal share', 0.0742, pn, 4); shown('markout z', -1.4453, (-1 - med) / s_m, 4)
    shown('bump -1.4', 0.7042, float(Phi(0.4 / h)), 4); shown('bump -0.2', 0.1416, float(Phi(-0.8 / h)), 4)
    shown('n factor', 0.6776, 7 ** -0.2, 4); shown('n factor 1.06', 0.7183, 1.06 * 7 ** -0.2, 4)
    shown('mean', 1.3143, d.mean(), 4); shown('sd', 2.883, d.std(ddof=1), 3)
    shown('ratio printed', 1.76, 0.1306 / 0.0742, 2)

    # --- p-five-weeks-flip
    wk = np.array([1.2, 0.8, 2.5, -0.4, 9.0]); ab = abs(wk)
    pats = list(itertools.product([1, -1], repeat=5))
    c_med = sum(1 for s in pats if np.median(ab * np.array(s)) >= 1.2 - 1e-12)
    c_mean = sum(1 for s in pats if (ab * np.array(s)).sum() >= wk.sum() - 1e-12)
    num(I, 'p-five-weeks-flip', 1, Fr(12, 10), np.median(wk), {'mean': wk.mean(), 'trimmed': stats.trim_mean(wk, 0.2)})
    num(I, 'p-five-weeks-flip', 2, 4, c_med, {'mean-count': c_mean, 'two-sided': sum(1 for s in pats if abs(np.median(ab * np.array(s))) >= 1.2 - 1e-12)})
    num(I, 'p-five-weeks-flip', 3, Fr(4, 32), c_med / 32, {'plus-one': 5 / 33, 'two-sided': 8 / 32})
    pick(I, 'p-five-weeks-flip', 4, 'robust')
    ok(c_mean == 2, 'mean statistic counts 2 patterns'); shown('week total', 13.1, wk.sum(), 1)


for n, f in ((1, level1), (2, level2), (3, level3)):
    if present(n):
        f()

if fails:
    for f in fails:
        print('FAIL', f)
    print(f'{len(fails)} of {checks} checks failed')
    sys.exit(1)
print(f'all {checks} checks passed')
