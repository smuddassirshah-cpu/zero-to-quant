#!/usr/bin/env python3
"""Delta read AE-3: recompute of the five problems re-authored by the validation fix pass.

Scope: p-signal-break (problems-2), p-fund-flows, p-closed-funds, p-carry-lookbacks and
p-fund-encoding (problems-3), and the `before-only` value of p-spread-blocks part 3.
Imports nothing from the author's or the second reader's script. Routes: scikit-learn's
TimeSeriesSplit, the exact chi-square law of an MSE, numpy on the raw series, Fractions,
numerical integration of the largest of N normals, seeded simulation, brute sets of days.
Bands use the engine's rule: |v - key| <= abs + 1e-9; a `%` field divides the typed
figure by 100.

Run: <scratch>/venv/bin/python docs/reports/delta-ae-3-numbers.py
Exit 0 when the content is right. A FINDING row fails until the content is fixed.
Paths resolve from __file__.
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
from scipy import stats, integrate
from sklearn.model_selection import TimeSeriesSplit

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'validation')
SETS = {n: json.load(open(os.path.join(COURSE, f'problems-{n}.json'))) for n in (2, 3)}

checks = fails = 0


def ok(cond, msg, finding=False):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print(('FINDING ' if finding else 'FAIL ') + msg)


def item(n, pid):
    return next(i for i in SETS[n]['items'] if i['id'] == pid)


def texts(o):
    """Every learner-facing string of a part or item."""
    if isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)
    elif isinstance(o, str):
        yield o


def alltext(o):
    return ' || '.join(texts(o))


def takes(w, v):
    scale = 100 if w.get('unit') == '%' else 1
    return abs(v / scale - w['answer']) <= w['tol']['abs'] + 1e-9


def wrong_takes(e, w, v):
    scale = 100 if w.get('unit') == '%' else 1
    return abs(v / scale - e['value']) <= e['tol']['abs'] + 1e-9


def numeric(n, pid, k, true, dp, typed, slips):
    """Part k (1-based). `true` is my unrounded key in typed units; `typed` are the
    values a learner types (rounded from the printed inputs); `slips` maps a wrong id
    to the value the slip gives from the printed inputs, in typed units."""
    it = item(n, pid)
    p = it['parts'][k - 1]
    w = p['widget']
    tag = f'{pid} p{k}'
    scale = 100 if w.get('unit') == '%' else 1
    ok(w['kind'] == 'numeric', f'{tag}: numeric')
    ok(abs(true / scale - w['answer']) <= w['tol']['abs'] + 1e-9, f'{tag}: key {w["answer"]} vs mine {true / scale}')
    for v in [round(true, dp)] + list(typed):
        ok(takes(w, v), f'{tag}: band refuses the stated rounding {v}')
    ids = {e['id'] for e in w.get('wrong', [])}
    ok(ids == set(slips), f'{tag}: wrong ids {sorted(ids)} vs recomputed {sorted(slips)}')
    for e in w.get('wrong', []):
        if e['id'] not in slips:
            continue
        v = slips[e['id']]
        ok(wrong_takes(e, w, v), f'{tag}: wrong {e["id"]} {e["value"]} does not take the slip value {v}')
        ok(not takes(w, v), f'{tag}: key band takes the slip {e["id"]} {v}')
        ok(abs(e['value'] - w['answer']) > e['tol']['abs'] + w['tol']['abs'], f'{tag}: wrong band {e["id"]} overlaps the key band')
        ok(e['id'] in p['feedback']['byKey'], f'{tag}: wrong {e["id"]} has no feedback line')
        for e2 in w['wrong']:
            if e2 is not e:
                ok(abs(e['value'] - e2['value']) > e['tol']['abs'] + e2['tol']['abs'], f'{tag}: wrong bands {e["id"]} and {e2["id"]} overlap')
    return p


def choice(n, pid, k, key, others):
    p = item(n, pid)['parts'][k - 1]
    opts = p['widget']['options']
    ok([o['id'] for o in opts if o.get('correct')] == [key], f'{pid} p{k}: key is {key}')
    ok({o['id'] for o in opts} == {key} | set(others), f'{pid} p{k}: option ids')
    for o in opts:
        if not o.get('correct'):
            ok(o['id'] in p['feedback']['byKey'], f'{pid} p{k}: option {o["id"]} has feedback')
    return p


def has(o, s, msg, finding=False):
    ok(s in alltext(o), msg, finding)


def emax(N):
    """Mean of the largest of N standard normals, by integration."""
    return integrate.quad(lambda x: x * N * stats.norm.pdf(x) * stats.norm.cdf(x) ** (N - 1), -12, 12)[0]


r = lambda x, d: float(f'{x:.{d}f}')

# ---------------------------------------------------------------- p-signal-break
PID = 'p-signal-break'
it = item(2, PID)
mses = [1.02, 0.97, 1.08, 1.05, 1.31, 1.38, 1.44]
for m in mses:
    has(it['prose'], str(m) if m != 1.44 else '1.44', f'{PID}: prose lists {m}')
folds = list(TimeSeriesSplit(n_splits=7).split(np.zeros(1120)))
ok(all(len(te) == 140 for _, te in folds), f'{PID}: sklearn test blocks of 140')
ok(folds[0][1][0] == 140 and len(folds[4][0]) == 700 and folds[4][1][0] == 700 and folds[4][1][-1] == 839,
   f'{PID}: fold 5 trains on 700, tests 700 to 839')
ok(len(folds[3][0]) == 560, f'{PID}: fold 4 trains on 560')
# sd of an MSE of n normal errors with variance 1: sd(chi2_n)/n, exact
se = math.sqrt(stats.chi2.var(140)) / 140
ok(abs(se - math.sqrt(2 / 140)) < 1e-12, f'{PID}: chi-square sd equals sqrt(2/n)')
rng = np.random.default_rng(31)
sim = (rng.standard_normal((40000, 140)) ** 2).mean(axis=1).std()
ok(abs(sim - se) < 0.002, f'{PID}: simulated sd {sim}')
numeric(2, PID, 1, se, 4, [0.1195], {'no-two': r(1 / math.sqrt(140), 4), 'all-days': r(math.sqrt(2 / 1120), 4)})
p2 = numeric(2, PID, 2, 0.31 / 0.1195, 1, [2.6], {'all-days': r(0.31 / 0.0423, 1), 'fold-4': r((1.31 - 1.05) / 0.1195, 1),
                                                    'no-two': r(0.31 / 0.0845, 1)})
has(p2['question'], '0.1195', f'{PID} p2 restates 0.1195')
odds_chi = 1 / stats.chi2.sf(140 * 1.31, 140)
odds_norm = 1 / stats.norm.sf(0.31 / 0.1195)
ok(120 < odds_chi < 130 and 200 < odds_norm < 220, f'{PID} p2: one fold at 1.31 is 1 in {odds_chi:.0f} (chi-square), 1 in {odds_norm:.0f} (normal)')
ok('once in 200' not in p2['explain']['text'] and 'less than once in 100 tries' in p2['explain']['text'] and odds_chi > 100,
   f'{PID} p2 explain: must say "less than once in 100 tries" (an MSE of 140 normal errors passes 1.31 once in {odds_chi:.0f})', finding=True)
thr = r(1 + 2 * 0.1195, 3)
ok(thr == 1.239, f'{PID} p3: threshold 1.239')
first = next(i for i, m in enumerate(mses) if m > thr)
ok(first == 4, f'{PID} p3: fold 5 is the first over the threshold')
p3 = numeric(2, PID, 3, len(folds[first][0]), 0, [700], {'previous-fold': len(folds[first - 1][0]), 'test-end': int(folds[first][1][-1]) + 1,
                                                          'fold-number': first + 1})
has(p3['question'], '1.239', f'{PID} p3 restates the threshold')
joined = sum(140 * m for m in mses[4:]) / 420
ok(r(joined, 3) == 1.377, f'{PID} p4: joined MSE {joined}')
se3 = math.sqrt(stats.chi2.var(420)) / 420
ok(r(se3, 4) == 0.0690, f'{PID} p4: sd over 420 days {se3}')
p4 = numeric(2, PID, 4, (joined - 1) / se3, 1, [5.5, r(0.377 / 0.0690, 2)], {'per-fold': r(0.377 / 0.1195, 1), 'all-days': r(0.377 / 0.0423, 1)})
tail_chi = stats.chi2.sf(420 * 1.377, 420)
ok(tail_chi < 1e-6, f'{PID} p5: chi-square tail {tail_chi} is under one in a million')
# finding 1: p5 is now a typed part, the 2-sd level over 420 days
p5 = numeric(2, PID, 5, 1 + 2 * se3, 3, [1.138, r(1 + 2 * 0.0690, 3)],
             {'per-fold': r(1 + 2 * 0.1195, 3), 'one-sd': r(1 + 0.0690, 3), 'all-days': r(1 + 2 * 0.0423, 3)})
has(p5['question'], '0.0690', f'{PID} p5 restates 0.0690')
ok(joined > 1 + 2 * se3, f'{PID} p5: 1.377 is above the 2-sd level')
ok('one in a million' not in alltext(item(2, PID)), f'{PID}: no claim about one in a million remains (tail {tail_chi:.1e})')
ok(1120 - 700 == 420, f'{PID} p5: 420 days since the flag')

# ---------------------------------------------------------------- p-fund-flows
PID = 'p-fund-flows'
it = item(3, PID)
x = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13, 17, 16, 20, 22, 18, 24], dtype=float)
has(it['prose'], '12, 15, 11, 14, 13, 16, 12, 15, 14, 13, 17, 16, 20, 22, 18 and 24', f'{PID}: prose series')
tr, te = x[:12], x[12:]
from sklearn.preprocessing import StandardScaler
s_all = StandardScaler().fit(x.reshape(-1, 1))
s_tr = StandardScaler().fit(tr.reshape(-1, 1))
ok(abs(s_all.mean_[0] - 15.75) < 1e-12 and abs(s_tr.mean_[0] - 14) < 1e-12, f'{PID}: means 15.75 and 14')
ok((x ** 2).sum() == 4174 and ((tr - 14) ** 2).sum() == 38, f'{PID}: sums of squares 4,174 and 38')
ok(list(tr - 14) == [-2, 1, -3, 0, -1, 2, -2, 1, 0, -1, 3, 2], f'{PID} p2: printed deviations')
numeric(3, PID, 1, s_all.scale_[0], 3, [3.579, 3.580], {'train': r(s_tr.scale_[0], 3), 'ddof-one': r(x.std(ddof=1), 3), 'variance': x.var()})
numeric(3, PID, 2, s_tr.scale_[0], 3, [1.780, 1.779], {'all': r(s_all.scale_[0], 3), 'ddof-one': r(tr.std(ddof=1), 3), 'variance': r(tr.var(), 4)})
ok(1.95 < s_all.scale_[0] / s_tr.scale_[0] < 2.05, f'{PID} p1 explain: spread roughly doubles')
p3 = numeric(3, PID, 3, 6 / 1.780, 2, [3.37, r(6 / s_tr.scale_[0], 2)],
             {'leaky': r((20 - 15.75) / 3.579, 2), 'mixed': r(6 / 3.579, 2), 'mean-only': r((20 - 15.75) / 1.780, 2)})
has(p3['question'], '1.780', f'{PID} p3 restates 1.780')
z_clean = (te - 14) / 1.780
z_leaky = (te - 15.75) / 3.579
p4 = numeric(3, PID, 4, int((np.abs(z_clean) > 3).sum()), 0, [3], {'leaky': int((np.abs(z_leaky) > 3).sum()), 'all': 4})
ok(int((np.abs((tr - 14) / 1.780) > 3).sum()) == 0, f'{PID} p4: no training day is flagged')
for d, z in zip((13, 15, 16), (z_clean[0], z_clean[2], z_clean[3])):
    has(p4, f'{z:.2f}', f'{PID} p4: day {d} printed as {z:.2f}')
ok(f'{z_clean[1]:.2f}' == '4.49' and f'{8 / s_tr.scale_[0]:.2f}' == '4.50', f'{PID} p4: week 14 is 4.49 from 1.780 and 4.50 unrounded')
ok('4.49' in p4['feedback']['correct'] and '4.50' not in p4['feedback']['correct'],
   f'{PID} p4 feedback: week 14 must print 4.49, since the generic line says to use 1.780 and 8/1.780 = {8 / 1.780:.4f}', finding=True)
ok(z_leaky.max() > 2.30 and f'{z_leaky.max():.2f}' in ('2.31', '2.30'), f'{PID} p4: leaky maximum {z_leaky.max():.4f}')
ok('beyond 2.30' not in alltext(p4) and 'beyond 2.31 sds' in p4['feedback']['byKey']['leaky'],
   f'{PID} p4 leaky line: must say "beyond 2.31 sds", since week 16 is at {z_leaky.max():.3f} ({8.25 / s_all.scale_[0]:.4f} unrounded)', finding=True)
choice(3, PID, 5, 'train-fit', ['robust', 'test-fit', 'drop'])

# ---------------------------------------------------------------- p-closed-funds
PID = 'p-closed-funds'
it = item(3, PID)
for s in ('164', '9.2%', '200', '36 defaults', '6.68%', '7 years'):
    has(it['prose'], s, f'{PID}: prose has {s}')
dead = F(18, 100) * 200
ok(dead == 36, f'{PID}: 36 defaulted')
allret = (F(164) * F(92, 10) + F(36) * (F(92, 10) - 14)) / 200          # head count, not the gap formula
ok(allret == F(668, 100), f'{PID} p1: all 200 average {allret}')
ok(allret == F(668, 100), f'{PID}: the prose 6.68% is the head-count average')
dmean = (200 * F(668, 100) - 164 * F(92, 10)) / 36                # defaulted issues' mean from the two files
ok(dmean == F(-48, 10), f'{PID} p1: defaulted issues average -4.8')
numeric(3, PID, 1, float(F(92, 10) - dmean), 1, [14.0], {'gap': 2.52, 'times': r(2.52 * 0.18, 2), 'stayers': r(2.52 / 0.82, 2)})
over = F(92, 10) - allret
ok(over == F(252, 100), f'{PID}: overstatement 2.52')
p2 = numeric(3, PID, 2, float((F(84, 10) - over) / 9), 3, [0.653], {'survivors': r(8.4 / 9, 4), 'added': r((8.4 + 2.52) / 9, 4), 'whole-gap': r((8.4 - 14) / 9, 4)})
ok('6.68' in p2['question'] and '2.52' in p2['question'] and 'part 1' not in p2['question'],
   f'{PID} p2: the question must restate 9.2 - 6.68 = 2.52 and not point at part 1', finding=True)
ok(r(emax(5), 2) == 1.16 and r(emax(12), 2) == 1.63, f'{PID} p3: mean best 1.16 and 1.63 ({emax(5)}, {emax(12)})')
p3 = numeric(3, PID, 3, 1.63 / math.sqrt(7), 3, [0.616], {'note': r(1.16 / math.sqrt(7), 4), 'by-years': r(1.63 / 7, 4)})
has(p3['feedback']['correct'], '2.646', f'{PID} p3: root 7 printed 2.646')
p4 = numeric(3, PID, 4, 0.653 - 0.616, 2, [0.04], {'note': 0.653 - 0.438, 'survivors': 0.933 - 0.616})
for e in p4['widget']['wrong']:
    v = {'note': 0.215, 'survivors': 0.317}[e['id']]
    for t in ({'note': (0.21, 0.22), 'survivors': (0.32,)}[e['id']]):
        ok(abs(t - e['value']) <= e['tol']['abs'] + 1e-9, f'{PID} p4: wrong {e["id"]} takes the 2 dp value {t}')
has(p4['question'], '0.653', f'{PID} p4 restates 0.653')
has(p4['question'], '0.616', f'{PID} p4 restates 0.616')
ok('0.04' in p4['feedback']['correct'] and 'nearly nothing' not in p4['feedback']['correct'], f'{PID} p4: correct line without the l12 wording')
p5 = choice(3, PID, 5, 'tiny', ['file', 'note', 'half'])
ok(r(8.4 / 9, 2) == 0.93 and r(0.6533 - 0.4384, 2) == 0.21 and r(0.9333 / 2, 2) == 0.47, f'{PID} p5: 0.93, 0.21, 0.47')
ok(1 / math.sqrt(7) > 0.04, f'{PID} p5 explain: the estimate noise 0.378 exceeds 0.04')
ok(over / F(18, 100) == 14 and r(2.52 * 0.18, 2) == 0.45 and r(2.52 / 0.82, 2) == 3.07, 'finding 3: 2.52/0.18 = 14.0; slips 0.45 and 3.07')

# ---------------------------------------------------------------- p-carry-lookbacks
PID = 'p-carry-lookbacks'
it = item(3, PID)
for s in ('24', '6 years', '4 families of 6', '0.95', 'She ran all 4 families', 'scaled up or down'):
    has(it['prose'], s, f'{PID}: prose has {s}')
sd6 = 1 / math.sqrt(6)
rng = np.random.default_rng(7)
# 6 years of daily noise, annualised Sharpe: spread 1/sqrt(6)
d = rng.standard_normal((20000, 1512))
sr = d.mean(axis=1) / d.std(axis=1, ddof=1) * math.sqrt(252)
ok(abs(sr.std() - sd6) < 0.01, f'{PID} p1: simulated Sharpe sd {sr.std()}')
numeric(3, PID, 1, sd6, 4, [0.4082], {'by-years': r(1 / 6, 4), 'inverted': r(math.sqrt(6), 4)})
ok(r(0.95 / sd6, 1) == 2.3, f'{PID} p1 explain: 2.3 sds')
ok(r(emax(4), 2) == 1.03 and r(emax(24), 2) == 1.95, f'{PID} p2: 1.03 and 1.95')
# 24 variants in 4 families that share one Sharpe: best of 24 is the best of 4
z = rng.standard_normal((200000, 4))
best24 = np.repeat(z, 6, axis=1).max(axis=1).mean()
ok(abs(best24 - emax(4)) < 0.01, f'{PID} p2: simulated best of 4 families of 6 {best24}')
p2 = numeric(3, PID, 2, 1.03 * 0.4082, 3, [0.420, 0.421], {'twenty-four': r(1.95 * 0.4082, 3), 'by-years': r(1.03 / 6, 4)})
has(p2['question'], '0.4082', f'{PID} p2 restates 0.4082')
p3 = numeric(3, PID, 3, 0.95 - 0.420, 2, [0.53], {'twenty-four': r(0.95 - 0.796, 2), 'by-years': r(0.95 - 0.172, 2)})
has(p3['question'], '0.420', f'{PID} p3 restates 0.420')
bar4 = stats.norm.isf(0.05 / 4)
ok(r(bar4, 2) == 2.24, f'{PID} p4: Bonferroni z for 4 tries {bar4}')
# finding 4: p4 is the forward step, t of the 0.95
p4 = numeric(3, PID, 4, 0.95 * math.sqrt(6), 2, [2.33, r(0.95 / 0.4082, 2)], {'times-sd': r(0.95 * 0.4082, 2), 'haircut': r(0.53 / 0.4082, 2), 'by-years': r(0.95 * 6, 2)})
has(p4['question'], '0.4082', f'{PID} p4 restates 0.4082')
ok(r(0.95 * 2.449, 2) == 2.33, f'{PID} p4 explain: t = 2.33')
p5 = choice(3, PID, 5, 'families', ['all24', 'best-only', 'real'])
ok(r(stats.norm.isf(0.05 / 24), 2) == 2.87 and r(stats.norm.isf(0.05), 2) == 1.64, f'{PID} p5: t bars 2.87 and 1.64')
ok(r(0.95 / 0.4082 - 2.24, 2) == 0.09 and 'only 0.09 over a bar built for 4 tries' in alltext(p5), f'{PID} p5: clears by 0.09')
has(p5['question'], '0.53', f'{PID} p5 restates 0.53')
has(p5['question'], '2.33', f'{PID} p5 restates 2.33')
has(p5['question'], '2.24', f'{PID} p5 restates 2.24')
ok('data the search never saw' not in alltext(it), f'{PID}: no l12 wording left')

# ---------------------------------------------------------------- p-fund-encoding
PID = 'p-fund-encoding'
it = item(3, PID)
rho = 2 / math.sqrt(15)
rng = np.random.default_rng(11)
y = rng.standard_normal((400000, 12))                       # column 0 is the own label
xenc = (2 * y[:, 0] + y[:, 1:].sum(axis=1)) / 13
rho_mc = np.corrcoef(xenc, y[:, 0])[0, 1]
ok(abs(rho_mc - rho) < 0.004, f'{PID} p1: simulated correlation {rho_mc} vs {rho}')
p1 = numeric(3, PID, 1, rho, 4, [0.5164], {'unweighted': r(1 / math.sqrt(13), 4), 'no-square': r(2 / math.sqrt(13), 4)})
w1 = (y[:, 0] + y[:, 1:].sum(axis=1)) / 13                    # own label weight 1, the 11 others as stated
rho_w1 = np.corrcoef(w1, y[:, 0])[0, 1]
ok(abs(rho_w1 - 1 / math.sqrt(12)) < 0.004, f'{PID} p1: own weight 1 with 11 others gives {rho_w1}, which is 1/sqrt(12) = 0.2887')
ok('plain mean of 13 labels' in p1['feedback']['byKey']['unweighted'] and 'weight 1,' not in p1['feedback']['byKey']['unweighted'],
   f'{PID} p1 unweighted line: 1/sqrt(13) = 0.2774 is a plain mean of 13 labels; weight 1 with the 11 others gives 1/sqrt(12) = 0.2887',
   finding=True)
ok('second time' in it['prose'] and '12 months' in it['prose'], f'{PID}: prose states the cause of the double count', finding=True)
ok('divisor of one encoding' in item(3, PID)['parts'][2]['feedback']['byKey']['category'], f'{PID} p3 category line says n = 13 is the divisor', finding=True)
slope_r2 = np.corrcoef(xenc, y[:, 0])[0, 1] ** 2
ok(abs(slope_r2 - 4 / 15) < 0.004, f'{PID} p2: simulated R squared {slope_r2}')
p2 = numeric(3, PID, 2, F(4, 15), 4, [r(0.5164 ** 2, 4)], {'rho': 0.5164, 'no-square': r(4 / 13, 4)})
has(p2['question'], '0.5164', f'{PID} p2 restates 0.5164')
t = 0.5164 * math.sqrt(98) / math.sqrt(1 - 0.5164 ** 2)
p3 = numeric(3, PID, 3, t, 2, [5.97, r(0.5164 * 9.899 / 0.8563, 2)],
             {'category': r(0.5164 * math.sqrt(11) / math.sqrt(1 - 0.5164 ** 2), 2), 'no-adjust': r(0.5164 * 9.899, 2),
              'n-not-n-minus-2': r(0.5164 * 10 / 0.8563, 2)})
has(p3['question'], '0.5164', f'{PID} p3 restates 0.5164')
ok(r(math.sqrt(98), 3) == 9.899 and r(math.sqrt(1 - 4 / 15), 4) == 0.8563, f'{PID} p3: printed roots')
ok(r(stats.norm.isf(0.05 / 40), 2) == 3.02 and r(stats.norm.isf(0.05), 2) == 1.64, f'{PID} p4: bars 3.02 and 1.64')
p4 = choice(3, PID, 4, 'leak', ['real', 'more-rows', 'one-try'])
has(p4['question'], '5.97', f'{PID} p4 restates 5.97')
# training-only encoding: no own label, correlation 0
clean = y[:, 1:].mean(axis=1)
ok(abs(np.corrcoef(clean, y[:, 0])[0, 1]) < 0.005, f'{PID}: encoding without the own label scores about 0')

# ---------------------------------------------------------------- p-spread-blocks part 3
PID = 'p-spread-blocks'
days = set(range(1, 25))
test = set(range(7, 13))
lab = lambda t: set(range(t + 1, t + 5))                     # label of day t: the next 4 days
test_lab = set().union(*(lab(t) for t in test))
ok(test_lab == set(range(8, 17)), f'{PID} p3: test labels cover days 8 to 16')
train = days - test
purged = {t for t in train if lab(t) & test_lab}
ok(purged == {4, 5, 6, 13, 14, 15}, f'{PID} p3: purged {sorted(purged)}')
after = sorted(t for t in train - purged if t > 12)[:2]
ok(after == [16, 17], f'{PID} p3: embargo days {after}')
key = len(train - purged - set(after))
before_only = train - {t for t in purged if t < 7}
before_only -= set(sorted(t for t in before_only if t > 12)[:2])
four = len(train) - 4 - 4 - 2
ok(len(before_only) == 13, f'{PID} p3: before-only is 13')
# The 24-day problem was re-authored (review-pkg3-reuse-hits fault 2); its keys are now checked in
# problems-validation-numbers.py and -read.py. The content check below runs only on the old text.
if '24 trading days' in item(2, PID)['prose']:
    numeric(2, PID, 3, key, 0, [10], {'horizon': four, 'no-embargo': len(train - purged), 'before-only': len(before_only)})

# ---------------------------------------------------------------- proposals quoted in the review
# finding 1: a 420-day bar as the last part of p-signal-break (now in the content)
ok(r(1 + 2 * 0.0690, 3) == 1.138 and r(1 + 2 * 0.1195, 3) == 1.239 and r(1 + 0.0690, 3) == 1.069 and r(1 + 2 * 0.0423, 3) == 1.085,
   'proposal: bars 1.138, 1.239, 1.069, 1.085')
ok(1.377 - 1.138 > 3 * 0.0690, 'proposal: 1.377 is more than 3 sds over the 420-day bar')
# finding 4: t of the best variant as part 4 of p-carry-lookbacks
ok(r(0.95 / 0.4082, 2) == 2.33 and r(0.95 * 2.449, 2) == 2.33 and r(0.95 * 0.4082, 2) == 0.39 and r(0.53 / 0.4082, 2) == 1.30
   and r(0.95 * 6, 2) == 5.70, 'proposal: t = 2.33; slips 0.39, 1.30, 5.70')
ok(r(stats.norm.isf(0.05 / 24), 2) == 2.87 and r(2.33 - 2.24, 2) == 0.09, 'proposal: bar 2.87 for 24 tries; margin 0.09')
# finding 8: odds wording
ok(odds_chi > 100 and odds_norm > 100, 'proposal: "less than once in 100 tries" holds on both tails')

print(f'{checks} checks, {fails} failed')
sys.exit(1 if fails else 0)
