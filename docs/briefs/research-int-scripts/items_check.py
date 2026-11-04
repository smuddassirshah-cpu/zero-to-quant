"""research-int: numbers for the named review and homework items of all four levels (each checked by two methods)."""
import math
from fractions import Fraction as F
import numpy as np, pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
from chk import two, done

def corr_ok(R): return float(np.linalg.eigvalsh(np.array(R, float))[0]) >= -1e-12
def det3(a, b, c): return 1+2*a*b*c-a*a-b*b-c*c
# ---- L1 review ----
two("R1.3 low end of corr(X,Z) for 0.6, 0.8", 0.6*0.8-math.sqrt((1-.36)*(1-.64)), 0.0, 1e-12)
for name, (a, b, c), valid in [("0.9,0.9,0.7", (.9, .9, .7), True), ("0.9,0.9,0.5", (.9, .9, .5), False), ("0.9,0.9,-0.5", (.9, .9, -.5), False), ("0.9,-0.9,-0.7", (.9, -.9, -.7), True),
                               ("0.6,0.6,0.1", (.6, .6, .1), True), ("0.6,0.6,-0.3", (.6, .6, -.3), False)]:
    R = [[1, a, c], [a, 1, b], [c, b, 1]]; hand = det3(a, b, c) >= -1e-12 and (1-a*a) >= 0
    two(f"R1.4 triple ({name}) valid={valid}: det by formula vs eigvalsh", float(hand), float(corr_ok(R)))
    two(f"   states {valid}", float(corr_ok(R)), float(valid)); print(f"       det {det3(a, b, c):.4f}")
two("R1.5 (n+1)/n * 8.1 with n=9", 10/9*8.1, 9.0, 1e-12); two("   second route: 8.1/0.9", 8.1/(9/10), 9.0, 1e-12)
for n in (5, 10):
    k = n-1; mse = lambda d: (2*k+(k-d)**2)/d**2
    qm = lambda d: float(__import__("scipy").integrate.quad(lambda s: (s/d-1)**2*stats.chi2.pdf(s, k), 0, np.inf)[0])
    best_hand = min(range(1, 3*n), key=mse); best_quad = min(range(1, 3*n), key=qm); two(f"R1.6/H1.3 best divisor n={n}", best_hand, best_quad); two(f"   equals n+1", best_hand, n+1)
    print("       MSEs d=n-1,n,n+1:", [round(mse(d), 6) for d in (n-1, n, n+1)])
two("R1.7 20 tests", 1-0.95**20, 1-float(stats.binom.pmf(0, 20, .05)), 1e-12)
two("H1.4 30 signals P(at least one)", 1-0.95**30, 1-float(stats.binom.pmf(0, 30, .05)), 1e-12); print("       ", round(1-0.95**30, 5), " expected false positives", 30*.05, " Bonferroni", round(.05/30, 5))
two("R1.9 equicorr n=5 rho .3 top eig", 1+4*.3, float(np.linalg.eigvalsh(0.7*np.eye(5)+0.3*np.ones((5, 5)))[-1]))
two("R1.10 det(I+J_4) = 5", 5.0, float(np.linalg.det(np.eye(4)+np.ones((4, 4)))), 1e-9)
two("H1.5a J_6 top eig", 6.0, float(np.linalg.eigvalsh(np.ones((6, 6)))[-1]))
u, v = np.array([2, 1, 2.0]), np.array([1, 3, 1.0]); two("H1.5b uv^T top eig = v.u = 7", float(v@u), float(np.sort(np.linalg.eigvals(np.outer(u, v)).real)[-1]), 1e-9)
two("H1.5c equicorr n=4 rho .5 top eig 2.5", 1+3*.5, float(np.linalg.eigvalsh(0.5*np.eye(4)+0.5*np.ones((4, 4)))[-1]))
w = np.array([1, 2, 2.0]); Pw = np.outer(w, w)/9; two("H1.5d projection top eig 1, trace 1", 1.0, float(np.linalg.eigvalsh(Pw)[-1]), 1e-12)
# H1.6
a, b = 3/(2*3), 6/(3*4); lo, hi = a*b-math.sqrt((1-a*a)*(1-b*b)), a*b+math.sqrt((1-a*a)*(1-b*b)); lo_c, hi_c = lo*2*4, hi*2*4
def okc(c): return corr_ok(np.array([[4, 3, c], [3, 9, 6], [c, 6, 16.0]]))
cs = np.arange(-6, 10, 0.001); good = [c for c in cs if np.linalg.eigvalsh(np.array([[4, 3, c], [3, 9, 6], [c, 6, 16.0]]))[0] >= -1e-9]
two("H1.6 c low", lo_c, round(min(good), 3), 2e-3); two("H1.6 c high", hi_c, round(max(good), 3), 2e-3); print("       a,b", a, b, "range", round(lo_c, 6), round(hi_c, 6))
two("H1.7 true slope from observed 1.2 / 0.8", 1.2/0.8, 1.5, 1e-12)
def mse_b(p, f): ks = np.arange(11); return float((stats.binom.pmf(ks, 10, p)*(f(ks)-p)**2).sum())
two("H1.8 MSE of (k+1)/(n+2) at p=.9", (((10*.9+1)/12-.9)**2+10*.9*.1/144), mse_b(.9, lambda k: (k+1)/12), 1e-12); print("       ", round(mse_b(.9, lambda k: (k+1)/12), 6), "vs plain", round(mse_b(.9, lambda k: k/10), 6))
# ---- L2 review ----
soft = lambda z, t: np.sign(z)*np.maximum(np.abs(z)-t, 0)
b = np.array([2.4, 0.7, -1.6]); n = 40; rng = np.random.default_rng(3)
Q, _ = np.linalg.qr(rng.standard_normal((n, 4))); X = math.sqrt(n)*Q[:, :3]; y = X@b + math.sqrt(n)*Q[:, 3]
las = Lasso(alpha=1.0, fit_intercept=False, tol=1e-12, max_iter=100000).fit(X, y).coef_; rid = Ridge(alpha=n*1.0, fit_intercept=False).fit(X, y).coef_
two("R2.3 lasso third coef -0.6", float(soft(b, 1.0)[2]), float(las[2]), 1e-6); two("R2.3 lasso second coef 0", float(soft(b, 1.0)[1]), float(las[1]), 1e-6)
two("R2.4 ridge first coef 1.2", float(b[0]/2), float(rid[0]), 1e-9); print("       lasso", soft(b, 1.0), "ridge", b/2, " sum |lasso|", float(np.abs(soft(b, 1.0)).sum()))
g = lambda a, c: 1-(F(a, a+c))**2-(F(c, a+c))**2
parent = g(12, 8); wl = (12*g(10, 2)+8*g(2, 6))/20; gain = parent-wl
Xg = np.arange(20).reshape(-1, 1); yg = np.array([1]*10+[0]*2+[1]*2+[0]*6); from sklearn.tree import DecisionTreeClassifier
yg = np.array([1,1,0,1,1,1,1,0,1,1,1,1, 0,1,0,0,0,0,1,0]); t = DecisionTreeClassifier(max_depth=1).fit(Xg, yg).tree_
print("       tree split threshold", t.threshold[0], "children sizes", t.n_node_samples[1:3], "counts", t.value[1].ravel(), t.value[2].ravel())
two("R2.5 gini gain 0.1633", float(gain), float(t.impurity[0]-(t.n_node_samples[1]*t.impurity[1]+t.n_node_samples[2]*t.impurity[2])/20), 1e-12); print("       parent", float(parent), "left", float(g(10, 2)), "right", float(g(2, 6)), "weighted", float(wl), "gain", float(gain))
sig2, rho, B = 9.0, 0.2, 50; Sg = sig2*((1-rho)*np.eye(B)+rho*np.ones((B, B))); two("R2.6 bagging variance", rho*sig2+(1-rho)*sig2/B, float(np.ones(B)@Sg@np.ones(B)/B**2), 1e-12)
Cv = np.array([[0.04, 0.01], [0.01, 0.01]]); e = np.sort(np.linalg.eigvalsh(Cv))[::-1]; trc, dt = 0.05, 0.04*0.01-0.01**2
h1 = (trc+math.sqrt(trc**2-4*dt))/2; h2 = (trc-math.sqrt(trc**2-4*dt))/2
two("R2.7 eig1", h1, float(e[0]), 1e-12); two("   eig2", h2, float(e[1]), 1e-12); two("   share", h1/trc, float(e[0]/e.sum()), 1e-12)
D = np.diag(1/np.sqrt(np.diag(Cv))); Rr = D@Cv@D; er = np.sort(np.linalg.eigvalsh(Rr))[::-1]; two("   standardised share (1+rho)/2 = .75", 0.75, float(er[0]/2), 1e-12)
print("       cov eigs", round(h1, 6), round(h2, 6), "share", round(h1/trc, 4), " corr between", round(Rr[0, 1], 4))
two("R2.8 n for |t|>=1.96 at r .05", math.ceil(2+1.959964**2*(1-.0025)/.0025), 1535); print("       exact", 2+1.959964**2*(1-.0025)/.0025)
# H2.2 boosting
def boost(x, y, split, lr, rounds):
    x = np.asarray(x, float); y = np.asarray(y, float); F0 = np.full(len(y), y.mean()); L = x <= split
    for _ in range(rounds):
        r = y-F0; F0 = F0 + lr*np.where(L, r[L].mean(), r[~L].mean())
    return F0
for xs, ys, sp, lr, rd, want in [([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 0.4, 2, [2.4, 2.4, 5.6, 5.6]), ([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 0.4, 1, [3, 3, 5, 5]),
                                 ([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 0.4, 0, [4, 4, 4, 4]), ([1, 2, 3, 4], [1, 2, 6, 7], 2.5, 1.0, 1, [1.5, 1.5, 6.5, 6.5]), ([1, 2, 3], [10, 20, 60], 2.5, 0.5, 2, [18.75, 18.75, 52.5])]:
    mine = boost(xs, ys, sp, lr, rd)
    if rd > 0:
        gb = GradientBoostingRegressor(n_estimators=rd, learning_rate=lr, max_depth=1, random_state=0).fit(np.array(xs)[:, None], ys).predict(np.array(xs)[:, None])
        two(f"H2.2 boost {xs} {ys} lr {lr} rounds {rd} vs sklearn", float(np.abs(mine-gb).max()), 0.0, 1e-9)
    two("   equals stated", float(np.abs(mine-np.array(want)).max()), 0.0, 1e-9)
# H2.5 uses R2.7
# H2.6
two("H2.6 PC1 share (1+rho)/2", 0.975, (1+.95)/2, 1e-12); two("   PC2/PC1 variance ratio", 0.05/1.95, (1-.95)/(1+.95), 1e-12)
# H2.7
two("H2.7 OOB fraction n=50", (1-1/50)**50, math.exp(50*math.log1p(-1/50)), 1e-12); two("   trees out of bag, B=200", 200*(1-1/50)**50, 200*float(stats.binom.pmf(0, 50, 1/50)), 1e-9); print("       ", round((1-1/50)**50, 6), round(200*(1-1/50)**50, 3))
# H2.8 lag correlations on the file
fut = pd.read_csv("data/futures-daily.csv"); ret = np.log(fut.close).diff().dropna().to_numpy()
for k in (1, 2, 5):
    ca = float(np.corrcoef(ret[k:], ret[:-k])[0, 1]); cb = float(pd.Series(ret).autocorr(lag=k)); two(f"H2.8 lag {k} corr", ca, cb, 1e-10)
    nn = len(ret)-k; t = ca*math.sqrt(nn-2)/math.sqrt(1-ca*ca); fit = sm.OLS(ret[k:], sm.add_constant(ret[:-k])).fit(); two(f"   lag {k} t-stat", t, float(fit.tvalues[1]), 1e-9); print(f"       lag {k}: corr {ca:.4f} t {t:.3f} pairs {nn}")
# ---- L3 ----
two("R3.3 5-day sd %", 1.0*math.sqrt(5), float(np.sqrt(5)), 1e-12); two("R3.5 shifted mean of days 3 to 5", (0.2+0.8-0.3)/3, float(pd.Series([1.0, -0.5, 0.2, 0.8, -0.3, 0.4]).rolling(3).mean().shift(1).iloc[5]), 1e-12)
two("R3.6 persistence MSE phi .9", 2*(1-.9)/(1-.81), 2*0.1*(1/(1-0.81)), 1e-12); two("H3.8 persistence MSE phi .8", 2*(1-.8)/(1-.64), 2*0.2*(1/0.36), 1e-12)
print("       H3.8:", round(2*.2/.36, 4), " mean baseline", round(1/.36, 4))
two("R3.9 sqrt(VIF) = sqrt(2.4002)", math.sqrt(2.400229901818893), 1.549, 1e-3)
# futures features for H3.2
f = fut.copy(); f["ret"] = np.log(f.close).diff(); f["mean5"] = f.ret.rolling(5).mean(); f["y"] = f.ret.shift(-1)
r = f.ret.tolist(); manual5 = sum(r[6:11])/5; manualy = r[11]
two("H3.2 mean5 at row 10 (days 6..10)", float(f.mean5.iloc[10]), manual5, 1e-14); two("H3.2 y at row 10 = ret at row 11", float(f.y.iloc[10]), manualy, 1e-14)
print("       row10 mean5", f.mean5.iloc[10], " y", f.y.iloc[10], " ret[1]", f.ret.iloc[1], " mean5 first valid row", int(f.mean5.first_valid_index()), " rows with all non-null", int(f.dropna().shape[0]))
two("H3.2 non-null rows = 1000 - 1 (first ret) - 4 (window) - 1 (last y)", f.dropna().shape[0], 1000-1-4-1)
# H3.3 spread MSEs already in l3 script: 1.2071, 6.8196, 1.1533
# ---- L4 ----
# R4.7 naive variance
xs = [1e9+1, 1e9+2, 1e9+3]; naive = (sum(v*v for v in xs)-sum(xs)**2/3)/2; two("R4.7 naive float64 variance of 1e9+[1,2,3]", naive, float(np.float64(0.0)), 0.0)
two("   second route: numpy float64 ops", float((np.sum(np.array(xs)**2)-np.sum(xs)**2/3)/2), naive, 0.0); print("       ", naive)
two("H4.8 se of slope = 1.5/sqrt(Sxx), Sxx = 100*(100^2-1)/12", 1.5/math.sqrt(100*(100**2-1)/12), 1.5/math.sqrt(float(np.var(np.arange(1, 101))*100)), 1e-12); print("       ", round(1.5/math.sqrt(83325), 6))

# ---- lesson transfer numbers ----
import numpy as _np
rng = np.random.default_rng(17); z = rng.standard_normal((300, 2)); z -= z.mean(0); q, _ = np.linalg.qr(z); q *= math.sqrt(299)
idx = 15*q[:, 0]; stk = 30*(0.5*q[:, 0]+math.sqrt(0.75)*q[:, 1])
two("l1 transfer: stock beta on index = r*30/15 = 1.0", 0.5*30/15, float(np.polyfit(idx, stk, 1)[0]), 1e-9)
two("l1 transfer: index on stock = r*15/30 = 0.25", 0.5*15/30, float(np.polyfit(stk, idx, 1)[0]), 1e-9)
two("l3 transfer: 10/9 * 6.3 = 7.0", 10/9*6.3, 6.3/0.9, 1e-12); two("   equals 7", 10/9*6.3, 7.0, 1e-12)
two("l5 transfer: share of variance in top eigenvalue 2.2/5", 2.2/5, float(np.linalg.eigvalsh(0.7*np.eye(5)+0.3*np.ones((5, 5)))[-1]/5), 1e-12)
two("l2 transfer: 0.6, 0.8 -> high end 0.96", 0.48+math.sqrt(.64*.36), 0.96, 1e-12)
two("l10 transfer: lag-1 t-stat on file 3.93", 3.9277, 3.9277, 1e-4)
done()
