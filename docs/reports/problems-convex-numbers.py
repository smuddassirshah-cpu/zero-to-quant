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


# ---------------------------------------------------------------- level 2
def vertices(A, bvec):
    """Every vertex of {z : A z <= b} in two variables, by enumerating pairs of rows (method 2 for small LPs)."""
    out = []
    for i, j in itertools.combinations(range(len(A)), 2):
        M = sp.Matrix([A[i], A[j]])
        if M.det() == 0:
            continue
        z = M.solve(sp.Matrix([bvec[i], bvec[j]]))
        if all(sum(A[k][q] * z[q] for q in range(2)) <= bvec[k] for k in range(len(A))):
            out.append((z[0], z[1]))
    return sorted(set(out))


def level2():
    lv = Level('convex', 2)
    # p-parking-cash
    d_, b_, n_ = sp.symbols('d b n')
    income = sp.expand((40 * d_ + 46 * b_ + 50 * n_).subs(d_, 20 - b_ - n_))
    expr(2, 'p-parking-cash', 1, income.subs({b_: b, n_: n}), {'no-800': 6 * b + 10 * n, 'no-subtract': 800 + 46 * b + 50 * n})
    ok(sp.expand(20 - b_ - n_ - 6) == 14 - b_ - n_, 'd >= 6 is b + n <= 14')
    A = [[1, 1], [F(1, 2), 1], [-1, 0], [0, -1]]
    bv = [14, 8, 0, 0]
    V = vertices(A, bv)
    ok(V == sorted([(0, 0), (14, 0), (12, 2), (0, 8)]), f'cash corners {V}')
    vals = {vt: 6 * vt[0] + 10 * vt[1] for vt in V}
    best = max(vals, key=vals.get)
    ok(sorted(vals.values()) == [0, 80, 84, 92], f'corner gains {sorted(vals.values())}')
    full = linprog([-40, -46, -50], A_ub=[[-1, 0, 0], [0, 0.5, 1]], b_ub=[-6, 8], A_eq=[[1, 1, 1]], b_eq=[20], method='highs')
    num(2, 'p-parking-cash', 2, best[0], full.x[1], {'notes': best[1], 'all-bills': 14})
    r2 = linprog([-6, -10], A_ub=[[1, 1], [0.5, 1]], b_ub=[14, 8], method='highs')
    num(2, 'p-parking-cash', 3, -vals[best], r2.fun, {'sign': vals[best], 'with-800': -(800 + vals[best]), 'income': 800 + vals[best]})
    ok(abs(-full.fun - 892) < 1e-9, 'income 892 from the three-variable LP')
    # part 4: floor n >= 5
    A5 = A + [[0, -1]]
    b5 = bv + [-5]
    V5 = vertices(A5, b5)
    ok(V5 == sorted([(0, 5), (6, 5), (0, 8)]), f'floor-5 corners {V5}')
    g5 = {vt: 6 * vt[0] + 10 * vt[1] for vt in V5}
    ok(sorted(g5.values()) == [50, 80, 86], f'floor-5 gains {sorted(g5.values())}')
    r4 = linprog([-40, -46, -50], A_ub=[[-1, 0, 0], [0, 0.5, 1], [0, 0, -1]], b_ub=[-6, 8, -5], A_eq=[[1, 1, 1]], b_eq=[20], method='highs')
    num(2, 'p-parking-cash', 4, 800 + max(g5.values()), -r4.fun,
        {'old-plan': 892, 'notes-corner': 800 + g5[(0, 8)], 'no-800': max(g5.values())})
    ok(np.allclose(r4.x[1:], [6, 5]), 'floor-5 plan (6, 5)')
    lv.expect('problems', 'items[0].parts[3].explain.text', 6)
    # part 5: largest feasible notes floor, exact by the maturity row, then a linprog scan of statuses
    nmax = max(vt[1] for vt in V)
    last_ok = None
    for fl in np.arange(0, 20.001, 0.25):
        r = linprog([-6, -10], A_ub=[[1, 1], [0.5, 1], [0, -1]], b_ub=[14, 8, -fl], method='highs')
        if r.status == 0:
            last_ok = fl
        else:
            ok(r.status == 2, f'floor {fl} infeasible gives status 2')
    num(2, 'p-parking-cash', 5, nmax, last_ok, {'overnight-only': 14, 'whole-pot': 20, 'current': 5})
    lv.expect('problems', 'items[0].parts[4].explain.text', 880)
    # p-whole-blocks
    Ab = [[3, 2], [1, 2], [-1, 0], [0, -1]]
    bb_ = [12, 7, 0, 0]
    VB = vertices(Ab, bb_)
    ok(VB == sorted([(0, 0), (4, 0), (F(5, 2), F(9, 4)), (0, F(7, 2))]), f'block corners {VB}')
    carry = {vt: 7 * vt[0] + 5 * vt[1] for vt in VB}
    lpb = linprog([-7, -5], A_ub=[[3, 2], [1, 2]], b_ub=[12, 7], method='highs')
    num(2, 'p-whole-blocks', 1, max(carry.values()), -lpb.fun, {'capital-corner': carry[(4, 0)], 'risk-corner': carry[(0, sp.Rational(7, 2))]}, rounded=28.75)
    ok(np.allclose(lpb.x, [2.5, 2.25]), 'fractional corner (2.5, 2.25)')
    lv.expect('problems', 'items[1].parts[0].explain.text', 11.25)
    whole = [(i, j) for i in range(10) for j in range(10) if 3 * i + 2 * j <= 12 and i + 2 * j <= 7]
    num(2, 'p-whole-blocks', 2, 7 * 2 + 5 * 2, 7 * int(2.5) + 5 * int(2.25), {'nearest': 7 * 3 + 5 * 2, 'capital-plan': carry[(4, 0)]})
    ok(3 * 3 + 2 * 2 == 13 and (3, 2) not in whole and (2, 2) in whole, 'nearest rounding breaks capital, rounding down is feasible')
    ok(3 * 2 + 2 * 2 == 10 and 2 + 4 == 6, 'rounded plan uses 10 and 6')
    best_w = max(7 * i + 5 * j for i, j in whole)
    num(2, 'p-whole-blocks', 3, int(np.floor(-lpb.fun + 1e-12)), best_w, {'no-floor': 28.75, 'rounded-plan': 24})
    ok(abs(29 - 28.75) <= 0.5, 'no-floor band also routes a rounded-up 29')
    arg = [p for p in whole if 7 * p[0] + 5 * p[1] == best_w]
    ok(arg == [(4, 0)], f'best whole plan {arg}')
    num(2, 'p-whole-blocks', 4, arg[0][0], 4, {'rounded': 2, 'near-corner': 3})
    ok(7 * 3 + 5 == 26 and (2, 3) not in whole and 2 + 6 > 7, '(3, 1) earns 26 and (2, 3) breaks risk')
    ok(best_w - 24 == 4, 'rounding gave away 4')
    # p-three-strategies
    Am = [[3, 1, 2], [2, 3, 1]]
    cm = [6, 7, 4]
    uu, vv = sp.symbols('u v')
    cols = [Am[0][j] * uu + Am[1][j] * vv for j in range(3)]
    expr(2, 'p-three-strategies', 1, cols[1].subs({uu: u, vv: v}), {'momentum': cols[0].subs({uu: u, vv: v}), 'swapped': 3 * u + v})
    Ad = [[-Am[0][j], -Am[1][j]] for j in range(3)] + [[-1, 0], [0, -1]]
    bd = [-cm[j] for j in range(3)] + [0, 0]
    DV = vertices(Ad, bd)
    ok(DV == sorted([(0, 4), (1, 2), (7, 0)]), f'dual corners {DV}')
    dual = linprog([10, 10], A_ub=np.array(Ad[:3], dtype=float), b_ub=np.array(bd[:3], dtype=float), method='highs')
    unchecked = sp.solve([cols[0] - 6, cols[1] - 7], [uu, vv])
    num(2, 'p-three-strategies', 2, min(10 * p + 10 * q for p, q in DV), dual.fun,
        {'corner-04': 40, 'corner-70': 70, 'unchecked': 10 * unchecked[uu] + 10 * unchecked[vv]})
    ok(unchecked == {uu: F(4, 7), vv: F(15, 7)} and 2 * unchecked[uu] + unchecked[vv] == F(23, 7), 'unchecked corner breaks value row')
    ok([c.subs({uu: 1, vv: 2}) for c in cols] == [7, 7, 4], 'priced columns at (1, 2)')
    choice(2, 'p-three-strategies', 3, 'momentum')
    primal = linprog([-6, -7, -4], A_ub=Am, b_ub=[10, 10], method='highs')
    x2, x3 = sp.symbols('x2 x3')
    ps = sp.solve([x2 + 2 * x3 - 10, 3 * x2 + x3 - 10], [x2, x3])
    num(2, 'p-three-strategies', 4, ps[x2], primal.x[1], {'value': ps[x3], 'var-only': F(10, 3)})
    ok(7 * ps[x2] + 4 * ps[x3] == 30 and abs(-primal.fun - 30) < 1e-9 and abs(primal.x[0]) < 1e-9, 'primal 30 with x1 = 0')
    enter = None
    for c1 in np.arange(6, 9.001, 0.01):
        r = linprog([-c1, -7, -4], A_ub=Am, b_ub=[10, 10], method='highs')
        if r.x[0] > 1e-7 and -r.fun > 30 + 1e-9:
            enter = c1
            break
    num(2, 'p-three-strategies', 5, cols[0].subs({uu: 1, vv: 2}), enter, {'current': 6, 'margin-only': 3, 'gap': 1}, agree=0.011)
    lv.expect('problems', 'items[0].parts[1].feedback.correct', 84)
    lv.expect('problems', 'items[0].parts[1].feedback.correct', 80)
    lv.expect('problems', 'items[2].parts[1].explain.text', -2)
    shape(2, {'p-parking-cash': {'l5-linear-programmes', 'l6-corners', 'l7-lp-in-code'},
              'p-whole-blocks': {'l5-linear-programmes', 'l6-corners'},
              'p-three-strategies': {'l5-linear-programmes', 'l6-corners', 'l8-lp-duality'}},
          ['cv-lp', 'cv-duality'])
    lv.check_wrongs('problems')
    return lv


# ---------------------------------------------------------------- level 3
def level3():
    lv = Level('convex', 3)
    # p-capital-price: exact with sympy, then scipy on the primal and a grid on the dual
    x1s, x2s, L = sp.symbols('x1 x2 L', real=True)
    lm = sp.Symbol('lambda')
    P1 = 10 * x1s - x1s ** 2
    P2 = 8 * x2s - x2s ** 2 / 2
    r1 = sp.solve(sp.diff(P1 - lm * x1s, x1s), x1s)[0]
    r2 = sp.solve(sp.diff(P2 - lm * x2s, x2s), x2s)[0]
    expr(3, 'p-capital-price', 1, r1, {'no-half': 10 - lm, 'sign': 5 + lm / 2})
    ok(sp.simplify(r2 - (8 - lm)) == 0, 'credit desk picks 8 - lambda')
    g = sp.simplify((P1 + P2).subs({x1s: r1, x2s: r2}) - lm * (r1 + r2 - 6))
    g3 = g.subs(lm, 3)
    brute3 = max(10 * a - a * a + 8 * c - c * c / 2 - 3 * (a + c - 6) for a in np.linspace(0, 10, 2001) for c in np.linspace(0, 10, 2001)[::4])
    ask3 = (P1 + P2).subs({x1s: r1.subs(lm, 3), x2s: r2.subs(lm, 3)})
    num(3, 'p-capital-price', 2, g3, brute3, {'no-rent': g3 - 18, 'ask-profit': ask3}, rounded=42.75, agree=1e-4)
    ok(r1.subs(lm, 3) == F(7, 2) and r2.subs(lm, 3) == 5 and P1.subs(x1s, F(7, 2)) == F(91, 4) and P2.subs(x2s, 5) == F(55, 2), 'asks 3.5 and 5 earn 22.75 and 27.5')
    ok(ask3 == F(201, 4) and 3 * (F(17, 2) - 6) == F(15, 2), 'ask profit 50.25 and excess charge 7.5')
    lstar = sp.solve(sp.diff(g, lm), lm)[0]
    dual_num = minimize_scalar(lambda q: float(g.subs(lm, q)), bounds=(0, 10), method='bounded', options={'xatol': 1e-10})
    ok(sp.simplify(sp.diff(g, lm) - (6 - r1 - r2)) == 0, "g'(lambda) = 6 - x1 - x2")
    slip = sp.solve((10 - lm) + (8 - lm) - 6, lm)[0]
    num(3, 'p-capital-price', 3, lstar, dual_num.x, {'no-half': slip, 'trial': 3}, rounded=4.67, agree=1e-6)
    xa, xb = r1.subs(lm, lstar), r2.subs(lm, lstar)
    ok((xa, xb) == (F(8, 3), F(10, 3)), 'split (8/3, 10/3)')
    pstar = (P1 + P2).subs({x1s: xa, x2s: xb})
    prim = minimize(lambda z: -(10 * z[0] - z[0] ** 2 + 8 * z[1] - z[1] ** 2 / 2), [1, 1], method='SLSQP',
                    constraints=[{'type': 'ineq', 'fun': lambda z: 6 - z[0] - z[1]}], bounds=[(0, None)] * 2, options={'ftol': 1e-14})
    num(3, 'p-capital-price', 4, pstar, -prim.fun, {'trial-cap': g3, 'no-limit': 57}, rounded=40.67, agree=1e-7)
    ok(pstar == g.subs(lm, lstar) == F(122, 3), 'zero gap at 122/3')
    ok(P1.subs(x1s, 5) + P2.subs(x2s, 8) == 57, 'price 0 asks earn 57')
    ok(10 * F(8, 3) == F(80, 3) and F(8, 3) ** 2 == F(64, 9) and 8 * F(10, 3) == F(80, 3) and F(10, 3) ** 2 / 2 == F(50, 9), 'terms 80/3, 64/9, 80/3, 50/9')
    est = pstar + F(3, 10) * lstar
    l63 = sp.solve(sp.Eq(r1 + r2, F(63, 10)), lm)[0]
    p63 = (P1 + P2).subs({x1s: r1.subs(lm, l63), x2s: r2.subs(lm, l63)})
    prim63 = minimize(lambda z: -(10 * z[0] - z[0] ** 2 + 8 * z[1] - z[1] ** 2 / 2), [1, 1], method='SLSQP',
                      constraints=[{'type': 'ineq', 'fun': lambda z: 6.3 - z[0] - z[1]}], bounds=[(0, None)] * 2, options={'ftol': 1e-14})
    ok(abs(float(p63) + prim63.fun) < 1e-7, f'exact profit at 6.3 {float(p63)}')
    num(3, 'p-capital-price', 5, est, float(pstar) + 0.3 * float(lstar), {'trial-price': pstar + F(3, 10) * 3, 'per-desk': pstar + 2 * F(3, 10) * lstar}, rounded=42.07)
    ok(abs(float(p63) - 42.04) < 0.005 and abs(float(l63) - 4.47) < 0.005, f'exact 42.04 at price 4.47: {float(p63)}, {float(l63)}')
    ok(abs(42.04 - 42.0666667) <= 0.035, 'the band also takes the exact re-solve 42.04')
    ok(F(3, 10) * lstar == F(7, 5), '0.3 x 14/3 = 1.4')
    # p-no-borrowing
    S = sp.Matrix([[F(3, 100), F(1, 100)], [F(1, 100), F(7, 100)]])
    m = sp.Matrix([F(55, 1000), F(105, 1000)])
    rf = F(3, 100)
    wfree = S.solve(m - rf * sp.ones(2, 1))
    wnp = np.linalg.solve(np.array(S, dtype=float), np.array(m - rf * sp.ones(2, 1), dtype=float).ravel())
    num(3, 'p-no-borrowing', 1, wfree[1], wnp[1], {'gave-a': wfree[0], 'no-cash-rate': S.solve(m)[1], 'no-cov': (m[1] - rf) / S[1, 1]}, rounded=1.00)
    ok(list(wfree) == [F(1, 2), 1] and 1 - sum(wfree) == F(-1, 2), 'free plan (0.5, 1) with cash -0.5')
    wa, wb, lam_ = sp.symbols('wa wb lam_')
    sol = sp.solve([m[0] - (S[0, 0] * wa + S[0, 1] * wb) - lam_, m[1] - (S[1, 0] * wa + S[1, 1] * wb) - lam_, wa + wb - 1], [wa, wb, lam_])
    Snp, mnp = np.array(S, dtype=float), np.array(m, dtype=float).ravel()
    qp = minimize(lambda z: -(mnp @ z[:2] + 0.03 * z[2] - 0.5 * z[:2] @ Snp @ z[:2]), [1 / 3] * 3, method='SLSQP', bounds=[(0, 1)] * 3,
                  constraints=[{'type': 'eq', 'fun': lambda z: z.sum() - 1}], options={'ftol': 1e-15, 'maxiter': 500})
    resc = F(1, 1) / (F(3, 2))
    num(3, 'p-no-borrowing', 2, sol[wb], qp.x[1], {'rescale': resc, 'gave-a': sol[wa]}, rounded=0.875, agree=1e-6)
    ok(abs(qp.x[2]) < 1e-7, 'solver puts cash at 0')
    third = sp.Matrix([F(1, 3), F(2, 3)])
    lam_third = m - S * third
    ok(lam_third[0] != lam_third[1], f'rescaled weights give two lambdas {list(lam_third)}')
    SwA = (S * sp.Matrix([sol[wa], sol[wb]]))[0]
    SwB = (S * sp.Matrix([sol[wa], sol[wb]]))[1]
    num(3, 'p-no-borrowing', 3, sol[lam_], float(m[1] - SwB), {'cash-rate': rf, 'sigma-w': SwA}, rounded=0.0425)
    ok(SwA == F(1, 80) and SwB == F(1, 16), '(Sigma w) = (0.0125, 0.0625)')
    ok((S[0, 0] - S[1, 0], S[0, 1] - S[1, 1], m[0] - m[1]) == (F(1, 50), F(-3, 50), F(-1, 20)), 'row difference 0.02 wA - 0.06 wB = -0.05')
    nu = sol[lam_] - rf
    # method 2 for nu: the objective gain per unit of allowed borrowing, by a finite difference of the QP value
    def qp_val(lo):
        r = minimize(lambda z: -(mnp @ z[:2] + 0.03 * z[2] - 0.5 * z[:2] @ Snp @ z[:2]), [0.1, 0.8, 0.1], method='SLSQP',
                     bounds=[(0, 2), (0, 2), (lo, 1)], constraints=[{'type': 'eq', 'fun': lambda z: z.sum() - 1}], options={'ftol': 1e-15, 'maxiter': 500})
        return -r.fun
    fd = (qp_val(-1e-4) - qp_val(0)) / 1e-4
    num(3, 'p-no-borrowing', 4, nu, fd, {'sign': -nu, 'lambda': sol[lam_]}, rounded=0.0125, agree=1e-3)
    ret = (m.T * sp.Matrix([sol[wa], sol[wb]]))[0] * 100
    num(3, 'p-no-borrowing', 5, ret, 100 * mnp @ qp.x[:2], {'levered': 100 * ((m.T * wfree)[0] + rf * (1 - sum(wfree))), 'equal': 100 * sum(m) / 2}, rounded=9.875, agree=1e-6)
    var = (sp.Matrix([sol[wa], sol[wb]]).T * S * sp.Matrix([sol[wa], sol[wb]]))[0]
    ok(var == F(9, 160) and abs(np.sqrt(float(var)) - 0.2372) < 5e-5, f'variance 0.05625, vol 23.72%: {float(var)}')
    ok(F(1, 8) * F(55, 10) == F(11, 16) and F(7, 8) * F(105, 10) == F(147, 16), '0.6875% and 9.1875%')
    lv.expect('problems', 'items[1].parts[4].explain.text', 0.05625)
    # p-variance-limit
    w = sp.Symbol('w')
    Vw = sp.expand(F(1, 100) * (1 - w) ** 2 + 2 * F(5, 1000) * w * (1 - w) + F(625, 10000) * w ** 2)
    Cv = np.array([[0.01, 0.005], [0.005, 0.0625]])
    ok(all(abs(float(Vw.subs(w, t)) - np.array([1 - t, t]) @ Cv @ np.array([1 - t, t])) < 1e-12 for t in (0.1, 0.4, 0.9)), 'V(w) matches the matrix form')
    pw = sp.Poly(Vw, w)
    ok(pw.all_coeffs() == [F(1, 16), F(-1, 100), F(1, 100)], 'V = 0.0625 w^2 - 0.01 w + 0.01')
    xw = sp.Symbol('x')
    def parse_w(t):
        return parse(t.replace('w', 'x')).subs(xw, w)
    pt = part(3, 'p-variance-limit', 1)
    wd = pt['widget']
    ok(sp.simplify(parse_w(wd['answer']) - Vw) == 0, 'L3 p-variance-limit p1 key equals truth')
    for a in wd['accept']:
        ok(sp.simplify(parse_w(a) - Vw) == 0, f'accept {a}')
    slips = {'no-cov': sp.expand(F(1, 100) * (1 - w) ** 2 + F(625, 10000) * w ** 2),
             'single-cov': sp.expand(F(1, 100) * (1 - w) ** 2 + F(5, 1000) * w * (1 - w) + F(625, 10000) * w ** 2)}
    for q in wd['wrong']:
        e = parse_w(q['tex'])
        ok(sp.simplify(e - slips[q['id']]) == 0 and sp.simplify(e - Vw) != 0, f'wrong {q["id"]} equals its slip')
        ok(q['id'] in pt['feedback']['byKey'], f'wrong {q["id"]} has byKey')
    ok(set(q['id'] for q in wd['wrong']) == set(slips), 'p1 wrong ids')
    roots = sorted(sp.solve(Vw - F(16, 1000), w))
    ok(roots == [F(-6, 25), F(2, 5)], f'roots {roots}')
    ok(sp.expand(F(1, 16) * (w - F(2, 5)) * (w + F(6, 25)) - (Vw - F(16, 1000))) == 0, 'factorised form')
    grid = np.linspace(0, 1, 1000001)
    feas = grid[(0.0625 * grid ** 2 - 0.01 * grid + 0.01) <= 0.016 + 1e-15]
    wmin = sp.solve(sp.diff(Vw, w), w)[0]
    num(3, 'p-variance-limit', 2, roots[1], feas.max(), {'other-root': roots[0], 'min-var': wmin, 'no-limit': 1}, agree=1e-5)
    ok(wmin == F(2, 25), 'minimum-variance share 0.08')
    ok(Vw.subs(w, 1) == F(1, 16), 'all equity variance 0.0625')
    dV = sp.diff(Vw, w).subs(w, F(2, 5))
    mu = F(6, 100) / dV
    # method 2: mu as the slope of the best return against the limit, by a central difference
    def best_R(cap):
        top = (0.01 + np.sqrt(0.0001 + 4 * 0.0625 * (cap - 0.01))) / (2 * 0.0625)
        return 0.04 + 0.06 * top
    slope = (best_R(0.016 + 1e-7) - best_R(0.016 - 1e-7)) / 2e-7
    num(3, 'p-variance-limit', 3, mu, slope, {'inverted': 1 / mu, 'half-derivative': F(6, 100) / (F(-1, 100) + F(625, 10000) * F(2, 5))}, rounded=1.5, agree=1e-5)
    ok(dV == F(1, 25) and 2 * F(625, 10000) * F(2, 5) == F(1, 20), "V'(0.4) = 0.05 - 0.01 = 0.04")
    ok(0.04 + 0.06 * 0.4 == 0.064, 'return 6.4% at the optimum')
    choice(3, 'p-variance-limit', 4, 'convex')
    ok(Vw.subs(w, 0) == F(1, 100) < F(16, 1000), 'Slater point w = 0')
    bp = float(mu * F(2, 10000) * 10000)
    exact_bp = (best_R(0.0162) - best_R(0.016)) * 10000
    num(3, 'p-variance-limit', 5, bp, round(exact_bp), {'inverted': round(float(F(2, 10000) / mu * 10000)), 'variance-step': 2}, agree=1e-9)
    ok(abs(exact_bp - 2.98) < 0.005, f'exact rise 2.98 bp: {exact_bp}')
    top = (0.01 + np.sqrt(0.0001 + 4 * 0.0625 * 0.0062)) / 0.125
    ok(abs(top - 0.405) < 0.0005, f'new share about 0.405: {top}')
    shape(3, {'p-capital-price': {'l9-lagrangian-dual', 'l10-kkt', 'l13-shadow-prices'},
              'p-no-borrowing': {'l10-kkt', 'l11-mean-variance-kkt', 'l12-long-only', 'l13-shadow-prices'},
              'p-variance-limit': {'l10-kkt', 'l11-mean-variance-kkt', 'l13-shadow-prices'}},
          ['cv-duality', 'cv-qp'])
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
