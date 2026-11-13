"""Check for drill pack ci, pack 4 (trees, heaps-tries): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method written here (brute force on small inputs; on large inputs a
  different algorithm: an iterative parser, a stack rebuild, Kadane on a chain, an Euler tour with
  a sparse table, a threshold search for pair sums, a sorted list, one search per word) and
  compares with `expect`;
- checks the starter fails at least one test;
- runs every planted solution on all hidden tests in its own CPython process and asserts it
  fails at least one and finishes inside 2.5 s (a planted run must never time out in the browser);
- runs each slow method in SLOW (the obvious method, kept out of `planted`) one test at a time
  and asserts some hidden test takes it past 5 s;
- times the model solution over all tests (must be under 1.5 s in CPython);
- checks the pack mix: 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700,
  10 to 15 hidden tests, 2 or 3 examples with a note, `pack-4` first in tags, two or more planted,
  and at difficulty 4 and 5 a `how` that names the obvious method.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-4-check.py [drill ids, to check only those]
"""
import json, os, subprocess, sys, time, heapq
from bisect import bisect_left, bisect_right, insort
from collections import Counter, defaultdict, deque
from itertools import permutations

import numpy as np

sys.setrecursionlimit(20000)
HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
IDS = ["ci-right-edge-view", "ci-read-preorder", "ci-busiest-links", "ci-first-misplaced",
       "ci-rebuild-from-orders", "ci-level-totals", "ci-no-repeat-rota", "ci-stock-by-prefix",
       "ci-downward-path-sums", "ci-best-route-value", "ci-handoff-distances", "ci-cheapest-pairs",
       "ci-funded-projects", "ci-live-median", "ci-board-words"]
SMALL = 12
# planted solutions that are right but too slow: each must time out on a hidden test (they come last in
# `planted`, because a timed-out run restarts Python in the browser; see BACKLOG-INBOX, drills ci 2)
SLOW_PLANTED = {("ci-live-median", 3), ("ci-stock-by-prefix", 3), ("ci-read-preorder", 3), ("ci-rebuild-from-orders", 3)}
FULL = len(sys.argv) == 1
if not FULL:
    IDS = sys.argv[1:]          # check only these drills (the mix check is then skipped)

# ---------------- independent methods ----------------

def right_edge_view(tree):
    # right side first, depth first: the first node met at each depth is the rightmost
    seen = []
    def go(t, d):
        if t is None:
            return
        if d == len(seen):
            seen.append(t[0])
        go(t[2], d + 1)
        go(t[1], d + 1)
    go(tree, 0)
    return seen

def read_tree(text):
    # iterative: a stack of nodes waiting for a child, filled left then right
    toks = text.split()
    if toks[0] == '#':
        return None
    root = [int(toks[0]), None, None]
    stack = [[root, 0]]
    for t in toks[1:]:
        node, filled = stack[-1]
        child = None if t == '#' else [int(t), None, None]
        node[1 + filled] = child
        stack[-1][1] += 1
        if stack[-1][1] == 2:
            stack.pop()
        if child is not None:
            stack.append([child, 0])
    def freeze(n):
        out, todo = {}, [n]
        order = []
        while todo:
            x = todo.pop()
            order.append(x)
            for c in (x[1], x[2]):
                if c is not None:
                    todo.append(c)
        for x in reversed(order):
            out[id(x)] = (x[0], out[id(x[1])] if x[1] is not None else None, out[id(x[2])] if x[2] is not None else None)
        return out[id(n)]
    return freeze(root)

def busiest_links(trips, k):
    c = Counter("-".join(sorted(t)) for t in trips)
    return [name for name, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]

def first_misplaced(book):
    # brute: preorder list of (price, [(ancestor price, went_left)])
    out = []
    stack = [(book, [])]
    while stack:
        node, anc = stack.pop()
        if node is None:
            continue
        out.append((node[0], anc))
        stack.append((node[2], anc + [(node[0], False)]))
        stack.append((node[1], anc + [(node[0], True)]))
    for price, anc in out:
        for a, left in anc:
            if (left and price >= a) or (not left and price <= a):
                return price
    return None

def rebuild(pre, ino):
    # the stack method: no recursion, no index map
    if not pre:
        return None
    nodes = {v: [v, None, None] for v in pre}
    stack = [nodes[pre[0]]]
    j = 0
    for v in pre[1:]:
        node = nodes[v]
        last = None
        while stack and stack[-1][0] == ino[j]:
            last = stack.pop()
            j += 1
        if last is not None:
            last[2] = node
        else:
            stack[-1][1] = node
        stack.append(node)
    def freeze(v):
        memo = {}
        order, todo = [], [nodes[v]]
        while todo:
            x = todo.pop()
            order.append(x)
            todo += [c for c in (x[1], x[2]) if c is not None]
        for x in reversed(order):
            memo[x[0]] = (x[0], memo[x[1][0]] if x[1] else None, memo[x[2][0]] if x[2] else None)
        return memo[v]
    return freeze(pre[0])

def solve_level_totals(text):
    v = [int(t) for t in text.split()]
    n = v[0]
    par, bal = v[1:1 + n], v[1 + n:1 + 2 * n]
    depth = [0] * n
    for i in range(n):              # climb with memo, iteratively
        path = []
        x = i
        while x >= 0 and depth[x] == 0:
            path.append(x)
            x = par[x]
        d = depth[x] if x >= 0 else 0
        for y in reversed(path):
            d += 1
            depth[y] = d
    tot = defaultdict(int)
    for i in range(n):
        tot[depth[i]] += bal[i]
    lvl = min(tot, key=lambda d: (-tot[d], d))
    return f"{lvl} {tot[lvl]}"

def spread_shifts(s):
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - 97] += 1
    n = len(s)
    if n <= SMALL:
        possible = n > 0 and max(cnt) <= (n + 1) // 2
    out = []
    prev = -1
    for _ in range(n):
        best = -1
        for c in range(26):
            if c != prev and cnt[c] and (best < 0 or cnt[c] > cnt[best]):
                best = c
        if best < 0:
            out = None
            break
        out.append(chr(97 + best))
        cnt[best] -= 1
        prev = best
    res = "" if out is None else "".join(out)
    if n <= SMALL:
        assert possible == (res != ""), s
        assert all(a != b for a, b in zip(res, res[1:])) and sorted(res) == (sorted(s) if res else [])
    return res

def prefix_stock(events):
    stock, by_prefix, out = {}, defaultdict(int), []
    small = len(events) <= SMALL
    for e in events:
        if e[0] == "set":
            delta = e[2] - stock.get(e[1], 0)
            stock[e[1]] = e[2]
            for L in range(len(e[1]) + 1):
                by_prefix[e[1][:L]] += delta
        else:
            got = by_prefix.get(e[1], 0)
            if small:
                assert got == sum(c for code, c in stock.items() if code.startswith(e[1]))
            out.append(got)
    return out

def _children(parent):
    ch = [[] for _ in parent]
    root = 0
    for i, p in enumerate(parent):
        if p < 0:
            root = i
        else:
            ch[p].append(i)
    return ch, root

def _is_chain(parent):
    return sum(1 for p in parent if p < 0) == 1 and len(set(p for p in parent if p >= 0)) == len(parent) - 1

def _chain_order(parent):
    ch, root = _children(parent)
    order = [root]
    while ch[order[-1]]:
        order.append(ch[order[-1]][0])
    return order

def count_sum_paths(parent, values, target):
    n = len(parent)
    if _is_chain(parent) and n > 1000:
        seq = [values[i] for i in _chain_order(parent)]
        seen, s, cnt = Counter({0: 1}), 0, 0       # subarray sums on a list
        for x in seq:
            s += x
            cnt += seen[s - target]
            seen[s] += 1
        return cnt
    cnt = 0                                        # walk up from every node
    for i in range(n):
        s, x = 0, i
        while x >= 0:
            s += values[x]
            cnt += s == target
            x = parent[x]
    return cnt

def best_route_value(parent, values):
    n = len(parent)
    if n <= SMALL:                                 # every pair of ends
        adj = defaultdict(list)
        for i, p in enumerate(parent):
            if p >= 0:
                adj[i].append(p)
                adj[p].append(i)
        best = None
        for s in range(n):
            tot = {s: values[s]}
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for w in adj[u]:
                    if w not in tot:
                        tot[w] = tot[u] + values[w]
                        dq.append(w)
            m = max(tot.values())
            best = m if best is None else max(best, m)
        return best
    if _is_chain(parent):                          # Kadane along the chain
        best = cur = None
        for i in _chain_order(parent):
            cur = values[i] if cur is None or cur < 0 else cur + values[i]
            best = cur if best is None else max(best, cur)
        return best
    # down[a] from every node walking up its ancestors (O(n h)), then the bend at each node
    pre = [0] * n
    ch, root = _children(parent)
    order = [root]
    for u in order:
        order.extend(ch[u])
    for u in order:
        pre[u] = values[u] + (pre[parent[u]] if parent[u] >= 0 else 0)
    down = [None] * n
    for u in range(n):
        x = u
        while x >= 0:
            s = pre[u] - (pre[parent[x]] if parent[x] >= 0 else 0)
            if down[x] is None or s > down[x]:
                down[x] = s
            x = parent[x]
    best = None
    for a in range(n):
        g = sorted((max(0, down[c]) for c in ch[a]), reverse=True)[:2]
        here = values[a] + sum(g)
        best = here if best is None else max(best, here)
    return best

def handoff_distances(parent, queries):
    n = len(parent)
    ch, root = _children(parent)
    depth = [0] * n
    if n <= 3000:                                  # climb one line at a time
        order = [root]
        for u in order:
            for c in ch[u]:
                depth[c] = depth[u] + 1
                order.append(c)
        out = []
        for a, b in queries:
            x, y, steps = a, b, 0
            while x != y:
                if depth[x] >= depth[y]:
                    x = parent[x]
                else:
                    y = parent[y]
                steps += 1
            out.append(steps)
        return out
    # Euler tour and a sparse table of (depth, node) minima
    euler, first = [], [0] * n
    stack = [(root, 0)]
    while stack:
        u, k = stack.pop()
        if k == 0:
            first[u] = len(euler)
        euler.append((depth[u], u))
        if k < len(ch[u]):
            c = ch[u][k]
            depth[c] = depth[u] + 1
            stack.append((u, k + 1))
            stack.append((c, 0))
    table = [euler]
    j = 1
    while 2 * j <= len(euler):
        prev = table[-1]
        table.append([min(prev[i], prev[i + j]) for i in range(len(euler) - 2 * j + 1)])
        j *= 2
    out = []
    for a, b in queries:
        l, r = sorted((first[a], first[b]))
        k = (r - l + 1).bit_length() - 1
        lca_d = min(table[k][l], table[k][r - (1 << k) + 1])[0]
        out.append(depth[a] + depth[b] - 2 * lca_d)
    return out

def cheapest_pairs(a, b, k):
    if not a or not b or k == 0:
        return []
    if len(a) * len(b) <= 10000:
        return sorted(x + y for x in a for y in b)[:k]
    A, B = np.array(a, dtype=np.int64), np.array(b, dtype=np.int64)
    def count_le(t):
        return int(np.searchsorted(B, t - A, side="right").sum())
    lo, hi = int(A[0] + B[0]), int(A[-1] + B[-1])
    while lo < hi:                                 # smallest t with at least k sums <= t
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    out = []
    for x in a:
        if x + b[0] > lo - 1:
            break
        out.extend(x + y for y in b[:bisect_right(b, lo - 1 - x)])
    out.sort()
    return out + [lo] * (k - len(out))

def funded_projects(capital, k, projects):
    if len(projects) <= 6:                         # every order of every choice
        best = capital
        for r in range(min(k, len(projects)) + 1):
            for perm in permutations(range(len(projects)), r):
                c, ok = capital, True
                for i in perm:
                    if projects[i][0] > c:
                        ok = False
                        break
                    c += projects[i][1]
                if ok:
                    best = max(best, c)
        return best
    # the greedy with a sorted list of open profits instead of a heap
    order = sorted(projects, key=lambda p: p[0])
    open_profits, i = [], 0
    for _ in range(k):
        while i < len(order) and order[i][0] <= capital:
            insort(open_profits, order[i][1])
            i += 1
        if not open_profits:
            break
        capital += open_profits.pop()
    return capital

def solve_live_median(text):
    t = text.split()
    q = int(t[0]) if t else 0
    live, out = [], []
    for i in range(q):
        op, x = t[1 + 2 * i], int(t[2 + 2 * i])
        if op == "+":
            insort(live, x)
        else:
            del live[bisect_left(live, x)]
        out.append(str(live[(len(live) + 1) // 2 - 1]) if live else "-")
    return " ".join(out)

def board_words(board, words):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    def on(w):                                     # one search per word
        used = set()
        def go(r, c, i):
            if board[r][c] != w[i]:
                return False
            if i == len(w) - 1:
                return True
            used.add((r, c))
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in used and go(nr, nc, i + 1):
                    used.discard((r, c))
                    return True
            used.discard((r, c))
            return False
        return any(go(r, c, 0) for r in range(rows) for c in range(cols))
    return sorted(w for w in words if on(w))

INDEP = {
    "ci-right-edge-view": right_edge_view, "ci-read-preorder": read_tree,
    "ci-busiest-links": busiest_links, "ci-first-misplaced": first_misplaced,
    "ci-rebuild-from-orders": rebuild, "ci-level-totals": solve_level_totals,
    "ci-no-repeat-rota": spread_shifts, "ci-stock-by-prefix": prefix_stock,
    "ci-downward-path-sums": count_sum_paths, "ci-best-route-value": best_route_value,
    "ci-handoff-distances": handoff_distances, "ci-cheapest-pairs": cheapest_pairs,
    "ci-funded-projects": funded_projects, "ci-live-median": solve_live_median,
    "ci-board-words": board_words,
}

# ---------------- the obvious methods, too slow ----------------
# Kept out of `planted`: a planted run that times out on the drill page restarts Python, and the
# playthrough then reads stale results (BACKLOG-INBOX, drills ci 2). Each must run past 5 s on one
# hidden test in CPython, which is faster than Pyodide, so it also fails the browser's limit.
SLOW = {
    "ci-downward-path-sums": [
        "def count_sum_paths(parent, values, target):\n    count = 0\n    for start in range(len(parent)):\n        total, node = 0, start\n        while node >= 0:\n            total += values[node]\n            if total == target:\n                count += 1\n            node = parent[node]\n    return count\n",
    ],
    "ci-best-route-value": [
        "def best_route_value(parent, values):\n    n = len(parent)\n    adj = [[] for _ in range(n)]\n    for i, p in enumerate(parent):\n        if p >= 0:\n            adj[i].append(p)\n            adj[p].append(i)\n    best = None\n    for s in range(n):\n        total = {s: values[s]}\n        stack = [s]\n        while stack:\n            u = stack.pop()\n            if best is None or total[u] > best:\n                best = total[u]\n            for w in adj[u]:\n                if w not in total:\n                    total[w] = total[u] + values[w]\n                    stack.append(w)\n    return best\n",
    ],
    "ci-handoff-distances": [
        "def handoff_distances(parent, queries):\n    n = len(parent)\n    depth = [-1] * n\n    def d(v):\n        path = []\n        while v >= 0 and depth[v] < 0:\n            path.append(v)\n            v = parent[v]\n        base = depth[v] if v >= 0 else -1\n        for u in reversed(path):\n            base += 1\n            depth[u] = base\n    for v in range(n):\n        d(v)\n    out = []\n    for a, b in queries:\n        steps = 0\n        while a != b:\n            if depth[a] >= depth[b]:\n                a = parent[a]\n            else:\n                b = parent[b]\n            steps += 1\n        out.append(steps)\n    return out\n",
    ],
    "ci-cheapest-pairs": [
        "import heapq\n\ndef cheapest_pairs(a, b, k):\n    return heapq.nsmallest(k, (x + y for x in a for y in b))\n",
    ],
    "ci-funded-projects": [
        "def funded_projects(capital, k, projects):\n    used = [False] * len(projects)\n    for _ in range(k):\n        pick = -1\n        for i, (need, profit) in enumerate(projects):\n            if not used[i] and need <= capital and (pick < 0 or profit > projects[pick][1]):\n                pick = i\n        if pick < 0:\n            break\n        used[pick] = True\n        capital += projects[pick][1]\n    return capital\n",
    ],
    "ci-live-median": [
        "def solve_live_median(text):\n    tokens = text.split()\n    q = int(tokens[0]) if tokens else 0\n    live, out = [], []\n    for i in range(q):\n        op, x = tokens[1 + 2 * i], int(tokens[2 + 2 * i])\n        if op == '+':\n            live.append(x)\n        else:\n            live.remove(x)\n        live.sort()\n        out.append(str(live[(len(live) + 1) // 2 - 1]) if live else '-')\n    return ' '.join(out)\n",
    ],
    "ci-board-words": [
        "def board_words(board, words):\n    rows = len(board)\n    cols = len(board[0]) if rows else 0\n\n    def on_board(word):\n        used = set()\n\n        def go(r, c, i):\n            if board[r][c] != word[i]:\n                return False\n            if i == len(word) - 1:\n                return True\n            used.add((r, c))\n            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):\n                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in used and go(nr, nc, i + 1):\n                    used.discard((r, c))\n                    return True\n            used.discard((r, c))\n            return False\n\n        return any(go(r, c, 0) for r in range(rows) for c in range(cols))\n\n    return sorted(w for w in words if on_board(w))\n",
        "from collections import Counter\n\ndef board_words(board, words):\n    rows = len(board)\n    cols = len(board[0]) if rows else 0\n    have = Counter(\"\".join(board))\n    grid = [list(r) for r in board]\n\n    def trace(word):\n        if any(have[ch] < c for ch, c in Counter(word).items()):\n            return False\n        last = len(word) - 1\n\n        def go(r, c, i):\n            if grid[r][c] != word[i]:\n                return False\n            if i == last:\n                return True\n            grid[r][c] = \".\"\n            ok = False\n            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):\n                if 0 <= nr < rows and 0 <= nc < cols and go(nr, nc, i + 1):\n                    ok = True\n                    break\n            grid[r][c] = word[i]\n            return ok\n\n        return any(go(r, c, 0) for r in range(rows) for c in range(cols))\n\n    return sorted(w for w in words if trace(w))\n",
    ],
}

# A slow method that must reach one named test: the per-word search with the letter-count check first
# passes tests[0..11] and is stopped only by the 3,602-word test (the 12th, index 12).
SLOW_AT = {("ci-board-words", 1): 12}

# ---------------- running ----------------

RUNNER = r"""
import json, sys, time
sys.setrecursionlimit(1000)
spec = json.load(sys.stdin)
ns = {}
exec(spec["code"], ns)
first = None
t0 = time.time()
for i, c in enumerate(spec["cases"]):
    try:
        ok = eval(c["call"], ns) == eval(c["expect"])
    except Exception as e:
        ok = False
    if not ok and first is None:
        first = i
    if spec.get("stop") and first is not None:
        break
print(json.dumps({"failed": first, "s": round(time.time() - t0, 2)}))
"""

def run_isolated(code, cases, limit=10, stop=False):
    try:
        r = subprocess.run([sys.executable, "-c", RUNNER], input=json.dumps({"code": code, "cases": cases, "stop": stop}),
                           capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"failed": "timeout", "s": limit}
    return json.loads(r.stdout.strip().splitlines()[-1])

errors = []
def err(m):
    errors.append(m)
    print("ERROR", m)

diffs = Counter()
stdin = 0
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    ns = {}
    exec(d["solution"], ns)
    t0 = time.time()
    for c in cases:
        if eval(c["call"], ns) != eval(c["expect"]):
            err(f"{did}: model fails {c['call'][:60]}")
    dt = time.time() - t0
    if dt > 1.5:
        err(f"{did}: model took {dt:.2f} s")
    ins = {fn: INDEP[did]}
    for c in cases:
        if eval(c["call"], ins) != eval(c["expect"]):
            err(f"{did}: independent method disagrees on {c['call'][:60]}")
    sres = run_isolated(d["starter"], d["tests"])
    if sres["failed"] is None:
        err(f"{did}: starter passes every test")
    pl = d.get("planted", [])
    if len(pl) < 2:
        err(f"{did}: fewer than two planted")
    caught = []
    for k, p in enumerate(pl):
        if (did, k) in SLOW_PLANTED:
            r = run_isolated(p["code"], d["tests"], limit=5)
            if r["failed"] != "timeout":
                err(f"{did}: planted[{k}] is meant to be too slow but did not time out")
            caught.append("timeout (slow plant)")
            continue
        r = run_isolated(p["code"], d["tests"], limit=2.5)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython, so it could time out in the browser")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(f"test {r['failed']} in {r['s']} s")
    slow_out = []
    for k, code in enumerate(SLOW.get(did, [])):
        hit = None
        for i, c in enumerate(d["tests"]):
            r = run_isolated(code, [c], limit=5)
            if r["failed"] == "timeout":
                hit = i
                break
        if hit is None:
            err(f"{did}: slow method {k} finishes every hidden test inside 5 s")
        elif (did, k) in SLOW_AT and hit != SLOW_AT[(did, k)]:
            err(f"{did}: slow method {k} should time out at test {SLOW_AT[(did, k)]} but did at {hit}")
        slow_out.append(hit)
    if d["difficulty"] >= 4:
        if did not in SLOW:
            err(f"{did}: difficulty {d['difficulty']} needs a slow method in SLOW")
        if "obvious method" not in d["how"] or "step to the target" not in d["how"]:
            err(f"{did}: how must name the obvious method and the step to the target")
    diffs[d["difficulty"]] += 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-4": err(f"{did}: tags must start pack-4")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if d["pattern"] not in ("trees", "heaps-tries"): err(f"{did}: pattern {d['pattern']}")
    if f"Submit runs {len(d['tests'])} hidden tests" not in d["how"]: err(f"{did}: how test count")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}, slow methods time out at {slow_out}")
if FULL and dict(diffs) != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {dict(diffs)}")
if FULL and stdin != 2: err(f"{stdin} stdin drills")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
