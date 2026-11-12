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


def derived_slips(slips, wrongs, e, text=''):
    """Slips the script derives itself for the `sign` / `sign2` and `decimal` wrong entries.

    sign: the absolute value of the computed key (the sign-dropped answer).
    decimal: the computed key over 100 (over 10,000 where the part is in %^2).
    Each is then compared with the content value inside its tolerance, and must lie
    outside the key band, by the ordinary slip checks below."""
    s = dict(slips or {})
    for wid in wrongs:
        if wid in s:
            continue
        if re.fullmatch(r'sign\d*', wid):
            s[wid] = abs(e)
        elif wid == 'decimal':
            s[wid] = e / (10000 if '%²' in text else 100)
    return s


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
    slips = derived_slips(slips, wrongs, e, json.dumps(part, ensure_ascii=False))
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
    # p-cube-root-27 (fix pass 1.3 b: now the fourth root of 16.32 about 16; the id is kept)
    f = X ** R(1, 4)
    a = 16
    fa, f1, f2 = f.subs(X, a), sp.diff(f, X).subs(X, a), sp.diff(f, X, 2).subs(X, a)
    ok(fa == 2 and f1 == R(1, 32) and f2 == R(-3, 2048), 'fourth root derivatives')
    ff = lambda x: x ** 0.25
    ok(abs(dnum(ff, 16) - 1 / 32) < 1e-8 and abs(d2num(ff, 16) + 3 / 2048) < 1e-6, 'fourth root numeric derivatives')
    ok(sp.diff(f, X, 2) == R(-3, 16) * X ** R(-7, 4) and 16 ** R(-3, 4) == R(1, 8) and 16 ** R(-7, 4) == R(1, 128), 'fourth root: f\'\' formula, 16^(-3/4) = 1/8, 16^(-7/4) = 1/128')
    expr(I, 'p-cube-root-27', 1, 2 + (X - 16) / 32)
    h = R(32, 100)
    L = fa + f1 * h
    num(I, 'p-cube-root-27', 2, L, 2 + 0.32 / 32,
        {'eighth': 2 + h / 8, 'quarter': 2 + h / 4, 'whole-x': 2 + R(1632, 100) / 32}, dp=4)
    err = f2 / 2 * h ** 2
    ok(h ** 2 == R(1024, 10000) and err == R(-75, 1000000), 'fourth root: h^2 = 0.1024 and error exactly -0.000075')
    num(I, 'p-cube-root-27', 3, err, -0.1024 * 3 / 2048 / 2,
        {'no-half': f2 * h ** 2, 'h-not-squared': f2 / 2 * h, 'sign': -err}, dp=6)
    num(I, 'p-cube-root-27', 4, L + err, 2.01 - 0.000075,
        {'sign': L - err, 'no-half': L + 2 * err, 'eighth-carried': 2 + h / 8 + err}, dp=6)
    ok(abs(round(16.32 ** 0.25, 6) - 2.009926) < 1e-12, 'fourth root of 16.32 is 2.009926 to 6 places')
    ok(abs(float(L + err) - 16.32 ** 0.25) < 1e-6 and abs(float(L - 16.32 ** 0.25) - 0.000075) < 1e-6, 'corrected estimate within 1e-6 of the true root; tangent error about 0.000075')

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
    ok(abs(4 * 103 / 1.04 ** 5 - 338.63397) < 1e-5 and abs(float(4 * 103 / R(104, 100) ** 5) - 338.63397) < 1e-5, 'loss-limit term 4 x 103 / 1.04^5 = 338.6340 (not 338.6338)')
    ok(round(2.7737 + 5.3340 + 7.6932 + 338.6340, 4) == 354.4349 and abs(sum(t * c / 1.04 ** (t + 1) for t, c in cf.items()) - 354.4349) < 5e-4, 'loss-limit terms 2.7737 + 5.3340 + 7.6932 + 338.6340 = 354.4349')
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
    ok(round(3 / 1.05 ** 4, 6) == 2.468107 and round(float(3 / R(105, 100) ** 4), 6) == 2.468107, 'loan-rate term 3 / 1.05^4 = 2.468107 (not 2.468108)')
    ok(abs(0.907029 + 1.727675 + 2.468107 - 5.102811) < 1e-9 and round(sum(t / 1.05 ** (t + 1) for t in (1, 2, 3)), 5) == 5.10281, 'loan-rate printed terms add to 5.102811; the true sum 5.1028121 rounds to the printed 5.10281')
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

# ---------------------------------------------------------------- level 2
I = load(2)
if I is not None:
    ok(3 <= len(I) <= 5, 'set 2: item count')
    # p-three-halves: f = x^(3/2) about 4
    f = X ** R(3, 2)
    d = [sp.diff(f, X, j).subs(X, 4) for j in range(4)]
    ff = lambda x: x ** 1.5
    ok(d == [8, 3, R(3, 8), R(-3, 64)], 'x^(3/2) derivatives at 4')
    num(I, 'p-three-halves', 1, d[1], dnum(ff, 4), {'no-root': R(3, 2), 'up-power': R(3, 2) * 4 ** R(5, 2)}, agree=1e-8)
    c2 = d[2] / 2
    num(I, 'p-three-halves', 2, c2, d2num(ff, 4) / 2, {'no-half': d[2], 'root-up': R(3, 4) * 2 / 2}, dp=4, agree=1e-6)
    h = R(4, 10)
    Q = 8 + 3 * h + c2 * h ** 2
    num(I, 'p-three-halves', 3, Q, 8 + 3 * 0.4 + 0.1875 * 0.16,
        {'no-half': 8 + 3 * h + d[2] * h ** 2, 'root-up': 8 + 3 * h + R(3, 4) * h ** 2, 'tangent': 8 + 3 * h}, dp=4)
    c3 = d[3] / 6
    c3alt = (d2num(ff, 4.001) - d2num(ff, 3.999)) / 0.002 / 6
    num(I, 'p-three-halves', 4, c3, c3alt, {'no-factorial': d[3], 'divide-three': d[3] / 3, 'sign': -c3}, dp=5, agree=1e-4)
    P3 = Q + c3 * h ** 3
    num(I, 'p-three-halves', 5, P3, sp.series(f, X, 4, 4).removeO().subs(X, R(44, 10)),
        {'divide-three': Q + d[3] / 3 * h ** 3, 'no-factorial': Q + d[3] * h ** 3, 'sign': Q - c3 * h ** 3}, dp=4)
    ok(round(4.4 ** 1.5, 4) == 9.2295 and abs(round(4.4 ** 1.5, 5) - 9.22952) < 1e-9, '4.4^(3/2) = 9.22952')

    # p-square-geometric: (1 - x)^-2
    g = (1 - X) ** -2
    ser = sp.series(g, X, 0, 6).removeO()
    ok(all(ser.coeff(X, j) == j + 1 for j in range(6)), 'coefficients k + 1 from sympy series')
    g3 = sp.diff(g, X, 3).subs(X, 0)
    gf = lambda x: (1 - x) ** -2.0
    # sympy against the hand product of the powers 2 x 3 x 4
    num(I, 'p-square-geometric', 1, g3, 2 * 3 * 4, {'geometric': sp.diff(1 / (1 - X), X, 3).subs(X, 0), 'sign': -g3})
    num(I, 'p-square-geometric', 2, g3 / 6, ser.coeff(X, 3), {'no-factorial': g3, 'divide-three': g3 / 3, 'geometric': R(6, 6)})
    expr(I, 'p-square-geometric', 3, K + 1)
    ok(all(sp.factorial(k + 1) / sp.factorial(k) == k + 1 for k in range(10)), '(k+1)!/k! = k + 1')
    pick(I, 'p-square-geometric', 4, 'outside')
    ok(gf(1.5) == 4 and sum((k + 1) * (-0.5) ** k for k in range(200)) - 1 / 2.25 < 1e-12, 'f(1.5) = 4; series at -0.5 sums to 1/2.25')
    xv = R(1, 10)
    est = sum((k + 1) * xv ** k for k in range(4))
    num(I, 'p-square-geometric', 5, est, 1 + 0.2 + 0.03 + 0.004,
        {'c3-24': est - 4 * xv ** 3 + 24 * xv ** 3, 'geometric': sum(xv ** k for k in range(4)), 'k-only': sum(k * xv ** k for k in range(4))}, dp=4)
    ok(abs(1 / 0.81 - 1.234568) < 5e-7 and abs(1 / 0.81 - float(est) - 0.000568) < 1e-6, '1/0.81 and the gap')

    # p-eight-coupon
    cf = {1: 8, 2: 8, 3: 8, 4: 108}
    P, dP, d2P = bond(cf, R(7, 100))
    pf = bondf(cf)
    ok(abs(float(-dP / P) - 3.3502) < 0.00005, 'D = 3.3502 as printed')
    num(I, 'p-eight-coupon', 1, P, pf(0.07), {'par': 100, 'face-only': R(108) / R(107, 100) ** 4, 'no-discount': 132}, dp=2)
    ok(abs(float(P - R(108) / R(107, 100) ** 4) - 20.99) < 0.005, 'coupons add 20.99')
    num(I, 'p-eight-coupon', 2, d2P, d2num(pf, 0.07),
        {'power-t': d2P * R(107, 100) ** 2, 't-squared': sum(R(t * t * c) / R(107, 100) ** (t + 2) for t, c in cf.items()),
         'one-term': R(20 * 108) / R(107, 100) ** 6}, dp=2, agree=1e-6)
    ok(abs(float(d2P - R(20 * 108) / R(107, 100) ** 6) - 118.13) < 0.005, 'coupons add 118.13 to the bend')
    Pr, d2r = R(10339, 100), R(155743, 100)
    num(I, 'p-eight-coupon', 3, d2r / Pr, 1557.43 / 103.39,
        {'power-t': R(178310, 100) / Pr, 't-squared': R(123372, 100) / Pr, 'upside-down': Pr / d2r}, dp=2)
    ok(abs(float(d2P / P) - 15.06) < 0.005, 'C from unrounded values also 15.06')
    D, Cv, dy = R(33502, 10000), R(1506, 100), R(15, 1000)
    dur = Pr * (1 - D * dy)
    num(I, 'p-eight-coupon', 4, dur, 103.39 - 3.3502 * 103.39 * 0.015,
        {'sign': Pr * (1 + D * dy), 'percent': Pr * (1 - D * R(15, 10)), 'no-price': Pr - D * dy}, dp=2)
    dc = dur + Cv * Pr * dy ** 2 / 2
    num(I, 'p-eight-coupon', 5, dc, 103.39 * (1 - 3.3502 * 0.015 + 0.5 * 15.06 * 0.015 ** 2),
        {'subtract': dur - Cv * Pr * dy ** 2 / 2, 'no-half': dur + Cv * Pr * dy ** 2, 'not-squared': dur + Cv * Pr * dy / 2}, dp=2)
    true85 = pf(0.085)
    ok(round(true85, 2) == 98.36 and round(true85 - float(dur), 2) == 0.17 and abs(float(dc) - true85) < 0.01, 'true price 98.36: 17p from duration, a penny from both')

    # p-log-two
    lg = sp.log(1 + X)
    ser = sp.series(lg, X, 0, 6).removeO()
    s5 = ser.subs(X, R(-1, 2))
    pick(I, 'p-log-two', 1, 'half')
    ok(abs(sum((-1) ** (k + 1) / k for k in range(1, 6)) - 0.78333) < 5e-6, 'five terms at x = 1 give 0.783')
    alt5 = sum(0.5 ** k / k for k in range(1, 6))
    num(I, 'p-log-two', 2, -s5, alt5,
        {'four-terms': sum(R(1, 2 ** k * k) for k in range(1, 5)), 'alternating': sum((-1) ** (k + 1) * R(1, 2 ** k * k) for k in range(1, 6)),
         'x-one': ser.subs(X, 1)}, dp=4)
    L2 = sp.log(X)
    e2 = [sp.diff(L2, X, j).subs(X, 2) for j in range(4)]
    num(I, 'p-log-two', 3, e2[2] / 2, d2num(log, 2) / 2, {'no-half': e2[2], 'centre-one': sp.diff(L2, X, 2).subs(X, 1) / 2, 'sign': -e2[2] / 2}, dp=4, agree=1e-6)
    num(I, 'p-log-two', 4, e2[3] / 6, (d2num(log, 2.001) - d2num(log, 1.999)) / 0.002 / 6,
        {'no-factorial': e2[3], 'divide-three': e2[3] / 3, 'centre-one': sp.diff(L2, X, 3).subs(X, 1) / 6}, dp=4, agree=1e-3)
    l2 = R(68854, 100000)
    t = R(1, 10)
    est = l2 + t / 2 - t ** 2 / 8 + t ** 3 / 24
    num(I, 'p-log-two', 5, est, 0.68854 + 0.05 - 0.00125 + 0.001 / 24,
        {'no-cubic': l2 + t / 2 - t ** 2 / 8, 'no-half': l2 + t / 2 - t ** 2 / 4 + t ** 3 / 24,
         'four-terms': sum(R(1, 2 ** k * k) for k in range(1, 5)) + t / 2 - t ** 2 / 8 + t ** 3 / 24,
         'x-one': ser.subs(X, 1) + t / 2 - t ** 2 / 8 + t ** 3 / 24}, dp=5)
    ok(abs(log(2) - float(-s5) - 0.0046) < 0.00005 and round(log(2.1), 5) == 0.74194, 'ln 2 gap 0.0046; ln 2.1 = 0.74194')

# ---------------------------------------------------------------- level 3
I = load(3)
if I is not None:
    ok(3 <= len(I) <= 5, 'set 3: item count')
    n = sp.Symbol('n', positive=True)
    # p-doubling-coefficients: c_n = 2^n / n^2
    c = lambda m: R(2) ** m / R(m) ** 2
    num(I, 'p-doubling-coefficients', 1, c(5) / c(4), 2 ** 5 / 25 / (2 ** 4 / 16),
        {'upside-down': c(4) / c(5), 'no-square': 2 * R(4, 5), 'powers-only': 2})
    lim = sp.limit((2 ** (n + 1) / (n + 1) ** 2) / (2 ** n / n ** 2), n, sp.oo)
    num(I, 'p-doubling-coefficients', 2, lim, 2 * (1e8 / (1e8 + 1)) ** 2,
        {'lost-two': 1, 'radius': R(1, 2), 'part-one': c(5) / c(4)}, agree=1e-6)
    num(I, 'p-doubling-coefficients', 3, 1 / lim, 1 / 2.0, {'no-flip': lim, 'one': 1})
    geo = R(8, 10) / (1 - R(8, 10))
    num(I, 'p-doubling-coefficients', 4, geo, sum(0.8 ** k for k in range(1, 400)),
        {'from-zero': 1 / (1 - R(8, 10)), 'first-term': R(8, 10), 'flipped': R(10, 8)})
    ok(sum(0.8 ** k / k ** 2 for k in range(1, 400)) < 4, 'series at 0.4 sums below 4')
    pick(I, 'p-doubling-coefficients', 5, 'closed')
    ok(all(abs(c(m) * R(1, 2) ** m - R(1, m * m)) == 0 for m in range(1, 20)), 'terms at x = 1/2 are 1/n^2')

    # p-two-months
    lg = lambda r: log(1 + r)
    r1, r2 = R(8, 100), R(-5, 100)
    e1, e2 = r1 - r1 ** 2 / 2, r2 - r2 ** 2 / 2
    num(I, 'p-two-months', 1, e1, 0.08 - 0.0064 / 2, {'no-half': r1 - r1 ** 2, 'plus': r1 + r1 ** 2 / 2, 'just-r': r1}, dp=4)
    b1 = r1 ** 3 / 3 * 10 ** 5
    num(I, 'p-two-months', 2, b1, 0.08 ** 3 / 3 * 1e5, {'factorial': r1 ** 3 / 6 * 10 ** 5, 'no-divide': r1 ** 3 * 10 ** 5, 'kept-term': r1 ** 2 / 2 * 10 ** 5, 'unscaled': r1 ** 3 / 3}, dp=1)
    ok(abs((lg(0.08) - float(e1)) * 1e5 - 16.10) < 0.005 and (lg(0.08) - float(e1)) * 1e5 < float(b1), 'true error 16.10e-5 under the bound')
    num(I, 'p-two-months', 3, e2, -0.05 - 0.0025 / 2, {'sign': r2 + r2 ** 2 / 2, 'just-r': r2, 'no-half': r2 - r2 ** 2}, dp=5)
    M = 2 / (1 + r2) ** 3
    Mnum = max(2 / (1 + x) ** 3 for x in [-0.05 + 0.05 * j / 1000 for j in range(1001)])
    b2 = M * abs(r2) ** 3 / 6 * 10 ** 5
    num(I, 'p-two-months', 4, b2, Mnum * 0.05 ** 3 / 6 * 1e5,
        {'wrong-end': 2 * abs(r2) ** 3 / 6 * 10 ** 5, 'two-factorial': M * abs(r2) ** 3 / 2 * 10 ** 5, 'no-m': abs(r2) ** 3 / 6 * 10 ** 5, 'unscaled': b2 / 10 ** 5}, dp=2)
    true2 = abs(lg(-0.05) - float(e2)) * 1e5
    ok(abs(true2 - 4.33) < 0.005 and true2 > float(abs(r2) ** 3 / 3 * 10 ** 5) and true2 < float(b2), 'true error 4.33e-5: above 4.17, under 4.86')
    ok(abs(float(M) - 2.3327) < 0.00005, 'M = 2.3327')
    tot = R(1707, 100) + R(486, 100)
    num(I, 'p-two-months', 5, tot, 17.07 + 4.86,
        {'subtracted': R(1707, 100) - R(486, 100), 'wrong-end': R(1707, 100) + R(417, 100), 'first-only': R(1707, 100), 'unscaled': tot / 10 ** 5}, dp=1)
    ok(abs(float(b1 + b2) - 21.93) < 0.005, 'unrounded bounds also sum to 21.93')
    truetot = log(1.08 * 0.95)
    ok(round(truetot, 6) == 0.025668 and abs((truetot - 0.02555) * 1e5 - 11.8) < 0.05 and float(e1 + e2) == 0.02555, 'true total 0.025668, 11.8e-5 above')

    # p-tail-bound: e^0.4
    xv = R(4, 10)
    T3 = sum(xv ** k / sp.factorial(k) for k in range(4))
    num(I, 'p-tail-bound', 1, T3, sum(0.4 ** k / [1, 1, 2, 6][k] for k in range(4)),
        {'quadratic': T3 - xv ** 3 / 6, 'cube-over-three': T3 - xv ** 3 / 6 + xv ** 3 / 3, 'no-half': T3 + xv ** 2 / 2}, dp=5)
    lag = R(3, 2) * xv ** 4 / 24
    num(I, 'p-tail-bound', 2, lag, 1.5 * 0.0256 / 24, {'m-one': xv ** 4 / 24, 'power-three': R(3, 2) * xv ** 3 / 6, 'no-factorial': R(3, 2) * xv ** 4}, dp=5)
    ok(exp(0.4) < 1.5, 'e^0.4 < 1.5')
    a = lambda k: xv ** k / sp.factorial(k)
    num(I, 'p-tail-bound', 3, a(5) / a(4), 0.4 / 5, {'over-four': xv / 4, 'x-only': xv, 'upside-down': a(4) / a(5)})
    ok(all(a(k + 1) / a(k) <= R(8, 100) for k in range(4, 30)), 'later ratios at most 0.08')
    tail = a(4) / (1 - R(8, 100))
    num(I, 'p-tail-bound', 4, tail * 10 ** 4, 0.4 ** 4 / 24 * sum(0.08 ** j for j in range(60)) * 1e4, {'first-term': a(4) * 10 ** 4, 'over-four': a(4) / (1 - xv / 4) * 10 ** 4, 'lagrange': lag * 10 ** 4, 'unscaled': tail}, dp=2)
    ok(abs((exp(0.4) - float(T3)) * 1e4 - 11.58) < 0.005 and exp(0.4) - float(T3) < float(tail), 'true error 11.58e-4 under the tail bound')
    ub = R(1490667, 10 ** 6) + R(11594, 10 ** 7)
    num(I, 'p-tail-bound', 5, ub, 1.490667 + 0.0011594,
        {'lagrange': T3 + lag, 'lower': T3 + a(4), 'over-four': T3 + a(4) / (1 - xv / 4)}, dp=5, agree=2e-7)
    ok(round(float(T3 + a(4)), 5) == 1.49173 and float(T3 + a(4)) < exp(0.4) < float(ub) and round(exp(0.4), 5) == 1.49182, 'bounds hold; e^0.4 = 1.49182')

    # fix pass 1.3 b: bands of the scaled parts, and the sign-free reading of p-two-months part 5
    def inband(iid, k, val, wid=None):
        w = I[iid]['parts'][k - 1]['widget']
        if wid is None:
            return abs(val - w['answer']) <= w['tol']['abs'] + 1e-12
        e = [x for x in w['wrong'] if x['id'] == wid][0]
        return abs(val - e['value']) <= e['tol']['abs'] + 1e-12
    ok(inband('p-two-months', 4, 4.854) and inband('p-two-months', 4, 4.85) and inband('p-two-months', 4, 4.86) and not inband('p-two-months', 4, 4.17), 'two-months part 4: band takes 4.85 (M kept as 2.33), 4.86 and refuses 4.17')
    ok(abs(2.33 * 0.000125 / 6 * 1e5 - 4.854) < 0.001, 'two-months part 4: M = 2.33 gives 4.854')
    ok(inband('p-tail-bound', 4, 11.60) and inband('p-tail-bound', 4, 11.59) and inband('p-tail-bound', 4, 10.67 / 0.92) and inband('p-tail-bound', 4, 10.667 / 0.92) and not inband('p-tail-bound', 4, 11.58)
       and not inband('p-tail-bound', 4, 10.67) and not inband('p-tail-bound', 4, 11.85) and not inband('p-tail-bound', 4, 16.0), 'tail-bound part 4: band takes 11.59 and 11.60, refuses the true error 11.58, 10.67, 11.85 and 16')
    # every other slip of the part, typed unscaled, stays outside each unscaled band
    others = {('p-two-months', 2): [r1 ** 3 / 6, r1 ** 3, r1 ** 2 / 2],
              ('p-two-months', 4): [2 * abs(r2) ** 3 / 6, M * abs(r2) ** 3 / 2, abs(r2) ** 3 / 6],
              ('p-two-months', 5): [(R(1707, 100) - R(486, 100)) / 10 ** 5, (R(1707, 100) + R(417, 100)) / 10 ** 5, R(1707, 100) / 10 ** 5],
              ('p-tail-bound', 4): [a(4), a(4) / (1 - xv / 4), lag]}
    for (iid, k), vals in others.items():
        ok(inband(iid, k, float(tail if iid == 'p-tail-bound' else {2: b1, 4: b2, 5: tot}[k] / 10 ** 5), 'unscaled'), f'{iid} part {k}: unscaled band holds the bound itself')
        for v in vals:
            sv = float(v) * (1 if iid == 'p-tail-bound' else 1)
            ok(not inband(iid, k, sv, 'unscaled'), f'{iid} part {k}: unscaled band must not catch the other slip {sv}')
    for v in (0.00853, 0.0000853, 0.000512, 0.0032, 0.0000417, 0.0001221, 0.0016, 0.0010667, 0.0000204):
        ok(not any(inband(i_, k_, v, 'unscaled') for i_, k_ in others), f'unscaled bands refuse the unrelated small number {v}')
    ol = [x for x in load(1)['p-loss-limit']['parts'][2]['widget']['wrong'] if x['id'] == 'one-lot'][0]
    ok(abs(0.35 - ol['value']) > ol['tol']['abs'] and abs(0.14 - ol['value']) > ol['tol']['abs'] and abs(0.0354 - ol['value']) <= ol['tol']['abs'], 'loss-limit part 3: one-lot band holds 0.0354 only')
    # signs of the two errors in p-two-months: opposite, so the safe bound without signs is the sum and the true total error is the difference
    d1 = lg(0.08) - float(e1)
    d2 = lg(-0.05) - float(e2)
    ok(d1 > 0 and d2 < 0 and abs(d1 * 1e5 - 16.10) < 0.005 and abs(d2 * 1e5 + 4.33) < 0.005 and abs((d1 + d2) * 1e5 - 11.8) < 0.05, 'two-months: errors +16.10 and -4.33 (opposite signs), total 11.8')
    ok(abs(float(tot) - 21.93) < 1e-9 and abs(float(tot) - 17.07) > 4 and abs(d1 + d2) * 1e5 < 17.07, 'two-months part 5: the sum 21.93 is the sign-free bound; the true total error is below even the first bound')

    # p-big-gain
    an = 1.8 ** n / n
    num(I, 'p-big-gain', 1, sp.limit(an.subs(n, n + 1) / an, n, sp.oo), 1.8 * 1e8 / (1e8 + 1),
        {'upside-down': 1 / 1.8, 'radius': 1}, agree=1e-6)
    s4 = sum((-1) ** (k + 1) * xv ** k / k for k in range(1, 5))
    num(I, 'p-big-gain', 2, s4, 0.4 - 0.08 + 0.064 / 3 - 0.0256 / 4,
        {'three-terms': s4 + xv ** 4 / 4, 'all-plus': sum(xv ** k / k for k in range(1, 5)),
         'factorials': sum((-1) ** (k + 1) * xv ** k / sp.factorial(k) for k in range(1, 5))}, dp=5)
    num(I, 'p-big-gain', 3, xv ** 5 / 5, 0.4 ** 5 / 5, {'last-kept': xv ** 4 / 4, 'factorial': xv ** 5 / 120, 'no-divide': xv ** 5}, dp=5)
    ok(abs(log(1.4) - float(s4) - 0.00154) < 0.000005 and round(log(1.4), 6) == 0.336472, 'ln 1.4 = 0.336472, 0.00154 above')
    l2 = R(693147, 10 ** 6)
    s4r = R(334933, 10 ** 6)
    num(I, 'p-big-gain', 4, l2 + s4r, log(2) + float(s4),
        {'three-terms': l2 + R(341333, 10 ** 6), 'multiplied': l2 * s4r, 'simple': R(18, 10)}, dp=4, agree=1e-6)
    ok(round(log(2.8), 6) == 1.029619 and log(2.8) - 1.02808 < 0.00205, 'ln 2.8 = 1.029619, inside the bound')
    ok(round(log(2), 6) == 0.693147, 'ln 2 as printed')

print(f'{checks} checks, {len(fails)} failures')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
