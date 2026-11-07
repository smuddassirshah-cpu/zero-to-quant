"""Recompute every figure of opt-dash homework-2 item h-asian-cv (performance task, L2).

Route 1: the item's own solution run through every hidden test, as the code widget does.
Route 2: an independent pricer on the same draws: paths by a running product, one fixing
at a time; the control's mean from the closed-form geometric sum; the weight b as the
least-squares slope of y on x (np.polyfit). The reference price in test 7 is checked by a
4,000,000-path control-variate run and a 4,000,000-path plain run on other seeds.
The starter fails every test; each planted wrong solution fails, first at its named test.
Needs numpy: run with the scratchpad venv, for example
    <venv>/bin/python -I docs/reports/opt-dash-2-perf-numbers.py
"""
import json, math, os, sys, warnings
import numpy as np

warnings.simplefilter('ignore', RuntimeWarning)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'opt-dash', 'homework-2.json')
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
    exp = eval(t['expect'], env)
    if t.get('compare') == 'isclose':
        tol = t.get('tol')
        rel, ab = (1e-9, 1e-12) if not tol else (tol.get('rel', 0.0), tol.get('abs', 0.0))
        return close(norm(act), norm(exp), rel, ab), act
    return norm(act) == norm(exp), act


def run_all(w, code):
    ns = {}
    try:
        exec(w['prelude'], ns)
        exec(code, ns)
    except Exception as e:
        return [(False, 'load ' + repr(e))] * len(w['tests'])
    with np.errstate(all='ignore'):
        return [run_case(ns, t) for t in w['tests']]


# ---- the item ----
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-asian-cv']
check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
print('item index (1-based):', idx[0] + 1, 'of', len(items))
check(item.get('performance') == 'code', 'performance kind is code')
check(sum('performance' in it for it in items) == 1, 'one performance item in homework-2')
check(len(items) <= 12, 'homework at or under 12 items (%d)' % len(items))
check(len(w['tests']) == 10 and len(w['examples']) == 2, 'tests 10, examples 2')
check(w['examples'] == w['tests'][:2], 'examples are tests 1 and 2')
check('10 hidden tests' in w['how'] and '1e-5' in w['how'], '"how" states 10 tests and 1e-5')

res = run_all(w, w['solution'])
check(all(ok for ok, _ in res), 'solution passes %d of %d' % (sum(ok for ok, _ in res), len(res)))
res = run_all(w, w['starter'])
check(not any(ok for ok, _ in res), 'starter fails %d of %d' % (sum(not ok for ok, _ in res), len(res)))


# ---- route 2 ----
def asian2(S, K, r, sigma, T, n_fix, n_paths, seed, q=0.0, control=True):
    z = np.random.default_rng(seed).standard_normal((n_paths, n_fix))
    dt = T / n_fix
    level = np.full(n_paths, float(S))
    total = np.zeros(n_paths)
    for k in range(n_fix):                       # one fixing at a time
        level = level * np.exp((r - q - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * z[:, k])
        total += level
    A = total / n_fix
    D = math.exp(-r * T)
    y = D * np.maximum(A - K, 0.0)
    if not control:
        return float(y.mean()), float(y.std(ddof=1) / math.sqrt(n_paths))
    g = math.exp((r - q) * dt)                   # E[S_{t_k}] = S g^k, k = 1..n
    mean_avg = S * g * (g ** n_fix - 1) / (g - 1) / n_fix if g != 1 else float(S)
    x = D * A
    b = np.polyfit(x, y, 1)[0]                   # least-squares slope of y on x
    adj = y - b * (x - D * mean_avg)
    return float(adj.mean()), float(adj.std(ddof=1) / math.sqrt(n_paths))


cases = {1: (100, 100, 0.05, 0.2, 1.0, 12, 20_000, 0),
         3: (50, 52, 0.03, 0.3, 0.5, 6, 20_000, 4, 0.02),
         4: (100, 95, 0.04, 0.25, 0.25, 13, 20_000, 5, 0.01),
         5: (100, 100, 0.05, 0.05, 1.0, 12, 20_000, 3),
         9: (100, 130, 0.05, 0.2, 1.0, 12, 20_000, 2)}
for k, a in cases.items():
    got = asian2(*a)
    filed = eval(w['tests'][k - 1]['expect'])
    check(close(list(got), filed, 1e-9, 0), 'test %d: route 2 %s equals the file %s' % (k, [round(v, 6) for v in got], filed))
    seen = eval(w['tests'][k - 1]['call'], {'list': list, 'asian_cv': lambda *a, q=0.0: list(a) + ([q] if q else [])})
    check(seen == list(a), 'test %d: call arguments %s match route 2' % (k, seen))

# test 6: one fixing is the European call
ns = {}
exec(w['prelude'], ns)
bs = ns['bs_price'](100, 100, 0.05, 0.2, 1.0)
d1 = (math.log(1) + (0.05 + 0.02) * 1) / 0.2
d2 = d1 - 0.2
Phi = lambda v: 0.5 * math.erfc(-v / math.sqrt(2))
bs2 = 100 * Phi(d1) - 100 * math.exp(-0.05) * Phi(d2)
check(abs(bs - bs2) < 1e-12 and round(bs, 4) == 10.4506, 'European call 10.4506 by two routes')
p, se = asian2(100, 100, 0.05, 0.2, 1.0, 1, 20_000, 1)
check(abs(p - bs) < 3 * se, 'test 6: one fixing within 3 se of Black-Scholes (%.4f vs %.4f, se %.4f)' % (p, bs, se))

# test 7: the reference 6.156
REF = 6.156
check('abs(p - 6.156) < 4 * se' in w['tests'][6]['call'], 'test 7 uses 6.156')
cv, cvv, pl, plv = [], [], [], []
for s in range(1000, 1040):
    a, b = asian2(100, 100, 0.05, 0.2, 1.0, 12, 100_000, s)
    cv.append(a); cvv.append(b * b)
    a, b = asian2(100, 100, 0.05, 0.2, 1.0, 12, 100_000, s + 5000, control=False)
    pl.append(a); plv.append(b * b)
cvm, cvs = float(np.mean(cv)), math.sqrt(sum(cvv)) / len(cvv)
plm, pls = float(np.mean(pl)), math.sqrt(sum(plv)) / len(plv)
print('reference: control %.5f (se %.5f), plain %.5f (se %.5f)' % (cvm, cvs, plm, pls))
check(abs(cvm - REF) < 3 * cvs and abs(plm - REF) < 3 * pls, 'both 4M-path runs agree with 6.156 within 3 se')
p, se = asian2(100, 100, 0.05, 0.2, 1.0, 12, 20_000, 9)
check(abs(p - REF) < 4 * se, 'test 7: seed 9 within 4 se of the reference (%.2f se)' % (abs(p - REF) / se))

# test 8 and the explain figures
p1, se1 = asian2(*cases[1])
pp, sep = asian2(*cases[1], control=False)
check(abs(sep - eval('plain_asian_se(100, 100, 0.05, 0.2, 1.0, 12, 20_000, 0)', dict(ns))) < 1e-12, 'plain se by two routes')
check(se1 < sep / 2, 'test 8: control se %.4f under half the plain se %.4f' % (se1, sep))
ex_avg = math.exp(-0.05) * 100 * sum(math.exp(0.05 * i / 12) for i in range(1, 13)) / 12
g = math.exp(0.05 / 12)
ex_avg2 = math.exp(-0.05) * 100 * g * (g ** 12 - 1) / (g - 1) / 12
check(abs(ex_avg - ex_avg2) < 1e-10 and round(ex_avg, 2) == 97.74, 'E[X] = %.4f, 97.74 by two routes' % ex_avg)
check(round(sep, 4) == 0.0604 and round(se1, 4) == 0.0245, 'se plain 0.0604 and control 0.0245')
ratio = (sep / se1) ** 2
check(round(ratio) == 6, 'path ratio (%.3f) is about six' % ratio)
txt = item['explain']['text']
check(all(s in txt for s in ('97.74', '0.0604', '0.0245', '20,000', 'six')), 'explain carries 97.74, 0.0604, 0.0245, 20,000, six')

# planted wrong solutions
SOL = w['solution']


def mut(*pairs):
    s = SOL
    for o, n in zip(pairs[::2], pairs[1::2]):
        assert o in s, o
        s = s.replace(o, n)
    return s


bugs = {
    'payoff not discounted': (mut('y = D * np.maximum(A - K, 0.0)', 'y = np.maximum(A - K, 0.0)'), 1),
    'control mean of S_T, S e^(-qT)': (mut('ex = D * S * np.exp((r - q) * t).mean()', 'ex = S * exp(-q * T)'), 1),
    'control mean not discounted': (mut('ex = D * S * np.exp((r - q) * t).mean()', 'ex = S * np.exp((r - q) * t).mean()'), 1),
    'average includes today': (mut('A = S * np.exp(logs).mean(axis=1)', 'A = (S + S * np.exp(logs).sum(axis=1)) / (n_fix + 1)',
                                   't = dt * np.arange(1, n_fix + 1)', 't = dt * np.arange(0, n_fix + 1)'), 1),
    'fixings drawn independently': (mut('logs = np.cumsum((r - q - sigma ** 2 / 2) * dt + sigma * sqrt(dt) * z, axis=1)',
                                        'tt = dt * np.arange(1, n_fix + 1)\n    logs = (r - q - sigma ** 2 / 2) * tt + sigma * np.sqrt(tt) * z'), 1),
    'error from raw payoffs': (mut('adj.std(ddof=1)', 'y.std(ddof=1)'), 1),
    'weight fixed at 1': (mut('b = np.cov(y, x)[0, 1] / np.var(x, ddof=1)', 'b = 1.0'), 1),
    'European control S_T': (mut('x = D * A ', 'x = D * S * np.exp(logs[:, -1]) ', 'ex = D * S * np.exp((r - q) * t).mean()', 'ex = S * exp(-q * T)'), 1),
    'yield left out of the paths': (mut('(r - q - sigma ** 2 / 2) * dt', '(r - sigma ** 2 / 2) * dt'), 3),
    'yield left out of the control mean': (mut('np.exp((r - q) * t)', 'np.exp(r * t)'), 3),
    'no ValueError': (mut('    if n_paths < 2:\n        raise ValueError("a standard error needs two paths")\n', ''), 2),
}
for name, (code, first) in bugs.items():
    res = run_all(w, code)
    failed = [i + 1 for i, (ok, _) in enumerate(res) if not ok]
    check(bool(failed) and failed[0] == first, 'bug "%s" fails tests %s (first %d)' % (name, failed, first))
# a harmless variant passes: population variance in b only moves b by n/(n-1)
res = run_all(w, mut('np.var(x, ddof=1)', 'np.var(x)'))
check(all(ok for ok, _ in res), 'ddof mismatch in b alone still passes (tolerance relative 1e-5)')
for k in item['feedback']['byKey']:
    check(k in ('test-2', 'test-3'), 'byKey %s is a first-failure test of a planted bug' % k)

print('failures:', fails)
sys.exit(1 if fails else 0)
