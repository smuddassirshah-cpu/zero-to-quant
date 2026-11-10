#!/usr/bin/env python3
"""Concept checks for numerics level 3 (l9 to l12, review-3, homework-3).

Run from anywhere: python3 docs/reports/numerics-L3-concepts.py
Each check names its ledger rows (docs/reports/audit-numerics-1-3-ledger.md).
Exit 0 means every checked claim holds. A check marked EXPECTED_FAIL fails
because the content is wrong as stated (a `wrong` finding of
docs/reviews/audit-numerics-1-3.md); it is reported, does not change the exit
code, and carries the corrected assert in a comment. A line starting "note"
records where a claim stops holding outside the case the lesson uses (the
`imprecise` findings); notes are measured and printed, not asserted against
the content.

Needs numpy and scipy. About 10 s (one loop of 10^7 RK4 steps).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm

COURSE = Path(__file__).resolve().parents[2] / "app/content/courses/numerics"
N = 0
FAILED = []
EXPECTED = []
BS = 10.450583572185565


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


def orders(errs):
    return [math.log2(abs(a) / abs(b)) for a, b in zip(errs, errs[1:])]


def g(z):
    return math.exp(-0.05) * np.maximum(100 * np.exp(0.03 + 0.2 * z) - 100, 0) * np.exp(-z ** 2 / 2) / math.sqrt(2 * math.pi)


# ---------------------------------------------------------------- l9
def newton_cotes():
    ns = {}
    exec(load("l9-quadrature")["screens"][8]["widget"]["solution"], ns)
    trap, simp = ns["trapezium"], ns["simpson"]
    I = math.e - 1
    te = [trap(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16, 32, 64)]
    se = [simp(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16, 32, 64)]
    check("trapezium_order_2", all(abs(p - 2) < 0.02 for p in orders(te)) and close(te[1], 0.00894, abs_=1e-5) and close(te[0], 0.0356, abs_=1e-4),
          "l9 screens[0], [1], summary: trapezium error falls by 4 per halving (order 2)")
    check("simpson_order_4", all(abs(p - 4) < 0.06 for p in orders(se)) and np.allclose(se[:4], [5.79e-4, 3.70e-5, 2.33e-6, 1.46e-7], rtol=0.01),
          "l9 screens[2], [5], summary: Simpson's error falls by 16 per halving (order 4) for a smooth integrand")
    for f, a, b, exact, d2, d4 in ((np.exp, 0, 1, I, math.e - 1, math.e - 1), (np.sin, 0, 2, 1 - math.cos(2), math.cos(0) - math.cos(2), None)):
        n = 64
        h = (b - a) / n
        lead = h ** 2 / 12 * (d2 if f is np.exp else (math.cos(2) - math.cos(0)))
        check(f"trapezium_error_formula_{f.__name__}", close(trap(f, a, b, n) - exact, lead, rel=0.01),
              "l9 screens[3]: rule minus integral is (b - a) h^2 / 12 times the average of f''")
    n = 4
    pred = (1 / 16) / 12 * (math.e - 1)
    check("trapezium_prediction", close(pred, 0.00895, abs_=1e-5) and te[1] > 0 and se[1] > 0,
          "l9 screens[3]: predicted 0.00895 against measured 0.00894; both rules sit above the integral of e^x")
    note("error_formula_sign", f"the lesson measures error as rule minus integral (+{te[1]:.5f}, +{se[1]:.2e}); the formulas -(b-a)h^2 f''/12 and -(b-a)h^4 f''''/180 "
         "are integral minus rule, so they are negative here (finding 19: l9 screens[1], [3], [7], summary.formula.note)")
    check("richardson_is_simpson", all(close((4 * trap(np.exp, 0, 1, 2 * n) - trap(np.exp, 0, 1, n)) / 3, simp(np.exp, 0, 1, 2 * n), abs_=1e-14) for n in (2, 4, 8, 16))
          and close((4 * 1.7272219 - 1.7539311) / 3, 1.7183188, abs_=1e-7) and close((4 * 2.0010 - 2.0040) / 3, 2.0, abs_=1e-12)
          and close((1 + 1 / 4) / 2, 5 / 8),
          "l9 screens[4], quiz[2]; review-3 items[2]: (4 T_2n - T_n)/3 is exactly Simpson's S_2n; averaging leaves 5/8 of c h^2")
    rng = np.random.default_rng(8)
    ok = True
    for _ in range(200):
        c = rng.standard_normal(4)
        a, b = sorted(rng.uniform(-3, 3, 2))
        p = np.poly1d(c)
        ok &= close(simp(p, a, b, 2), float(np.polyint(p)(b) - np.polyint(p)(a)), abs_=1e-10)
    q = np.poly1d([1, 0, 0, 0, 0])
    check("simpson_exact_for_cubics", ok and abs(simp(q, 0, 1, 2) - 0.2) > 1e-3 and close(simp(lambda x: x ** 3 - x, 0, 2, 2), 2.0, abs_=1e-12)
          and close(simp(lambda x: 4 * x ** 3 - x, 0, 1, 2), 0.5, abs_=1e-12),
          "l9 screens[7]; review-3 items[1]; homework-3 items[2]: one panel is exact for every cubic and not for x^4")
    raised = False
    try:
        simp(np.exp, 0, 1, 3)
    except ValueError:
        raised = True
    check("simpson_needs_even_n", raised, "l9 screens[2], [8]: Simpson's 1/3 rule needs an even number of strips")
    ke = [simp(g, -8, 8, n) - BS for n in (16, 32, 64, 128)]
    sp = [simp(g, -0.15, 8, n) - BS for n in (16, 32, 64, 128)]
    check("kink_inside_a_panel", np.allclose(ke, [0.600, 0.116, 0.0108, -0.00644], rtol=0.01) and np.allclose(sp, [9.26e-3, 5.10e-4, 3.10e-5, 1.92e-6], rtol=0.01)
          and all(abs(p - 4) < 0.2 for p in orders(sp)) and not all(abs(p - 4) < 0.5 for p in orders(ke)),
          "l9 screens[6], [9]: with the kink inside a panel the order is lost; integrating from the kink restores ratios near 16")

    def kink_error(parity, n):
        h = 16 / n
        j = n // 2 - (n // 2) % 2 + parity
        a = -0.15 - j * h
        ref = quad(g, -0.15, a + 16, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
        return abs(simp(g, a, a + 16, n) - ref)
    odd = [kink_error(1, n) for n in (16, 32, 64, 128, 256)]
    even = [kink_error(0, n) for n in (16, 32, 64, 128, 256)]
    po, pe = orders(odd)[-2:], orders(even)[-2:]
    # (corrected claim, fix pass) The content now says: put the kink where two panels meet, on an even-numbered
    # node, or split there. A kink on an odd-numbered node stays inside a panel and the order stays 2. Second
    # method: one panel of |x| on [-h, h] gives Simpson 2h^2/3 against the integral h^2, an O(h^2) panel error.
    h = 0.1
    panel = h / 3 * (abs(-h) + 4 * 0 + abs(h))
    l9 = load("l9-quadrature")
    l9_texts = [l9["screens"][6]["explain"]["text"], l9["screens"][9]["widget"]["options"][0]["text"], l9["screens"][9]["hints"][2]["text"], l9["summary"]["ideas"][2]]
    check("kink_on_any_node_restores_order_4", all(abs(p - 2) < 0.2 for p in po) and all(abs(p - 4) < 0.2 for p in pe)
          and close(panel, 2 * h * h / 3, rel=1e-12) and abs(panel - h * h) > 0.3 * h * h
          and all("two panels meet" in t or "even-numbered" in t for t in l9_texts) and not any("on a node" in t or "on nodes" in t for t in l9_texts),
          f"l9 screens[6], [9], summary.ideas[2] (finding 18, corrected claim, fix pass): order with the kink on an odd node {po[-1]:.2f} "
          f"(errors {odd[2]:.1e}, {odd[3]:.1e}), on an even node {pe[-1]:.2f}")
    check("doubling_counts", close(0.004 / 4, 0.001) and 3.7e-5 / 16 ** 3 > 1e-9 > 3.7e-5 / 16 ** 4 and 0.02 / 4 ** 3 > 1e-4 > 0.02 / 4 ** 4 and 0.02 / 16 ** 2 < 1e-4,
          "l9 quiz[0], quiz[1]; homework-3 items[0]; review-3 items[0]: halving h divides the error by 4 or 16")


# ---------------------------------------------------------------- l10
def gauss():
    ns = {}
    exec(load("l10-gaussian-quadrature")["screens"][7]["widget"]["solution"], ns)
    gl, glc, glp = ns["gl_integrate"], ns["gl_call_price"], ns["gl_put_price"]
    ok = True
    for n in range(1, 9):
        x, w = np.polynomial.legendre.leggauss(n)
        ok &= np.allclose(np.polynomial.legendre.Legendre.basis(n)(x), 0, atol=1e-12) and close(w.sum(), 2.0, rel=1e-13)
        for d in range(0, 2 * n + 1):
            exact = 0.0 if d % 2 else 2 / (d + 1)
            got = float(np.sum(w * x ** d))
            ok &= close(got, exact, abs_=1e-13) if d <= 2 * n - 1 else abs(got - exact) > 1e-6
    check("gauss_degree_2n_minus_1", ok, "l10 screens[1], quiz[1], summary; review-3 items[3]; homework-3 items[3]: n nodes at the roots of P_n are exact to degree 2n - 1 and not for degree 2n")
    x2, w2 = np.polynomial.legendre.leggauss(2)
    x3, w3 = np.polynomial.legendre.leggauss(3)
    check("gauss_small_rules", np.allclose(np.abs(x2), 1 / math.sqrt(3)) and np.allclose(w2, 1) and np.allclose(sorted(x3), [-math.sqrt(0.6), 0, math.sqrt(0.6)])
          and np.allclose(sorted(w3), [5 / 9, 5 / 9, 8 / 9]) and close(float(np.sum(w2 * x2 ** 4)), 2 / 9, rel=1e-12) and close(float(np.sum(w3 * x3 ** 6)), 0.24, rel=1e-12)
          and close(float(np.sum(w3 * x3 ** 4)), 0.4, rel=1e-12) and close(float(np.sum(w2 * (x2 ** 3 + 2 * x2 ** 2 + 1))), 10 / 3, rel=1e-12),
          "l10 screens[0], [1], [2], [6]: two- and three-node rules and their first failures (2/9 for x^4, 0.24 for x^6)")
    check("interval_map", close(gl(lambda t: t ** 5 - t, 0, 2, 3), 64 / 6 - 2, rel=1e-12) and close(gl(np.exp, 0, 1, 8), math.e - 1, abs_=1e-14)
          and close(float(np.sum(np.polynomial.legendre.leggauss(6)[1])) / 4, 0.5, rel=1e-12),
          "l10 screens[3], quiz[2]: the map to [a, b] needs the factor (b - a)/2; without it [0, 4] comes out at half")
    ge = [glc(100, 100, 0.05, 0.2, 1.0, n) - BS for n in (8, 16, 32)]
    tail = math.exp(-0.05) * (100 * math.exp(0.05) * norm.sf(7.8) - 100 * norm.sf(8))
    check("gauss_split_at_the_kink", np.allclose(ge[:2], [-1.32e-3, -2.0e-9], rtol=0.02) and close(ge[2], -tail, rel=0.05) and close(tail, 2.5e-13, rel=0.02),
          "l10 screens[4]: split at z*, Gauss errs by 1.3e-3, 2.0e-9 and then the cut-off tail 2.5e-13")
    gk = [gl(g, -8, 8, n) - BS for n in (8, 16, 32, 64)]
    ns9 = {}
    exec(load("l9-quadrature")["screens"][8]["widget"]["solution"], ns9)
    check("gauss_with_the_kink_inside", np.allclose(gk, [3.90, 0.927, 0.120, -0.036], rtol=0.01) and abs(gk[3]) > abs(ns9["simpson"](g, -8, 8, 64) - BS),
          "l10 screens[5]: with the kink inside, 64 Gauss nodes still err by 0.036, worse than Simpson with 64 strips")
    put = glp(100, 100, 0.05, 0.2, 1.0, 16)
    check("put_and_parity", close(put, 5.573526022256971, abs_=1e-8) and close(glc(100, 100, 0.05, 0.2, 1.0, 16) - put, 100 - 100 * math.exp(-0.05), abs_=1e-8),
          "l10 screens[7]: the put on [-8, z*] and put-call parity to 1e-8 with 16 nodes")
    d1 = (math.log(0.5) + 0.07) / 0.2
    bs200 = 100 * norm.cdf(d1) - 200 * math.exp(-0.05) * norm.cdf(d1 - 0.2)
    e16, e32 = abs(glc(100, 200, 0.05, 0.2, 1.0, 16) - bs200), abs(glc(100, 200, 0.05, 0.2, 1.0, 32) - bs200)
    # (corrected claim, fix pass) The content now says the far call is just as easy as the standard one. Second
    # method: the far call's piece [z*, 8] = [3.32, 8] is shorter than the standard call's [-0.15, 8], so the same
    # 16 nodes are denser there; 16 nodes reach the cut-off tail and 32 add nothing.
    zfar = (math.log(2) - 0.03) / 0.2
    l10x = load("l10-gaussian-quadrature")["screens"][7]["explain"]["text"]
    check("far_call_needs_32_nodes", e16 < 1e-11 and abs(e16 - e32) < 1e-14 and 8 - zfar < 8 + 0.15
          and "needs 32 nodes" not in l10x and "just as easy" in l10x,
          f"l10 screens[7].explain (finding 21, corrected claim, fix pass): with 16 nodes the K = 200 error is {e16:.1e}, with 32 it is {e32:.1e}; piece width {8 - zfar:.2f}")

    def dens(s):
        return np.exp(-(np.log(s / 100) - 0.03) ** 2 / 0.08) / (s * 0.2 * math.sqrt(2 * math.pi))
    tr = {Uq: [math.exp(-0.05) * gl(lambda s: (s - 100) * dens(s), 100, Uq, n) - BS for n in (64, 128)] for Uq in (200, 300, 400)}
    check("truncated_range", close(tr[200][0], -0.0483, abs_=1e-4) and close(tr[200][0], tr[200][1], abs_=1e-9) and close(tr[300][0], -9.2e-6, rel=0.01)
          and close(tr[400][0], -1.8e-9, rel=0.03),
          "l10 quiz[0]: on [K, 200] the error is -0.0483 whatever the node count; widening to 300 and 400 removes it")
    rng = np.random.default_rng(6)
    mc = [abs(np.mean(math.exp(-0.05) * np.maximum(100 * np.exp(0.03 + 0.2 * rng.standard_normal((40, n))) - 100, 0), axis=1) - BS).mean() for n in (10 ** 3, 10 ** 4, 10 ** 5)]
    slope = np.polyfit(np.log10([1e3, 1e4, 1e5]), np.log10(mc), 1)[0]
    check("monte_carlo_rate", -0.65 < slope < -0.35 and mc[2] > 1e-3,
          f"l10 screens[8] option mc: Monte Carlo error falls like 1/sqrt(n) (fitted slope {slope:.2f}; mean error {mc[2]:.3f} at 100,000 paths)")
    note("panels_and_strips", "l9 calls two strips one panel ('One panel, n = 2'); l10 screens[4], [8] call Simpson's 128 strips '128 panels' (finding 20). "
         "129 evaluations is 128 strips, 64 panels")


# ---------------------------------------------------------------- l11
def step_size():
    l11 = load("l11-step-size")
    ns = {}
    exec(l11["screens"][7]["widget"]["prelude"], ns)
    exec(l11["screens"][7]["widget"]["solution"], ns)
    rk4, euler, ark, sft = ns["rk4"], ns["euler"], ns["adaptive_rk4"], ns["steps_for_tol"]
    kap, th, sg = 0.5, 0.04, 0.1
    gam = math.sqrt(kap ** 2 + 2 * sg ** 2)
    eg = math.exp(gam * 5) - 1
    B5 = 2 * eg / ((gam + kap) * eg + 2 * gam)
    A5 = (2 * gam * math.exp((kap + gam) * 5 / 2) / ((gam + kap) * eg + 2 * gam)) ** (2 * kap * th / sg ** 2)
    cir = lambda t, y: np.array([1 - 0.5 * y[0] - 0.005 * y[0] ** 2, -0.02 * y[0]])
    y40 = rk4(cir, 0, [0, 0], 5 / 320, 320)
    check("cir_closed_form", close(B5, 1.812959, abs_=1e-6) and close(100 * A5 * math.exp(-B5 * 0.06), 79.1020, abs_=1e-4)
          and close(y40[0], B5, abs_=1e-10) and close(math.exp(y40[1]), A5, abs_=1e-10),
          "l11 screens[0]: the Riccati system B' = 1 - kB - s^2 B^2/2, (ln A)' = -k theta B matches the CIR closed form; B(5) = 1.812959, price 79.1020")
    ee = [abs(euler(cir, 0, [0, 0], 5 / n, n)[0] - B5) for n in (5, 10, 20, 40, 80, 160)]
    re = [rk4(cir, 0, [0, 0], 5 / n, n)[0] - B5 for n in (5, 10, 20, 40, 80, 160)]
    check("global_orders", all(abs(p - 1) < 0.06 for p in orders(ee)) and all(abs(p - 4) < 0.45 for p in orders(re)) and abs(orders(re)[-1] - 4) < 0.1
          and close(math.log10(ee[3] / ee[0]) / math.log10(8), -0.99, abs_=0.01) and close(math.log10(abs(re[3] / re[0])) / math.log10(8), -4.18, abs_=0.01),
          "l11 screens[0], [6], summary; review-3 items[5]: global error order 1 for Euler and 4 for RK4 (slopes -0.99 and -4.18 on the lesson's range)")
    f = lambda t, y: y * y
    exact = lambda t: 1 / (1 - t)
    loc_e = [abs(euler(f, 0, [1.0], h, 1)[0] - exact(h)) for h in (0.1, 0.05, 0.025, 0.0125)]
    loc_r = [abs(rk4(f, 0, [1.0], h, 1)[0] - exact(h)) for h in (0.1, 0.05, 0.025, 0.0125)]
    check("local_error_one_order_higher", all(abs(p - 2) < 0.15 for p in orders(loc_e)) and all(abs(p - 5) < 0.3 for p in orders(loc_r)),
          "l11 screens[1], [5]: one step errs like h^(p+1): h^2 for Euler, h^5 for RK4; the global order is one less")
    C = abs(re[1]) / 0.5 ** 4
    e65 = rk4(cir, 0, [0, 0], 5 / 65, 65)[0] - B5
    check("steps_for_tolerance", close(C, 2.81e-4, rel=0.005) and sft(rk4, cir, [0.0, 0.0], 5.0, B5, 1e-8, 4) == 65 and abs(e65) < 1e-8
          and close(abs(e65), 8.2e-9, rel=0.01) and sft(euler, cir, [0.0, 0.0], 5.0, B5, 1e-3, 1) == 494
          and math.ceil(1 / (1e-9 / 1e-3) ** 0.25) == 32 and close(0.0493 / 0.001 * 10, 493),
          "l11 screens[2], quiz[2]; review-3 items[6]: C from one run gives n = 65 for 1e-8 (true error 8.2e-9)")
    y10, y20 = rk4(cir, 0, [0, 0], 0.5, 10)[0], rk4(cir, 0, [0, 0], 0.25, 20)[0]
    est = (y10 - y20) / 15
    check("richardson_error_estimate", close(est, -1.10e-6, rel=0.01) and close(y20 - B5, -9.84e-7, rel=0.005) and abs(est / (y20 - B5) - 1) < 0.13,
          "l11 screens[3]: (y_h - y_h/2)/(2^p - 1) estimates the error of y_h/2 to within 12%, with the right sign")
    y, acc = ark(f, 0.0, [1.0], 0.95, 1e-8)
    fixed = abs(rk4(f, 0, [1.0], 0.95 / 400, 400)[0] - 20) / 20
    check("adaptive_controller", acc == 38 and close(abs(y[0] - 20) / 20, 2.4e-8, rel=0.05) and close(fixed, 7e-8, rel=0.05)
          and close(0.9 * 0.01 * (1e-8 / 3.2e-7) ** 0.2, 0.0045, rel=1e-9),
          "l11 screens[4], [7], quiz[0]; homework-3 items[5]: 38 accepted steps; per-step tolerance 1e-8 ends as 2.4e-8; 400 fixed steps give 7e-8")

    def rk4s(n, lam=-1.0):
        h, y = 1.0 / n, 1.0
        for _ in range(n):
            k1 = lam * y
            k2 = lam * (y + h / 2 * k1)
            k3 = lam * (y + h / 2 * k2)
            k4 = lam * (y + h * k3)
            y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return abs(y - math.exp(lam)) / math.exp(lam)
    floor = [rk4s(n) for n in (10, 100, 1000, 10 ** 4, 10 ** 5)]
    e7 = rk4s(10 ** 7)
    check("rounding_floor", floor[1] / floor[0] < 1e-3 and max(floor[2:]) < 1e-12 and min(floor[2:]) > 0 and e7 > 0,
          "l11 quiz[1]; review-3 items[9] key: RK4's error stops falling near 1e-14 to 1e-15; below the floor more steps only add rounding")
    note("rounding_per_step_is_a_bound", f"with 10^7 RK4 steps the measured error is {e7:.1e}, against n eps = {1e7 * 2.2e-16:.1e}; with 10^8 steps it is about 5e-13 against 2e-8 "
         "(audit run). 'Each step adds about eps, near 1e-8 in all' is the worst-case bound, about 10,000 times the measured drift (finding 22: review-3 items[9])")


# ---------------------------------------------------------------- l12
def stiff():
    A = np.array([[-0.5, 0], [50, -50.0]])
    c = np.array([0.02, 0])
    y0 = np.array([0.06, 0.03])
    rex = lambda t: 0.04 + 0.02 * 50 / 49.5 * math.exp(-0.5 * t) + (0.03 - 0.04 - 0.02 * 50 / 49.5) * math.exp(-50 * t)
    ref = solve_ivp(lambda t, y: A @ y + c, [0, 1], y0, method="Radau", rtol=1e-12, atol=1e-14).y[1, -1]

    def eul(h):
        y = y0.copy()
        for _ in range(round(1 / h)):
            y = y + h * (A @ y + c)
        return y[1]
    check("two_speed_model", close(rex(1), 0.052253, abs_=1e-6) and close(ref, rex(1), abs_=1e-10) and np.allclose(sorted(np.linalg.eigvals(A)), [-50, -0.5]),
          "l12 screens[0], [1]: the closed form r(1) = 5.2253% and the two decay rates -0.5 and -50")
    check("euler_stability_limit", close(eul(0.04), 0.082393, abs_=1e-6) and close(eul(0.05), -100.38, abs_=0.01) and close(eul(0.02), 0.052222, abs_=1e-6)
          and abs(eul(0.03) - rex(1)) < 1e-3 and abs(eul(0.039) - rex(1)) < 0.05 and abs(eul(0.041) - rex(1)) > 0.05
          and close(1.5 ** 20, 3325, rel=0.001),
          "l12 screens[0], [1], [5], quiz[0]; review-3 items[7]; homework-3 items[7]: Euler is stable for h < 2/50 = 0.04; 8.24% at 0.04; -10,038% at 0.05")
    ns = {}
    exec(load("l12-stiff-equations")["screens"][6]["widget"]["solution"], ns)
    ie, tr = ns["implicit_euler_linear"], ns["trapezoidal_linear"]
    check("implicit_euler_path", np.allclose([ie(A, c, y0, 0.25, k)[1] for k in (1, 2, 3, 4)], [0.055720, 0.055796, 0.054176, 0.052611], atol=1e-6)
          and all(abs(ie(A, c, y0, h, round(1 / h))[1] - rex(1)) < 0.003 for h in (0.05, 0.1, 0.25, 0.5, 1.0)),
          "l12 screens[2]: implicit Euler is stable at every step tried, up to h = 1; at h = 0.25 it gives 5.2611%")
    ie_err = [abs(ie(A, c, y0, h, round(1 / h))[1] - rex(1)) for h in (0.01, 0.005, 0.0025)]
    tr_err = [abs(tr(A, c, y0, h, round(1 / h))[1] - rex(1)) for h in (0.01, 0.005, 0.0025)]
    check("implicit_orders", all(abs(p - 1) < 0.1 for p in orders(ie_err)) and all(abs(p - 2) < 0.1 for p in orders(tr_err)),
          "l12 screens[2], [4]: implicit Euler is first order, the trapezoidal rule second order")
    check("trapezoidal_rings", np.allclose([tr(A, c, y0, 0.25, k)[1] for k in (1, 2, 3, 4)], [0.079696, 0.039891, 0.065346, 0.043941], atol=1e-6)
          and close((1 - 6.25) / (1 + 6.25), -0.7241, abs_=1e-4) and close((1 - 20) / (1 + 20), -0.905, abs_=1e-3) and close(tr(A, c, y0, 0.05, 20)[1], 0.0522528, abs_=1e-6)
          and close(math.exp(-12.5), 4e-6, rel=0.1),
          "l12 screens[4], [6]; review-3 items[8]: the trapezoidal rule at h = 0.25 rings 7.97%, 3.99%, 6.53%, 4.39% with factor -0.7241")
    R = {"euler": lambda z: 1 + z, "implicit": lambda z: 1 / (1 - z), "trap": lambda z: (1 + z / 2) / (1 - z / 2),
         "rk4": lambda z: 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24}
    zs = [complex(a, b) for a in np.linspace(-60, -0.01, 120) for b in np.linspace(-40, 40, 81)]
    lim = brentq(lambda z: abs(R["rk4"](z)) - 1, -3, -2.5)
    check("stability_regions", all(abs(R["implicit"](z)) < 1 and abs(R["trap"](z)) < 1 for z in zs)
          and np.allclose([abs(R[k](-2.5)) for k in ("euler", "implicit", "trap", "rk4")], [1.5, 0.286, 0.111, 0.648], atol=1e-3)
          and close(lim, -2.7853, abs_=1e-4) and close(2.7853 / 50, 0.0557, abs_=1e-4) and abs(R["rk4"](-2.9)) > 1 and abs(R["euler"](-2.01)) > 1
          and abs(R["trap"](-1e9) + 1) < 1e-8 and abs(R["implicit"](-1e9)) < 1e-8 and close(1 / 13.5, 0.0741, abs_=1e-4) and close(1 / 11, 0.0909, abs_=1e-4),
          "l12 screens[3], [5], quiz[1]; homework-3 items[1], [4]: amplification factors; implicit Euler and trapezoidal stable on the left half-plane; RK4 to -2.7853; trapezoidal factor tends to -1, implicit Euler's to 0")
    # amplification factors measured from the steppers themselves on y' = lambda y
    lam, h = -50.0, 0.25
    Am = np.array([[lam]])
    check("factors_from_code", close(ie(Am, [0.0], [1.0], h, 1)[0], 1 / (1 - h * lam), rel=1e-12) and close(tr(Am, [0.0], [1.0], h, 1)[0], (1 + h * lam / 2) / (1 - h * lam / 2), rel=1e-12),
          "l12 screens[2], [4]: the coded steppers multiply a mode by 1/(1 - h lambda) and (1 + h lambda/2)/(1 - h lambda/2)")
    nf = {}
    for m in ("RK45", "Radau", "BDF"):
        s = solve_ivp(lambda t, y: A @ y + c, [0, 10], y0, method=m, rtol=1e-6, atol=1e-9)
        nf[m] = (s.nfev, abs(s.y[1, -1] - rex(10)))
    check("solve_ivp_cost", nf["RK45"][0] > 2 * nf["BDF"][0] and nf["RK45"][0] > 2 * nf["Radau"][0] and all(v[1] < 1e-6 for v in nf.values()),
          f"l12 screens[7]: explicit RK45 needs several times the evaluations of Radau and BDF on the stiff model (here {nf['RK45'][0]}, {nf['Radau'][0]}, {nf['BDF'][0]}; the lesson quotes 1,172, 422, 226)")
    # explicit step limit scales with the square of the grid spacing (heat-equation model of the BS operator)
    lams = []
    for m in (20, 40, 80):
        dx = 1 / m
        L = (np.diag(-2 * np.ones(m - 1)) + np.diag(np.ones(m - 2), 1) + np.diag(np.ones(m - 2), -1)) / dx ** 2
        lams.append(np.abs(np.linalg.eigvalsh(L)).max())
    check("grid_stiffness", all(abs(b / a - 4) < 0.05 for a, b in zip(lams, lams[1:])),
          "l12 screens[8]: halving the grid spacing multiplies the fastest rate by 4, so the stable explicit step falls by 4")


if __name__ == "__main__":
    newton_cotes()
    gauss()
    step_size()
    stiff()
    tail = f"{N} checks passed, {len(EXPECTED)} EXPECTED_FAIL ({', '.join(EXPECTED) or 'none'})"
    if FAILED:
        print(f"L3 concepts: {tail}, {len(FAILED)} failing: {', '.join(FAILED)}")
        sys.exit(1)
    print(f"L3 concepts: {tail}")
