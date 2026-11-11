"""My own solutions to the 15 drills of pack 6, written from the brief,
constraints, hint and examples before reading any model solution.
harness.py runs them on every example and hidden test."""
from bisect import bisect_left, bisect_right

MOD = 1_000_000_007


def ways_up(n, broken):
    bad = set(broken)
    a, b, c = 0, 0, 1  # counts at i-3, i-2, i-1
    for i in range(1, n + 1):
        cur = 0 if i in bad else (a + b + c) % MOD
        a, b, c = b, c, cur
    return c


def best_session(pnl):
    # prefix sums: the best run ending at j starts after the earliest lowest prefix
    best = None
    low, low_at = 0, 0
    pre = 0
    for j, x in enumerate(pnl):
        pre += x
        tot = pre - low
        if best is None or tot > best[0]:
            best = [tot, low_at, j]
        if pre < low:
            low, low_at = pre, j + 1
    return best


def best_shifts(pay):
    skip = (0, 0)   # best with the current day free
    take = (0, 0)   # best with the current day worked (value before any day: none)
    first = True
    for p in pay:
        new_take = (skip[0] + p, skip[1] - 1)
        new_skip = max(skip, take) if not first else skip
        skip, take = new_skip, new_take
        first = False
    b = max(skip, take)
    return [b[0], -b[1]]


def _row(r, lo, hi):
    # best sum on r[lo..hi] with two or more empty between picks
    a = b = c = 0  # best up to i-3, i-2, i-1
    for i in range(lo, hi + 1):
        a, b, c = b, c, max(c, a + r[i])
    return c


def best_rent(rents):
    n = len(rents)
    out = _row(rents, 2, n - 1)                 # neither stall 0 nor stall 1
    out = max(out, rents[0] + _row(rents, 3, n - 3))
    if n > 1:
        out = max(out, rents[1] + _row(rents, 4, n - 2))
    return out


def solve_change_ways(text):
    tok = text.split()
    k = int(tok[0])
    coins = [int(x) for x in tok[1:1 + k]]
    q = int(tok[1 + k])
    fares = [int(x) for x in tok[2 + k:2 + k + q]]
    top = max(fares)
    ways = [0] * (top + 1)
    ways[0] = 1
    for c in coins:
        for a in range(c, top + 1):
            ways[a] = (ways[a] + ways[a - c]) % MOD
    return '\n'.join(str(ways[f]) for f in fares)


def best_product_stretch(factors):
    hi = lo = factors[0]
    best = None
    for f in factors[1:]:
        c1, c2 = f * hi, f * lo
        m, w = max(c1, c2), min(c1, c2)
        if best is None or m > best:
            best = m
        hi, lo = max(m, f), min(w, f)
    return best


def _moves():
    out = {}
    for free in range(8):       # bit set = cell still to cover in this column
        res = []

        def go(r, left, nxt):
            if r == 3:
                res.append(nxt)
                return
            if not left >> r & 1:
                go(r + 1, left, nxt)
                return
            go(r + 1, left, nxt | 1 << r)                      # slab along, into the next column
            if r < 2 and left >> (r + 1) & 1:
                go(r + 2, left, nxt)                           # slab across
        go(0, free, 0)
        out[free] = res
    return out


def paving_ways(n, drains):
    mv = _moves()
    block = [0] * (n + 1)
    for r, c in drains:
        block[c] |= 1 << r
    state = [0] * 8
    state[0] = 1
    for c in range(n):
        new = [0] * 8
        b, nb = block[c], block[c + 1]
        for m in range(8):
            v = state[m]
            if not v or m & b:
                continue
            for nxt in mv[7 & ~(m | b)]:
                if nxt & nb:
                    continue
                new[nxt] = (new[nxt] + v) % MOD
        state = new
    return state[0]


def cooldown_profit(prices, k):
    n = len(prices)
    cash = [0] * n
    hold = -prices[0]
    for i in range(1, n):
        cash[i] = max(cash[i - 1], hold + prices[i])
        j = i - k - 1
        hold = max(hold, (cash[j] if j >= 0 else 0) - prices[i])
    return cash[-1]


def fewest_words(text, words):
    # breadth-first over positions: the level a position is first reached at
    ws = set(words)
    lens = sorted({len(w) for w in ws})
    n = len(text)
    seen = [False] * (n + 1)
    seen[0] = True
    level = [0]
    steps = 0
    while level:
        steps += 1
        nxt = []
        for i in level:
            for L in lens:
                j = i + L
                if j > n:
                    break
                if not seen[j] and text[i:j] in ws:
                    if j == n:
                        return steps
                    seen[j] = True
                    nxt.append(j)
        level = nxt
    return -1


def rising_readings(readings):
    tails = []
    for x in readings:
        p = bisect_left(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
    return [len(tails), tails[-1]]


def _one(ch):
    return 9 if ch == '?' else (0 if ch == '0' else 1)


def _two(a, b):
    if a == '?':
        if b == '?':
            return 17
        return 2 if b <= '6' else 1
    if a == '1':
        return 10 if b == '?' else 1
    if a == '2':
        return 7 if b == '?' else (1 if b <= '6' else 0)
    return 0


def solve_tape_decodes(text):
    tok = text.split()
    t = int(tok[0])
    out = []
    for s in tok[1:1 + t]:
        p2, p1 = 0, 1
        prev = ''
        for ch in s:
            cur = p1 * _one(ch)
            if prev:
                cur += p2 * _two(prev, ch)
            p2, p1 = p1, cur % MOD
            prev = ch
        out.append(str(p1))
    return '\n'.join(out)


def fewest_tokens(values, amount):
    INF = float('inf')
    need = [0] + [INF] * amount
    vs = sorted(values, reverse=True)
    for a in range(1, amount + 1):
        b = INF
        for v in vs:
            if v <= a and need[a - v] + 1 < b:
                b = need[a - v] + 1
        need[a] = b
    if need[amount] == INF:
        return []
    out = []
    a = amount
    while a:
        for v in vs:
            if v <= a and need[a - v] == need[a] - 1:
                out.append(v)
                a -= v
                break
    return out


def _mul(A, B):
    m = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(m)) % MOD for j in range(m)] for i in range(m)]


def stride_ways(n, strides):
    m = max(strides)
    S = set(strides)
    # state (f[i], f[i-1], ..., f[i-m+1]); f[0] = 1 and f[negative] = 0
    M = [[0] * m for _ in range(m)]
    for s in S:
        M[0][s - 1] = 1
    for i in range(1, m):
        M[i][i - 1] = 1
    R = [[int(i == j) for j in range(m)] for i in range(m)]
    e = n
    while e:
        if e & 1:
            R = _mul(R, M)
        M = _mul(M, M)
        e >>= 1
    return R[0][0] % MOD


def longest_nest(crates):
    cs = sorted(set((w, h) for w, h in crates), key=lambda c: (c[0], -c[1]))
    tails = []
    for _, h in cs:
        p = bisect_right(tails, h)
        if p == len(tails):
            tails.append(h)
        else:
            tails[p] = h
    return len(tails)


def best_trips(prices, k, fee):
    NEG = float('-inf')
    free = [0] * (k + 1)
    hold = [NEG] * (k + 1)
    for p in prices:
        nf = free[:]
        nh = hold[:]
        for j in range(1, k + 1):
            if hold[j] + p - fee > nf[j]:
                nf[j] = hold[j] + p - fee
            if free[j - 1] - p > nh[j]:
                nh[j] = free[j - 1] - p
        free, hold = nf, nh
    return max(free)
