#!/usr/bin/env python3
"""Bank part 2, session 3: every key, slip and stated figure in statistics-3, finance-3, behavioural-7 and coding-3, by two routes.

coding-3: each solution runs on every example and hidden test, the untouched starter fails, a brute-force twin agrees on every
test, and each named trap (near-miss) fails a hidden test; the slow trap runs in a fresh CPython with a 5 s limit. Reading
items run their own lines (NumPy when present; C++ with g++ -std=c++20).

Standard library only (runs under plain python3). numbers_lib.py has no Bank loader yet (B2-E4), so the JSON is read here.
Route A is exact (Fraction) or closed form; route B is enumeration, a seeded simulation with a stated tolerance, a
numerical solve or a step-by-step loop that shares no code with route A. Each slip is computed by carrying out the
slip its byKey line names. Each value is then asserted at its path in the JSON. Exit 0 means every check passed.
"""
import json, math, os, random, re, sys
from fractions import Fraction as F
from math import sqrt, exp, log, erf, erfc, pi
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, '..', '..', 'app', 'content', 'bank')
FILES = ['statistics-3', 'finance-3', 'behavioural-7', 'coding-3']
DATA = {f: json.load(open(os.path.join(BANK, f + '.json'), encoding='utf-8')) for f in FILES}
ITEMS = {(f, it['id']): it for f in FILES for it in DATA[f]['items']}
fails, checks = [], [0]
N = NormalDist()


def ok(cond, label):
    checks[0] += 1
    if not cond:
        fails.append(label)
        print('FAIL', label)


def close(a, b, tol, label):
    ok(abs(float(a) - float(b)) <= tol, f'{label}: {float(a)!r} vs {float(b)!r} (tol {tol})')


def two(a, b, tol, label):
    """Route A and route B agree; returns route A."""
    close(a, b, tol, label + ' [two routes]')
    return float(a)


def item(f, i):
    it = ITEMS.get((f, i))
    ok(it is not None, f'{f}/{i} exists')
    return it


def numeric(f, i, key, asked_dp, slips):
    """key: the computed value. asked_dp: places the question asks for (None for a whole number).
    slips: {wrong id: computed slip value}. Checks the stored answer, its band, every wrong value and band, and byKey."""
    it = item(f, i)
    w = it['widget']
    ok(w['kind'] == 'numeric', f'{f}/{i}: numeric')
    scale = 100 if w.get('unit') == '%' else 1
    ans, tol = w['answer'], w['tol']['abs']
    lab = f'{f}/{i}'
    ok(abs(ans - float(key)) <= tol + 1e-12, f'{lab}: computed key {float(key)} inside stored band {ans} +- {tol}')
    if asked_dp is not None:
        rounded = round(float(key) * scale, asked_dp) / scale
        ok(abs(rounded - ans) <= tol + 1e-12, f'{lab}: rounded key {rounded} inside band')
        close(ans, key, 0.5 * 10 ** -asked_dp / scale, f'{lab}: stored answer within half a unit of the exact value')
    else:
        ok(float(key) == round(float(key)) and ans == key, f'{lab}: whole-number key {key} stored exactly')
    ids = {x['id']: x for x in w['wrong']}
    ok(set(ids) == set(slips), f'{lab}: wrong ids {sorted(ids)} match computed slips {sorted(slips)}')
    ok(len(ids) >= 2, f'{lab}: at least two wrong entries')
    for wid, v in slips.items():
        x = ids.get(wid)
        if not x:
            continue
        v = float(v)
        ok(abs(x['value'] - v) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: computed slip {v} inside its band {x["value"]} +- {x["tol"]["abs"]}')
        if asked_dp is not None:
            ok(abs(x['value'] - round(v * scale, asked_dp) / scale) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: slip as rounded inside its band')
        ok(abs(x['value'] - ans) > tol + x['tol']['abs'], f'{lab}.{wid}: band does not touch the key band')
        ok(wid in it['feedback'].get('byKey', {}), f'{lab}.{wid}: byKey line')
        ok(x['tol']['abs'] <= 0.5 * abs(x['value']) or x['value'] == 0, f'{lab}.{wid}: band not over half the value')
    vals = sorted(w['wrong'], key=lambda x: x['value'])
    for a, b in zip(vals, vals[1:]):
        ok(b['value'] - a['value'] > a['tol']['abs'] + b['tol']['abs'], f'{lab}: wrong bands {a["id"]} and {b["id"]} apart')
    return it


def stated(f, i, phrase):
    """A figure computed above is printed in the item (any field)."""
    blob = json.dumps(item(f, i), ensure_ascii=False)
    ok(phrase in blob, f'{f}/{i}: states "{phrase}"')


def choice(f, i, key_text_part):
    it = item(f, i)
    opts = it['widget']['options']
    corr = [o for o in opts if o.get('correct')]
    ok(len(opts) == 4 and len(corr) == 1, f'{f}/{i}: four options, one correct')
    ok(key_text_part in corr[0]['text'], f'{f}/{i}: key text')
    ok(all(o.get('why') for o in opts if not o.get('correct')), f'{f}/{i}: why on each distractor')
    others = max(len(o['text']) for o in opts if not o.get('correct'))
    ok(len(corr[0]['text']) - others <= 9, f'{f}/{i}: key not longer than the longest distractor by more than 9')
    ok(it['widget'].get('shuffle', True) is True, f'{f}/{i}: shuffle on')
    ok(len({o['text'] for o in opts}) == 4, f'{f}/{i}: options distinct')
    return it


def fmt(x, dp):
    return f'{x:.{dp}f}'


def ols(x, y):
    """Simple least squares with intercept: slope, its usual standard error, residuals."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx
    res = [c - a0 - b * a for a, c in zip(x, y)]
    return b, sqrt(sum(r * r for r in res) / (n - 2) / sxx), res


S, FI, B = 'statistics-3', 'finance-3', 'behavioural-7'

# ---------------------------------------------------------------- statistics-3
# es-estimators-pool-two-estimates: inverse-variance weights against a grid search over the weight
a = 1 / (F(1, 4) + F(1, 12))
grid = [(k / 100000, (k / 100000) ** 2 * 4 + (1 - k / 100000) ** 2 * 12) for k in range(100001)]
wbest, vbest = min(grid, key=lambda t: t[1])
two(a, vbest, 1e-8, 'pooled variance')
two(F(12, 16), wbest, 1e-5, 'weight on the variance-4 estimate is 3/4')
ok(all(v >= 3 - 1e-12 for _, v in grid), 'claim: no weights summing to 1 give less than 3')
eq = two(F(1, 4) * (4 + 12), dict(grid)[0.5], 1e-12, 'equal weights slip')
numeric(S, 'es-estimators-pool-two-estimates', int(a), None,
        {'equal-weights': eq, 'average-variances': F(4 + 12, 2), 'total-precision': F(1, 4) + F(1, 12)})

# estimator-bias-divide-by-n: (n-1)/n sigma^2 against a seeded simulation of 200,000 samples of five normals
a = F(4, 5) * 10
rng = random.Random(31)
tot = 0.0
for _ in range(200000):
    xs = [rng.gauss(0, sqrt(10)) for _ in range(5)]
    m = sum(xs) / 5
    tot += sum((x - m) ** 2 for x in xs) / 5
two(a, tot / 200000, 0.05, 'expected divide-by-n estimate (simulation tolerance 0.05)')
numeric(S, 'estimator-bias-divide-by-n', int(a), None, {'no-bias': 10, 'wrong-way': F(5, 4) * 10})
ok(F(10) - a == F(10, 5), 'bias is sigma^2/n = 2')

# es-intervals-wider-confidence: centre plus scaled half-width, against solving for the standard error first
centre, half = F(2 + 10, 2), F(10 - 2, 2)
a = centre + half * F(2576, 1000) / F(196, 100)
se = (10 - 2) / (2 * 1.96)
b = (2 + 10) / 2 + 2.576 * se
key = two(a, b, 1e-12, '99% upper end')
numeric(S, 'es-intervals-wider-confidence', key, 2,
        {'added-gap': 10 + (2.576 - 1.96), 'scaled-end': 10 * 2.576 / 1.96})
stated(S, 'es-intervals-wider-confidence', '4 \\\\times 2.576/1.96 \\\\approx 5.257')
ok(fmt(float(half * F(2576, 1000) / F(196, 100)), 3) == '5.257', 'half-width 5.257')

# es-bayes-arrivals-per-day: conjugate gamma against a midpoint integral of prior times likelihood
a = F(3 + 12, 1 + 5)
h = 1e-4
grid = [(k + 0.5) * h for k in range(int(30 / h))]
dens = [lam ** 2 * exp(-lam) * lam ** 12 * exp(-5 * lam) for lam in grid]      # gamma(3,1) prior times Poisson(5 lam) likelihood
b = sum(l * d for l, d in zip(grid, dens)) / sum(dens)
key = two(a, b, 1e-6, 'posterior mean rate')
numeric(S, 'es-bayes-arrivals-per-day', key, 1, {'data-only': F(12, 5), 'prior-only': F(3, 1)})

# ht-setup-die-sixty-rolls: the statistic two ways, and the 5% point on 5 degrees of freedom two ways
obs = [5, 8, 9, 8, 10, 20]
a = sum(F((o - 10) ** 2, 10) for o in obs)
b = sum(o * o for o in obs) / 10 - 60                                          # sum O^2/E - n
key = two(a, b, 1e-12, 'chi-squared')
numeric(S, 'ht-setup-die-sixty-rolls', key, 1, {'not-divided': sum((o - 10) ** 2 for o in obs), 'absolute-gaps': F(sum(abs(o - 10) for o in obs), 10)})
x = 11.07
q_closed = erfc(sqrt(x / 2)) + sqrt(2 * x / pi) * exp(-x / 2) * (1 + x / 3)     # survival of chi-squared on 5 df
hh = 1e-4
q_int = 1 - sum(((k + 0.5) * hh) ** 1.5 * exp(-(k + 0.5) * hh / 2) for k in range(int(x / hh))) * hh / (2 ** 2.5 * math.gamma(2.5))
two(q_closed, q_int, 1e-5, 'upper tail at 11.07 on 5 df')
close(q_closed, 0.05, 0.0005, '11.07 is the 5% point')
ok(float(a) > 11.07, 'statistic beats the 5% point')
stated(S, 'ht-setup-die-sixty-rolls', '134/10 = 13.4')

# weak-signal-daily-edge
a = F(5, 100) / (F(1) / 20)
b = 0.0005 / (0.01 / sqrt(400))
key = two(a, b, 1e-12, 't statistic')
numeric(S, 'weak-signal-daily-edge', key, 2, {'no-root': F(5, 100) / 1, 'annual-sharpe': 0.05 * sqrt(252)})
n2 = next(n for n in range(1, 10000) if 0.05 * sqrt(n) >= 2 - 1e-12)
two(n2, (2 / 0.05) ** 2, 0, 'days for t = 2')
stated(S, 'weak-signal-daily-edge', '1,600 days')

# ht-errors-sample-for-power: the formula against a count-up on exact two-sided power
n_formula = ((1.96 + 0.8416) * 10 / 2) ** 2
power = lambda n: N.cdf(sqrt(n) * 2 / 10 - 1.96) + N.cdf(-sqrt(n) * 2 / 10 - 1.96)
n_count = next(n for n in range(1, 1000) if power(n) >= 0.8)
key = two(math.ceil(n_formula), n_count, 0, 'smallest n')
ok(power(196) < 0.8 <= power(197), 'claim: 197 is the smallest n with power 80%')
ok(fmt(power(196), 4) == '0.7995', f'power at 196 is {power(196)}')
ok(fmt(n_formula, 1) == '196.2' and fmt(2.8016 * 5, 3) == '14.008', 'stated 196.2 and 14.008')
numeric(S, 'ht-errors-sample-for-power', key, None,
        {'no-power': math.ceil((1.96 * 5) ** 2), 'one-sided': math.ceil(((1.645 + 0.8416) * 5) ** 2), 'rounded-down': math.floor(n_formula)})
stated(S, 'ht-errors-sample-for-power', '79.95%')

# ht-multiple-share-false: expected false passes over passes, against a seeded simulation of 200 null signals
a = F(200, 100) / 14
rng = random.Random(5)
fp = sum(sum(1 for _ in range(200) if rng.random() < 0.01) for _ in range(20000)) / 20000
two(a, fp / 14, 0.002, 'share false (simulation tolerance 0.002)')
numeric(S, 'ht-multiple-share-false', a, 1, {'gave-level': F(1, 100), 'pass-rate': F(14, 200)})   # places of the per cent figure
stated(S, 'ht-multiple-share-false', '2/14 \\\\approx 14.3\\\\%')

# rg-fit-correlation-from-sums: closed form against least squares on built points with TSS 200 and RSS 50
a = -sqrt(1 - F(50, 200))
xs = [-3, -1, 1, 3]                     # Sxx = 20
slope = -sqrt(150 / 20)                 # explained SS = slope^2 Sxx = 150
resid = [sqrt(50 / 4) * s for s in (1, -1, -1, 1)]     # orthogonal to 1 and x, sum of squares 50
ys = [slope * x + r for x, r in zip(xs, resid)]
my = sum(ys) / 4
r_num = sum(x * (y - my) for x, y in zip(xs, ys)) / sqrt(sum(x * x for x in xs) * sum((y - my) ** 2 for y in ys))
two(sum((y - my) ** 2 for y in ys), 200, 1e-9, 'built points TSS 200')
key = two(a, r_num, 1e-12, 'correlation')
numeric(S, 'rg-fit-correlation-from-sums', key, 3, {'sign': -key, 'no-root': -F(3, 4), 'residual-share': -sqrt(F(50, 200))})

# rg-inference-new-observation: s sqrt(1 + 1/n) against a seeded simulation of fitted lines and new points
a = 2 * sqrt(1 + F(1, 25))
rng = random.Random(11)
xs = [k for k in range(25)]
mx = sum(xs) / 25
errs = []
for _ in range(40000):
    ys = [1 + 0.5 * x + rng.gauss(0, 2) for x in xs]
    b1, _, _ = ols(xs, ys)
    pred = sum(ys) / 25                  # the fitted value at the mean of x
    errs.append(1 + 0.5 * mx + rng.gauss(0, 2) - pred)
b = sqrt(sum(e * e for e in errs) / len(errs))
key = two(a, b, 0.02, 'prediction standard error (simulation tolerance 0.02)')
numeric(S, 'rg-inference-new-observation', key, 2, {'fitted-mean': F(2, 5), 'noise-only': 2})
ok(fmt(4 + 0.16, 2) == '4.16', 'variances add to 4.16')

# rg-diagnostics-fanning-residuals: seeded simulation against the sandwich formula on fresh designs
rng = random.Random(20261111)
slopes, ses = [], []
for _ in range(4000):
    x = [rng.uniform(0, 10) for _ in range(50)]
    y = [1 + 0.5 * a_ + rng.gauss(0, 0.2 * a_) for a_ in x]
    b1, se1, _ = ols(x, y)
    slopes.append(b1)
    ses.append(se1)
m_s = sum(slopes) / len(slopes)
sd_s = sqrt(sum((s - m_s) ** 2 for s in slopes) / (len(slopes) - 1))
rep = sum(ses) / len(ses)
rng = random.Random(99)
true_v, rep_v = [], []
for _ in range(4000):                                     # route B: exact conditional variances, no noise drawn
    x = [rng.uniform(0, 10) for _ in range(50)]
    mx_ = sum(x) / 50
    sxx = sum((a_ - mx_) ** 2 for a_ in x)
    sig2 = [(0.2 * a_) ** 2 for a_ in x]
    true_v.append(sum((a_ - mx_) ** 2 * s2 for a_, s2 in zip(x, sig2)) / sxx ** 2)
    rss = sum(s2 * (1 - 1 / 50 - (a_ - mx_) ** 2 / sxx) for a_, s2 in zip(x, sig2))
    rep_v.append(rss / 48 / sxx)
two(sd_s, sqrt(sum(true_v) / len(true_v)), 0.002, 'true spread of the slope')
two(rep, sqrt(sum(rep_v) / len(rep_v)), 0.002, 'reported standard error (route B is the root of the mean variance)')
two(m_s, 0.5, 0.003, 'slope unbiased')
ok(fmt(m_s, 3) == '0.500' and fmt(rep, 3) == '0.057' and fmt(sd_s, 3) == '0.063', f'printed figures {m_s} {rep} {sd_s}')
ok(rep < sd_s, 'claim: the usual error misstates (understates) the spread')
choice(S, 'rg-diagnostics-fanning-residuals', 'stays unbiased')
stated(S, 'rg-diagnostics-fanning-residuals', 'slopes average 0.500 for a true 0.5')
stated(S, 'rg-diagnostics-fanning-residuals', 'averages 0.057, against a true spread of 0.063')

# rg-multiple-partial-out: residual on residual against the 2 x 2 normal equations
rng = random.Random(7)
n = 20000
x2 = [rng.gauss(0, 1) for _ in range(n)]
x1 = [0.6 * c + rng.gauss(0, 0.8) for c in x2]
y = [2 * a_ + 1.5 * c + rng.gauss(0, 1) for a_, c in zip(x1, x2)]
_, _, ry = ols(x2, y)
_, _, r1 = ols(x2, x1)
fwl = ols(r1, ry)[0]
c1 = [v - sum(x1) / n for v in x1]
c2 = [v - sum(x2) / n for v in x2]
cy = [v - sum(y) / n for v in y]
s11, s22, s12 = sum(v * v for v in c1), sum(v * v for v in c2), sum(u * v for u, v in zip(c1, c2))
s1y, s2y = sum(u * v for u, v in zip(c1, cy)), sum(u * v for u, v in zip(c2, cy))
full = (s22 * s1y - s12 * s2y) / (s11 * s22 - s12 * s12)
two(fwl, full, 1e-9, 'Frisch-Waugh-Lovell equals the full regression')
simple = ols(x1, y)[0]
raw = ols(x1, ry)[0]                     # residual of y on x2 against the raw x1
avg = (simple + ols(x2, y)[0]) / 2
ok(fmt(fwl, 3) == '1.981' and fmt(simple, 3) == '2.888', f'printed figures {fwl} {simple}')
ok(min(abs(simple - full), abs(raw - full), abs(avg - full)) > 0.1, f'each distractor recipe misses: {simple} {raw} {avg}')
choice(S, 'rg-multiple-partial-out', 'residual on residual')
stated(S, 'rg-multiple-partial-out', 'both give 1.981')
stated(S, 'rg-multiple-partial-out', 'gives 2.888')

# ts-forecast-half-life: logs against a bisection on 0.75^k = 0.5
a = log(0.5) / log(0.75)
lo, hi = 0.0, 10.0
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 0.75 ** mid > 0.5 else (lo, mid)
key = two(a, lo, 1e-9, 'half-life')
numeric(S, 'ts-forecast-half-life', key, 1, {'linear-decay': F(1, 2) / F(1, 4), 'time-scale': 1 / (1 - F(3, 4))})
ok(fmt(a, 2) == '2.41' and round(0.75 ** 2 * 100) == 56 and round(0.75 ** 3 * 100) == 42, 'stated 2.41, 56% and 42%')

# ts-acf-noise-band: 1.96/sqrt(n) against a seeded simulation of lag-1 autocorrelations of white noise
a = 1.96 / sqrt(400)
rng = random.Random(3)
rs = []
for _ in range(4000):
    z = [rng.gauss(0, 1) for _ in range(400)]
    mz = sum(z) / 400
    rs.append(sum((z[t] - mz) * (z[t + 1] - mz) for t in range(399)) / sum((v - mz) ** 2 for v in z))
sd_r = sqrt(sum(r * r for r in rs) / len(rs))
key = two(a, 1.96 * sd_r, 0.004, 'noise band (simulation tolerance 0.004)')
numeric(S, 'ts-acf-noise-band', key, 3, {'no-multiplier': 1 / sqrt(400), 'divided-by-n': 1.96 / 400})

# equicorrelation-many-assets-vol: the equicorrelation formula against the full 25 x 25 double sum
n = 25
a = sqrt(F(4, 100) * (F(1, n) + (1 - F(1, n)) * F(1, 4)))
b = sqrt(sum((1 / n) * (1 / n) * 0.04 * (1 if i == j else 0.25) for i in range(n) for j in range(n)))
key = two(a, b, 1e-12, 'portfolio vol')
numeric(S, 'equicorrelation-many-assets-vol', key, 1, {'independent': sqrt(0.04 / n), 'many-asset-limit': sqrt(0.04 * 0.25)})
ok(F(4, 100) * (F(4, 100) + F(96, 100) * F(1, 4)) == F(112, 10000), 'variance 0.0112')

# ---------------------------------------------------------------- finance-3
# fi-interest-loan-payment: annuity formula against amortising the balance year by year
a = 10000 * 0.1 / (1 - 1.1 ** -3)
bal_pay = lambda p: ((10000 * 1.1 - p) * 1.1 - p) * 1.1 - p
lo, hi = 0.0, 10000.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if bal_pay(mid) > 0 else (lo, mid)
key = two(a, lo, 1e-6, 'loan payment')
numeric(FI, 'fi-interest-loan-payment', key, 2, {'simple-interest': 10000 * 1.3 / 3, 'no-interest': 10000 / 3})
ok(abs(bal_pay(a)) < 1e-6, 'balance ends at zero')
ok(fmt(1 / 1.1 + 1 / 1.1 ** 2 + 1 / 1.1 ** 3, 4) == '2.4869', 'annuity factor 2.4869')

# fi-bonds-three-year-coupon: Fraction sum against a backward loop
cfs = [6, 6, 106]
a = sum(F(c) / F(104, 100) ** (t + 1) for t, c in enumerate(cfs))
v = 0.0
for c in reversed(cfs):
    v = (v + c) / 1.04
key = two(a, v, 1e-9, 'bond price')
numeric(FI, 'fi-bonds-three-year-coupon', key, 2, {'par': 100, 'not-discounted': sum(cfs)})
ok([fmt(c / 1.04 ** (t + 1), 3) for t, c in enumerate(cfs)] == ['5.769', '5.547', '94.234'], 'stated parts')

# fi-bonds-pound-per-basis-point: duration rule against a finite difference of a price with that duration
a = F(98, 100) * 10_000_000 * F(45, 10) * F(1, 10000)
price = lambda dy: 9_800_000 * exp(-4.5 * dy)          # a price whose modified duration is 4.5 at dy = 0
b = (price(-0.00005) - price(0.00005)) / 0.0001 * 0.0001
key = two(a, b, 0.01, 'loss per basis point')
numeric(FI, 'fi-bonds-pound-per-basis-point', int(a), None, {'face-not-price': 10_000_000 * 4.5 * 0.0001, 'ten-basis-points': 9_800_000 * 4.5 * 0.001})

# fi-forwards-geared-loss: balance sheet against the gearing identity r_e = r_a + (D/E)(r_a - r_d)
a = (F(200000) * F(9, 10) - F(100000) * F(104, 100) - 100000) / 100000
b = -0.10 + (100000 / 100000) * (-0.10 - 0.04)
key = two(a, b, 1e-12, 'geared return')
numeric(FI, 'fi-forwards-geared-loss', key, 0, {'no-interest': 2 * F(-1, 10), 'no-gearing': F(-1, 10), 'sign': -key})

# fi-forwards-currency-forward: covered interest parity against a round trip of 1 pound
a = F(125, 100) * F(105, 100) / F(103, 100)
b = (1.25 * 1.05) / (1 * 1.03)
key = two(a, b, 1e-12, 'currency forward')
numeric(FI, 'fi-forwards-currency-forward', key, 4, {'rates-swapped': 1.25 * 1.03 / 1.05, 'added-gap': 1.25 * (1 + 0.05 - 0.03)})
stated(FI, 'fi-forwards-currency-forward', '1.3125/1.03 \\\\approx 1.2743')

# op-payoff-short-strangle-loss: premiums less payoffs, against a scan of the payoff
sp = lambda s: 2.20 + 1.80 - max(95 - s, 0) - max(s - 105, 0)
a = F(220 + 180, 100) - (95 - 88)
key = two(a, sp(88), 1e-12, 'strangle P&L at 88')
numeric(FI, 'op-payoff-short-strangle-loss', int(key), None, {'no-premium': -(95 - 88), 'premium-only': 4})

# op-strategies-one-by-two-breakeven: closed form against a scan of the expiry payoff
pay = lambda s: max(s - 100, 0) - 2 * max(s - 110, 0) - 5 + 2 * 2.5
a = 110 + 10                                             # peak of 10, falls one for one
scan = [k / 100 for k in range(11001, 20000) if abs(pay(k / 100)) < 1e-9]
two(a, scan[0], 0, 'upper break-even')
ok(pay(115) > 0 and pay(130) < 0, 'payoff falls one for one')
numeric(FI, 'op-strategies-one-by-two-breakeven', a, None, {'peak': 110, 'two-for-one': 110 + 10 / 2})   # falling 2 for 1 from 10 reaches 0 at 115

# op-parity-implied-forward: parity solved for F against a replication check
a = 100 + F(720 - 510, 100) / F(98, 100)
spot = 7.20 - 5.10 + 100 * 0.98
key = two(a, spot / 0.98, 1e-9, 'implied forward')
numeric(FI, 'op-parity-implied-forward', key, 2, {'not-compounded': 100 + 2.10, 'gave-spot': spot})
ok(fmt(2.10 / 0.98, 4) == '2.1429', 'gap 2.1429')

# op-greeks-vol-move-pnl: vega rule against a finite repricing with a linear-in-vol price
a = 50 * 100 * F(12, 100) * 3
val = lambda vol: 50 * 100 * 0.12 * vol                  # vega is the slope in vol points
key = two(a, val(21) - val(18), 1e-9, 'vega P&L')
numeric(FI, 'op-greeks-vol-move-pnl', int(a), None, {'no-multiplier': 50 * 0.12 * 3, 'one-point': 50 * 100 * 0.12, 'one-contract': 100 * 0.12 * 3})


def bs(S0, K, T, r, sig):
    d1 = (log(S0 / K) + (r + sig * sig / 2) * T) / (sig * sqrt(T))
    return S0 * N.cdf(d1) - K * exp(-r * T) * N.cdf(d1 - sig * sqrt(T))


# tp-bs-at-the-money-delta: N(d1) against a finite difference of the Black-Scholes price
a = N.cdf(0.4 * 1 / 2)
b = (bs(100.001, 100, 1, 0, 0.4) - bs(99.999, 100, 1, 0, 0.4)) / 0.002
key = two(a, b, 1e-6, 'delta')
two(a, 0.5 * (1 + erf(0.2 / sqrt(2))), 1e-12, 'N(0.2) by erf')
numeric(FI, 'tp-bs-at-the-money-delta', key, 2, {'one-half': 0.5, 'used-d2': N.cdf(-0.2)})

# tp-riskneutral-analyst-view: risk-neutral price against replication with shares and cash
q = F(100 - 80, 130 - 80)
a = (1 - q) * 20
delta = F(0 - 20, 130 - 80)                              # shares held to replicate the put
cash = 20 - delta * 80
two(a, delta * 100 + cash, 0, 'put price by replication')
ok(a == 12 and F(4, 10) * 20 == 8 and F(1, 2) * 20 == 10, 'option values 12, 8, 10, 20')
choice(FI, 'tp-riskneutral-analyst-view', '£12')

# tp-multistep-monthly-up-factor: exp against its power series
x = 0.3 * sqrt(1 / 12)
a = exp(x)
b = sum(x ** k / math.factorial(k) for k in range(20))
key = two(a, b, 1e-14, 'up factor')
numeric(FI, 'tp-multistep-monthly-up-factor', key, 4, {'no-root': exp(0.3 / 12), 'no-time-step': exp(0.3)})
ok(fmt(sqrt(1 / 12), 4) == '0.2887' and fmt(0.3 * 0.2887, 4) == '0.0866' and fmt(exp(0.0866), 4) == '1.0905', 'stated steps')

# ms-book-who-gets-filled: priority rule against a share-by-share matching loop


def fill(book, qty, key):
    got = {}
    for name, size, px, t in sorted(book, key=key):
        take = min(size, qty)
        got[name] = take
        qty -= take
    return got


book = [('A', 200, 50.00, 900), ('B', 300, 50.00, 901), ('C', 100, 50.01, 902)]
a = fill(book, 450, lambda o: (-o[2], o[3]))['B']
left = {'A': 200, 'B': 300, 'C': 100}
got = {'A': 0, 'B': 0, 'C': 0}
for _ in range(450):                                      # one share at a time to the best bid, earliest first
    best = max((o for o in book if left[o[0]] > 0), key=lambda o: (o[2], -o[3]))
    left[best[0]] -= 1
    got[best[0]] += 1
two(a, got['B'], 0, 'shares B buys')
numeric(FI, 'ms-book-who-gets-filled', a, None, {'time-first': fill(book, 450, lambda o: o[3])['B'], 'filled-in-full': 300})

# ms-costs-shortfall-with-unfilled: Fraction against a paper-portfolio comparison
a = 6000 * (F(2506, 100) - 25) + 4000 * (F(2520, 100) - 25) + 30
paper = 10000 * (25.20 - 25.00)
real = 6000 * (25.20 - 25.06) - 30
key = two(a, paper - real, 1e-6, 'implementation shortfall')
numeric(FI, 'ms-costs-shortfall-with-unfilled', int(a), None, {'filled-only': 6000 * F(6, 100) + 30, 'no-commission': a - 30})

# tp-bs-vega-rule: S N'(d1) sqrt(T) against a finite difference in vol, and the 0.4 rule
a = 100 * N.pdf(0.2 * 0.5 / 2) * 0.5 / 100
b = (bs(100, 100, 0.25, 0, 0.2001) - bs(100, 100, 0.25, 0, 0.1999)) / 0.0002 / 100
key = two(a, b, 1e-6, 'vega per vol point')
rule = F(4, 10) * 100 * F(1, 2) / 100
ok(abs(float(rule) - key) < 0.005, 'the 0.4 rule sits inside the key band')
numeric(FI, 'tp-bs-vega-rule', key, 2, {'no-time': F(4, 10) * 100 / 100, 'used-t': F(4, 10) * 100 * F(1, 4) / 100})
ok(fmt(key, 4) == '0.1992', 'exact 0.1992')

# ---------------------------------------------------------------- behavioural-7 (rule 11)
for it in DATA[B]['items']:
    w = it['widget']
    lab = f'{B}/{it["id"]}'
    ok(w['kind'] == 'longform' and 'prose' not in it, f'{lab}: longform, no prose')
    words = len(w['model'].split())
    ok(120 <= words <= 180, f'{lab}: model {words} words')
    ok([r['points'] for r in w['rubric']] == [2, 2, 2, 2, 1, 1], f'{lab}: rubric 2,2,2,2,1,1')
    q = it['question']
    ok(q.startswith('Answer aloud, then type it: ') and 3 <= len(q.split(': ', 1)[1].split()) <= 6 and q.endswith('.'), f'{lab}: question line')
    txt = (w['prompt'] + ' ' + ' '.join(r['text'] for r in w['rubric'])).lower()
    if 'two minutes' in txt:
        ok(it['pace'] == 120, f'{lab}: pace 120 for two minutes')
    if 'ninety seconds' in txt:
        ok(it['pace'] == 90, f'{lab}: pace 90 for ninety seconds')
    ok(it['feedback'] == {'correct': 'Compare your answer with the model and tick the rubric.', 'generic': 'Open the model answer and mark each rubric line.'}, f'{lab}: feedback lines')
qs = [it['question'] for it in DATA[B]['items']]
ok(len(set(qs)) == len(qs), 'behavioural question lines are distinct')
backtests = sum('backtest' in it['widget']['model'].lower() for it in DATA[B]['items'])
ok(backtests <= 1, f'at most one backtest story ({backtests})')

# ---------------------------------------------------------------- coding helpers (code items, rule 12; reading items, rule 13)
import io, contextlib, subprocess, tempfile, time, shutil


def code_cases(it):
    w = it['widget']
    return w['examples'], w['tests']


def run_case(ns_src, c, impl=None, name=None):
    """Run one case as the bank harness does: exec setup, eval call, eval expect, compare with ==. Returns (passed, seconds)."""
    ns = {}
    t0 = time.perf_counter()
    try:
        if impl is not None:
            ns[name] = impl
        else:
            exec(ns_src, ns)
        if c.get('setup'):
            exec(c['setup'], ns)
        a = eval(c['call'], ns)
        e = eval(c['expect'], ns)
        good = (a == e)
    except Exception:
        good = False
    return bool(good), time.perf_counter() - t0


def slow_case(src, c, limit=5.0):
    """Run one case of src in a fresh CPython with a time limit: 'timeout', 'wrong' or 'pass'."""
    prog = src + '\n' + (c.get('setup') or '') + f'\nimport sys\nsys.exit(0 if ({c["call"]}) == ({c["expect"]}) else 3)\n'
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False) as fh:
        fh.write(prog)
        path = fh.name
    try:
        r = subprocess.run([sys.executable, path], timeout=limit, capture_output=True)
        return 'pass' if r.returncode == 0 else 'wrong'
    except subprocess.TimeoutExpired:
        return 'timeout'
    finally:
        os.unlink(path)


def code_item(f, i, fn, brute, traps, slow_traps=(), expect_count=None):
    """solution passes every example and test (each under 1 s in CPython), the untouched starter fails, the brute-force twin
    agrees with every stated expect, each named trap fails at least one hidden test; slow traps time out (5 s) on a named test."""
    it = item(f, i)
    lab = f'{f}/{i}'
    w = it['widget']
    ok(w['kind'] == 'code' and w.get('language', 'python') == 'python', f'{lab}: Python code item')
    ok(w['starter'].strip().endswith('...') and w['starter'].startswith(f'def {fn}('), f'{lab}: starter is the signature with ...')
    ok(it['question'] == f'Complete `{fn}`.' and f'`{fn}(' in it['prose'], f'{lab}: question and worked call in prose')
    ok(240 <= it['pace'] <= 480, f'{lab}: pace 240 to 480')
    ex, ts = code_cases(it)
    ok(len(ex) == 2 and 6 <= len(ts) <= 10, f'{lab}: 2 examples, 6 to 10 tests ({len(ts)})')
    ok(all(c.get('compare') == 'equal' for c in ex + ts), f'{lab}: compare equal')
    m = re.match(r'Submit runs (\d+) hidden tests\. Each result must equal the expected (whole number|value)\.$', w['how'])
    ok(m and int(m.group(1)) == len(ts), f'{lab}: how line counts {len(ts)} tests')
    for c in ex + ts:
        good, secs = run_case(w['solution'], c)
        ok(good, f'{lab}: solution passes {c["call"]}')
        ok(secs < 1.0, f'{lab}: solution under 1 s on {c["call"]} ({secs:.3f} s)')
        ok(run_case(None, c, impl=brute, name=fn)[0], f'{lab}: brute-force twin agrees on {c["call"]} = {c["expect"]}')
    for c in ex:
        ok(any(c['call'] == t['call'] for t in ts), f'{lab}: example {c["call"]} is also a hidden test')
    ok(not all(run_case(w['starter'], c)[0] for c in ts), f'{lab}: untouched starter fails')
    ok(sum(not run_case(w['starter'], c)[0] for c in ts) >= 1, f'{lab}: starter fails at least one test')
    for name, src in traps.items():
        failed = [c['call'] for c in ts if not run_case(src, c)[0]]
        ok(failed, f'{lab}: trap "{name}" fails a hidden test')
        print(f'  trap {lab} "{name}" fails {len(failed)} of {len(ts)}: {failed[0][:70] if failed else "NONE"}')
    for name, src, call in slow_traps:
        c = next(t for t in ts if t['call'] == call)
        small = [t for t in ts if t is not c and not t.get('setup') and len(t['call']) < 60 and '**' not in t['call'] and ' * ' not in t['call']]
        ok(all(run_case(src, t)[0] for t in small), f'{lab}: slow trap "{name}" is right on the small tests')
        res = slow_case(src, c)
        ok(res == 'timeout', f'{lab}: slow trap "{name}" runs past 5 s on {call} ({res})')
        print(f'  slow trap {lab} "{name}" right on {len(small)} small tests, {res} at 5 s on {call[:70]}')
    return it


def run_prose(it, lang='python'):
    """Execute the fenced block of a reading item and return what it prints."""
    m = re.search(r'```' + lang + r'\n(.*?)```', it['prose'], re.S)
    ok(m is not None, f'{it["id"]}: fenced {lang} block')
    body = m.group(1)
    ok(len(body.strip('\n').split('\n')) <= 8, f'{it["id"]}: at most eight lines of code')
    buf = io.StringIO()
    if lang == 'python':
        with contextlib.redirect_stdout(buf):
            exec(body, {})
    return body, buf.getvalue().strip()


def cpp_run(src):
    """Compile and run a C++ program with g++ -std=c++20; returns stdout, or None (with a printed warning) when no compiler."""
    cxx = shutil.which('g++') or shutil.which('clang++')
    if not cxx:
        print('WARNING: no C++ compiler, C++ check skipped (not a pass)')
        return None
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'a.cpp')
    open(p, 'w').write(src)
    r = subprocess.run([cxx, '-std=c++20', '-O0', p, '-o', os.path.join(d, 'a.out')], capture_output=True, text=True)
    ok(r.returncode == 0, f'C++ compiles: {r.stderr[:200]}')
    out = subprocess.run([os.path.join(d, 'a.out')], capture_output=True, text=True).stdout.strip()
    shutil.rmtree(d)
    return out


def cpp_compiles(src):
    cxx = shutil.which('g++') or shutil.which('clang++')
    if not cxx:
        print('WARNING: no C++ compiler, C++ check skipped (not a pass)')
        return None
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'a.cpp')
    open(p, 'w').write(src)
    r = subprocess.run([cxx, '-std=c++20', '-fsyntax-only', p], capture_output=True, text=True)
    shutil.rmtree(d)
    return r.returncode == 0


# ---------------------------------------------------------------- coding-3
C = 'coding-3'
from collections import Counter
from itertools import combinations


# pf-idioms-trend-direction. Brute: the set of signs of every difference.
def trend_brute(xs):
    signs = set()
    for i in range(1, len(xs)):
        d = xs[i] - xs[i - 1]
        signs.add((d > 0) - (d < 0))
    return 1 if signs == {1} else -1 if signs == {-1} else 0


code_item(C, 'pf-idioms-trend-direction', 'trend', trend_brute, {
    'first against last': 'def trend(xs):\n    if len(xs) < 2:\n        return 0\n    return (xs[-1] > xs[0]) - (xs[-1] < xs[0])\n',
    'not strict (<= and >=)': 'def trend(xs):\n    p = list(zip(xs, xs[1:]))\n    if not p:\n        return 0\n    if all(a <= b for a, b in p):\n        return 1\n    if all(a >= b for a, b in p):\n        return -1\n    return 0\n'})


# at-sort-largest-gap. Brute: pop values off a heap one at a time (no call to sorted).
def gap_brute(xs):
    import heapq
    h = list(xs)
    heapq.heapify(h)
    best, prev = 0, None
    while h:
        v = heapq.heappop(h)
        if prev is not None:
            best = max(best, v - prev)
        prev = v
    return best


ok(gap_brute([10, 3, 8, 20]) == 10 and gap_brute([1, 1, 50, 50]) == 49, 'heap twin sanity')
code_item(C, 'at-sort-largest-gap', 'largest_gap', gap_brute, {
    'gaps in input order': 'def largest_gap(xs):\n    return max((abs(b - a) for a, b in zip(xs, xs[1:])), default=0)\n',
    'max less min': 'def largest_gap(xs):\n    return max(xs) - min(xs) if xs else 0\n'})
ok(abs(3 - 10) == 7 and abs(8 - 3) == 5 and abs(20 - 8) == 12, 'explain: input-order gaps 7, 5, 12')


# at-greedy-orders-to-fill. Brute: every subset, smallest size first (small cases); a heap of the largest (all cases).
def fill_brute(sizes, target):
    if target <= 0:
        return 0
    if len(sizes) <= 12:
        for k in range(1, len(sizes) + 1):
            if any(sum(c) >= target for c in combinations(sizes, k)):
                return k
        return -1
    import heapq
    h = [-s for s in sizes]
    heapq.heapify(h)
    got, k = 0, 0
    while h and got < target:
        got -= heapq.heappop(h)
        k += 1
    return k if got >= target else -1


code_item(C, 'at-greedy-orders-to-fill', 'orders_to_fill', fill_brute, {
    'input order': 'def orders_to_fill(sizes, target):\n    if target <= 0:\n        return 0\n    s = 0\n    for k, x in enumerate(sizes, 1):\n        s += x\n        if s >= target:\n            return k\n    return -1\n',
    'strict: total above the target': 'def orders_to_fill(sizes, target):\n    if target <= 0:\n        return 0\n    s = 0\n    for k, x in enumerate(sorted(sizes, reverse=True), 1):\n        s += x\n        if s > target:\n            return k\n    return -1\n'})
ok(200 + 50 + 400 >= 450 and 200 + 50 < 450 and 400 + 200 >= 450 and 400 < 450, 'input order takes 3, largest first takes 2')


# at-search-count-in-range. Brute: a Counter over every whole number in the range (no halving).
def range_brute(xs, lo, hi):
    if hi < lo:
        return 0
    c = Counter(xs)
    if hi - lo <= 2 * len(c):
        return sum(c[v] for v in range(lo, hi + 1))
    return sum(n for v, n in c.items() if lo <= v <= hi)


BIG = 'sum(count_in_range(xs, k, k + 10) for k in range(0, 2000000, 2000))'
code_item(C, 'at-search-count-in-range', 'count_in_range', range_brute, {
    'no guard for hi below lo': 'from bisect import bisect_left, bisect_right\ndef count_in_range(xs, lo, hi):\n    return bisect_right(xs, hi) - bisect_left(xs, lo)\n',
}, slow_traps=[('linear scan, O(n) per call', 'def count_in_range(xs, lo, hi):\n    return sum(1 for x in xs if lo <= x <= hi)\n', BIG)])
from bisect import bisect_left as _bl, bisect_right as _br
ok(_br([1, 3, 3, 5, 8, 8, 9], 2) - _bl([1, 3, 3, 5, 8, 8, 9], 9) == -5, 'trap value: -5 for (9, 2)')
two(len(range(6, 1000001, 2)), (1000000 - 6) // 2 + 1, 0, 'evens from 6 to 1,000,000: 499,998')
two(sum(len(range(k, k + 11, 2)) for k in range(0, 2000000, 2000)), 1000 * 6, 0, '1,000 windows of 6 evens')


# simulation-rules-clip-position. Brute: fill one share at a time while the limit holds.
def clip_brute(orders, limit):
    pos, out = 0, []
    for q in orders:
        step = 1 if q > 0 else -1
        done = 0
        for _ in range(abs(q)):
            if abs(pos + step) > limit:
                break
            pos += step
            done += step
        out.append(done)
    return out


code_item(C, 'simulation-rules-clip-position', 'apply_orders', clip_brute, {
    'reject a breaching order whole': 'def apply_orders(orders, limit):\n    pos, out = 0, []\n    for q in orders:\n        if abs(pos + q) <= limit:\n            pos += q\n            out.append(q)\n        else:\n            out.append(0)\n    return out\n',
    'clip the long side only': 'def apply_orders(orders, limit):\n    pos, out = 0, []\n    for q in orders:\n        new = min(limit, pos + q)\n        out.append(new - pos)\n        pos = new\n    return out\n'})
ok(clip_brute([6, 7, -20, 3], 10) == [6, 4, -20, 3], 'prose example')
ns = {}
exec('def apply_orders(orders, limit):\n    pos, out = 0, []\n    for q in orders:\n        if abs(pos + q) <= limit:\n            pos += q\n            out.append(q)\n        else:\n            out.append(0)\n    return out\n', ns)
ok(ns['apply_orders']([6, 7, -20, 3], 10) == [6, 0, 0, 3], 'brief trap value [6, 0, 0, 3]')


# at-recursion-depth-weighted-sum. Brute: read the repr character by character, tracking bracket depth.
def depth_brute(x):
    s, d, total, i = repr(x), 0, 0, 0
    while i < len(s):
        ch = s[i]
        if ch == '[':
            d += 1
        elif ch == ']':
            d -= 1
        elif ch == '-' or ch.isdigit():
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            total += int(s[i:j]) * d
            i = j
            continue
        i += 1
    return total


code_item(C, 'at-recursion-depth-weighted-sum', 'depth_sum', depth_brute, {
    'plain sum': 'def depth_sum(x):\n    return sum(depth_sum(v) if isinstance(v, list) else v for v in x)\n',
    'top list at depth 0': 'def depth_sum(x, d=0):\n    return sum(depth_sum(v, d + 1) if isinstance(v, list) else v * d for v in x)\n'})
two(1 + 2 * (2 + 3) + 3 * 4, depth_brute([1, [2, 3], [[4]]]), 0, 'depth sum 23')
two(5 - 2 + 6 + 12, depth_brute([5, [-1, [2, [3]]]]), 0, 'depth sum 21')
ok(1 + 2 + 3 + 4 == 10 and 5 - 1 + 2 + 3 == 9, 'plain sums 10 and 9')
two(7 * 200, depth_brute(__import__('functools').reduce(lambda a, _: [a], range(199), [7])), 0, 'deep test: 7 at depth 200')
two(500500 + 2 * 1000, sum(range(1, 1001)) + 2000, 0, 'wide test 502,500')
ok(200 < 300, 'deep test stays under the 300-call limit for a generator in each call (AUTHORING Deep recursion)')

# pf-idioms-stable-ties: run the lines; slips by carrying them out
it = choice(C, 'pf-idioms-stable-ties', "['c', 'b', 'a']")
body, out = run_prose(it)
ok(out == "['c', 'b', 'a']", f'stable ties prints {out}')
pairs = [("b", 2), ("a", 2), ("c", 1)]
ok([t[0] for t in sorted(pairs, key=lambda t: (t[1], t[0]))] == ['c', 'a', 'b'], 'slip: tie broken by letter')
ok([t[0] for t in sorted(pairs)] == ['a', 'b', 'c'], 'slip: sorted by letter')
ok([t[0] for t in pairs] == ['b', 'a', 'c'], 'slip: input order')
texts = {o['text'] for o in it['widget']['options']}
ok(texts == {"['c', 'b', 'a']", "['c', 'a', 'b']", "['a', 'b', 'c']", "['b', 'a', 'c']"}, 'stable ties option texts')

# at-search-stuck-loop: run with a step cap
it = choice(C, 'at-search-stuck-loop', 'never ends')
m = re.search(r'```python\n(.*?)```', it['prose'], re.S)
ok(len(m.group(1).strip('\n').split('\n')) <= 8, 'stuck loop: at most eight lines')


def trace(xs, x, le=False, cap=50):
    lo, hi = 0, len(xs)
    seen = []
    for _ in range(cap):
        if not (lo <= hi if le else lo < hi):
            return 'ended', seen
        mid = (lo + hi) // 2
        if mid >= len(xs):
            return 'index error', seen
        if xs[mid] < x:
            lo = mid
        else:
            hi = mid
        seen.append((lo, hi, mid))
    return 'stuck', seen


st, seen = trace([1, 3, 5, 7], 6)
ok(st == 'stuck' and seen[:3] == [(2, 4, 2), (2, 3, 3), (2, 3, 2)] and seen[-1] == (2, 3, 2), f'stuck at lo 2, hi 3: {seen[:3]}')
st2, seen2 = trace([1, 3, 5, 7], 6, le=True)
ok(st2 == 'stuck' and seen2[-1][0] == 2, f'with lo <= hi still stuck at lo 2 ({st2})')
ok((2 + 3) // 2 == 2, 'explain: mid (2 + 3) // 2 = 2')
ok(isinstance(10 ** 40 + 10 ** 40, int), 'Python ints do not overflow')
lo, hi = 0, 4
while lo < hi:                                          # with lo = mid + 1 the search ends at the insertion point
    mid = (lo + hi) // 2
    if [1, 3, 5, 7][mid] < 6:
        lo = mid + 1
    else:
        hi = mid
ok(lo == 3, 'fixed search ends at index 3')

# ds-stacks-push-pop-trace
it = item(C, 'ds-stacks-push-pop-trace')
body, out = run_prose(it)
key = int(out)
pushes = [3, 5, None, 2, 7, None, None]
from collections import deque
q, popped = deque(), []
for p in pushes:                                         # slip: pop from the front
    if p is None:
        popped.append(q.popleft())
    else:
        q.append(p)
two(key, 5 + 7 + 2, 0, 'stack pops 14')
numeric(C, 'ds-stacks-push-pop-trace', key, None, {'from-front': sum(popped), 'every-value': 3 + 5 + 2 + 7, 'two-pops': 5 + 7})
ok(popped == [3, 5, 2], 'queue order 3, 5, 2')

# gd-dp-table-size
it = item(C, 'gd-dp-table-size')
body, out = run_prose(it)
two(int(out), (6 + 1) * (9 + 1), 0, 'LCS table 70 cells')
ok(len('MARKET') == 6 and len('SPREADING') == 9, 'lengths 6 and 9')
numeric(C, 'gd-dp-table-size', int(out), None, {'no-empty-prefix': 6 * 9, 'added-lengths': 6 + 9, 'added-padded': 7 + 10})

# np-broadcast-column-plus-row: NumPy if present, and a hand broadcast
it = item(C, 'np-broadcast-column-plus-row')
try:
    import numpy
    body, out = run_prose(it)
    npv = int(out)
except ImportError:
    print('WARNING: NumPy missing; broadcast checked by hand only')
    npv = None
A_, B_ = [1, 2, 3], [10, 20, 30, 40]
hand = sum(a + b for a in A_ for b in B_)
if npv is not None:
    two(npv, hand, 0, 'broadcast sum: NumPy against the double loop')
two(hand, 4 * 6 + 3 * 100, 0, 'broadcast sum 324')
numeric(C, 'np-broadcast-column-plus-row', hand, None,
        {'added-sums': sum(A_) + sum(B_), 'swapped-counts': 3 * sum(A_) + 4 * sum(B_), 'paired-by-position': sum(a + b for a, b in zip(A_, B_))})
ok(sum(A_) == 6 and sum(B_) == 100 and [a + b for a, b in zip(A_, B_)] == [11, 22, 33], 'byKey figures 6, 100, 11, 22, 33')

# virtual-dispatch-missing-virtual: compile and run, and the virtual variant
it = choice(C, 'virtual-dispatch-missing-virtual', "'B'")
m = re.search(r'```cpp\n(.*?)```', it['prose'], re.S)
snippet = m.group(1)
ok(len(snippet.strip('\n').split('\n')) <= 8, 'virtual: at most eight lines')
decls, stmts = snippet.split('\n\n')
prog = '#include <cstdio>\n' + decls + '\nint main() {\n' + stmts + '\nstd::printf("%c", c);\n}\n'
out = cpp_run(prog)
if out is not None:
    ok(out == 'B', f'C++ non-virtual prints {out}')
    out_v = cpp_run(prog.replace('struct B { char name', 'struct B { virtual char name'))
    ok(out_v == 'D', f'C++ with virtual prints {out_v}')


# ---------------------------------------------------------------- whole-file checks
allids = []
for fn in sorted(os.listdir(BANK)):
    if fn.endswith('.json'):
        allids += [it['id'] for it in json.load(open(os.path.join(BANK, fn), encoding='utf-8'))['items']]
dups = {x for x in allids if allids.count(x) > 1}
ok(not dups, f'item ids unique across the bank ({sorted(dups)})')
for f in FILES:
    ok(DATA[f]['id'] == f, f'{f}: id is the file name')
    for it in DATA[f]['items']:
        ok(('requires' in it) == (it['difficulty'] >= 4), f'{f}/{it["id"]}: requires only at difficulty 4 and 5')
        ok(it['source'] == 'Original' and len(it['tags']) == 1, f'{f}/{it["id"]}: source and one tag')
        ok(it['difficulty'] in (2, 3, 4, 5), f'{f}/{it["id"]}: difficulty 2 to 5')
        blob = json.dumps(it, ensure_ascii=False)
        ok(not re.search(r'\bpercent\b', blob.lower()) and '!' not in blob and '—' not in blob, f'{f}/{it["id"]}: voice (no percent, !, em-dash)')

counts = {f: len(DATA[f]['items']) for f in FILES}
ok(counts == {'statistics-3': 15, 'finance-3': 15, 'behavioural-7': 8, 'coding-3': 12}, f'item counts {counts}')

print(f'{checks[0]} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
