"""Replacement review and homework numbers for the fix pass, each computed by two methods."""
import collections, heapq, itertools, random, bisect
from refs import ns
def two(name, a, b):
    assert a == b, (name, a, b); print(name, a); return a
# ---- R1.7 kth_largest_stream(3, [6,1,9,5], [2,7,12,8,3])
g = ns('l1.py', 'KL_REF'); kref = g['kth_largest_stream']
def kth_sort(k, init, adds):
    cur = list(init); out = []
    for a in adds:
        cur.append(a); out.append(sorted(cur, reverse=True)[k - 1])
    return out
r = kref(3, [6, 1, 9, 5], [2, 7, 12, 8, 3]); two('R1.7', r, kth_sort(3, [6, 1, 9, 5], [2, 7, 12, 8, 3])); print(' answers', r, 'sum', sum(r))
# ---- H1.2 two_singles replacement example
g = ns('l1.py', 'TS_REF'); ts = g['two_singles']
x = [8, 3, 5, 3, 7, 5]; print('two_singles', ts(x), sorted(v for v in set(x) if x.count(v) == 1))
# ---- H1.3 shortest_at_least
g = ns('l1.py', 'SA_REF'); sa = g['shortest_at_least']
def sa_b(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k and (best == -1 or j - i + 1 < best): best = j - i + 1
    return best
for nums, k in (([57, -21, 30, 45, 88], 150), ([57, -21, 30, 45, 88], 160), ([9, -4, 7, 2, -6, 11], 12)):
    print('sa', nums, k, two('sa', sa(nums, k), sa_b(nums, k)))
# ---- R2.1
g = ns('l2.py', 'FA_REF'); fa = g['find_anagrams']
def fa_b(s, p):
    return [i for i in range(len(s) - len(p) + 1) if sorted(s[i:i + len(p)]) == sorted(p)]
print('fa abcbac abc', two('fa', fa('abcbac', 'abc'), fa_b('abcbac', 'abc')))
# ---- R2.9 rotation index
def rot_cw(r, c, n): return (c, n - 1 - r)
def rot_ccw(r, c, n): return (n - 1 - c, r)
def rot_half(r, c, n): return (n - 1 - r, n - 1 - c)
n = 5
print('R2.9 (1,4): cw', rot_cw(1, 4, n), 'transpose', (4, 1), 'ccw', rot_ccw(1, 4, n), 'half', rot_half(1, 4, n))
m = [[r * 5 + c for c in range(5)] for r in range(5)]
rot = [list(row) for row in zip(*m[::-1])]      # clockwise by library idiom
two('R2.9 cw', [(i, j) for i in range(5) for j in range(5) if rot[i][j] == m[1][4]][0], rot_cw(1, 4, 5))
# ---- H2.5 spiral last entry of a 250 by 400 matrix
g = ns('l2.py', 'SO_REF'); so = g['spiral_order']
def spiral_walk(R, C):
    seen = set(); r = c = 0; dr, dc = 0, 1; last = None
    for _ in range(R * C):
        seen.add((r, c)); last = r * C + c
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen: dr, dc = dc, -dr; nr, nc = r + dr, c + dc
        r, c = nr, nc
    return last
mm = [[r * 400 + c for c in range(400)] for r in range(250)]
two('H2.5 spiral 250x400 last', so(mm)[-1], spiral_walk(250, 400))
# ---- H2.4/H2.8 new bot list
g = ns('l2.py', 'RS_REF'); rs = g['run_strategy']
def rs_variant(prices, hold_cmp):
    pos = None; profit = 0; trades = 0
    for i, p in enumerate(prices):
        if i == 0: continue
        if pos is None:
            if p < prices[i - 1]: pos = (i, p)
        else:
            b, e = pos
            if 100 * p >= 105 * e or 100 * p <= 97 * e or hold_cmp(i - b):
                profit += p - e; trades += 1; pos = None
    if pos is not None: profit += prices[-1] - pos[1]; trades += 1
    return [profit, trades]
P = [60, 59, 59, 60, 58, 58, 57, 61]
print('H2.8 bot', rs(P), rs_variant(P, lambda h: h == 3), 'rule >3', rs_variant(P, lambda h: h > 3), 'rule >=3', rs_variant(P, lambda h: h >= 3), 'rule ==2', rs_variant(P, lambda h: h == 2), 'rule ==4', rs_variant(P, lambda h: h == 4))
random.seed(8)
found = None
for _ in range(200000):
    P = [random.randint(95, 105) for _ in range(random.randint(7, 9))]
    res = [rs_variant(P, f) for f in (lambda h: h == 3, lambda h: h > 3, lambda h: h == 2, lambda h: h == 4, lambda h: False)]
    if len({tuple(r) for r in (res[0], res[1], res[2], res[4])}) == 4 and res[0] == rs(P):
        found = (P, res); break
print('H2.8 search', found)

# ---- H2.7 new stream and its total traded; uses the reference and the brute force of l2.py
L2 = open('l2.py').read().split('\n')
src = '\n'.join(L2[632:662])
gb = {'collections': collections}; exec(src, gb); book_brute = gb['book_brute']
gr = ns('l2.py', 'BOOK_REF'); runb, levs = gr['run_book'], gr['levels']
stream = [[0, 1, 1, 102, 3], [0, 2, 1, 101, 2], [0, 3, 0, 101, 4], [0, 4, 0, 100, 5], [1, 5, 1, 6]]
tr = runb(stream); bt = book_brute(stream)[0]
two('H2.7 trades', tr, bt); print(' total traded', sum(t[3] for t in tr), 'best bid/ask', levs(stream, 0), levs(stream, 1))

# ---- level 3 review replacements
from collections import OrderedDict
g = ns('l3.py', 'LRU_REF', 'LRU_POST'); run_lru = g['run_lru']
def lru_od(cap, ops):
    od = OrderedDict(); out = []
    for op in ops:
        if op[0] == 0:
            if op[1] in od: od.move_to_end(op[1])
            od[op[1]] = op[2]
            if len(od) > cap: od.popitem(last=False)
        else:
            if op[1] in od: od.move_to_end(op[1]); out.append(od[op[1]])
            else: out.append(-1)
    return out
ops = [[0, 2, 2], [0, 4, 4], [0, 6, 6], [1, 2], [0, 8, 8], [1, 4], [1, 6], [0, 10, 10], [1, 2], [1, 8]]
r = two('R3.1', run_lru(3, ops), lru_od(3, ops)); print(' sum', sum(r))
ex = [[0, 5, 50], [0, 6, 60], [1, 5], [0, 7, 70], [1, 6], [0, 8, 80], [1, 5], [1, 7], [1, 8]]
print('11.1 test1 new', two('lru ex', run_lru(2, ex), lru_od(2, ex)))
g = ns('l3.py', 'TTL_REF', 'TTL_POST'); run_ttl = g['run_ttl']
def ttl_b(cap, ttl, ops):
    store = []   # [key, value, last]
    out = []
    for op in ops:
        now = op[-1]
        store = [e for e in store if now - e[2] < ttl]
        if op[0] == 0:
            ex_ = [e for e in store if e[0] == op[1]]
            if ex_: ex_[0][1] = op[2]; ex_[0][2] = now; store.remove(ex_[0]); store.append(ex_[0])
            else:
                if len(store) >= cap: store.pop(0)
                store.append([op[1], op[2], now])
        else:
            ex_ = [e for e in store if e[0] == op[1]]
            if ex_: ex_[0][2] = now; store.remove(ex_[0]); store.append(ex_[0]); out.append(ex_[0][1])
            else: out.append(-1)
    return out
tops = [[0, 1, 10, 0], [1, 1, 2], [1, 1, 5], [1, 1, 6], [1, 1, 9]]
r = two('R3.3', run_ttl(2, 3, tops), ttl_b(2, 3, tops)); print(' misses', r.count(-1))
g = ns('l3.py', 'FS_REF', 'FS_POST'); run_fs = g['run_fs']
fso = [('write', '/var/a/one.txt', '123456'), ('write', '/var/a/two.txt', '12345678901'), ('write', '/var/b.txt', '1234'), ('size', '/var'), ('size', '/var/a'), ('size', '/var/b.txt'), ('size', '/')]
print('R3.4', run_fs(fso), 6 + 11 + 4)
fso2 = [('mkdir', '/y'), ('mkdir', '/x'), ('write', '/m.txt', '9'), ('write', '/y/k.txt', '9'), ('ls', '/')]
print('R3.5', run_fs(fso2), sorted(['y', 'x', 'm.txt']))
g = ns('l3.py', 'RL_REF', 'RL_POST'); run_limiter = g['run_limiter']
def rl_b(limit, window, calls):
    acc = collections.defaultdict(list); out = []
    for u, t in calls:
        c = sum(1 for x in acc[u] if x > t - window)
        if c < limit: acc[u].append(t); out.append(True)
        else: out.append(False)
    return out
calls = [['a', t] for t in [0, 1, 2, 5, 6, 7]]
r = two('R3.8', run_limiter(2, 5, calls), rl_b(2, 5, calls)); print(' accepted', sum(r))
g = ns('l3.py', 'TB_REF', 'TB_POST'); run_bucket = g['run_bucket']
def tb_b(cap, rate, times):
    tokens, clock, out = cap, 0, []
    for t in times:
        for _ in range(t - clock): tokens = min(cap, tokens + rate)
        clock = t
        if tokens >= 1: tokens -= 1; out.append(True)
        else: out.append(False)
    return out
times = [0, 0, 0, 0, 0, 1, 1, 1, 2, 9]
r = two('R3.9', run_bucket(4, 2, times), tb_b(4, 2, times)); print(' accepted', sum(r))
# LFU example replacement (H3.1 test 1)
g = ns('l3.py', 'LFU_REF', 'LRU_POST'); exec(g['run_lru'].__code__ and '', {}); import types
g = ns('l3.py', 'LFU_REF'); exec(__import__('refs').load('l3.py')['LRU_POST'].replace('LRUCache', 'LFUCache').replace('run_lru', 'run_lfu'), g); run_lfu = g['run_lfu']
src = '\n'.join(open('l3.py').read().split('\n')[344:362]); gl = {'collections': collections}; exec(src, gl); lfu_b = gl['lfu_brute']
lf1 = [[0, 5, 50], [0, 6, 60], [1, 5], [0, 7, 70], [1, 6], [1, 7], [0, 8, 80], [1, 5], [1, 7], [1, 8]]
print('LFU ex', two('lfu', run_lfu(2, lf1), lfu_b(2, lf1)))
