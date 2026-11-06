#!/usr/bin/env python3
"""Concept checks for mental-pressure level 2 (l5 to l8, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/mental-pressure-L2-concepts.py
Each check names its ledger row (docs/reports/audit-mental-pressure-1-3-ledger.md).
Exit 0 means every checked claim holds.
"""
import math
import random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP


def check(name, cond, msg):
    assert cond, f"{name}: {msg}"
    print(f"ok  {name}")


# ---- l5: a/b > c/d iff ad > bc (b, d > 0), exhaustive to denominator 30; gap formula
def cross_compare():
    n = 0
    for b in range(1, 31):
        for d in range(1, 31):
            for a in range(0, b + 1):
                for c in range(0, d + 1):
                    assert (F(a, b) > F(c, d)) == (a * d > b * c), f"cross_compare {a}/{b} vs {c}/{d}"
                    assert F(a, b) - F(c, d) == F(a * d - b * c, b * d), "gap formula"
                    n += 1
    print(f"ok  cross_compare ({n} pairs)")
    check("gap_examples", F(7, 12) - F(5, 9) == F(1, 36) and F(4, 7) - F(5, 9) == F(1, 63)
          and F(5, 6) - F(4, 5) == F(1, 30) and F(13, 17) - F(16, 21) == F(1, 357) and F(5, 8) - F(8, 13) == F(1, 104),
          "l5 screens[5], quiz[1], quiz[2], review-2 items[4], homework-2 items[4]")
    check("tops_bottoms_trap", F(9, 11) > F(13, 16) and 9 * 16 > 13 * 11, "l5 screens[6]: both numbers smaller, fraction bigger")
    check("equal_products", 6 * 21 == 9 * 14 and F(6, 14) == F(9, 21) == F(3, 7), "l5 quiz[0]")


def gap_to_one():
    # near 1, the smaller gap to 1 wins; the half benchmark
    for b in range(2, 31):
        for d in range(2, 31):
            x, y = F(b - 1, b), F(d - 1, d)
            assert (x > y) == (1 - x < 1 - y), "gap to one"
    check("gap_to_one", F(7, 9) > F(10, 13) and F(2, 9) < F(3, 13) and F(12, 13) > F(11, 12),
          "l5 screens[3], screens[10] row 7")
    check("half_benchmark", F(5, 11) < F(1, 2) < F(4, 7) and F(3, 7) < F(1, 2) < F(5, 9) and F(7, 13) > F(1, 2),
          "l5 quiz[3], screens[3] row 1, homework-2 row 13")
    # finding 5: "smaller pieces make a fraction smaller" holds only at equal counts
    check("smaller_pieces_hypothesis", F(5, 11) < F(5, 7) and not (F(3, 4) < F(1, 2)),
          "l5 quiz[3] why.den needs the equal-count hypothesis (finding 5)")


def float_fail():
    a, b, c, d = 10 ** 17 + 1, 10 ** 17, 10 ** 17 + 2, 10 ** 17 + 1
    check("float_fail", F(a, b) > F(c, d) and not (a / b > c / d) and a * d - b * c == 1,
          "l5 screens[9]: exact products decide where floats tie")
    check("sort_stable", sorted([(6, 14), (1, 2), (9, 21)], key=lambda p: F(*p)) == [(6, 14), (9, 21), (1, 2)],
          "l5 screens[9]: equal fractions keep their first order")


def implied_odds():
    # fractional odds a to b: fair implied probability b / (a + b)
    check("implied_odds", abs(12 / 19 - 0.632) < 0.001 and abs(9 / 14 - 0.643) < 0.001 and 12 / 19 < 9 / 14,
          "l5 screens[11].explain: the better payout implies the lower chance")


# ---- l6: growth factors, p^2 loss, undo rules, points against percent
def up_down_p2():
    for k in range(0, 101):
        p = k / 100
        assert abs((1 + p) * (1 - p) - (1 - p * p)) < 1e-12
    check("up_down_p2", abs(1.1 * 0.9 - 0.99) < 1e-12 and abs(1.2 * 0.8 - 0.96) < 1e-12 and abs(1.5 * 0.5 - 0.75) < 1e-12
          and abs(1.3 * 0.7 - 0.91) < 1e-12 and abs(1.4 * 0.6 - 0.84) < 1e-12 and abs(1.12 * 0.88 - 0.9856) < 1e-12,
          "l6 screens[1], [7], review-2 items[1], homework-2 row 2, l11 screens[2]")
    check("chain", abs(1.2 * 1.3 - 1.56) < 1e-12 and abs(1.05 * 0.9 * 1.2 - 1.134) < 1e-12 and abs(1.2 ** 3 - 1.728) < 1e-12
          and abs(0.8 * 0.75 - 0.6) < 1e-12 and abs(1.25 * 0.8 - 1) < 1e-12,
          "l6 screens[2], [3], [11], quiz[0], homework-2 row 18")


def undo_rise():
    for k in range(1, 200):
        p = k / 100
        assert abs((1 + p) * (1 - p / (1 + p)) - 1) < 1e-12, "undo a rise"
        assert p / (1 + p) < p, "the fall is smaller than the rise it undoes"
        if p < 1:
            assert abs((1 - p) * (1 + p / (1 - p)) - 1) < 1e-12, "undo a loss"
            assert p / (1 - p) > p, "the gain is larger than the loss it undoes"
    check("undo_rise", abs(0.2 / 1.2 - 1 / 6) < 1e-12 and abs(0.25 / 1.25 - 0.2) < 1e-12 and abs(0.5 / 0.5 - 1) < 1e-12
          and abs(0.25 / 0.75 - 1 / 3) < 1e-12 and abs(0.4 / 0.6 - 2 / 3) < 1e-12 and abs(0.6 / 0.4 - 1.5) < 1e-12,
          "l6 screens[5], [6], drill rows, review-2 items[8], homework-2 items[5]")

    def reverse_change(p):
        return None if p == -100 else -100 * p / (100 + p)
    check("reverse_change", reverse_change(-100) is None and abs(reverse_change(-50) - 100) < 1e-9
          and abs(reverse_change(20) + 100 / 6) < 1e-9, "l6 screens[9]: None at -100, 100 for -50")
    check("points_vs_percent", (5 - 4, (5 - 4) / 4) == (1, 0.25) and abs((1.5 - 2) / 2 + 0.25) < 1e-12
          and abs((6.5 - 5) / 5 - 0.3) < 1e-12 and abs((4 - 5) / 5 + 0.2) < 1e-12 and abs((3 - 2.5) / 2.5 - 0.2) < 1e-12,
          "l6 screens[4], quiz[2], review-2 items[5]: points subtract, percent divides by the old rate")


# ---- l7: relative errors add to first order; every hinted estimate is within 5%
def relerr_add():
    worst = 0
    for i in range(-50, 51):
        for j in range(-50, 51):
            ea, eb = i / 1000, j / 1000
            exact = (1 + ea) * (1 + eb) - 1
            worst = max(worst, abs(exact - (ea + eb)))
            assert abs(exact - (ea + eb) - ea * eb) < 1e-15
    check("relerr_add", worst <= 0.0025 + 1e-12, f"l7 screens[7], [8]: the cross term is at most 0.25% at 5% each (worst {worst:.4f})")
    ea, eb = 50 / 48 - 1, 50 / 52 - 1
    check("relerr_48_52", abs(ea * eb + 0.0016) < 0.0001 and abs(ea + eb - 0.0032) < 0.0001 and abs(2500 / 2496 - 1 - 0.0016) < 0.0001,
          "l7 screens[8].explain: sum 0.3%, cross term -0.16%, true 0.16%")
    check("relerr_examples", abs(2750 / 2496 - 1.102) < 0.001 and abs(2250 / 2496 - 0.901) < 0.001
          and abs(2500 / 2162 - 1.156) < 0.001 and abs(2025 / 2162 - 0.937) < 0.001 and abs(20 / 17.94 - 1.115) < 0.001
          and abs(1 / 0.98 ** 2 - 1.041) < 0.001 and abs(4900 / 4964 - 0.987) < 0.001,
          "l7 screens[1], [6], [7], quiz[2], screens[10].explain")
    check("rounding_sf_bound", all(abs(float(f"{x:.3g}") / x - 1) <= 0.005 + 1e-12 for x in range(1000, 100000, 7))
          and max(abs(float(f"{x:.2g}") / x - 1) for x in range(1000, 100000, 7)) <= 0.05 + 1e-12,
          "homework-2 items[1].explain: three figures cost at most about 0.5% each, two up to 5%")


ESTIMATES = [  # (exact, hinted estimate, where)
    (3.14 * 2.7, 8.5, "l7 screens[3] row 1"), (0.49 * 812, 400, "l7 screens[3] row 2"), (19 * 21, 400, "row 3"),
    (6.9 * 4.1, 28, "row 4"), (4.2e6 * 3.1e3 / 1e9, 13, "l7 screens[4]"), (46 * 47, 2160, "l7 screens[6]"),
    (39 * 41, 1600, "drill 1"), (73 * 68, 5000, "drill 2"), (2.9 * 6.1, 18, "drill 3"), (0.51 * 380, 190, "drill 4"),
    (998 * 47, 47000, "drill 5"), (1.9 * 1.9, 3.6, "drill 6"), (24 * 26, 625, "drill 7"), (0.32 * 4100, 1300, "drill 8"),
    (58 * 0.25, 14.5, "drill 9"), (3300 * 210, 690000, "drill 10"), (87 * 93, 8100, "drill 11"), (12.4 * 7.9, 98, "drill 12"),
    (4800 * 51.9, 250000, "l7 screens[11]"), (6.2 * 49, 300, "l7 quiz[0]"), (31 * 49, 1500, "l7 quiz[1]"),
    (360000 * 2500 / 1e6, 900, "l7 quiz[3]"), (6.8 * 410, 2800, "review-2 items[2]"), (51 * 49, 2500, "homework-2 row 3"),
    (0.26 * 840, 218.4, "homework-2 row 7"), (7.9 * 6.2, 48, "homework-2 row 11"), (2050 * 39, 80000, "homework-2 row 15"),
    (0.98 * 4500, 4410, "homework-2 row 19")]


def drill_estimates():
    for exact, est, where in ESTIMATES:
        assert abs(est - exact) <= 0.05 * exact, f"drill_estimates: {where} estimate {est} is outside 5% of {exact}"
    check("drill_estimates", 2704 > 1.05 * 2496 and 2304 < 0.95 * 2496 and 2500 > 1.05 * 2162 and 2025 < 0.95 * 2162 and 350 > 1.05 * 303.8,
          "l7: every hinted estimate within 5%; every both-up or both-down distractor outside")


# ---- homework-2 items[1]: the harness pairs, three figures pass, two figures miss once at 5.07%
def quick_product():
    g = random.Random(7)
    pairs = [(g.randint(1000, 99999), g.randint(1000, 99999)) for _ in range(20)]

    def rs(x, n):
        return float(f"{x:.{n}g}")
    err3 = [abs(rs(a, 3) * rs(b, 3) - a * b) / (a * b) for a, b in pairs]
    err2 = [abs(rs(a, 2) * rs(b, 2) - a * b) / (a * b) for a, b in pairs]
    check("quick_product", all(e <= 0.05 for e in err3) and max(err3) <= 0.0101,
          f"homework-2 items[1]: three figures pass all 20 (max {max(err3):.4f})")
    misses = [e for e in err2 if e > 0.05]
    check("quick_product_2sf", len(misses) == 1 and abs(max(err2) - 0.0507) < 0.0006,
          f"homework-2 items[1].explain: two figures miss once at 5.07% (got {sorted(err2)[-3:]})")


# ---- l8: tangent above the curve, one Newton step, error bound d^2/(8 n^3)
def tangent_above():
    prev = 0
    for i in range(1, 20001):
        x = i / 100
        line = 7 + (x - 49) / 14
        gap = line - math.sqrt(x)
        assert gap >= -1e-12, f"tangent below the curve at x = {x}"
        if x > 49:
            assert gap >= prev - 1e-12, "the gap must grow to the right of 49"
        prev = gap if x > 49 else 0
    check("tangent_above", abs((7 + 1 / 14) - 7.0714) < 5e-5 and abs(7 + 21 / 14 - 8.5) < 1e-12 and abs(8.5 - math.sqrt(70) - 0.133) < 0.001,
          "l8 screens[1]: 7.0714 at 50, 8.5 against 8.367 at 70")


def nearest_root(n):
    k = math.isqrt(n)
    return k + 1 if (k + 1) ** 2 - n < n - k * k else k


def newton_error_bound():
    worst_ratio, worst = 1.0, None
    total = 0
    for x in range(2, 10001):
        n = nearest_root(x)
        if n * n == x:
            continue
        d = x - n * n
        est = n + d / (2 * n)
        true = math.sqrt(x)
        assert est >= true, f"step not high at {x}"
        assert abs((est * est) - (x + (d / (2 * n)) ** 2)) < 1e-9, "the step's square is high by exactly h^2"
        pred = d * d / (8 * n ** 3)
        err = est - true
        ratio = err / pred
        if x >= 5 and abs(ratio - 1) > abs(worst_ratio - 1):
            worst_ratio, worst = ratio, x
        total += 1
    check("newton_error_bound", abs(worst_ratio - 1) <= 1 / 4,
          f"l8 screens[7]: error about d^2/(8n^3); worst ratio {worst_ratio:.3f} at x = {worst}")
    print(f"    always high and within a quarter of d^2/(8n^3) for every non-square x from 5 to 10,000 ({total} cases)")


def one_place_safe():
    def r1(v):
        return Decimal(repr(v)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    cases = disagree = within = 0
    for x in range(2, 1001):
        n = nearest_root(x)
        if n * n == x:
            continue
        d = x - n * n
        est = n + d / (2 * n)
        true = math.sqrt(x)
        cases += 1
        disagree += r1(est) != r1(true)
        within += abs(est - true) <= 0.05
    rate = disagree / cases
    print(f"    one place: the step disagrees with the true root at one decimal in {disagree} of {cases} ({rate:.1%}); within 0.05 in {within}")
    check("one_place_safe", rate < 0.25, f"l8 screens[4].explain 'one place is usually safe': disagreement {rate:.1%}")


ROOTS = [  # (x, key, tol, where) : the lesson's step from the nearest square must land inside the item's tolerance
    (50, 7.0711, 0.05, "l8 screens[0]"), (130, 11.4018, 0.01, "l8 screens[2]"), (200, 14.1421, 0.05, "l8 screens[3]"),
    (27, 5.1962, 0.05, "l8 screens[3]"), (85, 9.2195, 0.05, "l8 screens[3]"), (70, 8.3666, 0.05, "l8 screens[4]"),
    (40, 6.3246, 0.05, "l8 screens[4]"), (150, 12.2474, 0.05, "l8 screens[4]"), (105, 10.25, 0.01, "l8 screens[7]"),
    (20, 4.4721, 0.05, "drill"), (60, 7.746, 0.05, "drill"), (90, 9.4868, 0.05, "drill"), (120, 10.9545, 0.05, "drill"),
    (300, 17.3205, 0.05, "drill"), (175, 13.2288, 0.05, "drill"), (500, 22.3607, 0.05, "drill"), (80, 8.9443, 0.05, "l8 quiz[0]"),
    (1000, 31.6228, 0.05, "l8 quiz[3]"), (120, 11.0, 0.05, "review-2 items[3]"), (110, 10.4881, 0.05, "homework-2 row 8"),
    (250, 15.8114, 0.05, "homework-2 row 16"), (40, 6.3246, 0.05, "homework-2 row 4")]


def root_keys():
    for x, key, tol, where in ROOTS:
        n = nearest_root(x)
        est = n + (x - n * n) / (2 * n)
        assert abs(est - key) <= tol + 1e-9, f"root_keys: {where} step {est:.4f} outside {key} +- {tol}"
    # scaled roots: 0.5, 0.8, 0.3, 0.6 and the volatility items
    s05 = (7 + 1 / 14) / 10
    s03 = (5.5 - 0.25 / 11) / 10
    check("root_keys", abs(s05 - 0.7071) <= 0.05 and abs(s03 - 0.5477) <= 0.005 and abs((8 - 4 / 16) / 10 - 0.7746) <= 0.05
          and abs(math.sqrt(0.09) - 0.3) < 1e-12, "l8 screens[3], review-2 items[7], homework-2 row 12, l8 quiz[1]")
    check("vol_scaling", abs(20 / math.sqrt(252) - 1.2599) < 1e-4 and abs(20 / (16 - 4 / 32) - 1.26) < 0.005
          and abs(20 / math.sqrt(12) - 5.7735) < 1e-4 and abs(3.5 - 0.25 / 7 - 3.464) < 0.001,
          "l8 screens[11], homework-2 items[6]: annual over root of 252 or 12")


def newton_second_step():
    g = 8.375
    g2 = (g + 70 / g) / 2
    check("newton_second_step", abs(g2 - 8.36660) < 1e-5 and abs(8.375 ** 2 - 70.140625) < 1e-12
          and abs(0.1406 / (2 * 8.375) - 0.0084) < 1e-4, "l8 screens[5]: a second step takes off 0.0084, giving 8.3666")
    g = 1.0
    for _ in range(5):
        g = (g + 2 / g) / 2
    check("newton_sqrt2_steps", abs(g - math.sqrt(2)) < 1e-15, f"l8 screens[9].explain: five steps from 1 reach root 2 to 15 places (got {g!r})")
    check("average_is_step", all(abs((g0 + x / g0) / 2 - (g0 + (x - g0 * g0) / (2 * g0))) < 1e-9 for x in (50, 70, 130) for g0 in (7, 8, 11)),
          "l8 screens[9].explain and homework-2 items[3]: averaging g and x/g is the tangent step")
    check("no_ties", all((k + 1) ** 2 - n != n - k * k for n in range(1, 100001) for k in [math.isqrt(n)]),
          "l8 screens[9]: no number is equidistant from two squares")
    check("bracket", all(x / g0 > math.sqrt(x) > g0 for x, g0 in ((50, 7), (70, 8), (130, 11))) and abs((99 / 14) ** 2 - 50.005) < 0.001,
          "homework-2 items[3]: if g is low, x/g is high; 7.0714^2 = 50.005")


# ---- homework-2 items[7]: the longform model
def hw2_longform():
    base = 7.85e6
    pct = base * 0.042
    check("hw2_pct", abs(pct - 329700) < 1e-6 and abs(base * 0.01 - 78500) < 1e-6 and abs(base * 0.04 + base * 0.002 - pct) < 1e-6,
          "homework-2 items[7].model: 4% + 0.2% of 7.85m is 329,700")
    after = pct * 0.97
    check("hw2_fall", abs(after - 319809) < 1e-6 and abs(pct - 0.03 * 330000 - 319800) < 1e-6 and abs(0.03 * 330000 - 0.03 * pct - 9) < 1e-6,
          "homework-2 items[7].model: 319,809 exactly, 319,800 by the shortcut, the fall 9 high")
    check("hw2_errors", abs(8e6 * 0.042 / pct - 1.019) < 0.001 and abs(base * 0.04 / pct - 0.952) < 0.001
          and abs(0.042 * 0.97 - 0.04074) < 1e-9 and abs(8e6 / base - 1.019) < 0.001,
          "homework-2 items[7].model: +1.9% carries through, 4% is -4.8%, one factor 0.04074")


if __name__ == "__main__":
    cross_compare()
    gap_to_one()
    float_fail()
    implied_odds()
    up_down_p2()
    undo_rise()
    relerr_add()
    drill_estimates()
    quick_product()
    tangent_above()
    newton_error_bound()
    one_place_safe()
    root_keys()
    newton_second_step()
    hw2_longform()
    print("L2 concepts: all checks passed")
