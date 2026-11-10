"""Recompute the Fluency sets of estimation from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-estimation-numbers.py [--n 200]
Square roots are taken by sympy from n itself, and each root the set carries in a tuple (rt, rootpq) is asserted to
equal it. The confidence multipliers 1.645, 1.96 and 2.576 are checked against statistics.NormalDist().inv_cdf to
0.0005. The data-needed family solves SE(n2) = SE(n)/k for n2 with sympy. Checks are in fluency_check.py.
"""
import os
import sys
from statistics import NormalDist

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def root_n(V):
    rt = sp.sqrt(V['n'])
    assert rt == V['rt'], (V['n'], V['rt'])
    return rt


def z_for(V):
    lev, z = V['lev'], V['z']
    zz = NormalDist().inv_cdf(0.5 + float(lev) / 200)
    assert abs(zz - float(z)) <= 0.0005, (lev, z)
    return z


def se_mean(V):
    s, n = V['s'], V['n']
    return s / root_n(V), {'divided-by-n': s / n, 'gave-sd': s}


def se_prop(V):
    p, n = V['pc'] / 100, V['n']
    assert (V['pc'] * n) % 100 == 0
    assert sp.sqrt(p * (1 - p)) == V['rootpq']
    key = sp.sqrt(p * (1 - p) / n)
    return key, {'no-root': p * (1 - p) / n, 'root-over-n': sp.sqrt(p * (1 - p)) / n}


def data_needed(V):
    se1, k, n = V['se1'], V['k'], V['n']
    n2 = sp.Symbol('n2', positive=True)
    sigma = se1 * sp.sqrt(n)                      # SE = sigma / sqrt(n)
    sol = sp.solve(sp.Eq(sigma / sp.sqrt(n2), se1 / k), n2)
    assert len(sol) == 1
    key = sol[0]
    return key, {'linear': n * k, 'extra-only': key - n}


def interval(V):
    z = z_for(V)
    xb, se = V['xh'] / 100, V['sh'] / 100
    key = (xb - z * se, xb + z * se)
    w = {'no-multiplier': (xb - se, xb + se)}
    if V['lev'] != 95:
        w['used-1-96'] = (xb - sp.Rational('1.96') * se, xb + sp.Rational('1.96') * se)
    return key, w


def half_width(V):
    z = z_for(V)
    s, n = V['s'], V['n']
    return z * s / root_n(V), {'no-root-n': z * s, 'divided-by-n': z * s / n}


ck = Checker('estimation')
ck.add('fluency-l9-how-precise', 'se-of-mean', se_mean)
ck.add('fluency-l9-how-precise', 'se-of-proportion', se_prop)
ck.add('fluency-l9-how-precise', 'data-needed', data_needed)
ck.add('fluency-l10-catching-the-truth', 'interval-from-se', interval)
ck.add('fluency-l10-catching-the-truth', 'half-width-from-s', half_width)
ck.run()
