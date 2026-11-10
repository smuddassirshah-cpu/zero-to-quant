#!/usr/bin/env python3
"""Concept checks for number-sense level 3 (l10 to l14, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/number-sense-L3-concepts.py
Each check names its ledger row (docs/reports/audit-number-sense-1-3-ledger.md).
Exit 0 means every checked claim holds on the domain the lesson uses. A line
starting "note" records where a claim stops holding outside that domain; those
are the `imprecise` findings of docs/reviews/audit-number-sense-1-3.md and are
not asserted. A check marked EXPECTED_FAIL fails because the content is wrong
as it stands (a `wrong` finding); it passes once the content is fixed.
"""
import json
import math
import random
import shutil
import subprocess
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F
from pathlib import Path

COURSE = Path("app/content/courses/number-sense")
N = 0
FAILED = []
random.seed(20261109)


def check(name, cond, msg, expected_fail=False):
    global N
    if cond:
        N += 1
        print(f"ok  {name}")
    else:
        tag = "EXPECTED_FAIL" if expected_fail else "FAIL"
        FAILED.append(name)
        print(f"{tag} {name}: {msg}")


def note(name, msg):
    print(f"note {name}: {msg}")


# ---- l10: powers and the index laws
def index_laws():
    bases = [F(b, d) for b in (-5, -3, -2, -1, 1, 2, 3, 5, 7) for d in (1, 2, 3)]
    ok = True
    for a in bases:
        for m in range(-4, 7):
            for n in range(-4, 7):
                ok &= a ** m * a ** n == a ** (m + n)
                ok &= a ** m / a ** n == a ** (m - n)
                ok &= (a ** m) ** n == a ** (m * n)
        ok &= a ** 0 == 1
    check("index_laws", ok, "l10 screens[7], summary.formula: the three laws and a^0 = 1 for every non-zero base tried")
    try:
        F(0) ** 3 / F(0) ** 3
        zero = "defined"
    except ZeroDivisionError:
        zero = "undefined"
    check("zero_base_excluded", zero == "undefined", "l10 screens[7], [8]: the dividing law needs a base other than 0")
    check("power_counts_factors", all(a ** n == math.prod([a] * n) for a in range(-6, 7) for n in range(1, 8)),
          "l10 screens[2], summary.ideas[0]: a^n is n copies of a multiplied")
    check("adding_powers", 2 ** 3 + 2 ** 3 == 2 ** 4 != 2 ** 6 and all(a ** m + a ** m == 2 * a ** m for a in range(2, 9) for m in range(1, 8))
          and not any(a ** m + a ** m == a ** (2 * m) for a in range(3, 9) for m in range(1, 8)),
          "l10 screens[6]: a^m + a^m is 2 x a^m, not a^(2m)")
    check("doubling", abs(1.072 ** 10 - 2) < 0.01 and 1000 * 2 ** 4 == 16000 and abs(1000 * 1.072 ** 40 - 16000) / 16000 < 0.02,
          "l10 screens[9]: 7.2% a year doubles in about 10 years; four doublings multiply by 16")
    check("compound_keys", round(100 * 1.02 ** 2, 2) == 104.04 and round(1000 * 1.02 ** 3, 2) == 1061.21
          and round(500 * 1.03 ** 2, 2) == 530.45 and round(1000 * 1.1 ** 2, 2) == 1210.0
          and abs(1.02 ** 12 - 1.268) < 0.001 and abs(50000 * 1.02 ** 24 - 80422) < 1 and abs(50000 * 1.27 ** 2 - 80645) < 1
          and abs(240 * 1.02 ** 36 - 490) < 1,
          "l10 quiz[3]; l12 screens[8], quiz[4]; review-3 items[5]; homework-3 items[3], items[6]")
    check("two_to_thirty", 2 ** 30 == 1073741824 > 10 ** 9 and 2 ** 10 == 1024, "homework-3 items[8]")


# ---- l11: roots
def roots():
    check("root_definition", all(math.isqrt(b * b) == b for b in range(0, 200)) and (-7) ** 2 == 49 == 7 ** 2,
          "l11 screens[7], quiz[3]: the root sign names the non-negative b with b^2 = a; x^2 = 49 has two solutions")
    ok = True
    for a in range(1, 2000):
        lo = math.isqrt(a)
        ok &= lo * lo <= a < (lo + 1) ** 2 and lo <= math.sqrt(a) < lo + 1
    check("root_between_squares", ok, "l11 screens[3], [7], [8]: a between n^2 and (n+1)^2 puts its root between n and n+1")
    grid = [k / 1000 for k in range(1, 1000)]
    check("roots_below_one", all(math.sqrt(x) > x and x ** (1 / 3) > x for x in grid)
          and all(math.sqrt(x) < x for x in (1.5, 2, 10, 50)),
          "l11 screens[6], summary.ideas[2]: between 0 and 1 a root is bigger than the number")
    check("root_keys", abs(math.sqrt(50) - 7.07) < 0.005 and 4.45 ** 2 < 20 < 4.5 ** 2 and abs(100 ** (1 / 3) - 4.64) < 0.005
          and 38.7 ** 2 < 1500 < 38.75 ** 2 and 3.16 ** 2 < 10 < 3.165 ** 2 and 14 ** 2 < 200 < 15 ** 2
          and 5 ** 2 < 30 < 6 ** 2 and 9 ** 2 < 90 < 10 ** 2 and 20 ** 3 == 8000 and abs(math.sqrt(0.09) - 0.3) < 1e-12,
          "l11 screens[3], [5], [8], quiz; review-3 items[2]; homework-3 items[2], items[5]")


def root_of_time():
    """l11 screens[9], review-3 items[7]: 'risk grows with the square root of time'.
    Monte Carlo: with independent daily moves of sd 1%, the 252-day sd is about 15.87%.
    With positively correlated days (AR(1), rho = 0.3) it is much bigger, so the rule needs independence."""
    def year_sd(rho, reps=5000, days=252):
        totals = []
        scale = math.sqrt(1 - rho * rho)          # keeps each day's sd at 1%
        for _ in range(reps):
            x, s = random.gauss(0, 0.01), 0.0
            for _ in range(days):
                s += x
                x = rho * x + scale * random.gauss(0, 0.01)
            totals.append(s)
        m = sum(totals) / reps
        return math.sqrt(sum((t - m) ** 2 for t in totals) / (reps - 1))
    iid, ar = year_sd(0.0), year_sd(0.3)
    print(f"    252-day sd: independent days {iid:.4f} (rule: {0.01 * math.sqrt(252):.4f}); AR(1) rho 0.3 {ar:.4f}")
    check("root_of_time_iid", abs(iid / 0.1587 - 1) < 0.05 and 0.153 <= 0.1587 <= 0.164 and 3000 * math.sqrt(16) == 12000,
          "l11 screens[9]; review-3 items[7]: independent daily swings of 1% give about 15.9% over 252 days, not 252%")
    check("root_of_time_needs_independence", ar / iid > 1.2,
          "with correlated days the yearly swing is well above sqrt(252) x daily: the rule has a hypothesis")
    note("root_of_time", "the lesson states the rule with no condition (finding 11)")


# ---- l12: order of operations
def order_of_operations():
    check("python_follows_the_convention", 2 + 3 * 4 == 14 and (2 + 3) * 4 == 20 and 10 - 2 * 4 == 2 and 2 * 3 ** 2 == 18
          and 20 - 2 * 3 ** 2 == 2 and 8 - 3 + 2 == 7 and (6 + 4) / 2 == 5 and 3 + 2 * (5 - 1) ** 2 == 35
          and 5 + 3 * 2 ** 2 == 17 and 18 / 3 * 2 == 12 and (12 + 8) / 4 - 1 == 4 and 4 + 6 / 2 * 3 == 13,
          "l12 screens[0] to [7], quiz[0], [1], [3]; review-3 items[3]: every key under the stated ranks, left to right")
    check("unary_minus_and_power", -3 ** 2 == -9 and (-3) ** 2 == 9 and -2 ** 4 == -16 and (-2) ** 4 == 16,
          "l12 quiz[2], summary.ideas[2]; review-3 items[8]: the written convention, which Python shares")
    check("slips_are_not_alternative_readings", (8 - (3 + 2), (2 + 3) * 4, 18 / (3 * 2), 4 + 6 / (2 * 3)) == (3, 20, 3, 5),
          "l12 screens[5], quiz[1]; review-3 items[3]: each wrong[] value needs a grouping the stated ranks exclude")

    # 'Calculators and code follow the same rule' (l12 quiz[2].explain.text).
    # Documented behaviour: Python -3**2 is -9; a spreadsheet formula =-3^2 is 9 (Microsoft Support,
    # 'Calculation operators and precedence in Excel': negation ranks above exponentiation; Google Sheets and
    # LibreOffice Calc agree); JavaScript refuses -3 ** 2 as a SyntaxError (ECMAScript 2016, exponentiation operator).
    tools = {"python": -9, "spreadsheet formula =-3^2": 9, "javascript -3 ** 2": "SyntaxError"}
    node = shutil.which("node")
    if node:
        run = subprocess.run([node, "-e", "console.log(-3 ** 2)"], capture_output=True, text=True)
        js_live = "SyntaxError" if "SyntaxError" in run.stderr else run.stdout.strip()
        print(f"    node -e 'console.log(-3 ** 2)': {js_live}")
        tools["javascript -3 ** 2"] = js_live
    text = json.loads((COURSE / "l12-which-first.json").read_text())["quiz"][2]["explain"]["text"]
    claims_all_tools = "Calculators and code follow the same rule" in text
    all_agree = all(v == -9 for v in tools.values())
    # EXPECTED_FAIL while the sentence stands (finding 10). Corrected assert, true once the sentence names the exception:
    #   check("tools_minus_three_squared", "spreadsheet" in text and "Calculators and code follow the same rule" not in text, ...)
    check("tools_minus_three_squared", all_agree or not claims_all_tools,
          f"l12 quiz[2].explain: 'Calculators and code follow the same rule' is false: {tools}", expected_fail=True)


# ---- l13: one significant figure and estimates
def one_sf(x):
    x = D(str(x))
    exp = x.adjusted()
    return x.quantize(D(1).scaleb(exp), rounding=ROUND_HALF_UP)


def estimation():
    check("one_sf_keys", (one_sf(387), one_sf("0.0372"), one_sf("0.00586"), one_sf(96)) == (400, D("0.04"), D("0.006"), 100)
          and one_sf("0.0372") != D("0.037") and one_sf(48) == 50 and one_sf(312) == 300,
          "l13 screens[1], [2], quiz[0], quiz[3]")
    est = lambda *xs: [one_sf(x) for x in xs]
    a, b = est(48, 21)
    c, d = est(312, 48)
    e, f = est(612, "0.48")
    g, h, i = est("38.7", "5.12", "0.198")
    j, k = est(59, 312)
    m, n = est(4120, "0.21")
    p, q = est("0.62", "0.38")
    r, s = est("23.80", 395)
    t, u = est(2150, "0.38")
    v, w = est(4900, "19.70")
    x1, x2, x3 = est("0.0391", 5870, "19.6")
    y1, y2 = est("0.52", 7890)
    check("estimate_keys", (a * b, c * d, e / f, g * h / i, j * k, m / n, p * q, r * s, t * u, v * w, x1 * x2 / x3, y1 * y2)
          == (1000, 15000, 1200, 1000, 18000, 20000, D("0.24"), 8000, 800, 100000, 12, 4000),
          "l13 screens[0] to [9], quiz[1], [2], [4]; review-3 items[1]; homework-3 items[7]: each key is the unique 1 s.f. estimate")
    # how far can a 1 s.f. rounding move a number? ratio rounded/x over a fine grid of one decade
    ratios = [float(one_sf(D(k) / D(1000))) / (k / 1000) for k in range(1000, 10000)]
    lo, hi = min(ratios), max(ratios)
    print(f"    1 s.f. rounding changes a number by a factor between {lo:.3f} and {hi:.3f}")
    check("ten_times_rule", 0.66 < lo and hi < 1.34 and hi ** 2 / lo < 10 and hi ** 2 < 2,
          "l13 screens[6] hint, screens[7], summary.ideas[1]: a two- or three-number estimate is within a factor of 3, "
          "so a gap of ten means a slip")
    xs = [k / 10 for k in range(1, 2001)]
    ds = [k / 100 for k in range(1, 100)]
    check("dividing_by_between_0_and_1", all(x / d > x for x in xs[::37] for d in ds),
          "l13 screens[4], summary.ideas[2]; l14 quiz[3]: a positive number divided by a number between 0 and 1 gets bigger")
    note("dividing_by_a_number_below_1", f"600 / (-2) = {600 / -2:.0f} and -600 / 0.5 = {-600 / 0.5:.0f} are not bigger, and 600 / 0 "
         "has no value: 'a number below 1' needs 'between 0 and 1' and a positive dividend (finding 12)")


# ---- l14: standard form
def standard(x):
    x = D(str(x))
    n = x.adjusted()
    return x.scaleb(-n).normalize(), n


def standard_form():
    check("standard_form_keys", standard(4500000) == (D("4.5"), 6) and standard(380000) == (D("3.8"), 5)
          and standard("0.00042") == (D("4.2"), -4) and standard("0.0067") == (D("6.7"), -3)
          and standard(450000000) == (D("4.5"), 8) and standard(9 * 10 ** 13) == (D(9), 13) and standard(27 * 10 ** 11) == (D("2.7"), 12),
          "l14 screens[1], [2], [3], [9], quiz[0], quiz[4]")
    check("negative_index", all(F(10) ** -n == F(1, 10 ** n) for n in range(0, 12)) and F(10) ** -2 == F(1, 100),
          "l14 screens[3], [8], summary.ideas[1]: 10^-n = 1/10^n")
    fronts = [F(k, 10) for k in range(10, 100)]
    ok = True
    for _ in range(20000):
        a, b = random.choice(fronts), random.choice(fronts)
        m, n = random.randint(-8, 12), random.randint(-8, 12)
        x, y = a * F(10) ** m, b * F(10) ** n
        if m != n:
            ok &= (x > y) == (m > n)          # the power decides
        else:
            ok &= (x > y) == (a > b)          # the front number only decides ties
        prod = a * b
        ok &= x * y == (prod * F(10) ** (m + n) if prod < 10 else prod / 10 * F(10) ** (m + n + 1))
        ok &= (1 <= prod < 10) or (1 <= prod / 10 < 10)
    check("compare_and_multiply_standard_form", ok,
          "l14 screens[6], [7], summary: compare the powers first; multiply fronts, add indices, move one factor of 10 if needed")
    check("standard_form_products", 3 * 10 ** 4 * 2 * 10 ** 5 == 6 * 10 ** 9 and 4 * 10 ** 3 * 5 * 10 ** 6 == 2 * 10 ** 10
          and F(5, 1000) * 3 * 10 ** 8 == F(15, 10) * 10 ** 6 and F(45, 10) * 10 ** 8 / (9 * 10 ** 13) == F(5, 10 ** 6)
          and 6 * 10 ** 4 / F(3, 100) == 2 * 10 ** 6 and F(72, 10) * 10 ** 5 / (8 * 10 ** 2) == 900
          and F(49, 10) * 10 ** 8 / (7 * 10 ** 12) == F(7, 10 ** 5),
          "l14 screens[4], [5], [7], [9], quiz[3]; review-3 items[4]; homework-3 items[6]")
    ms = 6.5 * 3600 * 252 * 1000
    check("orders_of_magnitude", standard(int(ms))[1] == 9 and abs(ms / 1e9 - 5.9) < 0.01 and 2.4e6 * 50 == 1.2e8
          and 10 ** 6 * 10 ** 6 == 10 ** 12,
          "homework-3 items[4]; review-3 items[6]; l14 quiz[4]: a trillion is a million million")


if __name__ == "__main__":
    index_laws()
    roots()
    root_of_time()
    order_of_operations()
    estimation()
    standard_form()
    if FAILED:
        print(f"L3 concepts: {N} checks passed, {len(FAILED)} failing: {', '.join(FAILED)}")
        sys.exit(1)
    print(f"L3 concepts: all {N} checks passed")
