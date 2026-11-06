"""Concept checks for puzzles L5 (lessons l25 to l30, review-5, homework-5).

Run from the repo root: python3 -I docs/reports/puzzles-L5-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-puzzles-4-5-ledger.md).
Exact results use fractions, sympy or exhaustive enumeration; game claims (duels, truels,
the reroll game) get independent solves; Monte Carlo uses seeded numpy with 4-standard-error
bands. Content code (the lesson solutions) is run as written for code-behaviour claims.
"""
import json
import pathlib
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, pi, sqrt

import numpy as np
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / "app" / "content" / "courses" / "puzzles"
rng = np.random.default_rng(20261106)


def load(name):
    with open(COURSE / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


def solution_ns(widget):
    ns = {}
    exec(widget.get("prelude", ""), ns)
    exec(widget["solution"], ns)
    return ns


def band(p, n, k=4):
    return k * sqrt(p * (1 - p) / n)


# ------------------------------------------------------------------ l25 fair from biased
def check_l25():
    p = sp.symbols("p", positive=True)
    assert sp.simplify(2 / (2 * p * (1 - p)) - 1 / (p * (1 - p))) == 0, "l25 screens[6]: E[flips] = 2/(2pq) = 1/(pq)"
    for pp, want in ((F(2, 3), F(9, 2)), (F(3, 5), F(25, 6)), (F(1, 2), 4), (F(9, 10), F(100, 9)), (F(4, 5), F(25, 4))):
        assert 1 / (pp * (1 - pp)) == want, f"l25: 1/(pq) at p = {pp} is {want}"
    assert F(2, 3) * F(1, 3) == F(1, 3) * F(2, 3) == F(2, 9) and F(4, 9) != F(1, 9), "l25 screens[1]: HT = TH = 2/9; HH 4/9, TT 1/9"
    assert 2 * F(7, 10) * F(3, 10) == F(21, 50) and abs(float(F(21, 50)) - 0.42) < 1e-12, "l25 screens[9] row 2: 2pq = 0.42"
    assert 3 * F(8, 6) == 4 and 2 * F(4, 3) == F(8, 3) and 3 * F(8, 5) == F(24, 5), "l25 screens[4], [9] row 3, review-5 items[0]: 4, 8/3, 4.8 flips"
    assert 3 / (3 * F(3, 5) * F(2, 5) ** 2) == F(125, 12) and 2 * F(25, 6) == F(25, 3) and 2 * F(25, 6) * F(4, 3) == F(100, 9), "l25 screens[10], quiz[2], homework-5 items[5]: 125/12, 25/3, 100/9"
    assert F(1, 8) / F(6, 8) == F(1, 6), "l25 screens[4] explain: each face 1/6 once a round succeeds"
    # fairness and cost by simulation, p = 0.6: von Neumann pairs, and the three-string method
    n = 300_000
    flips = rng.random((n, 2)) < 0.6
    kept = flips[:, 0] != flips[:, 1]
    assert abs(kept.mean() - 0.48) < band(0.48, n), "l25 screens[3]: a round is kept with chance 2pq = 0.48"
    heads = flips[kept, 0].mean()
    assert abs(heads - 0.5) < band(0.5, kept.sum()), f"l25 screens[7]: a kept round is heads with chance 1/2 (got {heads:.4f})"
    tri = rng.random((n, 3)) < 0.6
    ones = tri.sum(axis=1) == 1
    assert abs(ones.mean() - 0.288) < band(0.288, n), "l25 screens[10]: a three-flip round succeeds with 3pq^2 = 0.288"
    who = tri[ones].argmax(axis=1)
    for k in range(3):
        assert abs((who == k).mean() - 1 / 3) < band(1 / 3, ones.sum()), "l25 screens[10]: HTT, THT, TTH name each person equally"
    # Wald: expected flips = flips per round x expected rounds
    assert abs(3 / ones.mean() - 125 / 12) < 0.1, "l25 screens[10]: 3/0.288 = 125/12 flips"
    # the lesson's code, run as written (seeded tests)
    ns = solution_ns(load("l25-fair-from-biased")["screens"][8]["widget"])
    bits = ns["von_neumann"](ns["_biased"](20000, 0.8, 1))
    assert abs(ns["_share"](bits) - 0.5) < 0.03, "l25 screens[8] test 5: fair share at p = 0.8"
    assert abs(len(ns["von_neumann"](ns["_biased"](20000, 0.8, 2))) - 3200) < 150, "l25 screens[8] test 6 and explain: about 3,200 bits from 20,000 flips"
    assert ns["von_neumann"]("THHTH") == "TH" and ns["von_neumann"]("HHTT") == "" and ns["expected_flips"](F(9, 10)) == F(100, 9), "l25 screens[8] tests"
    print("l25 ok")


# ------------------------------------------------------------------ l26 estimating n
def umvu(sample):
    m, k = max(sample), len(sample)
    return m + F(m, k) - 1


def check_l26():
    for N, k, want in ((20, 2, 14), (20, 3, F(63, 4)), (10, 4, F(44, 5)), (100, 5, F(505, 6))):
        subsets = list(combinations(range(1, N + 1), k))
        emax = sum(F(max(s)) for s in subsets) / len(subsets)
        assert emax == want == F(k * (N + 1), k + 1), f"l26: E[max] with N={N}, k={k} is {want} (exhaustive)"
        assert len(subsets) == comb(N, k), "l26 screens[5] explain: 1,140 triples" if (N, k) == (20, 3) else "count"
    assert comb(20, 3) == 1140 and comb(50, 4) == 230300 and comb(12, 4) == 495, "l26 screens[5], [8], homework-5 items[1]: subset counts"
    # unbiasedness and the variance ratio, exhaustively
    for N, k in ((20, 3), (12, 4), (50, 4), (20, 4)):
        subsets = list(combinations(range(1, N + 1), k))
        est = [umvu(s) for s in subsets]
        mean_based = [2 * F(sum(s), k) - 1 for s in subsets]
        rng_based = [F((max(s) - min(s)) * (k + 1), k - 1) - 1 for s in subsets]
        assert sum(est) / len(est) == N, f"l26 screens[4], [5]: m + m/k - 1 is unbiased (N={N}, k={k})"
        assert sum(mean_based) / len(est) == N, f"l26 screens[1], [3]: 2 x mean - 1 is unbiased too (N={N}, k={k})"
        assert sum(rng_based) / len(est) == N, f"l26 screens[8], homework-5 items[1]: R(k+1)/(k-1) - 1 is unbiased (N={N}, k={k})"
        assert sum(F(max(s)) for s in subsets) / len(subsets) < N, "l26 summary trap: the largest seen is biased low"
        var = lambda xs: sum((x - N) ** 2 for x in xs) / len(xs)
        assert var(mean_based) / var(est) == F(k + 2, 3), f"l26 screens[3]: variance ratio (k+2)/3 (N={N}, k={k})"
        if k == 4:
            assert var(mean_based) == 2 * var(est), "l26 screens[3] option c why: twice the variance at k = 4"
        if (N, k) == (50, 4):
            er = sum(F(max(s) - min(s)) for s in subsets) / len(subsets)
            assert er == F(3 * 51, 5) and float(er) == 30.6, "homework-5 items[2] explain: E[R] = 30.6 at k = 4, N = 50"
    assert umvu([60]) == 119 and umvu([19, 40, 42, 60]) == 74 and umvu([7, 3]) == F(19, 2) and umvu(list(range(1, 11))) == 10, "l26 screens[0], [1], [6] tests"
    assert umvu([100, 37, 81, 12, 64]) == 119 and umvu([77, 301, 455, 640, 812]) == F(4867, 5) and umvu([30, 50]) == 74 and umvu([10, 33, 45]) == 59, "l26 screens[7], [9], quiz[0], review-5 items[1]"
    assert 2 * F(161, 4) - 1 == F(159, 2) and float(F(159, 2)) == 79.5, "l26 screens[1] wrong mean-based: 79.5"
    assert [19 - 1, 40 - 19 - 1, 42 - 40 - 1, 60 - 42 - 1] == [18, 20, 1, 17] and sum([18, 20, 1, 17]) == 56 == 60 - 4, "l26 screens[1] explain: gaps 18, 20, 1, 17"
    assert F(41 * 5, 3) - 1 == F(202, 3) and F(57 * 6, 4) - 1 == F(169, 2), "l26 screens[8], review-5 items[2]: range estimates"
    theta, x = sp.symbols("theta x", positive=True)
    for k in (3, 4):
        emax = sp.integrate(x * k * x ** (k - 1) / theta ** k, (x, 0, theta))
        assert sp.simplify(emax - k * theta / (k + 1)) == 0, f"l26 screens[7] row 3, quiz[2]: E[max of {k} uniforms] = k theta/(k+1)"
    assert F(4, 3) * F(9, 10) == F(6, 5) and F(5, 4) * 2 == F(5, 2), "l26 screens[7] row 3, quiz[2]: 1.2 and 2.5"
    # the lesson's code with the quoted seed
    ns = solution_ns(load("l26-estimating-n")["screens"][6]["widget"])
    est, mx = ns["tank_sim"](100, 5, 20000, 1)
    assert abs(est - 99.94) < 0.01, f"l26 screens[6] explain: seed 1 gives about 99.94 (got {est:.3f})"
    assert abs(est - 100) < 0.36 and abs(mx - 505 / 6) < 0.3 + 0.0, "l26 screens[6] tests 6, 7"
    sd_est = sqrt((100 - 5) * 101 / (5 * 7))
    assert abs(3 * sd_est / sqrt(20000) - 0.35) < 0.01, "l26 screens[6] explain: three standard errors is about 0.35"
    hw = solution_ns(load("homework-5")["items"][1]["widget"])
    assert hw["_avg"](12, 4) == (F(12), F(12)), "homework-5 items[1] test 6: both estimates average to 12 over all 495 sets"
    assert hw["tank_estimates"]([5, 17, 30]) == (F(39), F(49)) and hw["tank_estimates"]([10, 20]) == (F(29), F(29)), "homework-5 items[1] tests"
    print("l26 ok")


# ------------------------------------------------------------------ l27 given the total
def rolls(n_dice=2, faces=6):
    return list(product(range(1, faces + 1), repeat=n_dice))


def cond_p(event, given, n_dice=2, faces=6):
    kept = [r for r in rolls(n_dice, faces) if given(r)]
    return F(sum(1 for r in kept if event(r)), len(kept)), len(kept)


def cond_mean(f, given, n_dice=2, faces=6):
    kept = [r for r in rolls(n_dice, faces) if given(r)]
    return F(sum(f(r) for r in kept), len(kept))


def check_l27():
    p, n = cond_p(lambda r: r[0] % 2 == 0 and r[1] % 2 == 0, lambda r: sum(r) == 8)
    assert n == 5 and p == F(3, 5) and cond_p(lambda r: r[0] % 2 == 0 and r[1] % 2 == 0, lambda r: True)[0] == F(1, 4), "l27 screens[0], [1]: five rolls total 8; both even 3/5 (1/4 unconditionally)"
    assert cond_mean(max, lambda r: sum(r) == 10) == F(17, 3) and cond_mean(max, lambda r: True) == F(161, 36), "l27 screens[2]: E[max | total 10] = 17/3; 161/36 unconditionally"
    p, n = cond_p(lambda r: r == (5, 5), lambda r: max(r) == 5)
    assert n == 9 and p == F(1, 9), "l27 screens[3], [4]: nine rolls with larger die 5; both 5 with 1/9"
    assert cond_p(lambda r: r == (6, 6), lambda r: sum(r) == 12) == (F(1), 1), "l27 screens[5]: total 12 forces (6, 6)"
    assert cond_mean(sum, lambda r: max(r) == 5) == F(70, 9) and cond_mean(sum, lambda r: True) == 7, "l27 screens[6]: E[total | max 5] = 70/9"
    assert cond_p(lambda r: 1 in r, lambda r: sum(r) == 6)[0] == F(2, 5), "l27 screens[8] row 1, screens[7] test 3"
    assert cond_mean(min, lambda r: max(r) == 6) == F(36, 11) and cond_mean(sum, lambda r: max(r) == 6) == F(102, 11), "l27 screens[8] row 2, homework-5 items[6]"
    p, n = cond_p(lambda r: 3 in r, lambda r: sum(r) == 5, n_dice=3)
    assert n == 6 and p == F(1, 2), "l27 screens[8] row 3: three dice total 5 in six ways, three with a 3"
    assert cond_p(lambda r: 6 in r, lambda r: sum(r) == 7)[0] == F(1, 3) and cond_p(lambda r: 6 in r, lambda r: True)[0] == F(11, 36), "l27 screens[9]"
    for faces, want in ((6, 5), (10, 8), (100, F(151, 2))):
        got = cond_mean(max, lambda r: sum(r) == faces + 1, faces=faces)
        assert got == want == F(3 * faces + 2, 4), f"l27 screens[10]: E[max | total n+1] = (3n+2)/4 at n = {faces}"
    days = list(product(range(-2, 3), repeat=2))
    kept = [d for d in days if sum(d) == 1]
    assert len(kept) == 4 and F(sum(1 for d in kept if min(d) < 0), 4) == F(1, 2), "l27 screens[11]: two of four pairs totalling +1 hold a loss"
    assert F(sum(1 for d in days if min(d) < 0), 25) == F(16, 25) and all(min(d) >= 0 for d in days if sum(d) == 2), "l27 screens[11]: 0.64 unconditionally; +2 rules out a loss"
    assert F(comb(13, 2), 2 * comb(26, 2)) == F(3, 25) and F(comb(13, 2), comb(52, 2)) == F(1, 17), "l27 quiz[0]: 78/650 = 3/25; 78/1326 unconditionally"
    assert cond_p(lambda r: r[0] == r[1], lambda r: sum(r) == 8)[0] == F(1, 5) and cond_mean(lambda r: r[0], lambda r: sum(r) == 9) == F(9, 2), "l27 quiz[1], quiz[2]"
    assert cond_mean(min, lambda r: max(r) == 4) == F(16, 7) and cond_p(lambda r: 6 in r, lambda r: sum(r) >= 10)[0] == F(5, 6), "review-5 items[3], [4]"
    p, n = cond_p(lambda r: 6 in r, lambda r: sum(r) == 10, n_dice=3)
    assert n == 27 and p == F(1, 3) and abs(1 - (5 / 6) ** 3 - 0.4213) < 5e-5, "homework-5 items[7]: 27 ordered rolls total 10, nine with a six"
    ns = solution_ns(load("l27-given-the-total")["screens"][7]["widget"])
    assert ns["cond_mean"](max, lambda r: sum(r) == 11, faces=10) == F(8) and ns["conditional"](lambda r: r == (5, 5), lambda r: max(r) == 5) == F(1, 9), "l27 screens[7] solution"
    print("l27 ok")


# ------------------------------------------------------------------ l28 duels and truels
def duel(p, q):
    p, q = F(p), F(q)
    return p / (1 - (1 - p) * (1 - q))


def truel_best_play(pa, pb, pc=F(1)):
    """Independent backward induction with C perfect: each player maximises own survival.
    Returns (A, B, C) chances and A's best first move."""
    pa, pb, pc = F(pa), F(pb), F(pc)
    assert pc == 1
    # after C's shot (all alive): C kills one rival, the survivor then fires first at C
    c_kill_b = (duel(pa, pc), F(0), 1 - duel(pa, pc))
    c_kill_a = (F(0), duel(pb, pc), 1 - duel(pb, pc))
    v_c = max((c_kill_b, c_kill_a), key=lambda v: v[2])
    mix = lambda pr, hit, miss: tuple(pr * h + (1 - pr) * m for h, m in zip(hit, miss))
    b_opts = {
        "air": v_c,
        "C": mix(pb, (duel(pa, pb), 1 - duel(pa, pb), F(0)), v_c),       # C dead, A fires first at B
        "A": mix(pb, (F(0), 1 - duel(pc, pb), duel(pc, pb)), v_c),       # A dead, C fires first at B
    }
    v_b = max(b_opts.values(), key=lambda v: v[1])
    a_opts = {
        "air": v_b,
        "C": mix(pa, (1 - duel(pb, pa), duel(pb, pa), F(0)), v_b),       # C dead, B fires first at A
        "B": mix(pa, (1 - duel(pc, pa), F(0), duel(pc, pa)), v_b),       # B dead, C fires first at A
    }
    move = max(a_opts, key=lambda k: a_opts[k][0])
    return a_opts[move], move, a_opts


def check_l28():
    p, q, x = sp.symbols("p q x", positive=True)
    sol = sp.solve(sp.Eq(x, p + (1 - p) * (1 - q) * x), x)[0]
    assert sp.simplify(sol - p / (1 - (1 - p) * (1 - q))) == 0, "l28 screens[5], [6]: x = p/(1 - (1-p)(1-q))"
    even_q = sp.solve(sp.Eq(sol, sp.Rational(1, 2)), q)
    assert len(even_q) == 1 and sp.simplify(even_q[0] - p / (1 - p)) == 0, "l28 screens[1]: even when q = p/(1-p)"
    assert duel(F(1, 3), F(1, 2)) == F(1, 2) and duel(F(1, 4), F(1, 3)) == F(1, 2) and duel(F(1, 5), F(1, 4)) == F(1, 2), "l28 screens[0], [1], review-5 items[5]"
    assert duel(F(1, 4), F(1, 4)) == F(4, 7) and duel(F(1, 2), F(1, 2)) == F(2, 3) and duel(F(1, 3), F(2, 3)) == F(3, 7) and duel(1, F(1, 2)) == 1, "l28 screens[8], [5]"
    assert duel(F(2, 5), F(3, 5)) == F(10, 19) and (1 - F(1, 3)) * duel(F(1, 2), F(1, 3)) == F(1, 2), "l28 quiz[0], quiz[1]"
    assert duel(F(1, 2), F(1, 3)) == F(3, 4), "l28 quiz[1] wrong a-first"
    # truel (1/3, 2/3, 1): values of A's three first moves
    air = F(2, 3) * duel(F(1, 3), F(2, 3)) + F(1, 3) * F(1, 3)
    at_c = F(1, 3) * (F(1, 3) * duel(F(1, 3), F(2, 3))) + F(2, 3) * air
    at_b = F(2, 3) * air
    assert air == F(25, 63) and at_c == F(59, 189) and at_b == F(50, 189) and air > at_c > at_b, "l28 screens[2..4]: 25/63, 59/189, 50/189; air is best"
    assert F(1, 3) * duel(F(1, 3), F(2, 3)) == F(1, 7), "l28 screens[3]: duel with B first is worth 1/7 to A"
    (a, b, c), move, opts = truel_best_play(F(1, 3), F(2, 3))
    assert (a, b, c, move) == (F(25, 63), F(8, 21), F(2, 9), "air") and a + b + c == 1, "l28 screens[9], quiz[2], review-5 items[6]: 25/63, 8/21, 2/9 under best play"
    assert F(2, 3) * F(4, 7) == F(8, 21) and F(1, 3) * F(2, 3) == F(2, 9), "l28 screens[9] hints: B 2/3 x 4/7, C 1/3 x 2/3"
    (a, b, c), move, opts = truel_best_play(F(1, 2), F(2, 3))
    assert (a, b, c, move) == (F(17, 30), F(4, 15), F(1, 6), "air") and opts["C"][0] == F(23, 60), "l28 screens[10]: air 17/30, aim at C 23/60"
    for pa, pb, want in ((F(1, 2), F(3, 4), (F(31, 56), F(9, 28), F(1, 8), "air")), (F(1, 3), F(1, 2), (F(5, 12), F(1, 4), F(1, 3), "air")),
                         (F(1, 5), F(1, 4), (F(59, 200), F(9, 40), F(12, 25), "C")), (F(1, 6), F(1, 4), (F(109, 432), F(49, 216), F(25, 48), "C"))):
        (a, b, c), move, opts = truel_best_play(pa, pb)
        assert (a, b, c, move) == want, f"homework-5 items[0] tests: truel({pa}, {pb}, 1) = {want} (got {(a, b, c, move)})"
    (a, b, c), move, opts = truel_best_play(F(1, 5), F(1, 4))
    assert opts["air"][0] == F(11, 40) and opts["C"][0] == F(59, 200) and F(3, 4) * F(1, 2) == F(3, 8), "homework-5 items[4]: air 11/40, aim at C 59/200, hit branch 3/8"
    (a, b, c), move, opts = truel_best_play(F(1, 4), F(2, 5))
    assert a + b + c == 1, "homework-5 items[0] test 7: chances add to 1"
    # the lesson's and the homework's code, run as written
    ns = solution_ns(load("l28-duels")["screens"][7]["widget"])
    assert tuple(ns["truel_air"](F(1, 3), F(2, 3), F(9, 10))) == (F(165, 406), F(80, 203), F(81, 406)), "l28 screens[7] test 7"
    assert sum(ns["truel_air"](F(1, 4), F(1, 2), F(3, 4))) == 1, "l28 screens[7] test 8"
    hw = solution_ns(load("homework-5")["items"][0]["widget"])
    for case in load("homework-5")["items"][0]["widget"]["tests"]:
        got = eval(case["call"], dict(hw))
        want = eval(case["expect"], {"Fraction": F})
        assert got == want, f"homework-5 items[0] solution: {case['call']}"
    # Monte Carlo: duel (1/3, 1/2) and the air truel (1/3, 2/3, 1)
    n = 300_000
    a_shots = rng.random((n, 40)) < 1 / 3
    b_shots = rng.random((n, 40)) < 1 / 2
    a_wins = np.zeros(n, dtype=bool)
    done = np.zeros(n, dtype=bool)
    for r in range(40):
        a_wins |= a_shots[:, r] & ~done
        done |= a_shots[:, r]
        done |= b_shots[:, r]
    assert abs(a_wins.mean() - 0.5) < band(0.5, n), f"l28 screens[0]: duel sim {a_wins.mean():.4f}"
    b_hits_c = rng.random(n) < 2 / 3
    a_hits = rng.random((n, 40)) < 1 / 3
    b_hits = rng.random((n, 40)) < 2 / 3
    # branch 1: C dead, A first against B; branch 2: B dead, A has one shot at C
    a_win_duel = np.zeros(n, dtype=bool)
    done = np.zeros(n, dtype=bool)
    for r in range(40):
        a_win_duel |= a_hits[:, r] & ~done
        done |= a_hits[:, r] | b_hits[:, r]
    a_surv = np.where(b_hits_c, a_win_duel, a_hits[:, 0])
    assert abs(a_surv.mean() - 25 / 63) < band(25 / 63, n), f"l28 screens[2]: truel sim {a_surv.mean():.4f}"
    print("l28 ok")


# ------------------------------------------------------------------ l29 random chords
def check_l29():
    d, th = sp.symbols("d theta", positive=True)
    assert sp.solve(sp.Eq(2 * sp.sqrt(1 - d ** 2), sp.sqrt(3)), d) == [sp.Rational(1, 2)], "l29 screens[1], [6]: L > sqrt3 iff d < 1/2"
    assert sp.solve(sp.Eq(2 * sp.sqrt(1 - d ** 2), sp.sqrt(2)), d) == [sp.sqrt(2) / 2] and sp.solve(sp.Eq(2 * sp.sqrt(1 - d ** 2), 1), d) == [sp.sqrt(3) / 2], "l29 screens[10], quiz[2]: cut-offs 1/sqrt2 and sqrt3/2"
    # exact: endpoints (central angle beyond 120 degrees), radius (d uniform), midpoint (d^2)
    assert sp.Rational(120, 360) == sp.Rational(1, 3) and sp.Rational(1, 2) ** 2 == sp.Rational(1, 4), "l29 screens[0..2]: 1/3, 1/2, 1/4"
    assert sp.Rational(180, 360) == sp.Rational(1, 2) and (sp.sqrt(2) / 2) ** 2 == sp.Rational(1, 2) and abs(float(sp.sqrt(2) / 2) - 0.7071) < 5e-5, "l29 screens[10]: 1/2, 0.7071, 1/2"
    assert sp.Rational(240, 360) == sp.Rational(2, 3) and abs(float(sp.sqrt(3) / 2) - 0.866) < 5e-4 and (sp.sqrt(3) / 2) ** 2 == sp.Rational(3, 4), "l29 quiz[1], quiz[2], review-5 items[8]: 2/3, 0.866, 3/4"
    # expected lengths
    e_end = sp.integrate(2 * sp.sin(th / 2), (th, 0, 2 * sp.pi)) / (2 * sp.pi)
    e_rad = sp.integrate(2 * sp.sqrt(1 - d ** 2), (d, 0, 1))
    e_mid = sp.integrate(2 * sp.sqrt(1 - d ** 2) * 2 * d, (d, 0, 1))
    assert sp.simplify(e_end - 4 / sp.pi) == 0 and sp.simplify(e_rad - sp.pi / 2) == 0 and e_mid == sp.Rational(4, 3), "l29 screens[9]: 4/pi, pi/2, 4/3"
    assert e_rad > e_mid > e_end, "l29 screens[9] explain: the radius procedure gives the longest chords on average"
    # Monte Carlo, all three procedures, both thresholds and the lengths
    n = 400_000
    a, b = rng.random(n) * 2 * pi, rng.random(n) * 2 * pi
    L_end = 2 * np.abs(np.sin((a - b) / 2))
    L_rad = 2 * np.sqrt(1 - rng.random(n) ** 2)
    L_mid = 2 * np.sqrt(1 - rng.random(n))                 # d = sqrt(U): 1 - d^2 = 1 - U
    for name, L, p3, p2, p1, mean in (("endpoints", L_end, 1 / 3, 1 / 2, 2 / 3, 4 / pi), ("radius", L_rad, 1 / 2, 2 ** -0.5, 3 ** 0.5 / 2, pi / 2), ("midpoint", L_mid, 1 / 4, 1 / 2, 3 / 4, 4 / 3)):
        for thr, want in ((3 ** 0.5, p3), (2 ** 0.5, p2), (1.0, p1)):
            got = (L > thr).mean()
            assert abs(got - want) < band(want, n), f"l29 {name}: P(L > {thr:.3f}) sim {got:.4f} vs {want:.4f}"
        assert abs(L.mean() - mean) < 4 * L.std() / sqrt(n), f"l29 screens[9] {name}: mean length sim {L.mean():.4f} vs {mean:.4f}"
    # the lesson's code with its seeds, and d = U in the midpoint branch giving the radius answer
    ns = solution_ns(load("l29-random-chords")["screens"][8]["widget"])
    cs = ns["chord_sim"]
    assert abs(cs("endpoints", 20000, 1) - 1 / 3) < 0.01 and abs(cs("radius", 20000, 2) - 0.5) < 0.0106 and abs(cs("midpoint", 20000, 3) - 0.25) < 0.0092, "l29 screens[8] tests 1 to 3"
    assert abs(sqrt(0.25 * 0.75 / 20000) - 0.003) < 1e-3, "l29 screens[8] explain: standard error about 0.003"
    # envelopes: exhaustive case tables
    def cases(pairs):
        return [(lo, hi, see) for lo, hi in pairs for see in (lo, hi)]
    two = cases([(10, 20), (20, 40)])
    see20 = [(lo, hi, s) for lo, hi, s in two if s == 20]
    assert len(see20) == 2 and sum(F(lo + hi - s) for lo, hi, s in see20) / 2 == 25, "l29 screens[4]: seeing £20 leaves two cases; switching worth £25"
    assert sum(F(s) for _, _, s in two) / 4 == sum(F(lo + hi - s) for lo, hi, s in two) / 4 == F(45, 2), "l29 screens[5]: keep and switch both £22.50"
    three = cases([(10, 20), (20, 40), (40, 80)])
    see80 = [c for c in three if c[2] == 80]
    assert len(see80) == 1 and see80[0][0] == 40, "l29 screens[6]: at £80 the other holds £40 for certain"
    see40 = [(lo, hi, s) for lo, hi, s in three if s == 40]
    assert sum(F(lo + hi - s) for lo, hi, s in see40) / len(see40) == 50, "l29 screens[6] explain, quiz[0]: at £40 switching is worth £50"
    rule = lambda lo, hi, s: s if s == 80 else lo + hi - s
    assert sum(F(rule(*c)) for c in three) / 6 == F(125, 3) and sum(F(c[2]) for c in three) / 6 == 35, "homework-5 items[8]: switch unless £80 is worth 125/3; always keep 35"
    best = F(0)
    for choice in product((0, 1), repeat=4):                # keep (0) or switch (1) at each seen amount 10, 20, 40, 80
        amounts = {10: choice[0], 20: choice[1], 40: choice[2], 80: choice[3]}
        val = sum(F((lo + hi - s) if amounts[s] else s) for lo, hi, s in three) / 6
        best = max(best, val)
    assert best == F(125, 3), "homework-5 items[8] explain: switch-unless-£80 is the best rule"
    five = cases([(5, 10), (10, 20), (20, 40)])
    see10 = [(lo, hi, s) for lo, hi, s in five if s == 10]
    assert sum(F(lo + hi - s) for lo, hi, s in see10) / 2 == F(25, 2), "review-5 items[7]: at £10 switching is worth £12.50"
    assert F(9 * 100 - 500, 10) == 40 and F(9 * 100 + 11 * (-500), 20) == -230, "l29 screens[11]: £40 a random day, -£230 for a random trade's day"
    print("l29 ok")


# ------------------------------------------------------------------ l30 follow-ups
def reroll_value_iteration(faces, cost, iters=5000):
    """Solve V = E[max(X, V - c)] by fixed-point iteration (independent of the threshold enumeration)."""
    c = F(cost)
    V = F(faces + 1, 2)
    for _ in range(iters):
        V_new = sum(max(F(k), V - c) for k in range(1, faces + 1)) / faces
        if V_new == V:
            break
        V = V_new
    return V


def check_l30():
    n = sp.symbols("n", positive=True, integer=True)
    m = sp.symbols("m", positive=True, integer=True)
    formula = sp.summation(m * (2 * m - 1), (m, 1, n)) / n ** 2
    assert sp.simplify(formula - (n + 1) * (4 * n - 1) / (6 * n)) == 0, "l30 screens[1], [6]: E[max] = (n+1)(4n-1)/(6n)"
    for faces in range(1, 31):
        got = sum(F(max(r)) for r in rolls(2, faces)) / faces ** 2
        assert got == F((faces + 1) * (4 * faces - 1), 6 * faces), f"l30 screens[0], [1]: formula matches enumeration at n = {faces}"
        assert all(sum(1 for r in rolls(2, faces) if max(r) == k) == 2 * k - 1 for k in range(1, faces + 1)), "l30 screens[0]: L of 2m - 1 cells"
    for faces, want in ((6, F(161, 36)), (20, F(553, 40)), (1, 1), (10, F(143, 20)), (100, F(13433, 200))):
        assert F((faces + 1) * (4 * faces - 1), 6 * faces) == want, f"l30: E[max] at n = {faces} is {want}"
    assert abs(float(F(553, 40)) - 13.825) < 1e-9 and abs(float(F(13433, 200)) - 67.165) < 1e-9 and abs(200 / 3 - 66.6667) < 5e-5, "l30 screens[1], [11]"
    assert F(13, 3) != F(161, 36) and sp.limit(((n + 1) * (4 * n - 1) / (6 * n)) / (2 * n / 3), n, sp.oo) == 1, "l30 screens[4]: (2n+1)/3 fails at n = 6; 2n/3 is only the large-n limit"
    # reroll game: value iteration against the lesson's threshold answers
    for faces, cost, want in ((6, F(1, 2), F(9, 2)), (6, 2, F(18, 5)), (6, 3, F(7, 2)), (6, 1, 4), (6, F(3, 2), F(15, 4)), (6, F(5, 2), F(7, 2)), (6, 10, F(7, 2)),
                              (8, 1, F(11, 2)), (10, 1, 7), (20, 1, F(91, 6))):
        got = reroll_value_iteration(faces, cost)
        assert abs(float(got - want)) < 1e-9, f"l30 screens[2], [7], quiz[0], review-5 items[9], homework-5 items[9]: reroll value n={faces}, c={cost} is {want} (got {got})"
    # the threshold rule keep x >= V - c, and the myopic rule differs in general
    V = reroll_value_iteration(20, 1)
    assert [k for k in range(1, 21) if k >= V - 1][0] == 15 and 2 * F(21, 2) / 2 - 1 < 15, "l30 screens[10], homework-5 items[9]: keep 15 or more at n = 20; one-step lookahead would keep from 10"
    V6 = reroll_value_iteration(6, 1)
    assert abs(float(V6 - 1) - 3) < 1e-9 and [k for k in range(1, 7) if k >= 6 - 1][0] == 5, "l30 screens[10]: at n=6, c=1 keep 3 or more; 'n - c' would keep 5 or more"
    assert F(18 - 3, 4) == F(15, 4) and F(20 - F(3, 2), 5) == F(37, 10) and F(15, 4) - F(3, 2) == F(9, 4), "l30 quiz[0]: 3.75 against 3.70; threshold 2.25"
    ns = solution_ns(load("l30-follow-ups")["screens"][7]["widget"])
    for case in load("l30-follow-ups")["screens"][7]["widget"]["tests"]:
        assert eval(case["call"], dict(ns)) == eval(case["expect"], {"Fraction": F}), f"l30 screens[7] test {case['call']}"
    # k players, runs, coupons
    assert F(1, 2) / (1 - F(1, 8)) == F(4, 7) and F(1, 2) / (1 - F(1, 16)) == F(8, 15), "l30 screens[9], quiz[1]"
    E = sp.symbols("E0:4")
    pr = sp.Rational(2, 3)
    eqs = [sp.Eq(E[i], 1 + pr * (E[i + 1] if i < 2 else 0) + (1 - pr) * E[0]) for i in range(3)]
    sol = sp.solve(eqs, E[:3])
    assert sol[E[0]] == sp.Rational(57, 8), "l30 screens[9] row 2: HHH at p = 2/3 waits 57/8 (chain solve)"
    pr = sp.Rational(1, 2)
    eqs = [sp.Eq(E[i], 1 + pr * (E[i + 1] if i < 3 else 0) + (1 - pr) * E[0]) for i in range(4)]
    assert sp.solve(eqs, E)[E[0]] == 30, "l30 quiz[2]: HHHH waits 30 flips (chain solve)"
    H = lambda k: sum(F(1, j) for j in range(1, k + 1))
    assert 12 * H(12) == F(86021, 2310) and abs(float(12 * H(12)) - 37.2385) < 5e-5 and 6 * H(6) == F(147, 10), "l30 screens[8]: 12 H_12 and 14.7"
    assert F(11 * 39, 60) == F(143, 20), "l30 screens[8] row 1: 7.15"
    print("l30 ok")


if __name__ == "__main__":
    for fn in (check_l25, check_l26, check_l27, check_l28, check_l29, check_l30):
        fn()
    print("puzzles L5 concepts: all checks passed")
    sys.exit(0)
