#!/usr/bin/env python3
"""Concept checks for algo-think L1 to L3 (round 1 blind audit, 12 Nov 2026).

Every complexity, operation-count and code-behaviour claim the audit ledger rests on
is recomputed here by running the algorithm with a counter, or by brute force.

Run: python3 docs/reports/algo-think-L1-3-concepts.py
Written on CPython 3.13 (64-bit); Pyodide 0.27.7 is CPython 3.12.7 on wasm32, and the
three Pyodide-only facts (recursion limit 1000, 16-byte floats, 4-byte list slots) were
read from the local Pyodide build and are quoted in the ledger, not asserted here.

Exit code: 0 when every check passes. A check marked FINDING tests a sentence of the
content as written; it fails while the content is wrong and is listed in
docs/reviews/audit-algo-think-1-3.md under the same number.
"""
import bisect
import itertools
import math
import random
import sys
import tracemalloc
from functools import lru_cache

sys.setrecursionlimit(20000)
RESULTS = []


def check(name, ok, detail="", finding=None):
    RESULTS.append((name, bool(ok), detail, finding))


# Fix pass (12 Nov 2026): each FINDING check now tests the corrected sentence. It reads the
# content string with T() and recomputes the claim the corrected sentence makes.
import json
import os
CDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "algo-think")
_CACHE = {}


def T(fname, path):
    if fname not in _CACHE:
        with open(os.path.join(CDIR, fname), encoding="utf-8") as fh:
            _CACHE[fname] = json.load(fh)
    o = _CACHE[fname]
    for k in path.split("."):
        o = o[int(k)] if k.isdigit() else o[k]
    return o


# ---------------------------------------------------------------- Level 1
# l1: scan, pair loop, grid
def scan_comparisons(prices):
    c, best = 0, prices[0]
    for p in prices[1:]:
        c += 1
        if p > best:
            best = p
    return c


def pair_count(n):
    return sum(1 for i in range(n) for j in range(i + 1, n))


P8 = [102, 98, 105, 101, 99, 108, 104, 100]
check("l1 scan 7 comparisons on 8, n-1 in general", scan_comparisons(P8) == 7
      and all(scan_comparisons(list(range(n))) == n - 1 for n in range(1, 40)))
check("l1 pairs 28/120/496, n(n-1)/2", [pair_count(n) for n in (8, 16, 32)] == [28, 120, 496]
      and all(pair_count(n) == n * (n - 1) // 2 for n in range(0, 60)))
check("l1 pair loop does zero work for n=0,1", pair_count(0) == 0 and pair_count(1) == 0)
ben = 1 + 7 + sum(1 for k in range(1, 8) if P8[k] > max(P8[:k])) + 1
check("l1 Ben counts 11 (assignments, comparisons, return)", ben == 11)
check("l1 2,000 stocks: 1,999,000 pairs; x250 about 5e8", 2000 * 1999 // 2 == 1999000
      and abs(1999000 * 250 / 5e8 - 1) < 0.01)
check("l1 quiz universe factor about 25", abs((10000 * 9999 / 2) / (2000 * 1999 / 2) - 25) < 0.05)

# l2: crossovers and the big-O definition
check("l2 2^n > n^2 for good from n=5 (4 is a tie)", 2 ** 4 == 4 ** 2 and 3 ** 2 > 2 ** 3
      and all(2 ** n > n * n for n in range(5, 2000)))
f = lambda n: 3 * n * n + 50 * n + 7
check("l2 3n^2+50n+7 < 4n^2 exactly from n=51", f(50) == 10007 and f(51) == 10360 and 4 * 51 ** 2 == 10404
      and all(f(n) < 4 * n * n for n in range(51, 5000)) and not f(50) < 4 * 50 * 50)
check("l2 c=60, n0=1 proves the bound", all(f(n) <= 60 * n * n for n in range(1, 5000)))
check("l2 50n vs n^2: tie at 50, A cheaper from 51", 50 * 50 == 50 ** 2 and 50 * 20 == 1000 and 20 ** 2 == 400
      and all(50 * n < n * n for n in range(51, 3000)))
check("l2 3n passes 1e6 at n=333,334", 3 * 333333 < 10 ** 6 < 3 * 333334)
check("l2 doubling table 11 / 2048 / 22528 / 4194304; n log n ratio 2.2",
      math.log2(2048) == 11 and 2048 * 11 == 22528 and 2048 ** 2 == 4194304 and abs(22528 / 10240 - 2.2) < 1e-9)
check("l2 2n log2 n passes 40n once log2 n > 20", all((2 * n * math.log2(n) > 40 * n) == (math.log2(n) > 20)
                                                    for n in (2 ** 19, 2 ** 20, 2 ** 20 + 1, 2 ** 21)))
# FINDING 6: options that are true statements under the lesson's own definition are graded wrong
g = lambda n: 2 * n * math.log2(n) + 40 * n + 9
is_O_n2logn = all(g(n) <= 60 * n * n * math.log2(n) for n in range(2, 5000))
check("l2 s6 (fixed): the O(n^2 log n) option is called true but not the smallest class; prose states the convention",
      is_O_n2logn and "True as an upper bound, but not the smallest class" in T("l2-big-o.json", "screens.6.widget.options.3.why")
      and "smallest class that holds" in T("l2-big-o.json", "screens.6.prose"),
      "the bound holds with c=60, n0=2, so the option is a true statement", finding=6)
check("l2 quiz (fixed): 5n is O(n^2) as a loose bound, and the why says so; summary names functions, not classes",
      all(5 * n <= 5 * n * n for n in range(1, 5000))
      and "True as a loose upper bound" in T("l2-big-o.json", "quiz.0.widget.options.1.why")
      and "O(\\log n)" not in T("l2-big-o.json", "summary.ideas.2"),
      "5n <= 5n^2 for n >= 1, so 'O(n^2)' is a true statement", finding=6)


# l3: memory
def prog_a(prices):
    best = prices[0]
    for p in prices[1:]:
        best = max(best, p)
    return best


def prog_a_fixed(prices):
    best = prices[0]
    for p in prices:
        best = max(best, p)
    return best


def peak(fn, *a):
    tracemalloc.start()
    try:
        fn(*a)
        return tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()


p4, p5 = [float(i) for i in range(10 ** 4)], [float(i) for i in range(10 ** 5)]
a4, a5 = peak(prog_a, p4), peak(prog_a, p5)
check("l3 s0 (old program A, for p in prices[1:]) is O(n): the slice copies n-1 references", a5 > 9 * a4 > 70000,
      f"peak bytes {a4} at n=1e4, {a5} at n=1e5")
_src = T("l3-memory.json", "screens.0.prose").split("```python\n")[1].split("# B")[0]
_ns = {}
exec("def prog_a_content(prices):\n" + "".join("    " + ln + "\n" for ln in _src.splitlines()) + "    return best", _ns)
check("l3 s0 (fixed): program A as now written holds O(1) extra values and finds the max",
      "[1:]" not in _src and peak(_ns["prog_a_content"], p5) < 2000 and _ns["prog_a_content"](P8) == 108,
      f"program A in the content: {_src!r}", finding=1)
check("l3 s0 proposed fix (loop over prices) is O(1) and still correct",
      peak(prog_a_fixed, p5) < 2000 and prog_a_fixed(P8) == 108 == prog_a(P8))
check("l3 reverse in place: floor(n/2) swaps, 500 for 1,001",
      1001 // 2 == 500 and all(sum(1 for _ in range(n // 2)) == n // 2 for n in (8, 1001)))
if sys.maxsize > 2 ** 32:
    xs = [float(i) for i in range(1_000_000)]
    check("l3 getsizeof list comprehension of 1e6 floats is 8,448,728 and a float is 24 (64-bit CPython)",
          sys.getsizeof(xs) == 8448728 and sys.getsizeof(xs[0]) == 24,
          f"{sys.getsizeof(xs)} {sys.getsizeof(xs[0])}")
    check("l3 about 32.4 MB together", abs((8448728 + 24e6) / 1e6 - 32.4) < 0.1)
    del xs
pre = [0]
for v in [3, 1, 4, 1, 5]:
    pre.append(pre[-1] + v)
check("l3 prefix sums [0,3,4,8,9,14]; days 1 to 3 total 6 = pre[4]-pre[1]", pre == [0, 3, 4, 8, 9, 14]
      and pre[4] - pre[1] == 6 == 1 + 4 + 1)
check("l3 s5 hint (fixed): days 1 to 3 total '9 - 3'", 9 - 3 == pre[4] - pre[1]
      and "$9 - 3$: `pre[4] - pre[1]`" in T("l3-memory.json", "screens.5.hints.1.text"),
      "pre[4] is 9, so the subtraction is 9 - 3 = 6; 8 - 3 is 5 and uses pre[3]", finding=2)
check("l3 range(1000)[10:20] sums to 145", sum(range(1000)[10:20]) == 145)


def total_rec(xs, i=0, d=1, deepest=[0]):
    deepest[0] = max(deepest[0], d)
    if i == len(xs):
        return 0
    return xs[i] + total_rec(xs, i + 1, d + 1, deepest)


dd = [0]
check("l3 recursive total: 21 and n+1 = 6 open calls", total_rec([5, 3, 8, 1, 4], 0, 1, dd) == 21 and dd[0] == 6)
check("l3 minute bars: 4,914,000 values a stock; 200 stocks 7.86 GB numpy, 31.45 GB lists",
      10 * 252 * 390 * 5 == 4914000 and abs(200 * 4914000 * 8 / 1e9 - 7.86) < 0.005
      and abs(200 * 4914000 * 32 / 1e9 - 31.45) < 0.005 and abs(50 * 4914000 * 8 / 1e9 - 1.97) < 0.005)
gains = (p for p in [120, -40, 330, -15] if p > 0)
s_ = sum(gains)
try:
    max(gains)
    exhausted = False
except ValueError:
    exhausted = True
check("l3 quiz: generator sums to 450 then is exhausted", s_ == 450 and exhausted)
rs = [random.Random(1).gauss(0, 1) for _ in range(1)]
rr = random.Random(2)
data = [rr.gauss(0.001, 0.02) for _ in range(5000)]
n_, sx, sxx = len(data), sum(data), sum(x * x for x in data)
mean_ = sx / n_
check("l3 quiz: count, sum and sum of squares give the population variance",
      abs((sxx / n_ - mean_ ** 2) - sum((x - mean_) ** 2 for x in data) / n_) < 1e-12)


# l4: amortised cost
def total_copies(n, factor=2, start=1):
    cap, size, copies, worst = start, 0, 0, 0
    for _ in range(n):
        if size == cap:
            cap *= factor
            copies += size
            worst = max(worst, size)
        size += 1
    return copies, worst


def copies_fixed(n, step):
    cap, size, copies = step, 0, 0
    for _ in range(n):
        if size == cap:
            cap += step
            copies += size
        size += 1
    return copies


check("l4 doubling totals 0,1,3,7,15 at n=1,2,4,8,16; 7 at 5; 31 at 17; 127 at 100; 1023 at 1000; 2047 at 1025",
      [total_copies(n)[0] for n in (1, 2, 4, 8, 16, 5, 17, 100, 1000, 1025)] == [0, 1, 3, 7, 15, 7, 31, 127, 1023, 2047])
check("l4 doubling total < 2n for every n up to 5000 (amortised O(1))",
      all(total_copies(n)[0] < 2 * n for n in range(1, 5000)))
check("l4 tripling total < 1.5n for every n up to 5000", all(total_copies(n, 3)[0] < 1.5 * n for n in range(1, 5000)))
check("hw1 any integer factor r: total < r/(r-1) n", all(total_copies(n, r)[0] < r / (r - 1) * n
                                                      for r in (2, 3, 4, 5, 10) for n in range(1, 3000)))
worse = [n for n in range(1, 300) if total_copies(n, 3)[0] > total_copies(n, 2)[0]]
check("l4 s5 option 'worse' (fixed): 'not in general', and the bounds 1.5n against 2n hold",
      worse and all(total_copies(n, 3)[0] < 1.5 * n and total_copies(n)[0] < 2 * n for n in range(1, 3000))
      and "copies less in total" not in T("l4-cheap-on-average.json", "screens.5.widget.options.3.why")
      and "under $1.5n$, against $2n$" in T("l4-cheap-on-average.json", "screens.5.widget.options.3.why"),
      f"tripling copies more at n = {worse[:8]}... (4 against 3 at n=4, 40 against 31 at n=28)", finding=7)
check("l4 worst append in 100 copies 64; in 1000 copies 512; average 1.023", total_copies(100)[1] == 64
      and total_copies(1000)[1] == 512 and total_copies(1000)[0] / 1000 == 1.023)
check("l4 grow by 10: 49,500 copies for 1000; grow by 100: 4,500", copies_fixed(1000, 10) == 49500
      and copies_fixed(1000, 100) == 4500 and copies_fixed(5, 1) == 10 and copies_fixed(11, 10) == 10)
check("l4 fixed growth is about n^2/(2 step)", abs(copies_fixed(100000, 10) / (100000 ** 2 / 20) - 1) < 0.001)
check("l4 pop(0) drain of 1000 shifts 499,500", sum(range(1000)) == 499500)
check("l4 order book: 2,097,151 copies for 2,000,000 ticks, 1.05 a tick",
      total_copies(2_000_000)[0] == 2097151 and abs(2097151 / 2e6 - 1.05) < 0.005)
check("review-1: 65 appends 127 copies; hw1 start 4: 124 for 100", total_copies(65)[0] == 127
      and total_copies(100, 2, 4)[0] == 124)
dbl_1e6 = total_copies(10 ** 6)[0]
check("hw1 h-fixed-code (fixed): a million appends with doubling make 'about 10^6' copies", abs(dbl_1e6 / 1e6 - 1) < 0.06
      and "about $10^6$ with doubling" in T("homework-1.json", "items.6.explain.text"),
      f"the total is {dbl_1e6:,}, about 1 x 10^6; 2 x 10^6 is the bound 2n", finding=3)
check("hw1 h-fixed-code: step 10 makes 49,999,500,000", 10 * (99999 * 100000 // 2) == 49999500000)
# CPython list growth factor
sizes, lst, last = [], [], sys.getsizeof([])
for i in range(200000):
    lst.append(i)
    s = sys.getsizeof(lst)
    if s != last:
        sizes.append(s)
        last = s
growth = sizes[-1] / sizes[-2]
check("l4 s0 (fixed): list.append grows by a factor 'of about 1.125'", abs(growth - 1.125) < 0.01
      and "about 1.125" in T("l4-cheap-on-average.json", "screens.0.explain.text"),
      f"measured capacity ratio {growth:.3f}; CPython over-allocates by about one eighth", finding=8)
check("l4 quiz np.append (fixed): feedback and whys say 0+1+...+(n-1) = n(n-1)/2, as the explain does",
      all(sum(range(n)) == n * (n - 1) // 2 for n in (5, 50))
      and all("0 + 1 + \\dots + (n - 1)" in T("l4-cheap-on-average.json", p) for p in ("quiz.0.feedback.correct", "quiz.0.widget.options.3.why"))
      and "$0, 1, 2, \\dots$" in T("l4-cheap-on-average.json", "quiz.0.widget.options.2.why"),
      "call k copies k-1 old elements: 0+1+...+(n-1) = n(n-1)/2; the feedback's sum is n larger", finding=9)
check("hw1 longform: 8,997,000 calls, 2.25e9 day-steps, 4,498,500 after halving",
      3000 * 2999 == 8997000 and abs(8997000 * 250 / 2.25e9 - 1) < 0.01 and 3000 * 2999 // 2 == 4498500)
if sys.maxsize > 2 ** 32:
    check("hw1 longform: a 3-tuple is 64 bytes (64-bit)", sys.getsizeof((1.0, "a", "b")) == 64)


# ---------------------------------------------------------------- Level 2
def fib_naive(n, counter, d=1):
    counter[0] += 1
    counter[1] = max(counter[1], d)
    if n < 2:
        return n
    return fib_naive(n - 1, counter, d + 1) + fib_naive(n - 2, counter, d + 1)


def fib_calls(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, 1 + a + b
    return a if n == 0 else b


@lru_cache(None)
def F(n):
    return n if n < 2 else F(n - 1) + F(n - 2)


ok = True
for n in range(0, 22):
    c = [0, 0]
    fib_naive(n, c)
    ok &= c[0] == fib_calls(n) == 2 * F(n + 1) - 1 and c[1] == max(n, 1)
check("l6/l8 naive fib: calls C(n) = 2F(n+1)-1 (15 at 5, 177 at 10), stack depth n", ok and fib_calls(5) == 15
      and fib_calls(10) == 177 and fib_calls(7) == 41 and fib_calls(6) == 25)
check("l8 fib_calls(80) = 75778124746287811; fib(90), fib(300) as in the tests",
      fib_calls(80) == 75778124746287811 and F(90) == 2880067194370816120
      and F(300) == 222232244629420445529739893461909967206666939096499764990979600 and 2 * F(31) - 1 == 2692537)
check("l8 naive fib calls <= 2^n - 1 and grow by about 1.618 a step",
      all(fib_calls(n) <= 2 ** n - 1 for n in range(1, 60)) and abs(fib_calls(60) / fib_calls(59) - 1.618) < 0.001)


def fib_levels(n):
    level, out = [n], []
    while level:
        out.append(len(level))
        level = [m for k in level if k >= 2 for m in (k - 1, k - 2)]
    return out


lv5 = fib_levels(5)
check("l8 s6 explain (fixed): fib's calls double on each level of the top half of its n levels",
      all(len(fib_levels(n)) == n and all(fib_levels(n)[k] == 2 ** k for k in range(n // 2 + 1)) for n in range(2, 18))
      and "doubling on each level of the top half" in T("l8-cost-of-recursion.json", "screens.6.explain.text"),
      f"levels of fib(5) hold {lv5}; only the top half of the levels are full", finding=10)
check("l8 fix text: fib(n) tree is n levels deep and levels 0..n//2 are full",
      all(len(fib_levels(n)) == n and all(fib_levels(n)[k] == 2 ** k for k in range(n // 2 + 1)) for n in range(2, 18)))

memo_calls = [0]
memo = {0: 0, 1: 1}


def fib_memo(n):
    memo_calls[0] += 1
    if n not in memo:
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]


check("l8 quiz: memoised fib(30) makes 59 calls", fib_memo(30) == 832040 and memo_calls[0] == 59)


@lru_cache(None)
def T_merge(n):
    return 1 if n == 1 else 2 * T_merge(n // 2) + n


@lru_cache(None)
def T_exp(n):
    return 1 if n == 1 else 2 * T_exp(n - 1) + 1


@lru_cache(None)
def T_half(n):
    return 1 if n == 1 else T_half(n // 2) + 1


@lru_cache(None)
def T_max(n):
    return 1 if n == 1 else 2 * T_max(n // 2) + 1


@lru_cache(None)
def T_sq(n):
    return 1 if n == 1 else 2 * T_sq(n // 2) + n * n


pw = [2 ** k for k in range(0, 21)]
check("l8 T(n)=2T(n/2)+n, T(1)=1 is n(log2 n + 1): 4, 12, 32, 80",
      all(T_merge(n) == n * (int(math.log2(n)) + 1) for n in pw) and [T_merge(n) for n in (2, 4, 8, 16)] == [4, 12, 32, 80])
check("l8 T(n)=T(n/2)+1 is log2 n + 1: 21 at 2^20", all(T_half(n) == int(math.log2(n)) + 1 for n in pw) and T_half(2 ** 20) == 21)
check("l8 T(n)=2T(n-1)+1 is 2^n - 1: 1023 at 10, 7 at 3", all(T_exp(n) == 2 ** n - 1 for n in range(1, 200)) and T_exp(10) == 1023)
check("l8 T(n)=2T(n/2)+1 is 2n-1", all(T_max(n) == 2 * n - 1 for n in pw))
check("l8 s8 / review-2 feedback (fixed): '1 + 2 + 4 + ... + n = 2n - 1'",
      all(sum(2 ** k for k in range(int(math.log2(n)) + 1)) == 2 * n - 1 for n in (1, 2, 8, 1024))
      and "1 + 2 + 4 + \\cdots + n = 2n - 1" in T("l8-cost-of-recursion.json", "screens.8.feedback.correct")
      and "1 + 2 + 4 + \\cdots + n = 2n - 1" in T("review-2.json", "items.8.feedback.correct"),
      "1+2+...+8 is 36; the sum meant is 1+2+4+8 = 15", finding=11)
check("hw2 T(n)=2T(n/2)+n^2 stays below 2n^2", all(T_sq(n) < 2 * n * n + 1 for n in pw))
check("l8 lattice: 15 against 10 nodes at 3 steps; 5,151 at 100; 2^101 - 1 about 2.5e30",
      2 ** 4 - 1 == 15 and 4 * 5 // 2 == 10 and 101 * 102 // 2 == 5151 and abs((2 ** 101 - 1) / 2.5e30 - 1) < 0.02)


# l5-l7 small traces
def sum_last(xs):
    return 0 if not xs else xs[-1] + sum_last(xs[1:])


def sum_skip(xs):
    return 0 if not xs else xs[0] + sum_skip(xs[2:])


def depth(n, d=1):
    return d if n < 2 else max(depth(n - 1, d + 1), depth(n - 2, d + 1))


check("l5 wrong recursive cases give 9 and 7", sum_last([4, 1, 3]) == 9 and sum_skip([4, 1, 3]) == 7)
check("l5 quiz: grow(3) 1157.625; bond value 97.2768; -1 // 2 == -1",
      abs(1000 * 1.05 ** 3 - 1157.625) < 1e-9 and abs(((104 / 1.05 + 4) / 1.05 + 4) / 1.05 - 97.2768) < 5e-5 and -1 // 2 == -1)
check("l5 folders total 395.75", 120.5 - 40 + 15.25 + 300 == 395.75)
check("l6 depth(5)=5, depth(15)=15, depth(3,10)=12, depth(0)=depth(1)=1",
      (depth(5), depth(15), depth(3, 10), depth(0), depth(1), depth(2)) == (5, 15, 12, 1, 1, 2))


def outer_closure():
    n = 3

    def inner(m):
        return n          # sees the enclosing function's n, not only its own names and the module's
    return inner(2)


check("l6 quiz q-scope why (fixed): a function sees its own names, then the enclosing code's, never its caller's",
      outer_closure() == 3 and "never sees its caller's" in T("l6-call-stack.json", "quiz.3.widget.options.1.why")
      and "only its own names" not in T("l6-call-stack.json", "quiz.3.widget.options.1.why"),
      "a nested function also reads the names of the function it is defined in (and built-ins)", finding=13)

tree = {"v": "r", "c": [{"v": "a", "c": [{"v": "a1", "c": []}, {"v": "a2", "c": []}]}, {"v": "b", "c": []}]}


def rec_order(node, out):
    out.append(node["v"])
    for ch in node["c"]:
        rec_order(ch, out)
    return out


def stack_order(node):
    out, stack = [], [node]
    while stack:
        item = stack.pop()
        out.append(item["v"])
        stack.extend(item["c"])
    return out


check("l6 s7 explain (fixed): the loop goes depth first but takes children last to first",
      stack_order(tree) == ["r", "b", "a", "a2", "a1"] and rec_order(tree, []) == ["r", "a", "a1", "a2", "b"]
      and "children last to first" in T("l6-call-stack.json", "screens.7.explain.text"),
      f"recursion {rec_order(tree, [])}, loop {stack_order(tree)}: depth first both, children reversed", finding=12)


def max_rec_calls(lo, hi, c, d=1):
    c[0] += 1
    c[2] = max(c[2], d)
    if lo == hi:
        return
    mid = (lo + hi) // 2
    max_rec_calls(lo, mid, c, d + 1)
    max_rec_calls(mid + 1, hi, c, d + 1)
    c[1] += 1


ok = True
for n in (1, 2, 3, 8, 16, 1000):
    c = [0, 0, 0]
    max_rec_calls(0, n - 1, c)
    ok &= c[0] == 2 * n - 1 and c[1] == n - 1
c = [0, 0, 0]
max_rec_calls(0, 999, c)
check("l7 max_rec: 2n-1 calls (15 for 8, 31 for 16), n-1 comparisons; 11 frames on 1000", ok and c[2] == 11 and c[0] == 1999)


def power_fast(x, n):
    if n == 0:
        return 1, 0
    if n == 1:
        return x, 0
    h, m = power_fast(x, n // 2)
    if n % 2 == 0:
        return h * h, m + 1
    return h * h * x, m + 2


def pf_calls(n):
    return 1 if n <= 1 else 1 + pf_calls(n // 2)


check("l7 power_fast counts: 4 (n=10), 3 (5), 41 (1e9), 14 (1000), 12 (252), 16 (2520), 8 (100)",
      [power_fast(1, n)[1] for n in (10, 5, 10 ** 9, 1000, 252, 2520, 100)] == [4, 3, 41, 14, 12, 16, 8]
      and power_fast(2, 10)[0] == 1024 and power_fast(3, 5)[0] == 243)
check("l7 power_fast levels: 30 for 1e9, 8 calls for 252, 6 frames for 50, 7 calls for 100",
      (pf_calls(10 ** 9), pf_calls(252), pf_calls(50), pf_calls(100)) == (30, 8, 6, 7))
check("l7 1.0002^252 about 1.0517; 1.05^252 as in the test", abs(1.0002 ** 252 - 1.0517) < 5e-5
      and math.isclose(power_fast(1.05, 252)[0], 218626.7836322, rel_tol=1e-9))


def inversions(xs):
    return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])


check("l7/hw2 inversions: [3,1,4,2] 3; [5,3,8,1,4,7,2,6] 14 = 4 + 3 + 7; [3,1,2,5,4,6] 3; [5,2,4,6,1,3] 9",
      inversions([3, 1, 4, 2]) == 3 and inversions([5, 3, 8, 1, 4, 7, 2, 6]) == 14 and inversions([5, 3, 8, 1]) == 4
      and inversions([4, 7, 2, 6]) == 3 and inversions([3, 1, 2, 5, 4, 6]) == 3 and inversions([5, 2, 4, 6, 1, 3]) == 9)


def rec_merge_comparisons(a, b):
    if not a or not b:
        return 0
    return 1 + (rec_merge_comparisons(a[1:], b) if a[0] <= b[0] else rec_merge_comparisons(a, b[1:]))


worst_merge = max(rec_merge_comparisons(sorted(p[:3]), sorted(p[3:])) for p in itertools.permutations(range(7)))
check("l7 quiz / l12: merging 3 with 4 takes at most 6 comparisons (n - 1)", worst_merge == 6)


def split_feed(feed, listed):
    if feed == "":
        return [[]]
    out = []
    for t in set(listed):
        if feed.startswith(t):
            out += [[t] + r for r in split_feed(feed[len(t):], listed)]
    return out


check("hw2 split_feed: 927 and 4,374 splits; at most 2^(n-1)",
      len(split_feed("A" * 12, ["A", "AA", "AAA"])) == 927
      and len(split_feed("BA" * 8, ["BA", "BAB", "AB", "A", "B"])) == 4374 and 927 <= 2 ** 11 and 4374 <= 2 ** 15)
check("hw2 pricer: 2^21 - 1 = 2,097,151 calls at n=20; 231 nodes; 2^253 about 1.4e76; 2,001,000 updates",
      2 ** 21 - 1 == 2097151 and 21 * 22 // 2 == 231 and abs(2 ** 253 / 1.4e76 - 1) < 0.05 and 2000 * 2001 // 2 == 2001000)


def price_rec(S, step, n, u, d, p, disc, K):
    if step == n:
        return max(S - K, 0)
    return disc * (p * price_rec(S * u, step + 1, n, u, d, p, disc, K) + (1 - p) * price_rec(S * d, step + 1, n, u, d, p, disc, K))


def price_loop(S, n, u, d, p, disc, K):
    v = [max(S * u ** j * d ** (n - j) - K, 0) for j in range(n + 1)]
    for step in range(n - 1, -1, -1):
        v = [disc * (p * v[j + 1] + (1 - p) * v[j]) for j in range(step + 1)]
    return v[0]


check("hw2 pricer: the model loop equals the recursive pricer",
      math.isclose(price_rec(100, 0, 12, 1.1, 0.9, 0.55, 0.99, 100), price_loop(100, 12, 1.1, 0.9, 0.55, 0.99, 100), rel_tol=1e-12))


# ---------------------------------------------------------------- Level 3
def bs_looks(n, target_index):
    """Looks of the l9 three-way binary search on range(n); target_index may be absent (x.5)."""
    lo, hi, looks = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        looks += 1
        if mid == target_index:
            return looks
        if mid < target_index:
            lo = mid + 1
        else:
            hi = mid - 1
    return looks


def worst_looks(n):
    return max(bs_looks(n, t / 2) for t in range(-1, 2 * n))


check("l9 worst-case looks floor(log2 n)+1: 1, 5, 10 for n = 1, 16, 1000; 13 for 5000",
      all(worst_looks(n) == int(math.log2(n)) + 1 for n in list(range(1, 300)) + [1000, 5000])
      and (worst_looks(1), worst_looks(16), worst_looks(1000), worst_looks(5000)) == (1, 5, 10, 13))
check("l9 a million needs 20: floor(log2 1e6) = 19", int(math.log2(10 ** 6)) + 1 == 20 and int(math.log2(2 * 10 ** 6)) + 1 == 21)


def first_at_least(xs, target, cond="<", passes=None):
    lo, hi, k = 0, len(xs), 0
    while lo < hi:
        mid = (lo + hi) // 2
        k += 1
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    if passes is not None:
        passes.append(k)
    return lo


rr = random.Random(7)
okb, worstp = True, {}
for n in range(0, 70):
    xs = sorted(rr.randrange(40) for _ in range(n))
    for t in range(-1, 42):
        ps = []
        okb &= first_at_least(xs, t, passes=ps) == bisect.bisect_left(xs, t)
        worstp[n] = max(worstp.get(n, 0), ps[0])
check("l9 first_at_least is bisect_left; at most ceil(log2(n+1)) passes",
      okb and all(worstp[n] <= math.ceil(math.log2(n + 1)) for n in worstp))
s8 = [96, 98, 99, 100, 100, 100, 101, 103]
check("l9 bisect_left 3, bisect_right 6; [1,3,3,3,8] gives 1 and 4; count_between 5",
      bisect.bisect_left(s8, 100) == 3 and bisect.bisect_right(s8, 100) == 6 and bisect.bisect_left([1, 3, 3, 3, 8], 3) == 1
      and bisect.bisect_right([1, 3, 3, 3, 8], 3) == 4 and bisect.bisect_right(s8, 101) - bisect.bisect_left(s8, 99) == 5)


def le_variant(xs, target, cap=200):
    """while lo <= hi with hi = mid (l9 s7 option 'le'), hi starting at len(xs)."""
    lo, hi, k = 0, len(xs), 0
    while lo <= hi:
        k += 1
        if k > cap:
            return "spins"
        mid = (lo + hi) // 2
        try:
            v = xs[mid]
        except IndexError:
            return "IndexError"
        if v < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


outcomes = {le_variant([10, 20, 30, 40], t) for t in (5, 25, 35, 45)}
check("l9 s7 option 'le' (fixed): with <= it spins when xs[mid] >= target, IndexError past the end",
      outcomes == {"spins", "IndexError"} and le_variant([10, 20, 30, 40], 45) == "IndexError"
      and "raises `IndexError`" in T("l9-halving.json", "screens.7.widget.options.1.why"),
      f"outcomes over four targets: {sorted(map(str, outcomes))}; it spins only when xs[mid] >= target", finding=14)


def unsorted_search(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


check("l9 quiz: binary_search([8,3,12,5,20], 5) is -1", unsorted_search([8, 3, 12, 5, 20], 5) == -1)
check("l9 ten years of days: 12 looks", math.ceil(math.log2(2520 + 1)) == 12)


def smallest_true(lo, hi, pred, calls=None):
    a, b = lo, hi + 1
    while a < b:
        mid = (a + b) // 2
        if calls is not None:
            calls.append(mid)
        if pred(mid):
            b = mid
        else:
            a = mid + 1
    return a if a <= hi else None


calls, lo_i, hi_i = [], 0, 64                 # the l10 s1 stepping: lo..hi with hi = mid, no "none" marker
while lo_i < hi_i:
    mid_i = (lo_i + hi_i) // 2
    calls.append(mid_i)
    if 0.15 * math.sqrt(mid_i) >= 1:
        hi_i = mid_i
    else:
        lo_i = mid_i + 1
check("l10 impact search: 45 thousand in six tries (32, 48, 40, 44, 46, 45)", lo_i == 45 and calls == [32, 48, 40, 44, 46, 45]
      and abs((1 / 0.15) ** 2 - 44.44) < 0.005 and smallest_true(0, 64, lambda q: 0.15 * math.sqrt(q) >= 1) == 45)
calls = []
smallest_true(0, 10 ** 12, lambda x: x >= 123456789, calls)
check("l10 about 40 calls for 1e12, 30 for 1e9, never outside the range",
      len(calls) <= math.ceil(math.log2(10 ** 12 + 2)) == 40 and math.ceil(math.log2(10 ** 9)) == 30)
check("l10 isqrt by smallest_true matches math.isqrt; 1e18 in about 60 steps",
      all(smallest_true(0, n + 1, lambda x: x * x > n) - 1 == math.isqrt(n) for n in list(range(3000)) + [10 ** 18, 10 ** 18 - 1])
      and math.ceil(math.log2(10 ** 18 + 3)) == 60)
check("l10 isqrt needs n+1 only for n = 0 and 1", [n for n in range(50) if smallest_true(0, n, lambda x: x * x > n) is None] == [0, 1])
closes = [97, 99, 102, 98, 96, 101, 103, 105]
check("l10 trap: non-monotone test returns 5; the prefix-max test returns 2",
      smallest_true(0, 7, lambda d: closes[d] > 100) == 5 and smallest_true(0, 7, lambda d: max(closes[:d + 1]) > 100) == 2)
check("l10 quiz: savings 26 days; 20 halvings for 1e-6; hw3 27 for 1e-8; review-3 doubling in 15 years",
      smallest_true(1, 100, lambda d: 120 + 35 * d >= 1000) == 26 and 2 ** 19 < 10 ** 6 < 2 ** 20 and 2 ** 26 < 10 ** 8 < 2 ** 27
      and smallest_true(1, 100, lambda n: 1.05 ** n >= 2) == 15)


def bond_price(y, coupon, years, face):
    return sum(coupon / (1 + y) ** t for t in range(1, years + 1)) + face / (1 + y) ** years


def yield_for_price(price, coupon, years, face, steps=None):
    lo, hi = 0.0, 1.0
    if price > bond_price(lo, coupon, years, face) or price < bond_price(hi, coupon, years, face):
        return None
    k = 0
    while True:
        mid = (lo + hi) / 2
        k += 1
        p = bond_price(mid, coupon, years, face)
        if abs(p - price) <= 0.01:
            if steps is not None:
                steps.append(k)
            return mid
        if p > price:
            lo = mid
        else:
            hi = mid


st = []
y95 = yield_for_price(95.0, 4, 5, 100, st)
check("l10 bond: 95.67 at 5%, 91.58 at 6%, 120 at 0%; yield for 95.00 about 5.16% in 15 halvings",
      abs(bond_price(0.05, 4, 5, 100) - 95.67) < 0.005 and abs(bond_price(0.06, 4, 5, 100) - 91.58) < 0.005
      and bond_price(0, 4, 5, 100) == 120 and abs(y95 - 0.0516) < 0.0001 and st[0] == 15, f"y={y95:.5f} steps={st}")
check("l10 bond tests: 0.05, 0.043, 0.016, None, None",
      round(yield_for_price(100.0, 5, 5, 100), 3) == 0.05 and round(yield_for_price(92.5, 3, 7, 100), 3) == 0.043
      and round(yield_for_price(850.0, 0, 10, 1000), 3) == 0.016 and yield_for_price(130.0, 4, 5, 100) is None
      and yield_for_price(5.0, 4, 5, 100) is None)


def bs_call(S, K, r, T, sig):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return S * N(d1) - K * math.exp(-r * T) * N(d2)


lo_, hi_ = 0.20, 0.30
for _ in range(20):
    m_ = (lo_ + hi_) / 2
    if bs_call(100, 100, 0.05, 1, m_) > 12:
        hi_ = m_
    else:
        lo_ = m_
check("l10 Black-Scholes: c(0.20)=10.45, c(0.25)=12.34, c(0.30)=14.23; implied vol for 12.00 about 0.2411",
      abs(bs_call(100, 100, 0.05, 1, 0.20) - 10.45) < 0.005 and abs(bs_call(100, 100, 0.05, 1, 0.25) - 12.34) < 0.005
      and abs(bs_call(100, 100, 0.05, 1, 0.30) - 14.23) < 0.005 and abs((lo_ + hi_) / 2 - 0.2411) < 0.00005, f"{(lo_ + hi_) / 2:.5f}")
check("l10 load test: next rate 3,250; 11 more tests pin it to one order a minute",
      (2500 + 4000) // 2 == 3250 and 1500 / 2 ** 10 > 1 >= 1500 / 2 ** 11)
check("l10 s9 explain (fixed): testing every rate from 1,000 up 'would take more than 1,500'", (2500 - 1000 + 1) > 1500
      and "more than 1,500" in T("l10-search-the-answer.json", "screens.9.explain.text"),
      "the limit is at least 2,500, so a scan from 1,000 runs at least 1,501 tests", finding=15)


# sorting
def insertion_sort(xs):
    a, comps = list(xs), 0
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps


check("l11 insertion sort comparisons: 12, 4, 10, 5, 9, 3, 7",
      [insertion_sort(x)[1] for x in ([5, 2, 4, 6, 1, 3], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [3, 1, 3, 1],
                                      [1, 2, 4, 3, 5, 6, 8, 7], [3, 1, 2], [4, 3, 2, 1, 5])] == [12, 4, 10, 5, 9, 3, 7])
check("l11 worst case n(n-1)/2 (499,500 at 1000, 780 at 40), best n-1; nothing beats reversed",
      insertion_sort(range(1000, 0, -1))[1] == 499500 and insertion_sort(range(1000))[1] == 999
      and max(insertion_sort(p)[1] for p in itertools.permutations(range(7))) == 21 and 40 * 39 // 2 == 780)
avg7 = sum(insertion_sort(p)[1] for p in itertools.permutations(range(7))) / math.factorial(7)
check("l11 random input: each key walks about halfway, still quadratic", 7 * 6 / 4 <= avg7 <= 7 * 6 / 2, f"mean {avg7:.2f} for n=7")


def stable_insertion(pairs, strict=True):
    a = list(pairs)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and (a[j][0] > key[0] if strict else a[j][0] >= key[0]):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


check("l11 insertion sort with > is stable, with >= is not",
      stable_insertion([(101, "A"), (100, "x"), (101, "B")]) == [(100, "x"), (101, "A"), (101, "B")]
      and stable_insertion([(101, "A"), (100, "x"), (101, "B")], strict=False) == [(100, "x"), (101, "B"), (101, "A")])
check("l11 order book insertion: 4 comparisons",
      insertion_sort([99.96, 99.97, 99.98, 99.99, 100.01, 99.975])[1] - insertion_sort([99.96, 99.97, 99.98, 99.99, 100.01])[1] == 4)


def merge(a, b, strict=False, counter=None):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if counter is not None:
            counter[0] += 1
        take_left = a[i][0] < b[j][0] if strict else a[i][0] <= b[j][0]
        if take_left:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


def merge_sort(xs, strict=False, counter=None):
    if len(xs) <= 1:
        return list(xs)
    mid = len(xs) // 2
    return merge(merge_sort(xs[:mid], strict, counter), merge_sort(xs[mid:], strict, counter), strict, counter)


trades = [(101, "A"), (100, "B"), (101, "C")]
check("l12 merge sort with <= is stable (B, A, C); with < it is not",
      [t[1] for t in merge_sort(trades)] == ["B", "A", "C"] and [t[1] for t in merge_sort(trades, strict=True)] == ["B", "C", "A"])
cnt = [0]
merge([(v,) for v in (2, 5, 9, 12)], [(v,) for v in (3, 4, 10, 15)], counter=cnt)
worst_m = 0
for n in (8, 64, 1024):
    rr = random.Random(n)
    for _ in range(50):
        c = [0]
        merge_sort([(rr.random(),) for _ in range(n)], counter=c)
        worst_m = max(worst_m, c[0] / (n * math.log2(n)))
check("l12 merge of 4 and 4 takes 7 comparisons; merge sort stays at or under n log2 n comparisons",
      cnt[0] == 7 and worst_m <= 1.0 and 40 + 25 - 1 == 64, f"worst ratio {worst_m:.3f}")
check("l12 numbers: 3 levels x 8 = 24 against 28; 1e6: about 20 levels against 5e11; 20,000 reversed about 2e8",
      8 * 7 // 2 == 28 and abs(math.log2(10 ** 6) - 20) < 0.1 and abs(10 ** 6 * (10 ** 6 - 1) / 2 / 5e11 - 1) < 0.01
      and abs(20000 * 19999 / 2 / 2e8 - 1) < 0.01 and abs(2 * math.log2(2e6) / math.log2(1e6) - 2.1) < 0.01)


def count_inversions_merge(xs):
    def sc(a):
        if len(a) <= 1:
            return list(a), 0, 0
        mid = len(a) // 2
        left, x, cx = sc(a[:mid])
        right, y, cy = sc(a[mid:])
        out, i, j, c, comps = [], 0, 0, x + y, cx + cy
        while i < len(left) and j < len(right):
            comps += 1
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
                c += len(left) - i
        return out + left[i:] + right[j:], c, comps
    _, c, comps = sc(xs)
    return c, comps


big = [(i * 7919) % 20011 for i in range(20000)]
sl, inv_big = [], 0
for v in big:                                   # independent count with a sorted list
    inv_big += len(sl) - bisect.bisect_right(sl, v)
    bisect.insort(sl, v)
check("l12/hw2 inversions of the 20,000-value test list are 99,930,366; [2,2,1] has 2; reversed 3000 has 4,498,500",
      inv_big == 99930366 == count_inversions_merge(big)[0] and count_inversions_merge([2, 2, 1])[0] == 2
      and count_inversions_merge(list(range(3000, 0, -1)))[0] == 4498500)
check("l12 Kendall tau for 3 discordant of 15 is 0.6", abs((12 - 3) / 15 - (1 - 2 * 3 / 15)) < 1e-12 and 1 - 2 * 3 / 15 == 0.6)
rev = list(range(64, 0, -1))
inv_rev, comps_rev = count_inversions_merge(rev)
check("hw2 h-sort-count explain (fixed): one comparison settles a group of pairs, not pair by pair",
      comps_rev < inv_rev and "compares each pair" not in T("homework-2.json", "items.5.explain.text")
      and "every left item still waiting is bigger" in T("homework-2.json", "items.5.explain.text"),
      f"64 reversed values: {inv_rev} inversions counted with {comps_rev} comparisons; the pairs are counted in bulk", finding=16)


def lomuto(xs, lo, hi, counter=None, key=lambda v: v):
    pivot, i = xs[hi], lo
    for j in range(lo, hi):
        if counter is not None:
            counter[0] += 1
        if key(xs[j]) <= key(pivot):
            xs[i], xs[j] = xs[j], xs[i]
            i += 1
    xs[i], xs[hi] = xs[hi], xs[i]
    return i


def quicksort(xs, pivot="last", rng=None, counter=None, key=lambda v: v):
    stack = [(0, len(xs) - 1, 1)]
    deepest = 0
    while stack:
        lo, hi, d = stack.pop()
        if lo >= hi:
            continue
        deepest = max(deepest, d)
        if pivot == "random":
            r = rng.randint(lo, hi)
            xs[r], xs[hi] = xs[hi], xs[r]
        p = lomuto(xs, lo, hi, counter, key)
        stack.append((lo, p - 1, d + 1))
        stack.append((p + 1, hi, d + 1))
    return deepest


x = [7, 2, 9, 4, 1, 8, 5]
p_ = lomuto(x, 0, 6)
y = [9, 3, 7, 1, 8, 2, 6, 5]
py_ = lomuto(y, 2, 5)
z = [3, 8, 2, 5, 1, 4]
pz = lomuto(z, 0, 5)
check("l13 Lomuto traces: (3, [2,4,1,5,9,8,7]); (3, [9,3,1,2,8,7,6,5]); review-3 (3, [3,2,1,4,8,5])",
      (p_, x) == (3, [2, 4, 1, 5, 9, 8, 7]) and (py_, y) == (3, [9, 3, 1, 2, 8, 7, 6, 5]) and (pz, z) == (3, [3, 2, 1, 4, 8, 5]))
c1, c2, c3 = [0], [0], [0]
quicksort([7, 2, 9, 4, 1, 8, 5], counter=c1)
quicksort(list(range(1, 8)), counter=c2)
d1000 = quicksort(list(range(1000)), counter=c3)
check("l13 last-pivot comparisons: 12 on the example, 21 on sorted 7 (the maximum), 499,500 on sorted 1000, about 1000 deep",
      c1[0] == 12 and c2[0] == 21 and c3[0] == 499500 and d1000 == 999 and 2000 * 1999 // 2 == 1999000
      and max((lambda c: (quicksort(list(p), counter=c), c[0])[1])([0]) for p in itertools.permutations(range(7))) == 21)
rng = random.Random(11)
ratios = []
for _ in range(30):
    c = [0]
    data = list(range(20000))
    rng.shuffle(data)
    quicksort(data, "random", rng, c)
    ratios.append(c[0])
mean_q = sum(ratios) / len(ratios)
H = lambda n: sum(1 / k for k in range(1, n + 1))
exact = 2 * (20000 + 1) * H(20000) - 4 * 20000
check("l13 random-pivot quicksort on distinct values: mean comparisons 2(n+1)H_n - 4n, leading term 1.39 n log2 n",
      abs(mean_q / exact - 1) < 0.02 and abs(2 * math.log(2) - 1.386) < 0.001, f"measured {mean_q:.0f}, formula {exact:.0f}")
c_sorted, c_equal = [0], [0]
quicksort(list(range(3000)), "random", rng, c_sorted)
quicksort([5] * 3000, "random", rng, c_equal)
check("l13 random pivot makes sorted input cheap", c_sorted[0] < 3 * 3000 * math.log2(3000))
check("l13 s4 explain / s7 key (fixed): expected O(n log n) is claimed only for distinct values",
      c_equal[0] == 3000 * 2999 // 2 and c_sorted[0] < 3 * 3000 * math.log2(3000)
      and "distinct values" in T("l13-quicksort.json", "screens.7.question")
      and "distinct values" in T("l13-quicksort.json", "screens.4.explain.text")
      and "every input" not in T("l13-quicksort.json", "screens.7.widget.options.0.text")
      and T("l13-quicksort.json", "screens.7.widget.options.0.id") == "a",
      f"3,000 equal values cost {c_equal[0]:,} comparisons = n(n-1)/2 whatever the pivot draw (Lomuto sends ties left)",
      finding=4)
outs = set()
for seed in range(60):
    t = [(5, "a"), (5, "b"), (1, "c")]
    quicksort(t, "random", random.Random(seed), key=lambda v: v[0])
    outs.add(tuple(v[1] for v in t))
t = [(5, "a"), (5, "b"), (1, "c")]
quicksort(t, key=lambda v: v[0])
check("l13 quiz q-stable: with the last value as pivot the output is c, b, a", [v[1] for v in t] == ["c", "b", "a"])
check("l13 quiz q-stable (fixed): the item names the last-value pivot, under which the output is unique",
      len(outs) == 2 and [v[1] for v in t] == ["c", "b", "a"]
      and "taking the last value as pivot" in T("l13-quicksort.json", "quiz.2.prose"),
      f"the lesson's own random-pivot quicksort gives {sorted(outs)}", finding=5)


def quickselect_comparisons(xs, k, rng):
    lo, hi, c = 0, len(xs) - 1, [0]
    while lo < hi:
        r = rng.randint(lo, hi)
        xs[r], xs[hi] = xs[hi], xs[r]
        p = lomuto(xs, lo, hi, c)
        if k == p:
            return xs[p], c[0]
        if k < p:
            hi = p - 1
        else:
            lo = p + 1
    return xs[lo], c[0]


n_q, tot_med, tot_min, tot_p20 = 20001, 0, 0, 0
REPS = 300
for _ in range(REPS):
    d = list(range(n_q))
    rng.shuffle(d)
    v, c = quickselect_comparisons(d, n_q // 2, rng)
    assert v == n_q // 2
    tot_med += c
    rng.shuffle(d)
    tot_min += quickselect_comparisons(d, 0, rng)[1]
    rng.shuffle(d)
    tot_p20 += quickselect_comparisons(d, n_q // 5, rng)[1]
med_ratio, min_ratio, p20_ratio = tot_med / REPS / n_q, tot_min / REPS / n_q, tot_p20 / REPS / n_q


def quickselect_exact(n):
    """Exact expected comparisons E[m][k] of random-pivot quickselect on m distinct keys, index k."""
    diag, col, arr = {}, {}, [0.0]

    def add(m, a):
        for k in range(m):
            diag[m - k] = diag.get(m - k, 0.0) + a[k]
            col[k] = col.get(k, 0.0) + a[k]
    add(1, arr)
    for m in range(2, n + 1):
        arr = [m - 1 + ((diag.get(m - k, 0.0) if k > 0 else 0.0) + (col.get(k, 0.0) if k < m - 1 else 0.0)) / m
               for k in range(m)]
        add(m, arr)
    return arr


ex = quickselect_exact(1501)
ex_med, ex_min, ex_p20 = ex[750] / 1501, ex[0] / 1501, ex[300] / 1501
check("l13 s9 table: quickselect costs 2n to 4n on average (exact recurrence at n=1501: median about 3.3n, "
      "tending to 2(1 + ln 2)n = 3.39n; minimum about 2n; 20th percentile about 3n)",
      3.2 < ex_med < 3.4 and 1.9 < ex_min < 2.05 and 2.85 < ex_p20 < 3.05 and 2.9 < med_ratio < 3.9 and 1.7 < min_ratio < 2.3,
      f"exact {ex_med:.2f}n / {ex_min:.2f}n / {ex_p20:.2f}n; simulated at n={n_q}: {med_ratio:.2f}n / {min_ratio:.2f}n / {p20_ratio:.2f}n")
check("l13 s8 feedback and explain (fixed): 2n to 4n on average, about 3.4n for a median; hw3 agrees",
      3.2 < ex_med < 3.4 and abs(2 * (1 + math.log(2)) - 3.39) < 0.01 and 1.9 < ex_min < 2.05
      and "$2n$ to $4n$" in T("l13-quicksort.json", "screens.8.feedback.correct")
      and "$3.4n$ for a median" in T("l13-quicksort.json", "screens.8.explain.text")
      and "2 million steps" not in T("l13-quicksort.json", "screens.8.explain.text")
      and "about $2n$ to $4n$" in T("homework-3.json", "items.6.explain.text"), f"exact expectation {ex_med:.2f}n at n=1501, simulated {med_ratio:.2f}n at n={n_q}; "
      "theory 2(1 + ln 2)n = 3.39n", finding=17)
sizes = [(i * 7919) % 10007 for i in range(100001)]
check("l13/hw3 tests: median of the 100,001 sizes is 5003; 20,000th largest is 8005",
      sorted(sizes)[50000] == 5003 and sorted(sizes)[100001 - 20000] == 8005)
check("l13 VaR table: n log2 n about 230 million at 1e7; 2n to 4n is 20 to 40 million",
      abs(1e7 * math.log2(1e7) / 2.3e8 - 1) < 0.02 and abs(500 * 1e7 / (1e7 * math.log2(1e7)) - 21.5) < 0.5
      and math.ceil(math.log2(1e7)) == 24)


# greedy
def greedy_coins(amount, coins):
    k = 0
    for c in sorted(coins, reverse=True):
        k += amount // c
        amount %= c
    return k if amount == 0 else None


def best_coins(limit, coins):
    best = [0] + [None] * limit
    for a in range(1, limit + 1):
        opts = [best[a - c] for c in coins if c <= a and best[a - c] is not None]
        best[a] = 1 + min(opts) if opts else None
    return best


def greedy_fails(coins, limit):
    best = best_coins(limit, coins)
    return [a for a in range(1, limit + 1) if greedy_coins(a, coins) != best[a]]


UK = [1, 2, 5, 10, 20, 50, 100, 200]
check("l14 greedy is optimal for UK coins (checked to 1,000, past the Kozen-Zaks bound 300), 87p needs 5",
      greedy_fails(UK, 1000) == [] and greedy_fails(UK[:6], 1000) == [] and greedy_coins(87, UK[:6]) == 5)
check("l14 coins 1,3,4: greedy uses 1,2,1,1,2,3,2,2,3,4 and fails exactly at 6 and 10 among 1..10",
      [greedy_coins(a, [1, 3, 4]) for a in range(1, 11)] == [1, 2, 1, 1, 2, 3, 2, 2, 3, 4]
      and [a for a in greedy_fails([1, 3, 4], 10)] == [6, 10])
check("l14/hw3 coin systems: 1,10,25 fails at 30 (6 against 3); 1,5,12 fails at 15 (4 against 3); "
      "1,2,5,10 / 1,3,9,27 / 1,5,10,25 never fail",
      greedy_coins(30, [1, 10, 25]) == 6 and best_coins(30, [1, 10, 25])[30] == 3 and greedy_coins(15, [1, 5, 12]) == 4
      and best_coins(15, [1, 5, 12])[15] == 3 and all(greedy_fails(c, 2000) == [] for c in ([1, 2, 5, 10], [1, 3, 9, 27], [1, 5, 10, 25])))


def eft(intervals, key=lambda iv: iv[1]):
    count, end = 0, float("-inf")
    for s, e in sorted(intervals, key=key):
        if s >= end:
            count += 1
            end = e
    return count


def brute_max(intervals):
    best = 0
    for mask in range(1 << len(intervals)):
        chosen = sorted(iv for k, iv in enumerate(intervals) if mask >> k & 1)
        if all(a[1] <= b[0] for a, b in zip(chosen, chosen[1:])):
            best = max(best, len(chosen))
    return best


diary = [(9, 15), (9.5, 10.5), (10.5, 11.5), (11, 12.5), (12, 13), (13.5, 14.5), (14, 16)]
rr = random.Random(5)
ok_eft, start_fails, short_fails = True, 0, 0
for _ in range(400):
    ivs = []
    for _ in range(rr.randint(0, 9)):
        s = rr.randint(0, 20)
        ivs.append((s, s + rr.randint(1, 8)))
    b = brute_max(ivs)
    ok_eft &= eft(ivs) == b
    start_fails += eft(ivs, key=lambda iv: iv[0]) != b
    short_fails += eft(ivs, key=lambda iv: iv[1] - iv[0]) != b
check("l14 earliest finish first equals the brute-force optimum on 400 random diaries; the diary gives 4",
      ok_eft and eft(diary) == 4 == brute_max(diary))
check("l14 sorting by start gives 1 on the diary; by start or by length fails on some diaries",
      eft(diary, key=lambda iv: iv[0]) == 1 and start_fails > 0 and short_fails > 0
      and eft([(1, 5), (4, 7), (6, 10)], key=lambda iv: iv[1] - iv[0]) == 1 and eft([(1, 5), (4, 7), (6, 10)]) == 2)
O_touch = [(9, 10), (10, 11)]
check("l14 s7 derive line s3 (fixed): every other meeting of O 'starts when o ends or later'",
      all(iv[0] >= O_touch[0][1] for iv in O_touch[1:]) and not all(iv[0] > O_touch[0][1] for iv in O_touch[1:])
      and "starts when $o$ ends or later" in T("l14-best-step-now.json", "screens.7.widget.lines.2.text"),
      "touching meetings are allowed, so the next one can start exactly when o ends: 'at or after'", finding=18)
trades_k = [(6000, 300), (5000, 200), (5000, 200)]
best01 = max(sum(p for k, (c, p) in enumerate(trades_k) if m >> k & 1) for m in range(8)
             if sum(c for k, (c, p) in enumerate(trades_k) if m >> k & 1) <= 10000)
check("l14 knapsack: 0/1 optimum 400, greedy 300, fractional 460; quiz fractional 38",
      best01 == 400 and 300 + 4000 * 200 / 5000 == 460 and 20 + 18 == 38)
check("l14 market order: 100,031 for 1,000 shares", abs(300 * 100.02 + 500 * 100.03 + 200 * 100.05 - 100031) < 1e-6)
sp = lambda s1, s2, rho: (s1 + s2) / math.sqrt(2 + 2 * rho)
rr = random.Random(9)
N = 200000
za = [rr.gauss(0, 1) for _ in range(N)]
ze = [rr.gauss(0, 1) for _ in range(N)]
ra = [1.5 / 16 + z for z in za]                                  # per-period Sharpe 1.5/16, unit vol
rb = [1.4 / 16 + 0.95 * z + math.sqrt(1 - 0.95 ** 2) * e for z, e in zip(za, ze)]
port = [(a + b) / 2 for a, b in zip(ra, rb)]
m = sum(port) / N
sd = math.sqrt(sum((v - m) ** 2 for v in port) / N)
check("l14 pair Sharpe: 1.47 for A and B, 1.77 for A and C, 1.70 for B and C; formula agrees with a simulation",
      abs(sp(1.5, 1.4, 0.95) - 1.47) < 0.005 and abs(sp(1.5, 1.0, 0) - 1.77) < 0.005 and abs(sp(1.4, 1.0, 0) - 1.70) < 0.005
      and abs(16 * m / sd - sp(1.5, 1.4, 0.95)) < 0.12, f"simulated {16 * m / sd:.3f}")


def min_capacity(sizes, days):
    def need(cap):
        d, load = 1, 0
        for s in sizes:
            if load + s > cap:
                d, load = d + 1, 0
            load += s
        return d
    lo, hi = max(sizes), sum(sizes)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


check("hw3 min_capacity: 15, 6, 3, 18, 10, 32, 25534",
      [min_capacity(list(range(1, 11)), 5), min_capacity([3, 2, 2, 4, 1, 4], 3), min_capacity([1, 2, 3, 1, 1], 4),
       min_capacity([7, 2, 5, 10, 8], 2), min_capacity([7, 2, 5, 10, 8], 5), min_capacity([7, 2, 5, 10, 8], 1),
       min_capacity([(i * 37) % 101 + 1 for i in range(50000)], 100)] == [15, 6, 3, 18, 10, 32, 25534])
check("review-3 max_size: 4000 and 2316", max(n for n in range(5000) if 2.5 * n <= 10000) == 4000
      and max(n for n in range(5000) if 2 * n + 0.001 * n * n <= 10000) == 2316)

# ---------------------------------------------------------------- report
fails = [r for r in RESULTS if not r[1]]
for name, ok, detail, finding in RESULTS:
    tag = "ok  " if ok else ("FINDING %-2s" % finding if finding else "FAIL")
    print(f"[{tag}] {name}" + (f"  ({detail})" if detail and (not ok or finding is None) else ""))
unexpected = [r for r in fails if r[3] is None]
print(f"\n{len(RESULTS)} checks: {len(RESULTS) - len(fails)} pass, {len(fails)} fail "
      f"({len(fails) - len(unexpected)} tied to findings, {len(unexpected)} unexpected)")
sys.exit(1 if fails else 0)
