"""Recompute the Fluency set of random-vars from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-random-vars-numbers.py [--n 200]
The variance is worked from its definition, E[(X - mu)^2], over the pmf built from the vars (the set's solutions use
the shortcut E[X^2] - mu^2, so the two routes differ), and the standard deviation is its exact sympy root.
Checks are in fluency_check.py beside this script.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def moments(pmf):
    assert sum(pmf.values()) == 1
    mu = sum(x * p for x, p in pmf.items())
    var = sum((x - mu) ** 2 * p for x, p in pmf.items())
    ex2 = sum(x ** 2 * p for x, p in pmf.items())
    return mu, var, ex2


def slips(mu, ex2):
    w = {}
    if mu != 0:
        w['no-mean'] = ex2
    if mu != 0 and mu != 1:
        w['mean-not-squared'] = ex2 - mu
    return w


def two_outcome(V):
    p, a, b = V['p'], V['a'], V['b']
    mu, var, ex2 = moments({a: p, -b: 1 - p})
    return var, slips(mu, ex2)


def three_value(V):
    pmf = {V['x1']: V['p1'], V['x2']: V['p2'], V['x3']: V['p3']}
    mu, var, ex2 = moments(pmf)
    return var, slips(mu, ex2)


def sd(V):
    p, q, a, b = V['p'], V['q'], V['a'], V['b']
    mu, var, ex2 = moments({a: p, -b: q})
    key = sp.sqrt(var)
    assert key.is_rational
    w = {}
    if var != key:
        w['gave-variance'] = var
    root = sp.sqrt(ex2)
    if mu != 0 and abs(float(root - key)) > 0.01:
        w['no-mean'] = root
    return key, w


ck = Checker('random-vars')
ck.add('fluency-l9-measuring-spread', 'two-outcome-variance', two_outcome)
ck.add('fluency-l9-measuring-spread', 'three-value-variance', three_value)
ck.add('fluency-l9-measuring-spread', 'standard-deviation', sd)
ck.run()
