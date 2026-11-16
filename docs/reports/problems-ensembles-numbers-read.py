#!/usr/bin/env python3
"""Second reader's recomputation of app/content/courses/ensembles/problems-1..3.json.

Imports nothing from the author's script. Every data set is typed here from the
prose. Route 1 is exact (fractions, brute force over every split). Route 2 is
another method (scikit-learn trees and boosters, a covariance matrix, a
simulation, NumPy position arithmetic). Each key, each `wrong` value and the
numbers printed in feedback and explanations are checked against the JSON.
Exit 0 on correct content.
"""
import itertools
import json
import math
import os
import sys
import warnings
from fractions import Fraction as F

import numpy as np

warnings.simplefilter('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ensembles')
SETS = {n: json.load(open(os.path.join(BASE, f'problems-{n}.json'))) for n in (1, 2, 3)}

checks = 0
fails = []


def ok(cond, label):
    global checks
    checks += 1
    if not cond:
        fails.append(label)
        print('FAIL', label)


def item(n, iid):
    for it in SETS[n]['items']:
        if it['id'] == iid:
            return it
    raise KeyError(iid)


seen_wrong = set()


def key(n, iid, k, mine, wrongs=None, says=()):
    """Part k (1-based): my value against the key, my slips against `wrong`,
    bands, and numbers the texts must print."""
    p = item(n, iid)['parts'][k - 1]
    w = p['widget']
    lab = f'problems-{n} {iid} part {k}'
    if w['kind'] == 'numeric' and 'answer' in w:
        tol = w['tol']['abs']
        ok(abs(w['answer'] - float(mine)) <= tol + 1e-12, f'{lab} key {w["answer"]} vs mine {float(mine)}')
        # the key is my value rounded to the stated form
        dp = max(0, -int(math.floor(math.log10(2 * tol)))) if tol > 0 else 0
        ok(abs(round(float(mine), dp) - w['answer']) < 1e-9, f'{lab} key is not mine rounded to {dp} dp')
        have = {x['id']: x for x in w.get('wrong', [])}
        for wid, val in (wrongs or {}).items():
            ok(wid in have, f'{lab} wrong id {wid} missing')
            if wid not in have:
                continue
            x = have[wid]
            seen_wrong.add((n, iid, k, wid))
            wt = x.get('tol', {'abs': 0})['abs']
            ok(abs(x['value'] - float(val)) <= wt + 1e-12, f'{lab} wrong {wid} {x["value"]} vs mine {float(val)}')
            ok(abs(x['value'] - w['answer']) > wt + tol + 1e-12, f'{lab} wrong {wid} band meets the key band')
        for wid in have:
            ok((n, iid, k, wid) in seen_wrong, f'{lab} wrong id {wid} not recomputed by the reader')
        vals = sorted((x['value'], x.get('tol', {'abs': 0})['abs']) for x in w.get('wrong', []))
        for (a, ta), (b, tb) in zip(vals, vals[1:]):
            ok(b - a > ta + tb, f'{lab} two wrong bands overlap: {a}, {b}')
        ok(set(p['feedback'].get('byKey', {})) <= set(have) | {'count'}, f'{lab} byKey id without a wrong entry')
    text = json.dumps(p, ensure_ascii=False)
    for s in says:
        ok(s in text, f'{lab} text lacks {s!r}')
    return p


def gini(*c):
    n = sum(c)
    return 1 - sum(F(x, n) ** 2 for x in c)


def H(*c):
    n = sum(c)
    return -sum(x / n * math.log2(x / n) for x in c if x)


def sse(v):
    v = [F(x) for x in v]
    if not v:
        return F(0)
    m = sum(v) / len(v)
    return sum((x - m) ** 2 for x in v)


def mean(v):
    return sum(F(x) for x in v) / len(v)


def splits(xs, ys, floor=1):
    """Every midpoint split of a 1-D regression set: (threshold, sse left + right, left, right)."""
    pts = sorted(zip(xs, ys))
    ux = sorted(set(xs))
    out = []
    for a, b in zip(ux, ux[1:]):
        t = (F(a) + F(b)) / 2
        L = [y for x, y in pts if x < t]
        R = [y for x, y in pts if x > t]
        if len(L) >= floor and len(R) >= floor:
            out.append((t, sse(L) + sse(R), L, R))
    return out


def fmt(x, dp):
    return f'{float(x):.{dp}f}'


# ---------------------------------------------------------------- problems-1
# p-spoof-alerts: 60 alerts, 18 spoof / 42 genuine; yes 14/8, no 4/34.
ok(14 + 4 == 18 and 8 + 34 == 42 and 22 + 38 == 60, 'spoof counts add up')
key(1, 'p-spoof-alerts', 1, min(14, 8) + min(4, 34), {'parent': min(18, 42), 'majority': max(14, 8) + max(4, 34), 'one-side': min(14, 8)},
    says=['That is 12', "root's 18 mistakes to 12"])
g_root = gini(18, 42)
key(1, 'p-spoof-alerts', 2, g_root, {'error-rate': F(18, 60), 'sum-squares': 1 - g_root, 'no-two': F(18, 60) * F(42, 60)},
    says=['0.09', '0.49'])
ok(g_root == 2 * F(3, 10) * F(7, 10), 'two-class Gini is 2pq')
gy, gn = gini(14, 8), gini(4, 34)
wg = F(22, 60) * gy + F(38, 60) * gn
key(1, 'p-spoof-alerts', 3, wg, {'unweighted': (gy + gn) / 2, 'yes-only': gy, 'gain': g_root - wg},
    says=[fmt(gy, 3), fmt(gn, 3), '0.289'])
ok(fmt(F(22, 60) * round(float(gy), 3) + F(38, 60) * round(float(gn), 3), 3) == '0.289', 'rounded side Ginis still give 0.289')
key(1, 'p-spoof-alerts', 4, g_root - wg, {'child': wg, 'carried': g_root - round(float((gy + gn) / 2), 3), 'mistakes': F(18 - 12, 60)},
    says=['0.42 - 0.289 = 0.131', '0.326'])
ok(12 + 2 == 14 and 1 + 7 == 8, 'second split keeps the yes side counts')
key(1, 'p-spoof-alerts', 5, min(12, 1) + min(2, 7) + min(4, 34), {'no-leaf': 1 + 2, 'carried': 12, 'spoof-only': 2 + 4},
    says=['from 12 to 7'])

# p-repo-terms
term = [1, 2, 4, 6, 9, 15]
cost = [5, 7, 6, 13, 9, 20]
root = sse(cost)
ok(mean(cost) == 10, 'repo mean 10')
med = F(sorted(cost)[2] + sorted(cost)[3], 2)
key(1, 'p-repo-terms', 1, root, {'unsquared': sum(abs(c - 10) for c in cost), 'mean-error': root / 6, 'median': sum((c - med) ** 2 for c in cost)},
    says=['25 + 9 + 16 + 9 + 1 + 100 = 160', '5 + 3 + 4 + 3 + 1 + 10'])
sp = splits(term, cost)
drops = {t: root - s for t, s, _, _ in sp}
ok([float(t) for t in drops] == [1.5, 3, 5, 7.5, 12], 'repo midpoints')
ok([float(d) for d in drops.values()] == [30, 48, 96, 60.75, 120], f'repo drops {list(map(float, drops.values()))}')
best = max(drops, key=drops.get)
key(1, 'p-repo-terms', 2, drops[best], {'left-over': root - drops[best], 'even': drops[F(5)], 'first': drops[F(3, 2)]},
    says=['30, 48, 96, 60.75 and 120', '9 + 1 + 4 + 25 + 1 = 40'])
Lb, Rb = [(L, R) for t, s, L, R in sp if t == best][0]
key(1, 'p-repo-terms', 3, mean(Rb), {'root': 10, 'left': mean(Lb), 'carried': mean([13, 9, 20])})
spf = splits(term, cost, floor=2)
bf = min(spf, key=lambda r: r[1])
ok([float(r[0]) for r in spf] == [3, 5, 7.5] and bf[0] == 5, 'floored splits 3, 5, 7.5; best 5')
key(1, 'p-repo-terms', 4, root - bf[1], {'no-floor': 120, 'left-over': bf[1], 'next-door': drops[F(15, 2)]},
    says=['leave 2 and 62', '48 at 3 weeks, 96 at 5 and 60.75 at 7.5'])
ok(sse(bf[2]) == 2 and sse(bf[3]) == 62 and mean(bf[2]) == 6, 'floored leaves')
key(1, 'p-repo-terms', 5, mean(bf[3]), {'carried': 20, 'left': mean(bf[2]), 'root': 10})
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
Xr = np.array(term, float).reshape(-1, 1)
t0 = DecisionTreeRegressor(max_depth=1).fit(Xr, cost)
t1 = DecisionTreeRegressor(max_depth=1, min_samples_leaf=2).fit(Xr, cost)
ok(t0.tree_.threshold[0] == 12 and t0.predict([[26]])[0] == 20, 'sklearn stump: 12 weeks, 20 bp at 26 weeks')
ok(t1.tree_.threshold[0] == 5 and abs(t1.predict([[26]])[0] - 14) < 1e-12, 'sklearn floored stump: 5 weeks, 14 bp')

# p-broker-pruning: a node as (stayed, left, children)
N = 400
node27 = (18, 9, [(0, 7, []), (18, 2, [(15, 0, []), (3, 2, [])])])


def R(nd):
    return F(nd[0] + nd[1], N) * gini(nd[0], nd[1])


def leaves(nd):
    return [nd] if not nd[2] else [l for c in nd[2] for l in leaves(c)]


def alpha(nd):
    return (R(nd) - sum(R(l) for l in leaves(nd))) / (len(leaves(nd)) - 1)


inner = node27[2][1]
key(1, 'p-broker-pruning', 1, gini(18, 9), {'error-rate': F(1, 3), 'sum-squares': F(5, 9), 'no-two': F(2, 9)})
key(1, 'p-broker-pruning', 2, R(node27), {'unweighted': F(4, 9), 'carried': F(27, 400) * F(1, 3), 'carried-squares': F(27, 400) * F(5, 9)},
    says=['0.0675'])
key(1, 'p-broker-pruning', 3, alpha(inner), {'no-subtract': R(inner), 'halved': alpha(inner) / 2, 'leaf-only': R((3, 2, []))},
    says=['0.18', '0.48', '0.009 - 0.006'])
ok(alpha(inner) < alpha(node27) == F(12, 1000), 'weakest link is the inner node (0.003 < 0.012)')
pruned = (18, 9, [(0, 7, []), (18, 2, [])])
key(1, 'p-broker-pruning', 4, alpha(pruned), {'three-leaves': alpha(node27), 'no-subtract': R(node27), 'halved': alpha(pruned) / 2},
    says=['0.03 - 0.009'])
path = [alpha(inner), alpha(pruned)]
kept = 11 - sum(1 for a in path if a <= F(16, 1000))
key(1, 'p-broker-pruning', 5, kept, {'carried': 11 - 2, 'not-cut': 11, 'three': 11 - 3})
# route 2: scikit-learn's own pruning path on the 27 clients (alphas scale by 27/400)
Xb = np.array([[1, 0]] * 7 + [[0, 0]] * 15 + [[0, 1]] * 5, float)
yb = np.array([1] * 7 + [0] * 15 + [0, 0, 0, 1, 1])
pp = DecisionTreeClassifier(random_state=0).fit(Xb, yb).cost_complexity_pruning_path(Xb, yb).ccp_alphas * 27 / 400
ok(np.allclose(pp, [0, 0.003, 0.021]), f'sklearn pruning path {pp}')

# p-opening-gaps
down = [-1.4, -0.9, -0.6, -0.2, 0.5, 2.4]
up = [0.3, 0.9, 1.2, 1.7]
pts = sorted([(F(str(x)), 0) for x in down] + [(F(str(x)), 1) for x in up])
ths = [(a[0] + b[0]) / 2 for a, b in zip(pts, pts[1:])]
changes = sum(1 for a, b in zip(pts, pts[1:]) if a[1] != b[1])
key(1, 'p-opening-gaps', 1, len(ths), {'per-day': len(pts), 'boundaries': changes})


def side(t):
    L = [l for x, l in pts if x < t]
    R_ = [l for x, l in pts if x > t]
    return (L.count(0), L.count(1)), (R_.count(0), R_.count(1))


def ggain(t, weighted=True):
    L, R_ = side(t)
    if weighted:
        return gini(6, 4) - F(sum(L), 10) * gini(*L) - F(sum(R_), 10) * gini(*R_)
    return gini(6, 4) - (gini(*L) + gini(*R_)) / 2


def igain(t):
    L, R_ = side(t)
    return H(6, 4) - sum(L) / 10 * H(*L) - sum(R_) / 10 * H(*R_)


miss = {t: sum(min(s) for s in side(t)) for t in ths}
ok(F('0.05') in ths and F('0.7') in ths and miss[F('0.05')] == 2 == miss[F('0.7')] == min(miss.values()), 'splits 0.05 and 0.7 both leave 2 mistakes, the fewest')
ok(max(ths, key=ggain) == F('0.05') and max(ths, key=igain) == F('0.05'), '0.05 has the largest Gini gain and information gain of all 9')
a, b = F('0.05'), F('0.7')
La, Ra = side(a)
key(1, 'p-opening-gaps', 2, ggain(a), {'child': gini(6, 4) - ggain(a), 'unweighted': ggain(a, False), 'other': ggain(b)}, says=['0.48', '0.444'])
key(1, 'p-opening-gaps', 3, ggain(b), {'child': gini(6, 4) - ggain(b), 'unweighted': ggain(b, False), 'carried': ggain(a)},
    says=['0.278', '0.375', '0.317'])
key(1, 'p-opening-gaps', 4, igain(a), {'other': igain(b), 'gini': ggain(a), 'child': H(6, 4) - igain(a)}, says=[fmt(H(6, 4), 3), fmt(H(2, 4), 3)])
ok(fmt(round(H(6, 4), 3) - 0.6 * round(H(2, 4), 3), 3) == '0.420', 'rounded entropies still give 0.420')
runs = 1 + changes
Xg = np.array([float(x) for x, _ in pts]).reshape(-1, 1)
yg = [l for _, l in pts]
for crit in ('gini', 'entropy'):
    tr = DecisionTreeClassifier(criterion=crit).fit(Xg, yg)
    ok(tr.get_n_leaves() == runs == 5 and abs(tr.tree_.threshold[0] - 0.05) < 1e-6, f'sklearn {crit}: 5 leaves, root 0.05')
key(1, 'p-opening-gaps', 5, runs, {'per-day': 10, 'boundaries': changes, 'depth': 2 ** 3})

# ---------------------------------------------------------------- problems-2
# p-bond-downgrades
q = F(24, 25) ** 25
key(2, 'p-bond-downgrades', 1, q, {'one-draw': F(1, 25), 'limit': math.exp(-1), 'drawn': 1 - q})
key(2, 'p-bond-downgrades', 2, 8 * round(float(q), 4), {'in-bag': 8 * (1 - q), 'limit': 8 * math.exp(-1), 'per-draw': F(8, 25)})
ok(fmt(8 * q, 2) == '2.88', 'unrounded chance also gives 2.88')
allin = (1 - q) ** 8
key(2, 'p-bond-downgrades', 3, 25 * allin, {'one-bond': allin, 'all-missed': 25 * q ** 8, 'one-tree': 25 * (1 - q)}, says=['0.0280', '0.70'])
ok(fmt(25 * (1 - 0.3604) ** 8, 2) == '0.70', 'rounded chance also gives 0.70')
rng = np.random.default_rng(7)
draws = rng.integers(0, 25, size=(60000, 8, 25))
present = np.zeros((60000, 8, 25), bool)
np.put_along_axis(present, draws, True, axis=2)
ok(abs((~present).mean() - float(q)) < 0.002, 'simulation: left out of one resample')
ok(abs((~present).sum(axis=1).mean() - 8 * float(q)) < 0.02, 'simulation: out-of-bag trees per bond')
ok(abs(present.all(axis=1).sum(axis=1).mean() - 25 * float(allin)) < 0.02, 'simulation: bonds with no out-of-bag tree')
key(2, 'p-bond-downgrades', 4, F(5 + 1, 25), {'skipped': F(5, 24), 'counted-right': F(5, 25), 'accuracy': F(19, 25)}, says=['0.208'])
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, GradientBoostingRegressor, GradientBoostingClassifier
n_unc = 0
for seed in range(60):
    Xs = rng.normal(size=(25, 3))
    ys = (rng.random(25) < 0.4).astype(int)
    for cls in (RandomForestClassifier, BaggingClassifier):
        m = cls(n_estimators=8, oob_score=True, random_state=seed).fit(Xs, ys)
        d = np.nan_to_num(m.oob_decision_function_)
        unc = d.sum(axis=1) == 0
        if unc.any():
            n_unc += 1
            pred = d.argmax(axis=1)
            ok((pred[unc] == 0).all() and abs((pred == ys).mean() - m.oob_score_) < 1e-12, f'sklearn {cls.__name__} seed {seed}: uncovered row scored as class 0')
ok(n_unc > 10, 'sklearn uncovered rows seen')

# p-ipo-forest
m_feat = int(math.sqrt(10))
key(2, 'p-ipo-forest', 1, F(m_feat, 10), {'one': F(1, 10), 'unrounded': math.sqrt(10) / 10, 'miss': 1 - F(m_feat, 10)})
ok(RandomForestClassifier(n_estimators=1, max_features='sqrt', random_state=0).fit(rng.normal(size=(40, 10)), rng.integers(0, 2, 40)).estimators_[0].max_features_ == 3, 'sklearn offers 3 of 10')


def var_avg(s2, rho, B):
    return rho * s2 + (1 - rho) * s2 / B


def var_cov(s2, rho, B):
    C = np.full((B, B), float(rho * s2))
    np.fill_diagonal(C, float(s2))
    return C.sum() / B ** 2


bs, br, fs, fr = F('0.12'), F('0.15'), F('0.15'), F('0.06')
vb, vf = var_avg(bs, br, 50), var_avg(fs, fr, 50)
ok(abs(var_cov(bs, br, 50) - float(vb)) < 1e-12 and abs(var_cov(fs, fr, 50) - float(vf)) < 1e-12, 'covariance-matrix route agrees')
key(2, 'p-ipo-forest', 2, vb, {'independent': bs / 50, 'floor': br * bs, 'one-tree': bs}, says=['0.018 + 0.00204'])
key(2, 'p-ipo-forest', 3, vf, {'floor': fr * fs, 'independent': fs / 50, 'swapped': var_avg(fs, br, 50)}, says=['0.009 + 0.00282', '0.0118', '0.0200'])
ok((1 - fr) * fs == F('0.141') and (1 - br) * bs == F('0.102'), 'the 1/B coefficients 0.141 and 0.102')
firstB = next(B for B in range(1, 1000) if var_avg(fs, fr, B) < var_avg(bs, br, B))
ok(all(var_avg(fs, fr, B) < var_avg(bs, br, B) for B in range(firstB, 2000)), 'forest stays lower from there on')
key(2, 'p-ipo-forest', 4, firstB, {'round-down': firstB - 1, 'one': 1, 'ratio': round(0.141 / 0.009)}, says=['4.33', '0.04425', '0.0435'])
ok(var_avg(fs, fr, 4) == F('0.04425') and var_avg(bs, br, 4) == F('0.0435') and F(39, 9) > 4, 'B = 4 values')

# p-dividend-importance
ok((100 + 10, 30 + 60) == (110, 90) and (100 + 30, 10 + 60) == (130, 70) and (6 + 24, 54 + 6) == (30, 60), 'dividend counts')
gr, gl, gR = gini(130, 70), gini(100, 10), gini(30, 60)
wch = F(110, 200) * gl + F(90, 200) * gR
c_pay = gr - wch
key(2, 'p-dividend-importance', 1, c_pay, {'child': wch, 'unweighted': gr - (gl + gR) / 2, 'parent': gr}, says=['0.455', '0.1653', '0.2909'])
wc2 = F(60, 90) * gini(6, 54) + F(30, 90) * gini(24, 6)
c_cov = F(90, 200) * (gR - wc2)
key(2, 'p-dividend-importance', 2, c_cov, {'node-only': gR - wc2, 'child': wc2, 'share-left': F(110, 200) * (gR - wc2)}, says=['0.18', '0.32', '0.2267', '0.2178'])
# company_id: 8 companies split off the left node; which mix earns 0.0144?
c_id = F(110, 200) * (gl - F(8, 110) * gini(4, 4) - F(102, 110) * gini(96, 6))
ok(fmt(c_id, 4) == '0.0144', f'8 companies (4 kept, 4 cut) earn {float(c_id):.4f}')
tot = F('0.1641') + F('0.0980') + F('0.0144')
share = F('0.1641') / tot
key(2, 'p-dividend-importance', 3, share, {'raw': F('0.1641'), 'third': F(1, 3), 'carried': F('0.1641') / (F('0.1641') + F('0.2178') + F('0.0144'))},
    says=['0.2765', fmt(F('0.0980') / tot, 3), fmt(F('0.0144') / tot, 3)])
ok(fmt(c_pay / (c_pay + c_cov + c_id), 3) == '0.593', 'unrounded credits give the same share')
# route 2: scikit-learn's own importances on a built book of 200 companies
rows = []
for kept_, cut_, pay, cov, cid in [(96, 6, 0, None, 0), (4, 4, 0, None, 1), (6, 54, 1, 0, 0), (24, 6, 1, 1, 0)]:
    for j in range(kept_ + cut_):
        lab = 0 if j < kept_ else 1
        rows.append((pay, (j % 2) if cov is None else cov, cid, lab))
A = np.array(rows, float)
tr = DecisionTreeClassifier(max_depth=2, random_state=0).fit(A[:, :3], A[:, 3])
ok(tr.tree_.feature[0] == 0 and sorted(tr.tree_.feature[tr.tree_.feature >= 0]) == [0, 1, 2], 'sklearn tree: payout at the root, cover and id below')
ok(np.allclose(tr.feature_importances_, [float(c_pay / (c_pay + c_cov + c_id)), float(c_cov / (c_pay + c_cov + c_id)), float(c_id / (c_pay + c_cov + c_id))]), f'sklearn importances {tr.feature_importances_}')
others = [F('0.48'), F('0.66'), F('0.55')]
key(2, 'p-dividend-importance', 4, (F('0.593') + sum(others)) / 4, {'three': sum(others) / 3, 'this-tree': F('0.593'), 'sum': F('0.593') + sum(others)}, says=['2.283'])
p5 = item(2, 'p-dividend-importance')['parts'][4]
ok([o['id'] for o in p5['widget']['options'] if o.get('correct')] == ['memorised'], 'dividend part 5 key')

# p-imbalance-stumps
imb = [-0.6, -0.4, -0.3, 0.2, 0.6, 0.8]
mv = [-4, -1, -2, 1, 4, 4]
drawA, drawB = [0, 0, 1, 3, 4, 4], [1, 2, 2, 3, 5, 5]
oobA = sorted(set(range(6)) - set(drawA))
oobB = sorted(set(range(6)) - set(drawB))
w1 = item(2, 'p-imbalance-stumps')['parts'][0]['widget']
checks += 1
ok(sorted(w1['answers']) == oobA == [2, 5] and oobB == [0, 4] and sorted(set(drawA) & set(drawB)) == [1, 3], 'out-of-bag rows')
ok({x['id']: x['value'] for x in w1['wrong']} == {'repeats': '0, 4', 'drawn-once': '1, 3'}, 'part 1 wrong lists')


def stump(draw):
    xs = [F(str(imb[i])) for i in draw]
    ys = [mv[i] for i in draw]
    sp_ = splits(xs, ys)
    t, s, L, R_ = min(sp_, key=lambda r: r[1])
    return t, mean(L), mean(R_), sp_


tA, lA, rA, spA = stump(drawA)
tB, lB, rB, spB = stump(drawB)
ok((tA, lA, rA) == (F('-0.1'), -3, 3) and sorted(float(s[1]) for s in spA) == [12, 18, 18], 'tree A stump')
ok((tB, lB, rB) == (F('0.5'), -1, 4) and [float(s[1]) for s in spB] == [36, float(F(20, 3)), 6], 'tree B stump')
for draw, t, l, r in ((drawA, tA, lA, rA), (drawB, tB, lB, rB)):
    sk = DecisionTreeRegressor(max_depth=1).fit(np.array([imb[i] for i in draw]).reshape(-1, 1), [mv[i] for i in draw])
    ok(abs(sk.tree_.threshold[0] - float(t)) < 1e-6 and np.allclose(sk.predict([[-9], [9]]), [float(l), float(r)]), 'sklearn stump agrees')


def fA(x):
    return lA if x < tA else rA


def fB(x):
    return lB if x < tB else rB


key(2, 'p-imbalance-stumps', 2, fA(F('0.8')), {'no-repeats': mean([mv[3], mv[4]]), 'own-value': mv[5], 'no-split': mean([mv[i] for i in drawA])},
    says=['6 + 6 = 12', '18 each'])
wrong_split = [s for s in spB if s[0] == F('-0.05')][0]
key(2, 'p-imbalance-stumps', 3, fB(F('-0.6')), {'no-repeats': mean([mv[1], mv[2], mv[3]]), 'own-value': mv[0], 'wrong-split': mean(wrong_split[2]), 'sign': 1},
    says=['36 and 6.67', '6 against 6.67'])
errs = [(fA(F(str(imb[i]))) - mv[i]) for i in oobA] + [(fB(F(str(imb[i]))) - mv[i]) for i in oobB]
key(2, 'p-imbalance-stumps', 4, mean([e ** 2 for e in errs]), {'all-six': sum(e ** 2 for e in errs) / 6, 'sum': sum(e ** 2 for e in errs), 'unsquared': mean([abs(e) for e in errs])},
    says=['1, 1, 9 and 0'])
key(2, 'p-imbalance-stumps', 5, (fA(F('0.3')) + fB(F('0.3'))) / 2, {'tree-a': fA(F('0.3')), 'tree-b': fB(F('0.3')), 'sum': fA(F('0.3')) + fB(F('0.3'))})

# ---------------------------------------------------------------- problems-3
# p-fill-times
ticks = [1, 2, 3, 4, 5]
mins = [4, 5, 9, 16, 21]
nu = F(1, 10)
F0 = mean(mins)
key(3, 'p-fill-times', 1, F0, {'median': sorted(mins)[2], 'zero': 0, 'midrange': F(min(mins) + max(mins), 2)})
res = [m - F0 for m in mins]
sp1 = splits(ticks, res)
t1_, s1_, L1, R1 = min(sp1, key=lambda r: r[1])
ok(t1_ == F(7, 2) and s1_ == F('26.5') and sse(res) == 214, 'first stump: between 3 and 4 ticks, 26.5 left; 214 before')
key(3, 'p-fill-times', 2, mean(L1), {'times': mean(mins[:3]), 'sign': -mean(L1), 'shrunk': nu * mean(L1)}, says=['14 + 12.5 = 26.5', '7.5'])
f1 = [F0 + nu * (mean(L1) if x < t1_ else mean(R1)) for x in ticks]
key(3, 'p-fill-times', 3, f1[0], {'full-step': F0 + mean(L1), 'sign': F0 - nu * mean(L1), 'from-zero': nu * mean(L1)}, says=['11.75'])
res1 = [m - f for m, f in zip(mins, f1)]
key(3, 'p-fill-times', 4, sum(r * r for r in res1), {'full-step': s1_, 'before': sse(res), 'mean': sum(r * r for r in res1) / 5},
    says=['42.25 + 30.25 + 2.25 + 18.0625 + 85.5625'])
sp2 = splits(ticks, res1)
t2_, s2_, L2, R2 = min(sp2, key=lambda r: r[1])
ok(t2_ == t1_, 'second stump splits in the same place')
key(3, 'p-fill-times', 5, f1[0] + nu * mean(L2), {'same-step': f1[0] + nu * mean(L1), 'full-step': f1[0] + mean(L2), 'unchanged': f1[0]}, says=['-4.5'])
gb = GradientBoostingRegressor(max_depth=1, learning_rate=0.1, n_estimators=2).fit(np.array(ticks).reshape(-1, 1), mins)
st = list(gb.staged_predict([[1]]))
ok(abs(gb.init_.predict([[1]])[0] - 11) < 1e-12 and abs(st[0][0] - 10.5) < 1e-12 and abs(st[1][0] - 10.05) < 1e-12, f'sklearn boosting stages {st}')

# p-callable-bonds
p0 = F(2, 8)
F0c = math.log(p0 / (1 - p0))
key(3, 'p-callable-bonds', 1, F0c, {'rate': p0, 'sign': -F0c, 'odds': p0 / (1 - p0)})
key(3, 'p-callable-bonds', 2, 1 - p0, {'slope': p0 - 1, 'p': p0, 'log-odds': 1 - round(F0c, 4)})
eps = 1e-6
num_slope = (math.log(1 + math.exp(-(F0c + eps))) - math.log(1 + math.exp(-(F0c - eps)))) / (2 * eps)
ok(abs(num_slope - float(p0 - 1)) < 1e-8, 'slope of ln(1 + e^-F) is p - 1 (numerical derivative)')
top = 2 * (1 - p0) + (0 - p0)
bot = 3 * p0 * (1 - p0)
leaf = top / bot
key(3, 'p-callable-bonds', 3, leaf, {'mean-residual': top / 3, 'sum': top, 'one-weight': top / (p0 * (1 - p0))}, says=['0.5625', '0.1875'])
F1 = round(F0c, 4) + 0.1 * round(float(leaf), 4)
key(3, 'p-callable-bonds', 4, F1, {'full-step': round(F0c, 4) + round(float(leaf), 4), 'carried': round(F0c, 4) + 0.1 * round(float(top / 3), 4),
                                   'sign': round(F0c, 4) - 0.1 * round(float(leaf), 4), 'abs': -F1})
ok(fmt(F0c + 0.1 * float(leaf), 4) == '-0.8764', 'unrounded log-odds agree')


def sig(z):
    return 1 / (1 + math.exp(-z))


key(3, 'p-callable-bonds', 5, sig(-0.8764), {'sign': sig(0.8764), 'added-p': p0 + F(1, 10) * leaf, 'carried': sig(1.1236)},
    says=[fmt(math.exp(0.8764), 4), fmt(1 + math.exp(0.8764), 4)])
Xc = np.array([[1]] * 3 + [[0]] * 5, float)
yc = np.array([1, 1, 0, 0, 0, 0, 0, 0])
gc = GradientBoostingClassifier(max_depth=1, learning_rate=0.1, n_estimators=1).fit(Xc, yc)
ok(abs(gc.decision_function([[1]])[0] - (F0c + 0.1 * float(leaf))) < 1e-9 and fmt(gc.predict_proba([[1]])[0, 1], 4) == '0.2939', 'sklearn classifier: F1 and p after one tree')

# p-futures-study
from sklearn.model_selection import TimeSeriesSplit
folds = list(TimeSeriesSplit(n_splits=4, test_size=60, gap=2).split(np.zeros(700)))
ok([(te[0], te[-1]) for _, te in folds] == [(460, 519), (520, 579), (580, 639), (640, 699)], 'four test blocks cover the last 240 days')
key(3, 'p-futures-study', 1, folds[0][0][-1], {'no-gap': 459, 'gap-one': 458, 'test-row': 460}, says=['458 and 459'])
h, bse = F(138, 240), F(126, 240)
se = math.sqrt(bse * (1 - bse) / 240)
key(3, 'p-futures-study', 2, float(h - bse) / se, {'fifty': float(h - F(1, 2)) / math.sqrt(0.25 / 240), 'one-day': float(h - bse) / math.sqrt(bse * (1 - bse)),
                                                    'hit-se': float(h - bse) / math.sqrt(h * (1 - h) / 240)}, says=['0.575', '0.525', fmt(se, 4)])
ok(fmt(0.05 / round(se, 4), 2) == '1.55', 'rounded standard error also gives 1.55')
from statsmodels.stats.proportion import proportions_ztest
ok(abs(proportions_ztest(138, 240, value=float(bse), prop_var=float(bse))[0] - float(h - bse) / se) < 1e-9, 'statsmodels z with the null variance')
pv = np.array([0.58, 0.61, 0.44, 0.47])
ret = np.array([0.008, -0.003, -0.006, 0.002])
pos = np.where(pv > 0.5, 1, -1)
gross = 2e6 * (pos * ret)
units = np.abs(np.diff(np.concatenate([[0], pos])))
unit_cost = 2e6 * 5e-4
net = gross.sum() - units.sum() * unit_cost
ok([round(g) for g in gross] == [16000, -6000, 12000, -4000] and units.sum() == 3 and unit_cost == 1000, 'P&L pieces')
key(3, 'p-futures-study', 3, round(net), {'gross': round(gross.sum()), 'flip-one': round(gross.sum() - 2 * unit_cost), 'closed': round(net - unit_cost)})
p4 = item(3, 'p-futures-study')['parts'][3]
ok([o['id'] for o in p4['widget']['options'] if o.get('correct')] == ['later-block'], 'futures part 4 key')

# p-surprise-drift: cells (small, positive) -> average return
cells = {(1, 1): 14, (1, 0): -10, (0, 1): 2, (0, 0): 2}
start = mean(cells.values())
key(3, 'p-surprise-drift', 1, start, {'zero': 0, 'positive-only': mean([14, 2]), 'no-sign': mean([14, 10, 2, 2])})
r0 = {c: v - start for c, v in cells.items()}
size_leaf = [mean([r0[c] for c in cells if c[0] == s]) for s in (0, 1)]
ok(size_leaf == [0, 0], 'a size split gains nothing')
pos_leaf = mean([r0[c] for c in cells if c[1] == 1])
neg_leaf = mean([r0[c] for c in cells if c[1] == 0])
key(3, 'p-surprise-drift', 2, pos_leaf, {'mean-not-residual': mean([14, 2]), 'small-only': r0[(1, 1)], 'sign': neg_leaf})
fc = {c: start + (pos_leaf if c[1] else neg_leaf) for c in cells}
key(3, 'p-surprise-drift', 3, fc[(1, 1)], {'truth': 14, 'leaf-only': pos_leaf, 'carried': start + mean([14, 2])})
r1 = {c: cells[c] - fc[c] for c in cells}
key(3, 'p-surprise-drift', 4, mean([v * v for v in r1.values()]), {'unsquared': 6, 'sum': sum(v * v for v in r1.values()), 'before': mean([v * v for v in r0.values()])})
ok(r1 == {(1, 1): 6, (1, 0): -6, (0, 1): -6, (0, 0): 6}, 'residuals after the first stump')
ok(all(mean([r1[c] for c in cells if c[f] == v]) == 0 for f in (0, 1) for v in (0, 1)), 'every stump leaf of the new residuals is 0')
Xs_ = np.array(list(cells) * 6, float)
ys_ = np.array(list(cells.values()) * 6, float)
for d, want in ((1, 36.0), (2, 0.0)):
    gbm = GradientBoostingRegressor(max_depth=d, n_estimators=50, learning_rate=1.0).fit(Xs_, ys_)
    ok(abs(np.mean((gbm.predict(Xs_) - ys_) ** 2) - want) < 1e-9, f'sklearn boosting depth {d}: MSE {want}')
p5 = item(3, 'p-surprise-drift')['parts'][4]
ok([o['id'] for o in p5['widget']['options'] if o.get('correct')] == ['depth'], 'drift part 5 key')

# ---------------------------------------------------------------- shape
for n, s in SETS.items():
    ok(3 <= len(s['items']) <= 5 and any(it['difficulty'] == 5 for it in s['items']), f'problems-{n}: 3 to 5 items, one of difficulty 5')
    parts = [p for it in s['items'] for p in it['parts']]
    typed = sum(1 for p in parts if p['widget']['kind'] != 'choice')
    ok(3 * typed >= 2 * len(parts), f'problems-{n}: two thirds typed')
    for it in s['items']:
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: 3 to 5 parts')
        for k, p in enumerate(it['parts'], 1):
            w = p['widget']
            if w['kind'] == 'numeric' and 'answer' in w and w['tol']['abs'] > 0:
                ok('decimal' in p['question'] or 'fraction' in p['question'], f'{it["id"]} part {k}: form not stated')

print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
