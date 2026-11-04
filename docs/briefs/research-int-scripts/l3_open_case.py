"""research-int level 3: l11 framing, l12 features and leakage, l13 baselines, l14 house price case, l15 presenting.
Reads ./data/*.csv written by gen_data.py. Method A = hand formula or numpy normal equations; method B = statsmodels or scikit-learn."""
import math
import numpy as np, pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from chk import two, done

# ---------- l11 ----------
pred = np.array([0.2, -0.1, 0.3]); act = np.array([0.5, 0.1, -0.2])
two("l11 toy MSE (%^2)", float(((act-pred)**2).mean()), (0.09+0.04+0.25)/3, 1e-12)
two("l11 toy hit rate 1/3", float((np.sign(act) == np.sign(pred)).mean()), 1/3, 1e-12)
two("l11 toy P&L with sign positions (%)", float((np.sign(pred)*act).sum()), 0.5-0.1-0.2, 1e-12)
fut = pd.read_csv("data/futures-daily.csv"); fut["ret"] = np.log(fut.close).diff()
# price on yesterday's price, hand r^2 vs statsmodels
p0, p1 = fut.close.iloc[:-1].to_numpy(), fut.close.iloc[1:].to_numpy()
r2_hand = np.corrcoef(p0, p1)[0, 1]**2; r2_sm = sm.OLS(p1, sm.add_constant(p0)).fit().rsquared
two("l11 R2 of price on yesterday's price", r2_hand, r2_sm, 1e-10); print("     R2 price", round(r2_sm, 5))
rr = fut.ret.dropna().to_numpy(); a0, a1 = rr[:-1], rr[1:]
r2r_hand = np.corrcoef(a0, a1)[0, 1]**2; fr = sm.OLS(a1, sm.add_constant(a0)).fit()
two("l11 R2 of return on yesterday's return", r2r_hand, fr.rsquared, 1e-10); print("     R2 return", round(fr.rsquared, 5), "slope", round(fr.params[1], 4), "t", round(fr.tvalues[1], 3), "autocorr", round(np.corrcoef(a0, a1)[0, 1], 4))
two("l11 'predict price = yesterday' RMSE in points equals sd of daily change (ddof 0, same as mean abs sq)", float(np.sqrt(((p1-p0)**2).mean())), float(np.sqrt(np.mean(np.diff(fut.close)**2))), 1e-9)
print("     RMSE of 'tomorrow = today' in index points:", round(float(np.sqrt(((p1-p0)**2).mean())), 2), " mean close", round(fut.close.mean(), 1), " sd of daily returns", round(rr.std(ddof=1), 5))
two("l11 5-day sd = sd*sqrt(5) for iid (sim tol .0003)", 0.01*math.sqrt(5), float(np.random.default_rng(1).normal(0, 0.01, (400000, 5)).sum(1).std()), 3e-4)
print("     5-day sd", round(0.01*math.sqrt(5), 5), " 21-day", round(0.01*math.sqrt(21), 5), " 252-day", round(0.01*math.sqrt(252), 4))
two("l11 zero-forecast MSE equals mean(r^2)", float((rr**2).mean()), float(np.mean(np.square(rr))), 1e-15); print("     zero forecast RMSE", round(float(np.sqrt((rr**2).mean())), 5))

# ---------- l12 ----------
f = fut.copy(); f["y"] = f.ret.shift(-1)                                  # label: next day's return
f["lag0"] = f.ret                                                       # known at today's close
f["mean5"] = f.ret.rolling(5).mean()                                    # known at today's close
f["leak3"] = f.ret.rolling(3, center=True).mean()                       # days t-1, t, t+1 : contains the label
f["vol_today"] = np.log(f.volume)
f["zscore_full"] = (f.ret - f.ret.mean())/f.ret.std()                   # uses whole-sample moments (mild look-ahead)
d = f.dropna(subset=["y", "lag0", "mean5", "leak3"])
for c in ("lag0", "mean5", "leak3", "vol_today"):
    ca = np.corrcoef(d[c], d.y)[0, 1]; cb = sm.OLS(d.y, sm.add_constant(d[c])).fit().rsquared**0.5
    two(f"l12 corr(label, {c})", float(ca), float(cb), 1e-10); print(f"     corr {c}: {ca:.4f}  R2 {ca**2:.4f}")
print("     leak3 expected about 1/sqrt(3) =", round(1/math.sqrt(3), 4))
two("l12 corr(vol_today, |next return|) is a different, legit question", 1.0, 1.0)
print("     corr(vol_today, |y|)", round(float(np.corrcoef(d.vol_today, d.y.abs())[0, 1]), 4))
mini = pd.Series([1.0, -0.5, 0.2, 0.8, -0.3, 0.4])
a = mini.rolling(3).mean().tolist(); b = mini.rolling(3).mean().shift(1).tolist()
print("     mini series rolling3:", [None if math.isnan(v) else round(v, 4) for v in a]); print("     shifted:", [None if math.isnan(v) else round(v, 4) for v in b])
hand = [None, None, (1.0-0.5+0.2)/3, (-0.5+0.2+0.8)/3, (0.2+0.8-0.3)/3, (0.8-0.3+0.4)/3]
two("l12 rolling3 by hand, last value", hand[5], a[5], 1e-12); two("l12 rolling3 by hand, value 3", hand[2], a[2], 1e-12)
print("     hand:", [None if v is None else round(v, 4) for v in hand])

# ---------- l13 ----------
sp = pd.read_csv("data/spread-daily.csv").spread_bp.to_numpy(); train, test = sp[:400], sp[400:]
# test targets x_t for t in 401..600 (index 400..599), predictor x_{t-1}
xprev, xnext = sp[399:-1], sp[400:]
mse_persist = float(((xnext-xprev)**2).mean()); mu_tr = train.mean(); mse_mean = float(((xnext-mu_tr)**2).mean())
tx, ty = train[:-1], train[1:]; X = np.c_[np.ones(len(tx)), tx]; beta = np.linalg.solve(X.T@X, X.T@ty)
mse_ar = float(((xnext-(beta[0]+beta[1]*xprev))**2).mean())
rm = sm.OLS(ty, sm.add_constant(tx)).fit(); mse_ar_b = float(((xnext-rm.predict(sm.add_constant(xprev, has_constant="add")))**2).mean())
two("l13 AR(1) beta0 normal equations vs statsmodels", float(beta[0]), float(rm.params[0]), 1e-9); two("l13 AR(1) beta1", float(beta[1]), float(rm.params[1]), 1e-9)
two("l13 AR(1) test MSE", mse_ar, mse_ar_b, 1e-9)
two("l13 persistence MSE via numpy vs pandas", mse_persist, float((pd.Series(sp).diff().iloc[400:]**2).mean()), 1e-12)
two("l13 mean-baseline MSE via numpy vs sklearn DummyRegressor", mse_mean, float(((xnext-__import__("sklearn.dummy", fromlist=["x"]).DummyRegressor().fit(train[:, None], train).predict(xprev[:, None]))**2).mean()), 1e-9)
print(f"     spread test MSE: persistence {mse_persist:.4f}  train-mean {mse_mean:.4f}  AR(1) {mse_ar:.4f}   beta {beta.round(4)}  mean(train) {mu_tr:.3f}")
print("     population values: persistence 2(1-phi)*var =", round(2*0.1*(1/(1-0.81)), 4), " mean = var =", round(1/(1-0.81), 4), " AR(1) = sigma^2 = 1")
two("l13 population persistence MSE", 2*0.1/(1-0.81), 1.0526315789, 1e-8); two("l13 population var 1/(1-phi^2)", 1/(1-0.81), 5.2631578947, 1e-8)
print("     improvement AR over persistence:", round(1-mse_ar/mse_persist, 4))
# futures: does anything beat the zero forecast out of sample?
rets = fut.ret.dropna().to_numpy(); tr, te = rets[:749], rets[749:]          # 749 train, 250 test
z_mse = float((te**2).mean()); m_mse = float(((te-tr.mean())**2).mean())
ta, tb = tr[:-1], tr[1:]; bb = np.polyfit(ta, tb, 1); prev = np.r_[tr[-1], te[:-1]]; ar_mse = float(((te-np.polyval(bb, prev))**2).mean())
rf = sm.OLS(tb, sm.add_constant(ta)).fit(); ar_mse_b = float(((te-rf.predict(sm.add_constant(prev, has_constant="add")))**2).mean())
two("l13 futures AR(1) test MSE polyfit vs statsmodels", ar_mse, ar_mse_b, 1e-12)
print(f"     futures test MSE (x1e-4): zero {z_mse*1e4:.4f}  train mean {m_mse*1e4:.4f}  AR(1) {ar_mse*1e4:.4f}   AR1 slope {bb[0]:.4f}")
print("     out-of-sample R2 vs zero forecast, AR(1):", round(1-ar_mse/z_mse, 5))

# ---------- l14 ----------
h = pd.read_csv("data/houses.csv")
print("     raw rows", len(h), " blank ages", int(h.age_years.isna().sum()), " prices > 5000:", int((h.price_k > 5000).sum()))
two("l14 rows after dropping price>5000", len(h[h.price_k <= 5000]), 396)
hc = h[h.price_k <= 5000].copy(); med_age = float(hc.age_years.median()); hc["age_years"] = hc.age_years.fillna(med_age)
hc["bandB"] = (hc.band == "B")*1; hc["bandC"] = (hc.band == "C")*1; hc["bandD"] = (hc.band == "D")*1
feats = ["area_m2", "bedrooms", "age_years", "distance_km", "garden", "bandB", "bandC", "bandD"]
tr, te = train_test_split(hc, test_size=0.25, random_state=0)
rm_ = lambda y, p: float(np.sqrt(((y-p)**2).mean()))
base = rm_(te.price_k, tr.price_k.mean())
Xa = np.c_[np.ones(len(tr)), tr[feats].to_numpy(float)]; ba = np.linalg.solve(Xa.T@Xa, Xa.T@tr.price_k.to_numpy())
pa = np.c_[np.ones(len(te)), te[feats].to_numpy(float)]@ba
lr = LinearRegression().fit(tr[feats], tr.price_k); pb = lr.predict(te[feats])
two("l14 OLS coefficient vector normal eq vs sklearn", float(np.abs(ba[1:]-lr.coef_).max()), 0.0, 1e-7)
two("l14 test RMSE linear", rm_(te.price_k, pa), rm_(te.price_k, pb), 1e-8)
smf = sm.OLS(tr.price_k, sm.add_constant(tr[feats].astype(float))).fit(); two("l14 test RMSE statsmodels", rm_(te.price_k, pa), rm_(te.price_k, smf.predict(sm.add_constant(te[feats].astype(float), has_constant="add"))), 1e-8)
one = LinearRegression().fit(tr[["area_m2"]], tr.price_k); r_area = rm_(te.price_k, one.predict(te[["area_m2"]]))
logm = LinearRegression().fit(tr[feats], np.log(tr.price_k)); r_log = rm_(te.price_k, np.exp(logm.predict(te[feats])))
rfm = RandomForestRegressor(300, min_samples_leaf=3, random_state=0, n_jobs=1).fit(tr[feats], tr.price_k); r_rf = rm_(te.price_k, rfm.predict(te[feats]))
print(f"     rows train/test {len(tr)}/{len(te)}  median age {med_age}")
print(f"     test RMSE (£000): mean-price baseline {base:.2f}  area only {r_area:.2f}  linear all {rm_(te.price_k, pb):.2f}  log-linear {r_log:.2f}  random forest {r_rf:.2f}")
print("     coefficients (£000 per unit):", dict(zip(feats, np.round(lr.coef_, 2))), " intercept", round(float(lr.intercept_), 2))
print("     true: area 2.6, beds 9, age -0.8, dist -5, garden 18, bands B -25, C -40, D -60 relative to A")
# collinearity
Xv = sm.add_constant(tr[["area_m2", "bedrooms"]].astype(float)); vif_b = variance_inflation_factor(Xv.to_numpy(), 1)
rcorr = np.corrcoef(tr.area_m2, tr.bedrooms)[0, 1]; two("l14 VIF area, bedrooms: 1/(1-r^2)", 1/(1-rcorr**2), vif_b, 1e-9)
print("     corr(area, bedrooms)", round(rcorr, 4), " VIF", round(vif_b, 3))
# outlier effect: keep the 4 bad prices
hb = h.copy(); hb["age_years"] = hb.age_years.fillna(med_age); lb = LinearRegression().fit(hb[["area_m2"]], hb.price_k)
print("     area slope with 4 typo rows kept:", round(float(lb.coef_[0]), 2), " without:", round(float(one.coef_[0]), 2))
two("l14 cleaning: price/1000 recovers typos (max price after dividing)", float((h[h.price_k > 5000].price_k/1000).max() < 1000), 1.0)

# ---------- l15 ----------
err_lin = (te.price_k.to_numpy()-pb)**2; err_base = (te.price_k.to_numpy()-tr.price_k.mean())**2
rm_lin = math.sqrt(err_lin.mean())
rng = np.random.default_rng(99); idx = rng.integers(0, len(te), (5000, len(te)))
boot = np.sqrt(err_lin[idx].mean(1)); lo, hi = np.percentile(boot, [2.5, 97.5])
mse_se = err_lin.std(ddof=1)/math.sqrt(len(te)); lo_n, hi_n = math.sqrt(max(err_lin.mean()-1.96*mse_se, 0)), math.sqrt(err_lin.mean()+1.96*mse_se)
two("l15 RMSE interval low: bootstrap vs normal on MSE (tol 1.0)", float(lo), lo_n, 1.0); two("l15 RMSE interval high (tol 1.0)", float(hi), hi_n, 1.0)
print(f"     linear RMSE {rm_lin:.2f}; bootstrap 95% [{lo:.2f}, {hi:.2f}]; normal-on-MSE [{lo_n:.2f}, {hi_n:.2f}]")
diff = err_base-err_lin; bd = diff[idx].mean(1); dl, dh = np.percentile(bd, [2.5, 97.5]); dn = diff.mean()/(diff.std(ddof=1)/math.sqrt(len(te)))
print(f"     per-row squared-error gain over baseline: mean {diff.mean():.1f} bootstrap 95% [{dl:.1f}, {dh:.1f}]  t {dn:.2f}")
two("l15 improvement CI lower above zero (bootstrap)", float(dl > 0), 1.0); two("l15 paired t above 2", float(dn > 2), 1.0)
print("     out-of-sample R2 vs mean baseline:", round(1-err_lin.sum()/err_base.sum(), 4))
done()
