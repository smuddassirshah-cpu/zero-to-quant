"""Delta reader's own solutions, pack 8. Written from the briefs, by a method other
than the model's wherever one exists. Used by run.py. Plain brute forces for the
small cases are in extra_8.py."""
import bisect
import heapq
from collections import deque


# ci-double-checks: not the greedy. With P(t) = visits at minutes up to t, the rules are
# P(end) - P(start - 1) >= need and 0 <= P(b) - P(a) <= b - a for neighbouring key minutes,
# and the fewest visits are the longest path over those difference constraints.
def fewest_checks(jobs):
    if not jobs:
        return 0
    pts = sorted({s - 1 for s, e, k in jobs} | {e for s, e, k in jobs})
    idx = {p: i for i, p in enumerate(pts)}
    n = len(pts)
    d = [0] * n
    by_end = sorted((idx[e], idx[s - 1], k) for s, e, k in jobs)
    changed = True
    while changed:
        changed = False
        j = 0
        for i in range(n):                       # forward: later minutes hold at least as many
            if i and d[i - 1] > d[i]:
                d[i] = d[i - 1]
                changed = True
            while j < len(by_end) and by_end[j][0] == i:
                _, a, k = by_end[j]
                if d[a] + k > d[i]:
                    d[i] = d[a] + k
                    changed = True
                j += 1
        for i in range(n - 2, -1, -1):           # backward: at most one visit a minute
            need = d[i + 1] - (pts[i + 1] - pts[i])
            if need > d[i]:
                d[i] = need
                changed = True
    return d[n - 1] - d[0]


# ci-first-fit-slot: list the free gaps, take the first with room from `start`, then join.
def first_fit(bookings, start, length):
    slot = None
    prev_end = 0
    for s, e in bookings:
        lo = max(prev_end, start)
        if lo + length <= s:
            slot = lo
            break
        prev_end = e
    if slot is None:
        slot = max(prev_end, start)
    allb = sorted([list(b) for b in bookings] + [[slot, slot + length]])
    merged = []
    for s, e in allb:
        if merged and merged[-1][1] >= s:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [slot, merged]


# ci-k-bit-count: a bit-by-bit count with no binomial coefficients.
def _upto(n, k):
    """numbers in 0..n with exactly k set bits"""
    if n < 0:
        return 0
    free = [0] * 62          # free[j] = numbers already below n with j set bits so far
    tight = 0                # set bits of n above the current bit
    for b in range(60, -1, -1):
        nxt = [0] * 62
        for j in range(61):
            if free[j]:
                nxt[j] += free[j]
                nxt[j + 1] += free[j]
        if n >> b & 1:
            nxt[tight] += 1      # put 0 here, below n from now on
            tight += 1
        free = nxt
    return free[k] + (1 if tight == k else 0) if k <= 61 else 0


def count_k_bits(queries):
    return [_upto(hi, k) - _upto(lo - 1, k) for lo, hi, k in queries]


# ci-rest-days
def run_days(tasks, rest):
    last = {}
    day = 0
    out = []
    for m in tasks:
        day += 1
        if m in last:
            earliest = last[m] + rest.get(m, 0) + 1
            if earliest > day:
                day = earliest
        last[m] = day
        out.append(day)
    return out


# ci-stone-hops: best hop count for each stone from a sliding minimum over the window behind it.
def fewest_hops(stones, lo, hi):
    n = len(stones)
    INF = float('inf')
    dist = [INF] * n
    dist[0] = 0
    window = deque()         # indices with rising dist, all inside [j - hi, j - lo]
    for j in range(1, n):
        new = j - lo
        if new >= 0 and dist[new] < INF:
            while window and dist[window[-1]] >= dist[new]:
                window.pop()
            window.append(new)
        while window and window[0] < j - hi:
            window.popleft()
        if stones[j] == '.' and window:
            dist[j] = dist[window[0]] + 1
    return -1 if dist[n - 1] == INF else dist[n - 1]


# ci-stop-cascade: sorted lists, the ready stops fired in order of arrival.
def solve_stop_cascade(text):
    tok = text.split()
    n = int(tok[0])
    pos = 1
    book = []                # sorted [price, arrival, shares left]
    stops = []               # sorted (price, arrival, shares)
    last = None
    total = 0
    out = []

    def buy(q):
        nonlocal last, total
        taken = 0
        while q and taken < len(book):
            order = book[taken]
            take = min(q, order[2])
            order[2] -= take
            q -= take
            total += take
            last = order[0]
            if order[2] == 0:
                taken += 1
        if taken:
            del book[:taken]

    for arrival in range(n):
        kind = tok[pos]
        if kind == 'S':
            bisect.insort(book, [int(tok[pos + 1]), arrival, int(tok[pos + 2])])
            pos += 3
        elif kind == 'B':
            buy(int(tok[pos + 1]))
            pos += 2
        else:
            bisect.insort(stops, (int(tok[pos + 1]), arrival, int(tok[pos + 2])))
            pos += 3
        while last is not None and stops and stops[0][0] <= last:
            cut = bisect.bisect_right(stops, (last, float('inf'), 0))
            ready = sorted(stops[:cut], key=lambda s: s[1])
            del stops[:cut]
            for _, _, q in ready:
                buy(q)
        out.append('- 0' if last is None else '%d %d' % (last, total))
    return '\n'.join(out)


# ci-switch-panel: every set by its bit mask, the best kept by (size, list).
def fewest_switches(switches, target):
    nums = [int(s, 2) for s in switches]
    want = int(target, 2)
    best = None
    for mask in range(1 << len(nums)):
        x = 0
        picked = []
        for i, v in enumerate(nums):
            if mask >> i & 1:
                x ^= v
                picked.append(i)
        if x == want:
            key = (len(picked), picked)
            if best is None or key < best:
                best = key
    return None if best is None else best[1]


# ci-room-numbers: free rooms in a heap, busy rooms in a heap (two heaps is the only
# quick way I know; the brute force in extra_8.py scans every room).
def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free, busy = [], []
    rooms = 0
    out = [None] * len(meetings)
    for i in order:
        s, e = meetings[i]
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            r = heapq.heappop(free)
        else:
            r = rooms
            rooms += 1
        out[i] = r
        heapq.heappush(busy, (e + clean, r))
    return out
