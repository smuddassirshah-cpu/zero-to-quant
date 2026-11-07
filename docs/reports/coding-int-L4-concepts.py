#!/usr/bin/env python3
"""Concept checks for coding-int level 4 (l15 to l19, review-4, homework-4).

Run from the repo root:  python3 -I docs/reports/coding-int-L4-concepts.py
Every assert names its ledger row (docs/reports/audit-coding-int-4-ledger.md).
Exit 0 means every check that the content gets right passes. A check marked
EXPECTED_FAIL fails because the content is wrong as stated; the corrected
assert sits beside it in a comment, ready to enable once the content is fixed.
Timing claims use operation counters, never wall-clock. C++ items are compiled
with g++ (-O1, no exceptions) using the engine's testkit macros copied from
app/js/engine/widgets/cpp-grade.js.
"""
import itertools, json, math, os, random, subprocess, sys, tempfile, bisect
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'coding-int')
FAILS = []
def check(cond, msg):
    if not cond:
        FAILS.append(msg); print('FAIL', msg)
def load(name):
    with open(os.path.join(COURSE, name)) as f:
        return json.load(f)
L15, L16, L17, L18, L19 = (load(n) for n in ['l15-reading-an-assessment.json', 'l16-edge-cases-first.json',
    'l17-two-in-sixty.json', 'l18-talking-while-coding.json', 'l19-a-live-round.json'])
R4, H4 = load('review-4.json'), load('homework-4.json')
def code_of(screen, part=None):
    w = screen['widget'] if part is None else screen['parts'][part]['widget']
    return w

# ---------------------------------------------------------------- l15: planning
def brute_plan(problems, budget):
    best = 0
    for ch in itertools.product(range(3), repeat=len(problems)):
        pts = mins = 0
        for (fp, fm, pp, pm), c in zip(problems, ch):
            if c == 1: pts += fp; mins += fm
            elif c == 2: pts += pp; mins += pm
        if mins <= budget: best = max(best, pts)
    return best

L15_PROBLEMS = [[40, 20, 12, 6], [60, 35, 25, 12], [90, 50, 30, 18]]
# screen 0: rates
rates = [fp / fm for fp, fm, _, _ in L15_PROBLEMS]
check(abs(rates[0] - 2.0) < 1e-12 and abs(rates[1] - 60 / 35) < 1e-12 and abs(rates[2] - 1.8) < 1e-12 and rates[0] == max(rates),
      'l15 screens[0] rates 2.0, 1.71, 1.8 and P1 best')
# screen 1: greedy full by rate with skip
def greedy_full(problems, budget):
    order = sorted(range(len(problems)), key=lambda i: -problems[i][0] / problems[i][1])
    pts = 0
    for i in order:
        if problems[i][1] <= budget: budget -= problems[i][1]; pts += problems[i][0]
    return pts
check(greedy_full(L15_PROBLEMS, 62) == 100, 'l15 screens[1] greedy by rate earns 100')
# screens 2 and 4: optimum 115 at 62, unique plan P3 full + P2 partial
check(brute_plan(L15_PROBLEMS, 62) == 115, 'l15 screens[2] optimum at 62 minutes is 115')
plans115 = [ch for ch in itertools.product(range(3), repeat=3)
            if sum((p[0] if c == 1 else p[2] if c == 2 else 0) for p, c in zip(L15_PROBLEMS, ch)) == 115
            and sum((p[1] if c == 1 else p[3] if c == 2 else 0) for p, c in zip(L15_PROBLEMS, ch)) <= 62]
check(plans115 == [(0, 2, 1)], 'l15 screens[2] the 115 plan is unique: P1 skip, P2 partial, P3 full')
check(abs(12 / 6 - 2.0) < 1e-12 and abs(25 / 12 - 2.083) < 1e-3, 'l15 screens[4] byKey d partial rates 2.0 and 2.08')
# screen 8: budget 58 -> 102; screen 9: bank problems -> 75
check(brute_plan(L15_PROBLEMS, 58) == 102, 'l15 screens[8] optimum at 58 minutes is 102')
check(greedy_full(L15_PROBLEMS, 58) == 100, 'l15 screens[8] greedy still earns 100 at 58')
plans102 = [ch for ch in itertools.product(range(3), repeat=3)
            if sum((p[0] if c == 1 else p[2] if c == 2 else 0) for p, c in zip(L15_PROBLEMS, ch)) == 102
            and sum((p[1] if c == 1 else p[3] if c == 2 else 0) for p, c in zip(L15_PROBLEMS, ch)) <= 58]
check(plans102 == [(2, 0, 1)], 'l15 screens[8] the 102 plan at 58 is unique: P1 partial, P2 skip, P3 full')
check(brute_plan([[50, 40, 20, 12], [60, 45, 25, 15]], 55) == 75, 'l15 screens[9] bank paper optimum 75')
check(3 ** 3 == 27, 'l15 screens[8] explain 27 choices for three problems')

# screen 3: the DP solution, run as written, against every test and a brute force
ns = {}
exec(L15['screens'][3]['widget']['solution'], ns)
best_plan = ns['best_plan']
for i, t in enumerate(L15['screens'][3]['widget']['tests']):
    loc = {'best_plan': best_plan}
    if 'setup' in t: exec(t['setup'], loc)
    got = eval(t['call'], loc)
    check(got == int(t['expect']), f'l15 screens[3] tests[{i}] solution gives {t["expect"]}')
    if 'setup' not in t:
        args = eval(t['call'][len('best_plan('):-1])
        check(brute_plan(*args) == int(t['expect']), f'l15 screens[3] tests[{i}] expect agrees with brute force')
ns_s = {}; exec(L15['screens'][3]['widget']['starter'], ns_s)
check(ns_s['best_plan'](L15_PROBLEMS, 62) == 0 != 115, 'l15 screens[3] starter fails test 1')
random.seed(7)
for _ in range(300):
    n = random.randint(0, 6); b = random.randint(0, 40)
    ps = [[random.randint(1, 50), random.randint(1, 20), random.randint(1, 50), random.randint(1, 20)] for _ in range(n)]
    check(best_plan(ps, b) == brute_plan(ps, b), 'l15 screens[3] DP equals brute force on random papers')
# operation counter: inner-loop iterations are exactly problems x (budget + 1)
def best_plan_counted(problems, budget):
    ops = 0
    best = [0] * (budget + 1)
    for full_pts, full_min, part_pts, part_min in problems:
        new = best[:]
        for m in range(budget + 1):
            ops += 1
            if m >= full_min: new[m] = max(new[m], best[m - full_min] + full_pts)
            if m >= part_min: new[m] = max(new[m], best[m - part_min] + part_pts)
        best = new
    return best[budget], ops
for n, b in [(3, 62), (10, 100), (60, 600)]:
    ps = [[random.randint(1, 50), random.randint(1, 20), random.randint(1, 50), random.randint(1, 20)] for _ in range(n)]
    check(best_plan_counted(ps, b)[1] == n * (b + 1), f'l15 screens[3] explain: work is problems x budget (n={n}, budget={b})')
    check(3 ** n > n * (b + 1) or n < 5, f'l15 screens[3] prose: 3^n exceeds n x budget for n={n}')
# screen 5 and quiz: step counts at the top of each group, 1e8 a second
check(1000 ** 2 == 10 ** 6 < 10 ** 8 and 100000 ** 2 == 10 ** 10 > 10 ** 8 and 10 ** 12 > 10 ** 8, 'l15 screens[5] quadratic step counts')
check(abs(10 ** 6 * math.log2(10 ** 6) - 2e7) < 1e5, 'l15 screens[5] n log n at 1e6 is about 2e7')
check(2000 ** 2 == 4 * 10 ** 6 and 300000 ** 2 == 9 * 10 ** 10, 'l15 quiz q-group step counts')
check(36 / 24 == 1.5 and 28 / 14 == 2.0, 'l15 quiz q-rate rates')
check(80 - 5 - 5 == 70, 'l15 quiz q-budget')

# ---------------------------------------------------------------- l16: mutants
pre = {}
exec(L16['screens'][2]['widget']['prelude'], pre)
ref, M = pre['_ref'], pre['_MUTANTS']
def catches(xs):
    return {m for m, f in M.items() if f(list(xs)) != ref(list(xs))}
# screen 0: m1 exposed by [2,2,2] and [3,1,1] only
m1 = M['m1']
for xs, bad in [([], False), ([1, 2], False), ([2, 2, 2], True), ([3, 1, 1], True), ([2, 1], False)]:
    check((m1(xs) != ref(xs)) == bad, f'l16 screens[0] m1 on {xs} exposed={bad}')
# screen 1: expected values
for xs, e in [([], 0), ([7], 1), ([1, 2], 1), ([3, 1, 1], 2), ([2, 2, 2], 3), ([1, 1, 2, 2, 2], 3)]:
    check(ref(xs) == e, f'l16 screens[1] longest_streak({xs}) = {e}')
# screen 2: solution list catches all six; hints name the right catches
sol = {}; exec(L16['screens'][2]['widget']['solution'], sol)
cases = sol['edge_cases']()
check(set().union(*(catches(c) for c in cases)) == set(M), 'l16 screens[2] solution exposes all six mutants')
check(len(cases) <= 8 and all(isinstance(c, list) for c in cases), 'l16 screens[2] well_formed')
check(catches([]) == {'m2'}, 'l16 screens[2] hint: [] catches m2 only')
check(catches([7]) == {'m1', 'm3'}, 'l16 screens[2] hint: [7] catches m1 and m3')
check(catches([1, 2]) == {'m4'}, 'l16 screens[2] hint: [1, 2] catches m4')
check(catches([3, 1, 1]) == {'m1', 'm5', 'm6'}, 'l16 screens[2] hint and screens[3]: [3, 1, 1] catches m1, m5, m6')
check(catches([1, 1, 2, 2, 2]) == {'m1', 'm4', 'm5', 'm6'}, 'l16 screens[2] hint: [1, 1, 2, 2, 2] catches four')
check(catches([2, 2, 2]) == {'m1'}, 'l16 screens[9] canvas: [2, 2, 2] catches m1 only')
st = {}; exec(L16['screens'][2]['widget']['starter'], st)
check(st['edge_cases']() == [], 'l16 screens[2] starter returns [] so caught() is False')
# screen 3: m2, m3, m4 return 2 on [3,1,1]; m1, m5, m6 return 1
check([M[m]([3, 1, 1]) for m in ['m1', 'm5', 'm6']] == [1, 1, 1] and [M[m]([3, 1, 1]) for m in ['m2', 'm3', 'm4']] == [2, 2, 2],
      'l16 screens[3] hints: m1, m5, m6 give 1; m2, m3, m4 give 2')
# screen 4: random lists of length 5..50 over 1..5 never catch m2; catch m4, m5, m6 often
random.seed(16)
hits = {m: 0 for m in M}; N = 20000
for _ in range(N):
    xs = [random.randint(1, 5) for _ in range(random.randint(5, 50))]
    for m in catches(xs): hits[m] += 1
check(hits['m2'] == 0, 'l16 screens[4] random lists never catch m2')
check(hits['m3'] == 0, 'l16 screens[4] random lists never catch m3 either (length 1 never made)')
check(hits['m4'] / N > 0.9 and hits['m5'] / N > 0.5 and hits['m6'] / N > 0.5 and hits['m1'] > 0,
      f'l16 screens[4] random lists expose m4, m5, m6 often: {dict((k, round(v / N, 3)) for k, v in hits.items())}')
# m2 differs from ref only on []: exhaustive over short lists
for n in range(1, 6):
    for xs in itertools.product(range(1, 4), repeat=n):
        check(M['m2'](list(xs)) == ref(list(xs)), 'l16 screens[4] step hint: m2 differs only on []')
# screens[4] options[2].why says m5 "shows on any run after a break": [1, 1, 2] has one and m5 is right there
# fix pass: the why now says m5 shows whenever a run after a break is longer than the first run.
# m5 counts every later run one short, so m5 = max(first run, later run - 1): [1, 1, 2] and [1, 1, 2, 2] give ref, [3, 1, 1] gives 1 not 2
_w5 = L16['screens'][4]['widget']['options'][2]['why']
check('run after a break is longer than the first run' in _w5
      and M['m5']([1, 1, 2]) == ref([1, 1, 2]) == 2 and M['m5']([1, 1, 2, 2]) == ref([1, 1, 2, 2]) == 2
      and M['m5']([3, 1, 1]) == 1 != ref([3, 1, 1]) == 2,
      'l16 screens[4] options[2].why: m5 shows whenever a run after a break is longer than the first run (corrected claim, fix pass)')
# corrected claim, ready to enable: m5 shows exactly when a run after a break is longer than the first run
def runs(xs):
    out = []
    for x in xs:
        if out and out[-1][0] == x: out[-1][1] += 1
        else: out.append([x, 1])
    return out
for n in range(0, 7):
    for xs in itertools.product(range(1, 4), repeat=n):
        r = runs(xs)
        exposed = bool(r) and max((ln for _, ln in r[1:]), default=0) > r[0][1]
        check((M['m5'](list(xs)) != ref(list(xs))) == exposed, 'l16 corrected: m5 exposed iff a later run is longer than the first run')
# screens[4] options[3].why says m6 "shows when the longest run does not start the list": [1, 2, 2, 1, 1] is a counter-example
# fix pass: the why now says m6 shows when a run of another value beats every run of the first value.
# m6 returns the longest run of xs[0]: [1, 2, 2, 1, 1] has no such run (2 ties 2) and m6 = ref = 2; [3, 1, 1] has one and m6 = 1 != 2
_w6 = L16['screens'][4]['widget']['options'][3]['why']
check('a run of another value beats every run of the first value' in _w6
      and M['m6']([1, 2, 2, 1, 1]) == ref([1, 2, 2, 1, 1]) == 2 and M['m6']([3, 1, 1]) == 1 != ref([3, 1, 1]),
      'l16 screens[4] options[3].why: m6 shows when a run of another value beats every run of the first value (corrected claim, fix pass)')
# corrected claim: m6 exposed iff the longest run overall beats every run of the first value
for n in range(0, 7):
    for xs in itertools.product(range(1, 4), repeat=n):
        r = runs(xs)
        exposed = bool(r) and max(ln for _, ln in r) > max(ln for v, ln in r if v == xs[0])
        check((M['m6'](list(xs)) != ref(list(xs))) == exposed, 'l16 corrected: m6 exposed iff the longest run beats every run of the first value')
# screen 9: set cover over the ten candidates has minimum 3
cands = [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2], [1, 1], [2, 1], [1, 2, 2], [6, 6, 6, 1]]
cover = {tuple(c): catches(c) for c in cands}
def min_cover():
    for k in range(1, len(cands) + 1):
        for sub in itertools.combinations(cands, k):
            if set().union(*(cover[tuple(c)] for c in sub)) == set(M): return k
check(min_cover() == 3, 'l16 screens[9] fewest inputs over the ten candidates is 3')
check(set().union(cover[()], cover[(7,)], cover[(1, 1, 2, 2, 2)]) == set(M), 'l16 screens[9] accept: [], [7], [1,1,2,2,2] cover all six')
# screen 6: edge families
def longest_run(s): return ref(list(s))
def blocks(spans):
    spans = sorted(spans); out = 0; end = None
    for a, b in spans:
        if end is None or a > end: out += 1; end = b
        else: end = max(end, b)
    return out
def digits(n): return len(str(abs(n)))
check(longest_run('') == 0 and longest_run('zzz') == 3 and blocks([[1, 2], [2, 3]]) == 1 and blocks([[1, 9], [3, 4]]) == 1
      and digits(0) == 1 and digits(-45) == 2, 'l16 screens[6] table values 0, 3, 1, 1, 1, 2')
# quiz q-expose: first-run-only mutant
def first_run_only(xs):
    r = runs(xs); return r[0][1] if r else 0
check(first_run_only([1, 4, 4]) == 1 != ref([1, 4, 4]) == 2 and all(first_run_only(x) == ref(x) for x in [[4, 4, 1], [5, 5, 5], [7]]),
      'l16 quiz q-expose only [1, 4, 4] exposes first-run-only')
check(ref([8, 8, 3, 8, 8, 8]) == 3, 'l16 quiz q-expected')

# ---------------------------------------------------------------- C++ helpers
TESTKIT = r'''#include <cstdio>
#include <vector>
namespace zq_tk {
struct T { const char* name; void (*fn)(); };
inline std::vector<T>& all() { static std::vector<T> v; return v; }
inline int& fails() { static int f = 0; return f; }
inline const char*& cur() { static const char* c = ""; return c; }
struct Reg { Reg(const char* n, void (*f)()) { all().push_back({ n, f }); } };
}
#define TEST(name) static void name(); static zq_tk::Reg zq_reg_##name(#name, name); static void name()
#define CHECK(cond) do { if (!(cond)) { ++zq_tk::fails(); std::printf("FAILED %s: CHECK(%s), line %d\n", zq_tk::cur(), #cond, __LINE__); } } while (0)
inline int run_tests() { int bad = 0; for (auto& t : zq_tk::all()) { int before = zq_tk::fails(); zq_tk::cur() = t.name; t.fn(); if (zq_tk::fails() > before) ++bad; } return bad; }
'''
TMP = tempfile.mkdtemp(prefix='ci4-')
def cpp_run(src, tag):
    path = os.path.join(TMP, tag + '.cpp'); exe = os.path.join(TMP, tag)
    with open(path, 'w') as f: f.write(src)
    r = subprocess.run(['g++', '-std=c++20', '-O1', '-fno-exceptions', path, '-o', exe], capture_output=True, text=True)
    if r.returncode: return None, r.stderr[:800]
    r = subprocess.run([exe], capture_output=True, text=True, timeout=120)
    return r.stdout.strip(), r.stderr
def cpp_main(body): return '#include <iostream>\n#include <vector>\nint main() {' + body + ' return 0; }\n'

# l16 screen 5: testkit item, solution and starter against each BUG define
w = L16['screens'][5]['widget']
def testkit_src(defs, learner):
    return TESTKIT + ''.join(f'#define {k} {v}\n' for k, v in defs.items()) + w['prelude'] + learner + w['postlude'] + \
        '#include <cstdio>\nint main() { std::printf("%d\\n", run_tests()); return 0; }\n'
for i, t in enumerate(w['tests']):
    defs = t.get('defines', {})
    out, err = cpp_run(testkit_src(defs, w['solution']), f'l16s5_sol_{i}')
    check(out is not None, f'l16 screens[5] tests[{i}] solution compiles: {err}')
    if out is not None:
        n = int(out.splitlines()[-1])
        want_zero = t['call'] == 'run_tests()'
        check((n == 0) if want_zero else (n > 0), f'l16 screens[5] tests[{i}] solution: run_tests()={n}, defines={defs}')
    out, err = cpp_run(testkit_src(defs, w['starter']), f'l16s5_st_{i}')
    if out is not None and defs:
        n = int(out.splitlines()[-1])
        check((n > 0) == (defs == {'BUG2': 1}), f'l16 screens[5] prose: starter catches only BUG2 (defines={defs}, fails={n})')

# ---------------------------------------------------------------- l17: prefix sums
def brute_div(nums, k):
    return sum(1 for i in range(len(nums)) for j in range(i, len(nums)) if sum(nums[i:j + 1]) % k == 0)
sol17 = {}; exec(L17['screens'][1]['widget']['solution'], sol17); cdk = sol17['count_subarrays_divisible_by_k']
st17 = {}; exec(L17['screens'][1]['widget']['starter'], st17); cdk_slow = st17['count_subarrays_divisible_by_k']
for i, t in enumerate(L17['screens'][1]['widget']['tests']):
    loc = {'count_subarrays_divisible_by_k': cdk}
    if 'setup' in t: exec(t['setup'], loc)
    check(eval(t['call'], loc) == int(t['expect']), f'l17 screens[1] tests[{i}] solution gives {t["expect"]}')
    if 'setup' not in t:
        args = eval(t['call'][len('count_subarrays_divisible_by_k('):-1])
        check(brute_div(*args) == int(t['expect']) and cdk_slow(*args) == int(t['expect']), f'l17 screens[1] tests[{i}] expect agrees with brute force and starter')
check(400001 * 400000 // 2 == 80000200000, 'l17 screens[1] tests[9] all prefixes share remainder 0: C(400001, 2)')
check(math.comb(200001, 2) + math.comb(200000, 2) == 40000000000, 'l17 screens[1] tests[10] remainders alternate 0, 1')
check([(s % 3) for s in itertools.accumulate([0, -1, 3, 0])] == [0, 2, 2, 2], 'l17 screens[1] byKey test-9: prefix remainders 0, 2, 2, 2')
check(400000 * 400001 // 2 == 80000200000 and 400000 * 400001 // 2 > 8e10 * 0.99, 'l17 screens[1] byKey test-10: a double loop makes 80 billion steps')
check(all((-s) % 5 >= 0 for s in range(1, 50)), 'l17 screens[1] byKey test-5: Python % with positive k is never negative')
random.seed(17)
for _ in range(500):
    nums = [random.randint(-6, 6) for _ in range(random.randint(0, 8))]; k = random.randint(1, 5)
    check(cdk(nums, k) == brute_div(nums, k), 'l17 screens[1] explain: dict count equals brute force on random lists')
# counters: the dict solution does one pass; the starter does n(n+1)/2 inner steps
def cdk_counted(nums, k):
    ops = 0; seen = {0: 1}; total = count = 0
    for x in nums:
        ops += 1; total = (total + x) % k; count += seen.get(total, 0); seen[total] = seen.get(total, 0) + 1
    return count, ops
def slow_counted(nums, k):
    ops = 0; count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            ops += 1; total += nums[j]
            if total % k == 0: count += 1
    return count, ops
for n in [10, 100, 1000]:
    nums = [random.randint(-9, 9) for _ in range(n)]
    check(cdk_counted(nums, 7)[1] == n and slow_counted(nums, 7)[1] == n * (n + 1) // 2, f'l17 screens[1]/[2] counters: one pass vs n(n+1)/2 at n={n}')
check(sum(1 for t in L17['screens'][1]['widget']['tests'][:9] if 'setup' not in t) == 9
      and all(len(eval(t['call'][len('count_subarrays_divisible_by_k('):-1])[0]) <= 6 for t in L17['screens'][1]['widget']['tests'][:9]),
      'l17 screens[2] canvas: tests 1 to 9 have at most 6 numbers')
# summary formula: pairs = sum_r C(c_r, 2) with the empty prefix
def pairs_formula(nums, k):
    from collections import Counter
    c = Counter(s % k for s in itertools.accumulate([0] + nums))
    return sum(math.comb(v, 2) for v in c.values())
for _ in range(300):
    nums = [random.randint(-6, 6) for _ in range(random.randint(0, 8))]; k = random.randint(1, 5)
    check(pairs_formula(nums, k) == brute_div(nums, k), 'l17 summary formula sum C(c_r, 2) counts the subarrays')
# screen 3: C++ remainders and the C++ solution against all 11 tests
out, err = cpp_run(cpp_main('std::cout << (-1 % 3) << " " << (((-1 % 3) + 3) % 3) << " " << (-3 % 3);'), 'l17_mod')
check(out == '-1 2 0', f'l17 screens[3] canvas: -1 % 3 is -1 in C++ and ((-1 % 3) + 3) % 3 is 2 (got {out!r} {err})')
w3 = L17['screens'][3]['widget']
def cpp_call(t):
    if 'args' in t:
        v, k = t['args']; return f'count_subarrays_divisible_by_k(std::vector<int>{{{", ".join(map(str, v))}}}, {k})'
    return t['call']
body = ''.join(f'std::cout << ({cpp_call(t)}) << "\\n";' for t in w3['tests'])
out, err = cpp_run(w3['solution'] + cpp_main(body), 'l17_cpp_sol')
check(out is not None and [int(x) for x in out.split()] == [int(t['expect']) for t in w3['tests']], f'l17 screens[3] C++ solution passes all 11 tests ({err[:200]})')
# the starter is correct on the nine small tests (it is slow, not wrong)
body_small = ''.join(f'std::cout << ({cpp_call(t)}) << "\\n";' for t in w3['tests'][:9])
out, err = cpp_run(w3['starter'] + cpp_main(body_small), 'l17_cpp_st')
check(out is not None and [int(x) for x in out.split()] == [int(t['expect']) for t in w3['tests'][:9]], 'l17 screens[3] C++ starter is correct on tests 1 to 9')
# byKey test-9: without the normalisation the C++ count on [-1, 3, 0], k=3 is 1
nofix = w3['solution'].replace('total = ((total + x) % k + k) % k;', 'total = (total + x) % k;')
out, err = cpp_run(nofix + cpp_main('std::cout << count_subarrays_divisible_by_k(std::vector<int>{-1, 3, 0}, 3);'), 'l17_nofix')
check(out == '1', f'l17 screens[3] byKey test-9: without the fix the count is 1, not 3 (got {out!r})')
check(80000200000 > 2 ** 31 - 1 and 40000000000 > 2 ** 31 - 1, 'l17 screens[3] how and byKey test-11: counts need long long')
# screen 5: longest zero-sum stretch
def brute_zero(nums):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i:j + 1]) == 0: best = max(best, j - i + 1)
    return best
sol5 = {}; exec(L17['screens'][5]['widget']['solution'], sol5); lzs = sol5['longest_zero_sum_subarray']
for i, t in enumerate(L17['screens'][5]['widget']['tests']):
    loc = {'longest_zero_sum_subarray': lzs}
    if 'setup' in t: exec(t['setup'], loc)
    check(eval(t['call'], loc) == int(t['expect']), f'l17 screens[5] tests[{i}] solution gives {t["expect"]}')
    if 'setup' not in t:
        args = eval(t['call'][len('longest_zero_sum_subarray('):-1])
        check(brute_zero(args) == int(t['expect']), f'l17 screens[5] tests[{i}] expect agrees with brute force')
for _ in range(500):
    nums = [random.randint(-4, 4) for _ in range(random.randint(0, 9))]
    check(lzs(nums) == brute_zero(nums), 'l17 screens[5] explain: first-sighting dict equals brute force')
# screen 6: keeping the latest sighting shortens the answer on [4, -4, 3, -3]
def lzs_latest(nums):
    last = {0: -1}; total = best = 0
    for i, x in enumerate(nums):
        total += x
        if total in last: best = max(best, i - last[total])
        last[total] = i
    return best
check(list(itertools.accumulate([0, 4, -4, 3, -3])) == [0, 4, 0, 3, 0], 'l17 screens[6] prefix sums 0, 4, 0, 3, 0')
check(lzs([4, -4, 3, -3]) == 4 and lzs_latest([4, -4, 3, -3]) == 2, 'l17 screens[6] first sighting gives 4, latest gives 2')
check(list(itertools.accumulate([0, 5, -3, 3])) == [0, 5, 2, 5] and lzs([5, -3, 3]) == 2, 'l17 quiz q-first')
check(60 - 5 - 28 - 5 == 22 and 90 - 6 - 8 - 37 == 39, 'l17 screens[0] and quiz q-left minute arithmetic')
check(500 ** 2 < 1e8 and 5000 ** 2 == 2.5e7 < 1e8 and 200000 ** 2 == 4e10 > 1e8, 'l17 quiz q-points groups')
check(brute_plan([[50, 20, 0, 0], [60, 40, 15, 10]], 50) == 65, 'l17 screens[9] A full and B partial, 65, is the optimum')

# ---------------------------------------------------------------- l18: product except self
w18 = L18['screens'][4]['widget']
sol18 = {}; exec(w18['solution'], sol18); pes = sol18['product_except_self']
def brute_pes(nums): return [math.prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]
for i, t in enumerate(w18['tests']):
    loc = {'product_except_self': pes, '__learner_source__': w18['solution']}
    if 'setup' in t: exec(t['setup'], loc)
    got = eval(t['call'], loc)
    check(got == eval(t['expect']), f'l18 screens[4] tests[{i}] solution gives {t["expect"]}')
    if 'setup' not in t and t['call'].startswith('product_except_self('):
        check(brute_pes(eval(t['call'][len('product_except_self('):-1])) == eval(t['expect']), f'l18 screens[4] tests[{i}] expect agrees with brute force')
st18 = {}; exec(w18['starter'], st18)
check(st18['product_except_self']([2, 3, 5, 7]) != [105, 70, 42, 30], 'l18 screens[4] starter fails test 1')
check(6 * 99998 + 3 + 2 == 599993, 'l18 screens[4] tests[7] sum 599993')
for _ in range(300):
    nums = [random.randint(-3, 3) for _ in range(random.randint(0, 7))]
    check(pes(nums) == brute_pes(nums), 'l18 screens[4] two-pass equals brute force (zeros included)')
# counters: two passes of n multiplications each; brute force touches n(n-1) entries
def pes_counted(nums):
    n = len(nums); out = [1] * n; left = 1; mul = 0
    for i in range(n): out[i] = left; left *= nums[i]; mul += 1
    right = 1
    for i in range(n - 1, -1, -1): out[i] *= right; right *= nums[i]; mul += 2
    return out, mul
for n in [10, 1000, 100000]:
    nums = [random.randint(1, 3) for _ in range(n)]
    check(pes_counted(nums)[1] == 3 * n, f'l18 screens[9] linear: 3n multiplications at n={n}')
    check(n * (n - 1) == sum(n - 1 for _ in range(n)), f'l18 screens[2] brute force touches n(n-1) entries at n={n}')
check(100000 * 99999 == 9999900000 and 50000 * 49999 == 2499950000, 'l18 screens[2] and quiz q-cost')
try:
    total = math.prod([3, 0, 2]); _ = total / 0; div_ok = True
except ZeroDivisionError:
    div_ok = False
check(not div_ok and brute_pes([3, 0, 2]) == [0, 6, 0], 'l18 screens[3] division by the zero entry cannot give 6')
check(brute_pes([4, 0, 5])[1] == 20, 'l18 quiz q-zero')
check(pes_counted([3, 4, 5])[0] == [20, 15, 12] and [1, 3, 12] == [1, 3, 3 * 4], 'l18 quiz q-pass left pass [1, 3, 12]')
# screens[8] options[3]: "It cannot be done in linear time with constant memory" is marked wrong, its why says
# "It can be done with stored numbers". Stored numbers are linear memory, which is what the explain itself says.
# So the option is not refuted by its why. A streaming lower bound for the no-division version is not established
# here; the finding is that the distractor's text is at least as true as the explain and the why does not rebut it.
check('linear' in L18['screens'][8]['explain']['text'], 'l18 screens[8] explain says the extra space is linear')
def stream_pes(stream):
    kept = []                                   # the why's remedy: store the numbers
    for x in stream: kept.append(x)
    return pes(kept), len(kept)                 # cells kept beyond the output
# fix pass: the distractor now reads "It cannot be done at all once the numbers arrive one at a time" and its why says
# storing the stream and running the right pass at the end works, in linear time and linear extra space.
# So the distractor is false: the stored-stream method gives the right answer with n cells kept and 3n multiplications.
_o18 = L18['screens'][8]['widget']['options'][3]
_t18 = 'cannot be done at all' in _o18['text'] and 'linear time and linear extra space' in _o18['why']
for n in [10, 1000, 100000]:
    stream = [random.randint(1, 3) for _ in range(n)]
    got, kept = stream_pes(iter(stream))
    out, mul = pes_counted(stream)
    right = got == out and (n > 1000 or got == brute_pes(stream))
    check(_t18 and right and kept == n and mul == 3 * n, f'l18 screens[8] options[3].why: storing the stream keeps {kept} cells and uses {mul} multiplications at n={n}, so it can be done and the distractor is false (corrected claim, fix pass)')

# ---------------------------------------------------------------- l19: calendar
def half_open_overlap(a, b): return a[0] < b[1] and b[0] < a[1]
class BruteCal:
    """Reference: counts cover at every integer instant (all tests use whole numbers)."""
    def __init__(self, k=1): self.k = k; self.b = []
    def fits(self, s, e):
        return all(sum(1 for (a, b) in self.b if a <= t < b) + 1 <= self.k for t in range(s, e))
    def book(self, s, e):
        if not self.fits(s, e): return False
        self.b.append((s, e)); return True
    def cancel(self, s, e):
        if (s, e) in self.b: self.b.remove((s, e)); return True
        return False
    def next_free(self, d, after):
        t = after
        while True:
            if self.fits(t, t + d): return t
            t += 1
def run_ref(k, ops):
    c = BruteCal(k); out = []
    for op in ops:
        if op[0] == 0: out.append(c.book(op[1], op[2]))
        elif op[0] == 1: out.append(c.cancel(op[1], op[2]))
        else: out.append(c.next_free(op[1], op[2]))
    return out
for si, name in [(2, 'A'), (4, 'B'), (6, 'C')]:
    w = L19['screens'][si]['widget']
    ns = {}; exec(w['solution'], ns); exec(w['postlude'], ns)
    for i, t in enumerate(w['tests']):
        loc = dict(ns)
        if 'setup' in t: exec(t['setup'], loc)
        got = eval(t['call'], loc)
        check(got == eval(t['expect']), f'l19 screens[{si}] stage {name} tests[{i}] solution gives {t["expect"]}')
        if 'setup' not in t:
            k, ops = eval(t['call'][len('run_cal('):].split(')')[0] + ')') if False else (None, None)
            m = t['call'][len('run_cal('):]
            inner = m[:m.rfind(')')]
            k, ops = eval('(' + inner + ')')
            check(run_ref(k, ops) == eval(t['expect']), f'l19 screens[{si}] stage {name} tests[{i}] expect agrees with the instant-count reference')
    nst = {}; exec(w['starter'], nst); exec(w['postlude'], nst)
    first = w['tests'][0]
    check(eval(first['call'], nst) != eval(first['expect']) or name == 'C', f'l19 screens[{si}] stage {name} starter fails test 1')
# stage C starter must fail some test (its cancel/next_free are stubs)
wC = L19['screens'][6]['widget']; nst = {}; exec(wC['starter'], nst); exec(wC['postlude'], nst)
check(any(eval(t['call'], dict(nst)) != eval(t['expect']) for t in wC['tests'] if 'setup' not in t), 'l19 screens[6] stage C starter fails a test')
# stage A bisect check equals the reference on random k=1 streams; the number of comparisons is two per booking after the search
wA = L19['screens'][2]['widget']; nsA = {}; exec(wA['solution'], nsA)
random.seed(19)
for _ in range(300):
    ops = []
    for _ in range(random.randint(0, 12)):
        s = random.randint(0, 20); ops.append([0, s, s + random.randint(1, 6)])
    c = nsA['Calendar'](); got = [c.book(o[1], o[2]) for o in ops]
    check(got == run_ref(1, ops), 'l19 screens[2] explain: neighbour check equals the reference with k = 1')
# stage B: the overlap count inside [start, end) peaks at start or at an existing start inside
wB = L19['screens'][4]['widget']; nsB = {}; exec(wB['solution'], nsB)
for _ in range(300):
    k = random.randint(1, 3); ops = []
    for _ in range(random.randint(0, 12)):
        s = random.randint(0, 20); ops.append([0, s, s + random.randint(1, 6)])
    c = nsB['Calendar'](k); got = [c.book(o[1], o[2]) for o in ops]
    check(got == run_ref(k, ops), 'l19 screens[4] explain: checking the start and inner starts equals the instant-count reference')
# stage C: next_free candidates (after and the ends above it) equal a scan over every whole start
wCs = {}; exec(wC['solution'], wCs)
for _ in range(400):
    k = random.randint(1, 3); c = wCs['Calendar'](k); r = BruteCal(k)
    for _ in range(random.randint(0, 10)):
        s = random.randint(0, 20); e = s + random.randint(1, 6)
        a = c.book(s, e); b = r.book(s, e); check(a == b, 'l19 stage C book agrees')
    for _ in range(3):
        d = random.randint(1, 6); after = random.randint(0, 25)
        check(c.next_free(d, after) == r.next_free(d, after), 'l19 screens[6] explain: a free start only improves at `after` or where a booking ends')
# screens 0, 3, 5, 7 by hand
check(run_ref(1, [[0, 1, 4], [0, 3, 6], [0, 4, 8], [0, 0, 1]]) == [True, False, True, True], 'l19 screens[0] accepted bookings i1, i3, i4')
check(run_ref(1, [[0, 2, 5], [0, 5, 7], [0, 4, 6], [0, 7, 9], [0, 0, 2]]).count(True) == 4, 'l19 screens[3] four accepted')
check(run_ref(2, [[0, 1, 4], [0, 3, 6], [0, 2, 5], [0, 4, 8]]) == [True, True, False, True], 'l19 screens[5] k = 2: three accepted')
check(run_ref(1, [[0, 9, 12], [0, 12, 15], [2, 3, 9], [2, 2, 9], [1, 9, 12], [2, 3, 9]]) == [True, True, 15, 15, True, 9], 'l19 screens[7] next_free before and after the cancel')
check(run_ref(1, [[0, 2, 6], [0, 6, 9]]) == [True, True], 'l19 quiz q-half')
check(run_ref(2, [[0, 0, 5], [0, 3, 8], [0, 4, 6]]) == [True, True, False], 'l19 quiz q-k')
check(run_ref(1, [[0, 4, 7], [0, 7, 9], [2, 2, 5]]) == [True, True, 9], 'l19 quiz q-free')
check(3 + 10 + 3 + 10 + 4 == 30 and 3 + 10 + 3 + 10 + 10 == 36 and 5 + 10 + 5 + 10 + 10 + 5 == 45, 'l19 quiz q-plan and screens[8] block sums')
# screen 10: the sorted-map-of-changes approach walks the changes inside (linear per booking), counted
def changes_cost(bookings, s, e):
    ops = 0; keys = sorted(set(a for a, _ in bookings) | set(b for _, b in bookings) | {s, e})
    for t in keys:
        if s <= t < e: ops += 1
    return ops
for n in [100, 1000, 10000]:
    bs = [(2 * i, 2 * i + 1) for i in range(n)]
    check(changes_cost(bs, 0, 2 * n) >= n, f'l19 screens[10] explain: the change map walks O(n) entries for a wide booking at n={n}')

# ---------------------------------------------------------------- review-4
R4P = [(36, 20, 14, 8), (48, 30, 16, 9), (75, 44, 30, 15)]
check(brute_plan(R4P, 56) == 92, 'review-4 r4-best-plan optimum 92')
check(48 + 30 + 14 == 92 and 30 + 15 + 8 == 53 <= 56, 'review-4 r4-best-plan accept plan: second full, third and first partial, 53 minutes')
check(max(75 + 16, 75 + 14) == 91 and 44 + 9 <= 56 and 44 + 8 + 9 > 56, 'review-4 r4-best-plan byKey p3: third in full with a partial earns at most 91')
check(greedy_full(R4P, 56) == 84 and sorted(range(3), key=lambda i: -R4P[i][0] / R4P[i][1]) == [0, 2, 1], 'review-4 r4-greedy 84, order first, third, second')
check(20 + 44 == 64 > 56 and 20 + 30 + 44 == 94, 'review-4 r4-greedy byKeys')
def second_largest(xs):
    d = sorted(set(xs), reverse=True); return d[1] if len(d) >= 2 else None
check(second_largest([4, 4, 3, 3, 1]) == 3 and second_largest([2, 2, 1]) == 1 and sorted([2, 2, 1], reverse=True)[1] == 2
      and second_largest([]) is None and second_largest([5]) is None and second_largest([5, 5]) is None, 'review-4 r4-edge-second and r4-edge-value')
check(60 - 5 - 5 - 31 == 19, 'review-4 r4-minutes')
check([s % 4 for s in itertools.accumulate([0, 8, -3, 4, 7, -6, 5])] == [0, 0, 1, 1, 0, 2, 3] and brute_div([8, -3, 4, 7, -6, 5], 4) == 4, 'review-4 r4-count 4 pairs')
check(250000 * 250001 // 2 == 31250125000, 'review-4 r4-steps')
check(brute_pes([2, 1, 3, 4]) == [12, 24, 8, 6], 'review-4 r4-product')
check(run_ref(1, [[0, 5, 9], [0, 8, 12], [0, 9, 13], [0, 13, 15], [0, 12, 14]]) == [True, False, True, True, False], 'review-4 r4-bookings three accepted')
check(run_ref(1, [[0, 10, 20], [0, 26, 40], [2, 6, 10]]) == [True, True, 20], 'review-4 r4-next-free 20')

# ---------------------------------------------------------------- homework-4
hb = H4['items'][0]
for pi in [0, 2]:
    w = hb['parts'][pi]['widget']; ns = {}; exec(w['solution'], ns); exec(w['postlude'], ns)
    tests = (hb['parts'][0]['widget']['tests'] if pi == 2 else []) + w['tests']   # cumulative, AUTHORING 5 "Code parts"
    for i, t in enumerate(tests):
        check(eval(t['call'], dict(ns)) == eval(t['expect']), f'homework-4 h4-leaderboard parts[{pi}] merged tests[{i}] solution gives {t["expect"]}')
    nst = {}; exec(w['starter'], nst); exec(w['postlude'], nst)
    check(any(eval(t['call'], dict(nst)) != eval(t['expect']) for t in w['tests']), f'homework-4 h4-leaderboard parts[{pi}] starter fails a test')
def ref_board(ops):
    sc = {}; out = []
    for op in ops:
        if op[0] == 0: sc[op[1]] = sc.get(op[1], 0) + op[2]
        elif op[0] == 1: out.append(sum(sorted(sc.values(), reverse=True)[:op[1]]))
        else: sc.pop(op[1], None)
    return out
for pi in [0, 2]:
    for t in hb['parts'][pi]['widget']['tests']:
        ops = eval(t['call'][len('run_board('):-1])
        check(ref_board(ops) == eval(t['expect']), f'homework-4 h4-leaderboard parts[{pi}] expect agrees with an independent board')
check(100000 * 2000 == 200000000, 'homework-4 h4-leaderboard parts[1] explain: sorting visits 2e8 scores in all')
check(sum(range(1200)) == 719400 == 1200 * 1199 // 2, 'homework-4 h4-calendar parts[0]')
check(math.ceil(math.log2(10 ** 6)) == 20 and 2 ** 19 < 10 ** 6 < 2 ** 20, 'homework-4 h4-calendar parts[2] ceil log2 1e6 = 20')
# a bisect over 10^6 sorted starts takes at most 20 comparisons (counted with a wrapper)
class Counted(list):
    def __init__(self, xs): super().__init__(xs); self.cmp = 0
starts = list(range(0, 2 * 10 ** 6, 2))
def bisect_counted(a, x):
    lo, hi, c = 0, len(a), 0
    while lo < hi:
        mid = (lo + hi) // 2; c += 1
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    assert lo == bisect.bisect_left(a, x)
    return c
check(max(bisect_counted(starts, x) for x in [0, 1, 999999, 1999999, 2000000, 3]) == 20, 'homework-4 h4-calendar parts[2] counted bisect over 1e6 uses at most 20 comparisons')
# h4-zero-sum-cpp: C++ solution and starter on the tests
wz = H4['items'][2]['widget']
def zcall(t):
    if 'args' in t: return f'longest_zero_sum_subarray(std::vector<int>{{{", ".join(map(str, t["args"][0]))}}})'
    return t['call']
out, err = cpp_run(wz['solution'] + cpp_main(''.join(f'std::cout << ({zcall(t)}) << "\\n";' for t in wz['tests'])), 'h4_zero_sol')
check(out is not None and [int(x) for x in out.split()] == [int(t['expect']) for t in wz['tests']], f'homework-4 h4-zero-sum-cpp solution passes all 12 tests ({err[:200]})')
out, err = cpp_run(wz['starter'] + cpp_main(''.join(f'std::cout << ({zcall(t)}) << "\\n";' for t in wz['tests'] if 'args' in t)), 'h4_zero_st')
check(out is not None and [int(x) for x in out.split()] == [int(t['expect']) for t in wz['tests'] if 'args' in t], 'homework-4 h4-zero-sum-cpp starter is correct on the small tests')
for t in wz['tests']:
    if 'args' in t: check(brute_zero(t['args'][0]) == int(t['expect']), f'homework-4 h4-zero-sum-cpp expect {t["expect"]} agrees with brute force')
check(lzs([2, -2] * 150000) == 300000 and lzs([3, 1, -4] * 120000 + [6]) == 360000, 'homework-4 h4-zero-sum-cpp big tests')
# h4-aloud model numbers
ps = list(itertools.accumulate([0, 7, -2, 9, 4, -5, 6]))
check(ps == [0, 7, 5, 14, 18, 13, 19] and [p % 5 for p in ps] == [0, 2, 0, 4, 3, 3, 4] and brute_div([7, -2, 9, 4, -5, 6], 5) == 3, 'homework-4 h4-aloud example answer 3')
check(300000 * 300001 // 2 == 45000150000, 'homework-4 h4-aloud brute force steps')
check(80000 * 1500 == 120000000 and 5 * 1500 == 7500 and 120000000 // 7500 == 16000, 'homework-4 h4-leaderboard-cost')
check(brute_plan([(28, 16, 9, 5), (54, 32, 21, 11), (80, 46, 26, 14)], 58) == 101 and greedy_full([(28, 16, 9, 5), (54, 32, 21, 11), (80, 46, 26, 14)], 58) == 82
      and 46 + 11 + 5 == 62 > 58, 'homework-4 h4-plan 101, greedy 82, over 62 minutes')
check(brute_zero([5, 3, -1, -2, 4, 7]) == 3 and list(itertools.accumulate([0, 5, 3, -1, -2, 4, 7])) == [0, 5, 8, 7, 5, 9, 16], 'homework-4 h4-next-test middle stretch of 3')
def prefix_only(nums):
    best = 0; total = 0
    for i, x in enumerate(nums):
        total += x
        if total == 0: best = i + 1
    return best
check(prefix_only([5, 3, -1, -2, 4, 7]) == 0 != 3 and all(prefix_only(x) == brute_zero(x) for x in [[], [7], [0], [2, -2]]), 'homework-4 h4-next-test explain: a prefix-only solution passes the four old tests and fails the new one')

# ---------------------------------------------------------------- report
print(f'{len(FAILS)} failing check(s)')
expected = [f for f in FAILS if f.startswith('EXPECTED_FAIL')]
print(f'{len(expected)} expected (content findings), {len(FAILS) - len(expected)} unexpected')
sys.exit(1 if FAILS else 0)
