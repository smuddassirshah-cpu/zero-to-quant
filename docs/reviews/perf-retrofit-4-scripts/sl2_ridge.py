"""stat-learning homework-2 h-ridge-formula: reader closed-form solution, starter, shipped
solution and reader-planted slips (none from the author's list) on every example and test."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, report

it = item('stat-learning', 'homework-2.json', 'h-ridge-formula')
W = it['widget']
SOL = W['solution']

READER = '''
import numpy as np

def ridge_formula(X, y, n_train, alpha):
    X = np.array(X, dtype=float); y = np.array(y, dtype=float)
    Xt, yt = X[:n_train], y[:n_train]
    m = Xt.mean(axis=0)
    s = Xt.std(axis=0)                  # ddof 0, as StandardScaler
    s[s == 0] = 1.0                     # StandardScaler leaves a constant column at scale 1
    Z = (Xt - m) / s
    zc = Z - Z.mean(axis=0)             # Z is centred already; kept for clarity
    yc = yt - yt.mean()
    b = np.linalg.solve(zc.T @ zc + alpha * np.eye(X.shape[1]), zc.T @ yc)
    coefs = b / s
    intercept = yt.mean() - coefs @ m
    pred = intercept + X[n_train:] @ coefs
    return float(intercept), coefs.tolist(), float(np.mean((y[n_train:] - pred) ** 2))
'''

def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)

PLANTS = {
    'training rows include row n_train (off by one)': swap(SOL, 'pipe.fit(X[:n_train], y[:n_train])', 'pipe.fit(X[:n_train + 1], y[:n_train + 1])'),
    'intercept sign: + coefs @ mean': swap(SOL, 'intercept = model.intercept_ - coefs @ scale.mean_', 'intercept = model.intercept_ + coefs @ scale.mean_'),
    'test error as RMSE': swap(SOL, 'test_mse = np.mean((y[n_train:] - pipe.predict(X[n_train:])) ** 2)', 'test_mse = np.sqrt(np.mean((y[n_train:] - pipe.predict(X[n_train:])) ** 2))'),
    'test error over all rows': swap(SOL, 'test_mse = np.mean((y[n_train:] - pipe.predict(X[n_train:])) ** 2)', 'test_mse = np.mean((y - pipe.predict(X)) ** 2)'),
    'coefficients times the sd, not divided': swap(SOL, 'coefs = model.coef_ / scale.scale_', 'coefs = model.coef_ * scale.scale_'),
    'alpha divided by n_train': swap(SOL, "Ridge(alpha=alpha)", "Ridge(alpha=alpha / n_train)"),
}

fails = 0
fe, ft = report('starter', run(it, W['starter']))
if not ft: print('  FAIL starter passes'); fails += 1
for lab, src in (('shipped solution', SOL), ('reader solution', READER)):
    fe, ft = report(lab, run(it, src))
    if fe or ft: print('  FAIL', lab); fails += 1
for lab, src in PLANTS.items():
    fe, ft = report('plant: ' + lab, run(it, src))
    if not ft: print('  FAIL plant uncaught:', lab); fails += 1
print('failures:', fails)
sys.exit(1 if fails else 0)
