"""Second-reader number checks for contests level 4 (l13 to l16, review-4, homework-4).

Every value is recomputed here in CPython with code written for this script: brute force on small cases, and a
different algorithm from the shipped solution on each size case, rebuilt from the seeds in the test's setup (the
generators below copy the preludes' seeded generators). Each value is then looked up where the content states it
(app/tools/numbers_lib.py). check_wrongs() checks every numeric wrong[] value. No shipped solution is imported.
Run: python3 docs/reports/contests-L4-numbers.py
"""
import bisect, itertools, math, os, random, sys
from collections import deque
from itertools import accumulate
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk, _numbers

lv = Level('contests', 4)
E = lv.expect


def K(ref, path, key, value):
    """A feedback.byKey line whose key has a hyphen (test-9): look the key up directly."""
    _, doc = lv._file(ref)
    txt = _walk(doc, path)[0].get(key, '')
    ok = any(abs(x - value) <= 1e-9 * max(1.0, abs(value)) for x in _numbers(txt))
    return lv._rec(ok, f'{ref} {path}.{key} = {value!r}', '' if ok else f'not found in: {txt[:120]!r}')


def closes(n, seed, lo=1, hi=10**9):
    g = random.Random(seed)
    return [g.randint(lo, hi) for _ in range(n)]

# ---------- l13: the virtual contest ----------
def peaks(xs):
    return sum(1 for a, b, c in zip(xs, xs[1:], xs[2:]) if b > a and b > c)
E('l13', 'screens[3].widget.tests[0].expect', peaks([3, 5, 4, 6, 2]))
E('l13', 'screens[1].widget.answer', peaks([5, 1, 5]))
E('l13', 'screens[3].widget.tests[8].expect', peaks(closes(200000, 13)))           # 66,543
E('l13', 'screens[3].widget.tests[9].expect', peaks(closes(200000, 14, 1, 3)))     # 37,237
E('l13', 'quiz[2].widget.answer', peaks([2, 2, 3, 3, 2]))
def tape(n, seed, rare='ZZZ'):
    g = random.Random(seed); names = [chr(65 + i) * 3 for i in range(25)]
    return [g.choice(names) for _ in range(n - 1)] + [rare]
ALL = [chr(65 + i) * 3 for i in range(25)] + ['ZZZ']
def cover(t, need):
    # shortest window ending at each right end: right - min(last seen of each needed name) + 1
    need = set(need); last = {}; best = -1
    for r, x in enumerate(t):
        if x in need:
            last[x] = r
        if len(last) == len(need):
            w = r - min(last.values()) + 1
            best = w if best == -1 else min(best, w)
    return best
E('l13', 'screens[4].widget.tests[0].expect', cover('AAA BBB AAA CCC BBB'.split(), ['BBB', 'CCC']))
E('l13', 'quiz[1].widget.answer', cover('AAA BBB AAA CCC BBB'.split(), ['AAA', 'BBB', 'CCC']))
E('l13', 'screens[4].widget.tests[7].call', cover(tape(2000, 22), ALL))               # 79
E('l13', 'screens[4].widget.tests[8].expect', cover(tape(200000, 21), ALL))           # 75
E('l13', 'screens[4].explain.text', 2, fmt='2 \\cdot 10^{{10}}'); assert 200000 ** 2 // 2 == 2 * 10**10
def days_needed(w, cap):
    days, load = 1, 0
    for x in w:
        if load + x > cap:
            days, load = days + 1, 0
        load += x
    return days
def min_cap(w, k):
    # smallest capacity by trying the answer's candidates through bisect on the monotone predicate
    lo, hi, calls = max(w), sum(w), 0
    while lo < hi:
        mid = (lo + hi) // 2; calls += 1
        if days_needed(w, mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo, calls
assert days_needed([4, 8, 2, 7, 5, 3], 11) == 4 and days_needed([4, 8, 2, 7, 5, 3], 12) <= 3
E('l13', 'screens[5].widget.tests[0].expect', min_cap([4, 8, 2, 7, 5, 3], 3)[0])
K('l13', 'screens[5].feedback.byKey', 'test-2', days_needed([4, 8, 2, 7, 5, 3], 11))
w40 = closes(40, 32, 1, 100)
ans40, calls40 = min_cap(w40, 2)
E('l13', 'screens[5].widget.tests[8].expect', ans40)                                  # 909
E('l13', 'screens[5].widget.how', sum(w40))                                           # 1,807
E('l13', 'screens[5].explain.text', calls40); E('l13', 'screens[5].explain.text', max(w40))
E('l13', 'screens[5].explain.text', ans40 - max(w40) + 1)                             # 811
assert all(days_needed(w40, c) > 2 for c in range(max(w40), ans40))                    # every smaller capacity fails
w100k = closes(100000, 31, 1, 10**4)
pre = list(accumulate(w100k, initial=0))
def days_fast(cap):
    i, d = 0, 0
    while i < len(w100k):
        i = bisect.bisect_right(pre, pre[i] + cap) - 1; d += 1
    return d
lo, hi = max(w100k), sum(w100k)
while lo < hi:
    mid = (lo + hi) // 2
    lo, hi = (lo, mid) if days_fast(mid) <= 500 else (mid + 1, hi)
E('l13', 'screens[5].widget.tests[10].expect', lo)                                     # 1,002,823
E('l13', 'quiz[0].explain.text', 1.07, fmt='1.07'); assert 2 ** 30 > 10**9 and abs(2 ** 30 / 1e9 - 1.07) < 0.01
E('l13', 'quiz[0].explain.text', 3, fmt='3 \\cdot 10^6')
STEP = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
def bfs(g, arrows=True):
    R, C = len(g), len(g[0]); dist = {(0, 0): 0}; q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for dr, dc in ([STEP[g[r][c]]] if arrows and g[r][c] in STEP else STEP.values()):
            a, b = r + dr, c + dc
            if 0 <= a < R and 0 <= b < C and g[a][b] != '#' and (a, b) not in dist:
                dist[(a, b)] = dist[(r, c)] + 1; q.append((a, b))
    return dist.get((R - 1, C - 1), -1)
EX = ['..#.>', '.#>..', '.#.#.', '...v.']
E('l13', 'screens[6].canvas.params.lines[5]', bfs(EX))                                 # 11
K('l13', 'screens[6].feedback.byKey', 'test-1', bfs(EX, arrows=False))                 # 7
E('l13', 'quiz[3].widget.answer', bfs(['.>', 'v.']))
def city(rows, cols, seed, block=0.25, arrow=0.1):
    g = random.Random(seed); out = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            x = g.random()
            row.append('#' if x < block else (g.choice('><^v') if x < block + arrow else '.'))
        out.append(row)
    out[0][0] = '.'; out[-1][-1] = '.'
    return [''.join(r) for r in out]
E('l13', 'screens[6].widget.tests[8].expect', bfs(city(400, 500, 40)))                 # 908
K('l13', 'screens[6].feedback.byKey', 'test-9', 400 * 500)                               # 200,000 cells
sam = {'open D': 0, 'wa1': 38, 'wa2': 51, 'open A': 52, 'ac A': 59}
E('l13', 'screens[7].explain.text', sam['open A'] - sam['open D'])                    # 52
E('l13', 'screens[7].widget.options[3].why', sam['wa2'] - sam['wa1'])                 # 13
E('l13', 'screens[7].hints[0].text', 'seven'); assert sam['ac A'] - sam['open A'] == 7
LOG = {'A': (2, 6, 1, 0), 'B': (4, 9, 4, 1), 'C': (5, 10, 12, 2), 'D': (5, 2, 0, 0)}
tots = [sum(v[i] for v in LOG.values()) for i in range(4)]
for c, t in zip(range(1, 4), tots):              # Read, Code, Debug (finding 19 moves Wrong into the prose)
    E('l13', f'screens[8].widget.rows[4][{c}].answer', t)
assert tots[3] == 3
assert sum(tots[:3]) == 60
# review-contests-3-4 finding 13: 75 minutes for 3 problems is 25 each, and 4 / 25 is about a sixth, not a tenth.
assert round(25 / 4) == 6
E('l13', 'screens[10].widget.options[3].text', 'a sixth')   # fails until the fix lands
E('l13', 'screens[8].explain.text', LOG['C'][2])

# ---------- l14: which problem first ----------
V = {'A': (500, 10), 'B': (1000, 20), 'C': (1500, 35), 'D': (2000, 50)}
def sc(v, minute, wrong=0, floor=0.3, per_wrong=50):
    return max(floor * v, v - v / 250 * minute - per_wrong * wrong)
def run(order, limit=10**9):
    t, out = 0, {}
    for p in order:
        t += V[p][1]; out[p] = sc(V[p][0], t) if t <= limit else 0
    return out
for i, p in enumerate('ABCD'):
    E('l14', f'screens[0].canvas.params.rows[{i}][3]', V[p][0] / 250)
abcd, dcba, cabd, abdc = run('ABCD'), run('DCBA'), run('CABD'), run('ABDC')
for fr, o in [(0, abcd), (1, dcba), (2, cabd)]:
    for p, v in o.items():
        E('l14', f'screens[1].canvas.controls[0].frames[{fr}].values.{p}', v)
    E('l14', f'screens[1].canvas.controls[0].frames[{fr}].caption', sum(o.values()))
E('l14', 'screens[1].explain.text', sum(abcd[p] - dcba[p] for p in 'ABC'))            # 630
E('l14', 'screens[9].explain.text', sum(abdc.values()))                               # 3,530
E('l14', 'screens[2].widget.rows[2][1].answer', 1500 / 35, fmt='42.857')
E('l14', 'screens[2].widget.rows[3][1].answer', 2000 / 50)
E('l14', 'screens[0].hints[2].text', round(1500 / 35))
E('l14', 'screens[3].widget.answer', sc(1000, 35, 1))                                 # 810
E('l14', 'screens[3].widget.wrong[0].value', sc(1000, 35, 0)); E('l14', 'screens[3].widget.wrong[2].value', sc(1000, 35, 2))
for t, args in enumerate([(1000, 35, 1, 4, 50, .3), (500, 120, 3, 2, 50, .3), (1000, 0, 0, 4, 50, .3), (2000, 110, 2, 8, 50, .3),
                          (1000, 175, 0, 4, 50, .3), (1500, 200, 4, 6, 50, .3), (1000, 300, 0, 4, 50, 0), (750, 10, 0, 3, 50, .3)]):
    v, m, w, pm, pw, fl = args
    E('l14', f'screens[4].widget.tests[{t}].expect', max(fl * v, v - pm * m - pw * w))
K('l14', 'screens[4].feedback.byKey', 'test-2', 500 - 2 * 120 - 50 * 3)                 # 110
K('l14', 'screens[4].feedback.byKey', 'test-6', 1500 - 6 * 200 - 50 * 4)                # 100
def icpc(res, pw=20):
    s = [(m, w) for m, w in res if m is not None]
    return len(s), sum(m + pw * w for m, w in s)
E('l14', 'screens[5].widget.tests[0].expect', icpc([(12, 0), (41, 1), (95, 2), (None, 3)])[1])   # 208
X, Y, Z = icpc([(15, 0), (50, 2), (90, 0)]), icpc([(20, 0), (45, 0), (100, 1)]), icpc([(60, 0), (70, 0), (80, 0), (190, 0)])
E('l14', 'quiz[1].widget.options[0].text', X[1]); E('l14', 'quiz[1].widget.options[0].text', Y[1])
K('l14', 'screens[5].feedback.byKey', 'test-7', Z[1])                                     # 400
assert sorted([('X', X), ('Y', Y), ('Z', Z)], key=lambda t: (-t[1][0], t[1][1]))[0][0] == 'Z'
f = lambda x: 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))
a, b = 0.0, 60.0
for _ in range(200):                                    # golden-section search for the maximum
    c1, c2 = b - (b - a) / 1.618034, a + (b - a) / 1.618034
    a, b = (c1, b) if f(c1) < f(c2) else (a, c2)
xs = (a + b) / 2
E('l14', 'screens[6].widget.points[0].target.x', round(xs, 2))                         # 34.84
E('l14', 'screens[6].explain.canvas.points.p.y', round(f(xs), 1))                       # 1,152.3
E('l14', 'screens[6].hints[2].text', round(f(xs)))
E('l14', 'screens[6].explain.text', round(f(60))); E('l14', 'screens[6].explain.text', round(f(0)))
E('l14', 'screens[6].canvas.state.points[0].y', f(10))
E('l14', 'screens[8].feedback.correct', 'seven'); assert int(702 / 96) == 7
E('l14', 'screens[9].widget.answer', -(2000 * 35 - 1500 * 50) / 250)
E('l14', 'screens[9].hints[2].text', 2000 * 35 - 1500 * 50)
assert sum(abcd.values()) - sum(abdc.values()) == 20
def best_order(probs, minutes):
    best = None
    for order in itertools.permutations(probs):
        t = tot = 0
        for nm, v, d in order:
            t += d
            if t <= minutes:
                tot += max(0.3 * v, v - v / 250 * t)
        key = (-tot, [o[0] for o in order])
        best = key if best is None or key < best else best
    return -best[0], best[1]
P = [('A', 500, 10), ('B', 1000, 20), ('C', 1500, 35), ('D', 2000, 50)]
for t, (probs, mins) in enumerate([(P, 120), (P, 60), (P[::-1], 120), ([('A', 500, 10)], 5), ([('P', 750, 25), ('Q', 1250, 50)], 120),
                                   ([('A', 500, 8), ('B', 1000, 15), ('C', 1500, 40), ('D', 2000, 60), ('E', 2500, 30), ('F', 3000, 90)], 180)]):
    tot, names = best_order(probs, mins)
    E('l14', f'screens[10].widget.tests[{t}].expect', tot)
    E('l14', f'screens[10].widget.tests[{t}].expect', ', '.join(repr(n) for n in names))
E('l14', 'screens[10].explain.text', run('AB')['A'] + run('AB')['B'])                   # 1,360
E('l14', 'screens[11].hints[2].text', 3000 / 5); E('l14', 'screens[11].hints[2].text', 12000 / 25); E('l14', 'screens[11].hints[2].text', 2000 / 20)
E('l14', 'quiz[0].widget.answer', sc(1000, 180, 1)); E('l14', 'quiz[0].widget.accept', 1000 - 720 - 50)
E('l14', 'quiz[0].widget.wrong[1].value', 1000 - 720)
E('l14', 'quiz[2].explain.text', 750 / 25); E('l14', 'quiz[2].explain.text', 1250 / 50)

# ---------- l15: debugging under time ----------
def buggy_last(xs, x):
    for i in range(len(xs) - 2, -1, -1):
        if xs[i] == x:
            return i
    return -1
def last(xs, x):
    return max([i for i, v in enumerate(xs) if v == x], default=-1)
cases = [([5], 5), ([3, 3, 3], 3), ([10**9, 10**9, 1], 10**9), ([4, 7], 9)]
rows = [(last(*c), buggy_last(*c)) for c in cases]
assert rows == [(0, -1), (2, 1), (1, 1), (-1, -1)]
E('l15', 'screens[1].widget.answer', sum(1 for e, y in rows if e != y))
E('l15', 'screens[3].widget.tests[0].expect', last([4, 7, 7, 1], 7))
xs81 = closes(1500, 81, 1, 5)
cnt, inv = [0] * 6, 0
for v in xs81:                                   # inversions by counting larger earlier values
    inv += sum(cnt[v + 1:]); cnt[v] += 1
E('l15', 'screens[4].widget.tests[6].expect', inv)                                     # 435,115
E('l15', 'screens[4].widget.how', 1.1, fmt='1.1 million'); assert abs(1500 * 1499 / 2 / 1e6 - 1.12) < 0.01
E('l15', 'screens[4].widget.tests[5].expect', sum(1 for i, j in itertools.combinations(range(4), 2) if [2, 1, 2, 1][i] > [2, 1, 2, 1][j]))
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        c = gen(rng)
        if fast(list(c)) != brute(list(c)):
            return c
    return None
inv_b = lambda a: sum(1 for i, j in itertools.combinations(range(len(a)), 2) if a[i] > a[j])
ties = lambda a: sum(1 for i, j in itertools.combinations(range(len(a)), 2) if a[i] >= a[j])
nolast = lambda a: inv_b(a[:-1])
adj = lambda a: sum(1 for i in range(len(a) - 1) if a[i] > a[i + 1])
gl = lambda rng, n: [rng.randint(1, 3) for _ in range(n)]
gw = lambda rng, n: [rng.randint(1, 10**6) for _ in range(n)]
def smallest(fast, gen, seed):
    for n in range(1, 9):
        c = stress(fast, inv_b, lambda rng: gen(rng, n), 200, seed)
        if c is not None:
            return c
for t, (fast, gen, seed) in enumerate([(ties, gl, 1), (nolast, gl, 1), (adj, gl, 1), (adj, gl, 4), (inv_b, gl, 1), (ties, gw, 3),
                                       (lambda a: inv_b(a) if len(a) < 5 else -1, gl, 2)]):
    E('l15', f'screens[9].widget.tests[{t}].expect', repr(smallest(fast, gen, seed)))
E('l15', 'quiz[0].explain.text', 2, fmt='2 \\cdot 10^{{14}}'); assert 2 * 10**5 * 10**9 == 2 * 10**14
E('l15', 'quiz[0].widget.options[1].why', 2 ** 31 - 1)
E('l15', 'quiz[0].explain.text', 9.2, fmt='9.2'); assert abs((2 ** 63 - 1) / 1e18 - 9.22) < 0.01
E('l15', 'quiz[3].widget.answer', adj([3, 2, 1])); E('l15', 'quiz[3].widget.wrong[0].value', inv_b([3, 2, 1]))

# ---------- l16: upsolving ----------
def thirds(a):
    n = len(a); P = list(accumulate(a, initial=0)); S = P[-1]
    if S % 3:
        return 0
    firsts = [i for i in range(1, n) if P[i] == S // 3]
    return sum(bisect.bisect_left(firsts, j) for j in range(1, n) if P[j] == 2 * S // 3)
E('l16', 'screens[3].widget.tests[0].expect', thirds([1, 2, 3, 0, 3]))
E('l16', 'screens[1].widget.answer', thirds([0] * 5)); assert math.comb(4, 2) == 6
E('l16', 'screens[1].widget.wrong[0].value', math.comb(5, 2)); E('l16', 'screens[1].widget.wrong[1].value', thirds([0] * 4))
E('l16', 'quiz[0].widget.answer', thirds([0] * 4))
E('l16', 'screens[1].hints[2].text', math.comb(199999, 2)); assert thirds([0] * 2000) == math.comb(1999, 2)
E('l16', 'screens[3].widget.tests[7].expect', math.comb(199999, 2))
E('l16', 'screens[3].widget.tests[8].expect', thirds(closes(200000, 92, -1, 1)))      # 97,944
for t, a in [(2, [1, 1]), (3, [3, 3, 3]), (4, [2, -2] * 4 + [2]), (5, [1, -1] * 3), (6, [5])]:
    E('l16', f'screens[3].widget.tests[{t}].expect', thirds(a))
K('l16', 'screens[3].feedback.byKey', 'test-5', sum([2, -2] * 4 + [2]))
LG = ['misread a constraint', 'forgot n = 1', 'greedy without proof', 'forgot n = 1', 'overflow', 'misread a constraint', 'greedy without proof', 'forgot n = 1']
for i, cat in enumerate(['forgot n = 1', 'misread a constraint', 'greedy without proof', 'overflow']):
    E('l16', f'screens[4].widget.rows[{i}][1].answer', LG.count(cat))
E('l16', 'screens[4].feedback.correct', 'eight'); assert len(LG) == 8
E('l16', 'screens[6].hints[1].text', 1200 + 300)
E('l16', 'screens[6].hints[2].text', 1900 - 1200); E('l16', 'screens[6].hints[2].text', 2400 - 1200)
E('l16', 'screens[7].hints[1].text', 1250 + 100); E('l16', 'screens[7].hints[1].text', 1250 + 200)
E('l16', 'screens[7].widget.options[3].why', 2000 - 1250)
E('l16', 'screens[11].feedback.byKey.rating', 1800 - 1410)
E('l16', 'quiz[1].explain.text', 1500 + 300); E('l16', 'quiz[1].widget.options[1].why', 2100 - 1500)

# ---------- review-4 ----------
E('review', 'items[0].widget.options[3].why', 2, fmt='2 \\cdot 10^{{14}}')
E('review', 'items[1].widget.answer', 18 / 60); E('review', 'items[1].widget.wrong[0].value', 30 / 60); E('review', 'items[1].widget.wrong[1].value', 18 / 30)
E('review', 'items[2].widget.answer', sc(1500, 48, 2))                                 # 1,112
E('review', 'items[2].widget.wrong[0].value', sc(1500, 48, 0)); E('review', 'items[2].widget.wrong[1].value', sc(1500, 48, 1))
E('review', 'items[2].explain.text', 0.3 * 1500)
def two(order):                  # P worth 1,000 in 40 minutes, Q worth 500 in 15
    T = {'P': (1000, 40), 'Q': (500, 15)}; t = tot = 0
    for p in order:
        t += T[p][1]; tot += T[p][0] - T[p][0] / 250 * t
    return tot
E('review', 'items[3].widget.answer', two('QP') - two('PQ'))
E('review', 'items[3].explain.text', 1000 / 250 * 15); E('review', 'items[3].explain.text', 500 / 250 * 40)
E('review', 'items[3].explain.text', round(500 / 15))
E('review', 'items[4].widget.options[1].why', sum([2, 2, 2][1:]))
E('review', 'items[5].explain.text', 'nine'); assert int(math.comb(199999, 2) / (2 ** 31 - 1)) == 9
assert math.comb(199999, 2) < 2 ** 53                                                    # a double holds it exactly
E('review', 'items[6].explain.text', 1350 + 300)
E('review', 'items[6].widget.options[2].why', 1900 - 1350); E('review', 'items[6].widget.options[3].why', 2300 - 1350)
E('review', 'items[7].widget.answer', sc(1250, 95 + 20))                               # 675
E('review', 'items[7].widget.wrong[0].value', 1250 - 5 * 20); E('review', 'items[7].widget.wrong[1].value', 0.3 * 1250)

# ---------- homework-4 ----------
def groups(n, links, cut):
    par = list(range(n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    g = n
    for i, (a, b) in enumerate(links):
        if i != cut:
            ra, rb = find(a), find(b)
            if ra != rb:
                par[ra] = rb; g -= 1
    return g
E('homework', 'items[0].widget.tests[0].expect', groups(4, [(0, 1), (1, 2), (2, 3), (3, 0)], 0))
E('homework', 'items[0].widget.tests[1].expect', groups(4, [(0, 1), (1, 2)], 1))
E('homework', 'items[0].widget.tests[6].expect', groups(200000, [(i, i + 1) for i in range(199999)], 100000))
g51 = random.Random(51); L51 = [(g51.randrange(200000), g51.randrange(200000)) for _ in range(200000)]
E('homework', 'items[0].widget.tests[7].expect', groups(200000, L51, 7))               # 32,360
def kprofit(p, k):
    # dp over trades with the running best of dp[t-1][j] - p[j], a different form from the shipped one
    n = len(p)
    if n < 2 or k == 0:
        return 0
    prev = [0] * n
    for _ in range(k):
        cur, best = [0] * n, -p[0]
        for i in range(1, n):
            cur[i] = max(cur[i - 1], p[i] + best)
            best = max(best, prev[i] - p[i])
        prev = cur
    return prev[-1]
E('homework', 'items[1].widget.tests[0].expect', kprofit([3, 2, 6, 5, 0, 3], 2))
E('homework', 'items[1].widget.tests[1].expect', kprofit([3, 2, 6, 5, 0, 3], 1))
E('homework', 'items[1].widget.tests[5].expect', kprofit([1, 3, 2, 5, 4, 8], 10))
E('homework', 'items[1].widget.tests[7].expect', kprofit(closes(10000, 61, 1, 1000), 20))   # 19,958
E('homework', 'items[1].explain.text', 2, fmt='2 \\cdot 10^5'); assert 10**4 * 20 == 2 * 10**5
K('homework', 'items[1].feedback.byKey', 'test-8', 2); assert 10**8 * 20 == 2 * 10**9
def gap(levels, m):
    xs = sorted(levels)
    def fits(d):
        i, placed = 0, 1
        while placed < m:
            i = bisect.bisect_left(xs, xs[i] + d, i + 1)
            if i == len(xs):
                return False
            placed += 1
        return True
    lo, hi = 0, xs[-1] - xs[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        lo, hi = (mid, hi) if fits(mid) else (lo, mid - 1)
    return lo
for t, (lv_, m) in enumerate([([1, 2, 8, 4, 9], 3), ([1, 2, 8, 4, 9], 2), ([1, 2, 8, 4, 9], 5), ([5, 5, 5], 2), ([10, 1], 2),
                               ([1, 3, 5, 7, 9, 11], 4), ([7, 1, 1, 7, 4], 3)]):
    E('homework', f'items[2].widget.tests[{t}].expect', gap(lv_, m))
E('homework', 'items[2].widget.tests[7].expect', gap(closes(200000, 71), 1000))        # 996,391
pen = 8 + 27 + 64 + 110
E('homework', 'items[4].widget.answer', pen + 20 * 3); E('homework', 'items[4].widget.wrong[0].value', pen + 20 * 7)
E('homework', 'items[4].explain.text', pen)
for p, mins in [('A', 9), ('B', 17), ('C', 27)]:
    assert sum(LOG[p][:3]) == mins
    E('homework', 'items[6].widget.model', mins)
E('homework', 'items[6].widget.model', 60 - 9 - 17 - 27)                                # 7 left for D

# ---------- fix pass (review-contests-3-4) ----------
# finding 13: 75 minutes for 3 problems is 25 each; 4 / 25 = 0.16, about a sixth (1/6 = 0.167)
assert 75 / 3 == 25 and abs(4 / 25 - 1 / 6) < 0.01 and abs(4 / 25 - 1 / 10) > 0.05
E('l13', 'screens[10].widget.options[3].text', 'a sixth of a problem')
# finding 14: the ends-counting slip first fails test 3, the two-close case 4 9
def peaks_ends(c): return sum(1 for i in range(len(c)) if (i == 0 or c[i] > c[i - 1]) and (i == len(c) - 1 or c[i] > c[i + 1]))
assert peaks_ends([4, 9]) == 1 and peaks_ends([5, 1, 5]) == 2
K('l13', 'screens[3].feedback.byKey', 'test-3', 9)
E('l13', 'screens[2].widget.options[2].why', 'previous screen')
# finding 18: the problem A statement is one sentence per line; the note is line 6 and the description line 2
import json as _j
_a = _j.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'contests', 'l13-virtual-contest.json')))
assert _a['screens'][1]['canvas']['params']['lines'][5].startswith('Note: the first and last days')
assert _a['screens'][1]['hints'][1]['highlight'] == ['l6']
for _s in (3, 4, 5):
    assert _a['screens'][_s]['hints'][1]['highlight'] == ['l2'] and len(_a['screens'][_s]['canvas']['params']['lines']) <= 6
assert [len(r) for r in _a['screens'][8]['widget']['rows']] == [4] * 5 and _a['screens'][8]['widget']['columns'] == ['Problem', 'Read', 'Code', 'Debug']
# finding 19: the Wrong column is in the prose now: none on A and D, one on B, two on C
assert [LOG[p][3] for p in 'ABCD'] == [0, 1, 2, 0]
E('l13', 'screens[8].prose', 'one on B and two on C')
E('l13', 'screens[8].hints[2].text', tots[0]); E('l13', 'screens[8].hints[2].text', tots[1]); E('l13', 'screens[8].hints[2].text', tots[2]); E('l13', 'screens[8].hints[2].text', sum(tots[:3]))
E('l13', 'screens[8].feedback.correct', sum(tots[:3]))
# finding 12: numbers added to the explanations
E('l14', 'screens[1].explain.text', sum(dcba.values())); E('l14', 'screens[1].explain.text', sum(abcd.values()))
assert sum(dcba.values()) == 3440 and sum(abcd.values()) == 3550 and dcba['D'] == 1600 and abcd['D'] == 1080
E('l16', 'screens[1].explain.text', thirds([0] * 5)); E('l16', 'screens[1].explain.text', 2, fmt='2 \\cdot 10^{{10}}')
assert abs(math.comb(199999, 2) / 2e10 - 1) < 0.01
E('homework', 'items[4].explain.text', pen + 20 * 3)
# finding 20, 24, 25
E('l14', 'screens[9].prose', 'neither score is at its floor'); E('l14', 'screens[9].explain.text', "lesson 10's exchange argument")
E('l16', 'screens[1].canvas.controls[0].frameLabels', 'test 9')
# finding 22
E('l15', 'screens[9].explain.text', 'almost never tie')
# finding 23, 26, 27
E('l16', 'screens[0].prose', 'five-problem virtual round')
E('review', 'items[3].prose', 1000); E('review', 'items[3].prose', 40); E('review', 'items[3].prose', 500); E('review', 'items[3].prose', 15); E('review', 'items[3].prose', 250)
E('homework', 'items[5].widget.options[0].text', 1380); E('homework', 'items[5].widget.options[0].text', 1600); E('homework', 'items[5].prose', 1380)

lv.check_wrongs()
lv.report()
