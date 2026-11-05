"""Recompute every number in coding-int homework-1 item h1-ticker-book (PLAN 2c item 5 pilot).

Run from the repo root: python3 docs/reports/coding-int-1-perf-numbers.py  (exits 0 when all checks pass).
Each test expectation is computed twice, by two implementations that share no code with each other:
  A. the item's own `solution` (a trie with end marks), run under the item's `postlude`;
  B. an independent reference in this file (a set plus a dict of wildcard masks), run under the same postlude.
The small cases are also run a third time with a plain set and a scan per query.
Times (CPython, seconds) are measured for the solution and the scan on test 9 and stated in the item's report.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/coding-int/homework-1.json')
doc = json.load(open(HW))
item = next(it for it in doc['items'] if it['id'] == 'h1-ticker-book')
w = item['widget']
fails = []

def check(name, got, want):
    ok = got == want
    print(('ok  ' if ok else 'FAIL'), name, got, '' if ok else f'(want {want})')
    if not ok:
        fails.append(name)

PREFIX_DICT = '''from itertools import product
class TickerBook:
    def __init__(self):
        self.live = set()
        self.mask = {}
    def _masks(self, t):
        for pick in product((False, True), repeat=len(t)):
            yield ''.join('?' if m else c for c, m in zip(t, pick))
    def add(self, t):
        if t in self.live: return
        self.live.add(t)
        for m in self._masks(t):
            self.mask[m] = self.mask.get(m, 0) + 1
    def remove(self, t):
        if t not in self.live: return
        self.live.discard(t)
        for m in self._masks(t):
            self.mask[m] -= 1
    def has(self, t):
        return t in self.live
    def longest_listed(self, q):
        for i in range(len(q), 0, -1):
            if q[:i] in self.live: return q[:i]
        return None
    def count_match(self, p):
        return self.mask.get(p, 0)
'''

SCAN = '''class TickerBook:
    def __init__(self):
        self.s = set()
    def add(self, t): self.s.add(t)
    def remove(self, t): self.s.discard(t)
    def has(self, t): return t in self.s
    def longest_listed(self, q):
        c = [t for t in self.s if q.startswith(t)]
        return max(c, key=len) if c else None
    def count_match(self, p):
        return sum(1 for t in self.s if len(t) == len(p) and all(a == '?' or a == b for a, b in zip(p, t)))
'''

def namespace(src):
    ns = {}
    exec(src + '\n' + w['postlude'], ns)
    return ns

A = namespace(w['solution'])
B = namespace(PREFIX_DICT)
C = namespace(SCAN)
S = namespace(w['starter'])

tests = w['tests']
# shape figures stated in the item and the report
check('hidden tests stated in how (9)', len(tests), 9)
check('examples (2)', len(w['examples']), 2)
check('more tests than examples', len(tests) > len(w['examples']), True)
check('examples are the first two tests', w['examples'] == tests[:2], True)
check('homework items within 6 to 12 (10)', len(doc['items']), 10)
check('homework has a difficulty 5', any(it['difficulty'] == 5 for it in doc['items']), True)
check('one performance item in the homework', sum('performance' in it for it in doc['items']), 1)

for k, t in enumerate(tests, 1):
    want = eval(t['expect'])
    a = eval(t['call'], A)
    b = eval(t['call'], B)
    check(f'test-{k} solution (A)', a, want)
    check(f'test-{k} reference (B)', b, want)
    if t['call'].startswith('run_book'):
        check(f'test-{k} scan (C)', eval(t['call'], C), want)
    try:
        s = eval(t['call'], S)
    except Exception as e:
        s = f'raised {type(e).__name__}'
    check(f'test-{k} starter fails', s != want, True)

# "100,000 random steps": big_case's default n
import inspect
check('big_case default n (100,000)', inspect.signature(B['big_case']).parameters['n'].default, 100000)

# scan work in test 9: query steps times live tickers at each, against the trie's walk per step
def scan_work():
    ns = namespace(PREFIX_DICT)
    book_cls = ns['TickerBook']
    work = {'query_steps': 0, 'scanned': 0}
    def wrap(name):
        base = getattr(book_cls, name)
        def f(self, a):
            work['query_steps'] += 1
            work['scanned'] += len(self.live)
            return base(self, a)
        return f
    class Counting(book_cls):
        count_match = wrap('count_match')
        longest_listed = wrap('longest_listed')
    ns['TickerBook'] = Counting
    ns['big_case']()
    return work
wk = scan_work()
print('info test 9: query steps', wk['query_steps'], 'tickers scanned by a scan per query', wk['scanned'])
check('test 9 scan work above 10**8 ticker checks', wk['scanned'] > 10**8, True)

# measured time of test 9 (CPython): the trie against the scan, limit 5 s
import time
def timed(src):
    ns = namespace(src)
    t0 = time.perf_counter()
    r = ns['big_case']()
    return time.perf_counter() - t0, r
t_trie, r_trie = timed(w['solution'])
t_mask, r_mask = timed(PREFIX_DICT)
print('info test 9 time: trie %.2f s, wildcard-mask dict %.2f s (limit 5 s)' % (t_trie, t_mask))
check('trie passes test 9 inside 5 s', t_trie < 5, True)
check('test 9 trie and mask reference agree', r_trie, r_mask)
# the scan, on the first half of the steps only: it already misses the limit, so the whole test does
ns_scan = namespace(SCAN)
t0 = time.perf_counter()
ns_scan['big_case'](50000)
t_scan_half = time.perf_counter() - t0
print('info scan per query on the first 50,000 steps: %.2f s (limit 5 s for all 100,000)' % t_scan_half)
check('a scan per query fails the 5 s limit', t_scan_half > 5, True)

# each byKey line names a slip; the slip, planted in the solution, fails that test
def first_fail(src):
    ns = namespace(src)
    for k, t in enumerate(tests, 1):
        try:
            if eval(t['call'], ns) != eval(t['expect']):
                return k
        except Exception:
            return k
    return None
sol = w['solution']
MUTANTS = {
    # test 4: remove wipes the whole subtree below the ticker
    4: sol.replace("            node.pop('#', None)          # clear the end mark only", "            node.clear()"),
    # test 5: remove walks without checking the node exists
    5: sol.replace("        node = self._walk(ticker)\n        if node:                         # absent: no change\n            node.pop('#', None)          # clear the end mark only",
                   "        node = self.root\n        for ch in ticker:\n            node = node[ch]\n        node.pop('#', None)"),
}
for k, src in MUTANTS.items():
    check(f'slip named by test-{k} byKey is caught first at test {k}', (src != sol, first_fail(src)), (True, k))
# test 8: a '?' that only tries the first child is caught by a test no later than 8
m8 = sol.replace("for k, c in node.items() if k != '#')", "for k, c in list(node.items())[:1] if k != '#')")
check('first-child-only ? is caught by a test up to 8', (m8 != sol, first_fail(m8) is not None and first_fail(m8) <= 8), (True, True))
check('byKey names exactly tests 4, 5, 8 and 9', sorted(item['feedback']['byKey']), ['test-%d' % k for k in (4, 5, 8, 9)])
check('item prose and how mention the 5 s limit and 9 tests', ('5 s' in w['how'], 'Check runs 9 hidden tests' in w['how']), (True, True))

print('\n%d failures' % len(fails))
sys.exit(1 if fails else 0)
