"""Recompute every number stated in app/content/exams/stage-2.json by a second route and assert it at its path.

Route A is build.py (closed forms and reference code). Route B here is independent where it can be: grid searches and
bisection, exact Fractions, companion-matrix roots, scipy's optimisers (SLSQP for the KKT weights, HiGHS for the LP and its
duals, root finding on the score equations for both GLMs, brentq for the implied volatilities), scipy.stats for the ranks,
the gamma posterior and the normal tail, numerical second derivatives of Black-Scholes, Simpson tail integrals, brute-force
counts, and second implementations of every code task run on the data files. Every code solution passes its hidden tests,
every starter fails one, a leaky walk-forward and a one-control Monte Carlo fail theirs, and second implementations of the
statistical code tasks pass. A last pass reads every number in every learner-visible string of each item: whole numbers 0 to
10 count as structure, every other number must match a route-B or given value for that item to its printed precision.
Topic 2.6 (the researcher track) has no items here: it sits in topic-2.6. Exits 1 on any failure. Run: python3 docs/briefs/exam-stage-2-scripts/check_numbers.py
"""
import glob
import json
import math
import os
import re
import sys
from fractions import Fraction as F
from statistics import NormalDist, stdev

import numpy as np
import pandas as pd
from scipy import optimize, stats
from statsmodels.tsa.adfvalues import mackinnoncrit
from statsmodels.tsa.stattools import adfuller

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'stage-2.json')
CDIR = os.path.join(ROOT, 'app', 'content')
DATA = os.path.join(CDIR, 'data', 'stage-2')
N01 = NormalDist()


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
ITEM, PAPER = {}, {}
for pi, p in enumerate(doc['parts']):
    for it in p.get('items', []):
        ITEM[it['id']] = it
        PAPER[it['id']] = p['id']
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def W(iid, part=None):
    it = ITEM[iid]
    return it['widget'] if part is None else it['parts'][part]['widget']


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, '' if ok else note)


def key(iid, value, part=None):
    w = W(iid, part)
    t = max(w['tol']['abs'] / 10, 1e-9) if w['tol']['abs'] else 1e-9
    rec(abs(w['answer'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = W(iid, part)
    hit = [x for x in w['wrong'] if x['id'] == wid]
    t = max(hit[0]['tol']['abs'] / 10, 1e-9) if hit and hit[0]['tol']['abs'] else 1e-9
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= t, f'{iid} wrong "{wid}" = {value!r}', f'found {hit}')
    allow(iid, value)


def correct_ids(iid, want):
    w = W(iid)
    got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    rec(got == sorted(want), f'{iid} correct options {got} = {sorted(want)}')
    rec(w.get('shuffle') is True, f'{iid} shuffle true')
    rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} every distractor has a why')
    keyt = [re.sub(r'\$', '', o['text']) for o in w['options'] if o.get('correct')]
    oth = [re.sub(r'\$', '', o['text']) for o in w['options'] if not o.get('correct')]
    if w['kind'] == 'choice':
        rec(not (len(keyt[0]) >= 12 and all(len(keyt[0]) > 1.5 * len(o) for o in oth)), f'{iid} key not far longer than its distractors')


def simpson(f, a, b, m=4000):
    h = (b - a) / m
    return h / 3 * (f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, m)))


def bs_call(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return S * N01.cdf(d1) - K * math.exp(-r * T) * N01.cdf(d1 - s * math.sqrt(T))


# ---------------------------------------------------------------- running code
def _close(a, b, tol):
    if isinstance(a, (list, tuple)):
        return isinstance(b, (list, tuple)) and len(a) == len(b) and all(_close(x, y, tol) for x, y in zip(a, b))
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return False
    rel = tol.get('rel', 0 if 'abs' in tol else 1e-9)
    ab = tol.get('abs', 0 if 'rel' in tol else 1e-12)
    return math.isclose(a, b, rel_tol=rel, abs_tol=ab)


def _plain(v):
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, (np.floating, np.integer, np.bool_)):
        return v.item()
    if isinstance(v, tuple):
        return [_plain(x) for x in v]
    return v


def run_py(src, tests, want_fail=False):
    """Number of tests passed, run in the data folder so files open by bare name."""
    here, passed = os.getcwd(), 0
    os.chdir(DATA)
    try:
        for t in tests:
            ns = {'__learner_source__': src}
            try:
                exec(src, ns)
                if t.get('setup'):
                    exec(t['setup'], ns)
                cmp_ = t.get('compare', 'equal')
                if cmp_ == 'raises':
                    try:
                        eval(t['call'], ns)
                        ok = False
                    except Exception as e:  # noqa: BLE001
                        ok = type(e).__name__ == t['expect']
                else:
                    got = _plain(eval(t['call'], ns))
                    want = eval(t['expect'], {})
                    ok = got == want if cmp_ == 'equal' else _close(got, want, t.get('tol', {}))
            except Exception:  # noqa: BLE001
                ok = False
            passed += bool(ok)
    finally:
        os.chdir(here)
    return passed


def code_py(iid, part=None):
    w = W(iid, part)
    lab = f'{iid}{"" if part is None else f" part {part}"}'
    n = len(w['tests'])
    rec(run_py(w['solution'], w['tests']) == n, f'{lab}: the solution passes all {n} tests')
    rec(run_py(w['starter'], w['tests']) < n, f'{lab}: the starter fails a test')
    rec(all(e['expect'] in [t['expect'] for t in w['tests']] for e in w['examples']), f'{lab}: each example is a hidden test')
    rec(run_py(w['solution'], w['examples']) == len(w['examples']), f'{lab}: the solution passes its examples as Run examples compares them')
    for e in w['examples']:
        isfloat = not (e['expect'] in ('True', 'False') or e['expect'].lstrip('-').isdigit() or e['expect'].isidentifier())
        rec(not isfloat or (e.get('compare') == 'isclose' and e.get('tol')), f'{lab}: the float example {e["call"][:40]} has compare isclose and a tolerance')
        tt = [t for t in w['tests'] if t['call'] == e['call'] and t['expect'] == e['expect']]
        rec(tt and all(e.get('compare', 'equal') == t.get('compare', 'equal') and e.get('tol') == t.get('tol') for t in tt), f'{lab}: the example keeps its hidden test\'s compare and tolerance')
    if w.get('data'):
        rec('import pandas' in w['starter'], f'{lab}: the starter imports pandas, so Pyodide loads it for the data tests')
    rec(f'{n} hidden tests' in w['how'], f'{lab}: how states {n} tests')
    for name in w.get('data', {}):
        rec(os.path.exists(os.path.join(DATA, name)) and os.path.getsize(os.path.join(DATA, name)) < 262144, f'{lab}: data file {name} exists, under 256 KB')
    return w['tests']


def expect_of(tests, call):
    hit = [t for t in tests if t['call'] == call]
    return eval(hit[0]['expect'])


def other_passes(iid, src, part=None, label='a second implementation'):
    w = W(iid, part)
    n = len(w['tests'])
    rec(run_py(src, w['tests']) == n, f'{iid}{"" if part is None else f" part {part}"}: {label} passes all {n} tests')


def other_fails(iid, src, part=None, label='a flawed version'):
    w = W(iid, part)
    rec(run_py(src, w['tests']) < len(w['tests']), f'{iid}{"" if part is None else f" part {part}"}: {label} fails a test')


def csv(name):
    return pd.read_csv(os.path.join(DATA, name))


# ======================================================================== Paper A
grid = np.linspace(0, 1, 2_000_001)
mse = grid ** 2 * 0.02 ** 2 / 250 + (1 - grid) ** 2 * 0.0004 ** 2
c1 = float(grid[np.argmin(mse)])
key('a-shrink-mean', round(c1, 6))
wrong('a-shrink-mean', 'ratio', float(F(16, 100) / F(16, 10)))
wrong('a-shrink-mean', 'flipped', round(1 - c1, 6))
allow('a-shrink-mean', 250, 0.0004, 0.02, 1.6, 1.76, 11)

c2 = optimize.brentq(lambda p: 160 * p - 40, 0, 1)
key('a-review-threshold', c2)
wrong('a-review-threshold', 'sum-denominator', float(F(40, 200)))
wrong('a-review-threshold', 'inverted', 1 - c2)
wrong('a-review-threshold', 'half', 0.5)
allow('a-review-threshold', 40, 160)

rows = range(1, 1501)
blocks = [list(range(601 + 120 * k, 721 + 120 * k)) for k in range(7)]
b3 = blocks[2]
train = [t for t in rows if t < b3[0] and t + 10 < b3[0]]
key('a-purged-fold', len(train))
wrong('a-purged-fold', 'no-purge', len([t for t in rows if t < b3[0]]))
wrong('a-purged-fold', 'second-block', len([t for t in rows if t < blocks[1][0] and t + 10 < blocks[1][0]]))
wrong('a-purged-fold', 'rolling', len([t for t in range(b3[0] - 600, b3[0]) if t + 10 < b3[0]]))
allow('a-purged-fold', 600, 1500, 601, 720, 120, b3[0], b3[-1], b3[0] - 10, 1)

correct_ids('a-leak-steps', ['a', 'b', 'c'])
allow('a-leak-steps', 120, 2015, 2024, 20)
correct_ids('a-curves-meet', ['a'])
allow('a-curves-meet', 1.02, 1.05, 0.80)

y6 = np.array([-14, -9, -2, 5, 7, 18], float)
lad = lambda v_: min(float(np.abs(v_ - c_).sum()) for c_ in np.linspace(-20, 20, 4001))      # the best centre, by search: the median
par6 = lad(y6)
dropa = [par6 - lad(y6[:k]) - lad(y6[k:]) for k in range(1, 6)]
sqd = max(len(y6) * y6.var() - k * y6[:k].var() - (6 - k) * y6[k:].var() for k in range(1, 6))
key('a-tree-split', round(max(dropa), 4))
wrong('a-tree-split', 'squared', round(sqd, 4))
wrong('a-tree-split', 'parent', round(par6, 4))
wrong('a-tree-split', 'biggest-gap', round(dropa[4], 4))
rec(int(np.argmax(dropa)) == 2, 'a-tree-split: the best split is after the third week')
allow('a-tree-split', 14, 9, 2, 18, 7, 5, np.median(y6), lad(y6[:3]), lad(y6[3:]), -9)

pmiss = F(24, 25) ** 25
key('a-block-bootstrap', round(float(25 * (1 - pmiss)), 4))
wrong('a-block-bootstrap', 'limit', round(25 * (1 - math.exp(-1)), 4))
wrong('a-block-bootstrap', 'out-of-bag', round(float(25 * pmiss), 4))
allow('a-block-bootstrap', 25, float(pmiss), 0.96, 24)


def leaf_loss(g, F0, ys):
    return sum(-(y * (F0 + g) - math.log(1 + math.exp(F0 + g))) for y in ys)


F0 = math.log(0.65 / 0.35)
ys8 = [1, 1, 1, 1, 0]
h = 1e-4
gr = (leaf_loss(h, F0, ys8) - leaf_loss(-h, F0, ys8)) / (2 * h)
he = (leaf_loss(h, F0, ys8) - 2 * leaf_loss(0, F0, ys8) + leaf_loss(-h, F0, ys8)) / h ** 2
newton = -gr / he
sig = lambda x: 1 / (1 + math.exp(-x))
key('a-boost-leaf', round(sig(F0 + 0.1 * newton), 6))
wrong('a-boost-leaf', 'no-shrink', round(sig(F0 + newton), 6))
wrong('a-boost-leaf', 'mean-residual', round(sig(F0 + 0.1 * (-gr / 5)), 6))
wrong('a-boost-leaf', 'base-rate', 0.65)
allow('a-boost-leaf', 13, 20, 0.1, F0, 0.75, 1.1375, newton, F0 + 0.1 * newton)

s9 = sum(F(x) for x in ('-0.55', '0.48', '-0.12', '0.41'))
key('a-shap-sum', round(sig(float(s9)), 6))
wrong('a-shap-sum', 'log-odds', float(s9))
wrong('a-shap-sum', 'base-only', round(sig(-0.55), 6))
allow('a-shap-sum', -0.55, 0.48, -0.12, 0.41)

xty = np.array([12.4, -18.6, 7.2, 15.0])
z10 = xty / 250
lo, hi = 0.0, 1.0                                         # bisection: the smallest lambda that soft-thresholds every z_j to 0
for _ in range(200):
    mid = (lo + hi) / 2
    if np.all(np.abs(z10) - mid <= 0):
        hi = mid
    else:
        lo = mid
key('a-lasso-entry', round(hi, 6))
wrong('a-lasso-entry', 'no-n', 18.6)
wrong('a-lasso-entry', 'signed-max', round(float(F('15.0') / 250), 6))
wrong('a-lasso-entry', 'two-n', round(float(F('18.6') / 500), 6))
allow('a-lasso-entry', 12.4, -18.6, 7.2, 15.0, 250, 18.6)


def gbinom(d, k):
    return math.gamma(d + 1) / (math.gamma(k + 1) * math.gamma(d - k + 1))


w2f = lambda d_: gbinom(d_, 2)                              # w_2 = (-1)^2 C(d, 2), the binomial-series weight
dlo = optimize.brentq(lambda d_: w2f(d_) + 0.1, 0.01, 0.5)
dhi = optimize.brentq(lambda d_: w2f(d_) + 0.1, 0.5, 0.99)
dhalf = optimize.brentq(lambda d_: 2 * w2f(d_) + 0.1, 0.01, 0.5)
key('a-frac-weight', round(dlo, 6))
wrong('a-frac-weight', 'other-root', round(dhi, 6))
wrong('a-frac-weight', 'dropped-half', round(dhalf, 6))
rec(abs(dlo + dhi - 1) < 1e-9, 'a-frac-weight: the two roots sum to 1')
allow('a-frac-weight', 0.1, 0.2, 0.5, dlo)

def uniq_b(spans):
    D_ = max(b_ for _, b_ in spans)
    M_ = np.zeros((len(spans), D_))
    for i_, (a_, b_) in enumerate(spans):
        M_[i_, a_ - 1:b_] = 1
    ct_ = M_.sum(axis=0)
    return ct_, [(M_[i_] / ct_)[M_[i_] > 0].mean() for i_ in range(len(spans))]


sp4 = [(1, 5), (4, 7), (6, 8), (7, 10)]
ct5, uq5 = uniq_b(sp4 + [(3, 9)])
ct4, uq4 = uniq_b(sp4)
key('a-label-uniqueness', round(sum(uq5), 4))
wrong('a-label-uniqueness', 'count', 5)
wrong('a-label-uniqueness', 'four-before', round(sum(uq4), 4))
wrong('a-label-uniqueness', 'old-plus-one', round(sum(uq4) + 1, 4))
rec(sum(uq5) < sum(uq4), 'a-label-uniqueness: the fifth label lowers the total, as the explanation says')
allow('a-label-uniqueness', *uq5)

zb = N01.inv_cdf(0.75)
pb = optimize.brentq(lambda p_: 2 * N01.cdf((p_ - 0.5) / math.sqrt(p_ * (1 - p_))) - 1 - 0.5, 0.5001, 0.9999)
key('a-bet-size', round(pb, 6))
wrong('a-bet-size', 'linear', 0.75)
m75 = 2 * N01.cdf(0.25 / math.sqrt(0.75 * 0.25)) - 1
rec(abs(m75 - 0.5) > 0.05, f'a-bet-size: p = 0.75, the answer of 2p - 1 = 0.5, gives size {m75:.3f} under the rule, not 0.5')
allow('a-bet-size', 0.5, 0.75, zb)

den = math.sqrt(1 + 0.8 * 0.12 + 4.5 / 4 * 0.0144)
z14 = 0.12 * math.sqrt(155) / den
key('a-psr', round(N01.cdf(z14), 6))
wrong('a-psr', 'normal', round(N01.cdf(0.12 * math.sqrt(155) / math.sqrt(1 + 0.0144 / 2)), 6))
wrong('a-psr', 'skew-sign', round(N01.cdf(0.12 * math.sqrt(155) / math.sqrt(1 - 0.096 + 0.0162)), 6))
allow('a-psr', 0.12, 156, -0.8, 5.5, 0.096, 0.0162, den, 0.12 * math.sqrt(155), z14, 155)

tab = {F('0.1'): [F('4.10'), F('3.70'), F('4.40')], F(1): [F('3.95'), F('3.62'), F('4.30')],
       F(10): [F('3.90'), F('3.66'), F('4.18')], F(100): [F('4.20'), F('3.95'), F('4.25')]}
held = {F('0.1'): 3.85, F(1): 3.80, F(10): 3.88, F(100): 3.79}
means = {k: sum(v) / 3 for k, v in tab.items()}
best = min(means, key=means.get)
key('a-lambda-honest', float(best), part=0)
wrong('a-lambda-honest', 'held-out-peek', float(min(held, key=held.get)), part=0)
wrong('a-lambda-honest', 'block-two', float(min(tab, key=lambda k: tab[k][1])), part=0)
key('a-lambda-honest', held[best], part=1)
wrong('a-lambda-honest', 'best-held-out', min(held.values()), part=1)
wrong('a-lambda-honest', 'validation-mean', round(float(means[best]), 4), part=1)
allow('a-lambda-honest', 0.1, 100, *[float(x) for v in tab.values() for x in v], *held.values(), *[float(v) for v in means.values()])

wf_t = code_py('a-walk-forward-ridge')
wf_b = ("import numpy as np\n\ndef ridge(Xa, ya, lam):\n    mu = Xa.mean(0); sd = np.sqrt(((Xa - mu) ** 2).mean(0)); Z = (Xa - mu) / sd\n"
        "    A = np.vstack([Z, np.sqrt(lam) * np.eye(Xa.shape[1])]); t = np.concatenate([ya - ya.mean(), np.zeros(Xa.shape[1])])\n"
        "    b = np.linalg.lstsq(A, t, rcond=None)[0]\n    return lambda Xb: ya.mean() + ((Xb - mu) / sd) @ b\n\n"
        "def nested_walk_forward(X, y, lams, first, step, val):\n    X = np.asarray(X, float); y = np.asarray(y, float); out = []\n    k = first\n"
        "    while k < len(y):\n        c = k - val\n        sc = [float(np.mean((y[c:k] - ridge(X[:c], y[:c], l)(X[c:k])) ** 2)) for l in lams]\n"
        "        best = lams[sc.index(min(sc))]\n        hi = min(k + step, len(y))\n        out += list(y[k:hi] - ridge(X[:k], y[:k], best)(X[k:hi]))\n        k += step\n"
        "    return float(np.mean(np.square(out)))\n")
other_passes('a-walk-forward-ridge', wf_b, label='an augmented least-squares ridge')
peek = wf_b.replace("sc = [float(np.mean((y[c:k] - ridge(X[:c], y[:c], l)(X[c:k])) ** 2)) for l in lams]",
                    "hi0 = min(k + step, len(y)); sc = [float(np.mean((y[k:hi0] - ridge(X[:k], y[:k], l)(X[k:hi0])) ** 2)) for l in lams]")
rec(peek != wf_b, 'a-walk-forward-ridge: peeking variant built')
other_fails('a-walk-forward-ridge', peek, label='choosing the penalty on the test block')
leak = wf_b.replace("def ridge(Xa, ya, lam):\n    mu = Xa.mean(0); sd = np.sqrt(((Xa - mu) ** 2).mean(0))",
                    "XALL = None\n\ndef ridge(Xa, ya, lam):\n    mu = XALL.mean(0); sd = XALL.std(0)").replace(
                    "X = np.asarray(X, float); y = np.asarray(y, float); out = []", "global XALL\n    X = np.asarray(X, float); XALL = X; y = np.asarray(y, float); out = []")
rec(leak != wf_b, 'a-walk-forward-ridge: leaky variant built')
other_fails('a-walk-forward-ridge', leak, label='a full-sample scaler')
other_fails('a-walk-forward-ridge', wf_b.replace("sd = np.sqrt(((Xa - mu) ** 2).mean(0))", "sd = Xa.std(0, ddof=1)"), label='a sample standard deviation')
allow('a-walk-forward-ridge', 360, 1e-7, 40, 4)

# ======================================================================== Paper B
correct_ids('b-returns-not-prices', ['a'])

psi = sum(0.6 ** (2 * k) for k in range(400))
key('b-ar1-spread', round(math.sqrt(0.0004 * psi), 6))
wrong('b-ar1-spread', 'no-square', round(0.02 / 0.4, 6))
wrong('b-ar1-spread', 'shock-sd', 0.02)
allow('b-ar1-spread', 0.3, 0.6, 0.0004, 0.64, 0.000625, 0.36)

rho3 = [F('0.12'), F('-0.05'), F('0.08')]
Q = 250 * 252 * sum(rk * rk / (250 - k) for k, rk in enumerate(rho3, 1))
key('b-ljung-box', round(float(Q), 4))
wrong('b-ljung-box', 'box-pierce', round(float(250 * sum(rk * rk for rk in rho3)), 4))
wrong('b-ljung-box', 'no-square', round(float(250 * 252 * sum(rk / (250 - k) for k, rk in enumerate(rho3, 1))), 4))
allow('b-ljung-box', 250, 0.12, -0.05, 0.08, 252, 0.0144, 249, 0.0025, 248, 0.0064, 247, stats.chi2.ppf(0.95, 2))
rec(abs(stats.chi2.ppf(0.95, 2) - 5.99) < 0.005, 'b-ljung-box: the 5% point of chi2(2), three lags less one AR coefficient, is 5.99')
rec(float(Q) < stats.chi2.ppf(0.95, 2) < stats.chi2.ppf(0.95, 3), 'b-ljung-box: Q is below the chi2(2) point, so the stated conclusion holds')

eig = sorted(abs(np.linalg.eigvals(np.array([[1.1, -0.3], [1, 0]]))))
key('b-ar2-root', round(eig[-1], 6))
wrong('b-ar2-root', 'smaller', round(eig[0], 6))
wrong('b-ar2-root', 'sum', round(1.1 - 0.3, 6))
allow('b-ar2-root', 1.1, -0.3, 0.3, 1.21, 1.2, 0.1)

yw = np.linalg.solve(np.array([[1, 0.45], [0.45, 1]]), np.array([0.45, 0.05]))
key('b-yule-walker', round(yw[1], 6))
wrong('b-yule-walker', 'gave-acf', 0.05)
wrong('b-yule-walker', 'no-denominator', round(0.05 - 0.45 ** 2, 6))
wrong('b-yule-walker', 'gave-phi1', round(yw[0], 6))
allow('b-yule-walker', 0.45, 0.05, -0.1525, 0.7975, yw[1], yw[0])

key('b-ma-forecast', float(F('0.0008') + F('0.35') * F('0.014')), part=0)
wrong('b-ma-forecast', 'no-mean', float(F('0.35') * F('0.014')), part=0)
wrong('b-ma-forecast', 'no-shock', 0.0008, part=0)
key('b-ma-forecast', 0.0008, part=1)
wrong('b-ma-forecast', 'decayed', round(float(F('0.0008') + F('0.35') ** 2 * F('0.014')), 6), part=1)
wrong('b-ma-forecast', 'same-as-one', float(F('0.0008') + F('0.35') * F('0.014')), part=1)
allow('b-ma-forecast', 0.0008, 0.35, 0.014)

key('b-arch-lm', float(750 * F('0.0188')))
wrong('b-arch-lm', 'per-lag', float(750 * F('0.0188') / 5))
wrong('b-arch-lm', 'r-not-n', 1.88)
allow('b-arch-lm', 750, 0.0188, stats.chi2.ppf(0.95, 5))
rec(abs(stats.chi2.ppf(0.95, 5) - 11.07) < 0.005, 'b-arch-lm: the 5% point of chi2(5) is 11.07')

def long_run(om_, ab_=0.06 + 0.92):
    v_ = 1e-4
    for _ in range(5000):
        v_ = om_ + ab_ * v_                                # E[sigma^2] under the recursion, iterated to its fixed point
    return v_


Vt = 0.18 ** 2 / 252
om = optimize.brentq(lambda o_: long_run(o_) - Vt, 1e-9, 1e-3, xtol=1e-18)
key('b-garch-target', round(om * 1e6, 4))
wrong('b-garch-target', 'annual', round(0.18 ** 2 * 0.02 * 1e6, 4))
wrong('b-garch-target', 'vol-not-variance', round(0.18 / math.sqrt(252) * 0.02 * 1e6, 4))
wrong('b-garch-target', 'one-minus-beta', round(Vt * 0.08 * 1e6, 4))
allow('b-garch-target', 18, 0.18, 252, 0.06, 0.92, 0.02, 0.08, Vt * 1e4)

v9 = 0.94 * 0.011 ** 2 + 0.06 * 0.028 ** 2
key('b-ewma-update', round(math.sqrt(v9), 6))
wrong('b-ewma-update', 'swapped', round(math.sqrt(0.06 * 0.011 ** 2 + 0.94 * 0.028 ** 2), 6))
wrong('b-ewma-update', 'vol-not-variance', round(0.94 * 0.011 + 0.06 * 0.028, 6))
allow('b-ewma-update', 0.94, 0.011, -0.028, 0.06, 0.000121, 0.000784, v9 * 1e4)

zq = N01.inv_cdf(0.975)
tail = simpson(lambda x: x * N01.pdf(x), zq, 12, 20000) / 0.025          # E[Z | Z > z], by integration
key('b-es-normal', round(3e6 * 0.014 * tail, 2))
wrong('b-es-normal', 'var', round(3e6 * 0.014 * zq, 2))
wrong('b-es-normal', 'density-only', round(3e6 * 0.014 * N01.pdf(zq), 2))
allow('b-es-normal', 0.014, 3e6, 0.975, 97.5, 1.96, N01.pdf(zq), 42000, 0.025, 3e6 * 0.014 * tail, 3e6 * 0.014 * zq)
tolES = W('b-es-normal')['tol']['abs']
for ph_ in (0.0584, 0.05845):
    rec(abs(42000 * ph_ / 0.025 - W('b-es-normal')['answer']) <= tolES, f'b-es-normal: phi rounded to {ph_} gives {42000 * ph_ / 0.025:,.0f}, inside the tolerance {tolES}')
rec(all(abs(w_['value'] - W('b-es-normal')['answer']) > tolES + w_['tol']['abs'] for w_ in W('b-es-normal')['wrong']), 'b-es-normal: no wrong band reaches the widened answer band')

correct_ids('b-spurious-read', ['a'])
allow('b-spurious-read', 11.4, 0.42, 0.98, 1000)

e12 = np.array([0.40, 0.25, 0.05, 0.12, -0.06, 0.02, -0.10, 0.03])
Xd, yd = e12[:-1, None], np.diff(e12)
bhat, res, *_ = np.linalg.lstsq(Xd, yd, rcond=None)
s2 = float(res[0]) / (len(yd) - 1)
tdf = float(bhat[0] / math.sqrt(s2 * np.linalg.inv(Xd.T @ Xd)[0, 0]))
key('b-df-hand', round(tdf, 4))
wrong('b-df-hand', 'slope', round(float(bhat[0]), 4))
wrong('b-df-hand', 'n-divisor', round(float(bhat[0] / math.sqrt(float(res[0]) / len(yd) * np.linalg.inv(Xd.T @ Xd)[0, 0])), 4))
allow('b-df-hand', *e12, float(Xd[:, 0] @ yd), float(Xd[:, 0] @ Xd[:, 0]), s2, -3.34, -1.95, 7, 6)
rec(abs(mackinnoncrit(N=1, regression='n', nobs=np.inf)[1] + 1.95) < 0.02, 'b-df-hand: the no-constant Dickey-Fuller 5% point is about -1.95')
rec(tdf < -1.95 and tdf > -3.34, 'b-df-hand: t misses the Engle-Granger point and passes the plain one')

eg_t = code_py('b-eg-pair', 0)
eg_b = ("import numpy as np\n\ndef adf1_spread(a, b):\n    y = np.log(np.array(a, float)); x = np.log(np.array(b, float))\n"
        "    beta = np.cov(x, y)[0, 1] / np.var(x, ddof=1); e = y - y.mean() - beta * (x - x.mean())\n"
        "    d = e[1:] - e[:-1]; Y = d[1:]; Z = np.stack([e[1:-1], d[:-1]], axis=1)\n"
        "    G = Z.T @ Z; g = np.linalg.solve(G, Z.T @ Y); u = Y - Z @ g\n"
        "    cov = (u @ u) / (len(Y) - 2) * np.linalg.inv(G)\n    return beta, g[0] / np.sqrt(cov[0, 0])\n")
other_passes('b-eg-pair', eg_b, part=0, label='a covariance-ratio beta and normal equations')
df0 = ("import numpy as np\n\ndef adf1_spread(a, b):\n    y = np.log(np.array(a, float)); x = np.log(np.array(b, float))\n"
       "    X = np.column_stack([np.ones(len(x)), x]); c = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ c\n"
       "    de, el = np.diff(e), e[:-1]; rho = el @ de / (el @ el); u = de - rho * el\n"
       "    return c[1], rho / np.sqrt((u @ u) / (len(de) - 1) / (el @ el))\n")
other_fails('b-eg-pair', df0, part=0, label='a plain Dickey-Fuller without the lagged change')
pc = csv('pair-closes.csv')
ya, xb = np.log(pc['a'].to_numpy()), np.log(pc['b'].to_numpy())
e = ya - np.polyval(np.polyfit(xb, ya, 1), xb)
rho13 = float(np.dot(e[:-1], np.diff(e)) / np.dot(e[:-1], e[:-1]))
given = round(rho13, 4)
rec(f'= {given}$' in ITEM['b-eg-pair']['parts'][1]['question'], f'b-eg-pair part 1 quotes the file slope {given}')
key('b-eg-pair', round(optimize.brentq(lambda h_: (1 + given) ** h_ - 0.5, 0.1, 100), 4), part=1)
wrong('b-eg-pair', 'small-rho', round(-math.log(2) / given, 4), part=1)
wrong('b-eg-pair', 'no-log', round(-1 / given, 4), part=1)
t_ab, t_ac = expect_of(eg_t, 'adf1_spread(a, b)[1]'), expect_of(eg_t, 'adf1_spread(a, c)[1]')
rec(t_ab < -3.34 < t_ac, f'b-eg-pair: a-b rejects ({t_ab:.2f}), a-c does not ({t_ac:.2f})')
for c_ in 'ab':
    pv_ = adfuller(np.log(pc[c_].to_numpy()), maxlag=1, autolag=None, regression='c')[1]
    rec(pv_ > 0.05, f'b-eg-pair: ln {c_} does not reject a unit root (ADF(1) p = {pv_:.2f}), as the prose says')
allow('b-eg-pair', 0.5, 500, given, 1 + given, t_ab, t_ac, -3.34, 1e-7, round(optimize.brentq(lambda h_: (1 + given) ** h_ - 0.5, 0.1, 100), 2))

key('b-hedge-notional', float(F('1.6') * 800000))
wrong('b-hedge-notional', 'divided', float(800000 / F('1.6')))
wrong('b-hedge-notional', 'equal', 800000)
allow('b-hedge-notional', 0.35, 1.6, 800000, 12800)

legs = [(-20000, F('50.00'), F('48.20')), (70000, F('20.00'), F('20.10'))]
gross = sum(q * (p1 - p0) for q, p0, p1 in legs)
traded = sum(abs(q) * (p0 + p1) for q, p0, p1 in legs)
key('b-pair-pnl', float(gross - F(5, 10000) * traded))
wrong('b-pair-pnl', 'gross', float(gross))
wrong('b-pair-pnl', 'entry-costs-only', float(gross - F(5, 10000) * sum(abs(q) * p0 for q, p0, _ in legs)))
allow('b-pair-pnl', 20000, 50.00, 70000, 20.00, 48.20, 20.10, 36000, 7000, float(traded), float(F(5, 10000) * traded))

# ======================================================================== Paper C
x = np.float32(100000)
fee = np.float32(0.01)
for _ in range(1000):
    x = np.add(x, fee, dtype=np.float32)
ulp = float(np.spacing(np.float32(100000)))
key('c-float32-fees', float(x) - 100000)
wrong('c-float32-fees', 'exact', 10)
wrong('c-float32-fees', 'absorbed', 0)
allow('c-float32-fees', 32, 24, 100000, 1000, ulp, 16, 17, 23, 0.01)
rec(abs(round(float(x) - 100000, 2) - W('c-float32-fees')['answer']) <= W('c-float32-fees')['tol']['abs'], 'c-float32-fees: a learner who rounds to the penny (7.81) is inside the tolerance')
rec(ulp == 2 ** -7, 'c-float32-fees: float32 spacing near 100,000 is 2^-7')

rc_ = optimize.brentq(lambda r_: np.linalg.cond(np.array([[1, r_], [r_, 1]])) - 1e4, 0.9, 0.9999999999, xtol=1e-14)
key('c-condition-digits', round(rc_, 6))
wrong('c-condition-digits', 'one-over-gap', 0.9999)
rec(abs(math.log10(np.linalg.cond(np.array([[1, 0.9998], [0.9998, 1]]))) - 4) < 0.001, 'c-condition-digits: at r = 0.9998 about four digits go')
allow('c-condition-digits', rc_)

f3 = lambda y: 5 / (1 + y) + 105 / (1 + y) ** 2 - 95
d3 = (f3(0.05 + 1e-6) - f3(0.05 - 1e-6)) / 2e-6
y1 = 0.05 - f3(0.05) / d3
ytrue = optimize.brentq(f3, 0.0, 0.5)
key('c-newton-yield', round(y1, 6))
wrong('c-newton-yield', 'sign', round(0.05 + f3(0.05) / d3, 6))
wrong('c-newton-yield', 'converged', round(ytrue, 6))
allow('c-newton-yield', 95, 105, 0.05, 4.7619, 95.2381, d3, -d3, ytrue)

correct_ids('c-simpson-jump', ['a'])


def q_s(S0, K, r, sg, T, n, start):
    m, s = (r - sg ** 2 / 2) * T, sg * math.sqrt(T)
    U = S0 * math.exp(m + 8 * s)
    f = lambda S: max(S - K, 0) * N01.pdf((math.log(S / S0) - m) / s) / (S * s)
    return math.exp(-r * T) * simpson(f, start, U, n)


bsb = bs_call(100, 105, 0.03, 0.25, 1.0)
e_split = [abs(q_s(100, 105, 0.03, 0.25, 1.0, n, 105) - bsb) for n in (200, 400)]
e_kink = [abs(q_s(100, 105, 0.03, 0.25, 1.0, n, 50.3) - bsb) for n in (200, 400)]
rec(13 < e_split[0] / e_split[1] < 19, f'c-error-rates: split at the strike, halving h divides the error by {e_split[0] / e_split[1]:.1f} (about 16)')
rec(e_kink[0] / e_kink[1] < 8 and e_kink[1] > 10 * e_split[1], f'c-error-rates: with the strike inside a panel the error is {e_kink[1]:.2e} against {e_split[1]:.2e}, no h^4 rate')


def digital_err(n, zk, split):
    # a digital call: integral of 1{z > zk} phi(z) dz by Simpson on a fixed grid [-8, 8], or split at zk and run to 8
    f = N01.pdf if split else (lambda z_: N01.pdf(z_) * (z_ > zk))
    a_, b_ = (zk, 8.0) if split else (-8.0, 8.0)
    return abs(simpson(f, a_, b_, n) - (1 - N01.cdf(zk)))


zks = np.random.default_rng(5).uniform(-1.5, 1.5, 60)
rms = lambda n, split: math.sqrt(np.mean([digital_err(n, z_, split) ** 2 for z_ in zks]))
ratio_fixed = rms(200, False) / rms(400, False)
ratio_split = rms(200, True) / rms(400, True)
rec(1.5 < ratio_fixed < 2.7, f'c-simpson-jump: on a fixed grid halving h divides the digital error by {ratio_fixed:.2f} (order h, about 2)')
rec(ratio_split > 10, f'c-simpson-jump: split at the strike halving h divides the error by {ratio_split:.1f} (order h^4)')
rec(rms(400, False) > 100 * rms(400, True), 'c-simpson-jump: the split rule is far more accurate')

cells = [r_[1] for r_ in W('c-error-rates')['rows']]
rec([c['answer'] for c in cells] == [2, 4, 16], 'c-error-rates: keys 2, 4, 16')
rec(math.isclose(math.sqrt(4), 2), 'c-error-rates: four times the paths divides the error by sqrt(4)')
fd_ref = ("import numpy as np\n\ndef fd_call(S0, K, r, sigma, T, M, N):\n    smax = 3 * K; S = np.linspace(0, smax, M + 1); i = np.arange(1, M); dt = T / N\n"
          "    a = 0.5 * dt * (sigma ** 2 * i ** 2 - r * i); b = 1 - dt * (sigma ** 2 * i ** 2 + r); c = 0.5 * dt * (sigma ** 2 * i ** 2 + r * i)\n"
          "    V = np.maximum(S - K, 0.0)\n    for n in range(1, N + 1):\n        V[1:-1] = a * V[:-2] + b * V[1:-1] + c * V[2:]\n"
          "        V[0], V[-1] = 0.0, smax - K * np.exp(-r * n * dt)\n    return float(np.interp(S0, S, V))\n")
ns = {}
exec(fd_ref, ns)                                         # an explicit grid in S, as the table's row describes
e1 = abs(ns['fd_call'](100, 105, 0.03, 0.25, 1.0, 63, 400) - bsb)       # M a multiple of 63 puts S0 = 100 on a node
e2 = abs(ns['fd_call'](100, 105, 0.03, 0.25, 1.0, 126, 1600) - bsb)
rec(3 < e1 / e2 < 5, f'c-error-rates: grid with dS halved and dtau quartered divides the error by {e1 / e2:.2f} (about 4)')
rec(13 < e_split[0] / e_split[1] < 19, 'c-error-rates: Simpson split at the strike divides by about 16')
rec([[w_['id'] for w_ in c['wrong']] for c in cells] == [['mc-linear'], ['fd-first-order'], ['simpson-unsplit']]
    and all(k in ITEM['c-error-rates']['feedback']['byKey'] for k in ('mc-linear', 'fd-first-order', 'simpson-unsplit')), 'c-error-rates: slip feedback keyed on wrong ids')
rec([c['wrong'][0]['value'] for c in cells] == [4, 2, 4], 'c-error-rates: wrong values 4, 2, 4 (1/n, first order, unsplit h^2)')
allow('c-error-rates', 2, 4, 16)

fd_t = code_py('c-three-pricers', 0)
for c_ in fd_t:
    a_ = eval(c_['call'].replace('fd_call', '(lambda *a: a)'))
    S0_, K_, r_, s_, T_, M_, N_ = a_
    rec(abs(float(c_['expect']) - bs_call(S0_, K_, r_, s_, T_)) < 0.005, f'c-three-pricers: {c_["call"]} within 0.005 of Black-Scholes')
    dx_ = 10 * s_ * math.sqrt(T_) / M_
    rec(M_ % 2 == 0 and T_ / N_ <= 1 / (s_ ** 2 / dx_ ** 2 + r_), f'c-three-pricers: {c_["call"]} has S0 on a node and is stable')
fd_b = ("import numpy as np\nfrom scipy import sparse\n\ndef fd_call(S0, K, r, sigma, T, M, N):\n    x = np.log(S0) + np.linspace(-5, 5, M + 1) * sigma * np.sqrt(T); h = x[1] - x[0]; k = T / N\n"
        "    D2 = sparse.diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(M + 1, M + 1)) / h ** 2; D1 = sparse.diags([-1.0, 1.0], [-1, 1], shape=(M + 1, M + 1)) / (2 * h)\n"
        "    L = 0.5 * sigma ** 2 * D2 + (r - 0.5 * sigma ** 2) * D1 - r * sparse.identity(M + 1)\n    V = np.clip(np.exp(x) - K, 0, None)\n"
        "    for n in range(N):\n        V = V + k * (L @ V); V[0] = 0; V[-1] = np.exp(x[-1]) - K * np.exp(-r * (n + 1) * k)\n    return V[M // 2]\n")
other_passes('c-three-pricers', fd_b, part=0, label='a sparse-operator grid')
q_t = code_py('c-three-pricers', 1)
for c_ in q_t:
    a_ = eval(c_['call'].replace('quad_call', '(lambda *a: a)'))
    rec(abs(float(c_['expect']) - bs_call(a_[0], a_[1], a_[2], a_[3], a_[4])) < 1e-9, f'c-three-pricers: {c_["call"]} expects Black-Scholes')
    rec(abs(q_s(*a_[:5], a_[5], a_[1]) - bs_call(*a_[:5])) < 1e-5, f'c-three-pricers: Simpson from the strike with n = {a_[5]} is within 1e-5')
quad_b = ("from scipy import integrate, stats\nimport math\n\ndef quad_call(S0, K, r, sigma, T, n):\n    s = sigma * math.sqrt(T); m = math.log(S0) + (r - sigma ** 2 / 2) * T\n"
          "    f = lambda S: (S - K) * stats.lognorm.pdf(S, s, scale=math.exp(m))\n    return math.exp(-r * T) * integrate.quad(f, K, math.inf, limit=200)[0]\n")
other_passes('c-three-pricers', quad_b, part=1, label='scipy quad on the lognormal density')
mc_t = code_py('c-three-pricers', 2)
mc_b = ("import numpy as np\n\ndef mc_cv_call(S0, K, r, sigma, T, n, seed):\n    g = np.random.default_rng(seed + 1000); z = g.normal(size=n)\n"
        "    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z); d = np.exp(-r * T)\n    Y = d * np.maximum(ST - K, 0)\n"
        "    X = np.column_stack([np.ones(n), d * ST - S0, d * ST ** 2 - S0 ** 2 * np.exp((r + sigma ** 2) * T)])\n"
        "    coef = np.linalg.solve(X.T @ X, X.T @ Y)\n    res = Y - X[:, 1:] @ coef[1:]\n    return res.mean(), res.std(ddof=1) / np.sqrt(n)\n")
other_passes('c-three-pricers', mc_b, part=2, label='a regression-form estimator on other seeds')
one_ctl = ("import numpy as np\n\ndef mc_cv_call(S0, K, r, sigma, T, n, seed):\n    z = np.random.default_rng(seed).standard_normal(n)\n"
           "    ST = S0 * np.exp((r - sigma ** 2 / 2) * T + sigma * np.sqrt(T) * z); d = np.exp(-r * T)\n    Y, X = d * np.maximum(ST - K, 0), d * ST\n"
           "    adj = Y - np.cov(Y, X)[0, 1] / np.var(X, ddof=1) * (X - S0)\n    return adj.mean(), adj.std(ddof=1) / np.sqrt(n)\n")
other_fails('c-three-pricers', one_ctl, part=2, label='a one-control estimator')
zz = np.random.default_rng(11).standard_normal(100000)
STz = 100 * np.exp(-0.00125 + 0.25 * zz)
Yz, Xz = math.exp(-0.03) * np.maximum(STz - 105, 0), math.exp(-0.03) * STz
plain = float(Yz.std(ddof=1) / math.sqrt(1e5))
one = float((Yz - np.polyfit(Xz, Yz, 1)[0] * (Xz - 100)).std(ddof=1) / math.sqrt(1e5))
ns = {}
exec(W('c-three-pricers', 2)['solution'], ns)
two = ns['mc_cv_call'](100, 105, 0.03, 0.25, 1.0, 100000, 11)[1]
rec(two < 0.016 < one < plain, f'c-three-pricers: errors two {two:.4f} < 0.016 < one {one:.4f} < plain {plain:.4f}')
rec(abs(100 ** 2 * math.exp((0.03 + 0.0625) * 1.0) - math.exp(-0.03) * simpson(lambda z_: (100 * math.exp(-0.00125 + 0.25 * z_)) ** 2 * N01.pdf(z_), -12, 12, 20000)) < 1e-6,
    'c-three-pricers: E[e^{-rT} S_T^2] = S0^2 e^{(r + sigma^2)T}')
allow('c-three-pricers', 0.4, 0.01, bsb, bs_call(50, 45, 0.01, 0.4, 0.5), plain, one, two, 0.016, 1e-6, 1e-5, 8, 3, 4)

mu7 = np.array([0.06, 0.10])
S7 = np.array([[0.15 ** 2, 0.2 * 0.15 * 0.25], [0.2 * 0.15 * 0.25, 0.25 ** 2]])
obj = lambda w_: -(mu7 @ w_ - 2.5 / 2 * w_ @ S7 @ w_)
sol = optimize.minimize(obj, np.array([0.5, 0.5]), method='SLSQP', constraints=[{'type': 'eq', 'fun': lambda w_: w_.sum() - 1}], options={'ftol': 1e-15})
w7 = sol.x
lam7 = mu7[0] - 2.5 * (S7 @ w7)[0]
key('c-kkt-hand', round(w7[0], 6), part=0)
un = optimize.minimize(obj, np.array([0.5, 0.5]), method='BFGS', options={'gtol': 1e-12}).x
wrong('c-kkt-hand', 'normalised', round(un[0] / un.sum(), 6), part=0)
mv = optimize.minimize(lambda w_: w_ @ S7 @ w_, np.array([0.5, 0.5]), method='SLSQP', constraints=[{'type': 'eq', 'fun': lambda w_: w_.sum() - 1}], options={'ftol': 1e-16}).x
wrong('c-kkt-hand', 'min-variance', round(mv[0], 6), part=0)
key('c-kkt-hand', round(lam7, 6), part=1)
wrong('c-kkt-hand', 'sign', round(-lam7, 6), part=1)
wrong('c-kkt-hand', 'unscaled', round(mu7[0] - (S7 @ w7)[0], 6), part=1)
allow('c-kkt-hand', 1.25, 0.06, 0.10, 0.15, 0.25, 0.2, 2.5, 0.0225, 0.0075, 0.0625, 0.07, 0.039, w7[0], lam7)

kk_t = code_py('c-kkt-code')
for c_ in kk_t:
    call = c_['call']
    inner = call[len('float(sum('):-2] if call.startswith('float(sum(') else call
    mu_, cov_, g_ = eval(inner.replace('mv_weights', '(lambda *a: a)'))
    mu_, cov_ = np.array(mu_), np.array(cov_)
    s_ = optimize.minimize(lambda w_: -(mu_ @ w_ - g_ / 2 * w_ @ cov_ @ w_), np.ones(len(mu_)) / len(mu_), method='SLSQP',
                           constraints=[{'type': 'eq', 'fun': lambda w_: w_.sum() - 1}], options={'ftol': 1e-16, 'maxiter': 500}).x
    want = [1.0] if call.startswith('float(sum(') else list(s_)
    got = eval(c_['expect'])
    got = [got] if not isinstance(got, list) else got
    rec(all(abs(a_ - b_) < 1e-6 for a_, b_ in zip(got, want)), f'c-kkt-code: {call[:40]}... matches SLSQP to 1e-6')
rec(all('[0.06, 0.1]' not in e_['call'] for e_ in W('c-kkt-code')['examples']), 'c-kkt-code: the visible example is not the c-kkt-hand problem')
allow('c-kkt-code', 1e-8)

res_lp = optimize.linprog([0.96, 1.01], A_ub=-np.array([[1, 0.05], [0, 1.05]]), b_ub=-np.array([80, 120]), bounds=[(0, None)] * 2, method='highs')
duals = -res_lp.ineqlin.marginals
key('c-dedication-lp', round(res_lp.fun, 4), part=0)
res_nc = optimize.linprog([0.96, 1.01], A_ub=-np.array([[1, 0], [0, 1.05]]), b_ub=-np.array([80, 120]), bounds=[(0, None)] * 2, method='highs')
wrong('c-dedication-lp', 'no-coupon', round(res_nc.fun, 4), part=0)
rc_c = 0.95 - 1.07 * duals[1]
key('c-dedication-lp', round(rc_c, 6), part=1)
wrong('c-dedication-lp', 'ignored-coupon', round(0.95 - 1.07 * (1.01 / 1.05), 6), part=1)
wrong('c-dedication-lp', 'sign', round(-rc_c, 6), part=1)
res_3 = optimize.linprog([0.96, 1.01, 0.95], A_ub=-np.array([[1, 0.05, 0], [0, 1.05, 1.07]]), b_ub=-np.array([80, 120]), bounds=[(0, None)] * 3, method='highs')
rec(res_3.fun < res_lp.fun - 1e-6 and res_3.x[2] > 0, f'c-dedication-lp: adding the third bond cuts the cost ({res_lp.fun:.2f} to {res_3.fun:.2f}), as the explanation says')
rec(abs(80 * duals[0] + 120 * duals[1] - res_lp.fun) < 1e-6, 'c-dedication-lp: the dual objective equals the primal cost')
allow('c-dedication-lp', 80000, 120000, 0.96, 0.05, 1.05, 1.01, 0.95, 1.07, 80, 120, *res_lp.x, res_lp.fun, 0.048, *duals)

correct_ids('c-convex-functions', ['a', 'b', 'c', 'd'])
g_ = np.random.default_rng(3)
Sg = np.array([[0.04, 0.01], [0.01, 0.09]])
Rs = g_.standard_normal((5, 2)) * 0.05
fns = {'a': lambda w_: w_ @ Sg @ w_, 'b': lambda w_: math.sqrt(w_ @ Sg @ w_), 'c': lambda w_: max(-Rs @ w_),
       'e': lambda w_: (np.array([0.05, 0.08]) @ w_) / math.sqrt(w_ @ Sg @ w_)}
for k_, f_ in fns.items():
    viol = 0
    for _ in range(3000):
        u_, v_ = g_.uniform(0.05, 1, 2), g_.uniform(0.05, 1, 2)
        viol += f_((u_ + v_) / 2) > (f_(u_) + f_(v_)) / 2 + 1e-12
    rec((viol == 0) == (k_ != 'e'), f'c-convex-functions: midpoint test on "{k_}" finds {viol} violations')
rec(-math.log(2) < (-math.log(1) - math.log(3)) / 2 and not ((-1) ** 3 <= (-2) ** 3 / 2 + 0 ** 3 / 2), 'c-convex-functions: -ln x passes and x^3 fails a midpoint test')
allow('c-convex-functions', 6)

v11 = np.array([0.6, 0.3, 0.1]) - 0.5 * np.array([0.2, -0.6, 0.5])
pr = optimize.minimize(lambda w_: ((w_ - v11) ** 2).sum(), np.ones(3) / 3, method='SLSQP', bounds=[(0, 1)] * 3,
                       constraints=[{'type': 'eq', 'fun': lambda w_: w_.sum() - 1}], options={'ftol': 1e-16}).x
key('c-projected-step', round(pr[0], 6))
wrong('c-projected-step', 'renormalise', round(float(F('0.5') / F('1.1')), 6))
wrong('c-projected-step', 'shift-all', round(v11[0] - (v11.sum() - 1) / 3, 6))
wrong('c-projected-step', 'no-projection', round(v11[0], 6))
allow('c-projected-step', 0.6, 0.3, 0.1, 0.2, -0.6, 0.5, *v11, *pr, 0.05)

# ======================================================================== Paper D
r1 = pd.Series([0.021, -0.012, 0.008, -0.025, 0.015, 0.006])
ddv = math.sqrt((r1.clip(upper=0) ** 2).mean())
so = r1.mean() / ddv * math.sqrt(12)
key('d-sortino', round(so, 5))
wrong('d-sortino', 'sharpe', round(r1.mean() / r1.std() * math.sqrt(12), 5))
wrong('d-sortino', 'losing-months-only', round(r1.mean() / math.sqrt((r1[r1 < 0] ** 2).mean()) * math.sqrt(12), 5))
wrong('d-sortino', 'monthly', round(r1.mean() / ddv, 5))
allow('d-sortino', *r1, 0.000144, 0.000625, r1.mean(), ddv, so)

left, cost, got = 60000, F(0), []
for vol, px in [(120000, F('50.10')), (80000, F('50.20')), (200000, F('50.05')), (150000, F('50.30')), (90000, F('50.40'))]:
    q_ = min(vol // 10, left)
    left -= q_
    got.append(q_)
    cost += q_ * px
key('d-participation-fill', round(float(cost / 60000), 6))
wrong('d-participation-fill', 'mean-price', round(float(sum(F(x) for x in ('50.10', '50.20', '50.05', '50.30', '50.40')) / 5), 6))
wrong('d-participation-fill', 'full-last-bar', round(float((cost - 5000 * F('50.40') + 9000 * F('50.40')) / 64000), 6))
allow('d-participation-fill', 9000, 60000, 120000, 80000, 200000, 150000, 90000, 50.10, 50.20, 50.05, 50.30, 50.40, *got, float(cost), float(cost / 60000))

key('d-survivors', float((400 * F('0.09') - 100 * F('0.30')) / 500))
wrong('d-survivors', 'survivors', 0.09)
wrong('d-survivors', 'plain-mean', float((F('0.09') - F('0.30')) / 2))
allow('d-survivors', 30, 500, 400, 0.09, 100, -0.30, 9, 7.8)
rec(abs((0.09 - 0.012) * 100 - 7.8) < 1e-9, 'd-survivors: bias of 7.8 percentage points')

correct_ids('d-held-out', ['a'])
allow('d-held-out', 2012, 2025)

se5 = math.sqrt((1 + 0.35 ** 2 / 2) / 60)
key('d-sharpe-interval', round((0.35 - 1.96 * se5) * math.sqrt(12), 5))
rec(abs(N01.inv_cdf(0.975) - 1.96) < 5e-5, 'd-sharpe-interval: 1.96 is the 97.5% normal point')
wrong('d-sharpe-interval', 'monthly', round(0.35 - 1.96 * se5, 5))
wrong('d-sharpe-interval', 'point', round(0.35 * math.sqrt(12), 5))
allow('d-sharpe-interval', 0.35, 60, 1.06125, se5, 0.35 - 1.96 * se5, 0.35 * math.sqrt(12), 1.96, 95)

correct_ids('d-universe-date', ['a'])
allow('d-universe-date', 300, 31, 2024, 2015)

r7 = pd.Series([0.05, -0.02, 0.01, -0.04, 0.03])
s7 = -(r7 - r7.mean())
w7d = s7 / s7.abs().sum()
key('d-reversal-weights', round(w7d[3], 6))
wrong('d-reversal-weights', 'no-demean', round(0.04 / r7.abs().sum(), 6))
wrong('d-reversal-weights', 'momentum', round(-w7d[3], 6))
allow('d-reversal-weights', *r7, 0.006, -0.046, 0.046, s7.abs().sum(), w7d[3])

br = 250 * 52
ic_need = optimize.brentq(lambda ic_: 0.4 * ic_ * math.sqrt(br) - 0.8, 1e-4, 1)
key('d-fundamental-law', round(ic_need, 6))
wrong('d-fundamental-law', 'no-tc', round(0.8 / math.sqrt(br), 6))
wrong('d-fundamental-law', 'tc-multiplied', round(0.8 * 0.4 / math.sqrt(br), 6))
wrong('d-fundamental-law', 'one-rebalance', round(0.8 / (0.4 * math.sqrt(250)), 6))
allow('d-fundamental-law', 250, 52, 0.4, 0.8, 40, br, math.sqrt(br), 13000)

cst = F(12) * F('0.40') * F(12, 10000)
key('d-net-sharpe', round(float((F('0.09') - cst) / F('0.06')), 5))
wrong('d-net-sharpe', 'one-month', round(float((F('0.09') - F('0.40') * F(12, 10000)) / F('0.06')), 5))
wrong('d-net-sharpe', 'gross', 1.5)
allow('d-net-sharpe', 9, 6, 40, 12, 0.40, 0.0012, float(cst), float(F('0.09') - cst), 0.06)

sr_t = code_py('d-signal-report')
pn = csv('signal-panel.csv')
sp = pn.pivot(index='date', columns='ticker', values='signal').sort_index()
fr = pn.pivot(index='date', columns='ticker', values='fwd_ret').sort_index()


def report_b(sp_, fr_):
    ics = [stats.spearmanr(sp_.loc[d], fr_.loc[d])[0] for d in sp_.index]
    rk_ = sp_.rank(axis=1)
    wt = rk_.sub(rk_.mean(axis=1), axis=0)
    wt = wt.div(wt.abs().sum(axis=1), axis=0)
    return float(np.mean(ics)), float((wt.diff().abs().sum(axis=1) / 2).iloc[1:].mean())


rb_full, rb_10 = report_b(sp, fr), report_b(sp.iloc[:10], fr.iloc[:10])
hand = pd.DataFrame({'date': ['d1'] * 4 + ['d2'] * 4 + ['d3'] * 4, 'ticker': list('ABCD') * 3,
                     'signal': [0.2, -0.1, 0.5, 0.0, 0.3, 0.1, -0.2, 0.4, -0.3, 0.6, 0.1, 0.2],
                     'fwd_ret': [0.01, -0.02, 0.03, 0.0, -0.01, 0.02, 0.01, 0.04, 0.0, 0.02, -0.03, 0.01]})
rb_h = report_b(hand.pivot(index='date', columns='ticker', values='signal'), hand.pivot(index='date', columns='ticker', values='fwd_ret'))
for c_, v_ in zip(sr_t, [rb_full[0], rb_full[1], rb_10[0], rb_h[0], rb_h[1]]):
    rec(math.isclose(eval(c_['expect']), v_, rel_tol=1e-9), f'd-signal-report {c_["call"][:40]}: scipy spearmanr and a pivot agree ({v_:.6f})')
allow('d-signal-report', 20, 30, rb_full[0], rb_full[1], 1e-9)

S, K, r_, s_, T_ = 80, 84, 0.03, 0.32, 0.4
hb = 0.01
gam = (bs_call(S + hb, K, r_, s_, T_) - 2 * bs_call(S, K, r_, s_, T_) + bs_call(S - hb, K, r_, s_, T_)) / hb ** 2
d1 = (math.log(S / K) + (r_ + s_ ** 2 / 2) * T_) / (s_ * math.sqrt(T_))
key('d-gamma-pnl', round(0.5 * gam * 9, 6))
wrong('d-gamma-pnl', 'no-half', round(gam * 9, 6))
wrong('d-gamma-pnl', 'not-squared', round(0.5 * gam * 3, 6))
allow('d-gamma-pnl', 80, 84, 0.03, 0.32, 0.4, d1, N01.pdf(d1), gam, 0.5 * gam * 9)

bf = (F('12.45') - 2 * F('8.35') + F('4.10')) / 25
key('d-butterfly-density', float(bf))
wrong('d-butterfly-density', 'sign', float(-bf))
wrong('d-butterfly-density', 'no-square', float(bf * 5))
allow('d-butterfly-density', 12.45, 8.35, 4.10, 90, 95, 100, 16.70, -0.15, 25)

pf_t = code_py('d-parity-fit')
for c_ in pf_t[:4]:
    K_, C_, P_ = eval(c_['call'].replace('parity_fit', '(lambda *a: a)').rsplit('[', 1)[0])
    K_, C_, P_ = np.array(K_, float), np.array(C_, float), np.array(P_, float)
    ok = ~np.isnan(C_ - P_)
    sl, ic = np.polyfit(K_[ok], (C_ - P_)[ok], 1)
    want = -sl if c_['call'].endswith('[0]') else ic / -sl
    rec(math.isclose(eval(c_['expect']), want, rel_tol=1e-9), f'd-parity-fit {c_["call"][-30:]}: polyfit gives {want:.6f}')
rec(abs(eval(pf_t[0]['expect']) - math.exp(-0.015)) < 0.001 and abs(eval(pf_t[1]['expect']) - 100 * math.exp(0.0075)) < 0.05,
    'd-parity-fit: the chain was priced with D = exp(-0.015) and F = 100 exp(0.0075), and the fit recovers them')
other_fails('d-parity-fit', W('d-parity-fit')['solution'].replace("float(a / D)", "float(a)"), label='returning the intercept as the forward')
allow('d-parity-fit', eval(pf_t[0]['expect']), eval(pf_t[1]['expect']), 1e-9)

c13b = 9.80
key('d-atm-vol', round(c13b / (250 * 0.5) / N01.pdf(0), 6))
wrong('d-atm-vol', 'no-root-t', round(c13b / 250 / N01.pdf(0), 6))
wrong('d-atm-vol', 'inverted', round(c13b * N01.pdf(0) / (250 * 0.5), 6))
exact = optimize.brentq(lambda v_: 250 * (2 * N01.cdf(v_ * 0.5 / 2) - 1) - c13b, 0.01, 2)
rec(abs(exact - c13b / (250 * 0.5) / N01.pdf(0)) < 0.001, f'd-atm-vol: the exact implied volatility {exact:.5f} is close to the approximation')
allow('d-atm-vol', 9.80, 250, 0.25, 0.5, 2.5066, 0.4, c13b / (250 * 0.5) / N01.pdf(0))

key('d-audit-ids', int(np.count_nonzero((np.arange(1, 10 ** 6 + 1) % 6 == 0) | (np.arange(1, 10 ** 6 + 1) % 14 == 0))))
wrong('d-audit-ids', 'no-overlap', 10 ** 6 // 6 + 10 ** 6 // 14)
wrong('d-audit-ids', 'product', 10 ** 6 // 6 + 10 ** 6 // 14 - 10 ** 6 // 84)
allow('d-audit-ids', 1, 10 ** 6, 6, 14, 42, 166666, 71428, 23809, 84)
rec(math.lcm(6, 14) == 42, 'd-audit-ids: lcm(6, 14) = 42')

a15 = [2, -1, 3, 1, -2, 2, 1, -3, 3]
seen, run_, cnt = {0: 1}, 0, 0
pref = [0]
for v_ in a15:
    run_ += v_
    pref.append(run_)
    cnt += seen.get(run_ - 3, 0)
    seen[run_] = seen.get(run_, 0) + 1
key('d-sum-runs', cnt)
lo_, s_w, win = 0, 0, 0
for hi_, v_ in enumerate(a15):
    s_w += v_
    while s_w > 3 and lo_ <= hi_:
        s_w -= a15[lo_]
        lo_ += 1
    win += s_w == 3
wrong('d-sum-runs', 'window', win)
wrong('d-sum-runs', 'singles-missed', cnt - sum(v_ == 3 for v_ in a15))
rec(ITEM['d-sum-runs']['explain']['text'].startswith('The prefix sums are ' + ', '.join(str(p) for p in pref)), 'd-sum-runs: the explanation lists the prefix sums')
allow('d-sum-runs', *a15, *pref)

correct_ids('d-constraints', ['a'])
nl = 200000 * math.log2(200000)
rec(abs(nl / 1e6 - 3.5) < 0.05 and 200000 ** 2 == 4e10 and 4e10 / 1e8 == 400, 'd-constraints: n log n about 3.5 million; n^2 = 4e10, 400 s')
allow('d-constraints', 200000, 3.5, 4e10, 1e8, 25)

e17 = 1 / (1 + 10 ** 0.5)
key('d-rating-odds', round(e17, 6))
wrong('d-rating-odds', 'flipped', round(1 - e17, 6))
wrong('d-rating-odds', 'natural-base', round(1 / (1 + math.exp(0.5)), 6))
allow('d-rating-odds', 1400, 1600, 400, 200, 0.5, math.sqrt(10), 1 + math.sqrt(10), e17)

# ---------------------------------------------------------------- every numeric wrong asserted, papers sized, topics covered
for iid, it in ITEM.items():
    for w in ([it['widget']] if 'widget' in it else [p['widget'] for p in it['parts']]):
        if w['kind'] == 'numeric':
            for x_ in w.get('wrong', []):
                rec(any(abs(x_['value'] - a_) <= max(x_['tol']['abs'] / 10, 1e-9) for a_ in ALLOW.get(iid, [])), f'{iid} wrong "{x_["id"]}" asserted by route B')
                bk = (it.get('feedback') or {}).get('byKey') or {}
                bks = [bk] + [p['feedback'].get('byKey', {}) for p in it.get('parts', [])]
                rec(any(x_['id'] in b for b in bks), f'{iid} wrong "{x_["id"]}" has a byKey line')
        if w['kind'] in ('choice', 'multi'):
            rec(w.get('shuffle') is True, f'{iid}: choice shuffled')
for p in doc['parts']:
    if p['kind'] == 'paper':
        n = len(p['items']) + sum(d['n'] for d in p.get('draw', []))
        rec(10 <= n <= 25, f'{p["id"]}: {n} items (10 to 25)')
        rec(p['id'] != 'numerics-optimisation' or p['minutes'] <= 120, f'{p["id"]}: {p["minutes"]} minutes (paper C stays one paper only at 120 or less)')
        pace = sum(it['pace'] for it in p['items']) + (1800 if p.get('draw') else 0)
        rec(p['minutes'] * 60 >= 1.25 * pace - 1e-9, f'{p["id"]}: {p["minutes"]} min covers 1.25 times the pace {pace} s')
        ds = [it['difficulty'] for it in p['items']]
        rec(sum(d in (3, 4) for d in ds) / len(ds) >= 0.6, f'{p["id"]}: difficulty mostly 3 and 4 ({sum(d in (3, 4) for d in ds)} of {len(ds)})')
        rec(p['pass'] == 0.7, f'{p["id"]}: pass 0.7')
cur = json.load(open(os.path.join(CDIR, 'curriculum.json')))
skill_topic = {}
for st in cur['stages']:
    for tp in st['topics']:
        for c in tp['courses']:
            for s in json.load(open(os.path.join(CDIR, 'courses', c, 'course.json')))['skills']:
                skill_topic[s] = tp['id']
AUTO = ('numeric', 'choice', 'multi', 'code', 'table', 'order', 'expression')
covered = {}
for iid, it in ITEM.items():
    kinds = [it['widget']['kind']] if 'widget' in it else [p['widget']['kind'] for p in it['parts']]
    if all(k in AUTO for k in kinds):
        for s in it['skills']:
            covered.setdefault(skill_topic[s], set()).add(iid)
rec(sorted(covered) == ['2.1', '2.2', '2.3', '2.4', '2.5'], f'every topic 2.1 to 2.5 on an auto-graded item, none from 2.6 (the researcher track): {sorted(covered)}')
for tp in sorted(covered):
    rec(len(covered[tp]) >= 2, f'topic {tp}: {len(covered[tp])} auto-graded items')
stage2_skills = {s for s, tp in skill_topic.items() if tp.startswith('2.') and tp != '2.6'}
used = {s for it in ITEM.values() for s in it['skills']}
rec(stage2_skills <= used, f'every Stage 2 skill outside topic 2.6 on an item (missing {sorted(stage2_skills - used)})')
rec(not any(skill_topic[s_] == '2.6' for s_ in used), 'no item carries a topic 2.6 skill')
refs = {n_ for it in ITEM.values() for w_ in ([it['widget']] if 'widget' in it else [p_['widget'] for p_ in it['parts']]) for n_ in w_.get('data', {})}
files_ = set(os.listdir(DATA))
rec(files_ == refs, f'every data file is used by an item, and every named file exists (files {sorted(files_)}, used {sorted(refs)})')
# drawn pools hold at least twice n
for p in doc['parts']:
    for d in p.get('draw', []):
        src, name = d['from'].split('/')
        lo_d, hi_d = d['difficulty']
        pool = [x_ for f_ in glob.glob(os.path.join(CDIR, 'drills', f'{name}-*.json')) for x_ in [json.load(open(f_))] if lo_d <= x_['difficulty'] <= hi_d]
        rec(len(pool) >= 2 * d['n'], f'{p["id"]} draw {d["from"]}: pool {len(pool)} >= 2n = {2 * d["n"]}')
        rec(all(x_.get('pace', 0) <= 1800 for x_ in pool), f'{p["id"]} draw {d["from"]}: every drill pace within the 1800 s allowed')
# no explanation names a shuffled option by place
PLACE = re.compile(r'\b(first|second|third|fourth|last|top|bottom)\s+(option|answer|choice|one)\b|\boption [A-F]\b|\([a-f]\)', re.I)
for iid, it in ITEM.items():
    if 'widget' not in it or it['widget']['kind'] not in ('choice', 'multi'):
        continue
    rec(not PLACE.search(json.dumps({k: v for k, v in it.items() if k not in ('widget', 'parts')}) + json.dumps(it.get('widget', {}).get('options', []))),
        f'{iid}: no option named by place')

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard', 'starter', 'solution', 'tests', 'examples', 'skills', 'placeholder', 'data', 'tol', 'value'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v_ in o.items():
            if kk not in SKIP:
                yield from strings(v_, kk)
    elif isinstance(o, list):
        for v_ in o:
            yield from strings(v_, k)


def tokens(s):
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)
    s = re.sub(r'`[^`]*`', ' ', s)                       # inline code: names and calls, read by the code checks
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t and 'e' not in t.lower() else 0), t


for iid, it in ITEM.items():
    vals = [abs(v_) for v_ in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v_ for k, v_ in it.items() if k not in ('difficulty', 'pace')}):
        for v_, dec, t in tokens(s):
            if dec == 0 and v_ == int(v_) and v_ <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v_ - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
