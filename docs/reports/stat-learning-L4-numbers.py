"""stat-learning level 4: every stated number recomputed twice, then tied to where the level states it.

Run with the scratchpad venv (NumPy 2.0, SciPy, scikit-learn 1.6.1):
    <venv>/bin/python docs/reports/stat-learning-L4-numbers.py [--verbose]
Route A is scikit-learn or NumPy as the lessons use them; route B is an independent route
(exact arithmetic, a hand loop, a closed form, or predictions counted by hand). The Pyodide values
of every code screen come from the playthrough, whose hidden tests carry them; the network cells are
bands there (MLPClassifier agrees with CPython only to the third place), and here they are claimed
within 0.01 of the Pyodide values the lessons state.
"""
import math
import os
import sys
import warnings
from fractions import Fraction as F

import numpy as np

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

from scipy.cluster.hierarchy import linkage, fcluster  # noqa: E402
from scipy.spatial.distance import squareform  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge  # noqa: E402
from sklearn.neighbors import KNeighborsClassifier  # noqa: E402
from sklearn.neural_network import MLPClassifier  # noqa: E402
from sklearn.pipeline import make_pipeline  # noqa: E402
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer, StandardScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402

lv = Level("stat-learning", 4)
ok = lv.claim


def close(a, b, t=1e-9):
    return abs(a - b) <= t


# ---------------------------------------------------------------- generators (the brief's, unchanged)
def make_street(n, seed):
    rng = np.random.default_rng(seed)
    y = np.arange(n) % 2
    X = rng.normal(0, 0.8, (n, 2)) + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y


def make_rings(n, seed):
    rng = np.random.default_rng(seed)
    y = np.arange(n) % 2
    r = np.where(y == 1, rng.normal(0.8, 0.3, n), rng.normal(2.2, 0.4, n))
    a = rng.uniform(0, 2 * np.pi, n)
    return np.round(np.c_[r * np.cos(a), r * np.sin(a)], 3), y


def make_quadrants(n, seed):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-2, 2, (n, 2))
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int)
    flip = rng.random(n) < 0.1
    return np.round(X, 3), np.where(flip, 1 - y, y)


def make_wide(n, seed, p=20):
    rng = np.random.default_rng(seed)
    y = np.arange(n) % 2
    X = rng.normal(0, 1, (n, p))
    X[:, :2] = X[:, :2] * 0.8 + np.where(y[:, None] == 1, 1.0, -1.0)
    return np.round(X, 3), y


def make_noise(n, seed):
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (n, 2))
    return np.round(X, 3), (rng.random(n) < 0.54).astype(int)


def make_stocks(seed):
    rng = np.random.default_rng(seed)
    rows, lab = [], []
    for g, (b, v) in enumerate([(0.6, 20.0), (1.4, 20.0), (1.0, 45.0)]):
        rows.append(np.c_[rng.normal(b, 0.12, 20), rng.normal(v, 5.0, 20)])
        lab += [g] * 20
    return np.round(np.vstack(rows), 2), np.array(lab)


def make_impact(n, seed):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 50, n)
    return np.round(x, 3), np.round(10 * np.sqrt(x) + rng.normal(0, 4, n), 3)


def make_additive(n, seed, interaction=0.0):
    rng = np.random.default_rng(seed)
    X = rng.uniform(-2, 2, (n, 2))
    y = np.sin(1.5 * X[:, 0]) + 0.5 * X[:, 1] ** 2 + interaction * X[:, 0] * X[:, 1] + rng.normal(0, 0.3, n)
    return np.round(X, 3), np.round(y, 3)


def acc_by_hand(model, X, y):
    return float(np.mean(model.predict(X) == y))


# ================================================================ l15 support vector machines
X6 = np.array([[1, 1], [0, 1], [2, 0], [3, 3], [4, 3], [3, 5]], float)
y6 = np.array([0, 0, 0, 1, 1, 1])
s6 = np.where(y6 == 1, 1, -1)
# route A: hard margin by SVC; route B: exact w = (1/2, 1/2), b = -2
hard = SVC(kernel="linear", C=1e6).fit(X6, y6)
w, b = np.array([0.5, 0.5]), -2.0
ok(np.allclose(hard.coef_[0], w, atol=1e-3) and close(hard.intercept_[0], b, 1e-3), "l15 hard margin w = (0.5, 0.5), b = -2 (SVC and by hand)")
ok(sorted(hard.support_.tolist()) == [0, 2, 3] and np.flatnonzero(np.abs(s6 * (X6 @ w + b) - 1) < 1e-12).tolist() == [0, 2, 3], "l15 support vectors (1,1), (2,0), (3,3)")
margin = 1 / math.sqrt(0.5)
ok(close(margin, math.sqrt(2)) and close(2 * margin, 2 * math.sqrt(2)), "l15 margin sqrt 2, street 2 sqrt 2")
lv.expect("l15", "screens[2].widget.answer", round(margin, 4))
lv.expect("l15", "screens[2].widget.wrong[0].value", round(math.sqrt(0.5), 4))
lv.expect("l15", "screens[2].widget.wrong[1].value", round(2 * margin, 4))
lv.expect("l15", "screens[0].feedback.correct", 2.83)
# the widest line over a fine grid of (m, b) beats every other: brute force (route B for the optimum)
best = max(((2 * min(m + bb - 1, bb - 1, 2 * m + bb, 3 - 3 * m - bb, 3 - 4 * m - bb, 5 - 3 * m - bb) / math.sqrt(m * m + 1)), m, bb)
           for m in np.arange(-3, 0.001, 0.05) for bb in np.arange(0, 8.001, 0.1))
ok(close(best[0], 2 * math.sqrt(2), 1e-9) and close(best[1], -1, 1e-9) and close(best[2], 4, 1e-9), "l15 slider optimum slope -1, intercept 4, width 2.828")
ok(close(2 * min(-0.5 + 3.5 - 1, 2.5, -1 + 3.5, 3 + 1.5 - 3.5, 3 + 2 - 3.5, 5 + 1.5 - 3.5) / math.sqrt(1.25), 1.789, 0.001), "l15 opening slider street 1.79")
# vertical line x = 2.5: street 1; scaled w = (2, 0), b = -5, margin 0.5
ok(close(min(abs(X6[:, 0] - 2.5)) * 2, 1.0), "l15 vertical street width 1")
lv.expect("l15", "screens[0].prose", 1)
ok(close(1 / np.linalg.norm([2, 0]), 0.5) and close(1 / np.linalg.norm([3, 4]), 0.2), "l15 code margins 0.5 and 0.2")
# frame 2: (3, 3) moved to (2.5, 3)
X7 = X6.copy(); X7[3] = [2.5, 3]
m7 = SVC(kernel="linear", C=1e6).fit(X7, y6)
wf = np.array([0.48, 0.64]); bf = -2.12
ok(np.allclose(m7.coef_[0], wf, atol=1e-3) and close(1 / np.linalg.norm(wf), 1.25) and close(-wf[0] / wf[1], -0.75) and close(-bf / wf[1], 3.3125), "l15 moved support vector: slope -0.75, intercept 3.3125, street 2.5")
lv.expect("l15", "screens[1].canvas.controls[0].frames[2].caption", 2.5)
# quiz: decision value 2 is 2.83 from the line; mislabelled loan slack 2
ok(close(2 / np.linalg.norm(w), 2 * math.sqrt(2)), "l15 q1 distance 2.83")
lv.expect("l15", "quiz[0].widget.answer", 2.83)
X8 = np.vstack([X6, [1.5, 0.5]]); y8 = np.r_[y6, 1]
m8 = SVC(kernel="linear", C=1).fit(X8, y8)
ok(np.allclose(m8.coef_[0], w, atol=2e-3) and close(1 - 1 * (w @ [1.5, 0.5] + b), 2.0), "l15 q3 soft margin keeps x1 + x2 = 4, slack 2")
ok(close(40 / 0.3, 133.33, 0.01), "l15 q4 sd ratio about 133")
lv.expect("l15", "quiz[3].explain.text", 133)


def svm_report(Xa, ya, Xb, yb, C, gamma=None):
    m = SVC(kernel="linear", C=C) if gamma is None else SVC(kernel="rbf", C=C, gamma=gamma)
    m.fit(Xa, ya)
    rep = (len(m.support_), round(m.score(Xa, ya), 4), round(m.score(Xb, yb), 4))
    ok(close(rep[2], round(acc_by_hand(m, Xb, yb), 4)), f"l15 score equals hand count C={C} gamma={gamma}")
    return rep, m


Xs, ys = make_street(200, 4); Xs2, ys2 = make_street(200, 5)
for C, want, width in [(0.01, (94, 0.965, 0.975), 2.78), (1, (24, 0.965, 0.965), 1.07), (100, (21, 0.97, 0.95), 0.80)]:
    rep, m = svm_report(Xs, ys, Xs2, ys2, C)
    ok(rep == want and close(round(2 / np.linalg.norm(m.coef_[0]), 2), width), f"l15 street C={C}: {want}, width {width}")
    lv.expect("l15", "screens[4].canvas.params.rows", want[0])
    lv.expect("l15", "screens[4].canvas.params.rows", width, fmt="%.2f" % width)
    lv.expect("l15", "screens[6].widget.tests", want[2])
Xr, yr = make_rings(300, 7); Xr2, yr2 = make_rings(300, 8)
rep, _ = svm_report(Xr, yr, Xr2, yr2, 1)
ok(rep == (298, 0.66, 0.65), "l15 rings linear 0.65 with 298 support vectors")
lr = LogisticRegression().fit(Xr, yr)
ok(close(round(lr.score(Xr2, yr2), 4), 0.5067) and close(round(acc_by_hand(lr, Xr2, yr2), 4), 0.5067), "l15 rings logistic 0.5067")
lv.expect("l15", "screens[5].prose", 0.5067)
fe = lambda X: np.c_[X, (X ** 2).sum(1)]
rep, mf = svm_report(fe(Xr), yr, fe(Xr2), yr2, 1)
ok(close(rep[2], 0.9733), "l15 rings with x1^2 + x2^2: 0.9733")
lv.expect("l15", "screens[5].prose", 0.9733)
wv, bv = mf.coef_[0], mf.intercept_[0]
cx, cy = -wv[0] / (2 * wv[2]), -wv[1] / (2 * wv[2])
r2c = cx ** 2 + cy ** 2 - bv / wv[2]
ok(close(wv[2], -2.26, 0.005) and close(bv, 4.50, 0.005) and close(r2c, 1.99, 0.01) and close(math.sqrt(r2c), 1.41, 0.005), "l15 feature boundary: circle radius 1.41 (r^2 1.99)")
lv.expect("l15", "screens[5].explain.text", 1.41)
GAM = {0.01: (300, 0.6333, 0.61), 0.1: (76, 0.99, 0.97), 1: (44, 0.9967, 0.98), 10: (177, 0.9967, 0.97), 100: (289, 1.0, 0.87), 1000: (300, 1.0, 0.64)}
for g, want in GAM.items():
    rep, _ = svm_report(Xr, yr, Xr2, yr2, 1, g)
    ok(rep == want, f"l15 rings rbf gamma={g}: {want}")
    lv.expect("l15", "screens[7].canvas.state.values", want[2])
lv.expect("l15", "screens[6].explain.text", 44)
lv.expect("l15", "screens[7].widget.options", 0.64)
# pick_gamma: validation on the last 100 training rows, ties to the smaller gamma
VAL = {}
for C in [0.1, 1, 10, 100]:
    VAL[C] = [round(SVC(kernel="rbf", C=C, gamma=g).fit(Xr[:200], yr[:200]).score(Xr[200:], yr[200:]), 4) for g in [0.01, 0.1, 1, 10]]
ok(VAL[1] == [0.7, 0.99, 1.0, 0.99] and VAL[100] == [1.0, 1.0, 0.98, 0.98] and VAL[10] == [0.95, 1.0, 0.99, 0.98] and VAL[0.1] == [0.7, 0.98, 0.99, 0.94], "l15 validation grid")
ok(all(max(VAL[C][1], VAL[C][2]) >= 0.98 for C in VAL), "l15 every C validates at 0.98 or better with gamma 0.1 or 1")
# unscaled warning: column x100
Xu, Xu2 = Xs.copy(), Xs2.copy(); Xu[:, 1] *= 100; Xu2[:, 1] *= 100
ok(close(round(SVC(kernel="rbf", C=1, gamma=1).fit(Xu, ys).score(Xu2, ys2), 4), 0.795) and close(round(SVC(kernel="rbf", C=1, gamma=1).fit(Xs, ys).score(Xs2, ys2), 4), 0.965), "l15 unscaled street 0.795 against 0.965")
lv.expect("l15", "quiz[3].explain.text", 0.795)
ok(close((0.98 - 0.9733) * 300, 2, 0.01), "l15 transfer: 2 trades in 300")

# ================================================================ l16 clustering
v = np.array([10, 12, 14, 30, 32, 40.])


def hand_kmeans(c):
    c = np.array(c, float); hist = []
    while True:
        lab = np.argmin(np.abs(v[:, None] - c[None]), 1)
        nc = np.array([v[lab == j].mean() if (lab == j).any() else c[j] for j in range(len(c))])
        hist.append(nc)
        if np.allclose(nc, c):
            return lab, nc, float(((v - nc[lab]) ** 2).sum()), hist
        c = nc


lab2, c2, in2, h2 = hand_kmeans([10, 12])
ok(np.allclose(h2[0], [10, 25.6]) and np.allclose(c2, [12, 34]) and in2 == 64, "l16 hand run: 10 and 25.6, then 12 and 34, inertia 64")
ok(F(12 + 14 + 30 + 32 + 40, 5) == F(128, 5) == F(256, 10), "l16 25.6 = 128/5 exactly")
lv.expect("l16", "screens[0].widget.rows[7][2].answer", 25.6)
lv.expect("l16", "screens[1].widget.answers", 34)
lv.expect("l16", "screens[2].widget.answer", 64)
_, c3, in3, _ = hand_kmeans([10, 12, 14])
ok(np.allclose(c3, [10, 13, 34]) and in3 == 58, "l16 bad start stops at 58")
lv.expect("l16", "screens[3].widget.answer", 58)
INER = {}
for k in [1, 2, 3, 4]:
    INER[k] = KMeans(k, n_init=10, random_state=0).fit(v[:, None]).inertia_
ok([round(INER[k], 6) for k in [1, 2, 3, 4]] == [790, 64, 10, 4], "l16 best inertias 790, 64, 10, 4 (KMeans)")
ok(float(((v - v.mean()) ** 2).sum()) == 790 and (4 + 0 + 4) + 0 + (1 + 1) == 10 and (1 + 1) + 0 + (1 + 1) + 0 == 4, "l16 inertias by hand: 790, 10 (12; 31; 40), 4")
lv.expect("l16", "screens[2].explain.text", 790)
ok(round(KMeans(3, n_init=1, random_state=1).fit(v[:, None]).inertia_, 6) == 58, "l16 one start can stop at 58 (random_state=1)")
Xst, lab_true = make_stocks(11)
ok(close(Xst.std(0)[0], 0.336, 0.0005) and close(Xst.std(0)[1], 13.04, 0.005), "l16 sds 0.336 and 13.04")
lv.expect("l16", "screens[5].widget.options", 13.04)


def purity(lab, pred):
    return sum(np.bincount(lab[pred == j]).max() for j in set(pred)) / len(lab)


praw = KMeans(3, n_init=10, random_state=0).fit_predict(Xst)
Zst = StandardScaler().fit_transform(Xst)
psc = KMeans(3, n_init=10, random_state=0).fit_predict(Zst)
ok(close(purity(lab_true, praw), 0.75) and close(purity(lab_true, psc), 1.0), "l16 purity 0.75 raw, 1.0 scaled")
lv.expect("l16", "screens[5].question", 75)
SC = [round(KMeans(k, n_init=10, random_state=0).fit(Zst).inertia_, 2) for k in range(1, 8)]
ok(SC == [120.0, 62.39, 14.16, 11.24, 9.79, 7.92, 6.47], "l16 scaled inertias 120 ... 6.47")
ok(close(((Zst - Zst.mean(0)) ** 2).sum(), 120, 1e-9), "l16 k = 1 inertia is n times p = 120 after scaling")
for val in [62.39, 14.16, 11.24]:
    lv.expect("l16", "screens[8].explain.text", val)
sizes4 = sorted(np.bincount(KMeans(4, n_init=10, random_state=0).fit(Zst).labels_).tolist())
ok(sizes4 == [6, 14, 20, 20], "l16 k = 4 sizes 6, 14, 20, 20")
Zn = StandardScaler().fit_transform(make_noise(300, 4)[0])
NI = [round(KMeans(k, n_init=10, random_state=0).fit(Zn).inertia_, 1) for k in range(1, 8)]
ok(NI == [600.0, 402.4, 277.8, 216.2, 179.0, 148.9, 128.9], "l16 noise inertias")
drops = [round(NI[i] - NI[i + 1]) for i in range(6)]
ok(drops == [198, 125, 62, 37, 30, 20], "l16 noise drops 198, 125, 62, 37, 30, 20")
lv.expect("l16", "quiz[0].explain.text", 198)
mn3 = KMeans(3, n_init=10, random_state=0).fit(Zn)
ok(round(mn3.inertia_, 2) == 277.77 and sorted(np.bincount(mn3.labels_).tolist()) == [88, 98, 114], "l16 noise k = 3: 277.77, sizes 88, 98, 114")
lv.expect("l16", "screens[8].explain.text", 114)
D5 = np.array([[0, .2, .6, .7, .8], [.2, 0, .65, .75, .85], [.6, .65, 0, .3, .9], [.7, .75, .3, 0, .95], [.8, .85, .9, .95, 0]])
H = {m: [round(h, 4) for h in linkage(squareform(D5), m)[:, 2]] for m in ["single", "complete", "average"]}
ok(H == {"single": [0.2, 0.3, 0.6, 0.8], "complete": [0.2, 0.3, 0.75, 0.95], "average": [0.2, 0.3, 0.675, 0.875]}, "l16 linkage heights")
# route B by hand: cross distances between {B1,B2} and {M1,M2}
cross = [0.6, 0.7, 0.65, 0.75]; ucross = [0.8, 0.85, 0.9, 0.95]
ok(min(cross) == 0.6 and max(cross) == 0.75 and close(sum(cross) / 4, 0.675) and min(ucross) == 0.8 and max(ucross) == 0.95 and close(sum(ucross) / 4, 0.875), "l16 linkages by hand")
for val in [0.6, 0.75, 0.675, 0.8, 0.95, 0.875]:
    lv.expect("l16", "screens[6].explain.text", val)
cut_s = len(set(fcluster(linkage(squareform(D5), "single"), 0.70, "distance")))
cut_c = len(set(fcluster(linkage(squareform(D5), "complete"), 0.70, "distance")))
ok(cut_s == 2 and cut_c == 3, "l16 cut at 0.70: 2 single, 3 complete")
lv.expect("l16", "screens[7].widget.answer", 3)
ok(math.comb(60, 2) == 1770 and 3 * math.comb(20, 2) == 570 and 3 * 20 * 19 == 1140 and math.comb(20, 2) == 190, "l16 pairs 1770 and 570")
lv.expect("l16", "screens[10].widget.answer", 570)
lv.expect("l16", "screens[10].explain.text", 1770)
ok(16 + 4 + 36 == 56 and close(56 / 3, 18.67, 0.005), "l16 q4 56")

# ================================================================ l17 network
def relu(x): return np.maximum(0, x)


def fwd(X, W1, b1, W2, b2):
    z = relu(np.asarray(X, float) @ np.asarray(W1, float).T + b1) @ np.asarray(W2, float) + b2
    return z, 1 / (1 + np.exp(-z))


z4, p4 = fwd([[0, 0], [1, 0], [0, 1], [1, 1]], [[1, 1], [1, 1]], [0, -1], [4, -8], -2)
ok(z4.tolist() == [-2, 2, 2, -2] and np.round(p4, 4).tolist() == [0.1192, 0.8808, 0.8808, 0.1192], "l17 corners z and p")
ok(close(1 / (1 + math.e ** 2), 0.1192, 5e-5), "l17 sigma(-2) by hand")
z5, p5 = fwd([[0.5, 0.8]], [[1, 1], [1, 1]], [0, -1], [4, -8], -2)
ok(close(z5[0], 0.8) and close(round(p5[0], 2), 0.69) and close(4 * 1.3 - 8 * 0.3 - 2, 0.8), "l17 (0.5, 0.8): z 0.8, p 0.69")
lv.expect("l17", "screens[2].widget.answer", 0.69)
ok(close(round(1 / (1 + math.exp(-3.2)), 2), 0.96), "l17 wrong: dropping h2 gives 0.96")
npar = lambda s: sum(a * b + b for a, b in zip(s[:-1], s[1:]))
ok(npar([2, 2, 1]) == 9 == 2 * 2 + 2 + 2 + 1 and npar([2, 8, 1]) == 33 == 16 + 8 + 8 + 1 and npar([10, 16, 16, 1]) == 465 == 176 + 272 + 17, "l17 parameter counts 9, 33, 465")
lv.expect("l17", "screens[3].widget.answer", 33)
lv.expect("l17", "screens[3].explain.text", 465)
ok(close(1 / (1 + math.exp(-0.5)), 0.6225, 5e-5), "l17 dead-unit network p = 0.6225")


def gd(w1, w2, x, y, lr):
    h = max(0, w1 * x); err = w2 * h - y
    g2 = err * h; g1 = err * w2 * (x if w1 * x > 0 else 0)
    w1, w2 = w1 - lr * g1, w2 - lr * g2
    return w1, w2, 0.5 * (w2 * max(0, w1 * x) - y) ** 2, g1, g2


a = gd(0.5, 2, 2, 3, 0.1); bstep = gd(0.5, 2, 2, 3, 0.5)
ok(close(a[0], 0.9) and close(a[1], 2.1) and close(a[2], 0.3042) and a[3] == -4 and a[4] == -1, "l17 step 0.1: 0.9, 2.1, loss 0.3042; slopes -4 and -1")
ok(close(bstep[0], 2.5) and close(bstep[1], 2.5) and close(bstep[2], 45.125), "l17 step 0.5: 2.5, 2.5, loss 45.125")
# route B: exact fractions
ok(F(1, 2) * (F(21, 10) * F(9, 10) * 2 - 3) ** 2 == F(3042, 10000) and F(1, 2) * (F(5, 2) * F(5, 2) * 2 - 3) ** 2 == F(45125, 1000), "l17 losses exactly")
lv.expect("l17", "screens[6].widget.answer", 0.3042)
lv.expect("l17", "screens[6].explain.text", 45.125)
ok(close(gd(-0.5, 2, 2, 3, 0.1)[2], 4.5) and close(gd(1, 1, 1, 0.5, 0.1)[2], 0.081, 1e-4), "l17 dead unit 4.5, fresh case 0.081")
ok(np.allclose(np.array([3, -1]) @ np.array([[1, 2], [0, 1]]), [3, 5]), "l17 q2 collapse v = (3, 5)")
Xr, yr = make_rings(300, 7); Xr2, yr2 = make_rings(300, 8)
PYO_W = {1: 0.6567, 2: 0.6467, 3: 0.82, 8: 0.97, 64: 0.97}
for hdn, pv in PYO_W.items():
    m = MLPClassifier(hidden_layer_sizes=(hdn,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500).fit(Xr, yr)
    ok(abs(m.score(Xr2, yr2) - pv) <= 0.01, f"l17 width {hdn}: CPython within 0.01 of Pyodide {pv}")
    lv.expect("l17", "screens[8].canvas.state.values", pv)
PYO_S = {0: 0.97, 1: 0.9667, 2: 0.96}
for s, pv in PYO_S.items():
    m = MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=s, max_iter=500).fit(Xr, yr)
    ok(abs(m.score(Xr2, yr2) - pv) <= 0.01 and 0.93 <= m.score(Xr2, yr2) < 0.99, f"l17 seed {s}: within 0.01 of {pv} and inside the test band")
    lv.expect("l17", "screens[8].explain.text", pv)
Xn, yn = make_noise(300, 4); Xn2, yn2 = make_noise(300, 5)
ok(close(yn2.mean(), 0.55), "l17 noise base rate 0.55 on test rows")
PYO_N = {0: (0.5833, 0.5567), 1: (0.6033, 0.5), 2: (0.65, 0.4967)}
for s, (ptr, pte) in PYO_N.items():
    m = MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=s, max_iter=500).fit(Xn, yn)
    ok(abs(m.score(Xn, yn) - ptr) <= 0.01 and abs(m.score(Xn2, yn2) - pte) <= 0.015 and m.score(Xn, yn) > m.score(Xn2, yn2), f"l17 noise seed {s}: CPython near Pyodide ({ptr}, {pte}), train above test")
    lv.expect("l17", "screens[9].canvas.params.rows", pte, fmt="%.4f" % pte)
m64 = MLPClassifier(hidden_layer_sizes=(64,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500).fit(Xn, yn)
ok(m64.score(Xn, yn) > 0.75 and m64.score(Xn2, yn2) < 0.53, "l17 noise, 64 units: training rises, test near 0.5")
ok(close(2e6 / 0.01, 2e8), "l17 q4 slope ratio 2e8")

# ================================================================ l18 splines
x, y = make_impact(200, 21); x2, y2 = make_impact(200, 22); X1, X2 = x[:, None], x2[:, None]
line = LinearRegression().fit(X1, y)
A = np.c_[np.ones(len(x)), x]; cf = np.linalg.lstsq(A, y, rcond=None)[0]
ok(np.allclose([line.intercept_, line.coef_[0]], cf) and close(round(cf[0] + cf[1], 2), 18.59) and close(round(line.score(X2, y2), 4), 0.9088), "l18 line 18.59 at 1%, test R2 0.9088 (sklearn and lstsq)")
lv.expect("l18", "screens[0].widget.answer", 18.59)
poly = make_pipeline(PolynomialFeatures(12), StandardScaler(), LinearRegression()).fit(X1, y)
ok(close(round(poly.score(X2, y2), 4), 0.9381) and close(round(poly.predict([[55]])[0], 2), 216.23) and close(round(10 * math.sqrt(55), 2), 74.16), "l18 degree 12: 0.9381, 216.23 at 55, truth 74.16")
lv.expect("l18", "screens[0].explain.text", 216.23)
f = lambda t: 2 + 3 * t - 2 * max(t - 4, 0)
ok((f(2), f(6), f(10)) == (8, 16, 20), "l18 hinge 8, 16, 20")
lv.expect("l18", "screens[1].widget.answer", 16)


def ls_spline(xx, yy, knots):
    Aa = np.column_stack([np.ones(len(xx)), xx] + [np.maximum(0, xx - c) for c in knots])
    return np.linalg.lstsq(Aa, yy, rcond=None)[0]


c520 = ls_spline(x, y, [5, 20])
ok(np.round(c520, 3).tolist() == [5.789, 3.822, -2.459, -0.488], "l18 knots 5, 20 coefficients")
ok(close(3.822 - 2.459 - 0.488, 0.875) and close(3.822 - 2.459, 1.363), "l18 slopes 1.363 and 0.875")
lv.expect("l18", "screens[2].widget.answer", 0.875)
for knots, te, f1 in [([], 0.9088, 18.59), ([5], 0.9289, 9.55), ([5, 20], 0.9426, 9.61), ([10, 30], 0.9428, 10.10)]:
    cc = ls_spline(x, y, knots)
    pred = lambda t: np.column_stack([np.ones(len(t)), t] + [np.maximum(0, t - c) for c in knots]) @ cc
    r2 = 1 - ((y2 - pred(x2)) ** 2).sum() / ((y2 - y2.mean()) ** 2).sum()
    ok(close(round(r2, 4), te) and close(round(pred(np.array([1.0]))[0], 2), f1), f"l18 linear spline {knots}: test R2 {te}, {f1} at 1%")
    lv.expect("l18", "screens[2].canvas.derive.caption", te)
ok(5 + 3 - 1 == 7 == 3 + 4 and 2 * 7 == 14 and 4 + 4 == 8 and 2 + 3 == 5 and 3 * (4 + 3 - 1) == 18, "l18 counts 7, 14, 8, 5, 18")
SPL = {2: (0.9575, 0.9424), 3: (0.9586, 0.9439), 5: (0.9598, 0.9417), 10: (0.9613, 0.938), 40: (0.9652, 0.9347)}
for k, (tr, te) in SPL.items():
    m = make_pipeline(SplineTransformer(n_knots=k, degree=3), LinearRegression()).fit(X1, y)
    ok((round(m.score(X1, y), 4), round(m.score(X2, y2), 4)) == (tr, te) and m[0].transform(X1).shape[1] == k + 2, f"l18 n_knots={k}: {tr}, {te}, {k + 2} columns")
    lv.expect("l18", "screens[5].canvas.state.values", te)
mv = {k: round(make_pipeline(SplineTransformer(n_knots=k, degree=3), LinearRegression()).fit(X1[:150], y[:150]).score(X1[150:], y[150:]), 4) for k in [2, 3, 5, 10, 40]}
ok(max(mv, key=lambda k: (mv[k], -k)) == 5 and mv[5] == 0.9495 and mv[3] == 0.9494, "l18 validation picks 5 knots (0.9495 against 0.9494)")
lv.expect("l18", "screens[5].explain.text", 0.9495)
me = make_pipeline(SplineTransformer(n_knots=5, degree=3, extrapolation="linear"), LinearRegression()).fit(X1, y)
ok(close(round(me.predict([[55]])[0], 2), 85.13), "l18 linear tail 85.13 at 55")
lv.expect("l18", "screens[5].explain.text", 85.13)
Xa, ya = make_additive(300, 31); Xa2, ya2 = make_additive(300, 32)
am = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(Xa, ya)
ok(close(round(LinearRegression().fit(Xa, ya).score(Xa2, ya2), 4), 0.3744) and close(round(am.score(Xa2, ya2), 4), 0.9101) and am[0].transform(Xa).shape[1] == 14, "l18 additive 0.3744 against 0.9101, 14 columns")
lv.expect("l18", "screens[6].prose", 0.9101)
Xi, yi = make_additive(300, 31, 1.0); Xi2, yi2 = make_additive(300, 32, 1.0)
INT = {5: 0.3292, 10: 0.2373, 20: 0.172}
for k, val in INT.items():
    ok(close(round(make_pipeline(SplineTransformer(n_knots=k, degree=3), LinearRegression()).fit(Xi, yi).score(Xi2, yi2), 4), val), f"l18 interaction, {k} knots: {val}")
    lv.expect("l18", "screens[8].canvas.params.rows", val, fmt="%.4f" % val)
ok(close(round(LinearRegression().fit(Xi, yi).score(Xi2, yi2), 4), 0.1213), "l18 interaction linear 0.1213")
m5 = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(X1, y)
sg = np.arange(0.5, 10, 0.001)
sav = m5.predict(sg[:, None]) - m5.predict(sg[:, None] / 2)
root = sg[np.argmax(sav > 5)]
ok(close(round(root, 1), 3.0) and close(root, 3.02, 0.01), "l18 splitting saves 5 bp above 3.0% (grid)")
# route B: bisection on the same fitted spline
lo_, hi_ = 2.0, 5.0
for _ in range(60):
    mid = (lo_ + hi_) / 2
    if m5.predict([[mid]])[0] - m5.predict([[mid / 2]])[0] > 5:
        hi_ = mid
    else:
        lo_ = mid
ok(close(lo_, root, 0.002), "l18 bisection agrees")
law = (5 / (10 * (1 - 1 / math.sqrt(2)))) ** 2
ok(close(round(law, 2), 2.91) and close(5 / 0.585, 8.55, 0.01) and close(1.17 / 2, 0.585), "l18 law 2.91; a line reaches 5 bp only at 8.5")
lv.expect("l18", "screens[10].explain.text", 2.91)
ok(close(round(m5.predict([[2]])[0] - m5.predict([[1]])[0], 2), 3.54) and close(round(m5.predict([[5]])[0] - m5.predict([[2.5]])[0], 2), 7.26), "l18 savings 3.54 at 2, 7.26 at 5")
mr = make_pipeline(SplineTransformer(n_knots=40, degree=3), Ridge(alpha=1)).fit(X1, y)
ok(close(round(mr.score(X2, y2), 4), 0.8868), "l18 q3 ridge alpha 1 on 40 knots: 0.8868")
lv.expect("l18", "quiz[2].explain.text", 0.8868)
ok(close(216.23 - 74.16, 142.07) and close(216.23 - 85.13, 131.1), "l18 q2 gaps 142 and 131 bp")

# ================================================================ l19 which learner
LEARN = {
    "logistic": lambda: make_pipeline(StandardScaler(), LogisticRegression()),
    "knn": lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(15)),
    "svm": lambda: make_pipeline(StandardScaler(), SVC(C=1, gamma="scale")),
    "net": lambda: make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=0, max_iter=500)),
    "additive": lambda: make_pipeline(StandardScaler(), SplineTransformer(n_knots=5), LogisticRegression(max_iter=2000)),
}
PROB = {"street": (make_street(300, 4), make_street(300, 5)), "rings": (make_rings(300, 7), make_rings(300, 8)),
        "quadrants": (make_quadrants(300, 3), make_quadrants(300, 4)), "wide": (make_wide(60, 4), make_wide(300, 5)),
        "noise": (make_noise(300, 4), make_noise(300, 5))}
TABLE = {"street": [0.9633, 0.9633, 0.9633, 0.9567, 0.96], "rings": [0.5067, 0.9767, 0.9767, 0.9733, 0.98],
         "quadrants": [0.4767, 0.86, 0.8567, 0.8467, 0.4567], "wide": [0.9233, 0.89, 0.92, 0.9067, 0.9167],
         "noise": [0.5567, 0.4967, 0.5567, 0.5367, 0.5333]}
for p, ((Xa_, ya_), (Xb_, yb_)) in PROB.items():
    for j, name in enumerate(LEARN):
        m = LEARN[name]().fit(Xa_, ya_)
        got = round(m.score(Xb_, yb_), 4)
        want = TABLE[p][j]
        tol = 0.03 if name == "net" else 0
        ok(close(got, want, tol + 1e-12) and close(got, round(acc_by_hand(m, Xb_, yb_), 4)), f"l19 {p} {name}: {want} (CPython {got})")
        lv.expect("l19", "screens[5].canvas.params.rows", want, fmt="%.4f" % want)
ok(close(PROB["noise"][1][1].mean(), 0.55), "l19 noise test base rate 0.55")
t = (0.5567 - 0.55) / math.sqrt(0.55 * 0.45 / 300)
ok(close(round(t, 2), 0.23) and close(math.sqrt(0.55 * 0.45 / 300), 0.0287, 5e-5) and close((0.5567 - 0.5) / math.sqrt(0.25 / 300), 1.96, 0.01), "l19 t 0.23 (0.0287); against a coin 1.96 to 1.97")
lv.expect("l19", "screens[4].widget.answer", 0.23)
SEEDS = {(9, 10): [0.48, 0.98, 0.98, 0.9733, 0.9833], (11, 12): [0.5167, 0.9633, 0.9667, 0.9567, 0.9567]}
for (s1, s2), want in SEEDS.items():
    (Xa_, ya_), (Xb_, yb_) = make_rings(300, s1), make_rings(300, s2)
    for j, name in enumerate(LEARN):
        if name == "logistic":
            continue
        got = round(LEARN[name]().fit(Xa_, ya_).score(Xb_, yb_), 4)
        ok(close(got, want[j], 0.01 if name == "net" else 0), f"l19 rings seeds {s1},{s2} {name}: {want[j]}")
lv.expect("l19", "quiz[0].prose", 0.9833)
ORDER = ["logistic", "additive", "knn", "svm", "net"]
for p, nval, want in [("street", 100, ("logistic", 0.9633)), ("rings", 100, ("additive", 0.98)), ("quadrants", 100, ("svm", 0.8567)), ("wide", 20, ("logistic", 0.9233)), ("noise", 100, ("knn", 0.4967))]:
    (Xa_, ya_), (Xb_, yb_) = PROB[p]
    vals = [LEARN[n]().fit(Xa_[:-nval], ya_[:-nval]).score(Xa_[-nval:], ya_[-nval:]) for n in ORDER]
    win = ORDER[vals.index(max(vals))]
    ok(win == want[0] and close(round(LEARN[win]().fit(Xa_, ya_).score(Xb_, yb_), 4), want[1]), f"l19 choose_on_validation {p}: {want}")
ok(25 * 64 + 64 + 64 + 1 == 1729 and 20 + 1 == 21 and round(750 / 20) == 38 and 750 // 20 == 37, "l19 1,700 parameters, 21, about 37 rows per feature")

# ================================================================ review and homework
ok(close(2 / 5, 0.4), "review street 0.4")
lv.expect("review", "items[0].widget.answer", 0.4)
P5 = np.array([[0, 0], [2, 0], [0, 4], [10, 10], [12, 10]], float)
C0 = np.array([[0, 0], [10, 10]], float)
labs = ((P5[:, None] - C0[None]) ** 2).sum(2).argmin(1)
C1 = np.array([P5[labs == j].mean(0) for j in range(2)])
ine = ((P5 - C1[labs]) ** 2).sum()
ok(close(ine, F(120, 9) + 2, 1e-12) and close(round(ine, 2), 15.33) and ((P5 - C0[labs]) ** 2).sum() == 24, "review k-means 15.33 (24 before)")
lv.expect("review", "items[1].widget.answer", 15.33)
zr, pr = fwd([[1, 3]], [[2, -1], [0, 1]], [0, -1], [3, 2], -4)
ok(close(zr[0], 0) and close(pr[0], 0.5) and close(round(1 / (1 + math.exp(3)), 2), 0.05), "review forward p 0.5 (no ReLU 0.05)")
ok(npar([4, 6, 3]) == 51, "review 4-6-3 has 51")
ok(1 + 12 + 12 - 4 == 21, "review spline f(6) 21")
se = math.sqrt(0.53 * 0.47 / 400)
ok(close(round(0.04 / se, 2), 1.6) and close(round(0.07 / 0.025, 2), 2.8) and close(round(0.04 / (0.53 * 0.47 / 400), 2), 64.23), "review t 1.60, coin 2.8")
lv.expect("review", "items[6].widget.answer", 1.6)
D4 = np.array([[0, .1, .5, .9], [.1, 0, .6, .7], [.5, .6, 0, .4], [.9, .7, .4, 0]])
ok([round(h, 4) for h in linkage(squareform(D4), "average")[:, 2]] == [0.1, 0.4, 0.675], "review average linkage 0.675")
lv.expect("review", "items[7].widget.answer", 0.675)
Xh = np.array([[1, 2], [2, 1], [0, 0], [4, 5], [5, 4], [6, 6]], float); yh = np.array([0, 0, 0, 1, 1, 1])
mh = SVC(kernel="linear", C=1e6).fit(Xh, yh)
ok(np.allclose(mh.coef_[0], [1 / 3, 1 / 3]) and close(mh.intercept_[0], -2, 1e-6) and close(round(3 / math.sqrt(2), 2), 2.12), "homework margin 2.12 with w = (1/3, 1/3), b = -2")
dh = np.where(yh == 1, 1, -1) * (Xh @ [1 / 3, 1 / 3] - 2)
ok(np.flatnonzero(np.abs(dh - 1) < 1e-9).tolist() == [0, 1, 3, 4], "homework edge points P1, P2, P4, P5")
lv.expect("homework", "items[0].parts[0].widget.answer", 2.12)
zh, ph = fwd([[2, 1]], [[1, -1], [0, 2], [-1, 1]], [0, -1, 0.5], [2, 1, -3], 0.5)
ok(npar([2, 3, 1]) == 13 and close(zh[0], 3.5) and close(round(ph[0], 2), 0.97), "homework 2-3-1: 13 parameters, z 3.5")
lv.expect("homework", "items[2].parts[1].widget.answer", 3.5)
ok(5 * 4 - 3 * 4 == 8 and (4 + 3 - 1) * 3 == 18 and 2 * 64 + 64 + 64 * 5 + 5 == 517, "homework 8, 18, 517")
lv.expect("homework", "items[3].widget.answer", 8)
lv.expect("homework", "items[8].model", 517)
st = SVC(kernel="rbf", C=1, gamma=1).fit(Xr, yr)
hand = [float(st.dual_coef_[0] @ np.exp(-1.0 * ((st.support_vectors_ - p) ** 2).sum(1)) + st.intercept_[0]) for p in ([0, 0], [1.5, 0], [0.3, -2.1])]
ok(np.allclose(hand, st.decision_function([[0, 0], [1.5, 0], [0.3, -2.1]])) and np.round(hand, 6).tolist() == [2.127469, -0.082931, -1.539442], "homework RBF by hand equals decision_function")
ok(close(2 * math.exp(-1) - 1, -0.264241, 1e-6), "homework hand kernel case")

lv.check_wrongs()
lv.report()
