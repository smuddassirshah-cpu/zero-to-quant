#!/usr/bin/env python3
"""Second reader's recompute of validation problems-1 to -3.

Imports nothing from the author's script. Every key is rebuilt from the prose by a
route other than the feedback's arithmetic where one exists: scikit-learn's own
splitters, a counting estimator inside a real nested grid search, brute sets of days,
scipy distributions, numerical integration and seeded simulation. Then every `wrong`
value is rebuilt from the slip its line names, and every band is tested with the
engine's rule (|v - key| <= abs + 1e-9; a `%` field divides the typed figure by 100).

Run: <scratch>/venv/bin/python docs/reports/problems-validation-numbers-read.py
Exit 0 when the content is right. Paths resolve from __file__.
"""
import json
import math
import os
import sys
from fractions import Fraction as F
from math import comb, sqrt, log, acos, asin, pi

import numpy as np
from scipy import stats, integrate

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'validation')
SETS = {n: json.load(open(os.path.join(COURSE, f'problems-{n}.json'))) for n in (1, 2, 3)}

checks = fails = 0
REBUILT = set()


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def W(n, item, part):
    it = SETS[n]['items'][item]
    return it['parts'][part]['widget'], f"problems-{n} {it['id']} parts[{part}]"


def within(v, a, tol):
    return abs(v - a) <= tol.get('abs', 0) + 1e-9


def typed(w, figure):
    """What the engine compares when the learner types `figure`."""
    return figure / 100 if w.get('unit') == '%' else figure


def key(n, item, part, true, dp=None, also=()):
    """The key equals my value; the stated rounding of it, and each figure in `also`
    (the value a learner gets from the restated rounded input), is accepted."""
    w, where = W(n, item, part)
    scale = 100 if w.get('unit') == '%' else 1
    ok(within(w['answer'], true, {'abs': max(w['tol'].get('abs', 0), 1e-9)}), f'{where}: key {w["answer"]} vs mine {true}')
    figs = [true * scale] if dp is None else [round(true * scale, dp)]
    for f in list(figs) + list(also):
        ok(within(typed(w, f), w['answer'], w['tol']), f'{where}: typed {f} refused by key band')
    return w, where


def wrong(n, item, part, wid, slip, dp=None, also=()):
    """`slip` is the figure the named slip gives, as typed. It must miss the key band,
    fall in its own band (also when rounded as the question asks), and in no earlier band."""
    w, where = W(n, item, part)
    entry = next((x for x in w.get('wrong', []) if x['id'] == wid), None)
    ok(entry is not None, f'{where}: wrong id {wid} missing')
    if entry is None:
        return
    REBUILT.add((n, item, part, wid))
    figs = [slip] + ([round(slip, dp)] if dp is not None else []) + list(also)
    for f in figs:
        v = typed(w, f)
        ok(not within(v, w['answer'], w['tol']), f'{where}: slip {wid} typed {f} graded right')
        first = next((x['id'] for x in w['wrong'] if within(v, x['value'], x.get('tol', {'abs': 1e-9}))), None)
        ok(first == wid, f'{where}: slip {wid} typed {f} routed to {first}')


def all_wrong_covered(n, item, part, ids):
    w, where = W(n, item, part)
    ok(sorted(x['id'] for x in w.get('wrong', [])) == sorted(ids), f'{where}: wrong ids {[x["id"] for x in w.get("wrong", [])]} not all rebuilt')


def choice(n, item, part, correct_id):
    w, where = W(n, item, part)
    right = [o['id'] for o in w['options'] if o.get('correct')]
    ok(right == [correct_id], f'{where}: correct option {right}')


def emax(N):
    """Mean of the largest of N standard normals, by integration."""
    f = lambda x: x * N * stats.norm.pdf(x) * stats.norm.cdf(x) ** (N - 1)
    return integrate.quad(f, -12, 12, epsabs=1e-12)[0]


rng = np.random.default_rng(20261116)

# ---------------------------------------------------------------- set shape
LESSONS = {1: 'l1 l2 l3 l4', 2: 'l5 l6 l7 l8', 3: 'l9 l10 l11 l12'}
course = json.load(open(os.path.join(COURSE, 'course.json')))
for n, s in SETS.items():
    ok(3 <= len(s['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in s['items']), f'problems-{n}: no difficulty 5')
    parts = [p for it in s['items'] for p in it['parts']]
    typed_n = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(typed_n * 3 >= 2 * len(parts), f'problems-{n}: typed share {typed_n}/{len(parts)}')
    for it in s['items']:
        ok(3 <= len(it['parts']) <= 5 and 3 <= it['difficulty'] <= 5, f'problems-{n} {it["id"]}: shape')
        ok(all(k in course['skills'] for k in it['skills']), f'problems-{n} {it["id"]}: skills')
        for j, p in enumerate(it['parts']):
            w = p['widget']
            if w['kind'] != 'numeric':
                continue
            bands = [(w['answer'], w['tol'].get('abs', 0), 'key')] + [(x['value'], x['tol'].get('abs', 0), x['id']) for x in w.get('wrong', [])]
            for a in range(len(bands)):
                for b in range(a + 1, len(bands)):
                    gap = abs(bands[a][0] - bands[b][0]) - bands[a][1] - bands[b][1]
                    ok(gap > 1e-9, f'problems-{n} {it["id"]} parts[{j}]: bands {bands[a][2]} and {bands[b][2]} touch')

# ================================================================ problems-1
# ---- p-flood-claims
s2 = 0.36
n_need = next(n for n in range(1, 5000) if s2 * sqrt(2 / n) <= 0.03 + 1e-12)
key(1, 0, 0, n_need)
ok(abs(np.std((rng.normal(0, 0.6, (20000, 288)) ** 2).mean(axis=1)) - 0.03) < 0.001, 'flood: simulated sd of a 288-claim MSE is 0.03')
wrong(1, 0, 0, 'unsquared', 0.36 * 2 / 0.0009)
wrong(1, 0, 0, 'no-two', 0.36 ** 2 / 0.03 ** 2)
all_wrong_covered(1, 0, 0, ['unsquared', 'no-two'])
rest = 1152 - n_need
key(1, 0, 1, rest * F(3, 4))
wrong(1, 0, 1, 'validation', rest / 4)
wrong(1, 0, 1, 'all-rest', rest)
all_wrong_covered(1, 0, 1, ['validation', 'all-rest'])
from sklearn.model_selection import KFold, TimeSeriesSplit, GridSearchCV, cross_val_score
from sklearn.base import BaseEstimator, RegressorMixin
sizes = {(len(tr), len(te)) for tr, te in KFold(4, shuffle=True, random_state=0).split(np.zeros(1152))}
ok(sizes == {(864, 288)}, 'flood: KFold(4) sizes')
key(1, 0, 2, 864)
wrong(1, 0, 2, 'test-fold', 288)
wrong(1, 0, 2, 'all', 1152)
p1 = stats.hypergeom.pmf(0, 1152, 12, 288)
ok(abs(p1 - float(F(comb(864, 12), comb(1152, 12)))) < 1e-12, 'flood: hypergeometric two ways')
prod = 1.0
for i in range(12):
    prod *= (864 - i) / (1152 - i)
ok(abs(prod - p1) < 1e-12 and round(p1, 4) == 0.0311, 'flood: product 864/1152 ... 853/1141 is 0.0311')
ok((864 - 11, 1152 - 11) == (853, 1141), 'flood: last factor 853/1141')
key(1, 0, 3, p1, dp=4)
wrong(1, 0, 3, 'independent', 0.75 ** 12, dp=4)
ok(0.75 ** 12 > p1, 'flood: without replacement is a little smaller')
pj = [float(F(comb(1152 - 288 * j, 12), comb(1152, 12))) for j in range(5)]
ok(round(pj[2], 5) == 0.00023, f'flood: pair chance {pj[2]} printed as 0.00023')
exact = 4 * pj[1] - 6 * pj[2] + 4 * pj[3]
ok(pj[3] < 1e-6, 'flood: three-fold term negligible')
# simulation of "some fold of four holds none of 12"
T = 200000
hits = 0
for _ in range(40):
    r = rng.random((5000, 1152)).argpartition(12, axis=1)[:, :12] // 288
    occ = np.zeros((5000, 4), bool)
    for f in range(4):
        occ[:, f] = (r == f).any(axis=1)
    hits += (~occ).any(axis=1).sum()
ok(abs(hits / T - exact) < 0.003, f'flood: simulated {hits / T} against exact {exact}')
key(1, 0, 4, exact, dp=3, also=[4 * 0.0311 - 6 * 0.00023, round(4 * 0.0311 - 6 * 0.00023, 3)])
ok(abs(1 / exact - 8) < 0.2, 'flood: about one run in eight')
wrong(1, 0, 4, 'union', 4 * 0.0311, dp=3)
wrong(1, 0, 4, 'independent-folds', 1 - (1 - 0.0311) ** 4, dp=3)
wrong(1, 0, 4, 'carried', 4 * 0.0317 - 6 * 0.00023, dp=3)
all_wrong_covered(1, 0, 4, ['union', 'independent-folds', 'carried'])

# ---- p-van-prices
folds = [1.84, 2.11, 1.97, 2.26, 1.92]
ok((1430 - 290, 1140 % 5) == (1140, 0), 'vans: 1,140 left, folds of 228')
m = float(np.mean(folds))
key(1, 1, 0, sum(F(str(x)) for x in folds) / 5, dp=2)
wrong(1, 1, 0, 'median', float(np.median(folds)))
wrong(1, 1, 0, 'by-four', 10.10 / 4, dp=2, also=[2.53])
ok(max(folds) == folds[3], 'vans: fold 4 is the odd one out')
devs = [round(x - 2.02, 2) for x in folds]
ok(devs == [-0.18, 0.09, -0.05, 0.24, -0.10], 'vans: deviations')
ok(abs(sum(d * d for d in devs) - 0.1106) < 1e-12, 'vans: squares add to 0.1106')
sd = float(np.std(folds))
import statistics
ok(abs(sd - statistics.pstdev(folds)) < 1e-12, 'vans: np.std is the population sd')
key(1, 1, 1, sd, dp=3)
wrong(1, 1, 1, 'ddof-one', float(np.std(folds, ddof=1)), dp=3)
wrong(1, 1, 1, 'variance', float(np.var(folds)), dp=3)
limit = 2.02 + 0.149
key(1, 1, 2, limit, dp=3, also=[round(m + sd, 3)])
wrong(1, 1, 2, 'ddof-limit', 2.02 + 0.166, dp=3, also=[round(m + float(np.std(folds, ddof=1)), 3)])
wrong(1, 1, 2, 'se', 2.02 + 0.149 / sqrt(5), dp=3)
means = {0.3: 2.05, 1: 2.03, 3: 2.02, 10: 2.12, 30: 2.18, 100: 2.31}
ok(min(means, key=means.get) == 3, 'vans: alpha 3 has the lowest mean')
pick = max(a for a, v in means.items() if v <= limit)
key(1, 1, 3, pick)
wrong(1, 1, 3, 'best', min(means, key=means.get))
wrong(1, 1, 3, 'carried', max(a for a, v in means.items() if v <= 2.186))
ok(sorted(v for v in means.values() if v <= limit) == [2.02, 2.03, 2.05, 2.12], 'vans: four means under the limit')
key(1, 1, 4, sqrt(2.25) * 1000, dp=-1)
wrong(1, 1, 4, 'mse-as-price', 2.25 * 1000)
wrong(1, 1, 4, 'cv-mean', sqrt(2.12) * 1000, dp=-1)

# ---- p-arrears-grid: count the fits of a real nested search
class Counter(BaseEstimator, RegressorMixin):
    log = []

    def __init__(self, degree=1, alpha=1.0):
        self.degree = degree
        self.alpha = alpha

    def fit(self, X, y):
        Counter.log.append(len(y))
        return self

    def predict(self, X):
        return np.zeros(len(X))


X = rng.normal(size=(640, 2))
y = rng.normal(size=640)
grid = {'degree': [1, 2, 3], 'alpha': [0.01, 0.1, 1, 10, 100, 1000]}
Counter.log = []
GridSearchCV(Counter(), grid, cv=KFold(6, shuffle=True, random_state=0), scoring='neg_mean_squared_error').fit(X, y)
plain = len(Counter.log)
key(1, 2, 0, plain)
wrong(1, 2, 0, 'no-refit', 6 * 18)
wrong(1, 2, 0, 'one-knob', 6 * 6 + 1)
Counter.log = []
cross_val_score(GridSearchCV(Counter(), grid, cv=KFold(6, shuffle=True, random_state=0), scoring='neg_mean_squared_error'), X, y,
                cv=KFold(4, shuffle=True, random_state=1), scoring='neg_mean_squared_error')
key(1, 2, 1, len(Counter.log))
ok(len(Counter.log) == 4 * plain, 'arrears: nested is four times the plain search')
wrong(1, 2, 1, 'no-refits', 4 * 6 * 18)
wrong(1, 2, 1, 'added', 4 + 109)
inner = sorted(set(Counter.log))
ok(inner == [400, 480], f'arrears: fit sizes of the nested run {inner}')
key(1, 2, 2, inner[0])
wrong(1, 2, 2, 'outer', inner[1])
wrong(1, 2, 2, 'all-inner', 640 * 5 / 6, dp=2)
ok((480 // 6, 640 // 4) == (80, 160), 'arrears: inner folds of 80, outer fold of 160')
key(1, 2, 3, (0.451 - 0.412) / 0.451, dp=None, also=[8.6, 8.65])
w, where = W(1, 2, 3)
ok(within(0.086, w['answer'], w['tol']), f'{where}: 8.6 accepted')
wrong(1, 2, 3, 'by-inner', 100 * 0.039 / 0.412, dp=1)
wrong(1, 2, 3, 'gap', 3.9)
choice(1, 2, 4, 'nested')
ok(abs((0.412 + 0.451) / 2 - 0.4315) < 1e-12, 'arrears: mean of the two is 0.4315')

# ---- p-rent-seeds
sd1 = 0.81 * sqrt(2 / 600)
chi = stats.chi2(600)
ok(abs(0.81 * chi.std() / 600 - sd1) < 1e-12, 'rents: sd of a 600-flat MSE from the chi-square')
key(1, 3, 0, sd1, dp=4)
wrong(1, 3, 0, 'all-flats', 0.81 * sqrt(2 / 3000), dp=4)
wrong(1, 3, 0, 'sigma', 0.9 * sqrt(2 / 600), dp=4)
wrong(1, 3, 0, 'no-two', 0.81 * sqrt(1 / 600), dp=4)
ok(round(sqrt(2 / 600), 4) == 0.0577, 'rents: root is 0.0577')
e16 = emax(16)
ok(round(e16, 3) == 1.766, f'rents: mean least of 16 normals {e16}')
best = 0.81 - 1.766 * 0.0468
key(1, 3, 1, best, dp=3, also=[round(0.81 - e16 * sd1, 3)])
ok(round(0.81 - best, 3) == 0.083, 'rents: about 0.083 below')
fb = SETS[1]['items'][3]['parts'][1]['feedback']['correct']
ok(f'{1.766 * 0.0468:.4f}' in fb, f'rents parts[1] feedback prints 0.0827; 1.766 x 0.0468 = {1.766 * 0.0468:.4f} (review finding 1)')
wrong(1, 3, 1, 'worst', 0.81 + 1.766 * 0.0468, dp=3)
wrong(1, 3, 1, 'carried', 0.81 - 1.766 * 0.0209, dp=3)
share = (0.81 - 0.727) / 0.81
key(1, 3, 2, share, also=[10.2, round(100 * (0.81 - best) / 0.81, 1)])
wrong(1, 3, 2, 'by-best', 100 * 0.083 / 0.727, dp=1)
wrong(1, 3, 2, 'gap', 8.3)
n4 = next(n for n in range(1, 10000) if 1.766 * sqrt(2 / n) < 0.04)
key(1, 3, 3, n4)
ok(abs(2 * (1.766 / 0.04) ** 2 - 3898.4) < 0.05 and round((1.766 / 0.04) ** 2, 1) == 1949.2 and n4 > 3000, 'rents: 3898.4, more than 3,000')
wrong(1, 3, 3, 'no-two', math.ceil((1.766 / 0.04) ** 2))
wrong(1, 3, 3, 'unsquared', math.ceil(2 * 1.766 / 0.04))

# ================================================================ problems-2
# ---- p-gas-demand
x = np.array([2, 4, 8, 9, 10, 9], float)
from statsmodels.tsa.stattools import acf
r1 = acf(x, nlags=1, fft=False)[1]
d = x - x.mean()
ok(x.mean() == 7 and list(d) == [-5, -3, 1, 2, 3, 2], 'gas: mean and deviations')
ok(list(d[:-1] * d[1:]) == [15, -3, 2, 6, 6] and (d[:-1] * d[1:]).sum() == 26 and (d * d).sum() == 52, 'gas: 26 over 52')
key(2, 0, 0, r1)
wrong(2, 0, 0, 'pearson', float(np.corrcoef(x[:-1], x[1:])[0, 1]), dp=3)
wrong(2, 0, 0, 'averaged', (26 / 5) / (52 / 6))
splits = list(TimeSeriesSplit(n_splits=6).split(np.zeros(1400)))
ok(all(len(te) == 200 for _, te in splits) and splits[0][1][0] == 200 and splits[-1][1][0] == 1200, 'gas: blocks of 200 from day 200, last from 1,200')
ok(len(splits[0][0]) == 200, 'gas: fold 1 trains on 200')
key(2, 0, 1, len(splits[-1][0]))
wrong(2, 0, 1, 'block', 200)
wrong(2, 0, 1, 'six-pieces', 1400 - 1400 // 6)
blocks = [5.2, 4.6, 4.4, 4.9, 6.1, 5.6]
errs = np.concatenate([np.full(200, b) for b in blocks] + [np.full(75, 8.0)])
ok(len(errs) == 1275 and abs(errs.sum() - 6760) < 1e-6 and abs(sum(blocks) - 30.8) < 1e-9, 'gas: 1,275 days, total 6,760')
key(2, 0, 2, float(errs.mean()), dp=2)
wrong(2, 0, 2, 'seven-mean', (sum(blocks) + 8.0) / 7, dp=2)
wrong(2, 0, 2, 'six-only', sum(blocks) / 6, dp=2)
key(2, 0, 3, 5.30 / 2.12, dp=2, also=[round(float(errs.mean()) / 2.12, 2)])
wrong(2, 0, 3, 'inverted', 2.12 / 5.30, dp=2)
wrong(2, 0, 3, 'carried', 5.54 / 2.12, dp=2, also=[round((sum(blocks) + 8) / 7 / 2.12, 2)])
wrong(2, 0, 3, 'difference', 5.30 - 2.12, dp=2)

# ---- p-forward-label: brute sets of days
N, h, L = 1260, 15, 30
ok(N / 9 == 140, 'label: nine blocks of 140')
label = lambda t: set(range(t + 1, t + h + 1))
feat = lambda t: set(range(t - L + 1, t + 1))
s, e = 560, 700
test_rows = range(s, e)
test_labels = set().union(*(label(t) for t in test_rows))
before = [t for t in range(0, s) if label(t) & test_labels]
after = [t for t in range(e, N) if label(t) & test_labels]
ok(before == list(range(s - 14, s)) and after == list(range(e, e + 14)), 'label: 14 rows overlap on each side')
key(2, 1, 0, len(before))
wrong(2, 1, 0, 'horizon', h)
wrong(2, 1, 0, 'both-sides', len(before) + len(after))
ok(len(label(s - 1) & label(s)) == 14 and max(label(s - 15)) == s and min(label(s)) == s + 1, 'label: row s-1 shares 14 days; row s-15 stops at day s')
touched = [t for t in range(e, N) if feat(t) & set(test_rows)]
ok(touched == list(range(e, e + 29)) and min(feat(e + 28)) == e - 1 and min(feat(e + 29)) == e, 'label: rows e to e+28 average a test day')
key(2, 1, 1, len(touched))
wrong(2, 1, 1, 'window', L)
wrong(2, 1, 1, 'none', 0)
# the lesson's rule (l7): drop from s - (h-1) up to, not including, e + (h-1) + embargo
train = [t for t in range(N) if not (s - (h - 1) <= t < e + (h - 1) + 29)]
key(2, 1, 2, len(train))
wrong(2, 1, 2, 'no-embargo', N - 140 - 28)
wrong(2, 1, 2, 'horizon', N - 140 - 30 - 29)
wrong(2, 1, 2, 'block-only', N - 140)
ok(N - 140 - len(train) == 57 and 0.155 < (N - len(train)) / N < 0.16, 'label: 57 rows beyond the block, nearly 16% out')
# the rows the stacked embargo removes that part 2's own count calls clean (finding)
clean_lost = [t for t in range(e + 14, e + 14 + 29) if t not in touched]
print(f'NOTE label: the stacked 29-row embargo removes {len(clean_lost)} rows (e+29 to e+42) that part 2 counts as clean; 15 more rows after the purge clear every touched row')
ok(len(clean_lost) == 14, 'label: 14 clean rows inside the stacked embargo')
ws = list(TimeSeriesSplit(n_splits=8, test_size=140, gap=14).split(np.zeros(N)))
ok(ws[0][1][0] == 140 and ws[-1][1][0] == 1120, 'label: fold 1 tests from 140, fold 8 from 1,120')
key(2, 1, 3, int(ws[0][0][-1]))
wrong(2, 1, 3, 'no-gap', 139)
wrong(2, 1, 3, 'horizon-gap', 139 - 15)
wrong(2, 1, 3, 'embargo', 125 - 29)
ok(not (label(125) & set().union(*(label(t) for t in ws[0][1]))), 'label: day 125 does not overlap fold 1 labels')
key(2, 1, 4, len(ws[-1][0]))
wrong(2, 1, 4, 'no-gap', 1120)
wrong(2, 1, 4, 'embargo', 1106 - 29)
wrong(2, 1, 4, 'last-day', int(ws[-1][0][-1]))
ok(len(ws[-1][0]) - len(train) == 43, 'label: 43 more than the purged middle block')

# ---- p-signal-break
hits7 = [0.585, 0.565, 0.605, 0.575, 0.490, 0.470, 0.455]
import re
ND = int(re.search(r'over ([\d,]+) days', SETS[2]['items'][2]['prose']).group(1).replace(',', ''))  # 1,600 as written; 1,440 after the fix of finding 7
bs = list(TimeSeriesSplit(n_splits=7).split(np.zeros(ND)))
BL = ND // 8
ok(all(len(te) == BL for _, te in bs), 'break: equal blocks')
f5 = (int(bs[4][1][0]), int(bs[4][1][-1]))
ok(f'{f5[0]:,} to {f5[1]:,}' in SETS[2]['items'][2]['parts'][2]['explain']['text'], f'break: fold 5 tests days {f5}')
if f5[0] in (1000, 1100):
    print(f'NOTE break: fold 5 starts on day {f5[0]:,}, a break day l8 uses (review finding 7)')
se = float(stats.binom(BL, 0.5).std() / BL)
se4 = round(se, 4)
key(2, 2, 0, se, dp=4)
wrong(2, 2, 0, 'variance', 0.25 / BL, dp=4)
wrong(2, 2, 0, 'all-days', sqrt(0.25 / ND), dp=4)
z6 = (hits7[5] - 0.52) / se4
key(2, 2, 1, round(z6, 1), also=[round((hits7[5] - 0.52) / se, 1)])
wrong(2, 2, 1, 'sign', -round(z6, 1))
wrong(2, 2, 1, 'earlier-level', round((hits7[5] - np.mean(hits7[:4])) / se4, 1))
wrong(2, 2, 1, 'carried', round((hits7[5] - 0.52) / round(sqrt(0.25 / ND), 4), 1))
alarm = next(i + 1 for i in range(1, 7) if hits7[i] < 0.52 and hits7[i - 1] < 0.52)
key(2, 2, 2, alarm)
wrong(2, 2, 2, 'run-start', next(i + 1 for i in range(7) if hits7[i] < 0.52))
wrong(2, 2, 2, 'seventh', 7)
ok(abs(sum(hits7) - 3.745) < 1e-9, 'break: seven add to 3.745')
key(2, 2, 3, float(np.mean(hits7)), dp=3)
wrong(2, 2, 3, 'first-four', float(np.mean(hits7[:4])), dp=4)
wrong(2, 2, 3, 'last-three', float(np.mean(hits7[4:])), dp=3, also=[0.4717])
ok(all(v < 0.52 for v in hits7[4:]) and np.mean(hits7) > 0.52, 'break: last three lose, the mean wins')
choice(2, 2, 4, 'old-sign')
# claim: a least-squares fit over 1,000 days of slope +b and 600 of slope -b keeps the old sign
xs = rng.normal(size=1600)
ys = np.where(np.arange(1600) < 1000, 1, -1) * 0.1 * xs + rng.normal(size=1600)
ok(np.polyfit(xs, ys, 1)[0] > 0, 'break: a full-history fit keeps the old sign')

# ---- p-spread-blocks
days = list(range(1, 25))
shuf = [3, 8, 11, 15, 19, 24]
both = [t for t in shuf if (t - 1 in days and t - 1 not in shuf) and (t + 1 in days and t + 1 not in shuf)]
key(2, 3, 0, len(both))
ok(both == [3, 8, 11, 15, 19], 'spread: the five sandwiched days')
wrong(2, 3, 0, 'all', 6)
kf = list(KFold(4).split(np.zeros(24)))
tr2, te2 = kf[1]
ok(list(te2 + 1) == list(range(7, 13)), 'spread: fold 2 tests days 7 to 12')
later = [t for t in tr2 + 1 if t > 12]
key(2, 3, 1, len(later))
wrong(2, 3, 1, 'all-train', len(tr2))
wrong(2, 3, 1, 'one-fold', 6)
lab4 = lambda t: set(range(t + 1, t + 5))
tl = set().union(*(lab4(t) for t in range(7, 13)))
ok((min(tl), max(tl)) == (8, 16), 'spread: test labels cover days 8 to 16')
purged = [t for t in tr2 + 1 if lab4(t) & tl]
ok(purged == [4, 5, 6, 13, 14, 15], 'spread: purge drops days 4 to 6 and 13 to 15')
kept = [t for t in tr2 + 1 if t not in purged and t not in (16, 17)]
ok(kept == [1, 2, 3] + list(range(18, 25)), 'spread: days 1 to 3 and 18 to 24 are left')
key(2, 3, 2, len(kept))
wrong(2, 3, 2, 'horizon', 18 - 8 - 2)
wrong(2, 3, 2, 'no-embargo', 18 - 6)
wrong(2, 3, 2, 'before-only', 18 - 3 - 2)  # purge before only, embargo kept: 13 (the set has 15, which drops the embargo too: review finding 10)
key(2, 3, 3, 4.62 / 3.85 - 1, also=[20.0, 20])
wrong(2, 3, 3, 'by-purged', 100 * (4.62 - 3.85) / 4.62, dp=1)

# ================================================================ problems-3
# ---- p-fund-flows
flow = np.array([14, 18, 16, 21, 19, 17, 22, 20, 15, 31, 27, 32], float)
from sklearn.preprocessing import StandardScaler
ok(flow[:9].sum() == 162 and flow[9:].sum() == 90 and flow.sum() == 252 and (flow > 0).all(), 'flows: totals 162, 90, 252; all positive')
key(3, 0, 0, float(StandardScaler().fit(flow.reshape(-1, 1)).mean_[0]))
wrong(3, 0, 0, 'train', float(flow[:9].mean()))
wrong(3, 0, 0, 'test-mean', float(flow[9:].mean()))
key(3, 0, 1, float(StandardScaler().fit(flow[:9].reshape(-1, 1)).mean_[0]))
wrong(3, 0, 1, 'with-day-10', float(flow[:10].mean()), dp=1)
wrong(3, 0, 1, 'twelve', 162 / 12, dp=1)
if 'revised' in SETS[3]['items'][0]['parts'][2]['question']:
    rev = flow.copy()
    rev[11] = 50
    key(3, 0, 2, float(rev.mean() - flow.mean()), dp=1)
    ok(rev.mean() == 22.5, 'flows: revised mean 22.5')
    wrong(3, 0, 2, 'moved-value', 50 - 32)
    wrong(3, 0, 2, 'test-mean', (50 - 32) / 3)
    wrong(3, 0, 2, 'train', float(rev[:9].mean() - flow[:9].mean()))
else:  # the replacement part of finding 13: training days above the colleague's mean
    key(3, 0, 2, int((flow[:9] > 21).sum()))
    wrong(3, 0, 2, 'train-mean', int((flow[:9] > 18).sum()))
    wrong(3, 0, 2, 'at-mean', int((flow[:9] >= 21).sum()))
import pandas as pd
used = []
for dday in range(12):
    bump = flow.copy()
    bump[dday] += 1000
    if pd.Series(bump).rolling(5, center=True).mean()[8] != pd.Series(flow).rolling(5, center=True).mean()[8]:
        used.append(dday + 1)
ok(used == [7, 8, 9, 10, 11], f'flows: centred window on day 9 reads days {used}')
key(3, 0, 3, len([u for u in used if u >= 10]))
wrong(3, 0, 3, 'all-test', 3)
trail = [dd + 1 for dd in range(12) if pd.Series(np.where(np.arange(12) == dd, 1e6, flow)).rolling(5).mean()[8] != pd.Series(flow).rolling(5).mean()[8]]
wrong(3, 0, 3, 'trailing', len([u for u in trail if u >= 10]))
choice(3, 0, 4, 'log')

# ---- p-fund-encoding
rho = 1 / sqrt(49)
sim_x = rng.normal(size=(200000, 49))
avg = sim_x.mean(axis=1)
ok(abs(np.corrcoef(avg, sim_x[:, 0])[0, 1] - rho) < 0.006, 'encoding: simulated correlation of an average of 49 with one term')
key(3, 1, 0, rho, dp=4)
wrong(3, 1, 0, 'one-over-n', 1 / 49, dp=4)
hit = 0.5 + asin(0.1429) / pi
ok(abs(hit - (1 - acos(0.1429) / pi)) < 1e-12, 'encoding: 1 - arccos/pi equals 1/2 + arcsin/pi')
ok(abs(np.mean(np.sign(avg) == np.sign(sim_x[:, 0])) - hit) < 0.004, 'encoding: simulated sign agreement')
ok(round(acos(0.1429), 4) == 1.4274, 'encoding: arccos(0.1429) = 1.4274')
key(3, 1, 1, hit, dp=4, also=[round(0.5 + asin(rho) / pi, 4)])
if any(x['id'] == 'no-one' for x in W(3, 1, 1)[0]['wrong']):
    wrong(3, 1, 1, 'no-one', acos(0.1429) / pi, dp=4)
else:  # the arcsin form of finding 16
    wrong(3, 1, 1, 'no-half', asin(0.1429) / pi, dp=4)
wrong(3, 1, 1, 'carried', 1 - acos(1 / 49) / pi, dp=4, also=[round(1 - acos(0.0204) / pi, 4)])
sef = sqrt(0.25 / 1200)
ok(round(sef, 5) == 0.01443, 'encoding: standard error 0.01443')
key(3, 1, 2, (0.5456 - 0.5) / sef, dp=2, also=[round(0.0456 / 0.01443, 2), round((hit - 0.5) / sef, 2)])
wrong(3, 1, 2, 'carried' if any(x['id'] == 'carried' for x in W(3, 1, 2)[0]['wrong']) else 'sign', (0.4544 - 0.5) / sef, dp=2)
wrong(3, 1, 2, 'months', (0.5456 - 0.5) / sqrt(0.25 / 49), dp=2)
b40 = stats.norm.ppf(1 - 0.05 / 40)
ok(round(b40, 2) == 3.02 and 3.16 > b40, f'encoding: Bonferroni bar for 40 is {b40}')
ok(abs(stats.norm.ppf(0.95) - 1.645) < 0.001, 'encoding: one try, about 1.64')
choice(3, 1, 3, 'leak')

# ---- p-closed-funds
pc, gap = 0.26, 6.5
ES, EC = 9.0, 9.0 - gap  # any level: only the gap matters
bias = ES - ((1 - pc) * ES + pc * EC)
key(3, 2, 0, bias / 100, also=[1.69])
wrong(3, 2, 0, 'gap', 6.5)
wrong(3, 2, 0, 'survivor-share', 0.74 * 6.5)
key(3, 2, 1, (7.4 - 1.69) / 12, dp=3)
ok(abs(7.4 - 1.69 - 5.71) < 1e-9, 'closed: honest excess 5.71')
wrong(3, 2, 1, 'survivors', 7.4 / 12, dp=3)
wrong(3, 2, 1, 'added', (7.4 + 1.69) / 12, dp=3)
wrong(3, 2, 1, 'carried', (7.4 - 4.81) / 12, dp=3)
ok([round(emax(k), 2) for k in (4, 18, 22)] == [1.03, 1.82, 1.91], f'closed: mean best of 4, 18, 22 {[emax(k) for k in (4, 18, 22)]}')
key(3, 2, 2, 1.82 / sqrt(9), dp=3)
sr = rng.normal(size=(100000, 18, 9)).mean(axis=2).max(axis=1)
ok(abs(sr.mean() - 0.607) < 0.004, f'closed: simulated best Sharpe of 18 noise rules over 9 years {sr.mean()}')
wrong(3, 2, 2, 'wiki', 1.03 / 3, dp=3)
wrong(3, 2, 2, 'double-count', 1.91 / 3, dp=3)
wrong(3, 2, 2, 'by-years', 1.82 / 9, dp=3)
key(3, 2, 3, round(0.476 - 0.607, 2), also=[round((7.4 - 1.69) / 12 - 1.82 / 3, 2)])
wrong(3, 2, 3, 'wiki', round(0.476 - 0.343, 2))
wrong(3, 2, 3, 'clipped', 0)
wrong(3, 2, 3, 'survivors', round(0.617 - 0.607, 2))

# ---- p-carry-lookbacks
ceil60 = sqrt(2 * log(60)) / sqrt(4)
ok(round(sqrt(2 * log(60)), 3) == 2.862 and 1.48 > ceil60, 'carry: root 2.862; 1.48 clears 1.43')
key(3, 3, 0, ceil60, dp=2)
wrong(3, 3, 0, 'no-root-t', sqrt(2 * log(60)), dp=2)
wrong(3, 3, 0, 'by-years', sqrt(2 * log(60)) / 4, dp=2)
wrong(3, 3, 0, 'wiki', sqrt(2 * log(9)) / 2, dp=2)
e60 = emax(60)
ok(round(e60, 3) == 2.319, f'carry: mean best of 60 normals {e60}')
key(3, 3, 1, 1.48 - 2.319 / 2, dp=2, also=[round(1.48 - 1.16, 2)])
wrong(3, 3, 1, 'ceiling', 1.48 - 1.43, dp=2)
wrong(3, 3, 1, 'no-root', 1.48 - 2.319, dp=2)
key(3, 3, 2, sqrt(0.2) * 1.16, dp=2, also=[round(sqrt(0.2) * 2.319 / 2, 2)])
z = rng.normal(size=(200000, 1))
eps = rng.normal(size=(200000, 60))
corr_best = ((sqrt(0.8) * z + sqrt(0.2) * eps) / 2).max(axis=1).mean()
ok(abs(corr_best - 0.5188) < 0.006, f'carry: simulated mean best of 60 correlated lookbacks {corr_best}')
ok(round(1.48 - 0.52, 2) == 0.96, 'carry: about 0.96 left')
wrong(3, 3, 2, 'rho', sqrt(0.8) * 1.16, dp=2)
wrong(3, 3, 2, 'no-root', 0.2 * 1.16, dp=2)
b60 = stats.norm.ppf(1 - 0.05 / 60)
ok(round(b60, 2) == 3.14, f'carry: Bonferroni bar for 60 is {b60}')
key(3, 3, 3, 3.14 / sqrt(4), dp=2)
ok(abs(1.48 * 2 - 2.96) < 1e-9 and 2.96 < 3.14, 'carry: t = 2.96 falls short')
wrong(3, 3, 3, 'bar', 3.14)
wrong(3, 3, 3, 'by-years', 3.14 / 4, dp=2)
choice(3, 3, 4, 'locked')

# every numeric wrong entry of every part was rebuilt above
seen_wrong = sum(len(p['widget'].get('wrong', [])) for s in SETS.values() for it in s['items'] for p in it['parts'] if p['widget']['kind'] == 'numeric')
ok(len(REBUILT) == seen_wrong, f'{len(REBUILT)} wrong entries rebuilt of {seen_wrong}')
print(f'{checks - fails} of {checks} checks passed; {seen_wrong} numeric wrong entries in the three sets')
sys.exit(1 if fails else 0)
