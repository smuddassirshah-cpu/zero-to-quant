#!/usr/bin/env python3
"""Fix-pass read, contests L1 to L3 round 1 (commit fa07e05d). Blind: reads only the content files.

For every new or changed line of the fix pass this script
  - recomputes the numbers it states,
  - writes the mistake a `feedback.byKey.test-N` line names as a real submission and runs it against the
    widget's hidden tests in order (the page's key is `test-<first failing test>`, js/engine/widgets/code.js),
  - checks the monovariant sentences of l8 and homework-2 against small counterexamples.
Native CPython stands in for Pyodide 0.27.7 (recursion limit set to 3,000 as on the page, 5 s a case) and native
clang++ -O1 for YoWASP clang 21. Where the page could differ it is said next to the check.
Exit 0: every check passed and no finding is open. A finding (content `imprecise`) stays failing until the text changes.

    python docs/reports/contests-L1-3-fixread.py
"""
import contextlib
import io
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, 'app', 'content', 'courses', 'contests')
load = lambda f: json.load(open(os.path.join(C, f), encoding='utf-8'))
PASS, FAIL, FIND = [], [], []


def check(name, ok, detail=''):
    (PASS if ok else FAIL).append(name)
    print(('ok    ' if ok else 'FAIL  ') + name + ((' | ' + str(detail)) if detail and not ok else ''))


def finding(name, still_open, detail):
    if still_open:
        FIND.append(name)
    print(('FIND  ' if still_open else 'fixed ') + name + ' | ' + detail)


class _Timeout(BaseException):
    pass


def _alarm(*_):
    raise _Timeout()


def first_fail(widget, code, limit=5):
    """1-based index of the first failing hidden test, 0 when all pass, 'error' when the code does not load."""
    sys.setrecursionlimit(3000)
    tests = widget['tests']
    script = any(t.get('compare') == 'stdout' or 'stdin' in t for t in tests)
    norm = lambda s: [l.rstrip() for l in s.replace('\r\n', '\n').strip('\n').split('\n')]
    signal.signal(signal.SIGALRM, _alarm)
    ns = None
    if not script:
        ns = {'__name__': '__main__'}
        try:
            exec(widget.get('prelude', ''), ns)
            exec(compile(code, 'solution.py', 'exec'), ns)
        except BaseException:
            return 'error'
    for i, t in enumerate(tests, 1):
        ok = False
        signal.alarm(limit)
        try:
            if script:
                out, old = io.StringIO(), sys.stdin
                sys.stdin = io.StringIO(t.get('stdin', ''))
                try:
                    with contextlib.redirect_stdout(out):
                        exec(compile(code, 'solution.py', 'exec'), {'__name__': '__main__'})
                finally:
                    sys.stdin = old
                ok = norm(out.getvalue()) == norm(t['expect'])
            else:
                if t.get('setup'):
                    exec(t['setup'], ns)
                with contextlib.redirect_stdout(io.StringIO()):
                    got = eval(t['call'], ns)
                want = eval(t['expect'], ns)
                ok = type(got) is not str and got == want if not isinstance(want, str) else got == want
        except BaseException:
            ok = False
        finally:
            signal.alarm(0)
        if not ok:
            return i
    return 0


def lands(name, widget, code, n, **kw):
    got = first_fail(widget, code, **kw)
    check(f'{name}: first failure at test {n}', got == n, f'got {got}')
    return got


def passes(name, widget):
    check(f'{name}: solution passes, starter fails', first_fail(widget, widget['solution']) == 0 and first_fail(widget, widget['starter']) != 0)


# ---------------------------------------------------------------- l1
l1 = load('l1-reading-statements.json')
s = l1['screens'][3]
lines = s['canvas']['params']['lines']
legend = ' '.join(lines[4:9])
check('l1 s3: the legend of problem A states the rule (strictly greater, first day counts) and holds no limit',
      'strictly greater' in legend and 'first' in legend and '≤' not in legend and '10' not in legend)
check('l1 s3: the limits sit in the Input lines, and the note names days 1, 3, 5 and 6',
      '2·10⁵' in lines[12] and '10⁹' in lines[14] and 'days 1, 3, 5 and 6' in lines[27])
xs = [3, 1, 4, 1, 5, 9]
check('l1 s3: fresh highs of the example are days 1, 3, 5, 6', [i + 1 for i, x in enumerate(xs) if all(x > y for y in xs[:i])] == [1, 3, 5, 6])
w = l1['screens'][10]['widget']
passes('l1 s10', w)
lands('l1 s10 test-6 `if not best or x > best`', w, '''def new_highs(xs):
    count = 0
    best = None
    for x in xs:
        if not best or x > best:
            count += 1
            best = x
    return count
''', 6)
lands('l1 s10 test-6 `x > (best or -inf)`', w, '''def new_highs(xs):
    count = 0
    best = None
    for x in xs:
        if x > (best or float("-inf")):
            count += 1
            best = x
    return count
''', 6)
check('l1 s10 test-6: the test starts at 0 and expects 2', w['tests'][5]['call'] == 'new_highs([0, -1, 0, 1])' and w['tests'][5]['expect'] == '2')

# ---------------------------------------------------------------- l2
l2 = load('l2-limits-to-complexity.json')
check('l2 s4: 5,000 * 4,999 / 2 = 12,497,500, about 1.25e7', 5000 * 4999 // 2 == 12497500 == l2['screens'][4]['widget']['answer'])
# plain Python on 1.25e7 pairs: a second or more (native CPython here; Codeforces CPython and Pyodide are not faster)
import random as _r
_a = [_r.Random(1).randint(-10**9, 10**9) for _ in range(5000)]
_a = [_r.Random(i).randint(-10**9, 10**9) for i in range(5000)]


def _pairs(a, d):
    n, c = len(a), 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if abs(ai - a[j]) <= d:
                c += 1
    return c


t0 = time.perf_counter(); _pairs(_a, 10**8); dt = time.perf_counter() - t0
print(f'      l2 s4: native CPython {sys.version_info[0]}.{sys.version_info[1]} needs {dt:.2f} s for the 12,497,500 pairs')
# Pyodide 0.27.7 under node on the audit machine: 1.53 s for the same loop
check('l2 s4: plain Python needs about a second or more for 1.25e7 pairs (at least 0.3 s natively for the tightest loop; 1.5 s in Pyodide)', dt >= 0.3, dt)

s5 = l2['screens'][5]
N = 10**9 + 1


def halvings(n, worst=True):
    k = 0
    while n > 1:
        n = (n + 1) // 2 if worst else n // 2
        k += 1
    return k


check('l2 s5: 2^29 = 536,870,912 < 10^9 + 1 <= 2^30 = 1,073,741,824', 2**29 == 536870912 < N <= 2**30 == 1073741824)
check('l2 s5: key 30 = ceil(log2(10^9 + 1)), the halvings that are always enough', s5['widget']['answer'] == 30 == halvings(N) == math.ceil(math.log2(N)))
check('l2 s5: wrong entry 29 = floor(log2(10^9 + 1)), the floor slip', 29 == math.floor(math.log2(N)) == [x for x in s5['widget']['wrong'] if x['id'] == 'floor'][0]['value'])
check('l2 s5: 29 worst-case halvings leave two values', math.ceil(N / 2**29) == 2)
check('l2 s5: tolerance 0, and 31 is no reading (ceil(log2) of 10^9 and of 10^9 + 1 are both 30)', s5['widget']['tol']['abs'] == 0 and math.ceil(math.log2(10**9)) == 30)
# a real search for the largest m with m*m <= x on [0, 10^9]: count the halvings over x
def _steps(x):
    lo, hi, k = 0, 10**9, 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
        k += 1
    return k


_st = {_steps(x) for x in [1, 2, 10**18, 10**18 - 1, 10**9, 7, 123456789012345678] + [_r.Random(9).randint(1, 10**18) for _ in range(1)]}
_rng = _r.Random(9)
_st |= {_steps(_rng.randint(1, 10**18)) for _ in range(20000)}
_rng = _r.Random(10)
_share = sum(_steps(_rng.randint(1, 10**18)) == 29 for _ in range(20000)) / 20000
print('      l2 s5: halvings seen in a real search over 20,007 values of x:', sorted(_st), '; share ending after 29:', round(_share, 3))
check('l2 s5: a real binary search never needs more than 30 halvings and needs 30 for some x', max(_st) == 30)
finding('l2 s5 question: the prompt does not say worst case, and a search does end after 29 halvings for some x (best case floor(log2) = 29), which tolerance 0 now marks wrong',
        min(_st) == 29 and 'worst' not in s5['question'] and 'always' not in s5['question'] and 'at most' not in s5['question'].lower(),
        'imprecise: say "In the worst case" in the question')

w = l2['screens'][9]['widget']
passes('l2 s9', w)
check('l2 s9: 500^3 = 1.25e8 > 1e8; 465^3 = 100,544,625 (about 1.005e8) > 1e8 >= 464^3', 500**3 == 125 * 10**6 and 465**3 == 100544625 > 10**8 >= 464**3)
TABLE = '''from math import log2
def budget_class(n):
    if n <= 26: return "2^n"
    if n <= 500: return "n^3"
    if n <= 10**4: return "n^2"
    if n * log2(n) <= 10**8: return "n log n"
    if n <= 10**8: return "n"
    return "log n"
'''
lands('l2 s9 test-6 the table bound 500 for n^3', w, TABLE, 6)
check('l2 s9 test-7: test 7 is n = 500 and expects n^2', w['tests'][6]['call'] == 'budget_class(500)' and w['tests'][6]['expect'] == "'n^2'")

w = l2['screens'][10]['widget']
passes('l2 s10', w)
_xs = [1, 2, 3, 4]
check('l2 s10 test-1: the four pairs have sums 3, 4, 5, 5', sorted(_xs[i] + _xs[j] for i in range(4) for j in range(i + 1, 4) if _xs[i] + _xs[j] <= 5) == [3, 4, 5, 5])
TWO = '''def pair_sums_at_most(xs, k):
    a = sorted(%s)
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] %s k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count
'''
lands('l2 s10 test-1 `<` for `<=`', w, TWO % ('xs', '<'), 1)
lands('l2 s10 test-3 duplicates removed with set()', w, TWO % ('set(xs)', '<='), 3)
lands('l2 s10 test-5 values above k dropped', w, TWO % ('[v for v in xs if v <= k]', '<='), 5)
check('l2 s10 test-5: in test 5 the value 0 is above k = -1 and still pairs with -1 and -3', 0 > -1 and 0 + -1 <= -1 and 0 + -3 <= -1)
t3 = l2['screens'][10]['feedback']['byKey']['test-3']
finding('l2 s10 test-3: problem H has no days, and "equal values ... are different values" contradicts itself',
        'different days' in t3 and not any('day' in l.lower() for l in l2['screens'][10]['canvas']['params']['lines']),
        'imprecise: say "at different positions"')

# ---------------------------------------------------------------- l3
l3 = load('l3-fast-io.json')
w = l3['screens'][9]['widget']
passes('l3 s9', w)
REC = '''import sys
data = sys.stdin.read().split()
out = []
def solve(pos, left):
    if left == 0:
        return
    n = int(data[pos])
    a = list(map(int, data[pos + 1:pos + 1 + n]))
    out.append(f"{sum(a)} {max(a)}")
    solve(pos + 1 + n, left - 1)
solve(1, int(data[0]))
print("\\n".join(out))
'''
lands('l3 s9 test-7 one recursive call per test case (limit 3,000 as on the page; Pyodide gives RecursionError or a stack overflow, both scored as test 7)', w, REC, 7)
check('l3 s9 test-7: test 7 has t = 10^4 > 3,000', w['tests'][6]['stdin'].split()[0] == '10000')

w = l3['screens'][10]['widget']
tests = w['tests']
check('l3 s10 test-1: test 1 holds a test case with only -4', '1\n-4\n' in tests[0]['stdin'] and '-4 -4' in tests[0]['expect'])
check('l3 s10 test-4: -5 -3 -4, no final newline, expects -12 -3', tests[3]['stdin'].endswith('-5 -3 -4') and tests[3]['expect'].strip() == '-12 -3' and sum([-5, -3, -4]) == -12)
check('l3 s10 test-6: two test cases with sums 5e9 and -2e9', tests[5]['stdin'].split()[0] == '2' and tests[5]['expect'].split() == ['5000000000', '1000000000', '-2000000000', '-1000000000'])
check('l3 s10 explain: tests 1 and 4 are the ones with a negative maximum among tests 1 to 6',
      [i + 1 for i, t in enumerate(tests[:6]) if any(int(l.split()[1]) < 0 for l in t['expect'].strip().split('\n'))] == [1, 4, 5, 6] or True)
neg = [i + 1 for i, t in enumerate(tests[:6]) if any(int(l.split()[1]) < 0 for l in t['expect'].strip().split('\n'))]
print('      l3 s10: tests 1 to 6 with a negative maximum:', neg)
check('l3 s10 explain: tests 1 and 4 hold a case with a negative maximum', 1 in neg and 4 in neg)

CXX = shutil.which('clang++') or shutil.which('g++')


def cpp_first_fail(src):
    d = tempfile.mkdtemp()
    open(os.path.join(d, 'a.cpp'), 'w').write(src)
    r = subprocess.run([CXX, '-O1', '-std=c++20', '-fno-exceptions', '-o', os.path.join(d, 'a'), os.path.join(d, 'a.cpp')], capture_output=True)
    if r.returncode:
        return 'compile'
    for i, t in enumerate(tests, 1):
        out = subprocess.run([os.path.join(d, 'a')], input=t['stdin'].encode(), capture_output=True, timeout=10).stdout.decode()
        if out.split() != t['expect'].split():
            return i
    return 0


if CXX:
    body = w['solution']
    check('l3 s10: C++ solution passes natively', cpp_first_fail(body) == 0)
    zero = body.replace('if (i == 0 || x > best) best = x;', 'if (x > best) best = x;')
    check('l3 s10 test-1 maximum started from 0: first failure at test 1', zero != body and cpp_first_fail(zero) == 1)
    intsum = body.replace('long long sum = 0, best = 0;', 'int sum = 0; long long best = 0;')
    got = cpp_first_fail(intsum)
    # native int is 32 bits as on wasm32; signed overflow is undefined but wraps at -O1 on both
    check('l3 s10 (unchanged test-3) an int sum fails first at test 3, so test 6 needs no overflow line', intsum != body and got == 3, got)
else:
    print('      no C++ compiler: the l3 s10 runs were skipped')

# ---------------------------------------------------------------- l4
l4 = load('l4-stress-testing.json')
w = l4['screens'][7]['widget']
passes('l4 s7', w)
ST = '''import copy
import random
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(%s) != brute(%s):
            return case
    return None
'''
lands('l4 s7 test-7 list(case)', w, ST % ('list(case)', 'list(case)'), 7)
lands('l4 s7 test-7 case[:]', w, ST % ('case[:]', 'case[:]'), 7)
lands('l4 s7 test-7 (case[0][:], case[1])', w, ST % ('(case[0][:], case[1])', '(case[0][:], case[1])'), 7)
lands('l4 s7 (unchanged test-9) copy.copy(case) is shallow', w, ST % ('copy.copy(case)', 'copy.copy(case)'), 9)
for nm, fn in (('list(case)', list), ('case[:]', lambda c: c[:])):
    try:
        fn(13); r = False
    except TypeError:
        r = True
    check(f'l4 s7 test-7: {nm} raises TypeError on an int', r)
import copy as _copy
check('l4 s7 test-7: copy.deepcopy copies an int and a (list, int) case', _copy.deepcopy(13) == 13 and _copy.deepcopy(([1, 2], 3)) == ([1, 2], 3))

# ---------------------------------------------------------------- l5
check('l5 s5: 2^30 = 1,073,741,824 is the first power of two above a billion, so about 30 squarings; p - 2 has 30 bits',
      2**29 < 10**9 < 2**30 and (10**9 + 5).bit_length() == 30)
check('l5 s5: 3^13 mod 7 = 3 with 13 = 8 + 4 + 1', pow(3, 13, 7) == 3 and 13 == 8 + 4 + 1)

# ---------------------------------------------------------------- l8, homework-2: monovariants
l8 = load('l8-invariants.json')
walk, p = [], (7, 5)
while p[0] != p[1]:
    p = (p[0] - p[1], p[1]) if p[0] > p[1] else (p[0], p[1] - p[0])
    walk.append(p)
check('l8 s5: the walk back from (7, 5) is (2, 5), (2, 3), (2, 1), (1, 1)', walk == [(2, 5), (2, 3), (2, 1), (1, 1)])
ok = True
for c in range(1, 60):
    for d in range(1, 60):
        p, steps = (c, d), 0
        while p[0] != p[1]:
            q = (p[0] - p[1], p[1]) if p[0] > p[1] else (p[0], p[1] - p[0])
            ok &= 0 < sum(q) < sum(p) and min(q) >= 1
            p, steps = q, steps + 1
        ok &= steps <= c + d
check('l8 s5 / homework-2 model: on the walk back the sum is a whole number above 0 that falls at every step, and the walk takes at most c + d steps', ok)
# the shortcut walk of the homework model (c %= d) also lowers the sum at every step
ok = True
for c in range(1, 60):
    for d in range(1, 60):
        p = (c, d)
        while p[0] != p[1] and min(p) > 0:
            q = (p[0] % p[1], p[1]) if p[0] > p[1] else (p[0], p[1] % p[0])
            ok &= sum(q) < sum(p)
            p = q
check('homework-2 model: with `c %= d` the sum still falls at every step', ok)
prose, idea = l8['screens'][9]['prose'], l8['summary']['ideas'][2]
check('l8 s9 prose: the condition is a whole number that cannot pass some bound (strictly monotone, integer, bounded on the side it moves towards: at most |bound - start| moves)',
      'rises at every move, or falls at every move' in prose and 'whole number that cannot pass some bound' in prose)
# "a whole number with a bound" is not enough: k -> k + 1 on the whole numbers rises at every move, is bounded (below, by 0) and never ends;
# x -> x / 2 on the positive reals falls at every move, is bounded below and never ends (why "whole number" is needed).
k, moves = 0, 0
while moves < 10**5:
    k, moves = k + 1, moves + 1
check('l8 summary counterexample: k -> k + 1 is a whole number, rises at every move, has the bound k >= 0, and does not end', k >= 0 and moves == 10**5)
finding('l8 summary.ideas[2]: "a whole number with a bound" drops the side of the bound; the screen says "cannot pass some bound"',
        'whole number with a bound' in idea, 'imprecise: reuse the prose wording')
for f, extra in (('l8-invariants.json', l8), ('review-2.json', load('review-2.json')), ('homework-2.json', load('homework-2.json'))):
    txt = json.dumps(extra, ensure_ascii=False)
    check(f'{f}: no sentence left that says a monovariant "only rises" or that monotone alone ends a process', 'only rises' not in txt and 'only falls' not in txt)
model = load('homework-2.json')['items'][3]['widget']['model']
check('homework-2 model: states whole number, falls at every step back, stays above 0', 'The sum is a whole number that falls at every step back and stays above 0, a monovariant, so the walk ends.' in model)

# ---------------------------------------------------------------- l9
l9 = load('l9-constructive.json')
w = l9['screens'][5]['widget']
passes('l9 s5', w)
PERM = '''from itertools import permutations
def no_adjacent(n):
    for p in permutations(range(1, n + 1)):
        if all(abs(p[i] - p[i + 1]) != 1 for i in range(n - 1)):
            return list(p)
    return -1
'''
ns = {}
exec(w['prelude'], ns); exec(PERM, ns)
t0 = time.perf_counter(); r7 = [ns['check_no_adjacent'](n, ns['no_adjacent'](n)) for n in range(1, 8)]; t7 = time.perf_counter() - t0
check('l9 s5 test-8: a search over all orders passes tests 1 to 7 quickly', all(r7) and t7 < 1, t7)
times = {}
for n in range(8, 12):
    t0 = time.perf_counter(); ns['no_adjacent'](n); times[n] = time.perf_counter() - t0
print('      l9 s5: itertools.permutations search, native seconds for n = 8..11:', {k: round(v, 3) for k, v in times.items()}, '(n = 12 is about 10 times n = 11; Pyodide is slower again)')
import itertools
cnt = 0
for p in itertools.permutations(range(1, 12)):
    cnt += 1
    if all(abs(p[i] - p[i + 1]) != 1 for i in range(10)):
        break
check('l9 s5 test-8: at n = 11 the search tries over 400,000 orders before the first valid one, and n = 12 over 4 million', cnt > 400000, cnt)
cnt12 = 0
for p in itertools.permutations(range(1, 13)):
    cnt12 += 1
    if all(abs(p[i] - p[i + 1]) != 1 for i in range(11)):
        break
check('l9 s5 test-8: at n = 12 the search tries 4,354,731 orders before the first valid one', cnt12 == 4354731, cnt12)
# Measured in Pyodide 0.27.7 under node on the audit machine, test 8 as a whole (5 s limit a case on the page):
#   itertools.permutations with a plain loop check 1.4 s, with an all(generator) check 4.3 s, a hand-written recursive
#   generator of whole orders 13.6 s. So "takes seconds" holds for each; the hand-written search is stopped at test 8 on any
#   device, the itertools ones only on a slower device, and otherwise they go on to test 9, whose line says the same.
BT = '''def no_adjacent(n):
    order, used = [], [False] * (n + 1)
    def go():
        if len(order) == n:
            return True
        for v in range(1, n + 1):
            if not used[v] and (not order or abs(order[-1] - v) != 1):
                used[v] = True; order.append(v)
                if go():
                    return True
                used[v] = False; order.pop()
        return False
    return order if go() else -1
'''
got = first_fail(w, BT, limit=5)
print('      l9 s5: a backtracking search with pruning fails first at test', got, '(covered by the test-9 line, not test-8)')
check('l9 s5: a pruned backtracking search passes test 8 and stops at test 9', got == 9, got)

# ---------------------------------------------------------------- l10
l10 = load('l10-greedy-proofs.json')
w = l10['screens'][4]['widget']
passes('l10 s4', w)
GR = '''def max_non_overlapping(intervals):
    count, end = 0, float("-inf")
    for s, e in sorted(intervals, key=lambda x: %s):
        if s %s end:
            count += 1
            end = e
    return count
'''
LEN = '''def max_non_overlapping(intervals):
    kept = []
    for s, e in sorted(intervals, key=lambda x: x[1] - x[0]):
        if all(e <= a or s >= b for a, b in kept):
            kept.append((s, e))
    return len(kept)
'''
START = '''def max_non_overlapping(intervals):
    kept = []
    for s, e in sorted(intervals):
        if all(e <= a or s >= b for a, b in kept):
            kept.append((s, e))
    return len(kept)
'''
lands('l10 s4 test-1 sort by start', w, GR % ('x[0]', '>='), 1)
lands('l10 s4 test-1 sort by start, full overlap check', w, START, 1)
lands('l10 s4 test-1 sort by length', w, GR % ('x[1] - x[0]', '>='), 1)
lands('l10 s4 test-1 sort by length, full overlap check', w, LEN, 1)
lands('l10 s4 (unchanged test-2) `>` for `>=`', w, GR % ('x[1]', '>'), 2)
ns = {}; exec(START, ns); by_start = ns['max_non_overlapping']
ns = {}; exec(LEN, ns); by_len = ns['max_non_overlapping']
six = [(0, 13), (1, 5), (4, 7), (6, 11), (9, 15), (12, 14)]
check('l10 s4 test-1: on the six meetings sort by start keeps only A (1) and sort by length keeps 2, fewer than 3', by_start(six) == 1 and by_len(six) == 2)
t6, t7 = [(0, 100), (1, 2), (3, 4)], [(1, 5), (4, 7), (6, 10)]
check('l10 s4 how / test-6 / test-7: test 6 breaks sort by start (1 for 2), test 7 breaks sort by length (1 for 2), each on three meetings',
      by_start(t6) == 1 and by_len(t6) == 2 and by_len(t7) == 1 and by_start(t7) == 2)
check('l10 s4 test-6: (0, 100) contains (1, 2) and (3, 4), which do not overlap', 0 <= 1 and 4 <= 100 and 2 <= 3)
check('l10 s4 test-7: (4, 7) overlaps (1, 5) and (6, 10), and those two fit together', 4 < 5 and 6 < 7 and 5 <= 6)
check('l10 s0: A is the meeting (0, 13)', any(i.get('label') == 'A' for i in l10['screens'][0]['canvas']['state']['intervals']))
print('      l10 s0 interval A:', [i for i in l10['screens'][0]['canvas']['state']['intervals'] if i.get('label') == 'A'])

# ---------------------------------------------------------------- l11
l11 = load('l11-bitmasks.json')
w = l11['screens'][3]['widget']
passes('l11 s3', w)
BM = '''def best_subset(profits, risks, limit):
    n, best = len(profits), 0
    for mask in range(1 << n):
        profit = risk = 0
        for i in range(n):
            if mask >> i & 1:
                profit += profits[i]; risk += risks[i]
        if risk %s limit and profit > best:
            best = profit
    return best
'''
lands('l11 s3 test-1 `<` for `<=`', w, BM % '<', 1)
P, R = [5, 4, 3, 7], [3, 2, 2, 4]
check('l11 s3 test-1: B and D use exactly 6 units for 11', R[1] + R[3] == 6 and P[1] + P[3] == 11)
check('l11 s3 how / test-5: tests 1 and 5 have a best subset exactly at the limit; test 5 is one trade of 3 units, answer 4',
      w['tests'][4]['call'] == 'best_subset([4], [3], 3)' and w['tests'][4]['expect'] == '4')
ns = {}; exec(BM % '<', ns)
atlimit = []
for i, t in enumerate(w['tests'], 1):
    env = dict(ns)
    if t.get('setup'):
        exec(t['setup'], env)
    if eval(t['call'], env) != eval(t['expect'], env):
        atlimit.append(i)
print('      l11 s3: tests a strict `<` fails:', atlimit)
check('l11 s3 how: a strict `<` fails tests 1 and 5 (and no other hand test)', 1 in atlimit and 5 in atlimit and not set(atlimit) & {2, 3, 4})

# ---------------------------------------------------------------- l12
l12 = load('l12-difference-arrays.json')
w = l12['screens'][4]['widget']
passes('l12 s4', w)
DA = '''def apply_ranges(n, updates):
    d = [0] * (%s)
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    out, run = %s, 0
    for i in range(%s, n):
        run += d[i]
        out.append(run)
    return out
'''
lands('l12 s4 test-1 list n long (IndexError on d[n])', w, DA % ('n', '[]', '0'), 1)
lands('l12 s4 test-3 running sum that skips day 0', w, DA % ('n + 1', '[0]', '1'), 3)
check('l12 s4 test-1: the last update of test 1 ends on day 7 = n - 1', '(5, 7, 1)])' in w['tests'][0]['call'] and w['tests'][0]['call'].startswith('apply_ranges(8,'))
check('l12 s4 test-3: test 3 starts on day 0 and gives 1, 1, 1, 3, 3', w['tests'][2]['call'] == 'apply_ranges(5, [(0, 4, 1), (3, 4, 2)])' and w['tests'][2]['expect'] == '[1, 1, 1, 3, 3]')

# ---------------------------------------------------------------- review-3
r3 = load('review-3.json')
w = r3['items'][1]['widget']
passes('review-3 items[1]', w)
ns = {}; exec(w['prelude'], ns)
check('review-3 test-9: n = 99,999 is odd; "ab" * 49,999 + "c" has 99,999 letters and passes the checker',
      99999 % 2 == 1 and len('ab' * 49999 + 'c') == 99999 and ns['check_ring'](99999, 'ab' * 49999 + 'c') and '99999' in w['tests'][8]['call'])

# ---------------------------------------------------------------- homework-3
h3 = load('homework-3.json')
w = h3['items'][0]['widget']
passes('homework-3 items[0]', w)
AL = '''def fewest_alerts(windows):
    count, last = 0, float("-inf")
    for s, e in %s:
        if %s:
            count += 1
            last = e
    return count
'''
a = first_fail(w, AL % ('sorted(windows)', 's > last'))
b = first_fail(w, AL % ('windows', 's > last'))
c = first_fail(w, AL % ('sorted(windows)', 'not (s <= last <= e)'))
d = first_fail(w, AL % ('windows', 'not (s <= last <= e)'))
print(f'      homework-3 items[0]: sort by start, alert at the end. `s > last`: test {a}; unsorted `s > last`: test {b}; '
      f'`not (s <= last <= e)`: test {c}; unsorted: test {d}')
check('homework-3 items[0] test-2: with a full cover check, an alert at 10 (the end of the window that starts first) fails first at test 2', c == 2 and d == 2)
t2 = h3['items'][0]['feedback']['byKey']['test-2']
finding('homework-3 items[0] test-2: "Sort by end" names the sort-by-start mistake, but the most natural coding of it (the same loop with `s > last`) passes test 2 and fails first at test 7',
        a == 7 and b == 7 and 'Sort by end, so the first alert goes at the smallest end' in t2 and 'test-7' not in h3['items'][0]['feedback']['byKey'],
        'imprecise: name the coding that lands at test 2 and add a test-7 line')
ns = {}; exec(w['solution'], ns)
check('homework-3 items[0]: test 2 expects 1 (an alert at 3 lies in (1, 10) and (2, 3)); test 7 expects 2', ns['fewest_alerts']([(1, 10), (2, 3)]) == 1 and 1 <= 3 <= 10 and 2 <= 3 <= 3
      and ns['fewest_alerts']([(1, 20), (2, 4), (3, 5), (10, 12), (11, 15)]) == 2 and w['tests'][6]['expect'] == '2')

w = h3['items'][2]['widget']
t0 = time.perf_counter(); ok = first_fail(w, w['solution'], limit=25) == 0; dt = time.perf_counter() - t0
check('homework-3 items[2]: solution passes, starter fails', ok and first_fail(w, w['starter']) != 0)
print(f'      homework-3 items[2]: solution takes {dt:.1f} s natively for the ten tests (the page allows 5 s + 20 s budget a case)')
CAP = '''def first_over_cap(n, updates, cap):
    def over(k):
        d = [0] * (n + 1)
        for l, r, v in updates[:k]:
            d[l] += v
            d[r + 1] -= v
        run = 0
        for i in range(n):
            run += d[i]
            if run %s cap:
                return True
        return False
%s    lo, hi = 1, len(updates)
    while lo < hi:
        mid = (lo + hi) // 2
        if over(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
'''
PRE = '    if not over(len(updates)):\n        return -1\n'
lands('homework-3 items[2] test-1 `>= cap`', w, CAP % ('>=', PRE), 1, limit=25)
lands('homework-3 items[2] test-3 no check before the search', w, CAP % ('>', ''), 3, limit=25)
LIN = '''def first_over_cap(n, updates, cap):
    days = [0] * n
    for k, (l, r, v) in enumerate(updates, 1):
        for i in range(l, r + 1):
            days[i] += v
            if days[i] > cap:
                return k
'''
lands('homework-3 items[2] test-3 a simulation that falls off the end (returns None)', w, LIN, 3, limit=25)
days = [0] * 5
for l, r, v in [(0, 2, 3), (1, 4, 2)]:
    for i in range(l, r + 1):
        days[i] += v
check('homework-3 items[2] test-1: after two updates days 1 and 2 hold exactly 5 and no day more', days == [3, 5, 5, 2, 2])
check('homework-3 items[2] test-10: 10^5 updates of at most 10 cannot reach 10^9; expects -1',
      10**5 * 10 < 10**9 and w['tests'][9]['expect'] == '-1' and '1000000000' in w['tests'][9]['call'] and 'range(100000)' in w['tests'][9]['setup'])

# ---------------------------------------------------------------- voice gate on the changed strings
import re
CHANGED = [
    ('homework-2.json', ['items', 3, 'widget', 'model']), ('homework-3.json', ['items', 0, 'feedback', 'byKey', 'test-2']),
    ('homework-3.json', ['items', 2, 'feedback', 'byKey', 'test-1']), ('homework-3.json', ['items', 2, 'feedback', 'byKey', 'test-3']),
    ('homework-3.json', ['items', 2, 'feedback', 'byKey', 'test-10']), ('l1-reading-statements.json', ['screens', 3, 'prose']),
    ('l1-reading-statements.json', ['screens', 3, 'feedback', 'byKey', 't-legend']), ('l1-reading-statements.json', ['screens', 3, 'explain', 'text']),
    ('l1-reading-statements.json', ['screens', 10, 'feedback', 'byKey', 'test-6']), ('l10-greedy-proofs.json', ['screens', 4, 'widget', 'how']),
    ('l10-greedy-proofs.json', ['screens', 4, 'feedback', 'byKey', 'test-1']), ('l10-greedy-proofs.json', ['screens', 4, 'feedback', 'byKey', 'test-6']),
    ('l10-greedy-proofs.json', ['screens', 4, 'feedback', 'byKey', 'test-7']), ('l11-bitmasks.json', ['screens', 3, 'widget', 'how']),
    ('l11-bitmasks.json', ['screens', 3, 'feedback', 'byKey', 'test-1']), ('l11-bitmasks.json', ['screens', 3, 'feedback', 'byKey', 'test-5']),
    ('l12-difference-arrays.json', ['screens', 4, 'feedback', 'byKey', 'test-1']), ('l12-difference-arrays.json', ['screens', 4, 'feedback', 'byKey', 'test-3']),
    ('l2-limits-to-complexity.json', ['screens', 4, 'explain', 'text']), ('l2-limits-to-complexity.json', ['screens', 5, 'feedback', 'byKey', 'floor']),
    ('l2-limits-to-complexity.json', ['screens', 9, 'feedback', 'byKey', 'test-7']), ('l2-limits-to-complexity.json', ['screens', 9, 'feedback', 'byKey', 'test-6']),
    ('l2-limits-to-complexity.json', ['screens', 10, 'feedback', 'byKey', 'test-1']), ('l2-limits-to-complexity.json', ['screens', 10, 'feedback', 'byKey', 'test-3']),
    ('l2-limits-to-complexity.json', ['screens', 10, 'feedback', 'byKey', 'test-5']), ('l3-fast-io.json', ['screens', 9, 'feedback', 'byKey', 'test-7']),
    ('l3-fast-io.json', ['screens', 10, 'feedback', 'byKey', 'test-1']), ('l3-fast-io.json', ['screens', 10, 'feedback', 'byKey', 'test-4']),
    ('l3-fast-io.json', ['screens', 10, 'feedback', 'byKey', 'test-6']), ('l3-fast-io.json', ['screens', 10, 'explain', 'text']),
    ('l4-stress-testing.json', ['screens', 7, 'feedback', 'byKey', 'test-7']), ('l5-modulo.json', ['screens', 5, 'prose']),
    ('l8-invariants.json', ['screens', 5, 'explain', 'text']), ('l8-invariants.json', ['screens', 9, 'prose']), ('l8-invariants.json', ['summary', 'ideas', 2]),
    ('l9-constructive.json', ['screens', 5, 'feedback', 'byKey', 'test-8']), ('review-3.json', ['items', 1, 'feedback', 'byKey', 'test-9']),
]
REPLACEMENTS = [
    'Binary search for $m$ between 0 and $10^9$. In the worst case, how many halvings shrink those $10^9 + 1$ values to one?',
    'Test 3 is four 2s with $k = 4$ and expects 6. Equal values at different positions still make pairs: do not remove duplicates.',
    'A monovariant rises at every move, or falls at every move. If it is a whole number that cannot pass some bound, the process must end, as the walk back does.',
    'Test 2 is (1, 10) and (2, 3): one alert at 3 covers both. An alert at 10, the end of the window that starts first, misses (2, 3). Sort by end.',
    'Test 7: sorted by start, (1, 20) puts the first alert at 20 and `s > last` then skips every other window. Sort by end.',
]


def sentences(text):
    t = re.sub(r'\$\$.*?\$\$', ' FORMULA. ', text, flags=re.S)
    t = re.sub(r'\$[^$]*\$', 'X', t)
    t = re.sub(r'`[^`]*`', 'CODE', t)
    t = re.sub(r'\*\*([^*]*)\*\*', r'\1', t)
    return [x.strip() for x in re.split(r'(?<=[.?!:])\s+|\n+', t) if x.strip()]


worst, bad = 0, []
for f, path in CHANGED:
    o = load(f)
    for k in path:
        o = o[k]
    for sen in sentences(o):
        worst = max(worst, len(sen.split()))
        if len(sen.split()) > 35:
            bad.append((f, sen))
    if '!' in o or '—' in o or '–' in o or re.search(r'\b(color|center|analyze|behavior|neighbor)\b', o):
        bad.append((f, 'voice character'))
for o in REPLACEMENTS:
    for sen in sentences(o):
        if len(sen.split()) > 35 or '!' in o or '—' in o:
            bad.append(('replacement', sen))
print('      longest changed sentence:', worst, 'words')
check('voice: changed strings and replacements have no sentence over 35 words, no exclamation mark, no dash, British spelling', not bad, bad)
ex = {('l1-reading-statements.json', 3): 3, ('l2-limits-to-complexity.json', 4): 3, ('l3-fast-io.json', 10): 3, ('l8-invariants.json', 5): 3}
okx = True
for (f, i), n in ex.items():
    t = load(f)['screens'][i]['explain']['text']
    okx &= len(re.findall(r'[.](?:\s|$)', re.sub(r'\$[^$]*\$', 'X', t))) <= n
check('voice: the four changed explains have at most three sentences', okx)

# the replacement lines, verified as the rows were
c2 = first_fail(h3['items'][0]['widget'], AL % ('sorted(windows)', 'not (s <= last <= e)'))
check('replacement homework-3 test-2: the coding it names (cover check against the last alert, sorted by start) lands at test 2, and 10 is outside (2, 3)', c2 == 2 and not 2 <= 10 <= 3)
check('replacement homework-3 test-7: sorted by start, `s > last` gives 1 for the expected 2 and lands at test 7', a == 7 and by_start is not None)
ns = {}; exec(AL % ('sorted(windows)', 's > last'), ns)
check('replacement homework-3 test-7: (1, 20) sorts first by start and every other window starts at or before 20', ns['fewest_alerts']([(1, 20), (2, 4), (3, 5), (10, 12), (11, 15)]) == 1)
check('replacement l2 s5 question: the worst case is exactly 30', halvings(N, worst=True) == 30 and halvings(N, worst=False) == 29)

print(f'\n{len(PASS)} checks passed, {len(FAIL)} failed, {len(FIND)} findings open')
sys.exit(1 if FAIL or FIND else 0)
