"""research-int level 4: l16 interpolation, l17 per-group regression, l18 updating a fit, l19 timed data task, l20 take-home."""
import math, bisect
from fractions import Fraction as F
import numpy as np, pandas as pd
import statsmodels.api as sm
from chk import two, done

# ---------- l16 ----------
def interp_hand(xs, ys, x):
    """Method A: sort, average duplicates, drop NaN ys, clamp at the edges, bisect for the bracket."""
    pts = {}
    for a, b in zip(xs, ys):
        if b is not None and not (isinstance(b, float) and math.isnan(b)): pts.setdefault(a, []).append(b)
    ks = sorted(pts); vs = [sum(pts[k])/len(pts[k]) for k in ks]
    if x <= ks[0]: return vs[0]
    if x >= ks[-1]: return vs[-1]
    j = bisect.bisect_right(ks, x)
    if ks[j-1] == x: return vs[j-1]
    x0, x1, y0, y1 = ks[j-1], ks[j], vs[j-1], vs[j]; return y0 + (y1-y0)*(x-x0)/(x1-x0)
def interp_np(xs, ys, x):
    df = pd.DataFrame({"x": xs, "y": ys}).dropna().groupby("x", as_index=False).y.mean().sort_values("x")
    return float(np.interp(x, df.x, df.y))
cases = [([0, 10], [100, 200], 2.5, 125.0), ([3, 1, 2], [30, 10, 25], 2.5, 27.5), ([3, 1, 2], [30, 10, 25], 1.2, 13.0),
         ([3, 1, 2], [30, 10, 25], 0, 10.0), ([3, 1, 2], [30, 10, 25], 5, 30.0), ([1, 1, 2], [10, 20, 30], 1.5, 22.5), ([1, 1, 2], [10, 20, 30], 1, 15.0),
         ([0, 1, 4], [100.0, float("nan"), 112.0], 1, 103.0), ([0, 1, 2], [5.0, 7.0, float("nan")], 1.5, 7.0)]
for xs, ys, x, want in cases:
    two(f"l16 interp xs={xs} ys={ys} x={x}", interp_hand(xs, ys, x), interp_np(xs, ys, x), 1e-12); two("   equals stated value", interp_hand(xs, ys, x), want, 1e-12)
s = pd.Series([100, np.nan, np.nan, 112.0]); two("l16 gap fill by position", float(s.interpolate().iloc[1]), 104.0); two("l16 gap fill second", float(s.interpolate().iloc[2]), 108.0)
by_pos = float(pd.Series([100, np.nan, 112.0]).interpolate().iloc[1]); by_time = float(pd.Series([100, np.nan, 112.0], index=[0, 1, 4]).interpolate(method="index").iloc[1])
two("l16 by position", by_pos, 106.0); two("l16 by time", by_time, 103.0)
tk = pd.read_csv("data/ticks-gaps.csv"); print("     ticks rows", len(tk), "blank prices", int(tk.price.isna().sum()), "duplicate t_sec rows", int(tk.t_sec.duplicated(keep=False).sum()))
clean = tk.dropna(subset=["price"]).groupby("t_sec", as_index=False).price.mean().sort_values("t_sec")
print("     clean rows", len(clean))
for tq in (12000, 100, 23000):
    two(f"l16 ticks value at t={tq}", interp_hand(tk.t_sec.tolist(), tk.price.tolist(), tq), interp_np(tk.t_sec, tk.price, tq), 1e-9)
    print("       ->", round(interp_hand(tk.t_sec.tolist(), tk.price.tolist(), tq), 5))
print("     first/last clean t", int(clean.t_sec.iloc[0]), int(clean.t_sec.iloc[-1]), " price there", round(float(clean.price.iloc[0]), 4), round(float(clean.price.iloc[-1]), 4))

# ---------- l17 ----------
tt = pd.read_csv("data/towns-temp.csv")
def slope_cov(g): 
    if len(g) < 3 or g.day.nunique() < 2: return pd.Series({"slope": np.nan, "intercept": np.nan, "r2": np.nan, "n": len(g)})
    c = np.cov(g.day, g.temp_c, ddof=1); m = c[0, 1]/c[0, 0]; r = c[0, 1]/math.sqrt(c[0, 0]*c[1, 1])
    return pd.Series({"slope": m, "intercept": g.temp_c.mean()-m*g.day.mean(), "r2": r*r, "n": len(g)})
def slope_sm(g):
    if len(g) < 3: return pd.Series({"slope": np.nan, "intercept": np.nan, "r2": np.nan, "n": len(g)})
    f = sm.OLS(g.temp_c, sm.add_constant(g.day.astype(float))).fit(); return pd.Series({"slope": f.params["day"], "intercept": f.params["const"], "r2": f.rsquared, "n": len(g)})
A = tt.groupby("town").apply(slope_cov, include_groups=False); B = tt.groupby("town").apply(slope_sm, include_groups=False)
pf = {t: (np.polyfit(g.day, g.temp_c, 1) if len(g) >= 3 else (np.nan, np.nan)) for t, g in tt.groupby("town")}
for t in A.index:
    if t == "Wick": two("l17 Wick slope NaN both", float(np.isnan(A.loc[t, "slope"]) and np.isnan(B.loc[t, "slope"])), 1.0); continue
    two(f"l17 {t} slope cov/var vs statsmodels", float(A.loc[t, "slope"]), float(B.loc[t, "slope"]), 1e-10); two(f"l17 {t} slope vs polyfit", float(A.loc[t, "slope"]), float(pf[t][0]), 1e-10)
    two(f"l17 {t} r2", float(A.loc[t, "r2"]), float(B.loc[t, "r2"]), 1e-10)
print(A.round(4).to_string())
print("     towns:", len(A), " rows", len(tt), " negative slopes:", int((A.slope < 0).sum()), " steepest:", A.slope.idxmax(), round(A.slope.max(), 4), " shallowest:", A.slope.idxmin(), round(A.slope.min(), 4))
print("     two-point town slope if not guarded:", (9.4-9.1)/(2-1))
sx = math.sqrt(100*(100**2-1)/12); print("     se of slope with sigma 1.5:", round(1.5/sx, 5), "(Sxx", round(sx**2, 1), ")")
print("     mean slope across towns", round(float(A.slope.mean()), 5), " planted mean", round(float(np.mean(np.linspace(-0.04, 0.10, 12))), 5))

# ---------- l18 ----------
pts = [(1, 2), (2, 3), (3, 5), (4, 4)]
def stats_of(P):
    n = len(P); sx = sum(F(a) for a, _ in P); sy = sum(F(b) for _, b in P); sxx = sum(F(a)**2 for a, _ in P); sxy = sum(F(a)*F(b) for a, b in P); return n, sx, sy, sxx, sxy
def fit_from(st):
    n, sx, sy, sxx, sxy = st; m = (n*sxy-sx*sy)/(n*sxx-sx**2); return m, (sy-m*sx)/n
def fit_np(P): a = np.array(P, float); c = np.polyfit(a[:, 0], a[:, 1], 1); return float(c[0]), float(c[1])
for label, P in [("4 pts", pts), ("add (5,8)", pts+[(5, 8)]), ("then remove (1,2)", pts[1:]+[(5, 8)])]:
    m, b = fit_from(stats_of(P)); m2, b2 = fit_np(P); two(f"l18 {label} slope", float(m), m2, 1e-12); two(f"l18 {label} intercept", float(b), b2, 1e-12); print(f"       {label}: stats {stats_of(P)} slope {m} intercept {b}")
# running update of the statistics = same as refit
st = list(stats_of(pts)); st = [st[0]+1, st[1]+5, st[2]+8, st[3]+25, st[4]+40]; two("l18 updated slope from running sums", float(fit_from(tuple(st))[0]), 1.3, 1e-12)
st = [st[0]-1, st[1]-1, st[2]-2, st[3]-1, st[4]-2]; two("l18 downdated slope", float(fit_from(tuple(st))[0]), 1.4, 1e-12); two("l18 downdated intercept", float(fit_from(tuple(st))[1]), 0.1, 1e-12)
# Sherman-Morrison on the same problem, design [1, x]
def design(P): return np.array([[1.0, a] for a, _ in P]), np.array([b for _, b in P], float)
X, y = design(pts); Pm = np.linalg.inv(X.T@X); beta = Pm@X.T@y
two("l18 base beta", float(beta[1]), 0.8, 1e-12); print("       (X'X)^-1 =", Pm.round(4).tolist(), " X'X =", (X.T@X).tolist())
xn = np.array([1.0, 5.0]); yn = 8.0
Pn = Pm - np.outer(Pm@xn, xn@Pm)/(1+xn@Pm@xn); bn = beta + Pn@xn*(yn - xn@beta)
X2, y2 = design(pts+[(5, 8)]); b_ref = np.linalg.lstsq(X2, y2, rcond=None)[0]
two("l18 Sherman-Morrison beta slope", float(bn[1]), float(b_ref[1]), 1e-12); two("l18 Sherman-Morrison beta intercept", float(bn[0]), float(b_ref[0]), 1e-12)
print("       gain denominator 1 + x'Px =", round(1+xn@Pm@xn, 4), " innovation y - x'beta =", yn-xn@beta, " new P =", Pn.round(4).tolist())
xr = np.array([1.0, 1.0]); yr = 2.0; Pd = Pn + np.outer(Pn@xr, xr@Pn)/(1-xr@Pn@xr); bd = bn - Pd@xr*(yr - xr@bn)/1.0
# downdate exact form: beta_new = beta - P_new x (y - x'beta)  with P_new from the downdated inverse; check against refit
Pd2 = Pn + np.outer(Pn@xr, xr@Pn)/(1-xr@Pn@xr); bd2 = bn - Pd2@xr*(yr - xr@bn)
X3, y3 = design(pts[1:]+[(5, 8)]); b3 = np.linalg.lstsq(X3, y3, rcond=None)[0]
two("l18 downdate slope via Sherman-Morrison", float(bd2[1]), float(b3[1]), 1e-12); two("l18 downdate intercept", float(bd2[0]), float(b3[0]), 1e-12)
two("l18 refit cost / update cost, n=1e6 p=10 (n p^2 / p^2)", 1e6*100/100, 1e6)
# numerical stability
xs = [1e9+1, 1e9+2, 1e9+3]; n = 3
naive = (sum(v*v for v in xs) - sum(xs)**2/n)/(n-1)
exact = float((sum(F(v)**2 for v in xs) - sum(F(v) for v in xs)**2/n)/(n-1))
welford = float(np.var(xs, ddof=1)); two("l18 exact variance of 1e9+[1,2,3] is 1", exact, 1.0, 1e-12); two("l18 centred (np.var) gives 1", welford, 1.0, 1e-9)
print("       naive sum-of-squares variance in float64:", naive, "(exact 1.0)")
xs2 = [1e5+1, 1e5+2, 1e5+3]; naive2 = (sum(v*v for v in xs2) - sum(xs2)**2/3)/2; print("       with 1e5 offset naive:", naive2)

# ---------- l19 ----------
od = pd.read_csv("data/orders-messy.csv", dtype={"qty": str})
print("     raw rows", len(od), " dup order_id rows", int(od.order_id.duplicated().sum()), " exact duplicate rows before cleaning", int(od.duplicated().sum()),
      " qty with comma", int(od.qty.str.contains(",").sum()), " blank price", int(od.price.isna().sum()), " price -999", int((od.price == -999).sum()))
print("     symbols raw:", sorted(od.symbol.unique()))
def clean_a(df):
    d = df.copy(); d["symbol"] = d.symbol.str.strip().str.upper(); d["qty"] = d.qty.str.replace(",", "").astype(int)
    d = d.drop_duplicates("order_id"); d = d[d.price.notna() & (d.price > 0)]; return d.reset_index(drop=True)
def clean_b(df):
    rows = []; seen = set()
    for r in df.itertuples():
        if r.order_id in seen: continue
        seen.add(r.order_id); p = r.price
        if p is None or math.isnan(p) or p <= 0: continue
        rows.append((r.order_id, r.symbol.strip().upper(), r.side, int(r.qty.replace(",", "")), p, r.mid))
    return pd.DataFrame(rows, columns=["order_id", "symbol", "side", "qty", "price", "mid"])
ca, cb = clean_a(od), clean_b(od)
two("l19 clean rows (pandas vs loop)", len(ca), len(cb)); print("       clean rows =", len(ca))
ca = ca.sort_values("order_id").reset_index(drop=True); cb = cb.sort_values("order_id").reset_index(drop=True)
two("l19 identical frames", float((ca.qty == cb.qty).all() and (ca.price == cb.price).all()), 1.0)
vw_a = ca.groupby("symbol").apply(lambda g: (g.price*g.qty).sum()/g.qty.sum(), include_groups=False)
vw_b = {s: sum(r.price*r.qty for r in cb[cb.symbol == s].itertuples())/sum(cb[cb.symbol == s].qty) for s in cb.symbol.unique()}
for s in vw_a.index: two(f"l19 VWAP {s}", float(vw_a[s]), float(vw_b[s]), 1e-9)
print("       VWAP:", vw_a.round(4).to_dict(), " orders per symbol:", ca.symbol.value_counts().to_dict(), " total qty:", int(ca.qty.sum()))
sgn = np.where(ca.side == "B", 1, -1); ca["slip_bp"] = sgn*(ca.price-ca.mid)/ca.mid*1e4; ca["lq"] = np.log(ca.qty/100)
c1 = np.polyfit(ca.lq, ca.slip_bp, 1); f1 = sm.OLS(ca.slip_bp, sm.add_constant(ca.lq)).fit()
two("l19 slope polyfit vs statsmodels", float(c1[0]), float(f1.params["lq"]), 1e-9); two("l19 intercept", float(c1[1]), float(f1.params["const"]), 1e-9)
print(f"       slippage model: slope {c1[0]:.4f} (planted 1.2) intercept {c1[1]:.4f} (planted 0.5) R2 {f1.rsquared:.4f}  mean slip {ca.slip_bp.mean():.3f} bp; se slope {f1.bse['lq']:.4f}")
print("       mean slippage by symbol:", ca.groupby("symbol").slip_bp.mean().round(3).to_dict())
two("l19 predicted slippage at qty 3,200 (lq=ln 32)", float(c1[0]*math.log(32)+c1[1]), float(f1.predict([[1, math.log(32)]])[0]), 1e-9); print("       ->", round(float(c1[0]*math.log(32)+c1[1]), 3), "bp")
# naive path: no dedupe or cleaning mistakes change the answer
nd = od.copy(); nd["qty"] = nd.qty.str.replace(",", "").astype(int); nd["symbol"] = nd.symbol.str.strip().str.upper(); nd = nd[nd.price.notna()]
print("       if -999 prices are kept and duplicates kept: rows", len(nd), " VWAP ALPHA", round(float((nd[nd.symbol == 'ALPHA'].price*nd[nd.symbol == 'ALPHA'].qty).sum()/nd[nd.symbol == 'ALPHA'].qty.sum()), 4))

# ---------- l20 ----------
h = pd.read_csv("data/houses.csv"); h = h[h.price_k <= 5000]
err = (h.price_k - h.price_k.mean()).to_numpy()
def boot_vec(e, B=2000, seed=0):
    r = np.random.default_rng(seed); idx = r.integers(0, len(e), (B, len(e))); return np.sqrt((e[idx]**2).mean(1))
def boot_loop(e, B=2000, seed=0):
    r = np.random.default_rng(seed); out = []
    for _ in range(B): out.append(math.sqrt(float((e[r.integers(0, len(e), len(e))]**2).mean())))
    return np.array(out)
v1, v2 = boot_vec(err), boot_loop(err)
two("l20 bootstrap draws identical (vectorised vs loop)", float(np.abs(v1-v2).max()), 0.0, 1e-12)
print("       n", len(h), " mean price", round(h.price_k.mean(), 3), " baseline RMSE (in-sample sd, ddof 0)", round(float(np.sqrt((err**2).mean())), 3), " boot 95% [", round(float(np.percentile(v1, 2.5)), 3), round(float(np.percentile(v1, 97.5)), 3), "]")
two("l20 rerun with same seed is identical", float(np.abs(boot_vec(err)-v1).max()), 0.0, 0.0)
two("l20 different seed differs", float(np.abs(boot_vec(err, seed=1)-v1).max() > 0), 1.0)
# fix pass: the keyed expression with a guard returns 13 rows, 12 numeric and Wick NaN
_g = tt.groupby("town").apply(lambda g: np.polyfit(g.day, g.temp_c, 1)[0] if len(g) > 2 else np.nan, include_groups=False)
two("l17 guarded groupby: rows", len(_g), 13); two("   numeric slopes", int(_g.notna().sum()), 12); two("   Wick is NaN", float(np.isnan(_g["Wick"])), 1.0)
_u = tt.groupby("town").apply(lambda g: np.polyfit(g.day, g.temp_c, 1)[0], include_groups=False); two("l17 unguarded Wick slope 0.3", round(float(_u["Wick"]), 4), 0.3)
two("l17 negative slopes among the 12 full towns", int((_g.dropna() < 0).sum()), 4)
done()
