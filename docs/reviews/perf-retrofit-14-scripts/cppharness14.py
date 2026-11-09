"""Native mirror of the app's C++ function-mode grading (cpp-grade.js), for second reads.

Each unit is: the engine's leakCheck block (read from cpp-grade.js: freed memory poisoned with
0xDD and quarantined, a double delete exits 1, a leak exits 1), the widget prelude, the code,
the postlude, then one function per value test holding its setup and call, so the locals die
before the value is printed. One process per test, as in the app. A compile test passes when
-fsyntax-only agrees with its expect. Flags: -O1 -fno-exceptions -w, with -std=c++17 (the app)
and -std=c++20, on g++ and clang++.
"""
import os, re, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
GRADE = os.path.join(ROOT, 'app', 'js', 'engine', 'widgets', 'cpp-grade.js')
LEAK = re.search(r'const LEAK = String\.raw`(.*?)`;', open(GRADE).read(), re.S).group(1)
assert 'memset(p, 0xDD' in LEAK
PRINT = r'''
#include <cstdio>
#include <string>
#include <vector>
#include <type_traits>
template <class X> static std::string zq_s(X v) { if constexpr (std::is_same_v<X, bool>) return v ? "true" : "false"; else return std::to_string((long long)v); }
static std::string zq_s(const std::vector<int>& v) { std::string s = "["; for (std::size_t i = 0; i < v.size(); ++i) { if (i) s += ", "; s += std::to_string(v[i]); } return s + "]"; }
'''
BUILDS = [(c, s) for c in ('g++', 'clang++') for s in ('-std=c++17', '-std=c++20')]


def etext(e):
    if isinstance(e, bool):
        return 'true' if e else 'false'
    if isinstance(e, list):
        return '[' + ', '.join(str(int(x)) for x in e) + ']'
    return str(e)


def run_unit(prelude, code, postlude, tests, cxx, std, leak=True):
    """Return a list of booleans, one per test."""
    tmp = tempfile.mkdtemp()
    flags = [std, '-O1', '-fno-exceptions', '-w']
    head = (LEAK if leak else '') + prelude + code + postlude
    res = [False] * len(tests)
    vals = [k for k, t in enumerate(tests) if 'compiles' not in t]
    body = head + PRINT
    for k in vals:
        body += 'static void zq_case_%d(std::string& zq_o) {\n%s\nzq_o = zq_s(%s);\n}\n' % (k, tests[k].get('setup', ''), tests[k]['call'])
    body += '#include <cstdlib>\nint main(int argc, char** argv) {\n std::string o;\n switch (std::atoi(argv[1])) {\n'
    body += ''.join(' case %d: zq_case_%d(o); break;\n' % (k, k) for k in vals)
    body += ' }\n std::printf("%s\\n", o.c_str());\n std::fflush(stdout);\n return 0;\n}\n'
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx] + flags + [src, '-o', exe], capture_output=True, text=True)
    if cp.returncode == 0:
        for k in vals:
            try:
                pr = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
                res[k] = pr.returncode == 0 and pr.stdout.strip() == etext(tests[k]['expect'])
            except subprocess.TimeoutExpired:
                pass
    elif os.environ.get('SHOWERR'):
        print(cp.stderr[:3000])
    for k, t in enumerate(tests):
        if 'compiles' in t:
            s2 = os.path.join(tmp, 'c%d.cpp' % k)
            open(s2, 'w').write(head + '\nvoid zq_probe() {\n%s\n%s\n}\nint main() { return 0; }\n' % (t.get('setup', ''), t['compiles']))
            built = subprocess.run([cxx] + flags + ['-fsyntax-only', s2], capture_output=True).returncode == 0
            res[k] = built == t['expect']
    shutil.rmtree(tmp)
    return res


def run_builds(prelude, code, postlude, tests, leak=True):
    return {b: run_unit(prelude, code, postlude, tests, b[0], b[1], leak) for b in BUILDS}


def failing(results):
    """{build: [1-based failing test numbers]}"""
    return {b: [k + 1 for k, r in enumerate(v) if not r] for b, v in results.items()}
