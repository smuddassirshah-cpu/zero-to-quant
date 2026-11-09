# Planted wrong solutions, sub-pack B, variant 1: off by one or boundary slips.
from bisect import bisect_right


def plan_filled_in_order(tape, plan):  # membership only, order ignored
    s = set(tape)
    return all(p in s for p in plan)


def count_pairs_within(prices, budget):  # strict < budget
    i, j, c = 0, len(prices) - 1, 0
    while i < j:
        if prices[i] + prices[j] < budget:
            c += j - i
            i += 1
        else:
            j -= 1
    return c


def solve_near_trades(text):  # strict < d
    tok = text.split()
    n, d = int(tok[0]), int(tok[1])
    t = [int(x) for x in tok[2:2 + n]]
    c = i = 0
    for j in range(n):
        while t[j] - t[i] >= d and i < j:
            i += 1
        c += j - i
    return str(c)


def closest_pair_gap(sizes, target):  # allows i == j
    s = sorted(sizes)
    i, j, best = 0, len(s) - 1, None
    while i <= j:
        v = s[i] + s[j] - target
        best = abs(v) if best is None else min(best, abs(v))
        if v < 0:
            i += 1
        else:
            j -= 1
    return best


def solve_sensor_alarm(text):  # strictly above the bar
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    if k > n:
        return '0'
    s = sum(r[:k])
    c = int(s > t * k)
    for i in range(k, n):
        s += r[i] - r[i - k]
        c += s > t * k
    return str(c)


def count_varied_windows(badges, k):  # misses the last window
    n = len(badges)
    c = 0
    for i in range(0, n - k):
        if len(set(badges[i:i + k])) == k:
            c += 1
    return c


def longest_stretch_within(fees, budget):  # strict < budget
    lo = s = best = 0
    for hi, f in enumerate(fees):
        s += f
        while s >= budget and lo <= hi:
            s -= fees[lo]
            lo += 1
        best = max(best, hi - lo + 1)
    return best


def longest_without_repeat(rota):  # does not check last index is inside window
    last, lo, best = {}, 0, 0
    for i, x in enumerate(rota):
        if x in last:
            lo = last[x] + 1
        last[x] = i
        best = max(best, i - lo + 1)
    return best


def bracket_partners(formula):  # sorted by closing index (no sort)
    st, out = [], []
    for i, ch in enumerate(formula):
        if ch in '([{':
            st.append(i)
        elif ch in ')]}':
            out.append((st.pop(), i))
    return out


def net_tape(orders):  # sells net against the oldest buy (queue)
    from collections import deque
    q = deque()
    neg = []
    for o in orders:
        if o > 0:
            q.append(o)
        else:
            s = -o
            while s and q:
                if q[0] > s:
                    q[0] -= s
                    s = 0
                else:
                    s -= q.popleft()
            if s:
                neg.append(-s)
                q.clear()
    return neg + list(q)


def solve_ticket_desk(text):  # queue counts a ticket starting at m
    tok = text.split()
    n = int(tok[0])
    arr = [int(tok[1 + 2 * i]) for i in range(n)]
    svc = [int(tok[2 + 2 * i]) for i in range(n)]
    free = wait = 0
    starts = []
    for a, s in zip(arr, svc):
        st = max(a, free)
        wait += st - a
        starts.append(st)
        free = st + s
    best = 0
    for m in set(arr):
        best = max(best, sum(1 for a, s in zip(arr, starts) if a <= m and s >= m))
    return f'{wait} {free} {best}'


def largest_depth_block(depth):  # forgets to flush the stack at the end
    st, best = [], 0
    for i, x in enumerate(depth):
        start = i
        while st and st[-1][1] >= x:
            p, v = st.pop()
            best = max(best, v * (i - p))
            start = p
        st.append((start, x))
    return best


def missing_seq_number(seqs):  # returns the first too-high value
    lo, hi = 0, len(seqs) - 1
    a = seqs[0]
    while hi - lo > 1:
        m = (lo + hi) // 2
        if seqs[m] == a + m:
            lo = m
        else:
            hi = m
    return seqs[hi]


def peak_index(path):  # compares with left neighbour, off by one
    lo, hi = 0, len(path) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if m > 0 and path[m] > path[m - 1]:
            lo = m + 1
        else:
            hi = m
    return lo


def widest_spacing(sites, k):  # gap counted as > g
    s = sorted(sites)

    def ok(g):
        c, last = 1, s[0]
        for x in s[1:]:
            if x - last > g:
                c += 1
                last = x
        return c >= k

    lo, hi = 0, s[-1] - s[0]
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo
