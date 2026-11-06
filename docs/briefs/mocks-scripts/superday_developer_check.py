"""Second route for app/content/exams/mock-superday-developer.json. Exits 1 on any failure.

Route A is superday_developer_build.py. Route B here is independent: a label-setting search over sites with each site's
runs sorted by departure and found by bisection for the earliest arrival, Python models of the price store and the slot pool for every C++ test, every C++ claim compiled
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


def cpp_case(src, t, alloc=False, cap=60):
    main = (ALLOC if alloc else '') + src + '\n#include <iostream>\n#include <iomanip>\nint main() { ' + t['setup'] + \
        ' std::cout << std::setprecision(17) << (' + t['call'] + ') << "\\n"; }\n'
    ok, exe, _ = gpp(main, 'm', '-O1', *(['-fno-builtin'] if alloc else []))
    if not ok:
        return None
    try:
        return float(sh([exe], timeout=cap).stdout.strip())
    except subprocess.TimeoutExpired:
        return None


def cpp_passes(src, tests, alloc=False, cap=60, stop_at_first_fail=False):
    n = 0
    for t in tests:
        got = cpp_case(src, t, alloc, cap)
        if got is None and stop_at_first_fail:
            return n
        if got is not None:
            tol = t.get('tol', {})
            n += math.isclose(got, float(t['expect']), rel_tol=tol.get('rel', 0), abs_tol=tol.get('abs', 0)) if t['compare'] == 'isclose' else got == t['expect']
    return n


# ======================================================================== A1: earliest arrival
def arrival_dijkstra(n, runs, src, dst, t0):
    """route B: label-setting search; each site's runs sorted by departure, the first boardable one found by bisection"""
    adj = [[] for _ in range(n)]
    for a, b, d, r in runs:
        adj[a].append((d, r, b))
    for lst in adj:
        lst.sort()
    dist = [math.inf] * n
    dist[src] = t0
    pq = [(t0, src)]
    while pq:
        t, u = heapq.heappop(pq)
        if t > dist[u]:
            continue
        for d, r, v in adj[u][bisect.bisect_left(adj[u], (t, -math.inf, -1)):]:
            if r < dist[v]:
                dist[v] = r
                heapq.heappush(pq, (r, v))
    return -1 if dist[dst] == math.inf else dist[dst]


a1 = W('a1-earliest-arrival')


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


for t in a1['tests']:
    ns = {'arrival_dijkstra': arrival_dijkstra}
    if t.get('setup'):
        exec(t['setup'], ns)
    b = eval(t['call'].replace('earliest_arrival', 'arrival_dijkstra'), ns)
    rec(b == eval(t['expect']), f'a1 {t["call"][:60]} = {b} by a label-setting search with bisection')
rec(run_py(a1['solution'], a1['tests']) == len(a1['tests']), f'a1 solution passes {len(a1["tests"])} tests')
rec(run_py(a1['starter'], a1['tests']) < len(a1['tests']), 'a1 starter fails a test')
rec(len(a1['tests']) <= 15, f'a1 {len(a1["tests"])} tests <= 15')
sol_a = a1['solution']
EA_WRONGS = {
    'plain Dijkstra on run lengths': (
        'import heapq\ndef earliest_arrival(n, runs, src, dst, t0):\n    adj = [[] for _ in range(n)]\n'
        '    for a, b, d, r in runs: adj[a].append((b, r - d))\n    dist = [float("inf")] * n; dist[src] = 0; pq = [(0, src)]\n'
        '    while pq:\n        c, u = heapq.heappop(pq)\n        if c > dist[u]: continue\n        for v, w in adj[u]:\n'
        '            if c + w < dist[v]: dist[v] = c + w; heapq.heappush(pq, (c + w, v))\n'
        '    return -1 if dist[dst] == float("inf") else t0 + dist[dst]\n'),
    'boards only if strictly earlier': sol_a.replace('best[a] <= depart', 'best[a] < depart'),
    'no waiting, must arrive exactly at departure': sol_a.replace('best[a] <= depart', 'best[a] == depart'),
    'ignores t0': sol_a.replace('best[src] = t0', 'best[src] = 0'),
    'runs taken in the order given': sol_a.replace('sorted(runs, key=lambda run: run[2])', 'runs'),
    'stops at the first run that reaches dst': sol_a.replace('            best[b] = arrive\n', '            best[b] = arrive\n            if b == dst:\n                return arrive\n'),
}
for name, src in EA_WRONGS.items():
    rec(src != sol_a and run_py(src, a1['tests']) < len(a1['tests']), f'a1 planted wrong "{name}" fails {len(a1["tests"]) - run_py(src, a1["tests"])} of {len(a1["tests"])} tests')
allow('a1-earliest-arrival', 3000, 30000, 6, 20)

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
big_total = sum(100.0 + t % 97 for t in range(200000))      # query q = 10t + 5 sees the tick at 10t, priced 100 + t % 97
win = Store()
for t in range(49000, 50000):                                 # the last erase_before(49000) keeps 49,000 to 49,999
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
opt('b1-asof-store', '`upper_bound` passes a tick at `t`; one step back finds it', part=2, correct=True)
choice_rules('b1-asof-store', 2)
allow('b1-asof-store', 200000, 1e10, 4e10, 1.0, 10)
rec(big_total == 29599419.0, f'b1 the large total {big_total}')
STORE_FULL = """#include <algorithm>
#include <iterator>
#include <utility>
#include <vector>

class PriceStore {
public:
    void insert(long long t, double px) {
        auto it = std::lower_bound(v_.begin(), v_.end(), std::make_pair(t, -1e300));
        if (it != v_.end() && it->first == t) it->second = px;
        else v_.insert(it, std::make_pair(t, px));
    }
    double asof(long long t) const {
        auto it = std::upper_bound(v_.begin(), v_.end(), std::make_pair(t, 1e300));
        if (it == v_.begin()) return -1.0;
        return std::prev(it)->second;
    }
    int size() const { return static_cast<int>(v_.size()); }
    double asof_fresh(long long t, long long max_age) const {
        auto it = std::upper_bound(v_.begin(), v_.end(), std::make_pair(t, 1e300));
        if (it == v_.begin()) return -1.0;
        --it;
        return t - it->first > max_age ? -1.0 : it->second;
    }
    void erase_before(long long t) { v_.erase(v_.begin(), std::lower_bound(v_.begin(), v_.end(), std::make_pair(t, -1e300))); }

private:
    std::vector<std::pair<long long, double>> v_;
};
"""
sol2 = w2['solution']
B1_WRONGS = {
    'a sorted vector with insert': STORE_FULL,
    'lower_bound in place of upper_bound': sol2.replace('ticks_.upper_bound(t)', 'ticks_.lower_bound(t)'),
    'a scan of the map per query': sol2.replace('        auto it = ticks_.upper_bound(t);\n        if (it == ticks_.begin()) return -1.0;\n        return std::prev(it)->second;',
                                                '        double best = -1.0;\n        for (const auto& kv : ticks_) { if (kv.first > t) break; best = kv.second; }\n        return best;'),
    'age test at least max_age': sol2.replace('t - it->first > max_age', 't - it->first >= max_age'),
    'erase_before also drops the tick at t': sol2.replace('ticks_.lower_bound(t)', 'ticks_.upper_bound(t)'),
}
for name, src in B1_WRONGS.items():
    rec(src != sol2, f'b1 planted wrong "{name}" differs from the solution')
    got = cpp_passes(src, t12, cap=5, stop_at_first_fail=False)
    rec(got < len(t12), f'b1 planted wrong "{name}" passes {got} of {len(t12)} tests (5 s cap on each)')

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

# ======================================================================== K6: slot pool with generation handles
k6 = W('k6-slot-pool')


class Pool:
    def __init__(self, cap):
        self.cap, self.stack, self.used, self.fresh, self.gen = cap, [], [False] * cap, 0, [0] * cap

    def acquire(self):
        if self.stack:
            s = self.stack.pop()
        elif self.fresh < self.cap:
            s, self.fresh = self.fresh, self.fresh + 1
        else:
            return -1
        self.used[s] = True
        return s + self.cap * self.gen[s]

    def _live(self, h):
        if h < 0 or self.cap == 0:
            return -1
        s, g = h % self.cap, h // self.cap
        return s if self.used[s] and self.gen[s] == g else -1

    def release(self, h):
        s = self._live(h)
        if s >= 0:
            self.used[s] = False
            self.gen[s] += 1
            self.stack.append(s)

    def valid(self, h):
        return self._live(h) >= 0

    def in_use(self):
        return sum(self.used)


def model(case):
    if case == 0:
        p = Pool(3); a, b, c = p.acquire(), p.acquire(), p.acquire(); return a * 100 + b * 10 + c
    if case == 1:
        p = Pool(2); p.acquire(); p.acquire(); return p.acquire()
    if case == 2:
        p = Pool(4)
        for _ in range(4):
            p.acquire()
        p.release(0); p.release(2); x, y = p.acquire(), p.acquire(); return (x % 4) * 10 + y % 4
    if case == 3:
        p = Pool(4); a = p.acquire(); p.release(a); return p.acquire()
    if case == 4:
        p = Pool(3); a = p.acquire(); p.release(a); b = p.acquire(); p.release(a); return p.in_use() * 10 + int(p.valid(b))
    if case == 5:
        p = Pool(3); a, b = p.acquire(), p.acquire(); p.release(a); return 100 * p.valid(a) + 10 * p.valid(b) + int(p.valid(7))
    if case == 6:
        p = Pool(3); p.acquire(); p.release(-1); p.release(7); p.release(2); return p.in_use()
    if case == 7:
        p = Pool(3); a = p.acquire(); p.release(a); p.release(a); x, y = p.acquire(), p.acquire(); return x * 100 + y
    if case == 8:
        p = Pool(10); h = [p.acquire() for _ in range(7)]; p.release(h[3]); p.release(h[5]); return p.in_use()
    if case == 9:
        p = Pool(0); return p.acquire() * 10 + int(p.valid(0))
    if case == 10:
        p = Pool(3)
        for _ in range(1000):
            p.release(p.acquire())
        return p.acquire()
    if case == 11:
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
rec(len(k6['tests']) <= 15, f'k6 {len(k6["tests"])} tests <= 15')
sol_k = k6['solution']
HEAP = """#include <algorithm>
#include <functional>
#include <vector>

class SlotPool {
public:
    explicit SlotPool(int capacity) : cap_(capacity), gen_(capacity, 0), used_(capacity, 0) {
        heap_.reserve(capacity);
        for (int i = 0; i < capacity; ++i) heap_.push_back(i);
    }
    long long acquire() {
        if (heap_.empty()) return -1;
        std::pop_heap(heap_.begin(), heap_.end(), std::greater<int>());
        const int s = heap_.back();
        heap_.pop_back();
        used_[s] = 1;
        ++count_;
        return s + static_cast<long long>(cap_) * gen_[s];
    }
    void release(long long handle) {
        const int s = live_slot(handle);
        if (s < 0) return;
        used_[s] = 0;
        ++gen_[s];
        heap_.push_back(s);
        std::push_heap(heap_.begin(), heap_.end(), std::greater<int>());
        --count_;
    }
    bool valid(long long handle) const { return live_slot(handle) >= 0; }
    int in_use() const { return count_; }

private:
    int live_slot(long long handle) const {
        if (handle < 0 || cap_ == 0) return -1;
        const int s = static_cast<int>(handle % cap_);
        return used_[s] && gen_[s] == handle / cap_ ? s : -1;
    }
    int cap_;
    std::vector<int> heap_, gen_;
    std::vector<char> used_;
    int count_ = 0;
};
"""
FIFO = """#include <vector>

class SlotPool {
public:
    explicit SlotPool(int capacity) : cap_(capacity), q_(capacity), gen_(capacity, 0), used_(capacity, 0), n_(capacity) {
        for (int i = 0; i < capacity; ++i) q_[i] = i;
    }
    long long acquire() {
        if (n_ == 0) return -1;
        const int s = q_[head_];
        head_ = (head_ + 1) % cap_;
        --n_;
        used_[s] = 1;
        ++count_;
        return s + static_cast<long long>(cap_) * gen_[s];
    }
    void release(long long handle) {
        const int s = live_slot(handle);
        if (s < 0) return;
        used_[s] = 0;
        ++gen_[s];
        q_[(head_ + n_) % cap_] = s;
        ++n_;
        --count_;
    }
    bool valid(long long handle) const { return live_slot(handle) >= 0; }
    int in_use() const { return count_; }

private:
    int live_slot(long long handle) const {
        if (handle < 0 || cap_ == 0) return -1;
        const int s = static_cast<int>(handle % cap_);
        return used_[s] && gen_[s] == handle / cap_ ? s : -1;
    }
    int cap_;
    std::vector<int> q_, gen_;
    std::vector<char> used_;
    int n_;
    int head_ = 0;
    int count_ = 0;
};
"""
GROW = """#include <vector>

class SlotPool {
public:
    explicit SlotPool(int capacity) : cap_(capacity), gen_(capacity, 0), used_(capacity, 0) {}
    long long acquire() {
        int s;
        if (!free_.empty()) { s = free_.back(); free_.pop_back(); }
        else if (next_ < cap_) s = next_++;
        else return -1;
        used_[s] = 1;
        ++count_;
        return s + static_cast<long long>(cap_) * gen_[s];
    }
    void release(long long handle) {
        const int s = live_slot(handle);
        if (s < 0) return;
        used_[s] = 0;
        ++gen_[s];
        free_.push_back(s);
        --count_;
    }
    bool valid(long long handle) const { return live_slot(handle) >= 0; }
    int in_use() const { return count_; }

private:
    int live_slot(long long handle) const {
        if (handle < 0 || cap_ == 0) return -1;
        const int s = static_cast<int>(handle % cap_);
        return used_[s] && gen_[s] == handle / cap_ ? s : -1;
    }
    int cap_;
    std::vector<int> free_, gen_;
    std::vector<char> used_;
    int next_ = 0;
    int count_ = 0;
};
"""
K6_WRONGS = {
    'a min-heap of free slots (lowest free first), reserved in the constructor': HEAP,
    'no generation counter, the handle is the slot': sol_k.replace('        ++gen_[s];\n', ''),
    'generation raised at acquire, not at release': sol_k.replace('        ++gen_[s];\n', '').replace('        used_[s] = 1;\n', '        used_[s] = 1;\n        ++gen_[s];\n'),
    'no in-use flag': sol_k.replace('return used_[s] && gen_[s] == g ? s : -1;', 'return gen_[s] == g ? s : -1;'),
    'first in, first out reuse': FIFO,
    'a free list that grows (no reserve)': GROW,
}
for name, src in K6_WRONGS.items():
    rec(src != sol_k, f'k6 planted wrong "{name}" differs from the solution')
    got = cpp_passes(src, k6['tests'], alloc=True, cap=5)
    rec(got < len(k6['tests']), f'k6 planted wrong "{name}" passes {got} of {len(k6["tests"])} tests')
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
paper = {p['id']: p for p in doc['parts'] if p['kind'] == 'paper'}
rec(paper['round-one']['pass'] == 1 and paper['round-two']['pass'] == 1, 'both coding rounds need every part (pass 1), so the added requirement cannot be skipped')
rec(sum(it['pace'] for it in paper['cpp']['items']) <= paper['cpp']['minutes'] * 60 - 120, 'cpp paces leave at least 120 s for the compiler start')
rec('concurrency' not in doc['models'].lower(), 'models does not list concurrency')
rec('This mock is built from reports' in doc['description'], 'the description states only the reported format')
rec(sum(r['points'] for r in ITEM['g1-risk-gateway']['rubric'] if 'Replays' in r['text'] or 'Measures latency' in r['text']) == 2, 'g1 testing earns two points, one each for replay and the latency gate')
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
