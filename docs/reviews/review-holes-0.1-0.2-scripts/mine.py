"""Second read, holes 0.1 and 0.2: the reader's own answers.

Every graded key and every wrong value of number-sense problems-4, quadratics problems-4 and the ten new exam items is
worked here from the item's text (the numbers are typed in from the prose, not read from the answer fields), by two
routes where there are two, and compared with the file. The script does not import the authors' scripts.

  <venv>/bin/python docs/reviews/review-holes-0.1-0.2-scripts/mine.py        (from the repo root; exit 0 = all agree)
"""
import itertools
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


def load(path):
    return {it['id']: it for it in json.load(open(path))['items']}


def num(part, want, name, tol=1e-9):
    w = part['widget']
    got = w.get('answer', w.get('answers'))
    if isinstance(want, (list, set)):
        ok(sorted(map(float, got)) == sorted(map(float, want)), f'{name}: answers {got} against {sorted(want)}')
    else:
        ok(abs(float(got) - float(want)) <= tol, f'{name}: answer {got} against {float(want)}')
        band = (w.get('tol') or {}).get('abs', 0)
        ok(abs(float(got) - float(want)) <= band + 1e-12, f'{name}: my value outside the band')


def wrongs(part, want, name, tol=1e-3):
    got = {x['id']: x.get('value', x.get('tex')) for x in part['widget'].get('wrong', [])}
    ok(set(got) == set(want), f'{name}: wrong ids {sorted(got)} against {sorted(want)}')
    for k, v in want.items():
        if k not in got:
            continue
        if isinstance(v, (list, set)):
            g = sorted(float(t) for t in str(got[k]).split(','))
            ok(all(abs(a - b) <= 0.006 for a, b in zip(g, sorted(map(float, v)))), f'{name}: wrong {k} {got[k]} against {sorted(v)}')
        elif isinstance(v, sp.Basic) and not v.is_number:
            ok(sp.simplify(sp.sympify(tex(got[k])) - v) == 0, f'{name}: wrong {k} {got[k]} against {v}')
        else:
            ok(abs(float(got[k]) - float(v)) <= tol, f'{name}: wrong {k} {got[k]} against {float(v)}')
    a = part['widget'].get('answer')
    if isinstance(a, (int, float)):
        band = (part['widget'].get('tol') or {}).get('abs', 0)
        for x in part['widget'].get('wrong', []):
            if not isinstance(x.get('value'), str) and x.get('value') is not None:
                ok(abs(x['value'] - a) > band + (x.get('tol') or {}).get('abs', 0), f"{name}: wrong {x['id']} band touches the answer band")


def tex(s):
    """the few LaTeX shapes these keys use, to sympy text"""
    import re
    s = s.replace('\\left', '').replace('\\right', '')
    while '\\frac' in s:
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = s.replace('^', '**').replace(')(', ')*(')
    s = re.sub(r'(\d)([a-z(])', r'\1*\2', s)
    s = re.sub(r'([a-z])\(', r'\1*(', s)
    return s


def expr(part, want, name, eq=False):
    w = part['widget']
    for form in [w['answer']] + list(w.get('accept', [])):
        if eq:
            l, r = form.split('=')
            d = sp.expand(sp.sympify(tex(l)) - sp.sympify(tex(r)))
            ratio = sp.simplify(d / want)
            ok(ratio.is_number and ratio != 0, f'{name}: {form} is not the same curve')
        else:
            ok(sp.simplify(sp.sympify(tex(form)) - want) == 0, f'{name}: {form} against {want}')


x, y, v, c, k = sp.symbols('x y v c k')
pi = math.pi

# ------------------------------------------------------------------ number-sense problems-4
NS = load('app/content/courses/number-sense/problems-4.json')
p = NS['p-hall-tiles']['parts']
ok(2 ** 4 * 3 ** 3 == 432 and 2 ** 2 * 3 ** 3 * 5 == 540, 'hall: the prose factorisations')
g = math.gcd(432, 540)
num(p[0], g, 'hall 1')
ok(g == max(d for d in range(1, 433) if 432 % d == 0 and 540 % d == 0), 'hall 1 by search')
wrongs(p[0], {'lcm': math.lcm(432, 540), 'threes-only': 27}, 'hall 1')
sides = [d for d in range(1, 541) if 432 % d == 0 and 540 % d == 0]
num(p[1], len(sides), 'hall 2')
ok(len(sides) == sp.divisor_count(108) == (2 + 1) * (3 + 1) and sides[0] == 1 and sides[-1] == 108, 'hall 2 by the index rule; "from 1 cm to 108 cm"')
wrongs(p[1], {'indices-multiplied': 2 * 3, 'indices-added': 3 + 4, 'lcm-carried': sp.divisor_count(2160)}, 'hall 2')
num(p[2], (432 // 108) * (540 // 108), 'hall 3')
wrongs(p[2], {'rows-added': 4 + 5, 'threes-carried': (432 // 27) * (540 // 27)}, 'hall 3')
num(p[3], Fr(20 * 108 * 108, 10000), 'hall 4')
ok(Fr(432, 100) * Fr(540, 100) == Fr(23328, 1000) and 108 * 108 == 11664 and 20 * 11664 == 233280, 'hall 4 by metres; the printed products')
wrongs(p[3], {'hundred': Fr(233280, 100), 'cm-squared': 233280}, 'hall 4')

p = NS['p-lawn-pond']['parts']
num(p[0], pi * 3 ** 2, 'lawn 1', 1e-4)
for name, q in (('3.14', 3.14), ('22/7', 22 / 7), ('3.142', 3.142)):
    a1 = round(q * 9, 2)
    ok(abs(a1 - p[0]['widget']['answer']) <= p[0]['widget']['tol']['abs'], f'lawn 1: pi = {name} gives {a1}, refused')
    a2 = round(108 - a1, 2)
    ok(abs(a2 - p[1]['widget']['answer']) <= p[1]['widget']['tol']['abs'] + 1e-9, f'lawn 2: pi = {name} carried gives {a2}, refused')
    ok(math.ceil(a2 / 20) == 4, f'lawn 3 with pi = {name}')
wrongs(p[0], {'diameter': pi * 36, 'circumference': pi * 6}, 'lawn 1')
num(p[1], 12 * 9 - 28.27, 'lawn 2')
wrongs(p[1], {'circumference-carried': 108 - 18.85, 'perimeter': 2 * (12 + 9) - 28.27}, 'lawn 2')
num(p[2], math.ceil(79.73 / 20), 'lawn 3')
wrongs(p[2], {'rounded-down': 79.73 // 20, 'circumference-carried': math.ceil(89.15 / 20), 'whole-lawn': math.ceil(108 / 20)}, 'lawn 3')
ok(round(79.73 / 20, 2) == 3.99, 'lawn 3: "about 3.99"')

p = NS['p-cycle-commute']['parts']
t = [26, 31, 24, 52, 27]
num(p[0], Fr(sum(t), 5), 'cycle 1')
wrongs(p[0], {'four-days': Fr(sum(t), 4), 'median': sorted(t)[2]}, 'cycle 1')
num(p[1], sorted(t)[2], 'cycle 2')
wrongs(p[1], {'unsorted': t[2], 'mean': Fr(sum(t), 5)}, 'cycle 2')
opts = {o['id']: o for o in p[2]['widget']['options']}
ok(opts['median'].get('correct') and max(t) - min(t) == 28 and sum(1 for z in t if z < 32) == 4, 'cycle 3: key, range 28, four rides under 32')
num(p[3], Fr(9) / Fr(27, 60), 'cycle 4')
wrongs(p[3], {'per-minute': Fr(9, 27), 'mean-time': Fr(9) / Fr(32, 60)}, 'cycle 4', 0.005)
num(p[4], Fr(20 * 1000, 3600), 'cycle 5', 1e-4)
wrongs(p[4], {'wrong-way': Fr(20 * 3600, 1000), 'minutes': Fr(20 * 1000, 60)}, 'cycle 5', 0.01)

p = NS['p-meshing-gears']['parts']
ok(2 ** 4 * 3 == 48 and 2 * 3 ** 2 == 18, 'gears: the prose factorisations')
first = next(n for n in range(1, 1000) if n % 48 == 0 and n % 18 == 0)
num(p[0], first, 'gears 1')
ok(first == math.lcm(48, 18) == 2 ** 4 * 3 ** 2, 'gears 1 by the primes')
wrongs(p[0], {'product': 48 * 18, 'hcf': math.gcd(48, 18)}, 'gears 1')
num(p[1], 144 // 18, 'gears 2')
wrongs(p[1], {'big-gear': 144 // 48, 'product-carried': 864 // 18}, 'gears 2')
num(p[2], Fr(4 * 60, 8), 'gears 3')
wrongs(p[2], {'per-second': Fr(4, 8), 'big-gear-carried': Fr(240, 3)}, 'gears 3')
num(p[3], round(240 * pi * 6 / 100), 'gears 4')
for q in (3.14, 22 / 7, 3.142):
    ok(round(240 * q * 6 / 100) == 45, f'gears 4 with pi = {q}')
wrongs(p[3], {'radius': round(240 * 2 * pi * 6 / 100), 'centimetres': round(240 * pi * 6)}, 'gears 4', 0.5)

# ------------------------------------------------------------------ quadratics problems-4
QD = load('app/content/courses/quadratics/problems-4.json')
p = QD['p-park-pond']['parts']
C, L = (-2, 3), (4, 11)
r = math.dist(C, L)
num(p[0], r, 'pond 1')
wrongs(p[0], {'added': 6 + 8, 'no-root': 100}, 'pond 1')
circle = (x + 2) ** 2 + (y - 3) ** 2 - 100
expr(p[1], sp.expand(circle), 'pond 2', eq=True)
ok(circle.subs({x: 4, y: 11}) == 0, 'pond 2: the lamp post is on the edge')
xs = sp.solve(circle.subs(y, x + 7), x)
num(p[2], xs, 'pond 3')
ok(sp.expand(circle.subs(y, x + 7)) == sp.expand(2 * (x ** 2 + 6 * x - 40)), 'pond 3: the printed quadratic')
bad = sp.solve(((x - 2) ** 2 + (y + 3) ** 2 - 100).subs(y, x + 7), x)
wrongs(p[2], {'signs': [-4, 10], 'centre-signs-carried': [float(b) for b in bad]}, 'pond 3')
pts = [(int(a), int(a) + 7) for a in xs]
ok(sorted(pts) == [(-10, -3), (4, 11)], 'pond 4: the two points of the question')
chord = sp.sqrt((pts[0][0] - pts[1][0]) ** 2 + (pts[0][1] - pts[1][1]) ** 2)
num(p[3], chord / sp.sqrt(2), 'pond 4')
ok(abs(float(chord) - 19.80) < 0.005, 'pond 4: "about 19.80 m"')
wrongs(p[3], {'squared': 196, 'added': 28}, 'pond 4')
sub = sp.expand(circle.subs(y, x + c))
ok(sp.expand(sub - (2 * x ** 2 + (2 * c - 2) * x + c ** 2 - 6 * c - 87)) == 0, 'pond 5: the quadratic printed in the question')
disc = sp.discriminant(sub, x)
ok(sp.expand(disc - (-4 * c ** 2 + 40 * c + 700)) == 0, 'pond 5: the printed discriminant')
cs = sp.solve(disc, c)
num(p[4], max(cs), 'pond 5', 1e-4)
dist = abs(-2 - 3 + float(max(cs))) / math.sqrt(2)          # second route: distance from the centre to the line is the radius
ok(abs(dist - 10) < 1e-9, 'pond 5: the tangent is 10 m from the centre')
wrongs(p[4], {'lower': min(cs), 'shift-by-radius': 5 + 10}, 'pond 5')

p = QD['p-windy-ride']['parts']
total = 16 / v + 9 / (v - 2)
top = sp.expand(sp.cancel(total * v * (v - 2)))
expr(p[0], top, 'windy 1')
wrongs(p[0], {'own-bottoms': sp.expand(16 * v + 9 * (v - 2)), 'tops-added': sp.Integer(25) + 0 * v}, 'windy 1')
roots = sp.solve(sp.Eq(total, sp.Rational(7, 2)), v)
num(p[1], [float(z) for z in roots], 'windy 2', 1e-4) if False else ok(sorted(roots) == [sp.Rational(8, 7), 8], f'windy 2: roots {roots}')
ok(all(abs(a - b) <= 0.005 for a, b in zip(sorted(p[1]['widget']['answers']), [8 / 7, 8])), 'windy 2: stored answers')
ok(sp.expand(7 * v ** 2 - 64 * v + 64 - (v - 8) * (7 * v - 8)) == 0, 'windy 2: the printed factorisation')
badr = sp.solve(sp.Eq((25 * v - 18) / (v * (v - 2)), sp.Rational(7, 2)), v)
wrongs(p[1], {'signs': [-8, -8 / 7], 'own-bottoms-carried': [float(b) for b in badr]}, 'windy 2')
good = [z for z in roots if z > 0 and z - 2 > 0]
num(p[2], good[0], 'windy 3')
ok(len(good) == 1 and Fr(16, 8) + Fr(9, 6) == Fr(7, 2), 'windy 3: one root is a ride, and 2 h + 1.5 h = 3.5 h')
wrongs(p[2], {'small-root': Fr(8, 7)}, 'windy 3', 0.005)
ratio = sp.simplify((9 / (v - 2)) / (16 / v))
expr(p[3], ratio, 'windy 4')
wrongs(p[3], {'not-flipped': (9 / (v - 2)) * (16 / v), 'upside-down': 1 / ratio}, 'windy 4')
num(p[4], ratio.subs(v, 8), 'windy 5')
ok(Fr(9, 6) / Fr(16, 8) == Fr(3, 4), 'windy 5 from the two times')
wrongs(p[4], {'upside-down': Fr(4, 3), 'small-root': ratio.subs(v, sp.Rational(8, 7))}, 'windy 5', 0.005)

p = QD['p-storage-crate']['parts']
V = x ** 3 + 4 * x ** 2 + x - 6
num(p[0], V.subs(x, -2), 'crate 1')
wrongs(p[0], {'sign': V.subs(x, 2), 'cube-sign': 8 + 16 - 2 - 6}, 'crate 1')
q, rem = sp.div(V, x + 2, x)
ok(rem == 0, 'crate 2: no remainder')
expr(p[1], q, 'crate 2')
wrongs(p[1], {'sign': sp.div(V, x - 2, x)[0], 'constant-sign': x ** 2 + 2 * x + 3}, 'crate 2')
ok(sp.div(V, x - 2, x)[1] == 20, 'crate 2: dividing by (x - 2) leaves 20')
expr(p[2], V, 'crate 3')
ok(sorted(sp.roots(V, x)) == [-3, -2, 1], 'crate 3: roots')
for w in p[2]['widget']['wrong']:
    ok(sp.expand(sp.sympify(tex(w['tex'])) - V) != 0, f"crate 3: wrong {w['id']} differs")
ok(sp.expand((x - 3) * (x + 1) - (x ** 2 - 2 * x - 3)) == 0, 'crate 3: the signs line')
expr(p[3], sp.cancel(V / (x ** 2 + 5 * x + 6)), 'crate 4')
wrongs(p[3], {'wrong-pair': x + 2, 'sign': x + 1}, 'crate 4')
x0 = Fr(5, 2) + 1
num(p[4], V.subs(x, sp.Rational(7, 2)), 'crate 5')
ok((x0 + 2) * (x0 + 3) * (x0 - 1) == Fr(715, 8) == Fr(89375, 1000), 'crate 5 by the brackets')
wrongs(p[4], {'x-is-height': V.subs(x, sp.Rational(5, 2)), 'base-only': (x0 + 2) * (x0 + 3)}, 'crate 5')

# ------------------------------------------------------------------ topic-0.1 new items
E1 = load('app/content/exams/topic-0.1.json')
it = E1['e-feed-updates']
num(it, 15 * 3600 * Fr(13, 2), 'feed')
ok(sum(15 for _ in range(int(6.5 * 3600))) == 351000, 'feed second by second')
wrongs(it, {'minutes-only': 15 * 60 * 6.5, 'hours-only': 15 * 6.5, 'six-hours': 15 * 3600 * 6}, 'feed')
it = E1['e-prime-table']
for o in it['widget']['options']:
    n = int(o['text'])
    ok(bool(o.get('correct')) == sp.isprime(n) == all(n % d for d in range(2, n)), f'prime table {n}')
ok(119 == 7 * 17 and 133 == 7 * 19 and 143 == 11 * 13 and 161 == 7 * 23 and 12 ** 2 == 144 and 13 ** 2 == 169 and math.isqrt(161) < 13 and 11 < math.sqrt(143) < 12, 'prime table: products and roots in the text')
it = E1['e-plan-hall']
num(it, (9 * 2) * (Fr(13, 2) * 2), 'plan hall')
ok(Fr(117, 2) * 4 == 234, 'plan hall by the area scale')
wrongs(it, {'scale-once': Fr(117, 2) * 2, 'plan-area': Fr(117, 2), 'perimeter': 2 * (18 + 13)}, 'plan hall')
it = E1['e-pit-area']
area = 50 ** 2 / (4 * pi)
num(it, round(area), 'pit')
ok(abs(pi * (50 / (2 * pi)) ** 2 - area) < 1e-9 and abs(625 / pi - area) < 1e-9 and round(50 / (2 * pi), 3) == 7.958, 'pit: two routes, 625/pi, r = 7.958')
for q in (3.14, 22 / 7, 3.142):
    ok(round(q * (50 / (2 * q)) ** 2) == 199, f'pit with pi = {q}')
ok(round(3.14 * round(50 / 6.28, 2) ** 2) == 199 and round(pi * 7.96 ** 2) == 199 and round(pi * 8 ** 2) != 199, 'pit: r kept to 2 d.p. still gives 199; r rounded to 8 does not')
wrongs(it, {'diameter-as-radius': pi * (50 / pi) ** 2, 'half-round': pi * 25 ** 2, 'edge-as-radius': pi * 50 ** 2}, 'pit', 1.0)
it = E1['e-partner-number']
cands = [n for n in range(1, 2001) if math.gcd(n, 24) == 8 and math.lcm(n, 24) == 168]
num(it, cands[0], 'partner')
ok(cands == [56] and 8 * 168 // 24 == 56 and math.gcd(192, 24) == 24, 'partner: unique; the times-hcf line')
wrongs(it, {'no-divide': 8 * 168, 'lcm-over': 168 // 24, 'times-hcf': 24 * 8}, 'partner')
it = E1['e-five-counts']
sols = []
for t5 in itertools.combinations_with_replacement(range(0, 41), 5):
    if sum(t5) != 40 or t5[2] != 9 or t5[4] - t5[0] != 7:
        continue
    cnt = {z: t5.count(z) for z in set(t5)}
    top = max(cnt.values())
    if [z for z in cnt if cnt[z] == top] == [10]:
        sols.append(t5)
ok(sols == [(3, 8, 9, 10, 10)], f'five counts: solutions {sols}')
num(it, sols[0][0], 'five counts')
wrongs(it, {'median-minus-range': 9 - 7, 'two-smallest': 40 - 9 - 20, 'second': 8}, 'five counts')

# ------------------------------------------------------------------ topic-0.2 new items
E2 = load('app/content/exams/topic-0.2.json')
it = E2['e-surd-difference']
val = sp.sqrt(75) - sp.sqrt(12)
opt = {o['id']: o for o in it['widget']['options']}
ok(opt['a'].get('correct') and val == 3 * sp.sqrt(3) and abs(float(val) - 3 * math.sqrt(3)) < 1e-12, 'surd difference key')
ok(sp.sqrt(75 - 12) == sp.sqrt(63) and 5 + 2 == 7 and 25 - 4 == 21, 'surd difference: the three slips')
it = E2['e-two-desks']
sol = sp.solve(sp.Eq(1 / x + 1 / (x + 3), sp.Rational(1, 2)), x)
num(it, max(sol), 'two desks')
ok(sorted(sol) == [-2, 3] and Fr(1, 3) + Fr(1, 6) == Fr(1, 2), 'two desks: roots and check')
wrongs(it, {'kept-negative': min(sol), 'tops-and-bottoms': sp.solve(sp.Eq(2 / (2 * x + 3), sp.Rational(1, 2)), x)[0], 'desk-b': 3 + 3}, 'two desks')
it = E2['e-diameter-ends']
A, B = (-5, 2), (7, 18)
cells = it['widget']['rows'][0]
mx, my, rad = Fr(A[0] + B[0], 2), Fr(A[1] + B[1], 2), math.dist(A, B) / 2
ok([cells[0]['answer'], cells[1]['answer'], cells[2]['answer']] == [mx, my, rad], 'diameter ends: key')
ok(all(abs(math.dist((mx, my), P) - 10) < 1e-12 for P in (A, B)), 'diameter ends: both ends are 10 from the centre')
ok(cells[0]['wrong'][0]['value'] == (B[0] - A[0]) / 2 and cells[1]['wrong'][0]['value'] == (B[1] - A[1]) / 2 and cells[2]['wrong'][0]['value'] == math.dist(A, B), 'diameter ends: wrongs')
p = E2['e-cubic-remainder']['parts']
P = x ** 3 + k * x ** 2 - 4 * x - 12
kk = sp.solve(sp.Eq(P.subs(x, 1), -12), k)[0]
num(p[0], kk, 'cubic 1')
ok(sp.rem(P.subs(k, kk), x - 1, x) == -12, 'cubic 1 by division')
wrongs(p[0], {'set-to-zero': sp.solve(P.subs(x, 1), k)[0], 'wrong-sign': sp.solve(sp.Eq(P.subs(x, -1), -12), k)[0]}, 'cubic 1')
expr(p[1], P.subs(k, 3), 'cubic 2')
ok(sorted(sp.roots(P.subs(k, 3), x)) == [-3, -2, 2] and P.subs({k: 3, x: 3}) == 30, 'cubic 2: roots; p(3) = 30')

print(f'mine: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
