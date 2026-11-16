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
# parts 4 and 5 re-authored in session AF; retargeted here: the fit sizes come from the counted nested run above
def curve(n):
    return 0.33 + 40 / n


sizes10 = []
Counter.log = []
cross_val_score(GridSearchCV(Counter(), grid, cv=KFold(6, shuffle=True, random_state=0), scoring='neg_mean_squared_error'), X, y,
                cv=KFold(10, shuffle=True, random_state=1), scoring='neg_mean_squared_error')
sizes10 = sorted(set(Counter.log))
ok(sizes10 == [480, 576], f'arrears: fit sizes with 10 outer folds {sizes10}')
key(1, 2, 3, curve(inner[1]) - curve(640), dp=4, also=[0.0208])
wrong(1, 2, 3, 'inner', curve(inner[0]) - curve(640), dp=4)
wrong(1, 2, 3, 'inner-outer', curve(inner[0]) - curve(inner[1]), dp=4)
wrong(1, 2, 3, 'carried', curve(640 * 5 / 6) - curve(640), dp=4)
wrong(1, 2, 3, 'level', curve(inner[1]), dp=4)
# smallest K by brute force over real outer training sizes from KFold (uneven folds included)
def worst_bias(k):
    tr = [len(t) for t, _ in KFold(k, shuffle=True, random_state=0).split(np.zeros(640))]
    return max(curve(n) - curve(640) for n in tr)
kmin = next(k for k in range(2, 50) if worst_bias(k) <= 0.007 + 1e-12)
ok(kmin == 10, f'arrears: smallest K {kmin}')
ok(abs(worst_bias(4) - 0.0208) < 5e-5, 'arrears: 0.0208 at K = 4')
key(1, 2, 4, len(Counter.log))
ok(len(Counter.log) == 10 * plain == 1090, 'arrears: ten outer folds make 1090 fits')
wrong(1, 2, 4, 'nine-folds', 9 * plain)
wrong(1, 2, 4, 'no-refits', 10 * 6 * 18)
wrong(1, 2, 4, 'added', 10 + plain)

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

# ---- p-signal-break (re-authored after the second read: fold MSEs against the working level 1.00)
mse7 = [1.02, 0.97, 1.08, 1.05, 1.31, 1.38, 1.44]
ND = 1120
bs = list(TimeSeriesSplit(n_splits=7).split(np.zeros(ND)))
BL = ND // 8
ok(all(len(te) == BL for _, te in bs) and BL == 140, 'break: equal blocks of 140')
ok(int(bs[0][1][0]) == 140 and int(bs[4][1][0]) == 700 and len(bs[4][0]) == 700 and len(bs[3][0]) == 560 and int(bs[4][1][-1]) == 839, 'break: fold 5 tests days 700 to 839 and trains on 700')
sdm = lambda n: float(stats.chi2(n).std() / n)          # sd of a mean of n squared unit normals (an MSE at sigma^2 = 1)
se = sdm(140)
ok(abs(se - sqrt(2 / 140)) < 1e-12, 'break: chi-square sd equals sigma^2 sqrt(2/n)')
key(2, 2, 0, se, dp=4)
wrong(2, 2, 0, 'no-two', 1 / sqrt(140), dp=4)
wrong(2, 2, 0, 'all-days', sdm(1120), dp=4)
z5 = (mse7[4] - 1.0) / round(se, 4)
key(2, 2, 1, round(z5, 1), also=[round((mse7[4] - 1.0) / se, 1)])
wrong(2, 2, 1, 'all-days', (mse7[4] - 1.0) / round(sdm(1120), 4), dp=1, also=[(mse7[4] - 1.0) / sdm(1120)])
wrong(2, 2, 1, 'fold-4', (mse7[4] - mse7[3]) / round(se, 4), dp=1)
wrong(2, 2, 1, 'no-two', (mse7[4] - 1.0) / round(1 / sqrt(140), 4), dp=1)
ok(stats.chi2.sf(140 * mse7[4], 140) < 0.01, f'break: an MSE of 140 normal errors reaches 1.31 less than once in 100 tries (1 in {1 / stats.chi2.sf(140 * mse7[4], 140):.0f})')
thr = 1 + 2 * se
flag = int(np.argmax(np.array(mse7) > thr)) + 1
ok(round(thr, 3) == 1.239 and flag == 5 and not any(v > thr for v in mse7[:4]), f'break: threshold {thr:.3f}, first flag fold {flag}')
key(2, 2, 2, len(bs[flag - 1][0]))
wrong(2, 2, 2, 'previous-fold', len(bs[flag - 2][0]))
wrong(2, 2, 2, 'test-end', int(bs[flag - 1][1][-1]) + 1)
wrong(2, 2, 2, 'fold-number', flag)
joined = float(np.mean(mse7[flag - 1:]))
ok(round(joined, 3) == 1.377 and ND - len(bs[flag - 1][0]) - 0 == 420, 'break: folds 5 to 7 are 420 days and join to 1.377')
z3 = (1.377 - 1.0) / sdm(420)
ok(abs(sdm(420) - 0.0690) < 5e-5, 'break: sd over 420 days is 0.0690')
key(2, 2, 3, z3, dp=1, also=[round((joined - 1.0) / sdm(420), 1)])
wrong(2, 2, 3, 'per-fold', 0.377 / round(se, 4), dp=1)
wrong(2, 2, 3, 'all-days', 0.377 / sdm(1120), dp=1)
key(2, 2, 4, 1 + 2 * sdm(420), dp=3, also=[round(1 + 2 * 0.0690, 3)])
wrong(2, 2, 4, 'per-fold', 1 + 2 * round(se, 4), dp=3)
wrong(2, 2, 4, 'one-sd', 1 + sdm(420), dp=3, also=[round(1 + 0.0690, 3)])
wrong(2, 2, 4, 'all-days', 1 + 2 * sdm(1120), dp=3, also=[round(1 + 2 * 0.0423, 3)])
ok(joined > 1 + 2 * sdm(420), 'break: the joined 1.377 is above the 2-sd level 1.138')
# claim: a least-squares fit over 700 days of slope +b and 420 of slope -b keeps the old sign
slopes = []
for _ in range(400):
    xs = rng.normal(size=1120)
    ys = np.where(np.arange(1120) < 700, 1, -1) * 0.3 * xs + rng.normal(size=1120)
    slopes.append(np.polyfit(xs, ys, 1)[0])
ok(np.mean(slopes) > 0 and abs(np.mean(slopes) - 0.3 * (700 - 420) / 1120) < 0.01, 'break: on average a full-history fit keeps the old sign')

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
wrong(2, 3, 2, 'before-only', 18 - 3 - 2)  # purge before only, embargo kept: 13
key(2, 3, 3, 4.62 / 3.85 - 1, also=[20.0, 20])
wrong(2, 3, 3, 'by-purged', 100 * (4.62 - 3.85) / 4.62, dp=1)

# ================================================================ problems-3
# ---- p-fund-flows (re-authored: the spread, not the mean)
import pandas as pd
import sympy as sp
flow = np.array([12, 15, 11, 14, 13, 16, 12, 15, 14, 13, 17, 16, 20, 22, 18, 24], float)
ok(flow[:12].sum() == 168 and flow[12:].sum() == 84 and flow.sum() == 252 and (flow[:12] - 14).__pow__(2).sum() == 38, 'flows: 168, 84, 252 and squares 38')
sa, st = pd.Series(flow), pd.Series(flow[:12])
sd_all, sd_tr = float(sa.std(ddof=0)), float(st.std(ddof=0))
ok(sa.mean() == 15.75 and st.mean() == 14 and abs(sa.var(ddof=0) - 12.8125) < 1e-12, 'flows: means 15.75 and 14, variance 12.8125')
key(3, 0, 0, sd_all, dp=3, also=[3.580])
wrong(3, 0, 0, 'train', sd_tr, dp=3)
wrong(3, 0, 0, 'ddof-one', float(sa.std(ddof=1)), dp=3)
wrong(3, 0, 0, 'variance', float(sa.var(ddof=0)), dp=3, also=[12.813])
key(3, 0, 1, sd_tr, dp=3, also=[1.779])
wrong(3, 0, 1, 'all', sd_all, dp=3)
wrong(3, 0, 1, 'ddof-one', float(st.std(ddof=1)), dp=3)
wrong(3, 0, 1, 'variance', float(st.var(ddof=0)), dp=3)
key(3, 0, 2, (20 - 14) / sd_tr, dp=2, also=[round(6 / 1.780, 2)])
wrong(3, 0, 2, 'leaky', (20 - sa.mean()) / sd_all, dp=2, also=[round(4.25 / 3.58, 2)])
wrong(3, 0, 2, 'mixed', (20 - 14) / sd_all, dp=2)
wrong(3, 0, 2, 'mean-only', (20 - sa.mean()) / sd_tr, dp=2)
zc, zl = (flow[12:] - 14) / sd_tr, (flow[12:] - sa.mean()) / sd_all
ok([round(float(v), 2) for v in zc] == [3.37, 4.5, 2.25, 5.62] and round(float(zl.max()), 2) == 2.30, f'flows: unrounded z values {zc} {zl}')
ok([round(d / 1.780, 2) for d in (6, 8, 4, 10)] == [3.37, 4.49, 2.25, 5.62] and round(8.25 / 3.579, 2) == 2.31 and zl.max() < 2.31, 'flows: with the printed 1.780 the z values are 3.37, 4.49, 2.25, 5.62; the leaky scaler tops out below 2.31')
key(3, 0, 3, int((np.abs(zc) > 3).sum()))
wrong(3, 0, 3, 'leaky', int((np.abs(zl) > 3).sum()))
wrong(3, 0, 3, 'all', 4)
choice(3, 0, 4, 'train-fit')

# ---- p-fund-encoding (task changed: weighted own label, R squared and the t of the fit)
rho = sp.Rational(2, 13) / sp.sqrt(sp.Rational(15, 169))      # covariance over the product of the sds, from the weights
ok(sp.simplify(rho - 2 / sp.sqrt(15)) == 0, 'encoding: rho = 2/sqrt(15)')
Wm = np.array([2] + [1] * 11) / 13
sim_x = rng.normal(size=(300000, 12))
ok(abs(np.corrcoef(sim_x @ Wm, sim_x[:, 0])[0, 1] - float(rho)) < 0.005, 'encoding: simulated correlation of the weighted average with its own label')
key(3, 1, 0, float(rho), dp=4)
wrong(3, 1, 0, 'unweighted', (1 / 13) / sqrt(13 / 169), dp=4)
wrong(3, 1, 0, 'no-square', (2 / 13) / sqrt(13 / 169), dp=4)
key(3, 1, 1, float(rho ** 2), dp=4, also=[round(0.5164 ** 2, 4)])
ok(rho ** 2 == sp.Rational(4, 15), 'encoding: R squared is exactly 4/15')
wrong(3, 1, 1, 'rho', float(rho), dp=4)
wrong(3, 1, 1, 'no-square', (2 / sqrt(13)) ** 2, dp=4)
# t of a fit with exactly this correlation on 100 rows, read from scipy's p-value
xr = rng.normal(size=100)
xr = (xr - xr.mean()) / xr.std()
zr = rng.normal(size=100)
zr -= zr.mean()
zr -= (zr @ xr) / (xr @ xr) * xr
zr /= zr.std()
yr = float(rho) * xr + sqrt(1 - float(rho) ** 2) * zr
lr = stats.linregress(xr, yr)
ok(abs(lr.rvalue - float(rho)) < 1e-9, 'encoding: constructed sample has correlation rho')
t_fit = float(stats.t.isf(lr.pvalue / 2, 98))
key(3, 1, 2, t_fit, dp=2, also=[round(0.5164 * sqrt(98 / (1 - 0.5164 ** 2)), 2)])
wrong(3, 1, 2, 'category', float(rho) * sqrt(11 / (1 - float(rho) ** 2)), dp=2)
wrong(3, 1, 2, 'no-adjust', float(rho) * sqrt(98), dp=2)
wrong(3, 1, 2, 'n-not-n-minus-2', float(rho) * sqrt(100 / (1 - float(rho) ** 2)), dp=2)
b40 = stats.norm.ppf(1 - 0.05 / 40)
ok(round(b40, 2) == 3.02 and t_fit > b40, f'encoding: Bonferroni bar for 40 is {b40}')
ok(abs(stats.norm.ppf(0.95) - 1.645) < 0.001, 'encoding: one try, about 1.64')
choice(3, 1, 3, 'leak')

# ---- p-closed-funds (re-authored: bonds, the average issue, then the haircut of the log's count)
rets = pd.Series([9.2] * 164 + [9.2 - 14.0] * 36)          # 200 issues, 36 of them defaulted
ok(len(rets) == 200 and abs(rets.mean() - 6.68) < 1e-12, 'closed: the 200 issues average 6.68')
# part 1 inverts the step: the file's 6.68 over 200 issues and 9.2 over the 164 survivors give the defaulted issues' mean
d_mean = (200 * 6.68 - 164 * 9.2) / 36
ok(abs(d_mean - (-4.8)) < 1e-9, 'closed: the 36 defaulted issues average -4.8')
key(3, 2, 0, 9.2 - d_mean, dp=1)
wrong(3, 2, 0, 'gap', 9.2 - 6.68, dp=2)
wrong(3, 2, 0, 'times', (9.2 - 6.68) * 0.18, dp=2)
wrong(3, 2, 0, 'stayers', (9.2 - 6.68) / 0.82, dp=2)
overstate = 9.2 - float(rets.mean())
honest = (8.4 - overstate) / 9
key(3, 2, 1, honest, dp=3)
wrong(3, 2, 1, 'survivors', 8.4 / 9, dp=3)
wrong(3, 2, 1, 'added', (8.4 + overstate) / 9, dp=3)
wrong(3, 2, 1, 'whole-gap', (8.4 - 14.0) / 9, dp=3)
ok([round(emax(k), 2) for k in (5, 12)] == [1.16, 1.63], f'closed: mean best of 5 and 12 {[emax(k) for k in (5, 12)]}')
sr = rng.normal(size=(100000, 12, 7)).mean(axis=2).max(axis=1)
ok(abs(sr.mean() - 1.63 / sqrt(7)) < 0.006, f'closed: simulated best Sharpe of 12 noise screens over 7 years {sr.mean()}')
key(3, 2, 2, 1.63 / sqrt(7), dp=3, also=[round(emax(12) / sqrt(7), 3)])
wrong(3, 2, 2, 'note', 1.16 / sqrt(7), dp=3)
wrong(3, 2, 2, 'by-years', 1.63 / 7, dp=3)
key(3, 2, 3, honest - 1.63 / sqrt(7), dp=2, also=[round(0.653 - 0.616, 2)])
wrong(3, 2, 3, 'note', honest - 1.16 / sqrt(7), dp=2, also=[0.22])
wrong(3, 2, 3, 'survivors', 8.4 / 9 - 1.63 / sqrt(7), dp=2, also=[round(0.933 - 0.616, 2)])
ok(round(8.4 / 9, 2) == 0.93 and 200 * 18 // 100 == 36, 'closed: 0.93 and 36 defaults')
choice(3, 2, 4, 'tiny')

# ---- p-carry-lookbacks (re-authored: 24 variants in 4 families)
shr = rng.normal(size=(20000, 1512))
ok(abs((shr.mean(axis=1) / shr.std(axis=1) * sqrt(252)).std() - 1 / sqrt(6)) < 0.01, 'carry: simulated sd of a 6-year Sharpe')
key(3, 3, 0, 1 / sqrt(6), dp=4)
wrong(3, 3, 0, 'by-years', 1 / 6, dp=4)
wrong(3, 3, 0, 'inverted', sqrt(6), dp=4)
ok([round(emax(k), 2) for k in (4, 24)] == [1.03, 1.95], f'carry: mean best of 4 and 24 {[emax(k) for k in (4, 24)]}')
fam = np.repeat(rng.normal(size=(200000, 4)), 6, axis=1)        # 4 families of 6 identical variants
ok(abs(fam.max(axis=1).mean() - emax(4)) < 0.01 and fam.shape[1] == 24, 'carry: the best of 24 variants in 4 families is the best of 4')
key(3, 3, 1, emax(4) / sqrt(6), dp=3, also=[round(1.03 * 0.4082, 3)])
wrong(3, 3, 1, 'twenty-four', 1.95 / sqrt(6), dp=3)
wrong(3, 3, 1, 'by-years', 1.03 / 6, dp=3)
key(3, 3, 2, 0.95 - emax(4) / sqrt(6), dp=2, also=[round(0.95 - 0.420, 2)])
wrong(3, 3, 2, 'twenty-four', 0.95 - 1.95 / sqrt(6), dp=2)
wrong(3, 3, 2, 'by-years', 0.95 - 1.03 / 6, dp=2)
b4 = stats.norm.isf(0.05 / 4)
ok(round(b4, 2) == 2.24, f'carry: Bonferroni bar for 4 is {b4}')
sd6 = 1 / sqrt(6)
key(3, 3, 3, 0.95 / sd6, dp=2, also=[round(0.95 / 0.4082, 2)])
wrong(3, 3, 3, 'times-sd', 0.95 * sd6, dp=2, also=[round(0.95 * 0.4082, 2)])
wrong(3, 3, 3, 'haircut', (0.95 - 1.03 * sd6) / sd6, dp=2, also=[round(0.53 / 0.4082, 2)])
wrong(3, 3, 3, 'by-years', 0.95 * 6, dp=2)
ok(abs(0.95 * sqrt(6) - 2.33) < 0.005 and 0.95 * sqrt(6) > b4 and abs(0.95 * sqrt(6) - 2.3) < 0.03, 'carry: t = 2.33 clears 2.24, and 0.95 is 2.3 sds out')
ok(round(stats.norm.isf(0.05 / 24), 2) == 2.87 and round(stats.norm.isf(0.05), 2) == 1.64 and round(0.95 / 0.4082 - 2.24, 2) == 0.09, 'carry: t bars 2.87 for 24 tries and 1.64 for one; 2.33 clears 2.24 by 0.09')
choice(3, 3, 4, 'families')

# every numeric wrong entry of every part was rebuilt above
seen_wrong = sum(len(p['widget'].get('wrong', [])) for s in SETS.values() for it in s['items'] for p in it['parts'] if p['widget']['kind'] == 'numeric')
ok(len(REBUILT) == seen_wrong, f'{len(REBUILT)} wrong entries rebuilt of {seen_wrong}')
print(f'{checks - fails} of {checks} checks passed; {seen_wrong} numeric wrong entries in the three sets')
sys.exit(1 if fails else 0)
