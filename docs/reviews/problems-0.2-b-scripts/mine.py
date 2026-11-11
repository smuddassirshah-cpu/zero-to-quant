"""Second read, problems 0.2 (b): the reader's own answers for quadratics 1 to 3 and equations 4.

Every part is solved here from its text, exactly with sympy and again by a second route (brute force over whole numbers,
a grid, bisection, or the story's own arithmetic). Every wrong[] value is rebuilt from the slip its feedback line names.
The keys are then read from the JSON and compared: numeric answers inside the part's own band, wrong values inside the
wrong entry's band and outside the answer's, expression keys and wrong[].tex by expansion against my own expression.

Run from the repo root: <venv>/bin/python docs/reviews/problems-0.2-b-scripts/mine.py
"""
import json
import math
import sys
from fractions import Fraction as Fr

import sympy as sp

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def load(course, n):
    d = json.load(open(f'app/content/courses/{course}/problems-{n}.json'))
    return {it['id']: it for it in d['items']}


def tex(s):
    """Parse the small LaTeX these keys use into sympy."""
    import re
    t = s.replace('\\left', '').replace('\\right', '').replace('\\times', '*').replace('\\cdot', '*')
    t = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    t = t.replace('^', '**').replace('{', '(').replace('}', ')')
    t = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', t)
    t = re.sub(r'([a-zA-Z)])(\()', r'\1*\2', t)
    t = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', t)
    return sp.sympify(t, rational=True)


def same_expr(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def same_eqn(a, b):
    """Two equations by lhs - rhs: one a nonzero constant multiple of the other."""
    la, ra = a.split('=')
    lb, rb = b.split('=')
    da, db = sp.expand(tex(la) - tex(ra)), sp.expand(tex(lb) - tex(rb))
    if da == 0 or db == 0:
        return da == db
    q = sp.simplify(da / db)
    return q.is_number and q != 0


def num(part, mine, label, second=None):
    w = part['widget']
    tol = (w.get('tol') or {}).get('abs', 0)
    ok(abs(float(mine) - float(w['answer'])) <= tol + 1e-12, f'{label}: key {w["answer"]} against mine {mine}')
    if second is not None:
        ok(abs(float(second) - float(mine)) < 1e-6, f'{label}: second route {second} against {mine}')
    a = w.get('accept')
    if isinstance(a, str):
        ok(abs(float(a) - float(w['answer'])) <= tol + 1e-12, f'{label}: accept {a} outside the band')


def numset(part, mine, label, second=None):
    w = part['widget']
    tol = (w.get('tol') or {}).get('abs', 0)
    ok(len(mine) == len(w['answers']) and all(abs(float(m) - float(k)) <= tol + 1e-12 for m, k in zip(sorted(map(float, mine)), sorted(w['answers']))),
       f'{label}: keys {w["answers"]} against mine {mine}')
    if second is not None:
        ok(all(abs(float(a) - float(b)) < 1e-6 for a, b in zip(sorted(map(float, mine)), sorted(map(float, second)))), f'{label}: second route')


def wrongs(part, slips, label):
    """slips: id -> my value for the slip the feedback names (number, list for a set, sympy expr, or equation string)."""
    w = part['widget']
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(sorted(ids) == sorted(slips), f'{label}: wrong ids {ids} against mine {sorted(slips)}')
    atol = (w.get('tol') or {}).get('abs', 0)
    for x in w.get('wrong', []):
        if x['id'] not in slips:
            continue
        m = slips[x['id']]
        if 'tex' in x:
            if isinstance(m, str):
                ok(same_eqn(x['tex'], m), f'{label}: wrong {x["id"]} {x["tex"]} against {m}')
                ok(not same_eqn(x['tex'], w['answer']), f'{label}: wrong {x["id"]} equals the answer')
            else:
                ok(same_expr(tex(x['tex']), m), f'{label}: wrong {x["id"]} {x["tex"]} against {m}')
                ok(not same_expr(tex(x['tex']), tex(w['answer'])), f'{label}: wrong {x["id"]} equals the answer')
        elif isinstance(m, (list, tuple)):
            vals = sorted(float(v) for v in str(x['value']).split(','))
            ok(all(abs(a - float(b)) <= 0.006 for a, b in zip(vals, sorted(map(float, m)))), f'{label}: wrong {x["id"]} {x["value"]} against {m}')
        else:
            t = (x.get('tol') or {}).get('abs', 0)
            ok(abs(float(x['value']) - float(m)) <= t + 1e-9, f'{label}: wrong {x["id"]} {x["value"]} against mine {m}')
            ok(abs(float(x['value']) - float(w['answer'])) > atol + t, f'{label}: wrong {x["id"]} band meets the answer band')


def expr(part, mine, label, accept_all=True):
    w = part['widget']
    for f in [w['answer']] + (w.get('accept') or []):
        if '=' in f:
            ok(same_eqn(f, mine), f'{label}: form {f} against {mine}')
        else:
            ok(same_expr(tex(f), mine), f'{label}: form {f} against {mine}')


def bisect(f, a, b):
    fa = f(a)
    for _ in range(200):
        m = (a + b) / 2
        if (f(m) > 0) == (fa > 0):
            a = m
        else:
            b = m
    return (a + b) / 2


x, t, n, p, v, b, c, y = sp.symbols('x t n p v b c y')

# ---------------------------------------------------------------- quadratics 1
S = load('quadratics', 1)
P = S['p-cinema-block']['parts']
seats = sp.expand((x + 3) * (x + 8))
ok(all(sum(1 for r in range(k + 3) for s in range(k + 8)) == seats.subs(x, k) for k in range(1, 30)), 'cinema: seat count by counting')
expr(P[0], seats, 'cinema 1')
wrongs(P[0], {'corner': x**2 + 24, 'added': x**2 + 11 * x + 11, 'swapped': x**2 + 24 * x + 11}, 'cinema 1')
ok(sp.factor(seats - 6) == (x + 2) * (x + 9), 'cinema 2: my factorisation')
ok([(a, 18 // a) for a in range(1, 5) if 18 % a == 0] == [(1, 18), (2, 9), (3, 6)], 'cinema 2: the pairs of 18')
expr(P[1], seats - 6, 'cinema 2')
wrongs(P[1], {'sum-nine': (x + 3) * (x + 6), 'one-eighteen': (x + 1) * (x + 18), 'signs': (x - 2) * (x - 9)}, 'cinema 2')
num(P[2], 12 * 19, 'cinema 3', (seats - 6).subs(x, 10))
wrongs(P[2], {'kept': seats.subs(x, 10), 'sum-nine': 13 * 16, 'one-eighteen': 11 * 28}, 'cinema 3')
# part 4: x^2 + 11x + c is (x + k)^2 for no whole k (and no k at all gives a whole c below 24 with 2k = 11 whole)
ok(not any(sp.expand((x + k)**2 - (x**2 + 11 * x + cc)) == 0 for k in range(0, 30) for cc in range(0, 25)), 'cinema 4: no whole k')
ok([o['id'] for o in P[3]['widget']['options'] if o.get('correct')] == ['no-middle'], 'cinema 4: key')
ok(sp.expand((x + 4)**2) == x**2 + 8 * x + 16 and sp.expand((x + 3)**2) == x**2 + 6 * x + 9 and 24 - 8 == 16 and 24 - 15 == 9, 'cinema 4: why lines')

P = S['p-allotment-plots']['parts']
A, B = x**2 + 9 * x + 20, 2 * x**2 + 15 * x + 28
ok(sp.factor(A) == (x + 4) * (x + 5) and sp.factor(B) == (x + 4) * (2 * x + 7), 'allotment: my factorisations')
expr(P[0], A, 'allotment 1')
wrongs(P[0], {'sum-twelve': (x + 2) * (x + 10), 'sum-21': (x + 1) * (x + 20)}, 'allotment 1')
expr(P[1], B, 'allotment 2')
wrongs(P[1], {'no-group': (x + 7) * (x + 8), 'wrong-pair': (2 * x + 4) * (x + 7)}, 'allotment 2')
ok(sp.expand((x + 7) * (x + 8)) == x**2 + 15 * x + 56 and sp.expand((2 * x + 4) * (x + 7)) == 2 * x**2 + 18 * x + 28, 'allotment 2: feedback expansions')
ok(sp.factor(A + B) == 3 * (x + 4)**2, 'allotment 3: my total')
expr(P[2], A + B, 'allotment 3')
wrongs(P[2], {'both-sides': 6 * (x + 4)**2, 'lost-square': 3 * (x + 4)}, 'allotment 3')
num(P[3], 3 * 10**2, 'allotment 4', (A + B).subs(x, 6))
ok(A.subs(x, 6) == 110 and B.subs(x, 6) == 190, 'allotment 4: 110 and 190')
wrongs(P[3], {'three-squared': (3 * 10)**2, 'both-sides': 6 * 10**2}, 'allotment 4')

P = S['p-steel-plates']['parts']
steel = (6 * x)**2 - 3**2
expr(P[0], steel, 'steel 1')
wrongs(P[0], {'six': 6 * x**2 - 9, 'hole': 36 * x**2 - 3, 'both': 6 * x**2 - 3}, 'steel 1')
ok(sp.expand(sp.factor(steel) - 9 * (2 * x - 1) * (2 * x + 1)) == 0 and sp.factor_list(steel)[0] == 9, 'steel 2: my factorisation')
expr(P[1], steel, 'steel 2')
wrongs(P[1], {'inside': 9 * (2 * x + 3) * (2 * x - 3), 'square': (6 * x - 3)**2}, 'steel 2')
ok(sp.expand(9 * (2 * x + 3) * (2 * x - 3)) == 36 * x**2 - 81 and sp.expand((6 * x - 3)**2).coeff(x, 1) == -36, 'steel 2: feedback expansions')
wide = sp.expand((6 * x + 2)**2 - 9)
expr(P[2], wide, 'steel 3')
wrongs(P[2], {'each-term': 36 * x**2 + 4 - 9, 'one-strip': 36 * x**2 + 12 * x + 4 - 9}, 'steel 3')
ok(sp.factor(wide) == (6 * x - 1) * (6 * x + 5), 'steel 4: my factorisation')
ok([(a, bb) for a in range(-200, 201) for bb in range(a, 201) if a * bb == -180 and a + bb == 24] == [(-6, 30)], 'steel 4: the pair for -180 and 24 is unique')
expr(P[3], wide, 'steel 4')
wrongs(P[3], {'signs': (6 * x - 5) * (6 * x + 1)}, 'steel 4')
ok(sp.expand((6 * x - 5) * (6 * x + 1)) == 36 * x**2 - 24 * x - 5, 'steel 4: feedback expansion')
num(P[4], 35 * 29, 'steel 5', 32 * 32 - 9)
wrongs(P[4], {'old': steel.subs(x, 5), 'each-term': 36 * 25 - 5, 'no-hole': 32**2, 'signs': 25 * 31}, 'steel 5')
ok(9 * 11 * 9 == 891, 'steel 5: 891 as 9 x 11 x 9')

# ---------------------------------------------------------------- quadratics 2
S = load('quadratics', 2)
P = S['p-cliff-stone']['parts']
h = 15 + 10 * t - 5 * t**2
q = sp.simplify(h - (-5 * (t - 1)**2))
num(P[0], q, 'cliff 1', max(h.subs(t, Fr(k, 1000)) for k in range(0, 4000)))
wrongs(P[0], {'sign': 15 - 5, 'no-five': 15 + 1}, 'cliff 1')
roots = sp.solve(h, t)
num(P[1], max(roots), 'cliff 2', bisect(lambda u: 15 + 10 * u - 5 * u * u, 1, 10))
ok(sp.expand(5 * (t - 3) * (t + 1)) == sp.expand(-h), 'cliff 2: 5(t-3)(t+1)')
wrongs(P[1], {'negative': min(roots), 'no-root': 1 + 4, 'carried': 1 + math.sqrt(2)}, 'cliff 2')
numset(P[2], sp.solve(h - 15, t), 'cliff 3', [0, bisect(lambda u: 10 * u - 5 * u * u, 1, 3)])
wrongs(P[2], {'sign': [0, -2]}, 'cliff 3')
r18 = sp.solve(h - 18, t)
numset(P[3], r18, 'cliff 4', [bisect(lambda u: 15 + 10 * u - 5 * u * u - 18, 0, 1), bisect(lambda u: 15 + 10 * u - 5 * u * u - 18, 1, 3)])
ok(round(float(min(r18)), 2) == 0.37 and round(float(max(r18)), 2) == 1.63 and abs(math.sqrt(0.4) - 0.632) < 5e-4, 'cliff 4: printed roundings')
wrongs(P[3], {'no-root': [1 - 0.4, 1 + 0.4], 'times-five': [1 - math.sqrt(10), 1 + math.sqrt(10)]}, 'cliff 4')

P = S['p-bus-chase']['parts']
gap = sp.expand(t**2 - (6 * t - 10))
num(P[0], sp.discriminant(gap, t), 'bus 1', (-6)**2 - 4 * 10)
wrongs(P[0], {'sign-b': -36 - 40, 'plus': 36 + 40, 'reversed': 40 - 36}, 'bus 1')
num(P[1], sp.simplify(gap - (t - 3)**2), 'bus 2', min(gap.subs(t, Fr(k, 100)) for k in range(0, 2000)))
wrongs(P[1], {'start': 10, 'halved': 10 - 3, 'sign': 10 + 9}, 'bus 2')
sam = sp.expand(t**2 - (6 * t - 7))
ok(sp.expand((t - 3)**2 - 2) == sam and sp.simplify(gap - sam) == 3, 'bus 3: square form and 3 m less')
num(P[2], min(sp.solve(sam, t)), 'bus 3', bisect(lambda u: u * u - 6 * u + 7, 0, 3))
wrongs(P[2], {'larger': 3 + math.sqrt(2), 'half-root': 6 / 2 - math.sqrt(8), 'no-root': 3 - 2}, 'bus 3')
vv = sp.solve(sp.discriminant(t**2 - v * t + 10, t), v)
num(P[3], max(vv), 'bus 4', math.sqrt(40))
# second route for bus 4: the least v on a fine grid for which the gap t^2 - vt + 10 reaches zero
grid = next(k / 10000 for k in range(60000, 70000) if (k / 10000)**2 - 40 >= 0)
ok(abs(grid - float(max(vv))) < 2e-4, 'bus 4: least speed on a grid')
ok(6.32**2 < 40 < 6.33**2, 'bus 4: 6.32 m/s falls short, 6.33 reaches (finding)')
wrongs(P[3], {'no-root': 40, 'no-four': math.sqrt(10)}, 'bus 4')

P = S['p-can-stack']['parts']
ok(all(sum(range(1, k + 1)) == k * (k + 1) // 2 for k in range(1, 60)), 'cans: the triangle rule')
num(P[0], next(k for k in range(1, 100) if sum(range(1, k + 1)) == 120), 'cans 1', max(sp.solve(n * (n + 1) / 2 - 120, n)))
ok(sp.expand((n + 16) * (n - 15)) == n**2 + n - 240, 'cans 1: (n+16)(n-15)')
wrongs(P[0], {'negative': -16, 'sign': 16}, 'cans 1')
num(P[1], sp.discriminant(n**2 + n - 200, n), 'cans 2', 1 + 800)
ok(28**2 == 784 and 29**2 == 841, 'cans 2: 784 and 841')
wrongs(P[1], {'sign-c': 1 - 800, 'no-double': 1 + 400}, 'cans 2')
num(P[2], max(sp.solve(n**2 + n - 200, n)), 'cans 3', bisect(lambda u: u * u + u - 200, 0, 50))
ok(abs(math.sqrt(801) - 28.302) < 5e-4 and round((-1 + 28.302) / 2, 3) == 13.651, 'cans 3: printed roundings')
wrongs(P[2], {'sign-b': (1 + math.sqrt(801)) / 2, 'no-half': -1 + math.sqrt(801), 'carried': (-1 + math.sqrt(401)) / 2}, 'cans 3')
rows = max(k for k in range(1, 100) if k * (k + 1) // 2 <= 100)
num(P[3], 100 - rows * (rows + 1) // 2, 'cans 4', 100 - 91)
ok(rows == 13, 'cans 4: 13 rows')
wrongs(P[3], {'rounded-up': 105 - 100, 'rows': 13}, 'cans 4')

# ---------------------------------------------------------------- quadratics 3
S = load('quadratics', 3)
P = S['p-canal-arch']['parts']
arch = sp.Rational(-1, 5) * x * (x - 20)
num(P[0], sum(sp.solve(arch, x)) / 2, 'arch 1', -sp.expand(arch).coeff(x, 1) / (2 * sp.expand(arch).coeff(x, 2)))
wrongs(P[0], {'root': 20, 'sign': -10}, 'arch 1')
num(P[1], arch.subs(x, 10), 'arch 2', max(arch.subs(x, Fr(k, 100)) for k in range(0, 2001)))
wrongs(P[1], {'sign': -20, 'no-a': 10 * 10}, 'arch 2')
expr(P[2], arch, 'arch 3')
wrongs(P[2], {'sign-h': sp.Rational(-1, 5) * (x + 10)**2 + 20, 'sign-a': sp.Rational(1, 5) * (x - 10)**2 + 20, 'no-a': -(x - 10)**2 + 20}, 'arch 3')
ends = sp.solve(arch - sp.Rational(64, 5), x)
num(P[3], max(ends) - min(ends), 'arch 4', (sum(1 for k in range(0, 20000) if arch.subs(x, Fr(k, 1000)) >= Fr(64, 5)) - 1) / 1000)
wrongs(P[3], {'half': 6, 'right-end': 16, 'left-end': 4}, 'arch 4')

P = S['p-bike-hire']['parts']
bikes = 150 - 5 * p
num(P[0], sp.solve(bikes, p)[0], 'bike 1', next(k for k in range(0, 100) if 150 - 5 * k == 0))
wrongs(P[0], {'no-divide': 150}, 'bike 1')
R = p * bikes
best = max(range(0, 3001), key=lambda k: (k / 100) * (150 - 5 * k / 100)) / 100
num(P[1], sp.solve(sp.diff(R, p), p)[0], 'bike 2', best)
wrongs(P[1], {'zero': 30}, 'bike 2')
num(P[2], R.subs(p, 15), 'bike 3', 15 * 75)
wrongs(P[2], {'bikes': 75, 'no-drop': 15 * 150}, 'bike 3')
profit = (p - 8) * bikes
bestp = max(range(0, 3001), key=lambda k: (k / 100 - 8) * (150 - 5 * k / 100)) / 100
num(P[3], sp.solve(sp.diff(profit, p), p)[0], 'bike 4', bestp)
wrongs(P[3], {'full-cost': 15 + 8, 'no-cost': 15, 'sign': (-8 + 30) / 2}, 'bike 4')
ok(profit.subs(p, 19) == 605 and sp.expand(605 - 5 * (p - 19)**2 - profit) == 0, 'bike 5: 605 and the square form')
band = [k / 100 for k in range(0, 4001) if (k / 100 - 8) * (150 - 5 * k / 100) >= 525 - 1e-9]
ok(min(band) == 15 and max(band) == 23 and len(band) == 801, 'bike 5: the band is 15 to 23, unbroken')
ok([o['id'] for o in P[4]['widget']['options'] if o.get('correct')] == ['inside'], 'bike 5: key')
ok(19 - 16 == 3 and 19 + 16 == 35, 'bike 5: the no-root option')

P = S['p-sprinkler-bank']['parts']
water, bank = 3 * x - x**2 / 2, x / 2
gapw = sp.expand(water - bank)
expr(P[0], gapw, 'sprinkler 1')
wrongs(P[0], {'added': sp.Rational(7, 2) * x - x**2 / 2, 'sign': sp.Rational(5, 2) * x + x**2 / 2}, 'sprinkler 1')
num(P[1], max(sp.solve(gapw, x)), 'sprinkler 2', bisect(lambda u: 2.5 * u - 0.5 * u * u, 1, 10))
wrongs(P[1], {'flat': max(sp.solve(water, x)), 'vertex': 2.5}, 'sprinkler 2')
num(P[2], bank.subs(x, 5), 'sprinkler 3', water.subs(x, 5))
wrongs(P[2], {'flat': bank.subs(x, 6), 'square-half': 15 - (0.5 * 5)**2}, 'sprinkler 3')
num(P[3], gapw.subs(x, sp.Rational(5, 2)), 'sprinkler 4', max(2.5 * k / 1000 - 0.5 * (k / 1000)**2 for k in range(0, 5001)))
ok(water.subs(x, 3) == sp.Rational(9, 2) and bank.subs(x, 3) == sp.Rational(3, 2) and sp.solve(sp.diff(water, x), x) == [3], 'sprinkler 4: water top 4.5 at 3, bank 1.5')
wrongs(P[3], {'water-top': 4.5, 'no-square': 2.5 * 2.5, 'x-value': 2.5}, 'sprinkler 4')

# ---------------------------------------------------------------- equations 4
S = load('equations', 4)
P = S['p-rowing-current']['parts']
sol = sp.solve([b + c - 14, b - c - 10], [b, c])
expr(P[0], 'b-c=10', 'rowing 1')
wrongs(P[0], {'reversed': 'c-b=10', 'helps': 'b+c=10', 'speed': 'b-c=14'}, 'rowing 1')
num(P[1], sol[b], 'rowing 2', (14 + 10) / 2)
wrongs(P[1], {'stopped': 24, 'current': 2, 'two-c': 14 - 10}, 'rowing 2')
num(P[2], sol[c], 'rowing 3', 14 - 12)
wrongs(P[2], {'carried': 14 - 24, 'added': 14 + 12, 'sign': -2}, 'rowing 3')
num(P[3], sp.Rational(42, 16 - 2), 'rowing 4', next(k for k in range(1, 100) if 14 * k == 42))
wrongs(P[3], {'with': 42 / 18, 'still': 42 / 16, 'multiplied': 42 * 14}, 'rowing 4')

P = S['p-seedling-trays']['parts']
brute = [(a, a + 8) for a in range(1, 200) if 5 * a + 3 * (a + 8) == 168]
ok(brute == [(18, 26)], 'trays: one whole-number solution')
expr(P[0], x + 8, 'trays 1')
wrongs(P[0], {'times': 8 * x, 'reversed': x - 8}, 'trays 1')
num(P[1], sp.solve(5 * x + 3 * (x + 8) - 168, x)[0], 'trays 2', brute[0][0])
wrongs(P[1], {'bracket': (168 - 8) / 8, 'reversed': (168 + 24) / 8, 'no-eight': 168 / 8, 'times': 168 / 29}, 'trays 2')
expr(P[2], 18 * 2 * n + 26 * n, 'trays 3')
wrongs(P[2], {'equal': 18 * n + 26 * n, 'reversed': 18 * n / 2 + 26 * n, 'carried': 20 * 2 * n + 28 * n}, 'trays 3')
num(P[3], 2 * sp.solve(62 * n - 310, n)[0], 'trays 4', next(2 * k for k in range(1, 100) if 2 * k * 18 + k * 26 == 310))
wrongs(P[3], {'large': 5, 'both': 15, 'plants': 10 * 18}, 'trays 4')

P = S['p-remote-cars']['parts']
numset(P[0], sp.solve(t**2 - 7 * t, t), 'cars 1', [k for k in range(-50, 51) if k * k == 7 * k])
wrongs(P[0], {'point': [7, 49]}, 'cars 1')
num(P[1], 7 * 7, 'cars 2', 7**2)
wrongs(P[1], {'double': 14, 'time': 7}, 'cars 2')
num(P[2], max(sp.solve(t**2 - 81, t)), 'cars 3', math.isqrt(81))
wrongs(P[2], {'negative': -9, 'halved': 81 / 2, 'squared': 81**2}, 'cars 3')
num(P[3], 81 - 7 * 9, 'cars 4', 9**2 - 7 * 9)
wrongs(P[3], {'position': 63, 'meeting': 81 - 49, 'time-gap': 9 - 7, 'carried': 81 - 7 * (-9)}, 'cars 4')
ok(all(k * k > 7 * k for k in range(8, 200)), 'cars 4: A stays ahead after t = 7')

P = S['p-salt-solutions']['parts']
sol = sp.solve([x + y - 500, sp.Rational(15, 100) * x + sp.Rational(40, 100) * y - 125], [x, y])
expr(P[0], '0.15x+0.4y=125', 'salt 1')
wrongs(P[0], {'per-cent': '15x+40y=125', 'strength': '0.15x+0.4y=0.25', 'swapped': '0.4x+0.15y=125'}, 'salt 1')
grams = [(a, 500 - a) for a in range(0, 501) if 15 * a + 40 * (500 - a) == 25 * 500]
ok(grams == [(300, 200)], 'salt: one mix by whole grams')
num(P[1], sol[y], 'salt 2', grams[0][1])
wrongs(P[1], {'other': 300, 'all-strong': 125 / 0.4, 'even': 250, 'multiplied': 50 * 0.25}, 'salt 2')
ok(abs((0.15 * 250 + 0.4 * 250) / 500 - 0.275) < 1e-12 and 0.15 * 500 == 75, 'salt 2: 27.5% and 75')
num(P[2], sol[x], 'salt 3', grams[0][0])
wrongs(P[2], {'salt': 125 - 0.4 * 200, 'carried': 500 - 312.5, 'added': 700}, 'salt 3')
ok(sp.solve([(sp.Rational(15, 100) * x + sp.Rational(40, 100) * y) - sp.Rational(1, 4) * (x + y)], [y])[y] == 2 * x / 3, 'salt 4: every 25% mix has y = 2x/3')
num(P[3], 360 + sp.Rational(2, 3) * 360, 'salt 4', next(360 + k for k in range(0, 2000) if 15 * 360 + 40 * k == 25 * (360 + k)))
wrongs(P[3], {'stopped': 240, 'reversed': 360 + 360 * 3 / 2, 'added': 500 + 60}, 'salt 4')
ok(0.15 * 360 + 0.4 * 240 == 150 and 0.25 * 600 == 150, 'salt 4: 54 + 96 = 150')

print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
