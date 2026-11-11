"""Delta read, stat-learning L4 fix pass: every changed number by two routes, and a run behind each reworded sentence.

Usage: <venv python> recompute.py [content dir]       (CPython, scikit-learn 1.6.1: everything)
       node pyo.mjs <pkgs> recompute.py                (Pyodide 0.27.7: the same file, with the long searches shortened)

'ok'/'BAD' rows compare a recomputed value with what the content file now stores or states.
'FINDING' rows are results that contradict, or bound, a sentence in the content; they are judged in the review.
'NOTE' rows are values printed so that the two runtimes can be compared line by line.
"""
import json, math, os, re, sys, warnings
from fractions import Fraction as F
import numpy as np
warnings.filterwarnings("ignore")
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'courses', 'stat-learning')
PYO = __name__ == 'pyodide'
BAD = []; NFIND = 0; NOK = 0


def ok(cond, msg):
    global NOK
    NOK += 1
    print(('ok   ' if cond else 'BAD  ') + msg)
    if not cond:
        BAD.append(msg)


def finding(msg):
    global NFIND
    NFIND += 1
    print('FINDING ' + msg)


def note(msg):
    print('NOTE ' + msg)


def load(f):
    return json.load(open(os.path.join(ROOT, f)))


def text(o):
    return json.dumps(o, ensure_ascii=False)


L15, L16, L17, L18, L19 = (load(f) for f in ('l15-widest-street.json', 'l16-groups-nobody-labelled.json', 'l17-a-small-network.json', 'l18-bending-the-line.json', 'l19-which-learner.json'))
REV, HW = load('review-4.json'), load('homework-4.json')
G = {}
exec(L19['screens'][7]['widget']['prelude'], G)          # every make_* generator, PROBLEMS, LEARNERS
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import SplineTransformer, StandardScaler


def wrongs(widget):
    return {w['id']: w for w in widget.get('wrong', [])}


# ================================================================ l15
X6 = np.array([[1, 1], [0, 1], [2, 0], [3, 3], [4, 3], [3, 5]], float); y6 = np.array([0, 0, 0, 1, 1, 1])
s6 = np.where(y6 == 1, 1, -1)
v = s6 * (X6 @ np.array([2.0, 0.0]) - 5)
on = [tuple(int(t) for t in X6[i]) for i in range(6) if abs(v[i] - 1) < 1e-9]
ok(on == [(2, 0), (3, 3), (3, 5)] and all('$(%d, %d)$' % p in L15['screens'][3]['explain']['text'].replace('and ', '') or '(%d, %d)' % p in L15['screens'][3]['explain']['text'] for p in on),
   f"l15 s3: the vertical street rests on {on} (route 1: s(w.x+b)=1)")
ok(sorted(tuple(p) for p in X6[(np.abs(X6[:, 0] - 2.5) == np.abs(X6[:, 0] - 2.5).min())].astype(int).tolist()) == sorted(on), "l15 s3: same three loans are the nearest to x1 = 2.5 (route 2: distances)")
# s1: 'could move anywhere beyond their own edge without effect'
hard = lambda X: SVC(kernel='linear', C=1e6).fit(X, y6)
m0 = hard(X6); w0 = np.r_[m0.coef_[0], m0.intercept_]
ok(np.allclose(w0, [0.5, 0.5, -2], atol=1e-3), f"l15 s1: hard-margin fit is w = (0.5, 0.5), b = -2 ({np.round(w0, 4).tolist()})")
rng = np.random.default_rng(1); worst = 0.0
for _ in range(60 if PYO else 300):
    X = X6.copy()
    for i in (1, 4, 5):                                   # the three loans off the edges
        while True:
            p = rng.uniform(-8, 12, 2)
            if (y6[i] == 0 and p.sum() <= 2) or (y6[i] == 1 and p.sum() >= 6):
                break
        X[i] = p
    m = hard(X); worst = max(worst, float(np.abs(np.r_[m.coef_[0], m.intercept_] - w0).max()))
ok(worst < 2e-3, f"l15 s1: the three other loans moved anywhere beyond their own edges, 300 draws: the street moves by at most {worst:.1e}")
X = X6.copy(); X[1] = [5, 5]                              # a default beyond the repaid edge: outside the street, breaks it
m = SVC(kernel='linear', C=1e6).fit(X, y6)
ok(np.abs(np.r_[m.coef_[0], m.intercept_] - w0).max() > 0.1, "l15 s1: the old wording's counter-example (a default moved beyond the repaid edge) does move the street")
# s4: scikit-learn's C is a price: small C, wide street
Xs, ys = G['make_street'](200, 4); Xt, yt = G['make_street'](200, 5)
rows = []
for C in (0.01, 1, 100):
    m = SVC(kernel='linear', C=C).fit(Xs, ys)
    rows.append([str(C), str(int(m.n_support_.sum())), '%.2f' % (2 / np.linalg.norm(m.coef_)), ('%.3f' % m.score(Xt, yt))])
want = L15['screens'][4]['canvas']['params']['rows']
ok(rows == want, f"l15 s4 table by SVC: {rows}")
dual = []
for C in (0.01, 100):                                     # route 2: width from the dual coefficients
    m = SVC(kernel='linear', C=C).fit(Xs, ys)
    wv = (m.dual_coef_ @ m.support_vectors_)[0]
    dual.append(round(2 / float(np.linalg.norm(wv)), 2))
ok(dual == [2.78, 0.80], f"l15 s4 widths from dual_coef_ @ support_vectors_: {dual}; small C is the wide street")

# ================================================================ l16
S6 = [F(10), F(12), F(14), F(30), F(32), F(40)]
w1 = wrongs(L16['screens'][1]['widget'])
half = [(F(10) + 12) / 2, (F('25.6') + 34) / 2]
ok(w1['half']['value'] == '11, 29.8' and half == [11, F(149, 5)] and np.allclose([(10 + 12) / 2, (25.6 + 34) / 2], [11, 29.8]), f"l16 s1 half: {[float(h) for h in half]} (fractions and floats)")
ok('11 and 29.8' in L16['screens'][1]['feedback']['byKey']['half'], "l16 s1 half line states 11 and 29.8")
w2 = wrongs(L16['screens'][2]['widget'])
c = [12, 12, 12, 34, 34, 34]
ok(w2['unsq']['value'] == 16 == sum(abs(x - m) for x, m in zip(S6, c)) == int(np.abs(np.array([10, 12, 14, 30, 32, 40]) - np.array(c)).sum()) == 2 + 0 + 2 + 4 + 2 + 6, "l16 s2 unsq: 16 (fractions, NumPy, and the sum written in its own line)")
ok(sum((x - m) ** 2 for x, m in zip(S6, c)) == 64 and w2['onegroup']['value'] == 8 and abs(64 / 6 - w2['var']['value']) < 0.01, "l16 s2: 64, and the other two entries 8 and 10.67 untouched")
ans = [L16['screens'][2]['widget']['answer']] + [w['value'] for w in w2.values()]
ok(len(set(ans)) == len(ans), f"l16 s2: answer and wrong values all distinct {ans}")
# new test 9: squared distance against summed absolute gaps, exactly
pts, cen = [(0, 0), (0, 6), (4, 3)], [(0, 5), (3, 3)]
sq = [[(p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in cen] for p in pts]
man = [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in cen] for p in pts]
ok([r.index(min(r)) for r in sq] == [1, 0, 1] and [r.index(min(r)) for r in man] == [0, 0, 1] and all(r[0] != r[1] for r in sq + man), f"l16 s4 test 9: squared {sq} gives [1, 0, 1], absolute {man} gives [0, 0, 1], no tie in either")
# s5: raw k-means on make_stocks(11): starts
Xk, lab = G['make_stocks'](11)


def purity(labels):
    return sum(np.bincount(lab[labels == j]).max() for j in np.unique(labels)) / len(lab)


res = {}
for n in (10, 50, 200):
    km = KMeans(3, n_init=n, random_state=0).fit(Xk)
    res[n] = (round(float(km.inertia_), 2), round(purity(km.labels_), 4))
note(f"l16 s5 KMeans(3, n_init=n, random_state=0) raw: {res}")
ok(res[10] == (842.33, 0.75) and res[200] == (842.15, 0.7333), "l16 s5: n_init=10 stops at 842.33 (purity 0.75); n_init=200 reaches 842.15 (purity 0.7333)")
ok(res[50] == (842.33, 0.75), "l16 s5: n_init=50, random_state=0 still stops at 842.33, as the fix pass says")


def lloyd(X, C):
    prev = None
    while True:
        l = ((X[:, None] - C[None]) ** 2).sum(2).argmin(1)
        if prev is not None and (l == prev).all():
            return l, float(((X - C[l]) ** 2).sum())
        C = np.array([X[l == j].mean(0) if (l == j).any() else C[j] for j in range(len(C))]); prev = l


rng = np.random.default_rng(0); stops = {}
for _ in range(300 if PYO else 3000):                     # route 2: the reader's own loop from random rows
    l, w = lloyd(Xk, Xk[rng.choice(60, 3, replace=False)])
    key = round(w, 2); stops.setdefault(key, [0, round(purity(l), 4)]); stops[key][0] += 1
low = sorted(stops)[:4]
note(f"l16 s5 own Lloyd loop, random starts: lowest stops {[(k, stops[k]) for k in low]} of {len(stops)} distinct")
ok(low[0] == 842.15 and stops[842.15][1] == 0.7333 and 842.33 in stops and stops[842.33][1] == 0.75, "l16 s5: 842.15 (purity 0.7333) is the lowest stop of the reader's loop and 842.33 (purity 0.75) is a local stop")
# is 842.15 a minimum no single move improves? (a check Lloyd's loop does not make)
kb = KMeans(3, n_init=200, random_state=0).fit(Xk); lb = kb.labels_.copy(); best = float(kb.inertia_); improved = False
for i in range(60):
    for j in range(3):
        if j != lb[i]:
            l2 = lb.copy(); l2[i] = j
            if all((l2 == q).any() for q in range(3)):
                w = sum(float(((Xk[l2 == q] - Xk[l2 == q].mean(0)) ** 2).sum()) for q in range(3))
                improved |= w < best - 1e-9
ok(not improved, "l16 s5: no single share moved to another group lowers 842.15")
if not PYO:
    hit = [round(float(KMeans(3, n_init=10, random_state=r).fit(Xk).inertia_), 2) for r in range(40)]
    n15 = hit.count(842.15)
    note(f"l16 s5 KMeans(3, n_init=10, random_state=r), r = 0..39: {n15} reach 842.15, {hit.count(842.33)} stop at 842.33, others {sorted(set(hit) - {842.15, 842.33})}")
    if n15:
        finding(f"l16 s5: the screen's call `KMeans(3, n_init=10)` names no random_state; with ten starts {n15} of 40 seeds already reach 842.15 (purity 0.73), so 'more starts lower it from 842.33 to 842.15' is the seed-0 run")
km = KMeans(3, n_init=10, random_state=0).fit(StandardScaler().fit_transform(Xk))
ok(purity(km.labels_) == 1.0, "l16 s5: after StandardScaler purity is 1.0")
ok(abs(Xk[:, 1].std() - 13.04) < 0.005 and abs(Xk[:, 0].std() - 0.336) < 0.0005, "l16 s5: sds 13.04 and 0.336 (key option, unchanged)")
# best inertia never rises with k (six shares, every grouping)
import itertools
best = {}
for labs in itertools.product(range(6), repeat=6):
    k = len(set(labs))
    w = sum(sum((x - F(sum(g), len(g))) ** 2 for x in g) for g in ([S6[i] for i in range(6) if labs[i] == j] for j in set(labs)))
    best[k] = min(best.get(k, w), w)
ok([best[k] for k in range(1, 7)] == sorted((best[k] for k in range(1, 7)), reverse=True) and best[6] == 0 and [best[k] for k in (1, 2, 3, 4)] == [790, 64, 10, 4],
   f"l16 summary: best inertia by exhaustive search {[float(best[k]) for k in range(1, 7)]} never rises, 0 at one row each")
ok(58 < 64 and 58 > best[3], "l16: one k = 3 run (58) sits above the best k = 3 (10): a single run is not the best inertia")

# ================================================================ l17
W1 = np.array([[1, 2], [0, 1]]); w2v = np.array([3, -1])
q2 = wrongs(L17['quiz'][1]['widget'])
ok((w2v @ W1).tolist() == [3, 5] and (W1 @ w2v).tolist() == [1, -1] and [3 * 1 + (-1) * 0, 3 * 2 + (-1) * 1] == [3, 5] and [1 * 3 + 2 * (-1), 0 * 3 + 1 * (-1)] == [1, -1],
   "l17 q2: w2 W1 = (3, 5); W1 w2 = (1, -1) (NumPy and by hand)")
ok(L17['quiz'][1]['widget']['answer'] == 5 and q2['order']['value'] == -1 and q2['dropped']['value'] == 6 == 3 * 2 and q2['first']['value'] == 3, "l17 q2: order -1, dropped 6, first 3, all distinct from 5")
# s0: 0.75 is the ceiling of any line on the four corners; logistic regression itself scores 0.5
C4 = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], float); yx = np.array([0, 1, 1, 0])
rng = np.random.default_rng(3); bestline = 0
for _ in range(20000):
    a, b, c0 = rng.normal(size=3)
    bestline = max(bestline, ((C4 @ [a, b] + c0 > 0).astype(int) == yx).mean())
lr = LogisticRegression().fit(C4, yx)
ok(bestline == 0.75 and np.abs(lr.coef_).max() < 1e-6, f"l17 s0: best of 20,000 random lines 0.75; LogisticRegression has weights 0 and scores {lr.score(C4, yx)}")
# s8: the rings need no scaler
Xr, yr = G['make_rings'](300, 7); Xr2, yr2 = G['make_rings'](300, 8)
ok(np.round(Xr.std(0), 2).tolist() == [1.2, 1.17], f"l17 s8: ring feature sds {np.round(Xr.std(0), 2).tolist()}")
# s9: the noise table, this runtime
Xn, yn = G['make_noise'](300, 4); Xn2, yn2 = G['make_noise'](300, 5)
base = max(yn2.mean(), 1 - yn2.mean())
tab = L17['screens'][9]['canvas']['params']['rows']
mine = []
for s in (0, 1, 2):
    m = MLPClassifier(hidden_layer_sizes=(8,), solver="lbfgs", alpha=0.01, random_state=s, max_iter=500).fit(Xn, yn)
    mine.append((int(round(m.score(Xn, yn) * 300)), int(round(m.score(Xn2, yn2) * 300))))
shown = [(int(round(float(r[1]) * 300)), int(round(float(r[2]) * 300))) for r in tab]
note(f"l17 s9 noise table rows right of 300 (training, test), seeds 0..2: this runtime {mine}; lesson table {shown}; base rate {base:.4f} = {int(round(base * 300))} rows")
ok(int(round(base * 300)) == 165 and max(t for _, t in shown) - 165 == 2, "l17 s9 key: the table's best test score, 167 rows, is two rows above the base rate's 165")
moves = [abs(a[1] - b[1]) for a, b in zip(mine, shown)]
if PYO:
    ok(mine == shown, "l17 s9: Pyodide reproduces the lesson's table exactly")
else:
    ok(max(moves) <= 4, f"l17 s9: CPython test scores differ from the table by {moves} rows: 'up to four rows in 300' holds for this pair of runtimes")
    ok(all(t - 165 <= 5 for _, t in mine), f"l17 s9: in CPython the best test score is {max(t for _, t in mine) - 165} rows above the base rate ({(max(t for _, t in mine) - 165) / 300 / math.sqrt(base * (1 - base) / 300):.2f} standard errors): the conclusion holds")
    trm = [abs(a[0] - b[0]) for a, b in zip(mine, shown)]
    note(f"l17 s9: CPython training scores differ from the table by {trm} rows")

# ================================================================ l18
ok(SplineTransformer(n_knots=5, degree=3).fit_transform(np.linspace(0, 1, 50)[:, None]).shape[1] == 7 == 3 + 4, "l18 s3: 5 knots, 3 interior, 7 columns")
w3 = wrongs(L18['screens'][3]['widget'])
vals = [L18['screens'][3]['widget']['answer']] + [w['value'] for w in w3.values()]
ok(w3['interior']['value'] == 3 and len(set(vals)) == len(vals), f"l18 s3: interior 3; values distinct {vals}")
x, y = G['make_impact'](200, 21); x2, y2 = G['make_impact'](200, 22); X1, X2 = x[:, None], x2[:, None]
grid = np.linspace(x.min(), x.max(), 400)[:, None]
fit = {a: make_pipeline(SplineTransformer(n_knots=40, degree=3), Ridge(alpha=a)).fit(X1, y) for a in (0.001, 1, 1e6)}
ols40 = make_pipeline(SplineTransformer(n_knots=40, degree=3), LinearRegression()).fit(X1, y)
ols5 = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(X1, y)
ok(round(fit[1].score(X2, y2), 4) == 0.8868, "l18 q3: 40 knots, ridge penalty 1: test R2 0.8868 (pipeline)")
B = SplineTransformer(n_knots=40, degree=3).fit(X1); Bt = B.transform(X1); mu = Bt.mean(0)
coef = np.linalg.solve((Bt - mu).T @ (Bt - mu) + np.eye(Bt.shape[1]), (Bt - mu).T @ (y - y.mean()))
pred = (B.transform(X2) - mu) @ coef + y.mean()
ok(round(1 - ((y2 - pred) ** 2).sum() / ((y2 - y2.mean()) ** 2).sum(), 4) == 0.8868, "l18 q3: 0.8868 again from the normal equations (centred columns, penalty 1)")
rough = lambda m: float((np.diff(m.predict(grid), 2) ** 2).sum())
p0, p1 = ols40.predict(grid), fit[1].predict(grid)
ok(rough(fit[1]) < rough(ols40) and p1.std() < p0.std(), f"l18 q3 'wiggles less, flattened towards its mean': squared second differences {rough(ols40):.2f} to {rough(fit[1]):.2f}; sd of the curve {p0.std():.1f} to {p1.std():.1f}")
ends = [round(float(m.predict([[s]])[0]), 1) for m in (fit[1], ols5) for s in (1, 40)]
ok(ends == [12.3, 61.0, 9.8, 62.5], f"l18 q3: penalised 40-knot fit at 1% and 40%: {ends[:2]}; 5-knot fit: {ends[2:]} (lifted at the low end, pulled down at the high end)")
flat = fit[1e6].predict(grid)
ok(np.ptp(flat) < 0.01 and abs(flat.mean() - y.mean()) < 0.01, f"l18 q3 option c: a penalty of 1e6 gives a constant {flat.mean():.2f}, the mean of y {y.mean():.2f}")
ok(np.abs(fit[0.001].predict(grid) - p0).max() < 0.5, f"l18 q3 option c: a penalty of 0.001 moves the curve by at most {np.abs(fit[0.001].predict(grid) - p0).max():.2f} bp on a curve that runs from {p0.min():.0f} to {p0.max():.0f} bp")
# the same limit on the lesson's other basis (a line plus hinges): the rule is not a property of B-splines
knots = np.quantile(x, np.linspace(0.05, 0.95, 12))
H = np.c_[x, np.maximum(0, x[:, None] - knots[None])]
hr = Ridge(alpha=1e12).fit(H, y)
ok(np.ptp(hr.predict(H)) < 0.01, "l18 q3: a huge ridge penalty on a hinge basis also gives the flat line at the mean")
try:
    from scipy.interpolate import make_smoothing_spline
    o = np.argsort(x); xs, ysort = x[o], y[o]
    keep = np.r_[True, np.diff(xs) > 0]
    sm = make_smoothing_spline(xs[keep], ysort[keep], lam=1e8)       # larger values lose the fit to rounding
    line = np.polyfit(xs[keep], ysort[keep], 1)
    ok(np.abs(sm(grid[:, 0]) - np.polyval(line, grid[:, 0])).max() < 0.05, f"l18 q3 'a trend is not flattened': a smoothing spline with a curvature penalty of 1e8 is the least-squares line to 0.05 bp, slope {line[0]:.3f} (ISLP 7.5.1)")
except ImportError:
    note("l18 q3: scipy.interpolate.make_smoothing_spline not in this build; smoothing-spline limit checked in CPython only")
# q2: what the lesson's own spline does beyond the data
me = make_pipeline(SplineTransformer(n_knots=5, degree=3, extrapolation="linear"), LinearRegression()).fit(X1, y)
out = me.predict(np.array([[51.0], [52.0], [53.0], [54.0], [55.0]]))
ok(round(float(out[-1]), 2) == 85.13 and round(10 * math.sqrt(55), 2) == 74.16, "l18 q2: 85.13 at 55 against a truth of 74.16")
if np.abs(np.diff(out, 2)).max() < 1e-8:
    finding("l18 q2: the lesson's spline with extrapolation=\"linear\" is already exactly linear beyond its boundary knots (second differences 0 at 51..55), so 'a natural spline goes further and is forced to be linear beyond its boundary knots' names no difference")
edge = np.array([[x.max() - 0.2], [x.max() - 0.1], [x.max()]])
note(f"l18 q2: curvature of the lesson's spline just inside the upper boundary (second difference at spacing 0.1): {float(np.diff(me.predict(edge), 2)[0]):.5f}; a natural spline has 0 there")

# ================================================================ l19
tabrows = {r[0]: [float(v) for v in r[1:]] for r in L19['screens'][5]['canvas']['params']['rows']}
ok(tabrows['wide'] == [0.9233, 0.89, 0.92, 0.9067, 0.9167] and 0.9067 < 0.92 < 0.9233, "l19 s3 option c: the network's 0.9067 is behind logistic regression (0.9233) and the SVM (0.92)")
order = ['logistic', 'knn', 'svm', 'net', 'additive']


def wide_run(pairs):
    out = []
    for a, b in pairs:
        Xa, ya = G['make_wide'](60, a); Xb, yb = G['make_wide'](300, b)
        out.append([G['LEARNERS'][k]().fit(Xa, ya).score(Xb, yb) for k in order])
    return np.array(out)


def describe(tag, R):
    mean = R.mean(0)
    last = int((R[:, 1][:, None] < np.delete(R, 1, 1)).all(1).sum())
    below = int((R[:, 1] < R[:, 0]).sum())
    d = R[:, 4] - R[:, 0]
    logbest = int((R[:, 0] >= R.max(1)).sum())
    note(f"l19 s3 {tag}: means {dict(zip(order, np.round(mean, 4).tolist()))}; k-NN strictly last in {last} of {len(R)}, below logistic in {below}; additive minus logistic {d.mean():+.4f} (se {d.std(ddof=1) / math.sqrt(len(R)):.4f}); logistic best or tied best in {logbest}")
    return mean, last, below, d


n40 = 10 if PYO else 40
R = wide_run([(100 + 2 * i, 101 + 2 * i) for i in range(n40)])
mean, last, below, d = describe(f"fixer's seed pairs (100+2i, 101+2i), first {n40}", R)
if not PYO:
    ok(round(mean[1], 2) == 0.86 and last == 35 and below == 40, "l19 s3: over the fixer's 40 pairs k-NN averages 0.86, is strictly last in 35 and below logistic regression in all 40")
    oth = np.delete(mean, 1)
    ok(0.90 <= oth.min() and oth.max() <= 0.93, f"l19 s3: the other four average {np.round(oth, 4).tolist()}, between 0.90 and 0.93")
    R2 = wide_run([(5000 + 2 * i, 5001 + 2 * i) for i in range(40)])
    m2, l2, b2, d2 = describe("reader's own 40 pairs (5000+2i, 5001+2i)", R2)
    ok(m2[1] == m2.min() and l2 >= 30 and b2 >= 38, f"l19 s3 as a rule: on 40 fresh pairs k-NN is still the lowest mean ({m2[1]:.4f}), strictly last in {l2}")
    o2 = np.delete(m2, 1)
    ok(0.895 <= o2.min() and o2.max() <= 0.935, f"l19 s3 as a rule: the other four average {np.round(o2, 4).tolist()} on the fresh pairs")
    both = np.r_[d, d2]
    if both.mean() / (both.std(ddof=1) / math.sqrt(len(both))) > 2:
        finding(f"l19: over 80 seed pairs the additive model beats logistic regression on the wide problem by {both.mean():.4f} (t = {both.mean() / (both.std(ddof=1) / math.sqrt(len(both))):.1f}); screens[5].explain still says 'Bias wins where the truth is simple or the rows are few'")
else:
    note("l19 s3: Pyodide ran the first 10 of the fixer's pairs; compare this NOTE's first 10 with CPython's by running recompute.py with PAIRS10=1")
if os.environ.get('PAIRS10') or PYO:
    note(f"l19 s3 first 10 pairs, every score: {np.round(wide_run([(100 + 2 * i, 101 + 2 * i) for i in range(10)]), 4).tolist()}")
# review r-few-rows
ok(SplineTransformer(n_knots=10).fit_transform(np.random.default_rng(0).normal(size=(80, 25))).shape[1] == 300 == 25 * (10 + 3 - 1), "review r-few-rows: 25 features, 10 knots: 300 spline columns (transformer and K + degree - 1)")
ok(25 * 64 + 64 + 64 + 1 == 1729, "review r-few-rows option c: a 64-unit network on 25 features has 1,729 parameters ('about 1,700', unchanged)")

# ================================================================ homework h-pick-learner
it = next(i for i in HW['items'] if i['id'] == 'h-pick-learner')
val = [0.61, 0.61, 0.60, 0.59, 0.58]; test = [0.59, 0.60, 0.62, 0.58, 0.61]; b, n = 0.56, 400
ok(all(str(v) in it['prose'] or ('%.2f' % v) in it['prose'] for v in val + test + [b]) and '400 test rows' in it['prose'] and '200 rows' in it['prose'], "h-pick-learner: the reader's transcription of the prose matches the file")
pick = val.index(max(val))                                 # first maximum: the simpler of the tied pair
t = lambda h, base=b, rows=n: (h - base) / math.sqrt(base * (1 - base) / rows)
tf = lambda h, base, rows: (F(h) - F(base)) ** 2 / (F(base) * (1 - F(base)) / rows)        # t squared, exact
ans = it['widget']['answer']; tol = it['widget']['tol']['abs']
ok(pick == 0 and abs(t(test[pick]) - ans) <= tol and round(t(test[pick]), 2) == ans, f"h-pick-learner: first learner, t = {t(test[0]):.4f}, key {ans}")
ok(abs(math.sqrt(tf('0.59', '0.56', 400)) - t(0.59)) < 1e-12 and tf('0.59', '0.56', 400) == F(225, 154), f"h-pick-learner: t squared is exactly 225/154, t = {math.sqrt(225 / 154):.4f}")
slips = {'besttest': t(max(test)), 'tie': t(test[1]), 'coin': t(test[0], 0.5), 'valscore': t(val[0])}
hw = wrongs(it['widget'])
for k, v in slips.items():
    ok(abs(v - hw[k]['value']) <= hw[k]['tol']['abs'] and round(v, 2) == hw[k]['value'], f"h-pick-learner wrong '{k}': {v:.4f}, stored {hw[k]['value']}")
bands = [(ans - tol, ans + tol)] + [(w['value'] - w['tol']['abs'], w['value'] + w['tol']['abs']) for w in hw.values()]
ok(all(a[1] < b2[0] or b2[1] < a[0] for i, a in enumerate(bands) for b2 in bands[i + 1:]), "h-pick-learner: no two bands meet")
ex = it['explain']['text']
ok(round(math.sqrt(b * (1 - b) / n), 4) == 0.0248 and '0.03/0.0248' in ex, "h-pick-learner explain: standard error 0.0248")
other = {
    "standard error from the learner's own 0.59": (0.59 - b) / math.sqrt(0.59 * 0.41 / n),
    'standard error rounded to 0.025': 0.03 / 0.025,
    "the explanation's own quotient 0.03/0.0248": 0.03 / 0.0248,
    'validation score on its own 200 rows': (0.61 - b) / math.sqrt(b * (1 - b) / 200),
    'most complex learner (0.58 on validation, 0.61 on test)': t(0.61),
    'average of the tied pair': t(0.595),
}
for k, v in other.items():
    inside = [i for i, (lo, hi) in enumerate(bands) if lo <= round(v, 2) <= hi]
    where = 'marked right' if inside == [0] else ('lands on a wrong entry' if inside else 'generic line')
    note(f"h-pick-learner other route, {k}: {v:.4f}, typed {round(v, 2):.2f}: {where}")
    if k.startswith('standard error') and inside != [0]:
        finding(f"h-pick-learner: {k} gives {round(v, 2):.2f}, outside the key's band {ans} +/- {tol}; it gets the generic line")
note("h-pick-learner: 'valscore' and 'most complex learner' both equal t(0.61) = %.4f: the stored 2.01 fires for either slip, with the valscore line" % t(0.61))

print(f"{NOK - len(BAD)} of {NOK} checks pass; {len(BAD)} BAD; {NFIND} FINDING rows")
if __name__ == '__main__':
    sys.exit(1 if BAD else 0)
