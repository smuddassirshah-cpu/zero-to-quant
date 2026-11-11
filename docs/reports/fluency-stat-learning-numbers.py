"""Recompute the Fluency sets of stat-learning from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-stat-learning-numbers.py [--n 200]
Level 4 sets (l15, l16, l17, l18). Each key is rebuilt by a route of its own, never from the family's `let`:
the margin as the distance from the centre line to a point placed on the edge w.x + b = 1; a point's distance
by projecting it onto the line with NumPy; one k-means step with scikit-learn's KMeans (one iteration from the
given centres); a group's inertia with scikit-learn; linkage distances with SciPy's `linkage`; the network by a
NumPy forward pass and sympy's derivative of the loss; spline values and slopes from a sympy Piecewise; the
coefficient count as the rank of a truncated-power basis on 400 points. Checks are in fluency_check.py.
"""
import os
import sys
import warnings

import numpy as np
import sympy as sp
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import KMeans

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402

warnings.filterwarnings('ignore')
R = sp.Rational


def f(v):
    return float(v)


# ---- l15: margins and decision values ----
def margin(V):
    w = np.array([f(V['h1']) / 2, f(V['h2']) / 2])
    b = f(V['b'])
    nrm = np.linalg.norm(w)
    edge = (1 - b) * w / nrm ** 2              # a point with w.x + b = 1
    dist = abs(w @ edge + b) / nrm             # its distance from the centre line w.x + b = 0
    key = sp.Float(dist, 30)
    exact = 1 / sp.sqrt((V['h1'] ** 2 + V['h2'] ** 2) / R(4))
    assert abs(f(exact) - dist) < 1e-12
    return exact, {'gave-norm': 1 / exact, 'street-width': 2 * exact}


def decision(V):
    w = sp.Matrix([V['w1'], V['w2']])
    x = sp.Matrix([V['x1'], V['x2']])
    key = (w.T * x)[0] + V['b']
    return key, {'no-intercept': key - V['b'], 'one-term': V['w1'] * V['x1'] + V['b']}


def distance(V):
    w = np.array([f(V['w1']), f(V['w2'])])
    b = f(V['b'])
    x = np.array([f(V['x1']), f(V['x2'])])
    foot = x - (w @ x + b) / (w @ w) * w       # orthogonal projection onto the line
    d = np.linalg.norm(x - foot)
    fval = V['w1'] * V['x1'] + V['w2'] * V['x2'] + V['b']
    nsq = V['w1'] ** 2 + V['w2'] ** 2
    exact = abs(fval) / sp.sqrt(nsq)
    assert abs(f(exact) - d) < 1e-9
    return exact, {'no-norm': abs(fval), 'squared-norm': abs(fval) / nsq}


# ---- l16: centres, inertia and linkage ----
def kmeans_step(V):
    vals = [V['v1']]
    for g in ('g2', 'g3', 'g4', 'g5'):
        vals.append(vals[-1] + V[g])
    c1, c2 = V['c1'], V['c1'] + V['gc']
    X = np.array([[f(v)] for v in vals])
    km = KMeans(2, init=np.array([[f(c1)], [f(c2)]]), n_init=1, max_iter=1, algorithm='lloyd').fit(X)
    # KMeans reports the labels of the last assignment, made with the moved centres; recompute by hand too
    lab = [0 if abs(v - c1) < abs(v - c2) else 1 for v in vals]
    grp = [v for v, l in zip(vals, lab) if l == 1]
    exact = sum(grp) / R(len(grp))
    assert abs(f(exact) - km.cluster_centers_[1][0]) < 1e-9, (exact, km.cluster_centers_)
    return exact, {'all-shares': sum(vals) / R(5), 'kept-centre': (sum(grp) + c2) / R(len(grp) + 1)}


def group_ss(V):
    m = V['m']
    e = [V['e1'], V['e2'], V['e3']]
    xs = [m + ei for ei in e] + [m - sum(e)]
    X = np.array([[f(x)] for x in xs])
    km = KMeans(1, n_init=1).fit(X)
    exact = sum((x - sum(xs) / R(4)) ** 2 for x in xs)
    assert abs(km.inertia_ - f(exact)) < 1e-6
    return exact, {'unsquared': sum(abs(x - sum(xs) / R(4)) for x in xs), 'averaged': exact / 4}


def linkage_dist(V):
    da, db = V['da'] / R(100), V['db'] / R(100)
    meth = {0: 'single', 1: 'complete', 2: 'average'}[int(V['code'])]
    # three points: A, B close together (merge first), C; condensed distances AB, AC, BC
    cond = np.array([0.01, f(da), f(db)])
    Z = linkage(cond, method=meth)
    got = Z[1, 2]
    exact = {'single': min(da, db), 'complete': max(da, db), 'average': (da + db) / 2}[meth]
    assert abs(got - f(exact)) < 1e-12
    w = {}
    if meth != 'single':
        w['nearest'] = min(da, db)
    if meth != 'complete':
        w['farthest'] = max(da, db)
    if meth != 'average':
        w['averaged'] = (da + db) / 2
    return exact, w


# ---- l17: a forward pass and one step ----
def forward(V):
    W1 = np.array([[f(V['a1']), f(V['a2'])], [f(V['b1']), f(V['b2'])]])
    c = np.array([f(V['c1']), f(V['c2'])])
    v = np.array([f(V['v1']), f(V['v2'])])
    x = np.array([f(V['x1']), f(V['x2'])])
    pre = W1 @ x + c
    z = v @ np.maximum(0, pre) + f(V['d'])
    exact = sp.Integer(int(round(z)))
    assert abs(z - int(round(z))) < 1e-12
    return exact, {'no-relu': int(round(v @ pre + f(V['d']))), 'no-output-bias': exact - V['d']}


def params(V):
    a, b, c = int(V['a']), int(V['b']), int(V['c'])
    sizes = [a, b, c]
    # count the entries of each weight matrix and bias vector
    exact = sum(np.zeros((sizes[i + 1], sizes[i])).size + np.zeros(sizes[i + 1]).size for i in range(2))
    return sp.Integer(exact), {'no-biases': a * b + b * c, 'units': a + b + c}


w1s, w2s = sp.symbols('w1 w2')


def slope(V):
    x, y = V['x'], V['y']
    yhat = w2s * sp.Max(0, w1s * x)
    L = (yhat - y) ** 2 / 2
    at = {w1s: V['w1'], w2s: V['w2']}
    # the unit is on (w1 x > 0), so differentiate the active branch
    La = (w2s * w1s * x - y) ** 2 / 2
    assert f(V['w1'] * x) > 0
    key = sp.diff(La, w1s).subs(at)
    # finite difference on the full loss as a second route
    h = 1e-6
    Lf = sp.lambdify((w1s, w2s), L)
    fd = (Lf(f(V['w1']) + h, f(V['w2'])) - Lf(f(V['w1']) - h, f(V['w2']))) / (2 * h)
    assert abs(fd - f(key)) < 1e-4
    g2 = sp.diff(La, w2s).subs(at)
    err = (yhat - y).subs(at)
    return key, {'slope-for-w2': g2, 'dropped-w2': err * x}


def step(V):
    w, g, eta = V['w'], V['g'], V['eta']
    # one step of plain gradient descent on L(w) = g * w, whose slope is g everywhere
    ws = sp.Symbol('ws')
    Lw = g * ws
    key = w - eta * sp.diff(Lw, ws)
    return key, {'uphill': w + eta * g, 'no-rate': w - g}


# ---- l18: hinges, slopes and basis counts ----
xs_ = sp.Symbol('x')


def hinge_value(V):
    a, b, d, c, x0 = V['a'], V['b'], V['d'], V['c'], V['x0']
    fx = a + b * xs_ + d * sp.Piecewise((0, xs_ <= c), (xs_ - c, True))
    key = fx.subs(xs_, x0)
    w = {'no-intercept': key - a}
    if x0 > c:
        w['ignored-hinge'] = a + b * x0
    if x0 < c:
        w['hinge-on-left'] = a + b * x0 + d * (x0 - c)
    return key, w


def slope_region(V):
    b, d1, d2 = V['bh'] / R(2), V['d1h'] / R(2), V['d2h'] / R(2)
    k1 = V['k1']
    k2 = k1 + V['gap']
    fx = b * xs_ + d1 * sp.Piecewise((0, xs_ <= k1), (xs_ - k1, True)) + d2 * sp.Piecewise((0, xs_ <= k2), (xs_ - k2, True))
    r = int(V['r'])
    at = (k1 + k2) / R(2) if r == 1 else k2 + 1
    key = sp.diff(fx, xs_).subs(xs_, at)
    coef = d1 if r == 1 else d2
    noearlier = b + (d2 if r == 2 else 0)
    return key, {'coefficient-only': coef, 'skipped-knot': noearlier}


def coef_count(V):
    k, add = int(V['k']), int(V['add'])
    deg = 3 if add == 4 else 1
    x = np.linspace(0, 1, 400)
    knots = np.linspace(0, 1, k + 2)[1:-1]
    cols = [x ** p for p in range(deg + 1)] + [np.maximum(0, x - kk) ** deg for kk in knots]
    rank = np.linalg.matrix_rank(np.column_stack(cols))
    return sp.Integer(int(rank)), {'no-constant': rank - 1, 'knots-only': k}


ck = Checker('stat-learning')
ck.add('fluency-l15-widest-street', 'margin', margin)
ck.add('fluency-l15-widest-street', 'decision-value', decision)
ck.add('fluency-l15-widest-street', 'distance', distance)
ck.add('fluency-l16-groups-nobody-labelled', 'assign-and-update', kmeans_step)
ck.add('fluency-l16-groups-nobody-labelled', 'group-inertia', group_ss)
ck.add('fluency-l16-groups-nobody-labelled', 'linkage-distance', linkage_dist)
ck.add('fluency-l17-a-small-network', 'forward-pass', forward)
ck.add('fluency-l17-a-small-network', 'parameter-count', params)
ck.add('fluency-l17-a-small-network', 'slope-first-weight', slope)
ck.add('fluency-l17-a-small-network', 'one-step', step)
ck.add('fluency-l18-bending-the-line', 'hinge-value', hinge_value)
ck.add('fluency-l18-bending-the-line', 'slope-in-a-region', slope_region)
ck.add('fluency-l18-bending-the-line', 'coefficient-count', coef_count)
ck.run()
