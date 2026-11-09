"""backtest homework-1 h-breakout-twice: reader solution, starter, shipped solution and
reader-planted slips against every example and test (CPython, venv)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, report, failing

it = item('backtest', 'homework-1.json', 'h-breakout-twice')
W = it['widget']

READER = '''
import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view as _sw

def breakout_loop(close, n):
    tgt, prev_tgt, res = 0, 0, []
    for t, c in enumerate(close):
        r = 0.0 if t == 0 else close[t] / close[t - 1] - 1
        res.append(tgt * r)
        if t >= n:
            past = close[t - n:t]
            tgt = 1 if c > max(past) else (-1 if c < min(past) else tgt)
    return res

def breakout_vector(close, n):
    c = np.asarray(close, dtype=float)
    m = len(c)
    sig = np.full(m, np.nan)
    if m > n:
        win = _sw(c[:-1], n)            # win[i] = c[i:i+n], the n closes before bar i+n
        hi, lo = win.max(axis=1), win.min(axis=1)
        today = c[n:]
        s = np.where(today > hi, 1.0, np.where(today < lo, -1.0, np.nan))
        sig[n:] = s
    tgt = pd.Series(sig).ffill().fillna(0.0).to_numpy()
    r = np.zeros(m)
    if m > 1:
        r[1:] = c[1:] / c[:-1] - 1
    held = np.concatenate([[0.0], tgt[:-1]]) if m else tgt
    return list(held * r)

def agree(loop_fn, vector_fn, close, n):
    a, b = list(loop_fn(close, n)), list(vector_fn(close, n))
    return len(a) == len(b) and all(abs(x - y) <= 1e-9 for x, y in zip(a, b))
'''
SOL = W['solution']

def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)

PLANTS = {
    'channel includes today (no shift)': swap(swap(SOL, 'hi = c.rolling(n).max().shift(1)', 'hi = c.rolling(n).max()'), 'lo = c.rolling(n).min().shift(1)', 'lo = c.rolling(n).min()'),
    'vector: target not lagged (same bar)': swap(SOL, 'target.shift(1).fillna(0.0) * ret', 'target * ret'),
    'loop: target updated before booking': swap(swap(SOL, '        out.append(target * ret)              # the target set at t - 1 earns it\n', ''), '    return out\n\n\ndef breakout_vector', '        out.append(target * ret)\n    return out\n\n\ndef breakout_vector'),
    'ties count as a breakout (>=)': swap(swap(SOL, 'np.where(c > hi', 'np.where(c >= hi'), 'np.where(c < lo, -1.0', 'np.where(c <= lo, -1.0'),
    'vector: no hold (flat inside the channel)': swap(SOL, 'np.where(c < lo, -1.0, np.nan)', 'np.where(c < lo, -1.0, 0.0)'),
    'agree: np.allclose with default tolerances': swap(SOL, 'bool(np.allclose(a, b, rtol=0, atol=1e-9))', 'bool(np.allclose(a, b))'),
    'agree: relative 1e-6': swap(SOL, 'bool(np.allclose(a, b, rtol=0, atol=1e-9))', 'bool(np.allclose(a, b, rtol=1e-6, atol=0))'),
    'agree: zip, no length check': swap(SOL, 'return a.shape == b.shape and bool(np.allclose(a, b, rtol=0, atol=1e-9))', 'return all(abs(x - y) <= 1e-9 for x, y in zip(a, b))'),
    'cheat: both functions call the prelude _ref': SOL.replace('def breakout_loop(close, n):', 'def breakout_loop(close, n):\n    return _ref(close, n)\n\ndef _old_loop(close, n):').replace('def breakout_vector(close, n):', 'def breakout_vector(close, n):\n    return _ref(close, n)\n\ndef _old_vec(close, n):'),
    'cheat: agree is the prelude _close': SOL.replace('def agree(loop_fn, vector_fn, close, n):', 'def agree(loop_fn, vector_fn, close, n):\n    return _close(loop_fn(close, n), vector_fn(close, n))\n\ndef _old_agree(loop_fn, vector_fn, close, n):'),
}

fails = 0
fe, ft = report('starter', run(it, W['starter']))
if not ft: print('  FAIL starter passes'); fails += 1
for lab, src in (('shipped solution', SOL), ('reader solution', READER)):
    fe, ft = report(lab, run(it, src))
    if fe or ft: print('  FAIL', lab); fails += 1
uncaught = []
for lab, src in PLANTS.items():
    fe, ft = report('plant: ' + lab, run(it, src))
    if not ft: uncaught.append(lab)
print('uncaught plants:', uncaught)
# _no_loop on the cheat: the prelude reference is not a learner function, so the check cannot see it
expected_uncaught = {'agree: np.allclose with default tolerances',
                     'cheat: both functions call the prelude _ref', 'cheat: agree is the prelude _close'}
if set(uncaught) != expected_uncaught:
    print('  FAIL uncaught set changed:', set(uncaught) ^ expected_uncaught); fails += 1
print('failures:', fails)
sys.exit(1 if fails else 0)
