import random, collections, json, math, itertools, bisect, subprocess, tempfile, functools
from harness import *
random.seed(41)
REP = {}; NUM = {}

# ---------- 4.1 best_plan ----------
BP_REF = '''
def best_plan(problems, budget):
    best = [0] * (budget + 1)               # best[m]: most points using at most m minutes
    for full_pts, full_min, part_pts, part_min in problems:
        new = best[:]
        for m in range(budget + 1):
            if m >= full_min:
                new[m] = max(new[m], best[m - full_min] + full_pts)
            if m >= part_min:
                new[m] = max(new[m], best[m - part_min] + part_pts)
        best = new
    return best[budget]
'''
BP_START = '''
def best_plan(problems, budget):
    return 0
'''
def bp_brute(problems, budget):
    best = 0
    for choice in itertools.product(range(3), repeat=len(problems)):
        pts = mins = 0
        for (fp, fm, pp, pm), c in zip(problems, choice):
            if c == 1: pts += fp; mins += fm
            elif c == 2: pts += pp; mins += pm
        if mins <= budget: best = max(best, pts)
    return best
def bp_memo(problems, budget):
    @functools.lru_cache(None)
    def go(i, left):
        if i == len(problems): return 0
        fp, fm, pp, pm = problems[i]
        r = go(i + 1, left)
        if left >= fm: r = max(r, fp + go(i + 1, left - fm))
        if left >= pm: r = max(r, pp + go(i + 1, left - pm))
        return r
    return go(0, budget)
ns = {}; exec(BP_REF, ns); bpref = ns['best_plan']
for _ in range(3000):
    n = random.randint(0, 6); pr = []
    for _ in range(n):
        fm = random.randint(5, 40); fp = random.randint(10, 100)
        pm = random.randint(2, fm); pp = random.randint(1, fp)
        pr.append([fp, fm, pp, pm])
    b = random.randint(0, 120)
    assert bpref(pr, b) == bp_brute(pr, b) == bp_memo(tuple(map(tuple, pr)), b), (pr, b)
A = [30, 15, 10, 5]; B = [50, 30, 20, 10]; C = [80, 45, 25, 15]
bps = [([A,B,C], 55), ([A,B,C], 60), ([A,B,C], 90), ([A,B,C], 0), ([A,B,C], 14), ([], 30), ([[40,20,10,20]], 20), ([[40,20,30,5]], 10), ([A,B,C,[20,10,5,3]], 45)]
BP_TESTS = [dict(call=f'best_plan({p}, {b})', expect=bp_brute(p, b)) for p, b in bps]
big = [[random.randint(10, 100), random.randint(5, 40), 0, 0] for _ in range(60)]
for g in big:
    g[3] = random.randint(2, g[1]); g[2] = random.randint(1, g[0])
BP_TESTS.append(dict(setup='import random; random.seed(1); ps = []\nfor _ in range(60):\n    fm = random.randint(5, 40); fp = random.randint(10, 100)\n    ps.append([fp, fm, random.randint(1, fp), random.randint(2, fm)])', call='best_plan(ps, 600)', expect=None))
random.seed(1); ps = []
for _ in range(60):
    fm = random.randint(5, 40); fp = random.randint(10, 100)
    ps.append([fp, fm, random.randint(1, fp), random.randint(2, fm)])
BP_TESTS[-1]['expect'] = bp_memo(tuple(map(tuple, ps)), 600); assert bpref(ps, 600) == BP_TESTS[-1]['expect']
check_py('best_plan', BP_REF, BP_START, BP_TESTS)
REP['bp'] = md_tests(BP_TESTS)
for p, b in bps[:5]: print('bp', b, bp_brute(p, b))
NUM['bp'] = {b: bp_brute([A,B,C], b) for b in (55, 60, 90, 0, 14)}
NUM['bp_options_3'] = 3**3

# ---------- 4.2 edge_cases against mutants ----------
LR_PRELUDE = '''
def _ref(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m1(xs):                      # forgets the last run
    best = run = 0
    for i, x in enumerate(xs):
        if i and x == xs[i - 1]:
            run += 1
        else:
            best = max(best, run)
            run = 1
    return best
def _m2(xs):                      # empty list gives 1
    best = run = 1
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m3(xs):                      # a single element gives 0
    if len(xs) == 1:
        return 0
    return _ref(xs)
def _m4(xs):                      # counts non-decreasing runs
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x >= xs[i - 1] else 1
        best = max(best, run)
    return best
def _m5(xs):                      # restarts the run at 0 after a break
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else (1 if i == 0 else 0)
        best = max(best, run)
    return best
def _m6(xs):                      # only compares with the first value
    best = run = 0
    for x in xs:
        run = run + 1 if x == xs[0] else 0
        best = max(best, run)
    return best
_MUTANTS = {'m1': _m1, 'm2': _m2, 'm3': _m3, 'm4': _m4, 'm5': _m5, 'm6': _m6}
def caught(name):
    try:
        cases = edge_cases()
    except Exception:
        return False
    return any(_MUTANTS[name](list(c)) != _ref(list(c)) for c in cases)
def well_formed():
    cases = edge_cases()
    return len(cases) <= 8 and all(isinstance(c, list) and all(isinstance(v, int) for v in c) for c in cases)
'''
EC_REF = '''
def edge_cases():
    return [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]
'''
EC_START = '''
def edge_cases():
    return []
'''
EC_TESTS = [dict(call=f"caught('m{i}')", expect=True) for i in range(1, 7)] + [dict(call='well_formed()', expect=True)]
# which mutants does each input catch
ns = {}; exec(LR_PRELUDE, ns)
inputs = [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2], [1, 1], [2, 1], [1, 2, 2], [5, 5, 5, 1]]
cov = {tuple(x): [m for m, f in ns['_MUTANTS'].items() if f(list(x)) != ns['_ref'](list(x))] for x in inputs}
for k, v in cov.items(): print('cover', k, v)
# brute check of reference
def lr_brute(xs):
    return max([j - i for i in range(len(xs)) for j in range(i + 1, len(xs) + 1) if len(set(xs[i:j])) == 1] + [0])
for _ in range(2000):
    xs = [random.randint(0, 2) for _ in range(random.randint(0, 8))]
    assert ns['_ref'](xs) == lr_brute(xs)
# the model set catches all six; each mutant is caught by at least one input
check_py('edge_cases (mutants)', EC_REF, EC_START, EC_TESTS, prelude=LR_PRELUDE)
REP['ec'] = md_tests(EC_TESTS)
NUM['ec_cover'] = {str(k): v for k, v in cov.items()}
# minimal set size: smallest subset of inputs catching all mutants (search)
allm = set(ns['_MUTANTS'])
best = None
for r in range(1, 7):
    for sub in itertools.combinations(inputs, r):
        if set().union(*[set(cov[tuple(x)]) for x in sub]) == allm:
            best = sub; break
    if best: break
print('minimal covering set size', len(best), best)
NUM['ec_min'] = (len(best), best)

# C++ testkit emulation and the C++ variant
KIT = r'''
#include <vector>
#include <functional>
#include <string>
#include <cstdio>
struct ZqTest { const char* name; void (*fn)(); };
inline std::vector<ZqTest>& zq_tests() { static std::vector<ZqTest> v; return v; }
inline int& zq_fail() { static int f = 0; return f; }
struct ZqReg { ZqReg(const char* n, void (*f)()) { zq_tests().push_back({n, f}); } };
#define TEST(name) static void zqt_##name(); static ZqReg zqr_##name(#name, zqt_##name); static void zqt_##name()
#define CHECK(cond) do { if (!(cond)) { zq_fail()++; } } while (0)
inline int run_tests() { int bad = 0; for (auto& t : zq_tests()) { int before = zq_fail(); t.fn(); if (zq_fail() > before) ++bad; } return bad; }
'''
CPP_PRELUDE = KIT + '''
int longest_streak(const std::vector<int>& xs);
'''
CPP_POST = '''
int longest_streak(const std::vector<int>& xs) {
    int best = 0, run = 0;
#ifdef BUG1
    for (size_t i = 0; i < xs.size(); ++i) {
        if (i && xs[i] == xs[i - 1]) ++run;
        else { best = std::max(best, run); run = 1; }
    }
    return best;
#elif defined(BUG2)
    best = 1;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG3)
    if (xs.size() == 1) return 0;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG4)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] >= xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG5)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : (i == 0 ? 1 : 0);
        best = std::max(best, run);
    }
    return best;
#else
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#endif
}
'''
CPP_LEARNER_SOL = '''#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_streak({}) == 0); }
TEST(single) { CHECK(longest_streak({7}) == 1); }
TEST(rising) { CHECK(longest_streak({1, 2}) == 1); }
TEST(run_after_break) { CHECK(longest_streak({3, 1, 1}) == 2); }
TEST(whole_list) { CHECK(longest_streak({2, 2, 2}) == 3); }
TEST(two_runs) { CHECK(longest_streak({1, 1, 2, 2, 2}) == 3); }
'''
CPP_LEARNER_START = '''#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_streak({}) == 0); }
'''
def cpp_variant(learner, define=None):
    d = tempfile.mkdtemp(dir='build')
    prog = '#include <vector>\n#include <algorithm>\n' + CPP_PRELUDE + learner + CPP_POST + '\n#include <iostream>\nint main(){ std::cout << run_tests() << "\\n"; }\n'
    open(d + '/m.cpp', 'w').write(prog)
    cmd = ['g++', '-std=c++20', '-O1', '-fno-exceptions'] + ([f'-D{define}=1'] if define else []) + ['-o', d + '/a', d + '/m.cpp']
    subprocess.run(cmd, check=True, capture_output=True)
    return int(subprocess.run([d + '/a'], capture_output=True, text=True).stdout)
assert cpp_variant(CPP_LEARNER_SOL) == 0
for b in range(1, 6):
    assert cpp_variant(CPP_LEARNER_SOL, f'BUG{b}') > 0, b
print('cpp edge cases: correct version passes, BUG1..BUG5 each caught by the model tests')
assert cpp_variant(CPP_LEARNER_START) == 0
caught_by_start = [b for b in range(1, 6) if cpp_variant(CPP_LEARNER_START, f'BUG{b}') > 0]
print('cpp starter catches', caught_by_start)
assert len(caught_by_start) < 5     # the starter (one test) fails the "catch every bug" cases
NUM['cpp_starter_catches'] = caught_by_start

# ---------- 4.3 two in sixty ----------
CS_REF = '''
def count_subarrays_sum_k(nums, k):
    seen = {0: 1}
    total = count = 0
    for x in nums:
        total += x
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
'''
CS_START = '''
def count_subarrays_sum_k(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count
'''
def cs_brute(nums, k):
    pre = [0]
    for x in nums: pre.append(pre[-1] + x)
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if pre[j] - pre[i] == k)
ns = {}; exec(CS_REF, ns); csref = ns['count_subarrays_sum_k']
for _ in range(3000):
    nums = [random.randint(-3, 5) for _ in range(random.randint(0, 12))]; k = random.randint(-3, 8)
    assert csref(nums, k) == cs_brute(nums, k)
css = [([1,1,1],2),([1,2,3],3),([],0),([0,0,0],0),([1,-1,0],0),([3,4,7,2,-3,1,4,2],7),([5],5),([5],-5),([-1,-1,1],0)]
CS_TESTS = [dict(call=f'count_subarrays_sum_k({n}, {k})', expect=cs_brute(n, k)) for n, k in css]
CS_TESTS.append(dict(setup='xs = [0] * 100000', call='count_subarrays_sum_k(xs, 0)', expect=100000 * 100001 // 2))
CS_TESTS.append(dict(setup='ys = [1, -1] * 50000', call='count_subarrays_sum_k(ys, 0)', expect=None))
ys = [1, -1] * 50000
# closed form: prefix sums alternate 1,0,1,0,...; subarrays summing to 0 are even-length: for n=100000 count = sum over even lengths L of (n-L+1)
n = 100000; cf = sum(n - L + 1 for L in range(2, n + 1, 2))
assert csref(ys, 0) == cf == cs_brute(ys[:2000], 0) * 0 + cf
assert csref([1, -1] * 500, 0) == cs_brute([1, -1] * 500, 0)
CS_TESTS[-1]['expect'] = cf
check_py('count_subarrays_sum_k', CS_REF, CS_START, CS_TESTS)
REP['cs'] = md_tests(CS_TESTS)
# the starter passes the first nine small cases and fails on time at the big one: confirm
r = run_py(CS_START, CS_TESTS[:9])
assert all(ok for ok, _ in r)
print('brute-force starter passes the 9 small cases (partial credit), fails by time on the 10th')
# time the quadratic on n = 100000 zero list in python estimate
import time
t0 = time.time(); CSn = [0] * 3000
ns2 = {}; exec(CS_START, ns2); ns2['count_subarrays_sum_k'](CSn, 0); t3 = time.time() - t0
print('quadratic 3000 elements seconds', round(t3, 3), '-> 100000 elements about', round(t3 * (100000 / 3000) ** 2), 's')
CS_CPP_REF = '''#include <vector>
#include <unordered_map>
long long count_subarrays_sum_k(std::vector<int> nums, long long k) {
    std::unordered_map<long long, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total += x;
        auto it = seen.find(total - k);
        if (it != seen.end()) count += it->second;
        ++seen[total];
    }
    return count;
}
'''
CS_CPP_START = '''#include <vector>
#include <unordered_map>
long long count_subarrays_sum_k(std::vector<int> nums, long long k) {
    long long count = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total == k) ++count;
        }
    }
    return count;
}
'''
calls = [(f'count_subarrays_sum_k(std::vector<int>{cpp_lit(n)}, {k})', cs_brute(n, k)) for n, k in css]
calls.append(('count_subarrays_sum_k(std::vector<int>(200000, 0), 0)', 200000 * 200001 // 2))
# the C++ quadratic starter would also pass the correctness cases; its failure is by time (5 s budget). Cannot show with correctness; verify timing
import os
d = tempfile.mkdtemp(dir='build')
open(d + '/m.cpp', 'w').write(CS_CPP_START + '\n#include <iostream>\nint main(){ std::cout << count_subarrays_sum_k(std::vector<int>(200000, 0), 0) << "\\n"; }\n')
subprocess.run(['g++', '-std=c++20', '-O1', '-fno-exceptions', '-o', d + '/a', d + '/m.cpp'], check=True)
t0 = time.time(); out = subprocess.run([d + '/a'], capture_output=True, text=True).stdout; tq = time.time() - t0
print('C++ quadratic on n=200000 natively', round(tq, 2), 's (wasm -O1 is slower, about 1.5 to 3 times)')
# honest check: reference passes all and the quadratic starter only fails on time, so use a bigger n for the failing case
CS_CPP_STARTER_FAIL_NOTE = tq
NUM['cs_cpp_quad_native_s'] = round(tq, 2)

LC_REF = '''
def longest_consecutive(nums):
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 not in present:
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
    return best
'''
LC_START = '''
def longest_consecutive(nums):
    best = 0
    for x in nums:
        length = 1
        while x + length in nums:
            length += 1
        best = max(best, length)
    return best
'''
def lc_brute(nums):
    s = sorted(set(nums)); best = 0; run = 0
    for i, v in enumerate(s):
        run = run + 1 if i and v == s[i-1] + 1 else 1
        best = max(best, run)
    return best
ns = {}; exec(LC_REF, ns); lcref = ns['longest_consecutive']
for _ in range(3000):
    nums = [random.randint(-6, 12) for _ in range(random.randint(0, 12))]
    assert lcref(nums) == lc_brute(nums)
lcs = [[100,4,200,1,3,2],[0,3,7,2,5,8,4,6,0,1],[],[5],[1,2,0,1],[9,1,4,7,3,-1,0,5,8,-1,6],[1,1,1],[-2,-1,0,1]]
LC_TESTS = [dict(call=f'longest_consecutive({n})', expect=lc_brute(n)) for n in lcs]
LC_TESTS.append(dict(setup='import random; random.seed(2); xs = list(range(200000)); random.shuffle(xs)', call='longest_consecutive(xs)', expect=200000))
LC_TESTS.append(dict(setup='ys = list(range(0, 400000, 2))', call='longest_consecutive(ys)', expect=1))
check_py('longest_consecutive', LC_REF, LC_START, LC_TESTS)
REP['lc'] = md_tests(LC_TESTS)
r = run_py(LC_START, LC_TESTS[:8]); print('lc starter (list membership) passes small:', [ok for ok, _ in r])

# ---------- 4.4 product_except_self ----------
PE_REF = '''
def product_except_self(nums):
    # plan: out[i] = (product of everything left of i) * (product of everything right of i)
    # pass 1 fills out[i] with the left product, pass 2 multiplies in the right product
    # no division, so zeros are safe; two passes, O(n) time and O(1) extra space
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
'''
PE_START = '''
def product_except_self(nums):
    # plan: write two or three comment lines here before the code
    return [0] * len(nums)
'''
def pe_brute(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j, v in enumerate(nums):
            if j != i: p *= v
        out.append(p)
    return out
ns = {}; exec(PE_REF, ns); peref = ns['product_except_self']
for _ in range(2000):
    nums = [random.randint(-3, 4) for _ in range(random.randint(1, 8))]
    assert peref(nums) == pe_brute(nums)
pes = [[2,3,5,7],[3,-2,0,4,-1],[2,0,0],[0,5],[7,3],[1,1,1],[5,-2]]
PE_TESTS = [dict(call=f'product_except_self({n})', expect=pe_brute(n)) for n in pes]
nn = 100000
PE_TESTS.append(dict(setup='xs = [1] * 100000; xs[10] = 2; xs[500] = 3', call='sum(product_except_self(xs))', expect=6 * (nn - 2) + 5))
xs = [1] * nn; xs[10] = 2; xs[500] = 3
assert sum(peref(xs)) == 6 * (nn - 2) + 5
assert sum(pe_brute(xs[:50]))  # brute sanity on small prefix
x_small = [1] * 50; x_small[10] = 2; x_small[20] = 3
assert sum(pe_brute(x_small)) == 6 * 48 + 5 == sum(peref(x_small))
PE_TESTS.append(dict(call="all('/' not in line.split('#')[0] for line in __learner_source__.splitlines())", expect=True))
PE_TESTS.append(dict(call="sum(1 for l in __learner_source__.splitlines() if l.strip().startswith('#')) >= 3", expect=True))
r = run_py(PE_REF, PE_TESTS); assert all(ok for ok, _ in r), r
check_py('product_except_self', PE_REF, PE_START, PE_TESTS)
REP['pe'] = md_tests(PE_TESTS, width=None)

# ---------- 4.5 calendar ----------
CAL_A = '''
import bisect

class Calendar:
    def __init__(self):
        self.starts, self.ends = [], []       # sorted by start; bookings never overlap

    def book(self, start, end):
        i = bisect.bisect_left(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:
            return False
        if i < len(self.starts) and self.starts[i] < end:
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True
'''
CAL_REF = '''
class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def _fits(self, start, end):
        points = [start] + [s for s, e in self.bookings if start < s < end]
        for p in points:
            if sum(1 for s, e in self.bookings if s <= p < e) + 1 > self.k:
                return False
        return True

    def book(self, start, end):
        if not self._fits(start, end):
            return False
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        if (start, end) in self.bookings:
            self.bookings.remove((start, end))
            return True
        return False

    def next_free(self, duration, after):
        for t in sorted({after} | {e for s, e in self.bookings if e > after}):
            if self._fits(t, t + duration):
                return t
'''
CAL_START = '''
class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def book(self, start, end):
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        return False

    def next_free(self, duration, after):
        return after
'''
CAL_POST = '''
def run_cal(k, ops):
    c = Calendar(k)
    out = []
    for op in ops:
        if op[0] == 0: out.append(c.book(op[1], op[2]))
        elif op[0] == 1: out.append(c.cancel(op[1], op[2]))
        else: out.append(c.next_free(op[1], op[2]))
    return out
'''
def cal_brute(k, ops, horizon=80):
    bk, out = [], []
    def fits(s, e):
        for t in range(s, e):
            if sum(1 for a, b in bk if a <= t < b) + 1 > k: return False
        return True
    for op in ops:
        if op[0] == 0:
            if fits(op[1], op[2]): bk.append((op[1], op[2])); out.append(True)
            else: out.append(False)
        elif op[0] == 1:
            if (op[1], op[2]) in bk: bk.remove((op[1], op[2])); out.append(True)
            else: out.append(False)
        else:
            t = op[2]
            while not fits(t, t + op[1]): t += 1
            out.append(t)
    return out
ns = {}; exec(CAL_REF + CAL_POST, ns); runcal = ns['run_cal']
nsA = {}; exec(CAL_A + '''
def run_a(ops):
    c = Calendar()
    return [c.book(s, e) for s, e in ops]
''', nsA)
def rand_cal_ops(n, with_extra=True):
    ops = []
    for _ in range(n):
        r = random.random(); s = random.randint(0, 25)
        if r < 0.6 or not with_extra: ops.append([0, s, s + random.randint(1, 6)])
        elif r < 0.8: ops.append([1, s, s + random.randint(1, 6)])
        else: ops.append([2, random.randint(1, 5), s])
    return ops
for _ in range(3000):
    k = random.randint(1, 3); ops = rand_cal_ops(random.randint(0, 14))
    assert runcal(k, ops) == cal_brute(k, ops), (k, ops)
for _ in range(2000):
    ops = rand_cal_ops(random.randint(0, 14), False)
    assert nsA['run_a']([[o[1], o[2]] for o in ops]) == cal_brute(1, ops)
# stage tests
cA = [[[10,20],[15,25],[20,30]], [[0,5],[5,10],[3,6],[10,11],[4,5]], [[5,10],[0,5],[10,15],[0,15]], [[1,2]], []]
CAL_T1 = [dict(call=f'run_cal(1, {[[0, s, e] for s, e in c]})', expect=cal_brute(1, [[0, s, e] for s, e in c])) for c in cA]
CAL_T1.append(dict(setup='ops = [[0, 2 * i, 2 * i + 1] for i in range(60000)] + [[0, 0, 120000]]', call='run_cal(1, ops).count(True)', expect=60000))
cB = [(2,[[0,10,20],[0,15,25],[0,20,30],[0,12,18]]), (2,[[0,10,20],[0,15,25],[0,5,15],[0,5,11]]), (3,[[0,1,5],[0,2,5],[0,3,5],[0,4,5],[0,0,2]]), (1,[[0,1,3],[0,3,5]]), (2,[[0,0,10],[0,0,10],[0,10,20],[0,5,15]])]
CAL_T2 = list(CAL_T1[:3]) + [dict(call=f'run_cal({k}, {o})', expect=cal_brute(k, o)) for k, o in cB]
cC = [(1,[[0,10,20],[1,10,20],[0,15,25],[1,15,26],[1,15,25],[0,10,12]]), (1,[[0,10,20],[0,30,40],[2,5,0],[2,10,5],[2,10,12],[2,10,35],[2,11,10]]), (2,[[0,0,10],[0,0,10],[2,5,0],[1,0,10],[2,5,0],[2,12,3]]), (1,[[2,5,7]]), (1,[[0,0,3],[0,3,6],[0,9,12],[2,3,0],[2,4,0],[1,3,6],[2,4,0]])]
CAL_T3 = list(CAL_T2) + [dict(call=f'run_cal({k}, {o})', expect=cal_brute(k, o)) for k, o in cC]
check_py('Calendar stage A (bisect, book only)', CAL_A + '''
class _X: pass
''', CAL_START, CAL_T1, postlude=CAL_POST.replace('c = Calendar(k)', 'c = Calendar()'))
_slow = run_py(CAL_REF, CAL_T1, postlude=CAL_POST)
print('stage A, linear-scan reference as a slow starter:', [ok for ok, _ in _slow], _slow[-1][1])
assert all(ok for ok, _ in _slow[:5]) and not _slow[5][0] and 'timeout' in str(_slow[5][1])
check_py('Calendar stage B (k)', CAL_REF, CAL_START, CAL_T2, postlude=CAL_POST)
check_py('Calendar stage C (cancel, next_free)', CAL_REF, CAL_START, CAL_T3, postlude=CAL_POST)
REP['cal1'] = md_tests(CAL_T1)
REP['cal2'] = md_tests(CAL_T2[3:]); REP['cal3'] = md_tests(CAL_T3[len(CAL_T2):])
print('stage counts: A', len(CAL_T1), 'B', len(CAL_T2), 'C', len(CAL_T3))
for nm, ts in (('A', CAL_T1), ('B', CAL_T2), ('C', CAL_T3)):
    _r = run_py(CAL_START, ts, postlude=CAL_POST if nm != 'A' else CAL_POST.replace('c = Calendar(k)', 'c = Calendar()'))
    print('starter fails stage', nm, sum(1 for ok, _ in _r if not ok), 'of', len(ts))
for k, o in cB: print('calB', cal_brute(k, o))
for k, o in cC: print('calC', cal_brute(k, o))

# ---------- HW4: Leaderboard (parts), top_k_frequent (C++) ----------
LB1_REF = '''
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])
'''
LB1_START = '''
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return 0
'''
LB_POST = '''
def run_board(ops):
    b = Leaderboard()
    out = []
    for op in ops:
        if op[0] == 0: b.add_score(op[1], op[2])
        elif op[0] == 1: out.append(b.top(op[1]))
        else: b.reset(op[1])
    return out
'''
LB2_REF = LB1_REF + '''
    def reset(self, player):
        self.scores.pop(player, None)
'''
LB2_START = LB1_START + '''
    def reset(self, player):
        pass
'''
def lb_brute(ops):
    sc, out = collections.Counter(), []
    for op in ops:
        if op[0] == 0: sc[op[1]] += op[2]
        elif op[0] == 1: out.append(sum(sorted([v for v in sc.values()], reverse=True)[:op[1]]))
        else: sc.pop(op[1], None)
    return out
ns = {}; exec(LB2_REF + LB_POST, ns); runlb = ns['run_board']
for _ in range(2000):
    ops = []
    for _ in range(random.randint(0, 15)):
        r = random.random()
        ops.append([0, random.randint(1, 4), random.randint(1, 9)] if r < 0.5 else ([1, random.randint(1, 5)] if r < 0.8 else [2, random.randint(1, 4)]))
    assert runlb(ops) == lb_brute(ops)
lbs = [[[0,1,73],[0,2,56],[0,3,39],[0,4,51],[0,5,4],[1,1],[2,1],[2,2],[0,2,51],[1,2]],
       [[0,1,5],[0,1,7],[1,1],[1,3]],
       [[1,2]],
       [[0,1,10],[0,2,20],[0,3,30],[1,2],[2,3],[1,2],[1,5]]]
LB1_TESTS = [dict(call=f'run_board({[o for o in ops if o[0] != 2]})', expect=lb_brute([o for o in ops if o[0] != 2])) for ops in lbs]
LB2_TESTS = [dict(call=f'run_board({ops})', expect=lb_brute(ops)) for ops in lbs]
check_py('Leaderboard part 1', LB1_REF, LB1_START, LB1_TESTS, postlude=LB_POST)
check_py('Leaderboard part 3 (reset)', LB2_REF, LB2_START, LB2_TESTS, postlude=LB_POST)
REP['lb1'] = md_tests(LB1_TESTS); REP['lb2'] = md_tests(LB2_TESTS)
print('lb', [lb_brute(o) for o in lbs])
# part 2: costs with concrete numbers: n = 100000 players, 2000 top queries at k = 10
NUM['lb_sort_work'] = 100000 * 2000      # score values sorted per query: n values, 2000 queries: 2e8 element visits (before the log factor)
NUM['lb_heap_work'] = 100000 * 2000      # heap of size k also visits every player: n per query; the same count of visits, log k per visit
NUM['lb_maintained_top_k_work'] = 2000 * 10

TKF_REF = '''#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k) {
    std::unordered_map<std::string, int> count;
    for (const auto& w : words) ++count[w];
    auto worse = [](const std::pair<int, std::string>& a, const std::pair<int, std::string>& b) {
        if (a.first != b.first) return a.first > b.first;
        return a.second < b.second;
    };
    std::priority_queue<std::pair<int, std::string>, std::vector<std::pair<int, std::string>>, decltype(worse)> heap(worse);
    for (const auto& kv : count) {
        heap.push({kv.second, kv.first});
        if ((int)heap.size() > k) heap.pop();
    }
    std::vector<std::string> out(heap.size());
    for (int i = (int)out.size() - 1; i >= 0; --i) {
        out[i] = heap.top().second;
        heap.pop();
    }
    return out;
}
'''
TKF_START = '''#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k) {
    std::unordered_map<std::string, int> count;
    for (const auto& w : words) ++count[w];
    std::vector<std::string> out;
    for (const auto& kv : count) out.push_back(kv.first);
    if ((int)out.size() > k) out.resize(k);
    return out;
}
'''
def tkf_brute(words, k):
    c = collections.Counter(words)
    return [w for w, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))][:k]
tkfs = [(["bid","ask","mid","bid","ask","bid"],2),(["last","mid","bid","mid","last","mid","last","bid","ask","mid"],4),(["a"],1),(["b","a"],5),(["x","y","x","y","z"],2),(["q","q"],0)]
calls = [(f'top_k_frequent(std::vector<std::string>{cpp_lit(w)}, {k})', tkf_brute(w, k)) for w, k in tkfs]
big_words = [f'w{i % 1000:04d}' for i in range(50000)]
calls.append(('[&]{ std::vector<std::string> ws; for (int i = 0; i < 50000; ++i) { char b[16]; std::snprintf(b, sizeof b, "w%04d", i % 1000); ws.push_back(b); } return top_k_frequent(ws, 3); }()', tkf_brute(big_words, 3)))
# includes cstdio for snprintf
check_cpp('top_k_frequent_cpp', TKF_REF.replace('#include <vector>', '#include <vector>\n#include <cstdio>', 1), TKF_START.replace('#include <vector>', '#include <vector>\n#include <cstdio>', 1), calls)
tk_tests = [dict(call=f'top_k_frequent({w}, {k})', expect=tkf_brute(w, k)) for w, k in tkfs]
REP['tkf'] = md_tests(tk_tests)

# numbers for review
NUM['rate'] = {}
# reading assessment: points per minute
probs = {'A': (30, 15), 'B': (50, 30), 'C': (80, 45)}
NUM['ppm'] = {k: round(p / m, 3) for k, (p, m) in probs.items()}
NUM['ppm_check'] = {k: p * 1.0 / m for k, (p, m) in probs.items()}
# 60-minute budget: 5 minutes reading
NUM['budget_after_reading'] = 60 - 5
# two in sixty: split 25 + 25 + 10 review
json.dump(NUM, open('l4_numbers.json', 'w'), default=str)
json.dump(REP, open('l4_tests.json', 'w'))
for k, v in NUM.items(): print(k, v)
