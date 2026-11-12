#!/usr/bin/env python3
"""Values of the hidden tests proposed in the review, each by two routes, and the proof that each catches its candidate.
Usage (repo root): python docs/reviews/review-delta-bank-2-scripts/proposed_code.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mine import MINE
from cands import C

def fn(src, name):
    ns = {}
    exec(src, ns)
    return ns[name]

def cand(iid, nm, name):
    return fn(next(s for m, _, s in C[iid] if m == nm), name)

fails = 0
def check(label, cond):
    global fails
    print(('ok   ' if cond else 'FAIL ') + label)
    fails += 0 if cond else 1

# 1. rows_needed: is there a target where the float root lands a row short and one step up is not enough? (No.)
mine = fn(MINE['at-search-smallest-n'], 'rows_needed')
up_only = cand('at-search-smallest-n', 'alt:float-formula-up-only', 'rows_needed')
ceil_f = cand('at-search-smallest-n', 'float-formula', 'rows_needed')
halving_f = cand('at-search-smallest-n', 'float-halving', 'rows_needed')
def exact(t):  # second route: integer square root
    if t <= 0: return 0
    n = (math.isqrt(8 * t + 1) - 1) // 2
    return n if n * (n + 1) // 2 >= t else n + 1
found = []
for m in range(1414213561, 1414000000, -1):
    T = m * (m + 1) // 2
    for t in (T + 1, T, T + 2, T - 1):
        if t <= 10**18 and up_only(t) != exact(t):
            found.append(t)
print(f'rows_needed: targets within 2 of a triangle number, m from 1,414,000,001 to 1,414,213,561, that the float-root-then-one-step-up')
print(f'   candidate gets wrong: {len(found)} (so it is a right solution in the stated range, and is listed as "alt:" in cands.py)')
check('the float root with a one-step-up check is right on all 854,244 targets tried', not found)
ts = [m * (m + 1) // 2 + 1 for m in range(1414213000, 1414213500)]
print('   float ceil formula wrong on', sum(1 for t in ts if ceil_f(t) != exact(t)), 'of 500 targets T(m) + 1; float halving wrong on', sum(1 for t in ts if halving_f(t) != exact(t)))
check('my halving agrees with the integer square root on those 500', all(mine(t) == exact(t) for t in ts))

# 2. above_mean([0, 6, 10, 10, 10]): mean 7.2, so 3; midrange 5 gives 4; median 10 gives 0.
xs = [0, 6, 10, 10, 10]
am = fn(MINE['pf-idioms-count-above-mean'], 'above_mean')
check('above_mean([0, 6, 10, 10, 10]) is 3 two ways', am(xs) == 3 == len([x for x in xs if x > sum(xs) / len(xs)]))
check('midrange candidate gives another value', cand('pf-idioms-count-above-mean', 'midrange', 'above_mean')(xs) != 3)
for nm, _, s in C['pf-idioms-count-above-mean']:
    if nm.startswith('alt:'): check(f'right alternative {nm[4:]} gives 3', fn(s, 'above_mean')(xs) == 3)

# 3. runner_up_gap([-1, -5, -2]) is 1; the size-comparing candidate gives 3.
xs = [-1, -5, -2]
rg = fn(MINE['edge-case-list-second-largest'], 'runner_up_gap')
d = sorted(set(xs))
check('runner_up_gap([-1, -5, -2]) is 1 two ways', rg(xs) == 1 == d[-1] - d[-2])
check('abs-values candidate gives another value', cand('edge-case-list-second-largest', 'abs-values', 'runner_up_gap')(xs) != 1)
check('every candidate that [-1, -5, -3] caught is still caught or caught elsewhere: smallest-gap, range, zero-start on [-1, -5, -2]',
      all(cand('edge-case-list-second-largest', n, 'runner_up_gap')(xs) != 1 for n in ('smallest-gap', 'range', 'zero-start')))

# 4. count_in_range with 3,000 calls: the copying slice is then far over the limit, the model is not.
total = sum(1000000 - k // 2 for k in range(0, 6000, 2))
series = 3000 * 1000000 - sum(range(3000))
xs = list(range(0, 2000000, 2))
cr = fn(MINE['at-search-count-in-range'], 'count_in_range')
check(f'sum(count_in_range(xs, k, 10**7) for k in range(0, 6000, 2)) is {total}', total == series == sum(cr(xs, k, 10**7) for k in range(0, 6000, 2)))

# 5. busiest_symbols with 20,000 symbols: expected value by my solution and by a Counter.
trades = [("S%05d" % (i % 20000), (i % 7) - 3) for i in range(100000)]
bs = fn(MINE['pf-collections-top-symbols'], 'busiest_symbols')
from collections import Counter
c = Counter()
for s, q in trades: c[s] += abs(q)
first = {}
for i, (s, _) in enumerate(trades): first.setdefault(s, i)
want = sorted(c, key=lambda s: (-c[s], first[s]))[:3]
check(f'busiest_symbols(trades, 3) with 20,000 symbols is {want}', bs(trades, 3) == want)
print('   totals of the first five:', [(s, c[s]) for s in sorted(c, key=lambda s: (-c[s], first[s]))[:5]])

print('failures:', fails)
sys.exit(1 if fails else 0)
