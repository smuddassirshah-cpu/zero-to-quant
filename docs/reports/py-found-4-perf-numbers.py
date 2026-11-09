"""Recompute every number in py-found homework-4 item h4-sweep-offers (performance task, code).

Run from anywhere with any Python 3 (standard library only):
    python3 -I docs/reports/py-found-4-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution` (sorted with a key, a generator, one pass for the average).
Route B is written differently in this file: it expands the book into one entry per share in book
order, picks shares by price with an index tie-break, and groups them back into fills; the averages
come from exact Fractions. Route C checks the stated figures (2,028, 450, 4,981, 1,100) by integer
pence arithmetic. Each test runs as the engine runs it: the prelude, the learner code, the case's
setup, then its call, judged like code.js __zq_cmp (== for equal, math.isclose rel 1e-9, or raises).
The starter must fail every test, and each planted beginner slip must fail at least one hidden test.
"""
import contextlib, io, json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/py-found/homework-4.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h4-sweep-offers')
w = item['widget']
fails = []
BOOK = [(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)]


def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)


def same(a, e, cmp):
    if isinstance(a, (list, tuple)) or isinstance(e, (list, tuple)):
        return (isinstance(a, (list, tuple)) and isinstance(e, (list, tuple)) and len(a) == len(e)
                and all(same(x, y, cmp) for x, y in zip(a, e)))
    if cmp == 'isclose':
        try:
            return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-12)
        except Exception:
            return a == e
    return bool(a == e)


def run_tests(code, cases=None):
    res = []
    for t in (cases or w['tests']):
        ns = {'__learner_source__': code}
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(w['prelude'], ns)
                exec(code, ns)
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns)
                        res.append(False)
                    except Exception as e:
                        res.append(t['expect'] in [k.__name__ for k in type(e).__mro__])
                    continue
                got = eval(t['call'], ns)
            res.append(same(got, eval(t['expect'], ns), t.get('compare', 'equal')))
        except Exception as e:
            res.append(type(e).__name__)
    return res


SOL = w['solution']
REF = '''from fractions import Fraction


def sweep_offers(qty, offers):
    if not qty > 0:
        raise ValueError("qty")
    book = list(offers)
    shares = []
    for n, (price, size) in enumerate(book):
        shares.extend([(price, n)] * size)
    chosen = []
    while shares and len(chosen) < qty:
        best = min(range(len(shares)), key=lambda i: (shares[i][0], shares[i][1]))
        chosen.append(shares.pop(best))
    i = 0
    while i < len(chosen):
        j = i
        while j < len(chosen) and chosen[j][1] == chosen[i][1]:
            j += 1
        yield chosen[i][0], j - i
        i = j


def average_price(qty, offers):
    fills = list(sweep_offers(qty, offers))
    bought = sum(s for _, s in fills)
    if bought == 0:
        return None
    return float(sum(Fraction(str(p)) * s for p, s in fills) / bought)
'''

# 1. the tests and examples are the ones the item describes
check('15 tests, at most 15', len(w['tests']) == 15)
check('2 examples, fewer than tests', len(w['examples']) == 2 and len(w['examples']) < len(w['tests']))
check('examples repeat tests 1 and 10', w['examples'][0] == w['tests'][0] and w['examples'][1] == w['tests'][9])
check('how says 15 tests', 'runs 15 hidden tests' in w['how'])
raises_at = [k + 1 for k, t in enumerate(w['tests']) if t.get('compare') == 'raises']
check('raises tests are 8, 9 and 14', raises_at == [8, 9, 14], str(raises_at))
check('how names tests 8, 9 and 14', 'Tests 8, 9 and 14' in w['how'])
check('how names test 15 spied', "test 15's `spied`" in w['how'] and 'spied(' in w['tests'][14]['call'])
check('how book is the setup book', '[(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)]' in w['how']
      and all('book = [(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)]' in t.get('setup', 'book = [(4.52, 300), (4.50, 200), (4.55, 500), (4.50, 100)]') for t in w['tests']))

# 2. solution and independent reference pass every test; starter fails every test
r = run_tests(SOL)
check('solution passes all 15', r == [True] * 15, str(r))
r = run_tests(REF)
check('reference (route B) passes all 15', r == [True] * 15, str(r))
r = run_tests(w['starter'])
check('starter fails all 15', not any(x is True for x in r), str(r))
r = run_tests(SOL, w['examples'])
check('solution passes both examples', r == [True, True])

# 3. route B and route A agree on the expects, and the expects are exact book arithmetic
ns_a, ns_b = {}, {}
exec(SOL, ns_a)
exec(REF, ns_b)
for q in (1, 100, 250, 299, 300, 301, 450, 600, 1099, 1100, 2000):
    a = list(ns_a['sweep_offers'](q, BOOK))
    b = list(ns_b['sweep_offers'](q, BOOK))
    check(f'fills agree, qty {q}', a == b, str(a))
    pa, pb = ns_a['average_price'](q, BOOK), ns_b['average_price'](q, BOOK)
    check(f'average agrees, qty {q}', math.isclose(pa, pb, rel_tol=1e-12), f'{pa} {pb}')

# 4. route C: pence integers for the stated figures
pence = [(452, 300), (450, 200), (455, 500), (450, 100)]
c450 = 450 * 200 + 450 * 100 + 452 * 150
check('450 shares cost 2,028.00', c450 == 202800, str(c450))
check('300 at 4.50 plus 150 at 4.52', 450 * 300 == 135000 and 452 * 150 == 67800)
check('test 10 expect 4.506666666666667', float(F(c450, 450 * 100)) == 4.506666666666667
      and math.isclose(eval(w['tests'][9]['expect']), 2028 / 450, rel_tol=1e-15))
c_all = sum(p * s for p, s in pence)
s_all = sum(s for _, s in pence)
check('book holds 1,100 shares', s_all == 1100)
check('whole book costs 4,981.00', c_all == 498100, str(c_all))
check('test 13 expect 4.528181818181818', float(F(c_all, s_all * 100)) == 4.528181818181818
      and math.isclose(eval(w['tests'][12]['expect']), 4981 / 1100, rel_tol=1e-15))
check('test 11 and 12 averages 4.5 exactly', 450 * 50 / 50 == 450 and (450 * 200 + 450 * 50) / 250 == 450)
check('dividing by qty instead gives 2.49', round(4981 / 2000, 4) == 2.4905)
check('tie order: sorted without key differs', sorted(BOOK)[:2] == [(4.50, 100), (4.50, 200)]
      and sorted(BOOK, key=lambda o: o[0])[:2] == [(4.50, 200), (4.50, 100)])
check('feedback test-10 states 2,028 over 450', '£2,028 over 450 shares' in item['feedback']['byKey']['test-10'])
check('feedback test-13 states 1,100', 'the 1,100 shares' in item['feedback']['byKey']['test-13'])
check('feedback test-1 states 200, 100, 150 of 300', '200 then 100' in item['feedback']['byKey']['test-1']
      and '150 of the 300 at £4.52' in item['feedback']['byKey']['test-1'])

# 5. planted beginner slips: each must fail at least one hidden test
SWEEP = SOL.split('\n\n\ndef average_price')[0]
AVG = 'def average_price' + SOL.split('\n\n\ndef average_price')[1]


def sub(src, old, new):
    assert old in src, old
    return src.replace(old, new)


slips = {
    'sorted without key (ties by size)': sub(SOL, 'sorted(offers, key=lambda offer: offer[0])', 'sorted(offers)'),
    'sorted highest first': sub(SOL, 'key=lambda offer: offer[0])', 'key=lambda offer: offer[0], reverse=True)'),
    'offers.sort() in place': sub(SOL, '    for price, size in sorted(offers, key=lambda offer: offer[0]):',
                                  '    offers.sort(key=lambda offer: offer[0])\n    for price, size in offers:'),
    'repeated min and remove on the caller list': '''def sweep_offers(qty, offers):
    if qty <= 0:
        raise ValueError("qty")
    left = qty
    while left > 0 and offers:
        best = min(offers, key=lambda offer: offer[0])
        offers.remove(best)
        take = min(best[1], left)
        yield best[0], take
        left = left - take
''' + '\n\n' + AVG,
    'len(offers) guard': sub(SOL, '    left = qty\n', '    if len(offers) == 0:\n        return\n    left = qty\n'),
    'checks total first (reads a generator twice)': sub(SOL, '    left = qty\n',
                                                         '    total = sum(size for price, size in offers)\n    left = min(qty, total)\n'),
    'empty book returns before the qty check': sub(SOL, '    if qty <= 0:', '    if not offers:\n        return\n    if qty <= 0:'),
    'assert instead of raise': sub(SOL, '    if qty <= 0:\n        raise ValueError(f"qty must be above zero: {qty}")\n',
                                   '    assert qty > 0, "qty must be above zero"\n'),
    'qty < 0 lets 0 through': sub(SOL, 'if qty <= 0:', 'if qty < 0:'),
    'wrong exception type': sub(SOL, 'raise ValueError(', 'raise TypeError('),
    'returns a list, not a generator': '''def sweep_offers(qty, offers):
    if qty <= 0:
        raise ValueError("qty")
    fills = []
    left = qty
    for price, size in sorted(offers, key=lambda offer: offer[0]):
        take = min(size, left)
        fills.append((price, take))
        left = left - take
        if left == 0:
            break
    return fills
''' + '\n\n' + AVG,
    'last offer taken whole': sub(SOL, 'take = min(size, left)', 'take = size'),
    'no stop: yields 0-share fills': sub(SOL, '        if left == 0:\n            break\n', ''),
    'stops before the offer that fills it': sub(SOL, '        take = min(size, left)\n',
                                                '        if size > left:\n            break\n        take = size\n'),
    'yields offer size, not shares taken': sub(SOL, 'yield price, take', 'yield price, size'),
    'average reads the fills twice': SWEEP + '''


def average_price(qty, offers):
    fills = sweep_offers(qty, offers)
    cost = sum(price * take for price, take in fills)
    shares = sum(take for price, take in fills)
    if shares == 0:
        return None
    return cost / shares
''',
    'average divides by qty': sub(SOL, 'return cost / shares', 'return cost / qty'),
    'average divides by zero on empty book': sub(SOL, '    if shares == 0:\n        return None\n', ''),
    'average returns 0 on empty book': sub(SOL, '        return None\n', '        return 0.0\n'),
    'average returns None for a bad qty': sub(SOL, 'def average_price(qty, offers):\n',
                                              'def average_price(qty, offers):\n    if qty <= 0:\n        return None\n'),
    'average is a plain mean of fill prices': sub(SOL, 'return cost / shares',
                                                  'return sum(p for p, t in sweep_offers(qty, offers)) / len(list(sweep_offers(qty, offers)))'),
    'average sorts again itself': SWEEP + '''


def average_price(qty, offers):
    shares = 0
    cost = 0.0
    for price, size in sorted(offers, key=lambda offer: offer[0]):
        take = min(size, qty - shares)
        shares = shares + take
        cost = cost + price * take
        if shares == qty:
            break
    if qty <= 0:
        raise ValueError("qty")
    if shares == 0:
        return None
    return cost / shares
''',
}
for name, code in slips.items():
    r = run_tests(code)
    caught = [k + 1 for k, x in enumerate(r) if x is not True]
    check(f'slip caught: {name}', len(caught) > 0, f'tests {caught}')

# 6. the three slip classes the task names are each caught by a test aimed at them
r = run_tests(slips['offers.sort() in place'])
check('mutating the argument fails test 6', r[5] is not True)
r = run_tests(slips['average reads the fills twice'])
check('generator read twice fails test 10', r[9] is not True)
r = run_tests(slips['average divides by zero on empty book'])
check('empty input fails test 11', r[10] is not True)
r = run_tests(slips['assert instead of raise'])
check('wrong exception type fails tests 8, 9, 14', all(r[k] is not True for k in (7, 8, 13)))

# 7. tests are fast
import time
t0 = time.perf_counter()
run_tests(SOL)
check('all 15 tests under 1 s natively', time.perf_counter() - t0 < 1.0)

print(f'{len(fails)} failures')
sys.exit(1 if fails else 0)
