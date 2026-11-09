# Reader's own solutions for sub-pack B, written from the brief text only.
from bisect import bisect_left


def plan_filled_in_order(tape, plan):
    j = 0
    for x in tape:
        if j < len(plan) and x == plan[j]:
            j += 1
    return j == len(plan)


def count_pairs_within(prices, budget):
    i, j = 0, len(prices) - 1
    c = 0
    while i < j:
        if prices[i] + prices[j] <= budget:
            c += j - i
            i += 1
        else:
            j -= 1
    return c


def solve_near_trades(text):
    tok = text.split()
    n, d = int(tok[0]), int(tok[1])
    t = [int(x) for x in tok[2:2 + n]]
    c = 0
    i = 0
    for j in range(n):
        while t[j] - t[i] > d:
            i += 1
        c += j - i
    return str(c)


def closest_pair_gap(sizes, target):
    s = sorted(sizes)
    i, j = 0, len(s) - 1
    best = None
    while i < j:
        v = s[i] + s[j] - target
        if best is None or abs(v) < best:
            best = abs(v)
        if v < 0:
            i += 1
        elif v > 0:
            j -= 1
        else:
            return 0
    return best


def solve_sensor_alarm(text):
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    if k > n:
        return '0'
    s = sum(r[:k])
    c = 1 if s >= t * k else 0
    for i in range(k, n):
        s += r[i] - r[i - k]
        if s >= t * k:
            c += 1
    return str(c)


def count_varied_windows(badges, k):
    n = len(badges)
    if k > n:
        return 0
    cnt = {}
    dup = 0  # number of badges with count >= 2 in window
    res = 0
    for i, b in enumerate(badges):
        cnt[b] = cnt.get(b, 0) + 1
        if cnt[b] == 2:
            dup += 1
        if i >= k:
            o = badges[i - k]
            cnt[o] -= 1
            if cnt[o] == 1:
                dup -= 1
        if i >= k - 1 and dup == 0:
            res += 1
    return res


def longest_stretch_within(fees, budget):
    lo = 0
    s = 0
    best = 0
    for hi, f in enumerate(fees):
        s += f
        while s > budget:
            s -= fees[lo]
            lo += 1
        best = max(best, hi - lo + 1)
    return best


def longest_without_repeat(rota):
    last = {}
    lo = 0
    best = 0
    for i, x in enumerate(rota):
        if x in last and last[x] >= lo:
            lo = last[x] + 1
        last[x] = i
        best = max(best, i - lo + 1)
    return best


def bracket_partners(formula):
    st = []
    out = []
    for i, ch in enumerate(formula):
        if ch in '([{':
            st.append(i)
        elif ch in ')]}':
            out.append((st.pop(), i))
    out.sort()
    return out


def net_tape(orders):
    st = []
    for o in orders:
        if o > 0:
            st.append(o)
        else:
            s = -o
            while s and st and st[-1] > 0:
                if st[-1] > s:
                    st[-1] -= s
                    s = 0
                else:
                    s -= st.pop()
            if s:
                st.append(-s)
    return st


def solve_ticket_desk(text):
    tok = text.split()
    if not tok:
        return '0 0 0'
    n = int(tok[0])
    arr = [int(tok[1 + 2 * i]) for i in range(n)]
    svc = [int(tok[2 + 2 * i]) for i in range(n)]
    free = 0
    wait = 0
    starts = []
    for a, s in zip(arr, svc):
        st = max(a, free)
        wait += st - a
        starts.append(st)
        free = st + s
    # queue at arrival minute m: arrived <= m minus started <= m
    best = 0
    j = 0  # starts <= m
    i = 0
    while i < n:
        m = arr[i]
        while i < n and arr[i] == m:
            i += 1
        while j < n and starts[j] <= m:
            j += 1
        best = max(best, i - j)
    return f'{wait} {free} {best}'


def largest_depth_block(depth):
    st = []
    best = 0
    h = depth + [-1]
    for i, x in enumerate(h):
        start = i
        while st and st[-1][1] >= x:
            p, v = st.pop()
            best = max(best, v * (i - p))
            start = p
        st.append((start, x))
    return best


def missing_seq_number(seqs):
    lo, hi = 0, len(seqs) - 1  # seqs[lo] ok, seqs[hi] too high
    a = seqs[0]
    while hi - lo > 1:
        m = (lo + hi) // 2
        if seqs[m] == a + m:
            lo = m
        else:
            hi = m
    return a + hi


def peak_index(path):
    lo, hi = 0, len(path) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if path[m] < path[m + 1]:
            lo = m + 1
        else:
            hi = m
    return lo


def widest_spacing(sites, k):
    s = sorted(sites)

    def ok(g):
        c = 1
        last = s[0]
        for x in s[1:]:
            if x - last >= g:
                c += 1
                last = x
                if c >= k:
                    return True
        return c >= k

    lo, hi = 0, s[-1] - s[0]
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo
