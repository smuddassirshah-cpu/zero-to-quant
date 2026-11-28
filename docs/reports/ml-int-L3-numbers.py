"""Recompute every number stated in ml-int level 3 (A deep learning case at a fund) and check each at its JSON path.

Run through the CI runner (from app/): node tools/run-number-scripts.mjs --python <venv>/bin/python --only ml-int-L3
Direct: ZQ_NUMBERS_STRICT=1 OPENBLAS_NUM_THREADS=1 <venv>/bin/python docs/reports/ml-int-L3-numbers.py
--write refits every model and rewrites app/content/data/ai/ml-int-case-daily-mse.csv (about 25 s), then checks.

scikit-learn 1.6.1 (the venv and Pyodide pin) recomputes every figure; the brief's figures came from 1.9.1, and the third
decimal of R^2 and the second of t moved (the orderings and signs the lessons rely on all hold, checked below).
Routes: R^2 by hand (1 - SSE/SST) against sklearn's r2_score on the refitted predictions; the file's day sums against both;
every claim about a world checked on two seeds; t by hand against scipy.stats.ttest_rel. Boosting and ridge are refitted and
compared with the file to 1e-9; the network's training is iterative, so its file figures are compared to 1e-4 relative and
every statement about it is a rounded figure or an ordering with a margin many times that.
"""
import csv
import io
import math
import os
import shutil
import sys
import tempfile

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai', 'ml-int-case-daily-mse.csv')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402
from sklearn.ensemble import HistGradientBoostingRegressor  # noqa: E402
from sklearn.linear_model import Ridge  # noqa: E402
from sklearn.metrics import r2_score  # noqa: E402
from sklearn.neural_network import MLPRegressor  # noqa: E402


def panel(world, seed, assets=100, days=500, p=8):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((days, assets, p))
    if world == 'A':
        sig = 0.6 * ((X[..., 0] > 0.8).astype(float) - (X[..., 1] < -0.8).astype(float)) * ((X[..., 0] > 0.8) | (X[..., 1] < -0.8))
        sig = sig + 0.4 * (X[..., 0] > 0.8) * (X[..., 1] > 0.5)
        noise = rng.standard_t(3, (days, assets)) / np.sqrt(3)
    else:
        w = rng.standard_normal(p)
        w /= np.linalg.norm(w)
        u = X @ w
        v = X @ np.roll(w, 3)
        sig = 0.5 * np.tanh(1.5 * u) + 0.15 * u * v
        noise = rng.standard_normal((days, assets))
    y = sig + 5.0 * noise * np.std(sig)
    return X, y, sig


def fit(world, seed, assets=100, days=500, ntest=150):
    X, y, sig = panel(world, seed, assets, days)
    ntr = days - ntest
    Xtr, ytr, Xte, yte = X[:ntr].reshape(-1, X.shape[2]), y[:ntr].ravel(), X[ntr:].reshape(-1, X.shape[2]), y[ntr:].ravel()
    pred = {'boost': HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, random_state=0).fit(Xtr, ytr).predict(Xte),
            'mlp': MLPRegressor(hidden_layer_sizes=(32, 32), alpha=1e-3, learning_rate_init=1e-3, max_iter=300, early_stopping=True, random_state=0).fit(Xtr, ytr).predict(Xte),
            'ridge': Ridge(alpha=1.0).fit(Xtr, ytr).predict(Xte)}
    return yte, pred, sig[ntr:].ravel(), ntest


RUNS = [(w, s) for w in 'AB' for s in (0, 1)]
FITS = {k: fit(*k) for k in RUNS}
if '--write' in sys.argv:
    out = io.StringIO()
    wr = csv.writer(out, lineterminator='\n')
    wr.writerow(['world', 'seed', 'day', 'mse_boost', 'mse_mlp', 'mse_ridge', 'var_y'])
    for (w, s), (yte, pred, _, nt) in FITS.items():
        mse = {k: ((yte - v) ** 2).reshape(nt, -1).mean(1) for k, v in pred.items()}
        vy = ((yte - yte.mean()) ** 2).reshape(nt, -1).mean(1)
        for d in range(nt):
            wr.writerow([w, s, d + 1] + [f'{x:.10f}' for x in (mse['boost'][d], mse['mlp'][d], mse['ridge'][d], vy[d])])
    open(DATA, 'w').write(out.getvalue())
    print('wrote', DATA, len(out.getvalue()), 'bytes')

ROWS = list(csv.DictReader(open(DATA)))
COL = lambda w, s, c: np.array([float(r[c]) for r in ROWS if r['world'] == w and int(r['seed']) == s])
lv = Level('ml-int', 3, coverage='strict')
E = lv.expect
L9, L10, L11, L12 = 'l9-net', 'l10-a-fair', 'l11-when', 'l12-the-case'


def agree(label, a, b, rel=1e-9, covers=()):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= rel * np.maximum(1e-12, np.maximum(np.abs(a), np.abs(b))) + 1e-12))
    lv.claim(ok, f'{label}: routes agree', covers=[float(x) for x in np.ravel(a)] + list(covers))
    return a


lv.claim(len(ROWS) == 600 and os.path.getsize(DATA) < 256 * 1024, f'the data file holds 600 rows and is under 256 KB ({os.path.getsize(DATA)} bytes)', covers=[600])
R2, ORC, T, D = {}, {}, {}, {}
for (w, s), (yte, pred, sig, nt) in FITS.items():
    for k, v in pred.items():
        hand = 1 - np.sum((yte - v) ** 2) / np.sum((yte - yte.mean()) ** 2)
        lib = r2_score(yte, v)
        filed = 1 - COL(w, s, 'mse_' + k).sum() / COL(w, s, 'var_y').sum()
        agree(f'{w}{s} {k}: R2 by hand against r2_score', hand, lib, 1e-9)
        agree(f'{w}{s} {k}: R2 from the file\'s day sums against the refit', filed, lib, 1e-9 if k != 'mlp' else 1e-4)
        R2[w, s, k] = filed
    ORC[w, s] = 1 - np.mean((yte - sig) ** 2) / np.var(yte)
    dd = COL(w, s, 'mse_mlp') - COL(w, s, 'mse_boost')
    T[w, s] = dd.mean() / (dd.std(ddof=1) / math.sqrt(len(dd)))
    D[w, s] = dd
    agree(f'{w}{s} paired t by hand against scipy ttest_rel', T[w, s], stats.ttest_rel(COL(w, s, 'mse_mlp'), COL(w, s, 'mse_boost')).statistic, 1e-9)
    print(w, s, {k: round(R2[w, s, k], 4) for k in ('boost', 'mlp', 'ridge')}, 'oracle', round(ORC[w, s], 4), 't', round(T[w, s], 2))

# orderings and signs the lessons rely on, on both seeds
lv.claim(all(R2['A', s, 'boost'] > R2['A', s, 'mlp'] > R2['A', s, 'ridge'] for s in (0, 1)), 'world A: boosting > network > ridge on both seeds')
lv.claim(all(R2['B', s, 'mlp'] > R2['B', s, 'boost'] for s in (0, 1)), 'world B: network > boosting on both seeds')
lv.claim(all(ORC[k] > max(R2[k + (m,)] for m in ('boost', 'mlp', 'ridge')) for k in RUNS), 'the oracle is above every model in every run')
lv.claim(T['A', 0] > 2 and T['A', 1] > 2 and T['B', 0] < -2 and -2 < T['B', 1] < 0, 'paired t: world A significant for boosting on both seeds; world B significant for the network on seed 0 only')
lv.claim(R2['B', 1, 'ridge'] > R2['B', 1, 'boost'], 'world B seed 1: ridge beats boosting')

# ------------------------------------------------------------------ the stated figures, from the file (route A) and the refit (route B)
f4 = lambda v: round(v, 4)
for k in RUNS:
    yte, pred, sig, nt = FITS[k]
    for m in ('boost', 'mlp', 'ridge'):
        lv.claim(abs(round(R2[k + (m,)], 4) - round(r2_score(yte, pred[m]), 4)) < 1e-12, f'{k} {m}: the stated R2 {round(R2[k + (m,)], 4)} is the refit\'s to 4 places', covers=[f4(R2[k + (m,)])])
    orc_sums = 1 - np.sum((yte - sig) ** 2) / np.sum((yte - yte.mean()) ** 2)
    lv.claim(abs(ORC[k] - orc_sums) < 1e-12, f'{k} oracle by means and by sums agree', covers=[f4(ORC[k])])
    lv.claim(abs(T[k] - stats.ttest_rel(COL(*k, 'mse_mlp'), COL(*k, 'mse_boost')).statistic) < 1e-9, f'{k} t {T[k]:.2f}', covers=[round(T[k], 2)])
for k in RUNS:
    md, se = D[k].mean(), D[k].std(ddof=1) / math.sqrt(150)
    lv.claim(abs(md / se - T[k]) < 1e-9, f'{k}: mean {md:.4f}, se {se:.4f}', covers=[round(md, 4), round(se, 4), round(D[k].std(ddof=1), 4)])
TQ = stats.t.ppf(0.975, 149)
from scipy.optimize import brentq  # noqa: E402
agree('t quantile 0.975 with 149 degrees of freedom: scipy against a root search on the cdf', TQ, brentq(lambda q: stats.t.cdf(q, 149) - 0.975, 1, 3), 1e-9, covers=[round(TQ, 3), 149])
for k in (('A', 0), ('B', 0)):
    md, se = D[k].mean(), D[k].std(ddof=1) / math.sqrt(150)
    lv.claim((md - TQ * se) * (md + TQ * se) > 0, f'{k} interval clear of 0', covers=[round(md - TQ * se, 4), round(md + TQ * se, 4), round(-(md + TQ * se), 4), round(md + 1.96 * se, 4), 1.96])
gapA = R2['A', 0, 'boost'] - R2['A', 0, 'mlp']
share = float((D['A', 0] > 0).mean())
lv.claim(abs(gapA / ORC['A', 0] - 0.25) < 0.01, 'the world A seed 0 gap is a quarter of the oracle', covers=[f4(gapA), round(gapA / ORC['A', 0], 2), round(ORC['A', 0] / gapA, 2), 0.25])
lv.claim(0 < share < 1, f'boosting has the lower error on {round(share * 150)} of 150 days', covers=[round(share, 2), round(1 - share, 2), round(share * 150), round(share * 100)])
derived = {
    'boost/oracle A0': R2['A', 0, 'boost'] / ORC['A', 0], 'oracle/boost A0': ORC['A', 0] / R2['A', 0, 'boost'], 'mlp/oracle A0': R2['A', 0, 'mlp'] / ORC['A', 0],
    'boost-ridge A0': R2['A', 0, 'boost'] - R2['A', 0, 'ridge'], 'mlp-ridge A0': R2['A', 0, 'mlp'] - R2['A', 0, 'ridge'], 'oracle-boost A1': ORC['A', 1] - R2['A', 1, 'boost'],
    'boost/oracle A1': R2['A', 1, 'boost'] / ORC['A', 1], 'mlp-boost B0': R2['B', 0, 'mlp'] - R2['B', 0, 'boost'], 'mlp-ridge B0': R2['B', 0, 'mlp'] - R2['B', 0, 'ridge'],
    'mlp-boost B1': R2['B', 1, 'mlp'] - R2['B', 1, 'boost'], 'ridge-boost B1': R2['B', 1, 'ridge'] - R2['B', 1, 'boost'], 'mlp/oracle B1': R2['B', 1, 'mlp'] / ORC['B', 1],
    'oracle/mlp B1': ORC['B', 1] / R2['B', 1, 'mlp']}
for lab, v in derived.items():
    lv.claim(bool(np.isfinite(v)), f'derived from the file\'s figures: {lab} = {v:.4f}', covers=[f4(v), round(v, 2), f4(-v)])
lv.claim(abs(T['B', 1]) < 2, 'world B seed 1 |t| below 2', covers=[round(abs(T['B', 1]), 2)])
lv.claim(sum(bool(abs(T[k]) > 2) for k in RUNS) == 3, 'three of four runs clear |t| > 2', covers=[3])
# small panel: refit world B seed 0 at 20 stocks by 200 days, the last 60 days for testing
ys, ps, ss, _ = fit('B', 0, 20, 200, 60)
r2s = {m: r2_score(ys, v) for m, v in ps.items()}
orc_s = r2_score(ys, ss)
lv.claim(r2s['mlp'] > r2s['boost'] and orc_s > max(r2s.values()), f'small panel: network {r2s["mlp"]:.4f} > boosting {r2s["boost"]:.4f}; oracle {orc_s:.4f} above all',
         covers=[round(r2s['boost'], 3), round(r2s['mlp'], 4), round(r2s['ridge'], 4), round(orc_s, 4), 2800, 20, 200, 60, 0.3])
lv.claim(r2s['mlp'] - r2s['boost'] > 0.02 and orc_s - r2s['mlp'] > 0.005, 'small-panel margins are many times any platform difference')
g = 2 * 0.004 / 0.003
lv.claim(math.ceil(g ** 2) == 8 and abs(g ** 2 - 7.11) < 0.005 and abs(g - 2.667) < 0.0005, 'seeds: k >= (2 x 0.004/0.003)^2 = 7.11, so 8', covers=[8, 7.11, 2.667, 0.004, 0.003, 7])
lv.claim(math.ceil((2 * 0.003 / 0.002) ** 2) == 9 and abs(2 * 0.003 / 0.002 - 3) < 1e-12, 'quiz: (2 x 0.003/0.002)^2 = 9', covers=[9, 0.002, 3])
lv.claim(abs(1 - 1050 / 1000 + 0.05) < 1e-12 and abs(1 - 2060 / 2000 + 0.03) < 1e-12, 'negative R2 items: -0.05 and -0.03', covers=[-0.05, 0.05, 1.05, -0.03, 0.03, 1.03, 1050, 1000, 2060, 2000])
lv.claim(abs(0.02 / (0.1 / 10) - 2) < 1e-12 and abs(0.015 / (0.08 / 8) - 1.5) < 1e-12 and abs(0.006 / 0.03 - 0.2) < 1e-12, 'paired t items: 2 and 1.5; gap share 0.2',
         covers=[2, 0.2, 1.5, 0.02, 0.1, 0.015, 0.08, 0.01, 0.006, 0.03, 5, round(0.015 / 0.08, 4)])
lv.claim(500 - 150 - 5 == 345 and 400 - 100 - 10 == 290 and 150 * 100 == 15000, 'purged split counts 345 and 290; 15,000 test rows', covers=[345, 350, 340, 290, 300, 280, 150, 15000, 3000, 400, 500])
lv.claim(abs(2 / (1 / math.sqrt(3)) - 3.4641) < 1e-4, 'hand case: differences (1, 2, 3), t = 3.46', covers=[3.46])
lv.claim(abs(1 - 0.75 / 5 - 0.85) < 1e-12, 'hand case: 1 - 0.75/5 = 0.85', covers=[0.85, 0.75])
lv.claim(abs(104 / 150 - share) < 1e-12, 'boosting wins 104 of 150 days', covers=['104/150'])
lv.claim(500 - 150 - 5 - 1 == 344 and 349 == 350 - 1 and 499 == 500 - 1 and 289 == 290 - 1 and 299 == 300 - 1 and 399 == 400 - 1, 'last day indices of each block, counting from 0', covers=[344, 349, 499, 289, 299, 399, 10])
# keys recomputed from the inputs as the screen shows them (the first error class of the review: a key from unrounded inputs)
def from_shown(ref, scr, mean, se, se_short, label):
    w = lv.files[ref]['screens'][scr]['widget']
    key, tol = w['answer'], w['tol']['abs']
    shown = lv.text(ref, f'screens[{scr}]')
    for s in (mean, se):
        lv.claim(str(s).replace('-', '') in shown.replace('−', '-').replace('-', ''), f'{label}: the screen shows {s}')
    for s, how in ((se, 'as shown'), (se_short, 'rounded to 4 places')):
        lv.claim(abs(mean / s - key) <= tol, f'{label}: {mean}/{s} = {mean / s:.4f} ({how}) lies within {key} +- {tol}')
    lv.claim(abs(round(mean / se, 2) - key) < 1e-9, f'{label}: the displayed route rounds to the key {key}')


from_shown('l10-a-fair-comparison', 3, 0.0414, 0.00787, 0.0079, 'l10 screens[3]')
from_shown('l10-a-fair-comparison', 4, 0.0436, 0.00789, 0.0079, 'l10 screens[4]')
from_shown('l11-when-the-net-wins', 2, -0.0233, 0.00676, 0.0068, 'l11 screens[2]')
for k, ref, scr in ((('A', 0), 'l10', 3), (('A', 1), 'l10', 4), (('B', 0), 'l11', 2)):
    lv.claim(abs(D[k].mean() / (D[k].std(ddof=1) / math.sqrt(150)) - lv.files[{'l10': 'l10-a-fair-comparison', 'l11': 'l11-when-the-net-wins'}[ref]]['screens'][scr]['widget']['answer']) <= 0.005,
             f'{ref} screens[{scr}]: the key is also the unrounded t', covers=[round(D[k].std(ddof=1) / math.sqrt(150), 5)])
md0 = D['A', 0].mean()
lv.claim(abs(round(md0, 5) - 0.04139) < 1e-12 and abs(md0 - TQ * 0.00787 - 0.0258) < 5e-5 and abs(md0 + TQ * 0.00787 - 0.0569) < 5e-5,
         'the interval from the displayed 0.04139 and 0.00787 is (0.0258, 0.0569) to 4 places', covers=[0.04139])
# homework h4 from the displayed inputs: upper end, and the 1.96 slip, with disjoint bands
hw = lv.files['homework-3']['items'][3]['widget']
up_t, up_z = -0.0233 + 1.976 * 0.0068, -0.0233 + 1.96 * 0.0068
wz = [x for x in hw['wrong'] if x['id'] == 'z'][0]
lv.claim(abs(up_t - hw['answer']) <= hw['tol']['abs'] and abs(up_z - wz['value']) <= wz['tol']['abs'] and abs(hw['answer'] - wz['value']) > hw['tol']['abs'] + wz['tol']['abs'],
         f'homework h4 from the displayed inputs: key {up_t:.5f}, the 1.96 slip {up_z:.5f}, the two bands disjoint')

# Newey-West: world B seed 1 under a Bartlett kernel with 5 lags, by hand and by statsmodels
import statsmodels.api as sm  # noqa: E402


def nw_t(x, lags):
    x = np.asarray(x, float)
    n, m = len(x), x.mean()
    e = x - m
    s = e @ e / n
    for lag in range(1, lags + 1):
        s += 2 * (1 - lag / (lags + 1)) * (e[lag:] @ e[:-lag]) / n
    return m / math.sqrt(s / n)


hac5 = nw_t(D['B', 1], 5)
sm5 = float(sm.OLS(D['B', 1], np.ones(150)).fit(cov_type='HAC', cov_kwds={'maxlags': 5, 'use_correction': False}).tvalues[0])
agree('Newey-West t, world B seed 1, 5 lags: by hand against statsmodels', hac5, sm5, 1e-9, covers=[round(hac5, 2)])
lv.claim(round(hac5, 2) == -2.43 and abs(T['B', 1] + 1.91) < 0.005 and abs(hac5) > 2 > abs(T['B', 1]),
         'world B seed 1: plain t -1.91, Newey-West (5 lags) t -2.43, past the bar of 2', covers=[-1.91, 5, 4])
lv.claim(round(stats.t.ppf(0.975, 7), 2) == 2.36, 'the two-sided 5% point with 7 degrees of freedom (8 seeds) is 2.36', covers=[2.36, 7])
lv.claim(500 - 150 - 4 == 346 and 345 + 1 == 346 and 500 - 150 - 8 == 342 and 400 - 100 - (11 - 1) == 290, 'validation l7 purge h - 1 for a 5-day label: 346 training days (and 342 for a double purge); 11-day label: 290',
         covers=[346, 345, 342, 4, 11, 10, 5])
l11_prelude = lv.files['l11-when-the-net-wins']['screens'][8]['widget']['prelude']
lv.claim('0.5 * np.tanh(1.5 * u) + 0.15 * u * v' in l11_prelude, 'world B signal coefficients 0.5, 1.5 and 0.15 are the l11 widget prelude\'s generator', covers=[0.5, 0.15, 1.5])
lv.literal('0.975', why='the quantile level of a 95% interval, a setting')
lv.literal('10^-6', why='a comparison tolerance, a setting')
lv.literal('ten times', why='an invented model size in a distractor')
lv.literal('50', why='invented tuning budgets in the trap (50 settings against 5)')
lv.literal('250', why='days of P&L in an invented transfer')
lv.literal('40', why='feature counts in invented scenarios')
lv.literal('15', why='a model setting: 15 leaves')
lv.literal('32', why='a model setting: two layers of 32')
lv.literal('0.0001', why='an invented tie in an edge case')
lv.literal('0.4', why='an invented t in an edge case')
lv.literal('-0.7', why='an invented t in a quiz item')

# ------------------------------------------------------------------ code widgets, through ZQ_LIB
def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        if isinstance(x, (bool, str)) or isinstance(y, (bool, str)) or x is None or y is None:
            return x == y
        try:
            rt, at = tol if tol else (1e-9, 1e-12)
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
        return bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    for k, v in (w.get('data') or {}).items():
        shutil.copy(os.path.join(APP, v), os.path.join(dd, k))
    ns = {'__learner_source__': src}
    exec(ZQ_LIB, ns)
    try:
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                tl = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (tl.get('rel') or 0, tl.get('abs') or 0) if tl else None)
            except Exception:
                ok = False
            if not ok:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        shutil.rmtree(dd, ignore_errors=True)


import warnings  # noqa: E402
warnings.filterwarnings('ignore')
nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab_ = f'{fid} {u.get("title") or u.get("id")}'
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab_}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab_}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab_}: at least two mutants')
        lv.claim(f'Submit runs {len(w["tests"])} hidden tests' in w.get('how', ''), f'{lab_}: the how line counts {len(w["tests"])} tests')
        for mu_ in w.get('mutants', []):
            nm += 1
            gg = first_fail(w, mu_['source'])
            lv.claim(gg == mu_['test'], f'{lab_}: mutant "{mu_["symptom"][:48]}" first fails test {mu_["test"]} (got {gg})')
        if 'small_panel_compare' in w['starter']:
            lv.claim(abs(eval(w['tests'][0]['expect']) - r2s['ridge']) < 1e-9 * abs(r2s['ridge']) and abs(eval(w['tests'][1]['expect']) - orc_s) < 1e-12, 'small_panel_compare expects = the script\'s refit (ridge, oracle)')
        if 'case_report' in w['starter']:
            v = eval(w['tests'][0]['expect'])
            lv.claim(v == {('A', 0): 'boosting', ('A', 1): 'boosting', ('B', 0): 'network', ('B', 1): 'no change'}, 'case_report verdicts: boosting, boosting, network, no change')
            agree('case_report t values against the paired t of the file', eval(w['tests'][2]['expect']), [T[k] for k in sorted(RUNS)], 1e-9)
print(f'code widgets {nw}, mutants {nm}')
lv.check_wrongs()
lv.report()
