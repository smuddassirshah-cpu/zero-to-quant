import json, math
import numpy as np, pandas as pd
from chk import two, done
h = pd.read_csv("data/houses.csv")
print("ids sorted:", bool((h.id.diff().dropna() > 0).all()), "n", len(h))

def report(df, seed=0, B=2000):
    d = df[df.price_k <= 5000].sort_values("id")
    price = d.price_k.to_numpy(float); err = price - price.mean()
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(err), (B, len(err)))
    draws = np.sqrt((err[idx] ** 2).mean(axis=1))
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(n=len(d), mean_price=float(price.mean()), rmse=float(np.sqrt((err ** 2).mean())), lo=float(lo), hi=float(hi)), draws

def loop_draws(df, seed, B=2000):
    d = df[df.price_k <= 5000].sort_values("id"); price = d.price_k.to_numpy(float); err = price - price.mean()
    rng = np.random.default_rng(seed); out = []
    for _ in range(B): out.append(math.sqrt(float((err[rng.integers(0, len(err), len(err))] ** 2).mean())))
    return np.array(out)

r0, d0 = report(h, 0); r1, d1 = report(h, 1)
two("vectorised vs loop draws identical", float(np.abs(d0 - loop_draws(h, 0)).max()), 0.0, 1e-12)
two("same seed identical", float(np.abs(report(h, 0)[1] - d0).max()), 0.0, 0.0)
two("different seed differs", float(np.abs(d1 - d0).max() > 0), 1.0)
sh = h.sample(frac=1, random_state=1); two("shuffled rows same report after sorting by id", report(sh, 0)[0]["lo"], r0["lo"], 0.0)
# method B for the percentile: sorted draws and linear interpolation by hand
s = sorted(d0.tolist()); k = 0.025 * (len(s) - 1); lo_a = s[int(k)] + (k - int(k)) * (s[int(k) + 1] - s[int(k)]); k = 0.975 * (len(s) - 1); hi_a = s[int(k)] + (k - int(k)) * (s[int(k) + 1] - s[int(k)])
two("lo percentile by hand", lo_a, r0["lo"], 1e-12); two("hi percentile by hand", hi_a, r0["hi"], 1e-12)
print("JSON:" + json.dumps({"r0": r0, "r1": r1, "sd": float(d0.std()), "draws": [round(float(v), 3) for v in d0], "below_lo": int((d0 < r0["lo"]).sum()), "min": float(d0.min()), "max": float(d0.max())}))
done()
