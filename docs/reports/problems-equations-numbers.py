"""Recompute every number in app/content/courses/equations/problems-<n>.json twice.

Method 1 is exact: fractions, or sympy solve / solve_univariate_inequality. Method 2 is
independent: a brute search over whole numbers (or whole pence), the forward formula put
back in, the story worked line by line (day by day, ticket by ticket), or a count by
enumeration. For each numeric part the script checks that the two methods agree; that the
JSON key lies within its tol of the value; that the value at the rounding the question asks
for is accepted; that the number printed last in `feedback.correct` is accepted (where that
line ends on the answer); that every `wrong` value matches its named slip, has a byKey line,
lies outside the key's band and does not overlap another `wrong`. Expression parts parse the
key, every accepted form and every wrong form from their TeX with sympy (a route separate
from the app's grader) and compare: expressions by simplification, equations as the engine
does (left minus right a nonzero constant multiple), inequalities by their solution sets.
Choice parts check the keyed option and the arithmetic that decides it. numbers_lib's
Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-equations-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import floor, isclose
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, rationalize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'equations')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
SYM = {c: sp.Symbol(c, real=True) for c in 'abcdfhknpstuvwxyz'}
SYM.update({c: sp.Symbol(c, real=True) for c in 'CFPV'})
TR = standard_transformations + (implicit_multiplication_application, rationalize)  # decimals read as exact fractions


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    path = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(path):
        return None
    return {it['id']: it for it in json.load(open(path))['items']}


# ------------------------------------------------------------------ TeX to sympy (only the forms these sets use)
def frac_to_div(s):
    while '\\frac' in s:
        i = s.index('\\frac')
        j = i + 5
        parts = []
        for _ in range(2):
            assert s[j] == '{', s
            depth, k = 0, j
            while True:
                if s[k] == '{':
                    depth += 1
                elif s[k] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            parts.append(s[j + 1:k])
            j = k + 1
        s = s[:i] + '((' + parts[0] + ')/(' + parts[1] + '))' + s[j:]
    return s


def tex(s):
    s = s.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    s = frac_to_div(s)
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('^', '**').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict=SYM, transformations=TR)


REL = [('\\ge', sp.Ge), ('\\le', sp.Le), ('>=', sp.Ge), ('<=', sp.Le), ('>', sp.Gt), ('<', sp.Lt), ('=', sp.Eq)]


def rel(s):
    for op, cls in REL:
        if op in s:
            lhs, rhs = s.split(op)
            return cls, tex(lhs), tex(rhs)
    return None, tex(s), None


def same_rel(a, b, var):
    """a, b: TeX relations. Equations: lhs - rhs proportional; inequalities: the same solution set."""
    ca, la, ra = rel(a)
    cb, lb, rb = rel(b)
    if ca is sp.Eq or cb is sp.Eq:
        if ca is not cb:
            return False
        q = sp.simplify((la - ra) / (lb - rb))
        return q.is_number and q != 0
    sa = sp.solve_univariate_inequality(ca(la, ra), var, relational=False)
    sb = sp.solve_univariate_inequality(cb(lb, rb), var, relational=False)
    return sa == sb


def printed_value(text):
    s = text.replace('{,}', '').replace('\\,', '').replace('−', '-')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', s))
    return float(hits[-1].group(2)) if hits else None


# ------------------------------------------------------------------ part checks
def num(items, iid, k, exact, alt, slips=None, dp=None, agree=1e-9, printed=True):
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
        ok(pv is not None and abs(pv - w['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    if 'accept' in w:
        lead = re.match(r'-?\d+(?:\.\d+)?', w['accept'])
        ok(lead is not None and abs(float(lead.group()) - w['answer']) <= tol + 1e-9, f'{tag}: accept line {w["accept"]} not accepted')
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
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {z["value"]} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'],
           f'{tag}: wrongs {a_} and {b_} overlap')


def expr_part(items, iid, k, truth, slips, var=None):
    """truth: the TeX of the right answer as worked here. slips: wrong id -> TeX the named slip gives."""
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    is_rel = rel(truth)[0] is not None
    def same(a, b):
        return same_rel(a, b, var) if is_rel else sp.simplify(tex(a) - tex(b)) == 0
    for s in [w['answer']] + w.get('accept', []):
        ok(same(s, truth), f'{tag}: {s} differs from the worked answer {truth}')
        ok(not re.search(r'(?<!\\)\b(ln|log|exp|sin|cos|tan|sqrt)\(', s), f'{tag}: plain-text function name in {s}')
    bykey = part['feedback'].get('byKey', {})
    wrongs = {z['id']: z['tex'] for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, t in wrongs.items():
        ok(not same(t, truth), f'{tag}: wrong {wid} {t} equals the key')
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        if wid in slips:
            ok(same(t, slips[wid]), f'{tag}: wrong {wid} {t} is not the slip {slips[wid]}')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        ok(not same(wrongs[a_], wrongs[b_]), f'{tag}: wrongs {a_} and {b_} are equal')
    if w.get('form'):
        ok('form' in bykey, f'{tag}: form set but no byKey form line')


def pick(items, iid, k, correct_id):
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    ok(all(o.get('correct') or o.get('why') for o in w['options']), f'{iid} p{k}: a distractor has no why')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def form_stated(items):
    for iid, it in items.items():
        for k, part in enumerate(it['parts'], 1):
            w = part['widget']
            if w['kind'] == 'numeric' and not float(w['answer']).is_integer():
                ok(re.search(r'decimal|places?|fraction|nearest|per cent|percentage|in pounds|in pence|%', part['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')


def brute(cond, lo, hi):
    """every whole number in [lo, hi] with cond"""
    return [v for v in range(lo, hi + 1) if cond(v)]


def solve1(eq_tex, var):
    c, l, r = rel(eq_tex)
    return sp.solve(sp.Eq(l, r), SYM[var])[0]


def run_level(n, body):
    items = load(n)
    if items is None:
        return
    body(items)
    form_stated(items)
    typed = sum(1 for it in items.values() for p in it['parts'] if p['widget']['kind'] in ('numeric', 'expression'))
    total = sum(len(it['parts']) for it in items.values())
    ok(3 * typed >= 2 * total, f'level {n}: typed parts {typed} of {total}, under two thirds')
    ok(any(it['difficulty'] == 5 for it in items.values()), f'level {n}: no difficulty 5')
    lv = Level('equations', n)
    lv.check_wrongs('problems')
    bad = [rr for rr in lv.results if not rr[0]]
    ok(not bad, f'level {n}: numbers_lib check_wrongs failures {bad}')


# ------------------------------------------------------------------ level 1
def level1(L):
    a, n, s = SYM['a'], SYM['n'], SYM['s']
    # p-family-tickets
    expr_part(L, 'p-family-tickets', 1, 'a-5', {'reversed': '5-a', 'times': '5a'})
    bill = sp.expand(2 * a + 3 * (a - 5))
    ok(bill == 5 * a - 15, 'tickets: bill expands to 5a - 15')
    expr_part(L, 'p-family-tickets', 2, '2a+3(a-5)',
              {'three-reach': '2a+3a-5', 'sign': '2a+3a+15', 'carried': '2a+3(5-a)'})
    ok(sp.gcd(sp.Poly(bill, a).coeffs()[0], sp.Poly(bill, a).coeffs()[1]) == 5 and sp.expand(bill / 5) == a - 3, 'tickets: highest common factor 5')
    expr_part(L, 'p-family-tickets', 3, '5(a-3)', {'one-term': '5(a-15)', 'sign': '5(a+3)'})
    num(L, 'p-family-tickets', 4, 5 * (18 - 3), 2 * 18 + 3 * (18 - 5),
        {'five-off': 5 * 18 - 5, 'sign': 5 * (18 + 3), 'no-child': 5 * 18})
    stated('tickets: 36 + 39', 36 + 39, 75)

    # p-food-van
    sat = F(65, 10) - F(23, 10)
    ok(sat == F(42, 10), 'van: margin 4.20 a burger')
    expr_part(L, 'p-food-van', 1, '6.5n-2.3n-45', {'no-cost': '6.5n-45', 'added-cost': '6.5n+2.3n-45'})
    expr_part(L, 'p-food-van', 2, '4.2(n-20)-45', {'twenty-reach': '4.2n-20-45', 'sign': '4.2n+84-45'})
    expr_part(L, 'p-food-van', 3, '(4.2n-45)+(4.2n-129)', {'carried': '(4.2n-45)+(4.2n-65)', 'one-pitch': '4.2n+4.2n-129'})
    week = lambda v: F(84, 10) * v - 174
    by_day = (sat * 90 - 45) + (sat * (90 - 20) - 45)
    num(L, 'p-food-van', 4, week(90), by_day,
        {'carried': F(84, 10) * 90 - 110, 'one-pitch': F(84, 10) * 90 - 129, 'sunday': week(70)})
    stated('van: 8.4 x 90', 756, F(84, 10) * 90)
    stated('van: Saturday 378 - 45', 333, sat * 90 - 45)
    stated('van: Sunday 294 - 45', 249, sat * 70 - 45)
    stated('van: 4.2 x 20', 84, sat * 20)

    # p-number-trick
    mia = sp.expand(5 * (n + 4) - 3 * (n - 2))
    ok(mia == 2 * n + 26, 'trick: Mia expands to 2n + 26')
    expr_part(L, 'p-number-trick', 1, '5(n+4)-3(n-2)', {'sign': '5n+20-3n-6', 'five-reach': '5n+4-3n+6'})
    expr_part(L, 'p-number-trick', 2, '2(n+13)', {'one-term': '2(n+26)', 'letter': '28n'})
    by_hand = 5 * (7 + 4) - 3 * (7 - 2)
    num(L, 'p-number-trick', 3, 2 * (7 + 13), by_hand,
        {'sign': 2 * 7 + 14, 'one-term': 2 * (7 + 26), 'letter': 28 * 7, 'half': 2 * 7 + 13})
    leo = sp.expand(2 * (n + 9) + 8)
    ok(leo == mia, 'trick: Leo equals Mia for every n')
    ok(all(2 * (v + 9) + 8 == 5 * (v + 4) - 3 * (v - 2) for v in range(-50, 51)), 'trick: equal on -50..50')
    ok(2 * (7 + 9) + 8 == 40, 'trick: Leo gets 40 from 7')
    pick(L, 'p-number-trick', 4, 'same')
    stated('trick: 55 - 15', 55 - 15, 40)

    # p-market-pitch
    ok(sp.expand(s * (s + 2)) == s ** 2 + 2 * s, 'pitch: corner area')
    expr_part(L, 'p-market-pitch', 1, 's(s+2)', {'two-reach': 's^2+2', 'doubled': '2s+2s'})
    expr_part(L, 'p-market-pitch', 2, '3(s^2+2s)+4s^2', {'three-reach': '3s^2+2s+4s^2', 'unlike': '7s^2+6s^2', 'carried': '3(s^2+2)+4s^2'})
    ok(sp.factor(7 * s ** 2 + 6 * s) == s * (7 * s + 6), 'pitch: factor')
    expr_part(L, 'p-market-pitch', 3, 's(7s+6)', {'square-out': 's^2(7+6)', 'seven-out': '7s(s+6)'})
    num(L, 'p-market-pitch', 4, 4 * (7 * 4 + 6), 4 * 4 ** 2 + 3 * (4 * (4 + 2)),
        {'squared-last': (7 * 4) ** 2 + 6 * 4, 'doubled': 7 * (2 * 4) + 6 * 4, 'three-reach': 7 * 4 ** 2 + 2 * 4})
    stated('pitch: 7 x 16', 112, 7 * 4 ** 2)
    stated('pitch: 64 + 72', 64 + 72, 136)
    stated('pitch: corner 4 x 6', 24, 4 * (4 + 2))


# ------------------------------------------------------------------ level 2
def level2(L):
    # p-climbing-wall
    expr_part(L, 'p-climbing-wall', 1, '45+8c=213', {'added': '53c=213', 'swapped': '8+45c=213', 'fee-side': '8c=213+45'}, SYM['c'])
    c = solve1('45+8c=213', 'c')
    num(L, 'p-climbing-wall', 2, c, brute(lambda v: 45 + 8 * v == 213, 0, 200)[0],
        {'no-fee': F(213, 8), 'add-fee': F(213 + 45, 8)})
    stated('climb: 8 x 21', 168, 8 * 21)
    most = floor(F(300 - 45, 8))
    num(L, 'p-climbing-wall', 3, most, max(brute(lambda v: 45 + 8 * v <= 300, 0, 200)),
        {'rounded-up': most + 1, 'no-fee': floor(F(300, 8))}, printed=False)
    stated('climb: 255/8', 31.875, F(255, 8))
    stated('climb: 32 cost 301', 301, 45 + 8 * 32)
    stated('climb: 31 cost 293', 293, 45 + 8 * 31)
    pence = floor(F(25500, 35))
    num(L, 'p-climbing-wall', 4, F(pence, 100), F(max(brute(lambda p: 4500 + 35 * p <= 30000, 0, 3000)), 100),
        {'rounded-up': F(pence + 1, 100), 'no-fee': F(300, 35)}, printed=False)
    stated('climb: 255/35', 7.2857, F(255, 35), 0.00005)
    stated('climb: at 7.29', 300.15, 45 + 35 * F(729, 100))
    stated('climb: at 7.28', 299.80, 45 + 35 * F(728, 100))

    # p-cottage-share
    x = SYM['x']
    eq = '\\frac{x}{5}-20=\\frac{x+30}{6}'
    expr_part(L, 'p-cottage-share', 1, eq, {'plus': '\\frac{x}{5}+20=\\frac{x+30}{6}', 'bed-each': '\\frac{x}{5}-20=\\frac{x}{6}+30',
                                            'no-bed': '\\frac{x}{5}-20=\\frac{x}{6}'}, x)
    xs = solve1(eq, 'x')
    num(L, 'p-cottage-share', 2, xs, brute(lambda v: F(v, 5) - 20 == F(v + 30, 6), 0, 5000)[0],
        {'lone-twenty': solve1('6x-20=5x+150', 'x'), 'top': solve1('6x-600=5x+30', 'x'), 'carried-plus': solve1('\\frac{x}{5}+20=\\frac{x+30}{6}', 'x')})
    ok(sp.expand(30 * (x / 5 - 20) - 30 * (x + 30) / 6) == sp.expand(6 * x - 600 - (5 * x + 150)), 'cottage: times 30 as printed')
    six = F(int(xs) + 30, 6)
    num(L, 'p-cottage-share', 3, six, F(int(xs), 5) - 20, {'no-bed': F(int(xs), 6), 'old-share': F(int(xs), 5)})
    seven = F(780 + 30, 7)
    num(L, 'p-cottage-share', 4, seven, 810 / 7.0, {'no-bed': F(780, 7), 'six': F(810, 6)}, dp=2, agree=1e-12)
    stated('cottage: fall 14.29', 14.29, six - seven, 0.005)
    stated('cottage: 115.714', 115.714, seven, 0.0005)

    # p-power-tariffs
    A = lambda u: 45 + F(24) * u
    B = lambda u: 30 * u
    u1 = F(216, 30)
    num(L, 'p-power-tariffs', 1, u1, sp.nsolve(30 * SYM['u'] - 216, SYM['u'], 1), {'times': 216 * 30, 'minus': 216 - 30})
    um = solve1('45+24u=30u', 'u')
    tenth = [F(v, 10) for v in range(0, 200) if A(F(v, 10)) == B(F(v, 10))]
    num(L, 'p-power-tariffs', 2, um, tenth[0], {'one-rate': F(45, 24), 'added': F(45, 54), 'sign': -um})
    stated('tariff: match 225p', 225, A(um))
    ok(B(um) == 225, 'tariff: B at match 225p')
    ok(A(u1) > B(u1) and u1 < um, 'tariff: B is cheaper at 7.2, below the match')
    stated('tariff: A at 7.2', 217.8, A(u1))
    stated('tariff: 1.8p a day', 1.8, A(u1) - B(u1))
    pick(L, 'p-power-tariffs', 3, 'b')
    num(L, 'p-power-tariffs', 4, B(9) - A(9), 6 * (9 - um), {'unit-gap': 9 - um, 'no-charge': 6 * 9})
    stated('tariff: A at 9', 261, A(9))
    stated('tariff: B at 9', 270, B(9))

    # p-interest-split
    s = SYM['s']
    expr_part(L, 'p-interest-split', 1, '12000-s', {'reversed': 's-12000', 'added': '12000+s'})
    eqi = '0.04s+0.065(12000-s)=660'
    expr_part(L, 'p-interest-split', 2, eqi, {'no-minus': '0.04s+0.065\\times12000=660', 'per-cent': '4s+6.5(12000-s)=660'}, s)
    ok(not same_rel('0.04s+0.065s=660', eqi, s), 'interest: the dropped-bonds equation is not equivalent to the key')
    si = sp.nsimplify(solve1(eqi, 's'))
    interest = lambda v: F(4, 100) * v + F(65, 1000) * (12000 - v)
    num(L, 'p-interest-split', 3, si, brute(lambda v: interest(v) == 660, 0, 12000)[0],
        {'sign': -si, 'bracket-sign': F(660000 - 780000, 105), 'rhs': F(660 - 780000, -25)}, agree=1e-9)
    stated('interest: 0.04 x 4800', 192, F(4, 100) * 4800)
    stated('interest: 0.065 x 7200', 468, F(65, 1000) * 7200)
    ok(sp.expand(interest(s)) == sp.expand(780 - sp.Rational(25, 1000) * s), 'interest: 780 - 0.025s as stated')
    s2 = sp.nsimplify(solve1('780-0.025s=720', 's'))
    num(L, 'p-interest-split', 4, s2, brute(lambda v: interest(v) == 720, 0, 12000)[0],
        {'sign': -s2, 'added': F(780 + 720, 1) / F(25, 1000), 'old': si})
    stated('interest: 0.04 x 2400', 96, F(4, 100) * 2400)
    stated('interest: 0.065 x 9600', 624, F(65, 1000) * 9600)
    stated('interest: 60 / 0.025', 2400, F(60) / F(25, 1000))


# ------------------------------------------------------------------ level 3
def level3(L):
    h, F_, C, t, P, V, k, a, b, w = (SYM[v] for v in ('h', 'F', 'C', 't', 'P', 'V', 'k', 'a', 'b', 'w'))
    # p-bakery-stock
    expr_part(L, 'p-bakery-stock', 1, '240-18h\\ge60', {'strict': '240-18h>60', 'reversed': '240-18h\\le60', 'plus': '240+18h\\ge60'}, h)
    expr_part(L, 'p-bakery-stock', 2, '240-18h\\ge60', {'no-flip': 'h\\ge10', 'added': '18h\\le300', 'negative': 'h\\le-10'}, h)
    grid = [F(v, 4) for v in range(-80, 200)]
    ok(all((240 - 18 * g >= 60) == (g <= 10) for g in grid), 'bakery: h <= 10 on a quarter-hour grid')
    stated('bakery: h = 12 leaves 24', 24, 240 - 18 * 12)
    stated('bakery: h = 5 leaves 150', 150, 240 - 18 * 5)
    pick(L, 'p-bakery-stock', 3, 'filled-left')
    hours = brute(lambda v: 4 < v <= 10 and 240 - 18 * v >= 60, -100, 100)
    num(L, 'p-bakery-stock', 4, len(hours), 10 - 4, {'with-four': len(hours) + 1, 'no-ten': len(hours) - 1})
    ok(hours == [5, 6, 7, 8, 9, 10], 'bakery: the hours listed')

    # p-fridge-temperature
    expr_part(L, 'p-fridge-temperature', 1, '\\frac{F-32}{1.8}', {'order': '\\frac{F}{1.8}-32', 'sign': '\\frac{F+32}{1.8}', 'times': '1.8(F-32)'})
    ok(sp.simplify(sp.solve(sp.Eq(F_, sp.Rational(18, 10) * C + 32), C)[0] - (F_ - 32) / sp.Rational(18, 10)) == 0, 'fridge: subject by solve')
    c41 = F(41 - 32) / F(18, 10)
    num(L, 'p-fridge-temperature', 2, c41, brute(lambda v: F(18, 10) * v + 32 == 41, -100, 100)[0],
        {'order': F(41) / F(18, 10) - 32, 'sign': F(41 + 32) / F(18, 10), 'times': F(18, 10) * 9})
    stated('fridge: 212 F is 100 C', 100, F(212 - 32) / F(18, 10))
    expr_part(L, 'p-fridge-temperature', 3, '\\frac{F-32}{1.8}\\le5', {'reversed': 'F\\ge41', 'stopped': 'F\\le9'}, F_)
    readings = brute(lambda v: -25 <= F(v - 32) / F(18, 10) <= -15, -200, 200)
    lo, hi = F(18, 10) * -25 + 32, F(18, 10) * -15 + 32
    num(L, 'p-fridge-temperature', 4, len(readings), hi - lo + 1,
        {'gap': hi - lo, 'celsius': -15 - (-25) + 1, 'both-out': hi - lo - 1})
    stated('fridge: -25 C is -13 F', -13, lo)
    stated('fridge: -15 C is 5 F', 5, hi)
    stated('fridge: -25 x 1.8', -45, F(18, 10) * -25)
    stated('fridge: -15 x 1.8', -27, F(18, 10) * -15)

    # p-van-value
    expr_part(L, 'p-van-value', 1, '\\frac{P-V}{k}', {'sign': '\\frac{V-P}{k}', 'top': '\\frac{P}{k}-V', 'not-gathered': 'P-\\frac{V}{k}'})
    ok(sp.simplify(sp.solve(sp.Eq(V, P - k * t), t)[0] - (P - V) / k) == 0, 'van: subject by solve')
    value = lambda yrs: 24000 - 2400 * yrs
    age = F(24000 - 9600, 2400)
    num(L, 'p-van-value', 2, age, brute(lambda v: value(v) == 9600, 0, 50)[0],
        {'value-only': F(9600, 2400), 'sign': -age, 'added': F(24000 + 9600, 2400)})
    expr_part(L, 'p-van-value', 3, '24000-2400t>6000', {'no-flip': 't>7.5', 'added': 't<12.5', 'value-only': 't<2.5'}, t)
    stated('van: t = 5 value', 12000, value(5))
    band = sp.solve_univariate_inequality(value(t) > 6000, t, relational=False) & \
        sp.solve_univariate_inequality(value(t) <= 19200, t, relational=False)
    ok(band == sp.Interval.Ropen(2, sp.Rational(15, 2)), f'van: band solves to [2, 7.5), got {band}')
    pick(L, 'p-van-value', 4, 'right')
    ok(all((6000 < value(F(v, 8)) <= 19200) == (2 <= F(v, 8) < F(15, 2)) for v in range(-80, 160)), 'van: band on an eighth-year grid')
    stated('van: -18000 / -2400', 7.5, F(-18000, -2400))
    stated('van: -4800 / -2400', 2, F(-4800, -2400))
    years = brute(lambda v: 6000 < value(v) <= 19200, -50, 50)
    num(L, 'p-van-value', 5, len(years), 7 - 2 + 1, {'no-two': len(years) - 1, 'rounded-up': len(years) + 1})
    ok(years == [2, 3, 4, 5, 6, 7], 'van: the years listed')

    # p-fund-weight
    expr_part(L, 'p-fund-weight', 1, '\\frac{wb}{1-w}', {'sign': '\\frac{wb}{1+w}', 'dropped': 'wb', 'not-alone': 'w(a+b)'})
    ok(sp.simplify(sp.solve(sp.Eq(w, a / (a + b)), a)[0] - w * b / (1 - w)) == 0, 'fund: subject by solve')
    a4 = F(4, 10) * 6000 / (1 - F(4, 10))
    num(L, 'p-fund-weight', 2, a4, brute(lambda v: F(v, v + 6000) == F(4, 10), 0, 50000)[0],
        {'dropped': F(4, 10) * 6000, 'sign': F(4, 10) * 6000 / (1 + F(4, 10))}, agree=1e-9)
    a25 = F(25, 100) * 6000 / (1 - F(25, 100))
    num(L, 'p-fund-weight', 3, a25, min(brute(lambda v: F(25, 100) <= F(v, v + 6000) <= F(4, 10), 0, 50000)),
        {'dropped': F(25, 100) * 6000, 'sign': F(25, 100) * 6000 / (1 + F(25, 100))})
    stated('fund: 4000/10000', 0.4, F(4000, 10000))
    stated('fund: 2000/8000', 0.25, F(2000, 8000))
    blocks = brute(lambda m: 2000 <= 250 * m <= 4000, -100, 100)
    num(L, 'p-fund-weight', 4, len(blocks), 16 - 8 + 1, {'gap': 16 - 8, 'both-out': 16 - 8 - 1})
    ok(blocks[0] == 8 and blocks[-1] == 16, 'fund: n from 8 to 16')


# ================================================================== level 4 (problems-4; added after sets 1 to 3, which are unchanged)
# Method 1: sympy solve / linsolve, or Fractions. Method 2: a brute search over whole numbers, a step-by-step simulation
# (minute by minute, second by second, tray by tray), or the story worked forward. Every slip is rebuilt from its description.
def level4(L):
    b, c, x, y, n, t = (SYM[v] for v in ('b', 'c', 'x', 'y', 'n', 't'))

    # p-rowing-current: b + c = 14, b - c = 10
    expr_part(L, 'p-rowing-current', 1, 'b-c=10', {'reversed': 'c-b=10', 'helps': 'b+c=10', 'speed': 'b-c=14'})
    sol = sp.solve([sp.Eq(b + c, 14), sp.Eq(b - c, 10)], [b, c])
    pairs = [(u, v) for u in range(0, 40) for v in range(0, 40) if u + v == 14 and u - v == 10]
    ok(pairs == [(12, 2)], f'rowing: brute pairs {pairs}')
    bb, cc = sol[b], sol[c]
    num(L, 'p-rowing-current', 2, bb, pairs[0][0], {'stopped': 2 * bb, 'current': cc, 'two-c': 14 - 10})
    num(L, 'p-rowing-current', 3, 14 - bb, pairs[0][1], {'carried': 14 - 2 * bb, 'added': 14 + bb, 'sign': 10 - bb})
    km, minutes = F(0), 0
    while km < 42:                                   # minute by minute against the current
        km += F(16 - pairs[0][1], 60)
        minutes += 1
    hours = F(42, 16 - cc)
    num(L, 'p-rowing-current', 4, hours, F(minutes, 60),
        {'with': F(42, 16 + cc), 'still': F(42, 16), 'multiplied': 42 * (16 - cc)})
    ok(14 - bb == cc and bb - cc == 10, 'rowing: c = 2 fits both equations')
    stated('rowing: 14 + 10', 24, 14 + 10)
    stated('rowing: 12 - 2', 10, bb - cc)
    stated('rowing: 16 - 2', 14, 16 - cc)
    stated('rowing: 3 x 14', 42, 3 * 14)

    # p-seedling-trays: y = x + 8, 5x + 3y = 168
    expr_part(L, 'p-seedling-trays', 1, 'x+8', {'times': '8x', 'reversed': 'x-8'})
    xs = sp.solve(sp.Eq(5 * x + 3 * (x + 8), 168), x)[0]
    brute_x = brute(lambda v: 5 * v + 3 * (v + 8) == 168, 0, 200)
    num(L, 'p-seedling-trays', 2, xs, brute_x[0],
        {'bracket': F(168 - 8, 8), 'reversed': F(168 + 24, 8), 'no-eight': F(168, 8), 'times': F(168, 5 + 24)})
    ok(brute_x == [18], 'trays: one whole-number x')
    ys = xs + 8
    stated('trays: 8x = 144', 144, 168 - 24)
    stated('trays: 90 + 78', 168, 5 * 18 + 3 * 26)
    stated('trays: y = 26', 26, ys)
    expr_part(L, 'p-seedling-trays', 3, '62n', {'equal': '18n+26n', 'reversed': '18\\frac{n}{2}+26n', 'carried': '20(2n)+28n'})
    ok(all(sum([xs] * (2 * k) + [ys] * k) == 62 * k for k in range(1, 12)), 'trays: 62n by adding trays one by one')
    stated('trays: 36n + 26n', 62, 2 * xs + ys)
    nn = sp.solve(sp.Eq(62 * n, 310), n)[0]
    order = [k for k in range(0, 50) if 2 * k * 18 + k * 26 == 310]
    num(L, 'p-seedling-trays', 4, 2 * nn, 2 * order[0], {'large': nn, 'both': 3 * nn, 'plants': 2 * nn * xs})
    stated('trays: 180 + 130', 310, 10 * 18 + 5 * 26)

    # p-remote-cars: d = t^2, d = 7t
    roots = sorted(sp.solve(sp.Eq(t ** 2, 7 * t), t))
    brute_t = brute(lambda v: v * v == 7 * v, -50, 50)
    ok(roots == [0, 7] and brute_t == [0, 7], f'cars: level times {roots} {brute_t}')
    w1 = L['p-remote-cars']['parts'][0]['widget']
    ok(sorted(w1['answers']) == [0, 7] and w1.get('unordered') is True, 'cars p1: key set')
    bk1 = L['p-remote-cars']['parts'][0]['feedback']['byKey']
    ok({'count', 'point'} <= set(bk1), 'cars p1: byKey for count and point')
    ok([z['value'] for z in w1['wrong']] == ['7, 49'] and sorted([7, 7 * 7]) != [0, 7], 'cars p1: wrong set is (t, d) of the crossing')
    d7 = 7 * roots[1]
    num(L, 'p-remote-cars', 2, d7, roots[1] ** 2, {'double': 2 * roots[1], 'time': roots[1]})
    post = [r for r in sp.solve(sp.Eq(t ** 2, 81), t) if r >= 0][0]
    brute_post = brute(lambda v: v * v == 81, -100, 100)
    ok(brute_post == [-9, 9], f'cars: t^2 = 81 has {brute_post}')
    num(L, 'p-remote-cars', 3, post, max(brute_post), {'negative': -post, 'halved': F(81, 2), 'squared': 81 ** 2})
    a_pos = sum(2 * s - 1 for s in range(1, 10))      # car A second by second: 1 + 3 + ... + 17
    b_pos = sum(7 for _ in range(9))                   # car B second by second
    num(L, 'p-remote-cars', 4, 81 - 7 * post, a_pos - b_pos,
        {'position': 7 * post, 'meeting': 81 - d7, 'time-gap': post - roots[1], 'carried': 81 - 7 * (-post)})
    stated('cars: 7 x 9', 63, 7 * 9)

    # p-salt-solutions: x + y = 500, 0.15x + 0.4y = 125
    expr_part(L, 'p-salt-solutions', 1, '0.15x+0.4y=125',
              {'per-cent': '15x+40y=125', 'strength': '0.15x+0.4y=0.25', 'swapped': '0.4x+0.15y=125'})
    stated('salt: 25% of 500', 125, F(25, 100) * 500)
    lin = sp.solve([sp.Eq(x + y, 500), sp.Eq(sp.Rational(15, 100) * x + sp.Rational(40, 100) * y, 125)], [x, y])
    salt = lambda u, v: F(15, 100) * u + F(40, 100) * v
    brute_y = brute(lambda v: salt(500 - v, v) == 125, 0, 500)
    swapped_y = sp.solve([sp.Eq(x + y, 500), sp.Eq(sp.Rational(40, 100) * x + sp.Rational(15, 100) * y, 125)], [x, y])[y]
    num(L, 'p-salt-solutions', 2, lin[y], brute_y[0],
        {'other': lin[x], 'all-strong': F(125) / F(40, 100), 'even': 250, 'multiplied': 50 * F(25, 100)})
    ok(swapped_y == lin[x], 'salt: the swapped-strengths slip gives 300, the value of "other"')
    stated('salt: 0.15 x 500', 75, F(15, 100) * 500)
    stated('salt: 0.25y = 50', 50, 125 - 75)
    stated('salt: half each is 27.5%', F(275, 1000), salt(250, 250) / 500)
    num(L, 'p-salt-solutions', 3, 500 - lin[y], brute(lambda u: salt(u, 200) == 125, 0, 500)[0],
        {'salt': 125 - F(40, 100) * 200, 'carried': 500 - F(125) / F(40, 100), 'added': 500 + 200})
    stated('salt: 45 + 80', 125, salt(300, 200))
    ratio = sp.solve(sp.Eq(sp.Rational(15, 100) * x + sp.Rational(40, 100) * y, sp.Rational(25, 100) * (x + y)), x)[0]
    ok(sp.simplify(ratio - sp.Rational(3, 2) * y) == 0, f'salt: every 25% batch has x = 3y/2, got {ratio}')
    ok(F(300, 200) == F(3, 2), 'salt: 300 to 200 is 3 to 2')
    y360 = sp.solve(sp.Eq(salt(360, 0) + sp.Rational(40, 100) * y, sp.Rational(25, 100) * (360 + y)), y)[0]
    brute_360 = brute(lambda v: salt(360, v) == F(25, 100) * (360 + v), 0, 2000)
    num(L, 'p-salt-solutions', 4, 360 + y360, 360 + brute_360[0],
        {'stopped': y360, 'reversed': 360 + F(3, 2) * 360, 'added': 500 + 360 - 300})
    stated('salt: 2/3 x 360', 240, F(2, 3) * 360)
    stated('salt: 54 + 96', 150, salt(360, 240))
    stated('salt: 25% of 600', 150, F(25, 100) * 600)


def run_level4():
    """run_level for set 4: the same checks, with form_stated reading a numeric `answers` set (cars part 1) value by value."""
    items = load(4)
    if items is None:
        return
    level4(items)
    for iid, it in items.items():
        for k, part in enumerate(it['parts'], 1):
            w = part['widget']
            vals = w.get('answers', [w.get('answer')]) if w['kind'] == 'numeric' else []
            if any(not float(v).is_integer() for v in vals):
                ok(re.search(r'decimal|places?|fraction|nearest|per cent|percentage|in pounds|in pence|%', part['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')
            if w['kind'] == 'numeric':
                ok(re.search(r'in (km/h|hours|metres|seconds|grams)|how many|values of', part['question'], re.I) is not None,
                   f'{iid} p{k}: unit or count not named')
    typed = sum(1 for it in items.values() for p in it['parts'] if p['widget']['kind'] in ('numeric', 'expression'))
    total = sum(len(it['parts']) for it in items.values())
    ok(3 * typed >= 2 * total, f'level 4: typed parts {typed} of {total}, under two thirds')
    ok(any(it['difficulty'] == 5 for it in items.values()), 'level 4: no difficulty 5')
    ok(all(3 <= it['difficulty'] <= 5 and 3 <= len(it['parts']) <= 5 for it in items.values()), 'level 4: difficulty or part count')
    lv = Level('equations', 4)
    lv.check_wrongs('problems')
    bad = [rr for rr in lv.results if not rr[0]]
    ok(not bad, f'level 4: numbers_lib check_wrongs failures {bad}')


run_level(1, level1)
run_level(2, level2)
run_level(3, level3)
run_level4()

present = [n for n in (1, 2, 3, 4) if load(n) is not None]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
