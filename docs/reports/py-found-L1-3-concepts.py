"""py-found levels 1 to 3: concept audit checks (blind audit, session 10).

Run from the repo root:  python3 -I docs/reports/py-found-L1-3-concepts.py
It also runs unchanged inside Pyodide 0.27.7 (CPython 3.12 on WebAssembly), the runtime learners use, when the
eighteen JSON files are copied beside it; the audit file records both runs.

Three blocks:
  A. every Python code widget in scope: the model solution passes every example and hidden test, the starter fails one;
  B. every "what does it print / what happens" item with a Python block: the block is run, the keyed option must
     describe what really happens and every other option must not (numeric items: the key equals the output, each
     slip differs);
  C. hand-written checks of the claims made in prose, hints, feedback and explanations (floats, slices, aliasing,
     copies, defaults, dict and set behaviour, imports, csv, exceptions, classes, stated numbers).
A check that fails because the content is wrong is named `FINDING n` (n is the finding number in
docs/reviews/audit-py-found-1-3.md) and stays failing until the content is fixed. Exit code: 0 when nothing fails.
"""
import contextlib
import csv
import io
import json
import math
import os
import random
import re
import statistics
import sys
import tempfile
from datetime import datetime
from decimal import Decimal
from math import comb

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'py-found')
except NameError:  # Pyodide runPython: the JSON files sit in the working directory
    ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, 'l1-why-not-0-3.json')):
    ROOT = os.getcwd()

LESSONS = ['l1-why-not-0-3', 'l2-slicing', 'l3-unpacking', 'l4-one-line-lists', 'l5-lookup-by-name', 'l6-membership',
           'l7-arguments', 'l8-who-changes-the-list', 'l9-splitting-files', 'l10-reading-a-csv',
           'l11-when-things-go-wrong', 'l12-data-with-behaviour']
SETS = ['review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3']
DOCS = {n: json.load(open(os.path.join(ROOT, n + '.json'), encoding='utf-8')) for n in LESSONS + SETS}

passed = 0
failed = []      # (label, detail) for unexpected failures
findings = []    # (n, label, detail) for failures tied to a finding


def ok(label, cond, detail='', finding=None):
    global passed
    if cond:
        passed += 1
    elif finding is not None:
        findings.append((finding, label, detail))
    else:
        failed.append((label, detail))


def chk(label, fn, finding=None):
    """fn() returns a truthy value when the content's claim holds."""
    try:
        res = fn()
        ok(label, bool(res), '' if res else 'claim does not hold', finding)
    except Exception as e:  # noqa: BLE001
        ok(label, False, f'{type(e).__name__}: {e}', finding)


def raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    except Exception:  # noqa: BLE001
        return False
    return False


def nodes(name):
    doc = DOCS[name]
    for key in ('screens', 'quiz', 'items'):
        for i, n in enumerate(doc.get(key, [])):
            yield f'{key}[{i}]', n


def node(name, path):
    x = DOCS[name]
    for key, idx in re.findall(r'([A-Za-z_][\w-]*)|\[(\d+)\]', path):
        x = x[key] if key else x[int(idx)]
    return x


def text_of(name, path):
    return node(name, path)


# ---------------------------------------------------------------- A. code widgets
def close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
    return a == b


def run_tests(code, w, tests):
    ns = {'__name__': '__main__'}
    out = []
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            exec(w.get('prelude', ''), ns)
            exec(code, ns)
        except Exception:  # noqa: BLE001
            return [False] * len(tests)
        ns['__learner_source__'] = code
        for t in tests:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                got = eval(t['call'], ns)
                err = None
            except Exception as e:  # noqa: BLE001
                got, err = None, e
            exp = t['expect']
            exp = eval(exp, ns) if isinstance(exp, str) else exp
            cmp_ = t.get('compare', 'equal')
            if cmp_ == 'raises':
                out.append(err is not None and isinstance(err, exp))
            elif err is not None:
                out.append(False)
            elif cmp_ == 'isclose':
                out.append(close(got, exp))
            else:
                out.append(got == exp and type(got) is type(exp) or got == exp)
    return out


n_widgets = 0
for name in LESSONS + SETS:
    for path, n in nodes(name):
        w = n.get('widget') or {}
        if w.get('kind') != 'code' or w.get('language') != 'python':
            continue
        n_widgets += 1
        tests = w.get('tests', [])
        sol = run_tests(w['solution'], w, tests)
        ok(f'A {name} {path}: solution passes all {len(tests)} tests', all(sol) and len(tests) > 0,
           f'failing tests {[i + 1 for i, r in enumerate(sol) if not r]}')
        ex = run_tests(w['solution'], w, w.get('examples', []))
        ok(f'A {name} {path}: solution passes its examples', all(ex), str(ex))
        st = run_tests(w['starter'], w, tests)
        ok(f'A {name} {path}: starter fails at least one test', not all(st))
        # feedback keys test-N must name a real test
        for k in (n.get('feedback', {}).get('byKey') or {}):
            m = re.fullmatch(r'test-(\d+)', k)
            if m:
                ok(f'A {name} {path}: byKey.{k} names a real test', 1 <= int(m.group(1)) <= len(tests))


# ---------------------------------------------------------------- B. predict-the-output items
def run_block(code):
    buf = io.StringIO()
    exc = None
    ns = {'__name__': '__main__'}
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(code, '<prose>', 'exec'), ns)
        except BaseException as e:  # noqa: BLE001  (SyntaxError included)
            exc = e
    return buf.getvalue(), exc


def blocks(prose):
    return re.findall(r'```python\n(.*?)```', prose or '', flags=re.S)


def spans(text):
    return re.findall(r'`([^`]*)`', text)


def describes(text, out, exc):
    """Does this option text describe the run (stdout `out`, exception `exc`)?"""
    if exc is not None:
        name = type(exc).__name__
        if not re.search(r'\b' + name + r'\b', text):
            return False
        for s in spans(text):  # a quoted "XError: message" must match the real message
            m = re.fullmatch(r'(\w+Error): (.+)', s)
            if m and not f'{name}: {exc}'.startswith(f'{m.group(1)}: {m.group(2)}'):
                return False
        return True
    if re.search(r'\b\w+Error\b|\ban error\b|\bAn error\b|traceback', text):
        return False
    lines = out.rstrip('\n').split('\n') if out.strip() else []
    sp = spans(text)
    return sp == lines or [' '.join(sp)] == lines


PY12 = '''
class Position:
    def __init__(self, ticker, qty, avg_price):
        self.ticker = ticker
        self.qty = qty
        self.avg_price = avg_price

    def value(self, price):
        return self.qty * price

shel = Position("SHEL", 150, 26.40)
azn = Position("AZN", 40, 104.20)
'''
CSVTEXT = 'text = "date,close\\n2024-03-11,101.20\\n2024-03-12,102.50\\n2024-03-13,99.80\\n2024-03-14,100.40\\n"\n' \
          'import csv\nrows = list(csv.DictReader(text.splitlines()))\n'
RETS10 = 'rets = [0.012, -0.034, 0.005, -0.008, 0.021, 0.0, -0.015, 0.009, -0.002, 0.017]\n'
CLOSES6 = 'closes = [101.20, 102.50, 99.80, 100.40, 103.10, 104.00]\n'

# (file, path) -> replacement or setup. ('pre', code) runs code first; ('code', code) replaces the prose blocks;
# ('manual', why) means the item is checked by hand in block C.
OVERRIDE = {
    ('l3-unpacking', 'quiz[2]'): ('manual', 'last line only: C'),
    ('l5-lookup-by-name', 'screens[8]'): ('manual', 'summary block, numeric about len(d): C'),
    ('l6-membership', 'screens[4]'): ('manual', 'comparison counts: C'),
    ('l6-membership', 'screens[7]'): ('manual', 'which makes an empty set: C'),
    ('l8-who-changes-the-list', 'screens[9]'): ('manual', 'which leaves xs unchanged: C'),
    ('l4-one-line-lists', 'screens[2]'): ('pre', RETS10),
    ('l7-arguments', 'screens[2]'): ('manual', 'which call is an error: C'),
    ('l7-arguments', 'screens[8]'): ('code', 'def f(a, b=2, c=None):\n    if c is None:\n        c = []\n    return a, b, c\nprint(f(1, c=[5]))\n'),
    ('l9-splitting-files', 'screens[1]'): ('manual', 'two files: C'),
    ('l9-splitting-files', 'screens[3]'): ('code', 'def simple_return(p0: float, p1: float) -> float:\n    return p1 / p0 - 1\n\nprint(simple_return("100", "105"))\n'),
    ('l9-splitting-files', 'screens[4]'): ('manual', 'two files: C'),
    ('l9-splitting-files', 'quiz[2]'): ('manual', 'shadowing: C'),
    ('l10-reading-a-csv', 'screens[1]'): ('pre', CSVTEXT),
    ('l10-reading-a-csv', 'screens[3]'): ('code', 'import csv\ntext = "date, close\\n2024-03-11, 101.20\\n2024-03-12, 102.50\\n"\nfor row in csv.DictReader(text.splitlines()):\n    print(row["close"])\n'),
    ('l10-reading-a-csv', 'screens[4]'): ('pre', CSVTEXT),
    ('l10-reading-a-csv', 'quiz[0]'): ('pre', "row = {'date': '2024-03-11', 'close': '101.20'}\n"),
    ('l10-reading-a-csv', 'quiz[1]'): ('pre', 'import csv\ntext = "date,close\\n1,1.0\\n2,2.0\\n3,3.0\\n4,4.0\\n5,5.0\\n\\n"\n'),
    ('l11-when-things-go-wrong', 'screens[1]'): ('pre', 'raw = ["101.20", "102.50", "n/a", "100.40"]\n'),
    ('l11-when-things-go-wrong', 'screens[6]'): ('manual', 'why is the list empty: C'),
    ('l12-data-with-behaviour', 'screens[1]'): ('code', PY12 + 'print(shel.value(27.00))\n'),
    ('l12-data-with-behaviour', 'screens[3]'): ('manual', 'default repr: C'),
    ('l12-data-with-behaviour', 'quiz[1]'): ('pre', PY12),
    ('review-3', 'items[1]'): ('pre', CSVTEXT),
    ('review-3', 'items[3]'): ('pre', "rows = [{'close': c} for c in ('101.20', '99.80', '100.40', '98.75', '102.50')]\n"),
    ('review-3', 'items[4]'): ('manual', 'function return: C'),
    ('homework-3', 'items[4]'): ('manual', 'default repr in a list: C'),
    ('homework-1', 'items[8]'): ('manual', 'which comprehension: C'),
}
n_predict = 0
unhandled = []
for name in LESSONS + SETS:
    for path, n in nodes(name):
        w = n.get('widget') or {}
        prose = n.get('prose', '')
        bl = blocks(prose)
        if not bl or w.get('kind') not in ('choice', 'numeric'):
            continue
        ov = OVERRIDE.get((name, path))
        if ov and ov[0] == 'manual':
            continue
        code = '\n'.join(bl)
        if ov and ov[0] == 'pre':
            code = ov[1] + code
        if ov and ov[0] == 'code':
            code = ov[1]
        out, exc = run_block(code)
        n_predict += 1
        if w['kind'] == 'numeric':
            try:
                val = float(out.strip())
            except ValueError:
                unhandled.append((name, path, repr(out), repr(exc)))
                continue
            tol = (w.get('tol') or {}).get('abs', 0)
            ok(f'B {name} {path}: numeric key {w["answer"]} equals the printed {val}', abs(val - w['answer']) <= tol + 1e-12)
            for wr in w.get('wrong', []):
                ok(f'B {name} {path}: slip {wr["id"]}={wr["value"]} differs from the output', abs(val - wr['value']) > tol + 1e-9)
            continue
        right = [o for o in w['options'] if o.get('correct')]
        ok(f'B {name} {path}: exactly one keyed option', len(right) == 1)
        hit = describes(right[0]['text'], out, exc)
        if not hit:
            unhandled.append((name, path, repr(out), repr(exc)))
        ok(f'B {name} {path}: keyed option "{right[0]["id"]}" is what the code does', hit, f'out={out!r} exc={exc!r}')
        for o in w['options']:
            if not o.get('correct'):
                ok(f'B {name} {path}: option "{o["id"]}" is really wrong', not describes(o['text'], out, exc), o['text'])

# ---------------------------------------------------------------- C. hand-written claim checks
F = None  # shorthand: F=n marks a finding


def T(name, path):
    return str(text_of(name, path))


# ---- l1 floats
s = 0.1 + 0.2
chk('C l1 s0: 0.1 + 0.2 == 0.3 is False and the sum prints 0.30000000000000004', lambda: (s != 0.3) and repr(s) == '0.30000000000000004')
chk('C l1 s0 explain: gap about 6e-17', lambda: 5e-17 < s - 0.3 < 6.5e-17)
chk('C l1 s0 explain: "0.3 is stored as 0.29999999999999998" is 0.3 to 17 places',
    lambda: '%.17f' % 0.3 == re.search(r'0\.3 as (0\.2\d+)', T('l1-why-not-0-3', 'screens[0].explain.text')).group(1), finding=2)
chk('C l1 s1: 0.1 in binary starts 0.000110011', lambda: bin(int(Decimal(0.1) * 2 ** 12))[2:].zfill(12)[:9] == '000110011')
chk('C l1 s1: gap at 8 digits is 0.00000000333', lambda: '%.11f' % (1 / 3 - 0.33333333) == '0.00000000333')
chk('C l1 s1 explain: a float keeps 53 binary digits', lambda: sys.float_info.mant_dig == 53)
chk('C l1 s2 table: stored values to 20 places',
    lambda: ['%.20f' % x for x in (0.1, 0.2, 0.3)] == ['0.10000000000000000555', '0.20000000000000001110', '0.29999999999999998890'])
chk('C l1 s2 prose: "about 17 significant digits" (53 bits is 15.95 digits; 17 digits always round-trip; stored 0.1 agrees with 0.1 to 17)',
    lambda: abs(53 * math.log10(2) - 16) < 0.1 and float(repr(0.1)) == 0.1 and float('%.17g' % 0.1) == 0.1 and '%.17g' % 0.1 == '0.10000000000000001')
chk('C l1 s2: stored 0.1 and 0.2 are high, stored 0.3 is low', lambda: Decimal(0.1) > Decimal('0.1') and Decimal(0.2) > Decimal('0.2') and Decimal(0.3) < Decimal('0.3'))
chk('C l1 s3: the six checks', lambda: [0.5 + 0.25 == 0.75, 0.1 + 0.2 == 0.3, 0.25 * 4 == 1.0, 0.1 * 3 == 0.3, 0.7 + 0.1 == 0.8, 1.5 + 2.5 == 4.0] == [True, False, True, False, False, True])
chk('C l1 s3 byKey: 0.1 * 3 and 0.7 + 0.1', lambda: repr(0.1 * 3) == '0.30000000000000004' and repr(0.7 + 0.1) == '0.7999999999999999')
chk('C l1 s4: the two isclose lines print True, False', lambda: math.isclose(0.1 + 0.2, 0.3) and not math.isclose(0.1 + 0.2 - 0.3, 0.0))
chk('C l1 s4: allowed gap next to 0.3 is about 3e-10', lambda: abs(1e-9 * max(abs(s), 0.3) - 3e-10) < 1e-11)
chk('C l1 s4 hints[1]: "on the second line the larger number is 0.0"',
    lambda: max(abs(0.1 + 0.2 - 0.3), abs(0.0)) == 0.0, finding=1)
chk('C l1 s4 explain.canvas r1c2: the allowed gap on line 2 is 0',
    lambda: 1e-9 * max(abs(0.1 + 0.2 - 0.3), abs(0.0)) == 0.0, finding=1)
chk('C l1 s4 explain: abs_tol fixes it', lambda: math.isclose(0.1 + 0.2 - 0.3, 0.0, abs_tol=1e-9))
chk('C l1 s8 o1: isclose(pnl, 0.0) acts like ==', lambda: all(math.isclose(x, 0.0) == (x == 0.0) for x in (0.0, 5e-17, -1e-300, 1e-9, 0.4)))
chk('C l1 s5: a - b without abs passes test 3 wrongly', lambda: (10.00 - 10.01 < 0.005) is True)
tot = 0.0
run = []
for _ in range(10):
    tot += 0.1
    run.append(tot)
chk('C l1 s6: ten deposits end at 0.9999999999999999', lambda: repr(tot) == '0.9999999999999999' and tot != 1.0)
chk('C l1 s6 canvas: running totals', lambda: [repr(x) for x in run] == ['0.1', '0.2', '0.30000000000000004', '0.4', '0.5', '0.6', '0.7', '0.7999999999999999', '0.8999999999999999', '0.9999999999999999'])
chk('C l1 s7: 0.29 * 100 and 19.99 * 100', lambda: repr(0.29 * 100) == '28.999999999999996' and repr(19.99 * 100) == '1998.9999999999998' and int(0.29 * 100) == 28 and round(0.29 * 100) == 29)
chk('C l1 s7 byKey.test-2: int gives 1999, unrounded sum gives 1999.9999999999998', lambda: int(19.99 * 100) + int(0.01 * 100) == 1999 and repr(19.99 * 100 + 0.01 * 100) == '1999.9999999999998')
chk('C l1 s7: round(x) returns an int', lambda: type(round(28.999999999999996)) is int)
chk('C l1 s8 o3: round(-0.40) == 0', lambda: round(-0.40) == 0)
chk('C l1 s9: 550.00 / 1.10', lambda: repr(550.00 / 1.10) == '499.99999999999994' and int(550.00 / 1.10) == 499 and 7 // 2 == 3 and 55000 // 110 == 500)
chk('C l1 s9 byKey.test-3: 100 / 3', lambda: repr(100.00 / 3.00) == '33.333333333333336')
chk('C l1 q0: round(2.675, 2) and its stored value', lambda: round(2.675, 2) == 2.67 and str(Decimal(2.675)) == '2.67499999999999982236431605997495353221893310546875' and round(2.675) == 3)
chk('C l1 q1: 6 / 3', lambda: repr(6 / 3) == '2.0')
chk('C l1 q2: 0.57 * 100', lambda: repr(0.57 * 100) == '56.99999999999999' and int(0.57 * 100) == 56 and round(0.57 * 100) == 57)
chk('C l1 q3: 0.2 + 0.4', lambda: repr(0.2 + 0.4) == '0.6000000000000001' and 0.5 + 0.25 == 0.75 and 0.1 + 0.3 == 0.4)

# ---- l2 slicing
c6 = [101.20, 102.50, 99.80, 100.40, 103.10, 104.00]
chk('C l2 s0: closes[1:4]', lambda: c6[1:4] == [102.5, 99.8, 100.4])
chk('C l2 s1: negative index', lambda: all(c6[-k] == c6[6 - k] for k in range(1, 7)) and c6[-2] == 103.1)
chk('C l2 s2: closes[-3:] and the distractors', lambda: c6[-3:] == [100.4, 103.1, 104.0] and c6[-3:-1] == [100.4, 103.1] and repr(100.40) == '100.4')
chk('C l2 s3: closes[1::2], closes[0:6:2], closes[1:2]', lambda: c6[1::2] == [102.5, 100.4, 104.0] and c6[0:6:2] == [101.2, 99.8, 103.1] and c6[1:2] == [102.5])
chk('C l2 s4: prices[-0:] is the whole list', lambda: c6[-0:] == c6 and c6[len(c6) - 0:] == [])
chk('C l2 s5 byKey: a slice from 0 gives [101.2, 104.0]', lambda: (c6 + [102.7, 101.9, 103.6, 105.2])[0::5] == [101.2, 104.0] and [1, 2, 3][4::5] == [])
chk('C l2 s6/s7: assignment never copies; a slice of a list is a new list', lambda: (lambda a: (a is a, a[:] is not a, a[:] == a))([1.0, 2.0]) == (True, True, True))
chk('C l2 s7 prose: a[:] is a "full" copy (inner lists are shared: the copy is one level deep)',
    lambda: (lambda a: a[:][0] is not a[0])([[1.0], [2.0]]), finding=3)
chk('C l2 s9: len(range(10)[2:7]) == 5', lambda: len(list(range(10))[2:7]) == 5)
chk('C l2 s10: means', lambda: math.isclose(sum((c6 + [102.7, 101.9, 103.6, 105.2])[-5:]), 517.4) and math.isclose(sum((c6 + [102.7, 101.9, 103.6, 105.2])[:5]) / 5, 101.40))
chk('C l2 q0/q1: reversed copy; slice past the end; index past the end', lambda: [1, 2, 3][::-1] == [3, 2, 1] and [1, 2, 3, 4][2:10] == [3, 4] and raises(IndexError, lambda: [1, 2, 3, 4][10]) and [1, 2, 3][-1:] == [3])
chk('C l2 q3: closes[1:20:3] has 7 items', lambda: list(range(20))[1:20:3] == [1, 4, 7, 10, 13, 16, 19])

# ---- l3 tuples and unpacking
chk('C l3 s2: too many values raises ValueError; starred name collects a list', lambda: raises(ValueError, lambda: exec('a, b = ("VOD", 72.5, 100)')) and (lambda t: exec('ticker, *rest = t', {'t': t}) or True)(("VOD", 72.5, 100)))


def _star():
    ns = {}
    exec('ticker, *rest = ("VOD", 72.50, 100)\nt, p, _ = ("VOD", 72.50, 100)', ns)
    return ns['rest'] == [72.5, 100] and ns['p'] == 72.5


chk('C l3 s2 o2/explain: rest is the list [72.5, 100]; _ takes the spare field', _star)


def _tuple_assign():
    t = ("VOD", 72.50, 100)
    try:
        t[1] = 72.55
    except TypeError as e:
        return str(e) == "'tuple' object does not support item assignment"
    return False


chk('C l3 s3: tuple item assignment raises the stated TypeError', _tuple_assign)
chk('C l3 s5: zip stops at the shorter list', lambda: list(zip(["Mon", "Tue", "Wed"], [101.20, 99.80])) == [("Mon", 101.2), ("Tue", 99.8)])
chk('C l3 s5 o2.why: "zip never complains about lengths" (zip(..., strict=True) raises ValueError, Python 3.10 on)',
    lambda: not raises(ValueError, lambda: list(zip([1, 2, 3], [1, 2], strict=True))), finding=4)
chk('C l3 s6 byKey: dividing by the later close gives about 0.0476', lambda: abs(5 / 105 - 0.0476) < 1e-4)
chk('C l3 s7: split gives strings; str * str is a TypeError; int ignores the newline', lambda: "VOD,72.50,100\n".split(",") == ['VOD', '72.50', '100\n'] and raises(TypeError, lambda: '72.50' * '100\n') and float('72.50') * int('100\n') == 7250.0 and '72.50' + '100' == '72.50100')
chk('C l3 s8: join needs strings; f-string :.2f', lambda: raises(TypeError, lambda: ",".join(["VOD", 72.5])) and f"{72.5:.2f}" == '72.50' and ",".join("a,b".split(",")) == "a,b")
chk('C l3 s9: the three wrong lines', lambda: [p for t, p in enumerate([("VOD", 72.5), ("BP", 4.8)])] == [("VOD", 72.5), ("BP", 4.8)] and raises(ValueError, lambda: exec('for a, b, c in [("VOD", 72.5)]: pass')))
chk('C l3 s10: float and int ignore surrounding spaces; strip trims newlines', lambda: float(' 4.85 ') == 4.85 and int(' 1000') == 1000 and ' vod\n'.strip().upper() == 'VOD')

# ---- l4 comprehensions, sorting
chk('C l4 s4: capitals sort before lower case', lambda: all(ord(a) < ord(b) for a in 'AZ' for b in 'az') and sorted(["VOD", "bp", "AZN"], key=str.lower) == ['AZN', 'bp', 'VOD'])
chk('C l4 s6 byKey: sorted by value gives [0.021, 0.012]; sizes give [0.034, 0.021]', lambda: sorted([0.012, -0.034, 0.005, -0.008, 0.021], reverse=True)[:2] == [0.021, 0.012] and sorted([abs(x) for x in [0.012, -0.034, 0.005, -0.008, 0.021]], reverse=True)[:2] == [0.034, 0.021])
chk('C l4 s7 explain: max with a key returns the Monday tuple', lambda: max([("Mon", 0.021), ("Tue", -0.034), ("Wed", 0.012)], key=lambda d: d[1]) == ("Mon", 0.021))
chk('C l4 s10 byKey: max without a key picks 2026-10-15', lambda: max([("2026-10-12", 0.021), ("2026-10-13", -0.034), ("2026-10-14", 0.012), ("2026-10-15", -0.008)])[0] == '2026-10-15')
chk('C l4 q0 o1: [p > 100 for p in closes]', lambda: [p > 100 for p in [101.20, 99.80, 100.40]] == [True, False, True])

# ---- l5 dictionaries
chk('C l5 s5 explain: [] raises KeyError("TSCO"); get returns None or the default', lambda: raises(KeyError, lambda: {"VOD": 0.72}["TSCO"]) and {"VOD": 0.72}.get("TSCO") is None and {"VOD": 0.72}.get("TSCO", 0.0) == 0.0)
chk('C l5 s6 explain: get never adds the key', lambda: (lambda d: (d.get("CBOE", 2.0), "CBOE" in d))({"LSE": 1.5}) == (2.0, False))
chk('C l5 s3: insertion order is kept and a replaced value keeps its place (language guarantee since 3.7)', lambda: (lambda d: (d.update(VOD=0.74), list(d))[1])({"VOD": 0.72, "BP": 4.85, "AZN": 118.5}) == ['VOD', 'BP', 'AZN'] and sys.version_info >= (3, 7))
chk('C l5 s3 explain: sorted(prices) gives alphabetical keys', lambda: sorted({"VOD": 1, "BP": 2, "AZN": 3}) == ['AZN', 'BP', 'VOD'])
chk('C l5 s7 byKey: [-1] on an empty list raises IndexError', lambda: raises(IndexError, lambda: [][-1]))
chk('C l5 s9: fees', lambda: math.isclose(20000 * 0.0010, 20.0) and math.isclose(4850 * 0.0015, 7.275) and math.isclose(1000 * 0.0015, 1.5))
chk('C l5 s2 explain: short 200 BP at 4.85 is -970', lambda: math.isclose(-200 * 4.85, -970.0))

# ---- l6 sets and counting
chk('C l6 s2 explain: a set has no positions', lambda: raises(TypeError, lambda: (lambda st: st[0])({"BP"})))


class Probe(str):
    """A string that counts its equality tests."""
    count = 0

    def __eq__(self, other):
        Probe.count += 1
        return str.__eq__(self, other)

    __hash__ = str.__hash__


def _comparisons():
    banned = [Probe('T%04d' % i) for i in range(5000)]
    Probe.count = 0
    'ZZZ' in banned
    in_list = Probe.count
    bs = set(banned)
    Probe.count = 0
    'ZZZ' in bs
    return in_list == 5000 and Probe.count <= 2


chk('C l6 s4: a miss costs 5,000 comparisons in a list and about 1 (here 0 to 2) in a set', _comparisons)


class Clash:
    """Every instance hashes alike: the worst case for a set."""
    count = 0

    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 1

    def __eq__(self, other):
        Clash.count += 1
        return self.v == other.v


def _worst_case():
    sset = {Clash(i) for i in range(500)}
    Clash.count = 0
    Clash(-1) in sset
    return Clash.count <= 2


chk('C l6 summary.ideas[0]: "x in s takes about one step however big s is" (average case; with clashing hashes a miss here costs 500 comparisons)',
    _worst_case, finding=5)
chk('C l6 s4 explain: a million orders: five billion against about a million', lambda: 10 ** 6 * 5000 == 5 * 10 ** 9)
chk('C l6 s7 feedback: set() is the way to write an empty set; there is no empty-set literal', lambda: type(eval('{}')) is dict and set() == set([]))
chk('C l6 s7: {} is a dict', lambda: type({}) is dict and type(set()) is set and type({"BP", "VOD"}) is set)


def _del_while_looping(book):
    try:
        for t in book:
            if book[t] == 0:
                del book[t]
    except RuntimeError:
        return 'RuntimeError'
    return book


chk('C l6 s8 byKey.test-2: deleting BP inside the loop raises RuntimeError in test 2', lambda: _del_while_looping({"BP": 0, "VOD": 1000}) == 'RuntimeError')
chk('C l6 s8 explain: deleting a key while looping over a dictionary is an error wherever the key sits, the last one included',
    lambda: _del_while_looping({"VOD": 1000, "BP": 0}) == 'RuntimeError' and _del_while_looping({"A": 0, "B": 1, "C": 2}) == 'RuntimeError')
chk('C l6 s6: in checks keys; values() searches values', lambda: (300 in {"BP": 300}) is False and 300 in {"BP": 300}.values())
chk('C l6 q3: dict has no add', lambda: raises(AttributeError, lambda: {}.add("BP")))

# ---- l7 arguments
chk('C l7 s2: positional after keyword is a SyntaxError before anything runs', lambda: raises(SyntaxError, lambda: compile('cost(price=2.50, 100)', 'x', 'eval')))


def _cost_calls():
    def cost(price, qty, fee=1.50):
        return price * qty + fee
    return (cost(2.50, qty=100), cost(qty=100, price=2.50), cost(2.50, 100, fee=0.00), cost(2.50, fee=0.00, qty=200)) == (251.5, 251.5, 250.0, 500.0)


chk('C l7 s1/s2: the three legal calls', _cost_calls)


def _doc():
    def high_low(prices):
        """Return (highest, lowest) as a tuple."""
        return max(prices), min(prices)

    def c(x):
        # a comment
        return x
    return high_low.__doc__ == 'Return (highest, lowest) as a tuple.' and c.__doc__ is None


chk('C l7 s5/q3: a docstring is stored as __doc__; a comment is not', _doc)


def _default_once():
    def log_trade(ticker, log=[]):
        log.append(ticker)
        return log
    a = log_trade("BP")
    b = log_trade("VOD")
    return a is b and b == ['BP', 'VOD']


chk('C l7 s6: the default list is made once and shared; a and b are one object', _default_once)
chk('C l7 s9: drawdown examples', lambda: math.isclose(1 - 0.9 * 0.9, 0.19) and math.isclose(sum([0.01, -0.02, 0.03]) / 3, 0.00666666666667, rel_tol=1e-9))


def _unpack_msg():
    try:
        exec('a, b, c = (1, 2)')
    except ValueError as e:
        return str(e) == 'not enough values to unpack (expected 3, got 2)'


chk('C l7 q1 explain: "not enough values to unpack (expected 3, got 2)"', _unpack_msg)

# ---- l8 mutation and aliasing


def _reset_clear():
    def reset(costs):
        costs = []  # noqa: F841

    def clear(costs):
        costs.clear()
    x, y = [1.5, 2.0], [1.5, 2.0]
    reset(x)
    clear(y)
    return x == [1.5, 2.0] and y == []


chk('C l8 s3: assigning to a parameter leaves the caller alone; clear() empties the object', _reset_clear)
chk('C l8 s3 explain: "Methods change objects; = moves names" (str.upper changes nothing; d[k] = v and xs[0] = v change the object)',
    lambda: (lambda xs: (xs.__setitem__(0, 9), xs)[1])([1, 2]) == [1, 2], finding=6)
chk('C l8 s4 o1.why: "a method that changes a list in place returns None" (pop changes the list and returns the item)',
    lambda: [1, 2, 3].pop() is None, finding=6)
chk('C l8 s4: sort returns None, sorted a new list', lambda: (lambda p: (sorted(p), p.sort(), p))([4.91, 4.72]) == ([4.72, 4.91], None, [4.72, 4.91]))
chk('C l8 s1/s9: list(a), dict(d), xs + [1] build new objects', lambda: (lambda a, d: list(a) is not a and dict(d) is not d and (a + [1]) is not a)([5, 8], {"BP": 1}))
chk('C l8 s8 explain: with dict(book) "every change lands on the copy" (a list stored as a value is shared with the original)',
    lambda: (lambda h: (dict(h)["BP"].append(4.91), len(h["BP"]))[1])({"BP": [4.80, 4.85]}) == 2, finding=7)
chk('C l8 s10: book value', lambda: math.isclose(500 * 4.85 + 1000 * 0.72, 3145.0) and math.isclose(-20 * 118.50 + 300 * 4.85, -915.0))

# ---- l9 modules (run with real files in a temporary folder)


def _with_folder(files, body):
    d = tempfile.mkdtemp()
    for fn, src in files.items():
        with open(os.path.join(d, fn), 'w') as fh:
            fh.write(src)
    saved = {k: sys.modules.pop(k) for k in list(sys.modules) if k in ('pricing', 'statistics', 'random', 'math', 'mypkg')}
    sys.path.insert(0, d)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try:
                exec(body, {'__name__': '__main__'})
                exc = None
            except Exception as e:  # noqa: BLE001
                exc = e
    finally:
        sys.path.remove(d)
        for k in ('pricing', 'statistics', 'random', 'math', 'mypkg'):
            sys.modules.pop(k, None)
        sys.modules.update(saved)
    return buf.getvalue(), exc


PRICING = 'import math\n\ndef simple_return(p0, p1):\n    return p1 / p0 - 1\n\ndef log_return(p0, p1):\n    return math.log(p1 / p0)\n'
chk('C l9 s1: main.py prints 0.05', lambda: _with_folder({'pricing.py': PRICING}, 'import pricing\nr = pricing.simple_return(100.00, 105.00)\nprint(round(r, 4))\n') == ('0.05\n', None))
chk('C l9 s4: the import runs the stray print first: 0.05 then 0.0488',
    lambda: _with_folder({'pricing.py': PRICING + 'print(round(simple_return(100.00, 105.00), 4))\n'}, 'import pricing\nprint(round(pricing.log_return(100.00, 105.00), 4))\n') == ('0.05\n0.0488\n', None))
chk('C l9 s4 explain: a block under if __name__ == "__main__" is skipped on import',
    lambda: _with_folder({'pricing.py': PRICING + 'if __name__ == "__main__":\n    print("check")\n'}, 'import pricing\nprint("main")\n') == ('main\n', None))
chk('C l9 s4: a module runs once however often it is imported',
    lambda: _with_folder({'pricing.py': 'print("ran")\n'}, 'import pricing\nimport pricing\n')[0] == 'ran\n')
chk('C l9 s2 explain: log return 0.04879 is below 0.05; never above the simple return', lambda: round(math.log(1.05), 5) == 0.04879 and all(math.log(1 + r) <= r for r in (-0.5, -0.01, 0.0, 0.01, 0.5, 3.0)) and math.log(1.0) == 0.0)
chk('C l9 s2 tests: stated log returns', lambda: math.isclose(math.log(99.80 / 101.20), -0.01393057353594691) and math.isclose(math.log(2), 0.6931471805599453))
chk('C l9 s5: mean of the four closes is 100.975', lambda: repr(statistics.mean([101.20, 102.50, 99.80, 100.40])) == '100.975')
chk('C l9 s6 explain: mean 101.50, sample sd about 1.26, band 98.97 to 104.03; pstdev is narrower',
    lambda: (lambda c: math.isclose(statistics.mean(c), 101.5) and round(statistics.stdev(c), 2) == 1.26 and statistics.pstdev(c) < statistics.stdev(c) and all(98.97 < x < 104.03 for x in c))([101.2, 102.5, 99.8, 100.4, 103.1, 102.0]))


def _shadow_stats():
    out, exc = _with_folder({'statistics.py': 'x = 1\n'}, 'from statistics import mean\n')
    return isinstance(exc, ImportError) and str(exc).startswith("cannot import name 'mean' from 'statistics'")


chk('C l9 s7: a local statistics.py is imported instead and the stated ImportError follows', _shadow_stats)


def _shadow_random():
    out, exc = _with_folder({'random.py': 'x = 1\n'}, 'import random\nrandom.seed(1)\n')
    return isinstance(exc, AttributeError) and "module 'random' has no attribute 'seed'" in str(exc)


chk('C l9 q2: a local random.py gives AttributeError: module random has no attribute seed', _shadow_random)


def _shadow_math():
    out, exc = _with_folder({'math.py': 'x = 1\n'}, 'import math\nprint(math.sqrt(16))\n')
    return exc is not None  # the claim: your math.py is found first and hides the real module


chk('C l9 s7 explain: a file named math.py hides the real module ("the script\'s folder is searched first"); math is built in here and in Pyodide, so it is not hidden',
    _shadow_math, finding=9)


def _import_package():
    d = tempfile.mkdtemp()
    os.mkdir(os.path.join(d, 'mypkg'))
    with open(os.path.join(d, 'mypkg', '__init__.py'), 'w') as fh:
        fh.write('x = 1\n')
    sys.path.insert(0, d)
    try:
        import mypkg  # noqa: F401
        is_folder = os.path.isdir(os.path.dirname(mypkg.__file__)) and not hasattr(sys, '_never')
    finally:
        sys.path.remove(d)
        sys.modules.pop('mypkg', None)
    built_in = not hasattr(sys, '__file__')  # sys itself is a module with no .py file
    return not (is_folder and built_in)


chk('C l9 s0 byKey.q-d-c: "import only loads .py files" (a folder imports as a package; sys and math have no .py file)', _import_package, finding=8)
chk('C l9 s3: dividing two strings raises the stated TypeError', lambda: (lambda: "105" / "100") and raises(TypeError, lambda: "105" / "100"))
random.seed(7)
first = [random.choice([0.99, 1.01]) for _ in range(3)]
chk('C l9 s9 explain: seed 7 gives [1.01, 0.99, 1.01]', lambda: first == [1.01, 0.99, 1.01])


def walk(start, days, seed):
    random.seed(seed)
    prices = [start]
    for _ in range(days):
        prices.append(prices[-1] * random.choice([0.99, 1.01]))
    return prices


w7 = walk(100.00, 20, 7)
chk('C l9 s10 canvas: the seed 7 path to 2 places', lambda: [round(p, 2) for p in w7] == node('l9-splitting-files', 'screens[10].canvas.params.series[0].values'))
chk('C l9 s10 explain: 6 up days in 20, last price 92.22', lambda: sum(b > a for a, b in zip(w7, w7[1:])) == 6 and round(w7[-1], 2) == 92.22 and math.isclose(100 * 1.01 ** 6 * 0.99 ** 14, w7[-1]))


def _global_seed_side_effect():
    random.seed(123)
    random.random()
    expect = random.random()   # the caller's second draw
    random.seed(123)
    random.random()
    walk(100.0, 5, 7)          # a helper called in between
    return random.random() == expect


chk('C l9 s10 solution: calling walk() leaves the caller\'s own random sequence untouched (it reseeds the shared generator)',
    _global_seed_side_effect, finding=10)
chk('C l9 q1/q3: Counter.most_common(1); int * str repeats', lambda: __import__('collections').Counter(["up", "down", "up", "up", "down"]).most_common(1) == [('up', 3)] and 3 * "2.50" == '2.502.502.50')

# ---- l10 csv
TXT = "date,close\n2024-03-11,101.20\n2024-03-12,102.50\n2024-03-13,99.80\n2024-03-14,100.40\n"
rows = list(csv.DictReader(TXT.splitlines()))
chk('C l10 s0/s1: rows[2]["close"] and the type of a row', lambda: rows[2]["close"] == '99.80' and type(rows[0]) is dict and repr(rows[0]) == "{'date': '2024-03-11', 'close': '101.20'}")
chk('C l10 s1 o2: csv.reader gives a list per line', lambda: list(csv.reader(TXT.splitlines()))[1] == ['2024-03-11', '101.20'])
chk('C l10 s3 explain: skipinitialspace=True drops the space, in the header too',
    lambda: list(csv.DictReader("date, close\n2024-03-11, 101.20\n".splitlines(), skipinitialspace=True))[0] == {'date': '2024-03-11', 'close': '101.20'} and list(csv.DictReader("date, close\n1, 2\n".splitlines()))[0] == {'date': '1', ' close': ' 2'})
chk('C l10 s4 explain: max over floats is 102.5', lambda: max(float(r["close"]) for r in rows) == 102.5 and max(r["close"] for r in rows) == '99.80')
chk('C l10 s5: text sort of UK dates; strptime sorts by time', lambda: sorted(["15/03/2024", "02/04/2024", "28/02/2024"]) == ['02/04/2024', '15/03/2024', '28/02/2024'] and sorted(["15/03/2024", "02/04/2024", "28/02/2024"], key=lambda d: datetime.strptime(d, "%d/%m/%Y")) == ['28/02/2024', '15/03/2024', '02/04/2024'])
chk('C l10 s6 explain: text sorting gets the year end wrong too', lambda: sorted(["05/01/2025", "31/12/2024"]) == ["05/01/2025", "31/12/2024"])
chk('C l10 s7: "250" * 1 is still text; int(dict) fails', lambda: '250' * 1 == '250' and raises(TypeError, lambda: int({'qty': '250'})))
chk('C l10 s8 explain: returns from the sorted closes', lambda: [round(b / a - 1, 4) for a, b in zip([100.0, 100.4, 102.0, 101.6, 103.1], [100.4, 102.0, 101.6, 103.1])] == [0.004, 0.0159, -0.0039, 0.0148])
chk('C l10 q0: float(...) * 2 is 202.4', lambda: repr(float('101.20') * 2) == '202.4')
chk('C l10 q2: a wrong format raises ValueError; %Y-%m-%d reads it', lambda: raises(ValueError, lambda: datetime.strptime("2024-03-15", "%d/%m/%Y")) and datetime.strptime("2024-03-15", "%Y-%m-%d").day == 15)

# ---- l11 exceptions
chk('C l11 s0/s2: what float can and cannot read', lambda: all(raises(ValueError, lambda v=v: float(v)) for v in ("n/a", "", "1,234.50", "-")) and float(" 99.80 ") == 99.8 and raises(TypeError, lambda: float(None)))
chk('C l11 s2 prose: "keep what float can read" keeps only prices (float also reads nan, inf and 1e5)',
    lambda: all(raises(ValueError, lambda v=v: float(v)) for v in ("nan", "inf", "-Infinity")), finding=12)


def _zde():
    try:
        101.20 / 0.00
    except ZeroDivisionError as e:
        return str(e)


chk('C l11 s3: float division by zero raises ZeroDivisionError with the stated message (3.12 and 3.13; 3.14 words it "division by zero")',
    lambda: _zde() in ('float division by zero', 'division by zero') and (sys.version_info >= (3, 14) or _zde() == 'float division by zero'))
chk('C l11 s4: printing the exception shows its message', lambda: str(ValueError("qty must be positive")) == 'qty must be positive')
chk('C l11 s5: int reads " 40 ", refuses "abc" and "2.5"', lambda: int(" 40 ") == 40 and raises(ValueError, lambda: int("abc")) and raises(ValueError, lambda: int("2.5")) and int(float("12.5")) == 12 and int(12.5) == 12)


def _bare():
    def clean(raw):
        out = []
        for p in raw:
            try:
                out.append(flaot(p))  # noqa: F821
            except:  # noqa: E722
                pass
        return out
    return clean(["101.20", "102.50", "100.40"]) == [] and raises(NameError, lambda: flaot("1"))  # noqa: F821


chk('C l11 s6: the typo raises NameError each time and the bare except hides it', _bare)
chk('C l11 s8 explain: one piece or three pieces into two names raise ValueError; None.split is an AttributeError',
    lambda: raises(ValueError, lambda: exec('a, b = "HSBA".split(",")')) and raises(ValueError, lambda: exec('a, b = "SHEL,10,20".split(",")')) and raises(AttributeError, lambda: None.split(",")))
chk('C l11 q3: float("£7.25") raises ValueError', lambda: raises(ValueError, lambda: float("£7.25")))

# ---- l12 classes
ns12 = {'__name__': '__main__'}
exec(PY12, ns12)
shel, azn, Position = ns12['shel'], ns12['azn'], ns12['Position']
chk('C l12 s1: values and the distractors', lambda: shel.value(27.00) == 4050.0 and repr(150 * 26.40) == '3960.0' and math.isclose(150 * (27.00 - 26.40), 90.0))
chk('C l12 s2 tests: stated float results', lambda: repr(150 * (27.00 - 26.40)) == '90.00000000000021' and repr(40 * (101.50 - 104.20)) == '-108.00000000000011' and repr(-500 * (1.80 - 1.85)) == '25.00000000000002')
chk('C l12 s3: the default repr names the class and an address', lambda: re.fullmatch(r'<__main__\.Position object at 0x[0-9a-f]+>', repr(shel)) is not None and str(shel) == repr(shel))


class _Both:
    def __str__(self):
        return 'S'

    def __repr__(self):
        return 'R'


class _OnlyRepr:
    def __repr__(self):
        return 'R'


chk('C l12 s4 explain: str() falls back to __repr__ when there is no __str__', lambda: str(_OnlyRepr()) == 'R' and str([_OnlyRepr()]) == '[R]')
chk('C l12 s4 explain: "str() and lists fall back to __repr__" (a list never tries __str__: it uses __repr__ even when __str__ exists)',
    lambda: str([_Both()]) == '[S]', finding=13)
chk('C l12 s4 byKey: a __repr__ that prints and returns None raises TypeError', lambda: raises(TypeError, lambda: repr(type('P', (), {'__repr__': lambda self: None})())))


def _no_self():
    class P:
        def __init__(self, ticker, qty, avg_price):
            ticker = ticker  # noqa: F841
            qty = qty  # noqa: F841
    try:
        P("SHEL", 150, 26.4).qty
    except AttributeError as e:
        return str(e) == "'P' object has no attribute 'qty'"


chk('C l12 s5: a local name stores nothing: the stated AttributeError', _no_self)


def _shared_class_list():
    class Book:
        trades = []

        def add(self, trade):
            self.trades.append(trade)
    mine, yours = Book(), Book()
    mine.add("VOD +100")
    return len(yours.trades) == 1 and mine.trades is Book.trades


chk('C l12 s6: a list in the class body is shared', _shared_class_list)
chk('C l12 s7: obj.method(x) is Class.method(obj, x)', lambda: azn.value(101.50) == Position.value(azn, 101.50) and raises(TypeError, lambda: Position.value(101.50)))
chk('C l12 s8 explain: cash flows', lambda: math.isclose(1000 * 0.72, 720) and math.isclose(400 * 0.75, 300) and round(-(40 * 104.20 - 500 * 1.85 + 10 * 101.50), 2) == -4258.0)


def _too_many():
    class P:
        def __init__(self, qty):
            self.qty = qty

        def value(price):
            return self.qty * price  # noqa: F821
    try:
        P(10).value(5.00)
    except TypeError as e:
        return 'takes 1 positional argument but 2 were given' in str(e)


chk('C l12 q0: a method without self gets one argument too many', _too_many)

# ---- review-1
chk('C review-1 i0: 1.1 + 2.2', lambda: repr(1.1 + 2.2) == '3.3000000000000003')
chk('C review-1 i0 o2.why: names the quantity that the line computes (it says "product"; 1.1 + 2.2 is a sum)',
    lambda: 'product' not in T('review-1', 'items[0].widget.options[2].why'), finding=14)
chk('C review-1 i4: -4.35 * 100', lambda: repr(-4.35 * 100) == '-434.99999999999994' and int(-4.35 * 100) == -434 and round(-4.35 * 100) == -435 and math.floor(-4.35 * 100) == -435)
chk('C review-1 i6 o2.why: "only string times string fails" (string times float fails too)',
    lambda: not raises(TypeError, lambda: '4.85' * 2.0), finding=15)

# ---- review-2, review-3
chk('C review-2 i7: list() as a default is still made once; a tuple has no append', lambda: (lambda f: f(1) is f(2))(eval('lambda p, history=list(): history')) and raises(AttributeError, lambda: ().append(1)))
chk('C review-3 i1: sum over strings raises the stated TypeError', lambda: (lambda: sum(["101.20"]))() if False else raises(TypeError, lambda: sum(["101.20", "99.80"])))
chk('C review-3 i3 explain: three closes are above 100 as numbers', lambda: sum(1 for c in ('101.20', '99.80', '100.40', '98.75', '102.50') if float(c) > 100) == 3)


def _swallow():
    def closes(rows_):
        out = []
        for row in rows_:
            try:
                out.append(float(row["Close"]))
            except:  # noqa: E722
                pass
        return out
    return closes(rows) == []


chk('C review-3 i4: the bare except hides the KeyError and returns []', _swallow)
chk('C review-3 i5 explain: the five closes sum to 507.00', lambda: math.isclose(101.20 + 102.50 + 99.80 + 100.40 + 103.10, 507.0))
chk('C review-3 i6: a list as a key raises TypeError', lambda: raises(TypeError, lambda: {"VOD": 0.72}[["VOD"]]))
chk('C review-3 i8 explain: 3975 over 150 is 26.50', lambda: 100 * 26.00 + 50 * 27.50 == 3975 and 3975 / 150 == 26.5)

# ---- homework-1
chk('C hw1 i0: ties go to the even neighbour', lambda: (round(2.5), round(3.5), round(0.5), round(1.5)) == (2, 4, 0, 2) and type(round(2.5)) is int)
chk('C hw1 i1: closes[3:-2] of 20 has 15 items', lambda: len(list(range(20))[3:-2]) == 15 and len(list(range(20))[3:]) == 17)
chk('C hw1 i2 explain: a comprehension builds separate levels', lambda: (lambda b: (b[0].__setitem__(0, 99.5), b)[1])([[0.0, 0.0] for _ in range(3)]) == [[99.5, 0.0], [0.0, 0.0], [0.0, 0.0]])
chk('C hw1 i6: sorted is stable', lambda: sorted([("BP", 4.85), ("VOD", 4.85), ("AZN", 1.20)], key=lambda q: q[1]) == [("AZN", 1.20), ("BP", 4.85), ("VOD", 4.85)])
chk('C hw1 i7 prompt: the script prints "mismatch: 0.30 vs 0.30"', lambda: sum([0.10, 0.20]) != 0.30 and f"mismatch: {sum([0.10, 0.20]):.2f} vs {0.30:.2f}" == 'mismatch: 0.30 vs 0.30')
chk('C hw1 i7 model: both fixes work', lambda: abs(sum([0.10, 0.20]) - 0.30) < 0.005 and sum(round(f * 100) for f in [0.10, 0.20]) == round(0.30 * 100) and math.isclose(0.1 + 0.2 - 0.3, 0.0, abs_tol=0.005))
chk('C hw1 i7 model: "0.30 is stored as 0.29999999999999998" is 0.30 to 17 places', lambda: ('%.17f' % 0.30) in T('homework-1', 'items[7].model'), finding=16)
chk('C hw1 i7 model: isclose(0.1 + 0.2 - 0.3, 0.0) is False "because one billionth of 0.0 is 0" (the larger number is the drift, not 0.0)',
    lambda: max(abs(0.1 + 0.2 - 0.3), 0.0) == 0.0, finding=16)
chk('C hw1 i8 o1: an if before the for needs an else', lambda: raises(SyntaxError, lambda: compile('[t if p * q > 1000 for t, p, q in trades]', 'x', 'eval')))

# ---- homework-2
chk('C hw2 i2: P&L sums', lambda: math.isclose(500 * 0.05 + (-200) * (-0.05), 35.0) and math.isclose(40 * (26.0 - 27.3) - 40 * (26.0 - 27.5), 8.0))
chk('C hw2 i3 byKey.test-1: names the call test 1 makes',
    lambda: node('homework-2', 'items[3].widget.tests[0].call').replace('commission', '').strip('()') in T('homework-2', 'items[3].feedback.byKey.test-1'), finding=17)
chk('C hw2 i3 byKey.test-3: 0.0012 x 800 is 0.96', lambda: math.isclose(0.0012 * 800, 0.96))


def _model_h5():
    def add_trade(ticker, qty, book={}):
        book[ticker] = book[ticker] + qty
        return book
    a1 = raises(KeyError, lambda: add_trade("BP", 100))

    def add2(ticker, qty, book={}):
        book[ticker] = book.get(ticker, 0) + qty
        return book
    a = add2("BP", 100)
    add2("VOD", 50)
    msg = None
    try:
        for _t in [1].sort():
            pass
    except TypeError as e:
        msg = str(e)
    return a1 and a == {'BP': 100, 'VOD': 50} and msg == "'NoneType' object is not iterable" and (4.85 in {"BP": 4.85}) is False


chk('C hw2 i5 model: KeyError on the first call; the shared default; None is not iterable; a price is not a key', _model_h5)


def book_weights(book, prices, cash=0.0):
    total = cash
    for ticker, qty in book.items():
        if ticker not in prices:
            return None
        total = total + qty * prices[ticker]
    if total == 0:
        return None
    return {t: q * prices[t] / total for t, q in book.items()}


chk('C hw2 i8 solution: `total == 0` returns None for a hedged book whose legs are 0.3 against 0.1 + 0.2 (weights of 1e16 come back)',
    lambda: book_weights({"A": 1, "B": -1, "C": -1}, {"A": 0.3, "B": 0.1, "C": 0.2}) is None, finding=18)
chk('C hw2 i8: stated weights', lambda: math.isclose(750 / 4000, 0.1875) and math.isclose(6 / 14, 0.42857142857142855) and 6 // 14 == 0)

# ---- homework-3
chk('C hw3 i0: log returns sum to ln(1.031) = 0.030529', lambda: round(math.log(103.10 / 100.00), 6) == 0.030529 and math.isclose(sum(round(math.log(b / a), 6) for a, b in zip([100.0, 101.2, 99.8, 100.4], [101.2, 99.8, 100.4, 103.1])), 0.030529, abs_tol=2e-6))
chk('C hw3 i0 explain: +100% then -50% cancel as log returns, not as simple returns', lambda: math.isclose(math.log(2) + math.log(0.5), 0.0, abs_tol=1e-15) and 1.0 + (-0.5) != 0)
chk('C hw3 i1: the format reads the stamp; %y and %Y-%d-%m do not', lambda: datetime.strptime("2024-03-15 16:30", "%Y-%m-%d %H:%M").minute == 30 and raises(ValueError, lambda: datetime.strptime("2024-03-15 16:30", "%y-%m-%d %H:%M")) and raises(ValueError, lambda: datetime.strptime("2024-03-15 16:30", "%Y-%d-%m %H:%M")))
exact = sum(comb(20, k) for k in range(11, 21)) / 2 ** 20
chk('C hw3 i5: exact chance 0.4119; 10 ups leave 99.90; 11 ups end above 100', lambda: round(exact, 4) == 0.4119 and round(100 * 0.9999 ** 10, 2) == 99.90 and 100 * 1.01 ** 11 * 0.99 ** 9 > 100 > 100 * 1.01 ** 10 * 0.99 ** 10)


def share_above(paths, days, seed):
    random.seed(seed)
    above = 0
    for _ in range(paths):
        price = 100.0
        for _ in range(days):
            price *= random.choice([0.99, 1.01])
        if price > 100.0:
            above += 1
    return above / paths


big = share_above(200000, 20, 11)
chk(f'C hw3 i5 explain (Monte Carlo, 200,000 paths): the share converges to 0.4119 (got {big:.4f}; 3 sd is 0.0033)', lambda: abs(big - exact) < 0.0033)
chk('C hw3 i7 model: the stated TypeError for "150" * 27.00 and the text max', lambda: raises(TypeError, lambda: '150' * 27.00) and max('99.80', '104.20') == '99.80')


def _str_times_float_msg():
    try:
        '150' * 27.00
    except TypeError as e:
        return str(e) == "can't multiply sequence by non-int of type 'float'"


chk('C hw3 i7 model: message "can\'t multiply sequence by non-int of type \'float\'"', _str_times_float_msg)
chk('C hw3 i8 byKey.test-2: three deposits of 0.70 added with + fall just short', lambda: repr(0.7 + 0.7 + 0.7) == '2.0999999999999996')


class FloatAccount:
    """The method the task rules out: floats, no pence."""

    def __init__(self, opening=0.0):
        self.opening = opening
        self.moves = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError
        self.moves.append(amount)

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance():
            raise ValueError
        self.moves.append(-amount)

    def balance(self):
        return self.opening + sum(self.moves)

    def history(self):
        return list(self.moves)


def _float_account_passes():
    w = node('homework-3', 'items[8].widget')
    src = 'import builtins\n'
    import inspect
    try:
        src = inspect.getsource(FloatAccount).replace('FloatAccount', 'Account')
    except (OSError, TypeError):
        return None
    return all(run_tests(src, w, w['tests']))


fa = _float_account_passes()
if fa is not None:
    ok('C hw3 i8 tests: a float-only Account (balance = opening + sum(moves)) fails the hidden tests, as the task intends', not fa)


# ---- items the generic block B cannot run (checked by hand here)


def _l3q2():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        for day, d in enumerate(["Mon", "Tue"], start=1):
            print(day, d)
    return buf.getvalue().splitlines()[-1] == '2 Tue'


chk('C l3 q2: the last line is "2 Tue"', _l3q2)
chk('C l5 s8: storing under an existing key leaves len(d) at 1', lambda: (lambda d: (d.__setitem__("BP", 4.90), len(d))[1])({"BP": 4.85}) == 1)
chk('C l6 s7: only set() makes an empty set among the four options', lambda: [type(x) for x in (set(), {}, [], ())] == [set, dict, list, tuple])


def _l7s2():
    def cost(price, qty, fee=1.50):
        return price * qty + fee
    okc = [cost(2.50, qty=100), cost(qty=100, price=2.50), cost(2.50, 100, fee=0.00)]
    return okc == [251.5, 251.5, 250.0] and raises(SyntaxError, lambda: compile('cost(price=2.50, 100)', 'x', 'eval'))


chk('C l7 s2: exactly one of the four calls is an error', _l7s2)


def _l8s9():
    res = []
    for stmt in ('ys = xs + [4.95]', 'xs.append(4.95)', 'ys = xs; ys.append(4.95)', 'xs.sort()'):
        ns = {'xs': [4.91, 4.72]}
        exec(stmt, ns)
        res.append(ns['xs'] == [4.91, 4.72])
    return res == [True, False, False, False]


chk('C l8 s9: only xs + [4.95] leaves xs unchanged', _l8s9)
chk('C l9 s5/q0: from-import creates only the named name; import math does not create sqrt',
    lambda: raises(NameError, lambda: exec('from statistics import mean\nstatistics.mean([1])', {})) and raises(NameError, lambda: exec('import math\nsqrt(16)', {})))
chk('C l12 s3 / hw3 i4: print(p) uses __str__; a list uses the default __repr__',
    lambda: (lambda P: (str(P()), re.fullmatch(r'\[<.*\.P object at 0x[0-9a-f]+>\]', str([P()])) is not None))(type('P', (), {'__str__': lambda self: 'VOD x100'})) == ('VOD x100', True))
chk('C hw1 i8: the keyed comprehension equals the loop; the others differ',
    lambda: (lambda trades: [t for t, p, q in trades if p * q > 1000] == ['VOD', 'AZN'] and [(t, p, q) for t, p, q in trades if p * q > 1000] != ['VOD', 'AZN'])([("VOD", 72.5, 100), ("BP", 4.85, 100), ("AZN", 120.0, 10)]))
chk('C l9 s9 explain: "anyone who runs your simulation with seed 7 gets your numbers" holds on this Python (the library promises it only for random.random(); see finding 11)',
    lambda: first == [1.01, 0.99, 1.01])

# ---------------------------------------------------------------- report
print(f'python {sys.version.split()[0]}; code widgets {n_widgets}; predict items run {n_predict}; checks passed {passed}')
for name, path, out, exc in unhandled:
    print(f'  UNMATCHED {name} {path}: out={out} exc={exc}')
for n, label, detail in sorted(findings):
    print(f'FINDING {n}: {label}' + (f' [{detail}]' if detail and detail != 'claim does not hold' else ''))
for label, detail in failed:
    print(f'FAIL: {label} [{detail}]')
print(f'{len(findings)} checks fail by design (findings {sorted(set(n for n, _, _ in findings))}); {len(failed)} unexpected failures')
sys.exit(1 if (failed or findings) else 0)
