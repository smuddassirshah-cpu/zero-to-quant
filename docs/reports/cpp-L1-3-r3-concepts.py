#!/usr/bin/env python3
"""Round 3 concept checks for cpp L1 to L3 (audit-cpp-1-3-r3).

Every check is a code-behaviour claim in the content, run either under the app's own compiler and grader
(YoWASP clang 21, wasm32, libc++, -O1, hardened, no exceptions; driven through docs/reports/cpp-L1-3-r2-zq.mjs)
or under local g++ / clang++ / clang-tidy where the content quotes those tools.

usage: python3 cpp-L1-3-r3-concepts.py [--pkgs <pkgs folder>] [L1|L2|L3 ...]
Exits 0 when every check agrees with the content. A check that fails because the content is wrong stays
failing until the content is fixed (round 3: finding 1, l13 screens[4] feedback.byKey.l7, fixed in the fix pass). Lines named NOTE are the measurements behind
imprecise findings; they pass because they state what was measured.
"""
import json, os, subprocess, sys, tempfile, shutil, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE)) if os.path.basename(HERE) == 'reports' else os.getcwd()
APP = os.path.join(ROOT, 'app')
DRIVER = os.path.join(ROOT, 'docs', 'reports', 'cpp-L1-3-r2-zq.mjs')
PKGS = '/tmp/claude-0/-home-user-zero-to-quant/bc4f6fd7-77dd-5244-9985-b0979ee22fb1/scratchpad/pkgs'
args = sys.argv[1:]
if '--pkgs' in args:
    k = args.index('--pkgs'); PKGS = args[k + 1]; del args[k:k + 2]
LEVELS = set(args) or {'L1', 'L2', 'L3'}
TMP = tempfile.mkdtemp(prefix='cppr3-')

JOBS = []      # app-compiler jobs
CHECKS = []    # (level, name, fn(results) -> (ok, detail))
LOCAL = []     # (level, name, fn() -> (ok, detail))


def grade(level, name, file, path, src, want, also=None):
    """Submit src to the widget at file/path; want is the grader key ('test-N', 'compile' or None for a pass).
    also(result) may add a further condition and returns (ok, detail)."""
    if level not in LEVELS:
        return
    JOBS.append({'name': name, 'file': file, 'path': path, 'src': src})

    def chk(res):
        r = res.get(name, {})
        key = r.get('key', 'MISSING' if not r else None)
        ok = key == want
        det = f'key={key} fails={r.get("fails")}'
        if r.get('exception'):
            return False, r['exception'][:200]
        if ok and also:
            ok2, d2 = also(r)
            return ok2, det + ' ' + d2
        if not ok:
            rows = r.get('rows') or []
            bad = [f'{i + 1}:{x.get("actual")}/{(x.get("error") or "")[:60]}/{(x.get("stdout") or "")[:40]!r}' for i, x in enumerate(rows) if not x.get('ok')][:3]
            det += ' ' + ' '.join(bad) + ' ' + (r.get('diag') or '')[:300].replace('\n', ' ')
        return ok, det
    CHECKS.append((level, name, chk))


def prog(level, name, src, fn, flags=None, stdin=''):
    """Compile and run a whole program under the app compiler; fn(result) -> (ok, detail)."""
    if level not in LEVELS:
        return
    JOBS.append({'name': name, 'prog': src, 'flags': flags or [], 'stdin': stdin})
    CHECKS.append((level, name, lambda res: fn(res.get(name, {}))))


def out_is(expect, diag_has=None):
    def f(r):
        o = (r.get('out') or '')
        ok = r.get('ok') and o.strip() == expect.strip() and not r.get('trap')
        if diag_has and diag_has not in (r.get('diag') or ''):
            ok = False
        return bool(ok), f'out={o[:80]!r} trap={r.get("trap")} code={r.get("code")} diag={(r.get("diag") or "")[:160]!r}'
    return f


def no_compile(*needles):
    def f(r):
        d = r.get('diag') or ''
        ok = r.get('ok') is False and all(n in d for n in needles)
        return ok, f'compiled={r.get("ok")} diag={d[:260]!r}'
    return f


def traps(needle=''):
    def f(r):
        t = str(r.get('trap')) + ' ' + str(r.get('err')) + ' code=' + str(r.get('code'))
        ok = bool(r.get('ok')) and (bool(r.get('trap')) or (r.get('code') not in (0, None))) and needle in t
        return ok, f'out={(r.get("out") or "")[:60]!r} {t[:200]}'
    return f


def cc(compiler, src, flags=(), run=False, stdin='', files=None, name='main.cpp'):
    d = tempfile.mkdtemp(dir=TMP)
    for fn, s in (files or {name: src}).items():
        open(os.path.join(d, fn), 'w').write(s)
    srcs = [f for f in (files or {name: src}) if f.endswith('.cpp')]
    p = subprocess.run([compiler, '-std=c++17', *flags, *srcs, '-o', 'main'], cwd=d, capture_output=True, text=True, env={**os.environ, 'LC_ALL': 'C'})
    out = ''
    if run and p.returncode == 0:
        q = subprocess.run(['./main'], cwd=d, capture_output=True, text=True, input=stdin, env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=1'})
        out = q.stdout + '\n--stderr--\n' + q.stderr + f'\n--rc {q.returncode}--'
    return p.returncode, p.stderr, out


def local(level, name, fn):
    if level in LEVELS:
        LOCAL.append((level, name, fn))


def has(compiler, src, flags, *needles, rc=None, absent=(), run_has=None, **kw):
    """needles must appear in the compiler's stderr; run_has (a list) must appear in the program's stdout+stderr."""
    def f():
        r, err, out = cc(compiler, src, flags, run=run_has is not None, **kw)
        ok = all(n in err for n in needles) and not any(a in err for a in absent)
        if rc is not None:
            ok = ok and ((r == 0) == (rc == 0))
        if run_has is not None:
            ok = ok and all(n in out for n in run_has)
        return ok, f'rc={r} run={out[:300]!r} err={err[:300]!r}'
    return f


def at(file, path):
    d = json.load(open(os.path.join(APP, 'content/courses/cpp', file + '.json')))
    for k in path.split('.'):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def sol(file, path):
    return at(file, path)['solution']


def main():
    fails = 0
    total = 0
    for level, name, fn in LOCAL:
        total += 1
        try:
            ok, det = fn()
        except Exception as e:
            ok, det = False, repr(e)
        fails += not ok
        print(('ok   ' if ok else 'FAIL ') + f'{level} {name}' + ('' if ok and '-v' not in sys.argv else '  :: ' + det))
    res = {}
    if JOBS:
        n = 4
        procs = []
        for i in range(n):
            part = JOBS[i::n]
            if not part:
                continue
            # the driver's first compile in a process sometimes never settles when it carries extra flags; start with a plain one
            part = [{'name': f'_warm{i}', 'prog': 'int main(){}'}] + part
            jf, of = os.path.join(TMP, f'j{i}.json'), os.path.join(TMP, f'o{i}.json')
            json.dump(part, open(jf, 'w'))
            procs.append((subprocess.Popen(['node', DRIVER, APP, PKGS, jf, of], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True), of))
        for p, of in procs:
            o, _ = p.communicate()
            if os.path.exists(of):
                res.update(json.load(open(of)))
            if p.returncode:
                print('driver:', o[-400:])
    for level, name, fn in CHECKS:
        total += 1
        try:
            ok, det = fn(res)
        except Exception as e:
            ok, det = False, repr(e)
        fails += not ok
        print(('ok   ' if ok else 'FAIL ') + f'{level} {name}  :: ' + det[:420])
    shutil.rmtree(TMP, ignore_errors=True)
    print(f'{total - fails} of {total} checks agree with the content')
    sys.exit(1 if fails else 0)


# ------------------------------------------------------------------ L1
L = 'L1'
H = '#include <iostream>\n#include <iomanip>\n#include <string>\n#include <vector>\n#include <cmath>\n'

# l1 screens[3]: test 2 is the exact comparison
F = 'l1-source-to-program'
s = sol(F, 'screens.3.widget')
grade(L, 'l1.s3 space before the line end -> test-2', F, 'screens.3.widget', s.replace('"Hello, market"', '"Hello, market "'), 'test-2')
grade(L, 'l1.s3 blank line after -> test-2', F, 'screens.3.widget', s.replace("'\\n'", '"\\n\\n"'), 'test-2')
grade(L, 'l1.s4 getline then >> -> test-2', F, 'screens.4.widget', '''#include <iostream>
#include <string>
int main() {
    std::string ticker; double price;
    std::getline(std::cin, ticker);
    std::cin >> price;
    std::cout << "Ticker: " << ticker << '\\n';
    std::cout << "Price: " << price << '\\n';
}
''', 'test-2')
grade(L, 'l1.s4 fixed two decimals (72.50) -> test-1', F, 'screens.4.widget', '''#include <iostream>
#include <iomanip>
#include <string>
int main() {
    std::string ticker; double price;
    std::cin >> ticker >> price;
    std::cout << "Ticker: " << ticker << '\\n';
    std::cout << "Price: " << std::fixed << std::setprecision(2) << price << '\\n';
}
''', 'test-1')
SEMI = '''#include <iostream>

int main() {
    double price = 101.5
    std::cout << price << '\\n';
    return 0;
}
'''
prog(L, 'l1.s6 app clang: expected ; at end of declaration, on line 4', SEMI, no_compile("main.cpp:4:", "expected ';' at end of declaration"))
local(L, 'l1.s5 g++ message for the missing semicolon', has('g++', SEMI, [], "main.cpp: In function 'int main()':", "main.cpp:5:5: error: expected ',' or ';' before 'std'", rc=1))
UNUSED = '''#include <iostream>

int main() {
    int qty = 100;
    std::cout << "Hello, market" << '\\n';
}
'''
local(L, 'l1.s7 g++ -Wall unused variable, builds and runs', has('g++', UNUSED, ['-Wall'], "main.cpp:4:9: warning: unused variable 'qty' [-Wunused-variable]", rc=0, run_has=['Hello, market', '--rc 0--']))
ASSIGN = '''#include <iostream>
int main() {
    int signals = 3;
    if (signals = 0) {
        std::cout << "flat\\n";
    }
    std::cout << signals << '\\n';
}
'''
local(L, 'l1.s8 g++ silent without -Wall, prints 0', has('g++', ASSIGN, [], rc=0, absent=['warning'], run_has=['0\n']))
local(L, 'l1.s8 g++ -Wall warns', has('g++', ASSIGN, ['-Wall'], 'warning', rc=0))
prog(L, 'l1.s8 app clang warns by default, prints 0', ASSIGN, out_is('0', 'warning: using the result of an assignment as a condition'))
VEC = '''#include <iostream>
#include <vector>

int main() {
    std::vector<double> closes{101.5, 102.0};
    std::cout << closes << '\\n';
}
'''
local(L, 'l1.s10 g++ first error line for printing a vector', has('g++', VEC, [], "main.cpp:6:15: error: no match for 'operator<<' (operand types are 'std::ostream' {aka 'std::basic_ostream<char>'} and 'std::vector<double>')", rc=1))


def veclines():
    r, err, out = cc('g++', VEC, [])
    n = len(err.strip().split('\n'))
    return n == 232, f'g++ printed {n} lines (content says 232)'


local(L, 'l1.s10 g++ prints 232 lines', veclines)
local(L, 'l1.quiz0 g++ did-you-mean message', has('g++', '''#include <iostream>

int main() {
    double price = 101.5;
    std::cout << pirce << '\\n';
}
''', [], "main.cpp:5:18: error: 'pirce' was not declared in this scope; did you mean 'price'?", rc=1))

# l2
F = 'l2-fixed-types'
prog(L, 'l2.s1 app build: 2147483645 + 1 three times prints -2147483648', H + 'int main(){ int count; std::cin >> count; count = count + 1; count = count + 1; count = count + 1; std::cout << count << "\\n"; }', out_is('-2147483648'), stdin='2147483645\n')
prog(L, 'l2 arithmetic table and sizes (wasm32)', H + '''int main(){ volatile int m7 = -7, m9 = -9, three = 3, one = 1;
 std::cout << 7 / 2 << ' ' << m7 / 2 << ' ' << m9 / 4 << ' ' << three / 4 * 1.0 << ' ' << static_cast<double>(three / 4) << ' ' << 3.0 / 4 << ' ' << (101.5 > 100.0) << ' ';
 double share = one / 4; auto r = 7 / 2; std::cout << share << ' ' << r << ' ' << sizeof(r) << '\\n';
 std::cout << sizeof(int) << sizeof(long long) << sizeof(double) << sizeof(bool) << sizeof(char) << ' ' << sizeof(long) << sizeof(std::size_t) << sizeof(std::vector<double>) << '\\n'; }''',
     out_is('3 -3 -2 0 0 0.75 1 0 3 4\n48811 4412'))
prog(L, 'l2.s7 and homework-1 items[5]: 19.99 and 0.29 times 100', H + '''int main(){ double price; while (std::cin >> price) { int pence = price * 100; std::cout << pence << ' ' << std::lround(price * 100) << ' ' << std::setprecision(17) << price * 100 << ' ' << price << '\\n'; } }''',
     out_is('1998 1999 1998.9999999999998 19.989999999999998\n28 29 28.999999999999996 0.28999999999999998'), stdin='19.99 0.29\n')
prog(L, 'l2.s5 20000 * 107500 stored in an int prints -2144967296', H + 'int main(){ long long q, p; std::cin >> q >> p; int value = q * p; std::cout << value << "\\n"; }', out_is('-2144967296'), stdin='20000 107500\n')
grade(L, 'l2.s4 starter -> test-1 (returns 3)', F, 'screens.4.widget', at(F, 'screens.4.widget')['starter'], 'test-1', lambda r: (r['rows'][0]['actual'] == '3', 'actual=' + str(r['rows'][0]['actual'])))
grade(L, 'l2.s4 (a + b) / 2.0 -> test-5', F, 'screens.4.widget', 'double average(int a, int b) {\n    return (a + b) / 2.0;\n}\n', 'test-5')
grade(L, 'l2.s5 starter -> test-2, negative', F, 'screens.5.widget', at(F, 'screens.5.widget')['starter'], 'test-2', lambda r: (r['rows'][1]['actual'] == '-2144967296', 'actual=' + str(r['rows'][1]['actual'])))
grade(L, 'l2.s9 divide by int 100 -> test-3 (0)', F, 'screens.9.widget', 'double pnl_pounds(long long b, long long s, long long q) { long long pence = (s - b) * q; return pence / 100; }\n', 'test-3', lambda r: (r['rows'][2]['actual'] == '0', 'actual=' + str(r['rows'][2]['actual'])))
grade(L, 'l2.s9 int pence -> test-2 (positive)', F, 'screens.9.widget', 'double pnl_pounds(long long b, long long s, long long q) { int pence = (s - b) * q; return pence / 100.0; }\n', 'test-2', lambda r: (float(r['rows'][1]['actual']) > 0, 'actual=' + str(r['rows'][1]['actual'])))

# l3
F = 'l3-branches-and-loops'
P = 'screens.3.widget'
s = sol(F, P)
LOOP = 'for (std::size_t i = 1; i < prices.size(); ++i) {\n        if (prices[i] > prices[i - 1]) {'
assert LOOP in s
grade(L, 'l3.s3 i < size() - 1 -> test-2', F, P, s.replace(LOOP, 'for (std::size_t i = 0; i < prices.size() - 1; ++i) {\n        if (prices[i + 1] > prices[i]) {'), 'test-2')
grade(L, 'l3.s3 >= -> test-6', F, P, s.replace('prices[i] > prices[i - 1]', 'prices[i] >= prices[i - 1]'), 'test-6')
grade(L, 'l3.s3 i <= size() -> test-1, index out of bounds', F, P, s.replace('i < prices.size()', 'i <= prices.size()'), 'test-1', lambda r: ('out of bounds' in (r['rows'][0]['error'] or ''), 'error=' + str(r['rows'][0]['error'])[:120]))
P = 'screens.4.widget'
grade(L, 'l3.s4 measured from the first close -> test-1 (0.12)', F, P, '#include <vector>\ndouble max_drawdown(const std::vector<double>& prices) { double worst = 0; for (double p : prices) { double fall = (prices[0] - p) / prices[0]; if (fall > worst) worst = fall; } return worst; }\n', 'test-1', lambda r: (r['rows'][0]['actual'].startswith('0.12'), 'actual=' + str(r['rows'][0]['actual'])))
grade(L, 'l3.s4 sign flipped -> test-1 (0)', F, P, sol(F, P).replace('(peak - p) / peak', '(p - peak) / peak'), 'test-1', lambda r: (r['rows'][0]['actual'] == '0', 'actual=' + str(r['rows'][0]['actual'])))
P = 'screens.5.widget'
grade(L, 'l3.s5 total starts at n -> test-1 (9.75)', F, P, sol(F, P).replace('double total = 0;', 'double total = n;'), 'test-1', lambda r: ('9.75' in r['rows'][0]['stdout'], 'stdout=' + r['rows'][0]['stdout']))
prog(L, 'l3.s6 app build stops prices[3]', H + 'int main(){ std::vector<double> prices{101.2, 102.5, 99.8}; double last = 0; for (std::size_t i = 0; i <= prices.size(); ++i) { last = prices[i]; } std::cout << last << "\\n"; }', traps('index out of bounds'))
P = 'screens.8.widget'
grade(L, 'l3.s8 starter -> test-1 with Cboe 3', F, P, at(F, P)['starter'], 'test-1', lambda r: (r['rows'][0]['actual'] == '[2,3,0,0]', 'actual=' + str(r['rows'][0]['actual'])))
grade(L, 'l3.s8 no default -> test-3', F, P, sol(F, P).replace("            default: ++counts[3]; break;\n", ''), 'test-3')
prog(L, 'l3 quiz0, quiz3 and the 0.3 print', H + '''int main(){ volatile double a = 0.1, b = 0.2; std::cout << (a + b == 0.3 ? "equal" : "different") << ' ' << a + b << ' ';
 int day = 0; for (double p : {101.0, 97.5, 94.0, 92.0, 99.0}) { if (p < 95) break; ++day; } std::cout << day << ' ' << std::setprecision(17) << a + b << '\\n'; }''', out_is('different 0.3 2 0.30000000000000004'))
prog(L, 'l3.quiz2 empty vector, size() - 1 wraps and the loop reads past the end', H + 'int main(){ std::vector<double> prices; std::cout << prices.size() - 1 << std::endl; for (std::size_t i = 0; i < prices.size() - 1; ++i) { std::cout << prices[i] << "\\n"; } }', lambda r: (r.get('out', '').startswith('4294967295') and bool(r.get('trap') or r.get('code')), f"out={r.get('out','')[:30]!r} trap={r.get('trap')}"))
local(L, 'l3.s7 loop variable is out of scope after the for', has('g++', H + 'int main(){ for (int i = 0; i < 5; ++i) { } std::cout << i; }', [], "'i' was not declared in this scope", rc=1))
FT = '#include <vector>\n#include <string>\nstd::vector<int> f(const std::string& venues){ std::vector<int> counts(4,0); for(char v: venues){ switch(v){ case 76: ++counts[0];\n case 67: ++counts[1]; break; } } return counts; }\nint main(){}\n'
local(L, 'l3.s8 fall-through: g++ silent with -Wall', has('g++', FT, ['-Wall'], rc=0, absent=['warning']))
local(L, 'l3.s8 fall-through: clang++ silent with -Wall -Wextra', has('clang++', FT, ['-Wall', '-Wextra'], rc=0, absent=['warning']))
local(L, 'l3.s8 fall-through: flagged by -Wimplicit-fallthrough', has('g++', FT, ['-Wimplicit-fallthrough'], 'fall through', rc=0))

# l4
F = 'l4-functions-and-headers'
local(L, 'l4.s0 g++ not declared in this scope at 5:18', has('g++', '''#include <cmath>
#include <iostream>

int main() {
    std::cout << annualise(0.01) << '\\n';
}

double annualise(double daily_vol) {
    return daily_vol * std::sqrt(252.0);
}
''', [], "main.cpp: In function 'int main()':", "main.cpp:5:18: error: 'annualise' was not declared in this scope", rc=1))
prog(L, 'l4.s1/s4 prints 0.158745 and 0.19105', H + 'double annualise(double daily_vol, int days = 252);\nint main(){ std::cout << annualise(0.01) << " " << annualise(0.01, 365) << "\\n"; }\ndouble annualise(double daily_vol, int days) { return daily_vol * std::sqrt(days); }', out_is('0.158745 0.19105'))
P = 'screens.5.widget'
s = sol(F, P)
SIG = 'std::vector<double> simple_returns(const std::vector<double>& prices) {'
assert SIG in s
grade(L, 'l4.s5 by-value definition -> compile, ambiguous', F, P, s.replace(SIG, 'std::vector<double> simple_returns(std::vector<double> prices) {'), 'compile', lambda r: ('ambiguous' in r['diag'], r['diag'][:200]))
grade(L, 'l4.s5 non-const reference definition -> compile, undefined symbol', F, P, s.replace(SIG, 'std::vector<double> simple_returns(std::vector<double>& prices) {'), 'compile', lambda r: ('undefined symbol' in r['diag'], r['diag'][:300]))
grade(L, 'l4.s5 different return type -> compile, previous declaration', F, P, s.replace(SIG, 'std::vector<float> simple_returns(const std::vector<double>& prices) {').replace('std::vector<double> out;', 'std::vector<float> out;'), 'compile', lambda r: ('previous declaration' in r['diag'], r['diag'][:300]))
grade(L, 'l4.s5 do-while reads prices[1] -> test-2', F, P, '#include <vector>\n' + SIG + '\n std::vector<double> out; if (prices.empty()) return out; std::size_t i = 1;\n do { out.push_back((prices[i] - prices[i - 1]) / prices[i - 1]); ++i; } while (i < prices.size());\n return out; }\n', 'test-2')
grade(L, 'l4.s5 divide by today -> test-1', F, P, s.replace('/ prices[i - 1]', '/ prices[i]'), 'test-1')
grade(L, 'l4.s5 size() - 1 -> test-3', F, P, '#include <vector>\n' + SIG + '\n std::vector<double> out;\n for (std::size_t i = 0; i < prices.size() - 1; ++i) out.push_back((prices[i + 1] - prices[i]) / prices[i]);\n return out; }\n', 'test-3')
P = 'screens.6.widget'
grade(L, 'l4.s6 default repeated -> compile, redefinition of default argument', F, P, sol(F, P).replace('int days)', 'int days = 252)'), 'compile', lambda r: ('redefinition of default argument' in r['diag'], r['diag'][:200]))
prog(L, 'l4.s8 default only in the definition: the call does not compile', H + 'double annualise(double daily_vol, int days);\nint main(){ std::cout << annualise(0.01); }\ndouble annualise(double daily_vol, int days = 252) { return daily_vol * std::sqrt(days); }', no_compile('error'))
prog(L, 'l4.quiz0 overloads print 10001 100.015', H + 'double mid(double bid, double ask) { return (bid + ask) / 2; }\nlong long mid(long long bid, long long ask) { return (bid + ask) / 2; }\nint main(){ std::cout << mid(10001LL, 10002LL) << \' \' << mid(100.01, 100.02); }', out_is('10001 100.015'))
prog(L, 'l4.quiz1 function name without () prints 1', H + 'double risk_free_rate() { return 0.04; }\nint main(){ std::cout << risk_free_rate << "\\n"; }', out_is('1'))
local(L, 'l4.quiz1 risk_free_rate(void) and (0) do not compile', lambda: (cc('g++', H + 'double risk_free_rate() { return 0.04; }\nint main(){ std::cout << risk_free_rate(void); }')[0] != 0 and cc('g++', H + 'double risk_free_rate() { return 0.04; }\nint main(){ std::cout << risk_free_rate(0); }')[0] != 0, ''))
HDR = '#pragma once\ndouble simple_return(double before, double after) {\n    return (after - before) / before;\n}\n'
local(L, 'l4.s7 body in a header: multiple definition from ld', has('g++', None, [], "multiple definition of `simple_return(double, double)'", 'first defined here', 'collect2: error: ld returned 1 exit status', rc=1,
      files={'returns.h': HDR, 'main.cpp': '#include "returns.h"\nint main(){ return simple_return(1, 2) > 0; }\n', 'pricer.cpp': '#include "returns.h"\ndouble px(){ return simple_return(1, 2); }\n'}))
local(L, 'l4.s7 inline fixes it', has('g++', None, [], rc=0,
      files={'returns.h': HDR.replace('double simple', 'inline double simple'), 'main.cpp': '#include "returns.h"\nint main(){ return simple_return(1, 2) > 0; }\n', 'pricer.cpp': '#include "returns.h"\ndouble px(){ return simple_return(1, 2); }\n'}))
local(L, 'l4.quiz2 undefined reference from ld', has('g++', 'double annualise(double daily_vol, int days = 252);\nint main(){ return annualise(0.01) > 0; }\n', [], "undefined reference to `annualise(double, int)'", 'collect2: error: ld returned 1 exit status', rc=1))

# review-1, homework-1
F = 'review-1'
P = 'items.5.widget'
grade(L, 'review-1.5 <= -> test-3', F, P, sol(F, P).replace('x < -limit', 'x <= -limit'), 'test-3')
grade(L, 'review-1.5 compare with limit -> test-1', F, P, sol(F, P).replace('x < -limit', 'x < limit'), 'test-1')
F = 'homework-1'
P = 'items.1.widget'
s = sol(F, P)
C = 'std::size_t comma = line.find(\',\');\n        if (comma == std::string::npos) {\n            continue;\n        }'
assert C in s
grade(L, 'homework-1.1 skips only empty lines -> test-6', F, P, s.replace(C, "if (line.empty()) continue;\n        std::size_t comma = line.find(',');"), 'test-6')
grade(L, 'homework-1.1 measures from the highest close of the whole file -> test-4', F, P, '''#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
int main() {
    std::string line; std::getline(std::cin, line);
    std::vector<double> px; double top = 0;
    while (std::getline(std::cin, line)) { std::size_t c = line.find(','); if (c == std::string::npos) continue; px.push_back(std::stod(line.substr(c + 1))); if (px.back() > top) top = px.back(); }
    double worst = 0; bool seen = false;
    for (double p : px) { if (p == top) seen = true; if (seen && (top - p) / top > worst) worst = (top - p) / top; }
    if (!seen) worst = 0;
    double peak = 0, w2 = 0; for (double p : px) { if (p > peak) peak = p; }
    for (double p : px) { double f = (peak - p) / peak; if (f > w2 && p != px.front()) w2 = f; }
    std::cout << "Max drawdown: " << std::fixed << std::setprecision(2) << w2 * 100 << "%\\n";
}
''', 'test-4')
P = 'items.2.widget'
grade(L, 'homework-1.2 <= on the buy edge -> test-4', F, P, sol(F, P).replace('price < average - band', 'price <= average - band'), 'test-4')
grade(L, 'homework-1.2 >= on the sell edge -> test-5', F, P, sol(F, P).replace('price > average + band', 'price >= average + band'), 'test-5')
P = 'items.3.widget'
grade(L, 'homework-1.3 int total -> test-3', F, P, sol(F, P).replace('long long total = 0;', 'int total = 0;'), 'test-3')
SIGN = H + 'int main(){ std::vector<double> prices{1, 2};\n for (int i = 0; i < prices.size(); ++i) { std::cout << prices[i]; } }\n'
local(L, 'homework-1.4 g++ -Wall sign-compare text', has('g++', SIGN, ['-Wall'], "warning: comparison of integer expressions of different signedness: 'int' and 'std::vector<double>::size_type'", rc=0))
PORT = H + '''int main(){ std::vector<int> fills; int x; while (std::cin >> x) fills.push_back(x); int n_fills = fills.size() ? (int)fills.size() : 1;
int total_qty = 0;
for (int q : fills) {
    total_qty += q;
}
double avg = total_qty / n_fills;
std::cout << total_qty << ' ' << std::fixed << avg << '\\n'; }
'''
PORT2 = 'int f(int total_qty, int n_fills, const int* fills, int n){\nfor (int i = 0; i < n; ++i) { int q = fills[i];\n    total_qty += q;\n}\ndouble avg = total_qty / n_fills;\nreturn avg > 1; }\nint main(){}\n'
local(L, 'homework-1.6 g++ prints nothing with -Wall -Wextra -Wconversion', has('g++', PORT2, ['-Wall', '-Wextra', '-Wconversion'], rc=0, absent=['warning']))
local(L, 'homework-1.6 clang++ prints nothing with -Wall -Wextra -Wconversion', has('clang++', PORT2, ['-Wall', '-Wextra', '-Wconversion'], rc=0, absent=['warning']))
local(L, 'homework-1.6 -fsanitize=undefined reports the overflow at run time', has('g++', PORT, ['-fsanitize=undefined'], rc=0, run_has=['signed integer overflow', '-1294967296'], stdin='1500000000 1500000000\n'))
prog(L, 'homework-1.6 / review-1.4 app build prints -1294967296 and 2500000', PORT, out_is('-1294967296 -647483648.000000'), stdin='1500000000 1500000000\n')
prog(L, 'homework-1.6 4 fills totalling 10,000,002 give 2500000', PORT, out_is('10000002 2500000.000000'), stdin='2500000 2500000 2500000 2500002\n')


def tidy():
    d = tempfile.mkdtemp(dir=TMP)
    open(os.path.join(d, 'm.cpp'), 'w').write(PORT2)
    p = subprocess.run(['clang-tidy', '-checks=-*,bugprone-integer-division', 'm.cpp', '--', '-std=c++17'], cwd=d, capture_output=True, text=True)
    return 'bugprone-integer-division' in p.stdout, p.stdout[:200]


local(L, 'homework-1.6 clang-tidy bugprone-integer-division flags the division', tidy)



# ------------------------------------------------------------------ L2
L = 'L2'
H = '#include <iostream>\n#include <iomanip>\n#include <string>\n#include <vector>\n#include <cmath>\n#include <memory>\n'

# l5
prog(L, 'l5 s0, s2, s6, quiz0 outputs', H + '''void add_fee(std::vector<double> costs) { costs.push_back(1.50); }
void apply_fee(double& balance, double fee) { balance -= fee; }
void normalise(std::vector<double> w) { double sum = 0; for (double x : w) sum += x; for (double& x : w) x /= sum; }
int main() { std::vector<double> mine{250.00, 120.00}; add_fee(mine); std::cout << mine.size() << " ";
 double cash = 1000.00; apply_fee(cash, 2.50); std::cout << cash << " ";
 std::vector<double> w{2.0, 3.0, 5.0}; normalise(w); std::cout << w[0] << " ";
 int x = 5; int& r = x; int& r2 = r; r2 = 9; std::cout << x << "\\n"; }''', out_is('2 997.5 2 9'))
prog(L, 'l5.quiz1 clang: expects an lvalue for 1st argument', 'void apply_fee(double& balance, double fee) {\n    balance -= fee;\n}\n\nint main() {\n    apply_fee(100.0, 2.50);\n}\n', no_compile('expects an lvalue for 1st argument'))
F = 'l5-value-or-reference'
grade(L, 'l5.s7 starter (by value) -> test-1', F, 'screens.7.widget', at(F, 'screens.7.widget')['starter'], 'test-1')

# l6
prog(L, 'l6.s0 clang message and positions', 'int main() {\n    const double tick = 0.01;\n    tick = 0.05;\n}\n', no_compile("main.cpp:3:10: error: cannot assign to variable 'tick' with const-qualified type 'const double'", "main.cpp:2:18: note: variable 'tick' declared const here"))
prog(L, 'l6.s1 only line 4 is rejected, with the quoted text', 'double with_fee(const double& px, double fee) {\n    double out = px;\n    out += fee;\n    px += fee;\n    fee = 0;\n    return out;\n}\nint main(){}\n',
     lambda r: (r.get('ok') is False and "main.cpp:4:8: error: cannot assign to variable 'px' with const-qualified type 'const double &'" in r['diag'] and '1 error generated' in r['diag'], r['diag'][:200]))
MEAN = '#include <vector>\ndouble mean(std::vector<double>& v);\nint main(){\nstd::vector<double> prices{101.5, 99.0};\nconst std::vector<double> fixed{100.0, 100.5};\n%s\n}\n'
prog(L, 'l6.s2 mean(prices) compiles (link aside)', MEAN.replace('double mean(std::vector<double>& v);', 'double mean(std::vector<double>& v) { return v[0]; }') % 'mean(prices);', lambda r: (bool(r.get('ok')), str(r.get('diag'))[:200]))
prog(L, 'l6.s2 mean({101.5, 99.0}): clang says expects an lvalue', MEAN % 'mean({101.5, 99.0});', no_compile('expects an lvalue'))
prog(L, 'l6.s2 mean(fixed): clang says would lose const qualifier', MEAN % 'mean(fixed);', no_compile('would lose const qualifier'))
Q = 'struct Quote {\n    double bid, ask;\n    double mid() const { return (bid + ask) / 2; }\n    void widen(double by) { bid -= by; ask += by; }\n};\nint main(){\nconst Quote q{99.98, 100.02};\n%s\n}\n'
prog(L, 'l6.s3 q.mid() and q.bid compile', Q % 'double m = q.mid(); double b = q.bid; return m > b;', lambda r: (bool(r.get('ok')), str(r.get('diag'))[:200]))
prog(L, 'l6.s3 q.widen: function is not marked const', Q % 'q.widen(0.01);', no_compile('function is not marked const'))
prog(L, 'l6.s3 q.ask = 100.05 is rejected', Q % 'q.ask = 100.05;', no_compile('error'))
CE = 'constexpr int lot_size = 100;\nconstexpr double tick = 0.01;\nconstexpr double min_fee = tick * lot_size;\ndouble read_tick();\n%s\nconst double start_tick = read_tick();\ndouble read_tick() { return 0.01; }\nint main(){ return min_fee > start_tick; }\n'
prog(L, 'l6.s5 line 5 rejected with the quoted text', CE % 'constexpr double live_tick = read_tick();', lambda r: (r.get('ok') is False and "main.cpp:5:18: error: constexpr variable 'live_tick' must be initialized by a constant expression" in r['diag'] and '1 error generated' in r['diag'], r['diag'][:200]))
prog(L, 'l6.s5 the other five lines compile', CE % '', lambda r: (bool(r.get('ok')), str(r.get('diag'))[:200]))
prog(L, 'l6.s6 view sees the change: 99', H + 'int main(){ std::vector<double> px{100.0, 101.0}; const std::vector<double>& view = px; px[0] = 99.0; std::cout << view[0] << "\\n"; }', out_is('99'))
PT = 'int main(){ double x = 1, y = 2;\n%s\nreturn 0; }\n'
prog(L, 'l6.s10 const double* p: *p = 3 rejected', PT % 'const double* p = &x; *p = 3;', no_compile('error'))
prog(L, 'l6.s10 const double* p: p = &y fine', PT % 'const double* p = &x; p = &y; (void)p;', lambda r: (bool(r.get('ok')), str(r.get('diag'))[:200]))
prog(L, 'l6.s10 double* const p: p = &y rejected with the quoted text', PT % 'double* const p = &x; p = &y;', no_compile("cannot assign to variable 'p' with const-qualified type 'double *const'"))
prog(L, 'l6.s10 double* const p: *p = 3 fine', PT % 'double* const p = &x; *p = 3;', lambda r: (bool(r.get('ok')), str(r.get('diag'))[:200]))
prog(L, 'l6.quiz2 clang text for p.qty = 0', 'struct Position { int qty; };\n\nvoid report(const Position& p) {\n    p.qty = 0;\n}\nint main(){}\n', no_compile("cannot assign to variable 'p' with const-qualified type 'const Position &'"))
prog(L, 'l6.quiz3 const& binds a braced temporary', H + 'double total(const std::vector<double>& v) { double t = 0; for (double x : v) t += x; return t; }\nint main(){ std::cout << total({1.0, 2.0}) << "\\n"; }', out_is('3'))
F = 'l6-const'
grade(L, 'l6.s7 starter -> compile, message as on the canvas', F, 'screens.7.widget', at(F, 'screens.7.widget')['starter'], 'compile', lambda r: ("main.cpp:5:15: error: cannot assign to return value because function 'operator[]' returns a const value" in r['diag'], r['diag'][:160]))

# l7
F = 'l7-addresses'
P = 'screens.3.widget'
grade(L, 'l7.s3 no null guard -> test-5', F, P, 'void bump(int* p) {\n    *p += 1;\n}\n', 'test-5', lambda r: (True, 'row5: actual=' + str(r['rows'][4]['actual']) + ' error=' + str(r['rows'][4]['error'])[:160]))
P = 'screens.4.widget'
grade(L, 'l7.s4 best starts at 0 -> test-2 (0)', F, P, 'double max_via_pointer(const double* begin, const double* end) {\n double best = 0; for (const double* p = begin; p != end; ++p) if (*p > best) best = *p; return best; }\n', 'test-2', lambda r: (r['rows'][1]['actual'] == '0', 'actual=' + str(r['rows'][1]['actual'])))
grade(L, 'l7.s4 loop reads *end (p <= end), best from *begin', F, P, 'double max_via_pointer(const double* begin, const double* end) {\n if (begin == end) return 0; double best = *begin; for (const double* p = begin; p <= end; ++p) if (*p > best) best = *p; return best; }\n', 'test-2', lambda r: (True, 'actual=' + str(r['rows'][1]['actual'])))
prog(L, 'l7.s0, s7, quiz1 outputs', H + 'int main(){ int qty = 300; int* p = &qty; *p = 500; std::cout << qty << " "; double a = 5.0, b = 5.0; std::cout << (&a == &b) << " "; int x = 1; int* q = &x; int** pp = &q; **pp = 7; std::cout << x << "\\n"; }', out_is('500 0 7'))
prog(L, 'l7.s5 app build printed 101.25 from the dead bid', H + 'int main(){\ndouble* p = nullptr;\n{\n    double bid = 101.25;\n    p = &bid;\n}\nstd::cout << *p << "\\n";\n}\n', out_is('101.25'))
prog(L, 'l7.quiz0 app build: null read printed 0', H + 'int main(){\nint* p = nullptr;\nstd::cout << *p << "\\n";\n}\n', out_is('0'))
prog(L, 'l7.quiz2 clang warns and builds', 'double* best_bid() {\n    double x = 101.25;\n    return &x;\n}\nint main(){ return best_bid() == nullptr; }\n', lambda r: (bool(r.get('ok')) and "warning: address of stack memory associated with local variable 'x' returned" in r['diag'], r['diag'][:200]))
SCOPE = '#include <iostream>\nint main() {\n    double* p = nullptr;\n    {\n        double bid = 101.25;\n        p = &bid;\n    }\n    std::cout << *p << "\\n";\n}\n'
local(L, 'l7.s6 g++ ASan: stack-use-after-scope, bid (line 5), scope.cpp:8', has('g++', SCOPE, ['-g', '-fsanitize=address'], rc=0, run_has=['AddressSanitizer: stack-use-after-scope', 'READ of size 8', "'bid' (line 5)", 'scope.cpp:8'], name='scope.cpp'))
local(L, 'l7.quiz0 g++ build: null read dies with a segmentation fault', has('g++', '#include <iostream>\nint main(){ int* volatile p = nullptr; std::cout << *p << "\\n"; }\n', [], rc=0, run_has=['--rc -11--']))
local(L, 'l7.quiz0 ASan: SEGV on unknown address 0x000000000000', has('g++', '#include <iostream>\nint main(){ int* volatile p = nullptr; std::cout << *p << "\\n"; }\n', ['-g', '-fsanitize=address'], rc=0, run_has=['SEGV on unknown address 0x000000000000']))

# l8
prog(L, 'l8.s0 program A stops with memory access out of bounds', H + 'int main() {\n    double prices[2000000];\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";\n}\n', traps('out of bounds'))
prog(L, 'l8.s0 program B prints 101; vector object is 12 bytes', H + 'int main() {\n    std::vector<double> prices(2000000);\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << " " << sizeof(prices) << "\\n";\n}\n', out_is('101 12'))
local(L, 'l8.s0 g++ program A: segmentation fault; vector object is 24 bytes', has('g++', H + 'int main() {\n    std::cout << sizeof(std::vector<double>) << std::endl; double prices[2000000];\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";\n}\n', [], rc=0, run_has=['--rc -11--']))
prog(L, 'l8.s1/s2 frames and heap double', H + 'double mid(double bid, double ask) { return (bid + ask) / 2; }\ndouble value(int qty, double bid, double ask) { double m = mid(bid, ask); return qty * m; }\ndouble* make_price() { double* p = new double(101.5); return p; }\nint main(){ std::cout << value(300, 99.5, 100.5) << " "; double* q = make_price(); std::cout << *q << "\\n"; delete q; }', out_is('30000 101.5'))
DEL = '#include <iostream>\nint main() {\ndouble* px = new double[1000];\npx[0] = 1; std::cout << "";\ndelete px;\n}\n'
prog(L, 'l8.s5 app: delete on new[] runs, exit 0, clang warns', DEL, lambda r: (bool(r.get('ok')) and r.get('code') == 0 and not r.get('trap') and r.get('out') == '' and "warning: 'delete' applied to a pointer that was allocated with 'new[]'; did you mean 'delete[]'?" in r['diag'], f"code={r.get('code')} trap={r.get('trap')} diag={r.get('diag','')[:160]!r}"))
local(L, 'l8.s5 ASan: alloc-dealloc-mismatch (operator new [] vs operator delete)', has('g++', DEL, ['-g', '-fsanitize=address'], rc=0, run_has=['AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)']))
LEAK = 'double sum_prices(int n) {\n    double* prices = new double[n];\n    double total = 0;\n    for (int i = 0; i < n; ++i) {\n        prices[i] = 100 + i;\n        total += prices[i];\n    }\n    return total;\n}\nint main() { return sum_prices(1000) < 0; }\n'
local(L, 'l8.s4 LeakSanitizer report: 8000 bytes in 1 object, sum_prices at leak.cpp:2', has('g++', LEAK, ['-g', '-fsanitize=address'], rc=0, run_has=['LeakSanitizer: detected memory leaks', 'Direct leak of 8000 byte(s) in 1 object(s)', 'operator new[](unsigned long)', 'in sum_prices(int)', 'leak.cpp:2', 'SUMMARY: AddressSanitizer: 8000 byte(s) leaked in 1 allocation(s).'], name='leak.cpp'))
F = 'l8-stack-and-heap'
P = 'screens.6.widget'
grade(L, 'l8.s6 right output but delete px -> test-1', F, P, sol(F, P).replace('delete[] px;', 'delete px;'), 'test-1', lambda r: ('300.75' in r['rows'][0]['stdout'], 'stdout=' + r['rows'][0]['stdout'] + ' error=' + str(r['rows'][0]['error'])[:200]))
prog(L, 'l8.s8 recursion 10,000,000 deep: call stack exhausted', H + '__attribute__((noinline)) double f(int n) { volatile double x = n; if (n == 0) return x; return f(n - 1) + x; }\nint main(){ std::cout << f(10000000) << "\\n"; }', traps('call stack exhausted'))
STK = '#include <iostream>\nint main() {\ndouble price = 101.25;\ndouble* p = &price;\ndelete p;\nstd::cout << "end\\n";\n}\n'
prog(L, 'l8.quiz0 app: delete of a stack address ran silently', STK, lambda r: (bool(r.get('ok')) and r.get('code') == 0 and r.get('out') == 'end\n', f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')} diag={r.get('diag','')[:120]!r}"))
local(L, 'l8.quiz0 g++ warns called on unallocated object; run aborts with free(): invalid pointer', has('g++', STK, [], "called on unallocated object 'price'", rc=0, run_has=['free(): invalid pointer']))
DBL = '#include <iostream>\nint main() {\ndouble* volatile r = new double(1.0);\ndouble* r2 = r;\ndelete r;\ndelete r2;\nstd::cout << "end\\n";\n}\n'
prog(L, 'l8 summary / review-2.3 / homework-2.5 app: double delete ran silently', DBL, lambda r: (bool(r.get('ok')) and r.get('code') == 0 and r.get('out') == 'end\n', f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')} err={str(r.get('err'))[:100]}"))
prog(L, 'homework-2.5 app: double delete exactly as written ran to the end', '#include <iostream>\nint main() {\ndouble* r = new double(1.0); delete r; delete r;\nstd::cout << "end\\n";\n}\n', lambda r: (bool(r.get('ok')) and r.get('code') == 0 and r.get('out') == 'end\n', f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')}"))
local(L, 'review-2.3 ASan reports double-free', has('g++', DBL, ['-g', '-fsanitize=address'], rc=0, run_has=['attempting double-free']))
prog(L, 'l8.quiz1 new double[0] is non-null', H + 'int main(){ volatile int n = 0; double* p = new double[n]; std::cout << (p != nullptr) << "\\n"; delete[] p; }', out_is('1'))

# l9
POS = H + 'struct Position {\n    std::string sym; int qty = 0;\n    Position(std::string s) : sym(s) { std::cout << "open " << sym << "\\n"; }\n    Position(std::string s, int q) : sym(s), qty(q) { std::cout << "open " << sym << "\\n"; }\n    ~Position() { std::cout << "close " << sym << "\\n"; }\n};\n'
prog(L, 'l9.s0 open, trading, close, done', POS + 'void trade() {\n    Position p("VOD");\n    std::cout << "trading\\n";\n}\nint main() {\n    trade();\n    std::cout << "done\\n";\n}\n', out_is('open VOD\ntrading\nclose VOD\ndone'))
prog(L, 'l9.s9 five lines in the stated order', POS + 'void hold(std::unique_ptr<Position> p) {\n    std::cout << "hold " << p->qty << "\\n";\n}\nint main() {\n    auto p = std::make_unique<Position>("VOD", 100);\n    std::cout << "opened\\n";\n    hold(std::move(p));\n    std::cout << (p == nullptr) << " after hold\\n";\n}\n', out_is('open VOD\nopened\nhold 100\nclose VOD\n1 after hold'))
prog(L, 'review-2.5 open AZN, close AZN, end', POS + 'int main(){\n{\n    std::vector<std::unique_ptr<Position>> book;\n    book.push_back(std::make_unique<Position>("AZN", 10));\n}\nstd::cout << "end\\n";\n}\n', out_is('open AZN\nclose AZN\nend'))
UP = '#include <memory>\nstruct Order { int qty; };\nvoid book_order(std::unique_ptr<Order> o);\nint main() {\n    auto a = std::make_unique<Order>(Order{100});\n    %s\n}\nvoid book_order(std::unique_ptr<Order> o) {}\n'
prog(L, 'l9.s4 copy: the two quoted clang lines, at 6:16', UP % 'book_order(a);', no_compile("main.cpp:6:16: error: call to implicitly-deleted copy constructor of 'std::unique_ptr<Order>'", "note: copy constructor is implicitly deleted because 'unique_ptr<Order>' has a user-declared move constructor"))
prog(L, 'l9.s4 std::move compiles', '#include <utility>\n' + UP % 'book_order(std::move(a)); return a ? 1 : 0;', lambda r: (bool(r.get('ok')) and r.get('code') == 0, str(r.get('diag'))[:200] + f" code={r.get('code')}"))
prog(L, 'l9.s4 a.get() does not compile', UP % 'book_order(a.get());', no_compile('error'))
prog(L, 'l9.s4 copy into b does not compile', UP % 'std::unique_ptr<Order> b = a; book_order(b);', no_compile('implicitly-deleted copy constructor'))
prog(L, 'l9.s4 *a does not compile', UP % 'book_order(*a);', no_compile('error'))
prog(L, 'l9.s3 hint: delete on a unique_ptr does not compile', UP % 'delete a;', no_compile('error'))
prog(L, 'l9.s6 use_count printed 1, 3, 1', H + 'struct Order {};\nint main(){ auto a = std::make_shared<Order>(); std::cout << a.use_count() << " ";\n{ auto b = a; auto c = b; std::cout << a.use_count() << " "; }\nstd::cout << a.use_count() << "\\n"; }', out_is('1 3 1'))
CYC = H + 'struct Node {\n    std::shared_ptr<Node> other;\n    ~Node() { std::cout << "freed\\n"; }\n};\nint main() {\n    {\n        auto a = std::make_shared<Node>();\n        auto b = std::make_shared<Node>();\n        a->other = b;\n        b->other = a;\n    }\n    std::cout << "end of main\\n";\n}\n'
prog(L, 'l9.s7 cycle prints end of main only', CYC, out_is('end of main'))
local(L, 'l9.s7 LeakSanitizer: 64 byte(s) leaked in 2 allocation(s)', has('g++', CYC, ['-g', '-fsanitize=address'], rc=0, run_has=['64 byte(s) leaked in 2 allocation(s)']))
prog(L, 'l9.quiz0 prints 1 101.5; quiz1 prints 0 101.5', H + 'int main(){ auto a = std::make_unique<double>(101.5); auto b = std::move(a); std::cout << (a == nullptr) << " " << *b << "\\n";\n auto px = std::make_unique<double[]>(3); px[2] = 101.5; std::cout << px[0] << " " << px[2] << "\\n"; }', out_is('1 101.5\n0 101.5'))
prog(L, 'l9.quiz3 push_back(o) error text', '#include <memory>\n#include <vector>\nstruct Order {};\nint main(){ std::vector<std::unique_ptr<Order>> book; auto o = std::make_unique<Order>(); book.push_back(o); }\n', no_compile('call to implicitly-deleted copy constructor'))
F = 'l9-owning-memory'
grade(L, 'l9.s3 starter -> test-3', F, 'screens.3.widget', at(F, 'screens.3.widget')['starter'], 'test-3')
P = 'screens.5.widget'
grade(L, 'l9.s5 always make_unique -> test-4', F, P, sol(F, P).replace('if (qty == 0) return nullptr;', ''), 'test-4')

# review-2, homework-2
prog(L, 'review-2.0 by-value swap prints 99.5 100.5', H + 'void swap_px(double a, double b) { double t = a; a = b; b = t; }\nint main(){ double bid = 99.5, ask = 100.5; swap_px(bid, ask); std::cout << bid << " " << ask << "\\n"; }', out_is('99.5 100.5'))
prog(L, 'review-2.3 app: reading *f() of a dead local ran silently', H + 'double* f() { double x = 1.0; return &x; }\nint main(){ double y = *f(); std::cout << "end\\n"; (void)y; }', lambda r: (bool(r.get('ok')) and r.get('code') == 0 and r.get('out') == 'end\n', f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')}"))
prog(L, 'review-2.3 / homework-2.5 app: v.at(5) stops with an error', H + 'int main(){ std::vector<double> v(3); double y = v.at(5); std::cout << y << "end\\n"; }', traps(''))
F = 'homework-2'
P = 'items.0.widget'
grade(L, 'homework-2.0 for (Position p : book) -> test-1', F, P, sol(F, P).replace('for (Position& p : book)', 'for (Position p : book)'), 'test-1')
P = 'items.1.widget'
grade(L, 'homework-2.1 int total quantity -> test-4', F, P, sol(F, P).replace('long long total_qty(const std::vector<Order>& orders) {\n    long long q = 0;', 'long long total_qty(const std::vector<Order>& orders) {\n    int q = 0;'), 'test-4')
grade(L, 'homework-2.1 reads qty into an int -> test-4', F, P, sol(F, P).replace('Order o;\n        std::cin >> o.qty >> o.px;', 'Order o; int q;\n        std::cin >> q >> o.px; o.qty = q;'), 'test-4')
prog(L, 'homework-2.2 prints 7.5', H + 'double payoff(double s, double k) { return s > k ? s - k : 0; }\ndouble price_option(double s, double k) { double up = payoff(s * 1.1, k); double down = payoff(s * 0.9, k); return 0.5 * up + 0.5 * down; }\nint main(){ std::cout << price_option(100, 95) << "\\n"; }', out_is('7.5'))
prog(L, 'homework-2.5 app: int x = *p with p null gave 0', H + 'int main(){\nint* p = nullptr; int x = *p;\nstd::cout << x << "\\n";\n}\n', out_is('0'))
prog(L, 'homework-2.5 app: delete on new double[4] ran to the end', H + 'int main(){\ndouble* q = new double[4]; delete q;\nstd::cout << "end\\n";\n}\n', lambda r: (bool(r.get('ok')) and r.get('code') == 0 and r.get('out') == 'end\n', f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')}"))
UAF = H + 'int main(){\nstd::vector<double> px{100.0, 101.0, 102.0};\nconst double& first = px[0];\npx.push_back(103.0);\nstd::cout << first << "\\n";\n}\n'
prog(L, 'homework-2.6 app test run printed about 2.9e-306', UAF, lambda r: (bool(r.get('ok')) and r.get('out', '').strip().startswith('2.9') and r.get('out', '').strip().endswith('e-306'), f"out={r.get('out')!r} trap={r.get('trap')}"))
local(L, 'homework-2.6 ASan: heap-use-after-free', has('g++', UAF, ['-g', '-fsanitize=address'], rc=0, run_has=['heap-use-after-free']))
prog(L, 'homework-2.7 app: <= loop stops with vector[] index out of bounds', H + 'struct Trade { std::string sym; int qty; double px; };\ndouble total_notional(std::vector<Trade> trades) { double sum = 0; for (std::size_t i = 0; i <= trades.size(); ++i) sum += trades[i].qty * trades[i].px; return sum; }\nint main(){ std::cout << total_notional({{"VOD", 1, 2.0}}) << "\\n"; }', traps('vector[] index out of bounds'))
prog(L, 'homework-2.7 clang warning for return &best', H + 'struct Trade { std::string sym; int qty; double px; };\nTrade* best_trade(std::vector<Trade>& trades) { Trade best = trades[0]; for (Trade t : trades) if (t.qty * t.px > best.qty * best.px) best = t; return &best; }\nint main(){ std::vector<Trade> t{{"VOD", 1, 2.0}}; return best_trade(t) == nullptr; }', lambda r: ("address of stack memory associated with local variable 'best' returned" in r.get('diag', ''), r.get('diag', '')[:200]))
MODEL = '#include <optional>\n' + H + '''struct Trade { std::string sym; int qty; double px; };
struct Pricer {};
double total_notional(const std::vector<Trade>& trades) {
    double sum = 0;
    for (const Trade& t : trades) sum += t.qty * t.px;
    return sum;
}

std::optional<Trade> best_trade(const std::vector<Trade>& trades) {
    if (trades.empty()) return std::nullopt;
    Trade best = trades[0];
    for (const Trade& t : trades)
        if (t.qty * t.px > best.qty * best.px) best = t;
    return best;
}

void add_fee(Trade& t, double fee) {
    t.px += fee;
}

std::unique_ptr<Pricer> make_pricer() {
    return std::make_unique<Pricer>();
}
int main(){ std::vector<Trade> t{{"VOD", 100, 0.72}, {"AZN", 10, 105.0}}; add_fee(t[0], 0.01); auto p = make_pricer(); std::cout << total_notional(t) << " " << best_trade(t)->sym << " " << best_trade({}).has_value() << (p != nullptr) << "\\n"; }'''
prog(L, 'homework-2.7 model answer (e) compiles and runs', MODEL, out_is('1123 AZN 01'))



# ------------------------------------------------------------------ L3
L = 'L3'
H = '#include <iostream>\n#include <iomanip>\n#include <string>\n#include <vector>\n#include <cmath>\n#include <memory>\n#include <stdexcept>\n#include <algorithm>\n#include <tuple>\n'
okc = lambda r: (bool(r.get('ok')), str(r.get('diag'))[:240])

# l10
QC = '''class Quote {
public:
    Quote(double bid, double ask) : bid_(bid), ask_(ask) {}
    double mid() const { return (bid_ + ask_) / 2; }
private:
    double bid_;
    double ask_;
};

int main() {
    Quote q(100.2, 100.4);
    q.bid_ = 100.6;
}
'''
prog(L, 'l10.s2 clang: private member, both positions, 1 error', QC, no_compile("main.cpp:12:7: error: 'bid_' is a private member of 'Quote'", "main.cpp:6:12: note: declared private here", '1 error generated.'))
prog(L, 'l10.s0, s7, quiz0 print -0.2', H + '''struct Q0 { double bid; double ask; };
class Quote { public: Quote(double bid, double ask) : bid_(bid), ask_(ask) { if (bid_ >= ask_) std::abort(); }
 void set_bid(double b) { bid_ = b; } double& bid() { return bid_; } double spread() const { return ask_ - bid_; } private: double bid_; double ask_; };
int main(){ Q0 q{100.2, 100.4}; q.bid = 100.6; std::cout << q.ask - q.bid << '\\n';
 Quote a(100.2, 100.4); a.set_bid(100.6); std::cout << a.spread() << '\\n';
 Quote b(100.2, 100.4); b.bid() = 100.6; std::cout << b.spread() << '\\n'; }''', out_is('-0.2\n-0.2\n-0.2'))
F = 'l10-invariants'
P = 'screens.3.widget'
s = sol(F, P)
CHK = '        if (bid_ >= ask_) throw std::invalid_argument("bid must be below ask");\n'
assert CHK in s
grade(L, 'l10.s3 no check -> test-4', F, P, s.replace(CHK, ''), 'test-4')
grade(L, 'l10.s3 > instead of >= -> test-5', F, P, s.replace('bid_ >= ask_', 'bid_ > ask_'), 'test-5')
grade(L, 'l10.s3 abort() also passes', F, P, s.replace('throw std::invalid_argument("bid must be below ask");', 'std::abort();').replace('#include <stdexcept>', '#include <cstdlib>'), None)
grade(L, 'l10.s3 spread not const -> compile, not marked const', F, P, s.replace('double spread() const', 'double spread()'), 'compile', lambda r: ('not marked const' in r['diag'], r['diag'][:200]))
grade(L, 'l10.s3 mid missing -> compile, names mid', F, P, s.replace('    double mid() const { return (bid_ + ask_) / 2; }\n', ''), 'compile', lambda r: ("'mid'" in r['diag'], r['diag'][:200]))
P = 'screens.5.widget'
s = sol(F, P)
BUY = '        avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty);\n        qty_ += qty;\n'
assert BUY in s
grade(L, 'l10.s5 adds the shares first, divides by the new qty_ -> test-2', F, P, s.replace(BUY, '        qty_ += qty;\n        avg_ = (qty_ * avg_ + qty * px) / qty_;\n'), 'test-2')
grade(L, 'l10.s5 average is the last price -> test-2', F, P, s.replace(BUY, '        avg_ = px;\n        qty_ += qty;\n'), 'test-2')
grade(L, 'l10.s5 sale resets the average -> test-4', F, P, s.replace('        if (qty_ == 0) avg_ = 0.0;\n', '        avg_ = 0.0;\n'), 'test-4')
grade(L, 'l10.s5 no reset when flat -> test-6', F, P, s.replace('        if (qty_ == 0) avg_ = 0.0;\n', ''), 'test-6')
grade(L, 'l10.s5 oversell not refused -> test-8', F, P, s.replace('qty <= 0 || qty > qty_', 'qty <= 0'), 'test-8')
grade(L, 'l10.s5 buy of 0 not refused -> test-9', F, P, s.replace('        if (qty <= 0) throw std::invalid_argument("buy a positive quantity");\n', ''), 'test-9')
prog(L, 'l10.s5 unchecked buy(0, 10.0) on a flat position gives nan', H + 'int main(){ volatile int qty_ = 0, qty = 0; double avg_ = 0.0, px = 10.0; avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty); std::cout << avg_ << "\\n"; }', lambda r: ('nan' in r.get('out', ''), r.get('out', '')))
LIM = '''class Limit {
public:
    %s
private:
    const double max_;
};

int main() {
    Limit l(5e6);
}
'''
LIM0 = LIM % 'Limit(double m) {\n        max_ = m;\n    }'
prog(L, 'l10.s6 clang: both errors, the note, 2 errors', LIM0, no_compile("main.cpp:3:5: error: constructor for 'Limit' must explicitly initialize the const member 'max_'", 'main.cpp:7:18: note: declared here', "main.cpp:4:14: error: cannot assign to non-static data member 'max_' with const-qualified type 'const double'", '2 errors generated.'))
prog(L, 'l10.s6 list version compiles', LIM % 'Limit(double m) : max_(m) {}', okc)
prog(L, 'l10.s6 this->max_ = m does not compile', LIM % 'Limit(double m) { this->max_ = m; }', no_compile('error'))
prog(L, 'l10.s6 local const: the first error remains', LIM % 'Limit(double m) { const double max_ = m; }', no_compile("must explicitly initialize the const member 'max_'"))
prog(L, 'l10 summary: a const member can also take a default member initialiser', 'class Limit { public: Limit() {} double max() const { return max_; } private: const double max_ = 5e6; };\nint main(){ Limit l; return l.max() > 0 ? 0 : 1; }', okc)
P = 'screens.9.widget'
s = sol(F, P)
grade(L, 'l10.s9 never sets Filled -> test-4', F, P, s.replace('        if (filled_ == qty_) state_ = State::Filled;\n', ''), 'test-4')
A = 'void fill(int q) {\n        if (state_ != State::New) throw std::logic_error("order is not live");\n'
assert A in s
grade(L, 'l10.s9 fill does not check the state -> test-7', F, P, s.replace(A, 'void fill(int q) {\n'), 'test-7')
grade(L, 'l10.s9 fill past the size not refused -> test-8', F, P, s.replace('q <= 0 || filled_ + q > qty_', 'q <= 0'), 'test-8')
A = 'void cancel() {\n        if (state_ != State::New) throw std::logic_error("order is not live");\n'
assert A in s
grade(L, 'l10.s9 cancel does not check the state -> test-9', F, P, s.replace(A, 'void cancel() {\n'), 'test-9')
QZ = H + 'class Quote { public: Quote(double b, double a) : bid_(b), ask_(a) {} %s bid() { return bid_; } double spread() %s { return ask_ - bid_; } private: double bid_, ask_; };\n%s'
prog(L, 'l10.quiz0 returning double: q.bid() = 100.6 does not compile', QZ % ('double', 'const', 'int main(){ Quote q(100.2, 100.4); q.bid() = 100.6; }'), no_compile('error'))
prog(L, 'l10.quiz0 returning const double&: does not compile', QZ % ('const double&', 'const', 'int main(){ Quote q(100.2, 100.4); q.bid() = 100.6; }'), no_compile('error'))
prog(L, 'l10.quiz2 clang text for a non-const spread', QZ % ('double', '', 'double width(const Quote& q) {\n    return q.spread();\n}\nint main(){}'), no_compile("'this' argument to member function 'spread' has type 'const Quote', but function is not marked const"))
local(L, 'l10.quiz1 Python prints -0.19999999999998863', lambda: (repr(100.4 - 100.6) == '-0.19999999999998863', repr(100.4 - 100.6)))

# l11
LOG = H + 'struct Logger {\n    std::string name;\n    Logger(std::string n) : name(n) {\n        std::cout << "open " << name << \'\\n\';\n    }\n    ~Logger() { std::cout << "close " << name << \'\\n\'; }\n};\n'
prog(L, 'l11.s0 order', LOG + 'int main() {\n    Logger a("a");\n    Logger b("b");\n    std::cout << "work\\n";\n}\n', out_is('open a\nopen b\nwork\nclose b\nclose a'))
prog(L, 'l11.s2 order', LOG + 'int main() {\n    Logger a("a");\n    {\n        Logger b("b");\n        std::cout << "work\\n";\n    }\n    Logger c("c");\n}\n', out_is('open a\nopen b\nwork\nclose b\nopen c\nclose c\nclose a'))
prog(L, 'l11.s5 copy prints close a twice', LOG + 'int main() {\n    Logger a("a");\n    Logger b = a;\n}\n', out_is('open a\nclose a\nclose a'))
prog(L, 'l11.quiz0 temporary', LOG + 'int main() {\n    Logger("tmp");\n    std::cout << "next\\n";\n}\n', out_is('open tmp\nclose tmp\nnext'))
prog(L, 'l11.quiz3 declaration order', LOG + 'class Desk {\n    Logger risk_;\n    Logger feed_;\npublic:\n    Desk() : feed_("feed"), risk_("risk") {}\n};\nint main() {\n    Desk d;\n}\n', out_is('open risk\nopen feed\nclose feed\nclose risk'))
prog(L, 'review-3.1 order', LOG + 'class Desk {\npublic:\n    Desk() : feed_("feed"), risk_("risk") {\n        std::cout << "desk open\\n";\n    }\n    ~Desk() { std::cout << "desk close\\n"; }\nprivate:\n    Logger feed_;\n    Logger risk_;\n};\nint main() {\n    Desk d;\n}\n', out_is('open feed\nopen risk\ndesk open\ndesk close\nclose risk\nclose feed'))
prog(L, 'homework-3.0 order', LOG + 'int main() {\n    Logger a("a");\n    {\n        Logger b("b");\n        Logger("tmp");\n        std::cout << "work\\n";\n    }\n    std::cout << "end\\n";\n}\n', out_is('open a\nopen b\nopen tmp\nclose tmp\nwork\nclose b\nend\nclose a'))
WIN = '''#include <vector>

class Window {
public:
    Window(int n) : n_(n), data_(n_, 0.0) {}
private:
    std::vector<double> data_;
    int n_;
};

int main() {
    Window w(20);
}
'''
prog(L, 'l11.s4 clang -Wall: both warnings with positions, 2 warnings', WIN.replace('Window w(20);', 'return 0;'), lambda r: (all(n in r.get('diag', '') for n in ["main.cpp:5:21: warning: field 'n_' will be initialized after field 'data_' [-Wreorder-ctor]", "main.cpp:5:34: warning: field 'n_' is uninitialized when used here [-Wuninitialized]", '2 warnings generated.']), r.get('diag', '')[:400]), flags=['-Wall'])
BUF = H + '''struct Buffer { std::vector<double> d;
 Buffer(int n, double x) : d(n, x) { std::cout << "ctor "; }
 Buffer(const Buffer& o) : d(o.d) { std::cout << "copy-ctor "; }
 Buffer(Buffer&& o) noexcept : d(std::move(o.d)) { std::cout << "move-ctor "; }
 Buffer& operator=(const Buffer& o) { d = o.d; std::cout << "copy-assign "; return *this; }
 Buffer& operator=(Buffer&& o) noexcept { d = std::move(o.d); std::cout << "move-assign "; return *this; } };
int main(){
Buffer a(3, 1.5);
Buffer b = a;
Buffer c(a);
b = a;
Buffer d = std::move(a);
c = std::move(b);
std::cout << "\\n"; }'''
prog(L, 'l11.s6 which special member runs on each of the six lines', BUF, out_is('ctor copy-ctor copy-ctor copy-assign move-ctor move-assign'))
F = 'l11-creation-destruction'
P = 'screens.7.widget'
s = sol(F, P)
FOUR = '    Buffer(const Buffer&) = default;\n    Buffer(Buffer&&) = default;\n    Buffer& operator=(const Buffer&) = default;\n    Buffer& operator=(Buffer&&) = default;\n'
assert FOUR in s
grade(L, 'l11.s7 only the copy constructor declared -> test-5', F, P, s.replace(FOUR, '    Buffer(const Buffer&) = default;\n'), 'test-5')
grade(L, 'l11.s7 copy and move constructors only -> test-9', F, P, s.replace(FOUR, '    Buffer(const Buffer&) = default;\n    Buffer(Buffer&&) = default;\n'), 'test-9')
grade(L, 'l11.s7 move assignment deleted -> test-10', F, P, s.replace('Buffer& operator=(Buffer&&) = default;', 'Buffer& operator=(Buffer&&) = delete;'), 'test-10')
grade(L, 'l11.s7 no move assignment declared -> test-12', F, P, s.replace('    Buffer& operator=(Buffer&&) = default;\n', ''), 'test-12')
grade(L, 'l11.s7 none of the four declared (rule of zero) passes', F, P, s.replace(FOUR, ''), None)
P = 'screens.3.widget'
s = sol(F, P)
A = '    Logger first(x);\n    {\n        Logger second(y);\n        std::cout << "work\\n";\n    }\n    Logger third(z);\n'
assert A in s
grade(L, 'l11.s3 no inner braces -> test-1', F, P, s.replace(A, '    Logger first(x);\n    Logger second(y);\n    std::cout << "work\\n";\n    Logger third(z);\n'), 'test-1')
P = 'screens.10.widget'
s = sol(F, P)
grade(L, 'l11.s10 move leaves the source open -> test-2', F, P, s.replace('        other.open_ = false;\n', ''), 'test-2')
grade(L, 'l11.s10 copy constructor defaulted beside a right move -> test-8', F, P, s.replace('Connection(const Connection&) = delete;', 'Connection(const Connection&) = default;'), 'test-8')
grade(L, 'l11.s10 destructor does nothing -> test-1', F, P, s.replace('        if (open_) disconnect(venue_);\n', ''), 'test-1')
grade(L, 'l11.s10 copy not mentioned at all, right move: still not copyable (passes test 8)', F, P, s.replace('    Connection(const Connection&) = delete;\n    Connection& operator=(const Connection&) = delete;\n', ''), None)
DD = 'class Prices {\npublic:\n    explicit Prices(int n) : data_(new double[n]) {}\n    ~Prices() { delete[] data_; }\nprivate:\n    double* data_;\n};\n\nint main() {\n    Prices a(100);\n    Prices b = a;\n}\n'
local(L, 'l11.s8 desk build: double delete[] crashes (abort)', has('g++', DD, [], rc=0, run_has=['double free', '--rc -6--']))
prog(L, 'l11.quiz1 const source is copied: prints 3', H + 'class Buffer { public: Buffer(int n, double x) : d(n, x) {} Buffer(const Buffer&) = default; Buffer(Buffer&&) = default; int size() const { return (int)d.size(); } private: std::vector<double> d; };\nint main(){\nconst Buffer a(3, 1.5);\nBuffer b = std::move(a);\nstd::cout << a.size() << \'\\n\'; }', out_is('3'))
prog(L, 'l11.quiz2 returned local: 0 copies', H + 'int copies = 0;\nstruct Lattice { std::vector<double> v; explicit Lattice(int n) : v(n) {} Lattice(const Lattice& o) : v(o.v) { ++copies; } Lattice(Lattice&& o) noexcept : v(std::move(o.v)) {} };\nLattice build(int steps) {\n    Lattice grid(steps);\n    grid.v[0] = 1;\n    return grid;\n}\nint main(){ Lattice g = build(500); std::cout << copies << " " << g.v.size() << "\\n"; }', out_is('0 500'))
PR = H + 'struct Lattice {};\nclass Pricer {\n    std::string name_;\n    std::unique_ptr<Lattice> grid_;\npublic:\n    explicit Pricer(std::string n) : name_(n) {}\n};\nint main(){\nPricer a("binomial");\n%s\n}\n'
prog(L, 'l11.s9 / review-3.6 move compiles', PR % 'Pricer b = std::move(a);', okc)
prog(L, 'review-3.6 copy does not compile', PR % 'Pricer b = a;', no_compile('deleted'))
prog(L, 'review-3.6 copy assignment does not compile', PR % 'Pricer b("tree"); b = a;', no_compile('deleted'))
prog(L, 'review-3.6 move from const does not compile', PR % 'const Pricer c("tree"); Pricer b = std::move(c);', no_compile('deleted'))

# l12
M0 = '''class Money {
public:
    explicit Money(long long pence) : pence_(pence) {}
private:
    long long pence_;
};

int main() {
    Money fee(250), tax(50);
    Money total = fee + tax;
}
'''
prog(L, 'l12.s0 clang: invalid operands at 10:23', M0, no_compile("main.cpp:10:23: error: invalid operands to binary expression ('Money' and 'Money')", '1 error generated.'))
prog(L, 'l12.s1 the first try on the six rows', H + 'std::string f(long long pence_) { return "£" + std::to_string(pence_ / 100)\n     + "." + std::to_string(pence_ % 100); }\nint main(){ for (long long p : {1234LL, 1205LL, 1200LL, 7LL, 99LL, -150LL}) std::cout << f(p) << "\\n"; }', out_is('£12.34\n£12.5\n£12.0\n£0.7\n£0.99\n£-1.-50'))
F = 'l12-operators'
P = 'screens.2.widget'
s = sol(F, P)
grade(L, 'l12.s2 no padding -> test-2', F, P, s.replace('        if (cents.size() < 2) cents = "0" + cents;\n', ''), 'test-2')
grade(L, 'l12.s2 padding but no sign handling -> test-8', F, P, s.replace('long long p = pence_ < 0 ? -pence_ : pence_;', 'long long p = pence_;').replace('std::string sign = pence_ < 0 ? "-" : "";', 'std::string sign = "";'), 'test-8')
grade(L, 'l12.s2 operator* missing -> compile, invalid operands', F, P, s.replace('Money operator*(Money m, int k) { return Money(m.pence() * k); }\n', ''), 'compile', lambda r: ('invalid operands' in r['diag'], r['diag'][:200]))
M3 = '''class Money {
public:
    explicit Money(long long pence) : pence_(pence) {}
    Money operator*(int k) const { return Money(pence_ * k); }
private:
    long long pence_;
};
%s
int main() {
    Money fee(250);
    Money a = fee * 3;
    Money b = 3 * fee;
}
'''
prog(L, 'l12.s3 clang: invalid operands (int and Money) at 12:17', M3 % '', no_compile("main.cpp:12:17: error: invalid operands to binary expression ('int' and 'Money')", '1 error generated.'))
prog(L, 'l12.s3 free operator*(int, Money) makes it compile', (M3 % '').replace('};\n\nint main', '};\nMoney operator*(int k, Money m) { return m * k; }\nint main'), okc)
prog(L, 'l12.s3 free operator*(Money, int) does not help', (M3 % '').replace('};\n\nint main', '};\nMoney operator*(Money m, int k);\nint main'), no_compile('error'))
MS = H + 'class Money { public: explicit Money(long long pence) : pence_(pence) {} long long pence() const { return pence_; }\n std::string str() const { long long p = pence_ < 0 ? -pence_ : pence_; std::string cents = std::to_string(p % 100); if (cents.size() < 2) cents = "0" + cents; std::string sign = pence_ < 0 ? "-" : ""; return sign + "£" + std::to_string(p / 100) + "." + cents; }\n private: long long pence_; };\nMoney operator*(Money m, int k) { return Money(m.pence() * k); }\n'
prog(L, 'l12.s4 chain prints £12.50 + £3.99; quiz3 prints -£7.50', MS + 'std::ostream& operator<<(std::ostream& os,\n                         const Money& m) {\n    os << m.str();\n    return os;\n}\nint main(){ std::cout << Money(1250) << " + " << Money(399) << \'\\n\'; Money fee(-375);\nstd::cout << (fee * 2).str() << \'\\n\'; }', out_is('£12.50 + £3.99\n-£7.50'))
prog(L, 'l12.s4 / quiz2 stream by value: deleted copy constructor', MS + 'std::ostream& operator<<(std::ostream os, const Money& m) {\n    os << m.str();\n    return os;\n}\nint main(){ std::cout << Money(1250) << \'\\n\'; }', no_compile('deleted'))
prog(L, 'l12.s5 prints 1250 1250; s6 prints 0', H + 'struct Money { long long pence; };\nMoney& operator+(Money& a, Money b) {\n    a.pence += b.pence;\n    return a;\n}\nstruct Price { double px; };\nbool operator==(Price a, Price b) {\n    return a.px == b.px;\n}\nint main() {\n    Money cash{1000}, fee{250};\n    Money total = cash + fee;\n    std::cout << cash.pence << \' \' << total.pence << \'\\n\';\n    Price fill{0.1 + 0.2}, limit{0.3};\n    std::cout << (fill == limit) << \'\\n\';\n}\n', out_is('1250 1250\n0'))
P = 'screens.7.widget'
s = sol(F, P)
grade(L, 'l12.s7 <= in operator< -> test-5', F, P, s.replace('a.pence < b.pence', 'a.pence <= b.pence'), 'test-5', lambda r: (True, 'rows 1,2: ' + str([(x['ok'], (x['error'] or '')[:80]) for x in r['rows'][:2]])))
grade(L, 'l12.s7 == also compares the venue -> test-7', F, P, s.replace('a.pence == b.pence', 'a.pence == b.pence && a.venue == b.venue'), 'test-7')
P = 'screens.9.widget'
s = sol(F, P)
T = 'return std::tie(a.price, a.time) < std::tie(b.price, b.time);'
assert T in s
grade(L, 'l12.s9 time only -> test-1 with C, A, B', F, P, s.replace(T, 'return a.time < b.time;'), 'test-1', lambda r: (r['rows'][0]['actual'] == '["C","A","B"]', 'actual=' + str(r['rows'][0]['actual'])))
grade(L, 'l12.s9 price only -> test-1 with B, A, C', F, P, s.replace(T, 'return a.price < b.price;'), 'test-1', lambda r: (r['rows'][0]['actual'] == '["B","A","C"]', 'actual=' + str(r['rows'][0]['actual'])))
prog(L, 'l12.quiz0 prints 000', H + 'struct Px { long long pence; std::string venue; };\nbool operator<(const Px& a, const Px& b) {\n    return a.pence < b.pence;\n}\nbool operator==(const Px& a, const Px& b) {\n    return a.pence == b.pence && a.venue == b.venue;\n}\nint main(){ Px a{100, "LSE"}, b{100, "CBOE"};\nstd::cout << (a < b) << (b < a) << (a == b); }', out_is('000'))
prog(L, 'l12.quiz1 Pnl + Quantity does not compile', 'struct Pnl { long long pence; };\nstruct Quantity { int shares; };\nPnl operator+(Pnl a, Pnl b) { return Pnl{a.pence + b.pence}; }\nint main(){\nPnl day{12500};\nQuantity filled{300};\nPnl oops = day + filled;\n}\n', no_compile('invalid operands'))
BID = H + 'struct Order { std::string id; long long price; int time; };\nbool operator<(const Order& a, const Order& b) { %s }\nint main(){ std::vector<Order> v{{"A", 100, 2}, {"B", 101, 3}, {"C", 101, 1}, {"D", 99, 1}}; std::sort(v.begin(), v.end()); for (auto& o : v) std::cout << o.id; std::cout << "\\n"; }'
prog(L, 'review-3.8 keyed body gives bids in trading order: C B A D', BID % 'return std::tie(b.price, a.time) < std::tie(a.price, b.time);', out_is('CBAD'))
prog(L, 'review-3.8 both flipped: latest first at one price: B C A D', BID % 'return std::tie(b.price, b.time) < std::tie(a.price, a.time);', out_is('BCAD'))
prog(L, 'review-3.8 ask order: D A C B', BID % 'return std::tie(a.price, a.time) < std::tie(b.price, b.time);', out_is('DACB'))

# l13
MAX = H + 'template <typename T>\nT max_of(const std::vector<T>& xs) {\n    T best = xs[0];\n    for (const T& x : xs) if (best < x) best = x;\n    return best;\n}\n'
prog(L, 'l13.s1 four calls; quiz0 VOD', MAX + 'int main(){ std::cout << max_of(std::vector<int>{3, 9, 4}) << max_of(std::vector<double>{101.5, 99.8}) << max_of(std::vector<int>{7, 2}) << max_of(std::vector<std::string>{"BARC", "AZN"}) << " " << max_of(std::vector<std::string>{"BARC", "AZN", "VOD", "LLOY"}) << "\\n"; }', out_is('9101.57BARC VOD'))
F = 'l13-templates'
P = 'screens.2.widget'
s = sol(F, P)
grade(L, 'l13.s2 T total = 0 -> test-7', F, P, s.replace('T total{};', 'T total = 0;'), 'test-7', lambda r: (True, 'row7 error=' + str(r['rows'][6]['error'])[:160]))
grade(L, 'l13.s2 int total -> compile, invalid operands next to std::string', F, P, s.replace('T total{};', 'int total = 0;'), 'compile', lambda r: ('invalid operands' in r['diag'] and 'std::string' in r['diag'], r['diag'][:300]))
grade(L, 'l13.s2 double total -> compile, invalid operands next to std::string', F, P, s.replace('T total{};', 'double total = 0;'), 'compile', lambda r: ('invalid operands' in r['diag'] and 'std::string' in r['diag'], r['diag'][:300]))
BG = 'template <typename T>\nT bigger(T a, T b) {\n    return a < b ? b : a;\n}\n\nint main() {\n    double x = %s;\n    return x == 3 ? 0 : 1;\n}\n'
prog(L, 'l13.s3 clang: no matching function, conflicting types note', BG % 'bigger(3, 2.5)', no_compile("main.cpp:7:16: error: no matching function for call to 'bigger'", "main.cpp:2:3: note: candidate template ignored: deduced conflicting types for parameter 'T' ('int' vs. 'double')", '1 error generated.'))
prog(L, 'l13.s3 bigger<double>(3, 2.5) compiles and is 3', BG % 'bigger<double>(3, 2.5)', lambda r: (bool(r.get('ok')) and r.get('code') == 0, f"{r.get('code')} {str(r.get('diag'))[:100]}"))
prog(L, 'l13.s3 bigger<int>(3, 2.5) compiles (2.5 becomes 2)', '#include <iostream>\n' + (BG % 'bigger<int>(3, 2.5)').replace('return x == 3 ? 0 : 1;', 'std::cout << bigger<int>(1, 2.5) << "\\n"; return 0;'), out_is('2'))
prog(L, 'l13.s3 bigger<int, double> does not compile', BG % 'bigger<int, double>(3, 2.5)', no_compile('error'))
prog(L, 'l13.s3 bigger(3.0, 2.5) works', BG % 'bigger(3.0, 2.5)', lambda r: (bool(r.get('ok')) and r.get('code') == 0, f"{r.get('code')}"))
SORTQ = '#include <algorithm>\n#include <vector>\n\nstruct Quote {\n    double bid;\n    double ask;\n};\n\nint main() {\n    std::vector<Quote> qs{{100.2, 100.4}, {99.9, 100.1}};\n    std::sort(qs.begin(), qs.end());\n}\n'
NEED = ["__algorithm/comp.h:41:18: error: invalid operands to binary expression ('const Quote' and 'const Quote')", '   41 |     return __lhs < __rhs;',
        "__debug_utils/strict_weak_ordering_check.h:43:31: note: in instantiation of function template specialization 'std::__less<>::operator()<Quote, Quote>' requested here",
        "__algorithm/sort.h:939:8: note: in instantiation of function template specialization 'std::__check_strict_weak_ordering_sorted<Quote *, std::__less<void, void>>' requested here",
        "__algorithm/sort.h:945:8: note: in instantiation of function template specialization 'std::__sort_impl<std::_ClassicAlgPolicy, std::__wrap_iter<Quote *>, std::__less<void, void>>' requested here",
        "__algorithm/sort.h:951:8: note: in instantiation of function template specialization 'std::sort<std::__wrap_iter<Quote *>, std::__less<void, void>>' requested here",
        "main.cpp:11:10: note: in instantiation of function template specialization 'std::sort<std::__wrap_iter<Quote *>>' requested here",
        'In file included from main.cpp:1:', 'algorithm:1842:', '__algorithm/adjacent_find.h:13:']


def sortq(r):
    d = r.get('diag') or ''
    miss = [n for n in NEED if n not in d]
    return r.get('ok') is False and not miss, f'missing={miss} head={d[:300]!r} tail={d[-200:]!r}'


JOBS.append({'name': 'l13.s4raw', 'prog': SORTQ, 'flags': ['-U_LIBCPP_HARDENING_MODE', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG', '-ferror-limit=19']}) if L in LEVELS else None
CHECKS.append((L, 'l13.s4 template error: every quoted line appears in the app compiler output with the library debug checks on (clang default error limit)', lambda res: (lambda d: (not [n for n in NEED if n not in d] and 'too many errors emitted' in d and '20 errors generated' in d, 'missing=' + str([n for n in NEED if n not in d]) + ' tail=' + d[-160:]))(open(os.path.join(TMP, 'sortq.txt')).read() if os.path.exists(os.path.join(TMP, 'sortq.txt')) else (res.get('l13.s4raw', {}).get('diag') or '')))) if L in LEVELS else None
SER = H + 'template <typename T>\nclass Series {\npublic:\n    void push(T x) { xs_.push_back(x); }\n    T mean() const {\n        T total{};\n        for (const T& x : xs_) total += x;\n        return total / xs_.size();\n    }\nprivate:\n    std::vector<T> xs_;\n};\n'
prog(L, 'l13.s5 Series<std::string> builds when mean is never called', SER + 'int main() {\n    Series<std::string> names;\n    names.push("AZN");\n    names.push("BARC");\n}\n', lambda r: (bool(r.get('ok')) and r.get('code') == 0, str(r.get('diag'))[:200]))
prog(L, 'l13.s5 adding names.mean(): invalid operands (std::string and size_type) at line 8 of the class', SER + 'int main() {\n    Series<std::string> names;\n    names.push("AZN");\n    names.mean();\n}\n', lambda r: (r.get('ok') is False and 'error: invalid operands to binary expression' in r['diag'] and "('std::string'" in r['diag'] and "'size_type'" in r['diag'] and 'return total / xs_.size();' in r['diag'], r['diag'][:300]))
prog(L, 'l13.s6 Series<int> mean prints 2000; negative total goes huge', SER + 'int main() {\n    Series<int> volumes;\n    volumes.push(1500);\n    volumes.push(2501);\n    std::cout << volumes.mean() << \'\\n\';\n    Series<int> neg; neg.push(-10); neg.push(4); std::cout << neg.mean() << \'\\n\';\n}\n', out_is('2000\n2147483645'))
P = 'screens.9.widget'
s = sol(F, P)
grade(L, 'l13.s9 oldest never dropped -> test-2', F, P, s.replace('        if (static_cast<int>(xs_.size()) > n_) xs_.erase(xs_.begin());\n', ''), 'test-2')
grade(L, 'l13.s9 empty window not refused -> test-7', F, P, s.replace('        if (xs_.empty()) throw std::logic_error("mean of an empty window");\n', ''), 'test-7')
grade(L, 'l13.s9 size 0 not refused -> test-8', F, P, s.replace('        if (n_ <= 0) throw std::invalid_argument("window size must be positive");\n', ''), 'test-8')
local(L, 'l13.quiz2 template defined in stats.cpp: undefined reference to sum_of<double> at link', has('g++', None, [], 'undefined reference to', 'sum_of<double>', rc=1,
      files={'stats.h': '#pragma once\n#include <vector>\ntemplate <typename T> T sum_of(const std::vector<T>&);\n', 'stats.cpp': '#include "stats.h"\ntemplate <typename T> T sum_of(const std::vector<T>& xs) { T t{}; for (const T& x : xs) t += x; return t; }\n', 'main.cpp': '#include "stats.h"\nint main(){ std::vector<double> v{1.0}; return sum_of(v) > 0 ? 0 : 1; }\n'}))
prog(L, 'l13.quiz3 empty sums are 0 and the empty string', H + 'template <typename T>\nT sum_of(const std::vector<T>& xs) {\n    T total{};\n    for (const T& x : xs) total += x;\n    return total;\n}\nint main(){ auto a = sum_of(std::vector<double>{});\nauto b = sum_of(std::vector<std::string>{}); std::cout << a << "[" << b << "]" << b.size() << "\\n"; }', out_is('0[]0'))



# ------------------------------------------------------------------ extras: empirical remarks, and the findings
H = '#include <iostream>\n#include <vector>\n#include <chrono>\n'


def speed():
    """l1 screens[10]: a compiled loop runs many times faster than the same loop in plain Python (a binomial-style backward pass)."""
    n, steps = 400, 400
    t0 = time.perf_counter()
    v = [float(i) for i in range(steps + 1)]
    for _ in range(n):
        for j in range(steps):
            v[j] = 0.5 * (v[j] + v[j + 1])
    py = time.perf_counter() - t0
    src = H + 'int main(){ const int n = 400 * 50, steps = 400; std::vector<double> v(steps + 1); for (int i = 0; i <= steps; ++i) v[i] = i;\n auto t0 = std::chrono::steady_clock::now(); for (int k = 0; k < n; ++k) for (int j = 0; j < steps; ++j) v[j] = 0.5 * (v[j] + v[j + 1]);\n auto t1 = std::chrono::steady_clock::now(); std::cout << std::chrono::duration<double>(t1 - t0).count() / 50 << " " << v[0] << "\\n"; }'
    r, err, out = cc('g++', src, ['-O1'], run=True)
    cpp = float(out.split()[0])
    return py / cpp > 5, f'python {py:.4f} s, g++ -O1 {cpp:.6f} s, ratio {py / cpp:.0f}'


local('L1', 'l1.s10 compiled loop is many times faster than plain Python (ratio above 5)', speed)
NRVO = H + 'int copies = 0, moves = 0;\nstruct Big { std::vector<double> v; explicit Big(int n) : v(n) {} Big(const Big& o) : v(o.v) { ++copies; } Big(Big&& o) noexcept : v(std::move(o.v)) { ++moves; } };\nBig make(int n) { Big b(n); b.v[0] = 1; return b; }\nint main(){ Big x = make(1000); std::cout << copies << " " << moves << " " << x.v.size() << "\\n"; }'
prog('L2', 'l5.s8 returned local: built in place by the app compiler (0 copies, 0 moves)', NRVO, out_is('0 0 1000'))
local('L2', 'l5.s8 returned local: g++ also builds it in place (0 copies, 0 moves)', has('g++', NRVO, [], rc=0, run_has=['0 0 1000']))
local('L2', 'l5.s8 with elision switched off it is moved, never copied (0 copies, 1 move)', has('g++', NRVO, ['-fno-elide-constructors'], rc=0, run_has=['0 1 1000']))
TIM = r'''#include <chrono>
#include <iostream>
#include <vector>
__attribute__((noinline)) double by_value(std::vector<double> v) { return v.empty() ? 0 : v[v.size() / 2]; }
__attribute__((noinline)) double by_cref(const std::vector<double>& v) { return v.empty() ? 0 : v[v.size() / 2]; }
int main() {
    for (int n : {1000, 10000, 100000, 1000000}) {
        std::vector<double> px(n, 100.0);
        int reps = 20000000 / n; volatile double sink = 0;
        auto t0 = std::chrono::steady_clock::now();
        for (int r = 0; r < reps; ++r) sink = sink + by_value(px);
        auto t1 = std::chrono::steady_clock::now();
        std::cout << std::chrono::duration<double, std::micro>(t1 - t0).count() / reps << " ";
    }
    std::vector<double> px(1000, 100.0); volatile double sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < 1000000; ++r) sink = sink + by_cref(px);
    auto t1 = std::chrono::steady_clock::now();
    std::cout << std::chrono::duration<double, std::nano>(t1 - t0).count() / 1000000 << "\n";
}
'''


def timing(r):
    try:
        a = [float(x) for x in r.get('out', '').split()]
    except ValueError:
        return False, str(r)[:200]
    want = [0.2, 3, 20, 1000]
    ok = len(a) == 5 and all(w / 10 <= x <= w * 10 for x, w in zip(a, want)) and a[4] < 100
    return ok, f'by value {a[:4]} us per call (table: 0.2, 3, 20, 1000); const& {a[4:]} ns'


prog('L2', 'l5.s4 copy timings under the app compiler are within a factor of 10 of the table', TIM, timing)


show = lambda r: (True, f"out={r.get('out')!r} code={r.get('code')} trap={r.get('trap')}")
# finding 2 (l7 screens[3] explain): what the app build does with an unguarded write through a null pointer
prog('L2', 'NOTE finding 2: bump(nullptr), the call on the canvas, does not write quietly: it stops (trap or non-zero exit)', '#include <iostream>\nvoid bump(int* p) {\n    *p += 1;\n}\nint main(){ bump(nullptr); std::cout << "end\\n"; }', lambda r: (bool(r.get('trap')) or r.get('code') not in (0, None), show(r)[1]))
prog('L2', 'NOTE finding 2: with a pointer the compiler cannot see is null, the write to address 0 is quiet', '#include <iostream>\nvoid bump(int* p) {\n    *p += 1;\n}\nint main(){ int* volatile q = nullptr; int before = *(volatile int*)0; bump(q); std::cout << "end " << *(volatile int*)0 - before << "\\n"; }', out_is('end 1'))
# finding 3 (l3 screens[7] options[1].why): Python leaves the loop variable at 4, not 5
local('L1', 'NOTE finding 3: Python for i in range(5) leaves i at 4; a C++ i declared before the loop ends at 5', lambda: ((lambda ns: (exec('for i in range(5):\n    pass', ns), ns['i'] == 4)[1])({}) and cc('g++', '#include <iostream>\nint main(){ int i; for (i = 0; i < 5; ++i) { } std::cout << i; }', [], run=True)[2].startswith('5'), ''))
# finding 4 (l4 screens[4]): 0.01 * sqrt(365)
local('L1', 'NOTE finding 4: 0.01 * sqrt(365) = 0.1910497, 4 dp 0.1910; the 0.19105 shown reads as 0.1911', lambda: (round(0.01 * 365 ** 0.5, 7) == 0.1910497 and f'{0.01 * 365 ** 0.5:.4f}' == '0.1910' and abs(0.1911 - 0.191) > 6e-05, f'{0.01 * 365 ** 0.5:.9f}'))


# finding 1 (l13 screens[4] feedback.byKey.l7): the key must sit on an instantiation note
def l13keys():
    s = at('l13-templates', 'screens.4')
    lines = s['canvas']['params']['lines']
    bad = []
    for k, text in s['feedback']['byKey'].items():
        n = int(k[1:])
        if '`instantiation` note' in text and 'note: in instantiation' not in lines[n - 1]:
            bad.append((k, lines[n - 1][:40]))
    return not bad, f'keys on lines that are not instantiation notes: {bad}'


local('L3', 'l13.s4 every byKey line that says "instantiation note" sits on a note line (finding 1)', l13keys)


def l1keys():
    s = at('l1-source-to-program', 'screens.10')
    lines = s['canvas']['params']['lines']
    bad = [k for k, t in s['feedback']['byKey'].items() if 'You picked a `note:`' in t and 'note:' not in lines[int(k[1:]) - 1]]
    return not bad, str(bad)


local('L1', 'l1.s10 every byKey line that says "You picked a note:" sits on a note line', l1keys)


if __name__ == '__main__':
    main()
