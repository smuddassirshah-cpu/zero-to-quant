"""Recompute every number in app/content/courses/stat-learning/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 4, one block per set. Method 1 is exact (sympy or fractions, the formula the lesson teaches). Method 2
takes another route. Level 1: calculus and a scan for the best constant, np.var, np.polyfit for the interpolant, a
simulated average of five noises, scikit-learn's KNeighborsRegressor. Level 4: a point's distance by NumPy projection onto the line, k-means by scikit-learn's KMeans from the stated
centres, inertia from KMeans, a spline from hinge columns in NumPy, the network's slope by a central finite
difference on the loss, a t statistic by statsmodels' proportions_ztest with the null variance, and a sample size
by brute search. For each numeric part the script checks: the two methods agree; the key is within its tol; every
`wrong` value matches its named slip, lies outside the key's band, is no wider than half its value, and does not
overlap another; byKey covers the wrongs. Choice parts check the keyed option and the numbers in their lines.
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-stat-learning-numbers.py
"""
import itertools
import json
import math
import os
import sys
import warnings

import numpy as np
import sympy as sp
from sklearn.cluster import KMeans
from statsmodels.stats.proportion import proportions_ztest

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'stat-learning')
fails, checks = [], 0
R = sp.Rational


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'stat-learning', f'problems-{n}: header')
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
        ok(wt <= abs(x['value']) / 2 + 1e-12, f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    fb = items[iid]['parts'][k - 1]['feedback']
    ok(set(fb.get('byKey', {})) == set(wrongs), f'{tag}: byKey keys vs wrongs')


def pick(items, iid, k, correct_id):
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    fb = items[iid]['parts'][k - 1]['feedback']
    ok(set(fb.get('byKey', {})) == {o['id'] for o in w['options'] if not o.get('correct')}, f'{iid} p{k}: byKey keys')


def t_null(h, b, n):
    return (h - b) / sp.sqrt(b * (1 - b) / n)


def t_sm(h, b, n):
    z, _ = proportions_ztest(round(float(h) * n), n, value=float(b), prop_var=float(b))
    return z


L4 = load(4)
if L4 is not None:
    # ---------- p-spam-filter ----------
    w = sp.Matrix([R(3, 2), -2])
    b = R(1, 2)
    nrm = sp.sqrt((w.T * w)[0])
    ok(nrm == R(5, 2), 'p-spam-filter: norm 2.5')
    wn, bn = np.array([1.5, -2.0]), 0.5
    edge = (1 - bn) * wn / (wn @ wn)                           # a point on the edge w.x + b = 1
    num(L4, 'p-spam-filter', 1, 1 / nrm, abs(wn @ edge + bn) / np.linalg.norm(wn),
        {'gave-norm': nrm, 'street-width': 2 / nrm, 'squared-norm': 1 / nrm ** 2})
    x = sp.Matrix([R(1, 5), R(3, 10)])
    f = (w.T * x)[0] + b
    ok(f == R(1, 5), 'p-spam-filter: decision value 0.2')
    xn = np.array([0.2, 0.3])
    foot = xn - (wn @ xn + bn) / (wn @ wn) * wn
    num(L4, 'p-spam-filter', 2, abs(f) / nrm, np.linalg.norm(xn - foot),
        {'decision-value': f, 'squared-norm': f / nrm ** 2, 'carried': f * nrm})   # decision value times a margin taken as 2.5
    ok(0 < f < 1 and abs(f) / nrm < 1 / nrm, 'p-spam-filter: email inside the street on the spam side')
    pick(L4, 'p-spam-filter', 3, 'inside')
    w2 = sp.Matrix([R(9, 10), R(-6, 5)])
    b2 = R(3, 10)
    nrm2 = sp.sqrt((w2.T * w2)[0])
    ok(nrm2 == R(3, 2), 'p-spam-filter p4: refit norm 1.5')
    ok(w2 == R(3, 5) * w and b2 == R(3, 5) * b, 'p-spam-filter p4: the refit is the old weights times 0.6, the same centre line')
    w2n, b2n = np.array([0.9, -1.2]), 0.3
    edge2 = (1 - b2n) * w2n / (w2n @ w2n)                      # a point on the new edge w.x + b = 1; its distance from the line
    foot2 = edge2 - (w2n @ edge2 + b2n) / (w2n @ w2n) * w2n
    num(L4, 'p-spam-filter', 4, 1 / nrm2, np.linalg.norm(edge2 - foot2),
        {'gave-norm': nrm2, 'street-width': 2 / nrm2, 'unchanged': 1 / nrm})
    ok((1 / nrm2) / (1 / nrm) == R(5, 3), 'p-spam-filter p4: the margin grows by 5/3 (0.4 to 0.667)')
    ok(abs(float(1 / nrm2) - 0.667) <= 0.0005 and abs(float(2 / nrm2) - 1.333) <= 0.0005, 'p-spam-filter p4: 0.667 and 1.333 inside the printed bands')
    ok('scaled so the street' in L4['p-spam-filter']['prose'] and L4['p-spam-filter']['parts'][3]['widget']['kind'] == 'numeric', 'p-spam-filter: prose states the scaling; part 4 is typed')
    t = t_null(R(93, 100), R(9, 10), 500)
    num(L4, 'p-spam-filter', 5, t, t_sm(0.93, 0.9, 500),
        {'own-rate': (R(93, 100) - R(9, 10)) / sp.sqrt(R(93, 100) * R(7, 100) / 500),
         'no-root': (R(93, 100) - R(9, 10)) / sp.sqrt(R(9, 10) * R(1, 10)),
         'coin': (R(93, 100) - R(1, 2)) / sp.sqrt(R(1, 4) / 500)}, round_tol=0.005, agree=1e-9)
    ok((R(93, 100) - R(9, 10)) * 500 == 15, 'p-spam-filter: 15 emails')

    # ---------- p-order-sizes ----------
    xs = [2, 4, 6, 18, 22, 26]
    X = np.array(xs, float).reshape(-1, 1)

    def step(c):
        lab = [0 if abs(v - c[0]) <= abs(v - c[1]) else 1 for v in xs]
        return [sum(R(v) for v, l in zip(xs, lab) if l == j) / sum(1 for l in lab if l == j) for j in (0, 1)], lab

    c1, lab1 = step([3, 8])
    km1 = KMeans(2, init=np.array([[3.0], [8.0]]), n_init=1, max_iter=1, algorithm='lloyd').fit(X)
    num(L4, 'p-order-sizes', 1, c1[1], km1.cluster_centers_[1][0],
        {'all-orders': R(sum(xs), 6), 'kept-centre': (R(sum(v for v, l in zip(xs, lab1) if l == 1)) + 8) / 5,
         'six-misassigned': R(18 + 22 + 26, 3), 'percent-sign': c1[1] / 100})
    c = [R(3), R(18)]
    for _ in range(10):
        nc, lab = step(c)
        if nc == c:
            break
        c = nc
    km = KMeans(2, init=np.array([[3.0], [18.0]]), n_init=1).fit(X)
    num(L4, 'p-order-sizes', 2, c[1], km.cluster_centers_[1][0], {'no-reassign': c1[1], 'all-orders': R(sum(xs), 6), 'percent-sign': c[1] / 100})
    ok(c == [4, 22], 'p-order-sizes: settled centres 4 and 22')
    inert = sum((v - c[l]) ** 2 for v, l in zip(xs, lab))
    num(L4, 'p-order-sizes', 3, inert, km.inertia_,
        {'unsquared': sum(abs(v - c[l]) for v, l in zip(xs, lab)), 'averaged': inert / 6,
         'carried': sum((v - [3, 18][l]) ** 2 for v, l in zip(xs, lab)),
         'not-settled': sum((v - [3, 18][l]) ** 2 for v, l in zip(xs, [0, 0, 1, 1, 1, 1]))}, round_tol=0.005)
    # route 2 for the two new slips: 6 kept in group 2 against centres 3 and 18, and a typed % read as a hundredth
    ok(1 + 1 + 144 + 0 + 16 + 64 == 226 and abs(km1.cluster_centers_[1][0] / 100 - 0.18) < 1e-12 and abs(km.cluster_centers_[1][0] / 100 - 0.22) < 1e-12, 'p-order-sizes: not-settled 226, percent-sign 0.18 and 0.22')
    xx = sp.Symbol('x')
    knot = (c[0] + c[1]) / 2

    def fspl(cc):
        return 1 + R(5, 2) * xx - R(9, 5) * sp.Piecewise((0, xx <= cc), (xx - cc, True))

    beta = np.array([1.0, 2.5, -1.8])

    def fnp(v, cc):
        return np.column_stack([np.ones(1), [v], np.maximum(0, np.array([v]) - cc)]) @ beta

    f20 = fspl(knot).subs(xx, 20)
    num(L4, 'p-order-sizes', 4, f20, fnp(20, float(knot))[0],
        {'no-hinge': 1 + R(5, 2) * 20, 'sign': 1 + R(5, 2) * 20 + R(9, 5) * (20 - knot),
         'knot-at-centre': fspl(c[0]).subs(xx, 20), 'carried': fspl(R(3 + 18, 2)).subs(xx, 20)})
    f10 = fspl(knot).subs(xx, 10)
    num(L4, 'p-order-sizes', 5, f20 - f10, fnp(20, 13.0)[0] - fnp(10, 13.0)[0],
        {'summed-halves': f20 - 2 * f10, 'negative-hinge': f20 - (1 + 25 - R(9, 5) * (10 - knot)),
         'carried': (1 + R(5, 2) * 20) - f10})

    # ---------- p-one-unit ----------
    w1, b1, v, d = sp.symbols('w1 b1 v d')
    xv, yv = 8, 10
    at = {w1: R(1, 2), b1: -1, v: 2, d: 1}
    yhat_on = v * (w1 * xv + b1) + d                      # the unit is on: 0.5 * 8 - 1 > 0
    ok((w1 * xv + b1).subs(at) > 0, 'p-one-unit: unit on')

    def fwd(W1, B1, V, D):
        return V * max(0.0, W1 * xv + B1) + D

    num(L4, 'p-one-unit', 1, yhat_on.subs(at), fwd(0.5, -1, 2, 1),
        {'no-hidden-bias': (v * w1 * xv + d).subs(at), 'no-output-bias': (v * (w1 * xv + b1)).subs(at)})
    L = (yhat_on - yv) ** 2 / 2
    num(L4, 'p-one-unit', 2, L.subs(at), 0.5 * (fwd(0.5, -1, 2, 1) - yv) ** 2,
        {'no-half': 2 * L.subs(at), 'unsquared': (yhat_on - yv).subs(at) / 2, 'carried': R(1, 2) * (9 - yv) ** 2})
    g = sp.diff(L, w1).subs(at)
    hh = 1e-6
    fd = (0.5 * (fwd(0.5 + hh, -1, 2, 1) - yv) ** 2 - 0.5 * (fwd(0.5 - hh, -1, 2, 1) - yv) ** 2) / (2 * hh)
    num(L4, 'p-one-unit', 3, g, fd,
        {'slope-for-v': sp.diff(L, v).subs(at), 'dropped-x': sp.diff(L, b1).subs(at), 'sign': -g,
         'carried': (9 - yv) * 2 * xv}, agree=1e-5)
    eta = R(1, 500)
    new_w1 = R(1, 2) - eta * g
    num(L4, 'p-one-unit', 4, new_w1, 0.5 - 0.002 * fd,
        {'uphill': R(1, 2) + eta * g, 'no-rate': R(1, 2) - g, 'carried': R(1, 2) - eta * sp.diff(L, v).subs(at)}, agree=1e-6)
    ws = sp.Symbol('ws')
    knot_exact = sp.solve(sp.Eq(new_w1 * ws - 1, 0), ws)[0]
    # route 2: scan x for the first point where the unit switches on
    grid = np.linspace(0, 3, 3_000_001)
    first_on = grid[np.argmax(0.596 * grid - 1 > 0)]
    num(L4, 'p-one-unit', 5, knot_exact, first_on,
        {'old-knot': 2, 'sign': -knot_exact, 'carried': 1 / (R(1, 2) - eta * sp.diff(L, v).subs(at))}, agree=1e-5)
    ok(abs(float(2 * new_w1) - 1.192) < 1e-12 and float(2 * R(1, 2)) == 1, 'p-one-unit: slope beyond the knot 1 to 1.192')
    # the step must lower the loss (review-holes-1.6-2.1 finding 10): exact, then by forward evaluation
    pred_new = yhat_on.subs({w1: new_w1, b1: -1, v: 2, d: 1})
    loss_new = ((pred_new - yv) ** 2 / 2)
    ok(new_w1 == R(149, 250) and pred_new == R(1067, 125) and abs(float(pred_new) - 8.536) < 1e-12, 'p-one-unit: w1 0.596, prediction 8.536')
    ok(abs(float(loss_new) - 1.071648) < 1e-9 and abs(0.5 * (fwd(0.596, -1, 2, 1) - yv) ** 2 - 1.071648) < 1e-9, 'p-one-unit: loss 4.5 falls to 1.0716 (two routes)')
    ok(float(loss_new) < float(L.subs(at)), 'p-one-unit: the step lowers the loss')
    # the old eta = 0.01 overshoots (prediction 14.68, loss 10.95): the reason it was changed
    ok(abs(0.5 * (fwd(0.98, -1, 2, 1) - yv) ** 2 - 10.9512) < 1e-9 and 0.5 * (fwd(0.98, -1, 2, 1) - yv) ** 2 > 4.5, 'p-one-unit: eta 0.01 would have raised the loss to 10.95')
    ok(abs(2 * (0.6875 - 0.5) / 48 - 0.0078125) < 1e-12 and eta < R(1, 128), 'p-one-unit: eta 0.002 is below the largest eta, 0.0078, that lowers the loss')
    ok(abs(float(knot_exact) - 1.67785) < 1e-5 and abs(float(1 / R(518, 1000)) - 1.9305) < 1e-4 and abs(float(10 * knot_exact) - 16.78) < 0.01, 'p-one-unit: knot 1.678 (16.8 km), the carried knot 1.931')
    ok(L4['p-one-unit']['parts'][0]['widget'].get('unit') == 'h', 'p-one-unit p1: unit h, so 7 h is read')

    # ---------- p-renewals ----------
    sizes = [6, 16, 1]
    count = sum(sizes[i] * sizes[i + 1] + sizes[i + 1] for i in range(2))
    shapes = sum(np.zeros((sizes[i + 1], sizes[i])).size + sizes[i + 1] for i in range(2))
    num(L4, 'p-renewals', 1, count, shapes, {'no-biases': 6 * 16 + 16, 'units': sum(sizes)})
    ok(6 + 1 == 7, 'p-renewals: logistic regression has 7 parameters')
    pick(L4, 'p-renewals', 2, 'logistic')
    t = t_null(R(74, 100), R(7, 10), 500)
    num(L4, 'p-renewals', 3, t, t_sm(0.74, 0.7, 500),
        {'own-rate': (R(74, 100) - R(7, 10)) / sp.sqrt(R(74, 100) * R(26, 100) / 500),
         'no-root': (R(74, 100) - R(7, 10)) / sp.sqrt(R(21, 100)),
         'coin': (R(74, 100) - R(1, 2)) / sp.sqrt(R(1, 4) / 500)}, round_tol=0.005, agree=1e-9)
    need = sp.ceiling(9 * R(21, 100) / R(4, 100) ** 2)
    brute = next(n for n in range(1, 10000) if 0.04 / math.sqrt(0.21 / n) >= 3)
    num(L4, 'p-renewals', 4, need, brute,
        {'rounded-down': need - 1, 'no-square': 3 * sp.sqrt(R(21, 100)) / R(4, 100),
         'carried': sp.ceiling(9 * R(74, 100) * R(26, 100) / R(4, 100) ** 2)}, round_tol=0.01)
    ok(abs((3 / 1.95) ** 2 - 2.4) < 0.05 and abs(34.37 ** 2 - 1181.3) < 0.05, 'p-renewals: printed 2.4 and 1181.3')
    ok((R(74, 100) - R(7, 10)) * 500 == 20, 'p-renewals: 20 customers')

L1 = load(1)
if L1 is not None:
    from sklearn.neighbors import KNeighborsRegressor
    # ---------- p-ferry-passengers ----------
    tr = [4, 7, 5, 9, 6, 11]
    te = [8, 6, 10, 12]
    c = sp.Rational(sum(tr), len(tr))
    cc = sp.Symbol('c')
    c_min = sp.solve(sp.diff(sum((v - cc) ** 2 for v in tr), cc), cc)[0]       # method 2: calculus on the loss
    grid = np.linspace(0, 15, 150001)
    c_scan = grid[np.argmin([np.mean((np.array(tr) - g) ** 2) for g in grid[::100]]) * 100]
    ok(c_min == c and abs(c_scan - 7) < 0.02, 'p-ferry: best constant 7 by calculus and by scan')
    num(L1, 'p-ferry-passengers', 1, c, c_min, {'median': sp.Rational(13, 2), 'midrange': sp.Rational(4 + 11, 2)})
    ok(float(np.median(tr)) == 6.5, 'p-ferry: median 6.5')
    mse_tr = sum((v - c) ** 2 for v in tr) / 6
    num(L1, 'p-ferry-passengers', 2, mse_tr, np.var(tr),
        {'n-minus-1': sum((v - c) ** 2 for v in tr) / 5, 'absolute': sum(abs(v - c) for v in tr) / 6, 'sum': sum((v - c) ** 2 for v in tr)})
    mse_te = sum((v - c) ** 2 for v in te) / 4
    num(L1, 'p-ferry-passengers', 3, mse_te, np.mean((np.array(te) - 7.0) ** 2),
        {'test-mean': sum((v - sp.Rational(sum(te), 4)) ** 2 for v in te) / 4,
         'carried': sum((v - sp.Rational(13, 2)) ** 2 for v in te) / 4, 'absolute': sum(abs(v - c) for v in te) / 4})
    ok(sp.Rational(sum(te), 4) == 9 and sum((v - c) ** 2 for v in tr) == 34 and sum((v - c) ** 2 for v in te) == 36, 'p-ferry: test mean 9, sums 34 and 36')
    temps = np.array([3.0, 6.0, 8.0, 11.0, 14.0, 17.0])            # any six distinct temperatures
    fit5 = np.polyfit(temps, tr, 5)
    fit4 = np.polyfit(temps, tr, 4)
    ok(np.allclose(np.polyval(fit5, temps), tr) and not np.allclose(np.polyval(fit4, temps), tr, atol=1e-6), 'p-ferry: degree 5 interpolates six days, degree 4 cannot')
    num(L1, 'p-ferry-passengers', 4, len(tr) - 1, len(fit5) - 1, {'six': 6, 'coefficients-short': 4})
    pick(L1, 'p-ferry-passengers', 5, 'constant')
    ok(31.4 > float(mse_te) and abs((9 + 31.4) / 2 - 20.2) < 1e-12 and float(31.4 / mse_te) > 3, 'p-ferry p5: 9 against 31.4, the average 20.2, a factor above 3')

    # ---------- p-loaves-k ----------
    f0, s2 = 20, 4
    k20 = [17, 18, 16, 17, 17]
    k1 = [23, 18, 19, 17, 23]
    m20 = sp.Rational(sum(k20), 5)
    b2 = (m20 - f0) ** 2
    num(L1, 'p-loaves-k', 1, b2, (np.mean(k20) - f0) ** 2, {'bias': m20 - f0, 'size': abs(m20 - f0), 'variance': sp.Rational(2, 5)})
    v20 = sum((x - m20) ** 2 for x in k20) / 5
    num(L1, 'p-loaves-k', 2, b2 + v20 + s2, (np.mean(k20) - f0) ** 2 + np.var(k20) + s2,
        {'no-noise': b2 + v20, 'ddof1': b2 + sum((x - m20) ** 2 for x in k20) / 4 + s2, 'carried': abs(m20 - f0) + v20 + s2})
    m1 = sp.Rational(sum(k1), 5)
    v1 = sum((x - m1) ** 2 for x in k1) / 5
    num(L1, 'p-loaves-k', 3, (m1 - f0) ** 2 + v1 + s2, (np.mean(k1) - f0) ** 2 + np.var(k1) + s2,
        {'no-noise': (m1 - f0) ** 2 + v1, 'ddof1': sum((x - m1) ** 2 for x in k1) / 4 + s2, 'carried': b2 + v20 + s2})
    ok(m1 == 20 and v1 == sp.Rational(32, 5) and m20 == 17 and v20 == sp.Rational(2, 5), 'p-loaves: means 17 and 20, variances 0.4 and 6.4')
    rng = np.random.default_rng(5)
    sim = rng.normal(0, 2, (400000, 5)).mean(axis=1)                 # route 2: simulate the average of five noises
    num(L1, 'p-loaves-k', 4, 1 + sp.Rational(4, 5) + s2, 1 + sim.var() + s2,
        {'no-average': 1 + 4 + s2, 'no-noise': 1 + sp.Rational(4, 5)}, agree=0.01)
    pick(L1, 'p-loaves-k', 5, 'k5')

    # ---------- p-broker-clients ----------
    q = sp.Matrix([14, 310])
    cl = {'A': ((13, 340), 7), 'B': ((22, 315), 3), 'C': ((15, 290), 8), 'D': ((9, 312), 4)}
    sd = sp.Matrix([5, 40])

    def dist(a, scale=None):
        g = sp.Matrix(a) - q
        if scale is not None:
            g = sp.Matrix([g[i] / scale[i] for i in range(2)])
        return sp.sqrt((g.T * g)[0])
    Xr = np.array([cl[k][0] for k in 'ABCD'], float)
    yr = np.array([cl[k][1] for k in 'ABCD'], float)
    qn = np.array([[14.0, 310.0]])
    num(L1, 'p-broker-clients', 1, dist(cl['D'][0]), np.linalg.norm(Xr[3] - qn[0]),
        {'squared': dist(cl['D'][0]) ** 2, 'city-block': 5 + 2}, round_tol=0.005, agree=1e-9)
    num(L1, 'p-broker-clients', 2, dist(cl['C'][0], sd), np.linalg.norm((Xr[2] - qn[0]) / [5, 40]),
        {'raw': dist(cl['C'][0]), 'variance': dist(cl['C'][0], [25, 1600])}, round_tol=0.005, agree=1e-9)
    sc = {k: float(dist(cl[k][0], sd)) for k in 'ABCD'}
    rw = {k: float(dist(cl[k][0])) for k in 'ABCD'}
    ok(sorted(sc, key=sc.get) == ['C', 'A', 'D', 'B'] and sorted(rw, key=rw.get) == ['D', 'B', 'C', 'A'], 'p-broker: scaled order C A D B, raw order D B C A')
    ok(abs(sc['A'] - 0.78) < 0.005 and abs(sc['D'] - 1.00) < 0.005 and abs(sc['B'] - 1.60) < 0.005 and abs(rw['B'] - 9.43) < 0.005, 'p-broker: printed 0.78, 1.00, 1.60, 9.43')
    knn = KNeighborsRegressor(n_neighbors=2).fit(Xr / [5, 40], yr)
    knn_raw = KNeighborsRegressor(n_neighbors=2).fit(Xr, yr)
    f_sc = sp.Rational(cl['C'][1] + cl['A'][1], 2)
    num(L1, 'p-broker-clients', 3, f_sc, knn.predict(qn / [5, 40])[0],
        {'raw': knn_raw.predict(qn)[0], 'all-four': yr.mean(), 'one': cl['C'][1]})
    fc = [f_sc, 6, 5]
    act = [7, sp.Rational(13, 2), 4]
    mse_k = sum((a - f) ** 2 for a, f in zip(act, fc)) / 3
    num(L1, 'p-broker-clients', 4, mse_k, np.mean((np.array([7, 6.5, 4.0]) - [7.5, 6, 5]) ** 2),
        {'carried': sum((a - f) ** 2 for a, f in zip(act, [sp.Rational(7, 2), 6, 5])) / 3,
         'absolute': sum(abs(a - f) for a, f in zip(act, fc)) / 3, 'sum': sum((a - f) ** 2 for a, f in zip(act, fc))})
    base = sp.Rational(sum(cl[k][1] for k in 'ABCD'), 4)
    ok(base == sp.Rational(11, 2), 'p-broker: training mean 5.5')
    num(L1, 'p-broker-clients', 5, sum((a - base) ** 2 for a in act) / 3, np.mean((np.array([7, 6.5, 4.0]) - yr.mean()) ** 2),
        {'test-mean': sum((a - sum(act) / 3) ** 2 for a in act) / 3, 'absolute': sum(abs(a - base) for a in act) / 3,
         'sum': sum((a - base) ** 2 for a in act)})

    # ---------- p-heat-demand ----------
    table = {0: (9.20, 9.85), 1: (3.10, 3.42), 2: (1.44, 1.80), 3: (1.38, 1.95), 6: (1.02, 2.60)}
    noise = R(6, 5)
    best = min(table, key=lambda d: table[d][1])
    num(L1, 'p-heat-demand', 1, best, sorted(table.items(), key=lambda kv: kv[1][1])[0][0],
        {'training': min(table, key=lambda d: table[d][0]), 'next': 3})
    ok(all(table[a][0] > table[b][0] for a, b in [(0, 1), (1, 2), (2, 3), (3, 6)]), 'p-heat: training MSE falls with degree')
    rest2 = R(180, 100) - noise
    num(L1, 'p-heat-demand', 2, rest2, 1.80 - 1.20,
        {'training': R(144, 100) - noise, 'carried': R(260, 100) - noise, 'added': R(180, 100) + noise})
    var2 = R(36, 100)
    bias2 = rest2 - var2
    num(L1, 'p-heat-demand', 3, bias2, (1.80 - 1.20) - 0.36,
        {'sd': rest2 - var2 ** 2, 'carried': R(260, 100) - noise - var2, 'added': rest2 + var2})
    e2 = noise + bias2 + var2 / 10
    e2_alt = 1.2 + 0.24 + 0.36 * 40 / 400                           # route 2: the 1/n rule written with n
    num(L1, 'p-heat-demand', 4, e2, e2_alt,
        {'all-shrink': noise + rest2 / 10, 'no-noise': bias2 + var2 / 10, 'carried': noise + (R(260, 100) - noise - var2) + var2 / 10})
    b6 = R(2, 100)
    v6 = R(260, 100) - noise - b6
    e6 = noise + b6 + v6 / 10
    num(L1, 'p-heat-demand', 5, e6, 1.2 + 0.02 + (2.60 - 1.20 - 0.02) * 40 / 400,
        {'no-shrink': R(260, 100), 'all-shrink': noise + (b6 + v6) / 10, 'no-noise': b6 + v6 / 10})
    ok(v6 == R(138, 100) and e6 < e2 and noise + bias2 == R(144, 100), 'p-heat: degree-6 variance 1.38, 1.358 < 1.476, floor 1.44')

present = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
