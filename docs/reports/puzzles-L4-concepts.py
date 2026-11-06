"""Concept checks for puzzles L4 (lessons l19 to l24, review-4, homework-4).

Run from the repo root: python3 -I docs/reports/puzzles-L4-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-puzzles-4-5-ledger.md).
Exact results use fractions, sympy or exhaustive game-tree solves; Monte Carlo uses
seeded numpy with 4-standard-error bands. Content code (the lesson solutions) is run
as written, so code-behaviour claims (seeded simulation figures) are checked literally.
"""
import json
import pathlib
import random
import sys
from fractions import Fraction as F
from itertools import product
from math import comb, exp, log, sqrt

import numpy as np
import sympy as sp
from scipy.optimize import brentq

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / "app" / "content" / "courses" / "puzzles"
rng = np.random.default_rng(20261106)


def load(name):
    with open(COURSE / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


def solution_ns(widget):
    """Run a code widget's prelude and model solution; return the namespace."""
    ns = {}
    exec(widget.get("prelude", ""), ns)
    exec(widget["solution"], ns)
    return ns


def band(p, n, k=4):
    return k * sqrt(p * (1 - p) / n)


# ------------------------------------------------------------------ l19 who wins
def takeaway_losing(k, top):
    """Exhaustive normal-play solve: pile sizes that lose for the mover with takes 1..k."""
    win = [False] * (top + 1)          # win[0] = False: no move, mover has lost
    for n in range(1, top + 1):
        win[n] = any(not win[n - t] for t in range(1, k + 1) if t <= n)
    return {n for n in range(1, top + 1) if not win[n]}


def alt_first(p, players=2):
    return F(1) / (1 - (1 - F(p)) ** players) * F(p)


def check_l19():
    for k in (3, 4, 5):
        lose = takeaway_losing(k, 60)
        assert lose == {n for n in range(1, 61) if n % (k + 1) == 0}, f"l19 screens[6]: losing piles with takes 1..{k} are the multiples of {k + 1}"
    l3 = takeaway_losing(3, 60)
    assert {4, 8, 12} == {n for n in l3 if n <= 12}, "l19 screens[1]: 4, 8, 12 lose for the mover"
    assert 21 - 1 in l3 and 21 - 2 not in l3 and 21 - 3 not in l3, "l19 screens[2]: from 21 only taking 1 leaves a losing pile"
    assert 20 in l3, "l19 screens[5]: 20 loses for the mover, so go second"
    assert 23 - 3 in l3 and 17 - 1 in l3 and 26 - 2 in l3, "l19 screens[9] row 3, quiz[1], review-4 items[0]: take 3 from 23, 1 from 17, 2 from 26"
    l4 = takeaway_losing(4, 60)
    assert 30 in l4 and all(30 - t not in l4 for t in range(1, 5)), "l19 screens[8]: 30 with takes 1..4 loses whatever you take"
    l5 = takeaway_losing(5, 60)
    assert 24 in l5 and not {20, 25, 28} & l5, "l19 quiz[3]: 24 loses with takes 1..5; 20, 25, 28 do not"
    assert 40 - 4 in l5 and all(40 - t not in l5 for t in (1, 2, 3, 5)), "l24 screens[4]: from 40 take 4"
    # alternating first success
    p = sp.symbols("p", positive=True)
    x = sp.solve(sp.Eq(sp.Symbol("x"), p + (1 - p) ** 2 * sp.Symbol("x")), sp.Symbol("x"))[0]
    assert sp.simplify(x - 1 / (2 - p)) == 0, "l19 screens[6], summary: x = 1/(2 - p)"
    assert alt_first(F(1, 6)) == F(6, 11) and alt_first(F(1, 2)) == F(2, 3) and alt_first(F(1, 3)) == F(3, 5), "l19 screens[3], [4], [9]: 6/11, 2/3, 3/5"
    assert alt_first(F(1, 4)) == F(4, 7), "l24 screens[8] row 4: 4-sided die first 1 wins 4/7"
    assert alt_first(F(1, 36)) == F(36, 71), "review-4 items[1]: double six first, 36/71"
    assert alt_first(F(1, 6), 3) == F(36, 91) and alt_first(F(1, 6), 4) == F(216, 671), "l19 screens[10], homework-4 items[4]: 36/91 and 216/671"
    assert F(5, 6) * F(36, 91) == F(30, 91) and F(25, 36) * F(36, 91) == F(25, 91), "l19 screens[10] explain: B, C get 30/91 and 25/91"
    assert alt_first(F(1, 2), 3) == F(4, 7) and alt_first(F(1, 2), 4) == F(8, 15), "l30 screens[9], quiz[1]: 4/7 and 8/15"
    assert abs(1 / (3 - 1 / 6) - 0.3529) < 5e-5, "l19 screens[10] wrong stretch: 1/(3 - p) = 0.3529"
    # duel in the drill: A 1/2, B 1/3, A first
    assert F(1, 2) / (1 - F(1, 2) * F(2, 3)) == F(3, 4), "l19 screens[9] row 2: duel 3/4"
    # Monte Carlo for the multi-player chains (homework-4 items[4] quotes 0.3230 from 200,000 games)
    n = 400_000
    for players, truth in ((2, 6 / 11), (3, 36 / 91), (4, 216 / 671)):
        rolls = rng.integers(1, 7, size=(n, 60 * players))
        first = (rolls == 6).argmax(axis=1)          # every row has a six with overwhelming chance
        got = ((first % players) == 0).mean()
        assert abs(got - truth) < band(truth, n), f"l19/homework-4: {players}-player first-six sim {got:.4f} vs {truth:.4f}"
    assert abs(0.3230 - 216 / 671) < band(216 / 671, 200_000), "homework-4 items[4] explain: quoted 0.3230 lies within noise of 216/671"
    # simultaneous roll, ties re-rolled: 1/2 by exact count
    win = sum(1 for a in range(1, 7) for b in range(1, 7) if a > b)
    tie = 6
    assert F(win, 36 - tie) == F(1, 2) and F(win, 36) == F(15, 36), "l19 quiz[0]: 15/36 per roll, 1/2 once ties re-roll"
    # second-price sealed bid: bidding the value is weakly dominant (private value 100)
    value = 100
    for rival in range(0, 201):
        best = max(payoff for payoff in [(value - rival) if bid > rival else 0 for bid in range(0, 201)])
        mine = (value - rival) if value > rival else 0
        assert mine >= best, f"l19 screens[11]: bidding the value is weakly dominant (rival {rival})"
    print("l19 ok")


# ------------------------------------------------------------------ l20 betting on sequences
def race(a, b, p=F(1, 2)):
    """Exact P(a before b) by first-step analysis on the joint prefix automaton (independent solve)."""
    states = sorted({x[:k] for x in (a, b) for k in range(len(x))}, key=len)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = sp.zeros(n, n)
    rhs = sp.zeros(n, 1)
    for s in states:
        i = idx[s]
        M[i, i] += 1
        for c, pc in (("H", p), ("T", 1 - p)):
            t = s + c
            if t.endswith(a):
                rhs[i] += sp.Rational(pc)
            elif t.endswith(b):
                continue
            else:
                while t not in idx:
                    t = t[1:]
                M[i, idx[t]] -= sp.Rational(pc)
    sol = M.LUsolve(rhs)
    return F(str(sol[idx[""]]))


def wait_time(a):
    """Expected flips until pattern a (fair coin), by absorbing-chain solve."""
    states = [a[:k] for k in range(len(a))]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = sp.eye(n)
    rhs = sp.ones(n, 1)
    for s in states:
        i = idx[s]
        for c in "HT":
            t = s + c
            if t == a:
                continue
            while t not in idx:
                t = t[1:]
            M[i, idx[t]] -= sp.Rational(1, 2)
    return F(str(M.LUsolve(rhs)[idx[""]]))


def conway(a, b):
    return sum(2 ** (k - 1) for k in range(1, min(len(a), len(b)) + 1) if a[-k:] == b[:k])


def conway_odds_b_first(a, b):
    return F(conway(a, a) - conway(a, b), conway(b, b) - conway(b, a))


def check_l20():
    claims = {
        ("HH", "TH"): F(1, 4), ("HHT", "THH"): F(1, 4), ("HHT", "HTH"): F(2, 3), ("HT", "TH"): F(1, 2),
        ("HHH", "THH"): F(1, 8), ("TTH", "HTT"): F(1, 4), ("TTH", "THT"): F(2, 3), ("HHT", "HTT"): F(2, 3),
        ("TTH", "THT"): F(2, 3), ("HHT", "THT"): F(5, 8), ("HTH", "THT"): F(1, 2), ("TTT", "THT"): F(2, 5),
        ("HTH", "HHH"): F(3, 5), ("HHT", "HTT"): F(2, 3), ("THT", "HTT"): F(1, 2), ("TTH", "HTT"): F(1, 4),
        ("HHH", "HTT"): F(2, 5), ("TTH", "THH"): F(2, 3), ("HHT", "THH"): F(1, 4), ("HTH", "THH"): F(1, 2),
        ("TTT", "THH"): F(2, 5),
        ("HTHT", "THTT"): F(9, 14), ("HH", "THT"): F(5, 8), ("HTH", "THTT"): F(3, 4), ("HHH", "TTTT"): F(15, 22),
        ("HHTT", "TTH"): F(3, 8), ("HTHH", "THHH"): F(7, 12),
    }
    for (a, b), want in claims.items():
        got = race(a, b)
        assert got == want, f"l20/review-4/homework-4: P({a} before {b}) = {want}, chain gives {got}"
        assert conway_odds_b_first(a, b) == (1 - want) / want, f"l20 screens[4]: Conway odds for {a} vs {b}"
    assert race("THH", "HHTH") + race("HHTH", "THH") == 1, "homework-4 items[0] test 9: chances add to 1"
    assert conway("HTH", "HTH") == 5 and conway("HHT", "HHT") == 4 and conway("HHT", "HTH") == 2 and conway("HTH", "HHT") == 1, "l20 screens[4]: leading numbers 5, 4, 2, 1"
    assert wait_time("HTH") == 10 and wait_time("HHT") == 8, "l20 screens[3] option c why: HTH waits 10 flips, HHT 8"
    # Penney's rule: opposite of their middle letter, then their first two; wins at least 2/3 for every pattern
    worst = F(1)
    for them in ("".join(t) for t in product("HT", repeat=3)):
        mine = ("T" if them[1] == "H" else "H") + them[:2]
        w = race(mine, them)
        worst = min(worst, w)
        best = max(race(m, them) for m in ("".join(t) for t in product("HT", repeat=3)) if m != them)
        assert w == best, f"l20 screens[9]: the rule's reply {mine} is the best reply to {them}"
    assert worst == F(2, 3), "l20 screens[9] explain: the rule wins at least 2/3 against every pattern"
    assert race("TH", "HH", F(2, 3)) == F(5, 9) and race("HH", "TH", F(2, 3)) == F(4, 9), "l20 screens[8]: biased coin 5/9"
    assert F(2, 3) / F(1, 3) == 2 and F(3, 4) / F(1, 4) == 3, "l20 screens[7] row 2, quiz[2]: fair odds 2 to 1 and 3 to 1"
    assert 10 * F(2, 3) - 10 * F(1, 3) == F(10, 3), "l20 screens[9] explain: worth £3.33 a game"
    # the lesson's code, run as written
    ns = solution_ns(load("l20-betting-on-sequences")["screens"][6]["widget"])
    for (a, b), want in list(claims.items())[:7]:
        assert ns["first_to_appear"](a, b) == want, f"l20 screens[6] solution: {a} vs {b}"
    share = ns["penney_sim"]("HHT", "HTH", 20000, 1)
    assert abs(share - 0.6640) < 5e-5, f"l20 screens[6] explain: seed 1 gives 0.6640 (got {share:.4f})"
    assert abs(sqrt(2 / 9 / 20000) - 0.0033) < 5e-5 and abs(share - 2 / 3) < 0.01, "l20 screens[6] explain and how: standard error 0.0033, within three of 2/3"
    assert abs(ns["penney_sim"]("TH", "HH", 20000, 2) - 0.75) < 0.0092, "l20 screens[6] test 9"
    hw = solution_ns(load("homework-4")["items"][0]["widget"])
    for (a, b), want in claims.items():
        assert hw["first_to_appear"](a, b) == want, f"homework-4 items[0] solution: {a} vs {b}"
    # Monte Carlo on two races
    n = 200_000
    for a, b, truth in (("HHT", "HTH", 2 / 3), ("TTH", "THH", 2 / 3)):
        flips = rng.random((n, 200)) < 0.5
        s = np.where(flips, "H", "T")
        wins = np.zeros(n, dtype=bool)
        done = np.zeros(n, dtype=bool)
        for j in range(2, 200):
            tri = np.char.add(np.char.add(s[:, j - 2], s[:, j - 1]), s[:, j])
            hit_a = (tri == a) & ~done
            hit_b = (tri == b) & ~done
            wins |= hit_a
            done |= hit_a | hit_b
        got = wins.mean()
        assert abs(got - truth) < band(truth, n), f"l20/homework-4 items[8]: {a} beats {b} sim {got:.4f}"
    assert abs(0.6669 - 2 / 3) < band(2 / 3, 100_000), "homework-4 items[8] explain: quoted 0.6669 within noise of 2/3"
    print("l20 ok")


# ------------------------------------------------------------------ l21 Kelly
def g(p, b, f):
    return p * log(1 + b * f) + (1 - p) * log(1 - f)


def kelly(p, b):
    return max(0.0, p - (1 - p) / b)


def check_l21():
    p, b, f = sp.symbols("p b f", positive=True)
    gf = p * sp.log(1 + b * f) + (1 - p) * sp.log(1 - f)
    crit = sp.solve(sp.Eq(sp.diff(gf, f), 0), f)
    assert len(crit) == 1 and sp.simplify(crit[0] - (p - (1 - p) / b)) == 0, "l21 screens[7], homework-4 items[2]: f* = p - q/b"
    assert sp.simplify(sp.diff(gf, f, 2) + p * b ** 2 / (1 + b * f) ** 2 + (1 - p) / (1 - f) ** 2) == 0, "l21 screens[6] explain: g'' < 0"
    for ff, want in ((0.2, 0.0201), (0.1, 0.0150), (0.4, -0.0024)):
        assert abs(g(0.6, 1, ff) - want) < 5e-5, f"l21 screens[2..4]: g({ff}) = {want}"
    assert abs(g(0.6, 1, 0.1) / g(0.6, 1, 0.2) - 0.747) < 5e-3, "l21 screens[3], quiz[2]: half Kelly keeps about three quarters"
    sd = lambda ff: sqrt(0.24) * (log(1 + ff) - log(1 - ff))
    assert abs(sd(0.1) / sd(0.2) - 0.5) < 0.01, "l21 screens[3] explain: the spread of log wealth about halves"
    root = brentq(lambda ff: g(0.6, 1, ff), 0.3, 0.45)
    assert abs(root - 0.39) < 0.005, "l21 screens[1] explain: growth turns negative past f = 0.39"
    assert abs(exp(200 * g(0.6, 1, 0.2)) - 56) < 1, "l21 screens[2] explain: e^4.03 = 56 times over 200 bets"
    assert abs(0.6 ** 10 - 0.006) < 5e-4 and abs(1 / 0.6 - 1.667) < 1e-3, "l21 screens[5]: survive 10 all-in bets 0.006; a 40% loss needs 67%"
    # expected wealth is maximised by staking everything (one bet; and so n bets)
    assert all(1 + 0.2 * f1 < 1 + 0.2 * f2 for f1, f2 in ((0.2, 0.5), (0.5, 1.0))), "l21 screens[5] explain: expected wealth rises with f up to f = 1"
    for pp, bb, want in ((0.4, 2, 0.1), (0.55, 1, 0.1), (0.3, 3, 1 / 15), (0.5, 2, 0.25), (0.55, 1.5, 0.25), (0.5, 1.5, 1 / 6),
                         (0.3, 2, 0.0), (0.7, 1, 0.4), (0.52, 1, 0.04), (0.25, 4, 0.0625), (0.3, 4, 0.125), (0.65, 1, 0.3)):
        assert abs(kelly(pp, bb) - want) < 1e-9, f"l21/l24/review-4: kelly({pp}, {bb}) = {want}"
    assert abs(g(0.55, 1, 0.1) - 0.005) < 5e-5 and abs(g(0.5, 2, 0.25) - 0.0589) < 5e-5, "l21 screens[9], [8] explain"
    assert abs(kelly(0.8, 1) - 0.6) < 1e-12 and kelly(0.8, 1) > 0.5, "l21 quiz[1] explain (finding): a large enough edge stakes more than half (p = 0.8 gives 0.6)"
    assert abs(g(0.55, 1, 0.2)) < 2e-4, "homework-4 items[3] model: at a true 0.55 the stake 0.2 has growth about zero"
    assert g(0.6, 1, 0.1) > g(0.6, 1, 0.3) and abs(g(0.6, 1, 0.3) / g(0.6, 1, 0.1) - 1) < 0.03, "homework-4 items[3] model: half and 1.5x Kelly give nearly the same growth"
    ns = solution_ns(load("l21-kelly")["screens"][8]["widget"])
    for case in load("l21-kelly")["screens"][8]["widget"]["tests"]:
        got = eval(case["call"], dict(ns))
        assert abs(got - float(case["expect"])) < 1e-9, f"l21 screens[8] test {case['call']}"
    # the fixed series on screen 0: same flips, 0.2 ends highest, 0.4 ends below 100
    series = {s["label"]: np.array(s["values"]) for s in load("l21-kelly")["screens"][0]["canvas"]["params"]["series"]}
    signs = {k: np.sign(np.diff(v)) for k, v in series.items()}
    keys = list(series)
    assert all((signs[keys[0]] == signs[k]).all() for k in keys[1:]), "l21 screens[0] prose: the three bettors back the same flips"
    finals = {k: v[-1] for k, v in series.items()}
    f02 = [k for k in keys if "0.2" in k][0]
    f04 = [k for k in keys if "0.4" in k][0]
    assert finals[f02] == max(finals.values()) and finals[f04] < 100, f"l21 screens[0] explain: 0.2 line ends highest, 0.4 line ends below 100 ({finals})"
    # long-run growth by simulation: mean log step and the median path
    n, bets = 20_000, 1_000
    wins = rng.random((n, bets)) < 0.6
    for ff in (0.1, 0.2, 0.4):
        steps = np.where(wins, log(1 + ff), log(1 - ff))
        finals = steps.sum(axis=1)
        se = steps.std() * sqrt(bets) / sqrt(n)
        assert abs(finals.mean() - bets * g(0.6, 1, ff)) < 4 * se, f"l21 screens[1]: mean log wealth tracks n g(f) at f = {ff}"
    steps = np.where(wins, log(1.4), log(0.6)).sum(axis=1)
    assert np.median(steps) < 0, "l21 screens[4]: double Kelly shrinks the typical bankroll"
    # homework-4 kelly_sim: run as written with the quoted seeds
    hw = solution_ns(load("homework-4")["items"][1]["widget"])
    ks = hw["kelly_sim"]
    assert abs(ks(0.6, 1, 0.2, 1000, 201, 1) - 20.1355) < 5e-4 and abs(ks(0.6, 1, 0.1, 1000, 201, 2) - 15.0419) < 5e-4, "homework-4 items[1] explain: seeds 1 and 2 give n g(f) exactly"
    assert abs(ks(0.6, 1, 0.4, 4000, 201, 3) - (-9.79)) < 5e-3, "homework-4 items[1] explain: seed 3 gives -9.79"
    assert abs(ks(0.5, 2, 0.25, 500, 101, 4) - 30.14) < 5e-3 and abs(500 * g(0.5, 2, 0.25) - 29.45) < 5e-3, "homework-4 items[1] explain: seed 4 gives 30.14 against 29.45"
    # l21 screens[2] explain: e^{n g} is the typical (median) path; expected wealth is 1.04^n (finding 5)
    n200 = 200
    pmf = [F(comb(n200, k)) * F(3, 5) ** k * F(2, 5) ** (n200 - k) for k in range(n200 + 1)]
    cdf = 0
    for k, pk in enumerate(pmf):
        cdf += pk
        if cdf >= F(1, 2):
            med_wealth = F(6, 5) ** k * F(4, 5) ** (n200 - k)
            break
    assert k == 120 and abs(float(med_wealth) / exp(n200 * g(0.6, 1, 0.2)) - 1) < 1e-9 and abs(float(med_wealth) - 56) < 1, "l21 screens[2] explain: the median 200-bet wealth (120 wins) is e^{200 g}, about 56"
    mean_wealth = sum(pk * F(6, 5) ** k * F(4, 5) ** (n200 - k) for k, pk in enumerate(pmf))
    assert mean_wealth == F(26, 25) ** n200 and float(mean_wealth) > 2500, "l21 screens[2] explain (finding 5): expected wealth is exactly 1.04^200, about 2,540 times, far above 56"
    # homework-4 items[3] model: overbetting hurts more than underbetting by the same amount
    for d in np.linspace(0.01, 0.2, 20):
        assert g(0.6, 1, 0.2 - d) >= g(0.6, 1, 0.2 + d) - 1e-12, f"homework-4 items[3] model: g(f* - d) >= g(f* + d) at d = {d:.2f}"
    assert g(0.6, 1, 0.0) == 0 > g(0.6, 1, 0.41), "homework-4 items[3] model: underbetting never turns growth negative, overbetting past 2 f* does"
    # homework-4 items[1] how: the tolerances are three standard errors of a sample median, 1.2533 sigma / sqrt(paths)
    for pp, bb, ff, bets_, paths_, tol in ((0.6, 1, 0.2, 1000, 201, 1.7), (0.6, 1, 0.1, 1000, 201, 0.85), (0.5, 2, 0.25, 500, 101, 2.9)):
        sigma = sqrt(bets_ * pp * (1 - pp)) * (log(1 + bb * ff) - log(1 - ff))
        assert abs(3 * 1.2533 * sigma / sqrt(paths_) - tol) < 0.06, f"homework-4 items[1] how: tolerance {tol} is three standard errors of the median"
    # median of the exact binomial final is n g(f) when np is an integer
    med_k = 600
    assert abs(med_k * log(1.2) + 400 * log(0.8) - 1000 * g(0.6, 1, 0.2)) < 1e-9, "homework-4 items[1] explain: the median path wins 600 of 1,000"
    print("l21 ok")


# ------------------------------------------------------------------ l22 when to hedge
def series_bet(r, s, stake=F(100)):
    """Bet on the next game that replicates +-stake on the series, by backward induction at evens."""
    memo = {}

    def value(r_, s_):
        if r_ == 0:
            return stake
        if s_ == 0:
            return -stake
        if (r_, s_) not in memo:
            memo[(r_, s_)] = (value(r_ - 1, s_) + value(r_, s_ - 1)) / 2
        return memo[(r_, s_)]

    return (value(r - 1, s) - value(r, s - 1)) / 2


def check_l22():
    for win, lose, price, h, locked in ((500, 100, 1, 300, 200), (500, 100, 2, 200, 300), (150, 50, 1, 100, 50),
                                        (80, 20, 1, 50, 30), (160, 40, 1, 100, 60), (180, 20, 1, 100, 80)):
        hh = F(win + lose, 1 + price)
        assert hh == h and win - hh == price * hh - lose == locked, f"l22/l24/review-4 hedge: win {win} lose {lose} at {price} to 1 -> hedge {h}, lock {locked}"
    for r, s, want in ((4, 4, F(125, 4)), (3, 3, F(75, 2)), (2, 2, 50), (3, 3, F(75, 2)), (2, 2, 50), (1, 2, 50), (1, 1, 100),
                       (5, 5, F(2734375, 100000)), (1, 3, 25), (3, 4, None)):
        got = series_bet(r, s)
        formula = 100 * F(comb(r + s - 2, r - 1), 2 ** (r + s - 2))
        assert got == formula, f"l22 summary formula: bet at r={r}, s={s} equals stake x C(r+s-2, r-1)/2^(r+s-2)"
        if want is not None:
            assert got == want, f"l22/review-4/homework-4: bet at r={r}, s={s} is {want} (got {got})"
    assert abs(float(series_bet(5, 5)) - 27.34) < 5e-3, "homework-4 items[5]: best-of-nine game 1 bet 27.34"
    # the series bets replicate exactly along every path of a best-of-seven
    for path in product((1, 0), repeat=7):
        r = s = 4
        pnl = F(0)
        for gwin in path:
            if r == 0 or s == 0:
                break
            bet = series_bet(r, s)
            pnl += bet if gwin else -bet
            if gwin:
                r -= 1
            else:
                s -= 1
        assert pnl == (100 if r == 0 else -100), "l22 screens[2]: game-by-game bets at evens replicate the series bet exactly"
    assert series_bet(4, 4) == F(100 * comb(6, 3), 64) and F(100, 7) != series_bet(4, 4), "l22 screens[2] explain and wrong 'seventh'"
    # belief 0.6: expected profit 260 against 200 locked
    assert 0.6 * 500 - 0.4 * 100 == 260 and 260 - 200 == 60, "l22 screens[4]: full hedge costs £60 of expectation"
    h = sp.symbols("h")
    obj = lambda pw: pw * sp.log(1500 - h) + (1 - pw) * sp.log(900 + h)
    assert sp.solve(sp.diff(obj(sp.Rational(3, 5)), h), h) == [60], "l22 screens[5]: Kelly hedge £60 at p = 0.6"
    assert sp.solve(sp.diff(obj(sp.Rational(11, 20)), h), h) == [180], "homework-4 items[7]: Kelly hedge £180 at p = 0.55"
    grid = np.arange(0, 601)
    val = 0.55 * np.log(1500 - grid) + 0.45 * np.log(900 + grid)
    assert grid[val.argmax()] == 180, "homework-4 items[7] explain: a grid search over whole pounds agrees"
    el = lambda hh: 0.6 * log(1500 - hh) + 0.4 * log(900 + hh)
    assert abs(el(0) - 7.109) < 5e-4 and abs(el(60) - 7.110) < 5e-4 and abs(log(1200) - 7.090) < 5e-4, "l22 screens[5] explain: 7.109, 7.110, 7.090"
    assert el(60) > el(0) > log(1200), "l22 screens[5] d1 why: the full hedge has the lowest expected log"
    assert F(50 - (-10), 2) == 30 and F(50 + (-10), 2) == 20, "l22 screens[6]: bet 30, node worth 20"
    assert F(10, 20) == F(1, 2), "l22 screens[9]: delta 0.5"
    assert 0.5 * 500 - 0.5 * 100 == 200, "l22 quiz[0]: a fair hedge leaves the expectation at £200"
    print("l22 ok")


# ------------------------------------------------------------------ l23 doubling up
def cycle_ev(q, n):
    return (1 - q ** n) - q ** n * (2 ** n - 1)


def check_l23():
    q = F(19, 37)
    for n_, want in ((3, 0), (10, 0), (6, 0), (4, 0), (8, 0)):
        assert cycle_ev(F(1, 2), n_) == want, f"l23/l24 screens[3]: fair cycle of {n_} bets has expectation 0"
    qn = sp.symbols("q n", positive=True)
    assert sp.simplify((1 - qn[0] ** qn[1]) - qn[0] ** qn[1] * (2 ** qn[1] - 1) - (1 - (2 * qn[0]) ** qn[1])) == 0, "l23 summary formula: 1 - (2q)^n"
    for n_, want in ((10, -0.3056), (7, -0.2052), (6, -0.1735), (4, -0.1126), (9, -0.2713)):
        got = float(cycle_ev(q, n_))
        assert abs(got - want) < 5e-4, f"l23/review-4/homework-4: European red cycle of {n_} bets {want} (exact {got:.5f})"
    assert abs(float(q ** 10) - 0.001275) < 5e-7 and abs(float(q ** 7) - 0.009416) < 5e-7 and abs(float(q ** 6) - 0.01834) < 5e-6 and abs(float(q ** 4) - 0.06954) < 5e-6, "l23 hints: q^n values"
    assert abs(1 - (1023 / 1024) ** 1000 - 0.6236) < 5e-5 and abs((1023 / 1024) ** 1000 - 0.376) < 5e-4, "l23 screens[4], quiz[2]: at least one disaster in 1,000 cycles 0.6236"
    assert abs(18 / 37 - 19 / 37 - (-0.027)) < 5e-4, "l23 screens[3] wrong 'one': edge on one £1 bet -0.027"
    assert 1 + 2 + 4 + 8 == 15 and F(1, 16) == F(1, 2) ** 4 and 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 == 255, "l23 quiz[1], l24 screens[3]: £15 funds four bets, £255 eight"
    assert 2 ** 9 - 1 == 511 and 2 ** 9 == 512 <= 500 * 2 and 256 <= 500 < 512, "homework-4 items[6]: table max £500 stops the doubling at £256, nine bets"
    assert abs(0.98 ** 30 - 0.55) < 5e-3 and 0.98 * 1000 / 0.02 == 49000, "l23 screens[10]: L = 49,000; 30 good months 0.55"
    # 'product stays 1' (finding): chance x size is 1 - 2^-n, which equals the chance of the £1 win
    for n_ in (3, 7, 10):
        assert F(1, 2 ** n_) * (2 ** n_ - 1) == 1 - F(1, 2 ** n_) != 1, "l23 screens[6] byKey d1 (finding): the product is 1 - 2^-n, not 1"
    # Monte Carlo: 400,000 cycles on red, ten and seven doublings (the lesson says the sim agrees within noise)
    for n_, want in ((10, -0.3056), (7, -0.2052)):
        trials = 400_000
        spins = rng.random((trials, n_)) < 18 / 37
        first_win = spins.argmax(axis=1)
        any_win = spins.any(axis=1)
        gain = np.where(any_win, 1.0, -(2.0 ** n_ - 1))
        se = gain.std() / sqrt(trials)
        assert abs(gain.mean() - want) < 4 * se, f"l23 screens[3], [9] explain: 400,000-cycle sim {gain.mean():.4f} vs {want}"
    # optional stopping: (a) bounded time, stop at +5 or 100 bets: exact DP gives 0
    probs = {0: F(1)}
    stopped = F(0)
    for t in range(100):
        nxt = {}
        for xpos, pr in probs.items():
            for d in (1, -1):
                y = xpos + d
                if y == 5:
                    stopped += pr / 2 * 5
                else:
                    nxt[y] = nxt.get(y, F(0)) + pr / 2
        probs = nxt
    assert stopped + sum(xpos * pr for xpos, pr in probs.items()) == 0, "l23 screens[5]: stop at +£5 or after 100 bets has expected gain 0"
    # (b) finite bankroll alone is not enough (finding): stop only at ruin, fair £1 bets from £7
    trials, block, blocks = 4_000, 10_000, 10
    T = block * blocks
    wealth = np.full(trials, 7, dtype=np.int64)
    ruined = np.zeros(trials, dtype=bool)
    for _ in range(blocks):
        path = wealth[:, None] + rng.choice(np.array([-1, 1], dtype=np.int8), size=(trials, block)).cumsum(axis=1)
        ruined |= (path <= 0).any(axis=1)
        wealth = path[:, -1]
    assert ruined.mean() > 0.97, f"l23 screens[5] (finding): from £7 the ruin rule ends within {T} bets almost always ({ruined.mean():.3f})"
    # on the paths that stopped, X_tau = 0 exactly; the martingale mass B sits on the vanishing set of unstopped paths
    unstopped_mean = wealth[~ruined].mean() * (~ruined).mean() if (~ruined).any() else 0.0
    assert abs(unstopped_mean - 7) < 1.0, "l23 screens[5] (finding): E[X_T; not yet ruined] stays near £7 while the stopped wealth is 0, so E[X_tau] = 0 < X_0"
    # (c) unlimited doubler: the expected stake diverges
    partial = sum(F(1, 2 ** k) * (2 ** k - 1) for k in range(1, 41))
    assert partial > 39, "l23 screens[5] explain, quiz[0]: the expected stake of the unlimited doubler is infinite (partial sums grow without bound)"
    print("l23 ok")


# ------------------------------------------------------------------ l24 mixed set
def check_l24():
    H = lambda n: sum(F(1, k) for k in range(1, n + 1))
    assert 5 * H(5) == F(137, 12) and abs(float(5 * H(5)) - 11.4167) < 5e-5, "l24 screens[0] row 1: 5 H_5"
    assert 12 * F(1, 12) == 1 and 9 * F(1, 4) == F(9, 4), "l24 screens[0] rows 2, 3"
    # two sixes in a row: absorbing chain
    E = sp.symbols("E0 E1")
    sol = sp.solve([sp.Eq(E[0], 1 + sp.Rational(5, 6) * E[0] + sp.Rational(1, 6) * E[1]), sp.Eq(E[1], 1 + sp.Rational(5, 6) * E[0])], E)
    assert sol[E[0]] == 42, "l24 screens[0] row 4: 6 + 36 = 42"
    assert F(2, 100) * F(95, 100) / (F(2, 100) * F(95, 100) + F(98, 100) * F(10, 100)) == F(19, 117), "l24 screens[0] row 5: 19/117"
    # fair ruin from 4 to 12: linear solve
    A = sp.zeros(11, 11)
    rhs = sp.zeros(11, 1)
    for i in range(1, 12):
        A[i - 1, i - 1] = 1
        if i - 1 >= 1:
            A[i - 1, i - 2] = -sp.Rational(1, 2)
        if i + 1 <= 11:
            A[i - 1, i] = -sp.Rational(1, 2)
        else:
            rhs[i - 1] = sp.Rational(1, 2)
    assert A.LUsolve(rhs)[3] == sp.Rational(1, 3), "l24 screens[0] row 6: reach £12 from £4 with 1/3"
    assert sp.integrate(4 * sp.Symbol("x") ** 4, (sp.Symbol("x"), 0, 1)) == sp.Rational(4, 5), "l24 screens[0] row 7: E[max of 4 uniforms] = 4/5"
    # ants: reflections equal pass-through, so every ant is off within 1 minute
    for _ in range(200):
        pos = list(np.sort(rng.random(5)))
        vel = list(rng.choice([-1.0, 1.0], size=5))
        t = 0.0
        while pos:
            exits = [((1 - x) if v > 0 else x) for x, v in zip(pos, vel)]
            cols = [((pos[i + 1] - pos[i]) / 2, i) for i in range(len(pos) - 1) if vel[i] > 0 and vel[i + 1] < 0]
            dt = min(exits + [c for c, _ in cols])
            pos = [x + v * dt for x, v in zip(pos, vel)]
            t += dt
            for c, i in cols:
                if abs(c - dt) < 1e-12:
                    vel[i], vel[i + 1] = -1.0, 1.0
            keep = [k for k in range(len(pos)) if 1e-12 < pos[k] < 1 - 1e-12]
            pos = [pos[k] for k in keep]
            vel = [vel[k] for k in keep]
        assert t <= 1 + 1e-9, "l24 screens[1]: with reflections every ant is off within one minute"
    # two coins
    post = F(1, 2) * 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 4))
    assert post == F(4, 5) and post + (1 - post) * F(1, 2) == F(9, 10), "l24 screens[2]: posterior 4/5, next head 0.9"
    n = 200_000
    coin = rng.random(n) < 0.5
    flips = rng.random((n, 3)) < np.where(coin, 1.0, 0.5)[:, None]
    hh = flips[:, 0] & flips[:, 1]
    got = flips[hh, 2].mean()
    assert abs(got - 0.9) < band(0.9, hh.sum()), f"l24 screens[2] explain: sim {got:.4f} vs 0.9"
    assert abs(0.9001 - 0.9) < band(0.9, 125_000), "l24 screens[2] explain: quoted 0.9001 within noise"
    # uniforms exceeding a target: e, by exact series and by simulation on [0, 2]
    assert abs((sum(sp.Rational(1, sp.factorial(k)) for k in range(60)) - sp.E).evalf(50)) < 1e-30, "l24 screens[5]: sum 1/n! = e"
    draws = rng.random((n, 30)) * 2
    count = (draws.cumsum(axis=1) <= 2).sum(axis=1) + 1
    se = count.std() / sqrt(n)
    assert abs(count.mean() - exp(1)) < 4 * se, f"l24 screens[5] explain: sim {count.mean():.4f} vs e"
    assert abs(2.7185 - exp(1)) < 4 * sqrt(3 * exp(1) - exp(2)) / sqrt(200_000), "l24 screens[5] explain: quoted 2.7185 within noise"
    x, y = sp.symbols("x y")
    meet = lambda w: 1 - (1 - w) ** 2
    assert meet(sp.Rational(1, 4)) == sp.Rational(7, 16) and meet(sp.Rational(1, 3)) == sp.Rational(5, 9), "l24 screens[6], [8] row 2: meeting 7/16 and 5/9"
    assert sp.integrate(sp.integrate(sp.Piecewise((1, sp.Abs(x - y) <= sp.Rational(1, 4)), (0, True)), (y, 0, 1)), (x, 0, 1)) == sp.Rational(7, 16), "l24 screens[6]: band area by integration"
    # Laplace's rule after two reds gives 3/4, not 2/3 (finding on l24 screens[7] option c)
    pp = sp.symbols("p")
    assert sp.integrate(pp ** 3, (pp, 0, 1)) / sp.integrate(pp ** 2, (pp, 0, 1)) == sp.Rational(3, 4), "l24 screens[7] option c (finding): Laplace's rule (n+1)/(n+2) at n = 2 is 3/4"
    for N in (3, 4, 6, 10, 25):
        num = den = F(0)
        for R in range(N + 1):                         # uniform prior on the number of reds
            if R < 2:
                continue
            p_rr = F(R, N) * F(R - 1, N - 1)
            den += p_rr
            if R >= 3:
                num += p_rr * F(R - 2, N - 2)
        assert num / den == F(3, 4), f"l24 screens[7] option c (finding): finite urn of {N} with a flat prior also gives 3/4"
    assert F(1, 2) == F(3 - 2, 4 - 2) and F(7, 8) == F(9 - 2, 10 - 2), "l24 screens[7] explain: 1/2 with 3 red 1 blue; 7/8 with 9 red 1 blue"
    assert F(5, 16) == F(5, 2 ** 4) and abs(2 / (2 * sp.pi) - 1 / sp.pi) == 0 and F(3, 3) == 1, "l24 screens[8] rows 1, 3, 4"
    pts = rng.random((n, 5)) * 2 * np.pi
    srt = np.sort(pts, axis=1)
    gaps = np.diff(np.concatenate([srt, srt[:, :1] + 2 * np.pi], axis=1), axis=1)
    got = (gaps.max(axis=1) >= np.pi).mean()
    assert abs(got - 5 / 16) < band(5 / 16, n), f"l24 screens[8] row 1: five points in a semicircle sim {got:.4f}"
    theta = rng.random(n) * np.pi
    dist = rng.random(n)                                 # centre to nearest line, lines 2 apart, needle length 1
    got = (dist < 0.5 * np.sin(theta)).mean()
    assert abs(got - 1 / np.pi) < band(1 / np.pi, n), f"l24 screens[8] row 3: Buffon sim {got:.4f}"
    # 8-sided die, three rolls: backward induction and simulation
    v1 = F(9, 2)
    v2 = sum(max(F(k), v1) for k in range(1, 9)) / 8
    v3 = sum(max(F(k), v2) for k in range(1, 9)) / 8
    assert v2 == F(11, 2) and v3 == F(97, 16), "l24 screens[9]: 4.5, 5.5, 97/16"
    rolls = rng.integers(1, 9, size=(n, 3))
    pay = np.where(rolls[:, 0] >= 6, rolls[:, 0], np.where(rolls[:, 1] >= 5, rolls[:, 1], rolls[:, 2]))
    se = pay.std() / sqrt(n)
    assert abs(pay.mean() - 97 / 16) < 4 * se, f"l24 screens[9] explain: sim {pay.mean():.4f} vs 6.0625"
    assert abs(6.058 - 97 / 16) < 4 * se, "l24 screens[9] explain: quoted 6.058 within noise"
    assert abs(6 * (1 - (5 / 6) ** 6) - 3.9906) < 5e-5, "l24 quiz[0], review-4 items[8]: 3.9906 faces"
    # boy-girl under the two protocols
    fams = [(a, b) for a in "BG" for b in "BG"]
    at_least = [f for f in fams if "B" in f]
    assert F(sum(f == ("B", "B") for f in at_least), len(at_least)) == F(1, 3), "l24 quiz[2] option c: 'at least one boy' gives 1/3"
    seen = [(f, i) for f in fams for i in (0, 1) if f[i] == "B"]            # a random child seen to be a boy
    assert F(sum(f == ("B", "B") for f, _ in seen), len(seen)) == F(1, 2), "l24 quiz[2] option b: a particular child seen gives 1/2"
    print("l24 ok")


# ------------------------------------------------------------------ content claims (the findings)
def check_content_claims():
    """Read the content and assert what it says agrees with the checks above.
    These stay failing until the fix pass lands (audit-puzzles-4-5.md findings 1 to 5)."""
    failures = []

    def expect(cond, msg):
        if not cond:
            failures.append(msg)

    l23 = load("l23-doubling-up")
    prose = l23["screens"][5]["prose"]
    expect(not ("finite bankroll" in prose and "no rule for when to stop changes" in prose),
           "finding 1: l23 screens[5].prose states optional stopping with 'finite bankroll' as the hypothesis; equality needs a bounded number of bets (the ruin rule from £7 has E[X_tau] = 0)")
    expect("no stopping rule changes" not in l23["summary"]["ideas"][1],
           "finding 1: l23 summary.ideas[1] repeats the finite-bankroll version")
    l24 = load("l24-mixed-set")
    expect("bankroll finite" not in l24["screens"][3]["hints"][0]["text"],
           "finding 1: l24 screens[3] hints reason from a finite bankroll; the cycle is bounded (eight bets), which is the hypothesis that applies")
    expect("product stays 1" not in l23["screens"][6]["feedback"]["byKey"]["d1"],
           "finding 2: l23 screens[6] byKey d1 says the product stays 1; it is 1 - 2^-n, the chance of the £1 win")
    laplace = [o for o in l24["screens"][7]["widget"]["options"] if "Laplace" in o["text"]]
    expect(laplace and ("tfrac34" in laplace[0]["text"] or "tfrac{3}{4}" in laplace[0]["text"]),
           "finding 3: l24 screens[7] option c labels 2/3 as Laplace's rule; after two reds the rule gives (2+1)/(2+2) = 3/4")
    l21 = load("l21-kelly")
    expect("Even a large edge stakes less than half" not in l21["quiz"][1]["explain"]["text"],
           "finding 4: l21 quiz[1] explain generalises 'less than half the bankroll'; p = 0.8 at evens stakes 0.6")
    expect("overstates it" not in l21["screens"][2]["explain"]["text"],
           "finding 5: l21 screens[2] explain says wealth grows like e^{0.0201 n} and that the mean return overstates it; e^{ng} is the median path, while expected wealth is 1.04^n (2,540 times over 200 bets)")
    for msg in failures:
        print("CONTENT FAIL:", msg)
    assert not failures, f"{len(failures)} content claim(s) disagree with the checks (see audit-puzzles-4-5.md)"


if __name__ == "__main__":
    for fn in (check_l19, check_l20, check_l21, check_l22, check_l23, check_l24):
        fn()
    check_content_claims()
    print("puzzles L4 concepts: all checks passed")
    sys.exit(0)
