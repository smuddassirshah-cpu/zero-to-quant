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
sf4 = item(1, 'p-settlement-fails')['parts'][3]
if lo_t < 1 < lo_q and not ('1.96' in sf4['question'] and '0.950' in sf4['explain']['text'] and 'in doubt' in sf4['explain']['text']):
    claim(f'problems-1 p-settlement-fails p4: interval end {lo_q:.3f} uses 1.96 with a dispersion on 8 df; '
          f't_8 = {stats.t.ppf(.975, 8):.3f} gives {lo_t:.3f}, below 1, and the part does not say so (review finding 2)')
ok('run above the domestic rate' not in sf4['explain']['text'], 'settlement p4: the unsafe conclusion is gone')

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

# --- p-auction-tails: re-authored in the fix pass as p-rfq-busy-minutes; its checks are removed here
# (the delta reader checks the new problem). brentq is still used below.
from scipy.optimize import brentq

# ================================================================ problems-2
# p-venue-markouts and p-rerun-the-test were re-authored in the fix pass (p-signal-variants, p-two-looks);
# their checks are removed here. The seeded generator is kept for the twin-books rows.
rng = np.random.default_rng(7)

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
shown('twin one tail', 0.0130, float(pt) / 2, 4); has(2, 'p-twin-books', 'P(t_{119} > 2.2530) = 0.0130')
ok(abs(2 * 0.0130 - float(pt)) <= 1e-4, 'twin p4: doubling the stated tail is accepted')
ok(abs(stats.norm.sf(za - 2.4005 / 1.22474) - 0.5) < 1e-3, 'twin-books: the no-power gain has power one half')


# ================================================================ problems-3
# p-ten-trading-days and p-block-markout-tail were re-authored in the fix pass (p-hedge-ranks, p-spread-day-tail);
# their checks are removed here, the claim of finding 14 with them.

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
if (cm_b, cs_b) == (cm, cs) and 'tells those four apart' not in w4['options'][0]['text']:
    claim(f'problems-3 p-five-weeks-flip p4: the keyed reason is the size of the 9.0 week; with 2.6 in its place the counts are '
          f'still {cs_b} (mean) and {cm_b} (median), so the size of that week explains nothing (review finding 15)')
means4 = sorted(((1.2 + 2.5 + 9.0 + a * 0.8 + b * 0.4) / 5 for a in (1, -1) for b in (1, -1)), reverse=True)
ok([round(m, 2) for m in means4] == [2.78, 2.62, 2.46, 2.30], 'five-weeks: the four means in the proposed fix')
has(3, 'p-five-weeks-flip', '2.78, 2.62, 2.46 and 2.30')

# numbers used in the review's replacement lines
ok(abs(math.sqrt(1.866667) - 1.3663) < 1e-4, 'fix: sqrt 1.8667')
ok(round(0.2628 * 2.2, 4) == 0.5782 and round(math.sqrt(2.2), 4) == 1.4832, 'fix: 0.5782 (the review printed 0.5781), 1.4832')
has(1, 'p-settlement-fails', '0.5782')
ok(abs(stats.t.ppf(.975, 8) - 2.306) < 1e-3 and abs(lo_t - 0.950) < 1e-3, 'fix: t_8 end 0.950')
ok(abs(2 * 225 * 1.6 - 720) < 1e-9 and abs(.6 * 225 - 135) < 1e-9, 'fix: 720, 135')
ok(abs(1 / 30 + 1 / 28 - 58 / 840) < 1e-15, 'fix: 1/30 + 1/28')

for f in findings:
    print('FINDING', f)
print(f'{checks} checks, {len(findings)} FINDING lines')
sys.exit(0)
