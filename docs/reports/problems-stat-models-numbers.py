"""Recompute every number in app/content/courses/stat-models/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 3, one block per set. Method 1 is exact or closed form (fractions, sympy, the formula the lesson teaches).
Method 2 takes another route. Level 1: statsmodels GLM fits on data built to hold the stated table (the IPOs, the
settlement months with their offsets, the six break days), its deviance, standard errors and Pearson statistic, and a
hand-written IRLS loop; SciPy's chi2 and norm for tails; statsmodels' variance functions and simulated negative
binomial minutes for the RFQ counts. Level 2: data built to hold the stated means and spreads, fitted by statsmodels
OLS and scipy.stats.f_oneway, a simulated paired test, Bonferroni bars by root finding and pairwise tests, and all
1,024 win patterns plus a simulation for the two-look plan. Level 3: all 4,096 sign patterns of the ranks and scipy's
wilcoxon for the signed-rank test, the MAD by statsmodels.robust, a numerical integral of the kernel estimate, and
an enumeration of all 32 sign patterns. Fix pass (session AF): re-authored p-rfq-busy-minutes, p-signal-variants,
p-two-looks, p-hedge-ranks and p-spread-day-tail, and `shown` checks for every number in the review's replacements.

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

    # fix pass lines (review findings 2 to 5)
    shown('fails 2.2 x se', 0.5782, 0.2628 * 2.2, 4); shown('fails root 2.2', 1.4832, sqrt(2.2), 4)
    ok(Fr(1, 30) + Fr(1, 28) == Fr(58, 840), 'fails 1/30 + 1/28 = 58/840')
    t8 = stats.t.ppf(0.975, 8)
    shown('fails t8', 2.306, t8, 3); shown('fails t8 end', 0.950, exp(b1f - t8 * seq), 3)
    shown('fails t8 end printed', 0.950, exp(0.84730 - 2.306 * 0.38975), 3); shown('fails 1.087', 1.087, lo, 3)
    shown('breaks phi 1.87', 1.87, 28 / 15, 2)

    # --- p-rfq-busy-minutes: quiet mean 2.5, variance 4.0; busy mean 7.5
    mq, vq, mb = Fr(5, 2), Fr(4), Fr(15, 2)
    phi_q = vq / mq
    # method 2: simulate negative binomial counts with the matched alpha and fit both variance functions by moments
    alpha = (vq - mq) / mq ** 2
    rng = np.random.default_rng(11)
    def nb_draw(m, a, size):
        r_ = 1 / a
        return rng.negative_binomial(r_, r_ / (r_ + m), size)
    quiet = nb_draw(2.5, float(alpha), 4_000_000)
    phi_sim = quiet.var() / quiet.mean()
    # method 2: Pearson dispersion of an intercept-only Poisson GLM on minutes built with mean 2.5 and variance 4.0
    c_ = sqrt(4.0 * 9 / 10)
    yq = np.array([2.5 + c_, 2.5 - c_] * 5)
    gq = sm.GLM(yq, np.ones((10, 1)), family=sm.families.Poisson()).fit()
    num(I, 'p-rfq-busy-minutes', 1, phi_q, gq.pearson_chi2 / gq.df_resid,
        {'inverted': mq / vq, 'excess': vq - mq})
    ok(abs(phi_sim - 1.6) < 0.01, f'rfq phi by simulation {phi_sim}')
    num(I, 'p-rfq-busy-minutes', 2, phi_q * mb, sm.families.Poisson().variance(np.array([7.5]))[0] * float(phi_q),
        {'poisson': mb, 'mu-squared': phi_q * mb ** 2})
    # method 2 for alpha: statsmodels' NB2 variance function solved for alpha at the quiet mean
    from scipy.optimize import brentq
    a2 = brentq(lambda a: sm.families.NegativeBinomial(alpha=a).variance(np.array([2.5]))[0] - 4.0, 1e-6, 5)
    num(I, 'p-rfq-busy-minutes', 3, alpha, a2, {'no-poisson-part': vq / mq ** 2, 'mu-not-squared': (vq - mq) / mq})
    vb = mb + alpha * mb ** 2
    busy = nb_draw(7.5, float(alpha), 4_000_000)
    num(I, 'p-rfq-busy-minutes', 4, vb, sm.families.NegativeBinomial(alpha=float(alpha)).variance(np.array([7.5]))[0],
        {'extra-only': alpha * mb ** 2, 'alpha-mu': mb + alpha * mb})
    ok(abs(busy.var() - 21.0) < 0.15, f'rfq busy variance by simulation {busy.var()}')
    pick(I, 'p-rfq-busy-minutes', 5, 'nb')
    ok(abs(20.6 - 21.0) < abs(20.6 - 12.0) and 7.5 < 20.6 / 2,'rfq: 20.6 nearer 21.0; Poisson 7.5 well under half of 20.6')
    shown('rfq 6.25', 6.25, mq ** 2, 2); shown('rfq 1.5', 1.5, vq - mq, 1); shown('rfq 56.25', 56.25, mb ** 2, 2)
    shown('rfq 13.5', 13.5, alpha * mb ** 2, 1)


def level2():
    I = load(2)

    # --- p-signal-variants: six variants of 9 months, SSW 172.8, means below
    from scipy.optimize import brentq
    means = dict(A=0.3, B=1.4, C=2.2, D=3.8, E=0.9, F=1.2)
    k_, n_g = 6, 9
    N_ = k_ * n_g
    # data built to hold the six means and SSW = 172.8 exactly
    base = np.array([1, -1, 1, -1, 1, -1, 1, -1, 0], float)
    sc = sqrt(172.8 / (k_ * (base ** 2).sum()))
    rows = [(v, m0 + sc * e) for v, m0 in means.items() for e in base]
    df = pd.DataFrame(rows, columns=['variant', 'ret'])
    ols = smf.ols('ret ~ C(variant)', data=df).fit()
    ok(abs(ols.ssr - 172.8) < 1e-9, 'variants: built SSW')
    msw = Fr(1728, 10) / (N_ - k_)
    num(I, 'p-signal-variants', 1, msw, ols.mse_resid, {'n-minus-one': 172.8 / 53, 'all-months': 172.8 / 54})
    Fv = ols.fvalue
    ok(stats.f.sf(Fv, 5, 48) < 0.05 and abs(Fv - stats.f_oneway(*[df.ret[df.variant == v] for v in means]).statistic) < 1e-9,
       f'variants: the ANOVA rejects at 5% (F {Fv:.3f})')
    pairs = list(itertools.combinations(means, 2))
    lev = Fr(5, 100) / len(pairs)
    num(I, 'p-signal-variants', 2, lev, 0.05 / math.comb(6, 2), {'per-variant': 0.05 / 6, 'halved': 0.05 / 30})
    se_v = sqrt(float(msw) * 2 / n_g)
    # method 2: the standard error statsmodels gives the difference of two dummy coefficients
    ols_b = smf.ols('ret ~ C(variant)', data=df).fit()
    se2 = ols_b.bse['C(variant)[T.B]']
    num(I, 'p-signal-variants', 3, se_v, se2, {'variance': 2 * float(msw) / n_g, 'one-mean': sqrt(float(msw) / n_g)})
    tc = stats.t.ppf(1 - float(lev) / 2, 48)
    tc2 = brentq(lambda q: 2 * stats.t.sf(q, 48) - float(lev), 1, 6)
    shown('variants t crit', 3.0892, tc, 4)
    bar = tc * se_v
    num(I, 'p-signal-variants', 4, bar, tc2 * se2,
        {'variance': tc * 0.8, 'one-mean': tc * sqrt(0.4), 'normal-five': 1.96 * se_v})
    ok(abs(3.0892 * 0.8944 - bar) <= 0.001, 'variants p4: restated inputs land in the key band')
    gaps = {a + b: abs(means[a] - means[b]) for a, b in pairs}
    cnt = lambda c: sum(g >= c for g in gaps.values())
    # method 2: pairwise t-tests on the built rows with the pooled MSW, at the Bonferroni level
    sig = sum(2 * stats.t.sf(abs(means[a] - means[b]) / se_v, 48) < float(lev) for a, b in pairs)
    num(I, 'p-signal-variants', 5, cnt(bar), sig, {'normal-five': cnt(1.96 * se_v), 'one-mean': cnt(tc * sqrt(0.4)), 'variance': cnt(tc * 0.8)})
    ok(min(abs(g - c) for g in gaps.values() for c in (bar, 1.96 * se_v, tc * sqrt(0.4), tc * 0.8)) > 0.05, 'variants: no gap near a bar')
    ok(sorted(k for k, g in gaps.items() if g >= bar) == ['AD', 'DE'] and abs(gaps['DF'] - 2.6) < 1e-9, 'variants: AD and DE clear, DF 2.6')
    ok(max(g for k, g in gaps.items() if k not in ('AD', 'DE')) <= 2.6 + 1e-9 and gaps['AD'] == 3.5 and abs(gaps['DE'] - 2.9) < 1e-9,
       'variants: every other gap 2.6 or less')
    shown('variants 0.4', 0.4, float(msw) / n_g, 1); shown('variants se', 0.8944, se_v, 4)
    shown('variants 1.753', 1.753, 1.96 * 0.8944, 3); shown('variants 1.954', 1.954, 3.0892 * 0.6325, 3)
    shown('variants 2.471', 2.471, 3.0892 * 0.8, 3); shown('variants 2.763', 2.763, 3.0892 * 0.8944, 3)

    # --- p-two-looks: sign test over 10 days, early look at day 5
    P9 = Fr(math.comb(10, 9) + 1, 1024); P5 = Fr(1, 32)
    pats = list(itertools.product((0, 1), repeat=10))
    num(I, 'p-two-looks', 1, P9, sum(sum(s) >= 9 for s in pats) / 1024, {'exactly-nine': 10 / 1024, 'eight-or-more': 56 / 1024})
    ok(stats.binom.sf(7, 10, .5) > 0.05 > stats.binom.sf(8, 10, .5), 'two-looks: 9 is the smallest 5% cut')
    num(I, 'p-two-looks', 2, P5, stats.binom.pmf(5, 5, .5), {'two-sided': 2 / 32})
    num(I, 'p-two-looks', 3, P9 + P5, float(P9) + float(P5), {'independent': 1 - (1 - float(P9)) * (1 - float(P5)), 'product': float(P9 * P5)})
    ok(abs(0.0107 + 0.0313 - float(P9 + P5)) <= 0.0001, 'two-looks p3 restated inputs')
    ok(abs(1 - (1 - 0.0107) * (1 - 0.0313) - 0.0417) < 0.00005, 'two-looks independent printed')
    exact = Fr(32 + 5, 1024)
    alarms = sum(1 for s in pats if sum(s[:5]) == 5 or sum(s) >= 9)
    # method 2: simulate the two-look plan
    rng2 = np.random.default_rng(5)
    sim = rng2.integers(0, 2, (2_000_000, 10))
    rate = float(((sim[:, :5].sum(1) == 5) | (sim.sum(1) >= 9)).mean())
    num(I, 'p-two-looks', 4, exact, alarms / 1024, {'bound': float(P9 + P5), 'independent': 1 - (1 - float(P9)) * (1 - float(P5)), 'day-ten': float(P9)})
    ok(abs(rate - float(exact)) < 0.0005, f'two-looks simulated rate {rate}')
    both = sum(1 for s in pats if sum(s[:5]) == 5 and sum(s) >= 9)
    ok(both == 6 and P9 + P5 == Fr(43, 1024), 'two-looks overlap 6 of 1024, bound 43/1024')
    ok(3 < float(exact / P9) < 4 and 3.5 < float((P9 + P5) / P9) < 4, 'two-looks: over three times; nearly four times')

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

    # fix pass lines in p-twin-books (review findings 9, 10, 17)
    shown('twin 720', 720, 2 * 225 * 1.6, 9); shown('twin 135', 135, 0.6 * 225, 9); shown('twin 180', 180, 2 * 225 * 0.4, 9)
    shown('twin 2.4005', 2.4005, z975 * se_d, 4); shown('twin one tail', 0.0130, stats.t.sf(tt, 119), 4)
    ok(abs(2 * 0.0130 - pt) <= 0.0001, 'twin p4: doubling the stated tail lands in the key band')
    ok(abs(stats.norm.sf(z975 - 2.4005 / se_d) - 0.5) < 1e-3, 'twin: the no-power gain has power one half')


def level3():
    I = load(3)

    # --- p-hedge-ranks: 12 monthly differences, new minus old
    dd = np.array([-3.1, -0.4, -2.2, 0.9, -1.5, -4.0, -0.9, -2.6, 1.2, -0.7, -3.5, -1.8])
    rk = stats.rankdata(abs(dd))
    Wp = Fr(int(2 * rk[dd > 0].sum()), 2)
    # method 2: W+ from the Walsh-average count (number of i <= j with d_i + d_j > 0, ties counted half)
    walsh = sum((1 if dd[i] + dd[j] > 1e-12 else 0.5 if abs(dd[i] + dd[j]) <= 1e-12 else 0)
                for i in range(12) for j in range(i, 12))
    num(I, 'p-hedge-ranks', 1, Wp, walsh, {'tie-low': 3 + 5, 'tie-high': 4 + 5, 'w-minus': rk[dd < 0].sum()})
    ok(sorted(rk[dd > 0]) == [3.5, 5.0] and rk.sum() == 78, 'ranks: the positive months take 3.5 and 5 of 78')
    nn = 12
    var_w = Fr(nn * (nn + 1) * (2 * nn + 1), 24)
    # method 2: the variance of W+ over all 4096 sign patterns of the ranks 1..12
    allW = np.array([sum(r_ for r_, s in zip(range(1, 13), sg) if s) for sg in itertools.product((0, 1), repeat=12)])
    num(I, 'p-hedge-ranks', 2, sqrt(var_w), allW.std(), {'variance': var_w, 'six-divisor': sqrt(4 * var_w)})
    ok(sum(r_ ** 2 for r_ in range(1, 13)) == 650 and allW.mean() == 39, 'ranks: 650 and mean 39')
    z = (float(Wp) - 39) / sqrt(var_w)
    num(I, 'p-hedge-ranks', 3, z, (8.5 - allW.mean()) / allW.std(),
        {'w-minus': (69.5 - 39) / sqrt(var_w), 'variance': (8.5 - 39) / float(var_w), 'no-centre': 8.5 / sqrt(var_w)})
    pz = Phi(z)
    wil = stats.wilcoxon(dd, alternative='less', method='approx', correction=False)
    num(I, 'p-hedge-ranks', 4, pz, stats.norm.sf(-z), {'two-sided': 2 * pz, 'upper': 1 - pz})
    ok(abs(Phi(-2.393) - pz) <= 0.0001 and abs(wil.pvalue - pz) < 0.0001 and wil.statistic == 8.5,
       f'ranks p4: restated z and scipy wilcoxon ({wil.pvalue:.6f}) in the band')
    exact_w = float((allW <= 8).mean())   # W+ with untied ranks: 8.5 lies between 8 and 9
    ok(exact_w < 0.01, f'ranks: exact lower tail of W+ also under 1% ({exact_w:.4f})')
    shown('ranks gap', -30.5, 8.5 - 39, 1); shown('ranks var', 162.5, float(var_w), 1)

    # --- p-spread-day-tail: eight daily spread changes, cut at -4
    d = np.array([-5.6, -1.3, -0.2, 0.6, 1.1, 1.7, 2.4, 8.8]); n8 = 8; cut = -4
    med = float(np.median(d)); raw = float(np.median(abs(d - med)))
    s_m = 1.4826 * raw
    num(I, 'p-spread-day-tail', 1, s_m, sm_mad(d, center=med) * 1.4826 * stats.norm.ppf(0.75), {'raw': raw, 'plain-sd': d.std(ddof=1)}, agree=1e-5)
    ok(np.allclose(np.sort(abs(d - med)), [0.25, 0.25, 0.85, 1.05, 1.55, 2.15, 6.45, 7.95]) and abs(med - 0.85) < 1e-12, 'spread: distances')
    h = 1.06 * s_m * n8 ** -0.2
    num(I, 'p-spread-day-tail', 2, h, 1.06 * s_m / n8 ** 0.2,
        {'plain-sd': 1.06 * d.std(ddof=1) * n8 ** -0.2, 'raw-mad': 1.06 * raw * n8 ** -0.2, 'no-n': 1.06 * s_m})
    ok(abs(1.06 * 1.9274 * 0.65975 - h) <= 0.0001 and abs(1.06 * 1.9274 * n8 ** -0.2 - h) <= 0.0001, 'spread p2 restated inputs')
    kshare = lambda hh: float(Phi((cut - d) / hh).mean())
    pk = kshare(h)
    pk2 = integrate.quad(lambda u: stats.norm.pdf((u - d) / h).sum() / (n8 * h), -60, cut)[0]
    hs = 1.06 * d.std(ddof=1) * n8 ** -0.2
    num(I, 'p-spread-day-tail', 3, pk, pk2, {'plain-sd': kshare(hs), 'raw-mad': kshare(1.06 * raw * n8 ** -0.2), 'empirical': 1 / 8}, agree=1e-7)
    ok(abs(kshare(1.3479) - pk) <= 0.0001, 'spread p3 restated h')
    ordinary = lambda hh: float(Phi((cut - d[1:7]) / hh).sum()) / 8
    ok(ordinary(hs) > 10 * ordinary(h), 'spread: wide bumps push far more of the ordinary days below -4')
    ok(Phi((cut + 5.6) / h) / 8 > 0.9 * pk, 'spread: nearly all of the share from the -5.6 day')
    pn = float(Phi((cut - med) / s_m))
    ratio = pk / pn
    num(I, 'p-spread-day-tail', 4, ratio, pk2 / stats.norm(med, s_m).cdf(cut),
        {'empirical-share': (1 / 8) / pn, 'classic-normal': pk / float(Phi((cut - d.mean()) / d.std(ddof=1)))}, agree=1e-6)
    ok(abs(0.1135 / 0.00593 - ratio) <= 0.1 and abs(0.1135 / pn - ratio) <= 0.1, 'spread p4 restated inputs')
    shown('spread pn', 0.00593, pn, 5); shown('spread z', -2.5164, (cut - med) / s_m, 4)
    shown('bump -5.6', 0.8824, float(Phi(1.6 / h)), 4); shown('bump -1.3', 0.0226, float(Phi(-2.7 / h)), 4)
    shown('n factor', 0.65975, n8 ** -0.2, 5); shown('n factor short', 0.6598, n8 ** -0.2, 4)
    shown('n factor 1.06', 0.6993, 1.06 * n8 ** -0.2, 4)
    shown('mean', 0.9375, d.mean(), 4); shown('sd', 4.0306, d.std(ddof=1), 4); shown('ratio printed', 19.1, ratio, 1)
    shown('empirical ratio', 21.08, 0.125 / pn, 2)

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
    # fix pass (review finding 15): the four patterns that keep 1.2, 2.5 and 9.0 positive
    m4 = sorted(((12.7 + a * 0.8 + b * 0.4) / 5 for a in (1, -1) for b in (1, -1)), reverse=True)
    for pr, v in zip((2.78, 2.62, 2.46, 2.30), m4):
        shown('five-weeks mean', pr, v, 2)
    ok(sum(v >= wk.mean() - 1e-12 for v in m4) == 2, 'five-weeks: two of the four reach 2.62')
    wk2 = np.array([1.2, 0.8, 2.5, -0.4, 2.6]); ab2 = abs(wk2)
    ok(sum(1 for s in pats if np.median(ab2 * np.array(s)) >= 1.2 - 1e-12) == 4
       and sum(1 for s in pats if (ab2 * np.array(s)).sum() >= wk2.sum() - 1e-12) == 2, 'five-weeks: 2.6 for 9.0 keeps 2 and 4')


def level4():
    """Level 4 (second author). Method 1: exact fractions and the conjugate formulas. Method 2: a grid posterior built
    from 36 planted daily figures and 8 planted weekly counts, scipy's distributions, Nelder-Mead on the marginal
    likelihood, a hand Metropolis step, quadrature, the finite-n AR(1) variance of a mean, and a simulation."""
    I = load(4)
    rng = np.random.default_rng(4)

    # --- p-etf-tracking: prior N(-0.3, 0.2^2), daily N(theta, 1.5^2), 36 days with mean -0.82, next 20-day average
    pr0, pr1 = Fr(1) / Fr(2, 10) ** 2, Fr(36) / Fr(15, 10) ** 2            # 25 and 16
    v1 = 1 / (pr0 + pr1)
    m1 = v1 * (pr0 * Fr(-3, 10) + pr1 * Fr(-82, 100))
    days = rng.normal(0, 1.5, 36); days = days - days.mean() - 0.82          # planted data with mean -0.82
    th = np.linspace(-2.5, 1.5, 400001); dth = th[1] - th[0]
    logp = stats.norm.logpdf(th, -0.3, 0.2) + stats.norm.logpdf(days[:, None], th, 1.5).sum(0)
    w = np.exp(logp - logp.max()); w /= w.sum()
    g_mean = float((w * th).sum()); g_var = float((w * (th - g_mean) ** 2).sum())
    num(I, 'p-etf-tracking', 1, sqrt(v1), sqrt(g_var),
        {'add-var': sqrt(0.2 ** 2 + 0.25 ** 2), 'daily-error': 1 / sqrt(25 + 1 / 1.5 ** 2)}, agree=1e-6)
    num(I, 'p-etf-tracking', 2, m1, g_mean,
        {'data-only': -0.82, 'plain-average': (-0.3 - 0.82) / 2, 'swapped': (16 * -0.3 + 25 * -0.82) / 41, 'sign': -float(m1)}, agree=1e-6)
    pv = Fr(225, 100) / 20 + v1
    g_pv = 2.25 / 20 + g_var                                                  # law of total variance on the grid
    num(I, 'p-etf-tracking', 3, sqrt(pv), sqrt(g_pv),
        {'plug-in': 1.5 / sqrt(20), 'one-day': sqrt(2.25 + 1 / 41), 'variance': float(pv), 'theta-only': sqrt(v1)}, agree=1e-6)
    tail = Phi((-1 + 0.5029) / 0.3700)
    g_tail = float((w * Phi((-1 - th) / (1.5 / sqrt(20)))).sum())
    num(I, 'p-etf-tracking', 4, tail, g_tail,
        {'plug-in': Phi((-1 + 0.5029) / (1.5 / sqrt(20))), 'upper': 1 - tail, 'theta-sd': Phi((-1 + 0.5029) / sqrt(1 / 41))}, agree=2e-5)
    ok(abs(tail - Phi((-1 - float(m1)) / sqrt(float(pv)))) < 1e-5, 'etf: rounded inputs move the tail')
    shown('etf prec 25', 25, float(pr0), 9); shown('etf prec 16', 16, float(pr1), 9); shown('etf sd', 0.1562, sqrt(v1), 4)
    shown('etf -20.62', -20.62, float(m1 * 41), 9); shown('etf mean', -0.5029, float(m1), 4)
    shown('etf w prior', 0.61, 25 / 41, 2); shown('etf w data', 0.39, 16 / 41, 2)
    shown('etf 0.1125', 0.1125, 2.25 / 20, 9); shown('etf 0.0244', 0.0244, 1 / 41, 4); shown('etf 0.1369', 0.1369, float(pv), 4)
    shown('etf pred sd', 0.3700, sqrt(pv), 4); shown('etf plug sd', 0.3354, 1.5 / sqrt(20), 4)
    shown('etf z', -1.3435, (-1 + 0.5029) / 0.37, 4); shown('etf tail', 0.0896, tail, 4)
    shown('etf plug tail', 0.0692, Phi((-1 - float(m1)) / (1.5 / sqrt(20))), 4)

    # --- p-iceberg-refills: exponential gaps, 36 totalling 14 minutes, Gamma(5, rate 2) prior; Metropolis from the peak
    a, b = Fr(5 + 36), Fr(2 + 14)                                             # posterior Gamma(41, rate 16)
    gaps = rng.exponential(0.4, 36); gaps = gaps * 14 / gaps.sum()             # planted gaps totalling 14
    ok(abs(gaps.sum() - 14) < 1e-9 and len(gaps) == 36, 'iceberg: planted gaps')

    def logpost(lam):                                                         # likelihood times prior, from scipy
        return stats.expon.logpdf(gaps, scale=1 / lam).sum() + stats.gamma(5, scale=1 / 2).logpdf(lam)
    lg = np.linspace(1.5, 3.5, 2_000_001)                                     # grid of the log posterior
    lp = stats.expon.logpdf(gaps[:, None], scale=1 / lg[::1000]).sum(0)        # coarse check of the likelihood form
    ok(np.allclose(lp, 36 * np.log(lg[::1000]) - 14 * lg[::1000]), 'iceberg: likelihood is lambda^36 e^(-14 lambda)')
    lpg = 36 * np.log(lg) - 14 * lg + stats.gamma(5, scale=0.5).logpdf(lg)
    mode = (a - 1) / b
    num(I, 'p-iceberg-refills', 1, mode, float(lg[np.argmax(lpg)]),
        {'mean': a / b, 'mle': Fr(36, 14), 'prior-mode': Fr(4, 2), 'swapped': Fr(5 + 14 - 1, 2 + 36)}, agree=2e-6)
    m, h = float(mode), 0.4
    up = 40 * ln((m + h) / m) - 16 * h
    dn = 40 * ln((m - h) / m) + 16 * h
    num(I, 'p-iceberg-refills', 2, up, logpost(m + h) - logpost(m),
        {'power-41': 41 * ln((m + h) / m) - 16 * h, 'as-scale': 40 * ln((m + h) / m) - h / 16, 'reversed': -up}, agree=1e-9)
    au, ad = min(1, exp(up)), min(1, exp(dn))
    leave = (au + ad) / 2
    # method 2: simulate the first step of the sampler two million times, with the scipy log posterior
    N = 2_000_000
    sgn = np.where(rng.uniform(size=N) < 0.5, 1.0, -1.0)
    lu = np.log(rng.uniform(size=N))
    d_up, d_dn = logpost(m + h) - logpost(m), logpost(m - h) - logpost(m)
    moved = lu < np.where(sgn > 0, d_up, d_dn)
    num(I, 'p-iceberg-refills', 3, leave, float(moved.mean()),
        {'up-only': au, 'down-only': ad, 'sum': au + ad, 'stay': 1 - leave}, agree=2e-3)
    ok(abs((exp(-0.4632) + exp(-0.5741)) / 2 - leave) < 1e-4, 'iceberg: rounded log ratios keep the key')
    drift = 0.5 * h * (au - ad)
    num(I, 'p-iceberg-refills', 4, drift, float((sgn * h * moved).mean()),
        {'no-half': h * (au - ad), 'no-step': 0.5 * (au - ad), 'sign': -drift}, agree=1e-3)
    ok(abs(0.2 * (0.6293 - 0.5632) - drift) < 1e-4, 'iceberg: rounded chances keep the key')
    ok(d_dn < d_up < 0, 'iceberg: both moves downhill, the upward one less so')
    shown('iceberg 40/16', 2.5, 40 / 16, 9); shown('iceberg mean', 2.5625, 41 / 16, 9); shown('iceberg mle', 2.5714, 36 / 14, 4)
    shown('iceberg swapped', 0.4737, 18 / 38, 4)
    shown('iceberg power', 5.9368, 40 * ln(2.9 / 2.5), 4); shown('iceberg exp', 6.4, 16 * 0.4, 9); shown('iceberg up', -0.4632, up, 4)
    shown('iceberg power-41', -0.3148, 41 * ln(1.16) - 6.4, 4); shown('iceberg scale', 5.9118, 40 * ln(1.16) - 0.025, 4)
    shown('iceberg dn', -0.5741, dn, 4); shown('iceberg au', 0.6293, au, 4); shown('iceberg ad', 0.5632, ad, 4)
    shown('iceberg leave', 0.5962, leave, 4); shown('iceberg sum', 1.1925, au + ad, 4); shown('iceberg stay', 0.4038, 1 - leave, 4)
    shown('iceberg drift', 0.0132, drift, 4); shown('iceberg no-half', 0.0264, 0.4 * (0.6293 - 0.5632), 4)
    shown('iceberg no-step', 0.0330, 0.5 * (0.6293 - 0.5632), 4)

    # --- p-quality-six-markets: six estimates, shared SE 0.5, empirical Bayes in closed form
    e = [Fr(19, 10), Fr(4, 10), Fr(11, 10), Fr(-2, 10), Fr(8, 10), Fr(14, 10)]
    mu = sum(e) / 6
    tot = sum((x - mu) ** 2 for x in e) / 6
    t2 = tot - Fr(1, 4)
    ef = np.array([float(x) for x in e])
    from scipy.optimize import minimize
    r = minimize(lambda p: -stats.norm(p[0], sqrt(0.25 + exp(p[1]))).logpdf(ef).sum(), [0, 0], method='Nelder-Mead',
                 options={'xatol': 1e-12, 'fatol': 1e-14, 'maxiter': 20000})
    ok(abs(r.x[0] - float(mu)) < 1e-6 and float(mu) == 0.9, 'quality: mu-hat is the plain mean 0.9')
    num(I, 'p-quality-six-markets', 1, tot, 0.25 + exp(r.x[1]),
        {'divisor-5': Fr(276, 500), 'root': sqrt(tot)}, agree=1e-6)
    num(I, 'p-quality-six-markets', 2, t2, exp(r.x[1]), {'from-divisor-5': Fr(276, 500) - Fr(1, 4), 'minus-se': tot - Fr(1, 2)}, agree=1e-6)
    B = Fr(1, 4) / (Fr(1, 4) + t2)
    num(I, 'p-quality-six-markets', 3, B, float((1 / t2) / (1 / t2 + 4)),                # prior precision over total
        {'kept-share': 1 - B, 'sd-ratio': 0.5 / (0.5 + sqrt(t2))})
    sh = mu + (1 - B) * (Fr(-2, 10) - mu)
    sh_alt = (4 * -0.2 + float(1 / t2) * 0.9) / (4 + float(1 / t2))           # precision-weighted average
    num(I, 'p-quality-six-markets', 4, sh, sh_alt,
        {'kept-b': mu + B * (Fr(-2, 10) - mu), 'towards-zero': (1 - B) * Fr(-2, 10), 'raw': Fr(-2, 10)})
    ok(abs(float(mu + (1 - Fr(5435, 10000)) * (Fr(-2, 10) - mu)) - float(sh)) < 1e-4, 'quality: B rounded moves the shrunk mean')
    psd = sqrt(1 / (4 + 1 / t2))
    p_up = Phi(0.3978 / psd)
    thg = np.linspace(-3, 4, 700001)
    lw = stats.norm.logpdf(-0.2, thg, 0.5) + stats.norm.logpdf(thg, 0.9, sqrt(float(t2)))
    ww = np.exp(lw - lw.max()); ww /= ww.sum()
    num(I, 'p-quality-six-markets', 5, p_up, float(ww[thg > 0].sum()),
        {'se-as-sd': Phi(0.3978 / 0.5), 'raw': Phi(-0.2 / 0.5), 'lower': 1 - p_up, 'tau-as-sd': Phi(0.3978 / sqrt(t2))}, agree=2e-5)
    ok(abs(p_up - Phi(float(sh) / psd)) < 2e-5, 'quality: rounded shrunk mean moves the tail')
    for printed, x in ((1, Fr(1)), (0.25, Fr(1, 4)), (0.04, Fr(4, 100)), (1.21, Fr(121, 100)), (0.01, Fr(1, 100))):
        ok(any((y - mu) ** 2 == x for y in e), f'quality squared gap {printed}')
    shown('q 2.76', 2.76, float(tot * 6), 9); shown('q 0.46', 0.46, float(tot), 9); shown('q 0.552', 0.552, 2.76 / 5, 9)
    shown('q 0.21', 0.21, float(t2), 9); shown('q B', 0.5435, float(B), 4); shown('q 1-B', 0.4565, float(1 - B), 4)
    shown('q tau', 0.4583, sqrt(t2), 4); shown('q sd ratio', 0.5 / (0.5 + 0.4583), 0.5 / (0.5 + sqrt(t2)), 4)
    shown('q 0.5022', 0.5022, float((1 - B) * Fr(11, 10)), 4); shown('q shrunk', 0.3978, float(sh), 4)
    shown('q prec', 8.762, float(4 + 1 / t2), 3); shown('q psd', 0.3378, psd, 4); shown('q p', 0.8805, p_up, 4)
    shown('q raw 34%', 34, 100 * Phi(-0.2 / 0.5), 0); shown('q 88%', 88, 100 * p_up, 0)

    # --- p-four-books: four books, SE 2, theta_j ~ N(mu, 1), mu ~ N(0, 1.5^2); Gibbs on (theta, mu)
    s2, t2b, J, v0 = Fr(4), Fr(1), 4, Fr(9, 4)
    Bk = (1 / t2b) / (1 / t2b + 1 / s2)                                       # weight on mu in theta_j | mu
    c = (J / t2b) / (1 / v0 + J / t2b)                                        # weight on the mean of theta in mu | theta
    phi = Bk * c
    yb = np.array([1.3, -0.6, 2.4, 0.5])                                      # planted estimates; they do not enter phi
    # method 2: run the Gibbs sampler, then read the lag-1 autocorrelation of mu
    T = 200_000
    vth = float(1 / (1 / t2b + 1 / s2)); vmu_c = float(1 / (1 / v0 + J / t2b))
    zt = rng.standard_normal((T, J)); zm = rng.standard_normal(T)
    mus = np.empty(T); cur = 0.0
    for t in range(T):
        th = float(Bk) * cur + float(1 - Bk) * yb + sqrt(vth) * zt[t]
        cur = float(c) * th.mean() + sqrt(vmu_c) * zm[t]
        mus[t] = cur
    phi_sim = float(np.corrcoef(mus[1000:-1], mus[1001:])[0, 1])
    num(I, 'p-four-books', 1, Bk, 1 / (1 + float(t2b) / float(s2)),
        {'estimate-weight': 1 - Bk, 'sd-weights': Fr(1) / (1 + Fr(1, 2))})
    ok(Bk == s2 / (s2 + t2b), 'books: the slope is lesson 18 B = s^2/(s^2 + tau^2)')
    num(I, 'p-four-books', 2, phi, phi_sim,
        {'square': Bk ** 2, 'mu-slope': c, 'no-quarter': Bk * v0 / (v0 + t2b), 'first-slope': Bk}, agree=1e-2)
    n = 4 * 2500
    ess = n * (1 - phi) / (1 + phi)
    k = np.arange(1, 2500)
    infl = float(1 + 2 * ((1 - k / 2500) * float(phi) ** k).sum())             # exact finite-n inflation of a chain mean
    num(I, 'p-four-books', 3, ess, n / infl,
        {'no-plus-phi': n * (1 - phi), 'one-chain': ess / 4, 'independent': n, 'square': n * (1 - Bk ** 2) / (1 + Bk ** 2)}, agree=2e-3)
    # the posterior sd of mu, twice: the marginal of the mean estimate, and the inverse of the joint precision matrix
    vmu = 1 / (1 / v0 + J / (s2 + t2b))
    P = np.zeros((J + 1, J + 1))
    for j in range(J):
        P[j, j] = 1 / float(s2) + 1 / float(t2b); P[j, J] = P[J, j] = -1 / float(t2b)
    P[J, J] = 1 / float(v0) + J / float(t2b)
    ok(abs(sqrt(np.linalg.inv(P)[J, J]) - sqrt(vmu)) < 1e-12, 'books: posterior sd of mu by the joint precision')
    ok(abs(float(np.std(mus[1000:])) - sqrt(vmu)) < 0.02, 'books: the Gibbs draws have the posterior sd')
    shown('books sd mu', 0.8964, sqrt(vmu), 4)
    err = 0.8964 / sqrt(1627.9)
    num(I, 'p-four-books', 4, err, sqrt(vmu) * sqrt(infl / n),
        {'independent': 0.8964 / sqrt(n), 'one-chain': 0.8964 / sqrt(ess / 4), 'no-plus-phi': 0.8964 / sqrt(2800),
         'square': 0.8964 / sqrt(2195.1)}, agree=2e-5)
    need = n * (0.0222 / 0.01) ** 2 / 4
    exact_need = float((vmu / Fr(1, 10000)) * (1 + phi) / (1 - phi)) / 4
    brute = next(m_ for m_ in range(1000, 20000) if sqrt(vmu) * sqrt((1 + float(phi)) / (1 - float(phi)) / (4 * m_)) <= 0.01)
    ok(abs(brute - exact_need) <= 1, f'books: brute search {brute} against {exact_need:.1f}')
    num(I, 'p-four-books', 5, exact_need, brute, {'total': 4 * need, 'linear': n * 2.22 / 4, 'no-ar': 0.8964 ** 2 / 0.01 ** 2 / 4}, agree=1)
    ok(abs(round(need, -2) - 12300) < 1e-9 and abs(round(exact_need, -2) - 12300) < 1e-9, 'books: both routes round to 12,300')
    shown('books prec mu', 1, 1 / float(t2b), 9); shown('books prec est', 0.25, 1 / float(s2), 9); shown('books 1/1.25', 0.8, 1 / 1.25, 9)
    shown('books 0.6667', 0.6667, 1 / 1.5, 4); shown('books B', 0.8, 4 / (4 + 1), 9)
    shown('books 1/2.25', 0.4444, 1 / 2.25, 4); shown('books c', 0.9, 4 / (4 + 1 / 2.25), 9); shown('books 0.72', 0.72, float(phi), 9)
    shown('books 0.5538', 0.5538, float(Bk * v0 / (v0 + 1)), 4); shown('books 72%', 72, 100 * float(phi), 9)
    shown('books ess', 1627.9, float(ess), 1); shown('books 0.28', 0.28, 1 - float(phi), 9); shown('books 1.72', 1.72, 1 + float(phi), 9)
    shown('books one', 407.0, float(ess) / 4, 1); shown('books 2195.1', 2195.1, 10000 * 0.36 / 1.64, 1)
    ok(abs(float(ess) / n - 1 / 6) < 0.005, 'books: about a sixth of an independent draw')
    shown('books root', 40.35, sqrt(1627.9), 2); shown('books err', 0.0222, err, 4); shown('books iid', 0.0090, 0.8964 / 100, 4)
    shown('books one err', 0.0444, 0.8964 / sqrt(407.0), 4); shown('books 2800 err', 0.0169, 0.8964 / sqrt(2800), 4)
    shown('books sq err', 0.0191, 0.8964 / sqrt(2195.1), 4)
    ok(abs(err / 0.8964 - 1 / 40) < 0.001 and abs(2 * err - 0.04) < 0.005, 'books: a fortieth of the sd; +/- 0.04 at two errors')
    shown('books ratio', 4.93, (0.0222 / 0.01) ** 2, 2); shown('books total', 49300, 4 * need, -2); shown('books per chain', 12300, need, -2)
    shown('books 2.22', 2.22, 0.0222 / 0.01, 9); shown('books linear', 5550, n * 2.22 / 4, 9)
    shown('books no-ar', 2000, 0.8964 ** 2 / 1e-4 / 4, -2); ok(abs(need / (0.8964 ** 2 / 1e-4 / 4) - 6) < 0.5, 'books: about six times as many')

    # --- fix pass: normal-table values printed in two questions (review finding 10)
    for zv, pv in ((1.3435, 0.9104), (1.4821, 0.9308), (3.1825, 0.9993), (0.7956, 0.7869), (0.8680, 0.8073), (1.1776, 0.8805)):
        shown(f'Phi({zv})', pv, Phi(zv), 4)
    shown('etf z plug', 1.4821, 0.4971 / 0.3354, 4); shown('etf z theta', 3.1825, 0.4971 / 0.1562, 4)
    shown('q z se', 0.7956, 0.3978 / 0.5, 4); shown('q z tau', 0.8680, 0.3978 / 0.4583, 4); shown('q z key', 1.1776, 0.3978 / 0.3378, 4)
    for given, iid, k, wid in ((1 - 0.9104, 'p-etf-tracking', 4, None), (1 - 0.9308, 'p-etf-tracking', 4, 'plug-in'),
                               (1 - 0.9993, 'p-etf-tracking', 4, 'theta-sd'), (0.8805, 'p-quality-six-markets', 5, None),
                               (0.7869, 'p-quality-six-markets', 5, 'se-as-sd'), (0.8073, 'p-quality-six-markets', 5, 'tau-as-sd'),
                               (1 - 0.8805, 'p-quality-six-markets', 5, 'lower')):
        wd = I[iid]['parts'][k - 1]['widget']
        x = wd if wid is None else next(y for y in wd['wrong'] if y['id'] == wid)
        ok(abs(given - x.get('answer', x.get('value'))) <= x['tol']['abs'] + 1e-12, f'{iid} p{k}: table value {given:.4f} lands in {wid or "key"}')
    shown('etf add-var', 0.3202, sqrt(0.04 + 0.0625), 4); shown('q sd-ratio', 0.5218, 0.5 / (0.5 + 0.4583), 4)
    shown('q 0.5978', 0.5978, 0.5435 * 1.1, 4); shown('q 0.3022', 0.3022, 0.9 - 0.5978, 4); shown('q 0.1195', 0.1195, 1 - 0.8805, 4)


for n, f in ((1, level1), (2, level2), (3, level3), (4, level4)):
    if present(n):
        f()

if fails:
    for f in fails:
        print('FAIL', f)
    print(f'{len(fails)} of {checks} checks failed')
    sys.exit(1)
print(f'all {checks} checks passed')
