"""Recompute the Fluency sets of limits-thm from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-limits-thm-numbers.py [--n 200]
Binomial chances are found by enumerating all 2^n win-loss paths with itertools.product and adding the chances of
the paths with k wins; the variance is the definition over the enumerated pmf. For the bell curve, every table value
the prompt gives is first checked against Phi from math.erf (to 0.00005), then the key is derived from the event
itself: x is standardised, and the chance is Phi(z) or 1 - Phi(z) from the table value with symmetry.
Checks are in fluency_check.py beside this script.
"""
import itertools
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker, phi  # noqa: E402


def pmf(n, p):
    out = {}
    for path in itertools.product([1, 0], repeat=int(n)):
        ch = sp.Integer(1)
        for w in path:
            ch *= p if w else 1 - p
        out[sum(path)] = out.get(sum(path), 0) + ch
    return out


def exactly_k(V):
    n, k, p = int(V['n']), int(V['k']), V['p']
    dist = pmf(n, p)
    key = dist[k]
    one = p ** k * (1 - p) ** (n - k)
    swap = pmf(n, 1 - p)[k]
    w = {}
    if abs(float(key - one)) > 0.0002:
        w['one-path'] = one
    if abs(float(key - swap)) > 0.0002:
        w['swapped'] = swap
    return key, w


def binomial_variance(V):
    n, p = int(V['n']), V['p']
    # Var of a sum of n independent indicators: enumerate one indicator, then add n copies.
    one = pmf(1, p)
    mu1 = sum(x * c for x, c in one.items())
    var1 = sum((x - mu1) ** 2 * c for x, c in one.items())
    return n * var1, {'gave-mean': n * mu1, 'one-trial': var1}


def none_succeed(V):
    n, p = int(V['n']), V['p']
    dist = pmf(n, p)
    return dist[0], {'used-p': dist[n], 'complement-of-all': 1 - dist[n]}


def table(V):
    za, ph = V['za'], V['ph']
    assert abs(phi(za) - float(ph)) <= 0.00005, (za, ph)
    return za, ph


def standardise(V):
    z, sig, mu = V['z'], V['sig'], V['mu']
    x = mu + z * sig
    key = (x - mu) / sig
    return key, {'divided-by-variance': (x - mu) / sig ** 2, 'sign-flipped': (mu - x) / sig}


def normal_probability(V):
    za, ph = table(V)
    sig, mu = V['sig'], V['mu']
    x = mu + V['sgn'] * za * sig
    z = (x - mu) / sp.sqrt(sig ** 2)
    below = ph if z > 0 else 1 - ph          # P(Z < z) from the table and symmetry
    key = below if V['op'] == '<' else 1 - below
    assert abs(float(key) - (phi(z) if V['op'] == '<' else 1 - phi(z))) <= 0.00006
    return key, {'other-tail': 1 - key, 'gave-z': z}


def within_band(V):
    za, ph = table(V)
    key = ph - (1 - ph)
    assert abs(float(key) - (phi(za) - phi(-za))) <= 0.0001
    return key, {'one-cut': ph, 'half-band': ph - sp.Rational(1, 2)}


ck = Checker('limits-thm')
ck.add('fluency-l1-counting-successes', 'exactly-k', exactly_k)
ck.add('fluency-l1-counting-successes', 'binomial-variance', binomial_variance)
ck.add('fluency-l1-counting-successes', 'none-succeed', none_succeed)
ck.add('fluency-l7-bell-curve', 'standardise', standardise)
ck.add('fluency-l7-bell-curve', 'normal-probability', normal_probability)
ck.add('fluency-l7-bell-curve', 'within-band', within_band)
ck.run()
