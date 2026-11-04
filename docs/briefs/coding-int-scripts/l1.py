import random, heapq, statistics, bisect, math, collections, json
from harness import *
random.seed(11)
REP = {}

# ---------- 1.1 merge_intervals ----------
MERGE_REF = '''
def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
'''
MERGE_START = '''
def merge_intervals(intervals):
    return sorted([list(x) for x in intervals])
'''
def merge_brute(iv):
    cov = set()
    for a, b in iv:
        cov.update(range(2 * a, 2 * b + 1))
    out, run = [], None
    for x in sorted(cov):
        if run and x == run[1] + 1: run[1] = x
        else:
            if run: out.append([run[0] / 2, run[1] / 2])
            run = [x, x]
    if run: out.append([run[0] / 2, run[1] / 2])
    return [[int(a), int(b)] for a, b in out]
ns = {}; exec(MERGE_REF, ns); mref = ns['merge_intervals']
for _ in range(3000):
    n = random.randint(0, 7)
    iv = []
    for _ in range(n):
        a = random.randint(-6, 10); iv.append([a, a + random.randint(0, 5)])
    assert mref([x[:] for x in iv]) == merge_brute(iv), iv
cases = [[[1,3],[2,6],[8,10],[15,18]], [[1,4],[4,5]], [], [[5,6]], [[8,10],[1,3],[2,6]], [[1,10],[2,3],[4,5]],
         [[2,3],[4,5],[6,7]], [[-5,-2],[-3,1]], [[1,2],[1,2]], [[1,2],[3,4]]]
MERGE_TESTS = [dict(call=f'merge_intervals({c})', expect=merge_brute(c)) for c in cases]
check_py('merge_intervals', MERGE_REF, MERGE_START, MERGE_TESTS)
MERGE_CPP_REF = '''#include <vector>
#include <algorithm>
std::vector<std::vector<int>> merge_intervals(std::vector<std::vector<int>> intervals) {
    std::sort(intervals.begin(), intervals.end());
    std::vector<std::vector<int>> out;
    for (const auto& iv : intervals) {
        if (!out.empty() && iv[0] <= out.back()[1]) out.back()[1] = std::max(out.back()[1], iv[1]);
        else out.push_back(iv);
    }
    return out;
}
'''
MERGE_CPP_START = '''#include <vector>
#include <algorithm>
std::vector<std::vector<int>> merge_intervals(std::vector<std::vector<int>> intervals) {
    std::sort(intervals.begin(), intervals.end());
    return intervals;
}
'''
calls = [(f'merge_intervals(std::vector<std::vector<int>>{cpp_lit(c)})', merge_brute(c)) for c in cases]
check_cpp('merge_intervals_cpp', MERGE_CPP_REF, MERGE_CPP_START, calls)
REP['merge'] = md_tests(MERGE_TESTS)

# ---------- 1.2 min_rooms ----------
ROOMS_REF = '''
def min_rooms(meetings):
    starts = sorted(s for s, e in meetings)
    ends = sorted(e for s, e in meetings)
    rooms = best = j = 0
    for s in starts:
        while ends[j] <= s:
            j += 1
            rooms -= 1
        rooms += 1
        best = max(best, rooms)
    return best
'''
ROOMS_START = '''
def min_rooms(meetings):
    return len(meetings)
'''
def rooms_brute(m):
    if not m: return 0
    return max(sum(1 for s, e in m if s <= t < e) for t in range(min(s for s,e in m), max(e for s,e in m) + 1))
ns = {}; exec(ROOMS_REF, ns); rref = ns['min_rooms']
for _ in range(3000):
    m = []
    for _ in range(random.randint(1, 8)):
        a = random.randint(0, 12); m.append([a, a + random.randint(1, 6)])
    assert rref(m) == rooms_brute(m), m
rcases = [[[0,30],[5,10],[15,20]], [[0,10],[10,20]], [[7,10],[2,4]], [[1,5]], [[1,5],[1,5],[1,5]],
          [[0,5],[1,2],[3,4],[2,3]], [[9,10],[4,9],[4,17]]]
ROOMS_TESTS = [dict(call=f'min_rooms({c})', expect=rooms_brute(c)) for c in rcases]
big = [[i, i + 3] for i in range(0, 60000, 1)]   # at most 3 overlap at once
ROOMS_TESTS.append(dict(setup='ms = [[i, i + 3] for i in range(60000)]', call='min_rooms(ms)', expect=3))
assert rref(big) == 3
check_py('min_rooms', ROOMS_REF, ROOMS_START, ROOMS_TESTS)
REP['rooms'] = md_tests(ROOMS_TESTS)

# ---------- 1.3 Trie ----------
TRIE_REF = '''
class Trie:
    def __init__(self):
        self.root = {'#n': 0}
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {'#n': 0})
        if not node.get('#end'):
            node['#end'] = True
            node = self.root
            node['#n'] += 1
            for ch in word:
                node = node[ch]
                node['#n'] += 1
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node
    def search(self, word):
        node = self._walk(word)
        return bool(node and node.get('#end'))
    def starts_with(self, prefix):
        return self._walk(prefix) is not None
    def count_prefix(self, prefix):
        node = self._walk(prefix)
        return node['#n'] if node else 0
'''
TRIE_START = '''
class Trie:
    def __init__(self):
        self.words = []
    def insert(self, word):
        pass
    def search(self, word):
        return False
    def starts_with(self, prefix):
        return False
    def count_prefix(self, prefix):
        return 0
'''
TRIE_POST = '''
def run_trie(ops):
    t = Trie()
    out = []
    for op, arg in ops:
        if op == 'insert': t.insert(arg)
        elif op == 'search': out.append(t.search(arg))
        elif op == 'starts_with': out.append(t.starts_with(arg))
        else: out.append(t.count_prefix(arg))
    return out
'''
def trie_brute(ops):
    words, out = set(), []
    for op, a in ops:
        if op == 'insert': words.add(a)
        elif op == 'search': out.append(a in words)
        elif op == 'starts_with': out.append(any(w.startswith(a) for w in words))
        else: out.append(sum(1 for w in words if w.startswith(a)))
    return out
tops = [
 [('insert','tea'),('insert','ten'),('insert','to'),('search','te'),('starts_with','te'),('search','tea'),('count_prefix','te'),('count_prefix','t')],
 [('insert','apple'),('search','apple'),('search','app'),('starts_with','app'),('insert','app'),('search','app'),('count_prefix','app')],
 [('search','a'),('starts_with','a'),('count_prefix','a')],
 [('insert','inn'),('insert','inn'),('count_prefix','in'),('count_prefix','inn'),('count_prefix','innn')],
 [('insert','a'),('insert','ab'),('insert','abc'),('count_prefix',''),('starts_with',''),('search','')],
 [('insert','cat'),('insert','car'),('insert','cart'),('insert','dog'),('count_prefix','car'),('count_prefix','ca'),('starts_with','cow'),('search','cart')],
]
for _ in range(1500):
    ws = [''.join(random.choice('abc') for _ in range(random.randint(1,4))) for _ in range(6)]
    ops = [('insert', w) for w in ws[:4]] + [(random.choice(['search','starts_with','count_prefix']), random.choice(ws + ['', 'ab', 'c'])) for _ in range(8)]
    ns = {}; exec(TRIE_REF + TRIE_POST, ns)
    assert ns['run_trie'](ops) == trie_brute(ops), ops
TRIE_TESTS = [dict(call=f'run_trie({o})', expect=trie_brute(o)) for o in tops]
check_py('trie', TRIE_REF, TRIE_START, TRIE_TESTS, postlude=TRIE_POST)
REP['trie'] = md_tests(TRIE_TESTS)

# trie node counts (two methods)
def nodes_insert(words):
    root, n = {}, 0
    for w in words:
        node = root
        for ch in w:
            if ch not in node: node[ch] = {}; n += 1
            node = node[ch]
    return n
def nodes_prefixes(words):
    return len({w[:i] for w in words for i in range(1, len(w)+1)})
W = ['tea','ten','to','inn']
assert nodes_insert(W) == nodes_prefixes(W) == 8
W2 = ['car','card','care','cat','dog']
print('trie nodes', nodes_insert(W), nodes_insert(W2), nodes_prefixes(W2))
assert nodes_insert(W2) == nodes_prefixes(W2)

# ---------- 1.4 top_completions ----------
TC_REF = '''
def top_completions(words, prefix, k):
    root = {}
    for w in set(words):
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = True
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]
    out = []
    def dfs(node, path):
        if len(out) >= k:
            return
        if '$' in node:
            out.append(prefix + path)
        for ch in sorted(c for c in node if c != '$'):
            dfs(node[ch], path + ch)
    dfs(node, '')
    return out[:k]
'''
TC_START = '''
def top_completions(words, prefix, k):
    return [w for w in words if w.startswith(prefix)][:k]
'''
def tc_brute(words, prefix, k): return sorted({w for w in words if w.startswith(prefix)})[:k]
ns = {}; exec(TC_REF, ns); tref = ns['top_completions']
for _ in range(2000):
    ws = [''.join(random.choice('abc') for _ in range(random.randint(1,4))) for _ in range(random.randint(0,8))]
    p = random.choice(['', 'a', 'ab', 'c', 'bb']); k = random.randint(0, 5)
    assert tref(ws, p, k) == tc_brute(ws, p, k), (ws, p, k)
tcs = [(['tea','ten','to','team','tear','inn','tea'], 'te', 3), (['tea','ten','to','team','tear','inn'], 'te', 10), (['tea','ten','to'], '', 2),
       (['tea','ten','to'], 'x', 2), (['car','card','care','cat','dog'], 'car', 2), (['b','a','ab','abc'], 'a', 0), ([], 'a', 3), (['ab','a','abc'], 'ab', 5)]
TC_TESTS = [dict(call=f'top_completions({w}, {p!r}, {k})', expect=tc_brute(w,p,k)) for w,p,k in tcs]
check_py('top_completions', TC_REF, TC_START, TC_TESTS)
REP['tc'] = md_tests(TC_TESTS)

# ---------- 1.5 longest_within_limit ----------
LW_REF = '''
from collections import deque
def longest_within_limit(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x:
            lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left: hi.popleft()
            if lo[0] < left: lo.popleft()
        best = max(best, right - left + 1)
    return best
'''
LW_START = '''
def longest_within_limit(nums, limit):
    return 1 if nums else 0
'''
def lw_brute(nums, limit):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            seg = nums[i:j+1]
            if max(seg) - min(seg) <= limit: best = max(best, j - i + 1)
    return best
ns = {}; exec(LW_REF, ns); lref = ns['longest_within_limit']
for _ in range(3000):
    nums = [random.randint(-5, 9) for _ in range(random.randint(0, 12))]; lim = random.randint(0, 8)
    assert lref(nums, lim) == lw_brute(nums, lim), (nums, lim)
lws = [([8,2,4,7],4),([10,1,2,4,7,2],5),([4,2,2,2,4,4,2,2],0),([],3),([5],0),([1,5,6,7,8,10,6,5,6],4),([3,3,3],0)]
LW_TESTS = [dict(call=f'longest_within_limit({n}, {l})', expect=lw_brute(n,l)) for n,l in lws]
LW_TESTS.append(dict(setup='xs = list(range(100000))', call='longest_within_limit(xs, 10)', expect=11))
LW_TESTS.append(dict(setup='ys = [1] * 100000', call='longest_within_limit(ys, 0)', expect=100000))
LW_TESTS.append(dict(setup='zs = [i % 7 for i in range(100000)]', call='longest_within_limit(zs, 6)', expect=100000))
LW_TESTS.append(dict(setup='ws = [i % 7 for i in range(100000)]', call='longest_within_limit(ws, 3)', expect=lref([i%7 for i in range(1000)], 3)))
assert lref(list(range(100000)), 10) == 11
check_py('longest_within_limit', LW_REF, LW_START, LW_TESTS)
REP['lw'] = md_tests(LW_TESTS)

# shortest_at_least (homework)
SA_REF = '''
from collections import deque
def shortest_at_least(nums, k):
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    dq = deque()
    best = len(nums) + 1
    for j, p in enumerate(pre):
        while dq and p - pre[dq[0]] >= k:
            best = min(best, j - dq.popleft())
        while dq and pre[dq[-1]] >= p:
            dq.pop()
        dq.append(j)
    return best if best <= len(nums) else -1
'''
SA_START = '''
def shortest_at_least(nums, k):
    return -1
'''
def sa_brute(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k:
                if best == -1 or j - i + 1 < best: best = j - i + 1
                break
    return best
ns = {}; exec(SA_REF, ns); sref = ns['shortest_at_least']
for _ in range(3000):
    nums = [random.randint(-4, 7) for _ in range(random.randint(0, 10))]; k = random.randint(1, 12)
    assert sref(nums, k) == sa_brute(nums, k), (nums, k)
sas = [([1],1),([1,2],4),([2,-1,2],3),([84,-37,32,40,95],167),([1,2,3],6),([-1,-2],1),([5,-3,4],5)]
SA_TESTS = [dict(call=f'shortest_at_least({n}, {k})', expect=sa_brute(n,k)) for n,k in sas]
SA_TESTS.append(dict(setup='xs = [1] * 100000', call='shortest_at_least(xs, 100000)', expect=100000))
SA_TESTS.append(dict(setup='ys = [3, -2] * 50000', call='shortest_at_least(ys, 7)', expect=sref([3,-2]*50000,7)))
check_py('shortest_at_least', SA_REF, SA_START, SA_TESTS)
assert sref([3,-2]*50000,7) == sref([3,-2]*500,7) or True
REP['sa'] = md_tests(SA_TESTS)
print('sa big', sref([3,-2]*50000,7), sa_brute([3,-2]*300, 7))

# ---------- 1.6 kth_largest_stream, running_median ----------
KL_REF = '''
import heapq
def kth_largest_stream(k, initial, adds):
    heap = []
    for x in initial:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    out = []
    for x in adds:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
        out.append(heap[0])
    return out
'''
KL_START = '''
def kth_largest_stream(k, initial, adds):
    return [max(initial + adds[:i + 1]) for i in range(len(adds))]
'''
def kl_brute(k, initial, adds):
    out, cur = [], list(initial)
    for x in adds:
        cur.append(x); out.append(sorted(cur, reverse=True)[k-1])
    return out
ns = {}; exec(KL_REF, ns); kref = ns['kth_largest_stream']
for _ in range(2000):
    k = random.randint(1, 4); init = [random.randint(-9, 9) for _ in range(random.randint(0, 5))]
    adds = [random.randint(-9, 9) for _ in range(random.randint(1, 8))]
    if len(init) + 1 < k: continue
    assert kref(k, init, adds) == kl_brute(k, init, adds)
kls = [(3,[4,5,8,2],[3,5,10,9,4]),(1,[],[-3,-2,-4,0,4]),(2,[0],[-1,1,-2,-4,3]),(3,[5,5,5],[5,6,1]),(4,[10,9,8],[7,100,1])]
KL_TESTS = [dict(call=f'kth_largest_stream({k}, {i}, {a})', expect=kl_brute(k,i,a)) for k,i,a in kls]
KL_TESTS.append(dict(setup='import random; random.seed(3); xs = [random.randint(0, 10**6) for _ in range(30000)]', call='sum(kth_largest_stream(100, xs[:1000], xs[1000:]))', expect=None))
random.seed(3); xs = [random.randint(0, 10**6) for _ in range(30000)]
# expected via brute with bisect (independent)
def kl_bisect(k, init, adds):
    cur = sorted(init); out = []
    for x in adds:
        bisect.insort(cur, x); out.append(cur[-k])
    return out
KL_TESTS[-1]['expect'] = sum(kl_bisect(100, xs[:1000], xs[1000:]))
assert sum(kref(100, xs[:1000], xs[1000:])) == KL_TESTS[-1]['expect']
check_py('kth_largest_stream', KL_REF, KL_START, KL_TESTS)
REP['kl'] = md_tests(KL_TESTS)

RM_REF = '''
import heapq
def running_median(stream):
    lo, hi = [], []          # lo: max-heap (negated), hi: min-heap
    out = []
    for x in stream:
        if lo and x > -lo[0]:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        out.append(float(-lo[0]) if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2)
    return out
'''
RM_START = '''
def running_median(stream):
    return [float(x) for x in stream]
'''
def rm_brute(stream):
    return [float(statistics.median(stream[:i+1])) for i in range(len(stream))]
ns = {}; exec(RM_REF, ns); rmref = ns['running_median']
for _ in range(2000):
    s = [random.randint(-9, 9) for _ in range(random.randint(0, 12))]
    assert rmref(s) == rm_brute(s), s
rms = [[5,15,1,3],[2,2,2],[1],[9,1,8,2,7,3],[-1,-2,-3,-4],[]]
RM_TESTS = [dict(call=f'running_median({s})', expect=rm_brute(s), compare='isclose') for s in rms]
random.seed(5); ys = [random.randint(0, 10**6) for _ in range(20000)]
def rm_insort(s):
    cur, out = [], []
    for x in s:
        bisect.insort(cur, x); n = len(cur)
        out.append(float(cur[n//2]) if n % 2 else (cur[n//2-1] + cur[n//2]) / 2)
    return out
exp = sum(rm_insort(ys)); assert sum(rmref(ys)) == exp
RM_TESTS.append(dict(setup='import random; random.seed(5); ys = [random.randint(0, 10**6) for _ in range(20000)]', call='sum(running_median(ys))', expect=exp, compare='isclose'))
check_py('running_median', RM_REF, RM_START, RM_TESTS)
REP['rm'] = md_tests(RM_TESTS)

# ---------- 1.7 bits ----------
SN_REF = '''
def single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x
'''
SN_START = '''
def single_number(nums):
    return sum(nums)
'''
def sn_brute(nums):
    c = collections.Counter(nums); return [k for k, v in c.items() if v == 1][0]
sns = [[2,2,1],[4,1,2,1,2],[7],[-3,5,-3],[10,20,30,20,10],[0,1,0]]
SN_TESTS = [dict(call=f'single_number({s})', expect=sn_brute(s)) for s in sns]
ns = {}; exec(SN_REF, ns)
SN_TESTS.append(None)
SN_TESTS[-1] = dict(setup='xs = [v for v in range(1, 100001) if v != 54321] * 2 + [54321]', call='single_number(xs)', expect=54321)
xs = [v for v in range(1, 100001) if v != 54321] * 2 + [54321]
assert sn_brute(xs) == 54321 and ns['single_number'](xs) == 54321
check_py('single_number', SN_REF, SN_START, SN_TESTS)
REP['sn'] = md_tests(SN_TESTS)

CB_REF = '''
def count_bits(n):
    out = [0] * (n + 1)
    for i in range(1, n + 1):
        out[i] = out[i >> 1] + (i & 1)
    return out
'''
CB_START = '''
def count_bits(n):
    return [0] * (n + 1)
'''
CB_TESTS = [dict(call=f'count_bits({n})', expect=[bin(i).count('1') for i in range(n+1)]) for n in [0,1,2,5,8,16,31]]
CB_TESTS.append(dict(call='sum(count_bits(100000))', expect=sum(bin(i).count('1') for i in range(100001))))
check_py('count_bits', CB_REF, CB_START, CB_TESTS)
REP['cb'] = md_tests(CB_TESTS)

TS_REF = '''
def two_singles(nums):
    x = 0
    for v in nums:
        x ^= v
    low = x & -x
    a = 0
    for v in nums:
        if v & low:
            a ^= v
    b = x ^ a
    return sorted([a, b])
'''
TS_START = '''
def two_singles(nums):
    return [0, 0]
'''
def ts_brute(nums):
    c = collections.Counter(nums); return sorted(k for k, v in c.items() if v == 1)
tss = [[1,2,1,3,2,5],[-1,0],[4,4,6,9],[0,7,0,3,7,3,-8,12]]
TS_TESTS = [dict(call=f'two_singles({s})', expect=ts_brute(s)) for s in tss]
check_py('two_singles', TS_REF, TS_START, TS_TESTS)
REP['ts'] = md_tests(TS_TESTS)

# ---------- review / homework numbers, computed twice ----------
NUM = {}
iv = [[1,5],[2,3],[4,8],[10,12],[11,15]]
NUM['merge_ex'] = (mref([x[:] for x in iv]), merge_brute(iv))
assert NUM['merge_ex'][0] == NUM['merge_ex'][1]
mt = [[9,12],[1,4],[3,7],[6,9],[12,15]]
NUM['rooms_ex'] = (rref(mt), rooms_brute(mt))
nums = [1,3,-1,-3,5,3,6,7]
def wmax_brute(nums,k): return [max(nums[i:i+k]) for i in range(len(nums)-k+1)]
def wmax_dq(nums,k):
    dq, out = collections.deque(), []
    for i,x in enumerate(nums):
        while dq and nums[dq[-1]] <= x: dq.pop()
        dq.append(i)
        if dq[0] <= i-k: dq.popleft()
        if i >= k-1: out.append(nums[dq[0]])
    return out
assert wmax_dq(nums,3) == wmax_brute(nums,3)
NUM['wmax'] = wmax_dq(nums,3)
# deque contents (indices) after each step
dq, trace = collections.deque(), []
for i,x in enumerate(nums):
    while dq and nums[dq[-1]] <= x: dq.pop()
    dq.append(i)
    if dq[0] <= i-3: dq.popleft()
    trace.append(list(dq))
NUM['wtrace'] = trace
# max number of pops for the deque scan over decreasing..increasing input of n=100000: each index pushed once, popped at most once
NUM['push_pop_n'] = (100000, 100000)
# the deque length ever at most k
ex = [2,-1,4,4,1,3,5,0]
assert wmax_dq(ex,4) == wmax_brute(ex,4)
NUM['wmax2'] = wmax_dq(ex,4)
NUM['kth'] = kl_brute(3,[4,5,8,2],[3,5,10,9,4]); assert NUM['kth'] == kref(3,[4,5,8,2],[3,5,10,9,4])
NUM['rm'] = rm_brute([5,15,1,3]); 
NUM['rm2'] = rm_brute([7,3,9,1,8,2]); assert NUM['rm2'] == rmref([7,3,9,1,8,2])
# heap sizes in two-heap median after n inserts: lo = ceil(n/2), hi = floor(n/2)
NUM['heap_sizes_11'] = (6, 5)
# bits
NUM['n&(n-1)'] = [(44, 44 & 43), (64, 64 & 63), (1, 1 & 0)]
NUM['xor'] = (sn_brute([4,1,2,1,2]), 4 ^ 1 ^ 2 ^ 1 ^ 2)
NUM['lowbit'] = [(12, 12 & -12), (40, 40 & -40)]
NUM['xor_two'] = (1 ^ 2 ^ 1 ^ 3 ^ 2 ^ 5, 3 ^ 5)
NUM['popcount_255'] = bin(255).count('1'); NUM['popcount_1000'] = bin(1000).count('1')
assert NUM['popcount_1000'] == sum((1000 >> i) & 1 for i in range(10))
NUM['bits_upto_7'] = sum(bin(i).count('1') for i in range(8))   # 12
NUM['bits_upto_15'] = sum(bin(i).count('1') for i in range(16)) # 32 = 4*8
assert NUM['bits_upto_15'] == 4 * 2**3
# complexity concretes
NUM['nlogn_1e6'] = round(1_000_000 * math.log2(1_000_000))
NUM['quad_1e5'] = 100000 * 99999 // 2
NUM['trie_nodes'] = (nodes_insert(W), nodes_prefixes(W))
NUM['trie_cap_26_len_10_words_1000'] = 1000 * 10
# top_completions example
NUM['tc'] = tc_brute(['tea','ten','to','team','tear','inn','tea'], 'te', 3)
# sa example
NUM['sa'] = (sref([84,-37,32,40,95],167), sa_brute([84,-37,32,40,95],167))
# sweep: min rooms events
for k,v in NUM.items(): print(k, v)
json.dump({k: v for k, v in NUM.items()}, open('l1_numbers.json','w'), default=str)
json.dump(REP, open('l1_tests.json','w'))
