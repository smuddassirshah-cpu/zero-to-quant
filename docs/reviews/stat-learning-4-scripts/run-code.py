"""Second read, stat-learning L4: every code screen and item run in CPython under the engine's comparison rule
(math.isclose rel 1e-9, abs 1e-12, or the case's own tol; element by element for lists, tuples and dicts).
For each: the author's solution passes every hidden test, the starter fails, the reader's own solution passes,
and each wrong solution a learner might write is run. A wrong solution that PASSES is listed as 'PASSES';
those marked expected=True are harmless (same result by another route) and do not count against the exit code.
Run from the repo root with the scratchpad venv python. Exit 0 when author, starter and reader rows all hold."""
import json, math, os, sys, warnings
warnings.filterwarnings("ignore")
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'app', 'content', 'courses', 'stat-learning')
bad = 0; passing = []


def flat(v):
    return v.tolist() if hasattr(v, 'tolist') else v


def close(x, y, tol):
    x, y = flat(x), flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k], tol) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, str) and not isinstance(y, str):
        return False
    try:
        rt, at = tol if tol else (1e-9, 1e-12)
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return x == y


def run(w, src):
    """Failed test count for src against w's hidden tests (prelude first; an exception is a failure)."""
    fails = 0
    g0 = {}
    exec(w.get('prelude', ''), g0)
    try:
        exec(src, g0)
    except Exception:
        return len(w['tests'])
    for t in w['tests']:
        try:
            got = eval(t['call'], g0); want = eval(t['expect'], g0)
            tol = None
            if isinstance(t.get('tol'), dict):
                tol = (t['tol'].get('rel', 0) or 0, t['tol'].get('abs', 0) or 0)
            ok = close(got, want, tol) if t.get('compare') == 'isclose' else bool(flat(got) == flat(want))
        except Exception:
            ok = False
        fails += 0 if ok else 1
    return fails


def widget(fname, where):
    d = json.load(open(os.path.join(ROOT, fname)))
    return (d.get('screens') or d.get('items'))[where]['widget']


def report(name, w, own, mutants):
    global bad
    for label, ok in [('author solution passes', run(w, w['solution']) == 0), ('starter fails', run(w, w['starter']) > 0),
                      ('reader solution passes', run(w, own) == 0)]:
        print(('ok  ' if ok else 'FAIL') + f' {name}: {label}'); bad += 0 if ok else 1
    for label, (src, expected) in mutants.items():
        f = run(w, src)
        if f:
            print(f'ok   {name}: wrong solution caught ({f} of {len(w["tests"])} fail): {label}')
        else:
            print(f'PASSES {name}: {label}' + (' [harmless]' if expected else ''))
            if not expected:
                passing.append(f'{name}: {label}')


# ------------------------------------------------------------ l15 s3
w = widget('l15-widest-street.json', 3)
own = '''
import math
def margin_width(w, b):
    return 1 / math.sqrt(sum(float(c) ** 2 for c in w))
def support_points(X, y, w, b, tol=1e-6):
    out = []
    for i, (row, lab) in enumerate(zip(X, y)):
        v = sum(c * x for c, x in zip(w, row)) + b
        if abs((1 if lab == 1 else -1) * v - 1) <= tol:
            out.append(i)
    return out
'''
tail = '''
def support_points(X, y, w, b, tol=1e-6):
    import numpy as np
    s = np.where(np.asarray(y) == 1, 1, -1); v = s * (np.asarray(X, float) @ np.asarray(w, float) + b)
    return [int(i) for i in np.flatnonzero(np.abs(v - 1) <= tol)]
'''
head = 'import numpy as np\ndef margin_width(w, b):\n    return 1 / np.linalg.norm(w)\n'
report('l15 s3', w, own, {
    'returns the whole street 2/|w|': ('import numpy as np\ndef margin_width(w, b):\n    return 2 / np.linalg.norm(w)\n' + tail, False),
    'returns |w|': ('import numpy as np\ndef margin_width(w, b):\n    return np.linalg.norm(w)\n' + tail, False),
    'distance of the origin |b|/|w|': ('import numpy as np\ndef margin_width(w, b):\n    return abs(b) / np.linalg.norm(w)\n' + tail, False),
    'support: labels 0/1 used as signs': (head + 'def support_points(X, y, w, b, tol=1e-6):\n    v = np.asarray(y) * (np.asarray(X, float) @ np.asarray(w, float) + b)\n    return [int(i) for i in np.flatnonzero(np.abs(v - 1) <= tol)]\n', False),
    'support: no sign at all (|w.x+b| = 1)': (head + 'def support_points(X, y, w, b, tol=1e-6):\n    v = np.abs(np.asarray(X, float) @ np.asarray(w, float) + b)\n    return [int(i) for i in np.flatnonzero(np.abs(v - 1) <= tol)]\n', False),
    'support: on or inside the edge (v <= 1 + tol)': (head + 'def support_points(X, y, w, b, tol=1e-6):\n    s = np.where(np.asarray(y) == 1, 1, -1); v = s * (np.asarray(X, float) @ np.asarray(w, float) + b)\n    return [int(i) for i in np.flatnonzero(v <= 1 + tol)]\n', False),
    'support: tol ignored (1e-9)': (head + 'def support_points(X, y, w, b, tol=1e-6):\n    s = np.where(np.asarray(y) == 1, 1, -1); v = s * (np.asarray(X, float) @ np.asarray(w, float) + b)\n    return [int(i) for i in np.flatnonzero(np.abs(v - 1) <= 1e-9)]\n', False),
})

# ------------------------------------------------------------ l15 s6
w = widget('l15-widest-street.json', 6)
T = '''
from sklearn.svm import SVC
def svm_report(X_train, y_train, X_test, y_test, C, gamma=None):
    %s
'''
own = T % '''kw = dict(kernel="linear") if gamma is None else dict(kernel="rbf", gamma=gamma)
    m = SVC(C=C, **kw).fit(X_train, y_train)
    acc = lambda X, y: round(float((m.predict(X) == y).mean()), 4)
    return (int(m.n_support_.sum()), acc(X_train, y_train), acc(X_test, y_test))'''
report('l15 s6', w, own, {
    'scaler fitted on the training rows first (pipeline)': ('from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\n' + T % '''m = make_pipeline(StandardScaler(), SVC(kernel="linear", C=C) if gamma is None else SVC(kernel="rbf", C=C, gamma=gamma)).fit(X_train, y_train)
    return (len(m[-1].support_), round(m.score(X_train, y_train), 4), round(m.score(X_test, y_test), 4))''', False),
    'gamma ignored (always scikit-learn default)': (T % '''m = SVC(kernel="linear" if gamma is None else "rbf", C=C).fit(X_train, y_train)
    return (len(m.support_), round(m.score(X_train, y_train), 4), round(m.score(X_test, y_test), 4))''', False),
    'C ignored': (T % '''m = (SVC(kernel="linear") if gamma is None else SVC(kernel="rbf", gamma=gamma)).fit(X_train, y_train)
    return (len(m.support_), round(m.score(X_train, y_train), 4), round(m.score(X_test, y_test), 4))''', False),
    'fitted on the test rows': (T % '''m = (SVC(kernel="linear", C=C) if gamma is None else SVC(kernel="rbf", C=C, gamma=gamma)).fit(X_test, y_test)
    return (len(m.support_), round(m.score(X_train, y_train), 4), round(m.score(X_test, y_test), 4))''', False),
    'accuracies swapped': (T % '''m = (SVC(kernel="linear", C=C) if gamma is None else SVC(kernel="rbf", C=C, gamma=gamma)).fit(X_train, y_train)
    return (len(m.support_), round(m.score(X_test, y_test), 4), round(m.score(X_train, y_train), 4))''', False),
    'no rounding': (T % '''m = (SVC(kernel="linear", C=C) if gamma is None else SVC(kernel="rbf", C=C, gamma=gamma)).fit(X_train, y_train)
    return (len(m.support_), m.score(X_train, y_train), m.score(X_test, y_test))''', False),
})

# ------------------------------------------------------------ l15 s8
w = widget('l15-widest-street.json', 8)
T = '''
from sklearn.svm import SVC
def pick_gamma(X, y, C, gammas=(0.01, 0.1, 1, 10), n_val=100):
    %s
'''
own = T % '''n = len(X) - n_val
    scores = {g: round(SVC(kernel="rbf", C=C, gamma=g).fit(X[:n], y[:n]).score(X[n:], y[n:]), 4) for g in gammas}
    top = max(scores.values())
    g = min(g for g in gammas if scores[g] == top)
    return (g, top)'''
loop = '''best, ba = None, -1.0
    for g in %s:
        acc = round(SVC(kernel="rbf", C=C, gamma=g).fit(%s).score(%s), 4)
        if acc %s ba:
            best, ba = g, acc
    return (best, ba)'''
tr, va = 'X[:-n_val], y[:-n_val]', 'X[-n_val:], y[-n_val:]'
report('l15 s8', w, own, {
    'tie to the larger gamma (>=)': (T % (loop % ('sorted(gammas)', tr, va, '>=')), False),
    'no sort (order as given)': (T % (loop % ('gammas', tr, va, '>')), False),
    'validates on the first n_val rows': (T % (loop % ('sorted(gammas)', 'X[n_val:], y[n_val:]', 'X[:n_val], y[:n_val]', '>')), False),
    'fits on ALL rows, scores the last n_val (validation rows seen in fitting)': (T % (loop % ('sorted(gammas)', 'X, y', va, '>')), False),
    'scores on the training part (no held-out rows)': (T % (loop % ('sorted(gammas)', tr, tr, '>')), False),
    'tunes on the TEST rows (globals Xr_te, yr_te)': (T % (loop % ('sorted(gammas)', 'X, y', 'Xr_te, yr_te', '>')), False),
    'scaler fitted on all rows before the split': ('from sklearn.preprocessing import StandardScaler\n' + T % ('X = StandardScaler().fit_transform(X)\n    ' + loop % ('sorted(gammas)', tr, va, '>')), False),
})

# ------------------------------------------------------------ l16 s4
w = widget('l16-groups-nobody-labelled.json', 4)
own = '''
import numpy as np
def kmeans_step(X, centres):
    X = np.array(X, dtype=float); C = np.array(centres, dtype=float)
    labels = np.array([int(np.argmin([np.sum((x - c) ** 2) for c in C])) for x in X])
    new = np.array([X[labels == j].mean(axis=0) if np.any(labels == j) else C[j] for j in range(len(C))])
    return labels, new
def inertia(X, labels, centres):
    X = np.array(X, dtype=float); C = np.array(centres, dtype=float)
    return float(sum(np.sum((x - C[l]) ** 2) for x, l in zip(X, labels)))
'''
K = '''
import numpy as np
def kmeans_step(X, centres):
    X = np.asarray(X, float); C = np.asarray(centres, float)
    d = %s
    labels = %s
    new = C.copy()
    for j in range(len(C)):
        %s
    return labels, new
def inertia(X, labels, centres):
    X = np.asarray(X, float); C = np.asarray(centres, float)
    return %s
'''
d2, am = '((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)', 'd.argmin(axis=1)'
upd = 'if (labels == j).any():\n            new[j] = X[labels == j].mean(axis=0)'
ine = 'float(((X - C[np.asarray(labels)]) ** 2).sum())'
report('l16 s4', w, own, {
    'no empty-centre guard (nan)': (K % (d2, am, 'new[j] = X[labels == j].mean(axis=0)', ine), False),
    'empty centre moved to the overall mean': (K % (d2, am, 'new[j] = X[labels == j].mean(axis=0) if (labels == j).any() else X.mean(axis=0)', ine), False),
    'ties to the higher index': (K % (d2, 'len(C) - 1 - d[:, ::-1].argmin(axis=1)', upd, ine), False),
    'median update': (K % (d2, am, 'if (labels == j).any():\n            new[j] = np.median(X[labels == j], axis=0)', ine), False),
    'Manhattan distance in the assign step': (K % ('np.abs(X[:, None, :] - C[None, :, :]).sum(axis=2)', am, upd, ine), False),
    'inertia: plain distances': (K % (d2, am, upd, 'float(np.sqrt(((X - C[np.asarray(labels)]) ** 2).sum(axis=1)).sum())'), False),
    'inertia: mean not sum': (K % (d2, am, upd, 'float(((X - C[np.asarray(labels)]) ** 2).sum(axis=1).mean())'), False),
    'inertia: about the overall mean': (K % (d2, am, upd, 'float(((X - X.mean(axis=0)) ** 2).sum())'), False),
})

# ------------------------------------------------------------ l16 s8
w = widget('l16-groups-nobody-labelled.json', 8)
H = '''
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
'''
CR = H + '''
def cluster_report(X, k):
    %s
def merge_heights(D, method):
    %s
'''
crs = 'Z = StandardScaler().fit_transform(X)\n    m = KMeans(k, n_init=10, random_state=0).fit(Z)\n    return (round(float(m.inertia_), 2), sorted(np.bincount(m.labels_).tolist()))'
mhs = 'return [round(float(h), 4) for h in linkage(squareform(np.asarray(D, float)), method)[:, 2]]'
own = H + '''
def cluster_report(X, k):
    X = np.asarray(X, float); Z = (X - X.mean(0)) / X.std(0)
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Z)
    sizes = sorted(int((m.labels_ == j).sum()) for j in range(k))
    own_inertia = float(((Z - m.cluster_centers_[m.labels_]) ** 2).sum())
    return (round(own_inertia, 2), sizes)
def merge_heights(D, method):
    D = np.asarray(D, float); groups = [[i] for i in range(len(D))]; out = []
    agg = {'single': min, 'complete': max, 'average': lambda v: sum(v) / len(v)}[method]
    while len(groups) > 1:
        best = None
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                h = agg([D[a][b] for a in groups[i] for b in groups[j]])
                if best is None or h < best[0]:
                    best = (h, i, j)
        h, i, j = best; out.append(round(float(h), 4)); groups[i] = groups[i] + groups[j]; del groups[j]
    return out
'''
report('l16 s8', w, own, {
    'no scaling': (CR % ('m = KMeans(k, n_init=10, random_state=0).fit(X)\n    return (round(float(m.inertia_), 2), sorted(np.bincount(m.labels_).tolist()))', mhs), False),
    'wrong random_state (1)': (CR % (crs.replace('random_state=0', 'random_state=1'), mhs), False),
    'wrong random_state (42)': (CR % (crs.replace('random_state=0', 'random_state=42'), mhs), False),
    'n_init=1 (one start)': (CR % (crs.replace('n_init=10', 'n_init=1'), mhs), False),
    'group sizes in label order, not sorted (labels permute)': (CR % (crs.replace('sorted(np.bincount(m.labels_).tolist())', 'np.bincount(m.labels_).tolist()'), mhs), False),
    'sizes largest first': (CR % (crs.replace('sorted(np.bincount(m.labels_).tolist())', 'sorted(np.bincount(m.labels_).tolist(), reverse=True)'), mhs), False),
    'linkage on the square matrix (rows read as points)': (CR % (crs, 'return [round(float(h), 4) for h in linkage(np.asarray(D, float), method)[:, 2]]'), False),
    'method ignored (always single)': (CR % (crs, 'return [round(float(h), 4) for h in linkage(squareform(np.asarray(D, float)), "single")[:, 2]]'), False),
})

# ------------------------------------------------------------ l17 s4
w = widget('l17-a-small-network.json', 4)
own = '''
import math
def forward(X, W1, b1, W2, b2):
    out = []
    for x in X:
        h = [max(0.0, sum(wi * xi for wi, xi in zip(row, x)) + b) for row, b in zip(W1, b1)]
        z = sum(a * b for a, b in zip(W2, h)) + b2
        out.append(1 / (1 + math.exp(-z)))
    import numpy as np
    return np.array(out)
def n_params(sizes):
    total = 0
    for i in range(len(sizes) - 1):
        total += sizes[i] * sizes[i + 1] + sizes[i + 1]
    return total
'''
FW = '''
import numpy as np
def forward(X, W1, b1, W2, b2):
    X = np.asarray(X, float)
    H = %s
    z = %s
    return %s
def n_params(sizes):
    return %s
'''
hh, zz, pp, nn = 'np.maximum(0, X @ np.asarray(W1, float).T + np.asarray(b1, float))', 'H @ np.asarray(W2, float) + b2', '1 / (1 + np.exp(-z))', 'sum(a * b + b for a, b in zip(sizes[:-1], sizes[1:]))'
report('l17 s4', w, own, {
    'no ReLU': (FW % ('X @ np.asarray(W1, float).T + np.asarray(b1, float)', zz, pp, nn), False),
    'W1 not transposed': (FW % ('np.maximum(0, X @ np.asarray(W1, float) + np.asarray(b1, float))', zz, pp, nn), False),
    'hidden bias left out': (FW % ('np.maximum(0, X @ np.asarray(W1, float).T)', zz, pp, nn), False),
    'output bias left out': (FW % (hh, 'H @ np.asarray(W2, float)', pp, nn), False),
    'returns z, no logistic': (FW % (hh, zz, 'z', nn), False),
    'ReLU on the output too': (FW % (hh, 'np.maximum(0, H @ np.asarray(W2, float) + b2)', pp, nn), False),
    'count: weights only': (FW % (hh, zz, pp, 'sum(a * b for a, b in zip(sizes[:-1], sizes[1:]))'), False),
    'count: one bias per layer': (FW % (hh, zz, pp, 'sum(a * b + 1 for a, b in zip(sizes[:-1], sizes[1:]))'), False),
    'count: biases on the inputs too': (FW % (hh, zz, pp, 'sum(a * b for a, b in zip(sizes[:-1], sizes[1:])) + sum(sizes)'), False),
})

# ------------------------------------------------------------ l17 s7
w = widget('l17-a-small-network.json', 7)
own = '''
def gd_step(w1, w2, x, y, lr):
    relu = lambda v: v if v > 0 else 0.0
    pre = w1 * x
    yhat = w2 * relu(pre)
    dL_dy = yhat - y
    slope2 = dL_dy * relu(pre)
    slope1 = dL_dy * w2 * x if pre > 0 else 0.0
    n1 = w1 - lr * slope1; n2 = w2 - lr * slope2
    return (round(n1, 4), round(n2, 4), round(0.5 * (n2 * relu(n1 * x) - y) ** 2, 4))
'''
G = '''
def gd_step(w1, w2, x, y, lr):
    h = max(0.0, w1 * x); err = w2 * h - y
    %s
    return (round(w1, 4), round(w2, 4), round(loss, 4))
'''
report('l17 s7', w, own, {
    'updates w1 first, then uses the new w1 for the w2 slope': (G % 'g1 = err * w2 * (x if w1 * x > 0 else 0.0)\n    w1 = w1 - lr * g1\n    h = max(0.0, w1 * x); g2 = (w2 * h - y) * h\n    w2 = w2 - lr * g2\n    loss = 0.5 * (w2 * max(0.0, w1 * x) - y) ** 2', False),
    'updates w2 first, then uses the new w2 for the w1 slope': (G % 'g2 = err * h\n    w2 = w2 - lr * g2\n    g1 = (w2 * h - y) * w2 * (x if w1 * x > 0 else 0.0)\n    w1 = w1 - lr * g1\n    loss = 0.5 * (w2 * max(0.0, w1 * x) - y) ** 2', False),
    'ReLU slope always 1 (no dead-unit guard)': (G % 'g2 = err * h; g1 = err * w2 * x\n    w1, w2 = w1 - lr * g1, w2 - lr * g2\n    loss = 0.5 * (w2 * max(0.0, w1 * x) - y) ** 2', False),
    'loss before the step': (G % 'g2 = err * h; g1 = err * w2 * (x if w1 * x > 0 else 0.0)\n    loss = 0.5 * err ** 2\n    w1, w2 = w1 - lr * g1, w2 - lr * g2', False),
    'steps up the slope': (G % 'g2 = err * h; g1 = err * w2 * (x if w1 * x > 0 else 0.0)\n    w1, w2 = w1 + lr * g1, w2 + lr * g2\n    loss = 0.5 * (w2 * max(0.0, w1 * x) - y) ** 2', False),
    'w1 slope without w2': (G % 'g2 = err * h; g1 = err * (x if w1 * x > 0 else 0.0)\n    w1, w2 = w1 - lr * g1, w2 - lr * g2\n    loss = 0.5 * (w2 * max(0.0, w1 * x) - y) ** 2', False),
    'loss without the half': (G % 'g2 = err * h; g1 = err * w2 * (x if w1 * x > 0 else 0.0)\n    w1, w2 = w1 - lr * g1, w2 - lr * g2\n    loss = (w2 * max(0.0, w1 * x) - y) ** 2', False),
})

# ------------------------------------------------------------ l17 s8 (bands)
w = widget('l17-a-small-network.json', 8)
M = '''
from sklearn.neural_network import MLPClassifier
def mlp_width_report(widths, seed):
    out = []
    for h in widths:
        m = %s
        m.fit(%s)
        out.append(round(m.score(%s), 4))
    return out
'''
mk = 'MLPClassifier(hidden_layer_sizes=(h,), solver="lbfgs", alpha=0.01, random_state=seed, max_iter=500)'
own = '''
from sklearn.neural_network import MLPClassifier
def mlp_width_report(widths, seed):
    def one(h):
        net = MLPClassifier(hidden_layer_sizes=(h,), solver="lbfgs", alpha=0.01, max_iter=500, random_state=seed)
        net.fit(Xr_tr, yr_tr)
        return round(float((net.predict(Xr_te) == yr_te).mean()), 4)
    return [one(h) for h in widths]
'''
report('l17 s8', w, own, {
    'wrong random_state: seed ignored, always 0': (M % (mk.replace('random_state=seed', 'random_state=0'), 'Xr_tr, yr_tr', 'Xr_te, yr_te'), False),
    'wrong random_state: seed + 7': (M % (mk.replace('random_state=seed', 'random_state=seed + 7'), 'Xr_tr, yr_tr', 'Xr_te, yr_te'), False),
    'default alpha (0.0001)': (M % (mk.replace('alpha=0.01, ', ''), 'Xr_tr, yr_tr', 'Xr_te, yr_te'), False),
    'default solver (adam), max_iter=500': (M % (mk.replace('solver="lbfgs", ', ''), 'Xr_tr, yr_tr', 'Xr_te, yr_te'), False),
    'scaler fitted on train AND test rows together': ('import numpy as np\nfrom sklearn.preprocessing import StandardScaler\n_sc = StandardScaler().fit(np.vstack([Xr_tr, Xr_te]))\n' + M % (mk, '_sc.transform(Xr_tr), yr_tr', '_sc.transform(Xr_te), yr_te'), False),
    'scores the training rows': (M % (mk, 'Xr_tr, yr_tr', 'Xr_tr, yr_tr'), False),
    'fits on the test rows': (M % (mk, 'Xr_te, yr_te', 'Xr_te, yr_te'), False),
    'width ignored (always 8)': (M % (mk.replace('(h,)', '(8,)'), 'Xr_tr, yr_tr', 'Xr_te, yr_te'), False),
    'no rounding': (M.replace('round(m.score(%s), 4)', 'm.score(%s)') % (mk, 'Xr_tr, yr_tr', 'Xr_te, yr_te'), True),
})

# ------------------------------------------------------------ l18 s4
w = widget('l18-bending-the-line.json', 4)
own = '''
import numpy as np
def hinge_features(x, knots):
    x = np.array(x, dtype=float)
    cols = [x]
    for c in knots:
        cols.append(np.where(x > c, x - c, 0.0))
    return np.array(cols).T
def fit_linear_spline(x, y, knots):
    A = np.hstack([np.ones((len(x), 1)), hinge_features(x, knots)])
    return np.linalg.pinv(A) @ np.asarray(y, float)
'''
S4 = '''
import numpy as np
def hinge_features(x, knots):
    x = np.asarray(x, float)
    return %s
def fit_linear_spline(x, y, knots):
    H = hinge_features(x, knots)
    A = %s
    return np.linalg.lstsq(A, np.asarray(y, float), rcond=None)[0]
'''
hf, aa = 'np.column_stack([x] + [np.maximum(0, x - c) for c in knots])', 'np.column_stack([np.ones(len(H)), H])'
report('l18 s4', w, own, {
    'put hinge (c - x)+': (S4 % ('np.column_stack([x] + [np.maximum(0, c - x) for c in knots])', aa), False),
    'no x column': (S4 % ('np.column_stack([np.maximum(0, x - c) for c in knots])', aa), False),
    'no intercept column': (S4 % (hf, 'H'), False),
    'hinge not floored': (S4 % ('np.column_stack([x] + [x - c for c in knots])', aa), False),
    'step function (x > c) instead of a hinge': (S4 % ('np.column_stack([x] + [(x > c).astype(float) for c in knots])', aa), False),
})

# ------------------------------------------------------------ l18 s7
w = widget('l18-bending-the-line.json', 7)
I = 'from sklearn.linear_model import LinearRegression\nfrom sklearn.preprocessing import SplineTransformer, StandardScaler\nfrom sklearn.pipeline import make_pipeline\nimport numpy as np\n'
S7 = I + '''
def spline_r2(n_knots):
    m = make_pipeline(SplineTransformer(n_knots=%s, degree=3), LinearRegression())
    m.fit(%s)
    return %s
def additive_r2(interaction):
    Xa, ya = make_additive(300, 31, interaction)
    Xb, yb = make_additive(300, %s)
    lin = LinearRegression().fit(Xa, ya)
    add = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(%s)
    return %s
'''
r1, r2 = '(round(m.score(x_tr[:, None], y_tr), 4), round(m.score(x_te[:, None], y_te), 4))', '(round(lin.score(Xb, yb), 4), round(add.score(Xb, yb), 4))'
own = I + '''
def _r2(y, p):
    y = np.asarray(y, float); return float(1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum())
def spline_r2(n_knots):
    st = SplineTransformer(n_knots=n_knots, degree=3).fit(x_tr.reshape(-1, 1))
    B = st.transform(x_tr.reshape(-1, 1)); c = np.linalg.lstsq(B, y_tr, rcond=None)[0]
    return (round(_r2(y_tr, B @ c), 4), round(_r2(y_te, st.transform(x_te.reshape(-1, 1)) @ c), 4))
def additive_r2(interaction):
    Xa, ya = make_additive(300, 31, interaction); Xb, yb = make_additive(300, 32, interaction)
    A = np.c_[np.ones(len(Xa)), Xa]; c = np.linalg.lstsq(A, ya, rcond=None)[0]
    st = SplineTransformer(n_knots=5, degree=3).fit(Xa); c2 = np.linalg.lstsq(st.transform(Xa), ya, rcond=None)[0]
    return (round(_r2(yb, np.c_[np.ones(len(Xb)), Xb] @ c), 4), round(_r2(yb, st.transform(Xb) @ c2), 4))
'''
report('l18 s7', w, own, {
    'spline fitted on the test rows': (S7 % ('n_knots', 'x_te[:, None], y_te', r1, '32, interaction', 'Xa, ya', r2), False),
    'spline fitted on train and test rows together': (S7 % ('n_knots', 'np.r_[x_tr, x_te][:, None], np.r_[y_tr, y_te]', r1, '32, interaction', 'Xa, ya', r2), False),
    'n_knots ignored (5)': (S7 % ('5', 'x_tr[:, None], y_tr', r1, '32, interaction', 'Xa, ya', r2), False),
    '(test, training) order': (S7 % ('n_knots', 'x_tr[:, None], y_tr', '(round(m.score(x_te[:, None], y_te), 4), round(m.score(x_tr[:, None], y_tr), 4))', '32, interaction', 'Xa, ya', r2), False),
    'test set made without the interaction': (S7 % ('n_knots', 'x_tr[:, None], y_tr', r1, '32', 'Xa, ya', r2), False),
    'additive model fitted on the test rows': (S7 % ('n_knots', 'x_tr[:, None], y_tr', r1, '32, interaction', 'Xb, yb', r2), False),
    'additive: training R^2 reported': (S7 % ('n_knots', 'x_tr[:, None], y_tr', r1, '32, interaction', 'Xa, ya', '(round(lin.score(Xa, ya), 4), round(add.score(Xa, ya), 4))'), False),
    'scaler fitted on train and test together, then splines': (S7.replace('add = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(%s)', '_s = StandardScaler().fit(np.vstack([Xa, Xb])); Xa2, Xb2 = _s.transform(Xa), _s.transform(Xb)\n    add = make_pipeline(SplineTransformer(n_knots=5, degree=3), LinearRegression()).fit(%s)') % ('n_knots', 'x_tr[:, None], y_tr', r1, '32, interaction', 'Xa2, ya', '(round(lin.score(Xb, yb), 4), round(add.score(Xb2, yb), 4))'), False),
})

# ------------------------------------------------------------ l19 s7
w = widget('l19-which-learner.json', 7)
own = '''
def fit_table(problems, learners):
    return {p: {name: round(float(learners[name]().fit(v[0], v[1]).score(v[2], v[3])), 4) for name in learners} for p, v in problems.items()}
'''
report('l19 s7', w, own, {
    'one model per learner, built once and refitted for every problem (the explain says this carries state)': ('''
def fit_table(problems, learners):
    built = {n: mk() for n, mk in learners.items()}
    return {p: {n: round(built[n].fit(Xa, ya).score(Xb, yb), 4) for n in built} for p, (Xa, ya, Xb, yb) in problems.items()}
''', False),
    'training accuracy': ('''
def fit_table(problems, learners):
    return {p: {n: round(mk().fit(Xa, ya).score(Xa, ya), 4) for n, mk in learners.items()} for p, (Xa, ya, Xb, yb) in problems.items()}
''', False),
    'fitted on the test rows': ('''
def fit_table(problems, learners):
    return {p: {n: round(mk().fit(Xb, yb).score(Xb, yb), 4) for n, mk in learners.items()} for p, (Xa, ya, Xb, yb) in problems.items()}
''', False),
    'fitted on train and test rows together': ('''
import numpy as np
def fit_table(problems, learners):
    return {p: {n: round(mk().fit(np.vstack([Xa, Xb]), np.r_[ya, yb]).score(Xb, yb), 4) for n, mk in learners.items()} for p, (Xa, ya, Xb, yb) in problems.items()}
''', False),
    'no rounding': ('''
def fit_table(problems, learners):
    return {p: {n: mk().fit(Xa, ya).score(Xb, yb) for n, mk in learners.items()} for p, (Xa, ya, Xb, yb) in problems.items()}
''', False),
})

# ------------------------------------------------------------ l19 s8
w = widget('l19-which-learner.json', 8)
C8 = '''
def choose_on_validation(X, y, X_test, y_test, learners, n_val):
    best, ba = None, -1.0
    for name, make in learners.items():
        acc = make().fit(%s).score(%s)
        if acc %s ba:
            best, ba = name, acc
    m = learners[best]().fit(%s)
    return (best, round(m.score(X_test, y_test), 4))
'''
own = '''
def choose_on_validation(X, y, X_test, y_test, learners, n_val):
    cut = len(X) - n_val
    names = list(learners)
    val = [learners[n]().fit(X[:cut], y[:cut]).score(X[cut:], y[cut:]) for n in names]
    winner = names[val.index(max(val))]
    return (winner, round(float(learners[winner]().fit(X, y).score(X_test, y_test)), 4))
'''
tr, va = 'X[:-n_val], y[:-n_val]', 'X[-n_val:], y[-n_val:]'
report('l19 s8', w, own, {
    'chooses on the TEST rows': (C8 % ('X, y', 'X_test, y_test', '>', 'X, y'), False),
    'chooses on the test rows after fitting on the training part': (C8 % (tr, 'X_test, y_test', '>', 'X, y'), False),
    'fits on all rows, validates on the last n_val (seen rows)': (C8 % ('X, y', va, '>', 'X, y'), False),
    'chooses by training accuracy': (C8 % ('X, y', 'X, y', '>', 'X, y'), False),
    'no refit: reports the model fitted on the training part': (C8 % (tr, va, '>', tr), False),
    'tie to the learner listed last (>=)': (C8 % (tr, va, '>=', 'X, y'), False),
    'validates on the first n_val rows': (C8 % ('X[n_val:], y[n_val:]', 'X[:n_val], y[:n_val]', '>', 'X, y'), False),
    'reports the validation accuracy': (C8.replace('round(m.score(X_test, y_test), 4)', 'round(ba, 4)') % (tr, va, '>', 'X, y'), False),
})

# ------------------------------------------------------------ homework h-kmeans (performance)
w = widget('homework-4.json', 6)
own = '''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.array(X, dtype=float); C = np.array(init, dtype=float)
    last = None; labels = None
    count = 0
    while count < max_iter:
        dist = np.array([[np.sum((x - c) ** 2) for c in C] for x in X])
        labels = dist.argmin(axis=1); count += 1
        if last is not None and np.array_equal(labels, last):
            break
        for j in range(k):
            members = X[labels == j]
            if len(members):
                C[j] = members.mean(axis=0)
        last = labels.copy()
    return labels, np.round(C, 4), round(float(sum(np.sum((x - C[l]) ** 2) for x, l in zip(X, labels))), 4)
'''
report('h-kmeans', w, own, {
    'spec read literally: stops straight after the max_iter-th assignment, no update after it': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.asarray(X, float); C = np.asarray(init, float).copy(); prev = None
    for it in range(max_iter):
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if (prev is not None and (labels == prev).all()) or it == max_iter - 1:
            break
        for j in range(k):
            if (labels == j).any():
                C[j] = X[labels == j].mean(axis=0)
        prev = labels
    return labels, np.round(C, 4), round(float(((X - C[labels]) ** 2).sum()), 4)
''', False),
    'not from scratch: calls sklearn KMeans(init=init, n_init=1) from the prelude': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    m = KMeans(k, init=np.asarray(init, float), n_init=1, max_iter=max_iter).fit(np.asarray(X, float))
    return m.labels_, np.round(m.cluster_centers_, 4), round(float(m.inertia_), 4)
''', False),
    'labels reassigned to the final centres after the loop': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.asarray(X, float); C = np.asarray(init, float).copy(); prev = None
    for _ in range(max_iter):
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if prev is not None and (labels == prev).all():
            break
        for j in range(k):
            if (labels == j).any():
                C[j] = X[labels == j].mean(axis=0)
        prev = labels
    labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    return labels, np.round(C, 4), round(float(((X - C[labels]) ** 2).sum()), 4)
''', False),
    'stops when the centres stop moving (not when labels repeat)': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.asarray(X, float); C = np.asarray(init, float).copy()
    for _ in range(max_iter):
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        new = C.copy()
        for j in range(k):
            if (labels == j).any():
                new[j] = X[labels == j].mean(axis=0)
        if np.allclose(new, C):
            break
        C = new
    return labels, np.round(C, 4), round(float(((X - C[labels]) ** 2).sum()), 4)
''', True),
    'no empty-centre guard': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.asarray(X, float); C = np.asarray(init, float).copy(); prev = None
    for _ in range(max_iter):
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if prev is not None and (labels == prev).all():
            break
        for j in range(k):
            C[j] = X[labels == j].mean(axis=0)
        prev = labels
    return labels, np.round(C, 4), round(float(((X - C[labels]) ** 2).sum()), 4)
''', False),
    'labels permuted (relabelled by centre order at the end)': ('''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.asarray(X, float); C = np.asarray(init, float).copy(); prev = None
    for _ in range(max_iter):
        labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        if prev is not None and (labels == prev).all():
            break
        for j in range(k):
            if (labels == j).any():
                C[j] = X[labels == j].mean(axis=0)
        prev = labels
    o = np.argsort(-C[:, 0]); C = C[o]; labels = np.argsort(o)[labels]
    return labels, np.round(C, 4), round(float(((X - C[labels]) ** 2).sum()), 4)
''', False),
})

# ------------------------------------------------------------ homework h-rbf-decision
w = widget('homework-4.json', 7)
own = '''
import math
def rbf_kernel_predict(X_sv, coef, b, gamma, x):
    total = float(b)
    for s, a in zip(X_sv, coef):
        total += float(a) * math.exp(-gamma * sum((float(p) - float(q)) ** 2 for p, q in zip(s, x)))
    return total
'''
R = '''
import numpy as np
def rbf_kernel_predict(X_sv, coef, b, gamma, x):
    X_sv = np.asarray(X_sv, float); x = np.asarray(x, float)
    k = %s
    return %s
'''
report('h-rbf-decision', w, own, {
    'distance not squared': (R % ('np.exp(-gamma * np.sqrt(((X_sv - x) ** 2).sum(axis=1)))', 'float(np.dot(coef, k) + b)'), False),
    'intercept left out': (R % ('np.exp(-gamma * ((X_sv - x) ** 2).sum(axis=1))', 'float(np.dot(coef, k))'), False),
    'gamma left out': (R % ('np.exp(-((X_sv - x) ** 2).sum(axis=1))', 'float(np.dot(coef, k) + b)'), False),
    'gamma as 1/(2 gamma^2) width': (R % ('np.exp(-((X_sv - x) ** 2).sum(axis=1) / (2 * gamma ** 2))', 'float(np.dot(coef, k) + b)'), False),
    'returns the class, not the value': (R % ('np.exp(-gamma * ((X_sv - x) ** 2).sum(axis=1))', 'float(np.dot(coef, k) + b > 0)'), False),
    '|coef| used (signs lost)': (R % ('np.exp(-gamma * ((X_sv - x) ** 2).sum(axis=1))', 'float(np.dot(np.abs(coef), k) + b)'), False),
})

print(f'\nrun-code: {bad} failure(s) in author, starter and reader rows; {len(passing)} wrong solution(s) pass:')
for p in passing:
    print('  PASSES ' + p)
sys.exit(1 if bad else 0)
