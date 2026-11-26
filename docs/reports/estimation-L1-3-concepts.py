#!/usr/bin/env python3
"""Concept audit estimation L1-3, round 1: recomputation and Monte Carlo checks.

Run from anywhere:  python docs/reports/estimation-L1-3-concepts.py
Exits 0 when every CHECK holds. A CHECK that fails because the content is false as stated stays
failing (it is a finding in docs/reviews/audit-estimation-1-3.md). NOTE lines carry the evidence for
`imprecise` and `misleading` findings and never fail the script.
NumPy/SciPy only; seeds fixed. Replication counts are chosen so the Monte Carlo standard error is at
most a fifth of the gap between the claim and its negation.
"""
import itertools, json, math, os, random, statistics, sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'estimation')
load = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf-8'))
rng = np.random.default_rng(20261126)
fails = []


def check(name, ok, detail=''):
    detail = str(detail)
    print(('ok   ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))
    if not ok:
        fails.append(name)


def note(name, detail):
    print('NOTE ' + name + ': ' + str(detail))


close = lambda a, b, tol: abs(a - b) <= tol
num = lambda s: float(str(s).replace('−', '-'))

# ---------------------------------------------------------------- L1: the 100-day population
l1 = load('l1-sample-population')
cells = [[num(v) for v in row] for row in l1['screens'][2]['canvas']['params']['cells']]
pop = np.array(sum(cells, []))
at = lambda ref: cells[int(ref[1:ref.index('c')]) - 1][int(ref[ref.index('c') + 1:]) - 1]
shade = l1['screens'][3]['canvas']['state']['shade']
A = np.array([at(r) for r in shade['sample A']]); B = np.array([at(r) for r in shade['sample B']])
check('l1 mu = 0.10, sigma = 1.00 (divide by N), p = 0.47', close(pop.mean(), 0.10, 5e-4) and close(pop.std(), 1.00, 5e-3) and close((pop > 0).mean(), 0.47, 1e-9), (pop.mean(), pop.std(), (pop > 0).mean()))
check('l1 sample A: mean 0.42, s 1.21, p-hat 0.7, sum of sizes 10.6', close(A.mean(), 0.42, 1e-9) and close(A.std(ddof=1), 1.21, 5e-3) and close((A > 0).mean(), 0.7, 1e-9) and close(np.abs(A).sum(), 10.6, 1e-9), (A.mean(), A.std(ddof=1)))
check('l1 sample B mean -0.15; one day in both samples', close(B.mean(), -0.15, 1e-9) and len(set(shade['sample A']) & set(shade['sample B'])) == 1)
check('l1/l2 single days range -1.9 to 2.9 (4.8 points)', pop.min() == -1.9 and pop.max() == 2.9)

# ---------------------------------------------------------------- L2: exact law of the mean of 10 draws with replacement
k = np.rint(pop * 10).astype(int); off = k.min()
pmf1 = np.bincount(k - off) / 100.0
pmf = np.array([1.0])
for _ in range(10):
    pmf = np.convolve(pmf, pmf1)
means = (np.arange(len(pmf)) + 10 * off) / 100.0
ex = (pmf * means).sum(); sd = math.sqrt((pmf * (means - ex) ** 2).sum())
check('l2 E[Xbar] = mu and SE = sigma/sqrt(10) = 0.316 exactly', close(ex, 0.10, 1e-9) and close(sd, 1 / math.sqrt(10), 2e-3), (ex, sd))
inside = pmf[(means >= 0.10 - 0.63 - 1e-9) & (means <= 0.10 + 0.63 + 1e-9)].sum()
check('l2 S8: exactly 95.6% of samples of 10 land within 0.10 +/- 0.63', close(inside, 0.956, 6e-4), round(inside, 4))
bars = l1 and load('l2-estimates-vary')['screens'][1]['canvas']['params']['exact']
tot = sum(b['y'] for b in bars if -0.2 <= b['x'] - 0.1 and b['x'] + 0.1 <= 0.4 + 1e-9)
mid = pmf[(means >= -0.2 - 1e-9) & (means < 0.4 - 1e-9)].sum()
check('l2 S2 caption: -0.2 to 0.4 holds about 66% (exact bins)', close(mid, 0.66, 0.01) and close(tot, mid, 2e-3), (round(mid, 4), round(tot, 4)))
check('l2 S8 option: half the means within 0.67 SE; 2 SE about 95%', close(2 * stats.norm.cdf(0.67) - 1, 0.5, 0.005) and close(2 * stats.norm.cdf(2) - 1, 0.9545, 1e-4))
check('l2 S9: a no-edge signal prints a mean of 0.4% or more "often"', stats.norm.sf(0.4 / (2.5 / math.sqrt(20))) > 0.2, round(stats.norm.sf(0.4 / (2.5 / math.sqrt(20))), 3))

# ---------------------------------------------------------------- L3: n - 1
x = rng.standard_normal((400000, 5))
vn = x.var(axis=1); s2 = x.var(axis=1, ddof=1); s = np.sqrt(s2)
se = vn.std() / math.sqrt(len(vn))
check('l3 S0: divide-by-n averages 0.8 at n = 5 (MC)', close(vn.mean(), 0.8, 5 * se), (round(vn.mean(), 4), 'se', round(se, 4)))
check('l3: s^2 unbiased (MC)', close(s2.mean(), 1.0, 5 * s2.std() / math.sqrt(len(s2))), round(s2.mean(), 4))
c4 = math.sqrt(2 / 4) * math.gamma(5 / 2) / math.gamma(2)
check('l3/hw1: E[s] < sigma; about 0.94 sigma at n = 5 (MC and c4)', s.mean() < 1 - 20 * s.std() / math.sqrt(len(s)) and close(s.mean(), 0.94, 0.002) and close(c4, 0.94, 5e-4), (round(s.mean(), 4), round(c4, 4)))
desks = rng.standard_normal((40000, 50, 5)).var(axis=2, ddof=1)
a1 = np.sqrt(desks).mean(axis=1); a2 = np.sqrt(desks.mean(axis=1))
check('hw1 h-average-s: mean of 50 s sits below sigma; root of mean s^2 comes closer', a1.mean() < 0.95 and abs(a2.mean() - 1) < abs(a1.mean() - 1) / 5, (round(a1.mean(), 4), round(a2.mean(), 4)))
samples = list(itertools.product([-1, 0, 1], repeat=2))
vn9 = [np.var(t) for t in samples]; s9 = [math.sqrt(np.var(t, ddof=1)) for t in samples]
check('l3 S2-S4: nine samples average 1/3, 2/3 and E[s] = 0.63 against 0.82', close(np.mean(vn9), 1 / 3, 1e-12) and close(np.mean([np.var(t, ddof=1) for t in samples]), 2 / 3, 1e-12) and close(np.mean(s9), 0.63, 0.005) and close(math.sqrt(2 / 3), 0.82, 0.005))
check('l3 S2/S3 slips: distinct-value averages 0.4167 and 0.8333', close((0 + 0.25 + 1) / 3, 0.4167, 1e-4) and close((0 + 0.5 + 2) / 3, 0.8333, 1e-4))
d5 = np.array([0.4, 1.2, -0.3, 0.9, 0.3])
check('l3 S5: SS about xbar 1.34, about mu 2.14, gap n(xbar-mu)^2 = 0.8', close(((d5 - 0.5) ** 2).sum(), 1.34, 1e-9) and close(((d5 - 0.1) ** 2).sum(), 2.14, 1e-9))
r = math.sqrt(20 / 19)
check('l3 S9: ratio sqrt(20/19) = 1.026; slips 0.0526, 0.00036, 0.0253; 250 days 0.2%', close(r, 1.026, 5e-4) and close(20 / 19 - 1, 0.0526, 1e-4) and close(1 - 1 / r, 0.0253, 1e-4) and close((math.sqrt(2) - math.sqrt(1.9)) / 100, 0.00036, 1e-5) and close(math.sqrt(250 / 249) - 1, 0.002, 1e-4))
check('l3 S10 tests: ddof=1 values', all(close(np.std(a, ddof=1), e, 1e-6) for a, e in [([2, 4, 6], 2.0), ([1.0, -0.5, 0.8, 0.2, -1.1], 0.881476), ([0.4, 1.2, -0.3, 0.9, 0.3], 0.578792), ([-2.0, 3.0], 3.535534), ([0.12, -0.34, 0.56, -0.78, 0.9, -0.11, 0.05], 0.555839)]) and close(np.std([1.0, -0.5, 0.8, 0.2, -1.1]), 0.788, 5e-4))
# S9 wording "the n version is 2.6% too low": against sigma itself both are low
sd20 = np.sqrt(rng.standard_normal((400000, 20)).var(axis=1))
note('l3 S9 "dividing by n understates the volatility by 2.6%"', 'at n = 20 the n version averages %.4f sigma (%.1f%% low) and s itself averages %.4f sigma; 2.6%% is the gap to s as a share of the n version' % (sd20.mean(), 100 * (1 - sd20.mean()), sd20.mean() * r))

# ---------------------------------------------------------------- L4: MSE
pts = {p['id']: p['y'] for p in load('l4-bias-against-variance')['screens'][0]['canvas']['state']['points']}
a = np.array([pts['a%d' % i] for i in range(1, 9)]); b = np.array([pts['b%d' % i] for i in range(1, 9)])
check('l4 S0: B = A/2, B closer on 6 of 8, mean squared miss 0.018 against 0.041', np.allclose(b, a / 2) and (np.abs(b - 0.2) < np.abs(a - 0.2)).sum() == 6 and close(((b - 0.2) ** 2).mean(), 0.018, 6e-4) and close(((a - 0.2) ** 2).mean(), 0.041, 6e-4), (((b - 0.2) ** 2).mean(), ((a - 0.2) ** 2).mean()))
mse = lambda w, v=0.04, m2=0.04: w * w * v + (1 - w) ** 2 * m2
check('l4 S1-S3: MSE(0.5) = 0.02, MSE(0.8) = 0.0272, MSE(0) = MSE(1) = 0.04; mu = 0.5 gives 0.25', close(mse(0.5), 0.02, 1e-12) and close(mse(0.8), 0.0272, 1e-12) and close(mse(0), 0.04, 1e-12) and close(mse(0, 0.04, 0.25), 0.25, 1e-12))
xb = 0.2 + 0.2 * rng.standard_normal(2000000)
check('l4 S0/S2 MC: 0.5 Xbar has bias -0.1, variance 0.01, MSE 0.02 against 0.04', close((0.5 * xb).mean() - 0.2, -0.1, 1e-3) and close(((0.5 * xb - 0.2) ** 2).mean(), 0.02, 2e-4) and close(((xb - 0.2) ** 2).mean(), 0.04, 4e-4))
# hint "the lowest point of the solid curve is where the two dashed curves cross": true only when v = mu^2
v_, a_ = 0.04, 0.01
wmin = a_ / (a_ + v_); wcross = math.sqrt(a_) / (math.sqrt(a_) + math.sqrt(v_))
note('l4 S1 hint "lowest point is where the two dashed curves cross"', 'with v = 0.04 and mu^2 = 0.01 the minimum is at w = %.3f but the curves cross at w = %.3f; they agree only when v = mu^2' % (wmin, wcross))
ss = (x - x.mean(axis=1, keepdims=True)) ** 2
ss = ss.sum(axis=1)
m = {c: ((ss / c - 1) ** 2).mean() for c in (4, 5, 6, 7)}
check('l4 S5: MSE of SS/c at n = 5 is 0.5, 0.36, 0.333 for c = 4, 5, 6 (MC), smallest at n + 1', close(m[4], 0.5, 0.01) and close(m[5], 0.36, 0.006) and close(m[6], 1 / 3, 0.005) and m[6] < m[5] < m[4] and m[6] < m[7], {c: round(v, 4) for c, v in m.items()})
f = lambda n, c: (2 * (n - 1) + (n - 1 - c) ** 2) / c ** 2
check('l4 quiz / hw1: MSE formula minimised at c = n + 1 for n = 2..60; n = 20 gives 0.1053, 0.0975, 0.0952', all(min(range(1, 3 * n), key=lambda c: f(n, c)) == n + 1 for n in range(2, 61)) and close(f(20, 19), 0.1053, 5e-5) and close(f(20, 20), 0.0975, 1e-12) and close(f(20, 21), 0.0952, 5e-5))
check('hw1 h-mse-vn: 3.04 against 3.56 (n = 10, sigma^2 = 4)', close(16 * f(10, 10), 3.04, 1e-9) and close(16 * f(10, 9), 3.5556, 1e-4))
check('l4 S8 Blume: 1.402, 0.598; swapped 1.198', close(0.67 * 1.6 + 0.33, 1.402, 1e-9) and close(0.67 * 0.4 + 0.33, 0.598, 1e-9) and close(0.33 * 1.6 + 0.67, 1.198, 1e-9))

# ---------------------------------------------------------------- L5-L7: likelihood
L = lambda p: p * p * (1 - p)
check('l5: L(2/3) = 4/27, ratio 32/27, L(0.45) = 0.111 > L(0.85) = 0.108, area 1/12', close(L(2 / 3), 4 / 27, 1e-12) and close(L(2 / 3) / L(0.5), 1.185, 5e-4) and L(0.45) > L(0.85) and close(L(0.45), 0.111, 5e-4) and close(L(0.85), 0.108, 5e-4) and close(1 / 3 - 1 / 4, 1 / 12, 1e-12))
check('l5 S8: L(0.5)/L(0.6) = 0.67 for 12 wins in 20; peak 1.427 millionths', close(0.5 ** 20 / (0.6 ** 12 * 0.4 ** 8), 0.67, 0.005) and close(1e6 * 0.6 ** 12 * 0.4 ** 8, 1.427, 1e-3))
rows = load('l5-which-fits')['screens'][9]['canvas']['params']['rows']
rr = np.array([num(q[1]) for q in rows]); f1 = np.array([num(q[2]) for q in rows]); f2 = np.array([num(q[3]) for q in rows])
check('l5 S9 table densities and ratio 5.554; slips 0.18 and 1.51', np.allclose(f1, stats.norm.pdf(rr, 0, 1), atol=6e-5) and np.allclose(f2, stats.norm.pdf(rr, 0, 2), atol=6e-5) and close(np.prod(stats.norm.pdf(rr, 0, 1) / stats.norm.pdf(rr, 0, 2)), 5.554, 2e-3) and close(f2.prod() / f1.prod(), 0.18, 2e-3) and close(f1.sum() / f2.sum(), 1.51, 5e-3), np.round(f1 / f2, 3))
check('l5 quiz: 27/16, (11/9)^2 = 1.4938, wins only 3.3335', close(0.75 ** 3 * 0.25 / 0.5 ** 4, 27 / 16, 1e-12) and close((11 / 9) ** 2, 1.4938, 1e-4) and close((11 / 9) ** 6, 3.3335, 1e-4))
obs = np.array([1.2, 2.0, 3.7])
grid = np.linspace(0, 5, 5001)
check('l6 S6: product of normal heights peaks at the mean 2.3, value 0.0124', close(grid[np.argmax([stats.norm.pdf(obs, g, 1).prod() for g in grid])], 2.3, 1e-3) and close(stats.norm.pdf(obs, 2.3, 1).prod(), 0.0124, 5e-5))
check('l6 S10: Poisson L(5)/L(4) = 0.52, L(3)/L(4) = 0.40', close(math.exp(-6) * 1.25 ** 24, 0.52, 0.006) and close(math.exp(6) * 0.75 ** 24, 0.40, 0.006))
check('l6 S4 options: L(0.1) = 0.35, L(0.5) = 0.001 for ten tails', close(0.9 ** 10, 0.35, 0.002) and close(0.5 ** 10, 0.001, 5e-5))
# MLE of a Poisson rate and of p are the sample mean / share: numeric maximisation on random data
ok = True
for _ in range(200):
    cnt = rng.poisson(3.0, 7); lam = np.linspace(0.01, 12, 12000)
    ok &= abs(lam[np.argmax(-7 * lam + cnt.sum() * np.log(lam))] - cnt.mean()) < 2e-3 or cnt.sum() == 0
check('l6/hw2: numeric maximiser of the Poisson log-likelihood is the sample mean (200 random samples)', bool(ok))
check('l7: ln(4/27) = -1.9095; slips -0.1806, -0.8293; l(0.6) = -1.938; product of logs -0.239', close(math.log(4 / 27), -1.9095, 5e-5) and close(math.log(2 / 3) ** 2 * math.log(1 / 3), -0.1806, 5e-5) and close(math.log10(4 / 27), -0.8293, 5e-5) and close(math.log(0.144), -1.938, 5e-4) and close(math.log(0.6) ** 2 * math.log(0.4), -0.239, 5e-4))
check('l7 S1/S6: 0.7^70 0.3^30 = 3e-27 (log -61.1); 0.5**1000 = 9.33e-302; 0.5**2000 underflows to 0', close(70 * math.log(0.7) + 30 * math.log(0.3), -61.1, 0.05) and repr(0.5 ** 1000) == '9.332636185032189e-302' and 0.5 ** 2000 == 0.0 and repr(2000 * math.log(0.5)) == '-1386.2943611198905')
r6 = [0.3, -0.5, 0.1, 0.8, -0.2, -0.4]
ll = lambda rs, mu, sg: -len(rs) / 2 * math.log(2 * math.pi * sg ** 2) - sum((q - mu) ** 2 for q in rs) / (2 * sg ** 2)
check('l7 S9 / hw2 tests: l_A = -3.735, l_B = -5.104, difference 1.3698, ratio 3.93', close(ll(r6, 0, 0.4), -3.7346368079831063, 1e-9) and close(ll(r6, 0, 0.8), -5.104457391342778, 1e-9) and close(ll(r6, 0, 0.4) - ll(r6, 0, 0.8), 1.3698, 5e-5) and close(math.exp(1.3698), 3.9346, 1e-3))
check('l7 S10: log scores B -2.6187, A -2.4488; slips -0.3161, -0.4214', close(3 * math.log(0.9) + math.log(0.1), -2.6187, 5e-5) and close(3 * math.log(0.6) + math.log(0.4), -2.4488, 5e-5) and close(3 * math.log(0.9), -0.3161, 5e-5) and close(4 * math.log(0.9), -0.4214, 5e-5))

# ---------------------------------------------------------------- L8: volatility by maximum likelihood
R20 = np.array([0.0042, -0.0115, 0.0087, -0.003, 0.0164, -0.0072, 0.0015, -0.021, 0.0095, 0.0033, -0.0048, 0.0121, -0.0086, 0.0007, -0.0137, 0.0058, 0.0205, -0.0064, 0.0026, -0.0011]) * 100
SS = ((R20 - R20.mean()) ** 2).sum()
check('l8 S0/S1: mean 0.04, SS 20.3098, sum of squares 20.3418, sigma-hat 1.0077, l(1.01) = -28.533, best sigma at mu = 1 is 1.39', close(R20.mean(), 0.04, 1e-9) and close(SS, 20.3098, 1e-4) and close((R20 ** 2).sum(), 20.3418, 1e-4) and close(math.sqrt(SS / 20), 1.0077, 5e-5) and close(-10 * math.log(2 * math.pi * 1.01 ** 2) - SS / (2 * 1.01 ** 2), -28.533, 1e-3) and close(math.sqrt(((R20 - 1) ** 2).mean()), 1.39, 5e-3))
sg = np.linspace(0.5, 2.0, 15001)
check('l8 S2: numeric maximiser of l(mean, sigma) divides by n, not n - 1', close(sg[np.argmax(-10 * np.log(2 * math.pi * sg ** 2) - SS / (2 * sg ** 2))], math.sqrt(SS / 20), 2e-4))
check('l8 S7/S8/S10: 0.010077, 0.010085, n-1 0.010339; annual 15.997, 365 days 19.25, n-1 16.41', close(math.sqrt(SS / 20) / 100, 0.010077, 5e-7) and close(math.sqrt((R20 ** 2).mean()) / 100, 0.010085, 5e-7) and close(math.sqrt(SS / 19) / 100, 0.010339, 5e-7) and close(1.0077 * math.sqrt(252), 15.997, 1e-3) and close(1.0077 * math.sqrt(365), 19.252, 1e-3) and close(math.sqrt(SS / 19) * math.sqrt(252), 16.41, 5e-3))
r5 = np.array([0.5, -1.0, 1.5, -0.5, 1.0])
lv = lambda v: -2.5 * math.log(2 * math.pi * v) - 4.3 / (2 * v)
check('l8 S3-S6: SS 4.30, sigma-hat 0.927, l(0.86) = -6.718 > l(1.075) = -6.776, zero-mean 0.975', close(((r5 - 0.3) ** 2).sum(), 4.30, 1e-9) and close(math.sqrt(0.86), 0.9274, 5e-5) and close(lv(0.86), -6.718, 1e-3) and close(lv(1.075), -6.776, 1e-3) and close(math.sqrt(0.95), 0.9747, 5e-5))
xn = rng.standard_normal((300000, 20))
vh = xn.var(axis=1); s2n = xn.var(axis=1, ddof=1)
m_mle = ((vh - 1) ** 2).mean(); m_s2 = ((s2n - 1) ** 2).mean()
check('l8 S4 / quiz q-bias: for normal data the divide-by-n variance is biased low and has the lower MSE (n = 20: 0.0975 against 0.1053)', vh.mean() < 0.96 and close(m_mle, 39 / 400, 0.002) and close(m_s2, 2 / 19, 0.002) and m_mle < m_s2, (round(vh.mean(), 4), round(m_mle, 4), round(m_s2, 4)))
for n in (5, 250):
    sh = np.sqrt(rng.standard_normal((200000, n)).var(axis=1))
    check('l8 S9: sd of sigma-hat about sigma/sqrt(2n) for normal returns, n = %d' % n, close(sh.std(), 1 / math.sqrt(2 * n), 0.04 / math.sqrt(2 * n) + 0.012 * (n == 5)), (round(sh.std(), 4), round(1 / math.sqrt(2 * n), 4)))
# the same rule on fat-tailed returns (Student t, 5 degrees of freedom, scaled to sd 1): evidence for finding 3
t5 = rng.standard_t(5, (200000, 504)) / math.sqrt(5 / 3)
sh = np.sqrt(t5.var(axis=1))
note('SE(sigma-hat) = sigma/sqrt(2n) needs normal returns', 'n = 504, t(5) returns: sd of sigma-hat %.4f against the rule %.4f, a factor %.2f' % (sh.std(), 1 / math.sqrt(1008), sh.std() * math.sqrt(1008)))
# l8 S6 "avoids a noisy mean" and quiz q-zero-mean "estimating the mean would add more noise than it removes"
xm = 0.04 + rng.standard_normal((400000, 20))
z0 = np.sqrt((xm ** 2).mean(axis=1)); z1 = np.sqrt(xm.var(axis=1)); z2 = np.sqrt(xm.var(axis=1, ddof=1))
note('l8 zero-mean against mean-estimated sd, n = 20, mu = 0.04, sigma = 1', 'sd of estimate: zero-mean %.4f, MLE with mean %.4f, s %.4f; RMSE: %.4f, %.4f, %.4f; sd as a share of own mean: %.4f, %.4f, %.4f' % (z0.std(), z1.std(), z2.std(), math.sqrt(((z0 - 1) ** 2).mean()), math.sqrt(((z1 - 1) ** 2).mean()), math.sqrt(((z2 - 1) ** 2).mean()), z0.std() / z0.mean(), z1.std() / z1.mean(), z2.std() / z2.mean()))
check('l8 quiz q-zero-mean: per unit of its own level the zero-mean estimate is the steadier one (cv 1/sqrt(2n) against 1/sqrt(2(n-1)))', z0.std() / z0.mean() < z1.std() / z1.mean())

# ---------------------------------------------------------------- L9: standard errors
check('l9 S0: within 0.1% about 95% (n = 400) and 38% (n = 25)', close(2 * stats.norm.cdf(2) - 1, 0.95, 0.005) and close(2 * stats.norm.cdf(0.5) - 1, 0.38, 0.005))
p_gt = stats.binom.sf(55, 100, 0.5); p_ge = stats.binom.sf(54, 100, 0.5)
note('l9 S10 "a coin-flipper beats 55% about 16% of the time"', 'exact binomial: more than 55 wins %.4f, 55 or more %.4f; the 16%% is the normal tail beyond one SE (%.4f) with no continuity correction' % (p_gt, p_ge, stats.norm.sf(0.05 / 0.0497)))
check('l9 S10: 0.05/0.0497 = 1.0 SE; poll of 1,000: 2 SE about 3 points', close(0.05 / math.sqrt(0.55 * 0.45 / 100), 1.0, 0.01) and close(2 * math.sqrt(0.52 * 0.48 / 1000), 0.03, 0.002))

# ---------------------------------------------------------------- L10: confidence intervals
l10 = load('l10-catching-the-truth')
cap = l10['screens'][2]['canvas']['derive']['caption']
import re
devs = [float(v) for v in re.findall(r'\(([0-9.]+) > z \* 0\.1\)', cap)]
cnt = lambda z: sum(d > z * 0.1 for d in devs)
check('l10 S2-S4: 100 intervals; 5 miss at 1.96, 10 at 1.645, 1 at 2.576, 0 at 3', len(devs) == 100 and (cnt(1.96), cnt(1.645), cnt(2.576), cnt(3)) == (5, 10, 1, 0), (len(devs), cnt(1.96), cnt(1.645), cnt(2.576), cnt(3)))
check('l10 S0 slips / S4 / S7: 68%, 90%, 95.45%, 99%; P(|Z|>3) = 0.0027; P(|Z|>3.92) about 0.0001; z = 0.98 gives 67%', close(2 * stats.norm.cdf(1) - 1, 0.68, 0.005) and close(2 * stats.norm.cdf(1.645) - 1, 0.90, 5e-4) and close(2 * stats.norm.cdf(2) - 1, 0.9545, 5e-5) and close(2 * stats.norm.cdf(2.576) - 1, 0.99, 5e-4) and close(2 * stats.norm.sf(3), 0.0027, 5e-5) and close(2 * stats.norm.sf(3.92), 0.0001, 2e-5) and close(2 * stats.norm.cdf(0.98) - 1, 0.67, 0.005))
# known-sigma z interval, normal days: coverage 95% (MC), the claim of S2
xb = 0.05 + 0.1 * rng.standard_normal(4000000)
cov = (np.abs(xb - 0.05) <= 1.96 * 0.1).mean()
check('l10 S2: known-sigma interval covers 95% for normal data (MC, 4e6)', close(cov, 0.95, 5e-4), round(cov, 5))
# the same interval on skewed days (shifted exponential, sd 1), n = 100: "exactly 5%" is then only approximate
e = rng.exponential(1.0, (400000, 100)).mean(axis=1) - 1.0
miss = (np.abs(e) > 1.96 * 0.1).mean(); lo = (e < -1.96 * 0.1).mean(); hi = (e > 1.96 * 0.1).mean()
note('l10 S2/S3 "converges to exactly 5%"', 'days with a skewed law (exponential, sd 1), n = 100, sigma known: miss share %.4f (%.4f below, %.4f above); exact only when the mean is exactly normal' % (miss, lo, hi))
x10 = rng.standard_normal((1000000, 10))
tt = x10.mean(axis=1) / (x10.std(axis=1, ddof=1) / math.sqrt(10))
c196 = (np.abs(tt) <= 1.96).mean(); c2262 = (np.abs(tt) <= 2.262).mean()
check('l10 S5 / hw3 h-small-t: normal data, n = 10: +/-1.96 s/sqrt(n) covers 0.918 and 2.262 covers 0.95 (MC and t9)', close(c196, 0.918, 0.0015) and close(c2262, 0.95, 0.001) and close(stats.t.cdf(1.96, 9) * 2 - 1, 0.918, 5e-4) and close(stats.t.ppf(0.975, 9), 2.262, 5e-4) and close(stats.t.ppf(0.975, 10), 2.228, 5e-4), (round(c196, 4), round(c2262, 4)))
ln = rng.lognormal(0, 1, (1000000, 10)); mu_ln = math.exp(0.5)
tl = (ln.mean(axis=1) - mu_ln) / (ln.std(axis=1, ddof=1) / math.sqrt(10))
e10 = rng.exponential(1.0, (1000000, 10))
te = (e10.mean(axis=1) - 1) / (e10.std(axis=1, ddof=1) / math.sqrt(10))
note('l10 S5 / hw3 h-small-t "follows a t distribution with 9 degrees of freedom"', 'needs normal data: with 2.262 at n = 10 the cover is %.3f for exponential days and %.3f for lognormal days, against 0.950 for normal days' % ((np.abs(te) <= 2.262).mean(), (np.abs(tl) <= 2.262).mean()))
for n in (16, 25, 64):
    xs = rng.standard_normal((600000, n))
    tz = xs.mean(axis=1) / (xs.std(axis=1, ddof=1) / math.sqrt(n))
    note('fluency-l10 half-width-from-s keys z with s at n = %d' % n, 'normal data: 1.645 / 1.96 / 2.576 cover %.3f / %.3f / %.3f (t values %.3f / %.3f / %.3f)' % ((np.abs(tz) <= 1.645).mean(), (np.abs(tz) <= 1.96).mean(), (np.abs(tz) <= 2.576).mean(), stats.t.ppf(0.95, n - 1), stats.t.ppf(0.975, n - 1), stats.t.ppf(0.995, n - 1)))
check('fluency-l10: z with s at n = 16 does not give the stated level (93.1% and 97.9% for "95%" and "99%")', close(2 * stats.t.cdf(1.96, 15) - 1, 0.931, 1e-3) and close(2 * stats.t.cdf(2.576, 15) - 1, 0.979, 1e-3))
check('l10 S9 / S10 / quiz: 0.08 +/- 0.149; vol half-width 0.988 (no-two 1.397); hit rate 0.5012; 99% upper 0.2488', close(1.96 * 1.2 / math.sqrt(250), 0.149, 5e-4) and close(1.96 * 16 / math.sqrt(1008), 0.988, 5e-4) and close(1.96 * 16 / math.sqrt(504), 1.397, 5e-4) and close(0.55 - 1.96 * math.sqrt(0.2475 / 400), 0.5012, 5e-5) and close(0.12 + 2.576 * 0.05, 0.2488, 1e-9))
# S6 option "95% of future 100-day means will lie in this interval" is false: average capture is about 83%
c0 = 0.1 * rng.standard_normal(1000000); c1 = 0.1 * rng.standard_normal(1000000)
cap_ = (np.abs(c1 - c0) <= 1.96 * 0.1).mean()
check('l10 S6 wrong option: a 95% interval holds a future sample mean only about 83% of the time', close(cap_, 0.834, 0.002), round(cap_, 4))
k40 = (np.abs(rng.standard_normal((200000, 40))) > 1.96).sum(axis=1)
check('l10 quiz q-forty: 40 null intervals, 2 exclude zero on average', close(k40.mean(), 2.0, 0.02), round(k40.mean(), 3))

# ---------------------------------------------------------------- L11: bootstrap
ret = [-0.1, 1.3, 1.5, -0.7, -0.8, 0.8, -0.4, -2.7, -0.8, -0.2, 1.4, 0.5, 1.1, -0.1, 0.3, 1.0, 0.8, -0.3, 0.5, -0.1]
check('l11: 20 returns have mean 0.15, s about 1.0; bootstrap sd of the mean 0.217; formula half-width 0.44', close(np.mean(ret), 0.15, 1e-9) and close(np.std(ret, ddof=1), 1.0, 0.05) and close(np.std(ret) / math.sqrt(20), 0.217, 5e-4) and close(1.96 * np.std(ret, ddof=1) / math.sqrt(20), 0.44, 0.005), (np.std(ret, ddof=1), np.std(ret) / math.sqrt(20)))


def bootstrap_ci(data, B, seed, draw='choices', stat=None):
    random.seed(seed); n = len(data); vals = []
    for _ in range(B):
        if draw == 'choices': rs = random.choices(data, k=n)
        elif draw == 'choice': rs = [random.choice(data) for _ in range(n)]
        elif draw == 'randrange': rs = [data[random.randrange(n)] for _ in range(n)]
        elif draw == 'randint': rs = [data[random.randint(0, n - 1)] for _ in range(n)]
        vals.append(stat(rs) if stat else sum(rs) / n)
    vals.sort(); kk = int(0.025 * B)
    return vals[kk], vals[B - 1 - kk]


ci = bootstrap_ci(ret, 1000, 1)
check('l11 S3/S4: seed 1, B = 1000 gives -0.29 to 0.555 (CPython random.choices; same generator as Pyodide)', [round(v, 3) for v in ci] == [-0.29, 0.555], ci)
ci4 = bootstrap_ci(ret, 4000, 1)
check('l11 S4 explain: B = 4000 gives -0.305 to 0.55', [round(v, 3) for v in ci4] == [-0.305, 0.55], ci4)
tab = [(200, 1, -0.235, 0.49), (200, 2, -0.23, 0.55), (10000, 1, -0.30, 0.56), (10000, 2, -0.305, 0.555)]
got = [[round(v, 3) for v in bootstrap_ci(ret, B_, s_)] for B_, s_, _, _ in tab]
check('l11 S5 table: four runs reproduce', all(close(g[0], t[2], 1e-9) and close(g[1], t[3], 1e-9) for g, t in zip(got, tab)), got)


def l11_tests(draw):
    f = lambda d, B_, s_: bootstrap_ci(d, B_, s_, draw)
    t = [list(f([0.4] * 10, 100, 1)) == [0.4, 0.4] or all(math.isclose(v, 0.4) for v in f([0.4] * 10, 100, 1)),
         f(ret, 500, 3)[1] - f(ret, 500, 3)[0] > 0.5,
         abs(f(ret, 4000, 1)[0] + 0.30) < 0.05, abs(f(ret, 4000, 1)[1] - 0.55) < 0.05,
         f(ret, 300, 7) == f(ret, 300, 7), list(f([0, 0, 0, 0, 10], 2000, 5)) == [0.0, 6.0],
         (lambda c: abs(c[0] + 0.39) < 0.06 and abs(c[1] - 0.92) < 0.06)(f([2.0, -1.0, 0.5, 0.1, -0.4, 1.2, 0.3, -0.8], 3000, 9))]
    return t


alt = {d: l11_tests(d) for d in ('choices', 'choice', 'randrange', 'randint')}
check('l11 S4 "another correct way of drawing ... still passes": random.choice, randrange and randint codings pass all 7 tests', all(all(v) for v in alt.values()), {d: [int(q) for q in v] for d, v in alt.items()})
# how robust is that, away from the fixed seeds? long-run ends and the spread of one run's ends
big = np.array(ret)[rng.integers(0, 20, (400000, 20))].mean(axis=1)
lo_inf, hi_inf = np.quantile(big, [0.025, 0.975])
ends = np.array([np.quantile(np.array(ret)[rng.integers(0, 20, (4000, 20))].mean(axis=1), [0.025, 0.975]) for _ in range(400)])
note('l11 S4 tests 3 and 4 (B = 4000, tolerance 0.05 around -0.30 and 0.55)', 'long-run ends %.3f and %.3f; one run of B = 4000 has end sd %.3f and %.3f; share of fresh correct runs inside both tolerances %.3f' % (lo_inf, hi_inf, ends[:, 0].std(), ends[:, 1].std(), ((np.abs(ends[:, 0] + 0.30) < 0.05) & (np.abs(ends[:, 1] - 0.55) < 0.05)).mean()))
check('l11 S9: 35 distinct resamples of 4 values; 63% of resamples of 250 contain the maximum; 64% of 20', math.comb(7, 4) == 35 and close(1 - (1 - 1 / 250) ** 250, 0.63, 0.005) and close(1 - 0.95 ** 20, 0.64, 0.005))
# single-day bootstrap on positively autocorrelated returns understates the spread of the mean
phi, n = 0.6, 60
eps = rng.standard_normal((20000, n + 50)); ar = np.zeros_like(eps)
for t_ in range(1, n + 50):
    ar[:, t_] = phi * ar[:, t_ - 1] + eps[:, t_]
ar = ar[:, 50:]
true_sd = ar.mean(axis=1).std(); iid_sd = (ar.std(axis=1) / math.sqrt(n)).mean()
blk = []
for row in ar[:1500]:
    starts = rng.integers(0, n - 10 + 1, (200, 6))
    idx = (starts[:, :, None] + np.arange(10)[None, None, :]).reshape(200, 60)
    blk.append(row[idx].mean(axis=1).std())
check('l11 S9/S11: with lag-1 correlation 0.6, single-day resampling understates the sd of the mean; 10-day blocks come much closer', iid_sd < 0.6 * true_sd and abs(np.mean(blk) - true_sd) < abs(iid_sd - true_sd) / 2, (round(true_sd, 3), round(iid_sd, 3), round(float(np.mean(blk)), 3)))
# percentile bootstrap coverage at n = 20 (no claim in the lesson beyond "close to the formula's"; recorded)
hit = 0; reps = 4000
for _ in range(reps):
    d = rng.standard_normal(20)
    bm = d[rng.integers(0, 20, (1000, 20))].mean(axis=1)
    l_, h_ = np.quantile(bm, [0.025, 0.975]); hit += l_ <= 0 <= h_
note('l11 percentile interval for a mean, n = 20, normal data', 'covers %.3f of the time (nominal 0.95); the lesson makes no coverage claim' % (hit / reps))
# problems-3 p-three-month-fund: exact bootstrap SE by listing the 27 resamples
m27 = [np.mean(t) for t in itertools.product([2, 4, 9], repeat=3)]
check('problems-3: bootstrap SE sqrt(26/9) = 1.70, s/sqrt(n) = 2.08, ratio sqrt(2/3)', close(np.std(m27), math.sqrt(26 / 9), 1e-12) and close(math.sqrt(13 / 3), 2.0817, 5e-5) and close(np.std(m27) / math.sqrt(13 / 3), math.sqrt(2 / 3), 1e-12))

# homework-3 bootstrap code: example and the tolerance tests under other correct ways of drawing
hw3 = load('homework-3')
items = hw3.get('items') or hw3.get('problems')
hb = [i for i in items if i['id'] == 'h-bootstrap-code'][0]
ns = {}
exec(hb['widget']['prelude'], ns)
daily, sharpe = ns['daily'], ns['sharpe']
e1 = bootstrap_ci(daily, 1000, 1, 'choices', sharpe)
check('hw3 h-bootstrap-code example: Sharpe interval -1.1 to 2.896 (seed 1, B = 1000); l11 S10 states -1.10 to 2.90', [round(v, 3) for v in e1] == [-1.1, 2.896], e1)
med = bootstrap_ci(ret, 2000, 4, 'choices', statistics.median)
check('hw3 explain: median interval -0.25 to 0.80 (seed 4, B = 2000)', close(med[0], -0.25, 1e-9) and close(med[1], 0.80, 1e-9), med)
dn = np.array(daily)
def np_sharpe(mat):
    return mat.mean(axis=1) / mat.std(axis=1, ddof=1) * math.sqrt(252)
bigs = np.concatenate([np_sharpe(dn[rng.integers(0, 250, (20000, 250))]) for _ in range(10)])
slo, shi = np.quantile(bigs, [0.025, 0.975])
runs = np.array([np.quantile(np_sharpe(dn[rng.integers(0, 250, (1000, 250))]), [0.025, 0.975]) for _ in range(600)])
pass3 = ((np.abs(runs[:, 0] + 1.10) < 0.15) & (np.abs(runs[:, 1] - 2.90) < 0.15)).mean()
alt3 = {d: (lambda c: abs(c[0] + 1.10) < 0.15 and abs(c[1] - 2.90) < 0.15)(bootstrap_ci(daily, 1000, 1, d, sharpe)) for d in ('choice', 'randrange', 'randint')}
note('hw3 h-bootstrap-code test 4 (Sharpe ends within 0.15 of -1.10 and 2.90, B = 1000)', 'long-run ends %.3f and %.3f; one run of B = 1000 has end sd %.3f and %.3f; share of fresh correct runs that pass %.3f; fixed-seed alternatives %s' % (slo, shi, runs[:, 0].std(), runs[:, 1].std(), pass3, alt3))
check('hw3 h-bootstrap-code test 4 accepts other correct ways of drawing (random.choice, randrange, randint at seed 1)', all(alt3.values()), alt3)
check('hw3 h-bootstrap-code "within 0.1 to 0.15 of their long-run ends": a correct program with its own draws passes test 4 at least 95% of the time', pass3 >= 0.95, round(float(pass3), 3))

# ---------------------------------------------------------------- L12: beta posteriors
q = lambda a_, b_: tuple(round(v, 3) for v in stats.beta.ppf([0.025, 0.975], a_, b_))
check('l12: central 95% of Beta(9,5) 0.386-0.861, Beta(160,140) 0.477-0.589, Beta(22,18) 0.396-0.699, Beta(50,40) 0.453-0.656', q(9, 5) == (0.386, 0.861) and q(160, 140) == (0.477, 0.589) and q(22, 18) == (0.396, 0.699) and q(50, 40) == (0.453, 0.656), (q(9, 5), q(160, 140), q(22, 18), q(50, 40)))
check('l12 S1: 6 heads in 6 gives 0.8; 70 in 100 gives 0.692; Beta(2,2) density 6p(1-p)', close(8 / 10, 0.8, 1e-12) and close(72 / 104, 0.692, 5e-4) and close(stats.beta.pdf(0.3, 2, 2), 6 * 0.3 * 0.7, 1e-12))
# conjugate update by simulation: p ~ Beta(2,2), 10 flips, condition on 7 heads
pp = rng.beta(2, 2, 3000000); kk = rng.binomial(10, pp); sel = pp[kk == 7]
check('l12 S2/S3: simulated posterior after 7 heads in 10 from Beta(2,2) has mean 9/14 and the Beta(9,5) quantiles', close(sel.mean(), 9 / 14, 0.002) and close(np.quantile(sel, 0.025), 0.386, 0.004) and close(np.quantile(sel, 0.975), 0.861, 0.004), (round(sel.mean(), 4), len(sel)))
check('l12 summary trap "a dogmatic prior such as Beta(100,100) ignores the data": the posterior mean does not move', close(160 / 300, 0.5, 1e-9), 'posterior mean 160/300 = %.3f, moved from 0.5; S6 feedback itself says the data do move the analyst' % (160 / 300))
# S8: flat prior and many flips, credible and confidence intervals nearly coincide
kq, nq = 5400, 10000
cr = stats.beta.ppf([0.025, 0.975], 1 + kq, 1 + nq - kq); ph = kq / nq; wald = (ph - 1.96 * math.sqrt(ph * (1 - ph) / nq), ph + 1.96 * math.sqrt(ph * (1 - ph) / nq))
check('l12 S8: flat prior, 10,000 flips: credible and confidence ends agree to 0.001', max(abs(cr[0] - wald[0]), abs(cr[1] - wald[1])) < 1e-3)

# ---------------------------------------------------------------- homework 2 and 3, problems
check('hw2: normal ratio e^0.375 = 1.455 (no-half 2.117); log score -6.3903 and -6.1086; vol 0.9055, 14.375, n-1 0.992', close(math.exp(0.375), 1.455, 5e-4) and close(math.exp(0.75), 2.117, 5e-4) and close(7 * math.log(0.8) + 3 * math.log(0.2), -6.3903, 5e-5) and close(7 * math.log(0.7) + 3 * math.log(0.3), -6.1086, 5e-5) and close(math.sqrt(4.92 / 6), 0.9055, 5e-5) and close(math.sqrt(4.92 / 6) * math.sqrt(252), 14.375, 1e-3) and close(math.sqrt(4.92 / 5), 0.992, 5e-4))
check('hw2 code tests: 5000 densities of 24.2 give 15931.158; three-return test 13.4067', close(ll([0.01] * 5000, 0.0, 0.01), 15931.158263917092, 1e-6) and close(ll([0.002, -0.004, 0.001], 0.0005, 0.003), 13.406724482439174, 1e-9) and close(stats.norm.pdf(0.01, 0, 0.01), 24.2, 0.05))
losses = [1.5, 1.2, 3.0, 1.1, 2.4, 1.8]; S = sum(math.log(v) for v in losses)
check('hw2 Pareto: S = 3.2450, alpha-hat 1.85, unbiased 1.54, tail chances 0.014 and 0.029', close(S, 3.2450, 5e-5) and close(6 / S, 1.85, 5e-3) and close(5 / S, 1.54, 5e-3) and close(10 ** (-6 / S), 0.014, 5e-4) and close(10 ** (-5 / S), 0.029, 5e-4))
al = 1.5; xs = (1 - rng.random((1000000, 6))) ** (-1 / al)
ah = 6 / np.log(xs).sum(axis=1)
check('hw2 Pareto MC: E[alpha-hat] = n alpha/(n-1) at n = 6 (20% high); (n-1)/n alpha-hat unbiased', close(ah.mean(), 1.2 * al, 0.004) and close((5 / 6 * ah).mean(), al, 0.004), round(ah.mean(), 4))
# hw3 Wald interval for 30 wins in 50: "95% of intervals built this way contain the true p"
def wald_cover(n, p):
    ks = np.arange(n + 1); ph_ = ks / n; hw = 1.96 * np.sqrt(ph_ * (1 - ph_) / n)
    return stats.binom.pmf(ks, n, p)[(ph_ - hw <= p) & (p <= ph_ + hw)].sum()
note('hw3 h-long-trader (b) "95% of intervals built this way contain the true p"', 'exact cover of p-hat +/- 1.96 SE at n = 50: p = 0.6 %.3f, p = 0.55 %.3f, p = 0.5 %.3f, p = 0.7 %.3f' % (wald_cover(50, 0.6), wald_cover(50, 0.55), wald_cover(50, 0.5), wald_cover(50, 0.7)))
check('hw3 h-long-trader: SE 0.0693, interval 0.464-0.736, posterior sd 0.0521, 0.453-0.658', close(math.sqrt(0.0048), 0.0693, 5e-5) and close(0.6 - 1.96 * math.sqrt(0.0048), 0.464, 5e-4) and close(math.sqrt(2000 / (8100 * 91)), 0.0521, 5e-5) and close(50 / 90 - 1.96 * 0.0521, 0.453, 6e-4) and close(50 / 90 + 1.96 * 0.0521, 0.658, 6e-4))
check('hw3 h-sample-size: 2376.99 rounds up to 2377; slips 2475 and 2401', math.ceil(1.96 ** 2 * 0.2475 / 0.02 ** 2) == 2377 and close(4 * 0.2475 / 0.0004, 2475, 1e-6) and close(1.96 ** 2 * 0.25 / 0.0004, 2401, 1e-6))
def bump_interval(delays, level):
    n_ = len(delays); m_ = max(delays); a__ = 1 - level
    return m_ / (1 - a__ / 2) ** (1 / n_), m_ / (a__ / 2) ** (1 / n_)
def bump_coverage(theta, n_, level, trials, seed):
    g = random.Random(seed); hits = 0
    for _ in range(trials):
        lo_, hi_ = bump_interval([theta * g.random() for _ in range(n_)], level)
        hits += lo_ <= theta <= hi_
    return hits / trials
check('hw3 h-bump-interval tests: 30.254-102.599, 4.103-160, coverage replays 0.947 and 0.90267', np.allclose(bump_interval([12.0, 30.0, 21.0], 0.95), [30.254249410473346, 102.59855680060177]) and np.allclose(bump_interval([4.0], 0.95), [4.102564102564103, 159.99999999999986]) and bump_coverage(10.0, 5, 0.95, 2000, 1) == 0.947 and math.isclose(bump_coverage(250.0, 20, 0.9, 1500, 11), 0.9026666666666666), (bump_coverage(10.0, 5, 0.95, 2000, 1), bump_coverage(250.0, 20, 0.9, 1500, 11)))
for n_, lev in ((1, 0.5), (3, 0.95), (20, 0.9)):
    mx = rng.random((2000000, n_)).max(axis=1); a__ = 1 - lev
    cv = ((mx / (1 - a__ / 2) ** (1 / n_) <= 1) & (1 <= mx / (a__ / 2) ** (1 / n_))).mean()
    check('hw3 h-bump-interval: interval from the maximum covers exactly the level, n = %d, level %.2f (MC 2e6)' % (n_, lev), close(cv, lev, 0.0012), round(cv, 4))
# hw3 h-bump-interval: which hidden test does each named mistake fail first? (page order; the page shows the line of the FIRST failing test)
def bump_first_fail(interval, coverage=None):
    def cov(theta, n_, level, trials, seed):
        g = random.Random(seed); hits = 0
        for _ in range(trials):
            lo_, hi_ = interval([theta * g.random() for _ in range(n_)], level); hits += lo_ <= theta <= hi_
        return hits / trials
    cov = coverage(interval) if coverage else cov
    d50 = [(7 * k_) % 50 + 0.5 for k_ in range(50)]
    same = lambda got, want: all(math.isclose(a_, b_) for a_, b_ in zip(got, want))
    tests = [lambda: same(interval([12.0, 30.0, 21.0], 0.95), [30.254249410473346, 102.59855680060177]),
             lambda: same(interval([4.0], 0.95), [4.102564102564103, 159.99999999999986]),
             lambda: same(interval([3.1, 0.4, 2.2, 4.9, 1.7], 0.9), [4.950526150657887, 8.920764594827794]),
             lambda: same(interval(d50, 0.99), [49.50496266515682, 55.03333083744145]),
             lambda: same(interval([30.0, 21.0, 12.0], 0.95), [30.254249410473346, 102.59855680060177]),
             lambda: math.isclose(cov(10.0, 5, 0.95, 2000, 1), 0.947),
             lambda: abs(cov(3.0, 2, 0.8, 5000, 7) - 0.8) < 0.02,
             lambda: abs(cov(1.0, 1, 0.5, 4000, 3) - 0.5) < 0.03,
             lambda: math.isclose(cov(250.0, 20, 0.9, 1500, 11), 0.9026666666666666)]
    for i_, t_ in enumerate(tests, 1):
        try:
            if not t_(): return i_
        except Exception:
            return i_
    return 0
def mk(pick=max, alpha=lambda lv: 1 - lv):
    def f(delays, level):
        n_ = len(delays); m_ = pick(delays); a__ = alpha(level)
        return m_ / (1 - a__ / 2) ** (1 / n_), m_ / (a__ / 2) ** (1 / n_)
    return f
def normal_approx(delays, level):
    z_ = stats.norm.ppf(1 - (1 - level) / 2); m_ = max(delays); s_ = statistics.pstdev(delays)
    return m_ - z_ * s_ / len(delays) ** 0.5, m_ + z_ * s_ / len(delays) ** 0.5
def count_cov(interval):
    def cov(theta, n_, level, trials, seed):
        g = random.Random(seed); hits = 0
        for _ in range(trials):
            lo_, hi_ = interval([theta * g.random() for _ in range(n_)], level); hits += lo_ <= theta <= hi_
        return hits
    return cov
order = {'solution': bump_first_fail(mk()), 'normal approximation (test-2 line)': bump_first_fail(normal_approx),
         'last delay (test-5 line)': bump_first_fail(mk(pick=lambda d_: d_[-1])), 'first delay (test-5 line)': bump_first_fail(mk(pick=lambda d_: d_[0])),
         'whole 1 - level off each end (test-8 line)': bump_first_fail(mk(alpha=lambda lv: 2 * (1 - lv))), 'count, not share (test-8 line)': bump_first_fail(mk(), count_cov)}
check('hw3 h-bump-interval: the solution passes all nine tests', order['solution'] == 0)
note('hw3 h-bump-interval feedback routing (first failing test of each named mistake; same result under the page Pyodide)', order)
check('problems-1: ping 310, 110, 4.69, 28; route 2.8125 and 2.598; labs 8/9 and 4/9; mass 76 and 0.513', close(math.sqrt(110 / 5), 4.6904, 5e-5) and math.ceil(110 / 4) == 28 and close(0.25 * 2.25 + 2.25, 2.8125, 1e-12) and close(math.sqrt(6.75), 2.5981, 5e-5) and close(0.5 * (8 / 9) ** 2 + 4 / 81, 4 / 9, 1e-12) and close(2 / math.sqrt(76 / 5), 0.513, 5e-4))
wv = np.linspace(0, 1, 100001)
check('problems-1 labs: numeric minimum of 0.5w^2 + 4(1-w)^2 is at 8/9', close(wv[np.argmin(0.5 * wv ** 2 + 4 * (1 - wv) ** 2)], 8 / 9, 1e-4))
la = 2.0 + 6 * rng.standard_normal((400000, 9)); lb = 2.5 + 3 * rng.standard_normal((400000, 36))
bl = 8 / 9 * lb.mean(axis=1) + 1 / 9 * la.mean(axis=1)
check('problems-1 labs MC: MSE(A) = 4, MSE(B) = 0.5, blend 4/9', close(((la.mean(axis=1) - 2) ** 2).mean(), 4, 0.04) and close(((lb.mean(axis=1) - 2) ** 2).mean(), 0.5, 0.006) and close(((bl - 2) ** 2).mean(), 4 / 9, 0.006), round(((bl - 2) ** 2).mean(), 4))
check('problems-2: robot ratio 3.028; tank e^1.125 = 3.08 and 55.29; FX 1.0874, 7.84, 1.96, 123; waits 5/28 and 0.1677', close((0.75 / 0.9) ** 9 * 2.5 ** 3, 3.0282, 5e-5) and close(math.exp(1.125), 3.0802, 5e-5) and close(51 + math.sqrt(8 * math.log(10)), 55.2919, 5e-5) and close(math.sqrt(9.46 / 8), 1.0874, 5e-5) and close(math.sqrt(9.46 / 8) * math.sqrt(52), 7.8414, 5e-4) and math.ceil((7.84 / 0.5) ** 2 / 2) == 123 and close(math.exp(-50 / 28), 0.16768, 5e-6))
# censored exponential: the MLE 5/28 maximises the censored log-likelihood; treating the censored wait as complete is biased up
lam = np.linspace(0.01, 1, 99001)
check('problems-2 waits: numeric maximiser of 5 ln(lambda) - 28 lambda is 5/28', close(lam[np.argmax(5 * np.log(lam) - 28 * lam)], 5 / 28, 1e-4))
true_l = 0.2; w = rng.exponential(1 / true_l, (300000, 200)); cens = np.minimum(w, 8.0); dnum = (w <= 8.0).sum(axis=1)
mle_c = dnum / cens.sum(axis=1); naive = 200 / cens.sum(axis=1)
check('problems-2 waits MC: events over total time recovers the rate; counting censored waits as complete overstates it', close(mle_c.mean(), true_l, 0.002) and naive.mean() > true_l * 1.15, (round(mle_c.mean(), 4), round(naive.mean(), 4)))
check('problems-3: SE 0.014967, lower 0.1307; ticket bot 580 and 0.5255; routing 0.461 and -0.1035', close(math.sqrt(0.16 * 0.84 / 600), 0.014967, 5e-7) and close(0.16 - 1.96 * 0.014967, 0.1307, 5e-5) and close(0.01 / math.sqrt(0.21 / 580), 0.5255, 5e-5) and close(math.sqrt(0.09 + 0.1225), 0.461, 5e-4) and close(0.8 - 1.96 * math.sqrt(0.2125), -0.1035, 5e-5))

print()
print('%d check(s) failed: %s' % (len(fails), '; '.join(fails)) if fails else 'all checks passed')
sys.exit(1 if fails else 0)
