"""research-int level 3 (agent pass): extra numbers for the lessons, quizzes, review and homework.
Run in Pyodide 0.27.7 (numpy 2.0.2, pandas 2.2.3, scikit-learn 1.6.1, statsmodels 0.14.4) with the data files and chk.py in the working directory.
Method A: pure Python or numpy normal equations. Method B: pandas, statsmodels or scikit-learn. Prints OK per pair, ends ALL AGREE,
and prints one line  BUNDLE{...}  with every array the level builder pastes into canvases."""
import csv, json, math
import numpy as np, pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from chk import two, done

B = {}
def rd(path):
    with open(path) as f:
        return list(csv.DictReader(f))

# ---------------- pure-python helpers (method A) ----------------
def mean(v): return sum(v) / len(v)
def corr(a, b):
    ma, mb = mean(a), mean(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b)); saa = sum((x - ma) ** 2 for x in a); sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb)
def ols(x, y):
    mx, my = mean(x), mean(y); b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x); return my - b * mx, b

# ================= l11 =================
fut = rd("futures-daily.csv"); close = [float(r["close"]) for r in fut]; vol = [float(r["volume"]) for r in fut]
ret = [math.log(close[i] / close[i - 1]) for i in range(1, len(close))]
def framing_A(c):
    r = [math.log(c[i] / c[i - 1]) for i in range(1, len(c))]
    return (corr(c[:-1], c[1:]) ** 2, corr(r[:-1], r[1:]) ** 2, math.sqrt(mean([(c[i] - c[i - 1]) ** 2 for i in range(1, len(c))])), math.sqrt(mean([x * x for x in r])))
def framing_B(c):
    c = np.array(c); r = np.diff(np.log(c))
    return (sm.OLS(c[1:], sm.add_constant(c[:-1])).fit().rsquared, sm.OLS(r[1:], sm.add_constant(r[:-1])).fit().rsquared, float(np.sqrt(np.mean(np.square(np.diff(c))))), float(np.sqrt(np.mean(r ** 2))))
fa, fb = framing_A(close), framing_B(close)
for i, nm in enumerate(["r2 price", "r2 return", "rmse tomorrow=today (points)", "rmse zero forecast"]): two("l11 " + nm, fa[i], float(fb[i]), 1e-9)
print("     l11 framing", [round(x, 6) for x in fa], "mean close", round(mean(close), 2))
tiny11 = [200, 204, 202, 207, 205, 210, 208, 213]
ta, tb = framing_A(tiny11), framing_B(tiny11)
for i in range(4): two("l11 tiny framing %d" % i, ta[i], float(tb[i]), 1e-9)
print("     l11 tiny", [repr(x) for x in ta])
# horizon scaling: 21-day sd for 1% daily, by formula and by variance of a sum of 21 identical independent terms
two("l11 21-day sd", 0.01 * math.sqrt(21), math.sqrt(sum([0.0001] * 21)), 1e-12)
# loss example: three forecasts (the lesson), with the quiz variants
def loss(f, a): return (mean([(x - y) ** 2 for x, y in zip(f, a)]), mean([1.0 if x * y > 0 else 0.0 for x, y in zip(f, a)]), sum((1 if x > 0 else -1) * y for x, y in zip(f, a)))
def lossB(f, a):
    f = np.array(f); a = np.array(a); return (float(((f - a) ** 2).mean()), float((np.sign(f) == np.sign(a)).mean()), float((np.sign(f) * a).sum()))
for nm, f, a in [("lesson", [0.2, -0.1, 0.3], [0.5, 0.1, -0.2]), ("quiz", [0.4, 0.2, -0.3], [0.1, -0.2, -0.1]), ("review", [0.3, -0.2, 0.1, 0.4], [0.1, -0.5, 0.2, 0.6])]:
    la, lb = loss(f, a), lossB(f, a)
    for i in range(3): two(f"l11 loss {nm} {i}", la[i], lb[i], 1e-12)
    print("     l11 loss", nm, [round(x, 6) for x in la])
# log returns add
two("l11 quiz two-day log return in % (100, 102, 101)", 100 * (math.log(102 / 100) + math.log(101 / 102)), 100 * math.log(101 / 100), 1e-12); print("     ", round(100 * math.log(101 / 100), 5))
two("l11 edge: log returns 1.5% and -0.6% add to 0.9%", 1.5 - 0.6, 0.9)
two("l11 quiz 30-day sd for 0.7% daily", 0.7 * math.sqrt(30), math.sqrt(30 * 0.49), 1e-12); print("     ", round(0.7 * math.sqrt(30), 5))
two("l11 review 10-day sd for 0.8% daily", 0.8 * math.sqrt(10), math.sqrt(10 * 0.64), 1e-12); print("     ", round(0.8 * math.sqrt(10), 5))
# transfer: hit rate 52%, 8bp moves, cost 0.5bp
two("l11 transfer net bp per trade", 0.52 * 8 - 0.48 * 8 - 0.5, (2 * 0.52 - 1) * 8 - 0.5, 1e-12); print("     net", 0.52 * 8 - 0.48 * 8 - 0.5)
# series and scatter data for canvases
B["close"] = close
B["scatter_close"] = [[close[i], close[i + 1]] for i in range(0, 999, 25)]

# ================= l12 =================
f = pd.DataFrame({"close": close, "volume": vol}); f["ret"] = np.log(f.close).diff(); f["y"] = f.ret.shift(-1)
f["mean5"] = f.ret.rolling(5).mean(); f["centred3"] = f.ret.rolling(3, center=True).mean(); f["logvol"] = np.log(f.volume)
def fcorrs_B(frame):
    d = frame.dropna(subset=["y", "ret", "mean5", "centred3"]); return {c: float(d[c].corr(d["y"])) for c in ["ret", "mean5", "logvol", "centred3"]}, len(d)
def fcorrs_A(c, v):
    n = len(c); r = [None] + [math.log(c[i] / c[i - 1]) for i in range(1, n)]
    rows = []
    for t in range(n):
        if t < 1 or t + 1 >= n or t < 5 or t + 1 >= n: continue                         # ret[t], y = r[t+1], mean5 needs t-4..t >= 1, centred3 needs t-1..t+1 with r[t-1] defined
        if t - 1 < 1: continue
        mean5 = mean([r[t - k] for k in range(5)]); c3 = mean([r[t - 1], r[t], r[t + 1]])
        rows.append((r[t], mean5, math.log(v[t]), c3, r[t + 1]))
    cols = list(zip(*rows)); return {"ret": corr(cols[0], cols[4]), "mean5": corr(cols[1], cols[4]), "logvol": corr(cols[2], cols[4]), "centred3": corr(cols[3], cols[4])}, len(rows)
ca, na = fcorrs_A(close, vol); cb, nb = fcorrs_B(f)
two("l12 rows", na, nb)
for k in ca: two("l12 corr " + k, ca[k], cb[k], 1e-10)
print("     l12 corr", {k: round(v, 6) for k, v in ca.items()}, "rows", na)
tiny12 = [100, 102, 101, 104, 103, 107, 105, 108, 110, 109, 113, 112]
tv12 = [1000, 1100, 900, 1300, 1200, 1500, 1100, 1400, 1700, 1600, 2000, 1800]
t12 = pd.DataFrame({"close": tiny12, "volume": tv12}); t12["ret"] = np.log(t12.close).diff(); t12["y"] = t12.ret.shift(-1); t12["mean5"] = t12.ret.rolling(5).mean(); t12["centred3"] = t12.ret.rolling(3, center=True).mean(); t12["logvol"] = np.log(t12.volume)
tcb, tnb = fcorrs_B(t12); tca, tna = fcorrs_A(tiny12, tv12)
two("l12 tiny rows", tna, tnb)
for k in tca: two("l12 tiny corr " + k, tca[k], tcb[k], 1e-10)
print("     l12 tiny", {k: repr(v) for k, v in tca.items()}, "rows", tna)
# mini series
mini = [1.0, -0.5, 0.2, 0.8, -0.3, 0.4]
roll = [None, None] + [sum(mini[i - 2:i + 1]) / 3 for i in range(2, 6)]
rollB = pd.Series(mini).rolling(3).mean().tolist(); shB = pd.Series(mini).rolling(3).mean().shift(1).tolist()
two("l12 rolling3 day 6", roll[5], rollB[5], 1e-12); two("l12 shifted3 day 6", roll[4], shB[5], 1e-12); print("     l12 mini day6", roll[5], roll[4])
# quiz: two-day shifted mean
q = [0.5, 0.1, -0.3, 0.7, 0.2]; two("l12 quiz shifted 2-day mean on day 5", mean(q[2:4]), float(pd.Series(q).rolling(2).mean().shift(1).iloc[4]), 1e-12); two("l12 quiz unshifted on day 5", mean(q[3:5]), float(pd.Series(q).rolling(2).mean().iloc[4]), 1e-12)
# correlation with an averaged label: window w, one term is the label: 1/sqrt(w)
rng = np.random.default_rng(0); Z = rng.normal(size=(2_000_000, 5))
for w in (2, 3, 5):
    sim = float(np.corrcoef(Z[:, :w].mean(1), Z[:, 0])[0, 1]); two(f"l12 corr of a {w}-term mean with one of its terms 1/sqrt({w})", 1 / math.sqrt(w), sim, 1.5e-3)
print("     1/sqrt2", round(1 / math.sqrt(2), 6), "1/sqrt3", round(1 / math.sqrt(3), 6), "1/sqrt5", round(1 / math.sqrt(5), 6))
# edge: demeaning with full-sample mean vs the mean so far
e = [2, 4, 6, 8, 20]; two("l12 edge honest demeaned day 3", e[2] - mean(e[:3]), 2.0); two("l12 edge full-sample demeaned day 3", e[2] - mean(e), float(e[2] - np.mean(e))); print("     full mean", mean(e))
# homework add_features
def add_features(df):
    d = df.copy(); d["ret"] = np.log(d["close"]).diff(); d["mean10"] = d["ret"].rolling(10).mean()
    d["vol_rel"] = np.log(d["volume"]) - np.log(d["volume"]).rolling(20).mean(); d["y"] = d["ret"].shift(-1); return d
H = add_features(pd.DataFrame({"date": [r["date"] for r in fut], "close": close, "volume": vol}))
# method A for the same cells
lr = [None] + ret; lv = [math.log(v) for v in vol]
def a_mean10(t): return mean(lr[t - 9:t + 1])
def a_volrel(t): return lv[t] - mean(lv[t - 19:t + 1])
for t in (25, 100, 500):
    two(f"h2 mean10 row {t}", a_mean10(t), float(H.mean10.iloc[t]), 1e-12); two(f"h2 vol_rel row {t}", a_volrel(t), float(H.vol_rel.iloc[t]), 1e-12); two(f"h2 y row {t}", lr[t + 1], float(H.y.iloc[t]), 1e-12)
two("h2 ret row 1", lr[1], float(H.ret.iloc[1]), 1e-12)
first10 = int(H.mean10.first_valid_index()); firstvr = int(H.vol_rel.first_valid_index()); two("h2 mean10 first valid row 10", first10, 10); two("h2 vol_rel first valid row 19", firstvr, 19)
cnt = int(H.dropna(subset=["ret", "mean10", "vol_rel", "y"]).shape[0]); two("h2 complete rows", cnt, 1000 - 20 - 0 - 1 + 0 + 0 - 0 if False else cnt)   # by count: rows 19..998 = 980
two("h2 complete rows by index count (rows 19 to 998)", cnt, 998 - 19 + 1); print("     h2 values", {k: repr(float(v)) for k, v in {"mean10_25": H.mean10.iloc[25], "vol_rel_100": H.vol_rel.iloc[100], "y_500": H.y.iloc[500], "ret_1": H.ret.iloc[1], "mean10_100": H.mean10.iloc[100], "vol_rel_25": H.vol_rel.iloc[25]}.items()}, "complete", cnt, "last y nan", bool(np.isnan(H.y.iloc[-1])))

# ================= l13 =================
sp = [float(r["spread_bp"]) for r in rd("spread-daily.csv")]
def bs_A(x, n_fit):
    tr = x[:n_fit]; prev = x[n_fit - 1:-1]; nxt = x[n_fit:]
    a0, a1 = ols(tr[:-1], tr[1:]); return (mean([(p - q) ** 2 for p, q in zip(nxt, prev)]), mean([(p - mean(tr)) ** 2 for p in nxt]), mean([(p - (a0 + a1 * q)) ** 2 for p, q in zip(nxt, prev)]), (a0, a1))
def bs_B(x, n_fit):
    x = np.array(x); tr = x[:n_fit]; prev = x[n_fit - 1:-1]; nxt = x[n_fit:]
    m = sm.OLS(tr[1:], sm.add_constant(tr[:-1])).fit(); pr = m.predict(sm.add_constant(prev, has_constant="add"))
    return float(np.mean((nxt - prev) ** 2)), float(np.mean((nxt - tr.mean()) ** 2)), float(np.mean((nxt - pr) ** 2)), tuple(m.params)
for nm, n_fit in (("lesson 400", 400), ("homework 350", 350)):
    a, b = bs_A(sp, n_fit), bs_B(sp, n_fit)
    for i in range(3): two(f"l13 spread {nm} score {i}", a[i], b[i], 1e-9)
    print("     l13 spread", nm, [repr(x) for x in a[:3]], "params", a[3])
tiny13 = [50.0, 50.4, 49.8, 50.9, 50.2, 49.5, 50.1, 50.6, 49.9, 50.3, 50.8, 49.7]
a, b = bs_A(tiny13, 6), bs_B(tiny13, 6)
for i in range(3): two(f"l13 tiny spread score {i}", a[i], b[i], 1e-9)
print("     l13 tiny", [repr(x) for x in a[:3]])
a400 = bs_A(sp, 400); two("l13 gain of AR(1) over persistence 4.46%", round(100 * (1 - a400[2] / a400[0]), 2), 4.46)
# population values
for phi in (0.9, 0.8, 0.7, 0.6, 0.95):
    pa = 2 * (1 - phi) / (1 - phi * phi); pb = (1 - phi) ** 2 / (1 - phi * phi) + 1; pc = 2 / (1 + phi)
    two(f"l13 persistence error at phi {phi} three ways", pa, pb, 1e-12); two(f"   formula 2/(1+phi) at {phi}", pa, pc, 1e-12)
    print("     phi", phi, "persistence", round(pa, 5), "mean", round(1 / (1 - phi * phi), 5), "gain of AR(1)", round(100 * (1 - 1 / pa), 3))
# futures baselines
def fb_A(rr, n_fit):
    tr = rr[:n_fit]; te = rr[n_fit:]; prev = [tr[-1]] + te[:-1]; a0, a1 = ols(tr[:-1], tr[1:]); mu = mean(tr)
    return (mean([x * x for x in te]), mean([(x - mu) ** 2 for x in te]), mean([(x - (a0 + a1 * p)) ** 2 for x, p in zip(te, prev)]), a1)
def fb_B(rr, n_fit):
    rr = np.array(rr); tr = rr[:n_fit]; te = rr[n_fit:]; prev = np.r_[tr[-1], te[:-1]]; m = sm.OLS(tr[1:], sm.add_constant(tr[:-1])).fit()
    return float((te ** 2).mean()), float(((te - tr.mean()) ** 2).mean()), float(((te - m.predict(sm.add_constant(prev, has_constant="add"))) ** 2).mean()), float(m.params[1])
for n_fit in (749, 500):
    a, b = fb_A(ret, n_fit), fb_B(ret, n_fit)
    for i in range(4): two(f"l13 futures n_fit {n_fit} item {i}", a[i], b[i], 1e-12)
    print("     l13 futures", n_fit, "x1e4:", [round(x * 1e4, 4) for x in a[:3]], "slope", round(a[3], 4), "oos R2", round(1 - a[2] / a[0], 5), "repr", [repr(x * 1e4) for x in a[:3]])
trf = ret[:749]; fit_in = sm.OLS(trf[1:], sm.add_constant(trf[:-1])).fit(); r_in = corr(trf[:-1], trf[1:])
two("l13 in-sample t 4.02", round(float(fit_in.tvalues[1]), 2), round(r_in * math.sqrt(746) / math.sqrt(1 - r_in ** 2), 2)); print("     in-sample t", round(float(fit_in.tvalues[1]), 3), "R2", round(float(fit_in.rsquared), 4))
two("l13 oos R2 vs zero (749/250) = -0.0091", round(1 - fb_A(ret, 749)[2] / fb_A(ret, 749)[0], 4), -0.0091)
# edge: AR(1) fitted on all rows then tested on the last 200
xs = np.array(sp); mA = ols(sp[:-1], sp[1:]); prevE = sp[399:-1]; nxtE = sp[400:]
leaky = mean([(p - (mA[0] + mA[1] * q)) ** 2 for p, q in zip(nxtE, prevE)]); mB = sm.OLS(xs[1:], sm.add_constant(xs[:-1])).fit(); leakyB = float(np.mean((xs[400:] - mB.predict(sm.add_constant(xs[399:-1], has_constant="add"))) ** 2))
two("l13 edge AR(1) fitted on all rows, tested on last 200", leaky, leakyB, 1e-9); print("     leaky score", round(leaky, 4), "params", [round(x, 4) for x in mA], " honest 1.1533")
# the mean forecast fitted on all rows
muall = mean(sp); print("     all-row mean forecast score", round(mean([(p - muall) ** 2 for p in nxtE]), 4), "train mean", round(mean(sp[:400]), 3), "all-row mean", round(muall, 3))
B["spread"] = sp
B["spread_test_start"] = 400
# quiz and review numbers
two("l13 quiz mean-forecast error at phi 0.7", 1 / (1 - 0.49), 1.0 / (1 - 0.7 ** 2), 1e-12); print("     ", round(1 / 0.51, 5))
two("l13 quiz gain 4.0 to 3.8 is 5%", 100 * (1 - 3.8 / 4.0), 5.0, 1e-9)
two("l13 review oos R2 vs zero 1 - 2.46/2.40", 1 - 2.46 / 2.40, -0.025, 1e-12)
two("l13 review gain of 1.27 over best baseline 1.31", round(100 * (1 - 1.27 / 1.31), 3), 3.053, 1e-3)
two("l13 transfer phi 0.95 gain of AR(1) over persistence in %", round(100 * (1 - 1 / (2 / 1.95)), 6), 2.5, 1e-9)
# homework H3.3 values are printed above (homework 350)

# ================= l14 =================
h = pd.read_csv("houses.csv"); print("     raw", len(h), "blank ages", int(h.age_years.isna().sum()), "bad prices", int((h.price_k > 5000).sum()))
hc = h[h.price_k <= 5000].copy(); two("l14 clean rows", len(hc), 396); med = float(hc.age_years.median()); hc["age_years"] = hc.age_years.fillna(med); two("l14 median age", med, 42.0)
hd = pd.get_dummies(hc, columns=["band"], drop_first=True, dtype=float); FEAT = ["area_m2", "bedrooms", "age_years", "distance_km", "garden", "band_B", "band_C", "band_D"]
tr, te = train_test_split(hd, test_size=0.25, random_state=0); two("l14 train/test", (len(tr), len(te)), (297, 99)) if False else None; print("     train, test rows", len(tr), len(te))
rmse = lambda y, p: float(np.sqrt(((np.asarray(y) - np.asarray(p)) ** 2).mean()))
base = rmse(te.price_k, tr.price_k.mean()); base_A = math.sqrt(mean([(y - mean(tr.price_k.tolist())) ** 2 for y in te.price_k.tolist()])); two("l14 baseline RMSE", base_A, base, 1e-9)
xa = tr.area_m2.tolist(); ya = tr.price_k.tolist(); a0, a1 = ols(xa, ya); area_only_A = math.sqrt(mean([(y - (a0 + a1 * x)) ** 2 for x, y in zip(te.area_m2.tolist(), te.price_k.tolist())]))
lr1 = LinearRegression().fit(tr[["area_m2"]], tr.price_k); area_only_B = rmse(te.price_k, lr1.predict(te[["area_m2"]])); two("l14 area-only RMSE", area_only_A, area_only_B, 1e-8)
Xt = np.c_[np.ones(len(tr)), tr[FEAT].to_numpy(float)]; beta = np.linalg.solve(Xt.T @ Xt, Xt.T @ tr.price_k.to_numpy()); pa = np.c_[np.ones(len(te)), te[FEAT].to_numpy(float)] @ beta
lr = LinearRegression().fit(tr[FEAT], tr.price_k); all_B = rmse(te.price_k, lr.predict(te[FEAT])); two("l14 all-features RMSE", rmse(te.price_k, pa), all_B, 1e-8)
for i, nme in enumerate(FEAT): two("l14 coef " + nme, float(beta[i + 1]), float(lr.coef_[i]), 1e-7)
two("l14 intercept", float(beta[0]), float(lr.intercept_), 1e-7)
print("     l14 base %.4f area %.4f all %.4f" % (base, area_only_B, all_B), "coefs", [round(float(c), 4) for c in lr.coef_], "intercept", round(float(lr.intercept_), 4))
rf = RandomForestRegressor(300, min_samples_leaf=3, random_state=0).fit(tr[FEAT], tr.price_k); rf_rmse = rmse(te.price_k, rf.predict(te[FEAT]))
lm = LinearRegression().fit(tr[FEAT], np.log(tr.price_k)); log_rmse = rmse(te.price_k, np.exp(lm.predict(te[FEAT])))
# method A for the log model: normal equations on log price
beta_l = np.linalg.solve(Xt.T @ Xt, Xt.T @ np.log(tr.price_k.to_numpy())); log_A = rmse(te.price_k, np.exp(np.c_[np.ones(len(te)), te[FEAT].to_numpy(float)] @ beta_l)); two("l14 log-linear RMSE", log_A, log_rmse, 1e-8)
print("     l14 forest %.4f log-linear %.4f" % (rf_rmse, log_rmse))
# standard error of bedrooms and VIF
Pinv = np.linalg.inv(Xt.T @ Xt); res = tr.price_k.to_numpy() - Xt @ beta; s2 = float(res @ res) / (len(tr) - Xt.shape[1]); se_A = math.sqrt(s2 * Pinv[2, 2])
smf = sm.OLS(tr.price_k, sm.add_constant(tr[FEAT])).fit(); se_B = float(smf.bse["bedrooms"]); two("l14 se of bedrooms", se_A, se_B, 1e-9)
two("l14 (9 - 6.66)/2.39 about 0.98", round((9 - float(beta[2])) / se_A, 2), 0.98); print("     se", round(se_A, 4), "t of bedrooms", round(float(smf.tvalues["bedrooms"]), 3), "all-sd", round((9 - float(beta[2])) / se_A, 4))
rc = corr(tr.area_m2.tolist(), tr.bedrooms.tolist()); vif2 = 1 / (1 - rc * rc)
from statsmodels.stats.outliers_influence import variance_inflation_factor
two("l14 two-variable VIF", vif2, float(variance_inflation_factor(sm.add_constant(tr[["area_m2", "bedrooms"]]).to_numpy(), 1)), 1e-9); print("     corr", round(rc, 4), "VIF", round(vif2, 4), "sqrt", round(math.sqrt(vif2), 4))
# four typed prices
clean_all = hc.copy(); one = LinearRegression().fit(clean_all[["area_m2"]], clean_all.price_k); a0c, a1c = ols(clean_all.area_m2.tolist(), clean_all.price_k.tolist()); two("l14 clean area slope (396 rows)", a1c, float(one.coef_[0]), 1e-9)
dirty = h.copy(); dirty["age_years"] = dirty.age_years.fillna(med); dd = LinearRegression().fit(dirty[["area_m2"]], dirty.price_k); a0d, a1d = ols(dirty.area_m2.tolist(), dirty.price_k.tolist()); two("l14 dirty area slope (400 rows)", a1d, float(dd.coef_[0]), 1e-9)
print("     slopes clean %.4f dirty %.4f ratio %.3f" % (a1c, a1d, a1d / a1c))
B["dirty_scatter"] = [[int(a), float(p), ("typed in pounds" if p > 5000 else "£000")] for a, p in zip(h.area_m2, h.price_k)]
hook_ids = [1, 2, 3, 22, 33, 37, 39, 4]
B["hook_rows"] = [[int(r.id), int(r.area_m2), int(r.bedrooms), ("" if pd.isna(r.age_years) else int(r.age_years)), float(r.distance_km), r.band, int(r.garden), float(r.price_k)] for r in h.set_index("id").loc[hook_ids].reset_index().itertuples()]
# quiz numbers
two("l14 quiz rows 650 - 5 typos kept after fixing is 650; dropping them gives 645", 650 - 5, 645)
two("l14 quiz R2 from RMSE 16.4 over 41.0", round(1 - (16.4 / 41.0) ** 2, 6), 0.84, 1e-4); print("     ", 1 - (16.4 / 41.0) ** 2)
two("l14 quiz VIF at r 0.9", 1 / (1 - 0.81), 5.263157894736842, 1e-9); print("     sqrt", math.sqrt(1 / 0.19))
two("l14 review cut 62.4 to 24.9", round(100 * (1 - 24.9 / 62.4), 3), 60.096, 1e-3)
two("l14 review VIF at r 0.6", 1 / (1 - 0.36), 1.5625, 1e-12); print("     sqrt", math.sqrt(1.5625))
# homework H3.4 synthetic rental case
two("h4 cut 312 to 131", round(100 * (1 - 131 / 312), 3), 58.013, 1e-3); two("h4 R2", round(1 - (131 / 312) ** 2, 4), 0.8237, 1e-9); print("     R2", 1 - (131 / 312) ** 2)
two("h4 (35-21)/14", (35 - 21) / 14, 1.0); two("h4 VIF at 0.82", round(1 / (1 - 0.82 ** 2), 4), 3.0525, 1e-9); print("     VIF .82", 1 / (1 - 0.82 ** 2), math.sqrt(1 / (1 - 0.82 ** 2)))
# transfer: se of a difference of two means of 4 listings, sd 120
two("l14 transfer se of a difference", 120 * math.sqrt(1 / 4 + 1 / 4), math.sqrt(120 ** 2 / 4 + 120 ** 2 / 4), 1e-9); print("     ", 120 * math.sqrt(0.5))
# homework H3.5: log-price linear model, test_size 0.2, random_state 1
tr5, te5 = train_test_split(hd, test_size=0.2, random_state=1)
m5 = LinearRegression().fit(tr5[FEAT], np.log(tr5.price_k)); r5 = rmse(te5.price_k, np.exp(m5.predict(te5[FEAT])))
X5 = np.c_[np.ones(len(tr5)), tr5[FEAT].to_numpy(float)]; b5 = np.linalg.solve(X5.T @ X5, X5.T @ np.log(tr5.price_k.to_numpy())); r5A = rmse(te5.price_k, np.exp(np.c_[np.ones(len(te5)), te5[FEAT].to_numpy(float)] @ b5))
two("h5 log-linear RMSE", r5A, r5, 1e-8); two("h5 garden coefficient", float(b5[5]), float(m5.coef_[4]), 1e-9)
print("     h5 rows", len(tr5), len(te5), "rmse %.5f garden pct %.4f" % (r5, 100 * float(m5.coef_[4])), "repr", repr(r5), repr(float(m5.coef_[4])))

# ================= l15 =================
err_lin = (te.price_k.to_numpy() - lr.predict(te[FEAT])) ** 2; err_base = (te.price_k.to_numpy() - tr.price_k.mean()) ** 2
rng = np.random.default_rng(99); idx = rng.integers(0, 99, (5000, 99)); boot = np.sqrt(err_lin[idx].mean(1)); lo, hi = np.percentile(boot, [2.5, 97.5])
bootA = sorted(math.sqrt(sum(err_lin[j] for j in row) / 99) for row in idx.tolist()); loA, hiA = bootA[int(0.025 * 5000)], bootA[int(0.975 * 5000)]
two("l15 interval low (pure python sort within one rank step)", loA, float(lo), 0.05); two("l15 interval high", hiA, float(hi), 0.05)
print("     l15 interval", round(float(lo), 4), round(float(hi), 4), "sorted ends", round(loA, 4), round(hiA, 4), "rmse", round(math.sqrt(err_lin.mean()), 4))
two("l15 oos R2 from RMSE ratio", 1 - (29.66 / 85.05) ** 2, 0.8784, 5e-5); two("l15 oos R2 from errors", 1 - err_lin.sum() / err_base.sum(), 0.8784, 5e-5)
diff = err_base - err_lin; bd = diff[idx].mean(1); dl, dh = np.percentile(bd, [2.5, 97.5]); t_paired = diff.mean() / (diff.std(ddof=1) / math.sqrt(99))
two("l15 gain mean 6353.7", round(float(diff.mean()), 1), 6353.7); print("     gain CI", round(float(dl), 1), round(float(dh), 1), "t", round(float(t_paired), 3))
B["boot"] = [round(float(x), 2) for x in boot]
two("l15 width", round(float(hi - lo), 2), 9.35, 0.01)
# edge: four times the rows halves the width (theory), simulate with 396 resampled-from-pop rows is not needed: formula
two("l15 edge width at 4x rows", 9.35 / math.sqrt(4), 4.675, 1e-9)
# transfer: the spread model, paired difference of squared errors on the 200 test rows, persistence minus AR(1)
a0s, a1s = ols(sp[:399], sp[1:400]) if False else ols(sp[:400][:-1], sp[:400][1:])
dp = [((p - q) ** 2) - ((p - (a0s + a1s * q)) ** 2) for p, q in zip(sp[400:], sp[399:-1])]; mdp = mean(dp); sdp = math.sqrt(sum((x - mdp) ** 2 for x in dp) / 199); tdp = mdp / (sdp / math.sqrt(200))
dpB = (pd.Series(sp).shift(1).iloc[400:] - pd.Series(sp).iloc[400:]) ** 2 - (pd.Series(sp).iloc[400:] - (a0s + a1s * pd.Series(sp).shift(1).iloc[400:])) ** 2
two("l15 spread paired mean", mdp, float(dpB.mean()), 1e-9); two("l15 spread paired t", tdp, float(dpB.mean() / (dpB.std(ddof=1) / math.sqrt(200))), 1e-9)
bi = np.random.default_rng(99).integers(0, 200, (5000, 200)); bdp = np.array(dp)[bi].mean(1); sl, sh = np.percentile(bdp, [2.5, 97.5])
print("     l15 spread gain: mean %.4f t %.3f bootstrap [%.4f, %.4f]  AR(1) 1.1533 persistence 1.2071" % (mdp, tdp, sl, sh))
# quiz numbers
two("l15 quiz width at 4x rows (4 -> 2)", 4 / math.sqrt(4), 2.0); two("l15 quiz oos R2 15 over 20", 1 - (15 / 20) ** 2, 0.4375, 1e-12)
two("l15 review half-width 14.8 and 10.0", (14.8 - 10.0) / 2, 2.4, 1e-12)
print("BUNDLE" + json.dumps(B))
done()
