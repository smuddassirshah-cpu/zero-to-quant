# Planted wrong solutions, sub-pack B, variant 3: the slow method named in each brief
# (plus a few cheap C-level shortcuts a learner might reach for).


def plan_filled_in_order(tape, plan):
    pos = 0
    for p in plan:
        found = False
        for i in range(0, len(tape)):  # searches from the start each time
            if i >= pos and tape[i] == p:
                pos = i + 1
                found = True
                break
        if not found:
            return False
    return True


def count_pairs_within(prices, budget):
    n = len(prices)
    return sum(1 for i in range(n) for j in range(i + 1, n) if prices[i] + prices[j] <= budget)


def solve_near_trades(text):
    tok = text.split()
    n, d = int(tok[0]), int(tok[1])
    t = [int(x) for x in tok[2:2 + n]]
    return str(sum(1 for i in range(n) for j in range(i + 1, n) if t[j] - t[i] <= d))


def closest_pair_gap(sizes, target):
    n = len(sizes)
    return min(abs(sizes[i] + sizes[j] - target) for i in range(n) for j in range(i + 1, n))


def solve_sensor_alarm(text):
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    return str(sum(1 for i in range(n - k + 1) if sum(r[i:i + k]) >= t * k))


def count_varied_windows(badges, k):
    return sum(1 for i in range(len(badges) - k + 1) if len(set(badges[i:i + k])) == k)


def longest_stretch_within(fees, budget):
    best = 0
    for i in range(len(fees)):
        s = 0
        for j in range(i, len(fees)):
            s += fees[j]
            if s > budget:
                break
            best = max(best, j - i + 1)
    return best


def longest_without_repeat(rota):
    best = 0
    for i in range(len(rota)):
        seen = set()
        for j in range(i, len(rota)):
            if rota[j] in seen:
                break
            seen.add(rota[j])
        best = max(best, len(seen))
    return best


def bracket_partners(formula):
    pair = {')': '(', ']': '[', '}': '{'}
    used = set()
    out = []
    for i, ch in enumerate(formula):
        if ch in pair:
            j = i - 1
            depth = 0
            while True:
                c = formula[j]
                if c in pair:
                    depth += 1
                elif c in '([{':
                    if depth == 0:
                        break
                    depth -= 1
                j -= 1
            out.append((j, i))
    return sorted(out)


def net_tape(orders):
    rest = []
    for o in orders:
        if o > 0:
            rest = rest + [o]
        else:
            s = -o
            while s and rest and rest[-1] > 0:
                if rest[-1] > s:
                    rest = rest[:-1] + [rest[-1] - s]
                    s = 0
                else:
                    s -= rest[-1]
                    rest = rest[:-1]
            if s:
                rest = rest + [-s]
    return rest


def solve_ticket_desk(text):
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
    for m in arr:
        best = max(best, sum(1 for a, s in zip(arr, starts) if a <= m < s))
    return f'{wait} {free} {best}'


def largest_depth_block(depth):
    best = 0
    for i in range(len(depth)):
        m = depth[i]
        for j in range(i, len(depth)):
            m = min(m, depth[j])
            best = max(best, m * (j - i + 1))
    return best


def missing_seq_number(seqs):  # C-level sum shortcut, O(n) per call
    n = len(seqs) + 1
    return (seqs[0] + seqs[-1]) * n // 2 - sum(seqs)


def peak_index(path):  # C-level max, O(n) per call
    return path.index(max(path))


def widest_spacing(sites, k):  # tries every gap from the top down
    s = sorted(sites)

    def ok(g):
        c, last = 1, s[0]
        for x in s[1:]:
            if x - last >= g:
                c += 1
                last = x
        return c >= k

    g = (s[-1] - s[0]) // (k - 1)
    while not ok(g):
        g -= 1
    return g
