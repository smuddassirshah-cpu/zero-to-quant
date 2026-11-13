#!/usr/bin/env python3
"""algo-think L1 to L3, round 3 blind concept audit: every count, bound and code-behaviour claim recomputed.

Run from the repository root:  python3 docs/reports/algo-think-L1-3-r3-concepts.py
CPython 3.12 or 3.13 (the page runs Pyodide 0.27.7, Python 3.12, wasm32). Exit 0 when every check holds.
A check that fails because the content is wrong stays failing: it is a finding in docs/reviews/audit-algo-think-1-3-r3.md.
Part A recomputes numbers. Part B runs each code widget's solution and starter and, for the feedback.byKey lines, a submission making the mistake the
line names or describes, and checks which key the page would show first (recursion limit 3000, as on the page). Lines that only
describe their test are paired with the natural mistake and the key that mistake really reaches.
Submissions that fail by the page's 5 second limit are marked slow and were run in Pyodide under node (see the ledger); here
they are skipped.
"""
import bisect, itertools, json, math, os, random, subprocess, sys, time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'algo-think')
FAILS, COUNT = [], [0]
def check(name, cond, detail=''):
    COUNT[0] += 1
    if not cond:
        FAILS.append(name + (' :: ' + str(detail) if detail != '' else ''))

# ------------------------------------------------------------------ Part A: numbers
pairs = lambda n: n * (n - 1) // 2
# l1
P8 = [102, 98, 105, 101, 99, 108, 104, 100]
check('l1 scan comparisons 7', len(P8) - 1 == 7)
check('l1 pairs 28/120/496/4950/1999000', [pairs(n) for n in (8, 16, 32, 100, 2000)] == [28, 120, 496, 4950, 1999000])
ben = 1 + 7 + sum(1 for i in range(1, 8) if P8[i] > max(P8[:i])) + 1
check('l1 Ben counts 11', ben == 11, ben)
check('l1 quiz 25 times', abs(pairs(10000) / pairs(2000) - 25) < 0.02 and round(pairs(10000) / 1e7) == 5)
check('l1 transfer 500 million', abs(pairs(2000) * 250 / 5e8 - 1) < 0.01)
# l2
check('l2 2^n ahead from 5', all(2 ** n > n * n for n in range(5, 200)) and 2 ** 4 == 16 and 3 * 3 > 2 ** 3 and 2 ** 2 == 4 and 2 ** 1 > 1)
f = lambda n: 3 * n * n + 50 * n + 7
check('l2 crossing 51', f(50) == 10007 and f(51) == 10360 and 4 * 51 * 51 == 10404 and all(f(n) < 4 * n * n for n in range(51, 5000)) and f(50) > 4 * 2500)
check('l2 50.14', abs((50 + math.sqrt(2500 + 28)) / 2 - 50.14) < 0.005)
check('l2 seventeen', min(n for n in range(1, 100) if 3 * n * n > 50 * n) == 17)
check('l2 doubling row', 2048 * 11 == 22528 and 2048 ** 2 == 4194304 and abs(22528 / 10240 - 2.2) < 1e-9)
check('l2 333334', min(n for n in range(333000, 334000) if 3 * n > 10 ** 6) == 333334)
check('l2 60n^2 bound', all(f(n) <= 60 * n * n for n in range(1, 2000)))
check('l2 log2 n > 20', 2 * 2 ** 21 * 21 > 40 * 2 ** 21 and not 2 * 2 ** 20 * 20 > 40 * 2 ** 20)
check('l2 backtest', 5000 * 500 == 2500000 and 5000 * 500 * 500 == 1250000000)
# l3
if sys.maxsize > 2 ** 32:
    xs = [float(i) for i in range(1_000_000)]
    check('l3 getsizeof list comp 8448728', sys.getsizeof(xs) == 8448728, sys.getsizeof(xs))
    check('l3 float 24 bytes', sys.getsizeof(xs[0]) == 24)
    check('l3 about 32 MB', abs((sys.getsizeof(xs) + 24e6) / 1e6 - 32.4) < 0.1)
    check('hw1 3-tuple 64 bytes', sys.getsizeof((0.5, 'a', 'b')) == 64)
    del xs
check('l3 reverse swaps', 1001 // 2 == 500)
v = 10 * 252 * 390 * 5
check('l3 minute bars', v == 4914000 and 200 * v == 982800000 and abs(200 * v * 8 / 1e9 - 7.86) < 0.005 and abs(200 * v * 32 / 1e9 - 31.45) < 0.005
      and [round(k * v * b / 1e9, 2) for k in (50, 100) for b in (32, 8)] == [7.86, 1.97, 15.72, 3.93])
try:
    gains = (p for p in [120, -40, 330, -15] if p > 0)
    s1 = sum(gains); max(gains); msg = ''
except ValueError as e:
    msg = str(e)
check('l3 generator quiz', s1 == 450 and msg == 'max() iterable argument is empty', msg)
# l4
def copies(n, grow=lambda c: 2 * c, start=1):
    cap, size, tot, worst, events = start, 0, 0, 0, []
    for k in range(1, n + 1):
        if size == cap:
            cap = grow(cap); tot += size; worst = max(worst, size); events.append((k, size))
        size += 1
    return tot, worst, events
check('l4 doubling totals', [copies(n)[0] for n in (1, 2, 3, 4, 5, 8, 9, 16, 17, 100, 1000, 1025, 65, 64)] == [0, 1, 3, 3, 7, 7, 15, 15, 31, 127, 1023, 2047, 127, 63])
check('l4 resize appends', [k for k, _ in copies(1000)[2]] == [2, 3, 5, 9, 17, 33, 65, 129, 257, 513] and copies(100)[1] == 64)
check('l4 below 2n', all(copies(n)[0] < 2 * n for n in range(1, 5000)))
check('l4 tripling below 1.5n', all(copies(n, lambda c: 3 * c)[0] < 1.5 * n for n in range(1, 5000)))
check('l4 fixed 10', copies(1000, lambda c: c + 10, 10)[0] == 49500 and copies(1000, lambda c: c + 10, 10)[2][-1] == (991, 990) and len(copies(1000, lambda c: c + 10, 10)[2]) == 99)
check('l4 fixed 100 and start 4', copies(1000, lambda c: c + 100, 100)[0] == 4500 and copies(100, start=4)[0] == 124)
check('l4 order book', copies(2_000_000)[0] == 2097151 and abs(2097151 / 2e6 - 1.05) < 0.005 and copies(1048576)[0] == 1048575)
check('l4 pop(0) shifts', sum(range(1000)) == 499500)
sizes = sorted({sys.getsizeof([None] * 0)})  # growth factor of list.append
l, caps, last = [], [], None
for i in range(200000):
    l.append(None)
    s = sys.getsizeof(l)
    if s != last: caps.append(s); last = s
ratios = [(b - 56) / (a - 56) for a, b in zip(caps[-12:], caps[-11:])]
check('l4 list growth about 1.125', all(1.11 < r < 1.14 for r in ratios), ratios[:3])
# l5
def grow(n, a=1000, r=1.05): return a if n == 0 else grow(n - 1, a, r) * r
check('l5 grow', abs(grow(3) - 1157.625) < 1e-9 and abs(grow(2) - 1102.5) < 1e-9 and abs(grow(3, 500, 1.02) - 530.604) < 1e-9)
def value(flows, r): return 0 if not flows else (flows[0] + value(flows[1:], r)) / (1 + r)
check('l5 bond 97.28', abs(value([4, 4, 104], 0.05) - 97.2768) < 5e-5 and abs(value([104], 0.05) - 99.0476) < 5e-5)
seq = [1000]
while seq[-1] != 0: seq.append(seq[-1] // 2)
check('l5 f(1000) ten halvings', len(seq) - 1 == 10 and -1 // 2 == -1)
# l6 / l8 fib counts
def fib_tree(n, d=1):
    if n < 2: return 1, d
    a, da = fib_tree(n - 1, d + 1); b, db = fib_tree(n - 2, d + 1)
    return 1 + a + b, max(da, db)
F = [0, 1]
while len(F) < 400: F.append(F[-1] + F[-2])
check('l6 fib(5) 15 calls depth 5', fib_tree(5) == (15, 5) and fib_tree(15)[1] == 15)
check('l8 C(n) = 2F(n+1) - 1', all(fib_tree(n)[0] == 2 * F[n + 1] - 1 for n in range(0, 20)) and 2 * F[31] - 1 == 2692537 and 2 * F[81] - 1 == 75778124746287811 and fib_tree(6)[0] == 25 and fib_tree(7)[0] == 41)
check('l8 fib(90), fib(300)', F[90] == 2880067194370816120 and F[300] == 222232244629420445529739893461909967206666939096499764990979600)
memo, calls = {0: 0, 1: 1}, [0]
def mfib(n):
    calls[0] += 1
    if n not in memo: memo[n] = mfib(n - 1) + mfib(n - 2)
    return memo[n]
mfib(30)
check('l8 memo fib(30) 59 calls', calls[0] == 59, calls[0])
check('l8 growth 1.618', abs(fib_tree(19)[0] / fib_tree(18)[0] - 1.618) < 0.001)
T1 = lambda n: 1 if n == 1 else T1(n - 1) + 1
T2 = lambda n: 1 if n == 1 else 2 * T2(n // 2) + n
T3 = lambda n: 1 if n == 1 else T3(n // 2) + 1
T4 = lambda n: 1 if n == 1 else 2 * T4(n - 1) + 1
T5 = lambda n: 1 if n == 1 else 2 * T5(n // 2) + 1
T6 = lambda n: 1 if n == 1 else 2 * T6(n // 2) + n * n
check('l8 recurrences', T1(8) == 8 and [T2(n) for n in (2, 4, 8, 16)] == [4, 12, 32, 80] and T3(2 ** 20) == 21 and T4(10) == 1023 and T4(3) == 7
      and all(T2(2 ** k) == 2 ** k * (k + 1) and T5(2 ** k) == 2 * 2 ** k - 1 and T6(2 ** k) < 2 * 4 ** k for k in range(1, 15)))
check('l8 lattice', 101 * 102 // 2 == 5151 and 4 * 5 // 2 == 10 and 2 ** 4 - 1 == 15 and abs((2 ** 101 - 1) / 2.5e30 - 1) < 0.02 and 21 * 22 // 2 == 231
      and 2 ** 21 - 1 == 2097151 and abs(2 ** 253 / 1.4e76 - 1) < 0.04)
# l7 power_fast
def pf(x, n):
    if n == 0: return 1, 0
    if n == 1: return x, 0
    h, m = pf(x, n // 2)
    return (h * h, m + 1) if n % 2 == 0 else (h * h * x, m + 2)
def pf_depth(n): return 1 if n < 2 else 1 + pf_depth(n // 2)
check('l7 multiplications', [pf(1, n)[1] for n in (10, 5, 10 ** 9, 1000, 252, 2520, 100)] == [4, 3, 41, 14, 12, 16, 8], [pf(1, n)[1] for n in (10, 5, 10 ** 9, 1000, 252, 2520, 100)])
check('l7 levels', pf_depth(10 ** 9) == 30 and pf_depth(50) == 6 and pf_depth(100) == 7 and pf_depth(252) == 8)
check('l7 values', abs(1.0002 ** 252 - 1.0517) < 5e-5 and abs(pf(1.05, 252)[0] - 218626.7836322) < 1e-4)
def mr_calls(lo, hi, d=1):
    if lo == hi: return 1, d
    mid = (lo + hi) // 2
    a, da = mr_calls(lo, mid, d + 1); b, db = mr_calls(mid + 1, hi, d + 1)
    return 1 + a + b, max(da, db)
check('l7 max_rec calls', mr_calls(0, 7)[0] == 15 and mr_calls(0, 15)[0] == 31 and mr_calls(0, 999) == (1999, 11))
inv = lambda a: sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
check('l7/l12/hw2 inversions', inv([3, 1, 4, 2]) == 3 and inv([3, 1, 2, 5, 4, 6]) == 3 and inv([5, 2, 4, 6, 1, 3]) == 9 and inv([5, 3, 8, 1, 4, 7, 2, 6]) == 14
      and inv([5, 3, 8, 1]) == 4 and inv([4, 7, 2, 6]) == 3 and sum(1 for a in [5, 3, 8, 1] for b in [4, 7, 2, 6] if a > b) == 7 and inv([2, 2, 1]) == 2)
def merge_count(a, b):
    c, i, j = 0, 0, 0
    while i < len(a) and j < len(b):
        c += 1
        if a[i] <= b[j]: i += 1
        else: j += 1
    return c
check('l7/l12 merge comparisons', max(merge_count(sorted(p[:3]), sorted(p[3:])) for p in itertools.permutations(range(7))) == 6
      and merge_count(list(range(0, 80, 2)), list(range(1, 50, 2)) ) <= 64 and merge_count([2 * i for i in range(39)] + [1000], [2 * i + 1 for i in range(24)] + [999]) == 64
      and merge_count([2, 5, 9, 12], [3, 4, 10, 15]) == 7)
# l9
def bs_looks(n, target_idx=None):
    worst = 0
    for t in range(-1, 2 * n + 1):  # every present value (even) and every gap (odd)
        lo, hi, k = 0, n - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2; k += 1
            if 2 * mid == t: break
            if 2 * mid < t: lo = mid + 1
            else: hi = mid - 1
        worst = max(worst, k)
    return worst
check('l9 worst looks floor(log2 n) + 1', all(bs_looks(n) == n.bit_length() for n in list(range(1, 300)) + [1000, 5000]) and (10 ** 6).bit_length() == 20 and (5000).bit_length() == 13)
def fal_passes(n):
    worst = 0
    for t in range(0, n + 1):
        lo, hi, k = 0, n, 0
        while lo < hi:
            mid = (lo + hi) // 2; k += 1
            if mid < t: lo = mid + 1
            else: hi = mid
        worst = max(worst, k)
    return worst
check('l9 passes at most ceil(log2(n + 1))', all(fal_passes(n) <= math.ceil(math.log2(n + 1)) for n in range(1, 600)) and fal_passes(2520) == 12)
S16 = [3, 8, 12, 17, 21, 26, 30, 35, 41, 47, 52, 58, 64, 70, 77, 85]
def trace(xs, t):
    lo, hi, seen = 0, len(xs) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2; seen.append(mid)
        if xs[mid] == t: return mid, seen
        if xs[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return -1, seen
check('l9 trace 64', trace(S16, 64) == (12, [7, 11, 13, 12]) and trace([8, 3, 12, 5, 20], 5) == (-1, [2, 0]))
s = [96, 98, 99, 100, 100, 100, 101, 103]
check('l9 bisect', (bisect.bisect_left(s, 100), bisect.bisect_right(s, 100)) == (3, 6) and (bisect.bisect_left([1, 3, 3, 3, 8], 3), bisect.bisect_right([1, 3, 3, 3, 8], 3)) == (1, 4))
class Looks:
    def __init__(self, data): self.data = list(data); self.looks = 0
    def __len__(self): return len(self.data)
    def __getitem__(self, i): self.looks += 1; return self.data[i]
def three_read(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target: return mid
        elif xs[mid] < target: lo = mid + 1
        elif xs[mid] > target: hi = mid - 1
    return -1
big = Looks(range(0, 2000000, 2)); three_read(big, 1999998); r11 = big.looks
big = Looks(range(0, 2000000, 2)); three_read(big, 777777); r12 = big.looks
THREE_READ = (r11, r12)
# Fix pass: the cap stays at 45 (a test change, recorded in docs/BACKLOG-INBOX.md); the text now states it and the test-12 line names the
# three-read search. These checks hold the new text: 39 and 50 reads, a miss of 777777 takes 20 passes, a million values need at most 20.
INBOX_L9 = 'inbox (test design, not a check): a correct three-comparison search reads %d and %d against the 45-read cap' % THREE_READ
def one_read(xs, target):
    lo, hi, p = 0, len(xs) - 1, 0
    while lo <= hi:
        p += 1; mid = (lo + hi) // 2; v = xs[mid]
        if v == target: return mid, p
        if v < target: lo = mid + 1
        else: hi = mid - 1
    return -1, p
check('l9 test-12 line: three reads a pass needs 50 on test 12, within 45 on test 11', r11 == 39 and r12 == 50, THREE_READ)
check('l9 prose and test-12 line: a million values need at most 20 passes; the miss of test 12 takes all 20',
      max(one_read(range(10**6), t)[1] for t in (-1, 0, 999999, 10**6, 500000, 777777)) == 20 and one_read(range(0, 2000000, 2), 777777)[1] == 20
      and math.floor(math.log2(10**6)) + 1 == 20)
# l10
imp = lambda q: 0.15 * math.sqrt(q)
check('l10 impacts', [round(imp(q), 4) for q in (32, 48, 40, 44, 46, 45)] == [0.8485, 1.0392, 0.9487, 0.995, 1.0173, 1.0062] and abs((1 / 0.15) ** 2 - 44.44) < 0.005)
def smallest_true(lo, hi, pred, log=None):
    a, b = lo, hi + 1
    while a < b:
        mid = (a + b) // 2
        if log is not None: log.append(mid)
        if pred(mid): b = mid
        else: a = mid + 1
    return a if a <= hi else None
lg = []
check('l10 six tries to 45', smallest_true(0, 64, lambda q: imp(q) >= 1) == 45)
lo, hi, tr = 0, 64, []
while lo < hi:
    mid = (lo + hi) // 2; tr.append((hi - lo + 1, mid))
    if imp(mid) >= 1: hi = mid
    else: lo = mid + 1
check('l10 manipulate trace', tr == [(65, 32), (32, 48), (16, 40), (8, 44), (4, 46), (2, 45)] and lo == 45, tr)
check('l10 savings', smallest_true(1, 100, lambda d: 120 + 35 * d >= 1000) == 26 and 120 + 35 * 25 == 995 and math.ceil(1000 / 35) == 29)
check('l10 trap returns 5', smallest_true(0, 7, lambda d: [97, 99, 102, 98, 96, 101, 103, 105][d] > 100, lg) == 5 and lg[0] == 4)
worst_calls = lambda n: max(len((lambda L: (smallest_true(0, n - 1, lambda x: x >= t, L), L)[1])([])) for t in range(0, n + 1))
check('l10 calls at most ceil(log2(hi - lo + 2))', all(worst_calls(n) <= math.ceil(math.log2(n + 1)) for n in range(1, 300)))
check('l10 powers', 2 ** 19 == 524288 and 2 ** 20 == 1048576 and 2 ** 30 == 1073741824 and 2 ** 26 == 67108864 and 2 ** 27 > 10 ** 8 and 39 < math.log2(10 ** 12) < 40 and 59 < math.log2(10 ** 18 + 2) < 60)
def bond_price(y, coupon, years, face): return sum(coupon / (1 + y) ** t for t in range(1, years + 1)) + face / (1 + y) ** years
def yfp(price, coupon, years, face):
    lo, hi, k = 0.0, 1.0, 0
    while True:
        mid = (lo + hi) / 2; k += 1
        p = bond_price(mid, coupon, years, face)
        if abs(p - price) <= 0.01: return mid, k
        if p > price: lo = mid
        else: hi = mid
y95, k95 = yfp(95, 4, 5, 100)
check('l10 bond', round(bond_price(0.05, 4, 5, 100), 2) == 95.67 and round(bond_price(0.06, 4, 5, 100), 2) == 91.58 and bond_price(0, 4, 5, 100) == 120 and abs(bond_price(1, 4, 5, 100) - 7) < 1e-9
      and round(y95, 4) == 0.0516 and k95 == 15, (y95, k95))
def exact_y(price, c, n, face):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if bond_price(mid, c, n, face) > price: lo = mid
        else: hi = mid
    return lo
margins = []
for price, c, n, face, want in ((95, 4, 5, 100, 0.052), (100, 5, 5, 100, 0.05), (92.5, 3, 7, 100, 0.043), (850, 0, 10, 1000, 0.016)):
    ya = exact_y(price + 0.01, c, n, face); yb = exact_y(price - 0.01, c, n, face)
    margins.append(round(ya, 3) == want == round(yb, 3))
check('l10 every yield within a penny rounds to the expected 3 decimals', all(margins), margins)
N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs(sig, S=100, K=100, r=0.05, T=1):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T)); d2 = d1 - sig * math.sqrt(T)
    return S * N(d1) - K * math.exp(-r * T) * N(d2)
lo, hi = 0.20, 0.30
for _ in range(20):
    mid = (lo + hi) / 2
    if bs(mid) > 12: hi = mid
    else: lo = mid
check('l10 implied vol', [round(bs(x), 2) for x in (0.20, 0.30, 0.25)] == [10.45, 14.23, 12.34] and round((lo + hi) / 2, 4) == 0.2411, (bs(0.2), bs(0.3), bs(0.25), lo))
check('l10 load tests', math.ceil(math.log2(1500)) == 11 and (2500 + 4000) / 2 == 3250 and (1000 + 2500) / 2 == 1750)
check('r3 doubling 15', smallest_true(1, 100, lambda n: 1.05 ** n >= 2) == 15 and round(1.05 ** 14, 3) == 1.980 and round(1.05 ** 15, 3) == 2.079)
# l11
def ins_count(xs):
    a, c, per = list(xs), 0, []
    for i in range(1, len(a)):
        key, j, k = a[i], i - 1, 0
        while j >= 0:
            k += 1
            if a[j] > key: a[j + 1] = a[j]; j -= 1
            else: break
        a[j + 1] = key; per.append(k)
    return a, sum(per), per
check('l11 counts', ins_count([5, 2, 4, 6, 1, 3])[1:] == (12, [1, 2, 1, 4, 4]) and ins_count([3, 1, 2])[1] == 3 and ins_count([1, 2, 4, 3, 5, 6, 8, 7])[1] == 9
      and ins_count([4, 3, 2, 1, 5])[1] == 7 and ins_count([3, 1, 3, 1])[1] == 5 and ins_count(range(1000, 0, -1))[1] == 499500 and ins_count(range(10000))[1] == 9999
      and pairs(40) == 780 and pairs(10000) == 49995000 and pairs(20000) == 199990000)
cmpn = [0]
class K:
    __slots__ = ('v',)
    def __init__(s, v): s.v = v
    def __lt__(s, o): cmpn[0] += 1; return s.v < o.v
def tim(xs):
    cmpn[0] = 0; sorted(K(x) for x in xs); return cmpn[0]
n = 20000
rnd = random.Random(1); shuffled = [rnd.random() for _ in range(n)]
check('l11 Timsort n - 1 comparisons on sorted and strictly falling input', tim(range(n)) == n - 1 and tim(range(n, 0, -1)) == n - 1 and n * 10 < tim(shuffled) < n * math.log2(n))
tr_ = [('09:00:01', 'a'), ('09:00:03', 'b'), ('09:00:02', 'c'), ('09:00:03', 'd'), ('09:00:02', 'e')]
check('l11 sorted is stable', [t[1] for t in sorted(tr_, key=lambda t: t[0])] == ['a', 'c', 'e', 'b', 'd'])
# l12
check('l12 numbers', abs(2 * math.log2(2e6) / math.log2(1e6) - 2.1) < 0.005 and 40 + 25 - 1 == 64 and math.ceil(200 / 15.5) == 13 and abs(1 - 2 * 3 / 15 - 0.6) < 1e-12 and pairs(6) == 15)
big = [(i * 7919) % 20011 for i in range(20000)]
def inv_fast(a):
    if len(a) <= 1: return list(a), 0
    m = len(a) // 2; l, x = inv_fast(a[:m]); r, y = inv_fast(a[m:]); out, i, j, c = [], 0, 0, x + y
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: out.append(l[i]); i += 1
        else: out.append(r[j]); j += 1; c += len(l) - i
    return out + l[i:] + r[j:], c
check('l12 big inversion count', inv_fast(big)[1] == 99930366 and inv_fast(list(range(3000, 0, -1)))[1] == 4498500)
# l13 quicksort
def lomuto(xs, lo, hi, cnt):
    pivot, i = xs[hi], lo
    for j in range(lo, hi):
        cnt[0] += 1
        if xs[j] <= pivot: xs[i], xs[j] = xs[j], xs[i]; i += 1
    xs[i], xs[hi] = xs[hi], xs[i]
    return i
def qs(xs, rnd=None):
    cnt, stack, depth = [0], [(0, len(xs) - 1, 1)], 0
    while stack:
        lo, hi, d = stack.pop()
        if lo >= hi: continue
        depth = max(depth, d)
        if rnd: r = rnd.randint(lo, hi); xs[r], xs[hi] = xs[hi], xs[r]
        p = lomuto(xs, lo, hi, cnt)
        stack.append((lo, p - 1, d + 1)); stack.append((p + 1, hi, d + 1))
    return cnt[0], depth
x = [7, 2, 9, 4, 1, 8, 5]; c0 = [0]; p0 = lomuto(x, 0, 6, c0)
check('l13 partition trace', (p0, x, c0[0]) == (3, [2, 4, 1, 5, 9, 8, 7], 6))
x = [3, 8, 2, 5, 1, 4]; p1 = lomuto(x, 0, 5, [0]); x2 = [9, 3, 7, 1, 8, 2, 6, 5]; p2 = lomuto(x2, 2, 5, [0])
check('l13 more partitions', (p1, x) == (3, [3, 2, 1, 4, 8, 5]) and (p2, x2) == (3, [9, 3, 1, 2, 8, 7, 6, 5]))
check('l13 comparison counts', qs([7, 2, 9, 4, 1, 8, 5])[0] == 12 and qs(list(range(1, 8)))[0] == 21 and qs(list(range(1000)))[0] == 499500 and pairs(2000) == 1999000)
def stable_demo():
    xs = [(5, 'a'), (5, 'b'), (1, 'c')]
    def part(lo, hi):
        pv, i = xs[hi][0], lo
        for j in range(lo, hi):
            if xs[j][0] <= pv: xs[i], xs[j] = xs[j], xs[i]; i += 1
        xs[i], xs[hi] = xs[hi], xs[i]; return i
    def srt(lo, hi):
        if lo < hi: p = part(lo, hi); srt(lo, p - 1); srt(p + 1, hi)
    srt(0, 2); return xs
check('l13 not stable', stable_demo() == [(1, 'c'), (5, 'b'), (5, 'a')])
rnd = random.Random(7); n = 20000; reps = 40
avg = sum(qs(rnd.sample(range(10 * n), n), rnd)[0] for _ in range(reps)) / reps
check('l13 average about 1.39 n log2 n (2n ln n, less a linear term)', 1.15 < avg / (n * math.log2(n)) < 1.39 and abs((2 * (n + 1) * (math.log(n) + 0.5772) - 4 * n) / avg - 1) < 0.02, avg / (n * math.log2(n)))
srt_in = sum(qs(list(range(n)), rnd)[0] for _ in range(10)) / 10
check('l13 random pivot does not care about sorted input', abs(srt_in / avg - 1) < 0.06, srt_in / avg)
def qsel(xs, k, rnd, lo=0, hi=None):
    cnt = [0]; hi = len(xs) - 1 if hi is None else hi
    while lo < hi:
        r = rnd.randint(lo, hi); xs[r], xs[hi] = xs[hi], xs[r]
        p = lomuto(xs, lo, hi, cnt)
        if k == p: break
        if k < p: hi = p - 1
        else: lo = p + 1
    return xs[k], cnt[0], lo, hi
n, reps = 100001, 60
med = sum(qsel(rnd.sample(range(10 * n), n), n // 2, rnd)[1] for _ in range(reps)) / reps / n
ext = sum(qsel(rnd.sample(range(10 * n), n), 0, rnd)[1] for _ in range(reps)) / reps / n
check('l13 quickselect about 3.4n for a median, about 2n at an end', abs(med - 3.39) < 0.25 and abs(ext - 2.0) < 0.25, (med, ext))
sizes = [(i * 7919) % 10007 for i in range(100001)]
check('l13/hw3 order statistics', sorted(sizes)[50000] == 5003 and sorted(sizes)[100001 - 20000] == 8005 and sorted([3, 1, 3, 2, 3])[5 - 4] == 2)
check('l13 VaR table', abs(1e7 * math.log2(1e7) / 2.3e8 - 1) < 0.02 and math.ceil(math.log2(1e7 + 1)) == 24 and 500 * 24 == 12000 and abs(500 * 1e7 / (1e7 * math.log2(1e7)) - 21.5) < 0.5 and abs(pairs(10 ** 7) / 5e13 - 1) < 0.01)
def three_stats():  # hw3 model answer: median first, then the 5% index in the left part, then the 1% index inside that
    xs = rnd.sample(range(10 * n), n); tot = 0
    _, c, _, _ = qsel(xs, n // 2, rnd); tot += c
    _, c, _, _ = qsel(xs, n // 20, rnd, 0, n // 2 - 1); tot += c
    _, c, _, _ = qsel(xs, n // 100, rnd, 0, n // 20 - 1); tot += c
    return tot / n
nested = sum(three_stats() for _ in range(40)) / 40
NESTED = (nested, med)
check('hw3 nested selects cost under two median selects', nested < 2 * med, NESTED)
# l14
def greedy(amount, coins):
    k = 0
    for c in sorted(coins, reverse=True): k += amount // c; amount %= c
    return k if amount == 0 else None
def best(limit, coins):
    dp = [0] + [10 ** 9] * limit
    for a in range(1, limit + 1):
        dp[a] = 1 + min(dp[a - c] for c in coins if c <= a)
    return dp
def fails(coins, limit=3000):
    dp = best(limit, coins); return [a for a in range(1, limit + 1) if greedy(a, coins) != dp[a]]
check('l14 greedy optimal: UK, US, 1-2-5-10, powers of 3', not fails([1, 2, 5, 10, 20, 50]) and not fails([1, 2, 5, 10, 20, 50, 100, 200]) and not fails([1, 5, 10, 25]) and not fails([1, 2, 5, 10]) and not fails([1, 3, 9, 27]))
check('l14 greedy fails', fails([1, 3, 4], 10) == [6, 10] and [greedy(a, [1, 3, 4]) for a in range(1, 11)] == [1, 2, 1, 1, 2, 3, 2, 2, 3, 4] and fails([1, 5, 12])[0] == 15 and greedy(30, [1, 10, 25]) == 6
      and best(30, [1, 10, 25])[30] == 3 and greedy(87, [1, 2, 5, 10, 20, 50]) == 5 and greedy(10 ** 6, [1, 2, 5, 10, 20, 50, 100, 200]) == 5000)
MEET = [(9, 15), (9.5, 10.5), (10.5, 11.5), (11, 12.5), (12, 13), (13.5, 14.5), (14, 16)]
def brute_meet(iv):
    b = 0
    for r in range(len(iv) + 1):
        for sub in itertools.combinations(sorted(iv, key=lambda t: t[1]), r):
            if all(sub[i][1] <= sub[i + 1][0] for i in range(len(sub) - 1)): b = max(b, r)
    return b
def eft(iv, key=lambda t: t[1], strict=False):
    c, end = 0, float('-inf')
    for s_, e_ in sorted(iv, key=key):
        if (s_ > end) if strict else (s_ >= end): c += 1; end = e_
    return c
rnd = random.Random(3); ok = True
for _ in range(400):
    iv = [(a, a + rnd.randint(1, 6)) for a in (rnd.randint(0, 14) for _ in range(rnd.randint(0, 8)))]
    ok = ok and eft(iv) == brute_meet(iv)
check('l14 earliest finish first is optimal on 400 random diaries', ok and brute_meet(MEET) == 4 and eft(MEET) == 4)
check('l14 wrong keys', eft(MEET, key=lambda t: t) == 1 and eft(MEET, strict=True) == 3 and eft([(1, 5), (4, 7), (6, 10)], key=lambda t: t[1] - t[0]) == 1 and brute_meet([(1, 5), (4, 7), (6, 10)]) == 2)
check('l14 knapsack', 300 + 4000 * 0.04 == 460 and 20 + 18 == 38 and 300 * 100.02 + 500 * 100.03 + 200 * 100.05 == 100031.0 and round((100.02 + 100.03 + 100.05 + 100.08) / 4 * 1000) == 100045)
sp = lambda a, b, rho: (a + b) / math.sqrt(2 + 2 * rho)
check('l14 Sharpe pairs', [round(sp(1.5, 1.4, 0.95), 2), round(sp(1.5, 1.0, 0), 2), round(sp(1.4, 1.0, 0), 2)] == [1.47, 1.77, 1.70])
# homework
check('hw1 numbers', pairs(500) * 250 == 31187500 and 500 * 499 * 250 == 62375000 and 3000 * 2999 == 8997000 and abs(8997000 * 250 / 2.25e9 - 1) < 0.001 and pairs(3000) == 4498500
      and 10 * pairs(100000) == 49999500000 and abs(8997000 * 96 / 1e9 - 0.86) < 0.01)
def trib(n):
    a = [1, 1, 2]
    while len(a) <= n: a.append(a[-1] + a[-2] + a[-3])
    return a[n]
def n_splits(feed, listed):
    if feed == '': return 1
    return sum(n_splits(feed[len(t):], listed) for t in set(listed) if feed.startswith(t))
check('hw2 split counts', trib(12) == 927 and n_splits('A' * 12, ['A', 'AA', 'AAA']) == 927 and n_splits('BA' * 8, ['BA', 'BAB', 'AB', 'A', 'B']) == 4374)
def price_loop(S, n, u, d, p, disc, Kk):
    v = [max(S * u ** j * d ** (n - j) - Kk, 0) for j in range(n + 1)]; upd = 0
    for step in range(n - 1, -1, -1):
        v = [disc * (p * v[j + 1] + (1 - p) * v[j]) for j in range(step + 1)]; upd += step + 1
    return v[0], upd
def price_rec(S, step, n, u, d, p, disc, Kk):
    if step == n: return max(S - Kk, 0)
    return disc * (p * price_rec(S * u, step + 1, n, u, d, p, disc, Kk) + (1 - p) * price_rec(S * d, step + 1, n, u, d, p, disc, Kk))
t0 = time.perf_counter(); pl = price_loop(100, 2000, 1.002, 1 / 1.002, 0.5, 0.99999, 100); dt = time.perf_counter() - t0
check('hw2 pricer loop', abs(price_loop(100, 12, 1.1, 0.9, 0.55, 0.99, 100)[0] - price_rec(100, 0, 12, 1.1, 0.9, 0.55, 0.99, 100)) < 1e-9 and pl[1] == 2001000 and dt < 1.0, dt)
def min_cap(sizes, days):
    def need(cap):
        d, load = 1, 0
        for s_ in sizes:
            if load + s_ > cap: d += 1; load = 0
            load += s_
        return d
    return next(c for c in range(max(sizes), sum(sizes) + 1) if need(c) <= days)
check('hw3 capacities', [min_cap(list(range(1, 11)), 5), min_cap([3, 2, 2, 4, 1, 4], 3), min_cap([1, 2, 3, 1, 1], 4), min_cap([7, 2, 5, 10, 8], 2), min_cap([7, 2, 5, 10, 8], 5), min_cap([7, 2, 5, 10, 8], 1)] == [15, 6, 3, 18, 10, 32])
R = [1000000 + 3 * ((j + 137017) % 200000) for j in range(200000)]
check('hw3 ring facts', R.index(min(R)) == 62983 and [R.index(s_) if s_ in set(R) else -1 for s_ in (1411051, 1411048, 1000000, 1599997, 1300000)] == [0, 199999, 62983, 62982, 162983] and (int((-2 + math.sqrt(44)) / 0.002)) == 2316)

# ------------------------------------------------------------------ submissions for Part B (key, mistake, key of the line that should show, code)
M = []
def m(key, name, expect, code): M.append((key, name, expect, code))

# ---------- l1 count_pairs
m('l1#8', 'self-pair j from i', 'test-1', '''
def count_pairs(prices, threshold):
    c = 0
    for i in range(len(prices)):
        for j in range(i, len(prices)):
            if prices[i] * prices[j] > threshold: c += 1
    return c
''')
m('l1#8', 'pairs of distinct values (set)', 'test-4', '''
def count_pairs(prices, threshold):
    v = sorted(set(prices)); c = 0
    for i in range(len(v)):
        for j in range(i + 1, len(v)):
            if v[i] * v[j] > threshold: c += 1
    return c
''')
m('l1#8', '>= threshold', 'test-1', '''
def count_pairs(prices, threshold):
    c = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            if prices[i] * prices[j] >= threshold: c += 1
    return c
''')
# ---------- l2
L2 = '''
def steps_a(n): return 50 * n
def steps_b(n): return n * n
'''
m('l2#8', 'always A', 'test-4', L2 + 'def cheaper(n): return "A"\n')
m('l2#8', 'no tie', 'test-6', L2 + 'def cheaper(n): return "A" if steps_a(n) <= steps_b(n) else "B"\n')
m('l2#8', 'ratio, n=0 divides', 'test-10', L2 + '''
def cheaper(n):
    r = steps_b(n) / steps_a(n)
    return "B" if r < 1 else "A" if r > 1 else "tie"
''')
# ---------- l3
m('l3#3', 'len(ticks)', 'test-1', 'def stream_mean(ticks):\n    return sum(ticks) / len(ticks) if len(ticks) else None\n')
m('l3#3', 'no empty check', 'test-3', 'def stream_mean(ticks):\n    t = c = 0\n    for x in ticks:\n        t += x; c += 1\n    return t / c\n')
m('l3#3', 'list(ticks)', 'test-7', 'def stream_mean(ticks):\n    xs = list(ticks)\n    return sum(xs) / len(xs) if xs else None\n')
RT = 'def range_total(pre, i, j):\n    return pre[j] - pre[i]\n'
m('l3#5', 'no leading 0', 'test-1', 'def prefix_sums(prices):\n    pre = []; t = 0\n    for p in prices:\n        t += p; pre.append(t)\n    return pre\n' + RT)
m('l3#5', 'empty gives []', 'test-2', 'def prefix_sums(prices):\n    if not prices: return []\n    pre = [0]\n    for p in prices: pre.append(pre[-1] + p)\n    return pre\n' + RT)
m('l3#5', 'pre[j-1]', 'test-4', 'def prefix_sums(prices):\n    pre = [0]\n    for p in prices: pre.append(pre[-1] + p)\n    return pre\ndef range_total(pre, i, j):\n    return pre[j - 1] - pre[i]\n')
# ---------- l4
m('l4#6', 'check after write', 'test-2', 'def total_copies(n):\n    cap, size, copies = 1, 0, 0\n    for _ in range(n):\n        size += 1\n        if size == cap:\n            cap *= 2; copies += size\n    return copies\n')
m('l4#6', 'counts the new one', 'test-3', 'def total_copies(n):\n    cap, size, copies = 1, 0, 0\n    for _ in range(n):\n        if size == cap:\n            cap *= 2; copies += size + 1\n        size += 1\n    return copies\n')
# ---------- l5
PW = 'def power(x, n):\n    if n == 0: return 1\n    return x * power(x, n - 1)\n'
SL = 'def sum_list(xs):\n    if not xs: return 0\n    return xs[0] + sum_list(xs[1:])\n'
m('l5#5', 'answer dropped', 'test-1', 'def sum_list(xs):\n    if not xs: return 0\n    sum_list(xs[1:])\n    return xs[0]\n' + PW)
m('l5#5', 'base len 1', 'test-2', 'def sum_list(xs):\n    if len(xs) == 1: return xs[0]\n    return xs[0] + sum_list(xs[1:])\n' + PW)
m('l5#5', 'power base n==1', 'test-7', SL + 'def power(x, n):\n    if n == 1: return x\n    return x * power(x, n - 1)\n')
m('l5#5', 'syntax error (load)', 'error', SL + 'def power(x, n)\n    return 1\n')
m('l5#9', 'subfolders skipped', 'test-1', 'def total_pnl(folder):\n    return sum(v for v in folder.values() if not isinstance(v, dict))\n')
m('l5#9', 'adds dict (TypeError)', 'test-1', 'def total_pnl(folder):\n    t = 0\n    for v in folder.values(): t += v\n    return t\n')
# ---------- l6
DP = 'def depth(n, d=1):\n    if n < 2: return d\n    return max(depth(n - 1, d + 1), depth(n - 2, d + 1))\n'
m('l6#6', 'recursive sum_to', 'test-3', 'def sum_to(n):\n    if n == 0: return 0\n    return n + sum_to(n - 1)\n' + DP)
m('l6#6', 'depth ignores d', 'test-10', 'def sum_to(n):\n    return n * (n + 1) // 2\ndef depth(n, d=1):\n    if n < 2: return 1\n    return 1 + max(depth(n - 1), depth(n - 2))\n')
m('l6#9', 'sum not max', 'test-1', 'def levels(node):\n    return 1 + sum(levels(c) for c in node["children"])\n')
m('l6#9', 'leaf counts 0', 'test-1', 'def levels(node):\n    if not node["children"]: return 0\n    return 1 + max(levels(c) for c in node["children"])\n')
m('l6#9', 'VALID: generator inside max', 'none', 'def levels(node):\n    return 1 + max((levels(c) for c in node["children"]), default=0)\n')
# ---------- l7
PF = 'def power_fast(x, n):\n    if n == 0: return 1, 0\n    if n == 1: return x, 0\n    h, m = power_fast(x, n // 2)\n    if n % 2 == 0: return h * h, m + 1\n    return h * h * x, m + 2\n'
MR = 'def max_rec(xs, lo, hi):\n    if lo == hi: return xs[lo]\n    mid = (lo + hi) // 2\n    return max(max_rec(xs, lo, mid), max_rec(xs, mid + 1, hi))\n'
m('l7#5', 'one-at-a-time max_rec', 'test-5', 'def max_rec(xs, lo, hi):\n    if lo == hi: return xs[lo]\n    return max(xs[lo], max_rec(xs, lo + 1, hi))\n' + PF)
m('l7#5', 'power_fast called twice', 'test-10', MR + 'def power_fast(x, n):\n    if n == 0: return 1, 0\n    if n == 1: return x, 0\n    a, m = power_fast(x, n // 2)\n    b, _ = power_fast(x, n // 2)\n    if n % 2 == 0: return a * b, m + 1\n    return a * b * x, m + 2\n')
m('l7#5', 'mid not mid+1 (RecursionError)', 'test-1', 'def max_rec(xs, lo, hi):\n    if lo == hi: return xs[lo]\n    mid = (lo + hi) // 2\n    return max(max_rec(xs, lo, mid), max_rec(xs, mid, hi))\n' + PF)
# ---------- l8
FB = 'memo = {0: 0, 1: 1}\ndef fib(n):\n    if n not in memo: memo[n] = fib(n - 1) + fib(n - 2)\n    return memo[n]\n'
FC = 'def fib_calls(n):\n    a, b = 1, 1\n    for _ in range(n - 1): a, b = b, 1 + a + b\n    return a if n == 0 else b\n'
m('l8#5', 'C(0) = 0', 'test-1', 'def fib_calls(n):\n    if n == 0: return 0\n    a, b = 1, 1\n    for _ in range(n - 1): a, b = b, 1 + a + b\n    return b\n' + FB)
m('l8#5', 'recursive count', 'test-6', 'def fib_calls(n):\n    if n < 2: return 1\n    return 1 + fib_calls(n - 1) + fib_calls(n - 2)\n' + FB)
m('l8#5', 'naive fib', 'test-10', FC + 'def fib(n):\n    if n < 2: return n\n    return fib(n - 1) + fib(n - 2)\n')
# ---------- l9
m('l9#3', 'linear scan', 'test-11', 'def binary_search(xs, target):\n    for i in range(len(xs)):\n        if xs[i] == target: return i\n    return -1\n')
m('l9#3', 'while lo < hi', 'test-1', 'def binary_search(xs, target):\n    lo, hi = 0, len(xs) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if xs[mid] == target: return mid\n        if xs[mid] < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1\n')
m('l9#3', 'three reads a pass (correct, over the read cap)', 'test-12', 'def binary_search(xs, target):\n    lo, hi = 0, len(xs) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if xs[mid] == target: return mid\n        elif xs[mid] < target: lo = mid + 1\n        elif xs[mid] > target: hi = mid - 1\n    return -1\n')
m('l9#3', 'reads xs[0] first', 'test-4', 'def binary_search(xs, target):\n    if xs[0] > target: return -1\n    lo, hi = 0, len(xs) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        v = xs[mid]\n        if v == target: return mid\n        if v < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1\n')
m('l9#5', 'returns first match', 'test-1', 'def first_at_least(xs, target):\n    lo, hi = 0, len(xs)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if xs[mid] == target: return mid\n        if xs[mid] < target: lo = mid + 1\n        else: hi = mid\n    return lo\n')
m('l9#5', 'hi = len - 1', 'test-4', 'def first_at_least(xs, target):\n    lo, hi = 0, len(xs) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if xs[mid] < target: lo = mid + 1\n        else: hi = mid\n    return lo\n')
m('l9#9', 'bisect_right', 'test-2', 'from bisect import bisect_right\ndef next_trading_day(days, day):\n    i = bisect_right(days, day)\n    return None if i == len(days) else days[i]\n')
m('l9#9', 'no None', 'test-4', 'from bisect import bisect_left\ndef next_trading_day(days, day):\n    return days[bisect_left(days, day)]\n')
m('l9#9', 'days[-1] check', 'test-6', 'from bisect import bisect_left\ndef next_trading_day(days, day):\n    if day > days[-1]: return None\n    return days[bisect_left(days, day)]\n')
# ---------- l10
m('l10#3', 'hi is the none marker', 'test-3', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a if a < hi else None\n')
m('l10#3', 'bare return', 'test-4', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi + 1\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a\n')
m('l10#3', 'pred(hi + 1) tried and returned', 'test-4', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi + 1\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a if pred(a) else None\n')
ST = 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi + 1\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a if a <= hi else None\n'
m('l10#4', 'range ends at n', 'test-2', ST + 'def isqrt(n):\n    return smallest_true(0, n, lambda x: x * x > n) - 1\n')
BP = 'def bond_price(y, coupon, years, face):\n    pv = sum(coupon / (1 + y) ** t for t in range(1, years + 1))\n    return pv + face / (1 + y) ** years\n'
m('l10#5', 'updates the wrong way', 'test-1', BP + 'def yield_for_price(price, coupon, years, face):\n    lo, hi = 0.0, 1.0\n    for _ in range(60):\n        mid = (lo + hi) / 2\n        if bond_price(mid, coupon, years, face) > price: hi = mid\n        else: lo = mid\n    return (lo + hi) / 2\n')
m('l10#5', 'no end check', 'test-8', BP + 'def yield_for_price(price, coupon, years, face):\n    lo, hi = 0.0, 1.0\n    for _ in range(60):\n        mid = (lo + hi) / 2\n        if bond_price(mid, coupon, years, face) > price: lo = mid\n        else: hi = mid\n    return (lo + hi) / 2\n')
# ---------- l11
m('l11#3', 'no break', 'test-1', 'def insertion_sort(xs):\n    a = list(xs); comps = 0\n    for i in range(1, len(a)):\n        for j in range(i, 0, -1):\n            comps += 1\n            if a[j - 1] > a[j]: a[j - 1], a[j] = a[j], a[j - 1]\n    return a, comps\n')
m('l11#3', '>=', 'test-6', 'def insertion_sort(xs):\n    a = list(xs); comps = 0\n    for i in range(1, len(a)):\n        key = a[i]; j = i - 1\n        while j >= 0:\n            comps += 1\n            if a[j] >= key:\n                a[j + 1] = a[j]; j -= 1\n            else: break\n        a[j + 1] = key\n    return a, comps\n')
m('l11#3', 'in place', 'test-8', 'def insertion_sort(xs):\n    a = xs; comps = 0\n    for i in range(1, len(a)):\n        key = a[i]; j = i - 1\n        while j >= 0:\n            comps += 1\n            if a[j] > key:\n                a[j + 1] = a[j]; j -= 1\n            else: break\n        a[j + 1] = key\n    return a, comps\n')
m('l11#8', 'whole tuples', 'test-4', 'def sort_trades(trades):\n    a = list(trades)\n    for i in range(1, len(a)):\n        key = a[i]; j = i - 1\n        while j >= 0 and a[j] > key:\n            a[j + 1] = a[j]; j -= 1\n        a[j + 1] = key\n    return a\n')
m('l11#8', '>= on times', 'test-1', 'def sort_trades(trades):\n    a = list(trades)\n    for i in range(1, len(a)):\n        key = a[i]; j = i - 1\n        while j >= 0 and a[j][0] >= key[0]:\n            a[j + 1] = a[j]; j -= 1\n        a[j + 1] = key\n    return a\n')
# ---------- l12
m('l12#2', 'tail of a dropped', 'test-3', 'def merge(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    out.extend(b[j:])\n    return out\n')
m('l12#2', 'recursive merge', 'test-9', 'def merge(a, b):\n    if not a: return list(b)\n    if not b: return list(a)\n    if a[0] <= b[0]: return [a[0]] + merge(a[1:], b)\n    return [b[0]] + merge(a, b[1:])\n')
m('l12#2', 'out = out + [x]', 'test-9', 'def merge(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out = out + [a[i]]; i += 1\n        else: out = out + [b[j]]; j += 1\n    return out + a[i:] + b[j:]\n')
MG = 'def merge(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    out.extend(a[i:]); out.extend(b[j:])\n    return out\n'
m('l12#3', 'splits off one value', 'test-7', MG + 'def merge_sort(xs):\n    if len(xs) <= 1: return list(xs)\n    return merge(xs[:1], merge_sort(xs[1:]))\n')
m('l12#3', 'base case len == 0 (RecursionError)', 'test-1', MG + 'def merge_sort(xs):\n    if len(xs) == 0: return xs\n    mid = len(xs) // 2\n    return merge(merge_sort(xs[:mid]), merge_sort(xs[mid:]))\n')
m('l12#7', '< on ties', 'test-8', 'def count_inversions(xs):\n    def sc(a):\n        if len(a) <= 1: return list(a), 0\n        mid = len(a) // 2\n        l, x = sc(a[:mid]); r, y = sc(a[mid:])\n        out, i, j, c = [], 0, 0, x + y\n        while i < len(l) and j < len(r):\n            if l[i] < r[j]: out.append(l[i]); i += 1\n            else: out.append(r[j]); j += 1; c += len(l) - i\n        return out + l[i:] + r[j:], c\n    return sc(xs)[1]\n')
m('l12#7', 'every pair', 'test-9', 'def count_inversions(xs):\n    c = 0\n    for i in range(len(xs)):\n        for j in range(i + 1, len(xs)):\n            if xs[i] > xs[j]: c += 1\n    return c\n')
m('l12#8', 'whole tuples', 'test-2?', 'def merge_logs(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n')
# ---------- l13
m('l13#3', 'i starts at 0', 'test-2', 'def partition(xs, lo, hi):\n    pivot = xs[hi]; i = 0\n    for j in range(lo, hi):\n        if xs[j] <= pivot:\n            xs[i], xs[j] = xs[j], xs[i]; i += 1\n    xs[i], xs[hi] = xs[hi], xs[i]\n    return i\n')
PT = 'import random\ndef partition(xs, lo, hi):\n    pivot = xs[hi]; i = lo\n    for j in range(lo, hi):\n        if xs[j] <= pivot:\n            xs[i], xs[j] = xs[j], xs[i]; i += 1\n    xs[i], xs[hi] = xs[hi], xs[i]\n    return i\n'
m('l13#4', 'fixed last pivot', 'test-7', PT + 'def quicksort(xs):\n    def sort(lo, hi):\n        if lo >= hi: return\n        p = partition(xs, lo, hi)\n        sort(lo, p - 1); sort(p + 1, hi)\n    sort(0, len(xs) - 1)\n')
m('l13#4', 'returns xs', 'test-2', PT + 'def quicksort(xs):\n    def sort(lo, hi):\n        if lo >= hi: return\n        r = random.randint(lo, hi); xs[r], xs[hi] = xs[hi], xs[r]\n        p = partition(xs, lo, hi)\n        sort(lo, p - 1); sort(p + 1, hi)\n    sort(0, len(xs) - 1)\n    return xs\n')
m('l13#8', 'full quicksort, last pivot', 'test-7', PT + 'def quickselect(xs, k):\n    def sort(lo, hi):\n        if lo >= hi: return\n        p = partition(xs, lo, hi)\n        sort(lo, p - 1); sort(p + 1, hi)\n    sort(0, len(xs) - 1)\n    return xs[k]\n')
m('l13#8', 'recursive one side, last pivot', 'page passes?', PT + 'def quickselect(xs, k, lo=0, hi=None):\n    if hi is None: hi = len(xs) - 1\n    if lo >= hi: return xs[lo]\n    p = partition(xs, lo, hi)\n    if k == p: return xs[p]\n    if k < p: return quickselect(xs, k, lo, p - 1)\n    return quickselect(xs, k, p + 1, hi)\n')
m('l13#8', 'sorted()', 'test-9', PT + 'def quickselect(xs, k):\n    return sorted(xs)[k]\n')
# ---------- l14
m('l14#3', 'assumes ascending input', 'test-3', 'def coins_greedy(amount, coins):\n    taken = []\n    for c in reversed(coins):\n        while amount >= c: taken.append(c); amount -= c\n    return taken if amount == 0 else None\n')
m('l14#3', 'no sort at all', 'test-3?', 'def coins_greedy(amount, coins):\n    taken = []\n    for c in coins:\n        while amount >= c: taken.append(c); amount -= c\n    return taken if amount == 0 else None\n')
m('l14#3', 'no None', 'test-5', 'def coins_greedy(amount, coins):\n    taken = []\n    for c in sorted(coins, reverse=True):\n        while amount >= c: taken.append(c); amount -= c\n    return taken\n')
m('l14#5', 'sorted by start', 'test-1 got 1', 'def max_meetings(intervals):\n    count, end = 0, float("-inf")\n    for s, e in sorted(intervals):\n        if s >= end: count += 1; end = e\n    return count\n')
m('l14#5', '> not >=', 'test-1 got 3', 'def max_meetings(intervals):\n    count, end = 0, float("-inf")\n    for s, e in sorted(intervals, key=lambda iv: iv[1]):\n        if s > end: count += 1; end = e\n    return count\n')
# ---------- review-3
m('review-3#4', 'plain merge', 'test-1', 'def merge_unique(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n')
m('review-3#6', 'bisect_left twice', 'test-1', 'from bisect import bisect_left, bisect_right\ndef count_between(closes, low, high):\n    return bisect_left(closes, high) - bisect_left(closes, low)\n')
m('review-3#6', 'no low > high check', 'test-7', 'from bisect import bisect_left, bisect_right\ndef count_between(closes, low, high):\n    return bisect_right(closes, high) - bisect_left(closes, low)\n')
m('review-3#7', 'None - 1', 'test-3', ST + 'def max_size(limit, risk, hi):\n    return smallest_true(0, hi, lambda n: risk(n) > limit) - 1\n')
m('review-3#7', 'returns -1', 'test-4', ST + 'def max_size(limit, risk, hi):\n    f = smallest_true(0, hi, lambda n: risk(n) > limit)\n    return hi if f is None else f - 1\n')
# ---------- homework-1
m('homework-1#5', 'global low then high', 'test-2', 'def best_trade(prices):\n    if not prices: return 0\n    i = prices.index(min(prices))\n    return max(prices[i:]) - prices[i]\n')
m('homework-1#5', 'best starts at -inf', 'test-3', 'def best_trade(prices):\n    if len(prices) < 2: return 0\n    best = float("-inf"); low = prices[0]\n    for p in prices[1:]:\n        best = max(best, p - low); low = min(low, p)\n    return best\n')
m('homework-1#5', 'prices[0]', 'test-4', 'def best_trade(prices):\n    best = 0; low = prices[0]\n    for p in prices:\n        best = max(best, p - low); low = min(low, p)\n    return best\n')
m('homework-1#5', 'pair loop', 'test-8', 'def best_trade(prices):\n    best = 0\n    for i in range(len(prices)):\n        for j in range(i + 1, len(prices)):\n            if prices[j] - prices[i] > best: best = prices[j] - prices[i]\n    return best\n')
m('homework-1#6', 'resize after write', 'test-1', 'def copies_fixed(n, step):\n    cap, size, copies = step, 0, 0\n    for _ in range(n):\n        size += 1\n        if size == cap:\n            cap += step; copies += size\n    return copies\n')
# ---------- homework-2
m('homework-2#0', 'appends the sublist', 'test-1', 'def flatten(xs):\n    out = []\n    for x in xs:\n        if isinstance(x, list): out.append(flatten(x))\n        else: out.append(x)\n    return out\n')
m('homework-2#5', '< on ties', 'test-5', 'def sort_count(xs):\n    if len(xs) <= 1: return list(xs), 0\n    mid = len(xs) // 2\n    a, x = sort_count(xs[:mid]); b, y = sort_count(xs[mid:])\n    out, i, j, c = [], 0, 0, x + y\n    while i < len(a) and j < len(b):\n        if a[i] < b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1; c += len(a) - i\n    return out + a[i:] + b[j:], c\n')
m('homework-2#5', 'pair by pair', 'test-7', 'def sort_count(xs):\n    c = 0\n    for i in range(len(xs)):\n        for j in range(i + 1, len(xs)):\n            if xs[i] > xs[j]: c += 1\n    out = list(xs)\n    for i in range(1, len(out)):\n        k = out[i]; j = i - 1\n        while j >= 0 and out[j] > k: out[j + 1] = out[j]; j -= 1\n        out[j + 1] = k\n    return out, c\n')
m('homework-2#5', 'pair by pair, count only loop', 'test-7', 'def sort_count(xs):\n    c = 0\n    n = len(xs)\n    for i in range(n):\n        x = xs[i]\n        for j in range(i + 1, n):\n            if x > xs[j]: c += 1\n    return sorted(xs), c\n')
m('homework-2#6', 'recursion', 'test-4', 'def total_value(fund):\n    return fund["value"] + sum(total_value(c) for c in fund["children"])\n')
m('homework-2#6', 'plain recursion loop', 'test-4', 'def total_value(fund):\n    t = fund["value"]\n    for c in fund["children"]: t += total_value(c)\n    return t\n')
m('homework-2#6', 'root children only', 'test-1', 'def total_value(fund):\n    return fund["value"] + sum(c["value"] for c in fund["children"])\n')
m('homework-2#9', 'no empty base case', 'test-2', 'def split_feed(feed, listed):\n    res = []\n    for t in set(listed):\n        if feed == t: res.append([t])\n        elif feed.startswith(t):\n            for r in split_feed(feed[len(t):], listed): res.append([t] + r)\n    return res\n')
m('homework-2#9', 'list as given', 'test-5', 'def split_feed(feed, listed):\n    if feed == "": return [[]]\n    res = []\n    for t in listed:\n        if feed.startswith(t):\n            for r in split_feed(feed[len(t):], listed): res.append([t] + r)\n    return res\n')
m('homework-2#9', 'sorts listed in place', 'test-12', 'def split_feed(feed, listed):\n    listed.sort()\n    if feed == "": return [[]]\n    res = []\n    for t in set(listed):\n        if feed.startswith(t):\n            for r in split_feed(feed[len(t):], listed): res.append([t] + r)\n    return res\n')
# ---------- homework-3
m('homework-3#4', 'tries every capacity', 'test-8', 'def min_capacity(sizes, days):\n    cap = max(sizes)\n    while True:\n        d, load = 1, 0\n        for s in sizes:\n            if load + s > cap: d += 1; load = 0\n            load += s\n        if d <= days: return cap\n        cap += 1\n')
MK = 'def merge(a, b):\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n'
m('homework-3#5', 'lists[0] on no lists', 'test-2', MK + 'def merge_k(lists):\n    while len(lists) > 1:\n        lists = [merge(lists[i], lists[i + 1]) if i + 1 < len(lists) else lists[i] for i in range(0, len(lists), 2)]\n    return list(lists[0])\n')
m('homework-3#5', 'one growing result', 'test-6', MK + 'def merge_k(lists):\n    out = []\n    for l in lists: out = merge(out, l)\n    return out\n')
m('homework-3#5', 'sorted()', 'test-7', MK + 'def merge_k(lists):\n    return sorted(x for l in lists for x in l)\n')
KL = 'import random\ndef kth_largest(xs, k):\n    a = %s\n    target = len(a) - k\n    def sel(lo, hi):\n        if lo >= hi: return a[lo]\n        %s\n        pivot, i = a[hi], lo\n        for j in range(lo, hi):\n            if a[j] <= pivot:\n                a[i], a[j] = a[j], a[i]; i += 1\n        a[i], a[hi] = a[hi], a[i]\n        if i == target: return a[i]\n        return sel(lo, i - 1) if target < i else sel(i + 1, hi)\n    return sel(0, len(a) - 1)\n'
m('homework-3#6', 'in place', 'test-7', KL % ('xs', 'r = random.randint(lo, hi); a[r], a[hi] = a[hi], a[r]'))
m('homework-3#6', 'recursive, fixed first pivot', 'test-8', KL % ('list(xs)', 'a[lo], a[hi] = a[hi], a[lo]'))
m('homework-3#6', 'sorted()', 'test-10', 'import random\ndef kth_largest(xs, k):\n    return sorted(xs)[len(xs) - k]\n')
m('homework-3#8', '< not <=', 'test-5', 'def find_trade(ring, seq):\n    lo, hi = 0, len(ring) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if ring[mid] == seq: return mid\n        if ring[lo] < ring[mid]:\n            if ring[lo] <= seq < ring[mid]: hi = mid - 1\n            else: lo = mid + 1\n        else:\n            if ring[mid] < seq <= ring[hi]: lo = mid + 1\n            else: hi = mid - 1\n    return -1\n')
m('homework-3#8', 'linear index', 'test-13', 'def find_trade(ring, seq):\n    for i in range(len(ring)):\n        if ring[i] == seq: return i\n    return -1\n')

# added after the earlier reads were opened: submissions that do reach the two lines
m('l12#2', 'empty lists returned first, tail of a dropped', 'test-6', 'def merge(a, b):\n    if not a: return list(b)\n    if not b: return list(a)\n    out = []; i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    out.extend(b[j:])\n    return out\n')
m('l10#3', 'pred(a) before the range check', 'test-9', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi + 1\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a if pred(a) and a <= hi else None\n')

# Fix pass (round 3), l6 screens[3] and [7]: with the limit raised, plain recursion runs in Python 3.12 and later (and in Pyodide 0.27.7,
# run under node: sum_to 20,000,000 deep; a generator inside max overflows the stack between 700 and 900 levels at any limit; audit fix pass)
def _sum_to(n): return 0 if n == 0 else n + _sum_to(n - 1)
def _walk(node):
    d = 0
    for c in node["children"]: d = max(d, _walk(c))
    return 1 + d
_old = sys.getrecursionlimit(); sys.setrecursionlimit(10**9)
_chain = {"children": []}
for _ in range(49999): _chain = {"children": [_chain]}
check('l6 raised limit: sum_to(5000) and a plain 50,000-level walk run (Python 3.12+)', sys.version_info < (3, 12) or (_sum_to(5000) == 12502500 and _walk(_chain) == 50000))
sys.setrecursionlimit(_old)
# Fix pass (round 3): submissions for the new and reworded lines, each with the key it first reaches
m('l5#5', 'power with no base case (RecursionError)', 'test-6', SL + 'def power(x, n):\n    return x * power(x, n - 1)\n')
m('l5#5', 'power never reduces n (RecursionError)', 'test-6', SL + 'def power(x, n):\n    if n == 0: return 1\n    return x * power(x, n)\n')
m('l7#5', 'syntax error (load)', 'error', 'def max_rec(xs, lo, hi)\n    return xs[lo]\n' + PF)
m('l10#3', 'end marker hi, bare return (returns 100)', 'test-4', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a\n')
m('l10#3', 'returns -1 for none', 'test-4', 'def smallest_true(lo, hi, pred):\n    a, b = lo, hi + 1\n    while a < b:\n        mid = (a + b) // 2\n        if pred(mid): b = mid\n        else: a = mid + 1\n    return a if a <= hi else -1\n')
m('l10#4', 'syntax error (load)', 'error', ST + 'def isqrt(n)\n    return 0\n')
m('l12#3', 'base case len == 1 misses the empty list (RecursionError)', 'test-2', MG + 'def merge_sort(xs):\n    if len(xs) == 1: return list(xs)\n    mid = len(xs) // 2\n    return merge(merge_sort(xs[:mid]), merge_sort(xs[mid:]))\n')
m('l12#3', 'syntax error (load)', 'error', MG + 'def merge_sort(xs)\n    return xs\n')
m('l9#3', 'two reads a pass (within the cap)', 'none', 'def binary_search(xs, target):\n    lo, hi = 0, len(xs) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if xs[mid] == target: return mid\n        elif xs[mid] < target: lo = mid + 1\n        else: hi = mid - 1\n    return -1\n')
# ------------------------------------------------------------------ Part B: code widgets and feedback.byKey submissions
import glob
def _same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)
def first_fail(w, code, skip_from=None):
    """The page's routing: 'error' only when the code fails to load; an exception inside a test is that test's failure."""
    sys.setrecursionlimit(3000)
    g = {'__name__': '__main__', '__learner_source__': code}
    try:
        if w.get('prelude'): exec(w['prelude'], g)
        exec(compile(code, 'solution.py', 'exec'), g)
        if w.get('postlude'): exec(w['postlude'], g)
    except BaseException:
        return 'error'
    for i, t in enumerate(w['tests'], 1):
        if skip_from and i >= skip_from: return 'slow-test-%d' % i
        try:
            if t.get('setup'): exec(t['setup'], g)
            a = eval(t['call'], g); e = eval(t['expect'], g)
            ok = math.isclose(a, e, rel_tol=1e-9, abs_tol=1e-12) if t.get('compare') == 'isclose' and not isinstance(a, (list, tuple, type(None))) else _same(a, e)
        except BaseException:
            ok = False
        if not ok: return 'test-%d' % i
    return 'none'
W = {}
for fpath in sorted(glob.glob(os.path.join(ROOT, '*.json'))):
    b = os.path.basename(fpath)[:-5]
    if b == 'course': continue
    d = json.load(open(fpath))
    for i, s in enumerate(d.get('screens') or d.get('items') or []):
        w = s.get('widget') or {}
        if w.get('kind') == 'code': W['%s#%d' % (b.split('-')[0] if b[0] == 'l' else b, i)] = w
check('41 code widgets', len(W) == 41, len(W))
for k, w in W.items():
    check(k + ' solution passes', first_fail(w, w['solution']) == 'none')
    check(k + ' starter fails', first_fail(w, w['starter']) != 'none')
    check(k + ' how states the number of tests', ('%d hidden tests' % len(w['tests'])) in w.get('how', ''), len(w['tests']))

# (widget, mistake the byKey line names or implies, key the line sits under, submission, first test too slow to run here)
SLOW = {'power_fast called twice': 10, 'recursive count': 6, 'naive fib': 10, 'out = out + [x]': 9, 'every pair': 9, 'pair loop': 8, 'pair by pair': 7,
        'pair by pair, count only loop': 7, 'tries every capacity': 8, 'one growing result': 6, 'linear scan': 11, 'linear index': 13, 'recursive merge': 9}
EXPECT_OTHER = {'VALID: generator inside max': 'none', 'recursive one side, last pivot': 'none', 'whole tuples@l12#8': 'test-1', 'no sort at all': 'test-1'}
REACH = []
for key, name, expect, code in M:
    if expect == 'error' and 'load' not in name: name += ' [the error line explains this exception]'
    want = EXPECT_OTHER.get(name + '@' + key, EXPECT_OTHER.get(name, expect.split(' ')[0]))
    got = first_fail(W[key], code, SLOW.get(name.split(' [the error')[0]))
    if name.split(' [the error')[0] in SLOW: got = got.replace('slow-', '')       # reached the slow test with every earlier test passing
    REACH.append((key, name, want, got))
    check('%s: the submission "%s" is shown the %s line' % (key, name, want), got == want, 'the key shown is ' + got)

print('%d checks, %d failing' % (COUNT[0], len(FAILS)))
for f_ in FAILS: print('FAIL', f_)
print(INBOX_L9)
print('nested three order statistics, comparisons per value (nested, one median):', tuple(round(x, 2) for x in NESTED))
sys.exit(1 if FAILS else 0)
