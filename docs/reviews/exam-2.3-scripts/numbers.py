"""Second reader's number script for app/content/exams/topic-2.3.json (review-exam-2.3.md).

Recomputes every graded key and every wrong[] value, the numbers in prose, feedback, consoles and explanations,
and runs the six code items: the solution passes every example and hidden test, the starter fails at least one,
and planted bugs are caught. Routes: closed forms written out again (Black-Scholes, CRR trees, Spearman, Newton);
a seeded Monte Carlo of my own for the pricer grid; a look-ahead cut test on each pandas line of e-peek-lines; and
an independent second implementation of each code item (pure-Python loops or an explicit-node tree).
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Needs numpy, pandas and scipy. Run: python3 docs/reviews/exam-2.3-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (NumPy imports it).
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import datetime as dt  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import integrate, optimize, stats  # noqa: E402

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.3.json')
COURSES = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}
IT = {it['id']: it for it in doc['items']}


def P(iid):
    return f'items[{idx[iid]}]'


def node(path):
    return _walk(doc, path)[0]


def near(a, b, t):
    return abs(a - b) <= t


def key(iid, value, path='widget', t=None):
    """The graded answer equals the recomputed value, within a tenth of its tolerance (or t)."""
    w = node(f'{P(iid)}.{path}')
    tol = w.get('tol', {}).get('abs', 0)
    t = t if t is not None else max(tol / 10, 1e-9)
    ok = near(w['answer'], value, t)
    ex._rec(ok, f'{iid} {path} answer {w["answer"]!r} = {value:.6g}', '' if ok else 'recomputed value differs')


def inband(iid, typed, path='widget', label='typed answer'):
    w = node(f'{P(iid)}.{path}')
    ok = abs(typed - w['answer']) <= w['tol']['abs'] + 1e-9
    ex._rec(ok, f'{iid} {label} {typed!r} graded right', '' if ok else 'outside the answer tolerance')


def wrong(iid, wid, value, typed=None, path='widget', t=None):
    w = node(f'{P(iid)}.{path}')
    ws = [x for x in w['wrong'] if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]
    tt = t if t is not None else max(v.get('tol', {}).get('abs', 1e-9), 1e-9)
    ok = near(v['value'], value, tt)
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {value:.6g}', '' if ok else 'recomputed slip differs')
    if typed is not None:
        ok2 = abs(typed - v['value']) <= v.get('tol', {}).get('abs', 1e-9) + 1e-9
        ex._rec(ok2, f'{iid} wrong "{wid}" catches a typed {typed!r}', '' if ok2 else 'typed slip misses its own band')


def correct_ids(iid):
    return sorted(o['id'] for o in IT[iid]['widget']['options'] if o.get('correct'))


def text(iid, path):
    return ex.text('exam', f'{P(iid)}.{path}')


N = stats.norm.cdf
npdf = stats.norm.pdf


def bs(S, K, r, sig, T, kind='call', q=0.0):
    d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    if kind == 'call':
        return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1)


def greeks_call(S, K, r, sig, T, q=0.0):
    d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    delta = math.exp(-q * T) * N(d1)
    gamma = math.exp(-q * T) * npdf(d1) / (S * sig * math.sqrt(T))
    vega = S * math.exp(-q * T) * npdf(d1) * math.sqrt(T)
    theta = (-S * math.exp(-q * T) * npdf(d1) * sig / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * N(d2)
             + q * S * math.exp(-q * T) * N(d1))
    return delta, gamma, vega, theta


# ---------------------------------------------------------------- metadata, shape, coverage (AUTHORING section 5)
hours = 400  # docs/curriculum.md row 2.3
exam_minutes = 45 if hours <= 60 else 60 if hours <= 150 else 90  # app/js/screens/learn.js examMinutes
ex.claim(doc['minutes'] == exam_minutes == 90 and doc['pass'] == 0.7, f'minutes {doc["minutes"]} = examMinutes(400 h) and pass 0.7')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 6, 3: 15, 4: 6, 5: 3}, f'ramp {ramp}: 20%, 50%, 20%, 10% exactly')
union = {}
for c in ('backtest', 'alpha', 'opt-dash'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the three course.json maps')
cnt = {s: sum(1 for it in doc['items'] if s in it['skills']) for s in union}
ex.claim(min(cnt.values()) >= 2, f'every skill tested by at least two items {cnt}')
ex.claim(not any('pace' in it for it in doc['items']), 'no item carries pace (finding: every topic exam from 2.5 on paces each item)')
rub = sum(r['points'] for r in IT['e-results-note']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')

# ---------------------------------------------------------------- e-visible-rows
rows = IT['e-visible-rows']['canvas']['params']['rows']
seen = [f'r{i}' for i, r in enumerate(rows) if int(r[0]) <= 4]
ex.claim(seen == IT['e-visible-rows']['widget']['answer'], f'e-visible-rows answer = bars 1 to 4 {seen}')
wv = {w['id']: w['set'] for w in IT['e-visible-rows']['widget']['wrong']}
ex.claim(wv['all'] == [f'r{i}' for i in range(6)] and wv['next'] == [f'r{i}' for i in range(5)], 'e-visible-rows wrong sets: all six; bars 1 to 5')

# ---------------------------------------------------------------- e-universe-date
D = dt.date(2021, 6, 15)
uk_hols = {dt.date(2021, 5, 31)}  # spring bank holiday
wk = [dt.date(2021, 5, 4) + dt.timedelta(d) for d in range((D - dt.date(2021, 5, 4)).days + 1)]
weekdays = sum(1 for d in wk if d.weekday() < 5)
trading = sum(1 for d in wk if d.weekday() < 5 and d not in uk_hols)
ex.claim(weekdays == 31 and trading == 30, f'e-universe-date GGG: {weekdays} weekdays, {trading} UK trading days from 4 May to 15 June (prose: about 30)')
uni = {'AAA': (dt.date(2019, 1, 2), None, 22.4), 'BBB': (dt.date(2019, 1, 2), dt.date(2021, 3, 3), None),
       'CCC': (dt.date(2019, 1, 2), None, 4.6), 'DDD': (dt.date(2021, 8, 20), None, None),
       'EEE': (dt.date(2019, 1, 2), dt.date(2021, 11, 12), 7.8), 'FFF': (dt.date(2019, 2, 1), None, 5.0),
       'GGG': (dt.date(2021, 5, 4), None, 11.0)}
inn = []
for i, (s, (a, b, v)) in enumerate(uni.items()):
    listed = a <= D and (b is None or b >= D)
    days = int(np.busday_count(a, D + dt.timedelta(1)))
    if listed and days >= 60 and v is not None and v >= 5.0:
        inn.append(f'r{i}')
ex.claim(inn == IT['e-universe-date']['widget']['answer'], f'e-universe-date answer AAA, EEE, FFF = {inn}')
# A 60-day mean volume cannot exist for a share with about 30 days of history (prose: "A dash means no figure exists").
ex.claim_text('exam', f'{P("e-universe-date")}.canvas.params.rows[6][3]', '£11.0m', False,
              'e-universe-date GGG shows a 60-day mean volume, £11.0m, after about 30 trading days')

# ---------------------------------------------------------------- e-clean-tap
q2 = IT['e-clean-tap']['canvas']['params']['rows']
drop = []
for i, (k, b, a, age) in enumerate(q2):
    b, a, age = float(b), float(a), float(age)
    mid = (a + b) / 2
    keep = b > 0 and b <= a and age <= 30 and (a - b) / mid < 0.5
    if not keep:
        drop.append(f'r{i}')
ex.claim(drop == IT['e-clean-tap']['widget']['answer'], f'e-clean-tap answer {drop}')
ex.claim(round(0.30 / 5.95 * 100) == 5 and near(0.08 / 0.08, 1.0, 1e-9) and round(0.04 / 0.12 * 100) == 33, 'e-clean-tap feedback 5%, 1.0 and 33%')

# ---------------------------------------------------------------- e-ticket-cost
comm, half = max(3000 * 0.005, 1.0), 3000 * 42.50 * 2e-4
key('e-ticket-cost', comm + half)
wrong('e-ticket-cost', 'spread-only', half, typed=25.50)
wrong('e-ticket-cost', 'commission-only', comm, typed=15.00)
wrong('e-ticket-cost', 'full-spread', comm + 2 * half, typed=66.00)
ex.expect('exam', f'{P("e-ticket-cost")}.explain.text', 127500)

# ---------------------------------------------------------------- e-mom-window
m = IT['e-mom-window']['canvas']['state']['values']
mv = [m[k] for k in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
key('e-mom-window', sum(mv[:11]))
wrong('e-mom-window', 'all-twelve', sum(mv))
wrong('e-mom-window', 'latest-only', mv[11])
wrong('e-mom-window', 'dropped-oldest', sum(mv[1:]))

# ---------------------------------------------------------------- e-newton-step
p25 = bs(100, 100, 0.05, 0.25, 1)
v25 = greeks_call(100, 100, 0.05, 0.25, 1)[2]
ex.claim(round(p25, 2) == 12.34 and round(v25, 1) == 37.8, f'e-newton-step model price {p25:.4f} and vega {v25:.3f} read 12.34 and 37.8')
s1 = 0.25 + (13.00 - 12.34) / 37.8
key('e-newton-step', s1, t=5e-5)  # stored to the 4 places asked
inband('e-newton-step', 0.2675, label='typed 26.75%')
iv_true = optimize.brentq(lambda s: bs(100, 100, 0.05, s, 1) - 13.0, 0.01, 2)
ex.claim(round(iv_true * 100, 2) == 26.75, f'e-newton-step true implied vol {iv_true:.6f} reads 26.75%')
wrong('e-newton-step', 'minus', 0.25 - 0.66 / 37.8, typed=0.2325)
wrong('e-newton-step', 'no-vega', 0.25 + 0.66, typed=0.91)
wrong('e-newton-step', 'units', (25 + 0.66 / 37.8) / 100, typed=0.2502)

# ---------------------------------------------------------------- e-bar-order
ex.claim(IT['e-bar-order']['widget']['answer'] == ['s1', 's2', 's3', 's4', 's5'] and IT['e-bar-order']['widget']['same'] == [['s2', 's3']],
         'e-bar-order: fill, then mark and hand over (either order), then signal, target, order')

# ---------------------------------------------------------------- e-split-div
key('e-split-div', 2 * (123 + 1.5) / 240 - 1)
inband('e-split-div', 0.0375, label='typed 3.75%')
wrong('e-split-div', 'raw', 123 / 240 - 1, typed=-0.4875)
wrong('e-split-div', 'no-dividend', 2 * 123 / 240 - 1, typed=0.025)
wrong('e-split-div', 'dividend-old', (2 * 123 + 1.5) / 240 - 1, typed=0.03125)

# ---------------------------------------------------------------- e-implied-q
F = 100 + math.exp(0.05) * (9.30 - 6.70)
qv = 0.05 - math.log(F / 100)
ex.claim(round(F, 2) == 102.73, f'e-implied-q forward {F:.4f}')
key('e-implied-q', qv, t=5e-5)  # stored as 2.30%
inband('e-implied-q', 0.0230, label='typed 2.30%')
wrong('e-implied-q', 'no-discount', 0.05 - math.log((100 + 2.60) / 100), typed=0.0243)
# "no-rate" is r = 0 throughout: F = 100 + 2.60 and q = -ln(F/S). With the right forward and r dropped only in the
# second step, a learner types -2.70%, which no wrong[] catches.
wrong('e-implied-q', 'no-rate', -math.log(1.026), typed=-0.0257)
wrong('e-implied-q', 'linear', 0.05 - (F / 100 - 1), typed=0.0227)
ex.claim(round(math.log(1.0273), 4) == 0.0270, f'e-implied-q explain: ln(1.0273) = {math.log(1.0273):.5f} is printed as 0.0270',
         'ln(1.0273) is 0.0269; 0.0270 needs the unrounded 1.02733')
expl = text('e-implied-q', 'explain.text')
outside = re.sub(r'\$[^$]*\$', '', expl)
ex.claim('^{' not in outside, 'e-implied-q explain: no TeX (e^{0.05}) outside $...$', 'raw "e^{0.05}" is shown to the learner as text')

# ---------------------------------------------------------------- e-impact-double
rate1, rate2 = 0.015 * math.sqrt(40000 / 1.6e6), 0.015 * math.sqrt(80000 / 1.6e6)
ex.claim(round(rate1 * 40000 * 60, 2) == 5692.10, f'e-impact-double first order £{rate1 * 2.4e6:.2f}')
key('e-impact-double', rate2 * 80000 * 60)
wrong('e-impact-double', 'linear', 2 * rate1 * 2.4e6, typed=11384.20)
wrong('e-impact-double', 'old-notional', rate2 * 2.4e6, typed=8049.84)
ex.claim(round(rate2 * 100, 3) == 0.335 and round(rate1 * 100, 3) == 0.237 and round(rate2 / rate1 * 2, 2) == 2.83, 'e-impact-double explain 0.335%, 0.237%, 2.83 times')

# ---------------------------------------------------------------- e-ic-tstat
key('e-ic-tstat', 0.036 / (0.081 / math.sqrt(36)), t=0.005)  # stored to 2 places
wrong('e-ic-tstat', 'ir', 0.036 / 0.081, typed=0.444)
wrong('e-ic-tstat', 'annual-ir', 0.036 / 0.081 * math.sqrt(12), typed=1.54)

# ---------------------------------------------------------------- e-three-pricers (BS, CRR 500 with q, my own MC)
S0, r0, q0, sg0, T0 = 100, 0.05, 0.01, 0.20, 0.5


def crr(S, K, r, sig, T, n, american, q=0.0, kind='put'):
    dtt = T / n
    u = math.exp(sig * math.sqrt(dtt))
    d = 1 / u
    p = (math.exp((r - q) * dtt) - d) / (u - d)
    disc = math.exp(-r * dtt)
    j = np.arange(n + 1)
    ST = S * u ** (2 * j - n)
    V = np.maximum(K - ST, 0.0) if kind == 'put' else np.maximum(ST - K, 0.0)
    for i in range(n - 1, -1, -1):
        V = disc * (p * V[1:] + (1 - p) * V[:-1])
        if american:
            Si = S * u ** (2 * np.arange(i + 1) - i)
            V = np.maximum(V, K - Si)
    return float(V[0])


grid = IT['e-three-pricers']['canvas']['params']['rows']
zz = np.random.default_rng(1).standard_normal(50_000)
flags = []
for i, row in enumerate(grid):
    K = float(row[0])
    bsv, eu, mc, se, us = (float(x) for x in row[1:])
    mybs = bs(S0, K, r0, sg0, T0, 'put', q0)
    myeu, myus = crr(S0, K, r0, sg0, T0, 500, False, q0), crr(S0, K, r0, sg0, T0, 500, True, q0)
    drift = (r0 - q0 - sg0 ** 2 / 2) * T0
    pay = [np.maximum(K - S0 * np.exp(drift + s * sg0 * math.sqrt(T0) * zz), 0) for s in (1, -1)]
    pair = math.exp(-r0 * T0) * (pay[0] + pay[1]) / 2
    myse = pair.std(ddof=1) / math.sqrt(len(pair))
    ex.claim(round(mybs, 3) == bsv, f'e-three-pricers K {K:g} BS {mybs:.4f} shown {bsv}')
    ex.claim(abs(myse - se) <= 0.0015, f'e-three-pricers K {K:g} se {myse:.4f} (my 100,000 antithetic paths) shown {se}')
    if f'r{i}c2' not in IT['e-three-pricers']['widget']['answer']:
        ex.claim(abs(myeu - eu) <= 0.0006, f'e-three-pricers K {K:g} European tree {myeu:.4f} shown {eu}')
    if f'r{i}c5' not in IT['e-three-pricers']['widget']['answer']:
        ex.claim(abs(myus - us) <= 0.0006, f'e-three-pricers K {K:g} American tree {myus:.4f} shown {us}')
    if abs(eu - bsv) > 0.01:
        flags.append(f'r{i}c2')
    if abs(mc - bsv) > 3 * se:
        flags.append(f'r{i}c3')
    if us < eu:
        flags.append(f'r{i}c5')
ex.claim(sorted(flags) == sorted(IT['e-three-pricers']['widget']['answer']), f'e-three-pricers the three rules flag {flags}')
z90 = (1.322 - 1.359) / 0.010
z110 = (10.503 - 10.525) / 0.012
ex.claim_text('exam', f'{P("e-three-pricers")}.feedback.byKey.r1c3', 'about 3.5 standard errors', round(abs(z90), 1) == 3.5,
              f'e-three-pricers byKey r1c3 "about 3.5 standard errors": the table gives {abs(z90):.1f}')
ex.claim_text('exam', f'{P("e-three-pricers")}.feedback.byKey.r3c3', '1.9 standard errors', round(abs(z110), 1) == 1.9,
              f'e-three-pricers byKey r3c3 "1.9 standard errors": the table gives {abs(z110):.2f}')
ex.claim(round(20.004 - 18.487, 2) == 1.52 and round(4.621 - 4.521, 2) == 0.10 and round(10.647 - 10.525, 2) == 0.12, 'e-three-pricers feedback 1.52, 0.10, 0.12')

# ---------------------------------------------------------------- e-peek-lines (a cut test on each line)
rng = np.random.default_rng(7)
idx400 = pd.bdate_range('2020-01-01', periods=400)
close0 = pd.Series(100 * np.exp(np.cumsum(0.01 * rng.standard_normal(400))), index=idx400)
close0.iloc[[198, 199]] = np.nan


def L_next(c):
    return c.rolling(20).mean().shift(-1) - c


def L_z(c):
    ret = c.pct_change()
    return (ret - ret.mean()) / ret.std()


LINES = {'next-mean': L_next, 'full-z': L_z, 'bfill': lambda c: c.bfill(), 'ffill': lambda c: c.ffill(),
         'lag': lambda c: np.sign(c.pct_change(5)).shift(1)}
peeks = []
for name, f in LINES.items():
    leak = False
    for cut in (100, 200, 300):
        c2 = close0.copy()
        c2.iloc[cut:] = c2.iloc[cut:] * np.exp(0.02 * rng.standard_normal(400 - cut))
        a, b = f(close0).iloc[:cut].to_numpy(float), f(c2).iloc[:cut].to_numpy(float)
        if not np.allclose(a, b, equal_nan=True):
            leak = True
    if leak:
        peeks.append(name)
ex.claim(sorted(peeks) == correct_ids('e-peek-lines'), f'e-peek-lines the cut test flags {peeks}')

# ---------------------------------------------------------------- e-rank-ic-hand
sig13 = [0.8, -0.3, 1.5, 0.1, -1.2, 0.5]
ret13 = [-1.4, -0.2, 6.0, 2.3, -3.1, 0.9]
rs, rr = stats.rankdata(sig13), stats.rankdata(ret13)
ex.claim(list(rs) == [5, 2, 6, 3, 1, 4] and list(rr) == [2, 3, 6, 5, 1, 4], 'e-rank-ic-hand explain ranks')
ex.claim(sum((rs - rr) ** 2) == 14, 'e-rank-ic-hand sum d^2 = 14')
key('e-rank-ic-hand', stats.spearmanr(sig13, ret13)[0])
wrong('e-rank-ic-hand', 'pearson', np.corrcoef(sig13, ret13)[0, 1], typed=0.763)
wrong('e-rank-ic-hand', 'seven', 1 - 6 * 14 / (7 * 48), typed=0.75)

# ---------------------------------------------------------------- e-drawdown-calmar
eq15 = np.array(IT['e-drawdown-calmar']['canvas']['params']['series'][0]['values'], float)
ex.claim(list(eq15) == [float(x) for x in IT['e-drawdown-calmar']['prose'].split('`')[1].split()], 'e-drawdown-calmar chart = prose list')
dd = eq15 / np.maximum.accumulate(eq15) - 1
mdd = dd.min()
cagr15 = (eq15[-1] / eq15[0]) ** (12 / 12) - 1
rows15 = 'widget.rows'
key('e-drawdown-calmar', -mdd * 100, path=f'{rows15}[0][1]', t=0.005)
key('e-drawdown-calmar', cagr15 * 100, path=f'{rows15}[1][1]', t=0.005)
key('e-drawdown-calmar', cagr15 / -mdd, path=f'{rows15}[2][1]', t=0.005)
glob_rng = (eq15.max() - eq15.min()) / eq15.max()
wrong('e-drawdown-calmar', 'global-range', glob_rng * 100, typed=19.0, path=f'{rows15}[0][1]')
wrong('e-drawdown-calmar', 'global-calmar', cagr15 / glob_rng, typed=0.97, path=f'{rows15}[2][1]')
ex.claim(int(np.argmin(dd)) == 4 and eq15[np.argmax(eq15[:5])] == 109, 'e-drawdown-calmar worst fall 109 to 98')
# Within the paper: e-code-tear-line's example uses the same equity and prints this item's keys.
tl = IT['e-code-tear-line']['widget']['examples'][0]
ex.claim('118.4' not in tl['setup'], 'e-code-tear-line example does not reuse e-drawdown-calmar\'s equity (it prints -0.100917 and 1.823273)',
         'the example shows the drawdown and Calmar keys of e-drawdown-calmar to anyone who opens the code item first')

# ---------------------------------------------------------------- e-rank-weights
sig16 = {'S1': 0.8, 'S2': -0.3, 'S3': 1.4, 'S4': 0.1, 'S5': -1.1, 'S6': None, 'S7': 0.5, 'S8': -0.6}
v16 = {k: v for k, v in sig16.items() if v is not None}
rk = dict(zip(v16, stats.rankdata(list(v16.values()))))
cen = {k: rk[k] - np.mean(list(rk.values())) for k in rk}
gross16 = sum(abs(x) for x in cen.values())
w16 = {k: (cen[k] / gross16 if k in cen else 0.0) for k in sig16}
for i, row in enumerate(IT['e-rank-weights']['widget']['rows']):
    cell = row[2]
    want = w16[row[0]]
    if isinstance(cell, dict):
        ex.claim(near(cell['answer'], want, 1e-4), f'e-rank-weights {row[0]} answer {cell["answer"]} = {want:.4f}')
    else:
        ex.claim(near(float(cell.replace('−', '-')), want, 1e-4), f'e-rank-weights {row[0]} given {cell} = {want:.4f}')
ex.claim(gross16 == 12, 'e-rank-weights centred ranks sum to 12 in absolute value')

# ---------------------------------------------------------------- e-explain-pnl
d17, g17, v17, t17 = greeks_call(100, 100, 0.05, 0.20, 0.5)
ex.claim(round(d17, 4) == 0.5977 and round(g17, 4) == 0.0274 and round(v17 / 100, 4) == 0.2736 and round(t17 / 365, 4) == -0.0222,
         f'e-explain-pnl Greeks of the 6-month 100 call: {d17:.4f}, {g17:.4f}, {v17 / 100:.4f}, {t17 / 365:.4f}')
act = bs(103, 100, 0.05, 0.22, 0.5 - 1 / 365) - bs(100, 100, 0.05, 0.20, 0.5)
ex.claim(round(act, 4) == 2.4155, f'e-explain-pnl full repricing {act:.5f}')
terms = [0.5977 * 3, 0.5 * 0.0274 * 9, 0.2736 * 2, -0.0222]
rows17 = 'widget.rows'
for i, v in enumerate(terms):
    key('e-explain-pnl', v, path=f'{rows17}[{i}][1]', t=5e-5)
key('e-explain-pnl', sum(terms), path=f'{rows17}[4][1]', t=5e-5)
key('e-explain-pnl', 2.4155 - sum(terms), path=f'{rows17}[5][1]', t=5e-5)
wrong('e-explain-pnl', 'no-half', 0.0274 * 9, typed=0.2466, path=f'{rows17}[1][1]')
wrong('e-explain-pnl', 'vega-scale', 0.2736 * 0.02, typed=0.0055, path=f'{rows17}[2][1]')

# ---------------------------------------------------------------- e-cost-drag
cost = 4.5 * 14e-4
r19 = 'widget.rows'
key('e-cost-drag', cost * 100, path=f'{r19}[0][1]', t=1e-6)
key('e-cost-drag', 5.4 - cost * 100, path=f'{r19}[1][1]', t=1e-6)
key('e-cost-drag', (5.4 - cost * 100) / 3.0, path=f'{r19}[2][1]', t=1e-6)
key('e-cost-drag', 0.054 / 4.5 * 1e4, path=f'{r19}[3][1]', t=1e-6)
ex.claim(near(5.4 / 3.0, 1.80, 1e-9), 'e-cost-drag gross Sharpe 1.80')

# ---------------------------------------------------------------- e-too-good, e-flat-vega, e-bump-size: keys and key length
ex.claim(correct_ids('e-too-good') == ['b'], 'e-too-good key: look-ahead check and next-open fills first')
for iid in ('e-too-good', 'e-flat-vega', 'e-bump-size'):
    ops = IT[iid]['widget']['options']
    kl = max(len(o['text']) for o in ops if o.get('correct'))
    dl = max(len(o['text']) for o in ops if not o.get('correct'))
    ex.claim(kl <= 1.5 * dl, f'{iid} key {kl} characters against the longest distractor {dl} (advisory rule 586)', 'the key is the giveaway longest option')

# ---------------------------------------------------------------- e-flat-vega (console)
K23, T23 = 130, 1 / 12
p0 = bs(100, K23, 0.05, 0.20, T23)
vg0 = greeks_call(100, K23, 0.05, 0.20, T23)[2]
s1_23 = 0.20 + (0.03 - p0) / vg0
p1 = bs(100, K23, 0.05, s1_23, T23)
vg1 = greeks_call(100, K23, 0.05, s1_23, T23)[2]
s2_23 = s1_23 + (0.03 - p1) / vg1
ex.claim(f'{p0:.6f}' == '0.000005' and f'{vg0:.5f}' == '0.00059', f'e-flat-vega step 0 price {p0:.3g}, vega {vg0:.3g}')
ex.claim(f'{s1_23:.4f}' == '50.6361' and f'{p1:.6f}' == '100.000000' and f'{vg1:.5f}' == '0.00000', f'e-flat-vega step 1 sigma {s1_23:.4f}, price {p1:.6f}')
ex.claim(f'{s2_23:.3e}' == '-3.033e+12', f'e-flat-vega step 2 sigma {s2_23:.4g}')
d1n = (math.log(100 / K23) + (0.05 + s2_23 ** 2 / 2) * T23) / (s2_23 * math.sqrt(T23))
pn = 100 * N(d1n) - K23 * math.exp(-0.05 * T23) * N(d1n - s2_23 * math.sqrt(T23))
ex.claim(round(pn, 1) == -129.5, f'e-flat-vega step 2 model price {pn:.2f} (the formula at a negative sigma)')
iv23 = optimize.brentq(lambda s: bs(100, K23, 0.05, s, T23) - 0.03, 0.05, 3)
ex.claim(round(iv23, 2) == 0.37, f'e-flat-vega true implied vol {iv23:.4f}: "about 37%"')
ex.claim(round(vg0, 4) == 0.0006 and round((0.03 - p0) / vg0) == 50, 'e-flat-vega key: vega about 0.0006, step about 50')
ex.claim(correct_ids('e-flat-vega') == ['a'], 'e-flat-vega key a')

# ---------------------------------------------------------------- e-reversal-crossover
fd = lambda x: 3.6 - 0.7 * x  # noqa: E731
fw = lambda x: 2.8 - 0.4 * x  # noqa: E731
fm = lambda x: 1.6 - 0.1 * x  # noqa: E731
xs = np.linspace(0, 7, 70001)
best = np.argmax(np.vstack([fd(xs), fw(xs), fm(xs)]), axis=0)
x_first = xs[np.argmax(best == 2)]
tg = IT['e-reversal-crossover']['widget']['points'][0]
ex.claim(near(x_first, 4.0, 1e-3) and near(tg['target'][0], 4.0, 1e-9) and near(tg['target'][1], fm(4.0), 1e-9), f'e-reversal-crossover monthly first best at {x_first:.3f} bp, Sharpe {fm(4):.2f}')
reg = {w['id']: w['region'] for w in IT['e-reversal-crossover']['widget']['wrong']}
xdm, xdw = 2.0 / 0.6, 0.8 / 0.3
ex.claim(reg['daily-cross']['x'][0] <= xdm <= reg['daily-cross']['x'][1] and reg['daily-cross']['y'][0] <= fm(xdm) <= reg['daily-cross']['y'][1],
         f'e-reversal-crossover daily-cross region holds ({xdm:.3f}, {fm(xdm):.3f})')
ex.claim(reg['weekly-cross']['x'][0] <= xdw <= reg['weekly-cross']['x'][1] and reg['weekly-cross']['y'][0] <= fw(xdw) <= reg['weekly-cross']['y'][1],
         f'e-reversal-crossover weekly-cross region holds ({xdw:.3f}, {fw(xdw):.3f})')
ex.claim(reg['daily-cross']['x'][1] < tg['target'][0] - tg['tol'][0], 'e-reversal-crossover answer box clear of the daily-cross region')

# ---------------------------------------------------------------- e-calendar-cells
T25 = [1 / 12, 0.25, 0.5, 1.0]
cal = IT['e-calendar-cells']['canvas']['params']['rows']
bad25, fall25 = [], []
for i, row in enumerate(cal):
    v = [float(x) / 100 for x in row[1:]]
    w = [s * s * t for s, t in zip(v, T25)]
    for j in range(1, 4):
        if w[j] < w[j - 1]:
            bad25.append(f'r{i}c{j + 1}')
        if v[j] < v[j - 1]:
            fall25.append(f'r{i}c{j + 1}')
ex.claim(sorted(bad25) == sorted(IT['e-calendar-cells']['widget']['answer']), f'e-calendar-cells answer {bad25}')
ex.claim(sorted(fall25) == sorted(IT['e-calendar-cells']['widget']['wrong'][0]['set']), f'e-calendar-cells falling-vol set {fall25}')
ex.claim(round((1 - 1 / math.sqrt(3)) * 100) == 42 and round((1 - 1 / math.sqrt(2)) * 100) == 29, 'e-calendar-cells "about 42%" and "29%"')
for path, a, b in [('feedback.byKey.r0c2', 0.0225, 0.0133), ('feedback.byKey.r3c2', 0.0048, 0.0100), ('feedback.byKey.r3c3', 0.0181, 0.0100),
                   ('feedback.byKey.r1c3', 0.0242, 0.0156), ('feedback.byKey.r4c3', 0.0145, 0.0081)]:
    ex.expect('exam', f'{P("e-calendar-cells")}.{path}', a)
ex.claim(round(0.46 ** 2 / 12, 4) == 0.0176 and round(0.35 ** 2 / 12, 4) == 0.0102 and round(0.18 ** 2 / 4, 4) == 0.0081, 'e-calendar-cells explain 0.0176, 0.0102, 0.0081')


# ---------------------------------------------------------------- e-bump-size (console, float64 bumps)
def bs_call_erf(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    Nf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))  # noqa: E731
    return S * Nf(d1) - K * math.exp(-r * T) * Nf(d2)


g26 = greeks_call(50, 55, 0.03, 0.30, 0.25)[1]
ex.claim(f'{g26:.6f}' == '0.046696', f'e-bump-size closed-form gamma {g26:.6f}')
lines26 = IT['e-bump-size']['canvas']['params']['lines'][4:]
errs = {}
for ln in lines26:
    h, shown = (float(x) for x in ln.split())
    V = lambda s: bs_call_erf(s, 55, 0.03, 0.30, 0.25)  # noqa: E731
    gb = (V(50 + h) - 2 * V(50) + V(50 - h)) / h ** 2
    errs[h] = abs(gb - g26)
    if h >= 1e-4:
        ex.claim(f'{gb:.6f}' == f'{shown:.6f}', f'e-bump-size h {h:g} bumped gamma {gb:.6f} shown {shown}')
    else:
        ex.claim(abs(gb - g26) > 1e-3, f'e-bump-size h {h:g} round-off ruins it: mine {gb:.4g}, shown {shown} (exact value depends on the pricer\'s rounding)')
ex.claim(min(errs, key=errs.get) in (1e-3, 1e-2), f'e-bump-size best h {min(errs, key=errs.get):g}: "near 0.001"')
ex.claim(round(g26 * 1e-16 * 1e18) == 5, 'e-bump-size second difference at 1e-8 is about 5e-18')
ex.claim(correct_ids('e-bump-size') == ['a'], 'e-bump-size key a')

# ---------------------------------------------------------------- e-results-note
emax60 = integrate.quad(lambda x: x * 60 * npdf(x) * N(x) ** 59, -10, 10)[0]
ex.claim(round(emax60, 2) == 2.32, f'e-results-note E[max of 60 normals] {emax60:.4f}')
ex.claim(round(0.5 + 0.7 * 2.32, 2) == 2.12 and round((2.4 - 2.124) / 0.7, 1) == 0.4, 'e-results-note 2.12 and 0.4 sd')
pp = optimize.brentq(lambda p: math.sqrt(252) * (2 * p - 1) / math.sqrt(1 - (2 * p - 1) ** 2) - 2.4, 0.5, 0.99)
ex.claim(round(pp, 3) == 0.575, f'e-results-note hit rate {pp:.4f} reads 57.5%')
se1 = math.sqrt((1 + (2.4 / math.sqrt(252)) ** 2 / 2) / 252) * math.sqrt(252)
ex.claim(round(se1, 1) == 1.0, f'e-results-note one-year Sharpe se {se1:.3f}')


# ---------------------------------------------------------------- code items
def same(got, want, cmp, tol):
    if cmp == 'raises':
        return got == ('raises', want)
    if cmp == 'equal':
        return got == want
    if want is None or got is None:
        return got is want
    if isinstance(want, list):
        return isinstance(got, (list, tuple)) and len(got) == len(want) and all(same(g, w, cmp, tol) for g, w in zip(got, want))
    if isinstance(want, bool) or isinstance(got, bool):
        return got == want
    if isinstance(want, (int, float)):
        try:
            g = float(got)
        except (TypeError, ValueError):
            return False
        t = tol or {}
        lim = max(t.get('abs') or 0, abs(want) * (t.get('rel') or 0), 1e-12)
        return abs(g - want) <= lim
    return got == want


def run_case(prelude, code, case):
    ns = {}
    try:
        exec(prelude, ns)
        exec(code, ns)
        if case.get('setup'):
            exec(case['setup'], ns)
    except Exception as e:  # noqa: BLE001
        return False, f'setup {type(e).__name__}: {e}'
    try:
        got = eval(case['call'], ns)
    except Exception as e:  # noqa: BLE001
        got = ('raises', type(e).__name__)
        if case.get('compare') != 'raises':
            return False, f'{type(e).__name__}: {e}'
    want = case['expect']
    if isinstance(want, str) and case.get('compare') != 'raises':
        want = eval(want, {})          # expect is a Python literal held as text, as the engine reads it
    return same(got, want, case.get('compare', 'equal'), case.get('tol')), got


def code_item(iid, mutants=()):
    w = IT[iid]['widget']
    cases = [('example', c) for c in w['examples']] + [('test', c) for c in w['tests']]
    runs = [run_case(w.get('prelude', ''), w['solution'], c) for _, c in cases]
    sol = [r[0] for r in runs]
    ex.claim(all(sol), f'{iid} solution passes {sum(sol)} of {len(sol)} examples and tests',
             '; '.join(f'case {i}: {r[1]!r}'[:160] for i, r in enumerate(runs) if not r[0]))
    st = [run_case(w.get('prelude', ''), w['starter'], c)[0] for k, c in cases if k == 'test']
    ex.claim(not all(st), f'{iid} starter fails {st.count(False)} of {len(st)} hidden tests')
    n_tests = len(w['tests'])
    ex.claim(f'{n_tests} hidden tests' in w['how'], f'{iid} how names {n_tests} hidden tests')
    dup = [i for i, t in enumerate(w['tests']) if any(t['call'] == e['call'] and t.get('setup') == e.get('setup') for e in w['examples'])]
    print(f'   {iid}: hidden tests identical to an example: {dup}')
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i for i, (k, c) in enumerate([x for x in cases if x[0] == 'test']) if not run_case(w.get('prelude', ''), bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')
    return w


# e-code-forward-vols, against a formula written again
w14 = code_item('e-code-forward-vols', [
    ('vol average', 'out.append(math.sqrt((w2 - w1) / (expiries[i + 1] - expiries[i])))', 'out.append((vols[i] + vols[i + 1]) / 2)'),
    ('no division by the gap', 'math.sqrt((w2 - w1) / (expiries[i + 1] - expiries[i]))', 'math.sqrt(w2 - w1)'),
    ('<= for equal variance', 'if w2 < w1:', 'if w2 <= w1:'),
    ('no input checks', 'if len(expiries) != len(vols):', 'if False:'),
])
T14, V14 = [1 / 12, 0.25, 0.5, 1.0], [0.22, 0.21, 0.21, 0.22]
f14 = [math.sqrt((V14[i + 1] ** 2 * T14[i + 1] - V14[i] ** 2 * T14[i]) / (T14[i + 1] - T14[i])) for i in range(3)]
ex.claim([round(x, 6) for x in f14] == eval(w14['examples'][0]['expect']), f'e-code-forward-vols example by hand {[round(x, 6) for x in f14]}')

# e-code-tear-line, against a pure-Python loop
w18 = code_item('e-code-tear-line', [
    ('ddof 0', 'r.std(ddof=1)', 'r.std(ddof=0)'),
    ('CAGR exponent over n', '(periods / (len(eq) - 1))', '(periods / len(eq))'),
    ('global-range drawdown', '(eq / eq.cummax() - 1).min()', '(eq.min() / eq.max() - 1)'),
    ('turnover over n - 1', 'np.abs(np.diff(w, prepend=0.0)).mean()', 'np.abs(np.diff(w)).mean()'),
    ('Calmar 0 with no drawdown', 'if max_dd < 0 else math.inf', 'if max_dd < 0 else 0.0'),
])


def tear_loop(e, w, periods):
    e, w = [float(x) for x in e], [float(x) for x in w]
    r = [e[i] / e[i - 1] - 1 for i in range(1, len(e))]
    if len(r) > 1:
        mu = sum(r) / len(r)
        sd = math.sqrt(sum((x - mu) ** 2 for x in r) / (len(r) - 1))
    else:
        mu, sd = 0.0, 0.0
    sh = 0.0 if sd <= 1e-12 else math.sqrt(periods) * mu / sd
    pk, mdd_ = -1e300, 0.0
    for x in e:
        pk = max(pk, x)
        mdd_ = min(mdd_, x / pk - 1)
    cg = (e[-1] / e[0]) ** (periods / (len(e) - 1)) - 1
    cm = cg / abs(mdd_) if mdd_ < 0 else math.inf
    prev, tot = 0.0, 0.0
    for x in w:
        tot += abs(x - prev)
        prev = x
    return [sh, mdd_, cm, tot / len(w)]


ns18 = {}
exec(w18['prelude'] + w18['solution'], ns18)
rg = np.random.default_rng(3)
mx = 0.0
for _ in range(30):
    n = int(rg.integers(3, 300))
    e = 100 * np.cumprod(1 + rg.normal(0.0005, 0.01, n))
    wts = np.round(rg.uniform(-1, 1, n), 2)
    a = ns18['tear_line'](pd.Series(e), pd.Series(wts), 252)
    b = tear_loop(e, wts, 252)
    mx = max(mx, max(abs(x - y) / max(1, abs(y)) for x, y in zip(a, b) if math.isfinite(y)))
ex.claim(mx < 1e-9, f'e-code-tear-line solution = pure-Python loop on 30 seeded series (max rel diff {mx:.1e})')
ex.claim(tear_loop([100, 104, 109, 103, 98, 101, 107, 112, 108, 115, 119, 121, 118.4], [0, 1, 1, 1, 0, 0, 0.5, 1, 1, 0, -1, -1, 0], 12)[3] == 6 / 13,
         'e-code-tear-line example turnover 6/13')

# e-code-first-leak, against a brute-force scan of every cut
w21 = code_item('e-code-first-leak', [
    ('last row only', 'full = run(bars).iloc[:cut].to_numpy(float)', 'full = run(bars).iloc[cut - 1:cut].to_numpy(float)'),
    ('unsorted cuts', 'for cut in sorted(cuts):', 'for cut in cuts:'),
    ('iloc[:cut+1]', 'noisy = run(noise_after(bars, cut)).iloc[:cut]', 'noisy = run(noise_after(bars, cut)).iloc[:cut + 1]'),
])
ns21 = {}
exec(w21['prelude'], ns21)
b21 = ns21['make_bars'](400)
g21 = b21.copy()
g21.iloc[118:121, g21.columns.get_loc('close')] = np.nan


def leak_start(run, bars):
    full = run(bars).to_numpy(float)
    for cut in range(1, len(bars) + 1):
        noisy = run(ns21['noise_after'](bars, cut)).to_numpy(float)[:cut]
        if not np.allclose(full[:cut], noisy, rtol=0, atol=1e-9, equal_nan=True):
            return cut
    return None


starts = {n: leak_start(ns21[n], bb) for n, bb in [('honest_engine', b21), ('peek_engine', b21), ('scaled_engine', b21),
                                                    ('late_engine', b21), ('bfill_engine', g21), ('ffill_engine', g21)]}
ex.claim(starts == {'honest_engine': None, 'peek_engine': 1, 'scaled_engine': 3, 'late_engine': 301, 'bfill_engine': 119, 'ffill_engine': None},
         f'e-code-first-leak leak starts by brute force {starts}')
noisy121 = ns21['bfill_engine'](ns21['noise_after'](g21, 121)).to_numpy()[:121]
full121 = ns21['bfill_engine'](g21).to_numpy()[:121]
changed = [i for i in range(121) if abs(noisy121[i] - full121[i]) > 1e-9]
ex.claim(changed == [118], f'e-code-first-leak at cut 121 the backfill engine changes rows {changed}; the last row, 120, is unchanged')
eng = [k for k in ns21 if k.endswith('_engine')]
ex.claim_text('exam', f'{P("e-code-first-leak")}.widget.prelude', '# five engines', len(eng) == 5,
              f'e-code-first-leak prelude comment "five engines": it defines {len(eng)}')

# e-code-sector-z, against a nested loop
w22 = code_item('e-code-sector-z', [
    ('whole-universe z', 'mu = block.mean(axis=1)', 'mu = signal.mean(axis=1)'),
    ('ddof 0', 'sd = block.std(axis=1, ddof=1)', 'sd = block.std(axis=1, ddof=0)'),
    ('min_names ignored', 'ok = (n >= min_names) & (sd > 1e-12)', 'ok = sd > 1e-12'),
    ('z over time', 'n = block.notna().sum(axis=1)\n        mu = block.mean(axis=1)\n        sd = block.std(axis=1, ddof=1)\n        z = block.sub(mu, axis=0).div(sd, axis=0)',
     'n = block.notna().sum(axis=1)\n        mu = block.mean(axis=1)\n        sd = block.std(axis=1, ddof=1)\n        z = (block - block.mean()) / block.std()'),
])
ns22 = {}
exec(w22['prelude'] + w22['solution'], ns22)


def sz_loop(sig, sec, min_names=3):
    out = pd.DataFrame(np.nan, index=sig.index, columns=sig.columns)
    for t in sig.index:
        for s in sig.columns:
            if pd.isna(sig.at[t, s]):
                continue
            peers = [sig.at[t, c] for c in sig.columns if sec[c] == sec[s] and not pd.isna(sig.at[t, c])]
            if len(peers) < min_names:
                continue
            mu = sum(peers) / len(peers)
            sd = math.sqrt(sum((x - mu) ** 2 for x in peers) / (len(peers) - 1))
            if sd > 1e-12:
                out.at[t, s] = (sig.at[t, s] - mu) / sd
    return out


ok22 = True
for seed in range(15):
    sg = ns22['mk'](12, 9, 100 + seed, 0.2)
    sc = pd.Series(np.arange(9) % 3, index=sg.columns)
    sg.iloc[3, [0, 3, 6]] = 1.5  # one constant sector on one date
    for mn in (2, 3, 4):
        a = ns22['sector_zscore'](sg, sc, mn).to_numpy()
        b = sz_loop(sg, sc, mn).to_numpy()
        ok22 &= bool(np.allclose(a, b, equal_nan=True))
ex.claim(ok22, 'e-code-sector-z solution = nested loop on 15 seeded frames with NaN and a constant sector')

# e-code-bermudan, against an explicit-node tree
w27 = code_item('e-code-bermudan', [
    ('exercise at every step', 'if i in allowed:', 'if True:'),
    ('step off by one', 'if i in allowed:', 'if i + 1 in allowed:'),
    ('r in p instead of r - q', 'p = (np.exp((r - q) * dt) - d) / (u - d)', 'p = (np.exp(r * dt) - d) / (u - d)'),
    ('exercise value discounted', 'V = np.maximum(V, K - nodes)', 'V = np.maximum(V, disc * (K - nodes))'),
])


def berm_nodes(S, K, r, sig, T, n, steps, q=0.0):
    dtt = T / n
    u = math.exp(sig * math.sqrt(dtt))
    d = 1 / u
    p = (math.exp((r - q) * dtt) - d) / (u - d)
    allowed = set(steps)
    val = {(n, j): max(K - S * u ** j * d ** (n - j), 0.0) for j in range(n + 1)}
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            hold = math.exp(-r * dtt) * (p * val[(i + 1, j + 1)] + (1 - p) * val[(i + 1, j)])
            val[(i, j)] = max(hold, K - S * u ** j * d ** (i - j)) if i in allowed else hold
    return val[(0, 0)]


ns27 = {}
exec(w27['prelude'] + w27['solution'], ns27)
rg = np.random.default_rng(27)
mx27 = 0.0
for _ in range(25):
    n = int(rg.integers(3, 60))
    steps = sorted(set(rg.integers(0, n, int(rg.integers(0, n)))))
    args = (float(rg.uniform(60, 140)), float(rg.uniform(70, 130)), float(rg.uniform(0, 0.08)), float(rg.uniform(0.1, 0.5)), float(rg.uniform(0.1, 2)), n)
    qq = float(rg.uniform(0, 0.04))
    mx27 = max(mx27, abs(ns27['bermudan_put'](*args, steps, q=qq) - berm_nodes(*args, steps, q=qq)))
ex.claim(mx27 < 1e-10, f'e-code-bermudan solution = explicit-node tree on 25 random cases (max diff {mx27:.1e})')
ex.claim(round(crr(100, 95, 0.04, 0.25, 0.5, 500, False), 4) == 3.9057 and round(crr(100, 95, 0.04, 0.25, 0.5, 500, True), 4) == 4.0053,
         'e-code-bermudan course 500-step puts 3.9057 and 4.0053')
ex.claim(abs(bs(100, 95, 0.04, 0.25, 0.5, 'put') - 3.9057) < 2e-3, f'e-code-bermudan European tree near Black-Scholes {bs(100, 95, 0.04, 0.25, 0.5, "put"):.4f}')
ex.claim(round(berm_nodes(100, 100, 0.05, 0.2, 1, 3, [2]), 5) == round(berm_nodes(100, 100, 0.05, 0.2, 1, 3, [0, 1, 2]), 5),
         'e-code-bermudan 3-step tree: exercise at step 2 alone already gives the American price')

# e-code-net-book, against a list-based simulation
w28 = code_item('e-code-net-book', [
    ('no lag', 'weights[p + 1:stop + 1] = w', 'weights[p:stop] = w'),
    ('cost on the rebalance row', 'cost[p + 1] = half_spread_bp / 1e4 * np.abs(w - w_prev).sum()', 'cost[p] = half_spread_bp / 1e4 * np.abs(w - w_prev).sum()'),
    ('one-sided cost', 'np.abs(w - w_prev).sum()', 'np.clip(w - w_prev, 0, None).sum()'),
    ('min_names ignored', 'if valid.sum() >= min_names:', 'if valid.sum() >= 2:'),
    ('warm-up rows kept', 'return out.iloc[reb[0] + 1:] if reb else out.iloc[0:0]', 'return out'),
])
ns28 = {}
exec(w28['prelude'] + w28['solution'], ns28)


def book_loop(sig, ret, hs, every=5, min_names=4):
    n, names = len(sig), list(sig.columns)
    reb = list(range(every - 1, n, every))
    held = [[0.0] * len(names) for _ in range(n)]
    cost = [0.0] * n
    prev = [0.0] * len(names)
    for j, p in enumerate(reb):
        vals = [(c, sig.iat[p, k]) for k, c in enumerate(names) if not pd.isna(sig.iat[p, k])]
        w = [0.0] * len(names)
        if len(vals) >= min_names:
            rk = dict(zip([c for c, _ in vals], stats.rankdata([v for _, v in vals])))
            mean = sum(rk.values()) / len(rk)
            gross = sum(abs(x - mean) for x in rk.values())
            if gross > 0:
                w = [((rk[c] - mean) / gross if c in rk else 0.0) for c in names]
        end = reb[j + 1] if j + 1 < len(reb) else n - 1
        for t in range(p + 1, end + 1):
            held[t] = w
        if p + 1 < n:
            cost[p + 1] = hs / 1e4 * sum(abs(a - b) for a, b in zip(w, prev))
        prev = w
    g = [sum(held[t][k] * (0.0 if pd.isna(ret.iat[t, k]) else ret.iat[t, k]) for k in range(len(names))) for t in range(n)]
    start = reb[0] + 1 if reb else n
    return [[g[t], g[t] - cost[t]] for t in range(start, n)]


sg, rt = ns28['hand']()
h0 = book_loop(sg, rt, 10)
ex.claim(np.allclose(h0, eval(w28['tests'][0]['expect'])), f'e-code-net-book hand case by a list loop {np.round(h0, 6).tolist()[:2]}...')
ex.claim(near(h0[0][0], -0.005, 1e-12) and near(h0[0][1], -0.006, 1e-12), 'e-code-net-book first row -0.005 gross, -0.006 net')
ok28 = True
for seed in range(20):
    sgr = ns28['mk'](30, 7, 300 + seed)
    rtr = ns28['mk'](30, 7, 400 + seed, 0.01)
    sgr[sgr > 1.2] = np.nan
    rtr.iloc[20:, 2] = np.nan
    sgr.iloc[20:, 2] = np.nan
    for ev, mn in ((5, 4), (3, 5), (7, 3)):
        a = ns28['net_book'](sgr, rtr, 7.5, every=ev, min_names=mn).to_numpy()
        b = np.array(book_loop(sgr, rtr, 7.5, ev, mn))
        ok28 &= a.shape == b.shape and bool(np.allclose(a, b))
ex.claim(ok28, 'e-code-net-book solution = list loop on 20 seeded panels with NaN, a death and three spacings')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
