"""Independent references for the code items of topic-3.5 (different algorithms from the model solutions)."""


def active_total_bit(n=100000, window=2000, mult=7919, mod=30011, div=3):
    """Sum over i of the number of distinct symbols with a tick at time s, t - window < s <= t, t = i // div,
    after tick i. Method: a Fenwick tree that keeps a 1 at the latest tick of each symbol."""
    sym = [(i * mult) % mod for i in range(n)]
    tim = [i // div for i in range(n)]
    tree = [0] * (n + 2)

    def add(i, v):
        i += 1
        while i <= n + 1:
            tree[i] += v
            i += i & -i

    def pref(i):  # sum of positions 0..i
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    last = {}
    lo = 0
    total = 0
    for i in range(n):
        if sym[i] in last:
            add(last[sym[i]], -1)
        add(i, 1)
        last[sym[i]] = i
        t = tim[i]
        while tim[lo] <= t - window:
            lo += 1
        total += pref(i) - (pref(lo - 1) if lo > 0 else 0)
    return total


def active_total_brute(n, window=2000, mult=7919, mod=30011, div=3):
    sym = [(i * mult) % mod for i in range(n)]
    tim = [i // div for i in range(n)]
    total = 0
    for i in range(n):
        t = tim[i]
        total += len({sym[j] for j in range(i + 1) if t - window < tim[j] <= t})
    return total


def active_query_brute(events, window, t):
    """events: list of (symbol, time). Distinct symbols with time s, t - window < s <= t."""
    return len({s for s, u in events if t - window < u <= t})
