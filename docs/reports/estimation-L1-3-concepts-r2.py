#!/usr/bin/env python3
"""Concept audit, round 2: estimation levels 1 to 3.

Independent recomputation of every stated number the audit ledger leans on, and a Monte
Carlo check of every empirical claim. Exits 0 when the content is right; a check that
fails because the content is wrong stays failing.

Run: python docs/reports/estimation-L1-3-concepts-r2.py [--quick]
  --quick cuts the bootstrap seed sweeps (used while drafting); the committed figures in
  the audit come from the full run.
The round 2 fix pass added seven checks at the end ("fix r2"); no earlier check was re-pointed.
"""
import json, math, os, random, statistics, sys, itertools
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'estimation')
QUICK = '--quick' in sys.argv
rng = np.random.default_rng(20261126)
fails = []
n_checks = 0


def load(name):
    return json.load(open(os.path.join(C, name + '.json')))


def check(label, ok, detail=''):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(label)
    print(('ok   ' if ok else 'FAIL ') + label + (('  [' + detail + ']') if detail else ''))


def close(a, b, tol):
    return abs(a - b) <= tol


def num(s):
    return float(str(s).replace('−', '-'))


# ---------------------------------------------------------------- level 1
l1 = load('l1-sample-population')
cells = [[num(c) for c in row] for row in l1['screens'][0]['canvas']['params']['cells']]
pop = np.array([c for row in cells for c in row])
check('L1 population mean 0.10', close(pop.mean(), 0.10, 5e-4), f'{pop.mean():.4f}')
check('L1 population sd 1.00 (divide by N)', close(pop.std(), 1.00, 5e-3), f'{pop.std():.4f}')
check('L1 share of up days 0.47', close((pop > 0).mean(), 0.47, 1e-9), f'{(pop > 0).mean():.2f}')


def cell(ref):
    r, c = ref[1:].split('c')
    return cells[int(r) - 1][int(c) - 1]


shade = l1['screens'][3]['canvas']['state']['shade']
A = np.array([cell(x) for x in shade['sample A']])
B = np.array([cell(x) for x in shade['sample B']])
check('L1 sample A mean 0.42', close(A.mean(), 0.42, 1e-9), f'{A.mean():.3f}')
check('L1 sample A s = 1.21 (n - 1)', close(A.std(ddof=1), 1.21, 5e-3), f'{A.std(ddof=1):.4f}')
check('L1 sample A share up 0.7', close((A > 0).mean(), 0.7, 1e-9))
check('L1 sample B mean -0.15', close(B.mean(), -0.15, 1e-9), f'{B.mean():.3f}')
check('L1 one day in both samples', len(set(shade['sample A']) & set(shade['sample B'])) == 1)
check('L1 sample A: three losers -0.3, -1.0, -1.9; winners add to 7.4',
      sorted(A[A < 0].tolist()) == [-1.9, -1.0, -0.3] and close(A[A > 0].sum(), 7.4, 1e-9))

# ---------------------------------------------------------------- level 2
l2 = load('l2-estimates-vary')
data2 = np.array(l2['screens'][0]['canvas']['params']['data'])
check('L2 population is the L1 grid', np.allclose(np.sort(data2), np.sort(pop)))
# exact law of the mean of 10 draws with replacement: convolve on the 0.1 grid
k = np.round(pop * 10).astype(int)
off = k.min()
pmf1 = np.bincount(k - off) / len(k)
pmf = np.array([1.0])
for _ in range(10):
    pmf = np.convolve(pmf, pmf1)
sums = (np.arange(len(pmf)) + 10 * off) / 100.0  # the mean, in %
ex = l2['screens'][1]['canvas']['params']['exact']
bad = []
for e in ex:
    lo, hi = e['x'] - 0.1, e['x'] + 0.1
    p = pmf[(sums >= lo - 1e-9) & (sums < hi - 1e-9)].sum()
    if not close(p, e['y'], 6e-4):
        bad.append((e['x'], round(p, 4), e['y']))
check('L2 dashed "exact" shares of the mean of 10 (bins [x-0.1, x+0.1))', not bad, str(bad))
m10 = (pmf * sums).sum()
sd10 = math.sqrt((pmf * (sums - m10) ** 2).sum())
check('L2 E[mean] = mu and SE = sigma/sqrt(10) = 0.316', close(m10, 0.10, 5e-4) and close(sd10, 0.316, 2e-3),
      f'{m10:.4f}, {sd10:.4f}')
p1 = pmf[(sums >= -0.2 - 1e-9) & (sums < 0.4 - 1e-9)].sum()
check('L2 66% of samples between -0.2 and 0.4', close(p1, 0.66, 0.012), f'{p1:.4f}')
p2 = pmf[np.abs(sums - 0.10) <= 0.63 + 1e-9].sum()
check('L2 "exactly 95.6%" within 0.10 +/- 0.63', close(p2, 0.956, 1.5e-3), f'{p2:.4f}')
tr = np.array(list(l2['screens'][9]['canvas']['state']['values'].values()))
check('L2 20 trades: mean 0.4, sd 2.5', close(tr.mean(), 0.4, 0.05) and close(tr.std(ddof=1), 2.5, 0.06),
      f'{tr.mean():.3f}, {tr.std(ddof=1):.3f} (n: {tr.std():.3f})')
check('L2 SE figures', close(2.5 / math.sqrt(20), 0.559, 5e-4) and (2.5 / 0.1) ** 2 == 625 and close(20 * 0.559 / 0.1, 112, 1))
# Monte Carlo: SE = sigma / sqrt(n) and the 1/sqrt(n) law, on the page's own population
draws = rng.choice(pop, size=(200000, 25))
check('L2 MC: sd of the mean of 25 = 0.20, of 100 = 0.10',
      close(draws.mean(1).std(), 0.2, 0.003) and close(rng.choice(pop, size=(100000, 100)).mean(1).std(), 0.1, 0.002))

# the page's own seeded run (engine: mulberry32, js/engine/sim.js; pick(arr) = arr[floor(u * len)]), replayed here
def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    M = 0xFFFFFFFF
    while True:
        a = (a + 0x6D2B79F5) & M
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & M
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & M)) & M
        yield ((t ^ (t >> 14)) & M) / 4294967296


g_ = mulberry32(l2['screens'][1]['canvas']['params']['sim']['seed'])
pl = [float(v) for v in data2]
runs = np.array([sum(pl[int(next(g_) * 100)] for _ in range(10)) / 10 for _ in range(1000)])
check('L2 the page run (seed 1610, 1,000 trials): mean of averages 0.095, sd 0.312, 96.2% within 0.10 +/- 0.63',
      close(runs.mean(), 0.095, 6e-4) and (close(runs.std(), 0.312, 6e-4) or close(runs.std(ddof=1), 0.312, 6e-4))
      and close((np.abs(runs - 0.10) <= 0.63 + 1e-9).mean(), 0.962, 6e-4),
      f'{runs.mean():.4f}, {runs.std():.4f}, {(np.abs(runs - 0.10) <= 0.63 + 1e-9).mean():.3f}')

# ---------------------------------------------------------------- level 3
l3 = load('l3-right-target')
a = l3['screens'][0]['canvas']['params']['params']['a']
check('L3 running average ends at 0.807 after 1,000 samples', len(a) == 1000 and close(a[-1], 0.807, 5e-4), f'{a[-1]}')
x = rng.standard_normal((400000, 5))
vn = x.var(axis=1)
check('L3 MC: E[divide-by-n variance], n = 5, is 0.8 (not 1)', close(vn.mean(), 0.8, 0.004), f'{vn.mean():.4f}')
x = rng.exponential(1.0, (400000, 5))
check('L3 MC: same for a skewed law (unit exponential, variance 1)', close(x.var(axis=1).mean(), 0.8, 0.008))
samples = list(itertools.product([-1, 0, 1], repeat=2))
v_n = [np.var(s) for s in samples]
s2 = [np.var(s, ddof=1) for s in samples]
check('L3 nine samples: mean of V_n = 1/3, of s^2 = 2/3, of s = 0.63; sigma = 0.82',
      close(np.mean(v_n), 1 / 3, 1e-12) and close(np.mean(s2), 2 / 3, 1e-12) and close(np.mean(np.sqrt(s2)), 0.63, 5e-3)
      and close(math.sqrt(2 / 3), 0.82, 5e-3))
five = np.array([0.4, 1.2, -0.3, 0.9, 0.3])
check('L3 sum of squares 1.34 about the mean, 2.14 about mu = 0.1',
      close(((five - five.mean()) ** 2).sum(), 1.34, 1e-9) and close(((five - 0.1) ** 2).sum(), 2.14, 1e-9))
check('L3 sqrt(20/19) = 1.026, sqrt(250/249) - 1 = 0.2%, other-way 2.53%',
      close(math.sqrt(20 / 19), 1.026, 5e-4) and close(math.sqrt(250 / 249) - 1, 0.002, 1e-4) and close(1 - math.sqrt(19 / 20), 0.0253, 1e-4))
for t in l3['screens'][10]['widget']['tests']:
    arg = eval(t['call'][len('round(vol('):-len('), 6)')])
    check('L3 code test ' + t['call'][:34], close(round(float(np.std(arg, ddof=1)), 6), float(t['expect']), 1e-9))

# ---------------------------------------------------------------- level 4
l4 = load('l4-bias-against-variance')
pts = {p['id']: p['y'] for p in l4['screens'][0]['canvas']['state']['points']}
ea = np.array([pts[f'a{i}'] for i in range(1, 9)]) - 0.2
eb = np.array([pts[f'b{i}'] for i in range(1, 9)]) - 0.2
check('L4 B is half of A on every sample', all(close(pts[f'b{i}'], pts[f'a{i}'] / 2, 1e-9) for i in range(1, 9)))
check('L4 B closer on six of eight; squared misses 0.018 and 0.041',
      (np.abs(eb) < np.abs(ea)).sum() == 6 and close((eb ** 2).mean(), 0.018, 6e-4) and close((ea ** 2).mean(), 0.041, 6e-4),
      f'{(np.abs(eb) < np.abs(ea)).sum()}, {(eb ** 2).mean():.4f}, {(ea ** 2).mean():.4f}')
xb = 0.2 + 0.2 * rng.standard_normal(2000000)
check('L4 MC: MSE of 0.5*mean is 0.02, of the mean 0.04 (mu = 0.2, var 0.04)',
      close(((0.5 * xb - 0.2) ** 2).mean(), 0.02, 3e-4) and close(((xb - 0.2) ** 2).mean(), 0.04, 3e-4))
x = rng.standard_normal((1000000, 5))
ss = ((x - x.mean(1, keepdims=True)) ** 2).sum(1)
mse = {c: ((ss / c - 1) ** 2).mean() for c in (4, 5, 6, 7)}
check('L4 MC: SS has mean 4, variance 8; MSE 0.5, 0.36, 0.333 for c = 4, 5, 6; c = 6 beats c = 7',
      close(ss.mean(), 4, 0.02) and close(ss.var(), 8, 0.08) and close(mse[4], 0.5, 0.006) and close(mse[5], 0.36, 0.004)
      and close(mse[6], 1 / 3, 0.004) and mse[6] < mse[7] and mse[6] < mse[5],
      str({c: round(v, 4) for c, v in mse.items()}))
for n in (3, 5, 10, 20, 50):
    cs = np.arange(1, 200)
    m = (2 * (n - 1) + (n - 1 - cs) ** 2) / cs ** 2
    if cs[m.argmin()] != n + 1:
        check(f'L4 MSE(c) minimised at n + 1 for n = {n}', False)
        break
else:
    check('L4 MSE(c) = [2(n-1) + (n-1-c)^2]/c^2 is smallest at c = n + 1 (n = 3..50)', True)
check('L4 Blume 1.402, 0.598; swapped 1.198', close(0.67 * 1.6 + 0.33, 1.402, 1e-9) and close(0.67 * 0.4 + 0.33, 0.598, 1e-9)
      and close(0.33 * 1.6 + 0.67, 1.198, 1e-9))

# ---------------------------------------------------------------- level 5
l5 = load('l5-which-fits')
rows = l5['screens'][9]['canvas']['params']['rows']
r = np.array([num(q[1]) for q in rows])
okd = all(close(stats.norm.pdf(x_, 0, 1), num(q[2]), 6e-5) and close(stats.norm.pdf(x_, 0, 2), num(q[3]), 6e-5) for x_, q in zip(r, rows))
lr = np.prod(stats.norm.pdf(r, 0, 1)) / np.prod(stats.norm.pdf(r, 0, 2))
check('L5 week table densities and likelihood ratio 5.554 = 32 exp(-0.375 * 4.67)',
      okd and close(lr, 5.554, 2e-3) and close((r ** 2).sum(), 4.67, 1e-9) and close(32 * math.exp(-0.375 * 4.67), lr, 1e-9), f'{lr:.4f}')
check('L5 L(2/3) = 4/27, ratio 32/27, L(.45) = .111 > L(.85) = .108, area 1/12',
      close(4 / 27, 0.1481, 1e-4) and close((4 / 27) / (1 / 8), 1.185, 1e-3) and 0.45 ** 2 * 0.55 > 0.85 ** 2 * 0.15
      and close(math.gamma(3) * math.gamma(2) / math.gamma(5), 1 / 12, 1e-12))
check('L5 12 of 20: L(.5)/L(.6) = 0.67; peak 1.427 millionths',
      close(0.5 ** 20 / (0.6 ** 12 * 0.4 ** 8), 0.67, 5e-3) and close(1e6 * 0.6 ** 12 * 0.4 ** 8, 1.427, 1e-3))
check('L5 quiz ratios 27/16, (11/9)^2', close(0.75 ** 3 * 0.25 / 0.5 ** 4, 27 / 16, 1e-12) and close((0.55 / 0.45) ** 6 * (0.45 / 0.55) ** 4, (11 / 9) ** 2, 1e-12))

# ---------------------------------------------------------------- level 6
obs = np.array([1.2, 2.0, 3.7])
grid = np.round(np.arange(0, 5.01, 0.1), 1)
L = np.array([np.prod(stats.norm.pdf(obs, m_, 1)) for m_ in grid])
check('L6 product of three heights peaks at 2.3, value 0.0124', grid[L.argmax()] == 2.3 and close(L.max(), 0.0124, 5e-5))
check('L6 Poisson check values L(5)/L(4) = 0.52, L(3)/L(4) = 0.40',
      close(math.exp(-6) * 1.25 ** 24, 0.52, 6e-3) and close(math.exp(6) * 0.75 ** 24, 0.40, 6e-3))
check('L6 L(0.1) = 0.35 for ten tails; fair coin 0.001; 1000 L(0.5) = 0.9766 for 7 of 10',
      close(0.9 ** 10, 0.35, 5e-3) and close(0.5 ** 10, 0.001, 5e-5) and close(1000 * 0.5 ** 10, 0.9766, 5e-5))
# MC: the MLE k/n is where the binomial likelihood peaks, on random data
ok = True
for _ in range(200):
    n_ = int(rng.integers(2, 40)); k_ = int(rng.integers(0, n_ + 1))
    g = np.linspace(0, 1, 2001)
    ll = k_ * np.log(np.where(g > 0, g, 1e-300)) + (n_ - k_) * np.log(np.where(g < 1, 1 - g, 1e-300))
    ok &= abs(g[ll.argmax()] - k_ / n_) < 6e-4
check('L6 numeric: argmax of p^k (1-p)^(n-k) is k/n, boundaries included (200 random cases)', ok)

# ---------------------------------------------------------------- level 7
check('L7 l(2/3) = -1.9095; slips -0.1806, -0.8293', close(2 * math.log(2 / 3) + math.log(1 / 3), -1.9095, 1e-4)
      and close(math.log(2 / 3) ** 2 * math.log(1 / 3), -0.1806, 1e-4) and close(math.log10(4 / 27), -0.8293, 1e-4))
check('L7 peak values: -6.109 (n = 10), -61.1 and 3e-27 (n = 100)',
      close(7 * math.log(.7) + 3 * math.log(.3), -6.109, 1e-3) and close(100 * (.7 * math.log(.7) + .3 * math.log(.3)), -61.1, 0.05)
      and close(math.exp(100 * (.7 * math.log(.7) + .3 * math.log(.3))) / 1e-27, 3, 0.1))
check('L7 floats: 0.5**1000 = 9.33e-302, 0.5**2000 = 0.0, 2000 ln 0.5 = -1386.29',
      repr(0.5 ** 1000) == '9.332636185032189e-302' and 0.5 ** 2000 == 0.0 and repr(2000 * math.log(0.5)) == '-1386.2943611198905')
hr = np.array([num(q[1]) for q in load('l7-taking-logs')['screens'][9]['canvas']['params']['rows'][:6]])


def nll(rr, s):
    return -len(rr) / 2 * math.log(2 * math.pi * s * s) - (rr ** 2).sum() / (2 * s * s)


check('L7 two volatility models: sum r^2 = 1.19, l_A = -3.735, l_B = -5.104, difference 1.370',
      close((hr ** 2).sum(), 1.19, 1e-9) and close(nll(hr, .4), -3.735, 1e-3) and close(nll(hr, .8), -5.104, 1e-3)
      and close(nll(hr, .4) - nll(hr, .8), 1.3698, 1e-4) and close(stats.norm.logpdf(hr, 0, .4).sum(), nll(hr, .4), 1e-9))
check('L7 log scores: B -2.619, A -2.449', close(3 * math.log(.9) + math.log(.1), -2.6187, 1e-4) and close(3 * math.log(.6) + math.log(.4), -2.4488, 1e-4))

# ---------------------------------------------------------------- level 8
l8 = load('l8-volatility-mle')
r20 = np.array([p['x'] for p in l8['screens'][0]['canvas']['state']['points']])
check('L8 20 returns: mean 0.04, SS about the mean 20.3098, sum of squares 20.3418',
      len(r20) == 20 and close(r20.mean(), 0.04, 1e-9) and close(((r20 - r20.mean()) ** 2).sum(), 20.3098, 1e-4)
      and close((r20 ** 2).sum(), 20.3418, 1e-4))
check('L8 sigma-hat 1.0077, zero-mean 1.0085, n - 1 version 1.0339; l(1.01) = -28.533',
      close(r20.std(), 1.0077, 5e-5) and close(math.sqrt((r20 ** 2).mean()), 1.0085, 5e-5) and close(r20.std(ddof=1), 1.0339, 5e-5)
      and close(-10 * math.log(2 * math.pi * 1.01 ** 2) - 20.3098 / (2 * 1.01 ** 2), -28.533, 1e-3))
check('L8 at mu = 1 the best sigma is 1.39', close(math.sqrt(((r20 - 1) ** 2).mean()), 1.39, 5e-3))
five = np.array([0.5, -1.0, 1.5, -0.5, 1.0])


def lv(v):
    return -2.5 * math.log(2 * math.pi * v) - 4.3 / (2 * v)


check('L8 five returns: 0.9274, 0.9747, n-1 1.0368; l(0.86) = -6.718 > l(1.075) = -6.776',
      close(five.std(), 0.9274, 5e-5) and close(math.sqrt((five ** 2).mean()), 0.9747, 5e-5) and close(five.std(ddof=1), 1.0368, 5e-5)
      and close(lv(.86), -6.718, 1e-3) and close(lv(1.075), -6.776, 1e-3))
check('L8 annualising: 15.997%, 365-day slip 19.25%, 254% slip', close(1.0077 * math.sqrt(252), 15.997, 2e-3)
      and close(1.0077 * math.sqrt(365), 19.252, 2e-3) and close(1.0077 * 252, 253.94, 0.01))
# MC: sd of the MLE sigma-hat against sigma / sqrt(2n), normal and fat-tailed
res = {}
for n_ in (5, 20, 250):
    reps = 400000 if n_ < 100 else 60000
    z = rng.standard_normal((reps, n_))
    res[('norm', n_)] = z.std(axis=1).std() * math.sqrt(2 * n_)
    t = rng.standard_t(5, (reps, n_)) / math.sqrt(5 / 3)
    res[('t5', n_)] = t.std(axis=1).std() * math.sqrt(2 * n_)
check('L8/L9 MC: SE(sigma-hat) = sigma/sqrt(2n) for normal data, within 5% (n = 5, 20, 250)',
      all(close(res[('norm', n_)], 1, 0.05) for n_ in (5, 20, 250)), str({k_: round(v, 3) for k_, v in res.items() if k_[0] == 'norm'}))
check('L9 MC: fat tails (t, 5 df, same variance) make SE(sigma-hat) larger, by more than 30% at n = 20 and 250',
      res[('t5', 20)] > 1.3 and res[('t5', 250)] > 1.3, str({k_: round(v, 3) for k_, v in res.items() if k_[0] == 't5'}))
z = rng.standard_normal((500000, 5))
mle = z.var(axis=1); s2_ = z.var(axis=1, ddof=1)
check('L8 MC: MLE variance is biased low ((n-1)/n) but has lower MSE than s^2 (n = 5): (2n-1)/n^2 = 0.36 < 0.5',
      close(mle.mean(), 0.8, 0.005) and close(((mle - 1) ** 2).mean(), 0.36, 0.006) and close(((s2_ - 1) ** 2).mean(), 0.5, 0.008))

# ---------------------------------------------------------------- level 9
check('L9 Ben 95%, Ana 38% within 0.1%', close(2 * stats.norm.cdf(2) - 1, 0.95, 5e-3) and close(2 * stats.norm.cdf(.5) - 1, 0.38, 5e-3))
check('L9 55 of 100: SE 0.0497, normal tail 16%, exact P(X >= 55) = 18%',
      close(math.sqrt(.55 * .45 / 100), 0.0497, 5e-5) and close(stats.norm.sf(1), 0.16, 5e-3) and close(stats.binom.sf(54, 100, .5), 0.18, 5e-3),
      f'{stats.binom.sf(54, 100, .5):.4f}')
check('L9 poll SE 0.0158; vol SE 1.5/30 = 0.05', close(math.sqrt(.52 * .48 / 1000), 0.0158, 5e-5) and close(1.5 / math.sqrt(900), 0.05, 1e-12))

# ---------------------------------------------------------------- level 10
l10 = load('l10-catching-the-truth')
der = l10['screens'][2]['canvas']['derive']
centres = [float(der[f's{i}.from.1'].split(' - ')[0]) for i in range(1, 101)]
miss = lambda z_: sum(abs(c - 0.05) > z_ * 0.1 for c in centres)
check('L10 100 intervals: 5 miss at 1.96, 10 at 1.645, 1 at 2.576, 0 at 3', (miss(1.96), miss(1.645), miss(2.576), miss(3)) == (5, 10, 1, 0),
      str((miss(1.96), miss(1.645), miss(2.576), miss(3))))
check('L10 multipliers: 68%, 90%, 95%, 95.45%, 99%, 0.0027, 0.0001, z = 0.98 gives 67%',
      close(2 * stats.norm.cdf(1) - 1, .68, 5e-3) and close(stats.norm.ppf(.95), 1.645, 5e-4) and close(stats.norm.ppf(.975), 1.96, 5e-4)
      and close(2 * stats.norm.cdf(2) - 1, .9545, 5e-5) and close(stats.norm.ppf(.995), 2.576, 5e-4) and close(2 * stats.norm.sf(3), .0027, 5e-5)
      and close(2 * stats.norm.sf(3.92), 1e-4, 2e-5) and close(2 * stats.norm.cdf(.98) - 1, .67, 5e-3))
check('L10 t, 9 df: +/-1.96 holds 0.918; 97.5% point 2.262; 10 df 2.228; 29 df 2.045',
      close(1 - 2 * stats.t.sf(1.96, 9), 0.918, 1e-3) and close(stats.t.ppf(.975, 9), 2.262, 5e-4) and close(stats.t.ppf(.975, 10), 2.228, 5e-4)
      and close(stats.t.ppf(.975, 29), 2.045, 5e-4))
z = 0.05 + rng.standard_normal((400000, 10))
m_, s_ = z.mean(1), z.std(1, ddof=1)
cov196 = (np.abs(m_ - 0.05) <= 1.96 * s_ / math.sqrt(10)).mean()
covt = (np.abs(m_ - 0.05) <= 2.262 * s_ / math.sqrt(10)).mean()
check('L10 MC: n = 10 normal, s for sigma: 1.96 covers 92%, 2.262 covers 95%', close(cov196, 0.918, 0.003) and close(covt, 0.95, 0.002),
      f'{cov196:.4f}, {covt:.4f}')
z = 0.05 + rng.standard_normal((400000, 100))
covz = (np.abs(z.mean(1) - 0.05) <= 1.96 * 1 / 10).mean()
check('L10 MC: known sigma, n = 100: 1.96 covers 95%, 1.645 covers 90%', close(covz, 0.95, 0.002)
      and close((np.abs(z.mean(1) - 0.05) <= 1.645 / 10).mean(), 0.90, 0.003), f'{covz:.4f}')
t = 0.05 + rng.standard_t(4, (400000, 100)) / math.sqrt(2)
covf = (np.abs(t.mean(1) - 0.05) <= 1.96 / 10).mean()
check('L10 MC: "close to it otherwise": fat-tailed days (t, 4 df, sd 1), n = 100, coverage within 1 point of 95%', close(covf, 0.95, 0.01), f'{covf:.4f}')
check('L10 transfer numbers: 0.0759, +/-0.149, vol SE 0.504, half-width 0.988, hit-rate lower end 0.5012',
      close(1.2 / math.sqrt(250), .0759, 5e-5) and close(1.96 * 1.2 / math.sqrt(250), .149, 5e-4) and close(16 / math.sqrt(1008), .504, 5e-4)
      and close(1.96 * 16 / math.sqrt(1008), .988, 5e-4) and close(.55 - 1.96 * math.sqrt(.55 * .45 / 400), .5012, 5e-5))
false_pos = (rng.random((200000, 40)) < 0.05).sum(1).mean()
check('L10 MC: 40 true-null strategies give 2 intervals excluding zero on average', close(false_pos, 2.0, 0.02), f'{false_pos:.3f}')

# ---------------------------------------------------------------- level 11: bootstrap
l11 = load('l11-bootstrap')
returns = [float(q) for row in l11['screens'][0]['canvas']['params']['rows'] for q in row[1:]]
R = np.array(returns)
check('L11 20 returns: mean 0.15, sample sd 1.0', close(R.mean(), 0.15, 1e-9) and close(R.std(ddof=1), 1.0, 0.03), f'{R.std(ddof=1):.4f}')
check('L11 long-run sd of the resampled mean 0.217', close(R.std() / math.sqrt(20), 0.217, 6e-4), f'{R.std() / math.sqrt(20):.4f}')
check('L11 formula interval 0.15 +/- 0.44', close(1.96 * R.std(ddof=1) / math.sqrt(20), 0.44, 0.012))
w4 = l11['screens'][4]['widget']
ns = {}
exec(w4['solution'], ns)
sol_ci = ns['bootstrap_ci']
ci1000 = sol_ci(returns, 1000, 1)
check('L11 solution, B = 1000, seed 1: -0.29 to 0.555', [round(v, 3) for v in ci1000] == [-0.29, 0.555], str(ci1000))
random.seed(1)
means = sorted(sum(random.choices(returns, k=20)) / 20 for _ in range(1000))
tab = l11['screens'][3]['canvas']['params']['rows']
okt = all(close(means[int(q[0]) - 1], num(q[1]), 5e-4) for q in tab if q[0].isdigit())
check('L11 rank table (ranks 24-27, 974-977) matches the seed-1 run', okt, str([round(means[i], 3) for i in (23, 24, 25, 26, 973, 974, 975, 976)]))
ci4000 = sol_ci(returns, 4000, 1)
check('L11 B = 4000, seed 1: -0.305 to 0.55', [round(v, 3) for v in ci4000] == [-0.305, 0.55], str(ci4000))
want = {(200, 1): (-0.235, 0.49), (200, 2): (-0.23, 0.55), (10000, 1): (-0.30, 0.56), (10000, 2): (-0.305, 0.555)}
got = {k_: tuple(round(v, 3) for v in sol_ci(returns, *k_)) for k_ in want}
check('L11 table of four runs (B = 200, 10,000; seeds 1, 2)', got == want, str(got))
check('L11 35 distinct resamples of 4; 63% of resamples of 250 contain a given day; 64% of 20',
      math.comb(7, 4) == 35 and close(1 - (249 / 250) ** 250, 0.63, 5e-3) and close(1 - (19 / 20) ** 20, 0.64, 5e-3))
sh = sorted(l11['screens'][10]['canvas']['params']['data'])
check('L11 Sharpe histogram: ranks 26 and 975 are -1.10 and 2.90', len(sh) == 1000 and close(sh[25], -1.10, 5e-3) and close(sh[974], 2.90, 5e-3),
      f'{sh[25]}, {sh[974]}')
ser = np.array(l11['screens'][11]['canvas']['params']['series'][0]['values'])
ac = np.corrcoef(ser[:-1], ser[1:])[0, 1]
check('L11 60-day series: lag-1 correlation about 0.6', close(ac, 0.6, 0.12), f'{ac:.3f}')
# exact long-run ends of the mean's bootstrap interval (law of the sum of 20 draws on the 0.1 grid)
kk = np.round(R * 10).astype(int); o = kk.min()
p1_ = np.bincount(kk - o) / 20
pm = np.array([1.0])
for _ in range(20):
    pm = np.convolve(pm, p1_)
vals = (np.arange(len(pm)) + 20 * o) / 200.0
cdf = np.cumsum(pm)
q_lo, q_hi = vals[np.searchsorted(cdf, 0.025)], vals[np.searchsorted(cdf, 0.975)]
check('L11 long-run ends of the 95% interval for the mean: -0.30 and 0.55 (the tests\' centres)', close(q_lo, -0.30, 0.0051) and close(q_hi, 0.55, 0.0051),
      f'{q_lo:.3f}, {q_hi:.3f}')
# MC: iid bootstrap on autocorrelated data understates the SE of the mean; a block bootstrap does better
phi, nn, reps = 0.6, 250, 400
true_sd = []
iid_sd, blk_sd = [], []
for _ in range(reps):
    e = rng.standard_normal(nn + 50)
    y = np.zeros(nn + 50)
    for i in range(1, nn + 50):
        y[i] = phi * y[i - 1] + e[i]
    y = y[50:]
    true_sd.append(y.mean())
    idx = rng.integers(0, nn, (200, nn))
    iid_sd.append(y[idx].mean(1).std())
    starts = rng.integers(0, nn - 25 + 1, (200, 10))
    bi = (starts[:, :, None] + np.arange(25)[None, None, :]).reshape(200, -1)
    blk_sd.append(y[bi].mean(1).std())
true_se = np.std(true_sd)
check('L11 MC: AR(1) 0.6, n = 250: single-day bootstrap SE is under 60% of the true SE; 25-day blocks recover over 75%',
      np.mean(iid_sd) < 0.6 * true_se and np.mean(blk_sd) > 0.75 * true_se,
      f'true {true_se:.3f}, iid {np.mean(iid_sd):.3f}, block {np.mean(blk_sd):.3f}')
# MC: the bootstrap percentile interval for a mean of 250 iid days covers about 95%; of 4 days far less
def boot_cover(n_, reps_, law):
    hit = 0
    for _ in range(reps_):
        y = law(n_)
        bm = y[rng.integers(0, n_, (400, n_))].mean(1)
        lo, hi = np.quantile(bm, [0.025, 0.975])
        hit += lo <= 0 <= hi
    return hit / reps_
c250 = boot_cover(250, 1500, lambda m__: rng.standard_t(5, m__))
c4 = boot_cover(4, 4000, lambda m__: rng.standard_normal(m__))
check('L11 MC: percentile interval for a mean covers about 95% at n = 250 (iid, fat-tailed) and well under 90% at n = 4',
      close(c250, 0.95, 0.02) and c4 < 0.88, f'n = 250: {c250:.3f}; n = 4: {c4:.3f}')
ymax = rng.standard_normal((2000, 250))
bmax = np.array([(y[rng.integers(0, 250, (200, 250))].max(1) == y.max()).mean() for y in ymax[:300]])
check('L11 MC: resampled maximum never exceeds the sample maximum and equals it in about 63% of resamples', close(bmax.mean(), 0.632, 0.02), f'{bmax.mean():.3f}')

# ---- bootstrap hidden tests: share of correct programs that fail (lesson 11 and homework 3)
hw3 = load('homework-3')
wb = hw3['items'][4]['widget']
pre = {}
exec(wb['prelude'], pre)
daily, sharpe = pre['daily'], pre['sharpe']
D = np.array(daily)


def codings():
    def c_choices(data, n, g):
        return g.choices(data, k=n)

    def c_choice(data, n, g):
        return [g.choice(data) for _ in range(n)]

    def c_randrange_rev(data, n, g):  # a third stream: indices drawn in pairs from getrandbits
        return [data[g.randint(0, n - 1)] for _ in range(n)][::-1] if n % 2 else [data[int(g.uniform(0, n)) % n] for _ in range(n)]

    return {'random.choices': c_choices, 'random.choice loop': c_choice, 'randint / uniform index': c_randrange_rev}


def ci_generic(draw, data, stat, B, seed):
    g = random.Random(seed)
    n = len(data)
    v = sorted(stat(draw(data, n, g)) for _ in range(B))
    k_ = int(0.025 * B)
    return v[k_], v[B - 1 - k_]


mean_ = lambda xs: sum(xs) / len(xs)
SEEDS = 40 if QUICK else 400
l11_tests = {
    'L11 t2 width > 0.5 (B 500)': lambda d, s: (lambda ci: ci[1] - ci[0] > 0.5)(ci_generic(d, returns, mean_, 500, s)),
    'L11 t3+t4 ends within 0.05 of -0.30, 0.55 (B 4000)': lambda d, s: (lambda ci: abs(ci[0] + 0.30) < 0.05 and abs(ci[1] - 0.55) < 0.05)(ci_generic(d, returns, mean_, 4000, s)),
    'L11 t6 [0,0,0,0,10] gives exactly (0, 6) (B 2000)': lambda d, s: (lambda ci: math.isclose(ci[0], 0.0, abs_tol=1e-9) and math.isclose(ci[1], 6.0))(ci_generic(d, [0, 0, 0, 0, 10], mean_, 2000, s)),
    'L11 t7 eight values within 0.06 of -0.39, 0.92 (B 3000)': lambda d, s: (lambda ci: abs(ci[0] + 0.39) < 0.06 and abs(ci[1] - 0.92) < 0.06)(ci_generic(d, [2.0, -1.0, 0.5, 0.1, -0.4, 1.2, 0.3, -0.8], mean_, 3000, s)),
}
hw3_tests = {
    'HW3 t2 max: upper end is the sample max (B 1000)': lambda d, s: ci_generic(d, returns, max, 1000, s)[1] == max(returns),
    'HW3 t3 median within 0.1 of -0.25, 0.80 (B 2000)': lambda d, s: (lambda ci: abs(ci[0] + 0.25) < 0.1 and abs(ci[1] - 0.8) < 0.1)(ci_generic(d, returns, statistics.median, 2000, s)),
    'HW3 t8 width > 0.5 (B 500)': lambda d, s: (lambda ci: ci[1] - ci[0] > 0.5)(ci_generic(d, returns, mean_, 500, s)),
}
sweep = {}
for cname, draw in codings().items():
    for tname, fn in {**l11_tests, **hw3_tests}.items():
        bad_ = sum(not fn(draw, 1000 + s) for s in range(SEEDS))
        sweep[(tname, cname)] = bad_
for tname in {**l11_tests, **hw3_tests}:
    tot = sum(sweep[(tname, c)] for c in codings())
    check(f'bootstrap sweep: {tname}: {tot} of {3 * SEEDS} correct runs fail (three codings, fresh seeds)', tot / (3 * SEEDS) < 0.01,
          ', '.join(f'{c}: {sweep[(tname, c)]}' for c in codings()))
# Sharpe test (B 2000, n 250) is slow in pure Python: fewer seeds per coding here, plus a vectorised sweep below
SH = 6 if QUICK else 60
bad_s = {}
for cname, draw in codings().items():
    bad_s[cname] = sum(not (lambda ci: abs(ci[0] + 0.98) < 0.25 and abs(ci[1] - 3.00) < 0.25)(ci_generic(draw, daily, sharpe, 2000, 2000 + s)) for s in range(SH))
check(f'bootstrap sweep: HW3 t4 Sharpe within 0.25 of -0.98, 3.00 (B 2000): {sum(bad_s.values())} of {3 * SH} correct runs fail', sum(bad_s.values()) / (3 * SH) < 0.01, str(bad_s))


def sharpe_vec(X):
    m = X.mean(1); v = X.var(1, ddof=1)
    return m / np.sqrt(v) * math.sqrt(252)


VREP = 300 if QUICK else 3000
ends = np.empty((VREP, 2))
for i in range(VREP):
    v = np.sort(sharpe_vec(D[rng.integers(0, 250, (2000, 250))]))
    ends[i] = v[50], v[1949]
fail_v = ((np.abs(ends[:, 0] + 0.98) >= 0.25) | (np.abs(ends[:, 1] - 3.00) >= 0.25)).mean()
check(f'bootstrap sweep (vectorised, {VREP} runs): Sharpe ends average {ends[:, 0].mean():.3f}, {ends[:, 1].mean():.3f} (sd {ends[:, 0].std():.3f}, {ends[:, 1].std():.3f}); share outside the test band {fail_v:.4%}',
      fail_v < 0.01 and close(ends[:, 0].mean(), -0.98, 0.03) and close(ends[:, 1].mean(), 3.00, 0.03))
# exact-law sweeps: draw the B resampled means straight from their exact distribution (any correct coding is such a draw)
def exact_law(data, scale):
    kk2 = np.round(np.array(data) * scale).astype(int); o2 = kk2.min()
    p2 = np.bincount(kk2 - o2) / len(data)
    pm2 = np.array([1.0])
    for _ in range(len(data)):
        pm2 = np.convolve(pm2, p2)
    return (np.arange(len(pm2)) + len(data) * o2) / (scale * len(data)), pm2


def exact_sweep(data, B, lo_c, hi_c, tol, reps_):
    v2, pm2 = exact_law(data, 10)
    c2 = np.cumsum(pm2)
    bad2 = 0; e_lo = []; e_hi = []
    k2 = int(0.025 * B)
    for _ in range(reps_ // 500):
        u = np.sort(rng.random((500, B)), axis=1)
        lo2 = v2[np.searchsorted(c2, u[:, k2])]; hi2 = v2[np.searchsorted(c2, u[:, B - 1 - k2])]
        bad2 += ((np.abs(lo2 - lo_c) >= tol) | (np.abs(hi2 - hi_c) >= tol)).sum()
        e_lo.append(lo2); e_hi.append(hi2)
    e_lo = np.concatenate(e_lo); e_hi = np.concatenate(e_hi)
    return bad2 / len(e_lo), e_lo.mean(), e_hi.mean(), e_lo.std(), e_hi.std(), v2[np.searchsorted(c2, 0.025)], v2[np.searchsorted(c2, 0.975)]


ER = 4000 if QUICK else 40000
r34 = exact_sweep(returns, 4000, -0.30, 0.55, 0.05, ER)
check(f'bootstrap sweep (exact law, {ER} runs): L11 t3+t4 fail share {r34[0]:.4%}; ends average {r34[1]:.4f}, {r34[2]:.4f} (sd {r34[3]:.4f}, {r34[4]:.4f})', r34[0] < 0.01)
r7 = exact_sweep([2.0, -1.0, 0.5, 0.1, -0.4, 1.2, 0.3, -0.8], 3000, -0.39, 0.92, 0.06, ER)
check(f'bootstrap sweep (exact law, {ER} runs): L11 t7 (eight values, tolerance 0.06) fail share {r7[0]:.4%}; long-run ends {r7[5]:.4f}, {r7[6]:.4f}; ends average {r7[1]:.4f}, {r7[2]:.4f} (sd {r7[3]:.4f}, {r7[4]:.4f})', r7[0] < 0.01)
check('HW3 Sharpe of the 250 days is 0.98 (lesson 11 figure)', close(sharpe(daily), 0.98, 6e-3), f'{sharpe(daily):.4f}')
exec(wb['solution'], pre)
ex_ci = pre['bootstrap_ci'](daily, sharpe, 1000, 1)
med_ci = pre['bootstrap_ci'](returns, statistics.median, 2000, 4)
check('HW3 solution: Sharpe, B 1000, seed 1 is -1.10 to 2.896; median, B 2000, seed 4 is -0.25 to 0.80',
      [round(v, 3) for v in ex_ci] == [-1.1, 2.896] and close(med_ci[0], -0.25, 1e-9) and close(med_ci[1], 0.80, 1e-9), f'{ex_ci}, {med_ci}')
# long-run ends of the median's interval, by a large run, and the weight of the neighbouring atoms
g = np.sort(np.median(R[rng.integers(0, 20, (2000000, 20))], axis=1))
qm = g[int(0.025 * len(g))], g[int(0.975 * len(g)) - 1]
check('HW3 long-run ends of the median interval are -0.25 and 0.80', close(qm[0], -0.25, 1e-9) and close(qm[1], 0.80, 1e-9), str(qm))

# ---------------------------------------------------------------- level 12
l12 = load('l12-updating-a-belief')
seq = eval(l12['screens'][1]['canvas']['derive']['params.A'].split('+', 1)[1].rsplit('[', 1)[0])
check('L12 slider data: 6 heads in 6, 70 in 100; posterior means 0.8 and 0.692', seq[6] == 6 and seq[100] == 70 and close(8 / 10, .8, 1e-12)
      and close(72 / 104, 0.692, 5e-4) and all(0 <= b_ - a_ <= 1 for a_, b_ in zip(seq, seq[1:])))
bi = lambda a_, b_: tuple(stats.beta.ppf([.025, .975], a_, b_))
ok = (close(bi(9, 5)[0], .386, 6e-4) and close(bi(9, 5)[1], .861, 6e-4) and close(bi(160, 140)[0], .477, 6e-4) and close(bi(160, 140)[1], .589, 6e-4)
      and close(bi(22, 18)[0], .396, 6e-4) and close(bi(22, 18)[1], .699, 6e-4) and close(bi(50, 40)[0], .453, 6e-4) and close(bi(50, 40)[1], .656, 6e-4))
check('L12/HW3 beta intervals: (9,5) .386-.861; (160,140) .477-.589; (22,18) .396-.699; (50,40) .453-.656', ok,
      str([tuple(round(v, 3) for v in bi(*ab)) for ab in ((9, 5), (160, 140), (22, 18), (50, 40))]))
lnB = lambda a_, b_: math.lgamma(a_) + math.lgamma(b_) - math.lgamma(a_ + b_)
check('L12 plotted beta constants (ln 1/B): 1.7918, 8.7695, 13.7362, 139.6653, 208.5137, 27.7465, 34.9555, 60.2709',
      all(close(-lnB(a_, b_), c_, 2e-4) for (a_, b_), c_ in {(2, 2): 1.791759, (9, 5): 8.769507, (10, 10): 13.736229, (100, 100): 139.665259,
                                                              (160, 140): 208.513733, (22, 18): 27.746548, (26, 24): 34.955463, (56, 34): 60.270917, (1, 6): 1.791759}.items()))
# MC: Bayes update by brute force. Draw p from the prior, flip, keep runs matching the data: the kept p follow Beta(a + k, b + n - k)
p = rng.beta(2, 2, 3000000)
kk_ = rng.binomial(10, p)
kept = p[kk_ == 7]
check('L12 MC: prior Beta(2,2), 7 heads in 10: posterior mean 9/14 = 0.643, middle 95% is 0.386 to 0.861',
      close(kept.mean(), 9 / 14, 0.002) and close(np.quantile(kept, .025), .386, 0.004) and close(np.quantile(kept, .975), .861, 0.004),
      f'{kept.mean():.4f}, {np.quantile(kept, .025):.3f}, {np.quantile(kept, .975):.3f} ({len(kept)} kept)')
p = rng.random(3000000)
kept = p[rng.binomial(5, p) == 0]
check('L12 MC: flat prior, 0 wins in 5: posterior mean 1/7 (Laplace)', close(kept.mean(), 1 / 7, 0.001), f'{kept.mean():.4f}')
# MC: a credible interval's frequentist reading: with a flat prior and many flips it covers like a confidence interval
ptrue = 0.55; kk_ = rng.binomial(400, ptrue, 200000)
lo = stats.beta.ppf(.025, 1 + kk_, 1 + 400 - kk_); hi = stats.beta.ppf(.975, 1 + kk_, 1 + 400 - kk_)
ph = kk_ / 400; se = np.sqrt(ph * (1 - ph) / 400)
check('L12 MC: flat prior, n = 400: credible and Wald intervals nearly coincide (ends within 0.004) and both cover about 95%',
      np.abs(lo - (ph - 1.96 * se)).max() < 0.004 and np.abs(hi - (ph + 1.96 * se)).max() < 0.004 and close(((lo <= ptrue) & (ptrue <= hi)).mean(), .95, .01))

# ---------------------------------------------------------------- homework and problems
check('HW1 MSE of SS/n, n = 10, sigma^2 = 4: 3.04; s^2: 3.56', close(2 * 9 * 16 / 100 + 0.16, 3.04, 1e-9) and close(2 * 9 * 16 / 81, 3.5556, 1e-4))
c4 = math.sqrt(2 / 4) * math.gamma(5 / 2) / math.gamma(2)
z = rng.standard_normal((500000, 5))
check('HW1 E[s] = 0.94 sigma for five normal days (exact c4 and MC)', close(c4, 0.94, 5e-4) and close(z.std(1, ddof=1).mean(), 0.94, 0.003), f'{c4:.4f}')
z = rng.standard_normal((200000, 50, 5)) if not QUICK else rng.standard_normal((20000, 50, 5))
s_ = z.std(2, ddof=1)
check('HW1 MC: the average of fifty s is low (0.94); the root of the average s^2 is within 1% of sigma',
      close(s_.mean(1).mean(), 0.94, 0.003) and close(np.sqrt((s_ ** 2).mean(1)).mean(), 1.0, 0.01), f'{s_.mean(1).mean():.4f}, {np.sqrt((s_ ** 2).mean(1)).mean():.4f}')
# HW1 longform part 5 gave (until the round 2 fix pass) "it relies on normality, which fat-tailed returns break" as a reason to keep n - 1.
# Fact checked here: for fat tails the gain from a larger divisor does not vanish, it grows.
# MSE(c)/sigma^4 = [2k + kappa k^2/n + (k - c)^2]/c^2 with k = n - 1 and excess kurtosis kappa; smallest near c = n + 1 + kappa.
tt = rng.standard_t(8, (600000, 20)) / math.sqrt(8 / 6)   # variance 1, excess kurtosis 1.5
ss_t = ((tt - tt.mean(1, keepdims=True)) ** 2).sum(1)
mt = {c: ((ss_t / c - 1) ** 2).mean() for c in (19, 20, 21, 22, 23)}
zz = rng.standard_normal((600000, 20))
ss_z = ((zz - zz.mean(1, keepdims=True)) ** 2).sum(1)
mz = {c: ((ss_z / c - 1) ** 2).mean() for c in (19, 21)}
check('HW1 MC (n = 20): dividing by n + 1 beats n - 1 for fat-tailed draws too (t, 8 df), and by a wider margin than for normal draws',
      mt[21] < mt[20] < mt[19] and (1 - mt[21] / mt[19]) > (1 - mz[21] / mz[19]) + 0.01,
      f't8: {({c: round(v, 4) for c, v in mt.items()})}; gain t8 {1 - mt[21] / mt[19]:.3f}, normal {1 - mz[21] / mz[19]:.3f}')
check('HW1 longform: 0.1053, 0.0975, 0.0952', close(38 / 361, .1053, 5e-5) and close(39 / 400, .0975, 1e-12) and close(42 / 441, .0952, 5e-5))
xs = [1.5, 1.2, 3.0, 1.1, 2.4, 1.8]
S = sum(math.log(v) for v in xs)
check('HW2 Pareto: S = 3.2450, alpha-hat 1.85, unbiased 1.54, tails 0.014 and 0.029',
      close(S, 3.2450, 5e-5) and close(6 / S, 1.85, 5e-3) and close(5 / S, 1.54, 5e-3) and close(10 ** (-6 / S), .014, 5e-4) and close(10 ** (-5 / S), .029, 5e-4))
al = 1.5
y = rng.exponential(1 / al, (1000000, 6))
ah = 6 / y.sum(1)
check('HW2 MC: Pareto MLE has mean n/(n-1) alpha (n = 6: 1.8 for alpha 1.5); (n-1)/n of it is unbiased',
      close(ah.mean(), 1.8, 0.005) and close((5 / 6 * ah).mean(), 1.5, 0.004), f'{ah.mean():.4f}')
u = rng.random(1000000) ** (-1 / al)
check('HW2 MC: ln of a Pareto(alpha) is exponential with rate alpha', close(np.log(u).mean(), 1 / al, 0.003) and close((np.log(u) > 1).mean(), math.exp(-al), 0.002))
check('HW2 numbers: e^0.375 = 1.455; log scores -6.390, -6.109; vol 0.9055, 14.375; 0.8^8 = 0.17',
      close(math.exp(.375), 1.455, 5e-4) and close(7 * math.log(.8) + 3 * math.log(.2), -6.3903, 1e-4) and close(7 * math.log(.7) + 3 * math.log(.3), -6.1086, 1e-4)
      and close(math.sqrt(4.92 / 6), .9055, 5e-5) and close(math.sqrt(4.92 / 6) * math.sqrt(252), 14.375, 2e-3) and close(.8 ** 8, .17, 5e-3))
check('HW2 code test 9: 5,000 densities of 24.2; log-likelihood 15931.158',
      close(stats.norm.pdf(.01, 0, .01), 24.2, 0.01) and close(stats.norm.logpdf([.01] * 5000, 0, .01).sum(), 15931.158263917092, 1e-6)
      and math.isinf(float(np.prod(stats.norm.pdf([.01] * 5000, 0, .01)))))
# Wald coverage at n = 50 ("nearer 94% at this n")
kx = np.arange(51); ph = kx / 50
se = np.sqrt(ph * (1 - ph) / 50)
covs = {p_: stats.binom.pmf(kx, 50, p_)[(ph - 1.96 * se <= p_) & (p_ <= ph + 1.96 * se)].sum() for p_ in (0.5, 0.55, 0.6, 0.65)}
check('HW3 Wald interval at n = 50 covers "nearer 94%" for p around 0.6 (exact binomial sums, within 0.93 to 0.95)',
      all(0.93 <= v <= 0.95 for v in covs.values()), str({k_: round(v, 4) for k_, v in covs.items()}))
check('HW3 numbers: n = 2377; t multiplier 15% wider; m = 25; SE 0.0693; sd 0.0521',
      math.ceil(1.96 ** 2 * .2475 / .0004 - 1e-9) == 2377 and close(stats.t.ppf(.975, 9) / 1.96, 1.154, 2e-3) and close((12.5 + 60) / 125, .58, 1e-12)
      and close(math.sqrt(.24 / 50), .0693, 5e-5) and close(math.sqrt(50 * 40 / (90 ** 2 * 91)), .0521, 5e-5))
# speed bump: exact interval for a uniform maximum
ns8 = {}
exec(hw3['items'][8]['widget']['solution'], ns8)
check('HW3 bump: replayed coverages 0.947 and 0.90267; intervals 30.254-102.599, 4.1026-160',
      ns8['bump_coverage'](10.0, 5, 0.95, 2000, 1) == 0.947 and close(ns8['bump_coverage'](250.0, 20, 0.9, 1500, 11), 0.9026666666666666, 1e-12)
      and close(ns8['bump_interval']([12.0, 30.0, 21.0], .95)[1], 102.59855680060177, 1e-9) and close(ns8['bump_interval']([4.0], .95)[0], 4.102564102564103, 1e-12))
okb = True; det = []
for n_, lev in ((1, .5), (2, .8), (5, .95), (20, .9), (50, .99)):
    m_ = (7.0 * rng.random((400000, n_))).max(1); a_ = 1 - lev
    cv = ((m_ / (1 - a_ / 2) ** (1 / n_) <= 7.0) & (7.0 <= m_ / (a_ / 2) ** (1 / n_))).mean()
    det.append(round(cv, 4)); okb &= close(cv, lev, 0.003)
check('HW3 MC: the max-based interval covers theta with chance exactly the level at n = 1, 2, 5, 20, 50', okb, str(det))
mon = np.array([2.0, 4.0, 9.0])
bm = mon[rng.integers(0, 3, (1000000, 3))].mean(1)
check('P3 bootstrap SE of three returns: 1.70 against s/sqrt(n) = 2.08; ratio sqrt(2/3)', close(bm.std(), 1.70, 0.01) and close(mon.std(ddof=1) / math.sqrt(3), 2.08, 5e-3)
      and close(math.sqrt(26 / 9) / math.sqrt(13 / 3), math.sqrt(2 / 3), 1e-12))
check('P3 numbers: SE 0.0150, lower end 0.131; difference SE 0.461, interval -0.10 to 1.70; gap 0.53 SE',
      close(math.sqrt(.16 * .84 / 600), .0150, 5e-5) and close(.16 - 1.96 * math.sqrt(.16 * .84 / 600), .131, 5e-4) and close(math.hypot(.30, .35), .461, 5e-4)
      and close(.8 - 1.96 * math.hypot(.30, .35), -.10, 5e-3) and close(.01 / math.sqrt(.21 / 580), .53, 5e-3))
a_ = 2.4 + 3.0 * rng.standard_normal((200000, 100)); b_ = 1.6 + 4.2 * rng.standard_normal((200000, 144))
check('P3 MC: sd of the difference of two independent means is 0.461', close((a_.mean(1) - b_.mean(1)).std(), 0.461, 0.004))
check('P2 numbers: LR 3.03; e^1.125 = 3.08; 55.29; sigma 1.0874, 7.84, 1.96, 123 weeks; 5/28, 0.1677',
      close((.75 / .9) ** 9 * 2.5 ** 3, 3.03, 5e-3) and close(math.exp(1.125), 3.08, 5e-3) and close(51 + math.sqrt(8 * math.log(10)), 55.2919, 1e-4)
      and close(math.sqrt(9.46 / 8), 1.0874, 5e-5) and close(math.sqrt(9.46 / 8) * math.sqrt(52), 7.84, 5e-3) and math.ceil((7.84 / .5) ** 2 / 2) == 123
      and close(math.exp(-50 / 28), .1677, 5e-5))
# MC: censored exponential MLE = events / total exposure
lam = 0.2
w = rng.exponential(1 / lam, (200000, 30)); cens = np.minimum(w, 8.0)
est = (w <= 8.0).sum(1) / cens.sum(1); naive = 30 / cens.sum(1)
check('P2 MC: with waits cut off at 8 minutes, events/total time centres on the true rate; treating cut-offs as finished waits overstates it',
      close(est.mean(), lam, 0.01) and naive.mean() > 1.15 * lam, f'{est.mean():.4f}, {naive.mean():.4f}')
check('P1 numbers: 310, 110, 4.69, 28 pings; 2.8125, 2.598; 4/9 at w = 8/9; 76, 0.51',
      close(np.var([304, 318, 296, 322, 310], ddof=1), 110, 1e-9) and close(math.sqrt(22), 4.69, 5e-3) and math.ceil(110 / 4) == 28
      and close(2.25 / 4 + 2.25, 2.8125, 1e-12) and close(math.sqrt(6.75), 2.5981, 5e-5) and close(.5 * 64 / 81 + 4 / 81, 4 / 9, 1e-12)
      and close(np.mean(np.square([12, -6, 6, -10, 8])), 76, 1e-9) and close(2 / math.sqrt(76 / 5), .51, 5e-3))
A_ = 6 * rng.standard_normal((300000, 9)); B_ = 0.5 + 3 * rng.standard_normal((300000, 36))
bl = 8 / 9 * B_.mean(1) + 1 / 9 * A_.mean(1)
check('P1 MC: blend of biased B and unbiased A at w = 8/9 has MSE 4/9, below both 0.5 and 4',
      close((bl ** 2).mean(), 4 / 9, 0.006) and close((B_.mean(1) ** 2).mean(), 0.5, 0.006) and close((A_.mean(1) ** 2).mean(), 4, 0.04))

# ---------------------------------------------------------------- fluency families, whole range
def expand(v):
    if 'pick' in v:
        return list(v['pick'])
    lo_, hi_ = v['int']
    return list(range(lo_, hi_ + 1))


def sweep_family(fam, env_fn):
    names = list(fam['vars'])
    n_ok = 0; problems = []
    for combo in itertools.product(*[expand(fam['vars'][nm]) for nm in names]):
        env = {}
        for nm, val in zip(names, combo):
            as_ = fam['vars'][nm].get('as')
            if as_:
                env.update(dict(zip(as_, val)))
            else:
                env[nm] = val
        msg = env_fn(env)
        if msg is None:
            continue
        n_ok += 1
        if msg:
            problems.append((combo, msg))
    return n_ok, problems


f9 = load('fluency-l9-how-precise')['families']
f10 = load('fluency-l10-catching-the-truth')['families']


def fam_se(e):
    key = e['s'] / e['rt']
    if e['rt'] ** 2 != e['n']:
        return 'rt is not sqrt(n)'
    if abs(key * 1e5 - round(key * 1e5)) > 1e-7:
        return 'answer not an exact decimal'
    if len({round(key, 9), round(e['s'] / e['n'], 9), e['s']}) < 3:
        return 'a slip equals the key'
    return ''


def fam_prop(e):
    if (e['pc'] * e['n']) % 100:
        return None
    p_ = e['pc'] / 100
    if not close(math.sqrt(p_ * (1 - p_)), e['rootpq'], 1e-12) or e['rt'] ** 2 != e['n']:
        return 'root wrong'
    key = e['rootpq'] / e['rt']
    if not close(key, math.sqrt(p_ * (1 - p_) / e['n']), 1e-12):
        return 'key is not the SE'
    if len({round(key, 10), round(p_ * (1 - p_) / e['n'], 10), round(e['rootpq'] / e['n'], 10)}) < 3:
        return 'a slip equals the key'
    return ''


def fam_need(e):
    key = e['n'] * e['k'] ** 2
    se2 = e['se1'] / e['k']
    # the answer is right iff se1 * sqrt(n / key) == se2
    if not close(e['se1'] * math.sqrt(e['n'] / key), se2, 1e-12):
        return 'key wrong'
    if len({key, e['n'] * e['k'], key - e['n']}) < 3:
        return 'a slip equals the key'
    return ''


def fam_ci(e):
    zt = {90: stats.norm.ppf(.95), 95: stats.norm.ppf(.975), 99: stats.norm.ppf(.995)}[e['lev']]
    if abs(zt - e['z']) > 6e-4:
        return 'multiplier'
    lo_, hi_ = e['xh'] / 100 - e['z'] * e['sh'] / 100, e['xh'] / 100 + e['z'] * e['sh'] / 100
    for end, e1, e96 in ((lo_, e['xh'] / 100 - e['sh'] / 100, e['xh'] / 100 - 1.96 * e['sh'] / 100), (hi_, e['xh'] / 100 + e['sh'] / 100, e['xh'] / 100 + 1.96 * e['sh'] / 100)):
        if abs(end - e1) <= 0.001 or (e['lev'] != 95 and abs(end - e96) <= 0.001):
            return 'a slip lies within tolerance of the key'
        if abs(round(end, 3) - end) > 0.0005 + 1e-12:
            return '3 dp answer outside tolerance'
    return ''


def fam_hw(e):
    if e['rt'] ** 2 != e['n']:
        return 'rt'
    key = e['z'] * e['s'] / e['rt']
    if abs(round(key, 3) - key) > 0.0005 + 1e-12:
        return '3 dp answer outside tolerance'
    if abs(key - e['z'] * e['s']) <= 0.001 or abs(key - e['z'] * e['s'] / e['n']) <= 0.001:
        return 'a slip lies within tolerance of the key'
    tm = stats.t.ppf({90: .95, 95: .975, 99: .995}[e['lev']], e['n'] - 1)
    if tm / e['z'] > 1.035:
        return f't multiplier {tm:.3f} is not close to {e["z"]}'
    return ''


for fam, fn in ((f9[0], fam_se), (f9[1], fam_prop), (f9[2], fam_need), (f10[0], fam_ci), (f10[1], fam_hw)):
    n_ok, probs = sweep_family(fam, fn)
    check(f'fluency {fam["id"]}: {n_ok} variable combinations, every key right and every slip distinct', not probs, str(probs[:3]))

# ---------------------------------------------------------------- round 2 fix pass (added by the fixer)
# Finding 1: s^2 is unbiased whatever the distribution; the MSE-best divisor is n + 1 + kappa (n - 1)/n.
nn, kk = 20, 19
def mse_k(c_, kap):
    return (2 * kk + kap * kk * kk / nn + (kk - c_) ** 2) / c_ ** 2
grid = np.linspace(15, 30, 150001)
opt = {kap: grid[np.argmin(mse_k(grid, kap))] for kap in (-1.2, 0.0, 1.5, 6.0)}
check('fix r2 HW1: MSE-best divisor n + 1 + kappa (n - 1)/n (19.86, 21, 22.43, 26.7 for kappa -1.2, 0, 1.5, 6)',
      all(close(opt[k_], nn + 1 + k_ * kk / nn, 2e-4) for k_ in opt), str({k_: round(float(v), 3) for k_, v in opt.items()}))
check('fix r2 HW1: E[s^2] = sigma^2 for fat-tailed t8 draws; dividing by 21 gains about 10% for normal data',
      close(ss_t.mean() / 19, 1.0, 0.004) and close(1 - mz[21] / mz[19], 0.10, 0.01), f'{ss_t.mean() / 19:.4f}, gain {1 - mz[21] / mz[19]:.3f}')
h1 = [it for it in load('homework-1')['items'] if it['id'] == 'h-long-n-plus-one'][0]
check('fix r2 HW1 text: part 5 and rubric item 7 no longer give normality as a reason to keep n - 1',
      'normality' not in h1['model'] and 'normality' not in h1['rubric'][6]['text'] and 'push the best divisor' in h1['model'])
# Finding 4: for 0/1 data the divide-by-n variance is p(1 - p); s^2 is n/(n - 1) times it.
xb = np.array([1] * 90 + [0] * 60)
check('fix r2 l9: 0/1 data: np.var(ddof=0) = p(1 - p) = 0.24; ddof=1 gives 150/149 of it',
      close(xb.var(), 0.24, 1e-12) and close(xb.var(ddof=1), 0.24 * 150 / 149, 1e-12))
# Finding 7: the log score is strictly proper.
qq = np.linspace(0.001, 0.999, 999)
check('fix r2 HW2: expected log score p ln q + (1 - p) ln(1 - q) peaks at q = p (p = 0.3, 0.7, 0.8)',
      all(close(qq[np.argmax(p_ * np.log(qq) + (1 - p_) * np.log(1 - qq))], p_, 1e-9) for p_ in (0.3, 0.7, 0.8)))
# Finding 9: the l3 s10 test-1 line's numbers.
v3 = np.array([2.0, 4.0, 6.0])
check('fix r2 l3 s10 test-1 line: [2, 4, 6] gives sd 2.0, divide-by-n sd 1.633, np.var 2.667 and 4.0 with ddof=1',
      close(v3.std(ddof=1), 2.0, 1e-12) and close(v3.std(), 1.633, 5e-4) and close(v3.var(), 2.667, 5e-4) and close(v3.var(ddof=1), 4.0, 1e-12))
# Finding 10: the review 1 decimal slip band holds 0.000667, 0.00067 and 0.0007, and not 0, 0.005 or the key.
dw = load('review-1')['items'][2]['widget']
sl = [w_ for w_ in dw['wrong'] if w_['id'] == 'decimal'][0]
inb = lambda v: abs(v - sl['value']) <= sl['tol']['abs']
check('fix r2 review 1 decimal slip: 0.002/3 = 0.000667; band takes 0.000667, 0.00067, 0.0007, not 0, 0.005, 6.67',
      close(0.002 / 3, sl['value'], 1e-8) and all(inb(v) for v in (0.000667, 0.00067, 0.0007)) and not any(inb(v) for v in (0, 0.005, 6.6667)))

print()
print(f'{n_checks} checks, {len(fails)} failed')
for f_ in fails:
    print('  FAILED:', f_)
sys.exit(1 if fails else 0)
