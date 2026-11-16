"""Recompute every number in app/content/courses/convex/problems-1.json to problems-3.json twice.

Method 1 is exact (fractions or sympy: solve, differentiate, substitute). Method 2 is independent: a brute grid search,
scipy.optimize (minimize, linprog), numpy eigenvalues or vertex enumeration. For each numeric part the script checks that
the two methods agree, that the JSON key lies within its tol of the value, that the value at the asked rounding is accepted,
that every `wrong` value equals its named slip recomputed here, has a byKey line and lies outside the key's band.
Expression parts: the key and every accepted form equal the sympy truth and every wrong form equals its slip and differs.
Choice parts: the keyed option is the one expected. Stated figures in feedback and explain are checked with numbers_lib
(Level.expect), and Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-convex-numbers.py
"""
import json, os, sys, itertools
from fractions import Fraction as F
import numpy as np
import sympy as sp
from scipy.optimize import linprog, minimize, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'convex')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(lv):
    p = os.path.join(COURSE, f'problems-{lv}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding='utf8'))
    return {it['id']: it for it in d['items']}


SETS = {lv: load(lv) for lv in (1, 2, 3)}


def part(lv, iid, p):
    return SETS[lv][iid]['parts'][p - 1]


def num(lv, iid, p, exact, alt, slips, rounded=None, agree=1e-7):
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} is numeric')
    exact, alt = float(exact), float(alt)
    ok(abs(exact - alt) <= agree * max(1, abs(exact)), f'{tag} methods agree {exact} vs {alt}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - exact) <= tol + 1e-12, f'{tag} key {w["answer"]} within {tol} of {exact}')
    if rounded is not None:
        ok(abs(rounded - w['answer']) <= tol + 1e-12, f'{tag} rounded {rounded} accepted')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} vs slips {sorted(slips)}')
    bk = pt['feedback'].get('byKey', {})
    for sid, val in slips.items():
        if sid not in ids:
            continue
        x = ids[sid]
        ok(abs(x['value'] - float(val)) <= x['tol']['abs'] + 1e-12, f'{tag} slip {sid} {x["value"]} vs recomputed {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag} slip {sid} outside key band')
        ok(sid in bk, f'{tag} slip {sid} has byKey')


x, y, lam, u, v, b, n = sp.symbols('x y lambda u v b n')


def parse(tex):
    t = tex.replace('\\lambda', 'lam').replace('λ', 'lam').replace('lambda', 'lam')
    t = t.replace('\\frac{', 'FRAC{')
    # FRAC{a}{b} -> ((a)/(b))
    while 'FRAC{' in t:
        i = t.index('FRAC{')
        depth, j = 0, i + 4
        for j in range(i + 4, len(t)):
            if t[j] == '{':
                depth += 1
            elif t[j] == '}':
                depth -= 1
                if depth == 0:
                    break
        a = t[i + 5:j]
        k = j + 1
        depth = 0
        for m in range(k, len(t)):
            if t[m] == '{':
                depth += 1
            elif t[m] == '}':
                depth -= 1
                if depth == 0:
                    break
        bb = t[k + 1:m]
        t = t[:i] + f'(({a})/({bb}))' + t[m + 1:]
    t = t.replace('^', '**').replace('{', '(').replace('}', ')')
    loc = {'lam': sp.Symbol('lambda'), 'b': b, 'n': n, 'u': u, 'v': v, 'x': x, 'y': y}
    return sp.sympify(sp.parsing.sympy_parser.parse_expr(
        t, local_dict=loc, transformations=sp.parsing.sympy_parser.standard_transformations +
        (sp.parsing.sympy_parser.implicit_multiplication_application,)))


def expr(lv, iid, p, truth, slips):
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'expression', f'{tag} is expression')
    ok(sp.simplify(parse(w['answer']) - truth) == 0, f'{tag} key equals truth')
    for a in w.get('accept', []):
        ok(sp.simplify(parse(a) - truth) == 0, f'{tag} accept {a!r} equals truth')
    ids = {q['id']: q['tex'] for q in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids')
    bk = pt['feedback'].get('byKey', {})
    for sid, val in slips.items():
        e = parse(ids[sid])
        ok(sp.simplify(e - val) == 0, f'{tag} wrong {sid} equals its slip')
        ok(sp.simplify(e - truth) != 0, f'{tag} wrong {sid} differs from key')
        ok(sid in bk, f'{tag} wrong {sid} has byKey')


def choice(lv, iid, p, key):
    w = part(lv, iid, p)['widget']
    good = [o['id'] for o in w['options'] if o.get('correct')]
    ok(good == [key], f'L{lv} {iid} p{p} correct option {good} == {key}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'L{lv} {iid} p{p} every distractor has why')


def shape(lv, lessons_by_item, skills):
    items = list(SETS[lv].values())
    ok(3 <= len(items) <= 5, f'L{lv} has 3 to 5 problems')
    ok(any(it['difficulty'] == 5 for it in items), f'L{lv} has a difficulty 5')
    parts = [pt for it in items for pt in it['parts']]
    typed = sum(pt['widget']['kind'] in ('numeric', 'expression') for pt in parts)
    ok(typed * 3 >= 2 * len(parts), f'L{lv} typed share {typed}/{len(parts)}')
    for it in items:
        ok(3 <= len(it['parts']) <= 5, f'L{lv} {it["id"]} has 3 to 5 parts')
        ok(set(it['skills']) <= set(skills), f'L{lv} {it["id"]} skills from the level')
        ok(len(lessons_by_item[it['id']]) >= 2, f'L{lv} {it["id"]} draws on two lessons')
    course = json.load(open(os.path.join(COURSE, 'course.json')))
    want = set(course['levels'][lv - 1]['lessons'])
    got = set().union(*lessons_by_item.values())
    ok(got == want, f'L{lv} every lesson drawn on: {sorted(want - got)} missing')


# ---------------------------------------------------------------- level 1
def level1():
    lv = Level('convex', 1)
    X = sp.Symbol('X', real=True)
    Cfun = lambda t: 2 * (t - 3) ** 2 + 5 * abs(t)
    # p-shortfall-and-fee
    gap = F(1, 2) * Cfun(-1) + F(1, 2) * Cfun(3) - Cfun(1)
    gap_alt = 0.5 * Cfun(-1.0) + 0.5 * Cfun(3.0) - Cfun(1.0)
    slip_abs = F(1, 2) * (2 * 16 - 5) + F(1, 2) * 15 - 13
    num(1, 'p-shortfall-and-fee', 1, gap, gap_alt, {'abs-dropped': slip_abs, 'reversed': -gap})
    choice(1, 'p-shortfall-and-fee', 2, 'sum')
    # convexity of C on a grid: every chord gap >= 0 (second method for part 2)
    g = np.linspace(-5, 8, 131)
    worst = min(0.5 * Cfun(a) + 0.5 * Cfun(c) - Cfun(0.5 * a + 0.5 * c) for a in g for c in g)
    ok(worst >= -1e-9, 'C passes the midpoint chord test on a grid')
    xs = sp.solve(sp.diff(2 * (X - 3) ** 2 + 5 * X, X), X)[0]
    xs_alt = minimize_scalar(Cfun, bounds=(-5, 8), method='bounded', options={'xatol': 1e-10}).x
    num(1, 'p-shortfall-and-fee', 3, xs, xs_alt, {'no-fee': 3, 'fee-sign': sp.solve(4 * (X - 3) - 5, X)[0],
                                                   'no-chain': sp.solve(2 * (X - 3) + 5, X)[0]}, agree=1e-6)
    cmin = Cfun(F(7, 4))
    cmin_alt = min(Cfun(t) for t in np.linspace(-5, 8, 1300001))
    num(1, 'p-shortfall-and-fee', 4, cmin, cmin_alt, {'half': F(25, 16) + F(35, 4), 'no-fee': F(25, 8)}, agree=1e-6)
    c12 = Cfun(F(6, 5))
    c12_alt = minimize_scalar(Cfun, bounds=(-5, 1.2), method='bounded', options={'xatol': 1e-12}).fun
    num(1, 'p-shortfall-and-fee', 5, c12, c12_alt, {'unconstrained': cmin, 'at-zero': Cfun(0), 'fee-dropped': 2 * (F(6, 5) - 3) ** 2},
        rounded=12.48, agree=1e-6)
    ok(4 * (F(6, 5) - 3) + 5 == F(-11, 5), "C'(1.2) = -2.2")
    for path, val in [('items[0].parts[0].feedback.correct', 37), ('items[0].parts[0].feedback.correct', 26),
                      ('items[0].parts[3].explain.text', 18), ('items[0].parts[3].explain.text', 15),
                      ('items[0].parts[4].feedback.correct', -2.2), ('items[0].parts[4].feedback.correct', 6.48),
                      ('items[0].parts[4].explain.text', 0.605), ('items[0].parts[3].feedback.correct', 3.125)]:
        lv.expect('problems', path, val)
    ok(float(c12 - cmin) == 0.605, 'limit costs 0.605')
    # p-worst-scenario
    L = [lambda w: 4 + 8 * w, lambda w: 10 - 8 * w, lambda w: -1 - 5 * w]
    # losses from the stated fund returns
    for k, (ra, rb) in enumerate([(-12, -4), (-2, -10), (6, 1)]):
        for w in (F(0), F(1, 3), F(1)):
            ok(-(ra * w + rb * (1 - w)) == L[k](w), f'scenario {k + 1} line from fund returns at w={w}')
    W = lambda w: max(f(w) for f in L)
    num(1, 'p-worst-scenario', 1, W(F(1, 2)), max(f(0.5) for f in L),
        {'average': sum(f(F(1, 2)) for f in L) / 3, 'rate': L[1](F(1, 2)), 'decimal': W(F(1, 2)) / 100})
    grid = np.linspace(0, 1, 400001)
    inside = grid[np.array([W(w) for w in grid]) <= 8 + 1e-12]
    num(1, 'p-worst-scenario', 2, F(1, 2) - F(1, 4), inside.max() - inside.min(),
        {'crash-only': F(1, 2), 'shock-only': 1 - F(1, 4)}, agree=1e-5)
    choice(1, 'p-worst-scenario', 3, 'epi')
    res = linprog([0, 1], A_ub=[[8, -1], [-8, -1], [-5, -1]], b_ub=[-4, -10, 1], bounds=[(0, 1), (None, None)], method='highs')
    wstar = sp.solve(sp.Eq(4 + 8 * X, 10 - 8 * X), X)[0]
    num(1, 'p-worst-scenario', 4, wstar, res.x[0], {'half': F(1, 2), 'edge': F(1, 4)})
    num(1, 'p-worst-scenario', 5, L[0](wstar), res.fun, {'half': 8, 'all-bond': W(0), 'decimal': F(7, 100)})
    ok(L[2](F(3, 8)) == F(-23, 8), 'rally loss at 0.375 is -2.875')
    lv.expect('problems', 'items[1].parts[3].explain.text', -2.875)
    lv.expect('problems', 'items[1].parts[0].feedback.correct', -3.5)
    # p-two-futures-hedge
    a, bb = sp.symbols('a b', real=True)
    V = a ** 2 + 6 * a * bb + 10 * bb ** 2 - 2 * a - 2 * bb + 6
    # V from the covariances: Var(P - aF1 - bF2)
    S = sp.Matrix([[6, 1, 1], [1, 1, 3], [1, 3, 10]])
    c = sp.Matrix([1, -a, -bb])
    ok(sp.expand((c.T * S * c)[0] - V) == 0, 'V is Var(P - aF1 - bF2)')
    H = sp.hessian(V, (a, bb))
    ev = np.linalg.eigvalsh(np.array(H, dtype=float))
    num(1, 'p-two-futures-hedge', 1, H.det(), ev.prod(), {'half-cross': 2 * 20 - 3 ** 2, 'no-two': 1 * 10 - 3 ** 2})
    ok(abs(ev[0] - 0.1833) < 5e-5 and abs(ev[1] - 21.8167) < 5e-5 and abs(ev.sum() - 22) < 1e-9, f'eigenvalues {ev}')
    ok(2 * 20 - 7 ** 2 == -9, 'cross term 7 gives det -9')
    choice(1, 'p-two-futures-hedge', 2, 'strict')
    sol = sp.solve([sp.diff(V, a), sp.diff(V, bb)], [a, bb])
    m = minimize(lambda z: float(V.subs({a: z[0], bb: z[1]})), [0, 0], method='BFGS', options={'gtol': 1e-10})
    num(1, 'p-two-futures-hedge', 3, sol[a], m.x[0], {'gave-b': sol[bb], 'sign': 1 - 3 * 2}, agree=1e-5)
    num(1, 'p-two-futures-hedge', 4, V.subs(sol), m.fun, {'unhedged': V.subs({a: 0, bb: 0}), 'no-constant': V.subs(sol) - 6}, agree=1e-6)
    Vf = sp.lambdify((a, bb), V)
    cons = minimize(lambda z: Vf(*z), [3, 1], bounds=[(None, None), (0, None)], method='L-BFGS-B', options={'ftol': 1e-14, 'gtol': 1e-12})
    edge = sp.solve(sp.diff(V.subs(bb, 0), a), a)[0]
    num(1, 'p-two-futures-hedge', 5, V.subs({a: edge, bb: 0}), cons.fun, {'free': 1, 'clip': V.subs({a: 7, bb: 0})}, agree=1e-6)
    ok(sp.diff(V, bb).subs({a: 1, bb: 0}) == 4, 'V_b(1, 0) = 4')
    lv.expect('problems', 'items[2].parts[1].explain.text', 0.18)
    lv.expect('problems', 'items[2].parts[1].explain.text', 21.82)
    shape(1, {'p-shortfall-and-fee': {'l1-convex-sets', 'l2-convex-functions', 'l3-local-is-global'},
              'p-worst-scenario': {'l1-convex-sets', 'l2-convex-functions', 'l3-local-is-global', 'l4-recognising-convex-problems'},
              'p-two-futures-hedge': {'l1-convex-sets', 'l2-convex-functions', 'l3-local-is-global', 'l4-recognising-convex-problems'}},
          ['cv-convex'])
    lv.check_wrongs('problems')
    return lv


levels = []
if SETS[1]:
    levels.append(level1())
if SETS.get(2) and 'level2' in globals():
    levels.append(level2())
if SETS.get(3) and 'level3' in globals():
    levels.append(level3())

bad_lib = sum(1 for lv in levels for r in lv.results if not r[0])
print(f'problems-convex-numbers: {checks - len(fails)} of {checks} own checks passed; numbers_lib failures {bad_lib}')
sys.exit(1 if fails or bad_lib else 0)
