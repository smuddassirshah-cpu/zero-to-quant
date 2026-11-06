"""Second route for app/content/exams/mock-superday-developer.json. Exits 1 on any failure.

Route A is superday_developer_build.py. Route B here is independent: a Dijkstra over (account, transfers) states for
the hop-limited path, Python models of the price store and the slot pool for every C++ test, every C++ claim compiled
and run with g++ (and clang++ where the standard leaves room: copy elision), a cache simulation, an arrivals replay.
Every code solution passes its hidden tests and every starter fails one. A last pass reads every number in each item's
learner-visible strings: whole numbers 0 to 10 count as structure, every other number must match a route-B or given
value for that item to its printed precision. Then numbers_lib's check_wrongs() and report().
Run: python3 docs/briefs/mocks-scripts/superday_developer_check.py
"""
import bisect
import heapq
import itertools
import json
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'mock-superday-developer.json')


class Exam(Level):
    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
ITEM, PATH = {}, {}
for pi, p in enumerate(doc['parts']):
    for j, it in enumerate(p.get('items', [])):
        ITEM[it['id']] = it
        PATH[it['id']] = f'parts[{pi}].items[{j}]'
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, '' if ok else note)


def W(iid, part=None):
    it = ITEM[iid]
    return it['widget'] if part is None else it['parts'][part]['widget']


def key(iid, value, part=None):
    w = W(iid, part)
    rec(abs(w['answer'] - value) <= max(w['tol']['abs'] / 10, 1e-9), f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', 'route B differs')
    ex.expect('exam', f'{PATH[iid]}' + ('' if part is None else f'.parts[{part}]') + '.widget.answer', w['answer'])
    allow(iid, value, w['answer'], w['tol']['abs'])


def wrong(iid, wid, value, part=None):
    w = W(iid, part)
    hit = [x for x in w['wrong'] if x['id'] == wid]
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= 1e-9, f'{iid}{"" if part is None else f" part {part}"} wrong "{wid}" = {value!r}', f'found {hit}')
    allow(iid, value)


def all_wrongs(iid, ids, part=None):
    rec(sorted(x['id'] for x in W(iid, part).get('wrong', [])) == sorted(ids), f'{iid} wrong ids are {sorted(ids)}')


def opt(iid, text, part=None, correct=False):
    w = W(iid, part)
    hit = [o for o in w['options'] if o['text'] == text]
    rec(len(hit) == 1 and bool(hit[0].get('correct')) == correct, f'{iid} option {text!r} {"is the key" if correct else "is a distractor"}')


def choice_rules(iid, part=None):
    w = W(iid, part)
    rec(w.get('shuffle') is True, f'{iid} shuffle true')
    rec(sum(1 for o in w['options'] if o.get('correct')) == 1, f'{iid} exactly one key')
    rec(all(str(o.get('why', '')).startswith('You ') for o in w['options'] if not o.get('correct')), f'{iid} every why names the learner’s action')
    vals = []
    for o in w['options']:
        m = re.fullmatch(r'-?\d+(?:\.\d+)?', o['text'])
        vals.append((float(m.group(0)), o.get('correct', False)) if m else None)
    if all(vals):
        k = [v for v, c in vals if c][0]
        ds = [v for v, c in vals if not c]
        bad = any((a < k < b or b < k < a) and (abs(a * 10 - b) < 1e-12 or abs(b * 10 - a) < 1e-12 or abs((k - a) - (b - k)) < 1e-12)
                  for a, b in itertools.combinations(ds, 2))
        rec(not bad, f'{iid} key sits between no times-ten pair and no two equal slips')


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def gpp(src, out, *flags, cxx='g++'):
    d = tempfile.mkdtemp()
    f = os.path.join(d, 'm.cpp')
    open(f, 'w').write(src)
    r = sh([cxx, '-std=c++17', *flags, f, '-o', os.path.join(d, out)])
    return r.returncode == 0, os.path.join(d, out), r.stderr


ALLOC = r'''
#include <cstdlib>
#include <new>
static volatile int g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new[](std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
int alloc_count() { return g_allocs; }
void reset_alloc_count() { g_allocs = 0; }
'''


def cpp_case(src, t, alloc=False):
    main = (ALLOC if alloc else '') + src + '\n#include <iostream>\n#include <iomanip>\nint main() { ' + t['setup'] + \
        ' std::cout << std::setprecision(17) << (' + t['call'] + ') << "\\n"; }\n'
    ok, exe, _ = gpp(main, 'm', '-O1', *(['-fno-builtin'] if alloc else []))
    if not ok:
        return None
    return float(sh([exe], timeout=60).stdout.strip())


def cpp_passes(src, tests, alloc=False):
    n = 0
    for t in tests:
        got = cpp_case(src, t, alloc)
        if got is not None:
            tol = t.get('tol', {})
            n += math.isclose(got, float(t['expect']), rel_tol=tol.get('rel', 0), abs_tol=tol.get('abs', 0)) if t['compare'] == 'isclose' else got == t['expect']
    return n


# ======================================================================== A1: hop-limited path
def dijkstra_hops(n, routes, src, dst, k):
    k = min(k, n)
    adj = [[] for _ in range(n)]
    for a, b, fee in routes:
        adj[a].append((b, fee))
    seen = {}
    pq = [(0, src, 0)]
    while pq:
        c, u, h = heapq.heappop(pq)
        if u == dst:
            return c
        if seen.get((u, h), math.inf) < c or h == k:
            continue
        for v, fee in adj[u]:
            if c + fee < seen.get((v, h + 1), math.inf):
                seen[(v, h + 1)] = c + fee
                heapq.heappush(pq, (c + fee, v, h + 1))
    return -1


a1 = W('a1-cheapest-within-hops')
ok_all = True
for t in a1['tests']:
    ns = {'dijkstra_hops': dijkstra_hops}
    if t.get('setup'):
        exec(t['setup'], ns)
    b = eval(t['call'].replace('cheapest_within', 'dijkstra_hops'), ns)
    ok_all &= b == eval(t['expect'])
    rec(b == eval(t['expect']), f'a1 {t["call"][:60]} = {b} by Dijkstra over (account, transfers)')


def run_py(src, tests):
    passed = 0
    for t in tests:
        ns = {}
        try:
            exec(src, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            passed += eval(t['call'], ns) == eval(t['expect'])
        except Exception:  # noqa: BLE001
            pass
    return passed


rec(run_py(a1['solution'], a1['tests']) == len(a1['tests']), f'a1 solution passes {len(a1["tests"])} tests')
rec(run_py(a1['starter'], a1['tests']) < len(a1['tests']), 'a1 starter fails a test')
plain = '''import heapq
def cheapest_within(n, routes, src, dst, k):
    adj = [[] for _ in range(n)]
    for a, b, f in routes: adj[a].append((b, f))
    dist = {src: (0, 0)}; pq = [(0, 0, src)]
    while pq:
        c, h, u = heapq.heappop(pq)
        if u == dst: return c
        if dist[u] != (c, h) or h == k: continue
        for v, f in adj[u]:
            if v not in dist or c + f < dist[v][0]:
                dist[v] = (c + f, h + 1); heapq.heappush(pq, (c + f, h + 1, v))
    return -1
'''
trap = [t for t in a1['tests'] if t['call'].startswith('cheapest_within(4, [[0, 1, 1]') and t['call'].endswith(', 2)')]
rec(len(trap) == 1 and run_py(plain, trap) == 0, 'a1 a Dijkstra that keeps one cost per account fails the trap test')
allow('a1-cheapest-within-hops', 3000, 30000)

# ======================================================================== B1: price store
b1 = ITEM['b1-asof-store']
w1, w2 = b1['parts'][0]['widget'], b1['parts'][1]['widget']


class Store:
    def __init__(self):
        self.t, self.p = [], []

    def insert(self, t, px):
        i = bisect.bisect_left(self.t, t)
        if i < len(self.t) and self.t[i] == t:
            self.p[i] = px
        else:
            self.t.insert(i, t)
            self.p.insert(i, px)

    def asof(self, t):
        i = bisect.bisect_right(self.t, t)
        return self.p[i - 1] if i else -1.0

    def asof_fresh(self, t, age):
        i = bisect.bisect_right(self.t, t)
        return -1.0 if not i or t - self.t[i - 1] > age else self.p[i - 1]

    def erase_before(self, t):
        i = bisect.bisect_left(self.t, t)
        del self.t[:i], self.p[:i]


def two():
    s = Store(); s.insert(10, 101.5); s.insert(5, 100.0); return s


def fresh():
    s = Store(); s.insert(100, 50.0); s.insert(130, 51.0); return s


s3 = Store(); s3.insert(3, 1.0); s3.insert(3, 2.0)
big_total = sum(100.0 + t % 97 for t in range(100000))      # query q = 10t + 5 sees the tick at 10t, priced 100 + t % 97
win = Store()
for t in range(45000, 50000):                                 # the last erase_before(45000) keeps 45,000 to 49,999
    win.t.append(t); win.p.append(t * 0.5)
f4, f5, f6 = fresh(), fresh(), fresh()
f4.erase_before(130); f5.erase_before(130); f6.erase_before(1000)
want1 = [two().asof(7), two().asof(10), two().asof(4), two().asof(1000), s3.asof(3) + 10 * len(s3.t), Store().asof(0), big_total]
want2 = [fresh().asof_fresh(140, 15), fresh().asof_fresh(150, 15), fresh().asof_fresh(145, 15), f4.asof(129) * 1000 + len(f4.t), f5.asof(130),
         len(f6.t), len(win.t) + win.asof_fresh(49999, 0)]
rec(len(w1['tests']) == len(want1) and all(math.isclose(float(t['expect']), v, rel_tol=1e-12) for t, v in zip(w1['tests'], want1)), f'b1 part 1 expects match the Python model {want1}')
rec(len(w2['tests']) == len(want2) and all(math.isclose(float(t['expect']), v, rel_tol=1e-12, abs_tol=1e-12) for t, v in zip(w2['tests'], want2)), f'b1 part 2 expects match the Python model {want2}')
rec(cpp_passes(w1['solution'], w1['tests']) == len(w1['tests']), 'b1 part 1 C++ solution passes its tests (g++)')
rec(cpp_passes(w1['starter'], w1['tests']) < len(w1['tests']), 'b1 part 1 starter fails a test')
t12 = w1['tests'] + w2['tests']
rec(cpp_passes(w2['solution'], t12) == len(t12), f'b1 part 2 C++ solution passes all {len(t12)} merged tests (g++)')
rec(cpp_passes(w2['starter'], t12) < len(t12), 'b1 part 2 starter fails a test')
rec(len(t12) <= 15, f'b1 merged tests {len(t12)} <= 15')
rec(all('try' not in w['solution'] and 'catch' not in w['solution'] for w in (w1, w2)), 'b1 uses no try or catch')
opt('b1-asof-store', '`upper_bound` skips a tick at exactly `t`, so the step back lands on it', part=2, correct=True)
choice_rules('b1-asof-store', 2)
allow('b1-asof-store', 100000, 1e10, 1.0, 10)

# ======================================================================== K1: padding
ORDER = 'struct Order {\n    bool live;\n    double price;\n    int qty;\n    char side;\n};\n'
ok, exe, _ = gpp('#include <cstdio>\n' + ORDER + 'int main() { std::printf("%zu", sizeof(Order)); }\n', 'k1', '-O1')
size0 = int(sh([exe]).stdout)
members = ['bool live;', 'double price;', 'int qty;', 'char side;']
sizes = []
for perm in itertools.permutations(members):
    ok, exe, _ = gpp('#include <cstdio>\nstruct O { ' + ' '.join(perm) + ' };\nint main() { std::printf("%zu", sizeof(O)); }\n', 'k1p', '-O1')
    sizes.append(int(sh([exe]).stdout))
rec(size0 == 24 and min(sizes) == 16, f'k1 g++ sizeof {size0}; the smallest of 24 orders is {min(sizes)}')
key('k1-struct-padding', size0, 0)
wrong('k1-struct-padding', 'summed', 1 + 8 + 4 + 1, 0)
wrong('k1-struct-padding', 'all-eight', 4 * 8, 0)
all_wrongs('k1-struct-padding', ['summed', 'all-eight'], 0)
key('k1-struct-padding', min(sizes), 1)
wrong('k1-struct-padding', 'no-tail', 14, 1)
wrong('k1-struct-padding', 'unchanged', size0, 1)
all_wrongs('k1-struct-padding', ['no-tail', 'unchanged'], 1)
allow('k1-struct-padding', 16, 20, 24, 14, 64, 32)

# ======================================================================== K2: copies
k2 = ITEM['k2-copies-counted']
code = re.search(r'```cpp\n(.*?)```', k2['prose'], re.S).group(1)
prog = '#include <cstdio>\n#include <utility>\n#include <vector>\n' + code.replace('    v.emplace_back();\n}', '    v.emplace_back();\n    std::printf("%d %d", Tick::copies, Tick::moves);\n}')
counts = set()
for cxx, flags in (('g++', ['-O0']), ('g++', ['-O1']), ('g++', ['-O0', '-fno-elide-constructors']), ('clang++', ['-O1'])):
    ok, exe, err = gpp(prog, 'k2', *flags, cxx=cxx)
    if ok:
        counts.add(sh([exe]).stdout.split()[0])
rec(counts == {'1'}, f'k2 copies under g++ -O0, -O1, -fno-elide-constructors and clang++: {sorted(counts)}')
opt('k2-copies-counted', '1', correct=True)
for d in ('2', '3', '4'):
    opt('k2-copies-counted', d)
choice_rules('k2-copies-counted')

# ======================================================================== K3: double delete
k3 = ITEM['k3-shallow-copy']
code = re.search(r'```cpp\n(.*?)```', k3['prose'], re.S).group(1)
probe = r'''#include <cstdio>
#include <cstdlib>
#include <new>
static void* seen[16]; static int nseen = 0, twice = 0;
void* operator new[](std::size_t n) { return std::malloc(n); }
void operator delete[](void* p) noexcept { for (int i = 0; i < nseen; ++i) if (seen[i] == p) { ++twice; return; } seen[nseen++] = p; }
void operator delete[](void* p, std::size_t) noexcept { operator delete[](p); }
''' + code + 'int main() { report(); std::printf("%d", twice); }\n'
ok, exe, err = gpp(probe, 'k3', '-O0')
rec(ok and sh([exe]).stdout == '1', 'k3 the same block is deleted twice (a counting operator delete[] sees it)')
choice_rules('k3-shallow-copy')
allow('k3-shallow-copy', 100)

# ======================================================================== K4: dispatch during construction
k4 = ITEM['k4-virtual-in-constructor']
code = re.search(r'```cpp\n(.*?)```', k4['prose'], re.S).group(1)
ok, exe, err = gpp(code, 'k4', '-O1')
out = sh([exe]).stdout.strip()
rec(out == 'base tree tree base', f'k4 prints {out!r}')
opt('k4-virtual-in-constructor', f'`{out}`', correct=True)
choice_rules('k4-virtual-in-constructor')

# ======================================================================== K5: template deduction
k5 = ITEM['k5-template-deduction']
tmpl = re.search(r'```cpp\n(.*?)```', k5['prose'], re.S).group(1)
fails = []
for o in W('k5-template-deduction')['options']:
    call = o['text'].strip('`')
    r = sh(['g++', '-std=c++17', '-fsyntax-only', '-x', 'c++', '-'], input='#include <string>\n' + tmpl + f'void f() {{ (void){call}; }}\n')
    fails.append((call, r.returncode != 0, bool(o.get('correct'))))
rec(all(f == c for _, f, c in fails), f'k5 only the key fails to compile: {[(c, f) for c, f, _ in fails]}')
choice_rules('k5-template-deduction')
allow('k5-template-deduction', 101.5, 100)

# ======================================================================== K6: slot pool
k6 = W('k6-slot-pool')


class Pool:
    def __init__(self, cap):
        self.cap, self.stack, self.used, self.fresh = cap, [], [False] * cap, 0

    def acquire(self):
        if self.stack:
            s = self.stack.pop()
        elif self.fresh < self.cap:
            s, self.fresh = self.fresh, self.fresh + 1
        else:
            return -1
        self.used[s] = True
        return s

    def release(self, s):
        if 0 <= s < self.cap and self.used[s]:
            self.used[s] = False
            self.stack.append(s)

    def in_use(self):
        return sum(self.used)


def model(case):
    if case == 0:
        p = Pool(3); a, b, c = p.acquire(), p.acquire(), p.acquire(); return a * 100 + b * 10 + c
    if case == 1:
        p = Pool(2); p.acquire(); p.acquire(); return p.acquire()
    if case in (2, 3):
        p = Pool(4)
        for _ in range(4):
            p.acquire()
        p.release(2); p.release(0)
        if case == 2:
            return p.acquire()
        x, y = p.acquire(), p.acquire(); return x * 10 + y
    if case == 4:
        p = Pool(5); p.acquire(); p.acquire(); p.release(1); x, y = p.acquire(), p.acquire(); return x * 10 + y
    if case in (5, 6):
        p = Pool(3); a = p.acquire(); p.release(a); p.release(a)
        if case == 5:
            p.release(7); p.release(-1); return p.in_use()
        x, y = p.acquire(), p.acquire(); return x * 10 + y
    if case == 7:
        p = Pool(10)
        for _ in range(7):
            p.acquire()
        p.release(3); p.release(5); return p.in_use()
    if case == 8:
        return Pool(0).acquire()
    if case == 9:
        return 0
    p = Pool(100000)
    tot = sum(p.acquire() for _ in range(100000))
    for i in range(0, 100000, 2):
        p.release(i)
    return tot + sum(p.acquire() for _ in range(50000))


want = [model(i) for i in range(len(k6['tests']))]
rec([t['expect'] for t in k6['tests']] == want, f'k6 every expect matches the Python model {want}')
rec(cpp_passes(k6['solution'], k6['tests'], alloc=True) == len(k6['tests']), f'k6 C++ solution passes {len(k6["tests"])} tests (g++, counting operator new)')
rec(cpp_passes(k6['starter'], k6['tests'], alloc=True) < len(k6['tests']), 'k6 starter fails a test')
vec = '''#include <set>
class SlotPool {
public:
    explicit SlotPool(int c) { for (int i = 0; i < c; ++i) free_.insert(i); }
    int acquire() { if (free_.empty()) return -1; int s = *free_.begin(); free_.erase(free_.begin()); used_.insert(s); return s; }
    void release(int s) { if (used_.erase(s)) free_.insert(s); }
    int in_use() const { return static_cast<int>(used_.size()); }
private:
    std::set<int> free_, used_;
};
'''
alloc_test = [t for t in k6['tests'] if t['call'] == 'alloc_count()']
rec(len(alloc_test) == 1 and cpp_passes(vec, alloc_test, alloc=True) == 0, 'k6 a version built on std::set fails the allocation test')
rec(k6.get('allocCheck') is True and 'try' not in k6['solution'], 'k6 allocCheck on, no try or catch')
allow('k6-slot-pool', 1)

# ======================================================================== Y1 to Y5
y1 = ITEM['y1-lost-updates']
atomic_prog = '#include <atomic>\n#include <cstdio>\n#include <thread>\nstd::atomic<int> hits{0};\nvoid work() { for (int i = 0; i < 1000000; ++i) ++hits; }\nint main() { std::thread a(work), b(work); a.join(); b.join(); std::printf("%d", hits.load()); }\n'
ok, exe, err = gpp(atomic_prog, 'y1', '-O1', '-pthread')
rec(ok and all(sh([exe]).stdout == '2000000' for _ in range(3)), 'y1 the atomic counter ends at 2,000,000 in three runs')
choice_rules('y1-lost-updates')
allow('y1-lost-updates', 2000000, 1000000)
choice_rules('y2-relaxed-flag')
allow('y2-relaxed-flag', 42)
lock_prog = ('#include <cstdio>\n#include <mutex>\n#include <thread>\nstruct Book { std::mutex m; long cash = 1000000; };\nBook alpha, beta;\n'
             'void move_cash(Book& src, Book& dst, long pence) { std::scoped_lock lk(src.m, dst.m); src.cash -= pence; dst.cash += pence; }\n'
             'int main() { std::thread a([] { for (int i = 0; i < 200000; ++i) move_cash(alpha, beta, 100); });\n'
             'std::thread b([] { for (int i = 0; i < 200000; ++i) move_cash(beta, alpha, 50); }); a.join(); b.join();\n'
             'std::printf("%ld", alpha.cash + beta.cash); }\n')
ok, exe, err = gpp(lock_prog, 'y3', '-O1', '-pthread')
rec(ok and sh([exe], timeout=60).stdout == '2000000', 'y3 the scoped_lock version finishes 400,000 opposite transfers and keeps the total')
choice_rules('y3-lock-order')
allow('y3-lock-order', 100, 50)


def misses(n, order, lines_cap=16, per_line=8):
    """LRU cache of lines_cap lines over an n by n row-major matrix of doubles"""
    cache, miss = [], 0
    for a in range(n):
        for b in range(n):
            i, j = (a, b) if order == 'row' else (b, a)
            line = (i * n + j) // per_line
            if line in cache:
                cache.remove(line)
            else:
                miss += 1
                if len(cache) == lines_cap:
                    cache.pop(0)
            cache.append(line)
    return miss


r_, c_ = misses(256, 'row'), misses(256, 'col')
rec(c_ / r_ == 8, f'y4 a 256 by 256 simulation: {c_} column misses against {r_} row misses, ratio {c_ / r_}')
key('y4-column-sum', c_ / r_)
wrong('y4-column-sum', 'bytes', 64)
wrong('y4-column-sum', 'row-length', 4096)
all_wrongs('y4-column-sum', ['bytes', 'row-length'])
allow('y4-column-sum', 4096, 64, 8)

# Y5: arrivals every 1/150,000 s, each staying 40 us: count inside at 1,000 sample times, in integer nanoseconds
gap_ns, stay_ns = 10 ** 9 / 150000, 40000
arr = [round(i * gap_ns) for i in range(200000)]
inside = [sum(1 for a in arr[max(0, int(s // gap_ns) - 10):int(s // gap_ns) + 2] if a <= s < a + stay_ns) for s in range(500000, 1000000, 499)]
rec(set(inside) == {6}, f'y5 the replay has {sorted(set(inside))} inside')
key('y5-littles-law', 150000 * 40e-6, 0)
wrong('y5-littles-law', 'ms', 150000 * 40e-3, 0)
wrong('y5-littles-law', 'divided', 150000 / 40, 0)
all_wrongs('y5-littles-law', ['ms', 'divided'], 0)
need = 4 * 6
pow2 = 1 << (need - 1).bit_length()
key('y5-littles-law', pow2, 1)
wrong('y5-littles-law', 'not-power', need, 1)
wrong('y5-littles-law', 'rounded-down', pow2 // 2, 1)
all_wrongs('y5-littles-law', ['not-power', 'rounded-down'], 1)
allow('y5-littles-law', 150000, 40, 0.00004, 24, 32, 31, 10 ** -6, 6)

# ======================================================================== longform and fit numbers
allow('g1-risk-gateway', 200000, 5, 1, 99, 350)
allow('g2-tail-regression', 8, 30, 99, 250)
allow('f1-why-trading-systems', 40, 9, 99, 200, 90)
allow('f2-review-disagreement', 200)
rec(200000 * 5e-6 == 1.0 and 1 / 200000 == 5e-6, 'g1 one order every 5 us; Little gives 1 in flight at 5 us')

# ======================================================================== structure
rec([p.get('minutes') for p in doc['parts'] if p['kind'] == 'paper'] == [45, 45, 40, 25, 45, 15], 'papers 45, 45, 40, 25, 45, 15 minutes')
rec(sum(len(p.get('items', [])) for p in doc['parts']) == 17, '17 items')
rec(sum(1 for it in ITEM.values() if it.get('kind') == 'longform') == 4, 'four longform items')
rec(all(sum(r['points'] for r in it['rubric']) == 10 for it in ITEM.values() if it.get('kind') == 'longform'), 'every rubric sums to 10')
for it in ITEM.values():
    for w in ([it['widget']] if 'widget' in it else [p['widget'] for p in it.get('parts', [])]):
        if w['kind'] == 'choice':
            rec(w.get('shuffle') is True, f'{it["id"]}: every choice shuffled')
firms = ('Hudson', 'Two Sigma', 'Jane Street', 'Citadel', 'Optiver', 'Goldman')
rec(not any(f in json.dumps(it) for it in ITEM.values() for f in firms), 'no firm named outside models and description')
rec('Reported' in doc['models'] and 'Nov 2026' in doc['models'] and 'Nov 2026' in doc['description'], 'models and description say reported, Nov 2026')
rec(len(doc['models']) <= 200, f'models is {len(doc["models"])} characters')
others = [json.load(open(os.path.join(ROOT, 'app', 'content', 'exams', f))) for f in sorted(os.listdir(os.path.join(ROOT, 'app', 'content', 'exams')))
          if f.startswith('mock-') and f != 'mock-superday-developer.json']


def all_items(d):
    for p in d.get('parts', [d]):
        for it in p.get('items', []) or []:
            if isinstance(it, dict):
                yield it


norm = lambda it: re.sub(r'\W+', ' ', str(it.get('question', it.get('prompt', '')))).strip().lower()
seen_q = {norm(it) for d in others for it in all_items(d)}
seen_t = {it.get('tags', [''])[0] for d in others for it in all_items(d) if it.get('tags')}
rec(not ({norm(it) for it in ITEM.values()} & seen_q - {''}), 'no question text repeats another mock')
rec(not ({it['tags'][0] for it in ITEM.values()} & seen_t), f'no family tag repeats another mock {sorted({it["tags"][0] for it in ITEM.values()} & seen_t)}')

# ======================================================================== every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'starter', 'solution', 'tests', 'examples', 'skills', 'placeholder', 'how', 'signature', 'label'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)
    s = re.sub(r'`[^`]*`', ' ', s)
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t and 'e' not in t.lower() else 0), t


for iid, it in ITEM.items():
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v for k, v in it.items() if k not in ('difficulty', 'pace')}):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
