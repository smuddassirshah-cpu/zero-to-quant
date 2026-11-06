"""Build app/content/exams/mock-superday-developer.json (route A: closed forms and reference code).

Deterministic: random.Random(2612) orders the choice options only; every parameter is fixed below. Code test
expectations come from the reference solutions, run in CPython (Python) and compiled by g++ (C++, with a counting
operator new standing in for the app's allocCheck harness). superday_developer_check.py recomputes every key and
every test value by a second route.
Run: python3 docs/briefs/mocks-scripts/superday_developer_build.py
"""
import math
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from superday_lib import numeric, choice, fb, item, part, parts_item, longform, write  # noqa: E402

OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-superday-developer.json')
rng = random.Random(2612)

ALLOC_HARNESS = r'''
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


def run_cpp(src, setup, call, alloc=False):
    """compile src with a main that runs setup then prints call; returns the printed text"""
    with tempfile.TemporaryDirectory() as td:
        main = ((ALLOC_HARNESS if alloc else '') + src + '\n#include <iostream>\n#include <iomanip>\nint main() { '
                + setup + ' std::cout << std::setprecision(17) << (' + call + ') << "\\n"; }\n')
        open(os.path.join(td, 'm.cpp'), 'w').write(main)
        flags = ['-fno-builtin'] if alloc else []
        subprocess.run(['g++', '-std=c++17', '-O1', *flags, os.path.join(td, 'm.cpp'), '-o', os.path.join(td, 'm')], check=True)
        return subprocess.run([os.path.join(td, 'm')], capture_output=True, text=True, check=True, timeout=60).stdout.strip()


def num(text):
    v = float(text)
    return int(v) if v == int(v) and 'e' not in text and '.' not in text else v


# ======================================================================== paper 1: coding round one (Python)
HOPS_SOL = '''def cheapest_within(n, routes, src, dst, k):
    INF = float("inf")
    best = [INF] * n
    best[src] = 0
    for _ in range(min(k, n - 1)):
        nxt = best[:]
        changed = False
        for a, b, fee in routes:
            if best[a] + fee < nxt[b]:
                nxt[b] = best[a] + fee
                changed = True
        best = nxt
        if not changed:
            break
    return -1 if best[dst] == INF else best[dst]
'''
HOPS_START = ('def cheapest_within(n, routes, src, dst, k):\n'
              '    """Smallest total fee from src to dst in at most k transfers, or -1."""\n    ...\n')
BASE4 = '[[0, 1, 100], [1, 2, 100], [2, 3, 100], [0, 3, 500], [0, 2, 250]]'
TRAP = '[[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 3, 1]]'
RAND = 'import random; R = random.Random(11); routes = [[R.randrange(3000), R.randrange(3000), R.randint(1, 500)] for _ in range(30000)]'
CHAIN = 'routes = [[i, i + 1, 1] for i in range(599)] + [[0, 599, 1000]]'
hops_cases = [
    ('', f'cheapest_within(4, {BASE4}, 0, 3, 3)'),
    ('', f'cheapest_within(4, {BASE4}, 0, 3, 2)'),
    ('', f'cheapest_within(4, {BASE4}, 0, 3, 1)'),
    ('', f'cheapest_within(4, {BASE4}, 0, 3, 0)'),
    ('', f'cheapest_within(4, {BASE4}, 2, 2, 0)'),
    ('', f'cheapest_within(4, {TRAP}, 0, 3, 2)'),
    ('', f'cheapest_within(4, {TRAP}, 0, 3, 3)'),
    ('', 'cheapest_within(5, [[0, 1, 4], [1, 0, 1], [3, 4, 2]], 0, 4, 10)'),
    ('', 'cheapest_within(3, [[0, 1, 2], [1, 0, 2], [1, 2, 7]], 0, 2, 10 ** 9)'),
    (RAND, 'cheapest_within(3000, routes, 0, 2999, 6)'),
    (RAND, 'cheapest_within(3000, routes, 0, 2999, 10 ** 9)'),
    (CHAIN, 'cheapest_within(600, routes, 0, 599, 599)'),
    (CHAIN, 'cheapest_within(600, routes, 0, 599, 598)'),
]
hns = {}
exec(HOPS_SOL, hns)
hops_tests = []
for setup, call in hops_cases:
    ns = dict(hns)
    if setup:
        exec(setup, ns)
    t = {'call': call, 'expect': repr(eval(call, ns)), 'compare': 'equal'}
    if setup:
        t = {'setup': setup, **t}
    hops_tests.append(t)
assert [t['expect'] for t in hops_tests[:9]] == ['300', '350', '500', '-1', '0', '6', '3', '-1', '9'], [t['expect'] for t in hops_tests]
assert hops_tests[11]['expect'] == '599' and hops_tests[12]['expect'] == '1000'
A1 = item('a1-cheapest-within-hops', 4, ['gd-paths', 'ci-timed'], ['hop-limited-path'], 1500, 'The cheapest route in k transfers',
          prose='Cash moves between accounts numbered 0 to `n - 1`. Each entry of `routes` is a one-way transfer `[a, b, fee]`, with a whole-number fee in pence. '
          'Fees are at least 1.',
          question='Write `cheapest_within(n, routes, src, dst, k)`. It returns the smallest total fee from `src` to `dst` in at most `k` transfers, else -1. '
          '`n` reaches 3,000 and `routes` 30,000, and `k` may be far larger than `n`.',
          widget={'kind': 'code', 'language': 'python', 'starter': HOPS_START, 'solution': HOPS_SOL,
           'examples': [hops_tests[0], hops_tests[5]], 'tests': hops_tests,
           'how': f'Submit runs {len(hops_tests)} hidden tests, compared exactly. Two use 30,000 random routes.'},
          feedback=fb('Bellman-Ford for at most $k$ rounds, each round from the last round’s costs.',
             'Keep the cheapest cost to each account in at most $j$ transfers. Build round $j + 1$ from round $j$ only.'),
          explain='Round $j$ of Bellman-Ford holds the cheapest cost in at most $j$ transfers, if it reads only round $j - 1$. '
          'Plain Dijkstra settles account 2 at cost 2 on the trap test, a route with too many transfers. '
          'Capping the rounds at $n - 1$ and stopping when nothing changes keeps a huge $k$ fast.')

# ======================================================================== paper 2: coding round two (C++ with a requirement added)
STORE1 = '''#include <iterator>
#include <map>

class PriceStore {
public:
    void insert(long long t, double px) { ticks_[t] = px; }
    double asof(long long t) const {
        auto it = ticks_.upper_bound(t);
        if (it == ticks_.begin()) return -1.0;
        return std::prev(it)->second;
    }
    int size() const { return static_cast<int>(ticks_.size()); }

private:
    std::map<long long, double> ticks_;
};
'''
STORE2 = STORE1.replace('''    int size() const { return static_cast<int>(ticks_.size()); }
''', '''    int size() const { return static_cast<int>(ticks_.size()); }
    double asof_fresh(long long t, long long max_age) const {
        auto it = ticks_.upper_bound(t);
        if (it == ticks_.begin()) return -1.0;
        --it;
        return t - it->first > max_age ? -1.0 : it->second;
    }
    void erase_before(long long t) { ticks_.erase(ticks_.begin(), ticks_.lower_bound(t)); }
''')
STORE_START1 = '''#include <iterator>
#include <map>

// One price per timestamp. Ticks may arrive out of order.
class PriceStore {
public:
    // Store a tick. A later insert at the same t replaces it.
    void insert(long long t, double px) { (void)t; (void)px; }
    // The price at the latest time at or before t, or -1.0 if none.
    double asof(long long t) const { (void)t; return -1.0; }
    // The number of stored ticks.
    int size() const { return 0; }
};
'''
STORE_START2 = STORE1.replace('''    int size() const { return static_cast<int>(ticks_.size()); }
''', '''    int size() const { return static_cast<int>(ticks_.size()); }
    // -1.0 if the latest tick at or before t is more than max_age old.
    double asof_fresh(long long t, long long max_age) const { (void)t; (void)max_age; return -1.0; }
    // Drop every tick strictly before t.
    void erase_before(long long t) { (void)t; }
''')
TWO = 'PriceStore s; s.insert(10, 101.5); s.insert(5, 100.0);'
BIG = ('PriceStore s; for (long long i = 0; i < 100000; ++i) { long long t = (i * 7919) % 100000; s.insert(t * 10, 100.0 + t % 97); } '
       'double total = 0; for (long long q = 5; q < 1000000; q += 10) total += s.asof(q);')
FRESH = 'PriceStore s; s.insert(100, 50.0); s.insert(130, 51.0);'
WINDOW = 'PriceStore s; for (long long t = 0; t < 50000; ++t) { s.insert(t, t * 0.5); if (t % 1000 == 999) s.erase_before(t - 4999); }'
store_cases1 = [(TWO, 's.asof(7)'), (TWO, 's.asof(10)'), (TWO, 's.asof(4)'), (TWO, 's.asof(1000)'),
                ('PriceStore s; s.insert(3, 1.0); s.insert(3, 2.0);', 's.asof(3) + 10 * s.size()'),
                ('PriceStore s;', 's.asof(0)'), (BIG, 'total')]
store_cases2 = [(FRESH, 's.asof_fresh(140, 15)'), (FRESH, 's.asof_fresh(150, 15)'), (FRESH, 's.asof_fresh(145, 15)'),
                (FRESH + ' s.erase_before(130);', 's.asof(129) * 1000 + s.size()'), (FRESH + ' s.erase_before(130);', 's.asof(130)'),
                (FRESH + ' s.erase_before(1000);', 's.size()'), (WINDOW, 's.size() + s.asof_fresh(49999, 0)')]


def cpp_tests(src, cases, alloc=False, ints=()):
    out = []
    for setup, call in cases:
        text = run_cpp(src, setup, call, alloc)
        v = int(text) if call in ints or alloc else float(text)
        t = {'setup': setup, 'call': call, 'expect': v}
        t.update({'compare': 'equal'} if isinstance(v, int) else {'compare': 'isclose', 'tol': {'rel': 1e-9, 'abs': 1e-9}})
        out.append(t)
    return out


store_tests1 = cpp_tests(STORE1, store_cases1)
store_tests2 = cpp_tests(STORE2, store_cases2, ints=('s.size()',))
B1 = parts_item(
    'b1-asof-store', 5, ['ci-design', 'cp-stl'], ['asof-store'], 1500, 'A price store, then fresher prices',
    'Build a small price store in C++, then extend it when the interviewer adds requirements.',
    [part('Write a C++ class `PriceStore` holding one price per timestamp. `insert(t, px)` stores a tick, and ticks may arrive out of order. '
          'A later insert at the same `t` replaces the price. `asof(t)` returns the price at the latest time at or before `t`, or -1.0. '
          '`size()` counts the stored ticks.',
          {'kind': 'code', 'language': 'cpp', 'starter': STORE_START1, 'solution': STORE1,
           'examples': [store_tests1[0], store_tests1[2]], 'tests': store_tests1,
           'how': f'Submit runs {len(store_tests1)} hidden tests. One inserts 100,000 ticks out of order and makes 100,000 queries.'},
          fb('An ordered map, and the tick before `upper_bound(t)`.',
             'Keep the ticks sorted by time, and search for the first tick after `t`.'),
          'A `std::map` keeps the ticks sorted, so each insert and each query costs $O(\\log n)$. '
          'The tick just before `upper_bound(t)` is the latest one at or before `t`. '
          'A scan of every tick per query takes about $10^{10}$ steps on the large test.'),
     part('The interviewer adds two requirements. `asof_fresh(t, max_age)` returns -1.0 when the latest tick at or before `t` is more than `max_age` older than `t`. '
          '`erase_before(t)` drops every tick strictly before `t`, so memory stays bounded.',
          {'kind': 'code', 'language': 'cpp', 'starter': STORE_START2, 'solution': STORE2,
           'examples': [store_tests2[0], store_tests2[1]], 'tests': store_tests2,
           'how': f'Submit runs {len(store_tests1) + len(store_tests2)} hidden tests: the {len(store_tests1)} from part 1 and {len(store_tests2)} new ones.'},
          fb('The same search, then an age test; `erase` from `begin()` to `lower_bound(t)`.',
             'Find the tick as `asof` does, then compare its age with `max_age`.'),
          'A tick exactly `max_age` old still counts, and one older does not. '
          '`erase(begin(), lower_bound(t))` removes exactly the ticks before `t`, keeping a tick at `t`. '
          'Each erased tick costs $O(1)$ amortised, so a sliding window stays cheap.'),
     part('Why does `asof` step back from `upper_bound(t)` rather than from `lower_bound(t)`?',
          choice(rng, [('`upper_bound` skips a tick at exactly `t`, so the step back lands on it', None),
                       ('`lower_bound` would give the same answer for every `t`',
                        'You expected no difference. Stepping back from `lower_bound` misses a tick at exactly `t`.'),
                       ('`upper_bound` is faster than `lower_bound` on a `std::map`',
                        'You picked by speed. Both are $O(\\log n)$ searches of the same tree.'),
                       ('`lower_bound` is undefined on an empty map',
                        'You expected an empty map to fail. Both return `end()` there.')]),
          fb('The first tick after `t`, then one back.', 'Ask what each search returns when a tick sits exactly at `t`.'),
          '`lower_bound(t)` is the first tick at or after `t`; `upper_bound(t)` is the first strictly after. '
          'Only the step back from `upper_bound` lands on a tick at exactly `t`.')])

# ======================================================================== paper 3: C++
ORDER = '```cpp\nstruct Order {\n    bool live;\n    double price;\n    int qty;\n    char side;\n};\n```'
K1 = parts_item(
    'k1-struct-padding', 3, ['sy-memory', 'cp-memory'], ['struct-padding'], 300, 'Bytes in an order',
    'A typical 64-bit desktop build aligns `double` to 8 bytes and `int` to 4.\n\n' + ORDER,
    [part('What is `sizeof(Order)`?',
          numeric(24, 0, w1 := [('summed', 14, 0, 'You added the member sizes, 1 + 8 + 4 + 1, and left out the padding.'),
                                ('all-eight', 32, 0, 'You gave every member 8 bytes. The `int` and `char` can share one 8-byte block.')],
                  placeholder='bytes', accept='24 bytes'),
          fb('7 bytes of padding after `live`, 3 at the end.', 'Place each member at the next offset that is a multiple of its alignment.', w1),
          '`live` sits at 0, then 7 bytes of padding put `price` at 8. `qty` is at 16 and `side` at 20, and the size rounds up to 24, a multiple of 8.'),
     part('You reorder the members to make `Order` as small as possible. What is `sizeof(Order)` now?',
          numeric(16, 0, w2 := [('no-tail', 14, 0, 'You left out the tail padding. The size must be a multiple of 8.'),
                                ('unchanged', 24, 0, 'You kept the old size. Putting the `double` first removes the 7-byte gap.')],
                  placeholder='bytes', accept='16 bytes'),
          fb('Largest first: 8 + 4 + 1 + 1, rounded up to 16.', 'Order the members from the largest alignment down.', w2),
          'With `price`, `qty`, `side`, `live` the members fill 14 bytes, rounded up to 16. '
          'Compiling all 24 orders of the four members gives 16 as the smallest.')])

TICK = ('```cpp\nstruct Tick {\n    Tick() {}\n    Tick(const Tick&) { ++copies; }\n    Tick(Tick&&) noexcept { ++moves; }\n'
        '    static int copies, moves;\n};\nint Tick::copies = 0, Tick::moves = 0;\n\nTick make() { Tick t; return t; }\n\n'
        'int main() {\n    std::vector<Tick> v;\n    v.reserve(4);\n    Tick a;\n    v.push_back(a);\n    v.push_back(std::move(a));\n'
        '    v.push_back(make());\n    v.emplace_back();\n}\n```')
K2 = item('k2-copies-counted', 4, ['cp-classes', 'cp-stl'], ['copy-or-move'], 240, 'Copies or moves',
          'How many times does the copy constructor of `Tick` run in this program?',
          choice(rng, [('1', None),
                       ('2', 'You counted the return from `make` as a copy. It is elided, or else moved.'),
                       ('3', 'You counted every `push_back` as a copy, the moved ones included.'),
                       ('4', 'You counted all four insertions. `emplace_back` builds in place.')]),
          fb('Only `push_back(a)` copies, since `a` is a named object.', 'Go line by line, and ask whether each argument is a named object or a temporary.'),
          'Only `push_back(a)` copies, so the count is 1. '
          '`std::move(a)` and the temporary from `make` bind to the move overload, and `emplace_back` builds in place. '
          'The `reserve(4)` means no reallocation moves elements.',
          prose=TICK)

SERIES = ('```cpp\nclass Series {\npublic:\n    explicit Series(int n) : data_(new double[n]()), n_(n) {}\n'
          '    ~Series() { delete[] data_; }\nprivate:\n    double* data_;\n    int n_;\n};\n\nvoid report() {\n    Series a(100);\n    Series b = a;\n}\n```')
K3 = item('k3-shallow-copy', 3, ['cp-memory', 'cp-classes'], ['shallow-copy'], 200, 'One block, two owners',
          'What goes wrong when `report` returns?',
          choice(rng, [('Both destructors delete the same block, a double delete', None),
                       ('Nothing, because the copy gets its own block of 100 doubles', 'You assumed the default copy is deep. It copies the pointer only.'),
                       ('It does not compile, since a class with a destructor cannot be copied', 'You expected the compiler to refuse. It still writes a copy constructor.'),
                       ('The block leaks, because neither destructor runs', 'You thought the destructors are skipped. Both run at the end of the scope.')]),
          fb('The rule of three: a destructor that frees means you need a copy too.', 'Ask what the compiler-written copy constructor copies.'),
          'The default copy constructor copies `data_`, so `a` and `b` share one block. '
          'Both destructors run `delete[]` on it, which is undefined behaviour. '
          'Write a deep copy, or delete copying and keep a move.',
          prose=SERIES)

PRICER = ('```cpp\n#include <iostream>\n#include <string>\n\nstruct Pricer {\n    Pricer() { std::cout << name() << " "; }\n'
          '    virtual ~Pricer() { std::cout << name() << " "; }\n    virtual std::string name() const { return "base"; }\n};\n'
          'struct Tree : Pricer {\n    Tree() { std::cout << name() << " "; }\n    ~Tree() override { std::cout << name() << " "; }\n'
          '    std::string name() const override { return "tree"; }\n};\n\nint main() { Tree t; }\n```')
K4 = item('k4-virtual-in-constructor', 4, ['cp-classes'], ['dispatch-during-construction'], 240, 'What it prints',
          'What does this program print?',
          choice(rng, [('`base tree tree base`', None),
                       ('`tree tree tree tree`', 'You expected the override to run inside the base constructor and destructor.'),
                       ('`base tree base tree`', 'You ran the destructors in the order of construction, not the reverse.'),
                       ('`tree tree`', 'You thought only the derived constructor and destructor print.')]),
          fb('Inside a base constructor or destructor, the object is still a base.', 'Ask what the dynamic type is while each constructor and destructor runs.'),
          'While `Pricer`’s constructor runs, the `Tree` part does not exist yet, so `name()` calls the base version. '
          'Destruction runs in reverse: `~Tree` sees a `Tree`, then `~Pricer` sees a base again.',
          prose=PRICER)

LARGER = '```cpp\ntemplate <typename T>\nT clamp_to(T x, T lo, T hi) { return x < lo ? lo : (hi < x ? hi : x); }\n```'
K5 = item('k5-template-deduction', 3, ['cp-classes'], ['template-deduction'], 180, 'One T, mixed types',
          'Which call does not compile?',
          choice(rng, [('`clamp_to(101.5, 0, 100)`', None),
                       ('`clamp_to<double>(101.5, 0, 100)`', 'You expected the explicit type to fail. Naming `T` lets 0 and 100 convert to `double`.'),
                       ('`clamp_to(101.5, 0.0, 100.0)`', 'You expected three doubles to fail. Each one deduces `T` as `double`.'),
                       ('`clamp_to(std::string("m"), std::string("a"), std::string("z"))`', 'You expected strings to fail. They have `<`, so `T` is `std::string`.')]),
          fb('Deduction gives `T = double` from 101.5 and `T = int` from 0, a conflict.', 'Deduce `T` from each argument separately and compare.'),
          'Each argument deduces `T` on its own, and deduction never converts. '
          'From 101.5 it gets `double` and from 0 it gets `int`, so the call fails. '
          'Naming `T` explicitly turns off deduction and lets the whole numbers convert.',
          prose=LARGER)

POOL_SOL = '''#include <vector>

class SlotPool {
public:
    explicit SlotPool(int capacity) : free_(capacity), used_(capacity, false), top_(capacity) {
        for (int i = 0; i < capacity; ++i) free_[i] = capacity - 1 - i;
    }
    int acquire() {
        if (top_ == 0) return -1;
        const int s = free_[--top_];
        used_[s] = true;
        ++count_;
        return s;
    }
    void release(int slot) {
        if (slot < 0 || slot >= static_cast<int>(used_.size()) || !used_[slot]) return;
        used_[slot] = false;
        free_[top_++] = slot;
        --count_;
    }
    int in_use() const { return count_; }

private:
    std::vector<int> free_;
    std::vector<bool> used_;
    int top_ = 0;
    int count_ = 0;
};
'''
POOL_START = '''#include <vector>

// A fixed pool of slots 0 to capacity - 1, handed out by index.
// No call after the constructor may allocate.
class SlotPool {
public:
    explicit SlotPool(int capacity) { (void)capacity; }
    // A free slot, or -1 when every slot is in use.
    int acquire() { return -1; }
    // Free a slot. A free or out-of-range slot is ignored.
    void release(int slot) { (void)slot; }
    // The number of slots in use.
    int in_use() const { return 0; }
};
'''
pool_cases = [
    ('SlotPool p(3); int a = p.acquire(); int b = p.acquire(); int c = p.acquire();', 'a * 100 + b * 10 + c'),
    ('SlotPool p(2); p.acquire(); p.acquire();', 'p.acquire()'),
    ('SlotPool p(4); for (int i = 0; i < 4; ++i) p.acquire(); p.release(2); p.release(0);', 'p.acquire()'),
    ('SlotPool p(4); for (int i = 0; i < 4; ++i) p.acquire(); p.release(2); p.release(0); int x = p.acquire(); int y = p.acquire();', 'x * 10 + y'),
    ('SlotPool p(5); p.acquire(); p.acquire(); p.release(1); int x = p.acquire(); int y = p.acquire();', 'x * 10 + y'),
    ('SlotPool p(3); int a = p.acquire(); p.release(a); p.release(a); p.release(7); p.release(-1);', 'p.in_use()'),
    ('SlotPool p(3); int a = p.acquire(); p.release(a); p.release(a); int x = p.acquire(); int y = p.acquire();', 'x * 10 + y'),
    ('SlotPool p(10); for (int i = 0; i < 7; ++i) p.acquire(); p.release(3); p.release(5);', 'p.in_use()'),
    ('SlotPool p(0);', 'p.acquire()'),
    ('SlotPool p(1000); reset_alloc_count(); for (int r = 0; r < 100000; ++r) { int s = p.acquire(); int t = p.acquire(); p.release(s); p.release(t); }', 'alloc_count()'),
    ('SlotPool p(100000); long long sum = 0; for (int i = 0; i < 100000; ++i) sum += p.acquire(); '
     'for (int i = 0; i < 100000; i += 2) p.release(i); for (int i = 0; i < 50000; ++i) sum += p.acquire();', 'sum'),
]
pool_tests = cpp_tests(POOL_SOL, pool_cases, alloc=True)
assert [t['expect'] for t in pool_tests] == [12, -1, 0, 2, 12, 0, 1, 5, -1, 0, 7499900000], [t['expect'] for t in pool_tests]
K6 = item('k6-slot-pool', 4, ['cp-memory', 'sy-latency'], ['slot-pool'], 1200, 'A pool that never allocates',
          prose='A gateway keeps open orders in a fixed table and hands out rows by index. The hot path may not touch the heap.',
          question='Write `SlotPool` in C++. `acquire()` returns the slot released most recently, else the lowest slot never used, else -1. '
          '`release(slot)` frees a slot, ignoring a free or out-of-range one. `in_use()` counts slots in use. Nothing after the constructor may allocate.',
          widget={'kind': 'code', 'language': 'cpp', 'allocCheck': True, 'starter': POOL_START, 'solution': POOL_SOL,
           'examples': [pool_tests[0], pool_tests[3]], 'tests': pool_tests,
           'how': f'Submit runs {len(pool_tests)} hidden tests. One counts calls of `operator new` after its setup and expects 0.'},
          feedback=fb('A stack of free slots, filled in the constructor, with a flag per slot.',
             'Preallocate a stack of free slot numbers, lowest on top. Push each released slot back on top.'),
          explain='Filling the stack with the highest slot at the bottom makes the never-used slots come out lowest first. '
          'A released slot goes on top, so it comes out next. '
          'The flag per slot stops a double release from handing one slot to two orders.')

# ======================================================================== paper 4: concurrency and systems
HITS = ('```cpp\nint hits = 0;\n\nvoid work() {\n    for (int i = 0; i < 1000000; ++i) ++hits;\n}\n'
        '// two threads run work() at the same time, then both are joined\n```')
Y1 = item('y1-lost-updates', 3, ['sy-concurrency'], ['lost-updates'], 200, 'A counter two threads share',
          'Which change makes `hits` end at exactly 2,000,000?',
          choice(rng, [('Declare it as `std::atomic<int> hits{0};`', None),
                       ('Declare it as `volatile int hits = 0;`', 'You used `volatile`. It stops some optimisations but does not make `++` atomic.'),
                       ('Sleep for a microsecond inside the loop', 'You slowed the threads down. The race is still there, only rarer.'),
                       ('Make `hits` a `static` local inside `work`', 'You moved the variable. Both threads still share one plain `int`.')]),
          fb('An atomic `++` cannot interleave with another.', 'Ask whether `++hits` is one step or three: load, add, store.'),
          '`++hits` on a plain `int` is a load, an add and a store, so two threads can lose updates. '
          'A `std::atomic<int>` makes each increment one indivisible step, so the total is 2,000,000.',
          prose=HITS)

FLAG = ('```cpp\nint data = 0;\nstd::atomic<bool> ready{false};\n\nvoid producer() {\n    data = 42;\n'
        '    ready.store(true, std::memory_order_release);\n}\n\nvoid consumer() {\n'
        '    while (!ready.load(std::memory_order_relaxed)) {}\n    use(data);\n}\n```')
Y2 = item('y2-relaxed-flag', 4, ['sy-concurrency'], ['release-acquire'], 240, 'A flag without acquire',
          'The consumer’s load uses `memory_order_relaxed`. What can go wrong?',
          choice(rng, [('The consumer can see `ready` true and still read the old `data`', None),
                       ('Nothing, since any atomic flag orders the writes around it', 'You expected every atomic to order other memory. Only release paired with acquire does.'),
                       ('The loop may spin forever, as a relaxed load never sees the store', 'You expected the store to stay hidden. A relaxed load still sees it in time.'),
                       ('It does not compile, since release and relaxed cannot be mixed', 'You expected a compile error. Orders may be mixed; only the guarantee changes.')]),
          fb('A release store is matched only by an acquire load.', 'Ask which load would make the write to `data` visible.'),
          'A release store publishes earlier writes only to a thread that reads the flag with acquire. '
          'With a relaxed load the read of `data` is not ordered after it, so it is a data race. '
          'Use `memory_order_acquire` in the loop.',
          prose=FLAG)

MOVE = ('```cpp\nvoid move_cash(Book& src, Book& dst, long pence) {\n    std::lock_guard<std::mutex> g1(src.m);\n'
        '    std::lock_guard<std::mutex> g2(dst.m);\n    src.cash -= pence;\n    dst.cash += pence;\n}\n'
        '// thread 1: move_cash(alpha, beta, 100);\n// thread 2: move_cash(beta, alpha, 50);\n```')
Y3 = item('y3-lock-order', 3, ['sy-concurrency'], ['lock-ordering'], 200, 'Two books, two locks',
          'Now and then both threads stop for good. Which fix is sound?',
          choice(rng, [('Take both with one `std::scoped_lock lk(src.m, dst.m);`', None),
                       ('Make both mutexes `std::recursive_mutex`', 'You let a thread relock its own mutex. Here each thread waits for the other one’s.'),
                       ('Add a short sleep between the two locks', 'You changed the timing. The opposite orders can still meet.'),
                       ('Unlock in the reverse of the order you locked', 'You changed the release order. The hang happens while locking.')]),
          fb('Take both locks at once, or always in one global order.', 'Ask what each thread holds and what it waits for.'),
          'Thread 1 holds `alpha` and waits for `beta`, while thread 2 holds `beta` and waits for `alpha`. '
          '`std::scoped_lock` takes both with a deadlock-avoiding algorithm. '
          'A fixed order, such as by address, also works.',
          prose=MOVE)

Y4 = item('y4-column-sum', 4, ['sy-memory'], ['cache-line-stride'], 240, 'Down the columns',
          prose='A 4,096 by 4,096 matrix of `double` is stored row by row. Cache lines are 64 bytes. '
          'The cache holds far fewer lines than one column touches.',
          question='You sum it column by column instead of row by row. About how many times as many cache lines are loaded?',
          widget=numeric(8, 0, w3 := [('bytes', 64, 0, 'You used the bytes in a line. A line holds 8 doubles, so row order loads one line per 8.'),
                               ('row-length', 4096, 0, 'You used the length of a row. Each element costs at most one line.')],
                  placeholder='a whole number', accept='8 times'),
          feedback=fb('Row order uses all 8 doubles of a line; column order uses one.', 'Count the lines loaded per element in each order.'),
          explain='Row by row, one 64-byte line serves 8 neighbouring doubles. '
          'Column by column, each access lands on a new line, which is evicted before its neighbours are read. '
          'So about 8 times as many lines are loaded, and a small cache simulation agrees.')

Y5 = parts_item(
    'y5-littles-law', 4, ['sy-latency'], ['queue-sizing'], 300, 'How many inside',
    'Orders reach a gateway at 150,000 a second. Each spends 40 µs inside it on average.',
    [part('On average, how many orders are inside the gateway at once?',
          numeric(6, 0.01, w4 := [('ms', 6000, 0.5, 'You read 40 µs as 40 ms.'),
                                  ('divided', 3750, 0.5, 'You divided the rate by 40 instead of multiplying by 40 µs.')],
                  placeholder='orders', accept='6 orders'),
          fb('Little’s law: $L = \\lambda W = 150{,}000 \\times 0.00004$.', 'Multiply the arrival rate by the time each order stays.', w4),
          'Little’s law gives $L = \\lambda W = 150{,}000 \\times 40 \\times 10^{-6} = 6$. '
          'A replay of arrivals every $1/150{,}000$ s, each staying 40 µs, has exactly 6 inside at any moment.'),
     part('A ring buffer in front of the gateway should hold four times that average. It needs a power-of-two size for a fast index mask. What size do you choose?',
          numeric(32, 0, w5 := [('not-power', 24, 0, 'You stopped at 24, which is not a power of two.'),
                                ('rounded-down', 16, 0, 'You rounded down, so the buffer holds less than four times the average.')],
                  placeholder='slots', accept='32 slots'),
          fb('$4 \\times 6 = 24$, rounded up to 32.', 'Find four times the average, then the next power of two.', w5),
          'Four times 6 is 24, and the next power of two is 32. '
          'Then the index is `i & 31` rather than a division.')])

# ======================================================================== paper 5: design
G1 = longform(
    'g1-risk-gateway', 5, ['sy-latency', 'sy-concurrency', 'ci-design'], ['risk-gateway-design'], 1800, 'Design a pre-trade risk check',
    'Say it out loud before you type. Keep the written version to 350 words.\n\n'
    'Design the pre-trade risk check between a firm’s strategies and one exchange. '
    'It checks every order against position, order-rate and price-band limits. '
    'Peak load is 200,000 orders a second. The check may add at most 5 µs at the 99th percentile. '
    'Say how you would build it, then how you would test it.',
    '*An example answer. Your own words are the real answer.*\n\n'
    'First the budget. At 200,000 orders a second, one arrives every 5 µs. '
    'So the check should take about 1 µs, or a queue builds and the tail grows.\n\n'
    'The hot path is one thread pinned to a core. It reads orders from a lock-free queue, with no locks and no allocation. '
    'All state is preallocated: flat arrays indexed by a symbol id, sized at start-up.\n\n'
    'Three checks run in order. Position: the current position plus open orders plus this order, against the limit. '
    'Rate: a token bucket per strategy. Price band: the price within a set distance of a reference price.\n\n'
    'Limits change rarely. A control thread builds a new limits table and swaps a pointer to it atomically. '
    'The hot path never waits for it.\n\n'
    'If the gateway cannot check an order, it rejects it. A kill switch blocks everything at once.\n\n'
    'To test it, I replay a recorded day and compare every decision with a slow reference checker. '
    'I add edge cases, such as a fill that crosses a limit. '
    'I measure latency from each order’s arrival, as a histogram, so a stall is not hidden. '
    'The build fails if the 99th percentile passes 5 µs.',
    [(1, 'Turns the load into a budget: one order every 5 µs'),
     (2, 'One pinned thread on the hot path, fed by a lock-free queue'),
     (2, 'Preallocated flat state and no allocation on the hot path'),
     (2, 'States the three checks correctly, with open orders in the position check'),
     (1, 'Updates limits without blocking the hot path'),
     (1, 'Fails closed, with a kill switch'),
     (1, 'Tests by replay against a reference, with a latency gate from arrival times')])
G2 = longform(
    'g2-tail-regression', 4, ['sy-latency', 'sy-os'], ['tail-latency-regression'], 900, 'The tail got worse',
    'Say it out loud before you type. Keep the written version to 250 words.\n\n'
    'After a release, a feed handler’s 99th percentile latency rose from 8 µs to 30 µs. '
    'Its median did not move. Talk through how you find the cause.',
    '*An example answer. Your own words are the real answer.*\n\n'
    'A flat median with a worse tail means most messages are fine. Something rare is slow.\n\n'
    'Rare slow events are usually a heap allocation, a page fault, a lock or a log write. A code path for rare messages is another.\n\n'
    'I would reproduce it first. I replay a recorded feed into the old and new builds, on the same machine. '
    'I check how latency is measured, so a stall is not hidden by measuring only from when work starts.\n\n'
    'Then I bisect the release diff with that replay until one change moves the 99th percentile.\n\n'
    'Inside the slow messages I time each stage. I count page faults and context switches, and use `perf` for cache misses.\n\n'
    'Once it is fixed, the replay joins the build with a 99th percentile limit. Then it cannot return quietly.',
    [(2, 'Reads a flat median and a worse tail as a rare slow event'),
     (2, 'Names at least three plausible causes, such as allocation, page faults, locks or logging'),
     (2, 'Reproduces with a recorded feed on both builds, on the same machine'),
     (1, 'Bisects the release diff'),
     (2, 'Times each stage and counts faults, switches or cache misses for the slow messages'),
     (1, 'Adds a latency gate so it cannot return quietly')])

# ======================================================================== paper 6: fit
F1 = longform(
    'f1-why-trading-systems', 3, ['rk-behave'], ['why-trading-systems'], 450, 'Why trading systems',
    'Say it out loud before you type. Keep the written version to 200 words.\n\n'
    'What makes you want to build trading systems, rather than software somewhere else?',
    '*An example answer. Your own words are the real answer.*\n\n'
    'I like code where speed and correctness are both measured, every day.\n\n'
    'Two things draw me. In trading a microsecond or a wrong fill has a price, so the work matters at once. '
    'And the problems are concrete: queues, caches and protocols, not only features.\n\n'
    'I tested this. I wrote a feed parser for a public data set. I cut its 99th percentile from 40 to 9 µs. '
    'Finding that one allocation taught me more than the course did.\n\n'
    'The hard part is the care a live system needs. I handle it with small changes and tests that replay real data.\n\n'
    'A trading firm puts developers next to the people using the code, and I want that feedback.',
    [(1, 'Gives a one-sentence answer first'),
     (2, 'Two reasons tied to the daily work, such as measured speed and concrete problems'),
     (3, 'One piece of their own evidence with a number or an outcome'),
     (2, 'Names something hard about the work and how they handle it'),
     (1, 'Says why a trading firm rather than elsewhere'),
     (1, 'About 90 seconds, with no stock phrases')])
F2 = longform(
    'f2-review-disagreement', 3, ['rk-behave'], ['review-disagreement'], 450, 'A review that disagreed',
    'Say it out loud before you type. Keep the written version to 200 words.\n\n'
    'Tell me about a code review where you and the other person disagreed. What happened, and what did you learn?',
    '*An example answer. Your own words are the real answer.*\n\n'
    'On a team project I wrote a cache for price lookups. A reviewer said it would serve stale prices after a restart.\n\n'
    'I disagreed at first, because my tests passed. I asked for a case that failed, and he described one.\n\n'
    'We wrote that case as a test, and it failed. So he was right, and my tests had missed it.\n\n'
    'I fixed it by clearing the cache on start-up. We added the test to the suite.\n\n'
    'I learned to ask for a failing case early, rather than argue in comments. Now I do that when I review too.',
    [(1, 'Sets the scene in one or two sentences'),
     (2, 'States the disagreement and both positions fairly'),
     (2, 'Settles it with evidence, such as a test, rather than by rank'),
     (2, 'Gives the outcome honestly, even if they were wrong'),
     (2, 'Names what they do differently now'),
     (1, 'Speaks in the first person, under two minutes')])

# ======================================================================== the exam document
SCORE = {'right': 1, 'wrong': 0, 'blank': 0}
doc = {
    'id': 'mock-superday-developer',
    'name': 'Developer superday',
    'style': 'developer',
    'models': 'Reported, as of Nov 2026: developer and quant developer onsites at Hudson River Trading, Two Sigma and Jane Street. '
              'Algorithms, C++, concurrency, design and fit.',
    'description': 'This is the reported shape of a quant developer final-round day, as candidates described it by Nov 2026. '
                   'Hudson River Trading, Two Sigma and Jane Street report rounds like these. '
                   'There are six papers, each on its own clock. '
                   'Two are live coding rounds, and the second adds requirements part-way. '
                   'Then come C++, concurrency and systems, a design round and fit. '
                   'Real rounds are spoken, so talk through your code as you type. '
                   'No search engine and no notes are allowed. '
                   'Orders and lengths differ by firm and office. '
                   'Two checks at the end ask for what the app cannot see.',
    'requires': ['graphs-dp/L2', 'coding-int/L4', 'cpp/L5', 'systems/L4'],
    'skills': {'gd-paths': 'Shortest paths', 'ci-timed': 'Coding under the clock', 'ci-design': 'Design in code',
               'cp-stl': 'The standard library', 'cp-memory': 'Memory and ownership', 'cp-classes': 'Classes and templates',
               'sy-memory': 'Memory and caches', 'sy-concurrency': 'Concurrency', 'sy-latency': 'Low latency', 'sy-os': 'Operating systems',
               'rk-behave': 'Behavioural answers'},
    'parts': [
        {'kind': 'paper', 'id': 'round-one', 'name': 'Coding round one', 'minutes': 45, 'scoring': SCORE, 'pass': 1, 'items': [A1]},
        {'kind': 'paper', 'id': 'round-two', 'name': 'Coding round two', 'minutes': 45, 'scoring': SCORE, 'pass': 0.6, 'items': [B1]},
        {'kind': 'paper', 'id': 'cpp', 'name': 'C++', 'minutes': 40, 'scoring': SCORE, 'pass': 0.6, 'items': [K1, K2, K3, K4, K5, K6]},
        {'kind': 'paper', 'id': 'systems', 'name': 'Concurrency and systems', 'minutes': 25, 'scoring': SCORE, 'pass': 0.6, 'items': [Y1, Y2, Y3, Y4, Y5]},
        {'kind': 'paper', 'id': 'design', 'name': 'System design', 'minutes': 45, 'scoring': SCORE, 'pass': 0.5, 'items': [G1, G2]},
        {'kind': 'paper', 'id': 'fit', 'name': 'Fit and motivation', 'minutes': 15, 'scoring': SCORE, 'pass': 0.5, 'items': [F1, F2]},
        {'kind': 'check', 'id': 'talked-aloud', 'name': 'I talked through both coding rounds aloud as I typed',
         'detail': 'Tick this only if you spoke at every step, as a live round needs.'},
        {'kind': 'check', 'id': 'no-lookup', 'name': 'I used no search engine, notes or AI help',
         'detail': 'Tick this only if you sat all six papers without them.'},
    ],
}
assert len(doc['models']) <= 200, len(doc['models'])
write(doc, OUT)
print(f'wrote {os.path.relpath(OUT)}: {sum(len(p.get("items", [])) for p in doc["parts"])} items, {sum(p.get("minutes", 0) for p in doc["parts"])} minutes')
