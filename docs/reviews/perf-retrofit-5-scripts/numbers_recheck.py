"""Reader recompute of the longform numbers (coint L1, mm-games L3, momentum-rep L1), by routes the authors did not use.
Venv Python, from this folder. Prints each figure; exits 1 only if a figure the item states fails its check.
Notes printed with 'NOTE' are findings, not failures (they are asserted in findings_assert.py)."""
import math, sys
from fractions import Fraction as F
from itertools import product
import numpy as np
import statsmodels.api as sm
from scipy.stats import norm

fails = 0
def check(name, ok, val):
    global fails
    fails += not ok
    print(("ok   " if ok else "FAIL ") + name + "  " + str(val))

# ---------------- coint L1: statsmodels OLS on the lesson generator, seeds 0 to 1,999, n = 1,000
n = 1000
T, R2 = [], []
for seed in range(2000):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    x, y = np.cumsum(z[:, 0]), np.cumsum(z[:, 1])
    f = sm.OLS(y, sm.add_constant(x)).fit()
    T.append(abs(f.tvalues[1])); R2.append(f.rsquared)
T, R2 = np.array(T), np.array(R2)
check("coint: 91.9% of seeds 0-1,999 give |t| > 1.96 (statsmodels)", round(100 * (T > 1.96).mean(), 1) == 91.9, (T > 1.96).mean())
check("coint: 95th percentile of |t| 48.0", round(np.quantile(T, 0.95), 1) == 48.0, np.quantile(T, 0.95))
check("coint: 9.4% with R^2 >= 0.60", round(100 * (R2 >= 0.6).mean(), 1) == 9.4, (R2 >= 0.6).mean())
check("coint: median R^2 0.18", round(np.median(R2), 2) == 0.18, np.median(R2))
check("coint: t from R^2 = 0.60, n = 1,000 is 38.7", round(math.sqrt(998 * 0.6 / 0.4), 1) == 38.7, math.sqrt(998 * 0.6 / 0.4))
# population values from a large independent run (seed 424242, 20,000 pairs), vectorised in chunks
pt, pr, q = [], [], []
rng = np.random.default_rng(424242)
for _ in range(10):
    Z = rng.standard_normal((2000, n, 2)).cumsum(1)
    X, Y = Z[:, :, 0] - Z[:, :, 0].mean(1, keepdims=True), Z[:, :, 1] - Z[:, :, 1].mean(1, keepdims=True)
    r = (X * Y).sum(1) / np.sqrt((X * X).sum(1) * (Y * Y).sum(1))
    pr.extend(r * r); pt.extend(np.abs(r) * np.sqrt((n - 2) / (1 - r * r)))
pt, pr = np.array(pt), np.array(pr)
print(f"NOTE coint population (20,000 pairs): |t|>1.96 {100*(pt>1.96).mean():.1f}%, 95th pct {np.quantile(pt,0.95):.1f}, "
      f"R^2>=0.6 {100*(pr>=0.6).mean():.1f}%, median R^2 {np.median(pr):.3f}")
check("coint: 'roughly nine in ten' holds for the population too", 0.88 < (pt > 1.96).mean() < 0.95, (pt > 1.96).mean())
check("coint: 'about one in eleven' near the population share (within 1.5 points)", abs((pr >= 0.6).mean() - 0.094) < 0.015, (pr >= 0.6).mean())
# drift 0.05 a day, sd 1, reader seed
for m, want in ((1000, 0.49), (16000, 0.97)):
    rr = []
    g = np.random.default_rng(777 + m)
    for _ in range(4):
        Z = (0.05 + g.standard_normal((250, m, 2))).cumsum(1)
        X, Y = Z[:, :, 0] - Z[:, :, 0].mean(1, keepdims=True), Z[:, :, 1] - Z[:, :, 1].mean(1, keepdims=True)
        rr.extend(((X * Y).sum(1)) ** 2 / ((X * X).sum(1) * (Y * Y).sum(1)))
    check(f"coint drift: median R^2 at {m} days near {want} (reader seed, 1,000 pairs)", abs(np.median(rr) - want) < 0.03, np.median(rr))
# AR(1) residual, phi 0.8, independent of x: share of |t| > 1.96 at 4,000 days
g = np.random.default_rng(99)
hits = []
for _ in range(4):
    m = 4000
    X = g.standard_normal((250, m)).cumsum(1)
    e = g.standard_normal((250, m)); u = np.zeros_like(e); u[:, 0] = e[:, 0] / math.sqrt(1 - 0.64)
    for t in range(1, m): u[:, t] = 0.8 * u[:, t - 1] + e[:, t]
    Y = 2.0 * X + u
    Xc, Yc = X - X.mean(1, keepdims=True), Y - Y.mean(1, keepdims=True)
    b = (Xc * Yc).sum(1) / (Xc * Xc).sum(1); res = Yc - b[:, None] * Xc
    se = np.sqrt((res * res).sum(1) / (m - 2) / (Xc * Xc).sum(1))
    hits.extend(np.abs((b - 2.0) / se) > 1.96)
check("coint f-up 2: about 51% pass 1.96 at 4,000 days (limit 2P(Z > 1.96/3))", abs(np.mean(hits) - 2 * norm.sf(1.96 / 3)) < 0.035, (np.mean(hits), 2 * norm.sf(1.96 / 3)))
# long-run variance of AR(1) by summing autocovariances: gamma0 (1 + 2 sum phi^k) = sigma^2/(1-phi)^2
phi = 0.8
lrv = (1 / (1 - phi ** 2)) * (1 + 2 * sum(phi ** k for k in range(1, 400)))
check("coint f-up 2: gamma0 (1 + 2 sum phi^k) = 1/(1 - phi)^2 = 25", abs(lrv - 25) < 1e-9, lrv)

# ---------------- mm-games L3: exact law of the total
def dice(k):
    d = {}
    for r in product(range(1, 7), repeat=k):
        d[sum(r)] = d.get(sum(r), 0) + F(1, 6 ** k)
    return d
two, four = dice(2), dice(4)
mix = {s: F(1, 2) * two.get(s, 0) + F(1, 2) * four.get(s, 0) for s in range(2, 25)}
mean = sum(s * p for s, p in mix.items()); var = sum(s * s * p for s, p in mix.items()) - mean ** 2
check("mm3: fair 10.5", mean == F(21, 2), mean)
check("mm3: variance 21, sd 4.58", var == 21, (var, math.sqrt(var)))
after6 = {s: F(1, 2) * dice(1).get(s, 0) + F(1, 2) * dice(3).get(s, 0) for s in range(1, 19)}
m6 = sum(s * p for s, p in after6.items()); v6 = sum(s * s * p for s, p in after6.items()) - m6 ** 2
check("mm3: after the 6, fair 6 + 7 = 13 and variance of the rest 18.08 (sd 4.25)", 6 + m6 == 13 and abs(float(v6) - 18.0833) < 1e-3, (6 + m6, float(v6), math.sqrt(v6)))
check("mm3: one die sd 1.71", abs(math.sqrt(35 / 12) - 1.708) < 1e-3, math.sqrt(35 / 12))
pm = lambda S: float(sum(mix[s] for s in S))
print("NOTE mm3 law of the total:", {s: round(float(p), 4) for s, p in mix.items() if 4 <= s <= 18})
print(f"NOTE mm3 P(6-8) {pm([6,7,8]):.3f}, P(9-12) {pm([9,10,11,12]):.3f}, P(13-15) {pm([13,14,15]):.3f}, P(10 or 11) {pm([10,11]):.3f}; P(10) {pm([10]):.4f} > P(14) {pm([14]):.4f}")
modes = [s for s in range(3, 24) if mix[s] > mix[s - 1] and mix[s] > mix[s + 1]]
print("NOTE mm3 local modes of the total:", modes, "(14 is a mode only by", round(float(mix[14] - mix[13]), 4), ")")
# P&L chain
cash, pos, edge = 0.0, 0, 0.0
for side, px, lots, fair in (("sell", 13, 1, 10.5), ("buy", 11.5, 2, 13), ("sell", 10, 1, 9.5)):
    sgn = 1 if side == "buy" else -1
    cash -= sgn * px * lots; pos += sgn * lots; edge += lots * (fair - px) * sgn
check("mm3: edge 6, flat, P&L 0", edge == 6 and pos == 0 and cash == 0, (edge, pos, cash))

# ---------------- momentum-rep L1
months = (2000 - 1963) * 12 + (11 - 7) + 1
check("mom1: rankings July 1963 to November 2000 give 449 months", months == 449, months)
se = 6.0 / math.sqrt(449)
check("mom1: 6.0/sqrt(449) = 0.28", round(se, 2) == 0.28, se)
check("mom1: band -1.63 to -0.49", (round(-1.06 - 2 * se, 2), round(-1.06 + 2 * se, 2)) == (-1.63, -0.49), (-1.06 - 2 * se, -1.06 + 2 * se))
import datetime as dt
days = [dt.date(1972, 12, d) for d in range(14, 32) if dt.date(1972, 12, d).weekday() < 5 and d not in (25, 28)]
print(f"NOTE mom1: Nasdaq trading days in December 1972 from the 14th (25th Christmas, 28th closed for Truman's funeral): {len(days)}; fewer than 15")
sys.exit(1 if fails else 0)
