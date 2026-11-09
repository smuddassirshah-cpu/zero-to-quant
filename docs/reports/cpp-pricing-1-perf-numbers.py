"""cpp-pricing level 1 performance task h-perf-corridor: every number twice, and
the solution, the starter and planted wrong solutions run against every test.

Route A: scipy.stats.norm (cdf and sf, picking the tail as the solution does).
Route B: mpmath at 60 digits, the plain difference of two CDFs (no cancellation
at that precision). The JSON expect must equal route B as a double and agree
with route A within a relative 1e-12.
Native: each hidden test is compiled with the code (g++ and clang++, both at
-std=c++20 -O1 -fno-exceptions), its value printed with %.17g and graded by the
engine's rule (cpp-grade.js `close`: relative 1e-9, absolute 1e-12 unless the
case's tol says otherwise; `equal` exact). The solution must pass all tests on
every compiler, the starter must fail, and every planted bug must fail at least
one test. Run with the venv Python (scipy, mpmath). Exit 0 only if all hold.
"""
import json, math, os, re, shutil, subprocess, sys, tempfile
import mpmath
from scipy.stats import norm

mpmath.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'cpp-pricing', 'homework-1.json')
DOC = json.load(open(HW))
item = next(i for i in DOC['items'] if i['id'] == 'h-perf-corridor')
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
check('12 hidden tests' in W['how'] and len(T) == 12, 'how says 12 hidden tests')
check(not item.get('hints') and 'parts' not in item, 'no hints, no parts')
check(len(DOC['items']) <= 12, 'homework within 12 items')

# ---- two routes for every expected value -------------------------------------
def parse(call):
    m = re.fullmatch(r'(\w+)\((.*)\)', call)
    args = [math.inf if a.strip() == 'INFINITY' else float(a) for a in m.group(2).split(',')]
    return m.group(1), args

def z_float(s, x, r, sig, t):
    if x == 0: return -math.inf
    if x == math.inf: return math.inf
    return (math.log(x / s) - (r - 0.5 * sig * sig) * t) / (sig * math.sqrt(t))

def route_a(fn, a):
    if fn == 'norm_cdf':
        return float(norm.cdf(a[0]))
    s, lo, hi, r, sig, t = a
    if not lo < hi: return 0.0
    za, zb = z_float(s, lo, r, sig, t), z_float(s, hi, r, sig, t)
    p = norm.sf(za) - norm.sf(zb) if za > 0 else norm.cdf(zb) - norm.cdf(za)
    return float(math.exp(-r * t) * p)

def route_b(fn, a):
    if fn == 'norm_cdf':
        return mpmath.ncdf(mpmath.mpf(a[0]))
    s, lo, hi, r, sig, t = a
    if not lo < hi: return mpmath.mpf(0)
    S, R, SG, TT = map(mpmath.mpf, (s, r, sig, t))
    def zz(x):
        if x == 0: return -mpmath.inf
        if x == math.inf: return mpmath.inf
        return (mpmath.log(mpmath.mpf(x) / S) - (R - SG ** 2 / 2) * TT) / (SG * mpmath.sqrt(TT))
    return mpmath.exp(-R * TT) * (mpmath.ncdf(zz(hi)) - mpmath.ncdf(zz(lo)))

for k, c in enumerate(T, 1):
    fn, a = parse(c['call'])
    va, vb = route_a(fn, a), float(route_b(fn, a))
    check(c['expect'] == vb, 'test %d expect is the 60-digit value (%r vs %r)' % (k, c['expect'], vb))
    check(va == vb or abs(va - vb) <= 1e-12 * abs(vb), 'test %d route A %r vs route B %r' % (k, va, vb))
    if vb != 0 and abs(vb) < 1e-6:
        check(c.get('tol') == {'rel': 1e-9}, 'test %d tiny value graded on relative error alone' % k)
    if vb == 0:
        check(c['compare'] == 'equal', 'test %d zero compared exactly' % k)

# ---- numbers stated in the prose, feedback and explain -------------------------
s, lo, hi, r, sig, t = parse(T[4]['call'])[1]
check(lo == 0 and hi == math.inf and abs(T[4]['expect'] - math.exp(-r * t)) < 1e-15, 'test 5: 0 to infinity is e^{-rT}')
s, lo, hi, r, sig, t = parse(T[6]['call'])[1]
za, zb = z_float(s, lo, r, sig, t), z_float(s, hi, r, sig, t)
check(za > 0 and float(1 - mpmath.ncdf(za)) < 1e-10 and float(1 - mpmath.ncdf(zb)) < 1e-10, 'test 7: both CDFs within 1e-10 of 1 (a = %.3f)' % za)
s, lo, hi, r, sig, t = parse(T[7]['call'])[1]
check(z_float(s, hi, r, sig, t) < 0, 'test 8: corridor below the median')
v30 = mpmath.ncdf(-30)
check(abs(float(v30) / 4.9e-198 - 1) < 0.01, 'Phi(-30) is about 4.9e-198 (%s)' % mpmath.nstr(v30, 5))
check(0.5 * (1 + math.erf(-30 / math.sqrt(2))) == 0.0, 'erf form rounds Phi(-30) to 0')
check('£1' in item['prose'] and '9 significant figures' in item['prose'], 'prose figures present')
check(1e-9 * 10 < 1e-7, '9 significant figures matches relative 1e-9')

# ---- native runs: solution, starter, planted bugs ------------------------------
SOL = W['solution']
BUGS = {
    'no discount': SOL.replace('return std::exp(-r * t) * p;', 'return p;'),
    'erf form of norm_cdf': SOL.replace('return 0.5 * std::erfc(-x / std::sqrt(2.0));', 'return 0.5 * (1 + std::erf(x / std::sqrt(2.0)));'),
    'plain CDF difference everywhere': SOL.replace('a > 0 ? norm_cdf(-a) - norm_cdf(-b) : norm_cdf(b) - norm_cdf(a)', 'norm_cdf(b) - norm_cdf(a)'),
    'upper tails everywhere': SOL.replace('a > 0 ? norm_cdf(-a) - norm_cdf(-b) : norm_cdf(b) - norm_cdf(a)', 'norm_cdf(-a) - norm_cdf(-b)'),
    'sigma * t for the spread (variance scaled by T)': SOL.replace('double vol = sigma * std::sqrt(t);', 'double vol = sigma * t;'),
    'd1 drift, r + sigma^2/2': SOL.replace('(r - 0.5 * sigma * sigma) * t', '(r + 0.5 * sigma * sigma) * t'),
    'integer division 1 / 2 in the drift': SOL.replace('(r - 0.5 * sigma * sigma) * t', '(r - 1 / 2 * sigma * sigma) * t'),
    'sqrt(2) missing in norm_cdf': SOL.replace('std::erfc(-x / std::sqrt(2.0))', 'std::erfc(-x)'),
    'no empty-corridor guard': SOL.replace('    if (!(lo < hi)) return 0.0;\n', ''),
    'tails swapped (d2 of each bound used for P(S_T <= x))': SOL.replace('(std::log(lo / s) - drift) / vol', '(std::log(s / lo) + drift) / vol').replace('(std::log(hi / s) - drift) / vol', '(std::log(s / hi) + drift) / vol'),
    'd1 point and no discount': SOL.replace('(r - 0.5 * sigma * sigma) * t', '(r + 0.5 * sigma * sigma) * t').replace('return std::exp(-r * t) * p;', 'return p;'),
}
for name, code in BUGS.items():
    check(code != SOL, 'planted bug applied: ' + name)

def close(a, e, tol):
    if a == e: return True
    if not (math.isfinite(a) and math.isfinite(e)): return False
    if tol: rel, ab = tol.get('rel', 0), tol.get('abs', 0)
    else: rel, ab = 1e-9, 1e-12
    return abs(a - e) <= max(rel * max(abs(a), abs(e)), ab)

def run(code, cxx):
    tmp = tempfile.mkdtemp()
    body = '#include <cstdio>\n#include <cstdlib>\n' + code + '\nint main(int argc, char** argv) {\n int which = std::atoi(argv[1]);\n'
    for k, c in enumerate(T):
        body += ' if (which == %d) { double zq = (%s); std::printf("%%.17g\\n", zq); }\n' % (k, c['call'])
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
        try:
            v = float(p.stdout.strip())
        except ValueError:
            out.append(False); continue
        out.append(close(v, c['expect'], c.get('tol')) if c['compare'] == 'isclose' else v == c['expect'])
    shutil.rmtree(tmp)
    return out

cxxs = [c for c in ('g++', 'clang++') if shutil.which(c)]
check(len(cxxs) >= 1, 'a native compiler')
for cxx in cxxs:
    res = run(SOL, cxx)
    check(res is not None and all(res), '%s: solution passes all 12 (%s)' % (cxx, res))
    res = run(W['starter'], cxx)
    check(res is not None and not all(res), '%s: starter fails' % cxx)
    print('%s starter fails tests %s' % (cxx, [k + 1 for k, ok in enumerate(res or []) if not ok]))
    for name, code in BUGS.items():
        res = run(code, cxx)
        caught = [k + 1 for k, ok in enumerate(res or []) if not ok]
        check(res is not None and caught, '%s: bug "%s" caught' % (cxx, name))
        print('%s bug %-48s caught by tests %s' % (cxx, '"' + name + '"', caught))

print('checks: %d, FAILURES: %d' % (nchecks, len(fails)))
sys.exit(1 if fails else 0)
