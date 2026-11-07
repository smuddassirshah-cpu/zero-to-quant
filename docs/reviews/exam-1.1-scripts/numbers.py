"""Second reader's number script for app/content/exams/topic-1.1.json (review-exam-1.1.md).

Recomputes every graded key and every wrong[] value, the numbers in prose, feedback and explanations, runs every
code-reading snippet the items print from (the fenced code in each prose, with the data the item states), and runs
the four code items: the solution passes every example and hidden test, the starter fails at least one, and planted
bugs show which test fails first (the engine's byKey "test-N" is the first failing test). The longform's buggy script
and its model answer are run on a newest-first file of the model's own hand path.
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Needs the Pyodide 0.27.7 versions: numpy 2.0.2, pandas 2.2.3, matplotlib 3.8.4.
Run: <venv>/bin/python docs/reviews/exam-1.1-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (NumPy imports it).
# Drop the script's own folder from the path before any other import.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import contextlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.1.json')
COURSES = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
print(f'numpy {np.__version__}, pandas {pd.__version__}, matplotlib {matplotlib.__version__}')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}
IT = {it['id']: it for it in doc['items']}


def P(iid):
    return f'items[{idx[iid]}]'


def node(path):
    return _walk(doc, path)[0]


def near(a, b, t):
    return abs(a - b) <= t


def key(iid, value, path='widget', t=None):
    """The graded answer equals the recomputed value, within a tenth of its tolerance (or t)."""
    w = node(f'{P(iid)}.{path}')
    tol = w.get('tol', {}).get('abs', 0)
    t = t if t is not None else max(tol / 10, 1e-9)
    ok = near(w['answer'], value, t)
    ex._rec(ok, f'{iid} {path} answer {w["answer"]!r} = {value:.6g}', '' if ok else 'recomputed value differs')


def inband(iid, typed, path='widget', label='typed answer'):
    w = node(f'{P(iid)}.{path}')
    ok = abs(typed - w['answer']) <= w['tol']['abs'] + 1e-9
    ex._rec(ok, f'{iid} {label} {typed!r} graded right', '' if ok else 'outside the answer tolerance')


def wrong(iid, wid, value, typed=None, t=None):
    w = node(f'{P(iid)}.widget')
    ws = [x for x in w['wrong'] if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]
    tt = t if t is not None else max(v.get('tol', {}).get('abs', 1e-9), 1e-9)
    ok = near(v['value'], value, tt)
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {value:.6g}', '' if ok else 'recomputed slip differs')
    if typed is not None:
        ok2 = abs(typed - v['value']) <= v.get('tol', {}).get('abs', 1e-9) + 1e-9
        ex._rec(ok2, f'{iid} wrong "{wid}" catches a typed {typed!r}', '' if ok2 else 'typed slip misses its own band')


def correct_ids(iid):
    return sorted(o['id'] for o in IT[iid]['widget']['options'] if o.get('correct'))


def opt(iid, oid):
    return [o for o in IT[iid]['widget']['options'] if o['id'] == oid][0]['text']


def code_of(iid, field='prose'):
    m = re.search(r'```python\n(.*?)```', IT[iid][field], re.S)
    return m.group(1)


def run_snippet(src, pre=''):
    """Run code as the item shows it; return (printed text, exception name or None, namespace)."""
    ns = {'np': np, 'pd': pd, 'plt': plt}
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(pre, ns)
            exec(src, ns)
        except Exception as e:  # noqa: BLE001
            err = type(e).__name__
    return buf.getvalue().strip(), err, ns


def strip_ticks(s):
    return s.strip().strip('`')


# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['minutes'] == 60 and doc['pass'] == 0.7, 'minutes 60 and pass 0.7 as stored')
hours = 150  # docs/curriculum.md row 1.1; learn.js examMinutes(h) = 45 if h <= 60, 60 if h <= 150, else 90
ex.claim((45 if hours <= 60 else 60 if hours <= 150 else 90) == doc['minutes'], 'minutes follow learn.js examMinutes(150 h)')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 13, 4: 5, 5: 3}, f'ramp {ramp} (19%, 50%, 19%, 12% against 20, 50, 20, 10)')
union = {}
for c in ('py-found', 'numpy-pandas', 'plotting'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the three course.json maps (15 ids)')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
rub = sum(r['points'] for r in IT['e-exit-review']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')
ex.claim(all('pace' not in it for it in doc['items']), 'no item carries pace (as found)')

# ---------------------------------------------------------------- e-slice-window
out, err, _ = run_snippet(code_of('e-slice-window'))
ex.claim(out == strip_ticks(opt('e-slice-window', 'a')) and correct_ids('e-slice-window') == ['a'], f'e-slice-window prints {out}')
closes = [100.0, 101.5, 99.8, 102.3, 103.1]
ex.claim(str(closes[-3:]) == strip_ticks(opt('e-slice-window', 'b')), 'e-slice-window b is the slice that keeps the stop')
ex.claim(str(closes[1:3]) == strip_ticks(opt('e-slice-window', 'c')), 'e-slice-window c is each index one place early')

# ---------------------------------------------------------------- e-mask-sum
r = np.array([0.012, -0.021, 0.034, -0.009, 0.018])
out, _, _ = run_snippet(code_of('e-mask-sum'))
ex.claim(math.isclose(float(out), -0.03), f'e-mask-sum prints {out}')
key('e-mask-sum', r[r < 0].sum())
wrong('e-mask-sum', 'count', (r < 0).sum(), typed=2)
wrong('e-mask-sum', 'positives', r[r > 0].sum(), typed=0.064)
wrong('e-mask-sum', 'all', r.sum(), typed=0.034)

# ---------------------------------------------------------------- e-rebased-gap
h, k_ = 2750 / 2500 * 100, 38 / 40 * 100
key('e-rebased-gap', h - k_)
ex.expect('exam', f'{P("e-rebased-gap")}.explain.text', 110)
ex.expect('exam', f'{P("e-rebased-gap")}.explain.text', 95)
wrong('e-rebased-gap', 'pounds', 2750 - 38, typed=2712)
wrong('e-rebased-gap', 'changes', (2750 - 2500) - (38 - 40), typed=252)

# ---------------------------------------------------------------- e-pct-change
out, _, _ = run_snippet(code_of('e-pct-change'))
ex.claim(out == strip_ticks(opt('e-pct-change', 'a')) and correct_ids('e-pct-change') == ['a'], f'e-pct-change prints {out}')
s = pd.Series([50.0, 55.0, 44.0])
ex.claim(str(s.diff().round(2).tolist()) == strip_ticks(opt('e-pct-change', 'c')), 'e-pct-change c is diff()')
ex.claim(str((s.shift(-1) / s - 1).round(2).tolist()) == strip_ticks(opt('e-pct-change', 'd')), 'e-pct-change d is the look-ahead return')

# ---------------------------------------------------------------- e-flat-book
out, _, ns = run_snippet(code_of('e-flat-book'))
ex.claim(out == strip_ticks(opt('e-flat-book', 'a')) and correct_ids('e-flat-book') == ['a'], f'e-flat-book prints {out}')
ex.claim(ns['book'] == {'BP': 0, 'VOD': 0, 'AZN': 50}, 'e-flat-book explain: BP 0, VOD 0, AZN 50')

# ---------------------------------------------------------------- e-weights-shape
_, _, ns = run_snippet(code_of('e-weights-shape'), pre='R = np.random.default_rng(1).normal(0, 0.01, (252, 4))')
ex.claim(ns['port'].shape == (252,) and correct_ids('e-weights-shape') == ['a'], 'e-weights-shape port.shape (252,)')
ex.claim(np.allclose(ns['port'], ns['R'] @ ns['w']), 'e-weights-shape explain: equals R @ w')

# ---------------------------------------------------------------- e-sharex
pre = 'days = np.arange(1, 61)\ncloses = 100 + np.cumsum(np.random.default_rng(2).normal(0, 1, 60))\nrets = closes[1:] / closes[:-1] - 1'
_, err, ns = run_snippet(code_of('e-sharex'), pre=pre)
xl = ns['bottom'].get_xlim()
ex.claim(err is None and xl == (1.0, 30.0) and correct_ids('e-sharex') == ['a'], f'e-sharex bottom.get_xlim() {xl}')
plt.close('all')

# ---------------------------------------------------------------- e-loc-iloc
cv = IT['e-loc-iloc']['canvas']['params']
df = pd.DataFrame({'close': [float(r_[1]) for r_ in cv['rows']], 'volume': [int(r_[2]) for r_ in cv['rows']]},
                  index=pd.to_datetime([r_[0] for r_ in cv['rows']]))
_, err, ns = run_snippet(code_of('e-loc-iloc'), pre='')
ns2 = {'df': df, 'pd': pd}
exec(code_of('e-loc-iloc'), ns2)
for row, name in enumerate(['v1', 'v2', 'v3', 'n']):
    key('e-loc-iloc', float(ns2[name]), path=f'widget.rows[{row}][1]')
ex.expect('exam', f'{P("e-loc-iloc")}.feedback.byKey.r2c1', 12.70)

# ---------------------------------------------------------------- e-truncated-bars
ex.claim(near((4.1 - 3.8) / (3.9 - 3.8), 3, 1e-9) and correct_ids('e-truncated-bars') == ['a'], 'e-truncated-bars drawn ratio 3 from a 3.8% base')

# ---------------------------------------------------------------- e-imported-name (run as files)
with tempfile.TemporaryDirectory() as tdir:
    with open(os.path.join(tdir, 'tools.py'), 'w') as f:
        f.write(code_of('e-imported-name'))
    with open(os.path.join(tdir, 'report.py'), 'w') as f:
        f.write('import tools\n')
    got = subprocess.run([sys.executable, 'report.py'], cwd=tdir, capture_output=True, text=True).stdout.strip()
ex.claim(got == 'tools' and strip_ticks(opt('e-imported-name', 'a')) == got, f'e-imported-name python report.py prints {got!r}')

# ---------------------------------------------------------------- e-annual-vol
r = np.array([0.01, -0.01, 0.02, 0.00])
vol = r.std(ddof=1) * np.sqrt(252)
key('e-annual-vol', vol)
inband('e-annual-vol', 0.2049, label='typed 20.49%')
wrong('e-annual-vol', 'ddof0', r.std() * np.sqrt(252), typed=0.1775)
wrong('e-annual-vol', 'times252', r.std(ddof=1) * 252, typed=3.2533)
wrong('e-annual-vol', 'daily', r.std(ddof=1), typed=0.0129)
ex.claim(near(((r - r.mean()) ** 2).sum(), 0.0005, 1e-12) and near(r.mean(), 0.005, 1e-12), 'e-annual-vol explain: mean 0.005, squares 0.0005')
ex.expect('exam', f'{P("e-annual-vol")}.explain.text', round(r.std(ddof=1), 5))
ex.expect('exam', f'{P("e-annual-vol")}.explain.text', round(math.sqrt(252), 2))

# ---------------------------------------------------------------- e-mdd-series
px = np.array(IT['e-mdd-series']['canvas']['params']['series'][0]['values'])
peak = np.maximum.accumulate(px)
dd = 1 - px / peak
key('e-mdd-series', dd.max())
wrong('e-mdd-series', 'first', 1 - 96 / 108, typed=0.1111)
wrong('e-mdd-series', 'start', 1 - px.min() / px[0], typed=0.048)
wrong('e-mdd-series', 'trough', (112 - 95.2) / 95.2, typed=0.1765)
ex.claim(int(np.argmax(px)) == IT['e-mdd-series']['explain']['canvas']['markers'][0]['i'] == 4
         and int(np.argmax(dd)) == IT['e-mdd-series']['explain']['canvas']['markers'][1]['i'] == 5,
         'e-mdd-series explain markers sit on the peak (day 5) and the trough (day 6)')
ex.expect('exam', f'{P("e-mdd-series")}.explain.text', round(100 * (1 - 96 / 108), 1))

# ---------------------------------------------------------------- e-position-alias
out, _, _ = run_snippet(code_of('e-position-alias'))
ex.claim(out == strip_ticks(opt('e-position-alias', 'a')) and correct_ids('e-position-alias') == ['a'], f'e-position-alias prints {out}')
ex.claim(f'{200 * 4.50}' == strip_ticks(opt('e-position-alias', 'b')), 'e-position-alias b is the copied object')

# ---------------------------------------------------------------- e-signal-shift
out, _, ns = run_snippet(code_of('e-signal-shift'))
key('e-signal-shift', float(out))
ex.claim(out == '1.0', f'e-signal-shift prints {out} (a learner types 1)')
ma = ns['ma']
ex.claim([round(v, 2) for v in ma.dropna()] == [10.23, 10.5, 10.7], 'e-signal-shift explain: means 10.23, 10.5, 10.7')
raw = (ns['s'] > ma).astype(int)
wrong('e-signal-shift', 'noshift', raw.sum(), typed=2)
wrong('e-signal-shift', 'all', ns['sig'].count(), typed=4)
ex.claim(raw.tolist() == [0, 0, 0, 1, 1], 'e-signal-shift explain: 0, 0, 0, 1, 1 before the shift')

# ---------------------------------------------------------------- e-fat-tails
p3 = math.erfc(3 / math.sqrt(2))
ex.claim(near(p3, 0.0027, 5e-5) and round(2520 * p3) == 7, f'e-fat-tails normal share beyond 3 sd {p3:.5f}, {2520 * p3:.2f} of 2,520 days')

# ---------------------------------------------------------------- e-catch-only
_, err, _ = run_snippet(code_of('e-catch-only'))
ex.claim(err == 'TypeError' and correct_ids('e-catch-only') == ['a'], f'e-catch-only raises {err}')
ex.claim('4.85' * 2 == strip_ticks(opt('e-catch-only', 'd').replace('It prints ', '')), 'e-catch-only d is "4.85" * 2')

# ---------------------------------------------------------------- e-exit-pipeline (run on a newest-first file with gaps)
csv = 'date,close\n2024-03-08,104.0\n2024-03-07,\n2024-03-06,101.0\n2024-03-05,100.0\n2024-03-04,\n2024-03-01,98.0\n'
lines = {l_['id']: l_['text'].strip('`') for l_ in IT['e-exit-pipeline']['widget']['lines']}


def pipeline(order):
    ns_ = {'pd': pd, 'np': np, 'io': io, 'CSV': csv}
    for i in order:
        exec(lines[i].replace('"prices.csv"', 'io.StringIO(CSV)'), ns_)
    return ns_


good = pipeline(IT['e-exit-pipeline']['widget']['answer'])
swap = pipeline(['s1', 's3', 's2', 's4', 's5'])
ex.claim(good['close'].tolist() == [98.0, 98.0, 100.0, 101.0, 101.0, 104.0], 'e-exit-pipeline: sort then fill carries the earlier close')
ex.claim(swap['close'].tolist() != good['close'].tolist() and swap['close'].loc['2024-03-07'] == 104.0,
         'e-exit-pipeline explain: filling before sorting copies a later price into the gap (looks ahead)')
ex.claim(math.isclose(good['vol'], good['r'].std(ddof=1) * math.sqrt(252)), 'e-exit-pipeline explain: std divides by n - 1')

# ---------------------------------------------------------------- e-simple-returns
close = pd.Series([100.0, 102.0, 99.0, 101.0, 104.5])
forms = {
    'a': close.pct_change(), 'b': close / close.shift(1) - 1, 'c': close.diff() / close.shift(1),
    'd': close.shift(-1) / close - 1, 'e': close.diff() / close, 'f': np.log(close).diff(),
}
same_ = {k: bool(np.allclose(v.iloc[1:], forms['a'].iloc[1:], rtol=0, atol=1e-15) and v.isna().iloc[0]) for k, v in forms.items()}
ex.claim(sorted(k for k, v in same_.items() if v) == correct_ids('e-simple-returns') == ['a', 'b', 'c'], f'e-simple-returns forms equal to pct_change: {same_}')

# ---------------------------------------------------------------- e-join-table
a = pd.DataFrame({'date': pd.to_datetime(['2024-07-01', '2024-07-02', '2024-07-03', '2024-07-04']), 'close': [10.0, 10.2, 10.1, 10.4]})
b = pd.DataFrame({'date': pd.to_datetime(['2024-07-02', '2024-07-03', '2024-07-05']), 'close': [20.0, 20.3, 20.6]})
sa, sb = a.set_index('date')['close'], b.set_index('date')['close']
ns3 = {'pd': pd, 'a': a, 'b': b, 'sa': sa, 'sb': sb}
exec(code_of('e-join-table'), ns3)
for row, name in enumerate(['n1', 'n2', 'n3', 'n4']):
    key('e-join-table', float(ns3[name]), path=f'widget.rows[{row}][1]')
nan_days = sorted(d.day for d in (sa / sb)[(sa / sb).isna()].index)
ex.claim(nan_days == [1, 4, 5], f'e-join-table byKey r3c1: NaN on {nan_days} July')

# ---------------------------------------------------------------- e-log-axis
per = 3 / math.log2(80 / 20)
key('e-log-axis', per * math.log2(80 / 10))
wrong('e-log-axis', 'linear', 3 * (80 - 10) / (80 - 20), typed=3.5)
wrong('e-log-axis', 'ratio', 3 * (80 / 10) / (80 / 20), typed=6)
ex.expect('exam', f'{P("e-log-axis")}.explain.text', 1.5)

# ---------------------------------------------------------------- e-rebase-mutate
out, _, _ = run_snippet(code_of('e-rebase-mutate'))
ex.claim(out == strip_ticks(opt('e-rebase-mutate', 'a')) and correct_ids('e-rebase-mutate') == ['a'], f'e-rebase-mutate prints {out}')
# option d's why: "You expected b to keep its own copy from the first call". That belief gives a[1] 1.5 (a changed
# by both calls), b[1] 150.0 (the copy) and c is a True, i.e. "1.5 150.0 True", not the option's "150.0 1.5 False".
belief_d = '1.5 150.0 True'
ex.claim_text('exam', f'{P("e-rebase-mutate")}.widget.options[3].text', '150.0 1.5 False',
              strip_ticks(opt('e-rebase-mutate', 'd')) == belief_d, 'e-rebase-mutate option d matches the belief its why names')
ex.claim(strip_ticks(opt('e-rebase-mutate', 'b')) == '75.0 150.0 False', 'e-rebase-mutate b is the copy-in-the-function belief')

# ---------------------------------------------------------------- e-daily-value: the table and the explain
cvr = IT['e-daily-value']['canvas']['params']['rows']
tr = pd.DataFrame(cvr, columns=['date', 'ticker', 'qty', 'price']).astype({'qty': int, 'price': float})
ex.claim(tr.to_dict('list') == eval(re.search(r'pd\.DataFrame\((\{.*\})\)', IT['e-daily-value']['widget']['tests'][0]['setup']).group(1)),
         'e-daily-value canvas table equals the first test\'s trades')
ex.claim(near(400 * 2.16, 864, 1e-9) and near(1000 * 2.15 + 864, 3014, 1e-9) and near(600 * 2.12, 1272, 1e-9)
         and near((3014 + 1272) / 2, 2143, 1e-9), 'e-daily-value explain: 864, 3,014, 1,272 and 2,143')

# ---------------------------------------------------------------- e-portfolio-dd: the byKey numbers
v = (np.array([[100.0, 200.0], [90.0, 210.0], [80.0, 190.0], [95.0, 230.0], [70.0, 220.0]]) / [100.0, 200.0]) @ [0.6, 0.4]
ex.claim([round(x, 2) for x in v] == [1.0, 0.96, 0.86, 1.03, 0.86], 'e-portfolio-dd byKey test-1: the value falls from 1.03 to 0.86')


# ---------------------------------------------------------------- code items, graded as the engine's harness grades them
def _flat(x):
    return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x


def _close(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:  # noqa: BLE001
        return x == y


def run_case(code, case):
    ns = {}
    try:
        exec(code, ns)
        if case.get('setup'):
            exec(case['setup'], ns)
        got = eval(case['call'], ns)
        want = eval(case['expect'], ns)
    except Exception as e:  # noqa: BLE001
        return False, f'{type(e).__name__}: {e}'
    if case.get('compare') == 'isclose':
        return _close(got, want), got
    try:
        return bool(_flat(got) == _flat(want)), got
    except Exception:  # noqa: BLE001
        return False, got


def first_fail(code, tests):
    for i, c in enumerate(tests):
        if not run_case(code, c)[0]:
            return i + 1
    return None


def code_item(iid, mutants=()):
    w = IT[iid]['widget']
    cases = [('example', c) for c in w['examples']] + [('test', c) for c in w['tests']]
    runs = [run_case(w['solution'], c) for _, c in cases]
    sol = [r_[0] for r_ in runs]
    ex.claim(all(sol), f'{iid} solution passes {sum(sol)} of {len(sol)} examples and tests',
             '; '.join(f'case {i}: {r_[1]!r}'[:160] for i, r_ in enumerate(runs) if not r_[0]))
    st = [run_case(w['starter'], c)[0] for k_, c in cases if k_ == 'test']
    ex.claim(not all(st), f'{iid} starter fails {st.count(False)} of {len(st)} hidden tests', 'starter passes every test')
    n = len(w['tests'])
    ex.claim(f'{n} hidden tests' in w.get('how', ''), f'{iid} how states {n} hidden tests')
    dup = [i + 1 for i, t in enumerate(w['tests']) if any(t['call'] == e['call'] and t.get('setup') == e.get('setup') for e in w['examples'])]
    print(f'   {iid}: hidden tests identical to an example: {dup}; starter passes tests {[i + 1 for i, ok in enumerate(st) if ok]}')
    out_ = {}
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i + 1 for i, c in enumerate(w['tests']) if not run_case(bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')
        out_[name] = fails
        plt.close('all')
    return out_


code_item('e-month-end', [
    ('no sort', 'for day, close in sorted(rows):', 'for day, close in rows:'),
    ('sorts in place', 'for day, close in sorted(rows):', 'rows.sort()\n    for day, close in rows:'),
    ('highest close', 'last[day[:7]] = close', 'last[day[:7]] = max(close, last.get(day[:7], close))'),
])
code_item('e-rebased-chart', [
    ('first share base', 'c / closes[0] * 100', 'c / list(prices.values())[0][0] * 100'),
    ('no label', ', label=name', ''),
    ('no y label', '    ax.set_ylabel("Value (start = 100)")\n', ''),
])
m22 = code_item('e-daily-value', [
    ('no abs', 'trades["qty"].abs()', 'trades["qty"]'),
    ('mean of fills', 'daily = value.groupby([trades["date"], trades["ticker"]]).sum()', 'daily = value.groupby([trades["date"], trades["ticker"]]).mean()'),
    ('sum of days', 'per_ticker = daily.groupby(level="ticker").mean()', 'per_ticker = daily.groupby(level="ticker").sum()'),
])
# byKey test-4 names the no-abs slip, but that slip fails test 1 first, so the learner reads test-1's line, which
# tells them to total each day. The check passes once test-1's line also names abs() (or the tests are reordered).
ex.claim_text('exam', f'{P("e-daily-value")}.feedback.byKey.test-1', 'Total each day before you take the mean.',
              m22['no abs'][0] != 1, 'e-daily-value: the no-abs slip first fails a test whose line names it')
m24 = code_item('e-portfolio-dd', [
    ('no rebase', 'value = (prices / prices[0]) @ weights', 'value = prices @ weights'),
    ('rows by first column', 'prices / prices[0]', 'prices / prices[:, :1]'),
    ('from day 1', 'peak = np.maximum.accumulate(value)', 'peak = value[0]'),
    ('wrong axis, flat', 'prices / prices[0]', 'prices / prices[:, 0]'),
])
# byKey.error explains the broadcasting slip, but the engine keys "error" only when the code fails to load; a shape
# error inside a test call is a failing row, so the key is test-1. Likewise test-5's "a wrong axis does not raise"
# line: the wrong-axis bug fails test 1 first.
w24 = IT['e-portfolio-dd']['widget']
bad = w24['solution'].replace('prices / prices[0]', 'prices / prices[:, 0]')
loads = run_snippet(bad)[1] is None
ex.claim_text('exam', f'{P("e-portfolio-dd")}.feedback.byKey.error', 'lines up by column',
              not loads, 'e-portfolio-dd byKey error: the broadcasting slip it explains stops the code loading')
ex.claim_text('exam', f'{P("e-portfolio-dd")}.feedback.byKey.test-5', 'a wrong axis does not raise an error',
              m24['wrong axis, flat'][0] == 5, 'e-portfolio-dd byKey test-5: the wrong-axis slip first fails test 5')

# ---------------------------------------------------------------- e-exit-review: the buggy script and the model
lf = IT['e-exit-review']
bug_src = re.search(r'```python\n(.*?)```', lf['prompt'], re.S).group(1)
model_src = re.search(r'```python\n(.*?)```', lf['model'], re.S).group(1)
hand = 'date,close\n2024-01-03,90.0\n2024-01-02,120.0\n2024-01-01,100.0\n'   # (c)'s path, newest first
with tempfile.TemporaryDirectory() as tdir:
    with open(os.path.join(tdir, 'prices.csv'), 'w') as f:
        f.write(hand)
    cwd = os.getcwd()
    os.chdir(tdir)
    try:
        nsb = {}
        with contextlib.redirect_stdout(io.StringIO()) as bufb:
            exec(bug_src, nsb)
        bug_saved = os.path.exists('risk.png')
        os.remove('risk.png')
        nsm = {'__name__': 'risk'}
        exec(model_src, nsm)        # imported, not run: nothing printed, no file saved
        saved_on_import = os.path.exists('risk.png')
        with contextlib.redirect_stdout(io.StringIO()) as bufm:
            nsm['main'](['risk.py', 'prices.csv'])
        made = os.path.exists('risk.png')
    finally:
        os.chdir(cwd)
r_true = pd.Series([100.0, 120.0, 90.0]).pct_change().dropna()
ex.claim([round(x, 2) for x in r_true] == [0.2, -0.25], 'e-exit-review (c): returns 0.2 and -0.25')
ex.claim(near(90 / 120 - 1, -0.25, 1e-12), 'e-exit-review (c): drawdown 90/120 - 1 = -0.25')
ex.claim(near(nsb['vol'] / (nsb['r'].std() * math.sqrt(252)), math.sqrt(252), 1e-9) and round(math.sqrt(252), 1) == 15.9,
         'e-exit-review bug 2: times 252 is sqrt(252) = 15.9 times too big')
ex.claim(nsb['close'].index[0] > nsb['close'].index[-1], 'e-exit-review bug 3: the first row is the newest price')
ex.claim(near(nsb['mdd'], min(90 / 90, 120 / 90, 100 / 90) - 1, 1e-12), f'e-exit-review bug 3: buggy MDD {nsb["mdd"]:.4f} misses the -25% fall')
ex.claim(nsb['ax'].get_title() == 'Fund', 'e-exit-review bug 4: the title is set (after the save)')
r_rev = nsb['r'].dropna().tolist()
ex.claim([round(x, 4) for x in r_rev] == [round(120 / 90 - 1, 4), round(100 / 120 - 1, 4)],
         'e-exit-review bug 1: unsorted, pct_change divides each day by the next day')
ex.claim(bug_saved, 'e-exit-review bug 5: the buggy script saves risk.png as soon as it runs')
ex.claim(not saved_on_import and made,'e-exit-review model: importing saves nothing; main() saves risk.png')
mv = re.search(r'Vol ([\d.]+)%  MDD (-?[\d.]+)%', bufm.getvalue())
ex.claim(mv is not None and float(mv.group(2)) == -25.0, f'e-exit-review model prints {bufm.getvalue().strip()!r}')
ex.claim(near(float(mv.group(1)) / 100, r_true.std() * math.sqrt(252), 0.0006), 'e-exit-review model: vol is the sample sd times sqrt(252)')
# The prompt asks for a figure "labelled with units" and rubric line 4 checks "labelled axes with units"; the model's
# drawdown panel is labelled "Drawdown" with no unit and neither panel has an x label.
ex.claim_text('exam', f'{P("e-exit-review")}.model', 'bottom.set_ylabel("Drawdown")', False,
              'e-exit-review model: the drawdown axis carries its unit, as the prompt and rubric ask')
# (c) says sorting "is checked by feeding the same three rows newest first and getting the same answers", right after
# "A test can feed `summary` these three closes". `summary` does not sort, so newest-first closes give other answers.
_, vol_rev, dd_rev = nsm['summary'](pd.Series([90.0, 120.0, 100.0]))
_, vol_fwd, dd_fwd = nsm['summary'](pd.Series([100.0, 120.0, 90.0]))
ex.claim_text('exam', f'{P("e-exit-review")}.model', 'feeding the same three rows newest first and getting the same answers',
              near(dd_rev.min(), dd_fwd.min(), 1e-12), f'e-exit-review model (c): summary of newest-first closes keeps MDD -0.25 (gets {dd_rev.min():.4f})')
plt.close('all')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
