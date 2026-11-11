"""Delta read, session AA: the constraints the `py` fix pass added, held against the tests.

Run from the repo root with the scratchpad venv Python.
"""
import datetime
import importlib.util
import json
import os
import re
import sys
import warnings

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
D = 'app/content/drills/'
bad = 0


def check(name, ok, detail=''):
    global bad
    print(('ok   ' if ok else 'FAIL ') + name + (f' | {detail}' if detail else ''))
    bad += not ok


def cases(i):
    d = json.load(open(D + i + '.json'))
    return d, d.get('examples', []) + d['tests']


# py-weekly-range: "on weekdays only". Every literal date in a call is a weekday; `daily` uses bdate_range.
d, cs = cases('py-weekly-range')
dates = re.findall(r'\d{4}-\d{2}-\d{2}', ' '.join(c['call'] for c in cs))
wk = [x for x in dates if datetime.date.fromisoformat(x).weekday() >= 5]
check('weekly-range: no weekend date in any call', not wk, wk)

# py-guarded-returns: no text is 'nan' or 'inf' (any case, signed, 'infinity')
d, cs = cases('py-guarded-returns')
texts = re.findall(r"'([^']*)'", ' '.join(c['call'] for c in cs))
odd = [t for t in texts if re.fullmatch(r'\s*[+-]?(nan|inf|infinity)\s*', t, re.I)]
check('guarded-returns: no nan or inf text in any call', not odd, odd)
ns = {}
exec(d['solution'], ns)
check("guarded-returns: ' 4.80 ' is a number and '1,200.00' is bad, as the brief now says",
      ns['guarded_returns']([(' 4.80 ', '4.92'), ('1,200.00', '5')]) == ([4.92 / 4.8 - 1], 1, 0))

# py-month-grid and py-growth-curve: every return at least -1 (or None for the curve)
for i in ('py-month-grid', 'py-growth-curve'):
    d, cs = cases(i)
    nums = [float(x) for c in cs for x in re.findall(r'(?<![\w.])-\d+\.?\d*', c['call'])]
    check(f'{i}: no return below -1 in a literal', all(x >= -1 for x in nums), sorted(set(nums))[:3])

# py-paired-returns tests[10]: 10,000 distinct valid dates, in order
d, cs = cases('py-paired-returns')
keys = ['%04d-%02d-%02d' % (2000 + i // 336, 1 + i // 28 % 12, 1 + i % 28) for i in range(10000)]
ok = len(set(keys)) == 10000 and keys == sorted(keys)
try:
    [datetime.date.fromisoformat(k) for k in keys]
except ValueError:
    ok = False
check('paired-returns: tests[10] keys are 10,000 real dates in rising order', ok and "'%04d-%02d-%02d'" in d['tests'][10]['call'])

# py-fx-to-pounds notes[1]: flat rates on a one-day table are right; on a square table wrong without error; else raises
import numpy as np
flat = lambda p, r: np.asarray(p, float) * np.asarray(r, float)
right = lambda p, r: np.asarray(p, float) * np.asarray(r, float).reshape(len(r), 1)
one = ([[100, 250, 40]], [0.8])
sq = ([[1, 2], [3, 4]], [0.5, 2.0])
rect = ([[1, 2, 3], [4, 5, 6]], [0.5, 2.0])
raised = False
try:
    flat(*rect)
except ValueError:
    raised = True
check('fx-to-pounds notes[1]: one-day right, square wrong, 2 by 3 raises',
      (flat(*one) == right(*one)).all() and not (flat(*sq) == right(*sq)).all() and raised)
# "on most other shapes it raises": the flat product also runs, wrongly, on any table with one share
col = ([[1], [2], [3]], [0.5, 2.0, 4.0])
check('fx-to-pounds notes[1]: a one-share table gives a 3 by 3 result with no error (not named in the note)',
      flat(*col).shape == (3, 3))

# py-wide-to-long: splitlines and StringIO readers agree on every case
import csv
import io
d, cs = cases('py-wide-to-long')
texts = []
for c in cs:
    m = re.search(r'wide_to_long\((.*)\)', c['call'], re.S)
    try:
        texts.append(eval(m.group(1)))
    except Exception:
        pass
same = all(list(csv.reader(t.splitlines())) == list(csv.reader(io.StringIO(t))) for t in texts if isinstance(t, str))
check(f'wide-to-long: both readers give the same rows on {len(texts)} literal texts', same and len(texts) >= 8)

# py-format-pence brief: the two f-string examples
check("format-pence brief: f'{1234567:,}' and f'{5:02d}'", f'{1234567:,}' == '1,234,567' and f'{5:02d}' == '05')
# py-best-desk brief: argmax example
check('best-desk brief: argmax example is [1, 0]', np.argmax(np.array([[1, 5, 5], [7, 2, 3]]), axis=1).tolist() == [1, 0])

# reports: difficulty in the two pack reports against the files
for rep in ('docs/reports/drills-py-a.md', 'docs/reports/drills-py-b.md'):
    txt = open(rep).read()
    off = []
    for line in txt.splitlines():
        m = re.match(r'\|\s*`?(py-[a-z-]+)`?\s*\|', line)
        if not m or not os.path.exists(D + m.group(1) + '.json'):
            continue
        dd = json.load(open(D + m.group(1) + '.json'))
        cells = [c.strip() for c in line.strip('|').split('|')]
        if str(dd['difficulty']) not in cells or str(len(dd['tests'])) not in cells:
            off.append((m.group(1), dd['difficulty'], len(dd['tests']), cells[1:6]))
    check(f'{rep}: rows carry the file difficulty and test count', not off, off)

print('problems:', bad)
sys.exit(1 if bad else 0)
