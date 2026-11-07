"""Second reader's number script for app/content/exams/topic-0.4.json (review-exam-0.4.md).

Recomputes every graded key and every wrong[] value, and the numbers in feedback and explanations, by a second route:
the shell items are replayed on the files their prose shows (Python filters for grep, fnmatch for the glob, a PATH
walk), the Python prediction items are executed and their printed text compared with each option, the path items are
resolved with posixpath, and the wrong-folder item is run for real in a throwaway folder. The three code items run
in an in-process harness that follows code.js (call cases compared with == or math.isclose(rel 1e-9, abs 1e-12),
script cases fed their stdin and compared whitespace-normalised, `printed` defined for a call after a script run).
Each solution must pass every example and hidden test and each starter must fail one; planted slips check that the
byKey test line each slip is meant to reach is the first test it fails (code.js keys on the first failing test, and
keys `error` only when the code fails to load).
The two quoted tracebacks are compared with what python3.12 (Pyodide 0.27.7 is 3.12.7) and python3.13 really print.
Continuity claims check that each construct an item needs appears in the terminal or first-python courses.
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Pure standard library. Run with both interpreters: python3.12 docs/reviews/exam-0.4-scripts/numbers.py and python3.13 ...
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers`. Drop its own folder from the path.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import contextlib  # noqa: E402
import fnmatch  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import posixpath  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

ROOT = os.path.join(HERE, '..', '..', '..', 'app', 'content')
EXAM = os.path.join(ROOT, 'exams', 'topic-0.4.json')
COURSES = os.path.join(ROOT, 'courses')


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
PY = sys.version.split()[0]


def P(iid):
    return f'items[{idx[iid]}]'


def W(iid):
    return IT[iid]['widget']


def key(iid, value):
    a = W(iid)['answer']
    ok = a == value
    ex._rec(ok, f'{iid} answer {a!r} = {value!r}', '' if ok else 'recomputed value differs')


def wrong(iid, wid, value):
    ws = [x for x in W(iid).get('wrong', []) if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    ok = ws[0]['value'] == value
    ex._rec(ok, f'{iid} wrong "{wid}" {ws[0]["value"]!r} = {value!r}', '' if ok else 'recomputed slip differs')


def fence(s, lang=None):
    """The body of the first fenced block (of that language) in s."""
    m = re.search(r'```' + (lang or r'\w*') + r'\n(.*?)```', s, re.S)
    return m.group(1) if m else ''


def run_print(src):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(src, {})
    return out.getvalue()


def opt_text(o):
    t = o['text']
    return fence(t, 'text') if t.startswith('```') else t.strip('`')


def correct_ids(iid):
    return sorted(o['id'] for o in W(iid)['options'] if o.get('correct'))


def predict(iid, src=None):
    """Execute the item's code and check that exactly the correct option(s) print what Python prints."""
    src = src or fence(IT[iid]['prose'], 'python')
    got = run_print(src).strip()
    hits = sorted(o['id'] for o in W(iid)['options'] if opt_text(o).strip() == got)
    ok = hits == correct_ids(iid)
    ex._rec(ok, f'{iid} Python {PY} prints {got!r}: matching option {hits}', '' if ok else 'key and printed text differ')
    return got


# ---------------------------------------------------------------- metadata, shape, coverage, time
ex.claim(doc['pass'] == 0.7, 'pass 0.7')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 4, 3: 10, 4: 4, 5: 2}, f'ramp {ramp} (20, 50, 20, 10 per cent)')
union = {}
for c in ('terminal', 'first-python'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the two course.json maps')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
ex.claim(all(o.get('correct') or o.get('why') for it in doc['items'] for o in it.get('widget', {}).get('options', [])),
         'every distractor has a why')
# Paces this review sets (seconds), from topic-0.6's paces (the one Stage 0 exam that has them) and review-exam-2.2.
PACE = {'e-typing-speed': 45, 'e-three-operators': 45, 'e-header-line': 45, 'e-rename-pdf': 45,
        'e-curly-quotes': 75, 'e-up-two': 90, 'e-two-greps': 90, 'e-wrong-folder': 90, 'e-range-step': 75,
        'e-slice-format': 75, 'e-list-update': 90, 'e-print-or-return': 75, 'e-code-band': 360,
        'e-text-number': 90, 'e-move-wildcard': 120, 'e-tap-cause': 150, 'e-code-biggest-move': 600,
        'e-path-search': 150, 'e-redirect-trace': 240, 'e-code-daily-returns': 720}
ex.claim(set(PACE) == set(IT), 'a pace for every item')
total = sum(PACE.values())
ex.claim(total == 3270, f'paces sum to {total} s, {total / 60:.1f} minutes')
ex.claim(doc['minutes'] * 60 >= total, f'minutes {doc["minutes"]} covers the paces ({total / 60:.1f} min)',
         'finding: the paper needs about 55 minutes')

# ---------------------------------------------------------------- e-typing-speed
key('e-typing-speed', 1050 // 5 // 3)
ex.claim(1050 / 3 / 5 == 70, '1,050 / 3 / 5 = 70 the other way round')
wrong('e-typing-speed', 'total', 1050 // 5)
wrong('e-typing-speed', 'chars', 1050 // 3)
ex.expect('exam', f'{P("e-typing-speed")}.explain.text', 210)

# ---------------------------------------------------------------- e-three-operators
predict('e-three-operators')

# ---------------------------------------------------------------- e-header-line
lines = ['id,ticker,side,qty'] + [f'{i},VOD,buy,500' for i in range(1, 41)]
ex.claim(len(lines) == 41, 'a 41-line file is a header and 40 rows')
key('e-header-line', len(lines) - 1)
wrong('e-header-line', 'header', len(lines))
wrong('e-header-line', 'both', len(lines) - 2)

# ---------------------------------------------------------------- e-curly-quotes and e-tap-cause: real tracebacks


def traceback_of(src, stdin, ver):
    """stderr of `python<ver> <file>` run from a throwaway /home/sam-like folder, File paths cut to the base name."""
    exe = shutil.which(f'python{ver}')
    if not exe:
        return None
    d = tempfile.mkdtemp()
    try:
        p = os.path.join(d, 'script.py')
        with open(p, 'w', encoding='utf8') as f:
            f.write(src)
        r = subprocess.run([exe, p], input=stdin, capture_output=True, text=True, cwd=d)
        return [re.sub(r'File ".*?script\.py"', 'File "X"', ln) for ln in r.stderr.rstrip('\n').split('\n')]
    finally:
        shutil.rmtree(d)


def shown_tb(text):
    return [re.sub(r'File ".*?\.py"', 'File "X"', ln) for ln in fence(text, 'text').rstrip('\n').split('\n')]


cq = IT['e-curly-quotes']['prose']
cq_src = shown_tb(cq)[1].strip() + '\n'
for v in ('3.12', '3.13'):
    tb = traceback_of(cq_src, '', v)
    ok = tb is not None and tb == shown_tb(cq)
    ex._rec(ok, f'e-curly-quotes quoted SyntaxError equals python{v} output', '' if ok else f'python{v} prints {tb}')

tc = IT['e-tap-cause']
tc_src = '\n'.join(tc['canvas']['params']['lines']) + '\n'
shown = shown_tb(tc['prose'])
last = re.search(r'The last line reads `(.*?)`', tc['prose']).group(1)
for v in ('3.12', '3.13'):
    tb = traceback_of(tc_src, '190.00\n', v)
    if tb is not None:
        tb[0] = tb[0].replace('Exit price: ', '')    # the prompt is printed before the traceback on the same line
    ok = tb is not None and tb[:-1] == shown and tb[-1] == last
    ex._rec(ok, f'e-tap-cause quoted traceback equals python{v} output',
            '' if ok else f'python{v} prints {len(tb or [])} lines: {tb}')
ex.claim(tc['canvas']['params']['lines'][5].startswith('exit_price = input('), 'e-tap-cause l6 (one-based) is the input line')
ex.claim(W('e-tap-cause')['answer'] == ['l6'], 'e-tap-cause key is l6')
ex.claim('line 9' in tc['prose'] and 'trade_pnl(entry' in tc['canvas']['params']['lines'][8]
         and 'line 3' in tc['prose'] and 'return (sell - buy)' in tc['canvas']['params']['lines'][2],
         'e-tap-cause traceback line numbers 9 and 3 match the console lines')

# ---------------------------------------------------------------- e-up-two
TREE = {}


def tree(nodes, prefix, path):
    for n in nodes:
        pid = f'{prefix}-{n["id"]}' if prefix else n['id']
        fp = '/' if n['label'] == '/' else posixpath.join(path, n['label'])
        TREE[pid] = fp
        tree(n.get('children', []), pid, fp)


tree(IT['e-up-two']['canvas']['params']['nodes'], '', '')
here = TREE[IT['e-up-two']['canvas']['state']['shade']['here'][0]]
ex.claim(here == '/home/sam/research/notebooks', f'e-up-two shaded folder is {here}')
target = posixpath.normpath(posixpath.join(here, '../../fx/eurusd.csv'))
ex.claim([k for k, v in TREE.items() if v == target] == W('e-up-two')['answer'], f'e-up-two key names {target}')
ex.claim(TREE['r-f-e'] == '/fx/eurusd.csv', 'e-up-two slip r-f-e is the path read from the top')
ex.claim(TREE['r-h-s-d-f-e'] == posixpath.normpath(posixpath.join(here, '../fx/eurusd.csv')),
         'e-up-two slip r-h-s-d-f-e is one step up only')

# ---------------------------------------------------------------- e-two-greps
cat = fence(IT['e-two-greps']['prose'], 'sh').split('\n')
rows = cat[1:cat.index('$ grep BA orders.csv | grep buy | wc -l')]
first = [r for r in rows if 'BA' in r]
both = [r for r in first if 'buy' in r]
key('e-two-greps', len(both))
ex.claim([r.split(',')[0] for r in both] == ['1', '3', '5', '7'], 'e-two-greps the four lines are 1, 3, 5 and 7')
wrong('e-two-greps', 'exact', sum(1 for r in rows if r.split(',')[1:2] == ['BA'] and 'buy' in r))
wrong('e-two-greps', 'all-buys', sum(1 for r in rows if 'buy' in r))
wrong('e-two-greps', 'first', len(first))

# ---------------------------------------------------------------- e-wrong-folder, run for real
d = tempfile.mkdtemp()
try:
    home = os.path.join(d, 'sam')
    os.makedirs(os.path.join(home, 'desk', 'backtest', 'data'))
    with open(os.path.join(home, 'desk', 'backtest', 'data', 'prices.csv'), 'w') as f:
        f.write('1,2\n')
    with open(os.path.join(home, 'desk', 'backtest', 'run.py'), 'w') as f:
        f.write('open("data/prices.csv").read()\nprint("ok")\n')

    def runs(cwd, script):
        r = subprocess.run([sys.executable, script], cwd=os.path.join(home, cwd), capture_output=True, text=True)
        return r.stdout.strip() == 'ok', r.stderr.strip().split('\n')[-1]

    first_run = runs('desk', 'backtest/run.py')
    ex.claim(not first_run[0] and first_run[1] == fence(IT['e-wrong-folder']['prose'], 'text').strip(),
             f'e-wrong-folder the quoted FileNotFoundError is what python {PY} prints: {first_run[1]!r}')
    outcome = {'a': runs('desk/backtest', 'run.py')[0],
               'b': runs('desk', os.path.join(home, 'desk', 'backtest', 'run.py'))[0],
               'c': runs('desk/backtest/data', '../run.py')[0],
               'd': runs('desk', 'run.py')[0]}
    ok = sorted(k for k, v in outcome.items() if v) == correct_ids('e-wrong-folder')
    ex._rec(ok, f'e-wrong-folder only the key runs cleanly: {outcome}', '' if ok else 'key differs from the real runs')
finally:
    shutil.rmtree(d)

# ---------------------------------------------------------------- e-range-step
src = fence(IT['e-range-step']['prose'], 'python')
key('e-range-step', int(run_print(src)))
ex.claim(list(range(3, 15, 4)) == [3, 7, 11], 'range(3, 15, 4) is 3, 7, 11')
wrong('e-range-step', 'stop', 3 + 7 + 11 + 15)
wrong('e-range-step', 'count', len(range(3, 15, 4)))

# ---------------------------------------------------------------- e-slice-format
predict('e-slice-format')
ex.claim(run_print('t = "VODAFONE"; print(f"{t[:4]}: £{72.456:.2f}")').strip() == 'VODA: £72.46', 'e-slice-format option b is the end included')
ex.claim(f'{math.floor(72.456 * 100) / 100:.2f}' == '72.45', 'e-slice-format option c is the digit cut off')

# ---------------------------------------------------------------- e-list-update
predict('e-list-update')
# option b's why: "You counted positions from 1, so closes[1] = 100 replaced 101". A learner who counts from 1 reads
# closes[1] from 1 as well, the first value, so gets 98 - 100 = -2: the correct option, not -1. -1 comes from skipping
# the assignment: 98 - 99.
one_based = [101, 99, 104, 98]
one_based[0] = 100
slip_b = one_based[-1] - one_based[0]
skip = [101, 99, 104, 98]
ex.claim(skip[-1] - skip[1] == -1, 'e-list-update -1 is the result of leaving out closes[1] = 100')
ex.stated('exam', f'{P("e-list-update")}.widget.options[1].why', 'You counted positions from 1', slip_b == -1)
ex.claim(run_print('c = [101, 99, 104]\nc[1] = 100\nprint(c[-1] - c[1], len(c))').strip() == '4 3', 'e-list-update option c is the append left out')

# ---------------------------------------------------------------- e-print-or-return
predict('e-print-or-return')
ex.claim(2500 * 0.01 == 25.0, '2500 * 0.01 is exactly 25.0 in floating point')

# ---------------------------------------------------------------- e-text-number
predict('e-text-number')

# ---------------------------------------------------------------- e-move-wildcard
names = fence(IT['e-move-wildcard']['prose'], 'sh').split('\n')[1:3]
names = ' '.join(names).split()
ex.claim(sorted(names) == names and len(names) == 6, f'e-move-wildcard six names: {names}')
moved = [n for n in names if fnmatch.fnmatchcase(n, '*2024*')]
left = [n for n in names if n not in moved] + ['old']
key('e-move-wildcard', len(left))
wrong('e-move-wildcard', 'folder', len(left) - 1)
wrong('e-move-wildcard', 'edge', len([n for n in names if not re.search(r'.2024', n)]) + 1)
ex.claim(sorted(left) == ['fx_2025.csv', 'notes.txt', 'old', 'rates_2025.csv'], 'e-move-wildcard explain lists the four names')
# ls -C at 80 columns fills columns first (bash and zsh, GNU and BSD ls); the prose shows the names row by row.
col_major = [names[i::2] for i in range(2)]
shown_rows = [r.split() for r in fence(IT['e-move-wildcard']['prose'], 'sh').split('\n')[1:3]]
ex.claim(shown_rows == col_major, 'e-move-wildcard ls output is laid out as ls prints it (columns first)',
         f'ls -C at 80 columns prints {col_major}')

# ---------------------------------------------------------------- e-path-search
sh = fence(IT['e-path-search']['prose'], 'sh').split('\n')
PATH = sh[1].split(':')
folders = {}
for k in range(2, len(sh) - 1, 2):
    folders[sh[k].split()[-1]] = sh[k + 1].split()


def resolve(cmd):
    if cmd.startswith('/'):
        return posixpath.dirname(cmd)
    return next((p for p in PATH if cmd in folders.get(p, [])), None)


from_usr_bin = sorted(o['id'] for o in W('e-path-search')['options'] if resolve(o['text'].strip('`')) == '/usr/bin')
ex.claim(from_usr_bin == correct_ids('e-path-search'), f'e-path-search the commands that run from /usr/bin are {from_usr_bin}')
ex.claim(resolve('python3') == '/usr/local/bin' and resolve('pytest') == '/home/sam/.local/bin' and resolve('pip3') == '/usr/local/bin',
         'e-path-search python3, pytest and pip3 resolve where the whys say')

# ---------------------------------------------------------------- e-redirect-trace
fills = fence(IT['e-redirect-trace']['prose'], 'text').rstrip('\n').split('\n')
ex.claim(len(fills) == 9, 'e-redirect-trace a header and eight fills')
report = fills[:1] + [r for r in fills if 'VOD' in r]
sells = [r for r in report if 'sell' in r] + [r for r in fills if 'BP' in r]
key('e-redirect-trace', len(sells))
wrong('e-redirect-trace', 'overwrite', len([r for r in fills if 'BP' in r]))
wrong('e-redirect-trace', 'all-sells', len([r for r in fills if 'sell' in r]) + len([r for r in fills if 'BP' in r]))
wrong('e-redirect-trace', 'header', len(sells) + 1)
ex.claim(len(report) == 5 and len([r for r in report if 'sell' in r]) == 2, 'e-redirect-trace report.csv 5 lines, two VOD sells')

# ---------------------------------------------------------------- code harness (follows code.js)


def run_cases(src, w):
    """One row per hidden test: (ok, row_error). Script mode when any case has stdin or compares stdout."""
    script = any('stdin' in c or c.get('compare') == 'stdout' for c in w['tests'] + w.get('examples', []))
    rows = []
    for c in w['tests']:
        d = tempfile.mkdtemp()
        old = os.getcwd()
        os.chdir(d)
        try:
            ns = {'__name__': '__main__'}
            out = io.StringIO()
            try:
                if script:
                    feed = io.StringIO(c.get('stdin', ''))
                    real_in = sys.stdin
                    sys.stdin = feed
                    try:
                        with contextlib.redirect_stdout(out):
                            exec(src, ns)
                    finally:
                        sys.stdin = real_in
                    ns['printed'] = out.getvalue().splitlines()
                    if c.get('compare') == 'stdout':
                        norm = lambda s: '\n'.join(ln.rstrip() for ln in s.strip('\n').split('\n')).strip()  # noqa: E731
                        rows.append((norm(out.getvalue()) == norm(c['expect']), None))
                        continue
                else:
                    with contextlib.redirect_stdout(out):
                        exec(src, ns)
                        if c.get('setup'):
                            exec(c['setup'], ns)
                got = eval(c['call'], ns)
                exp = eval(str(c['expect']), {})    # expect is Python source, as code.js reads it
                if c.get('compare') == 'isclose':
                    ok = math.isclose(float(got), float(exp), rel_tol=1e-9, abs_tol=1e-12)
                else:
                    ok = got == exp
                rows.append((ok, None))
            except Exception as e:  # a row error, keyed test-N by code.js, not `error`
                rows.append((False, f'{type(e).__name__}: {e}'))
        finally:
            os.chdir(old)
            shutil.rmtree(d)
    return rows


def first_fail(src, w):
    rows = run_cases(src, w)
    k = next((i for i, r in enumerate(rows) if not r[0]), None)
    return (None if k is None else k + 1), rows


def code_item(iid, slips):
    """Solution passes all, starter fails one, examples pass; each slip's first failing test is the one named."""
    w = W(iid)
    f, rows = first_fail(w['solution'], w)
    ex._rec(f is None, f'{iid} solution passes {sum(r[0] for r in rows)} of {len(rows)} hidden tests ({PY})',
            '' if f is None else f'test {f} fails: {rows[f - 1]}')
    ex_w = dict(w, tests=w['examples'])
    fe, _ = first_fail(w['solution'], ex_w)
    ex._rec(fe is None, f'{iid} solution passes every example', '')
    fs, rows = first_fail(w['starter'], w)
    ex._rec(fs is not None, f'{iid} starter fails {sum(not r[0] for r in rows)} of {len(rows)} hidden tests', '')
    same = [i + 1 for i, t in enumerate(w['tests']) if any(t.get('call') == e.get('call') and t.get('setup') == e.get('setup')
                                                           and t.get('stdin') == e.get('stdin') for e in w['examples'])]
    print(f'  note: {iid} hidden tests equal to an example: {same}')
    for label, src, want in slips:
        f, rows = first_fail(src, w)
        fb = IT[iid]['feedback']['byKey']
        if want == 'error':
            # byKey.error shows only when the code fails to load (code.js); a runtime error inside a case is a row
            # error, keyed test-N. So the slip this line names never reaches it.
            ex._rec(False, f'{iid} slip "{label}" reaches byKey.error',
                    f'it fails at test {f} with a row error ({rows[f - 1][1] if f else None}), so the key is test-{f}')
            continue
        named = f'test-{f}' in fb
        ok = f == want and named
        ex._rec(ok, f'{iid} slip "{label}" fails first at test {f} (byKey test-{want} expected)',
                '' if ok else f'first failure {f}, row {rows[f - 1] if f else None}, byKey line for it: {named}')


band = W('e-code-band')['solution']
code_item('e-code-band', [
    ('edges counted outside', band.replace('c < low or c > high', 'c <= low or c >= high'), 2),
    ('above high only', band.replace('c < low or c > high', 'c > high'), 4),
])
xs = [100 + (i % 21) - 10 for i in range(1000)]
per = sum(1 for v in range(90, 111) if v < 95 or v > 105)
ex.claim(per * (1000 // 21) + sum(1 for i in range(1000 % 21) if 90 + i < 95 or 90 + i > 105) == 475
         == sum(1 for v in xs if v < 95 or v > 105), 'e-code-band 1,000-close test is 475 by offset counting')

bm = W('e-code-biggest-move')['solution']
code_item('e-code-biggest-move', [
    ('no abs', bm.replace('abs(closes[i] - closes[i - 1])', 'closes[i] - closes[i - 1]'), 2),
    ('blank line not skipped', bm.replace('        if line.strip() == "":\n            continue\n', ''), 5),
    ('fixed file name', bm.replace('open(path)', "open('prices.csv')"), 6),
    ('header kept (byKey.error names it)', bm.replace('lines[1:]', 'lines'), 1),
])
rowsets = [t['setup'] for t in W('e-code-biggest-move')['tests']]
ns = {}
exec(rowsets[6].replace("open('prices.csv', 'w').write('\\n'.join(rows) + '\\n')", ''), ns)
cl = [float(r.split(',')[1]) for r in ns['rows'][1:]]
big = max(abs(b - a) for a, b in zip(cl, cl[1:]))
ex.claim(round(big, 2) == float(W('e-code-biggest-move')['tests'][6]['expect']), f'e-code-biggest-move 2,000-row test {big:.6f} by zip')

dr = W('e-code-daily-returns')['solution']
code_item('e-code-daily-returns', [
    ('best starts at 0', dr.replace('best = None\n', 'best = 0\n').replace('if best is None or r > best', 'if r > best'), 6),
    ('ties to the later day', dr.replace('r > best', 'r >= best'), 5),
    ('no Best: none', dr.replace('if best_day is None:\n    print("Best: none")\nelse:\n    ', '').replace('\n    print(f"Best: day', '\nprint(f"Best: day'), 3),
    ('reads one close too many (byKey.error names it)', dr.replace('for i in range(n):', 'for i in range(n + 1):'), 'error'),
])
for t in W('e-code-daily-returns')['tests'][:6]:
    c = [float(x) for x in t['stdin'].split()[1:]]
    rs = [(b - a) / a * 100 for a, b in zip(c, c[1:])]
    lines_ = [f'Day {k + 1}: {r:.2f}%' for k, r in enumerate(rs)]
    lines_.append('Best: none' if not rs else f'Best: day {rs.index(max(rs)) + 1}')
    ex.claim('\n'.join(lines_) == t['expect'].strip(), f'e-code-daily-returns stdin {t["stdin"].split()} by a list rewrite')

# ---------------------------------------------------------------- continuity: every construct is taught
CTXT = []
for c in ('terminal', 'first-python'):
    for fn in sorted(os.listdir(os.path.join(COURSES, c))):
        if fn.endswith('.json') and fn != 'course.json':
            with open(os.path.join(COURSES, c, fn), encoding='utf8') as f:
                for s in __import__('numbers_lib')._strings(json.load(f)):
                    CTXT.append(s)


def taught(iid, label, pattern):
    hit = any(re.search(pattern, s) for s in CTXT)
    ex._rec(hit, f'{iid} needs {label}: taught in terminal or first-python', '' if hit else 'no lesson, review or homework shows it')


taught('e-range-step', '`range` with a step', r'range\([^()]*,[^()]*,[^()]*\)')
taught('e-range-step', '`+=`', r'\w \+= ')
taught('e-slice-format', 'a slice with the start left out', r'\w\[:\d')
taught('e-text-number', '`int` of a float', r'int\(\s*-?\d+\.\d+\s*\)|int\(float\(')
taught('e-code-band', 'boolean `or` in a condition', r'if [^\n]*(?:<|>|==)[^\n]* or [^\n]*:')
taught('e-code-biggest-move', '`abs`', r'abs\(')
taught('e-code-daily-returns', '`is None`', r'is None')
taught('e-redirect-trace', '`>>`', r'(?<!>)>>(?!>)')
taught('e-move-wildcard', '`*` matching no characters', r'any characters, even none')
taught('e-two-greps', 'grep matching anywhere in a line', r'anywhere in each line')
taught('e-path-search', 'the PATH searched left to right', r'left to right')
taught('e-tap-cause', '`input()` returning a str', r'always returns a \*\*str\*\*|always returns a str')

ex.check_wrongs()
ex.report()
