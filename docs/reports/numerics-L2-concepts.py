#!/usr/bin/env python3
"""Concept checks for numerics level 2 (l5 to l8, review-2, homework-2).

Run from anywhere: python3 docs/reports/numerics-L2-concepts.py
Each check names its ledger rows (docs/reports/audit-numerics-1-3-ledger.md).
Exit 0 means every checked claim holds. A check marked EXPECTED_FAIL fails
because the content is wrong as stated (a `wrong` finding of
docs/reviews/audit-numerics-1-3.md); it is reported, does not change the exit
code, and carries the corrected assert in a comment. A line starting "note"
records where a claim stops holding outside the case the lesson uses (the
`imprecise` findings); notes are measured and printed, not asserted against
the content.

Needs numpy and scipy. About 5 s.
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from scipy.stats import norm

COURSE = Path(__file__).resolve().parents[2] / "app/content/courses/numerics"
N = 0
FAILED = []
EXPECTED = []


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


def counted(f):
    c = [0]

    def g(x):
        c[0] += 1
        return f(x)
    return g, c


def order(e0, e1, e2):
    return math.log(e2 / e1) / math.log(e1 / e0)


# ---------------------------------------------------------------- l5
def root_finding_orders():
    r2 = math.sqrt(2)
    x, ne = 1.0, []
    for _ in range(4):
        x -= (x * x - 2) / (2 * x)
        ne.append(abs(x - r2))
    a, b, se = 1.0, 2.0, []
    for _ in range(6):
        a, b = b, b - (b * b - 2) * (b - a) / (b * b - a * a)
        se.append(abs(b - r2))
    check("newton_quadratic_simple_root", close(order(*ne[0:3]), 1.98, abs_=0.01) and close(order(*ne[1:4]), 2.00, abs_=0.01)
          and close(ne[3] / ne[2] ** 2, 1 / (2 * r2), rel=1e-3) and close(ne[3], 1.59e-12, rel=0.01),
          "l5 screens[0], [2], [4], [5]: Newton on x^2 - 2 has order 2 and constant f''/(2f') = 0.353553")
    check("secant_golden_ratio", close(order(*se[1:4]), 1.50, abs_=0.01) and close(order(*se[2:5]), 1.67, abs_=0.01)
          and close(se[4], 3.16e-10, rel=0.01) and se[5] < 1e-12 and close((1 + 5 ** 0.5) / 2, 1.618, abs_=1e-3),
          "l5 screens[0], [3]: secant estimates 1.50 then 1.67, around 1.618; it passes 1e-12 at step 6")
    # secant order on other functions, extended precision so the asymptotic range is visible
    from mpmath import mp, mpf, cos, exp, log
    mp.dps = 400
    est = []
    for f, x0, x1 in ((lambda t: t ** 3 - 2 * t - 5, mpf(2), mpf(3)), (lambda t: cos(t) - t, mpf(0), mpf(1)), (lambda t: exp(t) - 3, mpf(1), mpf(2))):
        xs = [x0, x1]
        for _ in range(11):
            xs.append(xs[-1] - f(xs[-1]) * (xs[-1] - xs[-2]) / (f(xs[-1]) - f(xs[-2])))
        root = xs[-1]
        e = [abs(v - root) for v in xs[6:11]]
        est.append(float(log(e[3] / e[2]) / log(e[2] / e[1])))
    check("secant_order_other_functions", all(abs(p - 1.618) < 0.05 for p in est),
          f"l5 screens[3], summary: secant order is the golden ratio for simple roots ({', '.join(f'{p:.3f}' for p in est)})")
    check("efficiency_index", close(2 ** 0.5, 1.414, abs_=1e-3) and close(2 ** (1 / 1.5), 1.587, abs_=1e-3)
          and close(1 / math.log2((1 + 5 ** 0.5) / 2) - 1, 0.44, abs_=0.005),
          "l5 screens[7]; review-2 items[2]; homework-2 items[2]: per evaluation Newton gains 2^(1/(1+c)); it beats 1.618 only for c below 0.44")
    check("halvings", all(min(k for k in range(80) if w / 2 ** k < tol) == want for w, tol, want in
                          ((1, 1e-12, 40), (0.2, 1e-10, 31), (1, 1e-6, 20), (5, 1e-10, 36), (1, 1e-9, 30), (5, 1e-8, 29))) and close(5 / 2 ** 10, 0.00488, abs_=1e-5),
          "l5 screens[0], [6], quiz[1]; l6 screens[4], quiz[2]; review-2 items[0]; homework-2 items[0]: halving counts")
    mids, lo, hi = [], 1.0, 2.0
    for _ in range(4):
        m = (lo + hi) / 2
        mids.append(abs(m - r2))
        lo, hi = (m, hi) if m * m < 2 else (lo, m)
    check("midpoint_error_not_monotone", mids[1] > mids[0] and all(e <= 0.5 ** (k + 1) for k, e in enumerate(mids)),
          "l5 quiz[0]: the midpoint error can grow (0.0858 then 0.164) while half the width always bounds it")
    P = lambda y: sum(5 / (1 + y) ** t for t in range(1, 6)) + 100 / (1 + y) ** 5 - 95
    dP = lambda y: sum(-5 * t / (1 + y) ** (t + 1) for t in range(1, 6)) - 500 / (1 + y) ** 6
    y, ys = 0.05, []
    for _ in range(6):
        y -= P(y) / dP(y)
        ys.append(y)
    check("bond_yield_newton", close(ys[-1], 0.06193228, abs_=1e-8) and close(ys[0], 0.0615487, abs_=1e-7) and close(ys[1], 0.06193188, abs_=1e-8)
          and abs(ys[2] - ys[-1]) / ys[-1] < 1e-10,
          "l5 screens[6]: Newton from 5% reaches the yield 6.193228% to about 11 digits in 3 steps")
    ns = {}
    exec(load("l5-bisection-and-newton")["screens"][8]["widget"]["solution"], ns)
    f = lambda t: t * t - 2
    check("call_counts", ns["bisect"](f, 1, 2, 1e-12)[1] == 42 and ns["secant"](f, 1.0, 2.0, 1e-12)[1] == 9 and ns["newton"](f, lambda t: 2 * t, 1.0, 1e-12)[1] == 6,
          "l5 screens[8]: 42 calls for bisection, 9 for secant, 6 f and 6 f' for Newton")
    crashed = False
    try:
        ns["newton"](f, lambda t: 2 * t, 0.0, 1e-12)
    except ZeroDivisionError:
        crashed = True
    check("newton_from_zero_slope", crashed, "l5 quiz[2]: Newton on x^2 - 2 from 0 divides by zero")
    # multiple root: Newton is linear with ratio 1 - 1/m
    x, e = 2.0, []
    for _ in range(12):
        x -= (x - 1) ** 2 * (x + 1) / (2 * (x - 1) * (x + 1) + (x - 1) ** 2)
        e.append(abs(x - 1))
    note("newton_linear_at_a_double_root", f"on (x - 1)^2 (x + 1) Newton's error ratio settles at {e[9] / e[8]:.3f} (order 1, ratio 1/2), "
         f"measured order {order(*e[6:9]):.2f}: order 2 needs a simple root (finding 10: l5 screens[2], [5], summary)")
    root, calls = ns["bisect"](lambda t: 1 / t, -1.0, 2.0, 1e-12)
    note("sign_change_without_continuity", f"bisect on 1/x over [-1, 2] returns {root:.1e} after {calls} calls with no error, and tan on [1, 2] returns "
         f"{ns['bisect'](math.tan, 1.0, 2.0, 1e-12)[0]:.6f} (pi/2): a sign change gives a root only for continuous f "
         "(finding 11: l5 quiz[3], summary; l6 screens[3] line t1)")
    note("twelve_digits", f"Newton's step-4 error is {ne[3]:.2e}, above the 1e-12 that bisection's 40 halvings are held to "
         "(finding 13: l5 screens[0]); step 5 is exact, so the key stands")


# ---------------------------------------------------------------- l6
def bs(S, K, r, T, s, kind):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    c = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d1 - s * math.sqrt(T))
    return c if kind == "c" else c - S + K * math.exp(-r * T)


def vega(S, K, r, T, s):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return S * math.sqrt(T) * norm.pdf(d1)


def safe_solver():
    T = 1 / 12
    step = lambda K, kind, q, s: s - (bs(100, K, 0.05, T, s, kind) - q) / vega(100, K, 0.05, T, s)
    s80 = step(80, "p", 0.0794, 0.2)
    check("plain_newton_fails_on_wings", close(step(75, "p", 0.0766, 0.2), 2724, rel=0.001) and close(s80, 18.14, abs_=0.01)
          and close(step(80, "p", 0.0794, s80), -218, rel=0.01) and close(step(85, "p", 0.1154, 0.2), 0.885, abs_=0.005)
          and close(step(75, "p", 0.0766, 0.3), 2.53, abs_=0.01) and close(step(75, "p", 0.0766, 0.5), 0.482, abs_=0.001),
          "l6 screens[0], [1]: the 75 and 80 puts jump to 2,724 and 18.14 then -218; from 0.3 the 75 put lands at 2.53, from 0.5 at 0.482")
    check("bounds", close(100 - 95 * math.exp(-0.05 / 12), 5.3950, abs_=5e-5) and close(110 * math.exp(-0.05 / 12) - 100, 9.5426, abs_=5e-5)
          and all(bs(100, 95, 0.05, T, s, "c") >= 5.3950 for s in np.linspace(1e-4, 5, 400))
          and all(bs(100, 110, 0.05, T, s, "p") >= 9.5426 for s in np.linspace(1e-4, 5, 400))
          and all(np.diff([bs(100, 95, 0.05, T, s, "c") for s in np.linspace(1e-3, 5, 400)]) >= 0),
          "l6 screens[6], quiz[3]: no vol prices the 95 call below 5.3950 or the 110 put below 9.5426; price rises with vol")
    check("rounded_quote", close(vega(100, 125, 0.05, T, 0.2124), 0.0218, abs_=5e-5) and close(0.00005 / 0.0218, 0.0023, abs_=5e-5)
          and close(0.0001 / 0.5, 0.0002) and close(0.0001 / 0.0218 * 100, 0.46, abs_=0.005) and close(0.0005 / 0.02 * 100, 2.5),
          "l6 screens[5], quiz[1]; review-2 items[4]; homework-2 items[4]: a price error moves vol by dV/vega")
    l6 = load("l6-safe-root-finder")
    ns = {}
    exec(l6["screens"][7]["widget"]["solution"], ns)
    sn = ns["safe_newton"]
    x, seen = 0.0, []
    for _ in range(6):
        x -= (x ** 3 - 2 * x + 2) / (3 * x * x - 2)
        seen.append(x)
    check("safe_newton_lesson_cases", seen == [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
          and close(sn(lambda t: t ** 3 - 2 * t + 2, lambda t: 3 * t * t - 2, -3.0, 0.0), -1.769292354238631, abs_=1e-9)
          and close(sn(lambda t: t ** 3 - 1, lambda t: 3 * t * t, -2.0, 2.0), 1.0, abs_=1e-9),
          "l6 screens[7]: plain Newton cycles 0, 1 on x^3 - 2x + 2; the bracketed solver reaches -1.769292; a zero slope at the start costs a bisection")
    ns8 = {}
    exec(l6["screens"][8]["widget"]["prelude"], ns8)
    exec(l6["screens"][8]["widget"]["solution"], ns8)
    iv = ns8["implied_vols"]
    K11 = list(range(75, 130, 5))
    kinds = ["p"] * 5 + ["c"] * 6
    P11 = [0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003]
    got = iv(P11, K11, 100.0, 0.05, T, kinds)
    ref = [brentq(lambda s: bs(100, K, 0.05, T, s, k) - q, 1e-4, 5, xtol=1e-14) for K, k, q in zip(K11, kinds, P11)]
    check("implied_vols_match_brentq", np.allclose(got, ref, atol=1e-9) and np.isnan(iv([5.0], [95], 100.0, 0.05, T, ["c"])[0]),
          "l6 screens[8]: the vectorised solver agrees with scipy.optimize.brentq and returns NaN below the bound")
    K1k = np.linspace(80, 120, 1000)
    k1k = np.where(K1k < 100, "p", "c")
    P1k = ns8["bs_price"](100.0, K1k, 0.05, T, 0.2 + 0.001 * (K1k - 100) ** 2 / 10, k1k)

    def tm(fn, rep=15):
        t0 = time.perf_counter()
        for _ in range(rep):
            fn()
        return (time.perf_counter() - t0) / rep
    ratio = tm(lambda: iv(P1k, K1k, 100.0, 0.05, T, k1k)) / tm(lambda: iv(P1k[:1], K1k[:1], 100.0, 0.05, T, k1k[:1]))
    note("thousand_strikes_cost", f"1,000 strikes take {ratio:.0f} times as long as one strike here: far below 1,000 times, but not 'about as much as one' "
         "(finding 14: l6 screens[8].explain; homework-2 items[6].explain)")
    # Before the fix pass the taught solver had no test of slow progress: on 1e40 (x - 1)^p over [0, 3] it reached
    # maxit after 102 calls for p = 9 and 21 and returned x silently, 3.8e-3 from the root for p = 21.
    # (corrected claim, fix pass) The solution now has rtsafe's second test (bisect when the Newton step is over
    # half the step before last) and raises RuntimeError at maxit instead of returning a guess. The content no
    # longer claims an all-bisection worst case; it says Newton steps cannot creep and maxit is the last stop.
    # Every return must be by ftol (|f| below 1e-12, the residual test) or by a step below xtol, never at the cap.
    # Second method: with ftol = 0 only the step test can stop it, and each multiple root must be reached.
    ends_ok = True
    for p in (3, 9, 21):
        f = lambda t, p=p: 1e40 * (t - 1) ** p
        g, c = counted(f)
        root = sn(g, lambda t, p=p: 1e40 * p * (t - 1) ** (p - 1), 0.0, 3.0)
        ends_ok &= c[0] < 102 and (abs(f(root)) < 1e-12 or abs(root - 1) < 1e-9)
    creep = []
    for p in (3, 9, 21, 51):
        g, c = counted(lambda t, p=p: (t - 1) ** p)
        creep.append((abs(sn(g, lambda t, p=p: p * (t - 1) ** (p - 1), 0.0, 3.0, ftol=0.0) - 1), c[0]))
    raised = False
    try:
        sn(lambda t: (t - 1) ** 9, lambda t: 9 * (t - 1) ** 8, 0.0, 3.0, ftol=0.0, maxit=10)
    except RuntimeError:
        raised = True
    s4 = l6["screens"][4]
    check("safeguard_worst_case_is_all_bisection", ends_ok and raised and all(e < 1e-6 and n < 102 for e, n in creep)
          and all(e < 1e-9 for e, _ in creep[:3]) and "worst case is all bisection" not in s4["prose"]
          and "guaranteed cap" not in s4["feedback"]["correct"] and "maxit" in l6["screens"][3]["explain"]["text"],
          f"l6 screens[3], [4], [7] (finding 12, corrected claim, fix pass): on (x - 1)^p, p = 3, 9, 21, 51 with ftol = 0 the solver ends "
          f"with errors {', '.join(f'{e:.1e}' for e, _ in creep)} in {', '.join(str(n) for _, n in creep)} calls; with maxit = 10 it raises")


# ---------------------------------------------------------------- l7
def interpolation():
    ns = {}
    exec(load("l7-interpolation")["screens"][7]["widget"]["solution"], ns)
    le, mie = ns["lagrange_eval"], ns["max_interp_error"]
    rf = lambda x: 1 / (1 + 25 * x ** 2)
    g = np.linspace(-1, 1, 20001)
    eq = lambda n: np.linspace(-1, 1, n + 1)
    ch = lambda n: np.cos(np.arange(n + 1) * np.pi / n)
    check("runge_equal_spacing", close(mie(rf, eq(10), g), 1.9157, abs_=1e-4) and close(mie(rf, eq(20), g), 59.82, abs_=0.01)
          and close(float(le(eq(10), rf(eq(10)), 0.95)[0]), 1.9236, abs_=1e-4) and close(mie(rf, eq(8), g), 1.0452, abs_=1e-4),
          "l7 screens[0], [1], [5]; review-2 items[5]: Runge's function on equal nodes errs by 1.92 at n = 10 and 59.82 at n = 20")
    che = [mie(rf, ch(n), g) for n in (4, 8, 10, 20)]
    check("runge_chebyshev_nodes", np.allclose(che, [0.4600, 0.2047, 0.1322, 0.0177], atol=1e-4),
          "l7 screens[2]: on Chebyshev nodes the error falls 0.4600, 0.2047, 0.1322, 0.0177")
    rng = np.random.default_rng(4)
    xs = np.sort(rng.uniform(-1, 1, 6))
    ys = rng.standard_normal(6)
    co = np.polyfit(xs, ys, 5)
    check("unique_interpolant", np.allclose(le(xs, ys, g[::500]), np.polyval(co, g[::500]), atol=1e-8)
          and mie(lambda x: x ** 3, np.array([0.0, 0.3, 1.1, 2.0]), np.linspace(-1, 3, 101)) < 1e-12,
          "l7 screens[1], [6], quiz[0]: one polynomial of degree <= n through n + 1 points, whatever the method; a cubic is reproduced by 4 points")
    prod = lambda nodes: np.abs(np.prod(g[:, None] - nodes[None, :], axis=1))
    pe10, pc10 = prod(eq(10)), prod(ch(10))
    check("node_product_shape", close(abs(np.prod(0.95 - eq(10))), 0.00845, rel=0.001) and close(abs(np.prod(0.05 - eq(10))), 0.0000671, rel=0.001)
          and all(prod(ch(n)).max() <= 2.0 ** (1 - n) * (1 + 1e-9) for n in (4, 8, 10, 12, 20)),
          "l7 screens[3], quiz[1]: equal-node product is 126 times larger near the end than the middle; Chebyshev product never exceeds 2^(1-n)")
    pe = {n: prod(eq(n)).max() for n in (4, 8, 10, 20)}
    # (corrected claim, fix pass) The content now says the derivative factor grows faster than the node product
    # shrinks, and equal spacing leaves that product largest at the ends. Product maxima shrink with n; the Runge
    # derivative factor |f^(n+1)| / (n+1)! grows like 5^(n+1) (Cauchy estimate: the poles at +-0.2i set a radius
    # of 1/5), so factor times product grows; and the end-to-middle ratio stays large.
    deriv = {n: 5.0 ** (n + 1) for n in (10, 20)}
    l7 = load("l7-interpolation")
    check("equal_node_product_explodes_with_n", pe[20] < pe[10] < pe[8] < pe[4] and deriv[20] * pe[20] > deriv[10] * pe[10]
          and pe[10] / prod(eq(10))[len(g) // 2 - 500:len(g) // 2 + 500].max() > 50
          and "explodes" not in l7["screens"][5]["explain"]["text"] and "grows faster than the node product shrinks" in l7["screens"][5]["explain"]["text"],
          f"l7 screens[5].explain (finding 15, corrected claim, fix pass): the node product's maximum falls, {pe[10]:.5f} at n = 10 and {pe[20]:.6f} at n = 20, "
          f"while 5^(n+1) times it rises from {deriv[10] * pe[10]:.2e} to {deriv[20] * pe[20]:.2e}")
    ee = {n: mie(np.exp, eq(n), g) for n in (4, 8, 10, 20)}
    er = {n: mie(lambda x: 1 / (1 + x * x), eq(n), g) for n in (4, 8, 10, 20)}
    # (corrected claim, fix pass) The content now limits the growth to some functions (Runge's): for e^x and for
    # 1/(1 + x^2) more equally spaced points fit closer, while Runge's function gets worse.
    r2 = load("review-2")["items"][5]
    texts = [l7["summary"]["ideas"][1], l7["summary"]["trap"], l7["screens"][5]["widget"]["options"][1]["why"], r2["feedback"]["generic"]]
    check("equal_spacing_error_grows_with_n", ee[20] < ee[10] < ee[4] and er[20] < er[10] < er[4] and mie(rf, eq(20), g) > mie(rf, eq(10), g)
          and not any(t.startswith("On equal spacing the error swings") or t.startswith("More equally spaced points do not") for t in texts)
          and all(("Runge" in t or "this $f$" in t or "some smooth" in t) for t in texts),
          f"l7 summary, screens[5] option why; review-2 items[5] (finding 15, corrected claim, fix pass): "
          f"e^x: {ee[10]:.1e} at n = 10, {ee[20]:.1e} at n = 20; 1/(1 + x^2): {er[10]:.1e}, {er[20]:.1e}; only Runge's function grows")

    def lebesgue(nodes, grid):
        return sum(np.abs(le(nodes, np.eye(len(nodes))[j], grid)) for j in range(len(nodes)))
    L_eq, L_ch = lebesgue(eq(10), g).max(), lebesgue(ch(10), g).max()
    worst = 0.0
    for _ in range(300):
        d = rng.uniform(-1, 1, 11)
        worst = max(worst, np.abs(le(eq(10), d, g)).max())
    strikes = np.linspace(75, 125, 11)
    gg = np.linspace(75, 125, 5001)
    sw = le(strikes, 0.001 * (-1.0) ** np.arange(11), gg)
    i = int(np.argmax(np.abs(sw)))
    check("lebesgue_constants", close(L_eq, 29.9, abs_=0.05) and close(L_ch, 2.42, abs_=0.005) and worst <= L_eq
          and close(abs(sw[i]), 0.0292, abs_=1e-4) and (abs(gg[i] - 76.6) < 0.1 or abs(gg[i] - 123.4) < 0.1) and abs(sw[i]) <= 0.001 * L_eq,
          "l7 screens[4], [8], quiz[2]; review-2 items[6]: Lebesgue constants 29.9 and 2.42; alternating 0.001 errors swing 0.0292 near 76.6 and 123.4")
    f = lambda x: np.exp(x) * np.sin(5 * x)
    big = ch(400)
    check("barycentric_stable_on_chebyshev", np.abs(le(big, f(big), g[::7]) - f(g[::7])).max() < 1e-12,
          "l7 screens[7].explain, quiz[0].explain: the barycentric form is stable on well-placed nodes (degree 400 on Chebyshev nodes, error below 1e-12)")


# ---------------------------------------------------------------- l8
def splines():
    ns = {}
    exec(load("l8-splines")["screens"][7]["widget"]["solution"], ns)
    exec(load("l7-interpolation")["screens"][7]["widget"]["solution"], ns)
    t = np.array([1, 2, 3, 5, 7, 10, 20, 30.0])
    z = np.array([4.1, 3.95, 3.9, 3.95, 4.05, 4.25, 4.7, 4.8])
    cs = CubicSpline(t, z, bc_type="natural")
    M = ns["natural_spline_M"](t, z)
    poly = ns["lagrange_eval"](t, z, np.array([4.0, 15.0, 25.0]))
    check("degree_7_polynomial_wiggles", np.allclose(poly, [3.9103, 5.1921, -2.58], atol=5e-3),
          "l8 screens[0]: the degree-7 polynomial gives 3.9103%, 5.1921% and -2.58% at 4, 15 and 25 years")
    check("natural_spline", np.allclose(M, cs(t, 2), atol=1e-12) and M[0] == 0 and abs(M[-1]) < 1e-15
          and close(float(cs(4)), 3.9114, abs_=5e-5) and close(float(cs(15)), 4.5297, abs_=5e-5)
          and np.allclose(M[1:7], [0.1372, 0.0510, 0.0033, 0.0107, -0.0047, -0.0041], atol=5e-5)
          and close(ns["spline_eval"](t, z, M, 15.0), float(cs(15)), abs_=1e-12),
          "l8 screens[1], [3], [7]: the tridiagonal system reproduces CubicSpline(bc_type='natural'); 3.9114% and 4.5297%")
    xs = np.linspace(1, 30, 2901)
    jumps = [abs(float(cs(k + 1e-9, nu)) - float(cs(k - 1e-9, nu))) for k in t[1:-1] for nu in (0, 1, 2)]
    j3 = [abs(float(cs(k + 1e-9, 3)) - float(cs(k - 1e-9, 3))) for k in t[1:-1]]
    check("spline_smoothness", max(jumps) < 1e-6 and min(j3) > 1e-4 and abs(float(cs(1.0, 2))) < 1e-12 and abs(float(cs(1.0, 1))) > 0.1,
          "l8 screens[1], quiz[0], quiz[2]: value, slope and second derivative match at each knot, the third jumps; natural ends have zero curvature, not zero slope")
    note("flat_ended", f"the natural spline's slope at the 1-year end is {float(cs(1.0, 1)):.3f}% per year, not 0: 'flat-ended' reads as zero slope, "
         "which quiz[2] calls the clamped spline (finding 16: l8 summary.ideas[0])")
    fwd = lambda x: float(cs(x) + x * cs(x, 1))
    check("forwards", close(fwd(4), 4.0273, abs_=5e-5) and close(fwd(15), 5.2010, abs_=5e-5) and close(3.95 + 5 * 0.05, 4.20) and close(3.95 + 5 * 0.025, 4.075)
          and max(abs(fwd(k + 1e-9) - fwd(k - 1e-9)) for k in t[1:-1]) < 1e-6 and close(4 + 10 * 0.1, 5.0),
          "l8 screens[4]; review-2 items[8]: f = z + t z'; straight-line zeros jump 12.5 bp at 5 years; the spline's forward is continuous")
    z2 = z.copy()
    z2[3] += 0.1
    cs2 = CubicSpline(t, z2, bc_type="natural")
    mv = (cs2(np.array([4, 6, 8.5, 15])) - cs(np.array([4, 6, 8.5, 15]))) * 100
    check("spline_is_global", np.allclose(mv, [5.51, 6.42, -2.67, 3.25], atol=0.01) and np.all(np.abs(cs2(t, 2) - cs(t, 2))[1:-1] > 0),
          "l8 screens[5], summary.ideas[2]; review-2 items[7]: a 10 bp bump at 5 years moves 4, 6, 8.5 and 15 years by 5.51, 6.42, -2.67, 3.25 bp; every inner M changes")
    d = np.abs(cs2(xs) - cs(xs)) * 100
    per = [d[(xs >= a) & (xs <= b)].max() for a, b in zip(t[:-1], t[1:])]
    note("moves_do_not_fade_monotonically", f"largest move per interval, in bp: {', '.join(f'{v:.2f}' for v in per)}; the 10 to 20 year interval moves more than 7 to 10 "
         "(finding 17: review-2 items[7] option 'amounts that fade with distance')")
    line = ns["natural_spline_M"]([0, 1, 3, 4], [1, 3, 7, 9])
    check("spline_special_cases", np.allclose(line, 0, atol=1e-12) and np.allclose(ns["natural_spline_M"]([0, 1, 2], [0, 1, 0]), [0, -3, 0])
          and np.allclose(ns["natural_spline_M"]([0, 1, 3], [0, 2, 2]), [0, -2, 0]),
          "l8 screens[6], [7]; homework-2 items[3]: data on a line give the line; M2 = -3 and M2 = -2 in the three-point cases")
    check("zero_prices", close(ns["zero_price"](t, z / 100, 4.0), 85.5169, abs_=1e-4) and close(100 * math.exp(-4 * 0.03925), 85.4704, abs_=1e-4)
          and close(100 / 1.03925 ** 4, 85.7274, abs_=1e-3),
          "l8 screens[7], quiz[1]: 85.5169 from the spline, 85.4704 from straight lines, continuously compounded")
    # no Runge swings: the natural spline of Runge's function improves as knots are added
    rf = lambda x: 1 / (1 + 25 * x ** 2)
    g = np.linspace(-1, 1, 4001)
    se = [np.abs(CubicSpline(np.linspace(-1, 1, n + 1), rf(np.linspace(-1, 1, n + 1)), bc_type="natural")(g) - rf(g)).max() for n in (10, 20, 40, 80)]
    check("spline_has_no_runge_swings", all(b < a for a, b in zip(se, se[1:])) and se[1] < 0.01,
          f"l8 summary.ideas[1]: on Runge's function with equal knots the spline error falls ({', '.join(f'{v:.1e}' for v in se)})")
    # slope formulas of homework-2 items[1]
    k = 3
    hL, hR = t[k] - t[k - 1], t[k + 1] - t[k]
    left = (z[k] - z[k - 1]) / hL + hL / 6 * (M[k - 1] + 2 * M[k])
    right = (z[k + 1] - z[k]) / hR - hR / 6 * (2 * M[k] + M[k + 1])
    check("spline_slope_rows", close(left, float(cs(t[k], 1)), abs_=1e-12) and close(right, float(cs(t[k], 1)), abs_=1e-12),
          "homework-2 items[1]: the two one-sided slope formulas agree with the spline's slope at the knot")


if __name__ == "__main__":
    root_finding_orders()
    safe_solver()
    interpolation()
    splines()
    tail = f"{N} checks passed, {len(EXPECTED)} EXPECTED_FAIL ({', '.join(EXPECTED) or 'none'})"
    if FAILED:
        print(f"L2 concepts: {tail}, {len(FAILED)} failing: {', '.join(FAILED)}")
        sys.exit(1)
    print(f"L2 concepts: {tail}")
