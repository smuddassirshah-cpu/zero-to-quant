# Reader's own solutions for sub-pack A, written from the brief text only.

def majority_reading(readings):
    c = {}
    for r in readings:
        c[r] = c.get(r, 0) + 1
    n = len(readings)
    for r, v in c.items():
        if v * 2 > n:
            return r
    return None


def silent_sensors(expected, reported):
    seen = set(reported)
    return [e for e in expected if e not in seen]


def solve_kth_repeat(text):
    tok = text.split()
    if not tok:
        return 'NONE'
    n, k = int(tok[0]), int(tok[1])
    ids = tok[2:2 + n]
    c = {}
    for x in ids:
        c[x] = c.get(x, 0) + 1
        if c[x] == k:
            return x
    return 'NONE'


def traders_by_ticker(trades):
    out = {}
    seen = set()
    for tr, tk in trades:
        if (tr, tk) in seen:
            continue
        seen.add((tr, tk))
        out.setdefault(tk, []).append(tr)
    return out


def largest_shape_group(traces):
    c = {}
    best = 0
    for t in traces:
        key = tuple(x - t[0] for x in t)
        c[key] = c.get(key, 0) + 1
        best = max(best, c[key])
    return best


def first_overdrawn_day(opening, flows):
    b = opening
    for i, f in enumerate(flows):
        b += f
        if b < 0:
            return i
    return -1


def solve_range_volumes(text):
    tok = text.split()
    n, q = int(tok[0]), int(tok[1])
    v = tok[2:2 + n]
    p = [0]
    for x in v:
        p.append(p[-1] + int(x))
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(tok[pos]), int(tok[pos + 1])
        pos += 2
        out.append(str(p[r] - p[l - 1]))
    return '\n'.join(out)


def staff_per_hour(hours, shifts):
    d = [0] * (hours + 1)
    for s, e in shifts:
        d[s] += 1
        d[e + 1] -= 1
    out = []
    run = 0
    for h in range(hours):
        run += d[h]
        out.append(run)
    return out


def flattest_stretch(pnl):
    p = [0]
    for x in pnl:
        p.append(p[-1] + x)
    p.sort()
    return min(p[i + 1] - p[i] for i in range(len(p) - 1))


def longest_winning_stretch(pnl):
    first = {0: -1}
    s = 0
    best = 0
    for i, x in enumerate(pnl):
        s += 1 if x > 0 else -1
        if s > 0:
            best = i + 1
        elif s - 1 in first:
            best = max(best, i - first[s - 1])
        if s not in first:
            first[s] = i
    return best


def push_empty_to_back(qty):
    w = 0
    for x in qty:
        if x != 0:
            qty[w] = x
            w += 1
    for i in range(w, len(qty)):
        qty[i] = 0
    return qty


def trailing_stop_exit(prices, gap):
    if not prices:
        return -1
    hi = prices[0]
    for i in range(1, len(prices)):
        if prices[i] <= hi - gap:
            return i
        hi = max(hi, prices[i])
    return -1


def solve_stock_ledger(text):
    tok = text.split()
    if not tok:
        return '0'
    n = int(tok[0])
    stock = {}
    refused = 0
    pos = 1
    for _ in range(n):
        op, item, k = tok[pos], tok[pos + 1], int(tok[pos + 2])
        pos += 3
        if op == 'IN':
            stock[item] = stock.get(item, 0) + k
        elif stock.get(item, 0) < k:
            refused += 1
        else:
            stock[item] -= k
    lines = [str(refused)] + [f'{i} {c}' for i, c in sorted(stock.items()) if c > 0]
    return '\n'.join(lines)


def rotate_rota(staff, k):
    n = len(staff)
    if n == 0:
        return staff
    k %= n
    staff[:] = staff[n - k:] + staff[:n - k]
    return staff


def position_after(route, steps):
    d = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    full, rem = divmod(steps, len(route))
    px = sum(d[c][0] for c in route)
    py = sum(d[c][1] for c in route)
    x, y = px * full, py * full
    for ch in route[:rem]:
        x += d[ch][0]
        y += d[ch][1]
    return [x, y]
