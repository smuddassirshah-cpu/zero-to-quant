"""Recompute the Fluency set of markov from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-markov-numbers.py [--n 200]
The transition matrix is rebuilt as a sympy Matrix of exact Rationals (each row checked to add to 1); two-step chances
are entries of P**2 and the moved distribution is the row vector times P. Checks are in fluency_check.py.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def stochastic(rows):
    P = sp.Matrix(rows)
    for i in range(P.rows):
        assert sum(P.row(i)) == 1 and all(x >= 0 for x in P.row(i))
    return P


def slips(P, i, j, key):
    w = {}
    sq = P[i, j] ** 2
    if sq != key:
        w['squared-entry'] = sq
    if P[i, j] != key:
        w['one-step'] = P[i, j]
    return w


def two_state(V):
    a, b = V['a'], V['b']
    P = stochastic([[a, 1 - a], [b, 1 - b]])
    i, j = int(V['i']), int(V['j'])
    assert V['fi'] == ['bull', 'bear'][i] and V['tj'] == ['bull', 'bear'][j]
    key = (P ** 2)[i, j]
    return key, slips(P, i, j, key)


def three_state(V):
    P = stochastic([[V['a1'], V['a2'], V['a3']], [V['b1'], V['b2'], V['b3']], [V['c1'], V['c2'], V['c3']]])
    j = int(V['j']) - 1
    assert V['tj'] == ['Sunny', 'Cloudy', 'Rain'][j]
    key = (P ** 2)[0, j]
    return key, slips(P, 0, j, key)


def forward(V):
    a, b, u = V['a'], V['b'], V['u']
    P = stochastic([[a, 1 - a], [b, 1 - b]])
    pi0 = sp.Matrix([[u, 1 - u]])
    j = int(V['j'])
    assert V['tj'] == ['bull', 'bear'][j]
    key = (pi0 * P)[0, j]
    w = {}
    if P[0, j] != key:
        w['bull-row-only'] = P[0, j]
    col = P[0, j] + P[1, j]
    if col != key:
        w['unweighted-column'] = col
    return key, w


ck = Checker('markov')
ck.add('fluency-l2-transition-matrix', 'two-state-two-step', two_state)
ck.add('fluency-l2-transition-matrix', 'three-state-two-step', three_state)
ck.add('fluency-l2-transition-matrix', 'distribution-forward', forward)
ck.run()
