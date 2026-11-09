# Planted wrong solutions, sub-pack A, variant 3: the slow method named in each brief.

def majority_reading(readings):
    for r in readings:
        if 2 * readings.count(r) > len(readings):
            return r
    return None


def silent_sensors(expected, reported):
    return [e for e in expected if e not in reported]


def solve_kth_repeat(text):
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    ids = tok[2:2 + n]
    for i, x in enumerate(ids):
        if ids[:i + 1].count(x) == k:
            return x
    return 'NONE'


def traders_by_ticker(trades):
    out = {}
    for tr, tk in trades:
        lst = out.setdefault(tk, [])
        if tr not in lst:
            lst.append(tr)
    return out


def largest_shape_group(traces):
    best = 0
    for a in traces:
        c = 0
        for b in traces:
            if len(a) == len(b) and all(x - a[0] == y - b[0] for x, y in zip(a, b)):
                c += 1
        best = max(best, c)
    return best


def first_overdrawn_day(opening, flows):
    for i in range(len(flows)):
        if opening + sum(flows[:i + 1]) < 0:
            return i
    return -1


def solve_range_volumes(text):
    tok = text.split()
    n, q = int(tok[0]), int(tok[1])
    v = [int(x) for x in tok[2:2 + n]]
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(tok[pos]), int(tok[pos + 1])
        pos += 2
        out.append(str(sum(v[l - 1:r])))
    return '\n'.join(out)


def staff_per_hour(hours, shifts):
    c = [0] * hours
    for s, e in shifts:
        for h in range(s, e + 1):
            c[h] += 1
    return c


def flattest_stretch(pnl):
    best = None
    for i in range(len(pnl)):
        s = 0
        for j in range(i, len(pnl)):
            s += pnl[j]
            if best is None or abs(s) < best:
                best = abs(s)
    return best


def longest_winning_stretch(pnl):
    best = 0
    for i in range(len(pnl)):
        s = 0
        for j in range(i, len(pnl)):
            s += 1 if pnl[j] > 0 else -1
            if s > 0:
                best = max(best, j - i + 1)
    return best


def push_empty_to_back(qty):
    z = qty.count(0)
    for _ in range(z):
        qty.remove(0)
    qty.extend([0] * z)
    return qty


def trailing_stop_exit(prices, gap):
    for i in range(1, len(prices)):
        if prices[i] <= max(prices[:i]) - gap:
            return i
    return -1


def solve_stock_ledger(text):
    tok = text.split()
    n = int(tok[0])
    items, counts, ref, pos = [], [], 0, 1
    for _ in range(n):
        op, it, k = tok[pos], tok[pos + 1], int(tok[pos + 2])
        pos += 3
        if it in items:
            j = items.index(it)
        else:
            items.append(it)
            counts.append(0)
            j = len(items) - 1
        if op == 'IN':
            counts[j] += k
        elif counts[j] < k:
            ref += 1
        else:
            counts[j] -= k
    return '\n'.join([str(ref)] + [f'{a} {b}' for a, b in sorted(zip(items, counts)) if b > 0])


def rotate_rota(staff, k):
    if staff:
        for _ in range(k % len(staff)):
            staff.insert(0, staff.pop())
    return staff


def position_after(route, steps):
    d = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    x = y = 0
    for i in range(steps):
        dx, dy = d[route[i % len(route)]]
        x += dx
        y += dy
    return [x, y]
