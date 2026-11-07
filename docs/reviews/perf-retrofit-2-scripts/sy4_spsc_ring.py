"""Second read of systems/homework-4.json h4-spsc-ring.

Builds one program per case (prelude with allocation counters, the code under
test, then setup and call), compiles with g++ and clang++ at -O1 -fno-exceptions
in C++17 (the engine's standard) and C++20, and compares with `expect`.
Runs: the shipped solution, the starter, a reader solution by another route,
and reader-planted bugs. Exit 0 when every expectation below holds.
Run from this folder: python3 sy4_spsc_ring.py
"""
import json, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ITEM = None
for it in json.load(open(os.path.join(ROOT, 'app/content/courses/systems/homework-4.json')))['items']:
    if it['id'] == 'h4-spsc-ring':
        ITEM = it
W = ITEM['widget']
FAILS = []

def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)

PRELUDE = r'''
#include <cstdlib>
#include <cstdio>
#include <new>
#include <vector>
#include <type_traits>
static long long g_n = 0;
void* operator new(std::size_t n) { ++g_n; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new[](std::size_t n) { ++g_n; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void* operator new(std::size_t n, const std::nothrow_t&) noexcept { ++g_n; return std::malloc(n ? n : 1); }
void* operator new[](std::size_t n, const std::nothrow_t&) noexcept { ++g_n; return std::malloc(n ? n : 1); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
int alloc_count() { return (int)g_n; }
void reset_alloc_count() { g_n = 0; }
'''

SHOW = r'''
template <class T> void show(const T& v) {
    if constexpr (std::is_same_v<T, bool>) std::printf("%s", v ? "true" : "false");
    else if constexpr (std::is_integral_v<T>) std::printf("%lld", (long long)v);
    else { std::printf("["); bool first = true; for (auto x : v) { if (!first) std::printf(","); first = false; std::printf("%lld", (long long)x); } std::printf("]"); }
}
'''

def jsval(x):
    return json.dumps(x).replace(' ', '')

def compilers():
    out = []
    for c in ('g++', 'clang++'):
        if shutil.which(c):
            out.append(c)
    return out

def build(src, cxx, std, path):
    with open(path + '.cpp', 'w') as f:
        f.write(src)
    r = subprocess.run([cxx, '-std=' + std, '-O1', '-fno-exceptions', '-w', path + '.cpp', '-o', path],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stderr

def run_all(code, cxx, std, tmp, cases):
    """Return list of (passed, got, seconds) per case."""
    res = []
    for k, t in enumerate(cases):
        p = os.path.join(tmp, 'c%d' % k)
        if 'compiles' in t:
            src = PRELUDE + code + '\nint main() { ' + t.get('setup', '') + ' ' + t['compiles'] + ' return 0; }\n'
            ok, _ = build(src, cxx, std, p)
            res.append((ok == t['expect'], 'compiles' if ok else 'no-compile', 0.0))
            continue
        src = (PRELUDE + code + SHOW + '\nint main() { ' + t.get('setup', '') +
               '\n auto __r = (' + t['call'] + ');\n show(__r); std::printf("\\n"); return 0; }\n')
        ok, err = build(src, cxx, std, p)
        if not ok:
            res.append((False, 'compile error', 0.0))
            continue
        t0 = time.time()
        r = subprocess.run([p], capture_output=True, text=True, timeout=20)
        dt = time.time() - t0
        got = r.stdout.strip()
        res.append((r.returncode == 0 and got == jsval(t['expect']), got, dt))
    return res

SOL = W['solution']
STARTER = W['starter']

# Reader solution by another route: plain C array, seq_cst atomics, padding
# arrays instead of alignas, drain written as repeated pops, size from one load each.
READER = r'''
#include <atomic>
#include <cstddef>
#include <vector>
template <std::size_t N>
class TickRing {
    static_assert(N != 0 && (N & (N - 1)) == 0, "power of two");
    long long slots_[N];
public:
    std::atomic<unsigned> head_{0};
    char pad_a_[64];
    std::atomic<unsigned> tail_{0};
    char pad_b_[64];
    bool try_push(long long v) {
        unsigned t = tail_.load();
        if (t - head_.load() >= N) return false;
        slots_[t % N] = v;
        tail_.store(t + 1u);
        return true;
    }
    bool try_pop(long long& out) {
        unsigned h = head_.load();
        if (tail_.load() == h) return false;
        out = slots_[h % N];
        head_.store(h + 1u);
        return true;
    }
    int drain(std::vector<long long>& out, int max) {
        int n = 0; long long x;
        while (n < max && try_pop(x)) { out.push_back(x); ++n; }
        return n;
    }
    int size() const { return (int)(tail_.load() - head_.load()); }
};
'''

def mutate(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new)

BUGS = {
    # drain hands the batch over newest first
    'drain newest first': mutate(SOL, 'out.push_back(buf_[(h + i) & (N - 1)]);',
                                 'out.push_back(buf_[(h + n - 1 - i) & (N - 1)]);'),
    # size from the slots, so a full ring reads 0
    'size from masked slots': mutate(SOL,
        'return static_cast<int>(tail_.load(std::memory_order_acquire) - head_.load(std::memory_order_acquire));',
        'return static_cast<int>((tail_.load() - head_.load()) & (N - 1));'),
    # drain copies the ticks but never frees them
    'drain forgets to move head': mutate(SOL, 'head_.store(h + n, std::memory_order_release);        // one release frees them all',
                                         '(void)h;'),
    # publishes the tail before writing the slot: a real two-core bug
    'tail published before the slot (relaxed)': mutate(mutate(SOL,
        '        buf_[t & (N - 1)] = v;\n        tail_.store(t + 1, std::memory_order_release);        // publish the slot',
        '        tail_.store(t + 1, std::memory_order_relaxed);\n        buf_[t & (N - 1)] = v;'),
        'unsigned t = tail_.load(std::memory_order_acquire);   // see the producer\'s writes',
        'unsigned t = tail_.load(std::memory_order_relaxed);'),
}

cases = W['tests']
examples = W['examples']
check(len(cases) == 12 and len(examples) == 2, '12 tests against 2 examples')
check(all('compiles' in t or True for t in cases), 'every test is a single-threaded call or a compile check')
check(not any('thread' in (t.get('setup', '') + t.get('call', '') + t.get('compiles', '')) for t in cases),
      'no test starts a thread')
check(not any(w in (t.get('setup', '') + t.get('call', '')) for t in cases for w in ('chrono', 'clock', 'time(')),
      'no test reads a clock, so none is timing-flaky')

tmp = tempfile.mkdtemp()
try:
    for cxx in compilers():
        for std in ('c++17', 'c++20'):
            tag = '%s %s' % (cxx, std)
            r = run_all(SOL, cxx, std, tmp, examples + cases)
            check(all(x[0] for x in r), tag + ': shipped solution passes both examples and all 12 tests')
            slow = max(x[2] for x in r)
            check(slow < 1.0, tag + ': slowest native case %.3f s' % slow)
            r = run_all(STARTER, cxx, std, tmp, cases)
            fails = [k + 1 for k, x in enumerate(r) if not x[0]]
            check(len(fails) >= 10, tag + ': starter fails tests %s' % fails)
            r = run_all(READER, cxx, std, tmp, examples + cases)
            check(all(x[0] for x in r), tag + ': reader solution passes both examples and all 12 tests')
            for name, code in BUGS.items():
                r = run_all(code, cxx, std, tmp, cases)
                fails = [k + 1 for k, x in enumerate(r) if not x[0]]
                if name.startswith('tail published'):
                    check(fails == [], tag + ': planted "%s" passes every test (SY4-1)' % name)
                else:
                    check(len(fails) > 0, tag + ': planted "%s" fails tests %s' % (name, fails))
finally:
    shutil.rmtree(tmp)

# Wrap arithmetic behind test 8 (index 7), by hand: 8 pushes from 2^32 - 5.
M = 2 ** 32
start = M - 5
check((start + 8) % M == 3, 'tail after eight pushes from 2^32 - 5 wraps to 3')
check(((start + 8) % M - start) % M == 8, 'unsigned difference is 8 across the wrap')
# The difference survives the wrap for any N; the slot mapping needs N | 2^32 (SY4-2).
for n in (3, 5, 6, 8):
    t = (start + 8) % M
    check(((t - start) % M) == 8, 'N = %d: count by unsigned difference is right across the wrap' % n)
check([(c % M) % 6 for c in (M - 1, M)] == [(M - 1) % 6, 0] and ((M - 1) % 6 + 1) % 6 != 0,
      'N = 6: slots jump at the wrap ((2^32 - 1) mod 6 = 3, then 0), so only the slot needs N | 2^32')

print('failures:', len(FAILS))
sys.exit(1 if FAILS else 0)
