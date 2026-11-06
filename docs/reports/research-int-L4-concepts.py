"""Concept checks for research-int level 4 (l16 to l20, review-4, homework-4).

Run from the repo root: python3 -I docs/reports/research-int-L4-concepts.py
Every check is an assert naming its ledger row (docs/reports/audit-research-int-4-ledger.md).
A check that fails because the content is wrong is marked EXPECTED_FAIL and keeps failing; the
corrected assert sits in a comment beside it. All checks run; the script exits 1 if any failed.
"""
import math, os, sys, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "app", "content", "data")
FAILS = []


def check(name, cond, msg=""):
    try:
        assert cond, msg
        print(f"ok    {name}")
    except AssertionError as e:
        print(f"FAIL  {name}: {e}")
        FAILS.append(name)


rng = np.random.default_rng(20261106)

# ---------------------------------------------------------------- l16 interpolating
# L16-1 linear interpolation formula and the hand keys (derivation: equal slopes)
f = lambda x, x0, y0, x1, y1: y0 + (y1 - y0) * (x - x0) / (x1 - x0)
check("L16 formula keys", f(2.5, 0, 100, 10, 200) == 125 and f(2.5, 2, 25, 3, 30) == 27.5 and f(1.5, 1, 15, 2, 30) == 22.5
      and f(1, 0, 100, 4, 112) == 103 and f(1, 0, 10, 4, 50) == 20 and f(3, 0, 10, 4, 18) == 16)
# L16-2 np.interp holds the ends, one point everywhere, needs increasing xp (numpy docs)
check("L16 np.interp ends and one point", list(np.interp([0, 5], [1, 2, 3], [10, 25, 30])) == [10, 30] and np.interp(9, [5], [42]) == 42)
# L16-3 pandas interpolate: the default linear ignores the index; index/values use it; time needs a DatetimeIndex
s = pd.Series([100, np.nan, 112.0], index=[0, 1, 4])
check("L16 default linear fills by position", float(s.interpolate().iloc[1]) == 106.0)
check("L16 method=index fills by stamp", float(s.interpolate(method="index").iloc[1]) == 103.0 and float(s.interpolate(method="values").iloc[1]) == 103.0)
try:
    s.interpolate(method="time"); time_ok = False
except ValueError:
    time_ok = True
check("L16 method=time refuses an integer index", time_ok)
sd = pd.Series([100, np.nan, 112.0], index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-05"]))
check("L16 default linear ignores a DatetimeIndex too", float(sd.interpolate().iloc[1]) == 106.0 and float(sd.interpolate(method="time").iloc[1]) == 103.0)
# Finding 1: quiz q16-method explain says ONLY index or time use the stamps. slinear, polynomial and nearest read the index too.
using = set()
for m, kw in (("slinear", {}), ("polynomial", {"order": 1}), ("nearest", {})):
    v = float(s.interpolate(method=m, **kw).iloc[1])
    if v in (103.0, 100.0):
        using.add(m)
check("L16 q16-method 'only index or time read the stamps' (EXPECTED_FAIL: slinear, polynomial, nearest read the index)", using == set(),
      f"EXPECTED_FAIL methods that read the index besides index/time: {sorted(using)}")
# corrected, ready to enable: check("L16 q16-method fixed", using == {"slinear", "polynomial", "nearest"})
# L16-4 linear interpolation uses the later point; a forward fill does not (derivation: the formula holds y1)
y = pd.Series([100.0, np.nan, 112.0])
check("L16 linear fill reads the later point, ffill reads only the past", float(y.interpolate().iloc[1]) == 106.0 and float(y.ffill().iloc[1]) == 100.0)
# L16-5 ticks data counts: 312 rows, 15 blank, 12 repeated seconds, 11 pairs after the drop, 286 times
t = pd.read_csv(os.path.join(DATA, "ticks-gaps.csv"))
c = t.dropna(subset=["price"])
check("L16 ticks counts", len(t) == 312 and t.price.isna().sum() == 15 and t[t.t_sec.duplicated(keep=False)].t_sec.nunique() == 12
      and c[c.t_sec.duplicated(keep=False)].t_sec.nunique() == 11 and c.t_sec.nunique() == 286)
# L16-6 bisection interpolator equals np.interp after sort, merge by mean, drop (sim over random queries)
cl = c.groupby("t_sec", as_index=False).price.mean().sort_values("t_sec")
qs = rng.uniform(-10, 24000, 2000)
check("L16 hand bisection equals np.interp", np.allclose(np.interp(qs, cl.t_sec, cl.price), [f(q, *cl.iloc[max(0, np.searchsorted(cl.t_sec.values, q, "right") - 1)][["t_sec", "price"]].tolist(), *cl.iloc[min(len(cl) - 1, np.searchsorted(cl.t_sec.values, q, "right"))][["t_sec", "price"]].tolist()) if cl.t_sec.iloc[0] < q < cl.t_sec.iloc[-1] else (cl.price.iloc[0] if q <= cl.t_sec.iloc[0] else cl.price.iloc[-1]) for q in qs]))

# ---------------------------------------------------------------- l17 regression by group
def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
d = [1, 2, 3, 4]
check("L17 hand slopes Reed, Marsh, Plain, quiz", abs(slope(d, [10, 11, 11, 13]) - 0.9) < 1e-12 and abs(slope(d, [12, 11, 11, 10]) + 0.6) < 1e-12
      and abs(slope(d, [9, 10, 10, 9])) < 1e-12 and abs(slope(d, [5, 5, 8, 6]) - 0.6) < 1e-12)
# L17-2 S_xx for days 1..n is n(n^2-1)/12 (derivation: sum of squares about the mean of 1..n)
check("L17 Sxx closed form", all(((np.arange(1, n + 1) - (n + 1) / 2) ** 2).sum() == n * (n * n - 1) / 12 for n in (4, 50, 100)))
# L17-3 Var(slope) = sigma^2 / Sxx under independent homoskedastic noise (Wooldridge Thm 2.2): Monte Carlo, 200k reps
days = np.arange(1, 101); sxx = ((days - days.mean()) ** 2).sum()
R = 200_000
yy = 10 + 0.02 * days + rng.normal(0, 1.5, (R, 100))
sl = ((days - days.mean()) * (yy - yy.mean(axis=1, keepdims=True))).sum(axis=1) / sxx
se_mc = sl.std(ddof=1)
check("L17 SE of slope = sigma/sqrt(Sxx) = 0.0052 (MC 200k)", abs(se_mc - 1.5 / math.sqrt(sxx)) < 0.0001 and abs(se_mc - 0.15) > 0.1 and abs(se_mc - 0.015) > 0.005,
      f"mc {se_mc:.5f} theory {1.5 / math.sqrt(sxx):.5f}")
# L17-4 towns data: three routes agree; R^2 range; Wick two rows slope 0.3; four negative; Deal and Elgin inside two SE
tw = pd.read_csv(os.path.join(DATA, "towns-temp.csv"))
import statsmodels.api as sm
agree, r2, slopes = 0.0, {}, {}
for town, g in tw.groupby("town"):
    if len(g) < 3:
        wick = np.polyfit(g.day, g.temp_c, 1)[0]; continue
    b1 = g.day.cov(g.temp_c) / g.day.var(); b2 = np.polyfit(g.day, g.temp_c, 1)[0]
    fit = sm.OLS(g.temp_c, sm.add_constant(g.day)).fit()
    agree = max(agree, abs(b1 - b2), abs(b2 - fit.params.iloc[1])); r2[town] = fit.rsquared; slopes[town] = b2
check("L17 three routes agree to ten decimals", agree < 1e-10)
check("L17 R2 runs 0.0001 Deal to 0.8023 Leith", round(r2["Deal"], 4) == 0.0001 and round(r2["Leith"], 4) == 0.8023)
check("L17 Wick two rows give 0.3, three times Leith", abs(wick - 0.3) < 1e-9 and abs(wick / slopes["Leith"] - 3) < 0.01)
check("L17 four negative slopes; Deal and Elgin inside two SE, ten outside", sum(v < 0 for v in slopes.values()) == 4
      and sum(abs(v) < 2 * 1.5 / math.sqrt(sxx) for v in slopes.values()) == 2)
# L17-5 Wick's slope under the lesson's sigma: SE = 1.5/sqrt(0.5) = 2.12, so 0.3 is 0.14 SE from zero (no evidence)
check("L17 Wick slope is 0.14 SE from zero", abs(0.3 / (1.5 / math.sqrt(0.5)) - 0.1414) < 0.001)
# L17-6 groupby.apply with a scalar per group returns a Series indexed by group (pandas docs)
df = pd.DataFrame({"town": ["a"] * 3 + ["b"] * 2, "day": [1, 2, 3, 1, 2], "temp_c": [1.0, 2.0, 4.0, 5.0, 9.0]})
res = df.groupby("town").apply(lambda g: np.polyfit(g["day"], g["temp_c"], 1)[0], include_groups=False)
check("L17 apply returns a Series per group", isinstance(res, pd.Series) and list(res.index) == ["a", "b"] and abs(res["a"] - 1.5) < 1e-12)
# L17-7 two points: R^2 = 1 (derivation: zero residuals)
check("L17 two-point R2 is 1", abs(np.corrcoef([1, 2], [3, 7])[0, 1] ** 2 - 1) < 1e-12)
# L17-8 groupby sums give the same slope as polyfit (vectorised route of the follow-up)
gs = tw.groupby("town").agg(n=("day", "size"), sx=("day", "sum"), sy=("temp_c", "sum"), sxy=("day", lambda s: (s * tw.loc[s.index, "temp_c"]).sum()), sxx=("day", lambda s: (s * s).sum()))
vec = (gs.n * gs.sxy - gs.sx * gs.sy) / (gs.n * gs.sxx - gs.sx ** 2)
check("L17 vectorised sums equal polyfit", all(abs(vec[k] - v) < 1e-9 for k, v in slopes.items()))
# L17-9 beta = cov/var
check("L17 beta 0.000234/0.000180", abs(0.000234 / 0.000180 - 1.3) < 1e-12)
# L17-10 np.cov (ddof 1) over np.var (ddof 0) is off by n/(n-1) (review r4-beta-per-stock)
m, r = rng.normal(size=30), rng.normal(size=30)
check("R4 np.cov/np.var ratio n/(n-1)", abs((np.cov(m, r)[0, 1] / np.var(m)) / (np.cov(m, r)[0, 1] / pd.Series(m).var()) - 30 / 29) < 1e-12)

# ---------------------------------------------------------------- l18 updating a fit
def sums_slope(n, sx, sy, sxx, sxy):
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)
check("L18 running-sum keys", abs(sums_slope(4, 10, 14, 30, 39) - 0.8) < 1e-12 and abs(sums_slope(5, 15, 22, 55, 79) - 1.3) < 1e-12
      and abs(sums_slope(4, 14, 20, 54, 77) - 1.4) < 1e-12 and abs(sums_slope(250, 25, 37, 585, 726) - 1.24) < 1e-12
      and abs(sums_slope(251, 23, 34, 589, 732) - 1.2419) < 0.0001 and abs(sums_slope(3, 6, 9, 14, 19) - 0.5) < 1e-12
      and abs(sums_slope(4, 10, 17, 30, 51) - 1.7) < 1e-12 and abs(sums_slope(5, 20, 30, 90, 141) - 2.1) < 1e-12
      and abs(sums_slope(4, 22, 34, 126, 197) - 2.0) < 1e-12)
# L18-2 sums slope equals polyfit on the points (derivation from the normal equations, Wooldridge App 2A)
pts = [(1, 2), (2, 3), (3, 5), (4, 4)]
check("L18 sums equal polyfit", abs(sums_slope(4, 10, 14, 30, 39) - np.polyfit(*zip(*pts), 1)[0]) < 1e-12)
# L18-3 Sherman-Morrison update equals the refit (numbers of screen 4 and a random design)
X = np.c_[np.ones(4), [1, 2, 3, 4]]; P = np.linalg.inv(X.T @ X); x = np.array([1.0, 5.0]); b = np.linalg.lstsq(X, [2, 3, 5, 4], rcond=None)[0]
check("L18 P and 1 + x'Px = 2.5, innovation 2.5", np.allclose(P, [[1.5, -0.5], [-0.5, 0.2]]) and abs(1 + x @ P @ x - 2.5) < 1e-12 and abs(8 - x @ b - 2.5) < 1e-12)
Pn = P - np.outer(P @ x, P @ x) / (1 + x @ P @ x); bn = b + Pn @ x * (8 - x @ b)
X5 = np.vstack([X, x]); check("L18 rank-one update equals refit", np.allclose(Pn, np.linalg.inv(X5.T @ X5)) and np.allclose(bn, [0.5, 1.3]))
# L18-4 Sherman-Morrison downdate with the NEW P (homework h4-online-ols) equals the refit, random design, add then remove
Xr = np.c_[np.ones(60), rng.normal(size=(60, 2))]; yr = Xr @ [1, 2, -1] + rng.normal(size=60)
Pm = np.linalg.inv(Xr.T @ Xr); bm = Pm @ Xr.T @ yr
for i in range(10):
    xi, yi = Xr[i], yr[i]; Px = Pm @ xi; Pm = Pm + np.outer(Px, Px) / (1 - xi @ Px); bm = bm - (Pm @ xi) * (yi - xi @ bm)
check("H4 downdate b -= P_new x (y - x'b) equals refit", np.allclose(bm, np.linalg.lstsq(Xr[10:], yr[10:], rcond=None)[0]))
# L18-5 float64 trap: naive variance returns exactly 0.0 for 1e9+1..3 and 2.6667 for 1e8+1..4 (review)
def naive_var(xs):
    n = len(xs); return (sum(x * x for x in xs) - sum(xs) ** 2 / n) / (n - 1)
check("L18 naive variance 1e9 case is 0.0", naive_var([1e9 + 1, 1e9 + 2, 1e9 + 3]) == 0.0)
check("R4 naive variance 1e8 case is 2.6667 (true 1.6667)", abs(naive_var([1e8 + 1, 1e8 + 2, 1e8 + 3, 1e8 + 4]) - 2.6667) < 0.0005 and abs(np.var([1, 2, 3, 4], ddof=1) - 1.6667) < 0.0005)
check("L18 rounding step of the two big terms is 512", np.spacing(3e18) == 512.0)
# L18-6 centring: slope unchanged, intercept a' - mc (algebra); the lesson's numbers
u = np.array([1, 2, 3.0]); yv = np.array([1, 3, 2.0]); mm, a1 = np.polyfit(u, yv, 1)
check("L18 centre-first numbers", abs(mm - 0.5) < 1e-12 and abs(a1 - 1) < 1e-12 and abs((a1 - mm * 1e9) + 499_999_999) < 1e-6)
# Finding 3: the distractor 'subtract c from y as well' is said to leave the huge x^2 sums. With x shifted too it does not: the fit is exact.
xs = np.array([1e9 + 1, 1e9 + 2, 1e9 + 3]); cshift = 1e9
m_both = sums_slope(3, (xs - cshift).sum(), (yv - cshift).sum(), ((xs - cshift) ** 2).sum(), ((xs - cshift) * (yv - cshift)).sum())
check("L18 derive distractor x 'shifting y as well leaves the x^2 sums' (EXPECTED_FAIL: with x shifted too the slope is exact)", abs(m_both - 0.5) > 1e-6,
      f"EXPECTED_FAIL slope with both columns shifted is {m_both}, exact; the why only holds for shifting y instead of x")
# corrected, ready to enable: check("L18 derive distractor x fixed wording", abs(m_both - 0.5) < 1e-9)
# L18-7 OnlineLine: den == 0 only when the sums are exact. Finding 4 (MC over repeated non-integer x)
def coef(xy):
    n = len(xy); sx = sum(x for x, _ in xy); sy = sum(y for _, y in xy); sxx = sum(x * x for x, _ in xy); sxy = sum(x * y for x, y in xy)
    den = n * sxx - sx ** 2
    if n < 2 or den == 0:
        return [float("nan"), float("nan")]
    bb = (n * sxy - sx * sy) / den; return [(sy - bb * sx) / n, bb]
bad = 0; worst = 0.0
for _ in range(20000):
    xv = float(rng.uniform(0.01, 10)); k = int(rng.integers(2, 6)); cc = coef([(xv, float(rng.normal())) for _ in range(k)])
    if not math.isnan(cc[1]):
        bad += 1; worst = max(worst, abs(cc[1]))
check("L18 OnlineLine 'NaN when every x is equal' (EXPECTED_FAIL: den == 0 fails for about 28% of non-integer x)", bad == 0,
      f"EXPECTED_FAIL {bad / 20000:.3f} of repeated-x cases return a number (largest slope {worst:.3g}) instead of NaN")
# corrected, ready to enable (den <= 1e-12 * n * sxx):
# def coef_fixed(xy): ... if n < 2 or den <= 1e-12 * n * sxx: return [nan, nan]; check("L18 OnlineLine guard fixed", bad_fixed == 0)
# L18-8 the raw-sum class on x near 1e9 (Finding 5): the slope comes out wrong where the centred fit is exact
check("L18 raw-sum class fails on x near 1e9 where centring is exact", math.isnan(coef(list(zip(xs, yv)))[1]) or abs(coef(list(zip(xs, yv)))[1] - 0.5) > 1e-3)
# L18-9 remove a row never added: sums shift silently (sim)
cc1 = coef([(1, 2), (2, 3), (3, 5), (4, 4)]); n, sx, sy, sxx, sxy = 4, 10, 14, 30, 39
n, sx, sy, sxx, sxy = n - 1, sx - 7, sy - 9, sxx - 49, sxy - 63
check("L18 removing (7, 9) never added gives a different slope with no error", abs(sums_slope(n, sx, sy, sxx, sxy) - cc1[1]) > 0.01)
# L18-10 forgetting factor: scaling the sums by lambda gives weights lambda^k, equal to weighted least squares (Haykin, RLS)
lam, T = 0.99, 300; xf = rng.normal(size=T); yf = 1 + 2 * xf + rng.normal(size=T)
S = np.zeros((2, 2)); cvec = np.zeros(2)
for k in range(T):
    xt = np.array([1, xf[k]]); S = lam * S + np.outer(xt, xt); cvec = lam * cvec + xt * yf[k]
w = lam ** np.arange(T - 1, -1, -1); Xd = np.c_[np.ones(T), xf]
check("L18 forgetting factor equals WLS with weights lambda^k", np.allclose(np.linalg.solve(S, cvec), np.linalg.solve(Xd.T @ (w[:, None] * Xd), Xd.T @ (w * yf))))
# L18-11 cost ratio np^2 / p^2 = n
check("L18 update is n times cheaper", (1e4 * 25) / 25 == 1e4)

# ---------------------------------------------------------------- l19 timed data task
o = pd.read_csv(os.path.join(DATA, "orders-messy.csv"), dtype={"qty": str})
raw = o.copy()
o["symbol"] = o.symbol.str.strip().str.upper(); o["qty"] = o.qty.str.replace(",", "").astype(int)
check("L19 15 repeated ids, 12 exact copies before text cleaning, 15 after", raw.order_id.duplicated().sum() == 15 and raw.duplicated().sum() == 12 and o.duplicated().sum() == 15)
a = o.drop_duplicates("order_id"); a = a[a.price.notna() & (a.price > 0)]
bpr = o[o.price.notna() & (o.price > 0)].drop_duplicates("order_id")
check("L19 600 -> 585 -> 570, order of ids and prices immaterial on the file", len(o) == 600 and len(o.drop_duplicates("order_id")) == 585 and len(a) == 570 and len(bpr) == 570
      and o.price.isna().sum() == 10 and (o.price < 0).sum() == 5)
# Finding 6: the tiny-orders test keeps the first copy of id 7 (blank price) and so loses the order, though a later copy has a good price
tiny = pd.DataFrame({"order_id": [7, 7], "price": [np.nan, 8.0]})
kept_ids_then_prices = tiny.drop_duplicates("order_id").dropna(subset=["price"]).order_id.tolist()
kept_prices_then_ids = tiny.dropna(subset=["price"]).drop_duplicates("order_id").order_id.tolist()
check("L19 load_clean tiny case 'first copy kept even when its price is bad' (EXPECTED_FAIL: a recoverable order is dropped)", kept_ids_then_prices == [7],
      f"EXPECTED_FAIL ids-then-prices keeps {kept_ids_then_prices}, prices-then-ids keeps {kept_prices_then_ids}")
# corrected, ready to enable once the order is prices then ids: check("L19 tiny case keeps order 7", kept_prices_then_ids == [7])
# L19-3 VWAP definition and the stated figures; leaving in -999 and repeats drags ALPHA to 46.3874
def vw(d): return (d.price * d.qty).groupby(d.symbol).sum() / d.groupby("symbol").qty.sum()
check("L19 VWAPs", np.allclose(vw(a).values, [50.0152, 120.0146, 8.0005], atol=5e-5) and abs(vw(o[o.price.notna()])["ALPHA"] - 46.3874) < 5e-5)
check("L19 VWAP is not the simple mean", abs(vw(a)["ALPHA"] - a[a.symbol == "ALPHA"].price.mean()) > 1e-4)
# L19-4 a NaN price row still counts in the quantity total (pandas sum skips NaN; the denominator keeps the row)
d3 = pd.DataFrame({"symbol": ["x", "x"], "qty": [100, 100], "price": [10.0, np.nan]})
check("L19 NaN price biases the VWAP down", float(vw(d3).iloc[0]) == 5.0)
# L19-5 slippage model: polyfit slope, R2 = corr^2 for one regressor with intercept, SE 0.0486, mean 3.795
side = np.where(a.side == "B", 1.0, -1.0); slip = side * (a.price - a.mid) / a.mid * 1e4; xl = np.log(a.qty / 100)
fit = sm.OLS(slip, sm.add_constant(xl)).fit()
check("L19 slope 1.2421, SE 0.0486, R2 = corr^2 = 0.5346, mean 3.795", abs(fit.params.iloc[1] - 1.2421) < 5e-5 and abs(fit.bse.iloc[1] - 0.0486) < 5e-5
      and abs(fit.rsquared - np.corrcoef(xl, slip)[0, 1] ** 2) < 1e-12 and abs(fit.rsquared - 0.5346) < 5e-5 and abs(slip.mean() - 3.795) < 5e-4)
# L19-6 sign convention: seller at 49.80 against 50 is +40 bp; a zero price is 10,000 bp in size
check("L19 sign of slippage", abs(-1 * (49.80 - 50) / 50 * 1e4 - 40) < 1e-9 and abs(1 * (0 - 50) / 50 * 1e4) == 1e4)
# L19-7 prediction 3,200 shares and the slips; review 800 shares
check("L19 predictions", abs(0.3375 + 1.2421 * math.log(32) - 4.642) < 1e-3 and abs(0.3375 + 1.2421 * 32 - 40.08) < 0.01 and abs(0.3375 + 1.2421 * math.log(3200) - 10.362) < 0.01
      and abs(0.4 + 1.35 * math.log(8) - 3.2072) < 1e-4)
# L19-8 VWAP transfer and quiz; the repeat overstates by 4.8p
check("L19 fills VWAP", abs((2000 * 31.2 + 1500 * 31.4 + 500 * 30.8) / 4000 - 31.225) < 1e-9 and abs((2000 * 31.2 + 3000 * 31.4 + 500 * 30.8) / 5500 - 31.2727) < 5e-5
      and abs((200 * 10 + 600 * 10.4) / 800 - 10.3) < 1e-9)
# L19-9 drop_duplicates compares every column, finds non-adjacent rows, needs no sort (pandas docs)
d2 = pd.DataFrame({"id": [1, 2, 1, 3], "sym": ["alpha", "B", "ALPHA ", "B"]})
check("L19 drop_duplicates semantics", len(d2.drop_duplicates()) == 4 and len(d2.drop_duplicates("id")) == 3 and len(pd.DataFrame({"a": [1, 2, 1]}).drop_duplicates()) == 2)

# ---------------------------------------------------------------- l20 writing a take-home
h = pd.read_csv(os.path.join(DATA, "houses.csv"))
big = h[h.price_k > 5000].price_k
check("L20 four prices typed in pounds, repairable by /1000 into the usual range", len(big) == 4 and all((big / 1000).between(h.price_k[h.price_k <= 5000].min(), h.price_k[h.price_k <= 5000].max())))
dd = h[h.price_k <= 5000].sort_values("id"); p = dd.price_k.to_numpy(float); err = p - p.mean()
g0 = np.random.default_rng(0); idx = g0.integers(0, len(p), (2000, len(p)))
draws = np.sqrt((err[idx] ** 2).mean(axis=1)); lo, hi = np.percentile(draws, [2.5, 97.5])
check("L20 report numbers n 396, rmse 82.90, interval 77.45 to 88.22", len(p) == 396 and abs(np.sqrt((err ** 2).mean()) - 82.8998) < 5e-4 and abs(lo - 77.452) < 5e-3 and abs(hi - 88.225) < 5e-3)
# Finding 7: repairing instead of dropping keeps 400 homes
rep = h.copy(); rep.loc[rep.price_k > 5000, "price_k"] /= 1000
check("L20 make_report drops four repairable rows (EXPECTED_FAIL: the level's rule is repair first, drop only what cannot be repaired)", len(p) == 400,
      f"EXPECTED_FAIL dropped n={len(p)}, repaired n={len(rep)}, mean {rep.price_k.mean():.4f}, rmse {np.sqrt(((rep.price_k - rep.price_k.mean()) ** 2).mean()):.4f}")
# corrected, ready to enable once the item repairs: check("L20 repaired report", len(rep) == 400 and abs(rep.price_k.mean() - 307.416) < 1e-3)
# Finding 8: the draws keep the mean fixed; recentring inside each resample moves the ends by about 0.1
pi = p[idx]; d2r = np.sqrt(((pi - pi.mean(axis=1, keepdims=True)) ** 2).mean(axis=1)); lo2, hi2 = np.percentile(d2r, [2.5, 97.5])
check("L20 recentred bootstrap differs from the fixed-mean one by under 0.2 (size of the imprecision)", 0.01 < max(abs(lo - lo2), abs(hi - hi2)) < 0.2, f"{lo2:.3f} {hi2:.3f}")
# L20-3 width 10.77 is about four sd of the draws (2.76); 50 draws below the lower end
check("L20 width and sd", abs(hi - lo - 10.77) < 0.02 and abs(draws.std(ddof=1) - 2.76) < 0.01 and (draws < lo).sum() == 50)
# L20-4 loop and vectorised integer draws read the same stream (sim, several n and ranges)
same = True
for nn in (396, 5, 7, 1000, 2 ** 31 + 5):
    r1 = np.random.default_rng(0).integers(0, nn, (30, 9 if nn > 10000 else nn)); g2 = np.random.default_rng(0)
    same &= bool((r1 == np.array([g2.integers(0, nn, r1.shape[1]) for _ in range(30)])).all())
check("L20 loop equals vectorised draws, same seed", same)
check("L20 a different seed changes the draws", not np.array_equal(np.random.default_rng(1).integers(0, 396, 50), np.random.default_rng(0).integers(0, 396, 50)))
# L20-5 draws pick positions: sorting by price changes the interval; sorting by id makes a shuffle harmless
ps = np.sort(p); d3 = np.sqrt((((ps - ps.mean())[idx]) ** 2).mean(axis=1))
check("L20 sort by price changes the interval; shuffled rows sorted by id do not", abs(np.percentile(d3, 2.5) - lo) > 1e-6
      and np.array_equal(h[h.price_k <= 5000].sample(frac=1, random_state=1).sort_values("id").price_k.values, dd.price_k.values))
# L20-6 95% interval from +-1.96 SE; t(568) is 1.964
from scipy import stats
check("L20 slope interval 1.1468 to 1.3374, t(568) near 1.96", abs(1.2421 - 1.96 * 0.0486 - 1.1468) < 1e-4 and abs(1.2421 + 1.96 * 0.0486 - 1.3374) < 1e-4 and abs(stats.t.ppf(0.975, 568) - 1.96) < 0.01)
# L20-7 quiz: 2.5% of 2000 = 50; widths
check("L20 quiz numbers", 0.025 * 2000 == 50 and abs(52.8 - 41.2 - 11.6) < 1e-9)
# L20-8 homework writeup: interval 0.71 to 1.19, 5,000 shares 4.02 bp, 851 rows
check("H4 writeup numbers", abs(0.95 - 1.96 * 0.12 - 0.7148) < 1e-3 and abs(0.95 + 1.96 * 0.12 - 1.1852) < 1e-3 and abs(0.30 + 0.95 * math.log(50) - 4.02) < 5e-3 and 900 - 24 - 18 - 7 == 851)

# ---------------------------------------------------------------- review-4 and homework-4 remaining
check("R4 slope ratios: four beyond two SE", sum(abs(s_ / e_) > 2 for s_, e_ in [(0.020, 0.0075), (-0.004, 0.0075), (0.550, 0.3162), (-0.017, 0.0075), (0.090, 0.0388), (0.016, 0.0075)]) == 4)
check("R4 rows left 749 (union of removals)", 800 - (20 + 36 - 5) == 749)
check("R4 interp keys", f(4, 3, 26, 5, 50) == 38 and f(4, 5, 50, 1, 20) == 42.5 and f(2, 0, 50, 8, 62) == 53)
# H4 rates-gaps: 14 NA, 186 quotes, 5 to 479, 16 grid points, longest gap 14 (12 if NA rows counted)
rg = pd.read_csv(os.path.join(DATA, "research-int", "rates-gaps.csv")); q = rg.dropna(subset=["rate"]).sort_values("minute")
check("H4 rates-gaps counts and gaps", rg.rate.isna().sum() == 14 and len(q) == 186 and (q.minute.iloc[0], q.minute.iloc[-1]) == (5, 479)
      and len(np.arange(5, 480, 30)) == 16 and q.minute.diff().max() == 14 and rg.sort_values("minute").minute.diff().max() == 12)
# H4 lakes: SE = sqrt(s^2/Sxx) with n-2 df (Wooldridge 2.5); six lakes with |t| > 2 in order; Tarn 4 rows
lk = pd.read_csv(os.path.join(DATA, "research-int", "lakes-level.csv")); tv = {}
for lake, g in lk.groupby("lake"):
    if len(g) < 5:
        tarn = len(g); continue
    x_, y_ = g.year.to_numpy(float), g.level_m.to_numpy(float); sxx_ = ((x_ - x_.mean()) ** 2).sum(); b_ = ((x_ - x_.mean()) * (y_ - y_.mean())).sum() / sxx_
    s2 = ((y_ - (y_.mean() - b_ * x_.mean()) - b_ * x_) ** 2).sum() / (len(g) - 2); se_ = math.sqrt(s2 / sxx_)
    fit_ = sm.OLS(y_, sm.add_constant(x_)).fit(); assert abs(se_ - fit_.bse[1]) < 1e-12; tv[lake] = b_ / se_
order = [k for k, _ in sorted(tv.items(), key=lambda kv: -abs(kv[1])) if abs(tv[k]) > 2]
check("H4 lakes: hand SE equals statsmodels, six clear trends in order, Tarn 4 rows", order == ["Ard", "Gill", "Isla", "Esk", "Fyne", "Dee"] and tarn == 4 and abs(tv["Ard"] + 9.275) < 1e-3)
# H4 OnlineOLS: P0 = 1e8 I is ridge with lambda 1e-8; 20,000 rows stay within 1e-6 of lstsq
class OnlineOLS:
    def __init__(self, p): self.P = np.eye(p) * 1e8; self.b = np.zeros(p)
    def add(self, x, y):
        x = np.asarray(x, float); Px = self.P @ x; self.P = self.P - np.outer(Px, Px) / (1.0 + x @ Px); self.b = self.b + (self.P @ x) * (y - x @ self.b)
X4 = np.c_[np.ones(4), [1, 2, 3, 4]]; y4 = np.array([4, 6, 9, 10.0]); mo = OnlineOLS(2)
for i in range(4): mo.add(X4[i], y4[i])
check("H4 ridge start equals OLS to 1e-6, exact ridge(1e-8) to 1e-7", np.abs(mo.b - np.linalg.lstsq(X4, y4, rcond=None)[0]).max() < 1e-6
      and np.abs(mo.b - np.linalg.solve(X4.T @ X4 + 1e-8 * np.eye(2), X4.T @ y4)).max() < 1e-7)
g3 = np.random.default_rng(3); Xb = np.c_[np.ones(20000), g3.normal(size=(20000, 2))]; yb = Xb @ [1.0, 2.0, -1.0] + g3.normal(size=20000); mb = OnlineOLS(3)
for i in range(20000): mb.add(Xb[i], yb[i])
check("H4 20,000 rank-one updates stay within 1e-6 of lstsq", np.abs(mb.b - np.linalg.lstsq(Xb, yb, rcond=None)[0]).max() < 1e-6)
# H4 VWAP table and SE for fifty days
check("H4 vwap table", abs((300 * 20.10 + 500 * 20.30 + 200 * 19.90) / 1000 - 20.16) < 1e-9 and abs((100 * 55 + 400 * 55.5 + 300 * 54.9) / 800 - 55.2125) < 1e-9)
check("H4 SE fifty days", abs(50 * 2499 / 12 - 10412.5) < 1e-9 and abs(2.0 / math.sqrt(10412.5) - 0.0196) < 5e-5)
# H4 clean_fills: on the file the later row of an id is also the later time, so 'later' is unambiguous
fl = pd.read_csv(os.path.join(DATA, "research-int", "fills-messy.csv"), dtype=str); tt = fl.time.str.split(":", expand=True).astype(int); fl["secs"] = tt[0] * 3600 + tt[1] * 60 + tt[2]
fl["pos"] = range(len(fl)); conflict = any(not gg.sort_values("pos").secs.is_monotonic_increasing for _, gg in fl[fl.fill_id.duplicated(keep=False)].groupby("fill_id"))
check("H4 fills: file order agrees with time order inside every repeated id; 380 ids, 10 cancelled", not conflict and fl.fill_id.nunique() == 380 and (fl.status == "CANCELLED").sum() == 10)

print()
print(f"{len(FAILS)} failing check(s)" + (": " + "; ".join(FAILS) if FAILS else ""))
sys.exit(1 if FAILS else 0)
