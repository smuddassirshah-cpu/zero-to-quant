"""Recompute every number in app/content/courses/functions/problems-<n>.json twice.

Method 1 is exact: sympy (solve, expand, factor) or fractions. Method 2 is independent:
the lesson's own route done in floats (climb over climb, a row put into y = mx + c,
undoing a machine step by step), a brute search over a fine grid or over whole numbers,
or bisection on the graph. For each numeric part the script checks that the two methods
agree; that the JSON key lies within its tol of the value; that the value at the rounding
the question asks for is accepted; that the number printed last in `feedback.correct` is
accepted; that every `wrong` value matches its named slip, has a byKey line, lies outside
the key's band and does not overlap another `wrong`. Numeric sets (`answers`) check both
values two ways and every wrong set against its slip. Expression parts check the key and
every accepted form against the sympy truth and every wrong form against it. Choice parts
check the keyed option. numbers_lib.Level.check_wrongs runs over each set as a second check
of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-functions-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import isclose
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'functions')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
x, t, w, d = sp.symbols('x t w d')


def load(n):
    path = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(path):
        return None
    doc = json.load(open(path))
    return {it['id']: it for it in doc['items']}


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


def num(items, iid, k, exact, alt, slips=None, dp=None, agree=1e-9, printed=True):
    """Part k (1-based) of item iid: a numeric key. exact, alt: the value two ways; dp: the rounding asked."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    ok(wd['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = wd['tol']['abs']
    if dp is None:
        ok(abs(wd['answer'] - e) <= tol + 1e-12, f'{tag}: key {wd["answer"]} vs computed {e} (tol {tol})')
    else:
        rv = round(e, dp) if dp >= 0 else round(e, dp)
        ok(abs(rv - wd['answer']) <= 1e-9, f'{tag}: key {wd["answer"]} vs value at the asked rounding {rv}')
        ok(abs(e - wd['answer']) <= tol + 1e-9, f'{tag}: unrounded {e} not accepted by tol {tol}')
    if printed:
        pv = printed_value(part['feedback']['correct'])
        ok(pv is not None, f'{tag}: no printed value in feedback.correct')
        if pv is not None:
            ok(abs(pv - wd['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    slips = slips or {}
    wrongs = {z['id']: z for z in wd.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - wd['answer']) > tol + wt, f'{tag}: wrong {wid} {z["value"]} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'],
           f'{tag}: wrongs {a_} and {b_} overlap')


def numset(items, iid, k, values, alt, slips=None):
    """A numeric part with answers and unordered: the values two ways, each wrong set against its slip."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    key = sorted(float(v) for v in values)
    ok(key == sorted(float(v) for v in alt), f'{tag}: methods differ {values} vs {alt}')
    ok(sorted(wd['answers']) == key, f'{tag}: key {wd["answers"]} vs {values}')
    ok(wd.get('unordered') is True, f'{tag}: not unordered')
    bykey = part['feedback'].get('byKey', {})
    ok('count' in bykey, f'{tag}: no byKey line for count')
    slips = slips or {}
    ok({z['id'] for z in wd.get('wrong', [])} == set(slips), f'{tag}: wrong ids vs slips {sorted(slips)}')
    for z in wd.get('wrong', []):
        vals = sorted(float(s) for s in z['value'].split(','))
        ok(vals != key, f'{tag}: wrong {z["id"]} equals the key')
        ok(z['id'] in bykey, f'{tag}: wrong {z["id"]} has no byKey line')
        if z['id'] in slips:
            ok(vals == sorted(float(v) for v in slips[z['id']]), f'{tag}: wrong {z["id"]} {vals} vs slip {slips[z["id"]]}')


def pick(items, iid, k, correct_id):
    if items is None:
        return
    wd = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in wd['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')


def expr_part(items, iid, k, truth, tex):
    """tex: dict from every answer, accept and wrong text in the part to its sympy form."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    ok(wd['kind'] == 'expression', f'{tag}: not expression')
    for s in [wd['answer']] + wd.get('accept', []):
        ok(s in tex, f'{tag}: {s} not translated')
        if s in tex:
            ok(sp.simplify(tex[s] - truth) == 0, f'{tag}: {s} differs from the key')
    bykey = part['feedback'].get('byKey', {})
    for z in wd.get('wrong', []):
        ok(z['tex'] in tex, f'{tag}: wrong {z["tex"]} not translated')
        if z['tex'] in tex:
            ok(sp.simplify(tex[z['tex']] - truth) != 0, f'{tag}: wrong {z["id"]} equals the key')
        ok(z['id'] in bykey, f'{tag}: wrong {z["id"]} has no byKey line')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def form_stated(items):
    """the validator's [answer-form] words on every numeric part, whole or not"""
    if items is None:
        return
    for iid, it in items.items():
        for k, part in enumerate(it['parts'], 1):
            wd = part['widget']
            if wd['kind'] == 'numeric' and 'answer' in wd:
                ok(re.search(r'decimal|places?|whole number|exact value|nearest|in pounds|both', part['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')


def line_through(p, q):
    """exact gradient and intercept with fractions, as l8 teaches: m = rise / run, c = y1 - m x1"""
    m = F(q[1] - p[1]) / F(q[0] - p[0])
    return m, F(p[1]) - m * p[0]


def line_by_floats(p, q):
    """second route: solve the two equations y = m x + c by elimination in floats"""
    (x1, y1), (x2, y2) = p, q
    m = (y2 - y1) / (x2 - x1)
    c = (y1 * x2 - y2 * x1) / (x2 - x1)
    return m, c


def grid_zero(f, lo, hi, n=400000):
    """first sign change of f on a fine grid, refined by bisection"""
    step = (hi - lo) / n
    a = lo
    for i in range(n):
        b = lo + (i + 1) * step
        if f(a) == 0:
            return a
        if f(a) * f(b) < 0:
            for _ in range(200):
                mid = (a + b) / 2
                if f(a) * f(mid) <= 0:
                    b = mid
                else:
                    a = mid
            return (a + b) / 2
        a = b
    return None


def brute_whole(f, target, lo=-1000, hi=1000):
    return [v for v in range(lo, hi + 1) if f(v) == target]


def run_level(n, body):
    items = load(n)
    if items is None:
        return
    body(items)
    form_stated(items)
    lv = Level('functions', n)
    lv.check_wrongs('problems')
    bad = [rr for rr in lv.results if not rr[0]]
    ok(not bad, f'level {n}: numbers_lib check_wrongs failures {bad}')


# ------------------------------------------------------------------ level 1
def level1(L):
    # p-exchange-kiosk: rows (40, 43), (80, 89), (120, 135)
    rows = [(40, 43), (80, 89), (120, 135)]
    m, c = line_through(rows[0], rows[1])
    mf, cf = line_by_floats(rows[1], rows[2])
    ok(all(m * a + c == b for a, b in rows), 'kiosk: every row on E(x) = 1.15x - 3')
    num(L, 'p-exchange-kiosk', 1, m, mf,
        {'per-row': rows[1][1] - rows[0][1], 'first-row': F(43, 40), 'flipped': F(40, 46)})
    E = sp.Rational(23, 20) * x - 3
    ok(sp.Rational(m.numerator, m.denominator) == sp.Rational(23, 20) and c == -3 and isclose(cf, -3), 'kiosk: m = 23/20, c = -3 two ways')
    expr_part(L, 'p-exchange-kiosk', 2, E, {
        '1.15x-3': sp.Rational(115, 100) * x - 3, '-3+1.15x': -3 + sp.Rational(115, 100) * x,
        '\\frac{23x}{20}-3': 23 * x / 20 - 3, '\\frac{23}{20}x-3': sp.Rational(23, 20) * x - 3,
        '1.15x': sp.Rational(115, 100) * x, '1.15x+3': sp.Rational(115, 100) * x + 3, '1.15x+43': sp.Rational(115, 100) * x + 43,
        '46x-1797': 46 * x - 1797})
    stated('kiosk per-row rule c', -1797, 43 - 46 * 40)
    num(L, 'p-exchange-kiosk', 3, E.subs(x, 300), 1.15 * 300 - 3, {'no-fee': F(23, 20) * 300, 'plus-fee': F(23, 20) * 300 + 3}, agree=1e-9)
    inv = sp.solve(sp.Eq(E, 227), x)[0]
    num(L, 'p-exchange-kiosk', 4, inv, (227 + 3) / 1.15,
        {'minus-fee': (227 - 3) / 1.15, 'no-fee': 227 / 1.15, 'forward': 1.15 * 227 - 3}, agree=1e-9)
    stated('kiosk forward check', 227, F(23, 20) * 200 - 3)

    # p-van-fuel: F(d) = 60 - 0.15 d
    Fd = 60 - sp.Rational(3, 20) * d
    Ff = lambda v: 60 - 0.15 * v
    num(L, 'p-van-fuel', 1, Fd.subs(d, 120), Ff(120), {'added': 60 + 0.15 * 120, 'used': 0.15 * 120})
    empty = sp.solve(Fd, d)[0]
    num(L, 'p-van-fuel', 2, empty, grid_zero(Ff, 0, 1000), {'times': 60 * 0.15}, agree=1e-7)
    pick(L, 'p-van-fuel', 3, 'closed')
    grid = [400 * i / 4000 for i in range(4001)]
    numset(L, 'p-van-fuel', 4, [Fd.subs(d, 0), Fd.subs(d, empty)], [round(min(map(Ff, grid)), 9), round(max(map(Ff, grid)), 9)],
           {'domain': [0, 400], 'part-one': [42, 60]})
    g2 = [80 + 160 * i / 1600 for i in range(1601)]
    numset(L, 'p-van-fuel', 5, [Fd.subs(d, 80), Fd.subs(d, 240)], [round(min(map(Ff, g2)), 9), round(max(map(Ff, g2)), 9)],
           {'used': [0.15 * 80, 0.15 * 240], 'whole': [0, 60]})

    # p-stone-throw: h(t) = 45 - 5(t - 2)^2
    h = 45 - 5 * (t - 2) ** 2
    hf = lambda v: 45 - 5 * (v - 2) ** 2
    num(L, 'p-stone-throw', 1, h.subs(t, 0), hf(0), {'neg-square': 45 - 5 * (-4), 'no-square': 45 - 5 * (-2), 'whole-square': 45 - (5 * -2) ** 2})
    roots = sp.solve(h, t)
    ok(sorted(roots) == [-1, 5], 'stone: h = 0 at t = -1 and 5')
    land = max(roots)
    num(L, 'p-stone-throw', 2, land, grid_zero(hf, 0.001, 10), {'other-root': min(roots), 'no-root': 2 + 9, 'no-two': 3}, agree=1e-7)
    g3 = [5 * i / 50000 for i in range(50001)]
    numset(L, 'p-stone-throw', 3, [h.subs(t, land), sp.maximum(h, t, sp.Interval(0, 5))], [round(min(map(hf, g3)), 6), round(max(map(hf, g3)), 6)],
           {'ends': [hf(5), hf(0)], 'domain': [0, 5]})
    at40 = sorted(sp.solve(sp.Eq(h, 40), t))
    numset(L, 'p-stone-throw', 4, at40, brute_whole(hf, 40), {'signs': [-3, -1], 'no-five': roots})
    pick(L, 'p-stone-throw', 5, 'two-times')
    ok(hf(2) == 45 and len(brute_whole(hf, 45)) == 1, 'stone: 45 reached once, at t = 2 (the top option why)')

    # p-sapling-log
    log = [(1, 17), (3, 27), (4, 32), (3, 29), (6, 42)]
    weeks = [a for a, _ in log]
    ok([a for a in set(weeks) if len({b for aa, b in log if aa == a}) > 1] == [3], 'sapling: week 3 is the only clash')
    pick(L, 'p-sapling-log', 1, 'clash')
    good = [r for r in log if r != (3, 29)]
    m, c = line_through(good[0], good[1])
    mf, cf = line_by_floats(good[2], good[3])
    ok(all(m * a + c == b for a, b in good) and (m * 3 + c != 29), 'sapling: the four kept rows on h = 5w + 12, the 29 off it')
    num(L, 'p-sapling-log', 2, m, mf, {'per-row': 27 - 17, 'with-29': F(29 - 17, 2), 'height-over-week': 17})
    hw = 5 * w + 12
    ok(c == 12 and isclose(cf, 12), 'sapling: c = 12 two ways')
    expr_part(L, 'p-sapling-log', 3, hw, {'5w+12': 5 * w + 12, '12+5w': 12 + 5 * w, '5w+17': 5 * w + 17, '5w': 5 * w, '10w+7': 10 * w + 7})
    stated('sapling per-row c', 7, 17 - 10 * 1)
    num(L, 'p-sapling-log', 4, sp.solve(sp.Eq(hw, 72), w)[0], brute_whole(lambda v: 5 * v + 12, 72)[0],
        {'first-row': F(72 - 17, 5), 'no-c': F(72, 5), 'forward': 5 * 72 + 12, 'per-row': F(72 - 7, 10)})


run_level(1, level1)


# ------------------------------------------------------------------ level 2
def level2(L):
    # p-candle-burn: (2, 21), (5, 13.5)
    P, Q = (2, F(27, 2) * 0 + 21), (5, F(27, 2))
    m, c = line_through(P, Q)
    mf, cf = line_by_floats((2, 21.0), (5, 13.5))
    num(L, 'p-candle-burn', 1, m, mf, {'sign': -m, 'flipped': 1 / m, 'no-run': F(27, 2) - 21})
    num(L, 'p-candle-burn', 2, c, cf, {'sign': 21 + m * 2, 'first-point': 21, 'one-hour': 21 - m})
    hc = c + m * t
    out = sp.solve(hc, t)[0]
    num(L, 'p-candle-burn', 3, out, grid_zero(lambda v: 26 - 2.5 * v, 0, 30), {'sixteen': F(16) / F(5, 2), 'times': 26 * 2.5, 'flipped': 2.5 / 26}, agree=1e-7)
    stated('candle 0.4 h in minutes', 24, (out - 10) * 60)
    pick(L, 'p-candle-burn', 4, 't-axis')

    # p-path-and-pipe: A(-2, 1), B(4, 4), D(5, -3)
    m1, c1 = line_through((-2, 1), (4, 4))
    m1f, c1f = line_by_floats((-2, 1), (4, 4))
    num(L, 'p-path-and-pipe', 1, m1, m1f, {'flipped': 1 / m1, 'lost-minus': F(3, 2)})
    path = sp.Rational(1, 2) * x + 2
    ok(c1 == 2 and isclose(c1f, 2), 'path: c = 2 two ways')
    expr_part(L, 'p-path-and-pipe', 2, path, {
        '0.5x+2': x / 2 + 2, '\\frac{x}{2}+2': x / 2 + 2, '\\frac{1}{2}x+2': x / 2 + 2, '2+0.5x': 2 + x / 2, '\\frac{x+4}{2}': (x + 4) / 2,
        '0.5x+1': x / 2 + 1, '0.5x': x / 2, '2x+5': 2 * x + 5})
    stated('path flipped c', 5, 1 - 2 * (-2))
    m2 = -1 / m1
    num(L, 'p-path-and-pipe', 3, m2, -1 / m1f, {'reciprocal': 1 / m1, 'negative': -m1, 'same': m1})
    ok(m1 * m2 == -1, 'path: gradients multiply to -1')
    c2 = F(-3) - m2 * 5
    pipe = -2 * x + 7
    ok(c2 == 7 and sp.expand(pipe.subs(x, 5)) == -3, 'pipe: c = 7, passes D')
    expr_part(L, 'p-path-and-pipe', 4, pipe, {'-2x+7': -2 * x + 7, '7-2x': 7 - 2 * x, '-2x-3': -2 * x - 3, '-2x-13': -2 * x - 13, '2x-13': 2 * x - 13})
    stated('pipe sign slip c', -13, -3 + (-2) * 5)
    stated('pipe reciprocal slip c', -13, -3 - 2 * 5)
    xm = sp.solve(sp.Eq(path, pipe), x)[0]
    num(L, 'p-path-and-pipe', 5, xm, grid_zero(lambda v: (0.5 * v + 2) - (-2 * v + 7), -10, 10),
        {'y-value': path.subs(x, xm), 'sign-x': F(5) / F(-3, 2), 'constants': F(9) / F(5, 2)}, agree=1e-7)
    ok(path.subs(x, 2) == 3 and pipe.subs(x, 2) == 3, 'path and pipe meet at (2, 3)')

    # p-two-gyms
    mB, cB = line_through((3, 104), (8, 194))
    mBf, cBf = line_by_floats((3, 104), (8, 194))
    num(L, 'p-two-gyms', 1, mB, mBf, {'no-run': 90, 'one-point': F(104, 3)})
    num(L, 'p-two-gyms', 2, cB, cBf, {'first-point': 104, 'sign': 104 + 54, 'no-run': 104 - 90 * 3})
    A_, B_ = 24 * x + 20, 18 * x + 50
    meet = sp.solve(sp.Eq(A_, B_), x)[0]
    num(L, 'p-two-gyms', 3, meet, brute_whole(lambda v: (24 * v + 20) - (18 * v + 50), 0, 0, 100)[0],
        {'fee-gap': 30, 'fees-sum': F(70, 6)})
    stated('gyms cost at the crossing', 140, A_.subs(x, 5))
    stated('gyms cost at the crossing B', 140, B_.subs(x, 5))
    num(L, 'p-two-gyms', 4, A_.subs(x, 12) - B_.subs(x, 12), (12 - 5) * 6,
        {'rates-only': 6 * 12, 'gym-b': B_.subs(x, 12), 'gym-a': A_.subs(x, 12)})

    # p-two-savers
    asha = 15 * x + 40
    num(L, 'p-two-savers', 1, asha.subs(x, 6), sum([15] * 6) + 40, {'no-start': 90, 'swapped': 40 * 6 + 15})
    mb, cb = line_through((2, 50), (6, 110))
    mbf, cbf = line_by_floats((2, 50), (6, 110))
    num(L, 'p-two-savers', 2, mb, mbf, {'no-run': 60, 'one-point': 25})
    num(L, 'p-two-savers', 3, cb, cbf, {'first-point': 50, 'sign': 80, 'one-point': 50 - 25 * 2})
    ok(sp.solve(sp.Eq(asha, mb * x + cb), x) == [] and all(asha.subs(x, v) - (15 * v + 20) == 20 for v in range(0, 100)), 'savers: parallel, gap 20 every week')
    pick(L, 'p-two-savers', 4, 'never')


run_level(2, level2)


# ------------------------------------------------------------------ level 3
def level3(L):
    # p-bakery-trays
    P = -5 * x ** 2 + 60 * x - 100
    Pf = lambda v: -5 * v * v + 60 * v - 100
    num(L, 'p-bakery-trays', 1, P.subs(x, 0), Pf(0), {'sign': 100, 'zero': 0})
    ok(sp.expand(-5 * (x - 2) * (x - 10) - P) == 0, 'bakery: factorised form')
    numset(L, 'p-bakery-trays', 2, sp.solve(P, x), brute_whole(Pf, 0), {'signs': [-2, -10], 'fives': [-5, 2]})
    vert = sp.solve(sp.diff(P, x), x)[0]
    gbest = max(range(0, 2001), key=lambda i: Pf(i / 100)) / 100
    num(L, 'p-bakery-trays', 3, F(2 + 10, 2), gbest, {'half-top': 5, 'half-gap': 4})
    ok(vert == 6, 'bakery: vertex at 6 by calculus check')
    num(L, 'p-bakery-trays', 4, P.subs(x, 6), max(Pf(i / 100) for i in range(0, 2001)), {'from-five': Pf(5), 'from-four': Pf(4), 'sign-square': 5 * 36 + 360 - 100})
    pick(L, 'p-bakery-trays', 5, 'left')
    ok(all(Pf(v + 0.01) > Pf(v) for v in [i / 10 for i in range(0, 59)]) and all(Pf(v + 0.01) < Pf(v) for v in [6 + i / 10 for i in range(0, 60)]), 'bakery: rises below 6, falls above')
    stated('bakery P(2) check', 0, -20 + 120 - 100)

    # p-sledge-cyclist
    s = sp.Rational(1, 2) * t ** 2
    sf = lambda v: 0.5 * v * v
    num(L, 'p-sledge-cyclist', 1, s.subs(t, 4), sf(4), {'no-square': 0.5 * 4, 'whole-square': (0.5 * 4) ** 2, 'no-half': 16})
    num(L, 'p-sledge-cyclist', 2, F(8, 4), sf(4) / 4, {'times': 32, 'distance': 8})
    meet = [r for r in sp.solve(sp.Eq(s, 3 * t), t) if r > 0][0]
    num(L, 'p-sledge-cyclist', 3, meet, grid_zero(lambda v: sf(v) - 3 * v, 0.5, 20), {'no-half': 3, 'lost-t': sp.sqrt(6)}, agree=1e-7)
    num(L, 'p-sledge-cyclist', 4, s.subs(t, meet), 3 * 6, {'from-three': 3 * 3, 'no-half': 36})
    pick(L, 'p-sledge-cyclist', 5, 'sledge')
    hh = 1e-6
    ok(isclose((sf(6 + hh) - sf(6 - hh)) / (2 * hh), 6, rel_tol=1e-6) and 6 > 3, 'sledge: speed at t = 6 is 6 m/s, above the average 3')

    # p-two-cultures
    N = 200 * 2 ** t
    M = 1000 + 300 * t
    Nf = lambda v: 200 * 2 ** v
    Mf = lambda v: 1000 + 300 * v
    n3 = 200
    for _ in range(3):
        n3 *= 2
    num(L, 'p-two-cultures', 1, N.subs(t, 3), n3, {'times-three': 200 * 2 * 3, 'two-doublings': 200 * 4})
    num(L, 'p-two-cultures', 2, M.subs(t, 3) - N.subs(t, 3), Mf(3) - Nf(3), {'m-value': Mf(3), 'from-1200': Mf(3) - 1200})
    stated('cultures N(4)', 3200, Nf(4))
    stated('cultures M(4)', 2200, Mf(4))
    cross = sp.nsolve(N - M, t, 3.3)
    cross_b = grid_zero(lambda v: Nf(v) - Mf(v), 0, 10)
    signs = [Nf(v / 100) > Mf(v / 100) for v in range(0, 2001)]
    ok(sum(1 for a, b in zip(signs, signs[1:]) if a != b) == 1, 'cultures: one crossing on 0 to 20')
    pick(L, 'p-two-cultures', 3, 'once')
    num(L, 'p-two-cultures', 4, cross, cross_b, {'midway': 3.5, 'whole-hour': 3, 'too-late': 3.4}, dp=1, agree=1e-9)
    stated('cultures N(3.3)', 1970, Nf(3.3), 0.5)
    stated('cultures M(3.3)', 1990, Mf(3.3))
    stated('cultures N(3.4)', 2111, Nf(3.4), 0.5)
    stated('cultures M(3.4)', 2020, Mf(3.4))
    stated('cultures lead at 3.3 about 20', 20, Mf(3.3) - Nf(3.3), 0.5)
    stated('cultures lead at 3.4 about 90', 90, Nf(3.4) - Mf(3.4), 1.5)
    stated('cultures crossing about 3.32', 3.32, float(cross), 0.005)
    num(L, 'p-two-cultures', 5, Mf(3.3), Nf(float(cross)), {'at-three': Mf(3), 'at-four': Mf(4), 'n-at-three': Nf(3)}, dp=-2, agree=0.01)
    ok(abs(Nf(3.3) - 2000) <= 50 and abs(Mf(3.3) - 2000) <= 50, 'cultures: 1970 and 1990 both inside the band of 2000')

    # p-track-cubic
    h = x ** 3 - 6 * x ** 2 + 9 * x
    hf = lambda v: v ** 3 - 6 * v ** 2 + 9 * v
    num(L, 'p-track-cubic', 1, h.subs(x, 2), hf(2.0), {'all-plus': 8 + 24 + 18, 'cube-as-times': 6 - 24 + 18})
    ok(sp.expand(x * (x - 3) ** 2 - h) == 0, 'track: factorised form')
    numset(L, 'p-track-cubic', 2, sorted(set(sp.solve(h, x))), brute_whole(hf, 0, -100, 100), {'signs': [0, -3]})
    tp = sorted(sp.solve(sp.diff(h, x), x))
    ok(tp == [1, 3] and h.subs(x, 3) == 0 and h.subs(x, 1) == 4, 'track: turning points (1, 4) and (3, 0)')
    pick(L, 'p-track-cubic', 3, 'middle')
    ok(all(hf(v + 0.01) < hf(v) for v in [1 + i / 100 for i in range(1, 199)]), 'track: falls on 1 to 3')
    sols = sorted(r for r in set(sp.solve(sp.Eq(h, 4), x)) if 0 <= r <= 4)
    numset(L, 'p-track-cubic', 4, sols, [v for v in range(0, 5) if hf(v) == 4], {'roots': [0, 3], 'turns': [1, 3]})
    stated('track h(4)', 4, 64 - 96 + 36)


run_level(3, level3)

present = [n for n in (1, 2, 3) if load(n) is not None]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for msg in fails:
    print('FAIL', msg)
sys.exit(1 if fails else 0)
