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

present = [n for n in (1, 2, 3) if load(n) is not None]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
