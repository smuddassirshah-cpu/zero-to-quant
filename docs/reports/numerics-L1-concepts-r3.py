#!/usr/bin/env python3
"""Round-3 blind concept audit, numerics level 1 (l1 to l4, review-1, homework-1).

Independent experiments for every empirical or code-behaviour claim in the level.
Exit 0 when the content is right. A check that fails because the content is wrong
is registered with expected_fail=True: it prints EXPECTED_FAIL, leaves the exit
code alone, and carries the corrected assert in a comment beside it.
Run: python3 docs/reports/numerics-L1-concepts-r3.py
"""
import math, struct, sys, warnings
from fractions import Fraction
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

warnings.simplefilter("ignore")
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


def bs(S, K, r, sig, T, kind="c"):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    c = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return c if kind == "c" else c - S + K * math.exp(-r * T)


def vega(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    return S * math.sqrt(T) * norm.pdf(d1)


# ---------------------------------------------------------------- l1 floating point
eps, halv = 1.0, 0
while 1.0 + eps / 2 > 1.0:
    eps /= 2
    halv += 1
check("l1.s0 halvings", halv == 52 and eps == 2.0 ** -52)
check("l1.s0 tie rounds to even", 1.0 + 2.0 ** -53 == 1.0 and 1.0 + 2.0 ** -52 > 1.0)
toy = sorted((1 + m / 8) * 2.0 ** p for p in range(-1, 3) for m in range(8))
check("l1.s1 toy format", len(toy) == 32 and toy[0] == 0.5 and toy[-1] == 7.5
      and toy[toy.index(4.0) + 1] == 4.5 and toy[1] - toy[0] == 1 / 16 and toy[9] - toy[8] == 1 / 8)


def fields(x):
    b = int.from_bytes(struct.pack(">d", x), "big")
    return b >> 63, (b >> 52) & 0x7FF, b & (2 ** 52 - 1)


s, e, m = fields(-6.5)
check("l1.s2-3 fields of -6.5", (s, e, m / 2 ** 52) == (1, 1025, 0.625) and hex(m) == "0xa000000000000")
s, e, m = fields(100.25)
check("l1.s4 fields of 100.25", (s, e, m / 2 ** 52) == (0, 1029, 0.56640625) and format(e, "011b") == "10000000101")
check("l1.s5 spacing", near(np.spacing(100.0), 1.42e-14, rel=0.005) and near(np.spacing(1e6), 1.16e-10, rel=0.005))
check("l1.s5 gap formula 2^(k-52)", all(np.spacing(2.0 ** k * 1.3) == 2.0 ** (k - 52) for k in range(-300, 300, 7)))
check("l1.s5 2^53", float(2 ** 53) + 1 == float(2 ** 53) and float(2 ** 52) + 1 != float(2 ** 52)
      and 2 ** 53 == 9007199254740992)
check("l1.s6 limits", near(np.finfo(float).tiny, 2.225074e-308, rel=1e-6) and near(np.finfo(float).max, 1.797693e308, rel=1e-6)
      and 5e-324 == 2.0 ** -1074 and 5e-324 / 2 == 0.0 and near(math.exp(709), 8.218407e307, rel=1e-6))
try:
    math.exp(710)
    raised = False
except OverflowError:
    raised = True
with warnings.catch_warnings(record=True) as wlist:
    warnings.simplefilter("always")
    v710 = np.exp(710.0)
check("l1.s6/q1 exp(710)", raised and np.isinf(v710) and any(issubclass(w.category, RuntimeWarning) for w in wlist))
check("l1.s6 eps/tiny ratio ~1e292", near(math.log10(2.0 ** -52 / np.finfo(float).tiny), 292, ab=0.1))
# rounding model: 100,000 random decimal strings, exact relative error against u = 2^-53
rng = np.random.default_rng(11)
worst = Fraction(0)
for _ in range(100000):
    txt = f"{rng.uniform(1, 10):.17f}e{int(rng.integers(-300, 300))}"
    ex = Fraction(txt)
    worst = max(worst, abs(Fraction(float(txt)) - ex) / ex)
check("l1.s7 fl(x)=x(1+d), |d|<=u (100k decimals)", worst <= Fraction(1, 2 ** 53), f"worst/u={float(worst * 2 ** 53):.4f}")
p = Fraction(float("101.37")) - Fraction("101.37")
check("l1.s7 101.37 is rounded and inside u", p != 0 and abs(p) / Fraction("101.37") <= Fraction(1, 2 ** 53))
check("l1.s8 decode(1e6), decode(0.1)", fields(1e6)[1] - 1023 == 19 and fields(1e6)[2] / 2 ** 52 == 0.9073486328125
      and fields(0.1)[1] - 1023 == -4 and fields(0.1)[2] / 2 ** 52 == 0.6000000000000001)
# l1 screens[8]: the lesson's own decode, run on doubles that are not normal
import json as _json, os as _os
_w = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "numerics",
                                   "l1-floating-point.json")))["screens"][8]["widget"]
_env = {}
exec(_w["solution"], _env)
rebuild = lambda x: (lambda sg, pw, fr: (-1) ** sg * (1 + fr) * 2.0 ** pw)(*_env["decode"](x))
check("l1.s8 decode rebuilds normal doubles", all(rebuild(x) == x for x in (-6.5, 100.25, 0.1, 1e6, 1e-300, 1.7e308, 2.2250738585072014e-308)))
# Docstring says "of the double x". Corrected assert, which passes: the identity holds for every NORMAL double (line above).
check("l1.s8 decode rebuilds every double (0.0 and the subnormal 5e-324)", rebuild(0.0) == 0.0 and rebuild(5e-324) == 5e-324,
      f"decode(0.0) = {_env['decode'](0.0)} reads as {rebuild(0.0):.3e}; decode(5e-324) = {_env['decode'](5e-324)} reads as {rebuild(5e-324):.3e}",
      expected_fail=True)
check("l1.s9 gap at 1.7e18 is 256", np.spacing(1.7e18) == 256.0 and 2.0 ** 60 < 1.7e18 < 2.0 ** 61
      and near(math.log10(1.7e18), 18.2304, ab=1e-4))
g32 = float(np.spacing(np.float32(20000)))
st = float(np.float32(20000.01))
check("l1.q0 float32 near 20000", g32 == 2.0 ** -9 and st == 20000.009765625 and near(abs(st - 20000.01), 0.00023, ab=1e-5)
      and near(1 - 0.009765625 / 0.01, 0.023, ab=0.001) and near(2.0 ** -23 * 20000, 0.00238, ab=1e-5)
      and near(2.0 ** (14 - 52), 3.6e-12, rel=0.02))
err01 = Fraction(0.1) - Fraction(1, 10)
check("l1.q3 error of 0.1", near(float(err01), 5.55e-18, rel=0.002) and near(float(err01 * 10), 5.55e-17, rel=0.002))
check("r1 exponent of 0.01", fields(0.01)[1] == 1016 and near(0.01 / 2.0 ** -7, 1.28, ab=1e-12))
check("r1 float32 near 1e6", float(np.spacing(np.float32(1e6))) == 0.0625 and np.float32(1e6) + np.float32(0.01) == np.float32(1e6))
check("h1 hex word", struct.unpack(">d", bytes.fromhex("4024000000000000"))[0] == 10.0)
check("h1 float32 integers", np.float32(2 ** 24) + np.float32(1) == np.float32(2 ** 24)
      and all(float(np.float32(k)) == k for k in range(2 ** 24 - 2000, 2 ** 24 + 1)))

# ---------------------------------------------------------------- l2 cancellation
b = 1e8
tb = (b - math.sqrt(b * b - 4)) / 2
check("l2.s0 textbook root", near(tb, 7.450581e-9, rel=1e-6) and near(1 - tb / 1e-8, 0.255, ab=0.001))
pts = [-14.371, -12.913, -10.686, -8.952, -6.471, -5.118, -2.458, -0.594]
got = []
for k in range(1, 9):
    bb = 10.0 ** k
    d = math.sqrt(bb * bb - 4)
    got.append(math.log10(max(abs((bb - d) / 2 - 2 / (bb + d)) / (2 / (bb + d)), 1e-17)))
check("l2.s1 chart points", all(abs(a - c) < 0.01 for a, c in zip(got, pts)), str([round(x, 3) for x in got]))
check("l2.s1 slope about 2", near((got[-1] - got[0]) / 7, 2, ab=0.1))
check("l2.s2 half gap at 1e8", near(np.spacing(1e8) / 2, 7.5e-9, rel=0.01))
check("l2.s2 stable root", near(2 / (b + math.sqrt(b * b - 4)), 1e-8, rel=1e-15))
a1, a2 = math.exp(1e-10) - 1, math.expm1(1e-10)
check("l2.s3 expm1", near(a1, 1.000000082740371e-10, rel=1e-15) and near(a2, 1.00000000005e-10, rel=1e-12)
      and near((a1 - a2) / a2 * 1e8, 8.27, ab=0.01))


def onepass(xs):
    n = len(xs)
    return (sum(x * x for x in xs) - sum(xs) ** 2 / n) / (n - 1)


check("l2.s4 one-pass variance", onepass([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]) == 0.0
      and near(onepass([1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16]), 29.33, ab=0.01)
      and np.var([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16], ddof=1) == 30.0 and np.spacing(1e18) == 128.0)
fd = [math.log10(abs((math.exp(1 + 10.0 ** -k) - math.e) / 10.0 ** -k - math.e)) for k in range(1, 16)]
dots = [-0.852, -1.865, -2.867, -3.867, -4.867, -5.867, -6.854, -8.18, -6.667, -5.81, -4.486, -3.364, -3.341, -2.03, -0.409]
check("l2.s5 forward-difference dots", all(abs(a - c) < 0.01 for a, c in zip(fd, dots)), str([round(x, 3) for x in fd]))
check("l2.s5 best dot", fd.index(min(fd)) == 7 and near(10 ** fd[7], 6.6e-9, rel=0.02) and near(10 ** fd[14], 0.39, ab=0.005)
      and near(10 ** fd[0], 0.14, ab=0.005))
V0 = bs(100, 100, 0.05, 0.2, 1)
check("l2.s6 prices", near(V0, 10.450583572185565, ab=1e-12) and near(bs(101, 100, .05, .2, 1), 11.096708127437402, ab=1e-11)
      and near(bs(100.01, 100, .05, .2, 1), 10.456952816712182, ab=1e-11))
delta = norm.cdf((0.05 + 0.02) / 0.2)
check("l2.s6 delta", near(delta, 0.636831, ab=5e-7))
d1 = (bs(101, 100, .05, .2, 1) - V0) / 1
d2 = (bs(100.01, 100, .05, .2, 1) - V0) / 0.01
d3 = (10.450583572186197 - 10.450583572185565) / 1e-12
check("l2.s6 forward-bump errors", near(d1 - delta, 9.3e-3, rel=0.02) and near(d2 - delta, 9.4e-5, rel=0.02)
      and near(abs(d3 - delta), 4.4e-3, rel=0.05) and near(d1, 0.6461, ab=1e-4) and near(d3, 0.6324, ab=3e-4),
      f"{d1 - delta:.3e} {d2 - delta:.3e} {d3 - delta:.3e}")
gam = norm.pdf(0.35) / (100 * 0.2)
check("l2.s6/s9 gamma and model bump", near(gam, 0.0187620, ab=5e-8)
      and near(2 * math.sqrt(2.0 ** -52 * V0 / gam), 7e-7, rel=0.02))
check("l2.s7 h* and central h", near(2 * math.sqrt(2.0 ** -52), 2.98e-8, rel=0.002) and near((2.0 ** -52) ** (1 / 3), 6e-6, rel=0.02))
gt = {1: 0.01875972, 0.01: 0.01876202, 0.0001: 0.01876188, 0.000001: 0.02842171}
gg = {h: (bs(100 + h, 100, .05, .2, 1) - 2 * V0 + bs(100 - h, 100, .05, .2, 1)) / h ** 2 for h in gt}
check("l2.s9 gamma table (large bumps exact, tiny bumps are rounding noise)",
      near(gg[1], gt[1], ab=5e-9) and near(gg[0.01], gt[0.01], ab=2e-8) and abs(gg[0.0001] - gam) < 1e-6
      and abs(gg[0.000001] - gam) > 1e-4, str({h: round(v, 8) for h, v in gg.items()}))
check("l2.s9 errors", near(abs(gt[1] - gam), 2.3e-6, rel=0.05) and near(abs(gt[0.0001] - gam), 1.4e-7, rel=0.3)
      and near(gt[0.000001] / gam - 1, 0.51, ab=0.01))
cd = (bs(100.01, 100, .05, .2, 1) - bs(99.99, 100, .05, .2, 1)) / 0.02
check("l2.s9 central delta at 0.01", abs(cd - delta) < 2e-8, f"{cd - delta:.2e}")
check("l2.q0 log1p", near(math.log(1 + 1e-12), 1.000089e-12, rel=1e-6) and near(math.log1p(1e-12), 9.999999999995e-13, rel=1e-13))
ok = True
for _ in range(200000):
    y = float(rng.uniform(-1e3, 1e3)) * 10.0 ** int(rng.integers(-20, 20))
    x = y * float(rng.uniform(0.5, 2.0))
    if y / 2 <= x <= 2 * y or 2 * y <= x <= y / 2:
        ok &= Fraction(x - y) == Fraction(x) - Fraction(y)
check("l2.q1 Sterbenz (200k pairs)", ok and 1.5 - 1.25 == 0.25)
check("l2.q2 float32 gap at 1e9", float(np.spacing(np.float32(1e9))) == 64.0)
check("l2.q3 central error at 1e-5", near(abs((math.exp(1 + 1e-5) - math.exp(1 - 1e-5)) / 2e-5 - math.e), 5.9e-11, rel=0.25))
check("r1 sqrt gap", near(1 / (math.sqrt(1e12 + 1) + 1e6), 5e-7, rel=1e-6))
check("r1 bump", near(2 * math.sqrt(2.22e-16 * 100), 2.98e-7, rel=0.002))
check("h1 gamma bump", near((48 * 2.22e-16) ** 0.25, 3.21e-4, rel=0.002))
# homework-1 Kahan / float32 pennies
tot = np.float32(0.0)
pen = np.float32(0.01)
for _ in range(10 ** 6):
    tot = tot + pen
check("h1 plain float32 loop gives 9865.22", near(float(tot), 9865.22, ab=0.01), f"{float(tot):.2f}")
total, c = 0.0, 0.0
for _ in range(10 ** 6):
    y = pen - c
    t = total + y
    c = (t - total) - y
    total = t
check("h1 Kahan float32 pennies", isinstance(total, np.float32) and abs(float(total) - 10000.0) < 0.005, f"{float(total):.4f}")
# homework-1 long form: 200 simulated years of a 1bn book
zeros = wild = 0
twopass = []
for _ in range(200):
    x = 1e9 + np.cumsum(rng.normal(0, 0.2, 250)) + rng.normal(0, 3.0, 250)
    v1 = float((np.mean(x * x) - np.mean(x) ** 2))
    zeros += v1 == 0.0
    wild += abs(v1) >= 64
    twopass.append(float(np.var(x)))
check("h1 one-pass on a 1bn book is 0 or hundreds off", zeros + wild >= 190 and zeros > 20, f"zeros={zeros} wild={wild}")
check("h1 kappa of the variance ~2 xbar/s", near(2 * 1e9 / 3.0, 6e8, rel=0.15))

# ---------------------------------------------------------------- l3 conditioning
A = np.array([[1, 1], [1, 1.0001]])
sv = np.linalg.svd(A, compute_uv=False)
check("l3.s3 singular values", near(sv[0], 2.00005, ab=5e-6) and near(sv[1], 4.999875e-5, rel=1e-6) and near(sv[0] / sv[1], 40002.00007, rel=1e-8))
bvec = np.array([2, 2.0001])
db = np.array([0, 0.0001])
dx = np.linalg.solve(A, bvec + db) - np.linalg.solve(A, bvec)
ratio = (np.linalg.norm(dx) / math.sqrt(2)) / (np.linalg.norm(db) / np.linalg.norm(bvec))
check("l3.s1 measured amplification", near(np.linalg.norm(db) / np.linalg.norm(bvec) * 1e5, 3.536, ab=0.001) and near(ratio, 28285, rel=0.002))
# worst change for this b: the supremum over directions is ||A^-1|| ||b|| / ||x||
sup_b = (1 / sv[1]) * np.linalg.norm(bvec) / math.sqrt(2)
check("l3.s3 worst db for this b reaches 40,002", near(sup_b, 40002, rel=2e-5), f"{sup_b:.2f}")
worst = 0
for _ in range(20000):
    bb = rng.normal(size=2)
    dd = rng.normal(size=2) * 1e-6
    xx = np.linalg.solve(A, bb)
    worst = max(worst, (np.linalg.norm(np.linalg.solve(A, dd)) / np.linalg.norm(xx)) / (np.linalg.norm(dd) / np.linalg.norm(bb)))
check("l3.s6 bound kappa never exceeded (20k random b, db)", worst <= sv[0] / sv[1] * (1 + 1e-9), f"max ratio {worst:.1f}")
check("l3.s2 kappas", near(1.0001 / 0.0001, 10001, rel=1e-9) and near(1 / math.log(1.0001), 10000, rel=1e-3))
H8 = np.array([[1 / (j + k + 1) for k in range(8)] for j in range(8)])
check("l3.s4 Hilbert 8", near(np.linalg.cond(H8), 1.53e10, rel=0.005) and near(math.log10(np.linalg.cond(H8)), 10.2, ab=0.05)
      and near(math.log10(40002), 4.6, ab=0.01))
for r_ in (0.3, 0.95, 0.99):
    C = np.array([[1, r_], [r_, 1]])
    check(f"l3 corr-matrix kappa r={r_}", near(np.linalg.cond(C), (1 + r_) / (1 - r_), rel=1e-9))
check("l3.q0", near(1.95 / 0.05, 39, rel=1e-12) and near(1 / (1 - 0.95 ** 2), 10.26, ab=0.01) and near(math.log10(39), 1.6, ab=0.01))
res = bvec - A @ np.array([0, 2.0])
check("l3.s5 residual of (0,2)", np.allclose(res, [0, -0.0001], atol=1e-12))
check("l3.s9 call vega", near(vega(100, 100, .05, .2, 1), 37.52, ab=0.005) and near(0.01 / 37.52 * 100, 0.027, ab=5e-4))
p60 = bs(100, 60, .05, .2, 1, "p")
v60 = vega(100, 60, .05, .2, 1)
check("l3.s9 60 put", near(p60, 0.0113, ab=5e-5) and near(v60, 0.588, ab=5e-4) and near(0.01 / 0.588 * 100, 1.70, ab=0.005)
      and near(0.01 / p60, 0.89, ab=0.01), f"p={p60:.5f} vega={v60:.4f}")
iv = lambda price: brentq(lambda s_: bs(100, 60, .05, s_, 1, "p") - price, 1e-4, 5)
up, dn = (iv(p60 + 0.01) - 0.2) * 100, (0.2 - iv(p60 - 0.01)) * 100
check("l3.s9 true moves 1.3 up, 3.3 down", near(up, 1.3, ab=0.06) and near(dn, 3.3, ab=0.06), f"{up:.2f} {dn:.2f}")
check("l3.q3", near(0.05 / 37.52 * 100, 0.133, ab=5e-4) and near((iv(p60 + 0.05) - 0.2) * 100, 4.1, ab=0.06) and p60 - 0.05 < 0)

# ---------------------------------------------------------------- l4 stability
s_, t_ = 0.0, 1.0
for k in range(1, 120):
    s_ += t_
    t_ *= -20 / k
check("l4.s0 alternating series", near(s_, 6.147561828914626e-09, rel=1e-12) and near(math.exp(-20), 2.061153622438558e-09, rel=1e-15)
      and near(s_ / math.exp(-20) - 1, 1.983, ab=0.001), repr(s_))
s2, t2 = 0.0, 1.0
for k in range(1, 120):
    s2 += t2
    t2 *= 20 / k
check("l4.s2 reciprocal of the positive series", near(1 / s2, 2.061153622438557e-09, rel=1e-15), repr(1 / s2))
big = 20.0 ** 20 / math.factorial(20)
check("l4.s1 largest term", near(big, 4.31e7, rel=0.002) and near(math.log10(big) - math.log10(math.exp(-20)), 16.3, ab=0.05))
# reverse order of the alternating series does not rescue it
terms = [(-20.0) ** k / math.factorial(k) for k in range(120)]
rev = sum(sorted(terms, key=abs))
check("l4.s2 smallest-first still loses the answer", abs(rev / math.exp(-20) - 1) > 0.05, f"rel err {rev / math.exp(-20) - 1:.2f}")
e8 = 1e-8
L = np.array([[1, 1], [e8, 0], [0, e8]])
N_ = L.T @ L
check("l4.s3 Lauchli normal matrix is stored singular", N_[0, 0] == 1.0 and np.linalg.det(N_) == 0.0)
x_ls = np.linalg.lstsq(L, np.array([2, e8, e8]), rcond=None)[0]
Q, R = np.linalg.qr(L)
x_qr = np.linalg.solve(R, Q.T @ np.array([2, e8, e8]))
check("l4.s3 QR and lstsq return (1,1)", np.allclose(x_ls, 1, atol=1e-9) and np.allclose(x_qr, 1, atol=1e-9))
check("l4.s4 kappa(A)", near(np.linalg.cond(L), 1.41e8, rel=0.005) and near(math.log10(np.linalg.cond(L) ** 2), 16.3, ab=0.01)
      and near(2.0 ** 53, 9e15, rel=0.002))
# kappa(A^T A) = kappa(A)^2 and kappa(R) = kappa(A) on random tall matrices
okk = True
for _ in range(200):
    M = rng.normal(size=(8, 4)) @ np.diag(10.0 ** rng.uniform(-2, 2, 4))
    okk &= near(np.linalg.cond(M.T @ M), np.linalg.cond(M) ** 2, rel=1e-6)
    okk &= near(np.linalg.cond(np.linalg.qr(M)[1]), np.linalg.cond(M), rel=1e-9)
check("l4.s5 kappa(AtA)=kappa^2, kappa(R)=kappa (200 matrices)", okk)
tt = np.linspace(0, 1, 100)
A15 = np.vander(tt, 15, increasing=True)
b15 = np.exp(np.sin(4 * tt)) / 2006.787453080206
kA = np.linalg.cond(A15)
c_ls = np.linalg.lstsq(A15, b15, rcond=None)[0][-1]
Q, R = np.linalg.qr(A15)
c_qr = np.linalg.solve(R, Q.T @ b15)[-1]
try:
    c_ne = np.linalg.solve(A15.T @ A15, A15.T @ b15)[-1]
except np.linalg.LinAlgError:
    c_ne = float("nan")
check("l4.s6 Trefethen-Bau fit", near(kA, 2.27e10, rel=0.01) and abs(c_ls - 1) < 2.5e-6 and abs(c_qr - 1) < 2.5e-6
      and not abs(c_ne - 1) < 0.1, f"kappa={kA:.3e} lstsq={c_ls:.10f} qr={c_qr:.10f} normal={c_ne:.3f}")
check("l4.s6 stable bound kappa*u", near(kA * 2.0 ** -53, 2.5e-6, rel=0.03))
e7 = 1e-7
L7 = np.array([[1, 1], [e7, 0], [0, e7]])
x7 = np.linalg.solve(L7.T @ L7, L7.T @ np.array([2, e7, e7]))
check("l4.s8/q0 Lauchli at 1e-7", np.allclose(x7, 1, atol=1e-6) and near(np.linalg.cond(L7) ** 2 * 2.0 ** -53, 0.02, rel=0.15)
      and near(1e-14 / 2.0 ** -52, 45, ab=0.1), f"x={x7}, digits lost {16 + math.log10(max(abs(x7 - 1).max(), 1e-17)):.1f}")
ty = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30.0])
Ay = np.vander(ty, 4, increasing=True)
tc = (ty - ty.mean()) / ((ty.max() - ty.min()) / 2)
variants = [np.linalg.cond(np.vander((ty - ty.mean()) / ty.std(), 4, increasing=True)),
            np.linalg.cond(np.vander(tc, 4, increasing=True)),
            np.linalg.cond(np.vander((ty - ty.mean()) / ty.std(ddof=1), 4, increasing=True))]
check("l4.s9 cubic design", near(np.linalg.cond(Ay), 2.98e4, rel=0.005) and near(np.linalg.cond(Ay.T @ Ay), 8.88e8, rel=0.005)
      and any(near(v, 13.3, ab=0.1) for v in variants), str([round(v, 2) for v in variants]))
check("r1 discount series", near(30.0 ** 30 / math.factorial(30), 7.8e11, rel=0.01) and near(math.exp(-30), 9.4e-14, rel=0.01))
check("h1 normal digits", near(16 - math.log10(9e10), 5.0, ab=0.06) and near(16 - math.log10(3e5), 10.5, ab=0.03))

print(f"\n{N} checks, {len(FAILS)} failed, {len(XFAILS)} expected fails")
for f in FAILS:
    print("  FAILED:", f)
for f in XFAILS:
    print("  EXPECTED_FAIL:", f)
sys.exit(1 if FAILS else 0)
