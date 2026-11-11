"""Delta reader's own solutions, pack 5. Written from the briefs, by a method other
than the model's wherever one exists. Used by run.py."""
import heapq
from collections import Counter, deque


# ci-cheapest-route: one Dijkstra whose key is (cost, roads, the route itself).
def cheapest_route(n, roads, src, dst):
    near = [[] for _ in range(n)]
    for a, b, w in roads:
        near[a].append((b, w))
        near[b].append((a, w))
    done = [False] * n
    heap = [(0, 0, (src,))]
    while heap:
        c, h, path = heapq.heappop(heap)
        u = path[-1]
        if done[u]:
            continue
        done[u] = True
        if u == dst:
            return list(path)
        for v, w in near[u]:
            if not done[v]:
                heapq.heappush(heap, (c + w, h + 1, path + (v,)))
    return []


# ci-ferry-timetable: label correcting with a queue (no heap).
def solve_ferry_timetable(text):
    tok = text.split()
    n, m = int(tok[0]), int(tok[1])
    out = [[] for _ in range(n + 1)]
    for k in range(m):
        a, b, t, p = (int(x) for x in tok[2 + 4 * k: 6 + 4 * k])
        out[a].append((b, t, p))
    INF = float('inf')
    best = [INF] * (n + 1)
    best[1] = 0
    q = deque([1])
    inq = [False] * (n + 1)
    inq[1] = True
    while q:
        u = q.popleft()
        inq[u] = False
        now = best[u]
        for b, t, p in out[u]:
            leave = now if now % p == 0 else now + (p - now % p)
            if leave + t < best[b]:
                best[b] = leave + t
                if not inq[b]:
                    inq[b] = True
                    q.append(b)
    return str(best[n]) if best[n] < INF else '-1'


# ci-first-circular-rule: keep a topological order as the rules arrive (Pearce and Kelly).
def first_cycle_rule(n, rules):
    order = list(range(n))          # order[v] = place of v
    fwd = [[] for _ in range(n)]
    back = [[] for _ in range(n)]
    for k, (a, b) in enumerate(rules):
        if a == b:
            return k
        if order[a] > order[b]:
            lo, hi = order[b], order[a]
            # forward from b among places <= hi
            seen_f = {b}
            stack = [b]
            while stack:
                u = stack.pop()
                for v in fwd[u]:
                    if v == a:
                        return k
                    if v not in seen_f and order[v] < hi:
                        seen_f.add(v)
                        stack.append(v)
            seen_b = {a}
            stack = [a]
            while stack:
                u = stack.pop()
                for v in back[u]:
                    if v not in seen_b and order[v] > lo:
                        seen_b.add(v)
                        stack.append(v)
            fl = sorted(seen_f, key=order.__getitem__)
            bl = sorted(seen_b, key=order.__getitem__)
            places = sorted(order[v] for v in fl + bl)
            for v, p in zip(bl + fl, places):
                order[v] = p
        fwd[a].append(b)
        back[b].append(a)
    return -1


# ci-half-fare-route: plain distances from both ends, then the voucher tried on each road.
def _plain(n, near, s):
    INF = float('inf')
    d = [INF] * n
    d[s] = 0
    heap = [(0, s)]
    while heap:
        c, u = heapq.heappop(heap)
        if c > d[u]:
            continue
        for v, w in near[u]:
            if c + w < d[v]:
                d[v] = c + w
                heapq.heappush(heap, (c + w, v))
    return d


def cheapest_with_coupon(n, roads, src, dst):
    near = [[] for _ in range(n)]
    for a, b, w in roads:
        near[a].append((b, w))
        near[b].append((a, w))
    ds = _plain(n, near, src)
    dt = _plain(n, near, dst)
    best = ds[dst]
    for a, b, w in roads:
        if a == src or b == src:
            continue
        best = min(best, ds[a] + w // 2 + dt[b], ds[b] + w // 2 + dt[a])
    return -1 if best == float('inf') else best


# ci-island-shapes: fill with a stack, name a shape by its sorted cells moved to the corner.
def lone_shapes(grid):
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    tally = Counter()
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#' and not seen[r][c]:
                seen[r][c] = True
                cells = [(r, c)]
                i = 0
                while i < len(cells):
                    y, x = cells[i]
                    i += 1
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < R and 0 <= nx < C and grid[ny][nx] == '#' and not seen[ny][nx]:
                            seen[ny][nx] = True
                            cells.append((ny, nx))
                my = min(y for y, _ in cells)
                mx = min(x for _, x in cells)
                tally[tuple(sorted((y - my, x - mx) for y, x in cells))] += 1
    return sum(1 for v in tally.values() if v == 1)


# ci-loop-cables: group labels with member lists, the smaller list rewritten.
def loop_cables(n, cables):
    label = list(range(n))
    members = {}
    out = []
    for k, (a, b) in enumerate(cables):
        la, lb = label[a], label[b]
        if la == lb:
            out.append(k)
            continue
        ma = members.pop(la, None) or [a]
        mb = members.pop(lb, None) or [b]
        if len(ma) < len(mb):
            ma, mb, la, lb = mb, ma, lb, la
        for x in mb:
            label[x] = la
        ma.extend(mb)
        members[la] = ma
    return out


# ci-reclaimed-land: the same small-to-large lists on the grid.
def largest_after_each(rows, cols, fills):
    label = {}
    members = {}
    best = 0
    out = []
    for r, c in fills:
        if (r, c) not in label:
            label[(r, c)] = (r, c)
            members[(r, c)] = [(r, c)]
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in label:
                    la, lb = label[(r, c)], label[nb]
                    if la != lb:
                        ma, mb = members[la], members[lb]
                        if len(ma) < len(mb):
                            ma, mb, la, lb = mb, ma, lb, la
                        for x in mb:
                            label[x] = la
                        ma.extend(mb)
                        del members[lb]
            best = max(best, len(members[label[(r, c)]]))
        out.append(best)
    return out


# ci-stuck-jobs: depth-first over "waits for", a job is stuck when it meets a job
# still open or a stuck job.
def stuck_jobs(n, rules):
    waits = [[] for _ in range(n)]
    for a, b in rules:
        waits[b].append(a)
    state = [0] * n      # 0 new, 1 open, 2 runs, 3 stuck
    for s in range(n):
        if state[s]:
            continue
        state[s] = 1
        stack = [(s, 0, False)]
        while stack:
            u, i, bad = stack.pop()
            pushed = False
            while i < len(waits[u]):
                v = waits[u][i]
                i += 1
                if state[v] == 0:
                    state[v] = 1
                    stack.append((u, i, bad))
                    stack.append((v, 0, False))
                    pushed = True
                    break
                if state[v] in (1, 3):
                    bad = True
            if pushed:
                continue
            state[u] = 3 if bad else 2
            if stack and state[u] == 3:
                pu, pi, pb = stack.pop()
                stack.append((pu, pi, True))
    return [v for v in range(n) if state[v] == 3]


# ci-two-shift-rota: union-find with a parity to the root.
def max_day_shift(n, clashes):
    parent = list(range(n))
    par = [0] * n

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        # fold parities from the top down
        p = 0
        for y in reversed(path):
            p ^= par[y]
            par[y] = p
            parent[y] = x
        return x

    for a, b in clashes:
        ra, rb = find(a), find(b)
        if ra == rb:
            if par[a] == par[b]:
                return -1
        else:
            parent[ra] = rb
            par[ra] = par[a] ^ par[b] ^ 1
    side = {}
    for v in range(n):
        r = find(v)
        side.setdefault(r, [0, 0])[par[v] if v != r else 0] += 1
    return sum(max(s) for s in side.values())


# ci-wall-break-route: one search over (cell, wall already knocked).
def fewest_moves_one_break(grid):
    R, C = len(grid), len(grid[0])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                s = (r, c)
            if grid[r][c] == 'E':
                e = (r, c)
    dist = {(s[0], s[1], 0): 0}
    q = deque([(s[0], s[1], 0)])
    while q:
        r, c, k = q.popleft()
        d = dist[(r, c, k)]
        if (r, c) == e:
            return d
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C:
                nk = k + (grid[nr][nc] == '#')
                if nk <= 1 and (nr, nc, nk) not in dist:
                    dist[(nr, nc, nk)] = d + 1
                    q.append((nr, nc, nk))
    return -1


# ci-nearest-depot: one search level by level, each cell keeping the set of firms
# that reach it first.
def depot_shares(grid):
    R, C = len(grid), len(grid[0])
    mask = {}
    level = {}
    for r in range(R):
        for c in range(C):
            if grid[r][c] in 'AB':
                level[(r, c)] = 1 if grid[r][c] == 'A' else 2
    while level:
        mask.update(level)
        nxt = {}
        for (r, c), m in level.items():
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and (nr, nc) not in mask:
                    nxt[(nr, nc)] = nxt.get((nr, nc), 0) | m
        level = nxt
    a = sum(1 for (r, c), m in mask.items() if grid[r][c] == '.' and m == 1)
    b = sum(1 for (r, c), m in mask.items() if grid[r][c] == '.' and m == 2)
    return [a, b]
