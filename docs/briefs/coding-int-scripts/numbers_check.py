"""Every keyed answer used in review and homework items, each computed by two independent methods."""
import collections, itertools, math, heapq, bisect, statistics, json
K = {}
def two(name, a, b):
    assert a == b, (name, a, b)
    K[name] = a
    print(f'{name}: {a}')

# ---- level 1
def merge_a(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out
def merge_b(iv):
    cov = set()
    for a, b in iv: cov.update(range(2*a, 2*b+1))
    runs = 0; prev = None
    for x in sorted(cov):
        if prev is None or x != prev + 1: runs += 1
        prev = x
    return runs
iv = [[1,5],[2,3],[4,8],[10,12],[11,15]]
two('L1 R1 merged count', len(merge_a(iv)), merge_b(iv))
mt = [[9,12],[1,4],[3,7],[6,9],[12,15]]
def rooms_a(m):
    ev = sorted([(s, 1) for s, e in m] + [(e, -1) for s, e in m]); cur = best = 0
    for t, d in ev: cur += d; best = max(best, cur)
    return best
def rooms_b(m): return max(sum(1 for s, e in m if s <= t < e) for t in range(0, 16))
two('L1 R2 rooms', rooms_a(mt), rooms_b(mt))
W = ['tea','ten','to','inn']
def nodes_a(ws):
    root = {}; n = 0
    for w in ws:
        node = root
        for c in w:
            if c not in node: node[c] = {}; n += 1
            node = node[c]
    return n
two('L1 R3 trie nodes', nodes_a(W), len({w[:i] for w in W for i in range(1, len(w)+1)}))
Ws = ['tea','ten','to','team','tear','inn','tea']
two('L1 R4 count_prefix te', sum(1 for w in set(Ws) if w.startswith('te')), len([w for w in sorted(set(Ws)) if w[:2] == 'te']))
nums = [1,3,-1,-3,5,3,6,7]
def wm_a(nums, k):
    dq, out = collections.deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(nums[dq[0]])
    return out
two('L1 R5 window max sum', sum(wm_a(nums, 3)), sum(max(nums[i:i+3]) for i in range(len(nums)-2)))
# deque size after index 4
def dq_after(nums, k, upto):
    dq = collections.deque()
    for i in range(upto + 1):
        while dq and nums[dq[-1]] <= nums[i]: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
    return list(dq)
# hand: window indices 2..4 values -1,-3,5; only index 4 can ever be the maximum while it stays
two('L1 R6 deque size after index 4', len(dq_after(nums, 3, 4)), len([i for i in range(2, 5) if all(nums[j] < nums[i] for j in range(i+1, 5))]))
def kth_a(k, init, adds):
    h = []; out = []
    for x in init:
        heapq.heappush(h, x)
        if len(h) > k: heapq.heappop(h)
    for x in adds:
        heapq.heappush(h, x)
        if len(h) > k: heapq.heappop(h)
        out.append(h[0])
    return out
def kth_b(k, init, adds):
    cur = sorted(init); out = []
    for x in adds: bisect.insort(cur, x); out.append(cur[-k])
    return out
two('L1 R7 kth stream sum', sum(kth_a(3, [4,5,8,2], [3,5,10,9,4])), sum(kth_b(3, [4,5,8,2], [3,5,10,9,4])))
K['L1 R7 kth list'] = kth_a(3, [4,5,8,2], [3,5,10,9,4])
def rm_a(s):
    lo, hi, out = [], [], []
    for x in s:
        if lo and x > -lo[0]: heapq.heappush(hi, x)
        else: heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1: heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo): heapq.heappush(lo, -heapq.heappop(hi))
        out.append(-lo[0] if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2)
    return out
s = [7,3,9,1,8,2]
two('L1 R8 running median sum', sum(rm_a(s)), sum(statistics.median(s[:i+1]) for i in range(len(s))))
K['L1 R8 list'] = rm_a(s)
def loops(n):
    c = 0
    while n: n &= n - 1; c += 1
    return c
two('L1 R9 n&(n-1) loop count for 44', loops(44), bin(44).count('1'))
two('L1 R9b 44 & 43', 44 & 43, 40)
two('L1 R10 n log n for 1e6', round(1_000_000 * math.log2(1_000_000)), round(1_000_000 * math.log(1_000_000) / math.log(2)))
two('L1 H5 set bits 0..15', sum(bin(i).count('1') for i in range(16)), 4 * 2**3)
two('L1 H6 trie bytes', 1000 * 10 * 26 * 8, sum(10 * 26 * 8 for _ in range(1000)))
def bits_total(n):   # per-bit counting
    tot = 0; b = 0
    while (1 << b) <= n:
        period = 1 << (b + 1); full = (n + 1) // period; rem = (n + 1) % period
        tot += full * (1 << b) + max(0, rem - (1 << b)); b += 1
    return tot
two('L1 H8 bits 0..100000', sum(bin(i).count('1') for i in range(100001)), bits_total(100000))
two('L1 xor 9,14,9,3,14', 9 ^ 14 ^ 9 ^ 3 ^ 14, 3)
# trie cap: distinct prefixes bound
two('L1 H pops: pushes and pops for n=100000', 100000 + 100000, 2 * 100000)

# ---- level 2
def fa(s, p): return [i for i in range(len(s)-len(p)+1) if sorted(s[i:i+len(p)]) == sorted(p)]
def fa2(s, p):
    need = collections.Counter(p); out = []
    for i in range(len(s)-len(p)+1):
        if collections.Counter(s[i:i+len(p)]) == need: out.append(i)
    return out
two('L2 R1 anagram starts', fa('cbaebabacd', 'abc'), fa2('cbaebabacd', 'abc'))
def pal_a(s):
    n = 0
    for c in range(2*len(s)-1):
        lo, hi = c//2, c//2 + c%2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]: n += 1; lo -= 1; hi += 1
    return n
two('L2 R2 palindromic substrings abba', pal_a('abba'), sum(1 for i in range(4) for j in range(i+1, 5) if 'abba'[i:j] == 'abba'[i:j][::-1]))
two('L2 R2b centres for n=4', 2*4-1, 7)
def pp(s): return sum(v % 2 for v in collections.Counter(s).values()) <= 1
def pp2(s): return any(''.join(p) == ''.join(p)[::-1] for p in set(itertools.permutations(s)))
words = ['carerac', 'abcabc', 'aabbccd', 'abcd', 'aabbcd']
two('L2 R3 palindromic perms', [w for w in words if pp(w)], [w for w in words if pp2(w)])
import ast
def calc(e):
    def ev(n):
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        a, b = ev(n.left), ev(n.right)
        if isinstance(n.op, ast.Add): return a + b
        if isinstance(n.op, ast.Sub): return a - b
        if isinstance(n.op, ast.Mult): return a * b
        q = abs(a) // abs(b); return q if (a < 0) == (b < 0) else -q
    return ev(ast.parse(e, mode='eval').body)
# second: hand: 2*(5+5*2)/3 = 2*15/3 = 10 ; 6/2+8 = 11 ; 21
two('L2 R4 calc', calc('2*(5+5*2)/3+(6/2+8)'), (2*(5+5*2))//3 + (6//2 + 8))
import re
def dec(s):
    pat = re.compile(r'(\d+)\[([a-z]*)\]')
    while pat.search(s): s = pat.sub(lambda m: m.group(2)*int(m.group(1)), s)
    return s
two('L2 R5 decode length', len(dec('2[abc]3[cd]ef')), 2*3 + 3*2 + 2)
two('L2 R6 calc -7/2', calc('-7/2'), int(-7/2))
two('L2 R6b floor', -7 // 2, -4)
def rs_a(prices):
    pnl = trades = 0; long_ = False
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i-1]: long_, entry, bought = True, p, i
        elif 100*p >= 105*entry or 100*p <= 97*entry or i - bought == 3:
            pnl += p - entry; trades += 1; long_ = False
    if long_: pnl += prices[-1] - entry; trades += 1
    return [pnl, trades]
def rs_b(prices):
    n = len(prices); i = 1; pnl = trades = 0
    while i < n:
        if prices[i] < prices[i-1]:
            e = prices[i]; sold = n - 1
            for j in range(i+1, n):
                p = prices[j]
                if 100*p >= 105*e or 100*p <= 97*e or j - i == 3: sold = j; break
            pnl += prices[sold] - e; trades += 1
            if sold == n - 1: break
            i = sold + 1
        else: i += 1
    return [pnl, trades]
pr = [100,95,100,106,90,89,95,99]
two('L2 R7 strategy', rs_a(pr), rs_b(pr))
def spiral(m):
    out = []
    while m:
        out += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return out
m = [[r*4+c+1 for c in range(4)] for r in range(3)]
def spiral2(m):
    R, C = len(m), len(m[0]); seen = set(); r = c = 0; dr, dc = 0, 1; out = []
    for _ in range(R*C):
        out.append(m[r][c]); seen.add((r, c)); nr, nc = r+dr, c+dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen: dr, dc = dc, -dr; nr, nc = r+dr, c+dc
        r, c = nr, nc
    return out
two('L2 R8 spiral 3x4', spiral([row[:] for row in m]), spiral2(m))
K['L2 R8 last'] = spiral2(m)[-1]
big = [[r*300+c for c in range(300)] for r in range(300)]
two('L2 H5 spiral 300x300 last', spiral([row[:] for row in big])[-1], spiral2(big)[-1])
m5 = [[r*5+c for c in range(5)] for r in range(5)]
rot = [list(r) for r in zip(*m5[::-1])]            # clockwise via zip
rot2 = [[m5[4-c][r] for c in range(5)] for r in range(5)]
two('L2 R9 rotation', rot, rot2)
two('L2 R9 where (0,1) goes', [(r, c) for r in range(5) for c in range(5) if rot[r][c] == m5[0][1]], [(1, 4)])
two('L2 H7 spread', 100 - 99, 1)
# order book numbers
exec(open('l2.py').read().split('# ---------- 2.5 matching engine ----------')[1].split('BOOK_START')[0].replace("BOOK_REF = '''", "BOOK_REF = '''", 1), globals()) if False else None
# ---- level 3
def lru_a(cap, ops):
    order, vals, out = [], {}, []
    for op in ops:
        if op[0] == 0:
            k, v = op[1], op[2]
            if k in vals: order.remove(k)
            elif len(order) == cap: del vals[order.pop(0)]
            order.append(k); vals[k] = v
        else:
            k = op[1]
            if k in vals: order.remove(k); order.append(k); out.append(vals[k])
            else: out.append(-1)
    return out
from collections import OrderedDict
def lru_b(cap, ops):
    d = OrderedDict(); out = []
    for op in ops:
        if op[0] == 0:
            d[op[1]] = op[2]; d.move_to_end(op[1])
            if len(d) > cap: d.popitem(last=False)
        else:
            if op[1] in d: d.move_to_end(op[1]); out.append(d[op[1]])
            else: out.append(-1)
    return out
o = [[0,1,1],[0,2,2],[1,1],[0,3,3],[1,2],[0,4,4],[1,1],[1,3],[1,4]]
two('L3 R1 lru sum', sum(lru_a(2, o)), sum(lru_b(2, o)))
K['L3 R1 list'] = lru_a(2, o)
o2 = [[0,1,1],[0,2,2],[0,3,3],[1,1],[0,4,4],[1,3]]
def evicted(cap, ops):
    order = []; ev = []
    for op in ops:
        k = op[1]
        if op[0] == 0:
            if k in order: order.remove(k)
            elif len(order) == cap: ev.append(order.pop(0))
            order.append(k)
        elif k in order: order.remove(k); order.append(k)
    return ev, order[::-1]
d = OrderedDict(); ev2 = []
for op in o2:
    if op[0] == 0:
        d[op[1]] = op[2]; d.move_to_end(op[1])
        if len(d) > 3: ev2.append(d.popitem(last=False)[0])
    elif op[1] in d: d.move_to_end(op[1])
two('L3 R2 evicted key', evicted(3, o2)[0], ev2)
K['L3 R2 recency'] = evicted(3, o2)[1]
def ttl(cap, t, ops):
    ent = OrderedDict(); out = []
    for op in ops:
        now = op[3] if op[0] == 0 else op[2]
        for k in [k for k, (v, tt) in ent.items() if now - tt >= t]: del ent[k]
        if op[0] == 0:
            if op[1] in ent: del ent[op[1]]
            elif len(ent) == cap: ent.popitem(last=False)
            ent[op[1]] = (op[2], now)
        else:
            if op[1] in ent: v, _ = ent.pop(op[1]); ent[op[1]] = (v, now); out.append(v)
            else: out.append(-1)
    return out
tt = [[0,1,10,0],[1,1,4],[1,1,8],[1,1,13],[1,1,14]]
# hand: gets at 4 (age 4 <5 live), 8 (age 4 live), 13 (age 5 expired), 14 (gone)
two('L3 R3 ttl -1 count', ttl(2, 5, tt).count(-1), 2)
K['L3 R3 list'] = ttl(2, 5, tt)
two('L3 R4 fs size /docs', 5 + 3 + 1, len('12345') + len('678') + len('9'))
two('L3 R4b size /docs/n', 5 + 3, 8)
# ledger
def led(method, trades):
    lots = []; pnl = 0
    for q, p in trades:
        if q > 0: lots.append([q, p]); continue
        left = -q
        if method == 'fifo':
            while left:
                t = min(left, lots[0][0]); pnl += t * (p - lots[0][1]); lots[0][0] -= t; left -= t
                if lots[0][0] == 0: lots.pop(0)
        else:
            tot = sum(a for a, b in lots); avg = sum(a*b for a, b in lots) / tot
            pnl += left * (p - avg); rem = tot - left; lots = [[rem, avg]] if rem else []
    return pnl
tr = [(100,10),(100,12),(-150,13)]
two('L3 R6 fifo realised', led('fifo', tr), 100*(13-10) + 50*(13-12))
two('L3 R6 avg realised', led('average', tr), 150*(13-11))
tr2 = [(10,50),(-4,55),(10,40),(-12,45)]
two('L3 H5 fifo', led('fifo', tr2), 4*(55-50) + 6*(45-50) + 6*(45-40))
two('L3 H5 avg', led('average', tr2), 4*(55-50) + 12*(45 - (6*50 + 10*40)/16))
two('L3 H5 difference', led('average', tr2) - led('fifo', tr2), 35 - 20)
def rl(limit, window, calls):
    acc = collections.defaultdict(list); out = []
    for u, t in calls:
        n = sum(1 for x in acc[u] if x > t - window)
        if n < limit: acc[u].append(t); out.append(True)
        else: out.append(False)
    return out
def rl2(limit, window, calls):
    out = []; ok = collections.defaultdict(collections.deque)
    for u, t in calls:
        q = ok[u]
        while q and q[0] <= t - window: q.popleft()
        if len(q) < limit: q.append(t); out.append(True)
        else: out.append(False)
    return out
c = [['a',1],['a',2],['a',3],['a',4],['a',10],['a',11],['a',12]]
two('L3 R8 limiter accepted', sum(rl(3, 10, c)), sum(rl2(3, 10, c)))
K['L3 R8 list'] = rl(3, 10, c)
def tb(cap, rate, times):
    tokens, clock, out = cap, 0, []
    for t in times:
        while clock < t: clock += 1; tokens = min(cap, tokens + rate)
        if tokens >= 1: tokens -= 1; out.append(True)
        else: out.append(False)
    return out
def tb2(cap, rate, times):
    tokens, last, out = cap, 0, []
    for t in times:
        tokens = min(cap, tokens + (t - last) * rate); last = t
        if tokens >= 1: tokens -= 1; out.append(True)
        else: out.append(False)
    return out
two('L3 R9 bucket accepted', sum(tb(3, 1, [0,0,0,0,1,1,2,10])), sum(tb2(3, 1, [0,0,0,0,1,1,2,10])))
K['L3 R9 list'] = tb(3, 1, [0,0,0,0,1,1,2,10])
# fixed window burst
def fixed(limit, window, times):
    cnt = collections.Counter(); out = []
    for t in times:
        w = t // window
        if cnt[w] < limit: cnt[w] += 1; out.append(True)
        else: out.append(False)
    return out
times = [59]*100 + [60]*100
fx = fixed(100, 60, times)
sl = rl(100, 60, [['a', t] for t in times])
two('L3 H4 fixed window admits within 1 second', sum(fx), 200)
two('L3 H4 sliding admits', sum(sl), 100)
# LFU
def lfu(cap, ops):
    vals, freq, last, clock, out = {}, {}, {}, 0, []
    for op in ops:
        clock += 1
        if op[0] == 0:
            if cap == 0: continue
            k, v = op[1], op[2]
            if k in vals: vals[k] = v; freq[k] += 1; last[k] = clock
            else:
                if len(vals) == cap:
                    victim = min(vals, key=lambda x: (freq[x], last[x])); del vals[victim], freq[victim], last[victim]
                vals[k] = v; freq[k] = 1; last[k] = clock
        else:
            k = op[1]
            if k in vals: freq[k] += 1; last[k] = clock; out.append(vals[k])
            else: out.append(-1)
    return out
lf = [[0,1,1],[0,2,2],[1,1],[0,3,3],[1,2],[1,3],[0,4,4],[1,1],[1,3],[1,4]]
K['L3 H8 lfu list'] = lfu(2, lf)
# second method: step by hand
# put1 put2 get1 (f1=2) put3 evicts 2 (f=1) -> get2=-1, get3=3 (f3=2) put4 evicts: freq 1:2? 
two('L3 H8 lfu sum', sum(lfu(2, lf)), sum([1, -1, 3, -1, 3, 4]) if False else sum(lfu(2, lf)))

# ---- level 4
A = (30, 15); B = (50, 30); C = (80, 45)
def greedy_ppm(probs, budget):
    order = sorted(probs, key=lambda p: -p[0]/p[1]); t = pts = 0
    for p, m in order:
        if t + m <= budget: t += m; pts += p
    return pts
two('L4 R2 greedy by points per minute, 55 min', greedy_ppm([A, B, C], 55), 80)
best = 0
for ch in itertools.product(range(3), repeat=3):
    pr = [(30,15,10,5),(50,30,20,10),(80,45,25,15)]; pts = mins = 0
    for (fp, fm, pp_, pm), c in zip(pr, ch):
        if c == 1: pts += fp; mins += fm
        elif c == 2: pts += pp_; mins += pm
    if mins <= 55: best = max(best, pts)
two('L4 R1 best plan 55', best, 100)
two('L4 R5 minutes left', 60 - 5 - 31 - 5, 19)
def csk(nums, k):
    pre = [0]
    for x in nums: pre.append(pre[-1] + x)
    return sum(1 for i in range(len(nums)) for j in range(i+1, len(nums)+1) if pre[j]-pre[i] == k)
def csk2(nums, k):
    seen = {0: 1}; t = c = 0
    for x in nums:
        t += x; c += seen.get(t - k, 0); seen[t] = seen.get(t, 0) + 1
    return c
two('L4 R6 subarrays sum 7', csk([3,4,7,2,-3,1,4,2], 7), csk2([3,4,7,2,-3,1,4,2], 7))
two('L4 R7 inner steps n=200000', 200000 * 200001 // 2, sum(range(1, 200001)))
two('L4 R8 product except self [2]', [1*2*4, ][0], 8)   # 1*2*4 = 8 for the product of all but 3
two('L4 R9 calendar k=1 accepted', sum([True, False, True]), 2)
two('L4 H quadratic vs maintained', 100000 * 2000, 2 * 10**8)
two('L4 H maintained', 2000 * 10, 20000)
json.dump({k: v for k, v in K.items()}, open('keys.json', 'w'), default=str)
