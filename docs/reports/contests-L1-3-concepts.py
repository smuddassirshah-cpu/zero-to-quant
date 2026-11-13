#!/usr/bin/env python3
"""Concept audit, round 1 (blind): contests levels 1 to 3.

Parts, all run on the content's own code and data:
  A. every code widget (37 Python, 2 C++): the solution passes its hidden tests, the starter fails;
  B. every `feedback.byKey.test-N` line that names a mistake: a submission with that mistake
     must pass tests 1..N-1 and fail test N. A check that fails because the content is wrong is
     labelled FINDING n (the number in docs/reviews/audit-contests-1-3.md) and stays failing;
  C. worked examples, stated numbers and general claims, recomputed or brute-forced;
  D. speed claims, timed with wide margins (ratios, not absolute times).

Page against this script. The page runs Pyodide 0.27.7 (CPython 3.12.7, wasm32) with
sys.setrecursionlimit(3000) and a 5 s limit per test (app/js/engine/widgets/code.js, TEST_MS).
Here CPython 3.12 or 3.13 runs natively with the same recursion limit; a mistake that the page
stops at 5 s is stopped here by a shorter alarm (CAP seconds), since native Python is two to
three times faster than Pyodide. C++ runs on the page in YoWASP clang 21 (wasm32, libc++, -O1,
no exceptions, `long` 32 bits); here clang++ or g++ compiles natively with -O1 (x86-64, `long`
64 bits), so no check depends on the width of `long` or on exceptions. Without a C++ compiler
the C++ checks are skipped and reported.

Run from the repository root with the venv Python (pytest and sympy are used when present):
    python3 docs/reports/contests-L1-3-concepts.py
Exit 0 when every check holds; exit 1 lists the failing checks.
"""
import bisect, contextlib, io, itertools, json, math, os, random, shutil, signal, subprocess, sys, tempfile, time
from collections import deque

sys.setrecursionlimit(3000)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'contests')
FAIL, N, SKIP = [], [0], []
CAP = 2  # seconds: stands in for the page's 5 s limit on mistakes that are far too slow


def ck(label, cond, detail=''):
    N[0] += 1
    if not cond:
        FAIL.append(label + (' :: ' + ' '.join(str(detail).split())[:160] if detail != '' else ''))


FILES = ['l1-reading-statements', 'l2-limits-to-complexity', 'l3-fast-io', 'l4-stress-testing', 'l5-modulo',
         'l6-gcd-and-primes', 'l7-counting-mod', 'l8-invariants', 'l9-constructive', 'l10-greedy-proofs',
         'l11-bitmasks', 'l12-difference-arrays', 'review-1', 'review-2', 'review-3',
         'homework-1', 'homework-2', 'homework-3']
DOC = {f: json.load(open(os.path.join(ROOT, f + '.json'), encoding='utf-8')) for f in FILES}


class TimeUp(BaseException):
    pass


def _alarm(sig, frm):
    raise TimeUp()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    """__zq_judge 'equal' from code.js: lists and tuples compare element by element, the rest by ==."""
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(same(p, q) for p, q in zip(x, y)))
    return bool(x == y)


def norm(t):
    ls = [l.rstrip() for l in t.replace('\r\n', '\n').split('\n')]
    while ls and not ls[0]:
        ls.pop(0)
    while ls and not ls[-1]:
        ls.pop()
    return ls


def is_script(w):
    return any(c.get('compare') == 'stdout' or c.get('stdin') is not None for c in w.get('examples', []) + w['tests'])


def run_py(w, code, limit=30, stop=False):
    """Run code against a Python widget's tests as code.js does. Returns [(ok, got)], one per test
    (with stop=True, up to and including the first failing test)."""
    tests = w['tests']
    if is_script(w):
        out = []
        for t in tests:
            feed, buf = io.StringIO(t.get('stdin', '')), io.StringIO()

            def _input(prompt='', feed=feed):
                ln = feed.readline()
                if not ln:
                    raise EOFError
                return ln[:-1] if ln.endswith('\n') else ln
            ns = {'__name__': '__main__', 'input': _input, '__learner_source__': code}
            old = (sys.stdout, sys.stdin)
            sys.stdout, sys.stdin = buf, feed
            signal.alarm(limit)
            try:
                exec(compile(code, 'solution.py', 'exec'), ns)
                ok, got = norm(buf.getvalue()) == norm(t['expect']), buf.getvalue()[:60]
            except SystemExit:
                ok, got = norm(buf.getvalue()) == norm(t['expect']), buf.getvalue()[:60]
            except BaseException as e:  # noqa
                ok, got = False, type(e).__name__
            finally:
                signal.alarm(0)
                sys.stdout, sys.stdin = old
            out.append((ok, got))
            if stop and not ok:
                break
        return out
    ns = {'__name__': '__main__', '__learner_source__': code}
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp(prefix='zq-')
    os.chdir(tmp)
    sys.path.insert(0, '')
    out = []
    try:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                exec(w.get('prelude', ''), ns)
                exec(compile(code, 'solution.py', 'exec'), ns)
                exec(w.get('postlude', ''), ns)
        except BaseException as e:  # noqa
            return [(False, 'load: ' + type(e).__name__)] * len(tests)
        for t in tests:
            signal.alarm(limit)
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    if t.get('setup'):
                        exec(t['setup'], ns)
                    if t.get('compare') == 'raises':
                        try:
                            got = eval(t['call'], ns)
                            ok = False
                        except Exception as e:  # noqa
                            got = type(e).__name__
                            ok = t['expect'].strip() in [k.__name__ for k in type(e).__mro__]
                    else:
                        got = eval(t['call'], ns)
                        ok = same(got, eval(t['expect'], ns))
            except BaseException as e:  # noqa
                ok, got = False, type(e).__name__
            finally:
                signal.alarm(0)
            out.append((ok, got))
            if stop and not ok:
                break
    finally:
        os.chdir(cwd)
        sys.path.remove('')
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def first_fail(res):
    for i, (ok, _) in enumerate(res):
        if not ok:
            return i + 1
    return None


def items_of(doc):
    return [('screens', i, x) for i, x in enumerate(doc.get('screens') or [])] + \
           [('quiz', i, x) for i, x in enumerate(doc.get('quiz') or [])] + \
           [('items', i, x) for i, x in enumerate(doc.get('items') or [])]


def W(f, key, i):
    return DOC[f][key][i]['widget']


HAVE_PYTEST = True
try:
    import pytest  # noqa
except Exception:  # noqa
    HAVE_PYTEST = False
    SKIP.append('pytest not installed: l4 screens[8] (pytest widget) skipped')
CXX = shutil.which('clang++') or shutil.which('g++')
if not CXX:
    SKIP.append('no C++ compiler: the two C++ widgets and four C++ expression checks skipped')
CTMP = tempfile.mkdtemp(prefix='zq-cpp-')


def cpp_build(src, tag):
    path = os.path.join(CTMP, tag + '.cpp')
    exe = os.path.join(CTMP, tag)
    open(path, 'w').write(src)
    r = subprocess.run([CXX, '-std=c++17', '-O1', '-w', path, '-o', exe], capture_output=True, text=True)
    return exe if r.returncode == 0 else None


def run_cpp(w, code, tag):
    """Script mode: the program per test with its stdin. Function mode: a main per call. [(ok, got)]."""
    tests = w['tests']
    if is_script(w):
        exe = cpp_build(code, tag)
        if not exe:
            return [(False, 'compile')] * len(tests)
        out = []
        for t in tests:
            try:
                r = subprocess.run([exe], input=t.get('stdin', ''), capture_output=True, text=True, timeout=10)
                out.append((norm(r.stdout) == norm(t['expect']), r.stdout[:40]))
            except subprocess.TimeoutExpired:
                out.append((False, 'timeout'))
        return out
    calls = ''.join('    if (k == %d) std::cout << (long long)%s(%s);\n' % (
        i, t['call'], ', '.join(str(a) + 'LL' for a in t['args'])) for i, t in enumerate(tests))
    src = '#include <iostream>\n#include <cstdlib>\n' + code + '\nint main(int c, char** v) {\n    int k = std::atoi(v[1]);\n' + calls + '}\n'
    exe = cpp_build(src, tag)
    if not exe:
        return [(False, 'compile')] * len(tests)
    out = []
    for i, t in enumerate(tests):
        r = subprocess.run([exe, str(i)], capture_output=True, text=True, timeout=10)
        out.append((r.stdout.strip() == str(t['expect']), r.stdout.strip()))
    return out


def cpp_value(expr, tag):
    exe = cpp_build('#include <iostream>\nint main() { long long a = 3, b = 5, p = 7; int x = 8; int mask = 5, i = 0; std::cout << (long long)(%s); }\n' % expr, tag)
    return subprocess.run([exe], capture_output=True, text=True).stdout.strip() if exe else None


# ------------------------------------------------------------------ A. every code widget
n_py = n_cpp = 0
for f in FILES:
    for key, i, it in items_of(DOC[f]):
        w = it.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        tag = '%s %s[%d]' % (f, key, i)
        if w.get('language') == 'cpp':
            n_cpp += 1
            if not CXX:
                continue
            ck(tag + ': C++ solution passes', first_fail(run_cpp(w, w['solution'], 'sol%d' % n_cpp)) is None)
            ck(tag + ': C++ starter fails', first_fail(run_cpp(w, w['starter'], 'sta%d' % n_cpp)) is not None)
            continue
        n_py += 1
        if 'pytest' in w.get('postlude', '') and not HAVE_PYTEST:
            continue
        res = run_py(w, w['solution'])
        ck(tag + ': solution passes', first_fail(res) is None, (first_fail(res), res[(first_fail(res) or 1) - 1][1]))
        ck(tag + ': starter fails', first_fail(run_py(w, w['starter'], 5, stop=True)) is not None)
ck('code widget count', (n_py, n_cpp) == (37, 2), (n_py, n_cpp))


# ------------------------------------------------------------------ B. mutants
def mutant(label, w, code, n, got=None, limit=20, finding=None):
    """The mistake `code` must first fail at test n. With finding=k the content's line is wrong and the check keeps failing."""
    res = run_py(w, code, limit, stop=True)
    ff = first_fail(res)
    name = ('FINDING %d: ' % finding if finding else 'mutant ') + label + ': first failing test %s' % n
    ck(name, ff == n, 'first fail %s, got %s' % (ff, res[ff - 1][1] if ff else None))
    if got is not None and ff == n:
        ck('mutant ' + label + ': value', got(res[n - 1][1]), res[n - 1][1])
    return ff, (res[ff - 1][1] if ff else None)


# ---- l1
w = W('l1-reading-statements', 'screens', 9)
mutant('l1 parse drops the last line', w, '''def parse(text):
    lines = text.split('\\n')[:-1]
    t = int(lines[0]); cases = []
    for i in range(t):
        cases.append([int(x) for x in lines[2 + 2 * i].split()])
    return t, cases''', 2)
mutant('l1 parse pairs every line', w, '''def parse(text):
    lines = text.split('\\n')
    t = int(lines[0]); cases = []
    for i in range(1, len(lines) - 1, 2):
        cases.append([int(x) for x in lines[i + 1].split()])
    return t, cases''', 3)
mutant('l1 parse fixed line indices', w, '''def parse(text):
    lines = text.split('\\n')
    t = int(lines[0])
    return t, [[int(x) for x in lines[2 + 2 * i].split()] for i in range(t)]''', 4)
mutant('l1 parse pop(0)', w, '''def parse(text):
    tokens = text.split()
    t = int(tokens.pop(0)); cases = []
    for _ in range(t):
        n = int(tokens.pop(0))
        cases.append([int(tokens.pop(0)) for _ in range(n)])
    return t, cases''', 7, limit=CAP)
w = W('l1-reading-statements', 'screens', 10)
mutant('l1 >=', w, '''def new_highs(xs):
    c = 0; best = None
    for x in xs:
        if best is None or x >= best: c += 1; best = x
    return c''', 3, got=lambda g: g == 4)
BEST0 = '''def new_highs(xs):
    c = 0; best = 0
    for x in xs:
        if x > best: c += 1; best = x
    return c'''
mutant('l1 best = 0', w, BEST0, 5, got=lambda g: g == 0)
mutant('l1 test-6 line names best = 0, which fails test 5', w, BEST0, 6, finding=3)
mutant('l1 falsy best (the mistake that does reach test 6)', w, '''def new_highs(xs):
    c = 0; best = None
    for x in xs:
        if not best or x > best: c += 1; best = x
    return c''', 6, got=lambda g: g == 4)
mutant('l1 max of every prefix', w, '''def new_highs(xs):
    return sum(1 for i in range(len(xs)) if i == 0 or xs[i] > max(xs[:i]))''', 9, limit=CAP)
for alt in ('''def new_highs(xs):
    c = 1; best = xs[0]
    for x in xs[1:]:
        if x > best: c += 1; best = x
    return c''',):
    ck('l1 xs[0] start passes', first_fail(run_py(w, alt)) is None)

# ---- l2
w = W('l2-limits-to-complexity', 'screens', 9)
T500 = '''def budget_class(n):
    if n <= 26: return "2^n"
    if n <= 500: return "n^3"
    if n <= 10**4: return "n^2"
    if n <= 4.5e6: return "n log n"
    if n <= 10**8: return "n"
    return "log n"'''
mutant("l2 table's 500", w, T500, 6)
mutant("l2 test-7 line names the table's 500, which fails test 6", w, T500, 7, finding=5)
mutant('l2 unguarded 2 ** n', w, w['solution'].replace('n <= 60 and ', ''), 15, limit=CAP)
w = W('l2-limits-to-complexity', 'screens', 10)
STRICT = w['solution'].replace('<= k', '< k')
mutant('l2 < for <= fails the first test', w, STRICT, 1, got=lambda g: g == 2)
mutant('l2 test-3 line says use <=, but < fails test 1', w, STRICT, 3, finding=6)
mutant('l2 duplicates removed (the mistake that does reach test 3)', w, w['solution'].replace('sorted(xs)', 'sorted(set(xs))'), 3)
mutant('l2 values above k dropped (reaches test 5)', w, w['solution'].replace('sorted(xs)', 'sorted(x for x in xs if x <= k)'), 5)
mutant('l2 every pair on the argument', w, '''def pair_sums_at_most(xs, k):
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] + xs[j] <= k)''', 8)
mutant('l2 every pair on a copy', w, '''def pair_sums_at_most(xs, k):
    a = list(xs); n = len(a); c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] <= k: c += 1
    return c''', 9, limit=CAP)

# ---- l3
w = W('l3-fast-io', 'screens', 8)
mutant('l3 split on newline', w, '''def read_tokens(data):
    out = []
    for line in data.split(b'\\n'):
        for tok in line.split(b' '):
            if tok: out.append(int(tok))
    return iter(out)''', 3)
mutant('l3 returns a list', w, 'def read_tokens(data):\n    return [int(x) for x in data.split()]', 6)
mutant('l3 class with a fresh __iter__', w, '''class R:
    def __init__(self, xs): self.xs = xs; self.i = 0
    def __iter__(self): return iter(self.xs)
    def __next__(self):
        self.i += 1; return self.xs[self.i - 1]
def read_tokens(data):
    return R([int(x) for x in data.split()])''', 7)
w = W('l3-fast-io', 'screens', 9)
mutant('l3 S strips the last character of each line', w, '''import sys
lines = [l[:-1] for l in sys.stdin.readlines()]
t = int(lines[0]); out = []
for i in range(t):
    a = list(map(int, lines[2 + 2 * i].split()))
    out.append(f"{sum(a)} {max(a)}")
print("\\n".join(out))''', 4)
mutant('l3 S one input() per test case', w, '''t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(sum(a), max(a))''', 5)
NOPOS = w['solution'].replace('    pos += n\n', '')
mutant('l3 S pos not moved past the values fails the first test', w, NOPOS, 1)
mutant('l3 S test-7 line names a pos that does not move, which fails test 1', w, NOPOS, 7, finding=8)
mutant('l3 S recursion over the test cases (a mistake that does reach test 7)', w, '''import sys
data = sys.stdin.read().split()
out = []
def go(left, pos):
    if left == 0: return
    n = int(data[pos]); a = list(map(int, data[pos + 1:pos + 1 + n]))
    out.append(f"{sum(a)} {max(a)}")
    go(left - 1, pos + 1 + n)
go(int(data[0]), 1)
print("\\n".join(out))''', 7)
if CXX:
    w = W('l3-fast-io', 'screens', 10)
    sol = w['solution']

    def cmut(label, code, n, finding=None):
        res = run_cpp(w, code, 'm%d' % N[0])
        ff = first_fail(res)
        ck(('FINDING %d: ' % finding if finding else 'mutant ') + label + ': first failing test %s' % n, ff == n,
           'first fail %s, got %r' % (ff, res[ff - 1][1] if ff else None))
    INTSUM = sol.replace('long long sum = 0, best = 0;', 'int sum = 0; long long best = 0;')
    BESTZ = sol.replace('if (i == 0 || x > best)', 'if (x > best)')
    cmut('l3 C++ int sum', INTSUM, 3)
    cmut('l3 C++ test-6 line names an int sum, which fails test 3', INTSUM, 6, finding=10)
    cmut('l3 C++ unsigned sum fails the first test', sol.replace('long long sum = 0, best = 0;', 'unsigned sum = 0; long long best = 0;'), 1)
    cmut('l3 C++ maximum from 0 fails the first test', BESTZ, 1)
    cmut('l3 C++ test-4 line names a maximum from 0, which fails test 1', BESTZ, 4, finding=9)

# ---- l4
w = W('l4-stress-testing', 'screens', 7)
sol = w['solution']
mutant('l4 new Random each trial', w, sol.replace('    rng = random.Random(seed)\n', '').replace('case = gen(rng)', 'case = gen(random.Random(seed))'), 2)
mutant('l4 one trial too many', w, sol.replace('range(trials)', 'range(trials + 1)'), 4)
mutant('l4 list(case) copy', w, sol.replace('fast(copy.deepcopy(case)) != brute(copy.deepcopy(case))', 'fast(list(case)) != brute(list(case))'), 7)
mutant('l4 no copies', w, sol.replace('fast(copy.deepcopy(case)) != brute(copy.deepcopy(case))', 'fast(case) != brute(case)'), 9,
       got=lambda g: same(g, ([1, 1, 2, 4, 6, 10], 2)))
if HAVE_PYTEST:
    w = W('l4-stress-testing', 'screens', 8)
    sol = w['solution']
    mutant('l4 pytest: no assert', w, sol.replace('assert stress(fast, brute, gen, 500, 1) is None', 'stress(fast, brute, gen, 500, 1)'), 6)
    mutant('l4 pytest: brute calls the fast function', w, sol.replace('''    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n)
               if xs[i] + xs[j] <= k)''', '    return pair_sums_at_most(xs, k)'), 6)
    mutant('l4 pytest: k never negative', w, sol.replace('rng.randint(-10, 10)', 'rng.randint(0, 10)'), 10)
    mutant('l4 pytest: generator returns a list', w, sol.replace('return xs, rng.randint(-10, 10)', 'return [xs]'), 5)

# ---- l5 (no test-N lines; the `how` claims)
w = W('l5-modulo', 'screens', 6)
mutant('l5 loop of e multiplications', w, '''def power_mod(a, e, m):
    r = 1 % m
    for _ in range(e): r = r * a % m
    return r''', 7, limit=CAP)
mutant('l5 result starts at 1', w, w['solution'].replace('result = 1 % m', 'result = 1'), 3)
r = random.Random(1)
ns = {}
exec(w['solution'], ns)
ck('l5 power_mod equals pow', all(ns['power_mod'](a, e, m) == pow(a, e, m) for a, e, m in
                                    ((r.randint(0, 10**18), r.randint(0, 10**18), r.randint(1, 10**9 + 7)) for _ in range(2000))))
if CXX:
    w = W('l5-modulo', 'screens', 8)
    res = run_cpp(w, w['starter'], 'mulsta')
    ck('l5 C++ starter first fails test 2', first_fail(res) == 2, first_fail(res))
    ck('l5 mul_mod expects', all(int(t['expect']) == t['args'][0] * t['args'][1] % t['args'][2] for t in w['tests']))
    ck('C++ -3 % 7 == -3', cpp_value('(a - 6) % p', 'v1') == '-3')
    ck('C++ (3 - 5) % 7 == -2 and (3 - 5 + 7) % 7 == 5', (cpp_value('(a - b) % p', 'v2'), cpp_value('(a - b + p) % p', 'v3')) == ('-2', '5'))
    ck('C++ x & (x - 1) == 0 is false for 8', cpp_value('x & (x - 1) == 0', 'v4') == '0')
    ck('C++ 4 & 1 << 0 == 0 is 0 where (4 & 1 << 0) == 0 is 1', (cpp_value('4 & 1 << 0 == 0', 'v5'), cpp_value('(4 & 1 << 0) == 0', 'v6')) == ('0', '1'))

# ---- l6 (the `how` claims)
w = W('l6-gcd-and-primes', 'screens', 5)
mutant('l6 subtraction gcd', w, '''def gcd(a, b):
    if a == 0 or b == 0: return a + b
    while a != b:
        if a > b: a -= b
        else: b -= a
    return a
def gcd_all(xs):
    g = 0
    for x in xs: g = gcd(g, x)
    return g''', 13, limit=CAP)
w = W('l6-gcd-and-primes', 'screens', 9)
mutant('l6 factorise with no square-root bound', w, '''def factorise(n):
    out = []; d = 2
    while n > 1:
        while n % d == 0: out.append(d); n //= d
        d += 1
    return out''', 9, limit=CAP)

# ---- l7
w = W('l7-counting-mod', 'screens', 7)
ff, got = mutant('l7 no guard: negative index wraps silently', w, 'def n_choose_k(n, k, fact, inv_fact, p):\n    return fact[n] * inv_fact[k] % p * inv_fact[n - k] % p', 5)
ck('l7 no guard returns a number, not an error', isinstance(got, int) and got != 0, got)

# ---- l8
w = W('l8-invariants', 'screens', 7)
mutant('l8 one subtraction at a time', w, '''def can_reach(x, y, c, d):
    while c >= x and d >= y:
        if c == x and d == y: return True
        if c == d: return False
        if c > d: c -= d
        else: d -= c
    return False''', 11, limit=CAP)
w = W('l8-invariants', 'screens', 8)
mutant('l8 simulate with a scan per move', w, '''def final_parity(xs):
    xs = list(xs)
    if not xs: return 0
    while len(xs) > 1:
        i = xs.index(max(xs)); a = xs.pop(i)
        j = xs.index(max(xs)); b = xs.pop(j)
        xs.append(abs(a - b))
    return xs[0] % 2''', 8, limit=CAP)

# ---- l9
w = W('l9-constructive', 'screens', 5)
mutant('l9 -1 below 4', w, 'def no_adjacent(n):\n    if n < 4: return -1\n    return list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))', 1)
mutant('l9 no special case', w, 'def no_adjacent(n):\n    return list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))', 2)
mutant('l9 only n = 2', w, 'def no_adjacent(n):\n    if n == 2: return -1\n    return list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))', 3)
PERM = '\n'.join(DOC['l9-constructive']['screens'][6]['canvas']['params']['lines'])
t0 = time.perf_counter()
res = run_py(w, PERM, limit=8)
t_perm = time.perf_counter() - t0
ck('l9 the permutation search passes tests 1 to 8 when given time', all(ok for ok, _ in res[:8]))
ck('l9 the permutation search fails test 9', not res[8][0])
w = W('l9-constructive', 'screens', 8)
sol = w['solution']
mutant('l9 divide by k - 1', w, '''def fill_array(n, s, k):
    if s < n or s > n * k: return -1
    full = (s - n) // (k - 1); rest = (s - n) % (k - 1)
    out = [k] * full + ([1 + rest] if full < n else []) + [1] * (n - full - 1)
    return out[:n]''', 4)
mutant('l9 no upper check', w, sol.replace('if s < n or s > n * k:', 'if s < n:'), 6)
mutant('l9 no lower check', w, sol.replace('if s < n or s > n * k:', 'if s > n * k:'), 7)
mutant('l9 one raise at a time', w, '''def fill_array(n, s, k):
    if s < n or s > n * k: return -1
    out = [1] * n; i = 0; extra = s - n
    while extra > 0:
        if out[i] == k: i += 1
        else: out[i] += 1; extra -= 1
    return out''', 9, limit=CAP)

# ---- l10
w = W('l10-greedy-proofs', 'screens', 4)
sol = w['solution']
mutant('l10 > for >=', w, sol.replace('s >= end', 's > end'), 2)
BYSTART = sol.replace('key=lambda x: x[1]', 'key=lambda x: x[0]')
BYLEN = sol.replace('key=lambda x: x[1]', 'key=lambda x: x[1] - x[0]')
mutant('l10 sort by start fails the first test', w, BYSTART, 1, got=lambda g: g == 1)
mutant('l10 sort by length fails the first test', w, BYLEN, 1)
mutant('l10 test-6 line names a sort by start, which fails test 1', w, BYSTART, 6, finding=14)
mutant('l10 test-7 line names a sort by length, which fails test 1', w, BYLEN, 7, finding=14)
mutant('l10 check against every kept meeting', w, '''def max_non_overlapping(intervals):
    kept = []
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if all(s >= e2 or e <= s2 for s2, e2 in kept): kept.append((s, e))
    return len(kept)''', 8, limit=CAP)
w = W('l10-greedy-proofs', 'screens', 6)
sol = w['solution']
mutant('l10 rooms: starts first on ties', w, sol.replace('events.sort()', 'events.sort(key=lambda t: (t[0], -t[1]))'), 2, got=lambda g: g == 2)
mutant('l10 rooms: duplicates removed', w, sol.replace('for s, e in intervals:', 'for s, e in set(intervals):'), 3)
mutant('l10 rooms: every time point', w, '''def min_rooms(intervals):
    lo = min(s for s, e in intervals); hi = max(e for s, e in intervals); best = 0
    for t in range(lo, hi):
        best = max(best, sum(1 for s, e in intervals if s <= t < e))
    return best''', 7, limit=CAP)
w = W('l10-greedy-proofs', 'screens', 8)
sol = w['solution']
mutant('l10 first failure returned', w, '''import random
def greedy_counterexample(greedy, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if greedy(case) != brute(case): return case
    return None''', 1, got=lambda g: same(g, ([1, 5, 8], 15)))
mutant('l10 one trial too many', w, sol.replace('range(trials)', 'range(trials + 1)'), 5)

# ---- l11
w = W('l11-bitmasks', 'screens', 3)
sol = w['solution']
mutant('l11 max over non-empty subsets', w, '''def best_subset(profits, risks, limit):
    n = len(profits); out = []
    for mask in range(1, 1 << n):
        p = sum(profits[i] for i in range(n) if mask >> i & 1); r = sum(risks[i] for i in range(n) if mask >> i & 1)
        out.append(p if r <= limit else 0)
    return max(out)''', 2)
mutant('l11 n = 0 special case, max over fitting subsets', w, '''def best_subset(profits, risks, limit):
    n = len(profits)
    if n == 0: return 0
    out = []
    for mask in range(1, 1 << n):
        p = sum(profits[i] for i in range(n) if mask >> i & 1); r = sum(risks[i] for i in range(n) if mask >> i & 1)
        if r <= limit: out.append(p)
    return max(out)''', 3)
LT = sol.replace('risk <= limit', 'risk < limit')
mutant('l11 < for <= fails the first test', w, LT, 1, got=lambda g: g == 9)
mutant('l11 test-5 line says at most means <=, but < fails test 1', w, LT, 5, finding=15)
w = W('l11-bitmasks', 'screens', 5)
mutant('l11 count: empty set never counted', w, '''def count_subsets_with_sum(xs, target):
    n = len(xs)
    return sum(1 for mask in range(1, 1 << n) if sum(xs[i] for i in range(n) if mask >> i & 1) == target)''', 2)
mutant('l11 count: special case for the empty list only', w, '''def count_subsets_with_sum(xs, target):
    n = len(xs)
    if n == 0: return 1 if target == 0 else 0
    return sum(1 for mask in range(1, 1 << n) if sum(xs[i] for i in range(n) if mask >> i & 1) == target)''', 3)
mutant('l11 count: duplicate values removed', w, '''def count_subsets_with_sum(xs, target):
    xs = sorted(set(xs)); n = len(xs)
    return sum(1 for mask in range(1 << n) if sum(xs[i] for i in range(n) if mask >> i & 1) == target)''', 4)
mutant('l11 count: table of non-negative sums', w, '''def count_subsets_with_sum(xs, target):
    if target < 0: return 0
    ways = [1] + [0] * target
    for x in xs:
        for s in range(target, x - 1, -1):
            ways[s] += ways[s - x]
    return ways[target]''', 5)
for t in w['tests']:
    xs, target = eval('(' + t['call'].split('(', 1)[1].rsplit(')', 1)[0] + ',)')[:2]
    brute = sum(1 for k in range(len(xs) + 1) for c in itertools.combinations(xs, k) if sum(c) == target)
    ck('l11 count expect by combinations', brute == int(t['expect']), (xs[:3], target))
w = W('l11-bitmasks', 'screens', 6)
mutant('l11 popcounts seeded with [0, 1]', w, '''def popcounts(n):
    p = [0, 1]
    while len(p) < (1 << n): p = p + [x + 1 for x in p]
    return p''', 1)
mutant('l11 popcounts with bin', w, 'def popcounts(n):\n    return [bin(m).count("1") for m in range(1 << n)]', 8)

# ---- l12
w = W('l12-difference-arrays', 'screens', 4)
sol = w['solution']
mutant('l12 skips l == r', w, sol.replace('    for l, r, v in updates:\n', '    for l, r, v in updates:\n        if l == r: continue\n'), 2)
NCELLS = sol.replace('[0] * (n + 1)', '[0] * n')
mutant('l12 n cells fails the first test', w, NCELLS, 1)
mutant('l12 test-3 line names a list of n cells, which fails test 1', w, NCELLS, 3, finding=16)
mutant('l12 scan every update for each day', w, '''def apply_ranges(n, updates):
    return [sum(u[2] for u in updates if u[0] <= i <= u[1]) for i in range(n)]''', 7)
mutant('l12 loop over each range', w, '''def apply_ranges(n, updates):
    out = [0] * n
    for l, r, v in updates:
        for i in range(l, r + 1): out[i] += v
    return out''', 8, limit=CAP)
w = W('l12-difference-arrays', 'screens', 7)
sol = w['solution']
mutant('l12 coverage: -1 at r', w, sol.replace('d[r + 1] -= 1', 'd[r] -= 1'), 1)
mutant('l12 coverage: max over covered days only', w, '''def max_coverage(n, intervals):
    d = {}
    for l, r in intervals:
        for i in range(l, min(r, l + 50) + 1): d[i] = d.get(i, 0) + 1
    return max(d.values())''', 3)
mutant('l12 coverage: fill every day', w, '''def max_coverage(n, intervals):
    c = [0] * n
    for l, r in intervals:
        for i in range(l, r + 1): c[i] += 1
    return max(c) if c else 0''', 7, limit=CAP)

# ---- review-3
w = W('review-3', 'items', 1)
mutant('r3 ring: no n = 1 case', w, 'def ring_string(n):\n    return "ab" * (n // 2) + ("c" if n % 2 else "")', 1)
ALT = 'def ring_string(n):\n    if n == 1: return -1\n    return ("ab" * n)[:n]'
mutant('r3 ring: alternate only', w, ALT, 3)
mutant('r3 ring test-9 line names a wrong last letter for odd n, which fails test 3', w, ALT, 9, finding=17)

# ---- homework-1
w = W('homework-1', 'items', 0)
mutant('hw1 pairs: set of seen values', w, '''def count_pairs(xs, k):
    seen = set(); c = 0
    for x in xs:
        if k - x in seen: c += 1
        seen.add(x)
    return c''', 2, got=lambda g: g == 3)
mutant('hw1 pairs: every pair by index', w, '''def count_pairs(xs, k):
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] + xs[j] == k)''', 9)
mutant('hw1 pairs: xs.count in a loop', w, '''def count_pairs(xs, k):
    c = 0
    for x in xs:
        c += xs.count(k - x) - (1 if 2 * x == k else 0)
    return c // 2''', 10, limit=CAP)
mutant('hw1 pairs: walk a list of earlier positions', w, '''def count_pairs(xs, k):
    pos = {}; c = 0
    for i, x in enumerate(xs):
        for _ in pos.get(k - x, ()): c += 1
        pos.setdefault(x, []).append(i)
    return c''', 11, limit=6)
w = W('homework-1', 'items', 1)
mutant('hw1 window: at most k fills', w, 'def longest_window(tickers, k):\n    return min(len(tickers), k)', 1)
mutant('hw1 window: exactly k distinct', w, w['solution'].replace('best = max(best, right - left + 1)', 'best = max(best, right - left + 1) if len(counts) == k else best'), 8)
RESTART = '''def longest_window(tickers, k):
    t = tickers; n = len(t); best = 0
    for l in range(n):
        seen = set()
        for r in range(l, n):
            seen.add(t[r])
            if len(seen) > k: break
            best = max(best, r - l + 1)
    return best'''
mutant('hw1 window: restart at every day', w, RESTART, 9)
mutant('hw1 window: restart on a copy', w, RESTART.replace('t = tickers', 't = list(tickers)'), 11, limit=CAP)
ns = {}
exec(w['solution'].replace('            if counts[u] == 0:\n                del counts[u]\n', ''), ns)
try:
    ns['longest_window'](['C', 'A', 'B'], 1)
    ck('hw1 model mistake: no delete crashes on C A B', False)
except KeyError:
    ck('hw1 model mistake: no delete crashes on C A B', True)
w = W('homework-1', 'items', 2)
mutant('hw1 range sums: 0-based', w, w['solution'].replace('pre[r] - pre[l - 1]', 'pre[r + 1] - pre[l]'), 1)
mutant('hw1 range sums: sum per query', w, 'def range_sums(xs, queries):\n    return [sum(xs[l - 1:r]) for l, r in queries]', 6, limit=CAP)

# ---- homework-3
w = W('homework-3', 'items', 0)
sol = w['solution']
ATSTART = '''def fewest_alerts(windows):
    alerts = []
    for s, e in sorted(windows):
        if not any(s <= t <= e for t in alerts): alerts.append(s)
    return len(alerts)'''
mutant('hw3 alerts: alert at each start fails the first test', w, ATSTART, 1)
mutant("hw3 alerts test-2 line names an alert at a window's start, which fails test 1", w, ATSTART, 2, finding=18)
mutant('hw3 alerts: sort by start, alert at the end (the mistake that does reach test 2)', w, '''def fewest_alerts(windows):
    alerts = []
    for s, e in sorted(windows):
        if not any(s <= t <= e for t in alerts[-1:]): alerts.append(e)
    return len(alerts)''', 2)
mutant('hw3 alerts: >= for >', w, sol.replace('s > last', 's >= last'), 3)
mutant('hw3 alerts: check every alert', w, '''def fewest_alerts(windows):
    alerts = []
    for s, e in sorted(windows, key=lambda w: w[1]):
        if not any(s <= t for t in alerts): alerts.append(e)
    return len(alerts)''', 9, limit=CAP)
w = W('homework-3', 'items', 1)
mutant('hw3 spans: < for <=', w, w['solution'].replace('<= c', '< c'), 2)
WALK = '''def spans(closes):
    c = closes; out = []
    for i in range(len(c)):
        j = i
        while j > 0 and c[j - 1] <= c[i]: j -= 1
        out.append(i - j + 1)
    return out'''
mutant('hw3 spans: walk back', w, WALK, 7)
mutant('hw3 spans: walk back on a copy', w, WALK.replace('c = closes', 'c = list(closes)'), 8, limit=CAP)
w = W('homework-3', 'items', 2)
sol = w['solution']
mutant('hw3 cap: no -1 branch', w, sol.replace('    if not over(len(updates)):\n        return -1\n', ''), 3)
GE = sol.replace('run > cap', 'run >= cap')
NOCHECK = sol.replace('    if not over(len(updates)):\n        return -1\n', '')
mutant('hw3 cap: >= for > fails the first test', w, GE, 1, got=lambda g: g == 2)
mutant('hw3 cap test-4 line names >= for >, which fails test 1', w, GE, 4, finding=19)
mutant('hw3 cap test-10 line names a search with no -1 check, which fails test 3', w, NOCHECK, 10, finding=20)
mutant('hw3 cap: apply and scan per update', w, '''def first_over_cap(n, updates, cap):
    a = [0] * n
    for k, (l, r, v) in enumerate(updates, 1):
        for i in range(l, r + 1): a[i] += v
        if max(a) > cap: return k
    return -1''', 8, limit=CAP)

# ------------------------------------------------------------------ C. worked examples and claims
# l1
def highs(xs, strict=True):
    c, best = 0, None
    for x in xs:
        if best is None or (x > best if strict else x >= best):
            c += 1
            best = x if best is None else max(best, x)
    return c
ck('l1_fresh_highs', (highs([3, 1, 4, 1, 5, 9]), highs([7] * 4), highs([-5, -3, -4]), highs([-10**9]), highs([2, 2, 1, 3], False), highs([2, 2, 1, 3])) == (4, 1, 2, 1, 3, 2))
ck('l1 bounds', 2 * 10**5 * 10**9 == 2 * 10**14 > 2**31 - 1 and 10**5 * 10**6 == 10**11 and 3 * 10**5 - 9999 == 290001 and 10**4 * 2 * 10**5 == 2 * 10**9)
# l2
n = 2 * 10**5
ck('l2_counts', abs(n * (n + 1) * (n + 2) / 6 - 1.3e15) < 0.05e15 and n * n / 2 == 2e10)
lo, hi = 1, 10**8
while lo < hi:
    mid = (lo + hi + 1) // 2
    lo, hi = (mid, hi) if mid * math.log2(mid) <= 10**8 else (lo, mid - 1)
ck('l2_crossings', abs(lo - 4523071) <= 2 and math.isqrt(10**7) == 3162 and abs(1000 * math.log2(1000) - 9966) < 1 and abs(n * math.log2(n) - 3.5e6) < 0.05e6, lo)
ck('l2 boundaries', 2**26 <= 10**8 < 2**27 and 464**3 <= 10**8 < 465**3 and 500**3 == 1.25e8 and 5000 * 4999 // 2 == 12497500 and 2**30 >= 10**9 + 1 > 2**29 and 2**20 == 1048576)
r = random.Random(2)
for _ in range(300):
    a = [r.randint(-9, 9) for _ in range(r.randint(1, 8))]
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    if best != max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1)):
        ck('l2 single pass equals the best stretch', False, a)
        break
else:
    ck('l2 single pass equals the best stretch', True)
ns = {}
exec(W('l2-limits-to-complexity', 'screens', 10)['solution'], ns)
ck('l2 two pointers equal brute force', all(
    ns['pair_sums_at_most'](a, k) == sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] + a[j] <= k)
    for a, k in (([r.randint(-6, 6) for _ in range(r.randint(1, 7))], r.randint(-12, 12)) for _ in range(500))))
# l3
toks = '3\n2\n5 7\n1\n-4\n3\n1 2 3'.split()
ck('l3_tokens', len(toks) == 10 and toks[6] == '3' and len('2\n\n5 -3'.split()) == 3 and (b'3' == '3') is False and int(b'3') == 3 and int(b'12') == 12)
buf, feed = io.StringIO(), io.StringIO('2\n3\n4 1\n5\n2\n-1 -2\n')
with contextlib.redirect_stdout(buf):
    t = int(feed.readline())
    for _ in range(t):
        nn = int(feed.readline())
        a = list(map(int, feed.readline().split()))
        print(sum(a), max(a))
ck('l3_trap', buf.getvalue().split('\n')[:2] == ['5 4', '2 2'], buf.getvalue())
# l4
pre = {}
exec(W('l4-stress-testing', 'screens', 7)['prelude'], pre)
rng = random.Random(1)
cases = [pre['gen_pairs'](rng) for _ in range(5)]
ck('l4_trials', cases == [([10, 2], 10), ([8], 16), ([7, 4, 2, 8], 2), ([7, 10, 1, 8], 10), ([4, 10, 2, 6, 1, 1], 2)]
   and [(pre['fast_strict'](c), pre['brute_pairs'](c)) for c in cases] == [(0, 0), (0, 0), (0, 0), (2, 2), (0, 1)], cases)
ck('l4_shrink', [(pre['fast_strict'](c), pre['brute_pairs'](c)) for c in (([1, 1], 2), ([4, 10], 2), ([1], 2), ([6, 1, 1], 3), ([2, 3, 3], 6), ([5, 5, 1], 10), ([5, 5], 10), ([5, 5], 11))]
   == [(0, 1), (0, 0), (0, 0), (1, 1), (2, 3), (2, 3), (0, 1), (1, 1)])
found = 0
for seed in (1, 2, 3, 4):
    rng = random.Random(seed)
    for _ in range(100000):
        m = rng.randint(1, 6)
        xs = sorted(rng.randint(1, 10**9) for _ in range(m))
        k = rng.randint(2, 2 * 10**9)
        # a difference needs some pair summing to exactly k
        s = set(xs)
        if any(k - x in s and (k - x != x or xs.count(x) > 1) for x in xs):
            found += 1
ck('l4_gen_a: no exact tie in 4 x 100,000 trials', found == 0, found)
# l5
ck('l5_last_digit', [pow(7, k, 10) for k in (1, 2, 3, 4, 5, 2031)] == [7, 9, 3, 1, 7, 3] and 2031 == 4 * 507 + 3 and abs(10**18 * math.log10(2) - 3e17) < 0.02e17)
ck('l5_inverse_table', [pow(a, -1, 7) for a in range(1, 7)] == [1, 4, 5, 2, 3, 6] and all(
    int(c) == (i + 1) * j % 7 for i, row in enumerate(DOC['l5-modulo']['screens'][3]['canvas']['params']['rows']) for j, c in enumerate(row) if j))
ck('l5 small values', (38 * 45 % 7, 38 * 45, pow(3, 5, 7), pow(3, 13, 7), pow(3, 8, 7), 5 * pow(4, -1, 7) % 7, 2 * pow(5, 5, 7) % 7, 30 // 5 % 7, pow(4, -1, 11), pow(4, 9, 11))
   == (2, 1710, 5, 3, 2, 3, 6, 6, 3, 3))
h = 0
hs = []
for x in (5, 10**9, 3):
    h = (31 * h + x) % (10**9 + 7)
    hs.append(h)
ck('l5_checksum', hs == [5, 148, 4591] and 31 * (31 * 5 + 10**9) + 3 == 31000004808)
ck('l5 bits and primes', 2**59 < 10**18 < 2**60 and pow(2, -1, 10**9 + 7) == 500000004 and 10**9 + 7 < 2**30 and (10**9 + 6)**2 < 2**63 < (10**9 + 6)**3 and (-3) % 7 == 4)
try:
    import sympy
    ck('primes (sympy)', all(sympy.isprime(p) for p in (10**9 + 7, 2**31 - 1, 1000003, 999983, 999999999989)) and sympy.primepi(10**6) == 78498
       and sympy.primepi(2 * 10**6) == 148933 and sympy.primepi(100) == 25 and sympy.primepi(50) == 15)
    ns = {}
    exec(W('l6-gcd-and-primes', 'screens', 9)['solution'], ns)
    r = random.Random(6)
    ck('l6 factorise equals sympy.factorint', all(
        sorted(ns['factorise'](m)) == sorted(p for p, e in sympy.factorint(m).items() for _ in range(e))
        for m in (r.randint(1, 10**12) for _ in range(300))))
except ImportError:
    SKIP.append('sympy not installed: primality cross-checks skipped')
# l6
def steps(a, b):
    c = 0
    while b:
        a, b = b, a % b
        c += 1
    return c
fib = [0, 1]
while len(fib) < 90:
    fib.append(fib[-1] + fib[-2])
ck('l6_gears', math.lcm(84, 36) == 252 and 84 * 36 // 252 == 12 and math.gcd(1071, 462) == 21 and steps(89, 55) == 9
   and fib[88] == 1100087778366101931 and fib[87] == 679891637638612258 and steps(fib[88], fib[87]) == 86
   and math.lcm(14, 21) == 42 and math.gcd(252, 198) == 18 and math.lcm(4, 6, 10) == 60 and math.isqrt(1000003) == 1000)
g = DOC['l6-gcd-and-primes']['screens'][6]
cell = lambda v: 'r%dc%d' % ((v - 1) // 10 + 1, (v - 1) % 10 + 1)
dim = {cell(v) for v in range(1, 101) if v == 1 or any(v % p == 0 and v != p for p in (2, 3, 5))}
ck('l6_grid', set(g['canvas']['state']['dim']) == dim and set(g['widget']['only']) == {cell(v) for v in range(1, 101)} - dim
   and set(g['widget']['answer']) == {cell(49), cell(77), cell(91)} and len(g['widget']['only']) == 28)
ns = {}
exec(W('l6-gcd-and-primes', 'screens', 5)['solution'], ns)
r = random.Random(7)
ck('l6 gcd equals math.gcd', all(ns['gcd'](a, b) == math.gcd(a, b) for a, b in ((r.randint(0, 10**18), r.randint(0, 10**18)) for _ in range(2000))))
# l7
ck('l7_lattice', (math.comb(4, 2), math.comb(5, 2), math.comb(6, 3)) == (6, 10, 20) and len(str(math.comb(2000, 1000))) == 601 and len(str(math.comb(252, 126))) == 75)
digits = (math.lgamma(10**6 + 1) - 2 * math.lgamma(5 * 10**5 + 1)) / math.log(10)
ck('l7 C(10^6, 5*10^5) has 301,027 digits', math.floor(digits) + 1 == 301027, digits)
f13 = [math.factorial(i) % 13 for i in range(7)]
ck('l7_tables13', f13 == [1, 1, 2, 6, 11, 3, 5] and [pow(x, -1, 13) for x in f13] == [1, 1, 7, 11, 6, 9, 8] and pow(5, 11, 13) == 8 and 5 * 11 * 11 % 13 == 7 == 20 % 13 and 5 * 6 * 6 % 13 == 11)
def splits(lots, desks, least=0):
    return sum(1 for c in itertools.product(range(lots + 1), repeat=desks) if sum(c) == lots and min(c) >= least)
ck('stars and bars', (splits(5, 3), splits(4, 3), splits(10, 4), splits(12, 3, 2), splits(12, 3, 1), splits(12, 3)) == (21, 15, 286, 28, 55, 91)
   and (math.comb(7, 3), math.comb(13, 4), math.comb(10, 6), 10 * 9 * 8 * 7) == (35, 715, 210, 5040))
# l8
def moves(s):
    out = {}
    for i in range(3):
        if s[i] >= 2:
            t = list(s)
            for j in range(3):
                t[j] += -2 if i == j else 1
            out['ABC'[i]] = tuple(t)
    return out
def closure(start):
    seen, q = {start}, deque([start])
    while q:
        for t in moves(q.popleft()).values():
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen
reach = closure((3, 2, 1))
st = DOC['l8-invariants']['screens'][0]['widget']['states']
ok = len(st) == 9 == len(reach)
for name, s in st.items():
    pos = tuple(int(c) for c in name[1:])
    mv = moves(pos)
    for op in s['ops']:
        box = op['label'][-1]
        ok = ok and ((box not in mv) if op.get('reject') else (st and tuple(int(c) for c in op['to'][1:]) == mv.get(box)))
ck('l8_tokens', ok and all((a - b) % 3 == 1 for a, b, c in reach) and not any(6 in s for s in reach)
   and {tuple(map(int, row)) for row in DOC['l8-invariants']['screens'][1]['canvas']['params']['rows']} == reach
   and len(closure((4, 1, 1))) == 7 and all(6 not in s for s in closure((4, 1, 1))))
def finals(xs):
    if len(xs) == 1:
        return {xs[0]}
    out = set()
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            out |= finals(tuple(sorted(xs[:i] + xs[i + 1:j] + xs[j + 1:] + (abs(xs[i] - xs[j]),))))
    return out
ck('l8 difference game', finals((3, 5, 6, 9)) == {1, 5, 7} and all(v % 2 == 1 for v in finals(tuple(range(1, 8)) + (9,))))
ns = {}
exec(W('l8-invariants', 'screens', 7)['solution'], ns)
LIM = 12
def bfs_reach(x, y):
    seen, q = {(x, y)}, deque([(x, y)])
    while q:
        a, b = q.popleft()
        for t in ((a + b, b), (a, a + b)):
            if max(t) <= LIM and t not in seen:
                seen.add(t)
                q.append(t)
    return seen
ok = True
for x in range(1, LIM + 1):
    for y in range(1, LIM + 1):
        rs = bfs_reach(x, y)
        for c in range(1, LIM + 1):
            for d in range(1, LIM + 1):
                ok = ok and ns['can_reach'](x, y, c, d) == ((c, d) in rs)
ck('l8 can_reach equals breadth-first search for all values up to 12', ok)
ck('l8 pair game facts', (7, 5) in bfs_reach(1, 1) and (6, 4) not in bfs_reach(1, 1) and (2, 7) not in bfs_reach(3, 2) and (10, 4) not in bfs_reach(1, 1) and (12, 7) in bfs_reach(1, 1)
   and 8440 + 30 * 52 == 10000 and 8440 + 30 * 55 == 10090 and 8990 + 10 * 55 == 9540 and 8990 + 20 * 55 == 10090)
dark = DOC['l8-invariants']['screens'][3]['canvas']['state']['shade']['dark']['ids']
ck('l8 chessboard', len(dark) == 30 and all((int(c[1]) + int(c[3])) % 2 == 0 for c in dark))
# l9
def valid(p):
    return all(abs(p[i] - p[i + 1]) != 1 for i in range(len(p) - 1))
cnt = {m: sum(1 for p in itertools.permutations(range(1, m + 1)) if valid(p)) for m in range(1, 6)}
ck('l9 orders', cnt[1] == 1 and cnt[2] == 0 and cnt[3] == 0 and cnt[4] == 2 and all(valid(list(range(2, m + 1, 2)) + list(range(1, m + 1, 2))) for m in range(4, 2001))
   and [valid(p) for p in ([2, 4, 1, 3, 5], [5, 3, 1, 4, 2], [1, 3, 5, 2, 4], [1, 3, 5, 4, 2])] == [True, True, True, False])
ck('l9 bounded sum', all((s in {sum(c) for c in itertools.product(range(1, k + 1), repeat=m)}) == (m <= s <= m * k)
                         for m in range(1, 5) for k in range(1, 5) for s in range(0, 20)) and 250 + 250 + 200 + 300 == 1000 and 167 * 4 + 166 * 2 == 1000)
# l10
SIX = [(0, 13), (1, 5), (4, 7), (6, 11), (9, 15), (12, 14)]
def best_set(iv, strict=False):
    best = [[]]
    for m in range(1, 1 << len(iv)):
        c = sorted(iv[i] for i in range(len(iv)) if m >> i & 1)
        if all((c[i][1] < c[i + 1][0]) if strict else (c[i][1] <= c[i + 1][0]) for i in range(len(c) - 1)):
            if len(c) > len(best[0]):
                best = [c]
            elif len(c) == len(best[0]):
                best.append(c)
    return best
def greedy(iv, key):
    kept = []
    for s, e in sorted(iv, key=key):
        if all(s >= e2 or e <= s2 for s2, e2 in kept):
            kept.append((s, e))
    return len(kept)
b = best_set(SIX)
AUC = [(0, 30), (5, 10), (10, 25), (20, 35), (25, 40), (35, 50), (45, 60), (50, 55)]
R3 = [(0, 7), (1, 3), (3, 5), (5, 8), (8, 10), (4, 9)]
ck('l10 six meetings', b == [[(1, 5), (6, 11), (12, 14)]] and (greedy(SIX, lambda x: x[1] - x[0]), greedy(SIX, lambda x: x[0]), greedy(SIX, lambda x: x[1])) == (2, 1, 3)
   and len(best_set(AUC)[0]) == 4 == greedy(AUC, lambda x: x[1]) and greedy(AUC, lambda x: x[0]) == 3
   and len(best_set(R3)[0]) == 4 and greedy(R3, lambda x: x[0]) == 2
   and len(best_set([(1, 3), (3, 5), (5, 7)])[0]) == 3 and len(best_set([(1, 3), (3, 5), (5, 7)], True)[0]) == 2
   and len(best_set([(1, 4), (4, 6), (6, 9), (2, 5)])[0]) == 3 and len(best_set([(2, 9), (3, 4), (1, 6)])[0]) == 1)
ns = {}
exec(W('l10-greedy-proofs', 'screens', 4)['solution'] + W('l10-greedy-proofs', 'screens', 6)['solution'], ns)
r = random.Random(10)
ok = ok2 = True
for _ in range(2000):
    iv = []
    for _ in range(r.randint(1, 7)):
        s = r.randint(0, 9)
        iv.append((s, s + r.randint(1, 5)))
    ok = ok and ns['max_non_overlapping'](iv) == len(best_set(iv)[0])
    ok2 = ok2 and ns['min_rooms'](iv) == max(sum(1 for s, e in iv if s <= t + 0.5 < e) for t in range(0, 15))
ck('l10 earliest finish equals brute force on 2,000 instances', ok)
ck('l10 min_rooms equals the peak count on 2,000 instances', ok2)
ck('l10 rooms examples', ns['min_rooms'](SIX) == 3 and ns['min_rooms']([(0, 4), (1, 3), (2, 6), (3, 5), (5, 7)]) == 3)
def coins(cs, amount):
    best = [0] + [10**9] * amount
    for a in range(1, amount + 1):
        best[a] = min(best[a - c] + 1 for c in cs if c <= a)
    g, left = 0, amount
    for c in sorted(cs, reverse=True):
        g += left // c
        left %= c
    return g, best[amount]
first_bad = lambda cs, top: next((a for a in range(1, top) if coins(cs, a)[0] != coins(cs, a)[1]), None)
ck('greedy coins', first_bad([1, 3, 4], 50) == 6 and first_bad([1, 5, 6], 50) == 10 and first_bad([1, 5, 10, 20, 25], 100) == 40 and first_bad([1, 2, 5, 10], 1000) is None
   and coins([1, 5, 6], 15) == (5, 3) and coins([1, 4, 6], 8) == (3, 2) and coins([1, 5, 6], 10) == (5, 2))
# l11
P4, R4 = [5, 4, 3, 7], [3, 2, 2, 4]
opts = sorted(((sum(P4[i] for i in range(4) if m >> i & 1), m) for m in range(16) if sum(R4[i] for i in range(4) if m >> i & 1) <= 6), reverse=True)
ck('l11 four trades', opts[0] == (11, 0b1010) and opts[1][0] < 11)
ck('l11 bit operations', (10 >> 1 & 1, 10 | 1 << 2, 10 & -10, bin(10).count('1'), len(range(1 << 4 - 1)), 13, 22, 26, 20) == (1, 14, 2, 2, 8, 0b1101, 0b10110, 0b11010, 0b10100)
   and sum(2**bin(m).count('1') for m in range(8)) == 27 and 3**16 == 43046721 and 2**10 * 10 == 10240 and math.factorial(9) == 362880
   and 2**16 * 16**2 == 16777216 and 2 * 2**20 == 2097152 and 2**12 * 12 == 49152 and sum(bin(m).count('1') for m in range(4096)) == 24576 and 18 * 2**17 == 2359296)
sub, order = 0b1011, []
while sub:
    order.append(sub)
    sub = (sub - 1) & 0b1011
ck('l11 submask order', order == [0b1011, 0b1010, 0b1001, 0b1000, 0b0011, 0b0010, 0b0001])
r = random.Random(11)
ns = {}
exec(W('l11-bitmasks', 'screens', 3)['solution'], ns)
ok = True
for _ in range(300):
    m = r.randint(0, 8)
    p, q, lim = [r.randint(1, 20) for _ in range(m)], [r.randint(1, 9) for _ in range(m)], r.randint(0, 30)
    dp = [0] * (lim + 1)
    for pi, qi in zip(p, q):
        for c in range(lim, qi - 1, -1):
            dp[c] = max(dp[c], dp[c - qi] + pi)
    ok = ok and ns['best_subset'](p, q, lim) == dp[lim]
ck('l11 best_subset equals the knapsack DP', ok)
def mitm(p, q, lim):
    h = len(p) // 2
    def lst(pp, qq):
        return [(sum(qq[i] for i in range(len(pp)) if m >> i & 1), sum(pp[i] for i in range(len(pp)) if m >> i & 1)) for m in range(1 << len(pp))]
    right = sorted(lst(p[h:], q[h:]))
    risks, bestp, run = [], [], 0
    for rk, pf in right:
        run = max(run, pf)
        risks.append(rk)
        bestp.append(run)
    best = 0
    for rk, pf in lst(p[:h], q[:h]):
        if rk <= lim:
            best = max(best, pf + bestp[bisect.bisect_right(risks, lim - rk) - 1])
    return best
ck('l11 meet in the middle equals enumeration', all(mitm(p, q, lim) == ns['best_subset'](p, q, lim) for p, q, lim in
                                                    (([r.randint(1, 50) for _ in range(10)], [r.randint(1, 9) for _ in range(10)], r.randint(0, 40)) for _ in range(30))))
# l12
def diff(n, ups):
    d = [0] * (n + 1)
    for l, rr, v in ups:
        d[l] += v
        d[rr + 1] -= v
    return d
def totals(d):
    out, run = [], 0
    for x in d[:-1]:
        run += x
        out.append(run)
    return out
d = diff(8, [(1, 4, 3), (2, 6, 2), (5, 7, 1)])
ck('l12 frames', d == [0, 3, 2, 0, 0, -2, 0, -2, -1] and totals(d) == [0, 3, 5, 5, 5, 3, 3, 1]
   and diff(5, [(0, 2, 5), (1, 3, -2)]) == [5, -2, 0, -5, 2, 0] and totals(diff(5, [(0, 2, 5), (1, 3, -2)])) == [5, 3, 3, -2, 0]
   and diff(6, [(0, 5, 2), (2, 2, 5), (3, 5, -1)]) == [2, 0, 5, -6, 0, 0, -1] and totals(diff(6, [(0, 5, 2), (2, 2, 5), (3, 5, -1)])) == [2, 2, 7, 1, 1, 1]
   and totals(diff(10, [(1, 5, 1), (2, 8, 1), (4, 9, 1), (6, 7, 1), (0, 3, 1)])) == [1, 2, 3, 3, 3, 3, 3, 3, 2, 1] and 300 - 100 + 200 == 400)
nodown = lambda n, ups: totals([x if x > 0 else 0 for x in diff(n, ups)])  # the trap: the -v marks left out (v > 0 here)
ck('l12 trap', nodown(8, [(2, 7, 4), (5, 7, 1)]) == [0, 0, 4, 4, 4, 5, 5, 5] == totals(diff(8, [(2, 7, 4), (5, 7, 1)])) and nodown(8, [(1, 4, 3)])[5:] == [3, 3, 3])
r = random.Random(12)
bad = 0
for _ in range(1000):
    m = 8
    ups = []
    for _ in range(3):
        l = r.randint(0, m - 1)
        ups.append((l, r.randint(l, m - 1), r.randint(1, 9)))
    bad += nodown(m, ups) != totals(diff(m, ups))
ck('l12 the missing -v shows on more than 90% of random cases (8 days, 3 updates)', bad > 900, bad)
g2 = [[0] * 5 for _ in range(5)]
for (i, j), v in {(1, 1): 1, (1, 3): -1, (3, 1): -1, (3, 3): 1}.items():
    g2[i][j] += v
for row in g2:
    for j in range(1, 5):
        row[j] += row[j - 1]
for i in range(1, 5):
    for j in range(5):
        g2[i][j] += g2[i - 1][j]
ck('l12 two dimensions', g2 == [[1 if 1 <= i <= 2 and 1 <= j <= 2 else 0 for j in range(5)] for i in range(5)])
r = random.Random(12)
tot = 0
for _ in range(100000):
    l = r.randint(0, 199999)
    tot += r.randint(l, 199999) - l + 1
    r.randint(-1000, 1000)
ck('l12 test 8 range loop is about 5e9 additions', 4.9e9 < tot < 5.1e9, tot)
r = random.Random(13)
tot = 0
for _ in range(100000):
    a, b = r.randint(0, 199999), r.randint(0, 199999)
    tot += abs(a - b) + 1
ck('l12 coverage test 7 averages about 66,500 days', abs(tot / 100000 - 66500) < 700, tot / 100000)
# reviews and homework
ck('review numbers', abs(2000**2 * math.log2(2000) - 4.4e7) < 0.05e7 and pow(3, -1, 10**9 + 7) == 333333336 and pow(3, 10**18, 7) == 4 and 10**18 % 6 == 4
   and pow(3, 10**18 % 7, 7) == 3 and pow(0, 5, 7) == 0 and math.comb(8, 1) % 7 == 1 and pow(3, 200, 13) == 9 and 200 % 12 == 8 and 2 * 10**5 * 18 * 3 == 1.08e7
   and math.comb(200000, 2) == 19999900000 and math.comb(6, 2) == 15 and math.factorial(12) == 479001600)
try:
    int('\n')
    ck("review-1: int('\\n') raises ValueError", False)
except ValueError:
    ck("review-1: int('\\n') raises ValueError", True)
G = lambda m: sum(math.gcd(i, m) for i in range(1, m + 1))
ck('hw2 gcd sum closed forms', G(6) == 15 and G(12) == 40 and all(G(p**a) == (a + 1) * p**a - a * p**(a - 1) for p in (2, 3, 5, 7) for a in (1, 2, 3))
   and all(G(a * b) == G(a) * G(b) for a in range(1, 30) for b in range(1, 30) if math.gcd(a, b) == 1)
   and 42 * 2**39 == 23089744183296 and (13 * 2**12 - 12 * 2**11) * (13 * 5**12 - 12 * 5**11) == 74200000000000 and (2 * 999983 - 1) * (2 * 1000003 - 1) == 3999939999825)
Z = lambda k: sum(k // 5**i for i in range(1, 30))
ns = {}
exec(W('homework-2', 'items', 1)['solution'], ns)
zs, k, ok = [], 0, True
for m in range(0, 2001):
    while Z(k) < m:
        k += 1
    ok = ok and ns['smallest_k'](m) == k
ck('hw2 smallest_k equals a linear scan up to m = 2,000', ok and Z(24) == 4 and Z(25) == 6 and all(Z(5 * m) >= m for m in range(0, 3000)))
ck('hw2 Fermat example', [3 * i % 7 for i in range(1, 7)] == [3, 6, 2, 5, 1, 4])
ns = {}
exec(W('homework-3', 'items', 0)['solution'], ns)
r = random.Random(30)
ok = True
for _ in range(300):
    ws = []
    for _ in range(r.randint(1, 6)):
        s = r.randint(0, 8)
        ws.append((s, s + r.randint(0, 4)))
    pts = sorted({e for s, e in ws})
    brute = next(k for k in range(1, len(pts) + 1) if any(all(any(s <= t <= e for t in c) for s, e in ws) for c in itertools.combinations(pts, k)))
    ok = ok and ns['fewest_alerts'](ws) == brute
ck('hw3 fewest_alerts equals brute force on 300 instances', ok)
ck('hw3 derangement constructions', all(all(p != i + 1 for i, p in enumerate(list(range(2, m + 1)) + [1])) for m in range(2, 51))
   and [3, 2, 1][1] == 2)
def lateness(order, jobs, release=False, total=False):
    t, out = 0, []
    for j in order:
        p, d, rdy = jobs[j]
        t = max(t, rdy if release else 0) + p
        out.append(max(0, t - d))
    return sum(out) if total else max(out)
r = random.Random(31)
ok = True
for _ in range(3000):
    jobs = [(r.randint(1, 6), r.randint(0, 15), 0) for _ in range(r.randint(1, 6))]
    edd = sorted(range(len(jobs)), key=lambda j: jobs[j][1])
    ok = ok and lateness(edd, jobs) == min(lateness(o, jobs) for o in itertools.permutations(range(len(jobs))))
ck('hw3 due order minimises the worst lateness on 3,000 instances', ok)
J1 = [(5, 7, 0), (1, 6, 5)]
J2 = [(4, 10, 0), (1, 2, 1)]
J3 = [(5, 1, 0), (1, 2, 0)]
ck('hw3 counter-examples', (lateness([1, 0], J1, True), lateness([0, 1], J1, True)) == (4, 0) and (lateness([0, 1], J2, True), lateness([1, 0], J2, True)) == (3, 0)
   and (lateness([0, 1], J3, total=True), lateness([1, 0], J3, total=True), lateness([0, 1], J3), lateness([1, 0], J3)) == (8, 5, 4, 5))

# ------------------------------------------------------------------ D. speed claims (ratios, wide margins)
def best_time(f, reps=3):
    out = []
    for _ in range(reps):
        t0 = time.perf_counter()
        f()
        out.append(time.perf_counter() - t0)
    return min(out)
IN = os.path.join(CTMP, 'in.txt')
open(IN, 'w').write('200000\n' + '\n'.join(str(i) for i in range(200000)) + '\n')
def read_a():
    old, sys.stdin = sys.stdin, open(IN)
    try:
        nn = int(input())
        return [int(input()) for _ in range(nn)]
    finally:
        sys.stdin.close()
        sys.stdin = old
def read_b():
    old, sys.stdin = sys.stdin, open(IN)
    try:
        data = sys.stdin.buffer.read().split()
        return list(map(int, data[1:int(data[0]) + 1]))
    finally:
        sys.stdin.close()
        sys.stdin = old
ta, tb = best_time(read_a), best_time(read_b)
ck('l3_read_timing: read().split() is more than 1.5 times faster than input() per line', 1.5 * tb < ta, (ta, tb))
out_lines = list(range(100000))
dn = open(os.devnull, 'w')
def p_loop():
    for x in out_lines:
        print(x, file=dn)
def p_join():
    print('\n'.join(map(str, out_lines)), file=dn)
tl, tj = best_time(p_loop), best_time(p_join)
ck('l3_print_timing: one join beats a print per line', tj < tl, (tl, tj))
P = 10**9 + 7
def build(nn):
    fact = [1] * (nn + 1)
    for i in range(1, nn + 1):
        fact[i] = fact[i - 1] * i % P
    inv = [1] * (nn + 1)
    inv[nn] = pow(fact[nn], P - 2, P)
    for k in range(nn, 0, -1):
        inv[k - 1] = inv[k] * k % P
    return fact
def build_pow(nn):
    fact = build(nn)
    return [pow(x, P - 2, P) for x in fact]
t1, t2 = best_time(lambda: build(200000), 2), best_time(lambda: build_pow(200000), 2)
ck('l7 one pow per entry is several times slower than the backward loop', t2 > 3 * t1, (t1, t2))
if CXX:
    IOSRC = '''#include <iostream>
int main(int argc, char** argv) {
    int mode = argv[1][0] - '0';  // 0: neither line; 1: both lines and '\\n'; 2: both lines and std::endl
    if (mode) { std::ios::sync_with_stdio(false); std::cin.tie(nullptr); }
    long long x;
    if (mode == 2) { while (std::cin >> x) std::cout << x << std::endl; }
    else { while (std::cin >> x) std::cout << x << '\\n'; }
}
'''
    exe = cpp_build(IOSRC, 'io')
    NUMS = os.path.join(CTMP, 'nums.txt')
    rr = random.Random(1)
    open(NUMS, 'w').write('\n'.join(str(rr.randint(-10**9, 10**9)) for _ in range(500000)) + '\n')
    def io_time(mode):
        def go():
            with open(NUMS) as fi, open(os.path.join(CTMP, 'out.txt'), 'w') as fo:
                subprocess.run([exe, str(mode)], stdin=fi, stdout=fo)
        return best_time(go)
    c0, c1, c2 = io_time(0), io_time(1), io_time(2)
    ck('l3_cpp_timing: both lines beat neither, and std::endl gives much of it back', 2 * c1 < c0 and 1.5 * c1 < c2, (c0, c1, c2))
t0 = time.perf_counter()
s = 0
for i in range(10**7):
    s += i
t_add = time.perf_counter() - t0
ck('l2_additions: 10^7 additions take between 0.03 s and 5 s', 0.03 < t_add < 5, t_add)
print('info: 10^7 additions %.2f s; reading 200,000 lines %.3f s against %.3f s; permutation search on all 9 tests %.1f s' % (t_add, ta, tb, t_perm))

shutil.rmtree(CTMP, ignore_errors=True)
for sk in SKIP:
    print('skipped:', sk)
print('%d checks, %d failing' % (N[0], len(FAIL)))
for f in FAIL:
    print('  FAIL', f)
sys.exit(1 if FAIL else 0)
