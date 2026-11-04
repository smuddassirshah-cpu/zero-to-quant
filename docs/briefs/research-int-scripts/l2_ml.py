"""research-int level 2: l6 bias-variance, l7 ridge and lasso, l8 trees, l9 PCA, l10 weak signals."""
import math
from fractions import Fraction as F
import numpy as np
from scipy import integrate, stats
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from chk import two, done, Phi

# ---------- l6 ----------
mu, v = 1.0, 1.0   # mean 1, sigma^2/n = 1 (sigma 2, n 4)
mse = lambda c: (c-1)**2*mu**2 + c*c*v
xb = np.random.default_rng(2).normal(mu, math.sqrt(v), 2_000_000)
for c in (1.0, 0.5, 0.0):
    two(f"l6 MSE of c*xbar, c={c}", mse(c), float(((c*xb-mu)**2).mean()), 0.01)
two("l6 best c = mu^2/(mu^2+v)", mu**2/(mu**2+v), float(minimize_c := min(np.linspace(0, 1, 10001), key=mse)), 1e-4)
two("l6 MSE at best c", mse(0.5), 0.5)
# polynomial experiment
def f(x): return np.sin(2*np.pi*x)
rng = np.random.default_rng(11); n = 20
xtr = np.linspace(0, 1, n); ytr = f(xtr) + rng.normal(0, 0.3, n)
xte = np.linspace(0, 1, 2000); yte_clean = f(xte)
print("     train x:", [round(a, 3) for a in xtr]); print("     train y:", [round(a, 3) for a in ytr])
for d in (1, 3, 9):
    c = np.polyfit(xtr, ytr, d); tr_a = float(((np.polyval(c, xtr)-ytr)**2).mean()); te_a = float(((np.polyval(c, xte)-yte_clean)**2).mean())
    m = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(xtr[:, None], ytr)
    tr_b = float(((m.predict(xtr[:, None])-ytr)**2).mean()); te_b = float(((m.predict(xte[:, None])-yte_clean)**2).mean())
    two(f"l6 deg {d} train MSE", tr_a, tr_b, 1e-6); two(f"l6 deg {d} test MSE vs truth (noise-free)", te_a, te_b, 1e-5)
    print(f"     degree {d}: train {tr_a:.4f}  test(noise-free) {te_a:.4f}  test incl noise var 0.09: {te_a+0.09:.4f}")
# bias-variance decomposition over 400 refits, degree d, expected over the grid
def decomp(d, reps=400):
    r = np.random.default_rng(100+d); preds = []
    for _ in range(reps):
        xs = np.linspace(0, 1, n); ys = f(xs)+r.normal(0, 0.3, n); preds.append(np.polyval(np.polyfit(xs, ys, d), xte))
    P = np.array(preds); bias2 = float(((P.mean(0)-yte_clean)**2).mean()); var = float(P.var(0).mean())
    direct = float(((P-yte_clean)**2).mean())      # method B: average squared error over refits and grid
    return bias2, var, direct
for d in (1, 3, 9):
    b2, var, direct = decomp(d); two(f"l6 deg {d} bias2+var = mean sq error", b2+var, direct, 1e-9)
    print(f"     degree {d}: bias^2 {b2:.4f} variance {var:.4f} sum {b2+var:.4f}  (expected test MSE incl noise {b2+var+0.09:.4f})")

# ---------- l7 ----------
n = 50; rng = np.random.default_rng(4)
Q, _ = np.linalg.qr(rng.standard_normal((n, 4))); X = math.sqrt(n)*Q[:, :3]      # X'X = n I
b = np.array([3.0, 1.0, -0.5]); y = X@b + math.sqrt(n)*Q[:, 3]*2.0              # noise orthogonal to X
two("l7 X'y/n = b", float(np.abs(X.T@y/n-b).max()), 0.0, 1e-10)
soft = lambda z, t: np.sign(z)*np.maximum(np.abs(z)-t, 0)
for lam in (1.0, 0.5):
    las = Lasso(alpha=lam, fit_intercept=False, tol=1e-12, max_iter=100000).fit(X, y).coef_
    two(f"l7 lasso lambda {lam} vs soft threshold", float(np.abs(las-soft(b, lam)).max()), 0.0, 1e-6)
    rid = Ridge(alpha=n*lam, fit_intercept=False).fit(X, y).coef_
    two(f"l7 ridge lambda {lam} vs b/(1+lambda)", float(np.abs(rid-b/(1+lam)).max()), 0.0, 1e-9)
    print(f"     lambda {lam}: lasso {np.round(soft(b, lam), 4)} ridge {np.round(b/(1+lam), 4)}")
# duplicate columns
rng = np.random.default_rng(6); x1 = rng.standard_normal(200); Xd = np.c_[x1, x1]; yd = 2*x1 + 0.1*rng.standard_normal(200)
rd = Ridge(alpha=1e-6, fit_intercept=False).fit(Xd, yd).coef_
two("l7 ridge splits duplicate equally", float(abs(rd[0]-rd[1])), 0.0, 1e-6)
two("l7 ridge sum near 2", float(rd.sum()), float(np.polyfit(x1, yd, 1)[0]), 0.02)   # about 2
ld = Lasso(alpha=0.05, fit_intercept=False, tol=1e-12).fit(Xd, yd).coef_; print("     lasso on duplicates:", np.round(ld, 4), " ridge:", np.round(rd, 4))
two("l7 L2 penalty (1,1) = 2, (2,0) = 4", 1**2+1**2, 2.0); two("l7 L2 penalty (2,0)", 2**2+0**2, 4.0)
# sparse recovery: own coordinate descent vs sklearn
rng = np.random.default_rng(8); n, p = 60, 10
Xs = rng.standard_normal((n, p)); bt = np.zeros(p); bt[:3] = [3, -2, 1.5]; ys = Xs@bt + rng.standard_normal(n)
def cd(X, y, a, it=5000):
    n, p = X.shape; w = np.zeros(p)
    for _ in range(it):
        for j in range(p):
            r = y - X@w + X[:, j]*w[j]; z = X[:, j]@r/n; w[j] = np.sign(z)*max(abs(z)-a, 0)/((X[:, j]@X[:, j])/n)
    return w
for a in (0.1, 0.3, 1.0):
    w1 = cd(Xs, ys, a); w2 = Lasso(alpha=a, fit_intercept=False, tol=1e-12, max_iter=200000).fit(Xs, ys).coef_
    two(f"l7 nonzero count alpha {a}", int((np.abs(w1) > 1e-8).sum()), int((np.abs(w2) > 1e-8).sum()))
    print(f"     alpha {a}: nonzero {int((np.abs(w2) > 1e-8).sum())}  coefs {np.round(w2[:5], 3)}")
print("     ridge alpha 10 nonzero:", int((np.abs(Ridge(alpha=10, fit_intercept=False).fit(Xs, ys).coef_) > 1e-8).sum()), "of 10")

# ---------- l8 ----------
gini = lambda a, b: 1 - (F(a, a+b))**2 - (F(b, a+b))**2
two("l8 root gini 0.5", float(gini(10, 10)), 0.5); two("l8 child gini 0.32", float(gini(8, 2)), 0.32)
Xg = np.arange(20).reshape(-1, 1); yg = np.array([1,1,0,1,1,1,1,0,1,1, 0,0,1,0,0,0,0,1,0,0])   # left 8 up 2 down, right 2 up 8 down
t = DecisionTreeClassifier(max_depth=1, criterion="gini", random_state=0).fit(Xg, yg).tree_
two("l8 root impurity sklearn", float(t.impurity[0]), 0.5); two("l8 left child impurity sklearn", float(t.impurity[1]), 0.32, 1e-12)
two("l8 weighted child 0.32; gain 0.18", 0.5-0.32, float(t.impurity[0]-(t.n_node_samples[1]*t.impurity[1]+t.n_node_samples[2]*t.impurity[2])/20), 1e-12)
H = lambda p: -p*math.log2(p)-(1-p)*math.log2(1-p)
te = DecisionTreeClassifier(max_depth=1, criterion="entropy").fit(Xg, yg).tree_
two("l8 entropy child H(0.8)", H(0.8), float(te.impurity[1]), 1e-12); two("l8 entropy gain", 1-H(0.8), float(te.impurity[0]-te.impurity[1]), 1e-12)
print("     H(0.8) =", round(H(0.8), 4), " gain =", round(1-H(0.8), 4))
# bagging variance
sig2, rho, B = 4.0, 0.3, 100
hand = rho*sig2 + (1-rho)*sig2/B
Sg = sig2*((1-rho)*np.eye(B)+rho*np.ones((B, B))); Z = np.random.default_rng(1).multivariate_normal(np.zeros(B), Sg, 300000)
two("l8 bagging variance B=100 (sim tol .02)", hand, float(Z.mean(1).var()), 0.02); two("l8 limit rho*sigma2", 1.2, rho*sig2)
two("l8 bagging variance via 1^T Sigma 1 / B^2", hand, float(np.ones(B)@Sg@np.ones(B)/B**2), 1e-12)
print("     B=100:", hand, " B=10:", rho*sig2+(1-rho)*sig2/10)
# OOB fraction
two("l8 (1-1/100)^100", (1-1/100)**100, math.exp(100*math.log1p(-1/100)), 1e-12); print("     ", round((1-1/100)**100, 6), "1/e", round(math.exp(-1), 6))
bs = np.random.default_rng(3).integers(0, 100, (20000, 100)); oob = np.mean([100-len(np.unique(r)) for r in bs])/100
two("l8 OOB sim (tol .005)", (1-1/100)**100, float(oob), 0.005)
# boosting
xb4 = np.array([[1], [2], [3], [4]]); yb4 = np.array([1.0, 2, 6, 7])
F0 = yb4.mean(); r0 = yb4-F0; s1 = np.where(xb4[:, 0] <= 2, r0[:2].mean(), r0[2:].mean()); F1 = F0+0.4*s1
r1 = yb4-F1; s2 = np.where(xb4[:, 0] <= 2, r1[:2].mean(), r1[2:].mean()); F2 = F1+0.4*s2
gb1 = GradientBoostingRegressor(n_estimators=1, learning_rate=0.4, max_depth=1, random_state=0).fit(xb4, yb4)
gb2 = GradientBoostingRegressor(n_estimators=2, learning_rate=0.4, max_depth=1, random_state=0).fit(xb4, yb4)
two("l8 boosting round 1", float(np.abs(F1-gb1.predict(xb4)).max()), 0.0, 1e-12); two("l8 boosting round 2", float(np.abs(F2-gb2.predict(xb4)).max()), 0.0, 1e-12)
print("     F0", F0, "r0", r0, "F1", F1, "r1", r1, "F2", F2)
# importance with a duplicate and a high-cardinality noise feature
rng = np.random.default_rng(5); n = 1000; a = rng.standard_normal(n); Xi = np.c_[a, a, rng.integers(0, 500, n).astype(float), rng.standard_normal(n)]
yi = a + 0.5*rng.standard_normal(n)
rf = RandomForestRegressor(200, min_samples_leaf=5, random_state=0, n_jobs=1).fit(Xi[:700], yi[:700])
print("     impurity importance [x, copy of x, id-like noise, noise]:", np.round(rf.feature_importances_, 3))
pi = permutation_importance(rf, Xi[700:], yi[700:], n_repeats=20, random_state=0); print("     permutation importance (held out):", np.round(pi.importances_mean, 3))

# ---------- l9 ----------
vol = 0.20; R = (0.5*np.ones((3, 3)) + 0.5*np.eye(3)); C = vol**2*R
ev = np.sort(np.linalg.eigvalsh(C))[::-1]
two("l9 eig1 = 0.04(1+2*0.5) = 0.08", 0.04*(1+2*0.5), ev[0]); two("l9 eig2", 0.02, ev[1]); two("l9 PC1 share 2/3", 2/3, ev[0]/ev.sum())
Cu = np.array([[100, 9], [9, 1.0]]); tr, det = 101.0, 100*1-81
l1 = (tr+math.sqrt(tr*tr-4*det))/2; l2 = (tr-math.sqrt(tr*tr-4*det))/2; e2 = np.sort(np.linalg.eigvalsh(Cu))[::-1]
two("l9 raw eig1", l1, e2[0], 1e-9); two("l9 raw eig2", l2, e2[1], 1e-9); two("l9 raw PC1 share", l1/tr, e2[0]/e2.sum(), 1e-12)
print(f"     raw eigs {l1:.4f} {l2:.4f} share {l1/tr:.4%}")
Rc = np.array([[1, .9], [.9, 1.0]]); ec = np.sort(np.linalg.eigvalsh(Rc))[::-1]
two("l9 corr eig 1.9", 1.9, ec[0], 1e-12); two("l9 corr share 0.95", 0.95, ec[0]/2, 1e-12)
w, V = np.linalg.eigh(Cu); print("     raw PC1 direction", np.round(V[:, -1], 4))
# low-variance component carries the signal
rng = np.random.default_rng(12); Z = rng.standard_normal((500, 2)); Z -= Z.mean(0); Qz, _ = np.linalg.qr(Z); Qz *= math.sqrt(499)
rho = 0.95; s1 = math.sqrt(1+rho); s2 = math.sqrt(1-rho)
x1 = (s1*Qz[:, 0]+s2*Qz[:, 1])/math.sqrt(2); x2 = (s1*Qz[:, 0]-s2*Qz[:, 1])/math.sqrt(2)
yd = x1-x2
print("     sample corr x1,x2", round(float(np.corrcoef(x1, x2)[0, 1]), 6))
two("l9 y=x1-x2 R2 on PC1", 0.0, float(np.corrcoef(Qz[:, 0], yd)[0, 1]**2), 1e-12); two("l9 y R2 on PC2", 1.0, float(np.corrcoef(Qz[:, 1], yd)[0, 1]**2), 1e-12)
two("l9 PC1 share 0.975", (1+rho)/2, float(np.var(Qz[:, 0]*s1)/ (np.var(x1)+np.var(x2))), 1e-9)
# Marchenko-Pastur edge, p/n = 0.5
n, p = 2000, 1000; Xn = np.random.default_rng(0).standard_normal((n, p)); lam = np.linalg.eigvalsh(Xn.T@Xn/n)
two("l9 MP upper edge (1+sqrt(0.5))^2 (sim tol .06)", (1+math.sqrt(0.5))**2, float(lam[-1]), 0.06); two("l9 MP lower edge (1-sqrt .5)^2", (1-math.sqrt(0.5))**2, float(lam[0]), 0.03)
print("     sim top/bottom eig", round(float(lam[-1]),4), round(float(lam[0]),4)); print("     MP edges", round((1+math.sqrt(.5))**2, 4), round((1-math.sqrt(.5))**2, 4))

# ---------- l10 ----------
r_, n_ = 0.05, 250
t_ = r_*math.sqrt(n_-2)/math.sqrt(1-r_**2)
rr = stats.pearsonr  # not used for sample; check formula via exact-moment sample
rng = np.random.default_rng(13); Zs = rng.standard_normal((n_, 2)); Zs -= Zs.mean(0); Qs, _ = np.linalg.qr(Zs); Qs *= math.sqrt(n_-1)
xs_ = Qs[:, 0]; ys_ = r_*xs_ + math.sqrt(1-r_**2)*Qs[:, 1]
lr = stats.linregress(xs_, ys_); two("l10 t-stat of r=0.05, n=250", t_, lr.slope/lr.stderr, 1e-9); print("     t", round(t_, 4), "p", round(lr.pvalue, 4))
nreq = 2+1.959964**2*(1-r_**2)/r_**2; print("     n for |t|>=1.96 at r=0.05:", round(nreq, 1))
n2 = math.ceil(nreq); t2 = r_*math.sqrt(n2-2)/math.sqrt(1-r_**2); two("l10 t at ceil(n)", t2 >= 1.959964, True)
two("l10 t at ceil(n)-1 below", (r_*math.sqrt(n2-3)/math.sqrt(1-r_**2)) < 1.959964, True); print("     n =", n2)
two("l10 R2 = r^2", r_**2, 0.0025)
# single-asset signal Sharpe
rho_ = 0.05; hand_sr = rho_/math.sqrt(1+rho_**2)*math.sqrt(252)
rg = np.random.default_rng(21); N = 4_000_000; s = rg.standard_normal(N); rt = rho_*s + math.sqrt(1-rho_**2)*rg.standard_normal(N); pnl = s*rt
two("l10 annual Sharpe of z-score timing at IC .05 (sim tol .03)", hand_sr, float(pnl.mean()/pnl.std()*math.sqrt(252)), 0.03); print("     annual Sharpe", round(hand_sr, 4), "naive rho*sqrt(252)=", round(rho_*math.sqrt(252), 4))
# max |r| of 50 noise features, n=250
EmaxZ = integrate.quad(lambda z: 1-(2*Phi(z)-1)**50, 0, 12)[0]; hand_m = EmaxZ/math.sqrt(250)
rg = np.random.default_rng(31); mx = []
for _ in range(4000):
    Xn = rg.standard_normal((250, 50)); yv = rg.standard_normal(250)
    Xc = (Xn-Xn.mean(0))/Xn.std(0); yc = (yv-yv.mean())/yv.std(); mx.append(np.abs(Xc.T@yc/250).max())
two("l10 E[max |r|] of 50 noise features, n=250 (sim tol .005)", hand_m, float(np.mean(mx)), 0.005); print("     E max|r|", round(hand_m, 4), " R2", round(hand_m**2, 4), " E[max|Z|]", round(EmaxZ, 4), " mean max r^2 sim", round(float(np.mean(np.square(mx))), 4))
# leakage window of 3
rg = np.random.default_rng(41); rv = rg.standard_normal(1_000_000); ma = (rv + np.roll(rv, 1) + np.roll(rv, 2))/3
two("l10 corr(r_t, mean of r_t, r_t-1, r_t-2) = 1/sqrt(3) (sim tol .002)", 1/math.sqrt(3), float(np.corrcoef(rv, ma)[0, 1]), 0.002)
two("l10 honest lag feature (shifted) corr 0 (sim tol .003)", 0.0, float(np.corrcoef(rv[3:], ((np.roll(rv, 1)+np.roll(rv, 2)+np.roll(rv, 3))/3)[3:])[0, 1]), 0.003)
print("     leak R2 = 1/3 =", round(1/3, 4))
# regime flip, equal halves
z1 = rg.standard_normal((2, 5000)); 
def exact_pair(n, r, seed):
    g = np.random.default_rng(seed).standard_normal((n, 2)); g -= g.mean(0); q, _ = np.linalg.qr(g); q *= math.sqrt(n-1)
    return q[:, 0], r*q[:, 0]+math.sqrt(1-r*r)*q[:, 1]
xa, ya = exact_pair(500, 0.10, 1); xb_, yb_ = exact_pair(500, -0.10, 2)
two("l10 pooled corr of +0.1 and -0.1 halves = 0", 0.0, float(np.corrcoef(np.r_[xa, xb_], np.r_[ya, yb_])[0, 1]), 1e-12)
done()
