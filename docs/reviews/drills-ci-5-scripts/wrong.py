"""Wrong or too-slow solutions a real candidate writes, none of them planted by
the author. harness.py runs each against every example and hidden test.
CANDIDATES = {label: (drill id, source, what the slip is)}.
A label ending in '(right)' turned out to be a correct solution."""

C = {}

# ---------------------------------------------------------------- cheapest route
C['route: lexicographic, hops ignored'] = ('ci-cheapest-route', '''
import heapq
def cheapest_route(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    done = set()
    heap = [(0, [src])]
    while heap:
        cost, path = heapq.heappop(heap)
        u = path[-1]
        if u in done: continue
        done.add(u)
        if u == dst: return path
        for v, c in adj[u]:
            if v not in done: heapq.heappush(heap, (cost + c, path + [v]))
    return []
''', 'cheapest, then the list order; fewest roads forgotten')

C['route: dict of roads keeps last'] = ('ci-cheapest-route', '''
import heapq
def cheapest_route(n, roads, src, dst):
    w = {}
    for a, b, c in roads:
        w[(a, b)] = c; w[(b, a)] = c
    adj = [[] for _ in range(n)]
    for (a, b), c in w.items(): adj[a].append((b, c))
    done = set()
    heap = [(0, 0, (src,))]
    while heap:
        cost, k, path = heapq.heappop(heap)
        u = path[-1]
        if u in done: continue
        done.add(u)
        if u == dst: return list(path)
        for v, c in adj[u]:
            if v not in done: heapq.heappush(heap, (cost + c, k + 1, path + (v,)))
    return []
''', 'two roads between the same towns: the later one overwrites the cheaper')

C['route: walk on cost only'] = ('ci-cheapest-route', '''
import heapq
def cheapest_route(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    def dij(s):
        d = [None] * n; d[s] = 0; h = [(0, s)]
        while h:
            c, u = heapq.heappop(h)
            if c > d[u]: continue
            for v, w in adj[u]:
                if d[v] is None or c + w < d[v]:
                    d[v] = c + w; heapq.heappush(h, (c + w, v))
        return d
    f, b = dij(src), dij(dst)
    if f[dst] is None: return []
    out = [src]; u = src
    while u != dst:
        u = min(v for v, w in adj[u] if b[v] is not None and f[u] + w + b[v] == f[dst] and b[v] < b[u])
        out.append(u)
    return out
''', 'smallest next town on any cheapest route; fewest roads forgotten')

C['route: heap order as the tie'] = ('ci-cheapest-route', '''
import heapq
def cheapest_route(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    best = {src: (0, 0)}; came = {src: None}
    heap = [(0, 0, src)]
    while heap:
        c, k, u = heapq.heappop(heap)
        if (c, k) > best[u]: continue
        for v, w in sorted(adj[u]):
            if v not in best or (c + w, k + 1) < best[v]:
                best[v] = (c + w, k + 1); came[v] = u
                heapq.heappush(heap, (c + w, k + 1, v))
    if dst not in best: return []
    out = [dst]
    while came[out[-1]] is not None: out.append(came[out[-1]])
    return out[::-1]
''', '(cost, roads, town) in the heap and the first parent kept: no town-by-town tie')

C['route: search from dst, smaller next'] = ('ci-cheapest-route', '''
import heapq
def cheapest_route(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    best = {dst: (0, 0)}; nxt = {dst: None}
    heap = [(0, 0, dst)]
    while heap:
        c, k, u = heapq.heappop(heap)
        if (c, k) > best[u]: continue
        for v, w in adj[u]:
            cand = (c + w, k + 1)
            if v not in best or cand < best[v] or (cand == best[v] and u < nxt[v]):
                if v not in best or cand < best[v]: heapq.heappush(heap, (c + w, k + 1, v))
                best[v] = cand; nxt[v] = u
    if src not in best: return []
    out = [src]
    while nxt[out[-1]] is not None: out.append(nxt[out[-1]])
    return out
''', 'Dijkstra from dst keeping the smallest next town (right)')

# ---------------------------------------------------------------- checkpoint route
C['checkpoint: S not walkable on leg 2'] = ('ci-checkpoint-route', '''
from collections import deque
def solve_checkpoint_route(text):
    t = text.split(); r, c = int(t[0]), int(t[1]); g = t[2:2 + r]
    pos = {ch: (i, j) for i in range(r) for j in range(c) for ch in [g[i][j]] if ch in 'SCE'}
    def steps(a, b, ok):
        dist = {a: 0}; q = deque([a])
        while q:
            i, j = q.popleft()
            if (i, j) == b: return dist[(i, j)]
            for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if 0 <= x < r and 0 <= y < c and (x, y) not in dist and g[x][y] in ok:
                    dist[(x, y)] = dist[(i, j)] + 1; q.append((x, y))
        return -1
    a = steps(pos['S'], pos['C'], '.CE'); b = steps(pos['C'], pos['E'], '.E')
    return '-1' if a < 0 or b < 0 else str(a + b)
''', 'the second leg may not cross S again')

C['checkpoint: E blocks leg 1'] = ('ci-checkpoint-route', '''
from collections import deque
def solve_checkpoint_route(text):
    t = text.split(); r, c = int(t[0]), int(t[1]); g = t[2:2 + r]
    pos = {ch: (i, j) for i in range(r) for j in range(c) for ch in [g[i][j]] if ch in 'SCE'}
    def steps(a, b, ok):
        dist = {a: 0}; q = deque([a])
        while q:
            i, j = q.popleft()
            if (i, j) == b: return dist[(i, j)]
            for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if 0 <= x < r and 0 <= y < c and (x, y) not in dist and g[x][y] in ok:
                    dist[(x, y)] = dist[(i, j)] + 1; q.append((x, y))
        return -1
    a = steps(pos['S'], pos['C'], '.CS'); b = steps(pos['C'], pos['E'], '.ESC')
    return '-1' if a < 0 or b < 0 else str(a + b)
''', 'the walk to C may not pass E')

C['checkpoint: lines not stripped'] = ('ci-checkpoint-route', '''
from collections import deque
def solve_checkpoint_route(text):
    lines = text.split('\\n'); r, c = map(int, lines[0].split()); g = lines[1:1 + r]
    pos = {ch: (i, j) for i in range(r) for j in range(c) for ch in [g[i][j]] if ch in 'SCE'}
    def steps(a, b):
        dist = {a: 0}; q = deque([a])
        while q:
            i, j = q.popleft()
            if (i, j) == b: return dist[(i, j)]
            for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if 0 <= x < r and 0 <= y < c and (x, y) not in dist and g[x][y] != '#':
                    dist[(x, y)] = dist[(i, j)] + 1; q.append((x, y))
        return -1
    a = steps(pos['S'], pos['C']); b = steps(pos['C'], pos['E'])
    return '-1' if a < 0 or b < 0 else str(a + b)
''', 'rows read by line with the spaces left on')

C['checkpoint: seen kept in a list'] = ('ci-checkpoint-route', '''
def solve_checkpoint_route(text):
    t = text.split(); r, c = int(t[0]), int(t[1]); g = t[2:2 + r]
    pos = {ch: (i, j) for i in range(r) for j in range(c) for ch in [g[i][j]] if ch in 'SCE'}
    def steps(a, b):
        seen = [a]; q = [(a, 0)]
        while q:
            (i, j), d = q.pop(0)
            if (i, j) == b: return d
            for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if 0 <= x < r and 0 <= y < c and (x, y) not in seen and g[x][y] != '#':
                    seen.append((x, y)); q.append(((x, y), d + 1))
        return -1
    a = steps(pos['S'], pos['C']); b = steps(pos['C'], pos['E'])
    return '-1' if a < 0 or b < 0 else str(a + b)
''', 'right idea, quadratic: visited cells in a list')

# ---------------------------------------------------------------- ferry timetable
C['ferry: sweeps both ways in turn'] = ('ci-ferry-timetable', '''
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    legs = [v[2 + 4 * k: 6 + 4 * k] for k in range(m)]
    best = [None] * (n + 1); best[1] = 0
    changed = True; rev = legs[::-1]; turn = 0
    while changed:
        changed = False
        for a, b, t, p in (legs if turn % 2 == 0 else rev):
            if best[a] is not None:
                arr = (best[a] + p - 1) // p * p + t
                if best[b] is None or arr < best[b]:
                    best[b] = arr; changed = True
        turn += 1
    return str(best[n]) if best[n] is not None else '-1'
''', 'the method the constraints rule out, sweeping forwards then backwards')

C['ferry: crossings sorted by port first'] = ('ci-ferry-timetable', '''
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    legs = sorted(v[2 + 4 * k: 6 + 4 * k] for k in range(m))
    best = [None] * (n + 1); best[1] = 0
    changed = True
    while changed:
        changed = False
        for a, b, t, p in legs:
            if best[a] is not None:
                arr = (best[a] + p - 1) // p * p + t
                if best[b] is None or arr < best[b]:
                    best[b] = arr; changed = True
    return str(best[n]) if best[n] is not None else '-1'
''', 'the method the constraints rule out, after sorting the crossings')

C['ferry: queue of changed ports (right)'] = ('ci-ferry-timetable', '''
from collections import deque
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    out = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = v[2 + 4 * k: 6 + 4 * k]; out[a].append((b, t, p))
    best = [None] * (n + 1); best[1] = 0
    q = deque([1]); inq = [False] * (n + 1)
    while q:
        u = q.popleft(); inq[u] = False
        for b, t, p in out[u]:
            arr = (best[u] + p - 1) // p * p + t
            if best[b] is None or arr < best[b]:
                best[b] = arr
                if not inq[b]: inq[b] = True; q.append(b)
    return str(best[n]) if best[n] is not None else '-1'
''', 'relaxing from a queue of changed ports: no heap, right, worst case slow')

C['ferry: fixed on first reach'] = ('ci-ferry-timetable', '''
import heapq
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    out = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = v[2 + 4 * k: 6 + 4 * k]; out[a].append((b, t, p))
    best = {1: 0}; heap = [(0, 1)]
    while heap:
        now, u = heapq.heappop(heap)
        for b, t, p in out[u]:
            if b not in best:
                best[b] = (now + p - 1) // p * p + t
                heapq.heappush(heap, (best[b], b))
    return str(best.get(n, -1))
''', 'a port is fixed when first pushed, not when popped')

C['ferry: two-way crossings'] = ('ci-ferry-timetable', '''
import heapq
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    out = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = v[2 + 4 * k: 6 + 4 * k]; out[a].append((b, t, p)); out[b].append((a, t, p))
    best = {1: 0}; heap = [(0, 1)]
    while heap:
        now, u = heapq.heappop(heap)
        if now > best[u]: continue
        for b, t, p in out[u]:
            arr = (now + p - 1) // p * p + t
            if b not in best or arr < best[b]:
                best[b] = arr; heapq.heappush(heap, (arr, b))
    return str(best.get(n, -1))
''', 'crossings read as two-way')

C['ferry: scan for the nearest port'] = ('ci-ferry-timetable', '''
def solve_ferry_timetable(text):
    v = list(map(int, text.split())); n, m = v[0], v[1]
    out = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = v[2 + 4 * k: 6 + 4 * k]; out[a].append((b, t, p))
    INF = float('inf'); best = [INF] * (n + 1); best[1] = 0; done = [False] * (n + 1)
    while True:
        u = -1
        for x in range(1, n + 1):
            if not done[x] and best[x] < INF and (u < 0 or best[x] < best[u]): u = x
        if u < 0: break
        done[u] = True
        for b, t, p in out[u]:
            arr = (best[u] + p - 1) // p * p + t
            if arr < best[b]: best[b] = arr
    return str(best[n]) if best[n] < INF else '-1'
''', 'Dijkstra with a linear scan in place of the heap')

# ---------------------------------------------------------------- first circular rule
C['loop rule: search back from a'] = ('ci-first-circular-rule', '''
def first_cycle_rule(n, rules):
    before = [[] for _ in range(n)]
    for i, (a, b) in enumerate(rules):
        seen = {a}; stack = [a]
        while stack:
            u = stack.pop()
            for w in before[u]:
                if w not in seen:
                    seen.add(w); stack.append(w)
        if b in seen: return i
        before[b].append(a)
    return -1
''', 'the per-rule search the constraints rule out, run backwards from a')

C['loop rule: recursive search back'] = ('ci-first-circular-rule', '''
def first_cycle_rule(n, rules):
    before = [[] for _ in range(n)]
    def reach(u, target, seen):
        if u == target: return True
        seen.add(u)
        return any(w not in seen and reach(w, target, seen) for w in before[u])
    for i, (a, b) in enumerate(rules):
        if reach(a, b, set()): return i
        before[b].append(a)
    return -1
''', 'the same, recursive')

C['loop rule: self rule ignored'] = ('ci-first-circular-rule', '''
def first_cycle_rule(n, rules):
    def loops(k):
        after = [[] for _ in range(n)]; waits = [0] * n
        for a, b in rules[:k]:
            if a != b:
                after[a].append(b); waits[b] += 1
        ready = [j for j in range(n) if waits[j] == 0]; done = 0
        while ready:
            j = ready.pop(); done += 1
            for x in after[j]:
                waits[x] -= 1
                if waits[x] == 0: ready.append(x)
        return done < n
    if not loops(len(rules)): return -1
    lo, hi = 1, len(rules)
    while lo < hi:
        mid = (lo + hi) // 2
        if loops(mid): hi = mid
        else: lo = mid + 1
    return lo - 1
''', '[a, a] dropped')

C['loop rule: search bound off by one'] = ('ci-first-circular-rule', '''
def first_cycle_rule(n, rules):
    def loops(k):
        after = [[] for _ in range(n)]; waits = [0] * n
        for a, b in rules[:k]:
            after[a].append(b); waits[b] += 1
        ready = [j for j in range(n) if waits[j] == 0]; done = 0
        while ready:
            j = ready.pop(); done += 1
            for x in after[j]:
                waits[x] -= 1
                if waits[x] == 0: ready.append(x)
        return done < n
    lo, hi = 0, len(rules) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if loops(mid + 1): hi = mid
        else: lo = mid + 1
    return lo if loops(lo + 1) and rules else -1
''', 'bounds on positions (right)')

# ---------------------------------------------------------------- flood reach
C['flood: recursion, limit raised'] = ('ci-flood-reach', '''
import sys
sys.setrecursionlimit(1000000)
def wet_cells(heights, r, c):
    rows, cols = len(heights), len(heights[0]); seen = set()
    def flow(i, j):
        seen.add((i, j))
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen and heights[a][b] <= heights[i][j]:
                flow(a, b)
    flow(r, c)
    return len(seen)
''', 'recursive fill with the limit raised')

C['flood: counted on pop, marked on pop'] = ('ci-flood-reach', '''
def wet_cells(heights, r, c):
    rows, cols = len(heights), len(heights[0]); seen = set(); stack = [(r, c)]; count = 0
    while stack:
        i, j = stack.pop(); count += 1; seen.add((i, j))
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen and heights[a][b] <= heights[i][j]:
                stack.append((a, b))
    return count
''', 'a cell pushed twice is counted twice')

C['flood: r and c swapped'] = ('ci-flood-reach', '''
def wet_cells(heights, r, c):
    rows, cols = len(heights), len(heights[0]); seen = {(c, r)}; stack = [(c, r)]
    while stack:
        i, j = stack.pop()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen and heights[a][b] <= heights[i][j]:
                seen.add((a, b)); stack.append((a, b))
    return len(seen)
''', 'start read as (c, r)')

C['flood: start cell not counted'] = ('ci-flood-reach', '''
def wet_cells(heights, r, c):
    rows, cols = len(heights), len(heights[0]); seen = {(r, c)}; stack = [(r, c)]
    while stack:
        i, j = stack.pop()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen and heights[a][b] <= heights[i][j]:
                seen.add((a, b)); stack.append((a, b))
    return len(seen) - 1
''', 'the first cell left out')

# ---------------------------------------------------------------- half fare
C['voucher: answer read from the used layer'] = ('ci-half-fare-route', '''
import heapq
def cheapest_with_coupon(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    INF = float('inf'); best = [[INF, INF] for _ in range(n)]; best[src][0] = 0
    heap = [(0, src, 0)]
    while heap:
        c, u, k = heapq.heappop(heap)
        if c > best[u][k]: continue
        for v, w in adj[u]:
            if c + w < best[v][k]:
                best[v][k] = c + w; heapq.heappush(heap, (c + w, v, k))
            if k == 0 and c + w // 2 < best[v][1]:
                best[v][1] = c + w // 2; heapq.heappush(heap, (c + w // 2, v, 1))
    if best[dst][0] == INF: return -1
    return best[dst][1] if best[dst][1] < INF else best[dst][0]
''', 'the voucher always helps, so the answer is taken from the voucher-used layer')

C['voucher: rounds half up'] = ('ci-half-fare-route', '''
import heapq
def cheapest_with_coupon(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    INF = float('inf'); best = [[INF, INF] for _ in range(n)]; best[src][0] = 0
    heap = [(0, src, 0)]
    while heap:
        c, u, k = heapq.heappop(heap)
        if c > best[u][k]: continue
        for v, w in adj[u]:
            if c + w < best[v][k]:
                best[v][k] = c + w; heapq.heappush(heap, (c + w, v, k))
            if k == 0 and c + (w + 1) // 2 < best[v][1]:
                best[v][1] = c + (w + 1) // 2; heapq.heappush(heap, (c + (w + 1) // 2, v, 1))
    m = min(best[dst])
    return -1 if m == INF else m
''', 'half rounded up')

C['voucher: one distance per town'] = ('ci-half-fare-route', '''
import heapq
def cheapest_with_coupon(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    done = set(); heap = [(0, src, 0)]
    while heap:
        c, u, k = heapq.heappop(heap)
        if u in done: continue
        done.add(u)
        if u == dst: return c
        for v, w in adj[u]:
            if v not in done:
                heapq.heappush(heap, (c + w, v, k))
                if k == 0: heapq.heappush(heap, (c + w // 2, v, 1))
    return -1
''', 'a town is closed the first time it leaves the heap, whichever voucher state')

C['voucher: halve the whole total'] = ('ci-half-fare-route', '''
import heapq
def cheapest_with_coupon(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c)); adj[b].append((a, c))
    INF = float('inf'); best = [INF] * n; best[src] = 0; big = [0] * n
    heap = [(0, src)]
    while heap:
        c, u = heapq.heappop(heap)
        if c > best[u]: continue
        for v, w in adj[u]:
            if c + w < best[v] or (c + w == best[v] and max(big[u], w) > big[v]):
                best[v] = c + w; big[v] = max(big[u], w); heapq.heappush(heap, (c + w, v))
    return -1 if best[dst] == INF else best[dst] - big[dst] + big[dst] // 2
''', 'the planted greedy with ties broken towards the dearer road')

# ---------------------------------------------------------------- island shapes
C['shapes: eight neighbours'] = ('ci-island-shapes', '''
def lone_shapes(grid):
    R, C = len(grid), len(grid[0]); seen = set(); count = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and (r, c) not in seen:
                seen.add((r, c)); stack = [(r, c)]; cells = []
                while stack:
                    i, j = stack.pop(); cells.append((i - r, j - c))
                    for a in (i - 1, i, i + 1):
                        for b in (j - 1, j, j + 1):
                            if 0 <= a < R and 0 <= b < C and grid[a][b] == '#' and (a, b) not in seen:
                                seen.add((a, b)); stack.append((a, b))
                k = frozenset(cells); count[k] = count.get(k, 0) + 1
    return sum(1 for v in count.values() if v == 1)
''', 'slicks joined through corners too')

C['shapes: size and bounding box'] = ('ci-island-shapes', '''
def lone_shapes(grid):
    R, C = len(grid), len(grid[0]); seen = set(); count = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and (r, c) not in seen:
                seen.add((r, c)); stack = [(r, c)]; cells = []
                while stack:
                    i, j = stack.pop(); cells.append((i, j))
                    for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= a < R and 0 <= b < C and grid[a][b] == '#' and (a, b) not in seen:
                            seen.add((a, b)); stack.append((a, b))
                k = (len(cells), max(i for i, _ in cells) - min(i for i, _ in cells), max(j for _, j in cells) - min(j for _, j in cells))
                count[k] = count.get(k, 0) + 1
    return sum(1 for v in count.values() if v == 1)
''', 'shape named by its size and bounding box')

C['shapes: row and column profiles'] = ('ci-island-shapes', '''
def lone_shapes(grid):
    R, C = len(grid), len(grid[0]); seen = set(); count = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and (r, c) not in seen:
                seen.add((r, c)); stack = [(r, c)]; cells = []
                while stack:
                    i, j = stack.pop(); cells.append((i, j))
                    for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= a < R and 0 <= b < C and grid[a][b] == '#' and (a, b) not in seen:
                            seen.add((a, b)); stack.append((a, b))
                r0 = min(i for i, _ in cells); c0 = min(j for _, j in cells)
                rows = {}; cols = {}
                for i, j in cells:
                    rows[i - r0] = rows.get(i - r0, 0) + 1; cols[j - c0] = cols.get(j - c0, 0) + 1
                k = (tuple(sorted(rows.items())), tuple(sorted(cols.items())))
                count[k] = count.get(k, 0) + 1
    return sum(1 for v in count.values() if v == 1)
''', 'shape named by its cells per row and per column')

C['shapes: recursive fill'] = ('ci-island-shapes', '''
def lone_shapes(grid):
    R, C = len(grid), len(grid[0]); seen = set(); count = {}
    def fill(i, j, r, c, cells):
        seen.add((i, j)); cells.append((i - r, j - c))
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and grid[a][b] == '#' and (a, b) not in seen:
                fill(a, b, r, c, cells)
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and (r, c) not in seen:
                cells = []; fill(r, c, r, c, cells)
                k = frozenset(cells); count[k] = count.get(k, 0) + 1
    return sum(1 for v in count.values() if v == 1)
''', 'recursive fill, default limit: breaks on a slick of a thousand cells in a row')

C['shapes: turns and flips match'] = ('ci-island-shapes', '''
def lone_shapes(grid):
    R, C = len(grid), len(grid[0]); seen = set(); count = {}
    def norm(cells):
        r0 = min(i for i, _ in cells); c0 = min(j for _, j in cells)
        return tuple(sorted((i - r0, j - c0) for i, j in cells))
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and (r, c) not in seen:
                seen.add((r, c)); stack = [(r, c)]; cells = []
                while stack:
                    i, j = stack.pop(); cells.append((i, j))
                    for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if 0 <= a < R and 0 <= b < C and grid[a][b] == '#' and (a, b) not in seen:
                            seen.add((a, b)); stack.append((a, b))
                forms = []
                for f in (lambda i, j: (i, j), lambda i, j: (i, -j), lambda i, j: (-i, j), lambda i, j: (-i, -j),
                          lambda i, j: (j, i), lambda i, j: (j, -i), lambda i, j: (-j, i), lambda i, j: (-j, -i)):
                    forms.append(norm([f(i, j) for i, j in cells]))
                k = min(forms); count[k] = count.get(k, 0) + 1
    return sum(1 for v in count.values() if v == 1)
''', 'turned and flipped copies treated as one shape')

# ---------------------------------------------------------------- line from pairs
C['line: numbers ordered by value'] = ('ci-line-from-pairs', '''
import re
def rebuild_line(pairs):
    near = {}
    for x, y in pairs:
        near.setdefault(x, []).append(y); near.setdefault(y, []).append(x)
    key = lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\\d+)', s)]
    start = min((s for s in near if len(near[s]) == 1), key=key)
    line = [start]; prev = None; cur = start
    while True:
        nxt = [s for s in near[cur] if s != prev]
        if not nxt: return line
        prev, cur = cur, nxt[0]; line.append(cur)
''', "'S2' put before 'S10'")

C['line: scan the pairs each step'] = ('ci-line-from-pairs', '''
def rebuild_line(pairs):
    deg = {}
    for x, y in pairs:
        deg[x] = deg.get(x, 0) + 1; deg[y] = deg.get(y, 0) + 1
    cur = min(s for s in deg if deg[s] == 1)
    line = [cur]; left = [list(p) for p in pairs]
    while left:
        for k, (x, y) in enumerate(left):
            if x == cur or y == cur:
                cur = y if x == cur else x; line.append(cur); left.pop(k); break
    return line
''', 'the scan the constraints rule out')

C['line: recursive walk'] = ('ci-line-from-pairs', '''
def rebuild_line(pairs):
    near = {}
    for x, y in pairs:
        near.setdefault(x, []).append(y); near.setdefault(y, []).append(x)
    start = min(s for s in near if len(near[s]) == 1)
    out = []
    def go(cur, prev):
        out.append(cur)
        for s in near[cur]:
            if s != prev: go(s, cur)
    go(start, None)
    return out
''', 'the walk written as a recursion')

C['line: smaller end by length first'] = ('ci-line-from-pairs', '''
def rebuild_line(pairs):
    near = {}
    for x, y in pairs:
        near.setdefault(x, []).append(y); near.setdefault(y, []).append(x)
    start = min((s for s in near if len(near[s]) == 1), key=lambda s: (len(s), s))
    line = [start]; prev = None; cur = start
    while True:
        nxt = [s for s in near[cur] if s != prev]
        if not nxt: return line
        prev, cur = cur, nxt[0]; line.append(cur)
''', 'shorter name first')

# ---------------------------------------------------------------- loop cables
C['cables: no shortening, b under a'] = ('ci-loop-cables', '''
def loop_cables(n, cables):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    out = []
    for i, (a, b) in enumerate(cables):
        ra, rb = find(a), find(b)
        if ra == rb: out.append(i)
        else: parent[rb] = ra
    return out
''', 'parent chains never shortened, second root hung under the first')

C['cables: no shortening, a under b'] = ('ci-loop-cables', '''
def loop_cables(n, cables):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    out = []
    for i, (a, b) in enumerate(cables):
        ra, rb = find(a), find(b)
        if ra == rb: out.append(i)
        else: parent[ra] = rb
    return out
''', 'parent chains never shortened, first root hung under the second')

C['cables: group labels, relabel b side'] = ('ci-loop-cables', '''
def loop_cables(n, cables):
    label = list(range(n)); members = {i: [i] for i in range(n)}
    out = []
    for i, (a, b) in enumerate(cables):
        la, lb = label[a], label[b]
        if la == lb: out.append(i)
        else:
            for x in members[lb]: label[x] = la
            members[la] += members.pop(lb)
    return out
''', 'group labels rewritten without picking the smaller group')

C['cables: group labels, relabel a side'] = ('ci-loop-cables', '''
def loop_cables(n, cables):
    label = list(range(n)); members = {i: [i] for i in range(n)}
    out = []
    for i, (a, b) in enumerate(cables):
        la, lb = label[a], label[b]
        if la == lb: out.append(i)
        else:
            for x in members[la]: label[x] = lb
            members[lb] += members.pop(la)
    return out
''', 'the same, the other way')

C['cables: both racks seen before'] = ('ci-loop-cables', '''
def loop_cables(n, cables):
    seen = set(); out = []
    for i, (a, b) in enumerate(cables):
        if a in seen and b in seen: out.append(i)
        seen.add(a); seen.add(b)
    return out
''', 'spare when both racks already hold a cable')

# ---------------------------------------------------------------- nearest depot
C['depot: ties block the search'] = ('ci-nearest-depot', '''
from collections import deque
def depot_shares(grid):
    R, C = len(grid), len(grid[0]); own = {}; dist = {}; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] in 'AB':
                own[(i, j)] = grid[i][j]; dist[(i, j)] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        if own[(i, j)] == 'T': continue
        for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            a, b = p
            if 0 <= a < R and 0 <= b < C and grid[a][b] != '#':
                if p not in own:
                    own[p] = own[(i, j)]; dist[p] = dist[(i, j)] + 1; q.append(p)
                elif dist[p] == dist[(i, j)] + 1 and own[p] != own[(i, j)]:
                    own[p] = 'T'
    out = [0, 0]
    for (i, j), w in own.items():
        if grid[i][j] == '.' and w in 'AB': out[w == 'B'] += 1
    return out
''', 'one search with a tie mark, but a tied cell passes nothing on')

C['depot: one search, tie mark passed on (right)'] = ('ci-nearest-depot', '''
from collections import deque
def depot_shares(grid):
    R, C = len(grid), len(grid[0]); own = {}; dist = {}; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] in 'AB':
                own[(i, j)] = grid[i][j]; dist[(i, j)] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            a, b = p
            if 0 <= a < R and 0 <= b < C and grid[a][b] != '#':
                if p not in own:
                    own[p] = own[(i, j)]; dist[p] = dist[(i, j)] + 1; q.append(p)
                elif dist[p] == dist[(i, j)] + 1 and own[p] != own[(i, j)]:
                    own[p] = 'T'
    out = [0, 0]
    for (i, j), w in own.items():
        if grid[i][j] == '.' and w in 'AB': out[w == 'B'] += 1
    return out
''', 'one search, tie marks passed on')

C['depot: per depot, pruned'] = ('ci-nearest-depot', '''
from collections import deque
def depot_shares(grid):
    R, C = len(grid), len(grid[0]); INF = 10 ** 9
    near = {'A': [[INF] * C for _ in range(R)], 'B': [[INF] * C for _ in range(R)]}
    for si in range(R):
        for sj in range(C):
            m = grid[si][sj]
            if m not in 'AB': continue
            best = near[m]; best[si][sj] = 0; q = deque([(si, sj)])
            while q:
                i, j = q.popleft(); d = best[i][j] + 1
                for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if 0 <= a < R and 0 <= b < C and grid[a][b] != '#' and d < best[a][b]:
                        best[a][b] = d; q.append((a, b))
    out = [0, 0]
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '.':
                x, y = near['A'][i][j], near['B'][i][j]
                if x < y: out[0] += 1
                elif y < x: out[1] += 1
    return out
''', 'one search per depot, stopped where an earlier depot is as near')

C['depot: unreached read as -1'] = ('ci-nearest-depot', '''
from collections import deque
def depot_shares(grid):
    R, C = len(grid), len(grid[0])
    def spread(m):
        dist = [[-1] * C for _ in range(R)]; q = deque()
        for i in range(R):
            for j in range(C):
                if grid[i][j] == m: dist[i][j] = 0; q.append((i, j))
        while q:
            i, j = q.popleft()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R and 0 <= b < C and dist[a][b] < 0 and grid[a][b] != '#':
                    dist[a][b] = dist[i][j] + 1; q.append((a, b))
        return dist
    da, db = spread('A'), spread('B'); out = [0, 0]
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '.':
                if da[i][j] < db[i][j]: out[0] += 1
                elif db[i][j] < da[i][j]: out[1] += 1
    return out
''', 'an unreached -1 compared as a distance')

C['depot: depots counted as streets'] = ('ci-nearest-depot', '''
from collections import deque
def depot_shares(grid):
    R, C = len(grid), len(grid[0]); INF = 10 ** 9
    def spread(m):
        dist = [[INF] * C for _ in range(R)]; q = deque()
        for i in range(R):
            for j in range(C):
                if grid[i][j] == m: dist[i][j] = 0; q.append((i, j))
        while q:
            i, j = q.popleft()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R and 0 <= b < C and dist[a][b] == INF and grid[a][b] != '#':
                    dist[a][b] = dist[i][j] + 1; q.append((a, b))
        return dist
    da, db = spread('A'), spread('B'); out = [0, 0]
    for i in range(R):
        for j in range(C):
            if grid[i][j] != '#':
                if da[i][j] < db[i][j]: out[0] += 1
                elif db[i][j] < da[i][j]: out[1] += 1
    return out
''', 'depot cells counted too')

# ---------------------------------------------------------------- reclaimed land
C['land: island lists, others into the first'] = ('ci-reclaimed-land', '''
def largest_after_each(rows, cols, fills):
    isle = {}; cells = {}; best = 0; out = []; nid = 0
    for r, c in fills:
        if (r, c) not in isle:
            ids = []
            for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if p in isle and isle[p] not in ids: ids.append(isle[p])
            if not ids:
                nid += 1; isle[(r, c)] = nid; cells[nid] = [(r, c)]; k = nid
            else:
                k = ids[0]; isle[(r, c)] = k; cells[k].append((r, c))
                for o in ids[1:]:
                    for p in cells[o]: isle[p] = k
                    cells[k] += cells.pop(o)
            best = max(best, len(cells[k]))
        out.append(best)
    return out
''', 'island labels rewritten without picking the smaller island')

C['land: island lists, all into the new cell'] = ('ci-reclaimed-land', '''
def largest_after_each(rows, cols, fills):
    isle = {}; cells = {}; best = 0; out = []; nid = 0
    for r, c in fills:
        if (r, c) not in isle:
            nid += 1; isle[(r, c)] = nid; cells[nid] = [(r, c)]
            for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if p in isle and isle[p] != nid:
                    o = isle[p]
                    for x in cells[o]: isle[x] = nid
                    cells[nid] += cells.pop(o)
            best = max(best, len(cells[nid]))
        out.append(best)
    return out
''', 'every neighbouring island relabelled to the new cell')

C['land: sizes added per neighbour'] = ('ci-reclaimed-land', '''
def largest_after_each(rows, cols, fills):
    parent = {}; size = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    best = 0; out = []
    for r, c in fills:
        if (r, c) not in parent:
            parent[(r, c)] = (r, c); size[(r, c)] = 1
            for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if p in parent:
                    x, y = find((r, c)), find(p)
                    parent[y] = x; size[x] += size[y] if x != y else 0
                    if x == y: size[x] += 0
            best = max(best, size[find((r, c))])
        out.append(best)
    return out
''', 'union-find without union by size (right, slower)')

C['land: no shortening, no sizes order'] = ('ci-reclaimed-land', '''
def largest_after_each(rows, cols, fills):
    parent = {}; size = {}
    def find(x):
        while parent[x] != x: x = parent[x]
        return x
    best = 0; out = []
    for r, c in fills:
        if (r, c) not in parent:
            parent[(r, c)] = (r, c); size[(r, c)] = 1
            for p in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if p in parent:
                    x, y = find((r, c)), find(p)
                    if x != y:
                        parent[x] = y; size[y] += size[x]
            best = max(best, size[find((r, c))])
        out.append(best)
    return out
''', 'parent chains never shortened, new root hung under the old')

C['land: flat index wraps the row edge'] = ('ci-reclaimed-land', '''
def largest_after_each(rows, cols, fills):
    parent = {}; size = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    best = 0; out = []
    for r, c in fills:
        k = r * cols + c
        if k not in parent:
            parent[k] = k; size[k] = 1
            for p in (k + 1, k - 1, k + cols, k - cols):
                if p in parent:
                    x, y = find(k), find(p)
                    if x != y:
                        if size[x] < size[y]: x, y = y, x
                        parent[y] = x; size[x] += size[y]
            best = max(best, size[find(k)])
        out.append(best)
    return out
''', 'cell numbers plus and minus one join across the end of a row')

# ---------------------------------------------------------------- safest walk
C['walk: levels from the top, fresh search'] = ('ci-safest-walk', '''
from collections import deque
def safest_walk(grid):
    R, C = len(grid), len(grid[0]); cover = [[-1] * C for _ in range(R)]; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'G': cover[i][j] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and cover[a][b] < 0:
                cover[a][b] = cover[i][j] + 1; q.append((a, b))
    for level in range(min(cover[0][0], cover[R - 1][C - 1]), -1, -1):
        seen = {(0, 0)}; q = deque([(0, 0)])
        while q:
            i, j = q.popleft()
            if (i, j) == (R - 1, C - 1): return level
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R and 0 <= b < C and (a, b) not in seen and grid[a][b] != '#' and cover[a][b] >= level:
                    seen.add((a, b)); q.append((a, b))
    return -1
''', 'covers by one search, then every level from the top with a fresh search: rows x cols x levels')

C['walk: cover of the shortest walk'] = ('ci-safest-walk', '''
from collections import deque
def safest_walk(grid):
    R, C = len(grid), len(grid[0]); cover = [[-1] * C for _ in range(R)]; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'G': cover[i][j] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and cover[a][b] < 0:
                cover[a][b] = cover[i][j] + 1; q.append((a, b))
    low = {(0, 0): cover[0][0]}; q = deque([(0, 0)])
    while q:
        i, j = q.popleft()
        if (i, j) == (R - 1, C - 1): return low[(i, j)]
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and (a, b) not in low and grid[a][b] != '#':
                low[(a, b)] = min(low[(i, j)], cover[a][b]); q.append((a, b))
    return -1
''', 'the least cover along a shortest walk')

C['walk: right and down only'] = ('ci-safest-walk', '''
from collections import deque
def safest_walk(grid):
    R, C = len(grid), len(grid[0]); cover = [[-1] * C for _ in range(R)]; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'G': cover[i][j] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and cover[a][b] < 0:
                cover[a][b] = cover[i][j] + 1; q.append((a, b))
    best = [[-1] * C for _ in range(R)]; best[0][0] = cover[0][0]
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '#' or (i, j) == (0, 0): continue
            up = best[i - 1][j] if i else -1; left = best[i][j - 1] if j else -1
            m = max(up, left)
            best[i][j] = min(m, cover[i][j]) if m >= 0 else -1
    return best[R - 1][C - 1]
''', 'a table over moves right and down only')

C['walk: cameras cannot be crossed'] = ('ci-safest-walk', '''
import heapq
from collections import deque
def safest_walk(grid):
    R, C = len(grid), len(grid[0]); cover = [[-1] * C for _ in range(R)]; q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'G': cover[i][j] = 0; q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and cover[a][b] < 0:
                cover[a][b] = cover[i][j] + 1; q.append((a, b))
    best = {(0, 0): cover[0][0]}; heap = [(-cover[0][0], 0, 0)]
    while heap:
        s, i, j = heapq.heappop(heap); s = -s
        if (i, j) == (R - 1, C - 1): return s
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and grid[a][b] == '.':
                t = min(s, cover[a][b])
                if t > best.get((a, b), -1):
                    best[(a, b)] = t; heapq.heappush(heap, (-t, a, b))
    return -1
''', 'only open ground walked on')

C['walk: rows scanned for the nearest camera'] = ('ci-safest-walk', '''
import heapq, bisect
def safest_walk(grid):
    R, C = len(grid), len(grid[0])
    cams = [[j for j in range(C) if grid[i][j] == 'G'] for i in range(R)]
    cover = [[10 ** 9] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
            best = 10 ** 9
            for r in range(R):
                dr = abs(r - i)
                if dr >= best: continue
                row = cams[r]
                if not row: continue
                k = bisect.bisect_left(row, j)
                if k < len(row): best = min(best, dr + row[k] - j)
                if k: best = min(best, dr + j - row[k - 1])
            cover[i][j] = best
    best = {(0, 0): cover[0][0]}; heap = [(-cover[0][0], 0, 0)]
    while heap:
        s, i, j = heapq.heappop(heap); s = -s
        if (i, j) == (R - 1, C - 1): return s
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and grid[a][b] != '#':
                t = min(s, cover[a][b])
                if t > best.get((a, b), -1):
                    best[(a, b)] = t; heapq.heappush(heap, (-t, a, b))
    return -1
''', 'covers from a bisect in every row: rows x rows x cols x log')

# ---------------------------------------------------------------- stuck jobs
C['jobs: only the jobs on a loop'] = ('ci-stuck-jobs', '''
def stuck_jobs(n, rules):
    after = [[] for _ in range(n)]; before = [[] for _ in range(n)]
    for a, b in rules:
        after[a].append(b); before[b].append(a)
    def trim(out, inn):
        deg = [len(x) for x in inn]; live = [True] * n
        stack = [j for j in range(n) if deg[j] == 0]
        while stack:
            u = stack.pop(); live[u] = False
            for v in out[u]:
                deg[v] -= 1
                if deg[v] == 0: stack.append(v)
        return live
    f, b = trim(after, before), trim(before, after)
    return [j for j in range(n) if f[j] and b[j]]
''', 'jobs behind a loop left out')

C['jobs: sweep until nothing changes'] = ('ci-stuck-jobs', '''
def stuck_jobs(n, rules):
    ran = [False] * n; changed = True
    before = [[] for _ in range(n)]
    for a, b in rules: before[b].append(a)
    while changed:
        changed = False
        for j in range(n - 1, -1, -1):
            if not ran[j] and all(ran[a] for a in before[j]):
                ran[j] = True; changed = True
    return [j for j in range(n) if not ran[j]]
''', 'sweeps from the top job down until nothing changes')

C['jobs: sweep upwards'] = ('ci-stuck-jobs', '''
def stuck_jobs(n, rules):
    ran = [False] * n; changed = True
    before = [[] for _ in range(n)]
    for a, b in rules: before[b].append(a)
    while changed:
        changed = False
        for j in range(n):
            if not ran[j] and all(ran[a] for a in before[j]):
                ran[j] = True; changed = True
    return [j for j in range(n) if not ran[j]]
''', 'sweeps from job 0 up until nothing changes: quadratic on a chain listed backwards')

C['jobs: recursive, limit raised'] = ('ci-stuck-jobs', '''
import sys
sys.setrecursionlimit(1000000)
def stuck_jobs(n, rules):
    before = [[] for _ in range(n)]
    for a, b in rules: before[b].append(a)
    state = [0] * n
    def ok(j):
        if state[j] == 1: return False
        if state[j]: return state[j] == 2
        state[j] = 1
        good = all(ok(a) for a in before[j])
        state[j] = 2 if good else 3
        return good
    return [j for j in range(n) if not ok(j)]
''', 'memoised recursion with the limit raised: also wrong, a job met while its loop is open is marked for good')

# ---------------------------------------------------------------- two shift rota
C['rota: larger colour overall'] = ('ci-two-shift-rota', '''
from collections import deque
def max_day_shift(n, clashes):
    near = [[] for _ in range(n)]
    for a, b in clashes:
        near[a].append(b); near[b].append(a)
    side = [-1] * n
    for s in range(n):
        if side[s] >= 0: continue
        side[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for w in near[u]:
                if side[w] < 0: side[w] = 1 - side[u]; q.append(w)
                elif side[w] == side[u]: return -1
    return max(side.count(0), side.count(1))
''', 'the larger colour over the whole desk, not group by group')

C['rota: lone staff left out of the count'] = ('ci-two-shift-rota', '''
from collections import deque
def max_day_shift(n, clashes):
    near = [[] for _ in range(n)]
    for a, b in clashes:
        near[a].append(b); near[b].append(a)
    side = [-1] * n; total = 0
    for s in range(n):
        if side[s] >= 0 or not near[s]: continue
        side[s] = 0; cnt = [1, 0]; q = deque([s])
        while q:
            u = q.popleft()
            for w in near[u]:
                if side[w] < 0: side[w] = 1 - side[u]; cnt[side[w]] += 1; q.append(w)
                elif side[w] == side[u]: return -1
        total += max(cnt)
    return total
''', 'staff with no clash not counted')

C['rota: recursive colouring'] = ('ci-two-shift-rota', '''
def max_day_shift(n, clashes):
    near = [[] for _ in range(n)]
    for a, b in clashes:
        near[a].append(b); near[b].append(a)
    side = [-1] * n
    def paint(u, s, cnt):
        side[u] = s; cnt[s] += 1
        for w in near[u]:
            if side[w] < 0:
                if not paint(w, 1 - s, cnt): return False
            elif side[w] == s: return False
        return True
    total = 0
    for s in range(n):
        if side[s] < 0:
            cnt = [0, 0]
            if not paint(s, 0, cnt): return -1
            total += max(cnt)
    return total
''', 'recursive colouring at the default limit')

C['rota: half of each group'] = ('ci-two-shift-rota', '''
def max_day_shift(n, clashes):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    near = [[] for _ in range(n)]
    for a, b in clashes:
        near[a].append(b); near[b].append(a); parent[find(a)] = find(b)
    side = [-1] * n
    for s in range(n):
        if side[s] < 0:
            side[s] = 0; stack = [s]
            while stack:
                u = stack.pop()
                for w in near[u]:
                    if side[w] < 0: side[w] = 1 - side[u]; stack.append(w)
                    elif side[w] == side[u]: return -1
    size = {}
    for x in range(n): size[find(x)] = size.get(find(x), 0) + 1
    return sum((v + 1) // 2 for v in size.values())
''', 'half of each group, rounded up, on days')

# ---------------------------------------------------------------- wall break
C['break: straight through only'] = ('ci-wall-break-route', '''
from collections import deque
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    pos = {grid[i][j]: (i, j) for i in range(R) for j in range(C) if grid[i][j] in 'SE'}
    def spread(src):
        d = {src: 0}; q = deque([src])
        while q:
            i, j = q.popleft()
            for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= p[0] < R and 0 <= p[1] < C and p not in d and grid[p[0]][p[1]] != '#':
                    d[p] = d[(i, j)] + 1; q.append(p)
        return d
    ds, de = spread(pos['S']), spread(pos['E'])
    best = ds.get(pos['E'], -1)
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '#':
                for p, q2 in (((i - 1, j), (i + 1, j)), ((i + 1, j), (i - 1, j)), ((i, j - 1), (i, j + 1)), ((i, j + 1), (i, j - 1))):
                    if p in ds and q2 in de:
                        v = ds[p] + de[q2] + 2
                        if best < 0 or v < best: best = v
    return best
''', 'a wall is crossed only straight through, never round a corner')

C['break: nearest cells summed as one'] = ('ci-wall-break-route', '''
from collections import deque
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    pos = {grid[i][j]: (i, j) for i in range(R) for j in range(C) if grid[i][j] in 'SE'}
    def spread(src):
        d = {src: 0}; q = deque([src])
        while q:
            i, j = q.popleft()
            for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= p[0] < R and 0 <= p[1] < C and p not in d and grid[p[0]][p[1]] != '#':
                    d[p] = d[(i, j)] + 1; q.append(p)
        return d
    ds, de = spread(pos['S']), spread(pos['E'])
    best = ds.get(pos['E'], -1)
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '#':
                near = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                a = [ds[p] for p in near if p in ds]; b = [de[p] for p in near if p in de]
                if a and b:
                    v = min(a) + min(b) + 1
                    if best < 0 or v < best: best = v
    return best
''', 'one move through the wall, not two')

C['break: walls beside S or E missed'] = ('ci-wall-break-route', '''
from collections import deque
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    pos = {grid[i][j]: (i, j) for i in range(R) for j in range(C) if grid[i][j] in 'SE'}
    def spread(src):
        d = {src: 0}; q = deque([src])
        while q:
            i, j = q.popleft()
            for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= p[0] < R and 0 <= p[1] < C and p not in d and grid[p[0]][p[1]] != '#':
                    d[p] = d[(i, j)] + 1; q.append(p)
        return d
    ds, de = spread(pos['S']), spread(pos['E'])
    best = ds.get(pos['E'], -1)
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '#':
                near = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                a = [ds[p] for p in near if ds.get(p)]; b = [de[p] for p in near if de.get(p)]
                if a and b:
                    v = min(a) + min(b) + 2
                    if best < 0 or v < best: best = v
    return best
''', 'a distance of 0 read as "not reached", so a wall touching S or E is skipped')

C['break: per wall, only walls on the frontier'] = ('ci-wall-break-route', '''
from collections import deque
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    pos = {grid[i][j]: (i, j) for i in range(R) for j in range(C) if grid[i][j] in 'SE'}
    def steps(open_cell):
        dist = {pos['S']: 0}; q = deque([pos['S']])
        while q:
            i, j = q.popleft()
            if (i, j) == pos['E']: return dist[(i, j)], dist
            for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= p[0] < R and 0 <= p[1] < C and p not in dist and (grid[p[0]][p[1]] != '#' or p == open_cell):
                    dist[p] = dist[(i, j)] + 1; q.append(p)
        return -1, dist
    best, reach = steps(None)
    walls = set()
    full = {pos['S']}; q = deque([pos['S']])
    while q:
        i, j = q.popleft()
        for p in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= p[0] < R and 0 <= p[1] < C:
                if grid[p[0]][p[1]] == '#': walls.add(p)
                elif p not in full: full.add(p); q.append(p)
    for w in walls:
        d, _ = steps(w)
        if d >= 0 and (best < 0 or d < best): best = d
    return best
''', 'the per-wall search the constraints rule out, limited to walls S can touch')

CANDIDATES = C
