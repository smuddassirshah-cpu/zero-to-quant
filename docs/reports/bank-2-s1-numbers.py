#!/usr/bin/env python3
"""Bank part 2, session 1: every key, slip and stated figure in statistics-1, finance-1, behavioural-5 and coding-1, by two routes.

coding-1 uses bank_2_code_check.py (beside this script): each code item's solution, brute-force twin, starter and named
near-miss methods run on its own tests; reasoning items run their own snippet; the C++ item compiles with g++ -std=c++20.

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
FILES = ['statistics-1', 'finance-1', 'behavioural-5', 'coding-1']
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


def stale(f, i, olds):
    """Fix pass: none of the old values or phrases of a re-authored item survives anywhere in it."""
    blob = json.dumps(item(f, i), ensure_ascii=False)
    for o in olds:
        ok(o not in blob, f'{f}/{i}: stale value "{o}" is gone')


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
stated(S, 'es-mle-waits-between-trades', 'You time six gaps between your own fills, in seconds: 4, 9, 2, 7, 5 and 3.')   # delta finding 6
ok(len(waits) == 6 and 'six gaps' in item(S, 'es-mle-waits-between-trades')['prose'], 'es-mle-waits: six gaps are listed and the prose says six gaps, not six fills')
ok(len([4, 9, 2, 7, 5, 3]) == len(re.findall(r'\d+', item(S, 'es-mle-waits-between-trades')['prose'].split('seconds:')[1].split('.')[0])), 'es-mle-waits: the prose lists as many numbers as the six gaps it names')
stale(S, 'es-mle-waits-between-trades', ['quiet share', 'six of your own fills'])

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

# es-bayes-seven-in-ten (fix pass finding 2): Beta(3,1) prior + 7 on time, 3 late = Beta(10,4)
a = F(3 + 7, 3 + 1 + 10)
grid = [(k + 0.5) / 200000 for k in range(200000)]
dens = [p ** 9 * (1 - p) ** 3 for p in grid]                        # unnormalised Beta(10,4) density, midpoint rule
b = sum(p * d for p, d in zip(grid, dens)) / sum(dens)
key = two(a, b, 1e-6, 'posterior mean')
numeric(S, 'es-bayes-seven-in-ten', key, 4, {'no-prior': F(7, 10), 'one-each': F(1 + 7, 2 + 10)})
ok(a == F(5, 7), 'posterior mean is 5/7')
stated(S, 'es-bayes-seven-in-ten', '10/14 \\\\approx 0.7143')
stale(S, 'es-bayes-seven-in-ten', ['Beta(2, 2)', '9/14', '0.642857', '0.6429', 'coin', 'heads', 'Beta(9, 5)'])

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
stated(S, 'power-one-sided-shift', 'You are told $\\\\Phi(0.355) = 0.6387$.')           # fix pass finding 6: the table value is given
close(N.cdf(0.355), 0.6387, 5e-5, 'Phi(0.355) given in the prose')
close(0.5 * (1 + erf(0.355 / sqrt(2))), 0.6387, 5e-5, 'Phi(0.355) given in the prose [two routes]')

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

# rg-inference-t-from-r-squared (fix pass finding 5): 27 points, R^2 = 0.2, slope positive
a = sqrt(0.2 * 25 / 0.8)
# route B: build 102 points with R^2 exactly 0.2 and run least squares with its own standard error
rng = random.Random(3)
xv = [rng.gauss(0, 1) for _ in range(27)]
mx = sum(xv) / 27
xc = [x - mx for x in xv]
e = [rng.gauss(0, 1) for _ in range(27)]
me = sum(e) / 27
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
ok(bhat > 0, "slope positive")
b = bhat / sqrt(ss_res / 25 / sx2)
b_used_n = bhat / sqrt(ss_res / 27 / sx2)                      # divisor n in place of n - 2
key = two(a, b, 1e-9, 't from R^2')
numeric(S, 'rg-inference-t-from-r-squared', key, 2, {'no-one-minus': sqrt(0.2 * 25), 'used-n': two(sqrt(0.2 * 27 / 0.8), b_used_n, 1e-9, 'slip: n in place of n - 2'), 'no-root': 0.2 * 25 / 0.8})
ok(round(sqrt(0.2 * 27 / 0.8), 2) != round(key, 2), 'the n slip and the key differ at the asked place (2.60 against 2.50)')
stated(S, 'rg-inference-t-from-r-squared', '0.2 \\\\times 25 / 0.8 = 6.25')
stated(S, 'rg-inference-t-from-r-squared', 'The slope is positive.')
stale(S, 'rg-inference-t-from-r-squared', ['102', '0.2 \\\\times 100', 'Correct. t = 5.0', 'sits under the line.", "no-root": "You gave $t^2$. Take the square root of 25'])

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

# sample-size-for-signal-sharpe-years (delta finding 4: true Sharpe 1.1, t of 3; no course item has 1.1 with an expected t)
a = (F(3) / F(11, 10)) ** 2                                        # route A: exact, (3/1.1)^2 = 900/121
lo, hi = 0.0, 100.0
for _ in range(200):                                               # route B: bisection on 1.1 sqrt(T) = 3
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 1.1 * sqrt(mid) < 3 else (lo, mid)
key = two(a, lo, 1e-9, 'Sharpe years')
numeric(S, 'sample-size-for-signal-sharpe-years', key, 1, {'no-square': 3 / 1.1, 'aimed-at-two': (2 / 1.1) ** 2})
ok(a == F(900, 121) and abs(float(a) - 7.438) < 5e-4, 'years (3/1.1)^2 = 900/121 = 7.438')
stated(S, 'sample-size-for-signal-sharpe-years', '(3/1.1)^2 \\\\approx 7.44')
ok(fmt(a, 2) == '7.44' and fmt(F(900, 121), 1) == '7.4', '7.44 and 7.4 printed, two routes')
ok(fmt(3 / 1.1, 1) == '2.7' and fmt((2 / 1.1) ** 2, 1) == '3.3', 'slips 2.7 (3/1.1) and 3.3 (t of 2)')
stale(S, 'sample-size-for-signal-sharpe-years', ['8.16', 'used-1-96', 'reaches 2', '8.163', '(2/0.7)^2', '0.7', '18.4', '18.37', '18.367', '4.3', '8.2', 'reaches 3, to 1 decimal place'])

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


def stale_fc(f, i, *old):
    """Re-authored item: none of the old setting's figures is left anywhere in it."""
    blob = json.dumps(item(f, i), ensure_ascii=False)
    for o in old:
        ok(o not in blob, f'{f}/{i}: stale value "{o}" is gone')


# op-parity-price-the-put (re-authored after review bank 2 b: share 80, strike 84, three months, 6%, call 4.10)
a = 4.10 - 80 + 84 * exp(-0.06 * 0.25)
lo, hi = 0.01, 2.0
for _ in range(200):                                               # implied vol from the call, then price the put
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if bs(80, 84, 0.25, 0.06, mid) < 4.10 else (lo, mid)
b = bs(80, 84, 0.25, 0.06, lo, 'put')
key = two(a, b, 1e-6, 'put by parity and by Black-Scholes at the implied vol')
two(84 * exp(-0.015), 84 / sum(0.015 ** k / math.factorial(k) for k in range(30)), 1e-9, 'discounted strike two ways')
numeric(FI, 'op-parity-price-the-put', key, 2, {'undiscounted': 4.10 - 80 + 84, 'signs-swapped': 4.10 + 80 - 84 * exp(-0.015)})
ok(fmt(84 * exp(-0.015), 2) == '82.75', '84e^-0.015 is 82.75')
ok(abs(4.10 - 80 + 82.75 - 6.85) < 1e-9, '4.10 - 80 + 82.75 = 6.85')
stated(FI, 'op-parity-price-the-put', '4.10 - 80 + 82.75 = 6.85')
stale_fc(FI, 'op-parity-price-the-put', '50.97', '£52', '£3.10', '4.07', '0.02}', 'six months')

# op-strategies-bull-spread-breakeven (re-authored: buy the 40 call for 7, sell the 50 call for 3)
net = F(7) - F(3)
a = 40 + net
pay = lambda s: max(s - 40, 0) - max(s - 50, 0) - 4
b = next(k / 100 for k in range(3000, 6000) if pay(k / 100) >= 0)  # scan the expiry payoff
two(a, b, 0, 'break-even')
numeric(FI, 'op-strategies-bull-spread-breakeven', int(a), None, {'one-premium': 40 + 7, 'both-premiums': 40 + 7 + 3})
stated(FI, 'op-strategies-bull-spread-breakeven', '7 - 3 = 4')
stale_fc(FI, 'op-strategies-bull-spread-breakeven', '104', '106', '108', '100-strike', '110', '£6', '£2')

# op-greeks-second-order-estimate
a = F(4) + F(45, 100) * 2 + F(1, 2) * F(5, 100) * 4
quad = lambda x: 4 + 0.45 * x + 0.025 * x * x                       # the Taylor quadratic, evaluated by steps of 0.001
b = quad(0)
for k in range(2000):
    b += (quad((k + 1) / 1000) - quad(k / 1000))
key = two(a, b, 1e-9, 'delta-gamma estimate')
numeric(FI, 'op-greeks-second-order-estimate', float(a), 2, {'delta-only': 4 + 0.9, 'no-half': 4 + 0.9 + 0.05 * 4, 'change-only': float(a) - 4})
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
_it = item(FI, 'ms-orders-stop-through-a-gap')
ok(_it['difficulty'] == 3 and _it.get('requires') == ['micro/l4-market-or-limit'], 'stop item: difficulty 3, requires l4-market-or-limit')
ok('wakes once a trade prints at or below its stop price' in _it['prose'], 'stop item: prose defines the trigger')

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


# re-authored after review bank 2 b: buy the one-month call, sell the six-month call
net_c = [x - y for x, y in zip(greeks_closed(1 / 12), greeks_closed(0.5))]
net_f = [x - y for x, y in zip(greeks_fd(1 / 12), greeks_fd(0.5))]
for nm, x, y, t in zip(('gamma', 'vega', 'theta'), net_c, net_f, (1e-4, 1e-3, 1e-3)):
    two(x, y, t, f'calendar net {nm}')
ok(net_c[0] > 0 > net_c[1] and net_c[2] < 0, 'signs: gamma positive, vega negative, theta negative')
ok(fmt(net_c[0], 4) == '0.0409' and fmt(net_c[1], 2) == '-16.63' and fmt(net_c[2], 2) == '-8.19', f'net figures {net_c}')
choice(FI, 'greek-signs-calendar-spread', 'Positive gamma, negative vega, negative theta')
stated(FI, 'greek-signs-calendar-spread', 'gamma is +0.0409, vega -16.63 and theta -8.19 a year')
stale_fc(FI, 'greek-signs-calendar-spread', 'one-year', 'three-month', '19.77', '-0.0200', '+4.00')
_c = [o for o in item(FI, 'greek-signs-calendar-spread')['widget']['options'] if o.get('correct')][0]
ok(_c['text'] == 'Positive gamma, negative vega, negative theta', 'calendar key is the reverse of the old one')

# gv-risk-one-day-var
a = F(3000000) * F(12, 1000) * F(2326, 1000)
b = 3_000_000 * 0.012 * NormalDist(0, 1).inv_cdf(0.99)              # 2.326 is the rounded 99% point
two(a, b, 3000000 * 0.012 * 0.0005, 'VaR with the exact 99% point (within the rounding of 2.326)')
ok(a == 83736, 'VaR 83,736 exactly with 2.326')
numeric(FI, 'gv-risk-one-day-var', int(a), None, {'used-1-645': 3000000 * 0.012 * 1.645, 'ten-day': float(a) * sqrt(10), 'one-sd': 3000000 * 0.012})
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

# fix pass (review-bank-2-a findings 22, 23, 26, 27): re-authored stories carry none of the old story, rubric lines are checkable
stated(B, 'why-us-a-first-year-day', 'one timed estimation round a day')
stale(B, 'why-us-a-first-year-day', ['nine seconds', 'twenty minutes', 'arithmetic'])
stated(B, 'project-account-decision-to-redo', 'next-day footfall at one railway station')
stated(B, 'project-account-decision-to-redo', 'retrained on the first three years only and tested on the fourth')   # delta finding 16
stated(B, 'project-account-decision-to-redo', "barely better than the station's average for that month")
stale(B, 'project-account-decision-to-redo', ['electricity', 'demand', 'last week', 'copying the same weekday', 'earlier years only', 'the final year'])
ok(round(4.9 - 2.8, 1) == 2.1, 'decision-to-redo: 2.8% rose to 4.9% (a gap of 2.1 points)')
stated(B, 'star-story-unpopular-decision', 'The other four wanted a neural network')
stated(B, 'star-story-unpopular-decision', 'so I asked her to rerun my comparison herself.')
stale(B, 'star-story-unpopular-decision', ['Four of us'])
for it in DATA[B]['items']:
    for r in it['widget']['rubric']:
        ok('no filler' not in r['text'] and 'stops cleanly' not in r['text'].lower(), f'{B}/{it["id"]}: rubric line checkable from the text: {r["text"][:40]}')

# ---------------------------------------------------------------- coding-1 (rules 12 and 13; bank_2_code_check.py beside this script)
sys.path.insert(0, HERE)
import bank_2_code_check as cc
CO = 'coding-1'
print('coding-1 near-miss runs:')


def code(i, brute, traps):
    return cc.check_code(ok, f'{CO}/{i}', item(CO, i), brute, traps)


def tests_of(i):
    return {c['call']: c['expect'] for c in item(CO, i)['widget']['tests']}


# ds-arrays-sign-changes. Route B: runs of equal sign among the non-zero days (itertools.groupby).
code('ds-arrays-sign-changes',
     "from itertools import groupby\ndef sign_changes(pnl):\n    runs = [k for k, _ in groupby(x > 0 for x in pnl if x != 0)]\n    return max(len(runs) - 1, 0)\n",
     {'neighbours, zeros kept': "def sign_changes(pnl):\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if a * b < 0)\n",
      'zero as a third sign': "def sign_changes(pnl):\n    s = [(x > 0) - (x < 0) for x in pnl]\n    return sum(1 for a, b in zip(s, s[1:]) if a != b)\n",
      'flat day read as a loss (review bank 2 b, finding 11)': "def sign_changes(pnl):\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if (a > 0) != (b > 0))\n"})
t = tests_of('ds-arrays-sign-changes')
ok(t['sign_changes([1, 0, 2, 0, -3])'] == '1' and t['sign_changes([0, 5, -1])'] == '1', 'sign_changes: a flat day between two gains, and a leading flat day, give 1 each')
ok(t['sign_changes([3, -1, 0, -2, 5, 0, 0, -4])'] == '3' and t['sign_changes([-1, 0, 1])'] == '1', 'sign_changes: the brief values 3 and 1')
ok(eval(t['sign_changes([1, 0, -1] * 30000)']) == 2 * 30000 - 1, 'sign_changes: 60,000 alternating non-zero days give 59,999 flips')

# ds-hashing-price-mode (re-authored after review bank 2 b as modal_prices: every most frequent price, highest first).
# Route B: count each price by a list scan, keep those at the top count, sort them descending.
code('ds-hashing-price-mode',
     "def modal_prices(prices):\n    if len(prices) == 0:\n        return []\n    top = max(prices.count(v) for v in set(prices))\n    return sorted([v for v in set(prices) if prices.count(v) == top], reverse=True)\n",
     {'only one price': "def modal_prices(prices):\n    if not prices:\n        return []\n    return [max(set(prices), key=prices.count)]\n",
      'lowest first': "def modal_prices(prices):\n    if not prices:\n        return []\n    top = max(prices.count(v) for v in set(prices))\n    return sorted(v for v in set(prices) if prices.count(v) == top)\n",
      'repeats only (count of 2 or more)': "def modal_prices(prices):\n    return sorted((v for v in set(prices) if prices.count(v) >= 2), reverse=True)\n",
      'Counter.most_common(1)': "from collections import Counter\ndef modal_prices(prices):\n    return [Counter(prices).most_common(1)[0][0]] if prices else []\n"})
t = tests_of('ds-hashing-price-mode')
ok([t[k] for k in ('modal_prices([101, 100, 101, 100, 99])', 'modal_prices([5])', 'modal_prices([])', 'modal_prices([7, 8, 9])')] == ['[101, 100]', '[5]', '[]', '[9, 8, 7]'], 'modal_prices: the stated values')
ok(sorted({x for x in [101, 100, 101, 100, 99] if [101, 100, 101, 100, 99].count(x) == 2}, reverse=True) == [101, 100], 'modal_prices: 101 and 100 tie at two')
stale_fc(CO, 'ds-hashing-price-mode', 'price_mode', 'highest of the tied', 'returns the price that occurs most often')

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_DOWN
# edge-case-list-to-pence. Route B: decimal.Decimal on the cleaned text.
code('edge-case-list-to-pence',
     "from decimal import Decimal\ndef to_pence(text):\n    s = text.strip().replace('£', '').replace(',', '')\n    return int(Decimal(s) * 100)\n",
     {'int(float(s) * 100)': "def to_pence(text):\n    s = text.strip().replace('£', '').replace(',', '')\n    return int(float(s) * 100)\n",
      'decimals not padded': "def to_pence(text):\n    s = text.strip()\n    sign = -1 if s.startswith('-') else 1\n    s = s.lstrip('-').replace('£', '').replace(',', '')\n    p, _, d = s.partition('.')\n    return sign * (int(p) * 100 + int(d or 0))\n",
      # delta finding 8: a minus looked for before the spaces are stripped
      'minus tested before strip': "def to_pence(text):\n    neg = text.startswith('-')\n    s = text.replace('£', '').replace(',', '').strip()\n    p, _, d = s.partition('.')\n    pence = int((d + '00')[:2])\n    if neg: return -(abs(int(p or '0')) * 100 + pence)\n    return int(p or '0') * 100 + pence\n",
      'no strip, minus at index 0': "def to_pence(text):\n    s = text\n    sign = -1 if s[:1] == '-' else 1\n    if sign < 0: s = s[1:]\n    s = s.replace('£', '').replace(',', '')\n    p, _, d = s.partition('.')\n    return sign * (int(p or '0') * 100 + int((d.strip() + '00')[:2]))\n"})
# review bank 2 b, finding 21c: a function that returns 1999.0 for "£19.99" must fail the type test
_cl = cc.run("from decimal import Decimal\ndef to_pence(text):\n    return float(Decimal(text.strip().replace('£', '').replace(',', '')) * 100)\n", item(CO, 'edge-case-list-to-pence')['widget']['tests'])
ok(sum(1 for p, _ in _cl if not p) == 1 and not _cl[-1][0], 'to_pence: a float-returning twin with the right values fails only the type test')
t = tests_of('edge-case-list-to-pence')
ok(t['type(to_pence("£0.29")).__name__'] == "'int'", 'to_pence: the type test expects int')
brief = {'"£1,234.50"': 123450, '"0.07"': 7, '"12"': 1200, '"£3.5"': 350, '" -£2.05 "': -205, '"£0.29"': 29, '" £19.99 "': 1999}
ok(all(t[f'to_pence({k})'] == str(v) for k, v in brief.items()), 'to_pence: the seven brief values (the minus case now with spaces round it, delta finding 8)')
ok('to_pence("-£2.05")' not in t and 'to_pence("-0.5")' in t and t['to_pence("-0.5")'] == '-50', 'to_pence: the bare "-£2.05" test is gone; "-0.5" still tests a minus with no space')
ok(Decimal(' -£2.05 '.strip().replace('£', '')) * 100 == -205 and int(round(float(' -£2.05 '.strip().replace('£', '')) * 100)) == -205, 'to_pence: " -£2.05 " is -205 by Decimal and by a rounded float')
ok([int(float(s) * 100) for s in ('0.29', '-2.05', '19.99')] == [28, -204, 1998], 'to_pence: the float trap gives 28, -204 and 1998')
ok(0.29 * 100 < 29, 'explain: float 0.29 * 100 is just under 29')

# integer-division-lot-round. Route B: decimal division rounded towards zero (ROUND_DOWN).
code('integer-division-lot-round',
     "from decimal import Decimal, ROUND_DOWN, getcontext\ngetcontext().prec = 50\ndef lot_round(qty, lot):\n    return int((Decimal(qty) / Decimal(lot)).to_integral_value(rounding=ROUND_DOWN)) * lot\n",
     {'qty // lot * lot': "def lot_round(qty, lot):\n    return qty // lot * lot\n",
      'int(qty / lot) * lot': "def lot_round(qty, lot):\n    return int(qty / lot) * lot\n"})
t = tests_of('integer-division-lot-round')
ok([t[f'lot_round({a})'] for a in ('-250, 100', '250, 100', '-99, 100', '300, 100', '-300, 100')] == ['-200', '200', '0', '300', '-300'], 'lot_round: the brief values')
ok(-250 // 100 * 100 == -300 and -250 // 100 == -3, 'lot_round: floor gives -3 lots, -300')
ok(float(2 ** 53 + 1) == float(2 ** 53) and 10 ** 18 > 2 ** 53, 'explain: a float cannot hold every whole number above 2^53')

# pf-types-parse-fix. Route B: a regular expression over tag=value fields, read in order.
code('pf-types-parse-fix',
     "import re\ndef parse_fix(msg):\n    return {int(t): v for t, v in re.findall(r'(?:^|;)(\\d+)=([^;]*)', msg)}\n",
     {'split("=") without a limit': "def parse_fix(msg):\n    out = {}\n    if not msg:\n        return out\n    for f in msg.split(';'):\n        tag, value = f.split('=')\n        out[int(tag)] = value\n    return out\n",
      'no guard for the empty string': "def parse_fix(msg):\n    out = {}\n    for f in msg.split(';'):\n        tag, _, value = f.partition('=')\n        out[int(tag)] = value\n    return out\n",
      'tags left as text': "def parse_fix(msg):\n    return dict(f.split('=', 1) for f in msg.split(';')) if msg else {}\n"})
ok(''.split(';') == [''], 'explain: "".split(";") is [""]')

# pf-functions-binom-tail. Route B: enumeration of every sequence up to n = 16, a Pascal-row recurrence above.
code('pf-functions-binom-tail',
     "from fractions import Fraction\nfrom itertools import product\ndef binom_tail(n, k):\n    if n <= 16:\n        hits = sum(1 for s in product((0, 1), repeat=n) if sum(s) >= k)\n        return Fraction(hits, 2 ** n)\n    row = [1]\n    for _ in range(n):\n        row = [a + b for a, b in zip([0] + row, row + [0])]\n    return Fraction(sum(c for j, c in enumerate(row) if j >= k), 2 ** n)\n",
     {'a float result': "from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return sum(comb(n, j) for j in range(max(k, 0), n + 1)) / 2 ** n\n",
      'more than k': "from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(sum(comb(n, j) for j in range(max(k + 1, 0), n + 1)), 2 ** n)\n",
      'negative k not clamped': "from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(sum(comb(n, j) for j in range(k, n + 1)), 2 ** n)\n"})
t = tests_of('pf-functions-binom-tail')
ok(F(sum(comb(16, j) for j in range(13, 17)), 2 ** 16) == F(697, 65536) and [comb(16, j) for j in (13, 14, 15, 16)] == [560, 120, 16, 1], 'binom_tail(16, 13) = (560 + 120 + 16 + 1)/65,536')
ok(F(sum(comb(10, j) for j in range(5, 11)), 1024) == F(319, 512), 'binom_tail(10, 5) = 319/512')
ok(F(sum(comb(3, j) for j in (2, 3)), 8) == F(1, 2), 'prose: binom_tail(3, 2) = 1/2')
stated(CO, 'pf-functions-binom-tail', '(560 + 120 + 16 + 1)/65{,}536 = 697/65{,}536')
ok('`math.comb(n, j)` counts the ways to choose which `j` flips are heads.' in item(CO, 'pf-functions-binom-tail')['prose'], 'binom_tail: prose gives math.comb')
ok(item(CO, 'pf-functions-binom-tail')['requires'] == ['py-found/l7-arguments', 'conditional/l14-independent-trials'], 'binom_tail: requires the lesson that teaches comb')

# pf-types-round-half-even (re-authored after review bank 2 b; delta finding 12: two halves of different parity, so half-to-even and the school rule differ)
# Route A runs the line; route B uses decimal (half to even) and math.floor / math.trunc.
it_ = item(CO, 'pf-types-round-half-even')
key = cc.eval_line(it_['prose'])
dq = lambda x, mode: int(Decimal(x).quantize(Decimal(1), rounding=mode))
b_ = dq('-1.5', ROUND_DOWN) + dq('-1.5', ROUND_HALF_EVEN) + dq('-4.5', ROUND_HALF_EVEN) + math.floor(-9 / 2)
two(key, b_, 0, 'int + round + round + floor division')
all_zero = math.trunc(-1.5) + math.trunc(-1.5) + math.trunc(-4.5) + math.trunc(-9 / 2)                       # every term cut towards zero
half_up = math.trunc(-1.5) + math.floor(-1.5 + 0.5) + math.floor(-4.5 + 0.5) + math.floor(-9 / 2)            # each half read upwards, towards +infinity
half_away = math.trunc(-1.5) + dq('-1.5', ROUND_HALF_UP) + dq('-4.5', ROUND_HALF_UP) + math.floor(-9 / 2)     # the school rule: each half away from zero
two(half_up, -1 + math.floor(F(-3, 2) + F(1, 2)) + math.floor(F(-9, 2) + F(1, 2)) + F(-9, 2) // 1, 0, 'half up, by Fractions')
two(half_away, -1 - math.floor(F(3, 2) + F(1, 2)) - math.floor(F(9, 2) + F(1, 2)) + F(-9, 2) // 1, 0, 'half away, by Fractions (floor of |x| + 1/2, sign put back)')
numeric(CO, 'pf-types-round-half-even', key, None, {'all-towards-zero': all_zero, 'half-up': half_up, 'half-away': half_away})
ok((int(-1.5), round(-1.5), round(-4.5), -9 // 2) == (-1, -2, -4, -5) and key == -12, 'terms -1, -2, -4, -5; sum -12')
ok(all_zero == -10 and half_up == -11 and half_away == -13, 'slips -10, -11 and -13')
# the old line, round(-3.5), could not tell half-to-even from the school rule; the new one can
ok(round(-3.5) == dq('-3.5', ROUND_HALF_UP) == -4 and round(-4.5) != dq('-4.5', ROUND_HALF_UP) and key != half_away, 'round(-3.5) hid the difference; round(-4.5) shows it, so the school rule no longer gives the key')
stated(CO, 'pf-types-round-half-even', '-1 - 2 - 4 - 5 = -12')
stale_fc(CO, 'pf-types-round-half-even', '0.5', '2.5', '6', '"value": 3', '-3.5', 'three terms', '-3, -4 and -5', '-3 - 4 - 5')

# pf-functions-default-list (re-authored after review bank 2 b: a default dict, three calls, sizes summed)
# route A runs the lines; route B replays the calls on one explicit dict. Slips: a fresh dict each call, the count of x returned.
it_ = item(CO, 'pf-functions-default-list')
key = cc.run_snippet(it_['prose'])['total']
def mark_fresh(x, seen=None):
    seen = {} if seen is None else seen
    seen[x] = seen.get(x, 0) + 1
    return len(seen)
shared, replay = {}, []
for x_ in ('a', 'b', 'a'):
    shared[x_] = shared.get(x_, 0) + 1
    replay.append(len(shared))
two(key, sum(replay), 0, 'default dict total')
count_of_x = []
shared2 = {}
for x_ in ('a', 'b', 'a'):
    shared2[x_] = shared2.get(x_, 0) + 1
    count_of_x.append(shared2[x_])
numeric(CO, 'pf-functions-default-list', key, None, {'fresh-dict': mark_fresh('a') + mark_fresh('b') + mark_fresh('a'), 'count-of-x': sum(count_of_x)})
ok(replay == [1, 2, 2] and key == 5 and sum(count_of_x) == 4, 'calls return 1, 2, 2; total 5; count of x gives 4')
stale_fc(CO, 'pf-functions-default-list', 'acc=', 'add(', '[1, 2, 3', '"value": 6', 'three-each', 'fresh-list')

# complexity-read-doubling-inner: count the inner steps; n log2 n at n = 1,024; the ratio to n log n is flat.
it_ = item(CO, 'complexity-read-doubling-inner')
def inner_steps(n):
    steps = 0
    for i in range(n):
        j = 1
        while j < n:
            j *= 2
            steps += 1
    return steps
two(inner_steps(1024), 1024 * 10, 0, 'inner steps at n = 1,024')
ratios = [inner_steps(n) / (n * math.ceil(math.log2(n))) for n in (64, 256, 1024, 4096)]
ok(max(ratios) - min(ratios) < 1e-12, 'steps / (n ceil(log2 n)) is constant: O(n log n)')
ok(inner_steps(4096) / inner_steps(1024) < 4.9 and inner_steps(4096) / inner_steps(1024) > 4.5, 'quadrupling n multiplies the work by 4.8, not 16 or 4')
choice(CO, 'complexity-read-doubling-inner', 'O(n \\log n)')
stated(CO, 'complexity-read-doubling-inner', '1{,}024 \\\\times 10 = 10{,}240')

# at-complexity-tripling-loop: run the lines; first power of 3 at or above 1,000 by logarithms.
it_ = item(CO, 'at-complexity-tripling-loop')
key = cc.run_snippet(it_['prose'])['count']
two(key, math.ceil(math.log(1000, 3)), 0, 'tripling count')
numeric(CO, 'at-complexity-tripling-loop', key, None, {'stopped-early': sum(1 for k in range(1, 20) if 3 ** k < 1000), 'divided': 1000 // 3})
ok(3 ** 7 == 2187 and 3 ** 6 == 729, '3^6 = 729 and 3^7 = 2,187')

# pf-types-backward-slice: run the lines; route B lists the indices 7, 5, 3 by a loop.
it_ = item(CO, 'pf-types-backward-slice')
key = cc.run_snippet(it_['prose'])['total']
idx, k_ = [], 7
while k_ > 2:
    idx.append(k_)
    k_ -= 2
two(key, sum(idx), 0, 'backward slice')
xs_ = list(range(10))
numeric(CO, 'pf-types-backward-slice', key, None, {'step-one': sum(xs_[7:2:-1]), 'ends-swapped': sum(xs_[6:1:-2])})
ok(xs_[6:1:-2] == [6, 4, 2], 'ends-swapped slip is 6, 4 and 2')

# integer-division-toward-zero (C++ reading): compile and run the C++ lines; run the Python lines.
it_ = item(CO, 'integer-division-toward-zero')
ns_ = cc.run_snippet(it_['prose'])
# re-authored after review bank 2 b: 7 divided by -2 (the divisor carries the sign)
ok((ns_['q'], ns_['r']) == (-4, -1), 'Python: 7 // -2 = -4, 7 % -2 = -1')
ok(math.floor(7 / -2) == -4 and 7 - (-2) * (-4) == -1, 'Python route B: floor and remainder')
cpp_body = cc.snippet(it_['prose'], 'cpp')[0]
out = cc.cpp('#include <cstdio>\nint main() {\n' + cpp_body + 'static_assert(7 / -2 == -3 && 7 % -2 == 1);\nstd::printf("%d %d\\n", q, r);\n}\n')
if out is not None:
    ok(out.split() == ['-3', '1'], f'C++: 7 / -2 = -3, 7 % -2 = 1 (ran: {out.strip()})')
ok(math.trunc(7 / -2) == -3 and 7 - (-2) * (-3) == 1, 'C++ route B: truncation and remainder')
choice(CO, 'integer-division-toward-zero', 'C++: -3 and 1. Python: -4 and -1.')
opts = {o['text']: o for o in it_['widget']['options']}
ok(set(opts) == {'C++: -3 and 1. Python: -4 and -1.', 'C++: -3 and 1. Python: -3 and 1.', 'C++: -4 and -1. Python: -4 and -1.', 'C++: -4 and -1. Python: -3 and 1.'}, 'C++ reading: the four sign patterns')
stale_fc(CO, 'integer-division-toward-zero', '-7', '-1. Python: -4 and 1')

# coding-1 file shape (section 2): six code, five reasoning (numeric or choice), one C++ reading choice
kinds = [x['widget']['kind'] for x in DATA[CO]['items']]
ok(kinds.count('code') == 6 and kinds.count('numeric') == 4 and kinds.count('choice') == 2, f'coding-1 kinds {kinds}')
ok(sorted(x['difficulty'] for x in DATA[CO]['items']) == [2] * 4 + [3] * 7 + [4], 'coding-1 difficulties: D2 4, D3 7, D4 1')
ok(all(x['style'] == 'coding' for x in DATA[CO]['items']), 'coding-1 style')

# ---------------------------------------------------------------- whole-file checks
allids = []
for fn in sorted(os.listdir(BANK)):
    if fn.endswith('.json'):
        allids += [it['id'] for it in json.load(open(os.path.join(BANK, fn), encoding='utf-8'))['items']]
dups = {x for x in allids if allids.count(x) > 1}
ok(not dups, f'item ids unique across the bank ({sorted(dups)})')
for f in FILES:
    for it in DATA[f]['items']:
        # accepted exception to brief rule 16 (review bank 2 b, finding 1): the stop item is difficulty 3 and has requires
        ok(('requires' in it) == (it['difficulty'] >= 4 or it['id'] == 'ms-orders-stop-through-a-gap'), f'{f}/{it["id"]}: requires only at difficulty 4 and 5')
        ok(it['source'] == 'Original' and len(it['tags']) == 1, f'{f}/{it["id"]}: source and one tag')
        ok(it['difficulty'] in (2, 3, 4, 5), f'{f}/{it["id"]}: difficulty 2 to 5')

counts = {f: len(DATA[f]['items']) for f in FILES}
ok(counts == {'statistics-1': 15, 'finance-1': 15, 'behavioural-5': 8, 'coding-1': 12}, f'item counts {counts}')

print(f'{checks[0]} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
