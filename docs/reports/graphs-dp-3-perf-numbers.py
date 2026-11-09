"""Recompute every figure of graphs-dp homework-3 item h-fee-trades (performance task, L3).

Route 1: the item's own solution (two numbers a day, flat and long, bottom up).
Route 2: an O(n^2) table over the last buy day. Route 3: small tests by trying every plan
(each day buy, sell or wait); the two random walks by a memoised recursion, top down.
Every expectation must agree. Also: the starter fails; each planted wrong solution fails first
at the test its byKey names; the slow tables pass; the hand figures in byKey are right.
Run: python3 -I docs/reports/graphs-dp-3-perf-numbers.py
"""
import json, os, signal, sys, time
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'graphs-dp', 'homework-3.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-fee-trades']
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
T = w['tests']
print('item index (1-based):', idx[0] + 1, 'of', len(items))


class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def namespace(code):
    ns = {'__name__': '__main__', '__learner_source__': code}
    exec(code, ns)
    exec(w['postlude'], ns)
    return ns


def run_tests(code, limit=5.0):
    sys.setrecursionlimit(1000)
    bad, secs = [], []
    try:
        ns = namespace(code)
    except Exception:
        return list(range(1, len(T) + 1)), []
    for k, t in enumerate(T, 1):
        signal.setitimer(signal.ITIMER_REAL, limit)
        t0 = time.perf_counter()
        try:
            ok = eval(t['call'], ns) == eval(t['expect'], ns)
        except (Exception, Slow):
            ok = False
        signal.setitimer(signal.ITIMER_REAL, 0)
        secs.append(time.perf_counter() - t0)
        if not ok:
            bad.append(k)
    return bad, secs


def table_n2(prices, fee):
    n = len(prices)
    best = [0] * (n + 1)                 # best[j]: most profit, flat, after the first j days
    for j in range(1, n + 1):
        best[j] = best[j - 1]
        for i in range(j - 1):           # buy on day i, sell on day j - 1
            best[j] = max(best[j], best[i] + prices[j - 1] - prices[i] - fee)
    return best[n]


def every_plan(prices, fee):
    best = 0

    def go(day, holding, cash):
        nonlocal best
        if day == len(prices):
            if holding is None:
                best = max(best, cash)
            return
        p = prices[day]
        go(day + 1, holding, cash)                       # wait
        if holding is None:
            go(day + 1, p, cash - p)                     # buy
        else:
            go(day + 1, None, cash + p - fee)            # sell
    go(0, None, 0)
    return best


def memo(prices, fee):
    @lru_cache(maxsize=None)
    def f(i, holding):
        if i == len(prices):
            return 0 if not holding else float('-inf')
        if holding:
            return max(f(i + 1, True), f(i + 1, False) + prices[i] - fee)
        return max(f(i + 1, False), f(i + 1, True) - prices[i])
    return f(0, False)


sol = namespace(w['solution'])
alt = {name: dict(sol, trade_with_fee=fn) for name, fn in (('table', table_n2), ('plans', every_plan), ('memo', memo))}

# 1. Every expectation by at least two routes.
for k, t in enumerate(T, 1):
    want = eval(t['expect'])
    got = {'solution': eval(t['call'], sol), 'table': eval(t['call'], alt['table'])}
    if k <= 9:
        got['every plan'] = eval(t['call'], alt['plans'])
    else:
        got['memo'] = eval(t['call'], alt['memo'])
    check(all(v == want for v in got.values()), f'test {k}: file {want}, ' + ', '.join(f'{a} {b}' for a, b in got.items()))

# 2. Counts in the file.
check(len(T) == 11 and len(w['examples']) == 1 and w['examples'][0] == T[0], '11 tests, 1 example (test 1)')
check('Check runs 11 hidden tests' in w['how'] and '300 daily prices' in w['how'], 'how: 11 tests, 300 prices')
for call in ('price_walk()', 'price_walk(seed=4)'):
    ps = eval(call, sol)
    check(len(ps) == 300 and min(ps) >= 1 and all(isinstance(x, int) for x in ps), f'{call}: 300 whole prices, all at least 1 pence')
check(len(items) == 9 and sum(1 for it in items if it.get('performance')) == 1, 'homework-3 holds 9 items (cap 12), one performance item')

# 3. Starter fails.
st_bad, _ = run_tests(w['starter'])
check(len(st_bad) == len(T), f'starter fails tests {st_bad}')

# 4. Planted wrong solutions.
S = w['solution']
plants = {
    'one round trip only': ('''def trade_with_fee(prices, fee):
    best, lo = 0, float('inf')
    for p in prices:
        best = max(best, p - lo - fee)
        lo = min(lo, p)
    return best
''', 2),
    'greedy: trade each rise, low to high': ('''def trade_with_fee(prices, fee):
    total, i, n = 0, 0, len(prices)
    while i < n - 1:
        while i < n - 1 and prices[i + 1] <= prices[i]:
            i += 1
        lo = prices[i]
        while i < n - 1 and prices[i + 1] >= prices[i]:
            i += 1
        total += max(0, prices[i] - lo - fee)
    return total
''', 3),
    'table skips the first day': ('''def trade_with_fee(prices, fee):
    n = len(prices)
    flat, long = [0] * n, [float('-inf')] * n
    for i in range(1, n):
        flat[i] = max(flat[i - 1], long[i - 1] + prices[i] - fee)
        long[i] = max(long[i - 1], flat[i - 1] - prices[i])
    return flat[-1] if n else 0
''', 4),
    'table stops a day early': ('''def trade_with_fee(prices, fee):
    if not prices:
        return 0
    flat, long = 0, -prices[0]
    for i in range(1, len(prices) - 1):
        flat, long = max(flat, long + prices[i] - fee), max(long, flat - prices[i])
    return flat
''', 5),
    'reads prices[0] when there are none': ('''def trade_with_fee(prices, fee):
    flat, long = 0, -prices[0]
    for p in prices[1:]:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat
''', 7),
}
by_example = {
    'greedy: every daily rise less the fee': ('''def trade_with_fee(prices, fee):
    return sum(max(0, b - a - fee) for a, b in zip(prices, prices[1:]))
''', 1),
    'fee on the buy and the sale': (S.replace("max(long, flat - p)", "max(long, flat - p - fee)"), 1),
    'first share free (long starts at 0)': (S.replace("flat, long = 0, float('-inf')", "flat, long = 0, 0"), 1),
}
for _, (code, _) in list(by_example.items())[1:]:
    check(code != S, 'text plant built')
firsts = set()
for name, (code, first) in plants.items():
    bad, _ = run_tests(code)
    firsts.add(first)
    check(bool(bad) and bad[0] == first and 1 not in bad, f'plant "{name}" first fails test {bad[:1]} (named {first}), passes the example; fails {bad}')
for name, (code, first) in by_example.items():
    bad, _ = run_tests(code)
    check(bool(bad) and bad[0] == first, f'plant "{name}" fails the example; fails {bad}')
keyed = {int(k.split('-')[1]) for k in item['feedback']['byKey']}
check(keyed - {6} == firsts, f'byKey tests {sorted(keyed)}: the plants\' first failures {sorted(firsts)}, plus 6 (no trade pays)')
harmless = S.replace("    return flat                     # the answer must end flat", "    return max(flat, long)")
check(harmless != S and run_tests(harmless)[0] == [], 'returning max(flat, long) is still right: long < flat after any day')

# 5. Slow but correct.
for name, fn_src in (('O(n^2) table', table_n2), ('memoised recursion', memo)):
    ns = namespace('')
    ns['trade_with_fee'] = fn_src
    bad, secs = [], []
    for k, t in enumerate(T, 1):
        t0 = time.perf_counter()
        if eval(t['call'], ns) != eval(t['expect']):
            bad.append(k)
        secs.append(time.perf_counter() - t0)
    check(bad == [], f'{name} passes every test, slowest {max(secs):.4f} s in CPython')
bad, secs = run_tests(S)
check(bad == [], f'solution passes every test, slowest {max(secs):.4f} s in CPython (limit 5 s)')

# 6. Figures in byKey and the example.
E = lambda k: eval(T[k - 1]['expect'])
check(E(1) == 15 - 7 - 3 == 5, 'test 1: 15 - 7 - 3 = 5')
check(E(2) == (15 - 10 - 1) + (14 - 9 - 1) == 8, 'test 2: 4 + 4 = 8')
p2 = [12, 10, 15, 9, 14, 12]
check(max(p2[j] - p2[i] - 1 for i in range(6) for j in range(i + 1, 6)) == 4, 'test 2: one round trip makes at most 4')
check(E(3) == (16 - 10 - 2) + (18 - 13 - 2) == 7, 'test 3: 4 + 3 = 7')
check(12 - 10 - 2 == 0, 'test 3: selling at 12 earns nothing after the fee of 2')
check(eval('trade_with_fee([20, 10, 12, 11, 16, 13, 18, 15], 2)', dict(sol, trade_with_fee=eval('trade_with_fee', namespace(plants['greedy: trade each rise, low to high'][0])))) == 0 + 3 + 3 == 6,
      'test 3: trading each rise on its own makes 0 + 3 + 3 = 6')
check(E(4) == 13 - 8 - 2 == 3, 'test 4: 13 - 8 - 2 = 3')
check(E(5) == 12 - 6 - 2 == 4, 'test 5: 12 - 6 - 2 = 4')
p6 = [15, 14, 16, 13]
check(E(6) == 0 and max(p6[j] - p6[i] for i in range(4) for j in range(i + 1, 4)) == 16 - 14 == 2 < 3, 'test 6: the best rise, 14 to 16, is 2, below the fee of 3')
check(E(7) == 0 and E(8) == 0, 'tests 7 and 8: no days, one day: 0')
p9 = [3, 5, 4, 6, 2, 7]
check(E(9) == sum(max(0, b - a) for a, b in zip(p9, p9[1:])) == 2 + 2 + 5, 'test 9: with no fee, every rise: 2 + 2 + 5 = 9')

print('failures:', fails)
sys.exit(1 if fails else 0)
