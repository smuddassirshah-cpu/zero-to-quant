"""Findings of review-perf-retrofit-2 as assertions. Fails by design: each FAIL
line names a finding and stays failing until its fix lands. The rubric section
also lists, for every longform item, each tick set that passes (7 or more with
every required row ticked) while leaving out a row the objective names.
Run from this folder: python3 findings_assert.py
"""
import json, os, sys
from itertools import combinations
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
C = os.path.join(ROOT, 'app/content/courses')
def item(f, i):
    return next(x for x in json.load(open(os.path.join(C, f)))['items'] if x['id'] == i)
FAILS = []
def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)
def rubric(it):
    w = it.get('widget', it)
    return w['rubric']
def passing_without(rub, core_rows):
    """Tick sets (1-based) that pass while leaving out one of core_rows."""
    n = len(rub); out = []
    for k in range(1, n + 1):
        for s in combinations(range(n), k):
            if sum(rub[i]['points'] for i in s) < 7: continue
            if any(rub[i].get('required') and i not in s for i in range(n)): continue
            if any(c - 1 not in s for c in core_rows):
                out.append([i + 1 for i in s])
    return out

ITEMS = {
    'SY1': ('systems/homework-1.json', 'h1-branch-aloud'), 'SY3': ('systems/homework-3.json', 'h3-process-aloud'),
    'PD1': ('pdes/homework-1.json', 'h-derive-lazy-walk'), 'MP1': ('measure-prob/homework-1.json', 'h-build-space'),
    'MP2': ('measure-prob/homework-2.json', 'h-build-integral'), 'MP3': ('measure-prob/homework-3.json', 'h-prove-urn'),
    'PZ4': ('puzzles/homework-4.json', 'hw4-kelly-draw')}
# rows the matched objective (or the prompt's "check each condition") names
CORE = {'SY1': [1, 3], 'SY3': [1, 2, 3], 'PD1': [2, 3], 'MP1': [1, 2, 3, 4], 'MP2': [4], 'MP3': [2, 3], 'PZ4': [2]}
for key, (f, i) in ITEMS.items():
    rub = rubric(item(f, i))
    req = [k + 1 for k, r in enumerate(rub) if r.get('required')]
    check(sum(r['points'] for r in rub) == 10 and 3 <= len(rub) <= 5 and 0 < len(req) < len(rub),
          '%s %s: rows %s sum to 10, required rows %s' % (key, i, [r['points'] for r in rub], req))
    core_req = [c for c in CORE[key] if c in req]
    left = passing_without(rub, CORE[key])
    tag = {'SY3': 'SY3-2', 'MP1': 'MP1-1', 'MP3': 'MP3-1'}.get(key)
    if tag:
        check(not left, '%s: a pass leaves out a named part, tick sets %s' % (tag, left[:4]))
    else:
        check(not left, '%s: no pass without the core rows %s' % (key, CORE[key]))

# SY3-1: the wake's switch out is not on the order's path
sy3 = item('systems/homework-3.json', 'h3-process-aloud')['widget']['model']
check('waits at least the 5' not in sy3 and 'at least 5 µs of waiting' not in sy3,
      'SY3-1: model says an order waits at least the 5 us wake; the path carries 1 + 2 = 3 us')
# SY3-3: the fix row names an L4 ring
r3 = item('systems/homework-3.json', 'h3-process-aloud')['widget']['rubric'][3]['text']
check('ring' not in r3, 'SY3-3: rubric row 4 asks for "a ring in shared memory" (ring buffers are level 4)')
# SY3-4 (Could): copied through the kernel stated without the shared-mapping exception
check('The bytes must be copied through the kernel' not in sy3, 'SY3-4: "The bytes must be copied through the kernel" with no exception')
# SY3-5 (Could): TLB entries said to be gone on every switch
check("the sender's TLB entries are gone" not in sy3, 'SY3-5: follow-up 3 says the TLB entries are gone (tagged TLBs can keep them)')

sy4 = item('systems/homework-4.json', 'h4-spsc-ring')
w4 = sy4['widget']
# SY4-1: memory order is not graded; the learner is not told
told = 'memory order' in (w4.get('how', '') + sy4.get('prose', '') + sy4['feedback']['correct']).lower()
check(told, 'SY4-1: a relaxed tail published before the slot passes all 12 tests; how/prose never says the orders are ungraded')
# SY4-2: explain gives the wrong reason for the count across the wrap
ex = sy4['explain']['text']
check(not ('difference' in ex.split('. ')[0] and 'multiple of' in ex.split('. ')[0]),
      'SY4-2: explain says tail_ - head_ survives the wrap "because 2^32 is a multiple of N" (it holds for any N; the slot needs it)')
# SY4-3: the report does not name l16's laid-out push and ring code
rep = open(os.path.join(ROOT, 'docs/reports/systems-4-perf.md')).read()
check('screen' in rep and 'l16' in rep.split('Freshness')[-1], 'SY4-3: report does not name l16 screens 5, 8 and 9 as the shared substrate')

# PD1-1 (Could): the rubric calls a bound the size
pd = item('pdes/homework-1.json', 'h-derive-lazy-walk')['rubric'][2]['text']
check('of size $\\Delta x$' not in pd, 'PD1-1: row 3 says the space remainder is "of size dx"; its order is dx^2 (dx is a bound)')
# MP1-2 (Could): exactly what continuity from above needs
mp1 = item('measure-prob/homework-1.json', 'h-build-space')['model']
check('some $\\mu(A_m)' in mp1 or 'some $m$' in mp1, 'MP1-2: model gives mu(A_1) < infinity as what continuity from above needs; some mu(A_m) finite is enough')
# MP3-2 (Could): report says no lesson uses the process
rep3 = open(os.path.join(ROOT, 'docs/reports/measure-prob-3-perf.md')).read()
check('markov' in rep3, 'MP3-2: report omits markov l17 screens 8 and 9 (the Polya share, a required prerequisite)')

print('findings failing:', len(FAILS))
sys.exit(1 if FAILS else 0)
