"""Recompute every Fluency family of the least-squares course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-least-squares-numbers.py [--n 200]

The slope comes from solving A^T A x = A^T y with sympy (A = [1, x]), not from the centred-sum formula the family
prints; the normal equations are solved with linsolve. Exit 0 when all agree.
"""
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_la_common import run  # noqa: E402

R = lambda v: F(int(sp.fraction(sp.nsimplify(v))[0]), int(sp.fraction(sp.nsimplify(v))[1]))
XS = {(1, 2, 3, 4), (0, 1, 2, 3), (2, 3, 4, 5), (1, 3, 5, 7), (0, 2, 4, 6)}


def l11_slope(V):
    xs = [V['x%d' % i] for i in range(1, 5)]
    ys = [V['y%d' % i] for i in range(1, 5)]
    assert tuple(int(v) for v in xs) in XS
    A = sp.Matrix([[1, xv] for xv in xs])
    yv = sp.Matrix(ys)
    alpha, beta = (A.T * A).LUsolve(A.T * yv)
    # the centred sums, worked separately, for the upside-down slip
    xb, yb = sum(xs) / 4, sum(ys) / 4
    sxy = sum((xi - xb) * (yi - yb) for xi, yi in zip(xs, ys))
    sxx = sum((xi - xb) ** 2 for xi in xs)
    assert R(beta) == sxy / sxx
    raw = sum(xi * yi for xi, yi in zip(xs, ys)) / sum(xi ** 2 for xi in xs)
    return R(beta), {'upside-down': sxx / sxy, 'not-centred': F(raw)}


def l11_normal(V):
    n, sx, sxx, al, be = V['n'], V['sx'], V['sxx'], V['al'], V['be']
    a, b = sp.symbols('a b')
    r1, r2 = n * al + sx * be, sx * al + sxx * be
    (sol,) = sp.linsolve([sp.Eq(n * a + sx * b, r1), sp.Eq(sx * a + sxx * b, r2)], [a, b])
    key = tuple(R(v) for v in sol)
    return key, {'swapped-order': (key[1], key[0])}


def l11_intercept(V):
    b, xb, yb = V['b'], V['xb'], V['yb']
    a = sp.symbols('a')
    key = sp.solve(sp.Eq(yb, a + sp.nsimplify(b) * xb), a)[0]   # the line passes through the means
    return R(key), {'sign-slip': yb + b * xb, 'forgot-x-bar': yb - b}


S = 'fluency-l11-fitting-a-line'
run('least-squares', [(S, 'slope-from-points', 'num', l11_slope), (S, 'solve-normal-equations', 'vec', l11_normal),
                      (S, 'intercept-from-means', 'num', l11_intercept)])
