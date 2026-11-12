"""coding-4: my solutions (written from the statements before the models were read) and candidate-wrong solutions.
A name that starts "alt:" is another right solution and must pass."""
CANDS = {}

CANDS['pf-idioms-count-above-mean'] = {'mine': '''
def above_mean(xs):
    if not xs:
        return 0
    s, n = sum(xs), len(xs)
    return sum(1 for x in xs if x * n > s)
''', 'wrong': [
    ('at-least', 'counts the values equal to the mean too', '''
def above_mean(xs):
    if not xs:
        return 0
    m = sum(xs) / len(xs)
    return sum(1 for x in xs if x >= m)
'''),
    ('no-empty-case', 'divides by zero on the empty list', '''
def above_mean(xs):
    m = sum(xs) / len(xs)
    return sum(1 for x in xs if x > m)
'''),
    ('truncated-mean', 'integer against float division: int(sum / n) cuts a negative mean towards zero, so [-1, -2] gives 0', '''
def above_mean(xs):
    if not xs:
        return 0
    m = int(sum(xs) / len(xs))
    return sum(1 for x in xs if x > m)
'''),
    ('rounded-mean', 'rounds the mean to a whole number', '''
def above_mean(xs):
    if not xs:
        return 0
    m = round(sum(xs) / len(xs))
    return sum(1 for x in xs if x > m)
'''),
    ('median', 'uses the median', '''
def above_mean(xs):
    if not xs:
        return 0
    s = sorted(xs)
    m = (s[(len(s) - 1) // 2] + s[len(s) // 2]) / 2
    return sum(1 for x in xs if x > m)
'''),
    ('mean-inside-loop', 'the slower order: the mean is recomputed for every element', '''
def above_mean(xs):
    return sum(1 for x in xs if x > sum(xs) / len(xs))
'''),
    ('below-mean', 'counts the values below the mean', '''
def above_mean(xs):
    if not xs:
        return 0
    m = sum(xs) / len(xs)
    return sum(1 for x in xs if x < m)
'''),
    ('alt:floor-mean', 'right for whole numbers: x > sum // n is the same test as x > mean when x is whole', '''
def above_mean(xs):
    if not xs:
        return 0
    m = sum(xs) // len(xs)
    return sum(1 for x in xs if x > m)
'''),
]}

CANDS['ds-arrays-local-peaks'] = {'mine': '''
def local_peaks(xs):
    return [i for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]
''', 'wrong': [
    ('plateau', 'at least in place of strictly greater', '''
def local_peaks(xs):
    return [i for i in range(1, len(xs) - 1) if xs[i - 1] <= xs[i] >= xs[i + 1]]
'''),
    ('ends-count', 'lets an end count against its one neighbour', '''
def local_peaks(xs):
    out = []
    for i in range(len(xs)):
        left = xs[i - 1] if i > 0 else float('-inf')
        right = xs[i + 1] if i + 1 < len(xs) else float('-inf')
        if left < xs[i] > right:
            out.append(i)
    return out
'''),
    ('wraps-at-index-zero', 'off by one: the loop starts at index 0, where xs[i - 1] is the last value, so [5, 1, 2] gives [0]', '''
def local_peaks(xs):
    return [i for i in range(len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]
'''),
    ('runs-off-the-end', 'off by one: the loop reaches the last index', '''
def local_peaks(xs):
    return [i for i in range(1, len(xs)) if xs[i - 1] < xs[i] > xs[i + 1]]
'''),
    ('values-not-indices', 'returns the peak values', '''
def local_peaks(xs):
    return [xs[i] for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]
'''),
    ('left-neighbour-only', 'compares with the left neighbour only', '''
def local_peaks(xs):
    return [i for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i]]
'''),
    ('one-based', 'counts positions from 1', '''
def local_peaks(xs):
    return [i + 1 for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]
'''),
    ('stops-one-early', 'off by one: the last inner index is never tested', '''
def local_peaks(xs):
    return [i for i in range(1, len(xs) - 2) if xs[i - 1] < xs[i] > xs[i + 1]]
'''),
]}

CANDS['ds-pointers-median-of-three'] = {'mine': '''
def median3(xs):
    return [sorted(xs[i:i + 3])[1] for i in range(len(xs) - 2)]
''', 'wrong': [
    ('middle-element', 'the middle element of each window', '''
def median3(xs):
    return [xs[i + 1] for i in range(len(xs) - 2)]
'''),
    ('mean', 'the whole-number mean of each window', '''
def median3(xs):
    return [sum(xs[i:i + 3]) // 3 for i in range(len(xs) - 2)]
'''),
    ('misses-last-window', 'off by one: the last window is left out', '''
def median3(xs):
    return [sorted(xs[i:i + 3])[1] for i in range(len(xs) - 3)]
'''),
    ('short-windows', 'off by one: a window of two at the end is kept', '''
def median3(xs):
    return [sorted(xs[i:i + 3])[1] for i in range(len(xs) - 1)]
'''),
    ('blocks-of-three', 'windows that do not overlap', '''
def median3(xs):
    return [sorted(xs[i:i + 3])[1] for i in range(0, len(xs) - 2, 3)]
'''),
    ('sorts-the-list-first', 'sorts the whole list before taking windows', '''
def median3(xs):
    s = sorted(xs)
    return [s[i + 1] for i in range(len(s) - 2)]
'''),
    ('distinct-median', 'the middle of the different values, so 7, 7, 1 fails', '''
def median3(xs):
    out = []
    for i in range(len(xs) - 2):
        s = sorted(set(xs[i:i + 3]))
        out.append(s[len(s) // 2])
    return out
'''),
    ('alt:sum-less-ends', 'right: the sum less the largest and the smallest', '''
def median3(xs):
    return [a + b + c - max(a, b, c) - min(a, b, c) for a, b, c in zip(xs, xs[1:], xs[2:])]
'''),
]}

CANDS['simulation-rules-settle-day'] = {'mine': '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    left = lag
    while left > 0:
        d += 1
        if d % 7 < 5 and d not in holidays:
            left -= 1
    return d
''', 'wrong': [
    ('add-then-roll', 'adds the lag in calendar days, then rolls forward to a business day', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day + lag
    while d % 7 >= 5 or d in holidays:
        d += 1
    return d
'''),
    ('no-holidays', 'skips weekends only', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    while lag > 0:
        d += 1
        if d % 7 < 5:
            lag -= 1
    return d
'''),
    ('counts-trade-day', 'off by one: the trade day is counted as the first business day', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    left = lag
    while True:
        if d % 7 < 5 and d not in holidays:
            if left <= 1:
                return d
            left -= 1
        d += 1
'''),
    ('weekend-is-6-and-0', 'takes the weekend as remainders 6 and 0', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    while lag > 0:
        d += 1
        if d % 7 not in (6, 0) and d not in holidays:
            lag -= 1
    return d
'''),
    ('weekend-is-6-only', 'off by one in the weekend test: only remainder 6 is skipped', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    while lag > 0:
        d += 1
        if d % 7 < 6 and d not in holidays:
            lag -= 1
    return d
'''),
    ('weeks-then-holidays', 'jumps whole weeks, then adds one day for each holiday in the first span and never looks at the days added', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    weeks, rest = divmod(lag, 5)
    d += 7 * weeks
    while rest > 0:
        d += 1
        if d % 7 < 5:
            rest -= 1
    extra = sum(1 for h in holidays if trade_day < h <= d and h % 7 < 5)
    while extra > 0:
        d += 1
        if d % 7 < 5:
            extra -= 1
    return d
'''),
    ('holiday-on-weekend-twice', 'steps a day at a time but takes one more day for every holiday passed, weekend holidays too', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    left = lag
    while left > 0:
        d += 1
        if d in holidays:
            left += 1
        if d % 7 < 5:
            left -= 1
    return d
'''),
    ('rolls-the-start', 'first rolls a weekend trade day forward to Monday, then counts', '''
def settle_day(trade_day, lag, holidays):
    d = trade_day
    while d % 7 >= 5 or d in holidays:
        d += 1
    while lag > 0:
        d += 1
        if d % 7 < 5 and d not in holidays:
            lag -= 1
    return d
'''),
    ('alt:recursive', 'right: one call per calendar day (about 1,700 deep on the last test)', '''
def settle_day(trade_day, lag, holidays):
    if lag <= 0:
        return trade_day
    d = trade_day + 1
    return settle_day(d, lag - (1 if d % 7 < 5 and d not in holidays else 0), holidays)
'''),
]}

CANDS['at-search-smallest-n'] = {'mine': '''
def rows_needed(target):
    if target <= 0:
        return 0
    lo, hi = 0, 1
    while hi * (hi + 1) // 2 < target:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
''', 'wrong': [
    ('float-formula', 'ceil of the float root of the quadratic', '''
import math
def rows_needed(target):
    if target <= 0:
        return 0
    return math.ceil((-1 + math.sqrt(1 + 8 * target)) / 2)
'''),
    ('float-formula-root-2t', 'ceil of the float root of 2 * target, less a half', '''
import math
def rows_needed(target):
    if target <= 0:
        return 0
    return math.ceil(math.sqrt(2 * target + 0.25) - 0.5)
'''),
    ('float-power', 'the same formula with ** 0.5', '''
import math
def rows_needed(target):
    if target <= 0:
        return 0
    return math.ceil(((8 * target + 1) ** 0.5 - 1) / 2)
'''),
    ('float-mid', 'halving, but the triangle is worked out with float division', '''
def rows_needed(target):
    lo, hi = 0, 2 * 10 ** 9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) / 2 >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
'''),
    ('count-up', 'the slower order: one row at a time', '''
def rows_needed(target):
    n = 0
    total = 0
    while total < target:
        n += 1
        total += n
    return n
'''),
    ('strictly-more', 'needs more than target coins', '''
def rows_needed(target):
    lo, hi = 0, 2 * 10 ** 9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 > target:
            hi = mid
        else:
            lo = mid + 1
    return lo
'''),
    ('top-too-low', 'halving with a top end of 10 to the 9', '''
def rows_needed(target):
    lo, hi = 0, 10 ** 9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
'''),
    ('no-negative-case', 'the exact root with no case for a target below 0', '''
import math
def rows_needed(target):
    n = (math.isqrt(8 * target + 1) - 1) // 2
    return n if n * (n + 1) // 2 >= target else n + 1
'''),
    ('alt:isqrt', 'right: the whole-number square root', '''
import math
def rows_needed(target):
    if target <= 0:
        return 0
    n = (math.isqrt(8 * target + 1) - 1) // 2
    return n if n * (n + 1) // 2 >= target else n + 1
'''),
    ('alt:float-then-fix', 'right: a float first guess, then whole-number steps up or down', '''
import math
def rows_needed(target):
    if target <= 0:
        return 0
    n = max(0, int(math.sqrt(2 * target)) - 2)
    while n * (n + 1) // 2 < target:
        n += 1
    while n > 0 and (n - 1) * n // 2 >= target:
        n -= 1
    return n
'''),
]}

CANDS['gd-dp-dice-total-ways'] = {'mine': '''
def dice_ways(n, total):
    if total < n or total > 6 * n:
        return 0
    ways = [1] + [0] * total
    for _ in range(n):
        new = [0] * (total + 1)
        for t in range(total + 1):
            if ways[t]:
                for f in range(1, 7):
                    if t + f <= total:
                        new[t + f] += ways[t]
        ways = new
    return ways[total]
''', 'wrong': [
    ('plain-recursion', 'the slower order: recursion with no memory', '''
def dice_ways(n, total):
    if n == 0:
        return 1 if total == 0 else 0
    return sum(dice_ways(n - 1, total - f) for f in range(1, 7))
'''),
    ('pruned-recursion', 'the slower order: recursion with no memory, cut off when the total cannot be reached', '''
def dice_ways(n, total):
    if total < n or total > 6 * n:
        return 0
    if n == 0:
        return 1
    return sum(dice_ways(n - 1, total - f) for f in range(1, 7))
'''),
    ('unordered', 'counts sets of faces, not ordered rolls', '''
def dice_ways(n, total):
    def go(k, t, top):
        if k == 0:
            return 1 if t == 0 else 0
        return sum(go(k - 1, t - f, f) for f in range(1, top + 1) if t - f >= 0)
    return go(n, total, 6)
'''),
    ('five-faces', 'off by one: faces 1 to 5', '''
def dice_ways(n, total):
    ways = {0: 1}
    for _ in range(n):
        new = {}
        for t, c in ways.items():
            for f in range(1, 6):
                new[t + f] = new.get(t + f, 0) + c
        ways = new
    return ways.get(total, 0)
'''),
    ('faces-from-zero', 'off by one: faces 0 to 5', '''
def dice_ways(n, total):
    ways = {0: 1}
    for _ in range(n):
        new = {}
        for t, c in ways.items():
            for f in range(0, 6):
                new[t + f] = new.get(t + f, 0) + c
        ways = new
    return ways.get(total, 0)
'''),
    ('no-dice-is-one', 'with no dice every total has one way', '''
from functools import lru_cache
def dice_ways(n, total):
    @lru_cache(None)
    def f(k, t):
        if t < 0:
            return 0
        if k == 0:
            return 1
        return sum(f(k - 1, t - x) for x in range(1, 7))
    return f(n, total)
'''),
    ('float-chance', 'works with chances as floats and multiplies back by 6 to the n', '''
def dice_ways(n, total):
    p = {0: 1.0}
    for _ in range(n):
        new = {}
        for t, c in p.items():
            for f in range(1, 7):
                new[t + f] = new.get(t + f, 0.0) + c / 6
        p = new
    return round(p.get(total, 0.0) * 6 ** n)
'''),
    ('negative-index', 'a table indexed by total with no case for a total below 0', '''
def dice_ways(n, total):
    ways = [1] + [0] * (6 * n)
    for _ in range(n):
        new = [0] * (6 * n + 1)
        for t in range(6 * n + 1):
            for f in range(1, 7):
                if t - f >= 0:
                    new[t] += ways[t - f]
        ways = new
    return ways[total] if total <= 6 * n else 0
'''),
    ('alt:remembered-recursion', 'right: top-down with lru_cache (40 deep)', '''
from functools import lru_cache
def dice_ways(n, total):
    @lru_cache(None)
    def f(k, t):
        if t < k or t > 6 * k:
            return 0
        if k == 0:
            return 1
        return sum(f(k - 1, t - x) for x in range(1, 7))
    return f(n, total)
'''),
]}
