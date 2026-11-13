"""Second read of odes problems-1 to -3: every key, wrong value and printed number recomputed by the reader.

Imports nothing from the author's script. Each equation is typed here from the item's prose, solved with sympy
dsolve, checked by substitution, and integrated again with scipy solve_ivp. Each phase-plane class is read from
the trace and determinant by classify() below and checked against numpy eigenvalues. Printed numbers are checked
by formatting the reader's value and looking for it in the string that prints it.

Run from the repo root:  <scratchpad>/venv/bin/python docs/reports/problems-odes-numbers-read.py
Exit 0 on correct content. A check that fails on wrong content stays failing.
"""
import json
import math
import os
import re
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'odes')
SETS = {n: json.load(open(os.path.join(ROOT, f'problems-{n}.json'))) for n in (1, 2, 3)}
COURSE = json.load(open(os.path.join(ROOT, 'course.json')))

fails = 0
count = 0


def chk(name, cond, detail=''):
    global fails, count
    count += 1
    if not cond:
        fails += 1
        print('FAIL', name, detail)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def item(n, iid):
    return next(i for i in SETS[n]['items'] if i['id'] == iid)


def part(n, iid, k):
    return item(n, iid)['parts'][k - 1]


def wrongs(p):
    return {w['id']: w for w in p['widget'].get('wrong', [])}


def texts(p):
    fb = p['feedback']
    out = [p['question'], fb.get('correct', ''), fb.get('generic', ''), p['explain']['text']]
    out += list(fb.get('byKey', {}).values())
    out += [o.get('why', '') + ' ' + o.get('text', '') for o in p['widget'].get('options', [])]
    return ' '.join(out)


def printed(name, p, *strings, where=None):
    """Each string (a number as the reader formats it) must be printed in the part (or in the named text)."""
    hay = where if where is not None else texts(p)
    for s in strings:
        chk(f'{name}: prints {s}', s in hay)


t, B, m, r_, x, y, s = sp.symbols('t B m r x y s')


def tex2sym(tex):
    """A small TeX reader for the keys of these sets: e^{..}, \\frac, decimals, implicit products, i."""
    z = tex.replace('\\\\', '\\')
    z = re.sub(r'\\[td]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', z)
    z = re.sub(r'e\^\{([^{}]*)\}', r'exp(\1)', z)
    z = z.replace('{', '(').replace('}', ')').replace('^', '**')
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    tr = standard_transformations + (implicit_multiplication_application,)
    return parse_expr(z, local_dict={'t': t, 'B': B, 'i': sp.I, 'exp': sp.exp}, transformations=tr)


def same_expr(a, b, syms=(t, B)):
    d = sp.simplify(sp.nsimplify(a - b, rational=True))
    if d == 0:
        return True
    f = sp.lambdify(syms, a - b, 'numpy')
    return all(abs(complex(f(u, v))) < 1e-9 for u, v in ((0.3, 1.7), (1.1, -2.0), (2.9, 40.0)))


def matrix_of(tex):
    z = tex.replace('\\\\', '\\')
    mm = re.search(r'begin\{pmatrix\}(.*?)\\end\{pmatrix\}', z)
    if mm:
        return [[sp.nsimplify(c) for c in row.split('&')] for row in mm.group(1).split('\\')]
    return [[sp.nsimplify(c) for c in row] for row in json.loads(tex)]


def classify(tau, delta):
    """Reader's own rule from the trace and determinant (l12)."""
    if delta < 0:
        return 'saddle'
    if delta == 0:
        return 'degenerate'
    disc = tau * tau - 4 * delta
    if tau == 0:
        return 'centre'
    side = 'stable' if tau < 0 else 'unstable'
    return f'{side} node' if disc >= 0 else f'{side} spiral'


def classify_eig(A):
    ev = np.linalg.eigvals(np.array(A, dtype=float))
    if abs(ev[0].imag) > 1e-12:
        if abs(ev[0].real) < 1e-12:
            return 'centre'
        return ('stable' if ev[0].real < 0 else 'unstable') + ' spiral'
    a, b = sorted(ev.real)
    if a * b < 0:
        return 'saddle'
    return ('stable' if b < 0 else 'unstable') + ' node'


def correct_option(p):
    return next(o['id'] for o in p['widget']['options'] if o.get('correct'))


def ivp(f, y0, T, **kw):
    return solve_ivp(f, (0, T), y0, rtol=1e-11, atol=1e-13, dense_output=True, **kw)


# ---------------------------------------------------------------------------------------------- shape, every set
FORM = re.compile(r'whole number|decimal|fraction|places|nearest|separated by a comma|percentage')
for n, S in SETS.items():
    lessons = COURSE['levels'][n - 1]['lessons']
    chk(f'set {n}: 3 to 5 items', 3 <= len(S['items']) <= 5)
    chk(f'set {n}: a difficulty 5', any(i['difficulty'] == 5 for i in S['items']))
    typed = total = 0
    for it in S['items']:
        chk(f"{it['id']}: difficulty 3 to 5", 3 <= it['difficulty'] <= 5)
        chk(f"{it['id']}: 3 to 5 parts", 3 <= len(it['parts']) <= 5)
        chk(f"{it['id']}: skill of the level", it['skills'] == [['de-first'], ['de-second'], ['de-systems']][n - 1])
        for k, p in enumerate(it['parts'], 1):
            w = p['widget']
            total += 1
            typed += w['kind'] in ('numeric', 'expression')
            nm = f"{it['id']} part {k}"
            if k > 1:
                # lending part 3 restates the equilibria of part 1 inside the factors (m - 2)(6 - m)
                chk(f'{nm}: restates ("Using ...")', p['question'].startswith('Using ') or 'from part' in p['question']
                    or '(m - 2)(6 - m)' in p['question'])
            if w['kind'] == 'numeric':
                chk(f'{nm}: states its form', bool(FORM.search(p['question'])), p['question'][-60:])
                keys = w.get('answers', [w.get('answer')])
                tol = w['tol']['abs']
                bands = []
                for wr in w.get('wrong', []):
                    chk(f"{nm}: wrong {wr['id']} has a line", wr['id'] in p['feedback'].get('byKey', {}))
                    if isinstance(wr['value'], str):
                        vals = sorted(float(v) for v in wr['value'].split(','))
                        chk(f"{nm}: wrong pair {wr['id']} is not the key", vals != sorted(float(v) for v in keys))
                        continue
                    wt = wr.get('tol', {}).get('abs', tol)
                    chk(f"{nm}: wrong {wr['id']} outside the key band", abs(wr['value'] - keys[0]) > tol + wt,
                        f"{wr['value']} key {keys[0]}")
                    bands.append((wr['value'] - wt, wr['value'] + wt, wr['id']))
                bands.sort()
                for a, b in zip(bands, bands[1:]):
                    chk(f'{nm}: wrong bands {a[2]} and {b[2]} apart', a[1] < b[0])
                mdp = re.search(r'to (\d) decimal places', p['question'])
                if mdp and 'answer' in w:
                    dp = int(mdp.group(1))
                    scale = 100 if w.get('unit') == '%' else 1
                    v = round(w['answer'] * scale, dp) / scale
                    chk(f'{nm}: key rounded as asked is accepted', abs(v - w['answer']) <= tol)
                    for wr in w.get('wrong', []):
                        if isinstance(wr['value'], str):
                            continue
                        chk(f"{nm}: wrong {wr['id']} is given at the asked rounding or a band that takes it",
                            abs(round(wr['value'] * scale, dp) / scale - wr['value']) <= wr.get('tol', {}).get('abs', tol))
            elif w['kind'] == 'expression':
                for wr in w.get('wrong', []):
                    chk(f"{nm}: wrong {wr['id']} has a line", wr['id'] in p['feedback'].get('byKey', {}))
            else:
                chk(f'{nm}: one correct option', sum(1 for o in w['options'] if o.get('correct')) == 1)
                chk(f'{nm}: every other option has a why', all(o.get('why') for o in w['options'] if not o.get('correct')))
    chk(f'set {n}: two thirds typed', typed * 3 >= total * 2, f'{typed}/{total}')

# ================================================================================================= LEVEL 1
# ---- p-lending-members: m' = -m^2 + 8m - 12, m(0) = 2.5
f = -m**2 + 8 * m - 12
eq = sorted(sp.solve(f, m))
p = part(1, 'p-lending-members', 1)
chk('lend 1: equilibria', eq == [2, 6] and sorted(p['widget']['answers']) == [2, 6])
chk('lend 1: signs slip', sorted(sp.solve(m**2 + 8 * m + 12, m)) == [-6, -2] and wrongs(p)['signs']['value'] == '-2, -6')
chk('lend 1: no-constant slip', sorted(sp.solve(-m**2 + 8 * m, m)) == [0, 8] and wrongs(p)['no-constant']['value'] == '0, 8')
chk('lend 1: factor', sp.expand(-(m - 2) * (m - 6) - f) == 0)
p = part(1, 'p-lending-members', 2)
fp = sp.diff(f, m)
chk("lend 2: f'(2) = 4, f'(6) = -4", fp.subs(m, 2) == 4 and fp.subs(m, 6) == -4)
chk('lend 2: key', correct_option(p) == 'six-stable')
# numerically: starts either side of each equilibrium
for start, end in ((2.5, 6), (5.9, 6), (7.5, 6), (2.01, 6)):
    sol = ivp(lambda tt, u: [-u[0]**2 + 8 * u[0] - 12], [start], 12)
    chk(f'lend 2: path from {start} ends at {end}', close(sol.y[0, -1], end, 1e-6))
sol = ivp(lambda tt, u: [-u[0]**2 + 8 * u[0] - 12], [1.99], 1.0)
chk('lend 2: path from 1.99 leaves 2 downwards', sol.y[0, -1] < 1.9)
printed('lend 2', p, "$f'(2) = 4 > 0$", "$f'(6) = -4 < 0$")
uu = sp.symbols('u')
chk('lend 2: the gap u = m - 6 obeys u\' = -4u - u^2, so the linear law is only near', sp.expand(f.subs(m, 6 + uu) - (-4 * uu - uu**2)) == 0)
chk('lend 2: explain says the gap nearly obeys the linear law (l4 wording)', 'nearly obeys' in p['explain']['text'])
# part 3: partial fractions and k
p = part(1, 'p-lending-members', 3)
chk('lend 3: partial fractions', sp.simplify(1 / ((m - 2) * (6 - m)) - sp.Rational(1, 4) * (1 / (m - 2) + 1 / (6 - m))) == 0)
M = sp.Function('M')
gen = sp.dsolve(sp.Eq(M(t).diff(t), -M(t)**2 + 8 * M(t) - 12), M(t)).rhs
C1 = sp.Symbol('C1')
cands = [sp.simplify(gen.subs(C1, c)) for c in sp.solve(sp.Eq(gen.subs(t, 0), sp.Rational(5, 2)), C1)]
chk('lend 3: dsolve gives one solution through m(0) = 2.5', len(set(cands)) == 1, str(cands))
msol = cands[0]
chk('lend 3: dsolve solution satisfies the equation', sp.simplify(msol.diff(t) - (-msol**2 + 8 * msol - 12)) == 0)
chk('lend 3: m(0) = 2.5', sp.simplify(msol.subs(t, 0) - sp.Rational(5, 2)) == 0)
ratio = sp.simplify((msol - 2) / (6 - msol))
chk('lend 3,4: ratio is (1/7)e^{4t}', sp.simplify(ratio - sp.exp(4 * t) / 7) == 0, str(ratio))
chk('lend 3: key k = 4', p['widget']['answer'] == 4 and wrongs(p)['no-quarter']['value'] == 1)
chk('lend 3: explain integrates in m, not another letter', 'dq' not in p['explain']['text'],
    'explain prints \\int dq/(m - 2): the variable is m')
p = part(1, 'p-lending-members', 4)
A = sp.Rational(1, 2) / sp.Rational(7, 2)
chk('lend 4: A = 1/7', A == sp.Rational(1, 7) and close(p['widget']['answer'], 1 / 7, 1e-6))
w = wrongs(p)
chk('lend 4: slips', close(w['inverted']['value'], 3.5 / 0.5) and close(w['over-m']['value'], 0.5 / 2.5) and close(w['gap']['value'], 0.5 / 4))
printed('lend 4', p, f'{1/7:.4f}')
p = part(1, 'p-lending-members', 5)
tstar = sp.log(21) / 4
chk('lend 5: solve m(t) = 5', sp.solveset(sp.Eq(msol, 5), t, sp.S.Reals) == sp.FiniteSet(tstar) or close(sp.nsolve(msol - 5, t, 0.7), float(tstar), 1e-12))
chk('lend 5: key', close(p['widget']['answer'], float(tstar), 5e-7))
sol = ivp(lambda tt, u: [-u[0]**2 + 8 * u[0] - 12], [2.5], 2)
tnum = brentq(lambda tt: sol.sol(tt)[0] - 5, 0.1, 2)
chk('lend 5: solve_ivp reaches 5 at the key time', close(tnum, float(tstar), 1e-8), str(tnum))
w = wrongs(p)
for wid, Av, kv in (('inverted', 7, 4), ('no-quarter', 1 / 7, 1), ('over-m', 0.2, 4), ('gap', 0.125, 4)):
    chk(f'lend 5: slip {wid}', close(w[wid]['value'], math.log(3 / Av) / kv, 5e-4), f"{math.log(3 / Av) / kv}")
printed('lend 5', p, f'{float(tstar):.3f}', '$e^{4t} = 21$', '$e^{4t} = 15$', '$e^{4t} = 24$', r'$e^{4t} = \tfrac37$')
chk('lend 5: a little over three weeks', 3 < float(tstar) * 365.25 / 12 / 7 < 3.6)

# ---- p-moving-target: r' = 1.25(3 + 0.6t - r), r(0) = 5
R = sp.Function('R')
kap = sp.Rational(5, 4)
ds = sp.dsolve(sp.Eq(R(t).diff(t), kap * (3 + sp.Rational(3, 5) * t - R(t))), R(t), ics={R(0): 5})
rsol = sp.expand(ds.rhs)
chk('target: dsolve solution satisfies the equation', sp.simplify(rsol.diff(t) - kap * (3 + sp.Rational(3, 5) * t - rsol)) == 0)
p = part(1, 'p-moving-target', 1)
mu = tex2sym(p['widget']['answer'])
chk('target 1: mu makes one derivative', sp.simplify((mu * R(t)).diff(t) - mu * (R(t).diff(t) + kap * R(t))) == 0)
for a in p['widget']['accept']:
    chk(f'target 1: accept {a}', same_expr(tex2sym(a), mu))
for wr in p['widget']['wrong']:
    chk(f"target 1: wrong {wr['id']} differs", not same_expr(tex2sym(wr['tex']), mu))
p = part(1, 'p-moving-target', 2)
key = tex2sym(p['widget']['answer'])
chk('target 2: key is the dsolve solution', same_expr(key, rsol), str(rsol))
for a in p['widget']['accept']:
    chk(f'target 2: accept {a}', same_expr(tex2sym(a), rsol))
rnum = ivp(lambda tt, u: [1.25 * (3 + 0.6 * tt - u[0])], [5.0], 6)
for tt in (0.3, 1.0, 1.3138, 2.5, 6.0):
    chk(f'target 2: solve_ivp agrees at t = {tt}', close(rnum.sol(tt)[0], float(key.subs(t, tt)), 1e-8))
byparts = sp.integrate(kap * sp.exp(kap * t) * (3 + sp.Rational(3, 5) * t), t)
chk('target 2: by parts', sp.simplify(byparts - sp.exp(kap * t) * (sp.Rational(63, 25) + sp.Rational(3, 5) * t)) == 0)
w = {wr['id']: tex2sym(wr['tex']) for wr in p['widget']['wrong']}
chk('target 2: slip no-lag (line = target, C = 5 - 3)', same_expr(w['no-lag'], 3 + 0.6 * t + 2 * sp.exp(-kap * t)))
chk('target 2: slip sign (3 + 0.48, C = 5 - 3.48)', same_expr(w['sign'], 3.48 + 0.6 * t + 1.52 * sp.exp(-kap * t)))
chk('target 2: slip no-start', same_expr(w['no-start'], 2.52 + 0.6 * t))
for wid, e in w.items():
    chk(f'target 2: wrong {wid} differs from the key', not same_expr(e, rsol))
printed('target 2', p, '0.48', '2.52', '2.48')
chk('target 2: 0.6/1.25 = 0.48, 3 - 0.48 = 2.52, 5 - 2.52 = 2.48', close(0.6 / 1.25, 0.48) and close(3 - 0.48, 2.52) and close(5 - 2.52, 2.48))
p = part(1, 'p-moving-target', 3)
half = math.log(2) / 1.25
chk('target 3: half-life', close(p['widget']['answer'], half, 5e-7))
chk('target 3: by root-finding', close(brentq(lambda tt: math.exp(-1.25 * tt) - 0.5, 0, 2), half, 1e-10))
w = wrongs(p)
chk('target 3: slips', close(w['mean-life']['value'], 1 / 1.25) and close(w['times']['value'], math.log(2) * 1.25, 5e-5))
printed('target 3', p, f'{half:.4f}', f'{math.log(2):.4f}')
p = part(1, 'p-moving-target', 4)
tmin = math.log(3.1 / 0.6) / 1.25
chk('target 4: key', close(p['widget']['answer'], tmin, 5e-7))
chk("target 4: r' = 0.6 - 3.1e^{-1.25t}", same_expr(rsol.diff(t), 0.6 - 3.1 * sp.exp(-kap * t)))
res = minimize_scalar(lambda tt: rnum.sol(tt)[0], bounds=(0, 6), method='bounded', options={'xatol': 1e-10})
chk('target 4: minimum of the solve_ivp path', close(res.x, tmin, 1e-5), str(res.x))
chk('target 4: falls first, then climbs', rnum.sol(0.5)[0] < 5 and rnum.sol(6)[0] > rnum.sol(tmin)[0])
w = wrongs(p)
chk('target 4: slip no-chain', close(w['no-chain']['value'], math.log(2.48 / 0.6) / 1.25, 5e-4))
chk('target 4: slip no-lag (C = 2)', close(w['no-lag']['value'], math.log(1.25 * 2 / 0.6) / 1.25, 5e-4))
chk('target 4: slip sign (C = 1.52)', close(w['sign']['value'], math.log(1.25 * 1.52 / 0.6) / 1.25, 5e-4))
rmin = float(key.subs(t, tmin))
chk('target 4: r = theta at the minimum', close(rmin, 3 + 0.6 * tmin, 1e-9))
printed('target 4', p, f'{tmin:.3f}', f'{3.1 / 0.6:.3f}', f'{tmin / half:.2f} half-lives', f'{rmin:.2f} per cent')

# ---- p-rising-pension: B' = 0.04B + 2000e^{0.02t}, B(0) = 0
Bf = sp.Function('Bf')
ds = sp.dsolve(sp.Eq(Bf(t).diff(t), sp.Rational(1, 25) * Bf(t) + 2000 * sp.exp(t / 50)), Bf(t), ics={Bf(0): 0})
bsol = sp.expand(ds.rhs)
chk('pension: dsolve satisfies the equation', sp.simplify(bsol.diff(t) - bsol / 25 - 2000 * sp.exp(t / 50)) == 0)
p = part(1, 'p-rising-pension', 1)
keyrhs = tex2sym(p['widget']['answer'])
chk('pension 1: key', same_expr(keyrhs, 0.04 * B + 2000 * sp.exp(0.02 * t)))
for a in p['widget']['accept']:
    chk('pension 1: accept', same_expr(tex2sym(a), keyrhs))
for wr in p['widget']['wrong']:
    chk(f"pension 1: wrong {wr['id']} differs", not same_expr(tex2sym(wr['tex']), keyrhs))
chk('pension 1: payments rise 2% a year compounded continuously', close(2000 * math.exp(0.02), 2000 * 1.0202013, 1e-3))
p = part(1, 'p-rising-pension', 2)
mu = tex2sym(p['widget']['answer'])
chk('pension 2: mu', sp.simplify((mu * Bf(t)).diff(t) - mu * (Bf(t).diff(t) - Bf(t) / 25)) == 0)
for a in p['widget']['accept']:
    chk('pension 2: accept', same_expr(tex2sym(a), mu))
for wr in p['widget']['wrong']:
    chk(f"pension 2: wrong {wr['id']} differs", not same_expr(tex2sym(wr['tex']), mu))
p = part(1, 'p-rising-pension', 3)
key = tex2sym(p['widget']['answer'])
chk('pension 3: key is the dsolve solution', same_expr(key, bsol), str(bsol))
for a in p['widget']['accept']:
    chk('pension 3: accept', same_expr(tex2sym(a), bsol))
bnum = ivp(lambda tt, u: [0.04 * u[0] + 2000 * math.exp(0.02 * tt)], [0.0], 10)
for tt in (1, 5, 10):
    chk(f'pension 3: solve_ivp agrees at t = {tt}', close(bnum.sol(tt)[0], float(key.subs(t, tt)), 1e-5))
flat = sp.dsolve(sp.Eq(Bf(t).diff(t), Bf(t) / 25 + 2000), Bf(t), ics={Bf(0): 0}).rhs
w = {wr['id']: tex2sym(wr['tex']) for wr in p['widget']['wrong']}
chk('pension 3: slip flat is the flat-payment fund', same_expr(w['flat'], flat))
chk('pension 3: slip no-c', same_expr(w['no-c'], -100000 * sp.exp(0.02 * t)))
chk('pension 3: slip sign-int', same_expr(w['sign-int'], -bsol))
chk('pension 3: integral', sp.simplify(sp.integrate(2000 * sp.exp(-t / 50), t) + 100000 * sp.exp(-t / 50)) == 0)
p = part(1, 'p-rising-pension', 4)
b10 = 100000 * (math.exp(0.4) - math.exp(0.2))
chk('pension 4: key', close(p['widget']['answer'], b10, 0.005) and close(bnum.sol(10)[0], b10, 1e-4))
w = wrongs(p)
flat10 = float(flat.subs(t, 10))
paid = quad(lambda tt: 2000 * math.exp(0.02 * tt), 0, 10)[0]
chk('pension 4: slip flat', close(w['flat']['value'], flat10, 0.005))
chk('pension 4: slip no-interest is the payments made', close(w['no-interest']['value'], paid, 0.005))
printed('pension 4', p, f'{round(b10):,}'.replace(',', '{,}'), f'{math.exp(0.4):.5f}', f'{math.exp(0.2):.5f}',
        f'{math.exp(0.4):.6f}', f'{math.exp(0.2):.6f}', f'{math.exp(0.4) - math.exp(0.2):.6f}',
        f'£{round(b10 - flat10):,}', f'£{round(b10 - paid):,}', f'£{round(paid):,}')

# ================================================================================================= LEVEL 2
X = sp.Function('X')


def second_order(b, c, forcing, x0, v0):
    ds_ = sp.dsolve(sp.Eq(X(t).diff(t, 2) + b * X(t).diff(t) + c * X(t), forcing), X(t), ics={X(0): x0, X(t).diff(t).subs(t, 0): v0})
    sol_ = ds_.rhs
    chk(f'second order {b},{c}: substitution', sp.simplify(sol_.diff(t, 2) + b * sol_.diff(t) + c * sol_ - forcing) == 0)
    return sol_


def roots_of(p_):
    return sorted((complex(sp.N(tex2sym(a))) for a in p_['widget']['answers']), key=lambda z: z.imag)


def same_roots(a, b):
    return all(abs(u - v) < 1e-12 for u, v in zip(sorted(a, key=lambda z: (z.real, z.imag)), sorted(b, key=lambda z: (z.real, z.imag))))


# ---- p-hedge-overshoot: x'' + 4x' + 29x = 58, x(0) = x'(0) = 0
xs = second_order(4, 29, 58, 0, 0)
p = part(2, 'p-hedge-overshoot', 1)
chk('hedge 1: roots', same_roots(roots_of(p), np.roots([1, 4, 29])))
chk('hedge 1: discriminant -100', 16 - 4 * 29 == -100)
chk('hedge 1: the course spells it under-damped', 'underdamped' not in texts(p))
w = wrongs(p)
chk('hedge 1: slips', '2+5i, 2-5i' == w['sign']['tex'] and '-4+10i, -4-10i' == w['no-half']['tex'])
p = part(2, 'p-hedge-overshoot', 2)
chk('hedge 2: x_p', p['widget']['answer'] == 58 / 29 == 2 and wrongs(p)['no-divide']['value'] == 58)
chk('hedge 2: limit of the solution', sp.limit(xs, t, sp.oo) == 2)
p = part(2, 'p-hedge-overshoot', 3)
c1, c2 = sp.symbols('c1 c2')
form = 2 + sp.exp(-2 * t) * (c1 * sp.cos(5 * t) + c2 * sp.sin(5 * t))
cs = sp.solve([form.subs(t, 0), form.diff(t).subs(t, 0)], [c1, c2])
chk('hedge 3: c1 = -2, c2 = -0.8', cs[c1] == -2 and cs[c2] == sp.Rational(-4, 5) and close(p['widget']['answer'], -0.8))
chk('hedge 3: the form with these constants is the dsolve solution', sp.simplify(form.subs(cs) - xs) == 0)
w = wrongs(p)
chk('hedge 3: slip no-decay (5c2 = 0)', w['no-decay']['value'] == 0)
chk('hedge 3: slip sign (c1 = +2)', close(w['sign']['value'], sp.solve((-2 * 2 + 5 * c2), c2)[0]))
p = part(2, 'p-hedge-overshoot', 4)
chk("hedge 4: x' = 11.6e^{-2t} sin 5t", sp.simplify(xs.diff(t) - sp.Rational(58, 5) * sp.exp(-2 * t) * sp.sin(5 * t)) == 0)
hn = ivp(lambda tt, u: [u[1], 58 - 4 * u[1] - 29 * u[0]], [0.0, 0.0], 3)
tpk = brentq(lambda tt: hn.sol(tt)[1], 0.3, 0.9)
chk('hedge 4: first peak of the solve_ivp path', close(tpk, math.pi / 5, 1e-7) and close(p['widget']['answer'], math.pi / 5, 5e-7))
grid = np.linspace(0, 3, 30001)
chk('hedge 4: it is the highest point of the path', close(grid[np.argmax(hn.sol(grid)[0])], math.pi / 5, 2e-4))
w = wrongs(p)
chk('hedge 4: slips', close(w['period']['value'], 2 * math.pi / 5, 5e-5) and close(w['omega0']['value'], math.pi / math.sqrt(29), 5e-5))
printed('hedge 4', p, f'{math.pi / 5:.4f}')
p = part(2, 'p-hedge-overshoot', 5)
xpk = hn.sol(math.pi / 5)[0]
over = (xpk - 2) / 2
chk('hedge 5: key', close(over, math.exp(-2 * math.pi / 5), 1e-8) and close(p['widget']['answer'], over, 5e-6))
zeta = 2 / math.sqrt(29)
chk('hedge 5: l9 overshoot rule', close(math.exp(-zeta * math.pi / math.sqrt(1 - zeta**2)), over, 1e-9))
w = wrongs(p)
chk('hedge 5: slip sign', close(w['sign']['value'], -over, 5e-6))
chk('hedge 5: slip period (first trough)', close(w['period']['value'], (hn.sol(2 * math.pi / 5)[0] - 2) / 2, 5e-6))
printed('hedge 5', p, f'{xpk:.4f}', f'{100 * over:.2f}', f'{over:.4f}')

# ---- p-cash-buffer: x'' + 4x' + 5x = 10 cos t, x(0) = x'(0) = 0
xs = second_order(4, 5, 10 * sp.cos(t), 0, 0)
p = part(2, 'p-cash-buffer', 1)
chk('buffer 1: roots', same_roots(roots_of(p), np.roots([1, 4, 5])))
p = part(2, 'p-cash-buffer', 2)
Aa, Bb = sp.symbols('Aa Bb')
xp = Aa * sp.cos(t) + Bb * sp.sin(t)
res_ = sp.expand(xp.diff(t, 2) + 4 * xp.diff(t) + 5 * xp - 10 * sp.cos(t))
ab = sp.solve([res_.coeff(sp.cos(t)), res_.coeff(sp.sin(t))], [Aa, Bb])
chk('buffer 2: A = B = 1.25', ab[Aa] == sp.Rational(5, 4) == ab[Bb] and p['widget']['answer'] == 1.25)
chk('buffer 2: cos and sin rows', sp.expand(res_.coeff(sp.cos(t)) - (4 * Aa + 4 * Bb - 10)) == 0 and sp.expand(res_.coeff(sp.sin(t)) - (4 * Bb - 4 * Aa)) == 0)
res0 = sp.expand(xp.diff(t, 2) + 5 * xp - 10 * sp.cos(t))
ab0 = sp.solve([res0.coeff(sp.cos(t)), res0.coeff(sp.sin(t))], [Aa, Bb])
w = wrongs(p)
chk('buffer 2: slip no-damping', ab0[Bb] == 0 == w['no-damping']['value'] and ab0[Aa] == sp.Rational(5, 2))
chk('buffer 2: slip sign', w['sign']['value'] == -1.25)
p = part(2, 'p-cash-buffer', 3)
form = sp.exp(-2 * t) * (c1 * sp.cos(t) + c2 * sp.sin(t)) + sp.Rational(5, 4) * (sp.cos(t) + sp.sin(t))
cs = sp.solve([form.subs(t, 0), form.diff(t).subs(t, 0)], [c1, c2])
chk('buffer 3: c1 = -1.25, c2 = -3.75', cs[c1] == sp.Rational(-5, 4) and cs[c2] == sp.Rational(-15, 4) and p['widget']['answer'] == -3.75)
chk('buffer 3: the form is the dsolve solution', sp.simplify(form.subs(cs) - xs) == 0)
w = wrongs(p)
chk('buffer 3: slip no-decay (c2 + 1.25 = 0)', w['no-decay']['value'] == -1.25)
chk('buffer 3: slip sign (c1 = +1.25)', close(w['sign']['value'], sp.solve(-2 * sp.Rational(5, 4) + c2 + sp.Rational(5, 4), c2)[0]))
chk('buffer 3: slip drop-sign', w['drop-sign']['value'] == 3.75)
p = part(2, 'p-cash-buffer', 4)
bn = ivp(lambda tt, u: [u[1], 10 * math.cos(tt) - 4 * u[1] - 5 * u[0]], [0.0, 0.0], 3)
xhalf = float(xs.subs(t, sp.pi / 2))
chk('buffer 4: key', close(p['widget']['answer'], xhalf, 5e-7) and close(bn.sol(math.pi / 2)[0], xhalf, 1e-8))
w = wrongs(p)
chk('buffer 4: slips', close(w['no-decay']['value'], 1.25 - 1.25 * math.exp(-math.pi), 5e-4) and w['steady']['value'] == 1.25
    and close(w['sign']['value'], 1.25 + 1.25 * math.exp(-math.pi), 5e-4))
printed('buffer 4', p, f'{xhalf:.3f}', f'{3.75 * math.exp(-math.pi):.4f}', f'{math.exp(-math.pi):.5f}', f'{1.25 * math.sqrt(2):.2f}')

# ---- p-tracking-gap: x'' + bx' + 25x = 0, x(0) = 2, x'(0) = -4
p = part(2, 'p-tracking-gap', 1)
bb = sp.symbols('b', positive=True)
chk('gap 1: critical b', sp.solve(bb**2 - 100, bb) == [10] and p['widget']['answer'] == 10)
w = wrongs(p)
chk('gap 1: slips', w['omega0']['value'] == 5 and w['no-root']['value'] == 100)
for bv, osc in ((9.0, True), (10.0, False), (11.0, False)):
    chk(f'gap 1: b = {bv} oscillates: {osc}', (abs(np.roots([1, bv, 25])[0].imag) > 1e-6) == osc)
# "any more is slower": the slowest mode of b = 11 decays more slowly than e^{-5t}
chk('gap 1: more damping is slower', max(np.roots([1, 11, 25]).real) > -5)
p = part(2, 'p-tracking-gap', 2)
chk('gap 2: repeated root', sp.roots(sp.symbols('q')**2 + 10 * sp.symbols('q') + 25) == {-5: 2} and p['widget']['answer'] == -5)
w = wrongs(p)
chk('gap 2: slips', w['sign']['value'] == 5 and w['no-half']['value'] == -10)
xs = second_order(10, 25, 0, 2, -4)
p = part(2, 'p-tracking-gap', 3)
chk('gap 3: solution is (2 + 6t)e^{-5t}', sp.simplify(xs - (2 + 6 * t) * sp.exp(-5 * t)) == 0 and p['widget']['answer'] == 6)
w = wrongs(p)
chk('gap 3: slips', w['no-r']['value'] == -4 and w['sign']['value'] == -4 - 10)
p = part(2, 'p-tracking-gap', 4)
gn = ivp(lambda tt, u: [u[1], -10 * u[1] - 25 * u[0]], [2.0, -4.0], 4)
chk('gap 4: key', close(p['widget']['answer'], 5 * math.exp(-2.5), 5e-7) and close(gn.sol(0.5)[0], 5 * math.exp(-2.5), 1e-9))
w = wrongs(p)
chk('gap 4: slips', w['no-r']['value'] == 0 and close(w['sign']['value'], (2 - 14 * 0.5) * math.exp(-2.5), 5e-7)
    and close(w['no-t']['value'], 2 * math.exp(-2.5), 5e-5))
printed('gap 4', p, f'{5 * math.exp(-2.5):.4f}', f'{math.exp(-2.5):.6f}')
chk('gap 4: this path never crosses zero', min(gn.sol(np.linspace(0, 4, 4001))[0]) > 0)
# CLAIM (finding): "as critical damping promises". A critically damped path can cross zero once.
steep = ivp(lambda tt, u: [u[1], -10 * u[1] - 25 * u[0]], [2.0, -12.0], 4)
crosses = min(steep.sol(np.linspace(0, 4, 4001))[0]) < 0
print('CLAIM gap 4: with x(0) = 2, x\'(0) = -12 the critically damped gap crosses zero:', crosses,
      '(c2 = x\'(0) + 10 < 0); "as critical damping promises" is too strong')
chk('gap 4: explain does not say critical damping promises no crossing', not (crosses and 'as critical damping promises' in p['explain']['text']))

# ================================================================================================= LEVEL 3
# ---- p-yield-gaps
A = sp.Matrix([[-7, 2], [-6, 1]])
it = item(3, 'p-yield-gaps')
chk('yield: prose matrix', r'\begin{pmatrix}-7&2\\-6&1\end{pmatrix}' in it['prose'] and '(4, 2)' in it['prose'])
p = part(3, 'p-yield-gaps', 1)
chk('yield 1: det and trace', A.det() == 5 == p['widget']['answer'] and A.trace() == -6)
chk('yield 1: slip bc-sign', wrongs(p)['bc-sign']['value'] == (-7) * 1 + 2 * (-6))
p = part(3, 'p-yield-gaps', 2)
chk('yield 2: eigenvalues', A.eigenvals() == {-1: 1, -5: 1} and sorted(p['widget']['answers']) == [-5, -1])
chk('yield 2: numpy', np.allclose(sorted(np.linalg.eigvals(np.array(A, dtype=float)).real), [-5, -1]))
p = part(3, 'p-yield-gaps', 3)
chk('yield 3: class from trace and determinant', classify(-6, 5) == 'stable node' == classify_eig(A.tolist()) and correct_option(p) == 'stable-node')
printed('yield 3', p, r'\tau^2 - 4\Delta = 16')
chk('yield 3: 36 - 20 = 16', (-6)**2 - 4 * 5 == 16)
p = part(3, 'p-yield-gaps', 4)
chk('yield 4: eigenvectors', A * sp.Matrix([1, 3]) == -sp.Matrix([1, 3]) and A * sp.Matrix([1, 1]) == -5 * sp.Matrix([1, 1]))
cs = sp.Matrix([[1, 1], [3, 1]]).solve(sp.Matrix([4, 2]))
chk('yield 4: c1 = -1, c2 = 5', list(cs) == [-1, 5] and p['widget']['answer'] == -1)
w = wrongs(p)
chk('yield 4: slips', w['identity']['value'] == 4 and w['swapped']['value'] == 5 and w['drop-sign']['value'] == 1)
p = part(3, 'p-yield-gaps', 5)
xt = sp.exp(A * t) * sp.Matrix([4, 2])
mine = -sp.exp(-t) * sp.Matrix([1, 3]) + 5 * sp.exp(-5 * t) * sp.Matrix([1, 1])
chk('yield 5: matrix exponential is the stated solution', sp.simplify(xt - mine) == sp.zeros(2, 1))
chk('yield 5: limit of y/x', sp.limit(mine[1] / mine[0], t, sp.oo) == 3 == p['widget']['answer'])
yn = ivp(lambda tt, u: [-7 * u[0] + 2 * u[1], -6 * u[0] + u[1]], [4.0, 2.0], 6)
chk('yield 5: solve_ivp ratio at t = 6', close(yn.sol(6)[1] / yn.sol(6)[0], 3, 1e-6))
w = wrongs(p)
chk('yield 5: slips', w['fast']['value'] == 1 and close(w['inverted']['value'], 1 / 3, 1e-6) and w['start']['value'] == 2 / 4)

# ---- p-liquidity-arbitrage
F = sp.Matrix([x * (6 - x - y), y * (x - 2)])
it = item(3, 'p-liquidity-arbitrage')
chk('liq: prose equations', "$x' = x(6 - x - y)$ and $y' = y(x - 2)$" in it['prose'])
eqs = sp.solve(list(F), [x, y], dict=True)
pos = [(e[x], e[y]) for e in eqs if e[x] > 0 and e[y] > 0]
p = part(3, 'p-liquidity-arbitrage', 1)
chk('liq 1: positive equilibrium', pos == [(2, 4)] and p['widget']['answer'] == '(2,4)')
chk('liq 1: (6, 0) is an equilibrium', {x: 6, y: 0} in eqs)
p = part(3, 'p-liquidity-arbitrage', 2)
J = F.jacobian([x, y])
chk('liq 2: general Jacobian', J == sp.Matrix([[6 - 2 * x - y, -x], [y, x - 2]]))
J0 = J.subs({x: 2, y: 4})
chk('liq 2: key', sp.Matrix(matrix_of(p['widget']['answer'])) == J0 == sp.Matrix(matrix_of(p['widget']['accept'][0])), str(J0))
w = {wr['id']: sp.Matrix(matrix_of(wr['tex'])) for wr in p['widget']['wrong']}
chk('liq 2: slips', w['no-product'] == sp.Matrix([[6 - 2 - 4, -2], [4, 0]]) and w['transpose'] == J0.T and w['transpose'] != J0)
h = 1e-6
fn = lambda u: np.array([u[0] * (6 - u[0] - u[1]), u[1] * (u[0] - 2)])
Jfd = np.column_stack([(fn(np.array([2.0, 4.0]) + h * e) - fn(np.array([2.0, 4.0]) - h * e)) / (2 * h) for e in np.eye(2)])
chk('liq 2: central differences', np.allclose(Jfd, np.array(J0, dtype=float), atol=1e-6))
p = part(3, 'p-liquidity-arbitrage', 3)
tau, delta = J0.trace(), J0.det()
chk('liq 3: tau, delta, discriminant', (tau, delta) == (-2, 8) and tau**2 - 4 * delta == -28 == p['widget']['answer'])
w = wrongs(p)
chk('liq 3: slips', w['delta-sign']['value'] == 4 + 32 and w['no-four']['value'] == 4 - 8 and w['drop-sign']['value'] == 28)
p = part(3, 'p-liquidity-arbitrage', 4)
chk('liq 4: class', classify(-2, 8) == 'stable spiral' == classify_eig(J0.tolist()) and correct_option(p) == 'stable-spiral')
p = part(3, 'p-liquidity-arbitrage', 5)
ev = list(J0.eigenvals())
chk('liq 5: eigenvalues -1 +- i sqrt 7', set(ev) == {-1 + sp.sqrt(7) * sp.I, -1 - sp.sqrt(7) * sp.I})
turn = 2 * math.pi / math.sqrt(7)
chk('liq 5: key', close(p['widget']['answer'], turn, 5e-7))
# the nonlinear system, started close to (2, 4): time between successive upward crossings of x = 2
ln = ivp(lambda tt, u: list(fn(u)), [2.001, 4.0], 12)
g = np.linspace(0.05, 12, 240001)
dx = ln.sol(g)[0] - 2
ups = [brentq(lambda tt: ln.sol(tt)[0] - 2, g[i], g[i + 1]) for i in range(len(g) - 1) if dx[i] < 0 <= dx[i + 1]]
chk('liq 5: turn time of the nonlinear path near (2, 4)', len(ups) >= 3 and close(ups[1] - ups[0], turn, 2e-3), str(np.diff(ups)))
chk('liq 4: the nonlinear path spirals in', np.hypot(*(ln.sol(12) - np.array([2, 4]))) < 1e-6)
far = ivp(lambda tt, u: list(fn(u)), [5.0, 1.0], 40)
chk('liq 4: a far start also ends at (2, 4)', np.allclose(far.sol(40), [2, 4], atol=1e-6))
w = wrongs(p)
chk('liq 5: slips', close(w['centre']['value'], 2 * math.pi / math.sqrt(8), 5e-4) and close(w['no-half']['value'], 2 * math.pi / math.sqrt(28), 5e-4))
printed('liq 5', p, f'{turn:.3f}', f'{math.sqrt(7):.4f}')

# ---- p-trend-signal: s'' + 4s' - 5s = 0, s(0) = 1
p = part(3, 'p-trend-signal', 1)
A = sp.Matrix(matrix_of(p['widget']['answer']))
chk('trend 1: companion matrix', A == sp.Matrix([[0, 1], [5, -4]]) == sp.Matrix(matrix_of(p['widget']['accept'][0])))
chk('trend 1: characteristic polynomial is that of the equation', sp.expand(A.charpoly(s).as_expr() - (s**2 + 4 * s - 5)) == 0)
w = {wr['id']: sp.Matrix(matrix_of(wr['tex'])) for wr in p['widget']['wrong']}
chk('trend 1: slips', w['signs'] == sp.Matrix([[0, 1], [-5, 4]]) and w['swapped'] == sp.Matrix([[0, 1], [-4, 5]]))
p = part(3, 'p-trend-signal', 2)
chk('trend 2: det', A.det() == -5 == p['widget']['answer'] and A.trace() == -4)
w = wrongs(p)
chk('trend 2: slips', w['sign']['value'] == 5 and w['trace']['value'] == -4)
chk('trend 2: saddle', classify(-4, -5) == 'saddle' == classify_eig(A.tolist()))
p = part(3, 'p-trend-signal', 3)
chk('trend 3: eigenvalues', A.eigenvals() == {1: 1, -5: 1} and sorted(p['widget']['answers']) == [-5, 1])
p = part(3, 'p-trend-signal', 4)
Sg = sp.Function('Sg')
v = sp.symbols('v')
ssol = sp.dsolve(sp.Eq(Sg(t).diff(t, 2) + 4 * Sg(t).diff(t) - 5 * Sg(t), 0), Sg(t), ics={Sg(0): 1, Sg(t).diff(t).subs(t, 0): v}).rhs
chk('trend 4: substitution', sp.simplify(ssol.diff(t, 2) + 4 * ssol.diff(t) - 5 * ssol) == 0)
grow = sp.expand(ssol).coeff(sp.exp(t))
chk("trend 4: growing mode vanishes only at s'(0) = -5", sp.solve(grow, v) == [-5] and p['widget']['answer'] == -5)
chk('trend 4: then s = e^{-5t}', sp.simplify(ssol.subs(v, -5) - sp.exp(-5 * t)) == 0)
chk('trend 4: eigenvector (1, -5)', A * sp.Matrix([1, -5]) == -5 * sp.Matrix([1, -5]))
tn = ivp(lambda tt, u: [u[1], 5 * u[0] - 4 * u[1]], [1.0, -5.0], 2)
chk('trend 4: solve_ivp from slope -5 decays', close(tn.sol(1)[0], math.exp(-5), 1e-7))
for slope in (-4.9, 1.0, 5.0):
    tn = ivp(lambda tt, u: [u[1], 5 * u[0] - 4 * u[1]], [1.0, slope], 12)
    chk(f'trend 4: slope {slope} blows up', abs(tn.sol(12)[0]) > 100)
w = wrongs(p)
chk('trend 4: slips', w['unstable']['value'] == 1 and w['sign']['value'] == 5)

print(f'{count - fails} of {count} checks passed')
sys.exit(1 if fails else 0)
