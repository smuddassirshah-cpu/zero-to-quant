"""Second reader's own solutions to drill pack 5, written from the briefs
before the model solutions were read. A different method from the hint
wherever one exists."""
import heapq
from collections import deque


# ci-cheapest-route: one Dijkstra whose key is (cost, roads, the route itself)
def cheapest_route(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c))
        adj[b].append((a, c))
    best = {}
    heap = [(0, 0, (src,))]
    while heap:
        cost, hops, path = heapq.heappop(heap)
        u = path[-1]
        if u in best:
            continue
        best[u] = path
        if u == dst:
            return list(path)
        for v, c in adj[u]:
            if v not in best:
                heapq.heappush(heap, (cost + c, hops + 1, path + (v,)))
    return []


# ci-checkpoint-route: one search over (cell, scanned yet)
def solve_checkpoint_route(text):
    tok = text.split()
    r, c = int(tok[0]), int(tok[1])
    g = tok[2:2 + r]
    for i in range(r):
        for j in range(c):
            if g[i][j] == 'S':
                s = (i, j)
    start = (s[0], s[1], 0)
    seen = {start}
    q = deque([(start, 0)])
    while q:
        (i, j, k), d = q.popleft()
        if g[i][j] == 'C':
            k2 = 1
            if (i, j, 1) not in seen:
                seen.add((i, j, 1))
            k = 1
        if g[i][j] == 'E' and k == 1:
            return str(d)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < r and 0 <= b < c and g[a][b] != '#' and (a, b, k) not in seen:
                seen.add((a, b, k))
                q.append(((a, b, k), d + 1))
    return '-1'


# ci-ferry-timetable: Dijkstra on arrival minutes
def solve_ferry_timetable(text):
    tok = text.split()
    n, m = int(tok[0]), int(tok[1])
    adj = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = (int(x) for x in tok[2 + 4 * k:6 + 4 * k])
        adj[a].append((b, t, p))
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[1] = 0
    heap = [(0, 1)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == n:
            return str(d)
        for v, t, p in adj[u]:
            nd = d + (-d) % p + t
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return '-1'


# ci-first-circular-rule: binary search on the prefix, loop test by an
# iterative three-colour depth-first search
def _has_loop(n, rules, k):
    adj = [[] for _ in range(n)]
    for a, b in rules[:k]:
        if a == b:
            return True
        adj[a].append(b)
    colour = [0] * n
    for s in range(n):
        if colour[s]:
            continue
        colour[s] = 1
        stack = [(s, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if colour[v] == 1:
                    return True
                if colour[v] == 0:
                    colour[v] = 1
                    stack.append((v, 0))
            else:
                colour[u] = 2
                stack.pop()
    return False


def first_cycle_rule(n, rules):
    m = len(rules)
    if not _has_loop(n, rules, m):
        return -1
    lo, hi = 1, m          # smallest k with a loop in the first k rules
    while lo < hi:
        mid = (lo + hi) // 2
        if _has_loop(n, rules, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo - 1


# ci-flood-reach: queue
def wet_cells(heights, r, c):
    R, C = len(heights), len(heights[0])
    seen = [[False] * C for _ in range(R)]
    seen[r][c] = True
    q = deque([(r, c)])
    count = 0
    while q:
        i, j = q.popleft()
        count += 1
        h = heights[i][j]
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and not seen[a][b] and heights[a][b] <= h:
                seen[a][b] = True
                q.append((a, b))
    return count


# ci-half-fare-route: Dijkstra from both ends, then try the voucher on each road
def _dij(n, adj, s):
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, c in adj[u]:
            if d + c < dist[v]:
                dist[v] = d + c
                heapq.heappush(heap, (d + c, v))
    return dist


def cheapest_with_coupon(n, roads, src, dst):
    adj = [[] for _ in range(n)]
    for a, b, c in roads:
        adj[a].append((b, c))
        adj[b].append((a, c))
    ds = _dij(n, adj, src)
    dt = _dij(n, adj, dst)
    best = ds[dst]
    if best == float('inf'):
        return -1
    for a, b, c in roads:
        best = min(best, ds[a] + c // 2 + dt[b], ds[b] + c // 2 + dt[a])
    return best


# ci-island-shapes: shape as the sorted cells shifted to their bounding box
def lone_shapes(grid):
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    count = {}
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '#' and not seen[i][j]:
                seen[i][j] = True
                q = deque([(i, j)])
                cells = []
                while q:
                    a, b = q.popleft()
                    cells.append((a, b))
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < R and 0 <= y < C and grid[x][y] == '#' and not seen[x][y]:
                            seen[x][y] = True
                            q.append((x, y))
                mr = min(a for a, _ in cells)
                mc = min(b for _, b in cells)
                key = tuple(sorted((a - mr, b - mc) for a, b in cells))
                count[key] = count.get(key, 0) + 1
    return sum(1 for v in count.values() if v == 1)


# ci-line-from-pairs
def rebuild_line(pairs):
    nb = {}
    for x, y in pairs:
        nb.setdefault(x, []).append(y)
        nb.setdefault(y, []).append(x)
    start = min(s for s in nb if len(nb[s]) == 1)
    out = [start]
    prev = None
    cur = start
    while True:
        nxt = [s for s in nb[cur] if s != prev]
        if not nxt:
            break
        prev, cur = cur, nxt[0]
        out.append(cur)
    return out


# ci-loop-cables: union by size, path halving
def loop_cables(n, cables):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []
    for i, (a, b) in enumerate(cables):
        ra, rb = find(a), find(b)
        if ra == rb:
            out.append(i)
        else:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    return out


# ci-nearest-depot: two multi-source searches
def depot_shares(grid):
    R, C = len(grid), len(grid[0])

    def bfs(ch):
        dist = [[-1] * C for _ in range(R)]
        q = deque()
        for i in range(R):
            for j in range(C):
                if grid[i][j] == ch:
                    dist[i][j] = 0
                    q.append((i, j))
        while q:
            i, j = q.popleft()
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R and 0 <= b < C and grid[a][b] != '#' and dist[a][b] < 0:
                    dist[a][b] = dist[i][j] + 1
                    q.append((a, b))
        return dist

    da, db = bfs('A'), bfs('B')
    a = b = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] == '.':
                x, y = da[i][j], db[i][j]
                if x >= 0 and (y < 0 or x < y):
                    a += 1
                elif y >= 0 and (x < 0 or y < x):
                    b += 1
    return [a, b]


# ci-reclaimed-land: union-find keyed by cell in a dict
def largest_after_each(rows, cols, fills):
    parent = {}
    size = {}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    best = 0
    out = []
    for r, c in fills:
        key = (r, c)
        if key not in parent:
            parent[key] = key
            size[key] = 1
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in parent:
                    ra, rb = find(key), find(nb)
                    if ra != rb:
                        if size[ra] < size[rb]:
                            ra, rb = rb, ra
                        parent[rb] = ra
                        size[ra] += size[rb]
            best = max(best, size[find(key)])
        out.append(best)
    return out


# ci-safest-walk: covers by multi-source search, then open cells from the
# highest cover down, joining with union-find until the corners meet
def safest_walk(grid):
    R, C = len(grid), len(grid[0])
    cover = [[-1] * C for _ in range(R)]
    q = deque()
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'G':
                cover[i][j] = 0
                q.append((i, j))
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and cover[a][b] < 0:
                cover[a][b] = cover[i][j] + 1
                q.append((a, b))
    cells = sorted(((cover[i][j], i, j) for i in range(R) for j in range(C) if grid[i][j] != '#'), reverse=True)
    parent = list(range(R * C))
    opened = [False] * (R * C)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    last = R * C - 1
    for cv, i, j in cells:
        k = i * C + j
        opened[k] = True
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and opened[a * C + b]:
                parent[find(k)] = find(a * C + b)
        if opened[0] and opened[last] and find(0) == find(last):
            return cv
    return -1


# ci-stuck-jobs: waiting counts, a stack instead of a queue
def stuck_jobs(n, rules):
    wait = [0] * n
    out = [[] for _ in range(n)]
    for a, b in rules:
        wait[b] += 1
        out[a].append(b)
    stack = [j for j in range(n) if wait[j] == 0]
    ran = [False] * n
    while stack:
        u = stack.pop()
        ran[u] = True
        for v in out[u]:
            wait[v] -= 1
            if wait[v] == 0:
                stack.append(v)
    return [j for j in range(n) if not ran[j]]


# ci-two-shift-rota: union-find with a parity to the root
def max_day_shift(n, clashes):
    parent = list(range(n))
    par = [0] * n          # parity of x against parent[x]

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        p = 0
        for y in reversed(path):
            p ^= par[y]
            par[y] = p
            parent[y] = root
        return root

    for a, b in clashes:
        ra, rb = find(a), find(b)
        if ra == rb:
            if par[a] == par[b]:
                return -1
        else:
            parent[ra] = rb
            par[ra] = par[a] ^ par[b] ^ 1
    side = {}
    for x in range(n):
        r = find(x)
        s = side.setdefault(r, [0, 0])
        s[par[x] if x != r else 0] += 1
    return sum(max(s) for s in side.values())


# ci-wall-break-route: one search over (cell, wall already knocked)
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    for i in range(R):
        for j in range(C):
            if grid[i][j] == 'S':
                s = (i, j)
    seen = [[[False, False] for _ in range(C)] for _ in range(R)]
    seen[s[0]][s[1]][0] = True
    q = deque([(s[0], s[1], 0, 0)])
    while q:
        i, j, k, d = q.popleft()
        if grid[i][j] == 'E':
            return d
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C:
                k2 = k + (grid[a][b] == '#')
                if k2 <= 1 and not seen[a][b][k2]:
                    seen[a][b][k2] = True
                    q.append((a, b, k2, d + 1))
    return -1
