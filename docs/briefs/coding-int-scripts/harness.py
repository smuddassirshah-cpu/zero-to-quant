"""Shared checker. A problem = dict(name, ref, brute, starter, tests, prelude, postlude).
tests = list of dict(setup, call, expect, compare). Expected values come from brute (independent) and are
asserted equal to the reference; the starter must fail at least one test."""
import math, json, os, subprocess, tempfile, textwrap, signal
class _TO(BaseException): pass
def _alarm(*a): raise _TO()
signal.signal(signal.SIGALRM, _alarm)

OUT = os.path.dirname(os.path.abspath(__file__))
REPORT = []

def _eq(a, b, compare):
    if compare == 'isclose':
        if isinstance(a, (list, tuple)):
            return len(a) == len(b) and all(math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-12) for x, y in zip(a, b))
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    return a == b

def run_py(src, tests, prelude='', postlude='', timeout=None):
    ns = {}
    exec(prelude, ns)
    ns['__learner_source__'] = src
    exec(src, ns)
    exec(postlude, ns)
    res = []
    for t in tests:
        try:
            signal.alarm(5)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            signal.alarm(0)
            if t.get('compare') == 'raises':
                res.append((False, 'no error'))
                continue
            res.append((_eq(got, t['expect'], t.get('compare', 'equal')), got))
        except _TO:
            res.append((False, 'timeout 5 s'))
        except Exception as e:
            signal.alarm(0)
            if t.get('compare') == 'raises' and type(e).__name__ == t['expect']:
                res.append((True, type(e).__name__))
            else:
                res.append((False, 'EXC ' + repr(e)[:80]))
    return res

def check_py(name, ref_src, starter, tests, prelude='', postlude=''):
    r = run_py(ref_src, tests, prelude, postlude)
    bad = [i for i, (ok, g) in enumerate(r) if not ok]
    assert not bad, (name, 'reference fails tests', bad, [r[i] for i in bad][:3])
    s = run_py(starter, tests, prelude, postlude)
    nfail = sum(1 for ok, g in s if not ok)
    assert nfail >= 1, (name, 'starter passes everything')
    print(f'OK py {name}: {len(tests)} tests, reference passes all, starter fails {nfail}')
    return nfail

def lit(x, maxlen=None):
    s = repr(x)
    return s

def md_tests(tests, width=None):
    lines = ['| # | Call | Expected |', '| --- | --- | --- |']
    for i, t in enumerate(tests, 1):
        call = t['call']
        if t.get('setup'):
            call = t['setup'] + '; ' + call
        e = repr(t['expect'])
        if width and len(call) > width: call = call[:width - 3] + '...'
        pass
        lines.append(f'| {i} | `{call}` | `{e}` |')
    return '\n'.join(lines)

# ---------- C++ ----------
def cpp_lit(v):
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, int): return str(v)
    if isinstance(v, float): return repr(v)
    if isinstance(v, str): return json.dumps(v)
    if isinstance(v, (list, tuple)): return '{' + ', '.join(cpp_lit(x) for x in v) + '}'
    raise TypeError(v)

def check_cpp(name, ref_cpp, starter_cpp, calls, flags=('-std=c++20', '-O1', '-fno-exceptions'), postlude=''):
    """calls = list of (cpp_expression, expected_python_value, kind) kind in {'json'}; prints each result as JSON-ish
    text and compares to expected via python parse."""
    def build(src):
        prog = src + '\n' + postlude + '\n#include <iostream>\n' + TOSTR + '\nint main(){\n'
        for i, (expr, exp) in enumerate(calls):
            prog += f'  {{ std::cout << "T{i}:" ; zq_put(std::cout, ({expr})); std::cout << "\\n"; }}\n'
        prog += '  return 0;\n}\n'
        return prog
    def run(src, label):
        d = tempfile.mkdtemp(dir=os.path.join(OUT, 'build'))
        p = os.path.join(d, 'main.cpp')
        open(p, 'w').write(build(src))
        for std in (['-std=c++17'], ['-std=c++20']):
            cmd = ['g++'] + std + ['-O1', '-fno-exceptions', '-o', os.path.join(d, 'a.out'), p]
            c = subprocess.run(cmd, capture_output=True, text=True)
            assert c.returncode == 0, (name, label, std, c.stderr[:1500])
        r = subprocess.run([os.path.join(d, 'a.out')], capture_output=True, text=True, timeout=20)
        out = {}
        for line in r.stdout.splitlines():
            k, v = line.split(':', 1)
            out[int(k[1:])] = json.loads(v)
        return out
    ro = run(ref_cpp, 'reference')
    bad = [i for i, (e, x) in enumerate(calls) if ro.get(i) != x]
    assert not bad, (name, 'C++ reference mismatch', [(i, ro.get(i), calls[i][1]) for i in bad][:3])
    so = run(starter_cpp, 'starter')
    nfail = sum(1 for i, (e, x) in enumerate(calls) if so.get(i) != x)
    assert nfail >= 1, (name, 'C++ starter passes all')
    print(f'OK cpp {name}: {len(calls)} tests, reference passes all (c++17 and c++20), starter fails {nfail}')
    return nfail

TOSTR = r'''
#include <vector>
#include <string>
#include <type_traits>
template <class T> void zq_put(std::ostream& o, const T& v);
template <class T, class=void> struct zq_seq : std::false_type {};
template <class T> struct zq_seq<T, std::void_t<decltype(std::begin(std::declval<const T&>()))>> : std::true_type {};
template <class T> void zq_put(std::ostream& o, const T& v) {
  if constexpr (std::is_same_v<T,bool>) o << (v ? "true" : "false");
  else if constexpr (std::is_arithmetic_v<T>) { o.precision(17); o << v; }
  else if constexpr (std::is_convertible_v<const T&, std::string>) o << '"' << std::string(v) << '"';
  else { o << '['; bool f = true; for (const auto& x : v) { if (!f) o << ','; f = false; zq_put(o, x); } o << ']'; }
}
'''
os.makedirs(os.path.join(OUT, 'build'), exist_ok=True)
