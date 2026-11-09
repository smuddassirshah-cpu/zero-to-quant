# Planted wrong solutions, sub-pack B, variant 2: ties and duplicates mishandled.


def plan_filled_in_order(tape, plan):  # tape.index from last match, but reuses one position
    pos = 0
    for p in plan:
        try:
            pos = tape.index(p, pos)
        except ValueError:
            return False
    return True


def count_pairs_within(prices, budget):  # distinct prices only
    s = sorted(set(prices))
    i, j, c = 0, len(s) - 1, 0
    while i < j:
        if s[i] + s[j] <= budget:
            c += j - i
            i += 1
        else:
            j -= 1
    return c


def solve_near_trades(text):  # equal times not counted
    tok = text.split()
    n, d = int(tok[0]), int(tok[1])
    t = [int(x) for x in tok[2:2 + n]]
    c = i = 0
    for j in range(n):
        while t[j] - t[i] > d:
            i += 1
        c += sum(1 for x in range(i, j) if t[x] != t[j]) if j - i < 50 else j - i
    return str(c)


def closest_pair_gap(sizes, target):  # dedupes sizes
    s = sorted(set(sizes))
    if len(s) < 2:
        return abs(2 * s[0] - target) if len(sizes) >= 2 else None
    i, j, best = 0, len(s) - 1, None
    while i < j:
        v = s[i] + s[j] - target
        best = abs(v) if best is None else min(best, abs(v))
        if v < 0:
            i += 1
        else:
            j -= 1
    return best


def solve_sensor_alarm(text):  # integer floor of the average
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    if k > n:
        return '0'
    s = sum(r[:k])
    c = int(s // k >= t)
    for i in range(k, n):
        s += r[i] - r[i - k]
        c += s // k >= t
    return str(c)


def count_varied_windows(badges, k):  # counts windows whose first and last differ
    n = len(badges)
    if k > n:
        return 0
    if k == 1:
        return n
    return sum(1 for i in range(n - k + 1) if badges[i] != badges[i + k - 1])


def longest_stretch_within(fees, budget):  # stops growing on a free hour
    lo = s = best = 0
    for hi, f in enumerate(fees):
        if f == 0 and s == 0:
            lo = hi + 1
            continue
        s += f
        while s > budget:
            s -= fees[lo]
            lo += 1
        best = max(best, hi - lo + 1)
    return best


def longest_without_repeat(rota):  # restarts the window after any repeat
    seen, best, cur = set(), 0, 0
    for x in rota:
        if x in seen:
            seen = {x}
            cur = 1
        else:
            seen.add(x)
            cur += 1
        best = max(best, cur)
    return best


def bracket_partners(formula):  # ignores bracket kind by pairing round only
    st, out = [], []
    for i, ch in enumerate(formula):
        if ch == '(':
            st.append(i)
        elif ch == ')':
            out.append((st.pop(), i))
    return sorted(out)


def net_tape(orders):  # merges resting sells into one
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
                if st and st[-1] < 0:
                    st[-1] -= s
                else:
                    st.append(-s)
    return st


def solve_ticket_desk(text):  # queue measured just before each arrival
    tok = text.split()
    if not tok:
        return '0 0 0'
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
    j = 0
    for i, m in enumerate(arr):
        while j < n and starts[j] <= m:
            j += 1
        best = max(best, i - j)
    return f'{wait} {free} {best}'


def largest_depth_block(depth):  # only strictly larger neighbours extend
    best = 0
    st = []
    for i, x in enumerate(depth + [-1]):
        start = i
        while st and st[-1][1] > x:
            p, v = st.pop()
            best = max(best, v * (i - p))
            start = p
        st.append((start, x))
    return best


def missing_seq_number(seqs):  # midpoint of first and last
    return (seqs[0] + seqs[-1]) // 2


def peak_index(path):  # ties at the top resolved left; uses <= so plateau assumption
    lo, hi = 0, len(path) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if path[m] <= path[m + 1]:
            lo = m + 1
        else:
            hi = m
    return lo


def widest_spacing(sites, k):  # forgets to sort
    s = list(sites)

    def ok(g):
        c, last = 1, s[0]
        for x in s[1:]:
            if x - last >= g:
                c += 1
                last = x
        return c >= k

    lo, hi = 0, max(s) - min(s)
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ok(m):
            lo = m
        else:
            hi = m - 1
    return lo
