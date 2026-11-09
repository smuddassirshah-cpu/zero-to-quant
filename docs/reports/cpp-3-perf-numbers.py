"""cpp level 3 performance task h-session-range: recompute every number and run
the solution, the starter and planted wrong solutions against every hidden test.

Route A: the widget's prelude, the code and each value test's setup and call are
compiled natively with g++ and clang++ at -std=c++20 -O1 -fno-exceptions (and
-D_GLIBCXX_ASSERTIONS), one process per test as in the app; a raises test passes
when the process ends abnormally; a compile test passes when -fsyntax-only agrees
with its expect. Route B: every expected value is recomputed by a Python model of
the range (min and max over the values each test feeds in), and the numbers in
the explain are recomputed. Exit 0 only if all agree, the solution passes every
test on both compilers, the starter fails, and every planted slip is caught.
"""
import json, math, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'cpp', 'homework-3.json')
items = json.load(open(HW))['items']
idx = next(k for k, i in enumerate(items) if i['id'] == 'h-session-range')
item = items[idx]
W = item['widget']
T = W['tests']
fails = []

def check(cond, msg):
    print('ok  ' if cond else 'FAIL', msg)
    if not cond:
        fails.append(msg)

# ---- shape --------------------------------------------------------------
check(item.get('performance') == 'code' and W['language'] == 'cpp', 'performance code item in C++')
check(idx == len(items) - 1 and len(items) == 8, 'appended as item 8 of 8 (index 7)')
check(3 <= len(T) <= 15 and len(T) > len(W['examples']), 'more tests than examples, at most 15')
check(all(e in T for e in W['examples']), 'the example is also a test')
check('14 hidden tests' in W['how'] and len(T) == 14, 'how says 14 hidden tests')
check(sum(1 for t in T if t.get('compare') == 'raises') == 1, 'how: one raises test')
check(sum(1 for t in T if 'compiles' in t) == 2, 'how: two compile tests')
check(not item.get('hints'), 'no hints')

# ---- route B: a Python model --------------------------------------------
class R:
    def __init__(s, lo, hi=None):
        hi = lo if hi is None else hi
        if lo > hi: raise ValueError('low above high')
        s.lo, s.hi = lo, hi
    def add(s, x): s.lo, s.hi = min(s.lo, x), max(s.hi, x)
    def iadd(s, o): s.add(o.lo); s.add(o.hi); return s
    def plus(s, o): c = R(s.lo, s.hi); return c.iadd(o)
    def width(s): return float(s.hi) - float(s.lo)
    def eq(s, o): return s.lo == o.lo and s.hi == o.hi
    def text(s):
        f = lambda v: ('%g' % v) if isinstance(v, float) else str(v)
        return '[%s, %s]' % (f(s.lo), f(s.hi))

r = R(100); [r.add(x) for x in (97, 104, 101)]
model = [None] * len(T)
model[0] = [r.lo, r.hi]; model[1] = r.width()
r = R(50); r.add(60); r.add(55); model[2] = [r.lo, r.hi]
r = R(101.5); r.add(99.25); r.add(100.75); model[3] = r.width()
model[4] = R(-2000000000, 2000000000).width()
try:
    R(5, 3); model[5] = 'no stop'
except ValueError:
    model[5] = 'stops'
r = R(5000000000, 5000000000); r.add(4999999990); model[6] = r.width()
a, b, c = R(10), R(5), R(20); a.iadd(b).iadd(c); model[7] = [a.lo, a.hi]
a, b = R(10), R(5, 30); c = a.plus(b); model[8] = [a.lo, a.hi, b.lo, b.hi, c.lo, c.hi]
a = R(1, 9); a.iadd(R(3, 4)); model[9] = [a.lo, a.hi]
model[10] = [int(R(1, 4).eq(R(1, 4))), int(R(1, 4).eq(R(1, 5))), int(not R(1, 4).eq(R(1, 5))), int(not R(2, 4).eq(R(1, 4))), int(not R(1, 4).eq(R(1, 4)))]
model[11] = R(99.5, 101.25).text() + ';' + R(-3).text() + ';'
for k, t in enumerate(T):
    if 'compiles' in t:
        continue
    if t.get('compare') == 'raises':
        check(model[k] == 'stops', 'test %d: the model refuses low above high' % (k + 1))
    elif t['compare'] == 'isclose':
        check(math.isclose(model[k], t['expect'], rel_tol=1e-12), 'test %d: expect %s, model %s' % (k + 1, t['expect'], model[k]))
    else:
        check(model[k] == t['expect'], 'test %d: expect %s, model %s' % (k + 1, t['expect'], model[k]))

# numbers in the explain and how
INT_MAX = 2 ** 31 - 1
ex = item['explain']['text']
check(2000000000 - (-2000000000) == 4000000000 and '4,000,000,000' in ex, 'explain: the width 4,000,000,000')
check(INT_MAX == 2147483647 and '2,147,483,647' in ex and 4000000000 > INT_MAX, 'explain: past the int limit 2,147,483,647')
check(abs(2000000000) <= INT_MAX, 'test 5: both ends fit in an int')
check(5000000000 > INT_MAX, 'test 7: the long long ends do not fit in an int')
check(float(4000000000) == 4000000000.0, 'test 5: 4e9 is exact as a double')
w32 = ((2000000000 - (-2000000000) + 2 ** 31) % 2 ** 32) - 2 ** 31
check(w32 == -294967296, 'an int width wraps to -294,967,296 (the slip test 5 catches)')

# ---- route A: native builds -------------------------------------------------
PRINT = r'''
#include <cstdio>
#include <string>
#include <vector>
static void zq_print(double v) { std::printf("%.17g\n", v); }
static void zq_print(const std::string& s) { std::printf("%s\n", s.c_str()); }
static void zq_print(const std::vector<int>& v) { std::string s = "["; for (std::size_t i = 0; i < v.size(); ++i) { if (i) s += ", "; s += std::to_string(v[i]); } std::printf("%s]\n", s.c_str()); }
'''
FLAGS = ['-std=c++20', '-O1', '-fno-exceptions', '-D_GLIBCXX_ASSERTIONS', '-w']

def ok_value(out, t):
    out = out.strip()
    if t['compare'] == 'isclose':
        try:
            return math.isclose(float(out), t['expect'], rel_tol=1e-9)
        except ValueError:
            return False
    if isinstance(t['expect'], list):
        return out == '[' + ', '.join(str(x) for x in t['expect']) + ']'
    return out == t['expect']

def run_variant(code, cxx):
    tmp = tempfile.mkdtemp()
    res = [False] * len(T)
    vals = [k for k, t in enumerate(T) if 'compiles' not in t]
    body = W['prelude'] + code + PRINT + '#include <cstdlib>\nint main(int argc, char** argv) {\n int which = std::atoi(argv[1]);\n'
    for k in vals:
        t = T[k]
        body += ' if (which == %d) { %s zq_print(%s); }\n' % (k, t.get('setup', ''), t['call'])
    body += ' return 0;\n}\n'
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx] + FLAGS + [src, '-o', exe], capture_output=True, text=True)
    if cp.returncode == 0:
        for k in vals:
            pr = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
            if T[k].get('compare') == 'raises':
                res[k] = pr.returncode != 0
            else:
                res[k] = pr.returncode == 0 and ok_value(pr.stdout, T[k])
    elif os.environ.get('SHOWERR'):
        print(cp.stderr[:3000])
    for k, t in enumerate(T):
        if 'compiles' in t:
            s2 = os.path.join(tmp, 'c%d.cpp' % k)
            open(s2, 'w').write(W['prelude'] + code + '\nvoid zq_check() { %s %s }\nint main() { return 0; }\n' % (t.get('setup', ''), t['compiles']))
            built = subprocess.run([cxx] + FLAGS + ['-fsyntax-only', s2], capture_output=True).returncode == 0
            res[k] = built == t['expect']
    shutil.rmtree(tmp)
    return res

sol = W['solution']
BUGS = {
    '+= returns a copy': ('    SessionRange& operator+=(', '    SessionRange operator+=('),
    '+ takes its left side by reference and widens it': ('operator+(SessionRange<T> a,', 'operator+(SessionRange<T>& a,'),
    'width in T (int overflow)': ('return static_cast<double>(high_) - static_cast<double>(low_);', 'return high_ - low_;'),
    'constructor does not check': ('        if (low_ > high_) std::abort();   // a throw ends the run too\n', ''),
    'constructor refuses equal ends': ('if (low_ > high_) std::abort();', 'if (low_ >= high_) std::abort();'),
    'add with else moves the high down': ('        if (x < low_) low_ = x;\n        if (x > high_) high_ = x;', '        if (x < low_) low_ = x;\n        else high_ = x;'),
    '+= copies the other ends': ('        add(other.low_);\n        add(other.high_);', '        low_ = other.low_;\n        high_ = other.high_;'),
    '== compares the low only': ('return a.low() == b.low() && a.high() == b.high();', 'return a.low() == b.low();'),
    '!= written as low below': ('return !(a == b);', 'return a.low() < b.low();'),
    '!= compares the low only': ('return !(a == b);', 'return a.low() != b.low();'),
    '<< returns void': ('std::ostream& operator<<(std::ostream& os, const SessionRange<T>& r) {\n    return os <<', 'void operator<<(std::ostream& os, const SessionRange<T>& r) {\n    os <<'),
    '<< takes a non-const reference': ('std::ostream& operator<<(std::ostream& os, const SessionRange<T>& r)', 'std::ostream& operator<<(std::ostream& os, SessionRange<T>& r)'),
    'readers not const': ('    T low() const { return low_; }\n    T high() const { return high_; }', '    T low() { return low_; }\n    T high() { return high_; }'),
    'one-value constructor not explicit': ('    explicit SessionRange(T first)', '    SessionRange(T first)'),
    'width truncated to long long': ('    double width() const {\n        return static_cast<double>(high_) - static_cast<double>(low_);', '    double width() const {\n        return static_cast<long long>(high_) - static_cast<long long>(low_);'),
}
ALT = r'''#include <cstdlib>
#include <ostream>

template <typename T>
class SessionRange {
    T lo_, hi_;
public:
    explicit SessionRange(T v) : lo_(v), hi_(v) {}
    SessionRange(T lo, T hi) : lo_(lo), hi_(hi) { if (hi < lo) std::abort(); }
    void add(T x) { lo_ = x < lo_ ? x : lo_; hi_ = hi_ < x ? x : hi_; }
    T low() const { return lo_; }
    T high() const { return hi_; }
    double width() const { return double(hi_) - double(lo_); }
    SessionRange& operator+=(const SessionRange& o) {
        if (o.lo_ < lo_) lo_ = o.lo_;
        if (hi_ < o.hi_) hi_ = o.hi_;
        return *this;
    }
    friend SessionRange operator+(const SessionRange& a, const SessionRange& b) {
        SessionRange c = a;
        c += b;
        return c;
    }
    friend bool operator==(const SessionRange& a, const SessionRange& b) { return a.lo_ == b.lo_ && a.hi_ == b.hi_; }
    friend bool operator!=(const SessionRange& a, const SessionRange& b) { return !(a == b); }
    friend std::ostream& operator<<(std::ostream& os, const SessionRange& r) { os << '[' << r.lo_ << ", " << r.hi_ << ']'; return os; }
};
'''
NOT_TEMPLATE = sol.replace('template <typename T>\nclass SessionRange {', 'using T = int;\nclass SessionRange {', 1)

cxxs = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(len(cxxs) == 2, 'g++ and clang++ both present')
for cxx in cxxs:
    r = run_variant(sol, cxx)
    check(all(r), '%s: solution passes all %d tests %s' % (cxx, len(r), r))
    r = run_variant(ALT, cxx)
    check(all(r), '%s: a second solution (friend operators, ternaries) passes all %d tests' % (cxx, len(r)))
    FLAGS[0] = '-std=c++17'
    r = run_variant(sol, cxx)
    check(all(r), '%s: solution passes all tests at -std=c++17 (the app standard)' % cxx)
    FLAGS[0] = '-std=c++20'
    r = run_variant(W['starter'], cxx)
    check(not all(r), '%s: starter fails tests %s' % (cxx, [k + 1 for k, ok in enumerate(r) if not ok]))
    for name, (old, new) in BUGS.items():
        check(old in sol, 'anchor present: ' + name)
        r = run_variant(sol.replace(old, new), cxx)
        check(not all(r), '%s: bug "%s" caught by tests %s' % (cxx, name, [k + 1 for k, ok in enumerate(r) if not ok]))
    r = run_variant(NOT_TEMPLATE, cxx)
    check(not all(r), '%s: bug "a plain class, not a template" caught by tests %s' % (cxx, [k + 1 for k, ok in enumerate(r) if not ok]))

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
