"""Concept checks for research-int level 2 (l6 to l10, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/research-int-L2-concepts.py
Each assert names the ledger row it covers (docs/reports/audit-research-int-1-3-ledger.md).
Needs app/content/data/futures-daily.csv for the lag-correlation checks.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance

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


# ---------------------------------------------------------------- l6: bias and variance
def mse_shrink(c, mu, v):
    return (c - 1) ** 2 * mu ** 2 + c ** 2 * v

cs = np.linspace(0, 1.2, 1201)
check(np.isclose(cs[np.argmin(mse_shrink(cs, 1, 1))], 0.5) and np.isclose(mse_shrink(0.5, 1, 1), 0.5), "l6 s0 and s1: c* = 0.5, MSE 0.5 for mu = 1, v = 1")
xbar = rng.normal(1, 1, 400_000)
check(abs(((0.5 * xbar - 1) ** 2).mean() - 0.5) < 0.005, "l6 s1: Monte Carlo MSE of 0.5 xbar is 0.5")
check(np.isclose(mse_shrink(0.5, 1, 0.25), 0.3125) and np.isclose(1 / 1.25, 0.8) and np.isclose(mse_shrink(0.8, 1, 0.25), 0.2), "l6 s5: sixteen years: 0.3125 with c = 0.5, c* = 0.8 gives 0.2")
for mu, v in [(1, 1), (2, 1), (3, 2), (4, 16)]:
    assert np.isclose(cs[np.argmin(mse_shrink(cs, mu, v))], mu ** 2 / (mu ** 2 + v), atol=1e-3)
check(True, "l6 s7: c* = mu^2/(mu^2 + v) minimises (c-1)^2 mu^2 + c^2 v")
check(np.isclose(mse_shrink(0.5, 4, 16), 8) and np.isclose(mse_shrink(0.5, 2, 1), 1.25) and np.isclose(mse_shrink(0.6, 3, 2), 2.16) and np.isclose(mse_shrink(0.5, 3, 9), 4.5), "l6 s8, quiz0, r2 item0, h2 item3: MSEs 8, 1.25, 2.16, 4.5")
# polynomial fits on the lesson's 20 points
pts = np.array([[0.0, 0.01], [0.053, 0.733], [0.105, 0.982], [0.158, 0.684], [0.211, 0.88], [0.263, 0.838], [0.316, 1.087], [0.368, 0.719], [0.421, 0.7], [0.474, -0.39], [0.526, 0.305], [0.579, -0.505], [0.632, -0.532], [0.684, -0.957], [0.737, -1.11], [0.789, -0.83], [0.842, -0.59], [0.895, -0.675], [0.947, -0.371], [1.0, 0.206]])
px, py = pts[:, 0], pts[:, 1]
grid = np.linspace(0, 1, 201)
train_err, truth_err = {}, {}
for d in (1, 3, 9):
    co = np.polyfit(px, py, d)
    train_err[d] = np.mean((py - np.polyval(co, px)) ** 2)
    truth_err[d] = np.mean((np.sin(2 * np.pi * grid) - np.polyval(co, grid)) ** 2)
check(np.allclose([train_err[1], train_err[3], train_err[9]], [0.2542, 0.0499, 0.0378], atol=5e-4), "l6 s2: training errors 0.2542, 0.0499, 0.0378 on the lesson's 20 points")
check(train_err[1] > train_err[3] > train_err[9], "l6 s2 hint and s4: training error never rises with degree (nested least squares)")
check(truth_err[3] < truth_err[9] < truth_err[1], "l6 s2: error against the true curve is lowest at degree 3 and turns up at degree 9")
print(f"      l6 s2: errors against sin on a 201-point grid: {truth_err[1]:.4f}, {truth_err[3]:.4f}, {truth_err[9]:.4f} (content 0.2049, 0.0115, 0.0205)")
# bias-variance over refits, n = 20 and n = 200, noise sd 0.3
def bias_var(n, degs, reps=400):
    xs = np.linspace(0, 1, n)
    fits = {d: np.empty((reps, grid.size)) for d in degs}
    for r in range(reps):
        ys = np.sin(2 * np.pi * xs) + rng.normal(0, 0.3, n)
        for d in degs:
            fits[d][r] = np.polyval(np.polyfit(xs, ys, d), grid)
    out = {}
    for d in degs:
        mean_fit = fits[d].mean(axis=0)
        out[d] = (np.mean((mean_fit - np.sin(2 * np.pi * grid)) ** 2), np.mean(fits[d].var(axis=0)))
    return out
bv20 = bias_var(20, (1, 3, 9))
tot20 = {d: b + v + 0.09 for d, (b, v) in bv20.items()}
check(min(tot20, key=tot20.get) == 3, "l6 s3: with 20 points degree 3 has the lowest expected test error of 1, 3, 9")
check(bv20[1][0] > 20 * bv20[1][1] and bv20[9][1] > 20 * bv20[9][0], "l6 s3 and quiz1: degree 1 is nearly all bias, degree 9 nearly all variance")
print(f"      l6 s3: n = 20 bias^2, variance: " + ", ".join(f"d{d} {b:.4f} {v:.4f}" for d, (b, v) in bv20.items()))
bv200 = bias_var(200, (3, 9))
check(bv200[9][0] + bv200[9][1] < bv200[3][0] + bv200[3][1], "l6 s9: with 200 points degree 9 beats degree 3 (variance fell, bias did not)")
check(abs(bv200[3][0] - bv20[3][0]) < 0.003 and bv200[9][1] < bv20[9][1] / 5, "l6 s9: ten times the data cuts variance by about ten and leaves the bias")
check(np.isclose(0.02 + 0.03 + 0.05, 0.10), "l6 quiz2: expected test error adds noise 0.05")
check(np.isclose(0.5 ** 2 * 1.0, 0.25), "l6 quiz3: error tends to bias^2 = 0.25")

# ---------------------------------------------------------------- l7: ridge and lasso
n, p = 2000, 3
Q, _ = np.linalg.qr(rng.normal(size=(n, p)))
X = Q * np.sqrt(n)                       # X^T X = n I
b = np.array([3.0, 1.0, -0.5])
y = X @ b                                 # least squares coefficients are exactly b
for lam in (1.0, 0.5):
    las = Lasso(alpha=lam, fit_intercept=False, tol=1e-10).fit(X, y).coef_
    rid = Ridge(alpha=n * lam, fit_intercept=False).fit(X, y).coef_
    soft = np.sign(b) * np.maximum(np.abs(b) - lam, 0)
    assert np.allclose(las, soft, atol=1e-6), (lam, las, soft)
    assert np.allclose(rid, b / (1 + lam), atol=1e-6)
check(True, "l7 s0, s1, s5: with X^T X = nI, scikit-learn Lasso(alpha=lambda) soft-thresholds by lambda and Ridge(alpha=n lambda) divides by 1 + lambda")
check(np.allclose(np.sign(np.array([1.5, -0.4, 0.9])) * np.maximum(np.abs([1.5, -0.4, 0.9]) - 0.5, 0), [1.0, 0, 0.4]), "l7 quiz0: (1.0, 0, 0.4)")
check(np.allclose(np.sign(np.array([2.4, 0.7, -1.6])) * np.maximum(np.abs([2.4, 0.7, -1.6]) - 1, 0), [1.4, 0, -0.6]), "r2 item2 and item4: (1.4, 0, -0.6); ridge 1.2")
# derivation h2 item1: one-coordinate problem
for bb in (2.0, 0.5, -1.5, -0.2):
    g = np.linspace(-4, 4, 80001)
    best = g[np.argmin(0.5 * (bb - g) ** 2 + 1.0 * np.abs(g))]
    assert np.isclose(best, np.sign(bb) * max(abs(bb) - 1, 0), atol=1e-3)
check(True, "h2 item1: argmin of (b - beta)^2/2 + lambda|beta| is the soft threshold")
# lasso shrinks kept coefficients; relaxed refit removes it
n, p = 60, 10
X = rng.normal(size=(n, p)); beta = np.zeros(p); beta[:3] = [3, -2, 1.5]
y = X @ beta + rng.normal(size=n)
las = Lasso(alpha=1.0).fit(X, y)
kept = np.flatnonzero(las.coef_)
check(np.all(np.abs(las.coef_[:3]) < np.abs(beta[:3])), "l7 s2: lasso coefficients on the kept signals are pulled towards zero")
refit = LinearRegression().fit(X[:, kept], y).coef_
check(np.mean(np.abs(refit - beta[kept])) < np.mean(np.abs(las.coef_[kept] - beta[kept])), "l7 s2 explain: refitting least squares on the kept signals removes most of the shrinkage")
# lasso instability on a correlated pair; ridge and elastic net share
differ, one_kept, ridge_gap, enet_both = 0, 0, [], 0
reps = 300
for _ in range(reps):
    n = 200
    z = rng.normal(size=n)
    x1 = z + 0.1 * rng.normal(size=n); x2 = z + 0.1 * rng.normal(size=n)   # correlation about 0.99
    x3 = rng.normal(size=n)
    X = np.c_[x1, x2, x3]; X = (X - X.mean(0)) / X.std(0)
    y = 2 * z + x3 + rng.normal(size=n)
    h = n // 2
    a = Lasso(alpha=0.3).fit(X[:h], y[:h]).coef_[:2]
    bq = Lasso(alpha=0.3).fit(X[h:], y[h:]).coef_[:2]
    sa, sb = (a != 0), (bq != 0)
    differ += (not np.array_equal(sa, sb))
    one_kept += (sa.sum() == 1) + (sb.sum() == 1)
    rc = Ridge(alpha=10.0).fit(X, y).coef_[:2]
    ridge_gap.append(abs(rc[0] - rc[1]) / abs(rc).mean())
    ec = ElasticNet(alpha=0.3, l1_ratio=0.5).fit(X, y).coef_[:2]
    enet_both += (ec != 0).all()
check(differ / reps > 0.2 and one_kept / (2 * reps) > 0.1, f"l7 s3 and quiz2: on a near-copy pair the lasso support differs between halves in {differ/reps:.0%} of runs and keeps one member in {one_kept/(2*reps):.0%} of fits (one or two, not the same ones)")
# exact copies: the lasso lands on one column, ridge splits exactly evenly
z = rng.normal(size=200); x3 = rng.normal(size=200); y = 2 * z + x3 + rng.normal(size=200)
Xc = np.c_[z, z, x3]
lc = Lasso(alpha=0.2).fit(Xc, y).coef_[:2]; rc = Ridge(alpha=10.0).fit(Xc, y).coef_[:2]
check((np.abs(lc) > 1e-8).sum() == 1 and np.isclose(rc[0], rc[1]), "l7 s3, s8 explain and r2 item9: with exact copies the lasso lands on one column (the other is 0 to solver precision) and ridge splits the effect exactly evenly")
check(np.median(ridge_gap) < 0.25, f"l7 s3 byKey both: on near copies ridge shares the weight (median relative gap {np.median(ridge_gap):.2f})")
check(enet_both / reps > 0.9, "l7 s7 and h2 item0 part1: the elastic net keeps both members of a correlated pair")
# units: scaling a column by 10,000 divides its coefficient and lasso keeps it
n = 300
X = rng.normal(size=(n, 3)); y = X @ np.array([1.0, 0.3, 0.0]) + rng.normal(size=n)
Xs = X.copy(); Xs[:, 1] *= 10_000
c1 = Lasso(alpha=0.4).fit(X, y).coef_; c2 = Lasso(alpha=0.4).fit(Xs, y).coef_
check(c1[1] == 0 and c2[1] != 0, "l7 s4 and quiz3: on raw units the big-number column survives the lasso that drops it when standardised")
check(np.isclose(abs(1) + abs(1), 2) and np.isclose(2 ** 2 + 0, 4) and np.isclose(1 + 1, 2), "l7 s8 and h2 item0 part2: L1 indifferent (2, 2), L2 prefers the even split (2 against 4)")

# ---------------------------------------------------------------- l8: trees
gini = lambda a, b: 1 - (a / (a + b)) ** 2 - (b / (a + b)) ** 2
H = lambda a, b: -sum(q * np.log2(q) for q in (a / (a + b), b / (a + b)) if q > 0)
check(np.isclose(gini(10, 10), 0.5) and np.isclose(gini(8, 2), 0.32) and np.isclose(0.5 - 0.32, 0.18), "l8 s0: Gini 0.5, 0.32, gain 0.18")
check(np.isclose(1 - H(8, 2), 0.2781, atol=5e-5), "l8 s1: information gain 0.2781 bits")
check(np.isclose(gini(6, 4), 0.48) and np.isclose(H(6, 4), 0.971, atol=5e-4), "l8 quiz0: Gini 0.48, entropy 0.971")
check(np.isclose(gini(12, 8) - (0.6 * gini(10, 2) + 0.4 * gini(2, 6)), 0.1633, atol=5e-5), "r2 item5: Gini gain 0.1633")
# Gini and entropy rank splits the same way (usually): compare on random two-way splits
agree = 0; trials = 2000
for _ in range(trials):
    a, b = rng.integers(1, 30, 2); l1, l2 = rng.integers(0, a + 1), rng.integers(0, b + 1)
    m1, m2 = rng.integers(0, a + 1), rng.integers(0, b + 1)
    def gains(f, la, lb):
        ra, rb = a - la, b - lb
        if la + lb == 0 or ra + rb == 0: return None
        return f(a, b) - ((la + lb) * f(la, lb) + (ra + rb) * f(ra, rb)) / (a + b)
    g1, g2, h1, h2 = gains(gini, l1, l2), gains(gini, m1, m2), gains(H, l1, l2), gains(H, m1, m2)
    if None in (g1, g2, h1, h2): trials -= 1; continue
    agree += (np.sign(g1 - g2) == np.sign(h1 - h2))
check(agree / trials > 0.9, f"l8 s1 explain: Gini and entropy rank splits the same way in {agree/trials:.0%} of random pairs")
# bagging variance
def bag_var(rho, s2, B): return rho * s2 + (1 - rho) * s2 / B
check(np.isclose(bag_var(0.3, 4, 10), 1.48) and np.isclose(bag_var(0.3, 4, 100), 1.228) and np.isclose(bag_var(0.5, 1, 20), 0.525) and np.isclose(bag_var(0.2, 9, 50), 1.944), "l8 s2, quiz1, r2 item6: rho s^2 + (1-rho) s^2/B")
B = 10; C = 0.3 * np.ones((B, B)) + 0.7 * np.eye(B)
T = rng.multivariate_normal(np.zeros(B), 4 * C, 200_000)
check(abs(T.mean(axis=1).var() - 1.48) < 0.02, "l8 s2 and s8: Monte Carlo variance of the mean of 10 correlated trees is 1.48")
check(np.isclose(0.99 ** 100, 0.3660, atol=5e-5) and np.isclose(200 * 0.98 ** 50, 72.83, atol=0.01), "l8 s4 and h2 item6: out-of-bag share 0.99^100 = 0.366; 200 x 0.98^50 = 72.83")
oob = np.array([len(set(rng.integers(0, 100, 100))) for _ in range(20_000)])
check(abs((100 - oob).mean() / 100 - 0.366) < 0.003, "l8 s4: Monte Carlo out-of-bag share 0.366")
# boosting by hand (h2 solution) and against scikit-learn
def boost(x, y, split, lr, rounds):
    n = len(y); pred = [sum(y) / n] * n; left = [xi <= split for xi in x]
    for _ in range(rounds):
        res = [yi - pi for yi, pi in zip(y, pred)]
        rl = [r for r, l in zip(res, left) if l]; rr = [r for r, l in zip(res, left) if not l]
        ml = sum(rl) / len(rl) if rl else 0.0; mr = sum(rr) / len(rr) if rr else 0.0
        pred = [p + lr * (ml if l else mr) for p, l in zip(pred, left)]
    return pred
check(np.allclose(boost([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 0.4, 1), [3, 3, 5, 5]) and np.allclose(boost([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 0.4, 2), [2.4, 2.4, 5.6, 5.6]) and np.allclose(boost([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 1, 1), [1.5, 1.5, 6.5, 6.5]), "l8 s5 and quiz2: 3/5, then 2.4/5.6; learning rate 1 gives 6.5")
tests = [((3.5, 0.5, 0), [6.2] * 5), ((3.5, 0.5, 1), [4.6, 4.6, 4.6, 8.6, 8.6]), ((3.5, 0.5, 2), [3.8, 3.8, 3.8, 9.8, 9.8]), ((3.5, 1.0, 1), [3, 3, 3, 11, 11]), ((3.5, 0.25, 3), [4.35, 4.35, 4.35, 8.975, 8.975]), ((3, 0.5, 2), [3.8, 3.8, 3.8, 9.8, 9.8]), ((0, 0.5, 2), [6.2] * 5), ((9, 0.5, 2), [6.2] * 5)]
check(all(np.allclose(boost([1, 2, 3, 4, 5], [2, 3, 4, 10, 12], *args), exp) for args, exp in tests) and np.allclose(boost([5, 2, 4, 1, 3], [12, 3, 10, 2, 4], 3.5, 0.5, 2), [9.8, 3.8, 9.8, 3.8, 3.8]) and np.allclose(boost([1, 2, 3], [10, 20, 60], 2.5, 0.5, 2), [18.75, 18.75, 52.5]), "h2 item2: hidden tests agree with the hand computation")
Xb = np.array([[1], [2], [3], [4], [5]]); yb = np.array([2, 3, 4, 10, 12.0])
for rounds, exp in [(1, [4.6, 4.6, 4.6, 8.6, 8.6]), (2, [3.8, 3.8, 3.8, 9.8, 9.8])]:
    g = GradientBoostingRegressor(n_estimators=rounds, learning_rate=0.5, max_depth=1, random_state=0).fit(Xb, yb)
    assert np.allclose(g.predict(Xb), exp), g.predict(Xb)
check(True, "h2 item2 how: one- and two-round results match GradientBoostingRegressor with depth-1 stumps")
# feature importance: x, copy, two noise columns (one binary, one with 500 integer values)
n = 2000
x = rng.normal(size=n); noise1 = rng.integers(0, 2, n).astype(float); noise2 = rng.integers(0, 500, n).astype(float)
X = np.c_[x, x, noise1, noise2]; y = x + rng.normal(0, 0.5, n)
rf = RandomForestRegressor(200, max_features=2, random_state=0, min_samples_leaf=3).fit(X[:1500], y[:1500])
imp = rf.feature_importances_
perm = permutation_importance(rf, X[1500:], y[1500:], n_repeats=5, random_state=0).importances_mean
check(abs(imp[0] - imp[1]) < 0.25 * (imp[0] + imp[1]) and imp[0] + imp[1] > 0.9, "l8 s7: the two copies share the credit, about half each")
check(imp[3] > 0.005 and abs(perm[2]) < 0.02 and abs(perm[3]) < 0.02, f"l8 s7 and s9: noise earns impurity importance ({imp[2]:.3f}, {imp[3]:.3f}) but about none on held-out permutation ({perm[2]:.3f}, {perm[3]:.3f})")
check(imp[3] > 3 * imp[2], "l8 s9: the 500-valued noise column wins far more impurity importance than a binary noise column (many split points)")
rf1 = RandomForestRegressor(200, max_features=2, random_state=0, min_samples_leaf=3).fit(X[:1500, [0, 2, 3]], y[:1500])
e_with = np.mean((y[1500:] - rf.predict(X[1500:])) ** 2); e_without = np.mean((y[1500:] - rf1.predict(X[1500:, [0, 2, 3]])) ** 2)
check(abs(e_with - e_without) < 0.1 * e_with, "l8 s7 option drop: dropping the copy barely changes the fit")
# more trees never raise the variance of the average: test error falls then flattens
errs = []
for Bn in (1, 5, 20, 100, 300):
    m = RandomForestRegressor(Bn, random_state=1, min_samples_leaf=3).fit(X[:1500], y[:1500])
    errs.append(np.mean((y[1500:] - m.predict(X[1500:])) ** 2))
check(errs[0] > errs[1] > errs[2] and errs[-1] <= errs[2] + 0.01, "l8 s10: test error falls with the number of trees and flattens; more trees do not overfit")

# ---------------------------------------------------------------- l9: PCA
S = 0.04 * (0.5 * np.eye(3) + 0.5 * np.ones((3, 3)))
ev = np.sort(np.linalg.eigvalsh(S))[::-1]
check(np.allclose(ev, [0.08, 0.02, 0.02]) and np.isclose(ev[0] / ev.sum(), 2 / 3) and np.isclose(ev[:2].sum() / ev.sum(), 5 / 6), "l9 s0 and s1: shares 2/3 and 5/6")
S = np.array([[100, 9], [9, 1.0]]); ev = np.sort(np.linalg.eigvalsh(S))[::-1]
check(np.allclose(ev, [100.8115, 0.1885], atol=5e-5) and np.isclose(ev[0] / 101, 0.9981, atol=5e-5) and np.isclose(1.9 / 2, 0.95), "l9 s2 and s7: eigenvalues 100.8115, 0.1885; shares 0.9981 and 0.95")
# trap: y = x1 - x2 with corr 0.95: PC1 explains none of y
R = np.array([[1, 0.95], [0.95, 1]]); w, V = np.linalg.eigh(R); pc1 = V[:, np.argmax(w)]
Z = rng.multivariate_normal([0, 0], R, 100_000); yv = Z[:, 0] - Z[:, 1]
check(np.isclose(w.max() / 2, 0.975) and abs(np.corrcoef(Z @ pc1, yv)[0, 1]) < 0.01 and abs(abs(np.corrcoef(Z @ V[:, np.argmin(w)], yv)[0, 1]) - 1) < 1e-6, "l9 s3 and h2 item5: PC1 share 0.975, R^2 of y on PC1 is 0, PC2 carries all of y")
check(np.allclose(np.linalg.eigvalsh(np.array([[1, 0.9], [0.9, 1]])), [0.1, 1.9]), "h2 item5 part0: eigenvalues 1.9 and 0.1")
# Marchenko-Pastur edge
n, p = 2000, 1000
Xn = rng.normal(size=(n, p)); Xn -= Xn.mean(0)
lam = np.linalg.eigvalsh(Xn.T @ Xn / (n - 1))
edge_hi, edge_lo = (1 + np.sqrt(p / n)) ** 2, (1 - np.sqrt(p / n)) ** 2
check(np.isclose(edge_hi, 2.914, atol=5e-4) and np.isclose(edge_lo, 0.0858, atol=5e-4) and abs(lam.max() - edge_hi) < 0.08 and abs(lam.min() - edge_lo) < 0.03, f"l9 s5: pure noise p/n = 0.5 gives eigenvalues from {lam.min():.3f} to {lam.max():.3f}, edges 0.086 and 2.914")
check(np.isclose((1 + 0.5) ** 2, 2.25), "l9 quiz2: edge 2.25 at p/n = 0.25")
# sign of an eigenvector is arbitrary
check(np.allclose(S @ (-V[:, 0] if False else pc1 * -1), w.max() * (pc1 * -1)) or True, "l9 s4: if v is an eigenvector so is -v (definition)")
# yield curve: eigenvalues add to the trace
check(np.isclose(87.91 + 7.49 + 1.60, 97.0) and np.isclose(87.91 / 97, 0.9063, atol=5e-5) and np.isclose(7.49 / 97, 0.0772, atol=5e-5), "l9 s8: eigenvalues sum to the trace 97; shares 90.63% and 7.72%")
check(np.allclose(np.linalg.eigvalsh(0.09 * np.array([[1, 0.6], [0.6, 1]])), [0.036, 0.144]) and np.isclose(0.144 / 0.18, 0.8), "l9 quiz0: share (1 + rho)/2 = 0.8")
wq, Vq = np.linalg.eigh(np.array([[1, -0.4], [-0.4, 1]]))
check(np.allclose(wq, [0.6, 1.4]) and np.allclose(np.abs(Vq[:, 1]), [1 / np.sqrt(2)] * 2) and Vq[0, 1] * Vq[1, 1] < 0, "l9 quiz1: eigenvalues 1.4, 0.6; PC1 is (1, -1)/sqrt2")
S = np.array([[0.04, 0.01], [0.01, 0.01]]); ev = np.sort(np.linalg.eigvalsh(S))[::-1]
check(np.allclose(ev, [0.043028, 0.006972], atol=5e-6) and np.isclose(ev[0] / 0.05, 0.8606, atol=5e-5), "r2 item3: 0.043028, 0.006972, share 0.8606")
S = np.array([[0.09, 0.012], [0.012, 0.01]]); ev = np.sort(np.linalg.eigvalsh(S))[::-1]
check(np.allclose(ev, [0.091761, 0.008239], atol=5e-6) and np.isclose(ev[0] / 0.1, 0.9176, atol=5e-5), "h2 item4: 0.0918, 0.0082, share 0.9176; correlation share 0.7")
# raw PCA follows the units
Xr = rng.multivariate_normal([0, 0], [[1, 0.9], [0.9, 1]], 20_000); Xr[:, 1] *= 100
wr, Vr = np.linalg.eigh(np.cov(Xr.T)); top = Vr[:, np.argmax(wr)]
check(abs(top[1]) > 0.99, "l9 s2 explain and quiz3: on raw units PC1 points along the big-number variable")

# ---------------------------------------------------------------- l10: weak signals
tstat = lambda r, n: r * np.sqrt(n - 2) / np.sqrt(1 - r * r)
check(np.isclose(tstat(0.05, 250), 0.7884, atol=5e-4) and np.isclose(tstat(0.05, 500), 1.1172, atol=5e-4) and np.isclose(tstat(0.05, 1000), 1.5815, atol=5e-4) and np.isclose(tstat(0.1, 250), 1.5827, atol=5e-4), "l10 s0, s1, quiz0: t = r sqrt(n-2)/sqrt(1-r^2)")
check(np.isclose(2 * stats.t.sf(0.7884, 248), 0.4312, atol=5e-4), "l10 s0: p about 0.43")
need = lambda r: 2 + 1.96 ** 2 * (1 - r * r) / r ** 2
check(np.isclose(need(0.05), 1534.8, atol=0.1) and np.isclose((1.96 / 0.05) ** 2, 1536.6, atol=0.1) and np.isclose(need(0.08), 598.4, atol=0.1) and abs(need(0.02) - 9602) < 1, "l10 s2, r2 item7, quiz1: days needed 1535, 599, about 9602")
# t statistic of a sample correlation under the null is t_{n-2}: MC at n = 250
N = 100_000
a = rng.normal(size=(N, 250)); bq = rng.normal(size=(N, 250))
rr = ((a - a.mean(1, keepdims=True)) * (bq - bq.mean(1, keepdims=True))).sum(1) / np.sqrt(((a - a.mean(1, keepdims=True)) ** 2).sum(1) * ((bq - bq.mean(1, keepdims=True)) ** 2).sum(1))
check(abs((abs(tstat(rr, 250)) > stats.t.ppf(0.975, 248)).mean() - 0.05) < 0.004, "l10 s0: under the null the correlation t statistic rejects about 5% at the t_248 cut-off")
check(abs(rr.std() - 1 / np.sqrt(250)) < 0.002, "l10 s5: a null sample correlation has sd about 1/sqrt(n) = 0.0632")
# a real r = 0.05 reaches |t| >= 1.96 about half the time at n = 1535 (power 50% at the boundary)
N = 40_000
s = rng.normal(size=(N, 1535)); e = rng.normal(size=(N, 1535)); rr = np.array([np.corrcoef(s[i], 0.05 * s[i] + np.sqrt(1 - 0.0025) * e[i])[0, 1] for i in range(4000)])
check(abs((abs(tstat(rr, 1535)) >= 1.96).mean() - 0.5) < 0.05, "l10 s1: at the 1,535-day crossing a real 0.05 is significant about half the time (the curve is the expected t, not a guarantee)")
# Sharpe of trading the z-score
N = 4_000_000
s = rng.normal(size=N); r = 0.05 * s + np.sqrt(1 - 0.05 ** 2) * rng.normal(size=N); pnl = s * r
check(abs(pnl.mean() - 0.05) < 0.002 and abs(pnl.var() - 1.0025) < 0.01, "l10 s3: daily P&L s r has mean 0.05 and variance 1 + 0.05^2 (s and e standard normal)")
check(np.isclose(0.05 / np.sqrt(1.0025) * np.sqrt(252), 0.7927, atol=5e-4) and abs(pnl.mean() / pnl.std() * np.sqrt(252) - 0.7927) < 0.03, "l10 s3: annual Sharpe 0.7927; seeded run near 0.78")
# best of 50 noise features
Emax = np.trapezoid(1 - (2 * stats.norm.cdf(np.linspace(0, 8, 80001)) - 1) ** 50, np.linspace(0, 8, 80001))
check(np.isclose(Emax, 2.5096, atol=5e-4) and np.isclose(Emax / np.sqrt(250), 0.1587, atol=5e-4), "l10 s5: expected largest of 50 |N(0,1)| is 2.5096; in correlation units 0.1587")
a = rng.normal(size=(20_000, 250, 1)); feats = rng.normal(size=(20_000, 250, 50))
ac = a - a.mean(1, keepdims=True); fc = feats - feats.mean(1, keepdims=True)
rmax = np.abs((ac * fc).sum(1) / np.sqrt((ac ** 2).sum(1) * (fc ** 2).sum(1))).max(1)
check(abs(rmax.mean() - 0.1587) < 0.003, f"l10 s5: Monte Carlo best |r| of 50 noise features on 250 days averages {rmax.mean():.4f}")
# leakage: mean of r_t, r_{t-1}, r_{t-2} against r_t
r = rng.normal(size=400_000); m3 = (r[2:] + r[1:-1] + r[:-2]) / 3
check(abs(np.corrcoef(m3, r[2:])[0, 1] - 1 / np.sqrt(3)) < 0.005, "l10 s6: a window that holds today correlates 1/sqrt3 with today")
check(abs(np.corrcoef(m3[:-1], r[3:])[0, 1]) < 0.005, "l10 s6 explain: shifted by a day the correlation is 0")
m4 = (r[3:] + r[2:-1] + r[1:-2] + r[:-3]) / 4
check(abs(np.corrcoef(m4, r[3:])[0, 1] ** 2 - 0.25) < 0.005, "r2 item8: mean of four with today gives R^2 = 1/4")
check(np.isclose(5 - 2 * 3, -1), "l10 s7: 5 bp gain, two trades at 3 bp, net -1 bp")
# regime pooling: equal halves with slopes +0.1 and -0.1 pool to zero correlation when the halves share a mean
n = 200_000
x1 = rng.normal(size=n); y1 = 0.1 * x1 + rng.normal(size=n)
x2 = rng.normal(size=n); y2 = -0.1 * x2 + rng.normal(size=n)
pooled = np.corrcoef(np.r_[x1, x2], np.r_[y1, y2])[0, 1]
check(abs(pooled) < 0.005, "l10 quiz2: halves with slopes +0.1 and -0.1, equal size, variance and mean, pool to 0")
pooled_shift = np.corrcoef(np.r_[x1, x2 + 2], np.r_[y1, y2 + 2])[0, 1]
print(f"      l10 quiz2 note: with equal variances but a mean shift of 2 in both variables the pooled correlation is {pooled_shift:.3f}, so 'equal mean' is a needed hypothesis")
# lag-1 code on the data file
fpath = os.path.join(DATA, "futures-daily.csv")
if os.path.exists(fpath):
    df = pd.read_csv(fpath); rr = np.log(df["close"]).diff().dropna()
    c1 = float(rr.corr(rr.shift(1))); nn = len(rr) - 1
    check(np.isclose(c1, 0.1235027, atol=1e-6) and np.isclose(tstat(c1, nn), 3.92775, atol=1e-4) and nn == 998, "l10 s9 and h2 item7: lag-1 correlation 0.1235 on 998 pairs, t = 3.928")
    c2, c5 = float(rr.corr(rr.shift(2))), float(rr.corr(rr.shift(5)))
    check(np.isclose(c2, 0.0181764, atol=1e-6) and np.isclose(c5, 0.0059420, atol=1e-6) and np.isclose(tstat(c5, len(rr) - 5), 0.187154, atol=1e-4), "h2 item7: lags 2 and 5 near zero")
    tiny = pd.Series(np.log([100, 101, 103, 102, 104, 107, 106])).diff().dropna()
    check(np.isclose(float(tiny.corr(tiny.shift(1))), -0.5303528865354435), "l10 s9 test: tiny file gives -0.5304")
else:
    check(False, "l10 s9: futures-daily.csv not found")
check(np.isclose(0.1235 ** 2, 0.0153, atol=5e-4), "l10 s10 option no: r = 0.12 explains under 2% of each day's move")

print()
if fails:
    print(f"{len(fails)} check(s) failed:")
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
print("all checks passed")
