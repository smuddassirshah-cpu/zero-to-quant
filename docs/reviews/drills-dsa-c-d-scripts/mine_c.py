# Reader's own solutions for sub-pack C, written from the brief only.
import sys, heapq
sys.setrecursionlimit(10000)


def route_order(legs):
    nxt = {s: t for s, t in legs}
    pointed = {t for s, t in legs if t is not None}
    starts = [s for s in nxt if s not in pointed]
    if not starts:
        return []
    out = []
    cur = starts[0]
    while cur is not None:
        out.append(cur)
        cur = nxt[cur]
    return out


def fewest_checks(tree):
    if tree is None:
        return 0
    _, l, r = tree
    if l is None and r is None:
        return 1
    if l is None:
        return 1 + fewest_checks(r)
    if r is None:
        return 1 + fewest_checks(l)
    return 1 + min(fewest_checks(l), fewest_checks(r))


def solve_shared_tail(text):
    v = list(map(int, text.split()))
    n, a, b = v[0], v[1], v[2]
    nx = v[3:3 + n]
    seen = set()
    c = a
    while c != -1:
        seen.add(c)
        c = nx[c]
    c = b
    while c != -1:
        if c in seen:
            return str(c)
        c = nx[c]
    return '-1'


def shared_manager(chart, a, b):
    def go(t):
        if t is None:
            return None
        name, l, r = t
        if name == a or name == b:
            return name
        x, y = go(l), go(r)
        if x is not None and y is not None:
            return name
        return x if x is not None else y
    return go(chart)


def nearest_levels(book, prices):
    out = []
    for q in prices:
        best = None
        t = book
        while t is not None:
            p, l, r = t
            if best is None or abs(p - q) < abs(best - q) or (abs(p - q) == abs(best - q) and p < best):
                best = p
            if q == p:
                break
            t = l if q < p else r
        out.append(best)
    return out


def swapped_levels(book):
    order = []
    st = []
    t = book
    while st or t is not None:
        while t is not None:
            st.append(t)
            t = t[1]
        t = st.pop()
        order.append(t[0])
        t = t[2]
    drops = [i for i in range(len(order) - 1) if order[i] > order[i + 1]]
    if not drops:
        return []
    x = order[drops[0]]
    y = order[drops[-1] + 1]
    return [min(x, y), max(x, y)]


def nearest_strikes(strikes, spot, k):
    return sorted(strikes, key=lambda s: (abs(s - spot), s))[:k]


def short_codes(names):
    cnt = {}
    for w in names:
        for i in range(1, len(w) + 1):
            p = w[:i]
            cnt[p] = cnt.get(p, 0) + 1
    out = []
    for w in names:
        for i in range(1, len(w) + 1):
            if cnt[w[:i]] == 1:
                out.append(w[:i])
                break
        else:
            out.append(w)
    return out


def solve_print_queue(text):
    v = list(map(int, text.split()))
    n = v[0]
    jobs = sorted((v[1 + 3 * i + 1], v[1 + 3 * i + 2], v[1 + 3 * i]) for i in range(n))
    out = []
    h = []
    t = 0
    i = 0
    while i < n or h:
        if not h and jobs[i][0] > t:
            t = jobs[i][0]
        while i < n and jobs[i][0] <= t:
            arr, pg, jid = jobs[i]
            heapq.heappush(h, (pg, arr, jid))
            i += 1
        pg, arr, jid = heapq.heappop(h)
        out.append(str(jid))
        t += pg
    return ' '.join(out)


def tightest_window(feeds):
    k = len(feeds)
    m = sorted((x, f) for f, L in enumerate(feeds) for x in L)
    cnt = [0] * k
    have = 0
    best = None
    left = 0
    for right in range(len(m)):
        f = m[right][1]
        cnt[f] += 1
        if cnt[f] == 1:
            have += 1
        while have == k:
            lo, hi = m[left][0], m[right][0]
            if best is None or hi - lo < best[1] - best[0] or (hi - lo == best[1] - best[0] and lo < best[0]):
                best = [lo, hi]
            g = m[left][1]
            cnt[g] -= 1
            if cnt[g] == 0:
                have -= 1
            left += 1
    return best


def booked_minutes(bookings):
    tot = 0
    cs = ce = None
    for s, e in sorted(bookings):
        if ce is None or s > ce:
            if ce is not None:
                tot += ce - cs
            cs, ce = s, e
        else:
            ce = max(ce, e)
    if ce is not None:
        tot += ce - cs
    return tot


def any_clash(slots):
    s = sorted(slots)
    return any(s[i + 1][0] < s[i][1] for i in range(len(s) - 1)) if s else False


def solve_peak_calls(text):
    v = list(map(int, text.split()))
    n = v[0]
    ev = []
    for i in range(n):
        a, b = v[1 + 2 * i], v[2 + 2 * i]
        ev.append((a, 1))
        ev.append((b, -1))
    ev.sort()  # -1 before +1 at the same time
    cur = best = 0
    at = None
    for t, d in ev:
        cur += d
        if cur > best:
            best, at = cur, t
    return f'{best} {at}'


def fewest_shifts(shifts, close):
    s = sorted(shifts)
    reach = 0
    i = 0
    cnt = 0
    while reach < close:
        far = reach
        while i < len(s) and s[i][0] <= reach:
            far = max(far, s[i][1])
            i += 1
        if far <= reach:
            return -1
        reach = far
        cnt += 1
    return cnt


def shortest_windows(windows, parcels):
    w = sorted(windows)
    qs = sorted(range(len(parcels)), key=lambda i: parcels[i])
    out = [-1] * len(parcels)
    h = []
    j = 0
    for qi in qs:
        t = parcels[qi]
        while j < len(w) and w[j][0] <= t:
            heapq.heappush(h, (w[j][1] - w[j][0], w[j][1]))
            j += 1
        while h and h[0][1] <= t:
            heapq.heappop(h)
        if h:
            out[qi] = h[0][0]
    return out
