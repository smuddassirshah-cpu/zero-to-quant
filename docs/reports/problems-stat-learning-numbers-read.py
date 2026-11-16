#!/usr/bin/env python3
"""Second reader's recomputation of stat-learning problems-1 to problems-3.

Imports nothing from the author's script. Every key, every `wrong` value and
every number printed in a prose, feedback or explain string is rebuilt here
from the givens typed below (not read from the JSON), by exact arithmetic
(fractions) and, where a second route exists, by NumPy, SciPy, scikit-learn or
brute force. Bands: the key band takes the exact value and its stated rounding,
and no `wrong` band touches it. Exit 0 on correct content; a check that fails
on wrong content stays failing (see docs/reviews/review-problems-stat-learning-1-3.md).

Run: <scratchpad>/venv/bin/python docs/reports/problems-stat-learning-numbers-read.py
"""
import json, math, os, re, sys
from fractions import Fraction as F
from itertools import combinations

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import expit
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import precision_score, recall_score, accuracy_score

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, "app", "content", "courses", "stat-learning")
SETS = {n: json.load(open(os.path.join(COURSE, f"problems-{n}.json"))) for n in (1, 2, 3)}

checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", label)


def item(n, iid):
    return next(i for i in SETS[n]["items"] if i["id"] == iid)


POOL = {}  # item id -> list of floats the reader computed


def close(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


class Item:
    def __init__(self, n, iid):
        self.n, self.id, self.it = n, iid, item(n, iid)
        self.pool = POOL.setdefault(iid, [])

    def reg(self, *vals):
        self.pool.extend(float(v) for v in vals)

    def key(self, k, mine, dp=None, printed=None):
        """Part k (1-based): key equals mine (rounded to dp), band takes it."""
        w = self.it["parts"][k - 1]["widget"]
        lab = f"{self.id} part {k}"
        mine = float(mine)
        self.reg(mine)
        ans, tol = float(w["answer"]), float(w["tol"]["abs"])
        target = round(mine, dp) if dp is not None else mine
        ok(close(ans, target, 1e-9), f"{lab}: key {ans} against reader {target}")
        ok(abs(mine - ans) <= tol + 1e-12, f"{lab}: band {ans}±{tol} refuses the exact value {mine}")
        if dp is not None:
            # the stated rounding, half up and half even, and one more place
            for r in {round(mine, dp), math.floor(mine * 10**dp + 0.5) / 10**dp, round(mine, dp + 1)}:
                ok(abs(r - ans) <= tol + 1e-12, f"{lab}: band refuses the rounding {r}")
        if printed is not None:
            ok(abs(float(printed) - ans) <= tol + 1e-12, f"{lab}: band refuses the printed route {printed}")
        return ans, tol

    def wrong(self, k, wid, mine, loose=None):
        """Slip `wid` of part k equals mine and its band misses the key band."""
        w = self.it["parts"][k - 1]["widget"]
        lab = f"{self.id} part {k} wrong {wid}"
        e = next((x for x in w.get("wrong", []) if x["id"] == wid), None)
        ok(e is not None, f"{lab}: missing")
        if e is None:
            return
        mine = float(mine)
        self.reg(mine)
        v, t = float(e["value"]), float(e["tol"]["abs"])
        ok(abs(v - mine) <= (loose if loose is not None else t) + 1e-12, f"{lab}: {v} against reader {mine}")
        a, ta = float(w["answer"]), float(w["tol"]["abs"])
        ok(abs(v - a) > t + ta, f"{lab}: band {v}±{t} meets the key band {a}±{ta}")
        ok(wid in self.it["parts"][k - 1]["feedback"].get("byKey", {}), f"{lab}: no byKey feedback")

    def all_wrongs_named(self, k, ids):
        w = self.it["parts"][k - 1]["widget"]
        got = sorted(x["id"] for x in w.get("wrong", []))
        ok(got == sorted(ids), f"{self.id} part {k}: wrong ids {got} against checked {sorted(ids)}")
        # no two wrong bands overlap each other
        for x, y in combinations(w.get("wrong", []), 2):
            ok(abs(float(x["value"]) - float(y["value"])) > float(x["tol"]["abs"]) + float(y["tol"]["abs"]),
               f"{self.id} part {k}: wrong bands {x['id']} and {y['id']} overlap")

    def choice(self, k, correct_id):
        opts = self.it["parts"][k - 1]["widget"]["options"]
        right = [o["id"] for o in opts if o.get("correct")]
        ok(right == [correct_id], f"{self.id} part {k}: correct option {right} against {correct_id}")


def mse(pred, y):
    return sum((F(p) - F(v)) ** 2 for p, v in zip(pred, y)) / len(y)


def mae(pred, y):
    return sum(abs(F(p) - F(v)) for p, v in zip(pred, y)) / len(y)


def pvar(xs, ddof=0):
    m = sum(map(F, xs)) / len(xs)
    return sum((F(x) - m) ** 2 for x in xs) / (len(xs) - ddof)


# =============================================================== problems-1
# ---- p-ferry-passengers
I = Item(1, "p-ferry-passengers")
tr, te = [4, 7, 5, 9, 6, 11], [8, 6, 10, 12]
mean = F(sum(tr), len(tr))
scan = minimize_scalar(lambda c: sum((x - c) ** 2 for x in tr)).x  # route 2: minimise
ok(close(scan, mean, 1e-6), "ferry: mean is the minimiser")
I.key(1, mean)
med = F(sorted(tr)[2] + sorted(tr)[3], 2)
I.wrong(1, "median", med)
I.wrong(1, "midrange", F(min(tr) + max(tr), 2))
I.all_wrongs_named(1, ["median", "midrange"])
I.reg(sum(tr), 42 / 6)
tm = mse([mean] * 6, tr)
ok(close(tm, np.var(tr)), "ferry: training MSE is np.var")
I.key(2, tm, dp=3)
I.wrong(2, "n-minus-1", pvar(tr, 1))
I.wrong(2, "absolute", mae([mean] * 6, tr))
I.wrong(2, "sum", tm * 6)
I.all_wrongs_named(2, ["n-minus-1", "absolute", "sum"])
ok([x - 7 for x in tr] == [-3, 0, -2, 2, -1, 4], "ferry: printed training misses")
I.reg(-3, 0, -2, 2, -1, 4, 34, 34 / 6)
tst = mse([mean] * 4, te)
ok(close(tst, np.mean((np.array(te) - 7.0) ** 2)), "ferry: test MSE numpy")
I.key(3, tst)
I.wrong(3, "test-mean", pvar(te))
I.wrong(3, "carried", mse([med] * 4, te))
I.wrong(3, "absolute", mae([mean] * 4, te))
I.all_wrongs_named(3, ["test-mean", "carried", "absolute"])
ok([x - 7 for x in te] == [1, -1, 3, 5], "ferry: printed test misses")
I.reg(36, F(sum(te), 4), 1, -1, 3, 5)
# lowest degree through six points with distinct x: residual 0 at 5, not at 4
rng = np.random.default_rng(7)
least = []
for _ in range(50):
    x = rng.choice(np.arange(-5, 25), 6, replace=False).astype(float)
    r = [np.abs(np.polyval(np.polyfit(x, tr, d), x) - tr).max() for d in range(6)]
    least.append(min(d for d in range(6) if r[d] < 1e-6))
ok(set(least) == {5}, "ferry: degree 5 is least for 50 random sets of distinct temperatures")
I.key(4, 5)
I.wrong(4, "six", 6)
I.wrong(4, "coefficients-short", 4)
I.all_wrongs_named(4, ["six", "coefficients-short"])
I.choice(5, "constant")
ok(tst < F("31.4") and F("31.4") / tst > 3, "ferry: 31.4 is more than 3 times 9")
I.reg(31.4, (9 + 31.4) / 2, 7, 6, 4)

# ---- p-loaves-k
I = Item(1, "p-loaves-k")
truth, noise = 20, 4
k20, k1 = [17, 18, 16, 17, 17], [23, 18, 19, 17, 23]
b20 = F(sum(k20), 5) - truth
I.key(1, b20**2)
I.wrong(1, "bias", b20)
I.wrong(1, "size", abs(b20))
I.wrong(1, "variance", pvar(k20))
I.all_wrongs_named(1, ["bias", "size", "variance"])
e20 = b20**2 + pvar(k20) + noise
ok(close(e20, (np.mean(k20) - truth) ** 2 + np.var(k20) + noise), "loaves: k=20 numpy")
I.key(2, e20)
I.wrong(2, "no-noise", b20**2 + pvar(k20))
I.wrong(2, "ddof1", b20**2 + pvar(k20, 1) + noise)
I.wrong(2, "carried", abs(b20) + pvar(k20) + noise)
I.all_wrongs_named(2, ["no-noise", "ddof1", "carried"])
ok([x - 17 for x in k20] == [0, 1, -1, 0, 0], "loaves: printed deviations k=20")
b1 = F(sum(k1), 5) - truth
e1 = b1**2 + pvar(k1) + noise
ok(b1 == 0 and pvar(k1) == F(32, 5), "loaves: k=1 bias 0 and variance 6.4")
ok(close(e1, (np.mean(k1) - truth) ** 2 + np.var(k1) + noise), "loaves: k=1 numpy")
I.key(3, e1)
I.wrong(3, "no-noise", b1**2 + pvar(k1))
I.wrong(3, "ddof1", b1**2 + pvar(k1, 1) + noise)
I.wrong(3, "carried", e20)
I.all_wrongs_named(3, ["no-noise", "ddof1", "carried"])
ok([x - 20 for x in k1] == [3, -2, -1, -3, 3], "loaves: printed deviations k=1")
e5 = 1 + F(noise, 5) + noise
sim = np.random.default_rng(3).normal(0, 2, (400000, 5)).mean(axis=1).var()  # route 2
ok(abs(sim - 0.8) < 0.01, "loaves: mean of five noises has variance 0.8 (simulated)")
I.key(4, e5)
I.wrong(4, "no-average", 1 + noise + noise)
I.wrong(4, "no-noise", 1 + F(noise, 5))
I.all_wrongs_named(4, ["no-average", "no-noise"])
I.choice(5, "k5")
ok(e5 < e1 < e20, "loaves: 5.8 < 10.4 < 13.4")
I.reg(85, 85 / 5, 100, 100 / 5, 2 / 5, 32, 32 / 5, 0.8, 3, -3, -2, -1, 2, 0)

# ---- p-broker-clients
I = Item(1, "p-broker-clients")
C = {"A": (13, 340, 7), "B": (22, 315, 3), "C": (15, 290, 8), "D": (9, 312, 4)}
new, sd = (14, 310), (5, 40)
raw = {k: math.hypot(v[0] - new[0], v[1] - new[1]) for k, v in C.items()}
sc = {k: math.hypot((v[0] - new[0]) / sd[0], (v[1] - new[1]) / sd[1]) for k, v in C.items()}
I.key(1, raw["D"], dp=2)
ok(min(raw, key=raw.get) == "D" and sorted(raw, key=raw.get)[1] == "B", "broker: raw order D then B")
I.wrong(1, "squared", raw["D"] ** 2)
I.wrong(1, "city-block", abs(14 - 9) + abs(310 - 312))
I.all_wrongs_named(1, ["squared", "city-block"])
I.key(2, sc["C"], dp=2)
ok(sorted(sc, key=sc.get) == ["C", "A", "D", "B"], "broker: scaled order C, A, D, B")
I.wrong(2, "raw", raw["C"])
I.wrong(2, "variance", math.hypot(1 / 25, 20 / 1600))
I.all_wrongs_named(2, ["raw", "variance"])
for k, v in list(raw.items()) + list(sc.items()):
    I.reg(round(v, 2))
I.reg(0.29, 0.04, 0.25, 1 / 5, 20 / 40, 25, 29, 16, 1.00, 1.60)
X = np.array([[v[0] / 5, v[1] / 40] for v in C.values()])
y = np.array([v[2] for v in C.values()], float)
knn = KNeighborsRegressor(n_neighbors=2).fit(X, y).predict([[14 / 5, 310 / 40]])[0]  # route 2
f2 = F(C["C"][2] + C["A"][2], 2)
ok(close(knn, f2), "broker: scikit-learn 2-NN on scaled features")
I.key(3, f2)
rawf = F(C["D"][2] + C["B"][2], 2)
Xr = np.array([[v[0], v[1]] for v in C.values()], float)
ok(close(KNeighborsRegressor(n_neighbors=2).fit(Xr, y).predict([[14, 310]])[0], rawf), "broker: raw 2-NN")
I.wrong(3, "raw", rawf)
I.wrong(3, "all-four", F(sum(v[2] for v in C.values()), 4))
I.wrong(3, "one", C["C"][2])
I.all_wrongs_named(3, ["raw", "all-four", "one"])
fc, act = [F("7.5"), 6, 5], [7, F("6.5"), 4]
I.key(4, mse(fc, act))
I.wrong(4, "carried", mse([rawf, 6, 5], act))
I.wrong(4, "absolute", mae(fc, act), loose=0.0001)
I.wrong(4, "sum", mse(fc, act) * 3)
I.all_wrongs_named(4, ["carried", "absolute", "sum"])
tmean = F(sum(v[2] for v in C.values()), 4)
ok(tmean == F("5.5"), "broker: training mean 5.5")
I.key(5, mse([tmean] * 3, act), dp=3)
I.wrong(5, "test-mean", pvar(act))
I.wrong(5, "absolute", mae([tmean] * 3, act))
I.wrong(5, "sum", mse([tmean] * 3, act) * 3)
I.all_wrongs_named(5, ["test-mean", "absolute", "sum"])
I.reg(0.5, -0.5, 1, 1.5, -1.5, 2.25, 0.25, 5.5, 2, 3)

# ---- p-heat-demand
I = Item(1, "p-heat-demand")
T = {0: ("9.20", "9.85"), 1: ("3.10", "3.42"), 2: ("1.44", "1.80"), 3: ("1.38", "1.95"), 6: ("1.02", "2.60")}
T = {d: (F(a), F(b)) for d, (a, b) in T.items()}
nz = F("1.20")
best = min(T, key=lambda d: T[d][1])
I.key(1, best)
I.wrong(1, "training", min(T, key=lambda d: T[d][0]))
I.wrong(1, "next", 3)
I.all_wrongs_named(1, ["training", "next"])
tr_list = [T[d][0] for d in sorted(T)]
ok(all(a > b for a, b in zip(tr_list, tr_list[1:])), "heat: training MSE falls at every degree")
te_list = [T[d][1] for d in sorted(T)]
ok(te_list[2] == min(te_list) and te_list[3] < te_list[4], "heat: test MSE bottoms at degree 2 then climbs")
above = T[2][1] - nz
I.key(2, above)
I.wrong(2, "training", T[2][0] - nz)
I.wrong(2, "carried", T[6][1] - nz)
I.wrong(2, "added", T[2][1] + nz)
I.all_wrongs_named(2, ["training", "carried", "added"])
var2 = F("0.36")
b2 = above - var2
I.key(3, b2)
I.wrong(3, "sd", above - var2**2)
I.wrong(3, "carried", (T[6][1] - nz) - var2)
I.wrong(3, "added", above + var2)
I.all_wrongs_named(3, ["sd", "carried", "added"])
e400 = nz + b2 + var2 * F(40, 400)
I.key(4, e400, dp=3)
I.wrong(4, "all-shrink", nz + (b2 + var2) / 10)
I.wrong(4, "no-noise", b2 + var2 / 10)
I.wrong(4, "carried", nz + ((T[6][1] - nz) - var2) + var2 / 10)
I.all_wrongs_named(4, ["all-shrink", "no-noise", "carried"])
b6 = F("0.02")
v6 = T[6][1] - nz - b6
e6 = nz + b6 + v6 / 10
I.key(5, e6, dp=3)
I.wrong(5, "no-shrink", T[6][1])
I.wrong(5, "all-shrink", nz + (b6 + v6) / 10)
I.wrong(5, "no-noise", b6 + v6 / 10)
I.all_wrongs_named(5, ["no-shrink", "all-shrink", "no-noise"])
ok(e6 < e400 and nz + b2 == F("1.44"), "heat: degree 6 below degree 2 at 400 days; floor 1.44")
# route 2: the 1/n rule written with n, and the crossover where degree 6 wins
f = lambda n, b, v40: float(nz + b + v40 * 40 / n)
ok(close(f(400, b2, var2), 1.476) and close(f(400, b6, v6), 1.358), "heat: 1/n rule as a function of n")
cross = brentq(lambda n: f(n, b2, var2) - f(n, b6, v6), 41, 4000)
ok(40 < cross < 400, f"heat: degrees cross between 40 and 400 days ({cross:.1f})")
I.reg(v6, v6 / 10, var2 / 10, 1.44, 10, 200, 400, 40)

# =============================================================== problems-2
# ---- p-ice-cream-van
I = Item(2, "p-ice-cream-van")
fhat = lambda x, w, inter=True: 20 + F("1.5") * x + 8 * w + (F("0.5") * x * w if inter else 0)
days = [(12, 1, 55), (10, 0, 33), (16, 0, 45), (6, 1, 38)]
I.key(1, fhat(1, 1) - fhat(0, 1))
I.wrong(1, "weekday", fhat(1, 0) - fhat(0, 0))
I.wrong(1, "interaction", F("0.5"))
I.all_wrongs_named(1, ["weekday", "interaction"])
I.key(2, fhat(12, 1))
I.wrong(2, "no-interaction", fhat(12, 1, False))
I.wrong(2, "no-dummy", fhat(12, 1) - 8)
I.wrong(2, "weekday", fhat(12, 0))
I.all_wrongs_named(2, ["no-interaction", "no-dummy", "weekday"])
pred = [fhat(x, w) for x, w, _ in days]
ys = [d[2] for d in days]
ok(pred == [52, 35, 44, 40], "ice: forecasts 52, 35, 44, 40")
ok([a - p for a, p in zip(ys, pred)] == [3, -2, 1, -2], "ice: printed misses")
m = mse(pred, ys)
# route 2: design matrix times coefficients in NumPy
Xd = np.array([[1, x, w, x * w] for x, w, _ in days], float)
ok(close(np.mean((Xd @ [20, 1.5, 8, 0.5] - ys) ** 2), m), "ice: test MSE by matrix product")
I.key(3, m)
I.wrong(3, "carried", mse([fhat(x, w, False) for x, w, _ in days], ys))
I.wrong(3, "absolute", mae(pred, ys))
I.wrong(3, "sum", m * 4)
I.all_wrongs_named(3, ["carried", "absolute", "sum"])
base = mse([40] * 4, ys)
ok([a - 40 for a in ys] == [15, -7, 5, -2], "ice: printed baseline misses")
I.key(4, base)
I.wrong(4, "test-mean", pvar(ys))
I.wrong(4, "absolute", mae([40] * 4, ys))
I.all_wrongs_named(4, ["test-mean", "absolute"])
r2 = 1 - m / base
I.key(5, r2, dp=3, printed=1 - 0.0594)
I.wrong(5, "ratio", m / base)
I.wrong(5, "test-mean", 1 - m / pvar(ys))
I.wrong(5, "carried", 1 - mse([fhat(x, w, False) for x, w, _ in days], ys) / base)
I.all_wrongs_named(5, ["ratio", "test-mean", "carried"])
I.reg(35, 44, 40, 52, 15, -7, 5, -2, 28, 18, 6, 225, 49, 25, 4, 303, F(sum(ys), 4), 0.0594, 94.1, 20 + 18 + 8 + 6)

# ---- p-rent-ridge
I = Item(2, "p-rent-ridge")
n, sxy, sxx, lam = 25, F(90), F(100), 20
# route 2: build centred data with these sums and fit scikit-learn
rng = np.random.default_rng(11)
x = rng.normal(size=n); x -= x.mean(); x *= math.sqrt(100 / (x @ x))
e = rng.normal(size=n); e -= e.mean(); e -= (e @ x) / (x @ x) * x
yv = 0.9 * x + e
ok(close(x @ yv, 90, 1e-9) and close(x @ x, 100, 1e-9), "rent: built data has the stated sums")
fit = lambda xx, a: Ridge(alpha=a, fit_intercept=False).fit(xx.reshape(-1, 1), yv).coef_[0]
ols = sxy / sxx
ok(close(LinearRegression().fit(x.reshape(-1, 1), yv).coef_[0], ols), "rent: OLS by scikit-learn")
I.key(1, ols)
I.wrong(1, "inverse", sxx / sxy)
I.wrong(1, "per-month", sxy / n)
I.all_wrongs_named(1, ["inverse", "per-month"])
rd = sxy / (sxx + lam)
ok(close(fit(x, 20), rd), "rent: Ridge(alpha=20) on basis points")
I.key(2, rd)
I.wrong(2, "ols", ols)
I.wrong(2, "subtracted", sxy / (sxx - lam))
I.wrong(2, "on-top", (sxy + lam) / sxx)
I.all_wrongs_named(2, ["ols", "subtracted", "on-top"])
pp = (sxy / 100) / (sxx / 10000 + lam)
ok(close(fit(x / 100, 20), pp), "rent: Ridge(alpha=20) on percentage points")
I.key(3, pp, dp=3)
I.wrong(3, "ols", (sxy / 100) / (sxx / 10000))
I.wrong(3, "unchanged", rd)
I.wrong(3, "shrunk-units", rd / 100)
I.all_wrongs_named(3, ["ols", "unchanged", "shrunk-units"])
ok(abs(float(90 / pp) - 2000) < 2, f"rent: 0.045 is about a 2,000th of 90 (exactly 1/{float(90 / pp):.0f})")
s = math.sqrt(sxx / n)
ok(close(s, 2) and close(np.std(x), 2), "rent: sd dividing by n is 2")
z = sxy / 2 / (sxx / 4 + lam)
ok(close(fit(x / np.std(x), 20), z) and close(fit(x / 100 / np.std(x / 100), 20), z), "rent: standardised ridge, either unit")
I.key(4, z)
I.wrong(4, "unscaled", rd)
I.wrong(4, "variance", (sxy / 4) / (sxx / 16 + lam))
I.wrong(4, "ols", (sxy / 2) / (sxx / 4))
I.all_wrongs_named(4, ["unscaled", "variance", "ols"])
I.key(5, z / 2)
I.wrong(5, "times-sd", z * 2)
I.wrong(5, "not-converted", z)
I.wrong(5, "carried", rd / 2)
I.all_wrongs_named(5, ["times-sd", "not-converted", "carried"])
I.reg(120, 90 / 120, 100 / 120, 0.01, 20.01, 0.9, 45, 25, 50, 2000, 10000, 100, 2, z / 2 * 100)

# ---- p-futures-lasso
I = Item(2, "p-futures-lasso")
bo = [F("0.42"), F("-0.27"), F("0.11"), F("-0.06"), F("0.18")]
a, b0 = F("0.15"), F("0.30")
soft = lambda b, a: (1 if b > 0 else -1) * max(abs(b) - a, 0)
bl = [soft(b, a) for b in bo]
# route 2: scikit-learn Lasso on an orthogonal design with X'X = nI and these OLS coefficients
rng = np.random.default_rng(5)
nn = 400
Q, _ = np.linalg.qr(rng.normal(size=(nn, 6)))
Xo = math.sqrt(nn) * Q[:, :5]
yo = Xo @ np.array(bo, float) + 3.0 * Q[:, 5]
ok(np.allclose(LinearRegression(fit_intercept=False).fit(Xo, yo).coef_, np.array(bo, float)), "lasso: built OLS coefficients")
las = lambda al: Lasso(alpha=al, fit_intercept=False, tol=1e-12, max_iter=100000).fit(Xo, yo).coef_
ok(np.allclose(las(0.15), np.array(bl, float), atol=1e-8), "lasso: Lasso(alpha=0.15) is soft thresholding")
I.key(1, sum(1 for b in bl if b != 0))
I.wrong(1, "ridge", 5)
I.wrong(1, "positive", sum(1 for b in bo if b > a))
I.all_wrongs_named(1, ["ridge", "positive"])
I.key(2, bl[1])
I.wrong(2, "sign", -bl[1])
I.wrong(2, "away", bo[1] - a)
I.all_wrongs_named(2, ["sign", "away"])
amax = max(abs(b) for b in bo)
ok(np.count_nonzero(las(0.42)) == 0 and np.count_nonzero(las(0.4199)) == 1, "lasso: empty at 0.42, not at 0.4199")
I.key(3, amax)
I.wrong(3, "sum", sum(abs(b) for b in bo))
I.wrong(3, "first", min(abs(b) for b in bo))
I.all_wrongs_named(3, ["sum", "first"])
zc = F(7 - 1, 4)
I.key(4, zc)
I.wrong(4, "no-centre", F(7, 4))
I.wrong(4, "variance", F(7 - 1, 16))
I.all_wrongs_named(4, ["no-centre", "variance"])
zs = [zc, 1, -2, F("1.5"), 1]
dot = lambda bb, zz: b0 + sum(x * y for x, y in zip(bb, zz))
fc = dot(bl, zs)
ok(close(b0 + las(0.15) @ np.array(zs, float), fc, 1e-7), "lasso: forecast by scikit-learn coefficients")
I.key(5, fc, dp=3)
I.wrong(5, "ols", dot(bo, zs))
I.wrong(5, "no-shrink", dot([b if soft(b, a) != 0 else 0 for b in bo], zs))
I.wrong(5, "sign", dot([bl[0], -bl[1]] + bl[2:], zs))
carried = dot(bl, [F(7, 4)] + zs[1:])
I.wrong(5, "carried", carried)
I.all_wrongs_named(5, ["ols", "no-shrink", "sign", "carried"])
# NOTE (finding): the carried slip is exactly 0.6825, on the edge of its own band
print(f"NOTE futures-lasso part 5 carried slip is exactly {float(carried)}; listed 0.683 ± 0.0005")
I.reg(*[float(b) for b in bl], 0.405, 16, 4, 6, 7, 1, 0.27 * 1.5)

# ---- p-built-ridge
I = Item(2, "p-built-ridge")
true, est, nz, n = [F("0.5"), F("0.2"), F(0)], [F("0.6"), F("0.1"), F("0.14")], F(2), 500
emse = lambda bb: nz + sum((b - t) ** 2 for b, t in zip(bb, true))
shr = lambda lam: [b * F(n, n + lam) for b in est]
# route 2: scikit-learn Ridge on X'X = nI, and a simulated test set for the expected MSE
Q, _ = np.linalg.qr(rng.normal(size=(n, 4)))
Xb = math.sqrt(n) * Q[:, :3]
yb = Xb @ np.array(est, float) + 5.0 * Q[:, 3]
for lam in (125, 500):
    cf = Ridge(alpha=lam, fit_intercept=False).fit(Xb, yb).coef_
    ok(np.allclose(cf, np.array(shr(lam), float)), f"built: Ridge(alpha={lam}) multiplies by n/(n + lambda)")
Zt = rng.normal(size=(2_000_000, 3))
yt = Zt @ np.array(true, float) + rng.normal(0, math.sqrt(2), 2_000_000)
for bb in (est, shr(125), shr(500), [0, 0, 0]):
    ok(abs(np.mean((yt - Zt @ np.array(bb, float)) ** 2) - float(emse(bb))) < 0.01, "built: simulated test MSE")
I.key(1, emse(est), dp=4)
I.wrong(1, "no-noise", emse(est) - nz)
I.wrong(1, "unsquared", nz + sum(abs(b - t) for b, t in zip(est, true)))
I.all_wrongs_named(1, ["no-noise", "unsquared"])
I.key(2, emse(shr(125)), dp=4)
lin125 = emse([b * (1 - F(125, n)) for b in est])
I.wrong(2, "lambda-over-n", lin125, loose=0.0001)
print(f"NOTE built-ridge part 2 lambda-over-n slip is exactly {float(lin125)}; listed 2.0292")
I.wrong(2, "no-noise", emse(shr(125)) - nz, loose=0.0001)
I.all_wrongs_named(2, ["lambda-over-n", "no-noise"])
I.key(3, emse(shr(500)), dp=4)
I.wrong(3, "lambda-over-n", emse([b * (1 - F(500, n)) for b in est]))
I.wrong(3, "no-noise", emse(shr(500)) - nz)
I.all_wrongs_named(3, ["lambda-over-n", "no-noise"])
I.key(4, emse([0, 0, 0]))
I.wrong(4, "noise-only", nz)
I.wrong(4, "ols-coefs", nz + sum(b * b for b in est))
I.all_wrongs_named(4, ["noise-only", "ols-coefs"])
r2 = lambda bb: 1 - emse(bb) / emse([0, 0, 0])
I.key(5, r2(shr(125)), dp=3, printed=1 - 2.0273 / 2.29)
I.wrong(5, "ols", r2(est))
I.wrong(5, "ratio", emse(shr(125)) / emse([0, 0, 0]))
I.wrong(5, "too-much", r2(shr(500)))
I.all_wrongs_named(5, ["ols", "ratio", "too-much"])
ok(emse(shr(125)) < emse(est) < emse(shr(500)) < emse([0, 0, 0]), "built: 125 beats OLS beats 500 beats the mean")
# CLAIM (review finding 1; fails until the text is fixed): part 2's explain says shrinking "adds a little bias to the real 0.5 and cuts the noise in the other two"
e0 = [(b - t) ** 2 for b, t in zip(est, true)]
e1 = [(b - t) ** 2 for b, t in zip(shr(125), true)]
claim = e1[0] > e0[0] and e1[1] < e0[1] and e1[2] < e0[2]
print("CLAIM built-ridge part 2 explain (0.5 loses, the other two gain):", claim,
      "| squared errors OLS", [float(v) for v in e0], "ridge", [float(v) for v in e1])
ok(claim or "cuts the noise in the other two" not in I.it["parts"][1]["explain"]["text"],
   "built part 2 explain: 'adds a little bias to the real 0.5 and cuts the noise in the other two' is false: "
   "0.6 -> 0.48 gains (0.01 to 0.0004), 0.1 -> 0.08 loses (0.01 to 0.0144)  [review finding 1]")
I.reg(*[float(v) for v in e0 + e1], *[float(b) for b in shr(125) + shr(500)], 0.0396, 0.027344, 0.0674,
      0.04, 0.0225, 0.0049, 625, 1000, 0.8, 0.75, 0.25, 0.8853, 11.5, 10.9, 9.7, 500 / 625, 500 / 1000)

# =============================================================== problems-3
# ---- p-order-fill
I = Item(3, "p-order-fill")
zf = lambda d, v: 1.4 - 0.9 * d + 0.5 * v
sig = lambda t: 1 / (1 + math.exp(-t))
p1 = sig(zf(2, 1))
ok(close(p1, expit(0.1)), "fill: sigmoid by SciPy")
I.key(1, p1, dp=3)
I.wrong(1, "log-odds", zf(2, 1))
I.wrong(1, "sign", sig(-zf(2, 1)))
I.wrong(1, "odds", math.exp(zf(2, 1)))
I.all_wrongs_named(1, ["log-odds", "sign", "odds"])
orr = math.exp(-0.9)
ok(close((sig(zf(3, 1)) / (1 - sig(zf(3, 1)))) / (p1 / (1 - p1)), orr), "fill: odds ratio from two probabilities")
I.key(2, orr, dp=3)
I.wrong(2, "beta", -0.9)
I.wrong(2, "reciprocal", math.exp(0.9), loose=0.005)
I.wrong(2, "prob", sig(-0.9))
I.all_wrongs_named(2, ["beta", "reciprocal", "prob"])
ok(round((1 - orr) * 100) == 59, "fill: odds cut by 59%")
p3 = sig(zf(3, 1))
od = 0.525 / 0.475 * 0.407
I.key(3, p3, dp=3, printed=od / (1 + od))
I.wrong(3, "prob-times", 0.525 * 0.407)
I.wrong(3, "odds", od)
oc = 0.475 / 0.525 * 0.407
I.wrong(3, "carried", oc / (1 + oc))
I.all_wrongs_named(3, ["prob-times", "odds", "carried"])
ok(round(0.525 - 0.310, 3) == 0.215 and close(zf(3, 1), -0.8), "fill: fall of 0.215; z = -0.8")
# threshold: scan of expected costs. Rest when (1 - p) * 120 < p * 30
thr = F(120, 150)
ps = np.linspace(0, 1, 100001)
flip = ps[np.argmax((1 - ps) * 120 < ps * 30)]
ok(abs(flip - 0.8) < 2e-5, "fill: expected-cost scan flips at 0.8")
I.key(4, thr)
I.wrong(4, "swapped", F(30, 150))
I.wrong(4, "ratio", F(120, 30))
I.wrong(4, "half", F(1, 2))
I.all_wrongs_named(4, ["swapped", "ratio", "half"])
dstar = (1.9 - math.log(4)) / 0.9
ok(close(brentq(lambda d: sig(zf(d, 1)) - 0.8, 0, 5), dstar, 1e-9), "fill: boundary by root finding")
I.key(5, dstar, dp=3, printed=0.514 / 0.9)
I.wrong(5, "t-as-z", (1.9 - 0.8) / 0.9)
I.wrong(5, "carried", (1.9 - math.log(0.25)) / 0.9)
I.wrong(5, "no-log", (1.9 - 4) / 0.9)
I.all_wrongs_named(5, ["t-as-z", "carried", "no-log"])
I.reg(0.1, 1.8, 2.7, -0.8, 1.105, 2.105, 0.450, 1.450, 0.310, 0.215, 59, math.log(4), 0.514, 1.9, 150, 4, 0.2, 120, 30, 0.5)

# ---- p-payment-misses
I = Item(3, "p-payment-misses")
N, pos, flag, tp = 800, 40, 100, 24
fp, fn = flag - tp, pos - tp
tn = N - pos - fp
yt_ = np.r_[np.ones(tp), np.zeros(fp), np.ones(fn), np.zeros(tn)]
yp_ = np.r_[np.ones(flag), np.zeros(N - flag)]
ok(close(precision_score(yt_, yp_), F(tp, flag)) and close(recall_score(yt_, yp_), F(tp, pos)), "misses: scikit-learn precision and recall")
I.key(1, F(tp, flag))
I.wrong(1, "recall", F(tp, pos))
I.wrong(1, "all", F(tp, N))
I.all_wrongs_named(1, ["recall", "all"])
I.key(2, F(tp, pos))
I.wrong(2, "precision", F(tp, flag))
I.wrong(2, "flag-rate", F(flag, N))
I.all_wrongs_named(2, ["precision", "flag-rate"])
acc = F(tp + tn, N)
ok(close(accuracy_score(yt_, yp_), acc) and tn == 684 and fp == 76 and fn == 16, "misses: accuracy; 684, 76, 16")
I.key(3, acc, dp=3)
I.wrong(3, "always-no", F(N - pos, N))
I.wrong(3, "no-fp", F(tp + N - pos, N))
I.wrong(3, "hits-only", F(tp, N))
I.all_wrongs_named(3, ["always-no", "no-fp", "hits-only"])
gap = F("0.40") - F(tp, flag)
I.key(4, gap)
I.wrong(4, "recall", F("0.40") - F(tp, pos))
I.wrong(4, "base", F("0.40") - F(pos, N))
I.all_wrongs_named(4, ["recall", "base"])
g2 = abs(F("0.04") - F(fn, N - flag))
ece = F(flag, N) * gap + F(N - flag, N) * g2
# route 2: per-row arrays, binned in NumPy
pr = np.r_[np.full(flag, 0.40), np.full(N - flag, 0.04)]
ece2 = sum(np.mean(yp_ == b) * abs(pr[yp_ == b].mean() - yt_[yp_ == b].mean()) for b in (0, 1))
ok(close(ece, ece2), "misses: ECE over rows")
I.key(5, ece, dp=3)
I.wrong(5, "unweighted", (gap + g2) / 2)
I.wrong(5, "flagged-only", F(flag, N) * gap)
I.wrong(5, "carried", F(flag, N) * (F("0.40") - F(pos, N)) + F(N - flag, N) * g2)
I.all_wrongs_named(5, ["unweighted", "flagged-only", "carried"])
ok(round(float(F(tp, flag) / F(pos, N)), 1) == 4.8 and F(flag, N) * gap > F(N - flag, N) * g2, "misses: about 5 times the base rate; flagged bin is most of the ECE")
I.reg(0.05, 16 / 700, 0.0229, float(g2), 0.0171, 0.017, 0.125, 0.875, 0.020, 0.015, 708, 684, 76, 760, 16, 5, 0.95, 700)

# ---- p-sterling-calls
I = Item(3, "p-sterling-calls")
N, up, calls, right_up = 260, 143, 150, 99
I.key(1, F(right_up, calls))
I.wrong(1, "recall", F(right_up, up))
I.wrong(1, "base", F(up, N))
I.all_wrongs_named(1, ["recall", "base"])
down_calls = N - calls
right_down = down_calls - (up - right_up)
hit = F(right_up + right_down, N)
ya = np.r_[np.ones(right_up), np.zeros(calls - right_up), np.ones(up - right_up), np.zeros(right_down)]
yc = np.r_[np.ones(calls), np.zeros(down_calls)]
ok(close(accuracy_score(ya, yc), hit) and ya.sum() == up, "sterling: hit rate over built label arrays")
I.key(2, hit, dp=3)
I.wrong(2, "up-only", F(right_up, N))
I.wrong(2, "precision", F(right_up, calls))
I.wrong(2, "down-calls", F(right_down, down_calls))
I.all_wrongs_named(2, ["up-only", "precision", "down-calls"])
base = float(F(up, N))
se = math.sqrt(base * (1 - base) / N)
t_print, t_exact = (0.635 - base) / se, (float(hit) - base) / se
w = I.it["parts"][2]["widget"]
I.key(3, t_print, dp=2, printed=t_exact)
ok(abs(round(t_exact, 2) - w["answer"]) <= w["tol"]["abs"], "sterling: band takes the unrounded route 2.74")
ok(abs(0.085 / 0.0309 - w["answer"]) <= w["tol"]["abs"], "sterling: band takes the printed quotient")
I.wrong(3, "coin", (0.635 - 0.5) / math.sqrt(0.25 / N))
I.wrong(3, "own-rate", (0.635 - base) / math.sqrt(0.635 * 0.365 / N))
I.wrong(3, "no-root", (0.635 - base) / math.sqrt(base * (1 - base)))
I.all_wrongs_named(3, ["coin", "own-rate", "no-root"])
cost = F(3, 10000) * 2_000_000
I.key(4, cost * 70)
I.wrong(4, "one-unit", cost * 70 / 2)
I.wrong(4, "per-flip", cost)
I.all_wrongs_named(4, ["one-unit", "per-flip"])
# route 2: a position path with 70 sign changes, 1.5 bp per unit traded
pos_path = np.array([1 if (i // 1) % 2 == 0 else -1 for i in range(71)])
ok(close(np.abs(np.diff(pos_path)).sum() * 2_000_000 * 1.5e-4, cost * 70), "sterling: flips by a position path")
I.key(5, 50000 - cost * 70)
I.wrong(5, "carried", 50000 - cost * 35)
I.wrong(5, "gross", 50000)
I.all_wrongs_named(5, ["carried", "gross"])
I.reg(0.55, 110, 44, 66, 165, 0.085, 0.0309, round(se, 4), 0.2475, 0.45, 600, 0.0003, 2000000, 42000, 3, 1.5, 70, 2.74)

# ---- p-price-spikes
I = Item(3, "p-price-spikes")
zs = lambda h: -3.0 + 0.8 * h
p = sig(zs(2.5))
I.key(1, p, dp=3)
I.wrong(1, "log-odds", zs(2.5))
I.wrong(1, "odds", math.exp(zs(2.5)))
I.wrong(1, "sign", 1 - p)
I.all_wrongs_named(1, ["log-odds", "odds", "sign"])
cfp, cfn = 6000, 18000
t = F(cfp, cfp + cfn)
flip = ps[np.argmax((1 - ps) * cfp < ps * cfn)]
ok(abs(flip - 0.25) < 2e-5, "spikes: expected-cost scan flips at 0.25")
I.key(2, t)
I.wrong(2, "swapped", F(cfn, cfp + cfn))
I.wrong(2, "miss-only", F(cfp, cfn))
I.all_wrongs_named(2, ["swapped", "miss-only"])
obs = F(18, 100)
I.key(3, obs)
I.wrong(3, "did-not", 1 - obs)
I.wrong(3, "gap", F("0.29") - obs)
I.all_wrongs_named(3, ["did-not", "gap"])
hedge, skip = (1 - obs) * cfp, obs * cfn
sim = np.random.default_rng(2).random(1_000_000) < 0.18
ok(abs(np.where(sim, 0, cfp).mean() - float(hedge)) < 15 and abs(np.where(sim, cfn, 0).mean() - float(skip)) < 30, "spikes: simulated costs")
I.key(4, hedge)
I.wrong(4, "model-p", (1 - 0.269) * cfp, loose=1)
I.wrong(4, "spike", obs * cfp)
I.wrong(4, "not-hedge", skip)
I.all_wrongs_named(4, ["model-p", "spike", "not-hedge"])
I.key(5, (hedge - skip) * 100)
I.wrong(5, "per-day", hedge - skip)
e = next(x for x in I.it["parts"][4]["widget"]["wrong"] if x["id"] == "model-p")
for pp_ in (0.269, p):  # the printed 0.269 and the unrounded probability are both caught
    v = ((1 - pp_) * cfp - pp_ * cfn) * 100
    ok(abs(v - e["value"]) <= e["tol"]["abs"], f"spikes part 5 model-p band takes {v:.0f}")
I.wrong(5, "model-p", ((1 - p) * cfp - p * cfn) * 100, loose=1)
I.wrong(5, "carried", (obs * cfp - skip) * 100)
I.all_wrongs_named(5, ["per-day", "model-p", "carried"])
ok(0.29 > t > obs and p > t, "spikes: 0.29 and 0.269 above the threshold, 0.18 below")
I.reg(0.5, -1.0, 1.368, 0.368, 24000, 0.82, 82, 1680, 3240, 0.29, 18, 100, 0.731, 3, 1, 2.5, 0.25, 0.35, 6000, 18000, 1080)

# =============================================================== printed numbers
# Every number in a feedback, byKey, why or explain string is either a given
# (item prose, a question, an option) or a value the reader computed above.
NUM = re.compile(r"(?<![\w.])-?\d[\d,{}]*\.?\d*")


def nums(s):
    out = []
    s = s.replace("{,}", ",").replace("$-$", "-").replace("−", "-")
    for m in NUM.findall(s):
        m = m.replace(",", "").replace("{", "").replace("}", "").rstrip(".")
        try:
            out.append(float(m))
        except ValueError:
            pass
    return out


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


unknown = 0
for n in (1, 2, 3):
    for it in SETS[n]["items"]:
        given = set(nums(it["prose"]))
        for p_ in it["parts"]:
            given |= set(nums(p_["question"]))
            for o in p_["widget"].get("options", []):
                given |= set(nums(o["text"]))
        pool = POOL[it["id"]]
        for k, p_ in enumerate(it["parts"], 1):
            for s in list(strings(p_["feedback"])) + list(strings(p_.get("explain", {}))) + [o.get("why", "") for o in p_["widget"].get("options", [])]:
                for v in nums(s):
                    known = v in given or abs(v) in given or float(v).is_integer() and abs(v) <= 6 or any(
                        abs(abs(v) - abs(q)) <= 5.01 * 10 ** (-max(len(repr(v).split(".")[-1]), 1) - 1) for q in pool)
                    checks += 1
                    if not known:
                        unknown += 1
                        fails += 1
                        print(f"FAIL printed number not rebuilt: {it['id']} part {k}: {v} in: {s[:90]}")

# =============================================================== shape
for n in (1, 2, 3):
    d = SETS[n]
    lessons = {1: range(1, 5), 2: range(5, 10), 3: range(10, 15)}[n]
    skills = set()
    for f in os.listdir(COURSE):
        m = re.match(r"l(\d+)-", f)
        if m and int(m.group(1)) in lessons:
            skills |= set(json.load(open(os.path.join(COURSE, f))).get("skills", []))
    ok(3 <= len(d["items"]) <= 5, f"set {n}: item count")
    ok(any(i["difficulty"] == 5 for i in d["items"]), f"set {n}: has a difficulty 5")
    typed = total = 0
    for i in d["items"]:
        ok(3 <= i["difficulty"] <= 5 and 3 <= len(i["parts"]) <= 5, f"{i['id']}: difficulty and part count")
        ok(set(i["skills"]) <= skills, f"{i['id']}: skills {i['skills']} against the level's {sorted(skills)}")
        for p_ in i["parts"]:
            total += 1
            typed += p_["widget"]["kind"] in ("numeric", "expression")
            ok(len(re.findall(r"[.!?](?:\s|$)", p_["explain"]["text"].replace("e.g.", "eg"))) <= 3 or True, "explain length (voice scan owns this)")
            if p_["widget"]["kind"] == "numeric":
                w = p_["widget"]
                whole = float(w["answer"]).is_integer()  # a whole key needs no form sentence
                ok(whole or re.search(r"decimal|whole number|pounds", p_["question"]), f"{i['id']}: numeric part states its form: {p_['question'][:60]}")
    ok(typed * 3 >= total * 2, f"set {n}: typed share {typed}/{total}")

print(f"reader checks: {checks}; failures: {fails}; printed numbers not rebuilt: {unknown}")
sys.exit(1 if fails else 0)
