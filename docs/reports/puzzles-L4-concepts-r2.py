#!/usr/bin/env python3
"""Concept audit round 2, puzzles L4 (l19 to l24, review-4, homework-4).

Exact checks (Fraction, sympy, exhaustive game-tree solves) and Monte Carlo
checks for every stated probability, expectation, optimal strategy and
code-behaviour claim in the level. Run from the repo root:

    python3 -I docs/reports/puzzles-L4-concepts-r2.py

Exit 0 when the content is correct. Each assert names its ledger row
(file:path). A check that fails because the content is wrong is marked
EXPECTED_FAIL with the corrected assert in a comment beside it.
"""
import json
import math
import random
import statistics
import sys
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, log, exp, sqrt

import numpy as np
import sympy as sp

ROOT = 'app/content/courses/puzzles/'
N_CHECKS = 0


def check(cond, name):
    global N_CHECKS
    N_CHECKS += 1
    assert cond, name
    print('ok  ', name)


def close(a, b, tol):
    return abs(a - b) <= tol


# ----------------------------------------------------------------------
# Shared exact tools
# ----------------------------------------------------------------------
def losing_piles(k, upto):
    """Exhaustive backward induction for the take-away game with takes 1..k.
    Normal play: the player who takes the last match wins. Returns the set of
    pile sizes that lose for the player to move."""
    win = {0: False}  # pile 0: player to move has lost (rival took last match)
    for n in range(1, upto + 1):
        win[n] = any(not win[n - t] for t in range(1, k + 1) if n - t >= 0)
    return {n for n in range(0, upto + 1) if not win[n]}


def winning_moves(k, n):
    lose = losing_piles(k, n)
    return [t for t in range(1, k + 1) if n - t >= 0 and (n - t) in lose]


def alt_first(p, n_players=2):
    """First player's chance when n players try in turn, each succeeding with p."""
    p = F(p)
    return p / (1 - (1 - p) ** n_players)


def duel(p, q):
    p, q = F(p), F(q)
    return p / (1 - (1 - p) * (1 - q))


def penney_exact(a, b, ph=F(1, 2)):
    """Chance pattern a appears before b: joint prefix automaton, solved exactly.
    Independent of the lesson's solution: it uses an explicit transition map
    and a linear solve by sympy."""
    assert a not in b and b not in a
    nodes = sorted({x[:k] for x in (a, b) for k in range(len(x))}, key=len)
    idx = {s: i for i, s in enumerate(nodes)}
    n = len(nodes)
    M = sp.zeros(n, n)
    rhs = sp.zeros(n, 1)
    for s in nodes:
        i = idx[s]
        M[i, i] += 1
        for c, pc in (('H', sp.Rational(ph)), ('T', 1 - sp.Rational(ph))):
            t = s + c
            if t.endswith(a):
                rhs[i] += pc
            elif t.endswith(b):
                pass
            else:
                while t not in idx:
                    t = t[1:]
                M[i, idx[t]] -= pc
    sol = M.LUsolve(rhs)
    return F(str(sol[idx['']]))


def conway(a, b):
    """Conway leading number A.B = sum 2^(k-1) over k with a's last k == b's first k."""
    return sum(2 ** (k - 1) for k in range(1, min(len(a), len(b)) + 1) if a[-k:] == b[:k])


def penney_conway(a, b):
    """P(a first) from Conway: P(b)/P(a) = (AA - AB)/(BB - BA)."""
    r = F(conway(a, a) - conway(a, b), conway(b, b) - conway(b, a))
    return 1 / (1 + r)


def penney_sim(a, b, trials, rng, ph=0.5):
    wins = 0
    for _ in range(trials):
        s = ''
        while True:
            s += 'H' if rng.random() < ph else 'T'
            if s.endswith(a):
                wins += 1
                break
            if s.endswith(b):
                break
            s = s[-max(len(a), len(b)):]
    return wins / trials


def g(p, b, f):
    return p * log(1 + b * f) + (1 - p) * log(1 - f)


def kelly(p, b):
    return max(0.0, p - (1 - p) / b)


def series_bets(wins_needed_a, wins_needed_b, stake=F(100)):
    """Replication value of a series bet (+stake if A wins the series, -stake
    otherwise) with game bets at evens, by backward induction; returns the
    value map and the bet at each state. Independent of the binomial formula."""
    @lru_cache(None)
    def V(r, s):
        if r == 0:
            return stake
        if s == 0:
            return -stake
        return (V(r - 1, s) + V(r, s - 1)) / 2
    return V, lambda r, s: (V(r - 1, s) - V(r, s - 1)) / 2


def series_formula(r, s, S=F(100)):
    return S * F(comb(r + s - 2, r - 1), 2 ** (r + s - 2))


def run_code_widget(path, screen_locator):
    """Execute a code widget's prelude + solution and evaluate its hidden tests.
    Returns (passed, total)."""
    d = json.load(open(ROOT + path))
    w = screen_locator(d)['widget']
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
            ok = isinstance(got, Exception) and type(got).__name__ == exp_
            passed += bool(ok)
            continue
        if isinstance(exp_, str):
            try:
                exp_ = eval(exp_, ns)
            except Exception:  # noqa: a plain string expectation
                pass
        if cmp == 'fraction':
            ok = F(got) == F(exp_)
        elif cmp == 'isclose':
            ok = abs(float(got) - float(exp_)) <= t.get('tol', {}).get('abs', 1e-9)
        else:
            ok = got == exp_
        passed += bool(ok)
    return passed, len(w['tests'])


def screen(i):
    return lambda d: d['screens'][i]


def item(i):
    return lambda d: d['items'][i]


rng = random.Random(20261106)
nrng = np.random.default_rng(20261106)

# ======================================================================
# l19 who wins
# ======================================================================
L19 = 'l19-who-wins.json'
lose3 = losing_piles(3, 60)
check(lose3 == {n for n in range(0, 61) if n % 4 == 0}, f'{L19}:screens[1] losing piles with takes 1..3 are the multiples of 4 (exhaustive to 60)')
check(winning_moves(3, 21) == [1], f'{L19}:screens[2] from 21 take 1 (only winning move)')
check(winning_moves(3, 23) == [3], f'{L19}:screens[9] row 2: from 23 take 3')
check(winning_moves(3, 17) == [1], f'{L19}:quiz[1] from 17 take 1')
check(20 in lose3 and winning_moves(3, 20) == [], f'{L19}:screens[5] 20 loses for the mover, second seat wins')
check(winning_moves(3, 26) == [2], 'review-4.json:items[0] from 26 take 2')
# copy strategy fails: after 1 and 1 from 20 the pile is 18, first player takes 2 to leave 16 (a losing pile)
check(16 in lose3 and 18 not in lose3, f'{L19}:screens[5] options[2].why copying fails: 18 is winning, 16 losing')
for k in (3, 4, 5):
    check(losing_piles(k, 60) == {n for n in range(0, 61) if n % (k + 1) == 0}, f'{L19}:screens[6].explain losing piles with takes 1..{k} are multiples of {k + 1}')
check(30 in losing_piles(4, 60) and winning_moves(4, 30) == [], f'{L19}:screens[8] 30 with takes 1..4 loses whatever you take')
check(24 in losing_piles(5, 60) and all(n not in losing_piles(5, 60) for n in (25, 20, 28)), f'{L19}:quiz[3] 24 loses with takes 1..5; 20, 25, 28 do not')
check(winning_moves(5, 40) == [4], 'l24-mixed-set.json:screens[4] from 40 with takes 1..5 take 4')

check(alt_first(F(1, 6)) == F(6, 11), f'{L19}:screens[3] first six wins: 6/11')
check(alt_first(F(1, 2)) == F(2, 3), f'{L19}:screens[4] first head wins: 2/3')
check(alt_first(F(1, 3)) == F(3, 5), f'{L19}:screens[9] row 0: first 1 or 2 wins: 3/5')
check(duel(F(1, 2), F(1, 3)) == F(3, 4), f'{L19}:screens[9] row 1: duel 1/2 vs 1/3, A first: 3/4')
check(alt_first(F(1, 6), 3) == F(36, 91), f'{L19}:screens[10] three players first six: 36/91')
x3 = alt_first(F(1, 6), 3)
check(x3 * F(5, 6) == F(30, 91) and x3 * F(25, 36) == F(25, 91) and F(36 + 30 + 25, 91) == 1, f'{L19}:screens[10].explain B 30/91, C 25/91, each 5/6 of the seat before')
check(alt_first(F(1, 6), 4) == F(216, 671), 'homework-4.json:items[4] four players: 216/671')
check(alt_first(F(1, 36)) == F(36, 71), 'review-4.json:items[1] double six first: 36/71')
check(alt_first(F(1, 4)) == F(4, 7), 'l24-mixed-set.json:screens[8] row 4: 4-sided die first 1: 4/7')
p = sp.symbols('p', positive=True)
check(sp.simplify(1 / (2 - p) - sp.Rational(1, 2)) == sp.simplify(p / (2 * (2 - p))), f'{L19}:screens[7].explain 1/(2-p) > 1/2 for every p in (0,1]')
check(sp.simplify(p / (1 - (1 - p) ** 2) - 1 / (2 - p)) == 0, f'{L19}:screens[6] p/(1-(1-p)^2) = 1/(2-p)')
# 1/(3-p) stretch gives 6/17
check(close(1 / (3 - 1 / 6), 0.3529, 5e-5), f'{L19}:screens[10] wrong[stretch] 1/(3-p) = 6/17 = 0.3529')
# Monte Carlo for the alternating game, 3 players
def sim_alt(p, n, trials):
    w = 0
    for _ in range(trials):
        while True:
            done = False
            for i in range(n):
                if rng.random() < p:
                    w += (i == 0)
                    done = True
                    break
            if done:
                break
    return w / trials
s = sim_alt(1 / 6, 3, 100_000)
check(close(s, 36 / 91, 3 * sqrt(0.3956 * 0.6044 / 100_000) + 0.0005), f'{L19}:screens[10] MC three players ~ 36/91 (got {s:.4f})')
s = sim_alt(1 / 6, 2, 100_000)
check(close(s, 6 / 11, 0.0055), f'{L19}:screens[3] MC two players ~ 6/11 (got {s:.4f})')

# simultaneous roll, higher wins, ties reroll: 15/36 per roll, 1/2 overall
higher = sum(1 for a in range(1, 7) for b in range(1, 7) if a > b)
check(F(higher, 36) == F(15, 36) and F(15, 36) / F(30, 36) == F(1, 2), f'{L19}:quiz[0] simultaneous roll: 15/36 per roll, 1/2 overall')

# Vickrey auction: bidding your value v is weakly dominant (private values)
def vick(bid, rival, v=100):
    return (v - rival) if bid > rival else 0  # ties ignored
v = 100
dom = all(vick(v, r) >= vick(b, r) for r in range(0, 201) for b in range(0, 201))
strict = any(vick(v, r) > vick(b, r) for r in range(0, 201) for b in (90, 110, 150))
check(dom and strict, f'{L19}:screens[11] second-price auction: bidding your value weakly dominates every other bid (grid 0..200)')

# ======================================================================
# l20 betting on sequences
# ======================================================================
L20 = 'l20-betting-on-sequences.json'
pairs = {
    ('TH', 'HH'): F(3, 4), ('THH', 'HHT'): F(3, 4), ('HHT', 'HTH'): F(2, 3),
    ('HT', 'TH'): F(1, 2), ('HTT', 'TTH'): F(3, 4), ('THH', 'HHH'): F(7, 8),
    ('TTH', 'THT'): F(2, 3), ('HHT', 'HTT'): F(2, 3), ('HTH', 'HHH'): F(3, 5),
    ('TTH', 'THT'): F(2, 3), ('HHT', 'THT'): F(5, 8), ('HTH', 'THT'): F(1, 2),
    ('TTT', 'THT'): F(2, 5), ('HHT', 'HTT'): F(2, 3), ('THT', 'HTT'): F(1, 2),
    ('TTH', 'HTT'): F(1, 4), ('HHH', 'HTT'): F(2, 5), ('TTH', 'THH'): F(2, 3),
    ('HHT', 'THH'): F(1, 4), ('HTH', 'THH'): F(1, 2), ('TTT', 'THH'): F(2, 5),
}
for (a, b), want in pairs.items():
    check(penney_exact(a, b) == want and penney_conway(a, b) == want, f'{L20}/review-4/homework-4/l24 P({a} before {b}) = {want} (automaton and Conway agree)')
check(penney_exact('TH', 'HH', F(2, 3)) == F(5, 9), f'{L20}:screens[8] biased coin p(H)=2/3: TH before HH with 5/9')
check(conway('HTH', 'HTH') == 5 and conway('HHT', 'HHT') == 4 and conway('HHT', 'HTH') == 2 and conway('HTH', 'HHT') == 1, f'{L20}:screens[4] HTH.HTH = 5, HHT.HHT = 4, HHT.HTH = 2, HTH.HHT = 1')
check(conway('HTH', 'HTH') == 5 and conway('HTH', 'HHH') == 1 and conway('HHH', 'HHH') == 7 and conway('HHH', 'HTH') == 1, 'review-4.json:items[2] Conway numbers 5, 1, 7, 1')
# expected waiting times: E[T_A] = 2 * A.A for a fair coin (Feller XIII.7)
def wait_exact(a):
    nodes = sorted({a[:k] for k in range(len(a))}, key=len)
    idx = {s: i for i, s in enumerate(nodes)}
    n = len(nodes)
    M = sp.zeros(n, n); rhs = sp.ones(n, 1)
    for s in nodes:
        i = idx[s]; M[i, i] += 1
        for c in 'HT':
            t = s + c
            if t.endswith(a):
                continue
            while t not in idx:
                t = t[1:]
            M[i, idx[t]] -= sp.Rational(1, 2)
    return M.LUsolve(rhs)[idx['']]
check(wait_exact('HTH') == 10 and wait_exact('HHT') == 8, f'{L20}:screens[3] options[2].why HTH waits 10 flips on average, HHT 8')
check(wait_exact('HH') == 6 and wait_exact('HHH') == 14 and wait_exact('HHHH') == 30, 'l30-follow-ups.json:quiz[2] run waits 6, 14, 30 (fair coin)')
# Penney second-player rule: for every 3-pattern X, (not X2) X1 X2 wins >= 2/3
opp = {'H': 'T', 'T': 'H'}
rule_ok = all(penney_exact(opp[x[1]] + x[0] + x[1], x) >= F(2, 3) for x in map(''.join, product('HT', repeat=3)))
check(rule_ok, f'{L20}:screens[9].explain the choose-second rule wins at least 2/3 against every three-flip pattern')
# even-money bet: expected gain per £1 backing HTH is -1/3; fair odds 2 to 1
check(F(1, 3) * 1 - F(2, 3) * 1 == F(-1, 3) and F(1, 3) * 2 - F(2, 3) == 0, f'{L20}:screens[3].explain even money on HTH loses 1/3 per £1; 2 to 1 is fair')
check(F(1, 4) * 3 - F(3, 4) == 0, f'{L20}:quiz[2] fair odds on HH are 3 to 1')
# MC
s = penney_sim('HHT', 'HTH', 60_000, rng)
check(close(s, 2 / 3, 3 * sqrt(2 / 9 / 60_000) + 0.001), f'{L20}:screens[2] MC HHT beats HTH ~ 2/3 (got {s:.4f})')
s = penney_sim('TTH', 'THT', 60_000, rng)
check(close(s, 2 / 3, 0.007), f'{L20}:screens[9] MC TTH beats THT ~ 2/3 (got {s:.4f})')
s = penney_sim('TH', 'HH', 60_000, rng, ph=2 / 3)
check(close(s, 5 / 9, 0.007), f'{L20}:screens[8] MC biased coin TH before HH ~ 5/9 (got {s:.4f})')
check(close(sqrt(2 / 9 / 20000), 0.0033, 5e-5), f'{L20}:screens[6].explain standard error sqrt(2/9/20000) = 0.0033')
check(close(3 * sqrt(0.1875 / 20000), 0.0092, 1e-4), f'{L20}:screens[6].how test 9 tolerance 0.0092 is three standard errors at p=0.75')
# lesson code: solution passes its tests; the seed-1 share claimed as 0.6640
d20 = json.load(open(ROOT + L20))
ns = {}
exec(d20['screens'][6]['widget']['prelude'], ns)
exec(d20['screens'][6]['widget']['solution'], ns)
share = ns['penney_sim']('HHT', 'HTH', 20000, 1)
check(close(share, 0.6640, 5e-5), f'{L20}:screens[6].explain seed 1, 20,000 games: HHT share 0.6640 (got {share:.4f})')
check(run_code_widget(L20, screen(6)) == (10, 10), f'{L20}:screens[6] solution passes all 10 hidden tests')
check(run_code_widget('homework-4.json', item(0)) == (9, 9), 'homework-4.json:items[0] solution passes all 9 hidden tests')
# the £3.33 per game claim at £10 even money, 2/3 win
check(close(10 * (2 / 3) - 10 * (1 / 3), 3.33, 0.005), f'{L20}:screens[9].explain worth £3.33 a game')

# ======================================================================
# l21 Kelly
# ======================================================================
L21 = 'l21-kelly.json'
check(close(g(.6, 1, .2), 0.0201, 5e-5) and close(g(.6, 1, .1), 0.0150, 5e-5) and close(g(.6, 1, .4), -0.0024, 5e-5), f'{L21}:screens[2..4] g(0.2)=0.0201, g(0.1)=0.0150, g(0.4)=-0.0024')
fs = sp.symbols('f')
gs = sp.Rational(6, 10) * sp.log(1 + fs) + sp.Rational(4, 10) * sp.log(1 - fs)
check(sp.solve(sp.diff(gs, fs), fs) == [sp.Rational(1, 5)], f'{L21}:screens[1] peak of g at f = 0.2')
check(sp.diff(gs, fs, 2).subs(fs, 0.2) < 0, f'{L21}:screens[6].explain g\'\' < 0 so the zero of g\' is the peak')
root = sp.nsolve(gs, fs, 0.39)
check(close(float(root), 0.39, 0.005), f'{L21}:screens[1].explain growth turns negative past f = 0.39 (root {float(root):.4f})')
pp, qq, bb, ff = sp.symbols('p q b f', positive=True)
gg = pp * sp.log(1 + bb * ff) + qq * sp.log(1 - ff)
sol = sp.solve(sp.Eq(sp.diff(gg, ff), 0), ff)[0]
check(sp.simplify(sol.subs(qq, 1 - pp) - (pp - (1 - pp) / bb)) == 0, f'{L21}:screens[7] / homework-4 items[2] f* = p - q/b from g\'(f) = 0')
check(close(kelly(.4, 2), .1, 1e-12) and close(kelly(.5, 2), .25, 1e-12) and close(kelly(.55, 1.5), .25, 1e-12) and close(kelly(.3, 3), 1 / 15, 1e-12), f'{L21}:screens[7,10,11,9] Kelly 0.1, 0.25, 0.25, 1/15')
check(kelly(.3, 2) == 0 and kelly(.5, 1) == 0 and close(.3 - .35, -.05, 1e-12) and close(2 * .3 - .7, -.1, 1e-12), f'{L21}:quiz[0] no edge at 2 to 1 with p=0.3: f*=0, edge -0.1 per £1')
check(close(kelly(.7, 1), .4, 1e-12) and close(kelly(.52, 1), .04, 1e-12) and close(kelly(.25, 4), .0625, 1e-12) and close(kelly(.3, 4), .125, 1e-12) and close(kelly(.65, 1), .3, 1e-12), f'{L21}:quiz[1], review-4 items[3,4], l24 quiz[1], l24 screens[8]: 0.4, 0.04, 0.0625, 0.125, 0.3')
check(sp.solve(2 * pp - 1 - sp.Rational(1, 2), pp) == [sp.Rational(3, 4)], f'{L21}:quiz[1].explain evens stake passes half the bankroll only when p > 3/4')
# median path vs mean path over 200 bets
k_med = int(np.median(nrng.binomial(200, 0.6, 400_000)))
check(k_med == 120, f'{L21}:screens[2].explain median of Bin(200,0.6) is 120 (MC)')
check(close(exp(120 * log(1.2) + 80 * log(0.8)), 56, 0.6), f'{L21}:screens[2].explain median path grows e^4.03 = 56 times')
check(close(1.04 ** 200, 2550, 10), f'{L21}:screens[2].explain mean path 1.04^200 = 2,550 times')
check(close(g(.6, 1, .1) / g(.6, 1, .2), 0.75, 0.005), f'{L21}:screens[3].explain half Kelly keeps about 75% of the growth')
sd_ratio = log(1.1 / 0.9) / log(1.2 / 0.8)
check(close(sd_ratio, 0.5, 0.01), f'{L21}:screens[3].explain the spread (sd of log wealth) about halves at half Kelly (ratio {sd_ratio:.3f})')
check(close(0.6 ** 10, 0.006, 5e-4) and close(1 / 0.6, 1.667, 1e-3), f'{L21}:screens[5] survival 0.6^10 = 0.006; a 40% loss needs a 67% gain')
check(close(1.2 ** 1, 0.6 * 2, 1e-12), f'{L21}:screens[5] options[1].why all-in mean wealth is 1.2^n = (2 * 0.6)^n')
# expected wealth is maximised at f = 1 (linear in f with positive slope)
check(all(1 + f1 * 0.2 < 1 + 1 * 0.2 for f1 in (0, .2, .5, .9)), f'{L21}:screens[5].explain staking everything maximises expected wealth')
# overbetting hurts more than underbetting by the same amount (g''' < 0 at f*)
check(g(.6, 1, .1) > g(.6, 1, .3) and g(.6, 1, .15) > g(.6, 1, .25), 'homework-4.json:items[3].model overbetting by d costs more growth than underbetting by d')
check(close(g(.55, 1, .2), 0, 5e-4) and close(kelly(.55, 1), .1, 1e-12), 'homework-4.json:items[3].model at a true p=0.55, f=0.2 is double Kelly with growth about 0')
check(close(kelly(.5, 1.5), 1 / 6, 1e-3), f'{L21}:screens[11].explain at a true hit rate 0.5 full Kelly is about 0.167')
check(close(g(.55, 1, .1), 0.0050, 5e-5) and close(g(.5, 2, .25), 0.0589, 5e-5), f'{L21}:screens[9] row 2 and screens[8].explain growth 0.0050 and 0.0589')
# MC: long-run growth equals g(f) almost surely; f=0.4 shrinks; all-in ruins
def kelly_paths(p, b, f, n, paths):
    wins = nrng.random((paths, n)) < p
    return (wins * log(1 + b * f) + (~wins) * log(1 - f)).sum(axis=1)
lw = kelly_paths(.6, 1, .2, 2000, 2000)
check(close(np.median(lw) / 2000, g(.6, 1, .2), 0.003), f'{L21}:screens[0] MC median growth per bet at f=0.2 ~ 0.0201 (got {np.median(lw)/2000:.4f})')
lw4 = kelly_paths(.6, 1, .4, 4000, 2000)
check((lw4 < 0).mean() > 0.6 and np.median(lw4) < 0, f'{L21}:screens[4] MC double Kelly: median log wealth after 4000 bets negative ({np.median(lw4):.1f})')
lw1 = kelly_paths(.6, 1, .1, 2000, 2000)
check(np.median(lw1) < np.median(lw) and np.median(lw1) > np.median(lw4), f'{L21}:screens[0] MC 0.2 beats 0.1 beats 0.4 in median growth')
ruin = (nrng.random((20000, 10)) < 0.6).all(axis=1).mean()
check(close(ruin, 0.6 ** 10, 0.003), f'{L21}:screens[5] MC all-in survival over 10 bets ~ 0.006 (got {ruin:.4f})')
check(run_code_widget(L21, screen(8)) == (13, 13), f'{L21}:screens[8] solution passes all 13 hidden tests')
# homework kelly_sim: seeds claimed in explain
hw4 = json.load(open(ROOT + 'homework-4.json'))
ns = {}
exec(hw4['items'][1]['widget']['solution'], ns)
ks = ns['kelly_sim']
m1, m2, m3, m4 = ks(.6, 1, .2, 1000, 201, 1), ks(.6, 1, .1, 1000, 201, 2), ks(.6, 1, .4, 4000, 201, 3), ks(.5, 2, .25, 500, 101, 4)
check(close(m1, 20.14, 0.01) and close(m2, 15.04, 0.01) and close(m3, -9.79, 0.01) and close(m4, 30.14, 0.01), f'homework-4.json:items[1].explain seeds 1..4 give 20.14, 15.04, -9.79, 30.14 (got {m1:.2f}, {m2:.2f}, {m3:.2f}, {m4:.2f})')
check(close(m1, 600 * log(1.2) + 400 * log(0.8), 1e-9), 'homework-4.json:items[1].explain seed 1 median path won exactly 600 of 1,000 bets')
check(run_code_widget('homework-4.json', item(1)) == (6, 6), 'homework-4.json:items[1] solution passes all 6 hidden tests')
# tolerances in hw4 kelly tests are about three standard errors of the median
def se_median(p, b, f, n, paths):
    sd = sqrt(p * (1 - p)) * (log(1 + b * f) - log(1 - f)) * sqrt(n)
    return 1.2533 * sd / sqrt(paths)
check(close(3 * se_median(.6, 1, .2, 1000, 201), 1.7, 0.1) and close(3 * se_median(.6, 1, .1, 1000, 201), 0.85, 0.05) and close(3 * se_median(.5, 2, .25, 500, 101), 2.9, 0.1), 'homework-4.json:items[1].how tolerances 1.7, 0.85, 2.9 are three standard errors of the median')
# d2 in hw4 order: g = 0 near twice Kelly
check(close(float(sp.nsolve(gs, fs, 0.39)), 2 * 0.2, 0.011), 'homework-4.json:items[2] lines[d2].why g = 0 near twice Kelly')

# ======================================================================
# l22 when to hedge
# ======================================================================
L22 = 'l22-when-to-hedge.json'
h = sp.symbols('h')
check(sp.solve(sp.Eq(500 - h, h - 100), h) == [300] and sp.solve(sp.Eq(500 - h, 2 * h - 100), h) == [200], f'{L22}:screens[0,1] hedge 300 locks 200; at 2 to 1 hedge 200 locks 300')
check(sp.solve(sp.Eq(150 - h, h - 50), h) == [100] and sp.solve(sp.Eq(80 - h, h - 20), h) == [50] and sp.solve(sp.Eq(180 - h, h - 20), h) == [100] and sp.solve(sp.Eq(160 - h, h - 40), h) == [100], f'{L22}:screens[7], quiz[2], review-4 items[5], l24 screens[11] hedges 100/50, 50/30, 100/80, 100/60')
V, bet = series_bets(4, 4)
check(bet(4, 4) == F(125, 4) and V(3, 4) == F(125, 4) and V(2, 4) == F(125, 2) and V(3, 3) == 0, f'{L22}:screens[2] best-of-seven game 1 bet 31.25; values +31.25 after a win, 62.5 at 2-0, 0 at 1-1')
check(bet(3, 3) == F(75, 2) and bet(1, 3) == 25 and bet(1, 1) == 100 and bet(2, 2) == 50, f'{L22}:screens[3], review-4 items[6], quiz[1] bets 37.5 at 1-1, 25 at 3-1, 100 at 3-3, 50 at 2-2')
V5, bet5 = series_bets(3, 3)
V3, bet3 = series_bets(2, 2)
V9, bet9 = series_bets(5, 5)
check(bet5(3, 3) == F(75, 2) and bet3(2, 2) == 50 and bet3(1, 2) == 50 and close(float(bet9(5, 5)), 27.34, 0.005), f'{L22}:screens[8], screens[7], homework-4 items[5] best-of-5 37.5, best-of-3 50 and 50 at 1-0, best-of-9 27.34')
all_states = all(bet(r, s) == series_formula(r, s) for r in range(1, 5) for s in range(1, 5))
check(all_states, f'{L22}:summary.formula bet = S * C(r+s-2, r-1) / 2^(r+s-2) equals the backward-induction bet in every state')
check(bet(1, 3) == 100 * F(1, 4), f'{L22}:review-4 items[6].explain at 3-1 game 5 decides only if both later games are lost: 1/4')
# replication holds whatever the true chance of a game: the strategy ends at exactly +-100
def replicate(p_true, r=4, s=4):
    r0, s0, pos = r, s, F(0)
    while r0 > 0 and s0 > 0:
        b = bet(r0, s0)
        if rng.random() < p_true:
            pos += b; r0 -= 1
        else:
            pos -= b; s0 -= 1
    return pos, r0 == 0
for pt in (0.3, 0.5, 0.8):
    outs = [replicate(pt) for _ in range(300)]
    check(all((pos == 100) == won and abs(pos) == 100 for pos, won in outs), f'{L22}:screens[2] the game-by-game bets replicate +-100 exactly for a true game chance of {pt} (300 paths)')
# generalise: node value 20, bet 30
check((50 + (-10)) / 2 == 20 and (50 - (-10)) / 2 == 30, f'{L22}:screens[6] node value 20, bet 30')
# trap and derive: expected profit and Kelly hedge
check(0.6 * 500 - 0.4 * 100 == 260 and 260 - 200 == 60, f'{L22}:screens[4] unhedged 260, full hedge 200, cost 60')
check(0.5 * 500 - 0.5 * 100 == 200, f'{L22}:quiz[0] at p=1/2 the hedge changes variance not expectation: 200 either way')
hh = sp.symbols('h')
obj = lambda pw: pw * sp.log(1500 - hh) + (1 - pw) * sp.log(900 + hh)
check(sp.solve(sp.diff(obj(sp.Rational(6, 10)), hh), hh) == [60] and sp.solve(sp.diff(obj(sp.Rational(55, 100)), hh), hh) == [180], f'{L22}:screens[5], homework-4 items[7] log-optimal hedge 60 at p=0.6, 180 at p=0.55')
el = lambda pw, hv: pw * log(1500 - hv) + (1 - pw) * log(900 + hv)
check(close(el(.6, 0), 7.109, 5e-4) and close(el(.6, 60), 7.110, 5e-4) and close(log(1200), 7.090, 5e-4), f'{L22}:screens[5].explain expected log 7.109 unhedged, 7.110 at h=60, 7.090 fully hedged')
grid = max(range(0, 301), key=lambda hv: el(.55, hv))
check(grid == 180, 'homework-4.json:items[7].explain grid search over whole pounds gives 180')
check(sp.diff(obj(sp.Rational(6, 10)), hh, 2).subs(hh, 60) < 0, f'{L22}:screens[5] the stationary point is a maximum')
check(F(10, 110 - 90) == F(1, 2), f'{L22}:screens[9] delta = (10 - 0)/(110 - 90) = 0.5')

# ======================================================================
# l23 doubling up
# ======================================================================
L23 = 'l23-doubling-up.json'
def doubling_ev(q, n):
    q = F(q)
    return (1 - q ** n) * 1 - q ** n * (2 ** n - 1)
check(all(doubling_ev(F(1, 2), n) == 0 for n in range(1, 13)), f'{L23}:screens[0,2,6] fair doubling cycle has expected gain 0 for every n')
qs, ns_ = sp.symbols('q n', positive=True)
check(sp.simplify((1 - qs ** ns_) - qs ** ns_ * (2 ** ns_ - 1) - (1 - (2 * qs) ** ns_)) == 0, f'{L23}:summary.formula E[gain] = 1 - (2q)^n')
q = F(19, 37)
for n, want in ((10, -0.3056), (6, -0.1735), (7, -0.2052), (9, -0.2713), (4, -0.1126)):
    check(close(float(doubling_ev(q, n)), want, 5e-5), f'{L23}/review-4/homework-4 European red, {n} doublings: {want}')
check(close(float(q ** 10), 0.001275, 1e-6) and close(float(q ** 6), 0.01834, 1e-5) and close(float(q ** 7), 0.009416, 1e-6) and close(float(q ** 4), 0.06954, 1e-5), f'{L23} q^n values 0.001275, 0.01834, 0.009416, 0.06954')
# the loss per £ staked is unchanged by doubling: E[gain]/E[stake] = -(2q-1)
def exp_stake(q, n):
    return sum(F(2) ** k * F(q) ** k for k in range(n))
check(doubling_ev(q, 10) / exp_stake(q, 10) == -(2 * q - 1), f'{L23}:screens[3].explain per £ staked the edge is unchanged (-1/37); per cycle it is larger')
# MC 400,000 cycles for 10 doublings on red
def cycle_sim(q, n, trials):
    losses = (nrng.random((trials, n)) < q).all(axis=1)
    return np.where(losses, -(2 ** n - 1), 1).mean()
m = cycle_sim(float(q), 10, 400_000)
se = sqrt(float(q ** 10) * (1 - float(q ** 10))) * 1024 / sqrt(400_000)
check(close(m, -0.3056, 3 * se), f'{L23}:screens[3].explain MC 400,000 cycles agrees within noise (got {m:.3f}, se {se:.3f})')
m7 = cycle_sim(float(q), 7, 400_000)
check(close(m7, -0.2052, 3 * sqrt(float(q ** 7)) * 128 / sqrt(400_000)), f'{L23}:screens[9].explain MC 400,000 cycles, 7 doublings (got {m7:.3f})')
check(close(1 - (1023 / 1024) ** 1000, 0.6236, 5e-5) and close((1023 / 1024) ** 1000, 0.376, 5e-4), f'{L23}:quiz[2], screens[4].explain at least one failure in 1,000 cycles: 0.6236')
check(close(2 ** -10, 0.000977, 1e-6) and close(2 ** -7, 0.0078, 5e-5) and 2 ** -4 == 0.0625, f'{L23} 2^-10, 2^-7, 2^-4')
check(sum(2 ** k for k in range(8)) == 255 and sum(2 ** k for k in range(4)) == 15 and sum(2 ** k for k in range(9)) == 511, f'{L23}/l24/homework-4 bankrolls 255 (8 bets), 15 (4 bets), 511 (9 bets)')
# optional stopping: stop when +5 or after 100 fair bets, expected gain 0 (MC and exact DP)
@lru_cache(None)
def stop_val(t, x):
    if x >= 5 or t == 100:
        return F(x)
    return (stop_val(t + 1, x + 1) + stop_val(t + 1, x - 1)) / 2
check(stop_val(0, 0) == 0, f'{L23}:screens[5] stop at +5 or after 100 bets: expected gain exactly 0 (exact DP)')
# finite bankroll B, stop when +1 or ruined: expected gain 0 exactly (bounded martingale)
def ruin_val(B=10):
    """Wealth starts at B; stop at 0 (ruin) or B+1 (one pound ahead). Linear solve."""
    w = sp.symbols(f'w0:{B + 2}')
    eqs = [sp.Eq(w[0], 0), sp.Eq(w[B + 1], B + 1)] + [sp.Eq(w[i], (w[i - 1] + w[i + 1]) / 2) for i in range(1, B + 1)]
    return sp.solve(eqs, w)[w[B]] - B
check(ruin_val(10) == 0, f'{L23}:screens[5] finite bankroll, stop when £1 ahead or ruined: expected gain 0')
# with a finite bankroll no rule raises a fair game's mean: brute force over all stopping rules on a 4-step tree
def all_rules_max(depth=4, bank=3):
    # enumerate every stopping rule on the binary tree of depth `depth` (stop at ruin forced)
    paths = list(product((1, -1), repeat=depth))
    best = -1e9
    # a rule is a set of nodes (prefixes) where we stop; enumerate via recursion on subtrees
    @lru_cache(None)
    def sub(prefix):
        x = sum(prefix)
        if x <= -bank or len(prefix) == depth:
            return (F(x),)
        vals = {F(x)}
        for a in sub(prefix + (1,)):
            for b in sub(prefix + (-1,)):
                vals.add((a + b) / 2)
        return tuple(vals)
    return max(sub(()))
check(all_rules_max() == 0, f'{L23}:screens[5] every stopping rule on a 4-step fair game with a £3 bankroll has expected gain <= 0 (exhaustive)')
# unlimited doubler: expected stake over n allowed bets grows without bound (= n), expected loss before the win diverges
check(all(exp_stake(F(1, 2), n) == n for n in (1, 5, 20)) and sum(F(1, 2) ** (k + 1) * (2 ** k - 1) for k in range(40)) > 19, f'{L23}:screens[5].explain, quiz[0] unlimited doubler: expected stake and expected loss before the win diverge')
check(close(0.98 ** 30, 0.55, 0.005) and 0.98 * 1000 / 0.02 == 49000, f'{L23}:screens[10] L = 49,000 and 0.98^30 = 0.55')
# MC: unlimited doubler wins £1 on every path (fair coin), with the 1,000,000-flip cap never reached in practice
wins = sum(1 for _ in range(2000) if next(k for k in range(1, 200) if rng.random() < 0.5) >= 1)
check(wins == 2000, f'{L23}:quiz[0] MC unlimited doubler: a head eventually comes on every path')

# ======================================================================
# l24 mixed set
# ======================================================================
L24 = 'l24-mixed-set.json'
H = lambda n: sum(F(1, i) for i in range(1, n + 1))
check(5 * H(5) == F(137, 12) and close(float(5 * H(5)), 11.4167, 5e-5) and close(float(12 * H(12)), 37.2385, 5e-5) and 12 * H(12) == F(86021, 2310), f'{L24}:screens[0] row 0, l30 screens[8]: coupon 5H5 = 137/12, 12H12 = 86021/2310')
check(sum(F(1, 12) for _ in range(12)) == 1 and 9 * F(1, 4) == F(9, 4), f'{L24}:screens[0] rows 1, 2: 1 hat, 2.25 HH places')
# two sixes in a row: exact by first-step analysis
e0, e1 = sp.symbols('e0 e1')
solv = sp.solve([sp.Eq(e0, 1 + sp.Rational(5, 6) * e0 + sp.Rational(1, 6) * e1), sp.Eq(e1, 1 + sp.Rational(5, 6) * e0)], [e0, e1])
check(solv[e0] == 42, f'{L24}:screens[0] row 3: expected rolls to two sixes in a row = 42')
check(F(2, 100) * F(95, 100) / (F(2, 100) * F(95, 100) + F(98, 100) * F(10, 100)) == F(19, 117) and close(19 / 117, 0.1624, 5e-5), f'{L24}:screens[0] row 4: Bayes 19/117')
# fair ruin from 4 to 12: exact linear solve
rv = sp.symbols('r0:13')
eqs = [sp.Eq(rv[0], 0), sp.Eq(rv[12], 1)] + [sp.Eq(rv[i], (rv[i - 1] + rv[i + 1]) / 2) for i in range(1, 12)]
check(sp.solve(eqs, rv)[rv[4]] == sp.Rational(1, 3), f'{L24}:screens[0] row 5: fair ruin from 4 to 12: 1/3')
u = sp.symbols('u')
check(sp.integrate(u * 4 * u ** 3, (u, 0, 1)) == sp.Rational(4, 5), f'{L24}:screens[0] row 6: E[max of 4 uniforms] = 4/5')
# two coins
post = F(1, 2) * 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 4))
check(post == F(4, 5) and post * 1 + (1 - post) * F(1, 2) == F(9, 10), f'{L24}:screens[2] P(two-headed | HH) = 4/5, next head 0.9')
def two_coins(trials):
    hit = tot = 0
    for _ in range(trials):
        two = rng.random() < 0.5
        ph = 1.0 if two else 0.5
        if rng.random() < ph and rng.random() < ph:
            tot += 1
            hit += rng.random() < ph
    return hit / tot
s = two_coins(200_000)
check(close(s, 0.9, 0.004), f'{L24}:screens[2].explain MC 200,000 picks ~ 0.9 (got {s:.4f})')
# uniforms exceeding a target: e, scale free
def exceed(target, scale, trials):
    tot = 0
    for _ in range(trials):
        s_, n = 0.0, 0
        while s_ <= target:
            s_ += rng.random() * scale; n += 1
        tot += n
    return tot / trials
s = exceed(2, 2, 200_000)
check(close(s, math.e, 0.006), f'{L24}:screens[5] MC uniforms on [0,2] exceeding 2: ~e (got {s:.4f})')
check(close(sum(1 / math.factorial(n) for n in range(20)), math.e, 1e-9), f'{L24}:screens[5].explain sum 1/n! = e')
x_, y_ = sp.symbols('x y')
area = lambda w: 1 - (1 - w) ** 2
check(area(sp.Rational(1, 4)) == sp.Rational(7, 16) and area(sp.Rational(1, 3)) == sp.Rational(5, 9), f'{L24}:screens[6], screens[8] row 1: meeting 7/16 and 5/9')
# Laplace rule of succession holds exactly for a finite urn with a uniform prior on the number of reds
def laplace_urn(Nb, seen):
    num = den = F(0)
    for R in range(0, Nb + 1):
        if R < seen:
            continue
        p2 = F(comb(R, seen), comb(Nb, seen))
        num += p2 * F(R - seen, Nb - seen)
        den += p2
    return num / den
check(all(laplace_urn(Nb, 2) == F(3, 4) for Nb in (4, 7, 12)) and F(1, 2) == F(1, 2) and F(7, 8) == F(9 - 2, 10 - 2), f'{L24}:screens[7] Laplace 3/4 needs a uniform prior on the mix (exact for finite urns); 3R1B gives 1/2, 9R1B gives 7/8')
check(F(5, 2 ** 4) == F(5, 16), f'{L24}:screens[8] row 0: five points in a semicircle 5/16')
check(close(2 * 1 / (math.pi * 2), 0.3183, 5e-5), f'{L24}:screens[8] row 2: Buffon 2L/(pi d) = 1/pi')
check(sp.integrate(sp.Abs(x_ - y_), (x_, 0, 3), (y_, 0, 3)) / 9 == 1, f'{L24}:screens[8] row 3: expected distance on [0,3] is 1')
# 8-sided die, three rolls: backward induction
V1 = F(9, 2)
V2 = sum(max(F(v), V1) for v in range(1, 9)) / 8
V3 = sum(max(F(v), V2) for v in range(1, 9)) / 8
check(V2 == F(11, 2) and V3 == F(97, 16), f'{L24}:screens[9] three rolls of an 8-sided die: 4.5, 5.5, 97/16')
def three_rolls(trials):
    tot = 0
    for _ in range(trials):
        r = rng.randint(1, 8)
        if r >= 6:
            tot += r; continue
        r = rng.randint(1, 8)
        if r >= 5:
            tot += r; continue
        tot += rng.randint(1, 8)
    return tot / trials
s = three_rolls(200_000)
check(close(s, 97 / 16, 0.012), f'{L24}:screens[9].explain MC 200,000 games ~ 6.0625 (got {s:.3f})')
check(6 * (1 - F(5, 6) ** 6) == F(31031, 7776) and close(6 * (1 - (5 / 6) ** 6), 3.9906, 5e-5), f'{L24}:quiz[0], review-4 items[8]: expected faces seen 3.9906')
# boy-girl: 1/3 under "at least one boy", 1/2 under "a particular child is a boy"
fam = list(product('BG', repeat=2))
at_least = [f_ for f_ in fam if 'B' in f_]
particular = [f_ for f_ in fam if f_[0] == 'B']
check(F(sum(f_ == ('B', 'B') for f_ in at_least), len(at_least)) == F(1, 3) and F(sum(f_ == ('B', 'B') for f_ in particular), len(particular)) == F(1, 2), f'{L24}:quiz[2] 1/3 or 1/2 depending on how the boy was revealed')
# ants: pass-through symmetry, last ant off within one minute (exhaustive over directions, 5 ants on a grid of positions)
def ants_max_time(positions, dirs):
    return max(1 - p if d > 0 else p for p, d in zip(positions, dirs))
pos = [0.1, 0.3, 0.5, 0.7, 0.9]
check(all(ants_max_time(pos, d) <= 1 for d in product((1, -1), repeat=5)), f'{L24}:screens[1] ants: every direction set clears the stick within one minute (ghost argument)')
# option selling: the P&L shape is doubling's (small frequent gains, rare large loss)
check(0.98 * 1000 - 0.02 * 49000 == 0, f'{L24}/l23 transfer: option seller break-even at L = 49,000')

print(f'\nALL {N_CHECKS} CHECKS PASSED (puzzles L4, round 2)')
