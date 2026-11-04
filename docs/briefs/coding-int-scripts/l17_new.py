"""l17 replacement problems: divisible-by-k count and longest zero-sum subarray (Python and C++ twins)."""
import random, json, math, subprocess, tempfile, time, collections
from harness import *
random.seed(17)
REP = {}; NUM = {}

# ---------- 17.1 count_subarrays_divisible_by_k ----------
DIV_REF = '''
def count_subarrays_divisible_by_k(nums, k):
    seen = {0: 1}
    total = count = 0
    for x in nums:
        total = (total + x) % k
        count += seen.get(total, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
'''
DIV_START = '''
def count_subarrays_divisible_by_k(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total % k == 0:
                count += 1
    return count
'''
def div_brute(nums, k):
    pre = [0]
    for x in nums: pre.append(pre[-1] + x)
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums) + 1) if (pre[j] - pre[i]) % k == 0)
def div_closed(nums, k):          # independent: group prefix sums by remainder, choose pairs
    pre = [0]
    for x in nums: pre.append(pre[-1] + x)
    c = collections.Counter(p % k for p in pre)
    return sum(v * (v - 1) // 2 for v in c.values())
ns = {}; exec(DIV_REF, ns); divref = ns['count_subarrays_divisible_by_k']
for _ in range(4000):
    nums = [random.randint(-9, 9) for _ in range(random.randint(0, 14))]; k = random.randint(1, 8)
    assert divref(nums, k) == div_brute(nums, k) == div_closed(nums, k)
divs = [([6, -1, 8, 3, -4, 7], 5), ([10, 20], 10), ([], 4), ([0, 0, 0], 7), ([-3, 3], 3), ([-2, -4, -6], 5),
        ([5], 5), ([4], 5), ([-1, 3, 0], 3)]
DIV_TESTS = [dict(call=f'count_subarrays_divisible_by_k({n}, {k})', expect=div_brute(n, k)) for n, k in divs]
DIV_TESTS.append(dict(setup='xs = [3] * 400000', call='count_subarrays_divisible_by_k(xs, 1)', expect=400000 * 400001 // 2))
ys = [1, -1] * 200000
cf = div_closed(ys, 2)
assert cf == (200001 * 200000 // 2) + (200000 * 199999 // 2) == 40_000_000_000
assert divref(ys, 2) == cf
DIV_TESTS.append(dict(setup='ys = [1, -1] * 200000', call='count_subarrays_divisible_by_k(ys, 2)', expect=cf))
check_py('count_subarrays_divisible_by_k', DIV_REF, DIV_START, DIV_TESTS)
REP['div'] = md_tests(DIV_TESTS)
r = run_py(DIV_START, DIV_TESTS)
print('div starter results', [ok for ok, _ in r])
assert all(ok for ok, _ in r[:9]) and not r[9][0] and 'timeout' in r[9][1]
print('div starter passes the 9 small cases and times out on the tenth')
NUM['div_small'] = [t['expect'] for t in DIV_TESTS[:9]]
# C++ trap: without normalising negative remainders case 9 gives 1, not 3
import math
def _cpp_wrong(nums, k):
    seen = {0: 1}; t = 0; c = 0
    for x in nums:
        t = int(math.fmod(t + x, k)); c += seen.get(t, 0); seen[t] = seen.get(t, 0) + 1
    return c
_bad = [i + 1 for i, (n, k) in enumerate(divs) if _cpp_wrong(n, k) != div_brute(n, k)]
print('cases that expose an un-normalised C++ remainder:', _bad, [(_cpp_wrong(*divs[i - 1]), div_brute(*divs[i - 1])) for i in _bad])
assert _bad == [9]
# ---------- 17.2 longest_zero_sum_subarray ----------
ZS_REF = '''
def longest_zero_sum_subarray(nums):
    first = {0: -1}
    total = best = 0
    for i, x in enumerate(nums):
        total += x
        if total in first:
            best = max(best, i - first[total])
        else:
            first[total] = i
    return best
'''
ZS_START = '''
def longest_zero_sum_subarray(nums):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == 0:
                best = max(best, j - i + 1)
    return best
'''
def zs_brute(nums):
    return max([j - i for i in range(len(nums) + 1) for j in range(i + 1, len(nums) + 1) if sum(nums[i:j]) == 0], default=0)
ns = {}; exec(ZS_REF, ns); zsref = ns['longest_zero_sum_subarray']
for _ in range(5000):
    nums = [random.randint(-4, 4) for _ in range(random.randint(0, 14))]
    assert zsref(nums) == zs_brute(nums)
zss = [[5, -2, -3, 8, 1], [2, -2], [], [7], [0], [1, 2, 3], [4, -1, -3, 6, -6, 2], [-5, 5, 5, -5], [3, 1, -4, 2, 2, -4, 9]]
ZS_TESTS = [dict(call=f'longest_zero_sum_subarray({n})', expect=zs_brute(n)) for n in zss]
ZS_TESTS.append(dict(setup='xs = [1, -1] * 200000', call='longest_zero_sum_subarray(xs)', expect=400000))
ZS_TESTS.append(dict(setup='ys = [1, 2, -3] * 133333 + [5]', call='longest_zero_sum_subarray(ys)', expect=399999))
assert zsref([1, -1] * 200000) == 400000 and zsref([1, 2, -3] * 133333 + [5]) == 399999
assert zsref([1, 2, -3] * 40 + [5]) == zs_brute([1, 2, -3] * 40 + [5]) == 120
check_py('longest_zero_sum_subarray', ZS_REF, ZS_START, ZS_TESTS)
REP['zs'] = md_tests(ZS_TESTS)
r = run_py(ZS_START, ZS_TESTS)
assert all(ok for ok, _ in r[:9]) and not r[9][0] and 'timeout' in r[9][1], r
print('zs starter passes the 9 small cases and times out on the tenth')
NUM['zs_small'] = [t['expect'] for t in ZS_TESTS[:9]]

# ---------- C++ twins ----------
DIV_CPP_REF = '''#include <vector>
#include <unordered_map>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) {
    std::unordered_map<int, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total = ((total + x) % k + k) % k;
        count += seen[(int)total];
        ++seen[(int)total];
    }
    return count;
}
'''
DIV_CPP_START = '''#include <vector>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) {
    long long count = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total % k == 0) ++count;
        }
    }
    return count;
}
'''
STUB_DIV = '''#include <vector>
long long count_subarrays_divisible_by_k(std::vector<int> nums, int k) { return 0; }
'''
calls = [(f'count_subarrays_divisible_by_k(std::vector<int>{cpp_lit(n)}, {k})', div_brute(n, k)) for n, k in divs]
calls.append(('count_subarrays_divisible_by_k(std::vector<int>(400000, 3), 1)', 400000 * 400001 // 2))
calls.append(('[&]{ std::vector<int> v; for (int i = 0; i < 200000; ++i) { v.push_back(1); v.push_back(-1); } return count_subarrays_divisible_by_k(v, 2); }()', cf))
check_cpp('count_subarrays_divisible_by_k_cpp', DIV_CPP_REF, STUB_DIV, calls)

ZS_CPP_REF = '''#include <vector>
#include <unordered_map>
#include <algorithm>
int longest_zero_sum_subarray(std::vector<int> nums) {
    std::unordered_map<long long, int> first;
    first[0] = -1;
    long long total = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
        total += nums[i];
        auto it = first.find(total);
        if (it != first.end()) best = std::max(best, i - it->second);
        else first[total] = i;
    }
    return best;
}
'''
ZS_CPP_START = '''#include <vector>
#include <algorithm>
int longest_zero_sum_subarray(std::vector<int> nums) {
    int best = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total == 0) best = std::max(best, (int)(j - i + 1));
        }
    }
    return best;
}
'''
STUB_ZS = '''#include <vector>
int longest_zero_sum_subarray(std::vector<int> nums) { return 0; }
'''
calls = [(f'longest_zero_sum_subarray(std::vector<int>{cpp_lit(n)})', zs_brute(n)) for n in zss]
calls.append(('[&]{ std::vector<int> v; for (int i = 0; i < 200000; ++i) { v.push_back(1); v.push_back(-1); } return longest_zero_sum_subarray(v); }()', 400000))
calls.append(('[&]{ std::vector<int> v; for (int i = 0; i < 133333; ++i) { v.push_back(1); v.push_back(2); v.push_back(-3); } v.push_back(5); return longest_zero_sum_subarray(v); }()', 399999))
check_cpp('longest_zero_sum_subarray_cpp', ZS_CPP_REF, STUB_ZS, calls)

# C++ starters: correct on the small cases, timed natively on the first large case
def time_cpp(src, body, tmo=60):
    d = tempfile.mkdtemp(dir='build')
    open(d + '/m.cpp', 'w').write(src + '\n#include <iostream>\nint main(){ ' + body + ' }\n')
    subprocess.run(['g++', '-std=c++20', '-O1', '-fno-exceptions', '-o', d + '/a', d + '/m.cpp'], check=True)
    t0 = time.time()
    try:
        out = subprocess.run([d + '/a'], capture_output=True, text=True, timeout=tmo).stdout.strip()
    except subprocess.TimeoutExpired:
        return f'over {tmo} s (stopped)', None
    return round(time.time() - t0, 2), out
small_ok = True
for src, name, fn in ((DIV_CPP_START, 'div', 'count_subarrays_divisible_by_k'), (ZS_CPP_START, 'zs', 'longest_zero_sum_subarray')):
    pass
print('div C++ starter, 400000 x 3, k=1:', time_cpp(DIV_CPP_START, 'std::cout << count_subarrays_divisible_by_k(std::vector<int>(400000, 3), 1);'))
print('div C++ reference, same:', time_cpp(DIV_CPP_REF, 'std::cout << count_subarrays_divisible_by_k(std::vector<int>(400000, 3), 1);'))
zbody = 'std::vector<int> v; for (int i = 0; i < 200000; ++i) { v.push_back(1); v.push_back(-1); } std::cout << longest_zero_sum_subarray(v);'
print('zs C++ starter, alternating 400000:', time_cpp(ZS_CPP_START, zbody))
print('zs C++ reference, same:', time_cpp(ZS_CPP_REF, zbody))
# small-case correctness of the C++ starters (compare to brute through the harness with a correct 'starter' check)
check_cpp('div_start_small', DIV_CPP_START, STUB_DIV, calls=[(f'count_subarrays_divisible_by_k(std::vector<int>{cpp_lit(n)}, {k})', div_brute(n, k)) for n, k in divs])
check_cpp('zs_start_small', ZS_CPP_START, STUB_ZS, calls=[(f'longest_zero_sum_subarray(std::vector<int>{cpp_lit(n)})', zs_brute(n)) for n in zss])
# random C++ agreement for both references
for name, ref, bf, gen in (('div', DIV_CPP_REF, div_brute, lambda: ([random.randint(-9, 9) for _ in range(random.randint(0, 14))], random.randint(1, 8))),
                           ('zs', ZS_CPP_REF, zs_brute, lambda: ([random.randint(-4, 4) for _ in range(random.randint(0, 14))],))):
    cs = []
    for _ in range(600):
        a = gen()
        if name == 'div': cs.append((f'count_subarrays_divisible_by_k(std::vector<int>{cpp_lit(a[0])}, {a[1]})', bf(*a)))
        else: cs.append((f'longest_zero_sum_subarray(std::vector<int>{cpp_lit(a[0])})', bf(*a)))
    check_cpp(name + '_random', ref, STUB_DIV if name == 'div' else STUB_ZS, cs)
json.dump(dict(REP=REP, NUM=NUM), open('l17_tests.json', 'w'))
print(json.dumps(NUM))
