"""Recompute every number in validation homework-3 item h-dead-firms (performance task, code).

Run from the repo root with a Python that has pandas 2.2 (the scratchpad venv):
    <venv>/bin/python docs/reports/validation-3-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (a held mask from the records, rets.where).
Route B is a pure-Python loop in this file: month by month, firm by firm.
Every expectation must equal both routes under the engine's own comparison.
The starter must fail every test, and each planted bug must fail a hidden test.
"""
import json, math, os, sys, warnings
warnings.simplefilter('ignore')
try:
    import numpy as np
    import pandas as pd
except ImportError:
    sys.exit('needs pandas: run with the venv named in docs/reports/validation-3-perf.md')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/validation/homework-3.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-dead-firms')
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

REF = """
import pandas as pd
def survivor_free_returns(rets, listings, delist):
    rec = {f: (a, b) for f, a, b in listings}
    held, ret = [], []
    for m in list(rets.index):
        vals = []
        for f in rets.columns:
            if f not in rec:
                continue
            a, b = rec[f]
            if not (a <= m and (b is None or m <= b)):
                continue
            x = float(rets.at[m, f])
            if m == b:
                x = (1 + (0.0 if x != x else x)) * (1 + delist[f]) - 1
            vals.append(x)
        held.append(len(vals))
        ret.append(sum(vals) / len(vals))
    return pd.DataFrame({"held": held, "ret": ret}, index=rets.index)
"""
SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

ALIVE = 'alive = (months >= first) & ((months <= last) if last else True)'
COMP = 'r.loc[last, firm] = (1 + base) * (1 + delist[firm]) - 1'
BUGS = {
    "universe from today's listing (still listed, every month)": variant(ALIVE, 'alive = (last is None)'),
    "universe from today's file (a return in the last month)": variant(ALIVE, 'alive = bool(rets[firm].notna().iloc[-1])'),
    'universe from which firms have returns (back-fill)': variant('r.where(held)', 'r.where(rets.notna())').replace(
        '"held": held.sum(axis=1)', '"held": rets.notna().sum(axis=1)'),
    'listing month ignored (late listers held from the start)': variant(ALIVE, 'alive = ((months <= last) if last else True)'),
    'dead firm dropped in its last month': variant(ALIVE, 'alive = (months >= first) & ((months < last) if last else True)'),
    'dead firm dropped when it has no regular return': variant(ALIVE, ALIVE + '\n        alive = alive & rets[firm].notna().to_numpy()'),
    'dead firm dropped a month early (both ends exclusive)': variant(ALIVE, 'alive = (months > first) & ((months < last) if last else True)'),
    'delisting return ignored': variant(COMP, 'pass'),
    'delisting return replaces the regular return': variant(COMP, 'r.loc[last, firm] = delist[firm]'),
    'delisting return added, not compounded': variant(COMP, 'r.loc[last, firm] = base + delist[firm]'),
    'no regular return left as NaN': variant("            base = 0.0 if np.isnan(base) else base\n", ''),
    'delisting return a month late': variant('        if last in months:\n            base = r.loc[last, firm]',
        '        nxt = months[list(months).index(last) + 1] if last in months and last != months[-1] else None\n        if nxt is not None:\n            last = nxt\n            base = r.loc[last, firm]'),
    'mean over every firm, gaps as 0': variant('r.where(held).mean(axis=1)', 'r.where(held).fillna(0).mean(axis=1)'),
    'record end outside the file not guarded': variant('if last in months:', 'if last:'),
}

for name, code in (('A solution', SOL), ('B month-by-month loop', REF)):
    r = run_tests(code)
    check(f'{name} passes all {len(r)} tests', all(x is True for x in r), str(r))

r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

firsts = {}
for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    firsts[name] = bad[0] if bad else None
    check(f'bug "{name}" caught', bool(bad), f'fails tests {bad}')

want = {"universe from today's listing (still listed, every month)": 1,
        "universe from today's file (a return in the last month)": 1,
        'universe from which firms have returns (back-fill)': 1,
        'listing month ignored (late listers held from the start)': 1,
        'dead firm dropped in its last month': 2,
        'dead firm dropped when it has no regular return': 2,
        'dead firm dropped a month early (both ends exclusive)': 1,
        'delisting return ignored': 3, 'delisting return replaces the regular return': 3,
        'delisting return added, not compounded': 3, 'no regular return left as NaN': 3,
        'delisting return a month late': 3, 'mean over every firm, gaps as 0': 1,
        'record end outside the file not guarded': 5}
for name, k in want.items():
    check(f'bug "{name}" first fails test {k}', firsts[name] == k, f'first {firsts[name]}')
keys = set(item['feedback']['byKey'])
check('byKey names tests 1, 2, 3 and 5', keys == {'test-1', 'test-2', 'test-3', 'test-5'}, str(keys))

# numbers stated in the prose, feedback and helpers, each by a second route
ns = {}; exec(w['prelude'], ns)
rets, listings, delist = ns['market']()
check('market(): five firms over eight months', rets.shape == (8, 5) and len(listings) == 5)
jan = [f for f, a, b in listings if a <= '2023-01' and (b is None or '2023-01' <= b)]
check('test-1: AAA, BBB, CCC and EEE listed in January', jan == ['AAA', 'BBB', 'CCC', 'EEE'], str(jan))
check("test-1: today's list is AAA, CCC, DDD", [f for f, a, b in listings if b is None] == ['AAA', 'CCC', 'DDD'])
check('test-1: DDD has back-filled returns before April', rets.loc[:'2023-03', 'DDD'].notna().all())
check('test-2: DDD lists in April, BBB dies in May, EEE in July',
      dict((f, (a, b)) for f, a, b in listings)['DDD'][0] == '2023-04' and dict((f, b) for f, a, b in listings)['BBB'] == '2023-05'
      and dict((f, b) for f, a, b in listings)['EEE'] == '2023-07')
v = (1 - 0.20) * (1 - 0.40) - 1
check('test-3: BBB May (1 - 0.20)(1 - 0.40) - 1 = -0.52', abs(v + 0.52) < 1e-12 and abs((-0.2 - 0.4 + 0.08) + 0.52) < 1e-12
      and abs(rets.at['2023-05', 'BBB'] + 0.20) < 1e-12 and delist['BBB'] == -0.40)
check('test-3: EEE has no regular return in July, delisting return -0.30',
      rets.at['2023-07', 'EEE'] != rets.at['2023-07', 'EEE'] and delist['EEE'] == -0.30)
may = (0.00 + v + 0.03 + 0.03 - 0.07) / 5
jul = (-0.02 + 0.02 + 0.05 - 0.30) / 4
check('May portfolio -0.106 and July -0.0625 by hand', abs(may + 0.106) < 1e-12 and abs(jul + 0.0625) < 1e-12)
for s in (2, 5, 7):
    R, L, Dl = ns['exchange'](s)
    check(f'exchange({s}): 30 firms over 60 months', R.shape == (60, 30) and len(L) == 30)
    lastof = {f: b for f, a, b in L}
    check(f'exchange({s}): some deaths, some with no regular return in the last month, some late listers',
          len(Dl) >= 5 and any(R.at[lastof[f], f] != R.at[lastof[f], f] for f in Dl) and sum(a != '2015-01' for f, a, b in L) == 10,
          f'{len(Dl)} deaths')
    late = [(f, a) for f, a, b in L if a != '2015-01']
    i0 = list(R.index).index(late[0][1])
    check(f'exchange({s}): back-filled months before a late listing', R[late[0][0]].iloc[max(0, i0 - 12):i0].notna().all())
n_t, n_e = len(w['tests']), len(w['examples'])
check('8 tests, 1 example, tests > examples', (n_t, n_e) == (8, 1))
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('example equals test 1', w['examples'][0] == w['tests'][0])
check('tolerances match how', '0.000002' in w['how'] and '0.0002' in w['how'] and
      {json.dumps(t.get('tol')) for t in w['tests']} == {'null', '{"abs": 2e-06}', '{"abs": 0.0002}'})
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
