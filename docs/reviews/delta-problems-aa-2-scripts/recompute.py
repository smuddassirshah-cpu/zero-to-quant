"""Delta read of the fix passes of problems 1.3 c, 0.2 a, 0.3 a and 0.2 b: every changed answer, band and
`wrong` value recomputed by two routes (exact with sympy or fractions, then quadrature, a root-finder, a grid,
a finite difference or enumeration), read against the content files as they stand.

Run from the repo root with the scratchpad venv Python: python docs/reviews/delta-problems-aa-2-scripts/recompute.py
A FINDING row is a fault the reader records; it does not fail the script.
"""
import itertools
import json
import math
from fractions import Fraction as Fr

import sympy as sp
from scipy import integrate, optimize

checks = fails = findings = 0


def ok(cond, msg, finding=None):
    global checks, fails, findings
    checks += 1
    if finding:
        findings += 1
        print(('FINDING ' if cond else 'FAIL    ') + msg + '   [' + finding + ']')
        if not cond:
            fails += 1
    elif not cond:
        fails += 1
        print('FAIL    ' + msg)


def close(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


SETS = {}


def part(course, n, item, k):
    key = (course, n)
    if key not in SETS:
        SETS[key] = json.load(open(f'app/content/courses/{course}/problems-{n}.json'))
    it = next(i for i in SETS[key]['items'] if i['id'] == item)
    return it['parts'][k - 1]


def W(course, n, item, k):
    return part(course, n, item, k)['widget']


def tol(t):
    return (t or {}).get('abs', 0)


def inband(v, w):
    return abs(v - float(w['answer'])) <= tol(w.get('tol')) + 1e-9


def num(course, n, item, k, a, b, takes=(), refuses=(), wrong=None, t=None):
    """answer by two routes a and b; the band takes each of `takes`, refuses each of `refuses`;
    wrong = {id: (route a, route b)} each matching the stored value to its own band."""
    w = W(course, n, item, k)
    where = f'{course} {n} {item} part {k}'
    ok(close(a, b, 1e-6 * max(1, abs(a))), f'{where}: two routes differ {a} {b}')
    ok(abs(float(w['answer']) - a) <= max(tol(w.get('tol')), 1e-9) + 1e-12, f'{where}: key {w["answer"]} not the value {a}')
    if t is not None:
        ok(close(tol(w.get('tol')), t, 1e-12), f'{where}: band {w.get("tol")} is not {t}')
    for v in takes:
        ok(inband(v, w), f'{where}: band refuses {v}')
    for v in refuses:
        ok(not inband(v, w), f'{where}: band takes {v}')
    stored = {x['id']: x for x in w.get('wrong', [])}
    if wrong is not None:
        ok(set(stored) == set(wrong), f'{where}: wrong ids {sorted(stored)} not {sorted(wrong)}')
        for wid, (ra, rb) in wrong.items():
            x = stored.get(wid)
            if not x:
                continue
            ok(close(ra, rb, 1e-6 * max(1, abs(ra))), f'{where}: wrong {wid} two routes differ {ra} {rb}')
            ok(abs(float(x['value']) - ra) <= max(tol(x.get('tol')), 6e-5 * max(1, abs(ra))), f'{where}: wrong {wid} stored {x["value"]} not {ra}')
            ok(abs(ra - float(x['value'])) <= tol(x.get('tol')) + 1e-9 or tol(x.get('tol')) == 0 and close(ra, x['value'], 1e-9),
               f'{where}: wrong {wid} band {x.get("tol")} about {x["value"]} misses the slip {ra}')
            ok(not inband(float(x['value']), w), f'{where}: wrong {wid} sits in the answer band')


def texts(course, n, item, k):
    p = part(course, n, item, k)
    fb = p['feedback']
    e = p.get('explain')
    return ' '.join([p['question'], fb.get('correct', ''), fb.get('generic', ''), *fb.get('byKey', {}).values(),
                     e['text'] if isinstance(e, dict) else (e or ''), str(p['widget'].get('accept', ''))])


def says(course, n, item, k, *needles):
    t = texts(course, n, item, k)
    for s in needles:
        ok(s in t, f'{course} {n} {item} part {k}: text does not print "{s}"')


x, t, u, r, q, a = sp.symbols('x t u r q a', real=True)

# ====================== fix pass 1.3 c ======================
# limits 4, level annuity part 5
A = (1 - sp.exp(-10 * r)) / r
exact = float(A.subs(r, sp.Rational(2, 100)))
series = sum((-1) ** k * 10 ** (k + 1) * 0.02 ** k / math.factorial(k + 1) for k in range(40))
num('limits', 4, 'p-level-annuity', 5, exact, series, takes=(9.0635, 9.0634, 9.0636, 0.181269 / 0.02), refuses=(9.0633, 9.0637, 9.065),
    wrong={'tangent': (9, 10 - 50 * 0.02), 'lost-ten': ((1 - math.exp(-0.02)) / 0.02, float(((1 - sp.exp(-r)) / r).subs(r, 0.02))),
           'no-divide': (1 - math.exp(-0.2), -math.expm1(-0.2))}, t=0.0001)
ok(round(math.exp(-0.2), 6) == 0.818731 and close((1 - 0.818731) / 0.02, 9.06345, 1e-9), 'annuity: 6-place route is not 9.06345')
ok(abs((1 - 0.8187) / 0.02 - 9.065) < 1e-9, 'annuity: 4-place route is not 9.065')

# limits 4, barbell part 4
V = 50 * sp.exp(-2 * u) + 50 * sp.exp(-8 * u) - 100 * sp.exp(-5 * u)
Vf = sp.lambdify(u, V)
h = 1e-4
V2 = float(sp.diff(V, u, 2).subs(u, 0))
V2n = (Vf(h) - 2 * Vf(0) + Vf(-h)) / h ** 2
ok(V2 == 900 and abs(V2n - 900) < 0.01, 'barbell: V\'\'(0) is not 900')
terms = [round(50 * math.exp(-0.02), 5), round(50 * math.exp(-0.08), 5), round(100 * math.exp(-0.05), 5)]
ok(terms == [49.00993, 46.15582, 95.12294], f'barbell: 5-place terms {terms}')
num('limits', 4, 'p-barbell-hedge', 4, 1000 * Vf(0.01), 1000 * float(V.subs(u, sp.Rational(1, 100))), takes=(43, 42.81, 1000 * (terms[0] + terms[1] - terms[2])), refuses=(42, 44, 45, 47),
    wrong={'tangent': (0, 1000 * (Vf(0) + float(sp.diff(V, u).subs(u, 0)) * 0.01)), 'second-order': (0.5 * 900 * 0.0001 * 1000, 0.5 * V2n * 0.01 ** 2 * 1000),
           'wrong-way': (1000 * Vf(-0.01), 1000 * float(V.subs(u, -sp.Rational(1, 100))))})
# limits 4, signal decay part 3 (wording only): the largest day
N = 60 * sp.log(1 + t) - 3 * t
ok(sp.solve(sp.diff(N, t), t) == [19] and max(range(0, 200), key=lambda d: 60 * math.log(1 + d) - 3 * d) == 19, 'signal decay: largest day is not 19')
ok(float(sp.diff(N, t).subs(t, 0)) == 57, 'signal decay: N\'(0) is not 57')
# limits 5, app adoption part 5 (wording only)
num('limits', 5, 'p-app-adoption', 5, 800 / 250, float(Fr(900 - 100, 250)), takes=(3.2,), refuses=(4.39, 3.6, 1.6),
    wrong={'actual': (math.log(81), optimize.brentq(lambda s: 1000 / (1 + 9 * math.exp(-s)) - 900, 0, 20)), 'from-zero': (900 / 250, 3.6), 'carried-users': (800 / 500, 1.6)})
ok(close(max(1000 * 9 * math.exp(-s / 100) / (1 + 9 * math.exp(-s / 100)) ** 2 for s in range(0, 2000)), 250, 1e-2), 'app adoption: top rate is not 250')
# limits 5, impact curve part 4
p = 2 * sp.atan(q / 500)
q1 = 500 * math.tan(0.5)
dp = float(sp.diff(p, q).subs(q, q1))
dpn = (2 * math.atan((q1 + 1e-3) / 500) - 2 * math.atan((q1 - 1e-3) / 500)) / 2e-3
num('limits', 5, 'p-impact-curve', 4, 1 / dp, 1 / dpn, takes=(325, 324.61, 324.6), refuses=(324, 326),
    wrong={'at-y': (1 / float(sp.diff(p, q).subs(q, 1)), (250000 + 1) / 1000), 'at-500': (1 / float(sp.diff(p, q).subs(q, 500)), 500), 'not-inverted': (dp, dpn)})
x_ni = next(z for z in W('limits', 5, 'p-impact-curve', 4)['wrong'] if z['id'] == 'not-inverted')
ok(tol(x_ni['tol']) == 0.0005 and all(abs(v - x_ni['value']) > 0.0005 for v in (0, 0.002, 0.4)) and abs(0.003 - x_ni['value']) <= 0.0005, 'impact curve: not-inverted band')

# integrals 4, dish and spindle parts 2 to 4
f = x / ((x + 1) * (x + 2))
Vy = float(2 * sp.pi * sp.integrate(x * f, (x, 0, 2)))
Vyn = 2 * math.pi * integrate.quad(lambda s: s * s / ((s + 1) * (s + 2)), 0, 2)[0]
Vx = float(sp.pi * sp.integrate(f ** 2, (x, 0, 2)))
Vxn = math.pi * integrate.quad(lambda s: (s / ((s + 1) * (s + 2))) ** 2, 0, 2)[0]
If = integrate.quad(lambda s: s / ((s + 1) * (s + 2)), 0, 2)[0]
num('integrals', 4, 'p-dish-and-spindle', 3, Vx, Vxn, takes=(0.141, 0.140, 0.1404, math.pi * 0.0447, 0.1408), refuses=(0.139, 0.143, 0.260),
    wrong={'square-integral': (math.pi * If ** 2, math.pi * math.log(4 / 3) ** 2), 'no-square': (math.pi * If, math.pi * math.log(4 / 3)), 'cross-term': (math.pi * (2 / 3 + 1), math.pi * 5 / 3)}, t=0.001)
ok(not inband(0.142, W('integrals', 4, 'p-dish-and-spindle', 3)), 'dish part 3: 0.142 is refused though the accept line prints 0.141 +- 0.001',
   finding='the accept line prints 0.142 as inside the band')
num('integrals', 4, 'p-dish-and-spindle', 4, Vy / Vx, Vyn / Vxn, takes=(15, 14.55, 14.6, 2.048 / 0.141, 2.0485 / 0.1403, 2.048 / 0.140), refuses=(14, 16),
    wrong={'inverse': (Vx / Vy, Vxn / Vyn), 'square-integral': (Vy / (math.pi * If ** 2), Vyn / (math.pi * math.log(4 / 3) ** 2))})
x_inv = next(z for z in W('integrals', 4, 'p-dish-and-spindle', 4)['wrong'] if z['id'] == 'inverse')
ok(tol(x_inv['tol']) == 0.005 and all(abs(v - x_inv['value']) > 0.005 for v in (0.141, 0.326, 0, 0.5)), 'dish part 4: inverse band')
# integrals 4: the ten accept lines print value and band of the stored key
for item, k, v, tt in [('p-impact-kernel', 3, 2 * math.log(1.5), 0.0005), ('p-impact-kernel', 4, 2 * math.log(2), 0.0005), ('p-flared-mouth', 1, 2 * math.pi, 0.0005),
                       ('p-flared-mouth', 2, math.pi ** 2 / 6, 0.0005), ('p-flared-mouth', 3, math.pi ** 2 / 2, 0.0005), ('p-flared-mouth', 4, math.sqrt(2) / 2, 0.0005),
                       ('p-dish-and-spindle', 2, Vy, 0.0005), ('p-rubber-seal', 1, math.pi / 2, 0.0005), ('p-rubber-seal', 3, 6 * math.pi ** 2, 0.005), ('p-rubber-seal', 5, 50 / math.pi ** 2, 0.005)]:
    w = W('integrals', 4, item, k)
    dp_ = 2 if tt == 0.005 else 3
    ok(close(w['answer'], v, 1e-9) and tol(w['tol']) == tt and f'{v:.{dp_}f}' in w['accept'] and f'\\pm {tt}' in w['accept'] and 'Any form' not in w['accept'], f'integrals 4 {item} part {k}: accept line or band')
    ok(inband(round(v, dp_), w), f'integrals 4 {item} part {k}: band refuses the printed rounding')
ok(close(integrate.quad(lambda s: 0.5 / math.sqrt(s), 0, 1)[0], 1, 1e-6) and close(0.5 * 1 / (1 - 0.5), 1), 'kernel part 1: unit-rule bound on [0, 1] is not 1')
ok(close(integrate.quad(lambda s: 0.5 / math.sqrt(s), 0, 4)[0], 2, 1e-6), 'kernel part 1: bound on [0, 4] is not 2')

# multivar 4, sprinkler part 1
th = sp.symbols('theta', real=True)
d_polar = sp.simplify((9 - (x ** 2 + sp.Symbol('y') ** 2)).subs({x: r * sp.cos(th), sp.Symbol('y'): r * sp.sin(th)}))
ok(sp.simplify(d_polar - (9 - r ** 2)) == 0, 'sprinkler: depth in polar is not 9 - r^2')
ok(all(close(9 - (rr * math.cos(tt)) ** 2 - (rr * math.sin(tt)) ** 2, 9 - rr ** 2) for rr in (0, 0.7, 1.9, 3) for tt in (0, 0.4, 1.2)), 'sprinkler: depth numerically')
w = W('multivar', 4, 'p-corner-sprinkler', 1)
ok(w['answer'] == '9-r^2' and {z['tex'] for z in w['wrong']} == {'9-r', '9r-r^3'}, 'sprinkler part 1: key or wrong')
ok(W('multivar', 4, 'p-corner-sprinkler', 2)['answer'] == '9r-r^3' and close(integrate.quad(lambda s: 9 * s - s ** 3, 0, 3)[0], 20.25) and close(float(sp.integrate(9 * r - r ** 3, (r, 0, 3))), 20.25), 'sprinkler: chain 2 to 3')
ok(close(20.25 * math.pi / 2, integrate.dblquad(lambda yy, xx: 9 - xx * xx - yy * yy, 0, 3, 0, lambda xx: math.sqrt(9 - xx * xx))[0], 1e-6), 'sprinkler: litres by a Cartesian double integral')

# multivar 4, drone landing, all five parts
g1 = float(sp.integrate(sp.exp(-x ** 2 / 32), (x, -sp.oo, sp.oo)))
g1n = integrate.quad(lambda s: math.exp(-s * s / 32), -math.inf, math.inf)[0]
ok(sp.simplify(sp.integrate(sp.exp(-x ** 2 / 32), (x, -sp.oo, sp.oo)) - 4 * sp.sqrt(2 * sp.pi)) == 0, 'drone 1: exact value is not 4 sqrt(2 pi)')
num('multivar', 4, 'p-drone-landing', 1, g1, g1n, takes=(10.0265,), refuses=(10.0264, 10.0266, 5.0133),
    wrong={'no-scale': (math.sqrt(math.pi), integrate.quad(lambda s: math.exp(-s * s), -math.inf, math.inf)[0]), 'inverted': (math.sqrt(math.pi) / (4 * math.sqrt(2)), math.sqrt(math.pi / 32)),
           'sigma-root32': (math.sqrt(32) * math.sqrt(2 * math.pi), math.sqrt(64 * math.pi))})
plane = integrate.dblquad(lambda yy, xx: math.exp(-(xx * xx + yy * yy) / 32), -60, 60, -60, 60)[0]
ok(close(plane, 32 * math.pi, 1e-5) and close(g1 ** 2, 32 * math.pi, 1e-9), 'drone 2: plane integral is not 32 pi')
w2, w3 = W('multivar', 4, 'p-drone-landing', 2), W('multivar', 4, 'p-drone-landing', 3)
ok(w2['answer'] == '32\\pi' and {z['id']: z['tex'] for z in w2['wrong']} == {'not-squared': '\\sqrt{32\\pi}', 'doubled': '2\\sqrt{32\\pi}', 'carried': '\\pi'}, 'drone 2: key or wrong')
ok(w3['answer'] == '\\frac{1}{32\\pi}' and {z['id']: z['tex'] for z in w3['wrong']} == {'not-inverted': '32\\pi', 'from-root': '\\frac{1}{\\sqrt{32\\pi}}', 'carried': '\\frac{1}{\\pi}'}, 'drone 3: key or wrong')
ok(close(1 / (32 * math.pi), 1 / plane, 1e-7) and f'{1 / (32 * math.pi):.4f}' == '0.0099', 'drone 3: c is not 0.0099')
c = 1 / (32 * math.pi)
disc = integrate.dblquad(lambda yy, xx: c * math.exp(-(xx * xx + yy * yy) / 32), -4, 4, lambda xx: -math.sqrt(16 - xx * xx), lambda xx: math.sqrt(16 - xx * xx))[0]
radial = float(sp.integrate(sp.exp(-r ** 2 / 32) * r, (r, 0, 4)))
ok(close(radial, 16 * (1 - math.exp(-0.5))), 'drone 4: radial integral is not 16(1 - e^-1/2)')
num('multivar', 4, 'p-drone-landing', 4, 1 - math.exp(-0.5), disc, takes=(0.3935,), refuses=(0.3934, 0.3936, 0.2212),
    wrong={'r-not-squared': (1 - math.exp(-4 / 32), -math.expm1(-0.125)), 'no-2pi': (c * radial, (1 - math.exp(-0.5)) / (2 * math.pi)), 'outside': (math.exp(-0.5), 1 - disc)})
a90 = optimize.brentq(lambda s: 1 - math.exp(-s * s / 32) - 0.9, 0, 50)
num('multivar', 4, 'p-drone-landing', 5, math.sqrt(32 * math.log(10)), a90, takes=(8.58, 8.584), refuses=(8.57, 8.59, 4.29),
    wrong={'no-root': (32 * math.log(10), a90 ** 2), 'tail-swap': (math.sqrt(-32 * math.log(0.9)), optimize.brentq(lambda s: math.exp(-s * s / 32) - 0.9, 0, 50)),
           'log10': (math.sqrt(32 * math.log10(10)), math.sqrt(32))})
ok(2 < a90 / 4 < 2.3, 'drone 5: "a little more than doubles"')
says('multivar', 4, 'p-drone-landing', 1, '4\\sqrt2', '\\sigma = 4', '10.0265')
for k in range(1, 6):
    tx = texts('multivar', 4, 'p-drone-landing', k)
    ok('/8}' not in tx and '8\\pi}' not in tx.replace('32\\pi}', '') and '2 m' not in tx, f'drone part {k}: a stale 8 or 2 m is printed')

# ====================== fix pass 0.2 a ======================
# functions 2, path and pipe
Ax, Ay, Bx, By, Dx, Dy = -2, 1, 5, 29, 12, 23
m = Fr(By - Ay, Bx - Ax)
cc = Ay - m * Ax
m_fit, c_fit = sp.symbols('m c')
sol = sp.solve([sp.Eq(Ay, m_fit * Ax + c_fit), sp.Eq(By, m_fit * Bx + c_fit)], [m_fit, c_fit])
ok(m == 4 and cc == 9 and sol[m_fit] == 4 and sol[c_fit] == 9, 'path: line is not y = 4x + 9')
num('functions', 2, 'p-path-and-pipe', 1, float(m), float(sol[m_fit]), takes=(4,), refuses=(0.5, 2),
    wrong={'flipped': (7 / 28, float(Fr(Bx - Ax, By - Ay))), 'lost-minus': (28 / 3, float(Fr(By - Ay, Bx - 2)))}, t=0)
m2 = -1 / m
c2 = Dy - m2 * Dx
ok(m2 == Fr(-1, 4) and c2 == 26, 'pipe: line is not y = -0.25x + 26')
num('functions', 2, 'p-path-and-pipe', 3, float(m2), -0.25, takes=(-0.25,), refuses=(-0.5, -2),
    wrong={'reciprocal': (0.25, float(1 / m)), 'negative': (-4, float(-m)), 'same': (4, float(m))})
# the foot of the perpendicular from D by a grid search along the path
best = min((s / 1000 for s in range(-2000, 5001)), key=lambda s: (s - Dx) ** 2 + (4 * s + 9 - Dy) ** 2)
xm = Fr(c2 - cc) / (m - m2)
num('functions', 2, 'p-path-and-pipe', 5, float(xm), best, takes=(4,), refuses=(2, 3.6),
    wrong={'y-value': (float(m * xm + cc), -0.25 * 4 + 26), 'sign-x': (17 / 3.75, float(Fr(26 - 9) / (4 - Fr(1, 4)))), 'constants': (35 / 4.25, float(Fr(26 + 9) / (4 + Fr(1, 4))))}, t=0)
ok(Ax < xm < Bx, 'path: the foot is not between A and B')
w2, w4 = W('functions', 2, 'p-path-and-pipe', 2), W('functions', 2, 'p-path-and-pipe', 4)
xs = sp.Symbol('x')


def line(s):
    return sp.sympify(s.replace('\\frac{x}{4}', '(x/4)').replace('\\frac{1}{4}', '(1/4)*').replace('x', '*x').replace('+*', '+').replace('-*', '-').lstrip('*').replace('(*x', '(x').replace('**x', '*x'), locals={'x': xs})


ok(w2['answer'] == '4x+9' and {z['id']: z['tex'] for z in w2['wrong']} == {'c-first': '4x+1', 'sign': '4x-7', 'flipped': '0.25x+1.5'}, 'path part 2: key or wrong')
ok(Ay + 4 * Ax == -7 and Ay - Fr(1, 4) * Ax == Fr(3, 2), 'path part 2: slips sign and flipped')
ok(w4['answer'] == '-0.25x+26' and {z['id']: z['tex'] for z in w4['wrong']} == {'c-first': '-0.25x+23', 'sign': '-0.25x+20', 'reciprocal': '0.25x+20'}, 'path part 4: key or wrong')
ok(Dy + m2 * Dx == 20 and Dy - Fr(1, 4) * Dx == 20, 'path part 4: slips sign and reciprocal')
for acc in w4['accept']:
    ok(sp.simplify(line(acc) - (-xs / 4 + 26)) == 0, f'path part 4: accept {acc} is not the pipe')

# functions 3, bakery trays (parts swapped), sledge, cubic, cultures
P = lambda s: -5 * s * s + 60 * s - 100
ok(part('functions', 3, 'p-bakery-trays', 4)['widget']['kind'] == 'choice' and next(o for o in W('functions', 3, 'p-bakery-trays', 4)['options'] if o.get('correct'))['id'] == 'left', 'bakery trays: part 4 is not the choice keyed left')
num('functions', 3, 'p-bakery-trays', 5, max(P(s) for s in range(0, 13)), P(Fr(-60, 2 * -5)), takes=(80,), refuses=(75,),
    wrong={'from-five': (P(5), 75), 'from-four': (P(4), 60), 'sign-square': (5 * 36 + 360 - 100, 440)})
num('functions', 3, 'p-sledge-cyclist', 1, 0.5 * 5 ** 2, float(Fr(1, 2) * 25), takes=(12.5,), refuses=(8, 12),
    wrong={'no-square': (0.5 * 5, 2.5), 'whole-square': ((0.5 * 5) ** 2, 6.25), 'no-half': (5 ** 2, 25)}, t=0.001)
num('functions', 3, 'p-sledge-cyclist', 2, 12.5 / 5, float(Fr(25, 2) / 5), takes=(2.5,), refuses=(2, 3),
    wrong={'times': (12.5 * 5, 62.5), 'distance': (12.5, 0.5 * 25)}, t=0.001)
ok(12.5 / 5 < 3, 'sledge part 2: "slower than the cyclist so far"')
num('functions', 3, 'p-sledge-cyclist', 3, 6, optimize.brentq(lambda s: 0.5 * s * s - 3 * s, 1, 20), takes=(6,), refuses=(2.5,),
    wrong={'no-half': (3, 3), 'lost-t': (math.sqrt(6), optimize.brentq(lambda s: 0.5 * s * s - 3, 0, 10))})
x_lt = next(z for z in W('functions', 3, 'p-sledge-cyclist', 3)['wrong'] if z['id'] == 'lost-t')
ok(tol(x_lt['tol']) == 0.05 and abs(2.5 - x_lt['value']) > 0.05 and abs(2 - x_lt['value']) > 0.05 and abs(2.4 - x_lt['value']) <= 0.05, 'sledge part 3: lost-t band')
hx = x ** 3 - 12 * x ** 2 + 36 * x
hf = sp.lambdify(x, hx)
ok(sp.factor(hx) == x * (x - 6) ** 2, 'cubic: does not factorise as x(x - 6)^2')
num('functions', 3, 'p-track-cubic', 1, hf(4), 4 * (4 - 6) ** 2, takes=(16,), refuses=(2,), wrong={'all-plus': (64 + 192 + 144, 400), 'cube-as-times': (3 * 4 - 12 * 16 + 36 * 4, -36)})
w = W('functions', 3, 'p-track-cubic', 2)
grid = [s / 100 for s in range(0, 801)]
ok(sorted(w['answers']) == sorted(sp.solve(hx, x)) == [0, 6] and [s for s in grid if abs(hf(s)) < 1e-9] == [0, 6], 'cubic part 2: roots')
turn = sorted(sp.solve(sp.diff(hx, x), x))
falls = [s for s in grid[1:-1] if hf(s + 0.005) < hf(s - 0.005)]
ok(turn == [2, 6] and hf(2) == 32 and hf(6) == 0 and hf(8) == 32 and min(falls) > 1.99 and max(falls) < 6.01, 'cubic part 3: turning points or where it falls')
w = W('functions', 3, 'p-track-cubic', 4)
ok(sorted(w['answers']) == sorted(set(sp.solve(hx - 32, x))) == [2, 8] and [s for s in grid if abs(hf(s) - 32) < 1e-9] == [2, 8], 'cubic part 4: h = 32')
ok(sp.expand((x - 2) ** 2 * (x - 8) - (hx - 32)) == 0, 'cubic part 4: h - 32 is not (x - 2)^2 (x - 8)')
opts = {o['id']: o['text'] for o in W('functions', 3, 'p-track-cubic', 3)['options']}
ok(opts == {'middle': 'For $2 < x < 6$', 'start': 'For $0 < x < 2$', 'end': 'For $6 < x < 8$', 'first': 'For $0 < x < 6$'}, 'cubic part 3: options')
count_line = part('functions', 3, 'p-track-cubic', 2)['feedback']['byKey']['count']
ok('(x - 3)^2' in count_line and '(x - 6)^2' not in count_line, 'functions 3 p-track-cubic part 2: the "count" line names the factor ' + ('(x - 3)^2' if '(x - 3)^2' in count_line else '?') + ', the old curve',
   finding='stale line: the track is now x(x - 6)^2')
for k in range(1, 5):
    tx = texts('functions', 3, 'p-track-cubic', k).replace(count_line, '')
    ok('(x - 3)' not in tx and '3x^2' not in tx.replace('12x^2', ''), f'cubic part {k}: another stale line of the old curve')
ok(f'{2 ** 3.3:.3f}' == '9.849' and f'{2 ** 3.4:.3f}' == '10.556' and round(200 * 9.849) == 1970 and round(200 * 10.556) == 2111, 'two cultures part 4: given powers')
ok(3.3 < optimize.brentq(lambda s: 200 * 2 ** s - 1000 - 300 * s, 3, 4) < 3.35, 'two cultures part 4: crossing')
# equations 2 and 3
best_p = max(pp for pp in range(1, 1000) if 4500 + 35 * pp <= 30000)
num('equations', 2, 'p-climbing-wall', 4, best_p / 100, math.floor(Fr(300 - 45, 35) * 100) / 100, takes=(7.28,), refuses=(7.29, 7.2857, 7.3),
    wrong={'rounded-up': (round(255 / 35, 2), 7.29), 'no-fee': (300 / 35, float(Fr(300, 35))), 'pence': (best_p, 728)})
ok(max(n for n in range(100) if 45 + 8 * n <= 300) == 31 and (213 - 45) / 8 == 21, 'climbing wall: 21 and 31')
ok(len([F_ for F_ in range(-200, 200) if -25 <= (F_ - 32) / 1.8 <= -15]) == 19 == 5 - (-13) + 1, 'fridge part 4: 19 readings')
s_ = sp.Symbol('s')
ok(sp.solve(sp.Eq(sp.Rational(4, 100) * s_ + sp.Rational(65, 1000) * (12000 - s_), 660), s_) == [4800] and close(0.04 * 4800 + 0.065 * 7200, 660), 'interest split part 3: 4800')
ok(sorted(sp.solve(45 - 5 * (t - 2) ** 2, t)) == [-1, 5] and sorted(sp.solve(45 - 5 * (t - 2) ** 2 - 40, t)) == [1, 3], 'stone throw parts 2 and 4')
ok(W('equations', 2, 'p-interest-split', 1)['answer'] == '12000-s' and 'no comma' in part('equations', 2, 'p-interest-split', 1)['question'] and 'no comma' in part('equations', 2, 'p-interest-split', 2)['question'], 'interest split: no comma')

# ====================== fix pass 0.3 a ======================
fl = range(14)
cups = len(list(itertools.combinations(fl, 3)))
cones = len(list(itertools.permutations(fl, 3)))
items = [('cup', s) for s in itertools.combinations(fl, 3)] + [('cone', s) for s in itertools.permutations(fl, 3)]
buys = len([(i, top) for i in items for top in (None, 1, 2, 3, 4)])
num('counting', 1, 'p-ice-cream-van', 1, math.comb(14, 3), cups, takes=(364,), refuses=(165,),
    wrong={'ordered': (14 * 13 * 12, cones), 'repeats': (14 ** 3, len(list(itertools.product(fl, repeat=3)))), 'times': (14 * 3, 42)}, t=0)
num('counting', 1, 'p-ice-cream-van', 2, math.perm(14, 3), cones, takes=(2184,), refuses=(990,),
    wrong={'times-three': (364 * 3, cups * 3), 'added': (364 + 6, cups + math.factorial(3)), 'carried': (2184 * 6, cones * 6)}, t=0)
num('counting', 1, 'p-ice-cream-van', 3, 364 + 2184, len(items), takes=(2548,), refuses=(1155,),
    wrong={'multiplied': (364 * 2184, cups * cones), 'carried': (2184 + 13104, cones + cones * 6)}, t=0)
num('counting', 1, 'p-ice-cream-van', 4, 2548 * 5, buys, takes=(12740,), refuses=(5775,),
    wrong={'no-none': (2548 * 4, len(items) * 4), 'added': (2548 + 5, len(items) + 5), 'carried': (794976 * 5, cups * cones * 5)}, t=0)
for k in range(1, 5):
    tx = texts('counting', 1, 'p-ice-cream-van', k)
    ok(not any(s in tx for s in ('11 ', '165', '990', '1155', '5775', '1331', 'orders can')), f'ice-cream part {k}: a stale number of the 11-flavour item')
# team photo part 4 by enumeration (wording only)
n192 = sum(1 for o in itertools.permutations(range(7)) if o[3] == 0 and abs(o.index(1) - o.index(2)) == 1)
n720 = sum(1 for o in itertools.permutations(range(7)) if o[3] == 0)
ok(n192 == 192 == W('counting', 1, 'p-team-photo', 4)['answer'] and n720 == 720, 'team photo: 720 and 192')
ok(close(Fr(math.comb(17, 2), math.comb(80, 2)), 0.043038, 1e-6) and 80 - (45 + 38 - 20) == 17, 'leisure centre: 17 and 136/3160')
ok(math.comb(11, 4) == 330 and math.comb(5, 4) == 5 and 330 - 5 == 325, 'quiz team part 3')
ok(math.hypot(9, 12) + math.hypot(12, 16) == 35 and round(3500 - 100 * math.sqrt(793)) == 684 and round(250 * math.sqrt(52)) == 1803, 'orienteering and power line')
ang = math.degrees(math.acos(-145 / (math.hypot(40, 70) * math.hypot(2.5, 3.5))))
ok(round(ang) == 115 and 40 * 2.5 - 70 * 3.5 == -145, 'grain merchant part 4')
for c_, n_, it_, k_ in [('counting', 3, 'p-sail-ring', 3), ('functions', 4, 'p-car-park', 2), ('functions', 4, 'p-ticket-bonus', 2)]:
    ok(W(c_, n_, it_, k_).get('form') == 'simplified' and 'form' in part(c_, n_, it_, k_)['feedback']['byKey'], f'{it_} part {k_}: form or its line')
ok(sp.expand(3 + sp.Rational(5, 2) * (t - 2) - (sp.Rational(5, 2) * t - 2)) == 0 and sp.simplify((5 * t - 4) / 2 - (sp.Rational(5, 2) * t - 2)) == 0, 'car park part 2: 2.5t - 2 and (5t - 4)/2')
n = sp.Symbol('n')
ok(sp.expand(sp.Rational(2, 10) * (25 * n - 500) - (5 * n - 100)) == 0, 'ticket bonus part 2')

# ====================== fix pass 0.2 b ======================
ok(sp.expand((x + 4) * (x + 11)) == x ** 2 + 15 * x + 44 and sp.factor(x ** 2 + 15 * x + 36) == (x + 3) * (x + 12), 'cinema: expansion or factors')
pairs = [(i, j) for i in range(1, 37) for j in range(i, 37) if i * j == 36]
ok(pairs == [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)] and [pq for pq in pairs if sum(pq) == 15] == [(3, 12)], 'cinema part 2: pairs of 36')
w = W('quadratics', 1, 'p-cinema-block', 1)
ok(w['answer'] == 'x^2+15x+44' and {z['id']: z['tex'] for z in w['wrong']} == {'corner': 'x^2+44', 'added': 'x^2+15x+15', 'swapped': 'x^2+44x+15'}, 'cinema part 1: key or wrong')
w = W('quadratics', 1, 'p-cinema-block', 2)
ok(w['answer'] == '(x+3)(x+12)' and {z['id']: z['tex'] for z in w['wrong']} == {'sum-thirteen': '(x+4)(x+9)', 'square': '(x+6)^2', 'signs': '(x-3)(x-12)'}, 'cinema part 2: key or wrong')
ok(sp.expand((x + 4) * (x + 9)) == x ** 2 + 13 * x + 36 and sp.expand((x + 6) ** 2) == x ** 2 + 12 * x + 36 and sp.expand((x - 3) * (x - 12)) == x ** 2 - 15 * x + 36, 'cinema part 2: the slips expand as their lines say')
seats_old = sum(1 for row in range(10 + 4) for seat in range(10 + 11))
num('quadratics', 1, 'p-cinema-block', 3, seats_old - 8, (10 + 3) * (10 + 12), takes=(286,), refuses=(228,),
    wrong={'kept': (seats_old, 14 * 21), 'sum-thirteen': (14 * 19, sum(1 for row in range(14) for seat in range(19))), 'square': (16 ** 2, 256)}, t=0)
ok(not [k for k in range(0, 50) if 2 * k == 15] and 44 - 36 == 8 and 44 - 25 == 19 and sp.expand((x + 5) ** 2) == x ** 2 + 10 * x + 25, 'cinema part 4: options')
opts = {o['id']: o['text'] for o in W('quadratics', 1, 'p-cinema-block', 4)['options']}
ok('8 seats' in opts['six'] and '19 seats' in opts['five'] and '2k = 15' in opts['no-middle'] and '44' in opts['last-term'], 'cinema part 4: option texts')
ok(sp.factor(x ** 2 + 11 * x + 30) == (x + 5) * (x + 6) and sp.factor(2 * x ** 2 + 19 * x + 45) == (x + 5) * (2 * x + 9), 'allotment: factors')
ok([(i, j) for i in range(1, 91) for j in range(i, 91) if i * j == 90 and i + j == 19] == [(9, 10)] and [(i, j) for i in range(1, 31) for j in range(i, 31) if i * j == 30 and i + j == 11] == [(5, 6)], 'allotment: pairs by search')
ok(sp.expand((x + 3) * (x + 10)) == x ** 2 + 13 * x + 30 and sp.expand((x + 2) * (x + 15)) == x ** 2 + 17 * x + 30 and sp.expand((x + 9) * (x + 10)) == x ** 2 + 19 * x + 90
   and sp.expand((2 * x + 5) * (x + 9)) == 2 * x ** 2 + 23 * x + 45, 'allotment: the slips expand as their lines say')
ok(sp.factor(x ** 2 + 11 * x + 30 + 2 * x ** 2 + 19 * x + 45) == 3 * (x + 5) ** 2, 'allotment part 3: total')
for (k, key, wr) in [(1, '(x+5)(x+6)', {'sum-thirteen': '(x+3)(x+10)', 'sum-seventeen': '(x+2)(x+15)'}), (2, '(x+5)(2x+9)', {'no-group': '(x+9)(x+10)', 'wrong-pair': '(2x+5)(x+9)'}),
                     (3, '3(x+5)^2', {'both-sides': '6(x+5)^2', 'lost-square': '3(x+5)'})]:
    w = W('quadratics', 1, 'p-allotment-plots', k)
    ok(w['answer'] == key and {z['id']: z['tex'] for z in w['wrong']} == wr, f'allotment part {k}: key or wrong')
num('quadratics', 1, 'p-allotment-plots', 4, 3 * (5 + 5) ** 2, (25 + 55 + 30) + (50 + 95 + 45), takes=(300,), refuses=(363,),
    wrong={'three-squared': ((3 * 10) ** 2, 900), 'both-sides': (6 * 10 ** 2, 600)}, t=0)
ok(10 * 11 == 110 and 10 * 19 == 190, 'allotment part 4: plots at x = 5')
gap = t ** 2 - 6 * t + 6
ok(sp.expand((t - 3) ** 2 - 3 - gap) == 0 and sp.expand((t ** 2 - 6 * t + 10) - gap) == 4, 'bus chase part 3: square form, 4 m less than Jo')
first = optimize.brentq(lambda s: s * s - 6 * s + 6, 0, 3)
later = optimize.brentq(lambda s: s * s - 6 * s + 6, 3, 9)
num('quadratics', 2, 'p-bus-chase', 3, 3 - math.sqrt(3), first, takes=(1.27, 1.268), refuses=(1.26, 1.28, 1.59),
    wrong={'larger': (3 + math.sqrt(3), later), 'half-root': (6 / 2 - math.sqrt(12), 3 - math.sqrt(36 - 24)), 'no-root': (3 - 3, 0)}, t=0.005)
ok(sorted(float(s) for s in sp.solve(gap, t)) == sorted([float((6 - sp.sqrt(12)) / 2), float((6 + sp.sqrt(12)) / 2)]), 'bus chase part 3: formula route')
vmin = optimize.brentq(lambda v: v * v - 40, 0, 10)
num('quadratics', 2, 'p-bus-chase', 4, math.sqrt(40), vmin, takes=(6.32, 6.33, 6.325), refuses=(6.3, 6.31, 6.34),
    wrong={'no-root': (40, vmin ** 2), 'no-four': (math.sqrt(10), optimize.brentq(lambda v: v * v - 10, 0, 10))}, t=0.006)
ok(6.32 ** 2 < 40 < 6.33 ** 2, 'bus chase part 4: 6.32 falls short, 6.33 reaches')
hfl = 15 + 10 * t - 5 * t ** 2
ok(sp.expand(-5 * (t - 1) ** 2 + 20 - hfl) == 0 and sorted(sp.solve(hfl, t)) == [-1, 3] and sorted(sp.solve(hfl - 15, t)) == [0, 2], 'flare: square form and roots')
ok(all(close(a_, b_, 5e-6) for a_, b_ in zip(sorted(W('quadratics', 2, 'p-cliff-stone', 4)['answers']), [1 - math.sqrt(0.4), 1 + math.sqrt(0.4)])), 'flare part 4')
for k in range(1, 5):
    tx = texts('quadratics', 2, 'p-cliff-stone', k) + ' ' + next(i for i in SETS[('quadratics', 2)]['items'] if i['id'] == 'p-cliff-stone')['prose']
    ok(not any(s in tx.lower() for s in ('stone', 'cliff', 'throw', 'beach', 'ground')), f'flare part {k}: a word of the old story is left')
ok(sp.expand(-sp.Rational(1, 5) * (x - 10) ** 2 + 20 - (-sp.Rational(1, 5) * x * (x - 20))) == 0, 'canal arch part 3: key')
ok(sp.expand((3 * x - x ** 2 / 2) - x / 2 - (sp.Rational(5, 2) * x - x ** 2 / 2)) == 0, 'sprinkler bank part 1: key')
# equations 4
xx, yy = sp.symbols('x y')
both = sp.solve([sp.Eq(xx + yy, 500), sp.Eq(sp.Rational(15, 100) * xx + sp.Rational(4, 10) * yy, sp.Rational(1, 4) * (xx + yy))], [xx, yy])
keyed = sp.solve([sp.Eq(xx + yy, 500), sp.Eq(sp.Rational(15, 100) * xx + sp.Rational(4, 10) * yy, 125)], [xx, yy])
brute = [(i, 500 - i) for i in range(0, 501) if 15 * i + 40 * (500 - i) == 25 * 500]
ok(both == keyed == {xx: 300, yy: 200} and brute == [(300, 200)], 'salt solutions: both balances give 300 and 200')
w = W('equations', 4, 'p-salt-solutions', 1)
ok(any(z['id'] == 'both-letters' and z['tex'] == '0.15x+0.4y=0.25(x+y)' for z in w['wrong']) and '0.15x+0.4y=0.25(500)' in w['accept'] and 'as one number' in part('equations', 4, 'p-salt-solutions', 1)['question'], 'salt solutions part 1')
ok(49 + 32 == 81 and math.isqrt(81) == 9 and 81 - 7 * 9 == 18 and W('equations', 4, 'p-remote-cars', 3)['answer'] == 9 and W('equations', 4, 'p-remote-cars', 4)['answer'] == 18, 'remote cars parts 3 and 4')

# ====================== proposed (finding 2): the drone within 6 m, off the exam's 0.3935 ======================
import glob  # noqa: E402

exam = json.load(open('app/content/exams/topic-1.3.json'))
gd = next(i for i in exam['items'] if i['id'] == 'c-gauss-disc')
ok('0.3935' in json.dumps(gd) and close(W('multivar', 4, 'p-drone-landing', 4)['answer'], 0.3935), 'exam item c-gauss-disc and the drone part 4 no longer share 0.3935')
p6 = 1 - math.exp(-36 / 32)
p6n = integrate.dblquad(lambda yy_, xx_: c * math.exp(-(xx_ * xx_ + yy_ * yy_) / 32), -6, 6, lambda xx_: -math.sqrt(36 - xx_ * xx_), lambda xx_: math.sqrt(36 - xx_ * xx_))[0]
ok(close(p6, p6n, 1e-7) and f'{p6:.4f}' == '0.6753', f'proposed: within 6 m is {p6}')
ok(f'{1 - math.exp(-6 / 32):.4f}' == '0.1710' and f'{p6 / (2 * math.pi):.4f}' == '0.1075' and f'{math.exp(-36 / 32):.4f}' == '0.3247', 'proposed: the three slips')
rad6 = float(sp.integrate(sp.exp(-r ** 2 / 32) * r, (r, 0, 6)))
ok(close(c * rad6, p6 / (2 * math.pi), 1e-9) and close(rad6, 16 * p6), 'proposed: radial integral 16(1 - e^-9/8)')
ok(1.4 < a90 / 6 < 1.45, 'proposed: 8.58 / 6')
ok(not any(v in json.dumps(json.load(open(f_))) for v in ('0.6753', '0.3247', '0.1710', '0.1075')
           for f_ in ['app/content/exams/topic-1.3.json'] + glob.glob('app/content/courses/multivar/*.json')), 'proposed: a new value is already in multivar or the 1.3 exam')

# ====================== every numeric part of the 17 changed files ======================
FILES = [('limits', 4), ('limits', 5), ('integrals', 4), ('multivar', 4), ('equations', 2), ('equations', 3), ('functions', 1), ('functions', 2), ('functions', 3),
         ('counting', 1), ('counting', 2), ('counting', 3), ('functions', 4), ('quadratics', 1), ('quadratics', 2), ('quadratics', 3), ('equations', 4)]
nparts = 0
for course, n_ in FILES:
    d = json.load(open(f'app/content/courses/{course}/problems-{n_}.json'))
    for it in d['items']:
        for k, p_ in enumerate(it['parts'], 1):
            w = p_['widget']
            by = p_['feedback'].get('byKey', {})
            for z in w.get('wrong', []):
                ok(z['id'] in by, f'{course} {n_} {it["id"]} part {k}: wrong {z["id"]} has no byKey line')
            if w['kind'] != 'numeric' or 'answers' in w:
                continue
            nparts += 1
            bands = [('answer', float(w['answer']) - tol(w.get('tol')), float(w['answer']) + tol(w.get('tol')))]
            bands += [(z['id'], float(z['value']) - tol(z.get('tol')), float(z['value']) + tol(z.get('tol'))) for z in w.get('wrong', [])]
            for i in range(len(bands)):
                for j in range(i + 1, len(bands)):
                    ok(bands[i][2] < bands[j][1] or bands[j][2] < bands[i][1], f'{course} {n_} {it["id"]} part {k}: bands {bands[i][0]} and {bands[j][0]} meet')

print(f'recompute.py: {checks} checks, {fails} failures, {findings} finding rows; band check on {nparts} single-value numeric parts of {len(FILES)} files')
raise SystemExit(1 if fails else 0)
