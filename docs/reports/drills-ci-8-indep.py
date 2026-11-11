"""Independent methods and prose-constraint checks for drill pack ci, pack 8, imported by drills-ci-8-check.py.
Each method is written apart from the drill's model solution: brute force on small inputs, a different
algorithm on large ones."""
import heapq, bisect
from collections import Counter, defaultdict, deque
from itertools import accumulate, combinations
from math import comb

# ======================= prose constraints, per drill (AssertionError names the broken rule) =======================

def v_grace(a):
    s, g = a["sessions"], a["grace"]
    assert all(0 <= x <= y <= 10**9 for x, y in s), "0 <= start <= end <= 1e9"
    assert 0 <= g <= 10**9

def v_rest(a):
    t, r = a["tasks"], a["rest"]
    assert all(isinstance(k, str) and k.isalpha() and k.islower() for k in r), "rest keys are names"
    assert all(isinstance(v, int) and 0 <= v <= 10**9 for v in r.values()), "rest 0 to 1e9"
    assert len(t) <= 100000

def v_robot(a):
    tok = a["text"].split()
    r, c = int(tok[0]), int(tok[1])
    assert 1 <= r <= 200 and 1 <= c <= 200, "r, c"
    rows = tok[2:2 + r]
    assert len(rows) == r and all(len(x) == c and set(x) <= set(".#R") for x in rows), "row shape"
    assert "".join(rows).count("R") == 1, "R once"
    cmds = tok[2 + r:]
    assert len(cmds) <= 10000, "commands"
    for k in cmds:
        assert k in ("L", "R") or (k[0] == "F" and k[1:].isdigit() and 1 <= int(k[1:]) <= 1000), f"command {k}"

def v_onebit(a):
    assert len(a["codes"]) <= 100000 and all(0 <= x < 2**30 for x in a["codes"])

def v_switch(a):
    sw, t = a["switches"], a["target"]
    assert len(sw) <= 14 and 1 <= len(t) <= 18
    assert all(len(s) == len(t) and set(s) <= set("01") for s in sw) and set(t) <= set("01"), "same length, 0 and 1"

VALID = {"ci-grace-sessions": v_grace, "ci-rest-days": v_rest, "ci-robot-floor": v_robot,
         "ci-one-bit-apart": v_onebit, "ci-switch-panel": v_switch}

# ======================= independent methods =======================

def merge_with_grace(sessions, grace):
    n = len(sessions)
    if n <= 300:
        # brute force: union every pair whose grace-widened spans meet, then read the groups
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for i in range(n):
            for j in range(n):
                (a, b), (c, d) = sessions[i], sessions[j]
                if a <= c <= b + grace:
                    parent[find(i)] = find(j)
        groups = defaultdict(list)
        for i in range(n):
            groups[find(i)].append(sessions[i])
        out = [[min(x for x, _ in g), max(y for _, y in g), len(g)] for g in groups.values()]
        return sorted(out)
    # large: cut the sorted starts where a start passes the running maximum end plus grace
    order = sorted(sessions)
    ends = list(accumulate((e for _, e in order), max))
    cuts = [0] + [i for i in range(1, n) if order[i][0] > ends[i - 1] + grace] + [n]
    return [[order[a][0], ends[b - 1], b - a] for a, b in zip(cuts, cuts[1:])]

def run_days(tasks, rest):
    if len(tasks) <= 200 and all(v <= 50 for v in rest.values()):
        # brute force: walk the calendar a day at a time
        last, out, day, k = {}, [], 0, 0
        while k < len(tasks):
            day += 1
            m = tasks[k]
            if m not in last or day - last[m] > rest.get(m, 0):
                last[m] = day
                out.append(day)
                k += 1
        return out
    last, out, day = {}, [], 0
    for m in tasks:
        day = day + 1 if m not in last else max(day + 1, last[m] + rest.get(m, 0) + 1)
        last[m] = day
        out.append(day)
    return out

def solve_robot_floor(text):
    # complex numbers for place and heading; each F jumps to the first blocked cell along the line
    tok = text.split()
    r, c = int(tok[0]), int(tok[1])
    rows = tok[2:2 + r]
    open_cells = {complex(i, j) for i in range(r) for j in range(c) if rows[i][j] != "#"}
    pos = next(complex(i, j) for i in range(r) for j in range(c) if rows[i][j] == "R")
    head = complex(-1, 0)
    seen = {pos}
    for k in tok[2 + r:]:
        if k == "L":
            head *= 1j
        elif k == "R":
            head *= -1j
        else:
            n = 0
            while n < int(k[1:]) and pos + head * (n + 1) in open_cells:
                n += 1
            for s in range(1, n + 1):
                seen.add(pos + head * s)
            pos += head * n
    face = {complex(-1, 0): "N", complex(0, 1): "E", complex(1, 0): "S", complex(0, -1): "W"}[head]
    return f"{int(pos.real)} {int(pos.imag)} {face} {len(seen)}"

def one_bit_pairs(codes):
    if len(codes) <= 3000:
        return sum(bin(codes[i] ^ codes[j]).count("1") == 1 for i in range(len(codes)) for j in range(i))
    # by bit: a pair differing only in bit b is (v without b, v with b)
    cnt = Counter(codes)
    return sum(k * cnt.get(v | (1 << b), 0) for b in range(30) for v, k in cnt.items() if not v >> b & 1)

def fewest_switches(switches, target):
    n, want = len(switches), int(target, 2)
    m = [int(s, 2) for s in switches]
    best = None
    for mask in range(1 << n):
        x = 0
        for i in range(n):
            if mask >> i & 1:
                x ^= m[i]
        if x == want:
            key = (bin(mask).count("1"), [i for i in range(n) if mask >> i & 1])
            if best is None or key < best:
                best = key
    return None if best is None else best[1]

INDEP = {"ci-grace-sessions": merge_with_grace, "ci-rest-days": run_days, "ci-robot-floor": solve_robot_floor,
         "ci-one-bit-apart": one_bit_pairs, "ci-switch-panel": fewest_switches}

SLOW_IDX = {"ci-rest-days": [2], "ci-one-bit-apart": [3]}

# ======================= numbers stated in the briefs, recomputed by the independent methods =======================
STATED = {
    "ci-grace-sessions": [(lambda: merge_with_grace([[30, 45], [0, 10], [12, 20], [50, 52], [44, 47]], 2), [[0, 20, 2], [30, 47, 2], [50, 52, 1]]),
                          (lambda: (12 - 10, 50 - 47), (2, 3))],
    "ci-rest-days": [(lambda: run_days(["kiln", "drum", "kiln", "kiln", "drum"], {"kiln": 2, "drum": 0}), [1, 2, 4, 7, 8])],
    "ci-robot-floor": [(lambda: solve_robot_floor("3 3\n...\n.#.\nR..\nF5 R F1 R F4\n"), "0 1 S 4")],
    "ci-one-bit-apart": [(lambda: one_bit_pairs([5, 4, 7, 5, 1]), 6), (lambda: (5 ^ 4, 5 ^ 7, 5 ^ 1), (1, 2, 4))],
    "ci-switch-panel": [(lambda: fewest_switches(["1000", "1100", "0011", "0111"], "1111"), [0, 3]),
                        (lambda: (int("1000", 2) ^ int("0111", 2), int("1100", 2) ^ int("0011", 2)), (15, 15)),
                        (lambda: [s for s in ["1000", "1100", "0011", "0111"] if int(s, 2) == 15], []),
                        (lambda: 0b0110 < 0b1001, True)],
}

# ======================= drills six to ten =======================

def v_rings(a):
    g, k = a["grid"], a["k"]
    assert 1 <= len(g) <= 100 and all(len(r) == len(g[0]) for r in g) and 1 <= len(g[0]) <= 100, "rectangular"
    assert 0 <= k <= 10**9

def v_checks(a):
    for s, e, need in a["jobs"]:
        assert 0 <= s <= e <= 10**9 and 1 <= need <= 5 and need <= e - s + 1, "job shape"
    assert len(a["jobs"]) <= 10000

def v_fit(a):
    b = a["bookings"]
    assert all(0 <= s < e <= 10**9 for s, e in b), "0 <= s < e"
    assert all(b[i][1] <= b[i + 1][0] for i in range(len(b) - 1)), "sorted, no overlap"
    assert 0 <= a["start"] <= 10**9 and 1 <= a["length"] <= 10**9

def v_rooms(a):
    assert all(0 <= s < e <= 10**9 for s, e in a["meetings"]), "start < end"
    assert 0 <= a["clean"] <= 10**6

def v_loop(a):
    f, b = a["fuel"], a["burn"]
    assert len(f) == len(b) and 1 <= len(f) <= 100000, "same length"

VALID.update({"ci-ring-turns": v_rings, "ci-double-checks": v_checks, "ci-first-fit-slot": v_fit,
              "ci-room-numbers": v_rooms, "ci-loop-starts": v_loop})

def turn_rings(grid, k):
    R, C = len(grid), len(grid[0])
    if k <= 30:
        # brute force: k single steps, each ring moved by one cell along its border
        g = [r[:] for r in grid]
        for _ in range(k):
            h = [r[:] for r in g]
            t = 0
            while R - 2 * t >= 2 and C - 2 * t >= 2:
                a, b, c, d = t, t, R - 1 - t, C - 1 - t
                path = [(a, j) for j in range(b, d + 1)] + [(i, d) for i in range(a + 1, c + 1)] + \
                       [(c, j) for j in range(d - 1, b - 1, -1)] + [(i, b) for i in range(c - 1, a, -1)]
                n = len(path)
                for x in range(n):
                    src, dst = (path[x], path[(x + 1) % n]) if t % 2 == 0 else (path[(x + 1) % n], path[x])
                    h[dst[0]][dst[1]] = g[src[0]][src[1]]
                t += 1
            g = h
        return g
    # by formula: each cell's ring and place along it, moved and mapped back
    def place(i, j, t):
        h, w = R - 2 * t, C - 2 * t
        i, j = i - t, j - t
        if i == 0: return j
        if j == w - 1: return w - 1 + i
        if i == h - 1: return w - 1 + h - 1 + (w - 1 - j)
        return 2 * (w - 1) + (h - 1) + (h - 1 - i)
    def cell(p, t):
        h, w = R - 2 * t, C - 2 * t
        if p < w - 1: return (t, t + p)
        p -= w - 1
        if p < h - 1: return (t + p, t + w - 1)
        p -= h - 1
        if p < w - 1: return (t + h - 1, t + w - 1 - p)
        p -= w - 1
        return (t + h - 1 - p, t)
    out = [r[:] for r in grid]
    for i in range(R):
        for j in range(C):
            t = min(i, j, R - 1 - i, C - 1 - j)
            if R - 2 * t < 2 or C - 2 * t < 2:
                continue
            n = 2 * (R - 2 * t) + 2 * (C - 2 * t) - 4
            q = (place(i, j, t) + (k if t % 2 == 0 else -k)) % n
            a, b = cell(q, t)
            out[a][b] = grid[i][j]
    return out

def fewest_checks(jobs):
    if not jobs:
        return 0
    lo, hi = min(s for s, _, _ in jobs), max(e for _, e, _ in jobs)
    if hi - lo <= 15:
        # brute force: the smallest set of minutes in the span that serves every job
        span = range(lo, hi + 1)
        for size in range(len(span) + 1):
            for pick in combinations(span, size):
                if all(sum(s <= m <= e for m in pick) >= need for s, e, need in jobs):
                    return size
    # the latest-free-minutes greedy with a set of used minutes (a scan for short jobs, a sorted list for long ones)
    used, order = set(), []
    for s, e, need in sorted(jobs, key=lambda j: (j[1], -j[0])):
        if e - s <= 1000:
            have = sum(m in used for m in range(s, e + 1))
        else:
            have = bisect.bisect_right(order, e) - bisect.bisect_left(order, s)
        m = e
        while have < need:
            if m not in used:
                used.add(m)
                bisect.insort(order, m)
                have += 1
            m -= 1
    return len(used)

def first_fit(bookings, start, length):
    # brute force: try `start` and every booking end after it, in order, against every booking
    cands = sorted({start} | {e for _, e in bookings if e >= start})
    slot = next(c for c in cands if all(e <= c or s >= c + length for s, e in bookings))
    # join by a sweep over start (+1) and end (-1) events: a block ends where the count falls to 0
    ev = sorted([(s, 1) for s, _ in bookings + [[slot, slot + length]]] + [(e, -1) for _, e in bookings + [[slot, slot + length]]],
                key=lambda x: (x[0], -x[1]))
    out, depth = [], 0
    for x, dlt in ev:
        if depth == 0 and dlt == 1:
            begin = x
        depth += dlt
        if depth == 0:
            out.append([begin, x])
    return [slot, out]

def room_numbers(meetings, clean):
    n = len(meetings)
    order = sorted(range(n), key=lambda i: (meetings[i][0], i))
    if n <= 2000:
        # brute force: scan the rooms from 0
        ready, out = [], [0] * n
        for i in order:
            s, e = meetings[i]
            r = next((r for r, t in enumerate(ready) if t <= s), len(ready))
            if r == len(ready):
                ready.append(0)
            ready[r] = e + clean
            out[i] = r
        return out
    # segment tree over room numbers holding each room's free minute; leftmost room free by `start`
    size = 1
    while size < n: size *= 2
    INF = float("inf")
    tree = [INF] * (2 * size)       # unopened rooms read as free from minus infinity, set below
    for r in range(n):
        tree[size + r] = -1
    for p in range(size - 1, 0, -1):
        tree[p] = min(tree[2 * p], tree[2 * p + 1])
    out = [0] * n
    for i in order:
        s, e = meetings[i]
        p = 1
        while p < size:
            p = 2 * p if tree[2 * p] <= s else 2 * p + 1
        r = p - size
        out[i] = r
        tree[p] = e + clean
        p //= 2
        while p:
            tree[p] = min(tree[2 * p], tree[2 * p + 1])
            p //= 2
    return out

def loop_starts(fuel, burn):
    n = len(fuel)
    gain = [f - b for f, b in zip(fuel, burn)]
    if n <= 2000:
        # brute force: drive from every depot
        out = []
        for s in range(n):
            tank, ok = 0, True
            for k in range(n):
                tank += gain[(s + k) % n]
                if tank < 0:
                    ok = False
                    break
            if ok:
                out.append(s)
        return out
    # doubled prefix sums with a sliding-window minimum over the next n prefixes
    P = [0]
    for k in range(2 * n):
        P.append(P[-1] + gain[k % n])
    out, dq = [], deque()
    for j in range(2 * n, 0, -1):          # window P[s+1 .. s+n], built from the right
        while dq and P[dq[-1]] >= P[j]:
            dq.pop()
        dq.append(j)
        s = j - 1
        if s < n:
            while dq[0] > s + n:
                dq.popleft()
            if P[dq[0]] - P[s] >= 0:
                out.append(s)
    return sorted(out)

INDEP.update({"ci-ring-turns": turn_rings, "ci-double-checks": fewest_checks, "ci-first-fit-slot": first_fit,
              "ci-room-numbers": room_numbers, "ci-loop-starts": loop_starts})
SLOW_IDX.update({"ci-ring-turns": [2], "ci-room-numbers": [3, 4, 5], "ci-loop-starts": [3, 4, 5]})
STATED.update({
    "ci-ring-turns": [(lambda: turn_rings([[4, 7, 1], [9, 5, 2], [8, 3, 6]], 1), [[9, 4, 7], [8, 5, 1], [3, 6, 2]])],
    "ci-double-checks": [(lambda: fewest_checks([[1, 4, 2], [3, 6, 2], [6, 8, 1]]), 3),
                         (lambda: all(sum(s <= m <= e for m in (3, 4, 6)) >= need for s, e, need in [[1, 4, 2], [3, 6, 2], [6, 8, 1]]), True)],
    "ci-first-fit-slot": [(lambda: first_fit([[2, 5], [5, 9], [12, 14], [16, 20]], 6, 3), [9, [[2, 14], [16, 20]]])],
    "ci-room-numbers": [(lambda: room_numbers([[0, 30], [5, 10], [12, 40], [35, 50]], 2), [0, 1, 1, 0]), (lambda: (10 + 2, 30 + 2), (12, 32))],
    "ci-loop-starts": [(lambda: loop_starts([3, 1, 4, 0], [1, 2, 2, 3]), [0]),
                       (lambda: [f - b for f, b in zip([3, 1, 4, 0], [1, 2, 2, 3])], [2, -1, 2, -3]),
                       (lambda: list(accumulate([2, -1, 2, -3])), [2, 1, 3, 0]), (lambda: list(accumulate([2, -3])), [2, -1])],
})

# ======================= drills eleven to fifteen =======================
from functools import lru_cache
from math import isqrt

def v_hops(a):
    s, lo, hi = a["stones"], a["lo"], a["hi"]
    assert 1 <= len(s) <= 100000 and s[0] == "." and s[-1] == "." and set(s) <= set(".~"), "stones"
    assert 1 <= lo <= hi <= len(s), "1 <= lo <= hi <= n"

def v_kbits(a):
    q = a["queries"]
    assert 1 <= len(q) <= 2000
    assert all(0 <= lo <= hi < 2**60 and 0 <= k <= 60 for lo, hi, k in q), "query shape"

def v_bonus(a):
    assert 1 <= len(a["scores"]) <= 100000 and all(0 <= x <= 10**9 for x in a["scores"])

def v_spiral(a):
    r, c, ks = a["rows"], a["cols"], a["ks"]
    assert 1 <= r <= 10**9 and 1 <= c <= 10**9 and 1 <= len(ks) <= 10000
    assert all(1 <= k <= r * c for k in ks), "1 <= k <= rows * cols"

def v_stops(a):
    tok = a["text"].split()
    n = int(tok[0])
    assert 1 <= n <= 60000, "n"
    pos, events = 1, 0
    while pos < len(tok):
        kind = tok[pos]
        assert kind in ("S", "B", "T"), kind
        width = 2 if kind == "B" else 3
        vals = [int(x) for x in tok[pos + 1:pos + width]]
        assert len(vals) == width - 1 and all(1 <= v <= 10**6 for v in vals), "p, q in 1..1e6"
        pos += width
        events += 1
    assert events == n, "n events"
    lines = [l for l in a["text"].split("\n") if l.strip()]
    assert len(lines) == n + 1, "one event a line"

VALID.update({"ci-stone-hops": v_hops, "ci-k-bit-count": v_kbits, "ci-ring-bonuses": v_bonus,
              "ci-spiral-cells": v_spiral, "ci-stop-cascade": v_stops})

def fewest_hops(stones, lo, hi):
    n = len(stones)
    if n <= 3000:
        # brute force: breadth-first search over every hop
        dist = {0: 0}
        q = deque([0])
        while q:
            i = q.popleft()
            for j in range(i + lo, min(i + hi, n - 1) + 1):
                if stones[j] == "." and j not in dist:
                    dist[j] = dist[i] + 1
                    q.append(j)
        return dist.get(n - 1, -1)
    # a table of best hop counts with a sliding-window minimum (deque of positions with increasing values)
    INF = float("inf")
    best = [INF] * n
    best[0] = 0
    dq = deque()
    for j in range(1, n):
        i = j - lo                      # position entering the window [j - hi, j - lo]
        if i >= 0 and best[i] < INF:
            while dq and best[dq[-1]] >= best[i]:
                dq.pop()
            dq.append(i)
        while dq and dq[0] < j - hi:
            dq.popleft()
        if stones[j] == "." and dq:
            best[j] = best[dq[0]] + 1
    return -1 if best[n - 1] == INF else best[n - 1]

def count_k_bits(queries):
    out = []
    for lo, hi, k in queries:
        if hi - lo <= 100000:
            # brute force
            out.append(sum(bin(x).count("1") == k for x in range(lo, hi + 1)))
            continue
        # digit dynamic programming over the bits of the bound, top down
        def upto(n):
            if n < 0:
                return 0
            bits = bin(n)[2:]
            @lru_cache(maxsize=None)
            def go(pos, left, tight):
                if left < 0:
                    return 0
                if pos == len(bits):
                    return 1 if left == 0 else 0
                top = int(bits[pos]) if tight else 1
                return sum(go(pos + 1, left - d, tight and d == top) for d in range(top + 1))
            return go(0, k, True)
        out.append(upto(hi) - upto(lo - 1))
    return out

def ring_bonuses(scores):
    n = len(scores)
    if n <= 300:
        # brute force: raise anyone short until nothing changes
        t = [1] * n
        changed = True
        while changed:
            changed = False
            for i in range(n):
                for j in ((i - 1) % n, (i + 1) % n):
                    if scores[i] > scores[j] and t[i] <= t[j]:
                        t[i] = t[j] + 1
                        changed = True
        return sum(t)
    # three copies in a line: the middle copy sees every rising run in full (a run is shorter than n)
    line = scores * 3
    m = len(line)
    L, R = [1] * m, [1] * m
    for i in range(1, m):
        if line[i] > line[i - 1]:
            L[i] = L[i - 1] + 1
    for i in range(m - 2, -1, -1):
        if line[i] > line[i + 1]:
            R[i] = R[i + 1] + 1
    return sum(max(L[i], R[i]) for i in range(n, 2 * n))

def spiral_cells(rows, cols, ks):
    if rows * cols <= 100000:
        # brute force: list the spiral
        order, seen = [], set()
        r = c = 0
        d = 0
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for _ in range(rows * cols):
            order.append([r, c])
            seen.add((r, c))
            for turn in range(4):
                dr, dc = moves[(d + turn) % 4]
                a, b = r + dr, c + dc
                if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen:
                    d = (d + turn) % 4
                    r, c = a, b
                    break
        return [order[k - 1] for k in ks]
    # the ring from the quadratic 4t^2 - 2(R + C)t + (k - 1) = 0, settled by integer square roots
    out = []
    S = rows + cols
    last = (min(rows, cols) - 1) // 2
    def before(t):
        return 2 * t * S - 4 * t * t
    for k in ks:
        disc = S * S - 4 * (k - 1)
        t = max(0, min(last, (S - isqrt(max(disc, 0))) // 4))
        while t > 0 and before(t) >= k:
            t -= 1
        while t < last and before(t + 1) < k:
            t += 1
        p = k - 1 - before(t)
        h, w = rows - 2 * t, cols - 2 * t
        sides = [(w, lambda x: [t, t + x]), (h - 1, lambda x: [t + 1 + x, t + w - 1]),
                 (w - 1, lambda x: [t + h - 1, t + w - 2 - x]), (h - 2, lambda x: [t + h - 2 - x, t])]
        for length, at in sides:
            if p < length:
                out.append(at(p))
                break
            p -= max(length, 0)
    return out

def solve_stop_cascade(text):
    tok = text.split()
    n = int(tok[0])
    pos, events = 1, []
    for _ in range(n):
        if tok[pos] == "B":
            events.append(("B", 0, int(tok[pos + 1])))
            pos += 2
        else:
            events.append((tok[pos], int(tok[pos + 1]), int(tok[pos + 2])))
            pos += 3
    if n <= 400:
        # brute force: lists, the cheapest sell found by a scan, stops fired one at a time in list order
        book, stops, last, vol, out = [], [], None, 0, []
        def buy(q):
            nonlocal last, vol
            while q and book:
                best = min(range(len(book)), key=lambda i: (book[i][0], i))
                take = min(q, book[best][1])
                q -= take
                vol += take
                last = book[best][0]
                book[best][1] -= take
                if book[best][1] == 0:
                    book.pop(best)
        for kind, p, q in events:
            if kind == "S":
                book.append([p, q])
            elif kind == "T":
                stops.append([p, q])
            else:
                buy(q)
            fired = True
            while fired:
                fired = False
                for i in range(len(stops)):
                    if last is not None and stops[i][0] <= last:
                        q = stops.pop(i)[1]
                        buy(q)
                        fired = True
                        break
            out.append(f"{last} {vol}" if last is not None else "- 0")
        return "\n".join(out)
    # large: price levels in a dict with a sorted price list; every stop in reach fires together as one buy
    # (a cascade only buys, so the cheapest shares go first and the order of firing cannot change the result)
    levels, prices, triggers, waiting = defaultdict(int), [], [], defaultdict(int)
    last, vol, out = None, 0, []
    def buy(q):
        nonlocal last, vol
        while q and prices:
            p = prices[0]
            take = min(q, levels[p])
            q -= take
            vol += take
            levels[p] -= take
            last = p
            if levels[p] == 0:
                prices.pop(0)
                del levels[p]
    for kind, p, q in events:
        if kind == "S":
            if p not in levels:
                bisect.insort(prices, p)
            levels[p] += q
        elif kind == "T":
            if p not in waiting:
                bisect.insort(triggers, p)
            waiting[p] += q
        else:
            buy(q)
        while last is not None and triggers and triggers[0] <= last:
            cut = bisect.bisect_right(triggers, last)
            total = sum(waiting.pop(t) for t in triggers[:cut])
            del triggers[:cut]
            buy(total)
        out.append(f"{last} {vol}" if last is not None else "- 0")
    return "\n".join(out)

INDEP.update({"ci-stone-hops": fewest_hops, "ci-k-bit-count": count_k_bits, "ci-ring-bonuses": ring_bonuses,
              "ci-spiral-cells": spiral_cells, "ci-stop-cascade": solve_stop_cascade})
SLOW_IDX.update({"ci-stone-hops": [3, 4, 5], "ci-k-bit-count": [3, 4], "ci-ring-bonuses": [3, 4],
                 "ci-spiral-cells": [3, 4, 5], "ci-stop-cascade": [3, 4, 5]})
STATED.update({
    "ci-stone-hops": [(lambda: fewest_hops("..~.~..", 2, 3), 2), (lambda: 6 - 0 > 3, True)],
    "ci-k-bit-count": [(lambda: count_k_bits([[5, 12, 2]]), [5]),
                       (lambda: [x for x in range(5, 13) if bin(x).count("1") == 2], [5, 6, 9, 10, 12]),
                       (lambda: [bin(x)[2:] for x in (5, 6, 9, 10, 12)], ["101", "110", "1001", "1010", "1100"])],
    "ci-ring-bonuses": [(lambda: ring_bonuses([3, 1, 2, 5]), 8), (lambda: 2 + 1 + 2 + 3, 8)],
    "ci-spiral-cells": [(lambda: spiral_cells(3, 4, list(range(1, 13))), [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [2, 2], [2, 1], [2, 0], [1, 0], [1, 1], [1, 2]]),
                        (lambda: spiral_cells(3, 4, [5, 11, 12]), [[1, 3], [1, 1], [1, 2]]),
                        (lambda: (10 ** 9 - 1) // 2 + 1, 5 * 10 ** 8)],
    "ci-stop-cascade": [(lambda: solve_stop_cascade("4\nS 10 2\nT 10 3\nS 12 5\nB 1\n"), "- 0\n- 0\n- 0\n12 4")],
})
