"""One plausible wrong (or too slow) solution per drill that the author did not plant.

Run through harness.py. A PASS line here is a finding: the hidden tests miss it.
"""
from collections import Counter, deque
from math import gcd


# ---------------- pack 1 ----------------

def best_block_sum(grid, s):
    # sentinel too high: the best total can be far below -10**9
    R, C = len(grid), len(grid[0])
    pre = [[0] * (C + 1) for _ in range(R + 1)]
    for r in range(R):
        for c in range(C):
            pre[r + 1][c + 1] = grid[r][c] + pre[r][c + 1] + pre[r + 1][c] - pre[r][c]
    best = -10 ** 9
    for r in range(s, R + 1):
        for c in range(s, C + 1):
            best = max(best, pre[r][c] - pre[r - s][c] - pre[r][c - s] + pre[r - s][c - s])
    return best


def cells_covered_at_least(rows, cols, rects, m):
    # identical cameras merged into one
    diff = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r1, c1, r2, c2 in set(map(tuple, rects)):
        diff[r1][c1] += 1
        diff[r1][c2 + 1] -= 1
        diff[r2 + 1][c1] -= 1
        diff[r2 + 1][c2 + 1] += 1
    count = 0
    above = [0] * cols
    for r in range(rows):
        acc = 0
        cur = [0] * cols
        for c in range(cols):
            acc += diff[r][c]
            cur[c] = above[c] + acc
            if cur[c] >= m:
                count += 1
        above = cur
    return count


def count_code_classes(codes):
    # repeats dropped at odd positions only
    return len({("".join(sorted(c[0::2])), "".join(sorted(set(c[1::2])))) for c in codes})


def solve_equal_three(text):
    # key built by gluing the two differences with no separator
    tokens = text.split()
    n = int(tokens[0])
    calls = tokens[1] if n else ""
    seen = {"00": 1}
    a = b = c = 0
    total = 0
    for ch in calls:
        if ch == "A":
            a += 1
        elif ch == "B":
            b += 1
        else:
            c += 1
        key = str(a - b) + str(b - c)
        total += seen.get(key, 0)
        seen[key] = seen.get(key, 0) + 1
    return str(total)


def longest_even_vowels(tape):
    # one parity bit for all vowels together
    first = {0: -1}
    mask = best = 0
    for i, ch in enumerate(tape):
        if ch in "aeiou":
            mask ^= 1
        if mask in first:
            best = max(best, i - first[mask])
        else:
            first[mask] = i
    return best


def count_mean_stretches(pnl, target):
    # a set of totals, not counts
    seen = {0}
    run = total = 0
    for x in pnl:
        run += x - target
        if run in seen:
            total += 1
        seen.add(run)
    return total


def others_product_grid(grid):
    # divides by a modular inverse where one exists, and multiplies the others out
    # cell by cell where it does not: quadratic when many cells share a factor with 12345
    M = 12345
    flat = [v for row in grid for v in row]
    total = 1
    for v in flat:
        total = total * v % M
    out = []
    for i, v in enumerate(flat):
        if gcd(v, M) == 1:
            out.append(total * pow(v, -1, M) % M)
        else:
            p = 1
            for j, w in enumerate(flat):
                if j != i:
                    p = p * w % M
            out.append(p)
    C = len(grid[0])
    return [out[i:i + C] for i in range(0, len(flat), C)]


def shortest_peak_stretch(badges):
    # every badge at the peak overwrites the answer: the last one wins, not the shortest
    count, first, last = {}, {}, {}
    for i, b in enumerate(badges):
        count[b] = count.get(b, 0) + 1
        first.setdefault(b, i)
        last[b] = i
    if not count:
        return 0
    peak = max(count.values())
    ans = 0
    for b in count:
        if count[b] == peak:
            ans = last[b] - first[b] + 1
    return ans


def count_row_column_matches(grid):
    # rows and columns keyed by their digits glued together: (1, 12) and (11, 2) collide
    rows = Counter("".join(map(str, r)) for r in grid)
    return sum(rows.get("".join(map(str, col)), 0) for col in zip(*grid))


def longest_serial_run(serials):
    # walks from run starts, but loops over the list, not the set:
    # a run start repeated many times is walked again each time
    present = set(serials)
    best = [0, 0]
    for x in serials:
        if x - 1 in present:
            continue
        y = x
        while y + 1 in present:
            y += 1
        length = y - x + 1
        if length > best[1] or (length == best[1] and x < best[0]):
            best = [x, length]
    return best


def count_steady_pairs(prices):
    # counts rises and falls of a penny a day
    up, down = Counter(), Counter()
    total = 0
    for i, p in enumerate(prices):
        total += up[p - i] + down[p + i]
        up[p - i] += 1
        down[p + i] += 1
    return total


def count_target_blocks(grid, target):
    # right method on the wrong axis: fixes two columns, O(C^2 R)
    R, C = len(grid), len(grid[0])
    total = 0
    for lo in range(C):
        row = [0] * R
        for hi in range(lo, C):
            for r in range(R):
                row[r] += grid[r][hi]
            seen = {0: 1}
            run = 0
            for v in row:
                run += v
                total += seen.get(run - target, 0)
                seen[run] = seen.get(run, 0) + 1
    return total


def shortest_cut_to_multiple(lots, p):
    # forgets to wrap the looked-up value back into 0 .. p - 1
    need = sum(lots) % p
    if need == 0:
        return 0
    last = {0: -1}
    run = 0
    best = len(lots)
    for i, x in enumerate(lots):
        run = (run + x) % p
        want = run - need
        if want in last:
            best = min(best, i - last[want])
        last[run] = i
    return -1 if best == len(lots) else best


def solve_unique_counts(text):
    # goes through the counts from smallest to largest with the same cap rule turned round
    tokens = text.split()
    n = int(tokens[0])
    counts = Counter(tokens[1:1 + n])
    removed = 0
    used = set()
    for c in sorted(counts.values()):
        if c in used:
            removed += c
        else:
            used.add(c)
    return str(removed)


def count_zero_quads(a, b, c, d):
    # pairs a with c and b with d by position (zip), then crosses
    sums = Counter(x + y for x in a for y in b)
    return sum(sums.get(-(x + y), 0) for x in set(c) for y in d)


# ---------------- pack 2 ----------------

def shortest_basket_cover(tape, basket):
    # a surplus basket ticker leaving the window is counted as missing
    need = Counter(basket)
    missing = len(basket)
    best = None
    left = 0
    for right, t in enumerate(tape):
        if t in need:
            if need[t] > 0:
                missing -= 1
            need[t] -= 1
        while missing == 0:
            if best is None or right - left < best[1] - best[0]:
                best = (left, right)
            u = tape[left]
            if u in need:
                need[u] += 1
                missing += 1
            left += 1
    return best


def push_cancelled_back(sizes):
    # removes each 0 from the middle and appends it: quadratic
    n = sizes.count(0)
    for _ in range(n):
        sizes.remove(0)
        sizes.append(0)
    return len(sizes) - n


def longest_capped_run(log, m):
    # the window that never shrinks: one step of the left edge per breach (`if`, not `while`)
    count = {}
    best = left = 0
    for right, x in enumerate(log):
        count[x] = count.get(x, 0) + 1
        if count[x] > m:
            count[log[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def fewest_end_lots(lots, x):
    # front sums in a dict, back sums looked up, with no check that the two ends overlap
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
        if i is not None and (best is None or i + j < best):
            best = i + j
    return -1 if best is None else best


def count_exact_venue_runs(venues, k):
    # at most k minus at most k - 1, but the window keeps one venue too many
    def at_most(m):
        count = {}
        left = total = 0
        for right, v in enumerate(venues):
            count[v] = count.get(v, 0) + 1
            while len(count) > m and left < right:
                u = venues[left]
                count[u] -= 1
                if count[u] == 0:
                    del count[u]
                left += 1
            total += right - left + 1
        return total
    return at_most(k) - at_most(k - 1)


def solve_excused_outages(text):
    # on a breach it steps the left edge once and assumes the day it dropped was a down day
    tokens = text.split()
    n, k = int(tokens[0]), int(tokens[1])
    days = tokens[2] if n else ""
    best = left = down = 0
    for right, c in enumerate(days):
        if c == "D":
            down += 1
        while down > k:
            down -= 1
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def count_frames(rods):
    # equal lengths treated as one rod
    a = sorted(set(rods))
    count = 0
    for k in range(len(a) - 1, 1, -1):
        i, j = 0, k - 1
        while i < j:
            if a[i] + a[j] > a[k]:
                count += j - i
                j -= 1
            else:
                i += 1
    return count


def best_hop_total(gains, k):
    # greedy: hop to the next depot in reach that does not lose money, else to the best in reach
    i, total, n = 0, gains[0], len(gains)
    while i < n - 1:
        reach = range(i + 1, min(i + k, n - 1) + 1)
        nxt = next((j for j in reach if gains[j] >= 0), None)
        if nxt is None:
            nxt = max(reach, key=lambda j: (gains[j], j))
        total += gains[nxt]
        i = nxt
    return total


def merge_late_fills(log, m, late):
    # merges from the back but compares whole tuples, so a tie goes by venue name
    i, j = m - 1, len(late) - 1
    k = m + len(late) - 1
    while j >= 0:
        if i >= 0 and log[i] > late[j]:
            log[k] = log[i]
            i -= 1
        else:
            log[k] = late[j]
            j -= 1
        k -= 1


def best_signal_pair(signals, k):
    # drops at most one stale signal per step (`if`, not `while`)
    best = None
    window = deque()
    for j, (t, v) in enumerate(signals):
        if window and t - signals[window[0]][0] > k:
            window.popleft()
        if window:
            ti, vi = signals[window[0]]
            score = vi - ti + v + t
            if best is None or score > best:
                best = score
        while window and signals[window[-1]][1] - signals[window[-1]][0] <= v - t:
            window.pop()
        window.append(j)
    return best


def longest_after_swaps(rota, k):
    # recomputes the window's commonest letter, but only among the two end letters
    count = {}
    best = left = 0
    for right, c in enumerate(rota):
        count[c] = count.get(c, 0) + 1
        while right - left + 1 - max(count[c], count[rota[left]]) > k:
            count[rota[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best




def netting_triples(sizes, target):
    # the 3Sum shortcut `if s[i] > target: break`, sound only when no size left is negative
    s = sorted(sizes)
    n = len(s)
    out = []
    for i in range(n - 2):
        if s[i] > target:
            break
        if i and s[i] == s[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = s[i] + s[lo] + s[hi]
            if total < target:
                lo += 1
            elif total > target:
                hi -= 1
            else:
                out.append((s[i], s[lo], s[hi]))
                lo += 1
                hi -= 1
                while lo < hi and s[lo] == s[lo - 1]:
                    lo += 1
                while lo < hi and s[hi] == s[hi + 1]:
                    hi -= 1
    return out


def count_matching_pairs(a, b, target):
    # adds the product of the two runs, then steps each pointer by one, so runs are counted again
    i, j = 0, len(b) - 1
    count = 0
    while i < len(a) and j >= 0:
        s = a[i] + b[j]
        if s < target:
            i += 1
        elif s > target:
            j -= 1
        else:
            ra = 1
            while i + ra < len(a) and a[i + ra] == a[i]:
                ra += 1
            rb = 1
            while j - rb >= 0 and b[j - rb] == b[j]:
                rb += 1
            count += ra * rb
            i += 1
            j -= 1
    return count


def solve_van_pairs(text):
    # lower bound only: half the parcels rounded up, or the number too heavy to share
    tokens = text.split()
    n, cap = int(tokens[0]), int(tokens[1])
    w = [int(t) for t in tokens[2:2 + n]]
    return str(max((n + 1) // 2, sum(1 for x in w if 2 * x > cap)))


def widest_banner(posts):
    # moves the shorter post, but on equal heights stops looking
    i, j = 0, len(posts) - 1
    best = 0
    while i < j:
        best = max(best, min(posts[i], posts[j]) * (j - i))
        if posts[i] < posts[j]:
            i += 1
        elif posts[i] > posts[j]:
            j -= 1
        else:
            break
    return best
