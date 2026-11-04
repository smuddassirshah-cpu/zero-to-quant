"""Replacement review numbers (cases unseen in the lessons), each computed by two methods."""
import collections, heapq, itertools, ast, re, math, bisect
def two(name, a, b):
    assert a == b, (name, a, b); print(name, a)
# L1 R1/R2
iv = [[1,3],[2,4],[6,8],[10,12],[11,15],[20,21]]
def blocks_a(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
        else: out.append([s, e])
    return out
def blocks_b(iv):
    cov = set()
    for a, b in iv: cov.update(range(2*a, 2*b+1))
    runs = 0; prev = None
    for x in sorted(cov):
        if prev is None or x != prev + 1: runs += 1
        prev = x
    return runs
two('L1R1 blocks', len(blocks_a(iv)), blocks_b(iv))
def pairs_a(iv):
    ev = sorted([(s, 1) for s, e in iv] + [(e, -1) for s, e in iv]); act = p = 0
    for t, d in ev:
        if d == 1: p += act
        act += d
    return p
two('L1R2 pairs', pairs_a(iv), sum(1 for i in range(len(iv)) for j in range(i+1, len(iv)) if iv[i][0] < iv[j][1] and iv[j][0] < iv[i][1]))
W = ['car','card','care','cat','dog']
def nodes_a(ws):
    root = {}; n = 0
    for w in ws:
        node = root
        for c in w:
            if c not in node: node[c] = {}; n += 1
            node = node[c]
    return n
two('L1R3 nodes', nodes_a(W), len({w[:i] for w in W for i in range(1, len(w)+1)}))
Ws = ['car','card','care','cat','dog','car']
two('L1R4 count car', sum(1 for w in set(Ws) if w.startswith('car')), len([w for w in sorted(set(Ws)) if w[:3] == 'car']))
nums = [4,2,12,3,8,5,1,7]
def wm(nums, k):
    dq, out = collections.deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: out.append(nums[dq[0]])
    return out
two('L1R5 window max sum', sum(wm(nums, 3)), sum(max(nums[i:i+3]) for i in range(6)))
print(wm(nums, 3))
def dqs(nums, k, upto):
    dq = collections.deque()
    for i in range(upto + 1):
        while dq and nums[dq[-1]] <= nums[i]: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
    return list(dq)
# hand: after index 5 the window is indices 3..5 values 3,8,5: 8 stays (index 4) and 5 (index 5) is smaller: deque [4,5]
two('L1R6 deque size after index 5', len(dqs(nums, 3, 5)), len([i for i in range(3, 6) if all(nums[j] < nums[i] for j in range(i+1, 6))]))
two('L1R9 108&107', 108 & 107, 104)
# L2
two('L2R1 anagram starts abab/ab', [i for i in range(3) if sorted('abab'[i:i+2]) == ['a','b']], [i for i in range(len('abab')-1) if collections.Counter('abab'[i:i+2]) == collections.Counter('ab')])
def pal(s):
    n = 0
    for c in range(2*len(s)-1):
        lo, hi = c//2, c//2 + c%2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]: n += 1; lo -= 1; hi += 1
    return n
two('L2R2 palindromic substrings abcba', pal('abcba'), sum(1 for i in range(5) for j in range(i+1, 6) if 'abcba'[i:j] == 'abcba'[i:j][::-1]))
def pp(s): return sum(v % 2 for v in collections.Counter(s).values()) <= 1
def pp2(s): return any(''.join(p) == ''.join(p)[::-1] for p in set(itertools.permutations(s)))
ws = ['civic','ivicc','aabbcd','abcde','xxyyz']
two('L2R3 palindromic perms', [w for w in ws if pp(w)], [w for w in ws if pp2(w)])
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
two('L2R4 (8+2)*(9-4)/5-3', calc('(8+2)*(9-4)/5-3'), (10*5)//5 - 3)
def dec(s):
    pat = re.compile(r'(\d+)\[([a-z]*)\]')
    while pat.search(s): s = pat.sub(lambda m: m.group(2)*int(m.group(1)), s)
    return s
two('L2R5 decode length 2[x3[y]]z', len(dec('2[x3[y]]z')), 2*(1+3)+1)
two('L2R6 -9/4', calc('-9/4'), -2); two('floor', -9//4, -3)
def rs_a(prices):
    pnl = trades = 0; long_ = False
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i-1]: long_, entry, bought = True, p, i
        elif 100*p >= 105*entry or 100*p <= 97*entry or i - bought == 3:
            pnl += p - entry; trades += 1; long_ = False
    if long_: pnl += prices[-1] - entry; trades += 1
    return [pnl, trades]
def rs_slip(prices):   # buys on the sell day
    pnl = trades = 0; long_ = False
    for i, p in enumerate(prices):
        if long_ and (100*p >= 105*entry or 100*p <= 97*entry or i - bought == 3):
            pnl += p - entry; trades += 1; long_ = False
        if not long_ and i >= 1 and p < prices[i-1]: long_, entry, bought = True, p, i
    if long_: pnl += prices[-1] - entry; trades += 1
    return [pnl, trades]
pr = [100,95,90,85]
print('trap correct', rs_a(pr), 'slip', rs_slip(pr))
# by hand: buy 95 day1; day 2 price 90: 9000 <= 9215 sell -5; no buy day 2; day 3: 85 < 90 buy 85; end sell 85: 0 -> [-5, 2]
two('trap hand', [(90-95) + (85-85), 2], rs_a(pr))
# bought on day 2 sells on day 5
two('day count', 2 + 3, 5)
m = [[r*3+c+1 for c in range(3)] for r in range(4)]
def spiral(m):
    out = []
    while m:
        out += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return out
def spiral2(m):
    R, C = len(m), len(m[0]); seen = set(); r = c = 0; dr, dc = 0, 1; out = []
    for _ in range(R*C):
        out.append(m[r][c]); seen.add((r, c)); nr, nc = r+dr, c+dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in seen: dr, dc = dc, -dr; nr, nc = r+dr, c+dc
        r, c = nr, nc
    return out
two('L2R8 spiral 4x3', spiral([r[:] for r in m]), spiral2(m)); print(spiral2(m))
m5 = [[r*5+c for c in range(5)] for r in range(5)]
rot = [list(r) for r in zip(*m5[::-1])]
two('L2R9 (2,3)->', [(r, c) for r in range(5) for c in range(5) if rot[r][c] == m5[2][3]], [(3, 2)])
# amend down: three sells of 4 at 100, id1 amended to 2, buy 7
def book(events):
    rest = []; seq = 0; trades = []
    for ev in events:
        if ev[0] == 0:
            _, i, s, p, q = ev
            while q > 0:
                c = [o for o in rest if o['side'] == 1-s and (o['price'] <= p if s == 0 else o['price'] >= p)]
                if not c: break
                b = min(c, key=lambda o: (o['price'] if s == 0 else -o['price'], o['seq']))
                f = min(q, b['qty']); trades.append([i, b['id'], b['price'], f]); q -= f; b['qty'] -= f
                if b['qty'] == 0: rest.remove(b)
            if q > 0: seq += 1; rest.append(dict(id=i, side=s, price=p, qty=q, seq=seq))
        elif ev[0] == 3:
            for o in rest:
                if o['id'] == ev[1]:
                    if ev[2] < o['qty']: o['qty'] = ev[2]
                    elif ev[2] > o['qty']: seq += 1; o['qty'] = ev[2]; o['seq'] = seq
    return trades
ev = [[0,1,1,100,4],[0,2,1,100,4],[0,3,1,100,4],[3,1,2],[0,4,0,100,7]]
tr = book(ev); print(tr)
# hand: queue after amend: id1 2, id2 4, id3 4; buy 7 takes 2 + 4 + 1
two('L2R10 id3 qty', sum(t[3] for t in tr if t[1] == 3), 7 - 2 - 4)
# L3
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
tr = [(200,20),(100,23),(-250,25)]
two('L3R6 fifo', led('fifo', tr), 200*(25-20) + 50*(25-23))
two('L3R6 avg', led('average', tr), 250 * (25 - (200*20+100*23)/300))
def lru(cap, ops):
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
two('L3 lesson lru cap1', lru(1, [[0,2,1],[1,2],[0,3,2],[1,2],[1,3]]), [1,-1,2])
two('L3 99499499', sum(range(99000, 100000)) - 1, (99000 + 99999) * 1000 // 2 - 1)
def rl(limit, window, calls):
    acc = collections.defaultdict(list); out = []
    for u, t in calls:
        n = sum(1 for x in acc[u] if x > t - window)
        if n < limit: acc[u].append(t); out.append(True)
        else: out.append(False)
    return out
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
        tokens = min(cap, tokens + (t - last)*rate); last = t
        if tokens >= 1: tokens -= 1; out.append(True)
        else: out.append(False)
    return out
two('L3 lesson limiter (2,3)', sum(rl(2, 3, [['a',t] for t in range(6)])), 4)
print(rl(2, 3, [['a',t] for t in range(6)]))
two('L3 lesson bucket (2,2)', sum(tb(2, 2, [0,0,0,1,1,1])), sum(tb2(2, 2, [0,0,0,1,1,1])))
print(tb(2,2,[0,0,0,1,1,1]))
# hook log [5,6] limit 2 window 10
def alone(t): return sum(1 for x in [5,6] if x > t - 10) < 2
print('hook', {t: alone(t) for t in (14, 15, 16)})
# lesson fs example
two('L3 fs lesson', 4 + 2 + 6, len('abcd') + len('xy') + len('abcdef'))
