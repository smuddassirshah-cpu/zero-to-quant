#!/usr/bin/env python3
"""Concept checks for random-vars levels 4 and 5 (audit round 1, blind).

Exact enumeration where possible, Monte Carlo where the claim is empirical.
Exits 0 when every check passes. A check tied to a content sentence fails
while that sentence is still in the content and is false; it passes once the
sentence is corrected (see docs/reviews/audit-random-vars-4-5.md).
Standard library only.
"""
import json, math, os, random, statistics, sys
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, log, exp, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'random-vars')
fails = []
n_checks = 0


def load(name):
    with open(os.path.join(CDIR, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def raw(name):
    with open(os.path.join(CDIR, name + '.json'), encoding='utf-8') as fh:
        return fh.read()


def check(label, ok, detail=''):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(label + (' :: ' + str(detail) if detail else ''))
        print('FAIL', label, detail)


def close(a, b, tol):
    return abs(a - b) <= tol


def claim_absent_or_true(label, name, sentence, truth, detail=''):
    """A content sentence must be true, or gone."""
    present = sentence in raw(name)
    check(label, truth or not present, detail)


# ---------------------------------------------------------------- level 4
# l13 market / stock table
T13 = [[.12, .06, .02], [.10, .30, .10], [.03, .09, .18]]
rows = [sum(r) for r in T13]
cols = [sum(T13[i][j] for i in range(3)) for j in range(3)]
check('l13 margins', all(close(a, b, 1e-9) for a, b in zip(rows + cols, [.2, .5, .3, .25, .45, .30])))
check('l13 cond row1', close(T13[0][0] / rows[0], .6, 1e-9) and close(T13[0][0] / cols[0], .48, 1e-9))
check('l13 trap cols sum 0.92', close(sum(T13[2][j] / cols[j] for j in range(3)), .92, 1e-9))
check('l13 signal', close(.12 / .52, 3 / 13, 1e-12))

# l14 desks, pools, Y = X^2, vol regime
AB = [[.06, .08, .06], [.15, .20, .15], [.09, .12, .09]]
CD = [[.08, .06, .06], [.13, .22, .15], [.09, .12, .09]]


def margins(t):
    return [sum(r) for r in t], [sum(t[i][j] for i in range(len(t))) for j in range(len(t[0]))]


def mism(t):
    r, c = margins(t)
    return [(i, j) for i in range(len(t)) for j in range(len(t[0])) if abs(t[i][j] - r[i] * c[j]) > 1e-9]


check('l14 AB independent', mism(AB) == [])
check('l14 CD same margins', all(close(a, b, 1e-9) for a, b in zip(sum(margins(CD), []), sum(margins(AB), []))))
check('l14 CD four cells', mism(CD) == [(0, 0), (0, 1), (1, 0), (1, 1)])
exy = sum(i * j * AB[i][j] for i in range(3) for j in range(3))
check('l14 E[XY]=1.1', close(exy, 1.1, 1e-9))
POOL = [[.30, .15, .05], [.18, .11, .01], [.12, .04, .04]]
check('l14 pools four cells', mism(POOL) == [(1, 1), (1, 2), (2, 1), (2, 2)])
pr, pc = margins(POOL)
p_y2_x1 = POOL[1][2] / pr[1]
p_y2_xge1 = (POOL[1][2] + POOL[2][2]) / (pr[1] + pr[2])
p_y2_x2 = POOL[2][2] / pr[2]
check('l14 pools P(Y=2|X=2)=0.2', close(p_y2_x2, .2, 1e-9))
# Content sentence: "A default in one pool makes two in the other likelier".
# True only for two defaults: one default lowers it, at least one leaves it at 0.10.
claim_absent_or_true('l14 s5 "a default ... makes two likelier"', 'l14-independent-rvs',
                     'A default in one pool makes two in the other likelier',
                     p_y2_x1 > pc[2] + 1e-9 and p_y2_xge1 > pc[2] + 1e-9,
                     'P(Y=2|X=1)=%.4f, P(Y=2|X>=1)=%.4f, P(Y=2)=%.2f' % (p_y2_x1, p_y2_xge1, pc[2]))
# zero covariance, dependent
xs = [-1, 0, 1]
check('l14 Y=X^2 cov 0', sum(F(x ** 3, 3) for x in xs) - sum(F(x, 3) for x in xs) * F(2, 3) == 0)
# In a 2 x 2 table one matching cell forces all four (so "one matching cell proves nothing" needs "larger than 2 x 2")
ok22 = True
rng = random.Random(5)
for _ in range(2000):
    a, b = rng.random(), rng.random()
    t = [[a * b, a * (1 - b)], [(1 - a) * b, (1 - a) * (1 - b)]]
    ok22 &= mism(t) == []
check('2x2: one cell = product forces independence (algebra: other cells are margins minus it)', ok22)
VOL = {(a, b): .125 for a in (-3, 3) for b in (-3, 3)}
VOL.update({(a, b): .125 for a in (-1, 1) for b in (-1, 1)})
check('l14 vol corr 0', close(sum(a * b * p for (a, b), p in VOL.items()), 0, 1e-12))
check('l14 vol P(B=3|A=3)', close(VOL[(3, 3)] / .25, .5, 1e-12))

# l15 conditional expectation
T15 = [[.10, .08, .02], [.10, .25, .15], [.03, .09, .18]]
ys = [-2, 0, 2]
r15, c15 = margins(T15)
ce = [sum(y * p for y, p in zip(ys, row)) / tot for row, tot in zip(T15, r15)]
check('l15 E[Y|X]', all(close(a, b, 1e-9) for a, b in zip(ce, [-.8, .2, 1.0])))
check('l15 E[Y]=0.24 both ways', close(sum(y * p for y, p in zip(ys, c15)), .24, 1e-9)
      and close(sum(a * b for a, b in zip(ce, r15)), .24, 1e-9))
row0 = [p / r15[1] for p in T15[1]]
mse = lambda g: sum(p * (y - g) ** 2 for y, p in zip(ys, row0))
check('l15 mse', close(mse(.2), 1.96, 1e-9) and close(mse(.24), 1.9616, 1e-9) and close(mse(0), 2.0, 1e-9))
check('l15 mean minimises mse', all(mse(.2) <= mse(g / 100) + 1e-12 for g in range(-200, 201)))
check('l15 trap cols 0.77', close(sum(y * T15[2][j] / c15[j] for j, y in enumerate(ys)), .7677, 1e-3))
check('l15 fills', 100 * .3 + 300 * .3 + 500 * .2 == 220 and close(220 / 70, 3.14, .01))

# l16 waiting times: simulation of 1/p, HH = 6, HT = 4, two sixes = 42
rng = random.Random(2026)


def wait_pattern(pat, p, rng):
    n, hist = 0, ''
    while not hist.endswith(pat):
        hist = (hist + ('H' if rng.random() < p else 'T'))[-len(pat):]
        n += 1
    return n


def mc(f, reps):
    xs = [f() for _ in range(reps)]
    m = statistics.fmean(xs)
    return m, statistics.pstdev(xs) / sqrt(reps)


for pat, p, target in (('H', .5, 2), ('H', .25, 4), ('H', 1 / 6, 6), ('HH', .5, 6), ('HT', .5, 4), ('HH', 1 / 6, 42), ('H', .2, 5)):
    m, se = mc(lambda: wait_pattern(pat, p, rng), 200000)
    check('l16 wait %s p=%.3f = %s' % (pat, p, target), abs(m - target) < 5 * se, (m, se))

# l16 code: run the taught solution, compare the printed claims
l16 = load('l16-averaging-averages')
ns = {}
exec(l16['screens'][8]['widget']['solution'], ns)
got = [round(ns['average_wait'](p, 50000, s), 5) for p, s in ((.5, 1), (1 / 6, 2), (.2, 3))]
check('l16 code seeds 1.99834 6.03976 5.03602', got == [1.99834, 6.03976, 5.03602], got)
ns2 = {}
try:
    exec(l16['screens'][8]['widget']['starter'], ns2)
    starter_ok = abs(ns2['average_wait'](.5, 50000, 1) - 2) < .05
except Exception:
    starter_ok = False
check('l16 starter fails', not starter_ok)

# ---------------------------------------------------------------- level 5
# l17 total variance
inside = .8 * 100 ** 2 + .2 * 300 ** 2
between = .8 * (120 - 60) ** 2 + .2 * (-180 - 60) ** 2
check('l17 26000 + 14400 = 40400', (inside, between) == (26000, 14400))
pts = [(.1, 120), (.1, -480), (.4, 220), (.4, 20)]  # the screen's simulated days
m = sum(p * v for p, v in pts)
check('l17 sim outcome mean 60 var 40400', close(m, 60, 1e-9) and close(sum(p * (v - m) ** 2 for p, v in pts), 40400, 1e-6))
rng = random.Random(17)
xs = [rng.gauss(-180, 300) if rng.random() < .2 else rng.gauss(120, 100) for _ in range(400000)]
check('l17 MC variance near 40400', abs(statistics.pvariance(xs) - 40400) < 800, statistics.pvariance(xs))
cv = [sum(y * y * p for y, p in zip(ys, row)) / tot - c ** 2 for row, tot, c in zip(T15, r15, ce)]
check('l17 cond variances', all(close(a, b, 1e-9) for a, b in zip(cv, [1.76, 1.96, 1.8])))
ev = sum(a * b for a, b in zip(cv, r15))
ve = sum(c * c * p for c, p in zip(ce, r15)) - .24 ** 2
check('l17 1.872 + 0.3904 = 2.2624', close(ev, 1.872, 1e-9) and close(ve, .3904, 1e-9)
      and close(ev + ve, sum(y * y * p for y, p in zip(ys, c15)) - .24 ** 2, 1e-9))
# die and coins, exact
pmf = {}
for n in range(1, 7):
    for h in range(n + 1):
        pmf[h] = pmf.get(h, 0) + F(1, 6) * comb(n, h) * F(1, 2 ** n)
mh = sum(h * p for h, p in pmf.items())
check('l17 Var(H)=77/48', sum(h * h * p for h, p in pmf.items()) - mh ** 2 == F(77, 48) and mh == F(7, 4))
# "a mixture has fatter tails than either regime": with normal regimes the far-left tail chance of the
# mixture is BELOW the volatile regime's own, though its kurtosis is above 3. The sentence needs a referent.
Phi = lambda z: .5 * (1 + math.erf(z / sqrt(2)))
tail_mix = .2 * Phi((-480 + 180) / 300) + .8 * Phi((-480 - 120) / 100)
tail_vol = Phi((-480 + 180) / 300)
m4 = .8 * (3 * 100 ** 4 + 6 * 100 ** 2 * 60 ** 2 + 60 ** 4) + .2 * (3 * 300 ** 4 + 6 * 300 ** 2 * 240 ** 2 + 240 ** 4)
check('mixture: tail chance below volatile regime, kurtosis above 3', tail_mix < tail_vol and m4 / 40400 ** 2 > 3,
      (tail_mix, tail_vol, m4 / 40400 ** 2))
# quiz q-fixed: E[Var(Y|X)] = Var(Y) needs only a flat conditional mean, not independence (vol-regime table)
eb2 = {a: sum(b * b * p for (aa, b), p in VOL.items() if aa == a) / .25 for a in (-3, -1, 1, 3)}
check('flat conditional mean without independence gives E[Var(B|A)] = Var(B)',
      close(sum(.25 * v for v in eb2.values()), sum(b * b * p for (a, b), p in VOL.items()), 1e-12))

# l18 random sums
EN, VN = 20, .4 * 25 + .4 * 25
check('l18 18000 + 500', EN * 900 + VN * 25 == 18500 and close(sqrt(18500), 136.01, .005) and close(sqrt(18000), 134.16, .005))
l18 = load('l18-random-sums')
ns = {}
exec(l18['screens'][9]['widget']['solution'], ns)
sim = ns['random_sum']([15, 20, 25], [.4, .2, .4], [35, -25], [.5, .5], 20000, 8)
check('l18 code sim variance 18466.21', sim[1] == 18466.21, sim)
check('l18 code exact', ns['random_sum_moments']([15, 20, 25], [F(2, 5), F(1, 5), F(2, 5)], [35, -25], [F(1, 2), F(1, 2)]) == (100, 18500))
check('l18 desk 23200', 24 * 900 + 64 * 25 == 23200 and close(.8 * 18000 + .2 * 36000 + .8 * .2 * 100 ** 2, 23200, 1e-6))
check('l18 insurer 13115', round(sqrt(12 * 9e6 + 16 * 4e6)) == 13115)
# "If N depends on the fills, the formulas fail": dependence does not force failure.
# (a) N = index of the first +35 fill (a stopping time): the mean formula still holds (Wald), the variance one does not.
rng = random.Random(18)
S, N = [], []
for _ in range(300000):
    n, s = 0, 0
    while True:
        n += 1
        x = 35 if rng.random() < .5 else -25
        s += x
        if x == 35:
            break
    S.append(s); N.append(n)
mS, mN, vS, vN = statistics.fmean(S), statistics.fmean(N), statistics.pvariance(S), statistics.pvariance(N)
check('Wald: dependent N, E[S] = E[N]E[X] holds', abs(mS - mN * 5) < .5 and abs(mS - 10) < .3, (mS, mN))
check('Wald case: variance formula does fail (1250 against 1850)', abs(vS - 1250) < 40 and abs(mN * 900 + vN * 25 - 1850) < 40, (vS, vN))
# (b) fills whose shape, not mean or variance, changes with N: both formulas hold exactly.
rng = random.Random(19)
S = []
for _ in range(300000):
    n = rng.choice([15, 15, 20, 25, 25])
    if n == 25:
        s = sum(5 + 30 * sqrt(2) * rng.choice([-1, 0, 0, 1]) for _ in range(n))
    else:
        s = sum(rng.choice([35, -25]) for _ in range(n))
    S.append(s)
check('dependent N and fills with unchanged conditional mean and variance: 100 and 18500 hold',
      abs(statistics.fmean(S) - 100) < 1.5 and abs(statistics.pvariance(S) - 18500) < 350,
      (statistics.fmean(S), statistics.pvariance(S)))
dependence_forces_failure = False
claim_absent_or_true('l18 summary "If N depends on the fills, the formulas fail"', 'l18-random-sums',
                     'If $N$ depends on the fills, the formulas fail.', dependence_forces_failure,
                     'Wald: mean formula holds for a stopping time; both hold when only the shape changes')
# correlated fills with N independent of them also break the variance formula ("fail only if ... linked")
claim_absent_or_true('l18 quiz q-fail "fail only if the count and the fills are linked"', 'l18-random-sums',
                     'They fail only if the count and the fills are linked.', False,
                     'fills correlated with each other: Var(S|N) is not N Var(X)')

# l19 Jensen
check('l19 logs', close(.5 * log(.99), -.00503, 5e-6) and close(.5 * (log(1.07) + log(.95)), .00818, 5e-6))
check('l19 120 months', close(exp(120 * .5 * (log(1.07) + log(.95))), 2.67, .005) and close(1.01 ** 120, 3.30, .005))
rng = random.Random(1907)
W = []
for _ in range(40000):
    k = sum(rng.random() < .5 for _ in range(120))
    W.append(1.07 ** k * .95 ** (120 - k))
med, mean = statistics.median(W), statistics.fmean(W)
check('l19 MC: median wealth near 2.67, mean wealth near 3.30', abs(med - 2.67) < .12 and abs(mean - 3.30) < .08, (med, mean))
check('l19 pound-cost 17.14', close(300 / 17.5, 17.14, .005) and 17.5 / 300 > 1 / (70 / 3))
check('l19 cube gaps', (-27 + 1) / 2 - (-1) ** 3 == -12 and (-1 + 27) / 2 - 1 ** 3 == 12)
# feedback "gap is about sigma^2 over a few times the mean": second order gap is sigma^2 / (8 mu^1.5)
mu, var = 5, 16  # X = 1 or 9
gap = sqrt(mu) - 2
check('l19 root gap second order sigma^2/(8 mu^1.5)', close(var / (8 * mu ** 1.5), .179, .001) and .15 < gap < .25)
# quiz q-var: wrong value 0.5 is described as "half the range"; half the range of {1, 3} is 1.
claim_absent_or_true('l19 quiz q-var "Half the range" for 0.5', 'l19-convex-bets',
                     'Half the range is not the variance.', (3 - 1) / 2 == .5, 'half the range is 1, and the variance is 1')
# Jensen at a kink: call payoff has no tangent at 100 yet the inequality holds (support line)
check('l19 call payoff', .5 * 0 + .5 * 20 == 10 and max(100 - 100, 0) == 0)
check('l19 Cauchy-Schwarz bound', sqrt(4 * 9) == 6)

# l20 multinomial and negative binomial
mult = lambda c, p: factorial(sum(c)) / math.prod(factorial(x) for x in c) * math.prod(q ** x for q, x in zip(p, c))
check('l20 multinomial', close(mult([5, 2, 3], [.5, .2, .3]), .08505, 1e-9) and close(mult([4, 2, 4], [.5, .2, .3]), .0637875, 1e-9)
      and close(comb(10, 5) / 1024, .2461, 5e-5) and close(mult([6, 0, 4], [.6, 0, .4]), .2508, 5e-5))
cov = sum(mult([u, 10 - u - d, d], [.5, .2, .3]) * u * d for u in range(11) for d in range(11 - u)) - 5 * 3
check('l20 cov -1.5 corr -0.65', close(cov, -1.5, 1e-9) and close(cov / sqrt(2.5 * 2.1), -.65, .005))
# feedback for 0.0313: "the chance of one particular record"
claim_absent_or_true('l20 s2 0.0313 "one particular record"', 'l20-many-categories',
                     'That is the chance of one particular record. Multiply by the 252 ways.',
                     close(.5 ** 10, .0313, 5e-5), '0.0313 = 0.5^5; one up/not-up record has chance 0.5^10 = 0.00098')
nb = lambda t, r, p: comb(t - 1, r - 1) * p ** r * (1 - p) ** (t - r)
check('l20 NB', close(nb(5, 3, .4), .13824, 1e-12) and close(sum(nb(t, 3, .4) for t in range(3, 7)), .45568, 1e-12)
      and close(sum(comb(10, k) * .4 ** k * .6 ** (10 - k) for k in range(3)), .1673, 5e-5))
mT = sum(t * nb(t, 3, .4) for t in range(3, 400))
vT = sum(t * t * nb(t, 3, .4) for t in range(3, 400)) - mT ** 2
check('l20 NB mean 7.5 var 11.25', close(mT, 7.5, 1e-9) and close(vT, 11.25, 1e-8))
l20 = load('l20-many-categories')
ns = {}
exec(l20['screens'][10]['widget']['solution'], ns)
check('l20 code', close(ns['nb_pmf'](2, 3, .4), 0, 1e-15) and close(ns['multinomial_pmf']([6, 0, 4], [.6, 0, .4]), .250822656, 1e-12))

# review, homework, problems
check('rev4', close(.25 / .4, .625, 1e-12) and close((-.05 + .25) / .4, .5, 1e-12) and close(.6 / 12 + .4 * .5, .25, 1e-12))
check('hw4 c=0.18', close(.6 * .12 / .4, .18, 1e-12))
check('hw4 regimes -85', close(.25 * 800 - .6 * 100 - .15 * 1500, -85, 1e-9))
check('rev5', 6 * 4 + 9 * 9 == 105 and 20 * 100 + 100 * 4 == 2400 and 4 * 5 + 12 * 9 == 128 and close(2 * .8 / .04, 40, 1e-9)
      and close(.5 * (log(1.05) + log(.97)), .009165, 5e-7))
check('hw5', close(.75 * 4 + .25 * 36 + .75 + .25 * 9, 15, 1e-12) and 30 * 25 + 45 * 64 == 3630
      and close(-7 / sqrt(12 * 11.375), -.599, 5e-4))
hw5 = load('homework-5')
code = [it for it in hw5['items'] if it['id'] == 'h-code'][0]
ns = {}
exec(code['widget']['solution'], ns)
check('hw5 code sims', ns['book_sim'](2000, 1) == (120.21, 22822.56) and ns['book_sim'](3000, 3, 0.0) == (99.66, 18248.28)
      and abs(ns['book_sim'](5000, 7)[1] - 23200) < 1500 and abs(ns['book_sim'](3000, 4, 1.0)[1] - 36000) < 2500,
      (ns['book_sim'](2000, 1), ns['book_sim'](3000, 3, 0.0)))
check('hw5 code exact', ns['book_exact'](F(1, 5)) == (120, 23200) and ns['book_exact'](F(1, 2)) == (150, 29500))
# hw5 memory item: E[T | exactly one win in first four] = 9
rng = random.Random(55)
tot, cnt = 0, 0
while cnt < 60000:
    wins, t, first4 = 0, 0, 0
    while wins < 3:
        t += 1
        if rng.random() < .4:
            wins += 1
            if t <= 4:
                first4 += 1
    if first4 == 1:
        tot += t; cnt += 1
check('hw5 E[T | one win in four] = 9', abs(tot / cnt - 9) < .1, tot / cnt)
# hw5 long form
check('hw5 fund', close(1.012 ** 120, 4.18, .01) and close(exp(120 * (.012 - .07 ** 2 / 2)), 3.1, .06))
# problems-4
check('p4 courier', close(6 * (.6 * .5 + .4 * .9), 3.96, 1e-9) and close(.37 / .23, 1.6087, 5e-5))
check('p4 retry', close(2.1 / .5, 4.2, 1e-12) and close(1.95 / .7, 2.7857, 5e-5) and close(.5 + .5 * (3.2 + 1.95 / .7), 3.4929, 5e-5))
rng = random.Random(44)


def retry():
    t = 0
    while True:
        u = rng.random()
        if u < .5:
            return t + 1
        t += 2 if u < .8 else 5


m, se = mc(retry, 200000)
check('p4 retry MC 4.2', abs(m - 4.2) < 5 * se, (m, se))
# problems-5
check('p5 fish', close(31 * .25 + 220 * 2.25, 502.75, 1e-9) and close(495 / 502.75, .9846, 5e-5))
rng = random.Random(51)


def catch():
    n = max(0, round(rng.gauss(40, sqrt(40)))) if rng.random() < .7 else max(0, round(rng.gauss(10, sqrt(10))))
    return sum(rng.choice([1.0, 2.0]) for _ in range(n))  # mean 1.5, sd 0.5


xs = [catch() for _ in range(200000)]
check('p5 fish MC near 502.75 (rounded-normal counts add about 1/12 of variance each)', abs(statistics.pvariance(xs) - 502.75) < 12, statistics.pvariance(xs))
pm = {30: F(1, 4), 40: F(1, 2), 60: F(1, 4)}
over = sum(math.prod(pm[v] for v in vs) for vs in product(pm, repeat=4) if sum(F(12 * 60, v) for v in vs) > 80)
check('p5 drone 37/256', over == F(37, 256))
check('p5 chips', close(nb(5, 2, .1), .02916, 1e-12) and .6 * 180 + .4 * 40 == 124 and close(.6 * 16 + .4 * 36, 24, 1e-12))
elr = .5 * log(.9)
vlr = (log(1.5) - log(.6)) ** 2 / 4
check('p5 startup logs', close(elr, -.0527, 5e-5) and close(4 * elr, -.2108, 5e-4) and close(4 * vlr + 2 * elr ** 2, .8452, 1e-4))  # exact 0.84514; the key 0.8452 uses rounded inputs, tol 0.0005 accepts both
ew = sum(p * 1.05 ** n for n, p in ((2, .25), (4, .5), (6, .25)))
pw = sum(F(p) * sum(F(comb(n, k), 2 ** n) for k in range(n + 1) if 1.5 ** k * .6 ** (n - k) < 1) for n, p in ((2, F(1, 4)), (4, F(1, 2)), (6, F(1, 4))))
check('p5 startup E[W]=1.2184, P(W<1)=89/128', close(ew, 1.2184, 5e-5) and pw == F(89, 128))

print('%d checks, %d failed' % (n_checks, len(fails)))
sys.exit(1 if fails else 0)
