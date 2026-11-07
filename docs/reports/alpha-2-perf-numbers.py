"""Recompute every number in alpha homework-2 item h-momentum-pct (performance task, code).

Run from the repo root with a Python that has pandas 2.2 (the scratchpad venv):
    <venv>/bin/python docs/reports/alpha-2-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (shift, where, rank with pct=True).
Route B is an independent loop in this file: plain Python ratios and a hand-written average rank.
Every test expectation must equal both routes. The starter must fail every test,
and each planted bug must fail at least one hidden test (the byKey test named beside it).
"""
import json, os, sys
try:
    import pandas as pd  # noqa: F401
except ImportError:
    sys.exit('needs pandas: run with the venv named in docs/reports/alpha-2-perf.md')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/alpha/homework-2.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-momentum-pct')
w = item['widget']
fails = []

def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

REF = '''import math
import pandas as pd
def momentum_pct(px, lookback=12, skip=1):
    out = pd.DataFrame(float("nan"), index=px.index, columns=px.columns)
    v = px.values.tolist()
    for t in range(len(v)):
        if t - lookback < 0:
            continue
        score = {}
        for j, c in enumerate(px.columns):
            now, end, start = v[t][j], v[t - skip][j], v[t - lookback][j]
            if any(math.isnan(x) for x in (now, end, start)):
                continue
            score[c] = end / start - 1
        k = len(score)
        for c, s in score.items():
            below = sum(1 for x in score.values() if x < s)
            same = sum(1 for x in score.values() if x == s)
            out.loc[px.index[t], c] = (below + (same + 1) / 2) / k   # average rank / count
    return out
'''

SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

BUGS = {
    'no skip (window ends at t)': variant('px.shift(skip) / px.shift(lookback)', 'px / px.shift(lookback)'),
    'time-series rank': variant('mom.rank(axis=1, pct=True)', 'mom.rank(pct=True)'),
    'look-ahead (shift the wrong way)': variant('px.shift(skip) / px.shift(lookback)', 'px.shift(-skip) / px.shift(lookback)'),
    'no listed-today check': variant('mom = mom.where(px.notna())', 'pass'),
    'window starts a month early': variant('px.shift(lookback) - 1', 'px.shift(lookback + skip) - 1'),
    'raw rank, not divided': variant('rank(axis=1, pct=True)', 'rank(axis=1)'),
    'unscored shares ranked as 0': variant('mom.rank(axis=1, pct=True)', 'mom.fillna(0).rank(axis=1, pct=True).where(mom.notna())'),
    'strongest scores lowest': variant('rank(axis=1, pct=True)', 'rank(axis=1, pct=True, ascending=False)'),
    'ties by order': variant('rank(axis=1, pct=True)', 'rank(axis=1, pct=True, method="first")'),
    'scaled (r - 1)/(n - 1)': variant('return mom.rank(axis=1, pct=True)',
        'r = mom.rank(axis=1)\n    return r.sub(1).div(mom.notna().sum(axis=1) - 1, axis=0)'),
}

def run_tests(code):
    res = []
    for t in w['tests']:
        ns = {}
        try:
            exec(w['prelude'], ns)
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            res.append(got == eval(t['expect'], ns) and repr(got) == t['expect'])
        except Exception as e:
            res.append(type(e).__name__)
    return res

for name, code in (('A solution', SOL), ('B plain loop', REF)):
    r = run_tests(code)
    check(f'{name} passes all {len(r)} tests', all(x is True for x in r), str(r))

r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

for name, code in BUGS.items():
    r = run_tests(code)
    first = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'bug "{name}" caught', bool(first), f'fails tests {first}')

# byKey lines: each names a slip that fails at that test
for k, name in (('test-4', 'no skip (window ends at t)'), ('test-5', 'no listed-today check'),
                ('test-7', 'look-ahead (shift the wrong way)'), ('test-8', 'ties by order'),
                ('test-6', 'window starts a month early')):
    check(f'byKey {k} present', k in item['feedback']['byKey'])
    check(f'bug "{name}" fails {k}', run_tests(BUGS[name])[int(k[5:]) - 1] is not True)

# figures stated in the item and the explain text
ns = {}; exec(w['prelude'], ns)
px = ns['months']()
check('months(): 14 month ends, five shares', px.shape == (14, 5))
b_last = px['B'].iloc[-1] / px['B'].iloc[-2] - 1
check("B's last month is a jump of 30%", abs(b_last - 0.30) < 1e-12, f'{b_last:.6f}')
check('D unlisted from January 2024', str(px['D'].last_valid_index().date()) == '2023-12-31')
check('C listed from June 2023', str(px['C'].first_valid_index().date()) == '2023-06-30')
check('monthly_panel(): 30 shares', ns['monthly_panel'](11).shape == (40, 30))
n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 12, examples 1, tests > examples', (n_t, n_e) == (12, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('example equals test 1', w['examples'][0] == w['tests'][0])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
