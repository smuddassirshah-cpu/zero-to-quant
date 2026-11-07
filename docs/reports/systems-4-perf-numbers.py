"""systems level 4 performance task h4-spsc-ring: run the solution, the starter
and planted wrong solutions against every hidden test with a native compiler.

Route A: every test is compiled and run natively (g++, and clang++ if present),
at -std=c++20 -O1 -fno-exceptions, and its printed value is compared with the
JSON expect. Route B: the expected values of the value tests are recomputed by a
Python model of the ring (unsigned 32-bit counters), independent of the C++.
Exit 0 only if the solution passes every test on every compiler, the starter
fails 10 of the 12 (a stub trivially passes the empty pop and the heap test), every planted bug fails at least one, and the model agrees.
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'systems', 'homework-4.json')
item = next(i for i in json.load(open(HW))['items'] if i['id'] == 'h4-spsc-ring')
W = item['widget']
fails = []

def check(cond, msg):
    if not cond:
        fails.append(msg)
        print('FAIL', msg)

# ---- shape -------------------------------------------------------------
check(item.get('performance') == 'code', 'performance kind')
check(len(W['tests']) >= 3 and len(W['tests']) > len(W['examples']), 'more tests than examples')
check(len(W['tests']) <= 15, 'at most 15 tests')
for e in W['examples']:
    check(e in W['tests'], 'example also a test')
check(len(W['tests']) == 12, 'how says twelve tests')

PRE = r'''
#include <cstdio>
#include <cstdlib>
#include <new>
#include <string>
#include <type_traits>
#include <vector>
static long long g_allocs = 0;
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
long long alloc_count() { return g_allocs; }
void reset_alloc_count() { g_allocs = 0; }
'''
POST = r'''
static std::string js(bool b) { return b ? "true" : "false"; }
template <class T> static std::string js(const T& v) {
    if constexpr (std::is_integral_v<T>) return std::to_string(v);
    else { std::string s = "["; for (std::size_t i = 0; i < v.size(); ++i) { if (i) s += ", "; s += std::to_string(v[i]); } return s + "]"; }
}
'''

def jsval(x):
    if isinstance(x, bool):
        return 'true' if x else 'false'
    if isinstance(x, list):
        return '[' + ', '.join(str(int(v)) for v in x) + ']'
    return str(x)

def compilers():
    out = []
    for c in ('g++', 'clang++'):
        if shutil.which(c):
            out.append(c)
    return out

def run_variant(code, cxx):
    """Return a list of booleans, one per test, as the engine would grade them."""
    res = [False] * len(W['tests'])
    tmp = tempfile.mkdtemp()
    value_idx = [k for k, t in enumerate(W['tests']) if 'compiles' not in t]
    body = PRE + code + POST + '\nint main(int argc, char** argv) {\n int which = std::atoi(argv[1]);\n'
    for k in value_idx:
        t = W['tests'][k]
        body += ' if (which == %d) { %s auto zq_result = (%s); std::printf("%%s\\n", js(zq_result).c_str()); }\n' % (k, t['setup'], t['call'])
    body += ' return 0;\n}\n'
    src = os.path.join(tmp, 'main.cpp'); exe = os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx, '-std=c++20', '-O1', '-fno-exceptions', '-w', src, '-o', exe],
                        capture_output=True, text=True)
    ok = cp.returncode == 0
    if not ok and os.environ.get("SHOWERR"): print(cp.stderr[:2000])
    if ok:
        for k in value_idx:
            p = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
            res[k] = p.returncode == 0 and p.stdout.strip() == jsval(W['tests'][k]['expect'])
    for k, t in enumerate(W['tests']):
        if 'compiles' in t:
            s2 = os.path.join(tmp, 'c%d.cpp' % k)
            open(s2, 'w').write(PRE + code + '\nvoid zq_check() { %s %s }\nint main() { return 0; }\n'
                                % (t.get('setup', ''), t['compiles']))
            built = subprocess.run([cxx, '-std=c++20', '-O1', '-fno-exceptions', '-w', '-fsyntax-only', s2],
                                   capture_output=True).returncode == 0
            res[k] = built == t['expect']
    shutil.rmtree(tmp)
    return res

sol = W['solution']
BUGS = {
    'full one slot early (the lesson starter)': ('if (t - h == N) return false;', 'if (t - h >= N - 1) return false;'),
    'full test that breaks at the wrap': ('if (t - h == N) return false;', 'if (t >= h + N) return false;'),
    'slots on the heap': ('alignas(64) std::array<long long, N> buf_{};', 'std::vector<long long> buf_ = std::vector<long long>(N);'),
    'counters share a cache line': ('alignas(64) std::atomic<unsigned> head_{0};\n    alignas(64) std::atomic<unsigned> tail_{0};',
                                    'std::atomic<unsigned> head_{0};\n    std::atomic<unsigned> tail_{0};'),
    'drain clears out first': ('unsigned n = t - h;\n', 'unsigned n = t - h;\n        out.clear();\n'),
    'drain ignores max': ('if (n > static_cast<unsigned>(max)) n = static_cast<unsigned>(max);', ''),
    'no power-of-two check': ('static_assert(N > 0 && (N & (N - 1)) == 0, "N must be a power of two");', ''),
    'empty pop writes out': ('if (h == t) return false;                             // empty: out unchanged\n        out = buf_[h & (N - 1)];',
                             'out = buf_[h & (N - 1)];\n        if (h == t) return false;'),
    'slot by modulo N-1': ('out = buf_[h & (N - 1)];', 'out = buf_[h % (N - 1 ? N - 1 : 1)];'),
}

cxxs = compilers()
check(len(cxxs) >= 1, 'a native compiler is present')
for cxx in cxxs:
    r = run_variant(sol, cxx)
    check(all(r), '%s: solution passes all (%s)' % (cxx, r))
    r = run_variant(W['starter'], cxx)
    check(sum(r) <= 2 and r[2] and r[9], '%s: starter passes only the empty pop and the allocation test (%s)' % (cxx, r))
    print(cxx, 'solution passes all', len(r), 'tests; starter fails', len(r) - sum(r))
cxx = cxxs[0]
for name, (old, new) in BUGS.items():
    check(old in sol, 'bug anchor present: ' + name)
    r = run_variant(sol.replace(old, new), cxx)
    caught = [k + 1 for k, ok in enumerate(r) if not ok]
    print('bug %-42s caught by tests %s' % (name, caught))
    check(len(caught) >= 1, 'bug caught: ' + name)

# ---- route B: a Python model of the ring -------------------------------
M = 2 ** 32
class Ring:
    def __init__(s, n, start=0): s.n, s.h, s.t, s.buf = n, start, start, {}
    def push(s, v):
        if (s.t - s.h) % M == s.n: return False
        s.buf[s.t % s.n] = v; s.t = (s.t + 1) % M; return True
    def pop(s):
        if s.h == s.t: return None
        v = s.buf[s.h % s.n]; s.h = (s.h + 1) % M; return v
    def size(s): return (s.t - s.h) % M
    def drain(s, out, mx):
        k = 0
        while k < mx and s.size(): out.append(s.pop()); k += 1
        return k

T = W['tests']
r = Ring(8); [r.push(v) for v in (10, 20, 30)]
check([r.pop() for _ in range(3)] == T[0]['expect'], 'model E1')
r = Ring(4); check([int(r.push(v)) for v in range(1, 6)] == T[1]['expect'], 'model E2')
r = Ring(8); check([0, 77] == T[2]['expect'] and r.pop() is None, 'model T3')
r = Ring(4); [r.push(v) for v in range(1, 5)]; r.pop(); r.pop()
g = [int(r.push(v)) for v in (5, 6, 7)]
while r.size(): g.append(r.pop())
check(g == T[3]['expect'], 'model T4')
r = Ring(8); [r.push(v) for v in range(1, 6)]; r.pop(); r.pop(); check(r.size() == T[4]['expect'], 'model T5')
r = Ring(8); [r.push(v) for v in range(1, 7)]; o = []; n = r.drain(o, 4); o += [n, r.size()]
check(o == T[5]['expect'], 'model T6')
r = Ring(8); o = [99]; r.push(1); r.push(2); n = r.drain(o, 10); o += [n, r.size()]; o.append(r.drain(o, 5))
check(o == T[6]['expect'], 'model T7')
r = Ring(8, 4294967291); g = [int(r.push(v)) for v in range(1, 10)]; g.append(r.size())
while r.size(): g.append(r.pop())
g.append(r.t)
check(g == T[7]['expect'], 'model T8')
check((4294967291 + 8) % M == 3 and 4294967291 + 8 - M == 3, 'tail wraps to 3, twice')
check(M % 8 == 0 and M % 16 == 0 and M % 256 == 0, '2^32 is a multiple of each N used')
# random-call test: replay the LCG and the model, count mismatches (expect 0 by construction)
s, nxt, front, model = 12345, 1, 0, []
r = Ring(16); bad = 0; pushes = pops = drains = 0
for i in range(100000):
    s = (s * 6364136223846793005 + 1442695040888963407) % 2 ** 64
    op = (s >> 33) % 4
    if op < 2:
        pushes += 1; ok = r.push(nxt); want = len(model) - front < 16
        bad += ok != want
        if want: model.append(nxt)
        nxt += 1
    elif op == 2:
        pops += 1; v = r.pop(); want = len(model) > front
        bad += (v is not None) != want
        if want: bad += v != model[front]; front += 1
    else:
        drains += 1; o = []; n = r.drain(o, 3); want = min(3, len(model) - front)
        bad += n != want; bad += o != model[front:front + want]; front += want
    bad += r.size() != len(model) - front
check(bad == T[11]['expect'], 'model T12')
print('random test: %d pushes, %d pops, %d drains, model mismatches %d' % (pushes, pops, drains, bad))
check(pushes + pops + drains == 100000, 'random test makes 100,000 calls')
check('4,294,967,295' in item['prose'] and 2 ** 32 - 1 == 4294967295, 'wrap figure')
check('100,000' in W['how'] and 'Twelve' in W['how'], 'how figures')

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
