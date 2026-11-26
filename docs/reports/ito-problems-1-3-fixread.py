"""Fix-pass read of ito problems 1-3 (content commit 1fade7ab). Exits 0 when every changed figure recomputes."""
import math
from fractions import Fraction as F
import numpy as np
rng = np.random.default_rng(13)
bad = []
def chk(name, ok, shown):
    print(("ok  " if ok else "FAIL"), name, shown)
    if not ok: bad.append(name)

# problems-1 p-maker-tally part 3
p, n, a = F(507, 1000), 625, 40
mean1 = a * (2 * p - 1)
var_exact = n * (a * a - mean1 ** 2)                 # way 1: E[x^2] - mean^2
var_alt = n * a * a * 4 * p * (1 - p)                # way 2: 4pq a^2
chk("walk daily variance 999,804", var_exact == var_alt == 999804, float(var_exact))
qv = n * a * a
gap = (qv - var_exact) / qv
chk("gap within 0.02%", 0 < gap <= F(2, 10000), f"{float(gap)*100:.4f}%")
wins = rng.binomial(n, float(p), size=2_000_000)
pnl = a * (2 * wins - n)
chk("simulated daily variance", abs(pnl.var() / 999804 - 1) < 0.005, round(float(pnl.var())))
chk("walk QV fixed at 1,000,000 on every path", qv == 1_000_000, qv)
# QV of X_t = 350 t + sigma W_t over [0,1] is sigma^2 (Shreve 3.4.2, 4.4): fine partition
m = 200_000; sig = 1000.0
dX = 350 / m + sig * rng.normal(0, math.sqrt(1 / m), size=m)
chk("QV of drifted BM over a day = sigma^2", abs((dX ** 2).sum() / sig ** 2 - 1) < 0.02, float((dX ** 2).sum()))
sd5 = math.sqrt(5 * qv)
chk("week sd 2236.068", abs(sd5 - 2236.068) < 1e-3, sd5)
sd5_var = math.sqrt(5 * 999804)
chk("variance-matched sd also keys (tol 0.5)", abs(sd5_var - 2236.068) < 0.5, sd5_var)
chk("slips 5000, 1000 stay outside tol", min(abs(5000 - sd5), abs(1000 - sd5)) > 1, "")

# problems-2 p-results-vol part 1
v = F(4, 10) ** 2 * F(1, 4) + F(15, 100) ** 2 * F(3, 4)
chk("integrated variance 0.056875", v == F(56875, 1000000), float(v))
k = 400
sigt = np.where((np.arange(k) + 0.5) / k < 0.25, 0.4, 0.15)
I = (rng.normal(0, math.sqrt(1 / k), size=(100_000, k)) * sigt).sum(axis=1)
kurt = ((I - I.mean()) ** 4).mean() / I.var() ** 2
chk("simulated integral: variance and normal kurtosis", abs(I.var() / float(v) - 1) < 0.02 and abs(kurt - 3) < 0.1, (round(float(I.var()), 5), round(float(kurt), 3)))
# why 'deterministic' is needed: a random integrand (sigma_t = |W_t|) is not normal
W = np.cumsum(rng.normal(0, math.sqrt(1 / k), size=(100_000, k)), axis=1)
dW = np.diff(np.concatenate([np.zeros((100_000, 1)), W], axis=1), axis=1)
J = (np.abs(np.concatenate([np.zeros((100_000, 1)), W[:, :-1]], axis=1)) * dW).sum(axis=1)
kJ = ((J - J.mean()) ** 4).mean() / J.var() ** 2
chk("random integrand is not normal (kurtosis > 3.5)", kJ > 3.5, round(float(kJ), 2))

# problems-3 p-bridge-closes part 4
closes = [105.00, 107.60, 111.20, 110.30, 109.40]
b = math.log(112); s2 = 0.28 ** 2 / 252
touch = [math.exp(-2 * (b - math.log(x)) * (b - math.log(y)) / s2) for x, y in zip(closes, closes[1:])]
surv = math.prod(1 - t for t in touch)
chk("touch chances and survival 0.3837", [round(t, 4) for t in touch[1:]] == [0.1577, 0.4942, 0.0993] and abs(surv - 0.383717) < 1e-5, (touch, surv))
df = math.exp(-0.045 * 4 / 252)
chk("discount factor 0.999286", round(df, 6) == 0.999286, df)
ans = df * 9.40 * surv
chk("key 3.604419", abs(ans - 3.604419) < 5e-6, ans)
ans2 = round(df, 6) * 9.40 * 0.3837                   # way 2: the rounded figures the learner is handed
chk("learner's rounded route within tol", abs(ans2 - 3.604419) < 0.01 and round(ans2, 2) == 3.60, ans2)
chk("plain figure 9.3933", round(df * 9.40, 4) == 9.3933, df * 9.40)
for nm, val, w in [("plain", 9.39, 1), ("knock-in", 5.79, 1 - 0.3837), ("one-gap", 4.75, 1 - 0.4942), ("sum-rule", 2.34, 1 - (0.1577 + 0.4942 + 0.0993))]:
    chk(f"slip {nm}", abs(df * 9.40 * w - val) < 0.005 and abs(val - ans) > 0.02, round(df * 9.40 * w, 4))
alt = [math.exp(-0.045 * 4 / 365) * 9.40 * surv, 9.40 * surv]
chk("365-day clock and no discount also inside tol 0.01", all(abs(x - 3.604419) < 0.01 for x in alt), alt)
# bridge touch chance by simulation for the part 2 gap
x, y = math.log(111.20), math.log(110.30); st = 2000
t = np.arange(1, st + 1) / st
Wb = np.cumsum(rng.normal(0, math.sqrt(s2 / st), size=(20_000, st)), axis=1)
br = x + Wb - t * Wb[:, -1:] + t * (y - x)
est = (br.max(axis=1) >= b).mean()
chk("bridge touch simulated near 0.4942 (discrete grid reads low)", 0.46 < est < 0.50, float(est))
raise SystemExit(1 if bad else 0)
