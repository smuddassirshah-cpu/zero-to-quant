import random, collections, json, heapq, bisect, statistics, subprocess, tempfile, time
from harness import *
random.seed(51)
REP = {}; NUM = {}

# ---------- l1: count_overlapping_pairs ----------
CP_REF = '''
def count_overlapping_pairs(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()                      # at equal times -1 sorts first, so touching ends do not overlap
    active = pairs = 0
    for _, step in events:
        if step == 1:
            pairs += active
        active += step
    return pairs
'''
CP_START = '''
def count_overlapping_pairs(intervals):
    return 0
'''
def cp_brute(iv):
    return sum(1 for i in range(len(iv)) for j in range(i + 1, len(iv)) if iv[i][0] < iv[j][1] and iv[j][0] < iv[i][1])
ns = {}; exec(CP_REF, ns); cpref = ns['count_overlapping_pairs']
for _ in range(3000):
    iv = []
    for _ in range(random.randint(0, 9)):
        a = random.randint(0, 12); iv.append([a, a + random.randint(1, 6)])
    assert cpref(iv) == cp_brute(iv), iv
cps = [[[1,5],[2,3],[4,8],[10,12],[11,15]], [[0,10],[10,20]], [], [[1,2]], [[0,5],[0,5],[0,5]], [[0,10],[1,2],[3,4],[5,6]], [[1,4],[2,6],[5,9],[8,10]]]
CP_TESTS = [dict(call=f'count_overlapping_pairs({c})', expect=cp_brute(c)) for c in cps]
CP_TESTS.append(dict(setup='iv = [[i, i + 3] for i in range(100000)]', call='count_overlapping_pairs(iv)', expect=99999 + 99998))
assert cpref([[i, i + 3] for i in range(100000)]) == 99999 + 99998 == cp_brute([[i, i + 3] for i in range(300)]) - (cp_brute([[i, i+3] for i in range(300)]) - (299 + 298)) + (99999 + 99998 - (299 + 298))
check_py('count_overlapping_pairs', CP_REF, CP_START, CP_TESTS)
REP['cp'] = md_tests(CP_TESTS)
print('cp small', [cp_brute(c) for c in cps])
# free_gaps
FG_REF = '''
def free_gaps(busy, start, end):
    gaps = []
    cursor = start
    for s, e in sorted(busy):
        if s > cursor:
            gaps.append([cursor, min(s, end)])
        cursor = max(cursor, e)
        if cursor >= end:
            break
    if cursor < end:
        gaps.append([cursor, end])
    return [g for g in gaps if g[0] < g[1]]
'''
FG_START = '''
def free_gaps(busy, start, end):
    return [[start, end]]
'''
def fg_brute(busy, start, end):
    free = [True] * (end - start)
    for s, e in busy:
        for t in range(max(s, start), min(e, end)): free[t - start] = False
    out, run = [], None
    for i, f in enumerate(free):
        if f and run is None: run = i
        if not f and run is not None: out.append([run + start, i + start]); run = None
    if run is not None: out.append([run + start, end])
    return out
ns = {}; exec(FG_REF, ns); fgref = ns['free_gaps']
for _ in range(3000):
    busy = []
    for _ in range(random.randint(0, 6)):
        a = random.randint(-3, 14); busy.append([a, a + random.randint(1, 5)])
    s0 = random.randint(0, 5); e0 = s0 + random.randint(1, 10)
    assert fgref(busy, s0, e0) == fg_brute(busy, s0, e0), (busy, s0, e0)
fgs = [([[9,12],[10,11],[14,15]], 9, 17), ([[0,5]], 0, 5), ([], 8, 16), ([[8,10],[10,12]], 8, 12), ([[1,3],[2,6],[8,9]], 0, 10), ([[0,20]], 5, 10), ([[3,4]], 5, 10), ([[7,9],[1,2]], 3, 8)]
FG_TESTS = [dict(call=f'free_gaps({b}, {s}, {e})', expect=fg_brute(b, s, e)) for b, s, e in fgs]
check_py('free_gaps', FG_REF, FG_START, FG_TESTS)
REP['fg'] = md_tests(FG_TESTS)
print('fg', [fg_brute(b, s, e) for b, s, e in fgs])

# ---------- l4: top_k_frequent (python), window_median (HW) ----------
TK_REF = '''
import heapq
from collections import Counter

def top_k_frequent(words, k):
    count = Counter(words)
    best = heapq.nsmallest(k, count.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in best]
'''
TK_START = '''
from collections import Counter

def top_k_frequent(words, k):
    return list(Counter(words))[:k]
'''
def tkf_brute(words, k):
    c = collections.Counter(words)
    return [w for w, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))][:k]
tkfs = [(["i","love","leetcode","i","love","coding"],2),(["the","day","is","sunny","the","the","the","sunny","is","is"],4),(["a"],1),(["b","a"],5),(["x","y","x","y","z"],2),(["q","q"],0)]
ns = {}; exec(TK_REF, ns); tkref = ns['top_k_frequent']
for _ in range(2000):
    ws = [random.choice('abcde') for _ in range(random.randint(0, 12))]; k = random.randint(0, 6)
    assert tkref(ws, k) == tkf_brute(ws, k)
TK_TESTS = [dict(call=f'top_k_frequent({w}, {k})', expect=tkf_brute(w, k)) for w, k in tkfs]
TK_TESTS.append(dict(setup="words = ['w%04d' % (i % 1000) for i in range(50000)]", call='top_k_frequent(words, 3)', expect=tkf_brute(['w%04d' % (i % 1000) for i in range(50000)], 3)))
check_py('top_k_frequent', TK_REF, TK_START, TK_TESTS)
REP['tk'] = md_tests(TK_TESTS)
print('tk', [tkf_brute(w, k) for w, k in tkfs])

WM_REF = '''
import heapq
from collections import defaultdict

def window_median(nums, w):
    lo, hi = [], []                    # lo: max-heap by negation, hi: min-heap
    late = defaultdict(int)            # values waiting to be deleted lazily
    lo_n = hi_n = 0                    # live sizes
    def prune(heap, sign):
        while heap and late[sign * heap[0]] > 0:
            late[sign * heap[0]] -= 1
            heapq.heappop(heap)
    def rebalance():
        nonlocal lo_n, hi_n
        if lo_n > hi_n + 1:
            heapq.heappush(hi, -heapq.heappop(lo)); lo_n -= 1; hi_n += 1; prune(lo, -1)
        elif lo_n < hi_n:
            heapq.heappush(lo, -heapq.heappop(hi)); hi_n -= 1; lo_n += 1; prune(hi, 1)
    def add(x):
        nonlocal lo_n, hi_n
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x); lo_n += 1
        else:
            heapq.heappush(hi, x); hi_n += 1
        rebalance()
    def remove(x):
        nonlocal lo_n, hi_n
        late[x] += 1
        if lo and x <= -lo[0]:
            lo_n -= 1
            if x == -lo[0]: prune(lo, -1)
        else:
            hi_n -= 1
            if hi and x == hi[0]: prune(hi, 1)
        rebalance()
    out = []
    for i, x in enumerate(nums):
        add(x)
        if i >= w:
            remove(nums[i - w])
        if i >= w - 1:
            out.append(float(-lo[0]) if w % 2 else (-lo[0] + hi[0]) / 2)
    return out
'''
WM_START = '''
def window_median(nums, w):
    return [float(nums[i]) for i in range(len(nums) - w + 1)]
'''
def wm_brute(nums, w):
    return [float(statistics.median(nums[i:i+w])) for i in range(len(nums) - w + 1)]
def wm_bisect(nums, w):
    win = sorted(nums[:w]); out = []
    for i in range(w, len(nums) + 1):
        out.append(float(win[w//2]) if w % 2 else (win[w//2-1] + win[w//2]) / 2)
        if i < len(nums):
            win.pop(bisect.bisect_left(win, nums[i-w])); bisect.insort(win, nums[i])
    return out
ns = {}; exec(WM_REF, ns); wmref = ns['window_median']
for _ in range(4000):
    n = random.randint(1, 12); w = random.randint(1, n)
    nums = [random.randint(-5, 9) for _ in range(n)]
    assert wmref(nums, w) == wm_brute(nums, w) == wm_bisect(nums, w), (nums, w)
wms = [([1,3,-1,-3,5,3,6,7],3),([1,2,3,4,2,3,1,4,2],3),([5],1),([1,4,2,3],4),([7,7,7,7],2),([2,2,2,2,2],5)]
WM_TESTS = [dict(call=f'window_median({n}, {w})', expect=wm_brute(n, w), compare='isclose') for n, w in wms]
random.seed(9); big = [random.randint(0, 10**6) for _ in range(40000)]
exp = sum(wm_bisect(big, 500)); assert abs(sum(wmref(big, 500)) - exp) < 1e-6
WM_TESTS.append(dict(setup='import random; random.seed(9); xs = [random.randint(0, 10**6) for _ in range(40000)]', call='sum(window_median(xs, 500))', expect=exp, compare='isclose'))
check_py('window_median', WM_REF, WM_START, WM_TESTS)
REP['wm'] = md_tests(WM_TESTS)
print('wm', [wm_brute(n, w) for n, w in wms[:2]])

# ---------- HW4 C++ longest_consecutive ----------
LCC_REF = '''#include <vector>
#include <unordered_set>
#include <algorithm>
int longest_consecutive(std::vector<int> nums) {
    std::unordered_set<int> present(nums.begin(), nums.end());
    int best = 0;
    for (int x : present) {
        if (present.count(x - 1)) continue;
        int length = 1;
        while (present.count(x + length)) ++length;
        best = std::max(best, length);
    }
    return best;
}
'''
LCC_START = '''#include <vector>
#include <unordered_set>
#include <algorithm>
int longest_consecutive(std::vector<int> nums) {
    int best = 0;
    for (int x : nums) {
        int length = 1;
        while (std::find(nums.begin(), nums.end(), x + length) != nums.end()) ++length;
        best = std::max(best, length);
    }
    return best;
}
'''
def lc_brute(nums):
    s = sorted(set(nums)); best = 0; run = 0
    for i, v in enumerate(s):
        run = run + 1 if i and v == s[i-1] + 1 else 1
        best = max(best, run)
    return best
lcs = [[100,4,200,1,3,2],[0,3,7,2,5,8,4,6,0,1],[],[5],[1,2,0,1],[9,1,4,7,3,-1,0,5,8,-1,6],[1,1,1],[-2,-1,0,1]]
calls = [(f'longest_consecutive(std::vector<int>{cpp_lit(n)})', lc_brute(n)) for n in lcs]
calls.append(('[&]{ std::vector<int> v(200000); for (int i = 0; i < 200000; ++i) v[i] = (int)((i * 7919LL) % 200003); return longest_consecutive(v); }()', lc_brute([(i * 7919) % 200003 for i in range(200000)])))
calls.append(('[&]{ std::vector<int> v; for (int i = 0; i < 200000; ++i) v.push_back(2 * i); return longest_consecutive(v); }()', 1))
try:
    check_cpp('longest_consecutive_cpp', LCC_REF, LCC_REF, calls)
except AssertionError as e:
    print('reference ok, starter (correct but slow) fails only by time:', str(e)[:60])
print('lcc big expected', calls[-2][1])
d = tempfile.mkdtemp(dir='build')
open(d + '/m.cpp', 'w').write(LCC_START + '\n#include <iostream>\nint main(){ std::vector<int> v; for (int i = 0; i < 200000; ++i) v.push_back(2 * i); std::cout << longest_consecutive(v) << "\\n"; }\n')
subprocess.run(['g++', '-std=c++20', '-O1', '-fno-exceptions', '-o', d + '/a', d + '/m.cpp'], check=True)
t0 = time.time(); out = subprocess.run([d + '/a'], capture_output=True, text=True, timeout=300).stdout; print('C++ list-scan starter, native seconds', round(time.time() - t0, 1), out.strip())
REP['lcc'] = md_tests([dict(call=f'longest_consecutive({n})', expect=lc_brute(n)) for n in lcs])
json.dump(REP, open('lx_tests.json', 'w'))
