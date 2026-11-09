"""Recompute every number in py-found homework-1 item h-overnight-gaps (performance task, code).

Run from anywhere with any Python 3 (standard library only):
    python3 docs/reports/py-found-1-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (two comprehensions over zip(days, days[1:])).
Route B is an independent index loop in this file, with every gap also worked in exact
fractions. Each test expectation must match both routes under the engine's comparison
(a copy of code.js __zq_cmp: isclose through lists and tuples, else ==). The starter must
fail, and each planted beginner slip must fail at least one hidden test.
"""
import contextlib, io, json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/py-found/homework-1.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-overnight-gaps')
w = item['widget']
fails = []


def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)


def close(x, y):
    """code.js __zq_cmp, isclose branch."""
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
    if isinstance(x, str) and not isinstance(y, str):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def judge(got, case, ns):
    exp = eval(case['expect'], ns)
    if case.get('compare', 'equal') == 'isclose':
        return close(got, exp)
    return bool(got == exp)


def run_tests(code, cases=None):
    res = []
    for t in (cases or w['tests']):
        ns = {'__learner_source__': code}
        try:
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            with contextlib.redirect_stdout(io.StringIO()):
                got = eval(t['call'], ns)
            res.append(judge(got, t, ns))
        except Exception as e:
            res.append(type(e).__name__)
    return res


SOL = w['solution']

REF = '''def overnight_gaps(days, limit):
    gaps = []
    flagged = []
    for i in range(1, len(days)):
        prev_close = days[i - 1][2]
        gap = (days[i][1] - prev_close) / prev_close
        gaps.append(gap)
        if gap > limit or gap < -limit:
            flagged.append(days[i][0])
    return gaps, flagged
'''
# Route B uses append on purpose, so it is judged on every test but the source check (test 10),
# and that test's value part is judged separately below.

BUGS = {
    'same-day close (o_t - c_t) / c_t':
        'def overnight_gaps(days, limit):\n    gaps = [(d[1] - d[2]) / d[2] for d in days[1:]]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > limit]\n    return gaps, flagged\n',
    'divides by the open':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[2]) / t[1] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > limit]\n    return gaps, flagged\n',
    'previous open, not previous close':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[1]) / b[1] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > limit]\n    return gaps, flagged\n',
    'no abs (rises only)':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if g > limit]\n    return gaps, flagged\n',
    'flags the day before':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [b[0] for b, t in zip(days, days[1:]) if abs((t[1] - b[2]) / b[2]) > limit]\n    return gaps, flagged\n',
    'off by one: range(len(days)) wraps to days[-1]':
        'def overnight_gaps(days, limit):\n    gaps = [(days[i][1] - days[i - 1][2]) / days[i - 1][2] for i in range(len(days))]\n    flagged = [days[i][0] for i in range(len(days)) if abs(gaps[i]) > limit]\n    return gaps, flagged\n',
    'off by one: range(len(days) - 1) drops the last gap':
        'def overnight_gaps(days, limit):\n    gaps = [(days[i][1] - days[i - 1][2]) / days[i - 1][2] for i in range(1, len(days) - 1)]\n    flagged = [days[i + 1][0] for i in range(len(gaps)) if abs(gaps[i]) > limit]\n    return gaps, flagged\n',
    '>= limit (a zero gap flagged at limit 0)':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) >= limit]\n    return gaps, flagged\n',
    'gaps in per cent':
        'def overnight_gaps(days, limit):\n    gaps = [100 * (t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > 100 * limit]\n    return gaps, flagged\n',
    'empty input: reads days[0] first':
        'def overnight_gaps(days, limit):\n    prev = days[0][2]\n    gaps = [(t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > limit]\n    return gaps, flagged\n',
    'prints the result instead of returning it':
        'def overnight_gaps(days, limit):\n    gaps = [(t[1] - b[2]) / b[2] for b, t in zip(days, days[1:])]\n    flagged = [d[0] for d, g in zip(days[1:], gaps) if abs(g) > limit]\n    print(gaps, flagged)\n',
    'loop with append (no comprehension)': REF,
}

n = len(w['tests'])
r = run_tests(SOL)
check(f'A solution passes all {n} tests', all(x is True for x in r), str(r))
r = run_tests(REF)
check('B index loop passes tests 1 to 9', all(x is True for x in r[:9]), str(r))
check('B index loop fails test 10 only (it appends)', r[9] is not True)
ns = {}; exec(REF, ns); exec(w['tests'][9]['setup'], ns)
check('B: value part of test 10 holds', ns['overnight_gaps'](ns['W'], 0.01)[1] == ['Tue', 'Fri'])
r = run_tests(w['examples'][0:1] and SOL, w['examples'])
check('solution passes the example', all(x is True for x in r))
check('example equals test 1', w['examples'][0] == w['tests'][0])

r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'slip "{name}" caught', bool(bad), f'fails tests {bad}')

# byKey: each line names a slip that fails at that test
for key, name in (('test-2', 'divides by the open'), ('test-3', 'no abs (rises only)'), ('test-3', 'flags the day before'),
                  ('test-4', 'off by one: range(len(days)) wraps to days[-1]'), ('test-5', '>= limit (a zero gap flagged at limit 0)'),
                  ('test-9', 'empty input: reads days[0] first'), ('test-10', 'loop with append (no comprehension)')):
    check(f'byKey {key} present', key in item['feedback']['byKey'])
    check(f'slip "{name}" fails {key}', run_tests(BUGS[name])[int(key[5:]) - 1] is not True)

# Every stated number, by exact fractions (route C) against the floats the tests expect.
Wd = [("Mon", F('100.0'), F('101.0')), ("Tue", F('103.02'), F('102.0')), ("Wed", F('101.49'), F('100.5')),
      ("Thu", F('100.5'), F('99.0')), ("Fri", F('97.0'), F('98.0'))]
gW = [(t[1] - b[2]) / b[2] for b, t in zip(Wd, Wd[1:])]
check('W gaps exactly 1/50, -1/200, 0, -2/99', gW == [F(1, 50), F(-1, 200), F(0), F(-2, 99)], str(gW))
check('test 2 expect matches the fractions', close([float(x) for x in gW], eval(w['tests'][1]['expect'])))
check('-2/99 = -0.020202020202020204 as a float', float(F(-2, 99)) == -0.020202020202020204)
check('W limit 0.01: Tue and Fri', [d[0] for d, g in zip(Wd[1:], gW) if abs(g) > F(1, 100)] == ['Tue', 'Fri'])
check('W limit 0: Tue, Wed, Fri', [d[0] for d, g in zip(Wd[1:], gW) if abs(g) > 0] == ['Tue', 'Wed', 'Fri'])
check('W limit 0.05: none', [d[0] for d, g in zip(Wd[1:], gW) if abs(g) > F(5, 100)] == [])
Vd = [("02 Mar", F('250.0'), F('248.0')), ("03 Mar", F('255.44'), F('256.0')), ("04 Mar", F('245.76'), F('247.0')),
      ("05 Mar", F('247.0'), F('250.0')), ("06 Mar", F('251.0'), F('249.5')), ("09 Mar", F('249.5'), F('251.0'))]
gV = [(t[1] - b[2]) / b[2] for b, t in zip(Vd, Vd[1:])]
check('V gaps exactly 3/100, -4/100, 0, 4/1000, 0', gV == [F(3, 100), F(-4, 100), F(0), F(4, 1000), F(0)], str(gV))
check('V limit 0.025: 03 Mar and 04 Mar', [d[0] for d, g in zip(Vd[1:], gV) if abs(g) > F(25, 1000)] == ['03 Mar', '04 Mar'])
check('test 7 expect matches the fractions', close(([float(x) for x in gV], ['03 Mar', '04 Mar']), eval(w['tests'][6]['expect'])))
Ed = [("Mon", F(50), F(50)), ("Tue", F(51), F(52)), ("Wed", F(52), F('52.5'))]
gE = [(t[1] - b[2]) / b[2] for b, t in zip(Ed, Ed[1:])]
check('example gaps exactly 1/50 and 0', gE == [F(1, 50), F(0)])
check('feedback: Friday fell about 2%', abs(float(gW[3]) + 0.02) < 0.001)
check('feedback: 5 days give 4 gaps', len(Wd) == 5 and len(gW) == 4)
check('W floats: no gap sits on a limit used in tests 3, 5 and 6 except the exact zero',
      all(abs(abs(float(g)) - L) > 1e-6 for g in gW for L in (0.01, 0.05)) and float(gW[2]) == 0.0)

n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 10, examples 1, tests > examples', (n_t, n_e) == (10, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
