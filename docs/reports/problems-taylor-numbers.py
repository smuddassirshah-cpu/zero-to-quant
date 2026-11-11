"""Recompute every number in app/content/courses/taylor/problems-<n>.json twice.

Method 1 is exact: sympy with rationals (closed forms, exact derivatives, exact sums).
Method 2 is independent: floating-point arithmetic by another route (numerical
derivatives by central differences, root finding by bisection, the true function
evaluated directly, term-by-term loops). For each numeric part the script checks that
the two methods agree, that the JSON key equals them within its tol, that the value at
the decimal places the question asks for is accepted, that the number printed last in
feedback.correct lies inside the band, and that every `wrong` value matches its named
slip, lies outside the key's band and overlaps no other. Expression parts are checked
for equivalence of answer and accept forms and for every wrong form differing. Choice
parts check the keyed option. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-taylor-numbers.py
"""
import json, os, re, sys, itertools
from math import exp, log
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'taylor')
fails, checks = [], 0
R = sp.Rational
X, K = sp.symbols('x k')


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {it['id']: it for it in d['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def printed_value(text):
    """The number after the last '=' or '\\approx' in a feedback line."""
    t = text.replace('{,}', '').replace('\\,', '')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', t))
    return float(hits[-1].group(2)) if hits else None


def num(items, iid, k, exact, alt, slips, dp=None, agree=1e-9):
    """Part k of item iid: a numeric key. exact (sympy) and alt (float) by two methods;
    slips: {wrong id: value the slip gives}; dp: decimal places the question asks for."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if dp is not None:
        r = round(e, dp)
        ok(abs(r - w['answer']) <= tol + 1e-12, f'{tag}: value at {dp} dp {r} not accepted')
        ok(re.search(r'decimal|places|fraction|nearest', part['question']) is not None, f'{tag}: form not stated')
    pv = printed_value(part['feedback']['correct'])
    if pv is not None:
        ok(abs(pv - w['answer']) <= tol + 1e-12, f'{tag}: printed {pv} outside band')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    ok(set(wrongs) <= set(part['feedback'].get('byKey', {})), f'{tag}: a wrong id has no byKey line')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, 10 ** -(dp or 4) / 2 + 1e-12), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def tex_to_sympy(s):
    t = s.replace('\\left', '').replace('\\right', '').replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
    pat = re.compile(r'\\frac\{([^{}]*)\}\{([^{}]*)\}')
    while pat.search(t):
        t = pat.sub(r'((\1)/(\2))', t)
    t = t.replace('{', '(').replace('}', ')').replace('^', '**').replace('\\', '')
    tr = standard_transformations + (implicit_multiplication_application,)
    return parse_expr(t, local_dict={'x': X, 'k': K}, transformations=tr)


def expr(items, iid, k, target, accepts_min=1):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    ok(sp.simplify(tex_to_sympy(w['answer']) - target) == 0, f'{tag}: answer {w["answer"]} differs from {target}')
    ok(len(w.get('accept', [])) >= accepts_min, f'{tag}: too few accept forms')
    for a_ in w.get('accept', []):
        ok(sp.simplify(tex_to_sympy(a_) - target) == 0, f'{tag}: accept {a_} differs')
    for x in w.get('wrong', []):
        ok(sp.simplify(tex_to_sympy(x['tex']) - target) != 0, f'{tag}: wrong {x["id"]} equals the answer')


def pick(items, iid, k, correct_id, n_opts=4):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    ok(len(w['options']) == n_opts, f'{iid} p{k}: {len(w["options"])} options')
    ok(all(o.get('correct') or o.get('why') for o in w['options']), f'{iid} p{k}: option without why')


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def dnum(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def d2num(f, x, h=1e-4):
    return (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2


def bond(cfs, y):
    """Exact price, slope and second derivative of cash flows {t: c} at yield y."""
    Y = sp.Symbol('y')
    P = sum(R(c) / (1 + Y) ** t for t, c in cfs.items())
    return P.subs(Y, y), sp.diff(P, Y).subs(Y, y), sp.diff(P, Y, 2).subs(Y, y)


def bondf(cfs):
    return lambda y: sum(c / (1 + y) ** t for t, c in cfs.items())


# ---------------------------------------------------------------- level 1
I = load(1)
if I is not None:
    ok(len(I) >= 3 and len(I) <= 5, 'set 1: item count')
    # p-cube-root-27
    f = X ** R(1, 3)
    a = 27
    fa, f1, f2 = f.subs(X, a), sp.diff(f, X).subs(X, a), sp.diff(f, X, 2).subs(X, a)
    ok(fa == 3 and f1 == R(1, 27) and f2 == R(-2, 2187), 'cube root derivatives')
    ff = lambda x: x ** (1 / 3)
    ok(abs(dnum(ff, 27) - 1 / 27) < 1e-8 and abs(d2num(ff, 27) + 2 / 2187) < 1e-6, 'cube root numeric derivatives')
    expr(I, 'p-cube-root-27', 1, 3 + (X - 27) / 27)
    h = R(81, 100)
    L = fa + f1 * h
    num(I, 'p-cube-root-27', 2, L, 3 + 0.81 / 27,
        {'ninth': 3 + h / 9, 'third': 3 + h / 3, 'whole-x': 3 + R(2781, 100) / 27}, dp=4)
    err = f2 / 2 * h ** 2
    num(I, 'p-cube-root-27', 3, err, -0.6561 / 2187,
        {'no-half': f2 * h ** 2, 'h-not-squared': f2 / 2 * h, 'sign': -err}, dp=5)
    num(I, 'p-cube-root-27', 4, L + err, 3.03 - 0.0003,
        {'sign': L - err, 'no-half': L + 2 * err, 'ninth-carried': 3 + h / 9 + err}, dp=4)
    ok(abs(round(27.81 ** (1 / 3), 4) - 3.0297) < 1e-12, 'cube root of 27.81 is 3.0297 to 4 places')
    ok(abs(float(L - 27.81 ** (1 / 3)) - 0.000295) < 1e-5, 'true tangent error about 0.0003')

    # p-newton-cubic
    g = X ** 3 + X - 3
    gp = sp.diff(g, X)
    step = lambda x: x - g.subs(X, x) / gp.subs(X, x)
    x1 = step(sp.Integer(1)); x2 = step(x1); x3 = step(x2)
    ok(x1 == R(5, 4) and x2 == R(17, 14), 'newton iterates exact')
    ok(g.subs(X, x2) == R(13, 2744) and gp.subs(X, x2) == R(1063, 196), 'f and f\' at x2 as printed')
    gf = lambda x: x ** 3 + x - 3
    fx = [1.0]
    for _ in range(3):
        fx.append(fx[-1] - gf(fx[-1]) / dnum(gf, fx[-1]))
    root = bisect(gf, 1, 2)
    num(I, 'p-newton-cubic', 1, x1, fx[1], {'sign': 1 + R(-1, 4), 'no-plus-one': 1 + R(1, 3), 'no-step': 1})
    num(I, 'p-newton-cubic', 2, x2, fx[2],
        {'sign': x1 + g.subs(X, x1) / gp.subs(X, x1), 'no-plus-one': x1 - g.subs(X, x1) / (3 * x1 ** 2)}, dp=4, agree=1e-8)
    pick(I, 'p-newton-cubic', 3, 'above')
    ok(float(x2) > root and 6 * root > 0, 'x2 above the root and f\'\' > 0 there')
    num(I, 'p-newton-cubic', 4, x3, fx[3],
        {'sign': x2 + g.subs(X, x2) / gp.subs(X, x2), 'no-plus-one': x2 - g.subs(X, x2) / (3 * x2 ** 2), 'stop': x2}, dp=6, agree=1e-8)
    ok(abs(float(x3) - root) < 1e-6 and abs(round(float(x1) - root, 3) - 0.037) < 1e-9 and abs(float(x2) - root - 0.00087) < 1e-5, 'errors 0.037, 0.00087, 5e-7')

    # p-loss-limit
    cf = {1: 3, 2: 3, 3: 3, 4: 103}
    P, dP, _ = bond(cf, R(4, 100))
    pf = bondf(cf)
    num(I, 'p-loss-limit', 1, P, pf(0.04),
        {'par': 100, 'face-only': R(103) / R(104, 100) ** 4, 'no-discount': 112}, dp=2)
    num(I, 'p-loss-limit', 2, dP, dnum(pf, 0.04),
        {'no-t': -P / R(104, 100), 'power-t': dP * R(104, 100), 'positive': -dP}, dp=2, agree=1e-7)
    dPr = R(-35443, 100)
    lots = 40000
    dv01 = -dPr * R(1, 10000) * lots
    num(I, 'p-loss-limit', 3, dv01, 354.43 / 10000 * 40000,
        {'one-lot': -dPr / 10000, 'hundredfold': -dPr * R(1, 100) * lots, 'price-not-slope': R(9637, 100) / 10000 * lots}, dp=0)
    ok(abs(float(-dP) / 10000 * lots - 1417.74) < 0.005, 'DV01 from the unrounded slope is 1417.74')
    dv = R(141772, 100)
    move = 50000 / dv
    num(I, 'p-loss-limit', 4, move, 50000 / 1417.72,
        {'hundredfold': 50000 / (dv * 100), 'price-not-slope': 50000 / (R(9637, 100) / 10000 * lots)}, dp=1)
    pick(I, 'p-loss-limit', 5, 'later')
    true_loss = (pf(0.04) - pf(0.04 + float(move) / 10000)) * lots
    true_move = bisect(lambda z: (pf(0.04) - pf(0.04 + z)) * lots - 50000, 0, 0.01) * 10000
    ok(true_loss < 50000 and abs(round(true_loss, -2) - 49600) < 1e-9, f'true loss at 35.27 bp about 49,600 ({true_loss:.0f})')
    ok(abs(round(true_move, 1) - 35.6) < 1e-9, f'true move for the limit 35.6 bp ({true_move:.2f})')
    ok(abs((pf(0.04) - pf(0.0435)) - 1.25) < 0.02, 'about 1.25 a lot on 35 bp')

    # p-loan-rate
    cf = {1: 3700, 2: 3700, 3: 3700}
    V, dV, _ = bond(cf, R(5, 100))
    vf = bondf(cf)
    num(I, 'p-loan-rate', 1, V, vf(0.05),
        {'no-discount': 11100, 'one-year': R(11100) / R(105, 100), 'last-only': R(3700) / R(105, 100) ** 3}, dp=2)
    ok(abs(sum(1 / 1.05 ** t for t in (1, 2, 3)) - 2.723248) < 5e-7, 'annuity factor 2.723248')
    num(I, 'p-loan-rate', 2, dV, dnum(vf, 0.05),
        {'no-t': -V / R(105, 100), 'power-t': dV * R(105, 100), 'positive': -dV}, dp=2, agree=1e-7)
    ok(abs(sum(t / 1.05 ** (t + 1) for t in (1, 2, 3)) - 5.10281) < 5e-6, 'slope factor 5.10281')
    Vr, dVr = R(1007602, 100), R(-1888040, 100)
    D = -dVr / Vr
    num(I, 'p-loan-rate', 3, D, 18880.40 / 10076.02,
        {'upside-down': Vr / -dVr, 'macaulay': D * R(105, 100), 'negative': -D}, dp=3)
    y1 = R(5, 100) - (Vr - 10000) / dVr
    num(I, 'p-loan-rate', 4, y1, 0.05 + 76.02 / 18880.40,
        {'sign': R(5, 100) + (Vr - 10000) / dVr, 'step-only': -(Vr - 10000) / dVr}, dp=5)
    y1r = R(5403, 100000)
    V1, dV1, _ = bond(cf, y1r)
    ok(abs(float(V1) - 10000.41) < 0.005 and abs(float(dV1) + 18642.89) < 0.005, "V(y1) and V'(y1) as printed")
    y2 = y1r - (R(1000041, 100) - 10000) / R(-1864289, 100)
    y2alt = 0.05403 - (vf(0.05403) - 10000) / dnum(vf, 0.05403)
    num(I, 'p-loan-rate', 5, y2, y2alt,
        {'sign': y1r + (R(1000041, 100) - 10000) / R(-1864289, 100), 'step-only': R(41, 100) / R(1864289, 100), 'stop': y1r}, dp=6, agree=1e-6)
    rate = bisect(lambda z: vf(z) - 10000, 0.01, 0.2)
    ok(abs(rate - float(y2)) < 5e-7 and 0.05403 < rate, 'y2 is the rate to 6 places; y1 fell short')

print(f'{checks} checks, {len(fails)} failures')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
