"""Fix-pass read, markov L4-5 round 2 (commit edc8ef32). Recomputes every figure in the changed strings.

Run: python docs/reports/markov-L4-5-fixread-r2.py   (NumPy only; exits 0 when the content agrees).
Engine replays copy the walk canvas: mulberry32 from js/engine/sim.js, seed * 7919 + run * 104729, and per step
one uniform then one Box-Muller normal (js/engine/canvas/walk.js draws(), plane.js gauss()).
"""
import math
import sys
from fractions import Fraction

import numpy as np

FAIL = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
    if not ok:
        FAIL.append(name)


M32 = 0xFFFFFFFF


def imul(a, b):
    return (a * b) & M32


def mulberry(seed):
    a = seed & M32

    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & M32
        t = a
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & M32
        return ((t ^ (t >> 14)) & M32) / 4294967296

    return r


def engine_walk(seed, paths, steps, p, start, lower, upper):
    """Replays walk.js: returns (tau, S_tau, hit flag, up flag) per path; tau is capped at steps."""
    rng = mulberry((seed * 7919) & M32)
    res = []
    for _ in range(paths):
        us = []
        for _ in range(steps):
            us.append(rng())
            u = 0.0
            while u <= 1e-12:  # gauss(): first uniform, redrawn if tiny
                u = rng()
            rng()  # gauss(): second uniform
        x, hit = start, -1
        if x >= upper or x <= lower:
            hit = 0
        i = 0
        while hit < 0 and i < steps:
            x += 1 if us[i] < p else -1
            i += 1
            if x >= upper or x <= lower:
                hit = i
        res.append((hit if hit >= 0 else steps, x, hit >= 0, x >= upper))
    return res


def capped(p, start, lower, upper, cap):
    """Exact law of the walk stopped at the barriers or at step cap: (E[min(T, cap)], P(alive at cap), E[S at stop])."""
    n = upper - lower + 1
    v = np.zeros(n)
    v[start - lower] = 1.0
    et, es = 0.0, 0.0
    for _ in range(cap):
        alive = v[1:-1].sum()
        et += alive
        w = np.zeros(n)
        w[2:] += p * v[1:-1]
        w[:-2] += (1 - p) * v[1:-1]
        w[0] += v[0]
        w[-1] += v[-1]
        v = w
    es = float((v * np.arange(lower, upper + 1)).sum())
    return et, float(v[1:-1].sum()), es, float(v[-1])


rs = np.random.default_rng(20261126)

# ---- l14 ----
# screens[4]: Kac, mean return time 1/pi_i on a connected network (venues A-B, A-C, A-D, B-C)
P = np.array([[0, 1 / 3, 1 / 3, 1 / 3], [.5, 0, .5, 0], [.5, .5, 0, 0], [1, 0, 0, 0]])
pi = np.array([3, 2, 2, 1]) / 8
check("l14 s4 pi is stationary", np.allclose(pi @ P, pi))
for i, name in enumerate("ABCD"):
    # mean return time by first-step analysis: m_i = 1 + sum_{j != i} P_ij h_j, h solves (I - Q) h = 1
    keep = [k for k in range(4) if k != i]
    h = np.linalg.solve(np.eye(3) - P[np.ix_(keep, keep)], np.ones(3))
    m = 1 + P[i, keep] @ h
    check(f"l14 s4 return time to {name} = 1/pi", abs(m - 1 / pi[i]) < 1e-9, f"{m:.4f}")
# Kac also on a bipartite (periodic) and a weighted connected network
for W in (np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], float), np.array([[0, 1, 3], [1, 0, 2], [3, 2, 0]], float)):
    Pw = W / W.sum(1, keepdims=True)
    piw = W.sum(1) / W.sum()
    for i in range(3):
        keep = [k for k in range(3) if k != i]
        h = np.linalg.solve(np.eye(2) - Pw[np.ix_(keep, keep)], np.ones(2))
        check("l14 s4 Kac on periodic / weighted network", abs(1 + Pw[i, keep] @ h - 1 / piw[i]) < 1e-9)
# screens[6]: knight's graph
deg = {}
pairs = set()
for r in range(8):
    for c in range(8):
        k = 0
        for dr, dc in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
            if 0 <= r + dr < 8 and 0 <= c + dc < 8:
                k += 1
                pairs.add(frozenset(((r, c), (r + dr, c + dc))))
        deg[k] = deg.get(k, 0) + 1
check("l14 s6 degree classes", deg == {2: 4, 3: 8, 4: 20, 6: 16, 8: 16}, str(deg))
check("l14 s6 total 336, 168 unordered pairs", sum(k * v for k, v in deg.items()) == 336 and len(pairs) == 168)
# screens[10]: strengths add to twice the total weight
T = [("A", "B", 1), ("B", "C", 2), ("A", "C", 3)]
st = {}
for u, v, w in T:
    st[u] = st.get(u, 0) + w
    st[v] = st.get(v, 0) + w
check("l14 s10 strengths sum to twice total weight", sum(st.values()) == 2 * sum(w for *_, w in T))

# ---- l16 quiz[2]: piecewise-rate Poisson, mean 90, count Poisson (variance 90 too) ----
n = rs.poisson(4 * 10, 400000) + rs.poisson(1 * 50, 400000)
check("l16 q-varying-rate mean 90", abs(n.mean() - 90) < 0.1, f"{n.mean():.3f}")
check("l16 q-varying-rate variance 90 (Poisson)", abs(n.var() - 90) < 1.0, f"{n.var():.2f}")

# ---- l19 screens[7]: Wald ----
tot = []
g = rs.geometric(1 / 6, 400000)
tot = 6 + np.array([rs.integers(1, 6, k - 1).sum() for k in g[:200000]])
check("l19 s7 die total 21", abs(tot.mean() - 21) < 0.15, f"{tot.mean():.3f}")
# Wald needs a stopping time: T = last roll before the first 6 (looks ahead) breaks it
check("l19 s7 non-stopping time breaks the identity", abs((tot - 6).mean() - 3.5 * 5) > 1, f"{(tot - 6).mean():.2f} vs 17.5")
# Wald needs E[T] finite: fair walk stopped at first visit to +1 has S_T = 1, mu = 0 (E[T] infinite)
# Wald needs a common mean: steps X_k = 2^k * sign, not identically distributed, is the doubling game below.

# ---- l19 screens[9]: the wrong martingale, engine replay seed 6 ----
res = engine_walk(6, 200, 8000, 0.49, 50, 0, 100)
up = sum(1 for r in res if r[2] and r[3])
running = [r for r in res if not r[2]]
avg = sum(r[1] for r in res) / 200
check("l19 s9 23 of 200 reached 100", up == 23, str(up))
check("l19 s9 two still running at bet 8,000", len(running) == 2, f"{len(running)} running at {[r[1] for r in running]}")
check("l19 s9 average 11.75", abs(avg - 11.75) < 1e-9, f"{avg}")
r_ = Fraction(51, 49)
Pwin = float((1 - r_ ** 50) / (1 - r_ ** 100))
check("l19 s9 P about 0.1192", abs(Pwin - 0.1192) < 5e-5, f"{Pwin:.5f}")
et, alive, es, pu = capped(0.49, 50, 0, 100, 8000)
print(f"     exact: P(running at 8000) = {alive:.4f}, E[S at stop] = {es:.3f}, E[T uncapped] = {(50 - 100 * Pwin) / 0.02:.0f}")

# ---- l20 screens[2]: floor -L, upper +1, 300 paths, 1,000 bets, seed 2 ----
for L, want in ((9, 8.7), (99, None)):
    res = engine_walk(2, 300, 1000, 0.5, 0, -L, 1)
    tm = sum(r[0] for r in res) / 300
    unfinished = sum(1 for r in res if not r[2])
    et, alive, es, pu = capped(0.5, 0, -L, 1, 1000)
    print(f"     L={L}: batch tauMean {tm:.2f}, unfinished {unfinished}; exact E[min(T,1000)] {et:.2f}, P(T>1000) {alive:.4f}")
    if want is not None:
        check("l20 s2 batch at L=9 averaged 8.7", abs(round(tm, 1) - want) < 1e-9, f"{tm:.2f}")
    else:
        check("l20 s2 batch at L=99 shows about 40", 35 <= tm <= 45, f"{tm:.2f}")
        check("l20 s2 capped mean is far below 99", et < 60, f"{et:.2f}")
        # share of E[T] = 99 that comes from games longer than 1,000 bets, and how rare they are
        check("l20 s2 games past 1,000 bets are rare and carry about half the mean", alive < 0.05 and (99 - et) / 99 > 0.4, f"P {alive:.3f}, share {(99 - et) / 99:.2f}")
# E[T] = L exactly: i(N - i) with i = L, N = L + 1
check("l20 s2 E[T] = L", all(L * (L + 1 - L) == L for L in (9, 99)))

# ---- l20 screens[7]: doubling with unlimited money ----
ET = sum(k * 0.5 ** k for k in range(1, 200))
check("l20 s7 E[T] = 2", abs(ET - 2) < 1e-9)
part = [sum(Fraction(1, 2) ** k * 2 ** (k - 1) for k in range(1, m + 1)) for m in (10, 100)]
check("l20 s7 E[last stake] diverges (partial sums m/2)", part == [5, 50])
# martingale at every fixed n (so option 'mart' is false), yet M_T = 1 for sure (so the theorem's conclusion fails)
for nfix in (1, 5, 12):
    m = Fraction(0)
    for k in range(1, nfix + 1):
        m += Fraction(1, 2) ** k * 1  # won at bet k: net +1
    m += Fraction(1, 2) ** nfix * (-(2 ** nfix - 1))  # lost all nfix bets
    check(f"l20 s7 E[M at n={nfix}] = 0", m == 0)
# sum of absolute steps up to T has infinite mean: E[2^T - 1]
check("l20 s7 E[sum |steps|] diverges", sum(Fraction(1, 2) ** k * (2 ** k - 1) for k in range(1, 101)) > 99)

# ---- l21 quiz[3] ----
p, q = 0.6, 0.4
check("l21 q-biased-ht HH wait 4.4444", abs(1 / p + 1 / p ** 2 - 4.4444) < 5e-5)
check("l21 q-biased-ht HT wait 4.1667", abs(1 / (p * q) - 4.1667) < 5e-5)


def wait(pattern, reps):
    flips = rs.random((reps, 200)) < p
    out = np.zeros(reps)
    for i in range(reps):
        f = flips[i]
        for t in range(1, 200):
            if f[t - 1] == pattern[0] and f[t] == pattern[1]:
                out[i] = t + 1
                break
    return out.mean()


check("l21 simulated HH wait", abs(wait((True, True), 60000) - 4.4444) < 0.06)
check("l21 simulated HT wait", abs(wait((True, False), 60000) - 4.1667) < 0.05)

# ---- l22 screens[8] ----
nt = rs.poisson(50, 400000)
inv = 2 * rs.binomial(nt, 0.6) - nt
check("l22 s8 mean 10 over 10 minutes, drift 1 a minute", abs(inv.mean() - 10) < 0.05 and abs(5 * 0.2 - 1) < 1e-12, f"{inv.mean():.3f}")
check("l22 s8 sd 7.07", abs(inv.std() - math.sqrt(50)) < 0.03, f"{inv.std():.3f}")

print("FAILED: " + ", ".join(FAIL) if FAIL else "all checks pass")
sys.exit(1 if FAIL else 0)
