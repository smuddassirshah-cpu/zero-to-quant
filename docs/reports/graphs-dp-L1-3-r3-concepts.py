#!/usr/bin/env python3
"""Concept audit, round 3 (blind): graphs-dp levels 1 to 3.

Three parts, all run on the content's own code and graphs:
  A. every code widget: solution passes its tests, starter fails;
  B. every `test-N` feedback line that names a mistake: a mutant with that mistake
     must pass tests 1..N-1 and fail test N;
  C. worked examples and stated numbers, recomputed.
CPython 3.12 here; the page runs Pyodide 0.27.7 (CPython 3.12.7 on WebAssembly) with
sys.setrecursionlimit(3000), which this script also sets. Exit 0 when every check holds.
Run from the repository root:  python3 docs/reports/graphs-dp-L1-3-r3-concepts.py
"""
import heapq, itertools, json, math, os, random, signal, sys, io, contextlib
from collections import deque

sys.setrecursionlimit(3000)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'graphs-dp')
FAIL = []
N = [0]


def ck(label, cond, detail=''):
    N[0] += 1
    if not cond:
        FAIL.append(label + (' :: ' + str(detail) if detail != '' else ''))


def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


FILES = ['l1-nodes-and-edges', 'l2-level-by-level', 'l3-going-deep', 'l4-islands', 'l5-tasks-in-order',
         'l6-fewest-steps', 'l7-dijkstra', 'l8-groups', 'l9-arbitrage-cycle', 'l10-every-subset',
         'l11-dead-ends', 'l12-remembering', 'l13-climbing-stairs', 'review-1', 'review-2', 'review-3',
         'homework-1', 'homework-2', 'homework-3']
DOC = {f: load(f) for f in FILES}


def items_of(doc):
    return (doc.get('screens') or []) + (doc.get('quiz') or []) + (doc.get('items') or [])


def widget(fname, key, idx):
    return DOC[fname][key][idx]['widget']


class TimeUp(Exception):
    pass


def _alarm(sig, frm):
    raise TimeUp()


signal.signal(signal.SIGALRM, _alarm)


def run(w, code, limit=5):
    """Run code against the widget's tests the way code.js does: prelude, code, postlude in one
    namespace; per test: setup, then call compared with expect. Returns a list of (ok, got)."""
    ns = {'__name__': 'zq'}
    out = []
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(w.get('prelude', ''), ns)
            exec(code, ns)
            exec(w.get('postlude', ''), ns)
    except BaseException as e:  # noqa
        return [(False, 'load: ' + repr(e))] * len(w['tests'])
    for t in w['tests']:
        signal.alarm(limit)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if t.get('setup'):
                    exec(t['setup'], ns)
                got = eval(t['call'], ns)
                exp = eval(t['expect'], ns)
            ok = got == exp
        except BaseException as e:  # noqa
            ok, got = False, type(e).__name__
        finally:
            signal.alarm(0)
        out.append((ok, got))
    return out


def first_fail(res):
    for i, (ok, _) in enumerate(res):
        if not ok:
            return i + 1
    return None


# ---------------------------------------------------------------- A. widgets
n_widgets = 0
for f in FILES:
    for i, it in enumerate(items_of(DOC[f])):
        w = it.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        n_widgets += 1
        res = run(w, w['solution'])
        ck(f'{f} item {i}: solution passes', first_fail(res) is None, first_fail(res))
        res = run(w, w['starter'])
        ck(f'{f} item {i}: starter fails', first_fail(res) is not None)
ck('code widget count', n_widgets == 38, n_widgets)


# ---------------------------------------------------------------- B. mutants
def mutant(label, w, code, n, got=None, limit=5):
    res = run(w, code, limit)
    ff = first_fail(res)
    ck(f'mutant {label}: first failing test {n}', ff == n, f'first fail {ff}, got {res[ff - 1][1] if ff else None}')
    if got is not None and ff == n:
        ck(f'mutant {label}: output', got(res[n - 1][1]), res[n - 1][1])


L = lambda f, i: widget(f, 'screens', i)
H = lambda f, i: widget(f, 'items', i)

# l1
w = L('l1-nodes-and-edges', 5)
mutant('l1 one-way append', w, '''def adj_list(nodes, edges):
    adj = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v)
    for v in adj: adj[v].sort()
    return adj''', 1)
mutant('l1 dict from edges', w, '''def adj_list(nodes, edges):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        if u != v: adj.setdefault(v, []).append(u)
    for v in adj: adj[v].sort()
    return adj''', 2)
mutant('l1 self-loop twice', w, '''def adj_list(nodes, edges):
    adj = {v: [] for v in nodes}
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for v in adj: adj[v].sort()
    return adj''', 3)
mutant('l1 shared rows', L('l1-nodes-and-edges', 8), '''def adj_matrix(n, edges):
    m = [[0] * n] * n
    for u, v in edges:
        m[u][v] = 1; m[v][u] = 1
    return m''', 1, lambda g: all(r == g[0] for r in g))
w = L('l1-nodes-and-edges', 9)
mutant('l1 in-degree only', w, '''def find_ccp(n, posts):
    into = [0] * n
    for a, b in posts: into[b] += 1
    for f in range(n):
        if into[f] == n - 1: return f
    return -1''', 3)
mutant('l1 out-degree only', w, '''def find_ccp(n, posts):
    out = [0] * n
    for a, b in posts: out[a] += 1
    for f in range(n):
        if out[f] == 0: return f
    return -1''', 4)

# l2
w = L('l2-level-by-level', 4)
mutant('l2 mark on pop', w, '''from collections import deque
def bfs(adj, start):
    queue = deque([start]); seen, order = set(), []
    while queue:
        u = queue.popleft(); seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: queue.append(v)
    return order''', 1, lambda g: g.count('G') == 2)
mutant('l2 recursive bfs', w, '''from collections import deque
def bfs(adj, start):
    seen = {start}; order = []; q = deque([start])
    def step():
        if not q: return
        u = q.popleft(); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v); q.append(v)
        step()
    step()
    return order''', 7, lambda g: g == 'RecursionError')
w = L('l2-level-by-level', 8)
mutant('l2 expands at distance k', w, '''from collections import deque
def within_hops(adj, start, k):
    dist = {start: 0}; queue = deque([start])
    while queue:
        u = queue.popleft()
        if dist[u] > k: continue
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; queue.append(v)
    return sorted(f for f in dist if f != start)''', 1, lambda g: 'Hazel' in g)
mutant('l2 late mark in within_hops', w, '''from collections import deque
def within_hops(adj, start, k):
    seen = set(); out = []; q = deque([(start, 0)])
    while q:
        u, d = q.popleft(); seen.add(u)
        if u != start: out.append(u)
        if d == k: continue
        for v in adj[u]:
            if v not in seen: q.append((v, d + 1))
    return sorted(out)''', 5, lambda g: g.count('Oak') == 2)

# l3
w = L('l3-going-deep', 2)
mutant('l3 no seen check', w, '''def dfs(adj, start):
    order = []
    def visit(u):
        order.append(u)
        for v in sorted(adj[u]): visit(v)
    visit(start)
    return order''', 1, lambda g: g == 'RecursionError')
w = L('l3-going-deep', 5)
mutant('l3 sorted pushes', w, '''def dfs_stack(adj, start):
    seen = set(); stack = [start]; order = []
    while stack:
        u = stack.pop()
        if u in seen: continue
        seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: stack.append(v)
    return order''', 1, lambda g: g[:3] == ['A', 'D', 'F'])
mutant('l3 no skip on pop', w, '''def dfs_stack(adj, start):
    seen = set(); stack = [start]; order = []
    while stack:
        u = stack.pop()
        seen.add(u); order.append(u)
        for v in sorted(adj[u], reverse=True):
            if v not in seen: stack.append(v)
    return order''', 1, lambda g: g.count('D') == 2)
mutant('l3 recursive helper', w, '''def dfs_stack(adj, start):
    seen = set(); order = []
    def visit(u):
        seen.add(u); order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: visit(v)
    visit(start)
    return order''', 6, lambda g: g == 'RecursionError')
w = L('l3-going-deep', 8)
mutant('l3 counts only nodes with edges', w, '''def count_components(adj):
    seen = set(); count = 0
    for s in adj:
        if s in seen or not adj[s]: continue
        count += 1; seen.add(s); stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); stack.append(v)
    return count''', 2)
mutant('l3 recursive components', w, '''def count_components(adj):
    seen = set()
    def visit(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen: visit(v)
    count = 0
    for s in adj:
        if s not in seen:
            count += 1; visit(s)
    return count''', 7, lambda g: g == 'RecursionError')
w = L('l3-going-deep', 9)
mutant('l3 plain seen set', w, '''def has_cycle(rules):
    seen = set()
    def visit(u):
        seen.add(u)
        for v in rules[u]:
            if v in seen: return True
            if visit(v): return True
        return False
    return any(r not in seen and visit(r) for r in rules)''', 2)
mutant('l3 search from first rule only', w, '''def has_cycle(rules):
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
    return False''', 5)

# l4
mutant('l4 no bounds check', L('l4-islands', 2), '''def neighbours(r, c, rows, cols):
    return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]''', 2)
ISL = '''def count_islands(grid):
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
    return count'''
FOUR = '((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1))'
EIGHT = '[(a + i, b + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j]'
w = L('l4-islands', 4)
mutant('l4 eight neighbours', w, ISL % ('len(grid[0]) if rows else 0', EIGHT), 1, lambda g: g == 4)
mutant('l4 unguarded len(grid[0])', w, ISL % ('len(grid[0])', FOUR), 2, lambda g: g == 'IndexError')
mutant('l4 sinking', w, '''def count_islands(grid):
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
    return count''', 10)
w = L('l4-islands', 8)
mutant('l4 columns from len(pnl)', w, w['solution'].replace('cols = len(pnl[0]) if rows else 0', 'cols = rows'), 6, lambda g: g == 0)

# l5
w = L('l5-tasks-in-order', 3)
mutant('l5 plain queue', w, '''from collections import deque
def topo_sort(adj):
    indeg = {u: 0 for u in adj}
    for u in adj:
        for v in adj[u]: indeg[v] += 1
    ready = deque(u for u in adj if indeg[u] == 0); order = []
    while ready:
        u = ready.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: ready.append(v)
    return order if len(order) == len(adj) else None''', 1,
       lambda g: g.index('risk') > g.index('signals'))
mutant('l5 no length check', w, w['solution'].replace('return order if len(order) == len(adj) else None', 'return order'), 3, lambda g: g == [])
w = L('l5-tasks-in-order', 8)
mutant('l5 raw inputs left out', w, '''import heapq
def run_order(deps):
    after = {j: [] for j in deps}; indeg = {j: 0 for j in deps}
    for job, pre in deps.items():
        for p in pre:
            if p in after:
                after[p].append(job); indeg[job] += 1
    ready = [j for j in deps if indeg[j] == 0]; heapq.heapify(ready); order = []
    while ready:
        u = heapq.heappop(ready); order.append(u)
        for v in after[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(ready, v)
    return order if len(order) == len(deps) else None''', 1)

# l6
w = L('l6-fewest-steps', 4)
SP = w['solution']
mutant('l6 stack instead of queue', w, SP.replace('queue.popleft()', 'queue.pop()'), 1, lambda g: len(g) > 4)
mutant('l6 walk not reversed', w, SP.replace('return path[::-1]', 'return path'), 1, lambda g: g == ['H', 'F', 'E', 'A'])
mutant('l6 no t-in-parent check', w, SP.replace('    if t not in parent:\n        return None\n', ''), 5, lambda g: g == 'KeyError')
w = L('l6-fewest-steps', 8)
FC = w['solution']
mutant('l6 pairs one way', w, FC.replace('        adj.setdefault(b, []).append(a)\n', ''), 1, lambda g: g == -1)
mutant('l6 adj[u] not get', w, FC.replace('adj.get(u, [])', 'adj[u]'), 7, lambda g: g == 'KeyError')

# l7
w = L('l7-dijkstra', 4)
DJ = w['solution']
mutant('l7 seen on first push', w, '''import heapq, math
def dijkstra(adj, s):
    dist = {u: math.inf for u in adj}; dist[s] = 0; seen = {s}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        for v, w in adj[u]:
            if v not in seen:
                seen.add(v); dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist''', 1, lambda g: g['B'] == 4)
mutant('l7 record on pop, no check', w, '''import heapq
def dijkstra(adj, s):
    dist = {}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        dist[u] = d
        for v, w in adj[u]: heapq.heappush(heap, (d + w, v))
    return dist''', 1, lambda g: g['B'] == 4 and g['D'] == 6 and g['F'] == 9 and 'G' not in g)
mutant('l7 unreachable left out', w, '''import heapq, math
def dijkstra(adj, s):
    dist = {s: 0}; heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if d + w < dist.get(v, math.inf):
                dist[v] = d + w; heapq.heappush(heap, (d + w, v))
    return dist''', 1, lambda g: 'G' not in g and g['B'] == 3)
mutant('l7 no stale check', w, DJ.replace('        if d > dist[u]:\n            continue\n', ''), 9, lambda g: g == (300, 300))
w = L('l7-dijkstra', 9)
mutant('l7 ignores unreachable centres', w, w['solution'].replace('worst = max(dist.values())', 'worst = max(d for d in dist.values() if d < math.inf)'), 4, lambda g: g == 0)

# l8
w = L('l8-groups', 5)
DSU = w['solution']
mutant('l8 decrement before comparing roots', w, DSU.replace('        if ra == rb:\n            return False\n', '        if ra == rb:\n            self.groups -= 1\n            return False\n'), 5, lambda g: g == (False, 2))
mutant('l8 re-points the node', w, DSU.replace('''        if self.size[ra] < self.size[rb]:   # union by size
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]''', '        self.parent[a] = rb'), 7)
NAIVE = '''class DSU:
    def __init__(self, n):
        self.parent = list(range(n)); self.groups = n
    def find(self, x):
%s
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        self.parent[ra] = rb; self.groups -= 1
        return True
    def count(self):
        return self.groups'''
mutant('l8 recursive find on a chain', w, NAIVE % '        return x if self.parent[x] == x else self.find(self.parent[x])', 9, lambda g: g == 'RecursionError')
mutant('l8 iterative find, no compression, no size', w, NAIVE % '        while self.parent[x] != x: x = self.parent[x]\n        return x', 9,
       lambda g: g == 'TimeUp' or g == (True, 1, False), limit=20)
w = L('l8-groups', 9)
CL = w['solution']
mutant('l8 rho not abs(rho)', w, CL.replace('abs(rho) > threshold', 'rho > threshold'), 1, lambda g: ['GILT'] in g)
mutant('l8 >= threshold', w, CL.replace('abs(rho) > threshold', 'abs(rho) >= threshold'), 3)
mutant('l8 gather by parent', w, CL.replace('d.find(index[name])', 'd.parent[index[name]]'), 7)

# l9
w = L('l9-arbitrage-cycle', 4)
mutant('l9 n-2 passes, no detection', w, '''import math
def bellman_ford(edges, n, s):
    dist = [math.inf] * n; dist[s] = 0
    for _ in range(n - 2):
        for u, v, w in edges:
            if dist[u] + w < dist[v]: dist[v] = dist[u] + w
    return dist''', 1, lambda g: g == [0, 2, 5, math.inf])
mutant('l9 no detection pass', w, '''import math
def bellman_ford(edges, n, s):
    dist = [math.inf] * n; dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]: dist[v] = dist[u] + w
    return dist''', 3)
w = L('l9-arbitrage-cycle', 9)
HA = w['solution']
mutant('l9 weights -rate', w, HA.replace('-math.log(r)', '-r'), 2, lambda g: g is True)
mutant('l9 no tolerance', w, HA.replace('eps=1e-9', 'eps=0.0'), 4, lambda g: g is True)
mutant('l9 no start node', w, HA.replace('bellman_ford(edges, n + 1, n, eps=1e-9)', 'bellman_ford(edges, max(n, 1), 0, eps=1e-9)').replace('    edges += [(n, i, 0.0) for i in range(n)]   # a start joined to every currency\n', ''), 9, lambda g: g is False)

# l10
w = L('l10-every-subset', 9)
SS = w['solution']
mutant('l10 skip before take', w, SS.replace('''        path.append(xs[i])           # choose: take xs[i]
        walk(i + 1)
        path.pop()                   # un-choose
        walk(i + 1)                  # skip xs[i]''', '''        walk(i + 1)
        path.append(xs[i])
        walk(i + 1)
        path.pop()'''), 1, lambda g: g[0] == [])
mutant('l10 stores path itself', w, SS.replace('out.append(path[:])      # a copy: path keeps changing', 'out.append(path)'), 1, lambda g: all(x == [] for x in g))
mutant('l10 empty input returns []', w, SS.replace('def subsets(xs):\n', 'def subsets(xs):\n    if not xs: return []\n'), 2)

# l11
w = L('l11-dead-ends', 8)
QS = w['solution']
mutant('l11 no undo', w, QS.replace('            cols.remove(c); diag.remove(row - c); anti.remove(row + c)\n', ''), 2, lambda g: g == 0)
mutant('l11 end of list checked first', w, QS.replace('''        if total == target:
            return True
        if i == len(xs) or total + xs[i] > target:
            return False                      # sorted: nothing later fits''', '''        if i == len(xs):
            return False
        if total == target:
            return True
        if total + xs[i] > target:
            return False'''), 9)

# l12
w = L('l12-remembering', 9)
FM = w['solution']
mutant('l12 base cases not counted', w, FM.replace('        if k in cache:\n            return cache[k]\n', '        if k < 2:\n            return k\n        if k in cache:\n            return cache[k]\n'), 1, lambda g: g == (0, 0))
mutant('l12 module-level counter', w, FM.replace('def fib_memo(n):\n    cache = {}\n    computed = 0\n', 'computed = 0\ndef fib_memo(n):\n    cache = {}\n').replace('nonlocal computed', 'global computed'), 2, lambda g: g == (1, 2))
mutant('l12 counts lookups', w, FM.replace('        if k in cache:\n            return cache[k]\n        computed += 1\n', '        computed += 1\n        if k in cache:\n            return cache[k]\n'), 3, lambda g: g == (8, 11))
mutant('l12 module-level cache', w, FM.replace('def fib_memo(n):\n    cache = {}\n', 'cache = {}\ndef fib_memo(n):\n'), 3, lambda g: g == (8, 5))

# l13
w = L('l13-climbing-stairs', 9)
ST = w['solution']
MC = ST[ST.index('def min_coins'):]
mutant('l13 ways(0) = 0', w, '''def stairs(n):
    ways = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1): ways[i] = ways[i - 1] + ways[i - 2]
    return ways[n]
''' + MC, 1)
mutant('l13 plain recursion', w, 'def stairs(n):\n    return 1 if n < 2 else stairs(n - 1) + stairs(n - 2)\n' + MC, 5, lambda g: g == 'TimeUp', limit=3)
mutant('l13 memoised recursion', w, 'from functools import lru_cache\n@lru_cache(maxsize=None)\ndef stairs(n):\n    return 1 if n < 2 else stairs(n - 1) + stairs(n - 2)\n' + MC, 6, lambda g: g == 'RecursionError')
mutant('l13 greedy coins', w, ST[:ST.index('def min_coins')] + '''def min_coins(coins, amount):
    n = 0
    for c in sorted(coins, reverse=True):
        n += amount // c; amount %= c
    return n if amount == 0 else -1''', 7, lambda g: g == 3)

# review-1
w = H('review-1', 7)
mutant('review-1 recursive has_path', w, '''def has_path(adj, s, t):
    seen = set()
    def go(u):
        if u == t: return True
        seen.add(u)
        return any(v not in seen and go(v) for v in adj[u])
    return go(s)''', 7, lambda g: g == 'RecursionError')

# homework-1
w = H('homework-1', 1)
mutant('hw1 single source', w, w['solution'].replace('day = {f: 0 for f in defaulted}\n    queue = deque(defaulted)', 'day = {f: 0 for f in defaulted[:1]}\n    queue = deque(defaulted[:1])'), 2, lambda g: g == 5)
w = H('homework-1', 8)
SD = w['solution']
mutant('hw1 conflicts stored one way', w, SD.replace('        adj[b].append(a)\n', ''), 2, lambda g: g is None)
mutant('hw1 no clash check', w, SD.replace('                elif group[v] == group[u]:\n                    return None     # an odd loop: no split works\n', ''), 3)
mutant('hw1 first linked set only', w, SD.replace('    for start in sorted(desks):     # the first desk of each linked set', '    for start in sorted(desks)[:1]:'), 4)
mutant('hw1 desks taken from conflicts', w, SD.replace('adj = {d: [] for d in desks}', 'adj = {}\n    desks = sorted({x for p in conflicts for x in p})\n    adj = {d: [] for d in desks}'), 5)
mutant('hw1 desks in given order', w, SD.replace('sorted(desks)', 'desks'), 6, lambda g: g == {'Rates': 0, 'Credit': 1, 'Swaps': 1})
mutant('hw1 any placed neighbour is a clash', w, '''from collections import deque
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}; par = {}
    for start in sorted(desks):
        if start in group: continue
        group[start] = 0; par[start] = None; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in group:
                    group[v] = 1 - group[u]; par[v] = u; queue.append(v)
                elif v != par[u]:
                    return None
    return group''', 7, lambda g: g is None)
mutant('hw1 one conflict at a time', w, '''def split_desks(desks, conflicts):
    group = {}
    for a, b in conflicts:
        if a not in group and b not in group:
            group[a] = 0; group[b] = 1
        elif a not in group:
            group[a] = 1 - group[b]
        elif b not in group:
            group[b] = 1 - group[a]
        elif group[a] == group[b]:
            return None
    for d in desks:
        group.setdefault(d, 0)
    return group''', 8, lambda g: g is None)
mutant('hw1 recursive colouring', w, '''def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}
    def paint(u, g):
        group[u] = g
        for v in adj[u]:
            if v not in group:
                if not paint(v, 1 - g): return False
            elif group[v] == g:
                return False
        return True
    for s in sorted(desks):
        if s not in group and not paint(s, 0): return None
    return group''', 10, lambda g: g == 'RecursionError')

# homework-2
w = H('homework-2', 1)
CW = w['solution']
mutant('hw2 k rounds', w, CW.replace('range(k + 1)', 'range(k)'), 1, lambda g: g == -1)
mutant('hw2 relax in place', w, CW.replace('new = dict(cost)', 'new = cost'), 1, lambda g: abs(g - 2.6) < 1e-9)
mutant('hw2 cheapest cost keeps one hop count', w, '''import heapq, math
def cheapest_within(quotes, src, dst, k):
    adj = {}
    for a, b, bp in quotes: adj.setdefault(a, []).append((b, bp))
    best = {src: (0, 0)}; heap = [(0, 0, src)]
    while heap:
        d, h, u = heapq.heappop(heap)
        if (d, h) != best.get(u): continue
        if h == k + 1: continue
        for v, bp in adj.get(u, []):
            if d + bp < best.get(v, (math.inf, 0))[0]:
                best[v] = (d + bp, h + 1); heapq.heappush(heap, (d + bp, h + 1, v))
    return best[dst][0] if dst in best else -1''', 2, lambda g: abs(g - 2.9) < 1e-9)
w = H('homework-2', 8)
CC = w['solution']
mutant('hw2 returns when dst first reached', w, CC.replace('''                ways[v] = ways[u]
''', '''                ways[v] = ways[u]
                if v == dst: return nd, ways[v]
'''), 1, lambda g: g == (3, 1))
mutant('hw2 a tie adds 1', w, CC.replace('ways[v] += ways[u]', 'ways[v] += 1'), 2, lambda g: g == (4, 3))
mutant('hw2 a tie pushes again', w, CC.replace('ways[v] += ways[u]  # a tie: every cheapest route to u extends', 'ways[v] += ways[u]\n                heapq.heappush(heap, (nd, v))'), 2)
mutant('hw2 cheaper cost adds the count', w, CC.replace('ways[v] = ways[u]\n', 'ways[v] = ways.get(v, 0) + ways[u]\n'), 3, lambda g: g == (3, 2))
mutant('hw2 stale entry expanded', w, CC.replace('        if d > cost[u]:\n            continue                # a stale entry: u left the heap earlier\n', '        d = cost[u]\n'), 5, lambda g: g == (7, 2))
mutant('hw2 looks dst up', w, '''import heapq, math
def count_cheapest(links, src, dst):
    adj = {}; cost = {src: 0}; ways = {src: 1}
    for a, b, fee in links:
        adj.setdefault(a, []).append((b, fee))
        cost.setdefault(a, math.inf); cost.setdefault(b, math.inf)
        ways.setdefault(a, 0); ways.setdefault(b, 0)
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > cost[u]: continue
        for v, fee in adj.get(u, []):
            nd = d + fee
            if nd < cost[v]:
                cost[v] = nd; ways[v] = ways[u]; heapq.heappush(heap, (nd, v))
            elif nd == cost[v]:
                ways[v] += ways[u]
    return (None, 0) if cost[dst] == math.inf else (cost[dst], ways[dst])''', 8, lambda g: g == 'KeyError')

# homework-3
w = H('homework-3', 0)
CS = w['solution']
mutant('hw3 loop from 0', w, CS.replace('range(start, len(cands))', 'range(0, len(cands))'), 1, lambda g: [2, 3, 2] in g)
mutant('hw3 candidates not sorted', w, CS.replace('sorted(candidates)', 'list(candidates)'), 3)
w = H('homework-3', 8)
mutant('hw3 one round trip', w, '''def trade_with_fee(prices, fee):
    best, low = 0, float('inf')
    for p in prices:
        low = min(low, p); best = max(best, p - low - fee)
    return best''', 2, lambda g: g == 4)
mutant('hw3 each rise on its own', w, '''def trade_with_fee(prices, fee):
    total, i, n = 0, 0, len(prices)
    while i < n:
        j = i
        while j + 1 < n and prices[j + 1] >= prices[j]: j += 1
        total += max(0, prices[j] - prices[i] - fee)
        i = j + 1
    return total''', 3, lambda g: g == 6)
mutant('hw3 first day left out', w, '''def trade_with_fee(prices, fee):
    flat, long = 0, float('-inf')
    for p in prices[1:]:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat''', 4)
mutant('hw3 last day left out', w, '''def trade_with_fee(prices, fee):
    flat, long = 0, float('-inf')
    for p in prices[:-1]:
        flat, long = max(flat, long + p - fee), max(long, flat - p)
    return flat''', 5)


# ---------------------------------------------------------------- C. worked examples
def fn(fname, key, idx, name):
    ns = {}
    w_ = widget(fname, key, idx)
    exec(w_.get('prelude', ''), ns); exec(w_['solution'], ns); exec(w_.get('postlude', ''), ns)
    return ns[name]


def undirected(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    return adj


# l1
E1 = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("E", "F")]
a1 = fn('l1-nodes-and-edges', 'screens', 5, 'adj_list')("ABCDEF", E1)
ck('l1 neighbours of C', a1['C'] == ['A', 'D', 'E'] and a1['F'] == ['E'])
m1 = fn('l1-nodes-and-edges', 'screens', 8, 'adj_matrix')(6, [("ABCDEF".index(a), "ABCDEF".index(b)) for a, b in E1])
ck('l1 matrix canvas', m1 == DOC['l1-nodes-and-edges']['screens'][2]['canvas']['params']['matrices'][0]['rows'])
ck('l1 row C', m1[2] == [1, 0, 0, 1, 1, 0] and [sum(r) for r in m1] == [2, 2, 3, 2, 2, 1] and sum(map(sum, m1)) == 12)
ow = {v: [] for v in "ABCDEF"}
for u, v in E1: ow[u].append(v)
ck('l1 one-way D empty', ow['D'] == [])
ck('l1 fx loop', abs(1.27 * 0.92 * 0.856 - 1.0002) < 1e-3)
ck('l1 sizes', 10**5 * 20 == 2 * 10**6 and 10**5 * 20 // 2 == 10**6 and 8 * 10**10 == 80 * 10**9 and 1 - 6000 / 1e6 == 0.994)

# l2
E2 = [("A", "B"), ("A", "D"), ("B", "E"), ("D", "C"), ("D", "F"), ("E", "G"), ("C", "G"), ("E", "H")]
A2 = undirected(E2)
bfs = fn('l2-level-by-level', 'screens', 4, 'bfs')
ck('l2 bfs order', bfs(A2, 'A') == list('ABDECFGH'))


def levels(adj, s):
    d = {s: 0}; q = deque([s])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in d: d[v] = d[u] + 1; q.append(v)
    return d


d2 = levels(A2, 'A')
ck('l2 days', sorted(k for k in d2 if d2[k] == 1) == ['B', 'D'] and sorted(k for k in d2 if d2[k] == 2) == ['C', 'E', 'F'] and sorted(k for k in d2 if d2[k] == 3) == ['G', 'H'])
# queue states of the demonstrate screen
seen, q, states = {'A'}, deque(['A']), []
while q:
    u = q.popleft()
    for v in sorted(A2[u]):
        if v not in seen: seen.add(v); q.append(v)
    states.append(''.join(q))
ck('l2 queue states', states[:4] == ['BD', 'DE', 'ECF', 'CFGH'], states)
# marking too late
q, seen, order = deque(['A']), set(), []
while q:
    u = q.popleft(); seen.add(u); order.append(u)
    for v in sorted(A2[u]):
        if v not in seen: q.append(v)
ck('l2 late marking', order == list('ABDECFGH') + ['G'])
A2b = undirected([e for e in E2 if e not in (("D", "C"), ("E", "G"))])
ck('l2 unreachable', set(A2b) - set(bfs(A2b, 'A')) == {'C', 'G'})
wh = fn('l2-level-by-level', 'screens', 8, 'within_hops')
cedar = eval(widget('l2-level-by-level', 'screens', 8)['tests'][0]['setup'].split('=', 1)[1])
ck('l2 cedar', levels(cedar, 'Cedar')['Hazel'] == 3 and wh(cedar, 'Cedar', 2) == ['Alder', 'Birch', 'Elm', 'Fir', 'Larch', 'Oak'])

# l3
dfs = fn('l3-going-deep', 'screens', 2, 'dfs')
dfs_stack = fn('l3-going-deep', 'screens', 5, 'dfs_stack')
ck('l3 dfs order', dfs(A2, 'A') == list('ABEGCDFH'))
post, dead, seen = [], [], set()


def visit(u):
    seen.add(u); new = False
    for v in sorted(A2[u]):
        if v not in seen: new = True; visit(v)
    if not new: dead.append(u)
    post.append(u)


visit('A')
ck('l3 post-order', post == list('FDCGHEBA') and dead == ['F', 'H'], (post, dead))
st, seen, order = ['A'], set(), []
while st:
    u = st.pop()
    if u in seen: continue
    seen.add(u); order.append(u)
    for v in sorted(A2[u]):
        if v not in seen: st.append(v)
ck('l3 naive stack order', order == list('ADFCGEHB'), order)
rng = random.Random(3)
same = True
for _ in range(300):
    n = rng.randint(1, 9)
    es = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4]
    g = {i: [] for i in range(n)}
    for a, b in es: g[a].append(b); g[b].append(a)
    same &= dfs(g, 0) == dfs_stack(g, 0)
ck('l3 stack version equals recursive on 300 random graphs', same)
ck('l3 components', fn('l3-going-deep', 'screens', 8, 'count_components')({1: [2], 2: [1], 3: [], 4: [5], 5: [4], 6: []}) == 4)
old = sys.getrecursionlimit()
for lim in (1000, 3000):
    sys.setrecursionlimit(lim)
    chain = {i: [i + 1] for i in range(4999)}; chain[4999] = []
    try:
        dfs(chain, 0); hit = False
    except RecursionError:
        hit = True
    ck(f'l3 5,000 chain raises at limit {lim}', hit)
sys.setrecursionlimit(old)

# l4
G4 = [[1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1]]


def comps(grid, steps, land=lambda v: v == 1):
    R, C = len(grid), len(grid[0]); seen = set(); sizes = []
    for r in range(R):
        for c in range(C):
            if land(grid[r][c]) and (r, c) not in seen:
                seen.add((r, c)); st = [(r, c)]; k = 0
                while st:
                    a, b = st.pop(); k += 1
                    for i, j in steps:
                        x, y = a + i, b + j
                        if 0 <= x < R and 0 <= y < C and land(grid[x][y]) and (x, y) not in seen:
                            seen.add((x, y)); st.append((x, y))
                sizes.append(k)
    return sizes


S4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
S8 = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j]
ck('l4 islands', sorted(comps(G4, S4)) == [1, 1, 3, 3, 3, 3] and len(comps(G4, S8)) == 4 and sum(map(sum, G4)) == 14)
ck('l4 X', len(comps([[1, 0, 1], [0, 1, 0], [1, 0, 1]], S4)) == 5 and len(comps([[1, 0, 1], [0, 1, 0], [1, 0, 1]], S8)) == 1)


def snake_depth(n):
    """max depth of a recursive flood fill trying up, down, left, right on an n by n grid of land"""
    seen = {(0, 0)}; st = [((0, 0), 0)]; best = 1
    while st:
        (a, b), k = st[-1]
        if k == 4:
            st.pop(); continue
        st[-1] = ((a, b), k + 1)
        x, y = a + S4[k][0], b + S4[k][1]
        if 0 <= x < n and 0 <= y < n and (x, y) not in seen:
            seen.add((x, y)); st.append(((x, y), 0)); best = max(best, len(st))
    return best


ck('l4 snake depth', snake_depth(4) == 16 and snake_depth(300) == 90000)
P4 = [[5, -15, -35, -55, -75], [50, 30, 10, -10, -30], [65, 45, 25, 5, -15], [50, 30, 10, -10, -30], [5, -15, -35, -55, -75]]
ck('l4 loss regions', len(comps(P4, S4, lambda v: v < -50)) == 2 and len(comps(P4, S4, lambda v: v < -10)) == 1 and all(r[4] < -10 for r in P4)
   and [(r, c) for r in range(5) for c in range(5) if P4[r][c] < -50] == [(0, 3), (0, 4), (4, 3), (4, 4)])
g = [[1, 1, 0], [0, 0, 1]]
ck('l4 copy is shallow', g.copy()[0] is g[0])

# l5
E5 = [('prices', 'returns'), ('calendar', 'returns'), ('returns', 'signals'), ('returns', 'risk'), ('signals', 'backtest'), ('risk', 'backtest'), ('backtest', 'report')]
T5 = ['prices', 'calendar', 'returns', 'signals', 'risk', 'backtest', 'report']
valid = lambda o, es: all(o.index(a) < o.index(b) for a, b in es)
ck('l5 four orders', sum(valid(p, E5) for p in itertools.permutations(T5)) == 4)
A5 = {t: [] for t in T5}
for a, b in E5: A5[a].append(b)
ck('l5 in-degrees', [sum(b == t for _, b in E5) for t in T5] == [0, 0, 2, 1, 1, 2, 1])


def walk5(adj, pre, starts=None):
    seen, order = set(), []

    def v_(u):
        seen.add(u)
        if pre: order.append(u)
        for v in sorted(adj[u]):
            if v not in seen: v_(v)
        if not pre: order.append(u)
    for u in (starts or sorted(adj)):
        if u not in seen: v_(u)
    return order


ck('l5 pre-order trap', walk5(A5, True) == ['backtest', 'report', 'calendar', 'returns', 'risk', 'signals', 'prices'])
fromcal = walk5(A5, True, ['calendar'] + sorted(A5))
ck('l5 from calendar', fromcal.index('backtest') < fromcal.index('signals'))
po = walk5(A5, False)
ck('l5 post-order', po == ['report', 'backtest', 'risk', 'signals', 'returns', 'calendar', 'prices'] and valid(po[::-1], E5))
A5c = {k: list(v) for k, v in A5.items()}; A5c['backtest'].append('risk')
indeg = {u: 0 for u in A5c}
for u in A5c:
    for v in A5c[u]: indeg[v] += 1
ready = [u for u in A5c if indeg[u] == 0]; heapq.heapify(ready); emitted = []
while ready:
    u = heapq.heappop(ready); emitted.append(u)
    for v in A5c[u]:
        indeg[v] -= 1
        if indeg[v] == 0: heapq.heappush(ready, v)
ck('l5 kahn stalls at 4', emitted == ['calendar', 'prices', 'returns', 'signals'])
okdag = True
for _ in range(200):
    n = rng.randint(1, 8); perm = list(range(n)); rng.shuffle(perm)
    es = [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35]
    adj = {i: [] for i in range(n)}
    for a, b in es: adj[a].append(b)
    starts = list(range(n)); rng.shuffle(starts)
    okdag &= valid(walk5(adj, False, starts)[::-1], es)
ck('l5 reversed post-order valid on 200 random DAGs', okdag)
ck('l5 quiz valid order', [p for p in itertools.permutations('abc') if valid(p, [('a', 'b'), ('a', 'c'), ('c', 'b')])] == [('a', 'c', 'b')])

# l6
A6 = {"A": ["B", "E"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C", "G", "H"], "E": ["A", "F", "G"], "F": ["E", "H"], "G": ["D", "E"], "H": ["D", "F"]}


def simple_paths(adj, s, t, path=None):
    path = path or [s]
    if s == t:
        yield list(path); return
    for v in adj[s]:
        if v not in path:
            path.append(v); yield from simple_paths(adj, v, t, path); path.pop()


ck('l6 route lengths', sorted(len(p) - 1 for p in simple_paths(A6, 'A', 'H')) == [3, 4, 4, 7])
par, dist, q, qo = {'A': None}, {'A': 0}, deque(['A']), []
while q:
    u = q.popleft(); qo.append(u)
    for v in sorted(A6[u]):
        if v not in par: par[v] = u; dist[v] = dist[u] + 1; q.append(v)
ck('l6 queue order and parents', qo == list('ABECFGDH') and par['F'] == 'E' and (dist['D'], par['D']) == (3, 'C') and (dist['H'], par['H']) == (3, 'F'))
path, node = [], 'H'
while node is not None:
    path.append(node); node = par[node]
ck('l6 walk back', path == ['H', 'F', 'E', 'A'])


def find_path(adj, s, t, seen=None):
    if seen is None: seen = set()
    seen.add(s)
    if s == t: return [s]
    for v in sorted(adj[s]):
        if v not in seen:
            p = find_path(adj, v, t, seen)
            if p: return [s] + p
    return None


ck('l6 dfs route', find_path(A6, 'A', 'H') == list('ABCDGEFH'))
A6s = undirected([('you', 'bank1'), ('you', 'bank2'), ('bank1', 'cust'), ('cust', 'fund'), ('bank2', 'ccp'), ('ccp', 'fund'), ('bank2', 'broker'), ('broker', 'fund'), ('bank1', 'ccp')])
ck('l6 settlement', levels(A6s, 'you')['fund'] == 3 and sum(len(p) == 4 for p in simple_paths(A6s, 'you', 'fund')) == 4)
ck('l6 pairs', len(eval(widget('l6-fewest-steps', 'screens', 8)['prelude'].split('=', 1)[1])) == 12)
ck('l6 maze', fn('homework-2', 'items', 0, 'maze_steps')(['...#', '##.#', '....', '.##.']) == 6)

# l7
A7 = {"A": [("B", 4), ("C", 1)], "B": [("D", 1)], "C": [("B", 2), ("D", 5), ("E", 2)], "D": [("F", 3)], "E": [("F", 6)], "F": [], "G": [("F", 1)]}


def routes(adj, s, t, cost=0, path=None):
    path = path or [s]
    if s == t:
        yield cost, ''.join(path); return
    for v, w_ in adj[s]:
        yield from routes(adj, v, t, cost + w_, path + [v])


ck('l7 route costs', sorted(routes(A7, 'A', 'F')) == [(7, 'ACBDF'), (8, 'ABDF'), (9, 'ACDF'), (9, 'ACEF')])
dist = {u: math.inf for u in A7}; dist['A'] = 0; heap = [(0, 'A')]; snaps, pops, stale = [], [], []
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]:
        stale.append((d, u)); snaps.append(sorted(heap)); continue
    pops.append((u, d))
    for v, w_ in A7[u]:
        if d + w_ < dist[v]:
            dist[v] = d + w_; heapq.heappush(heap, (d + w_, v))
    snaps.append(sorted(heap))
ck('l7 heap states', snaps[:6] == [[(1, 'C'), (4, 'B')], [(3, 'B'), (3, 'E'), (4, 'B'), (6, 'D')], [(3, 'E'), (4, 'B'), (4, 'D'), (6, 'D')],
                                 [(4, 'B'), (4, 'D'), (6, 'D'), (9, 'F')], [(4, 'D'), (6, 'D'), (9, 'F')], [(6, 'D'), (7, 'F'), (9, 'F')]], snaps[:6])
ck('l7 pop order and stale', pops == [('A', 0), ('C', 1), ('B', 3), ('E', 3), ('D', 4), ('F', 7)] and stale == [(4, 'B'), (6, 'D'), (9, 'F')])
trap = {}
exec('''import heapq
def dijkstra(adj, s):
    dist = {}
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        %s
        dist[u] = d
        for v, w in adj[u]:
            heapq.heappush(heap, (d + w, v))
    return dist''' % 'if u in dist: continue', trap)
t7 = trap['dijkstra'](A7, 'A')
ck('l7 one-line fix', (t7['B'], t7['D'], t7['F']) == (3, 4, 7))
dj = fn('l7-dijkstra', 'screens', 4, 'dijkstra')
NEG = {'A': [('B', 2), ('C', 3)], 'B': [], 'C': [('B', -2)]}
ck('l7 negative edge', dj(NEG, 'A')['B'] == 1)
FX7 = {'GBP': [('USD', 1.2), ('EUR', 0.5), ('JPY', 4.0)], 'EUR': [('USD', 0.6), ('JPY', 2.4), ('CHF', 0.7)], 'USD': [('JPY', 1.5)], 'CHF': [('JPY', 1.9)], 'JPY': []}
f7 = dj(FX7, 'GBP')
ck('l7 fx costs', [round(f7[c], 6) for c in ('EUR', 'USD', 'CHF', 'JPY')] == [0.5, 1.1, 1.2, 2.6])
ck('l7 exact compounding', round(1e6 * (1 - (1 - 5e-5) * (1 - 6e-5) * (1 - 1.5e-4)), 2) == 259.98)
ns7 = {}
exec(widget('l7-dijkstra', 'screens', 9)['prelude'], ns7)
adjL = {c: [] for c in ns7['CENTRES']}
for a, b, ms in ns7['LINKS']: adjL[a].append((b, ms))
l7 = dj(adjL, 'LD4')
ck('l7 latency', [round(l7[c], 6) for c in ('FR2', 'NY4', 'CH1', 'SG1', 'TY3')] == [4.2, 29.5, 33.4, 81.2, 103.4] and round(81.2 + 34.0, 6) == 115.2)
ck('l7 quiz sparse', 8.0e6 < 5e5 * math.log2(1e5) < 8.6e6)
worst = 0
for _ in range(300):
    n = 6; es = set()
    while len(es) < 9:
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b: es.add((a, b))
    adj = {i: [] for i in range(n)}
    for a, b in es: adj[a].append((b, rng.randint(1, 9)))
    dist = {u: math.inf for u in adj}; dist[0] = 0; heap = [(0, 0)]; pushes = 1
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]: continue
        for v, w_ in adj[u]:
            if d + w_ < dist[v]: dist[v] = d + w_; heapq.heappush(heap, (d + w_, v)); pushes += 1
    worst = max(worst, pushes)
ck('l7 at most E + 1 pushes', worst <= 10, worst)

# l8
parent = [0, 0, 2, 2, 2, 4, 4, 6]


def find(x):
    root = x
    while parent[root] != root: root = parent[root]
    while x != root:
        nxt = parent[x]; parent[x] = root; x = nxt
    return root


before = list(parent)
ck('l8 find(7)', find(7) == 2 and [i for i in range(8) if parent[i] != before[i]] == [6, 7] and parent == [0, 0, 2, 2, 2, 4, 2, 2])
DS = fn('l8-groups', 'screens', 5, 'DSU')
d = DS(8)
for a, b in [(0, 1), (2, 3), (1, 3), (5, 6)]: d.union(a, b)
ck('l8 components', d.count() == 4)
p = [0, 1, 2]; p[0] = 1; p[0] = 2
ck('l8 node-level union', p == [2, 1, 2])
n = 5000
ck('l8 chain steps', n * (n - 1) == 24995000)


def kruskal(n, es):
    d_ = DS(n); tot = k = 0
    for w_, a, b in sorted(es):
        if d_.union(a, b):
            tot += w_; k += 1
            if k == n - 1: break
    return tot


okk = True
for _ in range(200):
    n = rng.randint(2, 6)
    es = [(rng.randint(1, 9), i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.7]
    best = None
    for sub in itertools.combinations(es, n - 1):
        d_ = DS(n)
        if all(d_.union(a, b) for _, a, b in sub):
            s_ = sum(w_ for w_, _, _ in sub); best = s_ if best is None else min(best, s_)
    if best is not None: okk &= kruskal(n, es) == best
ck('l8 kruskal equals brute force on 200 random graphs', okk)
ck('review-2 kruskal', kruskal(5, [(4, 0, 1), (1, 0, 2), (2, 1, 2), (5, 1, 3), (8, 2, 3), (3, 3, 4), (9, 2, 4)]) == 11)

# l9
R9 = {'GBP': {'USD': 1.27}, 'USD': {'EUR': 0.92}, 'EUR': {'GBP': 0.86, 'CHF': 0.95}, 'CHF': {'GBP': 0.8985, 'USD': 1.142}}


def cycles(rates):
    out = {}

    def go(start, u, prod, path):
        for v, r in rates.get(u, {}).items():
            if v == start: out[frozenset(path)] = prod * r
            elif v not in path and v > start: go(start, v, prod * r, path + [v])
    for s in rates: go(s, s, 1.0, [s])
    return sorted(round(x, 6) for x in out.values())


ck('l9 loops', cycles(R9) == [0.997317, 0.998108, 1.004824], cycles(R9))
ws = [-math.log(r) for r in (1.27, 0.92, 0.86)]
ck('l9 weights', [round(x, 6) for x in ws] == [-0.239017, 0.083382, 0.150823] and round(sum(ws), 6) == -0.004812 and round(1 / 1.1684, 6) == 0.855871)
ck('l9 float', -math.log(1.25) - math.log(0.8) < 0 and abs(-math.log(1.25) - math.log(0.8) + 5.55e-17) < 1e-18)
dist = [0, math.inf, math.inf, math.inf]; rows = []
for _ in range(3):
    for u, v, w_ in [(2, 3, 1), (1, 2, 3), (0, 1, 2)]:
        if dist[u] + w_ < dist[v]: dist[v] = dist[u] + w_
    rows.append(list(dist[1:]))
ck('l9 passes', rows == [[2, math.inf, math.inf], [2, 5, math.inf], [2, 5, 6]])
gross = (1 / 0.8543) * 1.0850 * (1 / 1.2700)
ck('l9 after costs', round(1.0850 / 1.2700, 6) == 0.854331 and round(gross, 7) == 1.0000359 and round(1e6 * (gross * 0.9999**3 - 1), 2) == -264.03
   and round(1e6 * (gross - 1), 2) == 35.95 and sum(-math.log(0.9999 * r) for r in (1 / 0.8543, 1.0850, 1 / 1.27)) > 0)
ck('l9 quiz', round(1.27 * 0.787, 5) == 0.99949 and round(-math.log(1.27) - math.log(0.787), 6) == 0.00051 and 8 * 40 == 320 and round(1.25 / 1.05, 4) == 1.1905
   and round(0.92 * 0.95 * 1.142, 6) == 0.998108 and round(-1.142 - 0.92 - 0.95, 3) == -3.012 and round(1.27 * 0.92 * 0.855, 6) == 0.998982 and abs(1.6 * 0.8 * 0.78125 - 1) < 1e-15 and 1.25 * 0.8 == 1.0)
ck('review-2 loop', round(191.20 * 0.006135 * 0.8530, 6) == 1.000579 and round(191.20 * 0.006135, 6) == 1.173012 and round(-math.log(191.20 * 0.006135 * 0.8530), 6) == -0.000579)
ck('hw2 triangle', round(1.2650 * 0.9230 * 0.8580, 8) == 1.00179651 and round(1e6 * (1.2650 * 0.9230 * 0.8580 * 0.9998**3 - 1), 2) == 1195.55
   and round(1e6 * (1.2650 * 0.9230 * 0.8580 * 0.9998 - 1), 2) == 1596.15)

# l10
subsets = fn('l10-every-subset', 'screens', 9, 'subsets')
ck('l10 walk order', [''.join(s) for s in subsets(list('ABC'))] == ['ABC', 'AB', 'AC', 'A', 'BC', 'B', 'C', ''])
dup = subsets(['VOD', 'BP', 'VOD'])
ck('l10 duplicate ticker', len(dup) == 8 and len({frozenset(s) for s in dup}) == 4 and len({tuple(sorted(s)) for s in dup}) == 6)
calls = [0]


def cw(i, n):
    calls[0] += 1
    if i == n: return
    cw(i + 1, n); cw(i + 1, n)


cw(0, 3); c3 = calls[0]; calls[0] = 0; cw(0, 10)
ck('l10 call counts', c3 == 15 and calls[0] == 2047)
cap = [0]


def capped(i, k):
    if i == 6:
        cap[0] += 1; return
    if k < 3: capped(i + 1, k + 1)
    capped(i + 1, k)


capped(0, 0)
ck('l10 capped portfolios', cap[0] == 42)
ck('l10 thirty stocks', abs(2**30 / 1000 / 86400 - 12.4) < 0.05 and round(2**30 / 3.6e6) == 298 and 34 < 2**40 / 1000 / 86400 / 365.25 < 36)
out, path, xs = [], [], ['a', 'b']


def nopop(i):
    if i == len(xs):
        out.append(path[:]); return
    path.append(xs[i]); nopop(i + 1); nopop(i + 1)


nopop(0)
ck('l10 no pop', out == [['a', 'b'], ['a', 'b'], ['a', 'b', 'b'], ['a', 'b', 'b']])

# l11
att = lambda q, c: q[1] == c[1] or abs(q[0] - c[0]) == abs(q[1] - c[1])
safe = lambda qs, rows_: sorted(f'r{r}c{c}' for r in rows_ for c in range(1, 5) if not any(att(q, (r, c)) for q in qs))
ck('l11 safe cells', safe([(1, 2)], (2, 3, 4)) == ['r2c4', 'r3c1', 'r3c3', 'r4c1', 'r4c3', 'r4c4'] and safe([(1, 2), (2, 4)], (3, 4)) == ['r3c1', 'r4c1', 'r4c3'])


def qnodes(n):
    per = [0] * (n + 1)

    def place(row, qs):
        per[row] += 1
        if row == n: return
        for c in range(n):
            if not any(att(q, (row, c)) for q in qs): place(row + 1, qs + [(row, c)])
    place(0, [])
    return per


ck('l11 four queens nodes', qnodes(4) == [1, 4, 6, 4, 2] and sum(4**k for k in range(5)) == 341)
q8 = qnodes(8)
ck('l11 eight queens nodes', sum(q8) == 2057 and q8[8] == 92 and sum(8**k for k in range(9)) == 19173961 and 8**8 == 16777216)
safe3 = lambda qs, r: [c for c in (1, 2, 3) if not any(att(q, (r, c)) for q in qs)]
ck('l11 three queens', qnodes(3)[3] == 0 and qnodes(2)[2] == 0 and safe3([(1, 2)], 2) == [] and safe3([(1, 2)], 3) == [1, 3] and safe3([(1, 1)], 2) == [3] and safe3([(1, 1), (2, 3)], 3) == [])
cs = fn('homework-3', 'items', 0, 'combination_sum')
ck('l11 combos', cs([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]] and cs([2, 3, 6, 7], 7) == [[2, 2, 3], [7]])
ordered = lambda cands, t: 1 if t == 0 else sum(ordered(cands, t - c) for c in cands if c <= t)
ck('l11 ordered counts', ordered([2, 3, 5], 8) == 6 and ordered([2, 3, 6, 7], 7) == 4)


def ss_trap(xs, target):
    def walk(i, total):
        if total == target: return True
        if total > target: return False
        if i == len(xs): return False
        return walk(i + 1, total + xs[i]) or walk(i + 1, total)
    return walk(0, 0)


brute = lambda xs, t: any(sum(c) == t for k in range(len(xs) + 1) for c in itertools.combinations(xs, k))
ck('l11 unsafe prune', ss_trap([6, -4, 3], 2) is False and brute([6, -4, 3], 2) and ss_trap([4, -2, 1], 3) is False and brute([4, -2, 1], 3)
   and not brute([-4, 3], 2) and not brute([-2, 1], 3))
ssum = fn('l11-dead-ends', 'screens', 8, 'subset_sum')
ck('l11 sorted prune equals brute force', all(ssum(xs, t) == brute(xs, t) for xs, t in (([rng.randint(1, 15) for _ in range(rng.randint(0, 8))], rng.randint(0, 40)) for _ in range(500))))
ck('l11 subsets making 13', sorted(c for k in range(5) for c in itertools.combinations([2, 3, 5, 8], k) if sum(c) == 13) == [(2, 3, 8), (5, 8)])
ck('l11 unpruned calls', len(range(2, 52, 2)) == 25 and 2**26 - 1 == 67108863)
ck('l11 netting example', list(itertools.accumulate([5, -3, 2, -4])) == [5, 2, 4, 0])

# l12
cnt = {}


def fibc(n):
    cnt[n] = cnt.get(n, 0) + 1
    return n if n < 2 else fibc(n - 1) + fibc(n - 2)


tot = []
for n in range(9):
    cnt.clear(); fibc(n); tot.append(sum(cnt.values()))
ck('l12 naive calls', tot == [1, 1, 3, 5, 9, 15, 25, 41, 67])
cnt.clear(); fibc(5)
ck('l12 fib(5) repeats', cnt[2] == 3 and cnt[3] == 2 and cnt[1] == 5)
cnt.clear(); fibc(6)
ck('l12 fib(6) per-argument', [cnt[i] for i in range(7)] == [5, 8, 5, 3, 2, 1, 1])
C = [1, 1]
for n in range(2, 31): C.append(1 + C[-1] + C[-2])
F = [0, 1]
for n in range(2, 92): F.append(F[-1] + F[-2])
ck('l12 fib(30)', C[30] == 2692537 and F[30] == 832040 and 1.6 < C[30] / C[29] < 1.63)
cache, comp, hits, hitpaths = {}, [0], [0], []


def fm(k, pth=''):
    if k in cache:
        hits[0] += 1; hitpaths.append(pth); return cache[k]
    comp[0] += 1
    cache[k] = k if k < 2 else fm(k - 1, pth + 'a') + fm(k - 2, pth + 'b')
    return cache[k]


fm(5)
ck('l12 memo trace', comp[0] + hits[0] == 9 and hitpaths == ['aab', 'ab', 'b'], hitpaths)
cache.clear(); comp[0] = hits[0] = 0; fm(30)
ck('l12 memo fib(30)', (comp[0], hits[0]) == (31, 28))
gp = fn('l12-remembering', 'screens', 9, 'grid_paths')
ck('l12 grid paths', gp(3, 4) == 10 == math.comb(5, 2) and gp(3, 3) == 6 and all(gp(r, c) == math.comb(r + c - 2, r - 1) for r in range(1, 13) for c in range(1, 13))
   and math.comb(34, 17) == 2333606220 and math.comb(58, 29) == 30067266499541040)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec('\n'.join(DOC['l12-remembering']['screens'][6]['canvas']['params']['lines']), {})
ck('l12 stale price', buf.getvalue().split() == ['95.24', '95.24'] and round(100 / 1.1, 2) == 90.91)
from functools import lru_cache


@lru_cache(maxsize=None)
def value(*a):
    return 1


try:
    value([100, 101, 99]); te = False
except TypeError:
    te = True
ck('l12 unhashable list', te and value((100, 101, 99)) == value(100.5, 0.05) == value('VOD', 3) == 1)
ns = {}
src = [l for l in DOC['l12-remembering']['screens'][8]['canvas']['params']['lines'][:6]]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec('\n'.join(src), ns); ns['fib'](5); first = buf.getvalue().count('computing'); ns['fib'](6)
ck('l12 default dict', first == 6 and buf.getvalue().count('computing') == 7)


class Curve:
    def __init__(self, rate): self.rate = rate

    @lru_cache(maxsize=None)
    def df(self, t): return (1 + self.rate) ** -t


c = Curve(0.05); c.df(2); c.rate = 0.06
ck('l12 method cache', str(round(c.df(2), 4)) == '0.907' and str(round(1.06 ** -2, 4)) == '0.89')
ck('l12 lattice', sum(range(1, 32)) == 496 and 2**30 == 1073741824)

# l13
comp_ = lambda n, parts: 1 if n == 0 else sum(comp_(n - p, parts) for p in parts if p <= n)
ck('l13 ways', [comp_(n, (1, 2)) for n in range(7)] == [1, 1, 2, 3, 5, 8, 13] and [comp_(n, (1, 2, 3)) for n in range(7)] == [1, 1, 2, 4, 7, 13, 24])
seqs = [s for k in range(1, 5) for s in itertools.product((1, 2), repeat=k) if sum(s) == 4]
ck('l13 four stairs', len(seqs) == 5 and sum(s[-1] == 1 for s in seqs) == 3 and len({tuple(sorted(s)) for s in seqs}) == 3)
prev, cur = 1, 1
for _ in range(2, 7): prev, cur = cur, prev + cur
ck('l13 two variables', (prev, cur) == (8, 13))
ways = [0, 1] + [0] * 3
for i in range(2, 5): ways[i] = ways[i - 1] + ways[i - 2]
ck('l13 zero base', ways == [0, 1, 1, 2, 3])
stairs = fn('l13-climbing-stairs', 'screens', 9, 'stairs')
mc = fn('l13-climbing-stairs', 'screens', 9, 'min_coins')
ck('l13 stairs(90)', stairs(90) == F[91] == 4660046610375530309)
ck('l13 coin table', [mc([1, 3, 4], a) for a in range(7)] == [0, 1, 2, 1, 1, 2, 2] and mc([1, 5, 6, 9], 11) == 2 and mc([2, 5], 11) == 4
   and [mc([1, 5, 6, 9], a) for a in (10, 6, 5, 2)] == [2, 1, 1, 2])
INF = float('inf'); best = [0] + [INF] * 6
for a in range(6, 0, -1):
    for c_ in (1, 3, 4):
        if c_ <= a: best[a] = min(best[a], best[a - c_] + 1)
ck('l13 wrong direction', best == [0, 1, INF, 1, 1, INF, INF])


def brute_coins(coins, amount):
    """fewest coins by breadth-first search over amounts: an independent method"""
    level, frontier, seen_ = 0, {0}, {0}
    while frontier:
        if amount in frontier: return level
        frontier = {a + c_ for a in frontier for c_ in coins if a + c_ <= amount} - seen_
        seen_ |= frontier; level += 1
    return -1


ck('l13 table equals BFS on 300 random coin sets', all(mc(cs_, a) == brute_coins(cs_, a) for cs_, a in ((rng.sample(range(1, 12), rng.randint(1, 4)), rng.randint(0, 40)) for _ in range(300))))
ck('l13 lattice', math.comb(6, 3) == 20 and math.comb(10, 5) == 252)

# reviews and homework: stated numbers
RV = undirected([('P', 'Q'), ('P', 'S'), ('Q', 'R'), ('S', 'T'), ('R', 'U'), ('T', 'U')])
ck('review-1 orders', bfs(RV, 'P') == list('PQSRTU') and dfs(RV, 'P') == list('PQRUTS'))
st, seen, order = ['P'], set(), []
while st:
    u = st.pop()
    if u in seen: continue
    seen.add(u); order.append(u)
    for v in sorted(RV[u]):
        if v not in seen: st.append(v)
ck('review-1 naive stack', order == list('PSTURQ'))
GR = [[1, 1, 0, 0, 1], [0, 1, 0, 1, 1], [1, 0, 0, 0, 0], [1, 1, 0, 1, 0]]
ck('review-1 islands', len(comps(GR, S4)) == 4 and len(comps(GR, S8)) == 3 and sum(map(sum, GR)) == 10)
topo = fn('l5-tasks-in-order', 'screens', 3, 'topo_sort')
adjk = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": ["f"], "f": ["d", "g"], "g": []}
indeg = {u: 0 for u in adjk}
for u in adjk:
    for v in adjk[u]: indeg[v] += 1
q = deque(u for u in adjk if indeg[u] == 0); em = []
while q:
    u = q.popleft(); em.append(u)
    for v in adjk[u]:
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
ck('review-1 kahn', em == ['a', 'b', 'c'] and topo(adjk) is None)
RD = {'S': [('A', 2), ('B', 6)], 'A': [('B', 3), ('C', 7)], 'B': [('C', 1), ('T', 8)], 'C': [('T', 2)], 'T': []}
ck('review-2 dijkstra', dj(RD, 'S') == {'S': 0, 'A': 2, 'B': 5, 'C': 6, 'T': 8})
dist = {u: math.inf for u in RD}; dist['S'] = 0; heap = [(0, 'S')]; stale = []
while heap:
    d, u = heapq.heappop(heap)
    if d > dist[u]:
        stale.append((d, u)); continue
    for v, w_ in RD[u]:
        if d + w_ < dist[v]: dist[v] = d + w_; heapq.heappush(heap, (d + w_, v))
ck('review-2 stale', sorted(stale) == [(6, 'B'), (9, 'C'), (13, 'T')])
parent = [0, 0, 1, 2, 3]; find(4)
ck('review-2 compress', parent == [0, 0, 0, 0, 0])
dist = [0] + [math.inf] * 5; first_ok = None
for p_ in range(1, 7):
    for u in range(4, -1, -1):
        if dist[u] + 1 < dist[u + 1]: dist[u + 1] = dist[u] + 1
    if first_ok is None and dist[5] == 5: first_ok = p_
ck('review-2 passes', first_ok == 5)
ck('review-3', len(subsets(list('ABCD'))) == 16 and safe([(1, 1)], (2,)) == ['r2c3', 'r2c4'])
ck('review-3 queen under r1c2', safe([(1, 2)], (2,)) == ['r2c4'])
out, path, xs = [], [], [1, 2, 3]


def wl(start):
    out.append(path[:])
    for i in range(start, len(xs)):
        path.append(xs[i]); wl(i + 1); path.pop()


wl(0)
ck('review-3 loop order', out[:4] == [[], [1], [1, 2], [1, 2, 3]] and len(out) == 8)
ck('hw1 numbers', 20000**2 * 8 == 3.2e9 and 20000 * 8 / 1e9 == 0.00016 and 20000 * 20 * 8 == 3.2e6)
RING = [[1] * 5, [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1] * 5]
ck('hw1 ring', sorted(comps(RING, S4)) == [1, 16])
ck('hw3 numbers', sum(math.comb(25, k) for k in range(7)) == 245506 and 2**25 == 33554432 and 2**25 / 3.6e6 > 9 and 26 * 7 * 121 == 22022 and 21 * 101 == 2121
   and sum(p.index('A') < p.index('D') for p in itertools.permutations('ABCD')) == 12 and 5 + 2 - 3 - 4 == 0 and 31 * 830 == 25730)
tetra = [1, 1, 2, 4]
for n in range(4, 41): tetra.append(sum(tetra[-4:]))
ck('hw3 word break splits in the billions', tetra[40] > 10**9, tetra[40])

print(f'{N[0]} checks, {len(FAIL)} failed')
for f_ in FAIL:
    print('FAIL', f_)
sys.exit(1 if FAIL else 0)
