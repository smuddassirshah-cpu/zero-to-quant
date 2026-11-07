"""Recompute every figure of opt-dash homework-3 item h-black-iv (performance task, L3).

Route 1: the item's own solution run through every hidden test, as the code widget does.
Route 2: SciPy. Prices from Black-Scholes with S = F and q = r (so the forward is F) and
r = -ln(D)/T, using scipy.special.ndtr; vols by scipy.optimize.brentq on [1e-9, 50]; the
NaN cases by the no-arbitrage bounds written out by hand. The starter fails every test;
each planted wrong solution fails, first at the test its byKey line names where it has one.
Run: <venv>/bin/python -I docs/reports/opt-dash-3-perf-numbers.py (needs scipy).
"""
import json, math, os, sys
from math import exp, log, sqrt, nan
from scipy.optimize import brentq
from scipy.special import ndtr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'opt-dash', 'homework-3.json')
doc = json.load(open(HW))
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


# ---- a copy of the code widget's grading: setup, call, expect, compare, tol, raises ----
def norm(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    return [norm(x) for x in v] if isinstance(v, list) else v


def close(a, b, rel, ab):
    if isinstance(a, list) or isinstance(b, list):
        return (isinstance(a, list) and isinstance(b, list) and len(a) == len(b)
                and all(close(x, y, rel, ab) for x, y in zip(a, b)))
    try:
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    except Exception:
        return False


def run_case(ns, t):
    env = dict(ns)
    try:
        if t.get('setup'):
            exec(t['setup'], env)
        if t.get('compare') == 'raises':
            try:
                eval(t['call'], env)
            except Exception as e:
                return any(c.__name__ == t['expect'] for c in type(e).__mro__), repr(e)
            return False, 'no error'
        act = eval(t['call'], env)
    except Exception as e:
        return False, 'error ' + type(e).__name__
    exp_ = eval(t['expect'], env)
    if t.get('compare') == 'isclose':
        tol = t.get('tol')
        rel, ab = (1e-9, 1e-12) if not tol else (tol.get('rel', 0.0), tol.get('abs', 0.0))
        return close(norm(act), norm(exp_), rel, ab), act
    return norm(act) == norm(exp_), act


def run_all(w, code):
    ns = {}
    try:
        exec(w['prelude'], ns)
        exec(code, ns)
    except Exception as e:
        return [(False, 'load ' + repr(e))] * len(w['tests'])
    return [run_case(ns, t) for t in w['tests']]


# ---- the item ----
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-black-iv']
check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
tests = w['tests']
print('item index (1-based):', idx[0] + 1, 'of', len(items))
check(item.get('performance') == 'code', 'performance kind is code')
check(sum('performance' in it for it in items) == 1, 'one performance item in homework-3')
check(len(items) <= 12, 'homework at or under 12 items (%d)' % len(items))
check(len(tests) == 13 and len(w['examples']) == 2, 'tests 13, examples 2')
check(w['examples'] == tests[:2], 'examples are tests 1 and 2')
check('13 hidden tests' in w['how'] and '1e-8' in w['how'], '"how" states 13 tests and 1e-8')

res = run_all(w, w['solution'])
check(all(ok for ok, _ in res), 'solution passes %d of %d' % (sum(ok for ok, _ in res), len(res)))
res = run_all(w, w['starter'])
check(not any(ok for ok, _ in res), 'starter fails %d of %d' % (sum(not ok for ok, _ in res), len(res)))


# ---- route 2 ----
def price2(F, K, D, sigma, T, kind):
    r = -log(D) / T
    S, q = F, r                                    # forward S e^((r - q) T) = F
    d1 = (log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if kind == 'call':
        return S * exp(-q * T) * ndtr(d1) - K * exp(-r * T) * ndtr(d2)
    return K * exp(-r * T) * ndtr(-d2) - S * exp(-q * T) * ndtr(-d1)


def bounds2(F, K, D, kind):
    if kind == 'call':
        return max(D * F - D * K, 0.0), D * F
    return max(D * K - D * F, 0.0), D * K


def iv2(price, F, K, D, T, kind='call'):
    lo, hi = bounds2(F, K, D, kind)
    if not (price == price) or price <= lo or price >= hi:
        return nan
    return brentq(lambda s: price2(F, K, D, s, T, kind) - price, 1e-9, 50, xtol=1e-14, rtol=1e-14, maxiter=500)


def args_of(call):
    """The arguments of a black_iv(...) call, by evaluating it with a recorder."""
    rec = []
    env = {'exp': exp, 'nan': nan, 'str': str, 'isinstance': isinstance, 'float': float,
           'black_iv': lambda *a: rec.append(a) or 0.0}
    eval(call, env)
    return rec


# tests with a vol stated in the file: the price in the call is that vol's price
for k, vol in ((1, 0.2), (3, 0.3), (5, 0.25), (6, 2.5)):
    (a,) = args_of(tests[k - 1]['call'])[:1]
    price, F, K, D, T = a[:5]
    kind = a[5] if len(a) > 5 else 'call'
    p2 = price2(F, K, D, vol, T, kind)
    check(abs(p2 - price) < 1e-12, 'test %d: price %.10f is the %s at vol %s (route 2 %.10f)' % (k, price, kind, vol, p2))
    check(abs(iv2(*a) - vol) < 1e-10 and float(eval(tests[k - 1]['expect'])) == vol, 'test %d: route 2 vol equals %s' % (k, vol))
# tests with a vol from the solver
for k in (4, 7, 11):
    (a,) = args_of(tests[k - 1]['call'])
    v2 = iv2(*a)
    check(abs(v2 - float(eval(tests[k - 1]['expect']))) < 1e-10, 'test %d: route 2 vol %.10f matches the file' % (k, v2))
# test 10, the slice
rec = args_of(tests[9]['call'])
v2 = [iv2(*a) for a in rec]
v2 = [v if v == v else -1.0 for v in v2]
check(len(rec) == 6 and close(v2, eval(tests[9]['expect']), 0, 1e-10), 'test 10: route 2 slice %s matches' % [round(v, 4) for v in v2])
check(v2[-1] == -1.0 and rec[-1][0] == 0.0, 'test 10: the 130 call at 0.00 has no vol (price at the lower bound 0)')
# NaN tests 2, 8, 9 by the bounds
for k in (2, 8, 9):
    for a in args_of(tests[k - 1]['call']):
        lo, hi = bounds2(*a[1:4], a[5] if len(a) > 5 else 'call')
        p = a[0]
        check(not (lo < p < hi), 'test %d: price %r is outside (%.4f, %.4f) or NaN' % (k, p, lo, hi))
# test 11: inside the discounted bound, outside the undiscounted one
(a,) = args_of(tests[10]['call'])
check(exp(-0.02) * 10 < a[0] < 10, 'test 11: 9.9 lies between D(F - K) = %.4f and F - K = 10' % (exp(-0.02) * 10))
# prose: test 6 is within the stated 300%; pennies: tests 4 and 7 quote 9p and 24p
check(2.5 <= 3.0 and args_of(tests[3]['call'])[0][0] == 0.09 and args_of(tests[6]['call'])[0][0] == 0.24, 'prose: vols up to 300% and penny quotes (9p, 24p)')

# explain: one plain Newton step from 0.2 on the 9p put, and vega there
ns = {}
exec(w['prelude'], ns)
exec(w['solution'], ns)
a = args_of(tests[3]['call'])[0]
price, F, K, D, T, kind = a
diff = ns['black_price'](F, K, D, 0.2, T, kind) - price
s1 = 0.2 - diff / ns['black_vega'](F, K, D, 0.2, T)
eps = 1e-6
num_vega = (price2(F, K, D, 0.2 + eps, T, kind) - price2(F, K, D, 0.2 - eps, T, kind)) / (2 * eps)
s1b = 0.2 - (price2(F, K, D, 0.2, T, kind) - price) / num_vega
check(round(s1) == 146935 and abs(s1b - s1) / s1 < 1e-4, 'explain: first plain step %.2f (route 2 %.2f), about 146,935' % (s1, s1b))
check(ns['black_vega'](F, K, D, s1, T) == 0.0, 'explain: vega at that vol is 0.0 in floating point')
check('146,935' in item['explain']['text'] and '9p' in item['explain']['text'], 'explain carries 146,935 and 9p')

# planted wrong solutions
SOL = w['solution']


def mut(*pairs):
    s = SOL
    for o, n in zip(pairs[::2], pairs[1::2]):
        assert o in s, o
        s = s.replace(o, n)
    return s


PLAIN = '''    sigma = 0.2
    for _ in range(100):
        diff = black_price(F, K, D, sigma, T, kind) - price
        if abs(diff) < 1e-13:
            return sigma
        sigma = sigma - diff / black_vega(F, K, D, sigma, T)
    return sigma
'''
CHECK = '    if not lower < price < upper:          # also False for a NaN price\n        return nan\n'
bugs = {
    'plain Newton from 0.2, no bracket': (SOL[:SOL.index('    lo, hi = 1e-6, 1.0')] + PLAIN, 4),
    'discounting omitted in the price': (mut('return D * (F * norm_cdf(d1) - K * norm_cdf(d2))', 'return F * norm_cdf(d1) - K * norm_cdf(d2)',
                                             'return D * (K * norm_cdf(-d2) - F * norm_cdf(-d1))', 'return K * norm_cdf(-d2) - F * norm_cdf(-d1)'), 1),
    'put by parity with the wrong sign': (mut('return D * (K * norm_cdf(-d2) - F * norm_cdf(-d1))', 'return D * (F * norm_cdf(d1) - K * norm_cdf(d2)) + D * (F - K)'), 3),
    'call formula for puts': (mut('    if kind == "call":\n        return D * (F', '    if True:\n        return D * (F'), 3),
    'call bounds for puts': (mut('lower, upper = D * max(K - F, 0.0), D * K', 'lower, upper = D * max(F - K, 0.0), D * F'), 3),
    'no bounds check': (mut(CHECK, ''), 2),
    'raises instead of NaN': (mut(CHECK, '    if not lower < price < upper:\n        raise ValueError("no vol fits")\n'), 2),
    'search capped at 2': (mut('''    while black_price(F, K, D, hi, T, kind) < price:   # widen until hi is above
        lo, hi = hi, 2 * hi
        if hi > 1000:
            return nan
''', '    hi = 2.0\n'), 6),
    'bounds not discounted': (mut('lower, upper = D * max(F - K, 0.0), D * F', 'lower, upper = max(F - K, 0.0), F',
                                  'lower, upper = D * max(K - F, 0.0), D * K', 'lower, upper = max(K - F, 0.0), K'), 11),
    'NaN price slips past the check': (mut('    if not lower < price < upper:          # also False for a NaN price', '    if price <= lower or price >= upper:'), 9),
    'bounds not strict': (mut('    if not lower < price < upper:', '    if not lower <= price <= upper:'), 8),
}
for name, (code, first) in bugs.items():
    res = run_all(w, code)
    failed = [i + 1 for i, (ok, _) in enumerate(res) if not ok]
    check(bool(failed) and failed[0] == first, 'bug "%s" fails tests %s (first %d)' % (name, failed, first))
for k in item['feedback']['byKey']:
    check(k in ('test-2', 'test-3', 'test-4', 'test-6', 'test-8', 'test-9', 'test-11'), 'byKey %s is a first-failure test of a planted bug' % k)

print('failures:', fails)
sys.exit(1 if fails else 0)
