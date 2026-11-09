"""Recompute every figure of algo-think homework-3 item h-ring-search (performance task, L3).

Route 1: the item's own solution (one-pass binary search on the turned list). Route 2: a linear
scan with list.index. Route 3: find the oldest slot by bisection, then bisect_left in the part that
can hold seq. For the 200,000-slot ring, route 4 is the closed form: 1,000,000 + 3i sits in slot
(i - 137,017) mod 200,000. Also: the starter fails; each planted wrong solution fails the tests
named; slow but correct solutions pass; the counts in prose, how and byKey match the file.
Run: python3 -I docs/reports/algo-think-3-perf-numbers.py
"""
import json, os, signal, sys, time
from bisect import bisect_left

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'algo-think', 'homework-3.json')
REV = os.path.join(ROOT, 'app', 'content', 'courses', 'algo-think', 'review-3.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-ring-search']
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


def same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
    return type(x) is type(y) and bool(x == y) if x is None or y is None else bool(x == y)


def namespace(code):
    ns = {'__name__': '__main__', '__learner_source__': code}
    exec(code, ns)
    exec(w['postlude'], ns)
    return ns


def run_tests(code, limit=5.0):
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


LINEAR = '''def find_trade(ring, seq):
    return ring.index(seq) if seq in ring else -1
'''
TWO_STEP = '''from bisect import bisect_left


def find_trade(ring, seq):
    if not ring:
        return -1
    lo, hi = 0, len(ring) - 1
    while lo < hi:                      # the oldest slot
        mid = (lo + hi) // 2
        if ring[mid] > ring[hi]:
            lo = mid + 1
        else:
            hi = mid
    p = lo
    if p > 0 and seq >= ring[0]:
        lo, hi = 0, p - 1
    else:
        lo, hi = p, len(ring) - 1
    i = bisect_left(ring, seq, lo, hi + 1)
    return i if i <= hi and ring[i] == seq else -1
'''
SOL = w['solution']
ns1, ns2, ns3 = namespace(SOL), namespace(LINEAR), namespace(TWO_STEP)

# 1. Every expectation by three routes.
for k, t in enumerate(T, 1):
    want = eval(t['expect'])
    got = []
    for ns in (ns1, ns2, ns3):
        if 'setup' in t:
            exec(t['setup'], ns)
        got.append(eval(t['call'], ns))
    check(all(same(g, want) for g in got), f'test {k}: {t["expect"]}: solution, linear scan and two-step agree')

# 2. The big ring by the closed form, and its shape.
n, k = 200000, 137017
R = [1000000 + 3 * ((j + k) % n) for j in range(n)]
check(sorted(R) == [1000000 + 3 * i for i in range(n)] and len(set(R)) == n, 'big ring: 200,000 distinct numbers, a turned sorted list')
check(min(range(n), key=R.__getitem__) == 62983 == n - k, 'big ring: oldest trade in slot 62,983 = 200,000 - 137,017')
check(sum(1 for j in range(n - 1) if R[j] > R[j + 1]) == 1, 'big ring: turned at exactly one point')


def closed(s):
    if (s - 1000000) % 3 or not 0 <= (s - 1000000) // 3 < n:
        return -1
    return ((s - 1000000) // 3 - k) % n


targets = (1411051, 1411048, 1000000, 1599997, 1300000, 1300001, 999997, 1600000)
check([closed(s) for s in targets] == eval(T[11]['expect']), f'test 12 by the closed form: {[closed(s) for s in targets]}')
check(R[0] == 1411051 and R[-1] == 1411048 and max(R) == 1599997 == R[62982], 'test 12 targets: slot 0, last slot, newest trade in slot 62,982')

# 3. The sweep: size and that it is clean for the routes.
calls = sum(max(m, 1) * (3 * m + 2) for m in range(13))
print('ring_sweep makes', calls, 'calls')
for name, ns in (('solution', ns1), ('linear', ns2), ('two-step', ns3)):
    check(same(ns['ring_sweep'](), [0, None]), f'ring_sweep() is [0, None] for the {name}')

# 4. Prose, how, byKey and file counts.
ex = [812, 815, 820, 803, 806, 809]
check(ex.index(803) == 3 and min(ex) == 803 and sum(1 for j in range(5) if ex[j] > ex[j + 1]) == 1, 'prose: 803 is the oldest, in slot 3, one turn')
check(len(T) == 13 and len(w['examples']) == 1 and w['examples'][0] == T[0], '13 tests, 1 example (test 1)')
check('Check runs 13 hidden tests' in w['how'] and 'Test 12 searches a ring of 200,000 slots' in w['how'] and 'Test 13' in w['how'] and 'up to 12 numbers' in w['how'], 'how: 13 tests, test 12 of 200,000, test 13 the sweep to 12')
check(T[12]['call'] == 'ring_sweep()' and 'top=12' in w['postlude'], 'sweep is test 13, sizes 0 to 12')
bk = item['feedback']['byKey']
check(set(bk) == {f'test-{j}' for j in range(1, 14)}, 'byKey has test-1 to test-13')
check('62,983' in bk['test-12'] and '200,000' in bk['test-12'], 'byKey 12: 200,000 slots, oldest in 62,983')
check(len(items) <= 12 and sum(1 for it in items if it.get('performance')) == 1, f'homework-3 holds {len(items)} items (cap 12), one performance item')
check(not any(it.get('performance') for it in json.load(open(REV))['items']), 'review-3 has no performance item')

# 5. Starter fails.
st_bad, _ = run_tests(w['starter'])
check(len(st_bad) == len(T), f'starter fails tests {st_bad}')

# 6. Planted wrong solutions.
plants = {
    'in-order test with <': (SOL.replace('if ring[lo] <= ring[mid]:', 'if ring[lo] < ring[mid]:'), [5]),
    'loop while lo < hi': (SOL.replace('while lo <= hi:', 'while lo < hi:'), [7]),
    'range check strict at lo': (SOL.replace('if ring[lo] <= seq < ring[mid]:', 'if ring[lo] < seq < ring[mid]:'), [9]),
    'range check strict at hi': (SOL.replace('if ring[mid] < seq <= ring[hi]:', 'if ring[mid] < seq < ring[hi]:'), [8]),
    'two-step, seq > ring[0]': (TWO_STEP.replace('seq >= ring[0]', 'seq > ring[0]'), [9]),
    'two-step, no check that seq is there': (TWO_STEP.replace('return i if i <= hi and ring[i] == seq else -1', 'return i if i <= hi else -1'), [4, 10]),
    'two-step, no empty guard': (TWO_STEP.replace('    if not ring:\n        return -1\n', '    if ring[0] < ring[-1]:\n        i = bisect_left(ring, seq)\n        return i if i < len(ring) and ring[i] == seq else -1\n'), [2]),
    'pivot search assumes a turn': (TWO_STEP.replace('''    while lo < hi:                      # the oldest slot
        mid = (lo + hi) // 2
        if ring[mid] > ring[hi]:
            lo = mid + 1
        else:
            hi = mid
''', '''    while lo < hi:
        mid = (lo + hi) // 2
        if ring[mid] >= ring[0]:
            lo = mid + 1
        else:
            hi = mid
'''), [3]),
    'place in sorted order': ('''from bisect import bisect_left


def find_trade(ring, seq):
    s = sorted(ring)
    i = bisect_left(s, seq)
    return i if i < len(s) and s[i] == seq else -1
''', [1]),
}
for name, (code, must) in plants.items():
    check(code != SOL and code != TWO_STEP, f'plant "{name}": differs from the solution')
    bad, _ = run_tests(code)
    check(bad and all(m in bad for m in must), f'plant "{name}": fails {bad} (must include {must})')

# 7. Slow but correct solutions pass; timing in CPython.
slow = {
    'linear scan': LINEAR,
    'oldest slot by a scan, then bisect': '''from bisect import bisect_left


def find_trade(ring, seq):
    if not ring:
        return -1
    p = min(range(len(ring)), key=ring.__getitem__)
    for lo, hi in ((0, p), (p, len(ring))):
        i = bisect_left(ring, seq, lo, hi)
        if i < hi and ring[i] == seq:
            return i
    return -1
''',
    'recursion on slices': '''def find_trade(ring, seq):
    if not ring:
        return -1
    mid = len(ring) // 2
    if ring[mid] == seq:
        return mid
    left, right = ring[:mid], ring[mid + 1:]
    if left and left[0] <= left[-1] and left[0] <= seq <= left[-1]:
        return find_trade(left, seq)
    if right and right[0] <= right[-1] and right[0] <= seq <= right[-1]:
        i = find_trade(right, seq)
        return -1 if i < 0 else mid + 1 + i
    if left and left[0] > left[-1]:
        return find_trade(left, seq)
    if right and right[0] > right[-1]:
        i = find_trade(right, seq)
        return -1 if i < 0 else mid + 1 + i
    return -1
''',
    'route 3 (two-step)': TWO_STEP,
}
bad, secs = run_tests(SOL)
check(bad == [], f'solution passes all 13; slowest case {max(secs):.3f} s')
for name, code in slow.items():
    bad, secs = run_tests(code)
    check(bad == [], f'slow but correct "{name}" passes all 13; slowest case {max(secs):.3f} s')

print('failures:', fails)
sys.exit(1 if fails else 0)
