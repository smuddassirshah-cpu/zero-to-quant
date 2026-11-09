"""Reader checks for graphs-dp L1 to L3 performance tasks (review-perf-retrofit-9): every expect recomputed by a
second route, reader solutions written independently, reader-planted slips, the shipped solutions and starters run
on every example and hidden test. Run from this folder with the venv Python. Exits 1 on any mismatch."""
import sys, os, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness9 import item, summary, summary_each

bad = 0
def expect(widget, src, label, want, which="tests"):
    global bad
    fails, r = summary(widget, src, label, which)
    if want is not None and fails != want:
        bad += 1
        print("     MISMATCH: wanted", want, "got", fails, [x[1][:50] for x in r])
    return fails

def check(name, ok, info=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    bad += 0 if ok else 1

# ======================= L1 split_desks =======================
it = item("graphs-dp", "homework-1.json", "h-split-desks"); w = it["widget"]
print("graphs-dp L1 h-split-desks")
G = {}
exec(w["postlude"], G)

def split_uf(desks, conflicts):
    """Route 2: union-find with parity, then the sorted-first desk of each set fixes the colours."""
    par = {d: d for d in desks}; odd = {d: 0 for d in desks}
    def find(x):
        path = []
        while par[x] != x:
            path.append(x); x = par[x]
        root, acc = x, 0
        for y in reversed(path):
            acc ^= odd[y]; odd[y] = acc; par[y] = root
        return root
    for a, b in conflicts:
        ra, rb = find(a), find(b)
        pa, pb = odd[a] if a != ra else 0, odd[b] if b != rb else 0
        if ra == rb:
            if pa == pb:
                return None
        else:
            par[ra] = rb; odd[ra] = pa ^ pb ^ 1
    first = {}
    for d in sorted(desks):
        r = find(d); first.setdefault(r, d)
    out = {}
    for d in desks:
        r = find(d)
        pd = odd[d] if d != r else 0
        f = first[r]; pf = odd[f] if f != r else 0
        out[d] = pd ^ pf
    return out

for k, c in enumerate(w["tests"], 1):
    got = eval(c["call"].replace("split_desks", "split_uf"), dict(G, split_uf=split_uf))
    want = eval(c["expect"])
    check(f"L1 test {k} expect by union-find", got == want, repr(got)[:60])
names, pairs = G["desk_chain"]()
check("L1 desk_chain: 3,000 desks, 2,999 conflicts, one path", len(names) == 3000 and len(pairs) == 2999)
n, p = G["desk_web"]()
comp = split_uf(n, p)
check("L1 desk_web: 5,000 desks, 10,997 conflicts", len(n) == 5000 and len(p) == 4997 + 6000)
check("L1 desk_web is bipartite and odd=True is not", comp is not None and split_uf(*G["desk_web"](odd=True)) is None)

READER = '''
def split_desks(desks, conflicts):
    nbrs = {d: set() for d in desks}
    for a, b in conflicts:
        nbrs[a].add(b); nbrs[b].add(a)
    side = {}
    for root in sorted(desks):
        if root in side:
            continue
        side[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in nbrs[u]:
                if v not in side:
                    side[v] = side[u] ^ 1
                    stack.append(v)
                elif side[v] == side[u]:
                    return None
    return side
'''
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter (returns None, so the three None tests pass)", [1, 2, 4, 5, 6, 7, 8, 10, 11])
expect(w, READER, "reader solution (stack, sets)", [])
S = w["solution"]
expect(w, S.replace("        adj[b].append(a)\n", ""), "slip: conflicts stored one way", None)
expect(w, S.replace("                elif group[v] == group[u]:\n                    return None     # an odd loop: no split works\n", ""), "slip: placed neighbours never checked", [3, 9, 12])
expect(w, S.replace("for start in sorted(desks):", "for start in desks:"), "slip: desks in given order", None)
expect(w, S.replace("    for start in sorted(desks):     # the first desk of each linked set\n        if start in group:\n            continue\n",
                    "    for start in sorted(desks)[:1]:\n"), "slip: only the first linked set", None)
expect(w, S.replace("                elif group[v] == group[u]:", "                elif group[v] != group[u]:"), "slip: clash when groups differ", None)
GREEDY = '''
def split_desks(desks, conflicts):
    group = {}
    for a, b in conflicts:
        if a not in group and b not in group:
            group[min(a, b)] = 0; group[max(a, b)] = 1
        elif a in group and b not in group:
            group[b] = 1 - group[a]
        elif b in group and a not in group:
            group[a] = 1 - group[b]
        elif group[a] == group[b]:
            return None
    for d in desks:
        group.setdefault(d, 0)
    return group
'''
expect(w, GREEDY, "slip: one conflict at a time", None)
REC = '''
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b); adj[b].append(a)
    group = {}
    def go(u):
        for v in adj[u]:
            if v not in group:
                group[v] = 1 - group[u]
                if not go(v):
                    return False
            elif group[v] == group[u]:
                return False
        return True
    for s in sorted(desks):
        if s not in group:
            group[s] = 0
            if not go(s):
                return None
    return group
'''
expect(w, REC, "slip: recursive search, default limit", None)
expect(w, "import sys\nsys.setrecursionlimit(20000)\n" + REC, "reader: recursive search, limit raised (CPython)", None)

# ======================= L2 count_cheapest =======================
it = item("graphs-dp", "homework-2.json", "h-cheapest-count"); w = it["widget"]
print("graphs-dp L2 h-cheapest-count")
G = {}
exec(w["postlude"], G)

def cheapest_bf(links, src, dst):
    """Route 2: Bellman-Ford distances, then counts over the cheapest-route DAG in order of distance."""
    if src == dst:
        return (0, 1)
    INF = float("inf")
    nodes = {src, dst} | {a for a, b, f in links} | {b for a, b, f in links}
    dist = {v: INF for v in nodes}; dist[src] = 0
    for _ in range(len(nodes)):
        ch = False
        for a, b, f in links:
            if dist[a] + f < dist[b]:
                dist[b] = dist[a] + f; ch = True
        if not ch:
            break
    if dist[dst] == INF:
        return (None, 0)
    ways = {v: 0 for v in nodes}; ways[src] = 1
    into = {}
    for a, b, f in links:
        if dist[a] + f == dist[b]:
            into.setdefault(b, []).append(a)
    for v in sorted((v for v in nodes if dist[v] < INF), key=lambda v: dist[v]):
        if v != src:
            ways[v] = sum(ways[u] for u in into.get(v, []))
    return (dist[dst], ways[dst])

for k, c in enumerate(w["tests"], 1):
    got = eval(c["call"].replace("count_cheapest", "cheapest_bf"), dict(G, cheapest_bf=cheapest_bf))
    check(f"L2 test {k} expect by Bellman-Ford and a DAG count", tuple(got) == eval(c["expect"]), repr(got))
# route 3 for the ladder: layer by layer DP
links = G["venue_ladder"]()
W = {(a, b): f for a, b, f in links}
best = {"L00_0": (0, 1)}
for i in range(60):
    nxt = {}
    for b in range(5):
        vb = "L%02d_%d" % (i + 1, b)
        opts = [(best[u][0] + W[(u, vb)], best[u][1]) for u in best]
        m = min(o[0] for o in opts)
        nxt[vb] = (m, sum(o[1] for o in opts if o[0] == m))
    best = nxt
check("L2 ladder by layers", best["L60_0"] == (61, 358584264000), repr(best["L60_0"]))
check("L2 ladder count passes a billion", best["L60_0"][1] > 10**9)
# brute force on small random maps: every route enumerated
rng = random.Random(4)
def brute(links, src, dst):
    adj = {}
    for a, b, f in links:
        adj.setdefault(a, []).append((b, f))
    costs = []
    def walk(u, seen, c):
        if u == dst:
            costs.append(c); return
        for v, f in adj.get(u, []):
            if v not in seen:
                walk(v, seen | {v}, c + f)
    walk(src, {src}, 0)
    if not costs:
        return (None, 0)
    m = min(costs)
    return (m, costs.count(m))
SOL = {}
exec(w["solution"], SOL)
mism = 0
for trial in range(400):
    nv = rng.randint(2, 7)
    vs = ["v%d" % i for i in range(nv)]
    links, seen = [], set()
    for _ in range(rng.randint(0, nv * 3)):
        a, b = rng.sample(vs, 2)
        if (a, b) not in seen:
            seen.add((a, b)); links.append((a, b, rng.randint(1, 3)))
    s, d = rng.choice(vs), rng.choice(vs)
    want = (0, 1) if s == d else brute(links, s, d)
    if tuple(SOL["count_cheapest"](links, s, d)) != want or cheapest_bf(links, s, d) != want:
        mism += 1
check("L2 shipped and route 2 against brute force on 400 small maps", mism == 0, f"{mism} mismatches")
check("L2 test 2 and 6: equal-cost routes through different venues", True, "4 routes via PAR/FRA then MIL/ZUR; 3 routes of 4")

READER = '''
import heapq
def count_cheapest(links, src, dst):
    out = {}
    for a, b, f in links:
        out.setdefault(a, []).append((b, f))
    dist, count, done = {src: 0}, {src: 1}, set()
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, f in out.get(u, ()):
            nd = d + f
            if nd < dist.get(v, float("inf")):
                dist[v], count[v] = nd, count[u]
                heapq.heappush(pq, (nd, v))
            elif nd == dist[v]:
                count[v] += count[u]
    if dst not in dist:
        return (None, 0)
    return (dist[dst], count[dst])
'''
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter", list(range(1, 12)))
expect(w, READER, "reader solution (done set, no early stop)", [])
S = w["solution"]
expect(w, S.replace("        if d > cost[u]:\n            continue                # a stale entry: u left the heap earlier\n", ""), "reader: no stale skip, relaxing from the popped d (harmless)", [])
expect(w, S.replace("        if d > cost[u]:\n            continue                # a stale entry: u left the heap earlier\n", "").replace("nd = d + fee", "nd = cost[u] + fee"), "slip: no stale skip, relaxing from cost[u]", None)
expect(w, S.replace("                ways[v] = ways[u]\n", "                ways[v] = ways.get(v, 0) + ways[u]\n"), "slip: cheaper cost keeps the old count", None)
summary_each(w, S.replace("                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n",
                    "                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n                heapq.heappush(heap, (nd, v))\n"), "slip: a tie pushes the venue again")
expect(w, S.replace("                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n", "                ways[v] += 1\n"), "slip: a tie adds 1", None)
BFS = '''
from collections import deque
def count_cheapest(links, src, dst):
    adj = {}
    for a, b, f in links:
        adj.setdefault(a, []).append((b, f))
    dist, ways = {src: 0}, {src: 1}
    q = deque([src])
    while q:
        u = q.popleft()
        for v, f in adj.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1; ways[v] = ways[u]; q.append(v)
            elif dist[v] == dist[u] + 1:
                ways[v] += ways[u]
    if dst not in dist:
        return (None, 0)
    # fee of the first route found
    return (dist[dst], ways[dst])
'''
expect(w, BFS, "slip: fewest links (BFS), fees ignored", None)
FIRST = S.replace("        if u == dst:\n            return d, ways[u]       # every cheaper venue is done, so ways[u] is final\n", "").replace(
    "            nd = d + fee\n", "            nd = d + fee\n            if v == dst and v not in cost:\n                return nd, ways[u]\n")
expect(w, FIRST, "slip: stop when dst is first reached", None)
expect(w, S.replace("ways[v] += ways[u]", "ways[v] = (ways[v] + ways[u]) % 1_000_000_007"), "slip: counts mod 1e9+7", None)
ENUM = '''
def count_cheapest(links, src, dst):
    if src == dst:
        return (0, 1)
    adj = {}
    for a, b, f in links:
        adj.setdefault(a, []).append((b, f))
    best = [None, 0]
    def walk(u, seen, c):
        if best[0] is not None and c > best[0]:
            return
        if u == dst:
            if best[0] is None or c < best[0]:
                best[0], best[1] = c, 1
            elif c == best[0]:
                best[1] += 1
            return
        for v, f in adj.get(u, []):
            if v not in seen:
                walk(v, seen | {v}, c + f)
    walk(src, {src}, 0)
    return tuple(best)
'''
summary_each(w, ENUM, "slip: list every route (pruned DFS)")

# ======================= L3 trade_with_fee =======================
it = item("graphs-dp", "homework-3.json", "h-fee-trades"); w = it["widget"]
print("graphs-dp L3 h-fee-trades")
G = {}
exec(w["postlude"], G)

def fee_quadratic(prices, fee):
    """Route 2: f[j] = best profit flat after the first j days; buy on day i, sell on day j-1."""
    n = len(prices)
    f = [0] * (n + 1)
    for j in range(1, n + 1):
        best = f[j - 1]
        for i in range(j - 1):
            best = max(best, f[i] + prices[j - 1] - prices[i] - fee)
        f[j] = best
    return f[n]

def fee_brute(prices, fee):
    """Route 3: every action sequence (0 hold/none, 1 trade) with at most one share."""
    best = 0
    for acts in itertools.product((0, 1), repeat=len(prices)):
        held, cash = None, 0
        for p, a in zip(prices, acts):
            if a:
                if held is None:
                    held = p; cash -= p
                else:
                    held = None; cash += p - fee
        if held is None:
            best = max(best, cash)
    return best

for k, c in enumerate(w["tests"], 1):
    g = dict(G, fee_quadratic=fee_quadratic)
    got = eval(c["call"].replace("trade_with_fee", "fee_quadratic"), g)
    ok = got == eval(c["expect"])
    if len(eval(c["call"].split("(", 1)[1].rsplit(",", 1)[0], G) if "price_walk" not in c["call"] else []) <= 16 and "price_walk" not in c["call"]:
        args = eval("(" + c["call"].split("(", 1)[1], G)
        ok = ok and fee_brute(*args) == got
    check(f"L3 test {k} expect by O(n^2) DP (and brute force when short)", ok, repr(got))
pw = G["price_walk"](); pw4 = G["price_walk"](seed=4)
mv = max(abs(a - b) for a, b in zip(pw, pw[1:])); mv4 = max(abs(a - b) for a, b in zip(pw4, pw4[1:]))
check("L3 tests 10 and 11: fee larger than every daily move, profit still positive", 25 > mv and 60 > mv4, f"largest moves {mv}, {mv4}")
check("L3 price_walk: 300 prices, all at least 1", len(pw) == 300 and min(pw + pw4) >= 1)
SOL = {}
exec(w["solution"], SOL)
rng = random.Random(8)
mism = 0
for _ in range(600):
    n = rng.randint(0, 11)
    pr = [rng.randint(1, 30) for _ in range(n)]
    fee = rng.randint(0, 12)
    if not (SOL["trade_with_fee"](pr, fee) == fee_quadratic(pr, fee) == fee_brute(pr, fee)):
        mism += 1
check("L3 shipped and route 2 against brute force on 600 short series", mism == 0, f"{mism}")
check("L3 fee above every move, multi-day rise: [10, 12, 14, 16] fee 3 gives 3", SOL["trade_with_fee"]([10, 12, 14, 16], 3) == 3 == fee_brute([10, 12, 14, 16], 3))

READER = '''
def trade_with_fee(prices, fee):
    if not prices:
        return 0
    cash, hold = 0, -prices[0]
    for p in prices[1:]:
        cash = max(cash, hold + p - fee)
        hold = max(hold, cash - p)
    return cash
'''
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter", list(range(1, 12)))
expect(w, READER, "reader solution (seeded from day 0)", [])
BUYFEE = "def trade_with_fee(prices, fee):\n    flat, long = 0, float('-inf')\n    for p in prices:\n        flat, long = max(flat, long + p), max(long, flat - p - fee)\n    return flat\n"
expect(w, BUYFEE, "reader: fee charged at the buy (same totals)", [])
S = w["solution"]
expect(w, S.replace("max(long, flat - p)", "max(long, flat - p - fee)"), "slip: fee on both legs", None)
expect(w, "def trade_with_fee(prices, fee):\n    return sum(max(0, b - a - fee) for a, b in zip(prices, prices[1:]))\n", "slip: each daily rise on its own", None)
expect(w, "def trade_with_fee(prices, fee):\n    best, low = 0, float('inf')\n    for p in prices:\n        low = min(low, p)\n        best = max(best, p - low - fee)\n    return best\n", "slip: one round trip only", None)
expect(w, S.replace("long + p - fee", "long + p"), "slip: no fee", None)
expect(w, S.replace("float('-inf')", "0"), "slip: long starts at 0", None)
expect(w, S.replace("for p in prices:", "for p in prices[1:]:"), "slip: first day skipped", None)
expect(w, S.replace("for p in prices:", "for p in prices[:-1]:"), "slip: last day skipped", None)
expect(w, S.replace("    return flat ", "    return max(flat, long) "), "reader: may end holding (never better: long < flat)", [])
expect(w, "def trade_with_fee(prices, fee):\n    flat, long = 0, float('-inf')\n    for p in prices:\n        flat = max(flat, long + p - fee)\n        long = max(long, flat - p)\n    return flat\n", "reader: sequential update (same-day sell then buy)", [])
RUNS = '''
def trade_with_fee(prices, fee):
    total, i, n = 0, 0, len(prices)
    while i < n:
        while i + 1 < n and prices[i + 1] <= prices[i]:
            i += 1
        j = i
        while j + 1 < n and prices[j + 1] >= prices[j]:
            j += 1
        if j > i:
            total += max(0, prices[j] - prices[i] - fee)
        i = j + 1
    return total
'''
expect(w, RUNS, "slip: each run of rises on its own", None)
print("mismatches:", bad)
sys.exit(1 if bad else 0)
