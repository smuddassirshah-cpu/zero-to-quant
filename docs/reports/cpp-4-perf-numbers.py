"""cpp level 4 performance task h4-test-median: the learner writes the unit tests.

Route A: the widget's prelude (the course's test stand-in and median_volume with
five planted slips), a test suite and the postlude are compiled natively with
g++ and clang++ at -std=c++20 -O1 -fno-exceptions -D_GLIBCXX_ASSERTIONS (the
stand-in for the app's libc++ hardening), then run once per hidden test with its
stdin, as the app does. The model suite and a second suite on other inputs must
pass all six; the starter and seven planted weak suites must each fail one.
Route B: every value the model suite pins is recomputed in Python by
statistics.median and by a hand sort, and each slip's value on those inputs is
recomputed with 32-bit int arithmetic to show which test catches it.
"""
import json, os, shutil, statistics, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'cpp', 'homework-4.json')
items = json.load(open(HW))['items']
idx = next(k for k, i in enumerate(items) if i['id'] == 'h4-test-median')
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
check(idx == len(items) - 1 and len(items) == 9, 'appended as item 9 of 9 (index 8)')
check(3 <= len(T) <= 15 and len(T) > len(W['examples']), 'more tests than examples, at most 15')
check(all(e in T for e in W['examples']), 'the example is also a test')
check(len(T) == 6 and 'Tests 2 to 6' in W['how'], 'how: test 1 real, tests 2 to 6 slips')
check('five slips' in item['feedback']['correct'] and len(T) - 1 == 5, 'feedback: five slips')
check(not item.get('hints'), 'no hints')

# ---- route B --------------------------------------------------------------
def wrap(x):
    return ((x + 2 ** 31) % 2 ** 32) - 2 ** 31

def median_a(v):
    return 0.0 if not v else float(statistics.median(v))

def median_b(v):
    s = sorted(v); n = len(s)
    if n == 0: return 0.0
    return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

def slip(v, k):
    """What planted slip k returns (None: the run stops)."""
    if not v:
        return None if k == 5 else 0.0
    s = list(v) if k == 1 else sorted(v); n = len(s)
    if n % 2 == 1 or k == 4: return float(s[n // 2])
    a, b = s[n // 2 - 1], s[n // 2]
    if k == 2:
        q = wrap(a + b); return float(int(q / 2))      # C++ int division truncates toward zero
    if k == 3: return wrap(a + b) / 2.0
    return (a + b) / 2

PINS = [([300, 100, 200], 200.0), ([700, 100, 400, 301], 350.5), ([2000000000, 1999999999], 1999999999.5),
        ([5000], 5000.0), ([], 0.0)]
sol = W['solution']
for v, want in PINS:
    check(median_a(v) == median_b(v) == want, 'median of %s is %s by both routes' % (v, want))
    shown = ('{%s}' % ', '.join(str(x) for x in v)) if v else '{}'
    check('median_volume(%s)' % shown in sol, 'the model suite calls median_volume(%s)' % shown)
check('(301 + 400) / 2' in sol and (301 + 400) / 2 == 350.5, 'comment: (301 + 400) / 2 = 350.5')
check(all(0 <= x <= 2000000000 for v, _ in PINS for x in v), 'every pinned volume is in 0..2,000,000,000')
check(2000000000 + 1999999999 > 2 ** 31 - 1, 'the two big middles overflow an int sum')
check(wrap(2000000000 + 1999999999) == -294967297, 'the int sum wraps to -294,967,297')
for k in range(1, 6):
    caught = [v for v, want in PINS if slip(v, k) != want]
    check(len(caught) >= 1, 'slip %d differs from the real median on %s' % (k, caught))
check(slip([700, 100, 400, 301], 2) == 350.0 and slip([700, 100, 400, 301], 4) == 400.0
      and slip([300, 100, 200], 1) == 100.0, 'slip values: 350, 400 and 100')

# ---- route A: native builds -------------------------------------------------
FLAGS = ['-std=c++20', '-O1', '-fno-exceptions', '-D_GLIBCXX_ASSERTIONS', '-w']

def norm(s):
    return ' '.join(s.split())

def run_suite(code, cxx):
    tmp = tempfile.mkdtemp()
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(W['prelude'] + code + W['postlude'])
    cp = subprocess.run([cxx] + FLAGS + [src, '-o', exe], capture_output=True, text=True)
    res = [False] * len(T)
    if cp.returncode == 0:
        for k, t in enumerate(T):
            pr = subprocess.run([exe], input=t['stdin'], capture_output=True, text=True, timeout=20)
            if t['compare'] == 'raises':
                res[k] = pr.returncode != 0
            else:
                res[k] = pr.returncode == 0 and norm(pr.stdout) == norm(t['expect'])
    elif os.environ.get('SHOWERR'):
        print(cp.stderr[:3000])
    shutil.rmtree(tmp)
    return res

HEAD = '// Tests for median_volume(volumes), which is supplied.\n'
ALT = HEAD + r'''
TEST(shuffled_five) { CHECK(median_volume({9, 1, 7, 3, 5}) == 5.0); }
TEST(pair_with_half) { CHECK(median_volume({4, 1, 2, 3}) == 2.5); }
TEST(upper_middle_not_taken) { CHECK(median_volume({10, 20, 40, 1000}) == 30.0); }
TEST(near_the_limit) { CHECK(median_volume({2000000000, 2000000000, 0, 1999999998}) == 1999999999.0); }
TEST(empty_is_zero) { double m = median_volume({}); CHECK(m == 0.0); }
'''
WEAK = {
    'odd counts only': HEAD + 'TEST(a) { CHECK_CLOSE(median_volume({300, 100, 200}), 200.0, 1e-9); }\nTEST(b) { CHECK_CLOSE(median_volume({}), 0.0, 1e-9); }\n',
    'even test whose middles have an even sum': HEAD + 'TEST(a) { CHECK_CLOSE(median_volume({5, 1, 4, 2}), 3.0, 1e-9); }\nTEST(b) { CHECK_CLOSE(median_volume({3, 1, 2}), 2.0, 1e-9); }\nTEST(c) { CHECK_CLOSE(median_volume({}), 0.0, 1e-9); }\n',
    'no empty list': sol.replace('TEST(no_volumes_give_zero) {\n    CHECK_CLOSE(median_volume({}), 0.0, 1e-12);\n}\n', ''),
    'sorted inputs only': sol.replace('{300, 100, 200}', '{100, 200, 300}').replace('{700, 100, 400, 301}', '{100, 301, 400, 700}').replace('{2000000000, 1999999999}', '{1999999999, 2000000000}'),
    'a wrong hand value (2 for 1, 2, 3, 4)': sol + 'TEST(wrong) { CHECK_CLOSE(median_volume({1, 2, 3, 4}), 2.0, 1e-9); }\n',
    'a tolerance of 0.5 on the even test, no large volumes': sol.replace('350.5, 1e-9', '350.5, 0.5').replace('{2000000000, 1999999999}), 1999999999.5', '{2000, 1999}), 1999.5'),
    'large volumes that fit an int sum': sol.replace('{2000000000, 1999999999}), 1999999999.5', '{1000000000, 1000000000}), 1000000000.0'),
}
for name, code in WEAK.items():
    check(code != sol, 'weak suite built: ' + name)

cxxs = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(len(cxxs) == 2, 'g++ and clang++ both present')
for cxx in cxxs:
    r = run_suite(sol, cxx)
    check(all(r), '%s: model suite passes all %d tests %s' % (cxx, len(r), r))
    r = run_suite(ALT, cxx)
    check(all(r), '%s: a second suite on other inputs passes all %d tests' % (cxx, len(r)))
    r = run_suite(W['starter'], cxx)
    check(not any(r), '%s: starter fails all tests %s' % (cxx, r))
    for name, code in WEAK.items():
        r = run_suite(code, cxx)
        check(not all(r), '%s: weak suite "%s" fails tests %s' % (cxx, name, [k + 1 for k, ok in enumerate(r) if not ok]))

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
