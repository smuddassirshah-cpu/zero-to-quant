"""Recompute every Fluency family of the odes course from the drawn variables alone (docs/briefs/fluency.md check 1).

    <scratchpad>/venv/bin/python docs/reports/fluency-odes-numbers.py [--n 200]
Every closed-form key is found again with sympy `dsolve` on the equation and starting values built from the vars
(and the integrating factor by integrating p(t), then checking (mu y)' = mu (y' + p y)); the money keys are
recomputed from exp and rounded to the penny with Decimal. For the characteristic-root families the equation is
read back from the printed prompt as well and solved, so the prompt is checked to show that equation.
Exit 0 when all agree (see fluency_1_11_lib.py).
"""
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_1_11_lib import Checker, t  # noqa: E402

I = sp.I
f = sp.Function('f')
C = Checker('odes')


def dsolve1(rhs, y0):
    """Solve f' = rhs(f, t) with f(0) = y0."""
    sol = sp.dsolve(sp.Eq(f(t).diff(t), rhs(f(t))), f(t), ics={f(0): y0})
    return sp.simplify(sol.rhs)


def dsolve2(b, c, y0, v0):
    sol = sp.dsolve(sp.Eq(f(t).diff(t, 2) + b * f(t).diff(t) + c * f(t), 0), f(t),
                    ics={f(0): y0, f(t).diff(t).subs(t, 0): v0})
    return sp.expand(sol.rhs)


def penny(v):
    return Decimal(str(sp.N(v, 30))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


# ---- fluency-l2-separable ----
def l2_constant(V):
    k, y0 = V['k'], V['y0']
    key = dsolve1(lambda Y: k * Y, y0)
    return key, {'constant-added': sp.exp(k * t) + (y0 - 1), 'start-not-used': sp.exp(k * t)}


def l2_varies(V):
    a, b, y0 = V['a'], V['b'], V['y0']
    key = dsolve1(lambda Y: (a + b * t) * Y, y0)
    return key, {'rate-kept-constant': y0 * sp.exp(a * t), 'not-halved': y0 * sp.exp(b * t ** 2 + a * t)}


def l2_square(V):
    k, y0 = V['k'], V['y0']
    key = dsolve1(lambda Y: k * Y ** 2, y0)
    return key, {'solved-linear': y0 * sp.exp(k * t), 'sign-lost': y0 / (1 + k * y0 * t)}


def l2_discount(V):
    p, r, n = V['p'], V['r'], V['yr']
    D = sp.Function('D')
    T = sp.Symbol('T')
    sol = sp.dsolve(sp.Eq(D(T).diff(T), -sp.Rational(r, 100) * D(T)), D(T), ics={D(0): 1}).rhs
    key = penny(p * sol.subs(T, n))
    simple = p * (1 - sp.Rational(r * n, 100))
    yearly = penny(p / (1 + sp.Rational(r, 100)) ** n)
    slips = {'simple-discount': simple}
    if abs(yearly - key) > Decimal('0.01'):
        slips['yearly-discount'] = yearly
    return key, slips


# ---- fluency-l3-integrating-factor ----
def l3_factor(V):
    p = V['s'] * V['m'] * t ** int(V['n'])
    mu = sp.exp(sp.integrate(p, t))
    Y = sp.Function('Y')(t)
    assert sp.simplify(sp.diff(mu * Y, t) - mu * (Y.diff(t) + p * Y)) == 0
    return mu, {'e-to-the-p': sp.exp(p), 'sign-flipped': 1 / mu}


def l3_constant(V):
    a, s, y0 = V['a'], V['s'], V['y0']
    key = dsolve1(lambda Y: a * Y - a * s, y0)
    slips = {'steady-sign': (y0 + s) * sp.exp(a * t) - s}
    if y0 != 0:
        slips['inflow-dropped'] = y0 * sp.exp(a * t)
    return key, slips


def l3_savings(V):
    r, d, n = V['r'], V['d'], V['n']
    key = penny(dsolve1(lambda B: sp.Rational(r, 100) * B + d, 0).subs(t, n))
    return key, {'deposits-only': d * n, 'minus-one-dropped': penny(d * 100 / r * sp.exp(sp.Rational(r * n, 100)))}


# ---- fluency-l7-characteristic-equation ----
def prompt_roots(prompt, v):
    """Read v''+bv'+cv = 0 back from the prompt and solve b, c's characteristic equation."""
    m = re.search(r'\$(.+?) = 0\$', prompt).group(1)
    R = sp.Symbol('R')
    e = m.replace(v + "''", '(R**2)').replace(v + "'", '(R)').replace(v, '(1)')
    e = re.sub(r'(\d)\(', r'\1*(', e)
    return sorted(sp.solve(sp.sympify(e), R), key=lambda q: (sp.re(q), sp.im(q)))


ITEM_PROMPTS = {}


def l7_real(V):
    r1, r2 = V['r1'], V['r2']
    R = sp.Symbol('R')
    roots = sp.solve(sp.expand((R - r1) * (R - r2)), R)
    return list(roots), {'signs-flipped': [-r1, -r2], 'not-halved': [2 * r1, 2 * r2]}


def l7_complex(V):
    al, be = V['al'], V['be']
    R = sp.Symbol('R')
    roots = sp.solve(R ** 2 - 2 * al * R + al ** 2 + be ** 2, R)
    key = [q for q in roots if sp.im(q) > 0][0]
    return key, {'other-root': sp.conjugate(key), 'minus-b-dropped': -al + be * I, 'not-halved': al + 2 * be * I}


def l7_fit(V):
    r1, r2, c1, c2 = V['r1'], V['r2'], V['c1'], V['c2']
    b, c = -(r1 + r2), r1 * r2
    y0, v0 = c1 + c2, r1 * c1 + r2 * c2
    key = dsolve2(b, c, y0, v0)
    slips = {}
    if c1 != c2:
        slips['constants-swapped'] = c2 * sp.exp(r1 * t) + c1 * sp.exp(r2 * t)
    if y0 != 0:
        slips['one-constant'] = y0 * sp.exp(r1 * t)
    return key, slips


def l7_repeated(V):
    r, y0, k = V['r'], V['y0'], V['k']
    v0 = k + r * y0
    key = dsolve2(-2 * r, r ** 2, y0, v0)
    return key, {'rc1-forgotten': (y0 + v0 * t) * sp.exp(r * t), 't-term-dropped': y0 * sp.exp(r * t)}


def check_prompts():
    """The characteristic-root prompts show the equation whose roots are the key."""
    for fam, getroots in (('real-roots', lambda V: [V['r1'], V['r2']]),
                          ('complex-root', lambda V: [V['al'] - V['be'] * I, V['al'] + V['be'] * I])):
        for it in C.sample('fluency-l7-characteristic-equation', fam):
            V = it['vars']
            got = prompt_roots(it['prompt'], V['v'])
            want = sorted(getroots(V), key=lambda q: (sp.re(q), sp.im(q)))
            C.checked += 1
            if [sp.simplify(p - q) for p, q in zip(got, want)] != [0, 0]:
                C.fails.append('%s seed %s: prompt roots %s, vars give %s' % (fam, it['seed'], got, want))


FAMILIES = [
    ('fluency-l2-separable', 'constant-rate', l2_constant),
    ('fluency-l2-separable', 'rate-that-varies', l2_varies),
    ('fluency-l2-separable', 'square-rate', l2_square),
    ('fluency-l2-separable', 'discount', l2_discount),
    ('fluency-l3-integrating-factor', 'find-the-factor', l3_factor),
    ('fluency-l3-integrating-factor', 'constant-coefficient', l3_constant),
    ('fluency-l3-integrating-factor', 'savings-balance', l3_savings),
    ('fluency-l7-characteristic-equation', 'real-roots', l7_real),
    ('fluency-l7-characteristic-equation', 'complex-root', l7_complex),
    ('fluency-l7-characteristic-equation', 'fit-two-roots', l7_fit),
    ('fluency-l7-characteristic-equation', 'repeated-root', l7_repeated),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        C.check(set_id, fam, fn)
    check_prompts()
    C.finish()
