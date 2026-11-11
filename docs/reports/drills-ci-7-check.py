"""Check for drill pack ci, pack 7 (two-dimensional DP and backtracking): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method written here (brute force on small inputs: every route, every subset,
  every split, every placement, every arrangement, a search over strings; on large inputs a different
  algorithm: a table filled the other way, a memoised recursion, a flag state, a Pareto list) and
  compares with `expect`;
- reads the arguments of every example and test as the function receives them and checks them against
  the drill's `constraints` objects (the same rules as tools/drill-constraints.mjs) and against the
  prose constraints (`VALID`: a grid is rectangular, the stdin text parses, sizes add up);
- checks the starter fails at least one test;
- runs every planted solution on the hidden tests in its own CPython process, stopping at the first
  failure: a wrong one must fail a test inside 2.5 s; a planted solution marked too slow
  (`SLOW_PLANTED`, always last) must run past 5 s;
- times the model over all tests (under 1.5 s in CPython);
- checks the pack mix: 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700, 10 to 15
  hidden tests, 2 or 3 examples with a note, `pack-7` first in tags, two or more planted, and at
  difficulty 4 and 5 a `how` that names the obvious method and the step to the target.
With --pyodide <pkgs>, it also times, in Pyodide under node, the model and the obvious method of every
difficulty 4 and 5 drill over all hidden tests: the model must take at most 1 s (a fifth of the 5 s
limit) and the obvious method more than 5 s. The model also runs there at Pyodide's default recursion
limit, so a model that recurses too deep fails.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-7-check.py [--pyodide <pkgs>] [drill ids]
"""
import json, os, re, subprocess, sys, time, heapq, tempfile
from collections import Counter, defaultdict, deque
from functools import lru_cache
from itertools import combinations, permutations, product

sys.setrecursionlimit(20000)
HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
IDS = ["ci-drop-point-routes", "ci-spaced-picks", "ci-long-mirrors", "ci-tolerant-common", "ci-priced-edits",
       "ci-hold-limit", "ci-pillar-queens", "ci-invoice-matches", "ci-trace-count", "ci-mirror-pieces",
       "ci-three-feed-common", "ci-even-desks", "ci-merged-tape", "ci-light-cargo", "ci-smooth-orderings"]
args = sys.argv[1:]
PYODIDE = None
if "--pyodide" in args:
    k = args.index("--pyodide")
    PYODIDE = args[k + 1]
    del args[k:k + 2]
FULL = not args
if not FULL:
    IDS = args
IDS = [i for i in IDS if os.path.exists(os.path.join(DRILLS, i + ".json"))]
MOD = 10 ** 9 + 7

# ======================= constraint objects (mirror of tools/drill-constraints.mjs) =======================

def kind(v):
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "float"
    if isinstance(v, str): return "str"
    if v is None: return "None"
    if isinstance(v, (list, tuple)): return "list"
    if isinstance(v, dict): return "dict"
    return "value"

def violations(c, v, where):
    m, k = [], kind(v)
    t = c.get("type")
    if t:
        ok = k == "int" if t == "int" else k in ("int", "float") if t in ("float", "number") else k == t
        if not ok:
            return [f"{where} is {k}, not {t}"]
    if c.get("range") and k in ("int", "float"):
        lo, hi = c["range"]
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            m.append(f"{where} = {v} outside {c['range']}")
    if k in ("str", "list", "dict"):
        if c.get("len"):
            lo, hi = c["len"]
            if (lo is not None and len(v) < lo) or (hi is not None and len(v) > hi):
                m.append(f"{where} has length {len(v)}, outside {c['len']}")
        if c.get("nonEmpty") and not v:
            m.append(f"{where} is empty")
    if k == "str" and c.get("pattern") and not re.fullmatch(c["pattern"], v):
        m.append(f"{where} does not match {c['pattern']}")
    if k == "list":
        if c.get("sorted"):
            desc = c["sorted"] == "desc"
            if any((v[i - 1] < v[i]) if desc else (v[i - 1] > v[i]) for i in range(1, len(v))):
                m.append(f"{where} not sorted")
        if c.get("distinct"):
            keys = [json.dumps(x) for x in v]
            if len(set(keys)) != len(keys):
                m.append(f"{where} repeats a value")
        if "of" in c or c.get("range"):
            sub = {"range": c["range"]} if "of" not in c else ({"type": c["of"], "range": c.get("range")} if isinstance(c["of"], str) else c["of"])
            if sub.get("range") is None:
                sub = {k2: v2 for k2, v2 in sub.items() if k2 != "range"}
            for i, x in enumerate(v):
                r = violations(sub, x, f"{where}[{i}]")
                if r:
                    m += r
                    break
    return m

def capture_args(d, call):
    """the arguments the function receives in this call, by parameter name"""
    names = re.match(r"def\s+\w+\s*\(([^)]*)\)", re.search(r"^def\s+" + d["fn"] + r"\s*\(.*$", d["starter"], re.M).group(0)).group(1)
    names = [s.strip().split("=")[0].strip() for s in names.split(",") if s.strip()]
    got = []
    def grab(*a, **kw):
        got.append(dict(zip(names, a), **kw))
        return CAPTURED
    try:
        eval(call, {d["fn"]: grab})
    except Exception:
        pass
    return got

class _Captured:
    def __getattr__(self, _): return self
    def __getitem__(self, _): return self
    def __len__(self): return 0
    def __iter__(self): return iter(())
    def __call__(self, *a, **k): return self
    def __mod__(self, _): return 0
    def __eq__(self, _): return False
    def __hash__(self): return 0
CAPTURED = _Captured()
# ======================= prose constraints and independent methods, per drill =======================
VALID, INDEP = {}, {}

def rect(g):
    return len(g) >= 1 and all(len(r) == len(g[0]) for r in g)

# ---- ci-drop-point-routes
def v_drop(a):
    g = a["grid"]
    assert rect(g), "rectangular"
    assert g[0][0] != "#" and g[-1][-1] != "#", "corners open"

def drop_point_routes(grid):
    rows, cols = len(grid), len(grid[0])
    if rows + cols <= 18:                       # every route, one by one
        hits = 0
        def walk(i, j, met):
            nonlocal hits
            if i >= rows or j >= cols or grid[i][j] == "#":
                return
            met = met or grid[i][j] == "P"
            if (i, j) == (rows - 1, cols - 1):
                hits += met
                return
            walk(i + 1, j, met)
            walk(i, j + 1, met)
        walk(0, 0, False)
        return hits % MOD
    # a flag state: ways[i][j][f], f = 1 once a drop point has been met
    ways = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "#":
                continue
            into = [1, 0] if (i, j) == (0, 0) else [0, 0]
            for a, b in ((i - 1, j), (i, j - 1)):
                if a >= 0 and b >= 0:
                    into[0] += ways[a][b][0]
                    into[1] += ways[a][b][1]
            if grid[i][j] == "P":
                into = [0, into[0] + into[1]]
            ways[i][j] = [into[0] % MOD, into[1] % MOD]
    return ways[-1][-1][1]

VALID["ci-drop-point-routes"] = v_drop
INDEP["ci-drop-point-routes"] = drop_point_routes

# ---- ci-spaced-picks
def spaced_picks(values, gap):
    out = []
    for r in range(1, len(values) + 1):
        for pick in combinations(values, r):
            if all(abs(x - y) >= gap for x, y in combinations(pick, 2)):
                out.append(sorted(pick))
    return sorted(out)

VALID["ci-spaced-picks"] = lambda a: None
INDEP["ci-spaced-picks"] = spaced_picks

# ---- ci-long-mirrors
def long_mirrors(tape, k):
    n = len(tape)
    if n <= 200:
        return sum(1 for i in range(n) for j in range(i + k, n + 1) if tape[i:j] == tape[i:j][::-1])
    # a table by length: pal[L][i] says tape[i:i+L] reads the same both ways
    two_back = [True] * (n + 1)              # length 0
    one_back = [True] * n                    # length 1
    total = n if k <= 1 else 0
    for L in range(2, n + 1):
        cur = [tape[i] == tape[i + L - 1] and two_back[i + 1] for i in range(n - L + 1)]
        if L >= k:
            total += sum(cur)
        two_back, one_back = one_back, cur
    return total

VALID["ci-long-mirrors"] = lambda a: None
INDEP["ci-long-mirrors"] = long_mirrors

# ---- ci-tolerant-common
def tolerant_common(a, b, tol):
    if len(a) <= 12:                         # every choice of ticks from a, matched greedily into b
        best = 0
        for mask in range(1 << len(a)):
            pick = [a[i] for i in range(len(a)) if mask >> i & 1]
            j = 0
            ok = True
            for x in pick:
                while j < len(b) and abs(x - b[j]) > tol:
                    j += 1
                if j == len(b):
                    ok = False
                    break
                j += 1
            if ok:
                best = max(best, len(pick))
        return best
    @lru_cache(maxsize=None)
    def f(i, j):                             # best for a[i:], b[j:]
        if i == len(a) or j == len(b):
            return 0
        r = max(f(i + 1, j), f(i, j + 1))
        if abs(a[i] - b[j]) <= tol:
            r = max(r, 1 + f(i + 1, j + 1))
        return r
    r = f(0, 0)
    f.cache_clear()
    return r

VALID["ci-tolerant-common"] = lambda a: None
INDEP["ci-tolerant-common"] = tolerant_common

# ---- ci-priced-edits
def parse_edits(text):
    lines = [l.strip() for l in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    prices = [int(x) for x in lines[0].split()]
    q = int(lines[1])
    pairs = [tuple(l.split()) for l in lines[2:]]
    return prices, q, pairs

def v_edits(a):
    prices, q, pairs = parse_edits(a["text"])
    assert len(prices) == 3 and all(1 <= p <= 100 for p in prices), "prices"
    assert 1 <= q <= 50 and len(pairs) == q, "query count"
    assert all(len(p) == 2 and all(re.fullmatch("[a-z]{1,300}", w) for w in p) for p in pairs), "codes"
    assert sum(len(s) * len(t) for s, t in pairs) <= 100000, "product total"

def _edit_search(s, t, ins, dele, sub):
    """Dijkstra over the strings themselves, for short codes"""
    letters = sorted(set(s + t))
    top = len(s) + len(t)
    dist = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == t:
            return d
        if d > dist[u]:
            continue
        moves = []
        for i in range(len(u) + 1):
            if len(u) < top:
                moves += [(u[:i] + c + u[i:], ins) for c in letters]
            if i < len(u):
                moves.append((u[:i] + u[i + 1:], dele))
                moves += [(u[:i] + c + u[i + 1:], sub) for c in letters if c != u[i]]
        for v, w in moves:
            if d + w < dist.get(v, 1 << 60):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))

def solve_priced_edits(text):
    (ins, dele, sub), q, pairs = parse_edits(text)
    out = []
    for s, t in pairs:
        if len(s) + len(t) <= 7:
            out.append(_edit_search(s, t, ins, dele, sub))
            continue
        @lru_cache(maxsize=None)
        def f(i, j):                         # cheapest for s[i:] into t[j:]
            if i == len(s):
                return (len(t) - j) * ins
            if j == len(t):
                return (len(s) - i) * dele
            return min(f(i + 1, j + 1) + (0 if s[i] == t[j] else sub), f(i + 1, j) + dele, f(i, j + 1) + ins)
        for i in range(len(s), -1, -1):      # fill from the end so the recursion stays shallow
            for j in range(len(t), -1, -1):
                f(i, j)
        out.append(f(0, 0))
    return "\n".join(map(str, out))

VALID["ci-priced-edits"] = v_edits
INDEP["ci-priced-edits"] = solve_priced_edits

# ---- ci-hold-limit
def v_hold(a):
    assert len(a["weights"]) == len(a["values"]), "equal lengths"

def hold_value(weights, values, cap, k):
    n = len(weights)
    if n <= 14:                              # every subset
        best = 0
        for mask in range(1 << n):
            idx = [i for i in range(n) if mask >> i & 1]
            if len(idx) <= k and sum(weights[i] for i in idx) <= cap:
                best = max(best, sum(values[i] for i in idx))
        return best
    states = {(0, 0): 0}                     # (crates, exact weight) -> best value
    for w, v in zip(weights, values):
        nxt = dict(states)
        for (c, t), val in states.items():
            if c < k and t + w <= cap and nxt.get((c + 1, t + w), -1) < val + v:
                nxt[(c + 1, t + w)] = val + v
        states = nxt
    return max(states.values())

VALID["ci-hold-limit"] = v_hold
INDEP["ci-hold-limit"] = hold_value

# ---- ci-pillar-queens
def v_queens(a):
    b = a["board"]
    assert rect(b) and len(b) == len(b[0]), "square"
    assert a["q"] <= len(b), "q at most n"

def queen_count(board, q):
    n = len(board)
    free = [(r, c) for r in range(n) for c in range(n) if board[r][c] == "."]
    def apart(p, s):
        return p[0] != s[0] and p[1] != s[1] and abs(p[0] - s[0]) != abs(p[1] - s[1])
    if n <= 5:                               # every set of q free squares
        return sum(1 for pick in combinations(free, q) if all(apart(p, s) for p, s in combinations(pick, 2)))
    count = 0                                # squares in reading order, each taken or not
    def walk(i, chosen):
        nonlocal count
        if len(chosen) == q:
            count += 1
            return
        if len(free) - i < q - len(chosen):
            return
        walk(i + 1, chosen)
        if all(apart(free[i], s) for s in chosen):
            walk(i + 1, chosen + [free[i]])
    walk(0, [])
    return count

VALID["ci-pillar-queens"] = v_queens
INDEP["ci-pillar-queens"] = queen_count

# ---- ci-invoice-matches
def invoice_matches(amounts, target, k):
    if len(amounts) <= 14:                   # every subset of invoices, made distinct
        ways = set()
        for mask in range(1 << len(amounts)):
            pick = sorted(amounts[i] for i in range(len(amounts)) if mask >> i & 1)
            if pick and len(pick) <= k and sum(pick) == target:
                ways.add(tuple(pick))
        return [list(w) for w in sorted(ways)]
    have = sorted(Counter(amounts).items())  # how many of each amount to use
    out = []
    def walk(i, left, used, pick):
        if left == 0:
            out.append(sorted(pick))
            return
        if i == len(have) or used > k:
            return
        v, m = have[i]
        for t in range(m + 1):
            if t * v > left or used + t > k:
                break
            walk(i + 1, left - t * v, used + t, pick + [v] * t)
    walk(0, target, 0, [])
    return sorted(out)

VALID["ci-invoice-matches"] = lambda a: None
INDEP["ci-invoice-matches"] = invoice_matches

# ---- ci-trace-count
def v_trace(a):
    assert rect(a["board"]), "rectangular"

def trace_count(board, word):
    rows, cols = len(board), len(board[0])
    near = lambda i, j: [(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)) if 0 <= a < rows and 0 <= b < cols]
    if rows * cols <= 9 and len(word) <= 6:  # every sequence of squares
        cells = [(i, j) for i in range(rows) for j in range(cols)]
        return sum(1 for path in product(cells, repeat=len(word))
                   if all(board[i][j] == word[k] for k, (i, j) in enumerate(path))
                   and all(path[k + 1] in near(*path[k]) for k in range(len(word) - 1))) % MOD
    # from the last letter back: tail[i][j] = traces of word[k:] starting on (i, j)
    tail = [[1 if board[i][j] == word[-1] else 0 for j in range(cols)] for i in range(rows)]
    for k in range(len(word) - 2, -1, -1):
        tail = [[sum(tail[a][b] for a, b in near(i, j)) % MOD if board[i][j] == word[k] else 0 for j in range(cols)]
                for i in range(rows)]
    return sum(map(sum, tail)) % MOD

VALID["ci-trace-count"] = v_trace
INDEP["ci-trace-count"] = trace_count

# ---- ci-mirror-pieces
def parse_tapes(text):
    lines = [l.strip() for l in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return int(lines[0]), lines[1:]

def v_mirror(a):
    q, tapes = parse_tapes(a["text"])
    assert 1 <= q <= 50 and len(tapes) == q, "tape count"
    assert all(re.fullmatch("[a-z]{1,400}", t) for t in tapes), "tapes"
    assert sum(map(len, tapes)) <= 3000, "letters in all"

def solve_mirror_pieces(text):
    q, tapes = parse_tapes(text)
    out = []
    for t in tapes:
        n = len(t)
        if n <= 14:                          # every set of cuts
            best = n
            for mask in range(1 << (n - 1)):
                cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
                if all(t[a:b] == t[a:b][::-1] for a, b in zip(cuts, cuts[1:])):
                    best = min(best, len(cuts) - 1)
            out.append(best)
            continue
        pal = [[False] * n for _ in range(n)]  # a table of mirrored pieces, then fewest pieces from the right
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                pal[i][j] = t[i] == t[j] and (j - i < 2 or pal[i + 1][j - 1])
        rest = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            rest[i] = min(1 + rest[j + 1] for j in range(i, n) if pal[i][j])
        out.append(rest[0])
    return "\n".join(map(str, out))

VALID["ci-mirror-pieces"] = v_mirror
INDEP["ci-mirror-pieces"] = solve_mirror_pieces

# ---- ci-three-feed-common
def _is_sub(s, t):
    it = iter(t)
    return all(ch in it for ch in s)

def three_feed_common(a, b, c):
    short = min((a, b, c), key=len)
    if len(short) <= 12:                     # every subsequence of the shortest string
        best = 0
        for mask in range(1 << len(short)):
            s = "".join(short[i] for i in range(len(short)) if mask >> i & 1)
            if len(s) > best and _is_sub(s, a) and _is_sub(s, b) and _is_sub(s, c):
                best = len(s)
        return best
    @lru_cache(maxsize=None)
    def f(i, j, k):                          # from the front, remembered
        if i == len(a) or j == len(b) or k == len(c):
            return 0
        if a[i] == b[j] == c[k]:
            return 1 + f(i + 1, j + 1, k + 1)
        return max(f(i + 1, j, k), f(i, j + 1, k), f(i, j, k + 1))
    r = f(0, 0, 0)
    f.cache_clear()
    return r

VALID["ci-three-feed-common"] = lambda a: None
INDEP["ci-three-feed-common"] = three_feed_common

# ---- ci-even-desks
def v_desks(a):
    assert len(a["skills"]) % 2 == 0, "even number of traders"

def even_desks(skills):
    n, m, total = len(skills), len(skills) // 2, sum(skills)
    if n <= 16:                              # every first desk
        return min(abs(total - 2 * sum(p)) for p in combinations(skills, m))
    reach = [set() for _ in range(m + 1)]    # sets of totals per count
    reach[0].add(0)
    for x in skills:
        for c in range(m, 0, -1):
            reach[c] |= {s + x for s in reach[c - 1]}
    return min(abs(total - 2 * s) for s in reach[m])

VALID["ci-even-desks"] = v_desks
INDEP["ci-even-desks"] = even_desks

# ---- ci-merged-tape
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape):
        return 0
    if n + m <= 14:                          # every choice of the positions that go to a
        return sum(1 for pos in combinations(range(n + m), n)
                   if "".join(tape[p] for p in pos) == a
                   and "".join(tape[p] for p in range(n + m) if p not in set(pos)) == b) % MOD
    # from the end: suf[i][j] = ways to make tape[i+j:] from a[i:] and b[j:]
    suf = [[0] * (m + 1) for _ in range(n + 1)]
    suf[n][m] = 1
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n and j == m:
                continue
            ch = tape[i + j]
            v = 0
            if i < n and a[i] == ch:
                v += suf[i + 1][j]
            if j < m and b[j] == ch:
                v += suf[i][j + 1]
            suf[i][j] = v % MOD
    return suf[0][0]

VALID["ci-merged-tape"] = lambda a: None
INDEP["ci-merged-tape"] = merge_ways

# ---- ci-light-cargo
def v_cargo(a):
    assert len(a["weights"]) == len(a["values"]), "equal lengths"

def light_cargo(weights, values, cap):
    n = len(weights)
    if n <= 14:                              # every subset
        best = 0
        for mask in range(1 << n):
            idx = [i for i in range(n) if mask >> i & 1]
            if sum(weights[i] for i in idx) <= cap:
                best = max(best, sum(values[i] for i in idx))
        return best
    front = [(0, 0)]                         # Pareto list of (weight, value), weight rising, value rising
    for w, v in zip(weights, values):
        merged = sorted(front + [(fw + w, fv + v) for fw, fv in front if fw + w <= cap])
        front = []
        for fw, fv in merged:
            if not front or fv > front[-1][1]:
                if front and front[-1][0] == fw:
                    front.pop()
                front.append((fw, fv))
    return front[-1][1]

VALID["ci-light-cargo"] = v_cargo
INDEP["ci-light-cargo"] = light_cargo

# ---- ci-smooth-orderings
def smooth_orderings(sizes, d):
    n = len(sizes)
    if n <= 8:                               # every distinct arrangement
        return sum(1 for p in set(permutations(sizes)) if all(abs(x - y) <= d for x, y in zip(p, p[1:])))
    # orders of the individual orders, then divide by the shuffles of equal sizes
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        ways[1 << i][i] = 1
    for sent in range(1 << n):
        for last in range(n):
            w = ways[sent][last]
            if w:
                for j in range(n):
                    if not sent >> j & 1 and abs(sizes[last] - sizes[j]) <= d:
                        ways[sent | 1 << j][j] += w
    shuffles = 1
    for c in Counter(sizes).values():
        for t in range(2, c + 1):
            shuffles *= t
    total = sum(ways[-1])
    assert total % shuffles == 0
    return total // shuffles

VALID["ci-smooth-orderings"] = lambda a: None
INDEP["ci-smooth-orderings"] = smooth_orderings

# ======================= slow plants =======================
# planted solutions that are right but too slow (always the last entry): (drill id, index)
SLOW_PLANTED = {("ci-trace-count", 3), ("ci-mirror-pieces", 3), ("ci-three-feed-common", 2), ("ci-even-desks", 2),
                ("ci-merged-tape", 3), ("ci-light-cargo", 3), ("ci-smooth-orderings", 3)}
# the obvious method timed in Pyodide for each difficulty 4 and 5 drill: its planted index
OBVIOUS = {d: k for d, k in SLOW_PLANTED}

# ======================= running =======================

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
    out = r.stdout.strip().splitlines()
    if not out:
        return {"failed": "crash", "s": None}
    return json.loads(out[-1])

errors = []
def err(m):
    errors.append(m)
    print("ERROR", m)

PYO_SCRIPT = r"""
import json, time, sys
spec = json.loads(open(SPEC_PATH).read())
ns = {}
exec(spec["code"], ns)
t0 = time.time()
ok = True
for c in spec["cases"]:
    try:
        ok = ok and eval(c["call"], ns) == eval(c["expect"])
    except RecursionError:
        ok = False
    if time.time() - t0 > spec["cap"]:
        break
print("PYO", json.dumps({"s": round(time.time() - t0, 3), "ok": ok, "limit": sys.getrecursionlimit()}))
"""

PYO_JS = r"""
import fs from 'node:fs'; import path from 'node:path';
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
py.FS.writeFile('/spec.json', fs.readFileSync(process.argv[3], 'utf8'));
py.runPython(fs.readFileSync(process.argv[4], 'utf8'));
"""

def pyodide_time(code, cases, cap=12.0):
    """seconds Pyodide takes over the cases (stops after `cap` seconds; a run cut off reports more than 5)"""
    with tempfile.TemporaryDirectory() as tmp:
        spec, script, js = (os.path.join(tmp, f) for f in ("spec.json", "t.py", "t.mjs"))
        json.dump({"code": code, "cases": cases, "cap": cap}, open(spec, "w"))
        open(script, "w").write("SPEC_PATH = '/spec.json'\n" + PYO_SCRIPT)
        open(js, "w").write(PYO_JS)
        pkg = os.path.join(PYODIDE, "pyodide-0.27.7", "package")
        try:
            r = subprocess.run(["node", js, pkg, spec, script], capture_output=True, text=True, timeout=cap + 60)
        except subprocess.TimeoutExpired:
            return {"s": cap, "ok": None}
        line = [l for l in r.stdout.splitlines() if l.startswith("PYO ")]
        if not line:
            return {"s": None, "ok": None, "err": r.stderr[-300:]}
        return json.loads(line[-1][4:])

diffs = Counter()
stdin = 0
timings = {}
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    objs = [c for c in d["constraints"] if isinstance(c, dict)]
    if not objs:
        err(f"{did}: no constraint objects")
    for c in cases:
        got = capture_args(d, c["call"])
        if not got:
            err(f"{did}: could not read the arguments of {c['call'][:50]}")
        for a in got:
            for o in objs:
                if o["arg"] in a:
                    for m in violations(o, a[o["arg"]], o["arg"]):
                        err(f"{did}: {c['call'][:50]}: {m}")
            try:
                VALID[did](a)
            except AssertionError as e:
                err(f"{did}: {c['call'][:60]} breaks the prose constraints ({e})")
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
            if k != len(pl) - 1:
                err(f"{did}: slow planted[{k}] is not last")
            r = run_isolated(p["code"], d["tests"], limit=5)
            if r["failed"] != "timeout":
                err(f"{did}: planted[{k}] is meant to be too slow but finished ({r})")
            caught.append("timeout (slow plant)")
            continue
        r = run_isolated(p["code"], d["tests"], limit=2.5, stop=True)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython before failing a test")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(f"test {r['failed']}")
    if d["difficulty"] >= 4:
        if did not in OBVIOUS:
            err(f"{did}: difficulty {d['difficulty']} needs an obvious method in OBVIOUS")
        if "obvious method" not in d["how"] or "step to the target" not in d["how"]:
            err(f"{did}: how must name the obvious method and the step to the target")
        if PYODIDE and did in OBVIOUS:
            code = pl[OBVIOUS[did]]["code"]
            tm = pyodide_time(d["solution"], d["tests"])
            ts = pyodide_time(code, d["tests"])
            timings[did] = (tm["s"], ts["s"])
            if tm["s"] is None or tm["s"] > 1.0 or not tm["ok"]:
                err(f"{did}: model in Pyodide {tm}")
            if ts["s"] is None or ts["s"] <= 5.0:
                err(f"{did}: obvious method in Pyodide {ts}")
            print(f"  {did}: Pyodide model {tm['s']} s (recursion limit {tm.get('limit')}), obvious {ts['s']} s{' (cut off)' if ts['s'] and ts['s'] >= 12 else ''}")
    diffs[d["difficulty"]] += 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-7": err(f"{did}: tags must start pack-7")
    if ("stdin" in d["tags"]) != d["fn"].startswith("solve_"): err(f"{did}: stdin tag and solve_ name disagree")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if d["pattern"] not in ("dp", "backtracking"): err(f"{did}: pattern {d['pattern']}")
    if f"Submit runs {len(d['tests'])} hidden tests" not in d["how"]: err(f"{did}: how test count")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}")
if len(IDS) == 15 and dict(diffs) != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {dict(diffs)}")
if len(IDS) == 15 and stdin != 2: err(f"{stdin} stdin drills")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
