"""Delta reader's own solutions, pack 6. Written from the briefs, by a method other
than the model's wherever one exists. Used by run.py. Brute forces for the small
cases are in extra_6.py."""
from collections import deque


class _MaxTree:
    """Fenwick tree for prefix maxima."""

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def best(self, i):          # max over places 1..i
        r = 0
        while i > 0:
            if self.t[i] > r:
                r = self.t[i]
            i -= i & -i
        return r

    def put(self, i, v):
        while i <= self.n:
            if self.t[i] < v:
                self.t[i] = v
            i += i & -i


# ci-best-session: prefix sums; the earliest start whose best later prefix reaches the top.
def best_session(pnl):
    n = len(pnl)
    pre = [0] * (n + 1)
    for i, x in enumerate(pnl):
        pre[i + 1] = pre[i] + x
    sufmax = [0] * (n + 2)
    sufmax[n] = pre[n]
    for i in range(n - 1, 0, -1):
        sufmax[i] = max(pre[i], sufmax[i + 1])
    top = max(sufmax[s + 1] - pre[s] for s in range(n))
    for s in range(n):
        if sufmax[s + 1] - pre[s] == top:
            e = s
            while pre[e + 1] - pre[s] != top:
                e += 1
            return [top, s, e]


# ci-capped-trips: table over (trips allowed, days seen) with a running best buy.
def best_trips(prices, k, fee):
    n = len(prices)
    prev = [0] * (n + 1)
    for _ in range(k):
        cur = [0] * (n + 1)
        buy = None            # best of prev[b - 1] - price of day b, over days b seen
        for i in range(1, n + 1):
            p = prices[i - 1]
            cur[i] = cur[i - 1]
            if buy is not None and buy + p - fee > cur[i]:
                cur[i] = buy + p - fee
            cand = prev[i - 1] - p
            if buy is None or cand > buy:
                buy = cand
        prev = cur
    return prev[n]


# ci-fewest-tokens: the payment itself is carried for every amount.
def fewest_tokens(values, amount):
    best = [None] * (amount + 1)
    best[0] = ()
    for a in range(1, amount + 1):
        pick = None
        for v in values:
            if v <= a and best[a - v] is not None:
                b = best[a - v]
                if pick is not None and len(b) + 1 > len(pick):
                    continue
                # put v into the falling list b
                lo, hi = 0, len(b)
                while lo < hi:
                    mid = (lo + hi) // 2
                    if b[mid] >= v:
                        lo = mid + 1
                    else:
                        hi = mid
                cand = b[:lo] + (v,) + b[lo:]
                if pick is None or len(cand) < len(pick) or cand > pick:
                    pick = cand
        best[a] = pick
    return list(best[amount]) if best[amount] is not None else []


# ci-longest-rising: chain length at each reading from a tree of maxima over ranks.
def rising_readings(readings):
    rank = {v: i + 1 for i, v in enumerate(sorted(set(readings)))}
    tree = _MaxTree(len(rank))
    top, end = 0, None
    for v in readings:
        r = rank[v]
        ln = tree.best(r - 1) + 1
        tree.put(r, ln)
        if ln > top or (ln == top and v < end):
            top, end = ln, v
    return [top, end]


# ci-nested-crates: sort by (height, width); a row is a strictly rising run of widths.
def longest_nest(crates):
    order = sorted(crates, key=lambda c: (c[1], c[0]))
    rank = {w: i + 1 for i, w in enumerate(sorted({c[0] for c in crates}))}
    tree = _MaxTree(len(rank))
    top = 0
    for w, _ in order:
        r = rank[w]
        ln = tree.best(r - 1) + 1
        tree.put(r, ln)
        top = max(top, ln)
    return top


# ci-paving-ways: cell by cell with a three-cell window (not the model's column moves).
def paving_ways(n, drains):
    MOD = 1_000_000_007
    drain = set((r, c) for r, c in drains)
    ways = {0: 1}             # bit 0 = this cell already covered, bits 1, 2 = the next two
    for c in range(n):
        for r in range(3):
            nxt = {}
            for mask, w in ways.items():
                if (r, c) in drain:
                    if mask & 1:
                        continue
                    m = mask >> 1
                    nxt[m] = (nxt.get(m, 0) + w) % MOD
                    continue
                if mask & 1:
                    m = mask >> 1
                    nxt[m] = (nxt.get(m, 0) + w) % MOD
                    continue
                if c + 1 < n and (r, c + 1) not in drain:        # along the pavement
                    m = (mask >> 1) | 4
                    nxt[m] = (nxt.get(m, 0) + w) % MOD
                if r < 2 and (r + 1, c) not in drain and not mask & 2:   # across it
                    m = (mask >> 1) | 1
                    nxt[m] = (nxt.get(m, 0) + w) % MOD
            ways = nxt
    return ways.get(0, 0) % MOD


# ci-product-stretch: every stretch, with a running product.
def best_product_stretch(factors):
    best = None
    n = len(factors)
    for i in range(n - 1):
        p = factors[i]
        for j in range(i + 1, n):
            p *= factors[j]
            if best is None or p > best:
                best = p
            if p == 0:
                break            # every longer stretch from i is 0 too
    return best


# ci-shift-picks: the pay table first, then the fewest days among plans that reach it.
def best_shifts(pay):
    n = len(pay)
    F = [0] * (n + 2)
    G = [0] * (n + 2)
    for i in range(n):
        rest = F[i + 1]
        work = F[i] + pay[i]
        F[i + 2] = max(rest, work)
        c = []
        if rest == F[i + 2]:
            c.append(G[i + 1])
        if work == F[i + 2]:
            c.append(G[i] + 1)
        G[i + 2] = min(c)
    return [F[n + 1], G[n + 1]]


# ci-tape-decodes: the same two-term count, with every price found by listing digits.
def _digits(ch):
    return range(10) if ch == '?' else (int(ch),)


_ONE = {ch: sum(1 for d in _digits(ch) if d != 0) for ch in '0123456789?'}
_TWO = {(a, b): sum(1 for x in _digits(a) for y in _digits(b) if 10 <= 10 * x + y <= 26)
        for a in '0123456789?' for b in '0123456789?'}


def solve_tape_decodes(text):
    MOD = 1_000_000_007
    lines = [ln.strip() for ln in text.split('\n')]
    lines = [ln for ln in lines if ln]
    t = int(lines[0])
    out = []
    for tape in lines[1:1 + t]:
        a, b = 1, _ONE[tape[0]]         # counts for i - 1 and i characters
        for i in range(1, len(tape)):
            a, b = b, (b * _ONE[tape[i]] + a * _TWO[(tape[i - 1], tape[i])]) % MOD
        out.append(str(b % MOD))
    return '\n'.join(out)


# ci-word-split: a breadth-first search over positions, walking a trie of the codes.
def fewest_words(text, words):
    trie = [{}]
    ends = [False]
    for w in words:
        node = 0
        for ch in w:
            nx = trie[node].get(ch)
            if nx is None:
                nx = len(trie)
                trie[node][ch] = nx
                trie.append({})
                ends.append(False)
            node = nx
        ends[node] = True
    n = len(text)
    dist = [-1] * (n + 1)
    dist[0] = 0
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n:
            return dist[n]
        node = 0
        j = i
        while j < n:
            node = trie[node].get(text[j])
            if node is None:
                break
            j += 1
            if ends[node] and dist[j] < 0:
                dist[j] = dist[i] + 1
                q.append(j)
    return -1
