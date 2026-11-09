"""cpp-pricing level 2 performance task h-perf-yield-tree: every number twice, and
the solution, the starter and planted wrong solutions run against every test.

Route A: a Python backward recursion on the CRR tree with a yield (floats).
Route B: the same price as a binomial sum, exp(-rT) * sum_j pmf(j) * payoff(leaf j),
with scipy's binomial pmf, and the closed forms where they exist: the forward
S e^{-qT} - K e^{-rT} (exact on any tree that prices the forward) and the
Black-Scholes price with a continuous yield (Merton) for the 2,000-step case.
The JSON expect must equal route A (or the closed form), and route B must agree
within a relative 1e-12.
Native: each hidden test is compiled after the hidden prelude with the code
(g++ and clang++, -std=c++20 -O1 -fno-exceptions), printed with %.17g and graded
by the engine's rule (cpp-grade.js `close`: relative 1e-9, absolute 1e-12
unless the case's tol says otherwise). The solution must pass every test on
every compiler, the starter must fail, and each planted bug must fail at least
one test. Run with the venv Python (scipy). Exit 0 only if all hold.
"""
import json, math, os, re, shutil, subprocess, sys, tempfile
from scipy.stats import binom, norm

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'cpp-pricing', 'homework-2.json')
DOC = json.load(open(HW))
item = next(i for i in DOC['items'] if i['id'] == 'h-perf-yield-tree')
W = item['widget']
T = W['tests']
fails = []
nchecks = 0

def check(cond, msg):
    global nchecks
    nchecks += 1
    if not cond:
        fails.append(msg)
        print('FAIL', msg)

# ---- shape -----------------------------------------------------------------
check(item.get('performance') == 'code', 'performance kind code')
check(W.get('language') == 'cpp', 'language cpp')
check(3 <= len(T) <= 15, '3 to 15 tests')
check(len(T) > len(W['examples']), 'more tests than examples')
for e in W['examples']:
    check(e in T, 'example is also a test')
check('10 hidden tests' in W['how'] and len(T) == 10, 'how says 10 hidden tests')
check(not item.get('hints') and 'parts' not in item, 'no hints, no parts')
check(len(DOC['items']) <= 12, 'homework within 12 items')
check('HiddenForward' not in item['prose'] and 'HiddenForward' not in W['starter'], 'the hidden payoff is not named to the learner')

# ---- payoffs and the two routes ----------------------------------------------
PAY = {
    'Call': lambda k: (lambda x: max(x - k, 0.0)),
    'Put': lambda k: (lambda x: max(k - x, 0.0)),
    'Strangle': lambda a, b: (lambda x: max(a - x, 0.0) + max(x - b, 0.0)),
    'HiddenForward': lambda k: (lambda x: x - k),
}

def route_a(pay, s, r, q, sig, t, n):
    if t == 0: return pay(s)
    dt = t / n; u = math.exp(sig * math.sqrt(dt)); d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d); disc = math.exp(-r * dt)
    v = [pay(s * u ** j * d ** (n - j)) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            v[j] = disc * (p * v[j + 1] + (1 - p) * v[j])
    return v[0]

def route_b(pay, s, r, q, sig, t, n):
    if t == 0: return pay(s)
    dt = t / n; up = sig * math.sqrt(dt)
    p = (math.exp((r - q) * dt) - math.exp(-up)) / (math.exp(up) - math.exp(-up))
    check(0 < p < 1, 'up probability in (0, 1): %r' % p)
    w = binom.pmf(range(n + 1), n, p)
    return math.exp(-r * t) * math.fsum(w[j] * pay(s * math.exp(up * (2 * j - n))) for j in range(n + 1))

def merton_call(s, k, r, q, sig, t):
    d1 = (math.log(s / k) + (r - q + sig * sig / 2) * t) / (sig * math.sqrt(t)); d2 = d1 - sig * math.sqrt(t)
    return float(s * math.exp(-q * t) * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2))

def merton_call_parity(s, k, r, q, sig, t):
    # second route: the put by its own formula, then parity c = p + S e^{-qT} - K e^{-rT}
    d1 = (math.log(s / k) + (r - q + sig * sig / 2) * t) / (sig * math.sqrt(t)); d2 = d1 - sig * math.sqrt(t)
    put = k * math.exp(-r * t) * norm.sf(d2) - s * math.exp(-q * t) * norm.sf(d1)
    return float(put + s * math.exp(-q * t) - k * math.exp(-r * t))

def parse(call):
    m = re.fullmatch(r'yield_tree_price\((\w+)\(([^)]*)\), (.*)\)', call)
    if not m: return None
    pay = PAY[m.group(1)](*[float(x) for x in m.group(2).split(',')])
    a = [float(x) for x in m.group(3).split(',')]
    return m.group(1), [float(x) for x in m.group(2).split(',')], pay, a[:5] + [int(a[5])]

for k, c in enumerate(T, 1):
    pr = parse(c['call'])
    if pr is None:
        check(c['expect'] == [5.0, 0.0, 6.5], 'test %d strangle payoffs 5, 0, 6.5' % k)
        st = PAY['Strangle'](70.0, 90.0)
        check([st(65.0), st(80.0), st(96.5)] == [70 - 65, 0.0, 96.5 - 90], 'strangle payoffs by hand')
        continue
    name, kargs, pay, (s, r, q, sig, t, n) = pr
    va, vb = route_a(pay, s, r, q, sig, t, n), route_b(pay, s, r, q, sig, t, n)
    check(va == vb or abs(va - vb) <= 1e-12 * abs(va), 'test %d route A %r vs route B %r' % (k, va, vb))
    if name == 'HiddenForward':
        closed = s * math.exp(-q * t) - kargs[0] * math.exp(-r * t)
        check(c['expect'] == closed, 'test %d expect is the forward closed form' % k)
        check(abs(va - closed) <= 1e-12 * abs(closed), 'test %d tree prices the forward exactly (%r vs %r)' % (k, va, closed))
    elif c.get('tol') == {'abs': 0.005}:
        m1, m2 = merton_call(s, kargs[0], r, q, sig, t), merton_call_parity(s, kargs[0], r, q, sig, t)
        check(abs(m1 - m2) < 1e-12, 'Merton call by two routes %r %r' % (m1, m2))
        check(c['expect'] == m1, 'test %d expect is the Merton call' % k)
        check(abs(va - m1) < 0.005, 'test %d 2,000-step tree within £0.005 of Merton (%.6f)' % (k, va - m1))
        check(n == 2000 and name == 'Call', 'test %d is the 2,000-step call' % k)
    else:
        check(c['expect'] == va, 'test %d expect is route A' % k)
    if t == 0:
        check(c['expect'] == max(kargs[0] - s, 0.0) == 5.0, 'test %d T = 0 gives the payoff 5' % k)

# numbers in the prose, feedback and explain
check('$Se^{-qT} - Ke^{-rT}$' in item['prose'], 'prose states the forward value')
check('£0.005' in W['how'] and '2,000-step' in W['how'], 'how states the 2,000-step tolerance')
check('at £65 it pays £5' in item['feedback']['byKey']['test-2'], 'strangle feedback figure')
check('struck at £75' in item['feedback']['byKey']['test-5'] and 'HiddenForward(75.0)' in T[4]['call'], 'test-5 is the forward at 75')
check(T[5]['call'].endswith(', 1)') and T[2]['call'].endswith(', 4)'), 'test-6 one step, test-3 four steps')
check(', 0.0, 10)' in T[6]['call'], 'test-7 has T = 0')

# ---- native runs: solution, starter, planted bugs ------------------------------
SOL = W['solution']
def rep(code, *pairs):
    for a, b in pairs:
        assert a in code, a
        code = code.replace(a, b)
    return code
BUGS = {
    'no discount': rep(SOL, ('v[j] = disc * (p * v[j + 1] + (1 - p) * v[j]);', 'v[j] = p * v[j + 1] + (1 - p) * v[j];')),
    'discount at r - q': rep(SOL, ('double disc = std::exp(-r * dt);', 'double disc = std::exp(-(r - q) * dt);')),
    'yield ignored in the up probability': rep(SOL, ('std::exp((r - q) * dt)', 'std::exp(r * dt)')),
    'yield added, growth at r + q': rep(SOL, ('std::exp((r - q) * dt)', 'std::exp((r + q) * dt)')),
    'strangle legs swapped (call at the lower strike)': rep(SOL, ('std::max(put_strike_ - spot, 0.0) + std::max(spot - call_strike_, 0.0)', 'std::max(spot - put_strike_, 0.0) + std::max(call_strike_ - spot, 0.0)')),
    'one step back too few': rep(SOL, ('for (int i = n - 1; i >= 0; --i)', 'for (int i = n - 1; i > 0; --i)')),
    'leaves one step short': rep(SOL, ('std::pow(d, n - j)', 'std::pow(d, n - 1 - j)')),
    'u = exp(sigma dt), variance scaled by dt squared': rep(SOL, ('std::exp(sigma * std::sqrt(dt))', 'std::exp(sigma * dt)')),
    'no T = 0 case': rep(SOL, ('    if (t == 0.0) return payoff(s);\n', '')),
    'integer steps, dt = 1 / n * t': rep(SOL, ('double dt = t / n;', 'double dt = 1 / n * t;')),
}

def close(a, e, tol):
    if a == e: return True
    if not (math.isfinite(a) and math.isfinite(e)): return False
    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
    return abs(a - e) <= max(rel * max(abs(a), abs(e)), ab)

def same(a, e, tol):
    if isinstance(e, list):
        return isinstance(a, list) and len(a) == len(e) and all(close(x, y, tol) for x, y in zip(a, e))
    return isinstance(a, float) and close(a, e, tol)

HARNESS = r'''
#include <cstdio>
#include <cstdlib>
#include <vector>
static void zq_print(double v) { std::printf("%.17g\n", v); }
static void zq_print(const std::vector<double>& v) { std::printf("["); for (std::size_t i = 0; i < v.size(); ++i) std::printf(i ? ",%.17g" : "%.17g", v[i]); std::printf("]\n"); }
'''

def run(code, cxx):
    tmp = tempfile.mkdtemp()
    body = HARNESS + W['prelude'] + code + '\nint main(int argc, char** argv) {\n int which = std::atoi(argv[1]);\n'
    for k, c in enumerate(T):
        body += ' if (which == %d) { zq_print(%s); }\n' % (k, c['call'])
    body += ' return 0;\n}\n'
    src, exe = os.path.join(tmp, 'main.cpp'), os.path.join(tmp, 'a.out')
    open(src, 'w').write(body)
    cp = subprocess.run([cxx, '-std=c++20', '-O1', '-fno-exceptions', '-w', src, '-o', exe], capture_output=True, text=True)
    if cp.returncode != 0:
        print(cp.stderr[:2000])
        return None
    out = []
    for k, c in enumerate(T):
        p = subprocess.run([exe, str(k)], capture_output=True, text=True, timeout=10)
        txt = p.stdout.strip()
        try:
            v = [float(x) for x in txt[1:-1].split(',')] if txt.startswith('[') else float(txt)
        except ValueError:
            out.append(False); continue
        out.append(p.returncode == 0 and same(v, c['expect'], c.get('tol')))
    shutil.rmtree(tmp)
    return out

cxxs = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(len(cxxs) >= 1, 'a native compiler')
for cxx in cxxs:
    res = run(SOL, cxx)
    check(res is not None and all(res), '%s: solution passes all 10 (%s)' % (cxx, res))
    res = run(W['starter'], cxx)
    check(res is not None and not all(res), '%s: starter fails' % cxx)
    print('%s starter fails tests %s' % (cxx, [k + 1 for k, ok in enumerate(res or []) if not ok]))
    for name, code in BUGS.items():
        res = run(code, cxx)
        caught = [k + 1 for k, ok in enumerate(res or []) if not ok]
        check(res is not None and caught, '%s: bug "%s" caught' % (cxx, name))
        print('%s bug %-50s caught by tests %s' % (cxx, '"' + name + '"', caught))

print('checks: %d, FAILURES: %d' % (nchecks, len(fails)))
sys.exit(1 if fails else 0)
