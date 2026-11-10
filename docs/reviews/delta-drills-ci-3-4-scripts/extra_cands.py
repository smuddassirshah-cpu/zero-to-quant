"""Candidates the fix pass did not plant, written by the delta reader.
Names are <fn>__<tag>; gen_times.py and extra.py rename them to <fn>."""
import bisect
from array import array


def find_in_ring__dict_probe(ring, targets):
    # no search: a dict of positions, and an absent id walks up one id at a time
    where = {v: i for i, v in enumerate(ring)}
    top = max(ring) if ring else None
    out = []
    for t in targets:
        if top is None or t > top:
            out.append(-1)
            continue
        while t not in where:
            t += 1
        out.append(where[t])
    return out


def solve_tick_ranges__dict_probe(text):
    # no search: dicts of first and last position, and an absent time walks up one millisecond at a time
    v = text.split()
    n, q = int(v[0]), int(v[1])
    ticks = [int(x) for x in v[2:2 + n]]
    first, last = {}, {}
    for i, t in enumerate(ticks):
        first.setdefault(t, i)
        last[t] = i
    top = ticks[-1] if ticks else -1
    out = []
    for t in map(int, v[2 + n:2 + n + q]):
        if t in first:
            out.append('%d %d' % (first[t], last[t]))
        elif t > top:
            out.append('-1 %d' % n)
        else:
            while t not in first:
                t += 1
            out.append('-1 %d' % first[t])
    return '\n'.join(out)


def solve_live_median__array(text):
    # the planted sorted list, kept in a C array of 32-bit ints (half the bytes to shift)
    tokens = text.split()
    q = int(tokens[0]) if tokens else 0
    live, out = array('i'), []
    for i in range(q):
        op, x = tokens[1 + 2 * i], int(tokens[2 + 2 * i])
        if op == '+':
            bisect.insort(live, x)
        else:
            del live[bisect.bisect_left(live, x)]
        out.append(str(live[(len(live) + 1) // 2 - 1]) if live else '-')
    return ' '.join(out)
