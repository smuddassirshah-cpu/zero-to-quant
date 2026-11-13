#!/usr/bin/env python3
"""Round 2 blind concept audit of algo-think L1 to L3: every complexity, operation-count, memory and
code-behaviour claim, run. Written blind (before any earlier review, audit or script was opened).

Run:  python3 docs/reports/algo-think-L1-3-r2-concepts.py          (CPython; written on 3.13)
      also runs unchanged under Pyodide 0.27.7 (Python 3.12.7, wasm32), the page's own interpreter.
Exit 0 only if every content claim checked here holds. A check that fails because the content is wrong
stays failing: each such line names its finding in docs/reviews/audit-algo-think-1-3-r2.md.
Expected on the content as audited: 6 failing checks (findings 1 to 7; finding 8 has no failing check), exit 1.
"""
import sys, math, random, bisect, time, tracemalloc, itertools, functools

FAILS, N = [], [0]
def ok(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name); print('FAIL', name)
W64 = sys.maxsize > 2**32
rng = random.Random(20261113)

# ---------------------------------------------------------------- L1 counting
P8 = [102, 98, 105, 101, 99, 108, 104, 100]
def scan(prices):
    comps = assigns = 0
    best = prices[0]; assigns += 1
    for p in prices[1:]:
        comps += 1
        if p > best: best = p; assigns += 1
    return comps, assigns
c, a = scan(P8)
ok('l1 scan 7 comparisons, best changes twice', c == 7 and a - 1 == 2)
ok('l1 Ben counts 11 = 1 + 7 + 2 + 1', a + c + 1 == 11 and a + c + 1 <= 2 * (8 - 1) + 2)
pairs = lambda n: sum(1 for i in range(n) for j in range(i + 1, n))
ok('l1 pair loop 28, 120, 496, 0, 0', [pairs(n) for n in (8, 16, 32, 1, 0)] == [28, 120, 496, 0, 0])
ok('l1 n(n-1)/2 for all n < 200', all(pairs(n) == n * (n - 1) // 2 for n in range(200)))
ok('l1 28 is four times 7', 28 / 7 == 4)
ok('l1 100 prices: 4950, 5050, 9900, 10000', (4950, 5050, 9900, 10000) == (100 * 99 // 2, sum(range(1, 101)), 100 * 99, 100 ** 2))
ok('l1 2000 stocks 1,999,000 pairs; x250 about 5e8', 2000 * 1999 // 2 == 1999000 and abs(1999000 * 250 / 5e8 - 1) < 0.01)
ok('l1 5x stocks about 25x pairs', abs((10000 * 9999 / 2) / 1999000 - 25) < 0.02 and abs(10000 * 9999 / 2 / 5e7 - 1) < 0.01)
ok('l1 quiz triangle 45, sequential 1000', sum(i for i in range(10)) == 45 and 500 + 500 == 1000)
try:
    [][0]; e = None
except IndexError as x: e = x
ok('l1 prices[0] on [] raises IndexError', e is not None)
# Finding 8: "cannot afford a further loop over n" is an unsupported feasibility claim; the arithmetic alone:
ok('l1 Q2 further loop is 5e11 steps', abs(10000 * 9999 / 2 * 10000 / 5e11 - 1) < 0.01)

# ---------------------------------------------------------------- L2 big O
ok('l2 2^n > n^2 for good from 5', [n for n in range(1, 60) if all(2 ** m > m * m for m in range(n, 200))][0] == 5 and 2 ** 4 == 16 and 3 ** 2 > 2 ** 3 and 2 ** 2 == 4)
f = lambda n: 3 * n * n + 50 * n + 7
ok('l2 3n^2+50n+7 < 4n^2 from 51', f(50) == 10007 and f(51) == 10360 and 4 * 51 ** 2 == 10404 and all(f(n) < 4 * n * n for n in range(51, 5000)) and f(50) > 4 * 2500)
ok('l2 root 50.14, 3n^2 passes 50n at 17', abs((50 + math.sqrt(2500 + 28)) / 2 - 50.14) < 0.005 and 3 * 17 ** 2 > 50 * 17 and 3 * 16 ** 2 < 50 * 16)
ok('l2 c=60, n0=1 works', all(f(n) <= 60 * n * n for n in range(1, 5000)))
def halvings(n):
    k = 0
    while n > 1: n //= 2; k += 1
    return k
ok('l2 snippet D is floor(log2 n)', all(halvings(n) == int(math.log2(n)) for n in (2, 3, 8, 1000, 1024, 10 ** 6)))
ok('l2 doubling table', (11, 2048 * 11, 2048 ** 2) == (11, 22528, 4194304) and round(22528 / 10240, 1) == 2.2)
ok('l2 50n vs n^2: B 400 v 1000, tie 50, A from 51', 50 * 20 == 1000 and 50 * 50 == 50 ** 2 and 50 * 51 < 51 ** 2 and 50 * 49 > 49 ** 2)
ok('l2 3n passes 1e6 at 333,334', 3 * 333334 > 10 ** 6 >= 3 * 333333)
ok('l2 2n log n passes 40n once log2 n > 20', 2 * 2 ** 21 * 21 > 40 * 2 ** 21 and 2 * 2 ** 20 * 20 == 40 * 2 ** 20)
ok('l2 backtest 2.5e6, x500 = 1.25e9', 5000 * 500 == 2500000 and 5000 * 500 * 500 == 1250000000)
def bs_steps(n):  # worst-case looks of the l9 binary search (lo <= hi, mid +/- 1)
    best = 0
    for t in range(-1, 2 * n + 1):
        lo, hi, k = 0, n - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2; k += 1; v = 2 * mid
            if v == t: break
            if v < t: lo = mid + 1
            else: hi = mid - 1
        best = max(best, k)
    return best
ok('l2/l9 worst looks floor(log2 n)+1 for n <= 600', all(bs_steps(n) == int(math.log2(n)) + 1 for n in range(1, 601)))
ok('l9 table 1, 16, 1000, 1e6, 5000', [int(math.log2(n)) + 1 for n in (1, 16, 1000, 10 ** 6, 5000, 2 * 10 ** 6)] == [1, 5, 10, 20, 13, 21])

# ---------------------------------------------------------------- L3 memory
xs = [float(i) for i in range(1_000_000)]
if W64:
    ok('l3 getsizeof list 8,448,728 and float 24 (64-bit)', sys.getsizeof(xs) == 8448728 and sys.getsizeof(xs[0]) == 24)
    ok('l3 about 32.4 MB, three quarters floats', abs((sys.getsizeof(xs) + 24e6) / 1e6 - 32.45) < 0.01 and abs(24 / 32.45 - 0.75) < 0.02)
    ok('hw1 3-tuple 64 bytes, about 96 a row, 9e6 rows near 1 GB', sys.getsizeof((1.0, 'a', 'b')) == 64 and 0.8e9 < 8997000 * 96 < 1e9)
else:
    ok('l3 this page: about 20 bytes a float (32-bit)', sys.getsizeof(xs[0]) == 16 and round((sys.getsizeof(xs) + 16e6) / 1e6) == 20)
del xs
def peak(fn):
    tracemalloc.start()
    try:
        fn(); return tracemalloc.get_traced_memory()[1]
    finally: tracemalloc.stop()
def stream_mean(ticks):
    total, count = 0.0, 0
    for x in ticks: total += x; count += 1
    return None if count == 0 else total / count
p1 = peak(lambda: stream_mean(float(i) for i in range(100_000)))
p2 = peak(lambda: (lambda t: sum(t) / len(t))(list(float(i) for i in range(100_000))))
ok('l3 stream_mean peak < 50,000 bytes; a stored list takes megabytes', p1 < 50_000 and p2 > 1_500_000)
rev = list(P8); lo, hi, sw = 0, 7, 0
while lo < hi: rev[lo], rev[hi] = rev[hi], rev[lo]; lo, hi, sw = lo + 1, hi - 1, sw + 1
ok('l3 in-place reverse: 4 swaps for 8, floor(1001/2) = 500', sw == 4 and rev == P8[::-1] and 1001 // 2 == 500)
pre = [0]
for p in [3, 1, 4, 1, 5]: pre.append(pre[-1] + p)
ok('l3 prefix sums', pre == [0, 3, 4, 8, 9, 14] and pre[4] - pre[1] == 6 and sum(range(10, 20)) == 145)
def total(xs, i=0, d=[0]):
    d[0] = max(d[0], i + 1)
    return 0 if i == len(xs) else xs[i] + total(xs, i + 1, d)
dd = [0]; total([5, 3, 8, 1, 4], 0, dd)
ok('l3 recursive total opens n+1 = 6 calls', dd[0] == 6)
try:
    total(list(range(5000)), 0, [0]); r = 'ran'
except RecursionError: r = 'RecursionError'
ok('l3/l6 5,000-deep recursion raises RecursionError at the default limit 1000', r == 'RecursionError' and sys.getrecursionlimit() == 1000)
ok('l3 minute bars', 10 * 252 * 390 * 5 == 4914000 and 200 * 4914000 == 982800000 and round(982800000 * 8 / 1e9, 2) == 7.86
   and [round(k * 4914000 * b / 1e9, 2) for k, b in ((200, 32), (100, 32), (50, 32), (50, 8), (100, 8))] == [31.45, 15.72, 7.86, 1.97, 3.93] and round(4914000 * 8 / 1e9, 3) == 0.039)
g = (p for p in [120, -40, 330, -15] if p > 0); s450 = sum(g)
try: max(g); msg = ''
except ValueError as x: msg = str(x)
ok('l3 generator: 450, then max() iterable argument is empty', s450 == 450 and msg == 'max() iterable argument is empty')
data = [rng.gauss(0, 1) for _ in range(5000)]
n_, s1, s2 = len(data), sum(data), sum(x * x for x in data)
ok('l3 Var = sum x^2 / n - mean^2 (population)', abs((s2 / n_ - (s1 / n_) ** 2) - sum((x - s1 / n_) ** 2 for x in data) / n_) < 1e-9)

# ---------------------------------------------------------------- L4 amortised
def grow(n, start=1, factor=2, step=0):
    cap, size, copies, per = start, 0, 0, []
    for _ in range(n):
        c = 0
        if size == cap:
            c = size; cap = cap * factor if not step else cap + step
        copies += c; per.append(c); size += 1
    return copies, per, cap, size
ok('l4 doubling totals', [grow(n)[0] for n in (0, 1, 2, 3, 4, 5, 8, 9, 16, 17, 100, 1000, 1025, 65)] == [0, 0, 1, 3, 3, 7, 7, 15, 15, 31, 127, 1023, 2047, 127])
ok('l4 9th append copies 8; worst of 100 is 64 at append 65', grow(9)[1][8] == 8 and max(grow(100)[1]) == 64 and grow(100)[1].index(64) == 64)
ok('l4 15/16, 3.75, 1.023; 10 resizes in 1000', 15 / 16 == 0.9375 and 15 / 4 == 3.75 and sum(1 for c in grow(1000)[1] if c) == 10 and [i + 1 for i, c in enumerate(grow(1000)[1]) if c][-1] == 513)
ok('l4 doubling total < 2n, n-1 at powers of two', all(grow(n)[0] < 2 * n for n in range(1, 3000)) and all(grow(2 ** k)[0] == 2 ** k - 1 for k in range(12)))
ok('l4 tripling total < 1.5n; r/(r-1) n for r = 2, 3, 4', all(grow(n, 1, 3)[0] < 1.5 * n for n in range(1, 3000)) and all(grow(n, 1, 4)[0] < 4 / 3 * n for n in range(1, 3000)))
ok('l4 tripling not always fewer copies than doubling (n=4) nor more (n=10)', grow(4, 1, 3)[0] > grow(4)[0] and grow(10, 1, 3)[0] < grow(10)[0])
c10 = grow(1000, 10, 1, 10)
ok('l4 grow-by-10: 49,500 copies, last resize at append 991, about n^2/20', c10[0] == 49500 and [i + 1 for i, c in enumerate(c10[1]) if c][-1] == 991 and abs(49500 / (1000 ** 2 / 20) - 1) < 0.02 and 48 < 49500 / 1023 < 50)
# Findings 3 and 4: l4 S7 fb "to-1000" says "The array is never full at 1,000 here"; review-1 I6 says "not full at 1,000 within these appends".
ok('FINDING 3 and 4, l4 S7 / review-1 I6: array "never full at 1,000" (it is full after the 1,000th append)', not (c10[2] == 1000 and c10[3] == 1000))
c100 = grow(1000, 100, 1, 100)
ok('review-1 fixed 100: 4,500; hw1 start 4: 124, 252 with 128', c100[0] == 4500 and grow(100, 4)[0] == 124 and 124 + 128 == 252)
ok('hw1 copies_fixed', grow(5, 1, 1, 1)[0] == 10 and grow(10 ** 6, 10, 1, 10)[0] == 49999500000 and grow(11, 10, 1, 10)[0] == 10)
ok('l4 pop(0) drain 499,500 shifts', sum(range(1000)) == 499500)
ok('l4 order book: 2^20, 2,097,151 copies, 1.05 a tick', grow(1048576)[0] == 1048575 and grow(2 * 10 ** 6)[0] == 2097151 and round(2097151 / 2e6, 2) == 1.05 and round(1048576 / 2e6, 2) == 0.52)
caps, lst, last = [], [], None
for i in range(200000):
    lst.append(0); s = sys.getsizeof(lst)
    if s != last: caps.append((len(lst), s)); last = s
ptr = 8 if W64 else 4
ratios = [(b[1] - caps[0][1] + ptr * 0) / (a[1]) for a, b in zip(caps[-30:], caps[-29:])]
ok('l4 CPython list growth factor about 1.125', all(1.11 < r < 1.14 for r in ratios))

# ---------------------------------------------------------------- L5 recursion
def fact(n): return 1 if n == 0 else n * fact(n - 1)
def sum_list(xs): return 0 if not xs else xs[0] + sum_list(xs[1:])
ok('l5 fact returns 1, 1, 2, 6, 24', [fact(k) for k in range(5)] == [1, 1, 2, 6, 24] and sum_list([4, 1, 3]) == 8)
def sl_last(xs): return 0 if not xs else xs[-1] + sl_last(xs[1:])
def sl_skip(xs): return 0 if not xs else xs[0] + sl_skip(xs[2:])
def sl_drop(xs):
    if not xs: return 0
    sl_drop(xs[1:]); return xs[0]
ok('l5 wrong recursive cases give 9, 7 and 4', (sl_last([4, 1, 3]), sl_skip([4, 1, 3]), sl_drop([4, 1, 3])) == (9, 7, 4))
def raises(fn, exc):
    try: fn(); return False
    except exc: return True
def fact1(n): return 1 if n == 1 else n * fact1(n - 1)
def f2(n): return 0 if n == 0 else n + f2(n - 2)
def ffloor(n): return 0 if n == 0 else ffloor(n // 2)
ok('l5 base cases skipped: fact1(0), f(3), f(-1) raise RecursionError; fact1(5) = 120', raises(lambda: fact1(0), RecursionError) and raises(lambda: f2(3), RecursionError) and raises(lambda: ffloor(-1), RecursionError) and fact1(5) == 120 and -1 // 2 == -1)
ok('l5 sum_list base case len == 1 fails on [] with IndexError', raises(lambda: (lambda xs: xs[0])([]), IndexError))
def count(xs): return 1 if not xs else 1 + count(xs[1:])
def grow_(n, start=1000, r=1.05): return start if n == 0 else grow_(n - 1, start, r) * r
def value(flows, r): return 0 if not flows else (flows[0] + value(flows[1:], r)) / (1 + r)
ok('l5 quiz: count 3, grow 1157.625, bond 97.2768', count([5, 5]) == 3 and abs(grow_(3) - 1157.625) < 1e-9 and abs(value([4, 4, 104], 0.05) - 97.2768) < 5e-5
   and abs(value([4, 4, 104], 0.05) - sum(cf / 1.05 ** t for t, cf in ((1, 4), (2, 4), (3, 104)))) < 1e-12 and abs(value([5, 5, 105], 0.05) - 100) < 1e-9)
ok('review-2 grow 530.604', abs(grow_(3, 500, 1.02) - 530.604) < 1e-9 and abs(grow_(2, 500, 1.02) - 520.2) < 1e-9)
ok('l5 folder total 395.75', abs(120.5 - 40 + 15.25 + 300 - 395.75) < 1e-12)

# ---------------------------------------------------------------- L6 call stack
import inspect
def depth_probe(fn, *a):
    best = [0]; base = len(inspect.stack(0))
    def tr(frame, event, arg):
        if event == 'call' and frame.f_code is fn.__code__:
            d, f = 0, frame
            while f is not None:
                if f.f_code is fn.__code__: d += 1
                f = f.f_back
            best[0] = max(best[0], d)
        return None
    sys.setprofile(tr)
    try: fn(*a)
    finally: sys.setprofile(None)
    return best[0]
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)
ok('l6 frames: fact(5) 6, fact(3) 4, sum_list of 6 is 7', depth_probe(fact, 5) == 6 and depth_probe(fact, 3) == 4 and depth_probe(sum_list, [1] * 6) == 7)
ok('l6 fib depth n (1 for n < 2): 5 -> 5, 15 -> 15', [depth_probe(fib, n) for n in (0, 1, 2, 5, 15)] == [1, 1, 2, 5, 15])
def sum_to(n): return 0 if n == 0 else n + sum_to(n - 1)
def sum_to_acc(n, acc=0): return acc if n == 0 else sum_to_acc(n - 1, acc + n)
ok('l6 sum_to(5000) and its tail-call form both raise RecursionError (no tail-call reuse)', raises(lambda: sum_to(5000), RecursionError) and raises(lambda: sum_to_acc(5000), RecursionError))
ok('l6 a loop sums to 100000', sum(range(1, 100001)) == 5000050000)
# Raising the limit: a pure-Python recursion then runs (3.11+); recursion through C code is not protected the same way.
# Under Pyodide 0.27.7 max([n], key=lambda x: f(n - 1)) 5,000 deep with the limit at 10**9 kills the interpreter
# (RangeError: Maximum call stack size exceeded, pyodide_fatal_error), so the "can crash with no traceback" claim holds there.
old = sys.getrecursionlimit(); sys.setrecursionlimit(20000)
try: r5000 = sum_to(5000)
finally: sys.setrecursionlimit(old)
ok('l6 note: with a raised limit sum_to(5000) runs (12,502,500)', r5000 == 12502500)
def sum_list_bad(xs):
    total = 0
    if not xs: return total
    total = total + xs[0]; sum_list_bad(xs[1:]); return total
def count_calls(n):
    calls = 0; calls += 1
    if n > 0: count_calls(n - 1)
    return calls
ok('l6 own-frame totals: 4; hw2 count_calls(5) = 1', sum_list_bad([4, 1, 3]) == 4 and count_calls(5) == 1)
def inner(m): return n_undefined_name  # noqa
ok('l6 a function cannot see its caller\'s locals: NameError', raises(lambda: inner(2), NameError))
def levels(node): return 1 + max([levels(c) for c in node['children']], default=0)
deep = functools.reduce(lambda acc, i: {'children': [acc]}, range(499), {'children': []})
ok('l6 levels of a 500 chain', levels(deep) == 500)

# ---------------------------------------------------------------- L7 divide and conquer
calls = [0]; cmps = [0]; maxd = [0]
def max_rec(xs, lo, hi, d=1):
    calls[0] += 1; maxd[0] = max(maxd[0], d)
    if lo == hi: return xs[lo]
    mid = (lo + hi) // 2
    l, r = max_rec(xs, lo, mid, d + 1), max_rec(xs, mid + 1, hi, d + 1)
    cmps[0] += 1
    return max(l, r)
res = []
for n in (1, 8, 16, 1000) + tuple(range(2, 60)):
    calls[0] = cmps[0] = maxd[0] = 0; max_rec(list(range(n)), 0, n - 1); res.append((n, calls[0], cmps[0], maxd[0]))
ok('l7 max_rec makes 2n-1 calls and n-1 comparisons', all(c == 2 * n - 1 and k == n - 1 for n, c, k, _ in res))
ok('l7 15 calls for 8, 31 for 16; hw2 11 frames and 1,999 calls for 1000', res[1][1] == 15 and res[2][1] == 31 and res[3][1] == 1999 and res[3][3] == 11)
ok('l7 bad split max_rec([5,8]) with mid recurses for ever', raises(lambda: (lambda g: g(g, [5, 8], 0, 1))(lambda g, xs, lo, hi: xs[lo] if lo == hi else max(g(g, xs, lo, (lo + hi) // 2), g(g, xs, (lo + hi) // 2, hi))), RecursionError))
def inv_brute(xs): return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])
ok('l7/l12/hw2 inversion counts 3, 3, 9, 2, 14 (4 + 3 + 7)', [inv_brute(x) for x in ([3, 1, 4, 2], [3, 1, 2, 5, 4, 6], [5, 2, 4, 6, 1, 3], [2, 2, 1], [5, 3, 8, 1, 4, 7, 2, 6], [5, 3, 8, 1], [4, 7, 2, 6])] == [3, 3, 9, 2, 14, 4, 3])
def power_fast(x, n, d=1):
    maxd[0] = max(maxd[0], d)
    if n == 0: return 1, 0
    if n == 1: return x, 0
    h, m = power_fast(x, n // 2, d + 1)
    return (h * h, m + 1) if n % 2 == 0 else (h * h * x, m + 2)
def pf(n):
    maxd[0] = 0; v, m = power_fast(1, n); return m, maxd[0]
ok('l7 multiplications: 10->4, 5->3, 1000->14, 252->12, 2520->16, 100->8, 1e9->41 in 30 calls', [pf(n)[0] for n in (10, 5, 1000, 252, 2520, 100, 10 ** 9)] == [4, 3, 14, 12, 16, 8, 41] and pf(10 ** 9)[1] == 30)
ok('review-2 power_fast(x, 50) is 6 frames; 1024 halves in 11 calls', pf(50)[1] == 6 and pf(1024)[1] == 11)
ok('l7 values: 2^10, 3^5, 1.05^252, 1.0002^252', power_fast(2, 10)[0] == 1024 and power_fast(3, 5)[0] == 243 and abs(power_fast(1.05, 252)[0] / 218626.7836322 - 1) < 1e-9 and round(1.0002 ** 252, 4) == 1.0517)
def merge_cmp(a, b):
    out, i, j, k = [], 0, 0, 0
    while i < len(a) and j < len(b):
        k += 1
        if a[i] <= b[j]: out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1
    return out + a[i:] + b[j:], k
worst = 0
for _ in range(3000):
    u = sorted(rng.sample(range(100), 7)); A, B = sorted(u[:3]), sorted(u[3:])
    A = sorted(rng.sample(u, 3)); B = sorted(set(u) - set(A)); worst = max(worst, merge_cmp(A, B)[1])
ok('l7/l12 merge of 3 and 4 never exceeds 6 comparisons and reaches 6; 40 + 25 - 1 = 64', worst == 6 and merge_cmp(list(range(0, 80, 2)), [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 79])[1] == 64)

# ---------------------------------------------------------------- L8 recurrences
@functools.lru_cache(None)
def T(kind, n):
    if n == 1: return 1
    return {'lin': lambda: T(kind, n - 1) + 1, 'ms': lambda: 2 * T(kind, n // 2) + n, 'bs': lambda: T(kind, n // 2) + 1,
            'exp': lambda: 2 * T(kind, n - 1) + 1, 'max': lambda: 2 * T(kind, n // 2) + 1, 'sq': lambda: 2 * T(kind, n // 2) + n * n}[kind]()
ok('l8 T(n-1)+1 = n; T(n/2)+1 = log2 n + 1 (21 at 2^20)', T('lin', 8) == 8 and T('bs', 2 ** 20) == 21 and T('bs', 8) == 4)
ok('l8 2T(n/2)+n = n(log2 n + 1): 4, 12, 32, 80', [T('ms', n) for n in (2, 4, 8, 16)] == [4, 12, 32, 80] and all(T('ms', 2 ** k) == 2 ** k * (k + 1) for k in range(20)))
ok('l8 2T(n-1)+1 = 2^n - 1 (1023 at 10, 7 at 3)', T('exp', 10) == 1023 and T('exp', 3) == 7 and all(T('exp', n) == 2 ** n - 1 for n in range(1, 60)))
ok('l8 2T(n/2)+1 = 2n-1; hw2 2T(n/2)+n^2 < 2n^2', all(T('max', 2 ** k) == 2 ** (k + 1) - 1 and T('sq', 2 ** k) < 2 * 4 ** k for k in range(20)))
def C(n):
    a, b = 1, 1
    for _ in range(n - 1): a, b = b, 1 + a + b
    return a if n == 0 else b
F = [0, 1]
while len(F) < 400: F.append(F[-1] + F[-2])
fibcalls = [0]
def fibc(n):
    fibcalls[0] += 1
    return n if n < 2 else fibc(n - 1) + fibc(n - 2)
fibc(20)
ok('l8 fib calls C(n) = 2F(n+1)-1: 15, 25, 41, 177, measured at 20', [C(n) for n in (5, 6, 7, 10)] == [15, 25, 41, 177] and all(C(n) == 2 * F[n + 1] - 1 for n in range(100)) and fibcalls[0] == C(20))
ok('l8 C(80), F(90), F(300), C(30) and C <= 2^n - 1', C(80) == 75778124746287811 and F[90] == 2880067194370816120 and F[300] == 222232244629420445529739893461909967206666939096499764990979600 and C(30) == 2692537 and all(C(n) <= 2 ** n - 1 for n in range(1, 80)))
ok('l8 fib calls grow by about 1.618 a step', abs(C(60) / C(59) - (1 + 5 ** 0.5) / 2) < 1e-6)
memo = {0: 0, 1: 1}; mcalls = [0]
def fibm(n):
    mcalls[0] += 1
    if n not in memo: memo[n] = fibm(n - 1) + fibm(n - 2)
    return memo[n]
fibm(30)
ok('l8 memoised fib(30) makes 59 calls', mcalls[0] == 59)
ok('l8 lattice 5,151 nodes; 15 for 3 steps; 2^101 - 1 about 2.5e30; hw2 231 and 2,097,151', 101 * 102 // 2 == 5151 and 2 ** 4 - 1 == 15 and abs((2 ** 101 - 1) / 2.5e30 - 1) < 0.02 and 21 * 22 // 2 == 231 and 2 ** 21 - 1 == 2097151 and abs(2 ** 253 / 1.4e76 - 1) < 0.04)
ok('l8 lattice leaves', [round(100 * 1.1 ** u * 0.9 ** (3 - u), 1) for u in (3, 2, 1, 0)] == [133.1, 108.9, 89.1, 72.9])
def price_rec(S, step, n, u, d, p, disc, K, cnt):
    cnt[0] += 1
    if step == n: return max(S - K, 0)
    return disc * (p * price_rec(S * u, step + 1, n, u, d, p, disc, K, cnt) + (1 - p) * price_rec(S * d, step + 1, n, u, d, p, disc, K, cnt))
def price_loop(S, n, u, d, p, disc, K):
    v = [max(S * u ** j * d ** (n - j) - K, 0) for j in range(n + 1)]; upd = 0
    for step in range(n - 1, -1, -1):
        v = [disc * (p * v[j + 1] + (1 - p) * v[j]) for j in range(step + 1)]; upd += step + 1
    return v[0], upd
cnt = [0]; pr = price_rec(100, 0, 12, 1.1, 0.9, 0.55, 0.99, 100, cnt)
ok('hw2 pricer: 2^(n+1)-1 calls, loop agrees, n(n+1)/2 updates', cnt[0] == 2 ** 13 - 1 and abs(pr - price_loop(100, 12, 1.1, 0.9, 0.55, 0.99, 100)[0]) < 1e-9 and price_loop(100, 12, 1.1, 0.9, 0.55, 0.99, 100)[1] == 78 and 2000 * 2001 // 2 == 2001000)

# ---------------------------------------------------------------- L9 binary search
S16 = [3, 8, 12, 17, 21, 26, 30, 35, 41, 47, 52, 58, 64, 70, 77, 85]
def binary_search(xs, target, trace=None):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if trace is not None: trace.append(mid)
        v = xs[mid]
        if v == target: return mid
        if v < target: lo = mid + 1
        else: hi = mid - 1
    return -1
tr = []
ok('l9 64 found at 12 in four looks 7, 11, 13, 12; scan needs 13', binary_search(S16, 64, tr) == 12 and tr == [7, 11, 13, 12] and S16.index(64) + 1 == 13)
ok('l9 unsorted list misses 5', binary_search([8, 3, 12, 5, 20], 5) == -1)
def first_at_least(xs, target, passes=None):
    lo, hi, k = 0, len(xs), 0
    while lo < hi:
        mid = (lo + hi) // 2; k += 1
        if xs[mid] < target: lo = mid + 1
        else: hi = mid
    if passes is not None: passes.append(k)
    return lo
good = True; worstp = {}
for n in range(0, 130):
    xs = sorted(rng.randrange(40) for _ in range(n)); ps = []
    for t in range(-1, 42): good &= first_at_least(xs, t, ps) == bisect.bisect_left(xs, t)
    worstp[n] = max(ps)
ok('l9 first_at_least == bisect_left; passes at most ceil(log2(n+1)), reached', good and all(worstp[n] == math.ceil(math.log2(n + 1)) for n in range(1, 130)))
ok('l9 [2,4,4,4,4,4,7,9] first 4 at 1; bisect_right 6 and 4', first_at_least([2, 4, 4, 4, 4, 4, 7, 9], 4) == 1 and bisect.bisect_right([96, 98, 99, 100, 100, 100, 101, 103], 100) == 6 and bisect.bisect_left([96, 98, 99, 100, 100, 100, 101, 103], 100) == 3 and (bisect.bisect_left([1, 3, 3, 3, 8], 3), bisect.bisect_right([1, 3, 3, 3, 8], 3)) == (1, 4))
def stuck(xs, target, le=False, limit=200):
    lo, hi, k = 0, (len(xs) - 1 if le else len(xs)), 0
    while (lo <= hi if le else lo < hi):
        k += 1
        if k > limit: return 'loops'
        mid = (lo + hi) // 2
        if xs[mid] < target: lo = mid + 1 if le else mid
        else: hi = mid
    return lo
ok('l9 lo = mid never ends on [10,20,30,40], 35; review-3 <= with hi = mid never ends on [10,20], 15', stuck([10, 20, 30, 40], 35) == 'loops' and stuck([10, 20], 15, le=True) == 'loops')
import datetime
ok('l9 7 and 8 March 2026 are a weekend; ISO strings sort by date; 12 looks for 2,520 days', datetime.date(2026, 3, 7).weekday() == 5 and datetime.date(2026, 3, 9).weekday() == 0 and sorted(['2026-03-10', '2026-02-27', '2026-03-09']) == ['2026-02-27', '2026-03-09', '2026-03-10'] and math.ceil(math.log2(2521)) == 12)

# ---------------------------------------------------------------- L10 search on the answer
def smallest_true(lo, hi, pred, log=None):
    a, b = lo, hi + 1
    while a < b:
        mid = (a + b) // 2
        if log is not None: log.append(mid)
        if pred(mid): b = mid
        else: a = mid + 1
    return a if a <= hi else None
imp = lambda q: 0.15 * math.sqrt(q)
lg = []; lo, hi = 0, 64
while lo < hi:
    mid = (lo + hi) // 2; lg.append((lo, hi, mid, round(imp(mid), 3)))
    if imp(mid) >= 1: hi = mid
    else: lo = mid + 1
ok('l10 impact trace: mids 32, 48, 40, 44, 46, 45 and answer 45', [m for _, _, m, _ in lg] == [32, 48, 40, 44, 46, 45] and lo == 45 and [v for *_, v in lg] == [0.849, 1.039, 0.949, 0.995, 1.017, 1.006] and abs((1 / 0.15) ** 2 - 44.44) < 0.01)
worstc = 0
for size in range(1, 200):
    for first in range(size + 1):
        lg = []; smallest_true(0, size - 1, lambda x: x >= first, lg); worstc = max(worstc, len(lg) - math.ceil(math.log2(size + 1)))
        if lg and (min(lg) < 0 or max(lg) > size - 1): worstc = 99
lg = []; r12 = smallest_true(0, 10 ** 12, lambda x: x >= 123456789, lg)
ok('l10 smallest_true: at most ceil(log2(range + 1)) calls, never outside the range; 40 for 1e12; 30 for 1e9', worstc == 0 and r12 == 123456789 and len(lg) == 40 and math.ceil(math.log2(10 ** 9)) == 30 and 2 ** 30 == 1073741824)
isq = lambda n: smallest_true(0, n + 1, lambda x: x * x > n) - 1
ok('l10 isqrt matches math.isqrt, 1e18; ending at n fails for 0 and 1 only', all(isq(n) == math.isqrt(n) for n in range(3000)) and isq(10 ** 18) == 10 ** 9 and isq(10 ** 18 - 1) == 999999999 and [n for n in range(50) if smallest_true(0, n, lambda x: x * x > n) is None] == [0, 1])
def bond_price(y, coupon, years, face): return sum(coupon / (1 + y) ** t for t in range(1, years + 1)) + face / (1 + y) ** years
def yfp(price, coupon, years, face, k=None):
    lo, hi = 0.0, 1.0
    if price > bond_price(lo, coupon, years, face) or price < bond_price(hi, coupon, years, face): return None
    while True:
        mid = (lo + hi) / 2; p = bond_price(mid, coupon, years, face)
        if k is not None: k.append(mid)
        if abs(p - price) <= 0.01: return mid
        if p > price: lo = mid
        else: hi = mid
k = []; y95 = yfp(95.0, 4, 5, 100, k)
ok('l10 bond: 95.67 at 5%, 91.58 at 6%, 120 at 0, 7 at 100%; yield 5.16% in 15 halvings', round(bond_price(0.05, 4, 5, 100), 2) == 95.67 and round(bond_price(0.06, 4, 5, 100), 2) == 91.58 and bond_price(0, 4, 5, 100) == 120 and abs(bond_price(1, 4, 5, 100) - 7) < 1e-12 and round(y95, 4) == 0.0516 and len(k) == 15)
def exact_y(price, c, yrs, face):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if bond_price(mid, c, yrs, face) > price: lo = mid
        else: hi = mid
    return lo
ok('l10 rounded test yields: any yield within 1p of the price rounds to the expected value', all(round(exact_y(a[0] + 0.01, *a[1:]), 3) == round(exact_y(a[0] - 0.01, *a[1:]), 3) == e for a, e in (((95, 4, 5, 100), 0.052), ((100, 5, 5, 100), 0.05), ((92.5, 3, 7, 100), 0.043), ((850, 0, 10, 1000), 0.016))))
ok('l10 trap: non-monotone test returns 5, first True is 2', smallest_true(0, 7, lambda d: [97, 99, 102, 98, 96, 101, 103, 105][d] > 100) == 5 and smallest_true(0, 7, lambda d: max([97, 99, 102, 98, 96, 101, 103, 105][:d + 1]) > 100) == 2)
Nc = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_call(sig, S=100, K=100, r=0.05, Tm=1):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * Tm) / (sig * math.sqrt(Tm)); return S * Nc(d1) - K * math.exp(-r * Tm) * Nc(d1 - sig * math.sqrt(Tm))
lo, hi = 0.20, 0.30
for _ in range(20):
    mid = (lo + hi) / 2
    if bs_call(mid) > 12: hi = mid
    else: lo = mid
ok('l10 Black-Scholes 10.45, 12.34, 14.23; implied vol 0.2411 after 20 halvings; rising in sigma', [round(bs_call(s), 2) for s in (0.2, 0.25, 0.3)] == [10.45, 12.34, 14.23] and round(lo, 4) == 0.2411 and all(bs_call(s + 0.01) > bs_call(s) for s in [i / 100 for i in range(1, 100)]))
ok('l10 quiz: 26 days, 20 halvings for 1e-6, 27 for 1e-8, next test 3250, 11 tests', smallest_true(1, 100, lambda d: 120 + 35 * d >= 1000) == 26 and 120 + 35 * 25 == 995 and math.ceil(1000 / 35) == 29 and [min(k for k in range(60) if 2 ** -k < e) for e in (1e-6, 1e-8)] == [20, 27] and (2500 + 4000) / 2 == 3250 and math.ceil(math.log2(1500)) == 11 and 2 ** 26 == 67108864)
ok('review-3 doubling at 5%: 15 years; 1.05^14 = 1.980', smallest_true(1, 100, lambda n: 1.05 ** n >= 2) == 15 and round(1.05 ** 14, 3) == 1.980 and round(1.05 ** 15, 3) == 2.079)

# ---------------------------------------------------------------- L11 insertion sort
def insertion_sort(xs, strict=True):
    a = list(xs); comps = 0
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0:
            comps += 1
            if (a[j] > key) if strict else (a[j] >= key): a[j + 1] = a[j]; j -= 1
            else: break
        a[j + 1] = key
    return a, comps
ok('l11 comparison counts 12, 4, 10, 5, 9, 3, 7', [insertion_sort(x)[1] for x in ([5, 2, 4, 6, 1, 3], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [3, 1, 3, 1], [1, 2, 4, 3, 5, 6, 8, 7], [3, 1, 2], [4, 3, 2, 1, 5])] == [12, 4, 10, 5, 9, 3, 7])
ok('l11 worst n(n-1)/2 (499,500; 780; about 5e7 for 10,000), best n-1', insertion_sort(range(1000, 0, -1))[1] == 499500 and 40 * 39 // 2 == 780 and insertion_sort(range(1000))[1] == 999 and 10000 * 9999 // 2 == 49995000)
worst_i = max(insertion_sort(p)[1] for p in itertools.permutations(range(7)))
ok('l11 no order of 7 values costs more than 21', worst_i == 21)
def swap_sort(a):
    a = list(a); comps = 0
    for i in range(1, len(a)):
        for j in range(i, 0, -1):
            comps += 1
            if a[j - 1] > a[j]: a[j - 1], a[j] = a[j], a[j - 1]
    return a, comps
ok('l11 no-break version costs 15 on sorted 6', swap_sort([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6], 15))
def ins_by(xs, strict=True):
    a = list(xs)
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and ((a[j][0] > key[0]) if strict else (a[j][0] >= key[0])): a[j + 1] = a[j]; j -= 1
        a[j + 1] = key
    return a
tr5 = [('09:00:01', 'a'), ('09:00:03', 'b'), ('09:00:02', 'c'), ('09:00:03', 'd'), ('09:00:02', 'e')]
ok('l11 stable with >, not with >=; same as sorted(key=...)', ins_by([(101, 'A'), (100, 'x'), (101, 'B')]) == [(100, 'x'), (101, 'A'), (101, 'B')] and ins_by([(101, 'A'), (100, 'x'), (101, 'B')], False) == [(100, 'x'), (101, 'B'), (101, 'A')] and ins_by(tr5) == sorted(tr5, key=lambda t: t[0]))
ok('l11 new level three from the end: 4 comparisons', insertion_sort([99.96, 99.97, 99.98, 99.99, 100.01, 99.975])[1] - insertion_sort([99.96, 99.97, 99.98, 99.99, 100.01])[1] == 4 and math.ceil(math.log2(1001)) == 10)
class Cnt:
    n = 0
    def __init__(s, v): s.v = v
    def __lt__(s, o): Cnt.n += 1; return s.v < o.v
def sort_cmps(vals):
    Cnt.n = 0; sorted(Cnt(v) for v in vals); return Cnt.n
m = 20000; shuffled = list(range(m)); rng.shuffle(shuffled)
c_sorted, c_rev, c_rand = sort_cmps(range(m)), sort_cmps(range(m, 0, -1)), sort_cmps(shuffled)
ok('l11 sorted() is O(n) on ordered input and about n log2 n on random input', c_sorted == m - 1 and 0.8 * m * math.log2(m) < c_rand < 1.1 * m * math.log2(m))
# Finding 7: l11 Q3 option c says O(n) "is only for input already in order"; reversed input is O(n) too.
ok('FINDING 7, l11 Q3: sorted() is O(n) "only for input already in order" (reversed input also costs n - 1 comparisons)', c_rev > 5 * m)
ok('l11 Q3 fix text: exactly reversed input costs n - 1 comparisons', c_rev == m - 1)

# ---------------------------------------------------------------- L12 merge sort
def merge(a, b): return merge_cmp(a, b)[0]
def merge_sort(xs, lt=False):
    if len(xs) <= 1: return list(xs)
    mid = len(xs) // 2; a, b = merge_sort(xs[:mid], lt), merge_sort(xs[mid:], lt)
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if (a[i][0] < b[j][0]) if lt else (a[i][0] <= b[j][0]): out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1
    return out + a[i:] + b[j:]
ok('l12 merge example, 7 comparisons', merge_cmp([2, 5, 9, 12], [3, 4, 10, 15]) == ([2, 3, 4, 5, 9, 10, 12, 15], 7))
ok('l12 stable with <= (B, A, C), not with <', [t[1] for t in merge_sort([(101, 'A'), (100, 'B'), (101, 'C')])] == ['B', 'A', 'C'] and [t[1] for t in merge_sort([(101, 'A'), (100, 'B'), (101, 'C')], True)] == ['B', 'C', 'A'])
ok('l12 a base case at len 0 only never ends on [7]', raises(lambda: (lambda g: g(g, [7]))(lambda g, xs: xs if len(xs) == 0 else merge(g(g, xs[:len(xs) // 2]), g(g, xs[len(xs) // 2:]))), RecursionError))
ok('l12 sizes: 24 v 28; 20 levels; half a trillion; 2e8; ratio 2.1', 8 * 3 == 24 and 8 * 7 // 2 == 28 and round(math.log2(10 ** 6)) == 20 and abs(10 ** 6 * (10 ** 6 - 1) / 2 / 5e11 - 1) < 0.01 and 20000 * 19999 // 2 == 199990000 and round(2 * math.log2(2e6) / math.log2(1e6), 1) == 2.1)
def sort_count(xs):
    if len(xs) <= 1: return list(xs), 0
    mid = len(xs) // 2; a, x = sort_count(xs[:mid]); b, y = sort_count(xs[mid:])
    out, i, j, c = [], 0, 0, x + y
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1; c += len(a) - i
    return out + a[i:] + b[j:], c
okc = all(sort_count(x)[1] == inv_brute(x) for x in ([rng.randrange(30) for _ in range(rng.randrange(0, 60))] for _ in range(300)))
big = [(i * 7919) % 20011 for i in range(20000)]
ok('l12 merge inversion count == brute force; 20,000-item count 99,930,366; reversed 3000 = 4,498,500', okc and sort_count(big)[1] == 99930366 and sort_count(list(range(3000, 0, -1)))[1] == 4498500)
ok('l12 Kendall tau 1 - 2*3/15 = 0.6', abs((12 - 3) / 15 - 0.6) < 1e-12 and 6 * 5 // 2 == 15)
ok('l12 external sort: 13 runs of about 15 GB fit 16 GB', 15 < 200 / 13 < 16)
# Finding 2: l12 S2 fb test-9 says "Sorting the joined list, or pop(0), is too slow" (limit: 5 seconds per homework-2 I5).
a50, b50 = list(range(0, 100000, 2)), list(range(1, 100000, 2))
t0 = time.time(); srt = sorted(a50 + b50); dt = time.time() - t0
ok('FINDING 2, l12 S2 fb test-9: "Sorting the joined list ... is too slow" (it takes milliseconds and passes test 9)', not (srt == list(range(100000)) and dt < 1.0))

# ---------------------------------------------------------------- L13 quicksort
def partition(xs, lo, hi, cnt=None):
    pivot = xs[hi]; i = lo
    for j in range(lo, hi):
        if cnt is not None: cnt[0] += 1
        if xs[j] <= pivot: xs[i], xs[j] = xs[j], xs[i]; i += 1
    xs[i], xs[hi] = xs[hi], xs[i]; return i
def part(xs, lo=0, hi=None):
    xs = list(xs); p = partition(xs, lo, len(xs) - 1 if hi is None else hi); return p, xs
ok('l13 Lomuto traces', part([7, 2, 9, 4, 1, 8, 5]) == (3, [2, 4, 1, 5, 9, 8, 7]) and part([9, 3, 7, 1, 8, 2, 6, 5], 2, 5) == (3, [9, 3, 1, 2, 8, 7, 6, 5]) and part([2, 1]) == (0, [1, 2]) and part([3, 5, 4, 1]) == (0, [1, 5, 4, 3]) and part([3, 8, 2, 5, 1, 4]) == (3, [3, 2, 1, 4, 8, 5]) and part([4, 4, 4, 4]) == (3, [4, 4, 4, 4]))
def quicksort(xs, pivot='last', cnt=None, key=None):
    xs = list(xs); st = [(0, len(xs) - 1)]; depth = 0
    while st:
        lo, hi = st.pop()
        if lo >= hi: continue
        if pivot == 'random': r = rng.randint(lo, hi); xs[r], xs[hi] = xs[hi], xs[r]
        if pivot == 'first': xs[lo], xs[hi] = xs[hi], xs[lo]
        if key:
            pv = key(xs[hi]); i = lo
            for j in range(lo, hi):
                if key(xs[j]) <= pv: xs[i], xs[j] = xs[j], xs[i]; i += 1
            xs[i], xs[hi] = xs[hi], xs[i]; p = i
        else: p = partition(xs, lo, hi, cnt)
        st.append((p + 1, hi)); st.append((lo, p - 1))
    return xs
c1, c2, c3, c4, c5 = [0], [0], [0], [0], [0]
quicksort([7, 2, 9, 4, 1, 8, 5], cnt=c1); quicksort(range(1, 8), cnt=c2); quicksort(range(1000), cnt=c3); quicksort(range(2000), cnt=c5)
ok('l13 comparisons: 12 shuffled example, 21 sorted 7, 499,500 sorted 1000, 1,999,000 sorted 2000', (c1[0], c2[0], c3[0], c5[0]) == (12, 21, 499500, 1999000))
wq = 0
for p in itertools.permutations(range(7)):
    c = [0]; quicksort(p, cnt=c); wq = max(wq, c[0])
ok('l13 21 is the most for 7 values (last pivot, every order)', wq == 21)
# Finding 6: l13 S5 slip 14 ("You assumed even splits"): even splits of 7 cost 6 + 2 + 2 = 10, not 14.
best7 = min((lambda cc: (quicksort(p, cnt=cc), cc[0])[1])([0]) for p in itertools.permutations(range(7)))
ok('FINDING 6, l13 S5 slip 14 "You assumed even splits" (even splits of 7 values cost 10 comparisons)', best7 == 14)
ok('l13 not stable: [(5,a),(5,b),(1,c)] -> c, b, a', quicksort([(5, 'a'), (5, 'b'), (1, 'c')], key=lambda t: t[0]) == [(1, 'c'), (5, 'b'), (5, 'a')])
n = 20001; tot = 0; reps = 30
for _ in range(reps):
    v = list(range(n)); rng.shuffle(v); c = [0]; quicksort(v, 'random', c); tot += c[0]
exact = 2 * (n + 1) * sum(1 / k for k in range(1, n + 1)) - 4 * n
ok('l13 random-pivot quicksort: mean comparisons match 2(n+1)H_n - 4n (leading term 1.39 n log2 n)', abs(tot / reps / exact - 1) < 0.02 and abs(2 * math.log(2) - 1.39) < 0.005)
c = [0]; v = list(range(n)); quicksort(v, 'random', c)
ok('l13 random pivot on sorted input stays near n log n (not n^2/2)', c[0] < 3 * n * math.log2(n))
def quickselect(xs, k, cnt, pivot='random'):
    xs = list(xs); lo, hi = 0, len(xs) - 1
    while lo < hi:
        if pivot == 'random': r = rng.randint(lo, hi); xs[r], xs[hi] = xs[hi], xs[r]
        p = partition(xs, lo, hi, cnt)
        if k == p: return xs[p]
        if k < p: hi = p - 1
        else: lo = p + 1
    return xs[lo]
def qs_mean(frac, n=20001, reps=400):
    tot = 0
    for _ in range(reps):
        v = list(range(n)); rng.shuffle(v); c = [0]; assert quickselect(v, int(frac * n), c) == int(frac * n); tot += c[0]
    return tot / reps / n
m50, m05, m00 = qs_mean(0.5), qs_mean(0.05), qs_mean(0.0)
ok('l13 quickselect mean comparisons: about 3.4n at the median, 2.4n at 5%, 2n at the end (within 2n to 4n)', abs(m50 - (2 + 2 * math.log(2))) < 0.15 and abs(m05 - 2 * (1 - 0.05 * math.log(0.05) - 0.95 * math.log(0.95))) < 0.15 and abs(m00 - 2) < 0.15)
ok('l13 sizes: 1e7 log2 = 230 million; 20 to 40 million; 20 million for 1e6', round(1e7 * math.log2(1e7) / 1e7) == 23 and round(1e6 * math.log2(1e6) / 1e6) == 20)
def three_way_levels(xs):
    if len(set(xs)) <= 1: return 1 if xs else 0
    p = rng.choice(xs); return 1 + max(three_way_levels([x for x in xs if x < p]), three_way_levels([x for x in xs if x > p]))
lv = {three_way_levels([rng.randrange(3) for _ in range(3000)]) for _ in range(200)}
ok('l13 three-way partition on three distinct values: two or three levels', lv == {2, 3})
c = [0]; quicksort([7] * 400, cnt=c)
ok('l13 Lomuto on equal values is quadratic', c[0] == 400 * 399 // 2)
# Finding 5: homework-3 I6 fb test-8: "Test 8 is already sorted. A fixed end pivot makes that O(n^2)". Test 8 asks for k = 1 (the largest).
c = [0]; r = quickselect(list(range(5000)), 5000 - 1, c, pivot='last')
ok('FINDING 5, homework-3 I6 test 8: a fixed last pivot is O(n^2) on it (it takes n - 1 = 4,999 comparisons)', not (r == 4999 and c[0] == 4999))
def qsel_first(xs, k):
    xs = list(xs); lo, hi, c = 0, len(xs) - 1, [0]
    while lo < hi:
        xs[lo], xs[hi] = xs[hi], xs[lo]; p = partition(xs, lo, hi, c)
        if k == p: break
        if k < p: hi = p - 1
        else: lo = p + 1
    return c[0]
ok('homework-3 I6 fix text: a fixed first pivot is quadratic on test 8 (12,497,500 comparisons)', qsel_first(range(5000), 4999) == 5000 * 4999 // 2)
c = [0]; quickselect(list(range(3000)), 1500, c, pivot='last')
ok('l13 S8 test 7: a fixed last pivot is quadratic there (about 3.4 million comparisons)', c[0] == sum(range(1500, 3000)))
sizes = [(i * 7919) % 10007 for i in range(100001)]
ok('l13/hw3 order statistics 5003 and 8005', sorted(sizes)[50000] == 5003 and sorted(sizes)[100001 - 20000] == 8005)

# ---------------------------------------------------------------- L14 greedy
def greedy(amount, coins):
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c: out.append(c); amount -= c
    return out if amount == 0 else None
def best_coins(top, coins):
    INF = 10 ** 9; d = [0] + [INF] * top
    for a in range(1, top + 1): d[a] = min((d[a - c] + 1 for c in coins if c <= a), default=INF)
    return d
def fails(coins, top=2000):
    d = best_coins(top, coins); return [a for a in range(1, top + 1) if len(greedy(a, coins)) != d[a]]
UK = [1, 2, 5, 10, 20, 50, 100, 200]
ok('l14 greedy is optimal for UK coins (with and without the pound coins), 1-2-5-10, powers of 3, US coins', fails(UK) == [] and fails(UK[:6]) == [] and fails([1, 2, 5, 10]) == [] and fails([1, 3, 9, 27]) == [] and fails([1, 5, 10, 25]) == [])
ok('l14 87p in 5 coins; 1-3-4 fails first at 6, and at 6 and 10 only up to 10', greedy(87, UK[:6]) == [50, 20, 10, 5, 2] and fails([1, 3, 4], 10) == [6, 10] and [len(greedy(a, [1, 3, 4])) for a in range(1, 11)] == [1, 2, 1, 1, 2, 3, 2, 2, 3, 4] and best_coins(10, [1, 3, 4])[6] == 2 and best_coins(10, [1, 3, 4])[10] == 3 and best_coins(10, [1, 3, 4])[9] == 3)
ok('l14 1-10-25 at 30: 6 v 3; 1-5-12 at 15: 4 v 3; greedy stuck on 3 with [5, 2]; 1e6 in 5000 coins', len(greedy(30, [1, 10, 25])) == 6 and best_coins(30, [1, 10, 25])[30] == 3 and len(greedy(15, [1, 5, 12])) == 4 and best_coins(15, [1, 5, 12])[15] == 3 and greedy(3, [5, 2]) is None and len(greedy(10 ** 6, UK)) == 5000)
def by_key(iv, key):
    count, end = 0, float('-inf')
    for s, e in sorted(iv, key=key):
        if s >= end: count += 1; end = e
    return count
def brute(iv):
    best = 0
    for r in range(len(iv), 0, -1):
        for sub in itertools.combinations(iv, r):
            s = sorted(sub)
            if all(s[i][1] <= s[i + 1][0] for i in range(len(s) - 1)): return r
    return 0
DIARY = [(9, 15), (9.5, 10.5), (10.5, 11.5), (11, 12.5), (12, 13), (13.5, 14.5), (14, 16)]
good = True; start_bad = short_bad = 0
for _ in range(1500):
    iv = [(s, s + rng.randrange(1, 8)) for s in (rng.randrange(0, 20) for _ in range(rng.randrange(0, 9)))]
    b = brute(iv); good &= by_key(iv, lambda t: t[1]) == b
    start_bad += by_key(iv, lambda t: t) < b; short_bad += by_key(iv, lambda t: t[1] - t[0]) < b
ok('l14 earliest finish first == brute-force optimum on 1,500 random diaries; start-first and shortest-first both fail somewhere', good and start_bad > 0 and short_bad > 0)
ok('l14 diary: 4 by finish, 1 by start, optimum 4; shortest-first counterexample', by_key(DIARY, lambda t: t[1]) == 4 and by_key(DIARY, lambda t: t) == 1 and brute(DIARY) == 4 and by_key([(1, 5), (4, 7), (6, 10)], lambda t: t[1] - t[0]) == 1 and brute([(1, 5), (4, 7), (6, 10)]) == 2)
tr = [(6000, 300), (5000, 200), (5000, 200)]
best01 = max(sum(p for _, p in s) for r in range(4) for s in itertools.combinations(tr, r) if sum(c for c, _ in s) <= 10000)
ok('l14 knapsack: fractional 460, whole 400, greedy whole 300', 300 + 4000 * 200 / 5000 == 460 and best01 == 400)
ok('l14 market order 100,031; slips 100,020 and 100,045', abs(300 * 100.02 + 500 * 100.03 + 200 * 100.05 - 100031) < 1e-6 and abs((100.02 + 100.03 + 100.05 + 100.08) / 4 * 1000 - 100045) < 1e-6)
def sp(s1, s2, rho, sig=0.1): return (s1 * sig + s2 * sig) / 2 / math.sqrt((sig * sig + sig * sig + 2 * rho * sig * sig) / 4)
ok('l14 pair Sharpe (S1+S2)/sqrt(2+2rho): 1.47, 1.77, 1.70', all(abs(sp(a, b, r) - (a + b) / math.sqrt(2 + 2 * r)) < 1e-12 for a, b, r in ((1.5, 1.4, 0.95), (1.5, 1.0, 0), (1.4, 1.0, 0))) and [round(sp(a, b, r), 2) for a, b, r in ((1.5, 1.4, 0.95), (1.5, 1.0, 0), (1.4, 1.0, 0))] == [1.47, 1.77, 1.70])
items = [(4, 20), (6, 18), (5, 10)]
ok('l14 Q2 fractional knapsack 38 (ratios 5, 3, 2); all values 48', [v / w for w, v in items] == [5, 3, 2] and 20 + 18 == 38 and 4 + 6 == 10 and 20 + 18 + 10 == 48)
# Finding 1: l14 Q2 fb "whole" (30): "You took whole items by value: 20 and 10". Whole items in value order are 20 then 18 (both fit): 38.
cap, got = 10, 0
for w, v in sorted(items, key=lambda t: -t[1]):
    if w <= cap: cap -= w; got += v
ok('FINDING 1, l14 Q2 slip 30 "You took whole items by value: 20 and 10" (by value gives 20 + 18 = 38)', got == 30)
cap, got = 10, 0
for w, v in sorted(items):
    if w <= cap: cap -= w; got += v
ok('l14 Q2: the two lightest items whole give 30 (the proposed fix text)', got == 30)

# ---------------------------------------------------------------- reviews and homework
ok('review-1: 570, 1200, 8000; 9x pairs', 190 * 3 == 570 and 20 * 20 * 3 == 1200 and abs((6000 * 5999 / 2) / (2000 * 1999 / 2) - 9) < 0.01 and abs(6000 * 5999 / 2 / 1.8e7 - 1) < 0.01)
ok('hw1: 31,187,500; 62,500,000; 62,375,000; ceil(log3 n) steps', 500 * 499 // 2 * 250 == 31187500 and 500 * 500 * 250 == 62500000 and 500 * 499 * 250 == 62375000
   and all((lambda n: (lambda k: 3 ** k >= n and (k == 0 or 3 ** (k - 1) < n))(sum(1 for _ in iter((lambda s=[1]: (s.__setitem__(0, s[0] * 3) or True) if s[0] < n else None), None))))(n) for n in (1, 2, 3, 4, 9, 10, 27, 28, 1000)))
ok('hw1 screener: 8,997,000 calls, 2.25e9 day-steps, 4,498,500 halved', 3000 * 2999 == 8997000 and abs(8997000 * 250 / 2.25e9 - 1) < 0.01 and 3000 * 2999 // 2 == 4498500)
def best_trade(prices):
    best, low = 0, None
    for p in prices:
        if low is None or p < low: low = p
        elif p - low > best: best = p - low
    return best
ok('hw1 best_trade == pair loop on random lists', all(best_trade(x) == max([0] + [x[j] - x[i] for i in range(len(x)) for j in range(i + 1, len(x))]) for x in ([rng.randrange(50) for _ in range(rng.randrange(0, 25))] for _ in range(400))) and abs(200001 ** 2 / 2 / 2e10 - 1) < 0.01)
def days_needed(sizes, cap):
    d, load = 1, 0
    for s in sizes:
        if load + s > cap: d += 1; load = 0
        load += s
    return d
ok('hw3 capacity: days needed never rises with capacity; 15 for 1..10 in 5 days', all(days_needed(list(range(1, 11)), c) >= days_needed(list(range(1, 11)), c + 1) for c in range(10, 60)) and min(c for c in range(10, 56) if days_needed(list(range(1, 11)), c) <= 5) == 15)
ok('hw3 report: 2.3e8, 24 comparisons, 12,000, 5e9 about twenty times, 5e13', abs(1e7 * math.log2(1e7) / 2.3e8 - 1) < 0.02 and math.ceil(math.log2(10 ** 7 + 1)) == 24 and 500 * 24 == 12000 and 19 < 5e9 / (1e7 * math.log2(1e7)) < 23 and abs(1e7 * (1e7 - 1) / 2 / 5e13 - 1) < 0.01)
class Looks:
    def __init__(s, d): s.data = list(d); s.looks = 0
    def __len__(s): return len(s.data)
    def __getitem__(s, i): s.looks += 1; return s.data[i]
def find_trade(ring, seq):
    lo, hi = 0, len(ring) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ring[mid] == seq: return mid
        if ring[lo] <= ring[mid]:
            if ring[lo] <= seq < ring[mid]: hi = mid - 1
            else: lo = mid + 1
        else:
            if ring[mid] < seq <= ring[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1
Wr = Looks([1000000 + 3 * ((j + 137017) % 200000) for j in range(200000)]); per = []
for s in (1300000, 1300001, 1411051, 1411048, 1000000, 1599997, 999997, 1600000):
    b0 = Wr.looks; find_trade(Wr, s); per.append(Wr.looks - b0)
ok('hw3 ring: oldest trade in slot 62,983; the model answer reads under 100 slots a search', Wr.data.index(1000000) == 62983 and max(per) < 100)

print(f'{N[0]} checks, {len(FAILS)} failing')
for f_ in FAILS: print('  finding:', f_)
sys.exit(1 if FAILS else 0)
