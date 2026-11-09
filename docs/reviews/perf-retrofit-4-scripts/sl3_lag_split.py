"""stat-learning homework-3 h-lag-split: reader pandas solution, starter, shipped solution and
reader-planted slips on every example and test."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, report

it = item('stat-learning', 'homework-3.json', 'h-lag-split')
W = it['widget']
SOL = W['solution']

READER = '''
import pandas as pd

def lag_split(prices, lags, horizon, split):
    p = pd.Series(prices, dtype=float)
    r = p / p.shift(1) - 1
    feats = pd.concat([r.shift(k) for k in lags], axis=1)
    label = (p.shift(-horizon) > p).astype(int)
    ok = feats.notna().all(axis=1) & p.shift(-horizon).notna()
    day = pd.Series(range(len(p)))
    train = ok & (day + horizon < split)
    test = ok & (day >= split)
    return (feats[train].values.tolist(), label[train].tolist(),
            feats[test].values.tolist(), label[test].tolist())
'''

def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)

PLANTS = {
    'training rule t < split (no purge at all)': swap(SOL, 'if t + horizon < split:', 'if t < split:'),
    'training rule t + horizon <= split (label on day split allowed)': swap(SOL, 'if t + horizon < split:', 'if t + horizon <= split:'),
    'label over one day whatever h': swap(SOL, 'label = 1 if prices[t + horizon] > prices[t] else 0', 'label = 1 if prices[t + 1] > prices[t] else 0'),
    'first row one day late (range from 2 + max)': swap(SOL, 'for t in range(1 + max(lags), n - horizon):', 'for t in range(2 + max(lags), n - horizon):'),
    'last labelled day dropped': swap(SOL, 'for t in range(1 + max(lags), n - horizon):', 'for t in range(1 + max(lags), n - horizon - 1):'),
    'log returns': swap(SOL, 'r = [None] + [prices[t] / prices[t - 1] - 1 for t in range(1, n)]', 'r = [None] + [__import__("math").log(prices[t] / prices[t - 1]) for t in range(1, n)]'),
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
