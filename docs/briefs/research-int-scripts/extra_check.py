"""research-int: extra precise values used in homework tests (houses split, spread MSEs, ticks values)."""
import numpy as np, pandas as pd, statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from chk import two, done
h = pd.read_csv("data/houses.csv"); hc = h[h.price_k <= 5000].copy(); hc["age_years"] = hc.age_years.fillna(hc.age_years.median())
hc = pd.concat([hc, pd.get_dummies(hc.band, prefix="band", drop_first=True).astype(int)], axis=1)
feats = ["area_m2", "bedrooms", "age_years", "distance_km", "garden", "band_B", "band_C", "band_D"]
tr, te = train_test_split(hc, test_size=0.25, random_state=0)
lr = LinearRegression().fit(tr[feats], tr.price_k); p = lr.predict(te[feats]); rmse = float(np.sqrt(((te.price_k-p)**2).mean()))
sm_fit = sm.OLS(tr.price_k, sm.add_constant(tr[feats].astype(float))).fit()
two("H3.5 bedrooms coefficient sklearn vs statsmodels", float(lr.coef_[1]), float(sm_fit.params["bedrooms"]), 1e-9)
two("H3.5 RMSE with get_dummies drop_first (same as manual dummies)", rmse, 29.658229024462884, 1e-8)
base = float(np.sqrt(((te.price_k-tr.price_k.mean())**2).mean())); one = LinearRegression().fit(tr[["area_m2"]], tr.price_k); r1 = float(np.sqrt(((te.price_k-one.predict(te[["area_m2"]]))**2).mean()))
print(f"     train {len(tr)} test {len(te)}  RMSE linear {rmse:.4f} baseline {base:.4f} area-only {r1:.4f} reduction {1-rmse/base:.4f}  coef {dict(zip(feats, lr.coef_.round(4)))} intercept {lr.intercept_:.4f}")
print("     test-set mean price", round(float(te.price_k.mean()), 3), " train mean", round(float(tr.price_k.mean()), 3), " R2 oos", round(1-((te.price_k-p)**2).sum()/((te.price_k-tr.price_k.mean())**2).sum(), 4))
print("     median age used", float(h[h.price_k <= 5000].age_years.median()))
tk = pd.read_csv("data/ticks-gaps.csv"); c = tk.dropna(subset=["price"]).groupby("t_sec", as_index=False).price.mean().sort_values("t_sec")
for t in (5, 100, 12000, 23000, 23400): print("     ticks", t, repr(float(np.interp(t, c.t_sec, c.price))))
sp = pd.read_csv("data/spread-daily.csv").spread_bp.to_numpy(); print("     spread rows", len(sp), "first values", sp[:3], "mean", round(sp.mean(), 3))
done()
