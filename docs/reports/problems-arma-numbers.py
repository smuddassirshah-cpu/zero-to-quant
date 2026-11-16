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
SXX, SXY = 2880, F('-662.4')   # fix pass: sums of one sample (2,880/364 = 7.91, near the part-4 variance 7.86)
g = SXY / SXX
ols = np.polyfit(np.array([0., 1.]), np.array([0., float(g)]), 1)[0]          # slope of a line with that rise
num(I, 'p-airport-anomaly', 1, g, ols, {'flip': F(SXX) / SXY, 'sign': -g})
t = float(g) / sqrt(3.2 / SXX)
ok(F(32, 10) / SXX == F(1, 900) and abs(t + 6.90) < 0.005, 'airport se 1/30 and t = -6.90')
ok(abs(SXX / 364 - 7.91) < 0.005 and abs(-0.23 * sqrt(364) / sqrt(1 - 0.77 ** 2) + 6.88) < 0.005, 'airport 7.91 and t by the AR(1) se, -6.88')
# method 2: simulate data with S_xx = 2880 and S_xy = -662.4 exactly, fit by least squares, read t
xx = rng.standard_normal(364); xx = (xx - xx.mean()) / sqrt(((xx - xx.mean()) ** 2).sum()) * sqrt(SXX)
res = rng.standard_normal(364); res -= res.mean(); res -= xx * (res @ xx) / (xx @ xx)
res *= sqrt(3.2 * 362 / (res @ res))
y = float(g) * xx + res
X = np.column_stack([np.ones(364), xx]); b, ssr = np.linalg.lstsq(X, y, rcond=None)[:2]
t2 = b[1] / sqrt(ssr[0] / 362 / (xx @ xx))
num(I, 'p-airport-anomaly', 2, t, t2, {'no-sqrt': float(g) / (3.2 / SXX), 's-not-s2': float(g) / sqrt(sqrt(3.2) / SXX), 'sign': -t})
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
ok(abs(sqrt(var) - 2.80) < 0.005 and abs(sqrt(3.2) - 1.79) < 0.005 and abs(5 / 2.804 - 1.783) < 0.0005, 'sds 2.80, 1.79, 1.783')
w5 = I['p-airport-anomaly']['parts'][4]['widget']
ok(all(within(v, w5['answer'], w5['tol']['abs']) for v in (0.037, 0.038, round(stats.norm.sf(1.78), 3))), 'airport tail band takes 0.037 and 0.038')
sk = next(x for x in w5['wrong'] if x['id'] == 'shock-sd')
ok(within(round(sk['value'], 3), sk['value'], sk['tol']['abs']), 'shock-sd slip typed to 3 places reaches its line')

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
num(I, 'p-etf-flows', 1, F(79200, 180000), 0.44, {'flip': F(180000, 79200)})
q2 = lb(200, ['0.44', '0.24'])
num(I, 'p-etf-flows', 2, q2, 200 * 202 * (0.44 ** 2 / 199 + 0.24 ** 2 / 198),
    {'box-pierce': 200 * (0.44 ** 2 + 0.24 ** 2), 'no-n-k': 40400 * (0.44 ** 2 + 0.24 ** 2)})
ok(float(q2) > stats.chi2.ppf(0.95, 2), 'Q(2) beats 5.99')
num(I, 'p-etf-flows', 3, F('0.44') ** 2, ArmaProcess([1, -0.44], [1]).acf(3)[2], {'double': 0.88, 'sample': 0.24})
s = sqrt(900 * (1 - 0.44 ** 2))
xs = sim_ar1(0.44, s, 4000, 50)
num(I, 'p-etf-flows', 4, s, sqrt(900 / sum(0.44 ** (2 * j) for j in range(400))), {'no-square': sqrt(900 * 0.56), 'series-sd': 30, 'variance': 725.76})
ok(abs(xs.var() / 900 - 1) < 0.02, 'flow variance 900 by simulation')
ok(abs(1.96 / sqrt(200) - 0.139) < 5e-4 and abs(1 - s / 30 - 0.10) < 0.005 and abs(0.24 - 0.1936 - 0.05) < 0.005, 'etf band 0.139, 10%, 0.05 away')

# p-trust-discount (re-authored): PACF from the regression rows, AR(2) mean, one-step forecasts
band = 1.96 / sqrt(520)
newest = [0.80, 0.24, 0.05, -0.08]
ok(abs(band - 0.086) < 5e-4 and [k + 1 for k, v in enumerate(newest) if abs(v) > band] == [1, 2] and 0.10 > band, 'trust band 0.086; PACF clears at 1 and 2; the row-4 b3 0.10 would clear')
pick(I, 'p-trust-discount', 1, 'two')
mu_t = F('1.38') / (1 - F('0.61') - F('0.24'))
# method 2: iterate the fitted equation with no shocks until it settles
xm = 0.0
for _ in range(400):
    xm = 1.38 + 0.61 * xm + 0.24 * xm
num(I, 'p-trust-discount', 2, mu_t, xm, {'one-lag': 1.38 / 0.39, 'constant': 1.38})
ok(within(1.84 / (1 - 0.80), 9.2, 1e-9), 'one-lag fit has the same mean 9.2')
ok(abs(0.61 / (1 - 0.24) - 0.80) < 0.005, 'two-lag fit implies rho_1 0.80, the one-lag slope')
f_two = F('1.38') + F('0.61') * 12 + F('0.24') * F('13.5')
num(I, 'p-trust-discount', 3, f_two, 9.2 + 0.61 * 2.8 + 0.24 * 4.3, {'swap': 1.38 + 0.61 * 13.5 + 0.24 * 12, 'no-constant': 0.61 * 12 + 0.24 * 13.5})
f_one = F('1.84') + F('0.80') * 12
num(I, 'p-trust-discount', 4, f_two - f_one, (9.2 + 0.61 * 2.8 + 0.24 * 4.3) - (9.2 + 0.8 * 2.8), {'sign': f_one - f_two, 'narrowing': 12 - f_one})
ok(abs(0.61 * 2.8 - 1.708) < 1e-9 and abs(0.24 * 4.3 - 1.032) < 1e-9 and abs(0.61 * 12 - 7.32) < 1e-9 and abs(0.24 * 13.5 - 3.24) < 1e-9
   and abs(12 - float(f_two) - 0.06) < 1e-9 and 0.85 < 0.50 / 0.56 < 0.95, 'trust 1.708, 1.032, 7.32, 3.24, 0.06, nine tenths')

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

# p-satellite-stocks (re-authored): AR(1) plus white measurement error
v_e = F(36) + F('3.5') ** 2
num(I, 'p-satellite-stocks', 1, v_e, np.var(sim_ar1(0.85, 6 * sqrt(1 - 0.85 ** 2), 4000, 50) + rng.standard_normal((50, 4000)) * 3.5),
    {'add-sds': 9.5 ** 2, 'true-only': 36, 'sd': sqrt(48.25)}, rel=0.02)
r1e = F('0.85') * 36 / v_e
ys = sim_ar1(0.85, 6 * sqrt(1 - 0.85 ** 2), 6000, 60) + rng.standard_normal((60, 6000)) * 3.5
yc = ys - ys.mean(1, keepdims=True)
acf_e = lambda k: (yc[:, k:] * yc[:, :-k]).mean() / (yc * yc).mean()
num(I, 'p-satellite-stocks', 2, r1e, acf_e(1), {'no-error': 0.85, 'error-lag': (30.6 + 12.25) / 48.25, 'sds': 0.85 * 6 / sqrt(48.25)}, rel=0.02)
r4e = F('0.85') ** 4 * 36 / v_e
num(I, 'p-satellite-stocks', 3, r4e, acf_e(4), {'ar1': float(r1e) ** 4, 'true': 0.85 ** 4, 'extra': float(r1e) * 0.85 ** 4}, rel=0.03)
ok(within(0.634 * 0.85 ** 3, float(r4e), 0.0006), 'lag 4 from the rounded 0.634 is in the band')
ph_hat = (0.40 / 0.61) ** (1 / 3)
# method 2: bisection on phi^3 * 0.61 = 0.40
lo, hi = 0.0, 1.0
for _ in range(80):
    md = (lo + hi) / 2
    lo, hi = (md, hi) if 0.61 * md ** 3 < 0.40 else (lo, md)
num(I, 'p-satellite-stocks', 4, ph_hat, lo, {'lag1': 0.61, 'fourth-root': (0.40 / 0.61) ** 0.25, 'ar1': 0.40 ** 0.25})
ok(abs(12.25 / 48.25 - 0.25) < 0.01 and abs(0.85 * 36 - 30.6) < 1e-9 and abs(0.85 ** 4 * 36 - 18.79) < 0.005 and abs(float(r1e) ** 4 - 0.162) < 5e-4
   and abs(0.40 / 0.61 - 0.6557) < 5e-5 and abs(0.40 / 0.61 - 0.656) < 5e-4, 'satellite a quarter, 30.6, 18.79, 0.162, 0.6557, 0.656')
ok(abs(0.61 - float(r1e)) < 2 / sqrt(520) and abs(0.40 - float(r4e)) < 2.5 / sqrt(520), 'sample bars 0.61 and 0.40 plausible on 520 weeks')

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

mu, ph, th = 0.25, 0.82, -0.20
eps = 0.55 - 0.43
num(I, 'p-inflation-arma', 1, F('0.55') - F('0.43'), eps, {'gap': 0.30, 'sign': -0.12})
f1 = mu + ph * (0.55 - mu) + th * eps
# method 2: recursion of the ARMA on a path whose last value and shock are fixed, future shocks 0
x = [0.55]; e_last = eps
f1b = mu + ph * (x[-1] - mu) + th * e_last
num(I, 'p-inflation-arma', 2, F('0.25') + F('0.82') * F('0.30') + F('-0.20') * F('0.12'), f1b, {'no-ma': mu + ph * 0.3, 'theta-sign': mu + ph * 0.3 + 0.20 * 0.12})
f2 = mu + ph * (f1 - mu)
num(I, 'p-inflation-arma', 3, f2, mu + ph * (f1b - mu) + th * 0, {'ma-again': f2 - 0.024, 'from-xn': mu + ph ** 2 * 0.3})
hh = first_h(lambda h: abs(0.222 * ph ** (h - 1)) < 0.05)
num(I, 'p-inflation-arma', 4, hh, 1 + ceil(log(0.05 / 0.222) / log(ph)), {'no-ma': first_h(lambda h: 0.3 * ph ** h < 0.05), 'off-by-one': hh - 1})
ok(abs(f1 - mu - 0.222) < 1e-9 and abs(0.222 * ph ** 7 - 0.0553) < 5e-5 and abs(0.222 * ph ** 8 - 0.0454) < 5e-5 and abs(log(0.05 / 0.222) / log(ph) - 7.51) < 0.005
   and abs(ph * 0.222 - 0.1820) < 5e-5 and abs(0.05 / 0.222 - 0.225) < 5e-4, 'inflation 0.222, 0.0553, 0.0454, 7.51, 0.1820, 0.225')

# p-swap-spread-hold (re-authored): half-life and long-run sd quoted, phi never needed
HL, LR, GAP0, H = 12, 6.0, 9.0, 20
share = 0.5 ** (H / HL)
phi_s = 0.5 ** (1 / HL)
num(I, 'p-swap-spread-hold', 1, GAP0 * share, GAP0 * phi_s ** H, {'linear': GAP0 * (1 - H / (2 * HL)), 'half': GAP0 / 2, 'flip': GAP0 * 0.5 ** (HL / H)})
sig_s = LR * sqrt(1 - phi_s ** 2)
sd20 = LR * sqrt(1 - share ** 2)
sd20b = sig_s * sqrt(sum(phi_s ** (2 * j) for j in range(H)))
num(I, 'p-swap-spread-hold', 2, sd20, sd20b, {'not-squared': LR * sqrt(1 - share), 'no-root': LR * (1 - share ** 2), 'variance': LR ** 2 * (1 - share ** 2)})
ok(within(LR * sqrt(1 - 0.315 ** 2), sd20, 0.006), 'sd from the rounded 0.315 is in the band')
# simulation of the 20-day path from 9 bp
pth = np.full(400000, GAP0)
for _ in range(H):
    pth = phi_s * pth + rng.standard_normal(400000) * sig_s
ok(abs(pth.mean() - GAP0 * share) < 0.03 and abs(pth.std() - sd20) < 0.03, 'swap mean and sd at day 20 by simulation')
pl = stats.norm.sf((GAP0 - GAP0 * share) / sd20)
num(I, 'p-swap-spread-hold', 3, pl, (pth > GAP0).mean(), {'from-mean': stats.norm.sf(GAP0 / sd20), 'long-run': stats.norm.sf((GAP0 - GAP0 * share) / LR), 'win': 1 - pl}, rel=0.02)
w3 = I['p-swap-spread-hold']['parts'][2]['widget']
ok(all(within(v, w3['answer'], w3['tol']['abs']) for v in (0.139, 0.140, round(stats.norm.sf(1.08), 3), round(stats.norm.sf((9 - 2.83) / 5.69), 3))), 'loss band takes 0.139 and 0.140')
pinf = stats.norm.sf(GAP0 / LR)
num(I, 'p-swap-spread-hold', 4, pinf, 1 - Phi(1.5), {'two-sided': 2 * pinf, 'variance': stats.norm.sf(GAP0 / LR ** 2)})
loss = [stats.norm.sf((GAP0 - GAP0 * 0.5 ** (h / HL)) / (LR * sqrt(1 - 0.25 ** (h / HL)))) for h in range(1, 400)]
ok(all(a > b for a, b in zip(loss, loss[1:])) and loss[-1] > pinf and loss[-1] - pinf < 1e-6, 'loss chance falls with the hold, towards 0.067 from above')
ok(abs(share - 0.315) < 5e-4 and abs(H / HL - 1.667) < 5e-4 and abs(36 * (1 - 0.315 ** 2) - 32.43) < 0.005 and abs(1 - 0.315 ** 2 - 0.9008) < 5e-5
   and abs(9 - 2.83 - 6.17) < 1e-9 and abs((9 - 2.83) / 5.69 - 1.08) < 0.005 and abs(pinf - 0.067) < 5e-4 and abs(1 / pl - 7) < 0.5, 'swap 0.315, 1.667, 32.43, 0.9008, 6.17, 1.08, 0.067, one in seven')

bicd = (3 * log(750) + 2920.4) - (4 * log(750) + 2899.4)
num(I, 'p-dual-listing', 1, bicd, 21 - log(750), {'aic': (6 + 2920.4) - (8 + 2899.4), 'sign': -bicd})
ir = ArmaProcess([1, -0.88], [1, 0.25]).arma2ma(8)
num(I, 'p-dual-listing', 2, F('0.88') + F('0.25'), ir[1], {'ar': 0.88, 'ma': 0.25, 'product': 0.22})
num(I, 'p-dual-listing', 3, 1.13 * 0.88 ** 6, ir[7], {'ar': 0.88 ** 7, 'off-by-one': 1.13 * 0.88 ** 7})
h4 = 1 + log(0.5 / 1.13) / log(0.88)
# method 2: bisection on the continuous path
lo, hi = 1.0, 30.0
for _ in range(80):
    md = (lo + hi) / 2
    lo, hi = (md, hi) if 1.13 * 0.88 ** (md - 1) > 0.5 else (lo, md)
num(I, 'p-dual-listing', 4, h4, lo, {'ar': log(0.5) / log(0.88), 'half-peak': 1 + log(0.5) / log(0.88)})
pick(I, 'p-dual-listing', 5, 'start')
ok(abs(0.88 ** 6 - 0.4644) < 5e-5 and 1.13 * 0.88 ** 6 > 0.5 and abs(log(1.13) / log(1 / 0.88) - 0.96) < 0.005 and abs(h4 - 1 - 6.38) < 0.005
   and abs(log(0.5) / log(0.88) + 1 + 0.96 - h4) < 0.01, 'dual 0.4644, day 7 above half, 0.96, 6.38, 5.42 + 1 + 0.96')
ok(abs(log(750) - 6.62) < 0.005 and abs(2920.4 - 2899.4 - 21.0) < 1e-9 and abs(21.0 - log(750) - 14.38) < 0.005 and abs(0.5 / 1.13 - 0.4425) < 5e-5
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
        lv.expect('problems', 'items[1].parts[2].feedback.correct', round(float(f_two), 2))
        lv.expect('problems', 'items[3].parts[1].feedback.correct', round(float(r1e), 3))
    if n == 3:
        lv.expect('problems', 'items[1].parts[2].feedback.correct', round(f2, 4))
        lv.expect('problems', 'items[2].parts[1].feedback.correct', round(sd20, 2))
        lv.expect('problems', 'items[2].parts[0].feedback.correct', round(GAP0 * share, 2))
        lv.expect('problems', 'items[3].parts[3].feedback.correct', round(h4, 2))
    try:
        lv.report()
    except SystemExit as ex:
        ok(ex.code in (0, None), f'numbers_lib level {n} failed')

print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
