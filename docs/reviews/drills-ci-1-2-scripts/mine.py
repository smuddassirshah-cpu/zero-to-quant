"""Second reader's own solutions to the 30 drills of ci packs 1 and 2.

Written from brief, constraints and examples, by a method that differs from the
model solution wherever one exists. Run through harness.py.
"""
import heapq
from bisect import bisect_left
from collections import Counter, defaultdict


# ---------------- pack 1 ----------------

def best_block_sum(grid, s):
    R, C = len(grid), len(grid[0])
    col = [sum(grid[r][c] for r in range(s)) for c in range(C)]
    best = None
    for top in range(R - s + 1):
        if top:
            old, new = grid[top - 1], grid[top + s - 1]
            for c in range(C):
                col[c] += new[c] - old[c]
        w = sum(col[:s])
        if best is None or w > best:
            best = w
        for c in range(s, C):
            w += col[c] - col[c - s]
            if w > best:
                best = w
    return best


def cells_covered_at_least(rows, cols, rects, m):
    line = [[0] * (cols + 1) for _ in range(rows)]
    for r1, c1, r2, c2 in rects:
        for r in range(r1, r2 + 1):
            line[r][c1] += 1
            line[r][c2 + 1] -= 1
    n = 0
    for r in range(rows):
        acc = 0
        for c in range(cols):
            acc += line[r][c]
            if acc >= m:
                n += 1
    return n


def count_code_classes(codes):
    def key(code):
        e = [0] * 26
        o = [0] * 26
        for i, ch in enumerate(code):
            (o if i % 2 else e)[ord(ch) - 97] += 1
        return (tuple(e), tuple(o))
    return len({key(c) for c in codes})


def solve_equal_three(text):
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    n = int(lines[0])
    calls = lines[1] if n else ""
    seen = Counter()
    a = b = c = 0
    seen[(0, 0)] = 1
    for ch in calls:
        if ch == "A":
            a += 1
        elif ch == "B":
            b += 1
        else:
            c += 1
        seen[(a - c, b - c)] += 1
    return str(sum(v * (v - 1) // 2 for v in seen.values()))


def longest_even_vowels(tape):
    first = [None] * 32
    first[0] = -1
    mask = best = 0
    for i, ch in enumerate(tape):
        p = "aeiou".find(ch)
        if p >= 0:
            mask ^= 1 << p
        if first[mask] is None:
            first[mask] = i
        elif i - first[mask] > best:
            best = i - first[mask]
    return best


def count_mean_stretches(pnl, target):
    pre = [0]
    for x in pnl:
        pre.append(pre[-1] + x)
    keys = Counter(pre[i] - target * i for i in range(len(pre)))
    return sum(v * (v - 1) // 2 for v in keys.values())


def others_product_grid(grid):
    M = 12345
    flat = [v for row in grid for v in row]
    n = len(flat)
    pre = [1] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] * flat[i] % M
    suf = [1] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] * flat[i] % M
    out = [pre[i] * suf[i + 1] % M for i in range(n)]
    C = len(grid[0])
    return [out[i:i + C] for i in range(0, n, C)]


def shortest_peak_stretch(badges):
    pos = defaultdict(list)
    for i, b in enumerate(badges):
        pos[b].append(i)
    if not pos:
        return 0
    peak = max(len(p) for p in pos.values())
    return min(p[-1] - p[0] + 1 for p in pos.values() if len(p) == peak)


def count_row_column_matches(grid):
    rows = Counter(tuple(r) for r in grid)
    cols = Counter(tuple(grid[r][c] for r in range(len(grid))) for c in range(len(grid)))
    return sum(v * cols[k] for k, v in rows.items())


def longest_serial_run(serials):
    u = sorted(set(serials))
    if not u:
        return [0, 0]
    best = [u[0], 1]
    start = 0
    for i in range(1, len(u) + 1):
        if i == len(u) or u[i] != u[i - 1] + 1:
            if i - start > best[1]:
                best = [u[start], i - start]
            start = i
    return best


def count_steady_pairs(prices):
    c = Counter(p - i for i, p in enumerate(prices))
    return sum(v * (v - 1) // 2 for v in c.values())


def count_target_blocks(grid, target):
    R, C = len(grid), len(grid[0])
    # column prefix sums down the rows
    down = [[0] * C]
    for r in range(R):
        down.append([down[-1][c] + grid[r][c] for c in range(C)])
    total = 0
    for top in range(R):
        for bottom in range(top + 1, R + 1):
            a, b = down[bottom], down[top]
            seen = defaultdict(int)
            seen[0] = 1
            run = 0
            for c in range(C):
                run += a[c] - b[c]
                total += seen[run - target]
                seen[run] += 1
    return total


def shortest_cut_to_multiple(lots, p):
    n = len(lots)
    need = sum(lots) % p
    if need == 0:
        return 0
    pre = [0]
    for x in lots:
        pre.append((pre[-1] + x) % p)
    # stretch (i, j]: pre[j] - pre[i] == need (mod p), 0 <= i < j <= n, not (0, n)
    latest = {}
    best = None
    for j in range(n + 1):
        i = latest.get((pre[j] - need) % p)
        if i is not None and j - i < n:
            if best is None or j - i < best:
                best = j - i
        latest[pre[j]] = j
    return -1 if best is None else best


def solve_unique_counts(text):
    tok = text.split()
    n = int(tok[0])
    counts = Counter(tok[1:1 + n])
    used = set()
    removed = 0
    for c in counts.values():
        while c > 0 and c in used:
            c -= 1
            removed += 1
        if c:
            used.add(c)
    return str(removed)


def count_zero_quads(a, b, c, d):
    ab = Counter(x + y for x in a for y in b)
    cd = Counter(x + y for x in c for y in d)
    return sum(v * cd.get(-k, 0) for k, v in ab.items())


# ---------------- pack 2 ----------------

def shortest_basket_cover(tape, basket):
    want = Counter(basket)
    have = Counter()
    formed = 0
    best = None
    left = 0
    for right, t in enumerate(tape):
        have[t] += 1
        if t in want and have[t] == want[t]:
            formed += 1
        while formed == len(want):
            if best is None or right - left < best[1] - best[0]:
                best = (left, right)
            u = tape[left]
            have[u] -= 1
            if u in want and have[u] < want[u]:
                formed -= 1
            left += 1
    return best


def push_cancelled_back(sizes):
    live = [x for x in sizes if x != 0]
    n = len(sizes)
    sizes[:] = live + [0] * (n - len(live))
    return len(live)


def longest_capped_run(log, m):
    pos = defaultdict(list)
    left = best = 0
    for i, x in enumerate(log):
        p = pos[x]
        p.append(i)
        if len(p) > m:
            left = max(left, p[-m - 1] + 1)
        best = max(best, i - left + 1)
    return best


def fewest_end_lots(lots, x):
    n = len(lots)
    front = {0: 0}
    s = 0
    for i, v in enumerate(lots):
        s += v
        front.setdefault(s, i + 1)
    best = None
    s = 0
    for j in range(n + 1):
        if j:
            s += lots[n - j]
        i = front.get(x - s)
        if i is not None and i + j <= n:
            if best is None or i + j < best:
                best = i + j
    return -1 if best is None else best


def count_exact_venue_runs(venues, k):
    # two left edges: lo is the first start with at most k venues,
    # hi the first start with fewer than k venues
    c1, c2 = {}, {}
    lo = hi = 0
    total = 0
    for right, v in enumerate(venues):
        c1[v] = c1.get(v, 0) + 1
        c2[v] = c2.get(v, 0) + 1
        while len(c1) > k:
            u = venues[lo]
            c1[u] -= 1
            if not c1[u]:
                del c1[u]
            lo += 1
        while len(c2) >= k:
            u = venues[hi]
            c2[u] -= 1
            if not c2[u]:
                del c2[u]
            hi += 1
        total += hi - lo
    return total


def solve_excused_outages(text):
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    days = tok[2] if n else ""
    downs = [-1] + [i for i, c in enumerate(days) if c == "D"] + [n]
    if len(downs) - 2 <= k:
        return str(n)
    best = 0
    for a in range(len(downs) - k - 1):
        best = max(best, downs[a + k + 1] - downs[a] - 1)
    return str(best)


def count_frames(rods):
    a = sorted(rods)
    n = len(a)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            k = bisect_left(a, a[i] + a[j], j + 1)
            total += k - j - 1
    return total


def best_hop_total(gains, k):
    heap = [(-gains[0], 0)]
    best = gains[0]
    for i in range(1, len(gains)):
        while heap[0][1] < i - k:
            heapq.heappop(heap)
        best = gains[i] - heap[0][0]
        heapq.heappush(heap, (-best, i))
    return best


def merge_late_fills(log, m, late):
    merged = []
    i = j = 0
    while i < m or j < len(late):
        if j == len(late) or (i < m and log[i][0] <= late[j][0]):
            merged.append(log[i])
            i += 1
        else:
            merged.append(late[j])
            j += 1
    log[:] = merged


def best_signal_pair(signals, k):
    heap = []
    best = None
    for t, v in signals:
        while heap and t - heap[0][1] > k:
            heapq.heappop(heap)
        if heap:
            sc = -heap[0][0] + v + t
            if best is None or sc > best:
                best = sc
        heapq.heappush(heap, (-(v - t), t))
    return best


def longest_after_swaps(rota, k):
    best = 0
    for letter in set(rota):
        left = other = 0
        for right, c in enumerate(rota):
            if c != letter:
                other += 1
            while other > k:
                if rota[left] != letter:
                    other -= 1
                left += 1
            best = max(best, right - left + 1)
    return best


def netting_triples(sizes, target):
    cnt = Counter(sizes)
    u = sorted(cnt)
    out = []
    for a, x in enumerate(u):
        for y in u[a:]:
            z = target - x - y
            if z < y:
                break
            if z not in cnt:
                continue
            need = Counter((x, y, z))
            if all(cnt[v] >= c for v, c in need.items()):
                out.append((x, y, z))
    return out


def count_matching_pairs(a, b, target):
    cb = Counter(b)
    return sum(v * cb.get(target - x, 0) for x, v in Counter(a).items())


def solve_van_pairs(text):
    tok = text.split()
    n, cap = int(tok[0]), int(tok[1])
    w = sorted((int(t) for t in tok[2:2 + n]), reverse=True)
    light = n - 1
    vans = 0
    heavy = 0
    while heavy <= light:
        if heavy < light and w[heavy] + w[light] <= cap:
            light -= 1
        heavy += 1
        vans += 1
    return str(vans)


def widest_banner(posts):
    order = sorted(range(len(posts)), key=lambda i: -posts[i])
    lo = hi = None
    best = 0
    for i in order:
        if lo is not None:
            best = max(best, posts[i] * max(i - lo, hi - i))
            lo, hi = min(lo, i), max(hi, i)
        else:
            lo = hi = i
    return best
