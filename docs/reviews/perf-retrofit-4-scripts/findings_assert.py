"""Fails by design until each finding in review-perf-retrofit-4.md is fixed: one FAIL line per
open finding. Also prints, for each longform rubric, every passing tick set (7 or more, every
required row ticked) and the rows a pass can leave out. Run with the venv from this folder."""
import sys, os, re, json, itertools
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, ROOT

open_ = 0
def finding(fid, ok, text):
    global open_
    if not ok:
        open_ += 1
    print('%-4s %-7s %s' % ('ok' if ok else 'FAIL', fid, text))

def rubric(it):
    return it['rubric'] if 'rubric' in it else it['widget']['rubric']

def passes(rows):
    out = []
    for k in range(1, len(rows) + 1):
        for s in itertools.combinations(range(len(rows)), k):
            if sum(rows[i]['points'] for i in s) >= 7 and all(i in s for i, r in enumerate(rows) if r.get('required')):
                out.append([i + 1 for i in s])
    return out

def report(name):
    return open(os.path.join(ROOT, 'docs', 'reports', name)).read()

LONG = [('arma', 'homework-1.json', 'h-aloud-two-notes'), ('arma', 'homework-3.json', 'h-derive-arma-fan'),
        ('backtest', 'homework-4.json', 'h-reversal-note')]
for c, f, i in LONG:
    rows = rubric(item(c, f, i)); ps = passes(rows)
    left = [j + 1 for j in range(len(rows)) if any(j + 1 not in p for p in ps)]
    print('info %s: passing sets %s; rows a pass can leave out %s' % (i, ps, left))

# arma L1
a1 = item('arma', 'homework-1.json', 'h-aloud-two-notes')
finding('AR1-1', bool(rubric(a1)[2].get('required')), 'arma L1: the assumptions row (row 3) is required, so no pass skips what the question asks the test to assume')
r = report('arma-1-perf.md')
finding('AR1-2', 'l3 screen' in r and 'r-power' in r, 'arma L1 report names l3 screens 4, 9, 10, 12, review-1 r-power and homework-1 h-df-sim as overlap')
finding('AR1-3', 'Brownian' not in a1['model'] and 'not more frequent prices' not in rubric(a1)[3]['text'], 'arma L1: no follow-up model or rubric row needs an idea level 1 does not teach')

# arma L3
a3 = item('arma', 'homework-3.json', 'h-derive-arma-fan')
finding('AR3-1', bool(rubric(a3)[3].get('required')), 'arma L3: the series-variance check and numbers row (row 4) is required')

# backtest L1
b1 = item('backtest', 'homework-1.json', 'h-breakout-twice'); W1 = b1['widget']
sol = W1['solution']
loose = sol.replace('bool(np.allclose(a, b, rtol=0, atol=1e-9))', 'bool(np.allclose(a, b))')
finding('BT1-2', bool([n for k, n, ok, *_ in run(b1, loose) if k == 'test' and not ok]), 'backtest L1: an agree with np.allclose default tolerances fails a hidden test')
cheat = sol.replace('def breakout_loop(close, n):', 'def breakout_loop(close, n):\n    return _ref(close, n)\n\ndef _a(close, n):').replace(
    'def breakout_vector(close, n):', 'def breakout_vector(close, n):\n    return _ref(close, n)\n\ndef _b(close, n):')
finding('BT1-3', bool([n for k, n, ok, *_ in run(b1, cheat) if k == 'test' and not ok]), 'backtest L1: code that calls the prelude reference _ref fails a hidden test')
r = report('backtest-1-perf.md')
finding('BT1-1', 'l1 screen' in r, 'backtest L1 report names l1 screens 4, 6 and 9 as overlap and lists the new parts')

# backtest L2
b2 = item('backtest', 'homework-2.json', 'h2-never-peeks')
finding('BT2-2', 'toleran' in b2['feedback']['byKey'].get('test-9', ''), 'backtest L2: test 9 feedback says the cost leak moves cash by about £1, so a relative tolerance misses it')
r = report('backtest-2-perf.md')
finding('BT2-1', 'l8 screen' in r, 'backtest L2 report names l8 screens 2, 4, 5, 8 and 9 as overlap')

# backtest L4
b4 = item('backtest', 'homework-4.json', 'h-reversal-note'); m4 = b4['widget']['model']; rb4 = rubric(b4)
finding('BT4-1', r'\sqrt{0.4/90}' not in m4 and '−0.39' not in rb4[3]['text'] and '0.37m' not in rb4[4]['text'],
        'backtest L4: impact is charged on each trade (one book, two on a flip), as l11 and homework-2 teach, not on the average daily trade')
finding('BT4-2', bool(rb4[1].get('required')), 'backtest L4: the results row (row 2) is required, so no pass omits research against held out')
r = report('backtest-4-perf.md')
finding('BT4-3', 'outside this agent' not in r and 'l16 screen' in r, 'backtest L4 report gives the kind reason (written note with worked figures) and names l16 screens 2, 4, 5 and 10')
finding('BT4-4', 'independent' in m4, 'backtest L4: the 0.78 bar states that it assumes 30 independent settings')

# stat-learning L2
r = report('stat-learning-2-perf.md')
finding('SL2-1', re.search(r'l9 screens?[^.\n]*\b8\b', r) is not None, 'stat-learning L2 report names l9 screen 8 (constants and dummies) and no longer lists the constant column as new')

print('open findings:', open_)
sys.exit(1 if open_ else 0)
