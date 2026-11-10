#!/usr/bin/env python3
"""Concept checks for numerics level 1 (l1 to l4, review-1, homework-1).

Run from anywhere: python3 docs/reports/numerics-L1-concepts.py
Each check names its ledger rows (docs/reports/audit-numerics-1-3-ledger.md).
Exit 0 means every checked claim holds. A check marked EXPECTED_FAIL fails
because the content is wrong as stated (a `wrong` finding of
docs/reviews/audit-numerics-1-3.md); it is reported, does not change the exit
code, and carries the corrected assert in a comment. A line starting "note"
records where a claim stops holding outside the case the lesson uses (the
`imprecise` findings); notes are measured and printed, not asserted against
the content.

Needs numpy, scipy, mpmath (ships with sympy). About 5 s.
"""
import json
import math
import struct
import sys
import warnings
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
from mpmath import mp, mpf, matrix, lu_solve, exp as mexp
from scipy.stats import norm

COURSE = Path(__file__).resolve().parents[2] / "app/content/courses/numerics"
N = 0
FAILED = []
EXPECTED = []
EPS = 2.0 ** -52
U = 2.0 ** -53


def load(name):
    return json.loads((COURSE / f"{name}.json").read_text(encoding="utf-8"))


def check(name, ok, where, expected_fail=False):
    global N
    if ok:
        N += 1
        if expected_fail:
            print(f"UNEXPECTED_PASS {name}: content may have been fixed; update this check ({where})")
            FAILED.append(name)
        return
    if expected_fail:
        EXPECTED.append(name)
        print(f"EXPECTED_FAIL {name}: {where}")
    else:
        FAILED.append(name)
        print(f"FAIL {name}: {where}")


def note(name, text):
    print(f"note {name}: {text}")


def close(a, b, rel=0.0, abs_=0.0):
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---------------------------------------------------------------- l1
def floating_point():
    eps, k = 1.0, 0
    while 1.0 + eps / 2 > 1.0:
        eps /= 2
        k += 1
    check("epsilon_loop_52", k == 52 and eps == 2.0 ** -52 == np.finfo(float).eps,
          "l1 screens[0]: the loop survives 52 halvings and ends at 2^-52, np.finfo(float).eps")
    check("one_plus_2m53_rounds_to_one", 1.0 + 2.0 ** -53 == 1.0 and 1.0 + 2.0 ** -52 > 1.0,
          "l1 screens[0].hints[2]: 1 + 2^-52 is stored, 1 + 2^-53 rounds to 1 (ties to even)")
    check("epsilon_is_gap_above_one", np.nextafter(1.0, 2.0) - 1.0 == EPS and np.spacing(1.0) == EPS,
          "l1 screens[0].explain, summary.formula.note: machine epsilon 2^-52 is the gap from 1 to the next double")
    # toy format: 3 mantissa bits, powers -1..2
    toy = sorted((1 + m / 8) * 2.0 ** p for p in range(-1, 3) for m in range(8))
    gaps = {p: {round(b - a, 6) for a, b in zip(toy, toy[1:]) if 2.0 ** p <= a < 2.0 ** (p + 1) and b <= 2.0 ** (p + 1)} for p in range(-1, 3)}
    check("toy_format", len(toy) == 32 and toy[0] == 0.5 and toy[-1] == 7.5 and toy[toy.index(4.0) + 1] == 4.5
          and gaps == {-1: {1 / 16}, 0: {1 / 8}, 1: {1 / 4}, 2: {1 / 2}},
          "l1 screens[1]: 32 numbers from 0.5 to 7.5; gap fixed between powers of two and doubling at each; next after 4 is 4.5")

    def decode(x):
        bits = int.from_bytes(struct.pack(">d", x), "big")
        return bits >> 63, ((bits >> 52) & 0x7FF) - 1023, (bits & (2 ** 52 - 1)) / 2 ** 52
    check("decode_fields", decode(-6.5) == (1, 2, 0.625) and decode(100.25) == (0, 6, 0.56640625)
          and decode(0.1) == (0, -4, 0.6000000000000001) and decode(0.01)[1] == -7 and close(0.01 / 2 ** -7, 1.28, rel=1e-15)
          and struct.unpack(">d", bytes.fromhex("4024000000000000"))[0] == 10.0,
          "l1 screens[2..4], [8]; review-1 items[0]; homework-1 items[0]: sign, biased exponent (1023), 52-bit fraction")
    ok = all(np.spacing(float(2 ** k) * 1.3) == 2.0 ** (k - 52) for k in range(-20, 62))
    check("spacing_staircase", ok and close(np.spacing(100.0), 1.42e-14, rel=0.01) and close(np.spacing(1e6), 1.16e-10, rel=0.01),
          "l1 screens[5].prose: between 2^k and 2^(k+1) the gap is 2^(k-52)")
    check("integers_to_2_53", all(float(n) + 1 == n + 1 for n in (2 ** 52, 2 ** 52 + 12345, 2 ** 53 - 2))
          and float(2 ** 53) + 1 == float(2 ** 53) and np.spacing(float(2 ** 53)) == 2.0,
          "l1 screens[5]: whole numbers go missing above 2^53; float(2**53) + 1 == float(2**53)")
    fi = np.finfo(float)
    check("smallest_double", fi.tiny == 2.0 ** -1022 and 5e-324 == 2.0 ** -1074 and 2.0 ** -1074 / 2 == 0.0
          and close(fi.eps / fi.tiny, 1e292, rel=0.01) and close(fi.max, 1.797693e308, rel=1e-6),
          "l1 screens[6]: eps is not the smallest double; tiny = 2^-1022 is the smallest normal; subnormals reach 2^-1074")
    raised = False
    try:
        math.exp(710)
    except OverflowError:
        raised = True
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        v = np.exp(710.0)
    check("overflow_behaviour", raised and np.isinf(v) and any(issubclass(x.category, RuntimeWarning) for x in w)
          and close(math.exp(709), 8.218407e307, rel=1e-6),
          "l1 screens[6], quiz[1]: math.exp(710) raises OverflowError; np.exp(710) returns inf with a RuntimeWarning")
    # rounding model: |fl(x) - x| / |x| <= u, checked exactly with Decimal on random decimal strings
    rng = np.random.default_rng(7)
    worst = 0.0
    for _ in range(4000):
        s = f"{rng.uniform(1, 10):.17f}e{rng.integers(-300, 300)}"
        d = Decimal(s)
        worst = max(worst, float(abs(Decimal(float(s)) - d) / d))
    check("rounding_model_u", worst <= U and worst > 0.9 * U / 2,
          "l1 screens[7], summary.formula: fl(x) = x(1 + d), |d| <= u = 2^-53, for x between tiny and max")
    sub = Decimal("1.3e-320")
    rel_sub = float(abs(Decimal(float("1.3e-320")) - sub) / sub)
    note("rounding_model_range", f"below tiny the bound fails: 1.3e-320 is stored with relative error {rel_sub:.1e} > u "
         "(finding 1: summary.ideas[2] says 'every stored result' without the range)")
    err01 = float(Decimal(0.1) - Decimal("0.1"))
    check("tenth_error", close(err01, 5.55e-18, rel=0.001) and close(err01 / 0.1, 5.55e-17, rel=0.001) and err01 / 0.1 < U,
          "l1 quiz[3]: stored 0.1 is too high by 5.55e-18, relative 5.55e-17, about half of u")
    check("gap_at_1p7e18", 2.0 ** 60 < 1.7e18 < 2.0 ** 61 and np.spacing(1.7e18) == 256.0,
          "l1 screens[9]: nanosecond stamps near 1.7e18 are 256 ns apart")
    f32 = np.float32
    check("float32_gaps", np.finfo(f32).eps == 2.0 ** -23 and np.spacing(f32(20000)) == 2.0 ** -9
          and float(f32(20000.01)) == 20000.009765625 and np.spacing(f32(1e6)) == 0.0625
          and f32(1e6) + f32(0.01) == f32(1e6) and np.spacing(f32(1e9)) == 64.0
          and f32(2 ** 24) + f32(1) == f32(2 ** 24) and f32(2 ** 24 - 1) + f32(1) == f32(2 ** 24),
          "l1 quiz[0]; l2 quiz[2] option float32; review-1 items[4]; homework-1 items[1]: float32 gaps 2^(k-23)")


# ---------------------------------------------------------------- l2
def bs_call(S, K=100.0, r=0.05, s=0.2, T=1.0):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d1 - s * math.sqrt(T))


def cancellation():
    b = 1e8
    tb, st = (b - math.sqrt(b * b - 4)) / 2, 2 / (b + math.sqrt(b * b - 4))
    check("textbook_root", close(tb, 7.450581e-9, rel=1e-6) and close(st, 1e-8, rel=1e-15) and close((st - tb) / st, 0.255, abs_=0.001)
          and close(np.spacing(1e8) / 2, 7.45e-9, rel=0.01),
          "l2 screens[0], [2]: the textbook small root has no correct digit; the conjugate form is right to full precision")
    logs = []
    for k in range(1, 9):
        b = 10.0 ** k
        tb, st = (b - math.sqrt(b * b - 4)) / 2, 2 / (b + math.sqrt(b * b - 4))
        logs.append(math.log10(max(abs(tb - st) / st, 1e-17)))
    slope = np.polyfit(range(1, 9), logs, 1)[0]
    check("root_error_grows_like_b_squared", 1.8 < slope < 2.2,
          f"l2 screens[1]: relative error of the textbook root grows like b^2 (fitted slope {slope:.2f} decades per decade)")
    mp.dps = 40
    exp_err = float(mpf(math.exp(1e-10)) - mexp(mpf(1e-10)))
    naive, good = math.exp(1e-10) - 1, math.expm1(1e-10)
    check("expm1", close((naive - good) / good, 8.27e-8, rel=0.01) and close(good, 1.00000000005e-10, rel=1e-13),
          "l2 screens[3]: exp(1e-10) - 1 has relative error 8.27e-8; expm1 keeps every digit")
    note("exp_rounding_error_size", f"the rounding error of math.exp(1e-10) is {exp_err:.2e}, not 'near 1e-16'; "
         f"that error over 1e-10 is the 8.27e-8 (finding 2: l2 screens[3].explain)")
    for off, want in ((1e9, 0.0), (1e8, 29.333333333333332)):
        xs = [off + 4, off + 7, off + 13, off + 16]
        one = (sum(x * x for x in xs) - sum(xs) ** 2 / 4) / 3
        check(f"one_pass_variance_{off:.0e}", one == want and np.var(xs, ddof=1) == 30.0 and np.spacing(1e18) == 128.0,
              "l2 screens[4]: one-pass variance gives 0.0 at offset 1e9 and 29.33 at 1e8; true 30; squares near 1e18 are 128 apart")
    l2 = load("l2-cancellation")
    ns = {}
    exec(l2["screens"][8]["widget"]["solution"], ns)
    check("welford_and_best_bump", ns["welford_var"]([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]) == 30.0
          and abs(ns["best_bump"](math.exp, 1.0) - math.e) < 1e-9 and close(ns["stable_small_root"](1e8, 1), 1e-8, rel=1e-12),
          "l2 screens[8]: Welford, the conjugate root and the central bump at eps^(1/3) all pass")
    errs = {e: abs((math.exp(1 + 10.0 ** -e) - math.e) / 10.0 ** -e - math.e) for e in range(1, 16)}
    best = min(errs, key=errs.get)
    hstar = 2 * math.sqrt(EPS)
    check("forward_bump_V", best == 8 and close(errs[8], 6.6e-9, rel=0.02) and close(errs[15], 0.39, rel=0.02)
          and close(hstar, 2.98e-8, rel=0.01) and all(errs[e] < errs[e - 1] for e in range(2, 8)) and errs[10] > errs[8],
          "l2 screens[5], [7]: forward-difference error falls like h then rises like eps/h; best measured h = 1e-8, model h* = 2 sqrt(eps)")
    d1 = 0.07 / 0.2
    delta, gamma = norm.cdf(d1), norm.pdf(d1) / 20
    V = bs_call
    de = {h: abs((V(100 + h) - V(100)) / h - delta) for h in (1.0, 0.01, 1e-12)}
    check("delta_bumps", de[0.01] < de[1e-12] < de[1.0] and close(de[1.0], 9.3e-3, rel=0.02) and close(de[0.01], 9.4e-5, rel=0.02)
          and 1e-3 < de[1e-12] < 2e-2 and close(2 * math.sqrt(EPS * V(100) / gamma), 7e-7, rel=0.02),
          "l2 screens[6]: the 1p bump beats both the pound bump and the 1e-12 bump for a forward delta")
    ge = {h: (V(100 + h) - 2 * V(100) + V(100 - h)) / h ** 2 - gamma for h in (1.0, 0.01, 1e-4, 1e-6)}
    check("gamma_bumps", abs(ge[0.01]) < 1e-8 and abs(ge[0.01]) < abs(ge[1e-4]) < abs(ge[1.0]) < abs(ge[1e-6]) and abs(ge[1e-6]) > 1e-3,
          "l2 screens[9]: second difference is best at 0.01 and wrong in the first digit at 1e-6")
    hs = (48 * 2.22e-16) ** 0.25
    ce = abs((math.exp(1 + 1e-5) - math.exp(1 - 1e-5)) / 2e-5 - math.e)
    check("central_and_second_difference_h", close(EPS ** (1 / 3), 6.06e-6, rel=0.01) and close(ce, 5.9e-11, rel=0.2) and close(hs, 3.21e-4, rel=0.005),
          "l2 quiz[3], screens[7]; homework-1 items[6]: central best h near eps^(1/3); second difference h* = (48 eps)^(1/4)")
    check("log1p", close(math.log(1 + 1e-12), 1.000089e-12, rel=1e-6) and close(math.log1p(1e-12), 9.999999999995e-13, rel=1e-13),
          "l2 quiz[0]: log(1 + 1e-12) is wrong in the fifth digit; log1p is right")
    rng = np.random.default_rng(3)
    ok = True
    for _ in range(20000):
        y = rng.uniform(0.1, 10)
        x = y * rng.uniform(0.5, 2.0)
        ok &= Fraction(x) - Fraction(y) == Fraction(x - y)
    check("sterbenz", ok, "l2 quiz[1]: for y/2 <= x <= 2y the computed x - y is exact (Sterbenz), 20,000 random pairs checked exactly")
    x = 1e12
    check("conjugate_sqrt", close(1 / (math.sqrt(x + 1) + math.sqrt(x)), 5e-7, rel=1e-9) and abs(math.sqrt(x + 1) - math.sqrt(x) - 5e-7) > 1e-12,
          "review-1 items[1]: 1/(sqrt(x+1)+sqrt(x)) avoids the cancellation")


# ---------------------------------------------------------------- l3
def conditioning():
    A = np.array([[1, 1], [1, 1.0001]])
    s = np.linalg.svd(A, compute_uv=False)
    kappa = s[0] / s[1]
    b, b2 = np.array([2, 2.0001]), np.array([2, 2.0002])
    x, x2 = np.linalg.solve(A, b), np.linalg.solve(A, b2)
    amp = (np.linalg.norm(x2 - x) / np.linalg.norm(x)) / (np.linalg.norm(b2 - b) / np.linalg.norm(b))
    check("two_lines", np.allclose(x, [1, 1], atol=1e-9) and np.allclose(x2, [0, 2], atol=1e-9) and close(amp, 28285, rel=0.001)
          and close(kappa, 40002.00007, rel=1e-6) and amp <= kappa and close(1 / np.linalg.det(A), 10000, rel=1e-6),
          "l3 screens[0], [1], [3]: amplification 28,285 for the tried change, below kappa = 40,002")
    rng = np.random.default_rng(5)
    worst = 0.0
    for _ in range(20000):
        db = rng.standard_normal(2) * 1e-7
        dx = np.linalg.solve(A, db)
        worst = max(worst, (np.linalg.norm(dx) / np.linalg.norm(x)) / (np.linalg.norm(db) / np.linalg.norm(b)))
    U_, S_, Vt = np.linalg.svd(A)
    reach = (np.linalg.norm(np.linalg.solve(A, U_[:, 1])) / np.linalg.norm(x)) / (1 / np.linalg.norm(b))
    check("kappa_is_the_worst_case_for_this_b", worst <= kappa * (1 + 1e-9) and close(reach, kappa, rel=1e-4),
          "l3 screens[1].explain, [3].explain, [6]: the bound is never exceeded, and a change along the smallest singular direction reaches 40,002 for this b")
    b_bad = U_[:, 1] * 2.8
    xb = np.linalg.solve(A, b_bad)
    reach_bad = max((np.linalg.norm(np.linalg.solve(A, d)) / np.linalg.norm(xb)) / (np.linalg.norm(d) / np.linalg.norm(b_bad)) for d in (U_[:, 0], U_[:, 1]))
    note("bound_reached_needs_worst_b_too", f"for b along the smallest singular direction the largest amplification over all changes is {reach_bad:.3f}, "
         f"not {kappa:.0f} (finding 5: l3 screens[6].explain says the bound is reached for the worst change, for any b)")
    for f, df, x0, want in ((math.sqrt, lambda t: 0.5 / math.sqrt(t), 7.3, 0.5), (math.exp, math.exp, 20.0, 20.0),
                            (lambda t: t - 1, lambda t: 1.0, 1.0001, 10001.0), (math.log, lambda t: 1 / t, 1.0001, 10000.5),
                            (lambda t: t * t, lambda t: 2 * t, 3.3, 2.0), (lambda t: t - 100, lambda t: 1.0, 100.01, 10001.0)):
        k = abs(x0 * df(x0) / f(x0))
        d = 1e-9
        measured = abs((f(x0 * (1 + d)) - f(x0)) / f(x0)) / d
        check(f"function_kappa_{want:g}", close(k, want, rel=1e-3) and close(measured, k, rel=5e-3),
              "l3 screens[2], quiz[2]; review-1 items[9]: kappa = |x f'/f| matches the measured relative amplification")
    H = np.array([[1 / (j + k + 1) for k in range(8)] for j in range(8)])
    kH = np.linalg.cond(H)
    rng = np.random.default_rng(11)
    xh = np.ones(8)
    bh = H @ xh
    errs = []
    for _ in range(200):
        bp = bh * (1 + 1e-12 * rng.uniform(-1, 1, 8))
        errs.append(np.linalg.norm(np.linalg.solve(H, bp) - np.linalg.solve(H, bh)) / np.linalg.norm(xh))
    lost = math.log10(max(errs) / 1e-12)
    check("digits_lost_rule_of_thumb", close(kH, 1.53e10, rel=0.01) and close(math.log10(40002), 4.6, abs_=0.01) and 6 < lost <= math.log10(kH) + 0.5,
          f"l3 screens[4], [7]: digits lost is about log10(kappa), an upper estimate (Hilbert 8: bound 10.2, measured worst of 200 random changes {lost:.1f})")
    r = b - A @ np.array([0.0, 2.0])
    check("small_residual_wrong_answer", np.allclose(r, [0, -1e-4], atol=1e-12) and np.linalg.norm(r) / np.linalg.norm(b) < 1e-4
          and np.linalg.norm(np.array([0.0, 2.0]) - x) / np.linalg.norm(x) > 0.99,
          "l3 screens[5], summary.trap; review-1 items[6]: a tiny residual with relative error 1; error <= kappa x relative residual")
    check("singular_matrix", np.linalg.svd(np.array([[1.0, 2.0], [1.0, 2.0]]), compute_uv=False)[1] < 1e-15 and close((1.95) / (0.05), 39, rel=1e-12)
          and close(1 / (1 - 0.95 ** 2), 10.26, rel=1e-3) and close(np.linalg.cond(np.array([[1, 0.95], [0.95, 1]])), 39, rel=1e-9),
          "l3 quiz[0], quiz[1]: kappa of the 2x2 correlation matrix is (1+r)/(1-r); a singular matrix has kappa = infinity")
    X = np.random.default_rng(2).multivariate_normal([0, 0], [[1, 0.95], [0.95, 1]], 200000)
    X = (X - X.mean(0)) / X.std(0)
    note("corr_kappa_is_the_normal_equations_figure", f"kappa of the standardised design is {np.linalg.cond(X):.2f} = sqrt(39) = {math.sqrt(39):.2f}; "
         "39 is kappa of X^T X, so 1.6 digits is what the normal equations lose and a QR fit loses about 0.8 (finding 4: l3 quiz[0].explain, screens[4].explain)")

    def put(K, s):
        d1 = (math.log(100 / K) + (0.05 + s * s / 2)) / s
        return K * math.exp(-0.05) * norm.cdf(-(d1 - s)) - 100 * norm.cdf(-d1), 100 * norm.pdf(d1)
    p60, v60 = put(60, 0.2)
    vatm = 100 * norm.pdf(0.35)
    check("implied_vol_sensitivity", close(p60, 0.0113, abs_=5e-5) and close(v60, 0.588, abs_=5e-4) and close(vatm, 37.52, abs_=0.005)
          and close(0.01 / v60 * 100, 1.70, abs_=0.01) and close(0.05 / vatm * 100, 0.133, abs_=0.001) and close(0.05 / v60 * 100, 8.5, abs_=0.01)
          and p60 / (v60 * 0.2) < 1,
          "l3 screens[9], quiz[3]: vol moves by dV/vega; the wing is ill-conditioned in absolute terms only (relative kappa V/(vega sigma) is below 1)")


# ---------------------------------------------------------------- l4
def exact_ls(A, b):
    mp.dps = 60
    Am, bm = matrix(A.tolist()), matrix(b.tolist())
    return np.array([float(v) for v in lu_solve(Am.T * Am, Am.T * bm)])


def stability():
    s, t, terms = 0.0, 1.0, []
    for k in range(1, 120):
        s += t
        terms.append(t)
        t *= -20 / k
    p, t = 0.0, 1.0
    for k in range(1, 120):
        p += t
        t *= 20 / k
    true = math.exp(-20)
    big = 20.0 ** 20 / math.factorial(20)
    check("series_exp_minus_20", s == 6.147561828914626e-09 and close((s - true) / true, 1.983, abs_=0.001) and close(1 / p, true, rel=4 * EPS)
          and close(math.log10(big) - math.log10(true), 16.3, abs_=0.05) and abs(sum(reversed(terms)) - true) / true > 1,
          "l4 screens[0..2]: the alternating series is 198% too big, in either order; 1/sum of the positive series is right to the last digit")
    check("series_not_backward_stable", abs(math.log(s) - (-20)) > 1.0 and abs(20 * EPS) < 1e-14,
          "l4 screens[2]: e^x = 6.1e-9 needs x = -18.9, not a rounding-sized change of -20; kappa = 20 only")
    check("series_exp_minus_30", close(30.0 ** 30 / math.factorial(30), 7.8e11, rel=0.01) and close(math.exp(-30), 9.4e-14, rel=0.01),
          "review-1 items[8]: largest term 7.8e11 against the answer 9.4e-14")
    for e, fails in ((1e-8, True), (1e-7, False)):
        A = np.array([[1, 1], [e, 0], [0, e]])
        b = np.array([2, e, e])
        N_ = A.T @ A
        Q, R = np.linalg.qr(A)
        xq = np.linalg.solve(R, Q.T @ b)
        xl = np.linalg.lstsq(A, b, rcond=None)[0]
        try:
            xn = np.linalg.solve(N_, A.T @ b)
            bad = not np.allclose(xn, [1, 1])
        except np.linalg.LinAlgError:
            bad = True
        check(f"lauchli_{e:.0e}", np.allclose(xq, [1, 1], atol=1e-9) and np.allclose(xl, [1, 1], atol=1e-9) and bad == fails
              and (np.linalg.det(N_) == 0) == fails and close(np.linalg.cond(A), math.sqrt(2) / e, rel=1e-6),
              "l4 screens[3], [4], [8], quiz[0]: normal equations are singular at 1e-8 and work at 1e-7; QR and lstsq return (1, 1) at both")
    check("stored_one_plus_e2", 1 + 1e-16 == 1.0 and 1 + 1e-14 > 1.0 and close(1e-14 / EPS, 45, abs_=0.1) and close(2e14 * U, 0.022, rel=0.02),
          "l4 screens[3], quiz[0]: 1 + 1e-16 rounds to 1; 1 + 1e-14 is about 45 gaps above 1; kappa^2 u = 0.02")
    rng = np.random.default_rng(1)
    ok = True
    for _ in range(50):
        M = rng.standard_normal((30, 6)) @ np.diag(np.logspace(0, -5, 6))
        ok &= close(np.linalg.cond(M.T @ M), np.linalg.cond(M) ** 2, rel=1e-3)
        ok &= close(np.linalg.cond(np.linalg.qr(M)[1]), np.linalg.cond(M), rel=1e-8)
    check("kappa_squared_and_R", ok, "l4 screens[5]: kappa(A^T A) = kappa(A)^2 and kappa(R) = kappa(A), 50 random full-rank matrices")
    t = np.linspace(0, 1, 100)
    A = np.vander(t, 15, increasing=True)
    b = np.exp(np.sin(4 * t)) / 2006.787453080206
    xl = np.linalg.lstsq(A, b, rcond=None)[0][-1]
    Q, R = np.linalg.qr(A)
    xq = np.linalg.solve(R, Q.T @ b)[-1]
    xn = np.linalg.solve(A.T @ A, A.T @ b)[-1]
    kA = np.linalg.cond(A)
    check("trefethen_bau_lecture_19", close(kA, 2.27e10, rel=0.01) and abs(xl - 1) < 1e-6 and abs(xq - 1) < 1e-6 and abs(xn - 1) > 0.5
          and abs(xl - 1) < kA * U,
          f"l4 screens[6], [7]: QR and lstsq keep about 7 digits (inside kappa u); the normal equations keep none (here {xn:.2f}; the value differs by platform)")
    tt = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30.0])
    Ay = np.vander(tt, 4, increasing=True)
    Ac = np.vander((tt - tt.mean()) / tt.std(), 4, increasing=True)
    check("yield_curve_design", close(np.linalg.cond(Ay), 2.98e4, rel=0.005) and close(np.linalg.cond(Ay.T @ Ay), 8.88e8, rel=0.005)
          and close(np.linalg.cond(Ac), 13.3, rel=0.005),
          "l4 screens[9]: kappa 2.98e4 in raw years, 8.88e8 for A^T A, 13.3 after centring and scaling")
    # least squares with a small and with a large residual
    out = {}
    for label, rs in (("small", 0.0), ("large", 1.0)):
        eq, en = [], []
        for _ in range(12):
            Uq, _ = np.linalg.qr(rng.standard_normal((50, 50)))
            Vq, _ = np.linalg.qr(rng.standard_normal((5, 5)))
            A = Uq[:, :5] @ np.diag(np.logspace(0, -6, 5)) @ Vq.T
            x = rng.standard_normal(5)
            r = Uq[:, 5:] @ rng.standard_normal(45)
            b = A @ x + rs * r / np.linalg.norm(r) * np.linalg.norm(A @ x)
            xe = exact_ls(A, b)
            Q, R = np.linalg.qr(A)
            eq.append(np.linalg.norm(np.linalg.solve(R, Q.T @ b) - xe) / np.linalg.norm(xe))
            en.append(np.linalg.norm(np.linalg.solve(A.T @ A, A.T @ b) - xe) / np.linalg.norm(xe))
        out[label] = (float(np.median(eq)), float(np.median(en)))
    ku = 1e6 * U
    check("qr_meets_kappa_u_when_the_fit_is_good", out["small"][0] < 100 * ku and out["small"][1] > 1e4 * out["small"][0],
          f"l4 screens[4], summary.ideas[1], [2], quiz[1], quiz[3]: with a near-exact fit QR errs by about kappa u ({out['small'][0]:.1e} against {ku:.1e}); the normal equations by about kappa^2 u ({out['small'][1]:.1e})")
    note("qr_loses_more_when_the_residual_is_large", f"kappa = 1e6: with a zero residual QR errs by {out['small'][0]:.1e} and the normal equations by {out['small'][1]:.1e}; "
         f"with a residual as large as the fit QR errs by {out['large'][0]:.1e}, about {out['large'][0] / ku:.0f} times kappa u, "
         f"and the normal equations by {out['large'][1]:.1e} (finding 7: 'QR loses log10 kappa digits' needs a small residual; Trefethen and Bau Theorem 18.1)")
    # variance: conditioning against stability (homework-1 items[8])
    x = np.round(1e9 + rng.normal(0, 3, 250), 2)
    s2 = np.var(x, ddof=1)
    d = 1e-10
    amp = abs(np.var(x * (1 + d * np.sign(x - x.mean())), ddof=1) - s2) / s2 / d
    kap = 2 * x.mean() / math.sqrt(s2)
    # Corrected assert (Chan, Golub and LeVeque 1983; Higham sec. 1.9): the relative condition number of the
    # sample variance is about 2 * mean / s, here about 6e8:
    #     0.5 * kap < amp < 1.5 * kap and amp > 1e8
    check("variance_is_well_conditioned", amp < 100,
          f"homework-1 items[8].model, rubric[2] (finding 6): 'variance as a function of the marks is well conditioned'; "
          f"measured relative amplification {amp:.2e}, 2 mean / s = {kap:.2e}", expected_fail=True)
    one, two = [], []
    for _ in range(200):
        y = 1e9 + rng.normal(0, 3, 250)
        one.append(np.mean(y * y) - np.mean(y) ** 2)
        two.append(np.var(y))
    one = np.array(one)
    check("one_pass_variance_simulation", np.mean(one == 0) > 0.1 and one.min() < -100 and one.max() > 100 and abs(np.mean(two) - 9) < 0.5
          and close(U * (1e9 / 3) ** 2, 10, rel=0.3),
          "homework-1 items[8].model; l2 quiz[2]; review-1 items[7]: one-pass variance is often exactly 0, otherwise a few hundred either way, and can be negative; two passes give about 9; u (mean/s)^2 is about 10")
    ns = {}
    exec(load("homework-1")["items"][7]["widget"]["solution"], ns)
    pennies = [np.float32(0.01)] * 10 ** 5
    plain = np.float32(0)
    for v in pennies:
        plain = plain + v
    kt = ns["kahan_total"](pennies)
    check("kahan_float32", isinstance(kt, np.float32) and abs(float(kt) - 1000.0) < 0.005 and abs(float(plain) - 1000.0) > 0.5
          and close(ns["kahan_total"]([1.0] + [1e-16] * 10 ** 5), 1.00000000001, rel=1e-13),
          "homework-1 items[7]: Kahan keeps float32 pennies exact where the plain float32 loop drifts (NumPy 2 scalar rules keep float32)")
    x0 = 1e-3
    kap_f = x0 * math.exp(x0) / math.expm1(x0)
    check("expm1_well_conditioned", close(kap_f, 1.0, abs_=1e-3) and close(3e5 ** 2, 9e10) and close(16 - math.log10(9e10), 5.05, abs_=0.01),
          "homework-1 items[2], items[4]: e^x - 1 has kappa -> 1 near 0; kappa = 3e5 squared costs about 11 digits")


if __name__ == "__main__":
    floating_point()
    cancellation()
    conditioning()
    stability()
    tail = f"{N} checks passed, {len(EXPECTED)} EXPECTED_FAIL ({', '.join(EXPECTED) or 'none'})"
    if FAILED:
        print(f"L1 concepts: {tail}, {len(FAILED)} failing: {', '.join(FAILED)}")
        sys.exit(1)
    print(f"L1 concepts: {tail}")
