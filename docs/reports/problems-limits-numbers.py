"""Recompute every number in app/content/courses/limits/problems-<n>.json twice.

Method 1 is exact: sympy (limit, diff, solve, simplify) or fractions. Method 2 is
independent: a numerical limit read from a table of inputs closing in (as lesson 1
does), a difference quotient with a small h, a brute search over whole numbers, or
the lesson's own shortcut done by hand. For each numeric part the script checks
that the two methods agree; that the JSON key lies within its tol of the value;
that the value at the rounding the question asks for is accepted; that the number
printed last in `feedback.correct` is accepted; that every `wrong` value matches its
named slip, has a byKey line, lies outside the key's band and does not overlap
another `wrong`. Expression parts check the key and every accepted form against the
sympy truth and every wrong form against it. Choice parts check the keyed option.
numbers_lib.Level.check_wrongs runs over each set as a second check of the bands.
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-limits-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import sin, cos, exp, log, pi, sqrt, isclose, ceil
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'limits')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
x, h, t, p, q, r, y = sp.symbols('x h t p q r y')


def load(n):
    path = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    return {it['id']: it for it in d['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def printed_value(text):
    """The number after the last '=' or '\\approx' in a feedback line."""
    s = text.replace('{,}', '').replace('\\,', '').replace('−', '-')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', s))
    return float(hits[-1].group(2)) if hits else None


def num(items, iid, k, exact, alt, slips=None, dp=None, agree=1e-7, printed=True):
    """Part k (1-based) of item iid: a numeric key. exact, alt: the value two ways; dp: rounding asked."""
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
        rv = round(e, dp)
        ok(abs(rv - w['answer']) <= tol + 1e-9, f'{tag}: value at {dp} dp {rv} not accepted')
    if printed:
        pv = printed_value(part['feedback']['correct'])
        ok(pv is not None, f'{tag}: no printed value in feedback.correct')
        if pv is not None:
            ok(abs(pv - w['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    slips = slips or {}
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005 if dp is None else 10 ** -dp / 2) + 1e-12,
           f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {z["value"]} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'],
           f'{tag}: wrongs {a_} and {b_} overlap')


def numset(items, iid, k, values, alt, slips=None):
    """A numeric part with answers and unordered."""
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(sorted(float(v) for v in values) == sorted(float(v) for v in alt), f'{tag}: methods differ {values} vs {alt}')
    ok(sorted(w['answers']) == sorted(float(v) for v in values), f'{tag}: key {w["answers"]} vs {values}')
    for z in w.get('wrong', []):
        vals = sorted(float(s) for s in z['value'].split(','))
        ok(vals != sorted(w['answers']), f'{tag}: wrong {z["id"]} equals the key')
        ok(z['id'] in (slips or {}), f'{tag}: wrong {z["id"]} not a named slip')
        if z['id'] in (slips or {}):
            ok(vals == sorted(float(v) for v in slips[z['id']]), f'{tag}: wrong {z["id"]} {vals} vs slip {slips[z["id"]]}')


def pick(items, iid, k, correct_id):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')


def expr_part(items, iid, k, truth, tex):
    """tex: dict from every answer, accept and wrong text in the part to its sympy form."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    for s in [w['answer']] + w.get('accept', []):
        ok(s in tex, f'{tag}: {s} not translated')
        if s in tex:
            ok(sp.simplify(tex[s] - truth) == 0, f'{tag}: {s} differs from the key')
    bykey = part['feedback'].get('byKey', {})
    for z in w.get('wrong', []):
        ok(z['tex'] in tex, f'{tag}: wrong {z["tex"]} not translated')
        if z['tex'] in tex:
            ok(sp.simplify(tex[z['tex']] - truth) != 0, f'{tag}: wrong {z["id"]} equals the key')
        ok(z['id'] in bykey, f'{tag}: wrong {z["id"]} has no byKey line')


def stated(label, shown, value, tol):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def form_stated(items):
    """the validator's [answer-form] words on every non-whole numeric part"""
    if items is None:
        return
    for iid, it in items.items():
        for k, part in enumerate(it['parts'], 1):
            w = part['widget']
            if w['kind'] == 'numeric' and 'answer' in w and not float(w['answer']).is_integer():
                ok(re.search(r'decimal|places?|fraction|nearest|per cent|percentage|in pounds|%', part['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')


def table_limit(f, a, side=0):
    """Lesson 1's method: outputs at inputs closing in on a, read off when they settle."""
    vals = []
    for n in range(3, 8):
        d = 10.0 ** -n
        if side <= 0:
            vals.append(f(a - d))
        if side >= 0:
            vals.append(f(a + d))
    return vals[-1]


def far_out(f):
    return f(1e9)


def first_whole(cond, start, stop=10 ** 6):
    return next(n for n in range(start, stop) if cond(n))


def run_level(n, body):
    items = load(n)
    if items is None:
        return
    body(items)
    form_stated(items)
    lv = Level('limits', n)
    hand = lv.check_wrongs('problems')
    bad = [rr for rr in lv.results if not rr[0]]
    ok(not bad, f'level {n}: numbers_lib check_wrongs failures {bad}')


# ------------------------------------------------------------------ level 1
def level1(L):
    # p-broker-schedule
    C_left = lambda v: 2 + 0.5 * v
    left = sp.limit(2 + sp.Rational(1, 2) * x, x, 10, '-')
    num(L, 'p-broker-schedule', 1, left, table_limit(C_left, 10, -1),
        {'no-fee': 0.5 * 10, 'right-rate': 2 + 0.4 * 10})
    k = sp.symbols('k')
    ksol = sp.solve(sp.Eq(k + sp.Rational(2, 5) * 10, left), k)[0]
    num(L, 'p-broker-schedule', 2, ksol, 7 - 0.4 * 10,
        {'value-only': 7, 'old-fee': 2, 'no-fee': 5 - 4})
    ok(abs((float(ksol) + 0.4 * 10.000001) - C_left(9.999999)) < 1e-5, 'broker: no jump at 10 once k = 3')
    per = sp.limit((3 + sp.Rational(2, 5) * x) / x, x, sp.oo)
    num(L, 'p-broker-schedule', 3, per, far_out(lambda v: (3 + 0.4 * v) / v),
        {'left-rate': 0.5, 'kept-fee': 3 + 0.4, 'to-zero': 0})

    # p-rational-features
    rx = (2 * x ** 2 - 2 * x - 12) / (x ** 2 - 9)
    rf = lambda v: (2 * v * v - 2 * v - 12) / (v * v - 9)
    ok(sp.expand(2 * (x - 3) * (x + 2)) == 2 * x ** 2 - 2 * x - 12, 'rational: top factorises as 2(x-3)(x+2)')
    l3 = sp.limit(rx, x, 3)
    num(L, 'p-rational-features', 1, l3, table_limit(rf, 3), {'lost-two': F(5, 6), 'zero-over-zero-one': 1, 'zero-over-zero': 0}, dp=4)
    ok(l3 == sp.Rational(5, 3), 'rational: limit at 3 is 5/3')
    pick(L, 'p-rational-features', 2, 'asymptote')
    ok(sp.simplify(rx - 2 * (x + 2) / (x + 3)) == 0, 'rational: simplified form')
    ok((2 * (x + 2)).subs(x, -3) == -2 and (2 * x ** 2 - 2 * x - 12).subs(x, -3) == 12, 'rational: top at -3 is -2 (simplified), 12 (original)')
    ok({sp.limit(rx, x, -3, '+'), sp.limit(rx, x, -3, '-')} == {sp.oo, -sp.oo}, 'rational: unbounded both sides of -3')
    num(L, 'p-rational-features', 3, sp.limit(rx, x, sp.oo), far_out(rf), {'constants': F(12, 9), 'hole': F(5, 3)})
    gap = sp.simplify(2 - 2 * (x + 2) / (x + 3))
    ok(sp.simplify(gap - 2 / (x + 3)) == 0, 'rational: gap 2/(x+3)')
    xs = first_whole(lambda v: F(2) - F(2 * (v + 2), v + 3) < F(1, 100), 4)
    alt = min(v for v in range(4, 1000) if 2 - rf(v) < 0.01 and F(2, v + 3) < F(1, 100))
    num(L, 'p-rational-features', 4, xs, alt,
        {'boundary': 197, 'no-shift': first_whole(lambda v: F(2, v) < F(1, 100), 1),
         'lost-two': first_whole(lambda v: F(1, v + 3) < F(1, 100), 1)})
    ok(F(2, 197 + 3) == F(1, 100), 'rational: gap at 197 is exactly 0.01')

    # p-fit-the-constants
    a, b = sp.symbols('a b')
    fx = (a * x ** 2 + b * x - 6) / (x ** 2 - x - 2)
    asol = sp.solve(sp.Eq(sp.limit(fx, x, sp.oo), 2), a)[0]
    num(L, 'p-fit-the-constants', 1, asol, 2 / 1, {'upside-down': F(1, 2)})
    bsol = sp.solve(sp.Eq((a * x ** 2 + b * x - 6).subs({a: 2, x: 2}), 0), b)[0]
    num(L, 'p-fit-the-constants', 2, bsol, (6 - 8) / 2,
        {'sign': 1, 'dropped-six': -8 / 2, 'from-half': sp.solve(sp.Eq((sp.Rational(1, 2) * x ** 2 + b * x - 6).subs(x, 2), 0), b)[0]})
    pick(L, 'p-fit-the-constants', 3, 'asymptote')
    f2 = fx.subs({a: 2, b: -1})
    ok((2 * x ** 2 - x - 6).subs(x, -1) == -3, 'fit: top at -1 is -3')
    ok(sp.limit(f2, x, -1, '+') in (sp.oo, -sp.oo), 'fit: unbounded at -1')
    ok(sp.expand((x - 2) * (2 * x + 3)) == 2 * x ** 2 - x - 6, 'fit: top factorises as (x-2)(2x+3)')
    ff = lambda v: (2 * v * v - v - 6) / (v * v - v - 2)
    num(L, 'p-fit-the-constants', 4, sp.limit(f2, x, 2), table_limit(ff, 2),
        {'far-level': 2, 'bottom-slip': F(7, 1), 'top-slip': F(4 - 3, 3)}, dp=4)
    ok(sp.expand((x - 2) * (2 * x - 3)) == 2 * x ** 2 - 7 * x + 6, 'fit: top-slip expands to 2x^2 - 7x + 6')

    # p-print-wiggle
    num(L, 'p-print-wiggle', 1, F(4, 20), max(abs(4 * sin(s) / 20) for s in [i * 0.0001 for i in range(70000)]),
        {'no-divide': 4, 'width': F(8, 20)}, agree=1e-6)
    pt = 50 + 4 * sp.sin(t) / t
    num(L, 'p-print-wiggle', 2, sp.limit(pt, t, sp.oo), 50 + 4 * sin(1e7) / 1e7, {'top': 54, 'zero': 0})
    T = first_whole(lambda v: F(4, v) <= F(1, 100), 1)
    num(L, 'p-print-wiggle', 3, T, 4 / 0.01,
        {'no-four': first_whole(lambda v: F(1, v) <= F(1, 100), 1), 'width': first_whole(lambda v: F(8, v) <= F(1, 100), 1),
         'tenth': first_whole(lambda v: F(4, v) <= F(1, 10), 1)})
    stated('wiggle band at 20 low', 49.80, 50 - 0.2, 1e-9)
    ok(all(abs(4 * sin(s) / s) <= 0.01 + 1e-12 for s in [400 + i * 0.01 for i in range(100000)]), 'wiggle: within a penny from 400 on (sampled)')


run_level(1, level1)


def dq(f, a, hh=1e-6):
    """A symmetric difference quotient: the shrinking window of l5 as the second method."""
    return (f(a + hh) - f(a - hh)) / (2 * hh)


# ------------------------------------------------------------------ level 2
def level2(L):
    # p-session-volume
    N = 3 * t ** 2 + 4 * t
    Nf = lambda v: 3 * v * v + 4 * v
    avg = (N.subs(t, 4) - N.subs(t, 1)) / 3
    num(L, 'p-session-volume', 1, avg, sum(dq(Nf, 1 + (i + 0.5) * 3 / 3000) for i in range(3000)) / 3000,
        {'no-divide': 57, 'since-start': F(64, 4), 'wrong-gap': F(57, 4)}, agree=1e-6)  # mean of the slopes over the window
    quot = sp.expand(sp.cancel((N.subs(t, 2 + h) - N.subs(t, 2)) / h))
    expr_part(L, 'p-session-volume', 2, quot, {'16+3h': 16 + 3 * h, '3h+16': 3 * h + 16, '4+3h': 4 + 3 * h, '16': sp.Integer(16)})
    ok(quot == 16 + 3 * h, 'volume: quotient is 16 + 3h')
    ok(sp.expand((3 * (4 + h ** 2) + 4 * (2 + h) - 20) / h) == 4 + 3 * h, 'volume: square-slip gives 4 + 3h')
    num(L, 'p-session-volume', 3, sp.limit(quot, h, 0), dq(Nf, 2),
        {'h-one': quot.subs(h, 1), 'since-start': F(20, 2), 'square-slip': 4}, agree=1e-6)
    tsol = sp.solve(sp.Eq(sp.diff(N, t), 34), t)[0]
    num(L, 'p-session-volume', 4, tsol, first_whole(lambda v: abs(dq(Nf, v) - 34) < 1e-4, 0),
        {'no-bring-down': sp.solve(sp.Eq(3 * t + 4, 34), t)[0], 'dropped-four': F(34, 6)})
    ok(sp.diff(N, t).subs(t, 2) == 16, 'volume: N\'(2) = 16 matches part 3')

    # p-fund-session
    V = 2 * t ** 3 - 9 * t ** 2 + 12 * t + 500
    Vf = lambda v: 2 * v ** 3 - 9 * v ** 2 + 12 * v + 500
    dV = sp.diff(V, t)
    expr_part(L, 'p-fund-session', 1, dV, {'6t^2-18t+12': 6 * t ** 2 - 18 * t + 12, '6(t-1)(t-2)': 6 * (t - 1) * (t - 2),
                                           '12-18t+6t^2': 12 - 18 * t + 6 * t ** 2, '6t^2-18t+512': 6 * t ** 2 - 18 * t + 512,
                                           '6t^3-18t^2+12t': 6 * t ** 3 - 18 * t ** 2 + 12 * t})
    roots = sp.solve(dV, t)
    alt_roots = sorted(v / 100 for v in range(0, 301) if abs(dq(Vf, v / 100)) < 1e-6)
    numset(L, 'p-fund-session', 2, roots, alt_roots, {'signs': [-1, -2]})
    pick(L, 'p-fund-session', 3, 'between')
    ok(all(dq(Vf, v) < 0 for v in [1.01 + i * 0.01 for i in range(98)]) and dq(Vf, 0.5) > 0 and dq(Vf, 2.5) > 0, 'fund: falling only on (1, 2)')
    ok(V.subs(t, 3) == 509 and V.subs(t, 0) == 500, 'fund: V(3) = 509, V(0) = 500')
    low = min(dV.subs(t, v) for v in [sp.Rational(i, 1000) for i in range(0, 3001)])
    num(L, 'p-fund-session', 4, dV.subs(t, sp.Rational(3, 2)), low,
        {'height': V.subs(t, sp.Rational(3, 2)), 'sign': F(3, 2), 'dropped-six': F(-1, 4)})

    # p-inventory-penalty
    Cq = sp.Rational(1, 2) * q ** 2
    qt = sp.expand(sp.cancel((Cq.subs(q, 4 + h) - Cq.subs(q, 4)) / h))
    expr_part(L, 'p-inventory-penalty', 1, qt, {'4+0.5h': 4 + h / 2, '4+\\frac{h}{2}': 4 + h / 2, '\\frac{8+h}{2}': (8 + h) / 2,
                                                 '0.5h+4': h / 2 + 4, '0.5h': h / 2, '8+h': 8 + h})
    ok(sp.expand((sp.Rational(1, 2) * (16 + h ** 2) - 8) / h) == h / 2, 'penalty: square-slip gives 0.5h')
    pick(L, 'p-inventory-penalty', 2, 'corner')
    ok(3 * 4 - 4 == 8 == Cq.subs(q, 4), 'penalty: draft is continuous at 4')
    left_slope = sp.limit(qt, h, 0, '-')
    num(L, 'p-inventory-penalty', 3, left_slope, dq(lambda v: 0.5 * v * v, 4),
        {'draft': 3, 'height': 8, 'no-power': sp.Rational(1, 2) * 4}, agree=1e-6)
    m_, b_ = sp.symbols('m_ b_')
    bsol = sp.solve(sp.Eq(4 * 4 + b_, Cq.subs(q, 4)), b_)[0]
    num(L, 'p-inventory-penalty', 4, bsol, 0.5 * 16 - 4 * 4, {'value': 8, 'draft': -4, 'height-slope': 8 - 8 * 4})
    tangent = sp.diff(Cq, q).subs(q, 4) * (q - 4) + Cq.subs(q, 4)
    ok(sp.expand(tangent - (4 * q - 8)) == 0, 'penalty: 4q - 8 is the tangent at 4')

    # p-perpetuity-slope
    P = 5 / r
    Pf = lambda v: 5 / v
    num(L, 'p-perpetuity-slope', 1, (P.subs(r, sp.Rational(4, 100)) - 100) / sp.Rational(-1, 100), (Pf(0.04) - Pf(0.05)) / (0.04 - 0.05),
        {'sign': 2500, 'no-divide': 25})
    ok(P.subs(r, sp.Rational(4, 100)) == 125 and P.subs(r, sp.Rational(5, 100)) == 100, 'perp: prices 125 and 100')
    s2 = (P.subs(r, sp.Rational(49, 1000)) - 100) / sp.Rational(-1, 1000)
    num(L, 'p-perpetuity-slope', 2, s2, (Pf(0.049) - Pf(0.05)) / (0.049 - 0.05),
        {'sign': -s2, 'no-divide': P.subs(r, sp.Rational(49, 1000)) - 100}, dp=0, agree=1e-9)
    stated('P(0.049)', 102.0408, P.subs(r, sp.Rational(49, 1000)), 0.00005)
    stated('rise 2.0408', 2.0408, P.subs(r, sp.Rational(49, 1000)) - 100, 0.00005)
    stated('exact -2040.82', -2040.82, s2, 0.005)
    num(L, 'p-perpetuity-slope', 3, sp.diff(P, r).subs(r, sp.Rational(5, 100)), dq(Pf, 0.05, 1e-7),
        {'sign': 2000, 'no-square': -5 / 0.05, 'secant': -2500}, agree=1e-6)
    pick(L, 'p-perpetuity-slope', 4, 'steepens')
    stated('slope at 0.04', -3125, sp.diff(P, r).subs(r, sp.Rational(4, 100)), 1e-9)


run_level(2, level2)


# ------------------------------------------------------------------ level 3
def level3(L):
    # p-relative-strength
    Pt = 40 * sp.exp(sp.Rational(6, 100) * t)
    It = 2000 * sp.exp(sp.Rational(4, 100) * t)
    Pf = lambda v: 40 * exp(0.06 * v)
    If = lambda v: 2000 * exp(0.04 * v)
    dP0 = sp.diff(Pt, t).subs(t, 0)
    num(L, 'p-relative-strength', 1, dP0, dq(Pf, 0), {'no-chain': 40, 'no-forty': F(6, 100)}, agree=1e-6)
    ok(sp.diff(It, t).subs(t, 0) == 80, 'ratio: I\'(0) = 80')
    Rt = Pt / It
    dR0 = sp.diff(Rt, t).subs(t, 0)
    quot = (dP0 * 2000 - 40 * 80) / sp.Integer(2000) ** 2
    ok(sp.simplify(dR0 - quot) == 0, 'ratio: quotient rule agrees with sympy')
    num(L, 'p-relative-strength', 2, dR0, dq(lambda v: Pf(v) / If(v), 0),
        {'swapped': -quot, 'no-square': F(4800 - 3200, 2000), 'rates': F(24, 800), 'no-chain': F(40 * 2000 - 40 * 80, 2000 ** 2)}, agree=1e-6)
    ok(Rt.subs(t, 0) == sp.Rational(1, 50), 'ratio: R(0) = 0.02')
    g = sp.simplify(sp.diff(sp.log(Rt), t))
    num(L, 'p-relative-strength', 3, dR0 / Rt.subs(t, 0), g, {'added': F(10, 100), 'raw': F(4, 10000), 'share-only': F(6, 100)})

    # p-research-price
    n_ = (50 - p) ** 2
    R_ = p * n_
    nf = lambda v: (50 - v) ** 2
    num(L, 'p-research-price', 1, sp.diff(n_, p).subs(p, 20), dq(nf, 20), {'lost-inner': 60, 'height': 900}, agree=1e-6)
    num(L, 'p-research-price', 2, sp.diff(R_, p).subs(p, 20), dq(lambda v: v * nf(v), 20),
        {'product-of-derivatives': -60, 'lost-inner': 900 + 20 * 60, 'one-term': 20 * -60}, agree=1e-6)
    dR = sp.diff(R_, p)
    expr_part(L, 'p-research-price', 3, dR, {'(50-p)(50-3p)': (50 - p) * (50 - 3 * p), '(p-50)(3p-50)': (p - 50) * (3 * p - 50),
                                             '(50-3p)(50-p)': (50 - 3 * p) * (50 - p), '(50-p)(50+p)': (50 - p) * (50 + p)})
    ok(sp.expand(1 * (50 - p) ** 2 + p * 2 * (50 - p) - (50 - p) * (50 + p)) == 0, 'feed: lost-inner gives (50-p)(50+p)')
    roots = [v for v in sp.solve(dR, p) if v < 50]
    ok(len(roots) == 1, 'feed: one flat price below 50')
    grid = min((abs(float(dR.subs(p, sp.Rational(i, 10000)))), i / 10000) for i in range(100000, 300000))[1]
    num(L, 'p-research-price', 4, roots[0], grid, {'two-p': 25}, dp=2, agree=1e-4)
    stated('feed: R\'(20) by the factorised form', -300, ((50 - p) * (50 - 3 * p)).subs(p, 20), 0)

    # p-weighted-pool
    yx = sp.Function('Y')(x)
    implicit = sp.diff(sp.Rational(4, 5) * sp.log(x) + sp.Rational(1, 5) * sp.log(yx), x)
    slope = sp.solve(sp.Eq(implicit, 0), sp.diff(yx, x))[0].subs(yx, y)
    ok(sp.simplify(slope + 4 * y / x) == 0, 'pool: dy/dx = -4y/x')
    k0 = 100 ** 0.8 * 1600 ** 0.2
    yexp = lambda v: (k0 / v ** 0.8) ** 5          # the curve solved for y
    num(L, 'p-weighted-pool', 1, slope.subs({x: 100, y: 1600}), dq(yexp, 100, 1e-4),
        {'no-weights': -F(1600, 100), 'swapped': -F(1, 4) * 16, 'upside-down': -4 * F(100, 1600), 'sign': 64}, agree=1e-6)
    ysol = sp.Integer(1600) * (sp.Rational(100, 200)) ** 4
    num(L, 'p-weighted-pool', 2, ysol, yexp(200), {'halved': 800, 'squared': 400})
    ok(abs(200 ** 0.8 * 100 ** 0.2 - k0) < 1e-9, 'pool: (200, 100) is on the curve')
    num(L, 'p-weighted-pool', 3, slope.subs({x: 200, y: 100}), dq(yexp, 200, 1e-4),
        {'old-point': -64, 'halved': -4 * F(800, 200), 'upside-down': -4 * F(200, 100)}, agree=1e-6)
    sec = (1600 - ysol) / (200 - 100)
    num(L, 'p-weighted-pool', 4, sec, (yexp(100) - yexp(200)) / 100, {'start-price': 64, 'mid': F(64 + 2, 2), 'end-price': 2}, agree=1e-9)
    ok(2 < sec < 64, 'pool: secant between the two tangent slopes')

    # p-gas-season
    s_ = 1 + sp.Rational(3, 10) * sp.cos(sp.pi * t / 6)
    sf = lambda v: 1 + 0.3 * cos(pi * v / 6)
    ds = sp.diff(s_, t)
    SINt = sp.sin(sp.pi * t / 6)
    expr_part(L, 'p-gas-season', 1, ds, {
        '-0.05\\pi\\sin\\left(\\frac{\\pi t}{6}\\right)': -sp.Rational(1, 20) * sp.pi * SINt,
        '-\\frac{\\pi}{20}\\sin\\left(\\frac{\\pi t}{6}\\right)': -sp.pi / 20 * SINt,
        '-\\frac{\\pi}{20}\\sin\\left(\\frac{\\pi}{6}t\\right)': -sp.pi / 20 * SINt,
        '-0.3\\sin\\left(\\frac{\\pi t}{6}\\right)': -sp.Rational(3, 10) * SINt,
        '0.05\\pi\\sin\\left(\\frac{\\pi t}{6}\\right)': sp.pi / 20 * SINt})
    num(L, 'p-gas-season', 2, ds.subs(t, 3), dq(sf, 3), {'lost-inner': -0.3, 'sign': sp.pi / 20}, dp=3, agree=1e-6)
    D_ = (200 + 5 * t) * s_
    Df = lambda v: (200 + 5 * v) * sf(v)
    num(L, 'p-gas-season', 3, sp.diff(D_, t).subs(t, 3), dq(Df, 3),
        {'product-of-derivatives': 5 * -sp.pi / 20, 'lost-inner': 5 + 215 * -0.3, 'one-term': 215 * -sp.pi / 20}, dp=2, agree=1e-6)
    ok(s_.subs(t, 3) == 1, 'gas: s(3) = 1')
    for route in (-0.157, -0.1571, -0.15708):
        ok(abs(5 + 215 * route - (-28.77)) <= 0.02, f'gas: the rounded route {route} is accepted')
    stated('gas: 215 x 0.05pi', 33.77, 215 * pi / 20, 0.005)
    ok(min(range(0, 12), key=lambda v: float(ds.subs(t, v))) == 3, 'gas: the factor falls fastest at t = 3')


run_level(3, level3)

present = [n for n in (1, 2, 3) if load(n) is not None]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
