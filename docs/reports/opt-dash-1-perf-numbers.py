"""Recompute every figure of opt-dash homework-1 item h-parity-fit (performance task, L1).

Route 1: the item's own solution run through every hidden test, as the code widget does.
Route 2: independent of the solution: the true F, r, q of each toy chain from its inputs,
and, for the two noisy expiries, a pure-Python least-squares line from closed-form sums
over strikes paired with dicts. The starter fails every test; each planted wrong solution
fails, and fails first at the test its byKey line names where it has one.
Needs pandas and numpy: run with the scratchpad venv, for example
    <venv>/bin/python -I docs/reports/opt-dash-1-perf-numbers.py
"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'opt-dash', 'homework-1.json')
doc = json.load(open(HW))
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


# ---- a copy of the code widget's grading: setup, call, expect, compare, tol ----
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
    return [run_case(ns, t) for t in w['tests']]


# ---- the item ----
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-parity-fit']
check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
print('item index (1-based):', idx[0] + 1, 'of', len(items))
check(item.get('performance') == 'code', 'performance kind is code')
check(sum('performance' in it for it in items) == 1, 'one performance item in homework-1')
check(len(items) <= 12, 'homework at or under 12 items (%d)' % len(items))
check(len(w['tests']) == 11 and len(w['examples']) == 2, 'tests 11, examples 2')
check(w['examples'] == w['tests'][:2], 'examples are tests 1 and 2')
check('11 hidden tests' in w['how'] and '1e-9' in w['how'], '"how" states 11 tests and 1e-9')

# Route 1: the solution passes every test; the starter fails every test.
res = run_all(w, w['solution'])
check(all(ok for ok, _ in res), 'solution passes %d of %d' % (sum(ok for ok, _ in res), len(res)))
res = run_all(w, w['starter'])
check(not any(ok for ok, _ in res), 'starter fails %d of %d' % (sum(not ok for ok, _ in res), len(res)))

# Route 2: independent values for every expectation.
ns = {}
exec(w['prelude'], ns)
exp = math.exp


def fit2(df, S, T):
    """Pure Python: pair mids by strike with dicts, closed-form least squares."""
    calls, puts = {}, {}
    for K, kind, b, a in zip(df['strike'], df['type'], df['bid'], df['ask']):
        if b > 0:
            (calls if kind == 'call' else puts)[float(K)] = (b + a) / 2
    ks = sorted(set(calls) & set(puts))
    if len(ks) < 3:
        return [float('nan')] * 3
    x = ks
    y = [calls[k] - puts[k] for k in ks]
    n = len(x)
    xb, yb = sum(x) / n, sum(y) / n
    slope = sum((a - xb) * (b - yb) for a, b in zip(x, y)) / sum((a - xb) ** 2 for a in x)
    icept = yb - slope * xb
    D = -slope
    if D <= 0 or icept <= 0:
        return [float('nan')] * 3
    F = icept / D
    r = -math.log(D) / T
    return [F, r, r - math.log(F / S) / T]


toy = ns['toy_chain']
T1 = toy(100, 0.04, 0.01, 0.25, 1.0, range(80, 121, 5))
truths = {
    1: (T1, 100, 1.0, [100 * exp((0.04 - 0.01) * 1.0), 0.04, 0.01]),
    3: (toy(50, 0.03, 0.02, 0.3, 2.0, [40, 45, 50, 55, 60]), 50, 2.0, [50 * exp((0.03 - 0.02) * 2.0), 0.03, 0.02]),
    4: (toy(100, 0.05, -0.01, 0.2, 0.5, [90, 95, 100, 105, 110]), 100, 0.5, [100 * exp((0.05 + 0.01) * 0.5), 0.05, -0.01]),
    5: (ns['zero_bid'](T1, 120, 'call'), 100, 1.0, [100 * exp(0.03), 0.04, 0.01]),
    6: (ns['without'](ns['without'](T1, 85, 'put'), 115, 'call'), 100, 1.0, [100 * exp(0.03), 0.04, 0.01]),
    7: (toy(100, 0.04, 0.01, 0.25, 1.0, [95, 100, 105]), 100, 1.0, [100 * exp(0.03), 0.04, 0.01]),
}
for k, (df, S, T, truth) in truths.items():
    got = fit2(df, S, T)
    check(close(got, truth, 0, 1e-9), 'test %d: route 2 %s equals the truth %s' % (k, [round(v, 6) for v in got], [round(v, 6) for v in truth]))
    check(close(norm(eval(w['tests'][k - 1]['expect'], dict(ns))), truth, 0, 1e-12), 'test %d: file expectation equals the truth' % k)

day = ns['day']
for k, T in ((8, 1.0), (9, 0.5)):
    got = fit2(day[day['T'] == T], 96.0, T)
    filed = eval(w['tests'][k - 1]['expect'])
    check(close(got, filed, 0, 1e-9), 'test %d: route 2 %s matches the file within 1e-9' % (k, [round(v, 6) for v in got]))
check(all(v != v for v in fit2(toy(100, 0.04, 0.01, 0.25, 1.0, [95, 105]), 100, 1.0)), 'test 2: two pairs give NaNs (route 2)')
rising = ns['quotes']([[1.0, 90, 'call', 4.9, 5.1, 10, 0.0], [1.0, 90, 'put', 4.9, 5.1, 10, 0.0],
                       [1.0, 100, 'call', 9.9, 10.1, 10, 0.0], [1.0, 100, 'put', 4.9, 5.1, 10, 0.0],
                       [1.0, 110, 'call', 14.9, 15.1, 10, 0.0], [1.0, 110, 'put', 4.9, 5.1, 10, 0.0]])
check(all(v != v for v in fit2(rising, 100, 1.0)), 'test 10: C - P = 0, 5, 10 gives slope +0.5 and NaNs (route 2)')

# Pairs on the noisy expiries, and the explain figures.
for T, n in ((1.0, 12), (0.5, 11)):
    s = day[day['T'] == T]
    c = set(s[(s['type'] == 'call') & (s['bid'] > 0)]['strike'])
    p = set(s[(s['type'] == 'put') & (s['bid'] > 0)]['strike'])
    check(len(c & p) == n, 'T = %s: %d strikes pair up' % (T, len(c & p)))
r1 = fit2(day[day['T'] == 1.0], 96.0, 1.0)[1]
check(round(100 * r1, 2) == 4.73, 'explain: fitted one-year r = %.4f%% rounds to 4.73%%' % (100 * r1))
check('make_chain(seed=58, S=96.0, r=0.045, q=0.015)' in w['prelude'], 'explain: the true r of the day chain is 4.5%')
check('4.73' in item['explain']['text'] and '4.5%' in item['explain']['text'], 'explain carries 4.73% and 4.5%')

# Planted wrong solutions: each fails, first at the named test.
SOL = w['solution']


def mut(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)


bugs = {
    'put-call sign (P - C)': (mut('(w["call"] - w["put"])', '(w["put"] - w["call"])'), 1),
    'discounting omitted (F = intercept)': (mut('F = icept / D', 'F = icept'), 1),
    'rate not divided by T': (mut('r = -log(D) / T', 'r = -log(D)'), 3),
    'zero-bid quote kept': (mut('.where(df_T["bid"] > 0)', ''), 5),
    'pairs by position': (mut('''    w = df_T.assign(mid=m).pivot(index="strike", columns="type", values="mid")
    w = w.reindex(columns=["call", "put"]).dropna()''', '''    c = df_T.assign(mid=m)[df_T["type"] == "call"].sort_values("strike")
    p = df_T.assign(mid=m)[df_T["type"] == "put"].sort_values("strike")
    n = min(len(c), len(p))
    w = pd.DataFrame({"call": c["mid"].to_numpy()[:n], "put": p["mid"].to_numpy()[:n]},
                     index=c["strike"].to_numpy()[:n]).dropna()'''), 6),
    'needs four pairs': (mut('len(w) < 3', 'len(w) < 4'), 7),
    'no positive-D guard': (mut('    if D <= 0 or icept <= 0:\n        return nan\n', ''), 10),
    'no pair minimum': (mut('    if len(w) < 3:\n        return nan\n', ''), 2),
    'yield sign flipped': (mut('q = r - log(F / S) / T', 'q = log(F / S) / T - r'), 1),
    'rate as 1 - D': (mut('r = -log(D) / T', 'r = (1 - D) / T'), 1),
}
for name, (code, first) in bugs.items():
    res = run_all(w, code)
    failed = [i + 1 for i, (ok, _) in enumerate(res) if not ok]
    check(bool(failed) and failed[0] == first, 'bug "%s" fails tests %s (first %d)' % (name, failed, first))
for k in item['feedback']['byKey']:
    check(k in ('test-3', 'test-5', 'test-6', 'test-7', 'test-10'), 'byKey %s is a first-failure test of a planted bug' % k)

print('failures:', fails)
sys.exit(1 if fails else 0)
