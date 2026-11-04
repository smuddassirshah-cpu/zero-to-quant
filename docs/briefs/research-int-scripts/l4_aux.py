"""research-int level 4 agent numbers: every value is computed by method A (hand formula, pure Python, fractions or math) and method B (numpy, pandas, statsmodels)."""
import math, bisect
from fractions import Fraction as F
import numpy as np, pandas as pd
import statsmodels.api as sm
from chk import two, done

def interp_hand(xs, ys, x):
    pts = {}
    for a, b in zip(xs, ys):
        if b is not None and not (isinstance(b, float) and math.isnan(b)): pts.setdefault(a, []).append(b)
    ks = sorted(pts); vs = [sum(pts[k]) / len(pts[k]) for k in ks]
    if x <= ks[0]: return vs[0]
    if x >= ks[-1]: return vs[-1]
    j = bisect.bisect_right(ks, x)
    if ks[j - 1] == x: return vs[j - 1]
    return vs[j - 1] + (vs[j] - vs[j - 1]) * (x - ks[j - 1]) / (ks[j] - ks[j - 1])
def interp_np(xs, ys, x):
    df = pd.DataFrame({"x": xs, "y": ys}).dropna().groupby("x", as_index=False).y.mean().sort_values("x")
    return float(np.interp(x, df.x, df.y))

# ---- review 1, 2 (fresh) ----
two("R4.1 xs (5,1,3) ys (50,20,26) at 4 is 38", interp_hand([5, 1, 3], [50, 20, 26], 4), interp_np([5, 1, 3], [50, 20, 26], 4)); two("   = 38", interp_hand([5, 1, 3], [50, 20, 26], 4), 38.0)
two("R4.1 unsorted wrong: line through first two listed points at 4", 20 + (50 - 20) * (4 - 1) / (5 - 1), float(np.polyval(np.polyfit([5, 1], [50, 20], 1), 4)), 1e-9); print("   wrong =", 20 + 30 * 3 / 4)
s = pd.Series([50, np.nan, 62.0], index=[0, 2, 8]);
two("R4.2 by time at t=2 is 53", interp_hand([0, 2, 8], [50, float('nan'), 62], 2), float(s.interpolate(method="index").iloc[1])); two("   = 53", interp_hand([0, 2, 8], [50, float('nan'), 62], 2), 53.0)
two("R4.2 by position is 56", 50 + 12 / 2, float(pd.Series([50, np.nan, 62.0]).interpolate().iloc[1]))
# ---- review 3 table: SE of a slope for n days 1..n with sigma 1.5 ----
for n in (100, 25, 4):
    d = np.arange(1, n + 1.0)
    sxx_hand = n * (n * n - 1) / 12; sxx_np = float(((d - d.mean()) ** 2).sum())
    two(f"SE n={n}: Sxx", sxx_hand, sxx_np)
    se_a = 1.5 / math.sqrt(sxx_hand); X = sm.add_constant(d); se_b = 1.5 * math.sqrt(np.linalg.inv(X.T @ X)[1, 1])
    two(f"SE n={n}", se_a, se_b, 1e-12); print("   se", round(se_a, 4))
tab = [("P", 100, 0.031), ("Q", 100, -0.004), ("R", 4, 0.20), ("S", 100, -0.022), ("T", 25, 0.09), ("U", 100, 0.0085)]
se = {100: 1.5 / math.sqrt(100 * 9999 / 12), 25: 1.5 / math.sqrt(1300), 4: 1.5 / math.sqrt(5)}
cnt_a = sum(1 for _, n, b in tab if abs(b) > 2 * se[n]); cnt_b = int(np.sum([abs(b) / se[n] > 2 for _, n, b in tab]))
two("R4.3 count of slopes beyond two standard errors", cnt_a, cnt_b); print("   t:", [(t, round(b / se[n], 2)) for t, n, b in tab], "count", cnt_a)
# ---- review 5, 6 ----
def fit_sums(P):
    n = len(P); sx = sum(F(a) for a, _ in P); sy = sum(F(b) for _, b in P); sxx = sum(F(a) ** 2 for a, _ in P); sxy = sum(F(a) * F(b) for a, b in P)
    m = (n * sxy - sx * sy) / (n * sxx - sx ** 2); return m, (sy - m * sx) / n, (n, sx, sy, sxx, sxy)
def fit_np(P): a = np.array(P, float); c = np.polyfit(a[:, 0], a[:, 1], 1); return float(c[0]), float(c[1])
P0 = [(1, 2), (2, 2), (3, 4), (4, 5)]; P1 = P0 + [(5, 5)]; P2 = P1[1:]
for label, P, want in (("base", P0, 1.1), ("add (5,5)", P1, 0.9), ("remove (1,2)", P2, 1.0)):
    m, b, st = fit_sums(P); m2, b2 = fit_np(P); two(f"R4.5/6 {label} slope", float(m), m2, 1e-12); two("   stated", float(m), want, 1e-12); two("   intercept", float(b), b2, 1e-12); print("   sums", st, "intercept", float(b))
# ---- review 7: naive variance in float64 ----
for off, k in ((1e9, 4), (1e8, 4), (1e9, 5), (1e10, 3), (1e8, 3), (1e9, 3)):
    xs = [off + i for i in range(1, k + 1)]
    naive = (sum(v * v for v in xs) - sum(xs) ** 2 / k) / (k - 1)
    exact = float((sum(F(v) ** 2 for v in xs) - sum(F(v) for v in xs) ** 2 / k) / (k - 1))
    print(f"   offset {off:g} n={k}: naive {naive!r} exact {exact!r} np.var {float(np.var(xs, ddof=1))!r}")
# ---- review 8 ----
raw, rep, blank, neg, overlap = 800, 20, 30, 6, 5
after_a = raw - rep - (blank + neg - overlap); after_b = raw - rep - (blank + neg) + overlap
two("R4.8 rows left", after_a, after_b); print("   =", after_a, " wrong (double count):", raw - rep - blank - neg)
# ---- review 9 ----
two("R4.9 0.4 + 1.35 ln 8", 0.4 + 1.35 * math.log(8), float(np.polyval([1.35, 0.4], np.log(8))), 1e-12); print("   =", round(0.4 + 1.35 * math.log(8), 4), " no-ln wrong", 0.4 + 1.35 * 8, " ln 800 wrong", round(0.4 + 1.35 * math.log(800), 4))

# ---- ticks queries (H4.1 fresh) ----
tk = pd.read_csv("data/ticks-gaps.csv")
clean = tk.dropna(subset=["price"]).groupby("t_sec", as_index=False).price.mean().sort_values("t_sec")
for tq in (3333, 16000, 20000, 7, 23258, 0, 23400):
    two(f"ticks at {tq}", interp_hand(tk.t_sec.tolist(), tk.price.tolist(), tq), interp_np(tk.t_sec, tk.price, tq), 1e-9); print("   ->", repr(interp_hand(tk.t_sec.tolist(), tk.price.tolist(), tq)))
# ---- towns (H4.2 fresh checks) ----
tt = pd.read_csv("data/towns-temp.csv")
def slope_cov(g):
    c = np.cov(g.day, g.temp_c, ddof=1); m = c[0, 1] / c[0, 0]; r = c[0, 1] / math.sqrt(c[0, 0] * c[1, 1])
    return pd.Series({"slope": m, "intercept": g.temp_c.mean() - m * g.day.mean(), "r2": r * r, "n": len(g)})
def slope_sm(g):
    f = sm.OLS(g.temp_c, sm.add_constant(g.day.astype(float))).fit(); return pd.Series({"slope": f.params["day"], "intercept": f.params["const"], "r2": f.rsquared, "n": len(g)})
A = tt[tt.town != "Wick"].groupby("town").apply(slope_cov, include_groups=False); B = tt[tt.town != "Wick"].groupby("town").apply(slope_sm, include_groups=False)
for t in ("Bath", "Cork", "Hove", "Ince", "Kelso", "Jarrow"):
    for c in ("slope", "intercept", "r2"): two(f"town {t} {c}", float(A.loc[t, c]), float(B.loc[t, c]), 1e-10)
    print("   ", t, {c: round(float(A.loc[t, c]), 7) for c in ("slope", "intercept", "r2")})
print("   Wick rows", tt[tt.town == "Wick"].to_dict("records"))
for t in ("Ayr", "Leith"): print("   ", t, {c: round(float(A.loc[t, c]), 7) for c in ("slope", "intercept", "r2")})
print("   n per town", tt.groupby("town").size().to_dict())
# ---- H4.8 ----
d = np.arange(1, 51.0); sxx = 50 * (2500 - 1) / 12; se_a = 2 / math.sqrt(sxx); se_b = 2 * math.sqrt(np.linalg.inv(sm.add_constant(d).T @ sm.add_constant(d))[1, 1])
two("H4.8 Sxx", sxx, float(((d - d.mean()) ** 2).sum())); two("H4.8 se 2/sqrt(Sxx)", se_a, se_b, 1e-12); print("   se", se_a, " wrong sigma/sqrt n", 2 / math.sqrt(50), " sigma/n", 2 / 50)
# ---- H4.5 table (fresh) ----
fills = [("X", 300, 20.10), ("X", 500, 20.30), ("X", 200, 19.90), ("Z", 100, 55.00), ("Z", 400, 55.50), ("Z", 500, 54.90)]
fd = pd.DataFrame(fills, columns=["sym", "qty", "px"])
for s in ("X", "Z"):
    a = sum(F(str(p)) * q for t, q, p in fills if t == s) / sum(q for t, q, p in fills if t == s); g = fd[fd.sym == s]; b = float((g.px * g.qty).sum() / g.qty.sum())
    two(f"H4.5 VWAP {s}", float(a), b, 1e-9); print("   ", s, float(a), "qty", int(g.qty.sum()), "n", len(g))
# ---- l19 transfer ----
a = (F("31.20") * 2000 + F("31.40") * 1500 + F("30.80") * 500) / 4000; b = np.average([31.2, 31.4, 30.8], weights=[2000, 1500, 500])
two("l19 transfer VWAP", float(a), float(b), 1e-9); print("   =", float(a), " repeat left in:", float((F("31.20") * 2000 + F("31.40") * 3000 + F("30.80") * 500) / 5500), " simple mean", (31.2 + 31.4 + 30.8) / 3)
# ---- l17 hook (Reed) ----
days = [1, 2, 3, 4]
for name, t in (("Reed", [10, 11, 11, 13]), ("Marsh", [12, 11, 11, 10]), ("Plain", [9, 10, 10, 9])):
    m_a = sum((d - 2.5) * (y - sum(t) / 4) for d, y in zip(days, t)) / 5; m_b = float(np.polyfit(days, t, 1)[0]); two(f"l17 hook {name} slope", m_a, m_b, 1e-12); print("   ", name, m_a, " endpoints", (t[-1] - t[0]) / 3)
# ---- l17 transfer: beta ----
two("l17 transfer beta 0.000234/0.000180", 0.000234 / 0.000180, float(np.float64(234) / np.float64(180)), 1e-12); print("   =", 0.000234 / 0.000180, " inverted", 0.000180 / 0.000234)
# ---- l16 quiz ----
two("l16 quiz (0,4),(10,50) at 1", interp_hand([0, 4], [10, 50], 1), interp_np([0, 4], [10, 50], 1)); two("   = 20", interp_hand([0, 4], [10, 50], 1), 20.0)
two("l16 quiz one point", interp_hand([5], [42], 9), interp_np([5], [42], 9)); two("l16 quiz times (0,3,4) 10,gap,18 at 3", interp_hand([0, 3, 4], [10, float('nan'), 18], 3), 16.0); print("  by position:", 10 + 8 / 2)
two("l16 quiz time by index", float(pd.Series([10, np.nan, 18.0], index=[0, 3, 4]).interpolate(method="index").iloc[1]), 16.0)
done()
