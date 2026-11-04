"""research-int level 3 (agent pass), part 2: coefficient table with standard errors for the l14 canvas, and two stated side numbers.
Run in Pyodide like l3_aux.py (data files and chk.py in the working directory). Method A: normal equations. Method B: statsmodels."""
import json, math
import numpy as np, pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from chk import two, done

h = pd.read_csv("houses.csv"); hc = h[h.price_k <= 5000].copy(); hc["age_years"] = hc.age_years.fillna(hc.age_years.median())
hd = pd.get_dummies(hc, columns=["band"], drop_first=True, dtype=float)
FEAT = ["area_m2", "bedrooms", "age_years", "distance_km", "garden", "band_B", "band_C", "band_D"]
tr, te = train_test_split(hd, test_size=0.25, random_state=0)
X = np.c_[np.ones(len(tr)), tr[FEAT].to_numpy(float)]; y = tr.price_k.to_numpy()
P = np.linalg.inv(X.T @ X); b = P @ X.T @ y; res = y - X @ b; s2 = float(res @ res) / (len(y) - X.shape[1]); se = np.sqrt(s2 * np.diag(P))
m = sm.OLS(tr.price_k, sm.add_constant(tr[FEAT])).fit()
for i, nme in enumerate(["const"] + FEAT):
    two("coef " + nme, float(b[i]), float(m.params.iloc[i]), 1e-7); two("se " + nme, float(se[i]), float(m.bse.iloc[i]), 1e-8)
print("TABLE" + json.dumps({"names": ["const"] + FEAT, "coef": [round(float(v), 2) for v in b], "se": [round(float(v), 2) for v in se]}))
# stated side number in l13: persistence 1.2128 and AR(1) 1.1574 when the first test row is left out
sp = pd.read_csv("spread-daily.csv").spread_bp.to_numpy()
tr_ = sp[:400]; A = np.polyfit(tr_[:-1], tr_[1:], 1); prev = sp[400:-1]; nxt = sp[401:]
two("l13 persistence without the first row", round(float(np.mean((nxt - prev) ** 2)), 4), 1.2128)
two("l13 AR(1) without the first row", round(float(np.mean((nxt - (A[1] + A[0] * prev)) ** 2)), 4), 1.1574)
m2 = sm.OLS(tr_[1:], sm.add_constant(tr_[:-1])).fit(); pr2 = m2.predict(sm.add_constant(prev, has_constant="add"))
two("l13 AR(1) without the first row, statsmodels", round(float(np.mean((nxt - pr2) ** 2)), 4), 1.1574)
# l14 edge: the same forest with other leaf sizes, scored on the same test rows (method A: forest.predict; method B: mean of the trees' predictions)
from sklearn.ensemble import RandomForestRegressor
for leaf in (1, 5, 10):
    rf = RandomForestRegressor(300, min_samples_leaf=leaf, random_state=0).fit(tr[FEAT], tr.price_k)
    pa = rf.predict(te[FEAT]); pb = np.mean([t.predict(te[FEAT].to_numpy()) for t in rf.estimators_], axis=0)
    ra = float(np.sqrt(np.mean((te.price_k.to_numpy() - pa) ** 2))); rb = float(np.sqrt(np.mean((te.price_k.to_numpy() - pb) ** 2)))
    two(f"l14 forest leaf {leaf} RMSE", ra, rb, 1e-9); print("     forest leaf", leaf, round(ra, 4))
done()
