# Reader's own solutions for sub-pack D, written from the brief only.
import sys
from collections import deque
from functools import lru_cache
sys.setrecursionlimit(10000)


def solve_lift_buttons(text):
    n, s, g, u, d = map(int, text.split())
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    while q:
        x = q.popleft()
        if x == g:
            break
        for y in (x + u, x - d):
            if 1 <= y <= n and dist[y] < 0:
                dist[y] = dist[x] + 1
                q.append(y)
    return str(dist[g])


def spare_cable_moves(n, cables):
    if len(cables) < n - 1:
        return -1
    p = list(range(n))
    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    comp = n
    for a, b in cables:
        ra, rb = f(a), f(b)
        if ra != rb:
            p[ra] = rb
            comp -= 1
    return comp - 1


def fewest_climb_steps(heights, climb):
    R, C = len(heights), len(heights[0])
    dist = [[-1] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for rr, cc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= rr < R and 0 <= cc < C and dist[rr][cc] < 0 and heights[rr][cc] - heights[r][c] <= climb:
                dist[rr][cc] = dist[r][c] + 1
                q.append((rr, cc))
    return dist[R - 1][C - 1]


def upstream_stations(n, pipes, r):
    rev = [[] for _ in range(n)]
    for a, b in pipes:
        rev[b].append(a)
    seen = [False] * n
    seen[r] = True
    st = [r]
    while st:
        x = st.pop()
        for y in rev[x]:
            if not seen[y]:
                seen[y] = True
                st.append(y)
    return [i for i in range(n) if seen[i] and i != r]


def forced_order(n, deps):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:
        adj[a].append(b)
        indeg[b] += 1
    ready = [i for i in range(n) if indeg[i] == 0]
    out = []
    while ready:
        if len(ready) > 1:
            return None
        x = ready.pop()
        out.append(x)
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                ready.append(y)
    return out if len(out) == n else None


def footpath_ways(n):
    M = 1_000_000_007
    a, b = 1, 1  # f(0), f(1)
    if n == 0:
        return 1
    for _ in range(n - 1):
        a, b = b, (b + 2 * a) % M
    return b


def unpayable_totals(stamps, limit):
    ok = bytearray(limit + 1)
    ok[0] = 1
    vals = sorted(set(stamps))
    for t in range(1, limit + 1):
        for s in vals:
            if s > t:
                break
            if ok[t - s]:
                ok[t] = 1
                break
    return limit - sum(ok[1:])


def solve_shift_pay(text):
    v = list(map(int, text.split()))
    n = v[0]
    pay = v[1:1 + n]
    # a: best ending with rest, b: ending with one worked day, c: ending with two
    a = b = c = 0
    b = c = float('-inf')
    for p in pay:
        a, b, c = max(a, b, c), a + p, b + p
    return str(max(a, b, c))


def solve_feed_passes(text):
    v = list(map(int, text.split()))
    n, p1, p7, p30 = v[0], v[1], v[2], v[3]
    days = v[4:4 + n]
    import bisect
    best = [0] * (n + 1)  # best[i]: cost to cover days[i:]
    for i in range(n - 1, -1, -1):
        d = days[i]
        j7 = bisect.bisect_left(days, d + 7, i)
        j30 = bisect.bisect_left(days, d + 30, i)
        best[i] = min(p1 + best[i + 1], p7 + best[j7], p30 + best[j30])
    return str(best[0])


def largest_free_square(plan):
    R, C = len(plan), len(plan[0])
    prev = [0] * (C + 1)
    best = 0
    for r in range(R):
        cur = [0] * (C + 1)
        row = plan[r]
        for c in range(C):
            if row[c] == '.':
                cur[c + 1] = 1 + min(prev[c], prev[c + 1], cur[c])
                if cur[c + 1] > best:
                    best = cur[c + 1]
        prev = cur
    return best


def first_short_change(notes):
    f = t = 0
    for i, x in enumerate(notes):
        if x == 5:
            f += 1
        elif x == 10:
            if f == 0:
                return i
            f -= 1
            t += 1
        else:
            if t and f:
                t -= 1
                f -= 1
            elif f >= 3:
                f -= 3
            else:
                return i
    return -1


def loop_start_depot(fuel, burn):
    n = len(fuel)
    if sum(fuel) < sum(burn):
        return -1
    # start s works iff prefix P_s is the minimum of P_0..P_{n-1}
    P = 0
    best = 0
    bests = 0
    for i in range(n):
        if P < best:
            best, bests = P, i
        P += fuel[i] - burn[i]
    return bests


def ticker_batches(tape):
    last = {c: i for i, c in enumerate(tape)}
    out = []
    start = end = 0
    for i, c in enumerate(tape):
        end = max(end, last[c])
        if i == end:
            out.append(i - start + 1)
            start = i + 1
    return out


def split_prices(digits, k, cap):
    L = len(digits)
    w = len(str(cap))
    out = []
    cur = []
    def go(i, left):
        if left == 0:
            if i == L:
                out.append(cur[:])
            return
        rem = L - i
        if rem < left or rem > left * w:
            return
        if digits[i] == '0':
            return
        for j in range(i + 1, min(L, i + w) + 1):
            v = int(digits[i:j])
            if v > cap:
                break
            cur.append(v)
            go(j, left - 1)
            cur.pop()
    go(0, k)
    return sorted(out)


def min_peak_load(jobs, k):
    n = len(jobs)
    if n == 0:
        return 0
    def need(T):
        INF = (99, 0)
        dp = [INF] * (1 << n)
        dp[0] = (1, 0)
        for m in range(1 << n):
            b, f = dp[m]
            if b == 99:
                continue
            for j in range(n):
                if not m >> j & 1:
                    x = jobs[j]
                    if f + x <= T:
                        c = (b, f + x)
                    else:
                        c = (b + 1, x)
                    mm = m | 1 << j
                    if c < dp[mm]:
                        dp[mm] = c
        return dp[-1][0]
    lo, hi = max(jobs), sum(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
