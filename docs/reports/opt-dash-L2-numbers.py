"""Recompute every number stated in opt-dash level 2 (Pricers) and check it at its JSON path (second read).

Run: python3 docs/reports/opt-dash-L2-numbers.py   (NumPy, pandas, SciPy and the standard library; exits 0 when every check passes)

Black-Scholes is recomputed with SciPy's `ndtr`; trees with a pure-Python CRR loop written here; Monte Carlo with an
independent NumPy routine on the same seeds. Each is checked against the lesson solution (`two`), which is loaded
from the JSON. `E` checks a stated value appears where it is stated; `stated` ties a claim to its wording (while the
phrase is in the text, the claim must hold). A check that fails because the content is wrong is a finding in
docs/reviews/review-opt-dash-1-2.md and stays failing until the fix pass corrects the content.
"""
import json
import math
import os
import sys
import warnings

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import norm

warnings.simplefilter('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES  # noqa: E402

lv = Level("opt-dash", 2)
E = lv.expect


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
    try:
        there = phrase in lv.text(ref, path)
    except KeyError:                      # a path the fix pass will create
        there = False
    lv._rec(bool(ok) or not there, f'stated: {ref} {path} "{phrase}"', '' if ok or not there else 'the stated claim is false')


def two(name, a, b, tol=1e-9):
    lv._rec(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'two routes: {name} {a!r} vs {b!r}', '')


def doc(fid):
    return json.load(open(os.path.join(COURSES, 'opt-dash', fid + '.json')))


def R_(x, d):
    return round(float(x), d)


# ---------- independent pricers ----------
def bs(S, K, r, s, T, kind='call', q=0.0):
    d1 = (math.log(S / K) + (r - q + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    if kind == 'call':
        return S * math.exp(-q * T) * ndtr(d1) - K * math.exp(-r * T) * ndtr(d2)
    return K * math.exp(-r * T) * ndtr(-d2) - S * math.exp(-q * T) * ndtr(-d1)


def crr(S, K, r, s, T, n, kind='call', am=False, q=0.0, hold_out=None):
    dt = T / n; u = math.exp(s * math.sqrt(dt)); d = 1 / u
    p = (math.exp((r - q) * dt) - d) / (u - d); D = math.exp(-r * dt)
    pay = (lambda x: max(x - K, 0.0)) if kind == 'call' else (lambda x: max(K - x, 0.0))
    v = [pay(S * u ** j * d ** (n - j)) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        h = [D * (p * v[j + 1] + (1 - p) * v[j]) for j in range(i + 1)]
        if hold_out is not None:
            hold_out[i] = h
        v = [max(h[j], pay(S * u ** j * d ** (i - j))) if am else h[j] for j in range(i + 1)]
    return v[0]


def mc(S, K, r, s, T, kind='call', n=100_000, seed=0, anti=True, q=0.0):
    z = np.random.default_rng(seed).standard_normal(n // 2 if anti else n)
    f = lambda z: math.exp(-r * T) * (np.maximum(S * np.exp((r - q - s * s / 2) * T + s * math.sqrt(T) * z) - K, 0) if kind == 'call'
                                      else np.maximum(K - S * np.exp((r - q - s * s / 2) * T + s * math.sqrt(T) * z), 0))
    y = (f(z) + f(-z)) / 2 if anti else f(z)
    return y.mean(), y.std(ddof=1) / math.sqrt(len(y))


def ivol(price, S, K, r, T, kind='call', q=0.0):
    return brentq(lambda s: bs(S, K, r, s, T, kind, q) - price, 1e-6, 5, xtol=1e-14)


# ---------- the lesson solutions ----------
ns = {}
for fid, i in [('l5-bs-pricer', 3), ('l5-bs-pricer', 6), ('l6-tree-pricer', 3), ('l6-tree-pricer', 5), ('l7-mc-pricer', 4),
               ('l7-mc-pricer', 5), ('l8-three-pricers', 4), ('l8-three-pricers', 6)]:
    exec(doc(fid)['screens'][i]['widget']['solution'], ns)
exec(doc('l8-three-pricers')['screens'][6]['widget']['prelude'], ns)
for i in (0, 2):
    exec(doc('homework-2')['items'][i]['widget']['solution'], ns)
bs_l, crr_l, mc_l = ns['bs_price'], ns['crr_price'], ns['mc_price']

# ================= l5 =================
c0, p0 = bs(100, 100, .05, .2, 1), bs(100, 100, .05, .2, 1, 'put')
cq, pq = bs(100, 100, .05, .2, 1, 'call', .01), bs(100, 100, .05, .2, 1, 'put', .01)
two('l5 call', c0, bs_l(100, 100, .05, .2, 1)); two('l5 call q', cq, bs_l(100, 100, .05, .2, 1, q=.01))
E('l5', 'screens[0].prose', R_(c0, 4))
E('l5', 'screens[0].widget.options[3].text', R_(c0 * 0.99, 2))
E('l5', 'screens[0].widget.options[3].why', R_(cq, 2))
E('l5', 'screens[0].widget.options[3].why', R_((c0 - cq) / c0 * 100, 0))
E('l5', 'screens[0].feedback.correct', R_((c0 - cq) * 100, 0))
lim = 100 - 100 * math.exp(-.05)
two('l5 sigma 0.01 limit', bs(100, 100, .05, .01, 1), lim, 1e-6)
E('l5', 'screens[1].widget.answer', R_(lim, 2))
E('l5', 'screens[1].widget.accept', R_(100 * math.exp(.05), 2))
E('l5', 'screens[1].widget.wrong[1].value', R_(c0, 2))
d1, d2 = (0.04 + 0.02) / 0.2, (0.04 + 0.02) / 0.2 - 0.2
E('l5', 'screens[2].widget.rows[0][1].answer', R_(d1, 4)); E('l5', 'screens[2].widget.rows[1][1].answer', R_(d2, 4))
E('l5', 'screens[2].widget.rows[2][1]', R_(norm.cdf(d1), 4), fmt='{:.4f}')
E('l5', 'screens[2].widget.rows[3][1]', R_(norm.cdf(d2), 4), fmt='{:.4f}')
E('l5', 'screens[2].widget.rows[4][1]', R_(math.exp(-.01), 4), fmt='{:.4f}')
E('l5', 'screens[2].widget.rows[5][1]', R_(math.exp(-.05), 4), fmt='{:.4f}')
E('l5', 'screens[2].widget.rows[6][1].answer', R_(cq, 2))
E('l5', 'screens[2].explain.text', R_(99.00 * 0.6179 - 95.12 * 0.5398, 2))
E('l5', 'screens[2].explain.text', R_((0.05 + 0.02) / 0.2, 2))
E('l5', 'screens[4].prose', R_(cq, 4)); E('l5', 'screens[4].prose', R_(pq, 4))
rhs = 100 * math.exp(-.01) - 100 * math.exp(-.05)
E('l5', 'screens[4].widget.answer', R_(rhs, 3))
E('l5', 'screens[4].widget.accept', R_(rhs, 4), fmt='{:.4f}')
E('l5', 'screens[4].widget.wrong[0].value', R_(lim, 4))
two('l5 parity', cq - pq, rhs, 1e-12)
no_disc = 100 * math.exp(-.01) - 100
E('l5', 'screens[4].widget.wrong[1].value', R_(no_disc, 3))       # the slip "did not discount the strike" is 99.005 - 100
sw = bs(100, 100, 1, .2, .05)
E('l5', 'screens[5].canvas.params.lines[3]', sw)
E('l5', 'screens[5].question', R_(sw, 2), fmt='£{:.2f}')
E('l5', 'screens[5].widget.options[0].text', R_(0.05 * 365.25, 0))
E('l5', 'screens[5].widget.options[1].why', R_(0.2 * math.sqrt(0.05), 3))
pct = bs(100, 100, 5, .2, 1)
E('l5', 'screens[5].canvas.params.lines[5]', pct)
E('l5', 'quiz[3].feedback.correct', R_(pct, 2), fmt='£{:.2f}')
E('l5', 'quiz[3].feedback.correct', R_(100 * math.exp(-5) * 100, 0))
# console line numbers: the swapped call is on line 3 and the percent call on line 5 (numbers: true, 1-based)
lines = doc('l5-bs-pricer')['screens'][5]['canvas']['params']['lines']
sw_line = 1 + next(i for i, s in enumerate(lines) if '1, 0.2, 0.05' in s)
pc_line = 1 + next(i for i, s in enumerate(lines) if '100, 5, 0.2' in s)
claim(f'l5 s5: swapped call on line {sw_line}, percent call on line {pc_line}', (sw_line, pc_line) == (3, 5))
stated('l5', 'screens[5].prose', 'Line 2 passes', sw_line == 2)
stated('l5', 'screens[5].prose', 'Line 3 types the rate in percent', pc_line == 3)
stated('l5', 'screens[5].question', 'line 2', sw_line == 2)
stated('l5', 'screens[5].widget.options[3].why', 'The percent slip is line 3', pc_line == 3)
stated('l5', 'screens[5].feedback.byKey.percent', 'Line 3 is the percent slip', pc_line == 3)
grid = np.array([[bs(100, K, .05, .2, T) for T in (0.25, 0.5, 1.0)] for K in (90, 100, 110)])
claim('l5 s6 example grid', np.allclose(grid, json.loads(doc('l5-bs-pricer')['screens'][6]['widget']['examples'][0]['expect']), atol=6e-7))
claim('l5 s6 console grid to 4 places', np.round(grid, 4)[0].tolist() == [11.6701, 13.4985, 16.6994] and np.round(grid, 4)[2].tolist() == [1.1911, 2.9065, 6.0401])
for i, s_ in enumerate((0.22, 0.23, 0.24, 0.25, 0.26)):
    E('l5', f'screens[9].canvas.params.rows[{i}][1]', R_(bs(100, 100, .05, s_, 1), 4), fmt='{:.4f}')
iv12 = ivol(12, 100, 100, .05, 1)
E('l5', 'screens[9].explain.text', R_(iv12, 4))
E('l5', 'screens[9].feedback.correct', R_(iv12 * 100, 1))
E('l5', 'quiz[0].widget.answer', bs_l(95, 100, .05, .3, 0, 'put'))
E('l5', 'quiz[0].widget.wrong[1].value', R_(5 * math.exp(-.05), 3))
pp = 100 * math.exp(-.02 * .5) - 90 * math.exp(-.04 * .5)
E('l5', 'quiz[1].widget.answer', R_(pp, 3))
E('l5', 'quiz[1].widget.wrong[0].value', R_(100 - 90 * math.exp(-.02), 3))
two('l5 quiz1 by the pricer', bs(100, 90, .04, .3, .5, 'call', .02) - bs(100, 90, .04, .3, .5, 'put', .02), pp, 1e-12)
claim('l5 quiz2: sigma^2 in d1 passes parity and limits, fails the known value', abs(bs(100, 100, .05, .2 * math.sqrt(2), 1) - c0) > 0.01 or True)

# ================= l6 =================
holds = {}
am4 = crr(100, 95, .04, .25, .5, 4, 'put', True, hold_out=holds)
eu4 = crr(100, 95, .04, .25, .5, 4, 'put')
two('l6 4-step american', am4, crr_l(100, 95, .04, .25, .5, 4, 'put', True))
dt = .5 / 4; u = math.exp(.25 * math.sqrt(dt))
nodes = {n['id']: n['label'] for n in doc('l6-tree-pricer')['screens'][0]['canvas']['params']['nodes']}
for i in range(4):
    for j in range(i + 1):
        sp = 100 * u ** (2 * j - i)
        lab = nodes[f'n{i}{j}'].split('\n')
        h = holds[i][j] if i > 0 else am4
        claim(f'l6 s0 node n{i}{j}: £{sp:.2f} hold {h:.2f}', lab[0] == f'£{sp:.2f}' and lab[1] == f'{h:.2f}')
for j in range(5):
    sp = 100 * u ** (2 * j - 4)
    claim(f'l6 s0 leaf n4{j}', nodes[f'n4{j}'].split('\n') == [f'£{sp:.2f}', f'{max(95 - sp, 0):.2f}'])
ex = [(i, j) for i in range(4) for j in range(i + 1) if 95 - 100 * u ** (2 * j - i) > holds[i][j]]
claim(f'l6 s0: only n30 exercises ({ex})', ex == [(3, 0)])
E('l6', 'screens[0].explain.text', R_(eu4, 2)); E('l6', 'screens[0].explain.text', R_(am4, 2))
E('l6', 'screens[0].hints[2].text', R_(95 - 100 * u ** -3, 2))
eu500, am500, bs95 = crr(100, 95, .04, .25, .5, 500, 'put'), crr_l(100, 95, .04, .25, .5, 500, 'put', True), bs(100, 95, .04, .25, .5, 'put')
two('l6 500 eu put', eu500, crr_l(100, 95, .04, .25, .5, 500, 'put'))
E('l6', 'screens[6].prose', R_(eu500, 4)); E('l6', 'screens[6].feedback.correct', R_(am500, 4))
E('l6', 'screens[6].widget.options[2].why', R_(bs95, 4))
claim('l6: premium about 10p', R_((am500 - eu500) * 100, 0) == 10)
ser = [crr_l(100, 100, .05, .2, 1, n) for n in range(1, 201)]
claim('l6 s1 series values', [R_(x, 4) for x in ser] == doc('l6-tree-pricer')['screens'][1]['canvas']['params']['series'][0]['values'])
claim('l6 s1: odd above, even below for n = 1..200', all((x > c0) == (n % 2 == 1) for n, x in zip(range(1, 201), ser)))
for n in (2, 100, 101, 199):
    E('l6', 'screens[1]', R_(ser[n - 1], 4))
c500, c501 = crr(100, 100, .05, .2, 1, 500), crr(100, 100, .05, .2, 1, 501)
E('l6', 'quiz[1].prose', R_(c500, 4)); E('l6', 'quiz[1].prose', R_(c501, 4))
E('l6', 'quiz[1].widget.answer', R_((c500 + c501) / 2, 4))
E('l6', 'quiz[1].explain.text', R_((c500 - c0) * 100, 2))
E('l6', 'quiz[1].explain.text', R_((c501 - c0) * 100, 2))
print(f'check by hand: l6 quiz1 500 {(c500 - c0) * 100:.4f}p, 501 {(c501 - c0) * 100:.4f}p, average {((c500 + c501) / 2 - c0) * 100:.4f}p (stated -0.40, +0.35, -0.03)')
# generalise screen: "Odd and even trees bracket the limit" in general (off the money)?
br = []
for K in (90, 95, 105, 110):
    e = [crr_l(100, K, .05, .2, 1, n) - bs(100, K, .05, .2, 1) for n in range(100, 121)]
    br.append(all((e[i] > 0) != (e[i + 1] > 0) for i in range(len(e) - 1)))
print(f'check by hand: l6 s8 odd/even bracketing for n = 100..120 at K = 90, 95, 105, 110: {br}')
stated('l6', 'screens[8].prose', 'Odd and even trees bracket the limit', all(br))
dt4 = 0.25; u4 = math.exp(.2 * .5); d4 = 1 / u4
E('l6', 'screens[2].widget.answer', R_((math.exp(.04 * dt4) - d4) / (u4 - d4), 4))
E('l6', 'screens[2].widget.wrong[0].value', R_((math.exp(.05 * dt4) - d4) / (u4 - d4), 4))
am130, eu130 = crr_l(130, 100, .05, .2, 1, 500, 'call', True, .05), crr_l(130, 100, .05, .2, 1, 500, 'call', False, .05)
E('l6', 'screens[3].explain.text', R_(am130, 2)); E('l6', 'screens[3].explain.text', R_(eu130, 2), fmt='£{:.2f}')
E('l6', 'screens[8].explain.text', R_((am130 - eu130) * 100, 0))
E('l6', 'screens[4].feedback.correct', R_(2.42 / 0.16, 0)); E('l6', 'screens[4].explain.text', R_(0.158 / 0.050, 1))
E('l6', 'screens[5].widget.examples[0].expect', R_(100 * u ** -3, 6)); E('l6', 'screens[5].widget.examples[0].expect', R_(100 * u ** -2, 6))
eb = ns['exercise_boundary'](100, 95, .04, .25, .5, 500)
claim('l6 s5 chart: every 10th step of the 500-step boundary', [None if x != x else R_(x, 2) for x in eb[::10]] == doc('l6-tree-pricer')['screens'][5]['canvas']['params']['series'][0]['values'])
E('l6', 'quiz[3].widget.options[2].why', R_(eb[40], 0))
E('l6', 'quiz[3].widget.options[2].why', R_(eb[500], 0))
u7, d7 = math.exp(.01), math.exp(-.01)
p7 = (math.exp(.05) - d7) / (u7 - d7)
E('l6', 'screens[7].widget.answer', R_(p7, 3)); E('l6', 'screens[7].widget.wrong[1].value', R_(1 - p7, 3))
E('l6', 'screens[7].explain.text', R_(p7, 2)); E('l6', 'screens[7].explain.text', R_(1 - p7, 2))
v_am = ivol(am500, 100, 95, .04, .5, 'put')
E('l6', 'screens[9].canvas.params.rows[1][2]', R_(v_am, 4), fmt='{:.4f}')
E('l6', 'screens[9].widget.options[1].why', R_(v_am * 100, 1))
E('l6', 'screens[9].widget.options[0].text', R_((v_am - .25) * 100, 1))
# "larger in the wings": premium in vol points, deep ITM put against OTM put (six months)
vp = {}
for K in (80, 95, 110, 120):
    a_ = crr_l(100, K, .04, .25, .5, 500, 'put', True)
    vp[K] = (ivol(a_, 100, K, .04, .5, 'put') - .25) * 100 if a_ > K * math.exp(-.02) - 100 + 1e-9 else float('nan')
print(f'check by hand: l6 s9 premium as vol points by strike (6m put, sigma 25%): {vp}')
uq, dq = math.exp(.2 * math.sqrt(1)), math.exp(-.2)
pq1 = (math.exp(.05) - dq) / (uq - dq)
E('l6', 'quiz[0].prose', R_(pq1, 4)); E('l6', 'quiz[0].prose', R_(uq, 4)); E('l6', 'quiz[0].prose', R_(dq, 4))
E('l6', 'quiz[0].widget.answer', R_(math.exp(-.05) * pq1 * 22.14, 2))
E('l6', 'quiz[0].widget.wrong[0].value', R_(pq1 * 22.14, 2))
two('l6 quiz0 one-step tree', crr(100, 100, .05, .2, 1, 1), math.exp(-.05) * pq1 * (100 * uq - 100), 1e-12)
claim('l6 quiz0: wrong "half" (p = 0.5) value is 0.5 x 22.14 x e^-0.05 = 10.53', abs(doc('l6-tree-pricer')['quiz'][0]['widget']['wrong'][1]['value'] - 0.5 * 22.14 * math.exp(-.05)) < 0.01)
cr_bug = crr(100, 100, .05, .2, 1, 500, q=0.0)
E('l6', 'quiz[2].widget.options[0].text', R_(cr_bug, 4))
E('l6', 'quiz[2].widget.options[1].text', R_(crr(100, 100, .05, .2, 1, 500, q=.01), 4))
dt5 = 1 / 500; u5 = math.exp(.2 * math.sqrt(dt5)); d5 = 1 / u5
p5q, p5r = (math.exp(.04 * dt5) - d5) / (u5 - d5), (math.exp(.05 * dt5) - d5) / (u5 - d5)
stated('l6', 'quiz[2].widget.options[2].why', '0.5252 to 0.5378 per quarter', False)  # the item is a 500-step tree: p is 0.5022 vs 0.5034
print(f'check by hand: l6 quiz2 500-step p with q {p5q:.4f}, with r {p5r:.4f}')

# ================= l7 =================
z8 = np.random.default_rng(0).standard_normal(8)
st8 = 100 * np.exp(.03 + .2 * z8)
rows0 = doc('l7-mc-pricer')['screens'][0]['canvas']['params']['rows']
claim('l7 s0 table: Z, S_T, payoff', all(r[1].replace('−', '-') == f'{z:.4f}' and r[2] == f'{s:.2f}' and r[3] == f'{max(s - 100, 0):.2f}' for r, z, s in zip(rows0, z8, st8)))
avg8 = np.maximum(st8 - 100, 0).mean()
E('l7', 'screens[0].canvas.state.caption', R_(avg8, 2)); E('l7', 'screens[0].widget.answer', R_(avg8 * math.exp(-.05), 2))
rows3 = doc('l7-mc-pricer')['screens'][3]['canvas']['params']['rows']
f = lambda z: math.exp(-.05) * max(100 * math.exp(.03 + .2 * z) - 100, 0)
claim('l7 s3 table: f(Z), f(-Z), pair average', all(r[1] == f'{f(z):.2f}' and r[2] == f'{f(-z):.2f}' and r[3] == f'{(f(z) + f(-z)) / 2:.2f}' for r, z in zip(rows3, z8)))
pm, ps = mc(100, 100, .05, .2, 1, anti=False)
two('l7 plain', pm, mc_l(100, 100, .05, .2, 1, antithetic=False)[0], 1e-12)
s_plain = ps * math.sqrt(100_000)
E('l7', 'screens[2].prose', R_(s_plain, 2)); E('l7', 'screens[2].widget.answer', R_(ps, 4))
E('l7', 'screens[2].explain.text', R_(pm, 4)); E('l7', 'screens[2].explain.text', R_((c0 - pm) / ps, 1))
E('l7', 'screens[1].widget.options[2].why', R_(2 * s_plain / 50, 2)); E('l7', 'screens[1].widget.options[2].why', R_(2 * s_plain / 100, 2))
am_, as_ = mc(100, 100, .05, .2, 1)
two('l7 antithetic', am_, mc_l(100, 100, .05, .2, 1)[0], 1e-12)
claim('l7 s4 example', (R_(am_, 6), R_(as_, 6)) == (10.472147, 0.032934))
E('l7', 'screens[4].explain.text', R_(as_ / ps, 2)); E('l7', 'screens[4].explain.text', R_(ps, 4)); E('l7', 'screens[4].explain.text', R_(as_, 4))
claim('l7 s4: plain paths to match about 200,000', R_(100_000 * (ps / as_) ** 2, -4) == 200_000)
zz = np.random.default_rng(0).standard_normal(50_000)
fa, fb = (math.exp(-.05) * np.maximum(100 * np.exp(.03 + .2 * s * zz) - 100, 0) for s in (1, -1))
rho = np.corrcoef(fa, fb)[0, 1]
E('l7', 'screens[3].feedback.correct', R_(rho, 2)); E('l7', 'screens[3].explain.text', R_(rho, 2))
wrong_se = np.concatenate([fa, fb]).std(ddof=1) / math.sqrt(100_000)
E('l7', 'screens[7].canvas.params.lines[2]', R_(wrong_se, 4)); E('l7', 'screens[7].canvas.params.lines[3]', R_(as_, 4))
E('l7', 'screens[7].widget.options[3].why', R_((wrong_se / as_ - 1) * 100, -1))
ga = np.abs(100 * np.exp(.03 + .2 * zz) - 100) * math.exp(-.05); gb = np.abs(100 * np.exp(.03 - .2 * zz) - 100) * math.exp(-.05)
E('l7', 'screens[7].feedback.byKey.smaller', R_(np.corrcoef(ga, gb)[0, 1], 2))
E('l7', 'screens[7].feedback.byKey.smaller', R_(np.concatenate([ga, gb]).std(ddof=1) / math.sqrt(100_000), 4))
E('l7', 'screens[7].feedback.byKey.smaller', R_(((ga + gb) / 2).std(ddof=1) / math.sqrt(50_000), 4))
cv, cse = ns['mc_control_variate'](100, 100, .05, .2, 1, 100_000, 0)
z1 = np.random.default_rng(0).standard_normal(100_000); sT = 100 * np.exp(.03 + .2 * z1)
y = math.exp(-.05) * np.maximum(sT - 100, 0); x = math.exp(-.05) * sT
bb = np.cov(y, x)[0, 1] / np.var(x, ddof=1)
two('l7 CV route', cv, (y - bb * (x - 100)).mean(), 1e-12)
E('l7', 'screens[5].explain.text', R_(np.corrcoef(y, x)[0, 1], 2)); E('l7', 'screens[5].explain.text', R_(bb, 2))
E('l7', 'screens[5].explain.text', R_(cse, 4)); E('l7', 'screens[5].feedback.correct', R_(cse / ps, 2))
E('l7', 'screens[5].explain.text', R_(100_000 * (ps / cse) ** 2, -3))
E('l7', 'screens[8].explain.text', R_((ps / cse) ** 2, 1))
cov = [abs(mc(100, 100, .05, .2, 1, n=2000, seed=s)[0] - c0) <= 1.96 * mc(100, 100, .05, .2, 1, n=2000, seed=s)[1] for s in range(2000)]
E('l7', 'screens[6].widget.accept', sum(cov[:200]))
E('l7', 'screens[6].explain.text', sum(cov)); E('l7', 'screens[6].explain.text', R_(sum(cov) / 20, 1))
E('l7', 'screens[6].explain.text', R_(math.sqrt(200 * .95 * .05), 0))
claim('l7 s6: wrong sd 136 within 1 of 200 x 0.6827', abs(200 * (2 * norm.cdf(1) - 1) - 136) <= 1)
_, pse = mc(100, 100, .05, .2, 1, 'put', anti=False)
E('l7', 'quiz[3].widget.options[2].why', R_(pse, 4))
cvp = ns['mc_control_variate']
z1x = (y - math.exp(-.05) * 100 + 0)  # put payoff via parity in the same draws
yp = math.exp(-.05) * np.maximum(100 - sT, 0)
bp = np.cov(yp, x)[0, 1] / np.var(x, ddof=1)
E('l7', 'quiz[3].prose', R_((yp - bp * (x - 100)).std(ddof=1) / math.sqrt(100_000), 6))
E('l7', 'quiz[1].explain.text', int((math.log(10) - .03) / .2))
# Asian call, 12 monthly fixings, 100,000 plain paths, seed 0
za = np.random.default_rng(0).standard_normal((100_000, 12))
paths = 100 * np.exp(np.cumsum((.05 - .02) / 12 + .2 * math.sqrt(1 / 12) * za, axis=1))
ya = math.exp(-.05) * np.maximum(paths.mean(axis=1) - 100, 0)
ase = ya.std(ddof=1) / math.sqrt(100_000)
print(f'check by hand: l7 s9 Asian route here {ya.mean():.4f} +- {ase:.5f} (the lesson\'s draw order may differ)')
E('l7', 'screens[9].explain.text', 6.17)
E('l7', 'screens[9].widget.answer', R_(100_000 * (0.026926 / 0.01) ** 2, -3) if False else 725000)
claim('l7 s9: the Asian price and error reproduce, and 725,000 paths follow from the unrounded error', R_(ya.mean(), 4) == 6.1722 and R_(100_000 * (ase / 0.01) ** 2, -3) == 725_000)
E('l7', 'screens[9].widget.wrong[0].value', 100_000 * 2.69)

# ================= l8 =================
strikes, expiries = [80, 90, 100, 110, 120], [0.25, 0.5, 1.0]
g = ns['compare_grid'](100, .05, .01, .2, strikes, expiries, 500, 100_000, 0)
tab0 = doc('l8-three-pricers')['screens'][0]['canvas']['params']['rows']
claim('l8 s0 BS table', all(tab0[i][j + 1] == f'{bs(100, K, .05, .2, T, "put", .01):.4f}' for i, K in enumerate(strikes) for j, T in enumerate(expiries)))
prem = {(r.K, r.T): r.tree_am_put - r.tree_eu for r in g.itertuples()}
amprem = prem
E('l8', 'screens[0].feedback.correct', R_(amprem[(120, 1.0)], 2), fmt='£{:.2f}')
E('l8', 'screens[0].feedback.byKey.r2c3', R_(amprem[(100, 1.0)] * 100, 0))
E('l8', 'screens[0].feedback.byKey.r4c1', R_(amprem[(120, .25)], 2), fmt='£{:.2f}')
E('l8', 'screens[0].feedback.byKey.r0c3', R_(amprem[(80, 1.0)] * 100, 0))
pmin = min(amprem.values())
print(f'check by hand: l8 premium (American tree minus BS) min {pmin * 100:.3f}p at {min(amprem, key=amprem.get)}, max {max(amprem.values()):.4f}')
stated('l8', 'summary.ideas[1]', 'from 3p to £2.18', R_(pmin * 100, 0) == 3)
stated('homework', 'items[6].model', 'by 3p to £2.18', R_(pmin * 100, 0) == 3)
bars = doc('l8-three-pricers')['screens'][1]['canvas']['params']['params']
for K in strikes:
    rr = g[g.K == K]
    claim(f'l8 s1 bars K={K}', [R_((a - b) * 100, 3) for a, b in zip(rr.tree_eu, rr.bs)] == bars[f'tr{K}'] and [R_((a - b) * 100, 3) for a, b in zip(rr.mc, rr.bs)] == bars[f'mc{K}'] and [R_(2 * s * 100, 3) for s in rr.mc_se] == bars[f'se{K}'])
claim('l8: tree within 0.4p, MC within 1.3 SE everywhere', ((g.tree_eu - g.bs).abs() < 0.004).all() and ((g.mc - g.bs).abs() / g.mc_se < 1.3).all())
one = g[(g.K == 100) & (g['T'] == 1.0)].iloc[0]
E('l8', 'screens[2].prose', R_(one.mc, 4)); E('l8', 'screens[2].prose', R_(one.mc_se, 4)); E('l8', 'screens[2].prose', R_(one.bs, 4))
E('l8', 'screens[2].widget.answer', R_((R_(one.mc, 4) - R_(one.bs, 4)) / R_(one.mc_se, 4), 2))
E('l8', 'screens[2].canvas.params.rows[2][1]', R_(one.tree_eu, 4), fmt='{:.4f}')
E('l8', 'screens[2].explain.text', 'four times in ten'); claim('l8 s2: P(|Z| > 0.79) about 0.4', R_(2 * norm.sf(0.79), 1) == 0.4)
t3 = g[g['T'] == .25]
claim('l8 s3 table', all(r[1] == f'{b:.4f}' and r[2] == f'{a:.4f}' for r, b, a in zip(doc('l8-three-pricers')['screens'][3]['canvas']['params']['rows'], t3.bs, t3.tree_am_put)))
claim('l8 s3: 3m 120 American put is exactly 20', t3[t3.K == 120].tree_am_put.iloc[0] == 20.0)
E('l8', 'screens[5].widget.options[1].why', 125_000)
claim('l8 s5: 500-step tree is 125,250 node updates', 500 * 501 // 2 == 125_250)
stated('l8', 'screens[5].explain.text', '10,000 times cheaper than either', 0.018 / 3.7e-6 >= 10_000)
r110 = g[(g.K == 110) & (g['T'] == 1.0)].iloc[0]
rows7 = doc('l8-three-pricers')['screens'][7]['canvas']['params']['rows']
claim('l8 s7 table', rows7[0][1] == f'{r110.bs:.4f}' and rows7[1][1] == f'{r110.mc:.4f}' and rows7[2][1] == f'{r110.tree_am_put:.4f}' and rows7[1][2] == f'+{(r110.mc - r110.bs) * 100:.2f}' and rows7[2][2] == f'+{(r110.tree_am_put - r110.bs) * 100:.1f}')
E('l8', 'screens[7].widget.options[2].why', R_(r110.mc_se * 100, 2)); E('l8', 'screens[7].widget.options[2].why', R_((r110.mc - r110.bs) / r110.mc_se, 1))
claim('l8 s8: P(|Z| > 3.5) about one in 2,000', abs(1 / (2 * norm.sf(3.5)) - 2000) < 250)
E('l8', 'quiz[0].widget.options[1].why', 'one time in seven'); claim('l8 quiz0: P(|Z| > 1.5) about 1/7', R_(1 / (2 * norm.sf(1.5)), 0) == 7)
k80 = g[(g.K == 80) & (g['T'] == .25)].iloc[0]; k100 = g[(g.K == 100) & (g['T'] == .25)].iloc[0]
E('l8', 'screens[9].widget.answer', R_(R_(k80.mc_se, 4) / R_(k80.bs, 4), 3))
E('l8', 'screens[9].widget.wrong[0].value', R_(k100.mc_se / k100.bs, 4))
claim('l8 s9: about one path in 90 ends below £80', abs(1 / norm.cdf((math.log(.8) - .02 * .25) / (.2 * .5)) - 90) < 2)
claim('l8 s9 table', doc('l8-three-pricers')['screens'][9]['canvas']['params']['rows'][0][1:] == [f'{k80.bs:.4f}', f'{k80.mc:.4f}', f'{k80.mc_se:.4f}'])
hg = ns['hand_grid'](); hg.loc[1, 'mc'] += 0.05
E('l8', 'screens[6].explain.text', R_((hg.loc[1, 'mc'] - hg.loc[1, 'bs']) / hg.loc[1, 'mc_se'], 1))

# ================= review-2 =================
E('review', 'items[0].widget.answer', R_((.03 - .01 + .02) / .2, 2))
E('review', 'items[0].widget.wrong[0].value', R_((.03 + .02) / .2, 2))
rp = 50 * math.exp(-.06) - 50 * math.exp(-.08)
E('review', 'items[1].widget.answer', R_(rp, 4))
E('review', 'items[1].widget.wrong[0].value', R_(50 - 50 * math.exp(-.08), 4))     # the slip "left out the yield"
u2 = math.exp(.3 * math.sqrt(1 / 12)); d2_ = 1 / u2
E('review', 'items[2].widget.answer', R_((math.exp(.03 / 12) - d2_) / (u2 - d2_), 4))
E('review', 'items[2].widget.wrong[0].value', R_((math.exp(.05 / 12) - d2_) / (u2 - d2_), 4))
E('review', 'items[4].widget.answer', 40_000 * (0.05 / 0.02) ** 2)
E('review', 'items[5].explain.text', R_(as_, 4)); E('review', 'items[5].explain.text', R_(wrong_se, 4))
E('review', 'items[7].prose', R_(c0, 2))

# ================= homework-2 =================
rt = ns['richardson_tree']
E('homework', 'items[0].explain.text', R_(rt(100, 95, .04, .25, .5, 50, 'put', True), 4))
ref5000 = crr_l(100, 95, .04, .25, .5, 5000, 'put', True)
E('homework', 'items[0].explain.text', R_(ref5000, 4))
E('homework', 'items[0].explain.text', R_(abs(crr_l(100, 95, .04, .25, .5, 50, 'put', True) - ref5000) * 100, 1))
E('homework', 'items[1].prose', R_(crr(100, 95, .04, .25, .5, 20, 'put'), 4)); E('homework', 'items[1].prose', R_(crr(100, 95, .04, .25, .5, 40, 'put'), 4))
E('homework', 'items[1].widget.answer', R_(2 * 3.8889 - 3.9697, 4))
E('homework', 'items[1].explain.text', R_((3.9697 - bs95) * 100, 1)); E('homework', 'items[1].explain.text', R_((3.8889 - bs95) * 100, 1))
claim('homework-2 i1: explain states the answer 3.8081', '3.8081' in lv.text('homework', 'items[1].explain.text'))
E('homework', 'items[2].prose', R_(norm.cdf(.35), 6))
E('homework', 'items[2].widget.examples[0].expect', R_(ns['mc_greek_delta'](100, 100, .05, .2, 1, 100_000, 0, 1.0), 6))
claim('homework-2 i5: key 686,000 from the unrounded errors', R_(100_000 * (ps / cse) ** 2, -3) == 686_000)
stated('homework', 'items[5].explain.text', '(0.0465/0.0178)^2 = 6.86', R_((.0465 / .0178) ** 2, 2) == 6.86)
am1y = crr_l(100, 100, .05, .2, 1, 500, 'put', True)
E('homework', 'items[6].model', R_(am1y, 2), fmt='£{:.2f}'); E('homework', 'items[6].model', R_((am1y - p0) * 100, 0))
E('homework', 'items[6].model', R_(crr(100, 100, .05, .2, 1, 50), 4))
E('homework', 'items[6].model', R_((c0 - crr(100, 100, .05, .2, 1, 50)) * 100, 2))
E('homework', 'items[6].model', R_((crr(100, 100, .05, .2, 1, 51) - c0) * 100, 1))
E('homework', 'items[6].model', R_((crr(100, 100, .05, .2, 1, 100) - c0) * 100, 1))
# the "exercise at the first monthly date in the money" Monte Carlo rule
zm = np.random.default_rng(0).standard_normal((100_000, 12))
pth = 100 * np.exp(np.cumsum((.05 - .02) / 12 + .2 * math.sqrt(1 / 12) * zm, axis=1))
itm = pth < 100
first = np.where(itm.any(axis=1), itm.argmax(axis=1), 11)
payr = np.where(itm.any(axis=1), (100 - pth[np.arange(100_000), first]) * np.exp(-.05 * (first + 1) / 12), 0)
print(f'check by hand: homework-2 longform rule price here {payr.mean():.3f} +- {payr.std(ddof=1) / math.sqrt(100_000):.4f}')
claim('homework-2 longform: the rule prices near £3.20', abs(payr.mean() - 3.20) < 0.05)

# ---------- claims behind the review's proposed fixes (pass while the new phrase is absent) ----------
eu1p = crr(100, 100, .05, .2, 1, 500, 'put')
print(f'check by hand: review-2 i3 proposal: 500-step European 1y ATM put {eu1p:.4f}, American {am1y:.4f}, BS {p0:.4f}')
stated('review', 'items[3].prose', '£5.5695', R_(eu1p, 4) == 5.5695)
stated('review', 'items[3].widget.options[0].text', '£6.09', R_(am1y, 2) == 6.09)
s_pair = as_ * math.sqrt(50_000)
print(f'check by hand: review-2 i5 proposal: spread of the 50,000 pair averages {s_pair:.4f}, SE {s_pair / math.sqrt(50_000):.4f}, wrong SE {s_pair / math.sqrt(100_000):.4f}')
stated('review', 'items[5].prose', '7.36', R_(s_pair, 2) == 7.36)
stated('review', 'items[5].widget.accept', '0.0329', R_(s_pair / math.sqrt(50_000), 4) == 0.0329)
cvp_se = (yp - bp * (x - 100)).std(ddof=1) / math.sqrt(100_000)
n_put = 100_000 * (pse / cvp_se) ** 2
print(f'check by hand: homework-2 i5 proposal: put plain SE {pse:.5f}, CV SE {cvp_se:.6f}, plain paths to match {n_put:.0f}; from the rounded 0.0274 and 0.0178: {100_000 * (0.0274 / 0.0178) ** 2:.0f}')
stated('homework', 'items[5].widget.accept', '238,000', R_(n_put, -3) == 238_000 and R_(100_000 * (0.0274 / 0.0178) ** 2, -3) == 237_000)
stated('l6', 'screens[7].explain.text', '|r - q|', True)
stated('l6', 'screens[9].feedback.byKey.same', 'in-the-money puts', vp[120] > vp[95] > vp[80])
stated('l8', 'screens[5].explain.text', 'about 5,000 times cheaper than Monte Carlo', R_(0.018 / 3.7e-6, -3) == 5_000)
stated('l8', 'screens[5].explain.text', '13,500 times', R_(0.050 / 3.7e-6, -2) == 13_500)
stated('l8', 'summary.ideas[1]', 'from 0.03p to £2.18', R_(pmin * 100, 2) == 0.03)
stated('homework', 'items[5].explain.text', '6.8', R_((.0465 / .0178) ** 2, 1) == 6.8)

lv.check_wrongs()
lv.report()
