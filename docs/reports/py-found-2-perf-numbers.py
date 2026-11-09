"""Recompute every number in py-found homework-2 item h-book-weights (performance task, code).

Run from anywhere with any Python 3 (standard library only):
    python3 -I docs/reports/py-found-2-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (one pass for the total with an early None, one to fill a new dict).
Route B is written differently in this file: it values every holding first into a list of
(ticker, value) pairs and divides at the end. Route C works each weight in exact fractions.
Each test expectation must match both code routes under the engine's comparison (a copy of
code.js __zq_cmp: isclose through lists and tuples, else ==). The starter must fail, and each
planted beginner slip must fail at least one hidden test.
"""
import contextlib, io, json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/py-found/homework-2.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-book-weights')
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
            with contextlib.redirect_stdout(io.StringIO()):
                exec(code, ns)
                if t.get('setup'):
                    exec(t['setup'], ns)
                got = eval(t['call'], ns)
            res.append(judge(got, t, ns))
        except Exception as e:
            res.append(type(e).__name__)
    return res


SOL = w['solution']
REF = '''def book_weights(book, prices, cash=0.0):
    values = []
    for ticker in book:
        price = prices.get(ticker)
        if price is None:
            return None
        values.append((ticker, book[ticker] * price))
    total = cash + sum(v for _, v in values)
    if total == 0:
        return None
    out = {}
    for ticker, v in values:
        out[ticker] = v / total
    return out
'''


def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)


BUGS = {
    'missing price priced at 0 (get with 0)': variant('        if ticker not in prices:\n            return None\n        total = total + qty * prices[ticker]',
                                                       '        total = total + qty * prices.get(ticker, 0)').replace('qty * prices[ticker] / total', 'qty * prices.get(ticker, 0) / total'),
    'missing price skipped': variant('        if ticker not in prices:\n            return None\n        total = total + qty * prices[ticker]',
                                     '        if ticker in prices:\n            total = total + qty * prices[ticker]').replace(
                                     '        weights[ticker] = qty * prices[ticker] / total', '        if ticker in prices:\n            weights[ticker] = qty * prices[ticker] / total'),
    'no zero-total check (ZeroDivisionError)': variant('    if total == 0:\n        return None\n', ''),
    'empty book returns None even with cash': variant('    total = cash\n', '    if len(book) == 0:\n        return None\n    total = cash\n'),
    'zero check on holdings before cash': variant('    total = cash\n', '    total = 0.0\n').replace(
                                     '    if total == 0:\n        return None\n', '    if total == 0:\n        return None\n    total = total + cash\n'),
    'cash ignored': variant('    total = cash\n', '    total = 0.0\n'),
    'cash given a weight of its own': variant('    return weights\n', '    weights["CASH"] = cash / total\n    return weights\n'),
    'abs(qty), as for volume': variant('total = total + qty * prices[ticker]', 'total = total + abs(qty) * prices[ticker]').replace(
                                     'qty * prices[ticker] / total', 'abs(qty) * prices[ticker] / total'),
    'weights by shares, not value': '''def book_weights(book, prices, cash=0.0):
    total = 0
    for ticker, qty in book.items():
        if ticker not in prices:
            return None
        total = total + qty
    if total + cash == 0:
        return None
    weights = {}
    for ticker, qty in book.items():
        weights[ticker] = qty / (total + cash)
    return weights
''',
    'floor division //': variant('qty * prices[ticker] / total', 'qty * prices[ticker] // total'),
    'mutates book in place': '''def book_weights(book, prices, cash=0.0):
    total = cash
    for ticker in book:
        if ticker not in prices:
            return None
        book[ticker] = book[ticker] * prices[ticker]
        total = total + book[ticker]
    if total == 0:
        return None
    for ticker in book:
        book[ticker] = book[ticker] / total
    return book
''',
    'adds cash to book as a ticker': '''def book_weights(book, prices, cash=0.0):
    book["CASH"] = 1
    prices["CASH"] = cash
    total = 0.0
    for ticker, qty in book.items():
        if ticker not in prices:
            return None
        total = total + qty * prices[ticker]
    if total == 0:
        return None
    weights = {}
    for ticker, qty in book.items():
        if ticker != "CASH":
            weights[ticker] = qty * prices[ticker] / total
    return weights
''',
    'loops over prices, not book': '''def book_weights(book, prices, cash=0.0):
    total = cash
    for ticker, price in prices.items():
        total = total + book.get(ticker, 0) * price
    if total == 0:
        return None
    weights = {}
    for ticker, price in prices.items():
        weights[ticker] = book.get(ticker, 0) * price / total
    return weights
''',
    'return inside the second loop': variant('        weights[ticker] = qty * prices[ticker] / total\n    return weights\n',
                                             '        weights[ticker] = qty * prices[ticker] / total\n        return weights\n'),
    'prints the weights instead of returning them': variant('    return weights\n', '    print(weights)\n'),
}

n = len(w['tests'])
for name, code in (('A solution', SOL), ('B value list', REF)):
    r = run_tests(code)
    check(f'{name} passes all {n} tests', all(x is True for x in r), str(r))
check('solution passes the example', all(x is True for x in run_tests(SOL, w['examples'])))
check('example equals test 1', w['examples'][0] == w['tests'][0])
r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'slip "{name}" caught', bool(bad), f'fails tests {bad}')

for key, name in (('test-2', 'cash ignored'), ('test-2', 'loops over prices, not book'), ('test-4', 'missing price priced at 0 (get with 0)'),
                  ('test-4', 'missing price skipped'), ('test-5', 'no zero-total check (ZeroDivisionError)'), ('test-5', 'empty book returns None even with cash'),
                  ('test-6', 'zero check on holdings before cash'), ('test-7', 'abs(qty), as for volume'), ('test-8', 'floor division //'),
                  ('test-9', 'mutates book in place')):
    check(f'byKey {key} present', key in item['feedback']['byKey'])
    check(f'slip "{name}" fails {key}', run_tests(BUGS[name])[int(key[5:]) - 1] is not True)

# Route C: exact fractions for every expected weight and every figure in the feedback.
def frac_weights(book, prices, cash):
    tot = F(cash) + sum(F(q) * F(str(prices[t])) for t, q in book.items())
    return None if tot == 0 else sorted((t, F(q) * F(str(prices[t])) / tot) for t, q in book.items())

B = {"VOD": 1000, "BP": 300, "AZN": 10}
P = {"VOD": 0.75, "BP": 5.0, "AZN": 120.0, "HSBA": 6.5}
cases = [
    (1, ({"VOD": 1000, "BP": 300}, {"VOD": 0.75, "BP": 5.0}, 0), [('BP', F(2, 3)), ('VOD', F(1, 3))]),
    (2, (B, P, '550'), [('AZN', F(3, 10)), ('BP', F(3, 8)), ('VOD', F(3, 16))]),
    (3, (B, P, 0), [('AZN', F(1200, 3450)), ('BP', F(1500, 3450)), ('VOD', F(750, 3450))]),
    (7, ({"BP": 300, "SHEL": -20}, {"BP": 5.0, "SHEL": 25.0}, '500'), [('BP', F(1)), ('SHEL', F(-1, 3))]),
    (8, ({"VOD": 3, "BP": 1}, {"VOD": 2, "BP": 4}, 4), [('BP', F(4, 14)), ('VOD', F(6, 14))]),
]
for k, args, want in cases:
    got = frac_weights(*args)
    check(f'test {k}: exact weights', got == want, str(got))
    check(f'test {k}: expect string matches the fractions', close([(t, float(x)) for t, x in want], eval(w['tests'][k - 1]['expect'])))
check('test 4: VOD alone with £250.00 cash is 0.75', frac_weights({"VOD": 1000}, P, 250) == [('VOD', F(3, 4))])
check('test 6: hedged book totals 0 without cash', frac_weights({"BP": 300, "SHEL": -60}, {"BP": 5.0, "SHEL": 25.0}, 0) is None)
check('test 6: with £1,000 cash the weights are 1.5 and -1.5',
      frac_weights({"BP": 300, "SHEL": -60}, {"BP": 5.0, "SHEL": 25.0}, 1000) == [('BP', F(3, 2)), ('SHEL', F(-3, 2))])
check('test 10: once TSCO is priced at 2.5 the weights are 0.4 and 0.6',
      frac_weights({"VOD": 1000, "TSCO": 200}, {"VOD": 0.75, "TSCO": 2.5}, 0) == [('TSCO', F(2, 5)), ('VOD', F(3, 5))])
check('test 8 feedback: the total is 14', 3 * 2 + 1 * 4 + 4 == 14)
check('test 2 feedback: total £4,000.00, VOD £750.00 is 0.1875', 1000 * F('0.75') + 300 * 5 + 10 * 120 + 550 == 4000 and F(750, 4000) == F('0.1875'))
check('test 5 feedback: £100.00 cash, no holdings, gives {}', run_tests(SOL, [w['tests'][4]])[0] is True)
check('weights with cash sum to 1 minus the cash share (test 2)', sum(x for _, x in frac_weights(B, P, 550)) == 1 - F(550, 4000))

n_t, n_e = len(w['tests']), len(w['examples'])
check('tests 10, examples 1, tests > examples', (n_t, n_e) == (10, 1) and n_t > n_e)
check('how states the test count', f'runs {n_t} hidden tests' in w['how'])
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)
check('solution uses no comprehension of a dict (not taught)', '{' not in SOL.split('weights = {}')[1])

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
