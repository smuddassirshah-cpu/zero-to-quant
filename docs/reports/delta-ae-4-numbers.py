#!/usr/bin/env python3
"""Delta read AE-4: the parts changed by the fix passes on delta reads AE-2 and AE-3.

Run with the scratchpad venv Python. Imports no earlier script. Paths come from __file__.

Every key, `wrong` value and printed number of the changed parts is recomputed here by a route
of this reader's own: day counts for the P&L, a compounding loop for the doubling time, numpy
on the raw data for the crabs and the disputes, scikit-learn's StandardScaler, a head count of
the 200 issues with Fractions, scipy's normal and chi-square laws, a simulation for the
encoding. Each numeric part's bands are rebuilt with the engine's rule (|x - a| <= tol + 1e-9,
grade.js) and fed the value a learner types from the rounded numbers the part prints.

Exit code. A check of this script's own arithmetic that fails is a bug and exits 1. A check
that fails because the content is as the review describes prints a FINDING line and does not
change the exit code, so the script exits 0 as committed (CI runs every script in docs/reports).
When a finding is fixed its line prints "resolved".
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
COURSES = os.path.join(HERE, '..', '..', 'app', 'content', 'courses')

checks = fails = findings = 0


def ok(cond, name):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', name)


def finding(n, still_there, name):
    """still_there is True while the content is as the review describes."""
    global findings
    if still_there:
        findings += 1
        print(f'FINDING {n}: {name}')
    else:
        print(f'resolved {n}: {name}')


def load(course, name):
    with open(os.path.join(COURSES, course, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def item(course, name, iid):
    return next(it for it in load(course, name)['items'] if it['id'] == iid)


def strings(o, skip=('id', 'skills', 'kind', 'layout', 'keyboard')):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in skip:
                out += strings(v, skip)
    elif isinstance(o, list):
        for v in o:
            out += strings(v, skip)
    elif isinstance(o, str):
        out.append(o)
    return out


def inband(x, a, tol):
    return abs(x - a) <= tol + 1e-9


def route(widget, x):
    """Where the engine sends a typed x: 'key', a wrong id, or None (generic line)."""
    if inband(x, widget['answer'], widget['tol']['abs']):
        return 'key'
    for w in widget.get('wrong', []):
        if inband(x, w['value'], w['tol']['abs']):
            return w['id']
    return None


def bands(pid, part, key_typed, wrong_typed):
    """key_typed: values that must grade right. wrong_typed: {id: [values that must reach it]}."""
    w = part['widget']
    for x in key_typed:
        ok(route(w, x) == 'key', f'{pid}: key band takes {x}')
    ids = {e['id'] for e in w.get('wrong', [])}
    ok(ids == set(wrong_typed), f'{pid}: wrong ids are {sorted(wrong_typed)} (found {sorted(ids)})')
    for wid, xs in wrong_typed.items():
        for x in xs:
            ok(route(w, x) == wid, f'{pid}: {x} is refused by the key and reaches {wid} (got {route(w, x)})')
        ok(wid in part['feedback'].get('byKey', {}), f'{pid}: {wid} has its own byKey line')
    es = [(w['answer'], w['tol']['abs'], 'key')] + [(e['value'], e['tol']['abs'], e['id']) for e in w.get('wrong', [])]
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            a, ta, na = es[i]
            b, tb, nb = es[j]
            ok(abs(a - b) > ta + tb + 2e-9, f'{pid}: bands {na} and {nb} do not overlap')


def has(text, *needles):
    return all(n in text for n in needles)


def alltext(part):
    return ' '.join(strings(part))


# ---------------------------------------------------------------- ensembles/problems-3 p-futures-study
PID = 'futures-study'
it = item('ensembles', 'problems-3', 'p-futures-study')
P = it['parts']
n, right, up = 240, 138, 126
hit, base = F(right, n), F(up, n)
se_base = math.sqrt(float(base * (1 - base)) / n)
t = float(hit - base) / se_base
t_counts = (right - up) / math.sqrt(n * float(base * (1 - base)))      # same statistic on counts
ok(abs(t - t_counts) < 1e-12 and abs(t - 1.5511) < 1e-4, f'{PID} p2: t = {t:.4f}')
ok(round(se_base, 4) == 0.0322, f'{PID} p2: standard error 0.0322')
t_from_print = 0.05 / 0.0322
fifty_own_se = 0.075 / math.sqrt(0.25 / n)          # error built from 0.5
fifty_base_se = 0.075 / se_base                     # error the part tells the learner to use
fifty_print = 0.075 / 0.0322
hit_se = 0.05 / math.sqrt(0.575 * 0.425 / n)
one_day = 0.05 / math.sqrt(0.525 * 0.475)
bands(f'{PID} p2', P[1], [round(t, 2), t, round(t_from_print, 2)],
      {'fifty': [2.32, 2.33, round(fifty_own_se, 4), round(fifty_base_se, 4), round(fifty_print, 2), fifty_print],
       'one-day': [0.1, round(one_day, 2)],
       'hit-se': [round(hit_se, 2), 1.57]})
ok(not inband(1.57, 2.325, 0.006) and not inband(1.55, 2.325, 0.006), f'{PID} p2: fifty band refuses 1.55 and 1.57')

# part 3 feeds part 4: gross by counting days
move = F(8, 1000) * 2_000_000
gross_days = (right - (n - right)) * move
ok(move == 16000 and gross_days / n == 2400, f'{PID} p3: gross {gross_days / n} a day by day count')
ok(P[2]['widget']['answer'] == 2400, f'{PID} p3: key 2400')
# part 4
unit = F(7, 10000) * 2_000_000
flips = n // 4
net_days = gross_days - flips * 2 * unit
ok(unit == 1400 and 2 * unit == 2800, f'{PID} p4: 7 bp of 2m is 1,400, a flip 2,800')
ok(net_days / n == 1700 and net_days == 408000, f'{PID} p4: {net_days / n} a day, {net_days} over 240 days')
ok(2400 - F(1, 4) * 2 * unit == 1700, f'{PID} p4: expectation route 1700')
ok(P[3]['widget']['answer'] == 1700 and P[3]['widget']['tol']['abs'] == 0, f'{PID} p4: key 1700, tol 0')
bands(f'{PID} p4', P[3], [1700],
      {'gross': [2400], 'flip-one': [float(2400 - F(1, 4) * unit)], 'every-day': [float(2400 - 2 * unit)]})
ok(2400 - F(1, 4) * unit == 2050 and 2400 - 2 * unit == -400, f'{PID} p4: 2050 and -400')
ok(F(700, 2400) > F(1, 4) and round(700 / 2400, 2) == 0.29, f'{PID} p4: costs take over a quarter (0.29)')
tx = alltext(P[3])
ok(has(tx, '7 bp of £2m', '£1{,}400', '£2{,}800', '£700', '£1,700', '£400'), f'{PID} p4: printed numbers')
ok('1,000' not in tx and '2,000' not in tx and '10 bp' not in tx, f'{PID} p4: none of rv-pnl\'s numbers left')
# part 5
ok(P[4]['widget']['kind'] == 'choice', f'{PID} p5: choice')
opts = {o['id']: o for o in P[4]['widget']['options']}
ok([k for k, o in opts.items() if o.get('correct')] == ['not-shown'], f'{PID} p5: key not-shown')
gross_base = (up - (n - up)) * move / n
ok(gross_base == 800 and gross_base - 700 == 100, f'{PID} p5: at 0.525 the book grosses 800 and nets 100')
ok(float(base - (1 - base)) == 0.05, f'{PID} p5: 0.525 - 0.475 = 0.05')
ok(240 * 1700 == 408000, f'{PID} p5: 240 days at 1,700')
tx = alltext(P[4])
ok(has(tx, '£100', '£408,000', '1.55', '0.525', '£800', '£700 of £2,400'), f'{PID} p5: printed numbers')
ok(not re.search(r'stopp|random share|later block', tx), f'{PID} p5: nothing of the old random-validation choice')

# reuse rows on this item
e3 = load('ensembles', 'l12-trees-on-returns')
s3 = e3['screens'][3]
mask = lambda s: re.sub(r'\d+(?:[.,]\d+)*', '#', s)
finding(1, P[0]['question'].endswith(s3['question'])
        and P[0]['feedback']['generic'].startswith(s3['feedback']['generic'].rstrip('.'))
        and mask(P[0]['feedback']['byKey']['test-row']) == mask(s3['feedback']['byKey']['test']),
        'p-futures-study part 1 repeats l12 screens[3]: the question sentence, the generic line and the test-row line')
hw = next(i for i in load('ensembles', 'homework-3')['items'] if i['id'] == 'hw-t-58')
rv = next(i for i in load('ensembles', 'review-3')['items'] if i['id'] == 'rv-tstat')
a = mask(P[1]['feedback']['byKey']['one-day'])
b = mask(hw['feedback']['byKey']['sd'])
finding(2, a.split('. ')[1] == b.split('. ')[1] and
        P[1]['feedback']['byKey']['fifty'].split('. ')[0] == rv['feedback']['byKey']['fifty'].split('. ')[0],
        'p-futures-study part 2: one-day and fifty lines share a sentence, numbers masked, with hw-t-58 sd and rv-tstat fifty')

# ---------------------------------------------------------------- ensembles/problems-2 p-dividend-importance
PID = 'dividend'
it = item('ensembles', 'problems-2', 'p-dividend-importance')
P = it['parts']
trees = [F(60, 100), F(80, 100), F(70, 100), F(78, 100)]
f1 = sum(trees) / 4
at20 = [f1, F(84, 100), F(66, 100), F(14, 100), F(22, 100), F(12, 100)]
at5 = [F(28, 100), F(36, 100), F(20, 100), F(10, 100), F(14, 100), F(12, 100)]
pd20, pd5 = sum(at20) / 6, sum(at5) / 6
rise = pd20 - pd5
rise_x = (sum(at20[:3]) - sum(at5[:3])) / 3
rise_d = (sum(at20[3:]) - sum(at5[3:])) / 3
ok((f1, pd20, pd5, rise) == (F(72, 100), F(45, 100), F(20, 100), F(25, 100)), f'{PID}: 0.72, 0.45, 0.20, 0.25')
ok(rise_x == F(46, 100) and rise_d == F(4, 100) and 2 * rise - rise_d == rise_x, f'{PID}: 0.46 and 0.04 from the rows')
ok(sum(at5[:3]) == F(84, 100) and sum(at20[:3]) == F(222, 100), f'{PID}: cross-border totals 0.84 and 2.22')
ok([p['widget'].get('answer') for p in P[:4]] == [0.72, 0.45, 0.25, 0.46], f'{PID}: keys unchanged')
bands(f'{PID} p1', P[0], [0.72], {'sum': [2.88], 'max': [0.8], 'vote': [1.0]})
bands(f'{PID} p2', P[1], [0.45], {'sum': [2.7], 'first': [0.72], 'five': [round(float(sum(at20[1:]) / 5), 2), float(sum(at20[1:]) / 5)]})
bands(f'{PID} p3', P[2], [0.25], {'start': [0.2], 'ratio': [2.25], 'sum': [0.65]})
bands(f'{PID} p4', P[3], [0.46], {'pd': [0.25], 'double': [0.5], 'added': [0.29]})
tx = ' '.join(strings(it))
ok(not re.search(r'\bslip|\border|urgent|calm|dividend', tx, re.I), f'{PID}: no word of the slippage story is left in the text')
ok(has(tx, 'custody desk', 'settle late', 'cross-border', 'domestic'), f'{PID}: custody story in place')
other = item('ensembles', 'problems-2', 'p-bond-downgrades')
finding(3, 'bond' in it['prose'] and 'bonds' in other['prose'],
        'ensembles/problems-2: p-dividend-importance and p-bond-downgrades both set a desk\'s trees on bonds')

# ---------------------------------------------------------------- fin-ml/problems-3 p-power-spread-cap
PID = 'power-cap'
it = item('fin-ml', 'problems-3', 'p-power-spread-cap')
P = it['parts']
p, b, cap = 0.70, 0.8, 0.20
g = lambda f, bb=b: p * math.log(1 + bb * f) + (1 - p) * math.log(1 - f)
kelly = p - (1 - p) / b
grid = np.linspace(0.001, 0.999, 99801)
f_star = grid[np.argmax([g(f) for f in grid])]
ok(abs(kelly - 0.325) < 1e-12 and abs(f_star - 0.325) < 2e-5, f'{PID} p1: Kelly 0.325 by formula and by maximising growth')
ok(round(g(kelly), 4) == 0.0439 and round(g(cap), 4) == 0.0370, f'{PID} p2, p3: growth 0.0439 and 0.0370')
bands(f'{PID} p1', P[0], [0.325], {'even-odds': [2 * p - 1], 'times-b': [p - (1 - p) * b]})
bands(f'{PID} p2', P[1], [0.0439, g(kelly)], {'even-payout': [round(g(kelly, 1.0), 4)], 'swapped': [round(0.3 * math.log(1.26) + 0.7 * math.log(0.675), 4)]})
bands(f'{PID} p3', P[2], [0.0370, g(cap)], {'uncapped': [0.0439], 'even-payout': [round(g(cap, 1.0), 4)]})


def bets_to_double(rate):
    cap_, k = 1.0, 0
    while cap_ < 2 - 1e-12:
        cap_ *= math.exp(rate)
        k += 1
    return k


ok(bets_to_double(0.0370) == 19 == math.ceil(math.log(2) / 0.0370), f'{PID} p4: 19 bets by compounding and by ln 2 / 0.0370')
ok(bets_to_double(g(cap)) == 19, f'{PID} p4: 19 from the unrounded growth too')
ok(bets_to_double(0.0439) == 16 == bets_to_double(g(kelly)), f'{PID} p4: 16 at the Kelly growth, rounded or not')
ok(round(math.log(2) / 0.0370, 1) == 18.7 and round(math.log(2) / 0.0439, 1) == 15.8, f'{PID} p4: 18.7 and 15.8')
ok(round(math.exp(18 * 0.0370), 2) == 1.95 and round(math.log(2), 3) == 0.693, f'{PID} p4: 1.95 after 18 bets; ln 2 = 0.693')
ok(math.ceil(1 / 0.0370) == 28 and 19 - 16 == 3, f'{PID} p4: no-log 28; the cap costs three bets')
ok(P[3]['widget']['answer'] == 19 and P[3]['widget']['tol']['abs'] == 0, f'{PID} p4: key 19, tol 0')
bands(f'{PID} p4', P[3], [19], {'kelly': [16], 'round-down': [math.floor(math.log(2) / 0.0370)], 'no-log': [28], 'even-payout': [math.ceil(math.log(2) / 0.0607)]})
tx = alltext(P[3])
ok(has(tx, '18.7', '0.693', '1.95', '15.8', '16', 'three bets'), f'{PID} p4: printed numbers')
carried = math.ceil(math.log(2) / round(g(cap, 1.0), 4))
ok(carried == 12, f'{PID} p4: part 3\'s even-payout slip, 0.0607, carried on gives 12')
finding(4, route(P[3]['widget'], carried) is None,
        'p-power-spread-cap part 4: 12, from part 3\'s even-payout slip 0.0607, has no wrong entry')
ok(not P[4]['explain']['text'].startswith('Each stage uses the one before'), f'{PID} p5: explain no longer opens with l12\'s sentence')
ok([o['id'] for o in P[4]['widget']['options'] if o.get('correct')] == ['sizing'], f'{PID} p5: key sizing')
l12 = load('fin-ml', 'l12-end-to-end')
order = re.findall(r'[a-z-]+(?: with DSR)?', [h['text'] for h in l12['screens'][0]['hints']][2].lower())
ok('calibration' in order and order.index('calibration') < order.index('sizing') < order.index('costs'),
   f'{PID} p5: l12 screen 0 puts sizing after calibration and before costs')
doubling = 0
for fn in sorted(os.listdir(os.path.join(COURSES, 'fin-ml'))):
    if fn.endswith('.json') and fn not in ('course.json', 'problems-3.json'):
        with open(os.path.join(COURSES, 'fin-ml', fn), encoding='utf-8') as fh:
            doubling += len(re.findall(r'to double|doubling time|\\ln 2\b', fh.read()))
ok(doubling == 0, f'{PID} p4: no doubling-time question elsewhere in fin-ml ({doubling} hits)')

# ---------------------------------------------------------------- eigen/problems-3 p-crab-sizes
PID = 'crab'
it = item('eigen', 'problems-3', 'p-crab-sizes')
P = it['parts']
W = np.array([191, 151, 145, 139, 99.0])
C = np.array([88, 118, 85, 52, 82.0])
X = np.column_stack([W - W.mean(), C - C.mean()])
S = np.cov(X.T)
vals, vecs = np.linalg.eigh(S)
ok(np.allclose(S, [[1076, 168], [168, 549]]) and np.allclose(vals, [500, 1125]), f'{PID}: covariance and eigenvalues')
v1 = vecs[:, -1] * np.sign(vecs[:, -1][np.argmax(abs(vecs[:, -1]))])
v0 = np.array([-0.28, 0.96])                      # the printed column for 500
ok(np.allclose(v1, [0.96, 0.28]) and np.allclose(S @ v0, 500 * v0), f'{PID}: PC1 (0.96, 0.28); printed first column belongs to 500')
x1 = X[0]
ok(np.allclose(x1, [46, 3]), f'{PID}: crab 1 demeaned (46, 3)')
s_key, s_first, s_pc2 = x1 @ v1, x1 @ v0, x1 @ np.array([0.28, -0.96])
s_raw = np.array([191, 88]) @ v1
ok(np.allclose([s_key, s_first, s_pc2, s_raw], [45, -10, 10, 208]), f'{PID} p4: scores 45, -10, 10, 208')
ok(F(-28, 100) * 46 + F(96, 100) * 3 == -10, f'{PID} p4: -0.28 x 46 + 0.96 x 3 = -10 exactly')
bands(f'{PID} p4', P[3], [45], {'no-flip': [-45], 'raw': [208], 'pc2': [10], 'first-column': [round(float(s_first), 6)]})
ok(has(P[3]['feedback']['byKey']['first-column'], '(-0.28, 0.96)', '500', '(0.96, 0.28)'), f'{PID} p4: first-column line names the column and the fix')
ok(any(w.get('tex') == '(-0.28, 0.96)' for w in P[2]['widget']['wrong']), f'{PID} p3: the slip carried on is part 3\'s first-column')

# ---------------------------------------------------------------- stat-learning/problems-2 p-ice-cream-van
PID = 'bike-hire'
it = item('stat-learning', 'problems-2', 'p-ice-cream-van')
P = it['parts']
model = lambda x, w, inter=0.5, dum=8: 20 + 1.5 * x + dum * w + inter * x * w
days = [(12, 1, 55), (10, 0, 33), (16, 0, 45), (6, 1, 38)]
fc = [model(x, w) for x, w, _ in days]
y = np.array([d[2] for d in days], float)
mse = float(np.mean((y - fc) ** 2))
base_mse = float(np.mean((y - 40) ** 2))
ok(fc == [52, 35, 44, 40] and mse == 4.5 and base_mse == 75.75, f'{PID}: forecasts, 4.5 and 75.75')
fc_no = [model(x, w, inter=0) for x, w, _ in days]
mse_no = float(np.mean((y - fc_no) ** 2))
tm = float(np.mean((y - y.mean()) ** 2))
ok(mse_no == 21.75 and y.mean() == 42.75 and round(tm, 2) == 68.19, f'{PID}: slips 21.75 and 68.19')
bands(f'{PID} p1', P[0], [2.0, 2], {'weekday': [1.5], 'interaction': [0.5]})
bands(f'{PID} p2', P[1], [52], {'no-interaction': [model(12, 1, inter=0)], 'no-dummy': [model(12, 1, dum=0)], 'weekday': [model(12, 0)]})
bands(f'{PID} p3', P[2], [4.5], {'carried': [mse_no], 'absolute': [float(np.mean(abs(y - fc)))], 'sum': [float(np.sum((y - fc) ** 2))]})
bands(f'{PID} p4', P[3], [75.75], {'test-mean': [round(tm, 2), tm], 'absolute': [float(np.mean(abs(y - 40)))]})
bands(f'{PID} p5', P[4], [round(1 - mse / base_mse, 3), 1 - mse / base_mse],
      {'ratio': [round(mse / base_mse, 3)], 'test-mean': [round(1 - mse / 68.19, 3)], 'carried': [round(1 - mse_no / base_mse, 3)]})
tx = ' '.join(strings(it))
ok(not re.search(r'ice|van\b|deckchair|chair|cone', tx, re.I), f'{PID}: no word of the van or the deckchairs is left')
ok(has(tx, 'bike-hire stand', 'tens of bikes', 'bike hires'), f'{PID}: bike-hire nouns in place')
ok(model(6, 1) == 40, f'{PID}: the 6 degree Sunday forecast is 40 tens')

# ---------------------------------------------------------------- validation/problems-2 p-signal-break
PID = 'signal-break'
it = item('validation', 'problems-2', 'p-signal-break')
P = it['parts']
sd = lambda m: math.sqrt(2 / m)
# sd of an MSE of m unit-variance normal errors, from the chi-square law, against the formula
ok(abs(stats.chi2(140).std() / 140 - sd(140)) < 1e-12 and abs(stats.chi2(420).std() / 420 - sd(420)) < 1e-12, f'{PID}: sd of an MSE is sqrt(2/n)')
ok(round(sd(140), 4) == 0.1195 and round(sd(420), 4) == 0.0690 and round(sd(1120), 4) == 0.0423, f'{PID}: 0.1195, 0.0690, 0.0423')
joined = (1.31 + 1.38 + 1.44) / 3
ok(round(joined, 3) == 1.377, f'{PID}: joined MSE 1.377')
bar = 1 + 2 * 0.0690
ok(round(bar, 3) == 1.138 and round(1 + 2 * sd(420), 3) == 1.138, f'{PID} p5: bar 1.138, rounded sd or not')
ok(P[4]['widget']['kind'] == 'numeric' and P[4]['widget']['answer'] == 1.138 and P[4]['widget']['tol']['abs'] == 0.0005, f'{PID} p5: typed, key 1.138, tol 0.0005')
bands(f'{PID} p5', P[4], [1.138, 1 + 2 * sd(420)],
      {'per-fold': [round(1 + 2 * 0.1195, 3), 1 + 2 * sd(140)],
       'one-sd': [round(1 + 0.0690, 3), 1 + sd(420)],
       'all-days': [round(1 + 2 * 0.0423, 3), 1 + 2 * 0.0423, 1 + 2 * sd(1120)]})
ok(joined > bar and has(P[4]['explain']['text'], '1.138', '1.377', '700'), f'{PID} p5: explain numbers; 1.377 is over the bar')
ok(round(1 + 2 * 0.1195, 3) == 1.239 and '1.239' in P[2]['question'], f'{PID} p3: one fold\'s bar 1.239')
odds_chi = 1 / stats.chi2.sf(140 * 1.31, 140)
odds_norm = 1 / stats.norm.sf((1.31 - 1) / 0.1195)
ok(odds_chi > 100 and odds_norm > 100, f'{PID} p2: "less than once in 100 tries" (1 in {odds_chi:.0f} chi-square, 1 in {odds_norm:.0f} normal)')
ok('less than once in 100 tries' in P[1]['explain']['text'], f'{PID} p2: corrected odds line present')
ok(not re.search(r'million|once in 200', alltext(it)), f'{PID}: the old odds lines are gone')
ok(not any(k in alltext(P[4]) for k in ('blends', 'outvote', 'since the break')), f'{PID} p5: none of l8\'s or r-mean-hides\' phrases')

# ---------------------------------------------------------------- validation/problems-3 p-fund-flows
PID = 'card-disputes'
it = item('validation', 'problems-3', 'p-fund-flows')
P = it['parts']
x = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13, 17, 16, 20, 22, 18, 24], float)
ok([int(v) for v in re.findall(r'\b\d+\b', it['prose'])][1:17] == [int(v) for v in x], f'{PID}: the 16 counts as printed')
tr, te = x[:12], x[12:]
sc_all = StandardScaler().fit(x.reshape(-1, 1))
sc_tr = StandardScaler().fit(tr.reshape(-1, 1))
s_all, s_tr = float(sc_all.scale_[0]), float(sc_tr.scale_[0])
ok(float(sc_all.mean_[0]) == 15.75 and float(sc_tr.mean_[0]) == 14, f'{PID}: means 15.75 and 14')
ok(abs(s_all - math.sqrt(12.8125)) < 1e-12 and abs(s_tr - math.sqrt(38 / 12)) < 1e-12, f'{PID}: sds from sklearn match 12.8125 and 38/12')
ok(int((x ** 2).sum()) == 4174 and int(((tr - 14) ** 2).sum()) == 38, f'{PID}: 4,174 and 38')
bands(f'{PID} p1', P[0], [3.579, 3.580, s_all], {'train': [1.780, 1.779, s_tr], 'ddof-one': [round(float(x.std(ddof=1)), 3)], 'variance': [12.8125, 12.813]})
bands(f'{PID} p2', P[1], [1.780, 1.779, s_tr], {'all': [3.579, s_all], 'ddof-one': [round(float(tr.std(ddof=1)), 3)], 'variance': [3.1667, 3.167]})
z13 = (20 - 14) / 1.780
bands(f'{PID} p3', P[2], [round(z13, 2), (20 - 14) / s_tr],
      {'leaky': [round((20 - 15.75) / 3.579, 2)], 'mixed': [round((20 - 14) / 3.579, 2)], 'mean-only': [round((20 - 15.75) / 1.780, 2)]})
z_print = [round((v - 14) / 1.780, 2) for v in te]
ok(z_print == [3.37, 4.49, 2.25, 5.62], f'{PID} p4: 3.37, 4.49, 2.25, 5.62 from the printed 1.780 ({z_print})')
ok(sum(abs(v - 14) / s_tr > 3 for v in te) == 3 and sum(abs(v - 14) / s_tr > 3 for v in tr) == 0, f'{PID} p4: three test weeks flagged, no training week')
leaky_max = max(abs(v - 15.75) / s_all for v in te)
ok(2.30 < leaky_max < 2.31 and (24 - 15.75) / 3.579 < 2.31, f'{PID} p4: the leaky scaler\'s largest test week is {leaky_max:.4f}, under 2.31')
ok(sum(abs(v - 15.75) / s_all > 3 for v in te) == 0, f'{PID} p4: the leaky scaler flags none')
bands(f'{PID} p4', P[3], [3], {'leaky': [0], 'all': [4]})
tx = alltext(P[3])
ok(has(tx, '3.37, 4.49 and 5.62', '2.25', '2.31') and '4.50' not in tx and '2.30' not in tx, f'{PID} p4: corrected 2.31 and 4.49 lines')
tx = ' '.join(strings(it))
ok(not re.search(r'£|\bdays?\b|colleague|busy|fund|flow', tx, re.I), f'{PID}: no word of the fund-flow story is left')
ok(has(tx, 'card disputes', 'nightly job', 'heavy'), f'{PID}: disputes story in place')
own = (te - te.mean()) / te.std()
ok(max(abs(own)) < 1.35, f'{PID} p5: scaled by their own mean and sd the four test weeks all sit within 1.35')
q = next(i for i in load('validation', 'l10-scaling-with-future')['quiz'] if i['id'] == 'q-fit-test')
finding(5, 'numbers nobody has when the test starts' in opts_text if (opts_text := alltext(P[4])) else False,
        'p-fund-flows part 5 test-fit: "uses numbers nobody has when the test starts" against l10 q-fit-test "uses numbers you will not have live"')
ok('uses numbers you will not have live' in q['explain']['text'], f'{PID}: l10 q-fit-test line as quoted')

# ---------------------------------------------------------------- validation/problems-3 p-closed-funds
PID = 'closed-funds'
it = item('validation', 'problems-3', 'p-closed-funds')
P = it['parts']
N, alive, dead = 200, 164, 36
r_alive, r_all = F(92, 10), F(668, 100)
r_dead = (N * r_all - alive * r_alive) / dead              # head count
ok(r_dead == F(-48, 10) and r_alive - r_dead == 14, f'{PID} p1: the 36 returned -4.8, so 14.0 points less')
ok((r_alive - r_all) / F(dead, N) == 14 and r_alive - r_all == F(252, 100), f'{PID} p1: 2.52 / 0.18 = 14.0')
ok(P[0]['widget']['answer'] == 14.0 and P[0]['widget']['tol']['abs'] == 0.05, f'{PID} p1: key 14.0, tol 0.05')
gap = float(r_alive - r_all)
bands(f'{PID} p1', P[0], [14.0, 14],
      {'gap': [2.52], 'times': [round(gap * 0.18, 2), gap * 0.18], 'stayers': [round(gap / 0.82, 2)]})
# the part asks for 1 decimal place: what a learner who obeys it types on each slip
one_dp = {'gap': 2.5, 'times': 0.5, 'stayers': 3.1}
unrouted = [k for k, v in one_dp.items() if route(P[0]['widget'], v) != k]
finding(6, bool(unrouted), f'p-closed-funds part 1 asks for 1 decimal place; typed so, {unrouted} miss their bands (2.5, 0.5, 3.1)')
for k, (v, tol) in {'gap': (2.52, 0.025), 'times': (0.45, 0.055), 'stayers': (3.07, 0.035)}.items():
    ok(inband(one_dp[k], v, tol) and not inband(14.0, v, tol), f'{PID} p1 proposal: {k} {v} tol {tol} takes {one_dp[k]}')
ok(2.52 + 0.025 < 3.07 - 0.035 and 0.45 + 0.055 < 2.52 - 0.025, f'{PID} p1 proposal: widened bands do not overlap')
ok(F(200) * F(252, 100) / 36 == 14, f'{PID} p1 proposal: 200 x 2.52 / 36 = 14.0')
sharpe = (F(84, 10) - F(252, 100)) / 9
ok(round(float(sharpe), 3) == 0.653 and F(84, 10) - F(252, 100) == F(588, 100), f'{PID} p2: 5.88 / 9 = 0.653')
bands(f'{PID} p2', P[1], [0.653, float(sharpe)],
      {'survivors': [round(8.4 / 9, 3)], 'added': [round((8.4 + 2.52) / 9, 3)], 'whole-gap': [round((8.4 - 14.0) / 9, 3)]})
ok(has(P[1]['question'], '9.2 - 6.68 = 2.52', '8.4%', '9%'), f'{PID} p2: the question restates 2.52')
ok(round(float(F(18, 100) * 14), 2) == 2.52, f'{PID} p2 proposal: 0.18 x 14.0 = 2.52')
finding(7, '14.0' not in P[1]['question'] and 'part 1' not in P[1]['question'],
        'p-closed-funds part 2 no longer uses part 1: 14.0 feeds only the whole-gap slip')
r_gap = next(i for i in load('validation', 'review-3')['items'] if i['id'] == 'r-gap')
l11 = load('validation', 'l11-dead-companies')['screens'][8]
m = mask
finding(8, 'points a year less than the' in P[0]['question'] and 'points a year less than the' in r_gap['prose']
        and m(P[0]['feedback']['byKey']['gap']).endswith('Only #% of issues defaulted, so divide by #.')
        and m(l11['feedback']['byKey']['four']).endswith('Only #% of funds closed, so multiply by #.'),
        'p-closed-funds part 1: r-gap\'s phrase in the question, and the gap line mirrors l11 screens[8] four')
ok(round(1.63 / math.sqrt(7), 3) == 0.616 and round(0.653 - 0.616, 2) == 0.04, f'{PID} p3, p4: 0.616 and 0.04 unchanged')

# ---------------------------------------------------------------- validation/problems-3 p-carry-lookbacks
PID = 'carry'
it = item('validation', 'problems-3', 'p-carry-lookbacks')
P = it['parts']
T = 6
sd6 = 1 / math.sqrt(T)
ok(round(sd6, 4) == 0.4082, f'{PID} p1: 0.4082')
t_sr = 0.95 / 0.4082
ok(round(t_sr, 3) == 2.327 and round(0.95 * math.sqrt(T), 3) == 2.327, f'{PID} p4: t = 2.327 by 0.95/0.4082 and 0.95 sqrt 6')
ok(P[3]['widget']['answer'] == 2.327 and P[3]['widget']['tol']['abs'] == 0.005, f'{PID} p4: key 2.327, tol 0.005')
bands(f'{PID} p4', P[3], [2.33, t_sr, 0.95 * math.sqrt(T)],
      {'times-sd': [round(0.95 * 0.4082, 2)], 'haircut': [round(0.53 / 0.4082, 2), 1.3], 'by-years': [round(0.95 * 6, 2)]})
z4 = stats.norm.ppf(1 - 0.05 / 4)
z24 = stats.norm.ppf(1 - 0.05 / 24)
z1 = stats.norm.ppf(0.95)
ok(round(z4, 2) == 2.24 and round(z24, 2) == 2.87 and round(z1, 2) == 1.64, f'{PID}: bars 2.24, 2.87, 1.64')
ok(round(2.33 - 2.24, 2) == 0.09 and 2.33 > 2.24 and 2.33 < 2.87, f'{PID} p5: clears 2.24 by 0.09, under 2.87')
ok(round(2.24 * 0.4082, 2) == 0.91, f'{PID} p4: "about 0.91" from the printed 2.24 and 0.4082')
ok(round(1.03 * 0.4082, 3) == 0.420 and round(0.95 - 0.420, 2) == 0.53, f'{PID} p2, p3: 0.420 and 0.53 unchanged')
tx = alltext(P[4])
ok(has(tx, '2.33', '2.24', '2.87', '1.64', '0.09', '0.53', 'years held back'), f'{PID} p5: printed numbers')
tx = ' '.join(strings(it))
ok('She ran all 4 families.' in it['prose'] and 'N = 3' not in tx and 'table' not in tx, f'{PID}: the results-table story is gone')
ok('scaled up or down, and so share one Sharpe ratio' in it['prose'], f'{PID}: corrected prose sentence')
ok('never saw' not in tx, f'{PID}: "data the search never saw" is gone')
hb = next(i for i in load('validation', 'homework-3')['items'] if i['id'] == 'h-bonf')
stem = 'one-sided Bonferroni bar at 5% is $t \\ge'
finding(9, stem in P[3]['question'] and stem in hb['prose'],
        'p-carry-lookbacks part 4 opens with h-bonf\'s stem "one-sided Bonferroni bar at 5% is $t \\ge"')
enc = item('validation', 'problems-3', 'p-fund-encoding')
why_c = next(o for o in P[4]['widget']['options'] if o['id'] == 'real')['why']
why_e = next(o for o in enc['parts'][3]['widget']['options'] if o['id'] == 'real')['why']
finding(10, 'bar guards against the luck of choosing' in why_c and 'bar guards against the luck of choosing' in why_e,
        'validation/problems-3: p-carry-lookbacks part 5 and p-fund-encoding part 4 share the real distractor and its reason')

# ---------------------------------------------------------------- validation/problems-3 p-fund-encoding
PID = 'encoding'
P = enc['parts']
rng = np.random.default_rng(4)
Y = rng.standard_normal((400_000, 12))
xi = (2 * Y[:, 0] + Y[:, 1:].sum(axis=1)) / 13
rho_sim = float(np.corrcoef(xi, Y[:, 0])[0, 1])
rho = 2 / math.sqrt(15)
ok(abs(rho_sim - rho) < 0.004 and round(rho, 4) == 0.5164, f'{PID} p1: rho 0.5164 (simulated {rho_sim:.4f})')
plain13 = float(np.corrcoef(Y[:, 0], np.column_stack([Y, rng.standard_normal(len(Y))]).mean(axis=1))[0, 1])
weight1 = float(np.corrcoef(Y[:, 0], Y.mean(axis=1))[0, 1])
ok(abs(plain13 - 1 / math.sqrt(13)) < 0.004 and round(1 / math.sqrt(13), 4) == 0.2774, f'{PID} p1: a plain mean of 13 labels gives 0.2774 (simulated {plain13:.4f})')
ok(abs(weight1 - 1 / math.sqrt(12)) < 0.004 and round(1 / math.sqrt(12), 4) == 0.2887, f'{PID} p1: weight 1 with the 11 others gives 0.2887, not 0.2774')
bands(f'{PID} p1', P[0], [0.5164, rho], {'unweighted': [0.2774], 'no-square': [round(2 / math.sqrt(13), 4)]})
ok('plain mean of 13 labels' in P[0]['feedback']['byKey']['unweighted'], f'{PID} p1: corrected unweighted line')
tstat = lambda r, m: r * math.sqrt(m - 2) / math.sqrt(1 - r * r)
bands(f'{PID} p3', P[2], [round(tstat(0.5164, 100), 2), tstat(rho, 100)],
      {'category': [round(tstat(0.5164, 13), 2)], 'no-adjust': [round(0.5164 * math.sqrt(98), 2)], 'n-not-n-minus-2': [round(0.5164 * 10 / math.sqrt(1 - 0.5164 ** 2), 2)]})
ok(round(tstat(0.5164, 13), 2) == 2.0, f'{PID} p3: n = 13 gives t = 2.00')
ok(has(P[2]['feedback']['byKey']['category'], 'divisor of one encoding', '98'), f'{PID} p3: corrected category line')
ok('a slip adds the row\'s own label a second time' in enc['prose'] and '/13' in enc['prose'], f'{PID}: the prose states the cause')
ok(round(stats.norm.ppf(1 - 0.05 / 40), 2) == 3.02, f'{PID} p4: bar 3.02 for 40 tries')

print(f'{checks} checks, {fails} failed, {findings} FINDING rows (findings do not change the exit code)')
sys.exit(1 if fails else 0)
