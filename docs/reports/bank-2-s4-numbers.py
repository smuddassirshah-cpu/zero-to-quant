#!/usr/bin/env python3
"""Bank part 2, session 4: every key, slip and stated figure in statistics-4, finance-4, behavioural-8 and coding-4, by two routes.

coding-4: each solution runs on every example and hidden test, the untouched starter fails, a brute-force twin agrees on every
test, and each named trap (near-miss) fails a hidden test; slow traps run in a fresh CPython with a 5 s limit. Reading
items run their own lines; the C++ item is checked by constant evaluation with g++ -std=c++20 -fsyntax-only.

Standard library only (runs under plain python3). numbers_lib.py has no Bank loader yet (B2-E4), so the JSON is read here.
Route A is exact (Fraction) or closed form; route B is enumeration, a seeded simulation with a stated tolerance, a
numerical solve or integral, or a step-by-step loop that shares no code with route A. Each slip is computed by carrying
out the slip its byKey line names. Each value is then asserted at its path in the JSON. Exit 0 means every check passed.
"""
import json, math, os, random, re, sys
from fractions import Fraction as F
from math import sqrt, exp, log, erf, pi, comb, lgamma
from itertools import combinations, permutations, product
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, '..', '..', 'app', 'content', 'bank')
FILES = ['statistics-4', 'finance-4', 'behavioural-8', 'coding-4']
DATA = {f: json.load(open(os.path.join(BANK, f + '.json'), encoding='utf-8')) for f in FILES}
ITEMS = {(f, it['id']): it for f in FILES for it in DATA[f]['items']}
fails, checks = [], [0]
N = NormalDist()
FREE = 'free'      # the question asks "as a decimal" (no rounding): the stored key must hold the exact value


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
    return a


def item(f, i):
    it = ITEMS.get((f, i))
    ok(it is not None, f'{f}/{i} exists')
    return it


def numeric(f, i, key, asked, slips):
    """key: the computed value. asked: places the question asks for, None for a whole number, FREE for "as a decimal".
    slips: {wrong id: computed slip value}. Checks the stored answer, its band, every wrong value and band, and byKey."""
    it = item(f, i)
    w = it['widget']
    ok(w['kind'] == 'numeric', f'{f}/{i}: numeric')
    scale = 100 if w.get('unit') == '%' else 1
    ans, tol = w['answer'], w['tol']['abs']
    lab = f'{f}/{i}'
    ok(abs(ans - float(key)) <= tol + 1e-12, f'{lab}: computed key {float(key)} inside stored band {ans} +- {tol}')
    if isinstance(asked, int):
        rounded = round(float(key) * scale, asked) / scale
        ok(abs(rounded - ans) <= tol + 1e-12, f'{lab}: rounded key {rounded} inside band')
        close(ans, key, 0.5 * 10 ** -asked / scale, f'{lab}: stored answer within half a unit of the exact value')
    elif asked is None:
        ok(float(key) * scale == round(float(key) * scale) and abs(ans - float(key)) < 1e-12, f'{lab}: whole key {key} stored exactly')
    else:
        close(ans, key, 1e-9, f'{lab}: stored answer is the exact value')
    ids = {x['id']: x for x in w['wrong']}
    ok(set(ids) == set(slips), f'{lab}: wrong ids {sorted(ids)} match computed slips {sorted(slips)}')
    ok(len(ids) >= 2, f'{lab}: at least two wrong entries')
    for wid, v in slips.items():
        x = ids.get(wid)
        if not x:
            continue
        v = float(v)
        ok(abs(x['value'] - v) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: computed slip {v} inside its band {x["value"]} +- {x["tol"]["abs"]}')
        if isinstance(asked, int):
            ok(abs(x['value'] - round(v * scale, asked) / scale) <= x['tol']['abs'] + 1e-12, f'{lab}.{wid}: slip as rounded inside its band')
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
    strip = lambda t: t.replace('$', '')
    others = max(len(strip(o['text'])) for o in opts if not o.get('correct'))
    ok(len(strip(corr[0]['text'])) - others <= 9, f'{f}/{i}: key not longer than the longest distractor by more than 9')
    ok(it['widget'].get('shuffle', True) is True, f'{f}/{i}: shuffle on')
    ok(len({o['text'] for o in opts}) == 4, f'{f}/{i}: options distinct')
    return it


def fmt(x, dp):
    return f'{float(x):.{dp}f}'


def ols(x, y):
    """Simple least squares with intercept: slope, its usual standard error, residuals."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx
    res = [c - a0 - b * a for a, c in zip(x, y)]
    return b, sqrt(sum(r * r for r in res) / (n - 2) / sxx), res


def corr(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def bs_call(S0, K, T, r, sig):
    d1 = (log(S0 / K) + (r + sig * sig / 2) * T) / (sig * sqrt(T))
    return S0 * N.cdf(d1) - K * exp(-r * T) * N.cdf(d1 - sig * sqrt(T))


def Phi_erf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


S, FI, B = 'statistics-4', 'finance-4', 'behavioural-8'

# ---------------------------------------------------------------- statistics-4
# es-estimators-error-of-the-vol: sigma/sqrt(2n) against the exact sd of s (c4 constant) and a seeded simulation
n, s = 50, 1.2
a = s / sqrt(2 * n)
c4 = sqrt(2 / (n - 1)) * exp(lgamma(n / 2) - lgamma((n - 1) / 2))
exact = s * sqrt(1 - c4 ** 2)
rng = random.Random(4)
sds = []
for _ in range(40000):
    xs = [rng.gauss(0, s) for _ in range(n)]
    m = sum(xs) / n
    sds.append(sqrt(sum((v - m) ** 2 for v in xs) / (n - 1)))
ms = sum(sds) / len(sds)
sim = sqrt(sum((v - ms) ** 2 for v in sds) / (len(sds) - 1))
two(exact, sim, 0.002, 'sd of s: exact c4 route against simulation (tolerance 0.002)')
two(a, exact, 0.005, 'large-sample value inside half a unit of the exact small-sample value')
ok(fmt(a, 2) == '0.12' and fmt(exact, 2) == '0.12', f'both round to 0.12 ({a}, {exact})')
numeric(S, 'es-estimators-error-of-the-vol', a / 100, 2, {'root-of-n': s / sqrt(n) / 100, 'divided-by-n': s / n / 100})
ok(fmt(1.2 - 2 * a, 2) == '0.96' and fmt(1.2 + 2 * a, 2) == '1.44', 'rough range 0.96 to 1.44')
stated(S, 'es-estimators-error-of-the-vol', '0.96% to 1.44%')

# es-mle-best-precision-rate: Cramer-Rao bound against Fisher information summed over every binomial outcome
p, n = F(1, 5), 100
info_a = n / (p * (1 - p))
info_b = sum(comb(n, k) * p ** k * (1 - p) ** (n - k) * (F(k) / p - F(n - k) / (1 - p)) ** 2 for k in range(n + 1))
two(info_a, info_b, 0, 'information 625 two ways')
ok(info_a == 625 and 1 / (p * (1 - p)) == F(25, 4), 'per trial 6.25, total 625')
var_phat = sum(comb(n, k) * p ** k * (1 - p) ** (n - k) * (F(k, n) - p) ** 2 for k in range(n + 1))
ok(var_phat == 1 / info_a, 'claim: the sample proportion attains the bound (variance 0.0016)')
key = sqrt(1 / info_a)
numeric(S, 'es-mle-best-precision-rate', two(key, sqrt(var_phat), 1e-15, 'smallest sd 0.04'), FREE,
        {'gave-variance': 1 / info_a, 'one-trial': sqrt(p * (1 - p))})

# es-intervals-two-desk-gap: Fraction route against a pooled-form float route
se2 = F(4, 50) + F(4, 50)
ok(se2 == F(16, 100), 'variance of the gap 0.16, so se 0.4')
a = F(104, 10) - F(96, 10) - F(196, 100) * F(4, 10)
b = (10.4 - 9.6) - 1.96 * 2 * sqrt(1 / 50 + 1 / 50)
key = two(a, b, 1e-12, 'lower end')
numeric(S, 'es-intervals-two-desk-gap', key, 3,
        {'one-mean': 0.8 - 1.96 * 2 / sqrt(50), 'upper-end': F(8, 10) + F(196, 100) * F(4, 10)})
ok(fmt(2 / sqrt(50), 3) == '0.283', 'one-mean error 0.283')

# es-bayes-three-from-three: Laplace's rule against a midpoint integral of p * p^3 / p^3
a = F(3 + 1, 3 + 2)
h = 1e-5
num_, den = 0.0, 0.0
for k in range(100000):
    q = (k + 0.5) * h
    num_ += q ** 4
    den += q ** 3
key = two(a, num_ / den, 1e-8, 'predictive chance')
numeric(S, 'es-bayes-three-from-three', key, FREE, {'no-prior': F(3, 3), 'one-failure': F(3, 3 + 1)})

# sm-nonpar-shuffled-labels: combinations against all 120 orderings of the pooled values
vals = [8, 9, 1, 2, 3]
obs = F(8 + 9, 2) - F(1 + 2 + 3, 3)
diff = lambda A: F(sum(A), 2) - F(sum(vals) - sum(A), 3)
splits = list(combinations(vals, 2))
a = F(sum(diff(A) >= obs for A in splits), len(splits))
perms = list(permutations(vals))
b = F(sum(diff(pp[:2]) >= obs for pp in perms), len(perms))
key = two(a, b, 0, 'permutation p-value')
ok(obs == F(13, 2) and len(splits) == 10, 'observed gap 6.5, 10 splits')
numeric(S, 'sm-nonpar-shuffled-labels', key, FREE, {'ordered-pairs': F(1, 20), 'two-sided': 2 * key})
ok(sum(1 for A in splits if abs(diff(A)) >= obs) == 1, 'note: the two-sided count is also 1 (no split as low), so doubling is the slip')

# ht-setup-one-or-two-sided: NormalDist against erf
p1 = two(1 - N.cdf(1.8), 1 - Phi_erf(1.8), 1e-12, 'one-sided p')
ok(fmt(p1, 3) == '0.036' and fmt(2 * p1, 3) == '0.072', f'p-values {p1} {2 * p1}')
ok(p1 < 0.05 < 2 * p1, 'one-sided rejects, two-sided does not')
two(N.inv_cdf(0.95), 1.645, 0.0005, 'one-sided cut-off 1.645')
two(N.inv_cdf(0.975), 1.96, 0.0005, 'two-sided cut-off 1.96')
choice(S, 'ht-setup-one-or-two-sided', 'Yes one-sided, with p = 0.036')
stated(S, 'ht-setup-one-or-two-sided', '1 - \\\\Phi(1.8) = 0.036')

# ht-multiple-better-of-two: 1/sqrt(pi) against the integral of 2 z phi(z) Phi(z) and a seeded simulation
a = 1 / sqrt(pi)
h = 1e-3
b = sum(2 * z * N.pdf(z) * N.cdf(z) * h for z in ((k + 0.5) * h - 10 for k in range(20000)))
two(a, b, 1e-6, 'expected maximum by integral')
rng = random.Random(8)
m = sum(max(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(400000)) / 400000
two(a, m, 0.005, 'expected maximum by 400,000 seeded pairs (tolerance 0.005)')
abs_mean = sqrt(2 / pi)
two(abs_mean, 2 * sum(z * N.pdf(z) * h for z in ((k + 0.5) * h for k in range(10000))), 1e-6, 'mean size of one statistic')
numeric(S, 'ht-multiple-better-of-two', a, 3, {'no-selection': 0, 'one-size': abs_mean})
two(sqrt(2) * abs_mean, 2 / sqrt(pi), 1e-12, 'E|X - Y| = 2/sqrt(pi)')

# power-half-the-effect: n scales as 1/effect^2, against the power function itself
d = (1.96 + N.inv_cdf(0.8)) / sqrt(150)          # the effect, in sd units, that gives 80% power at n = 150
pw = lambda n, eff: N.cdf(sqrt(n) * eff - 1.96)
close(pw(150, d), 0.8, 1e-9, 'planned power 80% at 150')
a = 150 * F(1) / F(1, 2) ** 2
b = next(k for k in range(1, 5000) if pw(k, d / 2) >= 0.8 - 1e-12)
key = two(a, b, 0, 'observations for half the effect')
numeric(S, 'power-half-the-effect', int(key), None, {'doubled': 300, 'root-two': 150 * sqrt(2)})

# rg-fit-next-year-return: regression line against a seeded sample of 400,000 correlated pairs
a = F(6) + F(1, 2) * F(10, 10) * (26 - 6)
rng = random.Random(9)
xs, ys = [], []
for _ in range(400000):
    z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1)
    xs.append(6 + 10 * z1)
    ys.append(6 + 10 * (0.5 * z1 + sqrt(0.75) * z2))
bb, _, _ = ols(xs, ys)
b = sum(ys) / len(ys) + bb * (26 - sum(xs) / len(xs))
key = two(a, b, 0.1, 'forecast by fitted line (simulation tolerance 0.1 points)')
numeric(S, 'rg-fit-next-year-return', a / 100, None, {'no-pull': F(26, 100), 'halved-return': F(13, 100)})

# rg-inference-overall-f: formula against sums of squares from a real least-squares fit built to R^2 = 0.3


def solve(A, y):
    """Gaussian elimination."""
    m = len(A)
    M = [row[:] + [v] for row, v in zip(A, y)]
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(m):
            if r != c:
                f_ = M[r][c] / M[c][c]
                M[r] = [u - f_ * v for u, v in zip(M[r], M[c])]
    return [M[r][m] / M[r][r] for r in range(m)]


def fit(X, y):
    k = len(X[0])
    XtX = [[sum(r[i] * r[j] for r in X) for j in range(k)] for i in range(k)]
    Xty = [sum(r[i] * v for r, v in zip(X, y)) for i in range(k)]
    beta = solve(XtX, Xty)
    return [sum(bi * xi for bi, xi in zip(beta, r)) for r in X]


rng = random.Random(10)
X = [[1.0] + [rng.gauss(0, 1) for _ in range(3)] for _ in range(44)]
y0 = [rng.gauss(0, 1) for _ in range(44)]
yh = fit(X, y0)
my = sum(y0) / 44
expl = [v - my for v in yh]
res = [u - v for u, v in zip(y0, yh)]
ess, rss = sum(v * v for v in expl), sum(v * v for v in res)
y1 = [my + e * sqrt(0.3 / ess) + r * sqrt(0.7 / rss) for e, r in zip(expl, res)]     # TSS 1, R^2 0.3
yh1 = fit(X, y1)
m1 = sum(y1) / 44
tss1 = sum((v - m1) ** 2 for v in y1)
rss1 = sum((u - v) ** 2 for u, v in zip(y1, yh1))
close(1 - rss1 / tss1, 0.3, 1e-9, 'built data has R^2 0.3')
b = ((tss1 - rss1) / 3) / (rss1 / 40)
a = (F(3, 10) / 3) / (F(7, 10) / 40)
key = two(a, b, 1e-8, 'overall F')
ok(a == F(40, 7), 'F = 40/7')
numeric(S, 'rg-inference-overall-f', key, 2, {'df-41': (F(3, 10) / 3) / (F(7, 10) / 41), 'no-df': F(3, 10) / F(7, 10)})
ok(F(7, 10) / 40 == F(175, 10000), '0.7/40 = 0.0175')

# rg-diagnostics-most-leverage: formula against the diagonal of the hat matrix X (X'X)^-1 X'
xv = [1, 2, 3, 4, 20]
mx = F(sum(xv), 5)
sxx = sum((x - mx) ** 2 for x in xv)
h_a = [F(1, 5) + (x - mx) ** 2 / sxx for x in xv]
s0, s1, s2 = 5, sum(xv), sum(x * x for x in xv)
det = F(s0 * s2 - s1 * s1)
h_b = [(s2 - 2 * s1 * x + s0 * x * x) / det for x in xv]
ok(h_a == h_b, 'hat values two ways')
ok(mx == 6 and sxx == 250 and h_a[-1] == F(984, 1000), 'mean 6, Sxx 250, leverage 0.984')
ok(max(h_a[:4]) == F(3, 10), 'every other point 0.3 or less')
choice(S, 'rg-diagnostics-most-leverage', 'x = 20')

# rg-multiple-dummy-and-slope
fitv = lambda x, D, inter=True: 3 + 2 * x + 4 * D + (F(3, 2) * x * D if inter else 0)
a = fitv(2, 1)
b = (3 + 4) + (2 + F(3, 2)) * 2                      # the D = 1 line: intercept 7, slope 3.5
key = two(a, b, 0, 'fitted value')
numeric(S, 'rg-multiple-dummy-and-slope', int(key), None, {'no-interaction': fitv(2, 1, False), 'other-group': fitv(2, 0)})

# gv-models-ewma-after-a-shock: the update formula against an EWMA run as a weighted sum over a long flat history
a = sqrt(0.94 * 1 + 0.06 * 9)
lam = 0.94
hist = [1.0] * 3000 + [3.0]                             # squared returns of 1 for a long time give a variance of 1
var = sum((1 - lam) * lam ** k * r * r for k, r in enumerate(reversed(hist)))
key = two(a, sqrt(var), 1e-9, 'new volatility')
numeric(S, 'gv-models-ewma-after-a-shock', key / 100, 2,
        {'averaged-vols': (0.94 * 1 + 0.06 * 3) / 100, 'weights-swapped': sqrt(0.06 * 1 + 0.94 * 9) / 100})
ok(F(94, 100) + F(6, 100) * 9 == F(148, 100) and key - 1 > 0.2, 'variance 1.48; a rise of more than a fifth')

# gv-forecast-long-run-vol: closed form against iterating the variance forecast to its limit
w_, al, be = 0.0000045, 0.10, 0.88
a = sqrt(w_ / (1 - al - be))
v = 0.0001
for _ in range(5000):
    v = w_ + (al + be) * v
key = two(a, sqrt(v), 1e-12, 'long-run daily vol')
ok(abs(w_ / (1 - al - be) - 0.000225) < 1e-15, 'variance 0.000225')
numeric(S, 'gv-forecast-long-run-vol', key, 1, {'annualised': key * sqrt(252), 'one-minus-beta': sqrt(w_ / (1 - be))})

# co-spurious-two-walks: seeded simulation; the t statistic two ways (slope over its error, and from r)
rng = random.Random(20261111)


def walk(nn):
    out, x = [], 0.0
    for _ in range(nn):
        x += rng.gauss(0, 1)
        out.append(x)
    return out


def rates(pairs, steps):
    lev, dif, gap = 0, 0, 0.0
    for _ in range(pairs):
        x, y = walk(steps), walk(steps)
        b1, se1, _ = ols(x, y)
        t1 = b1 / se1
        r = corr(x, y)
        gap = max(gap, abs(t1 - r * sqrt(steps - 2) / sqrt(1 - r * r)))
        lev += abs(t1) > 1.96
        dx = [u - v for u, v in zip(x[1:], x)]
        dy = [u - v for u, v in zip(y[1:], y)]
        b2, se2, _ = ols(dx, dy)
        dif += abs(b2 / se2) > 1.96
    return lev / pairs, dif / pairs, gap


lev, dif, gap = rates(1000, 500)
ok(gap < 1e-8, f't statistic two ways agree (largest gap {gap})')
lev100, _, _ = rates(1000, 100)
ok(lev100 < lev, f'claim: the longer sample rejects more often ({lev100} at 100 steps, {lev} at 500)')
ok(abs(dif - 0.05) < 0.02 and lev > 0.5, f'differenced rate near 5% ({dif}); levels far above ({lev})')
CO = {'levels': fmt(100 * lev, 1), 'diffs': fmt(100 * dif, 1)}
print('co-spurious figures:', CO, 'at 100 steps', lev100)
choice(S, 'co-spurious-two-walks', 'far more often than 5%')
stated(S, 'co-spurious-two-walks', f'500 steps, {CO["levels"]}% had')
stated(S, 'co-spurious-two-walks', f'{CO["diffs"]}% did')
if len(sys.argv) > 1 and sys.argv[1] == '--co-figs':
    json.dump(CO, open(sys.argv[2], 'w'))

# ---------------------------------------------------------------- finance-4
# fi-interest-one-year-forward-rate: Fraction against compounding a pound year by year in floats
a = F(104, 100) ** 2 / F(103, 100) - 1
pound = 1.0 * 1.04 * 1.04
b = pound / 1.03 - 1
key = two(a, b, 1e-12, 'forward rate')
numeric(FI, 'fi-interest-one-year-forward-rate', key, 2, {'linear': F(2 * 4 - 3, 100), 'gap': F(1, 100)})
ok(F(104, 100) ** 2 == F(10816, 10000) and fmt(F(10816, 10000) / F(103, 100), 6) == '1.050097', '1.0816 and 1.050097')

# fi-bonds-duration-and-convexity: Fraction against finite differences of a price built with D = 8, C = 80
dy = F(1, 100)
a = -8 * dy + F(1, 2) * 80 * dy ** 2
P = lambda y: 1 - 8 * y + 40 * y * y                  # a price curve with modified duration 8 and convexity 80 at y = 0
hh = 1e-4
D_fd = -(P(hh) - P(-hh)) / (2 * hh) / P(0)
C_fd = (P(hh) - 2 * P(0) + P(-hh)) / hh ** 2 / P(0)
two(D_fd, 8, 1e-9, 'duration of the built price')
two(C_fd, 80, 1e-4, 'convexity of the built price')
key = two(a, P(0.01) / P(0) - 1, 1e-12, 'price change')
numeric(FI, 'fi-bonds-duration-and-convexity', key, 1, {'duration-only': -8 * dy, 'no-half': -8 * dy + 80 * dy ** 2, 'sign': -key})

# fi-equity-combine-two-sharpes: closed form against a search over weights
a = sqrt(F(36, 100) + F(64, 100))
s1, s2 = 0.10, 0.20                                   # any vols: means are Sharpe times vol
mu1, mu2 = 0.6 * s1, 0.8 * s2
best = max(((w * mu1 + (1 - w) * mu2) / sqrt(w * w * s1 * s1 + (1 - w) ** 2 * s2 * s2), w) for w in (k / 100000 for k in range(100001)))
key = two(a, best[0], 1e-6, 'best Sharpe')
ok(best[0] <= a + 1e-12, 'claim: no mix beats 1.0')
w_star = (0.6 / s1) / (0.6 / s1 + 0.8 / s2)
two(best[1], w_star, 1e-4, 'best weight is proportional to Sharpe over vol')
numeric(FI, 'fi-equity-combine-two-sharpes', key, 1, {'average': (0.6 + 0.8) / 2, 'sum': 0.6 + 0.8})

# fi-forwards-implied-rate: logs against a bisection on 100 e^(r/2) = 102
a = 2 * log(1.02)
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 100 * exp(mid / 2) < 102 else (lo, mid)
key = two(a, lo, 1e-12, 'implied continuous rate')
numeric(FI, 'fi-forwards-implied-rate', key, 2, {'simple': F(2, 100) * 2, 'annual-effective': F(102, 100) ** 2 - 1})
ok(fmt(key, 4) == '0.0396', '0.0396')
two((1 + 0.04 / 2) ** 2 - 1, 0.0404, 1e-12, 'note: twice-yearly compounding at 4% is the 4.04% effective rate')

# digital-option-from-two-calls: call-spread slope against a Black-Scholes check of the approximation
a = (F(590, 100) - F(370, 100)) / 4
key = two(a, (5.90 - 3.70) / (102 - 98), 1e-12, 'digital estimate')
numeric(FI, 'digital-option-from-two-calls', key, 2, {'no-width': F(220, 100), 'half-width': F(220, 100) / 2})

# op-strategies-protective-put-floor: closed form against a scan of the expiry value
a = 120 + 3 - 110
scan = max(123 - (s_ + max(110 - s_, 0)) for s_ in (k / 10 for k in range(0, 3001)))
key = two(a, scan, 1e-9, 'largest loss')
numeric(FI, 'op-strategies-protective-put-floor', key, None, {'no-premium': 120 - 110, 'took-off-premium': 120 - 110 - 3})

# op-parity-exercise-before-dividend: parity value of holding against the dividend rule
exercise = 60 - 50
hold = (60 - F(2)) - (50 - F(30, 100)) + F(50, 100)
gain_a = exercise - hold
gain_b = F(2) - (F(30, 100) + F(50, 100))
two(gain_a, gain_b, 0, 'exercise gain')
ok(hold == F(88, 10) and gain_a == F(12, 10), 'hold 8.80, gain 1.20')
choice(FI, 'op-parity-exercise-before-dividend', 'Yes: the £2.00 dividend')
stated(FI, 'op-parity-exercise-before-dividend', '58 - 49.70 + 0.50 = 8.80')

# gamma-pnl-hedger-trades: N(d1) against a finite difference of Black-Scholes, at 20% vol, three months, zero rates
d_a = [N.cdf(log(S0 / 100) / (0.2 * 0.5) + 0.2 * 0.5 / 2) for S0 in (100, 101)]
d_b = [(bs_call(S0 + 1e-4, 100, 0.25, 0, 0.2) - bs_call(S0 - 1e-4, 100, 0.25, 0, 0.2)) / 2e-4 for S0 in (100, 101)]
two(d_a[0], d_b[0], 1e-6, 'delta at 100')
two(d_a[1], d_b[1], 1e-6, 'delta at 101')
ok(fmt(d_a[0], 2) == '0.52' and fmt(d_a[1], 2) == '0.56', f'deltas {d_a}')
choice(FI, 'gamma-pnl-hedger-trades', 'Sell more shares')
stated(FI, 'gamma-pnl-hedger-trades', 'from 0.52 to 0.56')
ok(fmt(d_a[1] - d_a[0], 2) == '0.04', 'sell 0.04 shares per call')
stated(FI, 'gamma-pnl-hedger-trades', 'sell 0.04 shares')

# op-greeks-put-delta-from-call: parity against finite differences of Black-Scholes at a call delta of 0.62
a = F(62, 100) - 1
d1 = N.inv_cdf(0.62)
sig, T = 0.3, 1.0
S0 = 100 * exp(d1 * sig * sqrt(T) - sig * sig * T / 2)    # the share price at which the call's delta is 0.62
put = lambda x: bs_call(x, 100, T, 0, sig) - x + 100
pd = (put(S0 + 1e-4) - put(S0 - 1e-4)) / 2e-4
key = two(a, pd, 1e-6, 'put delta')
numeric(FI, 'op-greeks-put-delta-from-call', key, 2, {'sign': -key, 'copied-call': F(-62, 100)})

# tp-multistep-lookback-two-step: path enumeration against backward induction on (price, running high)
q = F(1 - F(8, 10), F(12, 10) - F(8, 10))
ok(q == F(1, 2), 'q = 0.5')
paths = list(product([F(12, 10), F(8, 10)], repeat=2))


def path_val(pp):
    s_, hi_ = F(100), F(100)
    for m_ in pp:
        s_ *= m_
        hi_ = max(hi_, s_)
    return hi_ - 100, s_


a = sum((q if pp[0] > 1 else 1 - q) * (q if pp[1] > 1 else 1 - q) * path_val(pp)[0] for pp in paths)


def back(s_, hi_, steps):
    if steps == 0:
        return hi_ - 100
    up, dn = s_ * F(12, 10), s_ * F(8, 10)
    return q * back(up, max(hi_, up), steps - 1) + (1 - q) * back(dn, max(hi_, dn), steps - 1)


key = two(a, back(F(100), F(100), 2), 0, 'lookback price')
ok(sorted(path_val(pp)[0] for pp in paths) == [0, 0, 20, 44], 'highs less 100: 44, 20, 0, 0')
plain = sum(F(1, 4) * max(path_val(pp)[1] - 100, 0) for pp in paths)
paying = [path_val(pp)[0] for pp in paths if path_val(pp)[0] > 0]
numeric(FI, 'tp-multistep-lookback-two-step', key, None, {'plain-call': plain, 'paying-paths': F(sum(paying), len(paying))})

# ms-book-opening-auction: candidate limit prices against a fine price scan
buys = [(300, 10.3), (200, 10.2), (400, 10.1)]
sells = [(250, 10.0), (300, 10.1), (300, 10.2)]
vol = lambda px: min(sum(q_ for q_, l in buys if l >= px - 1e-9), sum(q_ for q_, l in sells if l <= px + 1e-9))
cands = {px: vol(px) for px in (10.0, 10.1, 10.2, 10.3)}
a = max(cands.values())
scan = max(vol(k / 100) for k in range(990, 1041))
key = two(a, scan, 0, 'auction volume')
ok(cands == {10.0: 250, 10.1: 550, 10.2: 500, 10.3: 300}, f'volumes by price {cands}')
numeric(FI, 'ms-book-opening-auction', key, None, {'cleared-high': cands[10.2], 'all-sells': sum(q_ for q_, _ in sells)})

# ms-orders-immediate-or-cancel: level sum against a share-by-share fill
offers = [(400, 30.03), (300, 30.05), (600, 30.06)]
a = sum(min(q_, 1000) for q_, px in offers if px <= 30.05)
left, filled = 1000, 0
for q_, px in offers:
    for _ in range(q_):
        if left and px <= 30.05:
            left -= 1
            filled += 1
key = two(a, filled, 0, 'shares filled')
numeric(FI, 'ms-orders-immediate-or-cancel', key, None, {'ignored-limit': 1000, 'first-level': offers[0][0]})

# ms-costs-participation-time: Fraction against an hour-by-hour loop
a = F(60000) / (F(1, 10) * 150000)
hours, left = 0, 60000
while left > 0:
    left -= 15000
    hours += 1
key = two(a, hours, 0, 'hours')
numeric(FI, 'ms-costs-participation-time', int(key), None, {'no-rate': F(60000, 150000), 'rate-twice': F(60000) / (F(1, 100) * 150000)})

# option-estimate-straddle-implied-move: the 0.8 rule against an exact Black-Scholes solve
a = F(4) / F(8, 10) / 50
straddle = lambda x: 2 * 50 * (2 * N.cdf(x / 2) - 1)       # at-the-money straddle at zero rates, x = sigma sqrt(T)
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if straddle(mid) < 4 else (lo, mid)
close(a, lo, 0.0005, 'rule inside the key band of the exact implied move')
ok(fmt(100 * lo, 2) == '10.03', f'exact move {lo}')
two(2 * (bs_call(50, 50, 1, 0, lo)) , straddle(lo), 1e-9, 'straddle formula against two Black-Scholes calls (parity at zero rates)')
ok(fmt(sqrt(2 / pi), 3) == '0.798', 'sqrt(2/pi) 0.798')
numeric(FI, 'option-estimate-straddle-implied-move', a, None, {'no-factor': F(4, 50), 'times-factor': F(4, 50) * F(8, 10)})

# tp-bs-delta-and-finishing-chance: d2 from d1 against a seeded risk-neutral simulation of the finish
sig, T = 0.25, 0.5
d1 = N.inv_cdf(0.30)
pa = N.cdf(d1 - sig * sqrt(T))
K = exp(-(d1 * sig * sqrt(T) - sig * sig * T / 2))       # the strike, share at 1, at which delta is 0.30
rng = random.Random(12)
hits = sum(exp(-sig * sig * T / 2 + sig * sqrt(T) * rng.gauss(0, 1)) > K for _ in range(400000))
key = two(pa, hits / 400000, 0.002, 'chance in the money (simulation tolerance 0.002)')
ok(fmt(100 * pa, 1) == '24.2' and pa < 0.30, f'chance {pa}')
choice(FI, 'tp-bs-delta-and-finishing-chance', 'Below 30%')
stated(FI, 'tp-bs-delta-and-finishing-chance', 'chance of 24.2%')

# ---------------------------------------------------------------- behavioural-8 (rule 11)
for it in DATA[B]['items']:
    w = it['widget']
    lab = f'{B}/{it["id"]}'
    ok(w['kind'] == 'longform' and 'prose' not in it, f'{lab}: longform, no prose')
    words = len(w['model'].split())
    ok(120 <= words <= 180, f'{lab}: model {words} words')
    ok([r['points'] for r in w['rubric']] == [2, 2, 2, 2, 1, 1], f'{lab}: rubric 2,2,2,2,1,1')
    q_ = it['question']
    ok(q_.startswith('Answer aloud, then type it: ') and 3 <= len(q_.split(': ', 1)[1].split()) <= 6 and q_.endswith('.'), f'{lab}: question line')
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

# figures inside the models
seqs = list(product('HT', repeat=6))
ok(F(1, 2) ** 5 == F(1, 32) and len(seqs) == 64 and sum(s_[:5] == tuple('HHHHH') for s_ in seqs) == 2, 'coin model: 1/32, 64 sequences, two start HHHHH')
stated(B, 'reasoning-aloud-correct-me-politely', 'one time in 32')


def wait_closed(k):
    return 2 ** (k + 1) - 2


def wait_chain(k):                                     # expected flips to k heads in a row, by solving the chain backwards
    # E_j = 1 + 0.5 E_{j+1} + 0.5 E_0, E_k = 0; write E_j = a_j + b_j E_0
    a_, b_ = F(0), F(0)
    for _ in range(k):
        a_, b_ = 1 + F(1, 2) * a_, F(1, 2) * b_ + F(1, 2)
    return a_ / (1 - b_)


ok(wait_closed(2) == wait_chain(2) == 6 and wait_closed(3) == wait_chain(3) == 14, 'three heads in a row takes 14 flips (6 is two heads)')
stated(B, 'final-round-earlier-answer-was-wrong', 'takes 6 flips on average, and I now think it is 14')
cut = 1 - F(31, 10) / F(46, 10)
ok(abs(cut - F(1, 3)) < F(1, 100), f'project model: 3.1 against 4.6 is about a third less ({float(cut)})')
ok(3 * 20 == 60, 'dull-task model: three Fridays of twenty sheets is sixty sheets')
stated(B, 'star-story-dull-task-done-well', 'sixty sheets')

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
    for name, src, call, small_calls in slow_traps:
        c = next(t for t in ts if t['call'] == call)
        small = [t for t in ts if t['call'] in small_calls]
        ok(len(small) == len(small_calls), f'{lab}: small tests named for the slow trap exist')
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



# ---------------------------------------------------------------- coding-4
C = 'coding-4'
from fractions import Fraction as _Fr
from itertools import product
from math import comb


# pf-idioms-count-above-mean. Brute: the mean as a Fraction.
def above_brute(xs):
    if len(xs) == 0:
        return 0
    m = _Fr(sum(xs), len(xs))
    return len([x for x in xs if x > m])


code_item(C, 'pf-idioms-count-above-mean', 'above_mean', above_brute, {
    'at or above the mean': 'def above_mean(xs):\n    if not xs:\n        return 0\n    m = sum(xs) / len(xs)\n    return sum(1 for x in xs if x >= m)\n',
    'no guard for the empty list': 'def above_mean(xs):\n    m = sum(xs) / len(xs)\n    return sum(1 for x in xs if x > m)\n'})
ok(sum(1 for x in [4, 4, 4] if x >= 4) == 3 and _Fr(1 + 2 + 3 + 10, 4) == 4, 'slip 3 for [4, 4, 4]; mean 4 in the prose')


# ds-arrays-local-peaks. Brute: the window's maximum is the middle value and occurs once.
def peaks_brute(xs):
    out = []
    for i in range(len(xs)):
        if 0 < i < len(xs) - 1:
            w = xs[i - 1:i + 2]
            if max(w) == xs[i] and w.count(xs[i]) == 1:
                out.append(i)
    return out


code_item(C, 'ds-arrays-local-peaks', 'local_peaks', peaks_brute, {
    'at least both neighbours': 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if xs[i - 1] <= xs[i] >= xs[i + 1]]\n',
    'ends included': 'def local_peaks(xs):\n    n = len(xs)\n    return [i for i in range(n) if (i == 0 or xs[i - 1] < xs[i]) and (i == n - 1 or xs[i] > xs[i + 1])]\n'})
ns = {}
exec('def lp(xs):\n    return [i for i in range(1, len(xs) - 1) if xs[i - 1] <= xs[i] >= xs[i + 1]]\n', ns)
ok(ns['lp']([1, 3, 2, 4, 4, 1, 5]) == [1, 3, 4], 'brief trap value [1, 3, 4]')
two(len(range(1, 99999, 2)), 49999, 0, 'peaks in [0, 1] * 50000: odd indices 1 to 99,997')


# ds-pointers-median-of-three. Brute: sort each window and take the middle.
def med_brute(xs):
    return [sorted(xs[i:i + 3])[1] for i in range(len(xs) - 2)]


code_item(C, 'ds-pointers-median-of-three', 'median3', med_brute, {
    'middle element of each window': 'def median3(xs):\n    return [xs[i + 1] for i in range(len(xs) - 2)]\n',
    'one window short': 'def median3(xs):\n    return [sorted(xs[i:i + 3])[1] for i in range(len(xs) - 3)]\n'})
ok([[5, 1, 4, 2, 8][i + 1] for i in range(3)] == [1, 4, 2], 'brief trap value [1, 4, 2]')
two(sum(range(1, 99999)), 99998 * 99999 // 2, 0, 'sum of medians of 0..99,999: 4,999,850,001')


# simulation-rules-settle-day. Brute: list every business day ahead and index it.
def settle_brute(trade_day, lag, holidays):
    if lag == 0:
        return trade_day
    span = range(trade_day + 1, trade_day + 2 * lag + len(holidays) + 10)
    biz = [d for d in span if d % 7 not in (5, 6) and d not in holidays]
    return biz[lag - 1]


code_item(C, 'simulation-rules-settle-day', 'settle_day', settle_brute, {
    'add the lag, then skip forward': 'def settle_day(trade_day, lag, holidays):\n    d = trade_day + lag\n    while d % 7 >= 5 or d in holidays:\n        d += 1\n    return d\n',
    'skip weekends, then add the number of holidays': 'def settle_day(trade_day, lag, holidays):\n    d, left = trade_day, lag\n    while left:\n        d += 1\n        if d % 7 < 5:\n            left -= 1\n    extra = sum(1 for h in holidays if trade_day < h <= d)\n    while extra:\n        d += 1\n        if d % 7 < 5 and d not in holidays:\n            extra -= 1\n    return d\n'})
ns = {}
exec('def cal(t, l, h):\n    d = t + l\n    while d % 7 >= 5 or d in h:\n        d += 1\n    return d\n', ns)
ok(ns['cal'](3, 2, set()) == 7 and ns['cal'](4, 2, {7}) == 8, 'add-then-skip gives 7 on the first test (right) and 8 on the second')
ok(3 % 7 == 3 and 7 % 7 == 0 and 5 % 7 == 5 and 6 % 7 == 6, 'day 3 is Thursday, 7 a Monday, 5 and 6 the weekend')
two(settle_brute(0, 260, set()), 52 * 7, 0, '260 business days from a Monday: 52 weeks')


# at-search-smallest-n (rows_needed). Brute: integer square root, then adjust.
def rows_brute(target):
    if target <= 0:
        return 0
    n = (math.isqrt(8 * target + 1) - 1) // 2
    while n * (n + 1) // 2 < target:
        n += 1
    while n > 0 and (n - 1) * n // 2 >= target:
        n -= 1
    return n


FLOAT = 'import math\ndef rows_needed(target):\n    if target <= 0:\n        return 0\n    return math.ceil((math.sqrt(8 * target + 1) - 1) / 2)\n'
COUNT = 'def rows_needed(target):\n    n = 0\n    while n * (n + 1) // 2 < target:\n        n += 1\n    return n\n'
SMALL_N = ['rows_needed(0)', 'rows_needed(1)', 'rows_needed(7)', 'rows_needed(10)', 'rows_needed(11)', 'rows_needed(3)', 'rows_needed(-5)']
code_item(C, 'at-search-smallest-n', 'rows_needed', rows_brute, {'float square root': FLOAT},
          slow_traps=[('count up one row at a time', COUNT, 'rows_needed(10**18)', SMALL_N)])
ns = {}
exec(FLOAT, ns)
ok(ns['rows_needed'](10 ** 18) == 1414213562, 'float formula is right at 10^18 itself')
ok(ns['rows_needed'](999999998765257142) == 1414213561, 'float formula is one row short at 999,999,998,765,257,142')
n0 = 1414213561
two(n0 * (n0 + 1) // 2 + 1, 999999998765257142, 0, 'that target is T(1,414,213,561) + 1')
ok(999999998765257142 <= 10 ** 18, 'the float test is inside the stated range')
k = 1414213562
ok(k * (k + 1) // 2 >= 10 ** 18 > (k - 1) * k // 2, '1,414,213,562 is the smallest n for 10^18')
ok(2 * 10 ** 9 * (2 * 10 ** 9 + 1) // 2 >= 10 ** 18 and math.ceil(math.log2(2 * 10 ** 9)) == 31, 'upper bound 2 x 10^9 covers 10^18; about 31 halvings')


# gd-dp-dice-total-ways. Brute: inclusion-exclusion (closed form), and every face tuple for n up to 4.
def dice_brute(n, total):
    if total < 0:
        return 0
    if n == 0:
        return 1 if total == 0 else 0
    if n <= 4:
        return sum(1 for f in product(range(1, 7), repeat=n) if sum(f) == total)
    s = 0
    for j in range(n + 1):
        top = total - 6 * j - 1
        if top < n - 1:
            break
        s += (-1) ** j * comb(n, j) * comb(top, n - 1)
    return s if n <= total <= 6 * n else 0


PLAIN = 'def dice_ways(n, total):\n    if n == 0:\n        return 1 if total == 0 else 0\n    return sum(dice_ways(n - 1, total - f) for f in range(1, 7) if total - f >= 0)\n'
code_item(C, 'gd-dp-dice-total-ways', 'dice_ways', dice_brute, {},
          slow_traps=[('plain recursion without a table', PLAIN, 'dice_ways(40, 140)',
                       ['dice_ways(2, 7)', 'dice_ways(3, 10)', 'dice_ways(0, 0)', 'dice_ways(2, 13)', 'dice_ways(0, 3)', 'dice_ways(1, 6)', 'dice_ways(3, -1)'])])
ok(dice_brute(3, 10) == sum(1 for f in product(range(1, 7), repeat=3) if sum(f) == 10) == 27, '27 for three dice to 10')

# pf-classes-shared-class-list: run the lines; slips by carrying them out
it = item(C, 'pf-classes-shared-class-list')
body, out = run_prose(it)


class Own:
    def __init__(self):
        self.levels = []

    def add(self, x):
        self.levels.append(x)


class Copied:
    levels = []

    def add(self, x):
        list(self.levels).append(x)


p_, q_ = Own(), Own()
p_.add(1); q_.add(2)
c1, c2 = Copied(), Copied()
c1.add(1); c2.add(2)
numeric(C, 'pf-classes-shared-class-list', int(out), None, {'own-list': len(p_.levels), 'copied-list': len(c1.levels)})
two(int(out), len([1, 2]), 0, 'shared list holds 1 and 2')

# ds-trees-heap-trace
import heapq
it = item(C, 'ds-trees-heap-trace')
body, out = run_prose(it)
h = [5, 1, 8, 3, 2]
srt = sorted(h)
a_, rest = srt[0], srt[1:]                               # by hand: smallest out, then push 4 and take the smallest
b_ = min(rest + [4])
rest2 = sorted(rest + [4])[1:]
two(int(out), a_ + b_ + rest2[0], 0, 'heap trace 1 + 2 + 3')
h2 = [5, 1, 8, 3, 2]
heapq.heapify(h2)
heapq.heappop(h2)
numeric(C, 'ds-trees-heap-trace', int(out), None, {'pushed-value': a_ + 4 + h2[0], 'old-top': a_ + b_ + b_})
ok(sorted(h2) == [2, 3, 5, 8], 'after the pop: 2, 3, 5, 8')

# bit-lowest-and-count
it = item(C, 'bit-lowest-and-count')
body, out = run_prose(it)
x_ = 44
low = 1 << ((x_ & -x_).bit_length() - 1)
two(int(out), low + format(x_, 'b').count('1'), 0, 'bit trick 4 + 3')
ok(format(44, 'b') == '101100' and 44 == 32 + 8 + 4, '44 is 101100')
numeric(C, 'bit-lowest-and-count', int(out), None,
        {'bit-index': (x_ & -x_).bit_length() - 1 + 3, 'highest-bit': (1 << (x_.bit_length() - 1)) + 3})

# edge-case-list-median-test: run median on each option
it = choice(C, 'edge-case-list-median-test', '[4, 1, 3, 2]')
m = re.search(r'```python\n(.*?)```', it['prose'], re.S)
ns = {}
exec(m.group(1), ns)
import statistics as _st
ok(ns['median']([4, 1, 3, 2]) == 3 and _st.median([4, 1, 3, 2]) == 2.5, 'returns 3, median 2.5')
try:
    ns['median']([])
    ok(False, '[] should raise')
except IndexError:
    ok(True, '[] raises IndexError')
ok(ns['median']([5]) == 5 and ns['median']([3, 1, 2]) == 2 == _st.median([3, 1, 2]), '[5] and [3, 1, 2] are right')
ok({o['text'] for o in it['widget']['options']} == {'`[4, 1, 3, 2]`', '`[]`', '`[5]`', '`[3, 1, 2]`'}, 'median option texts')

# gd-traversal-depth-first-order: run it; slips as named
it = choice(C, 'gd-traversal-depth-first-order', 'A, B, D, F, C, E')
m = re.search(r'```python\n(.*?)```', it['prose'], re.S)
ok(len(m.group(1).strip('\n').split('\n')) <= 8, 'dfs: at most eight lines')
ns = {}
exec(m.group(1), ns)
ok(', '.join(ns['seen']) == 'A, B, D, F, C, E', f'dfs order {ns["seen"]}')
g_ = ns['g']
order, qq = [], ['A']                                    # breadth first
while qq:
    v = qq.pop(0)
    if v in order:
        continue
    order.append(v)
    qq += [w for w in g_[v] if w not in order]
ok(', '.join(order) == 'A, B, C, D, E, F', 'slip: breadth first')
st, rev = ['A'], []                                      # stack of pushes, neighbours in list order
while st:
    v = st.pop()
    if v in rev:
        continue
    rev.append(v)
    st += [w for w in g_[v] if w not in rev]
ok(', '.join(rev) == 'A, C, E, F, D, B', 'slip: stack pushes give reversed neighbours')
texts = {o['text'] for o in it['widget']['options']}
ok(texts == {'A, B, D, F, C, E', 'A, B, C, D, E, F', 'A, B, D, C, E, F', 'A, C, E, F, D, B'}, 'dfs option texts')

# defined-vs-undefined-wraparound: constant evaluation with g++
it = choice(C, 'defined-vs-undefined-wraparound', '4,294,967,295')
good = cpp_compiles('#include <climits>\nstatic_assert(sizeof(int) == 4 && sizeof(unsigned) == 4);\n'
                    'constexpr unsigned u = 0;\nconstexpr auto x = u - 1;\nstatic_assert(x == 4294967295u);\nint main() {}\n')
bad = cpp_compiles('#include <climits>\nconstexpr int i = INT_MAX;\nconstexpr auto y = i + 1;\nint main() {}\n')
if good is not None:
    ok(good, 'unsigned 0 - 1 is 4,294,967,295 in a constant expression')
    ok(bad is False, 'INT_MAX + 1 is rejected in a constant expression (undefined)')
two(2 ** 32 - 1, 4294967295, 0, '2^32 - 1')


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
ok(counts == {'statistics-4': 15, 'finance-4': 15, 'behavioural-8': 8, 'coding-4': 12}, f'item counts {counts}')

print(f'{checks[0]} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
