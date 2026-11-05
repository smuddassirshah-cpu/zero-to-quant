"""Recompute every number in coding-int homework-1 item h1-ticker-book (PLAN 2c item 5 pilot).

Run from the repo root: python3 docs/reports/coding-int-1-perf-numbers.py  (exits 0 when all checks pass).
Each test expectation is computed twice, by two implementations that share no code with each other:
  A. the item's own `solution` (a trie with counts on the nodes), run under the item's `postlude`;
  B. an independent reference in this file (a dict of prefix counts plus a set), run under the same postlude.
The small cases are also run a third time with a plain set and a scan per query.
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

PREFIX_DICT = '''class TickerBook:
    def __init__(self):
        self.live = set()
        self.pre = {}
    def add(self, t):
        if t in self.live: return
        self.live.add(t)
        for i in range(len(t) + 1):
            self.pre[t[:i]] = self.pre.get(t[:i], 0) + 1
    def remove(self, t):
        if t not in self.live: return
        self.live.discard(t)
        for i in range(len(t) + 1):
            self.pre[t[:i]] -= 1
    def has(self, t):
        return t in self.live
    def count_prefix(self, p):
        return self.pre.get(p, 0)
'''

SCAN = '''class TickerBook:
    def __init__(self):
        self.s = set()
    def add(self, t): self.s.add(t)
    def remove(self, t): self.s.discard(t)
    def has(self, t): return t in self.s
    def count_prefix(self, p): return sum(1 for t in self.s if t.startswith(p))
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

# scan work in test 9: count steps times live tickers at each, against the trie's O(L) walk
def scan_work():
    ns = namespace(PREFIX_DICT)
    book_cls = ns['TickerBook']
    work = {'count_steps': 0, 'scanned': 0}
    class Counting(book_cls):
        def count_prefix(self, p):
            work['count_steps'] += 1
            work['scanned'] += len(self.live)
            return super().count_prefix(p)
    ns['TickerBook'] = Counting
    ns['big_case']()
    return work
wk = scan_work()
print('info test 9: count steps', wk['count_steps'], 'tickers scanned by a scan per query', wk['scanned'])
check('test 9 scan work above 10**8 startswith calls', wk['scanned'] > 10**8, True)

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
    3: sol.replace("        if self.has(ticker):             # listed already: no change\n            return\n", ""),
    4: sol.replace("        if not self.has(ticker):         # not listed: no change\n            return\n", "        if self._walk(ticker) is None:\n            return\n"),
    5: sol.replace("        node['#end'] = False\n", "        node['#end'] = False\n        node.clear(); node['#n'] = 0\n"),
    7: sol.replace("        if self.has(ticker):             # listed already: no change", "        if self._walk(ticker) is not None:"),
}
for k, src in MUTANTS.items():
    check(f'slip named by test-{k} byKey is caught first at test {k}', (src != sol, first_fail(src)), (True, k))
check('byKey names exactly those tests and test 9', sorted(item['feedback']['byKey']), ['test-%d' % k for k in (3, 4, 5, 7, 9)])

print('\n%d failures' % len(fails))
sys.exit(1 if fails else 0)
