"""stat-learning L2 performance task h-ridge-formula: every number recomputed.

Run with the scratchpad venv (scikit-learn 1.6.1, NumPy): exits 0 when
  - the shipped solution (route A, scikit-learn Pipeline) passes every example and test,
  - an independent closed form in NumPy (route B) gives every expected value,
  - the one-feature example agrees with exact fractions (route C),
  - the starter fails every test,
  - each planted wrong solution fails at least one test, none only on the last.
Grading copies app/js/engine/widgets/code.js: setup in the shared namespace,
then call; isclose element by element at rel 1e-9, abs 1e-12.
"""
import json
import math
import os
from fractions import Fraction as F

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'stat-learning', 'homework-2.json')
FAILS = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        FAILS.append(msg)


def flat(v):
    if isinstance(v, np.ndarray) or isinstance(v, np.generic):
        return v.tolist()
    return v


def close(x, y):
    x, y = flat(x), flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(close(a, b) for a, b in zip(x, y)))
    if x is None or y is None:
        return x is y
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return False


def run(code, cases):
    ns = {}
    exec(code, ns)
    out = []
    for c in cases:
        try:
            if c.get('setup'):
                exec(c['setup'], ns)
            out.append(close(eval(c['call'], ns), eval(c['expect'], {})))
        except Exception:
            out.append(False)
    return out


d = json.load(open(HW))
items = d['items']
it = next(i for i in items if i['id'] == 'h-ridge-formula')
w = it['widget']
tests, examples = w['tests'], w['examples']

# shape and homework limits
check(it.get('performance') == 'code' and w['kind'] == 'code', 'performance code item')
check(len(tests) >= 3 and len(tests) > len(examples), f'{len(tests)} tests > {len(examples)} examples')
check(6 <= len(items) <= 12, f'homework holds {len(items)} items (6 to 12)')
check(any(i.get('difficulty') == 5 for i in items), 'a difficulty 5 item present')
check(sum(1 for i in items if i.get('performance')) == 1, 'one performance item in homework-2')
check('6 hidden tests' in w['how'], 'how names 6 hidden tests')

# route A: the shipped solution
resA = run(w['solution'], examples + tests)
check(all(resA), 'solution passes every example and test')

# route B: closed form in NumPy, written independently of the solution


def closed_form(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    Xt, yt = X[:n_train], y[:n_train]
    m = Xt.mean(axis=0)
    s = np.sqrt(((Xt - m) ** 2).mean(axis=0))
    s[s == 0] = 1.0
    Z = (Xt - m) / s
    b = np.linalg.solve(Z.T @ Z + alpha * np.eye(X.shape[1]), Z.T @ (yt - yt.mean()))
    coefs = b / s
    icpt = yt.mean() - coefs @ m
    pred = icpt + X[n_train:] @ coefs
    return icpt, coefs.tolist(), float(np.mean((y[n_train:] - pred) ** 2))


for k, c in enumerate(tests, 1):
    ns = {}
    exec(c['setup'], ns)
    args = eval(c['call'].replace('ridge_formula', ''), ns)
    got = closed_form(*args)
    want = eval(c['expect'], {})
    check(close(got, want), f'test {k}: closed form gives {c["expect"][:60]}')
    # margin: the two routes agree far inside rel 1e-9
    a = np.array([want[0], *want[1], want[2]]); b = np.array([got[0], *got[1], got[2]])
    rel = np.max(np.abs(a - b) / np.maximum(np.abs(a), 1e-12))
    check(rel < 1e-11 or np.max(np.abs(a - b)) < 1e-13, f'test {k}: routes agree to {rel:.1e} relative')

# route C: the example by hand, exact fractions.
# x = 0, 2, 4, 6 train, mean 3, population variance 5; y = 1, 2, 4, 5, mean 3.
x = [F(v) for v in (0, 2, 4, 6)]; yv = [F(v) for v in (1, 2, 4, 5)]
mx, my = sum(x) / 4, sum(yv) / 4
var = sum((v - mx) ** 2 for v in x) / 4
sxy = sum((a - mx) * (b - my) for a, b in zip(x, yv))
# z = (x - 3)/sd: sum z^2 = 4, sum z (y - ybar) = sxy / sd; b = (sxy/sd) / (4 + 4); raw coef b / sd = sxy / (var * 8)
c_raw = sxy / (var * (4 + 4))
icpt = my - c_raw * mx
mse = (6 - (icpt + c_raw * 8)) ** 2
check((mx, var, sxy) == (3, 5, 14), 'example: mean 3, variance 5, sum of cross products 14')
check((c_raw, icpt, mse) == (F(7, 20), F(39, 20), F(25, 16)), 'example: coef 0.35, intercept 1.95, test MSE 1.5625 exactly')
check(examples[0]['expect'] == '(1.95, [0.35], 1.5625)' and tests[0]['expect'] == examples[0]['expect'], 'example shown as (1.95, [0.35], 1.5625)')
# the dummy test: the column is constant on training rows, so its coefficient is 0
ns = {}; exec(tests[4]['setup'], ns)
check(len(set(r[3] for r in ns['X'][:7])) == 1 and ns['X'][9][3] == 1, 'test 5: dummy constant on training rows, 1 on a test row')
check(eval(tests[4]['expect'])[1][3] == 0.0, 'test 5: dummy coefficient 0')

# the starter fails every test
resS = run(w['starter'], tests)
check(not any(resS), 'starter fails every test')

# planted wrong solutions
BUGS = {}
COMMON = '''import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
'''
BUGS['scaler fitted on all rows'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    sc = StandardScaler().fit(X)
    m = Ridge(alpha=alpha).fit(sc.transform(X[:n_train]), y[:n_train])
    coefs = m.coef_ / sc.scale_
    icpt = m.intercept_ - coefs @ sc.mean_
    return float(icpt), list(coefs), float(np.mean((y[n_train:] - icpt - X[n_train:] @ coefs) ** 2))
'''
BUGS['penalty on unscaled features'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    m = Ridge(alpha=alpha).fit(X[:n_train], y[:n_train])
    return float(m.intercept_), list(m.coef_), float(np.mean((y[n_train:] - m.predict(X[n_train:])) ** 2))
'''
BUGS['pipeline fitted on all rows'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    p = Pipeline([('s', StandardScaler()), ('m', Ridge(alpha=alpha))]).fit(X, y)
    s, m = p.named_steps['s'], p.named_steps['m']
    coefs = m.coef_ / s.scale_
    return float(m.intercept_ - coefs @ s.mean_), list(coefs), float(np.mean((y[n_train:] - p.predict(X[n_train:])) ** 2))
'''
BUGS['test rows scaled with their own mean and sd'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    s = StandardScaler().fit(X[:n_train])
    m = Ridge(alpha=alpha).fit(s.transform(X[:n_train]), y[:n_train])
    coefs = m.coef_ / s.scale_
    pred = m.predict(StandardScaler().fit_transform(X[n_train:]))
    return float(m.intercept_ - coefs @ s.mean_), list(coefs), float(np.mean((y[n_train:] - pred) ** 2))
'''
BUGS['coefficients left in scaled units'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    p = Pipeline([('s', StandardScaler()), ('m', Ridge(alpha=alpha))]).fit(X[:n_train], y[:n_train])
    m = p.named_steps['m']
    return float(m.intercept_), list(m.coef_), float(np.mean((y[n_train:] - p.predict(X[n_train:])) ** 2))
'''
BUGS['intercept not moved to raw units'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    p = Pipeline([('s', StandardScaler()), ('m', Ridge(alpha=alpha))]).fit(X[:n_train], y[:n_train])
    s, m = p.named_steps['s'], p.named_steps['m']
    return float(m.intercept_), list(m.coef_ / s.scale_), float(np.mean((y[n_train:] - p.predict(X[n_train:])) ** 2))
'''
BUGS['sample sd (ddof 1)'] = '''import numpy as np
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    Xt, yt = X[:n_train], y[:n_train]
    mu = Xt.mean(0); sd = Xt.std(0, ddof=1); sd[sd == 0] = 1
    Z = (Xt - mu) / sd
    b = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ (yt - yt.mean()))
    c = b / sd; i = yt.mean() - c @ mu
    return float(i), list(c), float(np.mean((y[n_train:] - i - X[n_train:] @ c) ** 2))
'''
BUGS['intercept penalised too'] = '''import numpy as np
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    Xt, yt = X[:n_train], y[:n_train]
    mu = Xt.mean(0); sd = Xt.std(0); sd[sd == 0] = 1
    Z = np.column_stack([np.ones(n_train), (Xt - mu) / sd])
    b = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ yt)
    c = b[1:] / sd; i = b[0] - c @ mu
    return float(i), list(c), float(np.mean((y[n_train:] - i - X[n_train:] @ c) ** 2))
'''
BUGS['no guard for a constant column'] = '''import numpy as np
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    Xt, yt = X[:n_train], y[:n_train]
    mu = Xt.mean(0); sd = Xt.std(0)
    with np.errstate(all='ignore'):
        Z = (Xt - mu) / sd
        b = np.linalg.solve(Z.T @ Z + alpha * np.eye(Z.shape[1]), Z.T @ (yt - yt.mean()))
        c = b / sd; i = yt.mean() - c @ mu
        return float(i), list(c), float(np.mean((y[n_train:] - i - X[n_train:] @ c) ** 2))
'''
BUGS['mean squared error in the objective'] = COMMON + '''
def ridge_formula(X, y, n_train, alpha):
    X = np.asarray(X, float); y = np.asarray(y, float)
    p = Pipeline([('s', StandardScaler()), ('m', Ridge(alpha=alpha * n_train))]).fit(X[:n_train], y[:n_train])
    s, m = p.named_steps['s'], p.named_steps['m']
    c = m.coef_ / s.scale_
    return float(m.intercept_ - c @ s.mean_), list(c), float(np.mean((y[n_train:] - p.predict(X[n_train:])) ** 2))
'''
for name, code in BUGS.items():
    res = run(code, tests)
    failed = [k + 1 for k, r in enumerate(res) if not r]
    check(bool(failed), f'planted "{name}" fails tests {failed}')
    check(bool(failed) and failed[0] < len(tests) or len(failed) > 1, f'planted "{name}" caught before the last test')

# a sanity check on the data: the training means and sds differ from the all-row ones
ns = {}; exec(tests[1]['setup'], ns)
X = np.asarray(ns['X'], float)
check(not np.allclose(X[:7].std(0), X.std(0)), 'test 2: training sd differs from all-row sd')

print('failures:', len(FAILS))
raise SystemExit(1 if FAILS else 0)
