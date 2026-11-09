"""Recompute every number in alpha homework-1 item h-review-universe (performance task, code).

Run from the repo root with a Python that has pandas 2.2 (the scratchpad venv):
    <venv>/bin/python docs/reports/alpha-1-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (rolling mean, one list per review date).
Route B is an independent day-by-day loop in this file that shares no code with it.
Every test expectation must equal both routes. The starter must fail every test,
and each planted bug must fail at least one hidden test (the one named beside it).
"""
import json, os, sys
try:
    import pandas as pd  # noqa: F401
except ImportError:
    sys.exit('needs pandas: run with the venv named in docs/reports/alpha-1-perf.md')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/alpha/homework-1.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-review-universe')
w = item['widget']
fails = []

def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

REF = '''import pandas as pd
def review_universe(close, shares, listed, n, window):
    dates, cols = list(close.index), list(close.columns)
    out = pd.DataFrame(False, index=close.index, columns=close.columns)
    current = []
    for i, d in enumerate(dates):
        for c in current:                      # yesterday's list, if listed today
            if bool(listed.iloc[i][c]):
                out.iloc[i, cols.index(c)] = True
        last = i + 1 == len(dates) or (dates[i + 1].year, dates[i + 1].month) != (d.year, d.month)
        if last:
            score = []
            for c in cols:
                if i + 1 < window or not bool(listed.iloc[i][c]):
                    continue
                v = [close.iloc[k][c] * shares.iloc[k][c] for k in range(i - window + 1, i + 1)]
                if any(x != x for x in v):
                    continue
                score.append((-sum(v) / window, c))
            current = [c for _, c in sorted(score)[:n]]
    return out
'''

SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

BUGS = {
    # look-ahead: each month uses the list chosen at its own close
    'same-month list': '''import pandas as pd
def review_universe(close, shares, listed, n, window):
    adv = (close * shares).rolling(window, min_periods=window).mean()
    month = close.index.to_period("M")
    out = pd.DataFrame(False, index=close.index, columns=close.columns)
    for m in month.unique():
        d = close.index[month == m][-1]
        s = adv.loc[d][listed.loc[d]].dropna().sort_index()
        out.loc[month == m, s.sort_values(ascending=False, kind="mergesort").index[:n]] = True
    return out & listed
''',
    'traded on the review day': variant('held = close.index > d', 'held = close.index >= d'),
    'full-sample mean volume (look-ahead)': variant(
        'adv = gbp.rolling(window, min_periods=window).mean()',
        'adv = pd.DataFrame([gbp.mean()] * len(gbp), index=gbp.index)'),
    'window peeks one day ahead': variant(
        'adv = gbp.rolling(window, min_periods=window).mean()',
        'adv = gbp.rolling(window, min_periods=window).mean().shift(-1)'),
    'partial window allowed': variant('min_periods=window', 'min_periods=1'),
    'dead share kept to next review': variant('return out & listed', 'return out'),
    'ranks shares traded, not £': variant('gbp = close * shares', 'gbp = shares + 0 * close'),
    'rank <= n keeps ties': variant(
        'picked = s.sort_values(ascending=False, kind="mergesort").index[:n]',
        'picked = s.index[s.rank(ascending=False, method="min") <= n]'),
    'smallest volume first': variant('ascending=False', 'ascending=True'),
    # fix pass AL1-1: product of the means, not the mean of the products
    'product of the means': variant('adv = gbp.rolling(window, min_periods=window).mean()',
        'adv = close.rolling(window, min_periods=window).mean() * shares.rolling(window, min_periods=window).mean()'),
}

def run_tests(code):
    """Results per test: True (pass), False (wrong) or the error name."""
    res = []
    for t in w['tests']:
        ns = {}
        try:
            exec(w['prelude'], ns)
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            res.append(repr(got) == t['expect'])
        except Exception as e:  # a crash is a fail
            res.append(type(e).__name__)
    return res

# 1. both routes give every expectation
for name, code in (('A solution', SOL), ('B day-by-day loop', REF)):
    r = run_tests(code)
    check(f'{name} passes all {len(r)} tests', all(x is True for x in r), str(r))

# 2. the starter fails every test
r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

# 3. each planted bug fails at least one hidden test (test number, 1-based)
for name, code in BUGS.items():
    r = run_tests(code)
    first = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'bug "{name}" caught', bool(first), f'fails tests {first}')

# 4. the byKey lines name the slip that first fails there
want_first = {'traded on the review day': 3, 'dead share kept to next review': 4,
              'partial window allowed': 2, 'ranks shares traded, not £': 2}
for name, k in want_first.items():
    r = run_tests(BUGS[name])
    check(f'bug "{name}" fails test {k}', r[k - 1] is not True)
for name, k in (('partial window allowed', 5), ('ranks shares traded, not £', 6),
                ('same-month list', 7), ('full-sample mean volume (look-ahead)', 7),
                ('window peeks one day ahead', 7), ('rank <= n keeps ties', 8), ('product of the means', 12)):
    check(f'bug "{name}" fails byKey test {k}', run_tests(BUGS[name])[k - 1] is not True)

# 5. counts stated in the item
ns = {}; exec(w['prelude'], ns)
c, s, l = ns['hand']()
check('hand(): five shares, 32 days', c.shape == (32, 5), str(c.shape))
check('hand(): D last listed 14 February', str(c['D'].last_valid_index().date()) == '2024-02-14')
check('hand(): B trades the most shares, at £1', s.max().idxmax() == 'B' and c['B'].iloc[0] == 1.0)
check('hand(): C has two days at the February review',
      int(c.loc[:'2024-02-29', 'C'].notna().sum()) == 2)
gbp = (c * s).loc['2024-01-29':'2024-01-31'].mean()
check('January list by £ volume is D then A', list(gbp.sort_values(ascending=False).index[:2]) == ['D', 'A'], str(gbp.to_dict()))
bc = ns['book'](7)[0]
check('book(): 12 shares, 130 days', bc.shape == (130, 12))
n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 12, examples 1, tests > examples', (n_t, n_e) == (12, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('examples equal test 1', w['examples'][0] == w['tests'][0])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
