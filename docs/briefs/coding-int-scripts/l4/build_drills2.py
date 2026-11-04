"""coding-int level 4: four more drills, so that prefix-sums and hashing each have two drills in each language (a session needs two).
Run after build_drills.py: python3 -I build_drills2.py"""
import json, random, time

ROOT = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/app/content/drills/'
rnd = random.Random(20261105)


def py_drill(did, name, pattern, tags, diff, pace, fn, returns, brief, cons, hint, starter, examples, tests, solution, notes):
    return {"id": did, "name": name, "course": "coding-int", "pack": "ci", "pattern": pattern, "tags": tags, "skills": ["ci-patterns", "ci-timed"],
            "difficulty": diff, "pace": pace, "fn": fn, "returns": returns, "brief": brief, "constraints": cons, "hint": hint,
            "starter": starter, "examples": examples, "tests": tests,
            "how": f"Submit runs {len(tests)} hidden tests. Each answer must equal the expected value.",
            "solution": solution, "notes": notes}


def cpp_drill(did, name, pattern, tags, diff, pace, brief, cons, hint, starter, examples, tests, solution, notes):
    return {"id": did, "name": name, "course": "coding-int", "pack": "ci", "language": "cpp", "pattern": pattern, "tags": tags, "skills": ["ci-patterns", "ci-timed"],
            "difficulty": diff, "pace": pace, "brief": brief, "constraints": cons, "hint": hint, "starter": starter,
            "examples": examples, "tests": tests, "how": f"Submit runs {len(tests)} hidden tests. Each answer must equal the expected value.",
            "solution": solution, "notes": notes}


def pyc(call, expect, note=None):
    d = {"call": call, "expect": repr(expect), "compare": "equal"}
    if note:
        d["note"] = note
    return d


def cppc(fn, args, types, expect, note=None):
    d = {"call": fn, "args": args, "types": types, "expect": expect, "compare": "equal"}
    if note:
        d["note"] = note
    return d


# ---- references and brute forces
def split_ref(nums):
    total = sum(nums)
    left = count = 0
    for x in nums[:-1]:
        left += x
        if left * 2 == total:
            count += 1
    return count


def split_brute(nums):
    return sum(1 for i in range(1, len(nums)) if sum(nums[:i]) == sum(nums[i:]))


def ds(n):
    return sum(int(c) for c in str(n))


def dsp_ref(nums):
    best = {}
    ans = -1
    for x in nums:
        k = ds(x)
        if k in best:
            ans = max(ans, best[k] + x)
        best[k] = max(best.get(k, 0), x)
    return ans


def dsp_brute(nums):
    ans = -1
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if ds(nums[i]) == ds(nums[j]):
                ans = max(ans, nums[i] + nums[j])
    return ans


def dsp_sorted(nums):
    """second method: group by digit sum, sort, take the top two of each group"""
    groups = {}
    for x in nums:
        groups.setdefault(ds(x), []).append(x)
    best = -1
    for g in groups.values():
        if len(g) > 1:
            g.sort()
            best = max(best, g[-1] + g[-2])
    return best


def rq_brute(nums, qs):
    return [sum(nums[l:r + 1]) for l, r in qs]


def sp_brute(nums, t):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] + nums[j] == t)


def sp_ref(nums, t):
    seen = {}
    c = 0
    for x in nums:
        c += seen.get(t - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return c


for _ in range(3000):
    a = [rnd.randint(-4, 6) for _ in range(rnd.randint(0, 10))]
    assert split_ref(a) == split_brute(a), a
    b = [rnd.randint(1, 120) for _ in range(rnd.randint(0, 9))]
    assert dsp_ref(b) == dsp_brute(b) == dsp_sorted(b), b
    t = rnd.randint(-3, 10)
    assert sp_ref(a, t) == sp_brute(a, t)
print('references agree')

drills = {}

# 1 Python, prefix-sums, d3: split points
small = [[], [5], [0, 0], [2, 2], [3, 1, 2], [5, -5, 5, -5, 5, -5], [0, 0, 0, 0], [6, -2, 4, 0, 0, 1, 3], [1, 1, 1, 1, 1, 1], [-3, 3, -3, 3, -3, 3], [9, 4, -13, 5, 8], [4, 1, 3, 4, 0, 4]]
tests = [pyc(f"count_split_points({n!r})", split_brute(n)) for n in small]
assert split_ref([0] * 200000) == 199999
assert split_ref([5, -5] * 100000) == 99999
tests.append(pyc("count_split_points([0] * 200000)", 199999))
tests.append(pyc("count_split_points([5, -5] * 100000)", 99999))
ex = [pyc("count_split_points([5, -5, 5, -5, 5, -5])", 2, "The total is 0. The left part sums to 0 after two numbers and after four, so there are two cuts."),
      pyc("count_split_points([5])", 0, "A single number has no place to cut.")]
for e in ex:
    assert eval(e['call'], {'count_split_points': split_ref}) == eval(e['expect'])
drills['ci-split-points'] = py_drill(
    'ci-split-points', 'Cuts with equal sums', 'prefix-sums', ['split-points'], 3, 900, 'count_split_points', 'a whole number',
    "`nums` is a list of whole numbers, which may be negative or zero. A cut is a place between two neighbours, so a list of `n` numbers has `n - 1` cuts. Count the cuts where the numbers to the left sum to the same as the numbers to the right.\n\nWrite `count_split_points(nums)`.\n\nExample. For `nums = [3, 1, 2]` the cut after the 3 gives 3 and 3, so the answer is 1.",
    ["$0 \\le n \\le 200{,}000$ entries, each between -1,000 and 1,000.", "$O(n)$ time is the target. Summing both sides at every cut is too slow.", "All tests share a 5-second time limit."],
    "Find the total once. Then walk along with a running left sum. A cut works when the left sum is exactly half the total.",
    "def count_split_points(nums):\n    # your code here\n    return 0\n", ex, tests,
    "def count_split_points(nums):\n    total = sum(nums)\n    left = count = 0\n    for x in nums[:-1]:\n        left += x\n        if left * 2 == total:\n            count += 1\n    return count\n",
    ["The right side is the total minus the left side, so equal sides mean the left is half the total.", "Compare `2 * left` with the total, so no fraction appears.", "Two passes over the list, so the work is $O(n)$."])

# 2 Python, hashing, d3: digit sum pairs
small = [[], [7], [18, 43, 36, 13, 7], [51, 71, 17, 42], [39, 93, 12, 48, 84], [5, 5], [10, 100, 1000], [123, 321, 213, 99], [64, 28, 46, 19, 91], [8, 17, 26, 35, 44, 53]]
tests = [pyc(f"largest_digit_sum_pair({n!r})", dsp_brute(n)) for n in small]
big = list(range(1, 200001))
assert dsp_ref(big) == dsp_sorted(big)
tests.append(pyc("largest_digit_sum_pair(list(range(1, 200001)))", dsp_ref(big)))
big2 = [10 ** 9 - 1 - 9 * i for i in range(100000)]
assert dsp_ref(big2) == dsp_sorted(big2)
tests.append(pyc("largest_digit_sum_pair([10 ** 9 - 1 - 9 * i for i in range(100000)])", dsp_ref(big2)))
ex = [pyc("largest_digit_sum_pair([18, 43, 36, 13, 7])", 54, "The digit sums are 9, 7, 9, 4 and 7. The pair 18 and 36 gives 54, and 43 and 7 gives 50."),
      pyc("largest_digit_sum_pair([7])", -1, "One number has no partner.")]
for e in ex:
    assert eval(e['call'], {'largest_digit_sum_pair': dsp_ref}) == eval(e['expect'])
print('digit pair big', dsp_ref(big), dsp_ref(big2))
drills['ci-same-total-pairs'] = py_drill(
    'ci-same-total-pairs', 'Pairs with equal digit sums', 'hashing', ['digit-sum-pairs'], 3, 1200, 'largest_digit_sum_pair', 'a whole number',
    "`nums` is a list of positive whole numbers. Find two numbers at different positions whose digits add up to the same total, and return the largest sum of such a pair. Return -1 if no two numbers share a digit sum.\n\nWrite `largest_digit_sum_pair(nums)`.\n\nExample. For `nums = [18, 43, 36, 13, 7]` the numbers 18 and 36 both have digit sum 9, so the answer is 54.",
    ["$0 \\le n \\le 200{,}000$ entries, each between 1 and $10^9$.", "$O(n)$ time is the target. Comparing every pair is too slow.", "All tests share a 5-second time limit."],
    "Use the digit sum as a dict key. Store the largest number seen for each key. When a new number arrives, a stored partner under the same key gives a candidate.",
    "def largest_digit_sum_pair(nums):\n    # your code here\n    return -1\n", ex, tests,
    "def largest_digit_sum_pair(nums):\n    best = {}\n    answer = -1\n    for x in nums:\n        key = sum(int(c) for c in str(x))\n        if key in best:\n            answer = max(answer, best[key] + x)\n        best[key] = max(best.get(key, 0), x)\n    return answer\n",
    ["Only the largest number seen under a key can make the best pair with a later number.", "Each number is looked up and stored once, so the work is $O(n)$ digit sums.", "Keep the answer at -1 until some key repeats."])

# 3 C++, prefix-sums, d3: range sums
T = ["std::vector<int>", "std::vector<std::vector<int>>"]
small = [([5], [[0, 0]]), ([1, 2, 3, 4], [[0, 3], [1, 2], [2, 2]]), ([-2, 5, -1, 4], [[0, 1], [1, 3], [0, 3]]), ([0, 0, 0], [[0, 2]]), ([7, -7, 7], [[0, 1], [1, 2], [0, 2]]),
         ([3, 1, 4, 1, 5, 9, 2, 6], [[2, 5], [0, 7], [7, 7], [3, 4]]), ([10, -3, 8], [[1, 1], [0, 0], [2, 2]]), ([100, 200, 300, -50], [[3, 3], [0, 3]])]
tests = [cppc("range_sums", [n, q], T, rq_brute(n, q)) for n, q in small]
big_ones = [1] * 200000
assert 200000 * 200000 == 40000000000
tests.append({"call": "[&]{ std::vector<int> v(200000, 1); std::vector<std::vector<int>> q(200000, std::vector<int>{0, 199999}); long long t = 0; for (long long s : range_sums(v, q)) t += s; return t; }()", "expect": 40000000000, "compare": "equal"})
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 100000; ++i) v.push_back(i % 3 - 1); std::vector<std::vector<int>> q; for (int i = 0; i < 100000; ++i) q.push_back({i, 99999}); long long t = 0; for (long long s : range_sums(v, q)) t += s; return t; }()", "expect": None, "compare": "equal"})
vv = [i % 3 - 1 for i in range(100000)]
pref = [0]
for x in vv:
    pref.append(pref[-1] + x)
exp2 = sum(pref[100000] - pref[i] for i in range(100000))
# second method: direct sum of suffixes
suf = 0
tot = 0
for i in range(99999, -1, -1):
    suf += vv[i]
    tot += suf
assert tot == exp2
tests[-1]["expect"] = exp2
ex = [cppc("range_sums", [[1, 2, 3, 4], [[0, 3], [1, 2]]], T, [10, 5], "The first query sums all four numbers. The second sums 2 and 3."),
      cppc("range_sums", [[5], [[0, 0]]], T, [5], "A query of one place is that number.")]
for e in ex:
    assert rq_brute(*e['args']) == e['expect']
print('range sums big', exp2)
drills['ci-cpp-range-sums'] = cpp_drill(
    'ci-cpp-range-sums', 'Many range sums', 'prefix-sums', ['range-sums'], 3, 900,
    "`nums` is a list of whole numbers. Each query `{l, r}` asks for the sum of `nums[l]` to `nums[r]`, both included, counting from 0. Write `range_sums(nums, queries)`, which returns the sums as a `std::vector<long long>`, one per query, in order.",
    ["$1 \\le n \\le 200{,}000$ numbers, each between -1,000 and 1,000, and up to 200,000 queries.", "$O(n + q)$ time is the target. Summing each range afresh is too slow.", "Each test has a 5-second limit. Sums can pass $2 \\times 10^9$, so use `long long`."],
    "Build the prefix sums once, with a leading 0. Then the sum of a range is one prefix minus another.",
    "#include <vector>\n\nstd::vector<long long> range_sums(std::vector<int> nums, std::vector<std::vector<int>> queries) {\n    // your code here\n    return {};\n}\n", ex, tests,
    "#include <vector>\n\nstd::vector<long long> range_sums(std::vector<int> nums, std::vector<std::vector<int>> queries) {\n    std::vector<long long> prefix(nums.size() + 1, 0);\n    for (size_t i = 0; i < nums.size(); ++i) prefix[i + 1] = prefix[i] + nums[i];\n    std::vector<long long> out;\n    for (const auto& q : queries) out.push_back(prefix[q[1] + 1] - prefix[q[0]]);\n    return out;\n}\n",
    ["`prefix[i]` holds the sum of the first `i` numbers, so `prefix[0]` is 0.", "The range from `l` to `r` is `prefix[r + 1] - prefix[l]`.", "One pass to build the table and one per query, so the work is $O(n + q)$."])

# 4 C++, hashing, d3: pairs with a sum
T1 = ["std::vector<int>", "int"]
small = [([], 4), ([3], 3), ([1, 2, 3, 4], 5), ([2, 2, 2], 4), ([5, -1, 6, 0, -6, 1], 0), ([4, 4, 4, 4], 8), ([1, 5, 7, -1, 5], 6), ([-3, -3, 6, 0], 0), ([9, 1, 8, 2, 7, 3], 10), ([0, 0, 0, 0, 0], 0)]
tests = [cppc("count_pairs_with_sum", [n, t], T1, sp_brute(n, t)) for n, t in small]
assert sp_ref([7] * 180000, 14) == 180000 * 179999 // 2 == 16199910000
cl = [i % 1000 for i in range(100000)]
assert sp_ref(cl, 1000) == 499 * 100 * 100 + 100 * 99 // 2 == 4994950
tests.append({"call": "count_pairs_with_sum(std::vector<int>(180000, 7), 14)", "expect": 16199910000, "compare": "equal"})
tests.append({"call": "[&]{ std::vector<int> v; for (int i = 0; i < 100000; ++i) v.push_back(i % 1000); return count_pairs_with_sum(v, 1000); }()", "expect": 4994950, "compare": "equal"})
ex = [cppc("count_pairs_with_sum", [[1, 2, 3, 4], 5], T1, 2, "The pairs 1 and 4, and 2 and 3, sum to 5."),
      cppc("count_pairs_with_sum", [[2, 2, 2], 4], T1, 3, "Any two of the three 2s make a pair, and there are three ways to choose two.")]
for e in ex:
    assert sp_brute(*e['args']) == e['expect']
drills['ci-cpp-sum-pairs'] = cpp_drill(
    'ci-cpp-sum-pairs', 'Pairs that reach a target', 'hashing', ['sum-pairs'], 3, 1200,
    "`nums` is a list of whole numbers and `target` is a whole number. Write `count_pairs_with_sum(nums, target)`, which returns the number of pairs of positions `i < j` with `nums[i] + nums[j] == target`. Equal values at different positions count separately. The answer needs a `long long`.",
    ["$0 \\le n \\le 180{,}000$ entries, each between -1,000,000 and 1,000,000.", "$O(n)$ expected time is the target. Checking every pair is too slow.", "Each test has a 5-second limit."],
    "Keep a hash map of how many times each value has been seen. For each new value `x`, add the count of `target - x`, then record `x`.",
    "#include <vector>\n#include <unordered_map>\n\nlong long count_pairs_with_sum(std::vector<int> nums, int target) {\n    // your code here\n    return 0;\n}\n", ex, tests,
    "#include <vector>\n#include <unordered_map>\n\nlong long count_pairs_with_sum(std::vector<int> nums, int target) {\n    std::unordered_map<int, long long> seen;\n    long long count = 0;\n    for (int x : nums) {\n        auto it = seen.find(target - x);\n        if (it != seen.end()) count += it->second;\n        ++seen[x];\n    }\n    return count;\n}\n",
    ["Each new value pairs with every earlier value equal to `target - x`.", "Looking up before recording stops a value pairing with itself.", "One pass with a hash map, so the work is $O(n)$."])

for did, d in drills.items():
    if d.get('language') == 'cpp':
        continue
    ns = {}
    exec(d['starter'], ns)
    nf = sum(1 for t in d['tests'] if not (eval(t['call'], ns) == eval(t['expect'])))
    assert nf >= 1, did
    ns = {}
    exec(d['solution'], ns)
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
