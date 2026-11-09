# Planted wrong solutions, sub-pack A, variant 2: ties, duplicates and order mishandled.

def majority_reading(readings):  # Boyer-Moore with no second pass
    cand, cnt = None, 0
    for r in readings:
        if cnt == 0:
            cand = r
        cnt += 1 if r == cand else -1
    return cand


def silent_sensors(expected, reported):  # set difference, sorted
    return sorted(set(expected) - set(reported))


def solve_kth_repeat(text):  # first id (by first appearance) with k messages anywhere
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    ids = tok[2:2 + n]
    c = {}
    for x in ids:
        c[x] = c.get(x, 0) + 1
    for x in ids:
        if c[x] >= k:
            return x
    return 'NONE'


def traders_by_ticker(trades):  # dedupe but sorted names
    out = {}
    for tr, tk in trades:
        out.setdefault(tk, set()).add(tr)
    return {k: sorted(v) for k, v in out.items()}


def largest_shape_group(traces):  # sorted after normalising, so order is lost
    c = {}
    for t in traces:
        m = min(t)
        key = tuple(sorted(x - m for x in t))
        c[key] = c.get(key, 0) + 1
    return max(c.values(), default=0)


def first_overdrawn_day(opening, flows):  # ignores the opening balance
    b = 0
    for i, f in enumerate(flows):
        b += f
        if b < 0:
            return i
    return -1


def solve_range_volumes(text):  # trailing newline kept
    tok = text.split()
    n, q = int(tok[0]), int(tok[1])
    p = [0]
    for x in tok[2:2 + n]:
        p.append(p[-1] + int(x))
    out = ''
    pos = 2 + n
    for _ in range(q):
        l, r = int(tok[pos]), int(tok[pos + 1])
        pos += 2
        out += str(p[r] - p[l - 1]) + '\n'
    return out


def staff_per_hour(hours, shifts):  # duplicate shifts counted once
    d = [0] * (hours + 1)
    for s, e in set(shifts):
        d[s] += 1
        d[e + 1] -= 1
    out, run = [], 0
    for h in range(hours):
        run += d[h]
        out.append(run)
    return out


def flattest_stretch(pnl):  # best single day or whole run only
    return min(min(abs(x) for x in pnl), abs(sum(pnl)))


def longest_winning_stretch(pnl):  # equal counts allowed
    first = {0: -1}
    s = best = 0
    for i, x in enumerate(pnl):
        s += 1 if x > 0 else -1
        if s >= 0:
            best = i + 1
        elif s in first:
            best = max(best, i - first[s])
        first.setdefault(s, i)
    return best


def push_empty_to_back(qty):  # in place but drops negatives' order (sort descending)
    qty.sort(key=lambda x: (x == 0, -x))
    return qty


def trailing_stop_exit(prices, gap):  # stop measured from the buy price only
    for i in range(1, len(prices)):
        if prices[i] <= prices[0] - gap:
            return i
    return -1


def solve_stock_ledger(text):  # lists items with zero stock
    tok = text.split()
    n = int(tok[0])
    st, ref, pos = {}, 0, 1
    for _ in range(n):
        op, it, k = tok[pos], tok[pos + 1], int(tok[pos + 2])
        pos += 3
        if op == 'IN':
            st[it] = st.get(it, 0) + k
        elif st.get(it, 0) < k:
            ref += 1
        else:
            st[it] -= k
    return '\n'.join([str(ref)] + [f'{a} {b}' for a, b in sorted(st.items())])


def rotate_rota(staff, k):  # no reduction of k modulo n
    if staff:
        k = min(k, len(staff))
        staff[:] = staff[len(staff) - k:] + staff[:len(staff) - k]
    return staff


def position_after(route, steps):  # counts only full passes
    d = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    full = steps // len(route)
    return [sum(d[c][0] for c in route) * full, sum(d[c][1] for c in route) * full]
