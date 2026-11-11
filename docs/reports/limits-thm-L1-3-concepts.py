#!/usr/bin/env python3
"""Concept audit checks for limits-thm levels 1 to 3 (round 1).

Pure Python (math, random, json). Run from anywhere:
    python3 docs/reports/limits-thm-L1-3-concepts.py
Exit 0 only if every check passes. A check that fails because the content
is wrong is left failing; it is listed as a finding in
docs/reviews/audit-limits-thm-1-3.md.
"""
import json
import math
import os
import random
import sys
from math import comb, exp, log, sqrt, erf

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'limits-thm')
FAILS = []
N = [0]


def check(name, ok, detail=''):
    N[0] += 1
    if not ok:
        FAILS.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))


def near(a, b, tol):
    return abs(a - b) <= tol


def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def binom_pmf(n, p, k):
    if p <= 0 or p >= 1 or n < 300:
        return comb(n, k) * p**k * (1 - p)**(n - k)
    lg = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return exp(lg + k * log(p) + (n - k) * log(1 - p))


def binom_tail(n, p, k):
    return sum(binom_pmf(n, p, j) for j in range(k, n + 1))


def pois_cdf(lam, k):
    return sum(exp(-lam) * lam**j / math.factorial(j) for j in range(k + 1))


def hyper(k, NN, K, n):
    return comb(K, k) * comb(NN - K, n - k) / comb(NN, n)


def load(name):
    with open(os.path.join(COURSE, name)) as f:
        return json.load(f)


random.seed(20261111)

# ---------------------------------------------------------------- Level 1
check('l1 s9 P(Bin(20,.55)>=15)=0.0553, once in 18', near(binom_tail(20, .55, 15), 0.0553, 5e-5)
      and near(1 / binom_tail(20, .55, 15), 18, 0.5))
check('l1 s10 0.98^50=0.3642', near(0.98**50, 0.3642, 5e-5))
check('l2 geometric: memoryless P(X>5|X>2)=P(X>3)', near(0.8**5 / 0.8**2, 0.8**3, 1e-12))
check('l2 s10 1-0.95^10=0.4013; 10th exactly 0.0315',
      near(1 - 0.95**10, 0.4013, 5e-5) and near(0.95**9 * 0.05, 0.0315, 5e-5))
check('l3 s2 (1-2/n)^n at 10, 50, 500', near(0.8**10, 0.1074, 5e-5) and near(0.96**50, 0.1299, 5e-5)
      and near(0.996**500, 0.1348, 5e-5))
check('l3 s3 Bin(500,.004) P(X=2)=0.2712', near(binom_pmf(500, .004, 2), 0.2712, 5e-5))
check('l3 s8 Pois(3) P(X>=6)=0.0839', near(1 - pois_cdf(3, 5), 0.0839, 5e-5))
check('l3 s9 Pois(2) P(X>=6)=0.0166, about 4 days in 250',
      near(1 - pois_cdf(2, 5), 0.0166, 5e-5) and near(250 * (1 - pois_cdf(2, 5)), 4, 0.5))
check('l3 quiz2 exact Bin(1000,.002) P(X=1)=0.2707', near(binom_pmf(1000, .002, 1), 0.2707, 5e-5))
check('l4 s7 C(16,5)/C(20,5)=0.2817', near(hyper(0, 20, 4, 5), 0.2817, 5e-5))
# Content claim (l4 s7 explain): "Each factor is below 0.8". The first is 16/20.
factors = [16 / 20, 15 / 19, 14 / 18, 13 / 17, 12 / 16]
check('l4 s7 CLAIM every factor of the clean-run product is below 0.8',
      all(f < 0.8 - 1e-12 for f in factors), 'first factor is exactly 0.8 (finding 1)')
t = [(20, 0.2817, 0.0459), (100, 0.3193, 0.0084), (1000, 0.3269, 0.0008)]
check('l4 s9 table exact, gap', all(near(hyper(0, n, n // 5, 5), e, 6e-5) and
                                    near(0.8**5 - hyper(0, n, n // 5, 5), g, 1.1e-4) for n, e, g in t))
tail = sum(hyper(k, 100, 20, 10) for k in range(4, 11))
check('l4 s10 hyper tail 0.1096, binomial 0.1209', near(tail, 0.1096, 5e-5)
      and near(binom_tail(10, .2, 4), 0.1209, 5e-5))
check('l4 quiz0 one ace 0.2995, binomial 0.2792', near(hyper(1, 52, 4, 5), 0.2995, 5e-5)
      and near(binom_pmf(5, 1 / 13, 1), 0.2792, 5e-5))
check('hw1 item4 1-C(45,10)/C(50,10)=0.6894', near(1 - hyper(0, 50, 5, 10), 0.6894, 5e-5))
pm = [hyper(k, 20, 4, 5) for k in range(5)]
check('hw1 item8 hypergeometric variance 0.6316 two ways',
      near(sum((k - 1)**2 * q for k, q in enumerate(pm)), 0.8 * 15 / 19, 1e-12))
check('hw1 item9 capped wait E[T]=(1-q^m)/p=5.354',
      near(sum(k * 0.85**(k - 1) * 0.15 for k in range(1, 10)) + 10 * 0.85**9, (1 - 0.85**10) / 0.15, 1e-12)
      and near((1 - 0.85**10) / 0.15, 5.354, 5e-4))
# problems-1
check('p1 item0 0.996^400, Pois(1.6) tails', near(0.996**400, 0.2012, 5e-5)
      and near(1 - pois_cdf(1.6, 3), 0.0788, 5e-5) and near(1 - pois_cdf(1.6, 5), 0.0060, 5e-5)
      and near(0.9212**30, 0.0852, 5e-5))
check('p1 item2 Bin(12,.65) P(X>=10)=0.1513', near(binom_tail(12, .65, 10), 0.1513, 5e-5))
check('p1 item3 exact clean run 0.2139', near(hyper(0, 2000, 60, 50), 0.2139, 5e-5))
nmin = next(n for n in range(1, 400) if 1 - hyper(0, 2000, 60, n) >= 0.99)
check('p1 item3 exact smallest n is 146; binomial 152; 0.98994 at 151', nmin == 146
      and near(1 - 0.97**151, 0.98994, 5e-6) and 1 - 0.97**152 >= 0.99, 'exact n=%d' % nmin)

# ---------------------------------------------------------------- Level 2
check('l7 s3 CLAIM 2.28% of days is "roughly once a month" (21 trading days)',
      near(1 / (1 - Phi(2)), 21, 5), '1 in %.0f days, about two months (finding 2)' % (1 / (1 - Phi(2))))
check('l7 s4 0.3085/0.0228 about 13', near(Phi(-0.5) / Phi(-2), 13.5, 0.6))
check('l7 s8 Phi(-3.05/1.2)=0.0055, once in 180 days', near(Phi(-3.05 / 1.2), 0.0055, 5e-5)
      and near(1 / Phi(-3.05 / 1.2), 181, 2))
check('l7 s9 VaR return -2.74%', near(0.05 - 2.326 * 1.2, -2.741, 1e-3))
p41 = binom_tail(2520, 0.01, 41)
check('l7 s10 P(Bin(2520,.01)>=41) about 1 in 450', 300 < 1 / p41 < 700, '1 in %.0f' % (1 / p41))
check('l8 mean/median', near(100 * exp(0.32), 137.71, 5e-3) and near(exp(4.745), 115.01, 5e-3)
      and near(exp(4.7), 109.95, 5e-3))
sdS = 54.16 * sqrt(exp(0.16) - 1)
check('l8 s6 wrong options 0.5793, 0.5732', near(Phi(0.2), 0.5793, 5e-5)
      and near(1 - Phi((50 - 54.16) / sdS), 0.5732, 2e-4))
z = (log(1.2) - 0.03) / 0.2
check('l8 s8 P(S1>120)=0.2231 and four slips', near(1 - Phi(z), 0.2231, 5e-5)
      and near(1 - Phi((log(1.2) - 0.05) / 0.2), 0.2541, 5e-5)
      and near(1 - Phi((0.2 - 0.03) / 0.2), 0.1977, 5e-5)
      and near(1 - Phi(log(1.2) / 0.2), 0.1810, 5e-5)
      and near(1 - Phi((120 - 100 * exp(.05)) / (100 * exp(.05) * sqrt(exp(.04) - 1))), 0.2419, 2e-4))
check('r2 item8 0.4345', near(Phi(-0.07 / (0.3 * sqrt(2))), 0.4345, 5e-5))
check('hw2 item3 sd 10.25', near(30 / (1.6449 + 1.2816), 10.25, 5e-3))
check('hw2 item5 0.3787', near(Phi((log(1.1) - .03) / .2) - Phi((log(.9) - .03) / .2), 0.3787, 5e-5))
check('hw2 item6 VaR 352,900 and slips', near(1e6 * (1 - exp(0.03 - 2.326 * 0.2)), 352900, 100)
      and near(1e6 * (1 - exp(0.05 - 2.326 * 0.2)), 339800, 100)
      and near(1e6 * (1 - exp(-2.326 * 0.2)), 371990, 100))
check('hw2 item8 0.95^40, 0.995^400 below e^-2', near(0.95**40, 0.1285, 5e-5)
      and near(0.995**400, 0.1347, 5e-5) and 0.995**400 < exp(-2))
check('p2 item1 VaR 30.42', near(80 - 80 * exp(0.015 - 1.645 * 0.3), 30.42, 5e-3))
check('p2 item2 triangle var 6; VaR 4.10; 99% gap 0.55',
      near(2 / 36 * (432 - 324), 6, 1e-12) and near(6 - sqrt(3.6), 4.10, 5e-3)
      and near(2.326 * sqrt(6) - (6 - sqrt(0.72)), 0.55, 6e-3))
check('p2 item3 0.9512*41.63=39.60; 0.4529', near(exp(-.05) * 40 * exp(.04), 39.60, 5e-3)
      and near(0.9512 * 0.4761, 0.4529, 5e-5))

# Monte Carlo: lognormal, P(S below its own mean) = Phi(sigma sqrt(T)/2) (l8 s9, s7)
R = 200000
below = sum(1 for _ in range(R) if exp(0.03 + 0.2 * random.gauss(0, 1)) < exp(0.05)) / R
check('MC l8 s9 P(S1 < E[S1]) = Phi(0.1) = 0.5398', near(below, 0.5398, 0.004), '%.4f' % below)
# Monte Carlo: exponential memorylessness (l6 s6)
xs = [random.expovariate(2) for _ in range(R * 3)]
gt1 = [x for x in xs if x > 1]
mm = sum(1 for x in gt1 if x > 1.5) / len(gt1)
check('MC l6 s6 P(T>1.5|T>1) = e^-1', near(mm, exp(-1), 0.008), '%.4f' % mm)

# ---------------------------------------------------------------- Level 3
# l9 s2: exact chance that the mean of n dice misses 3.5 by more than 0.25
def die_far(n):
    dist = {0: 1.0}
    for _ in range(n):
        new = {}
        for s, pr in dist.items():
            for f in range(1, 7):
                new[s + f] = new.get(s + f, 0.0) + pr / 6
        dist = new
    return sum(pr for s, pr in dist.items() if abs(s / n - 3.5) > 0.25 + 1e-12)


d10, d100, d1000 = die_far(10), die_far(100), die_far(1000)
check('l9 s2 far chances 0.6479, 0.1355, 3.4e-6', near(d10, 0.6479, 5e-5) and near(d100, 0.1355, 5e-5)
      and near(d1000, 3.4e-6, 1.5e-7), '%.4f %.4f %.2e' % (d10, d100, d1000))
l9 = load('l9-averages-settle.json')
s = l9['screens']
a, b, c = [x['values'] for x in s[0]['canvas']['params']['series']]
check('l9 s0 data matches text (4.50, 2.60, 3.70; 3.56, 3.43, 3.50)',
      [round(v[9], 2) for v in (a, b, c)] == [4.5, 2.6, 3.7]
      and [round(v[999], 2) for v in (a, b, c)] == [3.56, 3.43, 3.5])
v = s[1]['canvas']['params']['series'][0]['values']
check('l9 s1 data: 0.50 after 100 cards, 0.98 after 2,000', near(v[99], 0.50, 0.005) and near(v[1999], 0.98, 0.005))
sh = s[3]['canvas']['left']['params']['series'][0]['values']
ht = s[3]['canvas']['right']['params']['series'][0]['values']
check('l9 s3 data: share 0.491 and 0.4958; gap -18 and -84',
      near(sh[9], 0.491, 5e-4) and near(sh[99], 0.4958, 5e-5) and ht[9] == -18 and ht[99] == -84)
sp = s[7]['canvas']['params']['series'][0]['values']
check('l9 s7 data: about 13 at 1,000 games, about 42 at 2,550', near(sp[99], 13, 1.0) and near(sp[254], 42, 2.5),
      '%.2f %.2f' % (sp[99], sp[254]))
# MC: given a gap of -18 at 1,000 tosses, is |gap| at 10,000 typically larger? (l9 s3 key)
further = 0
for _ in range(20000):
    # 9,000 further tosses: gap change = 2*Bin(9000, .5) - 9000, use the normal sd sqrt(9000)
    g = -18 + random.gauss(0, sqrt(9000))
    further += abs(g) > 18
check('MC l9 s3 gap at 10,000 typically further from 0 than 18', further / 20000 > 0.75, '%.3f' % (further / 20000))
# MC: St Petersburg running mean does not settle: medians of the mean grow with n (l9 s7)
def stp():
    k = 1
    while random.random() < 0.5:
        k += 1
    return 2.0**k


def med_mean(n, reps=300):
    ms = sorted(sum(stp() for _ in range(n)) / n for _ in range(reps))
    return ms[reps // 2]


m1, m2 = med_mean(200), med_mean(20000, 120)
check('MC l9 s7 St Petersburg average keeps rising (median of mean grows with n)', m2 > m1 + 3, '%.1f -> %.1f' % (m1, m2))
# MC: Cauchy sample mean does not tighten (l9 summary, l11 quiz1)
def iqr_cauchy_mean(n, reps=1500):
    ms = sorted(sum(math.tan(math.pi * (random.random() - 0.5)) for _ in range(n)) / n for _ in range(reps))
    return ms[3 * reps // 4] - ms[reps // 4]


q1, q2 = iqr_cauchy_mean(1), iqr_cauchy_mean(400)
check('MC Cauchy mean of 400 as spread out as one draw (IQR about 2)', near(q1, 2, 0.35) and near(q2, 2, 0.35),
      '%.2f %.2f' % (q1, q2))
check('l9 s9 roulette: mean 27,027, sd 3,161, 8.5 sds', near(1e5 * 10 / 37, 27027, 1)
      and near(sqrt(1e5 * (100 - (10 / 37)**2)), 3161, 2) and near(27027 / 3161, 8.55, 0.02))
check('l10 s6 normal two-sided tails', near(2 * Phi(-1.5), 0.1336, 5e-5) and near(2 * Phi(-2), 0.0455, 5e-5)
      and near(2 * Phi(-3), 0.0027, 5e-5))
check('l10 s9 Chebyshev 4,000; normal 1,083', near(4 / (0.1 * 0.01), 4000, 1e-9)
      and math.ceil((1.6449 * 2 / 0.1)**2) == 1083)
# l11 bins: gamma(n) for exponential mean, Irwin-Hall for uniform mean
def gamma_cdf(n, x):
    if x <= 0:
        return 0.0
    return 1 - sum(exp(-x) * x**j / math.factorial(j) for j in range(n))


def exp_bin(n, lo, hi):  # P(lo < Z <= hi), Z = (S - n)/sqrt(n)
    return gamma_cdf(n, n + hi * sqrt(n)) - gamma_cdf(n, n + lo * sqrt(n))


l11 = load('l11-sums-look-normal.json')
c0 = l11['screens'][0]['canvas']
okb = True
for nn in (1, 3, 30):
    for i in range(14):
        lo = -3 + 0.5 * i
        okb &= near(c0['params']['params']['e%d' % i][nn], exp_bin(nn, lo, lo + 0.5), 6e-5)
check('l11 s0 exponential bars exact for n = 1, 3, 30', okb)
check('l11 s0 normal dashes', near(Phi(0.5) - 0.5, 0.1915, 5e-5) and near(Phi(-1.5), 0.0668, 5e-5))
check('l11 s6 normal 0.0786, exact gamma 0.0844', near(1 - Phi(10 / sqrt(50)), 0.0786, 5e-5)
      and near(1 - gamma_cdf(50, 60), 0.0844, 5e-5), '%.4f' % (1 - gamma_cdf(50, 60)))
def ih_cdf(n, x):  # Irwin-Hall CDF
    if x <= 0:
        return 0.0
    if x >= n:
        return 1.0
    return sum((-1)**k * comb(n, k) * (x - k)**n for k in range(int(math.floor(x)) + 1)) / math.factorial(n)


u3 = [ih_cdf(3, 1.5 + (-3 + 0.5 * (i + 1)) * sqrt(3 / 12)) - ih_cdf(3, 1.5 + (-3 + 0.5 * i) * sqrt(3 / 12)) for i in range(14)]
shown = l11['screens'][2]['canvas']['right']['state']['values']
dash = [Phi(-3 + 0.5 * (i + 1)) - Phi(-3 + 0.5 * i) for i in range(14)]
check('l11 s2 uniform n=3 bars exact and within 0.01 of the normal',
      all(near(shown['b%d' % i], u3[i], 6e-5) for i in range(14)) and all(abs(u3[i] - dash[i]) < 0.01 for i in range(14)))
# 100 dice total > 370 (l11 quiz2): normal 0.121; report the exact figure
dist = {0: 1.0}
for _ in range(100):
    new = {}
    for ss, pr in dist.items():
        for f in range(1, 7):
            new[ss + f] = new.get(ss + f, 0.0) + pr / 6
    dist = new
ex370 = sum(pr for ss, pr in dist.items() if ss > 370)
check('l11 quiz2 normal 0.121 (exact %.4f, within 0.01)' % ex370, near(1 - Phi(1.17), 0.121, 5e-4) and near(ex370, 0.121, 0.01))
check('l12 numbers: 0.17, 1.90, 0.028, 1600, SR 0.79, 0.606', near(1 - Phi(0.12 * sqrt(63)), 0.17, 0.005)
      and near(0.06 * sqrt(1008), 1.90, 0.01) and near(1 - Phi(1.905), 0.028, 6e-4)
      and near(0.05 * sqrt(252), 0.79, 0.005) and near(1 - (2 * Phi(2) - 1)**20, 0.606, 1e-3))
check('l12 s9 losing year 0.2136', near(Phi(-1.26 / (0.1 * sqrt(252))), 0.2136, 5e-4))
# MC: standard error of an annualised Sharpe ratio is about 1/sqrt(T) (l12 s5), iid normal days
def sr_hat(T, mu=0.0005, sd=0.01):
    n = int(252 * T)
    xs = [random.gauss(mu, sd) for _ in range(n)]
    m = sum(xs) / n
    s2 = sum((x - m)**2 for x in xs) / (n - 1)
    return m / sqrt(s2) * sqrt(252)


srs = [sr_hat(2) for _ in range(1500)]
mS = sum(srs) / len(srs)
seS = sqrt(sum((x - mS)**2 for x in srs) / (len(srs) - 1))
check('MC l12 s5 SE(SR-hat) over 2 years about 1/sqrt(2)=0.707', near(seS, 1 / sqrt(2), 0.05), '%.3f' % seS)
# MC: a true edge with expected t = 2 clears 2 about half the time (l12 s3)
hit = 0
for _ in range(1500):
    xs = [random.gauss(0.05, 1.0) for _ in range(1600)]
    hit += (sum(xs) / 1600) * sqrt(1600) / 1.0 > 2
check('MC l12 s3 expected t of 2 clears 2 about half the time', near(hit / 1500, 0.5, 0.05), '%.3f' % (hit / 1500))
# l13
check('l13 exact 0.0553, P(X<=8)=0.1308, P(X=12)=0.162', near(binom_tail(20, .55, 15), 0.0553, 5e-5)
      and near(1 - binom_tail(20, .55, 9), 0.1308, 5e-5) and near(binom_pmf(20, .55, 12), 0.162, 5e-4))
check('l13 normal 0.0579/0.0578, 0.0361, 0.1306, 0.161', near(1 - Phi(3.5 / sqrt(4.95)), 0.0578, 1e-4)
      and near(1 - Phi(4 / sqrt(4.95)), 0.0361, 1e-4) and near(Phi(-2.5 / sqrt(4.95)), 0.1306, 1e-4)
      and near(Phi(1.5 / sqrt(4.95)) - Phi(0.5 / sqrt(4.95)), 0.161, 6e-4))
check('l13 s7 Bin(100,.02) P(X>=5): 0.0508, Poisson 0.0527, normal 0.0371', near(binom_tail(100, .02, 5), 0.0508, 5e-5)
      and near(1 - pois_cdf(2, 4), 0.0527, 5e-5) and near(1 - Phi(2.5 / 1.4), 0.0371, 5e-5))
check('l13 s8 0.0287 against exact 0.0284', near(1 - Phi(1.9), 0.0287, 5e-5) and near(binom_tail(100, .5, 60), 0.0284, 5e-5))
check('l13 s9 0.0159, exact 0.0207, Poisson 0.0218', near(1 - Phi(9.5 / sqrt(19.6)), 0.0159, 5e-5)
      and near(binom_tail(1000, .02, 30), 0.0207, 5e-5) and near(1 - pois_cdf(20, 29), 0.0218, 5e-5))
check('l13 quiz2 exact P(Bin(100,.5)=50)=0.0796', near(binom_pmf(100, .5, 50), 0.0796, 5e-5))
check('r3 item6 0.0968 against exact 0.0978; item7 0.5704 exact',
      near(binom_tail(50, .4, 25), 0.0978, 5e-5) and near(binom_tail(40, .5, 18) - binom_tail(40, .5, 23), 0.5704, 5e-5))
check('r3 item5 at least one of 50 about 0.68', near(1 - Phi(2)**50, 0.68, 0.005))
check('hw3 item5 normal 0.0146, exact 0.0190', near(1 - Phi(9.5 / sqrt(19)), 0.0146, 1e-4)
      and near(binom_tail(400, .05, 30), 0.0190, 5e-5))
check('hw3 item7 1.06, 0.82, 1.30, 0.64', near(0.06 / 0.9 * sqrt(252), 1.06, 0.005) and near(1 / sqrt(1.5), 0.82, 0.005)
      and near(0.06 * sqrt(378) / 0.9, 1.30, 0.005) and near(1 - Phi(1.30)**10, 0.64, 0.005))
# hw3 item9 (d): exact P(W_A + 2 W_B <= n)
def desk_fail(n):
    pa = [binom_pmf(n, .55, k) for k in range(n + 1)]
    ca = [0.0] * (n + 2)
    for k in range(n + 1):
        ca[k + 1] = ca[k] + pa[k]
    tot = 0.0
    for wb in range(n // 2 + 1):
        tot += binom_pmf(n, .3, wb) * ca[n - 2 * wb + 1]
    return tot


f131 = desk_fail(131)
first = next(n for n in range(100, 200) if desk_fail(n) <= 0.05)
stays = all(desk_fail(n) <= 0.05 for n in range(136, 420))
check('hw3 item9 exact: 0.0528 at 131, first at most 0.05 at 136, stays below to 419',
      near(f131, 0.0528, 5e-5) and first == 136 and stays, '%.4f first=%d' % (f131, first))
check('hw3 item9 Chebyshev 967, normal 131', math.ceil(4.35 / (0.09 * 0.05)) == 967
      and math.ceil((1.6449 * sqrt(4.35) / 0.3)**2) == 131)
check('p3 item0 normal 0.0537, exact 0.0626, Poisson 0.0648',
      near(1 - Phi(3.8 / sqrt(5.7 * 0.9772)), 0.0537, 2e-4) and near(binom_tail(250, .0228, 10), 0.0626, 5e-5)
      and near(1 - pois_cdf(5.7, 9), 0.0648, 5e-5))
check('p3 item1 0.0606 against exact 0.0605; cut-off 227', near(binom_tail(400, .5, 216), 0.0605, 5e-5)
      and binom_tail(400, .5, 227) < 0.0043 <= binom_tail(400, .5, 226),
      '%.5f %.5f' % (binom_tail(400, .5, 226), binom_tail(400, .5, 227)))
check('p3 item2 Chebyshev 320, normal 62', 16 / 0.05 == 320 and math.ceil((1.96 * 4)**2) == 62)

# MC: aggregational normality with volatility clustering (l11 s8 key and explain).
# GARCH(1,1) with Student-t(5) shocks: excess kurtosis of 20-day sums is below the
# daily figure, and above that of 20-day sums of the same days shuffled (iid).
def tshock():
    zz = random.gauss(0, 1)
    ch = sum(random.gauss(0, 1)**2 for _ in range(5)) / 5
    return zz / sqrt(ch) * sqrt(3 / 5)  # unit variance


def kurt(xs):
    n = len(xs)
    m = sum(xs) / n
    v2 = sum((x - m)**2 for x in xs) / n
    return sum((x - m)**4 for x in xs) / n / v2**2 - 3


def med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2]


kd, k20, ks = [], [], []
for rep in range(12):
    h, r = 1.0, []
    for _ in range(40000):
        e = sqrt(h) * tshock()
        r.append(e)
        h = 0.05 + 0.10 * e * e + 0.85 * h
    sums = [sum(r[i:i + 20]) for i in range(0, len(r), 20)]
    sh2 = r[:]
    random.shuffle(sh2)
    sums_iid = [sum(sh2[i:i + 20]) for i in range(0, len(sh2), 20)]
    kd.append(kurt(r)); k20.append(kurt(sums)); ks.append(kurt(sums_iid))
check('MC l11 s8 20-day sums nearer normal than days; clustering slows it',
      med(k20) < med(kd) and med(k20) > med(ks) + 0.2,
      'excess kurtosis daily %.2f, 20-day %.2f, 20-day shuffled %.2f' % (med(kd), med(k20), med(ks)))
# MC: CLT speed depends on tail weight as well as skew (finding on l11 s2):
# a symmetric t(3) average is still far from normal at n = 3 where the uniform is close.
def t3():
    zz = random.gauss(0, 1)
    ch = sum(random.gauss(0, 1)**2 for _ in range(3)) / 3
    return zz / sqrt(ch) / sqrt(3)  # unit variance


cnt = sum(1 for _ in range(150000) if abs(sum(t3() for _ in range(3)) / sqrt(3)) < 0.5) / 150000
check('MC symmetric t(3): P(|Z|<0.5) at n=3 is far from the normal 0.383 (supports finding on l11 s2)',
      abs(cnt - 0.383) > 0.05, '%.3f' % cnt)

print('\n%d checks, %d failed' % (N[0], len(FAILS)))
for f in FAILS:
    print('  failed: ' + f)
sys.exit(1 if FAILS else 0)
