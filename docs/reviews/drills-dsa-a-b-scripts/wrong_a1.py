# Planted wrong solutions, sub-pack A, variant 1: off by one or boundary slips.

def majority_reading(readings):  # half counts as majority
    c = {}
    for r in readings:
        c[r] = c.get(r, 0) + 1
    for r, v in c.items():
        if 2 * v >= len(readings):
            return r
    return None


def silent_sensors(expected, reported):  # case-insensitive match
    seen = {x.lower() for x in reported}
    return [e for e in expected if e.lower() not in seen]


def solve_kth_repeat(text):  # flags at count > k
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    c = {}
    for x in tok[2:2 + n]:
        c[x] = c.get(x, 0) + 1
        if c[x] > k:
            return x
    return 'NONE'


def traders_by_ticker(trades):  # keeps duplicates
    out = {}
    for tr, tk in trades:
        out.setdefault(tk, []).append(tr)
    return out


def largest_shape_group(traces):  # key ignores the first reading's offset but drops length
    c = {}
    for t in traces:
        key = (t[-1] - t[0],)
        c[key] = c.get(key, 0) + 1
    return max(c.values(), default=0)


def first_overdrawn_day(opening, flows):  # zero counts as overdrawn
    b = opening
    for i, f in enumerate(flows):
        b += f
        if b <= 0:
            return i
    return -1


def solve_range_volumes(text):  # shifted prefix index
    tok = text.split()
    n, q = int(tok[0]), int(tok[1])
    p = [0]
    for x in tok[2:2 + n]:
        p.append(p[-1] + int(x))
    p.append(p[-1])
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(tok[pos]), int(tok[pos + 1])
        pos += 2
        out.append(str(p[r + 1] - p[l]))
    return '\n'.join(out)


def staff_per_hour(hours, shifts):  # end treated as exclusive
    d = [0] * (hours + 1)
    for s, e in shifts:
        d[s] += 1
        d[e] -= 1
    out, run = [], 0
    for h in range(hours):
        run += d[h]
        out.append(run)
    return out


def flattest_stretch(pnl):  # forgets the empty prefix 0
    p = []
    s = 0
    for x in pnl:
        s += x
        p.append(s)
    p.sort()
    best = abs(p[0])
    for i in range(len(p) - 1):
        best = min(best, p[i + 1] - p[i])
    return best


def longest_winning_stretch(pnl):  # zero counts as a win
    first = {0: -1}
    s = best = 0
    for i, x in enumerate(pnl):
        s += 1 if x >= 0 else -1
        if s > 0:
            best = i + 1
        elif s - 1 in first:
            best = max(best, i - first[s - 1])
        first.setdefault(s, i)
    return best


def push_empty_to_back(qty):  # returns a new list
    return [x for x in qty if x != 0] + [0] * qty.count(0)


def trailing_stop_exit(prices, gap):  # strictly below
    if not prices:
        return -1
    hi = prices[0]
    for i in range(1, len(prices)):
        if prices[i] < hi - gap:
            return i
        hi = max(hi, prices[i])
    return -1


def solve_stock_ledger(text):  # partial fill instead of refusal
    tok = text.split()
    n = int(tok[0])
    st, ref, pos = {}, 0, 1
    for _ in range(n):
        op, it, k = tok[pos], tok[pos + 1], int(tok[pos + 2])
        pos += 3
        if op == 'IN':
            st[it] = st.get(it, 0) + k
        else:
            if st.get(it, 0) < k:
                ref += 1
            st[it] = max(0, st.get(it, 0) - k)
    return '\n'.join([str(ref)] + [f'{a} {b}' for a, b in sorted(st.items()) if b > 0])


def rotate_rota(staff, k):  # rotates left
    n = len(staff)
    if n:
        k %= n
        staff[:] = staff[k:] + staff[:k]
    return staff


def position_after(route, steps):  # remainder off by one
    d = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    full, rem = divmod(steps, len(route))
    px = sum(d[c][0] for c in route)
    py = sum(d[c][1] for c in route)
    x, y = px * full, py * full
    for ch in route[:max(rem - 1, 0)]:
        x += d[ch][0]
        y += d[ch][1]
    return [x, y]
