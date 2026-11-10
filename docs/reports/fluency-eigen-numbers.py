"""Recompute every Fluency family of the eigen course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-eigen-numbers.py [--n 200]

The matrix is rebuilt from the vars by the family's construction, then sympy gives charpoly, eigenvals and the
nullspace of A - lambda I. Exit 0 when all agree.
"""
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_la_common import run, Set, LAM  # noqa: E402

R = lambda v: F(int(sp.fraction(sp.nsimplify(v))[0]), int(sp.fraction(sp.nsimplify(v))[1]))


def poly_of(A):
    return sp.expand((A - LAM * sp.eye(2)).det())


def l2_poly(V):
    a, b, c, d = V['a'], V['b'], V['c'], V['d']
    A = sp.Matrix([[a, b], [c, d]])
    key = poly_of(A)
    assert sp.expand(key - A.charpoly(LAM).as_expr()) == 0
    return key, {'sign-of-sum': sp.expand(LAM ** 2 + (a + d) * LAM + A.det()),
                 'added-bc': sp.expand(LAM ** 2 - (a + d) * LAM + a * d + b * c)}


def built(V):
    # the family's construction: diagonal l1 + t and l2 - t, off-diagonal t and gp - t (one of them signed)
    l1, gp, t, sg, sw = V['l1'], V['gp'], V['t'], V['sg'], V['sw']
    b, c = (t, gp - t) if sw == 0 else (gp - t, t)
    return sp.Matrix([[l1 + t, sg * b], [sg * c, l1 + gp - t]])


def l2_eigs(V):
    A = built(V)
    ev = A.eigenvals()
    assert all(m == 1 for m in ev.values()) and len(ev) == 2
    lam = [R(e) for e in ev]
    return Set(lam), {'diagonal-entries': Set([A[0, 0], A[1, 1]]), 'signs-flipped': Set([-v for v in lam])}


def l2_vec(V):
    l, a, b, n = V['l'], V['a'], V['b'], V['n']
    g = sp.gcd(abs(l - a), abs(b))
    A = sp.Matrix([[a, b], [(l - a) * n / g, l - b * n / g]])
    ns = (A - l * sp.eye(2)).nullspace()
    assert len(ns) == 1 and ns[0][0] != 0
    v = ns[0] / ns[0][0]
    assert A * v == l * v
    key = R(v[1])
    w = {'sign-slip': -key}
    if abs(a - l) != abs(b):
        w['upside-down'] = 1 / key
    return key, w


S = 'fluency-l2-characteristic'
run('eigen', [(S, 'characteristic-polynomial', 'poly', l2_poly), (S, 'both-eigenvalues', 'set', l2_eigs), (S, 'eigenvector', 'num', l2_vec)])
