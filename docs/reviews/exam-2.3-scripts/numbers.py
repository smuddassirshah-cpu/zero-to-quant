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
pace = {it['id']: it.get('pace') for it in doc['items']}
ex.claim(all(isinstance(v, (int, float)) and v > 0 for v in pace.values()) and sum(pace.values()) == 90 * 60,
         f'every item carries a positive pace and they sum to {sum(pace.values())} s = 90 minutes (finding 34)')
rub = sum(r['points'] for r in IT['e-results-note']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')

# ---------------------------------------------------------------- e-visible-rows
rows = IT['e-visible-rows']['canvas']['params']['rows']
closes = [float(r[5]) for r in rows]
cur = 3                                   # the engine stands at the close of bar 4 (row 3)
win = list(range(cur - 2, cur + 1))       # a trailing 3-bar window ends at the current bar
ex.claim([f'r{i}' for i in win] == IT['e-visible-rows']['widget']['answer'] == ['r1', 'r2', 'r3'], f'e-visible-rows answer = bars 2 to 4 {win}')
wv = {w['id']: w['set'] for w in IT['e-visible-rows']['widget']['wrong']}
ex.claim(wv == {'lagged': ['r0', 'r1', 'r2'], 'centred': ['r2', 'r3', 'r4'], 'history': ['r0', 'r1', 'r2', 'r3']},
         'e-visible-rows wrong sets: the window one bar late, centred on bar 4, and the whole history')
ex.claim(near(sum(closes[1:4]) / 3, 52.4833, 5e-5) and near(sum(closes[1:4]), 157.45, 1e-9), f'e-visible-rows 3-bar mean {sum(closes[1:4]) / 3:.4f} reads 52.48')
ex.expect('exam', f'{P("e-visible-rows")}.explain.text', 52.48)
ex.claim(IT['e-visible-rows']['explain']['canvas']['highlight']['rows'] == win, 'e-visible-rows explain highlights rows 1 to 3')

# ---------------------------------------------------------------- e-universe-date
D = dt.date(2021, 6, 15)
uk_hols = {dt.date(2021, 5, 31)}  # spring bank holiday
wk = [dt.date(2021, 5, 4) + dt.timedelta(d) for d in range((D - dt.date(2021, 5, 4)).days + 1)]
weekdays = sum(1 for d in wk if d.weekday() < 5)
trading = sum(1 for d in wk if d.weekday() < 5 and d not in uk_hols)
ex.claim(weekdays == 31 and trading == 30, f'e-universe-date GGG: {weekdays} weekdays, {trading} UK trading days from 4 May to 15 June (about 30)')
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'May': 5, 'Aug': 8, 'Nov': 11}


def dd(s):
    d, m, y = s.split()
    return dt.date(int(y), months[m], int(d))


def vol(s):
    return None if s == 'none' else float(s.strip('£m'))


tab = IT['e-universe-date']['canvas']['params']
ex.claim(tab['columns'][3:] == ['Mean to 15 Jun', 'Mean to 31 Dec'], 'e-universe-date two volume columns')
inn, inn_dec = [], []
for i, (s, a, b, v_jun, v_dec) in enumerate(tab['rows']):
    a = dd(a)
    b = None if b == 'trading' else dd(b)
    listed = a <= D and (b is None or b >= D)
    days = int(np.busday_count(a, D + dt.timedelta(1)))
    if listed and days >= 60 and vol(v_jun) is not None and vol(v_jun) >= 5.0:
        inn.append(f'r{i}')
    if vol(v_dec) is not None and vol(v_dec) >= 5.0:
        inn_dec.append(f'r{i}')
    ex.claim('—' not in ''.join(map(str, tab['rows'][i])), f'e-universe-date row {s} has no em-dash cell (finding 33)')
ex.claim(inn == IT['e-universe-date']['widget']['answer'] == ['r0', 'r4', 'r5'], f'e-universe-date answer AAA, EEE, FFF = {inn}')
ex.claim(inn_dec == IT['e-universe-date']['widget']['wrong'][-1]['set'] == ['r0', 'r2', 'r3', 'r6'], f'e-universe-date year-end slip set = shares that pass on the 31 December column {inn_dec}')
ex.claim(tab['rows'][6][3] == 'none', 'e-universe-date GGG has no 15 June figure (about 30 trading days of history)')
ex.claim(set(inn_dec) - set(inn) == {'r2', 'r3', 'r6'} and set(inn) - set(inn_dec) == {'r4', 'r5'}, 'e-universe-date explain: December swaps CCC, DDD and GGG in for EEE and FFF')

# ---------------------------------------------------------------- e-clean-tap
q2 = IT['e-clean-tap']['canvas']['params']['rows']
snap = 14 * 60 + 30
drop, ages = [], []
for i, (k, b, a, qt) in enumerate(q2):
    b, a = float(b), float(a)
    hh, mm = (int(x) for x in qt.split(':'))
    age = snap - (hh * 60 + mm)
    ages.append(age)
    mid = (a + b) / 2
    keep = b > 0 and b <= a and age <= 30 and (a - b) / mid < 0.5
    if not keep:
        drop.append(f'r{i}')
ex.claim(ages == [95, 2, 30, 1, 3, 6, 5], f'e-clean-tap ages from the 14:30 snapshot {ages}')
ex.claim(drop == IT['e-clean-tap']['widget']['answer'] == ['r0', 'r3', 'r4', 'r5'], f'e-clean-tap answer {drop}')
edge = [f'r{i}' for i, age in enumerate(ages) if age >= 30 or float(q2[i][1]) <= 0 or float(q2[i][1]) > float(q2[i][2])
        or (float(q2[i][2]) - float(q2[i][1])) / ((float(q2[i][2]) + float(q2[i][1])) / 2) >= 0.5]
ex.claim(edge == IT['e-clean-tap']['widget']['wrong'][0]['set'], f'e-clean-tap edge slip (age 30 dropped) {edge}')
ex.claim(round(0.30 / 5.95 * 100) == 5 and near(0.08 / 0.08, 1.0, 1e-9) and round(0.04 / 0.12 * 100) == 33, 'e-clean-tap feedback 5%, 1.0 and 33%')
ex.claim(near(0.20 / 2.50, 0.08, 1e-12) and 0.20 / 2.50 < 0.5, 'e-clean-tap the 30-minute £100 quote passes the spread rule (0.20 / 2.50 = 0.08)')

# ---------------------------------------------------------------- e-ticket-cost
child = max(150 * 0.005, 1.0)
comm20, half = 20 * child, 3000 * 42.50 * 2e-4
ex.claim(near(150 * 0.005, 0.75, 1e-12) and child == 1.0 and comm20 == 20.0, 'e-ticket-cost one child 150 x 0.005 = 0.75, minimum 1.00, twenty give 20.00')
key('e-ticket-cost', comm20 + half)
wrong('e-ticket-cost', 'one-order', max(3000 * 0.005, 1.0) + half, typed=40.50)
wrong('e-ticket-cost', 'spread-only', half, typed=25.50)
wrong('e-ticket-cost', 'commission-only', comm20, typed=20.00)
wrong('e-ticket-cost', 'full-spread', comm20 + 2 * half, typed=71.00)
ex.expect('exam', f'{P("e-ticket-cost")}.explain.text', 127500)
ex.expect('exam', f'{P("e-ticket-cost")}.explain.text', 45.5)
ex.claim(near(comm20 + half - (max(3000 * 0.005, 1.0) + half), 5.0, 1e-9), 'e-ticket-cost explain: £5.00 more than one order of 3,000')

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
ex.claim(round(p25, 2) == 12.34 and round(v25 / 100, 3) == 0.378, f'e-newton-step model price {p25:.4f} and vega per point {v25 / 100:.5f} read 12.34 and 0.378')
step = (13.00 - 12.34) / 0.378                      # in volatility points, with the vega as printed
ex.claim(round(step, 2) == 1.75, f'e-newton-step the step is {step:.4f} points (1.75)')
s1 = 0.25 + step / 100
key('e-newton-step', s1, t=5e-5)  # stored to the 4 places asked
inband('e-newton-step', 0.2675, label='typed 26.75%')
iv_true = optimize.brentq(lambda s: bs(100, 100, 0.05, s, 1) - 13.0, 0.01, 2)
ex.claim(round(iv_true * 100, 2) == 26.75, f'e-newton-step true implied vol {iv_true:.6f} reads 26.75%')
wrong('e-newton-step', 'minus', 0.25 - step / 100, typed=0.2325)
wrong('e-newton-step', 'per-unit', 0.25 + step, typed=1.996)
wrong('e-newton-step', 'no-vega', 0.25 + 0.66, typed=0.91)
ex.claim('units' not in IT['e-newton-step']['feedback']['byKey'] and IT['e-newton-step']['widget'].get('over100') is True, 'e-newton-step old units slip removed; over100 set for the 199.6% slip')

# ---------------------------------------------------------------- e-bar-order
wb = IT['e-bar-order']['widget']
ex.claim(wb['answer'] == ['s1', 's2', 's3', 's4', 's5'] and wb['same'] == [['s2', 's3']],
         'e-bar-order: fill, then mark and hand over (either order), then signal, target, order')
ex.claim(wb.get('distractors') == ['d1', 'd2'] and {l['id'] for l in wb['lines']} == {'s1', 's2', 's3', 's4', 's5', 'd1', 'd2'}
         and all(l.get('why') for l in wb['lines'] if l['id'].startswith('d')),
         'e-bar-order: two distractors, same-bar fill and a whole-file signal, each with a why; prose says five of seven')

# ---------------------------------------------------------------- e-split-div
key('e-split-div', 2 * (122 + 1.5) / 240 - 1, t=5e-6)
inband('e-split-div', 0.0292, label='typed 2.92%')
wrong('e-split-div', 'raw', 122 / 240 - 1, typed=-0.4917)
wrong('e-split-div', 'no-dividend', 2 * 122 / 240 - 1, typed=0.0167)
wrong('e-split-div', 'dividend-old', (2 * 122 + 1.5) / 240 - 1, typed=0.0229)
ex.claim(near(2 * (122 + 1.5), 247.0, 1e-9) and round(7 / 240 * 100, 2) == 2.92, 'e-split-div explain: 2 x (122.00 + 1.50) = 247.00 and 7 / 240 = 2.92%')
ex.claim(not (0.0291 <= 0.0167 <= 0.0293 or 0.0291 <= 0.0229 <= 0.0293), 'e-split-div the slips stay clear of the 2.91 to 2.93 accept range')

# ---------------------------------------------------------------- e-implied-q
Cm, Pm, Kq, Tq = 8.50, 2.80, 95.0, 0.5
F = Kq + math.exp(0.05 * Tq) * (Cm - Pm)
qv = 0.05 - math.log(F / 100) / Tq
ex.claim(round(F, 2) == 100.84, f'e-implied-q forward {F:.4f}')
key('e-implied-q', qv, t=5e-6)  # stored as 3.3185%
inband('e-implied-q', 0.0332, label='typed 3.32%')
Fnd = Kq + (Cm - Pm)
wrong('e-implied-q', 'no-T', 0.05 - math.log(F / 100), typed=0.0416)
wrong('e-implied-q', 'no-discount', 0.05 - math.log(Fnd / 100) / Tq, typed=0.0360)
wrong('e-implied-q', 'strike-as-spot', 0.05 - math.log(F / Kq) / Tq, typed=-0.0694)
# the linear slip (F/S - 1 for ln) falls inside the answer band, so it is no longer offered (finding 9)
ex.claim(near(0.05 - (F / 100 - 1) / Tq, qv, 0.0002), 'e-implied-q linear slip lies inside the answer band, so it was dropped')
ex.claim(not {'no-rate', 'linear'} & {w['id'] for w in IT['e-implied-q']['widget']['wrong']}, 'e-implied-q no-rate and linear removed')
ex.claim(round(math.log(1.00844) / Tq, 4) == 0.0168 and round(0.05 - 0.0168, 4) == 0.0332, 'e-implied-q explain 0.0168 and 3.32%')
ex.claim(near(Cm - Pm, 5.70, 1e-9) and near(math.exp(0.025), 1.025315, 1e-6), 'e-implied-q explain 5.70 and e^0.025')
expl = text('e-implied-q', 'explain.text')
outside = re.sub(r'\$[^$]*\$', '', expl)
ex.claim('^{' not in outside, 'e-implied-q explain: no TeX outside $...$', 'raw TeX is shown to the learner as text')

# ---------------------------------------------------------------- e-impact-double
rate1, rate2 = 0.015 * math.sqrt(40000 / 1.6e6), 0.015 * math.sqrt(80000 / 1.6e6)
ex.claim(round(rate1 * 40000 * 60, 2) == 5692.10, f'e-impact-double first order £{rate1 * 2.4e6:.2f}')
key('e-impact-double', rate2 * 80000 * 60)
wrong('e-impact-double', 'linear', 2 * rate1 * 2.4e6, typed=11384.20)
wrong('e-impact-double', 'old-notional', rate2 * 2.4e6, typed=8049.84)
ex.claim(round(rate2 * 100, 3) == 0.335 and round(rate1 * 100, 3) == 0.237 and round(rate2 / rate1 * 2, 2) == 2.83, 'e-impact-double explain 0.335%, 0.237%, 2.83 times')

# ---------------------------------------------------------------- e-ic-tstat
decay = 0.5 ** (1 / 2)                       # one month of a two-month half-life
ic_late = 0.036 * decay
se36 = 0.081 / math.sqrt(36)
ex.claim(round(decay, 3) == 0.707 and round(ic_late, 4) == 0.0255 and near(se36, 0.0135, 1e-12), f'e-ic-tstat decay {decay:.4f}, late IC {ic_late:.5f}, se {se36:.4f}')
key('e-ic-tstat', ic_late / se36, t=0.005)  # stored to 2 places
wrong('e-ic-tstat', 'no-delay', 0.036 / se36, typed=2.67)
wrong('e-ic-tstat', 'halved', 0.036 / 2 / se36, typed=1.33)
wrong('e-ic-tstat', 'ir', ic_late / 0.081, typed=0.314)
ex.claim(1.89 < 2, 'e-ic-tstat explain: 1.89 is below 2')

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
    if us < eu or us < max(K - S0, 0):
        flags.append(f'r{i}c5')
ex.claim(sorted(flags) == sorted(IT['e-three-pricers']['widget']['answer']), f'e-three-pricers the three rules flag {flags}')
z90 = (1.322 - 1.359) / 0.010
z110 = (10.503 - 10.525) / 0.012
ex.claim(round(abs(z90), 1) == 3.7, f'e-three-pricers byKey r1c3 "3.7 standard errors": the table gives {abs(z90):.2f}')
ex.claim(round(abs(z110), 1) == 1.8, f'e-three-pricers byKey r3c3 "1.8 standard errors": the table gives {abs(z110):.2f}')
ex.expect('exam', f'{P("e-three-pricers")}.feedback.byKey.r1c3', 3.7)
ex.expect('exam', f'{P("e-three-pricers")}.feedback.byKey.r3c3', 1.8)
am120 = crr(S0, 120, r0, sg0, T0, 500, True, q0)
eu120 = crr(S0, 120, r0, sg0, T0, 500, False, q0)
ex.claim(near(am120, 20.0042, 5e-4) and near(eu120, 18.487, 5e-4), f'e-three-pricers true 500-step American put at 120 is {am120:.4f} (>= 20), European {eu120:.4f}')
ex.claim(float(grid[4][5]) == 19.95 and 19.95 > eu120 and 19.95 < 120 - S0, 'e-three-pricers planted American 19.950 sits above the European tree and below the £20.00 exercise value')
ex.claim(float(grid[3][5]) > 110 - S0, 'e-three-pricers the 110 American price 11.142 is above its exercise value 10, a premium and not flagged')
ex.claim(sorted(IT['e-three-pricers']['widget']['wrong'][0]['set']) == ['r3c5'], 'e-three-pricers premium slip is the 110 premium alone')
ex.claim(round(20.00 - 19.95, 2) == 0.05, 'e-three-pricers r4c5 feedback £19.95 against £20.00')

# ---------------------------------------------------------------- e-peek-lines (a cut test on each line)
rng = np.random.default_rng(7)
idx400 = pd.bdate_range('2020-01-01', periods=400)
close0 = pd.Series(100 * np.exp(np.cumsum(0.01 * rng.standard_normal(400))), index=idx400)
close0.iloc[[198, 199]] = np.nan


LINES = {'month': lambda c: c.resample('ME').last().pct_change().reindex(c.index, method='bfill'),
         'interp': lambda c: c.interpolate(),
         'rank': lambda c: c.pct_change().rank(pct=True),
         'ffill': lambda c: c.ffill(),
         'ewm': lambda c: c.pct_change().ewm(span=20).std(),
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
ex.claim(sorted(peeks) == correct_ids('e-peek-lines') == ['interp', 'month', 'rank'], f'e-peek-lines the cut test flags {peeks}')
ex.claim({o['id'] for o in IT['e-peek-lines']['widget']['options']} == set(LINES), 'e-peek-lines options = the six tested lines')

# ---------------------------------------------------------------- e-rank-ic-hand
tab13 = IT['e-rank-ic-hand']['canvas']['params']['rows']
ex.claim(tab13[6][1] == 'none' and not any('—' in str(c) for r in tab13 for c in r), 'e-rank-ic-hand S7 reads "none", no em-dash (finding 33)')
sig13 = [float(r[1].replace('−', '-')) for r in tab13[:6]]
ret13 = [float(r[2].replace('−', '-')) for r in tab13[:6]]
rs, rr = stats.rankdata(sig13), stats.rankdata(ret13)
ex.claim(list(rs) == [4.5, 2, 6, 3, 1, 4.5] and list(rr) == [2, 3, 6, 5, 1, 4], f'e-rank-ic-hand explain ranks {list(rs)} {list(rr)} (S1 and S6 tie at 4.5)')
cp = float(((rs - 3.5) * (rr - 3.5)).sum())
ex.claim(near(cp, 11.5, 1e-12) and near(((rs - 3.5) ** 2).sum(), 17, 1e-12) and near(((rr - 3.5) ** 2).sum(), 17.5, 1e-12), 'e-rank-ic-hand explain cross products 11.5, squares 17 and 17.5')
key('e-rank-ic-hand', stats.spearmanr(sig13, ret13)[0], t=5e-4)
key('e-rank-ic-hand', cp / math.sqrt(17 * 17.5), t=5e-4)
d2s = float(((rs - rr) ** 2).sum())
wrong('e-rank-ic-hand', 'formula', 1 - 6 * d2s / (6 * 35), typed=0.671)
wrong('e-rank-ic-hand', 'pearson', np.corrcoef(sig13, ret13)[0, 1], typed=0.746)
ex.claim(near(d2s, 11.5, 1e-12), 'e-rank-ic-hand sum d^2 = 11.5 with the tie')

# ---------------------------------------------------------------- e-drawdown-calmar
eq15 = np.array(IT['e-drawdown-calmar']['canvas']['params']['series'][0]['values'], float)
ex.claim(list(eq15) == [float(x) for x in IT['e-drawdown-calmar']['prose'].split('`')[1].split()], 'e-drawdown-calmar chart = prose list')
dd = eq15 / np.maximum.accumulate(eq15) - 1
mdd = dd.min()
cagr15 = (eq15[-1] / eq15[0]) ** (12 / 12) - 1
rows15 = 'widget.rows'
below = (eq15 < np.maximum.accumulate(eq15)).astype(int)
spell = best_run = 0
for b_ in below:
    spell = spell + 1 if b_ else 0
    best_run = max(best_run, spell)
ex.claim([r[0] for r in IT['e-drawdown-calmar']['widget']['rows']][2].startswith('Longest spell'), 'e-drawdown-calmar row 2 is the spell')
key('e-drawdown-calmar', -mdd * 100, path=f'{rows15}[0][1]', t=0.005)
key('e-drawdown-calmar', cagr15 * 100, path=f'{rows15}[1][1]', t=0.005)
key('e-drawdown-calmar', best_run, path=f'{rows15}[2][1]', t=1e-9)
key('e-drawdown-calmar', cagr15 / -mdd, path=f'{rows15}[3][1]', t=0.005)
wrong('e-drawdown-calmar', 'with-recovery', best_run + 1, typed=5, path=f'{rows15}[2][1]', t=1e-9)
glob_rng = (eq15.max() - eq15.min()) / eq15.max()
wrong('e-drawdown-calmar', 'global-range', glob_rng * 100, typed=19.0, path=f'{rows15}[0][1]')
wrong('e-drawdown-calmar', 'global-calmar', cagr15 / glob_rng, typed=0.97, path=f'{rows15}[3][1]')
ex.claim(int(np.argmin(dd)) == 4 and eq15[np.argmax(eq15[:5])] == 109, 'e-drawdown-calmar worst fall 109 to 98')
ex.claim([int(i) for i in np.flatnonzero(below)][:4] == [3, 4, 5, 6] and list(eq15[3:7]) == [103, 98, 101, 107], 'e-drawdown-calmar the spell is months 3 to 6: 103, 98, 101 and 107')
ex.expect('exam', f'{P("e-drawdown-calmar")}.feedback.byKey.with-recovery', 107)
# Within the paper: e-code-tear-line's example no longer uses this item's equity or prints its keys (finding 16a).
tl = IT['e-code-tear-line']['widget']
ex.claim('118.4' not in tl['examples'][0]['setup'] and '1.823273' not in tl['examples'][0]['expect'] and '-0.100917' not in tl['examples'][0]['expect'],
         "e-code-tear-line example does not reuse e-drawdown-calmar's equity or print its keys")
ex.claim(not any('118.4' in t.get('setup', '') for t in tl['tests']), 'e-code-tear-line hidden tests do not reuse e-drawdown-calmar\'s equity')

# ---------------------------------------------------------------- e-rank-weights
sig16 = {r[0]: (None if r[1] == 'none' else float(r[1].replace('−', '-'))) for r in IT['e-rank-weights']['widget']['rows']}
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
ex.claim(sig16['S4'] == sig16['S7'] == 0.5 and rk['S4'] == rk['S7'] == 4.5, 'e-rank-weights S4 and S7 tie at 0.5 and share rank 4.5')
ex.claim(sorted(cen.values()) == [-3, -2, -1, 0.5, 0.5, 2, 3], f'e-rank-weights centred ranks {sorted(cen.values())}')
ord_rk = {'S4': 4, 'S7': 5}
ex.claim(near((ord_rk['S4'] - 4) / 12, 0.0, 1e-12) and near((ord_rk['S7'] - 4) / 12, 0.0833, 5e-5), 'e-rank-weights tie broken by order gives S4 0 and S7 0.0833')
ex.claim(IT['e-rank-weights']['widget']['rows'][3][2]['wrong'][0] == {'id': 'tie-order', 'value': 0, 'tol': {'abs': 0.003}}, 'e-rank-weights S4 tie-order slip is 0')

# ---------------------------------------------------------------- e-explain-pnl
S17, K17, r17, sg17, T17 = 100, 100, 0.05, 0.20, 0.5
d1_17 = (math.log(S17 / K17) + (r17 + sg17 ** 2 / 2) * T17) / (sg17 * math.sqrt(T17))
d2_17 = d1_17 - sg17 * math.sqrt(T17)
dl17 = N(d1_17) - 1
gm17 = npdf(d1_17) / (S17 * sg17 * math.sqrt(T17))
vg17 = S17 * npdf(d1_17) * math.sqrt(T17)
th17 = -S17 * npdf(d1_17) * sg17 / (2 * math.sqrt(T17)) + r17 * K17 * math.exp(-r17 * T17) * N(-d2_17)
ex.claim(round(dl17, 4) == -0.4023 and round(gm17, 4) == 0.0274 and round(vg17, 2) == 27.36 and round(th17, 2) == -3.24,
         f'e-explain-pnl Greeks of the 6-month 100 put: {dl17:.4f}, {gm17:.4f}, {vg17:.3f} per 1.00, {th17:.4f} a year')
ex.claim(near(dl17 + 1, greeks_call(100, 100, 0.05, 0.20, 0.5)[0], 1e-12), 'e-explain-pnl put delta = call delta - 1 (parity)')
act = bs(97, 100, 0.05, 0.22, 0.5 - 1 / 365, 'put') - bs(100, 100, 0.05, 0.20, 0.5, 'put')
ex.claim(round(act, 4) == 1.8706, f'e-explain-pnl full repricing of the put {act:.5f}')
terms = [-0.4023 * -3, 0.5 * 0.0274 * 9, 27.36 * 0.02, -3.24 / 365]
rows17 = 'widget.rows'
for i, v in enumerate(terms):
    key('e-explain-pnl', v, path=f'{rows17}[{i}][1]', t=5e-5)
key('e-explain-pnl', sum(terms), path=f'{rows17}[4][1]', t=5e-5)
key('e-explain-pnl', 1.8706 - sum(terms), path=f'{rows17}[5][1]', t=5e-5)
wrong('e-explain-pnl', 'delta-sign', -terms[0], typed=-1.2069, path=f'{rows17}[0][1]')
wrong('e-explain-pnl', 'no-half', 0.0274 * 9, typed=0.2466, path=f'{rows17}[1][1]')
wrong('e-explain-pnl', 'vega-units', 27.36 * 2, typed=54.72, path=f'{rows17}[2][1]')
wrong('e-explain-pnl', 'theta-year', -3.24, typed=-3.24, path=f'{rows17}[3][1]')

# ---------------------------------------------------------------- e-cost-drag
r19 = 'widget.rows'
per_reb = 2 * (0.5 * 0.30) * 2            # longs and shorts, each side 0.50; replacing 30% sells 0.15 and buys 0.15 on each
traded = per_reb * 12
ex.claim(near(per_reb, 0.6, 1e-12) and near(traded, 7.2, 1e-12), f'e-cost-drag £ traded {per_reb:.2f} a month, {traded:.1f} a year')
cost = traded * 14e-4
key('e-cost-drag', traded, path=f'{r19}[0][1]', t=1e-9)
key('e-cost-drag', cost * 100, path=f'{r19}[1][1]', t=1e-6)
key('e-cost-drag', (5.4 - cost * 100) / 3.0, path=f'{r19}[2][1]', t=0.005)   # stored to 2 places
key('e-cost-drag', 0.054 / traded * 1e4, path=f'{r19}[3][1]', t=1e-6)
wrong('e-cost-drag', 'one-side', traded / 2, typed=3.6, path=f'{r19}[0][1]')
ex.claim(near(5.4 / 3.0, 1.80, 1e-9) and round(5.4 - cost * 100, 2) == 4.39 and round(cost * 100, 2) == 1.01, 'e-cost-drag gross Sharpe 1.80, cost 1.01%, net return 4.39%')
ex.claim(round(100.8) == 101 and near(7.2 * 14, 100.8, 1e-9), 'e-cost-drag byKey r1c1 100.8 bp')

# ---------------------------------------------------------------- e-too-good
ex.claim(correct_ids('e-too-good') == ['b'], 'e-too-good key b: fix the cost sign')
for iid in ('e-too-good',):
    ops = IT[iid]['widget']['options']
    kl = max(len(o['text']) for o in ops if o.get('correct'))
    dl = max(len(o['text']) for o in ops if not o.get('correct'))
    ex.claim(kl <= 1.5 * dl, f'{iid} key {kl} characters against the longest distractor {dl} (advisory rule 586)', 'the key is the giveaway longest option')
lines20 = IT['e-too-good']['canvas']['params']['lines']
cash = 100000.0
cost_bp = 2.5
for ln in lines20[6:]:
    parts = ln.replace(',', '').split()
    shares, fill, flow, cst, after = int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
    ex.claim(near(abs(shares) * fill, abs(flow), 1e-9) and near(abs(flow) * cost_bp / 1e4, cst, 5e-3), f'e-too-good day {parts[0]}: £{abs(flow):,.2f} traded, cost {cst} = 2.5 bp')
    cash_bug = cash + flow + cst                                   # the engine adds the cost
    ex.claim(near(cash_bug, after, 5e-3), f'e-too-good day {parts[0]}: the log adds the cost, cash {cash_bug:,.2f} = {after:,.2f}')
    if parts[0] == '1':
        ex.claim(near(cash + flow - cst, 79995.00, 5e-3), 'e-too-good day 1 should end at £79,995.00')
    cash = after
drag = 0.97 * 252 * cost_bp / 1e4
ex.claim(round(drag * 100, 1) == 6.1 and round(drag / 0.15, 2) == 0.41, f'e-too-good drag {drag:.4f} a year, {drag / 0.15:.3f} of Sharpe')
ex.claim(near(2.61 + round(drag / 0.15, 2), 3.02, 1e-9) and round(2.61 - drag / 0.15, 2) == 2.20 and 2.20 > 2, 'e-too-good net 3.02 = gross 2.61 + 0.41; fixed it is 2.20, above 2')
ex.claim(IT['e-too-good']['canvas']['state']['shade']['bad'] == ['l7', 'l8'], 'e-too-good shades the two trade lines')

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
lo, hi = 1e-4, 5.0
lo = 0.20 if p0 < 0.03 else lo                         # step 0 priced too cheap, so the low end moves to 0.2
newton_out = not (lo <= s1_23 <= hi)
mid = (lo + hi) / 2
key('e-flat-vega', mid, t=1e-9)
inband('e-flat-vega', 2.6, label='typed 2.6')
wrong('e-flat-vega', 'newton', s1_23, typed=50.6361)
wrong('e-flat-vega', 'no-update', (1e-4 + hi) / 2, typed=2.50005)
p26 = bs(100, K23, 0.05, mid, T23)
ex.claim(newton_out and round(p26, 2) == 20.70 and p26 > 0.03, f'e-flat-vega Newton leaves [0.2, 5], the midpoint {mid} prices £{p26:.3f}, too dear, so it becomes the top')
ex.claim(IT['e-flat-vega']['widget']['kind'] == 'numeric' and 'options' not in IT['e-flat-vega']['widget'], 'e-flat-vega is a numeric (key-length cue gone)')

# ---------------------------------------------------------------- e-reversal-crossover
vol_bk, turn = 0.01, (70, 40, 10)
gross = (3.6, 2.8, 1.6)
slope = [t * 1e-4 / vol_bk for t in turn]           # Sharpe lost per bp of half spread
ex.claim([round(s, 6) for s in slope] == [0.7, 0.4, 0.1], f'e-reversal-crossover Sharpe lost per bp {slope}')
xs = np.linspace(0, 7, 70001)
net = np.vstack([g - s * xs for g, s in zip(gross, slope)])
x_first = xs[np.argmax(np.argmax(net, axis=0) == 2)]
key('e-reversal-crossover', x_first, t=1e-3)
x_dm = (gross[0] - gross[2]) / (slope[0] - slope[2])
x_dw = (gross[0] - gross[1]) / (slope[0] - slope[1])
wrong('e-reversal-crossover', 'daily-cross', x_dm, typed=3.333)
wrong('e-reversal-crossover', 'weekly-cross', x_dw, typed=2.667)
ex.claim(near(x_first, 4.0, 1e-3) and near(1.6 - 0.1 * 4, 2.8 - 0.4 * 4, 1e-12), 'e-reversal-crossover weekly and monthly meet at 4 bp, Sharpe 1.2')
ex.claim('canvas' not in IT['e-reversal-crossover'] and IT['e-reversal-crossover']['widget']['kind'] == 'numeric', 'e-reversal-crossover is a numeric with no plane')

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
V1 = lambda s: bs_call_erf(s, 55, 0.03, 0.30, 0.25)  # noqa: E731
call50 = V1(50)
trunc1 = abs((V1(51) - 2 * V1(50) + V1(49)) - g26)
ex.claim(round(call50, 2) == 1.35 and round(trunc1 * 1e5, 1) == 6.4, f'e-bump-size call £{call50:.4f}; h = 1 truncation error {trunc1:.3e} reads 6.4e-5')
epsV = 1.1e-16 * call50
ex.claim(round(epsV * 1e16, 1) == 1.5, f'e-bump-size eps V = {epsV:.3e} reads 1.5e-16')
h_star = (1.5e-16 / 6.4e-5) ** 0.25
key('e-bump-size', h_star, t=1e-4)
inband('e-bump-size', 0.0012, label='typed 0.0012')
wrong('e-bump-size', 'square-root', (1.5e-16 / 6.4e-5) ** 0.5, typed=1.5e-06)
ex.claim(round(1.5e-16 / 6.4e-5 * 1e12, 1) == 2.3, 'e-bump-size explain h^4 = 2.3e-12')
ex.claim(near(6.4e-5 * h_star ** 2, 1.5e-16 / h_star ** 2, 1e-18), 'e-bump-size at h* the two errors are equal')
ex.claim(IT['e-bump-size']['widget']['kind'] == 'numeric' and 'options' not in IT['e-bump-size']['widget'], 'e-bump-size is a numeric (key-length cue gone)')

# ---------------------------------------------------------------- e-results-note
emax60 = integrate.quad(lambda x: x * 60 * npdf(x) * N(x) ** 59, -10, 10)[0]
ex.claim(round(emax60, 2) == 2.32, f'e-results-note E[max of 60 standard normals] {emax60:.4f}')
ex.claim(round(0.5 + 0.7 * 2.32, 2) == 2.12 and round((2.4 - (0.5 + 0.7 * emax60)) / 0.7, 1) == 0.4, 'e-results-note 2.12 and 0.4 of the sd')
# Basis for finding 30: if no setting is better than the others, the 60 Sharpes are exchangeable draws around their own mean
# (here 0.5, sd 0.7), so the best of 60 is mean + sd x E[max of 60 standard normals]. Simulated directly:
rg30 = np.random.default_rng(30)
sim = rg30.normal(0.5, 0.7, (200_000, 60)).max(axis=1)
ex.claim(abs(sim.mean() - 2.1235) < 0.01, f'e-results-note simulated mean of the best of 60 equal settings {sim.mean():.4f} reads 2.12')
p_big = 1 - N((2.4 - 0.5) / 0.7) ** 60
ex.claim(abs((sim >= 2.4).mean() - p_big) < 0.005 and round(p_big, 2) == 0.18, f'e-results-note chance of a best of 60 at or above 2.4: formula {p_big:.3f}, simulation {(sim >= 2.4).mean():.3f}')
# With literally no skill the settings would centre on 0, not 0.5, and the best of 60 would be near 0.7 x 2.32 = 1.62.
ex.claim(round(0.7 * emax60, 2) == 1.62, 'e-results-note a true zero-mean set would give a best near 1.62 (why "no skill at all" was the wrong phrase)')
mdl = IT['e-results-note']['model']
ex.claim('no skill' not in mdl.lower() and 'no-skill' not in mdl.lower() and 'no skill' not in IT['e-results-note']['rubric'][2]['text'].lower(),
         'e-results-note model and rubric no longer say "no skill"')
ex.claim('equal settings' in mdl and 'If no setting were better than the others' in mdl, 'e-results-note model item 3 and (b) use the equal-settings wording')
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
    ex.claim(not dup, f'{iid} no hidden test repeats an example (finding 35)', f'tests {dup} repeat an example')
    if any(c.get('compare') == 'isclose' for c in w['tests']) and 'compared within' in w['how']:
        ex.claim('within 2e-6' in w['how'] and all(c['tol']['abs'] == 2e-6 for c in w['tests'] if c.get('compare') == 'isclose'),
                 f'{iid} how states the 2e-6 tolerance the cases use (finding 36)')
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i for i, (k, c) in enumerate([x for x in cases if x[0] == 'test']) if not run_case(w.get('prelude', ''), bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')
    return w


# e-code-forward-vols (term_vols), against the inverse formula written again
w14 = code_item('e-code-forward-vols', [
    ('no interval length', 'w += f * f * (T - prev)', 'w += f * f * T'),
    ('average of vols', 'out.append(math.sqrt(w / T))', 'out.append(sum(fwd_vols[:len(out) + 1]) / (len(out) + 1))'),
    ('no division by T', 'math.sqrt(w / T)', 'math.sqrt(w)'),
    ('negative forward allowed', 'if any(v < 0 for v in fwd_vols):', 'if False:'),
    ('zero expiry allowed', 'any(t <= 0 for t in expiries[:1])', 'any(t < 0 for t in expiries[:1])'),
    ('equal expiries allowed', 'any(b <= a for a, b in zip(expiries, expiries[1:]))', 'any(b < a for a, b in zip(expiries, expiries[1:]))'),
    ('no length check', 'if len(expiries) != len(fwd_vols):', 'if False:'),
])
ns14 = {}
exec(w14['prelude'] + w14['solution'], ns14)


def fwd_from_term(T, v):
    """The inverse: forward vols from spot vols by differencing total variance (the old course function, written again)."""
    w_ = [s * s * t for s, t in zip(v, T)]
    out_, pt, pw = [], 0.0, 0.0
    for t, wi in zip(T, w_):
        out_.append(math.sqrt((wi - pw) / (t - pt)))
        pt, pw = t, wi
    return out_


rg14 = np.random.default_rng(14)
mx14 = 0.0
for _ in range(50):
    n14 = int(rg14.integers(1, 9))
    T14 = np.cumsum(rg14.uniform(0.05, 1.0, n14))
    f14 = rg14.uniform(0.05, 0.9, n14)
    v14 = ns14['term_vols'](list(T14), list(f14))
    mx14 = max(mx14, max(abs(a - b) for a, b in zip(fwd_from_term(T14, v14), f14)))
ex.claim(mx14 < 1e-9, f'e-code-forward-vols term_vols inverts forward-from-term on 50 random curves (max diff {mx14:.1e})')
ex1 = w14['examples'][0]
ex.claim(near(sum((a - b) ** 2 for a, b in zip(fwd_from_term([1 / 12, 0.25, 0.5, 1.0], [0.22, 0.21, 0.21, 0.22])[1:], [0.204817, 0.21, 0.229565])), 0, 1e-10),
         'e-code-forward-vols example forward vols are the course example run backwards: 0.204817, 0.21, 0.229565')
ex.claim(round(sum([0.22, 0.204817, 0.21]) / 3, 6) != 0.21, 'e-code-forward-vols the average of the first three forward vols is not the 0.21 vol to six months')

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
tlx = tear_loop([100, 103, 99, 104, 101, 108, 106, 112.0], [0, 1, 1, 0.5, 0.5, -0.5, 0, 0], 12)
ex.claim(tlx[3] == 0.375 and [round(v, 6) for v in tlx] == eval(w18['examples'][0]['expect']), f'e-code-tear-line example by the loop {[round(v, 6) for v in tlx]}, turnover 3/8')

# e-code-first-leak (leak_rows), against a loop over rows written again
w21 = code_item('e-code-first-leak', [
    ('last row only', '.iloc[:cut]', '.iloc[cut - 1:cut]'),
    ('one row too many', '.iloc[:cut]', '.iloc[:cut + 1]'),
    ('tolerance too loose', 'atol=1e-9', 'atol=1e-1'),
    ('noise ignored', 'run(noise_after(bars, cut))', 'run(bars)'),
])
ns21 = {}
exec(w21['prelude'] + w21['solution'], ns21)
b21 = ns21['make_bars'](400)
g21 = b21.copy()
g21.iloc[118:121, g21.columns.get_loc('close')] = np.nan


def leak_loop(run, bars, cut):
    a = run(bars)
    b = run(ns21['noise_after'](bars, cut))
    out_ = []
    for i in range(min(cut, len(bars))):
        x, y = float(a.iloc[i]), float(b.iloc[i])
        if not (math.isnan(x) and math.isnan(y)) and abs(x - y) > 1e-9:
            out_.append(i)
    return out_


bad21 = 0
for name in ('honest_engine', 'peek_engine', 'scaled_engine', 'late_engine', 'bfill_engine', 'ffill_engine'):
    for cut in (1, 2, 50, 120, 121, 122, 299, 300, 301, 350, 399, 400):
        for bb in (b21, g21):
            bad21 += ns21['leak_rows'](ns21[name], bb, cut) != leak_loop(ns21[name], bb, cut)
ex.claim(bad21 == 0, f'e-code-first-leak leak_rows = row loop on 6 engines x 12 cuts x 2 bar sets ({bad21} differences)')
eng = [k for k in ns21 if k.endswith('_engine')]
ex.claim(len(eng) == 6 and '# six engines' in w21['prelude'] and '# five engines' not in w21['prelude'], f'e-code-first-leak prelude defines {len(eng)} engines and says six')
ch121 = ns21['leak_rows'](ns21['bfill_engine'], g21, 121)
ex.claim(ch121 == [118] and 'row 118' in IT['e-code-first-leak']['explain']['text'] and 'row 120 stays the same' in IT['e-code-first-leak']['explain']['text'],
         f'e-code-first-leak at cut 121 the backfill engine changes rows {ch121}; row 120 is unchanged (finding 21c)')

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
