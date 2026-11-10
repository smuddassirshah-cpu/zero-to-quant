"""Recompute every Fluency family of the elimination course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-elimination-numbers.py [--n 200]

Systems are solved with sympy's linsolve, determinants with Matrix.det, and the slips worked through step by step.
Exit 0 when all agree.
"""
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_la_common import run  # noqa: E402

x, y, z = sp.symbols('x y z')
R = lambda v: F(int(sp.fraction(sp.nsimplify(v))[0]), int(sp.fraction(sp.nsimplify(v))[1]))


def solve3(A, rhs):
    sol = sp.linsolve((sp.Matrix(A), sp.Matrix(rhs)), [x, y, z])
    (t,) = list(sol)
    return tuple(R(v) for v in t)


# ---- fluency-l2-back-substitution ----
def l2_up(V):
    a, b, c, e, f, g = (V[k] for k in 'abcefg')
    x0, y0, z0 = V['x0'], V['y0'], V['z0']
    A = [[a, b, c], [0, e, f], [0, 0, g]]
    rhs = list(sp.Matrix(A) * sp.Matrix([x0, y0, z0]))
    key = solve3(A, rhs)
    # the slip: in row 2, f*z kept its sign when moved across
    zs = F(rhs[2], g)
    ys = (F(rhs[1]) + f * zs) / e
    xs = (F(rhs[0]) - b * ys - c * zs) / a
    w = {'sign-not-changed': (xs, ys, zs)}
    if a != 1:
        w['pivot-not-divided'] = (a * key[0], key[1], key[2])
    if key[0] != key[2]:
        w['found-order'] = (key[2], key[1], key[0])
    return key, w


def l2_down(V):
    a, b, c, e, f, g = (V[k] for k in 'abcefg')
    x0, y0, z0 = V['x0'], V['y0'], V['z0']
    A = [[a, 0, 0], [b, e, 0], [c, f, g]]
    rhs = list(sp.Matrix(A) * sp.Matrix([x0, y0, z0]))
    key = solve3(A, rhs)
    xs = F(rhs[0], a)
    ys = (F(rhs[1]) + b * xs) / e
    zs = (F(rhs[2]) - c * xs - f * ys) / g
    w = {'sign-not-changed': (xs, ys, zs)}
    if g != 1:
        w['pivot-not-divided'] = (key[0], key[1], g * key[2])
    return key, w


# ---- fluency-l10-computing-dets ----
def l10_cof(V):
    A = sp.Matrix([[V['a'], V['b'], V['c']], [V['d'], V['e'], V['f']], [V['g'], V['h'], V['k']]])
    terms = [A[0, j] * A.minor(0, j) for j in range(3)]
    assert A.det() == terms[0] - terms[1] + terms[2]
    return R(A.det()), {'no-checkerboard': R(sum(terms)), 'minus-on-last': R(terms[0] - terms[1] - terms[2])}


def l10_ops(V):
    # build a matrix with the given determinant, apply the three operations, and take the determinant again
    dd, k, m = V['dd'], V['k'], V['m']
    A = sp.Matrix([[1, 2, 0], [0, 1, 3], [1, 0, dd + 6]])   # then shift the corner so that det A = dd exactly
    A[2, 2] = A[2, 2] - (A.det() - dd)
    assert A.det() == dd
    sw = {'$R_1$ and $R_2$': (0, 1), '$R_1$ and $R_3$': (0, 2), '$R_2$ and $R_3$': (1, 2)}[V['sw']]
    sc = {'$R_1$': 0, '$R_2$': 1, '$R_3$': 2}[V['sc']]
    B = A.copy()
    B.row_swap(*sw)
    B[sc, :] = k * B[sc, :]
    B[2, :] = B[2, :] + m * B[0, :]
    return R(B.det()), {'swap-ignored': k * dd, 'scale-ignored': -dd, 'add-counted': -k * m * dd}


def l10_piv(V):
    p = V['p1'] * V['p2'] * V['p3']
    s = int(V['s'])
    U = sp.diag(V['p1'], V['p2'], V['p3'])
    key = (-1) ** s * U.det()
    w = {'added-pivots': V['p1'] + V['p2'] + V['p3']}
    if s % 2 == 1:
        w['swaps-ignored'] = p
    if s == 2:
        w['flipped-once'] = -p
    return R(key), w


S2, S10 = 'fluency-l2-back-substitution', 'fluency-l10-computing-dets'
run('elimination', [
    (S2, 'bottom-up', 'vec', l2_up), (S2, 'top-down', 'vec', l2_down),
    (S10, 'cofactors-row-one', 'num', l10_cof), (S10, 'row-operations', 'num', l10_ops), (S10, 'pivots-and-swaps', 'num', l10_piv),
])
