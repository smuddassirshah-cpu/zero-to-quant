"""Second read, problems 0.3 c: the reader's own answers and slips for series and trig problem sets 1 to 3.

Each part was solved from its text before its key was read. Here every key is rebuilt by a route of the reader's own
(direct summation term by term for every series answer, coordinates, grid scans and mpmath for trig, sympy for exact
forms) and every wrong[] value is rebuilt from the slip its feedback names. A numeric key must sit within 1e-4 of my
value (or within 0.01 and inside its band where the key is built from rounded carried values); a wrong value must sit inside its own band around my slip
value and outside the key's band.

Run: <venv>/bin/python docs/reviews/problems-0.3-c-scripts/mine.py     (from the repo root; exits 0 when all agree)
"""
import json
import math
import re
import sys
from fractions import Fraction as F
from itertools import combinations, product

import mpmath as mp
import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application, parse_expr,
                                        standard_transformations)

mp.mp.dps = 30
checks = fails = 0


def say(ok, msg):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print('FAIL', msg)


def tex(t):
    """A small LaTeX reader for the forms these sets use."""
    t = t.replace('\\left', '').replace('\\right', '').replace('\\cdot', '*').replace('\\times', '*')
    t = t.replace('\\pi', ' pi ').replace('\\sin', ' sin ').replace('\\cos', ' cos ')
    for _ in range(6):
        t = re.sub(r'\\d?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
        t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
        t = re.sub(r'\^\{([^{}]*)\}', r'**(\1)', t)
    t = t.replace('^', '**')
    if '=' in t:
        l, r = t.split('=')
        return tex(l) - tex(r)
    tr = standard_transformations + (implicit_multiplication_application, convert_xor)
    return parse_expr(t, transformations=tr, local_dict={'n': sp.Symbol('n'), 's': sp.Symbol('s'), 'x': sp.Symbol('x'),
                                                          'C': sp.Symbol('C'), 'pi': sp.pi})


def same(a, b, eqn=False):
    if sp.simplify(a - b) == 0:
        return True
    if eqn:  # equations: equal up to a non-zero multiple
        r = sp.simplify(a / b)
        return bool(r.is_number and r != 0)
    syms = list((a - b).free_symbols)
    if not syms:
        return abs(sp.N(a - b)) < 1e-9
    return all(abs(sp.N((a - b).subs({v: sp.Rational(7 + 3 * k, 5) for v in syms}))) < 1e-9 for k in range(4))


n, s, x, C = sp.symbols('n s x C')
D = math.radians
MY = {}


def put(course, k, item, part, ans, **wrong):
    MY[(course, k, item, part)] = (ans, wrong)


# ---------------------------------------------------------------- series 1
rows = [18 + 3 * i for i in range(25)]                      # row 1 .. 25 by stepping
put('series', 1, 'p-theatre-rows', 1, rows[6], **{'seven-steps': 18 + 7 * 3, 'next-row': rows[4]})
put('series', 1, 'p-theatre-rows', 2, 3 * n + 15, **{'n-steps': 18 + 3 * n, 'swapped': 18 * n + 3, 'step-only': 3 * n})
put('series', 1, 'p-theatre-rows', 3, rows[24], **{'n-steps': 18 + 3 * 25, 'step-only': 75})
first = next(i + 1 for i, r in enumerate(rows) if 2 * r >= rows[24])
put('series', 1, 'p-theatre-rows', 4, first, halfway=12.5, divided=45 / 3, steps=(45 - 18) / 3)
sw = [F(80)]
while len(sw) < 12:
    sw.append(sw[-1] * F(9, 10))
say(sw[1] == 72 and sw[2] == F(648, 10), 'pendulum: the three swings are not times 0.9')
put('series', 1, 'p-pendulum-swings', 1, 'ratio')
put('series', 1, 'p-pendulum-swings', 2, 80 * sp.Rational(9, 10) ** (n - 1),
    **{'power-n': 80 * sp.Rational(9, 10) ** n, 'bracket': 72 ** (n - 1), 'arith': 88 - 8 * n})
put('series', 1, 'p-pendulum-swings', 3, float(sw[5]), **{'power-n': float(sw[6]), 'swing-five': float(sw[4]), 'arith': 80 - 8 * 5})
put('series', 1, 'p-pendulum-swings', 4, next(i + 1 for i, v in enumerate(sw) if v < 40),
    seven=next(i for i in range(1, 30) if 88 - 8 * i < 40), six=6)
say(next(i for i in range(1, 30) if 80 * 0.9 ** i < 40) == 7, 'pendulum 4: the 0.9^n slip does not give 7')
u = [F(240)]
for _ in range(9):
    u.append(u[-1] * F(4, 10) + 240)
u6 = [F(240)]
for _ in range(9):
    u6.append(u6[-1] * F(6, 10) + 240)
put('series', 1, 'p-daily-tablet', 1, float(u[2]), **{'no-clearing': 720, 'tablet-two': float(u[1]), 'kept-sixty': float(u6[2])})
Lv = sp.solve(sp.Eq(x, sp.Rational(2, 5) * x + 240), x)[0]
say(abs(float(u[-1]) - 400) < 0.1 and all(a < b < 400 for a, b in zip(u, u[1:])), 'tablet: terms do not rise to 400')
put('series', 1, 'p-daily-tablet', 2, Lv, **{'kept-sixty': 240 / 0.4, 'sign': 240 / 1.4})
say(all(400 - u[i] == 160 * F(4, 10) ** i for i in range(10)), 'tablet 3: gaps are not 160*0.4^(n-1)')
put('series', 1, 'p-daily-tablet', 3, 160 * sp.Rational(2, 5) ** (n - 1),
    **{'power-n': 160 * sp.Rational(2, 5) ** n, 'cleared': 160 * sp.Rational(3, 5) ** (n - 1), 'level': 400 * sp.Rational(2, 5) ** (n - 1)})
put('series', 1, 'p-daily-tablet', 4, next(i + 1 for i, v in enumerate(u) if v > 395),
    **{'power-n': next(i for i in range(1, 20) if 160 * 0.4 ** i < 5), 'kept-sixty': next(i + 1 for i, v in enumerate(u6) if v > 395)})
say(float(u[4]) == 395.904 and float(u[3]) == 389.76, 'tablet 4: u4, u5')
put('series', 1, 'p-shop-orders', 1, F(216 - 96, 2), **{'no-halve': 120, 'three-steps': 40})
put('series', 1, 'p-shop-orders', 2, math.sqrt(216 / 96), **{'no-root': 2.25, 'halved': 1.125, 'inverted': math.sqrt(96 / 216)})
put('series', 1, 'p-shop-orders', 3, 'geom')
say(96 * 1.5 == 144 and 144 * 1.5 == 216 and 96 + 60 == 156, 'shop 3')
put('series', 1, 'p-shop-orders', 4, 64 * sp.Rational(3, 2) ** (n - 1),
    **{'month-two-start': 96 * sp.Rational(3, 2) ** (n - 1), 'power-n': 64 * sp.Rational(3, 2) ** n, 'arith': 60 * n - 24})
m = [F(64)]
while len(m) < 12:
    m.append(m[-1] * F(3, 2))
say(m[1] == 96 and m[3] == 216 and m[6] == 729 and float(m[7]) == 1093.5, 'shop: months')
put('series', 1, 'p-shop-orders', 5, next(i + 1 for i, v in enumerate(m) if v > 1000),
    **{'power-n': next(i for i in range(1, 30) if 64 * 1.5 ** i > 1000), 'arith': next(i for i in range(1, 99) if 60 * i - 24 > 1000)})

# ---------------------------------------------------------------- series 2
tins = [5 + 2 * i for i in range(12)]
put('series', 2, 'p-tin-display', 1, tins[11], **{'n-steps': 5 + 24, 'step-only': 24})
put('series', 2, 'p-tin-display', 2, sum(tins), **{'no-halve': 2 * sum(tins), 'last-only': 6 * 27, 'n-steps': 6 * (10 + 24)})
say(all(tins[k - 1] == 2 * k + 3 for k in range(1, 13)), 'tins: row k is not 2k+3')
put('series', 2, 'p-tin-display', 3, len(range(5, 13)), subtract=7, top=12)
put('series', 2, 'p-tin-display', 4, sum(2 * k + 3 for k in range(5, 13)),
    **{'seven-rows': 3.5 * 40, 'five-left': sum(tins) - sum(tins[:5]), 'full': sum(tins)})
days = [4 * 3 ** i for i in range(12)]
put('series', 2, 'p-app-users', 1, days[5], **{'power-n': days[6], 'day-five': days[4]})
put('series', 2, 'p-app-users', 2, sum(days[:6]), **{'no-halve': 3 * sum(days[:6]) - sum(days[:6]), 'no-first': days[6] / 2})
say(all(sum(days[:k]) == 2 * 3 ** k - 2 for k in range(1, 12)), 'app 3: S_n by direct summation')
put('series', 2, 'p-app-users', 3, 2 * 3 ** n - 2, **{'no-divide': 4 * 3 ** n - 4, 'power-n-1': 2 * 3 ** (n - 1) - 2, 'sign': 2 - 2 * 3 ** n})
put('series', 2, 'p-app-users', 4, next(k for k in range(1, 12) if sum(days[:k]) > 100000),
    **{'one-day': next(k + 1 for k, v in enumerate(days) if v > 100000), 'nine': 9})
say(sum(days[:9]) == 39364 and sum(days[:10]) == 118096, 'app 4: S9, S10')
rises = [F(3)]
while len(rises) < 400:
    rises.append(rises[-1] * F(6, 10))
S = lambda k: float(sum(rises[:k]))
put('series', 2, 'p-bouncing-ball', 1, S(9), forever=S(400), ten=S(10), eight=S(8))
put('series', 2, 'p-bouncing-ball', 2, 5 + 2 * S(9), once=5 + 7.42, **{'no-drop': 2 * S(9), 'double-drop': 10 + 2 * S(9)})
put('series', 2, 'p-bouncing-ball', 3, S(400), whole=5 / 0.4, **{'divide-r': 3 / 0.6, 'second': float(sum(rises[1:]))})
put('series', 2, 'p-bouncing-ball', 4, 5 + 2 * S(400), once=12.5, **{'no-drop': 15, 'double-drop': 25})
pa = [50 + 10 * i for i in range(40)]
say(all(sum(pa[:k]) == 5 * k * k + 45 * k for k in range(1, 40)), 'plan A: S_n by direct summation')
put('series', 2, 'p-two-repayment-plans', 1, 5 * n ** 2 + 45 * n,
    **{'last-term': 5 * n ** 2 + 50 * n, 'no-halve': 10 * n ** 2 + 90 * n, 'one-month': 10 * n + 40})
put('series', 2, 'p-two-repayment-plans', 2, next(k for k in range(1, 40) if sum(pa[:k]) >= 3000), twenty=20, flat=3000 / 50)
say(sum(pa[:20]) == 2900 and sum(pa[:21]) == 3150, 'plan A: S20, S21')
pb = [F(200)]
while len(pb) < 600:
    pb.append(pb[-1] * F(9, 10))
B = lambda k: float(sum(pb[:k]))
put('series', 2, 'p-two-repayment-plans', 3, B(600), ar=float(sum(pb[1:])), plus=200 / 1.9, **{'divide-r': 200 / 0.9})
put('series', 2, 'p-two-repayment-plans', 4, B(21), twenty=B(20), forever=2000, left=float(sum(pb[21:])))
put('series', 2, 'p-two-repayment-plans', 5, 3000 - B(21), forever=1000, twenty=3000 - B(20), paid=B(21))

# ---------------------------------------------------------------- series 3
c = lambda N, k: sum(1 for _ in combinations(range(N), k))
put('series', 3, 'p-pizza-toppings', 1, c(8, 3), ordered=8 * 7 * 6, times=24, repeats=8 ** 3)
put('series', 3, 'p-pizza-toppings', 2, c(8, 5), ordered=8 * 7 * 6 * 5 * 4, **{'ordered-three': 336})
put('series', 3, 'p-pizza-toppings', 3, c(9, 3), ordered=9 * 8 * 7, doubled=112, **{'one-more': 64})
say(c(8, 2) == 28 and [c(9, k) for k in range(10)] == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1], 'pizza: row 9')
put('series', 3, 'p-pizza-toppings', 4, sum(1 for _ in product([0, 1], repeat=9)), **{'no-plain': 511, 'row-eight': 256})
co = sp.Poly(sp.expand((1 - 3 * x) ** 7), x).all_coeffs()[::-1]
put('series', 3, 'p-bracket-estimate', 1, co[2], sign=-co[2], **{'not-squared': 21 * 3, 'no-count': 9})
put('series', 3, 'p-bracket-estimate', 2, co[0] + co[1] * x + co[2] * x ** 2,
    sign=1 + 21 * x + 189 * x ** 2, **{'square-sign': 1 - 21 * x - 189 * x ** 2, 'no-count': 1 - 3 * x + 9 * x ** 2})
e3 = lambda t: 1 - 21 * t + 189 * t * t
put('series', 3, 'p-bracket-estimate', 3, e3(0.01), linear=0.79, calculator=0.97 ** 7, **{'square-sign': 1 - 0.21 - 0.0189, 'x-three': e3(0.03)})
put('series', 3, 'p-bracket-estimate', 4, co[3], sign=-co[3], **{'not-cubed': -35 * 3, 'no-count': -27})
put('series', 3, 'p-bracket-estimate', 5, e3(0.01) + float(co[3]) * 1e-6, added=e3(0.01) + 945e-6, square=0.8089 - 945 * 1e-4)
say(abs(0.97 ** 7 - 0.80798) < 5e-6, 'bracket 5: calculator 0.80798')
put('series', 3, 'p-gym-membership', 1, 1 + 12 * 0.005 + 66 * 0.005 ** 2, linear=1.06, calculator=1.005 ** 12, **{'no-half': 1 + 0.06 + 132 * 0.005 ** 2})
put('series', 3, 'p-gym-membership', 2, 1 / 1.0617, grown=1.0617, subtract=1 - 0.0617, **{'one-month': 1 / 1.005})
pv = sum(100 / 1.005 ** k for k in range(1, 13))             # the 12 present values added one by one
put('series', 3, 'p-gym-membership', 3, pv, undiscounted=1200, **{'no-one-minus': 20000 * 0.9419, 'one-payment': 94.19})
put('series', 3, 'p-gym-membership', 4, pv - 1150, undiscounted=50, sign=1150 - pv)
say(abs(pv - 1161.89) < 0.005 and round(20000 * (1 - 0.9419)) == 1162, 'gym 3: 1161.89 and 1162')
put('series', 3, 'p-powers-of-eleven', 1, 11 ** 4, share=10 ** 4 + 1, **{'no-count': 11111})
put('series', 3, 'p-powers-of-eleven', 2, 11 ** 5, digits=15101051, share=10 ** 5 + 1, **{'times-ten': 146410})
put('series', 3, 'p-powers-of-eleven', 3, 11 ** 5 / 10 ** 5, shift=16.1051, linear=1.5, **{'too-far': 0.161051})
put('series', 3, 'p-powers-of-eleven', 4, 1.1 ** 5 - 1.5, dropped=0.1, sign=1.5 - 1.1 ** 5, **{'three-term': 1.1 ** 5 - 1.6})

# ---------------------------------------------------------------- trig 1 (coordinates)
wire = math.dist((0, 14), (35, 2))
put('trig', 1, 'p-zip-wire', 1, wire, added=47, subtracted=math.sqrt(35 ** 2 - 12 ** 2), **{'used-14': math.hypot(14, 35)})
put('trig', 1, 'p-zip-wire', 2, 12 / wire, tan=12 / 35, cos=35 / 37, flipped=37 / 12)
rider = (35 * 20 / wire, 14 - 12 * 20 / wire)               # the point 20 m along the wire
put('trig', 1, 'p-zip-wire', 3, 14 - rider[1], cos=rider[0], tan=20 * 12 / 35, height=rider[1])
put('trig', 1, 'p-zip-wire', 4, rider[0], subtracted=20 - 6.49, added=math.hypot(20, 6.49))
hexa = [sp.Matrix([10 * sp.cos(sp.pi * k / 3), 10 * sp.sin(sp.pi * k / 3)]) for k in range(6)]  # A..F round the centre
A_, B_, C_, D_ = hexa[:4]
put('trig', 1, 'p-hexagon-tile', 1, sp.sqrt(10 ** 2 - 5 ** 2), added=sp.sqrt(125), **{'whole-side': 10 * sp.sqrt(3), 'half-square': 5 * sp.sqrt(2)})
put('trig', 1, 'p-hexagon-tile', 2, sp.simplify((A_ - C_).norm()), half=5 * sp.sqrt(3), side=sp.Integer(10), long=sp.Integer(20))
say(sp.simplify((A_ - D_).norm()) == 20 and sp.simplify((C_ - D_).norm()) == 10, 'hexagon: AD, CD')
say(sp.simplify(B_.dot(A_ - C_)) == 0 and sp.simplify(((A_ + C_) / 2 - B_ / 2).norm()) == 0, 'hexagon: OB does not bisect AC at right angles')
put('trig', 1, 'p-hexagon-tile', 3, sp.simplify((A_ - C_).norm() ** 2 + (C_ - D_).norm() ** 2),
    **{'root-as-three': 30 + 100, 'root-left': 100 * math.sqrt(3) + 100, 'cd-unsquared': 310})
v1, v2 = C_ - A_, D_ - A_
put('trig', 1, 'p-hexagon-tile', 4, math.degrees(math.acos(float(v1.dot(v2) / (v1.norm() * v2.norm())))),
    tan=math.degrees(math.atan(0.5)), radians=math.asin(0.5), **{'angle-d': 60})
Pa, Pb = (60, 0), (45 * math.cos(D(55)), 45 * math.sin(D(55)))      # P at the origin
AB = math.dist(Pa, Pb)
put('trig', 1, 'p-lake-markers', 1, 'cosine')
put('trig', 1, 'p-lake-markers', 2, AB, plus=math.sqrt(5625 + 3097.44), pythagoras=75, **{'no-root': 2527.56})
angA = math.degrees(math.atan2(Pb[1], 60 - Pb[0]))                    # angle PAB from coordinates
put('trig', 1, 'p-lake-markers', 3, angA, ratio=45 * 0.8192 / 50.27, radians=math.radians(angA),
    **{'wrong-side': math.degrees(math.asin(60 * 0.8192 / 50.27))})
dist = abs(Pa[0] * Pb[1] - Pa[1] * Pb[0]) / AB                        # distance from the origin to line AB
put('trig', 1, 'p-lake-markers', 4, dist, cos=60 * math.cos(D(47.2)), tan=60 * math.tan(D(47.2)), **{'used-45': 45 * math.sin(D(47.2))})
say(45 < AB < 60, 'lake 3: PB is not the shortest side, so angle A might be obtuse')
Ael = (40 * math.cos(D(60)), 40 * math.sin(D(60)))
Bb = (Ael[0] + 30 * math.cos(D(-30)), Ael[1] + 30 * math.sin(D(-30)))  # at right angles to OA, forward and down
put('trig', 1, 'p-desk-lamp', 1, 20 * sp.sqrt(3), **{'sin-30': sp.Integer(20), 'no-half': 40 * sp.sqrt(3), 'half-square': 20 * sp.sqrt(2)})
say(abs(Ael[1] - 20 * math.sqrt(3)) < 1e-9, 'lamp 1: elbow height')
put('trig', 1, 'p-desk-lamp', 2, math.hypot(*Bb), added=70, subtracted=math.sqrt(40 ** 2 - 30 ** 2))
aob = 60 - math.degrees(math.atan2(Bb[1], Bb[0]))
put('trig', 1, 'p-desk-lamp', 3, aob, flipped=math.degrees(math.atan(40 / 30)), sine=math.degrees(math.asin(0.75)), radians=math.radians(aob))
put('trig', 1, 'p-desk-lamp', 4, Bb[1], sixty=50 * math.sin(D(60)), cos=50 * math.cos(D(23.1)), added=50 * math.sin(D(96.9)),
    **{'angle-aob': 50 * math.sin(D(36.9))})
put('trig', 1, 'p-desk-lamp', 5, 20 * sp.sqrt(3) - 15, above=20 * sp.sqrt(3) + 15, **{'cos-30': 5 * sp.sqrt(3), 'whole-arm': 20 * sp.sqrt(3) - 30})
say(abs(Bb[1] - (20 * math.sqrt(3) - 15)) < 1e-9, 'lamp 5: exact height against coordinates')

# ---------------------------------------------------------------- trig 2
th = 5.4 / 2.4
tip = 2.4 * mp.e ** (1j * th)
put('trig', 2, 'p-water-wheel', 1, th, times=5.4 * 2.4, flipped=2.4 / 5.4, turns=5.4 / (2 * math.pi * 2.4))
put('trig', 2, 'p-water-wheel', 2, math.degrees(th), **{'wrong-way': th * math.pi / 180, 'no-pi': th * 180})
put('trig', 2, 'p-water-wheel', 3, 3 + float(tip.imag), cos=3 + 2.4 * math.cos(D(128.9)),
    **{'radian-mode': 3 + 2.4 * math.sin(128.9), 'degree-mode': 3 + 2.4 * math.sin(D(2.25)), 'no-hub': float(tip.imag)})
other = [d / 100 for d in range(0, 9000) if abs(2.4 * math.sin(D(d / 100)) - float(tip.imag)) < 2e-4]
put('trig', 2, 'p-water-wheel', 4, sum(other) / len(other), **{'cos-mirror': 360 - 128.9, 'half-turn': 128.9 + 180, 'minus-90': 38.9})
put('trig', 2, 'p-water-wheel', 5, 2.4 * (math.pi - th), degrees=2.4 * 51.1, divided=51.1 / 2.4, between=5.4 - 2.14)
h1 = lambda t: 6 + 0.8 * math.sin(math.pi * t / 5)
h2 = lambda t: 6 + 0.8 * math.sin(math.pi * (t - 3) / 5)
grid = [k / 1000 for k in range(0, 30001)]
per = next(t for t in grid[1:] if all(abs(h1(q) - h1(q + t)) < 1e-9 for q in (0.3, 1.7, 2.9, 4.4)))
put('trig', 2, 'p-two-buoys', 1, per, **{'read-five': 5, 'b-itself': math.pi / 5, 'times': 2 * math.pi * math.pi / 5})
pk1 = next(t for t in grid if h1(t) > 6.8 - 1e-9)
pk2 = next(t for t in grid if h2(t) > 6.8 - 1e-9)
put('trig', 2, 'p-two-buoys', 2, pk1, angle=math.pi / 2, half=5, trough=7.5)
put('trig', 2, 'p-two-buoys', 3, pk2, early=-0.5, lag=3)
put('trig', 2, 'p-two-buoys', 4, h2(5.5) - h1(5.5), height=h1(5.5), **{'degree-mode': 6.8 - (6 + 0.8 * math.sin(D(1.1 * math.pi))), 'full-swing': 1.6})
phys = lambda t: 28 - 25 * math.cos(2 * math.pi * t / 20)            # the wheel itself: bottom at t = 0
model = lambda t, cc=5: 25 * math.sin(math.pi / 10 * (t - cc)) + 28
say(all(abs(phys(t) - model(t)) < 1e-9 for t in grid[::37]), 'wheel: the model with c = 5 is not the wheel')
put('trig', 2, 'p-observation-wheel', 1, 25, diameter=50, top=53, hub=28)
put('trig', 2, 'p-observation-wheel', 2, sp.pi / 10, period=sp.Integer(20), half=sp.pi / 20, flipped=10 / sp.pi)
put('trig', 2, 'p-observation-wheel', 3, 5, boarding=0, top=10, falling=15)
for cbad in (0, 10, 15):
    say(any(abs(phys(t) - model(t, cbad)) > 1 for t in grid[::37]), f'wheel 3: c = {cbad} also fits')
put('trig', 2, 'p-observation-wheel', 4, phys(8), **{'degree-mode': 25 * math.sin(D(0.3 * math.pi)) + 28, 'no-shift': 25 * math.sin(0.8 * math.pi) + 28})
oth = [t for t in grid if t <= 20 and abs(phys(t) - phys(8)) < 1e-9 and abs(t - 8) > 1e-6]
say(len(oth) == 1, 'wheel 5: not exactly one other time in the first turn')
put('trig', 2, 'p-observation-wheel', 5, oth[0], **{'no-shift': 7, 'half-period': 18, 'mirror-start': 2})

# ---------------------------------------------------------------- trig 3
Aang = math.pi - math.asin(8 / 17)
Bang = math.acos(24 / 25)
put('trig', 3, 'p-two-angles', 1, math.cos(Aang), sign=15 / 17, **{'one-minus': 1 - 8 / 17, 'no-root': 225 / 289})
put('trig', 3, 'p-two-angles', 2, math.sin(Bang), negative=-0.28, **{'one-minus': 1 - 24 / 25, 'no-root': 49 / 625})
put('trig', 3, 'p-two-angles', 3, math.sin(Aang + Bang), sign=(192 + 105) / 425, **{'sum-of-sines': 8 / 17 + 7 / 25, 'cos-formula': math.cos(Aang + Bang)})
put('trig', 3, 'p-two-angles', 4, math.cos(Aang + Bang), plus=(-360 + 56) / 425, sign=(360 - 56) / 425)
say(F(87, 425) == F(8, 17) * F(24, 25) - F(15, 17) * F(7, 25) and 87 ** 2 + 416 ** 2 == 425 ** 2, 'two angles: 87/425, 416/425')
put('trig', 3, 'p-two-angles', 5, math.degrees(Aang + Bang), principal=math.degrees(math.asin(0.2047)),
    third=180 + math.degrees(math.asin(0.2047)), fourth=360 - math.degrees(math.asin(0.2047)))
q = sp.expand(2 * (1 - s ** 2) + 3 * s - 3)
put('trig', 3, 'p-quadratic-in-sine', 1, -q, **{'not-distributed': s ** 2 - 3 * s + 2, 'cos-as-sin': 2 * s ** 2 + 3 * s - 3, 'moved-3': 2 * s ** 2 - 3 * s - 5})
put('trig', 3, 'p-quadratic-in-sine', 2, sorted(float(r) for r in sp.solve(q, s)), signs=[-1, -0.5], carried=[1, 2])
sol = [d for d in range(0, 361) if abs(2 * math.cos(D(d)) ** 2 + 3 * math.sin(D(d)) - 3) < 1e-9]
fine = [d / 100 for d in range(0, 36001) if abs(2 * math.cos(D(d / 100)) ** 2 + 3 * math.sin(D(d / 100)) - 3) < 1e-9]
say(fine == [30.0, 90.0, 150.0], f'quadratic 3: fine scan gives {fine}')
put('trig', 3, 'p-quadratic-in-sine', 3, sol, **{'cos-rule': [30, 90, 330], 'tan-rule': [30, 90, 210]})
put('trig', 3, 'p-quadratic-in-sine', 4, sp.Rational(max(sol), 180) * sp.pi, degrees=sp.Integer(150), middle=sp.pi / 2, half=5 * sp.pi / 12)
put('trig', 3, 'p-daylight-model', 1, (16.4 - 7.6) / 2, range=8.8, longest=16.4, midline=12)
put('trig', 3, 'p-daylight-model', 2, sp.pi / 6, period=sp.Integer(12), flipped=6 / sp.pi, **{'half-cycle': sp.pi / 3})
Lm = lambda t, cc=3: 4.4 * math.sin(math.pi / 6 * (t - cc)) + 12
g12 = [k / 1000 for k in range(0, 12001)]
say(abs(max(g12, key=Lm) - 6) < 1e-9 and min(Lm(t) for t in g12) > 7.6 - 1e-9 and abs(Lm(6) - 16.4) < 1e-9 and abs(Lm(12) - 7.6) < 1e-9, 'daylight: peak and trough')
put('trig', 3, 'p-daylight-model', 3, 3, peak=6, falling=9, trough=12)
cross = [t for t in g12 if abs(Lm(t) - 14.2) < 1e-9]
put('trig', 3, 'p-daylight-model', 4, cross, below=[t for t in g12 if abs(Lm(t) - 9.8) < 1e-9],
    **{'no-shift': [t for t in g12 if abs(math.sin(math.pi * t / 6) - 0.5) < 1e-9]})
put('trig', 3, 'p-daylight-model', 5, round(sum(1 for t in g12 if Lm(t) > 14.2 + 1e-9) / 1000, 2), outside=8, counted=5)
put('trig', 3, 'p-garden-bed', 1, 30 * sp.sin(C), cos=30 * sp.cos(C), angle=30 * C, **{'no-half': 60 * sp.sin(C)})
ang = [d / 100 for d in range(1, 18000) if abs(0.5 * 5 * 12 * math.sin(D(d / 100)) - 18) < 0.0021]
lo = [a for a in ang if a < 90]
hi = [a for a in ang if a > 90]
put('trig', 3, 'p-garden-bed', 2, [sum(lo) / len(lo), sum(hi) / len(hi)],
    **{'no-half': [math.degrees(math.asin(0.3)), 180 - math.degrees(math.asin(0.3))], 'cos-rule': [36.87, 323.13]})
Cob = math.pi - math.asin(0.6)
put('trig', 3, 'p-garden-bed', 3, math.cos(Cob), sign=0.8, **{'one-minus': 0.4, 'no-root': -0.64})
third = math.dist((12, 0), (5 * math.cos(Cob), 5 * math.sin(Cob)))
put('trig', 3, 'p-garden-bed', 4, third, sign=math.sqrt(73), pythagoras=13, **{'no-root': 265, 'no-two': math.sqrt(169 + 48)})

# ---------------------------------------------------------------- compare with the files
parts = 0
for course in ('series', 'trig'):
    for k in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{course}/problems-{k}.json'))
        for it in d['items']:
            for i, p in enumerate(it['parts'], 1):
                parts += 1
                w, where = p['widget'], f"{course} {k} {it['id']} part {i}"
                if (course, k, it['id'], i) not in MY:
                    say(False, where + ': no answer of mine')
                    continue
                mine, slips = MY[(course, k, it['id'], i)]
                kind = w['kind']
                wr = w.get('wrong', [])
                say({x_['id'] for x_ in wr} == set(slips), f"{where}: wrong ids {sorted(x_['id'] for x_ in wr)} against mine {sorted(slips)}")
                if kind == 'choice':
                    good = [o['id'] for o in w['options'] if o.get('correct')]
                    say(good == [mine], f'{where}: keyed {good}, mine {mine}')
                elif kind == 'expression':
                    eqn = '=' in w['answer']
                    for f_ in [w['answer']] + w.get('accept', []):
                        say(same(tex(f_), sp.sympify(mine), eqn), f'{where}: form {f_} is not my {mine}')
                    for x_ in wr:
                        if x_['id'] in slips:
                            say(same(tex(x_['tex']), sp.sympify(slips[x_['id']]), eqn), f"{where}: wrong {x_['id']} {x_['tex']} is not my {slips[x_['id']]}")
                            say(not same(tex(x_['tex']), sp.sympify(mine), eqn), f"{where}: wrong {x_['id']} equals the answer")
                elif 'answers' in w:
                    tol = w['tol']['abs']
                    say(len(mine) == len(w['answers']) and all(abs(a - b) <= 0.0051 for a, b in zip(sorted(mine), sorted(w['answers']))),
                        f"{where}: keyed {w['answers']}, mine {mine}")
                    for x_ in wr:
                        vals = sorted(float(v) for v in str(x_['value']).split(','))
                        if x_['id'] in slips:
                            t = max(x_.get('tol', {'abs': 1e-9})['abs'], 1e-9)
                            say(len(vals) == len(slips[x_['id']]) and all(abs(a - b) <= t + 1e-9 for a, b in zip(vals, sorted(slips[x_['id']]))),
                                f"{where}: wrong {x_['id']} {vals} against mine {sorted(slips[x_['id']])}")
                        say(vals != sorted(w['answers']), f"{where}: wrong {x_['id']} is the answer")
                else:
                    tol = w['tol']['abs']
                    key = float(w['answer'])
                    gap = abs(float(mine) - key)
                    say(gap <= 1e-4 or (gap <= tol and gap <= 0.01), f'{where}: keyed {key}, mine {float(mine)}')  # 0.01: a key built from rounded carried values
                    for x_ in wr:
                        t = x_.get('tol', {'abs': 1e-9})['abs']
                        if x_['id'] in slips:
                            sg = abs(float(slips[x_['id']]) - float(x_['value']))
                            say(sg <= t + 1e-9, f"{where}: wrong {x_['id']} {x_['value']} (band {t}) against my slip {float(slips[x_['id']])}")
                            say(sg <= 5.1e-3 or t >= 0.5, f"{where}: wrong {x_['id']} {x_['value']} sits {sg:.5f} from my slip {float(slips[x_['id']])}")
                        say(abs(float(x_['value']) - key) > tol + 1e-9, f"{where}: wrong {x_['id']} inside the key's band")
                say(bool(p.get('explain')) and bool(p.get('feedback', {}).get('correct')), f'{where}: no explanation or correct line')
print(f'mine: {parts} parts, {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
