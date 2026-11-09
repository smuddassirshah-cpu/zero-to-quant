"""cpp level 1 performance task h-tick-rule: recompute every number and run the
solution, the starter and planted wrong solutions against every hidden test.

Route A: each hidden test is compiled and run natively with g++ and clang++ at
-std=c++20 -O1 -fno-exceptions, with library bounds checks on
(-D_GLIBCXX_ASSERTIONS, the stand-in for the app's libc++ hardening), and the
printed value is compared with the JSON expect. Route B: every expect is
recomputed in Python twice, by a forward pass that carries the sign and by a
backward search for the last different price. Exit 0 only if all agree, the
solution passes every test on both compilers, the starter fails, and every
planted slip fails at least one hidden test.
"""
import json, os, random, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'cpp', 'homework-1.json')
items = json.load(open(HW))['items']
idx = next(k for k, i in enumerate(items) if i['id'] == 'h-tick-rule')
item = items[idx]
W = item['widget']
fails = []

def check(cond, msg):
    print('ok  ' if cond else 'FAIL', msg)
    if not cond:
        fails.append(msg)

# ---- shape --------------------------------------------------------------
check(item.get('performance') == 'code' and W['language'] == 'cpp', 'performance code item in C++')
check(idx == len(items) - 1 and len(items) == 9, 'appended as item 9 of 9 (index 8)')
check(3 <= len(W['tests']) <= 15 and len(W['tests']) > len(W['examples']), 'more tests than examples, at most 15')
check(all(e in W['tests'] for e in W['examples']), 'the example is also a test')
check('10 hidden tests' in W['how'] and len(W['tests']) == 10, 'how says 10 hidden tests')
check(not item.get('hints'), 'no hints')

# ---- route B: two Python models -------------------------------------------
def forward(p, s):
    total, sign = 0, 0
    for i in range(1, len(p)):
        if p[i] > p[i - 1]: sign = 1
        elif p[i] < p[i - 1]: sign = -1
        total += sign * s[i]
    return total

def backward(p, s):
    total = 0
    for i in range(len(p)):
        j = i
        while j > 0 and p[j] == p[j - 1]:
            j -= 1          # walk back over flats to the last move
        sign = 0 if j == 0 else (1 if p[j] > p[j - 1] else -1)
        total += sign * s[i]
    return total

for k, t in enumerate(W['tests']):
    a, b = t['args']
    check(len(a) == len(b), 'test %d: equal lengths' % (k + 1))
    check(all(1 <= x <= 2000000000 for x in b), 'test %d: sizes in 1..2,000,000,000' % (k + 1))
    f, g = forward(a, b), backward(a, b)
    check(f == g == t['expect'], 'test %d: expect %d, forward %d, backward %d' % (k + 1, t['expect'], f, g))
    check(abs(t['expect']) < 2 ** 53, 'test %d: exact as a JSON number' % (k + 1))

# the seeded case is reproducible
rng = random.Random(20261109)
p = [1000]
for _ in range(29): p.append(p[-1] + rng.choice([-1, 0, 0, 1]))
s = [rng.randint(1, 2000000000) for _ in range(30)]
check(W['tests'][9]['args'] == [p, s], 'test 10 is the seed-20261109 walk')

# numbers in the text
INT_MAX = 2 ** 31 - 1
check(INT_MAX == 2147483647 and '2,147,483,647' in item['explain']['text'], 'int limit 2,147,483,647 stated right')
check(2 * 2000000000 > INT_MAX and '2,000,000,000' in item['explain']['text'], 'two sizes of 2,000,000,000 pass the int limit')
check('2,000,000,000' in item['prose'], 'size range stated in the prose')
ex = W['examples'][0]
check(ex['expect'] == 0 * 500 + 200 + 300 - 400 + 100 == 200, 'example: 0 + 200 + 300 - 400 + 100 = 200')
overflow_tests = [k + 1 for k, t in enumerate(W['tests']) if abs(t['expect']) > INT_MAX or
                  any(abs(sum(t['args'][1][1:m])) > INT_MAX for m in range(len(t['args'][1]) + 1))]
check(len(overflow_tests) >= 2, 'tests whose running total passes the int limit: %s' % overflow_tests)

# ---- route A: native builds -------------------------------------------------
def lit(v):
    return 'std::vector<int>{' + ', '.join(str(x) for x in v) + '}'

def run_variant(code, cxx):
    tmp = tempfile.mkdtemp()
    body = '#include <cstdio>\n#include <cstdlib>\n' + code + '\nint main(int argc, char** argv) {\n int which = std::atoi(argv[1]);\n'
    for k, t in enumerate(W['tests']):
        a, b = t['args']
        body += ' if (which == %d) { long long r = signed_volume(%s, %s); std::printf("%%lld\\n", r); }\n' % (k, lit(a), lit(b))
    body += ' return 0;\n}\n'
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx, '-std=c++20', '-O1', '-fno-exceptions', '-D_GLIBCXX_ASSERTIONS', '-w', src, '-o', exe],
                        capture_output=True, text=True)
    res = [False] * len(W['tests'])
    if cp.returncode == 0:
        for k, t in enumerate(W['tests']):
            pr = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=20)
            res[k] = pr.returncode == 0 and pr.stdout.strip() == str(t['expect'])
    elif os.environ.get('SHOWERR'):
        print(cp.stderr[:2000])
    shutil.rmtree(tmp)
    return res

sol = W['solution']
BUGS = {
    'int total (overflow)': ('long long total = 0;', 'int total = 0;'),
    'a flat trade resets the sign to 0': ('            sign = -1;\n        }', '            sign = -1;\n        } else {\n            sign = 0;\n        }'),
    'loop from i = 0 reads prices[i - 1] (unsigned wrap)': ('std::size_t i = 1;', 'std::size_t i = 0;'),
    'bound size() - 1 wraps on an empty feed': ('i < prices.size();', 'i <= prices.size() - 1;'),
    'off by one: sizes[i - 1]': ('sizes[i])', 'sizes[i - 1])'),
    'compares with the first price': ('if (prices[i] > prices[i - 1])', 'if (prices[i] > prices[0])'),
    'flat counted as a buy (>=)': ('if (prices[i] > prices[i - 1]) {\n            sign = 1;\n        } else if (prices[i] < prices[i - 1]) {\n            sign = -1;\n        }',
                                   'if (prices[i] >= prices[i - 1]) {\n            sign = 1;\n        } else {\n            sign = -1;\n        }'),
}
FIRST_AS_BUY = ('#include <vector>\n\nlong long signed_volume(const std::vector<int>& prices, const std::vector<int>& sizes) {\n'
                '    long long total = 0;\n    int prev = 0;\n    int sign = 0;\n'
                '    for (std::size_t i = 0; i < prices.size(); ++i) {\n'
                '        if (prices[i] > prev) sign = 1;\n        else if (prices[i] < prev) sign = -1;\n'
                '        total += sign * static_cast<long long>(sizes[i]);\n        prev = prices[i];\n    }\n    return total;\n}\n')

cxxs = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(len(cxxs) == 2, 'g++ and clang++ both present')
for cxx in cxxs:
    r = run_variant(sol, cxx)
    check(all(r), '%s: solution passes all %d tests' % (cxx, len(r)))
    r = run_variant(W['starter'], cxx)
    check(not all(r), '%s: starter fails tests %s' % (cxx, [k + 1 for k, ok in enumerate(r) if not ok]))
    for name, (old, new) in BUGS.items():
        check(old in sol, 'anchor present: ' + name)
        r = run_variant(sol.replace(old, new), cxx)
        check(not all(r), '%s: bug "%s" caught by tests %s' % (cxx, name, [k + 1 for k, ok in enumerate(r) if not ok]))
    r = run_variant(FIRST_AS_BUY, cxx)
    check(not all(r), '%s: bug "first trade signed against prev = 0" caught by tests %s' % (cxx, [k + 1 for k, ok in enumerate(r) if not ok]))

print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
