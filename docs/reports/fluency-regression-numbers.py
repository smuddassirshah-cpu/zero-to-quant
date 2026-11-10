"""Recompute the Fluency set of regression from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-regression-numbers.py [--n 200]
The slope from sums minimises S(b) = Syy - 2 b Sxy + b^2 Sxx (the centred sum of squares) with sympy, so the formula
Sxy / Sxx is not reused; the sums are also checked to be possible (Sxy^2 < Sxx Syy). The intercept solves
y-bar = a + b x-bar for a. The slope from r is Cov / Var with Cov = r sx sy. Checks are in fluency_check.py.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402

b_ = sp.Symbol('b')
a_ = sp.Symbol('a')


def least_squares(sxy, sxx, syy):
    S = syy - 2 * b_ * sxy + b_ ** 2 * sxx
    sol = sp.solve(sp.diff(S, b_), b_)
    assert len(sol) == 1 and sp.diff(S, b_, 2) > 0
    return sol[0]


def from_sums(V):
    sxy, sxx, syy = V['sxy'], V['sxx'], V['syy']
    assert sxy ** 2 < sxx * syy
    key = least_squares(sxy, sxx, syy)
    other = least_squares(sxy, syy, sxx)       # x on y: the roles of the two squared sums swap
    w = {}
    inv = sxx / sxy
    if abs(float(inv - key)) > 0.002:
        w['upside-down'] = inv
    if abs(float(other - key)) > 0.002 and abs(float(other - inv)) > 0.002:
        w['x-on-y'] = other
    return key, w


def intercept(V):
    b, xb, yb = V['bh'] / 10, V['xh'] / 10, V['yh'] / 10
    key = sp.solve(sp.Eq(yb, a_ + b * xb), a_)[0]
    w = {'added': yb + b * xb}
    swap = xb - b * yb
    if swap != key and swap != w['added']:
        w['means-swapped'] = swap
    return key, w


def from_r(V):
    r, sx, sy = V['r'], V['sx'], V['sy']
    cov = r * sx * sy
    key = cov / sx ** 2
    return key, {'sds-upside-down': r * sx / sy, 'forgot-r': sy / sx}


ck = Checker('regression')
ck.add('fluency-l2-slope-formula', 'slope-from-sums', from_sums)
ck.add('fluency-l2-slope-formula', 'intercept', intercept)
ck.add('fluency-l2-slope-formula', 'slope-from-r', from_r)
ck.run()
