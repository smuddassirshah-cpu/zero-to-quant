"""first-python level 2 performance task (h-split-bill): every number recomputed.

Run from the repo root: python3 -I docs/reports/first-python-2-perf-numbers.py
Route A runs the item's own solution in floats. Route B recomputes each share
exactly with Fraction from the call's arguments. The starter and twelve
planted beginner slips are run against every hidden test; each slip must fail,
and its first failing test must carry a byKey line. Exits 1 on any failure.
"""
import json
import math
import os
import re
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'first-python', 'homework-2.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-split-bill')
w = item['widget']
fails = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)


def run(src, case):
    """Return (passed, actual) for one function-mode case, as the widget grades it."""
    ns = {}
    try:
        exec(src, ns)
    except Exception as e:  # the whole program failed: key "error"
        return None, 'load error ' + type(e).__name__
    try:
        got = eval(case['call'], ns)
    except Exception as e:
        return False, type(e).__name__
    want = eval(case['expect'])
    try:
        ok = got is not None and not isinstance(got, (str, bool)) and math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        ok = False
    return ok, got


def grade(src):
    """First failing key as the widget gives it: 'error', 'test-k' or None."""
    for k, case in enumerate(w['tests'], 1):
        ok, got = run(src, case)
        if ok is None:
            return 'error', got
        if not ok:
            return f'test-{k}', got
    return None, None


# Route B: the share in exact arithmetic.
def exact_share(prices, people):
    total = sum(Fraction(p) for p in prices)
    if people >= 6:
        total *= Fraction(9, 8)  # 12.5% charge: 1 + 1/8
    return total / people


def args_of(call):
    m = re.fullmatch(r'split_bill\((\[.*\]), (\d+)\)', call)
    return json.loads(m.group(1)), int(m.group(2))


# 1. Shape
check(item.get('performance') == 'code', 'performance is code')
check(len(w['tests']) >= 3 and len(w['tests']) > len(w['examples']), f"{len(w['tests'])} tests > {len(w['examples'])} examples")
check(len(doc['items']) <= 12, f"homework holds {len(doc['items'])} items (limit 12)")
check(sum(1 for i in doc['items'] if i.get('performance')) == 1, 'one performance item in homework-2')
check(not re.search(r'\bdef\b', w['starter'].split('\n', 1)[1]), 'starter body defines nothing (def line given, as every L2 code screen)')

# 2. Every expect, by both routes
for k, case in enumerate(w['examples'] + w['tests']):
    prices, people = args_of(case['call'])
    a_ok, a = run(w['solution'], case)
    b = exact_share(prices, people)
    want = eval(case['expect'])
    check(bool(a_ok), f"route A solution {case['call'][:48]}... = {a}")
    check(math.isclose(float(b), want, rel_tol=1e-12), f"route B exact {b} = {float(b)} matches expect {want}")
check(all(c in w['tests'] for c in w['examples']), 'the example is also a hidden test')

# 3. Starter fails every test
results = [run(w['starter'], c)[0] for c in w['tests']]
check(not any(results), f'starter fails all {len(results)} tests')

# 4. Planted slips
SOL = w['solution']
slips = {
    'price left as text': SOL.replace('float(p)', 'p'),
    'int() on a price': SOL.replace('float(p)', 'int(p)'),
    'integer division //': SOL.replace('total / people', 'total // people'),
    'strict > 6 at the edge': SOL.replace('people >= 6', 'people > 6'),
    'loop misses the first price': SOL.replace('    for p in prices:\n        total = total + float(p)',
                                               '    for i in range(1, len(prices)):\n        total = total + float(prices[i])'),
    'loop misses the last price': SOL.replace('    for p in prices:\n        total = total + float(p)',
                                              '    for i in range(len(prices) - 1):\n        total = total + float(prices[i])'),
    'prints the share': SOL.replace('    share = total / people\n', '    print(total / people)\n'),
    'adds 0.125 not 12.5%': SOL.replace('total * 1.125', 'total + 0.125'),
    'charge alone, not bill plus charge': SOL.replace('total * 1.125', 'total * 0.125'),
    'charge counted by dishes': SOL.replace('people >= 6', 'len(prices) >= 6'),
    'charge for every group': SOL.replace('    if people >= 6:\n        total', '    total'),
    'divides by the number of dishes': SOL.replace('total / people', 'total / len(prices)'),
}
for name, src in slips.items():
    check(src != SOL, f'slip "{name}" changes the solution')
    key, got = grade(src)
    check(key is not None, f'slip "{name}" fails, first at {key} (got {got})')
    check(key in item['feedback']['byKey'], f'slip "{name}": byKey has a line for {key}')

# 5. Numbers stated in the prose and feedback
fb = item['feedback']['byKey']
check(math.isclose(60.0 / 3, 20.0) and float(sum(Fraction(p) for p in ["10", "20", "30"])) == 60.0, 'test-1 line: £60.00 three ways is £20.00')
check(math.isclose(23.70 / 2, 11.85) and exact_share(["12.50", "8.00", "3.20"], 2) == Fraction(237, 20), 'test-2 line: £11.85 each')
check(23.70 // 2 == 11.0, 'test-2 line: // gives 11.0')
check(exact_share(["16.00"] * 6, 6) == 18 and 96 * 1.125 / 6 == 18.0, 'test-3 line: £18.00 each at 6 people')
check(Fraction(1) + Fraction(125, 1000) == Fraction(9, 8) == Fraction('1.125'), '12.5% charge multiplies by 1.125')
check('£60.00' in fb['test-1'] and '£20.00' in fb['test-1'] and '£11.85' in fb['test-2'] and '£18.00' in fb['test-3'] and '1.125' in fb['test-3'], 'stated figures present in feedback')
p4, n4 = args_of(w['tests'][3]['call'])
check(n4 == 8 and len(p4) == 5, 'test-4 line: 8 people, 5 dishes')
check('8 hidden tests' in w['how'] and 'eight' in item['feedback']['correct'], 'counts in how and correct match 8 tests')

print(f'\n{len(fails)} failure(s)')
raise SystemExit(1 if fails else 0)
