"""coding-int level 4: six drills for E8 (sessions of prefix-sums and hashing, and an intervals stopwatch).
Every expected value comes from an independent brute force or a closed form. Run: python3 -I build_drills.py"""
import json, os, random, sys

ROOT = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/drills/'
rnd = random.Random(20261104)

# ---------------- reference and brute force ----------------


def balanced_ref(bits):
    first = {0: -1}
    total = best = 0
    for i, b in enumerate(bits):
        total += 1 if b else -1
        if total in first:
            best = max(best, i - first[total])
        else:
            first[total] = i
    return best


def balanced_brute(bits):
    best = 0
    for i in range(len(bits)):
        z = o = 0
        for j in range(i, len(bits)):
            if bits[j]:
                o += 1
            else:
                z += 1
            if z == o:
                best = max(best, j - i + 1)
    return best


def gap_ref(nums, k):
    seen = {}
    count = 0
    for x in nums:
        count += seen.get(x - k, 0)
        if k:
            count += seen.get(x + k, 0)
        seen[x] = seen.get(x, 0) + 1
    return count


def gap_brute(nums, k):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if abs(nums[i] - nums[j]) == k)


def sumk_brute(nums, k):
    best = 0
    for i in range(len(nums)):
        t = 0
        for j in range(i, len(nums)):
            t += nums[j]
            if t == k:
                best = max(best, j - i + 1)
    return best


def sumk_ref(nums, k):
    first = {0: -1}
    t = best = 0
    for i, x in enumerate(nums):
        t += x
        if t - k in first:
            best = max(best, i - first[t - k])
        if t not in first:
            first[t] = i
    return best


def missing_brute(nums):
    s = set(nums)
    m = 1
    while m in s:
        m += 1
    return m


def inter_brute(a, b):
    out = []
    for x, y in a:
        for u, v in b:
            lo, hi = max(x, u), min(y, v)
            if lo <= hi:
                out.append([lo, hi])
    out.sort()
    return out


def inter_ref(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            out.append([lo, hi])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


def insert_brute(iv, add):
    pts = [list(x) for x in iv] + [list(add)]
    pts.sort()
    out = []
    for s, e in pts:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def insert_ref(iv, add):
    out = []
    s, e = add
    i = 0
    while i < len(iv) and iv[i][1] < s:
        out.append(iv[i]); i += 1
    while i < len(iv) and iv[i][0] <= e:
        s = min(s, iv[i][0]); e = max(e, iv[i][1]); i += 1
    out.append([s, e])
    out.extend(iv[i:])
    return out


def rand_disjoint(n, span):
    pts = sorted(rnd.sample(range(span), 2 * n))
    return [[pts[2 * i], pts[2 * i + 1]] for i in range(n)]


# ---------------- verification of references ----------------
for _ in range(3000):
    bits = [rnd.randint(0, 1) for _ in range(rnd.randint(0, 14))]
    assert balanced_ref(bits) == balanced_brute(bits)
    nums = [rnd.randint(-3, 5) for _ in range(rnd.randint(0, 10))]
    k = rnd.randint(0, 5)
    assert gap_ref(nums, k) == gap_brute(nums, k)
    k2 = rnd.randint(-4, 6)
    assert sumk_ref(nums, k2) == sumk_brute(nums, k2), (nums, k2)
    a = rand_disjoint(rnd.randint(0, 4), 30)
    b = rand_disjoint(rnd.randint(0, 4), 30)
    assert inter_ref(a, b) == inter_brute(a, b), (a, b)
    iv = rand_disjoint(rnd.randint(0, 5), 40)
    add = sorted(rnd.sample(range(40), 2))
    assert insert_ref(iv, add) == insert_brute(iv, add), (iv, add)
print('references agree with brute forces')

# ---------------- drill builders ----------------


def py_drill(did, name, pattern, tags, skills, diff, pace, fn, returns, brief, cons, hint, starter, examples, tests, solution, notes):
    return {"id": did, "name": name, "course": "coding-int", "pack": "ci", "pattern": pattern, "tags": tags, "skills": skills,
            "difficulty": diff, "pace": pace, "fn": fn, "returns": returns, "brief": brief, "constraints": cons, "hint": hint,
            "starter": starter, "examples": examples, "tests": tests,
            "how": f"Submit runs {len(tests)} hidden tests. Each answer must equal the expected value.",
            "solution": solution, "notes": notes}


def pyc(call, expect, note=None):
    d = {"call": call, "expect": repr(expect), "compare": "equal"}
    if note:
        d["note"] = note
    return d


def cppc(fn, args, types, expect, note=None, name=None):
    d = {}
    if name:
        d["name"] = name
    d.update({"call": fn, "args": args, "types": types, "expect": expect, "compare": "equal"})
    if note:
        d["note"] = note
    return d


def cpp_drill(did, name, pattern, tags, skills, diff, pace, brief, cons, hint, starter, examples, tests, solution, notes):
    return {"id": did, "name": name, "course": "coding-int", "pack": "ci", "language": "cpp", "pattern": pattern, "tags": tags, "skills": skills,
            "difficulty": diff, "pace": pace, "brief": brief, "constraints": cons, "hint": hint, "starter": starter,
            "examples": examples, "tests": tests, "how": f"Submit runs {len(tests)} hidden tests. Each answer must equal the expected value.",
            "solution": solution, "notes": notes}


drills = {}

# 1 balanced run (python, prefix-sums, d4)
small = [[], [0], [1], [0, 1], [1, 1, 0], [1, 0, 0, 1, 1], [0, 0, 0], [1, 1, 0, 0, 0, 1], [0, 1, 1, 1, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1, 0, 0, 0]]
tests = [pyc(f"longest_balanced_run({b!r})", balanced_brute(b)) for b in small]
assert balanced_ref([0, 1] * 100000) == 200000 and balanced_ref([1] * 100000 + [0] * 50000) == 100000
tests.append(pyc("longest_balanced_run([0, 1] * 100000)", 200000))
tests.append(pyc("longest_balanced_run([1] * 100000 + [0] * 50000)", 100000))
ex = [pyc("longest_balanced_run([1, 0, 0, 1, 1])", 4, "The first four entries hold two 1s and two 0s. Nothing longer balances."),
      pyc("longest_balanced_run([1, 1, 1])", 0, "There is no 0, so no run is balanced.")]
for e in ex:
    assert eval(e['call'], {'longest_balanced_run': balanced_ref}) == eval(e['expect'])
drills['ci-balanced-run'] = py_drill(
    'ci-balanced-run', 'Longest run with equal zeros and ones', 'prefix-sums', ['balanced-run'], ['ci-patterns', 'ci-timed'], 4, 1500, 'longest_balanced_run', 'a whole number',
    "`bits` is a list of 0s and 1s. Return the length of the longest contiguous run that holds as many 0s as 1s, or 0 if no run does.\n\nWrite `longest_balanced_run(bits)`.\n\nExample. For `bits = [1, 0, 0, 1, 1]` the first four entries hold two 1s and two 0s, so the answer is 4.",
    ["$0 \\le n \\le 200{,}000$ entries, each 0 or 1.", "$O(n)$ time is the target. Checking every run is too slow.", "All tests share a 5-second time limit."],
    "Count each 1 as +1 and each 0 as -1. A balanced run is a stretch whose total is 0, so use the first index at which each running total was seen.",
    "def longest_balanced_run(bits):\n    # your code here\n    return 0\n", ex, tests,
    "def longest_balanced_run(bits):\n    first = {0: -1}\n    total = best = 0\n    for i, b in enumerate(bits):\n        total += 1 if b else -1\n        if total in first:\n            best = max(best, i - first[total])\n        else:\n            first[total] = i\n    return best\n",
    ["Scoring a 0 as -1 turns balanced into zero-sum.", "A repeated running total marks a balanced stretch, and the first sighting makes it longest.", "One pass with a dict, so the work is $O(n)$."])

# 2 pair gaps (python, hashing, d3)
small = [([], 1), ([5], 0), ([1, 2], 1), ([4, 4], 0), ([6, 2, 8, 2, 4], 2), ([7, 7, 7], 0), ([2, -1, 3, 0, -2], 3), ([2, 6, 2, 6], 4), ([9, 6, 9, 3, 6], 3), ([0, 0, 2, 2, 0], 2)]
tests = [pyc(f"count_pairs_with_gap({n!r}, {k})", gap_brute(n, k)) for n, k in small]
assert gap_ref([1, 2] * 100000, 1) == 10 ** 10 and gap_ref([9] * 150000, 0) == 150000 * 149999 // 2 == 11249925000
tests.append(pyc("count_pairs_with_gap([1, 2] * 100000, 1)", 10 ** 10))
tests.append(pyc("count_pairs_with_gap([9] * 150000, 0)", 11249925000))
ex = [pyc("count_pairs_with_gap([6, 2, 8, 2, 4], 2)", 4, "The pairs are 6 with 8, 6 with 4, and 4 with each 2. That is four."), pyc("count_pairs_with_gap([4, 4], 0)", 1, "The one pair has equal values, so the gap is 0.")]
for e in ex:
    assert eval(e['call'], {'count_pairs_with_gap': gap_ref}) == eval(e['expect'])
drills['ci-pair-gaps'] = py_drill(
    'ci-pair-gaps', 'Pairs a fixed gap apart', 'hashing', ['pair-gaps'], ['ci-patterns', 'ci-timed'], 3, 1200, 'count_pairs_with_gap', 'a whole number',
    "`nums` is a list of whole numbers and `k` is at least 0. Count the pairs of positions `i < j` with `abs(nums[i] - nums[j]) == k`. Equal values at different positions count separately.\n\nWrite `count_pairs_with_gap(nums, k)`.\n\nExample. For `nums = [6, 2, 8, 2, 4]` and `k = 2` the pairs are 6 with 8, 6 with 4, and 4 with each 2, so the answer is 4.",
    ["$0 \\le n \\le 200{,}000$ entries, each a whole number between $-10^9$ and $10^9$.", "$O(n)$ time is the target. Checking every pair is too slow.", "All tests share a 5-second time limit. Answers can pass $10^{10}$."],
    "Keep a dict of how many times each value has been seen. For each new value, add the counts of the values `k` below and `k` above it. Take care that `k = 0` is one value, not two.",
    "def count_pairs_with_gap(nums, k):\n    # your code here\n    return 0\n", ex, tests,
    "def count_pairs_with_gap(nums, k):\n    seen = {}\n    count = 0\n    for x in nums:\n        count += seen.get(x - k, 0)\n        if k:\n            count += seen.get(x + k, 0)\n        seen[x] = seen.get(x, 0) + 1\n    return count\n",
    ["Each new value pairs with every earlier value that is exactly `k` away.", "When `k` is 0 the two partners coincide, so the second count is skipped.", "One pass with a dict, so the work is $O(n)$."])

# 5 interval intersections (python, intervals, d4)
small = [([], []), ([[1, 3]], []), ([[0, 2]], [[2, 5]]), ([[0, 2], [5, 10]], [[1, 5], [8, 12]]), ([[1, 4], [6, 9]], [[2, 3], [7, 8]]),
         ([[3, 7]], [[0, 10]]), ([[0, 1], [3, 4], [6, 7]], [[1, 3], [4, 6]]), ([[2, 9]], [[2, 9]]), ([[1, 5], [10, 14], [16, 20]], [[3, 11], [13, 17]])]
tests = [pyc(f"interval_intersections({a!r}, {b!r})", inter_brute(a, b)) for a, b in small]
A = [[4 * i, 4 * i + 2] for i in range(100000)]
B = [[4 * i + 1, 4 * i + 3] for i in range(100000)]
assert sum(y - x for x, y in inter_ref(A, B)) == 100000
tests.append(pyc("sum(y - x for x, y in interval_intersections([[4 * i, 4 * i + 2] for i in range(100000)], [[4 * i + 1, 4 * i + 3] for i in range(100000)]))", 100000))
C = [[0, 400000]]
D = [[2 * i, 2 * i + 1] for i in range(200000)]
assert len(inter_ref(C, D)) == 200000
tests.append(pyc("len(interval_intersections([[0, 400000]], [[2 * i, 2 * i + 1] for i in range(200000)]))", 200000))
ex = [pyc("interval_intersections([[0, 2], [5, 10]], [[1, 5], [8, 12]])", [[1, 2], [5, 5], [8, 10]], "[0, 2] meets [1, 5] on [1, 2], [5, 10] meets [1, 5] at the point 5, and [5, 10] meets [8, 12] on [8, 10]."),
      pyc("interval_intersections([[0, 2]], [[2, 5]])", [[2, 2]], "Closed intervals that share an end meet at one point.")]
for e in ex:
    assert eval(e['call'], {'interval_intersections': inter_ref}) == eval(e['expect'])
drills['ci-interval-intersections'] = py_drill(
    'ci-interval-intersections', 'Where two interval lists overlap', 'intervals', ['interval-intersections'], ['ci-patterns', 'ci-timed'], 4, 1500, 'interval_intersections', 'a list of closed intervals',
    "`a` and `b` are lists of closed intervals `[start, end]`. Within each list the intervals are sorted and do not overlap. Return every overlap of an interval of `a` with an interval of `b`, as closed intervals sorted by start. A single shared point counts as `[x, x]`.\n\nWrite `interval_intersections(a, b)`.\n\nExample. For `a = [[0, 2]]` and `b = [[2, 5]]` the answer is `[[2, 2]]`.",
    ["Each list holds at most 200,000 intervals; either may be empty.", "$O(n + m)$ time is the target. Comparing every pair is too slow.", "All tests share a 5-second time limit."],
    "Walk both lists with two pointers. The overlap of the current pair is from the larger start to the smaller end. Then move on in the list whose interval ends first.",
    "def interval_intersections(a, b):\n    # your code here\n    return []\n", ex, tests,
    "def interval_intersections(a, b):\n    i = j = 0\n    out = []\n    while i < len(a) and j < len(b):\n        lo = max(a[i][0], b[j][0])\n        hi = min(a[i][1], b[j][1])\n        if lo <= hi:\n            out.append([lo, hi])\n        if a[i][1] < b[j][1]:\n            i += 1\n        else:\n            j += 1\n    return out\n",
    ["The overlap, if any, runs from the larger start to the smaller end.", "The interval that ends first cannot overlap anything later in the other list, so it is dropped.", "Each step drops one interval, so the work is $O(n + m)$."])

# 3 C++ longest sum k (prefix-sums, d4)
T2 = ["std::vector<int>", "int"]
small = [([], 3), ([5], 5), ([5], 4), ([1, 2, 3], 6), ([4, -1, 2, 1], 5), ([-2, 3, -1, 4], 0), ([2, -2, 2, -2], 0), ([1, 1, 1], 2), ([7, 3, -3, 3, -7, 8], 3), ([0, 0, 0], 0), ([-5, -5, 10, 5], 5)]
tests = [cppc("longest_sum_k", [n, k], T2, sumk_brute(n, k)) for n, k in small]
assert sumk_ref([1] * 300000, 150000) == 150000 and sumk_ref([4, -4] * 150000, 0) == 300000 and sumk_ref([1, -1] * 150000 + [1], 1) == 300001
tests.append({"call": "longest_sum_k(std::vector<int>(300000, 1), 150000)", "expect": 150000, "compare": "equal"})
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 150000; ++i) { v.push_back(4); v.push_back(-4); } return longest_sum_k(v, 0); }()", "expect": 300000, "compare": "equal"})
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 150000; ++i) { v.push_back(1); v.push_back(-1); } v.push_back(1); return longest_sum_k(v, 1); }()", "expect": 300001, "compare": "equal"})
ex = [cppc("longest_sum_k", [[4, -1, 2, 1], 5], T2, 3, "The last three entries, -1, 2 and 1, sum to 2, and the first three, 4, -1 and 2, sum to 5. That is 3."),
      cppc("longest_sum_k", [[5], 4], T2, 0, "The only subarray sums to 5, not 4.")]
assert sumk_brute([4, -1, 2, 1], 5) == 3 and sumk_brute([5], 4) == 0
drills['ci-cpp-longest-sum-k'] = cpp_drill(
    'ci-cpp-longest-sum-k', 'Longest stretch with a given sum', 'prefix-sums', ['sum-stretch'], ['ci-patterns', 'ci-timed'], 4, 1500,
    "`nums` is a list of whole numbers, which may be negative or zero. Write `longest_sum_k(nums, k)`, which returns the length of the longest contiguous subarray whose sum is exactly `k`, or 0 if there is none.",
    ["$0 \\le n \\le 300{,}001$ entries, each between -1,000 and 1,000.", "$O(n)$ time is the target. Trying every start and end is too slow.", "Each test has a 5-second limit. Keep running totals in `long long`."],
    "A stretch ends at `i` with sum `k` when an earlier prefix sum equals the current one minus `k`. Store the first index of each prefix sum, and look up `total - k`.",
    "#include <vector>\n#include <unordered_map>\n\nint longest_sum_k(std::vector<int> nums, int k) {\n    // your code here\n    return 0;\n}\n", ex, tests,
    "#include <vector>\n#include <unordered_map>\n#include <algorithm>\n\nint longest_sum_k(std::vector<int> nums, int k) {\n    std::unordered_map<long long, int> first;\n    first[0] = -1;\n    long long total = 0;\n    int best = 0;\n    for (int i = 0; i < (int)nums.size(); ++i) {\n        total += nums[i];\n        auto it = first.find(total - k);\n        if (it != first.end()) best = std::max(best, i - it->second);\n        if (!first.count(total)) first[total] = i;\n    }\n    return best;\n}\n",
    ["The stretch ending at `i` has sum `k` when some earlier prefix sum equals `total - k`.", "Keeping the first index of each prefix sum makes the stretch longest.", "One pass with a hash map, so the work is $O(n)$."])

# 4 C++ first missing positive (hashing, d3)
T1 = ["std::vector<int>"]
small = [[], [1], [2], [1, 2, 3], [3, 4, -1, 1], [7, 8, 9], [1, 1, 2, 2], [-3, -1, 0], [2, 3, 4, 5], [5, 4, 3, 1, 2, 7], [1000000000, 1, 2]]
tests = [cppc("first_missing_positive", [n], T1, missing_brute(n)) for n in small]
assert missing_brute(list(range(1, 200001))) == 200001
assert missing_brute([x for x in range(1, 200001) if x != 150000]) == 150000
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 200000; i >= 1; --i) v.push_back(i); return first_missing_positive(v); }()", "expect": 200001, "compare": "equal"})
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 1; i <= 200000; ++i) if (i != 150000) v.push_back(i); return first_missing_positive(v); }()", "expect": 150000, "compare": "equal"})
ex = [cppc("first_missing_positive", [[3, 4, -1, 1]], T1, 2, "The numbers 1, 3 and 4 are present, and 2 is the smallest positive missing."),
      cppc("first_missing_positive", [[7, 8, 9]], T1, 1, "The number 1 is missing.")]
drills['ci-cpp-first-missing'] = cpp_drill(
    'ci-cpp-first-missing', 'Smallest missing positive', 'hashing', ['first-missing'], ['ci-patterns', 'ci-timed'], 3, 1200,
    "`nums` is a list of whole numbers, which may repeat and may be negative. Write `first_missing_positive(nums)`, which returns the smallest positive whole number that is not in `nums`.",
    ["$0 \\le n \\le 200{,}000$ entries, each between $-10^9$ and $10^9$.", "$O(n)$ expected time is the target. Sorting is allowed, but checking each candidate with a scan is too slow.", "Each test has a 5-second limit."],
    "Put every entry in a hash set. Then count up from 1 until a number is missing. The answer is never above $n + 1$.",
    "#include <vector>\n#include <unordered_set>\n\nint first_missing_positive(std::vector<int> nums) {\n    // your code here\n    return 0;\n}\n", ex, tests,
    "#include <vector>\n#include <unordered_set>\n\nint first_missing_positive(std::vector<int> nums) {\n    std::unordered_set<int> seen(nums.begin(), nums.end());\n    int m = 1;\n    while (seen.count(m)) ++m;\n    return m;\n}\n",
    ["A set answers 'is `m` present' in constant time.", "The answer is at most $n + 1$, so the count-up loop is short.", "Building the set and the loop are both $O(n)$."])

# 6 C++ insert interval (intervals, d4)
TI = ["std::vector<std::vector<int>>", "std::vector<int>"]
small = [([], [3, 5]), ([[1, 2]], [4, 6]), ([[1, 2]], [2, 6]), ([[1, 2], [5, 6]], [3, 4]), ([[1, 3], [6, 9]], [2, 5]), ([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]),
         ([[4, 5]], [0, 1]), ([[4, 5]], [0, 4]), ([[0, 10]], [3, 4]), ([[1, 2], [4, 5], [7, 8]], [0, 9]), ([[2, 3], [5, 6]], [6, 6])]
tests = [cppc("insert_interval", [iv, add], TI, insert_brute(iv, add)) for iv, add in small]
big = [[3 * i, 3 * i + 1] for i in range(100000)]
exp1 = insert_brute(big, [5, 150000])
assert len(exp1) == insert_ref(big, [5, 150000]).__len__()
exp2 = insert_brute(big, [299998, 300005])
tests.append({"call": "[&]{ std::vector<std::vector<int>> v; for (int i = 0; i < 100000; ++i) v.push_back({3 * i, 3 * i + 1}); return (int)insert_interval(v, {5, 150000}).size(); }()", "expect": len(exp1), "compare": "equal"})
tests.append({"call": "[&]{ std::vector<std::vector<int>> v; for (int i = 0; i < 100000; ++i) v.push_back({3 * i, 3 * i + 1}); return (int)insert_interval(v, {299998, 300005}).size(); }()", "expect": len(exp2), "compare": "equal"})
ex = [cppc("insert_interval", [[[1, 3], [6, 9]], [2, 5]], TI, [[1, 5], [6, 9]], "The new interval joins [1, 3], and [6, 9] is left alone."),
      cppc("insert_interval", [[[1, 2]], [2, 6]], TI, [[1, 6]], "The two intervals share the point 2, so they join.")]
for e in ex:
    a = e['args']
    assert insert_brute(a[0], a[1]) == e['expect']
print('big results:', len(exp1), len(exp2))
drills['ci-cpp-insert-interval'] = cpp_drill(
    'ci-cpp-insert-interval', 'Insert into sorted intervals', 'intervals', ['insert-interval'], ['ci-patterns', 'ci-timed'], 4, 1500,
    "`intervals` holds closed intervals `{start, end}`, sorted by start, that do not overlap. Write `insert_interval(intervals, add)`, which adds the closed interval `add`, joins every interval it overlaps or touches, and returns the list sorted by start.",
    ["The list may be empty. Intervals that share an end point join: `{1, 2}` and `{2, 6}` give `{1, 6}`.", "$O(n)$ time is the target. Sorting the whole list again is allowed but not needed.", "Each test has a 5-second limit."],
    "Copy the intervals that end before `add` starts. Then widen `add` over every interval that starts at or before its end. Finally copy the rest.",
    "#include <vector>\n#include <algorithm>\n\nstd::vector<std::vector<int>> insert_interval(std::vector<std::vector<int>> intervals, std::vector<int> add) {\n    // your code here\n    return intervals;\n}\n", ex, tests,
    "#include <vector>\n#include <algorithm>\n\nstd::vector<std::vector<int>> insert_interval(std::vector<std::vector<int>> intervals, std::vector<int> add) {\n    std::vector<std::vector<int>> out;\n    size_t i = 0;\n    int s = add[0], e = add[1];\n    while (i < intervals.size() && intervals[i][1] < s) out.push_back(intervals[i++]);\n    while (i < intervals.size() && intervals[i][0] <= e) {\n        s = std::min(s, intervals[i][0]);\n        e = std::max(e, intervals[i][1]);\n        ++i;\n    }\n    out.push_back({s, e});\n    while (i < intervals.size()) out.push_back(intervals[i++]);\n    return out;\n}\n",
    ["Intervals that end before `add` starts come first and are copied.", "Every interval that starts at or before the growing end is absorbed into `add`.", "The three loops share one index, so the work is $O(n)$."])

# starter checks: every starter must fail at least one test (python ones by running)
for did, d in drills.items():
    if d.get('language') == 'cpp':
        continue
    ns = {}
    exec(d['starter'], ns)
    nf = sum(1 for t in d['tests'] if not (eval(t['call'], ns) == eval(t['expect'])))
    assert nf >= 1, did
    ns = {}
    exec(d['solution'], ns)
    import time
    for t in d['tests']:
        t0 = time.time()
        assert eval(t['call'], ns) == eval(t['expect']), (did, t['call'][:80])
        assert time.time() - t0 < 2, (did, t['call'][:60])
    print(did, 'starter fails', nf, 'of', len(d['tests']), '; solution passes all')

idx_path = ROOT + 'index.json'
idx = json.load(open(idx_path))
have = {r['id'] for r in idx}
for did, d in drills.items():
    with open(ROOT + did + '.json', 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')
    if did not in have:
        idx.append({"id": did, "name": d['name'], "course": "coding-int", "difficulty": d['difficulty']})
with open(idx_path, 'w') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('wrote', len(drills), 'drills')
