#!/usr/bin/env python3
"""Blind concept audit, first-python levels 1 to 3, round 1 (docs/reviews/audit-first-python-1-3.md).

Runs every code-behaviour claim of the course against the interpreter and recomputes every slip value.
  A  every prose snippet with a graded key: the output or error, the key, and that no wrong option is the true output
  A2 every graded key with no snippet in its prose (canvas code, taps, boxes, concept choices)
  B  every numeric slip value and named wrong option, recomputed from the mistake its feedback names
  C  every error message the content quotes
  D  every traceback the content prints (exact text on Python 3.12, the page's version; File lines and last line elsewhere)
  E  stated rules (always / never / every) on a grid of cases
  F  stated numbers (compounding, returns, drawdowns)
A FAIL is content that is false as stated: it stays failing and is a finding. A NOTE is a rule that is true only
under a condition the content does not state (verdict imprecise): it is printed and does not fail the script.
Exit 0 only when no check fails. Runs in CPython and, through first-python-L1-3-test-line-sweep.mjs --concepts,
inside the page's Pyodide 0.27.7 (Python 3.12, wasm32). No third-party imports.
"""
import builtins, contextlib, glob, io, json, linecache, math, os, re, sys, tempfile, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('ZQ_FP_CONTENT') or os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'first-python')
DOC = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, '*.json'))}
STRICT_TB = sys.version_info[:2] == (3, 12)
fails, notes, count = [], [], [0]

def check(ok, where, what):
    count[0] += 1
    if not ok:
        fails.append(f'FAIL {where}: {what}')

def note(cond_holds, where, what):
    """cond_holds is the unstated condition failing to hold in general: recorded, never fatal."""
    count[0] += 1
    if cond_holds:
        notes.append(f'NOTE {where}: {what}')

def item(file, idx):
    d = DOC[file]
    if isinstance(idx, int):
        return (d.get('screens') or d.get('items'))[idx]
    return next(q for q in d['quiz'] if q['id'] == idx)

def text_of(it):
    return json.dumps(it, ensure_ascii=False)

CLOSES = '101.20\n102.50\n99.80\n'
PRICES = 'Day,Close\nMon,101.20\nTue,102.50\nWed,99.80\nThu,100.40\nFri,101.10\n'

def run(code, inp=None, files=None, filename='main.py'):
    """Returns (stdout, 'Type: message' or None, traceback text or None, files left behind)."""
    d = tempfile.mkdtemp(); cwd = os.getcwd(); os.chdir(d)
    for k, v in ({'closes.txt': CLOSES, 'prices.csv': PRICES} if files is None else files).items():
        with open(k, 'w') as f:
            f.write(v)
    buf, err, tb, old = io.StringIO(), None, None, builtins.input
    builtins.input = lambda prompt='': inp
    linecache.cache[filename] = (len(code), None, code.splitlines(True), filename)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, filename, 'exec'), {'__name__': '__main__'})
    except SyntaxError as e:
        err = f'SyntaxError: {e.msg}'
    except Exception as e:
        err = f'{type(e).__name__}: {e}'
        tb = ''.join(traceback.format_exception(type(e), e, e.__traceback__.tb_next)).rstrip('\n')
    finally:
        builtins.input = old
        left = {}
        for k in os.listdir('.'):
            with open(k) as f:
                left[k] = f.read()
        os.chdir(cwd)
    return buf.getvalue(), err, tb, left

def snippet(it):
    return re.findall(r'```python\n(.*?)```', it.get('prose', ''), re.S)[-1]

def norm(s):
    return s.replace('`', '').rstrip()

def key_of(it):
    w = it['widget']
    if w['kind'] == 'choice':
        return norm(next(o['text'] for o in w['options'] if o.get('correct')))
    return w['answer']

# ---------------------------------------------------------------- A: snippets against keys
# file, index -> (expected stdout, expected error type or None, relation of the key to the run)
OUT, LINES, ERR, SAYS = 'key is the output', 'key is the number of printed lines', 'key names the error', 'key describes the run'
A = [
 ('l1-calculator', 0, '14\n', None, OUT), ('l1-calculator', 4, '3\n', None, OUT), ('l1-calculator', 5, '18\n', None, OUT),
 ('l1-calculator', 6, '17.0\n', None, OUT), ('l1-calculator', 'q-precedence', '11\n', None, OUT),
 ('l1-calculator', 'q-type', "<class 'float'>\n", None, OUT),
 ('l2-naming-a-value', 0, '36\n', None, OUT), ('l2-naming-a-value', 6, '6\n', None, OUT), ('l2-naming-a-value', 'q-copy', '4\n', None, OUT),
 ('l2-naming-a-value', 'q-stale', '30\n', None, OUT), ('l2-naming-a-value', 'q-steps', '7\n', None, OUT),
 ('l3-text', 0, '125\n', None, OUT), ('l3-text', 4, 'U\n', None, OUT), ('l3-text', 5, 'False\n', None, OUT),
 ('l3-text', 6, '', 'TypeError', ERR), ('l3-text', 'q-slice', 'VOD\n', None, OUT), ('l3-text', 'q-format', 'Cost: £7.00\n', None, OUT),
 ('l3-text', 'q-type', "<class 'str'>\n", None, OUT),
 ('l4-asking-and-printing', 0, '33\n', None, OUT), ('l4-asking-and-printing', 3, '', 'ValueError', ERR),
 ('l4-asking-and-printing', 5, '', 'NameError', SAYS), ('l4-asking-and-printing', 6, '', 'TypeError', ERR),
 ('l4-asking-and-printing', 'q-input-type', "<class 'str'>\n", None, OUT), ('l4-asking-and-printing', 'q-convert', '100.0\n', None, OUT),
 ('l5-decisions', 1, 'sell\ndone\n', None, SAYS), ('l5-decisions', 2, 'False\n', None, OUT), ('l5-decisions', 5, 'up\n', None, OUT),
 ('l5-decisions', 6, '', 'SyntaxError', ERR), ('l5-decisions', 'q-at-least', 'large\n', None, OUT),
 ('l5-decisions', 'q-loss-chain', 'big loss\n', None, OUT), ('l5-decisions', 'q-equal-and-less', 'True False\n', None, OUT),
 ('l6-until-done', 'q-zero-passes', '50.0\n', None, OUT), ('l6-until-done', 'q-count-prints', '3\n7\n11\n', None, LINES),
 ('l7-for-each', 1, '0\n1\n2\n3\n', None, SAYS), ('l7-for-each', 3, '15\n', None, OUT), ('l7-for-each', 5, '3.0\n', None, OUT),
 ('l7-for-each', 'q-range-two-five', '2\n3\n4\n', None, SAYS), ('l7-for-each', 'q-lines', 'check\ncheck\ncheck\nreport\n', None, LINES),
 ('l7-for-each', 'q-losses-only', '-1.5\n', None, OUT), ('l7-for-each', 'q-empty-list', '0\n', None, SAYS),
 ('l8-many-values', 1, '104.75 5\n', None, OUT), ('l8-many-values', 2, '[100.0, 101.25]\n', None, OUT), ('l8-many-values', 5, '0\n', None, OUT),
 ('l8-many-values', 7, 'ok 0.4\nok -0.8\nok 1.1\nlimit hit -2.6\n', None, SAYS), ('l8-many-values', 'q-index-sum', '24\n', None, OUT),
 ('l8-many-values', 'q-empty-index', '0\n', 'IndexError', ERR), ('l8-many-values', 'q-break-count', '3\n', None, OUT),
 ('l9-packaging-steps', 0, '9\n', None, OUT), ('l9-packaging-steps', 5, '-5.0\n', None, OUT), ('l9-packaging-steps', 7, '3.0\n', 'TypeError', ERR),
 ('l9-packaging-steps', 'q-before-def', '', 'NameError', ERR), ('l9-packaging-steps', 'q-print-none', '10.0\nNone\n', None, SAYS),
 ('l9-packaging-steps', 'q-local-copy', '500.0\n', None, OUT), ('l9-packaging-steps', 'q-cost', '121.5\n', None, OUT),
 ('l10-reading-errors', 2, '', 'IndexError', SAYS), ('l10-reading-errors', 3, '', 'NameError', SAYS),
 ('l10-reading-errors', 5, '', 'ZeroDivisionError', SAYS), ('l10-reading-errors', 'q-slice', '[102.5, 99.8, 100.4]\n', None, OUT),
 ('l10-reading-errors', 'q-last-index', '3\n', None, OUT),
 ('l11-numbers-from-a-file', 0, '', 'TypeError', ERR), ('l11-numbers-from-a-file', 4, '101.20\n\n102.50\n\n99.80\n\n', None, SAYS),
 ('l11-numbers-from-a-file', 5, '', 'ValueError', ERR), ('l11-numbers-from-a-file', 'q-split', "['Thu', '100.40\\n']\n", None, OUT),
 ('l11-numbers-from-a-file', 'q-strip', '101.200\n', None, OUT),
 ('l12-savings-script', 0, '2249.73\n', None, OUT), ('l12-savings-script', 4, 'Year 10: £1628.89\n', None, OUT),
 ('l12-savings-script', 'q-range-count', 'Year 1\nYear 2\nYear 3\nYear 4\n', None, LINES), ('l12-savings-script', 'q-ten-percent', '605.0\n', None, OUT),
 ('l12-savings-script', 'q-silent', '', None, SAYS),
 ('review-1', 0, '5.0\n', None, OUT), ('review-1', 1, '380\n', None, OUT), ('review-1', 2, '10\n', None, OUT),
 ('review-1', 3, 'Cost: £42.00\n', None, OUT), ('review-1', 4, '12\n', None, OUT), ('review-1', 5, 'P&L: -12.50\n', None, OUT),
 ('review-2', 0, 'at target\n', None, OUT), ('review-2', 1, '5\n', None, OUT), ('review-2', 2, '16\n', None, OUT),
 ('review-2', 3, '-8.25\n', None, OUT), ('review-2', 5, '42.0\n', None, SAYS), ('review-2', 7, '3\n', None, OUT),
 ('review-3', 0, '10.0\n', None, SAYS), ('review-3', 2, '1200\n\n', None, SAYS), ('review-3', 3, '31.84\n', None, OUT),
 ('review-3', 5, '', 'NameError', ERR),
 ('homework-1', 0, '-4\n', None, OUT), ('homework-1', 1, '16\n', None, OUT), ('homework-1', 2, '4.0\n', None, OUT),
 ('homework-1', 3, '', 'ValueError', SAYS),
 ('homework-2', 1, '5\n', None, OUT), ('homework-2', 5, '3\n', None, OUT), ('homework-2', 6, 'no order\n', None, OUT),
 ('homework-3', 5, '1000.0\n', None, OUT),
]
INPUTS = {('l4-asking-and-printing', 0): '3', ('l4-asking-and-printing', 6): '10', ('l4-asking-and-printing', 'q-input-type'): '42'}
for file, idx, want_out, want_err, rel in A:
    it = item(file, idx); where = f'{file}[{idx}]'
    out, err, _, _ = run(snippet(it), INPUTS.get((file, idx)))
    check(out == want_out, where, f'snippet prints {out!r}, the audit expected {want_out!r}')
    check((err or '').split(':')[0] == (want_err or ''), where, f'snippet ends with {err!r}, the audit expected {want_err}')
    key, w = key_of(it), it['widget']
    if rel == OUT:
        if w['kind'] == 'choice':
            check(key == out.strip(), where, f'the option marked correct is {key!r} but Python prints {out.strip()!r}')
        else:
            check(float(out.strip()) == float(key), where, f'answer {key} but Python prints {out.strip()}')
    elif rel == LINES:
        check(len(out.splitlines()) == key, where, f'answer {key} but {len(out.splitlines())} lines print')
    elif rel == ERR:
        check(want_err in key, where, f'the option marked correct ({key!r}) does not name {want_err}')
    if w['kind'] == 'choice':   # no wrong option may be the true output
        for o in w['options']:
            if not o.get('correct'):
                check(norm(o['text']) != out.rstrip('\n') or not out.strip(), where, f'wrong option {o["id"]} ({o["text"]!r}) is what Python prints')
    else:
        for x in w.get('wrong', []):
            true = len(out.splitlines()) if rel == LINES else float(out.strip())
            check(abs(x['value'] - true) > (x.get('tol') or {}).get('abs', 0), where, f'slip {x["id"]} = {x["value"]} is the true answer')

# keys that describe a run, checked one by one
check('sell' in key_of(item('l5-decisions', 1)) and 'done' in key_of(item('l5-decisions', 1)), 'l5-decisions[1]', 'key should be sell then done')
check(key_of(item('l7-for-each', 1)).startswith('0, 1, 2 and 3'), 'l7-for-each[1]', 'key should list 0 to 3')
check(key_of(item('l7-for-each', 'q-range-two-five')) == '2, 3 and 4', 'l7-for-each[q-range-two-five]', 'key should be 2, 3 and 4')
check('prints 0' in key_of(item('l7-for-each', 'q-empty-list')), 'l7-for-each[q-empty-list]', 'key should be: prints 0')
check('limit hit -2.6' in key_of(item('l8-many-values', 7)), 'l8-many-values[7]', 'key should end with limit hit -2.6')
check(key_of(item('l9-packaging-steps', 'q-print-none')) == '10.0, then None', 'l9[q-print-none]', 'key should be 10.0 then None')
check("'1200\\n'" in key_of(item('review-3', 2)), 'review-3[2]', "row[2] is the text '1200\\n'")
check(key_of(item('review-3', 0)) == '10.0 only', 'review-3[0]', 'key should be 10.0 only')

# file-state items
out, err, _, left = run(snippet(item('l12-savings-script', 6)))
check(left.get('plan.txt') == 'Year 3\n' and 'Year 3' in key_of(item('l12-savings-script', 6)), 'l12[6]', f'plan.txt holds {left.get("plan.txt")!r}')
out, err, _, left = run(snippet(item('l12-savings-script', 'q-append-mode')), files={'log.txt': 'Mon 101.20\n'})
check(left['log.txt'] == 'Mon 101.20\nTue 102.50\n', 'l12[q-append-mode]', f'log.txt holds {left["log.txt"]!r}')
out, err, _, _ = run(snippet(item('l11-numbers-from-a-file', 'q-blank-line')), files={'closes.txt': '101.20\n102.50\n\n'})
check(err == "ValueError: could not convert string to float: '\\n'", 'l11[q-blank-line]', f'got {err!r}')
check(err in text_of(item('l11-numbers-from-a-file', 'q-blank-line')).replace('\\\\n', '\\n'), 'l11[q-blank-line]', 'quoted message differs')
out, err, _, _ = run(snippet(item('l11-numbers-from-a-file', 'q-count-rows')), files={'prices.csv': 'Day,Close\n' + 'd,1.00\n' * 20})
check(out == '20\n' == f"{item('l11-numbers-from-a-file', 'q-count-rows')['widget']['answer']}\n", 'l11[q-count-rows]', f'prints {out!r}')
# the fixed scripts the explanations give
out, err, _, _ = run('print(with_fee(10.00))\n\ndef with_fee(price):\n    return price + 1.50\n'.split('\n\n')[1] + '\nprint(with_fee(10.00))\n')
check(out == '11.5\n', 'l9[q-before-def].explain', f'def first prints {out!r}, content says 11.5')
out, err, _, _ = run('def average(xs):\n    return sum(xs) / len(xs)\n\nprint(average([101.20, 102.50]))\n')
check(out == '101.85\n', 'l10[3].explain', f'prints {out!r}, content says 101.85')
out, err, _, _ = run('pnls = [-120.00, -45.50, -80.00]\nbest = pnls[0]\nfor p in pnls:\n    if p > best:\n        best = p\nprint(best)\n')
check(out == '-45.5\n', 'l8[5].explain', f'prints {out!r}, content says -45.5')
out, err, _, _ = run('price = float(input("Price: "))\nqty = 10\nvalue = price * qty\nprice = 52\nvalue = price * qty\navg = (50 + 52) / 2\nprint(value)\nprint(avg)\n', inp='50')
check(out == '520\n51.0\n', 'homework-1[7].model', f'fixed script prints {out!r}')
out, err, _, _ = run('price = input("Price: ")\nqty = 10\nvalue = price * qty\nprice = 52\navg = 50 + 52 / 2\nprint(value)\nprint(avg)\n', inp='50')
check(out == '50505050505050505050\n76.0\n' and '50505050505050505050\\n76.0' in text_of(item('homework-1', 7)), 'homework-1[7].model', f'prints {out!r}')
HW2 = 'pnls = [-35.00, 120.50, 0.00, -80.25, 64.75]\nbest = 0\nwinners = 0\ni = 1\nwhile i < len(pnls):\n    total = 0\n    p = pnls[i]\n    total = total + p\n    if p > best:\n        best = p\n    if p >= 0:\n        winners = winners + 1\n    i = i + 1\nprint(total, best, winners)\n'
out, err, _, _ = run(HW2)
check(out == '64.75 120.5 3\n' and '64.75 120.5 3' in item('homework-2', 8)['model'], 'homework-2[8].model (a)', f'prints {out!r}')
FIX2 = re.findall(r'```python\n(.*?)```', item('homework-2', 8)['model'], re.S)[0]
out, err, _, _ = run(FIX2)
check(out == '70.0 120.5 2\n', 'homework-2[8].model (c)', f'prints {out!r}')
out, err, _, _ = run(FIX2.replace('[-35.00, 120.50, 0.00, -80.25, 64.75]', '[]'))
check(out == '0 None 0\n', 'homework-2[8].model (d)', f'prints {out!r} {err!r}')
BUG3 = item('homework-3', 7)['prompt']; SRC3 = re.findall(r'```python\n(.*?)```', BUG3, re.S)[0]
out, err, tb3, _ = run(SRC3, filename='returns.py')
check(err == "ValueError: could not convert string to float: 'Close\\n'", 'homework-3[7]', f'got {err!r}')
out, err, _, _ = run(SRC3.replace('open(name):', 'open(name).readlines()[1:]:'), filename='returns.py')
check(err == "TypeError: object of type 'NoneType' has no len()", 'homework-3[7].model bug 2', f'got {err!r}')
out, err, _, _ = run(SRC3.replace('open(name):', 'open(name).readlines()[1:]:').replace('[1]))\n', '[1]))\n    return closes\n', 1), filename='returns.py')
check(err is None and out.count(',') == 4, 'homework-3[7].model bug 3', f'five numbers expected, got {out!r} {err!r}')
out, err, _, _ = run(re.findall(r'```python\n(.*?)```', item('homework-3', 7)['model'], re.S)[0])
check(err is None and out.count(',') == 3, 'homework-3[7].model (c)', f'four returns expected, got {out!r} {err!r}')

# ---------------------------------------------------------------- B: slips and named wrong options, recomputed
def slip(file, idx, sid):
    w = item(file, idx)['widget']
    if w['kind'] == 'numeric':
        return next(x['value'] for x in w['wrong'] if x['id'] == sid)
    return norm(next(o['text'] for o in w['options'] if o['id'] == sid))
def fb(file, idx, sid):
    it = item(file, idx)
    return (it.get('feedback', {}).get('byKey', {}) or {}).get(sid) or next((o.get('why', '') for o in it['widget'].get('options', []) if o['id'] == sid), '')
B = [  # file, idx, slip id, the value the named mistake gives
 ('l1-calculator', 'q-floor', 'decimal', round(20 / 6, 4)),
 ('l1-calculator', 4, 'four', str(round(19 / 5))), ('l1-calculator', 4, 'decimal', str(19 / 5)), ('l1-calculator', 4, 'rem', str(float(round(19 / 5)))),
 ('l1-calculator', 5, 'thirtysix', str((2 * 3) ** 2)), ('l1-calculator', 5, 'twelve', str(2 * 3 * 2)), ('l1-calculator', 5, 'sixtyfour', str(2 ** (3 * 2))),
 ('l1-calculator', 6, 'avg', str((10 + 14) / 2)), ('l1-calculator', 6, 'int', str(10 + 14 // 2)), ('l1-calculator', 0, 'twenty', str((2 + 3) * 4)),
 ('l1-calculator', 'q-precedence', 'lr', str((3 + 4) * 2)),
 ('l2-naming-a-value', 'q-steps', 'first', 2), ('l2-naming-a-value', 'q-steps', 'order', (2 + 1) * 3),
 ('l2-naming-a-value', 'q-copy', 'five', '5'), ('l2-naming-a-value', 'q-stale', 'new', str(11 * 3)),
 ('l3-text', 0, 'sum', str(12 + 5)), ('l3-text', 4, 'third', 'GBPUSD'[2]), ('l3-text', 4, 'rest', 'GBPUSD'[3:6]), ('l3-text', 4, 'first', 'GBPUSD'[0:3]),
 ('l3-text', 8, 'six', str(7 - 2 + 1)), ('l3-text', 'q-slice', 'four', 'VOD.L'[0:4]), ('l3-text', 'q-slice', 'from1', 'VOD.L'[1:4]),
 ('l4-asking-and-printing', 'q-convert', 'forty', 40), ('l4-asking-and-printing', 'q-convert', 'eighty', 40 * 2),
 ('l6-until-done', 2, 'last-positive', 1), ('l6-until-done', 2, 'sign', 3 - 1), ('l6-until-done', 2, 'start', 10),
 ('l6-until-done', 7, 'ten', str(len([2, 4, 6, 8, 10]))), ('l6-until-done', 7, 'ones', str(len(range(2, 10)))), ('l6-until-done', 7, 'skip-first', str(len([4, 6, 8]))),
 ('l6-until-done', 'q-count-prints', 'fifteen', len([3, 7, 11, 15])), ('l6-until-done', 'q-count-prints', 'ones', 15 - 3), ('l6-until-done', 'q-to-1500', 'four', 4),
 ('l7-for-each', 3, 'with-six', sum(range(1, 7))), ('l7-for-each', 3, 'last', 5), ('l7-for-each', 3, 'from-zero', sum(range(5))),
 ('l7-for-each', 'q-lines', 'inside', 3 + 3), ('l7-for-each', 'q-lines', 'three', 3),
 ('l7-for-each', 'q-losses-only', 'all', 1.5 - 0.5 + 2.0 - 1.0), ('l7-for-each', 'q-losses-only', 'last', -1.0),
 ('l7-for-each', 'q-losses-only', 'gains', 1.5 + 2.0), ('l7-for-each', 'q-losses-only', 'sign', 1.5), ('l7-for-each', 5, 'sum', str(12.5 - 4 + 7.25 + 3)),
 ('l8-many-values', 'q-index-sum', 'from-one', 4 + 16), ('l8-many-values', 'q-index-sum', 'neg-second-last', 8 + 15),
 ('l8-many-values', 'q-break-count', 'counted-break', 4), ('l8-many-values', 'q-break-count', 'no-break', 5), ('l8-many-values', 'q-break-count', 'skipped-neg', 2),
 ('l8-many-values', 5, 'largest', '-45.5'), ('l8-many-values', 5, 'first', '-120.0'), ('l8-many-values', 5, 'sum', str(-120.0 - 45.5 - 80.0)),
 ('l9-packaging-steps', 'q-cost', 'fee-each', (2.40 + 1.50) * 50), ('l9-packaging-steps', 'q-cost', 'no-fee', 2.40 * 50),
 ('l9-packaging-steps', 0, 'ten', str(2 * (4 + 1))), ('l9-packaging-steps', 0, 'eight', str(2 * 4)), ('l9-packaging-steps', 5, 'by-size', str(105.0 - 100.0)),
 ('l10-reading-errors', 'q-last-index', 'count', 4), ('l10-reading-errors', 'q-last-index', 'no-append', 2 - 1),
 ('l11-numbers-from-a-file', 'q-count-rows', 'with-header', 21), ('l11-numbers-from-a-file', 'q-count-rows', 'two-off', 19),
 ('l12-savings-script', 0, 'simple', str(2000.0 + 3 * 80)), ('l12-savings-script', 0, 'once', str(2000 * 1.04)), ('l12-savings-script', 0, 'four', str(round(2000 * 1.04 ** 4, 2))),
 ('l12-savings-script', 'q-range-count', 'five', 5), ('l12-savings-script', 'q-range-count', 'three', 3),
 ('l12-savings-script', 'q-ten-percent', 'simple', 500 + 2 * 50), ('l12-savings-script', 'q-ten-percent', 'once', 550),
 ('review-1', 4, 'nearest', round(18 / 5) + 3 ** 2), ('review-1', 4, 'times', 18 // 5 + 3 * 2), ('review-1', 0, 'added', str((2 + 6) / 2)),
 ('review-1', 1, 'follow', str(500 - 200)), ('review-1', 2, 'stop', '2026-10-16'[5:8]), ('review-1', 2, 'from1', '2026-10-16'[4:6]),
 ('review-2', 1, 'stopped-81', 4), ('review-2', 1, 'n', 243), ('review-2', 2, 'with-four', sum(2 * k + 1 for k in range(5))),
 ('review-2', 2, 'from-one', sum(2 * k + 1 for k in range(1, 5))), ('review-2', 7, 'fifteen', 4), ('review-2', 7, 'minus-forty', 2),
 ('review-3', 3, 'simple', 1500 * 0.02), ('review-3', 3, 'b', round(1500 * 1.02 ** 4, 2)),
 ('homework-1', 1, 'linked', 12 + 12), ('homework-1', 1, 'stale', 4 + 4), ('homework-1', 2, 'bracketed', round((2 + 18) / 3 ** 2, 4)),
 ('homework-1', 2, 'divfirst', 2 + (18 / 3) ** 2), ('homework-1', 0, 'chop', str(int(-7 / 2))), ('homework-1', 0, 'float', str(-7 / 2)),
 ('homework-2', 1, 'four', 4), ('homework-2', 5, 'flat-up', 5), ('homework-2', 5, 'all-ups', 6), ('homework-2', 5, 'last-run', 1),
 ('homework-3', 6, 'no-interest', 600), ('homework-3', 6, 'start-of-year', round(200 * (1.05 ** 3 + 1.05 ** 2 + 1.05), 2)),
 ('homework-3', 5, 'grown', '1157.625'),
]
for file, idx, sid, val in B:
    got = slip(file, idx, sid)
    ok = (got == val) if isinstance(val, str) else abs(got - val) < 5e-3
    check(ok, f'{file}[{idx}].{sid}', f'slip value {got!r} but the mistake its line names gives {val!r}')
# the one slip whose line names a mistake that does not give its value
q = item('l1-calculator', 'q-floor'); line = q['feedback']['byKey']['nearest']
if 'to the nearest' in line:
    check(round(20 / 6) == slip('l1-calculator', 'q-floor', 'nearest'), 'l1-calculator[q-floor].nearest',
          f'the line says "rounded 3.33 to the nearest", which is {round(20 / 6)}, but the slip value is {slip("l1-calculator", "q-floor", "nearest")} (rounding up)')
# table keys
k, vals = 10, []
while k > 0:
    k -= 3
check(k == item('l6-until-done', 2)['widget']['answer'] == -2, 'l6[2]', 'counting down ends at -2')
bal, rows = 1000.0, item('l6-until-done', 8)['widget']['rows']
for r in rows:
    bal *= 1.07
    check(abs(bal - r[1]['answer']) < 0.005, 'l6[8]', f'balance {bal:.3f} against key {r[1]["answer"]}')
check(round(1070 * 0.07, 2) == 74.9 and '74.90' in item('l6-until-done', 8)['feedback']['byKey']['r1c1'], 'l6[8].r1c1', 'second year adds 74.90')
check(round(1000 * 1.07 ** 3 - 1000 * 1.07 ** 2, 2) == 80.14, 'l6[8].explain', 'third year adds 80.14')
# a cell line fires for ANY wrong value of its cell (table.js: key is the cell id unless a cell wrong[] matches)
r1 = rows[1][1]
note('You added £70 again' in item('l6-until-done', 8)['feedback']['byKey']['r1c1'] and not r1.get('wrong'), 'l6-until-done[8].feedback.byKey.r1c1',
     'the line names one mistake (1140.00) but shows for every wrong value in the cell: no cell wrong[] carries it')

# ---------------------------------------------------------------- C: quoted error messages
C = [
 ('l3-text', 6, 'price = 12.5\nprint("Price: " + price)\n', 'TypeError: can only concatenate str (not "float") to str'),
 ('l4-asking-and-printing', 3, 'print(int("7.5"))\n', "ValueError: invalid literal for int() with base 10: '7.5'"),
 ('l4-asking-and-printing', 6, 'typed = "10"\nprint(typed + 5)\n', 'TypeError: can only concatenate str (not "int") to str'),
 ('l4-asking-and-printing', 7, 'typed_qty = "8"\nprice = 12.5\ntotal = price * typed_qty\nprint(total)\n', "TypeError: can't multiply sequence by non-int of type 'float'"),
 ('l5-decisions', 6, 'signal = "buy"\nif signal = "buy":\n    print("send order")\n', "SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?"),
 ('l8-many-values', 'q-empty-index', 'prices = []\nprint(prices[0])\n', 'IndexError: list index out of range'),
 ('l9-packaging-steps', 6, 'fee = 1.50\ndef net(px):\n    left = px - fee\n    return left\ncash = net(100.00)\nprint(left)\n', "NameError: name 'left' is not defined"),
 ('l9-packaging-steps', 7, 'g = None\nprint(g * 10)\n', "TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'"),
 ('l10-reading-errors', 7, 'float("Close")\n', "ValueError: could not convert string to float: 'Close'"),
 ('l11-numbers-from-a-file', 0, 'total = 0\nfor line in open("closes.txt"):\n    total = total + line\n', "TypeError: unsupported operand type(s) for +: 'int' and 'str'"),
 ('l11-numbers-from-a-file', 5, 'float("Close\\n")\n', "ValueError: could not convert string to float: 'Close\\n'"),
 ('l12-savings-script', 8, 'savings.py\n', "NameError: name 'savings' is not defined"),
]
for file, idx, code, msg in C:
    out, err, _, _ = run(code)
    check(err == msg, f'{file}[{idx}]', f'Python says {err!r}, the audit expected {msg!r}')
    check(msg in text_of(item(file, idx)).replace('\\"', '"').replace('\\\\n', '\\n'), f'{file}[{idx}]', f'content does not quote {msg!r}')
out, err, _, _ = run('typed = "4.5%"\nfloat(typed)\n'); check(err.startswith('ValueError'), 'l4[10].explain', 'float("4.5%") is a ValueError')
out, err, _, _ = run('cash = 98.5\nprint(cash)\n'); check(100.00 - 1.50 == 98.5, 'l9[6]', 'cash holds 98.5')

# ---------------------------------------------------------------- D: tracebacks
def pad(n, line, pre=''):
    """A script whose line n is `line`, with `pre` as its first lines."""
    head = pre.rstrip('\n').split('\n') if pre else []
    return '\n'.join(head + ['#'] * (n - 1 - len(head)) + [line]) + '\n'
RISK = item('l10-reading-errors', 8)['widget']['starter']
D = [  # file, idx, field, script name, source
 ('l4-asking-and-printing', 5, 'prose', 'main.py', 'price = float("12.50")\nquantity = int("8")\ntotal = price * qty\n'),
 ('l4-asking-and-printing', 'q-traceback', 'prose', 'main.py', pad(4, 'shares = int(typed)', 'typed = "12.5"')),
 ('l10-reading-errors', 2, 'prose', 'closes.py', 'prices = [101.20, 102.50, 99.80, 100.40]\nprint(prices[4])\n'),
 ('l10-reading-errors', 3, 'prose', 'avg.py', 'print(average([101.20, 102.50]))\n\ndef average(xs):\n    return sum(xs) / len(xs)\n'),
 ('l10-reading-errors', 4, 'prose', 'closes.py', 'closes = [101.20, 102.50]\ncloses = closes.append(99.80)\ncount = len(closes)\n'),
 ('l10-reading-errors', 5, 'prose', 'returns.py', 'def daily_return(p0, p1):\n    return (p1 - p0) / p0\n\ncloses = [0.00, 101.20, 102.50]\nprint(daily_return(closes[0], closes[1]))\n'),
 ('l10-reading-errors', 6, 'prose', 'fees.py', 'def with_fee(price_text):\n    return price_text + 1.50\n\nprint(with_fee("101.20"))\n'),
 ('l10-reading-errors', 8, 'prose', 'risk.py', RISK),
 ('l10-reading-errors', 'q-read-value', 'prose', 'load.py', pad(7, 'closes.append(float(parts[1]))', 'closes = []\nparts = ["Wed", "n/a"]')),
 ('l10-reading-errors', 'q-two-frames', 'prose', 'report.py',
  pad(12, 'report(closes)', '#\ndef average(xs):\n    return sum(xs) / len(xs)\n#\n#\n#\ndef report(closes):\n    print(average(closes[5:]))\ncloses = [1.0, 2.0]')),
 ('review-1', 7, 'prose', 'main.py', 'fee = "1.5"\nprice = 99.5\ntotal = price + fee\n'),
 ('review-3', 1, 'prose', 'risk.py',
  pad(9, 'print(worst_day(closes))', 'def worst_day(closes):\n    worst = 0.0\n    for i in range(len(closes)):\n        change = closes[i + 1] - closes[i]\n    return worst\ncloses = [1.0, 2.0]')),
 ('homework-1', 3, 'prose', 'main.py', 'typed = "1,250.40"\ncash = float(typed)\n'),
 ('homework-3', 4, 'prose', 'load.py',
  pad(11, 'closes = read_closes("prices.csv")', 'def read_closes(name):\n    closes = []\n    for line in ["Mon,1.0\\n", "\\n"]:\n        parts = line.split(",")\n        closes.append(float(parts[1]))\n    return closes')),
 ('homework-3', 7, 'prompt', 'returns.py', SRC3),
]
def loose(t):
    return [ln for ln in t.split('\n') if ln.startswith('  File') or not ln.startswith(' ')]
for file, idx, field, name, code in D:
    it = item(file, idx); where = f'{file}[{idx}] traceback'
    shown = re.findall(r'```text\n(Traceback.*?)\n```', it[field], re.S)[-1]
    out, err, tb, _ = run(code, filename=name)
    check(tb is not None, where, 'the reconstruction did not raise')
    if tb is None:
        continue
    if STRICT_TB:
        check(tb == shown, where, f'Python 3.12 prints\n{tb}\nbut the content shows\n{shown}')
    else:
        check(loose(tb) == loose(shown), where, f'File lines or last line differ:\n{tb}\nagainst\n{shown}')

# ---------------------------------------------------------------- E: stated rules on a grid
ints = [-9, -7, -2, -1, 1, 2, 3, 5, 6, 7, 19, 20]
check(all(type(a / b) is float for a in ints + [0] for b in ints), 'l1 rule', '/ on two ints always gives a float')
check(all(type(a // b) is int and a // b == math.floor(a / b) for a in ints + [0] for b in ints), 'l1 rule', '// on two ints gives an int, rounded down')
check(2 ** 3 ** 2 == 2 ** 9 == 512 and 10 - 4 - 3 == 3 and 8 - 6 / 2 == 5.0, 'l1[8]', 'ties left to right, except powers')
check((262.5 - 250) / 250 == 0.05 and 262.5 - 250 / 250 == 261.5, 'l1[9]', 'return 0.05; without brackets 261.5')
check(str(182.40 * 25) == '4560.0' and str(185.10 * 25) == '4627.5' and round(4627.5 - 4560, 2) == 67.5, 'l2[9]', 'position values and the gain')
check(('12' == 12) is False and ('0' == 0) is False and '12' + '5' == '125' and '12' * 2 == '1212' and '3' * 2 == '33', 'l3 rules', 'text against numbers')
s = 'ABCDEFGHIJ'
check(all(len(s[a:b]) == b - a for a in range(11) for b in range(a, 11)), 'l3[8]', 'slice length b - a inside the string')
note(len(s[2:15]) != 15 - 2 and len(s[7:2]) != 2 - 7, 'l3[8].prose, l10 summary',
     'slice length b - a needs 0 <= a <= b <= len(s); the l3 summary note states it, the l3 prose and the l10 summary do not')
check(f'{12.5:.2f}' == '12.50' and f'{7:.2f}' == '7.00' and f'{37.25:+.2f}' == '+37.25' and f'{-8.5:+.2f}' == '-8.50' and f'+{-8.5:.2f}' == '+-8.50', 'l3 formats', '.2f and +.2f')
check(int(7.5) == 7 and float(' 12.50\n') == 12.5 and float('12.75') * 4 == 51.0 and str(float('4.5') / 100) == '0.045' and f'{2000 * 0.045:.2f}' == '90.00', 'l4 conversions', 'int, float')
check(f'{(189.35 - 184.2) / 184.2 * 100:.2f}' == '2.80' and round(189.35 - 184.20, 2) == 5.15 and abs((189.35 - 184.2) / 184.2 - 0.02796) < 5e-6, 'l4[9]', 'return 2.80%')
check((98.0 < 98.0) is False and (98.0 <= 98.0) is True and (100 >= 100) is True, 'l5 rules', 'strict and non-strict comparisons')
ran = []
if 5: ran.append('int 5')
if 'no': ran.append('text')
if [0]: ran.append('list')
note(len(ran) == 3, 'l5-decisions[2].explain', '"An if line only asks whether its condition\'s value is True": any truthy value runs the block (5, "no", [0])')
def passes(a, b, st):
    n, c = a, 0
    while n < b:
        n += st; c += 1
    return c
check(all(passes(a, b, st) == math.ceil((b - a) / st) for a in range(-5, 8) for b in range(a + 1, 25) for st in range(1, 7)), 'l6[7]', 'passes = ceil((b - a)/s) for a < b, s > 0')
check(all(passes(a, b, st) == 0 for a in range(0, 6) for b in range(-3, a + 1) for st in (1, 3)), 'l6 summary', 'zero passes when a >= b')
check(all((n < 6) == (n <= 5) for n in range(-10, 20)), 'l6[4]', 'n < 6 is n <= 5 for whole numbers')
x, c = 10, 0
while x < 1000:
    x *= 2; c += 1
check((x, c) == (1280, 7), 'l6[q-never-ends].double', 'doubling from 10 reaches 1280 after seven passes')
def ytd(balance, rate):
    target, years = 2 * balance, 0
    while balance < target:
        balance *= 1 + rate; years += 1
    return years
check(ytd(1000.0, 0.07) == 11 and abs(1.07 ** 10 - 1.967) < 5e-4 and abs(1.07 ** 11 - 2.105) < 5e-4 and abs(72 / 7 - 10.3) < 0.05 and abs(1 / 0.07 - 14.3) < 0.05, 'l6[8], l6[9]', 'doubling at 7%')
b10 = [round(1000 * 1.1 ** k, 2) for k in range(1, 6)]
check(b10 == [1100.0, 1210.0, 1331.0, 1464.1, 1610.51], 'l6[q-to-1500]', f'balances {b10}')
check(list(range(4)) == [0, 1, 2, 3] and list(range(1, 6)) == [1, 2, 3, 4, 5] and list(range(1, 13))[-1] == 12 and len(range(1, 13)) == 12 and list(range(1, 1)) == [], 'l7 rules', 'range')
check(all(len(range(a, b)) == b - a for a in range(-3, 6) for b in range(a, 12)), 'l7[7].explain', 'count is b - a whenever b >= a')
check(sum([12.50, -4.00, 7.25, 3.00]) == 18.75 and sum([310.40, -120.15, -95.25, 42.00, 18.60]) - 155.6 < 1e-9, 'l7 totals', 'running totals')
p = [101.20, 99.80, 103.50, 102.10, 104.75]
check(p[-1] == p[len(p) - 1] and p[-len(p)] == p[0] and [][0:1] == [], 'l8 rules', 'negative index, last index is len - 1')
cl = []; r = cl.append(99.80)
check(r is None and str([100.00, 101.25]) == '[100.0, 101.25]', 'l8[2], l10[4]', 'append returns None; 100.00 prints as 100.0')
a = [1.0]; b = a; a.append(2.0)
note(b == [1.0, 2.0], 'l2-naming-a-value summary.ideas[2], [5].explain',
     '"A later change to a leaves b where it was" / "Changing a later never changes b": true for reassignment, false for a list changed in place (a.append shows through b); l8 teaches append and index assignment without saying so')
_x = 1
note(_x == 1, 'l2-naming-a-value[3].prose', '"A name starts with a letter": a name may also start with an underscore (language reference 2.3)')
note(str(0.1 + 0.2) != '0.3', 'l3-text[6].options[twodp].why', '"Python never adds digits on its own": print(0.1 + 0.2) shows 0.30000000000000004')
peaks, pk = [], 100.0
for v in [100.00, 104.00, 101.50, 106.20, 103.00]:
    pk = max(pk, v); peaks.append(round(pk - v, 2))
check(max(peaks) == 3.2 and peaks[-1] == 3.2, 'l8[9].explain, homework-2[4]', 'largest gap 3.20 on the last day')
def f_none():
    pass
check(f_none() is None and 250.0 * 0.01 == 2.5 and str(250.0 * 0.01) == '2.5' and 50.00 * 0.2 == 10.0 and 5000.00 * 0.002 == 10.0, 'l9 rules', 'no return gives None; fee values')
check(abs(-5 / 245 + 0.0204) < 5e-5 and 245 - 250 / 250 == 244.0 and (245 - 250) / 250 * 100 == -2.0 and (245.0 - 250.0) / 250.0 == -0.02, 'l9[10].test-1', 'the three wrong values the line names')
check((12.5 + 1.5) * 10 == 140.0 and 12.5 * 10 == 125.0, 'l9[4].test-1', '140.0 and 125.0')
check([101.20, 102.50, 99.80, 100.40][1:3] == [102.5, 99.8] and [1, 2][5:] == [], 'l10 slices', 'slice of a list; a slice past the end is empty')
def mdd(prices):
    peak, worst = prices[0], 0.0
    for price in prices:
        peak = max(peak, price); worst = max(worst, (peak - price) / peak)
    return worst
check(abs(mdd([100.0, 110.0, 99.0, 105.0, 88.0, 95.0]) - 0.2) < 1e-12 and mdd([120.0]) == 0.0 and abs(mdd([100.0, 120.0, 90.0, 130.0]) - 0.25) < 1e-12, 'l10[8], homework-3[1]', 'maximum drawdown')
check(abs((130 - 90) / 130 - 0.31) < 5e-3 and (100 - 90) / 100 == 0.1 and abs((240 - 175) / 240 - 0.271) < 5e-4 and (250 - 175) / 250 == 0.3, 'homework-3[1].test-1, test-2', 'the wrong values the lines name')
check('Tue,102.50\n'.split(',') == ['Tue', '102.50\n'] and '  101.20\n'.strip() == '101.20' and float('102.50\n') == 102.5, 'l11 rules', 'split, strip, float')
note('a\nb'.splitlines(True)[-1] == 'b', 'l11-numbers-from-a-file summary.ideas[0]', '"each ending in a newline": the last line of a file need not (test 2 of screen 2 passes one without)')
check(max(['101.20\n', '102.50\n', '99.80\n', '100.40\n', '101.10\n']) == '99.80\n' and '99.00' > '105.10', 'homework-3[2]', 'as text 99.80 beats 102.50')
check(round(2000 * 1.04 ** 3, 2) == 2249.73 and round(1000 * 1.05 ** 10 - 1000, 2) == 628.89 and round(1000 * 1.1 ** 10 - 1000, 2) == 1593.74
      and round(1000 * 1.05 ** 10 - 1000 * 1.05 ** 9, 2) == 77.57, 'l12[0], l12[1]', 'compounding figures')
def project(balance, rate, years):
    for _ in range(years):
        balance = balance * (1 + rate)
    return balance
check(project(2000.0, 0.04, 3) == 2249.7280000000005 and project(1000.0, 0.05, 10) == 1628.8946267774422 and round(project(1000.0, 0.05, 10), 2) == 1628.89, 'l12[2], l12[q-silent]', 'project values')
check(all(math.isclose(project(B, r, n), B * (1 + r) ** n, rel_tol=1e-12) for B in (500.0, 1000.0, 2000.0) for r in (0.0, 0.02, 0.05, 0.1) for n in range(0, 31)), 'l12[9]', 'the loop is B0 (1 + r)^n')
check((1000 * 1.05 + 100) * 1.05 + 100 == 1307.5 and (1100 * 1.05 + 100) * 1.05 == 1317.75 and 1000 * 1.05 ** 2 + 200 == 1302.5 and round((500 * 1.04 + 500) * 1.04 + 500, 2) == 1560.8, 'l12[3]', 'deposits')
check(f'{0.0128:.2%}' == '1.28%' and [f'{x:.2%}' for x in [(102.5 - 101.2) / 101.2, (99.8 - 102.5) / 102.5, (100.4 - 99.8) / 99.8, (101.1 - 100.4) / 100.4]] == ['1.28%', '-2.63%', '0.60%', '0.70%']
      and (245.0 - 250.0) / 250.0 == -0.02 and abs((101.2 - 102.5) / 102.5) < 0.013, 'l12[10]', 'returns as percentages')
check(round(1500 * 1.02 ** 3, 3) == 1591.812 and round(1500 * 1.02 ** 4 - 1500 * 1.02 ** 3, 2) == 31.84, 'review-3[3]', 'fourth year adds 31.84')
check(round(303.5 / 2, 2) == 151.75 and round(505 / 6, 2) == 84.17 and abs(sum([101.20, 102.50, 99.80, 100.40, 101.10]) - 505.0) < 1e-9, 'review-3[4], review-3[6]', 'the wrong values the lines name')
check(f'{(98.7 - 102.4) / 102.4 * 100:+.2f}' == '-3.61' and f'{63.5 * 40 * 0.0025:.2f}' == '6.35' and f'{63.5 * 40 * 1.0025:.2f}' == '2546.35' and f'{63.5 * 40 * 0.25:.2f}' == '635.00'
      and f'{(98.2 - 104.5) * 300:+.2f}' == '-1890.00' and f'{(98.2 - 104.5) / 104.5 * 100:+.2f}' == '-6.03', 'homework-1[4..6]', 'returns and fees')
check(f'{(98.7 - 102.4) / 102.4 * 100:.2f}' == f'{(98.7 - 102.4) / 102.4 * 100:+.2f}', 'homework-1[4]', 'for a negative value .2f and +.2f print the same')
check([round(1000 * 1.02 ** k, 2) for k in range(1, 6)] == [1020.0, 1040.4, 1061.21, 1082.43, 1104.08], 'homework-2[1]', 'balances at 2%')
check((103 - 100) * 50 - 3 == 147 and (103 - 100) * 50 - 1.5 == 148.5 and (103 - 100 - 3) * 50 == 0 and (100 - 103) * 50 - 3 == -153, 'homework-3[0]', 'P&L values')
check(410 * 1.05 + 200 == 630.5, 'homework-3[6]', '630.50')
t, fee = 0, 14.99
for _ in range(2):
    t += 12 * fee; fee *= 1.03
check(f'{t:.2f}' == '365.16' and 240 + 12 * 22 == 504, 'homework-3[8]', 'contract totals')
check(sum(float(v) for v in ['24.00', '31.50', '18.25', '9.75', '42.00']) * 1.125 / 8 == 17.6484375 and 23.7 // 2 == 11.0, 'homework-2[9]', 'split bill values')

# ---------------------------------------------------------------- A2: graded keys with no snippet in the prose (canvas code, taps, boxes, concept choices)
def ans(file, idx):
    return item(file, idx)['widget'].get('answer')
def canvas_code(file, idx):
    return '\n'.join(r[1].replace(chr(0x2003), '  ') for r in item(file, idx)['canvas']['params']['rows']) + '\n'
check(run('print(6 / 2)\n')[0].strip() == key_of(item('l1-calculator', 1)) == '3.0', 'l1[1]', '6 / 2 prints 3.0')
check(20 // 6 == ans('l1-calculator', 'q-floor') == 3 and 20 - 3 * 6 == 2, 'l1[q-floor]', '20 // 6 is 3 with 2 left over')
check(key_of(item('l1-calculator', 8)) == '6 / 2' and 8 - 6 / 2 == 5.0, 'l1[8]', 'division before subtraction')
# l2 boxes: the labels of the cards each box should hold
def labels(file, idx):
    cs = item(file, idx)['canvas']['params']['containers']
    lab = {i['id']: i['label'] for c in cs for i in c.get('items', [])}
    return {k: [lab[x] for x in v] for k, v in ans(file, idx).items()}
check(labels('l2-naming-a-value', 1) == {'price': ['12'], 'qty': ['3']}, 'l2[1]', 'price 12, qty 3')
check(labels('l2-naming-a-value', 2) == {'qty': ['5'], 'tray': ['3']}, 'l2[2]', 'qty holds 5')
check(labels('l2-naming-a-value', 4) == {'a': ['7'], 'b': ['7']}, 'l2[4]', 'a 7, b 7')
check(labels('l2-naming-a-value', 5) == {'a': ['10'], 'b': ['7'], 'tray': ['7']}, 'l2[5]', 'a 10, b 7')
check(key_of(item('l2-naming-a-value', 8)).startswith('Works out total + fee'), 'l2[8]', 'right side first')
check(ans('l3-text', 1) == ['r0c1', 'r0c2', 'r0c3'] and 'GBPUSD'[0:3] == 'GBP', 'l3[1]', 'pair[0:3] keeps the first three cells')
check(key_of(item('l3-text', 8)) == '5' == str(len('ABCDEFGHIJ'[2:7])), 'l3[8]', 's[2:7] keeps 5')
rows4 = [r[0] for r in item('l4-asking-and-printing', 1)['canvas']['params']['rows']]
vals4 = ['3', int('3'), float('2.5'), '3' * 2, int('3') * 2, str(6)]
check(len(rows4) == 6 and ans('l4-asking-and-printing', 1) == [f'r{i}c1' for i, v in enumerate(vals4) if isinstance(v, str)], 'l4[1]', 'the str rows are input(), "3" * 2 and str(6)')
o, e, _, _ = run('price = float(input("Price: "))\nprint(price + 5)\n', inp='12.75'); check(o == '17.75\n', 'l4[8].right', 'float(input()) reads a price')
o, e, _, _ = run('price = int(input("Price: "))\n', inp='12.75'); check((e or '').startswith('ValueError'), 'l4[8].int', 'int(input()) fails on 12.75')
o, e, _, _ = run('price = input("Price: ")\nprint(price * 2)\nprint(price + 5)\n', inp='12.75'); check(o == '12.7512.75\n' and (e or '').startswith('TypeError'), 'l4[8].noconv', 'text repeats or fails')
check(ans('l5-decisions', 0) == ['sell'] and 97.40 < 98.00, 'l5[0]', 'sell')
check(ans('l5-decisions', 3) == ['hold'] and not 98.00 < 98.00, 'l5[3]', 'hold on the stop')
check(ans('l5-decisions', 4) == ['q1', 'q2', 'take'] and not 112.50 < 98.00 and 112.50 > 110.00, 'l5[4]', 'two questions then take profit')
def compiles(line):
    try:
        compile(line + '\n    pass\n' if line.rstrip().endswith(':') else line + '\n', 'x.py', 'exec'); return True
    except SyntaxError:
        return False
for file, idx in (('l5-decisions', 8), ('l5-decisions', 'q-reject')):
    for o_ in item(file, idx)['widget']['options']:
        bad = not compiles(norm(o_['text']))
        check(bad == (o_['id'] in ('single',) or (idx == 'q-reject' and o_.get('correct', False))), f'{file}[{idx}].{o_["id"]}', f'SyntaxError is {bad}')
check(('0' == 0) is False and key_of(item('l5-decisions', 8)) == 'if qty == 0:', 'l5[8]', 'qty == 0 asks the question')
n, seen = 0, []
while True:
    seen.append(n)
    if not n < 3: break
    n += 1
check(seen == [r[1]['answer'] for r in item('l6-until-done', 0)['widget']['rows']] == [0, 1, 2, 3], 'l6[0]', 'arrivals see 0, 1, 2, 3')
check(run(canvas_code('l6-until-done', 0))[0] == '3\n', 'l6[0].explain', 'line 4 prints 3')
check(run(canvas_code('l6-until-done', 1))[0] == '0\n1\n2\n' and key_of(item('l6-until-done', 1)).startswith('0, 1 and 2'), 'l6[1]', 'prints 0, 1, 2')
check(run(canvas_code('l6-until-done', 2))[0] == '-2\n', 'l6[2]', 'prints -2')
check(run(canvas_code('l6-until-done', 3))[0] == '3 160\n' and [(r[1]['answer'], r[2]['answer']) for r in item('l6-until-done', 3)['widget']['rows']] == [(120, 1), (140, 2), (160, 3)], 'l6[3]', 'balance and years')
def bounded(start, test, step, cap=60):
    n, out_ = start, []
    while test(n) and len(out_) < cap:
        out_.append(n); n = step(n)
    return out_
V = {'lt': bounded(1, lambda n: n < 5, lambda n: n + 1), 'right': bounded(1, lambda n: n <= 5, lambda n: n + 1),
     'zero-le': bounded(0, lambda n: n <= 5, lambda n: n + 1), 'zero-lt': bounded(0, lambda n: n < 5, lambda n: n + 1)}
check([k_ for k_, v in V.items() if v == [1, 2, 3, 4, 5]] == ['right'] and len(V['zero-le']) == 6 and V['zero-lt'] == [0, 1, 2, 3, 4], 'l6[4]', 'only n = 1 with n <= 5 prints 1 to 5')
check(len(bounded(1, lambda n: n <= 5, lambda n: n)) == 60, 'l6[5]', 'no line changes n: the loop does not end')
check(str(passes(2, 10, 2)) == key_of(item('l6-until-done', 7)) == '4', 'l6[7]', 'four passes')
E_ = {'right': bounded(10, lambda x: x > 0, lambda x: x + 1), 'down': bounded(10, lambda x: x > 0, lambda x: x - 1),
      'up': bounded(10, lambda x: x < 100, lambda x: x + 1, 200), 'double': bounded(10, lambda x: x < 1000, lambda x: x * 2)}
check(len(E_['right']) == 60 and len(E_['down']) == 10 and len(E_['up']) == 90 and len(E_['double']) == 7, 'l6[q-never-ends]', 'only x + 1 under x > 0 never ends')
b_, y_ = 1000.0, 0
while b_ < 1500:
    b_ *= 1.1; y_ += 1
check(y_ == ans('l6-until-done', 'q-to-1500') == 5, 'l6[q-to-1500]', '5 years')
W = {'lt': bounded(10, lambda n: n < 50, lambda n: n + 10), 'right': bounded(10, lambda n: n <= 50, lambda n: n + 10),
     'zero': bounded(0, lambda n: n <= 50, lambda n: n + 10), 'ne': bounded(10, lambda n: n != 55, lambda n: n + 10)}
check([k_ for k_, v in W.items() if v == [10, 20, 30, 40, 50]] == ['right'] and len(W['ne']) == 60, 'review-2[4]', 'only n <= 50 from 10; != 55 never ends')
check(ans('l7-for-each', 0) == ['c1'], 'l7[0]', 'second pass holds the second value')
rets = [0.8, -1.2, 0.0, 2.1, -0.4, 0.3]
check(ans('l7-for-each', 4) == [f'c{i}' for i, r_ in enumerate(rets) if r_ > 0], 'l7[4]', 'up days are cells 0, 3, 5')
check(list(range(1, 13)) == list(range(1, 13)) and key_of(item('l7-for-each', 7)) == 'range(1, 13)' and list(range(12))[0] == 0 and list(range(1, 12))[-1] == 11 and len(range(0, 13)) == 13, 'l7[7]', 'months 1 to 12')
check(ans('l8-many-values', 0) == ['c2'] and ans('l10-reading-errors', 0) == ['c2'] and ans('l10-reading-errors', 1) == ['c1', 'c2'], 'l8[0], l10[0], l10[1]', 'index 2; slice [1:3]')
pr, pk_, ch = [50.00, 48.00, 52.00, 52.00, 55.00, 51.00], 50.00, []
for i_, v in enumerate(pr):
    if v > pk_: pk_ = v; ch.append(f'c{i_}')
check(ans('l8-many-values', 4) == ch == ['c2', 'c4'], 'l8[4]', 'peak moves at cells 2 and 4')
check(key_of(item('l8-many-values', 8)) == '7' and list(range(8))[-1] == 7 and list(range(8))[-8] == 0, 'l8[8]', 'last index 7; [-8] is the first')
def lowest(start, prices):
    low = start
    for p_ in prices:
        if p_ < low: low = p_
    return low
ps = [12.5, 8.4, 2000000.0, 9.9]
check(lowest(ps[0], ps) == 8.4 and lowest(0, ps) == 0 and lowest(1000000, [2000000.0, 3000000.0]) == 1000000 and lowest(len(ps), ps) == 4, 'l8[q-lowest-start]', 'only prices[0] is safe')
g = {}
exec('fee = 1.50\ndef net(px):\n    left = px - fee\n    return left\ncash = net(100.00)\n', g)
check(all(k_ in g for k_ in ans('l9-packaging-steps', 6)['main']) and not any(k_ in g for k_ in ans('l9-packaging-steps', 6)['gone']) and g['cash'] == 98.5, 'l9[6]', 'fee, net, cash stay; px, left go')
g = {}
exec('def fee(px):\n    cost = px * 0.01\n    return cost\nr = fee(250.00)\n', g)
check(ans('l9-packaging-steps', 1) == {'main': ['fee'], 'call': ['px', 'cost']} and 'px' not in g and 'cost' not in g and str(g['r']) == '2.5' == key_of(item('l9-packaging-steps', 2)), 'l9[1], l9[2]', 'fee in main; px, cost in the call; prints 2.5')
check(key_of(item('l9-packaging-steps', 9)) == 'None', 'l9[9]', 'no return gives None')
check(key_of(item('l10-reading-errors', 7)) == 'ValueError', 'l10[7]', 'float("Close") is a ValueError')
rows11 = [r[1] for r in item('l11-numbers-from-a-file', 1)['canvas']['params']['rows']]
bad11 = []
for i_, ln in enumerate(rows11):
    try:
        float((ln + '\n').split(',')[1])
    except ValueError:
        bad11.append(f'r{i_}c1')
check(ans('l11-numbers-from-a-file', 1) == bad11 == ['r0c1', 'r3c1'], 'l11[1]', 'header and n/a rows stop float')
check('Wed,99.80\n'.split(',')[0] == 'Wed' and key_of(item('l11-numbers-from-a-file', 7)) == "'Wed'" and 'Wed,99.80\n'[0] == 'W', 'l11[7]', "split(',')[0] is 'Wed'")
check(abs(project(1000.0, 0.10, 2) - 1210) < 1e-9 and '1210' in key_of(item('l12-savings-script', 9)), 'l12[9]', '1210')
steps = [1000 * 1.05 ** k_ - 1000 * 1.05 ** (k_ - 1) for k_ in range(1, 11)]
check(all(b2 > a2 for a2, b2 in zip(steps, steps[1:])) and key_of(item('l12-savings-script', 1)).startswith("Each year's step is bigger"), 'l12[1]', 'steps grow')
check(key_of(item('l12-savings-script', 8)) == 'python3 savings.py', 'l12[8]', 'python3 savings.py')
F7 = {'right': 'total = price + float(fee)', 'str': 'total = str(price) + fee', 'quotes': 'total = price + "fee"', 'int': 'total = int(price) + fee'}
res7 = {k_: run(f'fee = "1.5"\nprice = 99.5\n{v}\nprint(repr(total))\n') for k_, v in F7.items()}
check(res7['right'][0] == '101.0\n' and res7['str'][0] == "'99.51.5'\n" and all((res7[k_][1] or '').startswith('TypeError') for k_ in ('quotes', 'int')), 'review-1[7]', 'only float(fee) gives a sum')
check(all(norm(o_['text']) == F7[o_['id']] for o_ in item('review-1', 7)['widget']['options']), 'review-1[7]', 'option texts as audited')
pr = [1.0, 2.0, 3.0]
ok7 = {}
for o_ in item('homework-2', 7)['widget']['options']:
    try:
        g = {'prices': pr, 'seen': []}; exec(norm(o_['text']) + '\n    seen.append(prices[i])\n', g); ok7[o_['id']] = g['seen'] == pr
    except IndexError:
        ok7[o_['id']] = False
check(ok7 == {'right': True, 'skip': False, 'over': False, 'shifted': False}, 'homework-2[7]', f'only range(len(prices)) visits every index: {ok7}')
def kind(line):
    try:
        float(line.split(',')[1]); return 'ok'
    except Exception as e_:
        return type(e_).__name__
check(kind('\n') == 'IndexError' and kind('Day,Close\n') == 'ValueError' and kind('Wed,n/a\n') == 'ValueError', 'homework-3[4]', 'a line with no comma gives the IndexError')
check(ans('homework-3', 6) == 630.5 and ((0 * 1.05 + 200) * 1.05 + 200) * 1.05 + 200 == 630.5, 'homework-3[6]', '630.50')
check('Year 3' in key_of(item('l12-savings-script', 6)) and key_of(item('review-3', 7)).startswith('Open the file with "w" once'), 'l12[6], review-3[7]', 'open once')

print(f'{count[0]} checks, {len(fails)} failing, {len(notes)} notes (imprecise rules), Python {sys.version.split()[0]}, strict tracebacks: {STRICT_TB}')
for n in notes:
    print(n)
for f in fails:
    print(f)
sys.exit(1 if fails else 0)
