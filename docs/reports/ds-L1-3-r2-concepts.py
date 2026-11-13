#!/usr/bin/env python3
"""Round 2 blind concept audit of ds L1 to L3: executable checks.

Run from the repository root: python3 docs/reports/ds-L1-3-r2-concepts.py
CPython 3.13 here; the app runs Pyodide 0.27.7 (CPython 3.12.7, wasm32). The
two differ for this course only in object sizes (see PYODIDE below), which
were read from the local Pyodide build with node and are recorded as constants.

Sections
  A  every code widget: solution passes all hidden tests, starter fails one
  B  graded keys and slip values recomputed from the mistake the feedback names
  C  complexity and operation-count claims (counted, not timed, where possible)
  D  code lines quoted in prose, hints, explains and feedback
  E  algorithm invariants against brute force
  F  timing checks (ratios with wide margins)

A check that fails because the content is wrong or imprecise stays failing and
is tagged with its finding number in docs/reviews/audit-ds-1-3-r2.md. The
script exits 0 only when no check fails.
"""
import json, os, sys, time, random, itertools, collections
from collections import Counter, defaultdict, deque, OrderedDict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DS = os.path.join(ROOT, 'app', 'content', 'courses', 'ds')
LESSONS = ['l1-arrays-in-memory', 'l2-constant-time-lookup', 'l3-two-sum', 'l4-frequencies',
           'l5-both-ends', 'l6-sliding-window', 'l7-prefix-sums', 'l8-best-day',
           'l9-last-in-first-out', 'l10-next-greater', 'l11-first-in-first-out',
           'l12-nodes-and-pointers', 'l13-fast-and-slow']
SETS = ['review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3']
DOC = {n: json.load(open(os.path.join(DS, n + '.json'))) for n in LESSONS + SETS}
# sys.version, pointer size, sys.getsizeof(1.0) measured in pkgs/pyodide-0.27.7 with node
PYODIDE = {'pointer': 4, 'float': 16}

fails, passes = [], 0
random.seed(20261113)


def check(name, cond, finding=None):
    global passes
    if cond:
        passes += 1
    else:
        fails.append((name, finding))
        print('FAIL', name, '' if finding is None else '[finding %s]' % finding)


def L(n):
    return DOC[[x for x in LESSONS if x.startswith('l%d-' % n)][0]]


def S(n, i):
    return L(n)['screens'][i]


def Q(n, i):
    return L(n)['quiz'][i]


def W(item):
    return item['widget']


def slip(item, key):
    return [w for w in W(item)['wrong'] if w['id'] == key][0]['value']


def correct_text(item):
    return [o['text'] for o in W(item)['options'] if o.get('correct')]


# ---------------------------------------------------------------- A: code widgets
def run_tests(w, src):
    ns = {'__learner_source__': src}
    exec(w.get('prelude', ''), ns)
    exec(src, ns)
    out = []
    for t in w['tests']:
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            out.append(got == eval(t['expect'], ns))
        except BaseException:
            out.append(False)
    return out


def code_items():
    for n in LESSONS:
        for k in ('screens', 'quiz'):
            for i, it in enumerate(DOC[n].get(k, [])):
                if it.get('widget', {}).get('kind') == 'code':
                    yield '%s %s[%d]' % (n, k, i), it['widget']
    for n in SETS:
        for i, it in enumerate(DOC[n]['items']):
            if it.get('widget', {}).get('kind') == 'code':
                yield '%s items[%d]' % (n, i), it['widget']


ncode = 0
for name, w in code_items():
    ncode += 1
    check('A %s: solution passes all %d tests' % (name, len(w['tests'])), all(run_tests(w, w['solution'])))
    check('A %s: starter fails a test' % name, not all(run_tests(w, w['starter'])))
check('A: 32 code widgets found', ncode == 32)

# ---------------------------------------------------------------- B: keys and slips
# l1
check('B l1 s0', W(S(1, 0))['answer'] == 1000 + 4 * 8 and slip(S(1, 0), 'from-one') == 1000 + 5 * 8
      and slip(S(1, 0), 'no-size') == 1000 + 4 and slip(S(1, 0), 'index-three') == 1000 + 3 * 8)
cells = ['101.20', '102.50', '100.40', '103.10', '104.00']


def shifts(n, i):
    xs = list(range(n))
    before = xs[:]
    xs.insert(i, -1)
    return sum(1 for k, v in enumerate(before) if xs.index(v) != k)


check('B l1 s1 s2 shifts', [shifts(5, 0), shifts(5, 2), shifts(5, 5)] == [5, 3, 0]
      and [r[1]['answer'] for r in W(S(1, 2))['rows']] == [5, 3, 0] and W(S(1, 1))['answer'] == ['c2', 'c3', 'c4'])


def doubling_copies(appends, cap=1):
    size = copies = 0
    for _ in range(appends):
        if size == cap:
            copies += size
            cap *= 2
        size += 1
    return copies


check('B l1 s4 doubling 16 appends', doubling_copies(16) == 15 == W(S(1, 4))['answer'])
check('B l1 s4 slips', slip(S(1, 4), 'every-time') == sum(range(16)) and slip(S(1, 4), 'one-each') == 16
      and slip(S(1, 4), 'with-sixteen') == 15 + 16)
check('B l1 s5 insert(0) shifts', sum(range(1000)) == 499500 == W(S(1, 5))['answer']
      and slip(S(1, 5), 'one-to-n') == sum(range(1, 1001)) and slip(S(1, 5), 'n-squared') == 1000 ** 2)
check('B l1 s6 memory, 64-bit', (8 + 24) * 10 ** 6 / 1e6 == W(S(1, 6))['answer'] and sys.getsizeof(1.0) == 24)
# fix pass: the 8 and 24 bytes are now framed as 64-bit desktop Python, and the app's own sizes are stated
check('B l1 s6 memory: 64-bit premise stated, and the app runtime sizes (Pyodide, wasm32) given correctly',
      PYODIDE['pointer'] == 4 and PYODIDE['float'] == 16
      and S(1, 6)['prose'].startswith('On a 64-bit desktop Python') and 'a pointer is 4 bytes and a float object 16' in S(1, 6)['prose'] and '32-bit build' in S(1, 6)['prose']
      and S(1, 6)['question'].startswith('On a 64-bit desktop Python') and 'On a 64-bit build it uses a quarter' in S(1, 6)['explain']['text']
      and (PYODIDE['pointer'] + PYODIDE['float']) / 8 != 4, finding=2)
check('B l1 s7 string copies', 10 * sum(range(1, 1001)) == 5005000 == W(S(1, 7))['answer']
      and slip(S(1, 7), 'join-count') == 10 * 1000 and slip(S(1, 7), 'n-squared') == 1000 * 10000)
check('B l1 quiz', W(Q(1, 0))['answer'] == shifts(10, 3) == 7 and slip(Q(1, 0), 'upto') == 6
      and W(Q(1, 3))['answer'] == 2000 + 10 * 4 and slip(Q(1, 3), 'from-one') == 2000 + 11 * 4
      and slip(Q(1, 3), 'eight') == 2000 + 10 * 8 and slip(Q(1, 3), 'no-size') == 2010)

# l2
def toy(t):
    return sum(ord(c) - 64 for c in t) % 5


check('B l2 toy hash', [toy(t) for t in ('VOD', 'BP', 'HSBA', 'AZN', 'GSK', 'RIO', 'TSCO', 'BT', 'BARC', 'SHEL')]
      == [1, 3, 0, 1, 2, 2, 2, 2, 4, 4] and W(Q(2, 2))['answer'] == 4 and slip(Q(2, 2), 'sum') == 24
      and slip(Q(2, 2), 'quotient') == round(24 / 5))
check('B l2 s4', W(S(2, 4))['answer'] == 10000 ** 2 and slip(S(2, 4), 'added') == 20000 and slip(S(2, 4), 'half') == 10000 ** 2 // 2)
n = 2_000_000
check('B l2 s5 about 2e12', abs(n * (n - 1) / 2 / 2e12 - 1) < 0.01)
import math
check('B l2 s5 n log2 n about 4e7', abs(n * math.log2(n) / 4e7 - 1) < 0.06)
check('B l2 s9', W(S(2, 9))['answer'] == (1 + 500) / 2 * 10 ** 6 and slip(S(2, 9), 'full-scan') == 500 * 10 ** 6)
# l3
p = [3, 8, 5, 12, 6]
check('B l3 s0 one pair', [(i, j) for i in range(5) for j in range(i + 1, 5) if p[i] + p[j] == 17] == [(2, 3)])
check('B l3 s0 explain: "Only 5 and 12 find their partners in the list: each other"',
      [x for x in p if 17 - x in p] == [5, 12] and 'Only 5 and 12 find their partners' in S(3, 0)['explain']['text'], finding=4)
check('B l3 s1', W(S(3, 1))['answer'] == math.comb(5, 2) and slip(S(3, 1), 'ordered') == 20 and math.comb(1000, 2) == 499500 == W(Q(3, 0))['answer']
      and slip(Q(3, 0), 'ordered') == 999000)
# l5
xs = [1, 3, 4, 6, 8, 11, 15]


def two_ptr_sums(nums, t):
    i, j, out = 0, len(nums) - 1, []
    while i < j:
        s = nums[i] + nums[j]
        out.append(s)
        if s == t:
            return out, (i, j)
        if s < t:
            i += 1
        else:
            j -= 1
    return out, None


check('B l5 s1 walk', two_ptr_sums(xs, 10) == ([16, 12, 9, 11, 9, 10], (2, 3)) and math.comb(7, 2) == 21)
check('B l5 s2 target 20', two_ptr_sums(xs, 20) == ([16, 18, 19, 21, 17, 19], None))
visited = set()
i, j = 0, len(xs) - 1
while i < j:
    visited.add((i, j))
    s = xs[i] + xs[j]
    if s == 10:
        break
    if s < 10:
        i += 1
    else:
        j -= 1
check('B l5 s5 prose: the state i on 4, j on 8 is offered as a supposition, since the correct walk never reaches it',
      (2, 4) not in visited and 'Suppose a walk stands with `i` on 4 and `j` on 8' in S(5, 5)['prose']
      and 'We have reached' not in S(5, 5)['prose'], finding=5)
pal = lambda w: len(w) // 2
check('B l5 s3 palindrome comparisons', pal('refer') == 2 == W(S(5, 3))['answer'] and pal('noon') == 2 and W(Q(5, 2))['answer'] == 3)
check('B l5 s8', two_ptr_sums([-120, -75, -40, 15, 60, 90, 135], 50) == ([15, 60, 15, 50], (2, 5)) and abs(math.comb(10000, 2) / 5e7 - 1) < 0.01)
check('B l5 quiz0 unsorted', two_ptr_sums([8, 3, 5, 1, 9], 10) == ([17, 9, 4, 6], None))
# l6
v = [4, 2, 7, 1, 8, 3, 6, 5]
ws = [sum(v[s:s + 3]) for s in range(6)]
check('B l6 s0 s1', ws == [13, 10, 16, 12, 17, 14] and W(S(6, 0))['answer'] == 10 and slip(S(6, 0), 'kept') == 13 + 1
      and slip(S(6, 0), 'dropped') == 13 - 4 and slip(S(6, 0), 'two') == 2 + 1 and W(S(6, 1))['answer'] == ['c4'])
check('B l6 s2', 981 * 20 == 19620 and 20 + 2 * 980 == 1980 and 90 < (751 * 250) / (250 + 2 * 750) < 115)


def shortest_at_least(a, k, log=None):
    left = total = 0
    best = None
    for right, x in enumerate(a):
        total += x
        while total >= k:
            ln = right - left + 1
            if log is not None:
                log.append(ln)
            best = ln if best is None else min(best, ln)
            total -= a[left]
            left += 1
    return best


lg = []
check('B l6 s4', shortest_at_least([2, 3, 1, 2, 4, 3], 7, lg) == 2 and lg == [4, 4, 3, 3, 2])
check('B l6 quiz1 negatives', shortest_at_least([5, -4, 6], 6) == 3)
vol = [420, 380, 510, 610, 450, 390, 700, 650, 300, 480]
check('B l6 s9', [sum(vol[s:s + 5]) for s in range(6)] == [2370, 2340, 2660, 2800, 2490, 2520]
      and W(S(6, 9))['answer'] == 2800 and slip(S(6, 9), 'top5') == sum(sorted(vol)[-5:]))
cl = [100, 101, 103, 102, 104, 105, 107, 106]
ups = [b > a for a, b in zip(cl, cl[1:])]
runs = [len(list(g)) for k, g in itertools.groupby(ups) if k]
check('B l6 quiz0', max(runs) == 3 == W(Q(6, 0))['answer'] and sum(ups) == 5 and runs[0] == 2)
# l7
x7 = [3, -1, 4, 2, -5, 6]
pre = [0] + list(itertools.accumulate(x7))
check('B l7 s0-s3', pre == [0, 3, 2, 6, 8, 3, 9] and sum(x7[1:4]) == 5 == W(S(7, 0))['answer']
      and slip(S(7, 0), 'from0') == sum(x7[0:4]) and slip(S(7, 0), 'to4') == sum(x7[1:5]) and slip(S(7, 0), 'whole') == sum(x7)
      and W(S(7, 3))['answer'] == pre[6] - pre[2] == 7 and slip(S(7, 3), 'from1') == pre[6] - pre[1]
      and slip(S(7, 3), 'to5') == pre[5] - pre[2] and slip(S(7, 3), 'pre5') == pre[5] - pre[1])


def brute_count(a, k):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a) + 1) if sum(a[i:j]) == k)


check('B l7 s5', [0] + list(itertools.accumulate([2, -1, 1, 3, -2, 2])) == [0, 2, 1, 2, 5, 3, 5] and brute_count([2, -1, 1, 3, -2, 2], 3) == 5)
check('B l7 s6 key and slips', brute_count([0, 0, 0], 0) == 6 == W(S(7, 6))['answer'] and slip(S(7, 6), 'singles') == 3 and slip(S(7, 6), 'whole') == 1)
# fix pass: feedback for slip 4 now names singles plus the whole list, missing both pairs
check('B l7 s6 slip four: three singles plus the whole list, both pairs missed, gives the slip value 4',
      3 + 1 == 6 - 2 == slip(S(7, 6), 'four') and 'missed the two pairs' in S(7, 6)['feedback']['byKey']['four'], finding=1)
cum = [120, 40, 240, 290, 140, 230, 190, 370, 310, 420]
check('B l7 s9', cum[6] - cum[2] == -50 == W(S(7, 9))['answer'] and slip(S(7, 9), 'drop4') == cum[6] - cum[3]
      and [cum[k] - cum[k - 1] for k in (3, 4, 5, 6)] == [50, -150, 90, -40])
check('B l7 quiz2', brute_count([1, 2, 1, 2], 3) == 3 == W(Q(7, 2))['answer'])
# l8
px = [102, 110, 104, 98, 101, 107, 95, 99, 103, 97]


def brute_trade(a):
    best = (0, 0, 0)
    cands = [(a[j] - a[i], j, i) for i in range(len(a)) for j in range(i + 1, len(a)) if a[j] - a[i] > 0]
    if not cands:
        return best
    top = max(c[0] for c in cands)
    j, i = min((c[1], c[2]) for c in cands if c[0] == top)
    return (i, j, top)


def mdd(a):
    hi, worst = a[0], 0
    for q in a[1:]:
        hi = max(hi, q)
        worst = max(worst, hi - q)
    return worst


check('B l8 s0 s1', brute_trade(px) == (3, 5, 9) and math.comb(10, 2) == 45 == W(S(8, 1))['answer'] and math.comb(2520, 2) == 3173940)
lo, best, rows = px[0], 0, []
for q in px[1:]:
    best = max(best, q - lo)
    lo = min(lo, q)
    rows.append((lo, best))
check('B l8 s2 table', [(r[2]['answer'], r[3]['answer']) for r in W(S(8, 2))['rows'][3:7]] == rows[2:6])
a4 = [110, 104, 101, 97]
lo, best = a4[0], a4[1] - a4[0]
for q in a4[1:]:
    best = max(best, q - lo)
    lo = min(lo, q)
check('B l8 s4 colleague returns -3', best == -3)
check('B l8 s5 drawdown', mdd(px) == 15 == W(S(8, 5))['answer'] and slip(S(8, 5), 'first') == 110 - 98 and slip(S(8, 5), 'last') == 110 - 97)
d8 = [b - a for a, b in zip(px, px[1:])]


def kadane(a):
    run = best = 0
    for q in a:
        run = max(0, run + q)
        best = max(best, run)
    return best


check('B l8 s6', d8 == [8, -6, -6, 3, 6, -12, 4, 4, -6] and kadane(d8) == 9 == brute_trade(px)[2])
check('B l8 quiz', kadane([-2, 5, -1, 4, -6, 3]) == 8 == W(Q(8, 2))['answer'] and slip(Q(8, 2), 'ups') == 12 and slip(Q(8, 2), 'all') == 3
      and mdd([100, 120, 90, 130, 80]) == 50 == W(Q(8, 3))['answer'])
# l9, l10, l11
def postfix(tokens, swap=False):
    st = []
    for t in tokens.split():
        if t in '+-*/':
            b, a = st.pop(), st.pop()
            if swap:
                a, b = b, a
            st.append({'+': a + b, '-': a - b, '*': a * b, '/': a / b if b else 0}[t])
        else:
            st.append(float(t))
    return st.pop()


check('B l9 postfix', postfix('5 1 2 + 4 * + 3 -') == 14 == W(S(9, 7))['answer'] and slip(S(9, 7), 'swapped') == 3 - 17
      and postfix('2 3 4 * +') == 14 and slip(Q(9, 1), 'left-to-right') == (2 + 3) * 4
      and postfix('4 2 5 * + 1 -') == 13 == W(DOC['review-3']['items'][0])['answer'])
check('B l10 s1', math.comb(6, 2) == 15 == W(S(10, 1))['answer'] and abs(math.comb(100000, 2) / 5e9 - 1) < 0.01)


def next_greater(a, strict=True, ops=None):
    ans, st = [-1] * len(a), []
    for i, x in enumerate(a):
        while st and (a[st[-1]] < x if strict else a[st[-1]] <= x):
            ans[st.pop()] = x
            if ops is not None:
                ops[0] += 1
        st.append(i)
        if ops is not None:
            ops[0] += 1
    return ans, [a[k] for k in st]


check('B l10 scans', next_greater([4, 2, 6, 3, 1, 5, 7])[0] == [6, 6, 7, 5, 5, 7, -1]
      and next_greater([5, 5, 6], strict=False)[0] == [5, 6, -1] and next_greater([5, 5, 6])[0] == [6, 6, -1]
      and next_greater([6, 4, 5, 2])[1] == [6, 5, 2] and next_greater([3, 1, 4, 1, 5, 9, 2, 6])[1] == [9, 6]
      and next_greater([3, 8, 4, 1, 9])[0] == [8, 9, 9, 9, -1])
check('B l10 s2 / summary "the waiting values never rise from bottom to top" (ties wait, so they can be level)',
      next_greater([5, 5, 4])[1] == [5, 5, 4]
      and 'never rise from bottom to top' in S(10, 2)['explain']['text'] and 'never rise from bottom to top' in L(10)['summary']['ideas'][1], finding=8)
h = [2, 1, 5, 6, 2, 3]
check('B l10 s8 largest rectangle', max(min(h[i:j]) * (j - i) for i in range(6) for j in range(i + 1, 7)) == 10)
check('B l11', sum(range(1000)) == 499500 == W(S(11, 3))['answer'] and slip(S(11, 3), 'off') == sum(range(1, 1001))
      and W(Q(11, 2))['answer'] == 250 - 20 + 1 and W(Q(11, 3))['answer'] == 100 * 10 + 50 * 12
      and slip(Q(11, 3), 'lifo') == 100 * 12 + 50 * 10 and slip(Q(11, 3), 'average') == 150 * 11)
h3 = DOC['homework-3']['items'][2]
check('B hw3 FIFO', W(h3)['answer'] == 200 * 50 + 100 * 52 + 50 * 49 and slip(h3, 'lifo') == 300 * 49 + 50 * 52
      and abs(slip(h3, 'avg') - 350 * (200 * 50 + 100 * 52 + 300 * 49) / 600) < 0.01)
# l12, l13
check('B l12', W(S(12, 2))['answer'] == shifts(1000, 1) + 999000 == 999999 and W(Q(12, 0))['answer'] == 4999)
check('B l12 s0 explain "visiting k nodes" and summary "k - 1 steps" agree with quiz 0 (5,000th close: 4,999 steps)',
      W(Q(12, 0))['answer'] == 5000 - 1 and 'means visiting $k$ nodes' in S(12, 0)['explain']['text']
      and '$k - 1$ steps from the head' in L(12)['summary']['ideas'][0], finding=10)


def floyd(a, Lc, fast_speed=2, limit=10 ** 6):
    """positions on a rho: nodes 0..a+Lc-1, node a+Lc-1 points to a. Returns (moves, meeting node)."""
    nxt = lambda u: u + 1 if u + 1 < a + Lc else a
    s = f = 0
    for t in range(1, limit):
        s = nxt(s)
        for _ in range(fast_speed):
            f = nxt(f)
        if s == f:
            return t, s
    return None


check('B l13 s2', floyd(2, 4) == (4, 4))  # node index 4 holds the value 5
check('B rev3 item4', floyd(3, 5) == (5, 5) and W(DOC['review-3']['items'][4])['answer'] == 5)
ok = True
for a in range(0, 14):
    for Lc in range(1, 14):
        t, m = floyd(a, Lc)
        b = m - a
        ok &= (t - a <= Lc if t >= a else False) and (a + b) % Lc == 0 and 0 <= b < Lc
        # reset: a steps from head and from the meeting point both land on node a
        u = m
        for _ in range(a):
            u = u + 1 if u + 1 < a + Lc else a
        ok &= (u == a)
check('B l13 s3 s8: meet within L moves of slow entering; a+b=kL; reset lands on the start', ok)
check('B l13 quiz3 tortoise', 400 * 2 - 400 == 400 == W(Q(13, 3))['answer'])
# reviews and homework numbers
r1, r2 = DOC['review-1']['items'], DOC['review-2']['items']
check('B rev1', W(r1[0])['answer'] == shifts(8, 3) == 5 and W(r1[1])['answer'] == toy('SHEL') and 97 + 100 == 98 + 99)
check('B rev2', two_ptr_sums([2, 5, 9, 12, 20], 21)[1] == (2, 3) and W(r2[1])['answer'] == sum([5, 1, 4, 6, 2][2:4])
      and [0] + list(itertools.accumulate([4, -3, 6, 3, -4])) == [0, 4, 1, 7, 10, 6] and W(r2[2])['answer'] == 6
      and brute_trade([45, 52, 39, 44, 48, 36])[2] == 9 == W(r2[3])['answer'] and shortest_at_least([1, 4, 2, 3, 5], 8) == 2
      and brute_count([3, 4, -7, 3, 1, 3, 1, -4], 7) == 3 == W(r2[6])['answer'] and mdd([0, 50, 20, 90, 40, 70, 10, 60]) == 80 == W(r2[7])['answer'])
h1, h2 = DOC['homework-1']['items'], DOC['homework-2']['items']
check('B hw1', doubling_copies(1000) == 1023 == W(h1[2])['answer'] and slip(h1[2], 'with-1024') == 2047 and slip(h1[2], 'every') == sum(range(1000))
      and W(h1[6])['answer'] == 25000 * 10000 and math.comb(200000, 2) == 19999900000 and math.comb(100000, 2) == 4999950000)
g = [[2, -1, 3], [0, 4, 1], [5, -2, 2]]
P = [[sum(g[r][c] for r in range(R) for c in range(C)) for C in range(4)] for R in range(4)]
check('B hw2 grid', P == [[0, 0, 0, 0], [0, 2, 1, 4], [0, 2, 5, 9], [0, 7, 8, 14]] and P[3][3] - P[1][3] - P[3][1] + P[1][1] == 5 == W(h2[4])['answer']
      and slip(h2[4], 'noadd') == 14 - 4 - 7 and shortest_at_least([12, 3, 7, 9, 4, 15, 2], 20) == 3 == W(h2[5])['answer'])

# ---------------------------------------------------------------- C: complexity and operation counts
class K:
    """key with counted comparisons; bad=True forces every key into one bucket"""
    eq = 0

    def __init__(self, v, bad=False):
        self.v, self.bad = v, bad

    def __hash__(self):
        return 1 if self.bad else hash(self.v)

    def __eq__(self, o):
        K.eq += 1
        return self.v == o.v


def eq_calls(container, key):
    K.eq = 0
    _ = key in container
    return K.eq


nk = 2000
good = [K(i) for i in range(nk)]
bad = [K(i, True) for i in range(nk)]
check('C list membership is a scan: last item costs n comparisons', eq_calls(good, K(nk - 1)) == nk and eq_calls(good, K(-1)) == nk)
gs, bs = set(good), set(bad)
avg_good = sum(eq_calls(gs, K(i)) for i in range(nk)) / nk
avg_bad = sum(eq_calls(bs, K(i, True)) for i in range(0, nk, 50)) / (nk / 50)
check('C hash set, spread keys: O(1) comparisons on average', avg_good <= 2)
check('C hash set, every key in one bucket: lookups cost O(n)', avg_bad > nk / 8 and eq_calls(bs, K(-1, True)) >= nk)
# amortised append in CPython: count pointer copies at each reallocation, worst case (block always moves)
xs, copies, caps, last = [], 0, [], sys.getsizeof([])
N = 200000
for i in range(N):
    xs.append(i)
    sz = sys.getsizeof(xs)
    if sz != last:
        copies += i  # the i items already stored
        caps.append((sz - sys.getsizeof([])) // 8)
        last = sz
ratios = [b / a for a, b in zip(caps, caps[1:]) if a > 1000]
check('C CPython list grows by about an eighth', all(1.10 < r < 1.15 for r in ratios))
check('C CPython appends: total copies linear in n (amortised O(1))', copies < 10 * N)
check('C doubling: copies always fewer than twice the appends', all(doubling_copies(k) < 2 * k for k in range(1, 3000)))
# monotonic stack: pushes + pops <= 2n
okc = True
for _ in range(300):
    a = [random.randint(0, 9) for _ in range(random.randint(0, 40))]
    ops = [0]
    ans, _st = next_greater(a, ops=ops)
    okc &= ops[0] <= 2 * len(a)
    okc &= ans == [next((y for y in a[i + 1:] if y > x), -1) for i, x in enumerate(a)]
check('C next greater: pushes plus pops at most 2n, answers match the nested scan', okc)
ops = [0]
next_greater(list(range(200000, 0, -1)), ops=ops)
check('C l10 s7 explain "200,000 values take at most 400,000 stack operations" (falling test list: 200,000)',
      ops[0] == 200000 <= 400000 and 'at most 400,000 stack operations' in S(10, 7)['explain']['text'], finding=9)
ops = [0]
next_greater(list(range(1000)), ops=ops)
check('C rising list: 2n - 1 stack operations', ops[0] == 1999)
# sliding maximum: each index enters once, leaves at most once
def sliding_max(a, w, cnt=None, front=True):
    dq, out = deque(), []
    for i, x in enumerate(a):
        if front and dq and dq[0] <= i - w:
            dq.popleft()
            if cnt is not None:
                cnt[1] += 1
        while dq and a[dq[-1]] <= x:
            dq.pop()
            if cnt is not None:
                cnt[1] += 1
        dq.append(i)
        if cnt is not None:
            cnt[0] += 1
        if i >= w - 1:
            out.append(a[dq[0]])
    return out


okc = True
for _ in range(300):
    a = [random.randint(-5, 5) for _ in range(random.randint(0, 30))]
    w = random.randint(1, 8)
    cnt = [0, 0]
    okc &= sliding_max(a, w, cnt) == [max(a[i:i + w]) for i in range(len(a) - w + 1)]
    okc &= cnt[0] == len(a) and cnt[1] <= len(a)
check('C sliding maximum equals brute force; each index enters once and leaves at most once', okc)
check('C l11 s5 s7', sliding_max([5, 3, 4, 1, 2, 6], 3) == [5, 4, 4, 6] and sliding_max([5, 3, 4, 1, 2, 6], 3, front=False) == [5, 5, 5, 6]
      and sliding_max([2, 7, 3, 1, 5, 4], 2) == [7, 7, 3, 5, 5])
# l1 s10: window[1:] + [close] copies
check('C l1 s10 option c "about 40 copies per tick" (slice copies 19, + copies 20 more)',
      abs((19 + 20) / 40 - 1) < 0.05 and 'about 40 copies per tick' in W(S(1, 10))['options'][2]['why'], finding=3)
# rate limiter count

# ---------------------------------------------------------------- D: quoted code
def raises(fn, exc, text=None):
    try:
        fn()
    except exc as e:
        return text is None or text in str(e)
    except BaseException:
        return False
    return False


def newest_first(ticks):
    out = []
    for t in ticks:
        out.insert(0, t)
    return out


def app_rev(ticks):
    out = []
    for t in ticks:
        out.append(t)
    out.reverse()
    return out


check('D l1 s5 append then reverse equals insert(0)', newest_first(list(range(50))) == app_rev(list(range(50))))
check('D l1 quiz', raises(lambda: [][0], IndexError, 'list index out of range')
      and raises(lambda: exec('s="VOD"\ns[0]="B"'), TypeError, "'str' object does not support item assignment") and 'B' + 'VOD'[1:] == 'BOD')
check('D l1 s9 join', ','.join([]) == '' and f'{99.999:.2f}' == '100.00')
dq = deque(maxlen=20)
for c in range(30):
    dq.append(c)
w0 = list(range(10))
w0.remove(w0[0])
check('D l1 s10 deque(maxlen) and remove', list(dq) == list(range(10, 30)) and w0 == list(range(1, 10)))
check('D l2 keys', raises(lambda: {}['VOD'], KeyError, "'VOD'") and {}.get('VOD') is None and {}.get('VOD', 0) == 0 and Counter()['VOD'] == 0
      and raises(lambda: {}.__setitem__(['VOD', 'BP'], 1), TypeError, "unhashable type: 'list'")
      and raises(lambda: {{'VOD': 100}: 1}, TypeError) and {('VOD', '2024-03-01'): 1, 42: 2, 'VOD': 3} is not None)
check('D l2 s6 / summary "strings, numbers and tuples of them" (a tuple holding a list is not hashable)',
      raises(lambda: {(1, [2]): 0}, TypeError) and 'tuples of them' in S(2, 6)['feedback']['correct']
      and 'tuples of them' in L(2)['summary']['ideas'][2], finding=11)
check('D l2 quiz3', set([1, 2, 3]) & set([2, 3, 4]) == {2, 3})


def two_sum_store_first(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        seen[x] = i
        if target - x in seen:
            return (seen[target - x], i)
    return None


def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], i)
        seen[x] = i
    return None


check('D l3', two_sum_store_first([3, 4, 1], 6) == (0, 0) and two_sum([3, 3], 6) == (0, 1) and two_sum([6, 1, 9, 4, 7], 13) == (2, 3)
      and two_sum([5], 10) is None and two_sum([1250, 830, 2100, 1670, 420], 2500) == (1, 3)
      and two_sum([300, -100, 200, -300], 0) == (0, 3) and two_sum([1, 5, 1, 5], 6) == (0, 1))
okc = True
for _ in range(500):
    a = sorted(random.randint(-20, 20) for _ in range(random.randint(0, 12)))
    t = random.randint(-30, 30)
    sums, hit = two_ptr_sums(a, t)
    exists = any(a[i] + a[j] == t for i in range(len(a)) for j in range(i + 1, len(a)))
    okc &= (hit is not None) == exists and len(sums) <= max(0, len(a) - 1)
check('D l5 two pointers find a pair iff one exists, in at most n - 1 sums', okc)
check('D l3 s7', two_ptr_sums([2, 4, 5, 8, 11, 13], 16) == ([15, 17, 15, 16], (2, 4)))
fills = ['VOD', 'BP', 'VOD', 'AZN', 'VOD', 'BP']
counts = {}
for t in fills:
    counts[t] = counts.get(t, 0) + 1
check('D l4 tally', counts == {'VOD': 3, 'BP': 2, 'AZN': 1} and Counter(fills).most_common(1) == [('VOD', 3)])


def plus_eq():
    c = {}
    for t in ['VOD', 'BP', 'VOD']:
        c[t] += 1


dd = defaultdict(int)
dd['VOD'] += 2
check('D l4 misc', raises(plus_eq, KeyError, "'VOD'") and (dd['BP'], len(dd)) == (0, 2) and set('trades') == set('traders')
      and Counter('banana').most_common(1) == [('a', 3)] and Counter('banana') == {'a': 3, 'n': 2, 'b': 1}
      and raises(lambda: defaultdict(list)[sorted('tea')], TypeError, "unhashable type: 'list'")
      and ''.join(sorted('tea')) == 'aet' and ''.join(sorted('rate')) == 'aert' == ''.join(sorted('tear'))
      and Counter('') == Counter('') and Counter('Listen') != Counter('silent') and Counter('dirty room') != Counter('dormitory'))
bad_check = lambda a, b: all(a.count(c) == b.count(c) for c in a)
check('D l4 s6 option d is called wrong as well as slow: ab and abc pass it', bad_check('ab', 'abc') and Counter('ab') != Counter('abc')
      and 'Without a length check it is wrong too: `ab` and `abc` pass' in W(S(4, 6))['options'][3]['why'], finding=12)
check('D hw1 most_common tie', Counter(['VOD', 'BP', 'VOD', 'AZN', 'BP']).most_common(1)[0][0] == 'VOD')
x5 = [3, 8, 1, 9, 4]
for i in range(len(x5)):
    x5[i], x5[-1 - i] = x5[-1 - i], x5[i]
sq = sorted(q * q for q in [-7, -3, -1, 2, 4, 6])
check('D l5 quiz1 double swap; squares', x5 == [3, 8, 1, 9, 4] and sq == [1, 4, 9, 16, 36, 49])


def longest_unique_buggy(s):
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in last:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


check('D l6 s6 buggy window', longest_unique_buggy('abba') == 3 and longest_unique_buggy('abcbd') == 3)
# quiz 3: wrong update is off by xs[0] - xs[k] after k slides
okc = True
for _ in range(100):
    a = [random.randint(-9, 9) for _ in range(12)]
    w = random.randint(2, 5)
    tot = sum(a[:w])
    for k, right in enumerate(range(w, len(a)), 1):
        tot += a[right] - a[right - w + 1]
        okc &= tot - sum(a[k:k + w]) == a[0] - a[k]
check('D l6 quiz3 off by xs[0] - xs[k]', okc)
inc = [3, 2, 6, 8, 3, 9]
check('D l7 s4 inclusive convention wraps', inc[2] - inc[0 - 1] == -3 and inc[2] - inc[0] == 3)


def count_no_seed(a, k):
    seen, total, cnt = {}, 0, 0
    for q in a:
        total += q
        cnt += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return cnt


check('D l7 s6 without {0: 1} gives 3', count_no_seed([0, 0, 0], 0) == 3)
check('D l7 s8 explain test 13', Counter([0] + list(itertools.accumulate([1, -1] * 10000))) == {0: 10001, 1: 10000}
      and math.comb(10001, 2) + math.comb(10000, 2) == 10000 ** 2 and abs(math.comb(20001, 2) / 2e8 - 1) < 0.01)


def bal_first(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif stack.pop() != pairs[ch]:
            return False
    return True


check('D l9 s6 first attempt', bal_first('{[()]}') and not bal_first('([)]') and bal_first('((') and raises(lambda: bal_first(')'), IndexError, 'pop from empty list'))
s9 = []
for q in [3, 1, 4]:
    s9.append(q)
s9.pop()
s9.append(5)
q11 = deque([1, 2, 3])
q11.append(4)
q11.popleft()
q11.popleft()
check('D l9 l11 quiz snippets', s9 == [3, 1, 5] and list(q11) == [3, 4] and 8.0 == 8)


class Node:
    def __init__(self, val, next=None):
        self.val, self.next = val, next


def from_list(vals):
    head = None
    for q in reversed(vals):
        head = Node(q, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def rev_short(head):
    prev, cur = None, head
    while cur:
        cur.next = prev
        prev = cur
        cur = cur.next
    return prev


hd = from_list([7, 3, 9, 4])
a_ = hd.next
new = Node(5)
a_.next = new
new.next = a_.next
check('D l12 s1 wrong order makes a self-loop', new.next is new)
hd = from_list([7, 3, 9, 4])
a_ = hd.next
a_.next = a_.next.next
check('D l12 delete after', to_list(hd) == [7, 3, 4])
hd = from_list([7, 3, 9, 4])
del hd.next.next
check('D l12 s3 del a.next then walking raises AttributeError', raises(lambda: to_list(hd), AttributeError))
check('D l12 s5 short reverse returns [7]', to_list(rev_short(from_list([7, 3, 9, 4]))) == [7])


def has_cycle_bad(head):
    slow = fast = head
    while fast.next and fast:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


check('D l13 s5', raises(lambda: has_cycle_bad(from_list([1, 2])), AttributeError, "'NoneType' object has no attribute 'next'"))
check('D l13 middle', [middle(from_list(list(range(1, k + 1)))).val for k in (1, 2, 4, 5, 6)] == [1, 2, 3, 3, 4] and middle(None) is None)
# speed 3 against 1: fast can pass slow without landing on it
jumped = False
for a in range(0, 6):
    for Lc in range(2, 9):
        nxt = lambda u: u + 1 if u + 1 < a + Lc else a
        s = f = 0
        for t in range(1, 200):
            s2 = nxt(s)
            path = [nxt(f)]
            path.append(nxt(path[-1]))
            path.append(nxt(path[-1]))
            if s2 in path[:-1] and path[-1] != s2 and s >= a:
                jumped = True
            s, f = s2, path[-1]
check('D l13 s6 speed 3 against 1 can jump over slow', jumped)
calls = [0]
class CountSet(set):
    def __init__(self, it):
        calls[0] += 1
        super().__init__(it)
_ = [q for q in range(50) if q in CountSet(range(50))]
check('D rev1 item5 the set in a comprehension condition is rebuilt for every x', calls[0] == 50)
check('D rev1 item4', raises(lambda: sum(['a', 'b'], ''), TypeError, 'join'))

# ---------------------------------------------------------------- E: invariants against brute force
okc = oknn = True
for _ in range(400):
    a = [random.randint(1, 9) for _ in range(random.randint(1, 14))]
    k = random.randint(1, 30)
    br = min((j - i for i in range(len(a)) for j in range(i + 1, len(a) + 1) if sum(a[i:j]) >= k), default=None)
    okc &= shortest_at_least(a, k) == br
    z = [random.randint(0, 5) for _ in range(random.randint(1, 14))]
    br = min((j - i for i in range(len(z)) for j in range(i + 1, len(z) + 1) if sum(z[i:j]) >= k), default=None)
    oknn &= shortest_at_least(z, k) == br
check('E shrinking window is right on positive lists', okc)
check('E l6 summary note "safe only when no number is negative" (right with zeros too)',
      oknn and 'only when no number is negative' in L(6)['summary']['formula']['note'], finding=6)
okc = True
for _ in range(300):
    a = [random.randint(-4, 4) for _ in range(random.randint(0, 14))]
    k = random.randint(-3, 5)
    seen, total, cnt = {0: 1}, 0, 0
    for q in a:
        total += q
        cnt += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    okc &= cnt == brute_count(a, k)
check('E prefix-count with a dict equals brute force, negatives and zeros included', okc)
okc = True
for _ in range(400):
    a = [random.randint(1, 12) for _ in range(random.randint(1, 12))]
    lo, best = 0, (0, 0, 0)
    for j in range(1, len(a)):
        pr = a[j] - a[lo]
        if pr > best[2]:
            best = (lo, j, pr)
        if a[j] < a[lo]:
            lo = j
    okc &= best == brute_trade(a)
    dch = [y - x for x, y in zip(a, a[1:])]
    okc &= kadane(dch) == best[2]
    okc &= mdd(a) == max([a[i] - a[j] for i in range(len(a)) for j in range(i + 1, len(a))] + [0])
    okc &= mdd(a) == brute_trade([-q for q in a])[2] == -min([sum(dch[i:j]) for i in range(len(dch) + 1) for j in range(i, len(dch) + 1)])
check('E best trade (with tie rules) = brute force = Kadane on changes; drawdown = best trade on negated prices', okc)
# hw2 model (e): segment-tree merge of (max, min, drawdown)
okc = True
for _ in range(300):
    a = [random.randint(1, 30) for _ in range(random.randint(2, 16))]
    m = random.randint(1, len(a) - 1)
    Lh, Rh = a[:m], a[m:]
    okc &= mdd(a) == max(mdd(Lh), mdd(Rh), max(Lh) - min(Rh))
check('E hw2 (e) drawdown merges from (max, min, drawdown) of two halves', okc)
# convention: sums of simple returns are not compounded returns
r = [0.5, -0.4, 0.5]
best_sum = max((sum(r[i:j]), (i, j)) for i in range(3) for j in range(i + 1, 4))
best_cmp = max((math.prod(1 + q for q in r[i:j]) - 1, (i, j)) for i in range(3) for j in range(i + 1, 4))
lr = [math.log(1 + q) for q in r]
best_log = max((sum(lr[i:j]), (i, j)) for i in range(3) for j in range(i + 1, 4))
check('E l8 s6 / hw2 item2 now say log returns or P&L (simple returns compound; log returns add)',
      best_sum[1] != best_cmp[1] and best_log[1] == best_cmp[1]
      and 'On daily log returns, or daily P&L' in S(8, 6)['explain']['text']
      and "daily P&L is the maximum subarray" in DOC['homework-2']['items'][2]['prose'], finding=7)
lr = [math.log(1 + q) for q in r]
best_log = max((sum(lr[i:j]), (i, j)) for i in range(3) for j in range(i + 1, 4))
check('E with log returns the maximum-sum stretch is the best compounded stretch', best_log[1] == best_cmp[1])
okc = True
for _ in range(300):
    a = [random.randint(1, 9) for _ in range(random.randint(0, 14))]
    sp, st = [], []
    for i, q in enumerate(a):
        while st and a[st[-1]] <= q:
            st.pop()
        sp.append(i + 1 if not st else i - st[-1])
        st.append(i)
    br = []
    for i in range(len(a)):
        k = 0
        while i - k >= 0 and a[i - k] <= a[i]:
            k += 1
        br.append(k)
    okc &= sp == br
check('E stock span equals its definition', okc)
od_ok = True
exec(DOC['homework-3']['items'][4]['widget']['solution'], globals())
for _ in range(200):
    cap = random.randint(1, 4)
    c, od = LRUCache(cap), OrderedDict()
    for _ in range(60):
        k = random.randint(0, 6)
        if random.random() < 0.5:
            got = c.get(k)
            exp = od.get(k, -1)
            if k in od:
                od.move_to_end(k)
            od_ok &= got == exp
        else:
            val = random.randint(0, 99)
            c.put(k, val)
            od[k] = val
            od.move_to_end(k)
            if len(od) > cap:
                od.popitem(last=False)
check('E hw3 LRU solution behaves as OrderedDict with move_to_end', od_ok)

# ---------------------------------------------------------------- F: timing (wide margins)
def best_of(fn, reps=3):
    b = float('inf')
    for _ in range(reps):
        t = time.perf_counter()
        fn()
        b = min(b, time.perf_counter() - t)
    return b


def drain_list(n):
    a = list(range(n))
    while a:
        a.pop(0)


def drain_deque(n):
    a = deque(range(n))
    while a:
        a.popleft()


t1, t4 = best_of(lambda: drain_list(40000)), best_of(lambda: drain_list(160000))
d1, d4 = best_of(lambda: drain_deque(400000)), best_of(lambda: drain_deque(1600000))
check('F list.pop(0) drain is quadratic: 4x the items, over 7x the time', t4 / t1 > 7)
check('F deque.popleft drain is linear: 4x the items, under 7x the time', d4 / d1 < 7)
f1, f4 = best_of(lambda: newest_first(range(30000))), best_of(lambda: newest_first(range(120000)))
g1, g4 = best_of(lambda: app_rev(range(300000))), best_of(lambda: app_rev(range(1200000)))
check('F insert(0, x) loop is quadratic; append then reverse is linear', f4 / f1 > 7 and g4 / g1 < 7)
big = deque(range(2_000_000))
mid = best_of(lambda: [big[1_000_000] for _ in range(200)])
end = best_of(lambda: [big[0] for _ in range(200)])
check('F deque indexing in the middle is far slower than at an end', mid / end > 20)
bl = list(range(2_000_000))
lm = best_of(lambda: [bl[1_000_000] for _ in range(20000)])
le = best_of(lambda: [bl[0] for _ in range(20000)])
check('F list indexing costs the same at any index', lm / le < 3)

print('%d checks passed, %d failed' % (passes, len(fails)))
if fails:
    print('failing checks tied to findings:', sorted({str(f) for _, f in fails if f is not None}))
    untied = [n for n, f in fails if f is None]
    if untied:
        print('UNTIED FAILURES:', untied)
sys.exit(1 if fails else 0)
