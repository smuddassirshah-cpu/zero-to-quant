"""Second reader's recomputation of stat-models problems-1 to problems-3.

Imports nothing from the author's script. Every data set, table and model is typed from the
problem's prose. Route 1 is the closed form; route 2 is a fit, an enumeration or an integral
(statsmodels GLM on rows built to hold each table, a hand IRLS loop, scipy tests on built
samples, all labellings and sign patterns listed, quad of the density).
Exit 0 always on a clean run of the script; a failing check prints a FINDING line (CI rule,
session AE). Claims found false by reading are also printed as FINDING lines.
Run: <venv>/bin/python docs/reports/problems-stat-models-numbers-read.py
"""
import itertools
import json
import math
import os
import sys
import warnings

import numpy as np
from scipy import integrate, stats

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'stat-models')
SETS = {n: json.load(open(os.path.join(CDIR, f'problems-{n}.json'))) for n in (1, 2, 3)}
checks = 0
findings = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        findings.append(msg)


def claim(msg):
    findings.append(msg)


def item(n, iid):
    return next(i for i in SETS[n]['items'] if i['id'] == iid)


def band(w):
    t = w.get('tol', {})
    a = w['answer'] if 'answer' in w else w['value']
    return a - t.get('abs', 0), a + t.get('abs', 0)


def num(n, iid, part, mine, mine2, slips, dp=None, fed=None):
    """mine, mine2: the key by two routes. slips: {id: value rebuilt from the slip}.
    dp: places the part asks for. fed: value a learner gets from the rounded input the part restates."""
    w = item(n, iid)['parts'][part - 1]['widget']
    tag = f'problems-{n} {iid} p{part}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    lo, hi = band(w)
    ok(abs(mine - mine2) <= 1e-6 * max(1, abs(mine)), f'{tag}: my two routes differ {mine} {mine2}')
    ok(abs(w['answer'] - mine) <= 2e-6 * max(1, abs(mine)), f'{tag}: key {w["answer"]} against mine {mine}')
    if dp is not None:
        r = round(mine, dp)
        ok(lo - 1e-12 <= r <= hi + 1e-12, f'{tag}: rounding {r} to {dp} dp is refused')
    if fed is not None:
        ok(lo - 1e-12 <= fed <= hi + 1e-12, f'{tag}: value from the restated input {fed} is refused')
    ids = {x['id'] for x in w.get('wrong', [])}
    ok(ids == set(slips), f'{tag}: slip ids {sorted(ids)} against mine {sorted(slips)}')
    bands = []
    for x in w.get('wrong', []):
        xl, xh = x['value'] - x['tol']['abs'], x['value'] + x['tol']['abs']
        if x['id'] in slips:
            v = slips[x['id']]
            ok(xl - 1e-12 <= v <= xh + 1e-12, f'{tag}: slip {x["id"]} value {x["value"]} against rebuilt {v}')
        ok(xh < lo or xl > hi, f'{tag}: slip {x["id"]} band meets the key band')
        for (bl, bh, bid) in bands:
            ok(xh < bl or xl > bh, f'{tag}: slip bands {x["id"]} and {bid} meet')
        bands.append((xl, xh, x['id']))
    fb = item(n, iid)['parts'][part - 1]['feedback'].get('byKey', {})
    ok(set(fb) == ids, f'{tag}: byKey lines {sorted(fb)} against slip ids {sorted(ids)}')


def shown(tag, printed, value, dp):
    ok(abs(round(value, dp) - printed) < 0.5 * 10 ** -dp + 1e-12, f'{tag}: prints {printed}, value {value}')


def text_of(n, iid):
    return json.dumps(item(n, iid), ensure_ascii=False)


def has(n, iid, s):
    ok(s in text_of(n, iid), f'problems-{n} {iid}: expected the text {s!r}')


# ---------------------------------------------------------------- set shape
for n, lessons in ((1, 5), (2, 4), (3, 4)):
    S = SETS[n]
    ok(3 <= len(S['items']) <= 5, f'problems-{n}: item count')
    ok(max(i['difficulty'] for i in S['items']) == 5, f'problems-{n}: no difficulty 5')
    parts = [p for i in S['items'] for p in i['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(typed * 3 >= 2 * len(parts), f'problems-{n}: typed share')
    for i in S['items']:
        ok(3 <= len(i['parts']) <= 5, f'problems-{n} {i["id"]}: part count')
        ok(set(i['skills']) <= {{1: 'sm-glm', 2: 'sm-anova', 3: 'sm-nonpar'}[n]}, f'problems-{n} {i["id"]}: skills')
        for p in i['parts']:
            ok(len([s for s in p['explain']['text'].replace('e.g.', '').split('. ') if s.strip()]) <= 3,
               f'problems-{n} {i["id"]}: explain over three sentences: {p["explain"]["text"][:50]}')

# ================================================================ problems-1
import statsmodels.api as sm

# --- p-ipo-underwriter: 24 top-tier, 18 above; 36 others, 12 above
x = np.r_[np.ones(24), np.zeros(36)]
y = np.r_[np.ones(18), np.zeros(6), np.ones(12), np.zeros(24)]
fit = sm.GLM(y, sm.add_constant(x), family=sm.families.Binomial()).fit()
fit0 = sm.GLM(y, np.ones(60), family=sm.families.Binomial()).fit()
b1 = math.log((18 / 6) / (12 / 24))
num(1, 'p-ipo-underwriter', 1, b1, fit.params[1],
    {'odds-ratio': 6, 'share-ratio': math.log(0.75 / (1 / 3)), 'top-only': math.log(3)}, dp=4)
ll = 18 * math.log(.75) + 6 * math.log(.25) + 12 * math.log(1 / 3) + 24 * math.log(2 / 3)
num(1, 'p-ipo-underwriter', 2, -2 * ll, fit.deviance,
    {'no-two': -ll, 'risers-only': -2 * (18 * math.log(.75) + 12 * math.log(1 / 3))}, dp=3)
lr = 120 * math.log(2) + 2 * ll
num(1, 'p-ipo-underwriter', 3, lr, fit0.deviance - fit.deviance,
    {'null-only': 120 * math.log(2), 'halved': lr / 2}, dp=3, fed=round(120 * math.log(2), 3) - 72.821)
p_lr = stats.chi2.sf(lr, 1)
p_lr2 = 2 * stats.norm.sf(math.sqrt(lr))          # chi-square on 1 df is a squared normal
num(1, 'p-ipo-underwriter', 4, p_lr, p_lr2,
    {'two-df': math.exp(-lr / 2), 'lower-tail': 1 - p_lr}, dp=4, fed=stats.chi2.sf(10.357, 1))
shown('ipo loglik', -36.4106, ll, 4); shown('ipo null dev', 83.178, 120 * math.log(2), 3)
shown('ipo share', 0.3333, 1 / 3, 4)

# --- p-settlement-fails: any months with the stated totals give the same fit
t = np.array([10, 8, 9, 7, 8, 8, 5, 6, 4, 5.0]); yf = np.array([6, 5, 5, 4, 5, 5, 7, 8, 6, 7.0])
xf = np.r_[np.zeros(6), np.ones(4)]
ok(t[:6].sum() == 50 and t[6:].sum() == 20 and yf[:6].sum() == 30 and yf[6:].sum() == 28, 'settlement rows')
pf = sm.GLM(yf, sm.add_constant(xf), family=sm.families.Poisson(), offset=np.log(t)).fit()
rr = (28 / 20) / (30 / 50)
num(1, 'p-settlement-fails', 1, rr, math.exp(pf.params[1]),
    {'counts-only': 28 / 30, 'log-scale': math.log(rr), 'inverted': 1 / rr}, dp=4)
ok(abs(pf.mu[:6].sum() - 30) < 1e-8 and abs(pf.mu[6:].sum() - 28) < 1e-8, 'settlement: fitted fails match by group')
se = math.sqrt(1 / 30 + 1 / 28)
A = np.array([[58, 28], [28, 28.0]])
ok(abs(np.linalg.inv(A)[1, 1] - 58 / 840) < 1e-12 and abs(np.linalg.det(A) - 840) < 1e-9, 'settlement: inverse entry')
num(1, 'p-settlement-fails', 2, se, pf.bse[1],
    {'variance': 58 / 840, 'wrong-entry': math.sqrt(28 / 840), 'no-inverse': 1 / math.sqrt(28)}, dp=4)
phi = 17.6 / 8
zq = math.log(rr) / (se * math.sqrt(phi))
num(1, 'p-settlement-fails', 3, zq, pf.params[1] / (pf.bse[1] * math.sqrt(2.2)),
    {'poisson-z': math.log(rr) / se, 'phi-not-root': math.log(rr) / (se * phi),
     'ten-df': math.log(rr) / (se * math.sqrt(1.76))}, dp=3, fed=0.8473 / (0.2628 * math.sqrt(2.2)))
lo_q = math.exp(math.log(rr) - 1.96 * se * math.sqrt(phi))
num(1, 'p-settlement-fails', 4, lo_q, math.exp(pf.params[1] - 1.96 * pf.bse[1] * math.sqrt(2.2)),
    {'poisson-se': math.exp(math.log(rr) - 1.96 * se), 'log-scale': math.log(rr) - 1.96 * se * math.sqrt(phi)},
    dp=3, fed=math.exp(0.84730 - 1.96 * 0.38975))
ok(lo_q - stats.norm.ppf(.975) < 1e9 and abs(math.exp(math.log(rr) - stats.norm.ppf(.975) * se * math.sqrt(phi)) - 1.086964) < 1e-3,
   'settlement p4: the exact normal quantile leaves the band')
shown('settle se q', 0.38975, se * math.sqrt(phi), 5); shown('settle log end', 0.0834, math.log(rr) - 1.96 * se * math.sqrt(phi), 4)
shown('settle beta', 0.8473, math.log(rr), 4)
# The lesson (l5 screen 4) refers the scaled test to F(1, residual df); the matching interval uses t on 8 df.
lo_t = math.exp(math.log(rr) - stats.t.ppf(.975, 8) * se * math.sqrt(phi))
if lo_t < 1 < lo_q:
    claim(f'problems-1 p-settlement-fails p4: interval end {lo_q:.3f} uses 1.96 with a dispersion on 8 df; '
          f't_8 = {stats.t.ppf(.975, 8):.3f} gives {lo_t:.3f}, below 1, so the explain line "run above the domestic rate" does not hold (review finding 2)')

# --- p-recon-breaks: hand IRLS on the six days
yb = np.array([0, 6, 2, 5, 1, 4.0]); beta = 0.0; path = []
for _ in range(30):
    mu = np.full(6, math.exp(beta)); z = beta + (yb - mu) / mu
    beta = float(np.sum(mu * z) / np.sum(mu)); path.append(beta)
pb = sm.GLM(yb, np.ones(6), family=sm.families.Poisson()).fit()
num(1, 'p-recon-breaks', 1, 2.0, path[0], {'mean-count': yb.mean(), 'jump-to-fit': math.log(3)}, dp=3)
num(1, 'p-recon-breaks', 2, 1 + 3 * math.exp(-2), path[1],
    {'no-eta': (3 - math.e ** 2) / math.e ** 2, 'sign': 2 - (3 - math.e ** 2) / math.e ** 2}, dp=4)
num(1, 'p-recon-breaks', 3, math.log(3), pb.params[0], {'mean-scale': 3, 'one-more': path[2]}, dp=4)
ok(abs(path[-1] - math.log(3)) < 1e-12 and all(a > b for a, b in zip(path[:6], path[1:7])), 'recon: path falls to ln 3')
ok(round(path[4], 4) == 1.0986 and round(path[3], 4) != 1.0986, 'recon: "two more steps settle" after beta3')
chi = float(((yb - 3) ** 2 / 3).sum())
num(1, 'p-recon-breaks', 4, chi / 5, pb.pearson_chi2 / pb.df_resid, {'six-df': chi / 6, 'chi-only': chi}, dp=4)
shown('recon e2', 7.3891, math.e ** 2, 4)

# --- p-auction-tails
def mu_c(c):
    return 1 / (1 + math.exp(-(2.6 - 1.3 * c)))
from scipy.optimize import brentq
num(1, 'p-auction-tails', 1, 2.6 / 1.3, brentq(lambda c: mu_c(c) - .5, 0, 5), {'intercept': 2.6, 'inverted': 1.3 / 2.6}, dp=3)
m25 = mu_c(2.5)
num(1, 'p-auction-tails', 2, m25, stats.logistic.cdf(-0.65), {'sign': 1 - m25, 'linear': -0.65}, dp=4)
sim = stats.binom(12, m25)
num(1, 'p-auction-tails', 3, m25 * (1 - m25), stats.bernoulli(m25).var(), {'poisson-var': m25, 'gamma-var': m25 ** 2},
    dp=4, fed=0.3430 * 0.6570)
num(1, 'p-auction-tails', 4, math.sqrt(12 * m25 * (1 - m25)), sim.std(),
    {'variance': 12 * m25 * (1 - m25), 'one-auction': math.sqrt(m25 * (1 - m25)), 'poisson': math.sqrt(12 * m25)},
    dp=3, fed=math.sqrt(12 * 0.2253))
shown('auction mean', 4.12, 12 * m25, 2)
ok(mu_c(1.9) > .5 > mu_c(2.1), 'auction: a thinner cover makes a tail likelier')

# ================================================================ problems-2
# --- p-venue-markouts
ng = np.array([10, 6, 8]); mg = np.array([1.5, 3.5, 1.0])
gm = float((ng * mg).sum() / 24)
num(2, 'p-venue-markouts', 1, gm, 44 / 24, {'unweighted': mg.mean(), 'coef-mean': (1.5 + 2.0 - 0.5) / 3}, dp=4)
ssb = float((ng * (mg - gm) ** 2).sum()); ssb2 = float((ng * mg ** 2).sum() - 24 * gm ** 2)
num(2, 'p-venue-markouts', 2, ssb, ssb2,
    {'unweighted-mean': float((ng * (mg - 2) ** 2).sum()), 'no-counts': float(((mg - gm) ** 2).sum())}, dp=3,
    fed=float((ng * (mg - 1.8333) ** 2).sum()))
# rows that hold the three means and a residual SE of 2.4 exactly
rng = np.random.default_rng(7); rows = []; labs = []
raw = [rng.standard_normal(k) for k in ng]; raw = [r - r.mean() for r in raw]
sc = 2.4 / math.sqrt(sum((r ** 2).sum() for r in raw) / 21)
grp = [m + sc * r for m, r in zip(mg, raw)]
F2, pF2 = stats.f_oneway(*grp)
F = (ssb / 2) / 2.4 ** 2
num(2, 'p-venue-markouts', 3, F, float(F2), {'not-squared': (ssb / 2) / 2.4, 'no-df': ssb / 5.76}, dp=4, fed=(23.333 / 2) / 5.76)
num(2, 'p-venue-markouts', 4, stats.f.sf(F, 2, 21), float(pF2),
    {'lower-tail': stats.f.cdf(F, 2, 21), 'total-df': stats.f.sf(F, 2, 23)}, dp=4, fed=stats.f.sf(2.0255, 2, 21))
shown('venue parts', 1.111, 10 * (1.5 - gm) ** 2, 3); shown('venue parts', 16.667, 6 * (3.5 - gm) ** 2, 3)
shown('venue parts', 5.556, 8 * (1 - gm) ** 2, 3); shown('venue msb', 11.667, ssb / 2, 3)

# --- p-twin-books
sd_d = math.sqrt(2 * 15 ** 2 * (1 - .6)); cov = np.array([[225, 135], [135, 225.0]]); c = np.array([1, -1.0])
num(2, 'p-twin-books', 1, sd_d, math.sqrt(c @ cov @ c),
    {'plus-rho': math.sqrt(2 * 225 * 1.6), 'no-rho': 15 * math.sqrt(2), 'no-two': math.sqrt(225 * .4)}, dp=4)
za, zb = 1.95996, 0.84162
delta = (za + zb) * sd_d / math.sqrt(120)
# route 2: the gain at which a z-test on 120 differences has 80% power
d2 = brentq(lambda d: stats.norm.sf(za - d / (sd_d / math.sqrt(120))) - stats.norm.cdf(zb), 0.1, 20)
ok(abs(delta - d2) < 1e-6, 'twin-books p2: power route')
num(2, 'p-twin-books', 2, delta, d2, {'unpaired': (za + zb) * 15 * math.sqrt(2) / math.sqrt(120), 'no-power': za * sd_d / math.sqrt(120)},
    dp=4, fed=(za + zb) * 13.4164 / math.sqrt(120))
dd = rng.standard_normal(120); dd = (dd - dd.mean()) / dd.std(ddof=1) * 14.1 + 2.9
tt, pt = stats.ttest_1samp(dd, 0)
num(2, 'p-twin-books', 3, 2.9 / (14.1 / math.sqrt(120)), float(tt),
    {'no-root': 2.9 / 14.1, 'planned-sd': 2.9 / (sd_d / math.sqrt(120))}, dp=4)
p_int = 2 * integrate.quad(lambda u: stats.t.pdf(u, 119), float(tt), np.inf)[0]
ok(abs(p_int - pt) < 1e-8, 'twin-books p4: quad of the t density')
num(2, 'p-twin-books', 4, float(pt), p_int, {'one-sided': pt / 2, 'lower-tail': 1 - pt / 2}, dp=4, fed=2 * stats.t.sf(2.2530, 119))
shown('twin se', 1.22474, sd_d / math.sqrt(120), 5); shown('twin se obs', 1.28715, 14.1 / math.sqrt(120), 5)
shown('twin z sum', 2.80158, za + zb, 5)
ok(abs(stats.norm.sf(za - 2.4005 / 1.22474) - 0.5) < 1e-3, 'twin-books: the no-power gain has power one half')

# --- p-rerun-the-test
a = rng.standard_normal(40); b = rng.standard_normal(40); a -= a.mean(); b -= b.mean()
s = 4.5 / math.sqrt(((a ** 2).sum() + (b ** 2).sum()) / 78)
old, new = 6.2 + s * a, 4.4 + s * b
t2, p2 = stats.ttest_ind(old, new); F3, p3 = stats.f_oneway(old, new)
tk = 1.8 / (4.5 * math.sqrt(2 / 40))
num(2, 'p-rerun-the-test', 1, tk, float(t2), {'one-sample-se': 1.8 / (4.5 / math.sqrt(40)), 'no-root': 1.8 / 4.5}, dp=4)
num(2, 'p-rerun-the-test', 2, tk ** 2, float(F3), {'same': tk, 'doubled': 2 * tk}, dp=2, fed=1.7889 ** 2)
num(2, 'p-rerun-the-test', 3, stats.f.sf(3.2, 1, 78), float(p2), {'one-tail-t': p2 / 2, 'lower-tail': 1 - p2}, dp=4)
z9 = 1.28155
n_arm = 2 * (za + z9) ** 2 * 4.5 ** 2 / 1.8 ** 2
# route 2: smallest n whose normal-theory power reaches 90%
n2 = next(k for k in range(2, 1000) if stats.norm.sf(za - 1.8 / (4.5 * math.sqrt(2 / k))) >= stats.norm.cdf(z9) - 1e-9)
num(2, 'p-rerun-the-test', 4, math.ceil(n_arm), n2,
    {'eighty': math.ceil(2 * (za + zb) ** 2 * 6.25), 'no-two': math.ceil(n_arm / 2), 'one-sided': math.ceil(2 * (1.64485 + z9) ** 2 * 6.25)})
shown('rerun se', 1.00623, 4.5 * math.sqrt(2 / 40), 5); shown('rerun n', 131.34, n_arm, 2)
shown('rerun zsum', 3.24151, za + z9, 5); shown('rerun zsq', 10.5074, (za + z9) ** 2, 4)

# ================================================================ problems-3
# --- p-ten-trading-days
X = [1.8, 2.6, 0.9, 3.1]; Y = [0.4, 1.1, -0.6, 0.2, 0.7, -0.2]
U = sum(xv > yv for xv in X for yv in Y)
ranks = stats.rankdata(X + Y)
RX = ranks[:4].sum()
ok(sorted(ranks[:4]) == [6, 8, 9, 10], 'ten-days: X ranks')
num(3, 'p-ten-trading-days', 1, U, RX - 10, {'rank-sum': RX, 'u-y': 24 - U})
labs = list(itertools.combinations(range(1, 11), 4))
num(3, 'p-ten-trading-days', 2, len(labs), math.comb(10, 4), {'ordered': 10 * 9 * 8 * 7, 'sign-flips': 2 ** 10})
ext = [l for l in labs if sum(l) - 10 >= 23]
ok(sorted(ext) == [(6, 8, 9, 10), (7, 8, 9, 10)], 'ten-days: the two extreme labellings')
p_mw = stats.mannwhitneyu(X, Y, alternative='greater', method='exact').pvalue
num(3, 'p-ten-trading-days', 3, len(ext) / 210, float(p_mw), {'one-split': 1 / 210, 'plus-one': 3 / 211}, dp=4)
two = sum(1 for l in labs if abs(sum(l) - 10 - 12) >= 11) / 210
num(3, 'p-ten-trading-days', 4, two, float(stats.mannwhitneyu(X, Y, method='exact').pvalue),
    {'one-sided': 2 / 210, 'halved': 1 / 210}, dp=4)

# --- p-block-markout-tail
d = np.array([-1.4, -0.2, 0.3, 0.5, 0.9, 1.6, 7.5]); med = float(np.median(d))
mad = float(np.median(np.abs(d - med)))
ok(sorted(np.round(np.abs(d - med), 10)) == [0, 0.2, 0.4, 0.7, 1.1, 1.9, 7.0], 'block: sorted distances')
smad = 1.4826 * mad
num(3, 'p-block-markout-tail', 1, smad, float(stats.median_abs_deviation(d)) * 1.4826,
    {'raw': mad, 'plain-sd': d.std(ddof=1)}, dp=4)
ok(abs(stats.median_abs_deviation(d, scale='normal') - smad) < 1e-4, 'block: scipy scaled MAD to 4 dp')
h = 1.06 * smad * 7 ** -0.2
num(3, 'p-block-markout-tail', 2, h, 1.06 * smad / 7 ** 0.2,
    {'plain-sd': 1.06 * d.std(ddof=1) * 7 ** -.2, 'raw-mad': 1.06 * mad * 7 ** -.2, 'no-n': 1.06 * smad},
    dp=4, fed=1.06 * 1.0378 * 7 ** -.2)


def kshare(hh, cut=-1.0):
    return float(np.mean(stats.norm.cdf((cut - d) / hh)))


kde = stats.gaussian_kde(d, bw_method=h / d.std(ddof=1))
pk = kshare(h)
num(3, 'p-block-markout-tail', 3, pk, float(kde.integrate_box_1d(-np.inf, -1)),
    {'plain-sd': kshare(1.06 * d.std(ddof=1) * 7 ** -.2), 'raw-mad': kshare(1.06 * mad * 7 ** -.2), 'empirical': 1 / 7},
    dp=4, fed=kshare(0.7454))
pn = float(stats.norm.cdf((-1 - med) / smad))
num(3, 'p-block-markout-tail', 4, pk / pn, kshare(h) / stats.norm(med, smad).cdf(-1),
    {'inverted': pn / pk, 'classic-normal': pk / float(stats.norm.cdf((-1 - d.mean()) / d.std(ddof=1)))},
    dp=2, fed=0.1306 / 0.0742)
shown('block bump', 0.7042, float(stats.norm.cdf(0.4 / h)), 4); shown('block bump', 0.1416, float(stats.norm.cdf(-0.8 / h)), 4)
shown('block normal', 0.0742, pn, 4); shown('block z', -1.4453, (-1 - med) / smad, 4)
shown('block mean', 1.3143, d.mean(), 4); shown('block sd', 2.883, d.std(ddof=1), 3)
shown('block nfac', 0.6776, 7 ** -.2, 4); shown('block fac', 0.7183, 1.06 * 7 ** -.2, 4)
# claim in p3 byKey plain-sd: "Its wide bumps spread the spike's mass into the left tail"
hw = 1.06 * d.std(ddof=1) * 7 ** -.2
spike = float(stats.norm.cdf((-1 - 7.5) / hw)) / 7
if 'spike\'s mass into the left tail' in text_of(3, 'p-block-markout-tail') and spike < 0.001:
    claim(f'problems-3 p-block-markout-tail p3 byKey plain-sd: says the wide bumps spread the spike\'s mass into the left tail; '
          f'at h = {hw:.4f} the 7.5 bump puts {spike:.6f} of the estimate below -1, of {kshare(hw):.4f} in all (review finding 14)')

# --- p-five-weeks-flip
wk = [1.2, 0.8, 2.5, -0.4, 9.0]


def counts(vals):
    ab = [abs(v) for v in vals]; obs_med = sorted(vals)[2]; obs_sum = sum(vals)
    cm = cs = c2 = 0
    for sg in itertools.product((1, -1), repeat=5):
        v = [a * q for a, q in zip(ab, sg)]
        m = sorted(v)[2]
        cm += m >= obs_med - 1e-12; c2 += abs(m) >= obs_med - 1e-12
        cs += sum(v) >= obs_sum - 1e-12
    return cm, cs, c2


cm, cs, c2 = counts(wk)
num(3, 'p-five-weeks-flip', 1, sorted(wk)[2], float(np.median(wk)), {'mean': sum(wk) / 5, 'trimmed': float(stats.trim_mean(wk, 0.2))}, dp=3)
num(3, 'p-five-weeks-flip', 2, cm, 2 ** 2, {'mean-count': cs, 'two-sided': c2})
num(3, 'p-five-weeks-flip', 3, cm / 32, 4 / 32, {'plus-one': 5 / 33, 'two-sided': c2 / 32}, dp=4)
ok(cs == 2 and abs(cs / 32 - 0.0625) < 1e-12, 'five-weeks: the mean counts 2 patterns')
w4 = item(3, 'p-five-weeks-flip')['parts'][3]['widget']
ok([o['id'] for o in w4['options'] if o.get('correct')] == ['robust'], 'five-weeks p4: keyed option')
shown('five total', 13.1, sum(wk), 1)
# claim in p4: the mean counts fewer patterns because of the size of the 9.0 week
cm_b, cs_b, _ = counts([1.2, 0.8, 2.5, -0.4, 2.6])
if (cm_b, cs_b) == (cm, cs) and '9.0 week' in json.dumps(w4, ensure_ascii=False):
    claim(f'problems-3 p-five-weeks-flip p4: the keyed reason is the size of the 9.0 week; with 2.6 in its place the counts are '
          f'still {cs_b} (mean) and {cm_b} (median), so the size of that week explains nothing (review finding 15)')
means4 = sorted(((1.2 + 2.5 + 9.0 + a * 0.8 + b * 0.4) / 5 for a in (1, -1) for b in (1, -1)), reverse=True)
ok([round(m, 2) for m in means4] == [2.78, 2.62, 2.46, 2.30], 'five-weeks: the four means in the proposed fix')

# numbers used in the review's replacement lines
ok(abs(math.sqrt(1.866667) - 1.3663) < 1e-4, 'fix: sqrt 1.8667')
ok(abs(0.2628 * 2.2 - 0.5781) < 1e-4 and abs(math.sqrt(2.2) - 1.4832) < 1e-4, 'fix: 0.5781, 1.4832')
ok(abs(2.6 - 1.3 * 0.5 - 1.95) < 1e-12, 'fix: predictor at 0.5')
ok(abs(stats.t.ppf(.975, 8) - 2.306) < 1e-3 and abs(lo_t - 0.950) < 1e-3, 'fix: t_8 end 0.950')
ok(abs(2 * 225 * 1.6 - 720) < 1e-9 and abs(.6 * 225 - 135) < 1e-9, 'fix: 720, 135')
ss = ((d - d.mean()) ** 2).sum()
ok((7.5 - d.mean()) ** 2 / ss > 0.7, 'fix: the 7.5 supplies most of the SD')
ok(max(np.diff(np.sort(d)[:6])) < hw, 'fix: h from the SD exceeds every gap between ordinary trades')
ok(abs(1 / 1.4826 - 0.6745) < 1e-4, 'fix: MAD is about two thirds of an SD')
ok(abs(1 / 30 + 1 / 28 - 58 / 840) < 1e-15, 'fix: 1/30 + 1/28')

for f in findings:
    print('FINDING', f)
print(f'{checks} checks, {len(findings)} FINDING lines')
sys.exit(0)
