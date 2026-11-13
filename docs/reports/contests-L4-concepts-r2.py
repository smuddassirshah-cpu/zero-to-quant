#!/usr/bin/env python3
"""Concept audit, contests level 4, round 2 (blind). Executes the audit's checks.

Run:  python docs/reports/contests-L4-concepts-r2.py          (stdlib only, about a minute)
Exit: 0 when every check holds. A check that fails because the content is wrong stays failing
      and is printed as "FINDING n" (n is the finding number in docs/reviews/audit-contests-4-r2.md).

What it does
  1. Runs every code solution against its hidden tests, and every starter (which must fail).
  2. Sweeps every feedback.byKey.test-N line: the mistake the line names is written as a real submission
     and must fail first at test N. Semantics follow app/js/engine/widgets/code.js: prelude, then the
     learner's code, run once in one namespace; cases run in order in that namespace; a case that raises or
     passes 5 s fails on its own row; the key is test-(first failing row + 1); recursion limit 3,000.
  3. Recomputes every worked figure and checks each keyed choice is the unique best under the prompt.

Native CPython is faster than Pyodide (wasm32) by a small factor. So a mistake counted here as "times out"
must run past 5 s natively, and a solution must finish each case in under 1 s natively.
"""
import itertools
import json
import math
import os
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "contests")
LIMIT_S = 5.0          # code.js TEST_MS
RECURSION = 3000       # drill-worker.js RECURSION_LIMIT

results = []           # (ok, label, detail, finding)


def check(label, ok, detail="", finding=None):
    results.append((bool(ok), label, detail, finding))


def load(name):
    with open(os.path.join(COURSE, name), encoding="utf-8") as f:
        return json.load(f)


class _Timeout(BaseException):
    pass


def _alarm(signum, frame):
    raise _Timeout()


signal.signal(signal.SIGALRM, _alarm)


def _same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(_same(p, q) for p, q in zip(x, y)))
    return bool(x == y)


def _close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(_close(p, q) for p, q in zip(x, y)))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run(widget, code):
    """Returns (first failing test number or 0, list of per-case seconds, note for the failing case)."""
    sys.setrecursionlimit(RECURSION)
    g = {"__name__": "__main__"}
    try:
        if widget.get("prelude"):
            exec(compile(widget["prelude"], "<prelude>", "exec"), g)
        exec(compile(code, "solution.py", "exec"), g)
    except Exception as e:  # a load failure: the page's key is 'error'
        return -1, [], "load: " + type(e).__name__
    secs = []
    for i, case in enumerate(widget["tests"], 1):
        t0 = time.perf_counter()
        note = ""
        try:
            signal.setitimer(signal.ITIMER_REAL, LIMIT_S)
            if case.get("setup"):
                exec(case["setup"], g)
            actual = eval(case["call"], g)
            signal.setitimer(signal.ITIMER_REAL, 0)
            expected = eval(case["expect"], g)
            ok = _close(actual, expected) if case.get("compare") == "isclose" else _same(actual, expected)
            if not ok:
                note = "got " + repr(actual)[:60]
        except _Timeout:
            ok, note = False, "timeout"
        except RecursionError:
            ok, note = False, "RecursionError"
        except Exception as e:
            ok, note = False, "raised " + type(e).__name__
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        secs.append(time.perf_counter() - t0)
        if not ok:
            return i, secs, note
    return 0, secs, ""


def code_widgets(doc):
    items = doc.get("screens") or doc.get("items") or []
    for idx, it in enumerate(items):
        w = it.get("widget") or {}
        if w.get("kind") == "code":
            yield idx, it, w


FILES = ["l13-virtual-contest.json", "l14-which-first.json", "l15-debugging-under-time.json",
         "l16-upsolving.json", "review-4.json", "homework-4.json"]
DOC = {f: load(f) for f in FILES}
W = {}
for f in FILES:
    for idx, it, w in code_widgets(DOC[f]):
        fn = w["starter"].split("def ")[1].split("(")[0]
        W[fn] = (f, idx, it, w)

# ---------------------------------------------------------------- 1. solutions and starters
for fn, (f, idx, it, w) in W.items():
    first, secs, note = run(w, w["solution"])
    check(f"{f} [{idx}] {fn}: solution passes all {len(w['tests'])} tests", first == 0, note)
    check(f"{f} [{idx}] {fn}: slowest solution case under 1 s natively ({max(secs or [0]):.2f} s)", max(secs or [0]) < 1.0)
    first, secs, note = run(w, w["starter"])
    check(f"{f} [{idx}] {fn}: starter fails (first at test {first})", first != 0)
    # examples are among the tests and the 'how' line counts them
    n = len(w["tests"])
    how = w.get("how", "")
    check(f"{f} [{idx}] {fn}: how line states {n} hidden tests", f"{n} hidden tests" in how, how[:60])
    keys = [k for k in (it.get("feedback", {}).get("byKey") or {})]
    check(f"{f} [{idx}] {fn}: every byKey key is test-1..test-{n}",
          all(k.startswith("test-") and 1 <= int(k[5:]) <= n for k in keys), str(keys))

# ---------------------------------------------------------------- 2. byKey sweep: the named mistake fails first at N
SWEEP = []


def mistake(fn, n, what, code, finding=None, timeout=False):
    SWEEP.append((fn, n, what, code, finding, timeout))


# --- l13 A peaks
mistake("peaks", 2, "reads closes[1] before the loop (no guard for one close)", '''
def peaks(closes):
    count = 0
    first, second = closes[0], closes[1]
    for i in range(1, len(closes) - 1):
        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:
            count += 1
    return count
''')
mistake("peaks", 3, "counts the last day when it is above its one neighbour", '''
def peaks(closes):
    count = 0
    for i in range(1, len(closes) - 1):
        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:
            count += 1
    if len(closes) >= 2 and closes[-1] > closes[-2]:
        count += 1
    return count
''')
mistake("peaks", 4, "counts the first day when it is above its one neighbour", '''
def peaks(closes):
    count = 0
    for i in range(1, len(closes) - 1):
        if closes[i] > closes[i - 1] and closes[i] > closes[i + 1]:
            count += 1
    if len(closes) >= 2 and closes[0] > closes[1]:
        count += 1
    return count
''')
mistake("peaks", 5, ">= on both sides", '''
def peaks(closes):
    return sum(1 for i in range(1, len(closes) - 1) if closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1])
''')
mistake("peaks", 6, ">= on one side only (a plateau's right end counts)", '''
def peaks(closes):
    return sum(1 for i in range(1, len(closes) - 1) if closes[i] >= closes[i - 1] and closes[i] > closes[i + 1])
''')

# --- l13 B shortest_cover
_COVER = '''
def shortest_cover(tickers, needed):
    need = set(needed)
    count, have, best, left = {}, 0, %s, 0
    for right, t in enumerate(tickers):
        if t in need:
            count[t] = count.get(t, 0) + 1
            if count[t] == 1:
                have += 1
        while have == %s:
            if right - left + 1 < best:
                best = right - left + 1
            u = tickers[left]
            if u in need:
                count[u] -= 1
                if count[u] == 0:
                    have -= 1
            left += 1
    return %s
'''
mistake("shortest_cover", 3, "returns the starting 'infinity' when no window covers",
        _COVER % ("len(tickers) + 1", "len(need)", "best"))
mistake("shortest_cover", 5, "compares with len(needed), so a name listed twice is never covered",
        _COVER % ("len(tickers) + 1", "len(needed)", "best if best <= len(tickers) else -1"))
mistake("shortest_cover", 8, "restarts a scan at every left end, reading the tape by index", '''
def shortest_cover(tickers, needed):
    need = set(needed)
    n, best = len(tickers), -1
    for left in range(n):
        got = set()
        for right in range(left, n):
            t = tickers[right]
            if t in need:
                got.add(t)
                if len(got) == len(need):
                    if best == -1 or right - left + 1 < best:
                        best = right - left + 1
                    break
    return best
''')
mistake("shortest_cover", 9, "the same restart on a plain copy of the tape (reads are not counted)", '''
def shortest_cover(tickers, needed):
    tickers = list(tickers)
    need = set(needed)
    n, best = len(tickers), -1
    for left in range(n):
        got = set()
        for right in range(left, n):
            t = tickers[right]
            if t in need:
                got.add(t)
                if len(got) == len(need):
                    if best == -1 or right - left + 1 < best:
                        best = right - left + 1
                    break
    return best
''', timeout=True)

# --- l13 C shipping
_SHIP_OK = '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if w > cap:
            return False
        if load + w > cap:
            days += 1
            load = 0
        load += w
    return days <= k
'''
# fix pass: the drop-the-overflow can_ship, called by min_capacity as the prose requires, lands on the new test-1 line;
# the test-2 line now names can_ship called alone, reached when min_capacity carries its own check
_DROP = '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if w > cap:
            return False
        if load + w > cap:
            days += 1
            load = 0
        else:
            load += w
    return days <= k
'''
mistake("can_ship", 2, "fix pass: a can_ship that says 11 ships in 3 days, with min_capacity running its own check", _DROP + '''

def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    def ok(cap):
        days, load = 1, 0
        for x in weights:
            if load + x > cap:
                days += 1
                load = 0
            load += x
        return days <= k
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
''')
mistake("can_ship", 1, "the greedy drops the order that overflows; min_capacity calls can_ship as the prose requires", '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if w > cap:
            return False
        if load + w > cap:
            days += 1
            load = 0
        else:
            load += w
    return days <= k


def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
''')
mistake("can_ship", 4, "an order heavier than the van starts a day and is carried anyway", '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if load + w > cap and load > 0:
            days += 1
            load = 0
        load += w
    return days <= k


def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
''')
mistake("can_ship", 10, "binary search over 1 .. 10**9, not heaviest .. total", _SHIP_OK + '''

def min_capacity(weights, k):
    lo, hi = 1, 10**9
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
''')
mistake("can_ship", 10, "a scan upwards from the heaviest order, calling can_ship", _SHIP_OK + '''

def min_capacity(weights, k):
    cap = max(weights)
    while not can_ship(weights, k, cap):
        cap += 1
    return cap
''')
mistake("can_ship", 11, "a scan upwards with its own inlined check (no can_ship calls are counted)", _SHIP_OK + '''

def min_capacity(weights, k):
    cap = max(weights)
    while True:
        days, load = 1, 0
        for w in weights:
            if load + w > cap:
                days += 1
                load = 0
            load += w
        if days <= k:
            return cap
        cap += 1
''', timeout=True)

# --- l13 D grid_moves
_GRID = '''
from collections import deque

STEP = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def grid_moves(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    dist[0][0] = 0
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        %s
        cell = grid[r][c]
        moves = %s
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                %s
                queue.append((nr, nc))
    return %s
'''
_POP = "if (r, c) == (rows - 1, cols - 1):\n            return dist[r][c]"
_ARROWS = '[STEP[cell]] if cell in STEP else STEP.values()'
mistake("grid_moves", 1, "ignores the arrows", _GRID % (_POP, "STEP.values()", "pass", "-1"))
mistake("grid_moves", 2, "returns None, not -1, when the target is unreachable", _GRID % (_POP, _ARROWS, "pass", "None"))
mistake("grid_moves", 3, "tests for the target only when a neighbour is pushed",
        _GRID % ("pass", _ARROWS, "if (nr, nc) == (rows - 1, cols - 1):\n                    return dist[nr][nc]", "-1"))
mistake("grid_moves", 9, "a depth-first search that revisits a cell whenever it finds a shorter distance", '''
STEP = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def grid_moves(grid):
    rows, cols = len(grid), len(grid[0])
    best = [[10**9] * cols for _ in range(rows)]
    best[0][0] = 0
    stack = [(0, 0)]
    while stack:
        r, c = stack.pop()
        cell = grid[r][c]
        moves = [STEP[cell]] if cell in STEP else STEP.values()
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and best[r][c] + 1 < best[nr][nc]:
                best[nr][nc] = best[r][c] + 1
                stack.append((nr, nc))
    d = best[rows - 1][cols - 1]
    return -1 if d == 10**9 else d
''', timeout=True)

# --- l14 decayed_score
mistake("decayed_score", 2, "applies the floor before the attempt cost", '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    return max(floor * value, value - per_minute * minute) - per_wrong * wrong
''')
mistake("decayed_score", 2, "no floor at all", '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    return value - per_minute * minute - per_wrong * wrong
''')
mistake("decayed_score", 7, "treats a floor of 0 as no floor", '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    raw = value - per_minute * minute - per_wrong * wrong
    return max(floor * value, raw) if floor else raw
''')

# --- l14 icpc_rank_key
mistake("icpc_rank_key", 1, "charges rejections on unsolved problems", '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        penalty += per_wrong * wrong
        if minute is not None:
            solved += 1
            penalty += minute
    return (-solved, penalty)
''')
mistake("icpc_rank_key", 5, "a bare `if minute:`", '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        if minute:
            solved += 1
            penalty += minute + per_wrong * wrong
    return (-solved, penalty)
''')

# --- l14 best_order
_BEST = '''
from itertools import permutations


def best_order(problems, minutes):
    best_total, best_names = %s, None
    for order in permutations(%s):
        clock, total = 0, 0
        for name, value, time in order:
            clock += time
            if %s:
                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)
        if total > best_total:
            best_total, best_names = total, [p[0] for p in order]
    return best_total, best_names
'''
mistake("best_order", 2, "a problem finishing after the round still scores", _BEST % ("-1", "sorted(problems)", "True"))
mistake("best_order", 3, "does not sort by name first", _BEST % ("-1", "problems", "clock <= minutes"))
mistake("best_order", 4, "starts the best total at 0, so an all-zero round keeps no order", _BEST % ("0", "sorted(problems)", "clock <= minutes"))

# --- l15 last_occurrence
mistake("last_occurrence", 4, "the starter (starts at n - 2)", None)
mistake("last_occurrence", 3, "a special case that reads xs[-1] of an empty list", '''
def last_occurrence(xs, x):
    if xs[-1] == x:
        return len(xs) - 1
    for i in range(len(xs) - 2, -1, -1):
        if xs[i] == x:
            return i
    return -1
''')

# --- l15 count_inversions_small
mistake("count_inversions_small", 3, "the starter (>=)", None)
mistake("count_inversions_small", 6, "fix pass: the line's named mistake, repeated values removed (each copy's pairs lost)", '''
def count_inversions_small(xs):
    xs = list(dict.fromkeys(xs))
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] > xs[j])
''')

# --- l15 solve_all
mistake("solve_all", 2, "the starter (a global set, never emptied)", None)
mistake("solve_all", 3, "a set kept outside solve_all, emptied between cases but not at the start of a call", '''
seen = set()


def solve_all(text):
    data = text.split()
    t = int(data[0])
    pos = 1
    out = []
    for case in range(t):
        n = int(data[pos])
        pos += 1
        if case > 0:
            seen.clear()
        for s in data[pos:pos + n]:
            seen.add(s)
        pos += n
        out.append(len(seen))
    return out
''')

# --- l15 smallest_failing
_SMALL = '''
def smallest_failing(fast, brute, gen, seed):
    for n in range(1, %s):
        case = stress(fast, brute, lambda rng: %s(rng, n), 200, seed)
        if case is not None:
            return case
    return None
'''
mistake("smallest_failing", 3, "stops at length 2", _SMALL % ("3", "gen"))
mistake("smallest_failing", 6, "always uses gen_list, ignoring the generator passed in", _SMALL % ("9", "gen_list"))
mistake("smallest_failing", 7, "stops at length 4", _SMALL % ("5", "gen"))

# --- l16 equal_thirds
_THIRDS = '''
def equal_thirds(xs):
    total = sum(xs)
    %s
    third = total // 3
    ways, firsts, prefix = 0, 0, 0
    for j in range(len(xs) - 1):
        prefix += xs[j]
        %s
    return ways
'''
_DIV = "if total % 3 != 0:\n        return 0"
_RIGHT = "if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n            firsts += 1"
mistake("equal_thirds", 2, "counts the first cut before checking the second",
        _THIRDS % (_DIV, "if prefix == third:\n            firsts += 1\n        if prefix == 2 * third:\n            ways += firsts"))
mistake("equal_thirds", 5, "no divisibility test", _THIRDS % ("pass", _RIGHT))
mistake("equal_thirds", 6, "fix pass: the line's named mistake, stops once the prefix passes 2S/3",
        _THIRDS % (_DIV, _RIGHT.replace("if prefix == 2 * third:",
                                        "if prefix > 2 * third:\n            break\n        if prefix == 2 * third:")))
mistake("equal_thirds", 8, "the double loop over cuts", '''
def equal_thirds(xs):
    n = len(xs)
    P = [0] * (n + 1)
    for i, x in enumerate(xs):
        P[i + 1] = P[i] + x
    ways = 0
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if P[i] == P[j] - P[i] == P[n] - P[j]:
                ways += 1
    return ways
''', timeout=True)

# --- l16 mistakes_summary
_SUM = '''
def mistakes_summary(log):
    counts = {}
    for problem, category in log:
        counts[category] = counts.get(category, 0) + 1
    %s
'''
mistake("mistakes_summary", 1, "sorts by count only (ties stay in order of first appearance)",
        _SUM % "return sorted(counts.items(), key=lambda kv: -kv[1])")
mistake("mistakes_summary", 2, "takes max() of an empty log",
        _SUM % "top = max(counts.values())\n    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))")
mistake("mistakes_summary", 6, "sorts names case-insensitively",
        _SUM % "return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))")
mistake("mistakes_summary", 7, "sorts by name only", _SUM % "return sorted(counts.items())")

# --- homework desks_after_cut
_DESKS = '''
from collections import deque


def desks_after_cut(n, links, cut):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(links):
        if %s:
            adj[a].append(b)
            adj[b].append(a)
    seen = [False] * n
    groups = 0
    for s in range(n):
        if seen[s]%s:
            continue
        groups += 1
        seen[s] = True
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    queue.append(v)
    return groups
'''
mistake("desks_after_cut", 2, "counts only desks that still have a link", _DESKS % ("i != cut", " or not adj[s]"))
mistake("desks_after_cut", 4, "removes the link by value, so both copies go", _DESKS % ("(a, b) != links[cut]", ""))
mistake("desks_after_cut", 7, "a recursive DFS", '''
def desks_after_cut(n, links, cut):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(links):
        if i != cut:
            adj[a].append(b)
            adj[b].append(a)
    seen = [False] * n

    def dfs(u):
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                dfs(v)

    groups = 0
    for s in range(n):
        if not seen[s]:
            groups += 1
            dfs(s)
    return groups
''')

# --- homework max_profit_k
mistake("max_profit_k", 3, "tables of size k, read at index k - 1 (fails for k = 0)", '''
def max_profit_k(prices, k):
    buy = [float("-inf")] * k
    sell = [0] * k
    for p in prices:
        for j in range(k):
            buy[j] = max(buy[j], (sell[j - 1] if j else 0) - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k - 1]
''')
mistake("max_profit_k", 4, "forces exactly k trades on distinct days", '''
def max_profit_k(prices, k):
    NEG = float("-inf")
    buy = [NEG] * (k + 1)
    sell = [0] + [NEG] * k
    for p in prices:
        for j in range(k, 0, -1):
            sell[j] = max(sell[j], buy[j] + p)
            buy[j] = max(buy[j], sell[j - 1] - p)
    return max(sell) if k and len(prices) < 2 * k else sell[k]
'''.replace("return max(sell) if k and len(prices) < 2 * k else sell[k]", "return sell[k]"))
mistake("max_profit_k", 8, "tries every pair of days for each trade, O(n^2 k)", '''
def max_profit_k(prices, k):
    n = len(prices)
    prev = [0] * n
    for _ in range(k):
        cur = [0] * n
        for j in range(1, n):
            best = cur[j - 1]
            for i in range(j):
                gain = prices[j] - prices[i] + prev[i]
                if gain > best:
                    best = gain
            cur[j] = best
        prev = cur
    return prev[-1] if n else 0
''', timeout=True)

# --- homework widest_gap
_GAP = '''
def widest_gap(levels, m):
    xs = %s

    def fits(gap):
        placed, last = 1, xs[0]
        for x in xs[1:]:
            if x - last >= gap:
                placed += 1
                last = x
        return placed >= m

    %s
'''
_BS = "lo, hi = %s, xs[-1] - xs[0]\n    while lo < hi:\n        mid = (lo + hi + 1) // 2\n        if fits(mid):\n            lo = mid\n        else:\n            hi = mid - 1\n    return lo"
mistake("widest_gap", 1, "does not sort the levels", _GAP % ("list(levels)", _BS % "0"))
mistake("widest_gap", 4, "starts the search at 1, so equal levels give 1", _GAP % ("sorted(levels)", _BS % "1"))
mistake("widest_gap", 8, "tries every distance upwards",
        _GAP % ("sorted(levels)", "gap = 0\n    while fits(gap + 1):\n        gap += 1\n    return gap"), timeout=True)

swept = set()
for fn, n, what, code, finding, timeout in SWEEP:
    f, idx, it, w = W[fn]
    first, secs, note = run(w, code if code is not None else w["starter"])
    swept.add((fn, n))
    check(f"{f} [{idx}] {fn} byKey test-{n}: '{what}' fails first at test {n} (got test {first}, {note})",
          first == n, finding=finding)
    if timeout and first == n:
        check(f"{f} [{idx}] {fn} byKey test-{n}: that failure is a timeout past {LIMIT_S:.0f} s", note == "timeout", note)

# every byKey test line in scope was swept (max_profit_k test-6 names no mistake: its figure is checked below)
for fn, (f, idx, it, w) in W.items():
    for k in (it.get("feedback", {}).get("byKey") or {}):
        n = int(k[5:])
        if (fn, n) == ("max_profit_k", 6):
            continue
        check(f"{f} [{idx}] {fn}: byKey {k} was swept", (fn, n) in swept)

# reachable alternatives for the two lines whose named mistake lands on another test (recorded, not findings)
f, idx, it, w = W["count_inversions_small"]
first, _, note = run(w, "def count_inversions_small(xs):\n    xs = list(dict.fromkeys(xs))\n    n = len(xs)\n"
                        "    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] > xs[j])\n")
check("l15 fix 2: removing repeated values is a mistake that does fail first at test 6", first == 6, note)
f, idx, it, w = W["equal_thirds"]
first, _, note = run(w, _THIRDS % (_DIV, _RIGHT.replace("if prefix == 2 * third:",
                                                        "if prefix > 2 * third:\n            break\n        if prefix == 2 * third:")))
check("l16 D: stopping once the prefix passes 2S/3 is a mistake that does fail first at test 6", first == 6, note)
f, idx, it, w = W["can_ship"]
first, _, note = run(w, "def can_ship(weights, k, cap):\n    ...\n\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n"
                        "    def ok(cap):\n        days, load = 1, 0\n        for x in weights:\n            if load + x > cap:\n                days += 1\n                load = 0\n            load += x\n        return days <= k\n"
                        "    while lo < hi:\n        mid = (lo + hi) // 2\n        if ok(mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n")
check("l13 C: test 2 is the first failure only when min_capacity does not call can_ship (can_ship left unwritten)", first == 2, note)
# and a missing 'w > cap' line alone does not fail test 4 with the standard greedy (the day count already exceeds k)
first, _, note = run(w, _SHIP_OK.replace("        if w > cap:\n            return False\n", "") + "\n\ndef min_capacity(weights, k):\n    lo, hi = max(weights), sum(weights)\n"
                     "    while lo < hi:\n        mid = (lo + hi) // 2\n        if can_ship(weights, k, mid):\n            hi = mid\n        else:\n            lo = mid + 1\n    return lo\n")
# finding 4 was not applied by the fix pass (it needs a new hidden test, outside a content fix): the gap is recorded as it stands
check("l13 C (finding 4, not applied): a can_ship with no 'w > cap' test still passes all 11 hidden tests", first == 0,
      "if this fails, a hidden test now needs the guard: restore the finding-4 check", None)
# the audit's proposed test 12 separates them
_g = {}
exec(_SHIP_OK.replace("        if w > cap:\n            return False\n", ""), _g)
_h = {}
exec(w["solution"], _h)
check("l13 C fix: proposed test can_ship([5, 5], 3, 4) is False for the solution and True without the guard",
      _h["can_ship"]([5, 5], 3, 4) is False and _g["can_ship"]([5, 5], 3, 4) is True)

# ---------------------------------------------------------------- 3. worked figures
# l13
g = {}
exec(W["can_ship"][3]["prelude"], g)
w40 = g["_weights"](40, 32, 100)
check("l13 C: test 10 has 40 orders, total 1,807, heaviest 99", (len(w40), sum(w40), max(w40)) == (40, 1807, 99), str((sum(w40), max(w40))))
exec(W["can_ship"][3]["solution"], g)
ans, calls = g["checks_used"](w40, 2)
check("l13 C: test 10 answer 909 with 11 checks", (ans, calls) == (909, 11), str((ans, calls)))
check("l13 C: a scan upwards from 99 makes 811 checks", ans - max(w40) + 1 == 811)
check("l13 C: about log2(total - max) checks", math.ceil(math.log2(sum(w40) - max(w40))) == 11)
check("l13 C: 2^30 > 10^9 and about 1.07e9", 2**30 > 10**9 and abs(2**30 / 1e9 - 1.07) < 0.005)
w5 = g["_weights"](100000, 31)
check("l13 C: test 11 total is under 10^9, so at most 30 checks", math.ceil(math.log2(sum(w5) - max(w5))) <= 30)
check("l13 C: test 11's answer is about a million, the scan the test-11 line names", 0.9e6 < 1002823 - max(w5) < 1.1e6)
check("l13 B: restart at every left end on 200,000 trades is about 2e10 steps", abs(200000 * 200001 / 2 / 2e10 - 1) < 0.01)
check("l13 A: q-plateau 2 2 3 3 2 has 0 peaks", eval("peaks([2,2,3,3,2])", {**g, **{"peaks": None}} if False else (lambda d: (exec(W["peaks"][3]["solution"], d), d)[1])({})) == 0)
check("l13 Sam: D took 52 minutes, A seven, second wrong answer 13 later", (52 - 0, 59 - 52, 51 - 38) == (52, 7, 13))
rows = [(2, 6, 1), (4, 9, 4), (5, 10, 12), (5, 2, 0)]
check("l13 log: totals 16, 27, 17 and 60", [sum(c) for c in zip(*rows)] == [16, 27, 17] and sum(map(sum, rows)) == 60)
check("l13 homework model: A 9, B 17, C 27 minutes, 7 left for D", [sum(r) for r in rows] == [9, 17, 27, 7])
check("l13 transfer: four minutes is about a sixth of 25", abs(4 / (75 / 3) - 1 / 6) < 0.01)

# l14: the round
P4 = [("A", 500, 10), ("B", 1000, 20), ("C", 1500, 35), ("D", 2000, 50)]


def total(order, minutes=120, floor=0.3):
    clock, tot, each = 0, 0, {}
    for name, v, t in order:
        clock += t
        s = max(floor * v, v - v / 250 * clock) if clock <= minutes else 0
        each[name] = s
        tot += s
    return tot, each


byname = {p[0]: p for p in P4}
tot = {"".join(o): total([byname[c] for c in o])[0] for o in itertools.permutations("ABCD")}
best = max(tot.values())
check("l14: A B C D scores 3,550 (480, 880, 1110, 1080)", total(P4) == (3550, {"A": 480, "B": 880, "C": 1110, "D": 1080}))
check("l14: D C B A scores 3,440 and C A B D 3,520", (tot["DCBA"], tot["CABD"]) == (3440, 3520))
check("l14: the keyed order is the unique best up to the A/B tie", sorted(k for k, v in tot.items() if v == best) == ["ABCD", "BACD"] and best == 3550)
check("l14: hardest first drops A, B, C by 630 together and lifts D by 520", (480 - 270) + (880 - 580) + (1110 - 990) == 630 and 1600 - 1080 == 520)
check("l14: rates 50, 50, 42.857, 40", [round(v / t, 3) for _, v, t in P4] == [50, 50, 42.857, 40])
check("l14: A B D C scores 3,530, 20 fewer", tot["ABDC"] == 3530 and (2000 * 35 - 1500 * 50) / 250 == -20)
check("l14: B at minute 35 with one rejection scores 810", 1000 - 4 * 35 - 50 == 810)
# exchange argument: for every adjacent swap with no floor and no deadline the difference is (v_j t_i - v_i t_j)/250
ok = True
for o in itertools.permutations(P4):
    for k in range(3):
        s = list(o)
        s[k], s[k + 1] = s[k + 1], s[k]
        i, j = o[k], o[k + 1]
        lost_more = total(s, 10**9, 0)[0] - total(o, 10**9, 0)[0]      # points i-first loses beyond j-first
        ok &= abs(lost_more - (j[1] * i[2] - i[1] * j[2]) / 250) < 1e-9
check("l14: the swap formula holds for every adjacent pair of every order (no floor, no deadline)", ok)
# FINDING 5: "The floor of 30% matters only for a problem solved very late": in a two-hour round time alone never reaches it
check("l14: under v/250 a minute the floor is reached by time alone only at minute 175, after a two-hour round ends", 0.7 * 250 == 175 and 175 > 120)
check("l14 fix: in a two-hour round time alone leaves 52% of the value", 1 - 120 / 250 == 0.52)
binds_by_lateness_alone = any(v - v / 250 * m < 0.3 * v for v in (500, 1000, 1500, 2000) for m in range(0, 121))
binds_mid_round_with_rejections = 500 - 2 * 60 - 50 * 5 < 0.3 * 500      # A at minute 60 after five rejections: 130 < 150
# fix pass: the explain now says time alone takes at most 48% in a two-hour round, so only rejections reach the floor
_t3 = DOC["l14-which-first.json"]["screens"][3]["explain"]["text"]
check("l14 [3] explain (fix pass): states the 48% bound and ties the floor to rejections, and the model agrees",
      "very late" not in _t3 and "at most 48%" in _t3 and "only when rejections" in _t3 and 120 / 250 == 0.48
      and not binds_by_lateness_alone and binds_mid_round_with_rejections,
      _t3, finding=5)
check("l14 q-floor: 1000 - 720 - 50 = 230, floored to 300", max(300, 1000 - 4 * 180 - 50) == 300)
check("l14 icpc: penalty 208; X 195, Y 185", 12 + 41 + 20 + 95 + 40 == 208 and 15 + 50 + 90 + 40 == 195 and 20 + 45 + 100 + 20 == 185)
t60 = {"".join(o): total([byname[c] for c in o], 60)[0] for o in itertools.permutations("ABCD")}
check("l14: with 60 minutes the best is 2,090 (B then C) and A then B gives 1,360", max(t60.values()) == 2090 and t60["ABCD"] == 1360 and min(k for k, v in t60.items() if v == 2090) == "BCAD")
check("l14: no three problems fit in 60 minutes", min(sum(c) for c in itertools.combinations([10, 20, 35, 50], 3)) > 60)


# l14: how long on D
def E(x):
    return 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))


xs = [i / 1000 for i in range(0, 60001)]
xbest = max(xs, key=E)
check("l14 D/E: best fixed split 34.84 minutes, about 1,152 points", abs(xbest - 34.84) < 0.01 and round(E(xbest)) == 1152, f"{xbest} {E(xbest):.1f}")
check("l14 D/E: all D 699, all E 785, start point E(10) = 952.73", round(E(60)) == 699 and round(E(0)) == 785 and abs(E(10) - 952.7300522442163) < 1e-9)


def integrate(fn, a, b, n=20000):
    h = (b - a) / n
    return h * (fn(a) / 2 + sum(fn(a + k * h) for k in range(1, n)) + fn(b) / 2)


def leave_when_solved(c):
    """D first with cap c, leaving D the moment it is solved; D's time ~ Exp(mean 50), E's ~ Exp(mean 15)."""
    e_rest = lambda t: 800 * (1 - math.exp(-(60 - t) / 15))
    return (integrate(lambda t: math.exp(-t / 50) / 50 * (1000 + e_rest(t)), 0, c) + math.exp(-c / 50) * e_rest(c))


cs = [k / 10 for k in range(0, 601)]
cbest = max(cs, key=leave_when_solved)
check("l14 D/E: leaving D when solved, the best cap is near 45 minutes", abs(cbest - 45) <= 1.5, f"cap {cbest}, value {leave_when_solved(cbest):.0f}")
# E first, leaving E when solved, D with the rest: the lesson's own points-per-minute rule (800/15 > 1000/50)
e_first = integrate(lambda t: math.exp(-t / 15) / 15 * (800 + 1000 * (1 - math.exp(-(60 - t) / 50))), 0, 60)
# fix pass: the explain now says E first once a solved problem may be left, about 1,363, above D first with its best cap
_t6 = DOC["l14-which-first.json"]["screens"][6]["explain"]["text"]
_e_first_capped = max(integrate(lambda t: math.exp(-t / 15) / 15 * (800 + 1000 * (1 - math.exp(-(60 - t) / 50))), 0, c)
                      + math.exp(-c / 15) * 1000 * (1 - math.exp(-(60 - c) / 50)) for c in (10, 20, 30, 40, 50, 60))
check("l14 D/E [6] explain (fix pass): says start with E for about 1,363, which beats D first with its best cap",
      "near 45" not in _t6 and "start with E" in _t6 and "1,363" in _t6 and round(e_first) == 1363
      and e_first > leave_when_solved(cbest) and abs(_e_first_capped - e_first) < 1e-6,
      f"{_t6} | D first with the best cap {leave_when_solved(cbest):.0f}; E first {e_first:.0f}", finding=6)
# Monte Carlo of the same three policies (200,000 rounds, fixed seed)
import random as _r
_rng = _r.Random(20261113)
_n = 200000
_sum_fixed = _sum_cap = _sum_efirst = 0.0
for _ in range(_n):
    td, te = _rng.expovariate(1 / 50), _rng.expovariate(1 / 15)
    _sum_fixed += 1000 * (td <= xbest) + 800 * (te <= 60 - xbest)
    _sum_cap += (1000 + 800 * (te <= 60 - td)) if td <= cbest else 800 * (te <= 60 - cbest)
    _sum_efirst += (800 + 1000 * (td <= 60 - te)) if te <= 60 else 0
check("l14 D/E: Monte Carlo agrees: fixed split 1,152, D first with cap 1,229, E first 1,363 (each within 8)",
      abs(_sum_fixed / _n - 1152) < 8 and abs(_sum_cap / _n - leave_when_solved(cbest)) < 8 and abs(_sum_efirst / _n - e_first) < 8,
      f"{_sum_fixed / _n:.0f} {_sum_cap / _n:.0f} {_sum_efirst / _n:.0f}")
check("l14 D/E fix: E first, leaving E when solved, expects about 1,363", round(e_first) == 1363, f"{e_first:.1f}")
check("l14 D/E: points per expected minute are 53 for E and 20 for D", round(800 / 15) == 53 and 1000 / 50 == 20)

# l14 transfer
check("l14 desk: rates 600, 480, 100 a minute", (3000 / 5, 12000 / 25, 2000 / 20) == (600, 480, 100))
check("l14 desk: at 1% a minute quote first costs the hedge 600, hedge first costs the quote 750", (12000 * 0.01 * 5, 3000 * 0.01 * 25) == (600, 750))
# fix pass: feedback.correct and hints[2] now name only the two tasks that fit (5 + 25 = 30; 5 + 25 + 20 = 50)
_s11 = DOC["l14-which-first.json"]["screens"][11]
_texts11 = [_s11["feedback"]["correct"], _s11["hints"][2]["text"]]
check("l14 desk [11] (fix pass): feedback and last hint name quote then hedge only, and only those two fit in 30 minutes",
      all("then the hedge" in t and "quote, hedge, reconcile" not in t and "then reconcile" not in t for t in _texts11)
      and 5 + 25 <= 30 < 5 + 25 + 20, str(_texts11), finding=7)
check("l14 scoreboard: 702 / 96 is about seven", round(702 / 96) == 7)

# l15
def buggy_last(xs, x):
    for i in range(len(xs) - 2, -1, -1):
        if xs[i] == x:
            return i
    return -1


check("l15: the four hand cases give -1, 1, 1, -1 on the submission, two wrong",
      [buggy_last([5], 5), buggy_last([3, 3, 3], 3), buggy_last([10**9, 10**9, 1], 10**9), buggy_last([4, 7], 9)] == [-1, 1, 1, -1])
check("l15: the example 4 7 7 1 hides the bug", buggy_last([4, 7, 7, 1], 7) == 2)
check("l15: 1,500 values make about 1.1 million pairs", 1500 * 1499 // 2 == 1124250)
p_tie = sum(200 * math.comb(n, 2) / 10**6 for n in range(1, 9))
check("l15: with values to 10^6 the tie bug shows in under 2% of runs of the whole loop", p_tie < 0.02, f"{p_tie:.4f}")
check("l15 q-overflow: 2e5 * 1e9 = 2e14 > 2^31 - 1; long long to about 9.2e18", 2 * 10**5 * 10**9 == 2 * 10**14 > 2**31 - 1 and abs((2**63 - 1) / 9.2e18 - 1) < 0.01)
check("l15 q-adjacent: [3, 2, 1] gives 2 against 3", sum(1 for a, b in zip([3, 2, 1], [2, 1]) if a > b) == 2)

# l16
check("l16: C(199999, 2) = 19,999,700,001; C(4,2) = 6; C(3,2) = 3; C(5,2) = 10", (math.comb(199999, 2), math.comb(4, 2), math.comb(3, 2), math.comb(5, 2)) == (19999700001, 6, 3, 10))
check("l16: that count is about nine times 2^31 - 1 and exact in a double", 9 < 19999700001 / (2**31 - 1) < 9.5 and float(19999700001) == 19999700001 < 2**53)
log = ["misread a constraint", "forgot n = 1", "greedy without proof", "forgot n = 1", "overflow", "misread a constraint", "greedy without proof", "forgot n = 1"]
check("l16: log counts 3, 2, 2, 1", [log.count(c) for c in ("forgot n = 1", "misread a constraint", "greedy without proof", "overflow")] == [3, 2, 2, 1])
check("l16: test 6's one way and test 5's total of 2", sum([2, -2] * 4 + [2]) == 2)
# FINDING 8: the summary formula as printed puts no upper limit on j; read over cuts i >= 1 and every j up to n, a zero total overcounts
def formula_as_printed(xs):
    P = [0]
    for x in xs:
        P.append(P[-1] + x)
    S = P[-1]
    if S % 3:
        return 0
    return sum(sum(1 for i in range(1, j) if P[i] == S // 3) for j in range(1, len(P)) if P[j] == 2 * S // 3)


def formula_fixed(xs):          # the audit's fix: j <= n - 1 and 1 <= i < j
    P = [0]
    for x in xs:
        P.append(P[-1] + x)
    S = P[-1]
    if S % 3:
        return 0
    return sum(sum(1 for i in range(1, j) if P[i] == S // 3) for j in range(1, len(P) - 1) if P[j] == 2 * S // 3)


sol = {}
exec(W["equal_thirds"][3]["solution"], sol)
# fix pass: the summary formula now ranges j <= n - 1 and 1 <= i < j (formula_fixed); the unranged reading overcounts
_tex = DOC["l16-upsolving.json"]["summary"]["formula"]["tex"]
check("l16 summary formula (fix pass): printed with j <= n-1 and 1 <= i < j, which gives 6 on five zeros (unranged: 10)",
      "j \\le n-1" in _tex and "1 \\le i < j" in _tex and formula_fixed([0] * 5) == sol["equal_thirds"]([0] * 5) == 6
      and formula_as_printed([0] * 5) == 10, _tex, finding=8)
import random as _r2
_rng2 = _r2.Random(7)
check("l16 summary formula fix: with j <= n - 1 and 1 <= i < j it equals the count on 2,000 random lists",
      all(formula_fixed(x) == sol["equal_thirds"](x) for x in ([_rng2.randint(-1, 1) for _ in range(_rng2.randint(1, 9))] for _ in range(2000))))
check("l16 ratings: 1200 + 300, 1900 - 1200, 2400 - 1200, 2000 - 1250, 1800 - 1410, 2100 - 1500", (1500, 700, 1200, 750, 390, 600) == (1200 + 300, 1900 - 1200, 2400 - 1200, 2000 - 1250, 1800 - 1410, 2100 - 1500))

# review-4 and homework-4
check("r4-pattern: a scan upwards is up to about 2e14 limits", 2 * 10**5 * 10**9 == 2 * 10**14)
check("r4-log: 18/60 = 0.3, 30/60 = 0.5, 18/30 = 0.6, and the log totals 60", (18 / 60, 30 / 60, 18 / 30, 12 + 30 + 18) == (0.3, 0.5, 0.6, 60))
check("r4-decay: 1,112; slips 1,212 and 1,162; floor 450", (1500 - 6 * 48 - 100, 1500 - 6 * 48, 1500 - 6 * 48 - 50, 0.3 * 1500) == (1112, 1212, 1162, 450))
check("r4-swap: Q first scores 20 more; waits cost 60 and 80", ((1000 * 15 - 500 * 40) / 250, 15 * 4, 40 * 2, round(500 / 15)) == (-20, 60, 80, 33))
check("r4-hand: [5] gives 0, [2, 2, 2] gives 4, [] gives 0", [sum(x[1:]) for x in ([5], [2, 2, 2], [])] == [0, 4, 0])
check("r4-upsolve: 1650, 550 and 950", (1350 + 300, 1900 - 1350, 2300 - 1350) == (1650, 550, 950))
check("r4-late: 675 at minute 115; slip 1,150; floor 375", (1250 - 5 * 115, 1250 - 5 * 20, 0.3 * 1250, 1250 / 250) == (675, 1150, 375, 5))
check("hw4-penalty: 269; slips 349 and 209", (8 + 27 + 64 + 110 + 60, 269 + 80, 8 + 27 + 64 + 110) == (269, 349, 209))
check("hw4-ktrades: test 6 is 2 + 3 + 4 = 9; O(n^2 k) is 2e9; O(nk) is 2e5", (2 + 3 + 4, 10**4 * 10**4 * 20, 10**4 * 20) == (9, 2 * 10**9, 2 * 10**5))
check("hw4-desks: a chain of 200,000 cut at link 100,000 leaves a piece 100,001 desks long", 200000 // 2 + 1 == 100001 > RECURSION)

# ---------------------------------------------------------------- report
fails = [r for r in results if not r[0]]
for ok, label, detail, finding in results:
    if not ok:
        tag = f"FINDING {finding}" if finding else "FAIL"
        print(f"{tag}: {label}" + (f"  [{detail}]" if detail else ""))
unexpected = [r for r in fails if r[3] is None]
print(f"{len(results)} checks, {len(results) - len(fails)} hold, {len(fails) - len(unexpected)} findings, {len(unexpected)} unexpected failures")
sys.exit(1 if fails else 0)
