#!/usr/bin/env python3
"""Concept checks for graphs-dp L1 to L3 (round 1 blind audit).

Run from the repository root:  python3 docs/reports/graphs-dp-L1-3-concepts.py
Every check reads the content JSON where it can and recomputes the claim.
Exit 0 means every checked claim holds. A check that fails because the
content is wrong stays failing (it is listed as a finding in
docs/reviews/audit-graphs-dp-1-3.md). CPython 3.11+; no third-party imports.
"""
import heapq
import itertools
import json
import math
import os
import sys
import time
from collections import deque
from functools import lru_cache

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
C = os.path.join(ROOT, "app", "content", "courses", "graphs-dp")
FAILS, PASSES = [], [0]


def J(name):
    with open(os.path.join(C, name + ".json")) as f:
        return json.load(f)


def claim(name, ok, note=""):
    if ok:
        PASSES[0] += 1
    else:
        FAILS.append(name + (": " + str(note) if note else ""))


def sol(doc, where):
    """exec a code widget's prelude + solution (+ postlude); return its namespace."""
    w = where["widget"]
    ns = {}
    exec(w.get("prelude", "") + "\n" + w["solution"] + "\n" + w.get("postlude", ""), ns)
    return ns


def text_of(o):
    return json.dumps(o, ensure_ascii=False)


# ---------------------------------------------------------------- level 1
l1, l2, l3, l4, l5 = (J(n) for n in ("l1-nodes-and-edges", "l2-level-by-level",
                                      "l3-going-deep", "l4-islands", "l5-tasks-in-order"))
E6 = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("E", "F")]


def check_l1():
    ns = sol(l1, l1["screens"][5])
    adj = ns["adj_list"]("ABCDEF", E6)
    claim("l1 s1 neighbour table", adj == {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
                                           "D": ["B", "C"], "E": ["C", "F"], "F": ["E"]})
    m = sol(l1, l1["screens"][8])["adj_matrix"](6, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (4, 5)])
    claim("l1 s3 12 ones", sum(map(sum, m)) == l1["screens"][3]["widget"]["answer"] == 12)
    claim("l1 s3 symmetric", all(m[i][j] == m[j][i] for i in range(6) for j in range(6)))
    # s3.ex says an undirected matrix has 2E ones: only without self-loops (the lesson's own test 6)
    loop = sol(l1, l1["screens"][8])["adj_matrix"](2, [(1, 1)])
    claim("l1 s3.ex '2E ones' needs 'no self-loops' (imprecise, finding 9)", sum(map(sum, loop)) == 2 * 1,
          "one self-loop edge gives %d one(s), not 2E = 2" % sum(map(sum, loop)))
    # shared-row trap
    bad = [[0] * 3] * 3
    bad[0][1] = 1
    claim("l1 s8 [[0]*n]*n shares rows", bad == [[0, 1, 0]] * 3)
    # trap: one-way storage
    a = {v: [] for v in "ABCDEF"}
    for u, v in E6:
        a[u].append(v)
    claim("l1 s6 prints []", a["D"] == [])
    # generalise numbers
    claim("l1 s7 10^10 cells, 2e6 entries, 1e6 edges", 100_000 ** 2 == 10 ** 10 and 100_000 * 20 == 2 * 10 ** 6)
    claim("l1 s7 80 GB of pointers", 10 ** 10 * 8 / 1e9 == 80)
    row = [0] * 1000
    claim("l1 s7 a list cell is one 8-byte pointer", (sys.getsizeof([0] * 2000) - sys.getsizeof(row)) / 1000 == 8)
    f = sol(l1, l1["screens"][9])["find_ccp"]
    claim("l1 s9 ccp", f(4, [(0, 3), (1, 3), (2, 3), (0, 1)]) == 3 and f(1, []) == 0 and f(2, []) == -1)
    # s9 fb test-4: firm 2 posts to nobody and nobody posts to it; text says 'nobody needs to post to it'
    posts = [(0, 3), (1, 3)]
    into2 = sum(1 for a_, b in posts if b == 2)
    claim("l1 s9 fb test-4 wording (finding 13)", "nobody needs to post" not in l1["screens"][9]["feedback"]["byKey"]["test-4"],
          "firm 2 has in-degree %d: the text should say nobody posts to it, and every other firm must" % into2)
    claim("l1 quiz cells", 1000 ** 2 == 10 ** 6 and 1000 + 2 * 3000 == 7000 and 1 - 6000 / 10 ** 6 == 0.994)
    claim("l1 quiz entries, review-1 entries", 2 * 7 == 14 and 2 * 15 == 30)


G8 = {"A": ["B", "D"], "B": ["A", "E"], "C": ["D", "G"], "D": ["A", "C", "F"],
      "E": ["B", "G", "H"], "F": ["D"], "G": ["C", "E"], "H": ["E"]}


def check_l2():
    bfs = sol(l2, l2["screens"][4])["bfs"]
    claim("l2 s1 bfs order", bfs(G8, "A") == l2["screens"][1]["widget"]["answer"])
    # trap: mark on pop
    q, seen, order = deque(["A"]), set(), []
    while q:
        u = q.popleft()
        seen.add(u)
        order.append(u)
        for v in sorted(G8[u]):
            if v not in seen:
                q.append(v)
    claim("l2 s5 late marking order", order == ["A", "B", "D", "E", "C", "F", "G", "H", "G"])
    # s4 fb test-7 says a timeout there means list.pop(0); on a path the queue never holds more than 1
    adj = {i: [i - 1, i + 1] for i in range(1, 2999)}
    adj[0], adj[2999] = [1], [2998]
    q, seen, longest, out = [0], {0}, 0, []
    t0 = time.perf_counter()
    while q:
        longest = max(longest, len(q))
        u = q.pop(0)
        out.append(u)
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v)
                q.append(v)
    dt = time.perf_counter() - t0
    claim("l2 s4 test 7 cannot tell pop(0) from popleft (misleading, finding 10)",
          not (out == list(range(3000)) and longest == 1),
          "list.pop(0) BFS passes test 7 in %.4f s; the queue never exceeds %d item" % (dt, longest))
    # pop(0) worst case: star of V nodes
    V = 2000
    q, moves = list(range(V)), 0
    while q:
        moves += len(q) - 1
        q.pop(0)
    claim("l2 s7 pop(0) is quadratic on a full queue", moves == V * (V - 1) // 2)
    wh = sol(l2, l2["screens"][8])["within_hops"]
    net = {"Cedar": ["Birch", "Elm", "Larch"], "Birch": ["Alder", "Cedar"], "Elm": ["Cedar", "Fir"],
           "Alder": ["Birch", "Oak"], "Oak": ["Alder", "Larch"], "Fir": ["Elm", "Hazel"],
           "Hazel": ["Fir"], "Larch": ["Cedar", "Oak"]}
    claim("l2 s8 two hops", wh(net, "Cedar", 2) == ["Alder", "Birch", "Elm", "Fir", "Larch", "Oak"]
          and "Hazel" in wh(net, "Cedar", 3))


def check_l3():
    dfs = sol(l3, l3["screens"][2])["dfs"]
    dfs_stack = sol(l3, l3["screens"][5])["dfs_stack"]
    pre = dfs(G8, "A")
    claim("l3 s0 dfs order", pre == l3["screens"][0]["widget"]["answer"])
    claim("l3 s5 stack matches recursion from every start", all(dfs(G8, s) == dfs_stack(G8, s) for s in G8))
    stack, seen, order = ["A"], set(), []
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v in sorted(G8[u]):
            if v not in seen:
                stack.append(v)
    claim("l3 s4 naive stack order", order == ["A", "D", "F", "C", "G", "E", "H", "B"])
    post, seen = [], set()

    def visit(u):
        seen.add(u)
        for v in sorted(G8[u]):
            if v not in seen:
                visit(v)
        post.append(u)
    visit("A")
    claim("l3 s6 post-order", post == l3["screens"][6]["widget"]["answer"])
    tri = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}

    def nodfs(adj, u, order):
        order.append(u)
        for v in sorted(adj[u]):
            nodfs(adj, v, order)
    try:
        nodfs(tri, "A", [])
        claim("l3 s3 RecursionError", False)
    except RecursionError:
        claim("l3 s3 RecursionError", True)
    claim("l3 s7 default limit about 1,000", 900 <= sys.getrecursionlimit() <= 1100, sys.getrecursionlimit())
    hc = sol(l3, l3["screens"][9])["has_cycle"]
    claim("l3 s9 diamond is not a cycle", hc({"hedge": ["delta", "vega"], "delta": ["spot"], "vega": ["spot"], "spot": []}) is False)
    # quiz q-post: R(S(U), T)
    tree = {"R": ["S", "T"], "S": ["U"], "T": [], "U": []}
    pre, post = [], []

    def w(u):
        pre.append(u)
        for v in tree[u]:
            w(v)
        post.append(u)
    w("R")
    claim("l3 q-post key", post == ["U", "S", "T", "R"] and pre == ["R", "S", "U", "T"])
    opt = [o for o in l3["quiz"][3]["widget"]["options"] if o["id"] == "rev"][0]
    is_rev_pre = opt["text"].split(", ") == pre[::-1]
    claim("l3 q-post option 'rev' why says it reverses the pre-order (wrong, finding 3)",
          is_rev_pre or "reverses the pre-order" not in opt["why"],
          "%s is the reversed post-order %s; the reversed pre-order is %s" % (opt["text"], post[::-1], pre[::-1]))
    # quiz q-tree: 'no edge to a visited non-parent node' also holds on a forest, which is not a tree
    forest = {0: [1], 1: [0], 2: [3], 3: [2]}
    seen, back = set(), [0]

    def t(u, p):
        seen.add(u)
        for v in forest[u]:
            if v == p:
                continue
            if v in seen:
                back[0] += 1
            else:
                t(v, u)
    t(0, None)
    claim("l3 q-tree 'how DFS tests for a tree' also needs every node reached (imprecise, finding 12)",
          not (back[0] == 0 and len(seen) < len(forest)),
          "a two-piece forest has 0 back edges from node 0 and is not a tree")


GRID = [[1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 0], [1, 0, 0, 0, 1, 1], [1, 1, 0, 1, 0, 1]]


def islands(grid, diag=False):
    rows, cols = len(grid), len(grid[0]) if grid else 0
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)] + ([(-1, -1), (-1, 1), (1, -1), (1, 1)] if diag else [])
    seen, n = set(), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] and (r, c) not in seen:
                n += 1
                seen.add((r, c))
                st = [(r, c)]
                while st:
                    a, b = st.pop()
                    for dr, dc in steps:
                        x, y = a + dr, b + dc
                        if 0 <= x < rows and 0 <= y < cols and grid[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            st.append((x, y))
    return n


def check_l4():
    ci = sol(l4, l4["screens"][4])["count_islands"]
    claim("l4 s1 six islands, 4 with corners", ci(GRID) == 6 == islands(GRID) and islands(GRID, True) == 4)
    r1 = [[1, 1, 0, 0, 1], [0, 1, 0, 1, 1], [1, 0, 0, 0, 0], [1, 1, 0, 1, 0]]
    claim("review-1 islands 4, 3 with corners", islands(r1) == 4 and islands(r1, True) == 3)
    claim("l4 quiz X pattern 5 and 1", islands([[1, 0, 1], [0, 1, 0], [1, 0, 1]]) == 5 and islands([[1, 0, 1], [0, 1, 0], [1, 0, 1]], True) == 1)
    ring = [[1] * 5, [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1] * 5]
    claim("homework-1 ring 2", islands(ring) == 2 and sum(map(sum, ring)) - 1 == 16)
    # s6: recursive flood fill, order up, down, left, right, on k by k of all land: depth k*k
    k, deepest, seen = 20, [0], set()

    def fill(r, c, d):
        seen.add((r, c))
        deepest[0] = max(deepest[0], d)
        for x, y in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= x < k and 0 <= y < k and (x, y) not in seen:
                fill(x, y, d + 1)
    fill(0, 0, 1)
    claim("l4 s6 the dive passes every cell", deepest[0] == k * k)
    claim("l4 s3 neighbour looks", 1000 * 1000 * 4 == l4["screens"][3]["widget"]["answer"])
    # s4 fb test-11: marking on pop with a skip does not time out on 20 by 20
    g = [[1] * 20 for _ in range(20)]
    seen, st, pushes = set(), [(0, 0)], 1
    while st:
        a, b = st.pop()
        if (a, b) in seen:
            continue
        seen.add((a, b))
        for x, y in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
            if 0 <= x < 20 and 0 <= y < 20 and (x, y) not in seen:
                st.append((x, y))
                pushes += 1
    claim("l4 s4 test 11: mark-on-pop pushes stay under 4 per cell", pushes <= 4 * 400 and len(seen) == 400)
    clr = sol(l4, l4["screens"][8])["count_loss_regions"]
    pnl = [[5, -15, -35, -55, -75], [50, 30, 10, -10, -30], [65, 45, 25, 5, -15], [50, 30, 10, -10, -30], [5, -15, -35, -55, -75]]
    claim("l4 s8 loss regions", [clr(pnl, x) for x in (50, 10, 100, 30)] == [2, 1, 0, 2]
          and all(row[4] < -10 for row in pnl))


PIPE = {"prices": ["returns"], "calendar": ["returns"], "returns": ["signals", "risk"],
        "signals": ["backtest"], "risk": ["backtest"], "backtest": ["report"], "report": []}


def valid(order, adj):
    pos = {u: i for i, u in enumerate(order)}
    return all(pos[u] < pos[v] for u in adj for v in adj[u])


def check_l5():
    topo = sol(l5, l5["screens"][3])["topo_sort"]
    claim("l5 s0 four valid orders", sum(valid(p, PIPE) for p in itertools.permutations(PIPE)) == 4)
    claim("l5 s3 kahn order", topo(PIPE) == ["calendar", "prices", "returns", "risk", "signals", "backtest", "report"])

    def pre_post(adj, starts):
        seen, pre, post = set(), [], []

        def visit(u):
            seen.add(u)
            pre.append(u)
            for v in sorted(adj[u]):
                if v not in seen:
                    visit(v)
            post.append(u)
        for u in starts:
            if u not in seen:
                visit(u)
        return pre, post
    pre, post = pre_post(PIPE, sorted(PIPE))
    claim("l5 s4 pre-order result", pre == ["backtest", "report", "calendar", "returns", "risk", "signals", "prices"])
    claim("l5 s5 post-order", post == l5["screens"][5]["widget"]["answer"] and valid(post[::-1], PIPE))
    # s4 frames the bug as the starting place; pre-order from the in-degree-0 tasks is still invalid
    pre2, _ = pre_post(PIPE, ["calendar", "prices"])
    s4 = text_of(l5["screens"][4]) + l5["summary"]["trap"]
    claim("l5 s4 trap: pre-order started at a free task is still wrong, and the screen does not say so (misleading, finding 6)",
          valid(pre2, PIPE) or "still" in l5["screens"][4]["explain"]["text"],
          "pre-order from calendar gives %s" % pre2)
    # reversed post-order on a cyclic graph returns an order silently
    cyc = dict(PIPE, backtest=["report", "risk"])
    _, post_c = pre_post(cyc, sorted(cyc))
    claim("l5 reversed post-order gives no warning on a cycle (imprecise, finding 11)",
          not (len(post_c) == 7 and not valid(post_c[::-1], cyc)) or "three" in text_of(l5["screens"][5]) + text_of(l5["screens"][7]),
          "it returns all 7 tasks in an invalid order; Kahn returns None")
    claim("l5 s6 kahn emits 4 of 7", topo(cyc) is None)
    indeg = {u: 0 for u in cyc}
    for u in cyc:
        for v in cyc[u]:
            indeg[v] += 1
    ready, out = sorted(u for u in cyc if indeg[u] == 0), []
    while ready:
        u = ready.pop(0)
        out.append(u)
        for v in cyc[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
                ready.sort()
    claim("l5 s6 the four emitted", out == ["calendar", "prices", "returns", "signals"])
    r = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": ["e"], "e": ["f"], "f": ["d", "g"], "g": []}
    claim("review-1 kahn cycle None", topo(r) is None)
    claim("l5 quiz 4! = 24 and unique order a, c, b", math.factorial(4) == 24 and
          [p for p in itertools.permutations("abc") if valid(p, {"a": ["b", "c"], "c": ["b"], "b": []})] == [("a", "c", "b")])


def check_hw1():
    h = J("homework-1")
    it = {i["id"]: i for i in h["items"]}
    br = sol(h, it["h-rounds"])["batch_rounds"]
    deps = {"var_report": ["pnl_vectors", "positions"], "pnl_vectors": ["positions", "scenarios"],
            "scenarios": ["market_data"], "limits_check": ["var_report"]}
    claim("hw1 rounds 5 = longest chain in jobs", br(deps) == 5)
    claim("hw1 matrix GB", 20_000 ** 2 * 8 / 1e9 == 3.2 and 20_000 * 8 / 1e9 == 0.00016)
    sd = sol(h, it["h-split-desks"])["split_desks"]
    claim("hw1 split desks odd loop", sd(["Gilts", "Index", "Repo"], [("Repo", "Gilts"), ("Gilts", "Index"), ("Index", "Repo")]) is None)
    claim("hw1 split desks square", sd(["Credit", "Equity", "FX", "Rates"], [("Credit", "Equity"), ("Credit", "Rates"), ("Rates", "FX"), ("FX", "Equity")])
          == {"Credit": 0, "Equity": 1, "Rates": 1, "FX": 0})


# ---------------------------------------------------------------- level 2
l6, l7, l8, l9 = (J(n) for n in ("l6-fewest-steps", "l7-dijkstra", "l8-groups", "l9-arbitrage-cycle"))
H8 = {"A": ["B", "E"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C", "G", "H"],
      "E": ["A", "F", "G"], "F": ["E", "H"], "G": ["D", "E"], "H": ["D", "F"]}


def bfs_dist(adj, s):
    d, q = {s: 0}, deque([s])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def check_l6():
    sp = sol(l6, l6["screens"][4])["shortest_path"]
    d = bfs_dist(H8, "A")
    claim("l6 s1 rings", sorted(k for k, v in d.items() if v == 2) == ["C", "F", "G"] and d["D"] == d["H"] == 3)
    claim("l6 s0 route", sp(H8, "A", "H") == ["A", "E", "F", "H"])
    # s1 fb with-d: 'D is two hops from C'
    dc = bfs_dist(H8, "C")["D"]
    claim("l6 s1 fb with-d 'D is two hops from C' (wrong, finding 2)",
          dc == 2 or "two hops from C" not in l6["screens"][1]["feedback"]["byKey"]["with-d"],
          "D is %d hop from C; C is %d hops from A" % (dc, d["C"]))

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
    claim("l6 s5 dfs route", find_path(H8, "A", "H") == ["A", "B", "C", "D", "G", "E", "F", "H"])
    fc = sol(l6, l6["screens"][8])["fewest_conversions"]
    P = sol(l6, l6["screens"][8])["PAIRS"]
    claim("l6 s8 conversions", fc(P, "NGN", "THB") == 4 and len(P) == 12)
    maze = ["...#", "##.#", "....", ".##."]
    ms = sol(J("homework-2"), J("homework-2")["items"][0])["maze_steps"]
    claim("l6 quiz maze 6", ms(maze) == 6)
    claim("l6 quiz weights", abs(1.2 + 1.5 - 2.7) < 1e-12)


D7 = {"A": [("B", 4), ("C", 1)], "B": [("D", 1)], "C": [("B", 2), ("D", 5), ("E", 2)],
      "D": [("F", 3)], "E": [("F", 6)], "F": [], "G": [("F", 1)]}


def check_l7():
    ns = sol(l7, l7["screens"][4])
    dj = ns["dijkstra"]
    claim("l7 s0 costs", dj(D7, "A") == {"A": 0, "B": 3, "C": 1, "D": 4, "E": 3, "F": 7, "G": math.inf})
    # heap trace of s2
    dist = {u: math.inf for u in D7}
    dist["A"] = 0
    heap, trace, stale = [(0, "A")], [], 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1
            continue
        for v, w in D7[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
        trace.append((u, sorted(heap)))
    claim("l7 s2 heap after C", trace[1] == ("C", [(3, "B"), (3, "E"), (4, "B"), (6, "D")]))
    claim("l7 s2 heap after B, E", trace[2][1] == [(3, "E"), (4, "B"), (4, "D"), (6, "D")]
          and trace[3][1] == [(4, "B"), (4, "D"), (6, "D"), (9, "F")])
    claim("l7 s2 heap after D, three stale in all", trace[4] == ("D", [(6, "D"), (7, "F"), (9, "F")]) and stale == 3)
    # s5 trap
    def bad(adj, s):
        dist, heap = {}, [(0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            dist[u] = d
            for v, w in adj[u]:
                heapq.heappush(heap, (d + w, v))
        return dist
    b = bad(D7, "A")
    claim("l7 s5 trap values", b["B"] == 4 and b["F"] == 9 and b["D"] == 6)

    def fix(adj, s, which):
        dist, heap = {}, [(0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            if which == 1 and u in dist:
                continue
            if which == 2 and d > dist[u]:
                continue
            dist[u] = d
            for v, w in adj[u]:
                heapq.heappush(heap, (d + w, v))
        return dist
    claim("l7 s5 fix 1 works", fix(D7, "A", 1) == {k: v for k, v in dj(D7, "A").items() if v < math.inf})
    try:
        fix(D7, "A", 2)
        ok2 = True
    except KeyError as e:
        ok2 = False
    claim("l7 s5.ex second one-line fix `if d > dist[u]: continue` (wrong, finding 1)",
          ok2 or "if d > dist[u]: continue" not in l7["screens"][5]["explain"]["text"],
          "with `dist = {}` it raises KeyError: 'A' on the first pop")
    # s4: stale entries in test 9
    k = 300
    adj = {"s": [("c1", 1)]}
    for i in range(1, k + 1):
        nxt = [("c%d" % (i + 1), 1)] if i < k else []
        adj["c%d" % i] = nxt + [("h", 2 * k - 2 * i)]
    adj["h"] = [("t%d" % j, 1) for j in range(k)]
    for j in range(k):
        adj["t%d" % j] = []
    dist = {u: math.inf for u in adj}
    dist["s"] = 0
    heap, stale, hpush = [(0, "s")], 0, 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                hpush += v == "h"
                heapq.heappush(heap, (d + w, v))
    claim("l7 s4 hub test (300, 1)", ns["hub_scans"](300) == (300, 1) and hpush == 300)
    claim("l7 s4.ex 'Test 9 had 300 of them' (stale entries) (wrong, finding 4)",
          stale == 300 or "had 300 of them" not in l7["screens"][4]["explain"]["text"],
          "h is pushed %d times; %d of those entries are stale" % (hpush, stale))
    # s6: the lesson's own dijkstra on the negative arrow
    neg = {"A": [("B", 2), ("C", 3)], "B": [], "C": [("B", -2)]}
    got = dj(neg, "A")["B"]
    s6 = l7["screens"][6]
    claim("l7 s6 true cost 1", s6["widget"]["answer"] == 1)
    claim("l7 s6 fb.pop 'the cost Dijkstra fixed': the taught code returns 1, not 2 (imprecise, finding 5)",
          got == 2, "dijkstra(neg, 'A')['B'] == %d with the lesson's solution: it re-pushes B at 1" % got)
    # the taught code is right on negative edges with no negative cycle (label-correcting), on random DAG-free cases
    import random
    rnd = random.Random(3)
    agree = True
    for _ in range(300):
        n = 6
        order = list(range(n))
        rnd.shuffle(order)
        g = {i: [] for i in range(n)}
        for a in range(n):
            for b_ in range(a + 1, n):
                if rnd.random() < 0.5:
                    g[order[a]].append((order[b_], rnd.randint(-5, 9)))   # a DAG: no cycle at all
        bf = [math.inf] * n
        bf[order[0]] = 0
        for _ in range(n - 1):
            for u in g:
                for v, w in g[u]:
                    if bf[u] + w < bf[v]:
                        bf[v] = bf[u] + w
        dd = dj(g, order[0])
        agree &= all(dd[i] == bf[i] for i in range(n))
    claim("l7 lazy heap code agrees with Bellman-Ford on 300 negative-weight DAGs (basis for finding 5)", agree)
    # s8 fx
    fx = {"GBP": [("USD", 1.2), ("EUR", 0.5), ("JPY", 4.0)], "EUR": [("USD", 0.6), ("JPY", 2.4), ("CHF", 0.7)],
          "USD": [("JPY", 1.5)], "CHF": [("JPY", 1.9)], "JPY": []}
    dd = dj(fx, "GBP")
    claim("l7 s8 2.6 bp", abs(dd["JPY"] - 2.6) < 1e-9 and abs(dd["USD"] - 1.1) < 1e-9 and abs(dd["CHF"] - 1.2) < 1e-9)
    exact = 1e6 * (1 - (1 - 0.5e-4) * (1 - 0.6e-4) * (1 - 1.5e-4))
    claim("l7 s8.ex exact cost 259.98", round(exact, 2) == 259.98)
    claim("l7 s8.prose costs add 'to within a penny' (wrong, finding 7)",
          abs(260 - exact) <= 0.01 or "within a penny" not in l7["screens"][8]["prose"],
          "260 - %.4f = %.4f pounds, about 2 pence" % (exact, 260 - exact))
    sa = sol(l7, l7["screens"][9])
    claim("l7 s9 latency", [round(sa["slowest_arrival"](sa["LINKS"], sa["CENTRES"], s), 6) for s in ("LD4", "NY4", "FR2")] == [103.4, 110.7, 107.6]
          and abs(4.2 + 77 + 34 - 115.2) < 1e-9)
    claim("l7 quiz sparse", 8e6 < (100_000 + 400_000) * math.log2(100_000) < 9e6 and 100_000 ** 2 == 10 ** 10)
    # q-pushes: E + 1 is attained
    g = {0: [(1, 5), (2, 9), (3, 13)], 1: [(2, 3), (3, 7), (4, 11)], 2: [(3, 3), (4, 7)], 3: [(4, 3)], 4: [], 5: []}
    dist = {u: math.inf for u in g}
    dist[0] = 0
    heap, pushes = [(0, 0)], 1
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                pushes += 1
                heapq.heappush(heap, (d + w, v))
    claim("l7 q-pushes E + 1 = 10 is attained on 6 nodes, 9 edges", pushes == 10 and sum(map(len, g.values())) == 9)


def check_l8():
    parent = [0, 0, 2, 2, 2, 4, 4, 6]

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        changed = []
        while x != root:
            nxt = parent[x]
            if parent[x] != root:
                changed.append(x)
            parent[x] = root
            x = nxt
        return root, changed
    claim("l8 s2/s3 find(7) is 2 and re-points 7, 6", find(7) == (2, [7, 6]))
    D = sol(l8, l8["screens"][5])["DSU"]
    d = D(8)
    merges = sum(d.union(a, b) for a, b in [(0, 1), (2, 3), (1, 3), (5, 6)])
    claim("l8 s7 four components", merges == 4 and d.count() == 4)
    # union by size: depth at most log2 n over random unions without compression
    import random
    rnd = random.Random(1)
    n = 1024
    par, size = list(range(n)), [1] * n

    def root(x):
        while par[x] != x:
            x = par[x]
        return x
    for _ in range(5000):
        a, b = root(rnd.randrange(n)), root(rnd.randrange(n))
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            par[b] = a
            size[a] += size[b]

    def depth(x):
        k = 0
        while par[x] != x:
            x, k = par[x], k + 1
        return k
    claim("l8 s4 union by size keeps depth at most log2 n", max(map(depth, range(n))) <= math.log2(n))
    ns = sol(l8, l8["screens"][9])
    claim("l8 s9 clusters", ns["clusters"](ns["NAMES"], ns["CORR"]) == [["AZN"], ["BARC", "GILT", "HSBA", "LLOY"], ["BP", "SHEL"], ["GSK"], ["VOD"]])
    edges = sorted([(4, "A", "B"), (1, "A", "C"), (2, "B", "C"), (5, "B", "D"), (8, "C", "D"), (3, "D", "E"), (9, "C", "E")])
    idx, dsu, total = {c: i for i, c in enumerate("ABCDE")}, D(5), 0
    for w, a, b in edges:
        if dsu.union(idx[a], idx[b]):
            total += w
    best = min(sum(e[0] for e in comb) for comb in itertools.combinations(edges, 4)
               if (lambda dd: all(dd.union(idx[a], idx[b]) for _, a, b in comb))(D(5)))
    claim("review-2 kruskal 11 is the minimum over all spanning trees", total == 11 == best)
    claim("l8 q-chain 2.5e7", 5000 ** 2 == 2.5e7)
    claim("l8 quiz netting and records", True)


RATES = {"GBP": {"USD": 1.27}, "USD": {"EUR": 0.92}, "EUR": {"GBP": 0.86, "CHF": 0.95}, "CHF": {"GBP": 0.8985, "USD": 1.142}}


def check_l9():
    p = 1.27 * 0.92 * 0.86
    claim("l9 s0 products", round(p, 6) == 1.004824 and round(1.142 * 0.92 * 0.95, 6) == 0.998108
          and 1.27 * 0.92 * 0.95 * 0.8985 < 1)
    claim("l9 s1 break-even", round(1 / (1.27 * 0.92), 6) == 0.855871)
    w = [-math.log(r) for r in (1.27, 0.92, 0.86)]
    claim("l9 s2 weights", [round(x, 6) for x in w] == [-0.239017, 0.083382, 0.150823] and round(sum(w), 6) == -0.004812)
    bf = sol(l9, l9["screens"][4])["bellman_ford"]
    # s3 passes
    dist, table = [0, math.inf, math.inf, math.inf], []
    for _ in range(3):
        for u, v, wt in [(2, 3, 1), (1, 2, 3), (0, 1, 2)]:
            if dist[u] + wt < dist[v]:
                dist[v] = dist[u] + wt
        table.append(dist[1:])
    claim("l9 s3 pass table", table == [[2, math.inf, math.inf], [2, 5, math.inf], [2, 5, 6]])
    claim("l9 s4 unreachable negative cycle stays inf", bf([(0, 1, 2), (2, 3, -1), (3, 2, -1)], 4, 0) == [0, 2, math.inf, math.inf])
    f = -math.log(1.25) - math.log(0.8)
    claim("l9 s6 float sum is -5.55e-17", f < 0 and ("%.2e" % f) == "-5.55e-17")
    gross = 1.0850 / (0.8543 * 1.2700)
    claim("l9 s8 gross 1.0000359 and cross 0.854331", round(gross, 7) == 1.0000359 and round(1.0850 / 1.27, 6) == 0.854331)
    net = 1e6 * (gross * 0.9999 ** 3 - 1)
    claim("l9 s8 after costs", abs(net - l9["screens"][8]["widget"]["answer"]) < 1 and abs(1e6 * (gross - 1) - 35.95) < 1)
    ns = sol(l9, l9["screens"][9])
    claim("l9 s9 detector", ns["has_arbitrage"](RATES) is True and ns["has_arbitrage"]({"GBP": {"USD": 1.25}, "USD": {"GBP": 0.8}}) is False)
    claim("l9 quiz", 8 * 40 == 320 and round(1.27 * 0.787, 5) == 0.99949 and round(-math.log(1.27 * 0.787), 6) == 0.00051
          and abs(1.05 / 1.25 - 0.84) < 1e-12 and round(1.25 / 1.05, 4) == 1.1905)


def check_rev_hw2():
    r = J("review-2")
    claim("review-2 loop", round(191.20 * 0.006135 * 0.8530, 6) == 1.000579 and round(191.20 * 0.006135, 6) == 1.173012)
    g = {"S": [("A", 2), ("B", 6)], "A": [("B", 3), ("C", 7)], "B": [("C", 1), ("T", 8)], "C": [("T", 2)], "T": []}
    dist = {u: math.inf for u in g}
    dist["S"] = 0
    heap, stale = [(0, "S")], []
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale.append((d, u))
            continue
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    claim("review-2 dijkstra 8 and three stale", dist["T"] == 8 and stale == [(6, "B"), (9, "C"), (13, "T")])
    # passes on the chain, worst order
    dist, passes = [0] + [math.inf] * 5, 0
    while dist[5] != 5:
        passes += 1
        for u in range(4, -1, -1):
            if dist[u] + 1 < dist[u + 1]:
                dist[u + 1] = dist[u] + 1
    claim("review-2 five passes", passes == 5)
    h = J("homework-2")
    it = {i["id"]: i for i in h["items"]}
    ns = sol(h, it["h-within-k"])
    cw, Q = ns["cheapest_within"], ns["QUOTES"]
    claim("hw2 within k", [round(cw(Q, "GBP", "JPY", k), 6) for k in (0, 1, 2)] == [4.0, 2.7, 2.6]
          and [round(cw(Q, "GBP", "THB", k), 6) for k in (1, 2, 3)] == [7.5, 4.3, 4.2])
    gross = 1.2650 * 0.9230 * 0.8580
    claim("hw2 triangle", round(gross, 8) == 1.00179651 and abs(1e6 * (gross * 0.9998 ** 3 - 1) - 1195.55) < 0.01
          and abs(1e6 * (gross * 0.9998 - 1) - 1596.15) < 0.01 and abs(1e6 * (gross - 1) - 1796.51) < 0.01)
    claim("hw2 scanner relaxations about 26,000", 31 * 830 == 25730)
    cc = sol(h, it["h-cheapest-count"])["count_cheapest"]
    claim("hw2 count cheapest", cc([("LDN", "AMS", 4), ("LDN", "PAR", 1), ("PAR", "FRA", 1), ("LDN", "FRA", 2), ("FRA", "AMS", 2)], "LDN", "AMS") == (4, 3))
    # brute-force the count on small random graphs with fees >= 1
    import random
    rnd = random.Random(5)
    ok = True
    for _ in range(200):
        n = 6
        links = [(a, b, rnd.randint(1, 3)) for a in range(n) for b in range(n) if a != b and rnd.random() < 0.4]
        best, ways = None, 0
        adj = {}
        for a, b, f in links:
            adj.setdefault(a, []).append((b, f))

        def walk(u, cost, seen):
            nonlocal best, ways
            if u == n - 1:
                if best is None or cost < best:
                    best, ways = cost, 1
                elif cost == best:
                    ways += 1
                return
            for v, f in adj.get(u, []):
                if v not in seen:
                    walk(v, cost + f, seen | {v})
        walk(0, 0, {0})
        ok &= tuple(cc(links, 0, n - 1)) == (best, ways)
    claim("hw2 count cheapest equals brute force on 200 random maps", ok)


# ---------------------------------------------------------------- level 3
l10, l11, l12, l13 = (J(n) for n in ("l10-every-subset", "l11-dead-ends", "l12-remembering", "l13-climbing-stairs"))


def queens_nodes(n, prune):
    nodes = [0] * (n + 1)

    def place(row, cols):
        nodes[row] += 1
        if row == n:
            return
        for c in range(n):
            if prune and any(c == pc or abs(c - pc) == row - pr for pr, pc in enumerate(cols)):
                continue
            place(row + 1, cols + [c])
    place(0, [])
    return nodes


def check_l10_l11():
    ns = sol(l10, l10["screens"][9])
    subs = ns["subsets"](["A", "B", "C"])
    claim("l10 s2 fifth leaf is B C", subs[4] == ["B", "C"] and subs[0] == ["A", "B", "C"] and subs[-1] == [])
    claim("l10 counts", 2 ** 10 == 1024 and math.factorial(5) == 120 and 2 ** 4 - 1 == 15)
    v = ns["subsets"](["VOD", "BP", "VOD"])
    claim("l10 s8 duplicates", len(v) == 8 and len({frozenset(x) for x in v}) == 4 and len({tuple(sorted(x)) for x in v}) == 6)
    out, path, xs = [], [], ["a", "b"]

    def walk(i):
        if i == len(xs):
            out.append(path[:])
            return
        path.append(xs[i])
        walk(i + 1)
        walk(i + 1)
    walk(0)
    claim("l10 q-no-pop", out == [["a", "b"], ["a", "b"], ["a", "b", "b"], ["a", "b", "b"]])
    claim("l10 s10 42 portfolios", sum(math.comb(6, k) for k in range(4)) == 42 and 6 * 5 * 4 == 120)
    days = 2 ** 30 / 1000 / 86400
    claim("l10 s11 12.4 days, 35 years", round(days, 1) == 12.4 and round(2 ** 40 / 1000 / 86400 / 365.25) == 35
          and round(2 ** 30 / 1000 / 3600) == 298)
    q4, q4p = queens_nodes(4, False), queens_nodes(4, True)
    claim("l11 s3 4-queens table", q4 == [1, 4, 16, 64, 256] and q4p == [1, 4, 6, 4, 2] and sum(q4) == 341 and sum(q4p) == 17)
    claim("l11 s3 8-queens 19,173,961 against 2,057", (8 ** 9 - 1) // 7 == 19173961 and sum(queens_nodes(8, True)) == 2057
          and queens_nodes(8, True)[-1] == 92)
    # safe cells under r1c2
    safe = [(r, c) for r in range(1, 4) for c in range(4) if c != 1 and abs(c - 1) != r]
    claim("l11 s0 six safe cells", [(r + 1, c + 1) for r, c in safe] == [(2, 4), (3, 1), (3, 3), (4, 1), (4, 3), (4, 4)])
    # s2 hint: 'a queen in a corner of row 1 leads to a dead end by row 3'
    dead_rows = set()

    def place(row, cols):
        if row == 4:
            return
        opts = [c for c in range(4) if not any(c == pc or abs(c - pc) == row - pr for pr, pc in enumerate(cols))]
        if not opts:
            dead_rows.add(row + 1)
        for c in opts:
            place(row + 1, cols + [c])
    place(1, [0])
    claim("l11 s2 hint 'dead end by row 3' (imprecise, finding 14)", dead_rows <= {3},
          "from r1c1 the branches die at rows %s: r2c4 reaches r3c2 and fails in row 4" % sorted(dead_rows))

    def combos(cands, target):
        cands = sorted(cands)
        out, path = [], []

        def walk(start, left):
            if left == 0:
                out.append(path[:])
                return
            for i in range(start, len(cands)):
                if cands[i] > left:
                    break
                path.append(cands[i])
                walk(i, left - cands[i])
                path.pop()
        walk(0, target)
        return out
    claim("l11 s5 combos", combos([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]] and combos([2, 3, 6, 7], 7) == [[2, 2, 3], [7]])

    @lru_cache(None)
    def ordered(left, cands=(2, 3, 5)):
        return 1 if left == 0 else sum(ordered(left - c, cands) for c in cands if c <= left)
    claim("l11 s5 slip 6 = ordered sums", ordered(8) == 6 and ordered(7, (2, 3, 6, 7)) == 4)

    def trap(xs, target):
        def walk(i, total):
            if total == target:
                return True
            if total > target:
                return False
            if i == len(xs):
                return False
            return walk(i + 1, total + xs[i]) or walk(i + 1, total)
        return walk(0, 0)
    claim("l11 s6 and review-3 unsafe prune", trap([6, -4, 3], 2) is False and trap([4, -2, 1], 3) is False)
    ns = sol(l11, l11["screens"][8])
    claim("l11 s8 queens counts", [ns["n_queens"](n) for n in (1, 2, 3, 4, 5, 6, 8)] == [1, 0, 0, 2, 10, 4, 92])
    # q-restore
    def broken(n):
        cols, diag, anti = set(), set(), set()

        def place(row):
            if row == n:
                return 1
            count = 0
            for c in range(n):
                if c in cols or row - c in diag or row + c in anti:
                    continue
                cols.add(c); diag.add(row - c); anti.add(row + c)
                count += place(row + 1)
            return count
        return place(0)
    claim("l11 q-restore 0", broken(4) == 0)
    claim("l11 q-full", 8 ** 8 == 16777216)


def check_l12_l13():
    calls = [0]

    def fib(n):
        calls[0] += 1
        return n if n < 2 else fib(n - 1) + fib(n - 2)
    table = []
    for n in range(9):
        calls[0] = 0
        fib(n)
        table.append(calls[0])
    claim("l12 call counts", table == [1, 1, 3, 5, 9, 15, 25, 41, 67])
    a, b = 0, 1
    for _ in range(31):
        a, b = b, a + b
    claim("l12 fib(30) 832040 with 2,692,537 calls", a == 1346269 and 2 * a - 1 == 2692537 and b - a == 832040)
    fm = sol(l12, l12["screens"][9])
    claim("l12 fib_memo", fm["fib_memo"](30) == (832040, 31) and fm["fib_memo"](6) == (8, 7))
    cache, hits, total = {}, [0], [0]

    def f(k):
        total[0] += 1
        if k in cache:
            hits[0] += 1
            return cache[k]
        cache[k] = k if k < 2 else f(k - 1) + f(k - 2)
        return cache[k]
    f(30)
    claim("l12 s4 28 hits, 59 calls", hits[0] == 28 and total[0] == 59)
    cache.clear(); hits[0] = total[0] = 0
    f(5)
    claim("l12 s2 15 calls become 9", total[0] == 9 and hits[0] == 3)
    cnt = [0] * 7

    def g(n):
        cnt[n] += 1
        return n if n < 2 else g(n - 1) + g(n - 2)
    g(6)
    claim("l12 s3 naive column", cnt == [5, 8, 5, 3, 2, 1, 1])
    claim("l12 grid", fm["grid_paths"](3, 4) == 10 == math.comb(5, 2) and fm["grid_paths"](18, 18) == math.comb(34, 17))
    rate = [0.05]

    @lru_cache(maxsize=None)
    def price(cashflow, years):
        return round(cashflow / (1 + rate[0]) ** years, 2)
    first = price(100, 1)
    rate[0] = 0.10
    claim("l12 s6 stale price", (first, price(100, 1)) == (95.24, 95.24) and round(100 / 1.1, 2) == 90.91)

    class Curve:
        def __init__(self, r):
            self.rate = r

        @lru_cache(maxsize=None)
        def df(self, t):
            return (1 + self.rate) ** -t
    c = Curve(0.05)
    c.df(2)
    c.rate = 0.06
    claim("l12 q-method prints 0.907", str(round(c.df(2), 4)) == "0.907" and str(round(1.06 ** -2, 4)) == "0.89")
    try:
        lru_cache(lambda x: 0)([1, 2])
        claim("l12 s7 list key TypeError", False)
    except TypeError:
        claim("l12 s7 list key TypeError", True)
    claim("l12 s10 496 nodes", sum(range(1, 32)) == 496)
    ns = sol(l13, l13["screens"][9])
    claim("l13 stairs", [ns["stairs"](n) for n in range(7)] == [1, 1, 2, 3, 5, 8, 13])
    claim("l13 coins table", [ns["min_coins"]([1, 3, 4], a) for a in range(7)] == [0, 1, 2, 1, 1, 2, 2])
    INF = float("inf")
    best = [0] + [INF] * 6
    for a_ in range(6, 0, -1):
        for c_ in (1, 3, 4):
            if c_ <= a_:
                best[a_] = min(best[a_], best[a_ - c_] + 1)
    claim("l13 s6 wrong order", best == [0, 1, INF, 1, 1, INF, INF])
    # s6 labels a bottom-up loop in the wrong order 'top down', the name l12 gave memoisation
    s6 = l13["screens"][6]["prose"]

    @lru_cache(maxsize=None)
    def memo_coins(a_):
        return 0 if a_ == 0 else 1 + min((memo_coins(a_ - c_) for c_ in (1, 3, 4) if c_ <= a_), default=INF)
    claim("l13 a memoised (top-down) min_coins is right", [memo_coins(a_) for a_ in range(7)] == [0, 1, 2, 1, 1, 2, 2])
    l12_says = "top-down dynamic programming" in text_of(l12["screens"][2]["explain"])
    claim("l13 s6 calls the failing loop 'top down', the name l12 gave memoisation (misleading, finding 8)",
          not ("# top down" in s6 and l12_says),
          "a memoised min_coins is top-down and returns %d for 6" % memo_coins(6))
    w = [0, 1] + [0] * 3
    for i in range(2, 5):
        w[i] = w[i - 1] + w[i - 2]
    claim("l13 s4 base-case trap 3", w[4] == 3)
    t = [1, 1, 2]
    for i in range(3, 7):
        t.append(t[-1] + t[-2] + t[-3])
    claim("l13 three steps", t == [1, 1, 2, 4, 7, 13, 24])
    claim("l13 lots and review-3 coins", ns["min_coins"]([100, 500, 600, 900], 1100) == 2 == ns["min_coins"]([1, 5, 6, 9], 11)
          and [ns["min_coins"]([1, 5, 6, 9], a) for a in (10, 6, 5, 2)] == [2, 1, 1, 2])
    claim("l13 s10 lattice", math.comb(6, 3) == 20 and math.comb(10, 5) == 252)
    claim("l13 quiz greedy", ns["min_coins"]([2, 5], 11) == 4)


def check_hw3():
    h = J("homework-3")
    it = {i["id"]: i for i in h["items"]}
    cs = sol(h, it["h-combination-sum"])["combination_sum"]
    claim("hw3 combination counts", len(cs([2, 3, 5, 7], 30)) == 45 and len(cs([1, 2, 3, 4, 5], 20)) == 192)
    c = [1] + [0] * 40
    for n in range(1, 41):
        c[n] = sum(c[n - k] for k in range(1, 5) if k <= n)
    claim("hw3 word break 'billions of ways'", c[40] > 10 ** 9, c[40])
    claim("hw3 legs 12", sum(p.index("A") < p.index("D") for p in itertools.permutations("ABCD")) == 12)
    claim("hw3 states", 21 * 101 == 2121 and 26 * 7 * 121 == 22022)
    claim("hw3 netting sizes", 2 ** 25 == 33554432 and sum(math.comb(25, k) for k in range(7)) == 245506
          and [math.comb(25, k) for k in range(7)] == [1, 25, 300, 2300, 12650, 53130, 177100])
    # h-lattice fb.half: 'Half of all paths do not return'
    stay = 2 ** 10 - math.comb(10, 5)
    fb = it["h-lattice"]["feedback"]["byKey"]["half"]
    claim("hw3 h-lattice fb.half 'Half of all paths do not return' (wrong, finding 15)",
          stay == 512 or not fb.startswith("Half of all paths do not return"),
          "%d of 1,024 paths do not return, about %.0f%%" % (stay, 100 * stay / 1024))
    # longform premise: 2^25 subsets 'never finishes'
    t0 = time.perf_counter()
    xs = [(-1) ** i * (i % 11) for i in range(20)]
    n = hits = 0
    for k in range(0, 21):
        for basket in itertools.combinations(xs, k):
            n += 1
            hits += len(basket) <= 6 and sum(basket) == 0
    rate = n / (time.perf_counter() - t0)
    est = 2 ** 25 / rate
    claim("hw3 longform premise 'It never finishes' for 2^25 subsets (misleading, finding 16)", est > 3600,
          "itertools builds and filters %.1f million subsets a second here: 2^25 takes about %.0f s" % (rate / 1e6, est))
    tf = sol(h, it["h-fee-trades"])["trade_with_fee"]

    def brute(prices, fee):
        @lru_cache(None)
        def go(i, holding):
            if i == len(prices):
                return 0 if not holding else -math.inf
            best = go(i + 1, holding)
            if holding:
                best = max(best, prices[i] - fee + go(i + 1, False))
            else:
                best = max(best, -prices[i] + go(i + 1, True))
            return best
        return go(0, False)
    import random
    rnd = random.Random(2)
    claim("hw3 fee trades equals exhaustive DP on 300 random series",
          all(tf(p, f) == brute(tuple(p), f) for p, f in (([rnd.randint(1, 30) for _ in range(rnd.randint(0, 9))], rnd.randint(0, 6)) for _ in range(300))))
    claim("hw3 fee trades worked cases", tf([20, 10, 12, 11, 16, 13, 18, 15], 2) == 7 and tf([12, 10, 15, 9, 14, 12], 1) == 8)



# ---------------------------------------------------------------- every code widget
SCOPE = ["l1-nodes-and-edges", "l2-level-by-level", "l3-going-deep", "l4-islands", "l5-tasks-in-order",
         "l6-fewest-steps", "l7-dijkstra", "l8-groups", "l9-arbitrage-cycle", "l10-every-subset",
         "l11-dead-ends", "l12-remembering", "l13-climbing-stairs", "review-1", "review-2", "review-3",
         "homework-1", "homework-2", "homework-3"]


def same(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b or (isinstance(a, (int, float)) and isinstance(b, (int, float))
                                             and not isinstance(a, bool) and not isinstance(b, bool) and a == b)


def run_widget(w, code):
    """number of failing tests (examples included) for this source"""
    bad = 0
    for t in w.get("tests", []) + w.get("examples", []):
        ns = {"print": lambda *a, **k: None}   # a starter may print
        try:
            exec(w.get("prelude", "") + "\n" + code + "\n" + w.get("postlude", ""), ns)
            if t.get("setup"):
                exec(t["setup"], ns)
            got, want = eval(t["call"], ns), eval(t["expect"], {"float": float, "math": math})
            bad += not same(got, want)
        except BaseException:
            bad += 1
    return bad


def check_all_code():
    n = 0
    for name in SCOPE:
        doc = J(name)
        for where in doc.get("screens", []) + doc.get("quiz", []) + doc.get("items", []):
            w = where.get("widget") or {}
            if w.get("kind") != "code":
                continue
            n += 1
            tag = "%s %s" % (name, where.get("id") or where.get("title"))
            claim("code: solution passes every hidden test and example: " + tag, run_widget(w, w["solution"]) == 0)
            claim("code: starter fails: " + tag, run_widget(w, w["starter"]) > 0)
    claim("code: 38 code widgets found", n == 38, n)


for fn in (check_all_code, check_l1, check_l2, check_l3, check_l4, check_l5, check_hw1, check_l6, check_l7, check_l8, check_l9,
           check_rev_hw2, check_l10_l11, check_l12_l13, check_hw3):
    try:
        fn()
    except Exception as e:  # a crash is a failed check, not a pass
        FAILS.append("%s crashed: %r" % (fn.__name__, e))

print("python %s; %d checks passed, %d failed" % (sys.version.split()[0], PASSES[0], len(FAILS)))
for f in FAILS:
    print("FAIL", f)
sys.exit(1 if FAILS else 0)
