"""Second-reader number check for contests level 1 (How contests work): l1 to l4, review-1, homework-1.

Every value is recomputed here by a method independent of the content's own solution, then looked up in the text.
Checks that fail mark a finding in docs/reviews/review-contests-1-2.md and test the corrected value only.
Run: python3 docs/reports/contests-L1-numbers.py
"""
import bisect, collections, itertools, json, math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('contests', 1)
E = lv.expect
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'contests')


def fresh_highs(xs, strict=True):
    best, c = None, 0
    for x in xs:
        if best is None or (x > best if strict else x >= best):
            c += 1
            best = x
    return c


def brute_pairs(xs, k, strict=False):
    return sum(1 for a, b in itertools.combinations(xs, 2) if (a + b < k if strict else a + b <= k))


# ---------- l1 ----------
ex = [3, 1, 4, 1, 5, 9]
E('l1', 'screens[1].canvas.params.lines[24]', fresh_highs(ex))                 # example output 4
E('l1', 'screens[1].explain.text', 2 * 10**5)
E('l1', 'screens[2].hints[2].text', max(ex))
E('l1', 'screens[4].widget.answer', 2 * 10**5)                                 # sum bound
E('l1', 'screens[4].widget.wrong[0].value', 10**4 * 2 * 10**5)                # t times largest n
E('l1', 'screens[4].explain.text', '2 \\cdot 10^9')
E('l1', 'screens[5].prose', 2**31 - 1)
E('l1', 'screens[5].widget.options[0].why', '2 \\cdot 10^{14}')
assert 2 * 10**5 * 10**9 == 2 * 10**14
E('l1', 'screens[5].widget.options[2].why', '4.3 \\cdot 10^9')
assert round(2**32 / 1e9, 1) == 4.3
E('l1', 'screens[5].hints[2].text', '9.2 \\cdot 10^{18}')
assert round(2**63 / 1e18, 1) == 9.2
E('l1', 'screens[6].widget.answer', fresh_highs([7] * 4))
E('l1', 'screens[6].widget.wrong[0].value', fresh_highs([7] * 4, strict=False))
E('l1', 'screens[7].widget.answer', fresh_highs([-5, -3, -4]))
E('l1', 'screens[7].widget.wrong[0].value', sum(1 for i, x in enumerate([-5, -3, -4]) if x > max([0] + [-5, -3, -4][:i])))  # best = 0
E('l1', 'screens[10].feedback.byKey', '2 \\cdot 10^{10}')
assert (2 * 10**5) ** 2 // 2 == 2 * 10**10
E('l1', 'screens[11].widget.options[0].text', '10^{11}')
assert 10**5 * 10**6 == 10**11
E('l1', 'quiz[0].widget.options[0].text', fresh_highs([-10**9]))
E('l1', 'quiz[1].widget.answer', 3 * 10**5 - (10**4 - 1))
E('l1', 'quiz[1].widget.wrong[1].value', 3 * 10**5 // 10**4)
E('l1', 'quiz[1].explain.text', 9999)
E('l1', 'quiz[2].feedback.correct', '10^{12}')
E('l1', 'quiz[3].widget.answer', fresh_highs([2, 2, 1, 3], strict=False))
E('l1', 'quiz[3].widget.wrong[0].value', fresh_highs([2, 2, 1, 3]))
# finding: the hook hint names lines 13 and 15 of a console that shows no numbers; the fix rewords it
E('l1', 'screens[1].hints[2].text', 'The line with $1 \\le n \\le 2 \\cdot 10^5$ bounds $n$')

# ---------- l2 ----------
n = 2 * 10**5
E('l2', 'screens[0].hints[2].text', '1.3 \\cdot 10^{15}')
assert round(n**3 / 6 / 1e15, 1) == 1.3
E('l2', 'screens[0].hints[2].text', '2 \\cdot 10^{10}')
E('l2', 'screens[1].widget.answer', math.isqrt(10**8))
E('l2', 'screens[1].widget.wrong[0].value', math.isqrt(10**7))
lo, hi = 1, 10**8                      # largest n with n log2 n <= 1e8, by bisection
while lo < hi:
    mid = (lo + hi + 1) // 2
    if mid * math.log2(mid) <= 1e8:
        lo = mid
    else:
        hi = mid - 1
E('l2', 'screens[1].widget.wrong[2].value', lo)
E('l2', 'screens[1].canvas.state.points[1].y', round(1000 * math.log2(1000)))
E('l2', 'screens[1].explain.text', '3.5 \\cdot 10^6')
assert round(n * math.log2(n) / 1e6, 1) == 3.5
E('l2', 'screens[2].hints[1].text', 500**3 / 1e8, fmt='{:.2f} \\cdot 10^8')
E('l2', 'screens[2].hints[1].text', '2.5 \\cdot 10^7')
assert 5000**2 == 25 * 10**6
E('l2', 'screens[3].widget.answer', 2**20)
E('l2', 'screens[3].widget.wrong[0].value', 20**2)
E('l2', 'screens[3].widget.wrong[2].value', 20**3)
E('l2', 'screens[3].explain.text', '2 \\cdot 10^7')
assert round(2**20 * 20 / 1e7) == 2
E('l2', 'screens[4].widget.answer', math.comb(5000, 2))
E('l2', 'screens[4].widget.wrong[0].value', 5000**2)
E('l2', 'screens[4].widget.wrong[1].value', 5000 * 4999)
E('l2', 'screens[5].widget.answer', math.ceil(math.log2(10**9 + 1)))
E('l2', 'screens[5].hints[2].text', 2**30)
E('l2', 'screens[5].widget.wrong[1].value', round(math.sqrt(1e9)))
E('l2', 'screens[5].explain.text', '6 \\cdot 10^6')
assert n * 30 == 6 * 10**6
E('l2', 'screens[6].widget.options[1].text', '4 \\cdot 10^6')
assert 10**4 * 20**2 == 4 * 10**6
E('l2', 'screens[6].widget.options[2].text', '4 \\cdot 10^{14}')
assert 10**4 * (2 * 10**5)**2 == 4 * 10**14
E('l2', 'screens[8].widget.options[0].text', '2 \\cdot 10^7')
assert round(10**6 * math.log2(10**6) / 1e7) == 2
E('l2', 'screens[9].explain.text', 26)
assert 2**26 <= 10**8 < 2**27
E('l2', 'screens[9].explain.text', 464)
assert 464**3 <= 10**8 < 465**3
E('l2', 'screens[9].feedback.byKey', '1.005 \\cdot 10^8')
assert round(465**3 / 1e8, 3) == 1.005
E('l2', 'screens[9].explain.text', '4.5 \\cdot 10^6')
assert round(lo / 1e6, 1) == 4.5
# problem H: the size case by an independent bisect count, and the hand case by brute force
r = random.Random(5)
xs = [r.randint(-10**9, 10**9) for _ in range(200000)]
a = sorted(xs)
cnt = sum(max(0, bisect.bisect_right(a, 0 - v, i + 1) - (i + 1)) for i, v in enumerate(a))
E('l2', 'screens[10].widget.tests[8].expect', cnt)
E('l2', 'screens[10].widget.tests[6].expect', brute_pairs([3, 1, 4, 1, 5, 9, 2, 6], 7))
E('l2', 'screens[10].widget.tests[4].expect', brute_pairs([-3, -1, 4, 0], -1))
E('l2', 'screens[11].widget.options[1].why', '5 \\cdot 10^{11}')
assert 10**12 // 2 == 5 * 10**11
E('l2', 'quiz[0].widget.options[0].text', '10^6')
E('l2', 'quiz[0].explain.text', 20 - 3)
E('l2', 'quiz[2].explain.text', round(math.log2(10**6), 1))
E('l2', 'quiz[3].feedback.correct', '6.4 \\cdot 10^7')
assert 400**3 == 64 * 10**6
# finding: problem F has no n; the corrected prose names q and the value bound
E('l2', 'screens[5].prose', 'up to $2 \\cdot 10^5$ queries')

# ---------- l3 ----------
toks = '3 / 2 / 5 7 / 1 / -4 / 3 / 1 2 3'.replace('/', ' ').split()
E('l3', 'screens[1].prose', 'ten tokens')
assert len(toks) == 10
E('l3', 'screens[1].widget.answer', 1 + 1 + 2 + 1 + 1)              # t, n1, two values, n2, one value
E('l3', 'screens[6].widget.options[0].text', '10 5')
assert (4 + 1 + 5, max(4, 1, 5)) == (10, 5)
E('l3', 'screens[6].explain.text', '`2 2`')
E('l3', 'screens[8].widget.tests[9].expect', sum(range(200000)))
E('l3', 'screens[9].widget.tests[2].expect', 3 * 10**9)
E('l3', 'screens[10].hints[1].text', '5 \\cdot 10^9')
E('l3', 'quiz[2].widget.answer', len('2\n\n5 -3'.split()))
# finding: on the trap screen "line 3" needs numbered console lines (layout fix sets numbers: true)
l3doc = json.load(open(os.path.join(SRC, 'l3-fast-io.json')))
lv._rec(l3doc['screens'][6]['canvas']['params'].get('numbers') is True, 'l3 screens[6].canvas.params.numbers is true', 'missing: the screen names console lines by number')

# ---------- l4 ----------
pre = json.load(open(os.path.join(SRC, 'l4-stress-testing.json')))['screens'][7]['widget']['prelude']
g = {}
exec(pre, g)
rng = random.Random(1)
rows = []
for t in range(5):
    case = g['gen_pairs'](rng)
    rows.append((case, g['fast_strict']((list(case[0]), case[1])), g['brute_pairs'](case)))
first = next(i + 1 for i, (c, f, b) in enumerate(rows) if f != b)
E('l4', 'screens[1].widget.answer', first)
for i, (c, f, b) in enumerate(rows):
    line = lv.text('l4', f'screens[1].canvas.controls[0].frames[4].lines[{i + 2}]')
    ok = str(c[0]) in line and f'k={c[1]}' in line and line.split()[-2 if f != b else -1] == str(b)
    lv._rec(ok, f'l4 stress frame row {i + 1} = {c} fast {f} brute {b}', '' if ok else line)
# generator A finds nothing in 100,000 trials on each of four seeds (seeds 1, 2, 3, 7 as the author reported)
for seed in (1, 2, 3, 7):
    rr = random.Random(seed)
    hit = 0
    for _ in range(100000):
        m = rr.randint(1, 6)
        v = [rr.randint(1, 10**9) for _ in range(m)]
        k = rr.randint(2, 2 * 10**9)
        if any(p + q == k for p, q in itertools.combinations(v, 2)):
            hit += 1
    lv._rec(hit == 0, f'l4 screens[3] gen A seed {seed}: no exact tie in 100,000 trials', f'{hit} ties')
E('l4', 'screens[4].widget.options[3].why', 1 + 1)
assert brute_pairs([6, 1, 1], 3) == brute_pairs([6, 1, 1], 3, strict=True) == 1
assert brute_pairs([1, 1], 2) == 1 and brute_pairs([1, 1], 2, strict=True) == 0
E('l4', 'screens[9].explain.text', round(100.50 - 99.25, 2), fmt='£{:.2f}')
E('l4', 'quiz[2].widget.answer', brute_pairs([2, 3, 3], 6, strict=True))
E('l4', 'quiz[2].widget.wrong[0].value', brute_pairs([2, 3, 3], 6))

# ---------- review-1 ----------
E('review', 'items[0].widget.options[0].text', '10^{18}')
E('review', 'items[1].widget.options[0].text', '4.4 \\cdot 10^7')
assert round(2000**2 * math.log2(2000) / 1e7, 1) == 4.4
E('review', 'items[1].widget.options[1].why', 'eighty times')
assert 2000**3 // 10**8 == 80
E('review', 'items[1].explain.text', round(math.log2(2000)))
E('review', 'items[2].widget.answer', 1 + 1 + 3)
E('review', 'items[3].prose', brute_pairs([5, 5, 1], 10))
E('review', 'items[3].prose', brute_pairs([5, 5, 1], 10, strict=True))
E('review', 'items[4].widget.options[0].text', '10^{10}')
assert 10**4 * 10**6 == 10**10
E('review', 'items[5].feedback.correct', '4 \\cdot 10^{10}')
E('review', 'items[8].widget.answer', 10**5 * round(math.log2(10**6)))
E('review', 'items[8].widget.wrong[0].value', 10**5 * 10**6)

# ---------- homework-1 ----------
r = random.Random(22)
zs = [r.randint(-1000, 1000) for _ in range(200000)]
c = collections.Counter(zs)
pairs0 = sum(c[v] * c[-v] for v in c if v > 0) + math.comb(c[0], 2)
E('homework', 'items[0].widget.tests[9].expect', pairs0)
E('homework', 'items[0].widget.tests[10].expect', math.comb(200000, 2))
E('homework', 'items[0].explain.text', math.comb(200000, 2))
r = random.Random(31)
big = [r.choice(['T%d' % i for i in range(8)]) for _ in range(200000)]
best = 0                                 # independent: for each left end, extend while <= 4 distinct (windows are short here)
for left in range(len(big)):
    seen = set()
    j = left
    while j < len(big) and (big[j] in seen or len(seen) < 4):
        seen.add(big[j])
        j += 1
    best = max(best, j - left)
E('homework', 'items[1].widget.tests[9].expect', best)
r = random.Random(41)
xs = [r.randint(-10**9, 10**9) for _ in range(200000)]
qs = []
for _ in range(200000):
    p, q = r.randint(1, 200000), r.randint(1, 200000)
    qs.append((min(p, q), max(p, q)))
pre = [0, *itertools.accumulate(xs)]
out = [pre[q] - pre[p - 1] for p, q in qs]
E('homework', 'items[2].widget.tests[5].expect', out[0])
E('homework', 'items[2].widget.tests[5].expect', out[-1])
E('homework', 'items[2].widget.tests[5].expect', sum(out))
E('homework', 'items[2].feedback.byKey', '10^{10}')
assert 1e10 < 2e5 * 2e5 / 3 < 1e11 / 5
E('homework', 'items[6].widget.answer', 2 * 10**5 * 2 * 10**5)
E('homework', 'items[6].widget.wrong[1].value', 2 * 2 * 10**5)
E('homework', 'items[7].explain.text', math.comb(6, 2))
E('homework', 'items[7].explain.text', math.comb(200000, 2))
E('homework', 'items[4].widget.model', '2 \\cdot 10^{10}')
rub = json.load(open(os.path.join(SRC, 'homework-1.json')))['items'][4]['widget']['rubric']
lv._rec(sum(x['points'] for x in rub) == 10, 'homework items[4] rubric totals 10 points', '')
# finding: the count-in-range feedback leaves out the factor 2 its own explanation states
steps = 2 * 10**5 * math.log2(2 * 10**5) + 2 * 2 * 10**5 * math.log2(2 * 10**5)
E('homework', 'items[5].feedback.correct', '1.1 \\cdot 10^7')
assert round(steps / 1e7, 1) == 1.1
# finding: test 8 of problem W has k = 5 > n = 3; the fix widens the constraint to k <= 2·10^5
E('homework', 'items[1].canvas.params.lines[2]', '1 ≤ k ≤ 2·10⁵')

lv.check_wrongs()
lv.report()
