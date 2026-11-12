#!/usr/bin/env python3
"""Bank part 2, session 2: every key, slip and stated figure in statistics-2, finance-2, behavioural-6 and coding-2, by two routes.

coding-2 uses bank_2_code_check.py (beside this script): each code item's solution, brute-force twin, starter and named
near-miss methods run on its own tests; reasoning items run their own snippet; the C++ item compiles with g++ -std=c++20.

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
FILES = ['statistics-2', 'finance-2', 'behavioural-6', 'coding-2']
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


def stale(f, i, olds):
    """Fix pass: none of the old values or phrases of a re-authored item survives anywhere in it."""
    blob = json.dumps(item(f, i), ensure_ascii=False)
    for o in olds:
        ok(o not in blob, f'{f}/{i}: stale value "{o}" is gone')


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


S, FI, B = 'statistics-2', 'finance-2', 'behavioural-6'


def solve(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def r2_fit(cols, y):
    """R squared and adjusted R squared of y on an intercept and the given columns, by the normal equations."""
    n = len(y)
    X = [[1.0] + [c[i] for c in cols] for i in range(n)]
    k = len(X[0])
    beta = solve([[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)], [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)])
    my = sum(y) / n
    rss = sum((y[i] - sum(beta[j] * X[i][j] for j in range(k))) ** 2 for i in range(n))
    R = 1 - rss / sum((v - my) ** 2 for v in y)
    return R, 1 - (1 - R) * (n - 1) / (n - k), beta, rss


def bs(S0, K, T, r, sig):
    d1 = (log(S0 / K) + (r + sig * sig / 2) * T) / (sig * sqrt(T))
    return S0 * N.cdf(d1) - K * exp(-r * T) * N.cdf(d1 - sig * sqrt(T))


# ---------------------------------------------------------------- statistics-2
# es-mle-two-coins-ratio: Fraction of sequence probabilities against enumeration of all 32 sequences
a = (F(8, 10) ** 4 * F(2, 10)) / F(1, 2) ** 5
seqs = [[(s >> k) & 1 for k in range(5)] for s in range(32)]
lik = lambda p: sum(math.prod(p if h else 1 - p for h in sq) for sq in seqs if sum(sq) == 4)
key = two(a, lik(0.8) / lik(0.5), 1e-12, 'likelihood ratio')
numeric(S, 'es-mle-two-coins-ratio', key, 2, {'upside-down': 1 / a, 'all-heads': F(8, 10) ** 5 / F(1, 2) ** 5})
ok(F(8, 10) ** 4 * F(2, 10) == F(8192, 100000) and F(1, 2) ** 5 == F(3125, 100000), 'stated 0.08192 and 0.03125')

# shrinkage-mse-best-multiplier: calculus against a grid search of the mean squared error
mse = lambda c: c * c * 3 + (c - 1) ** 2 * 9
a = F(9, 9 + 3)
cbest = min((k / 100000 for k in range(200001)), key=mse)
key = two(a, cbest, 1e-5, 'best multiplier')
ok(all(mse(k / 1000) >= mse(0.75) - 1e-12 for k in range(-2000, 3000)), 'claim: 0.75 gives the smallest error')
ok(mse(F(3, 4)) == F(9, 4) and mse(1) == 3, 'error falls from 3 to 2.25')
numeric(S, 'shrinkage-mse-best-multiplier', key, 3, {'unbiased': 1, 'equal-split': F(3, 3 + 3)})   # "as a decimal": checked to 3 places
ok(item(S, 'shrinkage-mse-best-multiplier')['difficulty'] == 4 and item(S, 'shrinkage-mse-best-multiplier')['requires'] == ['research-int/l6-bias-variance-aloud'], 'fix pass 17: difficulty 4, requires kept')

# es-intervals-poll-margin: binomial standard error against a seeded simulation of the poll
p = F(240, 400)
a = 1.96 * sqrt(p * (1 - p) / 400) * 100
rng = random.Random(17)
shares = [sum(rng.random() < 0.6 for _ in range(400)) / 400 for _ in range(20000)]
ms = sum(shares) / len(shares)
b = 1.96 * sqrt(sum((s - ms) ** 2 for s in shares) / (len(shares) - 1)) * 100
key = two(a, b, 0.05, 'margin in points (simulation tolerance 0.05)')
numeric(S, 'es-intervals-poll-margin', key, 1, {'used-half': 1.96 * sqrt(0.25 / 400) * 100, 'no-multiplier': sqrt(0.24 / 400) * 100})
ok(fmt(sqrt(0.24 / 400), 4) == '0.0245', 'standard error 0.0245')
two(2 * sqrt(0.24 / 400) * 100, 1.96 * sqrt(0.25 / 400) * 100, 0.01, 'fix pass 15: 2 for 1.96 and p = 0.5 both land on 4.9')
close(round(2 * sqrt(0.24 / 400) * 100, 1), 4.9, 1e-9, 'fix pass 15: 2 in place of 1.96 prints 4.9')
stated(S, 'es-intervals-poll-margin', 'or 2 in place of 1.96')

# es-bayes-prior-and-sample: precision weights against a midpoint integral of prior times likelihood
a = (F(0) * F(1, 4) + F(3) * 1) / (F(1, 4) + 1) / 100
grid = [-10 + (k + 0.5) * 1e-4 for k in range(200000)]
dens = [exp(-m * m / 8 - (m - 3) ** 2 / 2) for m in grid]
b = sum(m * d for m, d in zip(grid, dens)) / sum(dens) / 100
key = two(a, b, 1e-8, 'posterior mean')
numeric(S, 'es-bayes-prior-and-sample', key, 1, {'plain-average': F(15, 1000), 'weights-swapped': (F(0) * 1 + F(3) * F(1, 4)) / F(5, 4) / 100})

# ht-setup-ten-paired-days: closed form against ten built differences with that mean and sd
a = 1.2 / (1.5 / sqrt(10))
base = [(-1) ** k for k in range(10)]                    # mean 0, sum of squares 10
d = [1.2 + 1.5 * sqrt(9 / 10) * v for v in base]          # sample sd 1.5
md = sum(d) / 10
sd = sqrt(sum((x - md) ** 2 for x in d) / 9)
key = two(a, md / (sd / sqrt(10)), 1e-12, 'paired t')
numeric(S, 'ht-setup-ten-paired-days', key, 2, {'no-root': 1.2 / 1.5, 'root-nine': 1.2 / (1.5 / 3)})
ok(fmt(1.5 / sqrt(10), 3) == '0.474' and fmt(1.2 / 0.474, 2) == '2.53', 'stated 0.474 and 2.53')

# ht-pvalue-z-two-and-a-half: NormalDist against erfc
a = 2 * (1 - N.cdf(2.2))                                    # fix pass finding 19: z = 2.2 (the id keeps its old name)
two(a, erfc(2.2 / sqrt(2)), 1e-12, 'two-sided p at 2.2')
ok(fmt(a, 3) == '0.028' and fmt(a / 2, 3) == '0.014' and fmt(1 - N.cdf(1.96), 3) == '0.025', 'options 0.028, 0.014, 0.025')
ok(fmt(a / 2, 4) == '0.0139' and fmt(a, 3) == '0.028' and 0.01 < a < 0.05, 'stated 0.0139, 0.028; significant at 5% not 1%')
choice(S, 'ht-pvalue-z-two-and-a-half', '0.028')
stale(S, 'ht-pvalue-z-two-and-a-half', ['2.5', '0.012', '0.006', '0.0062', '0.0124'])
ok(abs(a - 0.025) > 0.002 and abs(a / 2 - 0.014) < 0.0005, 'the 0.028 and 0.025 options are distinguishable at 3 places')

# ht-pvalue-bigger-sample: scaling rule against recomputing z from a mean, sd and n
a = 2.4 * sqrt(2.25)
n0 = 100
mean_ = 2.4 * 1.0 / sqrt(n0)                             # sd 1, n 100 gives z 2.4
key = two(a, mean_ / (1.0 / sqrt(2.25 * n0)), 1e-12, 'new z')
numeric(S, 'ht-pvalue-bigger-sample', key, 1, {'times-n': 2.4 * 2.25, 'divided': 2.4 / 1.5})

# ht-errors-equal-error-cutoff: symmetry against a bisection on the two error curves
lo, hi = 0.0, 3.0
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if (1 - N.cdf(mid)) > N.cdf(mid - 3) else (lo, mid)
two(1.5, lo, 1e-9, 'equal-error cut-off')
a = 1 - N.cdf(1.5)
key = two(a, 0.5 * erfc(1.5 / sqrt(2)), 1e-12, 'common error rate')
numeric(S, 'ht-errors-equal-error-cutoff', key, 4, {'added-both': 2 * a, 'cutoff-at-three': 1 - N.cdf(3)})
ok(N.cdf(3 - 3) == 0.5, 'cut-off at 3 has type II error 0.5')

# rg-fit-point-at-the-mean: least squares before and after, against the normal equations
b1, _, _ = ols([1, 2, 3], [2, 3, 7])
b2, _, _ = ols([1, 2, 3, 2], [2, 3, 7, 10])
_, _, beta, _ = r2_fit([[1, 2, 3, 2]], [2, 3, 7, 10])
two(b2, beta[1], 1e-12, 'slope after, by normal equations')
ok(abs(b1 - 2.5) < 1e-12 and abs(b2 - 2.5) < 1e-12, 'slope stays 2.5')
ok(abs((4 - 2.5 * 2) - (-1)) < 1e-12 and abs(beta[0] - 0.5) < 1e-12, 'intercept moves from -1 to 0.5')
for h in (-50, 0, 10, 99):                                # claim: whatever the height, the slope is unchanged
    ok(abs(ols([1, 2, 3, 2], [2, 3, 7, h])[0] - 2.5) < 1e-12, f'slope 2.5 with the new point at height {h}')
choice(S, 'rg-fit-point-at-the-mean', 'It stays 2.5')

# rg-multiple-useless-predictor: seeded count against the exact chance P(|t_47| < 1)
rng = random.Random(2)
fell_adj = fell_r2 = 0
for _ in range(2000):
    x1 = [rng.gauss(0, 1) for _ in range(50)]
    y = [0.5 * v + rng.gauss(0, 1) for v in x1]
    z = [rng.gauss(0, 1) for _ in range(50)]
    R1, A1, _, _ = r2_fit([x1], y)
    R2, A2, _, _ = r2_fit([x1, z], y)
    fell_adj += A2 < A1
    fell_r2 += R2 < R1 - 1e-12
    t2 = (R2 - R1) / (1 - R2) * 47                            # t squared of the added coefficient, from the two R^2 values
    ok((A2 < A1) == (t2 < 1), 'fix pass 11: adjusted R^2 falls exactly when |t| < 1')
nu = 47
tpdf = lambda t: math.gamma((nu + 1) / 2) / (sqrt(nu * pi) * math.gamma(nu / 2)) * (1 + t * t / nu) ** (-(nu + 1) / 2)
p_t = sum(tpdf(-1 + (k + 0.5) * 1e-5) for k in range(200000)) * 1e-5   # adjusted R^2 falls exactly when |t| < 1
two(fell_adj / 2000, p_t, 3 * sqrt(p_t * (1 - p_t) / 2000), 'adjusted R^2 fell (tolerance three binomial sds)')
ok(fell_r2 == 0 and 0.6 < p_t < 0.72 and 0.6 < fell_adj / 2000 < 0.72, f'about two times in three: exact {p_t:.3f}, simulated {fell_adj / 2000:.3f}; R^2 fell {fell_r2} times')
choice(S, 'rg-multiple-useless-predictor', 'cannot fall')
stated(S, 'rg-multiple-useless-predictor', "so it falls whenever the new coefficient's t statistic is below 1 in size. Pure noise manages that about two times in three.")
stale(S, 'rg-multiple-useless-predictor', ['1,362', 'seeded', '2,000'])

# collinear-features-inflation-factor: 1/(1 - r^2) against the diagonal of the inverse correlation matrix
a = 1 / (1 - F(36, 100))                                      # fix pass finding 8: correlation 0.6
inv11 = solve([[1, 0.6], [0.6, 1]], [1, 0])[0]
key = two(a, inv11, 1e-12, 'variance inflation factor')
numeric(S, 'collinear-features-inflation-factor', key, 2, {'one-minus-r': 1 / (1 - F(6, 10)), 'standard-error-factor': sqrt(a)})
ok(a == F(25, 16) and F(6, 10) ** 2 == F(36, 100) and 1 / (1 - 0.36) == 1 / 0.64, '0.6 squared is 0.36 and 1/0.64 = 25/16')
stated(S, 'collinear-features-inflation-factor', '1/0.64 \\\\approx 1.56')
stale(S, 'collinear-features-inflation-factor', ['0.9', '0.81', '0.19', '5.26', '5.2632', '2.29', '"value": 10,'])

# ts-forecast-two-steps-ahead: closed form against iterating the forecast
a = 10 + F(6, 10) ** 2 * 5
f_ = 15.0
for _ in range(2):
    f_ = 10 + 0.6 * (f_ - 10)
key = two(a, f_, 1e-12, 'two-step forecast')
numeric(S, 'ts-forecast-two-steps-ahead', key, 1, {'one-step': 10 + F(6, 10) * 5, 'no-mean': F(36, 100) * 15})

# ts-acf-two-day-variance-ratio: 1 + rho against a seeded MA(1) with that lag-1 autocorrelation
a = 1 + F(-15, 100)
th = (-1 + sqrt(1 - 4 * 0.15 ** 2)) / (2 * 0.15)          # MA(1) theta with theta/(1 + theta^2) = -0.15
two(th / (1 + th * th), -0.15, 1e-12, 'MA(1) autocorrelation')
rng = random.Random(23)
e = [rng.gauss(0, 1) for _ in range(400001)]
r = [e[t] + th * e[t - 1] for t in range(1, 400001)]
two_day = [r[t] + r[t + 1] for t in range(0, 399999, 2)]
var1 = sum(v * v for v in r) / len(r)
var2 = sum(v * v for v in two_day) / len(two_day)
key = two(a, var2 / (2 * var1), 0.01, 'variance ratio (simulation tolerance 0.01)')
numeric(S, 'ts-acf-two-day-variance-ratio', key, 2, {'independent': 1, 'sign': 1 + F(15, 100)})

# measurement-error-noisy-regressor: attenuation formula against a seeded regression on noisy x
a = F(14, 10) * F(7, 7 + 3)                                   # fix pass finding 9: slope 1.4, variance 7, noise 3
rng = random.Random(29)
xt = [rng.gauss(0, sqrt(7)) for _ in range(200000)]
yy = [1.4 * v + rng.gauss(0, 1) for v in xt]
xo = [v + rng.gauss(0, sqrt(3)) for v in xt]
key = two(a, ols(xo, yy)[0], 0.01, 'attenuated slope (simulation tolerance 0.01)')
numeric(S, 'measurement-error-noisy-regressor', key, 2, {'no-attenuation': F(14, 10), 'wrong-way': F(14, 10) * F(10, 7)})
ok(F(7, 10) == F(7, 7 + 3) and a == F(98, 100), 'reliability ratio 0.7 and slope 0.98')
stated(S, 'measurement-error-noisy-regressor', '1.4 \\\\times 0.7 = 0.98')
ok(a != F(3, 4), 'the key is no longer the 0.75 of shrinkage-mse-best-multiplier')
stale(S, 'measurement-error-noisy-regressor', ['1.2', '0.75', '0.625', '5/8', '8/5', '1.92', '0.75'])

# dl-clt-mean-of-hundred: NormalDist against erfc
a = 1 - N.cdf((5.8 - 5) / (4 / sqrt(100)))
key = two(a, 0.5 * erfc(2 / sqrt(2)), 1e-12, 'tail beyond z = 2')
numeric(S, 'dl-clt-mean-of-hundred', key, 3, {'no-root': 1 - N.cdf(0.8 / 4), 'both-tails': 2 * key})   # fix pass 14: 3 places
stated(S, 'dl-clt-mean-of-hundred', 'to 3 decimal places')
stated(S, 'dl-clt-mean-of-hundred', 'about $1 - \\\\Phi(2) \\\\approx 0.023$')
stale(S, 'dl-clt-mean-of-hundred', ['0.0228', '4 decimal places', '0.4207'])

# ---------------------------------------------------------------- finance-2
# fi-interest-three-payments-pv: annuity formula against a sum of discounted payments
a = 500 * (1 - 1.08 ** -3) / 0.08
b = sum(500 / 1.08 ** t for t in (1, 2, 3))
key = two(a, b, 1e-9, 'present value')
numeric(FI, 'fi-interest-three-payments-pv', key, 2, {'not-discounted': 1500, 'all-three-years': 1500 / 1.08 ** 3})
ok([fmt(500 / 1.08 ** t, 2) for t in (1, 2, 3)] == ['462.96', '428.67', '396.92'], 'stated parts')

# fi-bonds-zero-coupon-yield: root against a bisection on the price
a = (100 / 78.35) ** 0.2 - 1
lo, hi = 0.0, 0.2
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 100 / (1 + mid) ** 5 > 78.35 else (lo, mid)
key = two(a, lo, 1e-12, 'zero yield')
numeric(FI, 'fi-bonds-zero-coupon-yield', key, 2, {'simple-interest': 21.65 / 78.35 / 5, 'gain-over-five': 21.65 / 5 / 100})   # 2 dp of a per cent
ok(fmt(1.05 ** 5, 5) == '1.27628' and fmt(100 / 78.35, 5) == '1.27632', 'stated 1.27628 and 1.27632')

# fi-forwards-rich-forward: fair value against a cash-flow ledger of the arbitrage
fair = F(200) * F(103, 100) - 4
a = 205 - fair
ledger = -200 + 200 + 4 + 205 - 200 * 1.03              # buy share, borrow, dividend, deliver, repay
key = two(a, ledger, 1e-9, 'arbitrage profit')
numeric(FI, 'fi-forwards-rich-forward', int(a), None, {'no-dividend': 205 - 200 * F(103, 100), 'dividend-twice': 205 - (206 - 8)})

# fi-forwards-futures-daily-loss
a = 10 * 50 * (4000 - 3960)
b = sum(50 * 1 for _ in range(10) for _ in range(40))
two(a, b, 0, 'futures loss')
numeric(FI, 'fi-forwards-futures-daily-loss', a, None, {'one-contract': 50 * 40, 'points-times-contracts': 10 * 40})

# op-strategies-covered-call-at-fifty: payoff formula against a ledger
a = (45 - 40) + 2
b = 50 - 40 + 2 - max(50 - 45, 0)
two(a, b, 0, 'covered call profit')
numeric(FI, 'op-strategies-covered-call-at-fifty', a, None, {'no-cap': 50 - 40 + 2, 'no-premium': 45 - 40})

# op-strategies-butterfly-best-case: closed form against a scan of the expiry payoff
cost = F(1250, 100) - 2 * 6 + F(250, 100)
pay = lambda s: max(s - 90, 0) - 2 * max(s - 100, 0) + max(s - 110, 0)
best = max(pay(k / 10) for k in range(0, 2001))
two(10 - cost, best - float(cost), 1e-12, 'largest butterfly profit')
numeric(FI, 'op-strategies-butterfly-best-case', int(10 - cost), None, {'ignored-cost': 10, 'gave-cost': cost})

# op-parity-call-under-its-floor: floor less price against the worst case over expiry prices
a = F(100 - 95) - F(450, 100)
worst = min(-4.50 + 100 + max(s - 95, 0) - s for s in [k / 10 for k in range(0, 3001)])
key = two(a, worst, 1e-9, 'smallest locked-in profit')
numeric(FI, 'op-parity-call-under-its-floor', key, 2, {'gave-floor': 5, 'gave-price': F(45, 10)})

# gamma-pnl-break-even-move: closed form against a bisection on gamma gain less theta
a = sqrt(2 * 0.045 / 0.04)
lo, hi = 0.0, 5.0
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 0.5 * 0.04 * mid * mid < 0.045 else (lo, mid)
key = two(a, lo, 1e-9, 'break-even move')
numeric(FI, 'gamma-pnl-break-even-move', key, 1, {'no-half': sqrt(0.045 / 0.04), 'no-root': 2 * 0.045 / 0.04})

# digital-option-at-the-money: N(d2) against a seeded simulation, and against a call-spread limit
d2 = -0.3 * sqrt(0.25) / 2
a = N.cdf(d2)
spread = (bs(50, 49.999, 0.25, 0, 0.3) - bs(50, 50.001, 0.25, 0, 0.3)) / 0.002
key = two(a, spread, 1e-6, 'digital by a tight call spread')
rng = random.Random(41)
hits = sum(50 * exp(-0.045 / 4 + 0.15 * rng.gauss(0, 1)) > 50 for _ in range(400000))
two(a, hits / 400000, 0.003, 'digital by simulation (tolerance 0.003)')
numeric(FI, 'digital-option-at-the-money', key, 4, {'one-half': 0.5, 'used-d1': N.cdf(-d2)})
ok(fmt(d2, 3) == '-0.075', 'd2 = -0.075')

# tp-multistep-two-step-call: risk-neutral Fraction against replication by backward induction with shares and cash
q = (1 - F(8, 10)) / (F(125, 100) - F(8, 10))
a = q * q * (40 * F(125, 100) ** 2 - 40)
up, dn = F(125, 100), F(8, 10)


def replicate(s, steps):
    if steps == 0:
        return max(s - 40, 0)
    vu, vd = replicate(s * up, steps - 1), replicate(s * dn, steps - 1)
    delta = (vu - vd) / (s * up - s * dn)
    return delta * s + (vu - delta * s * up)              # shares plus cash (zero rate)


two(a, replicate(F(40), 2), 0, 'two-step call')
ok(q == F(4, 9) and a == F(40, 9), 'q = 4/9, price 40/9')
numeric(FI, 'tp-multistep-two-step-call', a, 2, {'even-chances': F(1, 4) * F(45, 2), 'q-once': q * F(45, 2)})

# ms-book-weighted-mid
a = (F(9998, 100) * 100 + F(10002, 100) * 900) / 1000
b = 99.98 + (100.02 - 99.98) * 900 / 1000                 # mid moves towards the ask by the bid's share of size
key = two(a, b, 1e-12, 'weighted mid')
numeric(FI, 'ms-book-weighted-mid', key, 3, {'own-side': (F(9998, 100) * 900 + F(10002, 100) * 100) / 1000, 'plain-mid': 100})

# ms-costs-impact-four-times-size
a = 40 * sqrt(16 / 4)
k_ = 40 / sqrt(0.04)
two(a, k_ * sqrt(0.16), 1e-9, 'square-root impact')
numeric(FI, 'ms-costs-impact-four-times-size', int(round(a)), None, {'linear': 40 * 4, 'no-change': 40})

# ms-mm-spread-less-drift
a = F(1000) * (F(1) - F(4, 10)) / 100
b = sum(0.01 - 0.004 for _ in range(1000))
key = two(a, b, 1e-9, 'market-making result')
numeric(FI, 'ms-mm-spread-less-drift', int(a), None, {'ignored-move': 10, 'added-move': 14})

# gv-risk-two-desks: closed form against a seeded simulation of the two desks' P&L quantile
a = sqrt(1 + 1 + 2 * 0.5)
rng = random.Random(43)
z99 = N.inv_cdf(0.99)
pnl = []
for _ in range(400000):
    u = rng.gauss(0, 1)
    v = 0.5 * u + sqrt(0.75) * rng.gauss(0, 1)
    pnl.append((u + v) / z99)                              # each desk's VaR is 1, so its sd is 1/z99
pnl.sort()
key = two(a, -pnl[int(0.01 * len(pnl))], 0.02, 'combined VaR (simulation tolerance 0.02)')
numeric(FI, 'gv-risk-two-desks', key, 3, {'added': 2, 'no-correlation': sqrt(2)})

# exotic-ranking-basket-or-calls: seeded simulation against a one-dimensional integral with a closed-form inner price
sig, rho, T = 0.25, 0.3, 1.0
half_calls = bs(100, 100, T, 0, sig)
rng = random.Random(1)
tot = 0.0
for _ in range(400000):
    z1 = rng.gauss(0, 1)
    z2 = rho * z1 + sqrt(1 - rho * rho) * rng.gauss(0, 1)
    s1 = 100 * exp(-sig * sig / 2 + sig * z1)
    s2 = 100 * exp(-sig * sig / 2 + sig * z2)
    tot += max((s1 + s2) / 2 - 100, 0)
basket_mc = tot / 400000


def inner(z1):
    """E[max((s1 + s2)/2 - 100, 0) | z1]: half a call on s2, struck at 200 - s1, s2 lognormal given z1."""
    s1 = 100 * exp(-sig * sig / 2 + sig * z1)
    sd = sig * sqrt(1 - rho * rho)
    fwd = 100 * exp(-sig * sig / 2 + sig * rho * z1 + sd * sd / 2)
    k = 200 - s1
    if k <= 0:
        return (s1 + fwd) / 2 - 100
    d1 = (log(fwd / k) + sd * sd / 2) / sd
    return 0.5 * (fwd * N.cdf(d1) - k * N.cdf(d1 - sd))


h = 1e-3
basket_int = sum(inner(-8 + (k + 0.5) * h) * N.pdf(-8 + (k + 0.5) * h) for k in range(16000)) * h
two(basket_mc, basket_int, 0.05, 'basket call (simulation tolerance 0.05)')
two(half_calls, 100 * erf(sig / 2 / sqrt(2)), 1e-9, 'at-the-money call two ways')
ok(fmt(half_calls, 2) == '9.95' and fmt(basket_int, 2) == '8.05', f'printed £9.95 and £8.05 ({half_calls}, {basket_int})')
ok(half_calls > basket_int, 'claim: the half calls cost more')
choice(FI, 'exotic-ranking-basket-or-calls', 'two half calls')
stated(FI, 'exotic-ranking-basket-or-calls', 'the half calls cost £9.95 and the basket call about £8.05')

# ---------------------------------------------------------------- behavioural-6: figures in the models
loss = F(45, 100)
ok(fmt(float(loss ** 5) * 100, 1) == '1.8', 'five losses at 55% wins: 1.8%')
state = {0: F(1)}
for _ in range(40):                                        # route A: exact chain on the current losing run
    new = {}
    for k, pr in state.items():
        new[0] = new.get(0, 0) + pr * (1 - loss)
        if k + 1 < 5:
            new[k + 1] = new.get(k + 1, 0) + pr * loss
    state = new
p_run = 1 - sum(state.values())
rng = random.Random(47)
sims = 0
for _ in range(100000):                                    # route B: seeded games of 40 trades
    run = best_run = 0
    for _ in range(40):
        run = run + 1 if rng.random() < 0.45 else 0
        best_run = max(best_run, run)
    sims += best_run >= 5
two(p_run, sims / 100000, 0.005, 'run of five losses in 40 trades (simulation tolerance 0.005)')
ok(abs(float(p_run) - 1 / 3) < 0.02, f'about one game in three ({float(p_run)})')
stated(B, 'reasoning-aloud-five-losses-running', 'about 1.8 per cent')
stated(B, 'reasoning-aloud-five-losses-running', 'about one game in three')
# project-account-too-good-to-be-true (fix pass finding 21): accuracy 91 then 84 per cent, baseline 80, held-out 83 per cent on 400 students
se = sqrt(0.83 * 0.17 / 400)
two(se, sqrt(sum((x - 0.83) ** 2 * (0.83 if x else 0.17) for x in (0, 1)) / 400), 1e-12, 'standard error of an accuracy of 83 per cent over 400 students')
ok(round(se * 100) == 2, f'about 2 points ({se * 100:.2f})')
ok(abs((0.83 - 0.80) / 0.02 - 1.5) < 1e-9 and abs((0.83 - 0.80) / se - 1.5) < 0.1, 'three points are about one and a half standard errors')
ok(91 - 80 == 11 and 84 - 80 == 4, 'edge four points, not eleven')
ok(item(B, 'project-account-too-good-to-be-true')['pace'] == 150, 'fix pass 24: pace 150')
stated(B, 'project-account-too-good-to-be-true', 'the model\'s edge was four points, not eleven')
stated(B, 'project-account-too-good-to-be-true', 'one and a half standard errors above the baseline')
stale(B, 'project-account-too-good-to-be-true', ['currency', 'hit rate', '58 per cent', '54 per cent', '53 per cent', 'moving average', 'three points of hit rate'])
# after-rejection-applied-before (finding 22): six unexplained steps a problem fell to one over fourteen sessions
ok(6 > 1 and 14 > 0, 'count of unfollowed steps fell from about six to one over fourteen sessions')
stated(B, 'after-rejection-applied-before', 'Over fourteen sessions that count fell from about six a problem to one.')
stale(B, 'after-rejection-applied-before', ['arithmetic', 'eighty-question', '45 correct', 'trading society', 'timed test'])
# final-round-questions-for-us (finding 25)
stated(B, 'final-round-questions-for-us', 'which tells me what to prepare before I start.')
stale(B, 'final-round-questions-for-us', ['Neither question is answered on a careers page'])
ok(42 - 30 == 12, 'too-much-to-do: 42 hours needed against 30 free')

# ---------------------------------------------------------------- behavioural-6 (rule 11)
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

# fix pass: no two of the 62 behavioural models share a story (a run of eight words in common) and no rubric line judges delivery
import itertools
GR = {}
for k in range(1, 9):
    for it in json.load(open(os.path.join(BANK, f'behavioural-{k}.json'), encoding='utf-8'))['items']:
        wds = re.findall(r"[a-z0-9']+", it['widget']['model'].lower())
        for i in range(len(wds) - 7):
            GR.setdefault(tuple(wds[i:i + 8]), set()).add((k, it['id']))
        if k >= 5:
            for r in it['widget']['rubric']:
                ok('no filler' not in r['text'] and 'stops cleanly' not in r['text'].lower(), f'behavioural-{k}/{it["id"]}: rubric line checkable from the text')
shared = {g: ks for g, ks in GR.items() if len(ks) > 1}
ok(not shared, f'no two of 62 models share a run of eight words ({[(" ".join(g), sorted(ks)) for g, ks in list(shared.items())[:2]]})')
ok(sum(1 for k in range(1, 9) for _ in json.load(open(os.path.join(BANK, f'behavioural-{k}.json'), encoding='utf-8'))['items']) == 62, '62 behavioural items')

# ---------------------------------------------------------------- coding-2 (rules 12 and 13; bank_2_code_check.py beside this script)
sys.path.insert(0, HERE)
import bank_2_code_check as cc
import contextlib, io
from math import comb
CO = 'coding-2'
print('coding-2 near-miss runs:')


def code(i, brute, traps):
    return cc.check_code(ok, f'{CO}/{i}', item(CO, i), brute, traps)


def tests_of(i):
    return {c['call']: c['expect'] for c in item(CO, i)['widget']['tests']}


# pf-idioms-argmax-last. Route B: max over the reversed list (max keeps the first, which is the last original).
code('pf-idioms-argmax-last',
     "def argmax_last(xs):\n    n = len(xs)\n    if n == 0:\n        return None\n    i = max(range(n), key=lambda j: xs[n - 1 - j])\n    return n - 1 - i\n",
     {'xs.index(max(xs))': "def argmax_last(xs):\n    return xs.index(max(xs)) if xs else None\n",
      'strict > in a loop': "def argmax_last(xs):\n    best = None\n    for i, x in enumerate(xs):\n        if best is None or x > xs[best]:\n            best = i\n    return best\n",
      'max over indices': "def argmax_last(xs):\n    return max(range(len(xs)), key=xs.__getitem__) if xs else None\n"})
t = tests_of('pf-idioms-argmax-last')
ok([t[k] for k in ('argmax_last([3, 7, 7, 1])', 'argmax_last([])', 'argmax_last([-2])', 'argmax_last([1, 2, 3])')] == ['2', 'None', '0', '2'], 'argmax_last: the brief values')
ok([3, 7, 7, 1].index(max([3, 7, 7, 1])) == 1, 'argmax_last: the index method gives 1')

# edge-case-list-second-largest. Route B: sorted distinct values with a length check.
code('edge-case-list-second-largest',
     "def second_largest(xs):\n    s = sorted(set(xs))\n    return s[-2] if len(s) >= 2 else None\n",
     {'sorted(xs)[-2]': "def second_largest(xs):\n    return sorted(xs)[-2]\n",
      'distinct, no guard': "def second_largest(xs):\n    return sorted(set(xs))[-2]\n",
      'guarded, repeats kept': "def second_largest(xs):\n    s = sorted(xs)\n    return s[-2] if len(s) >= 2 else None\n"})
t = tests_of('edge-case-list-second-largest')
ok([t[k] for k in ('second_largest([5, 5, 3])', 'second_largest([4])', 'second_largest([2, 2])', 'second_largest([-1, -5, -3])', 'second_largest([])')] == ['3', 'None', 'None', '-3', 'None'], 'second_largest: the brief values')
ok(sorted([5, 5, 3])[-2] == 5 and sorted([2, 2])[-2] == 2, 'second_largest: sorted(xs)[-2] gives 5 and 2')

# ds-pointers-merge-ticks. Route B: a stable sort on the time alone, a before b.
code('ds-pointers-merge-ticks',
     "def merge_ticks(a, b):\n    return sorted(a + b, key=lambda t: t[0])\n",
     {'sorted(a + b)': "def merge_ticks(a, b):\n    return sorted(a + b)\n",
      'two pointers with <': "def merge_ticks(a, b):\n    out, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i][0] < b[j][0]:\n            out.append(a[i]); i += 1\n        else:\n            out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n",
      'heapq.merge on whole tuples': "import heapq\ndef merge_ticks(a, b):\n    return list(heapq.merge(a, b))\n"})
t = tests_of('ds-pointers-merge-ticks')
ok(eval(t['merge_ticks([(1, 10.0), (4, 10.2)], [(1, 9.9), (2, 10.1), (4, 10.3)])']) == [(1, 10.0), (1, 9.9), (2, 10.1), (4, 10.2), (4, 10.3)], 'merge_ticks: the brief value')
ok(sorted([(1, 10.0), (4, 10.2), (1, 9.9), (2, 10.1), (4, 10.3)])[0] == (1, 9.9), 'merge_ticks: sorted(a + b) puts (1, 9.9) first')

# ds-arrays-round-trips. Route B: running positions by itertools.accumulate, then count zeros reached from non-zero.
code('ds-arrays-round-trips',
     "from itertools import accumulate\ndef round_trips(trades):\n    p = [0] + list(accumulate(trades))\n    return sum(1 for prev, now in zip(p, p[1:]) if now == 0 and prev != 0)\n",
     {'every zero position': "def round_trips(trades):\n    pos, count = 0, 0\n    for t in trades:\n        pos += t\n        if pos == 0:\n            count += 1\n    return count\n",
      'crossings counted too': "def round_trips(trades):\n    pos, count = 0, 0\n    for t in trades:\n        new = pos + t\n        if (new == 0 and pos != 0) or pos * new < 0:\n            count += 1\n        pos = new\n    return count\n"})
t = tests_of('ds-arrays-round-trips')
ok([t[k] for k in ('round_trips([5, -5, 3, 2, -5, 0, -1, 1])', 'round_trips([0, 0])', 'round_trips([])', 'round_trips([2, -4, 2])')] == ['3', '0', '0', '1'], 'round_trips: the brief values')
pos_, ends_ = 0, []
for k_, t_ in enumerate([5, -5, 3, 2, -5, 0, -1, 1], 1):
    if pos_ + t_ == 0 and pos_ != 0:
        ends_.append(k_)
    pos_ += t_
ok(ends_ == [2, 5, 8], 'explain: the trips end at the 2nd, 5th and 8th trades')

# pf-collections-top-symbols. Route B: collections.Counter totals and heapq.nsmallest on (minus total, symbol).
code('pf-collections-top-symbols',
     "import heapq\nfrom collections import Counter\ndef top_symbols(trades, k):\n    c = Counter()\n    for s, q in trades:\n        c[s] += q\n    return heapq.nsmallest(k, c, key=lambda s: (-c[s], s))\n",
     {'stable sort by total alone': "def top_symbols(trades, k):\n    t = {}\n    for s, q in trades:\n        t[s] = t.get(s, 0) + q\n    return sorted(t, key=lambda s: -t[s])[:k]\n",
      'Counter.most_common': "from collections import Counter\ndef top_symbols(trades, k):\n    c = Counter()\n    for s, q in trades:\n        c[s] += q\n    return [s for s, _ in c.most_common(k)]\n",
      'reverse on (total, symbol)': "def top_symbols(trades, k):\n    t = {}\n    for s, q in trades:\n        t[s] = t.get(s, 0) + q\n    return sorted(t, key=lambda s: (t[s], s), reverse=True)[:k]\n"})
tot_ = {}
for s_, q_ in [("TUV", 300), ("FGH", 500), ("TUV", 200), ("BCD", 500), ("MNO", 100)]:
    tot_[s_] = tot_.get(s_, 0) + q_
ok(tot_ == {'TUV': 500, 'FGH': 500, 'BCD': 500, 'MNO': 100}, 'top_symbols: three symbols tie at 500')
ok(sorted(tot_, key=lambda s: -tot_[s])[:2] == ['TUV', 'FGH'], 'top_symbols: the stable sort by total alone gives TUV first')

# gd-dp-walk-above-zero. Route B: a depth-first count of the walks up to n = 22, the ballot formula above.
code('gd-dp-walk-above-zero',
     "from math import comb\ndef nonneg_walk_counts(n):\n    if n <= 22:\n        out = {}\n        def go(pos, left):\n            if left == 0:\n                out[pos] = out.get(pos, 0) + 1\n                return\n            go(pos + 1, left - 1)\n            if pos > 0:\n                go(pos - 1, left - 1)\n        go(0, n)\n        return out\n    return {h: comb(n, (n - h) // 2) - (comb(n, (n - h) // 2 - 1) if (n - h) // 2 >= 1 else 0)\n            for h in range(n % 2, n + 1, 2)}\n",
     {'all 2^n paths listed': "from itertools import product\ndef nonneg_walk_counts(n):\n    out = {}\n    for steps in product((1, -1), repeat=n):\n        pos, okay = 0, True\n        for s in steps:\n            pos += s\n            if pos < 0:\n                okay = False\n                break\n        if okay:\n            out[pos] = out.get(pos, 0) + 1\n    return out\n",
      'depth-first, pruned at -1': "def nonneg_walk_counts(n):\n    out = {}\n    def go(pos, left):\n        if left == 0:\n            out[pos] = out.get(pos, 0) + 1\n            return\n        go(pos + 1, left - 1)\n        if pos > 0:\n            go(pos - 1, left - 1)\n    go(0, n)\n    return out\n",
      'the floor at 0 left out': "def nonneg_walk_counts(n):\n    c = {0: 1}\n    for _ in range(n):\n        d = {}\n        for p, w in c.items():\n            for q in (p + 1, p - 1):\n                d[q] = d.get(q, 0) + w\n        c = d\n    return c\n",
      'unreachable ends kept': "def nonneg_walk_counts(n):\n    row = [1] + [0] * n\n    for _ in range(n):\n        row = [(row[1] if len(row) > 1 else 0)] + [row[p - 1] + (row[p + 1] if p + 1 <= n else 0) for p in range(1, n + 1)]\n    return dict(enumerate(row))\n"})
t = tests_of('gd-dp-walk-above-zero')
catalan = lambda m: comb(2 * m, m) // (m + 1)
ok(eval(t['nonneg_walk_counts(10)']) == {0: 42, 2: 90, 4: 75, 6: 35, 8: 9, 10: 1} and sum(eval(t['nonneg_walk_counts(10)']).values()) == 252 == comb(10, 5), 'walks: n = 10 has 42 at 0 and 252 in all')
ok(t['nonneg_walk_counts(20)[0]'] == str(catalan(10)) == '16796', 'walks: n = 20 has 16,796 at 0 (Catalan 10)')
ok(t['sum(nonneg_walk_counts(22).values())'] == str(comb(22, 11)), 'walks: n = 22 has C(22, 11) walks in all')
ok(t['nonneg_walk_counts(60)[0]'] == str(catalan(30)) and t['sum(nonneg_walk_counts(60).values())'] == str(comb(60, 30)), 'walks: n = 60 gives Catalan 30 at 0 and C(60, 30) in all')
ok(2 ** 60 > 10 ** 18, 'explain: listing walks means up to 2^60 of them')

# pf-collections-first-of-ties: run the lines; route B scans the words keeping the first top count.
it_ = item(CO, 'pf-collections-first-of-ties')
ns_ = cc.run_snippet(it_['prose'])
words_ = 'to be or not to be'.split()
cnt_ = {w: words_.count(w) for w in words_}
first_ = None
for w in cnt_:
    if first_ is None or cnt_[w] > cnt_[first_]:
        first_ = w
ok(ns_['best'] == first_ == 'to', 'first of ties: best is "to"')
ok(ns_['d'] == {'to': 2, 'be': 2, 'or': 1, 'not': 1}, 'first of ties: the counts')
last_tie = None
for w in cnt_:
    if last_tie is None or cnt_[w] >= cnt_[last_tie]:
        last_tie = w
ok(last_tie == 'be' and list(ns_['d'])[-1] == 'not', 'first of ties: "be" is the later tie, "not" the last key inserted')
choice(CO, 'pf-collections-first-of-ties', '"to"')

# pf-functions-late-binding: run the lines; the slips bind i early and leave i out.
it_ = item(CO, 'pf-functions-late-binding')
key = cc.run_snippet(it_['prose'])['total']
two(key, 3 * (10 + 2), 0, 'late binding')
early = sum(f(10) for f in [lambda x, i=i: x + i for i in range(3)])
numeric(CO, 'pf-functions-late-binding', key, None, {'bound-early': early, 'ignored-i': 3 * 10})

# at-recursion-count-the-calls: count by instrumenting the item's own function; route B by the call recurrence.
it_ = item(CO, 'at-recursion-count-the-calls')
ns_ = cc.run_snippet(it_['prose'])
calls_ = [0]
orig_ = ns_['f']
def counted(n):
    calls_[0] += 1
    return orig_(n)
ns_['f'] = counted
value_ = counted(12)
calls = lambda n: 1 if n <= 1 else 1 + calls(n // 2) + calls(n // 3)
leaves = lambda n: 1 if n <= 1 else leaves(n // 2) + leaves(n // 3)
two(calls_[0], calls(12), 0, 'calls of f(12)')
ok(value_ == 7 and leaves(12) == 7 and calls(12) - leaves(12) == 6, 'f(12) is 7: 7 calls return 1, 6 add')
numeric(CO, 'at-recursion-count-the-calls', calls_[0], None, {'gave-value': value_, 'no-first': calls_[0] - 1})

# ds-hashing-list-membership: count the comparisons of each version with an id type that counts its == calls.
it_ = item(CO, 'ds-hashing-list-membership')
class Id:
    eqs = 0
    def __init__(self, v): self.v = v
    def __eq__(self, o):
        Id.eqs += 1
        return self.v == o.v
    def __hash__(self): return hash(self.v)
def cost(kind, n):
    Id.eqs = 0
    ids = [Id(k) for k in range(n)]
    if kind == 'set':
        seen = set()
        for x in ids:
            if x not in seen:
                seen.add(x)
    else:
        seen = [] if kind != 'tuple' else ()
        for x in ids:
            if x not in seen:
                seen = seen + (x,) if kind == 'tuple' else seen
                if kind == 'list':
                    seen.append(x)
                if kind == 'sorted':
                    seen.append(x)
                    seen.sort(key=lambda y: y.v)
    return Id.eqs
for kind in ('list', 'tuple', 'sorted'):
    ok(cost(kind, 2000) == 2000 * 1999 // 2, f'list membership: {kind} makes n(n - 1)/2 comparisons at n = 2,000')
ok(cost('set', 2000) <= 2000, 'list membership: the set makes at most one comparison per id')
# the item's own lines, on 2,000 different ids, then with the key's change (a set and add)
lines_ = cc.snippet(it_['prose'])[0]
def run_lines(src, n):
    Id.eqs = 0
    ns = {'ids': [Id(k) for k in range(n)]}
    exec(src, ns)
    return Id.eqs, ns['repeats']
two(run_lines(lines_, 2000)[0], cost('list', 2000), 0, 'list membership: the item lines make n(n - 1)/2 comparisons')
set_src = lines_.replace('seen = []', 'seen = set()').replace('seen.append(x)', 'seen.add(x)')
ok(set_src != lines_ and run_lines(set_src, 2000) == (0, 0), 'list membership: with a set the item lines make no comparisons on different ids')
ok(run_lines(lines_, 2000)[1] == 0, 'list membership: different ids give no repeats')
two(sum(range(20000)), 20000 * 19999 // 2, 0, 'comparisons for 20,000 ids')
ok(sum(range(20000)) == 199990000, '199,990,000 comparisons')
stated(CO, 'ds-hashing-list-membership', '0 + 1 + \\\\dots + 19{,}999 = 199{,}990{,}000')
choice(CO, 'ds-hashing-list-membership', 'set')

# pf-idioms-spent-generator: run the lines and capture what they print; route B by the sum-of-squares formula.
it_ = item(CO, 'pf-idioms-spent-generator')
buf_ = io.StringIO()
with contextlib.redirect_stdout(buf_):
    cc.run_snippet(it_['prose'])
ok(buf_.getvalue() == '14 0\n', f'spent generator prints "14 0" (printed {buf_.getvalue()!r})')
two(sum(x * x for x in range(4)), 3 * 4 * 7 // 6, 0, 'sum of squares 0 to 3')
choice(CO, 'pf-idioms-spent-generator', '`14 0`')

# copy-vs-move-vector-copy (C++ reading): compile and run the C++ lines; run the Python lines.
it_ = item(CO, 'copy-vs-move-vector-copy')
ns_ = cc.run_snippet(it_['prose'])
ok((len(ns_['v']), len(ns_['w'])) == (4, 4) and ns_['v'] is ns_['w'], 'Python: one list of 4, two names')
cpp_body = cc.snippet(it_['prose'], 'cpp')[0]
out = cc.cpp('#include <cstdio>\n#include <vector>\nint main() {\n' + cpp_body + 'std::printf("%zu %zu %d\\n", v.size(), w.size(), int(v.data() != w.data()));\n}\n')
if out is not None:
    ok(out.split() == ['3', '4', '1'], f'C++: v has 3, w has 4, separate storage (ran: {out.strip()})')
choice(CO, 'copy-vs-move-vector-copy', 'C++: 3 and 4. Python: 4 and 4.')

# coding-2 file shape (section 2): six code, five reasoning (numeric or choice), one C++ reading choice
kinds = [x['widget']['kind'] for x in DATA[CO]['items']]
ok(kinds.count('code') == 6 and kinds.count('numeric') == 2 and kinds.count('choice') == 4, f'coding-2 kinds {kinds}')
ok(sorted(x['difficulty'] for x in DATA[CO]['items']) == [2] * 3 + [3] * 7 + [4, 5], 'coding-2 difficulties: D2 3, D3 7, D4 1, D5 1')
ok(all(x['style'] == 'coding' for x in DATA[CO]['items']), 'coding-2 style')

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
        blob = json.dumps(it, ensure_ascii=False).replace('!=', '')   # Python's != in code is not an exclamation mark
        ok(not re.search(r'\bpercent\b', blob.lower()) and '!' not in blob and '—' not in blob, f'{f}/{it["id"]}: voice (no percent, !, em-dash)')

counts = {f: len(DATA[f]['items']) for f in FILES}
ok(counts == {'statistics-2': 15, 'finance-2': 15, 'behavioural-6': 8, 'coding-2': 12}, f'item counts {counts}')

print(f'{checks[0]} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
