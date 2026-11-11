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

# ================================================================ fix pass (docs/reviews/review-stat-learning-4.md)
# Every value the fix pass wrote, by two routes, tied to its text; each check fails if its fix is reverted.
gone = lambda ref, path, phrase: ok(phrase not in lv.text(ref, path), f"fix pass: {ref} {path} no longer says {phrase!r}")

# l15: the vertical street rests on (2, 0), (3, 3), (3, 5)
X6 = np.array([[1, 1], [0, 1], [2, 0], [3, 3], [4, 3], [3, 5]], float); s6 = np.array([-1, -1, -1, 1, 1, 1])
on = np.flatnonzero(np.abs(s6 * (X6 @ [2, 0] - 5) - 1) < 1e-9)
ok(X6[on].tolist() == [[2, 0], [3, 3], [3, 5]] and [p for p, s in zip(X6.tolist(), s6) if (p[0] == 2 and s < 0) or (p[0] == 3 and s > 0)] == X6[on].tolist(), "l15 s3: x1 = 2.5 scaled rests on (2, 0), (3, 3), (3, 5)")
lv.expect("l15", "screens[3].explain.text", "$(2, 0)$, $(3, 3)$ and $(3, 5)$")
lv.expect("l15", "screens[4].explain.text", "ISLP's $C$ is a budget")
gone("l15", "screens[1].explain.text", "anywhere outside the street")

# l16 s1 'half', s2 'unsq'
ok([(10 + 12) / 2, (25.6 + 34) / 2] == [11.0, 29.8] and F(128, 5) / 2 + 17 == F(298, 10), "l16 s1 halfway from (10, 25.6) to (12, 34) is 11 and 29.8")
lv.expect("l16", "screens[1].widget.wrong", "11, 29.8")
plain = float(np.abs(v - np.array([12, 12, 12, 34, 34, 34])).sum())
ok(plain == 16 == 2 + 0 + 2 + 4 + 2 + 6, "l16 s2 plain distances add to 16")
lv.expect("l16", "screens[2].widget.wrong[0].value", 16)
# l16 s5: more starts lower the raw inertia from 842.33 to 842.15, purity 0.7333 (scikit-learn; then my own Lloyd loop)
km10 = KMeans(3, n_init=10, random_state=0).fit(Xst); km200 = KMeans(3, n_init=200, random_state=0).fit(Xst)
ok(round(km10.inertia_, 2) == 842.33 and round(km200.inertia_, 2) == 842.15 and close(purity(lab_true, km200.labels_), 44 / 60), "l16 s5: 10 starts 842.33, 200 starts 842.15 with purity 0.7333")
_rng = np.random.default_rng(123); _low = []
for _ in range(400):
    cc_ = Xst[_rng.choice(60, 3, replace=False)].astype(float)
    for _i in range(200):
        l_ = ((Xst[:, None] - cc_[None]) ** 2).sum(2).argmin(1)
        nc_ = np.array([Xst[l_ == j].mean(0) if (l_ == j).any() else cc_[j] for j in range(3)])
        if np.allclose(nc_, cc_):
            break
        cc_ = nc_
    _low.append((round(float(((Xst - cc_[l_]) ** 2).sum()), 2), round(purity(lab_true, l_), 4)))
ok(min(_low) == (842.15, 0.7333) and (842.33, 0.75) in _low, "l16 s5: own Lloyd loop, 400 random starts: lowest 842.15 at purity 0.7333; 842.33 at 0.75 is a local stop")
for val in (842.33, 842.15, 73):
    lv.expect("l16", "screens[5].widget.options[2].why", val)
lv.expect("l16", "screens[5].feedback.byKey.c", 73)
gone("l16", "screens[5].widget.options[2].why", "Ten starts found the lowest")
# l16 s4 new test: squared distance against summed absolute gaps
P3 = np.array([[0, 0], [0, 6], [4, 3]], float); C2 = np.array([[0, 5], [3, 3]], float)
eu = ((P3[:, None] - C2[None]) ** 2).sum(2).argmin(1).tolist(); mn = np.abs(P3[:, None] - C2[None]).sum(2).argmin(1).tolist()
ok(eu == [1, 0, 1] and mn == [0, 0, 1] and [25 > 18, 1 < 18, 20 > 1] == [True] * 3 and [5 < 6], "l16 s4 new test: Euclid [1, 0, 1], Manhattan [0, 0, 1]")
lv.expect("l16", "screens[4].widget.tests[9].expect", "[1, 0, 1]")
import json  # noqa: E402
_CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'stat-learning')
ntests = lambda name, i: len(json.load(open(os.path.join(_CONTENT, name + '.json')))['screens'][i]['widget']['tests'])
ok(ntests('l16-groups-nobody-labelled', 4) == 10 and ntests('l17-a-small-network', 8) == 7 and ntests('l19-which-learner', 7) == 6 and ntests('l19-which-learner', 8) == 6,
   "test counts match each `how`: l16 s4 10, l17 s8 7, l19 s7 6, l19 s8 6")
lv.expect("l16", "screens[4].widget.how", 10)

# l17 q2 wrong[]: the wrong order gives -1; the dropped term gives 6
W1_ = np.array([[1, 2], [0, 1]]); w2_ = np.array([3, -1])
ok((W1_ @ w2_).tolist() == [1, -1] and 0 * 3 + 1 * (-1) == -1 and 3 * 2 == 6 and (w2_ @ W1_).tolist() == [3, 5], "l17 q2: W1 w2 = (1, -1); 3 x 2 = 6; w2 W1 = (3, 5)")
lv.expect("l17", "quiz[1].widget.wrong[1].value", -1)
lv.expect("l17", "quiz[1].widget.wrong[2].value", 6)
# l17 s9: CPython against the Pyodide table, in rows of 300; the best Pyodide score is two rows above the base rate
moves = []
for s, (ptr, pte) in PYO_N.items():
    m = MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=s, max_iter=500).fit(Xn, yn)
    moves.append(abs(round(m.score(Xn2, yn2) * 300) - round(pte * 300)))
ok(moves == [3, 4, 0] and max(moves) == 4, f"l17 s9: test scores move by up to four rows in 300 between runtimes ({moves})")
ok(round(0.5567 * 300) - round(0.55 * 300) == 2 and int(yn2.sum()) == 165 and max(pte for _, pte in PYO_N.values()) == 0.5567, "l17 s9: best test score is 167 rows, two above the base rate's 165")
lv.expect("l17", "screens[9].explain.text", "four rows in 300")
lv.expect("l17", "screens[9].widget.options[0].text", "two rows in 300")
gone("l17", "screens[9].explain.text", "third place")
# l17 s0: logistic regression fitted to the four corners scores 0.5 (weights 0 by symmetry), so 0.75 is a ceiling, not its score
X4 = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]); y4 = np.array([0, 1, 1, 0]); lr4 = LogisticRegression().fit(X4, y4)
best4 = max(np.mean(((X4 @ [a, b] + c) > 0) == y4) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1.5, -0.5, 0.5, 1.5))
ok(np.allclose(lr4.coef_, 0) and lr4.score(X4, y4) == 0.5 and best4 == 0.75, "l17 s0: logistic on the corners scores 0.5; the best line scores 0.75")
gone("l17", "screens[0].explain.text", "stuck at the same")
ok(close(Xr.std(0)[0], Xr.std(0)[1], 0.05), "l17 s8: the two ring features are on one scale (sds 1.20 and 1.17)")
# l17 s8 new tests: seed 1 at 3 units reaches the band, seed 0 does not; seed 5 stays under 0.85, the default alpha does not
mlp3 = lambda s, a=0.01: MLPClassifier(hidden_layer_sizes=(3,), solver="lbfgs", alpha=a, random_state=s, max_iter=500).fit(Xr, yr).score(Xr2, yr2)
ok(0.93 <= mlp3(1) < 0.99 and not 0.93 <= mlp3(0) < 0.99, "l17 s8 test 6: 3 units, seed 1 in [0.93, 0.99); seed 0 (seed ignored) is not")
ok(mlp3(5) < 0.85 and not mlp3(5, 1e-4) < 0.85, "l17 s8 test 7: 3 units, seed 5 under 0.85; with the default alpha it is not")
lv.expect("l17", "screens[8].widget.how", 7)
ok(3 + 1 == 4 == npar([3, 1]), "l17 s4: a layer from 3 units to 1 has 4 parameters")

# l18 s3 'interior' 3; q3 ridge on 40 knots
ok(5 - 2 == 3 and 3 + 4 == 7, "l18 s3: 3 interior knots, 7 basis functions")
lv.expect("l18", "screens[3].widget.wrong[3].value", 3)
gridg = np.linspace(0.5, 49.5, 491)[:, None]
u40 = make_pipeline(SplineTransformer(n_knots=40, degree=3), LinearRegression()).fit(X1, y)
rough = lambda m: float((np.diff(m.predict(gridg), 2) ** 2).sum())
big = make_pipeline(SplineTransformer(n_knots=40, degree=3), Ridge(alpha=1e6)).fit(X1, y)
small = make_pipeline(SplineTransformer(n_knots=40, degree=3), Ridge(alpha=1e-3)).fit(X1, y)
ok(rough(mr) < rough(u40) and mr.predict(gridg).std() < 0.85 * u40.predict(gridg).std(), "l18 q3: a ridge penalty of 1 wiggles less (second differences) and is flatter (sd of the fit 12.9 against 15.8)")
ok(np.allclose(big.predict(gridg), y.mean(), atol=0.01) and np.ptp(big.predict(gridg)) < 0.01, "l18 q3: a huge ridge penalty gives a flat line at the mean, not a line in x")
ok(np.abs(small.predict(gridg) - u40.predict(gridg)).max() < 0.1, "l18 q3: a small penalty (0.001) moves the curve by under 0.1 bp")
ok(close(round(mr.predict([[1]])[0], 1), 12.3) and close(round(m5.predict([[1]])[0], 1), 9.8) and close(round(mr.predict([[40]])[0], 1), 61.0) and close(round(m5.predict([[40]])[0], 1), 62.5), "l18 q3: flattened ends, 12.3 against 9.8 at 1% and 61.0 against 62.5 at 40%")
gone("l18", "quiz[2].explain.text", "too smooth")
lv.expect("l18", "quiz[1].explain.text", "natural spline")

# l19 s3: 40 further seed pairs of the wide problem (training seed 100 + 2i, test seed 101 + 2i)
WIDE = np.array([[LEARN[n]().fit(*make_wide(60, 100 + 2 * i)).score(*make_wide(300, 101 + 2 * i)) for n in LEARN] for i in range(40)])
wm = dict(zip(LEARN, WIDE.mean(0)))
last = int((WIDE[:, 1] < np.delete(WIDE, 1, 1).min(1)).sum())
ok(close(round(wm["knn"], 2), 0.86) and last == 35 and int((WIDE[:, 1] < WIDE[:, 0]).sum()) == 40, f"l19 s3: nearest neighbours averages 0.86 and is strictly last in 35 of 40 ({wm['knn']:.4f}, {last})")
ok(all(0.90 < wm[n] < 0.93 for n in LEARN if n != "knn") and wm["additive"] > wm["logistic"], "l19 s3: the other four average between 0.90 and 0.93, and logistic is not the best of them on average")
# second route for the same averages: predictions counted by hand on a fresh loop for the two deterministic ends
_k = np.mean([acc_by_hand(LEARN["knn"]().fit(*make_wide(60, 100 + 2 * i)), *make_wide(300, 101 + 2 * i)) for i in range(40)])
_l = np.mean([acc_by_hand(LEARN["logistic"]().fit(*make_wide(60, 100 + 2 * i)), *make_wide(300, 101 + 2 * i)) for i in range(40)])
ok(close(_k, wm["knn"], 1e-12) and close(_l, wm["logistic"], 1e-12) and close(round(_l, 2), 0.92), "l19 s3: the averages again from predictions counted by hand")
for val in (0.86, 35, 0.90, 0.93):
    lv.expect("l19", "screens[3].explain.text", val)
gone("l19", "screens[3].explain.text", "favour the simplest")
gone("l19", "summary.ideas[1]", "favour the simplest")
ok(TABLE["wide"][3] < TABLE["wide"][0] and TABLE["wide"][3] < TABLE["wide"][2], "l19 s3: the network's 0.9067 is behind logistic regression and the SVM")
gone("l19", "screens[3].widget.options[2].why", "both linear-boundary")
gone("l19", "screens[5].prose", "Each score is 1 minus a test error")
# l19 s7: fit() starts again, so a reused object scores the same; a kept reference is overwritten; the new test counts builds
same = True
for n in ("logistic", "knn", "svm", "additive"):
    one = LEARN[n]()
    for (Xa_, ya_), (Xb_, yb_) in PROB.values():
        same = same and one.fit(Xa_, ya_).score(Xb_, yb_) == LEARN[n]().fit(Xa_, ya_).score(Xb_, yb_)
one = LEARN["logistic"](); kept = {p: one.fit(*PROB[p][0]) for p in ("street", "rings")}
ok(same and kept["street"] is kept["rings"] and kept["street"].score(*PROB["street"][1]) < 0.5 < LEARN["logistic"]().fit(*PROB["street"][0]).score(*PROB["street"][1]),
   "l19 s7: a reused object scores the same in every cell, and a kept fitted model is overwritten by the next fit")
gone("l19", "screens[7].explain.text", "carry state")
built = []


def counted():
    built.append(1)
    return LEARN["logistic"]()


for p in ("street", "rings"):
    counted().fit(*PROB[p][0])
ok(len(built) == 2 == 2 * 1, "l19 s7 new test: one build per cell, 2 cells")
lv.expect("l19", "screens[7].widget.tests[5].expect", "2")
lv.expect("l19", "screens[7].widget.how", 6)
# l19 s8 new test: a learner that memorises; honest validation keeps logistic, validating on seen rows picks knn1
(Xa_, ya_), (Xb_, yb_) = PROB["street"]
knn1 = lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(1))
hon = (LEARN["logistic"]().fit(Xa_[:-100], ya_[:-100]).score(Xa_[-100:], ya_[-100:]), knn1().fit(Xa_[:-100], ya_[:-100]).score(Xa_[-100:], ya_[-100:]))
leak = (LEARN["logistic"]().fit(Xa_, ya_).score(Xa_[-100:], ya_[-100:]), knn1().fit(Xa_, ya_).score(Xa_[-100:], ya_[-100:]))
ok(close(hon[0], 0.97) and close(hon[1], 0.96) and close(leak[1], 1.0) and leak[1] > leak[0] and close(round(knn1().fit(Xa_, ya_).score(Xb_, yb_), 4), 0.93)
   and close(round(acc_by_hand(LEARN["logistic"]().fit(Xa_, ya_), Xb_, yb_), 4), 0.9633), "l19 s8 new test: honest ('logistic', 0.9633); on seen rows 1-NN scores 1.0 and the answer becomes ('knn1', 0.93)")
lv.expect("l19", "screens[8].widget.tests[5].expect", "['logistic', 0.9633]")
lv.expect("l19", "screens[8].widget.how", 6)

# review r-few-rows: 25 features, 10 knots each
ok(SplineTransformer(n_knots=10).fit_transform(np.random.default_rng(0).normal(size=(80, 25))).shape == (80, 300) and 25 * (10 + 3 - 1) == 300, "review r-few-rows: 300 spline columns")
lv.expect("review", "items[8].widget.options[3].why", 300)
# homework h-pick-learner (new item, index 9)
se_h = math.sqrt(0.56 * 0.44 / 400)
val_h = [0.61, 0.61, 0.60, 0.59, 0.58]; test_h = [0.59, 0.60, 0.62, 0.58, 0.61]
pick = val_h.index(max(val_h))
ok(pick == 0 and close(round((test_h[pick] - 0.56) / se_h, 2), 1.21) and close(float(F(3, 100) ** 2 / (F(56, 100) * F(44, 100) / 400)) ** 0.5, 0.03 / se_h, 1e-12) and close(round(se_h, 4), 0.0248), "homework h-pick-learner: t 1.21 (se 0.0248)")
ok([round((max(test_h) - 0.56) / se_h, 2), round((test_h[1] - 0.56) / se_h, 2), round((0.59 - 0.5) / math.sqrt(0.25 / 400), 2), round((0.61 - 0.56) / se_h, 2)] == [2.42, 1.61, 3.6, 2.01], "homework h-pick-learner slips 2.42, 1.61, 3.6, 2.01")
lv.expect("homework", "items[9].widget.answer", 1.21)
for j, val in enumerate([2.42, 1.61, 3.6, 2.01]):
    lv.expect("homework", f"items[9].widget.wrong[{j}].value", val)
lv.expect("homework", "items[9].explain.text", 0.0248)
lv.expect("homework", "items[6].prose", "each round is one assignment and the update that follows it")

lv.check_wrongs()
lv.report()
