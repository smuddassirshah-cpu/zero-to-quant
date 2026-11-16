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

# ---------------------------------------------------------------- level 2
L2 = load(2)
if L2:
    from math import comb
    from scipy.stats import binom

    # p-bond-downgrades. Method 2: scipy's binomial law of the number of draws that hit the bond.
    it = 'p-bond-downgrades'
    p_out = F(24, 25) ** 25
    sp_out = binom.pmf(0, 25, 1 / 25)
    rng = np.random.default_rng(0)
    sim = np.mean([0 not in rng.integers(0, 25, 25) for _ in range(40000)])
    ok(abs(sim - float(p_out)) < 0.01, f'{it}: simulation {sim}')
    pr = 0.3604  # the value later parts tell the learner to use
    num(L2, it, 1, p_out, sp_out, {'one-draw': F(1, 25), 'limit': math.exp(-1), 'drawn': 1 - p_out}, round_tol=0.00005)
    num(L2, it, 2, 8 * pr, binom(8, pr).mean(), {'in-bag': 8 * (1 - pr), 'limit': 8 * 0.368, 'per-draw': 8 / 25},
        round_tol=0.005, agree=1e-9)
    ok(abs(8 * float(p_out) - 2.88) < 0.005, f'{it}: exact p gives the same 2.88')
    num(L2, it, 3, 25 * (1 - pr) ** 8, 25 * binom.pmf(8, 8, 1 - pr),
        {'one-bond': (1 - pr) ** 8, 'all-missed': 25 * pr ** 8, 'one-tree': 25 * (1 - pr)}, round_tol=0.005)
    ok(abs(25 * float(1 - p_out) ** 8 - 0.70) < 0.005, f'{it}: exact p gives the same 0.70')
    # sklearn's rule: an uncovered row gets a zero row in oob_decision_function_, so argmax calls it class 0
    dec = np.zeros((25, 2))
    truth = np.zeros(25, int)
    truth[:6] = 1                      # bond 0 uncovered and downgraded; bonds 1 to 5 misjudged below
    dec[1:6] = [0.8, 0.2]              # downgraded, voted not
    dec[6:] = [0.7, 0.3]               # not downgraded, voted not
    sk_err = np.mean(dec.argmax(1) != truth)
    num(L2, it, 4, F(6, 25), sk_err, {'skipped': F(5, 24), 'counted-right': F(5, 25), 'accuracy': F(19, 25)})

    # p-ipo-forest. Method 2: the variance of an average from the full covariance matrix, 1'S1 / B^2.
    it = 'p-ipo-forest'

    def var_avg(s2, rho, B):
        return rho * s2 + (1 - rho) * s2 / B

    def var_cov(s2, rho, B):
        S = np.full((B, B), rho * s2)
        np.fill_diagonal(S, s2)
        return S.sum() / B ** 2

    m = math.isqrt(10)
    num(L2, it, 1, F(m, 10), 1 - comb(9, m) / comb(10, m), {'one': F(1, 10), 'unrounded': math.sqrt(10) / 10,
                                                            'miss': F(10 - m, 10)}, round_tol=0.0015)
    sb, rb, sf, rf = F(12, 100), F(15, 100), F(15, 100), F(6, 100)
    num(L2, it, 2, var_avg(sb, rb, 50), var_cov(0.12, 0.15, 50), {'independent': sb / 50, 'floor': rb * sb, 'one-tree': sb})
    num(L2, it, 3, var_avg(sf, rf, 50), var_cov(0.15, 0.06, 50), {'floor': rf * sf, 'independent': sf / 50,
                                                                 'swapped': var_avg(sf, rb, 50)}, round_tol=0.00005)
    ok(rf * sf == F(9, 1000) and (1 - rf) * sf == F(141, 1000) and rb * sb == F(18, 1000) and (1 - rb) * sb == F(102, 1000),
       f'{it}: terms quoted in part 4')
    first = next(B for B in range(1, 100) if var_cov(0.15, 0.06, B) < var_cov(0.12, 0.15, B))
    exact_first = math.floor((F(141, 1000) - F(102, 1000)) / (F(18, 1000) - F(9, 1000))) + 1
    num(L2, it, 4, exact_first, first, {'round-down': exact_first - 1, 'one': 1, 'ratio': math.ceil(0.141 / 0.009)})
    ok(abs(float(var_avg(sf, rf, 4)) - 0.04425) < 1e-12 and abs(float(var_avg(sb, rb, 4)) - 0.0435) < 1e-12,
       f'{it}: 4-tree values in feedback')

    # p-dividend-importance (partial dependence of a 4-tree forest). Method 2: NumPy arrays, means over axes and groups.
    it = 'p-dividend-importance'
    trees = [F('0.60'), F('0.80'), F('0.70'), F('0.78')]
    at20 = [F('0.72'), F('0.84'), F('0.66'), F('0.14'), F('0.22'), F('0.12')]
    at05 = [F('0.28'), F('0.36'), F('0.20'), F('0.10'), F('0.14'), F('0.12')]
    ok(sum(trees) / 4 == at20[0], f'{it}: order 1 is the mean of its trees')
    num(L2, it, 1, sum(trees) / 4, np.mean(np.array([0.60, 0.80, 0.70, 0.78])),
        {'sum': sum(trees), 'max': max(trees), 'vote': F(1)})
    pd20 = sum(at20) / 6
    num(L2, it, 2, pd20, np.mean(np.array(at20, float)), {'sum': sum(at20), 'first': at20[0], 'five': sum(at20[1:]) / 5})
    pd05 = sum(at05) / 6
    num(L2, it, 3, pd20 - pd05, np.mean(np.array(at20, float) - np.array(at05, float)),
        {'start': pd05, 'ratio': pd20 / pd05, 'sum': pd20 + pd05})
    rise = np.array(at20, float) - np.array(at05, float)
    calm = sum(F(b) - F(a) for a, b in zip(at05[3:], at20[3:])) / 3
    urgent = sum(F(b) - F(a) for a, b in zip(at05[:3], at20[:3])) / 3
    ok(calm == F('0.04') and abs(rise[:3].mean() - 0.46) < 1e-12 and abs(rise[3:].mean() - 0.04) < 1e-12, f'{it}: group rises')
    num(L2, it, 4, 2 * (pd20 - pd05) - calm, rise[:3].mean(), {'pd': pd20 - pd05, 'double': 2 * (pd20 - pd05), 'added': pd20 - pd05 + calm})
    ok(sum(at05[:3]) == F('0.84') and sum(at20[:3]) == F('2.22') and sum(at20[:3]) - sum(at05[:3]) == F('1.38'), f'{it}: explain totals')
    ok(sum(at05) == F('1.20') and sum(at20) == F('2.70'), f'{it}: totals')
    pick(L2, it, 5, 'urgent')

    # p-imbalance-stumps. Method 2: scikit-learn stumps fitted to each resample, repeats as repeated rows.
    it = 'p-imbalance-stumps'
    xs = np.array([-0.6, -0.4, -0.3, 0.2, 0.6, 0.8])
    ys = np.array([-4, -1, -2, 1, 4, 4], float)
    A = [0, 0, 1, 3, 4, 4]
    Bd = [1, 2, 2, 3, 5, 5]

    def stump_by_hand(idx):
        vals = sorted(set(idx), key=lambda i: xs[i])
        best = None
        for k in range(1, len(vals)):
            t = (xs[vals[k - 1]] + xs[vals[k]]) / 2
            L = [F(int(ys[i])) for i in idx if xs[i] <= t]
            R = [F(int(ys[i])) for i in idx if xs[i] > t]
            s = sse(L) + sse(R)
            if best is None or s < best[0]:
                best = (s, t, F(sum(L), len(L)), F(sum(R), len(R)))
        return best

    sa, sb_ = stump_by_hand(A), stump_by_hand(Bd)
    ta = DecisionTreeRegressor(max_depth=1, random_state=0).fit(xs[A].reshape(-1, 1), ys[A])
    tb = DecisionTreeRegressor(max_depth=1, random_state=0).fit(xs[Bd].reshape(-1, 1), ys[Bd])
    ok(abs(ta.tree_.threshold[0] - sa[1]) < 1e-6 and abs(tb.tree_.threshold[0] - sb_[1]) < 1e-6, f'{it}: thresholds')
    ok(abs(sa[1] + 0.1) < 1e-9 and abs(sb_[1] - 0.5) < 1e-9, f'{it}: thresholds -0.1 and 0.5')
    # part 1: a set answer, checked here by hand
    w1 = L2[it]['parts'][0]['widget']
    oobA = sorted(set(range(6)) - set(A))
    ok(sorted(w1['answers']) == oobA == [2, 5], f'{it} p1: answers {w1["answers"]} vs {oobA}')
    ok({x['id']: x['value'] for x in w1['wrong']} == {'repeats': '0, 4', 'drawn-once': '1, 3'}, f'{it} p1: wrongs')
    ok(sorted(set(range(6)) - set(Bd)) == [0, 4] and [i for i in A if A.count(i) == 2][::2] == [0, 4], f'{it} p1: repeats')
    ok(set(L2[it]['parts'][0]['feedback']['byKey']) == {'repeats', 'drawn-once', 'count'}, f'{it} p1: byKey')
    other_a = sorted(float(s) for s in [sse([F(-4)] * 2) + sse([F(-1), F(1), F(4), F(4)]),
                                        sse([F(-4), F(-4), F(-1), F(1)]) + sse([F(4)] * 2)])
    ok(sa[0] == 12 and other_a == [18, 18], f'{it}: tree A errors {sa[0]} {other_a}')
    other_b = [float(sse([F(-1)]) + sse([F(-2), F(-2), F(1), F(4), F(4)])), float(sse([F(-1), F(-2), F(-2)]) + sse([F(1), F(4), F(4)]))]
    ok(sb_[0] == 6 and abs(other_b[0] - 36) < 1e-9 and abs(other_b[1] - 20 / 3) < 1e-9, f'{it}: tree B errors {sb_[0]} {other_b}')
    num(L2, it, 2, sa[3], ta.predict([[0.8]])[0], {'no-repeats': F(1 + 4, 2), 'own-value': 4, 'no-split': F(int(ys[A].sum()), 6)},
        round_tol=0.05)
    num(L2, it, 3, sb_[2], tb.predict([[-0.6]])[0], {'no-repeats': F(-1 - 2 + 1, 3), 'own-value': -4,
                                                     'wrong-split': F(-1 - 2 - 2, 3), 'sign': 1}, round_tol=0.005)
    oob_pred = {2: ta.predict([[xs[2]]])[0], 5: ta.predict([[xs[5]]])[0], 0: tb.predict([[xs[0]]])[0], 4: tb.predict([[xs[4]]])[0]}
    errs = {i: (ys[i] - v) ** 2 for i, v in oob_pred.items()}
    exact_mse = (F(-2 - (-3)) ** 2 + F(4 - 3) ** 2 + F(-4 - (-1)) ** 2 + F(4 - 4) ** 2) / 4
    num(L2, it, 4, exact_mse, np.mean(list(errs.values())), {'all-six': exact_mse * 4 / 6, 'sum': exact_mse * 4,
                                                             'unsquared': F(1 + 1 + 3 + 0, 4)}, round_tol=0.005)
    num(L2, it, 5, (sa[3] + sb_[2]) / 2, (ta.predict([[0.3]])[0] + tb.predict([[0.3]])[0]) / 2,
        {'tree-a': sa[3], 'tree-b': sb_[2], 'sum': sa[3] + sb_[2]})

# ---------------------------------------------------------------- level 3
L3 = load(3)
if L3:
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
    from sklearn.model_selection import TimeSeriesSplit
    from statsmodels.stats.proportion import proportions_ztest

    # p-fill-times. Method 2: scikit-learn's GradientBoostingRegressor, read stage by stage.
    it = 'p-fill-times'
    tk = np.arange(1, 6, dtype=float).reshape(-1, 1)
    ft = [4, 5, 9, 16, 21]
    nu = F(1, 10)
    F0 = F(sum(ft), 5)
    r0 = [F(v) - F0 for v in ft]
    splits0 = {k: sse(r0[:k]) + sse(r0[k:]) for k in range(1, 5)}
    ok(min(splits0, key=splits0.get) == 3 and splits0[3] == F(53, 2), f'{it}: first split {splits0}')
    leftleaf = F(sum(r0[:3]), 3)
    rightleaf = F(sum(r0[3:]), 2)
    F1 = [F0 + nu * (leftleaf if i < 3 else rightleaf) for i in range(5)]
    r1 = [F(v) - f for v, f in zip(ft, F1)]
    splits1 = {k: sse(r1[:k]) + sse(r1[k:]) for k in range(1, 5)}
    ok(min(splits1, key=splits1.get) == 3, f'{it}: second split {splits1}')
    F2_left = F1[0] + nu * F(sum(r1[:3]), 3)
    gbr = GradientBoostingRegressor(n_estimators=2, max_depth=1, learning_rate=0.1, random_state=0).fit(tk, ft)
    stages = list(gbr.staged_predict(tk))
    ok(abs(gbr.init_.constant_.ravel()[0] - float(F0)) < 1e-12, f'{it}: init')
    stump1 = gbr.estimators_[0, 0].tree_
    ok(abs(stump1.threshold[0] - 3.5) < 1e-6, f'{it}: sklearn split {stump1.threshold[0]}')
    sk_leaf = gbr.estimators_[0, 0].predict([[1.0]])[0]
    sse0 = sum((F(v) - F0) ** 2 for v in ft)
    sse1 = sum(r * r for r in r1)
    num(L3, it, 1, F0, gbr.init_.constant_.ravel()[0], {'median': 9, 'zero': 0, 'midrange': F(4 + 21, 2)})
    num(L3, it, 2, leftleaf, sk_leaf, {'times': F(4 + 5 + 9, 3), 'sign': -leftleaf, 'shrunk': nu * leftleaf})
    num(L3, it, 3, F1[0], stages[0][0], {'full-step': F0 + leftleaf, 'sign': F0 - nu * leftleaf, 'from-zero': nu * leftleaf})
    num(L3, it, 4, sse1, float(np.sum((np.array(ft) - stages[0]) ** 2)), {'full-step': splits0[3], 'before': sse0,
                                                                          'mean': sse1 / 5})
    num(L3, it, 5, F2_left, stages[1][0], {'same-step': F1[0] + nu * leftleaf, 'full-step': F1[0] + F(sum(r1[:3]), 3),
                                           'unchanged': F1[0]})
    ok(F1[3] == F(47, 4) and [float(r) for r in r1] == [-6.5, -5.5, -1.5, 4.25, 9.25], f'{it}: residuals in feedback')
    ok(splits0[1] > splits0[3] and splits0[2] > splits0[3] and splits0[4] > splits0[3], f'{it}: least of four')

    # p-callable-bonds. Method 2: scikit-learn's GradientBoostingClassifier with one stump.
    it = 'p-callable-bonds'
    xb = np.array([1, 2, 3, 4, 5, 10, 10, 10], float).reshape(-1, 1)
    yb2 = np.array([0, 0, 0, 0, 0, 1, 1, 0])
    gbc = GradientBoostingClassifier(n_estimators=1, max_depth=1, learning_rate=0.1, random_state=0).fit(xb, yb2)
    base = gbc.decision_function(xb[:1])[0] - gbc.estimators_[0, 0].predict(xb[:1])[0] * 0.1
    lf0 = math.log(0.25 / 0.75)
    newton = F(F(3, 4) + F(3, 4) - F(1, 4)) / (3 * F(1, 4) * F(3, 4))
    sk_leaf = gbc.estimators_[0, 0].predict([[10.0]])[0]
    F1b = lf0 + 0.1 * float(newton)
    num(L3, it, 1, lf0, base, {'rate': 0.25, 'sign': -lf0, 'odds': F(1, 3)}, round_tol=0.00005)
    num(L3, it, 2, F(3, 4), 1 - 1 / (1 + math.exp(-base)), {'slope': F(-3, 4), 'p': F(1, 4), 'log-odds': 1 - lf0})
    num(L3, it, 3, newton, sk_leaf, {'mean-residual': F(5, 12), 'sum': F(5, 4), 'one-weight': F(5, 4) / F(3, 16)},
        round_tol=0.00005)
    num(L3, it, 4, F1b, gbc.decision_function([[10.0]])[0], {'full-step': lf0 + float(newton), 'carried': lf0 + 0.1 * 5 / 12,
                                                             'sign': lf0 - 0.1 * float(newton), 'abs': -F1b},
        round_tol=0.00005)
    num(L3, it, 5, 1 / (1 + math.exp(-F1b)), gbc.predict_proba([[10.0]])[0, 1],
        {'sign': 1 / (1 + math.exp(F1b)), 'added-p': 0.25 + 0.2222, 'carried': 1 / (1 + math.exp(-(lf0 + float(newton))))},
        round_tol=0.00005)
    ok(abs(math.exp(0.8764) - 2.4022) < 0.00005 and abs(1 + math.exp(0.8764) - 3.4022) < 0.00005, f'{it}: e^0.8764 in feedback')

    # p-futures-study. Method 2: scikit-learn's TimeSeriesSplit, statsmodels' z test with the null variance, a P&L in NumPy.
    it = 'p-futures-study'
    folds = list(TimeSeriesSplit(n_splits=4, test_size=60, gap=2).split(np.zeros(700)))
    tr0, te0 = folds[0]
    ok(te0[0] == 460 and te0[-1] == 519 and sum(len(te) for _, te in folds) == 240, f'{it}: test blocks')
    num(L3, it, 1, 460 - 2 - 1, tr0[-1], {'no-gap': 459, 'gap-one': 458, 'test-row': 460})
    h, b, n = F(138, 240), F(126, 240), 240
    t_exact = float(h - b) / math.sqrt(float(b * (1 - b)) / n)
    z, _ = proportions_ztest(138, 240, value=float(b), prop_var=float(b))
    num(L3, it, 2, t_exact, z, {'fifty': float(h - F(1, 2)) / math.sqrt(0.25 / n), 'one-day': float(h - b) / math.sqrt(float(b * (1 - b))),
                                'hit-se': float(h - b) / math.sqrt(float(h * (1 - h)) / n)}, round_tol=0.005)
    unit = F(2_000_000) * F(7, 10000)
    move = F(2_000_000) * F(8, 1000)
    gross_day = (F(138, 240) - (1 - F(138, 240))) * move
    sim = np.array([1.0] * 575 + [-1.0] * 425).mean() * 16000
    ok(abs(float(gross_day) - sim) < 1e-6, f'{it}: gross per day by enumeration')
    num(L3, it, 3, gross_day, sim, {'edge-only': F(5, 100) * move, 'half': F(75, 1000) * move, 'hit-only': F(575, 1000) * move})
    ok(F(138, 240) == F(575, 1000), f'{it}: hit rate 0.575')
    cost_day = F(1, 4) * 2 * unit
    flips = np.array([1] * 250 + [0] * 750)
    sim_cost = (flips * 2 * 1400.0).mean()
    ok(abs(float(cost_day) - sim_cost) < 1e-9 and cost_day == 700, f'{it}: cost per day')
    num(L3, it, 4, gross_day - cost_day, sim - sim_cost, {'gross': gross_day, 'flip-one': gross_day - F(1, 4) * unit, 'every-day': gross_day - 2 * unit})
    pick(L3, it, 5, 'not-shown')
    base_gross = (F(126, 240) - (1 - F(126, 240))) * move
    ok(base_gross == 800 and base_gross - cost_day == 100 and 240 * (gross_day - cost_day) == 408000, f'{it}: p5 at the base rate nets 100; 240 days at 1700 is 408000')
    ok(round(float(cost_day / gross_day), 2) == 0.29, f'{it}: costs take 29 per cent of gross')

    # p-surprise-drift. Method 2: scikit-learn boosting on 40 weeks (10 per cell, no noise).
    it = 'p-surprise-drift'
    cells = {(1, 1): 14, (0, 1): -10, (1, 0): 2, (0, 0): 2}   # (positive surprise, small company): mean return
    Xs = np.array([k for k in cells for _ in range(10)], float)
    ysd = np.array([cells[k] for k in cells for _ in range(10)], float)
    g1 = GradientBoostingRegressor(n_estimators=1, max_depth=1, learning_rate=1.0, random_state=0).fit(Xs, ysd)
    ok(g1.estimators_[0, 0].tree_.feature[0] == 0, f'{it}: first stump splits on the surprise')
    pred1 = g1.predict(Xs)
    g50 = GradientBoostingRegressor(n_estimators=50, max_depth=1, learning_rate=0.1, random_state=0).fit(Xs, ysd)
    gd2 = GradientBoostingRegressor(n_estimators=50, max_depth=2, learning_rate=0.5, random_state=0).fit(Xs, ysd)
    mse50 = float(np.mean((ysd - g50.predict(Xs)) ** 2))
    msed2 = float(np.mean((ysd - gd2.predict(Xs)) ** 2))
    ok(mse50 > 35.9 and msed2 < 1e-6, f'{it}: stumps stall at {mse50}, depth 2 reaches {msed2}')
    mean0 = F(sum(cells.values()), 4)
    pos_leaf = F(cells[(1, 1)] + cells[(1, 0)], 2) - mean0
    size_leaf = F(cells[(1, 1)] + cells[(0, 1)], 2) - mean0
    ok(size_leaf == 0 and F(cells[(1, 0)] + cells[(0, 0)], 2) - mean0 == 0, f'{it}: size split gains nothing')
    f_sp = mean0 + pos_leaf
    mse_after = sum((F(v) - (mean0 + (pos_leaf if k[0] else -pos_leaf))) ** 2 for k, v in cells.items()) / 4
    mse_before = sum((F(v) - mean0) ** 2 for v in cells.values()) / 4
    num(L3, it, 1, mean0, g1.init_.constant_.ravel()[0], {'zero': 0, 'positive-only': F(14 + 2, 2), 'no-sign': F(14 + 10 + 2 + 2, 4)})
    num(L3, it, 2, pos_leaf, g1.estimators_[0, 0].predict([[1.0, 1.0]])[0], {'mean-not-residual': F(14 + 2, 2),
                                                                             'small-only': 14 - mean0, 'sign': -pos_leaf})
    num(L3, it, 3, f_sp, g1.predict([[1.0, 1.0]])[0], {'truth': 14, 'leaf-only': pos_leaf, 'carried': mean0 + F(14 + 2, 2)})
    num(L3, it, 4, mse_after, float(np.mean((ysd - pred1) ** 2)), {'unsquared': 6, 'sum': mse_after * 4, 'before': mse_before})
    ok(mean0 - pos_leaf == -4, f'{it}: negative-surprise forecast')
    pick(L3, it, 5, 'depth')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
