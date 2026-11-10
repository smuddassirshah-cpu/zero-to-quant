"""Recompute the Fluency set of conditional from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-conditional-numbers.py [--n 200]
The count family builds the population person by person and counts inside the positives. The rate families turn the
percentages into natural frequencies over 1,000,000 cases (every count is whole, since each rate is a whole per cent)
and count again, so Bayes' rule itself is never evaluated. Checks are in fluency_check.py beside this script.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402

R = sp.Rational


def from_counts(V):
    tot, a, c, b = int(V['tot']), int(V['a']), int(V['c']), int(V['b'])
    people = [('bad', '+')] * a + [('bad', '-')] * c + [('good', '+')] * b
    people += [('good', '-')] * (tot - len(people))
    assert len(people) == tot and tot - a - b - c > 0
    pos = [p for p in people if p[1] == '+']
    bad = [p for p in people if p[0] == 'bad']
    both = [p for p in people if p == ('bad', '+')]
    return R(len(both), len(pos)), {'inverse': R(len(both), len(bad)), 'joint': R(len(both), tot)}


def frequencies(V):
    M = 1000000
    pp, s, f = int(V['pp']), int(V['s']), int(V['f'])
    bad = M * pp // 100
    good = M - bad
    bad_pos = bad * s // 100
    good_pos = good * f // 100
    assert bad * s % 100 == 0 and good * f % 100 == 0
    return M, bad, good, bad_pos, good_pos


def from_rates(V):
    M, bad, good, bad_pos, good_pos = frequencies(V)
    key = R(bad_pos, bad_pos + good_pos)
    unweighted = R(bad_pos, M) / (R(bad_pos, M) + R(int(V['f']), 100))
    return key, {'inverse': R(bad_pos, bad), 'no-division': R(bad_pos, M), 'unweighted-others': unweighted}


def every_path(V):
    M, bad, good, bad_pos, good_pos = frequencies(V)
    key = R(bad_pos + good_pos, M)
    return key, {'one-path': R(bad_pos, M), 'unweighted-others': R(bad_pos, M) + R(int(V['f']), 100)}


ck = Checker('conditional')
ck.add('fluency-l7-turning-around', 'from-counts', from_counts)
ck.add('fluency-l7-turning-around', 'from-rates', from_rates)
ck.add('fluency-l7-turning-around', 'every-positive-path', every_path)
ck.run()
