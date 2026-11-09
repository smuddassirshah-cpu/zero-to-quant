"""backtest homework-2 h2-never-peeks: reader test function, starter, shipped solution and
reader-planted wrong tests against every example and test, with CPython times."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, report

it = item('backtest', 'homework-2.json', 'h2-never-peeks')
W = it['widget']
SOL = W['solution']

READER = '''
import numpy as np
import pandas as pd

def test_never_peeks(engine):
    bars = daily_bars(150, seed=11)
    base = engine(bars).to_numpy()
    after_open = [c for c in bars.columns if c != "open"]
    for cut in range(len(bars)):
        head = engine(bars.iloc[:cut + 1]).to_numpy()
        assert (abs(head - base[:cut + 1]) <= 1e-9).all(), cut
        alt = bars.copy()
        k = alt.columns.get_indexer(after_open)
        alt.iloc[cut, k] = alt.iloc[cut, k].to_numpy() * 1.07      # bar cut after its open
        alt.iloc[cut + 1:] = alt.iloc[cut + 1:].to_numpy()[::-1]    # later bars scrambled
        got = engine(alt).to_numpy()
        assert (abs(got[:cut] - base[:cut]) <= 1e-9).all(), cut
        assert (abs(got[cut, 1:3] - base[cut, 1:3]) <= 1e-9).all(), cut   # shares, cash
'''

def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)

PLANTS = {
    'prefix check only': SOL.split('        # 2. bar cut after its open')[0],
    'no same-bar settle check': SOL.split('        assert np.allclose(run[settled]')[0],
    'every tenth cut': swap(SOL, 'for cut in range(1, len(bars)):', 'for cut in range(10, len(bars), 10):'),
    'open of the cut bar also replaced (too strict)': swap(SOL, '        alt.iloc[cut, bars.columns.get_loc("open")] = bars["open"].iloc[cut]\n', ''),
    'target of the cut row also held (too strict)': swap(SOL, 'settled = ["shares", "cash"]', 'settled = ["target", "shares", "cash"]'),
    'pandas assert_frame_equal (rtol 1e-5)': SOL.replace('assert np.allclose(part.to_numpy(), full.iloc[:cut].to_numpy(),\n                           rtol=0, atol=1e-9), f"rows before {cut} moved"', 'pd.testing.assert_frame_equal(part, full.iloc[:cut])').replace('assert np.allclose(run.iloc[:cut].to_numpy(), full.iloc[:cut].to_numpy(),\n                           rtol=0, atol=1e-9), f"rows before {cut} read later prices"', 'pd.testing.assert_frame_equal(run.iloc[:cut], full.iloc[:cut])').replace('assert np.allclose(run[settled].iloc[cut].to_numpy(),\n                           full[settled].iloc[cut].to_numpy(),\n                           rtol=0, atol=1e-9), f"row {cut} settled after its open"', 'pd.testing.assert_series_equal(run[settled].iloc[cut], full[settled].iloc[cut])'),
    'np.allclose default tolerances': SOL.replace('rtol=0, atol=1e-9', 'rtol=1e-5, atol=1e-8'),
    'compares with clean_engine': 'def test_never_peeks(engine):\n    b = daily_bars(100)\n    assert engine(b).equals(clean_engine(b))\n',
}

fails = 0
fe, ft = report('starter', run(it, W['starter']))
if not ft: print('  FAIL starter passes'); fails += 1
for lab, src in (('shipped solution', SOL), ('reader test', READER)):
    res = run(it, src)
    fe, ft = report(lab, res)
    if fe or ft: print('  FAIL', lab); fails += 1
uncaught = []
for lab, src in PLANTS.items():
    fe, ft = report('plant: ' + lab, run(it, src))
    if not ft: uncaught.append(lab)
print('uncaught plants:', uncaught)
if set(uncaught) != {'pandas assert_frame_equal (rtol 1e-5)', 'np.allclose default tolerances'} and uncaught:
    print('  FAIL uncaught changed'); fails += 1
print('failures:', fails)
sys.exit(1 if fails else 0)
