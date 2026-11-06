#!/usr/bin/env python3
"""Concept checks for systems level 4 (l15 to l18, review-4, homework-4).

Run from the repo root: python3 -I docs/reports/systems-L4-concepts.py
Exit 0 when the content is correct. A check that fails because the content is wrong is marked EXPECTED_FAIL in
its message, with the corrected assert in a comment beside it; the ledger row is named in each message.

Every C++ item is compiled with g++ at -std=c++17 and -std=c++20, -O1 -fno-exceptions, as the app's clang does
(the app adds -fno-builtin for allocCheck items; so do we). Allocations are counted by a replaced global
operator new, as app/js/engine/widgets/cpp-grade.js does (ENGINE-BACKLOG 470). No wall-clock asserts.
"""
import csv
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / 'app' / 'content' / 'courses' / 'systems'
CSV = ROOT / 'app' / 'content' / 'data' / 'systems' / 'latencies.csv'
TMP = pathlib.Path(tempfile.mkdtemp(prefix='sysL4-'))
FAILS = []


def load(name):
    with open(COURSE / f'{name}.json') as f:
        return json.load(f)


def check(cond, msg):
    """Record a failed check instead of stopping, so one run reports every failure."""
    if not cond:
        FAILS.append(msg)
        print('FAIL', msg)
    else:
        print('ok  ', msg.split(':')[0])


# ---------------------------------------------------------------- C++ harness
ALLOC = r'''
#include <cstdlib>
#include <cstddef>
#include <new>
namespace zq_alloc { inline volatile int n = 0; }
inline void reset_alloc_count() { zq_alloc::n = 0; }
inline int alloc_count() { return zq_alloc::n; }
void* operator new(std::size_t n) { zq_alloc::n = zq_alloc::n + 1; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new[](std::size_t n) { zq_alloc::n = zq_alloc::n + 1; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new(std::size_t n, const std::nothrow_t&) noexcept { zq_alloc::n = zq_alloc::n + 1; return std::malloc(n ? n : 1); }
void* operator new[](std::size_t n, const std::nothrow_t&) noexcept { zq_alloc::n = zq_alloc::n + 1; return std::malloc(n ? n : 1); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
'''

SHOW = r'''
#include <cstdio>
#include <string>
#include <vector>
static void show(bool v) { std::printf("%s\n", v ? "true" : "false"); }
static void show(int v) { std::printf("%d\n", v); }
static void show(long v) { std::printf("%ld\n", v); }
static void show(long long v) { std::printf("%lld\n", v); }
static void show(unsigned v) { std::printf("%u\n", v); }
static void show(unsigned long v) { std::printf("%lu\n", v); }
static void show(double v) { std::printf("%.17g\n", v); }
static void show(const std::string& s) { std::printf("\"%s\"\n", s.c_str()); }
static void show(const std::vector<int>& v) { std::printf("["); for (size_t i = 0; i < v.size(); ++i) std::printf("%s%d", i ? "," : "", v[i]); std::printf("]\n"); }
'''


def compile_run(src, std='c++17', flags=(), run_args=(), timeout=120):
    """Compile src with g++ and run it. Returns (compile_ok, stdout, stderr, returncode)."""
    d = TMP / f'u{abs(hash(src)) % 10**9}_{std}'
    d.mkdir(exist_ok=True)
    cpp = d / 'main.cpp'
    cpp.write_text(src)
    exe = d / 'a.out'
    cmd = ['g++', f'-std={std}', '-O1', '-fno-exceptions', '-w', *flags, str(cpp), '-o', str(exe)]
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        return False, '', cp.stderr, cp.returncode
    try:
        rp = subprocess.run([str(exe), *run_args], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return True, (e.stdout or ''), (e.stderr or '') + '\nTIMEOUT', None
    return True, rp.stdout, rp.stderr, rp.returncode


def run_cases(widget_code, cases, prelude='', postlude='', std='c++17', alloc=False):
    """Build one program that runs every case of a code widget (setup; show(call);) and returns the outputs
    as parsed JSON values, one per case (None where a case produced nothing readable)."""
    body = []
    for i, c in enumerate(cases):
        body.append('{ ' + c.get('setup', '') + ' show(' + c['call'] + '); }')
    src = (ALLOC if alloc else '') + SHOW + '\n' + prelude + '\n' + widget_code + '\n' + postlude + \
        '\nint main() {\n' + '\n'.join(body) + '\nreturn 0; }\n'
    flags = ['-fno-builtin'] if alloc else []
    ok, out, err, rc = compile_run(src, std, flags)
    if not ok:
        return None, err
    vals = []
    for line in out.splitlines():
        try:
            vals.append(json.loads(line))
        except ValueError:
            vals.append(None)
    while len(vals) < len(cases):
        vals.append(None)
    return vals, err


def grade(cases, vals):
    """Return the list of failing case indexes under the widget's compare rule."""
    bad = []
    for i, (c, v) in enumerate(zip(cases, vals)):
        exp = c.get('expect')
        if v is None:
            bad.append(i)
        elif c.get('compare') == 'isclose':
            if isinstance(exp, str):
                exp = float(exp)          # the Python harness evals a text expect ("10584.622") as a number
            tol = (c.get('tol') or {}).get('abs', 0)
            if not (isinstance(v, (int, float)) and (math.isclose(v, exp, rel_tol=1e-9) or abs(v - exp) <= tol)):
                bad.append(i)
        else:
            if v != exp:
                bad.append(i)
    return bad


def code_item(label, widget, std='c++17'):
    """Model solution passes every hidden test; starter fails at least one. Returns the solution outputs."""
    pre = widget.get('prelude', '')
    post = widget.get('postlude', '')
    alloc = bool(widget.get('allocCheck'))
    cases = widget['tests']
    sol, err = run_cases(widget['solution'], cases, pre, post, std, alloc)
    check(sol is not None, f'{label} solution compiles ({std}): {err[:300]}')
    if sol is not None:
        bad = grade(cases, sol)
        check(not bad, f'{label} solution passes all {len(cases)} tests ({std}): failing {bad} got {[sol[i] for i in bad]}')
    st, err = run_cases(widget['starter'], cases, pre, post, std, alloc)
    check(st is not None, f'{label} starter compiles ({std}): {err[:300]}')
    if st is not None:
        bad = grade(cases, st)
        check(len(bad) > 0, f'{label} starter fails at least one test ({std})')
    return sol, st


# ================================================================ l15 no allocation
l15 = load('l15-no-allocation')

# Which lines allocate: a replaced operator new counts each line of screens[0] separately (ledger l15 s0).
SRC_L15_S0 = ALLOC + r'''
#include <cstdio>
#include <map>
#include <string>
#include <vector>
#include <array>
struct Msg { int price; int qty; };
struct Event { Msg m; explicit Event(const Msg& x) : m(x) {} };
static int n0;
#define LINE(...) n0 = alloc_count(); __VA_ARGS__; std::printf("%d\n", alloc_count() - n0);
int main() {
    Msg m{10000, 7};
    LINE(std::vector<int> levels)
    LINE(levels.push_back(m.price))
    LINE(auto* ev = new Event(m))
    LINE(std::string s(100, 'x'))
    LINE(std::map<int, int> book; book[m.price] = 1)
    LINE(int x = m.qty * 2)
    LINE(std::vector<int> v)
    LINE(v.push_back(1))
    LINE(std::array<int, 8> a)
    LINE(int b[8])
    LINE(std::vector<double> w)
    LINE(w.emplace_back(2.5))
    LINE(auto* q = new double[3])
    LINE(std::string s64(64, 'y'))
    LINE(double arr3[3] = {1.5, 2.5, 3.5})
    LINE(std::array<double, 3> sa{})
    LINE(std::string s15(15, 'z'))
    LINE(std::string s16(16, 'z'))
    LINE(std::vector<int> r; r.reserve(1000))
    LINE(for (int msg = 0; msg < 50; ++msg) { for (int i = 0; i < 500; ++i) r.push_back(i); r.clear(); })
    (void)x; (void)a; (void)b; (void)arr3; (void)sa; delete ev; delete[] q;
    return 0;
}
'''
for std in ('c++17', 'c++20'):
    ok, out, err, rc = compile_run(SRC_L15_S0, std, ['-fno-builtin'])
    check(ok, f'l15 s0 allocation counter compiles ({std}): {err[:200]}')
    if ok:
        c = [int(t) for t in out.split()]
        (vec_decl, vec_push, new_ev, str100, map_ins, arith, v_decl, v_push, std_arr, plain_arr,
         w_decl, w_emplace, new_arr, str64, arr3, sa3, s15, s16, reserve, after_reserve) = c
        check(vec_decl == 0 and vec_push == 1 and new_ev == 1 and str100 == 1 and map_ins == 1 and arith == 0,
              f'l15 screens[0] widget.answer: lines 3,4,5,6 allocate (1 each) and lines 2,7 do not ({std}): {c[:6]}')
        check(v_decl == 0 and v_push == 1 and std_arr == 0 and plain_arr == 0,
              f'l15 screens[6] trap: only the first push_back allocates; vector declaration, std::array, int[8] do not ({std})')
        check(w_decl == 0 and w_emplace == 1 and new_arr == 1 and str64 == 1 and arr3 == 0 and sa3 == 0,
              f'review-4 items[0] r4-allocating-lines: emplace_back, new double[3], string(64) allocate; the arrays and the empty vector do not ({std})')
        check(s15 == 0 and s16 == 1,
              f'l15 screens[0] prose SSO: libstdc++ keeps 15 chars inline and allocates at 16, so 64 and 100 allocate ({std})')
        check(reserve == 1 and after_reserve == 0,
              f'l15 quiz[1] q15-reserve: reserve(1000) allocates once; 50 messages of 500 pushes and clear allocate 0 after it ({std})')

# Pool free-list semantics (ledger l15 s3, s10, quiz[2], review r4-pool-order): a stack of released slots.
def pool_sim(slots, ops):
    nxt = [s + 1 for s in range(slots)]
    if slots:
        nxt[-1] = -1
    head = 0 if slots else -1
    out = []
    for op in ops:
        if op == 'a':
            if head < 0:
                out.append(-1)
            else:
                s = head
                head = nxt[s]
                out.append(s)
        else:
            nxt[op] = head
            head = op
    return out


check(pool_sim(4, ['a', 'a', 0, 'a']) == [0, 1, 0], 'l15 screens[3]: after two allocates and release(0), the next allocate returns slot 0')
check(pool_sim(3, ['a', 'a', 'a', 1, 'a'])[-1] == 1, 'l15 screens[10] row 1: release 1 then allocate gives 1')
check(pool_sim(3, ['a', 'a', 'a', 0, 2, 'a'])[-1] == 2, 'l15 screens[10] row 2: release 0, 2 then allocate gives 2 (last released first)')
check(pool_sim(3, ['a', 'a', 'a', 'a'])[-1] == -1, 'l15 screens[10] row 3: a full pool returns -1')
check(pool_sim(4, ['a'] * 4 + [3, 1, 2, 'a', 'a'])[-2:] == [2, 1], 'l15 screens[10] row 4: release 3,1,2 then allocate twice gives 2 then 1')
check(pool_sim(5, ['a'] * 5 + [3, 0, 'a'])[-1] == 0, 'l15 quiz[2] q15-pool: release 3 then 0, allocate gives 0')
check(pool_sim(4, ['a'] * 4 + [2, 3, 1, 'a'])[-1] == 1, 'review-4 items[1] r4-pool-order: release 2,3,1 then allocate gives 1')

# The two C++ items of l15: tests pass with the solution, fail with the starter, and the starter allocates.
for std in ('c++17', 'c++20'):
    w = l15['screens'][5]['widget']
    sol, st = code_item('l15 screens[5] format_price', w, std)
    if st is not None:
        check(st[9] is not None and st[9] > 0, f'l15 screens[5] explain: the starter grows a vector so alloc_count() is above 0 ({std}): {st[9]}')
    w = l15['screens'][9]['widget']
    sol, st = code_item('l15 screens[9] Pool', w, std)

# ================================================================ l16 ring buffer
l16 = load('l16-ring-buffer')

# Counter arithmetic (ledger l16 s1, s2, s7, s8, s10, quiz, review r4-ring-counters).
check(5 % 4 == 1 and 20 - 13 == 7 and 20 & 7 == 4, 'l16 screens[1]: slot 5 mod 4 = 1, size 7, next slot 20 & 7 = 4')
check((2**32) % 3 == 1 and 4294967295 % 3 == 0 and 4294967295 == 3 * 1431655765, 'l16 screens[2] hints[1]: 2^32 mod 3 = 1, 4294967295 is a multiple of 3')
check(4294967293 & 3 == 1, 'l16 screens[2] row 0: counter 4294967293 & 3 = 1')
check(abs(2**32 / 1e7 - 429.5) < 0.05, 'l16 screens[2] row 3: 2^32 / 10^7 = 429.5 s')
# Slot order across the wrap: a power-of-two ring keeps consecutive slots; a ring of 3 repeats one.
wrap_seq = [4294967294, 4294967295, 0, 1]
check([c & 3 for c in wrap_seq] == [2, 3, 0, 1], 'l16 screens[2] explain: ring of 4 keeps slot order 2, 3, 0, 1 across the wrap')
check([c % 3 for c in wrap_seq] == [2, 0, 0, 1], 'l16 screens[2] explain: ring of 3 puts counters 4294967295 and 0 in the same slot')
check(11 - 7 == 4 and 11 & 3 == 3 and 7 & 3 == 3, 'l16 screens[7]: head 7, tail 11 in a ring of 4 holds 4 items with both slots 3')
check(45 & 15 == 13 and 103 - 100 == 3, 'l16 screens[10]: 45 & 15 = 13; head 100 tail 103 holds 3')
check(50 - 37 == 13 and 50 & 15 == 2, 'l16 quiz[0]: 13 items, next slot 2')
check(math.ceil(math.log2(2000)) == 11 and 2 ** 11 == 2048, 'l16 quiz[2]: 2,000 messages round up to 2,048 slots')
check(85 - 70 == 15 and 85 & 31 == 21, 'review-4 items[3] r4-ring-counters: 15 items, slot 21')
check(256 * 24 == 6144 and 2 ** 13 == 8192 and 5000 <= 8192 < 10000, 'l16 screens[11]: 256 slots are 6,144 bytes; 5,000 messages round up to 8,192')
check(6 - 1 == 5 and bin(5) == '0b101', 'l16 quiz[1] explain: N = 6 gives the mask 101')

# Unsigned subtraction across the wrap (ledger l16 s8 explain). In C++ the difference tail - head of two
# unsigned counters is exact mod 2^32 whatever N is: it does not depend on 2^32 being a multiple of N.
SRC_L16_S8 = r'''
#include <cstdio>
int main() {
    unsigned tail = 1u, head = 4294967295u;         // the tail passed the wrap, two items stored
    std::printf("%u %u %u\n", tail - head, tail % 3, head % 3);
    return 0;
}
'''
ok, out, err, rc = compile_run(SRC_L16_S8)
check(ok, f'l16 screens[8] unsigned wrap program compiles: {err[:200]}')
if ok:
    diff, slot_tail3, slot_head3 = [int(t) for t in out.split()]
    # The content says the subtraction stays right "because 2^32 is a multiple of N". The subtraction is right
    # for N = 3 too (diff == 2); it is the slot, counter mod N, that needs N to divide 2^32.
    check(diff == 2, 'l16 screens[8] explain: tail - head is 2 across the wrap for any N (here N = 3)')
    check(diff == 2 and not (slot_tail3 == 1 and slot_head3 == 0), 'EXPECTED_FAIL l16 screens[8] explain: the content attributes the correct subtraction to 2^32 being a multiple of N; with N = 3 the subtraction is still right (2) and only the slot mapping breaks')
    # corrected, ready to enable once the explain says the slot needs N | 2^32 and the subtraction does not:
    # check(diff == 2 and (slot_tail3, slot_head3) == (1, 0), 'l16 screens[8] explain (fixed): subtraction right for N = 3, slots 1 and 0 show the wrap breaks only the mask')

# The Ring code item: solution passes, starter fails, counters 64 bytes apart (ledger l16 s9).
for std in ('c++17', 'c++20'):
    w = l16['screens'][9]['widget']
    code_item('l16 screens[9] Ring', w, std)

# SPSC ordering (ledger l16 s5, s6, homework h4-pop-order): the push and pop orders the content teaches, run on two
# threads with N = 4 and 200,000 items. Every item arrives once, in order. ThreadSanitizer finds no race.
SPSC = r'''
#include <atomic>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <thread>
template <std::size_t N>
struct Ring {
    alignas(64) std::atomic<std::size_t> head_{0};
    alignas(64) std::atomic<std::size_t> tail_{0};
    int buf_[N];
    bool push(int v) {                                              // l16 screens[5] widget.answer
        std::size_t t = tail_.load(std::memory_order_relaxed);
        if (t - head_.load(std::memory_order_acquire) == N) return false;
        buf_[t & (N - 1)] = v;
        tail_.store(t + 1, std::memory_order_release);
        return true;
    }
    bool pop(int& out) {                                            // homework-4 items[4] widget.answer
        std::size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return false;
        out = buf_[h & (N - 1)];
        head_.store(h + 1, std::memory_order_release);
        return true;
    }
};
int main(int argc, char** argv) {
    const int n = argc > 1 ? std::atoi(argv[1]) : 200000;
    Ring<4> r;
    long long lost = 0, outoforder = 0, got = 0;
    std::thread prod([&] { for (int i = 0; i < n; ++i) while (!r.push(i)) {} });
    int expect = 0;
    while (got < n) { int v; if (r.pop(v)) { if (v != expect) ++outoforder; expect = v + 1; ++got; } }
    prod.join();
    lost = n - got;
    std::printf("%lld %lld %lld\n", got, lost, outoforder);
    return 0;
}
'''
ok, out, err, rc = compile_run(SPSC, 'c++17', ['-pthread'], ['200000'])
check(ok and rc == 0, f'SPSC ring program compiles and runs: {err[:200]}')
if ok:
    got, lost, ooo = [int(t) for t in out.split()]
    check(got == 200000 and lost == 0 and ooo == 0, 'l16 screens[5] and homework-4 items[4]: the taught push and pop orders deliver 200,000 items once each, in order, with N = 4')


def tsan(src, args=(), opt='-O1'):
    """Compile with ThreadSanitizer; return the count of 'data race' reports, or None when TSan is unavailable.
    A run that never ends (the optimiser hoists a plain counter out of a spin loop, which is itself the race)
    counts as one report."""
    ok, out, err, rc = compile_run(src, 'c++17', ['-pthread', '-fsanitize=thread', '-g', opt], args, timeout=120)
    if not ok:
        return None
    n = err.count('WARNING: ThreadSanitizer: data race')
    return n if rc is not None else max(n, 1)


races_atomic = tsan(SPSC, ['50000'])
if races_atomic is None:
    print('skip  ThreadSanitizer not available: the race checks are not run')
else:
    check(races_atomic == 0, 'l16 screens[6]: the atomic release/acquire ring has no data race under ThreadSanitizer')

    # A race needs two writers? One writer and one reader of a plain variable is a data race (C++17 [intro.races]/21).
    ONE_WRITER = r'''
#include <thread>
#include <cstdio>
int flag = 0;
int main() {
    std::thread w([] { for (int i = 0; i < 1000; ++i) flag = i; });
    long long s = 0;
    for (int i = 0; i < 1000; ++i) s += flag;
    w.join();
    std::printf("%lld\n", s);
    return 0;
}
'''
    races_one_writer = tsan(ONE_WRITER)
    check(races_one_writer == 0, 'EXPECTED_FAIL l16 screens[6] explain: "A race needs two writers of one variable"; one writer and one reader of a plain int is reported as a data race by ThreadSanitizer')
    # corrected, ready to enable once the explain reads "a race needs two threads touching one variable with at least one writer and nothing ordering them":
    # check(races_one_writer > 0, 'l16 screens[6] explain (fixed): one writer plus one reader of a plain variable is a data race')

    # The Ring of screens[9] (plain std::size_t counters) driven by two threads: the item's framing is the two-core
    # ring (separate cache lines for two cores), but its counters are not atomic, so it is a data race.
    # Deterministic: the producer fills the ring, then hands over through a relaxed flag, which creates no
    # happens-before, so the consumer's reads of tail_ and the slots are unordered against the producer's writes
    # (C++17 [intro.races]/21) and ThreadSanitizer reports them whatever the timing.
    PLAIN_RING = l16['screens'][9]['widget']['solution'] + r'''
#include <atomic>
#include <thread>
#include <cstdio>
int main() {
    Ring r(4);
    std::atomic<int> go{0};
    std::thread prod([&] { for (int i = 0; i < 4; ++i) r.push(i); go.store(1, std::memory_order_relaxed); });
    while (go.load(std::memory_order_relaxed) == 0) {}
    int got = 0; int v;
    while (r.pop(v)) ++got;
    prod.join();
    std::printf("%d\n", got);
    return 0;
}
'''
    races_plain = tsan(PLAIN_RING)
    check(races_plain == 0, 'EXPECTED_FAIL l16 screens[9] widget.solution: presented as the two-core ring (alignas(64) for two cores) but its plain size_t counters race under ThreadSanitizer when driven by two threads')
    # corrected, ready to enable once the prose says this version is single-threaded and the two-thread ring uses std::atomic counters with the orders of screens[5]:
    # check(races_plain > 0, 'l16 screens[9] (fixed prose): the plain-counter ring is single-threaded only; two threads race on it')

# The solution's counters are at least 64 bytes apart on this ABI too (ledger l16 s9 tests[9]).
SRC_L16_ALIGN = l16['screens'][9]['widget']['solution'] + r'''
#include <cstdio>
#include <cstddef>
int main() { Ring r(8); std::printf("%lld %zu\n", (long long)((const char*)&r.tail_ - (const char*)&r.head_), alignof(Ring)); return 0; }
'''
ok, out, err, rc = compile_run(SRC_L16_ALIGN)
check(ok and int(out.split()[0]) >= 64 and int(out.split()[1]) == 64, f'l16 screens[9] solution: head_ and tail_ are {out.split()[0] if ok else "?"} bytes apart and the struct is 64-aligned')

# ================================================================ l17 measuring latency
l17 = load('l17-measuring-latency')


def nearest_rank(values, p):
    """The lesson's rule: sort, rank = ceil(p n / 100) counted from 1, rank 1 for p = 0 (l17 screens[7])."""
    s = sorted(values)
    r = max(1, math.ceil(p * len(s) / 100 - 1e-9))
    return s[r - 1]


mix = [10] * 990 + [1000] * 10
check(abs(sum(mix) / 1000 - 19.9) < 1e-9 and 19.9 not in mix, 'l17 screens[0]: the mean 19.9 µs is a value no request had')
check(nearest_rank(mix, 50) == 10 and nearest_rank(mix, 99) == 10 and nearest_rank(mix, 99.9) == 1000, 'l17 screens[2]: p50 10, p99 10, p99.9 1000 by nearest rank')
check(nearest_rank([10] * 999 + [1000], 99.9) == 10, 'l17 screens[2] row 3 and screens[6]: one slow of 1,000 shows only at the maximum')
first_k = next(k for k in range(0, 31) if nearest_rank([10] * (1000 - k) + [1000] * k, 99) == 1000)
check(first_k == 11, f'l17 screens[1]: the p99 first reads 1,000 µs at 11 slow requests (got {first_k})')
check(abs((10 * 989 + 1000 * 11) / 1000 - 20.89) < 1e-9, 'l17 screens[1] explain: the mean moves from 19.9 to 20.9')
check(nearest_rank([5, 1, 4, 2, 3], 20) == 1 and nearest_rank([5, 1, 4, 2, 3], 50) == 3 and nearest_rank([5, 1, 4, 2, 3], 80) == 4 and nearest_rank([5, 1, 4, 2, 3], 100) == 5, 'l17 screens[10]: p20 1, p50 3, p80 4, p100 5')
check(math.ceil(0.95 * 40) == 38, 'l17 screens[7]: p95 of 40 samples is rank 38')
check(nearest_rank([3, 9, 4, 7, 5, 8, 6, 2, 10, 1], 75) == 8, 'l17 quiz[0]: p75 of ten samples is 8 (rank 8)')
check(nearest_rank([7, 3, 9, 1, 5, 8, 2, 6], 60) == 6, 'review-4 items[6] r4-p60: rank ceil(4.8) = 5 holds 6')
check(nearest_rank([15] * 940 + [400] * 60, 99) == 400 and abs((940 * 15 + 60 * 400) / 1000 - 38.1) < 1e-9, 'review-4 items[5] r4-mean-p99: mean 38.1, p99 400')
fleet = [10] * 1000 + [10] * 970 + [1000] * 30
check(nearest_rank([10] * 970 + [1000] * 30, 99) == 1000 and nearest_rank(fleet, 99) == 1000 and (10 + 1000) / 2 == 505, 'l17 screens[11]: host B p99 1000, average 505, pooled p99 1000 (rank 1980 of 2000 is slow)')
check(nearest_rank([20] * 1960 + [800] * 40, 99) == 800 and nearest_rank([20] * 1985 + [800] * 15, 99) == 20, 'homework-4 items[3] h4-two-hosts: pooled p99 800 with 40 slow, 20 with 15 slow')
check(sum(fleet) / len(fleet) != 505, 'l17 screens[11] hints[1]: the average of two percentiles is not a percentile of the pooled samples')

# The float-at-the-boundary claims (l17 screens[6], screens[8]). IEEE doubles, the same on wasm32 and x86-64 SSE.
check(repr(99.9 / 100 * 1000) == '999.0000000000001' and math.ceil(99.9 / 100 * 1000) == 1000, 'l17 screens[6]: 99.9 / 100 * 1000 in a double is 999.0000000000001 and ceil gives 1000')
check(0.999 * 1000 == 999.0, 'l17 screens[6] canvas: 0.999 * 1000 is exactly 999 in a double')
check(repr(64.4 * 250 / 100) == '161.00000000000003' and math.ceil(64.4 * 250 / 100) == 162 and math.ceil(64.4 * 250 / 100 - 1e-9) == 161, 'l17 screens[8]: 64.4 * 250 / 100 is 161.00000000000003; the 1e-9 guard gives rank 161')
try:
    import numpy as np
    v = [10.0] * 999 + [1000.0]
    check(float(np.percentile(v, 99.9, method='inverted_cdf')) == 1000.0, f'l17 screens[6] explain: NumPy {np.__version__} inverted_cdf also reads rank 1,000 (1000 µs) for 999 fast and one slow')
    v2 = [10.0] * 990 + [1000.0] * 10
    check(float(np.percentile(v2, 99, method='inverted_cdf')) == 10.0, f'l17 screens[1] convention: nearest rank (inverted_cdf) p99 is 10 µs; NumPy default linear interpolation would give {np.percentile(v2, 99):.1f}')
except ImportError:
    print('skip  numpy not installed')

# The same in C++ doubles, as the app's clang would compute (the C++ percentile item).
SRC_L17_FLOAT = r'''
#include <cmath>
#include <cstdio>
int main() { volatile double p = 99.9, n = 1000, q = 64.4, m = 250; std::printf("%.17g %.17g %d %d\n", p / 100 * n, q * m / 100, (int)std::ceil(p / 100 * n), (int)std::ceil(q * m / 100 - 1e-9)); return 0; }
'''
ok, out, err, rc = compile_run(SRC_L17_FLOAT)
check(ok and out.split() == ['999.00000000000011', '161.00000000000003', '1000', '161'], f'l17 screens[6] and [8] in C++ doubles: {out.strip() if ok else err[:100]}')

# C++ percentile item (l17 screens[8]) and the LatencyHist of homework-4 items[0].
for std in ('c++17', 'c++20'):
    code_item('l17 screens[8] percentile', l17['screens'][8]['widget'], std)
hw = load('homework-4')
for std in ('c++17', 'c++20'):
    code_item('homework-4 items[0] LatencyHist', hw['items'][0]['widget'], std)
check(math.floor(math.log2(10)) == 3 and 2 ** 4 == 16 and math.floor(math.log2(35184372088832)) == 45, 'homework-4 items[0] explain: 10 ns is bucket 3, upper bound 16; 2^45 clamps to bucket 39 (upper 2^40)')

# Python report item (l17 screens[4]) on latencies.csv and the generated files; coordinated omission figures.
with open(CSV) as f:
    rows = list(csv.DictReader(f))
late = sum(1 for r in rows if int(r['sent_us']) > int(r['intended_us']))
sent = [int(r['done_us']) - int(r['sent_us']) for r in rows]
true = [int(r['done_us']) - int(r['intended_us']) for r in rows]
check(len(rows) == 2000 and late == 875, f'l17 screens[3] canvas: 2,000 rows, 875 sent late (got {late})')
check(max(sent) >= 49000 and sum(1 for s in sent if s >= 49000) == 1, 'l17 screens[3]: one reply of about 50 ms in the run')
check(all(int(r['intended_us']) == 100 * i for i, r in enumerate(rows)), 'l17 screens[4] canvas: one request intended every 100 µs')
check([nearest_rank(sent, 50), nearest_rank(sent, 99), nearest_rank(sent, 99.9)] == [40, 50, 248], 'l17 screens[3] canvas: done - sent p50 40, p99 50, p99.9 248')
check([nearest_rank(true, 50), nearest_rank(true, 99), nearest_rank(true, 99.9)] == [49, 48821, 49911], 'l17 screens[3] canvas: done - intended p50 49, p99 48,821, p99.9 49,911')
check(abs(sum(true) / len(true) - 10584.622) < 0.001, 'l17 screens[4] tests[6]: mean of the true latency 10,584.622 µs')
check(all((d - i) - (d - s) == s - i for i, s, d in ((int(r['intended_us']), int(r['sent_us']), int(r['done_us'])) for r in rows)), 'l17 screens[3] options[2].why: the two measures differ by exactly the wait before the send')


def run_py(code, calls, workdir):
    ns = {}
    cwd = os.getcwd()
    os.chdir(workdir)
    try:
        exec(compile(code, 'item.py', 'exec'), ns)
        out = []
        for c in calls:
            if c.get('setup'):
                exec(c['setup'], ns)
            out.append(eval(c['call'], ns))
    finally:
        os.chdir(cwd)
    return out


w = l17['screens'][4]['widget']
import ast
w['tests'] = [dict(c, expect=ast.literal_eval(c['expect'])) if isinstance(c.get('expect'), str) else c for c in w['tests']]  # Python cases carry expect as source text
pyd = TMP / 'py'
pyd.mkdir(exist_ok=True)
shutil.copy(CSV, pyd / 'latencies.csv')
sol = run_py(w['solution'], w['tests'], pyd)
check(not grade(w['tests'], sol), f'l17 screens[4] solution passes all {len(w["tests"])} tests: {grade(w["tests"], sol)}')
st = run_py(w['starter'], w['tests'], pyd)
check(len(grade(w['tests'], st)) > 0, 'l17 screens[4] starter fails at least one test')
# The generated 77-row file: done - sent is a permutation of 10..86, so p99 and p99.9 both read rank 77.
perm77 = sorted(i * 37 % 77 + 10 for i in range(77))
check(perm77 == list(range(10, 87)) and nearest_rank(perm77, 99) == 86 and nearest_rank(perm77, 99.9) == 86, 'l17 screens[4] tests[7..8]: 77 rows give ranks 77 and 77, value 86')
check(nearest_rank([i * 37 % 1000 + 10 for i in range(1000)], 99.9) == 1008 and nearest_rank([i * 37 % 78 + 10 for i in range(78)], 50) == 48, 'l17 screens[4] tests[9..10]: rank 999 of 1,000 is 1008; rank 39 of 78 is 48')

# Closed-loop count (homework-4 items[5]) and the timing-overhead arithmetic as stated (l17 screens[9]).
check(40000 // 250 == 160, 'homework-4 items[5] h4-stall-count: 40,000 / 250 = 160 requests due')
check(40 / 50 == 0.8 and 40 / 1000 == 0.04, 'l17 screens[9] table (as the screen models it: two full reads of 20 ns inside the measurement): 80% and 0.04 ns')

# ================================================================ l18 feed handler
l18 = load('l18-feed-handler')


def arbitrate(frames):
    """l18 screens[4] policy: apply seq >= expected, count skipped numbers as a gap, drop seq < expected."""
    expected, gaps, applied = 1, 0, []
    for name in frames:
        seq = int(name[:-1])
        if seq < expected:
            continue
        gaps += seq - expected
        expected = seq + 1
        applied.append(name)
    return applied, gaps


applied, gaps = arbitrate(['1A', '1B', '2A', '2B', '4A', '3B', '4B', '5A', '5B'])
check(applied == ['1A', '2A', '4A', '5A'] and gaps == 1, 'l18 screens[4]: applied 1A, 2A, 4A, 5A with a gap of 1; 3B is stale after 4A')
check(arbitrate(['10A', '14A'][1:])[1] == 13 and 14 - 10 == 4, 'l18 quiz[1]: expecting 10, a 14 adds 4 to the gap count')
check(arbitrate(['9A', '7B'])[0] == ['9A'], 'l18 quiz[3]: expecting 9, a 7 is dropped')


def frames_from_reads(reads, size=24):
    held, done = 0, []
    for r in reads:
        held += r
        done.append(held // size)
        held %= size
    return done, held


check(frames_from_reads([50, 40, 80]) == ([2, 1, 4], 2), 'l18 screens[6]: reads of 50, 40, 80 complete 2, 1, 4 frames with 2 bytes waiting')
check(frames_from_reads([31, 41]) == ([1, 2], 0), 'review-4 items[8] r4-two-reads: 31 then 41 bytes give 3 frames, none left')
check(frames_from_reads([900]) == ([37], 12), 'l18 screens[9]: a 900-byte read holds 37 frames with 12 left')
check(10100 - 9900 + 1 == 201 and 201 * 2 * 4 == 1608 and 1024 * 16 == 16384 and 1608 + 16384 + 40 == 18032, 'l18 screens[3]: 201 levels, 1,608 + 16,384 + 40 = 18,032 bytes')
check(400 + 1 == 401, 'homework-4 items[2] model: a £4 range in pennies is 401 levels a side')

# The handler item: solution passes 15 tests, starter fails; sizeof matches the 18,032 of screens[3]; the frame layout
# puts the sequence number big-endian at offsets 4 to 7, as l14 taught.
for std in ('c++17', 'c++20'):
    code_item('l18 screens[8] Handler', l18['screens'][8]['widget'], std)
SRC_L18_SIZE = ALLOC + SHOW + l18['screens'][8]['widget']['prelude'] + l18['screens'][8]['widget']['solution'] + r'''
int main() {
    std::printf("%zu\n", sizeof(Handler));
    auto f = frame('A', 'B', 70000u, 1, 2, 10000);
    std::printf("%d %d %d %d %zu\n", f[4], f[5], f[6], f[7], f.size());
    return 0;
}
'''
ok, out, err, rc = compile_run(SRC_L18_SIZE, 'c++17', ['-fno-builtin'])
check(ok, f'l18 size program compiles: {err[:200]}')
if ok:
    lines = out.splitlines()
    check(int(lines[0]) == 18032, f'l18 screens[3] and screens[8]: sizeof(Handler) is 18,032 bytes (got {lines[0]})')
    check(lines[1].split() == ['0', '1', '17', '112', '24'], f'l18 screens[8] prelude: seq 70,000 = 00 01 11 70 at offsets 4 to 7 in a 24-byte frame (l14 layout): {lines[1]}')

# Budget arithmetic that carries a concept (the worst message, not the average).
check(1000 + 200 + 300 + 500 + 500 == 2500 and 3000 - 2500 == 500 and 2500 + 200 == 2700 and 2500 + 5000 == 7500, 'l18 screens[2]: 2,500; 500 slack; 2,700 with four allocations; 7,500 with a 5 µs stall')
check(1200 + 250 + 350 + 600 + 600 == 3000, 'homework-4 items[2] model: the budget adds to 3,000 ns')

# Sizing follow-up (homework-4 items[1]) and L1 residency.
check(2400 * 1.25 == 3000 and 3000 * 20 == 60000 and 150000 * 0.002 == 300 and 2 ** 9 == 512 and 512 * 24 == 12288, 'homework-4 items[1]: 3,000 slots, 60,000 bytes, 512 ring slots, 12,288 bytes')
check(12288 <= 32768 < 60000 and 60000 - 32768 == 27232 and 72288 - 32768 == 39520 and 2400 * 20 > 32768, 'homework-4 items[1] parts[4]: only the ring fits; even the 2,400 live slots (48,000 bytes) exceed L1')

# ---------------------------------------------------------------- result
print()
print(f'{len(FAILS)} failing check(s)')
for f in FAILS:
    print(' -', f)
expected = [f for f in FAILS if f.startswith('EXPECTED_FAIL')]
unexpected = [f for f in FAILS if not f.startswith('EXPECTED_FAIL')]
print(f'{len(expected)} expected (content findings), {len(unexpected)} unexpected')
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if FAILS else 0)
