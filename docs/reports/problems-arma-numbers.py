"""Recompute every number in app/content/courses/arma/problems-<n>.json twice.

Method 1 is closed form (fractions.Fraction or the course's formulas by hand).
Method 2 takes a different route: seeded simulation (AR, MA, ARMA paths and their sample moments),
brute-force search for horizons, statsmodels' theoretical ACF and PACF (ArmaProcess), SciPy's normal
and chi-square tails, and NumPy least squares. For each numeric part: both methods agree; the key is
within its band; each `wrong` value matches its named slip and lies outside the key's band; the
question states its form. Choice parts: the keyed option. numbers_lib then checks stated numbers.
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-arma-numbers.py
"""
import json, os, re, sys
from fractions import Fraction as F
from math import isclose, sqrt, log, ceil
import numpy as np
from scipy import stats
from statsmodels.tsa.arima_process import ArmaProcess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'arma')
FORM = re.compile(r'decimal places?|decimal to|whole number|percentage|fraction', re.I)
fails, checks = [], 0
rng = np.random.default_rng(20261116)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('FINDING', msg)


def load(n):
    d = json.load(open(os.path.join(COURSE, f'problems-{n}.json')))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'arma', f'set {n}: header')
    ok(3 <= len(d['items']) <= 5, f'set {n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'set {n}: no difficulty 5')
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for it in d['items'] for p in it['parts'])
    total = sum(len(it['parts']) for it in d['items'])
    ok(3 * typed >= 2 * total, f'set {n}: typed {typed} of {total}')
    for it in d['items']:
        ok(3 <= len(it['parts']) <= 5 and 3 <= it['difficulty'] <= 5, f'{it["id"]}: parts or difficulty')
    return {it['id']: it for it in d['items']}


def within(v, a, t):
    return abs(v - a) <= t + 1e-12


def num(items, iid, k, exact, alt, slips=None, rel=1e-6):
    p = items[iid]['parts'][k - 1]
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=rel, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(within(e, w['answer'], tol), f'{tag}: key {w["answer"]} vs computed {e}')
    ok(bool(FORM.search(p['question'])), f'{tag}: no form stated')
    slips = slips or {}
    wr = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wr) == set(slips), f'{tag}: wrong ids {sorted(wr)} vs {sorted(slips)}')
    ok(set(wr) == set(p['feedback'].get('byKey', {})), f'{tag}: byKey ids')
    for wid, val in slips.items():
        if wid not in wr:
            continue
        x = wr[wid]
        ok(within(float(val), x['value'], x['tol']['abs']), f'{tag}: wrong {wid} {x["value"]} vs slip {val}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag}: wrong {wid} overlaps key band')
    ids = list(wr)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = wr[ids[i]], wr[ids[j]]
            ok(abs(a['value'] - b['value']) > a['tol']['abs'] + b['tol']['abs'], f'{tag}: wrongs {ids[i]} {ids[j]} overlap')


def pick(items, iid, k, oid):
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [oid], f'{iid} p{k}: keyed {keyed}, expected {oid}')


def sim_ar1(phi, sigma, n, sims, burn=300):
    e = rng.standard_normal((sims, n + burn)) * sigma
    x = np.zeros_like(e)
    for t in range(1, n + burn):
        x[:, t] = phi * x[:, t - 1] + e[:, t]
    return x[:, burn:]


def lb(n, r):
    return n * (n + 2) * sum(F(rk) ** 2 / (n - k) for k, rk in enumerate(r, 1))


def first_h(f, start=1):
    h = start
    while not f(h):
        h += 1
    return h


Phi = stats.norm.cdf

# ------------------------------------------------------------------ level 1
I = load(1)
g = F('-287.5') / 1250
ols = np.polyfit(np.array([0., 1.]), np.array([0., float(g)]), 1)[0]          # slope of a line with that rise
num(I, 'p-airport-anomaly', 1, g, ols, {'flip': F(1250) / F('-287.5'), 'sign': -g})
t = float(g) / sqrt(3.2 / 1250)
# method 2: simulate data with S_xx = 1250 and S_xy = -287.5 exactly, fit by least squares, read t
xx = rng.standard_normal(364); xx = (xx - xx.mean()) / sqrt(((xx - xx.mean()) ** 2).sum()) * sqrt(1250)
res = rng.standard_normal(364); res -= res.mean(); res -= xx * (res @ xx) / (xx @ xx)
res *= sqrt(3.2 * 362 / (res @ res))
y = float(g) * xx + res
X = np.column_stack([np.ones(364), xx]); b, ssr = np.linalg.lstsq(X, y, rcond=None)[:2]
t2 = b[1] / sqrt(ssr[0] / 362 / (xx @ xx))
num(I, 'p-airport-anomaly', 2, t, t2, {'no-sqrt': float(g) / (3.2 / 1250), 's-not-s2': float(g) / sqrt(sqrt(3.2) / 1250), 'sign': -t})
pick(I, 'p-airport-anomaly', 3, 'reject-df')
ok(t < -3.45, 'anomaly t below the 1% Dickey-Fuller point')
phi = 1 + float(g)
var = 3.2 / (1 - phi ** 2)
xs = sim_ar1(phi, sqrt(3.2), 4000, 50)
num(I, 'p-airport-anomaly', 4, var, var, {'shock': 3.2, 'no-square': 3.2 / (1 - phi)})
ok(abs(xs.var() / var - 1) < 0.02, f'anomaly variance by simulation {xs.var():.3f} vs {var:.3f}')
tail = 1 - Phi(5 / sqrt(var))
num(I, 'p-airport-anomaly', 5, tail, stats.norm.sf(5, scale=sqrt(var)),
    {'shock-sd': stats.norm.sf(5, scale=sqrt(3.2)), 'no-square': stats.norm.sf(5, scale=sqrt(3.2 / 0.23))})
ok(abs((xs > 5).mean() - tail) < 0.004, f'tail by simulation {(xs > 5).mean():.4f}')
ok(round(tail * 365) == 14 and round(stats.norm.sf(5, scale=sqrt(3.2)) * 365) == 1, 'days a year 14 and 1')
ok(abs(sqrt(var) - 2.80) < 0.005 and abs(sqrt(3.2) - 1.79) < 0.005 and abs(5 / 2.804 - 1.78) < 0.005, 'sds 2.80, 1.79, 1.78')

# p-ppp-screen: Bayes counts with stated rates (method 2: Monte Carlo of the 48-series screen)
fa = F(36) * F('0.05')
mc = (rng.random((200000, 36)) < 0.05).sum(1).mean()
num(I, 'p-ppp-screen', 1, fa, fa, {'power': 36 * 0.2, 'normal': 36 * 0.45})
ok(abs(mc - 1.8) < 0.02, 'false alarms by Monte Carlo')
sh = F(12) * F('0.2') / (F(12) * F('0.2') + fa)
W = rng.random((400000, 36)) < 0.05; S = rng.random((400000, 12)) < 0.2
num(I, 'p-ppp-screen', 2, sh, S.sum() / (S.sum() + W.sum()), {'power-only': 0.2, 'false-share': 1 - sh}, rel=0.01)
shn = F(12) * F('0.89') / (F(12) * F('0.89') + F(36) * F('0.45'))
num(I, 'p-ppp-screen', 3, shn, 10.68 / 26.88, {'power-only': 0.89, 'false-share': 1 - shn})
nr = F(12) * F('0.8') / (F(12) * F('0.8') + F(36) * F('0.95'))
num(I, 'p-ppp-screen', 4, nr, (~S).sum() / ((~S).sum() + (~W).sum()), {'miss-rate': 0.8, 'prior': 0.25}, rel=0.01)
pick(I, 'p-ppp-screen', 5, 'over')
# the stated simulation rates: DF t with a constant on 360 months
def df_t(Xp):
    dx = np.diff(Xp, axis=1); xl = Xp[:, :-1]; m = dx.shape[1]
    xm = xl.mean(1, keepdims=True); ym = dx.mean(1, keepdims=True)
    sxx = ((xl - xm) ** 2).sum(1); bb = ((xl - xm) * (dx - ym)).sum(1) / sxx
    aa = ym[:, 0] - bb * xm[:, 0]; r = dx - aa[:, None] - bb[:, None] * xl
    return bb / np.sqrt((r ** 2).sum(1) / (m - 2) / sxx)
tw = df_t(np.cumsum(rng.standard_normal((6000, 360)), 1)); ta = df_t(sim_ar1(0.98, 1, 360, 6000))
for lab, v, target in [('walk DF', (tw < -2.87).mean(), 0.05), ('AR DF', (ta < -2.87).mean(), 0.20),
                       ('walk normal', (tw < -1.645).mean(), 0.45), ('AR normal', (ta < -1.645).mean(), 0.89)]:
    ok(abs(v - target) < 0.02, f'stated rate {lab}: simulated {v:.3f} vs {target}')

# p-gdp-trend
num(I, 'p-gdp-trend', 1, sqrt(2) * 0.035, np.std(np.diff(rng.standard_normal(10 ** 6) * 0.035)), {'same': 0.035, 'double': 0.07}, rel=0.005)
pick(I, 'p-gdp-trend', 2, 'a-fails')
num(I, 'p-gdp-trend', 3, 0.009 * sqrt(12), sqrt(12 * 0.009 ** 2), {'linear': 0.108})
ok(abs(12 * 0.9 ** 2 - 9.72) < 1e-9 and abs(sqrt(9.72) - 3.12) < 0.005, 'gdp 9.72 and 3.12')
h = first_h(lambda h: 0.009 * sqrt(h) > 0.035)
num(I, 'p-gdp-trend', 4, h, ceil((3.5 / 0.9) ** 2), {'round-down': 15, 'no-square': round(3.5 / 0.9)})
ok(abs(0.9 * sqrt(15) - 3.49) < 0.005 and abs(0.9 * sqrt(16) - 3.60) < 0.005 and abs((3.5 / .9) ** 2 - 15.1) < 0.05, 'gdp 3.49, 3.60, 15.1')

# p-gold-drift
m = log(1820 / 1450) / 500 * 1e4
r = np.diff(np.log(np.r_[1450, 1450 * np.exp(np.cumsum(np.full(500, log(1820 / 1450) / 500)))]))
num(I, 'p-gold-drift', 1, m, r.mean() * 1e4, {'simple': (1820 / 1450 - 1) / 500 * 1e4})
se = 110 / sqrt(500)
num(I, 'p-gold-drift', 2, m / se, 4.55 / se, {'no-sqrt': m / (110 / 500), 'sd': m / 110}, rel=0.002)
pick(I, 'p-gold-drift', 3, 'unclear')
n_need = first_h(lambda n: 4.55 * sqrt(n) / 110 >= 2)
num(I, 'p-gold-drift', 4, n_need, ceil((2 * 110 / 4.55) ** 2), {'no-square': 2 * 110 / 4.55, 't-one': ceil((110 / 4.55) ** 2)})
ok(within(ceil((2 * 110 / m) ** 2), 2338, 5), 'exact-drift day count also in the band')
ok(abs(1.1 * sqrt(500) - 24.6) < 0.05 and abs(log(1820 / 1450) - 0.2273) < 5e-5 and abs(n_need / 252 - 9.3) < 0.1, 'gold 24.6, 0.2273, nine years')

# ------------------------------------------------------------------ level 2
I = load(2)
num(I, 'p-etf-flows', 1, F(81000, 180000), 0.45, {'flip': F(180000, 81000)})
q2 = lb(200, ['0.45', '0.24'])
from statsmodels.stats.diagnostic import acorr_ljungbox  # noqa: E402
num(I, 'p-etf-flows', 2, q2, 200 * 202 * (0.45 ** 2 / 199 + 0.24 ** 2 / 198),
    {'box-pierce': 200 * (0.45 ** 2 + 0.24 ** 2), 'no-n-k': 40400 * (0.45 ** 2 + 0.24 ** 2)})
ok(float(q2) > stats.chi2.ppf(0.95, 2), 'Q(2) beats 5.99')
num(I, 'p-etf-flows', 3, F('0.45') ** 2, ArmaProcess([1, -0.45], [1]).acf(3)[2], {'double': 0.9, 'sample': 0.24})
s = sqrt(900 * (1 - 0.45 ** 2))
xs = sim_ar1(0.45, s, 4000, 50)
num(I, 'p-etf-flows', 4, s, s, {'no-square': sqrt(900 * 0.55), 'series-sd': 30, 'variance': 717.75})
ok(abs(xs.var() / 900 - 1) < 0.02, 'flow variance 900 by simulation')
ok(abs(1.96 / sqrt(200) - 0.139) < 5e-4 and abs(1 - s / 30 - 0.11) < 0.005, 'etf band 0.139, 11%')

NV = 680
num(I, 'p-vol-index-order', 1, 1.96 / sqrt(NV), stats.norm.ppf(0.975) / sqrt(NV), {'sd': 1 / sqrt(NV), 'over-n': 1.96 / NV}, rel=1e-4)
pick(I, 'p-vol-index-order', 2, 'two')
pac = [-0.21, -0.13, 0.05, -0.03, 0.04, -0.092]
ok([k + 1 for k, v in enumerate(pac) if abs(v) > 1.96 / sqrt(NV)] == [1, 2, 6], 'PACF lags outside: 1, 2, 6')
ok(0.06 < 1.96 / sqrt(NV), 'lags 7 to 20 within 0.06 lie inside the band')
from math import comb  # noqa: E402
ex1 = comb(18, 1) * F(5, 100) * F(95, 100) ** 17
mc1 = ((rng.random((400000, 18)) < 0.05).sum(1) == 1).mean()
num(I, 'p-vol-index-order', 3, ex1, stats.binom.pmf(1, 18, 0.05),
    {'at-least': 1 - 0.95 ** 18, 'none': 0.95 ** 18, 'no-count': 0.05 * 0.95 ** 17})
ok(abs(mc1 - float(ex1)) < 0.004, f'exactly one stray by Monte Carlo {mc1:.4f}')
ok(abs(0.05 * 0.95 ** 17 - 0.0209) < 5e-5 and abs(0.95 ** 18 - 0.397) < 5e-4 and abs(1 / sqrt(NV) - 0.038) < 5e-4, 'vol 0.0209, 0.397, 0.038')
bic = lambda k, l: k * log(NV) - 2 * l
num(I, 'p-vol-index-order', 4, bic(8, -807.9) - bic(4, -812.4), 4 * log(NV) - 9,
    {'aic': (16 + 2 * 807.9) - (8 + 2 * 812.4), 'no-fit': 4 * log(NV), 'sign': bic(4, -812.4) - bic(8, -807.9)})
ok(abs(4 * log(NV) - 26.09) < 0.005 and abs(log(NV) - 6.52) < 0.005, 'vol 26.09, 6.52')

g0 = 4 / (1 - 0.88 ** 2)
xs = sim_ar1(0.88, 2, 6000, 60)
num(I, 'p-peg-fridays', 1, g0, F(4) / (1 - F('0.88') ** 2), {'no-square': 4 / 0.12, 'sd-top': 2 / 0.2256})
ok(abs(xs.var() / g0 - 1) < 0.02, 'peg variance by simulation')
pw = 0.88 ** 5
w = xs[:, ::5]
num(I, 'p-peg-fridays', 2, pw, ArmaProcess([1, -0.88], [1]).acf(6)[5], {'linear': 0.4, 'daily': 0.88})
ok(abs(np.mean(w[:, 1:] * w[:, :-1]) / np.mean(w * w) - pw) < 0.01, 'Friday autocorrelation by simulation')
s2w = g0 * (1 - pw ** 2)
num(I, 'p-peg-fridays', 3, s2w, 4 * (1 - 0.88 ** 10) / (1 - 0.88 ** 2), {'daily': 4, 'five': 20, 'no-square': g0 * (1 - pw)})
band = 1.96 / sqrt(104)
kmax = max(k for k in range(1, 20) if pw ** k > band)
num(I, 'p-peg-fridays', 4, kmax, int(log(band) / log(pw)), {'sd-band': max(k for k in range(1, 20) if pw ** k > 1 / sqrt(104)), 'one': 1})
ok(abs(sqrt(g0) - 4.21) < 0.005 and abs(band - 0.192) < 5e-4 and abs(0.5277 ** 2 - 0.278) < 5e-4 and abs(pw ** 3 - 0.147) < 5e-4
   and abs(1 - pw ** 2 - 0.7215) < 5e-5, 'peg 4.21, 0.192, 0.278, 0.147, 0.7215')

rr = ['0.02', '0.145', '-0.04', '0.05', '0.03']
q5 = lb(400, rr)
num(I, 'p-freight-ar2', 1, q5, 400 * 402 * sum(float(v) ** 2 / (400 - k) for k, v in enumerate(rr, 1)),
    {'box-pierce': 400 * sum(float(v) ** 2 for v in rr), 'no-n-k': 160800 * sum(float(v) ** 2 for v in rr)})
ok(stats.chi2.ppf(0.95, 4) < float(q5) < stats.chi2.ppf(0.95, 5), 'Q(5) between the chi2_4 and chi2_5 points')
ok(abs(stats.chi2.ppf(0.95, 4) - 9.49) < 0.005 and abs(stats.chi2.ppf(0.95, 5) - 11.07) < 0.005, '9.49 and 11.07')
pick(I, 'p-freight-ar2', 2, 'reject')
b2 = (F('0.33') - F('0.42') ** 2) / (1 - F('0.42') ** 2)
sol = np.linalg.solve([[1, 0.42], [0.42, 1]], [0.42, 0.33])
num(I, 'p-freight-ar2', 3, b2, sol[1], {'acf': 0.33, 'no-divide': 0.1536})
num(I, 'p-freight-ar2', 4, 0.42 * (1 - 0.186), 0.42 - 0.42 * 0.186, {'ar1': 0.42, 'plus': 0.42 * 1.186})
ok(within(sol[0], 0.42 * (1 - 0.186), 0.0006), 'exact b1 also in the band')
ok(abs(0.145 ** 2 / 398 - 0.0000528) < 5e-8 and abs(sum(float(v) ** 2 / (400 - k) for k, v in enumerate(rr, 1)) - 0.0000665) < 5e-8
   and float(b2) > 1.96 / sqrt(400), 'freight 0.0000528, 0.0000665, b2 outside the band')

# ------------------------------------------------------------------ level 3
I = load(3)
e = rng.standard_normal((2000, 241)) * 0.04
ro = 0.6 * e[:, 1:] + 0.4 * e[:, :-1]
num(I, 'p-smoothed-fund', 1, 0.04 * sqrt(0.52), ro.std(), {'add-sds': 0.04, 'no-sqrt': 0.0208}, rel=0.01)
th = F(2, 3)
num(I, 'p-smoothed-fund', 2, F(24, 52), th / (1 + th ** 2), {'ratio': th, 'cov': 0.24})
ok(abs(np.mean(ro[:, 1:] * ro[:, :-1]) / np.mean(ro * ro) - 24 / 52) < 0.01, 'reported lag-1 autocorrelation by simulation')
num(I, 'p-smoothed-fund', 3, 1.96 * 0.6 * 0.04, stats.norm.ppf(0.975) * 0.024, {'uncond': 1.96 * 0.04 * sqrt(0.52), 'full': 0.0784}, rel=1e-4)
s12 = 0.04 * sqrt(12 * 0.52 + 22 * 0.24)
sums = np.add.reduceat(ro, np.arange(0, 240, 12), axis=1)
num(I, 'p-smoothed-fund', 4, s12, sums.std(), {'root-12': 0.04 * sqrt(0.52) * sqrt(12), 'true': 0.04 * sqrt(12), 'once': 0.04 * sqrt(12 * 0.52 + 11 * 0.24)}, rel=0.01)
ok(abs(1 - 0.04 * sqrt(0.52) / 0.04 - 0.28) < 0.005 and abs(1 - 0.04 * sqrt(6.24) / s12 - 0.26) < 0.005
   and abs(1.96 * 0.04 * sqrt(0.52) - 0.0565) < 5e-5, 'fund 28%, 26%, 5.65%')

mu, ph, th = 0.25, 0.82, -0.35
eps = 0.55 - 0.43
num(I, 'p-inflation-arma', 1, F('0.55') - F('0.43'), eps, {'gap': 0.30, 'sign': -0.12})
f1 = mu + ph * (0.55 - mu) + th * eps
# method 2: recursion of the ARMA on a path whose last value and shock are fixed, future shocks 0
x = [0.55]; e_last = eps
f1b = mu + ph * (x[-1] - mu) + th * e_last
num(I, 'p-inflation-arma', 2, F('0.25') + F('0.82') * F('0.30') + F('-0.35') * F('0.12'), f1b, {'no-ma': mu + ph * 0.3, 'theta-sign': mu + ph * 0.3 + 0.35 * 0.12})
f2 = mu + ph * (f1 - mu)
num(I, 'p-inflation-arma', 3, f2, mu + ph * (f1b - mu) + th * 0, {'ma-again': f2 - 0.042, 'from-xn': mu + ph ** 2 * 0.3})
hh = first_h(lambda h: abs(0.204 * ph ** (h - 1)) < 0.05)
num(I, 'p-inflation-arma', 4, hh, 1 + ceil(log(0.05 / 0.204) / log(ph)), {'no-ma': first_h(lambda h: 0.3 * ph ** h < 0.05), 'off-by-one': hh - 1})
ok(abs(0.204 * ph ** 7 - 0.0509) < 5e-5 and abs(0.204 * ph ** 8 - 0.0417) < 5e-5 and abs(log(0.05 / 0.204) / log(ph) - 7.09) < 0.005
   and abs(ph * 0.204 - 0.1673) < 5e-5, 'inflation 0.0509, 0.0417, 7.09, 0.1673')

phi = 0.915
hl = log(0.5) / log(phi)
num(I, 'p-inventory-half-life', 1, hl, -log(2) / log(phi), {'linear': 0.5 / 0.085, 'approx': log(2) / 0.085, 'flip': log(phi) / log(0.5)})
e15 = 30 * phi ** 15
num(I, 'p-inventory-half-life', 2, e15, 30 * 0.5 ** (15 / 7.80), {'half': 15, 'linear': 30 * (1 - 15 * 0.085)}, rel=0.002)
sm = sim_ar1(phi, 2.4, 1, 1)  # unused seed advance
paths = np.zeros((200000,)); paths[:] = 30
for _ in range(15):
    paths = phi * paths + rng.standard_normal(200000) * 2.4
hw = 1.96 * 2.4 * sqrt((1 - phi ** 30) / (1 - phi ** 2))
num(I, 'p-inventory-half-life', 3, hw, 1.96 * 2.4 * sqrt(sum(phi ** (2 * j) for j in range(15))),
    {'walk': 1.96 * 2.4 * sqrt(15), 'one-step': 1.96 * 2.4, 'limit': 1.96 * 2.4 / sqrt(1 - phi ** 2)})
ok(abs(paths.mean() - e15) < 0.05 and abs(1.96 * paths.std() - hw) < 0.05, 'inventory mean and half-width by simulation')
hb = first_h(lambda h: 30 * phi ** h < 5)
num(I, 'p-inventory-half-life', 4, hb, ceil(log(5 / 30) / log(phi)), {'round-down': hb - 1, 'linear': ceil(25 / (30 * 0.085))})
ok(abs(30 * phi ** 20 - 5.08) < 0.005 and abs(30 * phi ** 21 - 4.64) < 0.005 and abs(2.585 * 7.80 - 20.16) < 0.005
   and abs(log(phi) + 0.08883) < 5e-6 and abs(15 / 7.80 - 1.92) < 0.005, 'inventory 5.08, 4.64, 20.16, 0.08883, 1.92')

bicd = (3 * log(750) + 2920.4) - (4 * log(750) + 2899.4)
num(I, 'p-dual-listing', 1, bicd, 21 - log(750), {'aic': (6 + 2920.4) - (8 + 2899.4), 'sign': -bicd})
ir = ArmaProcess([1, -0.88], [1, 0.25]).arma2ma(8)
num(I, 'p-dual-listing', 2, F('0.88') + F('0.25'), ir[1], {'ar': 0.88, 'ma': 0.25, 'product': 0.22})
num(I, 'p-dual-listing', 3, 1.13 * 0.88 ** 4, ir[5], {'ar': 0.88 ** 5, 'off-by-one': 1.13 * 0.88 ** 5})
h4 = 1 + log(0.5 / 1.13) / log(0.88)
# method 2: bisection on the continuous path
lo, hi = 1.0, 30.0
for _ in range(80):
    md = (lo + hi) / 2
    lo, hi = (md, hi) if 1.13 * 0.88 ** (md - 1) > 0.5 else (lo, md)
num(I, 'p-dual-listing', 4, h4, lo, {'ar': log(0.5) / log(0.88), 'half-peak': 1 + log(0.5) / log(0.88)})
pick(I, 'p-dual-listing', 5, 'start')
ok(abs(log(750) - 6.62) < 0.005 and abs(0.88 ** 4 - 0.5997) < 5e-5 and abs(0.5 / 1.13 - 0.4425) < 5e-5
   and abs(log(0.5) / log(0.88) - 5.42) < 0.005 and 1.5 < h4 - log(0.5) / log(0.88) < 2.5, 'dual 6.62, 0.5997, 0.4425, 5.42, two days')

# ------------------------------------------------------------------ numbers_lib: stated numbers and wrong bands
for n in (1, 2, 3):
    lv = Level('arma', n)
    lv.check_wrongs('problems')
    if n == 1:
        lv.expect('problems', 'items[0].parts[4].feedback.correct', round(tail, 3))
        lv.expect('problems', 'items[3].parts[3].explain.text', 2338)
    if n == 2:
        lv.expect('problems', 'items[0].parts[1].feedback.correct', round(float(q2), 2))
        lv.expect('problems', 'items[2].parts[2].feedback.correct', round(s2w, 2))
        lv.expect('problems', 'items[3].parts[0].feedback.correct', round(float(q5), 2))
    if n == 3:
        lv.expect('problems', 'items[1].parts[2].feedback.correct', round(f2, 4))
        lv.expect('problems', 'items[2].parts[2].feedback.correct', round(hw, 2))
        lv.expect('problems', 'items[3].parts[3].feedback.correct', round(h4, 2))
    try:
        lv.report()
    except SystemExit as ex:
        ok(ex.code in (0, None), f'numbers_lib level {n} failed')

print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
