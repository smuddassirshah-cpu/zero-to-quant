#!/usr/bin/env python3
"""Concept checks for graphs-dp levels 1 to 3, round 2 blind audit (docs/reviews/audit-graphs-dp-1-3-r2.md).

Run from the repository root:  python3 docs/reports/graphs-dp-L1-3-r2-concepts.py [-v]

Three parts.
  A. Stated numbers, orders, counts and code-behaviour claims, recomputed.
  B. Every Python code widget of levels 1 to 3: the solution passes every hidden test and the starter fails.
  C. Every `feedback.byKey["test-N"]` line that names a mistake: a submission with that mistake is run against
     the widget's own tests, and its first failing test must be N. Slip values whose feedback names a mistake
     are recomputed from that mistake.
  D. Fix pass: the fixer's own submissions, one per cause named by a test-N line (each the solution with that one mistake
     put in), first failing test N; every test-N line is listed, and lines that name no cause have their facts checked.
  E. Fix pass: every numeric wrong[] value with a feedback line, recomputed from the mistake the line names.
Part C runs in CPython with the page's recursion limit (3,000, js/screens/drill-worker.js) and a 5 second
alarm per test (the page allows 5 seconds in Pyodide, which is slower than CPython).
The same submissions were also run in Pyodide 0.27.7 through the page's own grader; the audit file gives those results.

Exit 0 when every check holds. A check that fails because the content is wrong stays failing: each such
line is a finding in the audit file (the fix pass should turn them green by changing the content, not this script).
"""
import contextlib, io, json, math, os, re, signal, sys, itertools, heapq
from collections import deque
from math import comb, factorial

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'graphs-dp')
VERBOSE = '-v' in sys.argv
FAILS = []
N = [0]


def check(name, cond, detail=''):
    N[0] += 1
    if not cond:
        FAILS.append(f'{name}  {detail}')
    if VERBOSE or not cond:
        print(('ok   ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(detail)))


def load(f):
    return json.load(open(os.path.join(COURSE, f + '.json')))


# ---------------------------------------------------------------- part A: level 1
E1 = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('C', 'E'), ('E', 'F')]


def undirected(edges, nodes=None):
    adj = {v: [] for v in (nodes or sorted({x for e in edges for x in e}))}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return {k: sorted(v) for k, v in adj.items()}


a1 = undirected(E1, 'ABCDEF')
check('l1-adj neighbour lists', a1 == {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'D', 'E'], 'D': ['B', 'C'], 'E': ['C', 'F'], 'F': ['E']})
M1 = [[1 if b in a1[a] else 0 for b in 'ABCDEF'] for a in 'ABCDEF']
check('l1-matrix row C and 12 ones', M1[2] == [1, 0, 0, 1, 1, 0] and sum(map(sum, M1)) == 12 and [sum(r) for r in M1] == [2, 2, 3, 2, 2, 1])
one_way = {v: [] for v in 'ABCDEF'}
for u, v in E1:
    one_way[u].append(v)
check('l1-trap one-way loop leaves D empty', one_way['D'] == [])
rows = [[0] * 3] * 3
rows[0][1] = 1
check('l1-alias shared rows', rows == [[0, 1, 0]] * 3)
check('l1-sizes', 100_000 ** 2 == 10 ** 10 and 100_000 * 20 == 2 * 10 ** 6 and 100_000 * 20 // 2 == 10 ** 6
      and 1000 ** 2 == 10 ** 6 and 1000 + 2 * 3000 == 7000 and abs(1 - 6000 / 10 ** 6 - 0.994) < 1e-12 and 8 * 10 ** 10 == 80 * 10 ** 9)
check('hw1 matrix GB', 20_000 ** 2 * 8 == 3.2e9 and 20_000 * 8 / 1e9 == 0.00016 and 20_000 * 20 * 8 == 3.2e6)

E2 = [('A', 'B'), ('A', 'D'), ('B', 'E'), ('D', 'C'), ('D', 'F'), ('E', 'G'), ('C', 'G'), ('E', 'H')]
a2 = undirected(E2)


def bfs_order(adj, s):
    seen, q, out = {s}, deque([s]), []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return out


def bfs_dist(adj, s):
    d, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def dfs_pre_post(adj, s):
    seen, pre, post = set(), [], []

    def visit(u):
        seen.add(u)
        pre.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                visit(v)
        post.append(u)
    visit(s)
    return pre, post


d2 = bfs_dist(a2, 'A')
check('l2 rumour days', sorted(k for k, v in d2.items() if v == 2) == ['C', 'E', 'F'] and d2['G'] == 3 and d2['H'] == 3)
check('l2 BFS order', bfs_order(a2, 'A') == list('ABDECFGH'))
late, seen, order = deque(['A']), set(), []
while late:
    u = late.popleft()
    seen.add(u)
    order.append(u)
    for v in sorted(a2[u]):
        if v not in seen:
            late.append(v)
check('l2 trap mark-on-pop order', order == list('ABDECFGHG'))
cut = undirected([e for e in E2 if e not in (('D', 'C'), ('E', 'G'))], 'ABCDEFGH')
check('l2 unreachable C, G', sorted(set('ABCDEFGH') - set(bfs_order(cut, 'A'))) == ['C', 'G'])
cedar = undirected([('Cedar', 'Birch'), ('Cedar', 'Elm'), ('Birch', 'Alder'), ('Alder', 'Oak'), ('Elm', 'Fir'), ('Fir', 'Hazel'), ('Cedar', 'Larch'), ('Larch', 'Oak')])
dc = bfs_dist(cedar, 'Cedar')
check('l2 within 2 hops of Cedar', sorted(k for k, v in dc.items() if 0 < v <= 2) == ['Alder', 'Birch', 'Elm', 'Fir', 'Larch', 'Oak'] and dc['Hazel'] == 3)
pre, post = dfs_pre_post(a2, 'A')
check('l3 DFS pre-order and post-order', pre == list('ABEGCDFH') and post == list('FDCGHEBA'))
stack, seen, order = ['A'], set(), []
while stack:
    u = stack.pop()
    if u in seen:
        continue
    seen.add(u)
    order.append(u)
    for v in sorted(a2[u]):
        if v not in seen:
            stack.append(v)
check('l3 naive stack order', order == list('ADFCGEHB'))
# the reverse-push, skip-on-pop stack DFS equals the recursive pre-order on random graphs
import random
rng = random.Random(1)
same = True
for _ in range(300):
    n = rng.randint(1, 9)
    es = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    g = undirected(es, list(range(n)))
    st, sn, od = [0], set(), []
    while st:
        u = st.pop()
        if u in sn:
            continue
        sn.add(u)
        od.append(u)
        for v in sorted(g[u], reverse=True):
            if v not in sn:
                st.append(v)
    same &= od == dfs_pre_post(g, 0)[0]
check('l3 stack DFS with reverse pushes equals recursive pre-order (300 random graphs)', same)
st, sn, twice = ['A'], set(), {}
while st:
    u = st.pop()
    if u in sn:
        continue
    sn.add(u)
    for v in sorted(a2[u], reverse=True):
        if v not in sn:
            st.append(v)
            twice[v] = twice.get(v, 0) + 1
hint_node = load('l3-going-deep')['screens'][5]['hints'][1]['highlight']
check('l3 screens[5].hints[1]: the node the hint names is the one pushed twice by the solution', [k for k, v in twice.items() if v > 1] == hint_node,
      f'pushed twice: {[k for k, v in twice.items() if v > 1]}, hint highlights {hint_node}')
tree = {'A': ['B'], 'B': ['A']}


def no_seen(adj, u, depth=0):
    if depth > 50:
        raise RecursionError
    for v in adj[u]:
        no_seen(adj, v, depth + 1)


try:
    no_seen(tree, 'A')
    hides = True
except RecursionError:
    hides = False
# fix pass: the sentence now says "a tree stored as parent-to-child arrows"; undirected it never returns, stored parent to child it does
try:
    no_seen({'A': ['B'], 'B': []}, 'A')
    hides_directed = True
except RecursionError:
    hides_directed = False
check('l3 screens[3].explain (fix pass): no seen set fails on an undirected tree but returns on parent-to-child arrows',
      not hides and hides_directed and 'tree stored as parent-to-child arrows' in load('l3-going-deep')['screens'][3]['explain']['text'])
rev = undirected([('P', 'Q'), ('P', 'S'), ('Q', 'R'), ('S', 'T'), ('R', 'U'), ('T', 'U')])
check('review-1 BFS and DFS orders', bfs_order(rev, 'P') == list('PQSRTU') and dfs_pre_post(rev, 'P')[0] == list('PQRUTS'))


def islands(grid, diag=False):
    R, C = len(grid), len(grid[0]) if grid else 0
    seen, n = set(), 0
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)] + ([(-1, -1), (-1, 1), (1, -1), (1, 1)] if diag else [])
    for r in range(R):
        for c in range(C):
            if grid[r][c] and (r, c) not in seen:
                n += 1
                seen.add((r, c))
                st = [(r, c)]
                while st:
                    a, b = st.pop()
                    for dr, dc_ in steps:
                        x, y = a + dr, b + dc_
                        if 0 <= x < R and 0 <= y < C and grid[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            st.append((x, y))
    return n


G4 = [[1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1]]
check('l4 islands 6, diagonal slip 4, 14 land cells', islands(G4) == 6 and islands(G4, True) == 4 and sum(map(sum, G4)) == 14)
GR = [[1, 1, 0, 0, 1], [0, 1, 0, 1, 1], [1, 0, 0, 0, 0], [1, 1, 0, 1, 0]]
check('review-1 islands 4, diagonal slip 3', islands(GR) == 4 and islands(GR, True) == 3 and sum(map(sum, GR)) == 10)
X = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
check('l4 quiz X grid 5 and 1', islands(X) == 5 and islands(X, True) == 1)
ring = [[1] * 5, [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1] * 5]
check('hw1 ring 2 islands, 16 border cells', islands(ring) == 2 and sum(map(sum, ring)) == 17)
# recursive flood fill in the order up, down, left, right dives through every cell of an all-land grid
sys.setrecursionlimit(10000)


def dive(R, C):
    seen, best = set(), [0]

    def fill(a, b, depth):
        seen.add((a, b))
        best[0] = max(best[0], depth)
        for x, y in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
            if 0 <= x < R and 0 <= y < C and (x, y) not in seen:
                fill(x, y, depth + 1)
    fill(0, 0, 1)
    return best[0]


check('l4 recursion depth on all land equals the cell count (4x4: 16, 30x30: 900)', dive(4, 4) == 16 and dive(30, 30) == 900)
PNL = [[5, -15, -35, -55, -75], [50, 30, 10, -10, -30], [65, 45, 25, 5, -15], [50, 30, 10, -10, -30], [5, -15, -35, -55, -75]]
reg = lambda lim, strict=True: islands([[(v < -lim) if strict else (v <= -lim) for v in row] for row in PNL])
check('l4 loss regions 2, 1, 0, 2', [reg(50), reg(10), reg(100), reg(30)] == [2, 1, 0, 2])
t6 = lambda strict: islands([[(v < -50) if strict else (v <= -50) for v in [-50, -51]]])
# fix pass: test 6 cannot tell < from <= (strict 1, non-strict 1), so its line no longer says it checks the boundary;
# it names the first non-square grid, which a square-grid submission fails (part D). The tests are unchanged.
check('l4 screens[8] test 6 (fix pass): < and <= agree on it, and its line no longer claims the boundary', t6(True) == t6(False) == 1
      and 'boundary' not in load('l4-islands')['screens'][8]['feedback']['byKey']['test-6'])
p6 = lambda strict: islands([[(v < -50) if strict else (v <= -50) for v in [-50, 10, -51]]])
check('l4 proposed replacement test [[-50, 10, -51]] separates < (1 region) from <= (2 regions)', (p6(True), p6(False)) == (1, 2))
PIPE = {'prices': ['returns'], 'calendar': ['returns'], 'returns': ['signals', 'risk'], 'signals': ['backtest'], 'risk': ['backtest'], 'backtest': ['report'], 'report': []}


def kahn(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    ready = [u for u in adj if indeg[u] == 0]
    heapq.heapify(ready)
    out = []
    while ready:
        u = heapq.heappop(ready)
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(ready, v)
    return out


def valid_orders(adj):
    return [p for p in itertools.permutations(adj) if all(p.index(u) < p.index(v) for u in adj for v in adj[u])]


check('l5 four valid orders; Kahn order', len(valid_orders(PIPE)) == 4 and kahn(PIPE) == ['calendar', 'prices', 'returns', 'risk', 'signals', 'backtest', 'report'])
seen, pre5, post5 = set(), [], []


def v5(u):
    seen.add(u)
    pre5.append(u)
    for v in sorted(PIPE[u]):
        if v not in seen:
            v5(v)
    post5.append(u)


for u in sorted(PIPE):
    if u not in seen:
        v5(u)
check('l5 pre-order trap and post-order', pre5 == ['backtest', 'report', 'calendar', 'returns', 'risk', 'signals', 'prices']
      and post5 == ['report', 'backtest', 'risk', 'signals', 'returns', 'calendar', 'prices'] and tuple(post5[::-1]) in valid_orders(PIPE))
loop5 = {k: list(v) for k, v in PIPE.items()}
loop5['backtest'].append('risk')
check('l5 Kahn stalls after 4', kahn(loop5) == ['calendar', 'prices', 'returns', 'signals'])
check('l5 quiz: 24 orders; a, c, b only', factorial(4) == 24 and valid_orders({'a': ['b', 'c'], 'c': ['b'], 'b': []}) == [('a', 'c', 'b')])
check('review-1 Kahn emits 3', kahn({'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': ['e'], 'e': ['f'], 'f': ['d', 'g'], 'g': []}) == ['a', 'b', 'c'])

# ---------------------------------------------------------------- part A: level 2
a6 = undirected([('A', 'B'), ('A', 'E'), ('B', 'C'), ('C', 'D'), ('D', 'H'), ('E', 'F'), ('F', 'H'), ('E', 'G'), ('G', 'D')])
d6 = bfs_dist(a6, 'A')
check('l6 rings and queue order', d6 == {'A': 0, 'B': 1, 'E': 1, 'C': 2, 'F': 2, 'G': 2, 'D': 3, 'H': 3} and bfs_order(a6, 'A') == list('ABECFGDH'))


def find_path(adj, s, t, seen=None):
    if seen is None:
        seen = set()
    seen.add(s)
    if s == t:
        return [s]
    for v in sorted(adj[s]):
        if v not in seen:
            p = find_path(adj, v, t, seen)
            if p:
                return [s] + p
    return None


check('l6 trap DFS route', find_path(a6, 'A', 'H') == list('ABCDGEFH'))
sett = undirected([('you', 'bank1'), ('you', 'bank2'), ('bank1', 'cust'), ('cust', 'fund'), ('bank2', 'ccp'), ('ccp', 'fund'), ('bank2', 'broker'), ('broker', 'fund'), ('bank1', 'ccp')])
check('l6 settlement: 3 hops', bfs_dist(sett, 'you')['fund'] == 3)
maze = ['...#', '##.#', '....', '.##.']
mz = {(r, c): [(r + dr, c + dc_) for dr, dc_ in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= r + dr < 4 and 0 <= c + dc_ < 4 and maze[r + dr][c + dc_] == '.'] for r in range(4) for c in range(4) if maze[r][c] == '.'}
check('l6 quiz maze 6 moves', bfs_dist(mz, (0, 0))[(3, 3)] == 6)
W7 = {'A': [('B', 4), ('C', 1)], 'B': [('D', 1)], 'C': [('B', 2), ('D', 5), ('E', 2)], 'D': [('F', 3)], 'E': [('F', 6)], 'F': [], 'G': [('F', 1)]}


def dijkstra(adj, s, log=None):
    dist = {u: math.inf for u in adj}
    dist[s] = 0
    heap = [(0, s)]
    pushes, stale = 1, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1
            continue
        if log is not None:
            log.append((d, u))
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
                pushes += 1
    return dist, pushes, stale


log7 = []
dist7 = dijkstra(W7, 'A', log7)[0]
check('l7 costs and pop order', dist7 == {'A': 0, 'B': 3, 'C': 1, 'D': 4, 'E': 3, 'F': 7, 'G': math.inf} and log7 == [(0, 'A'), (1, 'C'), (3, 'B'), (3, 'E'), (4, 'D'), (7, 'F')])


def all_routes(adj, s, t, cost=0, path=None):
    path = path or [s]
    if s == t:
        yield cost, path
    for v, w in adj[s]:
        if v not in path:
            yield from all_routes(adj, v, t, cost + w, path + [v])


check('l7 route costs 7, 8, 9, 9', sorted(c for c, _ in all_routes(W7, 'A', 'F')) == [7, 8, 9, 9])
dpop, heap = {}, [(0, 'A')]
while heap:
    d, u = heapq.heappop(heap)
    dpop[u] = d
    for v, w in W7[u]:
        heapq.heappush(heap, (d + w, v))
check('l7 trap record-on-pop: B 4, F 9', dpop['B'] == 4 and dpop['F'] == 9)
check('l7 screens[5].explain (fix pass) "B ends at 4, D at 6 and F at 9, all wrong": exactly these three end wrong',
      sorted((k, dpop[k]) for k in dpop if dpop[k] != dist7[k]) == [('B', 4), ('D', 6), ('F', 9)] and 'D at 6' in load('l7-dijkstra')['screens'][5]['explain']['text'], f'wrong nodes: {sorted((k, dpop[k], dist7[k]) for k in dpop if dpop[k] != dist7[k])}')
seen7, d7s, heap = {'A'}, {'A': 0}, [(0, 'A')]
while heap:
    d, u = heapq.heappop(heap)
    for v, w in W7[u]:
        if v not in seen7:
            seen7.add(v)
            d7s[v] = d + w
            heapq.heappush(heap, (d + w, v))
check('l7 quiz seen-on-push gives B 4', d7s['B'] == 4)
NEG = {'A': [('B', 2), ('C', 3)], 'B': [], 'C': [('B', -2)]}
check('l7 negative arrow: true cost 1; re-pushing heap code also gets 1', dijkstra(NEG, 'A')[0]['B'] == 1)
FX = {'GBP': [('USD', 1.2), ('EUR', 0.5), ('JPY', 4.0)], 'EUR': [('USD', 0.6), ('JPY', 2.4), ('CHF', 0.7)], 'USD': [('JPY', 1.5)], 'CHF': [('JPY', 1.9)], 'JPY': []}
dfx = dijkstra(FX, 'GBP')[0]
check('l7 FX costs', all(abs(dfx[k] - v) < 1e-9 for k, v in {'EUR': 0.5, 'USD': 1.1, 'CHF': 1.2, 'JPY': 2.6}.items()))
check('l7 exact compounding 259.98', round(1e6 * (1 - (1 - 0.5e-4) * (1 - 0.6e-4) * (1 - 1.5e-4)), 2) == 259.98)
LINKS = [('LD4', 'FR2', 4.2), ('FR2', 'LD4', 4.2), ('LD4', 'NY4', 29.5), ('NY4', 'LD4', 29.5), ('NY4', 'CH1', 3.9), ('CH1', 'NY4', 3.9), ('FR2', 'SG1', 77.0), ('LD4', 'SG1', 84.0), ('SG1', 'TY3', 34.0), ('CH1', 'TY3', 70.0)]
LA = {c: [] for c in ['LD4', 'FR2', 'NY4', 'CH1', 'SG1', 'TY3']}
for a, b, ms in LINKS:
    LA[a].append((b, ms))
dl = dijkstra(LA, 'LD4')[0]
check('l7 latency map', [round(dl[k], 6) for k in ('FR2', 'NY4', 'CH1', 'SG1', 'TY3')] == [4.2, 29.5, 33.4, 81.2, 103.4] and round(4.2 + 77 + 34, 6) == 115.2 and 84 + 34 == 118)
check('l7 quiz sparse', abs((100_000 + 400_000) * math.log2(100_000) - 8.3e6) < 1e5 and 100_000 ** 2 == 10 ** 10)
# most heap entries: E + 1 is reached (a 6-node, 9-edge graph where every edge improves a cost)
best_pushes = 0
order6 = list(range(6))
fw = [(i, j) for i in range(6) for j in range(i + 1, 6)]
for es in itertools.combinations(fw, 9):
    adj = {i: [] for i in range(6)}
    for i, j in es:
        adj[i].append((j, 10 * (j - i) + (5 - i)))   # later tails offer strictly cheaper routes
    best_pushes = max(best_pushes, dijkstra(adj, 0)[1])
    if best_pushes == 10:
        break
check('l7 quiz: 6 nodes, 9 edges can reach E + 1 = 10 heap entries', best_pushes == 10)
k = 300
hub = {'s': [('c1', 1)], 'h': []}
for i in range(1, k + 1):
    hub['c%d' % i] = ([('c%d' % (i + 1), 1)] if i < k else []) + [('h', 2 * k - 2 * i)]
dh, _, stale_h = dijkstra(hub, 's')
check('l7 test 9: hub at 300 with 299 stale entries', dh['h'] == 300 and stale_h == 299)
RS = {'S': [('A', 2), ('B', 6)], 'A': [('B', 3), ('C', 7)], 'B': [('C', 1), ('T', 8)], 'C': [('T', 2)], 'T': []}
dr, _, stale_r = dijkstra(RS, 'S')
check('review-2 Dijkstra 8 and 3 stale pops', dr == {'S': 0, 'A': 2, 'B': 5, 'C': 6, 'T': 8} and stale_r == 3)


class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.n = n

    def find(self, x):
        while self.p[x] != x:
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.p[a] = b
        self.n -= 1
        return True


par = [0, 0, 2, 2, 2, 4, 4, 6]
x, steps = 7, 0
while par[x] != x:
    x, steps = par[x], steps + 1
check('l8 find(7) is 2 in three steps', (x, steps) == (2, 3))
d = DSU(8)
merged = [d.union(a, b) for a, b in [(0, 1), (2, 3), (1, 3), (5, 6)]]
check('l8 screens[7]: 4 components, four merges', d.n == 4 and all(merged))
with_edges = len({d.find(v) for v in (0, 1, 2, 3, 5, 6)})
slip = next(w['value'] for w in load('l8-groups')['screens'][7]['widget']['wrong'] if w['id'] == 'edges')
check('l8 screens[7] slip "edges": "You counted only the groups with edges" must give the slip value', with_edges == slip, f'groups with edges = {with_edges}, slip value = {slip}')
d = DSU(7)
for a, b in [(1, 2), (3, 4), (2, 5)]:
    d.union(a, b)
check('l8 quiz netting 3 groups, 2 with trades', d.n - 1 == 3)
KR = sorted([(4, 'A', 'B'), (1, 'A', 'C'), (2, 'B', 'C'), (5, 'B', 'D'), (8, 'C', 'D'), (3, 'D', 'E'), (9, 'C', 'E')])
d, tot, kept = DSU(5), 0, []
for w, a, b in KR:
    if d.union('ABCDE'.index(a), 'ABCDE'.index(b)):
        tot += w
        kept.append(w)
check('review-2 Kruskal 11', tot == 11 and kept == [1, 2, 3, 5] and 1 + 2 + 3 + 4 == 10 and 1 + 2 + 3 + 4 + 5 == 15)
CORR = [('SHEL', 'BP', 0.82), ('HSBA', 'BARC', 0.76), ('BARC', 'LLOY', 0.81), ('AZN', 'GSK', 0.64), ('HSBA', 'LLOY', 0.69), ('VOD', 'BP', 0.12), ('GSK', 'SHEL', -0.05), ('BP', 'BARC', 0.41), ('BARC', 'GILT', -0.74)]
NAMES = ['AZN', 'BARC', 'BP', 'GILT', 'GSK', 'HSBA', 'LLOY', 'SHEL', 'VOD']
d = DSU(9)
for a, b, r in CORR:
    if abs(r) > 0.7:
        d.union(NAMES.index(a), NAMES.index(b))
check('l8 five clusters at 0.7', d.n == 5)
check('l9 loop products', abs(1.27 * 0.92 * 0.86 - 1.004824) < 1e-12 and abs(1.142 * 0.92 * 0.95 - 0.998108) < 1e-12 and 1.27 * 0.92 * 0.95 * 0.8985 < 1)
check('l9 break-even rate', round(1 / (1.27 * 0.92), 6) == 0.855871 and abs(1.27 * 0.92 - 1.1684) < 1e-12)
ws = [-math.log(r) for r in (1.27, 0.92, 0.86)]
check('l9 log weights', [round(w, 6) for w in ws] == [-0.239017, 0.083382, 0.150823] and round(sum(ws), 6) == -0.004812 and round(1.27 + 0.92 + 0.86, 2) == 3.05 and round(1.142 + 0.92 + 0.95, 3) == 3.012)


def bellman(edges, n, s, passes=None):
    dist = [math.inf] * n
    dist[s] = 0
    hist = []
    for _ in range(n - 1 if passes is None else passes):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
        hist.append(list(dist))
    return dist, hist


check('l9 pass table', bellman([(2, 3, 1), (1, 2, 3), (0, 1, 2)], 4, 0)[1] == [[0, 2, math.inf, math.inf], [0, 2, 5, math.inf], [0, 2, 5, 6]])
h6 = bellman([(i, i + 1, 1) for i in range(4, -1, -1)], 6, 0)[1]
check('review-2 chain: node 5 first correct after pass 5', [h[5] for h in h6] == [math.inf] * 4 + [5])
w125 = -math.log(1.25) - math.log(0.8)
check('l9 floating point break-even sum is about -5.55e-17', w125 < 0 and abs(w125 + 5.55e-17) < 1e-18, w125)
gross = 1.0850 / (0.8543 * 1.2700)
check('l9 after costs', round(1.0850 / 1.2700, 6) == 0.854331 and round(gross, 7) == 1.0000359 and abs(1e6 * (gross * 0.9999 ** 3 - 1) + 264.03) < 0.05 and abs(1e6 * (gross - 1) - 35.95) < 0.05)
check('l9 quiz', 8 * 40 == 320 and 7 * 40 == 280 and 9 * 40 == 360 and round(1.27 * 0.787, 5) == 0.99949 and round(-math.log(1.27 * 0.787), 6) == 0.00051 and abs(1.05 / 1.25 - 0.84) < 1e-12 and round(1.25 / 1.05, 4) == 1.1905)
check('l9 test products', 1.27 * 0.92 * 0.855 < 1 and abs(9.1 * 0.1102 - 1.00282) < 1e-9 and 1.27 * 150 * 0.00585 * 0.9 > 1)
check('review-2 loop', round(191.20 * 0.006135 * 0.8530, 6) == 1.000579 and round(191.20 * 0.006135, 6) == 1.173012 and round(191.20 + 0.006135 + 0.8530, 6) == 192.059135)
g2 = 1.2650 * 0.9230 * 0.8580
check('hw2 triangle', abs(g2 - 1.00179651) < 1e-9 and abs(1e6 * (g2 * 0.9998 ** 3 - 1) - 1195.55) < 0.05 and abs(1e6 * (g2 - 1) - 1796.51) < 0.01 and abs(1e6 * (g2 * 0.9998 - 1) - 1596.15) < 0.05)
check('hw2 scanner arithmetic', 31 * 830 == 25730)

# ---------------------------------------------------------------- part A: level 3
check('l10 counts', 2 ** 3 == 8 and 2 ** 10 == 1024 and factorial(10) == 3628800 and factorial(5) == 120 and sum(comb(6, k) for k in range(4)) == 42 and 6 * 5 * 4 == 120)
check('l10 thirty stocks', abs(2 ** 30 / 1000 / 86400 - 12.43) < 0.01 and round(2 ** 30 / 1000 / 3600) == 298 and round(2 ** 30 / 1000) == 1073742 and abs(2 ** 40 / 1000 / 86400 / 365.25 - 34.8) < 0.1)
out, path = [], []


def walk10(i, xs):
    if i == len(xs):
        out.append(path[:])
        return
    path.append(xs[i])
    walk10(i + 1, xs)
    path.pop()
    walk10(i + 1, xs)


walk10(0, 'ABC')
check('l10 walk order: B C is fifth', [''.join(p) for p in out] == ['ABC', 'AB', 'AC', 'A', 'BC', 'B', 'C', ''])
out, path = [], []
walk10(0, ['VOD', 'BP', 'VOD'])
check('l10 duplicate ticker: 8 lists, 4 holdings as sets, 6 as multisets', len(out) == 8 and len({frozenset(p) for p in out}) == 4 and len({tuple(sorted(p)) for p in out}) == 6)
out, path = [], []


def nopop(i, xs):
    if i == len(xs):
        out.append(path[:])
        return
    path.append(xs[i])
    nopop(i + 1, xs)
    nopop(i + 1, xs)


nopop(0, ['a', 'b'])
check('l10 quiz no pop', out == [['a', 'b'], ['a', 'b'], ['a', 'b', 'b'], ['a', 'b', 'b']])


def queens_nodes(n, prune=True):
    by_depth = [0] * (n + 1)

    def place(row, cols):
        by_depth[row] += 1
        if row == n:
            return
        for c in range(n):
            if prune and any(c == c2 or abs(c - c2) == row - r2 for r2, c2 in enumerate(cols)):
                continue
            place(row + 1, cols + [c])
    place(0, [])
    return by_depth


check('l11 four queens node counts', queens_nodes(4) == [1, 4, 6, 4, 2] and sum(queens_nodes(4)) == 17 and sum(4 ** k for k in range(5)) == 341)
check('l11 eight queens: 2,057 nodes, 92 answers, 19,173,961 unpruned', sum(queens_nodes(8)) == 2057 and queens_nodes(8)[8] == 92 and sum(8 ** k for k in range(9)) == 19173961 and 8 ** 8 == 16777216)
check('l11 queen counts 1, 0, 0, 2, 10, 4', [queens_nodes(n)[n] for n in range(1, 7)] == [1, 0, 0, 2, 10, 4])
cols_only3 = sum(1 for p in itertools.permutations(range(3)))
slip3 = next(w['value'] for w in load('l11-dead-ends')['quiz'][0]['widget']['wrong'] if w['id'] == 'two')
# fix pass: the "two" line now says two is the 4 by 4 count; part E recomputes it
check('l11 quiz q-three slip "two" (fix pass): the line no longer names a mistake that gives another value', 'columns' not in load('l11-dead-ends')['quiz'][0]['feedback']['byKey']['two'] and slip3 == 2)


def combos(cands, target):
    cands = sorted(cands)
    res, pth = [], []

    def walk(start, left):
        if left == 0:
            res.append(pth[:])
            return
        for i in range(start, len(cands)):
            if cands[i] > left:
                break
            pth.append(cands[i])
            walk(i, left - cands[i])
            pth.pop()
    walk(0, target)
    return res


def compositions(cands, target):
    return 1 if target == 0 else sum(compositions(cands, target - c) for c in cands if c <= target)


check('l11 combos', combos([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]] and compositions([2, 3, 5], 8) == 6 and combos([2, 3, 6, 7], 7) == [[2, 2, 3], [7]] and compositions([2, 3, 6, 7], 7) == 4)
check('hw3 combination counts', len(combos([2, 3, 5, 7], 30)) == 45 and len(combos([1, 2, 3, 4, 5], 20)) == 192)


def unsafe(xs, target):
    def walk(i, total):
        if total == target:
            return True
        if total > target:
            return False
        if i == len(xs):
            return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)
    return walk(0, 0)


check('l11 trap and review-3: unsafe prune returns False although a basket exists', unsafe([6, -4, 3], 2) is False and 6 - 4 == 2 and unsafe([4, -2, 1], 3) is False and 4 - 2 + 1 == 3)
check('l11 test 13 size', 2 ** 26 - 1 == 67108863 and len(range(2, 52, 2)) == 25)


def fib_calls(n):
    return 1 if n < 2 else 1 + fib_calls(n - 1) + fib_calls(n - 2)


fibs = [0, 1]
for _ in range(100):
    fibs.append(fibs[-1] + fibs[-2])
check('l12 call counts', [fib_calls(n) for n in range(9)] == [1, 1, 3, 5, 9, 15, 25, 41, 67] and 2 * fibs[31] - 1 == 2692537 and fibs[30] == 832040 and fibs[90] == 2880067194370816120)
cnt = {}


def fib_count(n):
    cnt[n] = cnt.get(n, 0) + 1
    return n if n < 2 else fib_count(n - 1) + fib_count(n - 2)


fib_count(6)
check('l12 naive column', [cnt[k] for k in range(7)] == [5, 8, 5, 3, 2, 1, 1])
calls, cache = [0], {}


def fmemo(k):
    calls[0] += 1
    if k in cache:
        return cache[k]
    cache[k] = k if k < 2 else fmemo(k - 1) + fmemo(k - 2)
    return cache[k]


fmemo(30)
check('l12 memoised fib(30): 31 values, 59 calls', len(cache) == 31 and calls[0] == 59)
calls, cache = [0], {}
fmemo(5)
check('l12 memoised fib(5): 9 calls', calls[0] == 9)
check('l12 grid and lattice', comb(5, 2) == 10 and comb(34, 17) == 2333606220 and comb(58, 29) == 30067266499541040 and 2 * comb(34, 17) - 1 > 4 * 10 ** 9 and 31 * 32 // 2 == 496 and 31 * 31 == 961)
check('l12 prices', round(100 / 1.05, 2) == 95.24 and round(100 / 1.10, 2) == 90.91 and round(1.05 ** -2, 4) == 0.907 and round(1.06 ** -2, 4) == 0.89)


def climb(n, steps=(1, 2), w0=1):
    w = [w0, 1] + [0] * n
    for i in range(2, n + 1):
        w[i] = sum(w[i - s] for s in steps if i - s >= 0)
    return w[:n + 1]


check('l13 stairs tables', climb(6) == [1, 1, 2, 3, 5, 8, 13] and climb(4, w0=0) == [0, 1, 1, 2, 3] and climb(6, (1, 2, 3)) == [1, 1, 2, 4, 7, 13, 24] and climb(90)[90] == 4660046610375530309)


def coins_table(coins, amount):
    best = [0] + [math.inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return best


def greedy(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c
        amount %= c
    return n if amount == 0 else -1


check('l13 coin tables and greedy', coins_table([1, 3, 4], 6) == [0, 1, 2, 1, 1, 2, 2] and greedy([1, 3, 4], 6) == 3 and coins_table([1, 5, 6, 9], 11)[11] == 2 and greedy([1, 5, 6, 9], 11) == 3
      and coins_table([2, 5], 11)[11] == 4 and greedy([2, 5], 11) == -1 and coins_table([1, 5, 10, 25], 63)[63] == 6 and coins_table([186, 419, 83, 408], 6249)[6249] == 20
      and [coins_table([1, 5, 6, 9], 11)[k] for k in (10, 6, 5, 2)] == [2, 1, 1, 2])
bw = [0] + [math.inf] * 6
for a in range(6, 0, -1):
    for c in (1, 3, 4):
        if c <= a:
            bw[a] = min(bw[a], bw[a - c] + 1)
check('l13 wrong direction table', bw == [0, 1, math.inf, 1, 1, math.inf, math.inf])
check('l13 lattice and hw3', comb(6, 3) == 20 and comb(10, 5) == 252 and 21 * 101 == 2121 and 2 ** 20 == 1048576 and 26 * 7 * 121 == 22022
      and sum(comb(25, k) for k in range(7)) == 245506 and [comb(25, k) for k in range(7)] == [1, 25, 300, 2300, 12650, 53130, 177100] and 2 ** 25 == 33554432 and 2 ** 25 / 1000 / 3600 > 9)
perms4 = list(itertools.permutations('ABCD'))
a_before_d = sum(1 for p in perms4 if p.index('A') < p.index('D'))
a_first_d_last = sum(1 for p in perms4 if p[0] == 'A' and p[-1] == 'D')
slipL = next(w['value'] for w in load('homework-3')['items'][3]['widget']['wrong'] if w['id'] == 'fixed')
check('hw3 h-legs: 12 orders', a_before_d == 12)
check('hw3 h-legs slip "fixed" (fix pass): "You sent A first every time" gives the slip value', sum(1 for p in perms4 if p[0] == 'A') == slipL
      and 'A first every time' in load('homework-3')['items'][3]['feedback']['byKey']['fixed'], f'A first and D last gives {a_first_d_last}; A first alone gives {sum(1 for p in perms4 if p[0] == "A")}; slip value = {slipL}')
tw = [1] + [0] * 40
for i in range(1, 41):
    tw[i] = sum(tw[i - s] for s in (1, 2, 3, 4) if i - s >= 0)
check('hw3 word break: billions of splits of 40 letters', tw[40] > 10 ** 9, tw[40])


def fee_best(prices, fee):
    flat, long = 0, -math.inf
    for p in prices:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat


check('hw3 fee trades feedback numbers', fee_best([12, 10, 15, 9, 14, 12], 1) == 8 and fee_best([20, 10, 12, 11, 16, 13, 18, 15], 2) == 7 and (16 - 10 - 2) + (18 - 13 - 2) == 7
      and (12 - 10 - 2) + (16 - 11 - 2) + (18 - 13 - 2) == 6 and fee_best([8, 13, 11], 2) == 3 and fee_best([9, 6, 12], 2) == 4 and fee_best([15, 14, 16, 13], 3) == 0)

# ---------------------------------------------------------------- parts B and C: the code widgets
LEVELS = ['l1-nodes-and-edges', 'l2-level-by-level', 'l3-going-deep', 'l4-islands', 'l5-tasks-in-order', 'review-1', 'homework-1',
          'l6-fewest-steps', 'l7-dijkstra', 'l8-groups', 'l9-arbitrage-cycle', 'review-2', 'homework-2',
          'l10-every-subset', 'l11-dead-ends', 'l12-remembering', 'l13-climbing-stairs', 'review-3', 'homework-3']
RECURSION_LIMIT = 3000   # js/screens/drill-worker.js
TEST_SECONDS = 5


class _Timeout(Exception):
    pass


def _alarm(*_):
    raise _Timeout()


def widget(ref):
    f, p = ref.split('#')
    key, i = p[:-1].split('[')
    return load(f)[key][int(i)]['widget']


def run_tests(w, code, stop=False):
    """first failing test number (1-based) or None; also the list of all failing tests"""
    ns = {'__name__': '__zq__'}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(w.get('prelude', '') + '\n' + code + '\n' + w.get('postlude', ''), ns)
    except Exception as e:
        return 0, ['load:' + type(e).__name__]
    fails = []
    for k, t in enumerate(w['tests'], 1):
        sys.setrecursionlimit(RECURSION_LIMIT)
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(TEST_SECONDS)
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'], ns)
            ok = got == want or (isinstance(want, tuple) and isinstance(got, list) and tuple(got) == want)
        except _Timeout:
            ok = False
            fails.append(f'{k}:timeout')
            signal.alarm(0)
            break            # the page restarts Python here; later tests do not change the first failure
        except BaseException as e:
            ok = False
        finally:
            signal.alarm(0)
        if not ok and (not fails or not fails[-1].startswith(f'{k}:')):
            fails.append(str(k))
        if fails and stop:
            break
    sys.setrecursionlimit(10000)
    first = int(fails[0].split(':')[0]) if fails else None
    return first, fails


def code_widgets():
    for f in LEVELS:
        d = load(f)
        for key in ('screens', 'quiz', 'items'):
            for i, s in enumerate(d.get(key, [])):
                w = s.get('widget') or {}
                if w.get('kind') == 'code':
                    yield f'{f}#{key}[{i}]', w


for ref, w in code_widgets():
    stated = re.search(r'runs (\d+) hidden tests', w.get('how', ''))
    check(f'B `how` states the number of hidden tests: {ref}', stated is not None and int(stated.group(1)) == len(w['tests']))
    first, fails = run_tests(w, w['solution'])
    check(f'B solution passes: {ref}', first is None, fails)
    first, fails = run_tests(w, w['starter'])
    check(f'B starter fails: {ref}', first is not None)

M = {}


def m(ref, n, tag, code):
    M[f'{ref} test-{n}: {tag}'] = (ref, n, code)


# A submission tagged "(should pass)" is a control: it must pass every test.
# A submission tagged "(not the named mistake)" documents a variant; it is reported but not asserted.

m('l1-nodes-and-edges#screens[5]', 1, 'one-way', '''
def adj_list(nodes, edges):
    adj = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v)
    for v in adj: adj[v].sort()
    return adj
''')
m('l1-nodes-and-edges#screens[5]', 2, 'keys-from-edges', '''
def adj_list(nodes, edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        if u != v: adj.setdefault(v, []).append(u)
    for v in adj: adj[v].sort()
    return adj
''')
m('l1-nodes-and-edges#screens[5]', 3, 'selfloop-twice', '''
def adj_list(nodes, edges):
    adj = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for v in adj: adj[v].sort()
    return adj
''')
m('l1-nodes-and-edges#screens[8]', 1, 'shared-rows', '''
def adj_matrix(n, edges):
    m = [[0] * n] * n
    for u, v in edges:
        m[u][v] = 1; m[v][u] = 1
    return m
''')
m('l1-nodes-and-edges#screens[9]', 3, 'in-only', '''
def find_ccp(n, posts):
    into = [0] * n
    for a, b in posts: into[b] += 1
    for f in range(n):
        if into[f] == n - 1: return f
    return -1
''')
m('l1-nodes-and-edges#screens[9]', 4, 'out-only', '''
def find_ccp(n, posts):
    out = [0] * n
    for a, b in posts: out[a] += 1
    for f in range(n):
        if out[f] == 0: return f
    return -1
''')
m('l1-nodes-and-edges#screens[9]', 5, 'needs-a-poster', '''
def find_ccp(n, posts):
    into = [0] * n; out = [0] * n
    for a, b in posts: out[a] += 1; into[b] += 1
    for f in range(n):
        if into[f] > 0 and into[f] == n - 1 and out[f] == 0: return f
    return -1
''')
m('l2-level-by-level#screens[4]', 1, 'mark-on-pop', '''
from collections import deque
def bfs(adj, start):
    queue = deque([start]); seen = set(); order = []
    while queue:
        u = queue.popleft(); seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: queue.append(v)
    return order
''')
m('l2-level-by-level#screens[4]', 7, 'recursive-bfs', '''
from collections import deque
def bfs(adj, start):
    seen = {start}; queue = deque([start]); order = []
    def step():
        if not queue: return
        u = queue.popleft(); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v); queue.append(v)
        step()
    step()
    return order
''')
m('l2-level-by-level#screens[4]', 7, 'plain list with pop(0) (should pass)', '''
def bfs(adj, start):
    seen = {start}; queue = [start]; order = []
    while queue:
        u = queue.pop(0); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v); queue.append(v)
    return order
''')
m('l2-level-by-level#screens[8]', 1, 'expand-at-k', '''
from collections import deque
def within_hops(adj, start, k):
    dist = {start: 0}; queue = deque([start])
    while queue:
        u = queue.popleft()
        if dist[u] > k: continue
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; queue.append(v)
    return sorted(f for f in dist if f != start)
''')
m('l2-level-by-level#screens[8]', 3, 'record-then-stop', '''
from collections import deque
def within_hops(adj, start, k):
    dist = {start: 0}; queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                if dist[v] < k: queue.append(v)
    return sorted(f for f in dist if f != start)
''')
m('l2-level-by-level#screens[8]', 5, 'mark-on-pop list result', '''
from collections import deque
def within_hops(adj, start, k):
    queue = deque([(start, 0)]); seen = set(); out = []
    while queue:
        u, d = queue.popleft()
        seen.add(u)
        if u != start: out.append(u)
        if d == k: continue
        for v in adj[u]:
            if v not in seen: queue.append((v, d + 1))
    return sorted(out)
''')
m('l2-level-by-level#screens[8]', 7, 'no marking, level lists (variant)', '''
def within_hops(adj, start, k):
    frontier = [start]; out = []
    for _ in range(k):
        frontier = [v for u in frontier for v in adj[u] if v != start]
        out += frontier
    return sorted(out)
''')
m('l2-level-by-level#screens[8]', 7, 'no marking, level sets (variant)', '''
def within_hops(adj, start, k):
    frontier = {start}; out = set()
    for _ in range(k):
        frontier = {v for u in frontier for v in adj[u]}
        out |= frontier
    return sorted(out - {start})
''')
m('l3-going-deep#screens[2]', 1, 'no-seen-check', '''
def dfs(adj, start):
    seen = set(); order = []
    def visit(u):
        seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            visit(v)
    visit(start)
    return order
''')
m('l3-going-deep#screens[2]', 4, 'parent-only (variant)', '''
def dfs(adj, start):
    order = []
    def visit(u, p):
        order.append(u)
        for v in sorted(adj[u]):
            if v != p: visit(v, u)
    visit(start, None)
    return order
''')
m('l3-going-deep#screens[5]', 1, 'sorted-push', '''
def dfs_stack(adj, start):
    seen = set(); stack = [start]; order = []
    while stack:
        u = stack.pop()
        if u in seen: continue
        seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: stack.append(v)
    return order
''')
m('l3-going-deep#screens[5]', 1, 'no-skip-on-pop', '''
def dfs_stack(adj, start):
    seen = set(); stack = [start]; order = []
    while stack:
        u = stack.pop()
        seen.add(u); order.append(u)
        for v in sorted(adj[u], reverse=True):
            if v not in seen: stack.append(v)
    return order
''')
m('l3-going-deep#screens[5]', 3, 'mark-on-push (variant)', '''
def dfs_stack(adj, start):
    seen = {start}; stack = [start]; order = []
    while stack:
        u = stack.pop()
        order.append(u)
        for v in sorted(adj[u], reverse=True):
            if v not in seen:
                seen.add(v); stack.append(v)
    return order
''')
m('l3-going-deep#screens[5]', 6, 'recursive', '''
def dfs_stack(adj, start):
    seen = set(); order = []
    def visit(u):
        seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: visit(v)
    visit(start)
    return order
''')
m('l3-going-deep#screens[8]', 2, 'only-nodes-with-edges', '''
def count_components(adj):
    seen = set(); count = 0
    for s in adj:
        if s in seen or not adj[s]: continue
        count += 1; seen.add(s); stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); stack.append(v)
    return count
''')
m('l3-going-deep#screens[8]', 7, 'recursive', '''
def count_components(adj):
    seen = set(); count = 0
    def visit(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen: visit(v)
    for s in adj:
        if s not in seen:
            count += 1; visit(s)
    return count
''')
m('l3-going-deep#screens[9]', 2, 'plain-seen', '''
def has_cycle(rules):
    seen = set()
    def visit(u):
        seen.add(u)
        for v in rules[u]:
            if v in seen: return True
            if visit(v): return True
        return False
    return any(r not in seen and visit(r) for r in rules)
''')
m('l3-going-deep#screens[9]', 5, 'first-rule-only', '''
def has_cycle(rules):
    state = {r: "new" for r in rules}
    def visit(u):
        state[u] = "active"
        for v in rules[u]:
            if state[v] == "active": return True
            if state[v] == "new" and visit(v): return True
        state[u] = "done"
        return False
    for r in rules:
        return visit(r)
    return False
''')
m('l4-islands#screens[2]', 2, 'no-bounds', '''
def neighbours(r, c, rows, cols):
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
''')
ISL = '''
def count_islands(grid):
    rows = len(grid)
    cols = %s
    seen = set(); count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                count += 1; seen.add((r, c)); stack = [(r, c)]
                while stack:
                    a, b = stack.pop()
                    for x, y in %s:
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 1 and (x, y) not in seen:
                            seen.add((x, y)); stack.append((x, y))
    return count
'''
N4 = '((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1))'
N8 = '[(a + i, b + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)]'
m('l4-islands#screens[4]', 2, 'no-empty-guard', ISL % ('len(grid[0])', N4))
m('l4-islands#screens[4]', 1, 'diagonals', ISL % ('len(grid[0]) if rows else 0', N8))
m('l4-islands#screens[4]', 10, 'sinking', '''
def count_islands(grid):
    rows = len(grid); cols = len(grid[0]) if rows else 0
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                count += 1; grid[r][c] = 0; stack = [(r, c)]
                while stack:
                    a, b = stack.pop()
                    for x, y in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 1:
                            grid[x][y] = 0; stack.append((x, y))
    return count
''')
m('l4-islands#screens[4]', 11, 'recursive flood fill, 400 deep (should pass)', '''
def count_islands(grid):
    rows = len(grid); cols = len(grid[0]) if rows else 0
    seen = set(); count = 0
    def fill(a, b):
        seen.add((a, b))
        for x, y in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == 1 and (x, y) not in seen:
                fill(x, y)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                count += 1; fill(r, c)
    return count
''')
m('l4-islands#screens[8]', 6, 'non-strict <= (should pass)', '''
def count_loss_regions(pnl, limit):
    rows = len(pnl); cols = len(pnl[0]) if rows else 0
    seen = set(); count = 0
    for r in range(rows):
        for c in range(cols):
            if pnl[r][c] <= -limit and (r, c) not in seen:
                count += 1; seen.add((r, c)); stack = [(r, c)]
                while stack:
                    a, b = stack.pop()
                    for x, y in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
                        if 0 <= x < rows and 0 <= y < cols and pnl[x][y] <= -limit and (x, y) not in seen:
                            seen.add((x, y)); stack.append((x, y))
    return count
''')
TOPO = '''
import heapq
from collections import deque
def topo_sort(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]: indeg[v] += 1
    %s
    return %s
'''
HEAPLOOP = '''ready = [u for u in adj if indeg[u] == 0]
    heapq.heapify(ready); order = []
    while ready:
        u = heapq.heappop(ready); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(ready, v)'''
m('l5-tasks-in-order#screens[3]', 1, 'plain-queue', TOPO % ('''ready = deque(u for u in adj if indeg[u] == 0); order = []
    while ready:
        u = ready.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: ready.append(v)''', 'order if len(order) == len(adj) else None'))
m('l5-tasks-in-order#screens[3]', 3, 'no-cycle-check', TOPO % (HEAPLOOP, 'order'))
m('l5-tasks-in-order#screens[3]', 6, 'empty-is-None', TOPO % (HEAPLOOP, 'order if order and len(order) == len(adj) else None'))
RUN = '''
import heapq
def run_order(deps):
    jobs = set(deps)
    %s
    after = {j: [] for j in jobs}; indeg = {j: 0 for j in jobs}
    for job, pre in deps.items():
        for p in pre:
            if p in after:
                after[p].append(job); indeg[job] += 1
    ready = [j for j in jobs if indeg[j] == 0]
    heapq.heapify(ready); order = []
    while ready:
        u = heapq.heappop(ready); order.append(u)
        for v in after[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(ready, v)
    return order if len(order) == len(jobs) else None
'''
m('l5-tasks-in-order#screens[8]', 1, 'no-raw-inputs', RUN % 'pass')
m('review-1#items[7]', 2, 'undirected', '''
def has_path(adj, s, t):
    und = {u: set() for u in adj}
    for u in adj:
        for v in adj[u]: und[u].add(v); und[v].add(u)
    seen = {s}; stack = [s]
    while stack:
        u = stack.pop()
        if u == t: return True
        for v in und[u]:
            if v not in seen: seen.add(v); stack.append(v)
    return False
''')
m('review-1#items[7]', 4, 'check-on-discovery', '''
def has_path(adj, s, t):
    seen = {s}; stack = [s]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v == t: return True
            if v not in seen: seen.add(v); stack.append(v)
    return False
''')
m('review-1#items[7]', 7, 'recursive', '''
def has_path(adj, s, t):
    seen = set()
    def go(u):
        if u == t: return True
        seen.add(u)
        return any(v not in seen and go(v) for v in adj[u])
    return go(s)
''')
m('review-1#items[7]', 7, 'recursive plain loop', '''
def has_path(adj, s, t):
    seen = set()
    def go(u):
        if u == t: return True
        seen.add(u)
        for v in adj[u]:
            if v not in seen and go(v): return True
        return False
    return go(s)
''')
m('homework-1#items[1]', 2, 'first-source-only', '''
from collections import deque
def days_to_spread(adj, defaulted):
    day = {f: 0 for f in defaulted[:1]}
    queue = deque(defaulted[:1])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in day: day[v] = day[u] + 1; queue.append(v)
    if len(day) < len(adj): return -1
    return max(day.values()) if day else 0
''')
m('homework-1#items[1]', 5, 'no-reach-check', '''
from collections import deque
def days_to_spread(adj, defaulted):
    day = {f: 0 for f in defaulted}
    queue = deque(defaulted)
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in day: day[v] = day[u] + 1; queue.append(v)
    return max(day.values()) if day else 0
''')
m('homework-1#items[1]', 8, 'one BFS per source (should pass)', '''
from collections import deque
def days_to_spread(adj, defaulted):
    best = {}
    for s in defaulted:
        day = {s: 0}; queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in day: day[v] = day[u] + 1; queue.append(v)
        for k, d in day.items(): best[k] = min(d, best.get(k, d))
    if len(best) < len(adj): return -1
    return max(best.values()) if best else 0
''')
ROUNDS = '''
def batch_rounds(deps):
    jobs = set(deps)
    %s
    after = {j: [] for j in jobs}; indeg = {j: 0 for j in jobs}
    for job, pre in deps.items():
        for p in pre:
            if p in after: after[p].append(job); indeg[job] += 1
    current = [j for j in jobs if indeg[j] == 0]
    %s
    done = rounds = 0
    while current:
        rounds += 1; done += len(current); nxt = []
        for u in current:
            for v in after[u]:
                indeg[v] -= 1
                if indeg[v] == 0: nxt.append(v)
        current = nxt
    return %s
'''
ALLJ = 'for pre in deps.values(): jobs.update(pre)'
m('homework-1#items[2]', 1, 'raw-inputs-not-counted', ROUNDS % ('pass', 'pass', 'rounds if done == len(jobs) else None'))
m('homework-1#items[2]', 3, 'empty-is-None', ROUNDS % (ALLJ, 'pass', 'rounds if rounds and done == len(jobs) else None'))
m('homework-1#items[2]', 4, 'no-cycle-check', ROUNDS % (ALLJ, 'pass', 'rounds'))
m('homework-1#items[2]', 7, 'cycle-check-at-start-only', ROUNDS % (ALLJ, 'if jobs and not current: return None', 'rounds'))
SPLIT = '''
from collections import deque
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b)
        %s
    group = {}
    for start in %s:
        if start in group: continue
        group[start] = 0; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in group:
                    group[v] = 1 - group[u]; queue.append(v)
                elif group[v] == group[u]:
                    %s
    return group
'''
m('homework-1#items[8]', 2, 'one-way', SPLIT % ('pass', 'sorted(desks)', 'return None'))
m('homework-1#items[8]', 3, 'no-clash-check', SPLIT % ('adj[b].append(a)', 'sorted(desks)', 'pass'))
m('homework-1#items[8]', 4, 'first-set-only', SPLIT % ('adj[b].append(a)', 'sorted(desks)[:1]', 'return None'))
m('homework-1#items[8]', 5, 'adj-from-conflicts', '''
from collections import deque
def split_desks(desks, conflicts):
    adj = {}
    for a, b in conflicts:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    group = {}
    for start in sorted(adj):
        if start in group: continue
        group[start] = 0; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in group: group[v] = 1 - group[u]; queue.append(v)
                elif group[v] == group[u]: return None
    return group
''')
m('homework-1#items[8]', 6, 'given-order', SPLIT % ('adj[b].append(a)', 'desks', 'return None'))
m('homework-1#items[8]', 7, 'any-loop-is-clash', '''
from collections import deque
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}; parent = {}
    for start in sorted(desks):
        if start in group: continue
        group[start] = 0; parent[start] = None; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in group:
                    group[v] = 1 - group[u]; parent[v] = u; queue.append(v)
                elif v != parent[u] and parent.get(v) != u:
                    return None
    return group
''')
m('homework-1#items[8]', 8, 'one-conflict-at-a-time', '''
def split_desks(desks, conflicts):
    group = {}
    for a, b in conflicts:
        if a not in group and b not in group:
            lo, hi = sorted((a, b)); group[lo] = 0; group[hi] = 1
        elif a in group and b not in group: group[b] = 1 - group[a]
        elif b in group and a not in group: group[a] = 1 - group[b]
        elif group[a] == group[b]: return None
    for d in desks: group.setdefault(d, 0)
    return group
''')
m('homework-1#items[8]', 9, 'clash-only-in-first-set', '''
from collections import deque
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}; first = True
    for start in sorted(desks):
        if start in group: continue
        group[start] = 0; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in group: group[v] = 1 - group[u]; queue.append(v)
                elif group[v] == group[u] and first: return None
        first = False
    return group
''')
m('homework-1#items[8]', 10, 'recursive', '''
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}
    def paint(u, g):
        group[u] = g
        for v in adj[u]:
            if v not in group:
                if not paint(v, 1 - g): return False
            elif group[v] == g: return False
        return True
    for start in sorted(desks):
        if start not in group and not paint(start, 0): return None
    return group
''')


SP = '''
from collections import deque
def shortest_path(adj, s, t):
    %s
'''
m('l6-fewest-steps#screens[4]', 1, 'not-reversed', SP % '''parent = {s: None}; queue = deque([s])
    while queue:
        u = queue.popleft()
        if u == t: break
        for v in sorted(adj[u]):
            if v not in parent: parent[v] = u; queue.append(v)
    if t not in parent: return None
    path = []; node = t
    while node is not None: path.append(node); node = parent[node]
    return path''')
m('l6-fewest-steps#screens[4]', 5, 'no-reach-check', SP % '''parent = {s: None}; queue = deque([s])
    while queue:
        u = queue.popleft()
        if u == t: break
        for v in sorted(adj[u]):
            if v not in parent: parent[v] = u; queue.append(v)
    path = []; node = t
    while node is not None: path.append(node); node = parent[node]
    return path[::-1]''')
m('l6-fewest-steps#screens[4]', 4, 'same-node-empty', SP % '''if s == t: return []
    parent = {s: None}; queue = deque([s])
    while queue:
        u = queue.popleft()
        for v in sorted(adj[u]):
            if v not in parent: parent[v] = u; queue.append(v)
    if t not in parent: return None
    path = []; node = t
    while node is not None: path.append(node); node = parent[node]
    return path[::-1]''')
FC = '''
from collections import deque
def fewest_conversions(pairs, src, dst):
    adj = {}
    for a, b in pairs:
        %s
    dist = {src: %s}; queue = deque([src])
    while queue:
        u = queue.popleft()
        if u == dst: return dist[u]
        for v in %s:
            if v not in dist: dist[v] = dist[u] + 1; queue.append(v)
    return -1
'''
BOTH = 'adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)'
m('l6-fewest-steps#screens[8]', 1, 'counts-currencies', FC % (BOTH, '1', 'adj.get(u, [])'))
m('l6-fewest-steps#screens[8]', 1, 'one-direction a->b', FC % ('adj.setdefault(a, []).append(b)', '0', 'adj.get(u, [])'))
m('l6-fewest-steps#screens[8]', 3, 'one-direction b->a (variant)', FC % ('adj.setdefault(b, []).append(a)', '0', 'adj.get(u, [])'))
m('l6-fewest-steps#screens[8]', 7, 'adj[u] KeyError', FC % (BOTH, '0', 'adj[u]'))
DJ = '''
import heapq, math
def dijkstra(adj, s):
%s
'''
m('l7-dijkstra#screens[4]', 1, 'seen-on-push', DJ % '''    dist = {u: math.inf for u in adj}; dist[s] = 0; seen = {s}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            if v not in seen:
                seen.add(v); dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist''')
m('l7-dijkstra#screens[4]', 1, 'record-on-pop', DJ % '''    dist = {u: math.inf for u in adj}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        dist[u] = d
        for v, w in adj[u]:
            heapq.heappush(heap, (d + w, v))
    return dist''')
m('l7-dijkstra#screens[4]', 1, 'reached-only dict', DJ % '''    dist = {s: 0}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if v not in dist or d + w < dist[v]:
                dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist''')
m('l7-dijkstra#screens[4]', 9, 'no-stale-check', DJ % '''    dist = {u: math.inf for u in adj}; dist[s] = 0; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist''')
SA = '''
import heapq, math
def slowest_arrival(links, centres, src):
    adj = {c: [] for c in centres}
    for a, b, ms in links: adj[a].append((b, ms))
    dist = {c: math.inf for c in %s}
    dist[src] = 0; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, ms in adj[u]:
            if d + ms < dist[v]:
                dist[v] = d + ms; heapq.heappush(heap, (d + ms, v))
    %s
'''
m('l7-dijkstra#screens[9]', 1, 'sum-of-costs', SA % ('centres', 'return sum(dist.values())'))
m('l7-dijkstra#screens[9]', 4, 'max-of-finite', SA % ('centres', 'return max(d for d in dist.values() if d < math.inf)'))
m('l7-dijkstra#screens[9]', 8, 'nodes-from-links', SA % ('({a for a, b, m in links} | {b for a, b, m in links} | {src})', 'w = max(dist.values()); return -1 if w == math.inf else w'))
DSU = '''
class DSU:
    def __init__(self, n):
        self.parent = list(range(n)); self.size = [1] * n; self.groups = n
    def find(self, x):
%s
    def union(self, a, b):
%s
    def count(self):
        return self.groups
'''
FIND_OK = '''        root = x
        while self.parent[root] != root: root = self.parent[root]
        while x != root:
            nxt = self.parent[x]; self.parent[x] = root; x = nxt
        return root'''
FIND_NAIVE = '''        while self.parent[x] != x: x = self.parent[x]
        return x'''
FIND_REC = '''        if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])
        return self.parent[x]'''
UN_OK = '''        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        self.parent[ra] = rb; self.groups -= 1
        return True'''
m('l8-groups#screens[5]', 5, 'count-drops-on-self-union', DSU % (FIND_OK, '''        ra, rb = self.find(a), self.find(b)
        self.groups -= 1
        if ra == rb: return False
        self.parent[ra] = rb
        return True'''))
m('l8-groups#screens[5]', 5, 'no-root-check (variant)', DSU % (FIND_OK, '''        ra, rb = self.find(a), self.find(b)
        self.parent[ra] = rb; self.groups -= 1
        return True'''))
m('l8-groups#screens[5]', 7, 'repoint-node', DSU % (FIND_OK, '''        if self.find(a) == self.find(b): return False
        self.parent[a] = b; self.groups -= 1
        return True'''))
m('l8-groups#screens[5]', 9, 'naive-find chain (variant)', DSU % (FIND_NAIVE, UN_OK))
m('l8-groups#screens[5]', 9, 'recursive-find chain', DSU % (FIND_REC, UN_OK))
CL = '''
def clusters(names, pairs, threshold=0.7):
    index = {name: i for i, name in enumerate(names)}
    d = DSU(len(names))
    for a, b, rho in pairs:
        if %s: d.union(index[a], index[b])
    groups = {}
    for name in names:
        groups.setdefault(%s, []).append(name)
    return sorted(sorted(g) for g in groups.values())
'''
m('l8-groups#screens[9]', 1, 'no-abs', CL % ('rho > threshold', 'd.find(index[name])'))
m('l8-groups#screens[9]', 3, 'non-strict', CL % ('abs(rho) >= threshold', 'd.find(index[name])'))
m('l8-groups#screens[9]', 7, 'group-by-parent', CL % ('abs(rho) > threshold', 'd.parent[index[name]]'))
BF = '''
import math
def bellman_ford(edges, n, s):
    dist = [math.inf] * n; dist[s] = 0
    for _ in range(%s):
        for u, v, w in edges:
            if dist[u] + w < dist[v]: dist[v] = dist[u] + w
    %s
    return dist
'''
DET = '''for u, v, w in edges:
        if dist[u] + w %s dist[v]: return None'''
m('l9-arbitrage-cycle#screens[4]', 1, 'one-pass', BF % ('1', DET % '<'))
m('l9-arbitrage-cycle#screens[4]', 3, 'no-detection', BF % ('n - 1', 'pass'))
m('l9-arbitrage-cycle#screens[4]', 6, 'non-strict detection (variant)', BF % ('n - 1', DET % '<='))
HA = '''
import math
def has_arbitrage(rates):
    names = sorted(set(rates) | {b for a in rates for b in rates[a]})
    index = {c: i for i, c in enumerate(names)}
    n = len(names)
    edges = [(index[a], index[b], %s) for a in rates for b, r in rates[a].items()]
    %s
'''
VS = 'edges += [(n, i, 0.0) for i in range(n)]\n    return bellman_ford(edges, n + 1, n, eps=%s) is None'
m('l9-arbitrage-cycle#screens[9]', 2, 'minus-rate', HA % ('-r', VS % '1e-9'))
m('l9-arbitrage-cycle#screens[9]', 4, 'no-eps', HA % ('-math.log(r)', VS % '0.0'))
m('l9-arbitrage-cycle#screens[9]', 9, 'no-start-node', HA % ('-math.log(r)', 'return bellman_ford(edges, n, 0, eps=1e-9) is None'))
MZ = '''
from collections import deque
def maze_steps(grid):
    rows, cols = len(grid), len(grid[0])
    %s
    dist = {(0, 0): %s}; queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (rows - 1, cols - 1): return dist[(r, c)]
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1; queue.append((nr, nc))
    return -1
'''
m('homework-2#items[0]', 1, 'counts-cells', MZ % ('if grid[0][0] == "#": return -1', '1'))
m('homework-2#items[0]', 4, 'no-start-wall-check', MZ % ('pass', '0'))
CW = '''
import math
def cheapest_within(quotes, src, dst, k):
    cost = {src: 0}
    for _ in range(%s):
        new = %s
        for a, b, bp in quotes:
            if a in cost and cost[a] + bp < new.get(b, math.inf): new[b] = cost[a] + bp
        cost = new
    return cost.get(dst, -1)
'''
m('homework-2#items[1]', 1, 'k-rounds', CW % ('k', 'dict(cost)'))
m('homework-2#items[1]', 1, 'no-copy', CW % ('k + 1', 'cost'))
m('homework-2#items[1]', 2, 'plain-dijkstra (variant)', '''
import heapq, math
def cheapest_within(quotes, src, dst, k):
    adj = {}
    for a, b, bp in quotes: adj.setdefault(a, []).append((b, bp))
    dist = {src: 0}; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in adj.get(u, []):
            if d + w < dist.get(v, math.inf): dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist.get(dst, -1)
''')
m('homework-2#items[2]', 1, 'direct-shares-only', '''
def count_clients(records):
    n = len(records); used = [False] * n; c = 0
    for i in range(n):
        if used[i]: continue
        c += 1
        for j in range(i + 1, n):
            if set(records[i]) & set(records[j]): used[j] = True
    return c
''')
CC = '''
import heapq
def count_cheapest(links, src, dst):
    adj = {}
    for a, b, fee in links:
        adj.setdefault(a, []).append((b, fee))
        %s
    cost = {src: 0}; ways = {src: 1}; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        %s
        if u == dst: return d, ways[u]
        for v, fee in %s:
            nd = %s + fee
            if v not in cost or nd < cost[v]:
                cost[v] = nd; %s
                heapq.heappush(heap, (nd, v))
                %s
            elif nd == cost[v]:
                %s
    return None, 0
'''
STALE = 'if d > cost[u]: continue'
def cc(und='pass', stale=STALE, nb='adj.get(u, [])', base='d', better='ways[v] = ways[u]', early='pass', tie='ways[v] += ways[u]'):
    return CC % (und, stale, nb, base, better, early, tie)
m('homework-2#items[8]', 2, 'tie-adds-1', cc(tie='ways[v] += 1'))
m('homework-2#items[8]', 3, 'cheaper-keeps-count', cc(better='ways[v] = ways.get(v, 0) + ways[u]'))
m('homework-2#items[8]', 1, 'return-on-first-reach', cc(early='\n                if v == dst: return nd, ways[v]'))
m('homework-2#items[8]', 5, 'no-stale-check, cost[u] base', cc(stale='pass', base='cost[u]'))
m('homework-2#items[8]', 5, 'no-stale-check, d base (variant)', cc(stale='pass'))
m('homework-2#items[8]', 7, 'undirected', cc(und='adj.setdefault(b, []).append((a, fee))'))


SUB = '''
def subsets(xs):
    out, path = [], []
    %s
    def walk(i):
        if i == len(xs):
            out.append(%s)
            return
        %s
    walk(0)
    return out
'''
PERM = '''
def permutations(xs):
    out, path = [], []
    used = [False] * len(xs)
    %s
    def walk():
        if len(path) == len(xs):
            out.append(path[:])
            return
        for i, x in enumerate(xs):
            if not used[i]:
                used[i] = True; path.append(x); walk(); path.pop(); used[i] = False
    walk()
    return out
'''
TAKE = 'path.append(xs[i]); walk(i + 1); path.pop(); walk(i + 1)'
SKIP = 'walk(i + 1); path.append(xs[i]); walk(i + 1); path.pop()'
m('l10-every-subset#screens[9]', 1, 'skip-first', SUB % ('pass', 'path[:]', SKIP) + PERM % 'pass')
m('l10-every-subset#screens[9]', 2, 'empty-input-none', SUB % ('if not xs: return []', 'path[:]', TAKE) + PERM % 'pass')
m('l10-every-subset#screens[9]', 1, 'stores-path-itself', SUB % ('pass', 'path', TAKE) + PERM % 'pass')
m('l10-every-subset#screens[9]', 7, 'perm-empty-none', SUB % ('pass', 'path[:]', TAKE) + PERM % 'if not xs: return []')

NQ = '''
def n_queens(n):
    cols, diag, anti = set(), set(), set()
    def place(row):
        if row == n: return 1
        count = 0
        for c in range(n):
            if c in cols or row - c in diag or row + c in anti: continue
            cols.add(c); diag.add(row - c); anti.add(row + c)
            count += place(row + 1)
            %s
        return count
    return place(0)
'''
UNDO = 'cols.remove(c); diag.remove(row - c); anti.remove(row + c)'
SS = '''
def subset_sum(xs, target):
    xs = sorted(xs)
    def walk(i, total):
%s
    return walk(0, 0)
'''
SS_OK = '''        if total == target: return True
        if i == len(xs) or total + xs[i] > target: return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)'''
m('l11-dead-ends#screens[8]', 2, 'no-undo', NQ % 'pass' + SS % SS_OK)
m('l11-dead-ends#screens[8]', 10, 'end-check-before-target-check (variant)', NQ % UNDO + SS % '''        if i == len(xs): return False
        if total == target: return True
        if total + xs[i] > target: return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)''')
m('l11-dead-ends#screens[8]', 10, 'empty-list-special-case', NQ % UNDO + '''
def subset_sum(xs, target):
    if not xs: return False
    xs = sorted(xs)
    def walk(i, total):
''' + SS_OK + '''
    return walk(0, 0)
''')
m('l11-dead-ends#screens[8]', 13, 'no-prune, full tree (variant)', NQ % UNDO + SS % '''        if total == target: return True
        if i == len(xs): return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)''')
m('l11-dead-ends#screens[8]', 13, 'unsorted overshoot prune (should pass)', NQ % UNDO + '''
def subset_sum(xs, target):
    def walk(i, total):
        if total == target: return True
        if total > target or i == len(xs): return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)
    return walk(0, 0)
''')
FM = '''
%s
def fib_memo(n):
    %s
    computed = 0
    def f(k):
        nonlocal computed
%s
    return f(n), computed
'''
GP = '''
def grid_paths(r, c):
    cache = {}
    def paths(i, j):
        if i == 1 or j == 1: return 1
        %s
    return paths(r, c)
'''
GP_OK = '''if (i, j) not in cache: cache[(i, j)] = paths(i - 1, j) + paths(i, j - 1)
        return cache[(i, j)]'''
F_OK = '''        if k in cache: return cache[k]
        computed += 1
        value = k if k < 2 else f(k - 1) + f(k - 2)
        cache[k] = value
        return value'''
m('l12-remembering#screens[9]', 1, 'base-not-counted', FM % ('', 'cache = {}', '''        if k < 2: return k
        if k in cache: return cache[k]
        computed += 1
        cache[k] = f(k - 1) + f(k - 2)
        return cache[k]''') + GP % GP_OK)
m('l12-remembering#screens[9]', 3, 'counts-lookups', FM % ('', 'cache = {}', '''        computed += 1
        if k in cache: return cache[k]
        value = k if k < 2 else f(k - 1) + f(k - 2)
        cache[k] = value
        return value''') + GP % GP_OK)
m('l12-remembering#screens[9]', 3, 'module-level cache', FM % ('cache = {}', 'pass', F_OK) + GP % GP_OK)
m('l12-remembering#screens[9]', 6, 'default-arg cache (variant)', '''
def fib_memo(n, cache={}):
    computed = 0
    def f(k):
        nonlocal computed
''' + F_OK + '''
    return f(n), computed
''' + GP % GP_OK)
m('l12-remembering#screens[9]', 12, 'grid-not-memoised', FM % ('', 'cache = {}', F_OK) + GP % 'return paths(i - 1, j) + paths(i, j - 1)')
ST_OK = '''
def stairs(n):
    prev, cur = 1, 1
    for _ in range(2, n + 1): prev, cur = cur, prev + cur
    return cur
'''
MC = '''
def min_coins(coins, amount):
    INF = float('inf')
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]: best[a] = best[a - c] + 1
    return %s
'''
MC_OK = MC % 'best[amount] if best[amount] < INF else -1'
m('l13-climbing-stairs#screens[9]', 1, 'ways0-is-0', '''
def stairs(n):
    if n == 0: return 0
    prev, cur = 1, 1
    for _ in range(2, n + 1): prev, cur = cur, prev + cur
    return cur
''' + MC_OK)
m('l13-climbing-stairs#screens[9]', 6, 'memo-recursion', '''
def stairs(n, memo={}):
    if n < 2: return 1
    if n not in memo: memo[n] = stairs(n - 1) + stairs(n - 2)
    return memo[n]
''' + MC_OK)
m('l13-climbing-stairs#screens[9]', 7, 'greedy', ST_OK + '''
def min_coins(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c; amount %= c
    return n if amount == 0 else -1
''')
m('l13-climbing-stairs#screens[9]', 8, 'zero-amount-is-minus-1', ST_OK + MC % 'best[amount] if 0 < best[amount] < INF else -1')
m('l13-climbing-stairs#screens[9]', 9, 'returns-inf', ST_OK + MC % 'best[amount]')
CS = '''
def combination_sum(candidates, target):
    cands = %s
    out, path = [], []
    %s
    def walk(start, left):
        if left == 0:
            out.append(path[:]); return
        for i in range(%s, len(cands)):
            if cands[i] > left: %s
            path.append(cands[i]); walk(i, left - cands[i]); path.pop()
    walk(0, target)
    return out
'''
m('homework-3#items[0]', 1, 'loop-from-0', CS % ('sorted(candidates)', 'pass', '0', 'break'))
m('homework-3#items[0]', 3, 'not-sorted', CS % ('candidates', 'pass', 'start', 'break'))
m('homework-3#items[0]', 5, 'zero-target-empty', CS % ('sorted(candidates)', 'if target == 0: return []', 'start', 'break'))
WB = '''
def word_break(s, words):
    words = set(words)
    %s
    def ok(i):
        if i == len(s): return True
        for w in words:
            if w and s.startswith(w, i) and ok(i + len(w)): return True
        return False
    return ok(0)
'''
m('homework-3#items[1]', 5, 'empty-string-false', WB % 'if not s: return False')
m('homework-3#items[1]', 8, 'no-memo', WB % 'pass')
m('homework-3#items[1]', 2, 'prefix-greedy-accepts-partial', '''
def word_break(s, words):
    i = 0
    while i < len(s):
        for w in sorted(words, key=len, reverse=True):
            if w and s.startswith(w, i): i += len(w); break
        else:
            return i > 0
    return True
''')
m('homework-3#items[8]', 2, 'single-best-trade', '''
def trade_with_fee(prices, fee):
    best, lo = 0, None
    for p in prices:
        if lo is None or p < lo: lo = p
        best = max(best, p - lo - fee)
    return best
''')
m('homework-3#items[8]', 3, 'each-rise-net-of-fee', '''
def trade_with_fee(prices, fee):
    total, i, n = 0, 0, len(prices)
    while i < n:
        j = i
        while j + 1 < n and prices[j + 1] >= prices[j]: j += 1
        total += max(0, prices[j] - prices[i] - fee)
        i = j + 1
    return total
''')
FEE = '''
def trade_with_fee(prices, fee):
    flat, long = 0, float('-inf')
    for p in %s:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat
'''
m('homework-3#items[8]', 4, 'skips-first-day', FEE % 'prices[1:]')
m('homework-3#items[8]', 5, 'skips-last-day', '''
def trade_with_fee(prices, fee):
    flat, long = 0, float('-inf')
    for i in range(len(prices) - 1):
        p = prices[i]
        flat, long = max(flat, long + p - fee), max(long, flat - p)
        if i == len(prices) - 2: long = max(long, flat - prices[i + 1])
    return flat
''')
m('homework-3#items[8]', 6, 'every-rise-even-below-fee', '''
def trade_with_fee(prices, fee):
    flat, long = 0, float('-inf'); traded = False
    for p in prices:
        nf = max(flat, long + p - fee)
        flat, long = nf, max(long, flat - p)
    if flat == 0 and len(prices) > 1:
        best = max(prices[j] - prices[i] - fee for i in range(len(prices)) for j in range(i + 1, len(prices)))
        return best
    return flat
''')
m('homework-3#items[8]', 7, 'empty-raises', '''
def trade_with_fee(prices, fee):
    flat, long = 0, -prices[0]
    for p in prices[1:]:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat
''')

m('homework-2#items[8]', 8, 'looks dst up in a dict of linked venues', '''
import heapq, math
def count_cheapest(links, src, dst):
    adj = {}
    for a, b, fee in links:
        adj.setdefault(a, []).append((b, fee)); adj.setdefault(b, [])
    adj.setdefault(src, [])
    cost = {v: math.inf for v in adj}; ways = {v: 0 for v in adj}
    cost[src] = 0; ways[src] = 1; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > cost[u]: continue
        for v, fee in adj[u]:
            nd = d + fee
            if nd < cost[v]:
                cost[v] = nd; ways[v] = ways[u]; heapq.heappush(heap, (nd, v))
            elif nd == cost[v]:
                ways[v] += ways[u]
    return (None, 0) if cost[dst] == math.inf else (cost[dst], ways[dst])
''')


# ---------------------------------------------------------------- run part C
for name, (ref, n, code) in M.items():
    w = widget(ref)
    first, fails = run_tests(w, code, stop='(should pass)' not in name)
    if '(should pass)' in name:
        check('C control passes every test: ' + name, first is None, fails)
    elif '(variant)' in name:
        if VERBOSE:
            print(f'info {name}: first failing test {first}')
    else:
        check('C first failing test is the one the line names: ' + name, first == n,
              f'first failing test is {first}' if first else 'passes every test')


# ---------------------------------------------------------------- part D: fix-pass sweep (docs/reviews/audit-graphs-dp-1-3-r2.md, ## Fix pass)
# The fixer's own submissions, written separately from part C: each is the widget's solution with the named mistake
# put in by a text replacement, so the mistake and nothing else differs. Every feedback.byKey["test-N"] line of the
# L1 to L3 code widgets is listed in SWEEP below, either with a submission (the line names a cause) or as a
# description (the line names no cause; its facts are checked against the test).
D = {}


def mut(ref, *pairs):
    code = widget(ref)['solution']
    for old, new in pairs:
        assert code.count(old) == 1, (ref, old)
        code = code.replace(old, new)
    return code


def dm(ref, n, tag, code):
    D[f'{ref} test-{n}: {tag}'] = (ref, n, code)


def fb_lines(ref):
    f, p = ref.split('#')
    key, i = p[:-1].split('[')
    return load(f)[key][int(i)].get('feedback', {}).get('byKey', {})


def expect(ref, n):
    return widget(ref)['tests'][n - 1]['expect']


R = 'l1-nodes-and-edges#screens[5]'
dm(R, 1, 'stores each edge at one end', mut(R, ('        if u != v:\n            adj[v].append(u)\n', '')))
dm(R, 2, 'keys from the edges only', mut(R, ('adj = {v: [] for v in nodes}', 'adj = {}'), ('adj[u].append(v)', 'adj.setdefault(u, []).append(v)'),
                                       ('            adj[v].append(u)', '            adj.setdefault(v, []).append(u)')))
dm(R, 3, 'self-loop added at both ends', mut(R, ('        if u != v:\n            adj[v].append(u)\n', '        adj[v].append(u)\n')))
R = 'l1-nodes-and-edges#screens[8]'
dm(R, 1, 'rows are one shared list', mut(R, ('[[0] * n for _ in range(n)]', '[[0] * n] * n')))
R = 'l1-nodes-and-edges#screens[9]'
dm(R, 3, 'checks only the arrows in', mut(R, ('into[f] == n - 1 and out[f] == 0', 'into[f] == n - 1')))
dm(R, 4, 'checks only that it posts to nobody', mut(R, ('into[f] == n - 1 and out[f] == 0', 'out[f] == 0')))
dm(R, 5, 'needs at least one poster', mut(R, ('into[f] == n - 1 and out[f] == 0', 'into[f] == n - 1 and out[f] == 0 and into[f] > 0')))
R = 'l2-level-by-level#screens[4]'
dm(R, 1, 'marks on pop', mut(R, ('seen = {start}', 'seen = set()'), ('        order.append(u)\n', '        seen.add(u)\n        order.append(u)\n'),
                            ('                seen.add(v)\n', '')))
dm(R, 7, 'recursive level search', '''
def bfs(adj, start):
    order, seen = [], {start}
    def level(frontier):
        if not frontier:
            return
        nxt = []
        for u in frontier:
            order.append(u)
            for v in sorted(adj[u]):
                if v not in seen:
                    seen.add(v); nxt.append(v)
        level(nxt)
    level([start])
    return order
''')
R = 'l2-level-by-level#screens[8]'
dm(R, 1, 'expands a firm at distance k', mut(R, ('        if dist[u] == k:\n            continue\n', '        if dist[u] > k:\n            continue\n')))
dm(R, 5, 'marks on pop, records a firm when queued', '''
from collections import deque
def within_hops(adj, start, k):
    seen, found = set(), []
    queue = deque([(start, 0)])
    while queue:
        u, d = queue.popleft()
        seen.add(u)
        if d == k:
            continue
        for v in adj[u]:
            if v not in seen:
                found.append(v)
                queue.append((v, d + 1))
    return sorted(found)
''')
R = 'l3-going-deep#screens[2]'
dm(R, 1, 'no seen check', mut(R, ('            if v not in seen:\n                visit(v)', '            visit(v)')))
R = 'l3-going-deep#screens[5]'
dm(R, 1, 'pushes in sorted order', mut(R, ('sorted(adj[u], reverse=True)', 'sorted(adj[u])')))
dm(R, 1, 'no skip on pop', mut(R, ('        if u in seen:\n            continue\n', '')))
dm(R, 6, 'recursive helper', mut(R, ('    return order\n', '    return order\n\n\ndef dfs_stack(adj, start):\n    order, seen = [], set()\n    def go(u):\n        seen.add(u); order.append(u)\n        for v in sorted(adj[u]):\n            if v not in seen: go(v)\n    go(start)\n    return order\n')))
R = 'l3-going-deep#screens[8]'
dm(R, 2, 'counts only nodes with edges', mut(R, ('        if s in seen:\n            continue', '        if s in seen or not adj[s]:\n            continue')))
dm(R, 7, 'recursive search', '''
def count_components(adj):
    seen = set()
    def go(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen: go(v)
    count = 0
    for s in adj:
        if s not in seen:
            count += 1; go(s)
    return count
''')
R = 'l3-going-deep#screens[9]'
dm(R, 2, 'plain seen set', '''
def has_cycle(rules):
    seen = set()
    def visit(u):
        seen.add(u)
        for v in rules[u]:
            if v in seen or visit(v):
                return True
        return False
    return any(r not in seen and visit(r) for r in rules)
''')
dm(R, 5, 'searches from the first rule only', mut(R, ('    return any(state[r] == "new" and visit(r) for r in rules)', '    return bool(rules) and visit(next(iter(rules)))')))
R = 'l4-islands#screens[2]'
dm(R, 1, 'adds diagonals', mut(R, ('((-1, 0), (1, 0), (0, -1), (0, 1))', '((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))')))
dm(R, 1, 'order left, right, up, down', mut(R, ('((-1, 0), (1, 0), (0, -1), (0, 1))', '((0, -1), (0, 1), (-1, 0), (1, 0))')))
dm(R, 2, 'no bounds check', mut(R, ('        if 0 <= nr < rows and 0 <= nc < cols:\n', '        if nr < rows and nc < cols:\n')))
R = 'l4-islands#screens[4]'
dm(R, 1, 'eight neighbours', mut(R, ('((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1))', '((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1), (a - 1, b - 1), (a - 1, b + 1), (a + 1, b - 1), (a + 1, b + 1))')))
dm(R, 2, 'no guard on the empty grid', mut(R, ('len(grid[0]) if rows else 0', 'len(grid[0])')))
dm(R, 10, 'sinks the land', mut(R, ('                count += 1\n', '                count += 1\n                grid[r][c] = 0\n'), ('                            seen.add((x, y))\n', '                            seen.add((x, y))\n                            grid[x][y] = 0\n')))
dm(R, 11, 'recursive flood fill (should pass)', '''
def count_islands(grid):
    rows = len(grid); cols = len(grid[0]) if rows else 0
    seen = set()
    def fill(r, c):
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != 1 or (r, c) in seen:
            return
        seen.add((r, c))
        fill(r - 1, c); fill(r + 1, c); fill(r, c - 1); fill(r, c + 1)
    n = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                n += 1; fill(r, c)
    return n
''')
R = 'l4-islands#screens[8]'
dm(R, 6, 'assumes a square grid', mut(R, ('cols = len(pnl[0]) if rows else 0', 'cols = rows')))
dm(R, 6, 'non-strict <= (should pass)', mut(R, ('            if pnl[r][c] < -limit and', '            if pnl[r][c] <= -limit and'),
                                              ('and pnl[x][y] < -limit and', 'and pnl[x][y] <= -limit and')))
R = 'l5-tasks-in-order#screens[3]'
dm(R, 1, 'plain queue', mut(R, ('    heapq.heapify(ready)\n', ''), ('heapq.heappop(ready)', 'ready.pop(0)'), ('heapq.heappush(ready, v)', 'ready.append(v)')))
dm(R, 3, 'no cycle check', mut(R, ('return order if len(order) == len(adj) else None', 'return order')))
dm(R, 6, 'empty order read as a cycle', mut(R, ('return order if len(order) == len(adj) else None', 'return order if order and len(order) == len(adj) else None')))
R = 'l5-tasks-in-order#screens[8]'
dm(R, 1, 'raw inputs left out', mut(R, ('    for pre in deps.values():\n        jobs.update(pre)\n', ''), ('            after[p].append(job)', '            after.setdefault(p, []).append(job)'),
                                     ('            indeg[job] += 1', '            indeg[job] += 1 if p in jobs else 0')))
R = 'review-1#items[7]'
dm(R, 2, 'treats the arrows as two-way', mut(R, ('    seen = {s}\n', '    back = {}\n    for a in adj:\n        for b in adj[a]:\n            back.setdefault(b, []).append(a)\n    seen = {s}\n'),
                                               ('        for v in adj[u]:', '        for v in adj[u] + back.get(u, []):')))
dm(R, 4, 'checks the target only on discovery', mut(R, ('        if u == t:\n            return True\n', ''), ('                seen.add(v)\n', '                if v == t:\n                    return True\n                seen.add(v)\n')))
dm(R, 7, 'recursive search', '''
def has_path(adj, s, t, seen=None):
    seen = seen if seen is not None else set()
    if s == t:
        return True
    seen.add(s)
    return any(v not in seen and has_path(adj, v, t, seen) for v in adj[s])
''')
R = 'homework-1#items[1]'
dm(R, 2, 'spreads from the first firm only', mut(R, ('day = {f: 0 for f in defaulted}', 'day = {f: 0 for f in defaulted[:1]}'), ('deque(defaulted)', 'deque(defaulted[:1])')))
dm(R, 5, 'no check that every firm is reached', mut(R, ('    if len(day) < len(adj):\n        return -1\n', '')))
dm(R, 8, 'one search per defaulted firm (should pass)', '''
from collections import deque
def days_to_spread(adj, defaulted):
    best = {}
    for s in defaulted:
        d = {s: 0}; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1; q.append(v)
        for v, x in d.items():
            best[v] = min(best.get(v, x), x)
    if len(best) < len(adj):
        return -1
    return max(best.values()) if best else 0
''')
R = 'homework-1#items[2]'
dm(R, 1, 'raw inputs not counted as a round', mut(R, ('    return rounds if done == len(jobs) else None', '    return rounds - 1 if done == len(jobs) else None')))
dm(R, 3, 'empty input read as a cycle', mut(R, ('    return rounds if done == len(jobs) else None', '    return rounds if done == len(jobs) and jobs else None')))
dm(R, 4, 'no cycle check', mut(R, ('    return rounds if done == len(jobs) else None', '    return rounds')))
dm(R, 7, 'cycle check only when nothing starts free', mut(R, ('    done = rounds = 0\n', '    if jobs and not current:\n        return None\n    done = rounds = 0\n'), ('    return rounds if done == len(jobs) else None', '    return rounds')))
R = 'homework-1#items[8]'
dm(R, 2, 'stores each conflict one way', mut(R, ('        adj[b].append(a)\n', '')))
dm(R, 3, 'no clash check', mut(R, ('                elif group[v] == group[u]:\n                    return None     # an odd loop: no split works\n', '')))
dm(R, 4, 'searches from the first desk only', mut(R, ('    for start in sorted(desks):', '    for start in sorted(desks)[:1]:')))
dm(R, 5, 'desks taken from the conflicts', mut(R, ('    adj = {d: [] for d in desks}\n    for a, b in conflicts:          # a conflict runs both ways\n        adj[a].append(b)\n        adj[b].append(a)\n',
                                                  '    adj = {}\n    for a, b in conflicts:\n        adj.setdefault(a, []).append(b)\n        adj.setdefault(b, []).append(a)\n'),
                                                 ('    for start in sorted(desks):', '    for start in sorted(adj):')))
dm(R, 6, 'desks in the given order', mut(R, ('    for start in sorted(desks):', '    for start in desks:')))
dm(R, 7, 'any placed neighbour but the parent is a clash', mut(R, ('        group[start] = 0\n', '        group[start] = 0\n        parent = {start: None}\n'),
                                                                   ('                    group[v] = 1 - group[u]\n', '                    group[v] = 1 - group[u]\n                    parent[v] = u\n'),
                                                                   ('                elif group[v] == group[u]:', '                elif v != parent.get(u):')))
dm(R, 8, 'places one conflict at a time', '''
def split_desks(desks, conflicts):
    group = {}
    for a, b in conflicts:
        if a not in group and b not in group:
            group[a], group[b] = 0, 1
        elif a not in group:
            group[a] = 1 - group[b]
        elif b not in group:
            group[b] = 1 - group[a]
        elif group[a] == group[b]:
            return None
    for d in desks:
        group.setdefault(d, 0)
    return group
''')
dm(R, 9, 'checks clashes only in the first linked set', mut(R, ('                elif group[v] == group[u]:', '                elif group[v] == group[u] and start == min(desks):')))
dm(R, 10, 'recursive search', mut(R, ('    return group\n', '    return group\n\n\ndef split_desks(desks, conflicts):\n    adj = {d: [] for d in desks}\n    for a, b in conflicts:\n        adj[a].append(b); adj[b].append(a)\n    group = {}\n    def go(u):\n        for v in adj[u]:\n            if v not in group:\n                group[v] = 1 - group[u]\n                if not go(v): return False\n            elif group[v] == group[u]:\n                return False\n        return True\n    for s in sorted(desks):\n        if s not in group:\n            group[s] = 0\n            if not go(s): return None\n    return group\n')))
R = 'l6-fewest-steps#screens[4]'
dm(R, 1, 'walk back not reversed', mut(R, ('    return path[::-1]', '    return path')))
dm(R, 1, 'depth-first stack', mut(R, ('        u = queue.popleft()', '        u = queue.pop()')))
dm(R, 4, 'start equal to target gives no route', mut(R, ('    parent = {s: None}', '    if s == t:\n        return []\n    parent = {s: None}')))
dm(R, 5, 'no reach check', mut(R, ('    if t not in parent:\n        return None\n', '')))
R = 'l6-fewest-steps#screens[8]'
dm(R, 1, 'counts currencies', mut(R, ('dist = {src: 0}', 'dist = {src: 1}')))
dm(R, 1, 'pairs stored a to b only', mut(R, ('        adj.setdefault(b, []).append(a)\n', '        adj.setdefault(b, [])\n')))
dm(R, 1, 'pairs stored b to a only', mut(R, ('        adj.setdefault(a, []).append(b)\n', '        adj.setdefault(a, [])\n')))
dm(R, 7, 'adj[u] without a default', mut(R, ('adj.get(u, [])', 'adj[u]')))
R = 'l7-dijkstra#screens[4]'
dm(R, 1, 'marks seen when first pushed', '''
import heapq, math
def dijkstra(adj, s):
    dist = {u: math.inf for u in adj}; dist[s] = 0
    seen = {s}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            if v not in seen:
                seen.add(v); dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist
''')
dm(R, 1, 'dict of reached nodes only', mut(R, ('dist = {u: math.inf for u in adj}\n    dist[s] = 0', 'dist = {s: 0}'), ('            if nd < dist[v]:', '            if nd < dist.get(v, math.inf):')))
dm(R, 9, 'no stale check', mut(R, ('        if d > dist[u]:\n            continue\n', '')))
R = 'l7-dijkstra#screens[9]'
dm(R, 1, 'sums every cost', mut(R, ('    worst = max(dist.values())', '    worst = sum(dist.values())')))
dm(R, 4, 'max over the reached centres only', mut(R, ('    worst = max(dist.values())', '    worst = max(x for x in dist.values() if x < math.inf)')))
dm(R, 8, 'centres taken from the links', mut(R, ('    adj = {c: [] for c in centres}', '    adj = {}\n    for a, b, ms in links:\n        adj.setdefault(a, []); adj.setdefault(b, [])\n    adj.setdefault(src, [])'),
                                            ('    dist = {c: math.inf for c in centres}', '    dist = {c: math.inf for c in adj}')))
R = 'l8-groups#screens[5]'
dm(R, 5, 'count falls before the root check', mut(R, ('        if ra == rb:\n            return False\n', '        if ra == rb:\n            self.groups -= 1\n            return False\n')))
dm(R, 7, 're-points the node, not its root', mut(R, ('        if self.size[ra] < self.size[rb]:   # union by size\n            ra, rb = rb, ra\n        self.parent[rb] = ra\n', '        self.parent[a] = rb\n')))
dm(R, 9, 'recursive find, no union by size', '''
class DSU:
    def __init__(self, n):
        self.parent = list(range(n)); self.groups = n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        self.parent[ra] = rb; self.groups -= 1; return True
    def count(self):
        return self.groups
''')
R = 'l8-groups#screens[9]'
dm(R, 1, 'compares rho, not abs(rho)', mut(R, ('if abs(rho) > threshold:', 'if rho > threshold:')))
dm(R, 3, 'non-strict threshold', mut(R, ('if abs(rho) > threshold:', 'if abs(rho) >= threshold:')))
dm(R, 7, 'groups by parent', mut(R, ('groups.setdefault(d.find(index[name]), [])', 'groups.setdefault(d.parent[index[name]], [])')))
R = 'l9-arbitrage-cycle#screens[4]'
dm(R, 1, 'one pass only', mut(R, ('    for _ in range(n - 1):', '    for _ in range(1):')))
dm(R, 1, 'n - 2 passes', mut(R, ('    for _ in range(n - 1):', '    for _ in range(n - 2):')))
dm(R, 3, 'no detection pass', mut(R, ('    for u, v, w in edges:\n        if dist[u] + w < dist[v]:\n            return None\n', '')))
R = 'l9-arbitrage-cycle#screens[9]'
dm(R, 2, 'weights ln(rate)', mut(R, ('-math.log(r))', 'math.log(r))')))
dm(R, 2, 'weights -rate', mut(R, ('-math.log(r))', '-r)')))
dm(R, 4, 'no eps', mut(R, ('n, eps=1e-9)', 'n)')))
dm(R, 9, 'search from the first currency only', mut(R, ('    edges += [(n, i, 0.0) for i in range(n)]   # a start joined to every currency\n    return bellman_ford(edges, n + 1, n, eps=1e-9) is None',
                                                    '    return bellman_ford(edges, n, index["GBP"] if "GBP" in index else 0, eps=1e-9) is None')))
R = 'homework-2#items[0]'
dm(R, 1, 'counts cells', mut(R, ('    dist = {(0, 0): 0}', '    dist = {(0, 0): 1}')))
dm(R, 4, 'no check on the start cell', mut(R, ('    if grid[0][0] == "#" or grid[rows - 1][cols - 1] == "#":', '    if grid[rows - 1][cols - 1] == "#":')))
R = 'homework-2#items[1]'
dm(R, 1, 'k rounds', mut(R, ('range(k + 1)', 'range(k)')))
dm(R, 1, 'relaxes in place, no copy', mut(R, ('        new = dict(cost)\n', '        new = cost\n')))
dm(R, 2, 'Dijkstra keeping one cost per currency, with a hop limit', '''
import heapq, math
def cheapest_within(quotes, src, dst, k):
    adj = {}
    for a, b, bp in quotes:
        adj.setdefault(a, []).append((b, bp))
    best = {src: 0}
    heap = [(0, 0, src)]
    while heap:
        d, h, u = heapq.heappop(heap)
        if d > best[u]:
            continue
        if u == dst:
            return d
        if h == k + 1:
            continue
        for v, bp in adj.get(u, []):
            if d + bp < best.get(v, math.inf):
                best[v] = d + bp
                heapq.heappush(heap, (d + bp, h + 1, v))
    return -1
''')
R = 'homework-2#items[2]'
dm(R, 1, 'merges only records that share directly with a group\'s first record', '''
def count_clients(records):
    leaders = []
    for i, ids in enumerate(records):
        if not any(set(ids) & set(records[j]) for j in leaders):
            leaders.append(i)
    return len(leaders)
''')
R = 'homework-2#items[8]'
dm(R, 1, 'returns when dst is first reached', mut(R, ('                cost[v] = nd        # a cheaper route: the old count is void\n                ways[v] = ways[u]\n',
                                                     '                cost[v] = nd        # a cheaper route: the old count is void\n                ways[v] = ways[u]\n                if v == dst:\n                    return nd, ways[v]\n')))
dm(R, 2, 'a tie adds 1', mut(R, ('ways[v] += ways[u]', 'ways[v] += 1')))
dm(R, 2, 'a tie pushes the venue again', mut(R, ('                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n', '                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n                heapq.heappush(heap, (nd, v))\n')))
dm(R, 3, 'a cheaper route keeps the old count', mut(R, ('                ways[v] = ways[u]\n', '                ways[v] = ways.get(v, 0) + ways[u]\n')))
dm(R, 5, 'no stale check, base cost[u]', mut(R, ('        if d > cost[u]:\n            continue                # a stale entry: u left the heap earlier\n', '        d = cost[u]\n')))
dm(R, 7, 'links stored both ways', mut(R, ('        adj.setdefault(a, []).append((b, fee))\n', '        adj.setdefault(a, []).append((b, fee))\n        adj.setdefault(b, []).append((a, fee))\n')))
dm(R, 8, 'looks dst up in a cost dict of the linked venues', '''
import heapq, math
def count_cheapest(links, src, dst):
    adj = {}
    for a, b, fee in links:
        adj.setdefault(a, []).append((b, fee)); adj.setdefault(b, [])
    cost = {v: math.inf for v in adj}; ways = {v: 0 for v in adj}
    cost[src] = 0; ways[src] = 1; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > cost[u]:
            continue
        for v, fee in adj[u]:
            nd = d + fee
            if nd < cost[v]:
                cost[v] = nd; ways[v] = ways[u]; heapq.heappush(heap, (nd, v))
            elif nd == cost[v]:
                ways[v] += ways[u]
    return (None, 0) if cost[dst] == math.inf else (cost[dst], ways[dst])
''')
dm(R, 11, 'counts the cheapest routes one by one', '''
import heapq, math
def count_cheapest(links, src, dst):
    adj = {}
    for a, b, fee in links:
        adj.setdefault(a, []).append((b, fee))
    cost = {src: 0}; heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > cost[u]:
            continue
        for v, fee in adj.get(u, []):
            if d + fee < cost.get(v, math.inf):
                cost[v] = d + fee; heapq.heappush(heap, (d + fee, v))
    if dst not in cost:
        return None, 0
    def walk(u):                    # follow only links on a cheapest route, one route at a time
        if u == dst:
            return 1
        return sum(walk(v) for v, fee in adj.get(u, []) if v in cost and cost[u] + fee == cost[v] and cost[v] <= cost[dst])
    return cost[dst], walk(src)
''')
R = 'l10-every-subset#screens[9]'
dm(R, 1, 'skip before take', mut(R, ('        path.append(xs[i])           # choose: take xs[i]\n        walk(i + 1)\n        path.pop()                   # un-choose\n        walk(i + 1)                  # skip xs[i]\n',
                                     '        walk(i + 1)\n        path.append(xs[i])\n        walk(i + 1)\n        path.pop()\n')))
dm(R, 1, 'stores path itself', mut(R, ('out.append(path[:])      # a copy: path keeps changing', 'out.append(path)')))
dm(R, 2, 'empty input gives no subsets', mut(R, ('    out, path = [], []\n\n    def walk(i):', '    out, path = [], []\n    if not xs:\n        return []\n\n    def walk(i):')))
dm(R, 7, 'empty input gives no orderings', mut(R, ('    used = [False] * len(xs)\n', '    used = [False] * len(xs)\n    if not xs:\n        return []\n')))
R = 'l11-dead-ends#screens[8]'
dm(R, 2, 'no undo after the call', mut(R, ('            cols.remove(c); diag.remove(row - c); anti.remove(row + c)\n', '')))
dm(R, 9, 'end of list checked before the target', mut(R, ('        if total == target:\n            return True\n        if i == len(xs) or total + xs[i] > target:',
                                                       '        if i == len(xs):\n            return False\n        if total == target:\n            return True\n        if total + xs[i] > target:')))
dm(R, 10, 'empty list answered False', mut(R, ('    xs = sorted(xs)\n', '    if not xs:\n        return False\n    xs = sorted(xs)\n')))
dm(R, 13, 'unpruned walk (Pyodide times it, part D note)', mut(R, ('        if i == len(xs) or total + xs[i] > target:', '        if i == len(xs):')))
R = 'l12-remembering#screens[9]'
dm(R, 1, 'base cases not counted', mut(R, ('        computed += 1\n        value = k if k < 2 else f(k - 1) + f(k - 2)', '        if k >= 2:\n            computed += 1\n        value = k if k < 2 else f(k - 1) + f(k - 2)')))
dm(R, 2, 'counter outlives the call', mut(R, ('def fib_memo(n):\n    cache = {}\n    computed = 0\n', 'computed = 0\n\n\ndef fib_memo(n):\n    cache = {}\n'), ('        nonlocal computed', '        global computed')))
dm(R, 3, 'counts cache lookups', mut(R, ('        if k in cache:\n            return cache[k]\n        computed += 1\n', '        computed += 1\n        if k in cache:\n            return cache[k]\n')))
dm(R, 3, 'cache outlives the call', mut(R, ('def fib_memo(n):\n    cache = {}\n', 'cache = {}\n\n\ndef fib_memo(n):\n')))
dm(R, 3, 'cache as a default argument', mut(R, ('def fib_memo(n):\n    cache = {}\n', 'def fib_memo(n, cache={}):\n')))
dm(R, 12, 'grid not memoised', mut(R, ("        if (i, j) not in cache:\n            cache[(i, j)] = paths(i - 1, j) + paths(i, j - 1)\n        return cache[(i, j)]", '        return paths(i - 1, j) + paths(i, j - 1)')))
R = 'l13-climbing-stairs#screens[9]'
dm(R, 1, 'ways(0) taken as 0', mut(R, ('    prev, cur = 1, 1                 # ways(0), ways(1)\n    for _ in range(2, n + 1):', '    if n == 0:\n        return 0\n    prev, cur = 1, 1\n    for _ in range(2, n + 1):')))
dm(R, 5, 'plain recursion runs out of time', mut(R, ('    return cur\n', '    return cur\n\n\ndef stairs(n):\n    return 1 if n < 2 else stairs(n - 1) + stairs(n - 2)\n')))
dm(R, 6, 'memoised recursion', mut(R, ('    return cur\n', '    return cur\n\n\n_m = {}\ndef stairs(n):\n    if n < 2:\n        return 1\n    if n not in _m:\n        _m[n] = stairs(n - 1) + stairs(n - 2)\n    return _m[n]\n')))
dm(R, 7, 'largest coin first', mut(R, ('def min_coins(coins, amount):\n', 'def min_coins(coins, amount):\n    n = 0\n    for c in sorted(coins, reverse=True):\n        n += amount // c; amount %= c\n    return n if amount == 0 else -1\n\n\ndef _unused(coins, amount):\n')))
dm(R, 8, 'amount 0 answered -1', mut(R, ('    INF = float(\'inf\')\n', '    INF = float(\'inf\')\n    if amount == 0:\n        return -1\n')))
dm(R, 9, 'infinite entry returned', mut(R, ('    return best[amount] if best[amount] < INF else -1', '    return best[amount]')))
R = 'homework-3#items[0]'
dm(R, 1, 'loop from 0', mut(R, ('for i in range(start, len(cands)):', 'for i in range(0, len(cands)):')))
dm(R, 3, 'not sorted', mut(R, ('cands = sorted(candidates)', 'cands = list(candidates)')))
dm(R, 5, 'target 0 gives no combination', mut(R, ('    out, path = [], []\n', '    out, path = [], []\n    if target == 0:\n        return []\n')))
R = 'homework-3#items[1]'
dm(R, 5, 'empty string answered False', mut(R, ('    words = set(words)\n', '    words = set(words)\n    if not s:\n        return False\n')))
dm(R, 8, 'no memo', mut(R, ('    @lru_cache(maxsize=None)\n', '')))
R = 'homework-3#items[8]'
dm(R, 2, 'one round trip only', '''
def trade_with_fee(prices, fee):
    best, lo = 0, float('inf')
    for p in prices:
        lo = min(lo, p); best = max(best, p - lo - fee)
    return best
''')
dm(R, 3, 'each rising run traded on its own', '''
def trade_with_fee(prices, fee):
    total, i = 0, 0
    while i < len(prices):
        j = i
        while j + 1 < len(prices) and prices[j + 1] > prices[j]:
            j += 1
        total += max(0, prices[j] - prices[i] - fee)
        i = j + 1
    return total
''')
dm(R, 4, 'table starts on day 1', mut(R, ('    for p in prices:                # bottom up: day 0 first', '    for p in prices[1:]:')))
dm(R, 5, 'table stops before the last day', mut(R, ('    for p in prices:                # bottom up: day 0 first', '    for p in prices[:-1]:')))
dm(R, 7, 'reads prices[0] for the start', mut(R, ("    flat, long = 0, float('-inf')   # before day 0: no share, none to sell", '    flat, long = 0, -prices[0]')))

# Lines that name no cause: the facts each states about its test, checked against the test and the solution.
DESC = {
    ('l1-nodes-and-edges#screens[8]', 5): lambda: expect('l1-nodes-and-edges#screens[8]', 5) == '[]',
    ('l1-nodes-and-edges#screens[5]', 2): lambda: True,
    ('l2-level-by-level#screens[4]', 3): lambda: expect('l2-level-by-level#screens[4]', 3) == "['A', 'B', 'C', 'D']",
    ('l2-level-by-level#screens[4]', 4): lambda: expect('l2-level-by-level#screens[4]', 4) == "['X']",
    ('l2-level-by-level#screens[8]', 3): lambda: expect('l2-level-by-level#screens[8]', 3) == '[]',
    ('l2-level-by-level#screens[8]', 7): lambda: expect('l2-level-by-level#screens[8]', 7) == "['B', 'C']",
    ('l3-going-deep#screens[2]', 3): lambda: expect('l3-going-deep#screens[2]', 3) == "['A']",
    ('l3-going-deep#screens[2]', 4): lambda: expect('l3-going-deep#screens[2]', 4) == "['A', 'B', 'C']",
    ('l3-going-deep#screens[5]', 3): lambda: expect('l3-going-deep#screens[5]', 3) == "['A', 'B', 'D', 'C']",
    ('l3-going-deep#screens[8]', 3): lambda: expect('l3-going-deep#screens[8]', 3) == '0',
    ('l3-going-deep#screens[9]', 3): lambda: expect('l3-going-deep#screens[9]', 3) == 'True',
    ('l4-islands#screens[4]', 5): lambda: expect('l4-islands#screens[4]', 5) == '2',
    ('l4-islands#screens[4]', 11): lambda: expect('l4-islands#screens[4]', 11) == '1',
    ('l4-islands#screens[8]', 1): lambda: expect('l4-islands#screens[8]', 1) == '2',
    ('l4-islands#screens[8]', 2): lambda: expect('l4-islands#screens[8]', 2) == '1',
    ('l5-tasks-in-order#screens[8]', 2): lambda: expect('l5-tasks-in-order#screens[8]', 2) == "['report']",
    ('l5-tasks-in-order#screens[8]', 4): lambda: expect('l5-tasks-in-order#screens[8]', 4) == 'None',
    ('homework-1#items[0]', 3): lambda: expect('homework-1#items[0]', 3) == '0',
    ('homework-1#items[0]', 4): lambda: expect('homework-1#items[0]', 4) == '-1',
    ('homework-1#items[0]', 6): lambda: expect('homework-1#items[0]', 6) == '-1',
    ('homework-1#items[1]', 8): lambda: expect('homework-1#items[1]', 8) == '999',
    ('homework-1#items[2]', 3): lambda: expect('homework-1#items[2]', 3) == '0',
    ('homework-1#items[2]', 4): lambda: expect('homework-1#items[2]', 4) == 'None',
    ('l6-fewest-steps#screens[8]', 3): lambda: expect('l6-fewest-steps#screens[8]', 3) == '3',
    ('l7-dijkstra#screens[4]', 2): lambda: True,
    ('l9-arbitrage-cycle#screens[4]', 6): lambda: expect('l9-arbitrage-cycle#screens[4]', 6) == '[0, 1]',
    ('homework-2#items[1]', 7): lambda: expect('homework-2#items[1]', 7) == '-1',
    ('homework-2#items[2]', 4): lambda: expect('homework-2#items[2]', 4) == '1',
    ('homework-2#items[8]', 4): lambda: expect('homework-2#items[8]', 4) == '(2, 1)',
    ('l10-every-subset#screens[9]', 5): lambda: expect('l10-every-subset#screens[9]', 5) == '8',
    ('l11-dead-ends#screens[8]', 5): lambda: expect('l11-dead-ends#screens[8]', 5) == '[0, 0]',
    ('l12-remembering#screens[9]', 4): lambda: expect('l12-remembering#screens[9]', 4) == '(832040, 31)',
    ('l12-remembering#screens[9]', 6): lambda: expect('l12-remembering#screens[9]', 6) == '(55, 11)',
    ('homework-3#items[1]', 2): lambda: expect('homework-3#items[1]', 2) == 'False',
    ('homework-3#items[8]', 6): lambda: expect('homework-3#items[8]', 6) == '0',
}

for name, (ref, n, code) in D.items():
    w = widget(ref)
    first, fails = run_tests(w, code, stop='(should pass)' not in name)
    if '(Pyodide' in name:
        print(f'info {name}: first failing test in CPython {first}; Pyodide timing in the fix pass')
    elif '(should pass)' in name:
        check('D control passes every test: ' + name, first is None, fails)
    else:
        check('D first failing test is N: ' + name, first == n, f'first failing test is {first}' if first else 'passes every test')

# every test-N line is either swept by a submission or listed as a description
swept = {(ref, n) for ref, n, _ in D.values()} | set(DESC)
for ref, w in code_widgets():
    for key in fb_lines(ref):
        if key.startswith('test-'):
            n = int(key[5:])
            check(f'D line {ref} {key} is swept', (ref, n) in swept)
            if (ref, n) in DESC:
                check(f'D facts of descriptive line {ref} {key}', DESC[(ref, n)]())


# ---------------------------------------------------------------- part E: fix-pass slip sweep
# Every numeric wrong[] value with a feedback line in levels 1 to 3: the value the line's named mistake gives,
# computed here from the item's data, must equal the slip value in the content.
from itertools import permutations as _perms


def slip_value(ref, sid):
    f, p = ref.split('#')
    key, i = p[:-1].split('[')
    return next(w['value'] for w in load(f)[key][int(i)]['widget']['wrong'] if w['id'] == sid)


def _islands(grid, diag=False):
    cells = {(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v}
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)] + ([(-1, -1), (-1, 1), (1, -1), (1, 1)] if diag else [])
    seen, n = set(), 0
    for s in cells:
        if s in seen:
            continue
        n += 1
        stack = [s]; seen.add(s)
        while stack:
            r, c = stack.pop()
            for dr, dc in steps:
                q = (r + dr, c + dc)
                if q in cells and q not in seen:
                    seen.add(q); stack.append(q)
    return n


def _kahn_count(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    ready = [u for u in adj if indeg[u] == 0]; n = 0
    while ready:
        u = ready.pop(); n += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return n


def _ordered(t, parts):
    return 1 if t == 0 else sum(_ordered(t - x, parts) for x in parts if x <= t)


def _fib_calls(n):
    return 1 if n < 2 else 1 + _fib_calls(n - 1) + _fib_calls(n - 2)


def _lazy_dijkstra_stale(adj, s):
    dist = {u: math.inf for u in adj}; dist[s] = 0; heap = [(0, s)]; stale = 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1; continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist, stale


R2 = {'S': [('A', 2), ('B', 6)], 'A': [('B', 3), ('C', 7)], 'B': [('C', 1), ('T', 8)], 'C': [('T', 2)], 'T': []}
r2dist, r2stale = _lazy_dijkstra_stale(R2, 'S')
loop9 = 1.0850 / (0.8543 * 1.2700)            # GBP to EUR to USD to GBP, l9 screens[8]
loop_hw2 = 1.2650 * 0.9230 * 0.8580            # homework-2 items[5]
X = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
RING = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
legs = list(_perms('ABCD'))

SLIPS = {
    ('l1-nodes-and-edges#screens[3]', 'edges'): 6, ('l1-nodes-and-edges#screens[3]', 'cells'): 6 * 6,
    ('l1-nodes-and-edges#quiz[0]', 'once'): 14 // 2, ('l1-nodes-and-edges#quiz[0]', 'sq'): 7 ** 2,
    ('l1-nodes-and-edges#quiz[2]', 'list'): 1000 + 2 * 3000, ('l1-nodes-and-edges#quiz[2]', 'edges2'): 2 * 3000,
    ('l2-level-by-level#quiz[1]', 'centre'): 6 + 1, ('l2-level-by-level#quiz[1]', 'one'): 1,
    ('l3-going-deep#quiz[1]', 'edges'): 2, ('l3-going-deep#quiz[1]', 'nodes'): 6,      # {1, 2} and {4, 5}; six nodes
    ('l3-going-deep#quiz[2]', 'edges'): 10 - 1,
    ('l4-islands#screens[1]', 'diag'): islands(G4, True), ('l4-islands#screens[1]', 'cells'): sum(map(sum, G4)),
    ('l4-islands#screens[3]', 'cells'): 1000 * 1000, ('l4-islands#screens[3]', 'pairs'): (1000 * 1000) ** 2,
    ('l4-islands#quiz[1]', 'diag'): _islands(X, True),
    ('l4-islands#quiz[3]', 'cells'): sum([1, 1, 0, 1, 0, 0, 1, 1, 1]),
    ('l5-tasks-in-order#screens[6]', 'all'): 7, ('l5-tasks-in-order#screens[6]', 'none'): 0,
    ('l5-tasks-in-order#screens[6]', 'five'): _kahn_count({'prices': ['returns'], 'calendar': ['returns'], 'returns': ['signals', 'risk'], 'signals': ['backtest'],
                                                           'risk': ['backtest'], 'backtest': ['report', 'risk'], 'report': []}) + 1,   # the four, plus risk
    ('l5-tasks-in-order#quiz[0]', 'one'): 1, ('l5-tasks-in-order#quiz[0]', 'four'): 4,
    ('l5-tasks-in-order#quiz[3]', 'all'): 4, ('l5-tasks-in-order#quiz[3]', 'out'): 1,
    ('review-1#items[0]', 'once'): 15, ('review-1#items[0]', 'plus'): 10 + 15, ('review-1#items[0]', 'sq'): 10 ** 2,
    ('review-1#items[3]', 'diag'): islands(GR, True), ('review-1#items[3]', 'cells'): sum(map(sum, GR)),
    ('review-1#items[6]', 'all'): 7,
    ('review-1#items[6]', 'four'): _kahn_count({'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': ['e'], 'e': ['f'], 'f': ['d', 'g'], 'g': []}) + 1,   # the three, plus d
    ('homework-1#items[4]', 'nobytes'): 20_000 ** 2 / 1e9, ('homework-1#items[4]', 'linear'): 20_000 * 8 / 1e9,
    ('homework-1#items[5]', 'inside'): _islands(RING) - 1, ('homework-1#items[5]', 'sides'): 4,
    ('l6-fewest-steps#screens[7]', 'hops'): 3, ('l6-fewest-steps#screens[7]', 'nodes'): 4,
    ('l6-fewest-steps#quiz[3]', 'cells'): 6 + 1,
    ('l7-dijkstra#screens[5]', 'right'): 3,
    ('l7-dijkstra#screens[6]', 'pop'): 2,
    ('l7-dijkstra#screens[8]', 'direct'): round(1e6 * 4.0e-4), ('l7-dijkstra#screens[8]', 'usd'): round(1e6 * (1.2 + 1.5) * 1e-4),
    ('l7-dijkstra#screens[8]', 'eurjpy'): round(1e6 * (0.5 + 2.4) * 1e-4),
    ('l7-dijkstra#quiz[0]', 'right'): 1 + 2,
    ('l7-dijkstra#quiz[3]', 'nodes'): 6,
    ('l8-groups#screens[2]', 'one'): 6, ('l8-groups#screens[2]', 'self'): 7,
    ('l8-groups#screens[7]', 'edges'): 2,                 # {0, 1, 2, 3} and {5, 6}
    ('l8-groups#quiz[0]', 'pairs'): 2,                    # {1, 2, 5} and {3, 4}
    ('l8-groups#quiz[2]', 'direct'): 3,
    ('l9-arbitrage-cycle#screens[1]', 'now'): 0.86,
    ('l9-arbitrage-cycle#screens[2]', 'sign'): round(math.log(1.27 * 0.92 * 0.86), 6), ('l9-arbitrage-cycle#screens[2]', 'sum'): round(1.27 + 0.92 + 0.86, 2),
    ('l9-arbitrage-cycle#screens[2]', 'prod'): round(1.27 * 0.92 * 0.86, 6),
    ('l9-arbitrage-cycle#screens[8]', 'gross'): round(1e6 * (loop9 - 1), 2), ('l9-arbitrage-cycle#screens[8]', 'sign'): round(-1e6 * (loop9 * (1 - 1e-4) ** 3 - 1), 2),
    ('l9-arbitrage-cycle#quiz[0]', 'nodet'): 7 * 40, ('l9-arbitrage-cycle#quiz[0]', 'v'): 9 * 40,
    ('l9-arbitrage-cycle#quiz[2]', 'inv'): round(1.25 / 1.05, 4),
    ('review-2#items[1]', 'sb'): 6 + 8, ('review-2#items[1]', 'sat'): 2 + 7 + 2,
    ('review-2#items[3]', 'sum'): round(191.20 + 0.006135 + 0.8530, 6),
    ('review-2#items[4]', 'none'): 0,
    ('review-2#items[5]', 'cycle'): 1 + 2 + 3 + 4, ('review-2#items[5]', 'all-small'): 1 + 2 + 3 + 4 + 5,
    ('review-2#items[6]', 'one'): 1, ('review-2#items[6]', 'v'): 6,
    ('homework-2#items[4]', 'sg'): round(4.2 + 77.0 + 34.0, 1), ('homework-2#items[4]', 'direct-sg'): round(84.0 + 34.0, 1),
    ('homework-2#items[5]', 'gross'): round(1e6 * (loop_hw2 - 1), 2), ('homework-2#items[5]', 'onecost'): round(1e6 * (loop_hw2 * (1 - 2e-4) - 1), 2),
    ('l10-every-subset#screens[0]', 'no-empty'): 2 ** 3 - 1, ('l10-every-subset#screens[0]', 'orders'): factorial(3), ('l10-every-subset#screens[0]', 'one-each'): 3,
    ('l10-every-subset#screens[3]', 'square'): 10 ** 2, ('l10-every-subset#screens[3]', 'double'): 2 * 10, ('l10-every-subset#screens[3]', 'factorial'): factorial(10),
    ('l10-every-subset#screens[10]', 'no-cash'): comb(6, 1) + comb(6, 2) + comb(6, 3), ('l10-every-subset#screens[10]', 'exactly-3'): comb(6, 3),
    ('l10-every-subset#screens[10]', 'all'): 2 ** 6, ('l10-every-subset#screens[10]', 'ordered'): 6 * 5 * 4,
    ('l10-every-subset#screens[11]', 'hours'): round(2 ** 30 / 1000 / 3600), ('l10-every-subset#screens[11]', 'seconds'): round(2 ** 30 / 1000),
    ('l10-every-subset#quiz[1]', 'zero'): 0,
    ('l10-every-subset#quiz[2]', 'pow'): 2 ** 4, ('l10-every-subset#quiz[2]', 'sum'): 4 + 3 + 2 + 1,
    ('l10-every-subset#quiz[3]', 'leaves'): 2 ** 3, ('l10-every-subset#quiz[3]', 'inner'): 1 + 2 + 4,
    ('l11-dead-ends#screens[2]', 'one'): 1, ('l11-dead-ends#screens[2]', 'rows'): 4, ('l11-dead-ends#screens[2]', 'orders'): factorial(4),
    ('l11-dead-ends#screens[5]', 'orders'): _ordered(8, (2, 3, 5)),
    ('l11-dead-ends#screens[5]', 'no-reuse'): sum(1 for k in range(1, 4) for c in itertools.combinations([2, 3, 5], k) if sum(c) == 8),
    ('l11-dead-ends#quiz[0]', 'orders'): factorial(3), ('l11-dead-ends#quiz[0]', 'one'): 1,
    ('l11-dead-ends#quiz[0]', 'two'): sum(all(abs(p[i] - p[j]) != j - i for i in range(4) for j in range(i + 1, 4)) for p in _perms(range(4))),   # the 4 by 4 count
    ('l11-dead-ends#quiz[1]', 'perm'): factorial(8), ('l11-dead-ends#quiz[1]', 'total'): sum(8 ** k for k in range(9)),
    ('l11-dead-ends#quiz[3]', 'orders'): 3 + 1, ('l11-dead-ends#quiz[3]', 'one'): 1,
    ('l12-remembering#screens[1]', 'no-one'): _fib_calls(5) + _fib_calls(4), ('l12-remembering#screens[1]', 'double'): 2 * _fib_calls(5),
    ('l12-remembering#screens[4]', 'no-zero'): 30, ('l12-remembering#screens[4]', 'lookups'): 2 * 30 - 1, ('l12-remembering#screens[4]', 'naive'): 2 * 1346269 - 1,   # 2 fib(31) - 1
    ('l12-remembering#screens[5]', 'row'): 3 + 3, ('l12-remembering#screens[5]', 'both'): 6 + 6,
    ('l12-remembering#screens[8]', 'fresh'): 7, ('l12-remembering#screens[8]', 'none'): 0,
    ('l12-remembering#screens[10]', 'paths'): 2 ** 30, ('l12-remembering#screens[10]', 'square'): 31 * 31, ('l12-remembering#screens[10]', 'last'): 31,
    ('l12-remembering#quiz[0]', 'all'): 200 * 25,
    ('l12-remembering#quiz[2]', 'no-one'): _fib_calls(7) - 1,
    ('l13-climbing-stairs#screens[0]', 'pow3'): 2 ** 3, ('l13-climbing-stairs#screens[0]', 'pow4'): 2 ** 4, ('l13-climbing-stairs#screens[0]', 'three'): 3,   # 1111, 112, 22
    ('l13-climbing-stairs#screens[4]', 'right'): 5, ('l13-climbing-stairs#screens[4]', 'two'): 2,       # ways from 0, 1: 0, 1, 1, 2, 3; the entry one short of i = 4 is 2
    ('l13-climbing-stairs#screens[6]', 'right'): 2, ('l13-climbing-stairs#screens[6]', 'one'): 1,
    ('l13-climbing-stairs#screens[10]', 'one-side'): comb(5, 2), ('l13-climbing-stairs#screens[10]', 'all'): 2 ** 6,
    ('l13-climbing-stairs#screens[11]', 'greedy'): 3,     # 900 + 100 + 100
    ('l13-climbing-stairs#quiz[1]', 'greedy'): -1,
    ('l13-climbing-stairs#quiz[2]', 'two-steps'): 8,
    ('review-3#items[0]', 'no-empty'): 15, ('review-3#items[0]', 'orders'): factorial(4),
    ('review-3#items[2]', 'col-only'): 3,
    ('review-3#items[4]', 'no-one'): _fib_calls(8) - 1, ('review-3#items[4]', 'memo'): 9,
    ('review-3#items[6]', 'two'): 13 + 7,
    ('review-3#items[7]', 'greedy'): 3,                   # 9 + 1 + 1
    ('homework-3#items[3]', 'all'): 24, ('homework-3#items[3]', 'fixed'): sum(1 for p in legs if p[0] == 'A'),
    ('homework-3#items[4]', 'subsets'): 2 ** 20, ('homework-3#items[4]', 'no-ends'): 20 * 100, ('homework-3#items[4]', 'one-off'): 21 * 100,
    ('homework-3#items[5]', 'all'): 2 ** 10, ('homework-3#items[5]', 'half'): 2 ** 10 // 2,
}
check('E review-2 items[4] stale count is the key', r2stale == 3 and r2dist['T'] == 8)
check('E l12 fib calls 15, 9, 25, 41, 67', [_fib_calls(k) for k in (5, 4, 6, 7, 8)] == [15, 9, 25, 41, 67])
check('E l13 stairs(4) with ways(0) = 0', (lambda w: [w.append(w[-1] + w[-2]) for _ in range(3)] and w)([0, 1]) == [0, 1, 1, 2, 3])
for (ref, sid), v in SLIPS.items():
    got = slip_value(ref, sid)
    check(f'E slip {ref} {sid}: the named mistake gives the slip value', math.isclose(got, v, rel_tol=0, abs_tol=1e-9) or got == v, f'mistake gives {v}, slip value {got}')
# every numeric wrong[] value that has a feedback line is in SLIPS
for f in LEVELS:
    d = load(f)
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(d.get(key, [])):
            w = s.get('widget') or {}
            fbk = (s.get('feedback') or {}).get('byKey', {})
            if w.get('kind') == 'numeric':
                for x in w.get('wrong', []):
                    if x['id'] in fbk:
                        check(f'E slip listed: {f}#{key}[{i}] {x["id"]}', (f'{f}#{key}[{i}]', x['id']) in SLIPS)


print(f'{N[0]} checks, {len(FAILS)} failed')
if FAILS:
    print('Each failed check is a finding in docs/reviews/audit-graphs-dp-1-3-r2.md')
sys.exit(1 if FAILS else 0)
