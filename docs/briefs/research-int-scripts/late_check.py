"""research-int: late items (H2.5 PCA table, the E8 clean-frame drill, H2.4 soft threshold)."""
import math
import numpy as np, pandas as pd
from chk import two, done
C = np.array([[0.09, 0.012], [0.012, 0.01]]); tr, dt = 0.10, 0.09*0.01-0.012**2
l1 = (tr+math.sqrt(tr*tr-4*dt))/2; l2 = (tr-math.sqrt(tr*tr-4*dt))/2; e = np.sort(np.linalg.eigvalsh(C))[::-1]
two("H2.5 eig1", l1, float(e[0]), 1e-12); two("H2.5 eig2", l2, float(e[1]), 1e-12); two("H2.5 share", l1/tr, float(e[0]/e.sum()), 1e-12)
two("H2.5 corr used 0.012/(0.3*0.1) = 0.4", 0.012/(0.3*0.1), 0.4, 1e-12); two("H2.5 standardised share 0.70", (1+0.4)/2, float(np.linalg.eigvalsh(np.array([[1, .4], [.4, 1]]))[-1]/2), 1e-12)
print("      eigs", round(l1, 6), round(l2, 6), "share", round(l1/tr, 4))
rows = [(1, " alpha ", "1,200", 10.0), (2, "ALPHA", "300", -999.0), (3, "bravo", "500", 20.0), (3, "BRAVO", "500", 20.0), (4, "Bravo", "2,500", None), (5, " ALPHA", "100", 11.0)]
df = pd.DataFrame(rows, columns=["order_id", "symbol", "qty", "price"])
d = df.assign(symbol=df.symbol.str.strip().str.upper(), qty=df.qty.str.replace(",", "").astype(int)).drop_duplicates("order_id"); d = d[d.price.notna() & (d.price > 0)]
two("drill: rows left", len(d), 3); manual = [(r[0], r[1].strip().upper(), int(r[2].replace(",", "")), r[3]) for r in rows]
seen = set(); keep = []
for o, s, q, p in manual:
    if o in seen: continue
    seen.add(o)
    if p is None or p <= 0: continue
    keep.append((o, s, q, p))
two("drill: rows left by loop", len(keep), 3)
va = sum(p*q for o, s, q, p in keep if s == "ALPHA")/sum(q for o, s, q, p in keep if s == "ALPHA"); vb = float((d[d.symbol == "ALPHA"].price*d[d.symbol == "ALPHA"].qty).sum()/d[d.symbol == "ALPHA"].qty.sum())
two("drill: ALPHA VWAP 13100/1300", va, vb, 1e-12); two("   value", va, 13100/1300, 1e-12); print("      ", va)
two("H2.4 soft(1.9, 1) = 0.9", 0.9, float(np.sign(1.9)*max(1.9-1, 0)), 1e-12); two("H2.4 soft(-0.8, 1) = 0", 0.0, float(max(abs(-0.8)-1, 0)), 1e-12); two("H2.4 soft(3.5,1)=2.5", 2.5, 3.5-1, 1e-12)

# l14: area-only slope on all 396 clean rows against all 400 rows (typo prices kept), two methods
h = pd.read_csv("data/houses.csv"); clean = h[h.price_k <= 5000]
import statsmodels.api as sm
def slope_hand(d): return float(np.cov(d.area_m2, d.price_k, ddof=1)[0, 1]/np.var(d.area_m2, ddof=1))
two("l14 area slope, 396 clean rows (cov/var vs statsmodels)", slope_hand(clean), float(sm.OLS(clean.price_k, sm.add_constant(clean.area_m2.astype(float))).fit().params["area_m2"]), 1e-9)
two("l14 area slope, all 400 rows", slope_hand(h), float(sm.OLS(h.price_k, sm.add_constant(h.area_m2.astype(float))).fit().params["area_m2"]), 1e-9)
print("      clean", round(slope_hand(clean), 4), " all 400", round(slope_hand(h), 4), " mean price clean", round(float(clean.price_k.mean()), 3))
two("R4.1 naive unsorted bracket (3,30),(1,10) at 2.5 = 25", 30+(10-30)*(2.5-3)/(1-3), float(np.polyval(np.polyfit([3, 1], [30, 10], 1), 2.5)), 1e-9)

from scipy import stats
for n in (250, 500, 1000, 1535):
    r = 0.05; t = r*math.sqrt(n-2)/math.sqrt(1-r*r); fit_t = stats.pearsonr  # second route: t from the exact-moment sample regression
    g = np.random.default_rng(n).standard_normal((n, 2)); g -= g.mean(0); q, _ = np.linalg.qr(g); q *= math.sqrt(n-1); xx = q[:, 0]; yy = r*xx+math.sqrt(1-r*r)*q[:, 1]
    lr = stats.linregress(xx, yy); two(f"l10 t at n={n}", t, lr.slope/lr.stderr, 1e-9); print("      n", n, "t", round(t, 4))
done()
