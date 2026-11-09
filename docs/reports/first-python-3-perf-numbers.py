"""first-python level 3 performance task (h-contract-cost): every number recomputed.

Run from the repo root: python3 -I docs/reports/first-python-3-perf-numbers.py
Route A runs the item's own solution in floats, as the widget's script mode
does (the whole program runs afresh for every case, then the call). Route B is
the closed form 12 f ((1 + r)^n - 1) / r in exact Fraction arithmetic (12 f n
when r = 0). The starter and planted beginner slips run against every test;
each slip must fail, and its first failing test must carry a byKey line.
Exits 1 on any failure.
"""
import contextlib
import io
import json
import math
import os
import re
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'first-python', 'homework-3.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-contract-cost')
w = item['widget']
fb = item['feedback']['byKey']
fails = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)


def norm(t):
    lines = [l.rstrip() for l in t.split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def run(src, case):
    """(passed, actual) for one script-mode case; None when the code does not compile."""
    try:
        code = compile(src, 'main.py', 'exec')
    except SyntaxError:
        return None, 'SyntaxError'
    ns, out = {'__name__': '__main__'}, io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(code, ns)
    except Exception as e:
        return False, type(e).__name__
    if case.get('compare') == 'stdout':
        return norm(out.getvalue()) == norm(case['expect']), out.getvalue()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            got = eval(case['call'], ns)
    except Exception as e:
        return False, type(e).__name__
    want = eval(case['expect'])
    ok = isinstance(got, (int, float)) and not isinstance(got, bool) and math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12)
    return ok, got


def grade(src):
    for k, case in enumerate(w['tests'], 1):
        ok, got = run(src, case)
        if ok is None:
            return 'error', got
        if not ok:
            return f'test-{k}', got
    return None, None


def exact_total(fee, rise, years):
    f, r = Fraction(fee), Fraction(rise) / 100
    if r == 0:
        return 12 * f * years
    return 12 * f * ((1 + r) ** years - 1) / r


def args_of(call):
    m = re.fullmatch(r'contract_cost\("([\d.]+)", "([\d.]+)", (\d+)\)', call)
    return m.group(1), m.group(2), int(m.group(3))


# 1. Shape
check(item.get('performance') == 'code', 'performance is code')
check(len(w['tests']) >= 3 and len(w['tests']) > len(w['examples']), f"{len(w['tests'])} tests > {len(w['examples'])} examples")
check(len(doc['items']) <= 12, f"homework holds {len(doc['items'])} items (limit 12)")
check(sum(1 for i in doc['items'] if i.get('performance')) == 1, 'one performance item in homework-3')
check(w['starter'].count('def ') == 1 and 'pass' in w['starter'], 'starter is a stub')

# 2. Every expect, by both routes
for case in w['examples'] + w['tests']:
    if case.get('compare') == 'stdout':
        continue
    a_ok, a = run(w['solution'], case)
    b = exact_total(*args_of(case['call']))
    want = eval(case['expect'])
    check(bool(a_ok), f"route A solution {case['call']} = {a}")
    check(math.isclose(float(b), want, rel_tol=1e-12, abs_tol=1e-12), f"route B closed form {float(b)} matches expect {want}")
stdout_case = w['tests'][-1]
two_year = exact_total('14.99', '3', 2)
check(two_year == Fraction(3651564, 10000), f'form contract over 2 years is exactly {float(two_year)}')
check(stdout_case['expect'] == f'Total: £{float(two_year):.2f}\n', 'stdout expect is the 2-year total to the penny')
check(bool(run(w['solution'], stdout_case)[0]), 'route A: the solution prints the stdout line')

# 3. Starter fails every test
results = [run(w['starter'], c)[0] for c in w['tests']]
check(not any(results), f'starter fails all {len(results)} tests')

# 4. Planted slips
SOL = w['solution']
LOOP = '    for year in range(years):\n'
slips = {
    'texts never converted': SOL.replace('    fee = float(fee)\n    rise = float(rise)\n', ''),
    'int() on the texts': SOL.replace('float(fee)', 'int(fee)').replace('float(rise)', 'int(rise)'),
    'int() on the rise only': SOL.replace('float(rise)', 'int(rise)'),
    'prints instead of returning': SOL.replace('    return total\n', '    print(total)\n'),
    'integer division //': SOL.replace('rise / 100', 'rise // 100'),
    'range one year short': SOL.replace(LOOP, '    for year in range(1, years):\n'),
    'range one year long': SOL.replace(LOOP, '    for year in range(years + 1):\n'),
    'raises before paying': SOL.replace('        total = total + 12 * fee\n        fee = fee * (1 + rise / 100)\n',
                                        '        fee = fee * (1 + rise / 100)\n        total = total + 12 * fee\n'),
    'return inside the loop': SOL.replace('    return total\n', '        return total\n'),
    'fee becomes the rise alone': SOL.replace('fee * (1 + rise / 100)', 'fee * rise / 100'),
    'one payment a year': SOL.replace('12 * fee', 'fee'),
    'fee rises by rise pounds': SOL.replace('fee * (1 + rise / 100)', 'fee + rise'),
    'script prints without :.2f': SOL.replace(':.2f}', '}'),
    'script prints 1 year': SOL.replace('form_rise, 2)', 'form_rise, 1)'),
    'script prints nothing': SOL.split('\nprint(')[0] + '\n',
}
for name, src in slips.items():
    check(src != SOL, f'slip "{name}" changes the solution')
    key, got = grade(src)
    check(key is not None, f'slip "{name}" fails, first at {key} (got {str(got).strip()[:40]})')
    check(key in fb, f'slip "{name}": byKey has a line for {key}')

# 5. Numbers stated in the prose, feedback and explanation
check(exact_total('10', '5', 1) == 120 and 12 * 10.00 == 120.0, 'test-1 line: one year at £10.00 is £120.00')
check(12 * Fraction('20.00') == 240 and Fraction('20.00') * Fraction(110, 100) == 22, 'test-2 line: £240.00, then £22.00')
check(exact_total('20.00', '10', 2) == 504 and 240 + 12 * 22 == 504, 'test-2 line: £504.00 in all')
check(10 // 100 == 0 and 12 * 20 * 2 == 480, 'test-2 line: // gives 0 and 480.0')
check(4 / 100 == 0.04 and 4 // 100 == 0, 'explain: 4 / 100 is 0.04, 4 // 100 is 0')
check(exact_total('25.00', '4', 0) == 0, 'test-6 line: 0 years costs 0')
for s in ['£120.00', '£240.00', '£22.00', '£504.00', '480.0', '240.0']:
    check(s in fb['test-1'] + fb['test-2'], f'{s} stated in feedback')
check('7 hidden tests' in w['how'] and 'seven' in item['feedback']['correct'], 'counts in how and correct match 7 tests')

print(f'\n{len(fails)} failure(s)')
raise SystemExit(1 if fails else 0)
