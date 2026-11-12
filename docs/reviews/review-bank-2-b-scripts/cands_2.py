"""coding-2: my solutions (written from the statements before the models were read) and candidate-wrong solutions.
A name that starts "alt:" is another right solution and must pass."""
CANDS = {}

CANDS['pf-idioms-argmax-last'] = {'mine': '''
def argmax_last(xs):
    best = None
    for i, x in enumerate(xs):
        if best is None or x >= xs[best]:
            best = i
    return best
''', 'wrong': [
    ('first-tie', 'xs.index(max(xs)) finds the first tie', '''
def argmax_last(xs):
    if not xs:
        return None
    return xs.index(max(xs))
'''),
    ('strict-greater', 'a > comparison keeps the first tie', '''
def argmax_last(xs):
    best = None
    for i, x in enumerate(xs):
        if best is None or x > xs[best]:
            best = i
    return best
'''),
    ('no-empty-case', 'no guard for the empty list', '''
def argmax_last(xs):
    m = max(xs)
    return max(i for i, x in enumerate(xs) if x == m)
'''),
    ('starts-from-zero', 'the running best starts at 0, so an all-negative list finds nothing', '''
def argmax_last(xs):
    best, at = 0, None
    for i, x in enumerate(xs):
        if x >= best:
            best, at = x, i
    return at
'''),
    ('max-inside-loop', 'the slower order: max(xs) is recomputed for every element', '''
def argmax_last(xs):
    out = None
    for i, x in enumerate(xs):
        if x == max(xs):
            out = i
    return out
'''),
    ('reversed-off-by-one', 'searches the reversed list and forgets the minus 1', '''
def argmax_last(xs):
    if not xs:
        return None
    return len(xs) - xs[::-1].index(max(xs))
'''),
    ('minus-one-for-empty', 'returns -1 for the empty list', '''
def argmax_last(xs):
    best = -1
    for i, x in enumerate(xs):
        if best < 0 or x >= xs[best]:
            best = i
    return best
'''),
    ('alt:reversed-index', 'right: the reversed list, index of the max, turned back', '''
def argmax_last(xs):
    if not xs:
        return None
    return len(xs) - 1 - xs[::-1].index(max(xs))
'''),
    ('alt:key-pair', 'right: max over indices by (value, index)', '''
def argmax_last(xs):
    return max(range(len(xs)), key=lambda i: (xs[i], i)) if xs else None
'''),
]}

CANDS['edge-case-list-second-largest'] = {'mine': '''
def second_largest(xs):
    s = sorted(set(xs))
    return s[-2] if len(s) >= 2 else None
''', 'wrong': [
    ('sorted-minus-two', 'sorted(xs)[-2] counts a repeat of the largest', '''
def second_largest(xs):
    if len(xs) < 2:
        return None
    return sorted(xs)[-2]
'''),
    ('length-of-list', 'tests the length of the list, not of the set', '''
def second_largest(xs):
    if len(xs) < 2:
        return None
    return sorted(set(xs))[-2]
'''),
    ('no-equal-check', 'one pass that lets a repeat of the largest become the second', '''
def second_largest(xs):
    first = second = None
    for x in xs:
        if first is None or x > first:
            first, second = x, first
        elif second is None or x > second:
            second = x
    return second
'''),
    ('zero-start', 'one pass whose two bests start at 0, so negative lists fail', '''
def second_largest(xs):
    first = second = 0
    for x in xs:
        if x > first:
            first, second = x, first
        elif first > x > second:
            second = x
    return second if second else None
'''),
    ('minus-infinity', 'returns the minus infinity it started from in place of None', '''
def second_largest(xs):
    first = second = float('-inf')
    for x in xs:
        if x > first:
            first, second = x, first
        elif first > x > second:
            second = x
    return second
'''),
    ('max-of-rest-no-guard', 'removes the largest and takes max of the rest, with no guard when nothing is left', '''
def second_largest(xs):
    m = max(xs)
    return max(x for x in xs if x != m)
'''),
    ('max-inside-loop', 'the slower order: max(xs) is recomputed for every element', '''
def second_largest(xs):
    rest = [x for x in xs if x != max(xs)] if xs else []
    return max(rest) if rest else None
'''),
    ('second-smallest', 'takes the second value from the wrong end', '''
def second_largest(xs):
    s = sorted(set(xs))
    return s[1] if len(s) >= 2 else None
'''),
    ('alt:one-pass', 'right: one pass keeping the top two different values', '''
def second_largest(xs):
    first = second = None
    for x in xs:
        if first is None or x > first:
            first, second = x, first
        elif x != first and (second is None or x > second):
            second = x
    return second
'''),
]}

CANDS['ds-pointers-merge-ticks'] = {'mine': '''
def merge_ticks(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i][0] <= b[j][0]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
''', 'wrong': [
    ('sorted-tuples', 'sorted(a + b) orders a tie in time by price', '''
def merge_ticks(a, b):
    return sorted(a + b)
'''),
    ('ties-to-b', 'a < comparison sends ties to b', '''
def merge_ticks(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i][0] < b[j][0]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out + a[i:] + b[j:]
'''),
    ('drops-the-tail', 'stops when one feed runs out', '''
def merge_ticks(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i][0] <= b[j][0]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    return out
'''),
    ('heapq-merge', 'heapq.merge with no key compares whole tuples', '''
import heapq
def merge_ticks(a, b):
    return list(heapq.merge(a, b))
'''),
    ('b-first-sort', 'a stable sort of b + a by time: ties go to b', '''
def merge_ticks(a, b):
    return sorted(b + a, key=lambda t: t[0])
'''),
    ('one-per-time', 'keeps one tick per time', '''
def merge_ticks(a, b):
    seen = {}
    for t in a + b:
        seen.setdefault(t[0], t)
    return [seen[k] for k in sorted(seen)]
'''),
    ('pop-front-in-place', 'the slower order and changed inputs: pop(0) from both feeds, and a and b are emptied', '''
def merge_ticks(a, b):
    out = []
    while a and b:
        out.append(a.pop(0) if a[0][0] <= b[0][0] else b.pop(0))
    return out + a + b
'''),
    ('extends-a-in-place', 'right answer, but feed a is changed: a.extend(b) then a stable sort in place', '''
def merge_ticks(a, b):
    a.extend(b)
    a.sort(key=lambda t: t[0])
    return a
'''),
    ('alt:stable-sort', 'right: sorted(a + b, key=time) is stable, so a comes first at a tie', '''
def merge_ticks(a, b):
    return sorted(a + b, key=lambda t: t[0])
'''),
]}

CANDS['ds-arrays-round-trips'] = {'mine': '''
def round_trips(trades):
    pos = 0
    n = 0
    for t in trades:
        if t == 0:
            continue
        pos += t
        if pos == 0:
            n += 1
    return n
''', 'wrong': [
    ('every-zero', 'counts every time the position is zero, a zero trade while flat included', '''
def round_trips(trades):
    pos = n = 0
    for t in trades:
        pos += t
        if pos == 0:
            n += 1
    return n
'''),
    ('crossings', 'counts a move through zero as well as a stop on it', '''
def round_trips(trades):
    pos = n = 0
    for t in trades:
        new = pos + t
        if pos != 0 and (new == 0 or (new > 0) != (pos > 0)):
            n += 1
        pos = new
    return n
'''),
    ('starts-at-one', 'counts the flat start as a trip', '''
def round_trips(trades):
    pos = 0
    n = 1 if trades else 0
    for t in trades:
        if t:
            pos += t
            if pos == 0:
                n += 1
    return n
'''),
    ('skips-last-trade', 'off by one: the last trade is never applied', '''
def round_trips(trades):
    pos = n = 0
    for i in range(len(trades) - 1):
        if trades[i]:
            pos += trades[i]
            if pos == 0:
                n += 1
    return n
'''),
    ('prefix-sums-quadratic', 'the slower order: sum(trades[:i]) for every i', '''
def round_trips(trades):
    n = 0
    for i in range(1, len(trades) + 1):
        if sum(trades[:i]) == 0 and sum(trades[:i - 1]) != 0:
            n += 1
    return n
'''),
    ('cancelling-pairs', 'counts a trade that cancels the one before it', '''
def round_trips(trades):
    return sum(1 for a, b in zip(trades, trades[1:]) if a and a == -b)
'''),
    ('long-trips-only', 'counts a return to zero only from a long position', '''
def round_trips(trades):
    pos = n = 0
    for t in trades:
        if pos > 0 and pos + t == 0:
            n += 1
        pos += t
    return n
'''),
]}

CANDS['pf-collections-top-symbols'] = {'mine': '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return sorted(tot, key=lambda s: (-tot[s], s))[:k]
''', 'wrong': [
    ('total-only', 'sorts by the total alone, so ties keep the order of first appearance', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return sorted(tot, key=tot.get, reverse=True)[:k]
'''),
    ('pair-reversed', 'sorts (total, symbol) in reverse, so ties come Z to A', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return [s for _, s in sorted(((v, s) for s, v in tot.items()), reverse=True)][:k]
'''),
    ('most-common', 'Counter.most_common: ties keep the order of first appearance', '''
from collections import Counter
def top_symbols(trades, k):
    c = Counter()
    for s, q in trades:
        c[s] += q
    return [s for s, _ in c.most_common(k)]
'''),
    ('largest-single-trade', 'ranks by the largest single trade, not the total', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = max(tot.get(s, q), q)
    return sorted(tot, key=lambda s: (-tot[s], s))[:k]
'''),
    ('sizes-not-signed', 'adds the sizes, so a sale counts as a purchase', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + abs(q)
    return sorted(tot, key=lambda s: (-tot[s], s))[:k]
'''),
    ('drops-net-sellers', 'leaves out a symbol whose total is not positive', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return sorted((s for s in tot if tot[s] > 0), key=lambda s: (-tot[s], s))[:k]
'''),
    ('last-k-slice', 'sorts ascending and takes [-k:], which is the whole list when k is 0', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return sorted(tot, key=lambda s: (tot[s], [-ord(c) for c in s]))[-k:][::-1]
'''),
    ('rescans-per-symbol', 'the slower order: one scan of all trades for every symbol', '''
def top_symbols(trades, k):
    syms = sorted({s for s, _ in trades})
    tot = {s: sum(q for t, q in trades if t == s) for s in syms}
    return sorted(syms, key=lambda s: -tot[s])[:k]
'''),
    ('alt:alphabetical-then-stable', 'right: sort the symbols A to Z, then a stable sort by total', '''
def top_symbols(trades, k):
    tot = {}
    for s, q in trades:
        tot[s] = tot.get(s, 0) + q
    return sorted(sorted(tot), key=tot.get, reverse=True)[:k]
'''),
]}

CANDS['gd-dp-walk-above-zero'] = {'mine': '''
def nonneg_walk_counts(n):
    cur = {0: 1}
    for _ in range(n):
        nxt = {}
        for p, c in cur.items():
            nxt[p + 1] = nxt.get(p + 1, 0) + c
            if p > 0:
                nxt[p - 1] = nxt.get(p - 1, 0) + c
        cur = nxt
    return cur
''', 'wrong': [
    ('list-every-walk', 'the slower order: lists all 2 to the n walks', '''
from itertools import product
def nonneg_walk_counts(n):
    out = {}
    for steps in product((1, -1), repeat=n):
        p = 0
        for s in steps:
            p += s
            if p < 0:
                break
        else:
            out[p] = out.get(p, 0) + 1
    return out
'''),
    ('plain-recursion', 'the slower order: recursion over walks with no memory', '''
def nonneg_walk_counts(n):
    out = {}
    def go(k, p):
        if k == n:
            out[p] = out.get(p, 0) + 1
            return
        go(k + 1, p + 1)
        if p > 0:
            go(k + 1, p - 1)
    go(0, 0)
    return out
'''),
    ('unreachable-kept', 'a table over every position 0 to n, zeros included', '''
def nonneg_walk_counts(n):
    cur = [0] * (n + 2)
    cur[0] = 1
    for _ in range(n):
        nxt = [0] * (n + 2)
        for p in range(n + 1):
            if cur[p]:
                nxt[p + 1] += cur[p]
                if p > 0:
                    nxt[p - 1] += cur[p]
        cur = nxt
    return {p: cur[p] for p in range(n + 1)}
'''),
    ('no-floor', 'lets the walk go below 0 and keeps the ends at 0 or above', '''
from math import comb
def nonneg_walk_counts(n):
    return {k: comb(n, (n + k) // 2) for k in range(n % 2, n + 1, 2)}
'''),
    ('stays-positive', 'forbids a return to 0, not a visit below it', '''
def nonneg_walk_counts(n):
    cur = {0: 1}
    for i in range(n):
        nxt = {}
        for p, c in cur.items():
            nxt[p + 1] = nxt.get(p + 1, 0) + c
            if p > 1:
                nxt[p - 1] = nxt.get(p - 1, 0) + c
        cur = nxt
    return cur
'''),
    ('one-step-short', 'off by one: n - 1 rounds', '''
def nonneg_walk_counts(n):
    cur = {0: 1}
    for _ in range(n - 1):
        nxt = {}
        for p, c in cur.items():
            nxt[p + 1] = nxt.get(p + 1, 0) + c
            if p > 0:
                nxt[p - 1] = nxt.get(p - 1, 0) + c
        cur = nxt
    return cur
'''),
    ('float-ballot', 'the ballot formula with float factorial division', '''
from math import factorial
def nonneg_walk_counts(n):
    def c(a, b):
        return factorial(a) / (factorial(b) * factorial(a - b)) if 0 <= b <= a else 0
    return {k: int(c(n, (n + k) // 2) - c(n, (n + k) // 2 + 1)) for k in range(n % 2, n + 1, 2)}
'''),
    ('alt:ballot-formula', 'right: comb(n, u) - comb(n, u + 1) with u = (n + k) / 2', '''
from math import comb
def nonneg_walk_counts(n):
    return {k: comb(n, (n + k) // 2) - comb(n, (n + k) // 2 + 1) for k in range(n % 2, n + 1, 2)}
'''),
    ('alt:remembered-recursion', 'right: top-down with lru_cache', '''
from functools import lru_cache
def nonneg_walk_counts(n):
    @lru_cache(None)
    def f(k, p):
        if p < 0 or p > k:
            return 0
        if k == 0:
            return 1 if p == 0 else 0
        return f(k - 1, p - 1) + f(k - 1, p + 1)
    return {p: f(n, p) for p in range(n % 2, n + 1, 2)}
'''),
]}
