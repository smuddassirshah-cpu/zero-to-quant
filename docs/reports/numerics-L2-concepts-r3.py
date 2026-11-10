#!/usr/bin/env python3
"""Round-3 blind concept audit, numerics level 2 (l5 to l8, review-2, homework-2).

Independent experiments, plus attacks on the lesson's own solutions (loaded from
the content JSON and run in CPython). Exit 0 when the content is right. A check
that fails because the content is wrong is registered with expected_fail=True:
it prints EXPECTED_FAIL, leaves the exit code alone, and carries the corrected
assert in a comment beside it.
Run: python3 docs/reports/numerics-L2-concepts-r3.py
"""
import json, math, os, sys, warnings
from fractions import Fraction
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline

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


class Budget(Exception):
    pass


def capped(f, limit):
    calls = [0]

    def g(x):
        calls[0] += 1
        if calls[0] > limit:
            raise Budget()
        return f(x)
    g.calls = calls
    return g


rng = np.random.default_rng(5)
R2 = math.sqrt(2)

# ---------------------------------------------------------------- l5 rates
x = 1.0
ne = []
for _ in range(4):
    x = x - (x * x - 2) / (2 * x)
    ne.append(abs(x - R2))
check("l5.s0 Newton errors", all(near(a, c, rel=0.005) for a, c in zip(ne, [0.0858, 0.00245, 2.12e-6, 1.59e-12])), str(ne))
x0, x1 = 1.0, 2.0
se = []
for _ in range(6):
    x0, x1 = x1, x1 - (x1 * x1 - 2) * (x1 - x0) / (x1 * x1 - x0 * x0)
    se.append(abs(x1 - R2))
check("l5.s0 secant errors", all(near(a, c, rel=0.005) for a, c in zip(se, [0.0809, 0.0142, 4.21e-4, 2.12e-6, 3.16e-10]))
      and se[4] > 1e-12 > se[5], str(se))
check("l5.s0 bisection needs 40 halvings for 1e-12", 2.0 ** -39 > 1e-12 > 2.0 ** -40)
p = lambda e0, e1, e2: math.log(e2 / e1) / math.log(e1 / e0)
check("l5.s2 Newton order", near(p(0.0858, 0.00245, 2.12e-6), 1.98, ab=0.01) and near(p(0.00245, 2.12e-6, 1.59e-12), 2.0, ab=0.01))
check("l5.s3 secant order", near(p(0.0142, 4.21e-4, 2.12e-6), 1.50, ab=0.01) and near(p(4.21e-4, 2.12e-6, 3.16e-10), 1.67, ab=0.01))
check("l5.s4 Newton constant", near(ne[3] / ne[2] ** 2, 0.3535, ab=0.002) and near(ne[1] / ne[0] ** 2, 0.3333, ab=1e-3)
      and near(ne[2] / ne[1] ** 2, 0.3529, ab=1e-3) and near(1 / (2 * R2), 0.353553, ab=1e-6))
# secant order phi on other simple roots, in 400-digit arithmetic so the limit is visible
import mpmath as mp
mp.mp.dps = 400
for nm, f, r in [("cos", mp.cos, mp.pi / 2), ("x^3-x-1", lambda v: v ** 3 - v - 1, mp.findroot(lambda v: v ** 3 - v - 1, 1.3))]:
    a, b_ = r + mp.mpf("0.4"), r + mp.mpf("0.3")
    es = []
    for _ in range(14):
        if f(b_) == f(a) or abs(b_ - r) < mp.mpf(10) ** -250:
            break
        a, b_ = b_, b_ - f(b_) * (b_ - a) / (f(b_) - f(a))
        es.append(abs(b_ - r))
    es = [v for v in es if v > mp.mpf(10) ** -300]
    ords = [float(mp.log(es[i + 2] / es[i + 1]) / mp.log(es[i + 1] / es[i])) for i in range(len(es) - 2)]
    # cos has f''(r) = 0, so its secant order is higher than phi; the lesson's "f' != 0" covers the generic case only
    check(f"l5 secant order on {nm}", near(ords[-1], 1.618, ab=0.03) if nm != "cos" else ords[-1] > 1.618, str([round(o, 3) for o in ords[-4:]]))
x = 2.0
de = []
for _ in range(12):
    x = x - (x - 1) ** 2 / (2 * (x - 1))
    de.append(abs(x - 1))
check("l5.s5 double root: Newton is linear with ratio 1/2", all(near(de[i + 1] / de[i], 0.5, ab=1e-9) for i in range(10)))
P = lambda y: sum(5 / (1 + y) ** t for t in range(1, 6)) + 100 / (1 + y) ** 5 - 95
dP = lambda y: sum(-5 * t / (1 + y) ** (t + 1) for t in range(1, 6)) - 500 / (1 + y) ** 6
ytm = brentq(P, 0, 0.2, xtol=1e-15)
y = 0.05
its = []
for _ in range(3):
    y -= P(y) / dP(y)
    its.append(y)
check("l5.s6 bond yield and Newton iterates", near(ytm, 0.06193228, ab=5e-9) and near(its[0], 0.0615487, ab=5e-8)
      and near(its[1], 0.06193188, ab=5e-9) and near(its[2], 0.061932283, ab=5e-10), f"{ytm:.10f} {its}")
check("l5.s6 digits after 3 Newton steps", 10 <= -math.log10(abs(its[2] - ytm) / ytm) <= 12.5, f"{abs(its[2] - ytm):.1e}")
check("l5.s6 31 halvings", 0.2 / 2 ** 30 > 1e-10 > 0.2 / 2 ** 31 and 1 / 2 ** 33 > 1e-10 > 1 / 2 ** 34)
check("l5.s7 efficiency indices", near(2 ** 0.5, 1.414, ab=5e-4) and near((1 + 5 ** 0.5) / 2, 1.618, ab=5e-4))
c_star = 1 / math.log2((1 + 5 ** 0.5) / 2) - 1
check("r2 Newton beats secant only if f' costs under 0.44 f", near(c_star, 0.44, ab=0.005) and near(2 ** (1 / 1.5), 1.587, ab=5e-4))
E5 = load("l5-bisection-and-newton", "screens", 8)
f2 = lambda v: v * v - 2
check("l5.s8 call counts 42 / 9 / 6", E5["bisect"](f2, 1, 2, 1e-12)[1] == 42 and E5["secant"](f2, 1.0, 2.0, 1e-12)[1] == 9
      and E5["newton"](f2, lambda v: 2 * v, 1.0, 1e-12)[1] == 6)
check("l5.s8 bisect error is within tol", abs(E5["bisect"](f2, 1, 2, 1e-12)[0] - R2) < 1e-12)
# attacks on bisect
okb = True
for _ in range(2000):
    r = float(rng.uniform(-3, 3))
    lo, hi = r - float(rng.uniform(0.01, 5)), r + float(rng.uniform(0.01, 5))
    sgn = 1 if rng.random() < 0.5 else -1
    f = lambda v, r=r, sgn=sgn: sgn * math.atan(v - r) ** 3
    okb &= abs(E5["bisect"](f, lo, hi, 1e-9)[0] - r) < 1e-9
check("l5.s8 attack: bisect on 2,000 random rising and falling f", okb)
check("l5.s8 attack: bisect returns an exact midpoint root", E5["bisect"](lambda v: v, -1.0, 1.0, 1e-9)[0] == 0.0
      or abs(E5["bisect"](lambda v: v, -1.0, 1.0, 1e-9)[0]) < 1e-9)
g = capped(f2, 5000)
try:
    rt17 = E5["bisect"](g, 1.0, 2.0, 1e-17)
    ends = True
except Budget:
    ends = False
# (corrected claim, fix pass) the solution now also stops at `mid == lo or mid == hi`. Own computation: the bracket stalls
# at the two adjacent doubles around sqrt 2, 2^-52 apart (52 halvings of [1, 2]), so 2 + 52 = 54 calls, root within one gap.
_lo, _hi, _n = 1.0, 2.0, 0
while (_lo + _hi) / 2 not in (_lo, _hi):
    _m = (_lo + _hi) / 2; _n += 1
    _lo, _hi = (_m, _hi) if _m * _m < 2 else (_lo, _m)
check("l5.s8 bisect ends for every positive tol (tol = 1e-17 on [1, 2], 5,000 calls allowed) (corrected claim, fix pass)",
      ends and rt17[1] == 2 + _n == 54 and _hi - _lo == 2.0 ** -52 and abs(rt17[0] - R2) <= 2.0 ** -52,
      f"{rt17[1] if ends else 'no end'} calls, {_n} halvings to a bracket of width {_hi - _lo:.1e}")
try:
    E5["newton"](f2, lambda v: 2 * v, 0.0, 1e-12)
    zde = False
except ZeroDivisionError:
    zde = True
check("l5.q2 Newton from 0 divides by zero", zde)
m = [abs(v - R2) for v in (1.5, 1.25, 1.375, 1.4375)]
check("l5.q0 midpoint errors", all(near(a, c, ab=5e-5 + 5e-4 * (c > 0.1)) for a, c in zip(m, [0.0858, 0.164, 0.0392, 0.0233])), str(m))
check("l5.s9 / quizzes halvings", 2 ** 19 < 1e6 < 2 ** 20 and 2 ** 29 < 1e9 < 2 ** 30)

# ---------------------------------------------------------------- l6 safeguarded Newton
S, r_, T = 100.0, 0.05, 1 / 12


def bs(K, sig, kind):
    sd = sig * math.sqrt(T)
    d1 = (math.log(S / K) + (r_ + sig * sig / 2) * T) / sd
    c = S * norm.cdf(d1) - K * math.exp(-r_ * T) * norm.cdf(d1 - sd)
    return c if kind == "c" else c - S + K * math.exp(-r_ * T)


def vg(K, sig):
    d1 = (math.log(S / K) + (r_ + sig * sig / 2) * T) / (sig * math.sqrt(T))
    return S * math.sqrt(T) * norm.pdf(d1)


Ks = list(range(75, 130, 5))
kinds = ["p"] * 5 + ["c"] * 6
Q = [0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003]
V02 = [0.0000, 0.0000, 0.0030, 0.0609, 0.5039, 2.5121, 0.7440, 0.1476, 0.0196, 0.0018, 0.0001]
VG02 = [0.000028, 0.004424, 0.164048, 1.802487, 7.058698, 11.457839, 8.731917, 3.465519, 0.781334, 0.107697, 0.009660]
check("l6.s0 table of V(0.2) and vega", all(near(bs(K, 0.2, k), v, ab=6e-5) for K, k, v in zip(Ks, kinds, V02))
      and all(near(vg(K, 0.2), v, ab=6e-7) for K, v in zip(Ks, VG02)))
first = [0.2 - (bs(K, 0.2, k) - q) / vg(K, 0.2) for K, k, q in zip(Ks, kinds, Q)]
check("l6.s0 first Newton steps", [v > 5 for v in first] == [True, True] + [False] * 9 and near(first[0] - 0.2, 2724, rel=0.01)
      and near(first[1], 18.14, ab=0.02) and near(first[2], 0.89, ab=0.01), str([round(v, 3) for v in first]))
s1 = first[1]
s2 = s1 - (bs(80, s1, "p") - Q[1]) / vg(80, s1)
check("l6.s0 the 80 put goes to 18.14, then -218", near(s2, -218, rel=0.01), f"{s2:.1f}")
conv = 0
for K, k, q in zip(Ks, kinds, Q):
    s = 0.2
    try:
        for _ in range(60):
            s = s - (bs(K, s, k) - q) / vg(K, s)
        conv += abs(bs(K, s, k) - q) < 1e-10
    except (ValueError, ZeroDivisionError, OverflowError):
        pass
check("l6.s0 plain Newton: nine of eleven converge", conv == 9, f"{conv}")
nx = lambda s: s - (bs(75, s, "p") - 0.0766) / vg(75, s)
check("l6.s1 Newton from 0.3 and 0.5", near(nx(0.3), 2.53, ab=0.02) and near(nx(0.5), 0.482, ab=0.001)
      and near(bs(75, 0.3, "p"), 0.0007, ab=5e-5) and near(vg(75, 0.3), 0.034, ab=5e-4))
ivs = [brentq(lambda s: bs(K, s, k) - q, 1e-4, 5, xtol=1e-14) for K, k, q in zip(Ks, kinds, Q)]
exp_iv = [0.4805643773, 0.3888224503, 0.3178175298, 0.2643331891, 0.2257805086, 0.2000028726, 0.1852458045, 0.1800550096,
          0.1832333240, 0.1938045067, 0.2123829659]
check("l6.s8 implied vols agree with brentq to 1e-10", all(near(a, c, ab=1e-10) for a, c in zip(ivs, exp_iv)))
E6 = load("l6-safe-root-finder", "screens", 8)
mine = E6["implied_vols"](Q, Ks, S, r_, T, kinds)
check("l6.s8 solution matches brentq to 1e-10", float(np.max(np.abs(mine - np.array(ivs)))) < 1e-10)
check("l6.s4 bisection count", 4.9999 / 2 ** 35 > 1e-10 > 4.9999 / 2 ** 36 and 4.9999 / 2 ** 28 > 1e-8 > 4.9999 / 2 ** 29)
check("l6.s5 wing rounding", near(vg(125, 0.2124), 0.0218, ab=1e-4) and near(0.00005 / 0.0218, 0.0023, ab=5e-5)
      and round(bs(125, 0.2103, "c"), 4) == 0.0003)
check("l6.s6 bounds", near(100 - 95 * math.exp(-r_ * T), 5.3950, ab=5e-5) and near(110 * math.exp(-r_ * T) - 100, 9.5426, ab=5e-5)
      and near(bs(95, 1e-4, "c"), 5.3950, ab=5e-5))
nanv = E6["implied_vols"]([5.0, 9.40], [95, 110], S, r_, T, ["c", "p"])
check("l6.s6/q3 quotes below the bound give NaN", bool(np.all(np.isnan(nanv))))
SN = load("l6-safe-root-finder", "screens", 7)["safe_newton"]
f9, d9 = (lambda v: (v - 1) ** 9), (lambda v: 9 * (v - 1) ** 8)
stop = SN(f9, d9, 0.0, 3.0)
check("l6.s7 (x-1)^9 stops near 1.046 at the default ftol", near(stop, 1.046, ab=0.004) and 0.046 ** 9 < 1e-12 < 0.047 ** 9,
      f"{stop:.4f}")
check("l6.s7 (x-1)^9 with ftol=0 reaches 1", abs(SN(f9, d9, 0.0, 3.0, ftol=0.0) - 1) < 1e-9)
# without the halving rule the same call does not finish in maxit steps


def no_halving(f, df, lo, hi, xtol=1e-10, maxit=100):
    flo = f(lo)
    x = 0.5 * (lo + hi)
    for _ in range(maxit):
        fx = f(x)
        if (fx > 0) == (flo > 0):
            lo, flo = x, fx
        else:
            hi = x
        d = df(x)
        new = x - fx / d if d != 0 else lo - 1.0
        if not (min(lo, hi) < new < max(lo, hi)):
            new = 0.5 * (lo + hi)
        if abs(new - x) < xtol:
            return new
        x = new
    raise RuntimeError("no convergence")


try:
    no_halving(f9, d9, 0.0, 3.0)
    needs = False
except RuntimeError:
    needs = True
check("l6.s7 the ninefold root needs the halving rule", needs)
cube = lambda v: v ** 3 - 2 * v + 2
dcube = lambda v: 3 * v * v - 2
check("l6.s7 Newton cycle 0 -> 1 -> 0, safeguard finds -1.769292", 0 - cube(0) / dcube(0) == 1.0 and 1 - cube(1) / dcube(1) == 0.0
      and near(SN(cube, dcube, -3.0, 0.0), -1.769292354238631, ab=1e-9))
# attacks on safe_newton: 3,000 random problems, rising and falling, flat spots, roots at ends
bad = 0
worst_calls = 0
for i in range(3000):
    r = float(rng.uniform(-2, 2))
    lo, hi = r - float(rng.uniform(1e-3, 6)), r + float(rng.uniform(1e-3, 6))
    sgn = 1 if rng.random() < 0.5 else -1
    kind = i % 4
    if kind == 0:
        f, df = (lambda v: sgn * (math.exp(v - r) - 1)), (lambda v: sgn * math.exp(v - r))
    elif kind == 1:
        f, df = (lambda v: sgn * math.atan(5 * (v - r))), (lambda v: sgn * 5 / (1 + 25 * (v - r) ** 2))
    elif kind == 2:
        f, df = (lambda v: sgn * ((v - r) ** 3 + 1e-3 * (v - r))), (lambda v: sgn * (3 * (v - r) ** 2 + 1e-3))
    else:
        f, df = (lambda v: sgn * math.tanh(40 * (v - r))), (lambda v: sgn * 40 / math.cosh(40 * (v - r)) ** 2)
    g = capped(f, 100000)
    try:
        out = SN(g, df, lo, hi, ftol=0.0)
        bad += abs(out - r) > 1e-8
        worst_calls = max(worst_calls, g.calls[0])
    except RuntimeError:
        bad += 1
check("l6.s7 attack: 3,000 random brackets, ftol=0", bad == 0, f"bad={bad}, most f calls {worst_calls}")
check("l6.s7 attack: root at either end, sign change missing", SN(lambda v: v, lambda v: 1.0, 0.0, 1.0) == 0.0
      and SN(lambda v: v - 1, lambda v: 1.0, 0.0, 1.0) == 1.0)
# attacks on implied_vols: wide range of strikes, maturities and vols (no halving rule, no error at maxit)
badv = tested = 0
for _ in range(400):
    Tm = float(rng.choice([1 / 52, 1 / 12, 0.5, 2.0]))
    sig = float(rng.uniform(0.05, 1.5))
    K = S * math.exp(float(rng.uniform(-2.5, 2.5)) * sig * math.sqrt(Tm))
    kind = "p" if K < S else "c"
    sd = sig * math.sqrt(Tm)
    d1 = (math.log(S / K) + (r_ + sig * sig / 2) * Tm) / sd
    c = S * norm.cdf(d1) - K * math.exp(-r_ * Tm) * norm.cdf(d1 - sd)
    price = c if kind == "c" else c - S + K * math.exp(-r_ * Tm)
    if price < 1e-8:
        continue
    tested += 1
    out = float(E6["implied_vols"]([price], [K], S, r_, Tm, [kind])[0])
    badv += not abs(out - sig) < 1e-6
check("l6.s8 attack: 400 random strikes, maturities and vols", badv == 0, f"tested={tested} bad={badv}")
# iteration counts on screen 4: instrument a copy of the lesson's loop


def counts(prices, strikes, kinds_):
    p_ = np.asarray(prices, float); K_ = np.asarray(strikes, float); kk = np.asarray(kinds_)
    f = lambda s: E6["bs_price"](S, K_, r_, T, s, kk) - p_
    lo = np.full(p_.shape, 1e-4); hi = np.full(p_.shape, 5.0)
    s = np.full(p_.shape, 0.2)
    its_ = np.zeros(p_.shape, int); bis = np.zeros(p_.shape, int); live = np.ones(p_.shape, bool)
    with np.errstate(all="ignore"):
        for _ in range(100):
            fs = f(s); low = fs < 0
            lo = np.where(low, s, lo); hi = np.where(low, hi, s)
            new = s - fs / E6["bs_vega"](S, K_, r_, T, s)
            badm = ~np.isfinite(new) | (new <= lo) | (new >= hi)
            new = np.where(badm, 0.5 * (lo + hi), new)
            its_ += live; bis += live & badm
            live &= ~(np.abs(new - s) < 1e-10)
            s = new
            if not live.any():
                break
    return its_, bis


# l6 screens[8] solution: a strike that has converged is not frozen, and a zero Newton step counts as "left the bracket",
# so solved strikes are thrown back to the bracket's midpoint and re-solved until the whole book is done in one pass.


def passes(fn_env, name, *args):
    n_ = [0]
    orig = fn_env["bs_price"]

    def cp(*a):
        n_[0] += 1
        return orig(*a)
    fn_env["bs_price"] = cp
    out_ = fn_env[name](*args)
    fn_env["bs_price"] = orig
    return out_, n_[0] - 2          # two calls set up the bracket test


K1k = np.linspace(80, 120, 1000)
kinds1k = np.where(K1k < 100, "p", "c")
tv1k = 0.2 + 0.001 * (K1k - 100) ** 2 / 10
P1k = E6["bs_price"](100.0, K1k, 0.05, 1 / 12, tv1k, kinds1k)
o1k, n1k_ = passes(E6, "implied_vols", P1k, K1k, 100.0, 0.05, 1 / 12, kinds1k)
oex, nex = passes(E6, "implied_vols", E6["bs_price"](100.0, [100.0], 0.05, 1 / 12, 0.2, ["c"]), [100.0], 100.0, 0.05, 1 / 12, ["c"])
check("l6.s8 the book's answers are right all the same", float(np.max(np.abs(o1k - tv1k))) < 1e-9 and abs(float(oex[0]) - 0.2) < 1e-9)
# (corrected claim, fix pass) the solution now keeps a Newton step below tol (instead of reading a zero step as
# leaving the bracket) and freezes each strike once its step is below tol. Own computation: a scalar safeguarded
# Newton, one strike at a time, counts each strike's passes; the vectorised book must need exactly the hardest
# strike's count. The pre-fix loop (35 passes, 24 for an exact start) is rebuilt below for contrast.


def _scalar_passes(p_, K_, kk, tol=1e-10):
    g = lambda v: float(E6["bs_price"](100.0, np.array([K_]), 0.05, 1 / 12, v, np.array([kk]))[0]) - p_
    lo_, hi_, v, n_ = 1e-4, 5.0, 0.2, 0
    while True:
        n_ += 1
        gv = g(v)
        if gv < 0:
            lo_ = v
        else:
            hi_ = v
        nv = v - gv / float(E6["bs_vega"](100.0, np.array([K_]), 0.05, 1 / 12, v)[0])
        if not abs(nv - v) < tol and not (lo_ < nv < hi_):
            nv = 0.5 * (lo_ + hi_)
        if abs(nv - v) < tol:
            return n_
        v = nv


its1k = np.array([_scalar_passes(float(P1k[i]), float(K1k[i]), str(kinds1k[i])) for i in range(0, 1000, 1)])
_src6 = json.load(open(os.path.join(COURSE, "l6-safe-root-finder.json")))["screens"][8]["widget"]["solution"]
_old6 = '''
import numpy as np

def implied_vols(prices, strikes, S, r, T, kinds, tol=1e-10, maxit=100):
    p = np.asarray(prices, dtype=float)
    K = np.asarray(strikes, dtype=float)
    kinds = np.asarray(kinds)
    f = lambda s: bs_price(S, K, r, T, s, kinds) - p
    lo = np.full(p.shape, 1e-4)
    hi = np.full(p.shape, 5.0)
    ok = (f(lo) < 0) & (f(hi) > 0)
    s = np.full(p.shape, 0.2)
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        for _ in range(maxit):
            fs = f(s)
            low = fs < 0
            lo = np.where(low, s, lo)
            hi = np.where(low, hi, s)
            new = s - fs / bs_vega(S, K, r, T, s)
            bad = ~np.isfinite(new) | (new <= lo) | (new >= hi)
            new = np.where(bad, 0.5 * (lo + hi), new)
            done = np.abs(new - s) < tol
            s = new
            if np.all(done | ~ok):
                break
    return np.where(ok, s, np.nan)
'''
_E6o = dict(E6); exec(_old6, _E6o)
o1k_old, n1k_old = passes(_E6o, "implied_vols", P1k, K1k, 100.0, 0.05, 1 / 12, kinds1k)
_, nex_old = passes(_E6o, "implied_vols", E6["bs_price"](100.0, [100.0], 0.05, 1 / 12, 0.2, ["c"]), [100.0], 100.0, 0.05, 1 / 12, ["c"])
check("l6.s8 a book of 1,000 strikes needs about as many passes as its hardest strike (at most 12), and an exact start needs 1 (corrected claim, fix pass)",
      "live" in _src6 and n1k_ <= 12 and n1k_ == int(its1k.max()) and nex == 1 and n1k_old == 35 and nex_old == 24
      and float(np.max(np.abs(o1k - o1k_old))) < 1e-10,
      f"fixed loop: {n1k_} passes for the book (hardest strike {int(its1k.max())}), {nex} for an exact start; old loop: {n1k_old} and {nex_old}")
it_, bi_ = counts(Q, Ks, kinds)
check("l6.s4 iteration table", (it_[0], it_[1], it_[2], it_[5], it_[10]) == (9, 9, 8, 2, 6) and list(bi_[[0, 1, 2, 5, 10]]) == [1, 1, 0, 0, 0]
      and 2 <= it_.min() and it_.max() <= 9, f"its={list(it_)} bis={list(bi_)}")
check("r2/h2 wing numbers", near(0.0001 / 0.0218 * 100, 0.46, ab=0.005) and near(0.0005 / 0.02 * 100, 2.5, ab=1e-9))

# ---------------------------------------------------------------- l7 interpolation
runge = lambda v: 1 / (1 + 25 * v ** 2)
grid = np.linspace(-1, 1, 20001)


def bary(xs, ys, xq):
    xs = np.asarray(xs, float)
    w = np.array([1 / np.prod(xj - np.delete(xs, j)) for j, xj in enumerate(xs)])
    d = xq[:, None] - xs[None, :]
    hit = d == 0
    d[hit] = 1
    t = w / d
    out = (t @ ys) / t.sum(axis=1)
    rr, cc = np.nonzero(hit)
    out[rr] = np.asarray(ys)[cc]
    return out


def maxerr(nodes):
    return float(np.max(np.abs(bary(nodes, runge(nodes), grid) - runge(grid))))


eq = {n: maxerr(np.linspace(-1, 1, n + 1)) for n in (4, 8, 10, 20)}
ch = {n: maxerr(np.cos(np.arange(n + 1) * np.pi / n)) for n in (4, 8, 10, 20)}
check("l7 Runge on equal spacing", near(eq[4], 0.4384, ab=1e-4) and near(eq[8], 1.0452, ab=1e-4) and near(eq[10], 1.9157, ab=1e-4)
      and near(eq[20], 59.82, ab=0.01), str(eq))
check("l7 Runge on Chebyshev nodes", near(ch[4], 0.4600, ab=1e-4) and near(ch[8], 0.2047, ab=1e-4) and near(ch[10], 0.1322, ab=1e-4)
      and near(ch[20], 0.0177, ab=1e-4), str(ch))
# independent check of the n=10 value in exact rational arithmetic (Lagrange form)
xsF = [Fraction(-1) + Fraction(2 * k, 10) for k in range(11)]
ysF = [1 / (1 + 25 * v * v) for v in xsF]
xq = Fraction(95, 100)
pF = sum(ysF[j] * math.prod((xq - xsF[m]) / (xsF[j] - xsF[m]) for m in range(11) if m != j) for j in range(11))
check("l7.s1 p10(0.95) exactly", near(float(pF), 1.9236, ab=5e-5) and near(float(1 / (1 + 25 * xq * xq)), 0.0424, ab=5e-5)
      and near(float(pF) - 0.0424, 1.8812, ab=1e-4))
prod_eq = lambda v: abs(np.prod(v - np.linspace(-1, 1, 11)))
check("l7.s3 node product", near(prod_eq(0.95), 0.00845, rel=0.002) and near(prod_eq(0.05), 6.71e-5, rel=0.002)
      and near(prod_eq(0.95) / prod_eq(0.05), 126, rel=0.01))
chn = np.cos(np.arange(11) * np.pi / 10)
pc = np.max(np.abs(np.prod(grid[:, None] - chn[None, :], axis=1)))
check("l7.s3 Chebyshev node product never above 2^-9", 0.95 * 2.0 ** -9 < pc <= 2.0 ** -9, f"{pc:.6e} against {2.0 ** -9:.6e}")


def lebesgue(xs):
    xs = np.asarray(xs, float)
    w = np.array([1 / np.prod(xj - np.delete(xs, j)) for j, xj in enumerate(xs)])
    g = np.setdiff1d(grid, xs)
    d = g[:, None] - xs[None, :]
    t = w / d
    return float(np.max(np.abs(t).sum(axis=1) / np.abs(t.sum(axis=1))))


check("l7.s4 Lebesgue constants 29.9 and 2.42", near(lebesgue(np.linspace(-1, 1, 11)), 29.9, ab=0.05) and near(lebesgue(chn), 2.42, ab=0.01),
      f"{lebesgue(np.linspace(-1, 1, 11)):.3f} {lebesgue(chn):.3f}")
sgn = np.array([(-1) ** k for k in range(11)]) * 0.001
kk = np.linspace(75, 125, 20001)
sw = bary(np.linspace(75, 125, 11), sgn, kk)
ix = int(np.argmax(np.abs(sw)))
check("l7.s8 alternating quote errors", near(abs(sw[ix]), 0.0292, ab=1e-4) and (near(kk[ix], 76.6, ab=0.1) or near(kk[ix], 123.4, ab=0.1))
      and abs(sw[ix]) < 0.0299, f"{sw[ix]:.5f} at {kk[ix]:.2f}")
# x^3 through any four nodes is reproduced; uniqueness
nd = np.array([0.0, 0.3, 1.1, 2.0])
check("l7.s6 cubic reproduced", float(np.max(np.abs(bary(nd, nd ** 3, np.linspace(-1, 3, 101)) - np.linspace(-1, 3, 101) ** 3))) < 1e-12)
# Is the barycentric formula "stable" as the lesson says, with no condition on the nodes?
# Compare the float result with the exact interpolant OF THE FLOAT DATA (rational arithmetic), and
# measure the error in units of cond(x) * u, the best any algorithm can promise (Higham 2004, IMA J.
# Numer. Anal. 24: the second barycentric formula is forward stable only for small Lebesgue constants).


def bary_excess(nodes, q):
    ys_ = runge(nodes)
    xf = [Fraction(float(v)) for v in nodes]
    yf = [Fraction(float(v)) for v in ys_]
    qf = Fraction(q)
    ls = [math.prod((qf - xf[m]) / (xf[j] - xf[m]) for m in range(len(xf)) if m != j) for j in range(len(xf))]
    ex = sum(l * y for l, y in zip(ls, yf))
    cond = float(sum(abs(l * y) for l, y in zip(ls, yf)) / abs(ex))
    fl = bary(nodes, ys_, np.array([q]))[0]
    return abs(fl - float(ex)) / abs(float(ex)) / (cond * 2.0 ** -53), abs(fl - float(ex)) / abs(float(ex))


QS = (-0.997, -0.955, -0.503, 0.001, 0.333, 0.871, 0.993)
ex_ch = max(bary_excess(np.cos(np.arange(n + 1) * np.pi / n), q)[0] for n in (10, 20, 40, 60) for q in QS)
ex_eq20 = max(bary_excess(np.linspace(-1, 1, 21), q) for q in QS)
ex_eq40 = max(bary_excess(np.linspace(-1, 1, 41), q) for q in QS)
ex_eq60 = max(bary_excess(np.linspace(-1, 1, 61), q) for q in QS)
check("l7.s7 barycentric formula is stable on Chebyshev nodes (error within 20 cond u, n to 60)", ex_ch < 20, f"{ex_ch:.1f} cond*u")
check("l7.s7 barycentric formula keeps 11 figures on the lesson's own grids (equal nodes, n = 20)", ex_eq20[1] < 1e-11, f"rel err {ex_eq20[1]:.1e}")
# (corrected claim, fix pass) the content now says the formula is stable on Chebyshev (well-placed) nodes, and no longer
# "stable" for any nodes. Own computation: within 20 cond u on Chebyshev nodes to n = 60, but far beyond it on equal
# spacing (n = 40 and 60), so the condition on the nodes is needed; the three texts carry it.
_l7 = json.load(open(os.path.join(COURSE, "l7-interpolation.json")))
_t7 = [_l7["screens"][7]["explain"]["text"], _l7["summary"]["ideas"][0], _l7["quiz"][0]["explain"]["text"]]
check("l7.s7 barycentric formula is stable on Chebyshev nodes, not on equal spacing, and the text says so (corrected claim, fix pass)",
      ex_ch < 20 and ex_eq40[0] > 1e3 and ex_eq60[1] > 1e-6 and all("Chebyshev" in x for x in _t7)
      and "and is stable, so" not in _t7[0] and not _t7[1].endswith("evaluates it stably.") and "most stable" not in _t7[2],
      f"Chebyshev {ex_ch:.1f} cond*u; equal n=40: {ex_eq40[0]:.1e} cond*u, rel err {ex_eq40[1]:.1e}; n=60: rel err {ex_eq60[1]:.1e}")
check("r2/q2 Lebesgue arithmetic", near(29.9 * 0.002, 0.0598, ab=1e-9) and near(2.42 * 0.002, 0.00484, ab=1e-9))

# ---------------------------------------------------------------- l8 splines
t = np.array([1, 2, 3, 5, 7, 10, 20, 30.0])
z = np.array([4.1, 3.95, 3.9, 3.95, 4.05, 4.25, 4.7, 4.8])
cs = CubicSpline(t, z, bc_type="natural")
M = cs(t, 2)
check("l8.s3 second derivatives", np.allclose(M[1:-1], [0.1372, 0.0510, 0.0033, 0.0107, -0.0047, -0.0041], atol=5e-5)
      and abs(M[0]) < 1e-12 and abs(M[-1]) < 1e-12, str(np.round(M, 6)))
h = np.diff(t)
Am = np.zeros((6, 6))
rhs = np.zeros(6)
for i in range(1, 7):
    j = i - 1
    if j > 0:
        Am[j, j - 1] = h[i - 1]
    Am[j, j] = 2 * (h[i - 1] + h[i])
    if j < 5:
        Am[j, j + 1] = h[i]
    rhs[j] = 6 * ((z[i + 1] - z[i]) / h[i] - (z[i] - z[i - 1]) / h[i - 1])
check("l8.s2 system", Am.tolist() == [[4, 1, 0, 0, 0, 0], [1, 6, 2, 0, 0, 0], [0, 2, 8, 2, 0, 0], [0, 0, 2, 10, 3, 0], [0, 0, 0, 3, 26, 10], [0, 0, 0, 0, 10, 40]]
      and np.allclose(rhs, [0.60, 0.45, 0.15, 0.10, -0.13, -0.21]) and np.allclose(np.linalg.solve(Am, rhs), M[1:-1]))
check("l8.s1 spline values", near(float(cs(4)), 3.9114, ab=5e-5) and near(float(cs(15)), 4.5297, ab=5e-5))
poly = np.polynomial.polynomial.Polynomial.fit(t, z, 7)
check("l8.s0 degree-7 polynomial", near(poly(4), 3.9103, ab=1e-4) and near(poly(15), 5.1921, ab=1e-4) and near(poly(25), -2.58, ab=0.01),
      f"{poly(4):.4f} {poly(15):.4f} {poly(25):.3f}")
fwd = lambda u: float(cs(u) + u * cs(u, 1))
check("l8.s4 forwards", near(fwd(4), 4.0273, ab=1e-4) and near(fwd(15), 5.2010, ab=1e-4) and near(3.95 + 5 * 0.025, 4.075, ab=1e-12)
      and near(3.95 + 5 * 0.05, 4.20, ab=1e-12))
zb = z.copy()
zb[3] += 0.10
cb = CubicSpline(t, zb, bc_type="natural")
mv = lambda u: float(cb(u) - cs(u)) * 100
check("l8.s5 bump effects", near(mv(15), 3.25, ab=0.01) and near(mv(4), 5.51, ab=0.01) and near(mv(6), 6.42, ab=0.01) and near(mv(8.5), -2.67, ab=0.01),
      f"{mv(4):.2f} {mv(6):.2f} {mv(8.5):.2f} {mv(15):.2f}")
check("l8.s5 every inner M changes", bool(np.all(np.abs(cb(t, 2) - M)[1:-1] > 1e-6)))
others = [u for u in t if u != 5]
fine = np.linspace(1, 30, 2901)
moved = np.abs(cb(fine) - cs(fine)) > 1e-12
# (corrected claim, fix pass) review-2 items[7] now keys "Rates between every pair of quotes" and says the seven other
# quoted rates stay put. Own computation: the move is 0 at the seven other quotes (interpolation), and on 2,901
# maturities it is nonzero everywhere strictly between quotes, with no sign change inside any interval.
_r2 = json.load(open(os.path.join(COURSE, "review-2.json")))["items"][7]
_between = fine[~np.isin(fine, t)]
_mvb = (cb(_between) - cs(_between)) * 100
_nozero = all(int(np.sum(np.diff(np.sign(_mvb[(_between > a_) & (_between < b_)])) != 0)) == 0 for a_, b_ in zip(t[:-1], t[1:]))
check("r2 spline-global: every rate between quotes moves, the seven other quotes stay put (corrected claim, fix pass)",
      all(abs(mv(u)) < 1e-9 for u in others) and bool(np.all(np.abs(_mvb) > 1e-9)) and _nozero
      and _r2["widget"]["options"][0]["text"].startswith("Rates between every pair of quotes") and "seven other quoted rates stay put" in _r2["explain"]["text"],
      f"move at the seven other quotes: {max(abs(mv(u)) for u in others):.1e} bp; smallest move between quotes {np.min(np.abs(_mvb)):.1e} bp")
check("r2 spline-global corrected: every rate between quotes moves", bool(np.all(moved[np.array([not any(abs(x - u) < 1e-9 for u in others) for x in fine])])))
check("l8.s7 prices", near(100 * math.exp(-4 * float(cs(4)) / 100), 85.5169, ab=1e-4) and near(100 * math.exp(-4 * 0.03925), 85.4704, ab=1e-4)
      and near(100 / 1.03925 ** 4, 85.7274, ab=1e-3) and near(85.5169 - 85.4704, 0.0465, ab=1e-4))
E8 = load("l8-splines", "screens", 7)
Ms = E8["natural_spline_M"](t, z / 100)
check("l8.s7 solution equals CubicSpline", np.allclose(Ms, M / 100, atol=1e-12)
      and all(abs(E8["spline_eval"](t, z / 100, Ms, u) - float(cs(u)) / 100) < 1e-12 for u in np.linspace(1, 30, 400)))
# natural spline of Runge's function on equal spacing: the error falls as knots are added
se_ = []
for n in (10, 20, 40, 80):
    kn = np.linspace(-1, 1, n + 1)
    se_.append(float(np.max(np.abs(CubicSpline(kn, runge(kn), bc_type="natural")(grid) - runge(grid)))))
check("l8 summary: spline error on Runge's function falls with n", all(se_[i + 1] < se_[i] for i in range(3)), str([f"{v:.1e}" for v in se_]))
check("h2 spline M2", near(6 * ((2 - 2) / 2 - 2 / 1) / (2 * 3), -2, ab=1e-12))
# homework-2 ytm_book attacks
YB = load("homework-2", "items", 6)["ytm_book"]
check("h2 ytm_book: 95 bond, zero, par", near(float(YB([95.0], [0.05], [5])[0]), ytm, ab=1e-10)
      and near(float(YB([100.0], [0.04], [7])[0]), 0.04, ab=1e-10) and bool(np.isnan(YB([130.0], [0.05], [5])[0])))
nn = rng.integers(1, 41, 3000)
cc = rng.uniform(0.0, 0.15, 3000)
yy = rng.uniform(0.0005, 0.95, 3000)
pp = np.array([sum(100 * c_ / (1 + y_) ** k for k in range(1, n_ + 1)) + 100 / (1 + y_) ** n_ for n_, c_, y_ in zip(nn, cc, yy)])
out = YB(pp, cc, nn)
check("h2 ytm_book attack: 3,000 bonds, yields from 0.05% to 95%", float(np.nanmax(np.abs(out - yy))) < 1e-9 and not np.isnan(out).any(),
      f"max err {float(np.nanmax(np.abs(out - yy))):.1e}")
# homework-2 items[6]: the same unfrozen loop as l6 screens[8]; count its passes on the item's own 1,000-bond test
_src = json.load(open(os.path.join(COURSE, "homework-2.json")))["items"][6]["widget"]["solution"]
_src = _src.replace("    for _ in range(maxit):\n", "    for _ in range(maxit):\n        PASSES[0] += 1\n")
_e = {"PASSES": [0]}
exec(_src, _e)
r3 = np.random.default_rng(3)
n1 = r3.integers(1, 31, 1000); c1 = r3.uniform(0.0, 0.08, 1000); y1 = r3.uniform(0.005, 0.12, 1000)
p1 = np.array([sum(100 * c_ / (1 + y_) ** k for k in range(1, n_ + 1)) + 100 / (1 + y_) ** n_ for n_, c_, y_ in zip(n1, c1, y1)])
out1 = _e["ytm_book"](p1, c1, n1)
book_passes = _e["PASSES"][0]
_e["PASSES"][0] = 0
_e["ytm_book"]([95.0], [0.05], [5])
# (corrected claim, fix pass) the solution now keeps a Newton step below tol and freezes each bond once solved (the
# pre-fix loop took 19 passes). Own computation: a scalar safeguarded Newton per bond; the book needs the hardest bond's count.


def _bond_passes(p_, c_, n_, tol=1e-12):
    cfs = [100 * c_] * (n_ - 1) + [100 * c_ + 100]
    g = lambda v: sum(x / (1 + v) ** (k + 1) for k, x in enumerate(cfs)) - p_
    dg = lambda v: sum(-(k + 1) * x / (1 + v) ** (k + 2) for k, x in enumerate(cfs))
    lo_, hi_, v, m_ = 0.0, 1.0, (c_ if c_ > 0 else 0.05), 0
    while True:
        m_ += 1
        gv = g(v)
        if gv > 0:
            lo_ = v
        else:
            hi_ = v
        nv = v - gv / dg(v)
        if not abs(nv - v) < tol and not (lo_ < nv < hi_):
            nv = 0.5 * (lo_ + hi_)
        if abs(nv - v) < tol:
            return m_
        v = nv


_hard = max(_bond_passes(float(p1[i]), float(c1[i]), int(n1[i])) for i in range(1000))
check("h2 ytm_book: 1,000 bonds need at most 10 passes, the hardest bond's count (corrected claim, fix pass)",
      book_passes <= 10 and book_passes == _hard and float(np.max(np.abs(out1 - y1))) < 1e-9,
      f"{book_passes} passes for the book (hardest bond {_hard}), {_e['PASSES'][0]} for one bond; answers right to {float(np.max(np.abs(out1 - y1))):.0e}")
check("h2 order", near(math.log(3.16e-5 / 1e-3) / math.log(1e-3 / 1e-2), 1.5, ab=0.01))

print(f"\n{N} checks, {len(FAILS)} failed, {len(XFAILS)} expected fails")
for f in FAILS:
    print("  FAILED:", f)
for f in XFAILS:
    print("  EXPECTED_FAIL:", f)
sys.exit(1 if FAILS else 0)
