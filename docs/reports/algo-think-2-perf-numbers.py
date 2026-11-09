"""Recompute every figure of algo-think homework-2 item h-split-feed (performance task, L2).

Route 1: the item's own solution (recursion over the ticker set). Route 2: brute force over every
set of cuts in the feed's gaps. Route 3, for counts: a bottom-up count of splits from each position.
Also: the starter fails; each planted wrong solution fails the tests named; slow but correct
solutions pass; the counts in prose, how, byKey and explain match the file.
Run: python3 -I docs/reports/algo-think-2-perf-numbers.py
"""
import itertools, json, os, signal, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'algo-think', 'homework-2.json')
REV = os.path.join(ROOT, 'app', 'content', 'courses', 'algo-think', 'review-2.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-split-feed']
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


# ---- grading as code.js does it: code, then postlude, one namespace; setup, then eval call; equal ----
class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
    return bool(x == y)


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
            if 'setup' in t:
                exec(t['setup'], ns)
            ok = same(eval(t['call'], ns), eval(t['expect'], ns))
        except (Exception, Slow):
            ok = False
        signal.setitimer(signal.ITIMER_REAL, 0)
        secs.append(time.perf_counter() - t0)
        if not ok:
            bad.append(k)
    return bad, secs


# ---- route 2: brute force over cut sets ----
def brute_split(feed, listed):
    every = set(listed)
    if feed == '':
        return [[]]
    out = set()
    for bits in itertools.product((0, 1), repeat=len(feed) - 1):
        cuts = [0] + [i + 1 for i, b in enumerate(bits) if b] + [len(feed)]
        parts = tuple(feed[a:b] for a, b in zip(cuts, cuts[1:]))
        if all(p in every for p in parts):
            out.add(parts)
    return [list(p) for p in out]


# ---- route 3: bottom-up count of splits of feed[i:] ----
def count_splits(feed, listed):
    every = set(listed)
    n = len(feed)
    ways = [0] * (n + 1)
    ways[n] = 1
    for i in range(n - 1, -1, -1):
        ways[i] = sum(ways[i + len(t)] for t in every if feed.startswith(t, i))
    return ways[0]


SOL = w['solution']
sol_ns = namespace(SOL)
brute_ns = namespace(SOL)
brute_ns['split_feed'] = brute_split

# 1. Every expectation by two routes; counts by a third.
for k, t in enumerate(T, 1):
    want = eval(t['expect'])
    got = []
    for ns in (sol_ns, brute_ns):
        if 'setup' in t:
            exec(t['setup'], ns)
        got.append(eval(t['call'], ns))
    check(same(got[0], want) and same(got[1], want), f'test {k}: {t["expect"][:60]}: solution and brute force agree')

tally_cases = [('A' * 12, ['A', 'AA', 'AAA'], 927), ('BA' * 8, ['BA', 'BAB', 'AB', 'A', 'B'], 4374)]
for feed, listed, n in tally_cases:
    c = count_splits(feed, listed)
    check(c == n and c <= 2 ** (len(feed) - 1), f'{feed[:6]}... ({len(feed)} letters): bottom-up count {c} = {n}, at most 2^{len(feed) - 1} = {2 ** (len(feed) - 1)}')
# 927 is the tribonacci-like count of ordered parts 1, 2, 3 summing to 12, by a fourth route
comp = sum(1 for r in range(1, 13) for parts in itertools.product((1, 2, 3), repeat=r) if sum(parts) == 12)
check(comp == 927, f'ordered parts 1, 2, 3 summing to 12: {comp}')
for k in range(1, 10):
    t = T[k - 1]
    if t['call'].startswith('sorted(split_feed('):
        feed, listed = eval(t['call'][len('sorted(split_feed('):-2])
        check(count_splits(feed, listed) == len(eval(t['expect'])), f'test {k}: bottom-up count {count_splits(feed, listed)} splits')
for k, t in enumerate(T, 1):
    if t['call'].startswith('sorted(split_feed(') and "''" not in t['call']:
        feed, listed = eval(t['call'][len('sorted(split_feed('):-2])
        check(count_splits(feed, listed) <= 2 ** (len(feed) - 1), f'explain: test {k} has at most 2^(n-1) = {2 ** (len(feed) - 1)} splits')

# 2. Prose, how, byKey and file counts.
check(same(sorted(brute_split('BARCBP', ['BA', 'BARC', 'RC', 'BP', 'B'])), [['BA', 'RC', 'BP'], ['BARC', 'BP']]), 'prose: BARCBP has two splits, BA RC BP and BARC BP')
check(len(T) == 12 and len(w['examples']) == 1 and w['examples'][0] == T[0], '12 tests, 1 example (test 1)')
check('Check runs 12 hidden tests' in w['how'] and 'Tests 10 and 11' in w['how'], 'how: 12 tests; tests 10 and 11 use split_tally')
check(T[9]['call'].startswith('split_tally') and T[10]['call'].startswith('split_tally') and not any(t['call'].startswith('split_tally') for t in T[:9] + T[11:]), 'split_tally in tests 10 and 11 only')
bk = item['feedback']['byKey']
check(set(bk) == {f'test-{k}' for k in range(1, 13)}, 'byKey has test-1 to test-12')
check('927' in bk['test-10'] and '4,374' in bk['test-11'] and '12 `A`s' in bk['test-10'] and 'eight times' in bk['test-11'], 'byKey 10 and 11: 927 and 4,374')
check(len(brute_split('BTBT', ['BT', 'B', 'T', 'BT'])) == 4 and 'four different splits' in bk['test-5'], 'byKey 5: four splits')
check(len(brute_split('AAA', ['A', 'AA'])) == 3 and 'three splits' in bk['test-8'], 'byKey 8: three splits')
check(len(brute_split('SSEAZN', ['SSE', 'AZN', 'SS', 'EAZN', 'E'])) == 3 and 'three splits' in bk['test-9'], 'byKey 9: three splits')
check(len(items) <= 12 and sum(1 for it in items if it.get('performance')) == 1, f'homework-2 holds {len(items)} items (cap 12), one performance item')
check(not any(it.get('performance') for it in json.load(open(REV))['items']), 'review-2 has no performance item')

# 3. Starter fails.
st_bad, _ = run_tests(w['starter'])
check(len(st_bad) == len(T), f'starter fails tests {st_bad}')

# 4. Planted wrong solutions.
plants = {
    'base case returns []': (SOL.replace('return [[]]                  # one split, holding no tickers', 'return []'), [1, 2]),
    'stops when the rest is a ticker': (SOL.replace('    splits = []\n', '    if feed in listed:\n        return [[feed]]\n    splits = []\n'), [6]),
    'cut never reaches the end': ('''def split_feed(feed, listed):
    if feed == "":
        return [[]]
    splits = []
    for end in range(1, len(feed)):
        head = feed[:end]
        if head in set(listed):
            for rest in split_feed(feed[end:], listed):
                splits.append([head] + rest)
    return splits
''', [1, 7]),
    'first split only': ('''def split_feed(feed, listed):
    if feed == "":
        return [[]]
    for t in set(listed):
        if feed.startswith(t):
            rest = split_feed(feed[len(t):], listed)
            if rest:
                return [[t] + rest[0]]
    return []
''', [1]),
    'longest ticker only': ('''def split_feed(feed, listed):
    if feed == "":
        return [[]]
    fits = [t for t in set(listed) if feed.startswith(t)]
    if not fits:
        return []
    t = max(fits, key=len)
    return [[t] + r for r in split_feed(feed[len(t):], listed)]
''', [1, 4]),
    'list as given, so repeats': (SOL.replace('for ticker in set(listed):', 'for ticker in listed:'), [5]),
    'shared default list': ('''def split_feed(feed, listed, path=[], out=[]):
    if feed == "":
        out.append(list(path))
        return out
    for t in set(listed):
        if feed.startswith(t):
            path.append(t)
            split_feed(feed[len(t):], listed, path, out)
            path.pop()
    return out
''', [2]),
    'tickers in reverse order': (SOL.replace('splits.append([ticker] + rest)', 'splits.append(rest + [ticker])'), [1]),
    'sorts listed in place': (SOL.replace('    splits = []\n', '    listed.sort(key=len, reverse=True)\n    splits = []\n'), [12]),
    'empty feed gives no split': ('''def split_feed(feed, listed):
    if not feed:
        return []
    def walk(i):
        if i == len(feed):
            return [[]]
        out = []
        for t in set(listed):
            if feed.startswith(t, i):
                out += [[t] + r for r in walk(i + len(t))]
        return out
    return walk(0)
''', [2]),
}
for name, (code, must) in plants.items():
    check(code != SOL, f'plant "{name}": differs from the solution')
    bad, _ = run_tests(code)
    check(bad and all(m in bad for m in must), f'plant "{name}": fails {bad} (must include {must})')

# 5. Slow but correct solutions pass; timing in CPython.
slow = {
    'brute force over cuts': '''from itertools import product
def split_feed(feed, listed):
    every = set(listed)
    if feed == "":
        return [[]]
    found = set()
    for bits in product((0, 1), repeat=len(feed) - 1):
        cuts = [0] + [i + 1 for i, b in enumerate(bits) if b] + [len(feed)]
        parts = tuple(feed[a:b] for a, b in zip(cuts, cuts[1:]))
        if all(p in every for p in parts):
            found.add(parts)
    return [list(p) for p in found]
''',
    'backtracking with a path': '''def split_feed(feed, listed):
    every = sorted(set(listed))
    out, path = [], []
    def walk(i):
        if i == len(feed):
            out.append(path[:])
            return
        for t in every:
            if feed[i:i + len(t)] == t:
                path.append(t)
                walk(i + len(t))
                path.pop()
    walk(0)
    return out
''',
}
bad, secs = run_tests(SOL)
check(bad == [], f'solution passes all 12; slowest case {max(secs):.3f} s')
for name, code in slow.items():
    bad, secs = run_tests(code)
    check(bad == [], f'slow but correct "{name}" passes all 12; slowest case {max(secs):.3f} s')

print('failures:', fails)
sys.exit(1 if fails else 0)
