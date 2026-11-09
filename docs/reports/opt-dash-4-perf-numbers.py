"""Recompute every figure of opt-dash homework-4 item h4-weekend-explain (performance task, L4).

Route 1: the item's own solution run through every example and hidden test, as the code widget does.
Route 2: an independent explain. Prices with scipy.special.ndtr; delta, gamma, vega and theta by
central differences of that price (vega per 1.00, theta per year of 365 days), unit conversions
written separately; actual by revaluing the whole book at once. Every expect must match route 2.
The starter fails every test; each planted wrong solution fails, first at the test its byKey names.
The explain's figures (residual -2.52, vanna about -2.32) are checked by analytic and bumped vanna.
Run: <venv>/bin/python -I docs/reports/opt-dash-4-perf-numbers.py (needs scipy).
"""
import json, math, os, sys
from math import exp, log, sqrt
from scipy.special import ndtr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'opt-dash', 'homework-4.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h4-weekend-explain')
w = item['widget']
fails = 0
KEYS = ('delta', 'gamma', 'vega', 'theta', 'explained', 'actual', 'residual')


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


# ---- a copy of the code widget's grading: prelude, code, setup, call, isclose with tol ----
def close(a, b, rel, ab):
    if hasattr(a, 'tolist'):
        a = a.tolist()
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b)
                and all(close(x, y, rel, ab) for x, y in zip(a, b)))
    try:
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    except Exception:
        return False


def namespace(src):
    ns = {}
    exec(w['prelude'], ns)
    exec(src, ns)
    return ns


def run_case(src, t):
    env = namespace(src)
    try:
        if t.get('setup'):
            exec(t['setup'], env)
        act = eval(t['call'], env)
    except Exception as e:
        return False, 'error ' + type(e).__name__
    tol = t.get('tol', {})
    return close(act, eval(t['expect'], {}), tol.get('rel', 1e-9), tol.get('abs', 1e-12)), act


def results(src):
    return [run_case(src, t)[0] for t in w['tests']]


# ---- shape ----
tests, examples = w['tests'], w['examples']
check(item['performance'] == 'code', 'performance kind is code')
check(len(tests) == 12 and len(examples) == 1 and len(tests) > len(examples), '12 tests, 1 example')
check('12 hidden tests' in w['how'], 'how says 12 hidden tests')
check(all(t['compare'] == 'isclose' and t['tol'] == {'abs': 1e-06} for t in tests + examples),
      'every case isclose within abs 1e-6 (the how says within £0.000001)')

# ---- route 1: the solution passes everything, the starter fails every test ----
for i, t in enumerate(examples + tests):
    ok, act = run_case(w['solution'], t)
    check(ok, f'solution passes {"example" if i == 0 else "test " + str(i)}')
st = results(w['starter'])
check(not any(st), 'starter fails every test')

# ---- route 2: independent explain by scipy prices and bumped Greeks ----
def price2(S, K, r, sig, T, kind, q):
    sd = sig * sqrt(T)
    d1 = (log(S / K) + (r - q) * T) / sd + sd / 2
    d2 = d1 - sd
    c = S * exp(-q * T) * ndtr(d1) - K * exp(-r * T) * ndtr(d2)
    return c if kind == 'call' else c - S * exp(-q * T) + K * exp(-r * T)   # parity


def greeks2(S, K, r, sig, T, kind, q):
    f = lambda s=S, v=sig, t=T: price2(s, K, r, v, t, kind, q)
    h, e, k = 1e-4 * S, 1e-5, 1e-6
    return {'delta': (f(S + h) - f(S - h)) / (2 * h),
            'gamma': (f(S + h) - 2 * f() + f(S - h)) / h ** 2,
            'vega': (f(v=sig + e) - f(v=sig - e)) / (2 * e),          # per 1.00 of vol
            'theta': -(f(t=T + k) - f(t=T - k)) / (2 * k)}           # per year: dV/dt = -dV/dT


def explain2(book, S0, S1, r, days, q=0.0):
    dS, yrs = S1 - S0, days / 365.0
    out = dict.fromkeys(('delta', 'gamma', 'vega', 'theta'), 0.0)
    for p in book:
        g = greeks2(S0, p['K'], r, p['vol0'] / 100, p['T'], p['kind'], q)
        out['delta'] += p['qty'] * g['delta'] * dS
        out['gamma'] += p['qty'] * g['gamma'] * dS * dS / 2
        out['vega'] += p['qty'] * g['vega'] * (p['vol1'] - p['vol0']) * 0.01
        out['theta'] += p['qty'] * g['theta'] * yrs
    value = lambda S, which, t: sum(p['qty'] * price2(S, p['K'], r, p[which] / 100, p['T'] - t, p['kind'], q)
                                    for p in book)
    out['actual'] = value(S1, 'vol1', yrs) - value(S0, 'vol0', 0.0)
    out['explained'] = out['delta'] + out['gamma'] + out['vega'] + out['theta']
    out['residual'] = out['actual'] - out['explained']
    return out


ns2 = {}
exec(w['prelude'], ns2)          # only for weekend_book; route 2 uses none of its functions
ns2['explain_day'] = explain2
for i, t in enumerate(examples + tests):
    env = dict(ns2)
    if t.get('setup'):
        exec(t['setup'], env)
    act = eval(t['call'], env)
    exp_ = eval(t['expect'], {})
    check(close(act, exp_, 0, 2e-5), f'route 2 agrees with the expect of {"example" if i == 0 else "test " + str(i)} (within 2e-5, bump error)')

# ---- planted wrong solutions: each fails, first at the test its byKey names ----
SOL = w['solution']


def sub(a, b, src=SOL):
    assert a in src, a
    return src.replace(a, b)


BUGS = {
    'gamma without the half': (sub('n * 0.5 * g["gamma"]', 'n * g["gamma"]'), 2),
    'vega times vol points': (sub('(vol1 - vol0)    # vega', '(p["vol1"] - p["vol0"])    # vega'), 3),
    'theta times days (years taken as days)': (sub('g["theta"] * dt', 'g["theta"] * days'), 4),
    'one day whatever days says': (sub('dS, dt = S1 - S0, days / 365', 'dS, dt = S1 - S0, 1 / 365'), 4),
    'trading days, days / 252': (sub('dS, dt = S1 - S0, days / 365', 'dS, dt = S1 - S0, days / 252'), 4),
    'residual explained less actual': (sub('out["actual"] - out["explained"]', 'out["explained"] - out["actual"]'), 5),
    'revaluation with T not shortened': (sub('vol1, T - dt, kind', 'vol1, T, kind'), 5),
    'revaluation at the old vol': (sub('bs_price(S1, K, r, vol1', 'bs_price(S1, K, r, vol0'), 5),
    'qty ignored': (SOL.replace('n * ', ''), 1),
    'Greeks from the end of the period': (sub('bs_greeks(S0, K, r, vol0, T, kind, q)',
                                              'bs_greeks(S1, K, r, vol1, T - dt, kind, q)'), 1),
    'q left out': (SOL.replace(', kind, q)', ', kind)'), 8),
}
BUGS['summed Greeks with the mean vol move'] = ('''
def explain_day(book, S0, S1, r, days, q=0.0):
    dS, dt = S1 - S0, days / 365
    tot = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0}
    actual, moves = 0.0, []
    for p in book:
        g = bs_greeks(S0, p["K"], r, p["vol0"] / 100, p["T"], p["kind"], q)
        for k in tot:
            tot[k] += p["qty"] * g[k]
        moves.append((p["vol1"] - p["vol0"]) / 100)
        actual += p["qty"] * (bs_price(S1, p["K"], r, p["vol1"] / 100, p["T"] - dt, p["kind"], q)
                              - bs_price(S0, p["K"], r, p["vol0"] / 100, p["T"], p["kind"], q))
    dsig = sum(moves) / len(moves) if moves else 0.0
    out = {"delta": tot["delta"] * dS, "gamma": 0.5 * tot["gamma"] * dS ** 2,
           "vega": tot["vega"] * dsig, "theta": tot["theta"] * dt, "actual": actual}
    out["explained"] = out["delta"] + out["gamma"] + out["vega"] + out["theta"]
    out["residual"] = actual - out["explained"]
    return out
''', 6)
byKey = item['feedback']['byKey']
for name, (src, first) in BUGS.items():
    res = results(src)
    bad = [i + 1 for i, ok in enumerate(res) if not ok]
    check(bool(bad) and bad[0] == first and f'test-{first}' in byKey,
          f'bug "{name}" fails tests {bad}, first {first}, which has a byKey line')
check(set(byKey) == {f'test-{n}' for n in (1, 2, 3, 4, 5, 6, 8)}, 'byKey covers exactly the first failures')

# ---- the figures in the prose, feedback and explain ----
t = w['tests']
check("100.0, 94.0" in t[1]['call'] and '£6 fall' in byKey['test-2'], 'test 2 is a £6 fall')
check("'vol0': 22.0, 'vol1': 24.5" in t[2]['call'] and '2.5 vol points' in byKey['test-3'], 'test 3 is a 2.5-point rise')
check(t[3]['call'].rstrip(")]'theta[").endswith('3') and 'three calendar days' in byKey['test-4'], 'test 4 runs 3 days')
book = ns2['weekend_book']
S0, S1, r, q, days = 100.0, 96.5, 0.04, 0.01, 3
d1r = namespace(SOL)['explain_day'](book, S0, S1, r, days, q)
d2r = explain2(book, S0, S1, r, days, q)
check(round(d1r['residual'], 2) == -2.52 and round(d2r['residual'], 2) == -2.52, f'weekend residual -2.52 ({d1r["residual"]:.5f}, {d2r["residual"]:.5f})')
check('−£2.52' in item['explain']['text'] and '−£2.32' in item['explain']['text'], 'explain quotes -2.52 and -2.32')
van_a = van_b = 0.0
for p in book:
    K, T, kind, s0 = p['K'], p['T'], p['kind'], p['vol0'] / 100
    ds = (p['vol1'] - p['vol0']) / 100
    sd = s0 * sqrt(T)
    d1 = (log(S0 / K) + (r - q + s0 * s0 / 2) * T) / sd
    vanna = -exp(-q * T) * exp(-d1 * d1 / 2) / sqrt(2 * math.pi) * (d1 - sd) / s0   # same for calls and puts
    f = lambda S, v: price2(S, K, r, v, T, kind, q)
    h, e = 0.01, 1e-4
    vanna_fd = (f(S0 + h, s0 + e) - f(S0 + h, s0 - e) - f(S0 - h, s0 + e) + f(S0 - h, s0 - e)) / (4 * h * e)
    van_a += p['qty'] * vanna * (S1 - S0) * ds
    van_b += p['qty'] * vanna_fd * (S1 - S0) * ds
check(round(van_a, 2) == -2.32 and abs(van_a - van_b) < 1e-3, f'book vanna term about -2.32 ({van_a:.5f} analytic, {van_b:.5f} bumped)')
check(abs(van_a) / abs(d1r['residual']) > 0.5, 'vanna is most of the residual')
check(all(p['T'] > days / 365 for p in book), 'every weekend_book option outlives the period')

print('failures:', fails)
sys.exit(1 if fails else 0)
