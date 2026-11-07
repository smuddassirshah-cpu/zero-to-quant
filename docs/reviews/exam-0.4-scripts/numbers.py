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
Pure standard library. Run with python3.12 only (Pyodide 0.27.7 is 3.12.7); it exits 0 after the fix pass and asserts the interpreter version.
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
        'e-curly-quotes': 75, 'e-up-two': 90, 'e-two-greps': 90, 'e-wrong-folder': 120, 'e-range-step': 75,
        'e-slice-format': 75, 'e-list-update': 90, 'e-print-or-return': 90, 'e-code-band': 360,
        'e-text-number': 90, 'e-move-wildcard': 120, 'e-tap-cause': 150, 'e-code-biggest-move': 600,
        'e-path-search': 150, 'e-redirect-trace': 240, 'e-code-daily-returns': 720}
ex.claim(set(PACE) == set(IT), 'a pace for every item')
total = sum(PACE.values())
ex.claim(total == 3315, f'paces sum to {total} s, {total / 60:.1f} minutes')
ex.claim(doc['minutes'] == 60 and doc['minutes'] * 60 >= total, f'minutes {doc["minutes"]} covers the paces ({total / 60:.1f} min)',
         'AUTHORING section 5: set minutes to the time the exam needs')
ex.claim(all(it.get('pace') == PACE[it['id']] for it in doc['items']), 'every item stores the pace this script lists')
ex.claim(sys.version_info[:2] == (3, 12), f'run under Python 3.12 (Pyodide 0.27.7 is 3.12.7); this is {PY}')

# ---------------------------------------------------------------- e-typing-speed
key('e-typing-speed', 60 * 5 * 3)
ex.claim(60 * 3 * 5 == 900 and 900 / 3 / 5 == 60, '900 characters over 3 minutes at 5 a word is 60 words a minute, the other way round')
wrong('e-typing-speed', 'one-minute', 60 * 5)
wrong('e-typing-speed', 'words', 60 * 3)
wrong('e-typing-speed', 'divided', 60 // 5 * 3)
ex.claim('300 characters' in IT['e-typing-speed']['feedback']['correct'] and '$60 \\times 5 = 300$' in IT['e-typing-speed']['explain']['text']
         and '$300 \\times 3 = 900$' in IT['e-typing-speed']['explain']['text'], 'e-typing-speed feedback and explain state 300 and 900')

# ---------------------------------------------------------------- e-three-operators
predict('e-three-operators')

# ---------------------------------------------------------------- e-header-line
lines = ['id,ticker,side,qty'] + [f'{i},VOD,buy,500' for i in range(1, 41)]
ex.claim(len(lines) == 41 and '41 trades.csv' in IT['e-header-line']['prose'], 'a 41-line file is a header and 40 rows')
early = lines[:30]    # head -n 30 trades.csv > early.csv
ex.claim('head -n 30 trades.csv > early.csv' in IT['e-header-line']['prose'], 'e-header-line prose runs head -n 30')
key('e-header-line', len(early) - 1)
wrong('e-header-line', 'header', len(early))
wrong('e-header-line', 'all', len(lines) - 1)
wrong('e-header-line', 'rest', len(lines) - len(early))

# ---------------------------------------------------------------- e-curly-quotes ("Two Pythons") and e-tap-cause
def vkey(v):
    return tuple(int(x) for x in re.search(r'(\d+(?:\.\d+)+)', v).group(1).split('.'))


cq = IT['e-curly-quotes']
cq_sh = fence(cq['prose'], 'sh').split('\n')
vers = {cq_sh[0].split()[1]: vkey(cq_sh[1]), cq_sh[2].split()[1]: vkey(cq_sh[3])}
need = vkey(re.search(r'Python (3\.\d+) or newer', cq['prose']).group(1))
fine = sorted(c for c, v in vers.items() if v[:2] >= need)
ex.claim(vers == {'python3': (3, 9, 6), '/usr/local/bin/python3': (3, 13, 1)} and need == (3, 10), f'e-curly-quotes versions {vers}, need {need}')
ex.claim(fine == ['/usr/local/bin/python3'] and cq['widget']['options'][0]['text'] == '`/usr/local/bin/python3 backtest.py`'
         and cq['widget']['options'][0].get('correct'), 'e-curly-quotes only the full path is new enough, and it is the key')
ex.claim((3, 13, 1)[:2] > (3, 10) and (3, 9, 6)[:2] < (3, 10) and 3.13 < 3.9, 'e-curly-quotes part-by-part, and decimals would flip it (3.13 < 3.9)')
ex.claim(sum(1 for o in cq['widget']['options'] if o.get('correct')) == 1 and len(cq['widget']['options']) == 4, 'e-curly-quotes one key of four')

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


tc = IT['e-tap-cause']
tc_src = '\n'.join(tc['canvas']['params']['lines']) + '\n'
shown = shown_tb(tc['prose'])
last = re.search(r'The last line reads `(.*?)`', tc['prose']).group(1)
for v in ('3.12',):    # 3.13 leaves out the caret line under the call frame, so only 3.12 (Pyodide) is the reference
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
upath = re.search(r'opens `([^`]*)`', IT['e-up-two']['prose']).group(1)
ex.claim(upath == '../../research/../fx/eurusd.csv', f'e-up-two path {upath}')
target = posixpath.normpath(posixpath.join(here, upath))
ex.claim(target == '/home/sam/fx/eurusd.csv', f'e-up-two the path resolves to {target}')
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

# ---------------------------------------------------------------- e-wrong-folder, run for real (VS Code opens ~/desk)
d = tempfile.mkdtemp()
try:
    home = os.path.join(d, 'sam')
    os.makedirs(os.path.join(home, 'desk', 'backtest'))
    os.makedirs(os.path.join(home, 'desk', 'inputs'))
    with open(os.path.join(home, 'desk', 'inputs', 'closes.csv'), 'w') as f:
        f.write('1,2\n')
    with open(os.path.join(home, 'desk', 'backtest', 'run.py'), 'w') as f:
        f.write('open("../inputs/closes.csv").read()\nprint("ok")\n')
    wf = IT['e-wrong-folder']
    ex.claim("opens `../inputs/closes.csv`" in wf['prose'] and '`~/desk/inputs/closes.csv`' in wf['prose'], 'e-wrong-folder prose names ../inputs/closes.csv = ~/desk/inputs/closes.csv')

    def runs(cwd, script):
        r = subprocess.run([sys.executable, script], cwd=os.path.join(home, cwd), capture_output=True, text=True)
        return r.stdout.strip() == 'ok', r.stderr.strip().split('\n')[-1]

    first_run = runs('desk', 'backtest/run.py')    # the terminal opens in ~/desk
    ex.claim(not first_run[0] and first_run[1] == fence(wf['prose'], 'text').strip(),
             f'e-wrong-folder the quoted FileNotFoundError is what python {PY} prints: {first_run[1]!r}')
    outcome = {'a': runs('desk/backtest', 'run.py')[0],
               'b': runs('desk', os.path.join(home, 'desk', 'backtest', 'run.py'))[0],
               'c': runs('desk/inputs', '../backtest/run.py')[0],
               'd': runs('.', 'desk/backtest/run.py')[0]}    # `cd ~` is the sam folder
    ok = sorted(k for k, v in outcome.items() if v) == correct_ids('e-wrong-folder') == ['a', 'c']
    ex._rec(ok, f'e-wrong-folder exactly the keys a and c run cleanly: {outcome}', '' if ok else 'keys differ from the real runs')
    ex.claim(wf['widget']['kind'] == 'multi', 'e-wrong-folder is a multi item (two keys)')
finally:
    shutil.rmtree(d)

# ---------------------------------------------------------------- e-range-step (now a while loop)
src = fence(IT['e-range-step']['prose'], 'python')
key('e-range-step', int(run_print(src)))
trace = []
total, k = 0, 2
while total < 20:
    total = total + k
    k = k + 3
    trace.append((total, k))
ex.claim(trace == [(2, 5), (7, 8), (15, 11), (26, 14)], f'e-range-step passes (total, k): {trace}')
wrong('e-range-step', 'total', trace[-1][0])
wrong('e-range-step', 'early', trace[2][1])
wrong('e-range-step', 'extra', trace[-1][1] + 3)
ex.claim('2, 7, 15 and 26' in IT['e-range-step']['explain']['text'] and '5, 8, 11 and 14' in IT['e-range-step']['explain']['text'],
         'e-range-step explain lists the passes')

# ---------------------------------------------------------------- e-slice-format
predict('e-slice-format')
ex.claim('LSE:BARC'[4:8] == 'BARC' and 'LSE:BARC'[3:7] == ':BAR' and 'LSE:BARC'[4] == 'B', 'e-slice-format code[4:8] is BARC, code[3:7] is :BAR')
ex.claim(f'{1.876:.2f}' == '1.88' and f'{math.floor(1.876 * 100) / 100:.2f}' == '1.87', 'e-slice-format 1.876 rounds to 1.88, cut to 1.87')

# ---------------------------------------------------------------- e-list-update
predict('e-list-update')
# option b's why: "You left out closes[1] = 100. It replaces 99". Leaving the assignment out gives 98 - 99 = -1.
# (A learner who counts from 1 reads closes[1] as 100 as well and gets -2, the key, so that cannot be the slip.)
skip = [101, 99, 104, 98]
ex.claim(skip[-1] - skip[1] == -1 and len(skip) == 4, 'e-list-update -1 is the result of leaving out closes[1] = 100')
ex.stated('exam', f'{P("e-list-update")}.widget.options[1].why', 'You left out `closes[1] = 100`', skip[-1] - skip[1] == -1)
ex.claim('counted positions from 1' not in IT['e-list-update']['widget']['options'][1]['why'], 'e-list-update option b no longer blames counting from 1')
ex.claim(run_print('c = [101, 99, 104]\nc[1] = 100\nprint(c[-1] - c[1], len(c))').strip() == '4 3', 'e-list-update option c is the append left out')

# ---------------------------------------------------------------- e-print-or-return
predict('e-print-or-return')
ex.claim(2500 * 0.01 == 25.0 and 1000 * 0.01 == 10.0 and 25.0 + 10.0 == 35.0, '2500 * 0.01, 1000 * 0.01 and their sum are exact: 25.0, 10.0, 35.0')

# ---------------------------------------------------------------- e-text-number
predict('e-text-number')

# ---------------------------------------------------------------- e-move-wildcard
ls_rows = fence(IT['e-move-wildcard']['prose'], 'sh').split('\n')[1:3]
cols = [r.split() for r in ls_rows]
names = [n for pair in zip(*cols) for n in pair]    # ls fills columns first: read the two rows column by column
ex.claim(sorted(names) == names and len(names) == 6, f'e-move-wildcard six names: {names}')
moved = [n for n in names if fnmatch.fnmatchcase(n, '*2024*')]
left = [n for n in names if n not in moved] + ['old']
key('e-move-wildcard', len(left))
wrong('e-move-wildcard', 'folder', len(left) - 1)
wrong('e-move-wildcard', 'edge', len([n for n in names if not re.search(r'.2024', n)]) + 1)
ex.claim(sorted(left) == ['fx_2025.csv', 'notes.txt', 'old', 'rates_2025.csv'], 'e-move-wildcard explain lists the four names')
# ls -C at 80 columns fills columns first (bash and zsh, GNU and BSD ls); the prose shows the names row by row.
col_major = [names[i::2] for i in range(2)]
shown_rows = cols
widths = [max(len(n) for n in c) + 2 for c in zip(*col_major)]
ls_text = ['' .join(n.ljust(w) for n, w in zip(r, widths)).rstrip() for r in col_major]
ex.claim(ls_text == ls_rows, 'e-move-wildcard the two rows carry the exact spacing ls -C prints (column width = longest name + 2)', f'{ls_text}')
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
    ex._rec(not same, f'{iid} no hidden test repeats an example', f'tests {same} equal an example')
    reached = set()
    for label, src, want in slips:
        fb = IT[iid]['feedback']['byKey']
        if want == 'error':
            # code.js keys `error` only when the code fails to load (a syntax error does; a runtime error inside a case is a row error)
            try:
                compile(src, '<slip>', 'exec')
                loads = True
            except SyntaxError:
                loads = False
            ok = not loads and 'error' in fb
            ex._rec(ok, f'{iid} slip "{label}" fails to load, so byKey.error shows', '' if ok else 'the slip loads')
            reached.add('error')
            continue
        f, rows = first_fail(src, w)
        named = f'test-{f}' in fb
        ok = f == want and named
        if ok:
            reached.add(f'test-{f}')
        ex._rec(ok, f'{iid} slip "{label}" fails first at test {f} (byKey test-{want} expected)',
                '' if ok else f'first failure {f}, row {rows[f - 1] if f else None}, byKey line for it: {named}')
    ex._rec(set(IT[iid]['feedback']['byKey']) == reached, f'{iid} every byKey line is reached by a planted slip: {sorted(reached)}',
            f'unreached: {sorted(set(IT[iid]["feedback"]["byKey"]) - reached)}')


SYNTAX = 'def broken(:\n    pass\n'
band = W('e-code-band')['solution']
code_item('e-code-band', [
    ('edges counted outside', band.replace('c < low', 'c <= low').replace('c > high', 'c >= high'), 2),
    ('above high only (test-4: every close below)', band.replace('        if c < low:\n            count = count + 1\n        elif', '        if False:\n            count = count + 1\n        elif'), 4),
    ('below low only (test-1: two closes above)', band.replace('elif c > high', 'elif False'), 1),
    ('does not load', SYNTAX, 'error'),
])
ex.claim(eval(W('e-code-band')['tests'][0]['call'], {'days_outside': lambda cl, lo, hi: sum(1 for c in cl if c < lo or c > hi)}) == 2
         == int(W('e-code-band')['tests'][0]['expect']),
         'e-code-band tests[0] ([106.0, 100.0, 107.5, 104.9], band 98 to 105) is 2: 106.0 and 107.5 are above')
xs = [100 + (i % 21) - 10 for i in range(1000)]
per = sum(1 for v in range(90, 111) if v < 95 or v > 105)
ex.claim(per * (1000 // 21) + sum(1 for i in range(1000 % 21) if 90 + i < 95 or 90 + i > 105) == 475
         == sum(1 for v in xs if v < 95 or v > 105), 'e-code-band 1,000-close test is 475 by offset counting')

bm = W('e-code-biggest-move')['solution']
code_item('e-code-biggest-move', [
    ('no abs', bm.replace('abs(closes[i] - closes[i - 1])', 'closes[i] - closes[i - 1]'), 2),
    ('blank line not skipped', bm.replace('        if line.strip() != "":\n', '        if True:\n'), 5),
    ('fixed file name', bm.replace('open(path)', "open('prices.csv')"), 6),
    ('header kept (ValueError inside test 1)', bm.replace('lines[1:]', 'lines'), 1),
    ('does not load', SYNTAX, 'error'),
])
t0 = W('e-code-biggest-move')['tests'][0]
ex.claim(abs(65.05 - 63.10) > abs(63.10 - 64.20) and round(abs(65.05 - 63.10), 2) == 1.95 == float(t0['expect'])
         and '64.20' in t0['setup'] and '63.10' in t0['setup'] and '65.05' in t0['setup'], 'e-code-biggest-move tests[0] biggest move is 1.95 (1.10 and 1.95)')
ex.claim('`abs(x)` drops a number' in IT['e-code-biggest-move']['prose'], 'e-code-biggest-move prose defines abs in one line')
rowsets = [t['setup'] for t in W('e-code-biggest-move')['tests']]
ns = {}
exec(rowsets[6].replace("open('prices.csv', 'w').write('\\n'.join(rows) + '\\n')", ''), ns)
cl = [float(r.split(',')[1]) for r in ns['rows'][1:]]
big = max(abs(b - a) for a, b in zip(cl, cl[1:]))
ex.claim(round(big, 2) == float(W('e-code-biggest-move')['tests'][6]['expect']), f'e-code-biggest-move 2,000-row test {big:.6f} by zip')

dr = W('e-code-daily-returns')['solution']
code_item('e-code-daily-returns', [
    ('best starts at 0', dr.replace('    if day == 1:\n        best = r\n        best_day = 1\n    elif r > best:', '    if r > best:'), 6),
    ('ties to the later day', dr.replace('elif r > best', 'elif r >= best'), 5),
    ('no Best: none', dr.replace('if best_day == 0:\n    print("Best: none")\nelse:\n    print(f"Best: day {best_day}")', 'print(f"Best: day {best_day}")'), 3),
    ('reads one close too many (EOFError inside test 1)', dr.replace('for i in range(n):', 'for i in range(n + 1):'), 1),
    ('does not load', SYNTAX, 'error'),
])
ex.claim(first_fail(dr.replace('for i in range(n):', 'for i in range(n + 1):'), W('e-code-daily-returns'))[1][0][1].startswith('EOFError'),
         'e-code-daily-returns the extra read raises EOFError in test 1')
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


# The seven constructs the first review found untaught must not be needed by any item's code now.
def code_of(it):
    txt = json.dumps(it, ensure_ascii=False).replace('\\n', '\n').replace('\\"', '"')
    w = it.get('widget', {})
    return '\n'.join(re.findall(r'```python\n(.*?)```', txt, re.S) + [w.get('solution', ''), w.get('starter', '')])


ALL = '\n'.join(code_of(it) for it in doc['items'])
for label, pat in [('range with a step', r'range\([^()]*,[^()]*,[^()]*\)'), ('+=', r'\+='), ('boolean or', r'\b(?:if|elif|while)\b[^\n]*\bor\b'),
                   ('is None', r'\bis (?:not )?None\b'), ('a slice with no start', r'\w\[:\d'), ('int of a float', r'\bint\(\s*float\(|\bint\(\s*\d+\.\d+')]:
    ex.claim(not re.search(pat, ALL), f'no item needs {label}')
ex.claim(sum(1 for it in doc['items'] if re.search(r'\babs\(', code_of(it))) == 1 and '`abs(x)` drops' in IT['e-code-biggest-move']['prose'],
         'abs is used only in e-code-biggest-move, and its prose defines it')

taught('e-range-step', '`while`', r'while \w+ < ')
taught('e-range-step', 'a running total (`total = total + p`)', r'total = total \+ ')
taught('e-slice-format', 'a slice with both ends, `s[a:b]`', r'\w\[\d+:\d+\]')
taught('e-text-number', 'text times a whole number repeats it', r'"3" \* 2')
taught('e-text-number', '`float(...)` of text', r'float\(')
taught('e-code-band', '`elif`', r'\belif\b')
ex.claim('continue' not in W('e-code-biggest-move')['solution'], 'e-code-biggest-move solution avoids continue (not taught)')
taught('e-code-biggest-move', '`.strip()`', r'\.strip\(\)')
taught('e-code-biggest-move', '`splitlines`', r'splitlines')
taught('e-code-biggest-move', '`round(`', r'round\(')
taught('e-code-daily-returns', 'a loop over `range(1, n)`', r'range\(1, ')
taught('e-code-daily-returns', '`float(input())`', r'float\(input\(')
taught('e-code-daily-returns', 'starting from a real value', r'Start from a real value')
taught('e-header-line', '`head -n`', r'head -n \d')
taught('e-curly-quotes', '`python3 --version`', r'python3 --version')
taught('e-curly-quotes', 'versions compared part by part', r'part by part|minor')
taught('e-wrong-folder', "VS Code's built-in terminal", r'built-in terminal')
taught('e-print-or-return', '`return` handing a value back', r'return')
taught('e-redirect-trace', '`>>`', r'(?<!>)>>(?!>)')
taught('e-move-wildcard', '`*` matching no characters', r'any characters, even none')
taught('e-two-greps', 'grep matching anywhere in a line', r'anywhere in each line')
taught('e-path-search', 'the PATH searched left to right', r'left to right')
taught('e-tap-cause', '`input()` returning a str', r'always returns a \*\*str\*\*|always returns a str')

ex.check_wrongs()
ex.report()
