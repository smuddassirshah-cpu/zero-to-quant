"""Recompute every number in validation homework-2 item h-label-purge (performance task, code).

Run from the repo root with a Python that has pandas 2.2 (the scratchpad venv):
    <venv>/bin/python docs/reports/validation-2-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (pandas shift, positional purge).
Route B is a pure-Python loop in this file: labels close by close, and the purge
as an intersection of the sets of daily-return rows each label uses.
Every expectation must equal both routes under the engine's own comparison.
The starter must fail every test, and each planted bug must fail a hidden test.
"""
import json, math, os, sys, warnings
warnings.simplefilter('ignore')
try:
    import numpy as np
    import pandas as pd
except ImportError:
    sys.exit('needs pandas: run with the venv named in docs/reports/validation-2-perf.md')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/validation/homework-2.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-label-purge')
w = item['widget']
fails = []

def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

# the engine's comparison (app/js/engine/widgets/code.js, __zq_cmp)
def _flat(v):
    return v.tolist() if hasattr(v, 'tolist') and not isinstance(v, (int, float, complex, str)) else v
def _close(x, y, tol):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=tol[0], abs_tol=tol[1])
    except Exception:
        return x == y
def judge(got, t, ns):
    exp = eval(t['expect'], ns)
    if t['compare'] == 'isclose':
        tol = (t['tol'].get('rel', 0), t['tol'].get('abs', 0)) if 'tol' in t else (1e-9, 1e-12)
        return _close(got, exp, tol)
    try:
        return bool(_flat(got) == _flat(exp))
    except Exception:
        return False

def run_tests(code):
    res = []
    for t in w['tests']:
        ns = {}
        try:
            exec(w['prelude'], ns)
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            res.append(judge(eval(t['call'], ns), t, ns))
        except Exception as e:
            res.append(type(e).__name__)
    return res

REF = '''
def label_table(px, h):
    out = px.copy() * float('nan')
    rows = px.values.tolist()
    for t in range(len(rows)):
        for j in range(len(rows[t])):
            if t + h < len(rows):
                a, b = rows[t][j], rows[t + h][j]
                if a == a and b == b:
                    out.iat[t, j] = b / a - 1
    return out

def train_dates(px, h, test_start, test_end):
    dates = [str(d)[:10] for d in px.index]
    lab = label_table(px, h).values.tolist()
    has = [any(v == v for v in row) for row in lab]
    s, e = dates.index(str(test_start)[:10]), dates.index(str(test_end)[:10])
    used = set()
    for j in range(s, e + 1):
        if has[j]:
            used |= set(range(j + 1, j + h + 1))
    out = []
    for i in range(len(dates)):
        if s <= i <= e or not has[i]:
            continue
        if used & set(range(i + 1, i + h + 1)):
            continue
        out.append(px.index[i])
    return out
'''
SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

BUGS = {
    'shifted the wrong way (label on the exit day)': variant('px.shift(-h) / px - 1', 'px / px.shift(h) - 1'),
    'shift(+h) over today': variant('px.shift(-h) / px - 1', 'px.shift(h) / px - 1'),
    'horizon one short': variant('px.shift(-h) / px - 1', 'px.shift(-(h - 1)) / px - 1'),
    'horizon one long': variant('px.shift(-h) / px - 1', 'px.shift(-(h + 1)) / px - 1'),
    'h closes, not h rows (dropna then shift): a price after the horizon': variant(
        'px.shift(-h) / px - 1',
        'px.apply(lambda s: (s.dropna().shift(-h) / s.dropna() - 1).reindex(s.index))'),
    'back-filled gaps: a price after the horizon': variant('px.shift(-h) / px - 1', 'px.bfill().shift(-h) / px.bfill() - 1'),
    'forward-filled gaps': variant('px.shift(-h) / px - 1', 'px.ffill().shift(-h) / px.ffill() - 1'),
    'pct_change with its default padding': variant('px.shift(-h) / px - 1', 'px.pct_change(h).shift(-h)'),
    'last h rows dropped': variant('px.shift(-h) / px - 1', '(px.shift(-h) / px - 1).iloc[:-h]'),
    'purge h rows each side': variant('(pos <= s - h) | (pos >= e + h)', '(pos <= s - h - 1) | (pos >= e + h + 1)'),
    'purge h - 2 each side': variant('(pos <= s - h) | (pos >= e + h)', '(pos <= s - h + 1) | (pos >= e + h - 1)'),
    'lesson rule with an inclusive end (one row short after)': variant('(pos >= e + h)', '(pos >= e + h - 1)'),
    'purge before the fold only': variant('(pos >= e + h)', '(pos > e)'),
    'no purge': variant('(pos <= s - h) | (pos >= e + h)', '(pos < s) | (pos > e)'),
    'fold rows kept in training': variant('clear & labelled', 'labelled'),
    'unlabelled dates kept': variant('clear & labelled', 'clear'),
    'last h dates dropped instead of unlabelled ones': variant(
        'labelled = label_table(px, h).notna().any(axis=1).to_numpy()', 'labelled = pos < len(px) - h'),
}

# 1. both routes give every expectation
for name, code in (('A solution', SOL), ('B pure-Python loop', REF)):
    r = run_tests(code)
    check(f'{name} passes all {len(r)} tests', all(x is True for x in r), str(r))

# 2. the starter fails every test
r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

# 3. every planted bug fails a hidden test
firsts = {}
for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    firsts[name] = bad[0] if bad else None
    check(f'bug "{name}" caught', bool(bad), f'fails tests {bad}')

# 4. the byKey line the slip meets first fits it
want = {'shifted the wrong way (label on the exit day)': 1, 'shift(+h) over today': 1, 'horizon one short': 1,
        'horizon one long': 1, 'h closes, not h rows (dropna then shift): a price after the horizon': 3,
        'back-filled gaps: a price after the horizon': 3, 'forward-filled gaps': 3,
        'pct_change with its default padding': 3, 'purge h rows each side': 7, 'purge h - 2 each side': 7,
        'lesson rule with an inclusive end (one row short after)': 7, 'purge before the fold only': 7,
        'no purge': 7, 'fold rows kept in training': 7, 'unlabelled dates kept': 7,
        'last h dates dropped instead of unlabelled ones': 10}
for name, k in want.items():
    check(f'bug "{name}" first fails test {k}', firsts[name] == k, f'first {firsts[name]}')
keys = set(item['feedback']['byKey'])
check('byKey names tests 1, 3, 7 and 10', keys == {'test-1', 'test-3', 'test-7', 'test-10'}, str(keys))

# 5. a second reading of the purge rule (positional, every fold row's window) agrees on every test
POS = REF.replace('        if has[j]:\n            used |=', '        if True:\n            used |=')
check('positional reading of the fold agrees', all(x is True for x in run_tests(POS)))

# 6. numbers stated in the prose, feedback and helpers
ns = {}; exec(w['prelude'], ns)
px = ns['desk']()
check('desk(): three shares over nine days', px.shape == (9, 3))
check('test-1: AAA label on 4 March is 101/100 - 1 = 0.01', math.isclose(px['AAA'].iloc[2] / px['AAA'].iloc[0] - 1, 0.01)
      and math.isclose((101 - 100) / 100, 0.01))
check('test-3: BBB has no close on 6 March', str(px.index[2].date()) == '2024-03-06' and math.isnan(px['BBB'].iloc[2]))
lab = ns2 = {}
exec(w['prelude'], ns2); exec(REF, ns2)
L2 = ns2['label_table'](px, 2)
check('test-3: BBB labels on 4 and 6 March are NaN', math.isnan(L2['BBB'].iloc[0]) and math.isnan(L2['BBB'].iloc[2]))
check('test-3: CCC is not listed on its first two days', px['CCC'].iloc[:2].isna().all() and px['CCC'].iloc[2:].notna().all())
check('test-7: 13 and 14 March have no label with h = 2', [str(d.date()) for d in px.index[7:]] == ['2024-03-13', '2024-03-14']
      and L2.iloc[7:].isna().all().all())
q = px.copy(); q.iloc[5] = np.nan
check('test-10: 11 March is row 5, with no close for any share', str(q.index[5].date()) == '2024-03-11' and q.iloc[5].isna().all())
t = ns['tape'](3)
check('tape(): four shares over 80 days', t.shape == (80, 4))
check('tape(): S2 has 8 halts', int(t['S2'].isna().sum()) == 8)
check('tape(): S3 lists on the 16th day', t['S3'].first_valid_index() == t.index[15])
check('tape(): S4 delists after the 61st day', t['S4'].last_valid_index() == t.index[60])
check('tape(): S1 trades every day', t['S1'].notna().all())
n_t, n_e = len(w['tests']), len(w['examples'])
check('12 tests, 1 example, tests > examples', (n_t, n_e) == (12, 1))
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('example equals test 1', w['examples'][0] == w['tests'][0])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)
check('tolerance in how is 0.000002', all(t.get('tol', {}).get('abs') in (None, 2e-06) for t in w['tests']) and '0.000002' in w['how'])

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
