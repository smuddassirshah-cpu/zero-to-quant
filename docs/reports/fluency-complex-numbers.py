"""Recompute every Fluency family of the complex course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-complex-numbers.py [--n 200]
Keys come from sympy complex arithmetic, `solve`, `arg`, `Abs` and `cos`/`sin` of the drawn angle; each slip is
rebuilt from the vars as the learner would make it. Exit 0 when all agree (see fluency_1_11_lib.py).
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_1_11_lib import Checker, parse  # noqa: E402

I = sp.I
S3 = sp.sqrt(3)
C = Checker('complex')


# ---- fluency-l1-square-root-of-minus-one ----
def l1_multiply(V):
    a, b, c, d = V['a'], V['b'], V['c'], V['d']
    key = sp.expand((a + b * I) * (c + d * I))
    return key, {'i-squared-plus-one': (a * c + b * d) + (a * d + b * c) * I,  # i^2 read as +1
                 'parts-only': a * c + b * d * I}                              # cross terms dropped


def l1_divide(V):
    c, d, e, f = V['c'], V['d'], V['e'], V['f']
    num = sp.expand((c + d * I) * (e + f * I))
    key = sp.simplify(num / (c + d * I))
    nr, ni = sp.re(num), sp.im(num)
    slips = {'part-by-part': nr / c + ni / d * I}
    if abs(c) != abs(d):
        slips['bottom-i-squared'] = sp.expand(num * (c - d * I)) / (c ** 2 - d ** 2)
    return key, slips


def l1_roots(V):
    p, q = V['p'], V['q']
    X = sp.Symbol('X')
    key = sp.solve(X ** 2 - 2 * p * X + (p ** 2 + q ** 2), X)
    slips = {'not-halved': [p + 2 * q * I, p - 2 * q * I], 'plus-b': [-p + q * I, -p - q * I]}
    return list(key), slips


def l1_power(V):
    n = int(V['n'])
    key = I ** n
    slips = {}
    if n % 4 == 2:
        slips['even-is-positive'] = sp.Integer(1)
    if n % 2 == 1:
        slips['odd-sign'] = -key
    return key, slips


# ---- fluency-l2-points-in-a-plane ----
def l2_modulus(V):
    a, b = V['a'], V['b']
    return sp.Abs(a + b * I), {'added-parts': abs(a) + abs(b), 'no-root': a ** 2 + b ** 2}


def l2_distance(V):
    z, w = V['a'] + V['b'] * I, V['c'] + V['d'] * I
    key = sp.Abs(z - w)
    md = abs(sp.Abs(z) - sp.Abs(w))
    slips = {'sum-not-difference': sp.Abs(z + w), 'no-root': sp.re(z - w) ** 2 + sp.im(z - w) ** 2}
    if abs(float(md - key)) > 0.001:
        slips['moduli-subtracted'] = md
    return key, slips


def l2_arg(V):
    k = V['k']
    re = V['sx'] * k * (S3 if V['ra'] else 1)
    im = V['sy'] * k * (S3 if V['ia'] else 1)
    key = sp.simplify(sp.arg(re + im * I))
    slips = {}
    if V['sx'] < 0:
        slips['arctan-only'] = sp.atan(im / re)
    if key < 0:
        slips['not-principal'] = key + 2 * sp.pi
    return key, slips


def l2_polar(V):
    r, th = V['r'], parse(V['th'])
    key = sp.expand(r * sp.cos(th) + I * r * sp.sin(th))
    return key, {'cos-sin-swapped': r * sp.sin(th) + I * r * sp.cos(th),
                 'forgot-r': sp.cos(th) + I * sp.sin(th)}


FAMILIES = [
    ('fluency-l1-square-root-of-minus-one', 'multiply', l1_multiply),
    ('fluency-l1-square-root-of-minus-one', 'divide', l1_divide),
    ('fluency-l1-square-root-of-minus-one', 'complex-roots', l1_roots),
    ('fluency-l1-square-root-of-minus-one', 'power-of-i', l1_power),
    ('fluency-l2-points-in-a-plane', 'modulus', l2_modulus),
    ('fluency-l2-points-in-a-plane', 'distance', l2_distance),
    ('fluency-l2-points-in-a-plane', 'principal-argument', l2_arg),
    ('fluency-l2-points-in-a-plane', 'from-polar', l2_polar),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        C.check(set_id, fam, fn)
    C.finish()
