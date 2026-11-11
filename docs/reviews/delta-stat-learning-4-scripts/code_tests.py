"""Delta read, stat-learning L4 fix pass: the six new hidden tests and h-kmeans, in CPython and in Pyodide.

Usage: <venv python> code_tests.py [content dir]      (default: app/content/courses/stat-learning)
       node pyo.mjs <pkgs> code_tests.py              (the same file inside the local Pyodide 0.27.7 build)

For each changed code widget: the model solution passes every hidden test, the starter fails, the wrong
solution each new test was written for fails THAT test, and the reader's own correct solutions (written in a
different style from the model) pass. Graded by the engine's rule: isclose element by element (rel 1e-9,
abs 1e-12, or the case's tol), plain equality otherwise. Rows marked INFO are reported, not failures.
Prints one line per solution and a digest of every network value so the two runtimes can be compared.
"""
import json, math, os, sys, warnings
warnings.filterwarnings("ignore")
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'courses', 'stat-learning')
BAD = []


def flat(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    return v


def close(x, y, tol):
    x, y = flat(x), flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k], tol) for k in x)
    if isinstance(x, list) or isinstance(y, list):
        return isinstance(x, list) and isinstance(y, list) and len(x) == len(y) and all(close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, str) or isinstance(y, str):
        return x == y
    rt, at = tol if tol else (1e-9, 1e-12)
    try:
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return x == y


def run(w, src):
    """List of booleans, one per hidden test."""
    g = {}
    exec(w.get('prelude', ''), g)
    try:
        exec(src, g)
    except Exception:
        return [False] * len(w['tests'])
    out = []
    for t in w['tests']:
        try:
            got = eval(t['call'], g); want = eval(t['expect'], g)
            tol = (t['tol'].get('rel', 0) or 0, t['tol'].get('abs', 0) or 0) if isinstance(t.get('tol'), dict) else None
            ok = close(got, want, tol) if t.get('compare') == 'isclose' else bool(flat(got) == flat(want))
        except Exception:
            ok = False
        out.append(bool(ok))
    return out


def widget(fname, where):
    d = json.load(open(os.path.join(ROOT, fname)))
    rows = d.get('screens') or d.get('items')
    if isinstance(where, str):
        return next(r for r in rows if r['id'] == where)['widget']
    return rows[where]['widget']


def row(name, w, label, src, want, must_fail=None):
    """want: 'pass', 'fail', 'allfail' or 'info'. must_fail: index of the test a wrong solution was written for."""
    r = run(w, src)
    failed = [i for i, ok in enumerate(r) if not ok]
    if want == 'pass':
        ok = not failed
    elif want == 'fail':
        ok = bool(failed) and (must_fail is None or must_fail in failed)
    elif want == 'allfail':
        ok = len(failed) == len(r)
    else:
        ok = True
    tag = 'ok  ' if ok else 'BAD '
    if want == 'info':
        tag = 'INFO'
    print(f"{tag} {name} | {label} | wanted {want} | failed tests {failed if failed else 'none'} of {len(r)}")
    if not ok:
        BAD.append(f"{name} | {label}")


# ---------------------------------------------------------------- l16 screens[4]: kmeans_step, new test 9
w = widget('l16-groups-nobody-labelled.json', 4)
ALT16 = '''
import numpy as np
def kmeans_step(X, centres):
    X = np.array(X, dtype=float); C = np.array(centres, dtype=float)
    labels = np.zeros(len(X), dtype=int)
    for i, x in enumerate(X):
        best, bd = 0, None
        for j, c in enumerate(C):
            dist = np.linalg.norm(x - c)          # plain Euclidean length, not squared
            if bd is None or dist < bd:
                best, bd = j, dist
        labels[i] = best
    new = []
    for j, c in enumerate(C):
        mine = X[labels == j]
        new.append(mine.mean(axis=0) if len(mine) else c)
    return labels, np.array(new)
def inertia(X, labels, centres):
    total = 0.0
    for x, l in zip(np.array(X, dtype=float), labels):
        total += float(np.sum((x - np.array(centres[l], dtype=float)) ** 2))
    return total
'''
MAN16 = w['solution'].replace("d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)", "d = np.abs(X[:, None, :] - C[None, :, :]).sum(axis=2)")
CHEB16 = w['solution'].replace("d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)", "d = np.abs(X[:, None, :] - C[None, :, :]).max(axis=2)")
assert MAN16 != w['solution'] and CHEB16 != w['solution']
n = 'l16 s4 kmeans_step'
row(n, w, 'model solution', w['solution'], 'pass')
row(n, w, 'starter', w['starter'], 'allfail')
row(n, w, 'reader: loops and np.linalg.norm', ALT16, 'pass')
row(n, w, 'wrong: Manhattan assignment (finding 11)', MAN16, 'fail', 9)
row(n, w, 'wrong: largest-gap (Chebyshev) assignment', CHEB16, 'info')

# ---------------------------------------------------------------- l17 screens[8]: mlp_width_report, new tests 5 and 6
w = widget('l17-a-small-network.json', 8)
ALT17 = '''
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import numpy as np
def mlp_width_report(widths, seed):
    def one(h):
        net = MLPClassifier(alpha=0.01, hidden_layer_sizes=[h], max_iter=500, random_state=seed, solver="lbfgs")
        net = net.fit(Xr_tr, yr_tr)
        return float(np.round(accuracy_score(yr_te, net.predict(Xr_te)), 4))
    return [one(h) for h in widths]
'''
ALT17B = '''
from sklearn.neural_network import MLPClassifier
def mlp_width_report(widths, seed):
    scores = {}
    for h in widths:
        scores[h] = MLPClassifier(h, solver="lbfgs", alpha=1e-2, random_state=seed, max_iter=500).fit(Xr_tr, yr_tr).score(Xr_te, yr_te)
    return [round(scores[h], 4) for h in widths]
'''
S = w['solution']
SEED0 = S.replace("random_state=seed", "random_state=0")
NOALPHA = S.replace(' alpha=0.01,', '')
NOSEED = S.replace("random_state=seed, ", "")
NOITER = S.replace(", max_iter=500", "")
SCALEALL = '''
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
def mlp_width_report(widths, seed):
    sc = StandardScaler().fit(np.vstack([Xr_tr, Xr_te]))      # the leak: test rows in the scaler
    out = []
    for h in widths:
        m = MLPClassifier(hidden_layer_sizes=(h,), solver="lbfgs", alpha=0.01, random_state=seed, max_iter=500)
        m.fit(sc.transform(Xr_tr), yr_tr)
        out.append(round(m.score(sc.transform(Xr_te), yr_te), 4))
    return out
'''
SCALETRAIN = SCALEALL.replace("np.vstack([Xr_tr, Xr_te])", "Xr_tr")
ADAM = S.replace('solver="lbfgs", ', '')
assert len({S, SEED0, NOALPHA, NOSEED, NOITER, ADAM}) == 6
n = 'l17 s8 mlp_width_report'
row(n, w, 'model solution', S, 'pass')
row(n, w, 'starter', w['starter'], 'allfail')
row(n, w, 'reader: closure, list for the sizes, accuracy_score', ALT17, 'pass')
row(n, w, 'reader: positional width, dict of scores', ALT17B, 'pass')
row(n, w, 'wrong: random_state fixed at 0 (finding 18)', SEED0, 'fail', 5)
row(n, w, 'wrong: default alpha (finding 18)', NOALPHA, 'fail', 6)
row(n, w, 'wrong: no random_state at all', NOSEED, 'info')
row(n, w, 'wrong: default max_iter', NOITER, 'info')
row(n, w, 'wrong: default solver (adam)', ADAM, 'info')
row(n, w, 'wrong: scaler fitted on training and test rows (the fix pass says it still passes)', SCALEALL, 'info')
row(n, w, 'not asked for: scaler fitted on training rows only', SCALETRAIN, 'info')
g = {}
exec(w['prelude'], g); exec(S, g)
print('NET l17 s8 model: widths [1,2,3,8,64] seed 0', g['mlp_width_report']([1, 2, 3, 8, 64], 0), '| [3] seeds 0..7', [g['mlp_width_report']([3], s)[0] for s in range(8)], '| [8] seeds 0..2', [g['mlp_width_report']([8], s)[0] for s in range(3)])
g2 = {}
exec(w['prelude'], g2); exec(NOALPHA, g2)
print('NET l17 s8 default alpha: [3] seed 5', g2['mlp_width_report']([3], 5), '| seed 0', g2['mlp_width_report']([3], 0), '| seed 1', g2['mlp_width_report']([3], 1))
g3 = {}
exec(w['prelude'], g3); exec(SCALEALL, g3)
print('NET l17 s8 scaler on all rows: [1,2,3,8,64] seed 0', g3['mlp_width_report']([1, 2, 3, 8, 64], 0), '| [3] seed 1, 5', g3['mlp_width_report']([3], 1), g3['mlp_width_report']([3], 5))

# ---------------------------------------------------------------- l19 screens[7]: fit_table, new test 5 (count of builds)
w = widget('l19-which-learner.json', 7)
ALT19A = '''
def fit_table(problems, learners):
    def cell(data, name):
        Xa, ya, Xb, yb = data
        model = learners[name]()
        model.fit(Xa, ya)
        return round(float((model.predict(Xb) == yb).mean()), 4)
    return {p: {name: cell(data, name) for name in learners} for p, data in problems.items()}
'''
ALT19B = '''
def fit_table(problems, learners):
    # every model of a row built first, then fitted: still one fresh model per cell
    out = {}
    for p in problems:
        models = [(name, learners[name]()) for name in learners]
        Xa, ya, Xb, yb = problems[p]
        out[p] = dict((name, round(m.fit(Xa, ya).score(Xb, yb), 4)) for name, m in models)
    return out
'''
ALT19C = '''
from sklearn.base import clone
def fit_table(problems, learners):
    # one template per learner, a fresh unfitted clone of it for every cell
    templates = {name: make() for name, make in learners.items()}
    table = {}
    for p, (Xa, ya, Xb, yb) in problems.items():
        table[p] = {name: round(clone(t).fit(Xa, ya).score(Xb, yb), 4) for name, t in templates.items()}
    return table
'''
ALT19D = '''
def fit_table(problems, learners):
    # a fresh model per cell, and one more per learner built only to look at it
    table = {}
    for name, make in learners.items():
        kind = type(make()).__name__
        for p, (Xa, ya, Xb, yb) in problems.items():
            table.setdefault(p, {})[name] = round(make().fit(Xa, ya).score(Xb, yb), 4)
    return {p: {name: table[p][name] for name in learners} for p in problems}
'''
REUSE = '''
def fit_table(problems, learners):
    built = {name: make() for name, make in learners.items()}      # one object per learner, refitted per problem
    table = {}
    for p, (Xa, ya, Xb, yb) in problems.items():
        table[p] = {}
        for name, m in built.items():
            m.fit(Xa, ya)
            table[p][name] = round(m.score(Xb, yb), 4)
    return table
'''
n = 'l19 s7 fit_table'
row(n, w, 'model solution', w['solution'], 'pass')
row(n, w, 'starter', w['starter'], 'allfail')
row(n, w, 'reader A: comprehension, accuracy by hand', ALT19A, 'pass')
row(n, w, 'reader B: a row of models built first, then fitted', ALT19B, 'pass')
row(n, w, 'wrong by the comment: one model per learner, refitted (finding 24)', REUSE, 'fail', 5)
row(n, w, 'reader C: a fresh clone() of one template per cell (independent cells, one factory call per learner)', ALT19C, 'info')
row(n, w, 'reader D: a fresh model per cell plus one inspected per learner', ALT19D, 'info')
# what the count test sees, and whether a kept fitted model really is overwritten
g = {}
exec(w['prelude'], g)
for label, src in (('model', w['solution']), ('reused', REUSE), ('clone', ALT19C), ('inspect', ALT19D)):
    h = dict(g); exec(src, h)
    h['BUILDS'].clear()
    t = h['fit_table']({'street': h['PROBLEMS']['street'], 'rings': h['PROBLEMS']['rings']}, {'logistic': h['counted']('logistic')})
    print(f'COUNT l19 s7 {label}: builds {len(h["BUILDS"])}, cells {t}')
det = {k: v for k, v in g['LEARNERS'].items() if k != 'net'}
h = dict(g); exec(w['solution'], h); full = h['fit_table'](h['PROBLEMS'], det)
h2 = dict(g); exec(REUSE, h2); full2 = h2['fit_table'](h2['PROBLEMS'], det)
print('PROBE l19 s7: a reused object gives the same 20 deterministic cells:', full == full2)
print('NET l19 s7 deterministic table:', full)
P = g['PROBLEMS']
kept = g['LEARNERS']['logistic']().fit(P['street'][0], P['street'][1])
before = round(kept.score(P['street'][2], P['street'][3]), 4)
same_obj = kept.fit(P['rings'][0], P['rings'][1])
print('PROBE l19 s7: kept street model scores', before, 'on the street; after the same object is fitted to the rings it scores', round(kept.score(P['street'][2], P['street'][3]), 4), '| fit returns the same object:', same_obj is kept)
print('NET l19 net column', h['fit_table'](P, {'net': g['LEARNERS']['net']}))

# ---------------------------------------------------------------- l19 screens[8]: choose_on_validation, new test 5 (knn1)
w = widget('l19-which-learner.json', 8)
ALT19V = '''
def choose_on_validation(X, y, X_test, y_test, learners, n_val):
    cut = len(X) - n_val
    scores = {}
    for name in learners:
        model = learners[name]()
        model.fit(X[:cut], y[:cut])
        scores[name] = (model.predict(X[cut:]) == y[cut:]).mean()
    winner = max(scores, key=scores.get)            # max keeps the first of equal keys
    final = learners[winner]().fit(X, y)
    return winner, round(float(final.score(X_test, y_test)), 4)
'''
ALT19W = '''
import numpy as np
def choose_on_validation(X, y, X_test, y_test, learners, n_val):
    names = list(learners)
    Xa, ya, Xv, yv = X[:-n_val], y[:-n_val], X[-n_val:], y[-n_val:]
    accs = np.array([learners[n]().fit(Xa, ya).score(Xv, yv) for n in names])
    order = sorted(range(len(names)), key=lambda i: -accs[i])     # a stable sort: ties keep list order
    best = names[order[0]]
    return (best, round(learners[best]().fit(X, y).score(X_test, y_test), 4))
'''
S = w['solution']
SEEN = S.replace("acc = make().fit(X[:-n_val], y[:-n_val]).score(X[-n_val:], y[-n_val:])", "acc = make().fit(X, y).score(X[-n_val:], y[-n_val:])")
TIELAST = S.replace("if acc > best_acc:", "if acc >= best_acc:")
NOREFIT = S.replace("m = learners[best]().fit(X, y)", "m = learners[best]().fit(X[:-n_val], y[:-n_val])")
ONTEST = S.replace("acc = make().fit(X[:-n_val], y[:-n_val]).score(X[-n_val:], y[-n_val:])", "acc = make().fit(X, y).score(X_test, y_test)")
FIRSTVAL = S.replace("X[:-n_val], y[:-n_val]).score(X[-n_val:], y[-n_val:])", "X[n_val:], y[n_val:]).score(X[:n_val], y[:n_val])")
VALSCORE = S.replace("return (best, round(m.score(X_test, y_test), 4))", "return (best, round(best_acc, 4))")
assert len({S, SEEN, TIELAST, NOREFIT, ONTEST, FIRSTVAL, VALSCORE}) == 7
n = 'l19 s8 choose_on_validation'
row(n, w, 'model solution', S, 'pass')
row(n, w, 'starter', w['starter'], 'allfail')
row(n, w, 'reader: dict of scores and max', ALT19V, 'pass')
row(n, w, 'reader: array of scores and a stable sort', ALT19W, 'pass')
row(n, w, 'wrong: validates on rows it has fitted (finding 26)', SEEN, 'fail', 5)
row(n, w, 'wrong: tie to the later learner', TIELAST, 'fail')
row(n, w, 'wrong: winner not refitted on all rows', NOREFIT, 'info')
row(n, w, 'wrong: chooses on the test rows', ONTEST, 'fail')
row(n, w, 'wrong: validates on the first n_val rows', FIRSTVAL, 'fail')
row(n, w, 'wrong: reports the validation score', VALSCORE, 'fail')
g = {}
exec(w['prelude'], g)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
X, y, Xt, yt = g['PROBLEMS']['street']
two = {'logistic': g['LEARNERS']['logistic'], 'knn1': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(1))}
for name, mk in two.items():
    honest = mk().fit(X[:-100], y[:-100]).score(X[-100:], y[-100:])
    seen = mk().fit(X, y).score(X[-100:], y[-100:])
    test = mk().fit(X, y).score(Xt, yt)
    print(f'PROBE l19 s8 {name}: honest validation {honest:.4f}, on seen rows {seen:.4f}, test after refit {test:.4f}')
h = dict(g); exec(S, h)
print('NET l19 s8 model on the five problems:', [list(h['choose_on_validation'](*g['PROBLEMS'][p], g['LEARNERS'], 20 if p == 'wide' else 100)) for p in g['PROBLEMS']])

# ---------------------------------------------------------------- homework h-kmeans: one reading of the stop rule
w = widget('homework-4.json', 'h-kmeans')
ALTKM = '''
import numpy as np
def kmeans(X, k, init, max_iter):
    X = np.array(X, dtype=float)
    centres = np.array(init, dtype=float)
    last = None
    rounds = 0
    while rounds < max_iter:
        labels = np.array([int(np.argmin([np.sum((x - c) ** 2) for c in centres])) for x in X])
        if last is not None and np.array_equal(labels, last):
            break
        centres = np.array([X[labels == j].mean(axis=0) if np.any(labels == j) else centres[j] for j in range(k)])
        last = labels
        rounds += 1
    total = sum(float(np.sum((x - centres[l]) ** 2)) for x, l in zip(X, labels))
    return labels, np.round(centres, 4), round(total, 4)
'''
ALTKM2 = '''
import numpy as np
def kmeans(X, k, init, max_iter):
    # update first, then test for a repeat; plain Euclidean length
    X = np.asarray(X, float); C = np.asarray(init, float).copy()
    old = np.full(len(X), -1)
    for _ in range(max_iter):
        lab = np.linalg.norm(X[:, None] - C[None], axis=2).argmin(1)
        C = np.vstack([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if (lab == old).all():
            break
        old = lab
    return lab, C.round(4), round(float(((X - C[lab]) ** 2).sum()), 4)
'''
S = w['solution']
EARLY = S.replace("        for j in range(k):", "        if _ == max_iter - 1:\n            break\n        for j in range(k):")
REASSIGN = S.replace("    inertia = float", "    labels = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)\n    inertia = float")
EXTRA = S.replace("    for _ in range(max_iter):", "    for _ in range(max_iter + 1):")
SK = '''
import numpy as np
from sklearn.cluster import KMeans
def kmeans(X, k, init, max_iter):
    km = KMeans(k, init=np.asarray(init, float), n_init=1, max_iter=max_iter).fit(np.asarray(X, float))
    return km.labels_, np.round(km.cluster_centers_, 4), round(float(km.inertia_), 4)
'''
assert len({S, EARLY, REASSIGN, EXTRA}) == 4
n = 'homework h-kmeans'
row(n, w, 'model solution', S, 'pass')
row(n, w, 'starter', w['starter'], 'allfail')
row(n, w, 'reader: while loop counting rounds, list comprehensions', ALTKM, 'pass')
row(n, w, 'reader: update before the repeat test, plain Euclidean length', ALTKM2, 'pass')
row(n, w, 'wrong: stops straight after the max_iter-th assignment (finding 32)', EARLY, 'fail', 3)
row(n, w, 'wrong: labels assigned once more after the loop', REASSIGN, 'fail')
row(n, w, 'wrong: max_iter + 1 rounds', EXTRA, 'fail', 3)
row(n, w, "wrong: scikit-learn's KMeans called from the prelude", SK, 'fail')
g = {}
exec(w['prelude'], g); exec(S, g)
km = g['KMeans'](3, init=g['Z'][[0, 1, 2]], n_init=1).fit(g['Z'])
print('NET h-kmeans: model inertia', g['kmeans'](g['Z'], 3, g['Z'][[0, 1, 2]], 300)[2], '| scikit-learn', round(float(km.inertia_), 6), '| from rows 0, 20, 40:', g['kmeans'](g['Z'], 3, g['Z'][[0, 20, 40]], 300)[2])

print(f"{len(BAD)} BAD rows" + (': ' + '; '.join(BAD) if BAD else ''))
if __name__ == '__main__':
    sys.exit(1 if BAD else 0)
