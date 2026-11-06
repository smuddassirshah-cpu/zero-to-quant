"""Second-reader number checks for contests level 3 (l9 to l12, review-3, homework-3).

Every value is recomputed here in CPython with code written for this script (brute force over subsets or
permutations on small cases; a different algorithm from the shipped solution on the size cases, rebuilt from
the seeds in each test's setup). Each value is then looked up where the content states it
(app/tools/numbers_lib.py). check_wrongs() checks every numeric wrong[] value. No shipped solution is imported.
Run: python3 docs/reports/contests-L3-numbers.py
"""
import bisect, heapq, itertools, os, random, sys
from itertools import accumulate
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('contests', 3)
E = lv.expect


def K(ref, path, key, value):
    """A feedback.byKey line whose key has a hyphen (test-9): look the key up directly."""
    from numbers_lib import _walk, _numbers
    _, doc = lv._file(ref)
    txt = _walk(doc, path)[0].get(key, '')
    ok = any(abs(x - value) <= 1e-9 * max(1.0, abs(value)) for x in _numbers(txt))
    return lv._rec(ok, f'{ref} {path}.{key} = {value!r}', '' if ok else f'not found in: {txt[:120]!r}')

# ---------- l9: constructive ----------
def valid(p):
    return all(abs(p[i] - p[i + 1]) != 1 for i in range(len(p) - 1))
cands = ['1 3 2 4', '2 4 1 3', '3 1 2 4', '3 1 4 2', '1 4 2 3', '2 4 3 1']
good = [i + 1 for i, c in enumerate(cands) if valid(list(map(int, c.split())))]
assert good == [2, 4]
E('l9', 'screens[0].hints[1].text', 1); E('l9', 'screens[0].hints[1].text', 6)       # lines 1, 3, 5, 6 fail
assert sum(valid(p) for p in itertools.permutations(range(1, 5))) == 2              # exactly 2 4 1 3 and 3 1 4 2
none = [n for n in range(1, 9) if not any(valid(p) for p in itertools.permutations(range(1, n + 1)))]
assert none == [2, 3]
E('l9', 'screens[1].feedback.correct', 2); E('l9', 'screens[1].feedback.correct', 3)
E('l9', 'screens[0].hints[2].text', '2 4 1 3 has gaps 2, 3 and 2')
E('l9', 'screens[2].hints[2].text', 4 - 1)
# problem F: sums reachable with n numbers in 1..k
def reach(n, k):
    return {sum(t) for t in itertools.product(range(1, k + 1), repeat=n)}
r34 = reach(3, 4)
E('l9', 'quiz[3].widget.answer', sum(1 for s in range(1, 21) if s in r34))            # 10
E('l9', 'quiz[3].explain.text', 12 - 3 + 1)
E('l9', 'screens[7].widget.options[1].why', 3 + 3 + 3 + 1)                            # 10 with n = 4
E('l9', 'screens[8].canvas.state.caption', 10 - 4)                                    # extra 6
K('l9', 'screens[8].feedback.byKey', 'test-9', 1.5)                                     # s - n = 1,499,800,007
assert abs((1500000007 - 200000) - 1.5e9) / 1.5e9 < 0.001
# slicing a parent order: 6 children, 100..250, sum 1000
sched = {'A': [250, 250, 250, 250, 0, 0], 'B': [250, 250, 200, 100, 100, 100], 'C': [167, 167, 167, 167, 166, 166],
         'D': [250, 250, 250, 150, 50, 50], 'E': [200] * 5}
ok = [k for k, v in sched.items() if len(v) == 6 and sum(v) == 1000 and all(100 <= x <= 250 for x in v)]
assert ok == ['B', 'C']
E('l9', 'screens[9].explain.text', 6 * 100); E('l9', 'screens[9].explain.text', 6 * 250)
for opt, line in [(1, '2 4 1 3 5'), (2, '1 3 5 2 4'), (3, '5 3 1 4 2')]:
    xs = list(map(int, line.split()))
    gaps = ', '.join(str(abs(xs[i] - xs[i + 1])) for i in range(4))
    E('l9', f'quiz[0].widget.options[{opt}].why', gaps.rsplit(', ', 1)[0] + ' and ' + gaps.rsplit(', ', 1)[1])
assert not valid([1, 3, 5, 4, 2])
# review-contests-3-4 finding 1: two orders of 1 to 5 fail every pair (increasing and decreasing), not one.
assert sum(all(abs(p[i] - p[i + 1]) == 1 for i in range(4)) for p in itertools.permutations(range(1, 6))) == 2
E('l9', 'screens[4].widget.options[5].why', 'worst case')   # fails until the fix lands

# ---------- l10: greedy ----------
M = {'A': (0, 13), 'B': (1, 5), 'C': (4, 7), 'D': (6, 11), 'E': (9, 15), 'F': (12, 14)}
def compatible(ms, strict=False):
    ms = sorted(ms)
    return all((ms[i][1] < ms[i + 1][0]) if strict else (ms[i][1] <= ms[i + 1][0]) for i in range(len(ms) - 1))
best = max(r for r in range(7) for c in itertools.combinations(M.values(), r) if compatible(c))
E('l10', 'screens[0].feedback.correct', 'Three meetings'); assert best == 3
def rule(key):
    kept = []
    for m in sorted(M.values(), key=key):
        if all(m[1] <= k[0] or k[1] <= m[0] for k in kept):
            kept.append(m)
    return len(kept)
E('l10', 'screens[1].canvas.controls[0].frames[0].caption', rule(lambda m: m[1] - m[0]))   # 2
E('l10', 'screens[1].canvas.controls[0].frames[1].caption', rule(lambda m: m[0]))          # 1
E('l10', 'screens[1].canvas.controls[0].frames[2].caption', rule(lambda m: m[1]))          # 3
E('l10', 'screens[1].widget.options[3].why', 2); E('l10', 'screens[1].widget.options[3].why', 1)
overlaps_A = sum(1 for k, m in M.items() if k != 'A' and m[0] < M['A'][1] and M['A'][0] < m[1])
assert overlaps_A == 5
# review-contests-3-4 finding 2: A blocks five meetings, not two. Fails until the fix lands.
E('l10', 'screens[1].explain.text', 'all five others')
tri = [(1, 3), (3, 5), (5, 7)]
E('l10', 'screens[3].widget.answer', max(r for r in range(4) for c in itertools.combinations(tri, r) if compatible(c, strict=True)))
E('l10', 'screens[3].feedback.byKey.touch', max(r for r in range(4) for c in itertools.combinations(tri, r) if compatible(c)))
def rooms(iv):
    # heap of end times, a different method from the shipped event sweep
    h = []
    for s, e in sorted(iv):
        if h and h[0] <= s:
            heapq.heapreplace(h, e)
        else:
            heapq.heappush(h, e)
    return len(h)
E('l10', 'screens[5].widget.answer', rooms(M.values()))                                # 3
r = random.Random(2024); big = []
for _ in range(200000):
    s = r.randint(0, 10**9); big.append((s, s + r.randint(1, 10**6)))
# max disjoint by DP over intervals sorted by end with bisect (not the greedy)
srt = sorted(big, key=lambda x: x[1]); ends = [e for _, e in srt]; dp = [0] * (len(srt) + 1)
for i, (s, e) in enumerate(srt):
    j = bisect.bisect_right(ends, s, 0, i)
    dp[i + 1] = max(dp[i], dp[j] + 1)
E('l10', 'screens[4].explain.text', dp[-1])                                            # 11,256
E('l10', 'screens[6].explain.text', rooms(big))                                        # 144
def greedy(coins, a):
    n = 0
    for c in sorted(coins, reverse=True):
        n += a // c; a %= c
    return n
def fewest(coins, a):
    f = [0] + [10**9] * a
    for x in range(1, a + 1):
        f[x] = min(f[x - c] + 1 for c in coins if c <= x)
    return f[a]
def first_fail(coins, top=200):
    return next(a for a in range(1, top) if greedy(coins, a) != fewest(coins, a))
E('l10', 'screens[7].widget.options[0].text', first_fail([1, 3, 4]))                   # 6
E('l10', 'screens[7].explain.text', 5)
assert greedy([1, 3, 4], 6) == 3 and fewest([1, 3, 4], 6) == 2
assert all(greedy([1, 3, 4], a) == fewest([1, 3, 4], a) for a in (7, 8))
E('l10', 'quiz[2].widget.options[0].text', first_fail([1, 5, 10, 20, 25]))             # 40
assert all(greedy([1, 5, 10, 20, 25], a) == fewest([1, 5, 10, 20, 25], a) for a in range(1, 31))
# the coin hunt, rebuilt with this script's own loop over the lesson's generator
def gen_coins(rng):
    coins = sorted([1] + rng.sample(range(2, 10), 2)); return coins, rng.randint(1, 20)
def hunt(trials, seed, first=False):
    rng = random.Random(seed); out = None
    for _ in range(trials):
        c, a = gen_coins(rng)
        if greedy(c, a) != fewest(c, a):
            if first:
                return (c, a)
            if out is None or a < out[1]:
                out = (c, a)
    return out
for t, seed in enumerate([1, 2, 3, 4]):
    c, a = hunt(200, seed)
    E('l10', f'screens[8].widget.tests[{t}].expect', a); E('l10', f'screens[8].widget.tests[{t}].expect', c[1])
assert hunt(10, 1) is None and hunt(10, 2) == ([1, 5, 7], 11)
c, a = hunt(200, 1, first=True); K('l10', 'screens[8].feedback.byKey', 'test-1', a); K('l10', 'screens[8].feedback.byKey', 'test-1', c[2])
E('l10', 'screens[8].explain.text', 6)
assert all(greedy([1, 2, 5, 10], a) == fewest([1, 2, 5, 10], a) for a in range(1, 41))
orders = [(0, 30), (5, 10), (10, 25), (20, 35), (25, 40), (35, 50), (45, 60), (50, 55)]
E('l10', 'screens[10].widget.answer', max(r_ for r_ in range(9) for c_ in itertools.combinations(orders, r_) if compatible(c_)))
kept, last = [], -1
for s, e in sorted(orders):
    if s >= last:
        kept.append((s, e)); last = e
E('l10', 'screens[10].widget.wrong[0].value', len(kept))
assert sum(1 for o in orders[1:] if o[0] < 30) == 4
q1 = [(1, 4), (4, 6), (6, 9), (2, 5)]
E('l10', 'quiz[1].widget.answer', max(r_ for r_ in range(5) for c_ in itertools.combinations(q1, r_) if compatible(c_)))
assert max(r_ for r_ in range(5) for c_ in itertools.combinations(q1, r_) if compatible(c_, True)) == 2
E('l10', 'quiz[3].widget.answer', rooms([(0, 4), (1, 3), (2, 6), (3, 5), (5, 7)]))
assert sum(1 for s, e in [(0, 4), (1, 3), (2, 6), (3, 5), (5, 7)] if s <= 3 <= e) == 4   # the closed reading gives 4

# ---------- l11: bitmasks ----------
P4, R4 = [5, 4, 3, 7], [3, 2, 2, 4]
best4 = max((sum(P4[i] for i in c), c) for k in range(5) for c in itertools.combinations(range(4), k) if sum(R4[i] for i in c) <= 6)
assert best4 == (11, (1, 3))
E('l11', 'screens[0].explain.text', 11); E('l11', 'screens[0].explain.text', 2 ** 4)
E('l11', 'screens[1].widget.answer', 1 + 2)
E('l11', 'screens[2].widget.rows[0][1].answer', 10 >> 1 & 1)
E('l11', 'screens[2].widget.rows[1][1].answer', 10 | 1 << 2)
E('l11', 'screens[2].widget.rows[2][1].answer', 10 & -10)
E('l11', 'screens[2].widget.rows[3][1].answer', bin(10).count('1'))
p16 = [371, 481, 493, 292, 427, 233, 458, 6, 420, 875, 674, 729, 266, 244, 651, 228]
r16 = [2, 38, 39, 43, 86, 19, 96, 78, 40, 3, 29, 78, 33, 3, 20, 78]
knap = [0] * 401
for p, w in zip(p16, r16):
    for cap in range(400, w - 1, -1):
        knap[cap] = max(knap[cap], knap[cap - w] + p)
E('l11', 'screens[3].widget.tests[5].expect', knap[400]); E('l11', 'screens[3].widget.tests[6].expect', sum(p16))
E('l11', 'screens[3].explain.text', 2 ** 16 * 16 / 1e6, fmt='10^6')
E('l11', 'screens[4].widget.answer', len(range(1 << 4 - 1)))
K('l11', 'screens[4].feedback.byKey', 'minus-last', (1 << 4) - 1)
def count_sum(xs, t):
    return sum(1 for k in range(len(xs) + 1) for c in itertools.combinations(xs, k) if sum(c) == t)
E('l11', 'screens[5].widget.tests[6].expect', count_sum([3, 1, 4, 1, 5, 9, 2, 6], 10))
L16 = [17, 14, 26, 10, 12, 10, 6, 25, 23, 23, 18, 22, 9, 4, 30, 1]
E('l11', 'screens[5].widget.tests[7].expect', count_sum(L16, 120))
E('l11', 'screens[5].widget.tests[8].expect', count_sum(L16, 0))
E('l11', 'screens[5].widget.tests[9].expect', count_sum([-9, -13, 8, 1, -5, -8, 11, 20, 11, -9, 10, -2, 9, -4, -8, -4], 7))
E('l11', 'screens[5].canvas.params.lines[1]', count_sum([2, 2, 2], 4))
E('l11', 'screens[6].widget.tests[4].expect', 2 ** 18)
E('l11', 'screens[6].widget.tests[5].expect', sum(bin(m).count('1') for m in range(1 << 18)))
E('l11', 'screens[7].widget.answer', 2 ** 10 * 10)
E('l11', 'screens[7].feedback.byKey.perms', 362880); assert 362880 == len(list(itertools.permutations(range(9))))
E('l11', 'screens[7].explain.text', 1.7, fmt='1.7'); assert abs(2 ** 16 * 16 ** 2 / 1e7 - 1.68) < 0.01
E('l11', 'screens[8].prose', 1.1, fmt='1.1'); assert abs(2 ** 40 / 1e12 - 1.0995) < 1e-3
E('l11', 'screens[8].widget.answer', 2 * 2 ** 20)
E('l11', 'screens[8].widget.accept', 2 ** 20)
def submasks(m):
    s, out = m, [m]
    while s:
        s = (s - 1) & m; out.append(s)
    return out
assert [format(x, '04b') for x in submasks(0b1011)] == ['1011', '1010', '1001', '1000', '0011', '0010', '0001', '0000']
E('l11', 'screens[9].widget.answer', sum(len(submasks(m)) for m in range(8)))
E('l11', 'screens[9].explain.text', 4.3, fmt='4.3'); assert abs(3 ** 16 / 1e7 - 4.3) < 0.01
E('l11', 'screens[10].widget.answer', 2 ** 6 - 1)
E('l11', 'quiz[3].widget.answer', len(submasks(0b10110)))
assert [i for i in range(4) if 13 >> i & 1] == [0, 2, 3] and 0b1110 == 14 and 0b0101 == 5

# ---------- l12: difference arrays ----------
E('l12', 'screens[0].widget.answer', 10**5 * 2 * 10**5)
def apply(n, ups):
    v = [0] * n
    for l, r_, x in ups:
        for i in range(l, r_ + 1):
            v[i] += x
    return v
ex = [(1, 4, 3), (2, 6, 2), (5, 7, 1)]
vals = apply(8, ex)
E('l12', 'screens[4].widget.tests[0].expect', ', '.join(map(str, vals)))
E('l12', 'screens[1].widget.answer', vals[5])
d = [0] * 9
for l, r_, x in ex:
    d[l] += x; d[r_ + 1] -= x
assert d == [0, 3, 2, 0, 0, -2, 0, -2, -1] and list(accumulate(d))[:8] == vals
E('l12', 'screens[1].widget.wrong[1].value', d[5]); E('l12', 'screens[1].widget.wrong[0].value', 3 + 2 + 1)
r = random.Random(12); ups = []
for _ in range(100000):
    l = r.randint(0, 199999); ups.append((l, r.randint(l, 199999), r.randint(-1000, 1000)))
dd = [0] * 200001
for l, r_, x in ups:
    dd[l] += x; dd[r_ + 1] -= x
fin = list(accumulate(dd[:200000]))
E('l12', 'screens[4].widget.tests[7].expect', sum(i * x for i, x in enumerate(fin)) % 1000000007)
E('l12', 'screens[4].explain.text', 5, fmt='5 \\cdot 10^9'); assert abs(sum(r_ - l + 1 for l, r_, _ in ups) / 5e9 - 1) < 0.01
W = [(1, 5), (2, 8), (4, 9), (6, 7), (0, 3)]
cov = [sum(1 for l, r_ in W if l <= i <= r_) for i in range(10)]
E('l12', 'screens[6].explain.text', ', '.join(map(str, cov))); E('l12', 'screens[6].widget.answer', max(cov))
r = random.Random(13); wins = []
for _ in range(100000):
    a, b = r.randint(0, 199999), r.randint(0, 199999); wins.append((min(a, b), max(a, b)))
ev = sorted([(l, 0) for l, _ in wins] + [(r_ + 1, -1) for _, r_ in wins])   # sweep, ends at r + 1 first
run = peak = 0
for _, kind in ev:
    run += 1 if kind == 0 else -1; peak = max(peak, run)
E('l12', 'screens[7].explain.text', peak)                                             # 49,889
tot = sum(r_ - l + 1 for l, r_ in wins)
E('l12', 'screens[7].explain.text', 6.6, fmt='6.6'); assert abs(tot / 1e9 - 6.65) < 0.01
K('l12', 'screens[7].feedback.byKey', 'test-7', 66500); assert abs(tot / 100000 - 66500) < 10
fills = {0: 300, 2: -100, 3: 200, 5: -400}
E('l12', 'screens[9].widget.answer', sum(v for t, v in fills.items() if t <= 4))
E('l12', 'screens[9].widget.wrong[1].value', 300 + 100 + 200); E('l12', 'screens[9].widget.wrong[0].value', sum(fills.values()))
dq = [0] * 6
for l, r_, x in [(0, 2, 5), (1, 3, -2)]:
    dq[l] += x; dq[r_ + 1] -= x
E('l12', 'quiz[0].widget.options[0].text', ', '.join(map(str, dq)).replace('-', '−'))
E('l12', 'quiz[1].widget.answer', apply(5, [(0, 2, 5), (1, 3, -2)])[2])

# ---------- review-3 ----------
E('review', 'items[0].explain.text', 4); E('review', 'items[0].explain.text', 4 * 5)
assert 3 not in reach(4, 5) and 13 in reach(4, 5)
RM = [(0, 7), (1, 3), (3, 5), (5, 8), (8, 10), (4, 9)]
E('review', 'items[2].widget.answer', max(r_ for r_ in range(7) for c_ in itertools.combinations(RM, r_) if compatible(c_)))
E('review', 'items[3].widget.answer', first_fail([1, 5, 6]))                         # 10
assert greedy([1, 5, 6], 10) == 5 and fewest([1, 5, 6], 10) == 2
assert greedy([1, 5, 6], 15) == 5 and fewest([1, 5, 6], 15) == 3
assert [i for i in range(5) if 22 >> i & 1] == [1, 2, 4]
E('review', 'items[4].explain.text', 16 + 4 + 2)
dr = [0] * 7
for l, r_, x in [(0, 5, 2), (2, 2, 5), (3, 5, -1)]:
    dr[l] += x; dr[r_ + 1] -= x
E('review', 'items[6].explain.text', ', '.join(map(str, dr)).replace('-', '−'))
E('review', 'items[6].explain.text', ', '.join(map(str, list(accumulate(dr))[:6])))
E('review', 'items[6].widget.answer', apply(6, [(0, 5, 2), (2, 2, 5), (3, 5, -1)])[3])

# ---------- homework-3 ----------
r = random.Random(31); hw = []
for _ in range(200000):
    s = r.randint(0, 10**9); hw.append((s, s + r.randint(0, 10**5)))
# fewest stabbing points = most pairwise disjoint closed windows (duality), by DP with bisect
srt = sorted(hw, key=lambda x: x[1]); ends = [e for _, e in srt]; dp = [0] * (len(srt) + 1)
for i, (s, e) in enumerate(srt):
    j = bisect.bisect_left(ends, s, 0, i)
    dp[i + 1] = max(dp[i], dp[j] + 1)
E('homework', 'items[0].explain.text', dp[-1])                                       # 35,817
E('homework', 'items[4].widget.model', dp[-1])
def spans_brute(xs):
    out = []
    for i in range(len(xs)):
        j = i
        while j >= 0 and xs[j] <= xs[i]:
            j -= 1
        out.append(i - j)
    return out
E('homework', 'items[1].widget.tests[0].expect', ', '.join(map(str, spans_brute([100, 80, 60, 70, 60, 75, 85]))))
E('homework', 'items[1].widget.tests[7].expect', 200000 * 200001 // 2)
r = random.Random(33); cl = [r.randint(1, 1000) for _ in range(200000)]
st, tot = [], 0
for i, c in enumerate(cl):          # previous-greater by stack of (value, index), written afresh
    while st and st[-1][0] <= c:
        st.pop()
    tot += i - (st[-1][1] if st else -1); st.append((c, i))
E('homework', 'items[1].widget.tests[8].expect', tot)
r = random.Random(35); hu = []
for _ in range(100000):
    a, b = r.randint(0, 199999), r.randint(0, 199999); hu.append((min(a, b), max(a, b), r.randint(1, 10)))
def over_after(k, cap):
    d_ = [0] * 200001
    for l, r_, x in hu[:k]:
        d_[l] += x; d_[r_ + 1] -= x
    return max(accumulate(d_[:200000])) > cap
for t, cap in [(7, 100000), (8, 200000)]:
    want = int(lv.text('homework', f'items[2].widget.tests[{t}].expect'))
    assert over_after(want, cap) and not over_after(want - 1, cap), cap
    E('homework', f'items[2].widget.tests[{t}].expect', want)
assert not over_after(100000, 10**9)
E('homework', 'items[2].explain.text', 17); assert abs(__import__('math').log2(10**5) - 16.6) < 0.1
E('homework', 'items[5].widget.answer', 2 ** 12 * 12)
E('homework', 'items[5].explain.text', sum(bin(m).count('1') for m in range(1 << 12)))
E('homework', 'items[5].widget.wrong[0].value', __import__('math').factorial(12))
for n in range(1, 8):
    has = any(all(p[i] != i + 1 for i in range(n)) for p in itertools.permutations(range(1, n + 1)))
    assert has == (n != 1)
assert [3, 2, 1][1] == 2 and [2, 3, 1] != [1, 2, 3]   # reverse fixes 2 at n = 3; the shift does not
E('homework', 'items[7].widget.options[2].why', 4, fmt='4 \\cdot 10^{{10}}')

lv.check_wrongs()
lv.report()
