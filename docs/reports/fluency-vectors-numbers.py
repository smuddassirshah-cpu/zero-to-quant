"""Recompute every Fluency family of the vectors course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-vectors-numbers.py [--n 200]

Keys come from sympy (Matrix products, inverses, square roots), never from the engine's lets. Exit 0 when all agree.
"""
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_la_common import run  # noqa: E402

R = lambda x: F(int(sp.fraction(sp.nsimplify(x))[0]), int(sp.fraction(sp.nsimplify(x))[1]))
M = lambda *rows: sp.Matrix(rows)


def vec(m):
    return tuple(R(x) for x in m)


# ---- fluency-l3-lengths-angles ----
def coords(V):
    x = (V['p'] if V['sw'] == 0 else V['q']) * V['sx']
    y = (V['q'] if V['sw'] == 0 else V['p']) * V['sy']
    return x, y


def l3_length(V):
    x, y = coords(V)
    L = sp.sqrt(x ** 2 + y ** 2)
    assert L.is_integer and L == V['len']
    return R(L), {'no-square-root': R(x ** 2 + y ** 2), 'added-sizes': abs(x) + abs(y)}


def l3_unit(V):
    x, y = coords(V)
    v = M(x, y)
    u = v / v.norm()
    assert sp.simplify(u.norm() - 1) == 0
    w = {'divided-by-dot': vec(v / v.dot(v))}
    if x < 0 or y < 0:
        w['sign-dropped'] = vec(u.applyfunc(abs))
    return vec(u), w


def l3_cos(V):
    u = M(V['p1'] * V['s1'], V['p2'] * V['s2'])
    v = M(V['q1'] * V['s3'], V['q2'])
    c = u.dot(v) / (u.norm() * v.norm())
    w = {'no-lengths': R(u.dot(v))}
    if u.norm() != v.norm():
        w['projection-instead'] = R(u.dot(v) / u.dot(u))
    return R(c), w


def l3_proj(V):
    u, v = M(V['u1'], V['u2']), M(V['v1'], V['v2'])
    k = sp.symbols('k')
    kk = sp.solve(sp.Eq((u - k * v).dot(v), 0), k)[0]   # the error u - kv is perpendicular to v
    return R(kk), {'upside-down': R(v.dot(v) / u.dot(v)), 'divided-by-uu': R(u.dot(v) / u.dot(u))}


# ---- fluency-l5-acting-on-a-vector ----
def l5_two(V):
    A = M([V['a'], V['b']], [V['c'], V['d']])
    x = M(V['x1'], V['x2'])
    key = V['x1'] * A[:, 0] + V['x2'] * A[:, 1]
    assert key == A * x
    return vec(key), {'combined-rows': vec(A.T * x), 'diagonal-only': (V['a'] * V['x1'], V['d'] * V['x2'])}


def l5_tall(V):
    A = M([V['a'], V['b']], [V['c'], V['d']], [V['e'], V['f']])
    x = M(V['x1'], V['x2'])
    return vec(A * x), {'amounts-swapped': vec(A * M(V['x2'], V['x1'])), 'added-columns': vec(A[:, 0] + A[:, 1])}


# ---- fluency-l7-one-after-another ----
def AB(V):
    return M([V['a'], V['b']], [V['c'], V['d']]), M([V['e'], V['f']], [V['g'], V['h']])


def l7_entry(V):
    A, B = AB(V)
    i, j = int(V['i']) - 1, int(V['j']) - 1
    w = {'order-swapped': R((B * A)[i, j])}
    if i != j:
        w['row-column-swapped'] = R((A * B)[j, i])
    return R((A * B)[i, j]), w


def l7_column(V):
    A, B = AB(V)
    j = int(V['j']) - 1
    return vec((A * B)[:, j]), {'order-swapped': vec((B * A)[:, j]), 'combined-rows': vec(A.T * B[:, j])}


# ---- fluency-l10-undoing ----
def l10_det(V):
    A = M([V['a'], V['b']], [V['c'], V['d']])
    return R(A.det()), {'added-bc': V['a'] * V['d'] + V['b'] * V['c'], 'ad-only': V['a'] * V['d']}


def l10_invcol(V):
    a, b, c, d = V['a'], V['b'], V['c'], V['d']
    A = M([a, b], [c, d])
    j = int(V['j']) - 1
    Ai = A.inv()
    assert A * Ai == sp.eye(2)
    adj = M([d, -b], [-c, a])
    w = {'not-swapped': vec(M([a, -b], [-c, d])[:, j] / A.det()),
         'added-bc': vec(adj[:, j] / (a * d + b * c))}
    if A.det() != 1:
        w['not-divided'] = vec(adj[:, j])
    return vec(Ai[:, j]), w


def l10_solve(V):
    a, b, c = V['a'], V['b'], V['c']
    d = (V['det'] + b * c) / a
    A = M([a, b], [c, d])
    rhs = A * M(V['x0'], V['y0'])
    x, y = sp.symbols('x y')
    sol = sp.solve([sp.Eq(a * x + b * y, rhs[0]), sp.Eq(c * x + d * y, rhs[1])], [x, y])
    return (R(sol[x]), R(sol[y])), {'multiplied-by-a': vec(A * rhs), 'swapped-order': (V['y0'], V['x0'])}


S3, S5, S7, S10 = 'fluency-l3-lengths-angles', 'fluency-l5-acting-on-a-vector', 'fluency-l7-one-after-another', 'fluency-l10-undoing'
run('vectors', [
    (S3, 'length', 'num', l3_length), (S3, 'unit-vector', 'vec', l3_unit),
    (S3, 'cosine-of-angle', 'num', l3_cos), (S3, 'projection-multiple', 'num', l3_proj),
    (S5, 'two-by-two', 'vec', l5_two), (S5, 'taller-columns', 'vec', l5_tall),
    (S7, 'one-entry', 'num', l7_entry), (S7, 'one-column', 'vec', l7_column),
    (S10, 'determinant', 'num', l10_det), (S10, 'inverse-column', 'vec', l10_invcol), (S10, 'solve-with-inverse', 'vec', l10_solve),
])
