#!/usr/bin/env python3
"""Concept checks for cpp L1 to L3 (round 1 blind audit, 13 Nov 2026).

Compiles and runs the code-behaviour claims of app/content/courses/cpp (levels 1 to 3).

    python3 docs/reports/cpp-L1-3-concepts.py [--wasm <pkgs folder>]

Native checks use the local g++ and clang++ (x86-64 Linux, libstdc++). Where the app differs
(YoWASP clang 21, wasm32, libc++, -O1: long and size_t are 4 bytes, a vector object is 12 bytes)
the check says so. With --wasm <pkgs> (the local CDN copy that holds yowasp-clang-21.1.4-3) the
claims about "this browser build" are also compiled with the app's own compiler and flags and run
under node:wasi. The wasm probes use -fno-exceptions because the app links its own throw runtime.

Each check encodes a claim the content makes. A check that fails because the content is wrong
stays failing and is a finding in docs/reviews/audit-cpp-1-3.md. The five refuted claims are tied to
their sentence in the content JSON (claim()): once a fix pass removes the sentence, the check passes.
Exit 0 only if every check passes.

Fix pass (13 Nov 2026): the refuted sentences are gone, so their claim() checks report
"[sentence no longer in the content]". New checks cover the replacement text: -Wall -Wextra
-Wconversion silent on h-port-note, a deleted move assignment failing l11 test 10, and, under
--wasm, the null read printing 0, the h-realloc stray value, the template-error length and the
kept `delete book;` compile error.
"""
import os
import shutil
import subprocess
import sys
import tempfile

GXX = shutil.which('g++')
CLANG = shutil.which('clang++')
NODE = shutil.which('node')
WASM = None
if '--wasm' in sys.argv:
    WASM = os.path.join(sys.argv[sys.argv.index('--wasm') + 1], 'yowasp-clang-21.1.4-3', 'package', 'gen', 'bundle.js')
    if not (NODE and os.path.exists(WASM)):
        print('wasm: bundle or node not found, wasm checks skipped')
        WASM = None

TMP = tempfile.mkdtemp(prefix='cppaud-')
results = []
INC = '#include <algorithm>\n#include <cmath>\n#include <iomanip>\n#include <iostream>\n#include <memory>\n#include <stdexcept>\n#include <string>\n#include <tuple>\n#include <type_traits>\n#include <utility>\n#include <vector>\n'


def build(code, cc='g++', flags=(), files=None, name='t'):
    d = tempfile.mkdtemp(dir=TMP)
    srcs = []
    allf = {'main.cpp': code}
    allf.update(files or {})
    for fn, text in allf.items():
        with open(os.path.join(d, fn), 'w') as f:
            f.write(text)
        if fn.endswith('.cpp'):
            srcs.append(fn)
    exe = os.path.join(d, 'a.out')
    p = subprocess.run([cc, '-std=c++17', *flags, *srcs, '-o', exe], cwd=d, capture_output=True, text=True, env=dict(os.environ, LC_ALL='C'))
    return p.returncode, p.stdout + p.stderr, exe


def run(exe, stdin='', env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run([exe], input=stdin, capture_output=True, text=True, env=e, timeout=60)
    return p.returncode, p.stdout, p.stderr


def ok(name, cond, detail=''):
    results.append((name, bool(cond), detail))
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  <- ' + str(detail)[:300].replace('\n', ' | ')))


COURSE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'cpp')


def claimed(fname, needle):
    """True while the content still makes the claim (the JSON text of the file contains the needle)."""
    try:
        return needle in open(os.path.join(COURSE, fname), encoding='utf-8').read()
    except OSError:
        return True


def claim(name, fname, needle, holds, detail=''):
    """holds = what the experiment says about the claim. Fails only while the content still states a claim the run refutes."""
    if not claimed(fname, needle):
        return ok(name + ' [sentence no longer in the content]', True)
    ok(name, holds, detail)


def M(body, pre=''):
    return INC + pre + '\nint main() {\n' + body + '\n}\n'


def out(name, code, expect, cc='g++', flags=(), stdin=''):
    rc, msg, exe = build(code, cc, flags)
    if rc != 0:
        return ok(name, False, 'did not compile: ' + msg)
    r, o, e = run(exe, stdin)
    ok(name, o.strip() == expect.strip(), 'got ' + repr(o) + ' want ' + repr(expect))


def cerr(name, code, needle, cc='clang++', flags=(), files=None):
    rc, msg, _ = build(code, cc, flags, files)
    ok(name, rc != 0 and needle in msg, ('compiled' if rc == 0 else msg))


def cwarn(name, code, needle, cc='clang++', flags=()):
    rc, msg, _ = build(code, cc, flags)
    ok(name, rc == 0 and needle in msg, ('rc=%d ' % rc) + msg)


def compiles(name, code, cc='clang++', flags=(), want=True):
    rc, msg, _ = build(code, cc, flags)
    ok(name, (rc == 0) == want, msg)


def asan(name, code, needle, stdin=''):
    rc, msg, exe = build(code, 'g++', ('-g', '-fsanitize=address'))
    if rc != 0:
        return ok(name, False, msg)
    r, o, e = run(exe, stdin)
    ok(name, needle in e, e[:400])


def wasm(code, flags=('-fno-exceptions',)):
    d = tempfile.mkdtemp(dir=TMP)
    src = os.path.join(d, 'main.cpp')
    open(src, 'w').write(code)
    js = os.path.join(d, 'wrun.mjs')
    open(js, 'w').write(WRUN)
    p = subprocess.run([NODE, '--no-warnings', js, WASM, src, *flags], capture_output=True, text=True, timeout=600)
    lines = [l for l in (p.stdout + p.stderr).splitlines() if 'fetched' not in l]
    return '\n'.join(lines)


WRUN = r'''
import fs from 'node:fs';
import { WASI } from 'node:wasi';
const [bundle, src, ...extra] = process.argv.slice(2);
const { runClang } = await import(bundle);
const FLAGS = ['-std=c++17', '-O1', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_EXTENSIVE', '-D_LIBCPP_ENABLE_EXPERIMENTAL', '-D_LIBCPP_ASSERTION_SEMANTIC=_LIBCPP_ASSERTION_SEMANTIC_ENFORCE', '-fno-color-diagnostics', '-fmessage-length=0', '-ferror-limit=10'];
let out;
try {
  out = await runClang(['clang++', ...FLAGS, ...extra, '-Wl,--stack-first,-z,stack-size=8388608', 'main.cpp', '-o', 'a.wasm'], { 'main.cpp': fs.readFileSync(src, 'utf8') }, { stdout: (b) => b && process.stderr.write(b), stderr: (b) => b && process.stderr.write(b) });
} catch (e) { console.log('COMPILE-FAIL', e.exitCode ?? e.message); process.exit(0); }
const wasi = new WASI({ version: 'preview1', args: ['a'], returnOnExit: true });
const inst = await WebAssembly.instantiate(await WebAssembly.compile(out['a.wasm']), wasi.getImportObject());
try { const rc = wasi.start(inst); console.log('EXIT', rc); } catch (e) { console.log('TRAP', e.message); }
'''

print('compilers:', subprocess.run([GXX, '--version'], capture_output=True, text=True).stdout.splitlines()[0], '|',
      subprocess.run([CLANG, '--version'], capture_output=True, text=True).stdout.splitlines()[0])


# ---------------------------------------------------------------- L1: l1 build and errors
SEMI = '#include <iostream>\n\nint main() {\n    double price = 101.5\n    std::cout << price << \'\\n\';\n    return 0;\n}\n'
cerr('l1 s5 g++ wording for the missing semicolon, reported on line 5', SEMI, "main.cpp:5:5: error: expected ',' or ';' before 'std'", cc='g++')
cerr('l1 s6 clang points at the end of line 4', SEMI, "main.cpp:4:25: error: expected ';' at end of declaration")
rc, msg, exe = build('#include <iostream>\n\nint main() {\n    int qty = 100;\n    std::cout << "Hello, market" << \'\\n\';\n}\n', 'g++', ('-Wall',))
r = run(exe)
ok('l1 s7 -Wall warns about the unused variable, still builds, and main without return exits 0', rc == 0 and "unused variable 'qty' [-Wunused-variable]" in msg and r[0] == 0 and r[1] == 'Hello, market\n', msg)
ASG = '#include <iostream>\nint main() {\n    int signals = 3;\n    if (signals = 0) {\n        std::cout << "flat\\n";\n    }\n    std::cout << signals << \'\\n\';\n}\n'
rc1, m1, e1 = build(ASG, 'g++')
rc2, m2, _ = build(ASG, 'g++', ('-Wall',))
rc3, m3, _ = build(ASG, 'clang++')
ok('l1 s8 if (signals = 0) prints 0; g++ silent by default, warns with -Wall; clang warns by default', rc1 == 0 and m1 == '' and run(e1)[1] == '0\n' and 'warning' in m2 and 'warning' in m3, m1 + m2 + m3)
cerr('l1 quiz0 g++ suggests the name', '#include <iostream>\nint main() {\n    double price = 1;\n    (void)price;\n    std::cout << pirce << \'\\n\';\n}\n', "'pirce' was not declared in this scope; did you mean 'price'?", cc='g++')
cerr('l1 s10 printing a whole vector: g++ says no match for operator<<', '#include <iostream>\n#include <vector>\nint main() {\n    std::vector<double> closes{1.0};\n    std::cout << closes << \'\\n\';\n}\n', "no match for 'operator<<'", cc='g++')
cerr('l1 quiz2 cout without std:: does not compile', '#include <iostream>\nint main() { cout << "hi" << \'\\n\'; }\n', 'cout', cc='g++')
FT = '#include <vector>\nint f(char v) { std::vector<int> c(4, 0); switch (v) { case \'L\': ++c[0]; case \'C\': ++c[1]; break; } return c[1]; }\nint main() {}\n'
rc1, m1, _ = build(FT, 'clang++', ('-Wall',))
rc2, m2, _ = build(FT, 'clang++', ('-Wimplicit-fallthrough',))
ok('l3 s8 fall-through is silent (even with clang -Wall) until -Wimplicit-fallthrough', m1 == '' and 'fallthrough' in m2, m1 + m2)
cwarn('homework-1 h-signedness g++ wording', '#include <vector>\nint main() { std::vector<double> prices; for (int i = 0; i < prices.size(); ++i) { } }\n', "comparison of integer expressions of different signedness: 'int' and 'std::vector<double>::size_type'", cc='g++', flags=('-Wall',))

# ---------------------------------------------------------------- L1: l2 types
out('l2 s0,s6,s8 integer division and one-double rule',
    M('std::cout << 7 / 2 << " " << -7 / 2 << " " << 7.0 / 2 << " " << static_cast<double>(7) / 2 << " " << 3.0 / 4 << " " << 3 / 4 << " " << 3 / 4 * 1.0 << " " << static_cast<double>(3 / 4) << " " << -9 / 4 << "\\n";'),
    '3 -3 3.5 3.5 0.75 0 0 0 -2')
out('l2 s1, quiz2, review-1 r-volume-wrap: wrap value in practice (-fwrapv pins the usual result of this undefined operation)',
    M('volatile int c = 2147483645; int x = c; x = x + 1; x = x + 1; x = x + 1; volatile int v = 1500000000; int y = v; y = y + 1500000000; std::cout << x << " " << y << "\\n";'),
    '-2147483648 -1294967296', flags=('-fwrapv',))
out('l2 s3 auto r = 7 / 2 is int 3; auto r = 7.0 / 2 is double 3.5',
    M('auto r = 7 / 2; auto d = 7.0 / 2; std::cout << std::is_same<decltype(r), int>::value << r << " " << std::is_same<decltype(d), double>::value << d << "\\n";'),
    '13 13.5')
out('l2 s4 average: starter 3, /2.0 form overflows at INT_MAX (wraps to -1 with -fwrapv), cast form is right',
    M('volatile int a = 2147483647, b = 2147483647; int x = a, y = b; std::cout << (3 + 4) / 2 << " " << (x + y) / 2.0 << " " << (static_cast<double>(x) + y) / 2 << " " << (static_cast<double>(-7) + 2) / 2 << "\\n";'),
    '3 -1 2.14748e+09 -2.5', flags=('-fwrapv',))
out('l2 s5 long long product narrowed to int gives -2144967296 (modulo 2^32; guaranteed from C++20, implementation-defined before)',
    M('volatile long long q = 20000, p = 107500; int value = q * p; std::cout << value << " " << q * p << "\\n";'),
    '-2144967296 2150000000')
out('l2 s7 and homework-1 h-pence-truncate: 19.99*100 -> 1998, lround 1999; 0.29*100 -> 28, lround 29',
    M('volatile double p = 19.99, q = 0.29; int a = p * 100; int b = q * 100; std::cout << std::setprecision(17) << p * 100 << " " << a << " " << std::lround(p * 100) << " " << q * 100 << " " << b << " " << std::lround(q * 100) << "\\n";'),
    '1998.9999999999998 1998 1999 28.999999999999996 28 29')
out('l2 quiz0, quiz3: bool prints 1; double share = 1 / 4 is 0',
    M('bool up = 101.5 > 100.0; double share = 1 / 4; std::cout << up << " " << share << " " << sizeof(long long) << sizeof(int) << sizeof(double) << sizeof(bool) << sizeof(char) << "\\n";'),
    '1 0 84811')
out('l2 s9 pnl_pounds rows', M('auto f = [](long long b, long long s, long long q) { long long pence = (s - b) * q; return pence / 100.0; }; std::cout << std::fixed << std::setprecision(2) << f(10150, 10225, 4000) << " " << f(250000, 249000, 3000000) << " " << f(999, 1000, 1) << "\\n";'),
    '3000.00 -30000000.00 0.01')

out('l2 s3 and summary "auto copies the type of the value on the right": auto drops const and never makes a reference (prints 1 1 5)',
    M('const int c = 1; auto d = c; int x = 5; int& r = x; auto a = r; a = 9; std::cout << std::is_same<decltype(d), int>::value << " " << std::is_same<decltype(a), int>::value << " " << x << "\\n";'),
    '1 1 5')

# ---------------------------------------------------------------- L1: l3 loops
out('l3 quiz0, s5: 0.1 + 0.2 != 0.3, and cout shows 0.3 at six significant digits',
    M('volatile double a = 0.1, b = 0.2; std::cout << (a + b == 0.3) << " " << a + b << " " << std::setprecision(17) << a + b << "\\n";'),
    '0 0.3 0.30000000000000004')
out('l3 quiz3 break before ++day; quiz1 six turns; review-1 r-loop-step four turns',
    M('int day = 0; for (double p : {101.0, 97.5, 94.0, 92.0, 99.0}) { if (p < 95) break; ++day; } int t = 0; for (int i = 0; i <= 5; ++i) ++t; int u = 0; for (int i = 3; i < 10; i += 2) ++u; std::cout << day << t << u << "\\n";'),
    '264')
out('l3 quiz2: size() - 1 on an empty vector is the maximum of size_t (about 1.8e19 on this 64-bit build; 4,294,967,295 on wasm32)',
    M('std::vector<double> v; std::cout << (v.size() - 1 == static_cast<std::size_t>(-1)) << " " << (v.size() - 1 > 4000000000u) << "\\n";'),
    '1 1')
cerr('l3 s7: loop variable is out of scope after the for', M('for (int i = 0; i < 5; ++i) { } std::cout << i;'), "undeclared identifier 'i'")
out('l3 s4 max_drawdown solution on the hidden tests',
    M('auto f = [](std::vector<double> ps) { double peak = 0, worst = 0; for (double p : ps) { if (p > peak) peak = p; double fall = (peak - p) / peak; if (fall > worst) worst = fall; } return worst; }; std::cout << f({100,110,99,105,88,95}) << " " << f({}) << " " << f({100,90,95}) << " " << f({100,80,120,60}) << " " << f({10,5,10,2.5}) << "\\n";'),
    '0.2 0 0.1 0.5 0.75')
out('l3 s8 fall-through starter counts each L as Cboe too',
    M('std::vector<int> c(4, 0); for (char v : std::string("LLCT")) { switch (v) { case \'L\': ++c[0]; case \'C\': ++c[1]; break; } } std::cout << c[0] << c[1] << "\\n";'),
    '23')

# ---------------------------------------------------------------- L1: l4 functions
out('l4 s1, s4, quiz0, quiz1: annualise, overloads, function name prints 1',
    M('std::cout << annualise(0.01) << " " << std::fixed << std::setprecision(4) << annualise(0.01, 365) << std::defaultfloat << std::setprecision(6) << " " << mid(10001LL, 10002LL) << " " << mid(100.01, 100.02) << " " << risk_free_rate << "\\n";',
      'double annualise(double v, int days = 252);\ndouble annualise(double v, int days) { return v * std::sqrt(days); }\ndouble mid(double b, double a) { return (b + a) / 2; }\nlong long mid(long long b, long long a) { return (b + a) / 2; }\ndouble risk_free_rate() { return 0.04; }\n'),
    '0.158745 0.1910 10001 100.015 1', flags=('-w',))
cerr('l4 s0: use before declaration (g++ wording on the screen)', M('std::cout << annualise(0.01);') + 'double annualise(double v) { return v; }\n', "'annualise' was not declared in this scope", cc='g++')
cerr('l4 s6: default repeated in the definition', INC + 'double annualise(double v, int days = 252);\ndouble annualise(double v, int days = 252) { return v * std::sqrt(days); }\nint main() {}\n', 'redefinition of default argument')
cerr('l4 s7: body in a header included by two .cpp files is a linker error',
     '#include "returns.h"\nint main() { return simple_return(1, 2) > 0; }\n', 'multiple definition', cc='g++',
     files={'returns.h': '#pragma once\ndouble simple_return(double b, double a) { return (a - b) / b; }\n', 'pricer.cpp': '#include "returns.h"\ndouble g() { return simple_return(1, 2); }\n'})
rc, msg, _ = build('#include "returns.h"\nint main() { return simple_return(1, 2) > 0; }\n', 'g++', (),
                   {'returns.h': '#pragma once\ninline double simple_return(double b, double a) { return (a - b) / b; }\n', 'pricer.cpp': '#include "returns.h"\ndouble g() { return simple_return(1, 2); }\n'})
ok('l4 s7: marking it inline fixes the link', rc == 0, msg)
cerr('l4 s8: default only in the definition, caller sees none',
     '#include "returns.h"\nint main() { return annualise(0.01) > 0; }\n', 'too few arguments', cc='g++',
     files={'returns.h': 'double annualise(double v, int days);\n', 'returns.cpp': '#include <cmath>\ndouble annualise(double v, int days = 252) { return v * std::sqrt(days); }\n'})
cerr('l4 quiz2: declared, called, never linked', 'double annualise(double, int);\nint main() { return annualise(0.01, 252) > 0; }\n', 'undefined reference', cc='g++')

# ---------------------------------------------------------------- L2: l5 references
out('l5 s0, s2, s6, quiz0', M('std::vector<double> mine{250.0, 120.0}; add_fee(mine); double cash = 1000.0; apply_fee(cash, 2.50); std::vector<double> w{2.0, 3.0, 5.0}; normalise(w); int x = 5; int& r = x; int& r2 = r; r2 = 9; std::cout << mine.size() << " " << cash << " " << w[0] << " " << x << "\\n";',
                             'void add_fee(std::vector<double> c) { c.push_back(1.5); }\nvoid apply_fee(double& b, double fee) { b -= fee; }\nvoid normalise(std::vector<double> w) { double s = 0; for (double x : w) s += x; for (double& x : w) x /= s; }\n'),
    '2 997.5 2 9')
cerr('l5 quiz1: plain double& does not bind to 100.0, clang wording', M('apply_fee(100.0, 2.50);', 'void apply_fee(double& b, double fee) { b -= fee; }\n'), 'expects an lvalue for 1st argument')
out('l5 s8, quiz2 and l11 quiz2: a returned local vector is not copied (count copies of a tracked type)',
    M('T g = build(); std::cout << copies << "\\n";', 'int copies = 0;\nstruct T { std::vector<double> v; T() : v(500) {} T(const T& o) : v(o.v) { ++copies; } T(T&& o) noexcept : v(std::move(o.v)) {} };\nT build() { T grid; grid.v[0] = 1; return grid; }\n'),
    '0')
rc, msg, exe = build(M('T g = pick(true); std::cout << copies << "\\n";', 'int copies = 0;\nstruct T { std::vector<double> v; T() : v(500) {} T(const T& o) : v(o.v) { ++copies; } T(T&& o) noexcept : v(std::move(o.v)) {} };\nT pick(bool up) { T a, b; return up ? a : b; }\n'))
r = run(exe)
claim('l11 quiz2 feedback "Returning a local by value never copies it": a local returned through ?: is copied', 'l11-creation-destruction.json',
      'Returning a local by value never copies it', r[1].strip() == '0', 'copies made by return up ? a : b; = ' + r[1].strip())

# ---------------------------------------------------------------- L2: l6 const
cerr('l6 s0 clang wording', M('const double tick = 0.01; tick = 0.05;'), "cannot assign to variable 'tick' with const-qualified type 'const double'")
cerr('l6 s1 clang wording', INC + 'double with_fee(const double& px, double fee) { double out = px; out += fee; px += fee; fee = 0; return out; }\nint main() {}\n', "cannot assign to variable 'px' with const-qualified type 'const double &'")
PRE_MEAN = 'double mean(std::vector<double>& v) { return v.size(); }\n'
compiles('l6 s2 mean(prices) compiles with a plain reference', M('std::vector<double> prices{101.5, 99.0}; mean(prices);', PRE_MEAN))
cerr('l6 s2 mean(fixed): clang says "would lose const qualifier"', M('const std::vector<double> fixed{100.0, 100.5}; mean(fixed);', PRE_MEAN), 'would lose const qualifier')
cerr('l6 s2 option temp: clang says it "expects an lvalue" for mean({101.5, 99.0})', M('mean({101.5, 99.0});', PRE_MEAN), 'expects an lvalue')
compiles('l6 s2 explain: all three compile with const&', M('std::vector<double> prices{101.5, 99.0}; const std::vector<double> fixed{100.0, 100.5}; mean(prices); mean({101.5, 99.0}); mean(fixed);', 'double mean(const std::vector<double>& v) { return v.size(); }\n'))
PRE_Q = 'struct Quote { double bid, ask; double mid() const { return (bid + ask) / 2; } void widen(double by) { bid -= by; ask += by; } };\n'
compiles('l6 s3 const object: mid() and reading bid compile', M('const Quote q{99.98, 100.02}; double m = q.mid(); double b = q.bid; (void)m; (void)b;', PRE_Q))
cerr('l6 s3 widen on a const Quote', M('const Quote q{99.98, 100.02}; q.widen(0.01);', PRE_Q), 'function is not marked const')
cerr('l6 s3 assign to member of const Quote', M('const Quote q{99.98, 100.02}; q.ask = 100.05;', PRE_Q), 'cannot assign')
cerr('l6 s5 constexpr from a run-time call', INC + 'constexpr int lot_size = 100;\nconstexpr double tick = 0.01;\nconstexpr double min_fee = tick * lot_size;\ndouble read_tick();\nconstexpr double live_tick = read_tick();\nint main() {}\n', "constexpr variable 'live_tick' must be initialized by a constant expression")
compiles('l6 s5 the other five lines compile', INC + 'constexpr int lot_size = 100;\nconstexpr double tick = 0.01;\nconstexpr double min_fee = tick * lot_size;\ndouble read_tick() { return 0.01; }\nconst double start_tick = read_tick();\nint main() {}\n')
out('l6 s6 const view sees the change', M('std::vector<double> px{100.0, 101.0}; const std::vector<double>& view = px; px[0] = 99.0; std::cout << view[0] << "\\n";'), '99')
cerr('l6 s7 clang wording for px[i] += fee through const&', INC + 'std::vector<double> with_fees(const std::vector<double>& px, double fee) {\n    for (std::size_t i = 0; i < px.size(); ++i)\n        px[i] += fee;\n    return px;\n}\nint main() {}\n', "cannot assign to return value because function 'operator[]' returns a const value")
cerr('l6 s10 clang wording for double* const', M('double x = 1, y = 2; double* const p = &x; p = &y;'), "cannot assign to variable 'p' with const-qualified type 'double *const'")
compiles('l6 s10 const double* p: p = &y is fine', M('double x = 1, y = 2; const double* p = &x; p = &y; (void)p;'))
cerr('l6 s10 const double* p: *p = 3 fails', M('double x = 1; const double* p = &x; *p = 3;'), 'read-only variable is not assignable')
cerr('l6 quiz2 clang wording', INC + 'struct Position { int qty; };\nvoid report(const Position& p) { p.qty = 0; }\nint main() {}\n', "cannot assign to variable 'p' with const-qualified type 'const Position &'")

# ---------------------------------------------------------------- L2: l7 pointers
out('l7 s0, s1, s7, quiz1, quiz3, s9 sizeof(Level)',
    M('int qty = 300; int* p = &qty; *p = 500; std::vector<double> px{101.50, 101.25, 101.75, 102.00}; double* q = &px[1]; double a = 5.0, b = 5.0; int x = 1; int* xp = &x; int** pp = &xp; **pp = 7; int arr[4]; std::cout << qty << " " << *(q + 2) << " " << (reinterpret_cast<char*>(q + 2) - reinterpret_cast<char*>(q)) << " " << (&a == &b) << " " << x << " " << (reinterpret_cast<char*>(arr + 3) - reinterpret_cast<char*>(arr)) << " " << sizeof(Level) << "\\n";',
      'struct Level { double px; long long size; };\n'),
    '500 102 16 0 7 12 16')
cwarn('l7 quiz2 and homework-2 model: clang warns, still builds', INC + 'double* best_bid() { double x = 101.25; return &x; }\nint main() {}\n', "address of stack memory associated with local variable 'x' returned")
asan('l7 s6: g++ AddressSanitizer names stack-use-after-scope',
     '#include <iostream>\nint main() {\n    double* p = nullptr;\n    {\n        double bid = 101.25;\n        p = &bid;\n    }\n    std::cout << *p << "\\n";\n}\n', 'stack-use-after-scope')
asan('l7 quiz0: null read is SEGV on address 0 under AddressSanitizer', '#include <iostream>\nint main() { int* volatile p = nullptr; std::cout << *p << "\\n"; }\n', 'SEGV on unknown address 0x000000000000')

# ---------------------------------------------------------------- L2: l8 stack and heap
LEAK = '#include <iostream>\ndouble sum_prices(int n) {\n    double* prices = new double[n];\n    double total = 0;\n    for (int i = 0; i < n; ++i) { prices[i] = 100 + i; total += prices[i]; }\n    return total;\n}\nint main() { std::cout << sum_prices(1000) << "\\n"; }\n'
asan('l8 s4: LeakSanitizer reports 8000 bytes in 1 object', LEAK, 'Direct leak of 8000 byte(s) in 1 object(s)')
asan('l8 s5: alloc-dealloc-mismatch', 'int main() { double* volatile px = new double[1000]; delete px; }\n', 'alloc-dealloc-mismatch (operator new [] vs operator delete)')
cwarn('l8 s5: clang warns at compile time', 'int main() {\n    double* px = new double[1000];\n    delete px;\n}\n', "'delete' applied to a pointer that was allocated with 'new[]'; did you mean 'delete[]'?")
rc, msg, exe = build('int main() { double price = 101.25; double* p = &price; delete p; }\n', 'g++', ('-O1',))
r = run(exe) if rc == 0 else (0, '', '')
ok('l8 quiz0: g++ warns "called on unallocated object \'price\'" and the run aborts with free(): invalid pointer',
   "called on unallocated object 'price'" in msg and 'invalid pointer' in r[2], msg + r[2])
out('l8 quiz1: new double[0] is non-null', M('double* p = new double[0]; std::cout << (p != nullptr) << "\\n"; delete[] p;'), '1')
asan('review-2 r-which-ub, homework-2 h-which-ub: double delete is reported as double-free', 'int main() { double* volatile r = new double(1.0); delete r; delete r; }\n', 'double-free')
asan('homework-2 h-realloc: heap-use-after-free after push_back on a full vector', M('std::vector<double> px{100.0, 101.0, 102.0}; const double& first = px[0]; px.push_back(103.0); std::cout << first << "\\n";'), 'heap-use-after-free')
out('l8 s3 explain: a vector object is 24 bytes on a 64-bit desk', M('std::cout << sizeof(std::vector<double>) << "\\n";'), '24')

# ---------------------------------------------------------------- L2: l9 owning memory
POS = 'struct Position { std::string sym; int qty; Position(std::string s, int q = 0) : sym(s), qty(q) { std::cout << "open " << sym << "\\n"; } ~Position() { std::cout << "close " << sym << "\\n"; } };\n'
out('l9 s0 output order', M('trade(); std::cout << "done\\n";', POS + 'void trade() { Position p("VOD"); std::cout << "trading\\n"; }\n'), 'open VOD\ntrading\nclose VOD\ndone')
cerr('l9 s3 hint 3 says a kept "delete book;" would free the Book twice: in fact it does not compile',
     M('auto book = std::make_unique<int>(); delete book;'), 'cannot delete expression of type')
claim('l9 s3 hint 3 claim "Remove delete book;, or the object would be freed twice" (it is a compile error, so no double free can happen)', 'l9-owning-memory.json', 'or the object would be freed twice', False,
   "clang: cannot delete expression of type 'std::unique_ptr<int>'; g++: type 'class std::unique_ptr<int>' argument given to 'delete', expected pointer")
cerr('l9 s4 copying a unique_ptr does not compile (libstdc++ wording differs; the screen quotes libc++, checked under --wasm)', M('auto a = std::make_unique<int>(1); auto b = a;'), 'deleted')
cerr('l9 s4 option get: raw pointer does not convert to unique_ptr', M('auto a = std::make_unique<int>(1); book_order(a.get());', 'void book_order(std::unique_ptr<int> o) {}\n'), 'no matching function')
out('l9 s6 use_count 1, 3, 1', M('auto a = std::make_shared<int>(); std::cout << a.use_count(); { auto b = a; auto c = b; std::cout << a.use_count(); } std::cout << a.use_count() << "\\n";'), '131')
CYC = INC + 'struct Node { std::shared_ptr<Node> other; ~Node() { std::cout << "freed\\n"; } };\nint main() { { auto a = std::make_shared<Node>(); auto b = std::make_shared<Node>(); a->other = b; b->other = a; } std::cout << "end of main\\n"; }\n'
out('l9 s7 cycle prints only end of main', CYC, 'end of main')
asan('l9 s7 LeakSanitizer: 64 bytes in 2 allocations', CYC, '64 byte(s) leaked in 2 allocation(s)')
HOLD = POS + 'void hold(std::unique_ptr<Position> p) { std::cout << "hold " << p->qty << "\\n"; }\n'
out('l9 s9 output order', M('auto p = std::make_unique<Position>("VOD", 100); std::cout << "opened\\n"; hold(std::move(p)); std::cout << (p == nullptr) << " after hold\\n";', HOLD),
    'open VOD\nopened\nhold 100\nclose VOD\n1 after hold')
rc, msg, exe = build(M('auto p = std::make_unique<Position>("VOD", 100); (hold(std::move(p)), std::cout << "same statement\\n");', HOLD))
print('info  l9 s9 line o4 "the parameter dies at its }": implementation-defined (C++17 [expr.call]/4). This x86-64 build prints',
      repr(run(exe)[1]), '(the parameter outlives the call, to the end of the full expression); the app build destroys it at the }, see --wasm')
out('l9 quiz0, quiz1', M('auto a = std::make_unique<double>(101.5); auto b = std::move(a); auto px = std::make_unique<double[]>(3); std::cout << (a == nullptr) << " " << *b << " " << px[0]; px[2] = 101.5; std::cout << " " << px[2] << "\\n";'), '1 101.5 0 101.5')
cerr('l9 quiz3 push_back(o) copies', M('std::vector<std::unique_ptr<int>> book; auto o = std::make_unique<int>(); book.push_back(o);'), 'deleted')

# ---------------------------------------------------------------- L3: l10 invariants
out('l10 s0, s7, quiz0 print -0.2', M('struct Q { double bid; double ask; }; Q q{100.2, 100.4}; q.bid = 100.6; std::cout << q.ask - q.bid << "\\n";'), '-0.2')
cerr('l10 s2 clang wording', INC + 'class Quote {\npublic:\n    Quote(double bid, double ask) : bid_(bid), ask_(ask) {}\nprivate:\n    double bid_;\n    double ask_;\n};\nint main() { Quote q(100.2, 100.4); q.bid_ = 100.6; }\n', "'bid_' is a private member of 'Quote'")
LIM = INC + 'class Limit {\npublic:\n    Limit(double m) {\n        max_ = m;\n    }\nprivate:\n    const double max_;\n};\nint main() { Limit l(5e6); }\n'
cerr('l10 s6 first clang error', LIM, "constructor for 'Limit' must explicitly initialize the const member 'max_'")
cerr('l10 s6 second clang error', LIM, "cannot assign to non-static data member 'max_' with const-qualified type 'const double'")
cerr('l10 s6 option local: the first error remains', INC + 'class Limit { public: Limit(double m) { const double max_ = m; } private: const double max_; };\nint main() { Limit l(5e6); }\n', "must explicitly initialize the const member 'max_'")
out('l10 s5 Position table and test 9 NaN, quiz3, homework-3 h-avg-chain',
    M('int q = 0; double avg = 0; auto buy = [&](int n, double px) { avg = (q * avg + n * px) / (q + n); q += n; }; buy(100, 10); buy(300, 12); std::cout << avg << " "; q = 0; avg = 0; buy(0, 10.0); std::cout << std::isnan(avg) << " "; q = 0; avg = 0; buy(200, 5); buy(50, 6); std::cout << avg << " "; q = 0; avg = 0; buy(200, 50); buy(100, 53); q -= 150; buy(50, 56); std::cout << avg << "\\n";'),
    '11.5 1 5.2 52.25')

# ---------------------------------------------------------------- L3: l11 creation and destruction
LOG = 'struct Logger { std::string name; Logger(std::string n) : name(n) { std::cout << "open " << name << "\\n"; } ~Logger() { std::cout << "close " << name << "\\n"; } };\n'
out('l11 s0, s2 destruction order', M('Logger a("a"); { Logger b("b"); std::cout << "work\\n"; } Logger c("c");', LOG), 'open a\nopen b\nwork\nclose b\nopen c\nclose c\nclose a')
out('l11 s5 copy prints close a twice; quiz0 temporary dies at the semicolon', M('{ Logger a("a"); Logger b = a; } Logger("tmp"); std::cout << "next\\n";', LOG), 'open a\nclose a\nclose a\nopen tmp\nclose tmp\nnext')
WIN = '#include <vector>\n\nclass Window {\npublic:\n    Window(int n) : n_(n), data_(n_, 0.0) {}\nprivate:\n    std::vector<double> data_;\n    int n_;\n};\n\nint main() {\n    Window w(20);\n}\n'
cwarn('l11 s4 -Wall: reorder warning', WIN, "field 'n_' will be initialized after field 'data_'", flags=('-Wall',))
cwarn('l11 s4 -Wall: uninitialised use', WIN, "field 'n_' is uninitialized when used here", flags=('-Wall',))
out('l11 quiz3, review-3 r-desk-order: declaration order wins',
    M('{ Desk d; }', LOG + 'class Desk { Logger risk_; Logger feed_; public: Desk() : feed_("feed"), risk_("risk") { std::cout << "desk open\\n"; } ~Desk() { std::cout << "desk close\\n"; } };\n'),
    'open risk\nopen feed\ndesk open\ndesk close\nclose feed\nclose risk', flags=('-w',))
BUF = 'struct B4 { std::vector<double> d; B4(int n, double x) : d(n, x) {} B4(const B4&) = default; B4(B4&&) = default; B4& operator=(const B4&) = default; B4& operator=(B4&&) = default; };\n' \
      'struct CopyCtorOnly { std::vector<double> d; CopyCtorOnly(int n, double x) : d(n, x) {} CopyCtorOnly(const CopyCtorOnly&) = default; };\n' \
      'struct MoveCtorOnly { std::vector<double> d; MoveCtorOnly(int n, double x) : d(n, x) {} MoveCtorOnly(MoveCtorOnly&&) = default; };\n' \
      'struct BothCtors { std::vector<double> d; BothCtors(int n, double x) : d(n, x) {} BothCtors(const BothCtors&) = default; BothCtors(BothCtors&&) = default; };\n' \
      'struct NoMoveAssign { std::vector<double> d; NoMoveAssign(int n, double x) : d(n, x) {} NoMoveAssign(const NoMoveAssign&) = default; NoMoveAssign(NoMoveAssign&&) = default; NoMoveAssign& operator=(const NoMoveAssign&) = default; };\n'
out('l11 s7 feedback test-9: a declared move constructor deletes the copy assignment',
    M('std::cout << std::is_copy_assignable_v<MoveCtorOnly> << std::is_copy_assignable_v<BothCtors> << std::is_copy_assignable_v<B4> << "\\n";', BUF), '001')
rc, msg, exe = build(M('std::cout << std::is_move_assignable_v<CopyCtorOnly> << "\\n";', BUF))
r = run(exe)
claim('l11 s7 feedback test-10 names "a declared copy constructor" as the cause of failing is_move_assignable: with only a copy constructor declared the class IS move assignable (the copy assignment serves)',
      'l11-creation-destruction.json', 'Test 10 moves into an existing buffer. A declared copy constructor stops the compiler writing the move assignment', r[1].strip() == '0', 'is_move_assignable_v<CopyCtorOnly> = ' + r[1].strip() + ' (test 10 would pass, so this feedback never matches its cause)')
out('l11 s7 fixed feedback test-10: a deleted move assignment fails is_move_assignable (test 10) while test 9 still passes',
    M('std::cout << std::is_copy_assignable_v<DelMove> << std::is_move_assignable_v<DelMove> << "\\n";', BUF + 'struct DelMove { std::vector<double> d; DelMove(int n, double x) : d(n, x) {} DelMove(const DelMove&) = default; DelMove(DelMove&&) = default; DelMove& operator=(const DelMove&) = default; DelMove& operator=(DelMove&&) = delete; };\n'), '10')
out('l11 s7 feedback test-12: copy, move, copy-assign declared but no move assignment: "move" into an existing object copies',
    M('NoMoveAssign a(3, 1.5), c(1, 0.0); c = std::move(a); std::cout << std::is_move_assignable_v<NoMoveAssign> << a.d.size() + 10 * c.d.size() << "\\n";', BUF), '133')
out('l11 s7: moved-from vector is empty after move construction and move assignment (libstdc++; the standard guarantees it only for construction)',
    M('std::vector<double> a(3, 1.5); std::vector<double> b = std::move(a); std::vector<double> c(3, 1.0), d(1, 0.0); d = std::move(c); std::cout << a.size() << c.size() << "\\n";'), '00')
out('l11 quiz1: std::move of a const object copies', M('const B4 a(3, 1.5); B4 b = std::move(a); std::cout << a.d.size() << "\\n";', BUF), '3')
asan('l11 s8: copying a raw-pointer owner double-frees', 'class Prices { public: explicit Prices(int n) : data_(new double[n]) {} ~Prices() { delete[] data_; } private: double* data_; };\nint main() { Prices a(100); Prices b = a; }\n', 'double-free')
compiles('l11 s9 and review-3 r-move-unique: a unique_ptr member makes the class move-only',
         M('static_assert(!std::is_copy_constructible_v<Pricer> && !std::is_copy_assignable_v<Pricer> && std::is_move_constructible_v<Pricer>); Pricer a("binomial"); Pricer b = std::move(a);', 'struct Lattice {};\nclass Pricer { std::string name_; std::unique_ptr<Lattice> grid_; public: explicit Pricer(std::string n) : name_(n) {} };\n'))

# ---------------------------------------------------------------- L3: l12 operators
cerr('l12 s0 clang wording', INC + 'class Money { public: explicit Money(long long p) : pence_(p) {} private: long long pence_; };\nint main() { Money fee(250), tax(50); Money total = fee + tax; }\n', "invalid operands to binary expression ('Money' and 'Money')")
out('l12 s1 first-try table',
    M('for (long long p : {1234LL, 1205LL, 1200LL, 7LL, 99LL, -150LL}) std::cout << "£" + std::to_string(p / 100) + "." + std::to_string(p % 100) << " "; std::cout << "\\n";'),
    '£12.34 £12.5 £12.0 £0.7 £0.99 £-1.-50')
MONEY = 'class Money { public: explicit Money(long long pence) : pence_(pence) {} long long pence() const { return pence_; } std::string str() const { long long p = pence_ < 0 ? -pence_ : pence_; std::string c = std::to_string(p % 100); if (c.size() < 2) c = "0" + c; std::string s = pence_ < 0 ? "-" : ""; return s + "£" + std::to_string(p / 100) + "." + c; } private: long long pence_; };\nMoney operator+(Money a, Money b) { return Money(a.pence() + b.pence()); }\nMoney operator*(Money m, int k) { return Money(m.pence() * k); }\n'
out('l12 s2 tests and quiz3', M('std::cout << Money(1205).str() << " " << Money(7).str() << " " << Money(-5).str() << " " << (Money(100) + Money(-250)).str() << " " << (Money(-375) * 2).str() << " " << Money(123456789).str() << "\\n";', MONEY),
    '£12.05 £0.07 -£0.05 -£1.50 -£7.50 £1234567.89')
cerr('l12 s3: 3 * fee with a member operator*', INC + 'class Money { public: explicit Money(long long p) : pence_(p) {} Money operator*(int k) const { return Money(pence_ * k); } private: long long pence_; };\nint main() { Money fee(250); Money a = fee * 3; Money b = 3 * fee; }\n', "invalid operands to binary expression ('int' and 'Money')")
out('l12 s5 a plus that writes', M('Money cash{1000}, fee{250}; Money total = cash + fee; std::cout << cash.pence << " " << total.pence << "\\n";', 'struct Money { long long pence; };\nMoney& operator+(Money& a, Money b) { a.pence += b.pence; return a; }\n'), '1250 1250')
cerr('l12 s4, quiz2: taking std::ostream by value needs the deleted copy constructor', INC + 'struct Money { std::string str() const { return "x"; } };\nstd::ostream& operator<<(std::ostream os, const Money& m) { os << m.str(); return os; }\nint main() { std::cout << Money() << "\\n"; }\n', 'deleted')
out('l12 s6 and quiz0', M('volatile double x = 0.1, y = 0.2; Price fill{x + y}, limit{0.3}; Px a{100, "LSE"}, b{100, "CBOE"}; std::cout << (fill == limit) << " " << (a < b) << (b < a) << (a == b) << "\\n";',
                          'struct Price { double px; };\nbool operator==(Price a, Price b) { return a.px == b.px; }\nstruct Px { long long pence; std::string venue; };\nbool operator<(const Px& a, const Px& b) { return a.pence < b.pence; }\nbool operator==(const Px& a, const Px& b) { return a.pence == b.pence && a.venue == b.venue; }\n'),
    '0 000')
cerr('l12 quiz1: no operator+ for Pnl and Quantity', INC + 'struct Pnl { long long pence; };\nstruct Quantity { int shares; };\nPnl operator+(Pnl a, Pnl b) { return Pnl{a.pence + b.pence}; }\nint main() { Pnl day{12500}; Quantity filled{300}; Pnl oops = day + filled; }\n', 'invalid operands')
ORD = 'struct Order { std::string id; long long price; int time; };\n'
out('l12 s9 ask priority B, C, A', M('std::vector<Order> b{{"A", 10100, 3}, {"B", 10050, 5}, {"C", 10100, 1}}; std::sort(b.begin(), b.end()); for (auto& o : b) std::cout << o.id; std::cout << "\\n";', ORD + 'bool operator<(const Order& a, const Order& b) { return std::tie(a.price, a.time) < std::tie(b.price, b.time); }\n'), 'BCA')
out('review-3 r-bid-priority: tie(b.price, a.time) < tie(a.price, b.time) is price descending, time ascending', M('std::vector<Order> b{{"A", 10100, 3}, {"B", 10050, 5}, {"C", 10100, 1}, {"D", 10150, 9}}; std::sort(b.begin(), b.end()); for (auto& o : b) std::cout << o.id; std::cout << "\\n";', ORD + 'bool operator<(const Order& a, const Order& b) { return std::tie(b.price, a.time) < std::tie(a.price, b.time); }\n'), 'DCAB')
out('l12 summary "compare whole pence, never doubles" and l13 max_of over doubles: < on doubles orders them correctly (only == is the trap)',
    M('std::vector<double> v{101.25, 101.0, 101.5}; std::sort(v.begin(), v.end()); std::cout << v[0] << " " << v[2] << "\\n";'), '101 101.5')

# ---------------------------------------------------------------- L3: l13 templates
BIG = 'template <typename T>\nT bigger(T a, T b) {\n    return a < b ? b : a;\n}\n'
cerr('l13 s3 clang note wording', INC + BIG + 'int main() { double x = bigger(3, 2.5); }\n', "candidate template ignored: deduced conflicting types for parameter 'T' ('int' vs. 'double')")
out('l13 s3 options: bigger<double>(3, 2.5) is 3; bigger<int>(3, 2.5) turns 2.5 into 2; bigger(2, 2.5) cases', M('std::cout << bigger<double>(3, 2.5) << " " << bigger<int>(2, 2.5) << " " << bigger<double>(2, 2.5) << "\\n";', BIG), '3 2 2.5', flags=('-w',))
cerr('l13 s3 option two: bigger<int, double> does not compile', INC + BIG + 'int main() { bigger<int, double>(3, 2.5); }\n', 'no matching function')
SER = 'template <typename T>\nclass Series {\npublic:\n    void push(T x) { xs_.push_back(x); }\n    T mean() const {\n        T total{};\n        for (const T& x : xs_) total += x;\n        return total / xs_.size();\n    }\nprivate:\n    std::vector<T> xs_;\n};\n'
compiles('l13 s5 Series<std::string> builds while mean is never called', M('Series<std::string> names; names.push("AZN"); names.push("BARC");', SER))
cerr('l13 s5 and adding names.mean() fails', M('Series<std::string> names; names.push("AZN"); names.mean();', SER), 'invalid operands to binary expression')
out('l13 s6 Series<int> mean is 2000; a negative total turns into a huge unsigned number before the division (on this 64-bit build the narrowing back to int happens to give -3; on wasm32 it gives 2147483645, checked under --wasm)', M('Series<int> v; v.push(1500); v.push(2501); std::vector<int> xs{-10, 4}; int total = -6; std::cout << v.mean() << " " << (total / xs.size() > 4000000000u) << "\\n";', SER), '2000 1', flags=('-w',))
MAXOF = 'template <typename T>\nT max_of(const std::vector<T>& xs) { T best = xs[0]; for (const T& x : xs) if (best < x) best = x; return best; }\ntemplate <typename T>\nT sum_of(const std::vector<T>& xs) { T total{}; for (const T& x : xs) total += x; return total; }\n'
out('l13 quiz0, s2, quiz3', M('std::cout << max_of(std::vector<std::string>{"BARC", "AZN", "VOD", "LLOY"}) << " " << sum_of(std::vector<double>{0.5, 0.25}) << " " << sum_of(std::vector<std::string>{"BA", "RC"}) << " [" << sum_of(std::vector<std::string>{}) << "] " << sum_of(std::vector<double>{}) << " " << sum_of(std::vector<long long>{3000000000LL, 3000000000LL}) << "\\n";', MAXOF),
    'VOD 0.75 BARC [] 0 6000000000')
rc, msg, exe = build(M('std::cout << (std::string("Zebra") < std::string("apple")) << (std::string("VOD") < std::string("bp")) << "\\n";'))
r = run(exe)
claim('l13 quiz0 calls std::string < "alphabetical order": it is character-code order, so "Zebra" < "apple" and "VOD" < "bp" are both true', 'l13-templates.json',
      'alphabetical order, so the template compiles', r[1].strip() == '00', 'got ' + r[1].strip() + '; alphabetical order would give 00')
cerr('l13 quiz2: template defined in stats.cpp only gives an undefined reference',
     '#include "stats.h"\nint main() { return sum_of(std::vector<double>{1.0}) > 0; }\n', 'undefined reference', cc='g++',
     files={'stats.h': '#include <vector>\ntemplate <typename T> T sum_of(const std::vector<T>&);\n', 'stats.cpp': '#include "stats.h"\ntemplate <typename T> T sum_of(const std::vector<T>& xs) { T t{}; for (const T& x : xs) t += x; return t; }\n'})
rc, msg, _ = build('#include "stats.h"\ndouble g();\nint main() { return sum_of(std::vector<double>{1.0}) + g() > 0; }\n', 'g++', (),
                   {'stats.h': '#pragma once\n#include <vector>\ntemplate <typename T> T sum_of(const std::vector<T>& xs) { T t{}; for (const T& x : xs) t += x; return t; }\n', 'other.cpp': '#include "stats.h"\ndouble g() { return sum_of(std::vector<double>{2.0}); }\n'})
ok('l13 quiz2 and l4 summary (fix text of finding 10): a template body in a header included by two .cpp files links cleanly', rc == 0, msg)
out('l13 s9 Window tests', M('auto mean = [](std::vector<double> in, int n) { std::vector<double> xs; for (double x : in) { xs.push_back(x); if ((int)xs.size() > n) xs.erase(xs.begin()); } double t{}; for (double x : xs) t += x; return t / static_cast<double>(xs.size()); }; std::cout << mean({100, 101, 102, 106}, 3) << " " << mean({1500, 2500, 1200}, 2) << " " << mean({0.1, 0.2}, 5) << " " << mean({5, 9, 7}, 1) << "\\n";'),
    '103 1850 0.15 7')

# ---------------------------------------------------------------- homework
PORT = '#include <vector>\ndouble f(const std::vector<int>& fills, int n_fills) {\n    int total_qty = 0;\n    for (int q : fills) {\n        total_qty += q;\n    }\n    double avg = total_qty / n_fills;\n    return avg;\n}\nint main() {}\n'
for cc in ('g++', 'clang++'):
    rc, msg, _ = build(PORT, cc, ('-Wall', '-Wconversion'))
    claim('homework-1 h-port-note model: "-Wall -Wconversion also flags the implicit conversions" (%s)' % cc, 'homework-1.json', 'also flags the implicit conversions', rc == 0 and 'warning' in msg, 'no warning at all on the snippet: ' + repr(msg))
    rc, msg, _ = build(PORT, cc, ('-Wall', '-Wextra', '-Wconversion'))
    ok('homework-1 h-port-note fixed model: "g++ and clang print nothing for this code, even with -Wall -Wextra -Wconversion" (%s)' % cc, rc == 0 and msg == '', msg)
if shutil.which('clang-tidy'):
    d = tempfile.mkdtemp(dir=TMP)
    open(os.path.join(d, 'port.cpp'), 'w').write(PORT)
    t = subprocess.run(['clang-tidy', '-checks=-*,bugprone-integer-division', 'port.cpp', '--', '-std=c++17'], cwd=d, capture_output=True, text=True)
    ok('homework-1 h-port-note proposed fix text: clang-tidy bugprone-integer-division flags the division', 'bugprone-integer-division' in t.stdout, t.stdout + t.stderr)
rc, msg, exe = build('#include <iostream>\nint main() { volatile int a = 1500000000; int t = a; t += 1500000000; std::cout << t << "\\n"; }\n', 'g++', ('-fsanitize=undefined',))
r = run(exe)
ok('homework-1 h-port-note model: -fsanitize=undefined reports the overflow at run time', 'signed integer overflow' in r[2], r[2])
TICK = 'long long sv(const std::vector<int>& p, const std::vector<int>& s) { long long t = 0; int sign = 0; for (std::size_t i = 1; i < p.size(); ++i) { if (p[i] > p[i - 1]) sign = 1; else if (p[i] < p[i - 1]) sign = -1; t += sign * static_cast<long long>(s[i]); } return t; }\n'
out('homework-1 h-tick-rule keys',
    M('std::cout << sv({100,101,101,100,102},{500,200,300,400,100}) << " " << sv({250,250,249,249,249},{10,20,30,40,50}) << " " << sv({10,11,11,11,10,10,12},{1,2,4,8,16,32,64}) << " " << sv({100,102,101,103},{1,10,100,1000}) << " " << sv({500,499,499,500,500},{3,5,7,11,13}) << " " << sv({100,99,98,97},{1,2000000000,2000000000,2000000000}) << " "'
      ' << sv({1000,1000,999,1000,1000,1000,1001,1001,1001,1000,1001,1000,1000,1001,1001,1001,1001,1001,1001,1001,1001,1002,1003,1003,1004,1003,1003,1003,1003,1003},{1220090042,1815798291,975276522,285684284,637597906,679612584,765803393,1359989501,1026567591,1645564874,382876012,990094599,300688620,1186044220,1857707033,403768909,713875110,1494184151,171550329,123240266,310910996,1315246591,1988192705,1474835736,511366050,127174085,837470696,553145839,526341835,1763063502}) << "\\n";', TICK),
    '200 -120 30 910 12 -6000000000 8970232795')
out('homework-2 h-frames prints 7.5; h-vwap figures',
    M('auto payoff = [](double s, double k) { return s > k ? s - k : 0; }; std::cout << 0.5 * payoff(100 * 1.1, 95) + 0.5 * payoff(100 * 0.9, 95) << " " << std::fixed << std::setprecision(4) << (500 * 101.25 + 300 * 101.40 + 400 * 101.10) / 1200 << " " << (1000 * 4.85 + 500 * 4.88) / 1500 << " " << (1 * 100 + 2 * 100.0001) / 3 << "\\n";'),
    '7.5 101.2375 4.8600 100.0001')
out('homework-1 h-csv-drawdown test 4 prints 24.00', M('double worst = (262.50 - 199.50) / 262.50; std::cout << std::fixed << std::setprecision(2) << worst * 100 << " " << std::stod("100.00\\r") << "\\n";'), '24.00 100.00')
out('homework-3 h-session-range: width of an int range through double is exact', M('int lo = -2000000000, hi = 2000000000; std::cout << std::fixed << std::setprecision(0) << static_cast<double>(hi) - static_cast<double>(lo) << "\\n";'), '4000000000')

# ---------------------------------------------------------------- the app's own compiler (optional)
if WASM:
    o = wasm('#include <iostream>\n#include <vector>\n#include <string>\nstruct Level { double px; long long size; };\nint main() { std::vector<double> v; std::cout << sizeof(int) << sizeof(long) << sizeof(long long) << sizeof(double) << sizeof(bool) << sizeof(char) << sizeof(std::size_t) << " " << sizeof(std::vector<double>) << " " << sizeof(Level) << " " << v.size() - 1 << "\\n"; }\n')
    ok('wasm: l2 s2 table sizes (int 4, long long 8, double 8, bool 1, char 1); vector object 12 bytes; Level 16; size_t max 4294967295 (l3 s3 "about 4 billion")', '4488114 12 16 4294967295' in o, o)
    o = wasm('#include <iostream>\nint main() {\n    double prices[2000000];\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";\n}\n')
    ok('wasm: l8 s0 program A (16 MB local array) stops with "memory access out of bounds"', 'out of bounds' in o, o)
    o = wasm('#include <iostream>\n#include <vector>\nint main() {\n    std::vector<double> prices(2000000);\n    for (int i = 0; i < 2000000; ++i) prices[i] = 101;\n    std::cout << prices[1999999] << "\\n";\n}\n')
    ok('wasm: l8 s0 program B prints 101', '101' in o and 'EXIT 0' in o, o)
    o = wasm('#include <iostream>\n#include <vector>\nint main() { std::vector<double> prices{101.2, 102.5, 99.8}; double last = 0; for (std::size_t i = 0; i <= prices.size(); ++i) last = prices[i]; std::cout << last << "\\n"; }\n')
    ok('wasm: l3 s6 the app\'s library checks [] and stops ("vector[] index out of bounds")', 'index out of bounds' in o, o)
    o = wasm('#include <iostream>\nint main() {\n    double* p = nullptr;\n    {\n        double bid = 101.25;\n        p = &bid;\n    }\n    std::cout << *p << "\\n";\n}\n')
    ok('wasm: l7 s5 the dangling read printed 101.25 in the app build', '101.25' in o, o)
    o = wasm('#include <iostream>\nint main() { double* px = new double[1000]; px[0] = 1; std::cout << px[0] << "\\n"; delete px; double* r = new double(1.0); delete r; delete r; std::cout << "ran\\n"; }\n', ('-fno-exceptions', '-w'))
    ok('wasm: l8 s5 and summary: mismatched delete and double delete run silently in the app build', 'ran' in o and 'EXIT 0' in o, o)
    o = wasm('#include <iostream>\nint main() { int* p = nullptr; std::cout << *p << "\\n"; }\n')
    ok('wasm: l7 quiz0 the null read does not trap in the app build and printed 0 (fix pass: the screen now says 0)', o.strip().startswith('0') and 'EXIT 0' in o, o)
    o = wasm('#include <algorithm>\n#include <vector>\n\nstruct Quote {\n    double bid;\n    double ask;\n};\n\nint main() {\n    std::vector<Quote> qs{{100.2, 100.4}, {99.9, 100.1}};\n    std::sort(qs.begin(), qs.end());   // line 11\n}\n')
    ok('wasm: l13 s4 sorting Quotes with no < gives a message of hundreds of lines, even with the app\'s -ferror-limit=10 (%d lines)' % len(o.splitlines()), 'COMPILE-FAIL' in o and len(o.splitlines()) >= 200, o[:300])
    o = wasm('#include <iostream>\n#include <vector>\nint main() {\n    std::vector<double> px{100.0, 101.0, 102.0};\n    const double& first = px[0];\n    px.push_back(103.0);\n    std::cout << first << "\\n";\n}\n')
    ok('wasm: homework-2 h-realloc explain "a test run printed 2.8974e-306" with the app compiler', '2.8974e-306' in o, o)
    o = wasm('#include <memory>\nstruct Book {};\nint main() { auto book = std::make_unique<Book>(); delete book; }\n')
    ok('wasm: l9 s3 hint 3 (fixed): a kept delete book; on a unique_ptr does not compile', "cannot delete expression of type 'unique_ptr<Book>'" in o, o)
    o = wasm('#include <iostream>\n#include <vector>\nint main() { std::vector<double> px{100.0, 101.0, 102.0}; const double& first = px[0]; px.push_back(103.0); std::cout << first << "\\n"; }\n')
    print('info wasm: homework-2 h-realloc output in the app build:', o.replace('\n', ' | '))
    o = wasm('#include <iostream>\n#include <memory>\nstruct Order { int q; };\nvoid book_order(std::unique_ptr<Order> o) {}\nint main() {\n    auto a = std::make_unique<Order>(Order{100});\n    book_order(a);\n}\n')
    ok('wasm: l9 s4 clang and libc++ wording', "call to implicitly-deleted copy constructor of 'std::unique_ptr<Order>'" in o and 'user-declared move constructor' in o, o)
    o = wasm('#include <iostream>\n#include <memory>\nstruct P { ~P() { std::cout << "close\\n"; } };\nvoid hold(std::unique_ptr<P> p) { std::cout << "hold\\n"; }\nint main() { auto p = std::make_unique<P>(); (hold(std::move(p)), std::cout << "same statement\\n"); }\n')
    print('info wasm: l9 s9 order of "close" and "same statement" in the app build:', o.replace('\n', ' | '))
    o = wasm('#include <iostream>\n#include <vector>\nint main() { std::vector<int> xs{-10, 4}; int total = 0; for (int x : xs) total += x; int m = total / xs.size(); std::cout << m << "\\n"; }\n', ('-fno-exceptions', '-w'))
    ok('wasm: l13 s6 a negative int total over size() gives a huge value (2147483645)', '2147483645' in o, o)
    o = wasm('#include <iostream>\n#include <vector>\nint main() { std::vector<double> a(3, 1.5); std::vector<double> b = std::move(a); std::vector<double> c(3, 1.0), d(1, 0.0); d = std::move(c); std::cout << a.size() << c.size() << "\\n"; }\n')
    ok('wasm: l11 s7 moved-from vectors are empty in the app build', '00' in o, o)
else:
    print('wasm checks skipped (pass --wasm <pkgs>)')

shutil.rmtree(TMP, ignore_errors=True)
bad = [r for r in results if not r[1]]
print('\n%d checks, %d failed' % (len(results), len(bad)))
for n, _, d in bad:
    print('  FAIL', n)
sys.exit(1 if bad else 0)
