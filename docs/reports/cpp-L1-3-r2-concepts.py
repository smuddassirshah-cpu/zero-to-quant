#!/usr/bin/env python3
"""Round 2 blind concept audit of cpp L1 to L3: every code-behaviour claim, compiled and run.

    python3 docs/reports/cpp-L1-3-r2-concepts.py --wasm <pkgs folder> [--jobs 4] [--only <substring>] [--show]

Each check states a claim the content makes. Three kinds:
  number   plain arithmetic, in Python (CPython; the figures are IEEE doubles, the same as C++ and Pyodide)
  app      a program or a submission built by the app's own compiler (YoWASP clang 21.1.4, wasm32, libc++, -O1, the app's flags,
           harness, exception runtime and WASI shim, driven by cpp-L1-3-r2-zq.mjs, which reads js/engine/widgets/cpp-grade.js and
           js/screens/cpp-worker.js). A submission check names the mistake a `feedback.byKey` line names and the key the grader gives.
  desk     local g++ 13 and clang 18 on x86-64 Linux (messages g++ prints, AddressSanitizer reports, warning flags)
Exit 0 when every claim holds. A check that fails because the content is wrong stays failing: the ids are listed in
docs/reviews/audit-cpp-1-3-r2.md and in EXPECTED_FAIL below. With --recorded the exit code is 0 when exactly those fail
(the state at the audit: 366 checks, 350 hold, 16 fail; 94 of them run the solution and the starter of the 47 code widgets).
"""
import json, os, re, subprocess, sys, tempfile, shutil, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
APP = os.path.join(ROOT, 'app')
CPP = os.path.join(APP, 'content', 'courses', 'cpp')
ARGV = sys.argv[1:]
def arg(k, d=None):
    return ARGV[ARGV.index(k) + 1] if k in ARGV and ARGV.index(k) + 1 < len(ARGV) else d
PKGS = arg('--wasm')
NJOBS = int(arg('--jobs', '4'))
ONLY = arg('--only')
SHOW = '--show' in ARGV
TMP = tempfile.mkdtemp(prefix='cppr2-')

# Findings of the audit: these checks fail because the content is wrong (see the audit file, same ids)
EXPECTED_FAIL = {
    'h2.i5.at',                 # finding 1
    'l13.s2.fb-test-2',         # finding 2
    'l13.s7.slip-two',          # finding 3
    'l9.s2.throw-runs-destructor',  # finding 4
    'l5.s0.param-lifetime', 'l5.s0.param-lifetime-desk',  # finding 5
    'l13.s4.sort-error',        # finding 6
    'l13.s9.deque',             # finding 7
    'l3.s3.fb-error',           # finding 8
    'l1.s3.comma',              # finding 9
    'l1.s4.fb-test-3',          # finding 10
    'l3.s4.fb-test-6', 'l3.s4.fb-test-4',  # finding 11
    'l4.s5.fb-test-2',          # finding 12
    'l7.s4.fb-test-5',          # finding 13
    'l12.s9.fb-test-4',         # finding 14
}

checks = []   # (id, kind, claim, fn) where fn() -> (ok, detail)
jobs = []     # for the node driver
RES = {}

def load(f):
    return json.load(open(os.path.join(CPP, f + '.json')))
def at(o, p):
    for k in p.split('.'):
        o = o[int(k)] if isinstance(o, list) else o[k]
    return o
def sol(f, p):
    return at(load(f), p)['solution']
def starter(f, p):
    return at(load(f), p)['starter']

def check(cid, kind, claim, fn):
    if ONLY and ONLY not in cid:
        return
    checks.append((cid, kind, claim, fn))

# ------------------------------------------------------------------ app (wasm) helpers
HDR = ('#include <iostream>\n#include <iomanip>\n#include <vector>\n#include <string>\n#include <memory>\n#include <algorithm>\n'
       '#include <cmath>\n#include <stdexcept>\n#include <tuple>\n#include <cstdlib>\n')
def M(body, pre=''):
    return HDR + pre + '\nint main() {\n' + body + '\n}\n'

def app(cid, claim, code, pred, flags=None, stdin=''):
    if ONLY and ONLY not in cid:
        return
    jobs.append({'name': cid, 'prog': code, 'flags': flags or [], 'stdin': stdin})
    def fn():
        r = RES.get(cid)
        if r is None:
            return (False, 'no result (run with --wasm <pkgs>)')
        try:
            ok = bool(pred(r))
        except Exception as e:
            ok = False
        d = ('out=%r err=%r code=%r trap=%r' % (r.get('out'), (r.get('err') or '')[:300], r.get('code'), r.get('trap'))) if r.get('ok') else 'COMPILE: ' + (r.get('diag') or '')[:900]
        return (ok, d)
    checks.append((cid, 'app', claim, fn))

def out(s):
    return lambda r: r.get('ok') and r.get('code') == 0 and not r.get('trap') and r.get('out') == s
def diag(*needles, built=None):
    def p(r):
        d = r.get('diag') or ''
        if built is not None and bool(r.get('ok')) != built:
            return False
        return all(n in d for n in needles)
    return p
nobuild = lambda *n: diag(*n, built=False)

def submit(cid, claim, f, p, src, key, also=None):
    """The grader's key for a submission; key None means every test passes."""
    if ONLY and ONLY not in cid:
        return
    jobs.append({'name': cid, 'file': f, 'path': p, 'src': src})
    def fn():
        r = RES.get(cid)
        if r is None:
            return (False, 'no result (run with --wasm <pkgs>)')
        rows = r.get('rows') or []
        d = 'key=%r fails=%r ' % (r.get('key'), r.get('fails')) + ' | '.join('%d:%s %s%s' % (i + 1, 'ok' if x['ok'] else 'X', x.get('actual') if x.get('actual') is not None else repr((x.get('stdout') or '')[:40]), (' ERR ' + x['error'][:90]) if x.get('error') else '') for i, x in enumerate(rows) if not x['ok'])
        if r.get('key') == 'compile':
            d += ' DIAG ' + (r.get('diag') or '')[:500]
        ok = key(r.get('key')) if callable(key) else r.get('key') == key
        if ok and also:
            try:
                ok = bool(also(r))
            except Exception:
                ok = False
        return (ok, d)
    checks.append((cid, 'app', claim, fn))

def rep(s, a, b, n=1):
    assert s.count(a) >= 1, 'not found: ' + a
    return s.replace(a, b) if n == 0 else s.replace(a, b, n)

# ------------------------------------------------------------------ desk helpers
def desk_build(code, cc='g++', flags=(), name='main.cpp', extra=None):
    d = tempfile.mkdtemp(dir=TMP)
    open(os.path.join(d, name), 'w').write(code)
    files = [name]
    for k, v in (extra or {}).items():
        open(os.path.join(d, k), 'w').write(v)
        if k.endswith('.cpp'):
            files.append(k)
    p = subprocess.run([cc, '-std=c++17', *flags, *files, '-o', 'prog'], cwd=d, capture_output=True, text=True, env={**os.environ, 'LC_ALL': 'C'})
    return p.returncode, p.stdout + p.stderr, os.path.join(d, 'prog')
def desk_run(exe, stdin='', env=None):
    p = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=60, env={**os.environ, **(env or {})})
    return p.returncode, p.stdout, p.stderr
def desk(cid, claim, fn):
    def g():
        try:
            return fn()
        except Exception as e:
            return (False, 'exception ' + repr(e)[:300])
    check(cid, 'desk', claim, g)
def number(cid, claim, fn):
    check(cid, 'number', claim, lambda: (bool(fn()), ''))

# ================================================================== L1: l1-source-to-program
SEMI = '#include <iostream>\n\nint main() {\n    double price = 101.5\n    std::cout << price << \'\\n\';\n    return 0;\n}\n'
def _l1s5():
    rc, m, _ = desk_build(SEMI)
    return (rc != 0 and "main.cpp:5:5: error: expected ',' or ';' before 'std'" in m, m[:300])
desk('l1.s5.gxx-semicolon', "g++ reports the missing ; at main.cpp:5:5: expected ',' or ';' before 'std'", _l1s5)
app('l1.s6.clang-semicolon', "clang (the app) points at the end of line 4: expected ';' at end of declaration", SEMI, nobuild("main.cpp:4:25: error: expected ';' at end of declaration"))
WARN = '#include <iostream>\n\nint main() {\n    int qty = 100;\n    std::cout << "Hello, market" << \'\\n\';\n}\n'
def _l1s7():
    rc, m, exe = desk_build(WARN, flags=('-Wall',))
    r = desk_run(exe)
    return (rc == 0 and "main.cpp:4:9: warning: unused variable 'qty' [-Wunused-variable]" in m and r[0] == 0 and r[1] == 'Hello, market\n', m[:300])
desk('l1.s7.wall-unused', 'g++ -Wall warns at 4:9 about qty, still builds, and main without return exits 0', _l1s7)
ASG = M('    int signals = 3;\n    if (signals = 0) {\n        std::cout << "flat\\n";\n    }\n    std::cout << signals << \'\\n\';')
app('l1.s8.assign-in-if', 'if (signals = 0) prints 0, and clang warns by default', ASG, lambda r: out('0\n')(r) and 'Wparentheses' in r['diag'])
def _l1s8():
    a = desk_build(ASG); b = desk_build(ASG, flags=('-Wall',))
    return (a[0] == 0 and 'warning' not in a[1] and 'Wparentheses' in b[1] and desk_run(a[2])[1] == '0\n', a[1][:200] + b[1][:200])
desk('l1.s8.gxx-silent', 'g++ is silent about if (x = 0) without -Wall and warns with it', _l1s8)
VEC = '#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<double> closes{101.5, 102.0};\n    std::cout << closes << \'\\n\';\n}\n'
def _l1s10():
    rc, m, _ = desk_build(VEC)
    n = len(m.splitlines())
    first = "main.cpp:6:15: error: no match for 'operator<<' (operand types are 'std::ostream' {aka 'std::basic_ostream<char>'} and 'std::vector<double>')"
    return (rc != 0 and first in m and 150 <= n <= 320, 'lines=%d' % n)
desk('l1.s10.vector-error', "g++ 13: no match for operator<< at 6:15, and a message of about 232 lines (150 to 320 accepted: it depends on the headers)", _l1s10)
def _l1q0():
    rc, m, _ = desk_build('#include <iostream>\n\nint main() {\n    double price = 1;\n    std::cout << pirce << \'\\n\';\n}\n')
    return ("main.cpp:5:18: error: 'pirce' was not declared in this scope; did you mean 'price'?" in m, m[:300])
desk('l1.q0.did-you-mean', "g++: 'pirce' was not declared in this scope; did you mean 'price'? at 5:18", _l1q0)
def _l1s10b():
    import time
    cpp = '#include <cstdio>\n#include <vector>\n#include <cmath>\nint main() { int n = 2000; double u = 1.01, d = 1 / u, p = 0.5, s = 100, k = 100; double acc = 0; for (int rep = 0; rep < 5; ++rep) { std::vector<double> v(n + 1); for (int i = 0; i <= n; ++i) { double st = s * std::pow(u, i) * std::pow(d, n - i); v[i] = st > k ? st - k : 0; } for (int step = n; step > 0; --step) for (int i = 0; i < step; ++i) v[i] = p * v[i + 1] + (1 - p) * v[i]; acc += v[0]; } std::printf("%.6f\\n", acc); }\n'
    rc, m, exe = desk_build(cpp, flags=('-O1',))
    t0 = time.perf_counter(); o = desk_run(exe)[1]; tc = time.perf_counter() - t0
    t0 = time.perf_counter(); n = 2000; u = 1.01; d = 1 / u; p = 0.5; s = 100; k = 100
    v = [max(s * u**i * d**(n - i) - k, 0) for i in range(n + 1)]
    for step in range(n, 0, -1):
        for i in range(step):
            v[i] = p * v[i + 1] + (1 - p) * v[i]
    tp = (time.perf_counter() - t0) * 5
    return (tp / tc > 5 and abs(float(o) / 5 - v[0]) < 1e-6 * max(1, abs(v[0])), 'python %.2fs for 5 trees, C++ -O1 %.3fs, ratio %.0f' % (tp, tc, tp / tc))
desk('l1.s10.compiled-loop', 'a compiled binomial-tree loop runs many times faster than the same loop in plain Python (more than 5 times here)', _l1s10b)
app('l1.q2.no-std', 'cout without std:: does not compile', M('cout << "hi" << \'\\n\';'), nobuild('error'))
app('l1.q2.print', 'print("hi") does not compile', M('print("hi");'), nobuild('error'))
L1S3, L1S4 = 'screens.3.widget', 'screens.4.widget'
submit('l1.s3.fb-test-2', 'test-2 (words match, not every character): no line end passes test 1 and fails test 2', 'l1-source-to-program', L1S3, rep(sol('l1-source-to-program', L1S3), " << '\\n'", ''), 'test-2')
submit('l1.s3.comma', 'test-2 names the comma and the capital H: a missing comma passes test 1 and fails test 2', 'l1-source-to-program', L1S3, rep(sol('l1-source-to-program', L1S3), 'Hello, market', 'Hello market'), 'test-2')
submit('l1.s3.trailing-space', 'observation: a space before the line end passes test 1 and fails test 2', 'l1-source-to-program', L1S3, rep(sol('l1-source-to-program', L1S3), 'Hello, market"', 'Hello, market "'), 'test-2')
submit('l1.s4.fb-test-2', 'test-2: reading a whole line for the ticker passes test 1 and fails test 2', 'l1-source-to-program', L1S4, rep(sol('l1-source-to-program', L1S4), 'std::cin >> ticker >> price;', 'std::getline(std::cin, ticker); std::cin >> price;'), 'test-2')
submit('l1.s4.fb-test-3', 'test-3 (do not fix the decimal places): fixed with 2 decimals passes tests 1 and 2 and fails test 3', 'l1-source-to-program', L1S4, rep(rep(sol('l1-source-to-program', L1S4), '#include <string>', '#include <string>\n#include <iomanip>'), 'std::cout << "Ticker', 'std::cout << std::fixed << std::setprecision(2);\n    std::cout << "Ticker'), 'test-3')

# ================================================================== L1: l2-fixed-types
app('l2.types', 'this app: sizeof int 4, long long 8, double 8, bool 1, char 1; 7/2=3, -7/2=-3, 7.0/2=3.5, cast 3.5', M('std::cout << sizeof(int) << sizeof(long long) << sizeof(double) << sizeof(bool) << sizeof(char) << " " << 7 / 2 << " " << -7 / 2 << " " << 7.0 / 2 << " " << static_cast<double>(7) / 2 << " " << 3.0 / 4 << " " << 3 / 4 << " " << 3 / 4 * 1.0 << " " << static_cast<double>(3 / 4) << "\\n";'), out('48811 3 -3 3.5 3.5 0.75 0 0 0\n'))
app('l2.s1.wrap', 'int 2147483645 + 1 three times holds -2147483648 on this build (undefined by the standard)', M('volatile int k = 1; int count = 2147483645; count += k; count += k; count += k; std::cout << count << "\\n";'), out('-2147483648\n'), flags=['-w'])
app('l2.s3.auto', 'auto r = 7 / 2 is an int holding 3; auto r = 7.0 / 2 is a double 3.5', M('auto r = 7 / 2; auto d = 7.0 / 2; std::cout << std::is_same<decltype(r), int>::value << r << " " << std::is_same<decltype(d), double>::value << d << "\\n";', '#include <type_traits>\n'), out('13 13.5\n'))
L2 = 'l2-fixed-types'
submit('l2.s4.fb-test-1', 'test-1: the starter returns 3 for average(3, 4)', L2, 'screens.4.widget', starter(L2, 'screens.4.widget'), 'test-1', lambda r: r['rows'][0]['actual'] == '3')
submit('l2.s4.fb-test-5', 'test-5: (a + b) / 2.0 passes tests 1 to 4 and fails test 5 with a negative value', L2, 'screens.4.widget', rep(sol(L2, 'screens.4.widget'), '(static_cast<double>(a) + b) / 2', '(a + b) / 2.0'), 'test-5', lambda r: float(r['rows'][4]['actual']) < 0)
submit('l2.s5.fb-test-2', 'test-2: the starter squeezes 2,150,000,000 into an int and returns -2144967296', L2, 'screens.5.widget', starter(L2, 'screens.5.widget'), 'test-2', lambda r: r['rows'][1]['actual'] == '-2144967296')
number('l2.s5.narrow', '2,150,000,000 - 2^32 = -2,144,967,296', lambda: 2150000000 - 2**32 == -2144967296)
number('l2.s7.1999', '19.99 * 100 is 1998.9999999999998, truncates to 1998, rounds to 1999', lambda: repr(19.99 * 100) == '1998.9999999999998' and int(19.99 * 100) == 1998 and round(19.99 * 100) == 1999)
app('l2.s7.pence', 'int pence = price * 100 holds 1998 without a default warning; std::lround gives 1999', M('double price = 19.99; int pence = price * 100; std::cout << pence << " " << std::lround(price * 100) << "\\n";'), lambda r: out('1998 1999\n')(r) and 'warning' not in r['diag'])
submit('l2.s9.fb-test-3', 'test-3: dividing by the int 100 passes tests 1 and 2 and gives 0 on test 3', L2, 'screens.9.widget', rep(sol(L2, 'screens.9.widget'), '100.0', '100'), 'test-3', lambda r: r['rows'][2]['actual'] == '0')
submit('l2.s9.fb-test-2', 'test-2: an int for the pence passes test 1 and gives a positive number on test 2', L2, 'screens.9.widget', rep(sol(L2, 'screens.9.widget'), 'long long pence =', 'int pence ='), 'test-2', lambda r: float(r['rows'][1]['actual']) > 0)
app('l2.q0.bool', 'a bool prints as 1; std::boolalpha prints true', M('bool up = 101.5 > 100.0; std::cout << up << " " << std::boolalpha << up << "\\n";'), out('1 true\n'))
app('l2.q3.quarter', 'double share = 1 / 4 holds 0', M('double share = 1 / 4; std::cout << share << "\\n";'), out('0\n'))

# ================================================================== L1: l3-branches-and-loops
L3 = 'l3-branches-and-loops'
number('l3.s1.drawdown', 'drawdowns: (110-88)/110 = 0.2, slip from the first close 0.12, day 2 0.1', lambda: abs((110 - 88) / 110 - 0.2) < 1e-12 and (100 - 88) / 100 == 0.12 and abs((110 - 99) / 110 - 0.1) < 1e-12)
S33 = 'screens.3.widget'
submit('l3.s3.fb-test-2', 'test-2: i < prices.size() - 1 passes test 1 and stops on the empty vector', L3, S33, rep(sol(L3, S33), 'for (std::size_t i = 1; i < prices.size(); ++i) {\n        if (prices[i] > prices[i - 1]) {', 'for (std::size_t i = 0; i < prices.size() - 1; ++i) {\n        if (prices[i + 1] > prices[i]) {'), 'test-2')
submit('l3.s3.fb-test-6', 'test-6: >= passes tests 1 to 5 and fails test 6', L3, S33, rep(sol(L3, S33), 'prices[i] > prices[i - 1]', 'prices[i] >= prices[i - 1]'), 'test-6')
submit('l3.s3.fb-error', 'error (index out of bounds, <= in the loop test): the grader gives the key error for a program that stops', L3, S33, rep(sol(L3, S33), 'i < prices.size()', 'i <= prices.size()'), 'error')
app('l3.s3.size-minus-1', 'on this build size() - 1 of an empty vector is 4,294,967,295 (about 4 billion)', M('std::vector<double> p; std::cout << p.size() - 1 << " " << sizeof(std::size_t) << "\\n";'), out('4294967295 4\n'))
S34 = 'screens.4.widget'
MDD_STUCK = '#include <vector>\n\ndouble max_drawdown(const std::vector<double>& prices) {\n    if (prices.empty()) return 0;\n    double peak = prices[0];\n    double worst = 0;\n    for (double p : prices) {\n        double fall = (peak - p) / peak;\n        if (fall > worst) worst = fall;\n    }\n    return worst;\n}\n'
submit('l3.s4.fb-test-6', 'test-6 (if you got 0.4, your peak stayed at 100): a peak that never moves passes tests 1 to 5 and gives 0.4 on test 6', L3, S34, MDD_STUCK, 'test-6')
submit('l3.s4.fb-test-4', 'test-4 (if you got -0.1, subtract the other way): (p - peak) / peak passes tests 1 to 3 and fails test 4', L3, S34, rep(rep(sol(L3, S34), '(peak - p) / peak', '(p - peak) / peak'), 'fall > worst', 'fall < worst'), 'test-4')
submit('l3.s4.fb-test-1', 'test-1 (measure from the highest close so far, not the first): a peak fixed at the first close fails test 1', L3, S34, MDD_STUCK, 'test-1')
S35 = 'screens.5.widget'
submit('l3.s5.fb-test-1', 'test-1: starting the total at n prints 9.75', L3, S35, rep(sol(L3, S35), 'double total = 0;', 'double total = n;'), 'test-1', lambda r: r['rows'][0]['stdout'].strip() == '9.75')
submit('l3.s5.do-while', 'observation, no content claim: a do-while that runs once at n = 0 still passes every test (the failed read adds 0), so test 2 cannot tell', L3, S35, rep(sol(L3, S35), 'for (int i = 0; i < n; ++i) {\n        double x;\n        std::cin >> x;\n        total += x;\n    }', 'int i = 0;\n    do {\n        double x = 0;\n        std::cin >> x;\n        total += x;\n        ++i;\n    } while (i < n);'), None)
app('l3.s5.six-digits', '0.1 + 0.2 prints as 0.3: std::cout shows six significant digits', M('std::cout << 0.1 + 0.2 << "\\n";'), out('0.3\n'))
app('l3.s6.past-end', 'this app stops prices[3] on a vector of 3 (libc++ check), it does not throw std::out_of_range', M('std::vector<double> prices{101.2, 102.5, 99.8}; double last = 0; for (std::size_t i = 0; i <= prices.size(); ++i) { last = prices[i]; } std::cout << last << "\\n";'), lambda r: r.get('trap') and 'vector[] index out of bounds' in r.get('err', '') and 'out_of_range' not in r.get('err', ''))
app('l3.s6.at-throws', 'prices.at(3) throws std::out_of_range (which ends the run in this app)', M('std::vector<double> prices{101.2, 102.5, 99.8}; std::cout << prices.at(3) << "\\n";'), lambda r: r.get('code') == 134 and 'out_of_range' in r.get('err', ''))
app('l3.s7.scope', 'a for-loop variable does not exist after the loop: compile error', M('for (int i = 0; i < 5; ++i) { } std::cout << i;'), nobuild("use of undeclared identifier 'i'"))
S38 = 'screens.8.widget'
submit('l3.s8.fb-test-1', 'test-1: the starter gives Cboe 3 on LLCT', L3, S38, starter(L3, S38), 'test-1', lambda r: r['rows'][0]['actual'] == '[2,3,0,0]')
submit('l3.s8.fb-test-3', 'test-3: no default case passes tests 1 and 2 and fails test 3', L3, S38, rep(sol(L3, S38), "            default: ++counts[3]; break;\n", ''), 'test-3')
FALL = sol(L3, S38).replace("case 'L': ++counts[0]; break;", "case 'L': ++counts[0];") + '\nint main() { return fills_by_venue("L")[1]; }\n'
app('l3.s8.fallthrough-silent', 'clang is silent about the fall-through by default', FALL, lambda r: r.get('ok') and 'warning' not in r['diag'])
app('l3.s8.fallthrough-flag', 'clang warns with -Wimplicit-fallthrough', FALL, lambda r: r.get('ok') and 'Wimplicit-fallthrough' in r['diag'], flags=['-Wimplicit-fallthrough'])
def _l3s8():
    a = desk_build(FALL); b = desk_build(FALL, flags=('-Wimplicit-fallthrough',))
    return ('warning' not in a[1] and 'Wimplicit-fallthrough' in b[1], a[1][:200] + b[1][:200])
desk('l3.s8.gxx-fallthrough', 'g++ is silent by default and warns with -Wimplicit-fallthrough', _l3s8)
app('l3.q0.double-eq', '0.1 + 0.2 == 0.3 is false', M('volatile double a = 0.1, b = 0.2; std::cout << ((a + b == 0.3) ? "equal" : "different") << "\\n";'), out('different\n'))
number('l3.q0.repr', '0.1 + 0.2 is 0.30000000000000004', lambda: repr(0.1 + 0.2) == '0.30000000000000004')
app('l3.q2.empty-minus-one', 'the loop to size() - 1 on an empty vector reads past the end (this app stops it)', M('std::vector<double> prices; for (std::size_t i = 0; i < prices.size() - 1; ++i) { std::cout << prices[i] << "\\n"; }'), lambda r: bool(r.get('trap')))
app('l3.q3.stop-loss', 'day ends at 2', M('int day = 0; for (double p : {101.0, 97.5, 94.0, 92.0, 99.0}) { if (p < 95) break; ++day; } std::cout << day << "\\n";'), out('2\n'))

# ================================================================== L1: l4-functions-and-headers
L4 = 'l4-functions-and-headers'
LATE = '#include <cmath>\n#include <iostream>\n\nint main() {\n    std::cout << annualise(0.01) << \'\\n\';\n}\n\ndouble annualise(double daily_vol) {\n    return daily_vol * std::sqrt(252.0);\n}\n'
def _l4s0():
    rc, m, _ = desk_build(LATE)
    return (rc != 0 and "main.cpp:5:18: error: 'annualise' was not declared in this scope" in m, m[:300])
desk('l4.s0.not-declared', "g++: main.cpp:5:18: error: 'annualise' was not declared in this scope", _l4s0)
app('l4.s1.declared', 'with the declaration above main it prints 0.158745', LATE.replace('int main', 'double annualise(double daily_vol);\n\nint main'), out('0.158745\n'))
number('l4.s4.annualise', '0.01 * sqrt(365) = 0.19105 (0.1910), default 0.1587, slip 0.01 * 365 = 3.65', lambda: abs(0.01 * math.sqrt(365) - 0.191) < 6e-5 and abs(0.01 * math.sqrt(252) - 0.1587) < 1e-4 and abs(0.01 * 365 - 3.65) < 1e-12 and round(math.sqrt(365), 3) == 19.105)
number('l4.s6.tests', 'the four annualise test values', lambda: all(abs(a - b) < 1e-15 for a, b in [(0.01 * math.sqrt(252), 0.15874507866387544), (0.01 * math.sqrt(365), 0.191049731745428), (0.02 * math.sqrt(252), 0.3174901573277509), (0.01 * math.sqrt(12), 0.034641016151377546)]))
S45, S46 = 'screens.5.widget', 'screens.6.widget'
submit('l4.s5.fb-test-2', 'test-2 (your loop read prices[i - 1] with i at 0): a loop from index 0 passes test 1 and fails test 2', L4, S45, rep(sol(L4, S45), 'std::size_t i = 1', 'std::size_t i = 0'), 'test-2')
submit('l4.s5.fb-test-1', "test-1: dividing by today's close fails test 1", L4, S45, rep(sol(L4, S45), '/ prices[i - 1]);', '/ prices[i]);'), 'test-1')
submit('l4.s5.minus-one-bound', 'a loop to size() - 1 (no feedback line names it) passes tests 1 and 2 and stops on the empty vector, test 3', L4, S45, rep(sol(L4, S45), 'for (std::size_t i = 1; i < prices.size(); ++i) {\n        out.push_back((prices[i] - prices[i - 1]) / prices[i - 1]);', 'for (std::size_t i = 0; i < prices.size() - 1; ++i) {\n        out.push_back((prices[i + 1] - prices[i]) / prices[i]);'), 'test-3')
submit('l4.s6.fb-compile', 'compile: repeating = 252 in the definition is "redefinition of default argument"', L4, S46, rep(sol(L4, S46), 'int days)', 'int days = 252)'), 'compile', lambda r: 'redefinition of default argument' in r['diag'])
TWO = {'returns.h': '#pragma once\ndouble simple_return(double before, double after) {\n    return (after - before) / before;\n}\n', 'pricer.cpp': '#include "returns.h"\ndouble px() { return simple_return(1, 2); }\n'}
def _l4s7():
    rc, m, _ = desk_build('#include "returns.h"\nint main() { return simple_return(1, 2) > 0; }\n', extra=TWO)
    rc2, m2, _ = desk_build('#include "returns.h"\nint main() { return simple_return(1, 2) > 0; }\n', extra={**TWO, 'returns.h': TWO['returns.h'].replace('double simple', 'inline double simple')})
    return (rc != 0 and "multiple definition of `simple_return(double, double)'" in m and 'first defined here' in m and 'ld returned 1 exit status' in m and rc2 == 0, m[:300])
desk('l4.s7.multiple-definition', 'a body in a header included by two .cpp files: ld says multiple definition, despite #pragma once; inline fixes it', _l4s7)
def _l4q2():
    rc, m, _ = desk_build('double annualise(double daily_vol, int days = 252);\nint main() { return annualise(0.01) > 0; }\n')
    return (rc != 0 and "undefined reference to `annualise(double, int)'" in m and 'ld returned 1 exit status' in m, m[:300])
desk('l4.q2.undefined-reference', "a declared, called, never defined function: undefined reference to `annualise(double, int)'", _l4q2)
app('l4.s8.default-in-definition', 'with no default visible at the call, annualise(0.01) is a compile error', '#include <cmath>\ndouble annualise(double daily_vol, int days);\nint main() { return annualise(0.01) > 0; }\ndouble annualise(double daily_vol, int days = 252) { return daily_vol * std::sqrt(days); }\n', nobuild('no matching function for call'))
app('l4.q0.overload', 'mid(10001LL, 10002LL) and mid(100.01, 100.02) print 10001 100.015', M('std::cout << mid(10001LL, 10002LL) << \' \' << mid(100.01, 100.02);', 'double mid(double bid, double ask) { return (bid + ask) / 2; }\nlong long mid(long long bid, long long ask) { return (bid + ask) / 2; }\n'), out('10001 100.015'))
RF = 'double risk_free_rate() { return 0.04; }\n'
app('l4.q1.no-brackets', 'std::cout << risk_free_rate prints 1', M('std::cout << risk_free_rate << "\\n";', RF), out('1\n'))
app('l4.q1.void-call', 'risk_free_rate(void) in a call does not compile', M('std::cout << risk_free_rate(void) << "\\n";', RF), nobuild('error'))
app('l4.q1.extra-arg', 'risk_free_rate(0) does not compile', M('std::cout << risk_free_rate(0) << "\\n";', RF), nobuild('error'))

# ================================================================== L2: l5-value-or-reference
L5 = 'l5-value-or-reference'
app('l5.s0.copy', 'add_fee on a by-value vector leaves mine.size() at 2', M('std::vector<double> mine{250.00, 120.00}; add_fee(mine); std::cout << mine.size() << "\\n";', 'void add_fee(std::vector<double> costs) { costs.push_back(1.50); }\n'), out('2\n'))
app('l5.s1.alias', 'alias grows mine to 3; copy stays 2', M('std::vector<double> mine{250.00, 120.00}; std::vector<double>& alias = mine; std::vector<double> copy = mine; alias.push_back(1.50); std::cout << mine.size() << copy.size() << "\\n";'), out('32\n'))
app('l5.s2.ref', 'apply_fee through double& prints 997.5', M('double cash = 1000.00; apply_fee(cash, 2.50); std::cout << cash << "\\n";', 'void apply_fee(double& balance, double fee) { balance -= fee; }\n'), out('997.5\n'))
NORM = 'void normalise(std::vector<double> w) { double sum = 0; for (double x : w) sum += x; for (double& x : w) x /= sum; }\n'
app('l5.s6.normalise', 'normalise by value prints 2 and compiles without a warning', M('std::vector<double> w{2.0, 3.0, 5.0}; normalise(w); std::cout << w[0] << "\\n";', NORM), lambda r: out('2\n')(r) and 'warning' not in r['diag'], flags=['-Wall', '-Wextra'])
app('l5.s7.nan', 'dividing weights by a zero sum gives nan or infinity', M('volatile double z = 0; std::cout << 0.0 / z << " " << 1.0 / z << "\\n";'), lambda r: 'nan' in r['out'] and 'inf' in r['out'])
app('l5.q0.ref-ref', 'int& r2 = r; r2 = 9 changes x', M('int x = 5; int& r = x; int& r2 = r; r2 = 9; std::cout << x << "\\n";'), out('9\n'))
app('l5.q1.temporary', 'apply_fee(100.0, 2.50) with a double& does not compile: expects an lvalue for 1st argument', M('apply_fee(100.0, 2.50);', 'void apply_fee(double& balance, double fee) { balance -= fee; }\n'), nobuild('expects an lvalue for 1st argument'))
COPYCOUNT = '''
static int copies = 0, moves = 0;
struct V { std::vector<double> d; V(int n) : d(n, 100.0) {} V(const V& o) : d(o.d) { ++copies; } V(V&& o) noexcept : d(std::move(o.d)) { ++moves; } };
V make_prices(int n) { V v(n); return v; }
'''
app('l5.q2.return-no-copy', 'returning a local by value copies no element (built in place or moved)', M('V px = make_prices(1000); std::cout << copies << " " << px.d.size() << "\\n";', COPYCOUNT), out('0 1000\n'))
TIMING = HDR + '''#include <chrono>
__attribute__((noinline)) double by_value(std::vector<double> v) { return v[v.size() / 2]; }
__attribute__((noinline)) double by_cref(const std::vector<double>& v) { return v[v.size() / 2]; }
int main() {
    volatile double sink = 0;
    for (int n : {1000, 10000, 100000, 1000000}) {
        std::vector<double> v(n, 1.5);
        int reps = 200000000 / n / 8; if (reps < 20) reps = 20;
        auto t0 = std::chrono::steady_clock::now();
        for (int i = 0; i < reps; ++i) sink = sink + by_value(v);
        auto t1 = std::chrono::steady_clock::now();
        for (int i = 0; i < 2000000; ++i) sink = sink + by_cref(v);
        auto t2 = std::chrono::steady_clock::now();
        std::cout << n << " " << std::chrono::duration<double, std::micro>(t1 - t0).count() / reps << " " << std::chrono::duration<double, std::micro>(t2 - t1).count() / 2000000 << "\\n";
    }
}
'''
def _timing(r):
    rows = [l.split() for l in r['out'].strip().splitlines()]
    want = {1000: 0.2, 10000: 3, 100000: 20, 1000000: 1000}
    return all(want[int(n)] / 6 <= float(a) <= want[int(n)] * 6 and float(b) < 0.03 for n, a, b in rows)
app('l5.s4.timings', 'by-value calls take about 0.2, 3, 20 and 1000 microseconds for 1e3 to 1e6 doubles (within a factor of 6 under node), a const& call a few nanoseconds', TIMING, _timing)
BYVAL = 'struct L { L() {} L(const L&) { std::cout << "copy "; } ~L() { std::cout << "destroyed "; } };\nvoid f(L l) { std::cout << "body "; }\n'
app('l5.s0.param-lifetime', 'a by-value parameter (the copy) is destroyed at the function\'s closing brace, before the rest of the calling expression', M('L a; f(a), std::cout << "rest-of-expression "; std::cout << "next ";', BYVAL), lambda r: r['out'].startswith('copy body destroyed rest-of-expression'))
def _l5s0():
    code = HDR + BYVAL + 'int main() { L a; f(a), std::cout << "rest-of-expression "; std::cout << "next "; }\n'
    a = desk_run(desk_build(code)[2])[1]; b = desk_run(desk_build(code, cc='clang++')[2])[1]
    return (a.startswith('copy body destroyed rest-of-expression') and b.startswith('copy body destroyed rest-of-expression'), a + '| ' + b)
desk('l5.s0.param-lifetime-desk', 'the same on a desk build (g++ and clang)', _l5s0)
app('l9.s9.param-lifetime', 'in this app a unique_ptr parameter is destroyed at the callee\'s closing brace (close before the rest of the calling expression)', M('auto p = std::make_unique<Position>("VOD", 100); hold(std::move(p)), std::cout << "rest\\n";', 'struct Position {\n    std::string sym; int qty;\n    Position(std::string s, int q) : sym(s), qty(q) {}\n    ~Position() { std::cout << "close\\n"; }\n};\nvoid hold(std::unique_ptr<Position> p) { std::cout << "hold\\n"; }\n'), out('hold\nclose\nrest\n'))
number('l5.s4.mb', '1,000,000 doubles are 8 MB; slips 8,000,000, 1 and 64', lambda: 1000000 * 8 / 1e6 == 8)
number('l5.s5.book', '100 x 4.85 + 250 x 0.72 + 40 x 31.20 = 1913', lambda: abs(100 * 4.85 + 250 * 0.72 + 40 * 31.2 - 1913) < 1e-9)

# ================================================================== L2: l6-const
L6 = 'l6-const'
app('l6.s0.const-assign', "clang: main.cpp:3:10 cannot assign to variable 'tick' with const-qualified type 'const double', note at 2:18", 'int main() {\n    const double tick = 0.01;\n    tick = 0.05;\n}\n', nobuild("main.cpp:3:10: error: cannot assign to variable 'tick' with const-qualified type 'const double'", "main.cpp:2:18: note: variable 'tick' declared const here"))
app('l6.s1.px', "only line 4 fails: cannot assign to variable 'px' with const-qualified type 'const double &'", 'double with_fee(const double& px, double fee) {\n    double out = px;\n    out += fee;\n    px += fee;\n    fee = 0;\n    return out;\n}\nint main() {}\n', lambda r: not r.get('ok') and "cannot assign to variable 'px' with const-qualified type 'const double &'" in r['diag'] and r['diag'].count('error:') == 1 and 'main.cpp:4:' in r['diag'])
CALLS = '#include <vector>\ndouble mean(std::vector<double>& v);\nstd::vector<double> prices{101.5, 99.0};\nconst std::vector<double> fixed{100.0, 100.5};\nvoid f() {\n%s\n}\nint main() {}\ndouble mean(std::vector<double>& v) { return v[0]; }\n'
app('l6.s2.prices', 'mean(prices) compiles with a plain reference', CALLS % 'mean(prices);', diag(built=True))
app('l6.s2.temporary', 'mean({101.5, 99.0}) does not compile, and clang says it "expects an lvalue"', CALLS % 'mean({101.5, 99.0});', nobuild('expects an lvalue'))
app('l6.s2.fixed', 'mean(fixed) does not compile, and clang says it "would lose const qualifier"', CALLS % 'mean(fixed);', nobuild('would lose const qualifier'))
app('l6.s2.const-ref', 'with const std::vector<double>& all three calls compile', (CALLS % 'mean(prices); mean({101.5, 99.0}); mean(fixed);').replace('mean(std::vector<double>& v)', 'mean(const std::vector<double>& v)'), diag(built=True))
QUOTE = 'struct Quote {\n    double bid, ask;\n    double mid() const { return (bid + ask) / 2; }\n    void widen(double by) { bid -= by; ask += by; }\n};\nconst Quote q{99.98, 100.02};\nint main() {\n%s\n}\n'
app('l6.s3.ok', 'q.mid() and q.bid compile on a const Quote', QUOTE % 'double m = q.mid(); double b = q.bid; (void)m; (void)b;', diag(built=True))
app('l6.s3.widen', 'q.widen(0.01) fails: function is not marked const', QUOTE % 'q.widen(0.01);', nobuild('function is not marked const'))
app('l6.s3.ask', 'q.ask = 100.05 fails on a const Quote', QUOTE % 'q.ask = 100.05;', nobuild('error'))
CEX = 'constexpr int lot_size = 100;\nconstexpr double tick = 0.01;\nconstexpr double min_fee = tick * lot_size;\ndouble read_tick();\n%s\nconst double start_tick = read_tick();\nint main() {}\ndouble read_tick() { return 0.01; }\n'
app('l6.s5.constexpr', "line 5 alone is rejected: constexpr variable 'live_tick' must be initialized by a constant expression", CEX % 'constexpr double live_tick = read_tick();', lambda r: not r.get('ok') and "constexpr variable 'live_tick' must be initialized by a constant expression" in r['diag'] and r['diag'].count('error:') == 1)
app('l6.s5.rest', 'the other five lines compile', CEX % '', diag(built=True))
app('l6.s6.view', 'a const& view sees the change made through px: prints 99', M('std::vector<double> px{100.0, 101.0}; const std::vector<double>& view = px; px[0] = 99.0; std::cout << view[0] << "\\n";'), out('99\n'))
submit('l6.s7.starter-error', "the starter stops at main.cpp:5:15: cannot assign to return value because function 'operator[]' returns a const value", L6, 'screens.7.widget', starter(L6, 'screens.7.widget'), 'compile', lambda r: "main.cpp:5:15: error: cannot assign to return value because function 'operator[]' returns a const value" in r['diag'])
PTRS = 'int main() {\n    double x = 1, y = 2;\n%s\n}\n'
app('l6.s10.ptr-to-const', 'const double* p: *p = 3 fails, p = &y is fine', PTRS % '    const double* p = &x;\n    p = &y;\n    *p = 3;', lambda r: not r.get('ok') and r['diag'].count('error:') == 1 and 'main.cpp:5:' in r['diag'])
app('l6.s10.const-ptr', "double* const p: *p = 3 is fine, p = &y fails with 'double *const'", PTRS % '    double* const p = &x;\n    *p = 3;\n    p = &y;', lambda r: not r.get('ok') and r['diag'].count('error:') == 1 and "cannot assign to variable 'p' with const-qualified type 'double *const'" in r['diag'])
app('l6.s10.both', 'const double* const p: neither compiles', PTRS % '    const double* const p = &x;\n    *p = 3;\n    p = &y;', lambda r: not r.get('ok') and r['diag'].count('error:') == 2)
app('l6.q0.east-west', 'const int and int const are the same type', '#include <type_traits>\nstatic_assert(std::is_same<const int, int const>::value, "");\nint main() {}\n', diag(built=True))
app('l6.q2.report', "p.qty = 0 through const Position&: cannot assign to variable 'p' with const-qualified type 'const Position &'", 'struct Position { int qty; };\nvoid report(const Position& p) {\n    p.qty = 0;\n}\nint main() {}\n', nobuild("cannot assign to variable 'p' with const-qualified type 'const Position &'"))
app('l6.q3.temp', 'total({1.0, 2.0}) compiles with a const reference parameter', M('std::cout << total({1.0, 2.0}) << "\\n";', 'double total(const std::vector<double>& v) { return v[0] + v[1]; }\n'), out('3\n'))

# ================================================================== L2: l7-addresses
L7 = 'l7-addresses'
app('l7.s0.write-through', '*p = 500 changes qty', M('int qty = 300; int* p = &qty; *p = 500; std::cout << qty << "\\n";'), out('500\n'))
app('l7.s1.arith', '*(p + 2) from &px[1] reads 102, 16 bytes on; sizeof(Level) is 16; two variables have different addresses', M('std::vector<double> px{101.50, 101.25, 101.75, 102.00}; double* p = &px[1]; double a = 5.0, b = 5.0; std::cout << *(p + 2) << " " << (reinterpret_cast<char*>(p + 2) - reinterpret_cast<char*>(p)) << " " << sizeof(Level) << " " << (&a == &b) << "\\n";', 'struct Level { double px; long long size; };\n'), out('102 16 16 0\n'))
S73, S74 = 'screens.3.widget', 'screens.4.widget'
submit('l7.s3.fb-test-5', 'test-5: no nullptr guard passes tests 1 to 4 and fails test 5', L7, S73, rep(sol(L7, S73), '    if (p == nullptr) return;\n', ''), 'test-5')
app('l7.s3.null-write', 'this browser build quietly writes to address 0 through a null pointer (no crash)', HDR + '__attribute__((noinline)) void bump(int* p) { *p += 1; }\nint null_word() { return *(volatile int*)0; }\nint main() { int before = null_word(); int* volatile q = nullptr; bump(q); std::cout << null_word() - before << "\\n"; }\n', out('1\n'))
submit('l7.s4.fb-test-2', 'test-2: a best that starts at 0 passes test 1 and fails test 2', L7, S74, rep(rep(sol(L7, S74), 'double best = *begin;', 'double best = 0;'), 'begin + 1', 'begin'), 'test-2')
submit('l7.s4.fb-test-5', 'test-5 (read from begin and stop before end): a loop with p <= end passes tests 1 to 4 and fails test 5', L7, S74, rep(sol(L7, S74), 'p != end', 'p <= end'), 'test-5')
DANGLE = M('    double* p = nullptr;\n    {\n        double bid = 101.25;\n        p = &bid;\n    }\n    std::cout << *p << "\\n";')
app('l7.s5.dangling', 'in this browser the dangling read printed 101.25, and the program compiles cleanly', DANGLE, lambda r: out('101.25\n')(r) and 'warning' not in r['diag'])
SCOPE = '#include <iostream>\nint main() {\n    double* p = nullptr;\n    {\n        double bid = 101.25;\n        p = &bid;\n    }\n    std::cout << *p << "\\n";\n}\n'
def _l7s6():
    rc, m, exe = desk_build(SCOPE, flags=('-g', '-fsanitize=address'), name='scope.cpp')
    r = desk_run(exe)
    e = r[2]
    need = ['ERROR: AddressSanitizer: stack-use-after-scope', 'READ of size 8', 'in main', 'scope.cpp:8', "[32, 40) 'bid' (line 5) <== Memory access at offset 32 is inside this variable", 'SUMMARY: AddressSanitizer: stack-use-after-scope', 'This frame has 1 object(s):', 'is located in stack of thread T0 at offset 32 in frame']
    return (all(n in e for n in need), e[:700])
desk('l7.s6.asan-scope', 'g++ -g -fsanitize=address on scope.cpp: stack-use-after-scope, READ of size 8, scope.cpp:8, [32, 40) \'bid\' (line 5)', _l7s6)
app('l7.q0.null-read', "with this app's compiler a null read printed 0", M('int* p = nullptr; std::cout << *p << "\\n";'), out('0\n'))
def _l7q0():
    code = '#include <iostream>\nint main() {\n    int* p = nullptr;\n    std::cout << *p << "\\n";\n}\n'
    a = desk_build(code); ra = subprocess.run([a[2]], capture_output=True, text=True)
    b = desk_build(code, flags=('-g', '-fsanitize=address')); rb = desk_run(b[2])
    return (ra.returncode == -11 and 'SEGV on unknown address 0x000000000000' in rb[2], 'rc=%d %s' % (ra.returncode, rb[2][:200]))
desk('l7.q0.segv', "on Linux g++'s build dies with a segmentation fault; AddressSanitizer: SEGV on unknown address 0x000000000000", _l7q0)
app('l7.q1.pp', '**pp = 7 changes x', M('int x = 1; int* p = &x; int** pp = &p; **pp = 7; std::cout << x << "\\n";'), out('7\n'))
app('l7.q2.stack-address', "clang only warns: address of stack memory associated with local variable 'x' returned", 'double* best_bid() {\n    double x = 101.25;\n    return &x;\n}\nint main() { return best_bid() != nullptr; }\n', diag("warning: address of stack memory associated with local variable 'x' returned", built=True))
number('l7.q3.hex', '0x2000 + 3 * 4 = 0x200C; 0x1008 + 16 = 0x1018 = 0x1000 + 3 * 8; 0x4000 + 80 = 0x4050', lambda: 0x2000 + 12 == 0x200C and 0x1008 + 16 == 0x1018 == 0x1000 + 24 and 0x4000 + 5 * 16 == 0x4050)

# ================================================================== L2: l8-stack-and-heap
L8 = 'l8-stack-and-heap'
app('l8.s0.A', 'program A (a 16 MB local array) crashes in this browser with "memory access out of bounds"', M('    double prices[2000000];\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";'), lambda r: r.get('trap') and 'out of bounds' in r['trap'])
app('l8.s0.B', 'program B (a vector) prints 101; a vector object is 12 bytes here', M('    std::vector<double> prices(2000000);\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << " " << sizeof(prices) << "\\n";'), out('101 12\n'))
def _l8s0():
    a = desk_build('#include <iostream>\nint main() {\n    double prices[2000000];\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";\n}\n')
    ra = subprocess.run(['bash', '-c', 'ulimit -s 8192; exec ' + a[2]], capture_output=True, text=True)
    b = desk_build('#include <vector>\n#include <iostream>\nint main() { std::cout << sizeof(std::vector<double>) << "\\n"; }\n')
    return (ra.returncode in (-11, 139) and desk_run(b[2])[1] == '24\n', 'rc=%d' % ra.returncode)
desk('l8.s0.desk', 'g++ on Linux with an 8 MB stack: program A dies with a segmentation fault; a vector object is 24 bytes', _l8s0)
app('l8.s2.heap', 'make_price: *q reads 101.5 after the call', M('double* q = make_price(); std::cout << *q << "\\n"; delete q;', 'double* make_price() { double* p = new double(101.5); return p; }\n'), out('101.5\n'))
LEAK = 'double sum_prices(int n) {\n    double* prices = new double[n];\n    double total = 0;\n    for (int i = 0; i < n; ++i) {\n        prices[i] = 100 + i;\n        total += prices[i];\n    }\n    return total;\n}\nint main() { return sum_prices(1000) > 0 ? 0 : 1; }\n'
def _l8s4():
    rc, m, exe = desk_build(LEAK, flags=('-g', '-fsanitize=address'), name='leak.cpp')
    r = desk_run(exe, env={'ASAN_OPTIONS': 'detect_leaks=1'})
    e = r[2]
    need = ['ERROR: LeakSanitizer: detected memory leaks', 'Direct leak of 8000 byte(s) in 1 object(s) allocated from:', 'operator new[](unsigned long)', 'in sum_prices(int)', 'leak.cpp:2', 'in main', 'leak.cpp:10', 'SUMMARY: AddressSanitizer: 8000 byte(s) leaked in 1 allocation(s).']
    return (all(n in e for n in need), e[:600])
desk('l8.s4.lsan', 'LeakSanitizer: Direct leak of 8000 byte(s) in 1 object(s), sum_prices at leak.cpp:2, main at leak.cpp:10', _l8s4)
number('l8.s4.mb', '2,500 x 8,000 bytes = 20 MB; slips 0.008, 20,000,000 and 2.5', lambda: 2500 * 8000 / 1e6 == 20 and 8000 / 1e6 == 0.008 and 2500 * 1000 / 1e6 == 2.5)
MISMATCH = 'int main() {\n    double* px = new double[1000];\n    px[0] = 1;\n    delete px;\n}\n'
app('l8.s5.mismatch-runs', 'in this browser delete on new[] memory runs, prints nothing and exits 0; clang warns at compile time', MISMATCH, lambda r: out('')(r) and "warning: 'delete' applied to a pointer that was allocated with 'new[]'; did you mean 'delete[]'?" in r['diag'])
def _l8s5():
    rc, m, exe = desk_build(MISMATCH, flags=('-g', '-fsanitize=address'))
    e = desk_run(exe)[2]
    return ('ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)' in e, e[:200])
desk('l8.s5.asan-mismatch', 'AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)', _l8s5)
S86 = 'screens.6.widget'
submit('l8.s6.fb-test-1', 'test-1: the right output with delete px ends with status 1 from the leak checker', L8, S86, rep(sol(L8, S86), 'delete[] px;', 'delete px;'), 'test-1', lambda r: 'leak check' in (r['rows'][0]['error'] or '') and 'status 1' in (r['rows'][0]['error'] or ''))
app('l8.s8.deep-recursion', 'a recursion 10,000,000 calls deep stops in this app with "call stack exhausted"', HDR + '__attribute__((noinline)) long long down(long long n, volatile int* sink) { volatile int local = (int)n; *sink = local; if (n == 0) return 0; return 1 + down(n - 1, sink); }\nint main() { volatile int s = 0; std::cout << down(10000000, &s) << "\\n"; }\n', lambda r: r.get('trap') and 'call stack exhausted' in r['trap'])
app('l8.q0.delete-local', 'this browser build ran delete on the address of a local silently', M('double price = 101.25; double* volatile p = &price; delete p; std::cout << "ran\\n";'), out('ran\n'), flags=['-w'])
def _l8q0():
    rc, m, exe = desk_build('int main() {\n    double price = 101.25;\n    double* p = &price;\n    delete p;\n}\n')
    r = subprocess.run([exe], capture_output=True, text=True)
    return ("called on unallocated object 'price'" in m and r.returncode == -6 and 'free(): invalid pointer' in r.stderr, m[:200] + r.stderr[:100])
desk('l8.q0.gxx', "g++ warns \"called on unallocated object 'price'\", and the program aborts with free(): invalid pointer", _l8q0)
app('l8.q1.new-zero', 'new double[0] returns a non-null pointer', M('volatile int n = 0; double* p = new double[n]; std::cout << (p != nullptr) << "\\n"; delete[] p;'), out('1\n'))
app('l8.sum.double-delete', 'the browser build forgives a double delete (runs to the end, exit 0)', M('double* volatile r = new double(1.0); double* a = r; delete a; double* b = r; delete b; std::cout << "ran\\n";'), out('ran\n'), flags=['-w'])

# ================================================================== L2: l9-owning-memory
L9 = 'l9-owning-memory'
POS = 'struct Position {\n    std::string sym;\n    Position(std::string s) : sym(s) { std::cout << "open " << sym << "\\n"; }\n    ~Position() { std::cout << "close " << sym << "\\n"; }\n};\nvoid trade() {\n    Position p("VOD");\n    std::cout << "trading\\n";\n}\n'
app('l9.s0.order', 'open VOD, trading, close VOD, done', M('trade();\n    std::cout << "done\\n";', POS), out('open VOD\ntrading\nclose VOD\ndone\n'))
THROWDTOR = HDR + 'struct Guard { ~Guard() { std::cout << "freed\\n"; } };\nvoid f() { Guard g; throw std::runtime_error("x"); }\nint main() { f(); }\n'
app('l9.s2.throw-runs-destructor', "a local's destructor runs at every exit, a throw included (in this app)", THROWDTOR, lambda r: 'freed' in r.get('out', ''))
S93, S95 = 'screens.3.widget', 'screens.5.widget'
submit('l9.s3.fb-test-3', 'test-3: the starter leaks a Book on the capped path and fails test 3 only', L9, S93, starter(L9, S93), 'test-3', lambda r: r['fails'] == [3])
submit('l9.s3.delete-unique', 'hint: delete book on a unique_ptr does not compile', L9, S93, rep(sol(L9, S93), '    return book->total();', '    double t = book->total();\n    delete book;\n    return t;'), 'compile')
UP = HDR + 'struct Order { int qty; };\nvoid book_order(std::unique_ptr<Order> o) {}\nint main() {\n    auto a = std::make_unique<Order>(Order{100});\n%s\n}\n'
app('l9.s4.copy-error', "copying a unique_ptr: call to implicitly-deleted copy constructor of 'std::unique_ptr<Order>', because of a user-declared move constructor", UP % '    book_order(a);', nobuild("error: call to implicitly-deleted copy constructor of 'std::unique_ptr<Order>'", "copy constructor is implicitly deleted because 'unique_ptr<Order>' has a user-declared move constructor"))
app('l9.s4.move', 'book_order(std::move(a)) compiles and leaves a null', UP % '    book_order(std::move(a)); std::cout << (a == nullptr) << "\\n";', out('1\n'))
app('l9.s4.get', 'book_order(a.get()) does not compile', UP % '    book_order(a.get());', nobuild('error'))
app('l9.s4.deref', 'book_order(*a) does not compile', UP % '    book_order(*a);', nobuild('error'))
submit('l9.s5.fb-test-4', 'test-4: no check for a quantity of 0 passes tests 1 to 3 and fails test 4', L9, S95, rep(sol(L9, S95), '    if (qty == 0) return nullptr;\n', ''), 'test-4')
app('l9.s6.use-count', 'use_count is 1, then 3 inside the braces, then 1', M('struct Order {}; auto a = std::make_shared<Order>(); std::cout << a.use_count(); { auto b = a; auto c = b; std::cout << a.use_count(); } std::cout << a.use_count() << "\\n";'), out('131\n'))
CYCLE = '#include <iostream>\n#include <memory>\nstruct Node {\n    std::shared_ptr<Node> other;\n    ~Node() { std::cout << "freed\\n"; }\n};\nint main() {\n    {\n        auto a = std::make_shared<Node>();\n        auto b = std::make_shared<Node>();\n        a->other = b;\n        b->other = a;\n    }\n    std::cout << "end of main\\n";\n}\n'
app('l9.s7.cycle', 'two shared_ptr nodes that own each other: only "end of main" prints', CYCLE, out('end of main\n'))
def _l9s7():
    rc, m, exe = desk_build(CYCLE, flags=('-g', '-fsanitize=address'))
    e = desk_run(exe, env={'ASAN_OPTIONS': 'detect_leaks=1'})[2]
    return ('64 byte(s) leaked in 2 allocation(s)' in e, e[-200:])
desk('l9.s7.lsan', 'LeakSanitizer on a desk build: 64 byte(s) leaked in 2 allocation(s)', _l9s7)
HOLD = 'struct Position {\n    std::string sym; int qty;\n    Position(std::string s, int q) : sym(s), qty(q) { std::cout << "open " << sym << "\\n"; }\n    ~Position() { std::cout << "close " << sym << "\\n"; }\n};\nvoid hold(std::unique_ptr<Position> p) {\n    std::cout << "hold " << p->qty << "\\n";\n}\n'
app('l9.s9.five-lines', 'open VOD, opened, hold 100, close VOD, 1 after hold', M('    auto p = std::make_unique<Position>("VOD", 100);\n    std::cout << "opened\\n";\n    hold(std::move(p));\n    std::cout << (p == nullptr) << " after hold\\n";', HOLD), out('open VOD\nopened\nhold 100\nclose VOD\n1 after hold\n'))
app('l9.q0.moved', 'a moved-from unique_ptr is null: prints 1 101.5', M('auto a = std::make_unique<double>(101.5); auto b = std::move(a); std::cout << (a == nullptr) << " " << *b << "\\n";'), out('1 101.5\n'))
app('l9.q1.array', 'make_unique<double[]>(3) zeroes the elements: a run printed 0 101.5', M('auto px = std::make_unique<double[]>(3); px[2] = 101.5; std::cout << px[0] << " " << px[2] << "\\n";'), out('0 101.5\n'))
app('l9.q3.push-back', 'push_back(o) of a unique_ptr: call to implicitly-deleted copy constructor', M('struct Order {}; std::vector<std::unique_ptr<Order>> book; auto o = std::make_unique<Order>(); book.push_back(o);'), nobuild('call to implicitly-deleted copy constructor'))

# ================================================================== L3: l10-invariants
L10 = 'l10-invariants'
number('l10.s0.crossed', '100.4 - 100.6 is -0.19999999999998863 (Python prints it in full; six digits give -0.2)', lambda: repr(100.4 - 100.6) == '-0.19999999999998863' and '%.6g' % (100.4 - 100.6) == '-0.2')
app('l10.s0.struct', 'the crossed struct prints -0.2', M('Quote q{100.2, 100.4}; q.bid = 100.6; std::cout << q.ask - q.bid << \'\\n\';', 'struct Quote { double bid; double ask; };\n'), out('-0.2\n'))
PRIV = 'class Quote {\npublic:\n    Quote(double bid, double ask) : bid_(bid), ask_(ask) {}\n    double mid() const { return (bid_ + ask_) / 2; }\nprivate:\n    double bid_;\n    double ask_;\n};\n\nint main() {\n    Quote q(100.2, 100.4);\n    q.bid_ = 100.6;\n}\n'
app('l10.s2.private', "clang: main.cpp:12:7: error: 'bid_' is a private member of 'Quote'; note at 6:12; 1 error", PRIV, nobuild("main.cpp:12:7: error: 'bid_' is a private member of 'Quote'", 'main.cpp:6:12: note: declared private here', '1 error generated.'))
S103, S105, S109 = 'screens.3.widget', 'screens.5.widget', 'screens.9.widget'
submit('l10.s3.fb-test-4', 'test-4: no check in the constructor passes tests 1 to 3 and fails test 4', L10, S103, rep(sol(L10, S103), '        if (bid_ >= ask_) throw std::invalid_argument("bid must be below ask");\n', ''), 'test-4')
submit('l10.s3.fb-test-5', 'test-5: > in place of >= passes tests 1 to 4 and fails test 5', L10, S103, rep(sol(L10, S103), 'bid_ >= ask_', 'bid_ > ask_'), 'test-5')
submit('l10.s3.abort', 'a failed check may call std::abort()', L10, S103, rep(sol(L10, S103), 'throw std::invalid_argument("bid must be below ask");', 'std::abort();'), None)
number('l10.s4.avg', '(100 x 10 + 300 x 12) / 400 = 11.5; slips 11 and 12; quiz (200 x 5 + 50 x 6) / 250 = 5.2, slips 5.5 and 6', lambda: (100 * 10 + 300 * 12) / 400 == 11.5 and (10 + 12) / 2 == 11 and (200 * 5 + 50 * 6) / 250 == 5.2 and (5 + 6) / 2 == 5.5)
P105 = sol(L10, S105)
submit('l10.s5.fb-test-2', 'test-2: adding the shares before the average passes test 1 and fails test 2', L10, S105, rep(P105, '        avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty);\n        qty_ += qty;', '        qty_ += qty;\n        avg_ = (qty_ * avg_ + qty * px) / qty_;'), 'test-2')
submit('l10.s5.fb-test-4', 'test-4: a sale that changes the average passes tests 1 to 3 and fails test 4', L10, S105, rep(P105, '        qty_ -= qty;', '        avg_ = (qty_ * avg_) / (qty_ - qty + 1e-9);\n        qty_ -= qty;'), 'test-4')
submit('l10.s5.fb-test-6', 'test-6: no reset of the average when flat passes tests 1 to 5 and fails test 6', L10, S105, rep(P105, '        if (qty_ == 0) avg_ = 0.0;\n', ''), 'test-6')
submit('l10.s5.fb-test-8', 'test-8: no check on the size of a sale passes tests 1 to 7 and fails test 8', L10, S105, rep(P105, 'qty <= 0 || qty > qty_', 'qty <= 0'), 'test-8')
submit('l10.s5.fb-test-9', 'test-9: no check on a buy of 0 passes tests 1 to 8 and fails test 9', L10, S105, rep(P105, '        if (qty <= 0) throw std::invalid_argument("buy a positive quantity");\n', ''), 'test-9')
app('l10.s5.nan', 'a buy of 0 shares into a flat position makes the average 0/0, NaN', M('volatile int qty_ = 0, qty = 0; double avg_ = 0, px = 10; avg_ = (qty_ * avg_ + qty * px) / (qty_ + qty); std::cout << (avg_ != avg_) << "\\n";'), out('1\n'))
LIMIT = 'class Limit {\npublic:\n    Limit(double m) {\n        max_ = m;\n    }\nprivate:\n    const double max_;\n};\n\nint main() {\n    Limit l(5e6);\n}\n'
app('l10.s6.const-member', "clang: 3:5 constructor for 'Limit' must explicitly initialize the const member 'max_'; 7:18 note; 4:14 cannot assign to non-static data member; 2 errors", LIMIT, nobuild("main.cpp:3:5: error: constructor for 'Limit' must explicitly initialize the const member 'max_'", 'main.cpp:7:18: note: declared here', "main.cpp:4:14: error: cannot assign to non-static data member 'max_' with const-qualified type 'const double'", '2 errors generated.'))
app('l10.s6.list', 'Limit(double m) : max_(m) {} compiles', LIMIT.replace('    Limit(double m) {\n        max_ = m;\n    }', '    Limit(double m) : max_(m) {}'), diag(built=True))
app('l10.s6.this', 'this->max_ = m does not compile', LIMIT.replace('max_ = m;', 'this->max_ = m;'), nobuild('error'))
app('l10.s6.local', 'a local const double max_ leaves the first error', LIMIT.replace('max_ = m;', 'const double max_ = m;'), nobuild("must explicitly initialize the const member 'max_'"))
SETB = HDR + 'class Quote {\npublic:\n    Quote(double bid, double ask) : bid_(bid), ask_(ask) {\n        if (bid_ >= ask_) throw std::invalid_argument("crossed");\n    }\n    void set_bid(double b) { bid_ = b; }\n    double& bid() { return bid_; }\n    double spread() const { return ask_ - bid_; }\nprivate:\n    double bid_;\n    double ask_;\n};\nint main() {\n    Quote q(100.2, 100.4);\n    %s\n    std::cout << q.spread() << \'\\n\';\n}\n'
app('l10.s7.setter', 'an unchecked setter prints -0.2', SETB % 'q.set_bid(100.6);', out('-0.2\n'))
app('l10.q0.ref-getter', 'a getter returning double& prints -0.2', SETB % 'q.bid() = 100.6;', out('-0.2\n'))
P109 = sol(L10, S109)
submit('l10.s9.fb-test-4', 'test-4: no change of state when nothing remains passes tests 1 to 3 and fails test 4', L10, S109, rep(P109, '        if (filled_ == qty_) state_ = State::Filled;\n', ''), 'test-4')
submit('l10.s9.fb-test-7', 'test-7: no state check in fill passes tests 1 to 6 and fails test 7', L10, S109, rep(P109, '        if (state_ != State::New) throw std::logic_error("order is not live");\n        if (q <= 0', '        if (q <= 0'), 'test-7')
submit('l10.s9.fb-test-8', 'test-8: no check on the size of a fill passes tests 1 to 7 and fails test 8', L10, S109, rep(P109, 'q <= 0 || filled_ + q > qty_', 'q <= 0'), 'test-8')
submit('l10.s9.fb-test-9', 'test-9: no state check in cancel passes tests 1 to 8 and fails test 9', L10, S109, rep(P109, '        if (state_ != State::New) throw std::logic_error("order is not live");\n        state_ = State::Cancelled;', '        state_ = State::Cancelled;'), 'test-9')
app('l10.q2.not-const', "calling a non-const spread through const Quote&: 'this' argument ... has type 'const Quote', but function is not marked const", 'class Quote {\npublic:\n    Quote(double b, double a) : bid_(b), ask_(a) {}\n    double spread() { return ask_ - bid_; }\nprivate:\n    double bid_, ask_;\n};\ndouble width(const Quote& q) {\n    return q.spread();\n}\nint main() {}\n', nobuild("'this' argument to member function 'spread' has type 'const Quote', but function is not marked const"))

# ================================================================== L3: l11-creation-destruction
L11 = 'l11-creation-destruction'
LOG = 'struct Logger {\n    std::string name;\n    Logger(std::string n) : name(n) {\n        std::cout << "open " << name << \'\\n\';\n    }\n    ~Logger() { std::cout << "close " << name << \'\\n\'; }\n};\n'
app('l11.s0.lifo', 'open a, open b, work, close b, close a', M('Logger a("a");\n    Logger b("b");\n    std::cout << "work\\n";', LOG), out('open a\nopen b\nwork\nclose b\nclose a\n'))
app('l11.s2.scopes', 'open a, open b, work, close b, open c, close c, close a', M('Logger a("a");\n    {\n        Logger b("b");\n        std::cout << "work\\n";\n    }\n    Logger c("c");', LOG), out('open a\nopen b\nwork\nclose b\nopen c\nclose c\nclose a\n'))
WIN = '#include <vector>\n\nclass Window {\npublic:\n    Window(int n) : n_(n), data_(n_, 0.0) {}\nprivate:\n    std::vector<double> data_;\n    int n_;\n};\n\nint main() {\n    Window w(20);\n}\n'
app('l11.s4.reorder', "clang -Wall: 5:21 field 'n_' will be initialized after field 'data_' [-Wreorder-ctor]; 5:34 field 'n_' is uninitialized when used here [-Wuninitialized]; 2 warnings", WIN, lambda r: all(n in r['diag'] for n in ["main.cpp:5:21: warning: field 'n_' will be initialized after field 'data_' [-Wreorder-ctor]", "main.cpp:5:34: warning: field 'n_' is uninitialized when used here [-Wuninitialized]", '2 warnings generated.']), flags=['-Wall'])
app('l11.s5.copy', 'Logger b = a prints open a once and close a twice', M('Logger a("a");\n    Logger b = a;', LOG), out('open a\nclose a\nclose a\n'))
WHICH = 'struct Buffer {\n    Buffer(int, double) { std::cout << "ctor "; }\n    Buffer(const Buffer&) { std::cout << "copy-ctor "; }\n    Buffer(Buffer&&) { std::cout << "move-ctor "; }\n    Buffer& operator=(const Buffer&) { std::cout << "copy-assign "; return *this; }\n    Buffer& operator=(Buffer&&) { std::cout << "move-assign "; return *this; }\n};\n'
app('l11.s6.which', 'ctor, copy ctor, copy ctor, copy assignment, move ctor, move assignment', M('Buffer a(3, 1.5); Buffer b = a; Buffer c(a); b = a; Buffer d = std::move(a); c = std::move(b);', WHICH), out('ctor copy-ctor copy-ctor copy-assign move-ctor move-assign '))
S117, S1110 = 'screens.7.widget', 'screens.10.widget'
B = sol(L11, S117)
FOUR = '    Buffer(const Buffer&) = default;\n    Buffer(Buffer&&) = default;\n    Buffer& operator=(const Buffer&) = default;\n    Buffer& operator=(Buffer&&) = default;\n'
submit('l11.s7.fb-test-5', 'test-5: a copy constructor and nothing else (so a move copies) passes tests 1 to 4 and fails test 5', L11, S117, rep(B, FOUR, '    Buffer(const Buffer&) = default;\n'), 'test-5')
submit('l11.s7.fb-test-9', 'test-9: a declared move constructor deletes the copy assignment: copy and move constructors only pass tests 1 to 8 and fail test 9', L11, S117, rep(B, FOUR, '    Buffer(const Buffer&) = default;\n    Buffer(Buffer&&) = default;\n'), 'test-9')
submit('l11.s7.fb-test-10', 'test-10: a deleted move assignment passes tests 1 to 9 and fails test 10', L11, S117, rep(B, 'Buffer& operator=(Buffer&&) = default;', 'Buffer& operator=(Buffer&&) = delete;'), 'test-10')
submit('l11.s7.fb-test-12', 'test-12: without a move assignment (the other three declared) a is copied: passes tests 1 to 11 and fails test 12', L11, S117, rep(B, '    Buffer& operator=(Buffer&&) = default;\n', ''), 'test-12')
app('l11.s7.moved-from', 'a moved-from vector is empty in practice (construction and assignment, this build)', M('std::vector<double> a(3, 1.5), c(1, 0.0); std::vector<double> b = std::move(a); std::vector<double> d(3, 2.0); c = std::move(d); std::cout << a.size() << d.size() << b.size() << c.size() << "\\n";'), out('0033\n'), flags=['-w'])
C = sol(L11, S1110)
MOVE = '    Connection(Connection&& other) noexcept\n        : venue_(std::move(other.venue_)), open_(other.open_) {\n        other.open_ = false;\n    }\n'
DEL = '    Connection(const Connection&) = delete;\n    Connection& operator=(const Connection&) = delete;\n'
submit('l11.s10.fb-test-2', 'test-2: a move constructor that leaves other open (= default) passes test 1 and fails test 2', L11, S1110, rep(C, MOVE, '    Connection(Connection&&) = default;\n'), 'test-2')
submit('l11.s10.fb-test-8', 'test-8: a hand-written copy constructor (copying allowed) passes tests 1 to 7 and fails test 8', L11, S1110, rep(C, DEL, '    Connection(const Connection& o) : venue_(o.venue_), open_(false) {}\n'), 'test-8')
submit('l11.s10.no-delete', 'observation: with the move constructor declared, leaving both = delete lines out still passes every test (the copy is implicitly deleted)', L11, S1110, rep(C, DEL, ''), None)
submit('l11.s10.fb-test-1', 'test-1: no disconnect in the destructor fails test 1', L11, S1110, rep(C, '        if (open_) disconnect(venue_);\n', ''), 'test-1')
app('l11.q0.temporary', 'Logger("tmp"); prints open tmp, close tmp, next', M('Logger("tmp");\n    std::cout << "next\\n";', LOG), out('open tmp\nclose tmp\nnext\n'))
app('l11.q1.const-move', 'moving from a const Buffer copies: a.size() prints 3', M('const Buffer a(3, 1.5);\n    Buffer b = std::move(a);\n    std::cout << a.size() << \'\\n\';', B.replace('#include <vector>', '')), out('3\n'), flags=['-w'])
app('l11.q2.factory', 'returning a local Lattice copies its doubles 0 times', M('Lattice g = build(500); std::cout << copies << "\\n";', 'static int copies = 0;\nstruct Lattice { std::vector<double> v; explicit Lattice(int n) : v(n) {} Lattice(const Lattice& o) : v(o.v) { ++copies; } Lattice(Lattice&& o) noexcept : v(std::move(o.v)) {} };\nLattice build(int steps) { Lattice grid(steps); grid.v[0] = 1; return grid; }\n'), out('0\n'))
app('l11.q3.member-order', 'Desk with risk_ declared first: open risk, open feed, close feed, close risk', M('Desk d;', LOG + 'class Desk {\n    Logger risk_;\n    Logger feed_;\npublic:\n    Desk() : feed_("feed"), risk_("risk") {}\n};\n'), out('open risk\nopen feed\nclose feed\nclose risk\n'), flags=['-w'])

# ================================================================== L3: l12-operators
L12 = 'l12-operators'
MON = 'class Money {\npublic:\n    explicit Money(long long pence) : pence_(pence) {}\nprivate:\n    long long pence_;\n};\n\nint main() {\n    Money fee(250), tax(50);\n    Money total = fee + tax;\n}\n'
app('l12.s0.no-plus', "clang: main.cpp:10:23: error: invalid operands to binary expression ('Money' and 'Money')", MON, nobuild("main.cpp:10:23: error: invalid operands to binary expression ('Money' and 'Money')", '1 error generated.'))
app('l12.s1.first-try', 'the first try prints £12.34 £12.5 £12.0 £0.7 £0.99 £-1.-50', M('for (long long pence_ : {1234LL, 1205LL, 1200LL, 7LL, 99LL, -150LL}) std::cout << "£" + std::to_string(pence_ / 100) + "." + std::to_string(pence_ % 100) << " ";'), out('£12.34 £12.5 £12.0 £0.7 £0.99 £-1.-50 '))
S122, S127, S129 = 'screens.2.widget', 'screens.7.widget', 'screens.9.widget'
M2 = sol(L12, S122)
submit('l12.s2.fb-test-2', 'test-2: no padding passes test 1 and fails test 2', L12, S122, rep(M2, '        if (cents.size() < 2) cents = "0" + cents;\n', ''), 'test-2')
submit('l12.s2.fb-test-8', 'test-8: padding but no absolute value passes tests 1 to 7 and fails test 8', L12, S122, rep(rep(M2, 'long long p = pence_ < 0 ? -pence_ : pence_;', 'long long p = pence_;'), 'std::string sign = pence_ < 0 ? "-" : "";', 'std::string sign = "";'), 'test-8')
app('l12.s2.pound-bytes', 'the pound sign is two bytes in a std::string', M('std::cout << std::string("£").size() << "\\n";'), out('2\n'))
MEM = 'class Money {\npublic:\n    explicit Money(long long pence) : pence_(pence) {}\n    Money operator*(int k) const { return Money(pence_ * k); }\nprivate:\n    long long pence_;\n};\n\nint main() {\n    Money fee(250);\n    Money a = fee * 3;\n    Money b = 3 * fee;\n}\n'
app('l12.s3.member-side', "clang: main.cpp:12:17: error: invalid operands to binary expression ('int' and 'Money'); fee * 3 is fine", MEM, lambda r: not r.get('ok') and "main.cpp:12:17: error: invalid operands to binary expression ('int' and 'Money')" in r['diag'] and '1 error generated.' in r['diag'])
app('l12.s3.free', 'a free Money operator*(int k, Money m) makes 3 * fee compile', MEM.replace('int main', 'Money operator*(int k, Money m) { return m * k; }\nint main'), diag(built=True))
FULL = M2 + '\nstd::ostream& operator<<(std::ostream& os, const Money& m) {\n    os << m.str();\n    return os;\n}\n'
app('l12.s4.chain', 'std::cout << Money(1250) << " + " << Money(399) prints £12.50 + £3.99', '#include <iostream>\n' + FULL + 'int main() { std::cout << Money(1250) << " + " << Money(399) << \'\\n\'; }\n', out('£12.50 + £3.99\n'))
app('l12.q2.stream-by-value', "operator<< taking std::ostream by value: the call does not compile, the copy constructor is deleted", '#include <iostream>\n' + M2 + '\nstd::ostream& operator<<(std::ostream os, const Money& m) {\n    os << m.str();\n    return os;\n}\nint main() { std::cout << Money(1250) << \'\\n\'; }\n', nobuild('deleted'))
app('l12.q3.neg', '(Money(-375) * 2).str() is -£7.50', '#include <iostream>\n' + M2 + 'int main() { Money fee(-375); std::cout << (fee * 2).str() << \'\\n\'; }\n', out('-£7.50\n'))
app('l12.s5.plus-writes', 'a + that takes Money& prints 1250 1250', M('Money cash{1000}, fee{250};\n    Money total = cash + fee;\n    std::cout << cash.pence << \' \' << total.pence << \'\\n\';', 'struct Money { long long pence; };\nMoney& operator+(Money& a, Money b) {\n    a.pence += b.pence;\n    return a;\n}\n'), out('1250 1250\n'))
app('l12.s6.double-eq', 'Price{0.1 + 0.2} == Price{0.3} prints 0', M('volatile double x = 0.1; Price fill{x + 0.2}, limit{0.3};\n    std::cout << (fill == limit) << \'\\n\';', 'struct Price { double px; };\nbool operator==(Price a, Price b) { return a.px == b.px; }\n'), out('0\n'))
P7 = sol(L12, S127)
submit('l12.s7.fb-test-5', 'test-5: <= in operator< passes tests 1 to 4 and fails test 5', L12, S127, rep(P7, 'a.pence < b.pence', 'a.pence <= b.pence'), 'test-5')
submit('l12.s7.fb-test-7', 'test-7: an == that also compares the venue passes tests 1 to 6 and fails test 7', L12, S127, rep(P7, 'a.pence == b.pence', 'a.pence == b.pence && a.venue == b.venue'), 'test-7')
P9 = sol(L12, S129)
submit('l12.s9.fb-test-4', 'test-4 (compare prices before times): comparing time first passes tests 1 to 3 and fails test 4', L12, S129, rep(P9, 'std::tie(a.price, a.time) < std::tie(b.price, b.time)', 'std::tie(a.time, a.price) < std::tie(b.time, b.price)'), 'test-4')
submit('l12.s9.fb-test-1', 'test-1: the starter (always false) fails test 1', L12, S129, starter(L12, S129), 'test-1')
app('l12.q0.lt-eq', 'the Px operators print 000', M('Px a{100, "LSE"}, b{100, "CBOE"};\n    std::cout << (a < b) << (b < a) << (a == b);', 'struct Px { long long pence; std::string venue; };\nbool operator<(const Px& a, const Px& b) { return a.pence < b.pence; }\nbool operator==(const Px& a, const Px& b) { return a.pence == b.pence && a.venue == b.venue; }\n'), out('000'))
app('l12.q1.units', 'Pnl + Quantity does not compile', M('Pnl day{12500}; Quantity filled{300}; Pnl oops = day + filled;', 'struct Pnl { long long pence; };\nstruct Quantity { int shares; };\nPnl operator+(Pnl a, Pnl b) { return Pnl{a.pence + b.pence}; }\n'), nobuild('invalid operands'))

# ================================================================== L3: l13-templates
L13 = 'l13-templates'
MAXOF = 'template <typename T>\nT max_of(const std::vector<T>& xs) {\n    T best = xs[0];\n    for (const T& x : xs) if (best < x) best = x;\n    return best;\n}\n'
app('l13.s1.max-of', 'max_of works for int, double and std::string; the string maximum of BARC, AZN, VOD, LLOY is VOD', M('std::cout << max_of(std::vector<int>{3, 9, 4}) << " " << max_of(std::vector<double>{101.5, 99.8}) << " " << max_of(std::vector<std::string>{"BARC", "AZN"}) << " " << max_of(std::vector<std::string>{"BARC", "AZN", "VOD", "LLOY"}) << "\\n";', MAXOF), out('9 101.5 BARC VOD\n'))
S132, S139 = 'screens.2.widget', 'screens.9.widget'
T2 = sol(L13, S132)
submit('l13.s2.fb-test-2', 'test-2: an int total passes test 1 and gives 0 on test 2', L13, S132, rep(T2, 'T total{};', 'int total = 0;'), 'test-2', lambda r: r['rows'][1]['actual'] == '0')
submit('l13.s2.fb-test-7', 'test-7: T total = 0 passes tests 1 to 6 and fails test 7 (a std::string cannot start from a number)', L13, S132, rep(T2, 'T total{};', 'T total = 0;'), 'test-7')
BIG = 'template <typename T>\nT bigger(T a, T b) {\n    return a < b ? b : a;\n}\n\nint main() {\n    double x = bigger%s(3, 2.5);\n}\n'
app('l13.s3.conflict', "clang: 7:16 no matching function for call to 'bigger'; 2:3 note: deduced conflicting types for parameter 'T' ('int' vs. 'double')", BIG % '', nobuild("main.cpp:7:16: error: no matching function for call to 'bigger'", "main.cpp:2:3: note: candidate template ignored: deduced conflicting types for parameter 'T' ('int' vs. 'double')", '1 error generated.'))
app('l13.s3.double', 'bigger<double>(3, 2.5) compiles', BIG % '<double>', diag(built=True))
app('l13.s3.int', 'bigger<int>(3, 2.5) compiles', BIG % '<int>', diag(built=True))
app('l13.s3.two', 'bigger<int, double>(3, 2.5) does not compile', BIG % '<int, double>', nobuild('error'))
SORTQ = '#include <algorithm>\n#include <vector>\n\nstruct Quote {\n    double bid;\n    double ask;\n};\n\nint main() {\n    std::vector<Quote> qs{{100.2, 100.4}, {99.9, 100.1}};\n    std::sort(qs.begin(), qs.end());\n}\n'
def _sortq(r):
    d = r.get('diag') or ''
    need = ["/usr/include/c++/v1/__algorithm/comp.h:41:18: error: invalid operands to binary expression ('const Quote' and 'const Quote')",
            "/usr/include/c++/v1/__debug_utils/strict_weak_ordering_check.h:43:31: note: in instantiation of function template specialization 'std::__less<>::operator()<Quote, Quote>' requested here",
            '/usr/include/c++/v1/__algorithm/sort.h:939:8: note:', '/usr/include/c++/v1/__algorithm/sort.h:945:8: note:', '/usr/include/c++/v1/__algorithm/sort.h:951:8: note:',
            "main.cpp:11:10: note: in instantiation of function template specialization 'std::sort<std::__wrap_iter<Quote *>>' requested here",
            'fatal error: too many errors emitted, stopping now [-ferror-limit=]', '20 errors generated.', 'In file included from /usr/include/c++/v1/algorithm:1842:']
    return not r.get('ok') and all(n in d for n in need) and len(d.splitlines()) > 200
app('l13.s4.sort-error', 'std::sort on Quotes with no <, built as the screen says (clang++ -std=c++17 main.cpp, the library as shipped): the quoted lines, strict_weak_ordering_check.h and sort.h:939 included', SORTQ, lambda r: _sortq({**r, 'diag': (r.get('diag') or '').replace('21 errors generated.', '20 errors generated.')}), flags=['-ferror-limit=20', '-U_LIBCPP_HARDENING_MODE', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE'])
app('l13.s4.sort-error-debug', 'the same, with the library debug checks on (-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG): the quoted lines appear, in hundreds of lines (an explicit -ferror-limit=20 prints 21 errors; the default limit prints 20)', SORTQ, lambda r: _sortq({**r, 'diag': (r.get('diag') or '').replace('21 errors generated.', '20 errors generated.')}), flags=['-ferror-limit=20', '-U_LIBCPP_HARDENING_MODE', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG'])
app('l13.s4.two-lines', 'in the app build the two lines to tap exist: the first error (comp.h:41:18, invalid operands) and the main.cpp:11:10 note', SORTQ, lambda r: "comp.h:41:18: error: invalid operands to binary expression ('const Quote' and 'const Quote')" in r['diag'] and "main.cpp:11:10: note: in instantiation of function template specialization 'std::sort<std::__wrap_iter<Quote *>>' requested here" in r['diag'])
SER = '#include <iostream>\n#include <string>\n#include <vector>\ntemplate <typename T>\nclass Series {\npublic:\n    void push(T x) { xs_.push_back(x); }\n    T mean() const {\n        T total{};\n        for (const T& x : xs_) total += x;\n        return total / xs_.size();\n    }\nprivate:\n    std::vector<T> xs_;\n};\n'
app('l13.s5.lazy', 'Series<std::string> builds when nothing calls mean', SER + 'int main() {\n    Series<std::string> names;\n    names.push("AZN");\n    names.push("BARC");\n}\n', diag(built=True))
app('l13.s5.mean-string', "with names.mean() clang reports invalid operands ... ('std::string' ... and 'size_type' ...) at the return line", SER + 'int main() {\n    Series<std::string> names;\n    names.push("AZN");\n    names.mean();\n}\n', lambda r: not r.get('ok') and re.search(r"main\.cpp:11:\d+: error: invalid operands to binary expression \('std::string'.*and 'size_type'", r['diag']) is not None)
app('l13.s6.int-mean', 'Series<int> of 1500 and 2501 prints 2000; a negative total becomes a huge unsigned number before the division', SER + 'int main() {\n    Series<int> volumes;\n    volumes.push(1500);\n    volumes.push(2501);\n    std::vector<int> two(2); volatile int total = -6;\n    std::cout << volumes.mean() << " " << (total / two.size() > 2000000000u) << \'\\n\';\n}\n', out('2000 1\n'), flags=['-w'])
number('l13.s7.units', '1.2345 x 10^4 = 12345', lambda: round(1.2345 * 10**4) == 12345)
number('l13.s7.slip-two', 'the slip "two" (you used two places) has the value 123: 1.2345 x 10^2', lambda: round(1.2345 * 100, 2) == 123)
W = sol(L13, S139)
submit('l13.s9.fb-test-2', 'test-2: never dropping the oldest value passes test 1 and fails test 2', L13, S139, rep(W, '        if (static_cast<int>(xs_.size()) > n_) xs_.erase(xs_.begin());\n', ''), 'test-2')
submit('l13.s9.fb-test-7', 'test-7: no check for an empty window passes tests 1 to 6 and fails test 7', L13, S139, rep(W, '        if (xs_.empty()) throw std::logic_error("mean of an empty window");\n', ''), 'test-7')
submit('l13.s9.fb-test-8', 'test-8: no check in the constructor passes tests 1 to 7 and fails test 8', L13, S139, rep(W, '        if (n_ <= 0) throw std::invalid_argument("window size must be positive");\n', ''), 'test-8')
number('l13.s9.deque', 'l13 s9 explain says level 4 has a container that erases its front in constant time: level 4 (l14 to l18, review-4, homework-4) names std::deque, std::queue or pop_front', lambda: any(k in open(os.path.join(CPP, f + '.json')).read() for f in ['l14-vector', 'l15-maps', 'l16-algorithms', 'l17-cmake', 'l18-unit-tests', 'review-4', 'homework-4'] for k in ['std::deque', 'std::queue', 'pop_front']))
app('l13.q3.empty-sum', 'sum_of on empty vectors gives 0.0 and ""', M('auto a = sum_of(std::vector<double>{}); auto b = sum_of(std::vector<std::string>{}); std::cout << a << "[" << b << "]" << b.size() << "\\n";', T2.replace('#include <vector>\n#include <string>\n', '')), out('0[]0\n'))
def _l13q2():
    extra = {'stats.h': '#include <vector>\ntemplate <typename T> T sum_of(const std::vector<T>&);\n', 'stats.cpp': '#include "stats.h"\ntemplate <typename T> T sum_of(const std::vector<T>& xs) { T t{}; for (const T& x : xs) t += x; return t; }\n'}
    rc, m, _ = desk_build('#include "stats.h"\nint main() { return sum_of(std::vector<double>{0.5}) > 0; }\n', extra=extra)
    return (rc != 0 and 'undefined reference to' in m and 'sum_of<double>' in m, m[:300])
desk('l13.q2.template-in-cpp', 'a template defined in stats.cpp only: undefined reference to sum_of<double> at the link step', _l13q2)

# ================================================================== reviews
app('r1.prints', 'review-1: 3 / 4 into a double is 0; the loop from 3 by 2 below 10 runs 4 times; -9 / 4 is -2', M('int qty = 3; int lots = 4; double share = qty / lots; int turns = 0; for (int i = 3; i < 10; i += 2) { ++turns; } std::cout << share << " " << turns << " " << -9 / 4 << "\\n";'), out('0 4 -2\n'))
app('r1.i4.wrap', 'review-1: 1,500,000,000 + 1,500,000,000 in an int holds -1294967296 in practice (this build)', M('volatile int k = 1500000000; int volume = 1500000000; volume = volume + k; std::cout << volume << "\\n";'), out('-1294967296\n'))
number('r1.i4.arith', '3,000,000,000 - 2^32 = -1,294,967,296; Python -9 // 4 is -3', lambda: 3000000000 - 2**32 == -1294967296 and -9 // 4 == -3)
R1 = sol('review-1', 'items.5.widget')
submit('r1.i5.fb-test-3', 'review-1 test-3: <= passes tests 1 and 2 and fails test 3', 'review-1', 'items.5.widget', rep(R1, 'x < -limit', 'x <= -limit'), 'test-3')
submit('r1.i5.fb-test-1', 'review-1 test-1: comparing with limit, not -limit, fails test 1', 'review-1', 'items.5.widget', rep(R1, 'x < -limit', 'x < limit'), 'test-1')
app('r1.i6.default', 'review-1: annualise() does not compile; annualise(1) does', '#include <cmath>\ndouble annualise(double daily_vol, int days = 252) { return daily_vol * std::sqrt(days); }\nint main() { annualise(0.01); annualise(1); annualise(0.01, 12); annualise(); }\n', lambda r: not r.get('ok') and r['diag'].count('error:') == 1)
app('r2.i0.swap', 'review-2: swap_px by value prints 99.5 100.5', M('double bid = 99.5, ask = 100.5; swap_px(bid, ask); std::cout << bid << " " << ask << "\\n";', 'void swap_px(double a, double b) { double t = a; a = b; b = t; }\n'), out('99.5 100.5\n'))
REP = '#include <vector>\nvoid report(const std::vector<double>& v) {\n%s\n}\nint main() {}\n'
app('r2.i1.reads', 'review-2: size, v[0] and a changed copy compile through a const reference', REP % 'std::size_t n = v.size(); double first = v[0]; std::vector<double> c = v; c.push_back(1.0); (void)n; (void)first;', diag(built=True))
app('r2.i1.push', 'review-2: v.push_back(1.0) through a const reference does not compile', REP % 'v.push_back(1.0);', nobuild('error'))
app('r2.i3.dead-local', 'review-2: this browser build ran a read of a dead local silently', HDR + '__attribute__((noinline)) double* f() { double x = 1.0; double* volatile p = &x; return p; }\nint main() { volatile double y = *f(); std::cout << "ran\\n"; }\n', out('ran\n'), flags=['-w'])
app('r2.i3.at', 'review-2: v.at(5) on a vector of 3 throws std::out_of_range', M('std::vector<double> v(3); v.at(5); std::cout << "after\\n";'), lambda r: r.get('code') == 134 and 'out_of_range' in r.get('err', '') and 'after' not in r.get('out', ''), flags=['-w'])
def _r2i3():
    rc, m, exe = desk_build('int main() {\n    double* p = new double(1.0);\n    delete p;\n    delete p;\n}\n', flags=('-g', '-fsanitize=address', '-w'))
    e = desk_run(exe)[2]
    return ('double-free' in e, e[:200])
desk('r2.i3.asan-double-free', 'review-2: a desk build with -fsanitize=address reports "double-free"', _r2i3)
app('r2.i4.frames', 'review-2: depth(4) makes 5 calls of depth (6 frames with main)', M('std::cout << calls_of(4) << "\\n";', 'static int calls = 0;\nint depth(int n) { ++calls; if (n == 0) return 0; return 1 + depth(n - 1); }\nint calls_of(int n) { depth(n); return calls; }\n'), out('5\n'))
POS2 = 'struct Position {\n    std::string sym; int qty;\n    Position(std::string s, int q) : sym(s), qty(q) { std::cout << "open " << sym << "\\n"; }\n    ~Position() { std::cout << "close " << sym << "\\n"; }\n};\n'
app('r2.i5.scope', 'review-2: a vector of unique_ptr dies at the inner brace: open AZN, close AZN, end', M('{\n    std::vector<std::unique_ptr<Position>> book;\n    book.push_back(std::make_unique<Position>("AZN", 10));\n}\nstd::cout << "end\\n";', POS2), out('open AZN\nclose AZN\nend\n'))
number('r2.i6.accrue', 'review-2: 100 x 1.1 x 1.1 = 121; 1000 x 1.01 = 1010; 2500 x 1.002 = 2505', lambda: abs(100 * 1.1 * 1.1 - 121) < 1e-9 and abs(1000 * 1.01 - 1010) < 1e-9 and abs(2500 * 1.002 - 2505) < 1e-9)
app('r3.i1.desk-order', 'review-3: open feed, open risk, desk open, desk close, close risk, close feed', M('Desk d;', LOG + 'class Desk {\npublic:\n    Desk() : feed_("feed"), risk_("risk") {\n        std::cout << "desk open\\n";\n    }\n    ~Desk() { std::cout << "desk close\\n"; }\nprivate:\n    Logger feed_;\n    Logger risk_;\n};\n'), out('open feed\nopen risk\ndesk open\ndesk close\nclose risk\nclose feed\n'))
PRI = HDR + 'struct Lattice {};\nclass Pricer {\n    std::string name_;\n    std::unique_ptr<Lattice> grid_;\npublic:\n    explicit Pricer(std::string n) : name_(n) {}\n};\nint main() {\n    Pricer a("binomial");\n    %s\n}\n'
app('r3.i6.move', 'review-3: Pricer b = std::move(a) compiles', PRI % 'Pricer b = std::move(a);', diag(built=True))
app('r3.i6.copy', 'review-3: Pricer b = a does not compile', PRI % 'Pricer b = a;', nobuild('error'))
app('r3.i6.assign', 'review-3: b = a does not compile', PRI % 'Pricer b("tree"); b = a;', nobuild('error'))
app('r3.i6.const-move', 'review-3: moving from a const Pricer does not compile', PRI % 'const Pricer c("tree"); Pricer b = std::move(c);', nobuild('error'))
BID = HDR + 'struct Order { std::string id; long long price; int time; };\nbool operator<(const Order& a, const Order& b) {\n    %s\n}\nint main() {\n    std::vector<Order> book{{"A", 100, 2}, {"B", 101, 3}, {"C", 101, 1}, {"D", 99, 0}};\n    std::sort(book.begin(), book.end());\n    for (const Order& o : book) std::cout << o.id;\n}\n'
app('r3.i8.right', 'review-3: tie(b.price, a.time) < tie(a.price, b.time) sorts bids C, B, A, D (price down, time up)', BID % 'return std::tie(b.price, a.time) < std::tie(a.price, b.time);', out('CBAD'))
app('r3.i8.both', 'review-3: flipping both gives the latest first at one price: B, C, A, D', BID % 'return std::tie(b.price, b.time) < std::tie(a.price, a.time);', out('BCAD'))
app('r3.i8.ask', 'review-3: the unflipped body is the ask order: D, A, C, B', BID % 'return std::tie(a.price, a.time) < std::tie(b.price, b.time);', out('DACB'))

# ================================================================== homework
H1 = 'homework-1'
CSV = sol(H1, 'items.1.widget')
submit('h1.i1.fb-test-2', 'homework-1 test-2: reading a first close before the loop passes test 1 and stops on the header-only file', H1, 'items.1.widget', rep(CSV, '    double peak = 0;\n', '    std::getline(std::cin, line);\n    double peak = std::stod(line.substr(line.find(\',\') + 1));\n'), 'test-2')
submit('h1.i1.fb-test-6', 'homework-1 test-6: no skip of comma-less lines passes tests 1 to 5 and stops on test 6', H1, 'items.1.widget', rep(CSV, '        if (comma == std::string::npos) {\n            continue;\n        }\n', ''), 'test-6')
number('h1.i1.falls', 'homework-1: (262.5 - 199.5) / 262.5 = 24%, (275 - 247.5) / 275 = 10%, (80 - 60) / 80 = 25%', lambda: abs((262.5 - 199.5) / 262.5 - 0.24) < 1e-12 and abs((275 - 247.5) / 275 - 0.1) < 1e-12 and (80 - 60) / 80 == 0.25)
BAND = sol(H1, 'items.2.widget')
submit('h1.i2.fb-test-4', 'homework-1 test-4: <= on the buy side passes tests 1 to 3 and fails test 4', H1, 'items.2.widget', rep(BAND, 'price < average - band', 'price <= average - band'), 'test-4')
submit('h1.i2.fb-test-5', 'homework-1 test-5: >= on the sell side passes tests 1 to 4 and fails test 5', H1, 'items.2.widget', rep(BAND, 'price > average + band', 'price >= average + band'), 'test-5')
submit('h1.i3.fb-test-3', 'homework-1 test-3: an int total passes tests 1 and 2 and fails test 3', H1, 'items.3.widget', rep(sol(H1, 'items.3.widget'), 'long long total = 0;', 'int total = 0;'), 'test-3')
def _h1i4():
    rc, m, _ = desk_build('#include <vector>\nint main() {\n    std::vector<double> prices(3);\n    int n = 0;\n    for (int i = 0; i < prices.size(); ++i) { ++n; }\n    return n - 3;\n}\n', flags=('-Wall',))
    return ("warning: comparison of integer expressions of different signedness: 'int' and 'std::vector<double>::size_type'" in m, m[:300])
desk('h1.i4.sign-compare', "homework-1: g++ -Wall: comparison of integer expressions of different signedness: 'int' and 'std::vector<double>::size_type'", _h1i4)
number('h1.i5.pence', 'homework-1: 0.29 * 100 is 28.999999999999996, truncates to 28, rounds to 29', lambda: repr(0.29 * 100) == '28.999999999999996' and int(0.29 * 100) == 28 and round(0.29 * 100) == 29)
PORT = '#include <vector>\n#include <iostream>\nint main() {\n    std::vector<int> fills{1500000000, 1500000000};\n    int n_fills = 2;\n    int total_qty = 0;\n    for (int q : fills) {\n        total_qty += q;\n    }\n    double avg = total_qty / n_fills;\n    std::cout << total_qty << " " << avg << "\\n";\n}\n'
def _h1i6():
    a = desk_build(PORT, flags=('-Wall', '-Wextra', '-Wconversion'))
    b = desk_build(PORT, cc='clang++', flags=('-Wall', '-Wextra', '-Wconversion'))
    u = desk_build(PORT, flags=('-fsanitize=undefined',))
    ru = desk_run(u[2])
    d = os.path.dirname(a[2])
    t = subprocess.run(['clang-tidy', '-checks=-*,bugprone-integer-division', 'main.cpp', '--', '-std=c++17'], cwd=d, capture_output=True, text=True)
    return ('warning' not in a[1] and 'warning' not in b[1] and 'signed integer overflow' in ru[2] and 'bugprone-integer-division' in t.stdout and desk_run(a[2])[1].split()[0] == '-1294967296', a[1][:150] + b[1][:150] + ru[2][:150] + t.stdout[:150])
desk('h1.i6.model', 'homework-1 model answer: g++ and clang print nothing with -Wall -Wextra -Wconversion; UBSan reports the overflow; clang-tidy bugprone-integer-division flags the division; the total prints -1294967296', _h1i6)
number('h1.i6.avg', 'homework-1: 10,000,002 / 4 is 2,500,000 in integers and 2,500,000.5 exactly', lambda: 10000002 // 4 == 2500000 and 10000002 / 4 == 2500000.5)
def _tick():
    def sv(prices, sizes):
        tot, sign = 0, 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]: sign = 1
            elif prices[i] < prices[i - 1]: sign = -1
            tot += sign * sizes[i]
        return tot
    w = at(load(H1), 'items.8.widget')
    return all(sv(*t['args']) == t['expect'] for t in w['tests'])
number('h1.i8.tick-rule', 'homework-1: all ten tick-rule expected values, recomputed in Python from the rule', _tick)
H2 = 'homework-2'
submit('h2.i0.fb-test-1', 'homework-2 test-1: for (Position p : book) changes a copy and fails test 1', H2, 'items.0.widget', rep(sol(H2, 'items.0.widget'), 'for (Position& p : book)', 'for (Position p : book)'), 'test-1')
VW = sol(H2, 'items.1.widget')
submit('h2.i1.fb-test-4', 'homework-2 test-4: an int total passes tests 1 to 3 and fails test 4', H2, 'items.1.widget', rep(rep(rep(VW, 'long long total_qty', 'int total_qty'), 'long long q = 0;', 'int q = 0;'), 'long long q = total_qty', 'int q = total_qty'), 'test-4')
number('h2.numbers', 'homework-2: 121,485 / 1,200 = 101.2375; 7,290 / 1,500 = 4.86; 370 - 95 = 275; 10,000 x 501 x 8 = 40,080,000; payoff 0.5 x 15 = 7.5', lambda: abs((500 * 101.25 + 300 * 101.40 + 400 * 101.10) - 121485) < 1e-6 and abs(121485 / 1200 - 101.2375) < 1e-9 and abs((1000 * 4.85 + 500 * 4.88) / 1500 - 4.86) < 1e-9 and abs(200 * 1.85 - 50 * 1.90 - 275) < 1e-9 and 10000 * 501 * 8 == 40080000 and 10000 * 500 * 8 / 1e6 == 40 and 501 * 8 == 4008)
app('h2.i2.payoff', 'homework-2: price_option(100, 95) prints 7.5', M('std::cout << price_option(100, 95) << "\\n";', 'double payoff(double s, double k) { return s > k ? s - k : 0; }\ndouble price_option(double s, double k) { double up = payoff(s * 1.1, k); double down = payoff(s * 0.9, k); return 0.5 * up + 0.5 * down; }\n'), out('7.5\n'))
app('h2.i5.null', 'homework-2: the null read ran in this browser build without stopping', M('int* volatile p = nullptr; int x = *p; std::cout << "ran " << x << "\\n";'), lambda r: r.get('code') == 0 and not r.get('trap') and r['out'].startswith('ran'), flags=['-w'])
app('h2.i5.mismatch', 'homework-2: delete on new double[4] ran without stopping', M('double* volatile q = new double[4]; double* a = q; delete a; std::cout << "ran\\n";'), out('ran\n'), flags=['-w'])
app('h2.i5.twice', 'homework-2: the double delete ran without stopping', M('double* volatile r = new double(1.0); double* a = r; delete a; double* b = r; delete b; std::cout << "ran\\n";'), out('ran\n'), flags=['-w'])
app('h2.i5.at', 'homework-2 prose: EACH snippet ran in this browser build without stopping, v.at(5) included', M('std::vector<double> v(3); double y = v.at(5); std::cout << "ran " << y << "\\n";'), lambda r: r.get('code') == 0 and r['out'].startswith('ran'), flags=['-w'])
app('h2.i5.zero', 'homework-2: new double[0] and delete[] ran without stopping', M('double* s = new double[0]; delete[] s; std::cout << "ran\\n";'), out('ran\n'))
REALLOC = '#include <iostream>\n#include <vector>\nint main() {\n    std::vector<double> px{100.0, 101.0, 102.0};\n    const double& first = px[0];\n    px.push_back(103.0);\n    std::cout << first << "\\n";\n}\n'
app('h2.i6.realloc', "homework-2: with this app's compiler the dangling reference prints a stray tiny number, not 100 (the screen quotes one run, 2.8974e-306; this run gave 2.93542e-306)", REALLOC, lambda r: r.get('code') == 0 and 0 < abs(float(r['out'])) < 1e-300)
def _h2i6():
    rc, m, exe = desk_build(REALLOC, flags=('-g', '-fsanitize=address'))
    e = desk_run(exe)[2]
    return ('heap-use-after-free' in e and 'main.cpp:7' in e, e[:300])
desk('h2.i6.asan', 'homework-2: AddressSanitizer reports heap-use-after-free at the line that prints first (line 4 of the snippet)', _h2i6)
app('h2.i7.off-by-one', 'homework-2 model: in this browser the hardening check stops i <= trades.size() with "vector[] index out of bounds"', M('std::vector<Trade> trades{{"A", 1, 2.0}}; double sum = 0; for (std::size_t i = 0; i <= trades.size(); ++i) sum += trades[i].qty * trades[i].px; std::cout << sum;', 'struct Trade { std::string sym; int qty; double px; };\n'), lambda r: r.get('trap') and 'vector[] index out of bounds' in r.get('err', ''))
app('h2.i7.model-e', 'homework-2 model (e): the four corrected functions compile', HDR + '#include <optional>\nstruct Trade { std::string sym; int qty; double px; };\nstruct Pricer {};\ndouble total_notional(const std::vector<Trade>& trades) {\n    double sum = 0;\n    for (const Trade& t : trades) sum += t.qty * t.px;\n    return sum;\n}\nstd::optional<Trade> best_trade(const std::vector<Trade>& trades) {\n    if (trades.empty()) return std::nullopt;\n    Trade best = trades[0];\n    for (const Trade& t : trades)\n        if (t.qty * t.px > best.qty * best.px) best = t;\n    return best;\n}\nvoid add_fee(Trade& t, double fee) {\n    t.px += fee;\n}\nstd::unique_ptr<Pricer> make_pricer() {\n    return std::make_unique<Pricer>();\n}\nint main() { std::vector<Trade> t{{"A", 2, 3.0}}; add_fee(t[0], 1); std::cout << total_notional(t) << best_trade(t)->sym << (make_pricer() != nullptr) << "\\n"; }\n', out('8A1\n'))
number('h3.numbers', 'homework-3: 15,300 / 300 = 51; (7,650 + 2,800) / 200 = 52.25; slip (15,300 + 2,800) / 350 = 51.7143; 150 x 4 = 600; 150 x -2 = -300; 4 x (10 - 10.25) = -1', lambda: 15300 / 300 == 51 and (150 * 51 + 50 * 56) / 200 == 52.25 and round((15300 + 2800) / 350, 4) == 51.7143 and (50 + 53 + 56) / 3 == 53 and 150 * (55 - 51) == 600 and 150 * (49 - 51) == -300 and 4 * (10 - (30 + 11) / 4) == -1)
RAW = HDR + 'class Prices {\npublic:\n    explicit Prices(int n) : data_(%s) {}\n%s\nprivate:\n    %s data_;\n};\nint main() { Prices a(100); Prices b = a; std::cout << "ran\\n"; }\n'
app('h3.i4.vector', 'homework-3: with a std::vector<double> member and no destructor, copying Prices is safe', RAW % ('n', '', 'std::vector<double>'), out('ran\n'))

# ================================================================== every code widget: solution passes, starter fails
ALL_FILES = ['l1-source-to-program', 'l2-fixed-types', 'l3-branches-and-loops', 'l4-functions-and-headers', 'l5-value-or-reference', 'l6-const', 'l7-addresses', 'l8-stack-and-heap', 'l9-owning-memory', 'l10-invariants', 'l11-creation-destruction', 'l12-operators', 'l13-templates', 'review-1', 'review-2', 'review-3', 'homework-1', 'homework-2', 'homework-3']
def _code_widgets(o, p, acc):
    if isinstance(o, dict):
        if o.get('kind') == 'code' and 'tests' in o:
            acc.append(p)
        for k, v in o.items():
            _code_widgets(v, (p + '.' + k) if p else k, acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _code_widgets(v, '%s.%d' % (p, i), acc)
N_WIDGETS = 0
for _f in ALL_FILES:
    _acc = []
    _code_widgets(load(_f), '', _acc)
    for _p in _acc:
        N_WIDGETS += 1
        _tag = '%s.%s' % (_f.split('-')[0] if _f[0] == 'l' else _f, _p.replace('.widget', '').replace('screens.', 's').replace('items.', 'i'))
        submit('w.%s.solution' % _tag, 'the solution passes every hidden test under the app grader', _f, _p, sol(_f, _p), None)
        submit('w.%s.starter' % _tag, 'the starter fails (a test or the compile)', _f, _p, starter(_f, _p), lambda k: k is not None)

# ================================================================== run
def run_node():
    if not jobs:
        return
    if not PKGS:
        return
    node = shutil.which('node')
    drv = os.path.join(HERE, 'cpp-L1-3-r2-zq.mjs')
    procs = []
    for i in range(NJOBS):
        part = jobs[i::NJOBS]
        if not part:
            continue
        jf, of = os.path.join(TMP, 'jobs%d.json' % i), os.path.join(TMP, 'out%d.json' % i)
        json.dump(part, open(jf, 'w'))
        procs.append((subprocess.Popen([node, '--no-warnings', drv, APP, os.path.abspath(PKGS), jf, of], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), of))
    for p, of in procs:
        p.wait()
        if os.path.exists(of):
            RES.update(json.load(open(of)))

run_node()
fails = []
counts = {}
for cid, kind, claim, fn in checks:
    ok, detail = fn()
    counts[kind] = counts.get(kind, 0) + 1
    if not ok:
        fails.append(cid)
    if not ok or SHOW:
        print('%s %-28s [%s] %s\n      %s' % ('ok  ' if ok else 'FAIL', cid, kind, claim, str(detail)[:1400]))
shutil.rmtree(TMP, ignore_errors=True)
unexpected = sorted(set(fails) - EXPECTED_FAIL)
fixed = sorted(EXPECTED_FAIL - set(fails)) if not ONLY else []
print('%d checks (%s): %d hold, %d fail' % (len(checks), ', '.join('%d %s' % (v, k) for k, v in sorted(counts.items())), len(checks) - len(fails), len(fails)))
print('failing, as the audit records: %s' % ', '.join(sorted(set(fails) & EXPECTED_FAIL)))
if unexpected:
    print('UNEXPECTED failures: %s' % ', '.join(unexpected))
if fixed:
    print('recorded as failing but now hold (content fixed? update EXPECTED_FAIL): %s' % ', '.join(fixed))
# Exit 0 only when every claim holds (correct content). --recorded: exit 0 when exactly the recorded findings fail.
sys.exit((1 if unexpected or fixed else 0) if '--recorded' in ARGV else (1 if fails else 0))
