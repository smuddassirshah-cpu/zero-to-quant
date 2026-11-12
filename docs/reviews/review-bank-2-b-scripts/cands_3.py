"""coding-3: my solutions (written from the statements before the models were read) and candidate-wrong solutions.
A name that starts "alt:" is another right solution and must pass."""
CANDS = {}

CANDS['pf-idioms-trend-direction'] = {'mine': '''
def trend(xs):
    if len(xs) < 2:
        return 0
    if all(a < b for a, b in zip(xs, xs[1:])):
        return 1
    if all(a > b for a, b in zip(xs, xs[1:])):
        return -1
    return 0
''', 'wrong': [
    ('two-ends', 'compares the first value with the last only', '''
def trend(xs):
    if len(xs) < 2:
        return 0
    return 1 if xs[-1] > xs[0] else -1 if xs[-1] < xs[0] else 0
'''),
    ('not-strict', 'at least in place of above, so a repeat still counts as a rise', '''
def trend(xs):
    if len(xs) < 2:
        return 0
    if all(a <= b for a, b in zip(xs, xs[1:])):
        return 1
    if all(a >= b for a, b in zip(xs, xs[1:])):
        return -1
    return 0
'''),
    ('no-short-guard', 'all() of no pairs is True, so a short list gives 1', '''
def trend(xs):
    if all(a < b for a, b in zip(xs, xs[1:])):
        return 1
    if all(a > b for a, b in zip(xs, xs[1:])):
        return -1
    return 0
'''),
    ('first-pair-only', 'returns on the first pair it meets', '''
def trend(xs):
    for a, b in zip(xs, xs[1:]):
        if a < b:
            return 1
        if a > b:
            return -1
        return 0
    return 0
'''),
    ('first-and-last-pairs', 'checks the first pair and the last pair only, not the pairs between', '''
def trend(xs):
    if len(xs) < 2:
        return 0
    if xs[0] < xs[1] and xs[-2] < xs[-1]:
        return 1
    if xs[0] > xs[1] and xs[-2] > xs[-1]:
        return -1
    return 0
'''),
    ('first-pair-sets-direction', 'takes the direction from the first pair and rejects only a later pair that goes the other way, so a later repeat is let through', '''
def trend(xs):
    if len(xs) < 2 or xs[0] == xs[1]:
        return 0
    d = 1 if xs[1] > xs[0] else -1
    for a, b in zip(xs, xs[1:]):
        if (b - a) * d < 0:
            return 0
    return d
'''),
    ('every-pair-of-values', 'the slower order: compares every pair, not only neighbours', '''
def trend(xs):
    n = len(xs)
    if n < 2:
        return 0
    if all(xs[i] < xs[j] for i in range(n) for j in range(i + 1, n)):
        return 1
    if all(xs[i] > xs[j] for i in range(n) for j in range(i + 1, n)):
        return -1
    return 0
'''),
    ('sorted-equal', 'xs == sorted(xs) accepts repeats', '''
def trend(xs):
    if len(xs) < 2:
        return 0
    if xs == sorted(xs):
        return 1
    if xs == sorted(xs, reverse=True):
        return -1
    return 0
'''),
    ('alt:sorted-set', 'right: xs equals its sorted set', '''
def trend(xs):
    if len(xs) < 2:
        return 0
    s = sorted(set(xs))
    return 1 if xs == s else -1 if xs == s[::-1] else 0
'''),
]}

CANDS['at-sort-largest-gap'] = {'mine': '''
def largest_gap(xs):
    s = sorted(xs)
    return max((b - a for a, b in zip(s, s[1:])), default=0)
''', 'wrong': [
    ('input-order', 'gaps in input order', '''
def largest_gap(xs):
    return max((abs(b - a) for a, b in zip(xs, xs[1:])), default=0)
'''),
    ('range', 'the largest less the smallest', '''
def largest_gap(xs):
    return max(xs) - min(xs) if len(xs) > 1 else 0
'''),
    ('no-short-guard', 'max of an empty sequence raises', '''
def largest_gap(xs):
    s = sorted(xs)
    return max(b - a for a, b in zip(s, s[1:]))
'''),
    ('misses-last-gap', 'off by one: the last pair is never compared', '''
def largest_gap(xs):
    s = sorted(xs)
    best = 0
    for i in range(len(s) - 2):
        best = max(best, s[i + 1] - s[i])
    return best
'''),
    ('misses-first-gap', 'off by one: the first pair is never compared', '''
def largest_gap(xs):
    s = sorted(xs)
    best = 0
    for i in range(1, len(s) - 1):
        best = max(best, s[i + 1] - s[i])
    return best
'''),
    ('descending-signed', 'sorts downwards and keeps the signed differences', '''
def largest_gap(xs):
    s = sorted(xs, reverse=True)
    return max((b - a for a, b in zip(s, s[1:])), default=0)
'''),
    ('nearest-above-each', 'the slower order: for each value, a scan for the nearest value above it', '''
def largest_gap(xs):
    best = 0
    for x in xs:
        above = [y - x for y in xs if y > x]
        if above:
            best = max(best, min(above))
    return best
'''),
    ('alt:sorts-in-place', 'right, though it sorts the list it was given in place', '''
def largest_gap(xs):
    xs.sort()
    return max([xs[i + 1] - xs[i] for i in range(len(xs) - 1)] or [0])
'''),
]}

CANDS['at-greedy-orders-to-fill'] = {'mine': '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    for i, s in enumerate(sorted(sizes, reverse=True), 1):
        total += s
        if total >= target:
            return i
    return -1
''', 'wrong': [
    ('book-order', 'takes the orders as they sit, not largest first', '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    for i, s in enumerate(sizes, 1):
        total += s
        if total >= target:
            return i
    return -1
'''),
    ('smallest-first', 'sorts upwards', '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    for i, s in enumerate(sorted(sizes), 1):
        total += s
        if total >= target:
            return i
    return -1
'''),
    ('strictly-more', 'needs more than the target', '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    for i, s in enumerate(sorted(sizes, reverse=True), 1):
        total += s
        if total > target:
            return i
    return -1
'''),
    ('no-zero-target', 'no case for a target of 0 or less', '''
def orders_to_fill(sizes, target):
    total = 0
    for i, s in enumerate(sorted(sizes, reverse=True), 1):
        total += s
        if total >= target:
            return i
    return -1
'''),
    ('all-when-short', 'returns the number of orders when they fall short', '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    n = 0
    for s in sorted(sizes, reverse=True):
        total += s
        n += 1
        if total >= target:
            break
    return n
'''),
    ('checks-before-adding', 'off by one: tests the total before adding the order', '''
def orders_to_fill(sizes, target):
    total = 0
    n = 0
    for s in sorted(sizes, reverse=True):
        if total >= target:
            return n
        total += s
        n += 1
    return -1
'''),
    ('remove-max-in-place', 'the slower order and a changed input: max then remove, once per order taken', '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = n = 0
    while sizes:
        m = max(sizes)
        sizes.remove(m)
        total += m
        n += 1
        if total >= target:
            return n
    return -1
'''),
]}

CANDS['at-search-count-in-range'] = {'mine': '''
from bisect import bisect_left, bisect_right

def count_in_range(xs, lo, hi):
    if hi < lo:
        return 0
    return bisect_right(xs, hi) - bisect_left(xs, lo)
''', 'wrong': [
    ('linear-scan', 'the slower order: one pass over the whole list', '''
def count_in_range(xs, lo, hi):
    return sum(1 for x in xs if lo <= x <= hi)
'''),
    ('bisect-then-walk', 'the slower order: halves for the left edge, then walks to the right edge one value at a time', '''
from bisect import bisect_left
def count_in_range(xs, lo, hi):
    i = bisect_left(xs, lo)
    n = 0
    while i < len(xs) and xs[i] <= hi:
        n += 1
        i += 1
    return n
'''),
    ('left-both', 'bisect_left at both edges misses the values equal to hi', '''
from bisect import bisect_left
def count_in_range(xs, lo, hi):
    return max(0, bisect_left(xs, hi) - bisect_left(xs, lo))
'''),
    ('right-both', 'bisect_right at both edges misses the values equal to lo', '''
from bisect import bisect_right
def count_in_range(xs, lo, hi):
    return max(0, bisect_right(xs, hi) - bisect_right(xs, lo))
'''),
    ('no-empty-range', 'no case for hi below lo', '''
from bisect import bisect_left, bisect_right
def count_in_range(xs, lo, hi):
    return bisect_right(xs, hi) - bisect_left(xs, lo)
'''),
    ('search-stops-one-short', 'a hand-written halving whose top end is len(xs) - 1, so it can never answer len(xs)', '''
def count_in_range(xs, lo, hi):
    def first_at_least(v):
        a, b = 0, len(xs) - 1
        while a < b:
            m = (a + b) // 2
            if xs[m] < v:
                a = m + 1
            else:
                b = m
        return a
    def first_above(v):
        a, b = 0, len(xs) - 1
        while a < b:
            m = (a + b) // 2
            if xs[m] <= v:
                a = m + 1
            else:
                b = m
        return a
    if hi < lo or not xs:
        return 0
    return first_above(hi) - first_at_least(lo)
'''),
    ('index-of-lo', 'looks the edges up with list.index, which needs both to be present', '''
def count_in_range(xs, lo, hi):
    if hi < lo or not xs:
        return 0
    return len(xs) - xs[::-1].index(hi) - xs.index(lo)
'''),
    ('alt:hand-written', 'right: two hand-written halvings', '''
def count_in_range(xs, lo, hi):
    def first(pred):
        a, b = 0, len(xs)
        while a < b:
            m = (a + b) // 2
            if pred(xs[m]):
                b = m
            else:
                a = m + 1
        return a
    return max(0, first(lambda v: v > hi) - first(lambda v: v >= lo))
'''),
]}

CANDS['simulation-rules-clip-position'] = {'mine': '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        new = max(-limit, min(limit, pos + o))
        out.append(new - pos)
        pos = new
    return out
''', 'wrong': [
    ('all-or-nothing', 'rejects the whole order when it would breach', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        if abs(pos + o) <= limit:
            out.append(o); pos += o
        else:
            out.append(0)
    return out
'''),
    ('long-side-only', 'clips the long side only', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        new = min(limit, pos + o)
        out.append(new - pos)
        pos = new
    return out
'''),
    ('clips-the-order', 'clips each order to the limit, not the position', '''
def apply_orders(orders, limit):
    return [max(-limit, min(limit, o)) for o in orders]
'''),
    ('room-by-size', 'room is limit less the size of the position, so a sell from a full long book is refused', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        room = limit - abs(pos)
        f = min(abs(o), room) * (1 if o > 0 else -1)
        out.append(f)
        pos += f
    return out
'''),
    ('position-by-order', 'moves the position by the order, not by the fill', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        new = max(-limit, min(limit, pos + o))
        out.append(new - pos)
        pos += o
    return out
'''),
    ('returns-positions', 'returns the positions, not the fills', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        pos = max(-limit, min(limit, pos + o))
        out.append(pos)
    return out
'''),
    ('sums-the-fills', 'the slower order: the position is sum(out) at every order', '''
def apply_orders(orders, limit):
    out = []
    for o in orders:
        pos = sum(out)
        out.append(max(-limit, min(limit, pos + o)) - pos)
    return out
'''),
    ('alt:room-by-side', 'right: room worked out for the side of the order', '''
def apply_orders(orders, limit):
    pos = 0
    out = []
    for o in orders:
        f = min(o, limit - pos) if o > 0 else max(o, -limit - pos)
        out.append(f)
        pos += f
    return out
'''),
]}

CANDS['at-recursion-depth-weighted-sum'] = {'mine': '''
def depth_sum(x, depth=1):
    total = 0
    for v in x:
        if isinstance(v, list):
            total += depth_sum(v, depth + 1)
        else:
            total += v * depth
    return total
''', 'wrong': [
    ('top-at-zero', 'the outer list is depth 0', '''
def depth_sum(x, depth=0):
    return sum(depth_sum(v, depth + 1) if isinstance(v, list) else v * depth for v in x)
'''),
    ('plain-sum', 'adds the numbers with no weights', '''
def depth_sum(x):
    return sum(depth_sum(v) if isinstance(v, list) else v for v in x)
'''),
    ('depth-not-passed', 'every inner list is depth 2', '''
def depth_sum(x):
    def inner(y):
        return sum(inner(v) if isinstance(v, list) else 2 * v for v in y)
    return sum(inner(v) if isinstance(v, list) else v for v in x)
'''),
    ('counter-per-list', 'a shared counter that goes up at each list met and never comes back down', '''
def depth_sum(x):
    state = {'d': 0}
    def go(y):
        state['d'] += 1
        d = state['d']
        return sum(go(v) if isinstance(v, list) else v * d for v in y)
    return go(x)
'''),
    ('depth-squared', 'multiplies by the depth at every level on the way back up', '''
def depth_sum(x, depth=1):
    return depth * sum(depth_sum(v, depth + 1) if isinstance(v, list) else v for v in x)
'''),
    ('one-level', 'handles one level of nesting only', '''
def depth_sum(x):
    total = 0
    for v in x:
        if isinstance(v, list):
            total += 2 * sum(w for w in v if not isinstance(w, list))
        else:
            total += v
    return total
'''),
    ('max-depth-weight', 'weights every number by the depth of the deepest list', '''
def depth_sum(x):
    def depth(y):
        return 1 + max((depth(v) for v in y if isinstance(v, list)), default=0)
    def flat(y):
        return sum(flat(v) if isinstance(v, list) else v for v in y)
    return depth(x) * flat(x)
'''),
    ('alt:explicit-stack', 'right: a stack of (list, depth), no recursion', '''
def depth_sum(x):
    total = 0
    stack = [(x, 1)]
    while stack:
        y, d = stack.pop()
        for v in y:
            if isinstance(v, list):
                stack.append((v, d + 1))
            else:
                total += v * d
    return total
'''),
    ('alt:generator-in-sum', 'right: a generator inside sum at each call (the form the recursion rule in AUTHORING.md limits to about 300 deep)', '''
def depth_sum(x, depth=1):
    return sum(depth_sum(v, depth + 1) if isinstance(v, list) else v * depth for v in x)
'''),
    ('alt:head-and-tail', 'right: recursion on x[0] and x[1:], one call per element (about 2,000 deep on the last test)', '''
def depth_sum(x, depth=1):
    if not x:
        return 0
    h = x[0]
    return (depth_sum(h, depth + 1) if isinstance(h, list) else h * depth) + depth_sum(x[1:], depth)
'''),
]}
