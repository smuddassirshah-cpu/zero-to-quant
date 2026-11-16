#!/usr/bin/env python3
"""Delta read, session AF, arma problem sets 1 to 3 (docs/reviews/review-delta-af-arma.md).

Recomputes every key, every `wrong` value and the printed numbers of the parts in
scope: the three re-authored problems (p-trust-discount, p-satellite-stocks,
p-swap-spread-hold) and the parts the fix pass changed. Imports nothing from the
author's or the first reader's script. Routes differ from theirs where one exists:
Durbin-Levinson, brute search, recursions, damped sums, a seeded simulation.

Exits 0. Prints one FINDING line per failing check.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
ARMA = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'arma')

checks = 0
findings = []


def load(n):
    with open(os.path.join(ARMA, 'problems-%d.json' % n), encoding='utf-8') as f:
        return {it['id']: it for it in json.load(f)['items']}


def ok(cond, label):
    global checks
    checks += 1
    if not cond:
        findings.append(label)
        print('FINDING', label)


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


def widget(item, part):
    return item['parts'][part - 1]['widget']


def texts(part):
    out = [part.get('question', '')]
    fb = part.get('feedback', {})
    out += [fb.get('correct', ''), fb.get('generic', '')] + list(fb.get('byKey', {}).values())
    out.append(part.get('explain', {}).get('text', ''))
    for o in part['widget'].get('options', []):
        out += [o.get('text', ''), o.get('why', '')]
    return ' '.join(out)


def opts_text(item):
    return ' '.join(o['text'] for o in item['parts'][0]['widget']['options'])


def numeric(item, part, key, wrong, label, typed=()):
    """key and wrong values recomputed; bands: key takes every typed form, refuses
    each wrong value, wrong bands do not meet the key band or each other."""
    w = widget(item, part)
    tol = w['tol']['abs']
    ok(close(w['answer'], key, max(1e-4 * abs(key), 6e-6)), '%s part %d key %r, recomputed %r' % (label, part, w['answer'], key))
    for t in typed:
        ok(abs(t - w['answer']) <= tol + 1e-12, '%s part %d band refuses the typed form %r' % (label, part, t))
    have = {x['id']: x for x in w.get('wrong', [])}
    ok(set(have) == set(wrong), '%s part %d wrong ids %s' % (label, part, sorted(have)))
    bands = [(w['answer'] - tol, w['answer'] + tol, 'key')]
    for k, v in wrong.items():
        if k not in have:
            continue
        ok(close(have[k]['value'], v, max(1e-4 * abs(v), 6e-5)), '%s part %d wrong %s %r, recomputed %r' % (label, part, k, have[k]['value'], v))
        wt = have[k]['tol']['abs']
        bands.append((have[k]['value'] - wt, have[k]['value'] + wt, k))
    for i in range(len(bands)):
        for j in range(i + 1, len(bands)):
            a, b = bands[i], bands[j]
            ok(a[1] < b[0] or b[1] < a[0], '%s part %d bands %s and %s overlap' % (label, part, a[2], b[2]))


def printed(item, part, strings, label):
    t = texts(item['parts'][part - 1]) if part else item['prose']
    for s in strings:
        ok(s in t, '%s part %d does not print %r' % (label, part, s))


P1, P2, P3 = load(1), load(2), load(3)

# ---------------------------------------------------------------- p-airport-anomaly
A = P1['p-airport-anomaly']
Sxx, Sxy, s2, n = 2880.0, -662.4, 3.2, 364
printed(A, 0, ['S_{xx} = 2{,}880', 'S_{xy} = -662.4', 's^2 = 3.2', '364 pairs'], 'airport')
g = Sxy / Sxx
phi = 1 + g
numeric(A, 1, g, {'flip': Sxx / Sxy, 'sign': -g}, 'airport', typed=[-0.23])
se = math.sqrt(s2 / Sxx)
t = g / se
numeric(A, 2, t, {'no-sqrt': g / (s2 / Sxx), 's-not-s2': g / math.sqrt(math.sqrt(s2) / Sxx), 'sign': -t}, 'airport', typed=[-6.9])
ok(close(se, 1 / 30, 1e-12), 'airport se is 1/30')
printed(A, 2, ['\\tfrac{1}{30}', '\\tfrac{1}{900}', '-6.90', 's = 1.789'], 'airport')
ok(close(math.sqrt(s2), 1.789, 6e-4), 'airport s = 1.789')
printed(A, 3, ['-6.90', '−6.90', '−3.45', '−2.87'], 'airport')
ok(texts(A['parts'][2]).count('6.90') >= 6 and '4.55' not in texts(A['parts'][2]), 'airport part 3 carries -6.90 in every place')
ok(t < -3.45 < -2.87 < -1.645, 'airport verdict: t beyond the 1% and 5% points')
# variance by a damped sum of squared psi weights, not the closed form
gamma0 = s2 * sum(phi ** (2 * j) for j in range(4000))
numeric(A, 4, gamma0, {'shock': s2, 'no-square': s2 / (1 - phi)}, 'airport', typed=[7.86])
printed(A, 4, ['0.4071', '0.5929', '2.80', '1.79', '3.2/0.23'], 'airport')
# the stem statistics agree with each other
ok(abs(Sxx / n - gamma0) / gamma0 < 0.02, 'airport S_xx/364 = %.3f against the variance of part 4 %.3f' % (Sxx / n, gamma0))
t_theory = g * math.sqrt(n) / math.sqrt(1 - phi ** 2)
ok(abs(t - t_theory) < 0.05, 'airport t %.3f against gamma sqrt(n)/sqrt(1 - phi^2) %.3f' % (t, t_theory))
var_dx = 2 * gamma0 * (1 - phi)            # variance of a day's change of an AR(1)
resid = var_dx - g * g * gamma0             # what the regression leaves
ok(abs(resid - s2) < 1e-9, 'airport residual variance implied by the AR(1) is %.4f against s^2 3.2' % resid)
# the same regression on a seeded sample of 365 days gives statistics of this size
rng = np.random.default_rng(20261116)
ts = []
for _ in range(400):
    e = rng.normal(0, math.sqrt(s2), 365 + 200)
    x = np.zeros(565)
    for i in range(1, 565):
        x[i] = phi * x[i - 1] + e[i]
    x = x[200:]
    lag, d = x[:-1] - x[:-1].mean(), np.diff(x)
    b = (lag * (d - d.mean())).sum() / (lag * lag).sum()
    r = d - d.mean() - b * lag
    ts.append(b / math.sqrt((r * r).sum() / 362 / (lag * lag).sum()))
ok(np.percentile(ts, 5) < t < np.percentile(ts, 95), 'airport t %.2f inside the simulated 5 to 95 range (%.2f, %.2f)' % (t, np.percentile(ts, 5), np.percentile(ts, 95)))
sd = math.sqrt(gamma0)
p5 = norm.sf(5 / sd)
numeric(A, 5, p5, {'shock-sd': norm.sf(5 / math.sqrt(s2)), 'no-square': norm.sf(5 / math.sqrt(s2 / (1 - phi)))}, 'airport',
        typed=[0.037, 0.038, round(norm.sf(1.78), 3), round(norm.sf(1.783), 3)])
w5 = widget(A, 5)
for x in w5['wrong']:
    ok(abs(round(x['value'], 3) - x['value']) <= x['tol']['abs'], 'airport part 5 wrong %s takes its own 3-place form' % x['id'])
ok(close(5 / 2.804, 1.783, 6e-4) and round(norm.sf(1.783), 3) == 0.037, 'airport part 5 working 1.783 and 0.037')
printed(A, 5, ['5/2.804 = 1.783', '0.037', 'about 14 days', '13.91'], 'airport')
ok(round(p5 * 365) == 14 and round(norm.sf(5 / math.sqrt(s2)) * 365) == 1, 'airport 14 days and about one')

# ---------------------------------------------------------------- lines of problems-1 fixed as written
ok('You kept 3.5%' in texts(P1['p-gdp-trend']['parts'][0]), 'gdp slip line as the review wrote it')
ok(close(math.log(1820) - math.log(1450), 0.2273, 5e-5) and close((math.log(1820 / 1450)) / 500 * 1e4, 4.55, 6e-3), 'gold 0.2273 and 4.55 bp')
ok('whatever the closes in between' in texts(P1['p-gold-drift']['parts'][0]), 'gold explain as the review wrote it')
ok('It removes what the screen was for' in texts(P1['p-ppp-screen']['parts'][4]), 'ppp option as the review wrote it')

# ---------------------------------------------------------------- p-etf-flows
E = P2['p-etf-flows']
ss, cp, r2, nw = 180000.0, 79200.0, 0.24, 200
printed(E, 0, ['180{,}000', '79{,}200', '0.24', '200 weeks'], 'etf')
r1 = cp / ss
numeric(E, 1, r1, {'flip': ss / cp}, 'etf', typed=[0.44])
ok(abs(r1) < 1 and r2 >= 2 * r1 * r1 - 1, 'etf: phi = 0.44 is stationary and (0.44, 0.24) is a possible pair of autocorrelations')
Q = sum(nw * (nw + 2) * r * r / (nw - k) for k, r in ((1, r1), (2, r2)))
numeric(E, 2, Q, {'box-pierce': nw * (r1 * r1 + r2 * r2), 'no-n-k': nw * (nw + 2) * (r1 * r1 + r2 * r2)}, 'etf', typed=[51.06])
from scipy.stats import chi2
ok(close(chi2.ppf(0.95, 2), 5.99, 6e-3) and Q > 5.99, 'etf 5.99 and the rejection')
printed(E, 2, ['0.1936/199 + 0.0576/198', '51.06', '40{,}400', '0.1936 + 0.0576'], 'etf')
# lag-2 autocorrelation of the AR(1) from a long recursion of autocovariances
gam = [1.0]
for _ in range(2):
    gam.append(r1 * gam[-1])
numeric(E, 3, gam[2], {'double': 2 * r1, 'sample': r2}, 'etf', typed=[0.1936])
ok(close(1.96 / math.sqrt(nw), 0.139, 6e-4) and round(abs(r2 - gam[2]), 2) == 0.05, 'etf band 0.139 and the gap 0.05')
sig = math.sqrt(ss / nw * (1 - r1 * r1))
numeric(E, 4, sig, {'no-square': math.sqrt(ss / nw * (1 - r1)), 'series-sd': math.sqrt(ss / nw), 'variance': ss / nw * (1 - r1 * r1)}, 'etf', typed=[26.94])
printed(E, 4, ['0.8064', '725.76', '26.94', '900 \\times 0.56', 'about 10%'], 'etf')
ok(round((30 - sig) / 30 * 100) == 10, 'etf about 10%')
ok('0.45' not in json.dumps(E) and '0.2025' not in json.dumps(E) and '0.7975' not in json.dumps(E), 'etf: no number of the old set is left')

# ---------------------------------------------------------------- p-peg-fridays, changed lines
G = P2['p-peg-fridays']
ok(close(4 / (1 - 0.88 ** 2), 17.73, 6e-3) and close(1 - 0.88 ** 2, 0.2256, 1e-9), 'peg 17.73 and 0.2256')
ok(close(0.88 ** 5, 0.5277, 5e-5) and close(17.73 * (1 - 0.5277 ** 2), widget(G, 3)['answer'], widget(G, 3)['tol']['abs']), 'peg part 3 from the restated 17.73 stays in the band')
lin = [x for x in widget(G, 2)['wrong'] if x['id'] == 'linear']
ok(lin and close(lin[0]['value'], 1 - 5 * 0.12, 1e-9), 'peg linear slip is 1 - 5 x 0.12')
printed(G, 3, ['17.73 bp²'], 'peg')

# ---------------------------------------------------------------- p-trust-discount
T = P2['p-trust-discount']
import re
def row(word):
    m = re.search(word + r' lags give ((?:[−-]?\d\.\d\d(?:, | and )?)+)', T['prose'])
    return [float(x.replace('−', '-')) for x in re.findall(r'[−-]?\d\.\d\d', m.group(1))]
rows = {1: (1.84, [0.80]), 2: (1.38, [0.61, 0.24]), 3: (None, row('Three')), 4: (None, row('Four'))}
ok(len(rows[3][1]) == 3 and len(rows[4][1]) == 4, 'trust: three-lag and four-lag rows read from the prose')
printed(T, 0, ['constant 1.84 and slope 0.80', 'constant 1.38 and coefficients 0.61 and 0.24', '±0.086', '520 weeks'], 'trust')
band = 1.96 / math.sqrt(520)
ok(close(band, 0.086, 5e-4), 'trust band 0.086')
pacf = [rows[k][1][-1] for k in (1, 2, 3, 4)]
ok([abs(a) > band for a in pacf] == [True, True, False, False], 'trust: the PACF proposes order 2')
ok(abs(rows[4][1][2]) > band, 'trust: the trap coefficient of week 3 in the four-lag row is outside the band')
seq = ', '.join(('%.2f' % a).replace('-', '−') for a in pacf)
ok(seq in opts_text(T) and seq.replace(', ' + seq.split(', ')[-1], ' and ' + seq.split(', ')[-1]) in texts(T['parts'][0]), 'trust part 1 prints the PACF ' + seq)
opts = {o['id']: o for o in widget(T, 1)['options']}
ok(opts['two'].get('correct') is True and sum(1 for o in opts.values() if o.get('correct')) == 1, 'trust part 1 key')
# the one-lag slope is the lag-1 autocorrelation the two-lag fit implies
ok(abs(0.61 / (1 - 0.24) - 0.80) < 0.005, 'trust: rho_1 of the two-lag fit %.4f against the one-lag slope 0.80' % (0.61 / 0.76))
# Durbin-Levinson: each longer row follows from the row before and its newest coefficient
def step(prev, last):
    return [prev[j] - last * prev[len(prev) - 1 - j] for j in range(len(prev))] + [last]
for k in (3, 4):
    want = step(rows[k - 1][1], rows[k][1][-1])
    for j, (a, b) in enumerate(zip(rows[k][1], want)):
        ok(abs(a - b) < 0.0125, 'trust: %d-lag row, week %d prints %.2f, the %d-lag row and the newest coefficient give %.3f' % (k, j + 1, a, k - 1, b))
mu = 1.38 / (1 - 0.61 - 0.24)
numeric(T, 2, mu, {'one-lag': 1.38 / (1 - 0.61), 'constant': 1.38}, 'trust', typed=[9.2])
ok(close(1.84 / (1 - 0.80), mu, 1e-9), 'trust: both fits give the mean 9.2')
# the mean as the fixed point of the recursion
xs = [0.0, 0.0]
for _ in range(3000):
    xs.append(1.38 + 0.61 * xs[-1] + 0.24 * xs[-2])
ok(close(xs[-1], mu, 1e-9), 'trust: the recursion settles at the mean')
f2 = 1.38 + 0.61 * 12.0 + 0.24 * 13.5
numeric(T, 3, f2, {'swap': 1.38 + 0.61 * 13.5 + 0.24 * 12.0, 'no-constant': 0.61 * 12.0 + 0.24 * 13.5}, 'trust', typed=[11.94])
ok(close(mu + 0.61 * 2.8 + 0.24 * 4.3, f2, 1e-9), 'trust: the forecast from the mean form')
printed(T, 3, ['1.708', '1.032', '1.38 + 7.32 + 3.24'], 'trust')
f1 = 1.84 + 0.80 * 12.0
numeric(T, 4, f2 - f1, {'sign': f1 - f2, 'narrowing': 12.0 - f1}, 'trust', typed=[0.5])
printed(T, 4, ['11.44', '0.56', '0.06', 'nearly nine tenths'], 'trust')
ok(close(12.0 - f2, 0.06, 1e-9) and 0.85 < (f2 - f1) / (12.0 - f1) < 0.9, 'trust: 0.06 and nearly nine tenths')
# reuse: the PACF tail beside l8 screens[1], series B, and screens[4]
l8 = json.load(open(os.path.join(ARMA, [f for f in os.listdir(ARMA) if f.startswith('l8-')][0]), encoding='utf-8'))
B = l8['screens'][1]['canvas']['params']['params']['C2']
lesson_tail = [round(B[k][-1], 2) for k in (1, 2, 3)]
ok(max(abs(a - b) for a, b in zip(pacf[1:], lesson_tail)) > 0.015,
   'reuse: trust PACF at lags 2 to 4 %s against l8 screens[1] series B %s' % (pacf[1:], lesson_tail))

# ---------------------------------------------------------------- p-satellite-stocks
S = P2['p-satellite-stocks']
phis, sdx, sde = 0.85, 6.0, 3.5
printed(S, 0, ['\\phi = 0.85', 'sd 6', 'sd 3.5'], 'satellite')
v = sdx ** 2 + sde ** 2
numeric(S, 1, v, {'add-sds': (sdx + sde) ** 2, 'true-only': sdx ** 2, 'sd': math.sqrt(v)}, 'satellite', typed=[48.25])
ok(0.24 < sde ** 2 / v < 0.27, 'satellite: about a quarter is error')
rho = lambda k: phis ** k * sdx ** 2 / v
numeric(S, 2, rho(1), {'no-error': phis, 'error-lag': (phis * sdx ** 2 + sde ** 2) / v, 'sds': phis * sdx / math.sqrt(v)}, 'satellite', typed=[0.634])
numeric(S, 3, rho(4), {'ar1': rho(1) ** 4, 'true': phis ** 4, 'extra': rho(1) * phis ** 4}, 'satellite', typed=[0.389, round(0.634 * 0.85 ** 3, 3)])
printed(S, 3, ['18.79', '0.162', '0.389'], 'satellite')
ok(close(phis ** 4 * 36, 18.79, 6e-3), 'satellite 18.79')
est = (0.40 / 0.61) ** (1 / 3)
numeric(S, 4, est, {'lag1': 0.61, 'fourth-root': (0.40 / 0.61) ** 0.25, 'ar1': 0.40 ** 0.25}, 'satellite', typed=[0.869])
printed(S, 4, ['0.6557', '0.656', '0.869'], 'satellite')
# seeded simulation of the estimates: the ACF is scaled, not an AR(1)'s
rng = np.random.default_rng(7)
N = 400000
e = rng.normal(0, sdx * math.sqrt(1 - phis ** 2), N)
x = np.zeros(N)
for i in range(1, N):
    x[i] = phis * x[i - 1] + e[i]
y = x + rng.normal(0, sde, N)
y = y - y.mean()
ac = lambda k: float((y[k:] * y[:-k]).sum() / (y * y).sum())
ok(abs(y.var() - v) < 0.6 and abs(ac(1) - rho(1)) < 0.01 and abs(ac(4) - rho(4)) < 0.01, 'satellite: simulated variance and lags 1 and 4')
ok(abs((ac(4) / ac(1)) ** (1 / 3) - phis) < 0.01, 'satellite: the ratio of lags recovers phi')
# the sample values of part 4 are within sampling error of the model's on 520 weeks
ok(abs(0.61 - rho(1)) < 2 / math.sqrt(520) and abs(0.40 - rho(4)) < 2 / math.sqrt(520), 'satellite: 0.61 and 0.40 are plausible on 520 weeks')
l9 = json.load(open(os.path.join(ARMA, [f for f in os.listdir(ARMA) if f.startswith('l9-')][0]), encoding='utf-8'))
ok(not ('variance but no covariance' in json.dumps(l9) and 'variance but no covariance' in json.dumps(S)),
   'reuse: satellite part 2 `no-error` line "add variance but no covariance" against l9 quiz[3] "adds variance but no covariance"')

# ---------------------------------------------------------------- p-smoothed-fund, changed line
ok(close(0.4 * 0.6, 0.24, 1e-12) and close(0.24 / (0.4 ** 2 + 0.6 ** 2), 0.4615, 5e-5), 'smoothed fund 0.24 and 0.4615')

# ---------------------------------------------------------------- p-inflation-arma
I = P3['p-inflation-arma']
m, ph, th = 0.25, 0.82, -0.20
printed(I, 0, ['\\mu = 0.25', '\\phi = 0.82', '\\theta = -0.20', '0.43', '0.55'], 'inflation')
ok(abs(ph) < 1 and abs(th) < 1 and abs(ph + th) > 1e-9, 'inflation: stationary, invertible, no common factor')
eps = 0.55 - 0.43
numeric(I, 1, eps, {'gap': 0.55 - m, 'sign': -eps}, 'inflation', typed=[0.12])
# forecasts by running the model forward with future shocks at 0
def path(theta_used, x0=0.55, e0=eps, H=40):
    out, x, e = [], x0, e0
    for _ in range(H):
        x = m + ph * (x - m) + theta_used * e
        e = 0.0
        out.append(x)
    return out
f = path(th)
numeric(I, 2, f[0], {'no-ma': path(0.0)[0], 'theta-sign': path(-th)[0]}, 'inflation', typed=[0.472])
numeric(I, 3, f[1], {'ma-again': f[1] + th * eps, 'from-xn': m + ph ** 2 * (0.55 - m)}, 'inflation', typed=[0.4320, 0.43204])
first = next(h for h in range(1, 41) if abs(f[h - 1] - m) < 0.05)
first_ar = next(h for h in range(1, 41) if abs(path(0.0)[h - 1] - m) < 0.05)
numeric(I, 4, first, {'no-ma': first_ar, 'off-by-one': first - 1}, 'inflation', typed=[9])
ok(close(f[7] - m, 0.0553, 5e-5) and close(f[8] - m, 0.0454, 5e-5), 'inflation gaps 0.0553 and 0.0454')
ok(close(math.log(0.05 / 0.222) / math.log(0.82), 7.51, 6e-3) and close(0.05 / 0.222, 0.225, 6e-4), 'inflation 7.51 and 0.225')
printed(I, 2, ['0.246', '-0.024', '0.472'], 'inflation')
printed(I, 3, ['0.472', '0.1820', '0.4320', '0.222'], 'inflation')
printed(I, 4, ['0.222', '0.0553', '0.0454', '7.51', 'would say 10'], 'inflation')
ok('0.35' not in json.dumps(I) and '0.454' not in json.dumps(I).replace('0.0454', ''), 'inflation: no number of the old set is left')
# statsmodels: psi weights of the ARMA(1, 1) give the same two-step forecast
from statsmodels.tsa.arima_process import arma2ma
psi = arma2ma([1, -ph], [1, th], lags=6)
ok(close(psi[1], ph + th, 1e-12) and close(psi[2], ph * (ph + th), 1e-12), 'inflation psi weights')

# ---------------------------------------------------------------- p-dual-listing
D = P3['p-dual-listing']
la, lb, nd = -1460.2, -1449.7, 750
bic = lambda k, l: k * math.log(nd) - 2 * l
gap = bic(3, la) - bic(4, lb)
numeric(D, 1, gap, {'aic': (2 * 3 - 2 * la) - (2 * 4 - 2 * lb), 'sign': -gap}, 'dual', typed=[14.38])
printed(D, 1, ['2920.4', '2899.4', '21.0', '6.62', '14.38'], 'dual')
psi = arma2ma([1, -0.88], [1, 0.25], lags=12)
numeric(D, 2, psi[1], {'ar': 0.88, 'ma': 0.25, 'product': 0.88 * 0.25}, 'dual', typed=[1.13])
numeric(D, 3, psi[7], {'ar': 0.88 ** 7, 'off-by-one': psi[8]}, 'dual', typed=[0.5248])
printed(D, 3, ['0.4644', '0.5248', '0.4087', '7 days'], 'dual')
ok(close(0.88 ** 6, 0.4644, 5e-5), 'dual 0.4644')
h = 1 + math.log(0.5 / 1.13) / math.log(0.88)
numeric(D, 4, h, {'ar': math.log(0.5) / math.log(0.88), 'half-peak': 1 + math.log(0.5) / math.log(0.88)}, 'dual', typed=[7.38])
ok(close(math.log(0.5) / math.log(0.88) + 1 + math.log(1.13) / -math.log(0.88), h, 1e-9) and close(math.log(1.13) / -math.log(0.88), 0.96, 6e-3), 'dual 5.42 + 1 + 0.96')
ok(psi[7] > 0.5 > psi[8], 'dual: the effect is still above one half on day 7 and below it on day 8')
ok('0.88^5' not in json.dumps(D) and '0.5277' not in json.dumps(D), 'dual: 0.88^5 of p-peg-fridays is gone')

# ---------------------------------------------------------------- p-swap-spread-hold
W = P3['p-swap-spread-hold']
printed(W, 0, ['half-life of 12 trading days', 'long-run sd of 6 bp', '9 bp above', '20 trading days'], 'swap')
phd = 0.5 ** (1 / 12)
# gap by stepping the AR(1) day by day
gap20 = 9.0
for _ in range(20):
    gap20 *= phd
numeric(W, 1, gap20, {'linear': 9 * (1 - 20 / 24), 'half': 4.5, 'flip': 9 * 0.5 ** (12 / 20)}, 'swap', typed=[2.83])
ok(close(0.5 ** (20 / 12), 0.315, 5e-4) and close(20 / 12, 1.667, 5e-4), 'swap 0.315 and 1.667')
# 20-day error variance as a sum of 20 damped shock variances
sig2 = 36 * (1 - phd ** 2)
var20 = sum(sig2 * phd ** (2 * j) for j in range(20))
sd20 = math.sqrt(var20)
numeric(W, 2, sd20, {'not-squared': 6 * math.sqrt(1 - 0.315), 'no-root': 6 * (1 - 0.315 ** 2), 'variance': var20}, 'swap',
        typed=[5.69, round(math.sqrt(36 * (1 - 0.315 ** 2)), 2)])
printed(W, 2, ['0.9008', '32.43', '5.69'], 'swap')
p_loss = norm.sf((9 - gap20) / sd20)
numeric(W, 3, p_loss, {'from-mean': norm.sf(9 / sd20), 'long-run': norm.sf((9 - gap20) / 6), 'win': 1 - p_loss}, 'swap',
        typed=[0.139, 0.140, round(norm.sf(1.08), 3), round(norm.sf((9 - 2.83) / 5.69), 3)])
for x in widget(W, 3)['wrong']:
    alt = {'from-mean': norm.sf(9 / 5.69), 'long-run': norm.sf((9 - 2.83) / 6), 'win': 1 - norm.sf((9 - 2.83) / 5.69)}[x['id']]
    ok(abs(round(alt, 3) - x['value']) <= x['tol']['abs'], 'swap part 3 wrong %s takes the value from the restated 2.83 and 5.69' % x['id'])
# the key sits on a rounding tie: the working printed should give the value the key rounds to
z_stated = (9 - 2.83) / 5.69
ok(round(p_loss, 3) == round(norm.sf(z_stated), 3) == 0.139, 'swap part 3: exact and restated routes both round to 0.139')
ok('0.139' in texts(W['parts'][2]),
   'other: swap part 3 prints "1.08 sds" and 0.140 (the tail at 1.08 is %.4f); the key %.6f and the value from 2.83 and 5.69 at z = %.3f (%.4f) both round to 0.139'
   % (norm.sf(1.08), p_loss, z_stated, norm.sf(z_stated)))
floor = norm.sf(9 / 6)
numeric(W, 4, floor, {'two-sided': 2 * floor, 'variance': norm.sf(9 / 36)}, 'swap', typed=[0.067])
# "never below 0.067": the chance of a loss falls at every longer hold
ps = []
for hh in range(1, 2000):
    a = phd ** hh
    ps.append(norm.sf(9 * (1 - a) / (6 * math.sqrt(1 - a * a))))
ok(all(ps[i] > ps[i + 1] for i in range(300)) and all(ps[i] >= ps[i + 1] for i in range(len(ps) - 1)) and ps[-1] > floor - 1e-12 and abs(ps[-1] - floor) < 1e-6, 'swap: the chance of a loss falls with the hold and stays above the floor')
ok(close(ps[19], p_loss, 1e-9) and 6.5 < 1 / p_loss < 7.5, 'swap: day 20 on the path, about one trade in seven')

print('%d checks, %d FINDING lines' % (checks, len(findings)))
sys.exit(0)
