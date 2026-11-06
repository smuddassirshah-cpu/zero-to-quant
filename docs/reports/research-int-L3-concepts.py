"""Concept checks for research-int level 3 (l11 to l15, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/research-int-L3-concepts.py
Each assert names the ledger row it covers (docs/reports/audit-research-int-1-3-ledger.md).
Needs app/content/data/{futures-daily,spread-daily,houses}.csv for the data checks.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(20261106)
fails = []
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "app", "content", "data")


def check(cond, msg):
    if cond:
        print("ok   ", msg)
    else:
        print("FAIL ", msg)
        fails.append(msg)


def framing(c):
    c = np.asarray(c, float)
    r = np.diff(np.log(c))
    return (np.corrcoef(c[:-1], c[1:])[0, 1] ** 2, np.corrcoef(r[:-1], r[1:])[0, 1] ** 2,
            np.sqrt(np.mean(np.diff(c) ** 2)), np.sqrt(np.mean(r ** 2)))


# ---------------------------------------------------------------- l11: framing
fut = os.path.join(DATA, "futures-daily.csv")
if os.path.exists(fut):
    c = pd.read_csv(fut)["close"].to_numpy(float)
    f = framing(c)
    check(np.allclose(f, [0.9943951, 0.0152529, 57.780408, 0.01037423], atol=[1e-6, 1e-6, 1e-5, 1e-7]), "l11 s1: R^2 0.9944 on prices, 0.0153 on returns, miss 57.78 points, RMS return 0.01037")
    check(np.isclose(c.mean(), 5561.9, atol=0.1) and np.isclose(0.1235 ** 2, 0.0153, atol=1e-4), "l11 s1 explain: mean close 5,561.9; return R^2 is the squared lag-1 correlation")
    # the price R^2 is persistence: a random walk with the same returns scores about the same
    walk = c[0] * np.exp(np.cumsum(rng.permutation(np.diff(np.log(c)))))
    check(np.corrcoef(walk[:-1], walk[1:])[0, 1] ** 2 > 0.98, "l11 s4 and r3 item7: shuffled returns rebuilt into a walk still give R^2 near 0.99 on levels (persistence, not skill)")
    # tiny file
    check(np.allclose(framing([200, 204, 202, 207, 205, 210, 208, 213]), [0.2485294117647059, 0.9908097897584781, 3.835920452027872, 0.018585139765335365]), "l11 s1 test: tiny file values")
else:
    check(False, "l11 s1: futures-daily.csv not found")
# sqrt(h) scaling
r = rng.normal(0, 0.01, (200_000, 21))
check(abs(r.sum(1).std() - 0.01 * np.sqrt(21)) < 2e-4 and np.isclose(np.sqrt(21), 4.583, atol=5e-4) and np.isclose(np.sqrt(252), 15.87, atol=5e-3), "l11 s2 and s7: 21 independent days have spread sqrt(21) x daily; 252 days 15.87x")
check(np.isclose(0.7 * np.sqrt(30), 3.834, atol=5e-4) and np.isclose(0.8 * np.sqrt(10), 2.530, atol=5e-4), "l11 quiz0 and r3 item4: 3.834% and 2.530%")
# the sum of log returns against percentages
check(np.isclose(np.log(1.1) + np.log(0.9), np.log(0.99)) and np.isclose(np.log(0.99), -0.01005, atol=5e-6) and np.isclose(np.log(1.02) + np.log(101 / 102), np.log(1.01)), "l11 s5 and quiz3: log returns add; ln 0.99 = -1.005%, ln 1.01 = 0.995%")
# scores on the three-day table
fc, ac = np.array([0.2, -0.1, 0.3]), np.array([0.5, 0.1, -0.2])
check(np.isclose(np.mean((ac - fc) ** 2), 0.1267, atol=5e-5) and np.isclose(np.mean(np.sign(fc) == np.sign(ac)), 1 / 3) and np.isclose((np.sign(fc) * ac).sum(), 0.2), "l11 s3: MSE 0.1267, hit rate 1/3, profit 0.2%")
fc, ac = np.array([0.4, 0.2, -0.3]), np.array([0.1, -0.2, -0.1])
check(np.isclose((np.sign(fc) * ac).sum(), 0) and np.isclose(np.mean(np.sign(fc) == np.sign(ac)), 2 / 3), "l11 quiz2: profit 0 with a 67% hit rate")
fc, ac = np.array([0.3, -0.2, 0.1, 0.4]), np.array([0.1, -0.5, 0.2, 0.6])
check(np.isclose(np.mean((ac - fc) ** 2), 0.045) and np.all(np.sign(fc) == np.sign(ac)), "r3 item0: MSE 0.045 with every sign right")
check(np.isclose(0.52 * 8 - 0.48 * 8, 0.32) and np.isclose(0.32 - 0.5, -0.18), "l11 s8: 52% hit rate on 8 bp moves, 0.5 bp cost: -0.18 bp")
# a 52% direction call loses after costs in simulation
moves = 8 * rng.choice([-1, 1], 400_000); right = rng.random(400_000) < 0.52
pnl = np.where(right, abs(moves), -abs(moves)) - 0.5
check(abs(pnl.mean() + 0.18) < 0.03, "l11 s8: Monte Carlo of the 52% caller nets about -0.18 bp a trade")
# overlapping long-horizon returns inflate R^2 without skill
ret = rng.normal(size=5000); sig = rng.normal(size=5000)
r2_1 = np.corrcoef(sig[:-1], ret[1:])[0, 1] ** 2
h = 20; long_ret = np.convolve(ret, np.ones(h), "valid"); long_sig = np.convolve(sig, np.ones(h), "valid")
r2_h = np.corrcoef(long_sig[:-h], long_ret[h:])[0, 1] ** 2
print(f"      l11 s9 option long: pure-noise R^2 at horizon 1 is {r2_1:.4f}, overlapping 20-day sums give {r2_h:.4f}")
check(r2_h > 5 * r2_1, "l11 s9 option long why: overlapping long-horizon returns inflate R^2 on pure noise")

# ---------------------------------------------------------------- l12: features
def feature_corrs(df):
    df = df.copy()
    df["ret"] = np.log(df["close"]).diff(); df["y"] = df["ret"].shift(-1)
    df["mean5"] = df["ret"].rolling(5).mean(); df["centred3"] = df["ret"].rolling(3, center=True).mean()
    df["logvol"] = np.log(df["volume"])
    d = df.dropna(subset=["y", "ret", "mean5", "centred3"])
    return {c: float(d[c].corr(d["y"])) for c in ["ret", "mean5", "logvol", "centred3"]}, len(d)
if os.path.exists(fut):
    out, nrow = feature_corrs(pd.read_csv(fut))
    check(np.allclose([out[k] for k in ("ret", "mean5", "logvol", "centred3")], [0.126083, 0.0285335, 0.0303372, 0.6086035], atol=1e-6) and nrow == 994, "l12 s2: 0.1261, 0.0285, 0.0303, 0.6086 on 994 rows")
    check(np.isclose(0.6086 ** 2, 0.37, atol=0.005), "l12 s4: R^2 of the centred mean is 0.37")
    tiny = pd.DataFrame({"close": [100, 102, 101, 104, 103, 107, 105, 108, 110, 109, 113, 112], "volume": [1000, 1100, 900, 1300, 1200, 1500, 1100, 1400, 1700, 1600, 2000, 1800]})
    out, _ = feature_corrs(tiny)
    check(np.allclose([out[k] for k in ("ret", "mean5", "logvol", "centred3")], [-0.8230710139959321, -0.44114985645770866, -0.529172653444366, 0.7981286387830613]), "l12 s2 test: twelve-row file")
    # pandas rolling windows end at the current row; center=True reaches one day ahead
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    check(s.rolling(3).mean().iloc[4] == 4.0 and s.rolling(3, center=True).mean().iloc[2] == 3.0 and np.isnan(s.rolling(3, center=True).mean().iloc[4]), "l12 s2 hint and l10 quiz3: rolling(w) ends at the current row; center=True spans t-1, t, t+1")
# leakage correlation 1/sqrt(w)
r = rng.normal(size=400_000)
for w, target in [(3, 1 / np.sqrt(3)), (2, 1 / np.sqrt(2)), (5, 1 / np.sqrt(5))]:
    m = np.convolve(r, np.ones(w) / w, "valid")
    assert abs(np.corrcoef(m, r[w - 1:])[0, 1] - target) < 0.005
check(True, "l12 s7, quiz2, h3 item6: a mean of w independent returns holding the label correlates 1/sqrt(w) with it")
check(np.isclose((0.8 - 0.3 + 0.4) / 3, 0.3) and np.isclose((0.2 + 0.8 - 0.3) / 3, 0.2333, atol=5e-5) and np.isclose((-0.3 + 0.7) / 2, 0.2) and np.isclose((-0.3 + 0.5 + 0.2 + 0.7) / 4, 0.275), "l12 s1, quiz1, r3 item5: shifted rolling means")
check(np.isclose(6 - (2 + 4 + 6) / 3, 2) and np.isclose(np.mean([2, 4, 6, 8, 20]), 8), "l12 s5: expanding mean 4 against the full-sample mean 8")
# shuffled label test: a pipeline that fits a scaler on all rows keeps a score above chance; an honest one does not
n = 2000; X = rng.normal(size=(n, 3)); y = X @ np.array([1.0, 0.5, 0]) + rng.normal(size=n)
ys = rng.permutation(y)
m = LinearRegression().fit(X[:1000], ys[:1000]); sc = 1 - np.mean((ys[1000:] - m.predict(X[1000:])) ** 2) / np.var(ys[1000:])
check(abs(sc) < 0.02, "l12 s9 step d: with the label shuffled an honest pipeline scores at chance on a later period")

# ---------------------------------------------------------------- l13: baselines
def ar1_errors(phi, s2=1.0):
    return {"ar1": s2, "persist": 2 * s2 / (1 + phi), "mean": s2 / (1 - phi ** 2)}
e = ar1_errors(0.9)
check(np.isclose(e["persist"], 1.0526, atol=5e-5) and np.isclose(e["mean"], 5.263, atol=5e-4) and np.isclose(0.1 ** 2 * 5.263 + 1, 1.0526, atol=5e-5), "l13 s0 and s8: persistence 2/(1+phi) = 1.0526, mean 5.263, AR(1) 1")
check(np.isclose(ar1_errors(0.7)["mean"], 1.9608, atol=5e-5) and np.isclose(ar1_errors(0.65)["persist"], 1.2121, atol=5e-5) and np.isclose(ar1_errors(0.8)["persist"], 1.1111, atol=5e-5) and np.isclose(ar1_errors(0.65)["mean"], 1.7316, atol=5e-5), "l13 quiz0, r3 item2, h3 item7")
check(np.isclose(1 - 1 / (2 / 1.95), 0.025) and np.isclose((1 - 0.95) / 2, 0.025), "l13 s9: gain over persistence is (1 - phi)/2 = 2.5% at phi = 0.95")
# Monte Carlo of an AR(1) with known parameters
phi, T = 0.9, 400_000
x = np.empty(T); x[0] = 50 + rng.normal() * np.sqrt(5.263)
eps = rng.normal(size=T)
for t in range(1, T):
    x[t] = 50 + phi * (x[t - 1] - 50) + eps[t]
check(abs(np.mean((x[1:] - x[:-1]) ** 2) - 1.0526) < 0.02 and abs(np.mean((x[1:] - 50) ** 2) - 5.263) < 0.1 and abs(np.mean((x[1:] - 50 - phi * (x[:-1] - 50)) ** 2) - 1) < 0.01, "l13 s0: Monte Carlo AR(1) errors 1.0526, 5.263, 1")
def baseline_scores(x, n_fit):
    x = np.asarray(x, float)
    train, prev, nxt = x[:n_fit], x[n_fit - 1:-1], x[n_fit:]
    slope, icpt = np.polyfit(train[:-1], train[1:], 1)
    return (np.mean((nxt - prev) ** 2), np.mean((nxt - train.mean()) ** 2), np.mean((nxt - (icpt + slope * prev)) ** 2))
spr = os.path.join(DATA, "spread-daily.csv")
if os.path.exists(spr):
    xs = pd.read_csv(spr)["spread_bp"].to_numpy(float)
    sc = baseline_scores(xs, 400)
    check(np.allclose(sc, [1.207112, 6.8195945, 1.1532709], atol=1e-6), "l13 s1: 1.2071, 6.8196, 1.1533 with 400 fitted")
    check(np.isclose(1 - sc[2] / sc[0], 0.0446, atol=5e-4), "l13 s2: AR(1) 4.46% below the best baseline")
    nxt, prev = xs[400:], xs[399:-1]
    slope, icpt = np.polyfit(xs[:-1], xs[1:], 1)
    leaked = np.mean((nxt - (icpt + slope * prev)) ** 2)
    check(np.isclose(leaked, 1.1518, atol=5e-4) and leaked < sc[2], "l13 s6: fitting on all 600 days flatters the test error to 1.1518")
    sc2 = baseline_scores(xs, 350)
    check(np.allclose(sc2, [1.1942044, 7.4129795, 1.1482173], atol=1e-6) and np.isclose(1 - sc2[2] / sc2[0], 0.039, atol=5e-4), "h3 item3: 1.1942, 7.4130, 1.1482, a 3.9% gain")
    gain = (nxt - prev) ** 2 - (nxt - (np.polyfit(xs[:399], xs[1:400], 1)[1] + np.polyfit(xs[:399], xs[1:400], 1)[0] * prev)) ** 2
    t_gain = gain.mean() / (gain.std(ddof=1) / np.sqrt(len(gain)))
    boots = np.array([rng.choice(gain, len(gain)).mean() for _ in range(5000)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    check(np.isclose(t_gain, 1.87, atol=0.03) and lo < 0 < hi and np.isclose(hi, 0.111, atol=0.01), f"l15 s8: per-day gain t = {t_gain:.2f}, bootstrap interval {lo:.3f} to {hi:.3f} touches zero")
    check(np.allclose(baseline_scores([50.0, 50.4, 49.8, 50.9, 50.2, 49.5, 50.1, 50.6, 49.9, 50.3, 50.8, 49.7], 6), [0.45333333333333203, 0.15555555555555475, 0.13724687539451944]), "l13 s1 test: tiny file")
else:
    check(False, "l13 s1: spread-daily.csv not found")
def futures_baselines(c, n_fit):
    r = np.diff(np.log(c)); train, test = r[:n_fit], r[n_fit:]
    prev = np.r_[train[-1], test[:-1]]
    slope, icpt = np.polyfit(train[:-1], train[1:], 1)
    return 1e4 * np.mean(test ** 2), 1e4 * np.mean((test - train.mean()) ** 2), 1e4 * np.mean((test - (icpt + slope * prev)) ** 2), slope
if os.path.exists(fut):
    fb = futures_baselines(c, 749)
    check(np.allclose(fb[:3], [1.0135, 1.016667, 1.022689], atol=1e-5) and np.isclose(fb[3], 0.1458, atol=5e-4), "l13 s3: zero 1.0135, mean 1.0167, AR(1) 1.0227; slope 0.1458")
    check(np.isclose(1 - fb[2] / fb[0], -0.0091, atol=5e-4), "l13 s4: out-of-sample R^2 against zero is -0.0091")
    check(np.allclose(futures_baselines(c, 500)[:3], [1.02721, 1.027422, 1.032173], atol=1e-5), "l13 s3 test: n_fit = 500")
    r = np.diff(np.log(c)); tr = r[:749]
    import statsmodels.api as sm
    m = sm.OLS(tr[1:], sm.add_constant(tr[:-1])).fit()
    check(np.isclose(m.tvalues[1], 4.02, atol=0.02) and m.nobs == 748, "l13 s4: in-sample slope t = 4.02 on 748 pairs")
# standard error of the out-of-sample R^2 on 250 days for an AR(1) return series with slope about 0.12
r2s = []
for _ in range(3000):
    rr = np.empty(999); rr[0] = rng.normal() * 0.0104; ee = rng.normal(size=999) * 0.0104 * np.sqrt(1 - 0.12 ** 2)
    for t in range(1, 999):
        rr[t] = 0.12 * rr[t - 1] + ee[t]
    z0, mn, a1, _ = futures_baselines(np.exp(np.cumsum(np.r_[0, rr])) * 5000, 749)
    r2s.append(1 - a1 / z0)
r2s = np.array(r2s)
check(0.012 < r2s.std() < 0.03, f"l13 s4 explain: the out-of-sample R^2 on 250 days has standard error about 0.02 (simulated sd {r2s.std():.3f} at a true slope 0.12)")
check(r2s.mean() > 0 and -0.0091 > r2s.mean() - 2 * r2s.std(), f"l13 s5 explain: an observed -0.0091 is within two standard errors of what a true slope near 0.1 produces (mean {r2s.mean():.4f}), so 'not shown' is the honest claim")
check(np.isclose(1 - 3.19 / 3.10, -0.029, atol=5e-4) and np.isclose(0.95 * 3.10, 2.945), "r3 item8: R^2 -0.029; 5% cut is 2.945")
check(np.isclose(1 - 3.8 / 4.0, 0.05) and np.isclose(1 - 24.9 / 62.4, 0.601, atol=5e-4) and np.isclose(1 - 131 / 312, 0.58, atol=5e-4), "l13 quiz2, r3 item3, h3 item0: percentage cuts")

# ---------------------------------------------------------------- l14: house price case
hp = os.path.join(DATA, "houses.csv")
if os.path.exists(hp):
    df = pd.read_csv(hp)
    check(len(df) == 400 and df["age_years"].isna().sum() == 20 and (df["price_k"] > 5000).sum() == 4, "l14 s0: 400 homes, 20 blank ages, 4 prices in pounds")
    d = df[df["price_k"] <= 5000].copy()
    d["age_years"] = d["age_years"].fillna(d["age_years"].median())
    d = pd.get_dummies(d, columns=["band"], drop_first=True, dtype=float)
    FEATURES = ["area_m2", "bedrooms", "age_years", "distance_km", "garden", "band_B", "band_C", "band_D"]
    tr, te = train_test_split(d, test_size=0.25, random_state=0)
    Xtr, Xte, ytr, yte = tr[FEATURES], te[FEATURES], tr["price_k"], te["price_k"]
    check(len(d) == 396 and len(tr) == 297 and len(te) == 99, "l14 s1: 396 clean rows, 297 train, 99 test")
    base = np.sqrt(np.mean((yte - ytr.mean()) ** 2))
    area = LinearRegression().fit(Xtr[["area_m2"]], ytr); rm_area = np.sqrt(np.mean((yte - area.predict(Xte[["area_m2"]])) ** 2))
    full = LinearRegression().fit(Xtr, ytr); rm_full = np.sqrt(np.mean((yte - full.predict(Xte)) ** 2))
    check(np.isclose(base, 85.0489, atol=0.005) and np.isclose(rm_area, 46.8608, atol=0.005) and np.isclose(rm_full, 29.6582, atol=0.01), "l14 s1 to s3: RMSE 85.05, 46.86, 29.66")
    check(np.isclose(1 - rm_area / base, 0.45, atol=0.01) and np.isclose(1 - rm_full / base, 0.651, atol=0.001) and np.isclose(1 - (rm_full / base) ** 2, 0.8784, atol=0.001), "l14 s2, s3 and l15 s2: cuts 45% and 65.1%; out-of-sample R^2 0.8784")
    check(np.allclose(full.coef_[[1, 4, 5]], [6.6594, 17.6867, -26.405], atol=0.01), "l14 s3: coefficients bedrooms 6.66, garden 17.69, band B -26.40")
    import statsmodels.api as sm
    ols = sm.OLS(ytr, sm.add_constant(Xtr)).fit()
    check(np.isclose(ols.bse["bedrooms"], 2.39, atol=0.01) and np.isclose((9 - 6.66) / 2.39, 0.98, atol=0.01), "l14 s5: SE of bedrooms 2.39; 9 is 0.98 SE away")
    rab = np.corrcoef(Xtr["area_m2"], Xtr["bedrooms"])[0, 1]
    check(np.isclose(rab, 0.7638, atol=0.001) and np.isclose(1 / (1 - rab ** 2), 2.40, atol=0.01) and np.isclose(np.sqrt(2.40), 1.549, atol=0.001), "l14 s5 explain: corr 0.7638, pair VIF 2.40, SE factor 1.549")
    # collinearity does not bias: OLS on correlated regressors is unbiased in simulation
    bs = []
    for _ in range(2000):
        a = rng.normal(size=200); bdr = 0.76 * a + np.sqrt(1 - 0.76 ** 2) * rng.normal(size=200)
        yy = 2 * a + 3 * bdr + rng.normal(size=200)
        bs.append(np.linalg.lstsq(np.c_[np.ones(200), a, bdr], yy, rcond=None)[0][2])
    check(abs(np.mean(bs) - 3) < 0.02, "l14 s5 and summary: collinearity widens the standard error and does not bias the estimate (simulated mean of 2000 fits)")
    # forest and log model
    rf = RandomForestRegressor(300, min_samples_leaf=3, random_state=0).fit(Xtr, ytr)
    rm_rf = np.sqrt(np.mean((yte - rf.predict(Xte)) ** 2))
    lg = LinearRegression().fit(Xtr, np.log(ytr)); rm_log = np.sqrt(np.mean((yte - np.exp(lg.predict(Xte))) ** 2))
    check(np.isclose(rm_rf, 40.4417, atol=0.05) and np.isclose(rm_log, 32.9514, atol=0.01), "l14 s4: forest 40.44, log-linear 32.95; neither beats 29.66")
    # Duan smearing: exp(prediction) estimates a median-type quantity, not the conditional mean
    smear = np.mean(np.exp(np.log(ytr) - lg.predict(Xtr)))
    rm_smear = np.sqrt(np.mean((yte - smear * np.exp(lg.predict(Xte))) ** 2))
    print(f"      l14 s4 note: smearing factor {smear:.4f}; RMSE with it {rm_smear:.3f} against {rm_log:.3f} without (Wooldridge 6.4: exp of a log prediction underestimates E[y|x])")
    check(smear > 1.0, "l14 s4 and h3 item4: exp of the log fit is biased low for the mean price (smearing factor above 1)")
    # all 400 rows: the slope on area jumps
    sl_all = np.polyfit(df["area_m2"], df["price_k"], 1)[0]; sl_clean = np.polyfit(d["area_m2"], d["price_k"], 1)[0]
    check(np.isclose(sl_all, 71.70, atol=0.05) and np.isclose(sl_clean, 2.81, atol=0.01) and np.isclose(sl_all / sl_clean, 25.5, atol=0.1), "l14 s6: slope 71.70 against 2.81, 25.5 times")
    # leaf sizes tuned on the test rows
    scores = {}
    for leaf in (1, 3, 5, 10):
        m = RandomForestRegressor(300, min_samples_leaf=leaf, random_state=0).fit(Xtr, ytr)
        scores[leaf] = np.sqrt(np.mean((yte - m.predict(Xte)) ** 2))
    check(np.allclose([scores[k] for k in (1, 3, 5, 10)], [40.60, 40.44, 41.50, 43.84], atol=0.05), "l14 s8: leaf sizes 1, 3, 5, 10 score 40.60, 40.44, 41.50, 43.84")
    # bootstrap of the test RMSE
    err = (yte - full.predict(Xte)).to_numpy()
    boots = np.array([np.sqrt(np.mean(rng.choice(err, len(err)) ** 2)) for _ in range(5000)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    check(abs(lo - 24.87) < 0.6 and abs(hi - 34.22) < 0.6, f"l15 s0: bootstrap 95% interval of the test RMSE is about 24.9 to 34.2 (this seed: {lo:.2f} to {hi:.2f})")
    check(np.isclose((34.22 - 24.87) / 2, 4.675), "l15 s1: half-width 4.675")
    gain_row = (yte - ytr.mean()) ** 2 - err ** 2
    gb = np.array([rng.choice(gain_row, len(gain_row)).mean() for _ in range(5000)])
    check(np.isclose(gain_row.mean(), 6353.7, atol=1) and np.percentile(gb, 2.5) > 0, "l15 s2 explain: per-row gain 6,353.7 with a bootstrap interval that excludes zero")
    # interval width falls like 1/sqrt(n): bootstrap on 4x the rows (resampled errors)
    err4 = np.tile(err, 4)
    b4 = np.array([np.sqrt(np.mean(rng.choice(err4, len(err4)) ** 2)) for _ in range(5000)])
    w1, w4 = hi - lo, np.diff(np.percentile(b4, [2.5, 97.5]))[0]
    check(abs(w1 / w4 - 2) < 0.2, f"l15 s5 and quiz1: four times the rows halves the width ({w1:.2f} against {w4:.2f})")
    # h3 item4: log model with the 80/20 split
    X = d.drop(columns=["id", "price_k"]); y = d["price_k"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=1)
    m = LinearRegression().fit(X_tr, np.log(y_tr))
    rmse = np.sqrt(np.mean((y_te - np.exp(m.predict(X_te))) ** 2)); g = dict(zip(X.columns, m.coef_))["garden"]
    check(np.isclose(rmse, 28.76694122, atol=0.001) and np.isclose(100 * g, 7.251774340, atol=0.001), "h3 item4: RMSE 28.77, garden coefficient 7.25%")
    print(f"      h3 item4 note: exact proportional effect of the garden dummy is exp({g:.4f}) - 1 = {100*(np.exp(g)-1):.2f}% (Halvorsen and Palmquist 1980)")
else:
    check(False, "l14: houses.csv not found")
check(np.isclose(np.sqrt(2 * 120 ** 2 / 4), 84.85, atol=0.01) and np.isclose(90 / 84.85, 1.06, atol=0.01), "l14 s9: SE of a difference of two means of 4 is 84.85; the gap is 1.06 SE")
check(np.isclose(np.sqrt(1 / (1 - 0.81)), 2.294, atol=5e-4) and np.isclose(1 / (1 - 0.5625), 2.2857, atol=5e-5) and np.isclose(np.sqrt(2.2857), 1.5119, atol=5e-5) and np.isclose(1 / (1 - 0.82 ** 2), 3.05, atol=0.01), "l14 quiz2, r3 item6, h3 item0: VIF and its root")
check(np.isclose(1 - (16.4 / 41) ** 2, 0.84) and np.isclose(1 - (28 / 40) ** 2, 0.51) and np.isclose(1 - (131 / 312) ** 2, 0.8237, atol=5e-4) and np.isclose(1 - (212 / 498) ** 2, 0.82, atol=0.005), "l14 quiz1, l15 quiz2, h3 item0 and item5: out-of-sample R^2 from RMSE ratios")
# dummy trap: four dummies plus intercept are collinear
D = np.c_[np.ones(8), np.eye(4)[np.arange(8) % 4]]
check(np.linalg.matrix_rank(D) == 4, "l14 quiz3: four dummies and an intercept have rank 4, not 5")
# h3 item2 features
if os.path.exists(fut):
    out = pd.read_csv(fut)
    out["ret"] = np.log(out["close"]).diff(); out["mean10"] = out["ret"].rolling(10).mean()
    lv = np.log(out["volume"]); out["vol_rel"] = lv - lv.rolling(20).mean(); out["y"] = out["ret"].shift(-1)
    check(np.isclose(out["mean10"].iloc[25], 0.0010172139996774022) and np.isclose(out["vol_rel"].iloc[100], 0.3826938053002724) and np.isclose(out["y"].iloc[500], 0.008563024651925488) and int(out["mean10"].first_valid_index()) == 10 and len(out.dropna(subset=["ret", "mean10", "vol_rel", "y"])) == 980 and np.isnan(out["y"].iloc[-1]), "h3 item2: hidden test values, first mean10 at row 10, 980 complete rows, last y missing")

print()
if fails:
    print(f"{len(fails)} check(s) failed:")
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
print("all checks passed")
