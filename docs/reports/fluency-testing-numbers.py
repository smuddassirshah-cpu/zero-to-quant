"""Recompute the Fluency sets of testing from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-testing-numbers.py [--n 200]
Each statistic is (estimate - null) / standard error, with the standard error from sympy's sqrt of n (the tuple root
is asserted equal). The Sharpe family rebuilds a mean and sd with that Sharpe ratio (mean = SR, sd = 1) and forms
t = mean / (sd / sqrt(T)) from them. Checks are in fluency_check.py beside this script.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def z_zero(V):
    xb, sig, n = V['xh'] / 100, V['sig'], V['n']
    rt = sp.sqrt(n)
    assert rt == V['rt']
    key = (xb - 0) / (sig / rt)
    return key, {'divided-by-sigma': xb / sig, 'divided-by-n': xb / (sig / n)}


def z_nonzero(V):
    m0, sig, n = V['m0'], V['sig'], V['n']
    xb = m0 + V['dh'] / 10
    rt = sp.sqrt(n)
    assert rt == V['rt']
    key = (xb - m0) / (sig / rt)
    return key, {'centred-on-zero': xb / (sig / rt), 'divided-by-sigma': (xb - m0) / sig}


def t_stat(V):
    n, xb, s = V['n'], V['xh'] / 10, V['sh'] / 10
    key = xb / (s / sp.sqrt(n))
    return key, {'no-root-n': xb / s, 'root-of-df': xb / (s / sp.sqrt(n - 1))}


def sharpe(V):
    sr, T = V['sr'], V['y']
    assert V['lo'] <= T <= V['hi']
    mean, sd = sr, sp.Integer(1)
    key = mean / (sd / sp.sqrt(T))
    return key, {'times-t': sr * T, 'over-root': sr / sp.sqrt(T)}


ck = Checker('testing')
ck.add('fluency-l2-measuring-surprise', 'z-null-zero', z_zero)
ck.add('fluency-l2-measuring-surprise', 'z-null-nonzero', z_nonzero)
ck.add('fluency-l4-t-test', 't-statistic', t_stat)
ck.add('fluency-l4-t-test', 'sharpe-t', sharpe)
ck.run()
