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
    value = float(value)
    slips = {k: float(v) for k, v in slips.items()}
    p = widget(lv, i, j)
    w = p['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    band = w['tol']['abs'] + 1e-12
    lv.claim(abs(w['answer'] - value) <= band, f'{tag} key {w["answer"]} within its band of {value:.8g}')
    sv_ = float(str(shown).replace('{,}', '').replace(',', ''))
    if w.get('unit') == '%':
        sv_ /= 100
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

# ====================================================================== level 2
def second_order(b, c, rhs, x0, v0):
    X = sp.Function('X')
    return sp.dsolve(sp.Eq(X(t).diff(t, 2) + b*X(t).diff(t) + c*X(t), rhs), X(t), ics={X(0): x0, X(t).diff(t).subs(t, 0): v0}).rhs


def level2():
    lv = Level('odes', 2)
    rr = sp.Symbol('rr')

    # ---- item 0: x'' + 4x' + 29x = 58, x(0) = x'(0) = 0
    roots = sp.solve(rr**2 + 4*rr + 29, rr)
    nr = np.roots([1, 4, 29])
    lv.claim(sorted(complex(z).imag for z in roots) == [-5, 5] and np.allclose(sorted(nr.imag), [-5, 5]) and np.allclose(nr.real, -2), 'roots -2 +- 5i (sympy, numpy)')
    expr_part(lv, 0, 0, [-2 + 5*sp.I, -2 - 5*sp.I], {'sign': [2 + 5*sp.I, 2 - 5*sp.I], 'no-half': [-4 + 10*sp.I, -4 - 10*sp.I]})
    numeric_part(lv, 0, 1, 58 / 29, {'no-divide': 58}, 2)
    xt = second_order(4, 29, 58, 0, 0)
    c1 = sp.Symbol('c1'); c2 = sp.Symbol('c2')
    gen = 2 + sp.exp(-2*t) * (c1*sp.cos(5*t) + c2*sp.sin(5*t))
    cs = sp.solve([gen.subs(t, 0), sp.diff(gen, t).subs(t, 0)], [c1, c2])
    lv.claim(cs[c1] == -2 and cs[c2] == sp.Rational(-4, 5), 'c1 = -2, c2 = -0.8')
    lv.claim(sp.simplify(xt - gen.subs(cs)) == 0, 'dsolve agrees with 2 - e^{-2t}(2cos5t + 0.8 sin5t)')
    sn = ivp(lambda tt, y: [y[1], 58 - 4*y[1] - 29*y[0]], [0, 0], 3)
    lv.claim(abs(sn.sol(1.0)[0] - float(xt.subs(t, 1))) < 1e-8, 'x(1) closed form against solve_ivp')
    c2v = float(cs[c2])
    numeric_part(lv, 0, 2, c2v, {'no-decay': 0, 'sign': -c2v}, -0.8)
    lv.claim(sp.simplify(sp.diff(xt, t) - sp.Rational(58, 5)*sp.exp(-2*t)*sp.sin(5*t)) == 0, "x' = 11.6 e^{-2t} sin 5t")
    tp = brentq(lambda x: sn.sol(x)[1], 0.3, 0.9)
    tpe = two(lv, 'first peak', sp.pi / 5, tp, 1e-7)
    numeric_part(lv, 0, 3, tpe, {'period': round(2*math.pi/5, 4), 'omega0': round(math.pi/math.sqrt(29), 4)}, '0.6283')
    over = (xt.subs(t, sp.pi/5) - 2) / 2
    ov = two(lv, 'overshoot fraction', over, (sn.sol(tp)[0] - 2) / 2, 1e-7)
    lv.claim(sp.simplify(over - sp.exp(-2*sp.pi/5)) == 0, 'overshoot = e^{-2pi/5}')
    zeta = 2 / sp.sqrt(29)
    lv.claim(abs(float(sp.exp(-zeta*sp.pi/sp.sqrt(1 - zeta**2))) - ov) < 1e-12, 'damping rule with zeta = 2/sqrt29 agrees')
    trough = float((xt.subs(t, 2*sp.pi/5) - 2) / 2)
    numeric_part(lv, 0, 4, ov, {'sign': round(-ov, 6), 'period': round(trough, 6)}, '28.46')
    lv.claim(abs(float(xt.subs(t, sp.pi/5)) - 2.5692) < 5e-5, 'peak x = 2.5692')

    # ---- item 1: x'' + 4x' + 5x = 10 cos t, x(0) = x'(0) = 0
    expr_part(lv, 1, 0, [-2 + sp.I, -2 - sp.I], {'sign': [2 + sp.I, 2 - sp.I], 'no-half': [-4 + 2*sp.I, -4 - 2*sp.I]})
    nr = np.roots([1, 4, 5])
    lv.claim(np.allclose(sorted(nr.imag), [-1, 1]) and np.allclose(nr.real, -2), 'roots -2 +- i (numpy)')
    Aa, Bb = sp.symbols('Aa Bb')
    xp = Aa*sp.cos(t) + Bb*sp.sin(t)
    res = sp.expand(sp.diff(xp, t, 2) + 4*sp.diff(xp, t) + 5*xp - 10*sp.cos(t))
    ab = sp.solve([res.coeff(sp.cos(t)), res.coeff(sp.sin(t))], [Aa, Bb])
    lv.claim(ab[Aa] == sp.Rational(5, 4) and ab[Bb] == sp.Rational(5, 4), 'A = B = 1.25')
    resn = sp.expand(sp.diff(xp, t, 2) + 5*xp - 10*sp.cos(t))
    abn = sp.solve([resn.coeff(sp.cos(t)), resn.coeff(sp.sin(t))], [Aa, Bb])
    xps = Aa*sp.cos(t) + Bb*sp.sin(t)
    ress = sp.expand(sp.diff(xps, t, 2) + 4*(Aa*sp.sin(t) - Bb*sp.cos(t)) + 5*xps - 10*sp.cos(t))  # first derivative with both signs flipped
    abs_ = sp.solve([ress.coeff(sp.cos(t)), ress.coeff(sp.sin(t))], [Aa, Bb])
    numeric_part(lv, 1, 1, 1.25, {'no-damping': float(abn[Bb]), 'sign': float(abs_[Bb])}, 1.25)
    xt = second_order(4, 5, 10*sp.cos(t), 0, 0)
    gen = sp.exp(-2*t)*(c1*sp.cos(t) + c2*sp.sin(t)) + sp.Rational(5, 4)*(sp.cos(t) + sp.sin(t))
    cs = sp.solve([gen.subs(t, 0), sp.diff(gen, t).subs(t, 0)], [c1, c2])
    lv.claim(cs[c1] == sp.Rational(-5, 4) and cs[c2] == sp.Rational(-15, 4) and sp.simplify(xt - gen.subs(cs)) == 0, 'c1 = -1.25, c2 = -3.75, dsolve agrees')
    numeric_part(lv, 1, 2, -3.75, {'no-decay': -1.25, 'sign': 1.25, 'drop-sign': 3.75}, -3.75)
    sn = ivp(lambda tt, y: [y[1], 10*math.cos(tt) - 4*y[1] - 5*y[0]], [0, 0], 2)
    xv = two(lv, 'x(pi/2)', xt.subs(t, sp.pi/2), sn.sol(math.pi/2)[0], 1e-8)
    at = lambda cc2: 1.25 + cc2*math.exp(-math.pi)
    numeric_part(lv, 1, 3, xv, {'no-decay': round(at(-1.25), 3), 'steady': 1.25, 'sign': round(at(1.25), 3)}, '1.088')
    lv.claim(abs(3.75*math.exp(-math.pi) - 0.1621) < 5e-5 and abs(math.exp(-math.pi) - 0.04321) < 5e-6 and abs(1.25*math.sqrt(2) - 1.77) < 0.005, 'printed 0.1621, 0.04321 and amplitude 1.77')

    # ---- item 2: x'' + bx' + 25x = 0, x(0) = 2, x'(0) = -4
    bb = sp.Symbol('bb', positive=True)
    bc = sp.solve(bb**2 - 100, bb)
    lv.claim(bc == [10], 'critical b = 10')
    numeric_part(lv, 2, 0, 10, {'omega0': 5, 'no-root': 100}, 10)
    lv.claim(sp.roots(rr**2 + 10*rr + 25, rr) == {-5: 2} and np.allclose(np.roots([1, 10, 25]), -5, atol=1e-6), 'repeated root -5')
    numeric_part(lv, 2, 1, -5, {'sign': 5, 'no-half': -10}, -5)
    xt = second_order(10, 25, 0, 2, -4)
    lv.claim(sp.simplify(xt - (2 + 6*t)*sp.exp(-5*t)) == 0, 'dsolve gives (2 + 6t)e^{-5t}')
    numeric_part(lv, 2, 2, 6, {'no-r': -4, 'sign': -4 - 10}, 6)
    sn = ivp(lambda tt, y: [y[1], -10*y[1] - 25*y[0]], [2, -4], 1)
    xv = two(lv, 'x(0.5)', xt.subs(t, sp.Rational(1, 2)), sn.sol(0.5)[0], 1e-8)
    numeric_part(lv, 2, 3, xv, {'no-r': 0, 'sign': (2 - 14*0.5)*math.exp(-2.5), 'no-t': round(2*math.exp(-2.5), 4)}, '0.4104')
    lv.claim(abs(math.exp(-2.5) - 0.082085) < 5e-7, 'e^{-2.5} = 0.082085')
    lv.claim(min(sn.sol(np.linspace(0, 1, 201))[0]) > 0, 'gap never crosses zero (sampled)')
    # under b = 8 or b = 12 the decay is slower or oscillates: the claim "any more is slower"
    slow = max(np.roots([1, 12, 25]).real)
    lv.claim(slow > -5, f'b = 12 has slowest root {slow:.3f} > -5, so slower')
    lv.check_wrongs('problems')
    return lv

# ====================================================================== level 3
def pm(st):
    """A pmatrix or [[a, b], [c, d]] text as a sympy Matrix."""
    st = st.strip()
    if st.startswith('[['):
        rows = st[2:-2].split('],[')
        return sp.Matrix([[ex(c) for c in row.split(',')] for row in rows])
    body = st.replace('\\begin{pmatrix}', '').replace('\\end{pmatrix}', '')
    return sp.Matrix([[ex(c) for c in row.split('&')] for row in body.split('\\\\')])


def mat_part(lv, i, j, M, slips):
    p = widget(lv, i, j)
    w = p['widget']
    tag = f'problems-{lv.n} items[{i}].parts[{j}]'
    for a in [w['answer']] + w.get('accept', []):
        lv.claim(pm(a) == M, f'{tag} form {a} equals {M.tolist()}')
    ws = {x['id']: pm(x['tex']) for x in w.get('wrong', [])}
    lv.claim(set(ws) == set(slips), f'{tag} wrong ids are the slips')
    for k, sv in slips.items():
        lv.claim(ws[k] == sv and ws[k] != M, f'{tag} wrong "{k}" is its slip {sv.tolist()} and differs from the key')
        lv.claim(k in p['feedback'].get('byKey', {}), f'{tag} wrong "{k}" has a byKey line')


def level3():
    lv = Level('odes', 3)

    # ---- item 0: x' = Ax, A = [[-7, 2], [-6, 1]], x(0) = (4, 2)
    A = sp.Matrix([[-7, 2], [-6, 1]])
    numeric_part(lv, 0, 0, A.det(), {'bc-sign': -7*1 + 2*(-6)}, 5)
    lv.claim(A.trace() == -6 and abs(np.linalg.det(np.array(A, dtype=float)) - 5) < 1e-9, 'trace -6, det 5 (sympy, numpy)')
    ev = sorted(A.eigenvals().keys())
    nev = sorted(np.linalg.eigvals(np.array(A, dtype=float)).real)
    lv.claim(ev == [-5, -1] and np.allclose(nev, [-5, -1]), 'eigenvalues -1 and -5 (sympy, numpy)')
    numset_part(lv, 0, 1, [-1, -5], {'trace-sign': sorted(np.roots([1, -6, 5]).real)})
    lv.claim(max(ev) < 0 and A.trace()**2 - 4*A.det() == 16, 'two real negative eigenvalues, tau^2 - 4Delta = 16: stable node')
    choice_part(lv, 0, 2, 'stable-node')
    lv.claim(A * sp.Matrix([1, 3]) == -1 * sp.Matrix([1, 3]) and A * sp.Matrix([1, 1]) == -5 * sp.Matrix([1, 1]), 'eigenvectors (1, 3) for -1 and (1, 1) for -5')
    c = sp.Matrix([[1, 1], [3, 1]]).solve(sp.Matrix([4, 2]))
    cn = np.linalg.solve(np.array([[1, 1], [3, 1]], float), [4, 2])
    lv.claim(list(c) == [-1, 5] and np.allclose(cn, [-1, 5]), 'c1 = -1, c2 = 5 (sympy, numpy)')
    csw = sp.Matrix([[1, 1], [1, 3]]).solve(sp.Matrix([4, 2]))
    numeric_part(lv, 0, 3, -1, {'identity': 4, 'swapped': int(csw[0]), 'drop-sign': 1}, -1)
    xt = -sp.exp(-t)*sp.Matrix([1, 3]) + 5*sp.exp(-5*t)*sp.Matrix([1, 1])
    lv.claim(sp.simplify(sp.diff(xt, t) - A*xt) == sp.zeros(2, 1) and xt.subs(t, 0) == sp.Matrix([4, 2]), "x(t) solves x' = Ax with x(0) = (4, 2)")
    lim = sp.limit(xt[1] / xt[0], t, sp.oo)
    An = np.array(A, dtype=float)
    sn = ivp(lambda tt, yy: An @ yy, [4, 2], 12)
    rv = two(lv, 'y/x as t grows', lim, sn.y[1][-1] / sn.y[0][-1], 1e-6)
    numeric_part(lv, 0, 4, rv, {'fast': 1, 'inverted': round(1 / 3, 6), 'start': 2 / 4}, 3)

    # ---- item 1: x' = x(6 - x - y), y' = y(x - 2)
    x, y = sp.symbols('x y', real=True)
    F = sp.Matrix([x*(6 - x - y), y*(x - 2)])
    eqs = sp.solve(list(F), [x, y], dict=True)
    pos = [e for e in eqs if e[x] > 0 and e[y] > 0]
    lv.claim(pos == [{x: 2, y: 4}] and {x: 6, y: 0} in eqs, 'only positive equilibrium (2, 4); (6, 0) is one too')
    w = widget(lv, 1, 0)['widget']
    lv.claim(w['answer'] == '(2,4)' and {k['id']: k['tex'] for k in w['wrong']} == {'swapped': '(4,2)', 'boundary': '(6,0)'}, 'part 1 key (2,4), slips (4,2) and (6,0)')
    J = F.jacobian([x, y]).subs({x: 2, y: 4})
    fn = sp.lambdify((x, y), F)
    h = 1e-6
    col = lambda a, b: np.array(fn(a, b), float).ravel()
    Jn = np.column_stack([(col(2 + h, 4) - col(2 - h, 4)) / (2*h), (col(2, 4 + h) - col(2, 4 - h)) / (2*h)])
    lv.claim(J == sp.Matrix([[-2, -2], [4, 0]]) and np.allclose(Jn, [[-2, -2], [4, 0]], atol=1e-6), 'J(2,4) = [[-2,-2],[4,0]] (symbolic, finite differences)')
    Jslip = sp.Matrix([[(6 - x - y), -x], [y, x - 2]]).subs({x: 2, y: 4})
    mat_part(lv, 1, 1, J, {'no-product': Jslip, 'transpose': J.T})
    tau, Dl = J.trace(), J.det()
    disc = tau**2 - 4*Dl
    lv.claim(tau == -2 and Dl == 8, 'tau = -2, Delta = 8')
    numeric_part(lv, 1, 2, disc, {'delta-sign': tau**2 + 4*Dl, 'no-four': tau**2 - Dl, 'drop-sign': -disc}, -28)
    evs = list(J.eigenvals().keys())
    lv.claim(all(sp.re(e) == -1 for e in evs) and sorted(sp.im(e) for e in evs) == [-sp.sqrt(7), sp.sqrt(7)], 'eigenvalues -1 +- i sqrt7')
    choice_part(lv, 1, 3, 'stable-spiral')
    per = 2*sp.pi / sp.sqrt(7)
    nev = np.linalg.eigvals(np.array(J, dtype=float))
    pv = two(lv, 'period of one turn', per, 2*math.pi / abs(nev[0].imag), 1e-9)
    # third route: the linearised flow returns to the same direction after one period (u(T) is a positive multiple of u(0))
    Jn_ = np.array(J, dtype=float)
    sl = ivp(lambda tt, u: Jn_ @ u, [1, 0], 3.5)
    uT = sl.sol(float(per))
    lv.claim(abs(uT[1]) < 1e-8 and uT[0] > 0 and abs(uT[0] - math.exp(-float(per))) < 1e-8, 'u(T) = e^{-T} u(0) after one period (solve_ivp)')
    numeric_part(lv, 1, 4, pv, {'centre': round(2*math.pi/math.sqrt(8), 3), 'no-half': round(2*math.pi/math.sqrt(28), 3)}, '2.375')
    lv.claim(abs(math.sqrt(7) - 2.6458) < 5e-5, 'sqrt7 = 2.6458')

    # ---- item 2: s'' + 4s' - 5s = 0
    A3 = sp.Matrix([[0, 1], [5, -4]])
    mat_part(lv, 2, 0, A3, {'signs': sp.Matrix([[0, 1], [-5, 4]]), 'swapped': sp.Matrix([[0, 1], [-4, 5]])})
    numeric_part(lv, 2, 1, A3.det(), {'sign': -A3.det(), 'trace': A3.trace()}, -5)
    A3n = np.array(A3, dtype=float)
    lv.claim(abs(np.linalg.det(A3n) + 5) < 1e-9, 'det -5 (numpy)')
    ev = sorted(A3.eigenvals().keys())
    lv.claim(ev == [-5, 1] and np.allclose(sorted(np.linalg.eigvals(A3n)), [-5, 1]), 'eigenvalues 1 and -5')
    numset_part(lv, 2, 2, [1, -5], {'trace-sign': sorted(np.roots([1, -4, -5]).real)})
    S = sp.Function('S')
    v0 = sp.Symbol('v0')
    st = sp.dsolve(S(t).diff(t, 2) + 4*S(t).diff(t) - 5*S(t), S(t), ics={S(0): 1, S(t).diff(t).subs(t, 0): v0}).rhs
    vs = sp.solve(sp.expand(st).coeff(sp.exp(t)), v0)
    lv.claim(vs == [-5], "s'(0) = -5 removes the e^t mode (dsolve)")
    good = ivp(lambda tt, u: [u[1], 5*u[0] - 4*u[1]], [1, -5], 3)
    bad = ivp(lambda tt, u: [u[1], 5*u[0] - 4*u[1]], [1, -4.9], 3)
    lv.claim(abs(good.y[0][-1]) < 1e-5 and bad.y[0][-1] > 0.1, "numerically s'(0) = -5 decays and -4.9 does not")
    lv.claim(A3 * sp.Matrix([1, -5]) == -5 * sp.Matrix([1, -5]), 'eigenvector (1, -5) for -5')
    numeric_part(lv, 2, 3, float(vs[0]), {'unstable': 1, 'sign': 5}, -5)
    lv.check_wrongs('problems')
    return lv


LEVELS = [level1, level2, level3]

if __name__ == '__main__':
    bad = 0
    for fn in LEVELS:
        lv = fn()
        n_bad = sum(1 for x in lv.results if not x[0])
        print(f'level {lv.n}: {len(lv.results) - n_bad} of {len(lv.results)} checks passed')
        bad += n_bad
    print('FAILURES' if bad else 'all checks passed', bad)
    sys.exit(1 if bad else 0)
