"""Recompute the Fluency set of counting-chance from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-counting-chance-numbers.py [--n 200]
Each chance is counted by brute force: the bag is a list of labelled items and every ordered draw is enumerated
(itertools.permutations without replacement, itertools.product with), so no probability formula is reused.
Checks are in fluency_check.py beside this script.
"""
import itertools
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def bag(V):
    return ['A'] * int(V['r']) + ['B'] * int(V['b'])


def share(draws, ok):
    draws = list(draws)
    return sp.Rational(sum(1 for d in draws if ok(d)), len(draws))


def two_without(V):
    items = bag(V)
    n = len(items)
    key = share(itertools.permutations(items, 2), lambda d: d == ('A', 'A'))
    wrep = share(itertools.product(items, repeat=2), lambda d: d == ('A', 'A'))
    keep = sp.Rational(int(V['r']) * (int(V['r']) - 1), n * n)
    return key, {'with-replacement': wrep, 'kept-bottom': keep}


def two_with(V):
    items = bag(V)
    n = len(items)
    key = share(itertools.product(items, repeat=2), lambda d: d == ('A', 'B'))
    nrep = share(itertools.permutations(items, 2), lambda d: d == ('A', 'B'))
    both = share(itertools.product(items, repeat=2), lambda d: sorted(d) == ['A', 'B'])
    assert both == 2 * key
    return key, {'without-replacement': nrep, 'either-order': both}


def three_without(V):
    items = bag(V)
    n = len(items)
    r = int(V['r'])
    key = share(itertools.permutations(items, 3), lambda d: d == ('A', 'A', 'A'))
    wrep = share(itertools.product(items, repeat=3), lambda d: d == ('A', 'A', 'A'))
    w = {'with-replacement': wrep}
    if r > 2:
        w['kept-bottom'] = sp.Rational(r * (r - 1) * (r - 2), n ** 3)
    return key, w


ck = Checker('counting-chance')
ck.add('fluency-l7-replacement', 'two-without', two_without)
ck.add('fluency-l7-replacement', 'two-with', two_with)
ck.add('fluency-l7-replacement', 'three-without', three_without)
ck.run()
