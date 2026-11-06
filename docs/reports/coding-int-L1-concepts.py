#!/usr/bin/env python3
"""Concept checks for coding-int level 1 (blind concept audit, 6 Nov 2026).

Run from the repo root: python3 -I docs/reports/coding-int-L1-concepts.py
Exit 0 when every check passes. A check that encodes a content claim the
audit found wrong stays failing until the content is fixed (brief step 4).

Covers l1 to l5, review-1 and homework-1: every Python and C++ code widget
(model solution passes its hidden tests, the untouched starter fails at least
one), and the stated traces, counts, invariants and complexity claims, by
brute force, operation counters or direct computation. No timing is used.
"""
import bisect
import heapq
import json
import math
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, deque

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / 'app' / 'content' / 'courses' / 'coding-int'
FAILS = []


def check(cond, name):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        FAILS.append(name)


def load(name):
    return json.loads((COURSE / f'{name}.json').read_text())


def code_widgets(doc):
    out = []

    def add(path, obj):
        w = obj.get('widget')
        if w and w.get('kind') == 'code':
            out.append((path, w))
        for k, p in enumerate(obj.get('parts', []) or []):
            w = p.get('widget')
            if w and w.get('kind') == 'code':
                out.append((f'{path}.parts[{k}]', w))

    for i, s in enumerate(doc.get('screens', [])):
        add(f'screens[{i}]', s)
    for key in ('quiz', 'items'):
        for i, it in enumerate(doc.get(key, [])):
            add(f'{key}[{i}]', it)
    return out


def _close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_py(widget, code):
    """Run `code` against the widget's hidden tests as the engine does. Returns one bool per test."""
    tests = widget['tests']
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    try:
        for name, rel in (widget.get('data') or {}).items():
            shutil.copy(ROOT / 'app' / rel, name)
        ns = {'__learner_source__': code}
        src = widget.get('prelude', '') + '\n' + code + '\n' + widget.get('postlude', '')
        try:
            exec(src, ns)
        except Exception:
            return [False] * len(tests)
        res = []
        for t in tests:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns)
                        res.append(False)
                    except Exception as e:
                        res.append(isinstance(e, eval(t['expect'], ns)))
                    continue
                val = eval(t['call'], ns)
                exp = eval(t['expect'], ns)
                res.append(_close(val, exp) if t.get('compare') == 'isclose' else val == exp)
            except Exception:
                res.append(False)
        return res
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


CPP_PRINT = r'''
#include <iostream>
#include <string>
#include <vector>
static void pj(int v) { std::cout << v; }
static void pj(long long v) { std::cout << v; }
static void pj(const std::string& s) { std::cout << '"' << s << '"'; }
template <class T> static void pj(const std::vector<T>& v) {
    std::cout << '[';
    for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; pj(v[i]); }
    std::cout << ']';
}
'''


def cpp_lit(value, typ):
    if typ is None:
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return repr(value)
        if isinstance(value, str):
            return json.dumps(value)
        return '{' + ','.join(cpp_lit(v, None) for v in value) + '}'
    if typ.startswith('std::vector<'):
        inner = typ[len('std::vector<'):-1]
        return typ + '{' + ','.join(cpp_lit(v, inner) for v in value) + '}'
    if typ == 'std::string':
        return json.dumps(value)
    return str(value)


def cpp_run_source(src, timeout=120):
    """Compile and run a C++17 program; returns stdout or None on a compile error."""
    tmp = tempfile.mkdtemp()
    try:
        p = pathlib.Path(tmp) / 'main.cpp'
        p.write_text(src)
        c = subprocess.run(['g++', '-std=c++17', '-O1', '-o', tmp + '/a.out', str(p)],
                           capture_output=True, text=True)
        if c.returncode != 0:
            return None
        r = subprocess.run([tmp + '/a.out'], capture_output=True, text=True, timeout=timeout)
        return r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_cpp(widget, code, extra_tests=None):
    """Run C++ `code` against the widget's tests (function mode) with g++. Returns one bool per test."""
    tests = list(widget['tests']) + list(extra_tests or [])
    main = ['int main() {']
    for k, t in enumerate(tests):
        body = []
        if t.get('setup'):
            body.append(t['setup'])
        call = t['call']
        if 'args' in t or 'types' in t:
            types = t.get('types') or [None] * len(t.get('args', []))
            args = t.get('args', [[] for _ in types])
            call = call + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(args, types)) + ')'
        body.append(f'std::cout << {k} << " "; pj({call}); std::cout << "\\n";')
        main.append('{' + '\n'.join(body) + '}')
    main.append('return 0; }')
    src = code + '\n' + widget.get('postlude', '') + '\n' + CPP_PRINT + '\n'.join(main)
    out = cpp_run_source(src)
    if out is None:
        return [False] * len(tests)
    got = {}
    for line in out.splitlines():
        k, _, rest = line.partition(' ')
        try:
            got[int(k)] = json.loads(rest)
        except ValueError:
            pass
    return [k in got and got[k] == t.get('expect', []) for k, t in enumerate(tests)]


def check_code(doc, label):
    for path, w in code_widgets(doc):
        runner = run_cpp if w.get('language') == 'cpp' else run_py
        sol = runner(w, w['solution'])
        st = runner(w, w['starter'])
        check(all(sol), f'{label} {path}: model solution passes all {len(sol)} hidden tests')
        check(not all(st), f'{label} {path}: untouched starter fails at least one hidden test')


def widget(doc, path):
    key, idx = path[:-1].split('[')
    return doc[key][int(idx)]['widget']


def ns_of(w, code=None):
    ns = {}
    exec(w.get('prelude', '') + '\n' + (code or w['solution']) + '\n' + w.get('postlude', ''), ns)
    return ns


# ---------------------------------------------------------------- load
L1, L2, L3, L4, L5 = (load(n) for n in ('l1-merging-intervals', 'l2-prefix-trees', 'l3-window-maximum',
                                       'l4-top-k', 'l5-bit-tricks'))
R1, H1 = load('review-1'), load('homework-1')
random.seed(20261106)

print('# code widgets: solution passes, starter fails')
for doc, label in ((L1, 'l1'), (L2, 'l2'), (L3, 'l3'), (L4, 'l4'), (L5, 'l5'), (R1, 'review-1'), (H1, 'homework-1')):
    check_code(doc, label)

# ---------------------------------------------------------------- l1 merging intervals
print('# l1 merging intervals')
merge_ns = ns_of(widget(L1, 'screens[4]'))
merge_intervals = merge_ns['merge_intervals']
sweep_ns = ns_of(widget(L1, 'screens[8]'))
count_pairs = sweep_ns['count_overlapping_pairs']


def merge_unsorted(intervals):
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def merge_copy_end(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = e
        else:
            out.append([s, e])
    return out


def brute_merge(intervals):
    # union of closed integer intervals by marking points
    if not intervals:
        return []
    lo = min(s for s, _ in intervals)
    hi = max(e for _, e in intervals)
    covered = [False] * (2 * (hi - lo) + 1)      # half-integer resolution: [1, 2] and [3, 4] stay apart
    for s, e in intervals:
        for x in range(2 * (s - lo), 2 * (e - lo) + 1):
            covered[x] = True
    out, i = [], 0
    while i < len(covered):
        if covered[i]:
            j = i
            while j + 1 < len(covered) and covered[j + 1]:
                j += 1
            out.append([i // 2 + lo, j // 2 + lo])
            i = j + 1
        else:
            i += 1
    return out


def brute_pairs(iv):
    return sum(1 for i in range(len(iv)) for j in range(i + 1, len(iv))
               if max(iv[i][0], iv[j][0]) < min(iv[i][1], iv[j][1]))


check(merge_unsorted([[8, 10], [1, 3], [2, 6]]) == [[8, 10]], 'l1 s2: loop without the sort returns [[8, 10]]')
check(merge_intervals([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]], 'l1 s2 explain: with the sort [[1, 6], [8, 10]]')
check(merge_intervals([[1, 4], [4, 5]]) == [[1, 5]] and count_pairs([[1, 4], [4, 5]]) == 0,
      'l1 s3: closed touching ends merge; half-open touching ends do not overlap')
check(merge_copy_end([[1, 10], [2, 3], [4, 5]]) == [[1, 3], [4, 5]], 'l1 s6: copying the end gives [[1, 3], [4, 5]]')
ok = True
for _ in range(300):
    iv = [[a, a + random.randint(0, 6)] for a in (random.randint(0, 30) for _ in range(random.randint(0, 8)))]
    ok &= merge_intervals(iv) == brute_merge(iv)
    # closed intervals that touch merge; gaps of one integer stay apart (brute marks integer points)
check(ok, 'l1 s4: merge_intervals equals the pointwise union on 300 random closed integer-interval sets')
ok = True
for _ in range(300):
    iv = [[a, a + random.randint(1, 6)] for a in (random.randint(0, 30) for _ in range(random.randint(0, 8)))]
    ok &= count_pairs(iv) == brute_pairs(iv)
check(ok, 'l1 s8: sweep count equals the double loop on 300 random half-open sets')
check(count_pairs([[i, i + 3] for i in range(10)]) == 17 and brute_pairs([[i, i + 3] for i in range(10)]) == 17
      and count_pairs([[i, i + 3] for i in range(100000)]) == 199997,
      'l1 s8 test 8: [i, i+3) for n gives 2n - 3 (17 at n = 10, 199,997 at n = 100,000)')
check(sorted([(10, 1), (10, -1)]) == [(10, -1), (10, 1)], 'l1 s8 hint: tuple sort puts (t, -1) before (t, 1)')


def active_at_starts(iv):
    ev = sorted([(s, 1) for s, _ in iv] + [(e, -1) for _, e in iv])
    active, out = 0, []
    for _, step in ev:
        if step == 1:
            out.append(active)
        active += step
    return out


check(active_at_starts([[1, 4], [2, 6], [5, 9], [8, 10]]) == [0, 1, 1, 1], 'l1 s9: active at each start 0, 1, 1, 1 (total 3)')
check(len(merge_intervals([[3, 6], [1, 2], [5, 9], [11, 13], [12, 12]])) == 3
      and merge_intervals([[3, 6], [1, 2], [5, 9], [11, 13], [12, 12]]) == [[1, 2], [3, 9], [11, 13]],
      'l1 q0: three blocks [1, 2], [3, 9], [11, 13]')
check(merge_intervals([[2, 5], [5, 7]]) == [[2, 7]], 'l1 q1: closed [2, 5] and [5, 7] merge to [2, 7]')
check(abs(1e6 * math.log2(1e6) - 19931569) < 1, 'l1 q2: n log2 n at a million is 19,931,569')
check(math.comb(100000, 2) == 4999950000 and 100000 * 99999 == 9999900000, 'l1 q3: C(100000, 2) = 4,999,950,000; n(n-1) = 9,999,900,000')
check(sum(merge_intervals(sorted([[a, a + 1] for a in range(5)]))[0]) == 5, 'l1: sort then one pass (sanity)')
# C++ claims on s5
out = cpp_run_source(r'''
#include <vector>
#include <algorithm>
#include <iostream>
int main() {
    std::vector<std::vector<int>> v = {{2, 5}, {1, 9}, {1, 3}};
    std::sort(v.begin(), v.end());
    for (auto& x : v) std::cout << x[0] << ' ' << x[1] << ';';
    std::vector<std::vector<int>> out = {{1, 2}};
    out.back()[1] = 7;
    std::cout << out[0][1];
    return 0;
}
''')
check(out == '1 3;1 9;2 5;7', 'l1 s5: std::sort on vector<vector<int>> is lexicographic; out.back() is a reference')

# ---------------------------------------------------------------- l2 prefix trees
print('# l2 prefix trees')
trie_ns = ns_of(widget(L2, 'screens[4]'))
Trie = trie_ns['Trie']
comp_ns = ns_of(widget(L2, 'screens[8]'))
top_completions = comp_ns['top_completions']


def trie_nodes(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})

    def count(n):
        return sum(1 + count(c) for c in n.values())
    return count(root)


check(trie_nodes(['tea', 'ten', 'to', 'inn']) == 8, 'l2 s0: tea, ten, to, inn make 8 nodes (11 letters)')
check(trie_nodes(['tea', 'ten']) == 4, 'l2 s1: tea then ten make 4 nodes (ten adds only n)')
t = Trie()
for w in ('tea', 'ten', 'to', 'inn'):
    t.insert(w)
check(t.search('te') is False and t.starts_with('te') is True, 'l2 s2: search(te) False, starts_with(te) True')
ok = True
for _ in range(50):
    words = [''.join(random.choice('ab') for _ in range(10)) for _ in range(1000)]
    ok &= trie_nodes(words) <= 10000
check(ok and trie_nodes(['%010d' % i for i in range(1000)]) <= 10000, 'l2 s3: 1,000 words of 10 letters never exceed 10,000 nodes')
t = Trie()
for w in ('inn', 'inn'):
    t.insert(w)
check(t.count_prefix('in') == 1, 'l2 s5: a repeat insert leaves count_prefix(in) at 1')
t = Trie()
t.insert('apple')
check(t.search('app') is False and t.starts_with('app') is True, 'l2 s6: search(app) False after only apple')
t = Trie()
for w in ('bid', 'bid', 'bids'):
    t.insert(w)
check(t.count_prefix('bid') == 2, 'l2 q2: bid, bid, bids give count_prefix(bid) = 2')
check(trie_nodes(['buy', 'bus', 'bid']) == 6, 'l2 q0: buy, bus, bid make 6 nodes')
t = Trie()
for w in ('sell', 'seller'):
    t.insert(w)
check(t.search('sel') is False and t.starts_with('sel') is True, 'l2 q1: sel is a prefix, not a word')
ok = True
for _ in range(200):
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(random.randint(0, 12))]
    prefix = ''.join(random.choice('abc') for _ in range(random.randint(0, 2)))
    k = random.randint(0, 5)
    ok &= top_completions(words, prefix, k) == sorted({w for w in words if w.startswith(prefix)})[:k]
check(ok, 'l2 s8: sorted-child preorder DFS from the prefix node yields the k smallest matches in lexicographic order (200 random)')


def bisect_comparisons(a, x):
    lo, hi, n = 0, len(a), 0
    while lo < hi:
        mid = (lo + hi) // 2
        n += 1
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return n


symbols = sorted('%04d' % i for i in range(4000))
counts = [bisect_comparisons(symbols, '%04d' % random.randint(-5, 4005)) for _ in range(2000)]
check(max(counts) == 12 and min(counts) >= 11 and 2 ** 12 == 4096,
      'l2 s9 and q3: bisect_left on 4,000 symbols makes 11 or 12 comparisons; 2^12 = 4,096')


def trie_walk_steps(root, s):
    node, steps = root, 0
    for ch in s:
        node = node.get(ch)
        steps += 1
        if node is None:
            break
    return steps


root = {}
for w in symbols:
    node = root
    for ch in w:
        node = node.setdefault(ch, {})
# content claim (l2 s9 option b why): "both are fast, about 12 steps each" for the trie on 4,000 symbols.
# A trie walk costs one step per letter of the prefix (3 for a 3-letter prefix), so this encoded claim fails.
check(abs(trie_walk_steps(root, '012') - 12) <= 2, 'l2 s9 o1.why: a trie prefix walk on 4,000 symbols takes about 12 steps (content claim; the walk takes len(prefix) = 3)')

# ---------------------------------------------------------------- l3 window maximum
print('# l3 window maximum')
lw_ns = ns_of(widget(L3, 'screens[4]'))
longest_within_limit = lw_ns['longest_within_limit']


def max_deque_run(nums, k, strict_front=False):
    """Returns (maxima, deque after each index). strict_front drops the front only when f < i - k (the quiz distractor)."""
    dq, maxima, states = deque(), [], []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if (strict_front and dq[0] < i - k) or (not strict_front and dq[0] <= i - k):
            dq.popleft()
        states.append(list(dq))
        if i >= k - 1:
            maxima.append(nums[dq[0]])
    return maxima, states


nums = [2, 5, -1, -4, 6, 4, 7, 9]
maxima, states = max_deque_run(nums, 3)
check(states[3] == [1, 2, 3] and states[4] == [4], 'l3 s0: deque [1, 2, 3] after index 3 and [4] after index 4')
check(maxima == [5, 5, 6, 6, 7, 9] and sum(maxima) == 38 and sum(nums) == 28 and sum(maxima[:5]) == 29
      and sum(min(nums[i:i + 3]) for i in range(6)) == -5,
      'l3 s1: six maxima 5, 5, 6, 6, 7, 9 sum to 38 (distractors 28, 29, -5)')


def brute_longest(nums, limit):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if max(nums[i:j + 1]) - min(nums[i:j + 1]) <= limit:
                best = max(best, j - i + 1)
    return best


check(brute_longest([8, 2, 4, 7], 4) == 2, 'l3 s2: longest run with range at most 4 in [8, 2, 4, 7] is 2')


def traced_lwl(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    lefts, lo_fronts = [], []
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x:
            lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left:
                hi.popleft()
            if lo[0] < left:
                lo.popleft()
        lefts.append(left)
        lo_fronts.append(lo[0])
        best = max(best, right - left + 1)
    return best, lefts, lo_fronts


best, lefts, lo_fronts = traced_lwl([10, 1, 2, 4, 7, 2], 5)
check(lefts[1] == 1 and lefts[4] == 2 and lo_fronts[3] == 1 and lo_fronts[4] == 2 and best == 4,
      'l3 s3: at right = 4 left moves to 2 and the 1 at index 1 leaves the min deque (10 left at right = 1)')
ok = True
for _ in range(300):
    xs = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
    lim = random.randint(0, 5)
    ok &= longest_within_limit(xs, lim) == brute_longest(xs, lim)
check(ok, 'l3 s4: longest_within_limit equals brute force on 300 random lists')


class CountingDeque(deque):
    ops = 0

    def append(self, x):
        CountingDeque.ops += 1
        super().append(x)

    def pop(self):
        CountingDeque.ops += 1
        return super().pop()

    def popleft(self):
        CountingDeque.ops += 1
        return super().popleft()


def counted_lwl(nums, limit):
    CountingDeque.ops = 0
    hi, lo = CountingDeque(), CountingDeque()
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
            if hi[0] < left:
                hi.popleft()
            if lo[0] < left:
                lo.popleft()
        best = max(best, right - left + 1)
    return best, CountingDeque.ops


ok = True
for n in (1000, 10000, 100000):
    for xs in (list(range(n)), [random.randint(0, 100) for _ in range(n)], [i % 7 for i in range(n)]):
        ok &= counted_lwl(xs, 10)[1] <= 4 * n
check(ok, 'l3 s5: pushes plus pops over both deques never exceed 4n (n = 1,000, 10,000, 100,000; three shapes)')


def trap_lwl(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x:
            lo.pop()
        lo.append(right)
        while left <= right and nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
        best = max(best, right - left + 1)
    return best


check(trap_lwl([4, 2, 2, 2, 4, 4, 2, 2], 0) == 1 and longest_within_limit([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3,
      'l3 s6: never dropping stale fronts returns 1 where the answer is 3')


def strict_pop_lwl(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] < x:
            hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] > x:
            lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left:
                hi.popleft()
            if lo[0] < left:
                lo.popleft()
        best = max(best, right - left + 1)
    return best


ok = True
for _ in range(300):
    xs = [random.randint(0, 5) for _ in range(random.randint(0, 12))]
    lim = random.randint(0, 3)
    ok &= strict_pop_lwl(xs, lim) == brute_longest(xs, lim)
check(ok, 'l3 s6 explain: dropping fronts below left is right whether back pops use <= or < (300 random)')
check(brute_longest([412, 415, 417, 414, 419, 421, 418, 416, 422, 409], 5) == 4
      and max([412, 415, 417, 414, 419, 421, 418, 416, 422, 409]) - min([412, 415, 417, 414, 419, 421, 418, 416, 422, 409]) == 13,
      'l3 s9: longest calm stretch of the ten ticks is 4; whole day range 13')
check(max_deque_run([5, 2, 7, 3, 6, 8, 1, 4], 3)[1][3] == [2, 3], 'l3 q0: deque holds indices 2 and 3 after index 3')
ok, bad = True, False
for _ in range(300):
    xs = [random.randint(0, 9) for _ in range(random.randint(1, 12))]
    k = random.randint(1, len(xs))
    truth = [max(xs[i:i + k]) for i in range(len(xs) - k + 1)]
    ok &= max_deque_run(xs, k)[0] == truth
    bad |= max_deque_run(xs, k, strict_front=True)[0] != truth
check(ok and bad, 'l3 q1: dropping the front when f <= i - k gives every window maximum; f < i - k fails on some input')
check(50001 * 50000 == 2500050000 and 100000 - 50000 + 1 == 50001, 'l3 q2: 50,001 windows of 50,000 reads is 2,500,050,000')
ok = True
for n in (1000, 100000):
    CountingDeque.ops = 0
    dq = CountingDeque()
    xs = [random.randint(0, 100) for _ in range(n)]
    for i, x in enumerate(xs):
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - 50000:
            dq.popleft()
    ok &= CountingDeque.ops <= 2 * n
check(ok, 'l3 q2 and homework-1 i5: one max deque does at most 2n operations (200,000 at n = 100,000)')
check(brute_longest([5, 8, 6, 9, 3, 4, 4, 2], 3) == 4 and longest_within_limit([5, 8, 6, 9, 3, 4, 4, 2], 3) == 4, 'l3 q3: answer 4')

# ---------------------------------------------------------------- l4 top-k
print('# l4 top-k')
tk_ns = ns_of(widget(L4, 'screens[3]'))
top_k_frequent = tk_ns['top_k_frequent']
ks_ns = ns_of(widget(L4, 'screens[6]'))
kth_largest_stream = ks_ns['kth_largest_stream']
table = [('KRN', 9), ('TAV', 14), ('ORX', 11), ('ZEN', 6), ('MPL', 11), ('VLT', 9), ('BLN', 11), ('QRS', 4)]
check([s for s, _ in sorted(table, key=lambda r: (-r[1], r[0]))[:3]] == ['TAV', 'BLN', 'MPL'], 'l4 s0: count descending then symbol ascending picks TAV, BLN, MPL')
sizes = [300, 120, 450, 80, 600, 250, 90, 700, 310, 150]
heap, pops = [], 0
for s in sizes:
    heapq.heappush(heap, s)
    if len(heap) > 3:
        heapq.heappop(heap)
        pops += 1
check(pops == 7 and heap[0] == 450 and sorted(heap, reverse=True) == [700, 600, 450],
      'l4 s1 and s2: 7 pops over ten pushes; the min-heap top 450 is the 3rd largest behind 700 and 600')
ok = True
for _ in range(300):
    words = [random.choice('abcdefg') for _ in range(random.randint(0, 15))]
    k = random.randint(0, 8)
    c = Counter(words)
    ok &= top_k_frequent(words, k) == [w for w, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
check(ok, 'l4 s3: nsmallest with key (-count, word) equals the full sort on 300 random inputs')
c = Counter(['bid', 'ask', 'bid', 'ask', 'mid'])
check(list(c) == ['bid', 'ask', 'mid'] and [w for w, _ in sorted(c.items(), key=lambda kv: -kv[1])][:2] == ['bid', 'ask']
      and top_k_frequent(['bid', 'ask', 'bid', 'ask', 'mid'], 2) == ['ask', 'bid'],
      'l4 s5: Counter keeps first-appearance order; a stable sort by -count alone leaves bid before ask; the two-part key gives ask, bid')
c2 = Counter(['ask', 'bid', 'bid', 'ask', 'mid'])
check([w for w, _ in sorted(c2.items(), key=lambda kv: -kv[1])][:2] == ['ask', 'bid'], 'l4 s5 explain: a different input order flips the count-only answer')
check(sorted([(2, 'b'), (2, 'a'), (3, 'c')], key=lambda t: -t[0]) == [(3, 'c'), (2, 'b'), (2, 'a')], 'l4 s5: Python sort is stable')


def brute_kth(k, initial, adds):
    seen, out = list(initial), []
    for x in adds:
        seen.append(x)
        out.append(sorted(seen, reverse=True)[k - 1])
    return out


ok = True
for _ in range(300):
    k = random.randint(1, 4)
    initial = [random.randint(-5, 20) for _ in range(random.randint(k - 1, 5))]
    adds = [random.randint(-5, 20) for _ in range(random.randint(1, 8))]
    ok &= kth_largest_stream(k, initial, adds) == brute_kth(k, initial, adds)
check(ok, 'l4 s6: size-k min-heap top equals the sorted k-th largest after every add (300 random)')
random.seed(3)
xs = [random.randint(0, 10 ** 6) for _ in range(30000)]
check(sum(kth_largest_stream(100, xs[:1000], xs[1000:])) == 28666963171 and sum(brute_kth(100, xs[:1000], xs[1000:5000])) == sum(kth_largest_stream(100, xs[:1000], xs[1000:5000])),
      'l4 s6 test 6: seed-3 sum 28,666,963,171; prefix agrees with re-sorting')
random.seed(20261106)


def running_medians(vals):
    lo, hi, out = [], [], []
    for x in vals:
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x)
        else:
            heapq.heappush(hi, x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        out.append(-lo[0] if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2)
    return out


import statistics
meds = running_medians([7, 3, 9, 1, 8, 2])
check(meds == [7, 5, 7, 5, 7, 5] and sum(meds) == 36
      and meds == [statistics.median([7, 3, 9, 1, 8, 2][:i + 1]) for i in range(6)],
      'l4 s7: running medians 7, 5, 7, 5, 7, 5 sum to 36')
check(abs(500000 * math.log2(500000) - 9.47e6) < 5e4, 'l4 s9: 500,000 log2 500,000 is about 9.5 million')
check(abs(100000 * math.log(100000) / math.log(10) - 500000) < 1e-6 and abs(100000 * math.log2(100000) - 1660964) < 1,
      'l4 s10: n log n / log k = 500,000 in any base; n log2 n = 1,660,964')
check(top_k_frequent(['sell', 'buy', 'sell', 'buy'], 1) == ['buy'], 'l4 q0: tie broken alphabetically: buy')
heap, pops = [], 0
for s in range(12):
    heapq.heappush(heap, random.random())
    if len(heap) > 4:
        heapq.heappop(heap)
        pops += 1
check(pops == 8, 'l4 q1: twelve values into a heap of 4 cause 8 pops')
out = cpp_run_source(r'''
#include <queue>
#include <vector>
#include <functional>
#include <iostream>
int main() {
    std::priority_queue<int, std::vector<int>, std::greater<int>> q;
    for (int x : {5, 1, 8, 3}) q.push(x);
    std::priority_queue<int> d;
    for (int x : {5, 1, 8, 3}) d.push(x);
    std::cout << q.top() << ' ' << d.top();
    return 0;
}
''')
check(out == '1 8', 'l4 q3: std::greater makes a min-heap (top 1); the default std::less puts 8 on top')

# ---------------------------------------------------------------- l5 bit tricks
print('# l5 bit tricks')
ht_ns = ns_of(widget(L5, 'screens[6]'))
hamming_total = ht_ns['hamming_total']
check(4 ^ 1 ^ 2 ^ 1 ^ 2 == 4 and 4 + 1 + 2 + 1 + 2 == 10 and 4 | 1 | 2 == 7, 'l5 s0: XOR of [4, 1, 2, 1, 2] is 4 (sum 10, OR 7)')
check(all((x ^ x) == 0 and (x & x) == x and (x | x) == x for x in range(64)), 'l5 s1: x ^ x = 0, x & x = x | x = x')


def popcount_runs(n):
    r = 0
    while n:
        n &= n - 1
        r += 1
    return r


check(44 & 43 == 40 and popcount_runs(44) == 3 and bin(44) == '0b101100', 'l5 s2: 44 & 43 = 40; three runs of n &= n - 1')
check(all(popcount_runs(n) == bin(n).count('1') for n in range(2000)), 'l5 s2: n &= n - 1 runs once per set bit (0 to 1999)')
check(12 & -12 == 4 and 40 & -40 == 8 and 88 & -88 == 8 and 88 & 87 == 80 and all((n & -n) == (1 << (bin(n)[::-1].index('1'))) for n in range(1, 2000)),
      'l5 s4 and q2: n & -n isolates the lowest set bit (12 -> 4, 40 -> 8, 88 -> 8; 88 & 87 = 80)')
check(2 ^ 2 ^ 2 == 2 and 2 ^ 7 ^ 5 == 0 and 23 ^ 23 ^ 23 == 23, 'l5 s5 and q3: three copies leave one; 2 ^ 7 ^ 5 = 0')
check(sum(((sum((v >> b) & 1 for v in [2, 2, 2, 7, 7, 7, 5]) % 3) << b) for b in range(32)) == 5,
      'l5 s5 explain: counting ones per column modulo 3 recovers 5')
check(all(sn == 0 or True for sn in [0]) and ns_of(widget(L5, 'screens[3]'))['single_number']([-3, 5, -3]) == 5 and (-7 ^ -7) == 0,
      'l5 s3: XOR cancels pairs for negative Python ints too')


def brute_hamming(nums):
    return sum(bin(a ^ b).count('1') for i, a in enumerate(nums) for b in nums[i + 1:])


ok = True
for _ in range(200):
    xs = [random.randint(0, 2 ** 31 - 1) for _ in range(random.randint(0, 8))]
    ok &= hamming_total(xs) == brute_hamming(xs)
check(ok, 'l5 s6: column count c(n - c) equals the pairwise Hamming sum (200 random, values to 2^31 - 1)')
check(hamming_total([5, 9, 12]) == 6 and hamming_total(list(range(65536))) == 2 ** 34 and math.comb(65536, 2) == 2147450880,
      'l5 s6: [5, 9, 12] gives 6; 0..65535 gives 2^34 = 17,179,869,184; about 2.1 billion pairs')
check(101 ^ 102 ^ 101 ^ 103 ^ 102 == 103, 'l5 s8: the feed XORs to 103')
ok = True
for _ in range(100):
    n = random.randint(1, 30)
    missing = random.randint(1, n)
    stream = [s for s in range(1, n + 1) for _ in range(2) if not (s == missing and _ == 1)]
    random.shuffle(stream)
    ok &= 2 * sum(set(stream)) - sum(stream) == missing and 2 * (n * (n + 1) // 2) - sum(stream) == missing
check(ok, 'l5 s8 o3: 2 x (sum of distinct) - (sum of all) is the unpartnered number; with sequence numbers 1..N it needs no set (constant memory)')
check(sum(bin(i).count('1') for i in range(16)) == 32, 'l5 s9: set bits in 0..15 total 32')
check(6 ^ 11 ^ 6 ^ 11 ^ 13 ^ 13 ^ 9 == 9 and popcount_runs(77) == 4 and bin(77) == '0b1001101', 'l5 q0 and q1: 9; 77 has four set bits')

# ---------------------------------------------------------------- review-1
print('# review-1')
check(merge_intervals([[0, 4], [3, 8], [10, 13], [15, 18], [17, 21], [23, 24]]) == [[0, 8], [10, 13], [15, 21], [23, 24]], 'r1 i0: four blocks')
check(count_pairs([[0, 4], [3, 8], [10, 13], [15, 18], [17, 21], [23, 24]]) == 2 and brute_pairs([[0, 4], [3, 8], [10, 13], [15, 18], [17, 21], [23, 24]]) == 2, 'r1 i1: two half-open overlapping pairs')
check(trie_nodes(['car', 'card', 'care', 'cat', 'dog']) == 9, 'r1 i2: 9 nodes')
t = Trie()
for w in ('car', 'card', 'care', 'cat', 'dog', 'car'):
    t.insert(w)
check(t.count_prefix('car') == 3, 'r1 i3: count_prefix(car) = 3 with the repeat counted once')
maxima, states = max_deque_run([4, 2, 12, 3, 8, 5, 1, 7], 3)
check(maxima == [12, 12, 12, 8, 8, 7] and sum(maxima) == 59 and sum([4, 2, 12, 3, 8, 5, 1, 7]) == 42 and sum(maxima[:5]) == 52,
      'r1 i4: maxima sum 59 (distractors 42 and 52)')
check(states[5] == [4, 5], 'r1 i5: deque holds indices 4 and 5 after index 5')
ans = kth_largest_stream(3, [6, 1, 9, 5], [2, 7, 12, 8, 3])
check(ans == [5, 6, 7, 8, 8] and sum(ans) == 34 and sum(brute_kth(1, [6, 1, 9, 5], [2, 7, 12, 8, 3])) == 54 and sum(brute_kth(2, [6, 1, 9, 5], [2, 7, 12, 8, 3])) == 40,
      'r1 i6: 3rd largest after each add 5, 6, 7, 8, 8 (sum 34; largest 54; 2nd 40)')
check(108 & 107 == 104 and 108 | 107 == 111 and 108 ^ 107 == 7 and 9 ^ 14 ^ 9 ^ 3 ^ 14 == 3, 'r1 i8 and i9: 104 (111 OR, 7 XOR); XOR 3')

# ---------------------------------------------------------------- homework-1
print('# homework-1')
fg_ns = ns_of(widget(H1, 'items[0]'))
free_gaps = fg_ns['free_gaps']


def brute_gaps(busy, start, end):
    free = [all(not (s <= m < e) for s, e in busy) for m in range(start, end)]
    out, m = [], 0
    while m < len(free):
        if free[m]:
            j = m
            while j + 1 < len(free) and free[j + 1]:
                j += 1
            out.append([start + m, start + j + 1])
            m = j + 1
        else:
            m += 1
    return out


ok = True
for _ in range(300):
    busy = [[a, a + random.randint(1, 5)] for a in (random.randint(0, 20) for _ in range(random.randint(0, 6)))]
    start = random.randint(0, 10)
    end = start + random.randint(0, 15)
    ok &= free_gaps(busy, start, end) == brute_gaps(busy, start, end)
check(ok, 'h1 i0: free_gaps equals the minute-by-minute scan on 300 random bookings')

tb_ns = ns_of(widget(H1, 'items[1]'))
TickerBook = tb_ns['TickerBook']


class ListBook:
    def __init__(self):
        self.s = set()

    def add(self, t):
        self.s.add(t)

    def remove(self, t):
        self.s.discard(t)

    def has(self, t):
        return t in self.s

    def longest_listed(self, q):
        best = None
        for i in range(1, len(q) + 1):
            if q[:i] in self.s:
                best = q[:i]
        return best

    def count_match(self, p):
        return sum(1 for t in self.s if len(t) == len(p) and all(a == b or a == '?' for a, b in zip(p, t)))


ok = True
for _ in range(100):
    a, b = TickerBook(), ListBook()
    for _ in range(40):
        op = random.choice('aarhlc')
        w = ''.join(random.choice('AB') for _ in range(random.randint(1, 3)))
        if op == 'a':
            a.add(w); b.add(w)
        elif op == 'r':
            a.remove(w); b.remove(w)
        elif op == 'h':
            ok &= a.has(w) == b.has(w)
        elif op == 'l':
            ok &= a.longest_listed(w) == b.longest_listed(w)
        else:
            p = ''.join(random.choice('AB?') for _ in range(random.randint(1, 3)))
            ok &= a.count_match(p) == b.count_match(p)
check(ok, 'h1 i1: TickerBook agrees with a set-based reference on 100 random op sequences')


def count_match_visits(book, pattern):
    visits = 0

    def go(node, i):
        nonlocal visits
        visits += 1
        if i == len(pattern):
            return 1 if node.get('#') else 0
        if pattern[i] == '?':
            return sum(go(c, i + 1) for k, c in node.items() if k != '#')
        child = node.get(pattern[i])
        return go(child, i + 1) if child else 0
    go(book.root, 0)
    return visits


small, big = TickerBook(), TickerBook()
for i in range(100):
    small.add(''.join('ABCDEFGH'[(i // 8 ** j) % 8] for j in range(4)))
for i in range(4096):
    big.add(''.join('ABCDEFGH'[(i // 8 ** j) % 8] for j in range(4)))
vs, vb = count_match_visits(small, '????'), count_match_visits(big, '????')
# content claim (h1 i1 prose and explain): every step costs time in proportion to the length of its argument,
# not the number of tickers listed. For count_match with '?' the nodes visited grow with the tickers, so this fails.
check(vb <= 2 * vs, 'h1 i1 prose: count_match(????) costs the same with 4,096 tickers as with 100 (content claim; visits %d against %d)' % (vb, vs))
check(count_match_visits(big, 'ABCD') == 5, 'h1 i1: without a ? the walk is one node per letter (5 visits for ABCD)')

ts_ns = ns_of(widget(H1, 'items[2]'))
two_singles = ts_ns['two_singles']
ok = True
for _ in range(300):
    pairs = [random.randint(-20, 20) for _ in range(random.randint(0, 5))]
    a, b = random.sample(range(-20, 21), 2)
    xs = pairs * 2 + [a, b]
    random.shuffle(xs)
    ok &= two_singles(xs) == sorted([a, b])
check(ok and (-1 & 1) == 1 and (-6 & 6) == 2, 'h1 i2: two_singles right on 300 random lists with negatives; x & -x works on negative ints')

sa_ns = ns_of(widget(H1, 'items[3]'))
shortest_at_least = sa_ns['shortest_at_least']


def brute_shortest(nums, k):
    best = -1
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i:j + 1]) >= k and (best < 0 or j - i + 1 < best):
                best = j - i + 1
    return best


ok = True
for _ in range(400):
    xs = [random.randint(-5, 9) for _ in range(random.randint(0, 10))]
    k = random.randint(1, 12)
    ok &= shortest_at_least(xs, k) == brute_shortest(xs, k)
check(ok, 'h1 i3: deque of prefix sums equals brute force on 400 random lists with negatives')

wm_ns = ns_of(widget(H1, 'items[4]'))
window_median = wm_ns['window_median']
ok = True
for _ in range(300):
    xs = [random.randint(0, 6) for _ in range(random.randint(1, 12))]
    w = random.randint(1, len(xs))
    truth = [float(statistics.median(xs[i:i + w])) for i in range(len(xs) - w + 1)]
    ok &= _close(window_median(xs, w), truth)
check(ok, 'h1 i4: two heaps with lazy deletion equal the sorted-window median on 300 random lists with repeats')
check(abs(4e6 * math.log2(4e6) / 1e6 - 87.7) < 0.05 and abs(4e6 * math.log10(4e6) / 1e6 - 26.4) < 0.05, 'h1 i6: 87.7 million comparisons (26.4 with log10)')
total = sum(bin(i).count('1') for i in range(100001))
by_col = 0
for b in range(17):
    period = 1 << (b + 1)
    full, rem = divmod(100001, period)
    by_col += full * (1 << b) + max(0, rem - (1 << b))
check(total == 815030 and by_col == 815030, 'h1 i7: set bits in 0..100,000 total 815,030 by direct sum and by column periods')
check(10000 * 26 * 8 == 2080000, 'h1 i8: 10,000 nodes x 208 bytes = 2,080,000')

print()
print(f'{len(FAILS)} failures')
for f in FAILS:
    print('  -', f)
sys.exit(1 if FAILS else 0)
