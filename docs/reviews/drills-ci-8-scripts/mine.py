"""Second reader's own solutions to pack 8, written from the candidate's view
(brief, constraints, hint, examples) before reading the model solutions.
Where a second method exists I used it (noted per function)."""
import heapq
from bisect import bisect_left, bisect_right, insort
from collections import Counter, deque
from itertools import combinations
from math import comb


def merge_with_grace(sessions, grace):
    out = []
    for s, e in sorted(map(tuple, sessions)):
        if out and s <= out[-1][1] + grace:
            if e > out[-1][1]:
                out[-1][1] = e
            out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out


def run_days(tasks, rest):
    ready = {}
    day = 0
    out = []
    for m in tasks:
        day = max(day + 1, ready.get(m, 1))
        out.append(day)
        ready[m] = day + rest.get(m, 0) + 1
    return out


def solve_robot_floor(text):
    tok = text.split()
    r, c = int(tok[0]), int(tok[1])
    rows = tok[2:2 + r]
    cmds = tok[2 + r:]
    for i in range(r):
        j = rows[i].find('R')
        if j >= 0:
            y, x = i, j
    d = 0
    dy = (-1, 0, 1, 0)
    dx = (0, 1, 0, -1)
    seen = {(y, x)}
    i = 0
    while i < len(cmds):
        t = cmds[i]
        i += 1
        if t == 'L':
            d = (d + 3) % 4
        elif t == 'R':
            d = (d + 1) % 4
        else:
            if t == 'F':          # "F 5" written apart
                k = int(cmds[i])
                i += 1
            else:
                k = int(t[1:])
            for _ in range(k):
                ny, nx = y + dy[d], x + dx[d]
                if not (0 <= ny < r and 0 <= nx < c) or rows[ny][nx] == '#':
                    break
                y, x = ny, nx
                seen.add((y, x))
    return '%d %d %s %d' % (y, x, 'NESW'[d], len(seen))


def fewest_checks(jobs):
    # by end; a set of used minutes and a sorted list for the counting
    used = set()
    vis = []
    for s, e, need in sorted(jobs, key=lambda j: (j[1], j[0])):
        have = bisect_right(vis, e) - bisect_left(vis, s)
        m = e
        while have < need:
            if m not in used:
                used.add(m)
                insort(vis, m)
                have += 1
            m -= 1
    return len(vis)


def first_fit(bookings, start, length):
    slot = start
    for s, e in bookings:
        if e <= slot:
            continue
        if s >= slot + length:
            break
        slot = e
    allb = sorted([list(b) for b in bookings] + [[slot, slot + length]])
    merged = []
    for s, e in allb:
        if merged and merged[-1][1] == s:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    return [slot, merged]


def one_bit_pairs(codes):
    # every ordered pair counted, then halved
    cnt = Counter(codes)
    tot = 0
    for c, k in cnt.items():
        for b in range(30):
            o = cnt.get(c ^ (1 << b))
            if o:
                tot += k * o
    return tot // 2


def turn_rings(grid, k):
    R, C = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    t = 0
    while R - 2 * t >= 2 and C - 2 * t >= 2:
        top, left, bot, right = t, t, R - 1 - t, C - 1 - t
        cells = [(top, j) for j in range(left, right + 1)]
        cells += [(i, right) for i in range(top + 1, bot + 1)]
        cells += [(bot, j) for j in range(right - 1, left - 1, -1)]
        cells += [(i, left) for i in range(bot - 1, top, -1)]
        n = len(cells)
        sh = k % n if t % 2 == 0 else (-k) % n
        for idx, (i, j) in enumerate(cells):
            a, b = cells[(idx + sh) % n]
            out[a][b] = grid[i][j]
        t += 1
    return out


def fewest_switches(switches, target):
    nums = [int(s, 2) for s in switches]
    tg = int(target, 2)
    for size in range(len(nums) + 1):
        for combo in combinations(range(len(nums)), size):
            x = 0
            for i in combo:
                x ^= nums[i]
            if x == tg:
                return list(combo)
    return None


def count_k_bits(queries):
    def below(n, k):          # numbers x with 0 <= x < n and k set bits
        tot = 0
        ones = 0
        for i in range(n.bit_length() - 1, -1, -1):
            if n >> i & 1:
                if 0 <= k - ones <= i:
                    tot += comb(i, k - ones)
                ones += 1
                if ones > k:
                    break
        return tot
    return [below(hi + 1, k) - below(lo, k) for lo, hi, k in queries]


def loop_starts(fuel, burn):
    # sliding minimum of the doubled prefix sums with a deque
    n = len(fuel)
    g = [f - b for f, b in zip(fuel, burn)]
    if sum(g) < 0:
        return []
    pre = [0] * (2 * n + 1)
    for i in range(2 * n):
        pre[i + 1] = pre[i] + g[i % n]
    out = []
    dq = deque()
    for j in range(1, n):
        while dq and pre[dq[-1]] >= pre[j]:
            dq.pop()
        dq.append(j)
    for s in range(n):
        j = s + n
        while dq and pre[dq[-1]] >= pre[j]:
            dq.pop()
        dq.append(j)
        while dq[0] <= s:
            dq.popleft()
        if pre[dq[0]] >= pre[s]:
            out.append(s)
    return out


def ring_bonuses(scores):
    # in increasing order of score: one more than the largest lower neighbour
    n = len(scores)
    tok = [1] * n
    for i in sorted(range(n), key=scores.__getitem__):
        for j in ((i - 1) % n, (i + 1) % n):
            if scores[j] < scores[i] and tok[j] + 1 > tok[i]:
                tok[i] = tok[j] + 1
    return sum(tok)


def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: meetings[i][0])
    busy = []
    free = []
    opened = 0
    out = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room = opened
            opened += 1
        out[i] = room
        heapq.heappush(busy, (e + clean, room))
    return out


def spiral_cells(rows, cols, ks):
    def before(t):
        return rows * cols - (rows - 2 * t) * (cols - 2 * t)
    tmax = (min(rows, cols) - 1) // 2
    out = []
    for k in ks:
        lo, hi = 0, tmax
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if before(mid) < k:
                lo = mid
            else:
                hi = mid - 1
        t = lo
        o = k - before(t) - 1
        h, w = rows - 2 * t, cols - 2 * t
        if h == 1:
            out.append([t, t + o])
        elif w == 1:
            out.append([t + o, t])
        elif o < w:
            out.append([t, t + o])
        elif o < w + h - 1:
            out.append([t + 1 + o - w, t + w - 1])
        elif o < 2 * w + h - 2:
            out.append([t + h - 1, t + w - 2 - (o - w - h + 1)])
        else:
            out.append([t + h - 2 - (o - 2 * w - h + 2), t])
    return out


def fewest_hops(stones, lo, hi):
    # table of fewest hops with a sliding minimum over [j - hi, j - lo]
    n = len(stones)
    INF = float('inf')
    dp = [INF] * n
    dp[0] = 0
    dq = deque()
    for j in range(1, n):
        i = j - lo
        if i >= 0 and dp[i] < INF:
            while dq and dp[dq[-1]] >= dp[i]:
                dq.pop()
            dq.append(i)
        while dq and dq[0] < j - hi:
            dq.popleft()
        if stones[j] == '.' and dq:
            dp[j] = dp[dq[0]] + 1
    return -1 if dp[-1] == INF else dp[-1]


def solve_stop_cascade(text):
    lines = [ln.split() for ln in text.split('\n')]
    lines = [ln for ln in lines if ln]
    n = int(lines[0][0])
    book = []
    stops = []
    last = None
    total = 0
    out = []

    def buy(q):
        nonlocal last, total
        while q and book:
            top = book[0]
            take = min(q, top[1])
            q -= take
            top[1] -= take
            total += take
            last = top[0]
            if top[1] == 0:
                heapq.heappop(book)

    for ev in lines[1:1 + n]:
        if ev[0] == 'S':
            heapq.heappush(book, [int(ev[1]), int(ev[2])])
        elif ev[0] == 'B':
            buy(int(ev[1]))
        else:
            heapq.heappush(stops, (int(ev[1]), int(ev[2])))
        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[1])
        out.append('- 0' if last is None else '%d %d' % (last, total))
    return '\n'.join(out)
