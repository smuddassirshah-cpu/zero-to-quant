"""Check for drill sub-pack D (pack dsa): graphs, dp, greedy, backtracking.

For every drill it runs the model solution on every example and hidden test, and an
independent method written here (brute force on small inputs; on the large inputs, where
brute force cannot finish, a different algorithm or a closed form). Both must equal every
`expect`. It also checks that the starter fails at least one test, the difficulty and stdin
mix, and that no case uses `setup`. Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-dsa-d-check.py
"""
import heapq, json, os, random, sys
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
MOD = 1_000_000_007

# ---------------- independent methods ----------------

def solve_lift_buttons(text):
    n, s, g, u, d = map(int, text.split())
    if n <= 2000:  # Bellman-Ford style relaxation over all floors until nothing changes
        INF = float("inf")
        dist = [INF] * (n + 1)
        dist[s] = 0
        changed = True
        while changed:
            changed = False
            for x in range(1, n + 1):
                if dist[x] < INF:
                    for y in (x + u, x - d):
                        if 1 <= y <= n and dist[x] + 1 < dist[y]:
                            dist[y] = dist[x] + 1
                            changed = True
        return str(dist[g] if dist[g] < INF else -1)
    seen, frontier, steps = {s}, {s}, 0  # layer by layer with sets
    while frontier:
        if g in frontier:
            return str(steps)
        nxt = set()
        for x in frontier:
            for y in (x + u, x - d):
                if 1 <= y <= n and y not in seen:
                    seen.add(y)
                    nxt.add(y)
        frontier, steps = nxt, steps + 1
    return "-1"

def spare_cable_moves(n, cables):
    parent = list(range(n))  # union-find with path halving
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    groups = n
    for a, b in cables:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1
    return groups - 1 if len(cables) >= n - 1 else -1

def fewest_climb_steps(heights, climb):
    rows, cols = len(heights), len(heights[0])
    def moves(r, c):
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and heights[nr][nc] - heights[r][c] <= climb:
                yield nr, nc
    INF = float("inf")
    if rows * cols <= 100:  # relax every edge until stable
        dist = {(r, c): INF for r in range(rows) for c in range(cols)}
        dist[(0, 0)] = 0
        changed = True
        while changed:
            changed = False
            for (r, c), v in list(dist.items()):
                if v < INF:
                    for cell in moves(r, c):
                        if v + 1 < dist[cell]:
                            dist[cell] = v + 1
                            changed = True
        v = dist[(rows - 1, cols - 1)]
        return v if v < INF else -1
    dist = {(0, 0): 0}  # Dijkstra with unit weights
    heap = [(0, 0, 0)]
    while heap:
        v, r, c = heapq.heappop(heap)
        if v > dist[(r, c)]:
            continue
        for cell in moves(r, c):
            if v + 1 < dist.get(cell, INF):
                dist[cell] = v + 1
                heapq.heappush(heap, (v + 1, *cell))
    return dist.get((rows - 1, cols - 1), -1)

def route_stations(n, pipes, s, r):
    # a station is on a route when s reaches it and it reaches r: test every station pair by its own search
    if n <= 50:
        adj = [[] for _ in range(n)]
        for a, b in pipes:
            adj[a].append(b)

        def reaches(u, v):
            seen, stack = {u}, [u]
            while stack:
                x = stack.pop()
                for y in adj[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            return v in seen
        return [v for v in range(n) if reaches(s, v) and reaches(v, r)]
    # SciPy's breadth-first order forward from s and on the reversed pipes from r
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import breadth_first_order
    if not pipes:
        return []
    src = np.array([a for a, b in pipes]); dst = np.array([b for a, b in pipes])
    fwd = csr_matrix((np.ones(len(pipes)), (src, dst)), shape=(n, n))
    from_s = set(int(v) for v in breadth_first_order(fwd, s, directed=True, return_predecessors=False))
    to_r = set(int(v) for v in breadth_first_order(fwd.T.tocsr(), r, directed=True, return_predecessors=False))
    return sorted(from_s & to_r)

def forced_order(n, deps):
    if n <= 7:  # list every order that obeys the rules
        good = [p for p in permutations(range(n))
                if all(p.index(a) < p.index(b) for a, b in deps)]
        return list(good[0]) if len(good) == 1 else None
    adj = [[] for _ in range(n)]  # DFS post-order topological sort, then a Hamiltonian-path test
    edges = set()
    for a, b in deps:
        adj[a].append(b)
        edges.add((a, b))
    state, post = [0] * n, []
    for s in range(n):
        if state[s]:
            continue
        state[s] = 1
        stack = [(s, 0)]
        while stack:
            v, i = stack.pop()
            if i < len(adj[v]):
                stack.append((v, i + 1))
                w = adj[v][i]
                if state[w] == 1:
                    return None  # back edge: a loop
                if state[w] == 0:
                    state[w] = 1
                    stack.append((w, 0))
            else:
                state[v] = 2
                post.append(v)
    order = post[::-1]
    return order if all((order[i], order[i + 1]) in edges for i in range(n - 1)) else None

def footpath_ways(n):
    if n <= 12:  # fill the first empty cell of a real 2-by-n grid in every possible way
        def count(filled):
            if len(filled) == 2 * n:
                return 1
            r, c = min(((r, c) for c in range(n) for r in range(2) if (r, c) not in filled), key=lambda t: (t[1], t[0]))
            total = 0
            shapes = [{(r, c), (r, c + 1)}, {(r, c), (r + 1, c)}, {(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)}]
            for cells in shapes:
                if all(0 <= rr < 2 and 0 <= cc < n and (rr, cc) not in filled for rr, cc in cells):
                    total += count(filled | cells)
            return total
        return count(frozenset())
    # closed form (2^(n+1) + (-1)^n) / 3, the Jacobsthal numbers
    return (pow(2, n + 1, MOD) + (1 if n % 2 == 0 else -1)) * pow(3, MOD - 2, MOD) % MOD

def unpayable_totals(stamps, limit):
    reach = 1  # bit t set when total t can be made; add stamps one value at a time
    mask = (1 << (limit + 1)) - 1
    for s in set(stamps):
        if s > limit:
            continue
        step = reach
        while True:
            new = (reach | (reach << s)) & mask
            if new == reach:
                break
            reach = new
    got = bin(reach).count("1") - 1
    if limit <= 100 and stamps:  # cross-check by listing sums of up to limit stamps
        sums = {0}
        for _ in range(limit):
            sums = sums | {x + s for x in sums for s in stamps if x + s <= limit}
        assert len(sums) - 1 == got
    return limit - got

def solve_shift_pay(text):
    data = text.split()
    n = int(data[0])
    pay = list(map(int, data[1:1 + n]))
    if n <= 16:  # every set of working days
        best = 0
        for mask in range(1 << n):
            if all(not (mask >> i & 7 == 7) for i in range(n)):
                best = max(best, sum(p for i, p in enumerate(pay) if mask >> i & 1))
        return str(best)
    # the rest-day view: pay given up is least when rests are at most 3 apart
    INF = float("inf")
    lost = [INF] * (n + 2)  # lost[i]: least pay given up with a rest on day i - 1 (day -1 virtual)
    lost[0] = 0
    ext = pay + [0]  # a virtual rest after the last day
    for i in range(1, n + 2):
        lost[i] = ext[i - 1] + min(lost[j] for j in range(max(0, i - 3), i))
    return str(sum(pay) - lost[n + 1])

def solve_feed_passes(text):
    data = list(map(int, text.split()))
    n, prices = data[0], data[1:4]
    days = data[4:4 + n]
    lengths = (1, 7, 30)
    if n <= 12:  # plain recursion over the pass bought at each uncovered day
        def go(i):
            if i == n:
                return 0
            best = INF = float("inf")
            for p, L in zip(prices, lengths):
                j = i
                while j < n and days[j] < days[i] + L:
                    j += 1
                best = min(best, p + go(j))
            return best
        return str(go(0))
    if days[-1] <= 2_000_000:  # a table over every calendar day
        need = bytearray(days[-1] + 31)
        for d in days:
            need[d] = 1
        cost = [0] * (days[-1] + 31)
        for t in range(1, days[-1] + 1):
            if not need[t]:
                cost[t] = cost[t - 1]
            else:
                cost[t] = min(p + cost[max(0, t - L)] for p, L in zip(prices, lengths))
        return str(cost[days[-1]])
    # forward DP over needed days with three moving pointers
    best = [float("inf")] * (n + 1)
    best[0] = 0
    ptr = [0, 0, 0]
    for i in range(n):  # best[i] final; push forward
        for k, (p, L) in enumerate(zip(prices, lengths)):
            if ptr[k] < i:
                ptr[k] = i
            while ptr[k] < n and days[ptr[k]] < days[i] + L:
                ptr[k] += 1
            best[ptr[k]] = min(best[ptr[k]], best[i] + p)
    return str(best[n])

def largest_free_square(plan):
    rows, cols = len(plan), len(plan[0])
    if rows * cols <= 100:  # test every square
        best = 0
        for r in range(rows):
            for c in range(cols):
                s = 1
                while r + s <= rows and c + s <= cols and all(plan[rr][cc] == "." for rr in range(r, r + s) for cc in range(c, c + s)):
                    best = max(best, s)
                    s += 1
        return best
    taken = np.array([[ch == "#" for ch in row] for row in plan], dtype=np.int64)
    P = np.zeros((rows + 1, cols + 1), dtype=np.int64)
    P[1:, 1:] = taken.cumsum(0).cumsum(1)
    def fits(s):  # some s-by-s window holds no taken desk
        w = P[s:, s:] - P[:-s, s:] - P[s:, :-s] + P[:-s, :-s]
        return bool((w == 0).any())
    lo, hi = 0, min(rows, cols)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

def first_short_change(notes):
    states = {(0, 0)}  # every reachable (fives, tens) after each customer, trying all change choices
    for i, note in enumerate(notes):
        nxt = set()
        for f, t in states:
            if note == 5:
                nxt.add((f + 1, t))
            elif note == 10:
                if f:
                    nxt.add((f - 1, t + 1))
            else:
                if f and t:
                    nxt.add((f - 1, t - 1))
                if f >= 3:
                    nxt.add((f - 3, t))
        if not nxt:
            return i
        states = nxt
    return -1

def loop_start_depot(fuel, burn):
    n = len(fuel)
    if n <= 2000:  # drive the loop from every depot
        for s in range(n):
            tank, ok = 0, True
            for j in range(n):
                i = (s + j) % n
                tank += fuel[i] - burn[i]
                if tank < 0:
                    ok = False
                    break
            if ok:
                return s
        return -1
    if sum(fuel) < sum(burn):
        return -1
    pre = np.concatenate(([0], np.cumsum(np.array(fuel, dtype=np.int64) - np.array(burn, dtype=np.int64))))[:n]
    return int(np.argmin(pre))  # smallest index of the lowest prefix total

def ticker_batches(tape):
    n = len(tape)
    if n <= 12:  # every set of cuts; keep the valid one with most batches
        best = None
        for m in range(1 << max(n - 1, 0)):
            cuts = [0] + [i + 1 for i in range(n - 1) if m >> i & 1] + [n]
            pieces = [tape[a:b] for a, b in zip(cuts, cuts[1:]) if b > a]
            sets = [set(p) for p in pieces]
            if all(not (sets[i] & sets[j]) for i in range(len(sets)) for j in range(i + 1, len(sets))):
                if best is None or len(pieces) > len(best):
                    best = pieces
        return [len(p) for p in best] if n else []
    first, last = {}, {}
    for i, ch in enumerate(tape):
        first.setdefault(ch, i)
        last[ch] = i
    cover = [0] * (n + 1)  # a cut before position p is blocked when some ticker spans it
    for ch in first:
        cover[first[ch] + 1] += 1
        cover[last[ch] + 1] -= 1
    cuts, run = [], 0
    for p in range(1, n):
        run += cover[p]
        if run == 0:
            cuts.append(p)
    edges = [0] + cuts + [n]
    return [b - a for a, b in zip(edges, edges[1:])]

def split_prices(digits, k, cap):
    n = len(digits)
    ok = lambda s: s[0] != "0" and 1 <= int(s) <= cap
    if n <= 20:  # every choice of k - 1 cut points
        out = []
        for cuts in combinations(range(1, n), k - 1):
            e = (0,) + cuts + (n,)
            pieces = [digits[a:b] for a, b in zip(e, e[1:])]
            if all(ok(p) for p in pieces):
                out.append([int(p) for p in pieces])
        return sorted(out)
    @lru_cache(maxsize=None)
    def suffix(pos, left):  # every split of digits[pos:] into `left` prices
        if left == 0:
            return [[]] if pos == n else []
        res = []
        for end in range(pos + 1, n + 1):
            if end - pos > len(str(cap)):
                break
            if ok(digits[pos:end]):
                res += [[int(digits[pos:end])] + rest for rest in suffix(end, left - 1)]
        return res
    return sorted(suffix(0, k))

def min_peak_load(jobs, k):
    n = len(jobs)
    if n == 0:
        return 0
    if k ** n <= 200_000:  # every assignment
        return min(max(sum(j for j, s in zip(jobs, a) if s == srv) for srv in range(k)) for a in product(range(k), repeat=n))
    sums = [0] * (1 << n)
    for m in range(1, 1 << n):
        low = (m & -m).bit_length() - 1
        sums[m] = sums[m & (m - 1)] + jobs[low]
    def fits(cap):  # fewest servers for each set of jobs, by subset DP
        INF = n + 1
        need = [INF] * (1 << n)
        need[0] = 0
        for m in range(1, 1 << n):
            sub = m
            while sub:
                if sums[sub] <= cap and need[m ^ sub] + 1 < need[m]:
                    need[m] = need[m ^ sub] + 1
                sub = (sub - 1) & m
        return need[-1] <= k
    lo, hi = max(jobs), sum(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

INDEP = {f.__name__: f for f in [solve_lift_buttons, spare_cable_moves, fewest_climb_steps, route_stations,
                                  forced_order, footpath_ways, unpayable_totals, solve_shift_pay, solve_feed_passes,
                                  largest_free_square, first_short_change, loop_start_depot, ticker_batches,
                                  split_prices, min_peak_load]}
MINE = ["dsa-lift-buttons", "dsa-spare-cables", "dsa-climb-limit", "dsa-upstream-stations", "dsa-forced-order",
        "dsa-footpath-slabs", "dsa-stamp-gaps", "dsa-shift-pay", "dsa-feed-passes", "dsa-free-desk-square",
        "dsa-kiosk-change", "dsa-loop-depots", "dsa-ticker-batches", "dsa-split-prices", "dsa-server-loads"]

# Worked by hand, as a third check on small cases:
#   footpath_ways(3) = ways(2) + 2 ways(1) = 3 + 2 = 5, and ways(4) = 5 + 2 * 3 = 11.
#   unpayable_totals([3, 5], 10): makeable 3, 5, 6, 8, 9, 10, so 1, 2, 4, 7 are not: 4.
#   loop_start_depot([1, 5, 2, 4], [3, 2, 4, 1]): from depot 1 the tank reads 3, 1, 4, 2: answer 1.
#   min_peak_load([3, 5, 2, 7, 4], 2): ceil(21 / 2) = 11, reached by {7, 4} and {5, 3, 2}.
HAND = {"footpath_ways(3)": 5, "footpath_ways(4)": 11, "unpayable_totals([3, 5], 10)": 4,
        "loop_start_depot([1, 5, 2, 4], [3, 2, 4, 1])": 1, "min_peak_load([3, 5, 2, 7, 4], 2)": 11,
        "solve_shift_pay('5\\n4 7 3 6 2\\n')": "19", "solve_feed_passes('5 3 10 25\\n1 2 3 4 30\\n')": "13",
        "ticker_batches('ABACDDCE')": [3, 4, 1], "first_short_change([5, 5, 10, 20, 20])": 4}

# ---------------- random small-input stress for the drills replaced or extended in the fix pass ----------------

def stress(models):
    rng = random.Random(7)
    bad = 0
    for _ in range(1500):  # route_stations against every ordered pair reachability
        n = rng.randrange(2, 9)
        pipes = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(0, 14))]
        s, r = rng.sample(range(n), 2)
        reach = [[i == j for j in range(n)] for i in range(n)]
        for a, b in pipes:
            reach[a][b] = True
        for m in range(n):
            for i in range(n):
                for j in range(n):
                    reach[i][j] = reach[i][j] or (reach[i][m] and reach[m][j])
        want = [v for v in range(n) if reach[s][v] and reach[v][r]]
        if models["route_stations"](n, pipes, s, r) != want:
            bad += 1
    for _ in range(1500):  # first_short_change against every change choice
        notes = [rng.choice([5, 5, 10, 20]) for _ in range(rng.randrange(0, 12))]
        if models["first_short_change"](notes) != first_short_change(notes):
            bad += 1
    for _ in range(1500):  # split_prices against every cut set
        digits = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 9)))
        k = rng.randrange(1, 6)
        cap = rng.choice([9, 50, 99, 255, 999])
        if models["split_prices"](digits, k, cap) != split_prices(digits, k, cap):
            bad += 1
    print(f"random stress: {bad} mismatches")
    return bad

# ---------------- runner ----------------

def run(code, call, extra=None):
    ns = dict(extra or {})
    if code is not None:
        exec(code, ns)
    return eval(call, ns)

def same(a, b):
    return type(a) == type(b) and a == b

def main():
    sys.setrecursionlimit(10000)
    errors = 0
    diffs, stdin, hand_seen = Counter(), 0, set()
    models = {}
    for did in MINE:
        d = json.load(open(os.path.join(DRILLS, did + ".json")))
        fn = d["fn"]
        ns = {}
        exec(d["solution"], ns)
        models[fn] = ns[fn]
        diffs[d["difficulty"]] += 1
        stdin += "stdin" in d.get("tags", [])
        if "stdin" in d.get("tags", []):
            assert fn.startswith("solve_"), did
        assert d["pack"] == "dsa" and 480 <= d["pace"] <= 1500, did
        assert d["pattern"] in ("graphs", "dp", "greedy", "backtracking"), did
        assert 10 <= len(d["tests"]) <= 14 and 2 <= len(d["examples"]) <= 3, did
        assert all(e.get("note") for e in d["examples"]) and len(d["notes"]) == 3, did
        assert not any("setup" in c for c in d["tests"] + d["examples"]), did  # the drill page ignores setup
        assert d["how"].startswith(f"Submit runs {len(d['tests'])} hidden tests"), did
        starter_fails = 0
        for kind, cases in (("example", d["examples"]), ("test", d["tests"])):
            for i, c in enumerate(cases):
                want = eval(c["expect"])
                got = run(d["solution"], c["call"])
                if not same(got, want):
                    print(f"FAIL {did} {kind} {i}: solution gave {got!r:.60}, expect {want!r:.60}"); errors += 1
                indep = run(None, c["call"], {fn: INDEP[fn]})
                if not same(indep, want):
                    print(f"FAIL {did} {kind} {i}: independent gave {indep!r:.60}, expect {want!r:.60}"); errors += 1
                if c["call"] in HAND:
                    hand_seen.add(c["call"])
                    if not same(HAND[c["call"]], want):
                        print(f"FAIL {did} {kind} {i}: hand value {HAND[c['call']]!r}, expect {want!r}"); errors += 1
                if kind == "test":
                    try:
                        starter_fails += not same(run(d["starter"], c["call"]), want)
                    except Exception:
                        starter_fails += 1
        if starter_fails == 0:
            print(f"FAIL {did}: starter passes every test"); errors += 1
        print(f"ok {did}: {len(d['examples'])} examples, {len(d['tests'])} tests, starter fails {starter_fails}")
    if set(HAND) != hand_seen:
        print(f"FAIL hand values not found: {set(HAND) - hand_seen}"); errors += 1
    if diffs != Counter({1: 5, 2: 6, 3: 4}) or stdin != 3:
        print(f"FAIL mix: difficulties {dict(diffs)}, stdin {stdin}"); errors += 1
    errors += stress(models)
    print(f"{len(MINE)} drills, {errors} errors")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
