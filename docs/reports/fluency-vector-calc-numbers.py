"""Recompute every Fluency family of the vector-calc course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-vector-calc-numbers.py [--n 200]
Each field is built from the vars, and divergence and curl come from sympy `diff` (the space curl from
sympy.vector's `curl`, as an independent route). Each slip is rebuilt from the vars. Exit 0 when all agree
(see fluency_1_11_lib.py).
"""
import os
import sys

import sympy as sp
from sympy.vector import CoordSys3D, curl as vcurl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_1_11_lib import Checker, x, y, z  # noqa: E402

C = Checker('vector-calc')
N3 = CoordSys3D('N')


def div2(P, Q):
    return sp.expand(sp.diff(P, x) + sp.diff(Q, y))


def curl2(P, Q):
    return sp.expand(sp.diff(Q, x) - sp.diff(P, y))


def field_a(V):
    return V['a'] * x ** 2 * y + V['b'] * y ** 2, V['c'] * x + V['d'] * y ** 2


def f_divergence(V):
    P, Q = field_a(V)
    return div2(P, Q), {'curl-instead': curl2(P, Q), 'stopped-at-px': sp.diff(P, x)}


def f_curl(V):
    P, Q = V['a'] * x ** 2 * y + V['b'] * x, V['c'] * x ** 2 + V['d'] * y ** 2
    return curl2(P, Q), {'reversed': -curl2(P, Q), 'divergence-instead': div2(P, Q)}


def f_point(V):
    P, Q = field_a(V)
    pt = {x: V['x0'], y: V['y0']}
    dv, cu = div2(P, Q).subs(pt), curl2(P, Q).subs(pt)
    key, other = (dv, cu) if V['w'] == 'div' else (cu, dv)
    slips = {}
    if other != key:
        slips['other-quantity'] = other
    if V['w'] == 'curl' and cu != 0 and other != -cu:
        slips['curl-reversed'] = -cu
    return key, slips


def f_space(V):
    a, b, c, d = V['a'], V['b'], V['c'], V['d']
    X, Y, Z = N3.x, N3.y, N3.z
    F = (a * X * Y + d * Z ** 2) * N3.i + (b * Y * Z) * N3.j + (c * Z * X) * N3.k
    G = vcurl(F)
    pt = {X: V['x0'], Y: V['y0'], Z: V['z0']}
    comp = tuple(sp.expand(G.dot(e)).subs(pt) for e in (N3.i, N3.j, N3.k))
    return comp, {'each-reversed': tuple(-q for q in comp), 'order-reversed': tuple(reversed(comp))}


FAMILIES = [
    ('fluency-l5-divergence-and-curl', 'divergence', f_divergence),
    ('fluency-l5-divergence-and-curl', 'curl', f_curl),
    ('fluency-l5-divergence-and-curl', 'at-a-point', f_point),
    ('fluency-l5-divergence-and-curl', 'curl-in-space', f_space),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        C.check(set_id, fam, fn)
    C.finish()
