"""Second reader's number script for app/content/exams/topic-1.2.json (review-exam-1.2.md).

Recomputes every graded key and every wrong[] value, the numbers in prose, feedback and explanations, and runs
the behaviour each item claims:
- SQL items: the shown tables are loaded into SQLite and the shown query (and each slip's query) is run.
- Shell items: the shown trades.csv is written to a temporary folder and the pipelines run in /bin/sh.
- pytest items: real pytest runs on the shown tests (the float report, the parametrised count, the longform's layout).
- Code items: each solution passes every example and hidden test, each starter fails at least one, and planted bugs are caught.
- Git items: counts are rebuilt from the shown consoles. The git behaviour itself was checked by hand in throwaway
  repositories with git 2.43.0 (see the review's Tool results); this script runs no git.
- Proposed fixes: every number a fix in the review states is computed here too (labelled "fix").
A check that fails because the content is wrong stays failing; each such check is a finding in the review.

Needs pytest (8.1.1 used, as in Pyodide 0.27.7). Run with a Python that has it, for example:
    <scratchpad>/fix-pytest-1-3/venv/bin/python docs/reviews/exam-1.2-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (statistics and fractions import it).
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import contextlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import sqlite3  # noqa: E402
import statistics  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402

import pytest  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.2.json')
COURSES = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
PYTEST_BIN = os.path.join(os.path.dirname(sys.executable), 'pytest')   # the console command, as the courses run it
print(f'pytest {pytest.__version__}, SQLite {sqlite3.sqlite_version}, Python {sys.version.split()[0]}')


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


def E(iid, path, value, fmt=None):
    return ex.expect('exam', f'{P(iid)}.{path}', value, fmt)


def near(a, b, t):
    return abs(a - b) <= t


def key(iid, value, path='widget', t=None):
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
    return [o for o in IT[iid]['widget']['options'] if o['id'] == oid][0]


def cell(v):
    if v == 'NULL':
        return None
    for f in (int, float):
        try:
            return f(v.replace('−', '-'))
        except ValueError:
            pass
    return v


def db_from(tables):
    """tables: {name: canvas params with columns and rows}. Returns an in-memory SQLite database."""
    db = sqlite3.connect(':memory:')
    for name, p in tables.items():
        db.execute(f'CREATE TABLE {name} ({", ".join(p["columns"])})')
        db.executemany(f'INSERT INTO {name} VALUES ({", ".join("?" * len(p["columns"]))})',
                       [[cell(v) for v in r] for r in p['rows']])
    return db


def sql_of(iid):
    m = re.search(r'```sql\n(.*?)```', IT[iid]['prose'], re.S)
    return m.group(1)


def console_ids(lines, pred):
    """Region ids of the console canvas are l1, l2, ... in line order (1-based)."""
    return [f'l{i + 1}' for i, s in enumerate(lines) if pred(s)]


def sh(cmd, cwd):
    return subprocess.run(['/bin/sh', '-c', cmd], cwd=cwd, capture_output=True, text=True).stdout


def run_pytest(files, args=(), module=False):
    """Write files into a fresh folder and run real pytest there; returns (exit code, output)."""
    d = tempfile.mkdtemp(prefix='exam12-')
    try:
        for rel, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
            with open(os.path.join(d, rel), 'w', encoding='utf8') as f:
                f.write(text)
        cmd = ([sys.executable, '-m', 'pytest'] if module else [PYTEST_BIN]) + ['-q', '-p', 'no:cacheprovider', *args]
        r = subprocess.run(cmd, cwd=d, capture_output=True, text=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        return r.returncode, r.stdout + r.stderr
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['minutes'] == 75 and doc['pass'] == 0.7, f'minutes {doc["minutes"]} and pass {doc["pass"]} as stored (fix 18: sibling paces sum to about 71 minutes; AUTHORING section 5 sets minutes per file)')
ex.claim(len(doc['items']) == 26 and 20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 14, 4: 5, 5: 2}, f'ramp {ramp} of {len(doc["items"])} (19%, 54%, 19%, 8% against 20, 50, 20, 10)')
union = {}
for c in ('git', 'sql', 'pytest'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the git, sql and pytest course.json maps')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
rub = sum(r['points'] for r in IT['e-tools-exit']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')
ex.claim(not any(it.get('pace') for it in doc['items']), 'no item carries a pace (timing finding)')
# Sibling medians over every topic exam item with a pace: d2 60, d3 120, d4 195, d4 code 360, d5 360, longform 600 s.
PACE = {(2, 'o'): 60, (3, 'o'): 120, (4, 'o'): 195, (4, 'c'): 360, (5, 'o'): 360, (5, 'l'): 600}
tot = sum(PACE[(it['difficulty'], 'l' if it.get('kind') == 'longform' else 'c' if it.get('widget', {}).get('kind') == 'code' else 'o')]
          for it in doc['items'])
ex.claim(tot == 4245 and doc['minutes'] * 60 >= tot, f'sibling-median paces sum to {tot} s = {tot / 60:.2f} min, inside the stored {doc["minutes"]} minutes')

# ---------------------------------------------------------------- [0] e-status-commit
L0 = IT['e-status-commit']['canvas']['params']['lines']
staged = L0[L0.index('Changes to be committed:') + 1:L0.index('Changes not staged for commit:') - 1]
ex.claim(console_ids(L0, lambda s: s in staged) == IT['e-status-commit']['widget']['answer'], f'e-status-commit key l4, l5 = the staged lines {staged}')
ex.claim(console_ids(L0, lambda s: 'backtest.py' in s) == ['l8'] and console_ids(L0, lambda s: 'notes.txt' in s) == ['l11'],
         'e-status-commit l8 is backtest.py (unstaged), l11 is notes.txt (untracked)')
ex.claim([w['set'] for w in IT['e-status-commit']['widget']['wrong']] == [['l4', 'l5', 'l8'], ['l4', 'l5', 'l8', 'l11']], 'e-status-commit wrong sets: staged plus unstaged, then all four')
# Real run (git 2.43.0): git status prints these three headings with these files; git commit takes costs.py and signal.py only.

# ---------------------------------------------------------------- [1] e-sql-where
c1 = IT['e-sql-where']['canvas']['params']
db = db_from({'prices': c1})
got = db.execute(sql_of('e-sql-where')).fetchall()
key('e-sql-where', len(got))
wrong('e-sql-where', 'or', db.execute('SELECT ticker, close FROM prices WHERE close > 1 OR volume < 450000').fetchall().__len__())
wrong('e-sql-where', 'tickers', len({r[0] for r in got}))
rows_in = [i for i, r in enumerate(c1['rows']) if float(r[2]) > 1 and int(r[3]) < 450000]
ex.claim(rows_in == IT['e-sql-where']['explain']['canvas']['highlight']['rows'], f'e-sql-where explain highlights rows {rows_in}')

# ---------------------------------------------------------------- [2] e-approx-fix
r2 = 55.00 / 50.00 - 1
ex.claim(repr(r2) == '0.10000000000000009', f'e-approx-fix 55/50 - 1 = {r2!r}')
DR = 'def daily_returns(prices):\n    return [b / a - 1 for a, b in zip(prices, prices[1:])]\n'
code, out = run_pytest({'test_r.py': 'import pytest\n' + DR + '\ndef test_r():\n    r = daily_returns([50.00, 55.00])\n    assert r == [0.1]\n'})
ex.claim(code == 1 and 'E       assert [0.10000000000000009] == [0.1]' in out, 'e-approx-fix real pytest report prints "assert [0.10000000000000009] == [0.1]"')
code, out = run_pytest({'test_r.py': 'import pytest\n' + DR + '\ndef test_r():\n    r = daily_returns([50.00, 55.00])\n    assert r == pytest.approx([0.1])\n'})
ex.claim(code == 0, 'e-approx-fix option a passes on the correct code')
ex.claim(correct_ids('e-approx-fix') == ['a'], 'e-approx-fix key a')
ex.claim(abs(0.9 - 0.1) < 1, 'e-approx-fix option c why: a return of 0.9 passes abs(r - 0.1) < 1')
ex.claim(pytest.approx(0.1).tolerance == 1e-7 and math.isclose(pytest.approx(0.1).tolerance / 0.1, 1e-6),
         'e-approx-fix explain: default relative tolerance one in a million (1e-6 of 0.1 = 1e-7)')
I2 = IT['e-approx-fix']
ex.claim('0.32000000000000006 == 0.32' in I2['prose'] and '0.10000000000000009' not in json.dumps(I2) and 'total_return([0.10, 0.20])' in I2['prose'],
         'e-approx-fix now shows the compounding report (0.32000000000000006 == 0.32), not the daily_returns one')
ex.claim('1.2 would pass' in opt('e-approx-fix', 'c')['why'] and '0.32000000000000006' in I2['explain']['text'], 'e-approx-fix option c why and explain carry the new numbers')
# fix: fresh float slip, compounding 10% and 20% (sum() is compensated from Python 3.12, so a sum of weights would not do)
TR = 'def total_return(returns):\n    g = 1.0\n    for r in returns:\n        g *= 1 + r\n    return g - 1\n'
w2 = 1.1 * 1.2 - 1
ex.claim(repr(w2) == '0.32000000000000006' and w2 == pytest.approx(0.32) and abs(1.2 - 0.32) < 1, f'fix e-approx-fix: 1.1 x 1.2 - 1 = {w2!r}; approx(0.32) accepts it; a return of 1.2 passes abs < 1')
code, out = run_pytest({'test_w.py': TR + '\ndef test_w():\n    r = total_return([0.10, 0.20])\n    assert r == 0.32\n'})
ex.claim(code == 1 and 'E       assert 0.32000000000000006 == 0.32' in out, 'fix e-approx-fix: real pytest prints "assert 0.32000000000000006 == 0.32"')
code, out = run_pytest({'test_w.py': 'import pytest\n' + TR + '\ndef test_w():\n    r = total_return([0.10, 0.20])\n    assert r == pytest.approx(0.32)\n'})
ex.claim(code == 0, 'fix e-approx-fix: pytest.approx(0.32) passes on the correct code')

# ---------------------------------------------------------------- [3] e-shell-sells and [11] e-shell-order
L3 = IT['e-shell-sells']['canvas']['params']['lines']
tmp = tempfile.mkdtemp(prefix='exam12-sh-')
with open(os.path.join(tmp, 'trades.csv'), 'w') as f:
    f.write('\n'.join(L3[1:]) + '\n')
key('e-shell-sells', int(sh('grep SELL trades.csv | wc -l', tmp)))
wrong('e-shell-sells', 'whole', int(sh('wc -l < trades.csv', tmp)))
wrong('e-shell-sells', 'qty', sum(int(s.split(',')[3]) for s in L3[2:] if ',SELL,' in s))
ex.claim(console_ids(L3, lambda s: ',SELL,' in s) == IT['e-shell-sells']['explain']['canvas']['shade']['sell'], 'e-shell-sells explain shades the three SELL lines')
_lines = {l['id']: l for l in IT['e-shell-order']['widget']['lines']}
pipe = ' '.join(_lines[i]['text'].strip('`') for i in IT['e-shell-order']['widget']['answer'])
top = sh(pipe, tmp).split()
ex.claim(len(top) == 2, f'e-shell-order pipeline "{pipe}" prints one line with a count: {top}')
ex.claim(sh('cut -d, -f2 trades.csv | uniq -c | wc -l', tmp).strip() != sh('cut -d, -f2 trades.csv | sort | uniq -c | wc -l', tmp).strip(),
         'e-shell-order: uniq -c merges only neighbours (unsorted input gives more lines)')
ex.claim(IT['e-shell-order']['widget']['distractors'] == ['d1', 'd2'] and _lines['d1']['text'] == '`| sort -n`' and _lines['d2']['text'] == '`| wc -l`',
         'e-shell-order: the two distractors are sort -n and wc -l (both whys checked below)')
ex.claim(sh(pipe.replace('sort -rn', 'sort -n'), tmp).split() == ['1', 'SHEL'] and sh(pipe.replace('| head -n 1', '| wc -l'), tmp).strip() == '2',
         'e-shell-order d1 why: sort -n keeps the least sold (1 SHEL); d2 why: wc -l counts 2 sold tickers, not which')
# fix: the most-sold ticker, with grep first; distractors sort -n and wc -l
fixpipe = 'grep SELL trades.csv | cut -d, -f2 | sort | uniq -c | sort -rn | head -n 1'
ex.claim(sh(fixpipe, tmp).split() == ['2', 'VOD'], f'fix e-shell-order: "{fixpipe}" prints "2 VOD"')
ex.claim(sh('grep SELL trades.csv | cut -d, -f2 | sort | uniq -c | sort -n | head -n 1', tmp).split() == ['1', 'SHEL'],
         'fix e-shell-order: with sort -n the top line is "1 SHEL" (the least sold)')
shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- [4] e-sql-null
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE prices (date, ticker, close)')
db.executemany('INSERT INTO prices VALUES (?, ?, ?)', [('d1', 'BARC', 2.15), ('d2', 'BARC', None), ('d3', 'BARC', 2.12), ('d4', 'BARC', 0.0 + 2.18), ('d5', 'BARC', None)])
res = {o['id']: len(db.execute('SELECT * FROM prices ' + o['text'].strip('`')).fetchall()) for o in IT['e-sql-null']['widget']['options']}
ex.claim(res == {'a': 2, 'b': 0, 'c': 0, 'd': 0}, f'e-sql-null rows per option {res}: only IS NULL finds the two gaps')

# ---------------------------------------------------------------- [5] e-conflict-order
ex.claim(IT['e-conflict-order']['widget']['answer'] == ['m1', 'm2', 'm3', 'm4', 'm5'], 'e-conflict-order key: merge, edit, add, commit, log')
# Real run: commit before add is refused ("Committing is not possible because you have unmerged files"); add then commit makes
# the merge commit. Fix distractors: `git merge --abort` restores main's pre-merge file; `git commit -a` commits the markers.

# ---------------------------------------------------------------- [6] e-sql-having
c6 = IT['e-sql-having']['canvas']['params']
db = db_from({'fills': c6})
tot6 = dict(db.execute('SELECT ticker, SUM(qty) FROM fills GROUP BY ticker').fetchall())
ex.claim(tot6 == {'AZN': 50, 'BARC': 500, 'SHEL': 450, 'VOD': 900}, f'e-sql-having totals {tot6}')
key('e-sql-having', len(db.execute(sql_of('e-sql-having')).fetchall()))
wrong('e-sql-having', 'single', len(db.execute('SELECT ticker, SUM(qty) FROM fills WHERE qty > 400 GROUP BY ticker').fetchall()))
wrong('e-sql-having', 'groups', len(tot6))
for v in (500, 450, 900, 50):
    E('e-sql-having', 'feedback.correct', v)
for v in (400, 300, 200, 500, 1500, 600, 900, 450, 50):
    E('e-sql-having', 'explain.text', v)

# ---------------------------------------------------------------- [7] e-catch-bug
def mdd_pos(p):
    peak, worst = p[0], 0.0
    for c in p:
        peak = max(peak, c)
        worst = max(worst, 1 - c / peak)
    return worst


def mdd_neg(p):
    return -mdd_pos(p) if mdd_pos(p) else 0.0


def bug7b(p):
    # the planted bug: the worst one-day return, or 0.0 when no day falls
    return min([0.0] + [b / a - 1 for a, b in zip(p, p[1:])])


def pounds(t):
    return [float(x) for x in re.findall(r'£([\d.]+)', t)]


catch = {o['id']: not math.isclose(-mdd_pos(pounds(o['text'])), bug7b(pounds(o['text'])), abs_tol=1e-12) for o in IT['e-catch-bug']['widget']['options']}
ex.claim(sorted(k for k, v in catch.items() if v) == correct_ids('e-catch-bug') == ['a', 'd'], f'e-catch-bug key {correct_ids("e-catch-bug")}: the paths where the two versions differ (worst one-day return bug)')
ex.claim('negative fractions' in IT['e-catch-bug']['prose'] and 'positive fraction' not in IT['e-catch-bug']['prose'], 'e-catch-bug prose uses the negative convention of items 10 and 24')


FIX7 = {'a': [100, 90, 81], 'b': [100, 80, 120], 'c': [120, 100, 120], 'd': [100, 90, 99, 81], 'e': [100, 100, 100]}
ex.claim({o['id']: pounds(o['text']) for o in IT['e-catch-bug']['widget']['options']} == {k: [float(x) for x in v] for k, v in FIX7.items()}, 'e-catch-bug options hold the five paths a to e')
fx = {k: (round(mdd_neg(p), 4), round(bug7b(p), 4)) for k, p in FIX7.items()}
ex.claim(fx == {'a': (-0.19, -0.1), 'b': (-0.2, -0.2), 'c': (-0.1667, -0.1667), 'd': (-0.19, -0.1818), 'e': (0.0, 0.0)},
         f'fix e-catch-bug (right, worst one-day return) per option {fx}: a and d catch, b, c, e do not')
E('e-catch-bug', 'explain.text', -0.19)
E('e-catch-bug', 'explain.text', -0.1)
E('e-catch-bug', 'explain.text', round(81 / 99 - 1, 2))
ex.claim(round(81 / 99 - 1, 4) == -0.1818 and round(-mdd_pos([100, 90, 81]), 2) == -0.19, 'e-catch-bug explain: 81/99 - 1 = -0.1818 (shown -0.18), right answer -0.19 (1 - 81/100)')

# ---------------------------------------------------------------- [8] e-push-rejected
L8 = IT['e-push-rejected']['canvas']['params']['lines']
ex.claim('[rejected]' in L8[2] and L8[3].startswith('error') and "risk.git'" in L8[4]
         and sorted(IT['e-push-rejected']['explain']['canvas']['tone']) == ['l3', 'l4', 'l5'],
         'e-push-rejected explain tones the rejected and error lines l3 to l5')
ex.claim(correct_ids('e-push-rejected') == ['a'], 'e-push-rejected key a (pull, then push)')
# Real run, git 2.43.0 with no pull setting: the pull stops with "fatal: Need to specify how to reconcile divergent branches."
_it8 = IT['e-push-rejected']
ex.claim('Your Git is set to merge when it pulls.' in _it8['prose'],
         'e-push-rejected prose states the pull setting (git 2.43: a plain pull on divergent branches stops; with pull.rebase false it merges and the push then succeeds)')

# ---------------------------------------------------------------- [9] e-inner-join
cv = IT['e-inner-join']['canvas']
db = db_from({'securities': cv['left']['params'], 'trades': cv['right']['params']})
key('e-inner-join', db.execute(sql_of('e-inner-join')).fetchone()[0])
wrong('e-inner-join', 'all', sum(cell(r[-1]) for r in cv['right']['params']['rows']))
wrong('e-inner-join', 'pairs', db.execute('SELECT SUM(t.qty) FROM trades AS t, securities AS s').fetchone()[0])
unm = [i for i, r in enumerate(cv['right']['params']['rows']) if r[1] not in {s[0] for s in cv['left']['params']['rows']}]
ex.claim(unm == IT['e-inner-join']['explain']['canvas']['right']['highlight']['rows'], f'e-inner-join explain highlights the unmatched trades {unm}')
# fix: ask for SUM(t.qty) over the join instead of the row count
s_join = db.execute('SELECT SUM(t.qty) FROM trades AS t JOIN securities AS s ON t.ticker = s.ticker').fetchone()[0]
s_all = db.execute('SELECT SUM(qty) FROM trades').fetchone()[0]
s_cross = db.execute('SELECT SUM(t.qty) FROM trades AS t, securities AS s').fetchone()[0]
ex.claim((s_join, s_all, s_cross) == (600, 800, 4000), f'fix e-inner-join: joined total {s_join}, every trade {s_all}, cross join {s_cross}')
E('e-inner-join', 'explain.text', 600)
ex.claim(400 + 200 - 150 + 50 + 100 == 600 and 300 - 100 == 200 and 'BARC 250, SHEL 300 and AZN 50' in IT['e-inner-join']['feedback']['correct'] and 250 + 300 + 50 == 600,
         'e-inner-join feedback and explain sums: 250 + 300 + 50 = 600 = 400 + 200 - 150 + 50 + 100; the two RR trades are 300 and -100')

# ---------------------------------------------------------------- [10] e-param-table
paths10 = [[100, 125, 100], [80, 60, 90, 72], [50], [200, 150, 180, 120]]
want10 = [-mdd_pos(p) if mdd_pos(p) else 0.0 for p in paths10]
for i, v in enumerate(want10):
    key('e-param-table', v, path=f'widget.rows[{i}][1]')
key('e-param-table', len(paths10), path='widget.rows[4][1]')
MDN = ('def max_drawdown(prices):\n    peak, worst = prices[0], 0.0\n    for p in prices:\n        peak = max(peak, p)\n'
       '        worst = min(worst, p / peak - 1)\n    return worst\n')
src10 = re.search(r'```python\n(.*?)```', IT['e-param-table']['prose'], re.S).group(1)
for k, v in zip('ABCD', want10):
    src10 = src10.replace(f'], {k})', f'], {v!r})')
code, out = run_pytest({'test_p.py': 'import pytest\n' + MDN + '\n' + src10})
ex.claim(code == 0 and '4 passed' in out, 'e-param-table real pytest: the filled table gives "4 passed"')
E('e-param-table', 'feedback.byKey.r1c1', -0.25)
E('e-param-table', 'feedback.byKey.r1c1', round(72 / 90 - 1, 2))

# fix (coverage, new item e-fixture-calls): a fixture asked for by a plain test and a parametrised test
FIXSRC = ('import pytest\nCALLS = []\n\n@pytest.fixture\ndef closes():\n    CALLS.append(1)\n    return [100.00, 104.00, 101.00]\n\n'
          'def test_first(closes):\n    assert closes[0] == 100.00\n\n'
          '@pytest.mark.parametrize("n", [1, 2, 3])\ndef test_head(closes, n):\n    assert len(closes[:n]) == n\n\n'
          'def test_empty():\n    assert [] == []\n\n'
          'def test_zz_count():\n    assert len(CALLS) == 4, len(CALLS)\n')
code, out = run_pytest({'test_fx.py': FIXSRC})
ex.claim(code == 0 and '6 passed' in out, 'fix e-fixture-calls: real pytest calls closes() 4 times (1 plain test + 3 parametrised rows; test_empty asks for none)')

# ---------------------------------------------------------------- [12] e-sql-null-count
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE prices (date, ticker, close)')
db.executemany('INSERT INTO prices VALUES (?, ?, ?)', [(f'd{i}', 'BARC', c) for i, c in enumerate([2.15, None, 2.12, 2.18, None])])
v12 = db.execute(sql_of('e-sql-null-count')).fetchone()[0]
key('e-sql-null-count', v12)
wrong('e-sql-null-count', 'avg', db.execute("SELECT AVG(close) FROM prices WHERE ticker = 'BARC'").fetchone()[0])
ex.claim(db.execute("SELECT SUM(close) FROM prices").fetchone()[0] is not None, 'e-sql-null-count: SUM skips the NULLs (the "null" slip 0 is a guess, not a result)')
E('e-sql-null-count', 'explain.text', 6.45)
E('e-sql-null-count', 'explain.text', 1.29)
E('e-sql-null-count', 'explain.text', 2.15)

# ---------------------------------------------------------------- [13] e-tdd-order
ex.claim(IT['e-tdd-order']['widget']['answer'] == ['t1', 't2', 't3', 't4', 't5'], 'e-tdd-order key: red, green, refactor order')


def _raises(f):
    try:
        f()
    except statistics.StatisticsError:
        return True
    return False


ex.claim(_raises(lambda: statistics.stdev([0.01])), 'e-tdd-order: statistics.stdev of one return raises StatisticsError (a length check is the fix)')

# ---------------------------------------------------------------- [14] e-log-graph
L14 = IT['e-log-graph']['canvas']['params']['lines'][1:]
commits = [s for s in L14 if '*' in s]
first = [s for s in L14 if s.startswith('*')]
below = L14[L14.index('|/') + 1:]
lane = [s for s in L14 if s.startswith('| *')]
key('e-log-graph', len(lane) + len(below))
wrong('e-log-graph', 'lane', len(lane))
wrong('e-log-graph', 'main', len(commits))
E('e-log-graph', 'explain.text', 4)
ex.claim(console_ids(IT['e-log-graph']['canvas']['params']['lines'], lambda s: s.startswith('| *')) == IT['e-log-graph']['explain']['canvas']['shade']['carry'],
         'e-log-graph explain shades the two carry commits l4, l5')
# fix: how many commits the branch carry contains = its two lane commits and the two below the split
ex.claim(2 + len(below) == 4, 'fix e-log-graph: carry contains 4 commits (git rev-list --count carry gave 4 on the rebuilt repository)')

# ---------------------------------------------------------------- [15] e-fetchall-shape
db = sqlite3.connect(':memory:')
db.execute('CREATE TABLE trades (id, ticker, qty)')
db.executemany('INSERT INTO trades VALUES (?, ?, ?)', [(1, 'BARC', 400), (2, 'SHEL', 200), (3, 'BARC', -150), (4, 'AZN', 50), (5, 'BARC', 10)])
# fix: fetchone on a many-row query
db2 = sqlite3.connect(':memory:')
db2.execute('CREATE TABLE trades (id, ticker, qty)')
db2.executemany('INSERT INTO trades VALUES (?, ?, ?)', [(1, 'BARC', 400), (2, 'SHEL', 200), (3, 'BARC', -150), (4, 'AZN', 50)])
cur = db2.execute('SELECT ticker, qty FROM trades ORDER BY qty DESC')
ex.claim(repr(cur.fetchone()) == "('BARC', 400)" == opt('e-fetchall-shape', 'a')['text'].strip('`') and correct_ids('e-fetchall-shape') == ['a'], "fix e-fetchall-shape: fetchone() of ORDER BY qty DESC prints ('BARC', 400), option a, the key")
ex.claim(repr(db2.execute('SELECT ticker, qty FROM trades ORDER BY qty DESC').fetchall()) == opt('e-fetchall-shape', 'd')['text'].strip('`'), 'e-fetchall-shape option d is the whole fetchall() list')
ex.claim(repr(db2.execute('SELECT ticker, qty FROM trades ORDER BY qty DESC').fetchall()[:1]) == "[('BARC', 400)]", "fix e-fetchall-shape: fetchall()[:1] would be [('BARC', 400)]")

# ---------------------------------------------------------------- [16] e-network-test (option lengths for the key-length fix)
FIX16 = ['Pass a short hand-made list of closes, with its answer worked out',
         'Retry the download up to three times before the assert runs',
         'Loosen the assert to `vol < 5.0` so a wild month still passes',
         'Skip the test whenever it runs on GitHub after a push']
ex.claim([o['text'] for o in IT['e-network-test']['widget']['options']] == FIX16, 'e-network-test options are the four texts below')
ln = [len(s) for s in FIX16]
ex.claim(ln[0] <= 1.5 * max(ln[1:]) and ln[0] < max(ln[1:]) + 10, f'fix e-network-test option lengths {ln}: no key-length cue')

# ---------------------------------------------------------------- [18] e-reset-hard
L18 = IT['e-reset-hard']['canvas']['params']['lines'][1:]
n18 = len(L18)
ex.claim(L18[2].startswith('e52b8a9'), 'e-reset-hard HEAD~2 is e52b8a9, two back from the top')
key('e-reset-hard', n18 - 2 + 1)
wrong('e-reset-hard', 'kept', n18 + 1)
wrong('e-reset-hard', 'no-new', n18 - 2)
wrong('e-reset-hard', 'two', 2)
E('e-reset-hard', 'explain.text', 4)
ex.claim(console_ids(IT['e-reset-hard']['canvas']['params']['lines'], lambda s: 'lookback' in s) == sorted(IT['e-reset-hard']['explain']['canvas']['tone']),
         'e-reset-hard explain mutes the two lookback lines')
# "You read HEAD~2 as keeping two commits": with the new commit that reading gives 3, which grades as no-new.
ex.claim('You kept only two commits and left out the new one' in IT['e-reset-hard']['feedback']['byKey']['two'] and 'leaves three' in IT['e-reset-hard']['feedback']['byKey']['two']
         and n18 - 2 == 3 and n18 - 2 + 1 == 4,
         'e-reset-hard byKey "two" names both slips (keep two, drop the new commit); HEAD~2 leaves 3 and the new commit makes 4')
# Real run, git 2.43.0: five commits, reset --hard HEAD~2, edit, add, commit: git log --oneline lists 4.

# ---------------------------------------------------------------- [19] e-daily-volume (code)


def same(got, want, mode, tol):
    if mode == 'isclose':
        return math.isclose(got, want, abs_tol=(tol or {}).get('abs', 1e-9))
    return got == want


def run_case(prelude, code, case, ns=None):
    ns = {} if ns is None else ns
    try:
        exec(prelude, ns)
        exec(code, ns)
        if case.get('setup'):
            exec(case['setup'], ns)
        got = eval(case['call'], ns)
    except Exception as e:  # noqa: BLE001
        return False, f'{type(e).__name__}: {e}'
    want = case['expect']
    if isinstance(want, str):
        want = eval(want, {})
    return same(got, want, case.get('compare', 'equal'), case.get('tol')), got


def code_item(iid, mutants=(), runner=run_case):
    w = IT[iid]['widget']
    cases = [('example', c) for c in w['examples']] + [('test', c) for c in w['tests']]
    runs = [runner(w.get('prelude', ''), w['solution'], c) for _, c in cases]
    sol = [r[0] for r in runs]
    ex.claim(all(sol), f'{iid} solution passes {sum(sol)} of {len(sol)} examples and tests',
             '; '.join(f'case {i}: {r[1]!r}'[:160] for i, r in enumerate(runs) if not r[0]))
    st = [runner(w.get('prelude', ''), w['starter'], c)[0] for k, c in cases if k == 'test']
    ex.claim(not all(st), f'{iid} starter fails {st.count(False)} of {len(st)} hidden tests (passes {[i + 1 for i, s in enumerate(st) if s]})')
    dup = [i + 1 for i, t in enumerate(w['tests']) if any(t['call'] == e['call'] and t.get('setup') == e.get('setup') for e in w['examples'])]
    print(f'   {iid}: hidden tests identical to an example: {dup}')
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i + 1 for i, (k, c) in enumerate([x for x in cases if x[0] == 'test']) if not runner(w.get('prelude', ''), bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')
    return st, dup


st19, dup19 = code_item('e-daily-volume', [
    ('no tie-break', 'ORDER BY shares DESC, ticker', 'ORDER BY shares DESC'),
    ('day pasted into the SQL', '"WHERE date = ? GROUP BY ticker "', '"WHERE date = \'" + day + "\' GROUP BY ticker "'),
    ('no GROUP BY', 'GROUP BY ticker ', ''),
    ('ascending', 'ORDER BY shares DESC, ticker', 'ORDER BY shares, ticker'),
])
# The no-tie-break planted bug is caught only if SQLite happens to return VOD before SHEL; the check above records which tests catch it.
w19 = IT['e-daily-volume']['widget']
ex.claim(len(w19['tests']) == 5 and '5 hidden tests' in w19['how'] and 'OR' in w19['tests'][3]['call'], 'e-daily-volume how: 5 hidden tests, test 4 hides SQL')
ex.claim(dup19 == [], f'e-daily-volume no hidden test repeats an example (tests {dup19} do)')
NEW19 = {'call': "daily_volume(db, '2026-03-04')[-1]", 'expect': "('AZN', 50)", 'compare': 'equal'}
ex.claim(w19['tests'][0] == NEW19 and IT['e-daily-volume']['feedback']['byKey']['test-1'].startswith("Test 1 expects `('AZN', 50)` last on 4 March"),
         'e-daily-volume tests[0] and byKey.test-1 are the new AZN check')
ex.claim(run_case('', w19['solution'], NEW19)[0] and not run_case('', w19['starter'], NEW19)[0],
         "fix e-daily-volume tests[0]: daily_volume(db, '2026-03-04')[-1] is ('AZN', 50) on the solution; the starter fails it")

# ---------------------------------------------------------------- [20] e-vol-by-hand
r20 = [0.01, -0.01, 0.01, -0.01]
v20 = statistics.stdev(r20) * math.sqrt(252)
key('e-vol-by-hand', v20, t=5e-5)
inband('e-vol-by-hand', round(v20, 4), label=f'typed {round(v20, 4)}')
wrong('e-vol-by-hand', 'pstdev', statistics.pstdev(r20) * math.sqrt(252), typed=round(statistics.pstdev(r20) * math.sqrt(252), 4))
wrong('e-vol-by-hand', 'times252', statistics.stdev(r20) * 252, typed=round(statistics.stdev(r20) * 252, 4))
wrong('e-vol-by-hand', 'daily', statistics.stdev(r20), typed=round(statistics.stdev(r20), 4))
E('e-vol-by-hand', 'explain.text', 0.0004)
E('e-vol-by-hand', 'explain.text', round(statistics.stdev(r20), 6))
E('e-vol-by-hand', 'explain.text', round(math.sqrt(252), 2))
E('e-vol-by-hand', 'explain.text', round(v20, 4))
ex.claim(f'{0.0004 / 3:.7f}' == '0.0001333', 'e-vol-by-hand explain 0.0004 / 3 = 0.0001333')

# ---------------------------------------------------------------- [21] e-anti-join
cv = IT['e-anti-join']['canvas']
# fix: dated trades, "no trade on 3 March"
db3 = sqlite3.connect(':memory:')
db3.execute('CREATE TABLE securities (ticker, name, sector)')
db3.executemany('INSERT INTO securities VALUES (?, ?, ?)', [[cell(v) for v in r] for r in cv['left']['params']['rows']])
db3.execute('CREATE TABLE trades (id, date, ticker, qty)')
T21 = [(1, '2026-03-02', 'BARC', 400), (2, '2026-03-02', 'SHEL', 200), (3, '2026-03-03', 'BARC', -150), (4, '2026-03-03', 'RR', 300),
       (5, '2026-03-03', 'AZN', 50), (6, '2026-03-04', 'SHEL', 100), (7, '2026-03-04', 'RR', -100)]
db3.executemany('INSERT INTO trades VALUES (?, ?, ?, ?)', T21)
F21 = {'a': "LEFT JOIN trades AS t ON s.ticker = t.ticker AND t.date = '2026-03-03' WHERE t.id IS NULL",
       'b': "LEFT JOIN trades AS t ON s.ticker = t.ticker AND t.date <> '2026-03-03' WHERE t.id IS NULL",
       'c': "LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE t.id IS NULL",
       'd': "JOIN trades AS t ON s.ticker = t.ticker AND t.date = '2026-03-03' WHERE t.id IS NULL"}
fr21 = {k: [r[0] for r in db3.execute('SELECT s.ticker FROM securities AS s ' + q + ' ORDER BY s.ticker').fetchall()] for k, q in F21.items()}
ex.claim(fr21 == {'a': ['HSBA', 'SHEL', 'VOD'], 'b': ['AZN', 'HSBA', 'VOD'], 'c': ['HSBA', 'VOD'], 'd': []}, f'fix e-anti-join per option {fr21}')
ex.claim([[cell(v) for v in r] for r in cv['right']['params']['rows']] == [list(r) for r in T21], 'e-anti-join right table holds the seven dated trades')
ex.claim({o['id']: o['text'].strip('`') for o in IT['e-anti-join']['widget']['options']} == F21 and correct_ids('e-anti-join') == ['a'],
         'e-anti-join options a to d are the four queries above; a is the key')
ex.claim([i for i, r in enumerate(cv['left']['params']['rows']) if r[0] in fr21['a']] == IT['e-anti-join']['explain']['canvas']['left']['highlight']['rows'] == [2, 3, 4],
         'e-anti-join explain highlights HSBA, SHEL and VOD')
ex.claim('HSBA, SHEL and VOD' in IT['e-anti-join']['feedback']['correct'] and 'HSBA, SHEL and VOD' in IT['e-anti-join']['explain']['text']
         and 'SHEL traded on 2 and 4 March' in IT['e-anti-join']['explain']['text'] and 'such as AZN' in opt('e-anti-join', 'b')['why'] and 'SHEL is missed' in opt('e-anti-join', 'c')['why'],
         'e-anti-join feedback, explain and whys name HSBA, SHEL, VOD; AZN (b); SHEL missed (c)')
_s = {r[0]: [t_[1] for t_ in T21 if t_[2] == r[0]] for r in cv['left']['params']['rows']}
ex.claim(_s['SHEL'] == ['2026-03-02', '2026-03-04'] and _s['AZN'] == ['2026-03-03'], 'e-anti-join: SHEL traded on 2 and 4 March only; AZN on 3 March only')

# ---------------------------------------------------------------- [22] e-pytest-file (code, real pytest through the postlude)


def run_pytest_case(prelude, code, case):
    w = IT['e-pytest-file']['widget']
    d = tempfile.mkdtemp(prefix='exam12-pt-')
    old = os.getcwd()
    os.chdir(d)
    try:
        ns = {'__learner_source__': code, '__name__': 'learner'}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, ns)
            exec(w['postlude'], ns)
            if case.get('setup'):
                exec(case['setup'], ns)
            got = eval(case['call'], ns)
    except Exception as e:  # noqa: BLE001
        return False, f'{type(e).__name__}: {e}'
    finally:
        os.chdir(old)
        shutil.rmtree(d, ignore_errors=True)
    want = case['expect']
    if isinstance(want, str):
        want = eval(want, {})
    return got == want, got


st22, dup22 = code_item('e-pytest-file', [], runner=run_pytest_case)
sol22 = IT['e-pytest-file']['widget']['solution']
learner_bugs = [
    ('no single-price row', '    ([80.00], []),\n', '', 6),
    ('raise test on a negative price', 'daily_returns([100.00, 0.00, 105.00])', 'daily_returns([100.00, -5.00, 105.00])', 7),
    ('exact == instead of approx', '== pytest.approx(expected)', '== expected', 1),
]
for name, old, new, want_fail in learner_bugs:
    assert old in sol22, name
    bad = sol22.replace(old, new)
    fails = [i + 1 for i, c in enumerate(IT['e-pytest-file']['widget']['tests']) if not run_pytest_case('', bad, c)[0]]
    ex.claim(want_fail in fails, f'e-pytest-file weak learner file "{name}" fails hidden test {want_fail} (fails {fails})')
w22 = IT['e-pytest-file']['widget']
ex.claim(len(w22['tests']) == 7 and '7 hidden tests' in w22['how'], 'e-pytest-file how: 7 hidden tests')

# ---------------------------------------------------------------- [23] e-sector-table
cv = IT['e-sector-table']['canvas']
db = db_from({'securities': cv['left']['params'], 'trades': cv['right']['params']})
got23 = db.execute(sql_of('e-sector-table')).fetchall()
for i, (sec, n, net) in enumerate(got23):
    ex.claim(IT['e-sector-table']['widget']['rows'][i][0] == sec, f'e-sector-table row {i} is {sec}')
    key('e-sector-table', n, path=f'widget.rows[{i}][1]')
    key('e-sector-table', net, path=f'widget.rows[{i}][2]')
banks = db.execute("SELECT COUNT(*) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE s.sector = 'Banks'").fetchone()[0]
ex.claim(banks == 3, 'e-sector-table byKey r0c1: Banks has 3 rows after the join')
ex.claim(db.execute("SELECT SUM(t.qty) FROM securities AS s LEFT JOIN trades AS t ON s.ticker = t.ticker WHERE s.sector = 'Telecoms'").fetchone()[0] is None,
         'e-sector-table byKey r3c2: SUM over only NULLs is NULL')
for v in (250, 300, 50):
    E('e-sector-table', 'feedback.correct', v)

# ---------------------------------------------------------------- [24] e-tools-exit (longform)
model = IT['e-tools-exit']['model']
blocks = re.findall(r'```(\w+)\n(.*?)```', model, re.S)
py = [b for lang, b in blocks if lang == 'python']
risk_src, test_src = py[0], py[1]
code, out = run_pytest({'risk.py': risk_src, 'tests/test_risk.py': test_src})
ex.claim(code != 0 and 'ModuleNotFoundError' in out and 'pythonpath = ["."]' in model and '[tool.pytest.ini_options]' in model,
         f'e-tools-exit model layout: without pyproject.toml plain `pytest` fails (exit {code}, ModuleNotFoundError), and the model now supplies it')
code_m, _ = run_pytest({'risk.py': risk_src, 'tests/test_risk.py': test_src}, module=True)
ex.claim(code_m == 0, 'e-tools-exit model layout passes under `python -m pytest`, which adds the folder to the path')
code_f, _ = run_pytest({'risk.py': risk_src, 'tests/test_risk.py': test_src, 'pyproject.toml': '[tool.pytest.ini_options]\npythonpath = ["."]\n'})
ex.claim(code_f == 0, 'fix e-tools-exit: with pyproject.toml `pythonpath = ["."]`, plain pytest passes (1 test)')
ns24 = {}
exec(risk_src.replace('main(sys.argv)', 'pass'), ns24)
ex.claim(math.isclose(ns24['max_drawdown']([100.00, 125.00, 100.00]), -0.2), 'e-tools-exit model max_drawdown gives -0.2 for £100, £125, £100')
ex.claim('git init -b main\ngit add' in model and 'git add tests/test_risk.py risk.py pyproject.toml' in model and 'pyproject.toml' in model.split('(c)')[0],
         'e-tools-exit model: `git init -b main` (git 2.43.0: plain init names the branch master and the push of main fails), pyproject.toml committed')
E('e-tools-exit', 'rubric[2].text', -0.2)

# ---------------------------------------------------------------- new item e-fixture-calls, distractor items, leaked key, counts
fx_it = IT['e-fixture-calls']
ex.claim(idx['e-fixture-calls'] == idx['e-param-table'] + 1 and fx_it['difficulty'] == 3 and fx_it['skills'] == ['pt-tools'], 'e-fixture-calls is a d3 pt-tools item straight after e-param-table')
key('e-fixture-calls', 4)
_src = re.search(r'```python\n(.*?)```', fx_it['prose'], re.S).group(1)
_n_tests = _src.count('def test_') + 2   # three parametrised rows share one function
ex.claim(_n_tests == 5 and 'closes' in _src.split('def test_no_prices')[0] and 'closes' not in _src.split('def test_no_prices')[1], 'e-fixture-calls: five tests, four name closes, test_no_prices does not')
for wid, v in (('per-function', 2), ('once', 1), ('every-test', 5)):
    wrong('e-fixture-calls', wid, v)
code, out = run_pytest({'test_fx2.py': 'import pytest\nCALLS = []\n\ndef daily_returns(p):\n    return []\n\n'
                        + _src.replace('from risk import daily_returns\n', '').replace('def closes():\n', 'def closes():\n    CALLS.append(1)\n')
                        + '\ndef test_zz_count():\n    assert len(CALLS) == 4, len(CALLS)\n'})
ex.claim(code == 0 and '6 passed' in out, 'e-fixture-calls: the shown file under real pytest 8.1.1 builds the fixture 4 times (5 tests plus the counter)')
E('e-fixture-calls', 'explain.text', 4)

ex.claim(IT['e-conflict-order']['widget']['distractors'] == ['d1', 'd2'] and IT['e-conflict-order']['widget']['answer'] == ['m1', 'm2', 'm3', 'm4', 'm5'],
         'e-conflict-order: answer unchanged, distractors d1 (commit -a) and d2 (merge --abort), both whys run by hand on git 2.43.0')
ex.claim(IT['e-tdd-order']['widget']['distractors'] == ['d1', 'd2'] and IT['e-tdd-order']['widget']['answer'] == ['t1', 't2', 't3', 't4', 't5'],
         'e-tdd-order: answer unchanged, distractors d1 and d2')
ex.claim(correct_ids('e-leaked-key') == ['a', 'b'], 'e-leaked-key key a and b (revoke; new key in an ignored .env)')
ex.claim('config.py' in IT['e-leaked-key']['prose'] and 'download.py' not in IT['e-leaked-key']['prose'], 'e-leaked-key: new setup (a closed pull request and a deleted branch, config.py)')
ex.claim(IT['e-pytest-file']['explain']['text'].split('```')[0].count('. ') + 1 <= 3, 'e-pytest-file explain prose is three sentences')
E('e-sql-having', 'explain.text', 3)

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
