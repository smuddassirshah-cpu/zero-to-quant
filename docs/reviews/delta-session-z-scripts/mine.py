"""Delta reader's own solutions for the changed ci drills (independent of the model where a second method exists)."""
from collections import Counter, defaultdict
from bisect import bisect_left, bisect_right
import heapq


def best_block_sum(grid, s):
    R, C = len(grid), len(grid[0])
    rows = []
    for row in grid:
        w = sum(row[:s]); out = [w]
        for c in range(s, C):
            w += row[c] - row[c - s]; out.append(w)
        rows.append(out)
    best = None
    col = [sum(rows[r][c] for r in range(s)) for c in range(C - s + 1)]
    best = max(col)
    for r in range(s, R):
        add, sub = rows[r], rows[r - s]
        col = [x + a - b for x, a, b in zip(col, add, sub)]
        m = max(col)
        if m > best:
            best = m
    return best


def longest_capped_run(log, m):
    n = len(log)
    def ok(L):
        if L == 0:
            return True
        cnt = Counter(); bad = 0
        for i, x in enumerate(log):
            cnt[x] += 1
            if cnt[x] == m + 1: bad += 1
            if i >= L:
                y = log[i - L]
                if cnt[y] == m + 1: bad -= 1
                cnt[y] -= 1
            if i >= L - 1 and bad == 0:
                return True
        return False
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid): lo = mid
        else: hi = mid - 1
    return lo


def count_code_classes(codes):
    return len({(tuple(sorted(Counter(c[0::2]).items())), tuple(sorted(Counter(c[1::2]).items())), len(c)) for c in codes})


def fewest_end_lots(lots, x):
    n = len(lots)
    pre = [0]
    for v in lots: pre.append(pre[-1] + v)
    suf = [0]
    for v in reversed(lots): suf.append(suf[-1] + v)
    best = -1
    for i in range(n + 1):
        need = x - pre[i]
        if need < 0: break
        j = bisect_left(suf, need, 0, n - i + 1)
        if j <= n - i and suf[j] == need:
            if best < 0 or i + j < best: best = i + j
    return best


def solve_equal_three(text):
    lines = text.split("\n")
    n = int(lines[0].strip())
    calls = ""
    for ln in lines[1:]:
        if ln.strip():
            calls = ln.strip(); break
    calls = calls[:n]
    a = b = c = 0
    seen = [(0, 0)]
    for ch in calls:
        if ch == "A": a += 1
        elif ch == "B": b += 1
        else: c += 1
        seen.append((a - b, a - c))
    return str(sum(v * (v - 1) // 2 for v in Counter(seen).values()))


def longest_even_vowels(tape):
    first = {0: -1}; mask = 0; best = 0
    idx = {"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}
    for i, ch in enumerate(tape):
        mask ^= idx.get(ch, 0)
        if mask in first: best = max(best, i - first[mask])
        else: first[mask] = i
    return best


def count_mean_stretches(pnl, target):
    run = 0; pre = [0]
    for x in pnl:
        run += x - target; pre.append(run)
    pre.sort()
    total = 0; i = 0
    while i < len(pre):
        j = i
        while j < len(pre) and pre[j] == pre[i]: j += 1
        k = j - i; total += k * (k - 1) // 2; i = j
    return total


def others_product_grid(grid):
    M = 10010
    C = len(grid[0])
    flat = [v for row in grid for v in row]
    n = len(flat)
    out = [0] * n
    # iterative divide and conquer: stack of (lo, hi, product of everything outside)
    stack = [(0, n, 1)]
    while stack:
        lo, hi, outside = stack.pop()
        if hi - lo == 1:
            out[lo] = outside % M; continue
        mid = (lo + hi) // 2
        pl = 1
        for v in flat[lo:mid]: pl = pl * v % M
        pr = 1
        for v in flat[mid:hi]: pr = pr * v % M
        stack.append((lo, mid, outside * pr % M))
        stack.append((mid, hi, outside * pl % M))
    return [out[i:i + C] for i in range(0, n, C)]


def best_signal_pair(signals, k):
    heap = []; best = None
    for t, v in signals:
        while heap and t - heap[0][1] > k:
            heapq.heappop(heap)
        if heap:
            s = -heap[0][0] + v + t
            if best is None or s > best: best = s
        heapq.heappush(heap, (-(v - t), t))
    return best


def shortest_peak_stretch(badges):
    pos = defaultdict(list)
    for i, b in enumerate(badges): pos[b].append(i)
    if not pos: return 0
    peak = max(len(p) for p in pos.values())
    return min(p[-1] - p[0] + 1 for p in pos.values() if len(p) == peak)


def longest_after_swaps(rota, k):
    best = 0
    for L in set(rota):
        left = 0; other = 0
        for right, c in enumerate(rota):
            if c != L: other += 1
            while other > k:
                if rota[left] != L: other -= 1
                left += 1
            best = max(best, right - left + 1)
    return best


def count_row_column_matches(grid):
    cols = [list(c) for c in zip(*grid)]
    return sum(1 for row in grid for col in cols if list(row) == col)


def longest_serial_run(serials):
    if not serials: return [0, 0]
    u = sorted(set(serials))
    best = [u[0], 1]; start = u[0]; ln = 1
    for a, b in zip(u, u[1:]):
        if b == a + 1: ln += 1
        else: start = b; ln = 1
        if ln > best[1]: best = [start, ln]
    return best


def count_target_blocks(grid, target):
    R, C = len(grid), len(grid[0])
    if R * C <= 400:
        P = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                P[r + 1][c + 1] = P[r][c + 1] + P[r + 1][c] - P[r][c] + grid[r][c]
        return sum(1 for r1 in range(R) for r2 in range(r1 + 1, R + 1) for c1 in range(C) for c2 in range(c1 + 1, C + 1)
                   if P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1] == target)
    total = 0
    for top in range(R):
        col = [0] * C
        for bot in range(top, R):
            row = grid[bot]
            col = [a + b for a, b in zip(col, row)]
            seen = Counter(); seen[0] = 1; run = 0
            for v in col:
                run += v
                total += seen[run - target]
                seen[run] += 1
    return total


def netting_triples(sizes, target):
    cnt = Counter(sizes); vals = sorted(cnt)
    out = []
    for i, x in enumerate(vals):
        for y in vals[i:]:
            z = target - x - y
            if z < y or z not in cnt: continue
            need = Counter([x, y, z])
            if all(cnt[v] >= q for v, q in need.items()):
                out.append((x, y, z))
    return sorted(out)


def shortest_cut_to_multiple(lots, p):
    n = len(lots)
    total = sum(lots)
    need = total % p
    if need == 0: return 0
    last = {0: 0}; run = 0; best = None
    for i, v in enumerate(lots, 1):
        run = (run + v) % p
        want = (run - need) % p
        if want in last:
            L = i - last[want]
            if L < n and (best is None or L < best): best = L
        last[run] = i
    return -1 if best is None else best


def widest_banner(posts):
    n = len(posts)
    if n < 2: return 0
    order = sorted(range(n), key=lambda i: -posts[i])
    lo = hi = None; best = 0
    for i in order:
        if lo is not None:
            best = max(best, posts[i] * max(i - lo, hi - i))
        lo = i if lo is None else min(lo, i)
        hi = i if hi is None else max(hi, i)
    return best


def count_zero_quads(a, b, c, d):
    ab = Counter(x + y for x in a for y in b)
    cd = Counter(x + y for x in c for y in d)
    if len(ab) > len(cd): ab, cd = cd, ab
    return sum(q * cd.get(-s, 0) for s, q in ab.items())


def split_by_reference(sizes, ref):
    s = sorted(sizes)
    sizes[:] = s
    return (bisect_left(s, ref), bisect_right(s, ref))
