"""Second read, problems 0.2 (a): the reader's own answers for equations 1 to 3 and functions 1 to 3.

Each part was solved from its text before its key was read. Here every part is worked twice (sympy exact, then a second
route: plain arithmetic from the story, a brute-force count, a root finder or a grid), and compared with the key and its band.
Every wrong[] value is rebuilt from the slip its feedback line names. Expression keys, accept forms and wrong[].tex are
compared with the reader's own sympy expression (equations and inequalities by their solution sets).
Claims in feedback and explanations that go beyond the key are checked at the end.

Run from the repo root with the scratchpad venv python. Exit 0 when every check holds.
"""
import json
import re
import sys
from fractions import Fraction as Fr

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                        standard_transformations)

TR = standard_transformations + (implicit_multiplication_application, convert_xor)
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def load(course, n):
    return {it['id']: it for it in json.load(open(f'app/content/courses/{course}/problems-{n}.json'))['items']}


def tex2sym(t, names):
    t = t.replace('\\left', '').replace('\\right', '').replace('\\times', '*').replace('\\cdot', '*').replace('\\,', '')
    while '\\frac' in t:
        t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    t = t.replace('{', '(').replace('}', ')')
    loc = {k: sp.Symbol(k) for k in names}
    return parse_expr(t, local_dict=loc, transformations=TR)


REL = re.compile(r'\\geq?|\\leq?|>=|<=|=|<|>')


def rel(t, names):
    """An equation or inequality as (kind, lhs - rhs) with kind in eq, le, lt (ge and gt turned round)."""
    m = REL.search(t)
    l, r, k = t[:m.start()], t[m.end():], m.group(0)
    d = tex2sym(l, names) - tex2sym(r, names)
    k = {'=': 'eq', '\\le': 'le', '\\leq': 'le', '<=': 'le', '<': 'lt', '\\ge': 'ge', '\\geq': 'ge', '>=': 'ge', '>': 'gt'}[k]
    if k in ('ge', 'gt'):
        d, k = -d, {'ge': 'le', 'gt': 'lt'}[k]
    return k, sp.expand(d)


def same_rel(a, b, names):
    (ka, da), (kb, db) = rel(a, names), rel(b, names)
    if ka != kb:
        return False
    q = sp.simplify(da / db)
    return q.is_number and (q != 0) and (ka == 'eq' or q > 0)


def same(a, b, names):
    if REL.search(a) or REL.search(b):
        return bool(REL.search(a) and REL.search(b)) and same_rel(a, b, names)
    return sp.simplify(tex2sym(a, names) - tex2sym(b, names)) == 0


def band(w):
    return (w.get('tol') or {}).get('abs', 0)


def num(part, mine, second, slips=None, label=''):
    """mine and second: the reader's two values; slips: id -> value rebuilt from the named slip."""
    w = part['widget']
    if 'answers' in w:
        ok(sorted(map(Fr, map(str, w['answers']))) == sorted(Fr(str(x)) for x in mine), f'{label}: set key {w["answers"]} vs mine {mine}')
        ok(sorted(float(x) for x in mine) == sorted(float(x) for x in second), f'{label}: second route {second}')
        for x in w.get('wrong', []):
            got = sorted(float(v) for v in str(x['value']).split(','))
            ok(x['id'] in (slips or {}), f'{label}: slip {x["id"]} not rebuilt')
            if slips and x['id'] in slips:
                ok(got == sorted(float(v) for v in slips[x['id']]), f'{label}: slip {x["id"]} key {got} vs mine {slips[x["id"]]}')
            ok(got != sorted(float(v) for v in mine), f'{label}: slip {x["id"]} equals the answer')
        return
    ok(abs(float(mine) - w['answer']) <= band(w) + 1e-9, f'{label}: key {w["answer"]} vs mine {float(mine)}')
    ok(abs(float(mine) - float(second)) < 1e-6, f'{label}: second route {float(second)} vs {float(mine)}')
    for x in w.get('wrong', []):
        ok(x['id'] in (slips or {}), f'{label}: slip {x["id"]} not rebuilt')
        if slips and x['id'] in slips:
            ok(abs(float(slips[x['id']]) - x['value']) <= band(x) + 1e-9, f'{label}: slip {x["id"]} key {x["value"]} vs mine {float(slips[x["id"]])}')
        ok(abs(x['value'] - w['answer']) > band(w) + band(x), f'{label}: slip {x["id"]} band meets the answer band')
    ws = w.get('wrong', [])
    for i, x in enumerate(ws):
        for y in ws[i + 1:]:
            ok(abs(x['value'] - y['value']) > band(x) + band(y), f'{label}: slips {x["id"]} and {y["id"]} overlap')


def expr(part, mine, names, slips=None, label=''):
    w = part['widget']
    for f in [w['answer']] + list(w.get('accept', [])):
        ok(same(f, mine, names), f'{label}: key form {f} vs mine {mine}')
    for x in w.get('wrong', []):
        ok(not same(x['tex'], mine, names), f'{label}: wrong {x["id"]} equals the answer')
        ok(x['id'] in (slips or {}), f'{label}: slip {x["id"]} not rebuilt')
        if slips and x['id'] in slips:
            ok(same(x['tex'], slips[x['id']], names), f'{label}: slip {x["id"]} key {x["tex"]} vs mine {slips[x["id"]]}')


def choice(part, right, label=''):
    c = [o['id'] for o in part['widget']['options'] if o.get('correct')]
    ok(c == [right], f'{label}: keyed {c}, mine {right}')
    ok(all('why' in o for o in part['widget']['options'] if not o.get('correct')), f'{label}: an option has no why')


# ---------------------------------------------------------------- equations 1
S = load('equations', 1)
P = S['p-family-tickets']['parts']
a = sp.Symbol('a')
bill = sp.expand(2 * a + 3 * (a - 5))
expr(P[0], 'a-5', 'a', {'reversed': '5-a', 'times': '5a'}, 'tickets 1')
ok(bill == 5 * a - 15, 'tickets 2 bill')
expr(P[1], '5a-15', 'a', {'three-reach': '2a+3a-5', 'sign': '2a+3a+15', 'carried': '2a+3(5-a)'}, 'tickets 2')
ok(sp.factor_list(bill) == (5, [(a - 3, 1)]), 'tickets 3 factor')
expr(P[2], '5(a-3)', 'a', {'one-term': '5(a-15)', 'sign': '5(a+3)'}, 'tickets 3')
num(P[3], bill.subs(a, 18), 2 * 18 + 3 * 13, {'five-off': 5 * 18 - 5, 'sign': 5 * (18 + 3), 'no-child': 5 * 18}, 'tickets 4')

P = S['p-food-van']['parts']
n = sp.Symbol('n')
sat = sp.nsimplify(6.5) * n - sp.nsimplify(2.3) * n - 45
sun = sp.expand(sp.Rational(42, 10) * (n - 20) - 45)
expr(P[0], '4.2n-45', 'n', {'no-cost': '6.5n-45', 'added-cost': '6.5n+2.3n-45'}, 'van 1')
ok(sp.simplify(sat - (sp.Rational(42, 10) * n - 45)) == 0, 'van 1 sympy')
expr(P[1], '4.2n-129', 'n', {'twenty-reach': '4.2n-20-45', 'sign': '4.2n+84-45'}, 'van 2')
ok(sun == sp.Rational(42, 10) * n - 129, 'van 2 sympy')
expr(P[2], '8.4n-174', 'n', {'carried': '4.2n-45+4.2n-65', 'one-pitch': '8.4n-129'}, 'van 3')
wk = sat + sun
by_days = (6.5 - 2.3) * 90 - 45 + (6.5 - 2.3) * 70 - 45
num(P[3], wk.subs(n, 90), by_days, {'carried': 8.4 * 90 - 110, 'one-pitch': 8.4 * 90 - 129, 'sunday': 8.4 * 70 - 174}, 'van 4')
ok(abs((4.2 * 90 - 45) - 333) < 1e-9 and abs((4.2 * 70 - 45) - 249) < 1e-9, 'van 4 check by days 333 and 249')

P = S['p-number-trick']['parts']
mia = sp.expand(5 * (n + 4) - 3 * (n - 2))
expr(P[0], '2n+26', 'n', {'sign': '5n+20-3n-6', 'five-reach': '5n+4-3n+6'}, 'trick 1')
ok(mia == 2 * n + 26, 'trick 1 sympy')
expr(P[1], '2(n+13)', 'n', {'one-term': '2(n+26)', 'letter': '2n(1+13)'}, 'trick 2')
num(P[2], mia.subs(n, 7), 5 * 11 - 3 * 5, {'sign': 2 * 7 + 14, 'one-term': 2 * (7 + 26), 'letter': 28 * 7, 'half': 2 * 7 + 13}, 'trick 3')
choice(P[3], 'same', 'trick 4')
ok(sp.expand(2 * (n + 9) + 8) == mia, 'trick 4 Leo equals Mia for every n')
ok(2 * (7 + 9) + 8 == 40, 'trick 4 Leo at 7')

P = S['p-market-pitch']['parts']
s = sp.Symbol('s')
corner = sp.expand(s * (s + 2))
tot = sp.expand(3 * corner + 4 * s**2)
expr(P[0], 's^2+2s', 's', {'two-reach': 's^2+2', 'doubled': '2s+2s'}, 'pitch 1')
expr(P[1], '7s^2+6s', 's', {'three-reach': '3s^2+2s+4s^2', 'unlike': '13s^2', 'carried': '3(s^2+2)+4s^2'}, 'pitch 2')
ok(tot == 7 * s**2 + 6 * s, 'pitch 2 sympy')
expr(P[2], 's(7s+6)', 's', {'square-out': 's^2(7+6)', 'seven-out': '7s(s+6)'}, 'pitch 3')
ok(sp.factor(tot) == s * (7 * s + 6), 'pitch 3 sympy')
num(P[3], tot.subs(s, 4), 4 * 16 + 3 * (4 * 6), {'squared-last': (7 * 4)**2 + 24, 'doubled': 7 * 8 + 24, 'three-reach': 7 * 16 + 2 * 4}, 'pitch 4')

# ---------------------------------------------------------------- equations 2
S = load('equations', 2)
P = S['p-climbing-wall']['parts']
c = sp.Symbol('c')
expr(P[0], '45+8c=213', 'c', {'added': '(45+8)c=213', 'swapped': '8+45c=213', 'fee-side': '8c=213+45'}, 'wall 1')
num(P[1], sp.solve(45 + 8 * c - 213, c)[0], (213 - 45) / 8, {'no-fee': 213 / 8, 'add-fee': (213 + 45) / 8}, 'wall 2')
most = max(k for k in range(200) if 45 + 8 * k <= 300)
num(P[2], sp.floor(sp.Rational(300 - 45, 8)), most, {'rounded-up': 32, 'no-fee': 300 // 8}, 'wall 3')
ok(45 + 8 * 32 == 301 and 45 + 8 * 31 == 293, 'wall 3 costs 301 and 293')
pence = max(p for p in range(2000) if 4500 + 35 * p <= 30000)
num(P[3], Fr(pence, 100), sp.floor(sp.Rational(25500, 35)) / 100, {'rounded-up': 7.29, 'no-fee': 300 / 35}, 'wall 4')
ok(round(45 + 35 * 7.29, 2) == 300.15 and round(45 + 35 * 7.28, 2) == 299.80, 'wall 4 costs 300.15 and 299.80')

P = S['p-cottage-share']['parts']
x = sp.Symbol('x')
expr(P[0], '\\frac{x}{5}-20=\\frac{x+30}{6}', 'x', {'plus': '\\frac{x}{5}+20=\\frac{x+30}{6}', 'bed-each': '\\frac{x}{5}-20=\\frac{x}{6}+30', 'no-bed': '\\frac{x}{5}-20=\\frac{x}{6}'}, 'cottage 1')
X = sp.solve(x / 5 - 20 - (x + 30) / 6, x)[0]
brute = [v for v in range(0, 5000, 10) if Fr(v, 5) - 20 == Fr(v + 30, 6)]
num(P[1], X, brute[0], {'lone-twenty': sp.solve(6 * x - 20 - 5 * (x + 30), x)[0], 'top': sp.solve(6 * x - 600 - (5 * x + 30), x)[0], 'carried-plus': sp.solve(x / 5 + 20 - (x + 30) / 6, x)[0]}, 'cottage 2')
ok(len(brute) == 1, 'cottage 2 one solution')
num(P[2], (X + 30) / 6, 750 / 5 - 20, {'no-bed': 750 / 6, 'old-share': 750 / 5}, 'cottage 3')
num(P[3], sp.Rational(810, 7), 780 / 7 + 30 / 7, {'no-bed': 780 / 7, 'six': 810 / 6}, 'cottage 4')
ok(round(130 - 810 / 7, 2) == 14.29, 'cottage 4 the share falls by about 14.29')

P = S['p-power-tariffs']['parts']
u = sp.Symbol('u')
num(P[0], sp.Rational(216, 30), 216 / 30, {'times': 216 * 30, 'minus': 216 - 30}, 'tariff 1')
U = sp.solve(45 + 24 * u - 30 * u, u)[0]
num(P[1], U, 45 / (30 - 24), {'one-rate': 45 / 24, 'added': 45 / 54, 'sign': -7.5}, 'tariff 2')
ok(45 + 24 * 7.5 == 225 == 30 * 7.5, 'tariff 2 both 225p')
choice(P[2], 'b', 'tariff 3')
ok(abs(45 + 24 * 7.2 - 217.8) < 1e-9 and 30 * 7.2 == 216 and all(45 + 24 * v > 30 * v for v in [0, 1, 5, 7.2, 7.49]), 'tariff 3 B cheaper below 7.5')
num(P[3], 30 * 9 - (45 + 24 * 9), 6 * (9 - 7.5), {'unit-gap': 9 - 7.5, 'no-charge': 30 * 9 - 24 * 9}, 'tariff 4')

P = S['p-interest-split']['parts']
sv = sp.Symbol('s')
expr(P[0], '12000-s', 's', {'reversed': 's-12000', 'added': '12000+s'}, 'interest 1')
expr(P[1], '0.04s+0.065(12000-s)=660', 's', {'no-minus': '0.04s+0.065*12000=660', 'per-cent': '4s+6.5(12000-s)=660'}, 'interest 2')
eq = sp.Rational(4, 100) * sv + sp.Rational(65, 1000) * (12000 - sv)
Sv = sp.solve(eq - 660, sv)[0]
grid = [v for v in range(0, 12001, 100) if abs(0.04 * v + 0.065 * (12000 - v) - 660) < 1e-9]
num(P[2], Sv, grid[0], {'sign': -4800, 'bracket-sign': sp.solve(40 * sv + 780000 + 65 * sv - 660000, sv)[0], 'rhs': sp.solve(40 * sv + 780000 - 65 * sv - 660, sv)[0]}, 'interest 3')
ok(0.04 * 4800 == 192 and abs(0.065 * 7200 - 468) < 1e-9, 'interest 3 check 192 + 468')
ok(sp.expand(eq) == 780 - sp.Rational(25, 1000) * sv, 'interest 4 the given 780 - 0.025s')
S4 = sp.solve(eq - 720, sv)[0]
num(P[3], S4, 60 / 0.025, {'sign': -2400, 'added': (720 + 780) / 0.025, 'old': 4800}, 'interest 4')
ok(0.04 * 2400 == 96 and abs(0.065 * 9600 - 624) < 1e-9, 'interest 4 check 96 + 624')

# ---------------------------------------------------------------- equations 3
S = load('equations', 3)
P = S['p-bakery-stock']['parts']
h = sp.Symbol('h', real=True)
expr(P[0], '240-18h\\ge60', 'h', {'strict': '240-18h>60', 'reversed': '240-18h\\le60', 'plus': '240+18h\\ge60'}, 'bakery 1')
ok(sp.solve_univariate_inequality(240 - 18 * h >= 60, h, relational=False) == sp.Interval(-sp.oo, 10), 'bakery 2 sympy')
ok([k for k in range(0, 30) if 240 - 18 * k >= 60] == list(range(0, 11)), 'bakery 2 brute')
expr(P[1], 'h\\le10', 'h', {'no-flip': 'h\\ge10', 'added': '18h\\le240+60', 'negative': 'h\\le-10'}, 'bakery 2')
choice(P[2], 'filled-left', 'bakery 3')
cnt = [k for k in range(0, 30) if k > 4 and 240 - 18 * k >= 60]
num(P[3], len(cnt), 10 - 4, {'with-four': len(cnt) + 1, 'no-ten': len(cnt) - 1}, 'bakery 4')

P = S['p-fridge-temperature']['parts']
F_, C_ = sp.symbols('F C')
inv = sp.solve(sp.Eq(F_, sp.Rational(18, 10) * C_ + 32), C_)[0]
expr(P[0], '\\frac{F-32}{1.8}', 'F', {'order': '\\frac{F}{1.8}-32', 'sign': '\\frac{F+32}{1.8}', 'times': '1.8(F-32)'}, 'fridge 1')
ok(sp.simplify(inv - (F_ - 32) / sp.Rational(18, 10)) == 0 and inv.subs(F_, 212) == 100, 'fridge 1 sympy and 212 gives 100')
num(P[1], inv.subs(F_, 41), (41 - 32) / 1.8, {'order': 41 / 1.8 - 32, 'sign': (41 + 32) / 1.8, 'times': 1.8 * (41 - 32)}, 'fridge 2')
expr(P[2], 'F\\le41', 'F', {'reversed': 'F\\ge41', 'stopped': 'F\\le9'}, 'fridge 3')
ok([k for k in range(-100, 100) if (k - 32) / 1.8 <= 5 + 1e-12][-1] == 41, 'fridge 3 brute')
lo, hi = 1.8 * -25 + 32, 1.8 * -15 + 32
okF = [k for k in range(-200, 200) if -25 - 1e-9 <= (k - 32) / 1.8 <= -15 + 1e-9]
num(P[3], len(okF), round(hi - lo) + 1, {'gap': round(hi - lo), 'celsius': 11, 'both-out': round(hi - lo) - 1}, 'fridge 4')
ok((round(lo), round(hi)) == (-13, 5), 'fridge 4 limits -13 and 5')

P = S['p-van-value']['parts']
Pp, V, k, t = sp.symbols('P V k t')
tt = sp.solve(sp.Eq(V, Pp - k * t), t)[0]
expr(P[0], '\\frac{P-V}{k}', 'PVk', {'sign': '\\frac{V-P}{k}', 'top': '\\frac{P}{k}-V', 'not-gathered': 'P-\\frac{V}{k}'}, 'value 1')
ok(sp.simplify(tt - (Pp - V) / k) == 0, 'value 1 sympy')
num(P[1], tt.subs({Pp: 24000, V: 9600, k: 2400}), next(y for y in range(40) if 24000 - 2400 * y == 9600), {'value-only': 9600 / 2400, 'sign': -6, 'added': (24000 + 9600) / 2400}, 'value 2')
expr(P[2], 't<7.5', 't', {'no-flip': 't>7.5', 'added': '2400t<24000+6000', 'value-only': 't<6000/2400'}, 'value 3')
ok(all((24000 - 2400 * y > 6000) == (y < 7.5) for y in [v / 4 for v in range(0, 60)]), 'value 3 brute')
choice(P[3], 'right', 'value 4')
ok(all((6000 < 24000 - 2400 * y <= 19200) == (2 <= y < 7.5) for y in [v / 4 for v in range(0, 60)]), 'value 4 brute')
yrs = [y for y in range(0, 40) if 6000 < 24000 - 2400 * y <= 19200]
num(P[4], len(yrs), 7 - 2 + 1, {'no-two': 5, 'rounded-up': 7}, 'value 5')

P = S['p-fund-weight']['parts']
aa, b, w = sp.symbols('a b w')
A = sp.solve(sp.Eq(w, aa / (aa + b)), aa)[0]
expr(P[0], '\\frac{wb}{1-w}', 'wba', {'sign': '\\frac{wb}{1+w}', 'dropped': 'wb', 'not-alone': 'w(a+b)'}, 'fund 1')
ok(sp.simplify(A - w * b / (1 - w)) == 0, 'fund 1 sympy')
a2 = A.subs({w: sp.Rational(4, 10), b: 6000})
num(P[1], a2, next(v for v in range(0, 20000, 50) if Fr(v, v + 6000) == Fr(4, 10)), {'dropped': 0.4 * 6000, 'sign': 0.4 * 6000 / 1.4}, 'fund 2')
a3 = A.subs({w: sp.Rational(1, 4), b: 6000})
least = min(v for v in range(0, 20000, 50) if Fr(1, 4) <= Fr(v, v + 6000) <= Fr(4, 10))
num(P[2], a3, least, {'dropped': 0.25 * 6000, 'sign': 0.25 * 6000 / 1.25}, 'fund 3')
ok(sp.diff(A, w).subs(b, 6000).subs(w, 0.3) > 0, 'fund 3 a rises with w')
ns = [q for q in range(0, 100) if 2000 <= 250 * q <= 4000]
num(P[3], len(ns), 16 - 8 + 1, {'gap': 8, 'both-out': 7}, 'fund 4')

# ---------------------------------------------------------------- functions 1
S = load('functions', 1)
P = S['p-exchange-kiosk']['parts']
xs = sp.Symbol('x')
m = sp.Rational(89 - 43, 80 - 40)
cc = 43 - m * 40
E = m * xs + cc
ok([E.subs(xs, v) for v in (40, 80, 120)] == [43, 89, 135], 'kiosk rule fits all three rows')
num(P[0], m, (135 - 89) / 40, {'per-row': 46, 'first-row': 43 / 40, 'flipped': 40 / 46}, 'kiosk 1')
expr(P[1], '1.15x-3', 'x', {'no-fee': '1.15x', 'plus-fee': '1.15x+3', 'first-row': '1.15x+43', 'per-row': '46x+(43-46*40)'}, 'kiosk 2')
num(P[2], E.subs(xs, 300), 1.15 * 300 - 3, {'no-fee': 345, 'plus-fee': 348}, 'kiosk 3')
num(P[3], sp.solve(E - 227, xs)[0], (227 + 3) / 1.15, {'minus-fee': (227 - 3) / 1.15, 'no-fee': 227 / 1.15, 'forward': 1.15 * 227 - 3}, 'kiosk 4')

P = S['p-van-fuel']['parts']
d = sp.Symbol('d')
Fd = 60 - sp.Rational(15, 100) * d
num(P[0], Fd.subs(d, 120), 60 - 0.15 * 120, {'added': 60 + 18, 'used': 18}, 'fuel 1')
num(P[1], sp.solve(Fd, d)[0], 60 / 0.15, {'times': 60 * 0.15}, 'fuel 2')
choice(P[2], 'closed', 'fuel 3')
g = [float(Fd.subs(d, v)) for v in range(0, 401)]
num(P[3], [0, 60], [min(g), max(g)], {'domain': [0, 400], 'part-one': [42, 60]}, 'fuel 4')
g = [float(Fd.subs(d, v)) for v in range(80, 241)]
num(P[4], [Fd.subs(d, 240), Fd.subs(d, 80)], [min(g), max(g)], {'used': [12, 36], 'whole': [0, 60]}, 'fuel 5')

P = S['p-stone-throw']['parts']
hh = lambda v: 45 - 5 * (v - 2)**2
num(P[0], hh(0), 45 - 20, {'neg-square': 45 - 5 * (-4), 'no-square': 45 - 5 * (-2), 'whole-square': 45 - (5 * -2)**2}, 'stone 1')
roots = sorted(sp.solve(hh(t), t))
ok(roots == [-1, 5], 'stone 2 roots')
num(P[1], roots[1], next(v for v in range(1, 50) if hh(v) == 0), {'other-root': roots[0], 'no-root': 2 + 9, 'no-two': 3}, 'stone 2')
g = [hh(v / 100) for v in range(0, 501)]
num(P[2], [0, 45], [min(g), max(g)], {'ends': [hh(5), hh(0)], 'domain': [0, 5]}, 'stone 3')
ok(hh(2) == 45, 'stone 3 top at t = 2')
r40 = sorted(sp.solve(hh(t) - 40, t))
num(P[3], r40, [v / 100 for v in range(0, 501) if abs(hh(v / 100) - 40) < 1e-9], {'signs': sorted(sp.solve(45 - 5 * (t + 2)**2 - 40, t)), 'no-five': roots}, 'stone 4')
choice(P[4], 'two-times', 'stone 5')
ok(len([v for v in range(0, 501) if abs(hh(v / 100) - 45) < 1e-9]) == 1, 'stone 5: 45 is reached once')

P = S['p-sapling-log']['parts']
choice(P[0], 'clash', 'sapling 1')
rows = [(1, 17), (3, 27), (4, 32), (6, 42)]
slopes = {Fr(y2 - y1, x2 - x1) for (x1, y1) in rows for (x2, y2) in rows if x1 != x2}
ok(slopes == {5}, 'sapling 2 every pair of rows gives 5')
num(P[1], 5, (42 - 32) / 2, {'per-row': 10, 'with-29': (29 - 17) / 2, 'height-over-week': 17}, 'sapling 2')
wv = sp.Symbol('w')
expr(P[2], '5w+12', 'w', {'first-row': '5w+17', 'no-c': '5w', 'per-row': '10w+(17-10)'}, 'sapling 3')
ok(all(5 * a_ + 12 == b_ for a_, b_ in rows), 'sapling 3 fits the four rows')
num(P[3], sp.solve(5 * wv + 12 - 72, wv)[0], (72 - 12) / 5, {'first-row': (72 - 17) / 5, 'no-c': 72 / 5, 'forward': 5 * 72 + 12, 'per-row': (72 - 7) / 10}, 'sapling 4')

# ---------------------------------------------------------------- functions 2
S = load('functions', 2)
P = S['p-candle-burn']['parts']
m = sp.Rational(135 - 210, 10) / (5 - 2)
num(P[0], m, (13.5 - 21) / 3, {'sign': 2.5, 'flipped': 3 / -7.5, 'no-run': -7.5}, 'candle 1')
c0 = 21 - m * 2
num(P[1], c0, 13.5 + 2.5 * 5, {'sign': 21 - 5, 'first-point': 21, 'one-hour': 21 + 2.5}, 'candle 2')
num(P[2], sp.solve(c0 + m * t, t)[0], 26 / 2.5, {'sixteen': 16 / 2.5, 'times': 26 * 2.5, 'flipped': 2.5 / 26}, 'candle 3')
ok(abs(0.4 * 60 - 24) < 1e-9, 'candle 3: 10.4 h is 10 h 24 min')
choice(P[3], 't-axis', 'candle 4')

P = S['p-path-and-pipe']['parts']
A_, B_, D_ = (-2, 1), (4, 4), (5, -3)
m1 = Fr(B_[1] - A_[1], B_[0] - A_[0])
num(P[0], m1, 3 / 6, {'flipped': 2, 'lost-minus': 3 / (4 - 2)}, 'path 1')
c1 = A_[1] - m1 * A_[0]
ok(m1 * B_[0] + c1 == B_[1], 'path 2 fits B')
expr(P[1], '0.5x+2', 'x', {'c-first': '0.5x+1', 'sign': '0.5x', 'flipped': '2x+(1+4)'}, 'path 2')
m2 = -1 / m1
num(P[2], m2, -1 / 0.5, {'reciprocal': 2, 'negative': -0.5, 'same': 0.5}, 'path 3')
c2 = D_[1] - m2 * D_[0]
expr(P[3], '-2x+7', 'x', {'c-first': '-2x-3', 'sign': '-2x+(-3-10)', 'reciprocal': '2x+(-3-10)'}, 'path 4')
ok(c2 == 7, 'path 4 intercept')
X0 = sp.solve(sp.Rational(1, 2) * xs + 2 - (-2 * xs + 7), xs)[0]
# second route: foot of the perpendicular from D to AB by projection
ux, uy = B_[0] - A_[0], B_[1] - A_[1]
tproj = Fr((D_[0] - A_[0]) * ux + (D_[1] - A_[1]) * uy, ux * ux + uy * uy)
foot = (A_[0] + tproj * ux, A_[1] + tproj * uy)
ok(foot == (2, 3), f'path 5 foot of the perpendicular {foot}')
num(P[4], X0, foot[0], {'y-value': 3, 'sign-x': 5 / (0.5 - 2), 'constants': 9 / 2.5}, 'path 5')

P = S['p-two-gyms']['parts']
mB = Fr(194 - 104, 8 - 3)
num(P[0], mB, 90 / 5, {'no-run': 90, 'one-point': 104 / 3}, 'gyms 1')
cB = 104 - mB * 3
num(P[1], cB, 194 - 18 * 8, {'first-point': 104, 'sign': 104 + 54, 'no-run': 104 - 90 * 3}, 'gyms 2')
meet = sp.solve(24 * xs + 20 - (18 * xs + 50), xs)[0]
num(P[2], meet, next(v for v in range(1, 100) if 24 * v + 20 == 18 * v + 50), {'fee-gap': 30, 'fees-sum': 70 / 6}, 'gyms 3')
ok(24 * 5 + 20 == 140 == 18 * 5 + 50, 'gyms 3 both 140')
num(P[3], (24 * 12 + 20) - (18 * 12 + 50), 6 * (12 - 5), {'rates-only': 6 * 12, 'gym-b': 266, 'gym-a': 308}, 'gyms 4')
ok(all(24 * v + 20 > 18 * v + 50 for v in range(6, 200)), 'gyms 4 B cheaper after month 5')

P = S['p-two-savers']['parts']
num(P[0], 15 * 6 + 40, 40 + 6 * 15, {'no-start': 90, 'swapped': 40 * 6 + 15}, 'savers 1')
mb = Fr(110 - 50, 6 - 2)
num(P[1], mb, 60 / 4, {'no-run': 60, 'one-point': 50 / 2}, 'savers 2')
num(P[2], 50 - mb * 2, 110 - 15 * 6, {'first-point': 50, 'sign': 50 + 30, 'one-point': 50 - 25 * 2}, 'savers 3')
choice(P[3], 'never', 'savers 4')
ok(sp.solve(15 * xs + 40 - (15 * xs + 20), xs) == [], 'savers 4 no meeting point')

# ---------------------------------------------------------------- functions 3
S = load('functions', 3)
P = S['p-bakery-trays']['parts']
Pf = -5 * xs**2 + 60 * xs - 100
num(P[0], Pf.subs(xs, 0), -100, {'sign': 100, 'zero': 0}, 'trays 1')
ok(sp.expand(-5 * (xs - 2) * (xs - 10)) == Pf, 'trays 2 the factorised form is the rule')
num(P[1], sorted(sp.solve(Pf, xs)), [v for v in range(-50, 50) if Pf.subs(xs, v) == 0], {'signs': [-2, -10], 'fives': [-5, 2]}, 'trays 2')
tp = sp.solve(sp.diff(Pf, xs), xs)[0]
num(P[2], tp, (2 + 10) / 2, {'half-top': 10 / 2, 'half-gap': (10 - 2) / 2}, 'trays 3')
num(P[3], Pf.subs(xs, tp), max(Pf.subs(xs, v) for v in range(0, 13)), {'from-five': Pf.subs(xs, 5), 'from-four': Pf.subs(xs, 4), 'sign-square': 5 * 36 + 360 - 100}, 'trays 4')
choice(P[4], 'left', 'trays 5')
ok(all(Pf.subs(xs, v + 1) > Pf.subs(xs, v) for v in range(-5, 6)) and all(Pf.subs(xs, v + 1) < Pf.subs(xs, v) for v in range(6, 15)), 'trays 5 rises to 6, falls after')
ok(Pf.subs(xs, 11) < 0 and Pf.subs(xs, 12) < Pf.subs(xs, 11), 'trays 5 past 10 negative and falling')

P = S['p-sledge-cyclist']['parts']
sl = lambda v: 0.5 * v**2
num(P[0], sp.Rational(1, 2) * 16, sl(4), {'no-square': 0.5 * 4, 'whole-square': (0.5 * 4)**2, 'no-half': 16}, 'sledge 1')
num(P[1], sp.Rational(8, 4), sl(4) / 4, {'times': 32, 'distance': 8}, 'sledge 2')
r = sorted(sp.solve(sp.Rational(1, 2) * t**2 - 3 * t, t))
ok(r == [0, 6], 'sledge 3 roots 0 and 6')
num(P[2], r[1], next(v for v in range(1, 100) if sl(v) == 3 * v), {'no-half': 3, 'lost-t': 6**0.5}, 'sledge 3')
num(P[3], 3 * 6, sl(6), {'from-three': 9, 'no-half': 36}, 'sledge 4')
choice(P[4], 'sledge', 'sledge 5')
ok(sp.diff(sp.Rational(1, 2) * t**2, t).subs(t, 6) == 6 > 3, 'sledge 5 speed 6 m/s at t = 6')
ok(all(3 * v / 10 > sl(v / 10) for v in range(1, 60)), 'sledge 5 the cyclist is ahead for 0 < t < 6')

P = S['p-two-cultures']['parts']
N = lambda v: 200 * 2**v
M = lambda v: 1000 + 300 * v
num(P[0], 200 * 2**3, 200 * 2 * 2 * 2, {'times-three': 200 * 2 * 3, 'two-doublings': 800}, 'cultures 1')
num(P[1], M(3) - N(3), 1900 - 1600, {'m-value': 1900, 'from-1200': 1900 - 1200}, 'cultures 2')
choice(P[2], 'once', 'cultures 3')
ok((N(4), M(4)) == (3200, 2200), 'cultures 3 values at 4 hours')
signs = [N(v / 1000) > M(v / 1000) for v in range(0, 20001)]
ok(sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1]) == 1, 'cultures 3 one crossing on 0 to 20 hours')
root = float(sp.nsolve(200 * 2**t - 1000 - 300 * t, t, 3.3))
lo_, hi_ = 3.0, 4.0
for _ in range(60):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if N(mid) < M(mid) else (lo_, mid)
ok(abs(root - lo_) < 1e-9 and round(root, 2) == 3.32, f'cultures 4 crossing {root}')
num(P[3], round(root, 1), round(lo_, 1), {'midway': 3.5, 'whole-hour': 3, 'too-late': 3.4}, 'cultures 4')
ok(round(N(3.3)) == 1970 and M(3.3) == 1990 and round(N(3.4)) == 2111 and M(3.4) == 2020, 'cultures 4 the four printed values')
ok(round(M(3.3) - N(3.3), -1) == 20 and round(N(3.4) - M(3.4), -1) == 90, 'cultures 4 leads of about 20 and about 90')
num(P[4], round(M(3.3), -2), round(N(root), -2), {'at-three': M(3), 'at-four': M(4), 'n-at-three': N(3)}, 'cultures 5')

P = S['p-track-cubic']['parts']
hc = xs**3 - 6 * xs**2 + 9 * xs
num(P[0], hc.subs(xs, 2), 8 - 24 + 18, {'all-plus': 8 + 24 + 18, 'cube-as-times': 6 - 24 + 18}, 'track 1')
ok(sp.expand(xs * (xs - 3)**2) == hc, 'track 2 the factorised form is the rule')
num(P[1], sorted(set(sp.solve(hc, xs))), [v / 10 for v in range(0, 41) if abs(hc.subs(xs, sp.Rational(v, 10))) == 0], {'signs': [0, -3]}, 'track 2')
ok(sorted(sp.solve(sp.diff(hc, xs), xs)) == [1, 3], 'track 3 turning points 1 and 3')
choice(P[2], 'middle', 'track 3')
vals = [float(hc.subs(xs, sp.Rational(v, 100))) for v in range(0, 401)]
ok(all(vals[i + 1] > vals[i] for i in range(0, 100)) and all(vals[i + 1] < vals[i] for i in range(100, 300)) and all(vals[i + 1] > vals[i] for i in range(300, 400)), 'track 3 up, down, up')
ok(hc.subs(xs, 4) == 4 and hc.subs(xs, 1) == 4, 'track 3 and 4: h(1) = h(4) = 4')
num(P[3], sorted(set(sp.solve(hc - 4, xs))), [v / 100 for v in range(0, 401) if abs(vals[v] - 4) < 1e-12], {'roots': [0, 3], 'turns': [1, 3]}, 'track 4')

# claims beyond the keys
ok(sp.solve(sp.diff(xs**3 + xs, xs), xs, domain=sp.S.Reals) in ([], sp.S.EmptySet) or all(not v.is_real for v in sp.solve(sp.diff(xs**3 + xs, xs), xs)),
   'x^3 + x has no turning point: "a cubic with a positive x^3 rises, turns down, then turns up again" is not true of every cubic')

print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
