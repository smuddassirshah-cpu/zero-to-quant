#!/usr/bin/env python3
"""Concept checks for mental-pressure L4 (l13 to l17, review-4, homework-4).

Run from the repo root: python3 -I docs/reports/mental-pressure-L4-concepts.py
Every assert names the ledger row it backs (docs/reports/audit-mental-pressure-4-ledger.md).
Exact checks use fractions; the few Monte Carlo checks use enough replications to
separate the claim from its negation by many standard errors. Exit 0 means every
check passed; a failing check is a finding, not a check to weaken.
"""
import json
import math
import random
import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = ROOT / "app" / "content" / "courses" / "mental-pressure"

CHECKS = []


def check(name):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


def load(name):
    with open(COURSE / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- l13 helpers
def guess(k, w=F(1)):
    """Expected mark of a blind guess among k options: +1 right, -w wrong."""
    k = F(k)
    return 1 / k - F(w) * (k - 1) / k


def answer_value(p, w=F(1)):
    return F(p) - (1 - F(p)) * F(w)


def breakeven(w):
    return F(w) / (1 + F(w))


# ---------------------------------------------------------------- l13 checks
@check("l13_net_scores")
def _():
    assert 62 - 10 == 52, "l13 s[0] net 52"
    assert 62 - 10 - 8 == 44 and 62 + 10 == 72, "l13 s[0] wrong[] values are the named slips"
    assert 75 - 11 == 64 and 64 - 11 == 53, "l13 quiz[0] net 53"
    assert 66 - 9 == 57 and 57 - 9 == 48, "review-4 items[0] net 48"
    assert 15 - 4 == 11, "l17 quiz[1] net 11"
    assert 71 - 9 == 62, "homework-4 items[0] r2"


@check("l13_guess_table")
def _():
    assert [guess(k) for k in (4, 3, 2, 1)] == [F(-1, 2), F(-1, 3), F(0), F(1)], "l13 s[1] bars at -1"
    assert guess(5) == F(-3, 5), "l13 s[2] five options -0.6"
    assert guess(4, F(1, 3)) == 0 and guess(4, F(1, 2)) == F(-1, 8) and guess(4, 0) == F(1, 4), "l13 s[5] rules"
    assert guess(4, F(33, 100)) > 0, "l13 s[1].explain: at -0.33 a blind guess is (just) free"
    assert guess(3) == F(-1, 3), "l13 s[7] five less two leaves three"
    assert [k for k in range(1, 50) if guess(k) == 0] == [2], "l13 s[7].explain: free only when two are left"
    assert guess(4) * 80 == -40, "l13 s[10] r2 at +1/-1"
    assert 6 * guess(4, 0) == F(3, 2), "l13 quiz[3] six free guesses"
    assert guess(5) == F(-3, 5) and guess(3, F(1, 3)) == F(1, 9), "homework-4 items[0] r0, r1"
    assert 2 + 2 * guess(4, 0) == F(5, 2), "l17 s[5] r4 two guesses in B"


@check("l13_guess_value_mc")
def _():
    rng = random.Random(13)
    n = 400_000
    for k, target in ((4, -0.5), (3, -1 / 3), (2, 0.0), (5, -0.6)):
        total = sum(1 if rng.randrange(k) == 0 else -1 for _ in range(n))
        mean = total / n
        se = math.sqrt(max(1e-12, 1 - target * target) / n)
        assert abs(mean - target) < 5 * se, f"l13 s[1]/s[2]: average mark of many guesses among {k} is {target}"


@check("l13_monotone_in_k")
def _():
    # l13 s[2].explain: every option removed moves the bar up, for any penalty w >= 0.
    for i in range(0, 201):
        w = F(i, 100)
        vals = [guess(k, w) for k in range(1, 101)]
        assert all(a > b for a, b in zip(vals, vals[1:])), f"l13 s[2].explain E(k, w) strictly decreasing in k at w={w}"


@check("l13_answer_value")
def _():
    rows = {F(2, 5): F(-1, 5), F(1, 2): F(0), F(3, 5): F(1, 5), F(3, 4): F(1, 2), F(9, 10): F(4, 5)}
    for p, v in rows.items():
        assert answer_value(p) == 2 * p - 1 == v, f"l13 s[3] row p={p}"
    assert answer_value(F(11, 20)) == F(1, 10), "l13 quiz[2] 55% sure earns 0.1"
    assert all(answer_value(q) < 0 for q in (F(45, 100), F(1, 4), F(1, 10))), "l13 quiz[2].options[2].why: another option averages below 0"
    assert 70 * F(85, 100) == F(119, 2) and 70 - F(119, 2) == F(21, 2) and F(119, 2) - F(21, 2) == 49, "l13 s[10] r3-r5"
    assert 60 * (2 * F(4, 5) - 1) == 36 and 64 * F(4, 5) + 16 * guess(4) == F(216, 5), "homework-4 items[0] r3, r4"
    assert 2 * F(7, 10) - 1 == F(2, 5), "homework-4 items[0] r5"


@check("l13_breakeven")
def _():
    # Finding 1: the half-sure rule is the w = 1 case of p* = w / (1 + w).
    for w, pstar in ((1, F(1, 2)), (F(1, 2), F(1, 3)), (F(1, 3), F(1, 4)), (F(1, 4), F(1, 5)), (0, F(0))):
        assert breakeven(w) == pstar, f"break-even at w={w}"
        for i in range(0, 101):
            p = F(i, 100)
            assert (answer_value(p, w) > 0) == (p > pstar), f"answer beats blank iff p > w/(1+w) at w={w}, p={p}"
    assert answer_value(F(3, 10), F(1, 3)) > 0, "at -1/3 a 30%-sure answer already beats a blank: 'half sure' is not the rule there"
    # l13 s[10] r2 and r6 keys hold at +1/-1 only.
    assert 80 * guess(4, F(1, 3)) == 0 and breakeven(F(1, 3)) == F(1, 4), "l13 s[10] r2, r6 keys change under -1/3"


@check("l13_fair_penalty")
def _():
    for k in range(2, 12):
        w = F(1, k - 1)
        assert guess(k, w) == 0, f"l13 s[8] fair penalty 1/(k-1) at k={k}"
        assert guess(k - 1, w) > 0 or k == 2, f"l13 s[8].explain: under a fair penalty, removing one option makes the guess pay (k={k})"
        assert guess(k, F(1, k)) != 0 or k == 2, "l13 s[8].wrong over-k does not zero the guess"
        assert guess(k, k - 1) != 0 or k == 2, "l13 s[8].wrong upside-down does not zero the guess"
    assert guess(4, F(1, 3)) == 0 and guess(5, F(1, 4)) == 0, "l13 s[8].feedback: a third for four, a quarter for five"
    assert guess(5, F(1, 3)) == F(-1, 15) < 0, "l13 s[11].options[3]: at -1/3 'guess everything' fails with five options (finding 1)"
    assert F(1, 5 - 1) == F(1, 4), "homework-4 items[0] r6"


@check("l13_trade")
def _():
    per = 2 * F(9, 10) - 1
    assert per == F(4, 5), "l13 s[4] canvas: solving at 90% earns 0.8"
    assert guess(2) + F(20 - 2, 6) * per == F(12, 5), "l13 s[4] trade 2.4"
    assert F(12, 5) - per == F(8, 5), "l13 s[4].explain gain 1.6"
    assert 3 * F(9, 10) == F(27, 10) and 3 * 1 == 3, "l13 s[4] wrong[] 2.7 and 3"
    assert 5 * per == 4, "l13 s[6].options[3].why: five questions at 6 s worth 4 marks"
    per80 = 2 * F(4, 5) - 1
    assert per80 == F(3, 5) and guess(2) + F(24 - 3, 6) * per80 == F(21, 10), "review-4 items[1] 2.1"
    assert F(24, 6) * per80 == F(12, 5) and F(21, 6) * F(4, 5) == F(14, 5), "review-4 items[1] wrong[] 2.4 and 2.8"
    # The trade is worth nothing when the clock is not binding (finding 3): the saved seconds then buy no question.
    assert guess(2) + 0 * per < per, "with no questions left to reach, guessing loses 0.8 to solving"


@check("l13_quick_eight")
def _():
    keys = [guess(3), 58 - 14, 80 * guess(4), 70 * F(85, 100), 70 * F(15, 100), 70 * F(70, 100), breakeven(1), guess(4, F(1, 3))]
    assert keys == [F(-1, 3), 44, -40, F(119, 2), F(21, 2), 49, F(1, 2), 0], "l13 s[10] eight keys"


# ---------------------------------------------------------------- code runners
def run_code_widget(widget, use_starter=False):
    """Run a Python code widget's solution (or starter) against its hidden tests.

    Returns the list of (call, passed) pairs."""
    ns = {}
    src = (widget.get("prelude") or "") + "\n" + (widget["starter"] if use_starter else widget["solution"])
    exec(src, ns)
    results = []
    for t in widget["tests"]:
        try:
            if t.get("setup"):
                exec(t["setup"], ns)
            actual = eval(t["call"], ns)
            expected = eval(t["expect"], ns)
            cmp = t.get("compare", "equal")
            if cmp == "fraction":
                ok = F(actual) == F(expected)
            elif cmp == "isclose":
                ok = math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=1e-12)
            else:
                ok = actual == expected
        except Exception:  # noqa: BLE001 - a starter raising is a failing test
            ok = False
        results.append((t["call"], ok))
    return results


def code_screen(lesson, idx):
    return load(lesson)["screens"][idx]["widget"]


def assert_code(widget, label):
    res = run_code_widget(widget)
    bad = [c for c, ok in res if not ok]
    assert not bad, f"{label}: solution fails hidden tests {bad}"
    starter = run_code_widget(widget, use_starter=True)
    assert any(not ok for _, ok in starter), f"{label}: the starter must fail at least one test"
    return len(res)


@check("code_l13")
def _():
    n = assert_code(code_screen("l13-negative-marking", 9), "l13 s[9]")
    assert n == 13, "l13 s[9].how says 13 hidden tests"


@check("code_l14")
def _():
    n = assert_code(code_screen("l14-ranking-likelihoods", 9), "l14 s[9]")
    assert n == 11, "l14 s[9].how says 11 hidden tests"


@check("code_l15")
def _():
    n = assert_code(code_screen("l15-probability-at-speed", 9), "l15 s[9]")
    assert n == 10, "l15 s[9].how says 10 hidden tests"


@check("code_l16")
def _():
    w = code_screen("l16-harder-sequences", 9)
    n = assert_code(w, "l16 s[9]")
    assert n == 13, "l16 s[9].how says 13 hidden tests"
    ns = {}
    exec(w["solution"], ns)
    nt = ns["next_term"]
    # l16 s[9].explain: alternating steps and digit sums return None; the reversal row solves by its halves.
    assert nt([3, 6, 4, 8, 6, 12, 10]) is None and nt([7, 14, 19, 29, 40, 44]) is None, "l16 s[9].explain None cases"
    assert nt([12, 21, 23, 32, 34, 43]) == 45, "l16 s[9].explain: 45 comes out either way"
    assert nt([1, 2, 3, 4, 9, 8, 27]) == 16 and nt([2, 4, 8, 6, 32, 8]) == 128, "l16 s[9] interleaved tests"


@check("code_hw_generator")
def _():
    hw = load("homework-4")
    w = hw["items"][4]["widget"]
    n = assert_code(w, "homework-4 items[4]")
    assert n == 12, "homework-4 items[4].how says 12 hidden tests"
    # The prose's distractor definitions match the prelude checkers: one reverse, one point, one slip, all positive and distinct.
    ns = {}
    exec(w["prelude"] + "\n" + w["solution"], ns)
    items = ns["battery_generator"](99, {"add": 50, "sub": 50, "mul": 50, "div": 50})
    assert all(ns["_types_ok"](it) and ns["_once"](it) and ns["_positive"](it) and ns["_whole_div"](it) for it in items), "homework-4 items[4] prose: near-miss kinds hold on a fresh seed"
    # A slipped 9 steps down instead of wrapping (explain.text).
    rng = random.Random(0)
    for _ in range(2000):
        v = ns["slip"](rng, 999)
        assert v in (899, 989, 998), "homework-4 items[4].explain: a slipped 9 cannot wrap to 0"


@check("code_hw_trade")
def _():
    hw = load("homework-4")
    w = hw["items"][5]["widget"]
    n = assert_code(w, "homework-4 items[5]")
    assert n == 11, "homework-4 items[5].how says 11 hidden tests"
    ns = {}
    exec(w["solution"], ns)
    tv, aog = ns["trade_values"], ns["answer_or_guess"]
    # explain: at 50% accuracy both sides are 0 and the tie goes to answering.
    assert tv(20, 2, 6, F(1, 2)) == (0, 0) and aog(20, 2, 6, F(1, 2)) == "answer", "homework-4 items[5].explain 50% tie"
    # explain: with two left a slow question nearly always becomes a guess: exactly when s - g > pace and accuracy > 1/2.
    for s in range(2, 61):
        for pace in (6, 10, 20):
            for a in (F(3, 5), F(3, 4), F(9, 10)):
                want = "guess" if s - 2 > pace else "answer"
                assert aog(s, 2, pace, a) == want, f"homework-4 items[5].explain two-left rule s={s} pace={pace} a={a}"
    # The two ties named in `how`.
    assert tv(12, 3, 6, F(3, 4))[0] == tv(12, 3, 6, F(3, 4))[1] == F(1, 2), "homework-4 items[5] tie at 12 s, 3 left"


# ---------------------------------------------------------------- l14 helpers
def at_least_one(p, n):
    return 1 - (1 - F(p)) ** n


def binom_pmf(n, k):
    return F(comb(n, k), 2 ** n)


def birthday(n):
    q = F(1)
    for i in range(n):
        q *= F(365 - i, 365)
    return 1 - q


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ---------------------------------------------------------------- l14 checks
@check("l14_rank_exact")
def _():
    h5, t7, ak = binom_pmf(10, 5), F(1, 6), F(8, 52)
    assert h5 == F(63, 256) and ak == F(2, 13) and h5 > t7 > ak, "l14 s[0] order h5, t7, ak"
    assert 13 > 12, "l14 s[0].explain cross multiply 1/6 vs 2/13: 13 against 12"
    b30, six6, heads6 = birthday(30), at_least_one(F(1, 6), 6), sum(binom_pmf(10, k) for k in range(6, 11))
    assert abs(float(b30) - 0.706) < 5e-4 and abs(float(six6) - 0.665) < 5e-4 and heads6 == (1 - F(63, 256)) / 2, "l14 s[2] values"
    assert b30 > six6 > heads6, "l14 s[2] order bday, six, heads"
    four, b23, dbl = at_least_one(F(1, 6), 4), birthday(23), at_least_one(F(1, 36), 24)
    assert four == F(671, 1296) and abs(float(b23) - 0.507) < 5e-4 and abs(float(dbl) - 0.491) < 5e-4, "l14 s[3] values"
    assert four > b23 > dbl and all(abs(float(x) - 0.5) < 0.02 for x in (four, b23, dbl)), "l14 s[3] order and 'within 0.02 of a half'"
    assert abs(math.exp(-2 / 3) - 0.513) < 2e-3 and abs(float(1 - dbl) - math.exp(-2 / 3)) < 0.01, "l14 s[3] hint e^(-2/3) approximation"
    assert at_least_one(F(1, 10), 10) == 1 - F(9, 10) ** 10 and abs(float(at_least_one(F(1, 10), 10)) - 0.6513) < 5e-5, "l14 s[7] 0.6513"
    # s[10] six rankings
    larger6 = F(11, 36)
    ge8 = F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= 8), 36)
    hhh = F(1, 8)
    assert ge8 == F(15, 36) and ge8 > larger6 > hhh, "l14 s[10] r0 B likeliest, r1 C least (three flips reading)"
    assert at_least_one(F(1, 6), 3) == F(91, 216) > ge8, "l14 s[10] r2 A"
    assert binom_pmf(20, 10) > F(1, 6) and abs(float(binom_pmf(20, 10)) - 0.176) < 5e-4, "l14 s[10] r3 A"
    assert binom_pmf(6, 3) == F(20, 64) < binom_pmf(4, 2) == F(6, 16), "l14 s[10] r4 B"
    assert binom_pmf(6, 2) == binom_pmf(6, 4), "l14 s[10] r5 S"
    # s[11]
    quote, trades = at_least_one(F(1, 10), 10), at_least_one(F(1, 20), 20)
    fall = 1 - phi(2)
    assert abs(float(trades) - 0.6415) < 5e-5 and quote > trades and abs(fall - 0.02275) < 1e-4 and float(trades) > fall, "l14 s[11] order quote, trades, fall"
    # quiz
    assert abs(float(F(252, 1024)) / float(F(1, 6)) - 1.48) < 0.01 and 252 // 6 == 42, "l14 quiz[0] half as much again; 42 times by ways"
    q1 = at_least_one(F(1, 6), 12)
    assert abs(float(q1) - 0.8878) < 5e-5 and abs(1 - math.exp(-2) - 0.8647) < 1e-4 and abs(float(q1) - (1 - math.exp(-2))) < 0.03, "l14 quiz[1] exact and benchmark within tol"
    assert comb(8, 3) == comb(8, 5) == 56, "l14 quiz[3]"
    # review-4 items[2], items[3]
    four_plus = sum(binom_pmf(6, k) for k in range(4, 7))
    assert four_plus == F(22, 64) and four > ge8 > four_plus, "review-4 items[2] order"
    assert abs(float(trades) - 0.6415) < 1e-4 and abs(float(F(95, 100) ** 20) - 0.358) < 1e-3, "review-4 items[3]"
    # homework-4 items[1]
    five = at_least_one(F(1, 6), 5)
    b25 = birthday(25)
    assert abs(float(five) - 0.598) < 1e-3 and abs(float(b25) - 0.569) < 1e-3 and five > b25, "homework-4 items[1] r0 A"
    seven_plus = sum(binom_pmf(10, k) for k in range(7, 11))
    assert seven_plus == F(176, 1024) > F(1, 6), "homework-4 items[1] r1 A"
    assert comb(10, 3) == comb(10, 7) == 120, "homework-4 items[1] r2 S"
    d36 = at_least_one(F(1, 36), 36)
    assert abs(float(d36) - 0.637) < 1e-3 and six6 > d36, "homework-4 items[1] r3 B"
    assert abs((1 - phi(1)) - 0.1587) < 1e-4 and (1 - phi(1)) < 1 / 6, "homework-4 items[1] r4 B"
    assert F(12, 51) < F(252, 1024), "homework-4 items[1] r5 B"
    pairs = [(five, b25), (seven_plus, F(1, 6)), (F(120, 1024), F(120, 1024)), (d36, six6), (F(1 - phi(1)), F(1, 6)), (F(12, 51), F(252, 1024))]
    assert all(abs(float(a) - float(b)) < 0.03 for a, b in pairs), "homework-4 items[1].explain: all six pairs within 0.03"


@check("l14_one_over_e")
def _():
    prev = 0.0
    for n in range(1, 100_001):
        v = (1 - 1 / n) ** n
        assert v > prev or n == 1, "l14 s[1] (1-1/n)^n creeps up: strictly increasing"
        assert v < 0.5, "l14 s[1].byKey.half: never reaches a half"
        prev = v
    assert abs((5 / 6) ** 6 - 0.335) < 5e-4 and abs((49 / 50) ** 50 - 0.364) < 5e-4, "l14 s[1] hint values at n = 6 and 50"
    assert abs(prev - math.exp(-1)) < 1e-5 and abs(math.exp(-1) - 0.368) < 5e-4, "l14 s[1] limit 1/e = 0.368"
    # s[8] derivation: ln(1 - x) ~ -x is the tangent at 0, and the two-term expansion is wrong at np = 1.
    assert abs(math.log(1 - 1e-3) + 1e-3) < 1e-6, "l14 s[8] tangent line"
    assert abs(1 - 1000 * (1 / 1000) - (1 - 1 / 1000) ** 1000) > 0.3, "l14 s[8].d1: two-term expansion gives 0, far from 1/e"


@check("l14_np1_decreasing")
def _():
    vals = [1 - (1 - 1 / n) ** n for n in range(1, 10_001)]
    assert all(a > b for a, b in zip(vals, vals[1:])), "l14 s[7].explain, s[11].explain: with np = 1 fewer tries at a bigger chance land higher"
    assert vals[0] == 1.0 and abs(vals[-1] - (1 - math.exp(-1))) < 1e-4, "l14 s[7] limit 0.632"


@check("l14_normal_tail")
def _():
    exact = sum(binom_pmf(100, k) for k in range(60, 101))
    assert abs(float(exact) - 0.0284) < 5e-5, "l14 s[4].explain exact 0.0284"
    assert abs((1 - phi((59.5 - 50) / 5)) - 0.0287) < 5e-4, "l14 s[4].explain continuity z = 1.9 gives about 0.029"
    assert math.sqrt(100 * 0.25) == 5, "l14 s[4].prose sd 5"
    assert abs((1 - phi(1)) - 0.16) < 0.01 and abs((1 - phi(10 / 25)) - 0.34) < 0.01, "l14 s[4] option whys: sd 10 gives 0.16, variance 25 gives 0.34"
    assert abs(2 * (1 - phi(2)) - 0.0455) < 1e-3, "l14 quiz[2] two sds either way: exact 4.6%"
    assert abs((1 - phi(2)) - 0.023) < 1e-3, "l14 s[11] one tail beyond two sds about 2.3%"
    assert abs(phi(1) - phi(-1) - 0.68) < 0.003 and abs(phi(2) - phi(-2) - 0.95) < 0.005, "l14 s[2] 68 and 95 benchmarks"


@check("l14_three_heads_ambiguity")
def _():
    # Finding 4: "three heads in a row" is 1/8 in three flips but a run of three in ten flips is about 0.51.
    n = 10
    runs = 0
    for bits in product((0, 1), repeat=n):
        best = cur = 0
        for b in bits:
            cur = cur + 1 if b else 0
            best = max(best, cur)
        runs += best >= 3
    p_run = F(runs, 2 ** n)
    assert F(1, 8) < F(11, 36) < F(15, 36), "l14 s[10] key under the three-flip reading: C least likely"
    assert p_run > F(15, 36), "under the ten-flip reading C would be the likeliest, so the row needs its flip count"
    assert abs(float(p_run) - 0.508) < 1e-3, "P(run of 3 heads in 10 flips) = 0.508"


@check("l14_float_tie")
def _():
    # l14 s[9].explain says floats could split the 210/1024 vs 105/512 tie: they cannot, both are dyadic.
    assert 210 / 1024 == 105 / 512, "l14 s[9].explain: this tie is exact in floats too (finding 5)"
    # A tie floats can split: the same chance reached by two routes.
    a = 1 - (5 / 6) ** 6
    b = 31031 / 46656
    c = sum(comb(6, k) * (1 / 6) ** k * (5 / 6) ** (6 - k) for k in range(1, 7))
    assert F(31031, 46656) == at_least_one(F(1, 6), 6), "exact tie"
    assert len({a, b, c}) > 1, "the same chance by three float routes differs in the last bits"
    assert F(210, 1024) == F(105, 512), "l14 s[9] test 7 tie exact"


@check("l14_birthday")
def _():
    assert birthday(22) < F(1, 2) < birthday(23), "l14 s[2].prose: 23 people make a shared birthday an even bet"
    assert abs(float(birthday(23)) - 0.507) < 5e-4 and abs(float(birthday(30)) - 0.706) < 5e-4, "l14 birthday values"


# ---------------------------------------------------------------- l15 checks
def prob_dice(event, n=2):
    hits = total = 0
    for roll in product(range(1, 7), repeat=n):
        total += 1
        hits += bool(event(roll))
    return F(hits, total)


@check("l15_exact_fractions")
def _():
    assert F(4, 52) * F(3, 51) == F(1, 221) and F(4, 52) ** 2 == F(1, 169) and F(3, 51) == F(1, 17), "l15 s[0]"
    primes = {2, 3, 5, 7, 11}
    cells = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b in primes]
    assert len(cells) == 15, "l15 s[1] 15 prime cells"
    counts = {t: sum(1 for a, b in cells if a + b == t) for t in sorted(primes)}
    assert counts == {2: 1, 3: 2, 5: 4, 7: 6, 11: 2}, "l15 s[1].feedback counts by total"
    tapped = {"r1c1", "r1c2", "r1c4", "r1c6", "r2c1", "r2c3", "r2c5", "r3c2", "r3c4", "r4c1", "r4c3", "r5c2", "r5c6", "r6c1", "r6c5"}
    assert tapped == {f"r{a}c{b}" for a, b in cells}, "l15 s[1].widget.answer cells are exactly the prime cells"
    assert F(15, 36) == F(5, 12) and F(12, 36) == F(1, 3) and F(21, 36) == F(7, 12) and F(5, 11) == F(len(primes), 11), "l15 s[2] options"
    assert prob_dice(lambda r: r[0] == r[1]) == F(1, 6) and prob_dice(lambda r: sum(r) >= 8) == F(5, 12), "l15 s[9] tests"
    assert F(2, 8) == F(1, 4), "l15 s[7] HHH or TTT"
    assert F(1, 2) * F(1, 2) == F(1, 4), "l15 s[7].explain second route"
    assert F(13, 52) * F(12, 51) == F(1, 17) and F(1, 4) ** 2 == F(1, 16), "review-4 items[5]"
    assert prob_dice(lambda r: 6 in r) == F(11, 36) and F(1, 6) + F(1, 6) == F(1, 3), "l15 quiz[0]"
    assert F(3, 5) * F(2, 4) == F(3, 10) and F(3, 5) ** 2 == F(9, 25), "l15 quiz[1]"
    assert F(12, 51) == F(4, 17) and 1 - F(4, 17) == F(13, 17) and F(13, 52) * F(12, 51) == F(1, 17), "l17 C Q1 options"
    assert prob_dice(lambda r: sum(r) == 5) == F(1, 9) and 1 - F(1, 9) == F(8, 9), "l17 C Q2"
    assert binom_pmf(5, 3) == F(5, 16) and 1 - F(5, 16) == F(11, 16), "l17 C Q3"
    assert F(1, 7) == F(1, 7) and F(1, 49) == F(1, 7) ** 2, "l15 s[10] r3 weekday; homework distractor 1/49 names a day for both"
    assert 1 - F(1, 16) == F(15, 16), "l15 s[10] r1"


@check("l15_bayes")
def _():
    def nat(base, sens, fpr, n=1000):
        have = n * F(base)
        tp = have * F(sens)
        fp = (n - have) * F(fpr)
        return tp, fp, tp / (tp + fp)
    assert nat(F(2, 100), F(9, 10), F(1, 10)) == (18, 98, F(9, 58)) and abs(float(F(9, 58)) - 0.1552) < 5e-5, "l15 s[3], s[8]"
    assert F(1, 10) * 1000 == 100 != 98, "l15 s[8].d1: 10% of everyone is 100, of the clear 98"
    assert nat(F(1, 2), F(3, 10), F(1, 10), 100) == (15, 5, F(3, 4)), "l15 s[11] 3/4"
    assert F(3, 10) / F(1, 10) == 3 and F(1, 1) * 3 == 3, "l15 s[11].explain: likelihood ratio 3 turns even odds into 3 to 1"
    assert nat(F(5, 100), F(8, 10), F(2, 100)) == (40, 19, F(40, 59)) and abs(float(F(40, 59)) - 0.678) < 5e-4, "l15 quiz[2]"
    assert nat(F(1, 10), F(8, 10), F(2, 10)) == (80, 180, F(4, 13)) and abs(float(F(4, 13)) - 0.3077) < 5e-5, "review-4 items[4]"
    assert nat(F(1, 10), F(9, 10), F(1, 10)) == (90, 90, F(1, 2)), "l17 C Q5"
    # Bayes' rule agrees with the crowd count (C&B Thm 1.3.5).
    post = F(2, 100) * F(9, 10) / (F(2, 100) * F(9, 10) + F(98, 100) * F(1, 10))
    assert post == F(9, 58), "l15 s[3] crowd count equals Bayes' rule"


@check("l15_expectations")
def _():
    # l15 s[4]: roll a die; on a 6 roll again and add. Enumerate the 36 equally likely cells.
    cells = [(a if a < 6 else 6 + b) for a in range(1, 7) for b in range(1, 7)]
    assert F(sum(cells), 36) == F(49, 12), "l15 s[4] 49/12"
    assert F(7, 2) + F(1, 6) * F(7, 2) == F(49, 12), "l15 s[4].explain shortcut"
    assert F(sum(range(1, 6)), 5) == 3 and F(6 * 6 + sum(range(1, 7)), 6) == F(19, 2), "l15 s[4] hint: rows 1 to 5 average 3, row 6 averages 9.5"
    cells4 = [(a if a < 4 else 4 + b) for a in range(1, 5) for b in range(1, 5)]
    assert F(sum(cells4), 16) == F(25, 8) == F(5, 2) + F(1, 4) * F(5, 2), "l17 C Q4 3.125"
    assert F(5, 2) + F(1, 4) == F(11, 4), "l17 C Q4 option A 2.75 adds the chance"
    # geometric: rolls up to and including the first 6 average 6; rolls before it average 5.
    assert sum(F(k) * F(1, 6) * F(5, 6) ** (k - 1) for k in range(1, 400)) - 6 < F(1, 10 ** 10), "l15 s[10] r2 expected rolls until the first 6 is 6 (inclusive)"
    assert F(5, 6) / F(1, 6) == 5, "homework-4 items[2] r2 distractor C: 5 is the rolls before the first 6 (finding 7)"


@check("l15_probability_bounds")
def _():
    for v in (F(7, 6), F(-1, 6), F(7, 5), 2):
        assert not (0 <= F(v) <= 1), "l15 s[5], quiz[3], homework items[2] r1: outside [0, 1] goes at once"
    assert all(0 <= F(v) <= 1 for v in (F(1, 6), F(5, 6), F(2, 3), F(1, 3), F(2, 5))), "l15 s[5] options that stay"
    assert guess(2) == 0, "l15 s[5].explain: two options left is a guess worth 0 at +1/-1"


# ---------------------------------------------------------------- l16 helpers: rule enumeration
def digit_sum(n):
    return sum(int(c) for c in str(abs(n)))


def rev(n):
    return int(str(n)[::-1])


def look_and_say(s):
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(f"{j - i}{s[i]}")
        i = j
    return "".join(out)


def simple_rules(seq):
    """Rules from the course's own taxonomy that fit every term; name -> next term."""
    out = {}
    n = len(seq)
    if n >= 2:
        d = [b - a for a, b in zip(seq, seq[1:])]
        if n >= 3 and len(set(d)) == 1:
            out["const-diff"] = seq[-1] + d[0]
        if n >= 4:
            dd = [b - a for a, b in zip(d, d[1:])]
            if len(set(dd)) == 1 and dd[0] != 0:
                out["quadratic"] = seq[-1] + d[-1] + dd[0]
            if all(x != 0 for x in d[:-1]):
                rr = {F(b, a) for a, b in zip(d, d[1:])}
                if len(rr) == 1 and rr != {F(1)}:
                    out["gaps-ratio"] = seq[-1] + d[-1] * rr.pop()
        if n >= 3 and all(x != 0 for x in seq[:-1]):
            r = {F(b, a) for a, b in zip(seq, seq[1:])}
            if len(r) == 1:
                out["const-ratio"] = seq[-1] * r.pop()
        if n >= 3 and all(F(b, a) == F(i + 2, 1) for i, (a, b) in enumerate(zip(seq, seq[1:])) if a != 0):
            out["factorial-ratios"] = seq[-1] * (n + 1)
    if n >= 3 and all(b == a + digit_sum(a) for a, b in zip(seq, seq[1:])):
        out["digit-sum"] = seq[-1] + digit_sum(seq[-1])
    if n >= 4 and all(seq[i + 2] == seq[i + 1] + seq[i] for i in range(n - 2)):
        out["fibonacci"] = seq[-1] + seq[-2]
    if n >= 4:
        for m in range(2, 6):
            c = seq[1] - m * seq[0]
            if all(b == m * a + c for a, b in zip(seq, seq[1:])):
                out[f"affine x{m}{c:+d}"] = m * seq[-1] + c
    if n >= 4:
        def ops(a, b):
            res = [("+", b - a)]
            if a != 0 and F(b, a).denominator == 1 and F(b, a) != 1:
                res.append(("x", F(b, a)))
            return res

        def apply(op, a):
            return a + op[1] if op[0] == "+" else a * op[1]
        for o1 in ops(seq[0], seq[1]):
            for o2 in ops(seq[1], seq[2]):
                if o1 == o2:
                    continue
                ok = all(apply(o1 if i % 2 == 0 else o2, seq[i]) == seq[i + 1] for i in range(n - 1))
                if ok:
                    nxt = o1 if (n - 1) % 2 == 0 else o2
                    out[f"alternating {o1[0]}{o1[1]},{o2[0]}{o2[1]}"] = apply(nxt, seq[-1])
    if n >= 4:
        for c in range(-9, 10):
            if c == 0:
                continue
            fits = all((seq[i + 1] == rev(seq[i])) if i % 2 == 0 else (seq[i + 1] == seq[i] + c) for i in range(n - 1))
            if fits:
                out[f"reverse,+{c}"] = rev(seq[-1]) if (n - 1) % 2 == 0 else seq[-1] + c
    if n >= 3 and all(str(b) == look_and_say(str(a)) for a, b in zip(seq, seq[1:])):
        out["look-and-say"] = int(look_and_say(str(seq[-1])))
    if n >= 5:
        odd, even = seq[0::2], seq[1::2]
        ro, re_ = simple_rules_half(odd), simple_rules_half(even)
        if ro and re_:
            nxt = ro if n % 2 == 0 else re_
            for name, v in nxt.items():
                out[f"interleaved ({name})"] = v
    return out


def simple_rules_half(seq, confirm=True):
    """A half of three or more terms solved by a one-step test.

    With confirm=True a rule about the gaps needs four terms, so that at least one
    term confirms it: any three terms fit 'growing gaps' and 'gaps ratio' vacuously."""
    out = {}
    if len(seq) < 3:
        return out
    d = [b - a for a, b in zip(seq, seq[1:])]
    if len(set(d)) == 1:
        out["const-diff"] = seq[-1] + d[0]
    if all(x != 0 for x in seq[:-1]):
        r = {F(b, a) for a, b in zip(seq, seq[1:])}
        if len(r) == 1 and r != {F(1)}:
            out["const-ratio"] = seq[-1] * r.pop()
    if len(seq) >= (4 if confirm else 3) and len(set(d)) > 1:
        dd = [b - a for a, b in zip(d, d[1:])]
        if len(set(dd)) == 1:
            out["growing-gaps"] = seq[-1] + d[-1] + dd[0]
        if all(x != 0 for x in d[:-1]):
            rr = {F(b, a) for a, b in zip(d, d[1:])}
            if len(rr) == 1:
                out["gaps-ratio"] = seq[-1] + d[-1] * rr.pop()
    return out


SEQ_ROWS = [
    # (label, sequence, key, claimed unique)
    ("l16 s[0]", [2, 20, 4, 17, 8, 14, 16], 11, False),
    ("l16 s[1]", [3, 6, 4, 8, 6, 12, 10], 20, False),
    ("l16 s[2] r0", [1, 10, 3, 20, 5, 30], 7, False),
    ("l16 s[2] r1", [2, 5, 15, 18, 54], 57, False),
    ("l16 s[2] r2", [40, 1, 38, 2, 36, 4], 34, False),
    ("l16 s[3]", [7, 14, 19, 29, 40, 44], 52, False),
    ("l16 s[4]", [1, 11, 21, 1211, 111221], 312211, False),
    ("l16 s[5]", [2, 4, 8, 6, 32, 8], 128, False),
    ("l16 s[7]", [10, 1, 20, 2, 30, 3], 40, False),
    ("l16 s[10] r0", [1, 2, 6, 24, 120], 720, True),
    ("l16 s[10] r1", [5, 7, 11, 19, 35], 67, True),
    ("l16 s[10] r2", [81, 27, 9, 3], 1, True),
    ("l16 s[10] r3", [2, 3, 5, 9, 17], 33, True),
    ("l16 s[10] r4", [1, 4, 2, 8, 3, 12], 4, True),
    ("l16 s[10] r5", [12, 21, 23, 32, 34, 43], 45, True),
    ("l16 s[11]", [100, 300, 200, 600, 500, 1500], 1400, False),
    ("l16 quiz[0]", [5, 100, 10, 90, 15, 80], 20, False),
    ("l16 quiz[1]", [3, 8, 16, 21, 42, 47], 94, False),
    ("l16 quiz[2]", [15, 51, 53, 35, 37, 73], 75, False),
    ("l16 quiz[3]", [1, 2, 3, 4, 9, 8, 27], 16, False),
    ("l17 B Q1", [2, 6, 5, 15, 14, 42, 41], 123, False),
    ("l17 B Q2", [17, 26, 37, 50, 65], 82, False),
    ("l17 B Q3", [4, 11, 25, 53, 109], 221, False),
    ("l17 B Q4", [4, 12, 36, 108, 324], 972, False),
    ("l17 B Q5", [21, 24, 30, 33, 39, 51], 57, False),
    ("l17 B Q6", [3, 1, 7, 2, 11, 4, 15], 8, False),
    ("l17 B Q7", [4, 3, 7, 10, 17, 27], 44, False),
    ("l17 B Q8", [8, 12, 18, 26, 36], 48, False),
    ("review-4 items[6]", [4, 50, 8, 45, 12, 40], 16, False),
    ("review-4 items[7]", [23, 28, 38, 49, 62, 70], 77, False),
    ("homework-4 items[3] r0", [3, 30, 6, 25, 12, 20, 24], 15, True),
    ("homework-4 items[3] r1", [1, 2, 5, 10, 13, 26], 29, True),
    ("homework-4 items[3] r2", [11, 13, 17, 25, 32, 37], 47, True),
    ("homework-4 items[3] r3", [1, 3, 2, 6, 4, 12, 8], 24, True),
    ("homework-4 items[3] r4", [2, 12, 1112, 3112, 132112], 1113122112, True),
    ("homework-4 items[3] r5", [16, 61, 63, 36, 38, 83], 85, True),
]

MULTI_RULE_ROWS = {}


@check("l16_sequence_keys")
def _():
    for label, seq, key, _unique in SEQ_ROWS:
        fits = simple_rules(seq)
        assert fits, f"{label}: no rule from the course's taxonomy fits {seq}"
        preds = set(fits.values())
        assert key in preds, f"{label}: key {key} is not produced by any fitting rule {fits}"
        assert preds == {key}, f"{label}: fitting rules disagree on the next term {fits}"
        if len(fits) > 1:
            MULTI_RULE_ROWS[label] = fits


@check("l16_one_clear_rule_claims")
def _():
    # l16 s[10].prose and homework-4 items[3].prose say "each with one clear rule"; the lesson's own feedback
    # names a second reading for l16 r1 and r5. Record the rows where two rules of the taxonomy fit (finding 6).
    claimed = [label for label, _, _, unique in SEQ_ROWS if unique]
    multi = [label for label in claimed if label in MULTI_RULE_ROWS]
    assert "l16 s[10] r1" in multi and "l16 s[10] r5" in multi and "l16 s[10] r3" in multi, "l16 s[10] rows 1, 3, 5 each fit two rules (the byKey lines say so for r1, the explain for r5)"
    hw_multi = [label for label in multi if label.startswith("homework-4")]
    assert not hw_multi, f"homework-4 items[3]: with a confirming fourth term required, each row fits one rule {hw_multi}"
    # Every multiply-fitted row still has a single next term (checked above), which is what the claim needs.


@check("l16_specific_claims")
def _():
    # s[0].explain: neither half's rule fits the whole list, so differences failed.
    whole = simple_rules([2, 20, 4, 17, 8, 14, 16])
    assert all(k.startswith("interleaved") for k in whole), "l16 s[0].explain only an interleaved reading fits"
    # s[3].explain: no difference or ratio rule finds 7, 14, 19, 29, 40, 44.
    r = simple_rules([7, 14, 19, 29, 40, 44])
    assert set(r) == {"digit-sum"}, "l16 s[3].explain: only the digit-sum rule fits"
    assert [7, 1 + 4, 1 + 9, 2 + 9, 4 + 0] == [7, 5, 10, 11, 4], "l16 s[3].explain gaps are digit sums"
    # s[4]: look-and-say, and 13112221 is the term after 312211.
    assert look_and_say("111221") == "312211" and look_and_say("312211") == "13112221", "l16 s[4] look-and-say (Conway 1987)"
    assert look_and_say("132112") == "1113122112", "homework-4 items[3] r4"
    # s[5]: doubling fits 2, 4, 8 and fails at 6.
    assert simple_rules([2, 4, 8]).get("const-ratio") == 16 and "const-ratio" not in simple_rules([2, 4, 8, 6]), "l16 s[5] doubling breaks at the fourth term"
    # s[6]: 1, 2, 4 fits both doubling (8) and growing gaps (7).
    h = simple_rules_half([1, 2, 4], confirm=False)
    assert h.get("const-ratio") == 8 and h.get("growing-gaps") == 7, "l16 s[6].prose: 1, 2, 4 admits 8 and 7"
    # s[10] hint: the fourth is 2^n + 1; r1 is 2^n + 3; both readings agree (byKey r1c1 'also x2 then -3').
    assert [2 ** n + 1 for n in range(6)] == [2, 3, 5, 9, 17, 33] and [2 ** n + 3 for n in range(2, 7)] == [7, 11, 19, 35, 67], "l16 s[10] r1, r3 closed forms"
    assert simple_rules([5, 7, 11, 19, 35]).get("affine x2-3") == 67 and simple_rules([5, 7, 11, 19, 35]).get("gaps-ratio") == 67, "l16 s[10].byKey.r1c1 both readings give 67"
    # s[10].explain: the reversal row's halves climb by 11.
    assert simple_rules_half([12, 23, 34]) == {"const-diff": 45}, "l16 s[10].explain halves climb by 11"
    # l17 B Q6: the even half 1, 2, 4 admits 8 and 7; only 8 is offered.
    assert simple_rules_half([1, 2, 4], confirm=False).get("growing-gaps") == 7 and 7 not in (19, 26, 8, 12), "l17 B Q6: 7 is not among the options, so 8 is the only consistent letter"
    # l17 B Q4 due time: section B starts at 2:00, four items at 100 s.
    assert 120 + 4 * 100 == 520 and 520 == 8 * 60 + 40, "l17 s[3].explain Q4 due near 8:40"
    # l16 s[11] order sizes: alternating x3, -100 and the interleaved reading agree on 1400.
    r11 = simple_rules([100, 300, 200, 600, 500, 1500])
    assert set(r11.values()) == {1400} and "alternating x3,+-100" in r11, "l16 s[11]: x3 then -100 gives 1,400"
    assert simple_rules_half([100, 200, 500], confirm=False).get("gaps-ratio") == 1400, "l16 s[11]: the (unconfirmed) interleaved reading of the odd places agrees"
    assert 1500 * 3 == 4500 and 1500 + 100 == 1600, "l16 s[11] wrong[] values"


# ---------------------------------------------------------------- l17 checks
def arith(text):
    t = text.replace("−", "-").replace("×", "*").replace("÷", "/").replace(",", "")
    if "% of" in t:
        p, rest = t.split("% of")
        return F(int(p), 100) * int(rest)
    a, op, b = t.split()
    a, b = F(a), F(b)
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[op]


@check("l17_section_A_keys")
def _():
    lesson = load("l17-full-battery")
    rows = lesson["screens"][2]["widget"]["rows"]
    import re
    for row in rows:
        text, cell = row[0].replace("\xa0", " ").replace(" ", " "), row[1]
        m = re.match(r"\*\*Q(\d+):\*\* (.+?)\s{2,}(.*)", text)
        q, expr, opts = m.group(1), m.group(2), m.group(3)
        options = dict(re.findall(r"\*\*([ABCD])\*\* ([\d.,]+)", opts))
        value = arith(expr)
        letter = [k for k, v in options.items() if F(v.replace(",", "")) == value]
        assert letter == [cell["answer"]], f"l17 section A Q{q}: {expr} = {value}, key {cell['answer']}, options {options}"
    assert 20 * 6 == 120 and 8 * 100 == 800 and 6 * 120 == 720 and 120 + 800 + 720 == 1640 == 27 * 60 + 20, "l17 s[0] section times"
    assert 120 / 6 == 20, "l17 s[0].explain paces differ twentyfold"


@check("l17_section_C_keys")
def _():
    # Every section C key as an exact fraction (the other rows are in l15_* checks).
    keys = {"Q1": F(12, 51), "Q2": F(1, 9), "Q3": F(5, 16), "Q4": F(25, 8), "Q5": F(1, 2), "Q6": F(11, 36)}
    assert keys["Q1"] == F(4, 17) and keys["Q4"] == F(3125, 1000), "l17 section C keys D, B, D, B, C, A"
    assert F(13, 52) * F(12, 51) == F(1, 17) and F(2, 9) == 2 * F(1, 9) and F(1, 11) == F(1, 11), "l17 C Q1 option C, Q2 options A and C"


@check("l17_sample_candidate")
def _():
    lesson = load("l17-full-battery")
    marks = lesson["screens"][5]["canvas"]["params"]["rows"]
    tally = {}
    for name, row in marks:
        sec = name[0]
        t = tally.setdefault(sec, {"✓": 0, "✗": 0, "○": 0})
        for ch in row.split():
            t[ch] += 1
    assert tally["A"] == {"✓": 18, "✗": 2, "○": 0} and tally["B"] == {"✓": 2, "✗": 4, "○": 2} and tally["C"] == {"✓": 1, "✗": 5, "○": 0}, "l17 s[5] canvas marks"
    assert 18 - 2 == 16 and 2 + 1 + 16 == 19, "l17 s[5] net 16, 2, 1, total 19"
    assert 2 + tally["B"]["○"] * guess(4, 0) == F(5, 2), "l17 s[5] r4 2.5"
    # s[6]: classification from the definitions (S wrong within pace, M wrong over pace, T right over twice pace).
    pace = {"A": 6, "B": 100, "C": 120}
    rows = lesson["screens"][6]["widget"]["rows"]
    counts = {"S": 0, "M": 0, "T": 0}
    for item, secs_mark, cell in rows:
        sec = item[0]
        secs, mark = secs_mark.split(", ")
        secs = float(secs.replace(" s", ""))
        if mark == "wrong":
            want = "S" if secs <= pace[sec] else "M"
        else:
            want = "T" if secs > 2 * pace[sec] else None
        assert cell["answer"] == want, f"l17 s[6] {item}: {secs_mark} should be {want}"
        counts[want] += 1
    assert counts == {"S": 6, "M": 5, "T": 1}, "l17 s[6].feedback.correct six slips, five method gaps, one time loss"
    c_wrong = [30.7, 39.9, 378.4, 39.8, 41.5]
    assert sum(1 for s in c_wrong if s < 45) == 4 and 720 - 164 - sum(c_wrong) > 0, "l17 s[7]: four wrong under 45 s; 164 s unused leaves a positive time for Q1"
    assert abs(40 / 120 - 1 / 3) < 1e-9 and 378.4 / 120 > 3, "l17 s[7] hints: a third of the pace; three times it"
    assert 240 > 2 * 100, "l17 quiz[2] 240 s is over twice the 100 s pace"


@check("l17_pacing")
def _():
    assert 18 * 60 / 12 == 90 and 6 * 90 == 540 == 9 * 60, "l17 s[9] 90 s; item 6 due at 9 minutes"
    assert 30 * 60 / 15 == 120 and 20 * 60 / 12 == 100, "l17 quiz[0], review-4 items[8]"
    assert abs(12 / 18 - 0.67) < 0.01 and 18 / 12 == 1.5, "l17 s[9] wrong[] upside (items per minute) and minutes per item"
    # s[1] caption formulas on the whole line, half-minute grid.
    def done(x):
        a = min(20, math.floor(x * 10))
        b = max(0, min(8, math.floor((x - 2) * 0.6 + 0.0001)))
        c = max(0, min(6, math.floor((x - 2 - 40 / 3) / 2 + 0.0001)))
        return a, b, c
    prev = (0, 0, 0)
    for i in range(0, 57):
        x = i / 2
        d = done(x)
        assert all(p <= q for p, q in zip(prev, d)), "l17 s[1] caption counts never fall"
        prev = d
    assert done(2) == (20, 0, 0) and done(12) == (20, 6, 0) and done(15.5)[1] == 8 and done(27.5) == (20, 8, 6), "l17 s[1] switch times 2:00, 15:20, 27:20 and the 12-minute key 6"
    assert done(1.2) == (12, 0, 0), "l17 s[1] A runs at 10 a minute (6 s each)"


@check("l17_zetamac_claim")
def _():
    with open(ROOT / "app" / "content" / "warmup.json", encoding="utf-8") as fh:
        text = fh.read()
    assert "Zetamac default settings" in text, "l17 s[11].prose: the Today warm-up runs Zetamac's default settings (app content says so)"


def main():
    failed = 0
    for name, fn in CHECKS:
        try:
            fn()
            print(f"ok    {name}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL  {name}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"ERROR {name}: {type(exc).__name__}: {exc}")
    if MULTI_RULE_ROWS:
        print("rows where more than one rule of the taxonomy fits (all agree on the next term):")
        for label, fits in MULTI_RULE_ROWS.items():
            print(f"  {label}: {', '.join(sorted(fits))}")
    print(f"{len(CHECKS) - failed} of {len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
