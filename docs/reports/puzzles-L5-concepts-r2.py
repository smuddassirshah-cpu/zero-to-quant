#!/usr/bin/env python3
"""Concept audit round 2, puzzles L5 (l25 to l30, review-5, homework-5).

Exact checks (Fraction, sympy, exhaustive enumeration, independent backward
induction) and Monte Carlo checks for every stated probability, expectation,
estimator, optimal strategy and code-behaviour claim. Run from the repo root:

    python3 -I docs/reports/puzzles-L5-concepts-r2.py

Exit 0 when the content is correct. Each assert names its ledger row
(file:path). A check that fails because the content is wrong is marked
EXPECTED_FAIL with the corrected assert in a comment beside it; the two
EXPECTED_FAIL checks below are the audit's findings 2 and 3 (imprecise claims
whose literal reading is false). They are run last so every other check still
reports.
"""
import json
import math
import random
import sys
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, log, sqrt, pi

import numpy as np
import sympy as sp

ROOT = 'app/content/courses/puzzles/'
N_CHECKS = 0
FAILS = []


def check(cond, name, expected_fail=False):
    global N_CHECKS
    N_CHECKS += 1
    if expected_fail:
        if cond:
            print('ok   (unexpectedly passed) ', name)
        else:
            print('FAIL EXPECTED_FAIL ', name)
            FAILS.append(name)
        return
    assert cond, name
    print('ok  ', name)


def close(a, b, tol):
    return abs(a - b) <= tol


def run_code_widget(path, locator):
    d = json.load(open(ROOT + path))
    w = locator(d)['widget']
    ns = {}
    exec(w.get('prelude', ''), ns)
    exec(w['solution'], ns)
    passed = 0
    for t in w['tests']:
        cmp = t.get('compare', 'equal')
        try:
            got = eval(t['call'], ns)
        except Exception as e:  # noqa
            got = e
        exp_ = t['expect']
        if cmp == 'raises':
            passed += isinstance(got, Exception) and type(got).__name__ == exp_
            continue
        if isinstance(exp_, str):
            try:
                exp_ = eval(exp_, ns)
            except Exception:  # noqa
                pass
        if cmp == 'fraction':
            ok = F(got) == F(exp_)
        elif cmp == 'isclose':
            ok = abs(float(got) - float(exp_)) <= t.get('tol', {}).get('abs', 1e-9)
        else:
            ok = got == exp_
        passed += bool(ok)
    return passed, len(w['tests'])


screen = lambda i: (lambda d: d['screens'][i])
item = lambda i: (lambda d: d['items'][i])
rng = random.Random(20261106)
nrng = np.random.default_rng(20261106)

# ======================================================================
# l25 fair from biased
# ======================================================================
L25 = 'l25-fair-from-biased.json'
p = sp.symbols('p', positive=True)
check(F(2, 3) * F(1, 3) == F(1, 3) * F(2, 3) == F(2, 9) and F(2, 3) ** 2 == F(4, 9) and F(1, 3) ** 2 == F(1, 9), f'{L25}:screens[1] HT = TH = 2/9, HH = 4/9, TT = 1/9')
check(sp.simplify(p * (1 - p) - (1 - p) * p) == 0, f'{L25}:screens[6,7] independence gives P(HT) = P(TH) = pq for every p')
ef = lambda pv: 2 / (2 * F(pv) * (1 - F(pv)))
check(ef(F(2, 3)) == F(9, 2) and ef(F(3, 5)) == F(25, 6) and ef(F(1, 2)) == 4 and ef(F(9, 10)) == F(100, 9) and ef(F(4, 5)) == F(25, 4), f'{L25}:screens[2,3,9,11], quiz: flips 9/2, 25/6, 4, 100/9, 25/4')
check(2 * F(7, 10) * F(3, 10) == F(21, 50) and F(21, 50) == F(42, 100), f'{L25}:screens[9] row 1: round kept with 2pq = 0.42 at p = 0.7')
check(3 * F(8, 6) == 4 and 2 * F(4, 3) == F(8, 3) and 3 * F(8, 5) == F(24, 5), f'{L25}:screens[4,9], review-5 items[0]: die from a coin 4 flips, three people 8/3, five people 24/5')
pq2 = F(3, 5) * F(2, 5) ** 2
check(pq2 == F(12, 125) and 3 / (3 * pq2) == F(125, 12) and F(125, 12) / F(25, 6) == F(5, 2), f'{L25}:screens[10] HTT/THT/TTH each pq^2 = 0.096, flips 125/12, 2.5 times the two-way wait')
check(2 * F(25, 6) == F(25, 3) and 2 * F(25, 6) * F(4, 3) == F(100, 9), f'{L25}:quiz[2], homework-5 items[5]: two bits 25/3; two bits with a restart 100/9')
check(F(125, 12) < F(100, 9), 'homework-5.json:items[3].model, items[5]: the direct three-flip method (125/12) beats two bits with restart (100/9)')
# Wald: expected flips = flips per round x expected rounds, MC at p = 0.6 and p = 0.8
def vn_flips(pv, trials):
    tot = 0
    for _ in range(trials):
        while True:
            a, b = rng.random() < pv, rng.random() < pv
            tot += 2
            if a != b:
                break
    return tot / trials
s = vn_flips(0.6, 100_000)
check(close(s, 25 / 6, 0.03), f'{L25}:screens[3] MC flips per fair bit at p=0.6 ~ 4.1667 (got {s:.4f})')
# fairness of the bit at p = 0.8: share of H among kept bits ~ 1/2 (exact: P(HT|kept) = 1/2)
flips = nrng.random(400_000) < 0.8
pairs = flips.reshape(-1, 2)
kept = pairs[pairs[:, 0] != pairs[:, 1]]
share = kept[:, 0].mean()
check(close(share, 0.5, 3 * 0.5 / sqrt(len(kept))), f'{L25}:screens[8].explain MC kept bits are heads with chance 1/2 at p=0.8 (got {share:.4f} over {len(kept)} bits)')
check(close(len(kept) / 200_000, 0.32, 0.005), f'{L25}:screens[8].explain a pair is kept with chance 2pq = 0.32 at p=0.8')
check(run_code_widget(L25, screen(8)) == (10, 10), f'{L25}:screens[8] solution passes all 10 hidden tests')
check(close(sqrt(10000 * 0.32 * 0.68) * 3, 150, 15) and close(3 * 0.5 / sqrt(3200), 0.03, 0.005), f'{L25}:screens[8].how tolerances 150 bits and 0.03 are about three standard errors')
# trap: HH heads is unfair; p=1 never succeeds
check(F(2, 3) ** 2 != F(1, 2) and 2 * F(1) * 0 == 0, f'{L25}:screens[5], quiz[1]: HH has chance 4/9; at p=1 no round succeeds')

# ======================================================================
# l26 estimating n
# ======================================================================
L26 = 'l26-estimating-n.json'
def all_samples(N, k):
    return list(combinations(range(1, N + 1), k))

def e_max_exact(N, k):
    s = all_samples(N, k)
    return F(sum(max(t) for t in s), len(s))

check(e_max_exact(20, 2) == 14 and e_max_exact(20, 3) == F(63, 4) and e_max_exact(10, 4) == F(44, 5), f'{L26}:screens[2,7], quiz[1]: E[max] = 14, 15.75, 8.8 (exhaustive)')
for N, k in ((20, 2), (20, 3), (10, 4), (12, 4), (30, 5)):
    check(e_max_exact(N, k) == F(k * (N + 1), k + 1), f'{L26}:screens[4] E[m] = k(N+1)/(k+1) at N={N}, k={k} (exhaustive)')
    s = all_samples(N, k)
    est = [max(t) + F(max(t), k) - 1 for t in s]
    mean_based = [2 * F(sum(t), k) - 1 for t in s]
    check(F(sum(est), len(s)) == N and F(sum(mean_based), len(s)) == N, f'{L26}:screens[5], screens[1].byKey.mean-based: m + m/k - 1 and 2*mean - 1 are both unbiased at N={N}, k={k} (exhaustive)')
# variances at k = 4: mean-based / max-based = (k+2)/3 = 2
def var_of(vals):
    m = F(sum(vals), len(vals))
    return F(sum((v - m) ** 2 for v in vals), len(vals))
s = all_samples(30, 4)
v_max_est = var_of([max(t) + F(max(t), 4) - 1 for t in s])
v_mean_est = var_of([2 * F(sum(t), 4) - 1 for t in s])
v_raw_max = var_of([F(max(t)) for t in s])
check(v_mean_est / v_max_est == 2, f'{L26}:screens[3] options[2].why mean-based estimate has twice the variance of the max-based one at k=4 (exhaustive, N=30)')
N_, k_ = sp.symbols('N k', positive=True)
check(sp.simplify(((N_ + 1) * (N_ - k_) / (3 * k_)) / ((N_ + 1) * (N_ - k_) / (k_ * (k_ + 2))) - (k_ + 2) / 3) == 0, f'{L26}:screens[3] variance ratio is (k+2)/3 in general (Var m from Casella-Berger style order-statistic moments)')
check(all(max(t) <= 30 for t in s) and F(sum(max(t) for t in s), len(s)) < 30, f'{L26}:screens[3] options[1].why the largest seen is never above N, so its mean is below N')
# the MLE of N is the maximum m (likelihood 1/C(N,k) decreases in N)
check(all(F(1, comb(N1, 4)) > F(1, comb(N1 + 1, 4)) for N1 in range(4, 40)), f'{L26}:screens[5] lines[d1] the largest is the most likely value (MLE), yet biased')
# serial-number arithmetic
est = lambda m, k: m + F(m, k) - 1
check(est(60, 1) == 119 and est(60, 4) == 74 and est(100, 5) == 119 and est(812, 5) == F(4867, 5) and est(50, 2) == 74 and est(45, 3) == 59 and est(10, 10) == 10, f'{L26}/review-5 estimates 119, 74, 119, 973.4, 74, 59, 10')
check(60 - 4 == 56 and F(56, 4) == 14 and [18, 20, 1, 17] == [19 - 1, 40 - 19 - 1, 42 - 40 - 1, 60 - 42 - 1], f'{L26}:screens[1] gaps 18, 20, 1, 17 hold 56 unseen numbers, 14 on average')
# uniform [0, theta]: E[max of k] = k theta/(k+1); (k+1)/k * m unbiased
th, x = sp.symbols('theta x', positive=True)
for kk in (3, 4):
    emax = sp.integrate(x * kk * x ** (kk - 1) / th ** kk, (x, 0, th))
    check(sp.simplify(emax - kk * th / (kk + 1)) == 0, f'{L26}:screens[7], quiz[2]: E[max of {kk} uniforms] = {kk}/{kk+1} theta, so (k+1)/k m is unbiased')
check(F(4, 3) * F(9, 10) == F(6, 5) and F(5, 4) * 2 == F(5, 2), f'{L26}:screens[7] row 2, quiz[2]: 1.2 and 2.5')
# range estimator for an unknown start
def e_range_exact(N, k):
    s_ = all_samples(N, k)
    return F(sum(max(t) - min(t) for t in s_), len(s_))
check(e_range_exact(50, 4) == F(3 * 51, 5) and e_range_exact(12, 4) == F(3 * 13, 5), f'{L26}:screens[8], homework-5 items[2]: E[R] = (k-1)(N+1)/(k+1) (exhaustive at N=50 and 12, k=4)')
s50 = all_samples(50, 4)
check(F(sum((max(t) - min(t)) * F(5, 3) - 1 for t in s50), len(s50)) == 50, f'{L26}:screens[8].explain the range estimate averages exactly 50 over every set of four from 1 to 50')
check(41 * F(5, 3) - 1 == F(202, 3) and 57 * F(6, 4) - 1 == F(169, 2), f'{L26}:screens[8], review-5 items[2]: 202/3 and 84.5')
check(e_range_exact(12, 4) < 12 - 1, 'homework-5.json:items[2] lines[d1].why R itself is biased low (two end gaps missing)')
check(run_code_widget(L26, screen(6)) == (8, 8), f'{L26}:screens[6] solution passes all 8 hidden tests')
check(run_code_widget('homework-5.json', item(1)) == (7, 7), 'homework-5.json:items[1] solution passes all 7 hidden tests')
d26 = json.load(open(ROOT + L26))
ns = {}
exec(d26['screens'][6]['widget']['solution'], ns)
m_est, m_max = ns['tank_sim'](100, 5, 20000, 1)
check(close(m_est, 99.94, 0.005) and close(float(F(5 * 101, 6)), 84.17, 0.005), f'{L26}:screens[6].explain seed 1 gives about 99.94 (got {m_est:.2f}); mean maximum 84.17')
sd_est = sqrt(101 * 95 / (5 * 7))
check(close(3 * sd_est / sqrt(20000), 0.35, 0.01), f'{L26}:screens[6].how tolerance 0.36 is three standard errors ({3 * sd_est / sqrt(20000):.3f})')
# MC: the max-based estimate centres on N, the raw max below it
samp = np.array([nrng.choice(100, 5, replace=False) + 1 for _ in range(20000)])
mx = samp.max(axis=1)
check(close((mx + mx / 5 - 1).mean(), 100, 0.4) and close(mx.mean(), 505 / 6, 0.4), f'{L26}:screens[6] MC mean estimate ~ 100, mean max ~ 84.17')

# ======================================================================
# l27 conditioning on a total
# ======================================================================
L27 = 'l27-given-the-total.json'
rolls = list(product(range(1, 7), repeat=2))
cond = lambda ev, gv, rs=rolls: F(sum(1 for r in rs if gv(r) and ev(r)), sum(1 for r in rs if gv(r)))
cmean = lambda f, gv, rs=rolls: F(sum(f(r) for r in rs if gv(r)), sum(1 for r in rs if gv(r)))
check(sum(1 for r in rolls if sum(r) == 8) == 5 and cond(lambda r: r[0] % 2 == 0 and r[1] % 2 == 0, lambda r: sum(r) == 8) == F(3, 5), f'{L27}:screens[0,1] five rolls total 8; both even 3/5')
check(cmean(max, lambda r: sum(r) == 10) == F(17, 3) and cmean(max, lambda r: True) == F(161, 36), f'{L27}:screens[2] E[max | total 10] = 17/3; unconditional 161/36')
check(sum(1 for r in rolls if max(r) == 5) == 9 and cond(lambda r: r == (5, 5), lambda r: max(r) == 5) == F(1, 9), f'{L27}:screens[3,4] nine rolls with max 5; both 5 with 1/9')
check(cmean(sum, lambda r: max(r) == 5) == F(70, 9) and cmean(sum, lambda r: True) == 7, f'{L27}:screens[6] E[total | max 5] = 70/9; unconditional 7')
check(cond(lambda r: 1 in r, lambda r: sum(r) == 6) == F(2, 5) and cmean(min, lambda r: max(r) == 6) == F(36, 11) and cond(lambda r: 6 in r, lambda r: sum(r) == 7) == F(1, 3), f'{L27}:screens[8,9] 2/5, 36/11, 1/3')
r3 = list(product(range(1, 7), repeat=3))
check(cond(lambda r: 3 in r, lambda r: sum(r) == 5, r3) == F(1, 2) and sum(1 for r in r3 if sum(r) == 5) == 6, f'{L27}:screens[8] row 2: three dice total 5 in six ways, three with a 3')
check(sum(1 for r in r3 if sum(r) == 10) == 27 and cond(lambda r: 6 in r, lambda r: sum(r) == 10, r3) == F(1, 3) and close(1 - (5 / 6) ** 3, 0.4213, 5e-5), 'homework-5.json:items[7] three dice total 10: 27 rolls, 9 with a six, 1/3; unconditional 0.4213')
for n, want in ((6, 5), (10, 8), (100, F(151, 2))):
    rs = list(product(range(1, n + 1), repeat=2))
    check(cmean(max, lambda r: sum(r) == n + 1, rs) == want == F(3 * n + 2, 4), f'{L27}:screens[10] n-sided dice total n+1: E[max] = (3n+2)/4 = {want} at n={n}')
check(cmean(max, lambda r: sum(r) == 11, list(product(range(1, 11), repeat=2))) == 8, f'{L27}:screens[7] test 9: ten-sided dice total 11 give mean larger 8')
check(cond(lambda r: r == (6, 6), lambda r: sum(r) == 12) == 1, f'{L27}:screens[5] total 12 forces (6,6)')
pnl = list(product((-2, -1, 0, 1, 2), repeat=2))
check(sum(1 for r in pnl if sum(r) == 1) == 4 and cond(lambda r: min(r) < 0, lambda r: sum(r) == 1, pnl) == F(1, 2) and cond(lambda r: min(r) < 0, lambda r: sum(r) == 2, pnl) == 0 and 1 - F(3, 5) ** 2 == F(16, 25), f'{L27}:screens[11] two-day P&L: 1/2 given +1, 0 given +2, unconditional 0.64')
check(F(comb(13, 2), 2 * comb(26, 2)) == F(3, 25) and F(comb(13, 2), comb(52, 2)) == F(78, 1326), f'{L27}:quiz[0] both hearts given same colour: 78/650 = 0.12')
check(cond(lambda r: r[0] == r[1], lambda r: sum(r) == 8) == F(1, 5) and cmean(lambda r: r[0], lambda r: sum(r) == 9) == F(9, 2), f'{L27}:quiz[1,2] double given 8: 1/5; first die given 9: 4.5')
check(cmean(min, lambda r: max(r) == 4) == F(16, 7) and cond(lambda r: 6 in r, lambda r: sum(r) >= 10) == F(5, 6) and cmean(sum, lambda r: max(r) == 6) == F(102, 11), 'review-5.json:items[3,4], homework-5 items[6]: 16/7, 5/6, 102/11')
check(run_code_widget(L27, screen(7)) == (9, 9), f'{L27}:screens[7] solution passes all 9 hidden tests')
# dependence after conditioning on a total or a maximum
def joint_indep(gv):
    kept = [r for r in rolls if gv(r)]
    n = len(kept)
    for a in range(1, 7):
        for b in range(1, 7):
            pj = F(sum(1 for r in kept if r == (a, b)), n)
            pa = F(sum(1 for r in kept if r[0] == a), n)
            pb = F(sum(1 for r in kept if r[1] == b), n)
            if pj != pa * pb:
                return False
    return True
check(not joint_indep(lambda r: sum(r) == 7) and not joint_indep(lambda r: max(r) == 5), f'{L27}:summary.ideas[2] the dice are dependent given a total or a maximum')
# given the maximum the other die is not uniform
other = lambda r: r[1] if r[0] == 5 else r[0]  # the die that is not the 5 (5 itself when both are 5)
dist_other_given_max5 = {b: cond(lambda r, b=b: other(r) == b, lambda r: max(r) == 5) for b in range(1, 6)}
check(dist_other_given_max5[5] == F(1, 9) and all(v == F(2, 9) for b, v in dist_other_given_max5.items() if b < 5), f'{L27}:screens[4].explain given max 5 the other die is 5 with 1/9 and each of 1..4 with 2/9: not uniform')

# ======================================================================
# l28 duels and truels
# ======================================================================
L28 = 'l28-duels.json'
duel = lambda pa, pb: F(pa) / (1 - (1 - F(pa)) * (1 - F(pb)))
check(duel(F(1, 3), F(1, 2)) == F(1, 2) and duel(F(1, 4), F(1, 4)) == F(4, 7) and duel(F(1, 2), F(1, 2)) == F(2, 3) and duel(F(1, 3), F(2, 3)) == F(3, 7) and duel(1, F(1, 2)) == 1, f'{L28}:screens[0,5,8] duels 1/2, 4/7, 2/3, 3/7, 1')
check(duel(F(2, 5), F(3, 5)) == F(10, 19) and F(2, 3) * duel(F(1, 2), F(1, 3)) == F(1, 2) and duel(F(1, 5), F(1, 4)) == F(1, 2), f'{L28}:quiz[0,1], review-5 items[5]: 10/19, 1/2 (B first), 1/2')
pa, pb = sp.symbols('p q', positive=True)
even = sp.solve(sp.Eq(pa / (1 - (1 - pa) * (1 - pb)), sp.Rational(1, 2)), pb)
check(sp.simplify(even[0] - pa / (1 - pa)) == 0 and duel(F(1, 4), F(1, 3)) == F(1, 2), f'{L28}:screens[1] the duel is even when q = p/(1-p); q = 1/3 at p = 1/4')
check(duel(F(1, 4), F(1, 4)) == F(4, 7) and duel(F(1, 4), F(1, 2)) < F(1, 2), f'{L28}:screens[1].byKey at q=1/4 A has 4/7; at q=1/2 B is the favourite')
# firing first is an asset: x > p/(p+q) for 0 < p, q < 1
check(all(duel(F(i, 10), F(j, 10)) > F(i, i + j) for i in range(1, 10) for j in range(1, 10)), f'{L28}:screens[1].explain the first move is an asset: x > p/(p+q) for every p, q in (0,1)')

# independent truel solver: full backward induction over who is alive and whose turn,
# each player choosing the target (or the air) that maximises its own survival; A may
# fire into the air only when all three stand (as in the lesson's rules), duels by formula
def truel_values(pa_, pb_, pc_, a_move=None, b_air_allowed=True):
    pa_, pb_, pc_ = F(pa_), F(pb_), F(pc_)
    acc = {'A': pa_, 'B': pb_, 'C': pc_}
    order = ['A', 'B', 'C']
    def duel_val(first, second):
        x = duel(acc[first], acc[second])
        v = {'A': F(0), 'B': F(0), 'C': F(0)}
        v[first] = x; v[second] = 1 - x
        return v
    # three alive, round A, B, C; solve by backward induction with a fixed point for the repeat
    # Let W(turn) = value vector when all three stand and `turn` is about to fire.
    import itertools
    def solve(a_choice):
        # unknowns: W_A, W_B, W_C (3 vectors) -> solve as linear system per candidate pure strategy profile,
        # then check each player's choice is a best response (pure-strategy equilibrium search)
        best = None
        for sa, sb, sc in itertools.product(['air', 'B', 'C'] if a_choice is None else [a_choice], ['air', 'A', 'C'] if b_air_allowed else ['A', 'C'], ['A', 'B']):
            syms = {t: sp.symbols(f'w{t}A w{t}B w{t}C') for t in order}
            eqs = []
            def shoot(t, target, nxt):
                hit = acc[t]
                after_hit = duel_val(nxt if nxt != target else order[(order.index(nxt) + 1) % 3], t) if False else None
                # after a hit, the survivors duel with the next shooter in order firing first
                survivors = [q_ for q_ in order if q_ != target]
                nxt_s = [q_ for q_ in order[order.index(t) + 1:] + order[:order.index(t)] if q_ != target][0]
                other = [q_ for q_ in survivors if q_ != nxt_s][0]
                dv = duel_val(nxt_s, other)
                miss = syms[nxt]
                return [hit * dv[q_] + (1 - hit) * miss[i] for i, q_ in enumerate(order)]
            for t, strat in zip(order, (sa, sb, sc)):
                nxt = order[(order.index(t) + 1) % 3]
                if strat == 'air':
                    val = list(syms[nxt])
                else:
                    val = shoot(t, strat, nxt)
                eqs += [sp.Eq(syms[t][i], val[i]) for i in range(3)]
            sol = sp.solve(eqs, sum((list(s_) for s_ in syms.values()), []))
            W = {t: [F(str(sol[syms[t][i]])) for i in range(3)] for t in order}
            # best-response check for B and C (and A when free)
            def payoff(t, strat, W):
                nxt = order[(order.index(t) + 1) % 3]
                if strat == 'air':
                    return W[nxt][order.index(t)]
                hit = acc[t]
                survivors = [q_ for q_ in order if q_ != strat]
                nxt_s = [q_ for q_ in order[order.index(t) + 1:] + order[:order.index(t)] if q_ != strat][0]
                other = [q_ for q_ in survivors if q_ != nxt_s][0]
                dv = duel_val(nxt_s, other)
                return hit * dv[t] + (1 - hit) * W[nxt][order.index(t)]
            ok = True
            for t, strat, opts in (('B', sb, ['air', 'A', 'C'] if b_air_allowed else ['A', 'C']), ('C', sc, ['A', 'B'])):
                if any(payoff(t, o, W) > payoff(t, strat, W) for o in opts):
                    ok = False
            if a_choice is None and any(payoff('A', o, W) > payoff('A', sa, W) for o in ['air', 'B', 'C']):
                ok = False
            if ok:
                best = (W['A'], sa)
        return best
    return solve(a_move)

W_air, _ = truel_values(F(1, 3), F(2, 3), 1, a_move='air')
W_C, _ = truel_values(F(1, 3), F(2, 3), 1, a_move='C')
W_B, _ = truel_values(F(1, 3), F(2, 3), 1, a_move='B')
check(W_air == [F(25, 63), F(8, 21), F(2, 9)], f'{L28}:screens[2,9], quiz[2], review-5 items[6]: A air: 25/63, 8/21, 2/9 (independent solver)')
check(W_C[0] == F(59, 189) and W_B[0] == F(50, 189), f'{L28}:screens[3,4] A aims at C: 59/189; at B: 50/189')
W_best, move = truel_values(F(1, 3), F(2, 3), 1)
check(move == 'air' and W_best[0] == F(25, 63), f'{L28}:screens[4] firing into the air is A\'s best first move with best play by all')
W2, mv2 = truel_values(F(1, 2), F(2, 3), 1)
W2c, _ = truel_values(F(1, 2), F(2, 3), 1, a_move='C')
check(W2 == [F(17, 30), F(4, 15), F(1, 6)] and mv2 == 'air' and W2c[0] == F(23, 60), f'{L28}:screens[10] A at 1/2: air 17/30 beats aiming at C 23/60')
hw5_tests = {(F(1, 3), F(2, 3)): ([F(25, 63), F(8, 21), F(2, 9)], 'air'), (F(1, 2), F(2, 3)): ([F(17, 30), F(4, 15), F(1, 6)], 'air'),
             (F(1, 2), F(3, 4)): ([F(31, 56), F(9, 28), F(1, 8)], 'air'), (F(1, 3), F(1, 2)): ([F(5, 12), F(1, 4), F(1, 3)], 'air'),
             (F(1, 5), F(1, 4)): ([F(59, 200), F(9, 40), F(12, 25)], 'C'), (F(1, 6), F(1, 4)): ([F(109, 432), F(49, 216), F(25, 48)], 'C')}
for (pa_, pb_), (want, mv) in hw5_tests.items():
    got = truel_values(pa_, pb_, 1)
    check(got == (want, mv), f'homework-5.json:items[0] truel({pa_}, {pb_}, 1) = {want}, {mv} (independent equilibrium solve)')
    # no tie between A's moves
    vals = [truel_values(pa_, pb_, 1, a_move=m)[0][0] for m in ('air', 'B', 'C')]
    check(len(set(vals)) == 3, f'homework-5.json:items[0].how no tie between A\'s moves at ({pa_}, {pb_})')
W_weak_air, _ = truel_values(F(1, 5), F(1, 4), 1, a_move='air')
check(W_weak_air[0] == F(11, 40) and F(59, 200) > F(55, 200), 'homework-5.json:items[4] weak B: air 11/40 = 55/200, aim at C 59/200')
check(F(3, 4) * F(1, 2) == F(3, 8), 'homework-5.json:items[4].explain a hit on C leaves B firing first and A still wins 3/8')
check(sum(W_air) == 1 and sum(truel_values(F(1, 4), F(2, 5), 1)[0]) == 1, 'homework-5.json:items[0] test 7, l28 screens[9]: the three chances add to 1')
check(run_code_widget(L28, screen(7)) == (8, 8), f'{L28}:screens[7] solution passes all 8 hidden tests')
check(run_code_widget('homework-5.json', item(0)) == (7, 7), 'homework-5.json:items[0] solution passes all 7 hidden tests')
# truel_air with p_C = 9/10 (rounds may repeat): independent linear solve
pc9 = F(9, 10)
ends = 1 - (1 - F(2, 3)) * (1 - pc9)
a9 = (F(2, 3) * duel(F(1, 3), F(2, 3)) + F(1, 3) * pc9 * duel(F(1, 3), pc9)) / ends
check(a9 == F(165, 406), f'{L28}:screens[7].explain with p_C = 0.9 A\'s chance is 165/406')
# MC of the truel with A firing into the air once, B -> C, C -> B, then duels
def truel_mc(trials):
    w = {'A': 0, 'B': 0, 'C': 0}
    for _ in range(trials):
        if rng.random() < 2 / 3:  # B hits C; A first vs B
            cur = 'A'
            while True:
                if cur == 'A' and rng.random() < 1 / 3: w['A'] += 1; break
                if cur == 'B' and rng.random() < 2 / 3: w['B'] += 1; break
                cur = 'B' if cur == 'A' else 'A'
        else:  # C kills B; A one shot
            if rng.random() < 1 / 3: w['A'] += 1
            else: w['C'] += 1
    return {k: v / trials for k, v in w.items()}
mc = truel_mc(200_000)
check(close(mc['A'], 25 / 63, 0.004) and close(mc['B'], 8 / 21, 0.004) and close(mc['C'], 2 / 9, 0.004), f'{L28}:screens[9] MC truel ~ 25/63, 8/21, 2/9 (got {mc["A"]:.4f}, {mc["B"]:.4f}, {mc["C"]:.4f})')
# B and C aiming at each other is each one's best response (checked inside truel_values by the equilibrium search)
check(truel_values(F(1, 3), F(2, 3), 1, a_move='air') is not None, f'{L28}:screens[2] B aiming at C and C at B is a best response for each (equilibrium found)')

# ======================================================================
# l29 random chords and envelopes
# ======================================================================
L29 = 'l29-random-chords.json'
d, t = sp.symbols('d theta', positive=True)
chord = 2 * sp.sqrt(1 - d ** 2)
check(sp.solve(sp.Eq(chord, sp.sqrt(3)), d) == [sp.Rational(1, 2)] and sp.solve(sp.Eq(chord, sp.sqrt(2)), d) == [sp.sqrt(2) / 2] and sp.solve(sp.Eq(chord, 1), d) == [sp.sqrt(3) / 2], f'{L29}:screens[6], screens[10], quiz: cut-offs d < 1/2, 1/sqrt2, sqrt3/2')
# endpoints: chord = 2 sin(theta/2) with theta uniform on [0, 2pi); P(chord > L) = share of central angles
ang = lambda L: 2 * sp.asin(sp.Rational(L) / 2 if not isinstance(L, sp.Expr) else L / 2)
share_end = lambda L: sp.simplify((2 * sp.pi - 2 * ang(L)) / (2 * sp.pi))
check(share_end(sp.sqrt(3)) == sp.Rational(1, 3) and share_end(sp.sqrt(2)) == sp.Rational(1, 2) and share_end(1) == sp.Rational(2, 3), f'{L29}:screens[0,10], quiz[1]: endpoints 1/3, 1/2, 2/3')
share_rad = lambda c: c
share_mid = lambda c: c ** 2
check(share_rad(sp.Rational(1, 2)) == sp.Rational(1, 2) and share_mid(sp.Rational(1, 2)) == sp.Rational(1, 4), f'{L29}:screens[1,2] radius 1/2, midpoint 1/4')
check(sp.simplify(share_rad(sp.sqrt(2) / 2) - sp.sqrt(2) / 2) == 0 and share_mid(sp.sqrt(2) / 2) == sp.Rational(1, 2) and close(float(sp.sqrt(2) / 2), 0.7071, 5e-5), f'{L29}:screens[10] sqrt2 threshold: radius 0.7071, midpoint 1/2')
check(close(float(sp.sqrt(3) / 2), 0.866, 5e-4) and share_mid(sp.sqrt(3) / 2) == sp.Rational(3, 4), f'{L29}:quiz[2], review-5 items[8]: radius 0.866, midpoint 3/4 for a chord longer than 1')
# the midpoint density: P(d < r) = r^2, so density 2d
check(sp.integrate(2 * d, (d, 0, sp.Rational(1, 2))) == sp.Rational(1, 4), f'{L29}:screens[7] uniform midpoint has P(d < r) = r^2')
# expected lengths
e_end = sp.integrate(2 * sp.sin(t / 2), (t, 0, 2 * sp.pi)) / (2 * sp.pi)
e_rad = sp.integrate(chord, (d, 0, 1))
e_mid = sp.integrate(chord * 2 * d, (d, 0, 1))
check(sp.simplify(e_end - 4 / sp.pi) == 0 and sp.simplify(e_rad - sp.pi / 2) == 0 and e_mid == sp.Rational(4, 3), f'{L29}:screens[9] expected lengths 4/pi, pi/2, 4/3')
check(close(4 / pi, 1.2732, 5e-5) and close(pi / 2, 1.5708, 5e-5), f'{L29}:screens[9] 1.2732 and 1.5708')
# the radius procedure favours chords near the centre: E[d] smallest
e_d_end = sp.integrate(sp.Abs(sp.cos(t / 2)), (t, 0, 2 * sp.pi)) / (2 * sp.pi)
check(sp.Rational(1, 2) < sp.simplify(e_d_end) and sp.Rational(1, 2) < sp.Rational(2, 3), f'{L29}:screens[9].explain radius procedure has the smallest mean distance from the centre (1/2 vs 2/pi vs 2/3)')
check(close((1 / 3 + 1 / 2 + 1 / 4) / 3, 0.36, 0.002), f'{L29}:screens[3] options[3] the average of the three is about 0.36')
# MC of the three procedures
def chord_mc(method, trials):
    if method == 'endpoints':
        a, b = nrng.uniform(0, 2 * pi, trials), nrng.uniform(0, 2 * pi, trials)
        L = 2 * np.abs(np.sin((a - b) / 2))
    elif method == 'radius':
        L = 2 * np.sqrt(1 - nrng.random(trials) ** 2)
    else:
        dd = np.sqrt(nrng.random(trials))
        L = 2 * np.sqrt(1 - dd ** 2)
    return (L > sqrt(3)).mean(), (L > sqrt(2)).mean(), (L > 1).mean(), L.mean()
for method, want in (('endpoints', (1 / 3, 1 / 2, 2 / 3, 4 / pi)), ('radius', (1 / 2, sqrt(2) / 2, sqrt(3) / 2, pi / 2)), ('midpoint', (1 / 4, 1 / 2, 3 / 4, 4 / 3))):
    got = chord_mc(method, 400_000)
    check(all(close(g_, w_, 0.004) for g_, w_ in zip(got, want)), f'{L29}:screens[8,9,10] MC {method}: shares and mean length match ({", ".join(f"{g_:.4f}" for g_ in got)})')
check(run_code_widget(L29, screen(8)) == (5, 5), f'{L29}:screens[8] solution passes all 5 hidden tests')
# drawing d = U in the midpoint branch gives 1/2 (the radius answer)
check(close((2 * np.sqrt(1 - nrng.random(200_000) ** 2) > sqrt(3)).mean(), 0.5, 0.005), f'{L29}:screens[8].explain d = U in the midpoint branch gives 1/2 again')
# two envelopes: exhaustive over (pair, envelope opened)
def env_cases(pairs_):
    return [(lo, hi, seen, other) for lo, hi in pairs_ for seen, other in ((lo, hi), (hi, lo))]
cases2 = env_cases([(10, 20), (20, 40)])
check(F(sum(c[2] for c in cases2), 4) == F(45, 2) and F(sum(c[3] for c in cases2), 4) == F(45, 2), f'{L29}:screens[5] always keep = always switch = 22.5')
see20 = [c for c in cases2 if c[2] == 20]
check(len(see20) == 2 and F(sum(c[3] for c in see20), 2) == 25, f'{L29}:screens[4] seeing 20: other is 10 or 40, switching worth 25')
cases3 = env_cases([(10, 20), (20, 40), (40, 80)])
val = lambda amt, cs=cases3: F(sum(c[3] for c in cs if c[2] == amt), sum(1 for c in cs if c[2] == amt))
check(val(80) == 40 and val(40) == 50 and val(20) == 25 and val(10) == 20, f'{L29}:screens[6], quiz[0]: at 80 keep (other is 40), at 40 switch for 50')
rule = [c[3] if c[2] != 80 else c[2] for c in cases3]
check(F(sum(rule), 6) == F(125, 3) and F(sum(c[2] for c in cases3), 6) == 35, 'homework-5.json:items[8] switch unless 80: 125/3; always keep 35')
best_rule = [max(c[2], val(c[2])) for c in cases3]
check(F(sum(best_rule), 6) == F(125, 3), 'homework-5.json:items[8].explain the rule is the prior-optimal one (switch at 10, 20, 40; keep at 80)')
cases5 = env_cases([(5, 10), (10, 20), (20, 40)])
check(val(10, cases5) == F(25, 2) and val(40, cases5) == 20, 'review-5.json:items[7] seeing 10: switching worth 12.5; at 40 keep')
check(F(9 * 100 - 500, 10) == 40 and F(9 * 100 + 11 * (-500), 20) == -230, f'{L29}:screens[11] random day 40, random trade -230')

# ======================================================================
# l30 follow-ups
# ======================================================================
L30 = 'l30-follow-ups.json'
emax = lambda n: F((n + 1) * (4 * n - 1), 6 * n)
for n in (1, 6, 10, 20, 100):
    rs = list(product(range(1, n + 1), repeat=2))
    check(F(sum(max(r) for r in rs), n * n) == emax(n), f'{L30}:screens[1,5,6] E[max of two {n}-sided dice] = (n+1)(4n-1)/(6n) (exhaustive)')
check(emax(6) == F(161, 36) and emax(20) == F(553, 40) and emax(10) == F(143, 20) and emax(100) == F(13433, 200) and close(float(emax(100)), 67.165, 5e-4), f'{L30} values 161/36, 553/40, 143/20, 67.165')
check(all(sum(1 for r in product(range(1, 7), repeat=2) if max(r) == m) == 2 * m - 1 for m in range(1, 7)), f'{L30}:screens[0] P(max = m) = (2m-1)/n^2')
m_, n_ = sp.symbols('m n', positive=True, integer=True)
check(sp.simplify(sp.summation(m_ * (2 * m_ - 1), (m_, 1, n_)) / n_ ** 2 - (n_ + 1) * (4 * n_ - 1) / (6 * n_)) == 0, f'{L30}:screens[6] the sum gives (n+1)(4n-1)/(6n)')
check(F(13, 3) != F(161, 36) and F(2 * 1 + 1, 3) == 1 and sp.limit(((n_ + 1) * (4 * n_ - 1) / (6 * n_)) / (2 * n_ / 3), n_, sp.oo) == 1, f'{L30}:screens[4] (2n+1)/3 fails at n=6, passes n=1, has the right growth 2n/3')
check(sp.integrate(x * 2 * x / n_ ** 2, (x, 0, n_)) == 2 * n_ / 3, f'{L30}:screens[4] the larger of two uniforms on [0,n] averages 2n/3')
# reroll game: value iteration (independent of the threshold formula), V = E[max(X, V - c)]
def reroll_vi(faces, c):
    c = F(c); V = F(faces + 1, 2)
    for _ in range(200):
        V = sum(max(F(v), V - c) for v in range(1, faces + 1)) / faces
    return V
def reroll_thresh(faces, c):
    c = F(c)
    return max((sum(range(tt, faces + 1)) - (tt - 1) * c) / (faces - tt + 1) for tt in range(1, faces + 1))
for faces, c, want in ((6, F(1, 2), F(9, 2)), (6, 2, F(18, 5)), (6, 3, F(7, 2)), (6, 1, 4), (6, F(3, 2), F(15, 4)), (6, F(5, 2), F(7, 2)), (6, 10, F(7, 2)), (8, 1, F(11, 2)), (10, 1, 7), (20, 1, F(91, 6))):
    vi = reroll_vi(faces, c)
    check(abs(vi - want) < F(1, 10 ** 9) and reroll_thresh(faces, c) == want, f'{L30}/review-5/homework-5 reroll {faces}-sided at cost {c}: value {want} (value iteration and threshold rules agree)')
check(reroll_thresh(6, F(1, 2)) == (15 - F(3, 2)) / 3 == (11 - 2) / F(2), f'{L30}:screens[2].explain at £0.50 keep 4 or more; a 4 is a tie with keep 5 or more')
# one-step lookahead is not optimal (c = 0.5: keep 3+ is worth 4.25 < 4.5); n - c rule fails at (6, 1)
check((18 - 1) / F(4) == F(17, 4) < F(9, 2), f'{L30}:screens[10] options[2].why one-step lookahead (keep x >= 3.5 - c) is worth 4.25 < 4.5 at c = 0.5')
check((11 - 4 * 1) / F(2) == F(7, 2) < 4, f'{L30}:screens[10] options[3].why keep >= n - c = 5 is worth 3.5 < 4 at (6, 1)')
check(reroll_thresh(6, 1) - 1 == 3 and reroll_thresh(6, F(3, 2)) - F(3, 2) == F(9, 4) and reroll_thresh(8, 1) - 1 == F(9, 2) and close(float(reroll_thresh(20, 1) - 1), 14.17, 0.005), f'{L30}:screens[10], quiz[0], review-5, homework-5: thresholds V - c = 3, 2.25, 4.5, 14.17')
check(run_code_widget(L30, screen(7)) == (11, 11), f'{L30}:screens[7] solution passes all 11 hidden tests')
# k players and runs
altk = lambda pv, k: F(pv) / (1 - (1 - F(pv)) ** k)
check(altk(F(1, 6), 2) == F(6, 11) and altk(F(1, 6), 3) == F(36, 91) and altk(F(1, 2), 3) == F(4, 7) and altk(F(1, 2), 4) == F(8, 15), f'{L30}:screens[3,9], quiz[1]: 6/11, 36/91, 4/7, 8/15')
def run_wait(pv, r):
    # first-step analysis: E_j = expected flips from j heads in a row
    e = sp.symbols(f'e0:{r + 1}')
    eqs = [sp.Eq(e[r], 0)] + [sp.Eq(e[j], 1 + sp.Rational(pv) * e[j + 1] + (1 - sp.Rational(pv)) * e[0]) for j in range(r)]
    return sp.solve(eqs, e)[e[0]]
check(run_wait(F(2, 3), 3) == sp.Rational(57, 8) and run_wait(F(1, 2), 4) == 30 and run_wait(F(1, 2), 3) == 14 and run_wait(F(1, 6), 2) == 42, f'{L30}:screens[9], quiz[2], l24: run waits 57/8, 30, 14, 42 (first-step analysis)')
check(sum(F(3, 2) ** j for j in range(1, 4)) == F(57, 8), f'{L30}:screens[9] hint: run formula 1/p + 1/p^2 + 1/p^3')
H = lambda n: sum(F(1, i) for i in range(1, n + 1))
check(close(float(H(12)), 3.1032, 5e-5) and 6 * H(6) == F(147, 10), f'{L30}:screens[8] H_12 = 3.1032; 6H_6 = 14.7')
check(close(2 * 100 / 3, 66.6667, 5e-5) and close(67.165 - 66.667, 0.5, 0.01), f'{L30}:screens[11] continuous shortcut 66.67 is off by about half a pound')

# ======================================================================
# EXPECTED_FAIL checks (findings 2 and 3): literal readings that are false
# ======================================================================
# Finding 2: l26 screens[3].feedback.correct "74: fair on average and the least noisy".
# The raw maximum (the "60" option) has lower variance than the max-based unbiased
# estimate: Var(m) = (k/(k+1))^2 Var(m + m/k - 1). It is the least noisy of the
# UNBIASED estimates (and the UMVUE), not of the three options.
check(v_max_est <= v_raw_max, f'{L26}:screens[3].feedback.correct EXPECTED_FAIL: the max-based estimate is not less noisy than the raw maximum (Var ratio {float(v_max_est / v_raw_max):.3f}); it is the least noisy UNBIASED one', expected_fail=True)
# corrected assert, ready to enable once the text says "the least noisy of the fair estimates":
# check(v_max_est < v_mean_est and v_raw_max < v_max_est, f'{L26}:screens[3].feedback.correct max-based is the least noisy unbiased estimate; the raw maximum is less noisy but biased')

# Finding 3: l27 summary.ideas[2] "After conditioning on a total or a maximum, the dice
# are no longer independent or uniform." Given a total the first die IS uniform on its
# feasible range (for total 7, uniform on 1..6 exactly as before); only given the
# maximum is the other die non-uniform.
dist_given_7 = {a: cond(lambda r, a=a: r[0] == a, lambda r: sum(r) == 7) for a in range(1, 7)}
check(len(set(dist_given_7.values())) > 1, f'{L27}:summary.ideas[2] EXPECTED_FAIL: given total 7 each die is still uniform on 1..6 ({dict((k, str(v)) for k, v in dist_given_7.items())}); only the maximum makes the other die non-uniform', expected_fail=True)
# corrected assert, ready to enable once the text says "no longer independent; given the maximum the other die is not even uniform":
# check(len(set(dist_given_7.values())) == 1 and len(set(dist_other_given_max5.values())) > 1 and not joint_indep(lambda r: sum(r) == 7), f'{L27}:summary.ideas[2] dependent given a total; non-uniform only given the maximum')

print(f'\n{N_CHECKS} checks run (puzzles L5, round 2); {len(FAILS)} EXPECTED_FAIL')
for f_ in FAILS:
    print('  ', f_)
sys.exit(1 if FAILS else 0)
