#!/usr/bin/env python3
"""Bank part 2, session 1: every key, slip and stated figure in statistics-1, finance-1 and behavioural-5, by two routes.

Standard library only (runs under plain python3). numbers_lib.py has no Bank loader yet (B2-E4), so the JSON is read here.
Route A is exact (Fraction) or closed form; route B is enumeration, a seeded simulation with a stated tolerance, or a
numerical solve that shares no code with route A. Each value is then asserted at its path in the JSON.
Exit 0 means every check passed.
"""
import json, math, os, random, re, statistics, sys
from fractions import Fraction as F
from math import comb, sqrt, exp, log, erf, erfc, pi
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, '..', '..', 'app', 'content', 'bank')
FILES = ['statistics-1', 'finance-1', 'behavioural-5']
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
    """Route A and route B agree."""
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
    pct = w.get('unit') == '%'
    scale = 100 if pct else 1
    ans, tol = w['answer'], w['tol']['abs']
    lab = f'{f}/{i}'
    ok(abs(ans - key) <= tol, f'{lab}: computed key {key} inside stored band {ans} +- {tol}')
    if asked_dp is not None:
        rounded = round(key * scale, asked_dp) / scale
        ok(abs(rounded - ans) <= tol + 1e-12, f'{lab}: rounded key {rounded} inside band')
        close(ans, key, max(0.5 * 10 ** -asked_dp / scale, 1e-9) * 1.0001 if tol <= 0.5 * 10 ** -asked_dp / scale else tol, f'{lab}: stored answer near exact')
    else:
        ok(float(key) == round(float(key)) and ans == key, f'{lab}: whole-number key {key} stored exactly')
    ids = {x['id']: x for x in w['wrong']}
    ok(set(ids) == set(slips), f'{lab}: wrong ids {sorted(ids)} match computed slips {sorted(slips)}')
    ok(len(ids) >= 2, f'{lab}: at least two wrong entries')
    for wid, v in slips.items():
        x = ids.get(wid)
        if not x:
            continue
        ok(abs(x['value'] - v) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: computed slip {v} inside its band {x["value"]} +- {x["tol"]["abs"]}')
        if asked_dp is not None:
            ok(abs(x['value'] - round(v * scale, asked_dp) / scale) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: slip as rounded inside its band')
        ok(abs(x['value'] - ans) > tol + x['tol']['abs'], f'{lab}.{wid}: band does not touch the key band')
        ok(wid in it['feedback'].get('byKey', {}), f'{lab}.{wid}: byKey line')
    vals = sorted(w['wrong'], key=lambda x: x['value'])
    for a, b in zip(vals, vals[1:]):
        ok(b['value'] - a['value'] > a['tol']['abs'] + b['tol']['abs'], f'{lab}: wrong bands {a["id"]} and {b["id"]} apart')
    return it


def stated(f, i, phrase):
    """A figure computed above is printed in the item (any field)."""
    blob = json.dumps(item(f, i), ensure_ascii=False)
    ok(phrase in blob, f'{f}/{i}: states "{phrase}"')


def fmt(x, dp):
    return f'{x:.{dp}f}'


S, FI, B = 'statistics-1', 'finance-1', 'behavioural-5'

# ---------------------------------------------------------------- statistics-1
# es-mle-waits-between-trades: exponential MLE = n / sum
waits = [4, 9, 2, 7, 5, 3]
a = F(len(waits), sum(waits))
ll = lambda lam: len(waits) * log(lam) - lam * sum(waits)
b = max((k / 100000 for k in range(1, 100000)), key=ll)          # grid search of the log-likelihood
key = two(a, b, 1e-5, 'mle rate')
numeric(S, 'es-mle-waits-between-trades', key, 4, {'mean-wait': F(sum(waits), 6), 'five-gaps': 5 / 30})
two(F(sum(waits), 6), statistics.mean(waits), 1e-12, 'mean wait')
stated(S, 'es-mle-waits-between-trades', '6/30 = 0.2')

# es-biasvar-four-closes
xs = [4, 7, 9, 12]
m = F(sum(xs), 4)
a = sum((x - m) ** 2 for x in xs) / 3
b = sum((x - y) ** 2 for x in xs for y in xs) / (2 * 4 * 3)          # pairwise form of the unbiased variance
key = two(a, b, 1e-12, 'sample variance')
ok(a == F(34, 3), 'variance is 34/3')
two(statistics.variance(xs), a, 1e-12, 'statistics.variance')
numeric(S, 'es-biasvar-four-closes', key, 2, {'divide-by-n': F(34, 4), 'gave-sd': sqrt(34 / 3)})
stated(S, 'es-biasvar-four-closes', '34/3 \\\\approx 11.33')

# es-intervals-halve-the-width
a = F(64) * (F(294, 100) / F(147, 100)) ** 2
s_ = 2.94 * 8 / 1.96
b = next(n for n in range(1, 10000) if abs(1.96 * s_ / sqrt(n) - 1.47) < 1e-9)
key = two(a, b, 0, 'halved width n')
numeric(S, 'es-intervals-halve-the-width', int(key), None, {'doubled-n': 128, 'halved-n': 32})
stated(S, 'es-intervals-halve-the-width', '4 \\\\times 64 = 256')

# es-bayes-seven-in-ten: Beta(2,2) + 7H 3T = Beta(9,5)
a = F(2 + 7, 2 + 2 + 10)
grid = [(k + 0.5) / 200000 for k in range(200000)]
dens = [p ** 8 * (1 - p) ** 4 for p in grid]                        # unnormalised Beta(9,5) density, midpoint rule
b = sum(p * d for p, d in zip(grid, dens)) / sum(dens)
key = two(a, b, 1e-6, 'posterior mean')
numeric(S, 'es-bayes-seven-in-ten', key, 4, {'no-prior': F(7, 10), 'one-each': F(8, 12)})
stated(S, 'es-bayes-seven-in-ten', '9/14 \\\\approx 0.6429')

# ht-pvalue-thirteen-of-sixteen
a = 2 * F(sum(comb(16, k) for k in range(13, 17)), 2 ** 16)
cnt = sum(1 for s in range(2 ** 16) if abs(bin(s).count('1') - 8) >= 5)   # enumerate all 65,536 sequences
b = F(cnt, 2 ** 16)
ok(a == b == F(697, 32768), 'two-sided p = 697/32768 (exact and enumerated)')
one_tail = F(697, 65536)
z = (13 - 8) / sqrt(16 * 0.25)
normal_a = 2 * (1 - N.cdf(z))
normal_b = erfc(z / sqrt(2))
two(normal_a, normal_b, 1e-12, 'normal-curve slip')
numeric(S, 'ht-pvalue-thirteen-of-sixteen', float(a), 4, {'one-tail': one_tail, 'normal-curve': normal_a})
ok([comb(16, k) for k in (13, 14, 15, 16)] == [560, 120, 16, 1], 'binomial terms 560, 120, 16, 1')
stated(S, 'ht-pvalue-thirteen-of-sixteen', '(560 + 120 + 16 + 1)/65536 = 697/65536')
ok(z == 2.5, 'z = 2.5 for the normal slip')

# power-one-sided-shift
se = 12 / sqrt(36)
crit = 1.645 * se
zz = (4 - crit) / se
a = N.cdf(zz)
rng = random.Random(20261111)
reps = 20000
hits = sum(1 for _ in range(reps) if sum(rng.gauss(4, 12) for _ in range(36)) / 36 > crit)
b = hits / reps                                                     # seeded simulation, tolerance 0.01
two(a, b, 0.01, 'power (simulation, tol 0.01)')
two(a, 0.5 * (1 + erf(zz / sqrt(2))), 1e-12, 'power by erf')
two_sided = (1 - N.cdf((1.96 * se - 4) / se)) + N.cdf((-1.96 * se - 4) / se)
numeric(S, 'power-one-sided-shift', a, 4, {'miss-rate': 1 - a, 'two-sided': two_sided})
ok(abs(zz - 0.355) < 1e-9 and abs(crit - 3.29) < 1e-9 and se == 2, 'se 2, line 3.29, z 0.355')
stated(S, 'power-one-sided-shift', '\\\\Phi(0.355) \\\\approx 0.6387')

# multiple-testing-how-many-tests
p2 = 2 * (1 - N.cdf(3.2))
ok(abs(p2 - 0.001374) < 5e-7, f'two-sided p at z = 3.2 is 0.001374 ({p2})')
two(p2, erfc(3.2 / sqrt(2)), 1e-12, 'p by erfc')
pq = 0.001374
a = math.floor(0.05 / pq)
b = max(mm for mm in range(1, 1000) if 0.05 / mm >= pq)            # count up
two(a, b, 0, 'Bonferroni m')
numeric(S, 'multiple-testing-how-many-tests', a, None, {'rounded-up': a + 1, 'one-sided': math.floor(0.05 / (pq / 2))})
ok(0.05 / 37 < pq <= 0.05 / 36, '37 fails and 36 passes')
stated(S, 'multiple-testing-how-many-tests', '36.39')
ok(abs(0.05 / pq - 36.39) < 0.005, '0.05/0.001374 is 36.39 to 2 dp')

# two-regressions-two-slopes
r2 = F(25, 10) * F(1, 10)
ok(F(1, 2) ** 2 == r2, 'r = 1/2 exactly')
rng = random.Random(7)
n = 200000
X = [rng.gauss(0, 1) for _ in range(n)]
Y = [5 * (0.5 * x + sqrt(0.75) * rng.gauss(0, 1)) for x in X]       # sd ratio 5, r 0.5: slopes 2.5 and 0.1
mx, my = sum(X) / n, sum(Y) / n
sxy = sum((x - mx) * (y - my) for x, y in zip(X, Y)); sxx = sum((x - mx) ** 2 for x in X); syy = sum((y - my) ** 2 for y in Y)
two(sxy / sxx, 2.5, 0.02, 'simulated y-on-x slope')
two(sxy / syy, 0.1, 0.002, 'simulated x-on-y slope')
two(sqrt(r2), sxy / sqrt(sxx * syy), 0.005, 'correlation (simulation, tol 0.005)')
numeric(S, 'two-regressions-two-slopes', 0.5, 4, {'no-root': 0.25, 'ratio': 0.1 / 2.5})
stated(S, 'two-regressions-two-slopes', 'r^2 = 2.5 \\\\times 0.1 = 0.25')

# rg-inference-t-from-r-squared
a = sqrt(0.2 * 100 / 0.8)
# route B: build 102 points with R^2 exactly 0.2 and run least squares with its own standard error
rng = random.Random(3)
xv = [rng.gauss(0, 1) for _ in range(102)]
mx = sum(xv) / 102
xc = [x - mx for x in xv]
e = [rng.gauss(0, 1) for _ in range(102)]
me = sum(e) / 102
e = [v - me for v in e]
beta_e = sum(u * v for u, v in zip(xc, e)) / sum(u * u for u in xc)
e = [v - beta_e * u for u, v in zip(xc, e)]                       # residual part orthogonal to x
sx2, se2 = sum(u * u for u in xc), sum(v * v for v in e)
k = sqrt(0.25 * se2 / sx2)                                          # explained/unexplained = 0.2/0.8
yv = [k * u + v for u, v in zip(xc, e)]
bhat = sum(u * v for u, v in zip(xc, yv)) / sx2
res = [v - bhat * u for u, v in zip(xc, yv)]
ss_res = sum(r * r for r in res); ss_tot = sum(v * v for v in yv)
ok(abs(1 - ss_res / ss_tot - 0.2) < 1e-12, 'constructed data has R^2 = 0.2')
b = bhat / sqrt(ss_res / 100 / sx2)
key = two(a, b, 1e-9, 't from R^2')
numeric(S, 'rg-inference-t-from-r-squared', key, 1, {'no-one-minus': sqrt(0.2 * 100), 'no-root': 0.2 * 100 / 0.8})
stated(S, 'rg-inference-t-from-r-squared', '0.2 \\\\times 100 / 0.8 = 25')

# rg-multiple-left-out-factor
a = F(15, 10) + F(-2) * F(4, 10)
rng = random.Random(11)
n = 200000
x1 = [rng.gauss(0, 1) for _ in range(n)]
x2 = [0.4 * u + rng.gauss(0, 1) for u in x1]
yy = [1.5 * u - 2 * v + rng.gauss(0, 1) for u, v in zip(x1, x2)]
m1, my = sum(x1) / n, sum(yy) / n
b = sum((u - m1) * (v - my) for u, v in zip(x1, yy)) / sum((u - m1) ** 2 for u in x1)
key = two(a, b, 0.02, 'omitted-variable slope (simulation, tol 0.02)')
numeric(S, 'rg-multiple-left-out-factor', float(a), 1, {'no-bias': 1.5, 'added-bias': 1.5 + 2 * 0.4})
stated(S, 'rg-multiple-left-out-factor', '1.5 - 0.8 = 0.7')

# ts-models-ar1-long-run-variance
a = F(16) / (1 - F(6, 10) ** 2)
b = sum(16 * 0.36 ** j for j in range(400))                         # MA(infinity) sum of weights squared
key = two(a, b, 1e-9, 'AR(1) variance')
numeric(S, 'ts-models-ar1-long-run-variance', int(a), None, {'unsquared': 16 / 0.4, 'noise-only': 16})
stated(S, 'ts-models-ar1-long-run-variance', '16/0.64 = 25')

# ts-acf-ma1-first-lag
a = F(3, 4) / (1 + F(3, 4) ** 2)
ok(a == F(12, 25), 'MA(1) rho = 12/25')
rng = random.Random(5)
ee = [rng.gauss(0, 1) for _ in range(300001)]
xt = [ee[t] + 0.75 * ee[t - 1] for t in range(1, len(ee))]
mx = sum(xt) / len(xt)
b = sum((xt[t] - mx) * (xt[t - 1] - mx) for t in range(1, len(xt))) / sum((v - mx) ** 2 for v in xt)
two(a, b, 0.01, 'MA(1) lag-1 (simulation, tol 0.01)')
numeric(S, 'ts-acf-ma1-first-lag', float(a), 2, {'coefficient': 0.75, 'unsquared': 0.75 / 1.75})
stated(S, 'ts-acf-ma1-first-lag', '0.75/1.5625 = 0.48')

# sample-size-for-signal-sharpe-years
a = (2 / 0.7) ** 2
lo, hi = 0.0, 100.0
for _ in range(200):                                               # bisection on 0.7 sqrt(T) = 2
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 0.7 * sqrt(mid) < 2 else (lo, mid)
key = two(a, lo, 1e-9, 'Sharpe years')
numeric(S, 'sample-size-for-signal-sharpe-years', key, 1, {'no-square': 2 / 0.7, 'used-1-96': (1.96 / 0.7) ** 2})
stated(S, 'sample-size-for-signal-sharpe-years', '(2/0.7)^2 \\\\approx 8.16')
ok(fmt(a, 2) == '8.16', '8.16 printed')

# correlation-bounds-highest-third
rxy, ryz = 0.28, 0.96
a = rxy * ryz + sqrt((1 - rxy ** 2) * (1 - ryz ** 2))
lo_a = rxy * ryz - sqrt((1 - rxy ** 2) * (1 - ryz ** 2))
det = lambda c: 1 + 2 * rxy * ryz * c - rxy ** 2 - ryz ** 2 - c ** 2
feas = [c / 100000 for c in range(-100000, 100001) if det(c / 100000) >= -1e-12]
b, lo_b = max(feas), min(feas)                                      # grid search on the determinant
two(a, b, 2e-5, 'highest corr(X, Z)')
two(lo_a, lo_b, 2e-5, 'lowest corr(X, Z)')
ok(abs(lo_a) < 1e-12, 'the floor is 0')
ok(abs(sqrt(1 - rxy ** 2) - 0.96) < 1e-12, 'sqrt(1 - 0.28^2) = 0.96')
numeric(S, 'correlation-bounds-highest-third', a, 4, {'product-only': rxy * ryz, 'no-limit': 1})
ok(abs(a - 0.5376) < 1e-12 and abs(rxy * ryz - 0.2688) < 1e-12, '0.2688 + 0.2688 = 0.5376')
stated(S, 'correlation-bounds-highest-third', '0.2688 + 0.2688 = 0.5376')
stated(S, 'correlation-bounds-highest-third', 'the root of 0.9216 times 0.0784')
ok(abs((1 - rxy ** 2) - 0.9216) < 1e-12 and abs((1 - ryz ** 2) - 0.0784) < 1e-12, '0.9216 and 0.0784')
ok(b == max(feas), 'claim: highest (no feasible value above it on the grid)')

# es-estimators-median-standard-error (large-sample)
a = 0.2 * sqrt(pi / 2)
c = 1 / (2 * NormalDist(0, 2).pdf(0) * sqrt(100))                  # 1/(2 f(m) sqrt n) from the density
two(a, c, 1e-12, 'median se from density')
rng = random.Random(2026)
meds = [statistics.median(rng.gauss(0, 2) for _ in range(100)) for _ in range(20000)]
b = statistics.pstdev(meds)                                         # seeded simulation, n = 100, tolerance 0.005
two(a, b, 0.005, 'median se (simulation, tol 0.005)')
numeric(S, 'es-estimators-median-standard-error', a, 3, {'mean-se': 2 / sqrt(100), 'no-root': 0.2 * pi / 2})
stated(S, 'es-estimators-median-standard-error', '0.2\\\\sqrt{\\\\pi/2} \\\\approx 0.251')

# ---------------------------------------------------------------- finance-1
# fi-interest-monthly-to-annual
a = F(201, 200) ** 12 - 1
v = 1.0
for _ in range(12):
    v += v * 0.005
b = v - 1
key = two(a, b, 1e-12, 'effective annual rate')
cont_a = exp(0.06) - 1
cont_b = sum(0.06 ** k / math.factorial(k) for k in range(1, 30))
two(cont_a, cont_b, 1e-12, 'continuous slip')
numeric(FI, 'fi-interest-monthly-to-annual', key, 2, {'continuous': cont_a, 'nominal': 0.06})
ok(fmt(1 + key, 4) == '1.0617', '1.005^12 is 1.0617 to 4 dp')
stated(FI, 'fi-interest-monthly-to-annual', '1.005^{12} \\\\approx 1.0617')

# fi-bonds-duration-move
a = F(-7) * F(25, 10000)
h = 1e-7
P = lambda y: exp(-7 * y)                                           # a bond whose modified duration is 7 (continuous zero)
b = (P(0.03 + h) - P(0.03 - h)) / (2 * h) / P(0.03) * 0.0025
key = two(a, b, 1e-9, 'duration change')
numeric(FI, 'fi-bonds-duration-move', float(a), 2, {'sign': 0.0175, 'basis-points': -7 * 0.025})
stated(FI, 'fi-bonds-duration-move', '-7 \\\\times 0.0025 = -0.0175')

# fi-forwards-six-month-fair
a = 80 * exp(0.025)
b = 80 * (1 + 0.05 / 10 ** 7) ** (10 ** 7 * 0.5)                   # limit of ever finer compounding
key = two(a, b, 1e-4, 'forward')
numeric(FI, 'fi-forwards-six-month-fair', key, 2, {'simple': 80 * 1.025, 'full-year': 80 * exp(0.05)})

# fi-equity-growing-dividend
a = F(3) / (F(9, 100) - F(4, 100))
b = sum(3 / 1.04 * (1.04 / 1.09) ** t for t in range(1, 5000))     # sum the discounted stream
key = two(a, b, 1e-6, 'Gordon price')
numeric(FI, 'fi-equity-growing-dividend', int(a), None, {'no-growth': 3 / 0.09, 'grew-again': 3 * 1.04 / 0.05})
stated(FI, 'fi-equity-growing-dividend', '3/0.05 = 60')


def bs(S0, K, T, r, sig, kind='call'):
    d1 = (log(S0 / K) + (r + sig * sig / 2) * T) / (sig * sqrt(T))
    d2 = d1 - sig * sqrt(T)
    if kind == 'call':
        return S0 * N.cdf(d1) - K * exp(-r * T) * N.cdf(d2)
    return K * exp(-r * T) * N.cdf(-d2) - S0 * N.cdf(-d1)


# op-parity-price-the-put
a = 3.10 - 50 + 52 * exp(-0.02)
lo, hi = 0.01, 2.0
for _ in range(200):                                               # implied vol from the call, then price the put
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if bs(50, 52, 0.5, 0.04, mid) < 3.10 else (lo, mid)
b = bs(50, 52, 0.5, 0.04, lo, 'put')
key = two(a, b, 1e-6, 'put by parity and by Black-Scholes at the implied vol')
numeric(FI, 'op-parity-price-the-put', key, 2, {'undiscounted': 3.10 - 50 + 52, 'signs-swapped': 3.10 + 50 - 52 * exp(-0.02)})
ok(fmt(52 * exp(-0.02), 2) == '50.97', '52e^-0.02 is 50.97')
ok(abs(3.10 - 50 + 50.97 - 4.07) < 1e-9, '3.10 - 50 + 50.97 = 4.07')
stated(FI, 'op-parity-price-the-put', '3.10 - 50 + 50.97 = 4.07')

# op-strategies-bull-spread-breakeven
net = F(6) - F(2)
a = 100 + net
pay = lambda s: max(s - 100, 0) - max(s - 110, 0) - 4
b = next(k / 100 for k in range(9000, 12000) if pay(k / 100) >= 0)  # scan the expiry payoff
two(a, b, 0, 'break-even')
numeric(FI, 'op-strategies-bull-spread-breakeven', int(a), None, {'one-premium': 100 + 6, 'both-premiums': 100 + 6 + 2})
stated(FI, 'op-strategies-bull-spread-breakeven', '6 - 2 = 4')

# op-greeks-second-order-estimate
a = F(4) + F(45, 100) * 2 + F(1, 2) * F(5, 100) * 4
quad = lambda x: 4 + 0.45 * x + 0.025 * x * x                       # the Taylor quadratic, evaluated by steps of 0.001
b = quad(0)
for k in range(2000):
    b += (quad((k + 1) / 1000) - quad(k / 1000))
key = two(a, b, 1e-9, 'delta-gamma estimate')
numeric(FI, 'op-greeks-second-order-estimate', float(a), 2, {'delta-only': 4 + 0.9, 'no-half': 4 + 0.9 + 0.05 * 4})
stated(FI, 'op-greeks-second-order-estimate', '0.45 \\\\times 2 + 0.5 \\\\times 0.05 \\\\times 4 = 1')
stated(FI, 'op-greeks-second-order-estimate', '\\\\tfrac{1}{2} \\\\times 0.05 \\\\times 2^2 = 0.10')

# tp-riskneutral-one-step-with-rate
q = (F(105) - 90) / (120 - 90)
a = q * 15 / F(105, 100)
delta = F(15 - 0, 120 - 90)
bond = (0 - delta * 90) / F(105, 100)
b = delta * 100 + bond                                              # replicate with shares and a loan
ok(a == b, 'risk-neutral price equals replication')
numeric(FI, 'tp-riskneutral-one-step-with-rate', float(a), 2, {'undiscounted': q * 15, 'zero-rate': F(1, 3) * 15})
ok(q == F(1, 2), 'q = 0.5')
stated(FI, 'tp-riskneutral-one-step-with-rate', '0.5 \\\\times 15/1.05 \\\\approx 7.14')

# tp-multistep-american-put-two-step
u, d, R, K = F(11, 10), F(9, 10), F(105, 100), 100
q = (R - d) / (u - d)


def tree(american, disc_root=True):
    vals = [max(K - 100 * u ** j * d ** (2 - j), 0) for j in range(3)]   # j ups after two steps
    for step in (1, 0):
        new = []
        for j in range(step + 1):
            cont = (q * vals[j + 1] + (1 - q) * vals[j])
            if step > 0 or disc_root:
                cont = cont / R
            ex = max(K - 100 * u ** j * d ** (step - j), 0)
            new.append(max(cont, ex) if american else cont)
        vals = new
    return vals[0]


a = tree(True)
# route B: value every exercise policy by enumerating paths with floats, take the best
best = 0.0
for ex_root in (0, 1):
    for ex_up in (0, 1):
        for ex_dn in (0, 1):
            if ex_root:
                val = 0.0
            else:
                val = 0.0
                for m1, p1 in ((1.1, 0.75), (0.9, 0.25)):
                    s1 = 100 * m1
                    if (m1 > 1 and ex_up) or (m1 < 1 and ex_dn):
                        val += p1 * max(100 - s1, 0) / 1.05
                    else:
                        for m2, p2 in ((1.1, 0.75), (0.9, 0.25)):
                            val += p1 * p2 * max(100 - s1 * m2, 0) / 1.05 ** 2
            best = max(best, val)
key = two(a, best, 1e-9, 'American put')
eur = tree(False)
two(eur, (0.75 * 0.25 * 2 * 1 + 0.25 * 0.25 * 19) / 1.05 ** 2, 1e-9, 'European put')
numeric(FI, 'tp-multistep-american-put-two-step', key, 2, {'european': eur, 'root-undiscounted': tree(True, False)})
ok(q == F(3, 4), 'q = 0.75')
ok(fmt((0.75 + 0.25 * 19) / 1.05, 2) == '5.24' and fmt(0.25 / 1.05, 3) == '0.238', 'node values 5.24 and 0.238')
ok(fmt((0.75 * 0.238 + 0.25 * 10) / 1.05, 2) == '2.55', 'root from the rounded node value is 2.55')
stated(FI, 'tp-multistep-american-put-two-step', '(1.05 - 0.9)/0.2 = 0.75')
stated(FI, 'tp-multistep-american-put-two-step', '\\\\approx 5.24')

# ms-book-sweep-four-hundred
book = [(100, F(1001, 100)), (200, F(1002, 100)), (500, F(1004, 100))]
left, cost = 400, F(0)
for qty, px in book:
    take = min(left, qty); cost += take * px; left -= take
a = cost / 400
shares = [px for qty, px in book for _ in range(qty)][:400]          # one share at a time
b = sum(float(p) for p in shares) / 400
key = two(a, b, 1e-9, 'average fill')
numeric(FI, 'ms-book-sweep-four-hundred', float(a), 4, {'unweighted': (10.01 + 10.02 + 10.04) / 3, 'last-price': 10.04})
ok(cost == 4009, 'total cost 4009')
stated(FI, 'ms-book-sweep-four-hundred', '1001 + 2004 + 1004 = 4009')
stated(FI, 'ms-book-sweep-four-hundred', '4009/400 = 10.0225')

# ms-costs-effective-spread
mid = (F(1998, 100) + F(2002, 100)) / 2
a = 2 * (F(2001, 100) - mid) / mid * 10000
b = 2 * abs(20.01 - (19.98 + 20.02) / 2) / ((19.98 + 20.02) / 2) * 1e4
two(a, b, 1e-6, 'effective spread')
numeric(FI, 'ms-costs-effective-spread', int(a), None, {'quoted': (F(2002, 100) - F(1998, 100)) / mid * 10000, 'not-doubled': (F(2001, 100) - mid) / mid * 10000})
stated(FI, 'ms-costs-effective-spread', '0.02/20 = 0.001')


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


# ms-orders-stop-through-a-gap: a definition, checked by a toy matching rule
def stop_fill(trade, stop, limit=None):
    if trade > stop:
        return 'resting'
    if limit is None:
        return trade                       # becomes a market order: fills at the next price
    return trade if trade >= limit else 'resting at limit'


ok(stop_fill(93, 95) == 93 and stop_fill(93, 95, 95) == 'resting at limit', 'stop fills near 93; stop-limit rests')
choice(FI, 'ms-orders-stop-through-a-gap', 'stop-limit rests unfilled')

# greek-signs-calendar-spread: Black-Scholes closed forms against finite differences, r = 0, S = K = 100, vol 20%


def greeks_closed(T, S0=100.0, sig=0.2):
    d1 = sig * sqrt(T) / 2
    ph = N.pdf(d1)
    return ph / (S0 * sig * sqrt(T)), S0 * ph * sqrt(T), -S0 * ph * sig / (2 * sqrt(T))


def greeks_fd(T, S0=100.0, sig=0.2, h=1e-3):
    c = lambda s, v, t: bs(s, 100, t, 0.0, v)
    gam = (c(S0 + h, sig, T) - 2 * c(S0, sig, T) + c(S0 - h, sig, T)) / h ** 2
    veg = (c(S0, sig + 1e-5, T) - c(S0, sig - 1e-5, T)) / 2e-5
    the = -(c(S0, sig, T + 1e-6) - c(S0, sig, T - 1e-6)) / 2e-6
    return gam, veg, the


net_c = [x - y for x, y in zip(greeks_closed(1.0), greeks_closed(0.25))]
net_f = [x - y for x, y in zip(greeks_fd(1.0), greeks_fd(0.25))]
for nm, x, y, t in zip(('gamma', 'vega', 'theta'), net_c, net_f, (1e-4, 1e-3, 1e-3)):
    two(x, y, t, f'calendar net {nm}')
ok(net_c[0] < 0 < net_c[1] and net_c[2] > 0, 'signs: gamma negative, vega positive, theta positive')
ok(fmt(net_c[0], 4) == '-0.0200' and fmt(net_c[1], 2) == '19.77' and fmt(net_c[2], 2) == '4.00', f'net figures {net_c}')
choice(FI, 'greek-signs-calendar-spread', 'Negative gamma, positive vega, positive theta')
stated(FI, 'greek-signs-calendar-spread', 'gamma is -0.0200, vega +19.77 and theta +4.00 a year')

# gv-risk-one-day-var
a = F(3000000) * F(12, 1000) * F(2326, 1000)
b = 3_000_000 * 0.012 * NormalDist(0, 1).inv_cdf(0.99)              # 2.326 is the rounded 99% point
two(a, b, 3000000 * 0.012 * 0.0005, 'VaR with the exact 99% point (within the rounding of 2.326)')
ok(a == 83736, 'VaR 83,736 exactly with 2.326')
numeric(FI, 'gv-risk-one-day-var', int(a), None, {'used-1-645': 3000000 * 0.012 * 1.645, 'ten-day': float(a) * sqrt(10)})
ok(round(float(a) * sqrt(10)) == 264796 and 3000000 * 0.012 == 36000, 'ten-day slip 264,796; sd 36,000')
stated(FI, 'gv-risk-one-day-var', '2.326 \\\\times 36{,}000 = 83{,}736')

# option-estimate-short-dated-call
a = F(4, 10) * 150 * F(32, 100) * F(1, 4)
bsv = bs(150, 150, 1 / 16, 0.0, 0.32)
bsv2 = 150 * erf(0.32 * 0.25 / 2 / sqrt(2))                         # r = 0 at the money: S(2N(d1) - 1)
two(bsv, bsv2, 1e-9, 'Black-Scholes value two ways')
two(a, bsv, 0.02, 'rule of thumb within its band of Black-Scholes')
numeric(FI, 'option-estimate-short-dated-call', float(a), 2, {'no-root': 0.4 * 150 * 0.32 / 16, 'no-time': 0.4 * 150 * 0.32})
ok(fmt(bsv, 2) == '4.79', 'Black-Scholes 4.79')
ok(abs(1 / sqrt(2 * pi) - 0.4) < 0.002, '1/sqrt(2 pi) is about 0.4')
stated(FI, 'option-estimate-short-dated-call', '£4.79')
stated(FI, 'option-estimate-short-dated-call', '0.4 \\\\times 150 \\\\times 0.32 \\\\times 0.25 = 4.8')

# ---------------------------------------------------------------- behavioural-5 (rule 11)
for it in DATA[B]['items']:
    w = it['widget']
    lab = f'{B}/{it["id"]}'
    ok(w['kind'] == 'longform' and 'prose' not in it, f'{lab}: longform, no prose')
    words = len(w['model'].split())
    ok(120 <= words <= 180, f'{lab}: model {words} words')
    ok([r['points'] for r in w['rubric']] == [2, 2, 2, 2, 1, 1], f'{lab}: rubric 2,2,2,2,1,1')
    q = it['question']
    ok(q.startswith('Answer aloud, then type it: ') and 3 <= len(q.split(': ', 1)[1].split()) <= 6, f'{lab}: question line')
    txt = (w['prompt'] + ' ' + ' '.join(r['text'] for r in w['rubric'])).lower()
    if 'two minutes' in txt:
        ok(it['pace'] == 120, f'{lab}: pace 120 for two minutes')
    if 'ninety seconds' in txt:
        ok(it['pace'] == 90, f'{lab}: pace 90 for ninety seconds')
qs = [it['question'] for it in DATA[B]['items']]
ok(len(set(qs)) == len(qs), 'behavioural question lines are distinct')

# ---------------------------------------------------------------- whole-file checks
allids = []
for fn in sorted(os.listdir(BANK)):
    if fn.endswith('.json'):
        allids += [it['id'] for it in json.load(open(os.path.join(BANK, fn), encoding='utf-8'))['items']]
dups = {x for x in allids if allids.count(x) > 1}
ok(not dups, f'item ids unique across the bank ({sorted(dups)})')
for f in FILES:
    for it in DATA[f]['items']:
        ok(('requires' in it) == (it['difficulty'] >= 4), f'{f}/{it["id"]}: requires only at difficulty 4 and 5')
        ok(it['source'] == 'Original' and len(it['tags']) == 1, f'{f}/{it["id"]}: source and one tag')
        ok(it['difficulty'] in (2, 3, 4, 5), f'{f}/{it["id"]}: difficulty 2 to 5')

counts = {f: len(DATA[f]['items']) for f in FILES}
ok(counts == {'statistics-1': 15, 'finance-1': 15, 'behavioural-5': 8}, f'item counts {counts}')

print(f'{checks[0]} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
