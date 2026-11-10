#!/usr/bin/env python3
"""Round-3 blind concept audit, numerics level 3 (l9 to l12, review-3, homework-3).

Independent experiments, plus attacks on the lesson's own solutions (loaded from
the content JSON and run in CPython). Exit 0 when the content is right. A check
that fails because the content is wrong is registered with expected_fail=True:
it prints EXPECTED_FAIL, leaves the exit code alone, and carries the corrected
assert in a comment beside it.
Run: python3 docs/reports/numerics-L3-concepts-r3.py
"""
import json, math, os, sys, warnings
import numpy as np
from scipy.stats import norm
from scipy.integrate import solve_ivp, quad

warnings.simplefilter("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "numerics")
FAILS, XFAILS, N = [], [], 0


def check(name, cond, detail="", expected_fail=False):
    global N
    N += 1
    if cond:
        print(f"PASS  {name}  {detail}")
    elif expected_fail:
        XFAILS.append(name)
        print(f"EXPECTED_FAIL  {name}  {detail}")
    else:
        FAILS.append(name)
        print(f"FAIL  {name}  {detail}")


def near(a, b, rel=0.0, ab=0.0):
    return abs(a - b) <= max(rel * abs(b), ab)


def load(fname, where, idx):
    j = json.load(open(os.path.join(COURSE, fname + ".json")))
    w = j[where][idx]["widget"]
    env = {}
    exec(w.get("prelude", ""), env)
    exec(w["solution"], env)
    return env


rng = np.random.default_rng(9)

# ---------------------------------------------------------------- l9 trapezium and Simpson


def trap(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)


def simp(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / n / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


I = math.e - 1
te = [trap(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16)]
se = [simp(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16)]
check("l9.s0-1 trapezium errors", all(near(a, c, rel=0.003) for a, c in zip(te, [0.0356, 0.00894, 0.00224, 0.000559])), str(te))
check("l9.s2 Simpson errors", all(near(a, c, rel=0.003) for a, c in zip(se, [5.79e-4, 3.70e-5, 2.33e-6, 1.46e-7])), str(se))
check("l9 ratios", near(te[0] / te[1], 3.99, ab=0.01) and near(te[2] / te[3], 4.0, ab=0.01) and near(se[0] / se[1], 15.6, ab=0.06)
      and near(se[1] / se[2], 15.9, ab=0.05) and near(se[2] / se[3], 16.0, ab=0.05))
check("l9.s3 predicted trapezium error from the mean of f''", near(1 / 16 / 12 * (math.e - 1), 0.00895, ab=5e-6) and te[1] > 0)
# error formulas with their signs: integral minus rule = -(b-a)h^2/12 f''(xi) and -(b-a)h^4/180 f''''(xi)
ok = True
for n in (2, 4, 8, 16, 32):
    h = 1 / n
    xi2 = -(I - trap(np.exp, 0, 1, n)) / (h * h / 12)
    xi4 = -(I - simp(np.exp, 0, 1, n)) / (h ** 4 / 180)
    ok &= 1 <= xi2 <= math.e and 1 <= xi4 <= math.e
check("l9.s1/s7 error formulas hold with f''(xi), f''''(xi) inside [1, e]", ok)
check("l9.s4 Richardson of T4, T8 equals S8", near((4 * trap(np.exp, 0, 1, 8) - trap(np.exp, 0, 1, 4)) / 3, simp(np.exp, 0, 1, 8), ab=1e-14)
      and near(simp(np.exp, 0, 1, 8), 1.7182841547, ab=5e-11))
okr = True
for _ in range(200):
    c = rng.normal(size=6)
    f = lambda x: np.polyval(c, x) + np.sin(3 * x)
    n = int(rng.choice([2, 4, 6, 10]))
    okr &= near((4 * trap(f, -1, 2, 2 * n) - trap(f, -1, 2, n)) / 3, simp(f, -1, 2, 2 * n), ab=1e-10)
check("l9.s4 Richardson of the trapezium rule IS Simpson's rule (200 random f)", okr)
check("l9.s5 slope", near((math.log10(1.46e-7) - math.log10(5.79e-4)) / math.log10(8), -3.98, ab=0.01))
m, s_ = 0.03, 0.2
g = lambda z: math.exp(-0.05) * np.maximum(100 * np.exp(m + s_ * z) - 100, 0) * np.exp(-z ** 2 / 2) / math.sqrt(2 * math.pi)
C0 = 100 * norm.cdf(0.35) - 100 * math.exp(-0.05) * norm.cdf(0.15)
ke = [simp(g, -8, 8, n) - C0 for n in (16, 32, 64, 128)]
check("l9.s6 Simpson errors with the kink inside", all(near(a, c, rel=0.01) for a, c in zip(ke, [0.600, 0.116, 0.0108, -0.00644])), str(ke))
sp = [simp(g, -0.15, 8, n) - C0 for n in (16, 32, 64, 128)]
check("l9.s6 split errors", all(near(a, c, rel=0.01) for a, c in zip(sp, [9.26e-3, 5.10e-4, 3.10e-5, 1.92e-6])), str(sp))
check("l9.s6 split restores ratios near 16", all(14 < sp[i] / sp[i + 1] < 19 for i in range(3)))
tail = 100 * norm.sf(8 - 0.2) - 100 * math.exp(-0.05) * norm.sf(8)
check("l9.s6 tail beyond z=8 is about 1e-13", 1e-13 < tail < 5e-13, f"{tail:.2e}")
# with the kink inside a panel the error is second order and erratic, for both rules:
# error * n^2 stays bounded but changes size and sign from one even n to the next
for lo_n in (200, 2000):
    sc = [(simp(g, -8, 8, n) - C0) * n * n for n in range(lo_n, lo_n + 200, 2)]
    tc = [(trap(g, -8, 8, n) - C0) * n * n for n in range(lo_n, lo_n + 200, 2)]
    flips = sum(1 for u, v in zip(sc, sc[1:]) if u * v < 0)
    check(f"l9.s6/s9 kink inside, n near {lo_n}: Simpson error is O(h^2) and erratic", max(abs(v) for v in sc) < 400 and flips > 20 and min(sc) < -100 and max(sc) > 50,
          f"error*n^2 from {min(sc):.0f} to {max(sc):.0f}, {flips} sign changes in 100 values of n")
    check(f"l9.s9 kink inside, n near {lo_n}: trapezium error is O(h^2) and erratic", max(abs(v) for v in tc) < 200 and min(tc) < -50 and max(tc) > 50,
          f"error*n^2 from {min(tc):.0f} to {max(tc):.0f}")
# kink on an even-numbered node restores order 4; on an odd-numbered node it does not
ev = [abs(simp(g, -8.15, 7.85, n) - (C0 - 0)) for n in (32, 64, 128, 256)]     # h = 0.5, 0.25, ... ; kink at node 16, 32, ...
ev_ref = quad(g, -0.15, 7.85, epsabs=1e-14, epsrel=1e-14)[0]
ev = [abs(simp(g, -8.15, 7.85, n) - ev_ref) for n in (32, 64, 128, 256)]
od_ref = quad(g, -0.15, 8.1, epsabs=1e-14, epsrel=1e-14)[0]
od = [abs(simp(g, -8.4, 8.1, n) - od_ref) for n in (66, 198, 594)]              # h = 0.25, kink at node 33; then 99; then 297: all odd
check("l9.s6 kink on an even-numbered node: ratios near 16", all(13 < ev[i] / ev[i + 1] < 19 for i in range(3)), str([f"{v:.2e}" for v in ev]))
check("l9.s6 kink on an odd-numbered node: order 2 only (ratio 9 for h/3)", all(7 < od[i] / od[i + 1] < 11 for i in range(2)), str([f"{v:.2e}" for v in od]))
check("l9.s7 cubic exact with one panel", near(simp(lambda x: x ** 3 - x, 0, 2, 2), 2.0, ab=1e-14)
      and near(simp(lambda x: 4 * x ** 3 - x, 0, 1, 2), 0.5, ab=1e-15))
okc = all(near(simp(lambda x, c=c: np.polyval(c, x), -1.3, 0.9, 2), np.polyval(np.polyint(c), 0.9) - np.polyval(np.polyint(c), -1.3), ab=1e-12)
          for c in rng.normal(size=(200, 4)))
check("l9.s7/h3 Simpson exact for 200 random cubics, not for x^4", okc and abs(simp(lambda x: x ** 4, -1, 1, 2) - 0.4) > 0.1)
check("l9 quizzes", near(3.70e-5 / 16 ** 3, 9.0e-9, rel=0.01) and near(3.70e-5 / 16 ** 4, 5.6e-10, rel=0.01)
      and near((4 * 1.7272219 - 1.7539311) / 3, 1.7183188, ab=1e-7) and near(trap(np.exp, 0, 1, 2), 1.7539311, ab=5e-8)
      and near(trap(np.exp, 0, 1, 4), 1.7272219, ab=5e-8) and near((1.7539311 + 1.7272219) / 2, 1.7405765, ab=1e-7))
check("r3/h3 arithmetic", near((4 * 2.0010 - 2.0040) / 3, 2.0, ab=1e-12) and near(0.02 / 4 ** 4, 7.8e-5, rel=0.01)
      and near(0.02 / 4 ** 3, 3.1e-4, rel=0.01) and near(0.02 / 16 ** 2, 7.8e-5, rel=0.01))

# ---------------------------------------------------------------- l10 Gauss-Legendre
okg = True
for n in range(1, 9):
    x, w = np.polynomial.legendre.leggauss(n)
    for d in range(2 * n + 1):
        ex = 0.0 if d % 2 else 2 / (d + 1)
        exact = abs(np.sum(w * x ** d) - ex) < 1e-13
        okg &= exact if d <= 2 * n - 1 else not exact
    okg &= np.allclose(np.sort(np.roots(np.polynomial.legendre.leg2poly([0] * n + [1])[::-1])), x, atol=1e-10) and near(w.sum(), 2, ab=1e-13)
check("l10.s1 n nodes at the roots of P_n: exact to degree 2n-1 and not 2n (n = 1 to 8); weights sum to 2", okg)
x3, w3 = np.polynomial.legendre.leggauss(3)
check("l10.s0-2 small rules", near(2 * (1 / 3) ** 2, 2 / 9, ab=1e-15) and np.allclose(x3, [-math.sqrt(0.6), 0, math.sqrt(0.6)])
      and np.allclose(w3, [5 / 9, 8 / 9, 5 / 9]) and near(np.sum(w3 * x3 ** 6), 0.24, ab=1e-12) and near(np.sum(w3 * x3 ** 4), 0.4, ab=1e-12))
f6 = lambda v: v ** 3 + 2 * v ** 2 + 1
check("l10.s6", near(f6(-1 / math.sqrt(3)), 1.4742, ab=5e-5) and near(f6(1 / math.sqrt(3)), 1.8591, ab=5e-5)
      and near(f6(-1 / math.sqrt(3)) + f6(1 / math.sqrt(3)), 10 / 3, ab=1e-13))


def gl(f, a, b, n):
    x, w = np.polynomial.legendre.leggauss(n)
    return (b - a) / 2 * np.sum(w * f((b - a) / 2 * x + (a + b) / 2))


gs = [gl(g, -0.15, 8, n) - C0 for n in (8, 16, 32)]
check("l10.s4 Gauss errors on the smooth piece", near(gs[0], -1.32e-3, rel=0.01) and near(gs[1], -2.0e-9, rel=0.05) and near(gs[2], -2.6e-13, rel=0.2),
      str(gs))
check("l10.s4 the 32-node error is the tail cut off at z=8", near(tail, 2.5e-13, rel=0.05) and near(-gs[2], tail, rel=0.25), f"tail {tail:.3e}")
gk = [gl(g, -8, 8, n) - C0 for n in (8, 16, 32, 64)]
check("l10.s5 Gauss errors with the kink inside", all(near(a, c, rel=0.02) for a, c in zip(gk, [3.90, 0.927, 0.120, -0.036])), str(gk))
check("l10.s5 unsplit Gauss at 64 nodes is worse than unsplit Simpson at 64 strips", abs(gk[3]) > abs(ke[2]))
E10 = load("l10-gaussian-quadrature", "screens", 7)
P0 = C0 - 100 + 100 * math.exp(-0.05)
d1 = (math.log(100 / 200) + 0.07) / 0.2
C200 = 100 * norm.cdf(d1) - 200 * math.exp(-0.05) * norm.cdf(d1 - 0.2)
check("l10.s7 table", near(C0, 10.450584, ab=5e-7) and near(P0, 5.573526, ab=5e-7) and near(C200, 0.004799, ab=5e-7)
      and near(E10["gl_call_price"](100, 200, 0.05, 0.2, 1.0, 32), C200, ab=1e-10) and near((math.log(2) - 0.03) / 0.2, 3.32, ab=0.01))
# attack: random strikes near the money (|z*| below 2.5), 32 nodes
worst = 0.0
for _ in range(500):
    sg = float(rng.uniform(0.08, 0.5)); T = float(rng.uniform(0.05, 1.4)); r = float(rng.uniform(0, 0.1))
    K = 100 * math.exp(float(rng.uniform(-2.5, 2.5)) * sg * math.sqrt(T))
    dd = (math.log(100 / K) + (r + sg * sg / 2) * T) / (sg * math.sqrt(T))
    c = 100 * norm.cdf(dd) - K * math.exp(-r * T) * norm.cdf(dd - sg * math.sqrt(T))
    worst = max(worst, abs(E10["gl_call_price"](100, K, r, sg, T, 32) - c), abs(E10["gl_put_price"](100, K, r, sg, T, 32) - (c - 100 + K * math.exp(-r * T))))
check("l10.s7 attack: 500 random calls and puts within 2.5 sd of the money, 32 nodes", worst < 1e-8, f"worst {worst:.1e}")


def bsc(K, sg, T, r=0.05):
    dd = (math.log(100 / K) + (r + sg * sg / 2) * T) / (sg * math.sqrt(T))
    return 100 * norm.cdf(dd) - K * math.exp(-r * T) * norm.cdf(dd - sg * math.sqrt(T))


# l10 screens[8].explain: "Sixteen evaluations per price give 2e-9, so 2,000 prices cost 32,000 evaluations."
# That is the at-the-money figure. The smooth piece [z*, 8] is longer for a strike in the money, and 16 nodes no longer do.
book = {K: abs(E10["gl_call_price"](100, K, 0.05, 0.2, 1.0, 16) - bsc(K, 0.2, 1.0)) for K in (50, 70, 85, 100, 120, 150)}
# (corrected claim, fix pass) l10 screens[8].explain now reads: at the money 16 evaluations give 2e-9; a strike deep in
# the money needs 32, so 2,000 prices cost at most 64,000. Own computation: 16 integrand evaluations per price, counted
# by instrumenting gl_integrate and equal to n for one smooth piece; 2,000 x 16 = 32,000 and 2,000 x 32 = 64,000; errors below.
_l10 = json.load(open(os.path.join(COURSE, "l10-gaussian-quadrature.json")))
_x8 = _l10["screens"][8]["explain"]["text"]
_cnt = [0]
_Ec = {"CNT": _cnt}
exec(_l10["screens"][7]["widget"]["solution"].replace("    return float((b - a) / 2 * np.sum(w * f(t)))",
                                                     "    CNT[0] += len(t)\n    return float((b - a) / 2 * np.sum(w * f(t)))"), _Ec)
_Ec["gl_call_price"](100, 100, 0.05, 0.2, 1.0, 16)
check("l10.s8 16 evaluations give 2e-9 at the money, 32 cover the deep strikes, at most 64,000 for 2,000 prices (corrected claim, fix pass)",
      _cnt[0] == 16 and near(book[100], 2.0e-9, rel=0.05) and max(book.values()) > 1e-8 and 2000 * 16 == 32000 and 2000 * 32 == 64000
      and all(abs(E10["gl_call_price"](100, K, 0.05, 0.2, 1.0, 32) - bsc(K, 0.2, 1.0)) < 1e-9 for K in book)
      and "needs 32" in _x8 and "at most 64,000 evaluations" in _x8 and "32,000" not in _x8,
      f"{_cnt[0]} evaluations per price; 16-node errors " + ", ".join(f"K={K}: {v:.1e}" for K, v in book.items()))
check("l10.s8 corrected: 16 nodes at the money, 32 nodes across the book", book[100] < 1e-8
      and all(abs(E10["gl_call_price"](100, K, 0.05, 0.2, 1.0, 32) - bsc(K, 0.2, 1.0)) < 1e-8 for K in book))
# l10 screens[7] solution integrates from z* even when z* lies beyond -zmax (the homework-3 solution clips at the ends)
deep = abs(E10["gl_call_price"](100, 50, 0.05, 0.2, 1 / 52, 32) - bsc(50, 0.2, 1 / 52))
deep_h3 = abs(load("homework-3", "items", 6)["price_by_quadrature"](lambda v: np.maximum(v - 50, 0), [50], 100, 0.05, 0.2, 1 / 52, 32) - bsc(50, 0.2, 1 / 52))
# (corrected claim, fix pass) the solution now clips z* to [-zmax, zmax]. Own computation: z* = -25.0 for this call, and
# the clipped price matches Black-Scholes (here S - K e^{-rT}, since d1 and d2 are near 25) to 1e-8, as homework-3's does.
_zs = (math.log(50 / 100) - (0.05 - 0.02) / 52) / (0.2 * math.sqrt(1 / 52))
check("l10.s7 a one-week call struck at 50 is priced to 1e-8 with 32 nodes (corrected claim, fix pass)",
      deep < 1e-8 and deep_h3 < 1e-8 and _zs < -8 and near(bsc(50, 0.2, 1 / 52), 100 - 50 * math.exp(-0.05 / 52), ab=1e-12)
      and abs(E10["gl_call_price"](100, 1000, 0.05, 0.2, 1.0, 32)) == 0.0,
      f"z* = {_zs:.2f}; lesson solution {deep:.1e}, homework-3 solution {deep_h3:.1e}")
dens = lambda S: np.exp(-((np.log(S / 100) - m) / s_) ** 2 / 2) / (S * s_ * math.sqrt(2 * math.pi))
qe = {U: [math.exp(-0.05) * gl(lambda S: (S - 100) * dens(S), 100, U, n) - C0 for n in (64, 128)] for U in (200, 300, 400)}
check("l10.q0 truncation in S_T", near(qe[200][0], -0.0483, rel=0.01) and near(qe[200][1], qe[200][0], ab=1e-9) and near(qe[300][0], -9.2e-6, rel=0.02)
      and near(qe[400][0], -1.8e-9, rel=0.05), str(qe))
# homework-3 pricer
E3 = load("homework-3", "items", 6)["price_by_quadrature"]
d110 = (math.log(100 / 110) + 0.07) / 0.2
C110 = 100 * norm.cdf(d110) - 110 * math.exp(-0.05) * norm.cdf(d110 - 0.2)
check("h3 closed forms", near(C0 - C110, 4.410495442461325, ab=1e-12) and near(math.exp(-0.05) * norm.cdf(0.15), 0.5323248154537634, ab=1e-13)
      and near(100 - 100 * math.exp(-0.05), 4.877057549928594, ab=1e-12) and norm.pdf(8) < 1e-14)
check("h3 solution: spread, digital, strangle", near(E3(lambda s: np.clip(s - 100, 0, 10), [100, 110], 100, 0.05, 0.2, 1.0, 24), C0 - C110, ab=1e-9)
      and near(E3(lambda s: (s > 100).astype(float), [100], 100, 0.05, 0.2, 1.0, 24), math.exp(-0.05) * norm.cdf(0.15), ab=1e-9))
check("h3 a forgotten kink costs accuracy", abs(E3(lambda s: np.maximum(s - 100, 0), [], 100, 0.05, 0.2, 1.0, 24) - C0) > 1e-3)

# ---------------------------------------------------------------- l11 step size and order
kap, th, sg = 0.5, 0.04, 0.10
gam = math.sqrt(kap ** 2 + 2 * sg ** 2)
den = (gam + kap) * (math.exp(gam * 5) - 1) + 2 * gam
B5 = 2 * (math.exp(gam * 5) - 1) / den
A5 = (2 * gam * math.exp((kap + gam) * 5 / 2) / den) ** (2 * kap * th / sg ** 2)
cir = lambda t, y: np.array([1 - kap * y[0] - 0.5 * sg ** 2 * y[0] ** 2, -kap * th * y[0]])


def rk4(f, t0, y0, h, n):
    t, y = t0, np.array(y0, float)
    for _ in range(n):
        k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    return y


def euler(f, t0, y0, h, n):
    t, y = t0, np.array(y0, float)
    for _ in range(n):
        y = y + h * f(t, y); t += h
    return y


ref = solve_ivp(cir, [0, 5], [0, 0], rtol=1e-13, atol=1e-15, method="DOP853").y[:, -1]
check("l11.s0 closed form B(5), ln A(5) against DOP853", near(B5, 1.812959, ab=5e-7) and near(ref[0], B5, ab=1e-11) and near(ref[1], math.log(A5), ab=1e-11),
      f"B5={B5:.10f}")
check("l11.s0 bond price at r0 = 6%", near(100 * A5 * math.exp(-B5 * 0.06), 79.1020, ab=5e-5), f"{100 * A5 * math.exp(-B5 * 0.06):.4f}")
eu = {n: abs(euler(cir, 0, [0, 0], 5 / n, n)[0] - B5) for n in (5, 10, 20, 40)}
rk = {n: abs(rk4(cir, 0, [0, 0], 5 / n, n)[0] - B5) for n in (5, 10, 20, 40, 65)}
check("l11.s0 errors", near(eu[5], 0.0964, rel=0.005) and near(eu[40], 0.0124, rel=0.005) and near(rk[5], 3.49e-4, rel=0.005) and near(rk[40], 5.83e-8, rel=0.005)
      and near(eu[10], 0.0493, rel=0.005) and near(rk[10], 1.75e-5, rel=0.005))
check("l11.s0 slopes", near(math.log10(eu[40] / eu[5]) / math.log10(8), -0.99, ab=0.01) and near(math.log10(rk[40] / rk[5]) / math.log10(8), -4.18, ab=0.01))
check("l11.s0 chart points", np.allclose([math.log10(eu[n]) for n in (5, 10, 20, 40)], [-1.0159, -1.3069, -1.6068, -1.908], atol=2e-3)
      and np.allclose([math.log10(rk[n]) for n in (5, 10, 20, 40)], [-3.4574, -4.7559, -6.0068, -7.2343], atol=2e-3))
# local error like h^(p+1): one step from the same state, h against h/2
y0 = rk4(cir, 0, [0, 0], 0.05, 20)
one = lambda meth, h: meth(cir, 1.0, y0, h, 1)[0] - solve_ivp(cir, [1.0, 1.0 + h], y0, rtol=1e-13, atol=1e-16, method="DOP853").y[0, -1]
check("l11.s1 local errors: Euler like h^2, RK4 like h^5", near(one(euler, 0.2) / one(euler, 0.1), 4, rel=0.1) and near(one(rk4, 0.4) / one(rk4, 0.2), 32, rel=0.15),
      f"{one(euler, 0.2) / one(euler, 0.1):.2f} {one(rk4, 0.4) / one(rk4, 0.2):.1f}")
C = rk[10] / 0.5 ** 4
check("l11.s2 step for 1e-8", near(C, 2.81e-4, rel=0.005) and math.ceil(5 / (1e-8 / C) ** 0.25) == 65 and near(rk[65], 8.2e-9, rel=0.02)
      and near(C * (5 / 64) ** 4, 1.05e-8, rel=0.01) and near(C * (5 / 60) ** 4, 1.35e-8, rel=0.01))
y10, y20 = rk4(cir, 0, [0, 0], 0.5, 10)[0], rk4(cir, 0, [0, 0], 0.25, 20)[0]
check("l11.s3 two-run estimate", near(y10, 1.81294125, ab=5e-9) and near(y20, 1.81295781, ab=5e-9) and near((y10 - y20) / 15, -1.10e-6, rel=0.01)
      and near(y20 - B5, -9.84e-7, rel=0.005))
# the estimate has the right sign and size for other methods and problems too
okq = True
for meth, p in ((euler, 1), (rk4, 4)):
    for lam in (-1.0, 0.7):
        f = lambda t, y, lam=lam: lam * y + np.sin(t)
        exact = solve_ivp(f, [0, 2], [1.0], rtol=1e-13, atol=1e-15, method="DOP853").y[0, -1]
        yh, yh2 = meth(f, 0, [1.0], 2 / 40, 40)[0], meth(f, 0, [1.0], 2 / 80, 80)[0]
        okq &= near((yh - yh2) / (2 ** p - 1), yh2 - exact, rel=0.25)
check("l11.s3 (y_h - y_h/2)/(2^p - 1) estimates the error of y_h/2 (4 cases)", okq)


def adaptive(f, t0, y0, T, tol, h=0.1):
    t, y = t0, np.array(y0, float)
    acc, rej, steps = 0, 0, []
    while t < T - 1e-15:
        h = min(h, T - t)
        big = rk4(f, t, y, h, 1)
        half = rk4(f, t + h / 2, rk4(f, t, y, h / 2, 1), h / 2, 1)
        err = float(np.max(np.abs(half - big))) / 15
        scale = tol * max(1.0, float(np.max(np.abs(half))))
        if err <= scale:
            t += h; y = half + (half - big) / 15; acc += 1; steps.append(h)
        else:
            rej += 1
        h = h * (5.0 if err == 0 else min(5.0, max(0.2, 0.9 * (scale / err) ** 0.2)))
    return y, acc, rej, steps


ya, acc, rej, steps = adaptive(lambda t, y: y * y, 0.0, [1.0], 0.95, 1e-8)
check("l11.s4 controller on y' = y^2", acc == 38 and rej == 1 and (acc + rej) * 12 == 468 and near(steps[0], 0.070, ab=0.001)
      and near(min(steps[:-1]), 0.0043, ab=1e-4) and near(steps[-1], 0.0021, ab=1e-4) and near(abs(ya[0] - 20) / 20, 2.4e-8, rel=0.05),
      f"acc={acc} rej={rej} first={steps[0]:.4f} min={min(steps[:-1]):.4f} last={steps[-1]:.4f} rel={abs(ya[0] - 20) / 20:.2e}")
E11 = load("l11-step-size", "screens", 7)
out = E11["adaptive_rk4"](lambda t, y: y * y, 0.0, [1.0], 0.95, 1e-8)
check("l11.s7 solution agrees", out[1] == 38 and near(float(out[0][0]), float(ya[0]), ab=1e-12))
fx = abs(rk4(lambda t, y: y * y, 0, [1.0], 0.95 / 400, 400)[0] - 20) / 20
check("l11.s4 fixed-step RK4 with 400 steps", near(fx, 7e-8, rel=0.1), f"{fx:.2e}")
check("l11.s5/h3 controller arithmetic", near(0.9 * 0.01 * (1e-8 / 3.2e-7) ** 0.2, 0.0045, ab=1e-9) and near(0.9 * 0.01 * (1e-8 / 3.2e-7) ** 0.25, 0.0038, ab=5e-5))
check("l11.s7 Euler steps for 1e-3", math.ceil(5 / (1e-3 / (eu[10] / 0.5))) == 494 and near(eu[10] / 0.001 * 10, 493, ab=2))
# attack: adaptive solver on other problems, global error within 100 tol
oka = True
for f, T, y0_ in ((lambda t, y: -3 * y + np.cos(5 * t), 4.0, [1.0]), (lambda t, y: np.array([y[1], -y[0]]), 10.0, [1.0, 0.0]),
                  (lambda t, y: y * (1 - y), 6.0, [0.01])):
    exact = solve_ivp(f, [0, T], y0_, rtol=1e-13, atol=1e-15, method="DOP853").y[:, -1]
    got = E11["adaptive_rk4"](f, 0.0, y0_, T, 1e-9)[0]
    oka &= float(np.max(np.abs(got - exact))) < 1e-7
check("l11.s7 attack: adaptive_rk4 on three other problems", oka)
# quiz 1: the error floor of RK4 on the CIR system
fl = [abs(rk4(cir, 0, [0, 0], 5 / n, n)[0] - B5) for n in (320, 640, 1280, 2560, 5120, 10240)]
check("l11.q1 RK4 error stops falling by 16 near 1e-14", fl[1] / fl[2] > 10 and min(fl[3:]) < 3e-14 and fl[4] / fl[5] < 8, str([f"{v:.1e}" for v in fl]))
check("r3 arithmetic", near(3.2e-6 / 16, 2e-7, rel=1e-9) and math.ceil(1 / (1e-9 / 1e-3) ** 0.25) == 32)

# ---------------------------------------------------------------- l12 stiff equations
a_, b_ = 2 * 50 / 49.5, 3 - 4 - 2 * 50 / 49.5
rex = lambda t: 4 + a_ * math.exp(-0.5 * t) + b_ * math.exp(-50 * t)
Am = np.array([[-0.5, 0.0], [50.0, -50.0]])
cv = np.array([2.0, 0.0])                   # per cent units: m' = 0.5(4 - m)
y0 = np.array([6.0, 3.0])
ref = solve_ivp(lambda t, y: Am @ y + cv, [0, 1], y0, rtol=1e-12, atol=1e-14, method="Radau").y[1, -1]
check("l12.s0 exact solution", near(a_, 2.0202020, ab=1e-6) and near(b_, -3.0202020, ab=1e-6) and near(rex(1), 5.2253, ab=5e-5) and near(ref, rex(1), ab=1e-8))


def lin_euler(h, n):
    y = y0.copy()
    for _ in range(n):
        y = y + h * (Am @ y + cv)
    return y[1]


check("l12.s0/s5 Euler at four steps", near(lin_euler(0.04, 25), 8.2393, ab=5e-4) and near(lin_euler(0.05, 20), -10038, rel=0.001)
      and near(lin_euler(0.02, 50), 5.2222, ab=5e-5) and abs(lin_euler(0.01, 100) - rex(1)) < 0.01,
      f"{lin_euler(0.04, 25):.4f} {lin_euler(0.05, 20):.1f} {lin_euler(0.02, 50):.4f} {lin_euler(0.01, 100):.4f}")
check("l12.s1 eigenvalues and Euler limits", np.allclose(sorted(np.linalg.eigvals(Am)), [-50, -0.5]) and near(2 / 50, 0.04, ab=1e-15) and near(2 / 0.5, 4, ab=1e-15))
# Euler's stability boundary found by experiment: bisect on h for bounded against growing
grow = lambda h: not abs(lin_euler(h, 4000)) < 1e6      # inf and nan count as growth
lo, hi = 0.03, 0.05
for _ in range(40):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if grow(mid) else (mid, hi)
check("l12.s1 Euler blows up above h = 0.04 (experiment, 4,000 steps)", near(lo, 0.04, ab=1e-4), f"{lo:.6f}")


def implicit(h, n, path=False):
    y = y0.copy(); out = []
    M = np.eye(2) - h * Am
    for _ in range(n):
        y = np.linalg.solve(M, y + h * cv); out.append(y[1])
    return out if path else y[1]


def trapz(h, n, path=False):
    y = y0.copy(); out = []
    L, R = np.eye(2) - h / 2 * Am, np.eye(2) + h / 2 * Am
    for _ in range(n):
        y = np.linalg.solve(L, R @ y + h * cv); out.append(y[1])
    return out if path else y[1]


check("l12.s2 implicit Euler path", np.allclose(implicit(0.25, 4, True), [5.5720, 5.5796, 5.4176, 5.2611], atol=5e-5) and near(1 / 13.5, 0.0741, ab=5e-5))
check("l12.s4 trapezoidal path and factor", np.allclose(trapz(0.25, 4, True), [7.9696, 3.9891, 6.5346, 4.3941], atol=5e-5)
      and np.allclose([rex(t) for t in (0.25, 0.5, 0.75, 1)], [5.7828, 5.5733, 5.3885, 5.2253], atol=5e-5) and near((1 - 6.25) / (1 + 6.25), -0.7241, ab=5e-5)
      and near(math.exp(-12.5), 4e-6, rel=0.1))
check("l12.s6 trapezoidal at h=0.05", near(trapz(0.05, 20), 5.22528, ab=5e-6) and near(rex(1), 5.22531, ab=5e-6))
# orders by experiment on this system, at steps where the fast mode is resolved
ie = [abs(implicit(1 / n, n) - rex(1)) for n in (400, 800, 1600)]
tr = [abs(trapz(1 / n, n) - rex(1)) for n in (400, 800, 1600)]
check("l12 implicit Euler is first order, the trapezoidal rule second", near(ie[0] / ie[1], 2, rel=0.05) and near(tr[0] / tr[1], 4, rel=0.05))
R = {"eu": lambda z: 1 + z, "ie": lambda z: 1 / (1 - z), "tr": lambda z: (1 + z / 2) / (1 - z / 2),
     "rk": lambda z: 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24}
check("l12.s3 factors at z = -2.5", near(abs(R["eu"](-2.5)), 1.5, ab=1e-12) and near(abs(R["ie"](-2.5)), 0.286, ab=5e-4) and near(abs(R["tr"](-2.5)), 0.111, ab=5e-4)
      and near(abs(R["rk"](-2.5)), 0.648, ab=5e-4))
from scipy.optimize import brentq
check("l12.s3 RK4 real stability limit", near(brentq(lambda z: abs(R["rk"](z)) - 1, -3.5, -1), -2.7853, ab=5e-5) and near(2.7853 / 50, 0.0557, ab=5e-5))
zl = -np.abs(rng.normal(size=20000)) * 10 ** rng.uniform(-3, 4, 20000) + 1j * rng.normal(size=20000) * 10 ** rng.uniform(-3, 4, 20000)
check("l12.s3 implicit Euler and trapezoidal: |R| < 1 on 20,000 points of the left half-plane", bool(np.all(np.abs(R["ie"](zl)) < 1) and np.all(np.abs(R["tr"](zl)) < 1)))
check("l12.s3 explicit regions are bounded; trapezoidal factor tends to -1, implicit Euler's to 0",
      abs(R["eu"](-1e3)) > 1 and abs(R["rk"](-1e3)) > 1 and abs(R["rk"](1e3j)) > 1 and near(R["tr"](-1e9), -1, ab=1e-8) and abs(R["ie"](-1e9)) < 1e-8)
# l12 screens[4].explain defines L-stable as "a method whose factor tends to 0 for stiff modes".
# Hairer and Wanner IV.3 Def. 3.7: L-stable = A-stable AND R(z) -> 0. The (0,3) Pade method has R -> 0 and is not A-stable.
pade03 = lambda z: 1 / (1 - z + z ** 2 / 2 - z ** 3 / 6)
zz = -10 ** rng.uniform(-3, 1, 200000) + 1j * rng.uniform(-6, 6, 200000)
unst = int(np.sum(np.abs(pade03(zz)) > 1))
# (corrected claim, fix pass) l12 screens[4] and quiz[1] now define L-stable as A-stable plus a factor tending to 0.
# Own computation: on the imaginary axis |1 - iy - y^2/2 + iy^3/6|^2 = (1 - y^2/2)^2 + (y^3/6 - y)^2 = 8/9 at y = sqrt 2,
# so the (0,3) Pade factor has |R| = 3/(2 sqrt 2) > 1 there although R -> 0: the A-stable half is needed. Implicit Euler has
# |1 - z| >= 1 on Re z <= 0 (A-stable) and R -> 0, so it is L-stable.
_l12 = json.load(open(os.path.join(COURSE, "l12-stiff-equations.json")))
_x4, _q1 = _l12["screens"][4]["explain"]["text"], _l12["quiz"][1]["explain"]["text"]
check("l12.s4 L-stable = A-stable and factor -> 0; the Pade (0,3) factor tends to 0 but is not A-stable (corrected claim, fix pass)",
      abs(pade03(-1e9)) < 1e-8 and unst > 0 and near(abs(pade03(1j * math.sqrt(2))), 3 / (2 * math.sqrt(2)), ab=1e-12)
      and bool(np.all(np.abs(1 / (1 - zl)) <= 1)) and "**A-stable**" in _x4 and "**L-stable**" in _x4 and "A-stable" in _q1,
      f"|R(i sqrt 2)| = {abs(pade03(1j * math.sqrt(2))):.4f}; |R| > 1 at {unst} of 200,000 points with Re z < 0")
# implicit expression drawn for the RK4 region against |R(z)|^2 - 1
xx, yy = rng.uniform(-4, 2, 2000), rng.uniform(-4, 4, 2000)
drawn = (1 + xx + xx ** 2 / 2 - yy ** 2 / 2 + xx ** 3 / 6 - xx * yy ** 2 / 2 + xx ** 4 / 24 - xx ** 2 * yy ** 2 / 4 + yy ** 4 / 24) ** 2 + \
        (yy + xx * yy + xx ** 2 * yy / 2 - yy ** 3 / 6 + xx ** 3 * yy / 6 - xx * yy ** 3 / 6) ** 2 - 1
check("l12.s3 drawn RK4 curve is |R(z)| = 1", np.allclose(drawn, np.abs(R["rk"](xx + 1j * yy)) ** 2 - 1, atol=1e-9))
check("l12 quizzes and review", near(2 / 200, 0.01, ab=1e-15) and near(1 / 11, 0.0909, ab=5e-5) and near((1 - 20) / (1 + 20), -0.905, ab=5e-4)
      and near(1 / 41, 0.024, ab=5e-4) and near(2 / 100, 0.02, ab=1e-15) and near(1.5 ** 20, 3300, rel=0.01))
# solve_ivp on [0, 10]: cost ordering and accuracy (counts depend on the SciPy version; the lesson quotes 1.14.1)
E12 = load("l12-stiff-equations", "screens", 7)
res = E12["compare_solvers"]()
r10 = 0.04 + (0.02 * 50 / 49.5) * math.exp(-5) + (0.03 - 0.04 - 0.02 * 50 / 49.5) * math.exp(-500)
check("l12.s7 RK45 costs more than twice BDF, Radau in between, all within 1e-6", res["RK45"][0] > 2 * res["BDF"][0] and res["RK45"][0] > res["Radau"][0] > res["BDF"][0]
      and max(abs(v[1] - r10) for v in res.values()) < 1e-6, str({k: v[0] for k, v in res.items()}))
# Black-Scholes on a grid: the fastest decay rate scales like sigma^2 Smax^2 / dS^2


def fastest(nS, Smax=200.0, sig=0.2, r=0.05):
    dS = Smax / nS
    S = np.arange(1, nS) * dS
    a = 0.5 * sig ** 2 * S ** 2 / dS ** 2
    b = r * S / (2 * dS)
    L = np.diag(-2 * a - r) + np.diag((a + b)[:-1], 1) + np.diag((a - b)[1:], -1)
    return float(np.max(np.abs(np.linalg.eigvals(L))))


f1, f2, f3 = fastest(50), fastest(100), fastest(200)
check("l12.s8 halving dS multiplies the fastest rate by about 4", near(f2 / f1, 4, rel=0.08) and near(f3 / f2, 4, rel=0.06)
      and 0.5 < f2 / (0.2 ** 2 * 200 ** 2 / 2.0 ** 2) < 2.5, f"{f1:.0f} {f2:.0f} {f3:.0f}")

# (corrected claim, fix pass) l10 quiz[2] now asks what multiple of the true integral is computed, so only the key 0.5 is
# right and 2 stays a wrong value. Key twice: (a) the weights sum to 2 and [0, 4] has length 4, so 2 / 4 = 0.5; (b) the
# rule mapped to [0, 4] without (b - a) / 2, run on x^2 and e^x, returns 0.5 times the true integral.
_q2 = json.load(open(os.path.join(COURSE, "l10-gaussian-quadrature.json")))["quiz"][2]
_xg, _wg = np.polynomial.legendre.leggauss(6)
_tg = 2 * _xg + 2
_ratio = [float(np.sum(_wg * fn(_tg)) / tv) for fn, tv in ((lambda v: v ** 2, 64 / 3), (np.exp, math.e ** 4 - 1))]
check("l10.q2 the computed integral is 0.5 times the true one, and the stem asks for that multiple (corrected claim, fix pass)",
      near(float(np.sum(_wg)) / 4, 0.5, ab=1e-15) and all(near(x, 0.5, ab=1e-6) for x in _ratio)
      and _q2["widget"]["answer"] == 0.5 and [w_["value"] for w_ in _q2["widget"]["wrong"]] == [2]
      and _q2["question"] == "The computed integral is what multiple of the true one?",
      f"weights / length = {float(np.sum(_wg)) / 4}; ratios {_ratio}")

print(f"\n{N} checks, {len(FAILS)} failed, {len(XFAILS)} expected fails")
for f in FAILS:
    print("  FAILED:", f)
for f in XFAILS:
    print("  EXPECTED_FAIL:", f)
sys.exit(1 if FAILS else 0)
