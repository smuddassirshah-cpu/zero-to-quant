"""Recompute every number in app/content/courses/ensembles/problems-<n>.json twice (docs/briefs/chained.md check 1).

Method 1 is exact: fractions or sympy, the formula the lesson teaches. Method 2 takes another route: scikit-learn
trees fitted to data built to match each story (impurity, thresholds, leaf means, pruning path, leaf counts),
NumPy floats, simulation, or a brute-force scan. For each numeric part the script checks: the two methods agree;
the key is within its tol; every `wrong` value matches its named slip, lies outside the key's band, has a band no
wider than half its value, and overlaps no other slip; byKey covers the wrongs. Choice parts check the keyed
option. Exit 0 when all pass.

Run (any working directory): <scratchpad>/venv/bin/python docs/reports/problems-ensembles-numbers.py
"""
import itertools
import json
import math
import os
import sys
import warnings
from fractions import Fraction as F

import numpy as np
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.normpath(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ensembles'))
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    with open(p) as fh:
        d = json.load(fh)
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'ensembles', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: no difficulty 5')
    return {it['id']: it for it in d['items']}


def num(items, iid, k, exact, alt, slips, round_tol=0.0006, agree=1e-6):
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, round_tol), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
        ok(abs(float(val) - e) > tol, f'{tag}: slip {wid} equals the answer')
        ok(wt <= abs(x['value']) / 2 + 1e-12, f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    fb = items[iid]['parts'][k - 1]['feedback']
    ok(set(fb.get('byKey', {})) == set(wrongs), f'{tag}: byKey keys vs wrongs')


def pick(items, iid, k, correct_id):
    w = items[iid]['parts'][k - 1]['widget']
    ok(w['kind'] == 'choice', f'{iid} p{k}: not choice')
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed} vs {correct_id}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} p{k}: distractor without why')


def gini(c):
    n = sum(c)
    return 1 - sum(F(x, n) ** 2 for x in c)


def ent(c):
    n = sum(c)
    return -sum(x / n * math.log2(x / n) for x in c if x)


def sse(v):
    m = F(sum(v), len(v))
    return sum((F(a) - m) ** 2 for a in v)


def rows(counts):
    """Labels for a list of (class 0, class 1) counts, one block per count pair."""
    y = []
    for a, b in counts:
        y += [0] * a + [1] * b
    return np.array(y)


# ---------------------------------------------------------------- level 1
L1 = load(1)
if L1:
    # p-spoof-alerts. Method 2: scikit-learn trees on 60 built rows (x0 = cancelled > 90%, x1 = rested < 2 s).
    it = 'p-spoof-alerts'
    blocks = [((1, 1), (1, 12)), ((1, 0), (7, 2)), ((0, 0), (34, 4))]   # (features, (genuine, spoof))
    X = np.array([f for f, (g, s) in blocks for _ in range(g + s)], dtype=float)
    y = np.concatenate([rows([(g, s)]) for f, (g, s) in blocks])
    t1 = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X[:, :1], y)
    root_g = t1.tree_.impurity[0]
    child_w = sum(t1.tree_.n_node_samples[i] / 60 * t1.tree_.impurity[i] for i in (1, 2))
    mis1 = int((t1.predict(X[:, :1]) != y).sum())
    t2 = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)
    leaves2 = t2.get_n_leaves()
    # the no side must stay a leaf: its rows share one feature vector, so the depth-2 tree has 3 leaves
    ok(leaves2 == 3, f'{it}: depth-2 leaves {leaves2}')
    mis2 = int((t2.predict(X) != y).sum())
    gp, gy, gn = gini((18, 42)), gini((14, 8)), gini((4, 34))
    w = F(22, 60) * gy + F(38, 60) * gn
    num(L1, it, 1, 8 + 4, mis1, {'parent': 18, 'majority': 14 + 34, 'one-side': 8})
    num(L1, it, 2, gp, root_g, {'error-rate': 0.3, 'sum-squares': 1 - gp, 'no-two': gp / 2})
    num(L1, it, 3, w, child_w, {'unweighted': (gy + gn) / 2, 'yes-only': gy, 'gain': gp - w})
    num(L1, it, 4, gp - w, root_g - child_w, {'child': w, 'carried': gp - (gy + gn) / 2, 'mistakes': F(18 - 12, 60)})
    num(L1, it, 5, 1 + 2 + 4, mis2, {'no-leaf': 3, 'carried': 12, 'spoof-only': 2 + 4})
    ok(abs(float(gy) - 0.463) < 0.0005 and abs(float(gn) - 0.188) < 0.0005, f'{it}: side Gini values in prose')

    # p-repo-terms. Method 2: DecisionTreeRegressor (squared_error), impurity times n is the summed squared error.
    it = 'p-repo-terms'
    T = np.array([1, 2, 4, 6, 9, 15], dtype=float)
    C = [5, 7, 6, 13, 9, 20]
    root = sse(C)
    drops = {(T[i - 1] + T[i]) / 2: root - sse(C[:i]) - sse(C[i:]) for i in range(1, 6)}
    ok([float(drops[k]) for k in sorted(drops)] == [30, 48, 96, 60.75, 120], f'{it}: drops {drops}')
    r1 = DecisionTreeRegressor(max_depth=1, random_state=0).fit(T.reshape(-1, 1), C)
    sk_root = r1.tree_.impurity[0] * 6
    sk_drop = sk_root - sum(r1.tree_.impurity[i] * r1.tree_.n_node_samples[i] for i in (1, 2))
    ok(abs(r1.tree_.threshold[0] - 12) < 1e-9, f'{it}: sklearn threshold {r1.tree_.threshold[0]}')
    r2 = DecisionTreeRegressor(max_depth=1, min_samples_leaf=2, random_state=0).fit(T.reshape(-1, 1), C)
    sk_drop2 = sk_root - sum(r2.tree_.impurity[i] * r2.tree_.n_node_samples[i] for i in (1, 2))
    ok(abs(r2.tree_.threshold[0] - 5) < 1e-9, f'{it}: floored threshold {r2.tree_.threshold[0]}')
    num(L1, it, 1, root, sk_root, {'unsquared': sum(abs(c - 10) for c in C), 'mean-error': root / 6,
                                   'median': sum((c - 8) ** 2 for c in C)})
    num(L1, it, 2, drops[12.0], sk_drop, {'left-over': sse(C[:5]), 'even': drops[5.0], 'first': drops[1.5]})
    num(L1, it, 3, F(20), r1.predict([[26]])[0], {'root': 10, 'left': F(sum(C[:5]), 5), 'carried': F(42, 3)})
    num(L1, it, 4, drops[5.0], sk_drop2, {'no-floor': drops[12.0], 'left-over': sse(C[:3]) + sse(C[3:]),
                                          'next-door': drops[7.5]})
    num(L1, it, 5, F(13 + 9 + 20, 3), r2.predict([[26]])[0], {'carried': 20, 'left': F(18, 3), 'root': 10})
    ok(sse(C[:5]) == 40 and sse(C[:3]) == 2 and sse(C[3:]) == 62, f'{it}: leaf errors in prose')

    # p-broker-pruning. Method 2: the node of 27 grown alone by scikit-learn; its pruning path, scaled from 27 to
    # 400 clients, gives the break-even alphas (sklearn weights impurity by the share of the rows it was fitted on).
    it = 'p-broker-pruning'
    N = 400
    G27 = gini((18, 9))
    Rt = F(27, N) * G27
    R20 = F(20, N) * gini((18, 2))
    R5 = F(5, N) * gini((3, 2))
    a1 = (R20 - R5) / 1
    a2 = (Rt - R20 - 0) / 1
    # greedy check: splitting off the 7 who left beats splitting off the mixed 5
    ok(F(20, N) * gini((18, 2)) < F(5, N) * gini((3, 2)) + F(22, N) * gini((15, 7)), f'{it}: greedy first split')
    Xb, yb = [], []
    for feat, (st, lf) in [((1, 0), (0, 7)), ((0, 0), (15, 0)), ((0, 1), (3, 2))]:
        Xb += [feat] * (st + lf)
        yb += [0] * st + [1] * lf
    Xb, yb = np.array(Xb, float), np.array(yb)
    full = DecisionTreeClassifier(random_state=0).fit(Xb, yb)
    ok(full.get_n_leaves() == 3, f'{it}: standalone leaves {full.get_n_leaves()}')
    ok(abs(full.tree_.threshold[0] - 0.5) < 1e-9 and full.tree_.feature[0] == 0, f'{it}: root splits off the 7')
    path = full.cost_complexity_pruning_path(Xb, yb)
    scaled = sorted(float(a) * 27 / N for a in path.ccp_alphas if a > 1e-12)
    ok(len(scaled) == 2, f'{it}: path {scaled}')
    sk_G = full.tree_.impurity[0]
    sk_Rt = sk_G * 27 / N
    sk_R20 = full.tree_.impurity[full.tree_.children_left[0]] * 20 / N
    if full.tree_.n_node_samples[full.tree_.children_left[0]] != 20:
        sk_R20 = full.tree_.impurity[full.tree_.children_right[0]] * 20 / N
    kept = DecisionTreeClassifier(random_state=0, ccp_alpha=0.016 * N / 27).fit(Xb, yb).get_n_leaves()
    num(L1, it, 1, G27, sk_G, {'error-rate': F(1, 3), 'sum-squares': 1 - G27, 'no-two': G27 / 2})
    num(L1, it, 2, Rt, sk_Rt, {'unweighted': G27, 'carried': F(27, N) * F(1, 3), 'carried-squares': F(27, N) * (1 - G27)})
    num(L1, it, 3, a1, scaled[0], {'no-subtract': R20, 'halved': a1 / 2, 'leaf-only': R5}, round_tol=0.00005)
    num(L1, it, 4, a2, scaled[1], {'three-leaves': (Rt - R5) / 2, 'no-subtract': Rt, 'halved': a2 / 2},
        round_tol=0.00005)
    num(L1, it, 5, 11 - 1, 11 - (3 - kept), {'carried': 9, 'not-cut': 11, 'three': 8})
    ok(float(a1) <= 0.016 < float(a2) < 0.024 and float((Rt - R5) / 2) <= 0.016, f'{it}: 0.016 sits between the cuts')
    ok(abs(float(sk_R20) - 0.009) < 1e-12 and gini((18, 2)) == F(18, 100), f'{it}: R of the inner node')

    # p-opening-gaps. Method 2: scikit-learn stumps with gini and entropy, and the unlimited tree's leaf count.
    it = 'p-opening-gaps'
    gaps = np.array([-1.4, -0.9, -0.6, -0.2, 0.3, 0.5, 0.9, 1.2, 1.7, 2.4])
    lab = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 0])
    par = (6, 4)

    def gain_at(i, crit):
        L, Rr = lab[:i], lab[i:]
        cl = ((L == 0).sum(), (L == 1).sum())
        cr = ((Rr == 0).sum(), (Rr == 1).sum())
        if crit == 'gini':
            return gini(par) - F(i, 10) * gini(cl) - F(10 - i, 10) * gini(cr)
        return ent(par) - i / 10 * ent(cl) - (10 - i) / 10 * ent(cr)

    mids = (gaps[:-1] + gaps[1:]) / 2
    g = {round(float(m), 2): gain_at(i + 1, 'gini') for i, m in enumerate(mids)}
    mist = {round(float(m), 2): min(((lab[:i + 1] == 0).sum(), (lab[:i + 1] == 1).sum()))
            + min(((lab[i + 1:] == 0).sum(), (lab[i + 1:] == 1).sum())) for i, m in enumerate(mids)}
    ok(mist[0.05] == 2 and mist[0.7] == 2 and min(mist.values()) == 2 and list(mist.values()).count(2) == 2,
       f'{it}: mistakes {mist}')
    ok(max(g, key=g.get) == 0.05, f'{it}: best Gini split {max(g, key=g.get)}')
    s_g = DecisionTreeClassifier(max_depth=1, random_state=0).fit(gaps.reshape(-1, 1), lab)
    s_e = DecisionTreeClassifier(max_depth=1, criterion='entropy', random_state=0).fit(gaps.reshape(-1, 1), lab)
    ok(abs(s_g.tree_.threshold[0] - 0.05) < 1e-6 and abs(s_e.tree_.threshold[0] - 0.05) < 1e-6, f'{it}: thresholds')

    def sk_gain(m):
        t = m.tree_
        return t.impurity[0] - sum(t.n_node_samples[i] / 10 * t.impurity[i] for i in (1, 2))

    # the split at 0.7 by hand in NumPy floats
    p_l, p_r = 1 / 6, 3 / 4
    alt07 = 0.48 - 0.6 * 2 * p_l * (1 - p_l) - 0.4 * 2 * p_r * (1 - p_r)
    full_g = DecisionTreeClassifier(random_state=0).fit(gaps.reshape(-1, 1), lab)
    runs = 1 + int((lab[1:] != lab[:-1]).sum())
    num(L1, it, 1, len(mids), len(np.unique(gaps)) - 1, {'per-day': 10, 'boundaries': runs - 1})
    num(L1, it, 2, g[0.05], sk_gain(s_g), {'child': gini(par) - g[0.05],
                                           'unweighted': gini(par) - gini((2, 4)) / 2, 'other': g[0.7]})
    num(L1, it, 3, g[0.7], alt07, {'child': gini(par) - g[0.7],
                                   'unweighted': gini(par) - (gini((5, 1)) + gini((1, 3))) / 2, 'carried': g[0.05]})
    num(L1, it, 4, gain_at(4, 'entropy'), sk_gain(s_e), {'other': gain_at(6, 'entropy'), 'gini': g[0.05],
                                                         'child': ent(par) - gain_at(4, 'entropy')})
    num(L1, it, 5, runs, full_g.get_n_leaves(), {'per-day': 10, 'boundaries': runs - 1, 'depth': 8})
    ok(abs(ent(par) - 0.971) < 0.0005 and abs(ent((2, 4)) - 0.918) < 0.0005, f'{it}: entropies in feedback')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
