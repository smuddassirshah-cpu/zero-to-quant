"""Second reader's recomputation of stat-learning level 4 numbers (CPython, scikit-learn 1.6.1).
Independent of docs/reports/stat-learning-L4-numbers.py. Exit 1 if any check fails;
a check that fails because the content is wrong stays failing (see the review)."""
import copy, math, sys, warnings
from fractions import Fraction as F
from itertools import combinations
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, SplineTransformer, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

n_ok = n_bad = 0
def chk(name, got, want, tol=5e-5):
    global n_ok, n_bad
    g, w = np.asarray(got, float), np.asarray(want, float)
    ok = g.shape == w.shape and bool(np.all(np.abs(g - w) <= tol))
    n_ok += ok; n_bad += (not ok)
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f": got {np.round(g, 5).tolist()} want {w.tolist()}"))
def claim(name, ok):
    global n_ok, n_bad
    n_ok += bool(ok); n_bad += (not ok)
    print(("ok   " if ok else "FAIL ") + name)

def make_street(n, seed):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    X = rng.normal(0, 0.8, (n, 2)) + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y
def make_rings(n, seed):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    r = np.where(y == 1, rng.normal(0.8, 0.3, n), rng.normal(2.2, 0.4, n))
    a = rng.uniform(0, 2 * np.pi, n)
    return np.round(np.c_[r * np.cos(a), r * np.sin(a)], 3), y
def make_quadrants(n, seed):
    rng = np.random.default_rng(seed); X = rng.uniform(-2, 2, (n, 2))
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int); flip = rng.random(n) < 0.1
    return np.round(X, 3), np.where(flip, 1 - y, y)
def make_wide(n, seed, p=20):
    rng = np.random.default_rng(seed); y = np.arange(n) % 2
    X = rng.normal(0, 1, (n, p))
    X[:, :2] = X[:, :2] * 0.8 + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y
def make_noise(n, seed):
    rng = np.random.default_rng(seed); X = rng.normal(0, 1, (n, 2))
    return np.round(X, 3), (rng.random(n) < 0.54).astype(int)
def make_stocks(seed):
    rng = np.random.default_rng(seed); rows, lab = [], []
    for g, (b, v) in enumerate([(0.6, 20.0), (1.4, 20.0), (1.0, 45.0)]):
        rows.append(np.c_[rng.normal(b, 0.12, 20), rng.normal(v, 5.0, 20)]); lab += [g] * 20
    return np.round(np.vstack(rows), 2), np.array(lab)
def make_impact(n, seed):
    rng = np.random.default_rng(seed); x = rng.uniform(0, 50, n)
    return np.round(x, 3), np.round(10 * np.sqrt(x) + rng.normal(0, 4, n), 3)
def make_additive(n, seed, interaction=0.0):
    rng = np.random.default_rng(seed); X = rng.uniform(-2, 2, (n, 2))
    y = np.sin(1.5 * X[:, 0]) + 0.5 * X[:, 1] ** 2 + interaction * X[:, 0] * X[:, 1] + rng.normal(0, 0.3, n)
    return np.round(X, 3), np.round(y, 3)

print("== l15")
X6 = np.array([[1, 1], [0, 1], [2, 0], [3, 3], [4, 3], [3, 5]], float); y6 = np.array([0, 0, 0, 1, 1, 1])
m = SVC(kernel="linear", C=1e6).fit(X6, y6)
chk("six loans w", m.coef_[0], [0.5, 0.5], 1e-3); chk("b", m.intercept_[0], -2, 1e-3)
chk("support", sorted(m.support_), [0, 2, 3]); chk("margin", 1 / np.linalg.norm(m.coef_), 1.4142, 1e-3)
best = 0   # second route: search over unit normals for the widest gap between the classes
for th in np.linspace(0, np.pi, 180001):
    u = np.array([np.cos(th), np.sin(th)]); p = X6 @ u
    best = max(best, p[3:].min() - p[:3].max(), p[:3].min() - p[3:].max())
chk("street by direction search", best, 2 * math.sqrt(2), 1e-4)
Xm = X6.copy(); Xm[3] = [2.5, 3]
mm = SVC(kernel="linear", C=1e6).fit(Xm, y6)
chk("moved (3,3): slope", -mm.coef_[0][0] / mm.coef_[0][1], -0.75, 1e-3)
chk("moved: street", 2 / np.linalg.norm(mm.coef_), 2.5, 1e-3)
chk("moved: intercept", -mm.intercept_[0] / mm.coef_[0][1], 3.3125, 2e-3)
Xn = X6.copy(); Xn[5] = [5, 6]
mn = SVC(kernel="linear", C=1e6).fit(Xn, y6); chk("moved (3,5): w unchanged", mn.coef_[0], [0.5, 0.5], 1e-3)
def street(mm_, b):
    s = min(mm_ + b - 1, b - 1, 2 * mm_ + b, 3 - 3 * mm_ - b, 3 - 4 * mm_ - b, 5 - 3 * mm_ - b)
    return 2 * s / math.sqrt(mm_ * mm_ + 1)
chk("slider start street", street(-0.5, 3.5), 1.79, 0.005); chk("slider best", street(-1, 4), 2.828, 0.001)
Xs, ys = make_street(200, 4); Xt, yt = make_street(200, 5)
for C, want in [(0.01, (94, 2.78, 0.975)), (1, (24, 1.07, 0.965)), (100, (21, 0.80, 0.95))]:
    m = SVC(kernel="linear", C=C).fit(Xs, ys)
    chk(f"street C={C}", [len(m.support_), round(2 / np.linalg.norm(m.coef_), 2), m.score(Xt, yt)], want, 0.0051)
Xr, yr = make_rings(300, 7); Xe, ye = make_rings(300, 8)
m = SVC(kernel="linear", C=1).fit(Xr, yr); chk("rings linear", [len(m.support_), m.score(Xr, yr), m.score(Xe, ye)], [298, 0.66, 0.65])
chk("rings logistic", LogisticRegression().fit(Xr, yr).score(Xe, ye), 0.5067)
f = lambda X: np.c_[X, (X ** 2).sum(1)]
m = SVC(kernel="linear", C=1).fit(f(Xr), yr); chk("rings + r2 column", m.score(f(Xe), ye), 0.9733)
w = m.coef_[0]; chk("w3, b", [w[2], m.intercept_[0]], [-2.26, 4.50], 0.006); chk("radius", math.sqrt(-m.intercept_[0] / w[2]), 1.41, 0.005)
claim("w1, w2 small next to w3 (|.| < 0.25): circle centre within 0.06 of the origin", abs(w[0]) < 0.25 and abs(w[1]) < 0.25)
rows = {0.01: (300, .6333, .61), 0.1: (76, .99, .97), 1: (44, .9967, .98), 10: (177, .9967, .97), 100: (289, 1.0, .87), 1000: (300, 1.0, .64)}
for g, want in rows.items():
    m = SVC(kernel="rbf", C=1, gamma=g).fit(Xr, yr); chk(f"rbf gamma={g}", [len(m.support_), m.score(Xr, yr), m.score(Xe, ye)], want)
def pick(C, gs=(0.01, 0.1, 1, 10)):
    out = [(round(SVC(kernel="rbf", C=C, gamma=g).fit(Xr[:-100], yr[:-100]).score(Xr[-100:], yr[-100:]), 4), -g) for g in gs]
    a, g = max(out); return [-g, a]
for C, want in [(1, [1, 1.0]), (100, [0.01, 1.0]), (10, [0.1, 1.0]), (0.1, [1, 0.99])]:
    chk(f"pick_gamma C={C}", pick(C), want)
X7 = np.vstack([X6, [1.5, 0.5]]); y7 = np.r_[y6, 1]
m = SVC(kernel="linear", C=1).fit(X7, y7)
d7 = m.decision_function([[1.5, 0.5]])[0]
print("   q3: w", np.round(m.coef_[0], 3), "b", np.round(m.intercept_, 3), "decision", round(d7, 3))
chk("q3 line about x1+x2=4, decision -1 (slack 2)", [m.coef_[0][0] / m.coef_[0][1], -m.intercept_[0] / m.coef_[0][1], d7], [1, 4, -1], 0.05)
Xs100, Xt100 = Xs * [100, 1], Xt * [100, 1]
for g in (1, "scale"):
    a = SVC(kernel="rbf", C=1, gamma=g).fit(Xs, ys).score(Xt, yt); b_ = SVC(kernel="rbf", C=1, gamma=g).fit(Xs100, ys).score(Xt100, yt)
    print(f"   q4 rbf gamma={g}: plain {a:.4f}, first column x100 {b_:.4f}")
chk("q4 second column x100, gamma=1", [SVC(kernel="rbf", C=1, gamma=1).fit(Xs, ys).score(Xt, yt), SVC(kernel="rbf", C=1, gamma=1).fit(Xs * [1, 100], ys).score(Xt * [1, 100], yt)], [0.965, 0.795])
chk("q1 distance of (3,5)", 2 / math.sqrt(0.5), 2.83, 0.005); chk("q4 ratio", 40 / 0.3, 133, 0.5)

print("== l16")
S = [10, 12, 14, 30, 32, 40]
def km1(S, C, rounds=50):
    C = [F(c) for c in C]; hist = []
    for _ in range(rounds):
        lab = [min(range(len(C)), key=lambda j: (abs(x - C[j]), j)) for x in S]
        newC = [sum(x for x, l in zip(S, lab) if l == j) / F(lab.count(j)) if lab.count(j) else C[j] for j in range(len(C))]
        hist.append((lab, newC))
        if newC == C: break
        C = newC
    return hist
h = km1(S, [10, 12]); chk("round 1 centres", [float(c) for c in h[0][1]], [10, 25.6]); chk("final centres", [float(c) for c in h[-1][1]], [12, 34])
ine = lambda lab, C: float(sum((x - C[l]) ** 2 for x, l in zip(S, lab)))
chk("inertia 2", ine(*h[-1]), 64)
h3 = km1(S, [10, 12, 14]); chk("bad start centres", [float(c) for c in h3[-1][1]], [10, 13, 34]); chk("bad start inertia", ine(*h3[-1]), 58)
def best_inertia(k):   # exhaustive over contiguous partitions
    best = 1e9
    for cuts in combinations(range(1, 6), k - 1):
        b = [0, *cuts, 6]; tot = 0
        for i in range(k):
            g = S[b[i]:b[i + 1]]; mu = F(sum(g), len(g)); tot += sum((x - mu) ** 2 for x in g)
        best = min(best, float(tot))
    return best
chk("best inertias k=1..4", [best_inertia(k) for k in (1, 2, 3, 4)], [790, 64, 10, 4])
chk("CONTENT s2 wrong 'unsq': the sum its feedback writes (2+0+2+4+2+6) equals the stored 12", 2 + 0 + 2 + 4 + 2 + 6, 12)
chk("CONTENT s1 wrong 'half': halfway between old and new centres equals the stored 11, 29", [(10 + 12) / 2, (25.6 + 34) / 2], [11, 29])
Xk, lab = make_stocks(11)
chk("sds", Xk.std(0), [0.336, 13.04], 0.006)
def purity(l):
    return sum(np.bincount(lab[l == j]).max() for j in np.unique(l)) / len(l)
chk("purity raw", purity(KMeans(3, n_init=10, random_state=0).fit(Xk).labels_), 0.75)
raw_best = min(KMeans(3, n_init=1, random_state=s).fit(Xk).inertia_ for s in range(200))
k50 = KMeans(3, n_init=50, random_state=1).fit(Xk); print("   raw inertia: 10 starts", round(KMeans(3, n_init=10, random_state=0).fit(Xk).inertia_, 2), "; best of 200 single starts", round(raw_best, 2), "; n_init=50:", round(k50.inertia_, 2), "purity", round(purity(k50.labels_), 4))
chk("CONTENT s5 option c why: 'Ten starts found the lowest raw inertia' (equals the best of 200 single starts)", KMeans(3, n_init=10, random_state=0).fit(Xk).inertia_, raw_best, 1e-6)
Z = StandardScaler().fit_transform(Xk)
chk("purity scaled", purity(KMeans(3, n_init=10, random_state=0).fit(Z).labels_), 1.0)
chk("scaled inertias", [round(KMeans(k, n_init=10, random_state=0).fit(Z).inertia_, 2) for k in range(1, 8)], [120, 62.39, 14.16, 11.24, 9.79, 7.92, 6.47], 0.006)
chk("k=4 sizes", sorted(np.bincount(KMeans(4, n_init=10, random_state=0).fit(Z).labels_)), [6, 14, 20, 20])
Zn = StandardScaler().fit_transform(make_noise(300, 4)[0])
ni = [KMeans(k, n_init=10, random_state=0).fit(Zn).inertia_ for k in range(1, 8)]
chk("noise inertias", ni, [600, 402.4, 277.8, 216.2, 179.0, 148.9, 128.9], 0.06)
chk("noise drops", -np.diff(ni), [198, 125, 62, 37, 30, 20], 0.6)
chk("noise k=3 sizes", sorted(np.bincount(KMeans(3, n_init=10, random_state=0).fit(Zn).labels_)), [88, 98, 114])
D5 = np.array([[0, 0.2, 0.6, 0.7, 0.8], [0.2, 0, 0.65, 0.75, 0.85], [0.6, 0.65, 0, 0.3, 0.9], [0.7, 0.75, 0.3, 0, 0.95], [0.8, 0.85, 0.9, 0.95, 0]])
for meth, want, cut in [("single", [0.2, 0.3, 0.6, 0.8], 2), ("complete", [0.2, 0.3, 0.75, 0.95], 3), ("average", [0.2, 0.3, 0.675, 0.875], 2)]:
    L = linkage(squareform(D5), meth); chk(f"heights {meth}", L[:, 2], want); chk(f"cut 0.70 {meth}", len(set(fcluster(L, 0.70, "distance"))), cut)
chk("pairs", [math.comb(60, 2), 3 * math.comb(20, 2), 20 * 19 * 3, 570 / 1770], [1770, 570, 1140, 1 / 3], 0.012)
chk("q4", [16 + 4 + 36, 56 / 3, 4 + 2 + 6], [56, 18.67, 12], 0.005)

print("== l17")
sig = lambda z: 1 / (1 + math.exp(-z))
def net(x1, x2, relu=True):
    r = (lambda v: max(0, v)) if relu else (lambda v: v)
    return 4 * r(x1 + x2) - 8 * r(x1 + x2 - 1) - 2
chk("corners z", [net(*c) for c in [(0, 0), (1, 0), (0, 1), (1, 1)]], [-2, 2, 2, -2]); chk("p", [sig(-2), sig(2)], [0.1192, 0.8808])
chk("(0.5,0.8)", [net(0.5, 0.8), sig(net(0.5, 0.8)), 1 - sig(0.8), sig(4 * 1.3 - 2)], [0.8, 0.69, 0.31, 0.96], 0.005)
chk("norelu6", net(0, 0, False), 6)
npar = lambda s: sum(a * b + b for a, b in zip(s, s[1:]))
chk("params", [npar([2, 2, 1]), npar([2, 8, 1]), npar([10, 16, 16, 1]), npar([4, 6, 3]), npar([2, 3, 1]), npar([2, 64, 5]), npar([25, 64, 1])], [9, 33, 465, 51, 13, 517, 1729])
def gd(w1, w2, x, y, lr):
    h = max(0, w1 * x); e = w2 * h - y; g2 = e * h; g1 = e * w2 * (x if w1 * x > 0 else 0)
    w1, w2 = w1 - lr * g1, w2 - lr * g2
    return w1, w2, 0.5 * (w2 * max(0, w1 * x) - y) ** 2
L = lambda w1, w2: 0.5 * (w2 * max(0, w1 * 2) - 3) ** 2
chk("slopes by finite difference", [(L(0.5 + 1e-6, 2) - L(0.5 - 1e-6, 2)) / 2e-6, (L(0.5, 2 + 1e-6) - L(0.5, 2 - 1e-6)) / 2e-6], [-4, -1], 1e-4)
chk("step 0.1", gd(0.5, 2, 2, 3, 0.1), [0.9, 2.1, 0.3042]); chk("step 0.5", gd(0.5, 2, 2, 3, 0.5), [2.5, 2.5, 45.125])
chk("dead", gd(-0.5, 2, 2, 3, 0.1), [-0.5, 2, 4.5]); chk("fresh", gd(1, 1, 1, 0.5, 0.1), [0.95, 0.95, 0.081])
chk("q2 v", np.array([3, -1]) @ np.array([[1, 2], [0, 1]]), [3, 5])
chk("CONTENT q2 wrong 'order': W1 w2 (the wrong order), second entry, equals the stored 6", (np.array([[1, 2], [0, 1]]) @ np.array([3, -1]))[1], 6)
chk("q4 ratio", 2e6 / 0.01, 2e8)
def mlp(h, seed, Xa, ya, Xb, yb):
    m = MLPClassifier(hidden_layer_sizes=(h,), solver="lbfgs", alpha=0.01, random_state=seed, max_iter=500).fit(Xa, ya)
    return round(m.score(Xa, ya), 4), round(m.score(Xb, yb), 4)
sw = [mlp(h, 0, Xr, yr, Xe, ye)[1] for h in (1, 2, 3, 8, 64)]
print("   CPython width sweep", sw, "(lesson, Pyodide: 0.6567 0.6467 0.82 0.97 0.97)")
chk("width sweep within 0.005 of the lesson", sw, [0.6567, 0.6467, 0.82, 0.97, 0.97], 0.005)
sd = [mlp(8, s, Xr, yr, Xe, ye)[1] for s in (0, 1, 2)]; print("   CPython seeds", sd)
chk("seeds within 0.005", sd, [0.97, 0.9667, 0.96], 0.005)
Xno, yno = make_noise(300, 4); Xnt, ynt = make_noise(300, 5)
chk("noise base rate on test rows", ynt.mean(), 0.55); print("   train base rate", round(yno.mean(), 4))
nz = [mlp(8, s, Xno, yno, Xnt, ynt) for s in (0, 1, 2)]
print("   CPython noise (train, test)", nz, " lesson (Pyodide): (0.5833,0.5567) (0.6033,0.5000) (0.6500,0.4967)")
se = math.sqrt(0.55 * 0.45 / 300)
claim("noise: every CPython test score within 2 se of the base rate, or below it", all(t <= 0.55 + 2 * se for _, t in nz))
claim("noise: every lesson test score within 2 se of the base rate, or below it", all(t <= 0.55 + 2 * se for t in (0.5567, 0.5, 0.4967)))
claim("CONTENT noise option a: 'test accuracy sits at or below the 0.55 base rate' for seed 0 (0.5567 <= 0.55)", 0.5567 <= 0.55)
claim("CONTENT noise explain: 'values move in the third place on another runtime' (max |Pyodide - CPython| < 0.005)", max(abs(a - b) for (_, a), b in zip(nz, (0.5567, 0.5, 0.4967))) < 0.005)
n64 = [mlp(64, s, Xno, yno, Xnt, ynt) for s in (0, 1, 2)]; print("   noise 64 units (train, test)", n64)
claim("64 units: training above every 8-unit score, test between 0.44 and 0.57", min(a for a, _ in n64) > max(a for a, _ in nz) and all(0.44 <= t <= 0.57 for _, t in n64))

print("== l18")
x, y = make_impact(200, 21); xt, yt2 = make_impact(200, 22)
lin = LinearRegression().fit(x[:, None], y)
chk("line", [lin.intercept_, lin.coef_[0], lin.predict([[1]])[0], lin.score(xt[:, None], yt2)], [17.417, 1.170, 18.59, 0.9088], 0.005)
p12 = make_pipeline(PolynomialFeatures(12), StandardScaler(), LinearRegression()).fit(x[:, None], y)
chk("degree 12", [p12.score(xt[:, None], yt2), p12.predict([[55]])[0], 10 * math.sqrt(55)], [0.9381, 216.23, 74.16], 0.02)
H = lambda x, ks: np.column_stack([np.ones_like(x), x] + [np.maximum(0, x - c) for c in ks])
r2 = lambda yy, pp: 1 - ((yy - pp) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()
for ks, coef, sc, at1 in [((5,), [4.893, 4.653, -3.652], 0.9289, 9.55), ((5, 20), [5.789, 3.822, -2.459, -0.488], 0.9426, 9.61), ((10, 30), [7.456, 2.647, -1.624, -0.173], 0.9428, 10.10)]:
    c = np.linalg.solve(H(x, ks).T @ H(x, ks), H(x, ks).T @ y)   # normal equations, not lstsq
    chk(f"linear spline {ks}", [*c, r2(yt2, H(xt, ks) @ c), (H(np.array([1.0]), ks) @ c)[0]], [*coef, sc, at1], 0.006)
chk("slopes", [3.822 - 2.459, 3.822 - 2.459 - 0.488], [1.363, 0.875], 1e-9)
sp = lambda k, **kw: make_pipeline(SplineTransformer(n_knots=k, degree=3, **kw), LinearRegression())
for k, want in [(2, (.9575, .9424)), (3, (.9586, .9439)), (5, (.9598, .9417)), (10, (.9613, .938)), (40, (.9652, .9347))]:
    m = sp(k).fit(x[:, None], y); chk(f"cubic spline {k}", [m.score(x[:, None], y), m.score(xt[:, None], yt2)], want)
chk("columns", [SplineTransformer(n_knots=5, degree=3).fit_transform(x[:, None]).shape[1], SplineTransformer(n_knots=4, degree=3).fit_transform(x[:, None]).shape[1] * 3], [7, 18])
val = {k: sp(k).fit(x[:150, None], y[:150]).score(x[150:, None], y[150:]) for k in (2, 3, 5, 10, 40)}
print("   validation R2 by knots", {k: round(v, 4) for k, v in val.items()})
chk("validation picks 5 at 0.9495, 3 at 0.9494", [max(val, key=val.get), val[5], val[3]], [5, 0.9495, 0.9494])
chk("linear tail at 55", sp(5, extrapolation="linear").fit(x[:, None], y).predict([[55]])[0], 85.13, 0.006)
rg = make_pipeline(SplineTransformer(n_knots=40, degree=3), Ridge(alpha=1)).fit(x[:, None], y)
chk("ridge on 40 knots", rg.score(xt[:, None], yt2), 0.8868)
g = np.array([1.0, 10, 25, 40, 49]); pr = rg.predict(g[:, None]); p5 = sp(5).fit(x[:, None], y).predict(g[:, None])
print("   ridge(1) fit at 1,10,25,40,49:", np.round(pr, 1), " 5-knot:", np.round(p5, 1), " truth:", np.round(10 * np.sqrt(g), 1))
claim("ridge(1) on B-spline columns pulls both ends towards the mean (a bias in level, not only less wiggle)", pr[0] > p5[0] + 2 and pr[-1] < p5[-1] - 2)
Xa, ya = make_additive(300, 31); Xb, yb = make_additive(300, 32)
add = lambda k: make_pipeline(SplineTransformer(n_knots=k, degree=3), LinearRegression())
chk("additive", [LinearRegression().fit(Xa, ya).score(Xb, yb), add(5).fit(Xa, ya).score(Xb, yb)], [0.3744, 0.9101])
Xa1, ya1 = make_additive(300, 31, 1.0); Xb1, yb1 = make_additive(300, 32, 1.0)
chk("interaction", [LinearRegression().fit(Xa1, ya1).score(Xb1, yb1)] + [add(k).fit(Xa1, ya1).score(Xb1, yb1) for k in (5, 10, 20)], [0.1213, 0.3292, 0.2373, 0.172])
m5 = sp(5).fit(x[:, None], y); sav = lambda s: m5.predict([[s]])[0] - m5.predict([[s / 2]])[0]
lo, hi = 1.0, 6.0
for _ in range(60):
    mid = (lo + hi) / 2; lo, hi = (mid, hi) if sav(mid) < 5 else (lo, mid)
chk("saving crosses 5 at", lo, 3.02, 0.01); chk("saving at 2 and 5", [sav(2), sav(5)], [3.54, 7.26], 0.006)
chk("true law crossing, line crossing", [(5 / (10 * (1 - 1 / math.sqrt(2)))) ** 2, 5 / (1.17 / 2)], [2.91, 8.5], 0.05)
chk("q2 gaps", [216.23 - 74.16, 216.23 - 85.13], [142, 131], 0.2)
chk("CONTENT r-few-rows option d: 25 features through SplineTransformer(n_knots=10) give the stored 250 columns", SplineTransformer(n_knots=10, degree=3).fit_transform(np.random.default_rng(0).normal(size=(80, 25))).shape[1], 250)

print("== l19")
P = {"street": (*make_street(300, 4), *make_street(300, 5)), "rings": (Xr, yr, Xe, ye), "quadrants": (*make_quadrants(300, 3), *make_quadrants(300, 4)),
     "wide": (*make_wide(60, 4), *make_wide(300, 5)), "noise": (Xno, yno, Xnt, ynt)}
Lr = {"logistic": lambda: make_pipeline(StandardScaler(), LogisticRegression()),
      "additive": lambda: make_pipeline(StandardScaler(), SplineTransformer(n_knots=5), LogisticRegression(max_iter=2000)),
      "knn": lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(15)),
      "svm": lambda: make_pipeline(StandardScaler(), SVC(C=1, gamma="scale")),
      "net": lambda: make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500))}
T = {"street": [.9633, .9633, .9633, .9567, .96], "rings": [.5067, .9767, .9767, .9733, .98], "quadrants": [.4767, .86, .8567, .8467, .4567],
     "wide": [.9233, .89, .92, .9067, .9167], "noise": [.5567, .4967, .5567, .5367, .5333]}
order = ["logistic", "knn", "svm", "net", "additive"]
for p, (A, a, B, b) in P.items():
    got = [round(Lr[k]().fit(A, a).score(B, b), 4) for k in order]
    chk(f"table {p} (deterministic cells)", [got[i] for i in (0, 1, 2, 4)], [T[p][i] for i in (0, 1, 2, 4)])
    chk(f"table {p} network cell within 0.03 (CPython {got[3]})", got[3], T[p][3], 0.03)
    nv = 20 if p == "wide" else 100
    va = {k: Lr[k]().fit(A[:-nv], a[:-nv]).score(A[-nv:], a[-nv:]) for k in Lr}
    print("   validation", p, {k: round(v, 4) for k, v in va.items()})
chk("t", [(167 / 300 - 0.55) / se, (0.5567 - 0.5) / math.sqrt(0.25 / 300), 0.5567 - 0.55], [0.23, 1.96, 0.0067], 0.005)
for s1, s2, want in [(9, 10, [.48, .98, .98, .9733, .9833]), (11, 12, [.5167, .9633, .9667, .9567, .9567])]:
    A, a = make_rings(300, s1); B, b = make_rings(300, s2); got = [round(Lr[k]().fit(A, a).score(B, b), 4) for k in order]
    chk(f"rings seeds {s1},{s2}", [got[i] for i in (0, 1, 2, 4)], [want[i] for i in (0, 1, 2, 4)], 0.004); chk("  network within 0.02", got[3], want[3], 0.02)
worst = {k: 0 for k in order}; bestc = {k: 0 for k in order}; mean = {k: 0.0 for k in order}
for s in range(20):   # s3: is 'few rows and noisy columns hurt the distance-based learner most' a property of the seed?
    A, a = make_wide(60, 100 + s); B, b = make_wide(300, 200 + s); sc = {k: Lr[k]().fit(A, a).score(B, b) for k in order}
    worst[min(sc, key=sc.get)] += 1; bestc[max(sc, key=sc.get)] += 1
    for k in order: mean[k] += sc[k] / 20
print("   wide over 20 seed pairs: mean", {k: round(v, 3) for k, v in mean.items()}, "worst", worst, "best", bestc)
claim("wide: k-NN has the lowest mean over 20 seed pairs", min(mean, key=mean.get) == "knn")
claim("CONTENT s3 explain: 'few rows and many noisy features favour the simplest learner': logistic has the highest mean over 20 seed pairs", max(mean, key=mean.get) == "logistic")
A, a, B, b = P["street"]; A2, B2 = A * [100, 1], B * [100, 1]
raw = {"logistic": LogisticRegression(), "knn": KNeighborsClassifier(15), "svm": SVC(C=1, gamma="scale"),
       "net": MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500),
       "additive": make_pipeline(SplineTransformer(n_knots=5), LogisticRegression(max_iter=2000))}
for k in order:   # s6: which learners (without a scaler) change when one column changes units
    m1 = copy.deepcopy(raw[k]).fit(A, a); m2 = copy.deepcopy(raw[k]).fit(A2, a)
    dv = lambda mm_, XX: mm_.predict_proba(XX)[:, 1] if hasattr(mm_, "predict_proba") else mm_.decision_function(XX)
    same = bool(np.abs(dv(m1, B) - dv(m2, B2)).max() < 1e-6)
    claim(f"s6 units: {k} output {'unchanged' if k == 'additive' else 'changes'} when one column is x100 (no scaler)", same == (k == "additive"))
one = Lr["svm"](); r1 = []
for p in ("street", "quadrants"):
    A, a, B, b = P[p]; r1.append(one.fit(A, a).score(B, b))
r2_ = [Lr["svm"]().fit(*P[p][:2]).score(*P[p][2:]) for p in ("street", "quadrants")]
claim("CONTENT s7 explain: a reused, refitted pipeline scores differently from a fresh one ('carries state')", r1 != r2_)

print("== review-4 and homework-4")
chk("r-street", [2 / 5, 1 / 5, 10 / 5], [0.4, 0.2, 2])
pts = np.array([[0, 0], [2, 0], [0, 4], [10, 10], [12, 10]], float); c = np.array([[0, 0], [10, 10.0]])
l = ((pts[:, None] - c[None]) ** 2).sum(2).argmin(1); c2 = np.array([pts[l == j].mean(0) for j in (0, 1)])
chk("r-kmeans", [((pts - c2[l]) ** 2).sum(), ((pts - c[l]) ** 2).sum(), ((pts - c2[l]) ** 2).sum(1)[:3].sum()], [15.33, 24, 13.33], 0.005)
h1, h2 = max(0, 2 - 3), max(0, 3 - 1); chk("r-forward", [sig(3 * h1 + 2 * h2 - 4), sig(3 * -1 + 4 - 4)], [0.5, 0.05], 0.005)
chk("r-spline", [1 + 12 + 12 - 4, 1 + 12 + 12, 13], [21, 25, 13])
s_ = math.sqrt(.53 * .47 / 400); chk("r-t", [0.04 / s_, 0.07 / 0.025, 0.04 / s_ ** 2], [1.60, 2.8, 64.23], 0.006)
D4 = [0.1, 0.5, 0.9, 0.6, 0.7, 0.4]   # condensed: AB AC AD BC BD CD
chk("r-linkage", [linkage(D4, m_)[2, 2] for m_ in ("average", "single", "complete")], [0.675, 0.5, 0.9])
chk("r-linkage first merges", linkage(D4, "average")[:2, 2], [0.1, 0.4])
Xh = np.array([[1, 2], [2, 1], [0, 0], [4, 5], [5, 4], [6, 6]], float); yh = np.array([0, 0, 0, 1, 1, 1])
m = SVC(kernel="linear", C=1e6).fit(Xh, yh)
chk("h-margin", [*m.coef_[0], m.intercept_[0], 1 / np.linalg.norm(m.coef_)], [1 / 3, 1 / 3, -2, 2.12], 0.005)
dv = np.abs(m.decision_function(Xh)); claim("h-margin: P1, P2, P4, P5 on the edges; P3, P6 clear", np.allclose(dv[[0, 1, 3, 4]], 1, atol=1e-3) and dv[2] > 1.5 and dv[5] > 1.5)
W = np.array([[1, -1], [0, 2], [-1, 1.0]]); bh = np.array([0, -1, 0.5]); hh = W @ [2, 1] + bh
chk("h-net", [np.maximum(0, hh) @ [2, 1, -3] + 0.5, hh @ [2, 1, -3] + 0.5, np.maximum(0, hh) @ [2, 1, -3], sig(3.5)], [3.5, 5, 3, 0.97], 0.005)
chk("h-df", [5 * 4 - 3 * 4, 4 + 4], [8, 8])
sv = SVC(kernel="rbf", C=1, gamma=1).fit(Xr, yr); sv2 = SVC(kernel="rbf", C=10, gamma=0.5).fit(Xr, yr)
chk("h-rbf", [*sv.decision_function([[0, 0], [1.5, 0], [0.3, -2.1]]), sv2.decision_function([[0, 0]])[0], len(sv.support_), 2 * math.exp(-1) - 1], [2.127469, -0.082931, -1.539442, 5.539871, 44, -0.264241], 1e-5)
print(f"\nread-numbers: {n_ok} of {n_ok + n_bad} checks pass"); sys.exit(1 if n_bad else 0)
