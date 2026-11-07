"""stat-learning L3 performance task h-lag-split: every number recomputed.

Run with the scratchpad venv (pandas 2.2.3): exits 0 when
  - the shipped solution (route A, plain loops) passes every example and test,
  - an independent pandas build with shift and masks (route B) gives every expected value,
  - the example's rows, labels and split agree with a hand count (route C),
  - the starter fails every test,
  - each planted wrong solution fails at least one hidden test.
Grading copies app/js/engine/widgets/code.js: isclose element by element at rel 1e-9, abs 1e-12.
"""
import json
import math
import os
import random

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'stat-learning', 'homework-3.json')
FAILS = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        FAILS.append(msg)


def flat(v):
    return v.tolist() if hasattr(v, 'tolist') else v


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
            out.append(close(eval(c['call'], ns), eval(c['expect'], {})))
        except Exception:
            out.append(False)
    return out


d = json.load(open(HW))
items = d['items']
it = next(i for i in items if i['id'] == 'h-lag-split')
w = it['widget']
tests, examples = w['tests'], w['examples']

check(it.get('performance') == 'code' and w['kind'] == 'code', 'performance code item')
check(len(tests) >= 3 and len(tests) > len(examples), f'{len(tests)} tests > {len(examples)} examples')
check(6 <= len(items) <= 12, f'homework holds {len(items)} items (6 to 12)')
check(any(i.get('difficulty') == 5 for i in items), 'a difficulty 5 item present')
check(sum(1 for i in items if i.get('performance')) == 1, 'one performance item in homework-3')
check('6 hidden tests' in w['how'], 'how names 6 hidden tests')
check(examples[0]['expect'] == tests[0]['expect'] and examples[0]['call'] == tests[0]['call'], 'test 1 is the example')

# route A
check(all(run(w['solution'], examples + tests)), 'solution passes every example and test')


# route B: pandas, written apart from the solution
def pandas_split(prices, lags, horizon, split):
    p = pd.Series(prices, dtype=float)
    r = p.pct_change()                      # r_t = p_t / p_{t-1} - 1, NaN at day 0
    X = pd.concat({k: r.shift(k) for k in lags}, axis=1)[list(lags)]
    y = (p.shift(-horizon) > p).astype(int)
    ok = X.notna().all(axis=1) & p.shift(-horizon).notna()
    day = pd.Series(range(len(p)))
    train = ok & (day + horizon <= split - 1)
    test = ok & (day >= split)
    return (X[train].values.tolist(), y[train].tolist(), X[test].values.tolist(), y[test].tolist())


for k, c in enumerate(tests, 1):
    args = eval(c['call'].replace('lag_split', ''), {})
    got = pandas_split(*args)
    check(close(got, eval(c['expect'], {})), f'test {k}: pandas route agrees ({len(got[1])} train, {len(got[3])} test rows)')

# route C: the example by hand. 12 prices, lags 0 and 1, horizon 1, split 7.
# Rows need r_{t-1}, so t >= 2, and p_{t+1}, so t <= 10. Train: t + 1 <= 6, so t = 2..5.
# Day 6 is dropped (its label reads p_7). Test: t = 7..10.
P1 = [100, 101, 99, 99, 102, 104, 103, 103, 105, 102, 101, 104]
ex = eval(examples[0]['expect'], {})
check(len(ex[0]) == 4 and len(ex[2]) == 4, 'example: 4 training rows (days 2 to 5), 4 test rows (days 7 to 10)')
labels = [int(P1[t + 1] > P1[t]) for t in range(2, 11)]
check(labels == [0, 1, 1, 0, 0, 1, 0, 0, 1], 'example: labels for days 2 to 10 are 0 1 1 0 0 1 0 0 1 (day 2 is a tie, 99 to 99)')
check(ex[1] == labels[:4] and ex[3] == labels[5:], 'example: day 6 label left out of both sets')
check(close(ex[0][0], [99 / 101 - 1, 101 / 100 - 1]) and close(ex[2][0], [0.0, 103 / 104 - 1]), 'example: first rows read r_2, r_1 and r_7, r_6')
check(close(-2 / 101, ex[0][0][0]) and close(-1 / 104, ex[2][0][1]), 'example: -2/101 = -0.0198 and -1/104 = -0.00962')
# the empty training set of test 6: lags [0], horizon 1, split 2, so train needs t <= 0 but rows start at t = 1
check(eval(tests[5]['expect'], {})[:2] == ([], []), 'test 6: no training row')

# the starter fails every test
check(not any(run(w['starter'], tests)), 'starter fails every test')

# planted wrong solutions (plain Python, one slip each)
BASE = '''def lag_split(prices, lags, horizon, split):
    n = len(prices)
    r = [None] + [prices[t] / prices[t - 1] - 1 for t in range(1, n)]
    rows = []
    for t in range(START, n - horizon):
        rows.append((t, [FEAT for k in lags], 1 if prices[t + horizon] CMP prices[LBL] else 0))
    tr = [(x, y) for t, x, y in rows if TRAIN]
    te = [(x, y) for t, x, y in rows if TEST]
    SHUFFLE
    return [x for x, y in tr], [y for x, y in tr], [x for x, y in te], [y for x, y in te]
'''
DEF = dict(START='1 + max(lags)', FEAT='r[t - k]', CMP='>', LBL='t', TRAIN='t + horizon < split', TEST='t >= split', SHUFFLE='pass')


def make(**kw):
    s = BASE
    for k, v in {**DEF, **kw}.items():
        s = s.replace(k, v)
    return s


check(all(run(make(), tests)), 'planted base with no slip passes (harness sanity)')
BUGS = {
    'features shifted forward (shift(-k))': make(START='1', FEAT='r[t + k]').replace(
        'for t in range(1, n - horizon)', 'for t in range(1, min(n - horizon, n - max(lags)))'),
    'label looks back (p_t > p_{t-h})': make(START='max(1 + max(lags), horizon)').replace(
        'prices[t + horizon] > prices[t]', 'prices[t] > prices[t - horizon]'),
    'shuffled rows before the split': make(TRAIN='True', TEST='False', SHUFFLE=(
        'allr = tr; random.Random(0).shuffle(allr); '
        'k = sum(1 for t, x, y in rows if t + horizon < split); '
        'tr, te = allr[:k], allr[k + sum(1 for t, x, y in rows if split - horizon <= t < split):]')),
    'no purge: training label crosses the split (t < split)': make(TRAIN='t < split'),
    "next-day purge only (t + 1 < split)": make(TRAIN='t + 1 < split'),
    'dropped days put in the test set (t + h >= split)': make(TEST='t + horizon >= split'),
    'tie counted as a rise (>=)': make(CMP='>='),
    'lags sorted, not in the order given': make(FEAT='r[t - k]').replace('for k in lags', 'for k in sorted(lags)'),
    'rows start one day early, return wraps round (np.roll)': make(START='max(lags)').replace(
        "r = [None] + [prices[t] / prices[t - 1] - 1 for t in range(1, n)]",
        "r = [prices[t] / prices[t - 1] - 1 for t in range(n)]"),
    'price difference, not a return': make().replace('prices[t] / prices[t - 1] - 1', 'prices[t] - prices[t - 1]'),
    'test features built from the test block alone': make(TEST='t >= split + 1 + max(lags)'),
}
for name, code in BUGS.items():
    code = 'import random\n' + code
    res = run(code, tests)
    failed = [k + 1 for k, ok in enumerate(res) if not ok]
    hidden = [k for k in failed if k > 1]
    check(bool(hidden), f'planted "{name}" fails tests {failed}')

print('failures:', len(FAILS))
raise SystemExit(1 if FAILS else 0)
