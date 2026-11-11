"""Check for drill pack ci, pack 6 (one-dimensional dynamic programming): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method written here and compares with `expect`: brute force on small inputs (every
  subset, every stride sequence, every tiling, every fill of the smudges, every multiset of tokens, every
  stretch, every pair of crates) and on large inputs a different algorithm (prefix minima, a state machine,
  a cell-by-cell profile, a breadth-first search over positions, a Fenwick tree, the Kitamasa method,
  numpy sums by residue, a backward table);
- reads the arguments of every example and test as the function receives them and checks them against
  the drill's `constraints` objects (the same rules as tools/drill-constraints.mjs) and against the
  prose constraints (`VALID`, e.g. a broken step is at most `n`, a stdin text has the counts it states);
- checks the starter fails at least one test;
- runs every planted solution on all hidden tests in its own CPython process: a wrong one must fail a
  test inside 2.5 s; a planted solution marked too slow (`SLOW_PLANTED`, always last) must run past 5 s;
- times the model over all tests (under 1.5 s in CPython);
- checks the pack mix: 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700, 10 to 15
  hidden tests, 2 or 3 examples with a note, `pack-6` first in tags, two or more planted, and at
  difficulty 4 and 5 a `how` that names the obvious method and the step to the target.
With --pyodide <pkgs>, it also times, in Pyodide under node, the model and the obvious method of every
difficulty 4 and 5 drill over all hidden tests: the model must take at most 1 s (a fifth of the 5 s
limit) and the obvious method more than 5 s. The model runs at Pyodide's default recursion limit.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-6-check.py [--pyodide <pkgs>] [drill ids]
"""
import json, os, re, subprocess, sys, time, tempfile
from bisect import bisect_left
from collections import deque
from functools import lru_cache
from itertools import combinations, product as iproduct
import numpy as np

sys.setrecursionlimit(20000)
MOD = 1_000_000_007
HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
IDS = ["ci-broken-steps", "ci-best-session", "ci-shift-picks", "ci-ring-stalls", "ci-change-ways",
       "ci-product-stretch", "ci-paving-ways", "ci-cooldown-trades", "ci-word-split", "ci-longest-rising",
       "ci-tape-decodes", "ci-fewest-tokens", "ci-long-stairwell", "ci-nested-crates", "ci-capped-trips"]
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
        return None
    eval(call, {d["fn"]: grab})
    return got

# ======================= prose constraints, per drill =======================

def v_broken(a):
    assert all(1 <= b <= a["n"] for b in a["broken"]), "a broken step above n"

def v_change(a):
    lines = a["text"].split()
    k = int(lines[0])
    coins = [int(x) for x in lines[1:1 + k]]
    q = int(lines[1 + k])
    fares = [int(x) for x in lines[2 + k:]]
    assert 1 <= k <= 20 and len(coins) == k and len(set(coins)) == k, "coins"
    assert all(1 <= c <= 20000 for c in coins), "coin range"
    assert 1 <= q <= 100000 and len(fares) == q, "fare count"
    assert all(0 <= f <= 20000 for f in fares), "fare range"
    rows = [r for r in a["text"].split("\n") if r.strip()]
    assert rows[0].strip() == str(k) and len(rows[1].split()) == k and rows[2].strip() == str(q), "line layout"

def v_paving(a):
    cells = [tuple(x) for x in a["drains"]]
    assert len(set(cells)) == len(cells), "a repeated drain"
    assert all(0 <= r <= 2 and 0 <= c < a["n"] for r, c in cells), "a drain off the pavement"

def v_tape(a):
    rows = [r.strip() for r in a["text"].split("\n")]
    while rows and not rows[-1]:
        rows.pop()
    t = int(rows[0])
    tapes = rows[1:]
    assert 1 <= t <= 1000 and len(tapes) == t, "tape count"
    assert all(re.fullmatch(r"[0-9?]+", x) for x in tapes), "tape characters"
    assert sum(map(len, tapes)) <= 200000, "total length"

def v_none(a):
    pass

VALID = {"ci-broken-steps": v_broken, "ci-change-ways": v_change, "ci-paving-ways": v_paving, "ci-tape-decodes": v_tape}

# ======================= independent methods =======================

def ways_up(n, broken):
    bad = set(broken)
    if n <= 18:
        def walk(i):
            if i > n or i in bad: return 0
            if i == n: return 1
            return walk(i + 1) + walk(i + 2) + walk(i + 3)
        return walk(0) % MOD
    f = [0] * (n + 4)
    f[0] = 1
    for i in range(n + 1):
        if i in bad:
            f[i] = 0
            continue
        for s in (1, 2, 3):
            f[i + s] = (f[i + s] + f[i]) % MOD
    return f[n]

def best_session(pnl):
    n = len(pnl)
    if n <= 60:
        best = None
        for s in range(n):
            for e in range(s, n):
                t = sum(pnl[s:e + 1])
                if best is None or t > best[0]:
                    best = [t, s, e]
        return best
    # prefix sums: best run ending at e starts after the earliest smallest prefix
    best = None
    pre = 0
    lo, lo_at = 0, 0          # smallest prefix P[j] for j <= e, earliest j
    for e, x in enumerate(pnl):
        nxt = pre + x
        t = nxt - lo
        cand = [t, lo_at, e]
        if best is None or t > best[0] or (t == best[0] and lo_at < best[1]):
            best = cand
        pre = nxt
        if pre < lo:
            lo, lo_at = pre, e + 1
    return best

def best_shifts(pay):
    n = len(pay)
    if n <= 16:
        best = (0, 0)
        for m in range(1 << n):
            if m & (m >> 1): continue
            ch = [i for i in range(n) if m >> i & 1]
            best = max(best, (sum(pay[i] for i in ch), -len(ch)))
        return [best[0], -best[1]]
    rest, work = (0, 0), (-1, 0)   # best ending with day i rested / worked
    for x in pay:
        rest, work = max(rest, work), (rest[0] + x, rest[1] - 1)
    b = max(rest, work)
    return [b[0], -b[1]]

def best_rent(r):
    n = len(r)
    if n <= 16:
        best = 0
        for m in range(1 << n):
            ch = [i for i in range(n) if m >> i & 1]
            if all(min(b - a, n - b + a) >= 3 for a, b in combinations(ch, 2)):
                best = max(best, sum(r[i] for i in ch))
        return best
    # state machine: (first taken, capped at 3; -1 none), gap since last taken capped at 3, more than one taken
    states = {(-1, 3, False): 0}
    for i, x in enumerate(r):
        new = {}
        def put(s, v):
            if new.get(s, -1) < v: new[s] = v
        for (f, g, many), v in states.items():
            put((f, min(g + 1, 3), many), v)
            if f == -1:
                put((min(i, 3), 0, False), v + x)
            elif g + 1 >= 3:
                put((f, 0, True), v + x)
        states = new
    best = 0
    for (f, g, many), v in states.items():
        if f == -1 or not many or f >= 3 or g >= 3 or f + g + 1 >= 3:
            best = max(best, v)
    return best

def solve_change_ways(text):
    nums = [int(x) for x in re.findall(r"\d+", text)]
    k = nums[0]
    coins = nums[1:1 + k]
    q = nums[1 + k]
    fares = nums[2 + k:2 + k + q]
    top = max(fares)
    if top <= 300:
        @lru_cache(None)
        def ways(i, a):
            if a == 0: return 1
            if i == len(coins): return 0
            return sum(ways(i + 1, a - t * coins[i]) for t in range(a // coins[i] + 1))
        return "\n".join(str(ways(0, f) % MOD) for f in fares)
    w = np.zeros(top + 1, dtype=np.int64)
    w[0] = 1
    for c in coins:
        for res in range(min(c, top + 1)):
            w[res::c] = np.cumsum(w[res::c]) % MOD
    return "\n".join(str(int(w[f])) for f in fares)

def best_product_stretch(f):
    best = None
    for s in range(len(f)):
        p = f[s]
        for e in range(s + 1, len(f)):
            p *= f[e]
            if best is None or p > best:
                best = p
            if p == 0 and best is not None and best >= 0:
                break
    return best

def paving_ways(n, drains):
    blocked = {(r, c) for r, c in drains}
    if 3 * n <= 24:
        filled = set(blocked)
        def go():
            for c in range(n):
                for r in range(3):
                    if (r, c) not in filled:
                        t = 0
                        for cell in ((r, c + 1), (r + 1, c)):
                            if cell[0] < 3 and cell[1] < n and cell not in filled:
                                filled.add((r, c)); filled.add(cell)
                                t += go()
                                filled.discard((r, c)); filled.discard(cell)
                        return t
            return 1
        return go() % MOD
    # cell by cell, column major: bit r says whether (r, current or next column) is already covered
    dp = {0: 1}
    for c in range(n):
        for r in range(3):
            new = {}
            for mask, w in dp.items():
                bit = 1 << r
                if (r, c) in blocked:
                    if mask & bit: continue
                    new[mask] = (new.get(mask, 0) + w) % MOD
                elif mask & bit:
                    m2 = mask & ~bit
                    new[m2] = (new.get(m2, 0) + w) % MOD
                else:
                    if c + 1 < n and (r, c + 1) not in blocked:
                        new[mask | bit] = (new.get(mask | bit, 0) + w) % MOD
                    if r < 2 and not mask & (bit << 1) and (r + 1, c) not in blocked:
                        m2 = mask | (bit << 1)
                        new[m2] = (new.get(m2, 0) + w) % MOD
            dp = new
    return dp.get(0, 0)

def cooldown_profit(prices, k):
    n = len(prices)
    if n <= 12:
        @lru_cache(None)
        def go(i, state):   # state: 'f' free, 'h' holding, or an int of rest days left
            if i == n: return 0
            p = prices[i]
            if state == "h":
                return max(go(i + 1, "h"), p + go(i + 1, k if k else "f"))
            if state == "f":
                return max(go(i + 1, "f"), go(i + 1, "h") - p)
            return go(i + 1, state - 1 if state > 1 else "f")
        return go(0, "f")
    if k + 1 >= n:
        best, low = 0, prices[0]
        for p in prices:
            best, low = max(best, p - low), min(low, p)
        return best
    NEG = -10 ** 18
    free, hold = 0, NEG
    rest = [NEG] * (k + 1)      # rest[r]: sold, r more days to sit out (r = 0 means free from tomorrow)
    for p in prices:
        nf = max(free, rest[0])
        nh = max(hold, free - p)
        nr = rest[1:] + [NEG]
        sold = hold + p
        if k == 0:
            nf = max(nf, sold)
        else:
            nr[k - 1] = max(nr[k - 1], sold)
        free, hold, rest = nf, nh, nr
    return max(free, max(rest))

def fewest_words(text, words):
    vocab = set(words)
    lens = {len(w) for w in words}
    n = len(text)
    dist = [-1] * (n + 1)
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        for L in lens:
            j = i + L
            if j <= n and dist[j] < 0 and text[i:j] in vocab:
                dist[j] = dist[i] + 1
                q.append(j)
    return dist[n]

def rising_readings(a):
    n = len(a)
    if n <= 2000:
        L = [1] * n
        for i in range(n):
            for j in range(i):
                if a[j] < a[i]: L[i] = max(L[i], L[j] + 1)
        top = max(L)
        return [top, min(a[i] for i in range(n) if L[i] == top)]
    vals = sorted(set(a))
    pos = {v: i + 1 for i, v in enumerate(vals)}
    tree = [0] * (len(vals) + 1)
    L = []
    for x in a:
        i, best = pos[x] - 1, 0
        while i > 0:
            best = max(best, tree[i]); i -= i & -i
        L.append(best + 1)
        i = pos[x]
        while i < len(tree):
            tree[i] = max(tree[i], best + 1); i += i & -i
    top = max(L)
    return [top, min(a[i] for i in range(n) if L[i] == top)]

CODES = [str(c) for c in range(1, 27)]

def tape_count(tape):
    if len(tape) <= 12 and tape.count("?") <= 4:
        total = 0
        spots = [i for i, ch in enumerate(tape) if ch == "?"]
        for fill in iproduct("0123456789", repeat=len(spots)):
            s = list(tape)
            for i, d in zip(spots, fill): s[i] = d
            s = "".join(s)
            def dec(i):
                if i == len(s): return 1
                t = 0
                if s[i] != "0":
                    t += dec(i + 1)
                    if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26: t += dec(i + 2)
                return t
            total += dec(0)
        return total % MOD
    f = [0] * (len(tape) + 1)
    f[0] = 1
    for i in range(len(tape)):
        if not f[i]: continue
        for code in CODES:
            piece = tape[i:i + len(code)]
            if len(piece) == len(code) and all(p == "?" or p == c for p, c in zip(piece, code)):
                f[i + len(code)] = (f[i + len(code)] + f[i]) % MOD
    return f[-1]

def solve_tape_decodes(text):
    rows = [r.strip() for r in text.splitlines()]
    rows = [r for r in rows if r]
    t = int(rows[0])
    return "\n".join(str(tape_count(x)) for x in rows[1:1 + t])

def fewest_tokens(values, amount):
    if amount <= 40:
        best = None
        vs = sorted(values, reverse=True)
        def go(i, left, cur):
            nonlocal best
            if left == 0:
                key = (-len(cur), cur)
                if best is None or key > best: best = (-len(cur), list(cur))
                return
            if i == len(vs): return
            v = vs[i]
            for t in range(left // v, -1, -1):
                go(i + 1, left - t * v, cur + [v] * t)
        go(0, amount, [])
        return [] if best is None else best[1]
    dist = [-1] * (amount + 1)
    dist[0] = 0
    q = deque([0])
    while q:
        a = q.popleft()
        for v in values:
            b = a + v
            if b <= amount and dist[b] < 0:
                dist[b] = dist[a] + 1
                q.append(b)
    if dist[amount] < 0: return []
    out, a = [], amount
    for _ in range(dist[amount]):
        v = max(v for v in values if v <= a and dist[a - v] == dist[a] - 1)
        out.append(v); a -= v
    return out

def stride_ways(n, strides):
    m = max(strides)
    if n <= 100000:
        f = [1] + [0] * n
        for i in range(1, n + 1):
            f[i] = sum(f[i - s] for s in strides if s <= i) % MOD
        return f[n]
    # Kitamasa: x^n modulo x^m - sum_{s} x^{m - s}
    init = [1] + [0] * (m - 1)
    for i in range(1, m):
        init[i] = sum(init[i - s] for s in strides if s <= i) % MOD
    rec = [0] * (m + 1)          # x^m = sum rec[j] x^j
    for s in strides: rec[m - s] += 1
    def mulmod(a, b):
        prod = [0] * (2 * m - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    prod[i + j] += x * y
        for d in range(2 * m - 2, m - 1, -1):
            c = prod[d] % MOD
            if c:
                for j in range(m):
                    prod[d - m + j] += c * rec[j]
            prod[d] = 0
        return [x % MOD for x in prod[:m]]
    res = [1] + [0] * (m - 1)
    base = [0] * m
    if m == 1:
        base = [rec[0] % MOD]
    else:
        base[1] = 1
    e = n
    while e:
        if e & 1: res = mulmod(res, base)
        base = mulmod(base, base)
        e >>= 1
    return sum(c * v for c, v in zip(res, init)) % MOD

def longest_nest(crates):
    n = len(crates)
    if n <= 2000:
        best = [1] * n
        order = sorted(crates)
        for i in range(n):
            for j in range(n):
                if order[j][0] < order[i][0] and order[j][1] <= order[i][1]:
                    best[i] = max(best[i], best[j] + 1)
        return max(best) if n else 0
    hs = sorted({h for _, h in crates})
    pos = {h: i + 1 for i, h in enumerate(hs)}
    tree = [0] * (len(hs) + 1)
    def query(i):
        b = 0
        while i > 0: b = max(b, tree[i]); i -= i & -i
        return b
    def add(i, v):
        while i < len(tree): tree[i] = max(tree[i], v); i += i & -i
    by_w = {}
    for w, h in crates: by_w.setdefault(w, []).append(h)
    top = 0
    for w in sorted(by_w):
        got = [(pos[h], query(pos[h]) + 1) for h in by_w[w]]
        for p, v in got:
            add(p, v); top = max(top, v)
    return top

def best_trips(prices, k, fee):
    n = len(prices)
    NEG = -10 ** 18
    nxt_free = [0] * (k + 1)       # value from day i on, no share, `left` trips left
    nxt_hold = [NEG] * (k + 1)     # holding the share of a trip already counted
    for i in range(n - 1, -1, -1):
        p = prices[i]
        cur_free = [max(nxt_free[l], (nxt_hold[l - 1] - p) if l else NEG) for l in range(k + 1)]
        cur_hold = [max(nxt_hold[l], p - fee + nxt_free[l]) for l in range(k + 1)]
        nxt_free, nxt_hold = cur_free, cur_hold
    return nxt_free[k]

INDEP = {"ci-broken-steps": ways_up, "ci-best-session": best_session, "ci-shift-picks": best_shifts,
         "ci-ring-stalls": best_rent, "ci-change-ways": solve_change_ways, "ci-product-stretch": best_product_stretch,
         "ci-paving-ways": paving_ways, "ci-cooldown-trades": cooldown_profit, "ci-word-split": fewest_words,
         "ci-longest-rising": rising_readings, "ci-tape-decodes": solve_tape_decodes, "ci-fewest-tokens": fewest_tokens,
         "ci-long-stairwell": stride_ways, "ci-nested-crates": longest_nest, "ci-capped-trips": best_trips}

# planted solutions that are right but too slow: (drill id, index). Each must run past 5 s natively, or, for the
# few that finish natively in 4 to 5 s on the largest allowed input, past 5 s in Pyodide (see --pyodide).
SLOW_PLANTED = {(d, 2) for d in ("ci-word-split", "ci-longest-rising", "ci-tape-decodes", "ci-fewest-tokens",
                                  "ci-long-stairwell", "ci-nested-crates", "ci-capped-trips")}
SLOW_PLANTED |= {("ci-best-session", 3), ("ci-word-split", 3), ("ci-longest-rising", 3), ("ci-longest-rising", 4),
                 ("ci-nested-crates", 3), ("ci-paving-ways", 4)}
SOFT_SLOW = {("ci-word-split", 3)}   # about 4.7 s natively on the 5,000-code test; the Pyodide run is the gate
OBVIOUS = {d: 2 for d, _ in SLOW_PLANTED if d not in ("ci-best-session", "ci-paving-ways")}
OBVIOUS["ci-paving-ways"] = 4
EXPECT_PLANTED = {"ci-best-session": 4, "ci-shift-picks": 4, "ci-product-stretch": 4, "ci-paving-ways": 5,
                  "ci-word-split": 4, "ci-longest-rising": 5, "ci-fewest-tokens": 5, "ci-nested-crates": 4,
                  "ci-capped-trips": 6}   # planted count after the fix pass (finding: 12 wrong candidates added)
WANT_DIFF = {"ci-longest-rising": 3, "ci-paving-ways": 4, "ci-capped-trips": 4, "ci-long-stairwell": 5}

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
    return json.loads(r.stdout.strip().splitlines()[-1])

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
        print("PYO-RECURSION")
    if time.time() - t0 > spec["cap"]:
        break
print("PYO", json.dumps({"s": round(time.time() - t0, 3), "ok": ok}))
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
        res = json.loads(line[-1][4:])
        res["recursion"] = "PYO-RECURSION" in r.stdout
        return res

diffs = {}
stdin = 0
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    objs = [c for c in d["constraints"] if isinstance(c, dict)]
    if not objs:
        err(f"{did}: no constraint objects")
    for c in cases:
        got = capture_args(d, c["call"])
        if len(got) != 1:
            err(f"{did}: {c['call'][:50]} calls the function {len(got)} times")
        for a in got:
            for o in objs:
                if o["arg"] not in a:
                    err(f"{did}: {o['arg']} missing from {c['call'][:50]}")
                    continue
                for m in violations(o, a[o["arg"]], o["arg"]):
                    err(f"{did}: {c['call'][:50]}: {m}")
            try:
                VALID.get(did, v_none)(a)
            except (AssertionError, ValueError, IndexError) as e:
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
            r = run_isolated(p["code"], d["tests"], limit=5)
            if (did, k) in SOFT_SLOW and r["failed"] is None and r["s"] >= 3.5:
                caught.append(f"slow plant, {r['s']} s natively")
                continue
            if r["failed"] != "timeout":
                err(f"{did}: planted[{k}] is meant to be too slow but finished ({r})")
            caught.append("timeout (slow plant)")
            continue
        r = run_isolated(p["code"], d["tests"], limit=2.5)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython, so it could time out in the browser")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(f"test {r['failed']} in {r['s']} s")
    if did in EXPECT_PLANTED and len(pl) != EXPECT_PLANTED[did]:
        err(f"{did}: {len(pl)} planted, expected {EXPECT_PLANTED[did]}")
    if did in WANT_DIFF and d["difficulty"] != WANT_DIFF[did]:
        err(f"{did}: difficulty {d['difficulty']}, expected {WANT_DIFF[did]}")
    if PYODIDE:
        for (sd, sk) in sorted(SLOW_PLANTED):
            if sd == did and (sd, sk) in SOFT_SLOW:
                ts = pyodide_time(pl[sk]["code"], d["tests"])
                if ts["s"] is None or ts["s"] <= 5.0:
                    err(f"{did}: planted[{sk}] in Pyodide {ts}")
                print(f"  {did}: planted[{sk}] in Pyodide {ts['s']} s")
    if d["difficulty"] >= 4:
        if did not in OBVIOUS:
            err(f"{did}: difficulty {d['difficulty']} needs an obvious method in OBVIOUS")
        if "obvious method" not in d["how"] or "step to the target" not in d["how"]:
            err(f"{did}: how must name the obvious method and the step to the target")
        if PYODIDE and did in OBVIOUS:
            code = pl[OBVIOUS[did]]["code"]
            tm = pyodide_time(d["solution"], d["tests"])
            ts = pyodide_time(code, d["tests"])
            if tm["s"] is None or tm["s"] > 1.0 or not tm["ok"] or tm.get("recursion"):
                err(f"{did}: model in Pyodide {tm}")
            if ts["s"] is None or ts["s"] <= 5.0:
                err(f"{did}: obvious method in Pyodide {ts}")
            print(f"  {did}: Pyodide model {tm['s']} s, obvious {ts['s']} s{' (cut off)' if ts['s'] and ts['s'] >= 12 else ''}")
    diffs[d["difficulty"]] = diffs.get(d["difficulty"], 0) + 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-6": err(f"{did}: tags must start pack-6")
    if ("stdin" in d["tags"]) != d["fn"].startswith("solve_"): err(f"{did}: stdin tag and solve_ name disagree")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if d["pattern"] != "dp": err(f"{did}: pattern {d['pattern']}")
    if f"Submit runs {len(d['tests'])} hidden tests" not in d["how"]: err(f"{did}: how test count")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}")
if FULL and diffs != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {diffs}")
if FULL and stdin != 2: err(f"{stdin} stdin drills")
idx = {r["id"]: r for r in json.load(open(os.path.join(DRILLS, "index.json")))}
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    if did not in idx or idx[did]["difficulty"] != d["difficulty"] or idx[did]["name"] != d["name"]:
        err(f"{did}: index.json row out of step")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
