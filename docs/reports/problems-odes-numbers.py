"""Recompute every number in app/content/courses/odes/problems-1.json to problems-3.json twice.

Route 1 is exact: sympy (dsolve, solve, eigenvects, symbolic derivatives and limits).
Route 2 is a different method in floating point: scipy.integrate.solve_ivp on the equation itself,
numpy.roots and numpy.linalg.eig, brentq root finding and finite differences.

Per part:
- numeric: both routes agree; the key lies in its band; every wrong value equals its named slip (recomputed
  here, to the rounding asked), lies outside the key band, and no two wrong bands overlap; the key's printed
  value appears in feedback.correct.
- expression: the answer and every accept form equal the exact value (checked at sample points); every wrong
  form equals its named slip and differs from the key and from the other slips.
- choice: exactly one keyed option, the one the working picks, and every distractor has a why.
numbers_lib (Level.expect, check_wrongs, report) records every check. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-odes-numbers.py [--verbose]
"""
import math
import os
import re
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

TR = standard_transformations + (implicit_multiplication_application,)
t, q, B, r, s = sp.symbols('t q B r s', real=True)
SYM = {'t': t, 'q': q, 'B': B, 'r': r, 's': s, 'i': sp.I, 'exp': sp.exp, 'sqrt': sp.sqrt, 'pi': sp.pi}
FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|in pounds|per ?cent|percentage|%|exact', re.I)


def _group(st, k):
    depth = 0
    for j in range(k, len(st)):
        depth += st[j] == '{'
        depth -= st[j] == '}'
        if depth == 0:
            return st[k + 1:j], j + 1
    raise ValueError(st)


def tex2py(st):
    st = st.replace('\\left', '').replace('\\right', '').replace('\\,', '').replace(' ', '').replace('\\pi', 'pi')
    out, k = '', 0
    while k < len(st):
        if st.startswith('\\frac', k) or st.startswith('\\tfrac', k):
            k = st.index('{', k)
            a, k = _group(st, k)
            b, k = _group(st, k)
            out += f'(({tex2py(a)})/({tex2py(b)}))'
        elif st.startswith('\\sqrt', k):
            a, k = _group(st, k + 5)
            out += f'sqrt({tex2py(a)})'
        elif st.startswith('e^{', k):
            a, k = _group(st, k + 2)
            out += f'exp({tex2py(a)})'
        elif st.startswith('^{', k):
            a, k = _group(st, k + 1)
            out += f'**({tex2py(a)})'
        elif st[k] == '^':
            out += '**'
            k += 1
        else:
            out += st[k]
            k += 1
    return out


def ex(st):
    return parse_expr(tex2py(st), local_dict=SYM, transformations=TR)


def same(a, b, pts=(0.3, 0.9, 1.7, 2.6)):
    fa, fb = sp.lambdify(list(SYM.values())[:5], a), sp.lambdify(list(SYM.values())[:5], b)
    for p in pts:
        va, vb = complex(fa(p, p + .1, p + .2, p + .3, p + .4)), complex(fb(p, p + .1, p + .2, p + .3, p + .4))
        if abs(va - vb) > 1e-9 * max(1, abs(va)):
            return False
    return True


def widget(lv, i, j):
    return lv.files[f'problems-{lv.n}']['items'][i]['parts'][j]


def two(lv, label, exact, numeric, tol=1e-6):
    e = float(sp.N(exact)) if not isinstance(exact, (int, float)) else float(exact)
    lv.claim(abs(e - numeric) <= tol * max(1, abs(e)), f'{label}: exact {e:.8g} and numeric {numeric:.8g} agree')
    return e


def numeric_part(lv, i, j, value, slips, shown):
    """value: the true value; slips: {id: true slip value}; shown: the key as printed in feedback.correct."""
    p = widget(lv, i, j)
    w = p['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    band = w['tol']['abs'] + 1e-12
    lv.claim(abs(w['answer'] - value) <= band, f'{tag} key {w["answer"]} within its band of {value:.8g}')
    sv_ = float(str(shown).replace('{,}', '').replace(',', ''))
    lv.claim(abs(sv_ - value) <= band, f'{tag} printed key {shown} is taken by the band')
    lv.expect('problems', f'items[{i}].parts[{j}].feedback.correct', shown if isinstance(shown, str) else float(shown))
    if float(w['answer']) != round(w['answer']) or band > 1e-9:
        lv.claim(FORM.search(p['question']), f'{tag} question names a form')
    ws = {x['id']: x for x in w.get('wrong', [])}
    lv.claim(set(ws) == set(slips), f'{tag} wrong ids {sorted(ws)} are the slips recomputed {sorted(slips)}')
    for k, sv in slips.items():
        x = ws[k]
        wt = x.get('tol', {}).get('abs', 1e-9)
        lv.claim(abs(x['value'] - sv) <= max(wt, 1e-9), f'{tag} wrong "{k}" {x["value"]} is the slip {sv:.8g}')
        lv.claim(abs(x['value'] - w['answer']) > band + wt, f'{tag} wrong "{k}" outside the key band')
        lv.claim(k in p['feedback'].get('byKey', {}), f'{tag} wrong "{k}" has a byKey line')
    ids = list(ws)
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            x, y = ws[ids[a]], ws[ids[b]]
            lv.claim(abs(x['value'] - y['value']) > x.get('tol', {}).get('abs', 0) + y.get('tol', {}).get('abs', 0),
                     f'{tag} wrong bands "{ids[a]}" and "{ids[b]}" do not overlap')


def numset_part(lv, i, j, values, slips):
    p = widget(lv, i, j)
    w = p['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    lv.claim(sorted(w['answers']) == sorted(values), f'{tag} answers {w["answers"]} are {sorted(values)}')
    ws = {x['id']: sorted(float(v) for v in x['value'].split(',')) for x in w.get('wrong', [])}
    lv.claim(set(ws) == set(slips), f'{tag} wrong ids are the slips')
    for k, sv in slips.items():
        sv = sorted(float(v) for v in sv)
        lv.claim(np.allclose(ws[k], sv), f'{tag} wrong "{k}" {ws[k]} is the slip {sv}')
        lv.claim(not np.allclose(ws[k], sorted(values)), f'{tag} wrong "{k}" differs from the key')


def expr_part(lv, i, j, exact, slips, cmp=same):
    p = widget(lv, i, j)
    w = p['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    keys = w['answers'] if 'answers' in w else [w['answer']]
    if 'answers' in w:
        got = sorted([complex(sp.N(ex(a))) for a in keys], key=lambda z: (z.real, z.imag))
        want = sorted([complex(sp.N(e)) for e in exact], key=lambda z: (z.real, z.imag))
        lv.claim(all(abs(a - b) < 1e-9 for a, b in zip(got, want)) and len(got) == len(want), f'{tag} answers {keys} equal {want}')
        ws = {x['id']: x['tex'] for x in w.get('wrong', [])}
        for k, sv in slips.items():
            g = sorted([complex(sp.N(ex(a))) for a in ws[k].split(',')], key=lambda z: (z.real, z.imag))
            v = sorted([complex(sp.N(e)) for e in sv], key=lambda z: (z.real, z.imag))
            lv.claim(all(abs(a - b) < 1e-9 for a, b in zip(g, v)), f'{tag} wrong "{k}" is its slip')
            lv.claim(any(abs(a - b) > 1e-9 for a, b in zip(g, want)), f'{tag} wrong "{k}" differs from the key')
        lv.claim(set(ws) == set(slips), f'{tag} wrong ids are the slips')
        return
    for a in keys + w.get('accept', []):
        lv.claim(cmp(ex(a), exact), f'{tag} form {a} equals {exact}')
    ws = {x['id']: x['tex'] for x in w.get('wrong', [])}
    lv.claim(set(ws) == set(slips), f'{tag} wrong ids {sorted(ws)} are the slips {sorted(slips)}')
    for k, sv in slips.items():
        lv.claim(cmp(ex(ws[k]), sv), f'{tag} wrong "{k}" {ws[k]} is its slip {sv}')
        lv.claim(not cmp(ex(ws[k]), exact), f'{tag} wrong "{k}" differs from the key')
        lv.claim(k in p['feedback'].get('byKey', {}), f'{tag} wrong "{k}" has a byKey line')
    ids = list(ws)
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            lv.claim(not cmp(ex(ws[ids[a]]), ex(ws[ids[b]])), f'{tag} wrongs "{ids[a]}" and "{ids[b]}" differ')


def choice_part(lv, i, j, keyed):
    w = widget(lv, i, j)['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    good = [o['id'] for o in w['options'] if o.get('correct')]
    lv.claim(good == [keyed], f'{tag} keyed option {good} is {keyed}')
    lv.claim(all(o.get('correct') or o.get('why') for o in w['options']), f'{tag} every distractor has a why')


def ivp(f, y0, t1, **kw):
    sol = solve_ivp(f, (0, t1), np.atleast_1d(np.array(y0, dtype=float)), rtol=1e-11, atol=1e-12, dense_output=True, **kw)
    return sol


# ====================================================================== level 1
def level1():
    lv = Level('odes', 1)

    # ---- item 0 (p-lending-members): m' = -m^2 + 8m - 12, m(0) = 2.5 (symbol q here)
    f = -q**2 + 8*q - 12
    eq = sorted(sp.solve(f, q))
    roots = sorted(np.roots([-1, 8, -12]).real)
    lv.claim(eq == [2, 6] and np.allclose(roots, [2, 6]), 'p-lending-members equilibria 2 and 6 (sympy, numpy)')
    numset_part(lv, 0, 0, [2, 6], {'signs': sorted(np.roots([1, 8, 12]).real), 'no-constant': sorted(sp.solve(-q**2 + 8*q, q))})
    fp = sp.diff(f, q)
    d2, d6 = fp.subs(q, 2), fp.subs(q, 6)
    h = 1e-6
    fn = sp.lambdify(q, f)
    lv.claim(d2 == 4 and d6 == -4 and abs((fn(2 + h) - fn(2 - h)) / 2 / h - 4) < 1e-5 and abs((fn(6 + h) - fn(6 - h)) / 2 / h + 4) < 1e-5,
             "f'(2) = 4 and f'(6) = -4 (symbolic, finite difference)")
    choice_part(lv, 0, 1, 'six-stable')
    # separation: exact solution and k
    # closed form from the ratio, checked against the equation symbolically (dsolve cannot fit the constant here)
    E4 = sp.exp(4*t) / 7
    qt = (2 + 6*E4) / (1 + E4)
    lv.claim(sp.simplify(sp.diff(qt, t) - f.subs(q, qt)) == 0 and qt.subs(t, 0) == sp.Rational(5, 2), 'q(t) from the ratio solves the equation with q(0) = 2.5')
    ratio = sp.simplify((qt - 2) / (6 - qt))
    lv.claim(sp.simplify(ratio - sp.Rational(1, 7) * sp.exp(4*t)) == 0, 'p-lending-members ratio (q-2)/(6-q) = e^{4t}/7 from dsolve')
    pf = sp.apart(1 / ((q - 2) * (6 - q)), q)
    lv.claim(sp.simplify(pf - sp.Rational(1, 4) * (1 / (q - 2) + 1 / (6 - q))) == 0, 'partial fractions with 1/4 as stated')
    numeric_part(lv, 0, 2, 4, {'no-quarter': 1}, 4)
    A = sp.Rational(1, 2) / sp.Rational(7, 2)
    numeric_part(lv, 0, 3, float(A), {'inverted': 7, 'over-m': 0.5 / 2.5, 'gap': 0.5 / 4}, '0.1429')
    lv.expect('problems', 'items[0].parts[3].feedback.correct', '\\tfrac17')
    T = sp.log(21) / 4
    sol_n = ivp(lambda tt, y: -y**2 + 8*y - 12, [2.5], 1.0, events=lambda tt, y: y[0] - 5)
    tn = sol_n.t_events[0][0]
    tv = two(lv, 'time to membership 5', T, tn)
    slip = lambda a, k: math.log(3 / a) / k
    numeric_part(lv, 0, 4, tv, {'inverted': round(slip(7, 4), 3), 'no-quarter': round(slip(1 / 7, 1), 3),
                                'over-m': round(slip(0.2, 4), 3), 'gap': round(slip(0.125, 4), 3)}, '0.761')
    lv.claim(3 < tv * 365.25 / 12 / 7 < 3.5, 'a little over three weeks')

    # ---- item 1: r' = 1.25(3 + 0.6t - r), r(0) = 5
    k = sp.Rational(5, 4)
    R = sp.Function('R')
    rt = sp.dsolve(sp.Eq(R(t).diff(t), k * (3 + sp.Rational(3, 5)*t - R(t))), R(t), ics={R(0): 5}).rhs
    expr_part(lv, 1, 0, sp.exp(k*t), {'sign': sp.exp(-k*t), 'no-t': sp.exp(k)})
    lv.claim(sp.simplify(sp.diff(sp.exp(k*t) * r, t).subs(sp.diff(r, t), 0) - k*sp.exp(k*t)*r) == 0, 'mu = e^{1.25t} gives the product rule')
    expr_part(lv, 1, 1, rt, {'no-lag': 3 + 0.6*t + 2*sp.exp(-k*t), 'sign': 3.48 + 0.6*t + 1.52*sp.exp(-k*t), 'no-start': 2.52 + 0.6*t})
    lv.claim(abs(sp.N(rt - (2.52 + 0.6*t + 2.48*sp.exp(-k*t))).subs(t, 1.3)) < 1e-12, 'dsolve gives 2.52 + 0.6t + 2.48e^{-1.25t}')
    byparts = sp.integrate(k*sp.exp(k*t)*(3 + sp.Rational(3, 5)*t), t)
    lv.claim(sp.simplify(byparts - sp.exp(k*t)*(sp.Rational(63, 25) + sp.Rational(3, 5)*t)) == 0, 'by parts: e^{1.25t}(2.52 + 0.6t)')
    sn = ivp(lambda tt, y: 1.25 * (3 + 0.6*tt - y), [5], 3)
    lv.claim(abs(sn.sol(2.0)[0] - float(rt.subs(t, 2))) < 1e-8, 'r(2) closed form against solve_ivp')
    hl = two(lv, 'half-life', sp.log(2) / k, brentq(lambda x: math.exp(-1.25 * x) - 0.5, 0, 5))
    numeric_part(lv, 1, 2, hl, {'mean-life': 1 / 1.25, 'times': round(math.log(2) * 1.25, 4)}, '0.5545')
    tmin_exact = sp.solve(sp.diff(rt, t), t)[0]
    tmin_num = sn.t[np.argmin(sn.y[0])]
    tmin_num = brentq(lambda x: sn.sol(x + 1e-6)[0] - sn.sol(x - 1e-6)[0], 0.5, 2.5)
    tm = two(lv, 'time r is lowest', tmin_exact, tmin_num, 1e-5)
    numeric_part(lv, 1, 3, tm, {'no-chain': round(math.log(2.48 / 0.6) / 1.25, 3), 'no-lag': round(math.log(2.5 / 0.6) / 1.25, 3),
                                'sign': round(math.log(1.25 * 1.52 / 0.6) / 1.25, 3)}, '1.314')
    rmin = float(rt.subs(t, tmin_exact))
    lv.claim(abs(rmin - (3 + 0.6 * tm)) < 1e-9 and abs(rmin - 3.79) < 0.005, f'at the trough r = theta = {rmin:.4f} (about 3.79)')
    lv.claim(abs(tm / hl - 2.37) < 0.005, f'trough at {tm / hl:.4f} half-lives (about 2.37)')
    lv.claim(abs(3.1 / 0.6 - 5.167) < 0.0005, '3.1/0.6 = 5.167')
    lv.claim(float(sp.diff(rt, t).subs(t, 0)) < 0, 'r first falls: r\'(0) < 0')

    # ---- item 2: B' = 0.04B + 2000e^{0.02t}, B(0) = 0
    Bf = sp.Function('Bf')
    a, g = sp.Rational(1, 25), sp.Rational(1, 50)
    bt = sp.dsolve(sp.Eq(Bf(t).diff(t), a*Bf(t) + 2000*sp.exp(g*t)), Bf(t), ics={Bf(0): 0}).rhs
    expr_part(lv, 2, 0, a*B + 2000*sp.exp(g*t), {'flat': a*B + 2000, 'no-interest': 2000*sp.exp(g*t), 'swapped': g*B + 2000*sp.exp(a*t)})
    expr_part(lv, 2, 1, sp.exp(-a*t), {'sign': sp.exp(a*t), 'forcing': sp.exp(g*t)})
    flat = sp.dsolve(sp.Eq(Bf(t).diff(t), a*Bf(t) + 2000), Bf(t), ics={Bf(0): 0}).rhs
    expr_part(lv, 2, 2, bt, {'no-c': -100000*sp.exp(g*t), 'flat': flat, 'sign-int': 100000*(sp.exp(g*t) - sp.exp(a*t))})
    sn = ivp(lambda tt, y: 0.04*y + 2000*math.exp(0.02*tt), [0], 10)
    b10 = two(lv, 'B(10)', bt.subs(t, 10), sn.y[0][-1], 1e-8)
    noint = float(sp.integrate(2000*sp.exp(g*t), (t, 0, 10)))
    numeric_part(lv, 2, 3, b10, {'flat': round(float(flat.subs(t, 10)), 2), 'no-interest': round(noint, 2)}, '27{,}042')
    lv.claim(round(b10 - float(flat.subs(t, 10))) == 2451 and round(b10 - noint) == 4902 and round(noint) == 22140, 'gaps £2,451, £4,902 and payments £22,140')
    lv.claim(abs(math.exp(0.4) - 1.491825) < 5e-7 and abs(math.exp(0.2) - 1.221403) < 5e-7 and abs(math.exp(.4) - math.exp(.2) - 0.270422) < 5e-7, 'e^0.4, e^0.2 and the gap as printed')
    lv.check_wrongs('problems')
    return lv


LEVELS = [level1]

if __name__ == '__main__':
    bad = 0
    for fn in LEVELS:
        lv = fn()
        n_bad = sum(1 for x in lv.results if not x[0])
        print(f'level {lv.n}: {len(lv.results) - n_bad} of {len(lv.results)} checks passed')
        bad += n_bad
    print('FAILURES' if bad else 'all checks passed', bad)
    sys.exit(1 if bad else 0)
