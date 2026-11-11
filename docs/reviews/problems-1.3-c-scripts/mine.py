"""Second read, problems 1.3 (c): the reader's own answers and slips for limits 4 and 5, integrals 4, multivar 4 and 5.

Every part is worked here from its question text: once exactly (sympy), once by a second route (mpmath quadrature, a numeric
limit, a central difference, a grid scan). Each wrong[] value is rebuilt from the slip its feedback names. The script then
reads the JSON and compares: my answer inside the key's band, my slip value inside that wrong entry's band, expression keys
equal to mine at sample points. Claims in feedback and explanations are checked at the end of each block.

Run from the repo root:  <venv>/bin/python docs/reviews/problems-1.3-c-scripts/mine.py
"""
import json
import math
import sys

import mpmath as mp
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


def band(t):
    return (t or {}).get('abs', 0) + 1e-9


def num(item, part, mine, second=None, wrongs=None, label=''):
    """mine: my exact value; second: the same by another route; wrongs: {id: my slip value}."""
    w = item['parts'][part - 1]['widget']
    where = f"{item['id']} part {part}"
    ok(w['kind'] == 'numeric', f'{where}: not numeric')
    ok(abs(float(mine) - w['answer']) <= band(w.get('tol')), f"{where}: mine {float(mine)} vs key {w['answer']} ±{w.get('tol')}")
    if second is not None:
        ok(abs(float(mine) - float(second)) <= 1e-6 * max(1, abs(float(mine))), f'{where}: two routes differ {float(mine)} {float(second)}')
    have = {x['id']: x for x in w.get('wrong', [])}
    wrongs = wrongs or {}
    ok(set(have) == set(wrongs), f'{where}: wrong ids {sorted(have)} vs mine {sorted(wrongs)}')
    for k, v in wrongs.items():
        if k in have:
            x = have[k]
            ok(abs(float(v) - x['value']) <= band(x.get('tol') or w.get('tol')), f"{where}: wrong {k}: slip gives {float(v)}, entry {x['value']}")
            ok(abs(x['value'] - w['answer']) > band(w.get('tol')), f'{where}: wrong {k} inside the answer band')


def keyfn(tex, sym):
    """A small LaTeX reader for the keys in these five files (fractions, powers, e^{..}, \\ln, \\sqrt, \\pi)."""
    s = tex
    for a, b in [('\\left', ''), ('\\right', ''), ('\\cdot', '*'), ('\\pi', '(pi)'), ('\\ln', 'log')]:
        s = s.replace(a, b)
    while '\\frac' in s or '\\sqrt' in s:
        i = max(s.rfind('\\frac'), s.rfind('\\sqrt'))
        isfrac = s.startswith('\\frac', i)

        def grp(j):
            assert s[j] == '{', s
            d, k = 0, j
            while True:
                d += s[k] == '{'
                d -= s[k] == '}'
                if d == 0:
                    return s[j + 1:k], k + 1
                k += 1
        a, j = grp(i + 5)
        if isfrac:
            b, j = grp(j)
            s = s[:i] + f'(({a})/({b}))' + s[j:]
        else:
            s = s[:i] + f'sqrt({a})' + s[j:]
    s = s.replace('re^', 'r*e^').replace('{', '(').replace('}', ')').replace('^', '**')
    from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, standard_transformations)
    loc = {str(v): v for v in sym}
    loc.update(e=sp.E, pi=sp.pi, log=sp.log, sqrt=sp.sqrt)
    return parse_expr(s, local_dict=loc, transformations=standard_transformations + (implicit_multiplication_application,))


def expr(item, part, mine, sym, wrongs=None, up_to_const=False):
    w = item['parts'][part - 1]['widget']
    where = f"{item['id']} part {part}"
    ok(w['kind'] == 'expression', f'{where}: not expression')
    pts = [0.37, 0.81, 1.9, 2.6]

    def same(a, b):
        ds = [complex((a - b).subs({s: p + 0.11 * i for i, s in enumerate(sym)}).evalf()) for p in pts] if sym else [complex((a - b).evalf())]
        if up_to_const:
            return all(abs(d - ds[0]) < 1e-9 for d in ds)
        return all(abs(d) < 1e-9 for d in ds)
    for t in [w['answer']] + list(w.get('accept', [])):
        ok(same(keyfn(t, sym), mine), f'{where}: key form {t} is not my answer')
    have = {x['id']: x for x in w.get('wrong', [])}
    wrongs = wrongs or {}
    ok(set(have) == set(wrongs), f'{where}: wrong ids {sorted(have)} vs mine {sorted(wrongs)}')
    for k, v in wrongs.items():
        if k in have:
            ok(same(keyfn(have[k]['tex'], sym), v), f"{where}: wrong {k}: entry {have[k]['tex']} is not my slip {v}")
            ok(not same(v, mine), f'{where}: wrong {k} equals the answer')


E, ln, pi = sp.E, sp.log, sp.pi
quad = lambda f, *lim: mp.quad(f, list(lim))  # noqa: E731

# ============================================================ limits 4
L4 = load('limits', 4)
s, t, u, r = sp.symbols('s t u r', positive=True)

it = L4['p-spread-quote']
R = 900 * s / (2 + s) ** 2
dR = sp.simplify(sp.diff(R, s))
uu, vv = 900 * s, (2 + s) ** 2
expr(it, 1, dR, [s], {'swapped': (uu * sp.diff(vv, s) - sp.diff(uu, s) * vv) / vv ** 2, 'added': (sp.diff(uu, s) * vv + uu * sp.diff(vv, s)) / vv ** 2,
                      'bottom-unsquared': 900 * (2 - s) / (2 + s), 'product-of-derivatives': sp.diff(uu, s) * sp.diff(1 / vv, s)})
num(it, 2, sp.solve(dR, s)[0], max((float(R.subs(s, k / 1000)), k / 1000) for k in range(0, 20001))[1], {'pole': -2, 'start': 0})
num(it, 3, R.subs(s, 2), None, {'no-s': sp.Rational(900, 16), 'bottom-unsquared': sp.Rational(1800, 4), 'slope': dR.subs(s, 2)})
num(it, 4, R.subs(s, 1), max(float(R.subs(s, k / 1000)) for k in range(0, 1001)), {'ignored-cap': R.subs(s, 2), 'slope': dR.subs(s, 1), 'start': R.subs(s, 0)})
num(it, 5, dR.subs(s, 1) / 4, (float(R.subs(s, 1 + 1e-6)) - float(R.subs(s, 1 - 1e-6))) / 2e-6 * 0.25,
    {'true-gain': R.subs(s, sp.Rational(5, 4)) - R.subs(s, 1), 'full-cap': dR.subs(s, 1) * sp.Rational(5, 4), 'sign': -dR.subs(s, 1) / 4, 'flat-top': 0})
ok(dR.subs(s, 1) == sp.Rational(900, 27), 'spread: R\'(1) = 900/27')
ok(sp.diff(R, s, 2).subs(s, 1) < 0, 'spread: curve below tangent at 1')
ok(abs(float(R.subs(s, sp.Rational(5, 4)) - R.subs(s, 1)) - 6.51) < 0.005, 'spread: true gain 6.51')

it = L4['p-signal-decay']
N = 60 * ln(1 + t) - 3 * t
num(it, 1, sp.limit(N / t, t, 0), float(N.subs(t, 1e-7)) / 1e-7, {'no-cost': 60, 'cost-sign': 63, 'zero-over-zero': 0})
num(it, 2, sp.limit(N / t, t, sp.oo), None, {'start': 57, 'lost-cost': 0, 'cost-sign': 3})
ok(abs(float((N / t).subs(t, 10 ** 9)) + 3) < 1e-5, 'signal: N/t far out')
num(it, 3, sp.solve(sp.diff(N, t), t)[0], max((float(N.subs(t, k)), k) for k in range(0, 200))[1], {'dropped-one': 20, 'start-rate': 57})
num(it, 4, N.subs(t, 19), 60 * math.log(20) - 57, {'dropped-one': N.subs(t, 20), 'no-cost': 60 * ln(20), 'log-ten': 60 * sp.log(20, 10) - 57})
ok(sp.diff(N, t, 2).subs(t, 19) < 0, 'signal: maximum')

it = L4['p-barbell-hedge']
V = 50 * E ** (-2 * u) + 50 * E ** (-8 * u) - 100 * E ** (-5 * u)
expr(it, 1, sp.diff(V, u), [u], {'short-sign': -100 * E ** (-2 * u) - 400 * E ** (-8 * u) - 500 * E ** (-5 * u),
                                 'lost-inner': -50 * E ** (-2 * u) - 50 * E ** (-8 * u) + 100 * E ** (-5 * u), 'no-minus': -sp.diff(V, u)})
num(it, 2, sp.diff(V, u).subs(u, 0), (float(V.subs(u, 1e-6)) - float(V.subs(u, -1e-6))) / 2e-6, {'short-sign': -1000})
num(it, 3, sp.diff(V, u, 2).subs(u, 0), (float(V.subs(u, 1e-4)) + float(V.subs(u, -1e-4))) / 1e-8, {'first-power': 0, 'short-sign': 200 + 3200 + 2500, 'sign': -900})
num(it, 4, 1000 * V.subs(u, sp.Rational(1, 100)), 1000 * (50 * math.exp(-.02) + 50 * math.exp(-.08) - 100 * math.exp(-.05)),
    {'tangent': 0, 'wrong-way': 1000 * V.subs(u, -sp.Rational(1, 100))})
ok(all(float(V.subs(u, k / 100)) > 0 for k in range(-300, 301) if k), 'barbell: V > 0 away from 0 (any shift raises the value)')
ok(abs(1000 * (round(50 * math.exp(-.02), 5) + round(50 * math.exp(-.08), 5) - round(100 * math.exp(-.05), 5)) - 42.81) < 1e-6, 'barbell: 5 dp working gives 42.81')

it = L4['p-level-annuity']
A = (1 - E ** (-10 * r)) / r
dA = sp.diff(A, r)
num(it, 1, sp.limit(A, r, 0), float(A.subs(r, 1e-8)), {'upside-down': sp.Rational(1, 10), 'top-only': 0, 'lost-inner': 1})
ok(abs(float(quad(lambda x: mp.e ** (-0.02 * x), 0, 10)) - float(A.subs(r, 0.02))) < 1e-9, 'annuity: A(r) is the integral of e^{-rt} over 10 years')
uu, vv = 1 - E ** (-10 * r), r
expr(it, 2, dA, [r], {'swapped': (uu * 1 - sp.diff(uu, r) * vv) / vv ** 2, 'lost-inner': (r * E ** (-10 * r) - uu) / r ** 2, 'bottom-unsquared': (sp.diff(uu, r) * vv - uu) / r})
num(it, 3, sp.limit(dA, r, 0), float(sp.N(dA.subs(r, sp.Rational(1, 10 ** 9)), 40)), {'no-two': -100, 'sign': 50, 'value': 10})
ok(sp.simplify(sp.diff(10 * r * E ** (-10 * r) - (1 - E ** (-10 * r)), r) + 100 * r * E ** (-10 * r)) == 0, 'annuity: top derivative is -100 r e^{-10r}')
num(it, 4, 10 - 50 * sp.Rational(2, 100), None, {'carried-no-two': 10 - 100 * 0.02, 'sign': 10 + 1, 'change-only': -1})
num(it, 5, A.subs(r, sp.Rational(2, 100)), (1 - math.exp(-0.2)) / 0.02, {'tangent': 9, 'lost-ten': (1 - math.exp(-0.02)) / 0.02, 'no-divide': 1 - math.exp(-0.2)})
ok(sp.diff(A, r, 2).subs(r, 0.01) > 0, 'annuity: A bends up')
ok(abs(float(A.subs(r, 0.02)) - 9 - 0.0635) < 5e-5, 'annuity: tangent about 6p low')

# ============================================================ limits 5
L5 = load('limits', 5)
x, q = sp.symbols('x q', real=True)
it = L5['p-camera-pan']
th = sp.atan(x / 30)
dth = sp.simplify(sp.diff(th, x))
expr(it, 1, dth, [x], {'lost-inner': 900 / (900 + x ** 2), 'plain-arctan': 1 / (1 + x ** 2), 'arcsin': 1 / sp.sqrt(1 - x ** 2 / 900)})
num(it, 2, dth.subs(x, 40) * 20, (math.atan((40 + 20e-6) / 30) - math.atan((40 - 20e-6) / 30)) / 2e-6,
    {'no-speed': dth.subs(x, 40), 'lost-inner': sp.Rational(900, 2500) * 20, 'divided': dth.subs(x, 40) / 20})
num(it, 3, (th.subs(x, 30) - th.subs(x, -30)) / 3, (math.atan(1) - math.atan(-1)) / (60 / 20), {'half-sweep': pi / 4 / 3, 'per-metre': pi / 2 / 60, 'degrees': 30})
xs = sp.sqrt(3600 / pi - 900)
num(it, 4, xs, mp.findroot(lambda z: 600 / (900 + z ** 2) - mp.pi / 6, 15), {'midpoint': 0, 'carried-half': sp.sqrt(7200 / pi - 900), 'time': xs / 20})
ok(abs(600 / 900 - 0.667) < 5e-4 and 600 / 900 > math.pi / 6, 'camera: rate at 0 is 0.667, above the average')

it = L5['p-app-adoption']
Nt = 1000 / (1 + 9 * E ** (-t))
ok(sp.simplify(sp.diff(Nt, t) - Nt * (1000 - Nt) / 1000) == 0 and Nt.subs(t, 0) == 100, 'app: the rate law and the start')
num(it, 1, sp.Rational(200 * 800, 1000), None, {'no-thousand': 160000, 'one-factor': 200})
t200 = sp.solve(sp.Eq(Nt, 200), t)[0]
num(it, 2, sp.Rational(160 * 600, 1000), float(sp.diff(Nt, t, 2).subs(t, t200)), {'no-rate': 0.6, 'one-term': 160 * 800 / 1000, 'substituted-first': 0})
num(it, 3, 500, float(Nt.subs(t, sp.solve(sp.diff(Nt, t, 2), t)[0])), {'cap': 1000, 'start': 100})
ok(abs(float(sp.solve(sp.diff(Nt, t, 2), t)[0]) - math.log(9)) < 1e-12, 'app: inflection at t = ln 9')
num(it, 4, 250, max(float(sp.diff(Nt, t).subs(t, k / 1e5)) for k in range(219000, 220500, 5)), {'users': 500, 'no-thousand': 250000, 'carried-cap': 0})
num(it, 5, sp.Rational(800, 250), None, {'actual': sp.solve(sp.Eq(Nt, 900), t)[0], 'from-zero': sp.Rational(900, 250), 'carried-users': sp.Rational(800, 500)})
ok(abs(float(sp.solve(sp.Eq(Nt, 900), t)[0]) - math.log(81)) < 1e-12, 'app: true time ln 81')

it = L5['p-impact-curve']
p = 2 * sp.atan(q / 500)
dp = sp.simplify(sp.diff(p, q))
expr(it, 1, dp, [q], {'lost-inner': 500000 / (250000 + q ** 2), 'no-two': 500 / (250000 + q ** 2), 'plain-arctan': 2 / (1 + q ** 2)})
num(it, 2, dp.subs(q, 500) * 200, (2 * math.atan((500 + 200e-5) / 500) - 2 * math.atan((500 - 200e-5) / 500)) / 2e-5,
    {'no-rate': dp.subs(q, 500), 'lost-inner': 200, 'no-two': 0.2})
ok(sp.simplify(sp.diff(p, q, 2) + 2000 * q / (250000 + q ** 2) ** 2) == 0, "impact: the stated p''")
ok(abs(float(sp.diff(p, q, 2).subs(q, 500)) + 1e6 / 2.5e11) < 1e-18, "impact: p''(500)")
q1 = 500 * math.tan(0.5)
ok(abs(q1 - 273.15) < 0.005, 'impact: q(1) = 273.15')
num(it, 4, 1 / dp.subs(q, 500 * sp.tan(sp.Rational(1, 2))), (500 * math.tan((1 + 1e-6) / 2) - 500 * math.tan((1 - 1e-6) / 2)) / 2e-6,
    {'at-y': 1 / dp.subs(q, 1), 'at-500': 1 / dp.subs(q, 500), 'not-inverted': dp.subs(q, q1)})
ok(abs((250000 + 273.15 ** 2) / 1000 - 324.61) < 0.005, 'impact: the printed 324.61')

# ============================================================ integrals 4
I4 = load('integrals', 4)
it = I4['p-impact-kernel']
w = lambda z: 1 / (mp.sqrt(z) * (1 + mp.sqrt(z)) * (2 + mp.sqrt(z)))  # noqa: E731
num(it, 1, sp.integrate(1 / (2 * sp.sqrt(t)), (t, 0, 4)), None, {'no-half': 4, 'unit-rule': sp.Rational(1, 2) * 2})
F = 2 * ln(1 + u) - 2 * ln(2 + u)
ok(sp.simplify(sp.diff(F, u) - 2 / ((1 + u) * (2 + u))) == 0, 'kernel: antiderivative differentiates back')
expr(it, 2, F, [u], {'sign': -F, 'no-two': F / 2, 'plus': 2 * ln(1 + u) + 2 * ln(2 + u)}, up_to_const=True)
num(it, 3, 2 * ln(sp.Rational(3, 2)), quad(w, 0, 1e-6, 1e-3, 1, 4), {'t-limits': F.subs(u, 4) - F.subs(u, 0), 'sign': -2 * ln(sp.Rational(3, 2)), 'no-two': ln(sp.Rational(3, 2))})
num(it, 4, 2 * ln(2), quad(lambda z: 2 / ((1 + z) * (2 + z)), 0, mp.inf), {'no-two': ln(2), 'sign': -2 * ln(2), 'top-only': 0})
num(it, 5, ln(sp.Rational(3, 2)) / ln(2), None, {'inverse': ln(2) / ln(sp.Rational(3, 2)), 't-limits': ln(sp.Rational(5, 3)) / ln(2)})
ok(abs(0.811 / 1.386 - float(ln(sp.Rational(3, 2)) / ln(2))) < 0.0005, 'kernel: the rounded inputs the part restates stay in the band')
ok(all(w(z) < 1 / (2 * mp.sqrt(z)) for z in [1e-6, 0.01, 1, 4, 100]), 'kernel: the bound')
ok(abs(w(1e8) * 1e12 - 1) < 0.001, 'kernel: w falls like t^{-3/2}')

it = I4['p-flared-mouth']
num(it, 1, pi * sp.integrate((1 - x) ** sp.Rational(-1, 2), (x, 0, 1)), None, {'no-pi': 2, 'p-plus': pi / (1 + sp.Rational(1, 2))})
num(it, 2, pi * sp.asin(sp.Rational(1, 2)), quad(lambda z: mp.pi / mp.sqrt(1 - z * z), 0, 0.5), {'x-limits': pi / 2, 'no-pi': pi / 6, 'tan-form': pi * sp.atan(sp.Rational(1, 2))})
num(it, 3, pi * sp.asin(1), quad(lambda z: mp.pi / mp.sqrt(1 - z * z), 0, 0.9, 0.999, 1), {'no-pi': pi / 2, 'tan-form': pi * sp.atan(1), 'x-limits': pi * 1})
num(it, 4, sp.sin(pi / 4), mp.findroot(lambda b: mp.pi * mp.asin(b) - mp.pi ** 2 / 4, 0.7), {'half-x': 0.5, 'no-sine': pi / 4})
ok(all(1 / math.sqrt(1 - z * z) <= 1 / math.sqrt(1 - z) for z in [0, .3, .9, .999]), 'mouth: the bound')

it = I4['p-dish-and-spindle']
f = x / ((x + 1) * (x + 2))
ok(sp.simplify(f - (-1 / (x + 1) + 2 / (x + 2))) == 0, 'dish: the split')
num(it, 1, 2, None, {'sign': -2, 'top-one': sp.Rational(1, -2 + 1)})
Vy = 2 * pi * sp.integrate(x * f, (x, 0, 2))
Vx = pi * sp.integrate(f ** 2, (x, 0, 2))
ok(sp.simplify(x * f - (1 + 1 / (x + 1) - 4 / (x + 2))) == 0, 'dish: the division')
num(it, 2, Vy, quad(lambda z: 2 * mp.pi * z * z / ((z + 1) * (z + 2)), 0, 2), {'no-divide': 2 * pi * (ln(3) - 4 * ln(2)), 'no-2pi': Vy / (2 * pi), 'disc': Vx})
ok(abs(float(Vy - 2 * pi * (2 + ln(3) - 4 * ln(2)))) < 1e-12 and abs(float(Vx - pi * (sp.Rational(5, 3) + 4 * ln(sp.Rational(2, 3))))) < 1e-12, 'dish: the exact forms')
If = sp.integrate(f, (x, 0, 2))
num(it, 3, Vx, quad(lambda z: mp.pi * (z / ((z + 1) * (z + 2))) ** 2, 0, 2), {'square-integral': pi * If ** 2, 'no-square': pi * If, 'cross-term': pi * sp.Rational(5, 3)})
num(it, 4, Vy / Vx, None, {'inverse': Vx / Vy, 'square-integral': Vy / (pi * If ** 2)})
ok(round(2.0485 / 0.1408) == 15 and round(2.048 / 0.141) == 15, 'dish: restated and 3 dp inputs both round to 15')
ok(abs(float(f.subs(x, sp.sqrt(2))) - 0.17) < 0.005 and sp.solve(sp.diff(f, x), x)[-1] == sp.sqrt(2), 'dish: highest point f(sqrt 2) = 0.17')

it = I4['p-rubber-seal']
th_ = sp.symbols('theta', real=True)
shell = quad(lambda z: 2 * mp.pi * z * 2 * mp.sqrt(1 - (z - 3) ** 2), 2, 4)
ok(abs(float(shell) - 6 * math.pi ** 2) < 1e-8, 'seal: the shell integral is 6 pi^2')
c2 = sp.integrate(sp.cos(th_) ** 2, (th_, -pi / 2, pi / 2))
G2 = th_ / 2 + sp.sin(2 * th_) / 4
num(it, 1, c2, quad(lambda z: mp.cos(z) ** 2, -mp.pi / 2, mp.pi / 2), {'x-limits': G2.subs(th_, 4) - G2.subs(th_, 2), 'no-half': 2 * c2, 'quarter': c2 / 2})
G3 = -sp.cos(th_) ** 3 / 3
num(it, 2, sp.integrate(sp.sin(th_) * sp.cos(th_) ** 2, (th_, -pi / 2, pi / 2)), None, {'half-range': sp.Rational(1, 3), 'x-limits': G3.subs(th_, 4) - G3.subs(th_, 2)})
num(it, 3, 4 * pi * 3 * c2, shell, {'no-half': 4 * pi * 3 * pi, 'no-radius': 2 * pi * pi, 'quarter': 4 * pi * 3 * pi / 4})
num(it, 5, 100 / (2 * pi ** 2), None, {'no-half': 100 / (4 * pi ** 2), 'area-times-R': 100 / pi})
ok(abs(100 / (6 * math.pi ** 2) - 1.69) < 0.005 and abs(3 * 100 / (6 * math.pi ** 2) - 5.066) < 0.001, 'seal: scaling by 1.69')

# ============================================================ multivar 4
M4 = load('multivar', 4)
y, rr, a = sp.symbols('y r a', positive=True)
xp = sp.symbols('x', positive=True)
it = M4['p-weighted-rectangle']
w1 = it['parts'][0]['widget']
ok(sp.simplify(keyfn(w1['answer'], [y]) - sp.integrate(xp * y ** 2, (xp, 0, 1))) == 0, 'rectangle 1: key')
ok(sp.simplify(keyfn(w1['wrong'][0]['tex'], [xp, y]) - sp.integrate(xp * y ** 2, y)) == 0, 'rectangle 1: wrong-var is the y antiderivative')
tot = sp.integrate(xp * y ** 2, (xp, 0, 1), (y, 0, 2))
num(it, 2, 1 / tot, 1 / float(mp.quad(lambda X, Y: X * Y * Y, [0, 1], [0, 2])), {'not-inverted': tot, 'no-third': 1 / (8 * sp.Rational(1, 2)), 'carried': 1 / sp.integrate(y ** 2, (y, 0, 2))})
c = sp.Rational(3, 4)
expr(it, 3, sp.integrate(c * xp * y ** 2, (y, 0, 2 * xp)), [xp], {'rect-limits': sp.integrate(c * xp * y ** 2, (y, 0, 2)), 'cube-two': c * xp * 2 * xp ** 3 / 3,
                                                                'carried': sp.integrate(sp.Rational(4, 3) * xp * y ** 2, (y, 0, 2 * xp))})
P = sp.integrate(c * xp * y ** 2, (y, 0, 2 * xp), (xp, 0, 1))
num(it, 4, P, mp.quad(lambda X: mp.quad(lambda Y: 0.75 * X * Y * Y, [0, 2 * X]), [0, 1]),
    {'rect-limits': sp.integrate(2 * xp, (xp, 0, 1)), 'cube-two': sp.integrate(xp ** 4 / 2, (xp, 0, 1)), 'complement': 1 - P, 'carried': sp.integrate(32 * xp ** 4 / 9, (xp, 0, 1))})

it = M4['p-corner-sprinkler']
expr(it, 1, sp.sqrt(9 - xp ** 2), [xp], {'straight': 3 - xp, 'no-root': 9 - xp ** 2})
expr(it, 2, (9 - rr ** 2) * rr, [rr], {'no-r': 9 - rr ** 2, 'r-not-squared': 9 * rr - rr ** 2})
inner = sp.integrate(9 * rr - rr ** 3, (rr, 0, 3))
num(it, 3, inner, None, {'no-r': sp.integrate(9 - rr ** 2, (rr, 0, 3)), 'r-not-squared': sp.integrate(9 * rr - rr ** 2, (rr, 0, 3))})
cart = mp.quad(lambda X: mp.quad(lambda Y: 9 - X * X - Y * Y, [0, mp.sqrt(9 - X * X)]), [0, 3])
num(it, 4, inner * pi / 2, cart, {'full-turn': inner * 2 * pi, 'no-theta': inner, 'carried': 18 * pi / 2})
asol = sp.sqrt(9 - 9 / sp.sqrt(2))
ok(abs(float(sp.integrate(9 * rr - rr ** 3, (rr, 0, asol)) - inner / 2)) < 1e-12, 'sprinkler: a holds half')
num(it, 5, asol, mp.findroot(lambda z: 4.5 * z * z - z ** 4 / 4 - 10.125, 1.5), {'half-radius': 1.5, 'no-root': asol ** 2, 'half-area': 3 / sp.sqrt(2)})

it = M4['p-drone-landing']
num(it, 1, sp.sqrt(8 * pi), quad(lambda z: mp.e ** (-z * z / 8), -mp.inf, mp.inf), {'no-scale': sp.sqrt(pi), 'inverted': sp.sqrt(pi) / (2 * sp.sqrt(2)), 'sigma-root8': sp.sqrt(8) * sp.sqrt(2 * pi)})
expr(it, 2, 8 * pi, [], {'not-squared': sp.sqrt(8 * pi), 'doubled': 2 * sp.sqrt(8 * pi), 'carried': pi})
expr(it, 3, 1 / (8 * pi), [], {'not-inverted': 8 * pi, 'from-root': 1 / sp.sqrt(8 * pi), 'carried': 1 / pi})
Pin = lambda A: 1 - sp.exp(-sp.Rational(A * A, 8))  # noqa: E731
num(it, 4, Pin(2), quad(lambda z: mp.e ** (-z * z / 8) * z / 4, 0, 2), {'r-not-squared': 1 - sp.exp(-sp.Rational(2, 8)), 'no-2pi': Pin(2) / (2 * pi), 'outside': 1 - Pin(2)})
num(it, 5, sp.sqrt(8 * ln(10)), mp.findroot(lambda z: 1 - mp.e ** (-z * z / 8) - 0.9, 4), {'no-root': 8 * ln(10), 'tail-swap': sp.sqrt(-8 * ln(sp.Rational(9, 10))), 'log10': sp.sqrt(8)})
ok(2 < float(sp.sqrt(8 * ln(10))) / 2 < 2.2, 'drone: radius a little more than doubles')

# ============================================================ multivar 5
M5 = load('multivar', 5)
X, Y, Z, lam, mu = sp.symbols('x y z lambda mu', real=True)
it = M5['p-three-strategies']
Gf = 3 * X + 2 * Y + Z - (X ** 2 + Y ** 2 + Z ** 2)
sol = sp.solve([sp.diff(Gf, X) - lam, sp.diff(Gf, Y) - lam, sp.diff(Gf, Z) - lam, X + Y + Z - 1], [X, Y, Z, lam], dict=True)[0]
num(it, 1, sol[lam], None, {'no-two': sp.solve((3 - lam) + (2 - lam) + (1 - lam) - 1, lam)[0], 'no-budget': sp.solve(6 - 3 * lam, lam)[0]})
num(it, 2, sol[Z], None, {'sign': -sol[Z], 'carried': 1 - sp.Rational(5, 3), 'carried-budget': (1 - 2) / sp.Integer(2)})
ok(sol[X] == sp.Rational(5, 6) and sol[Y] == sp.Rational(1, 3), 'strategies: Lagrange point')
e = sp.solve([sp.diff(Gf, X) - lam, sp.diff(Gf, Y) - lam, sp.diff(Gf, Z) - lam - mu, X + Y + Z - 1, Z], [X, Y, Z, lam, mu], dict=True)[0]
num(it, 4, e[X], None, {'clipped': sp.Rational(5, 6), 'rescaled': sp.Rational(5, 6) / sp.Rational(7, 6), 'equal': sp.Rational(1, 2)})
ok(e[lam] == sp.Rational(3, 2) and e[Y] == sp.Rational(1, 4), 'strategies: edge z = 0')
best = max((float(Gf.subs({X: i / 200, Y: j / 200, Z: 1 - i / 200 - j / 200})), i, j) for i in range(201) for j in range(201 - i))
num(it, 5, Gf.subs({X: e[X], Y: e[Y], Z: 0}), best[0], {'infeasible': Gf.subs(sol), 'clipped': Gf.subs({X: sp.Rational(5, 6), Y: sp.Rational(1, 3), Z: 0}), 'corner': Gf.subs({X: 1, Y: 0, Z: 0})})
ok(abs(max(float(Gf.subs({X: 0, Y: k / 1000, Z: 1 - k / 1000})) for k in range(1001)) - 1.125) < 1e-9, 'strategies: edge x = 0 gives 1.125')
ok(abs(max(float(Gf.subs({X: k / 1000, Y: 0, Z: 1 - k / 1000})) for k in range(1001)) - 2) < 1e-9, 'strategies: edge y = 0 gives 2 at the corner')
ok(Gf.subs({X: 0, Y: 1, Z: 0}) == 1 and Gf.subs({X: 0, Y: 0, Z: 1}) == 0, 'strategies: other corners 1 and 0')

it = M5['p-dome-tent']
U, Vv = sp.symbols('u v', real=True)
num(it, 1, 2, None, {'inverse': sp.Rational(1, 2), 'sum': 3})
h = 2 - ((2 * U) ** 2 + 4 * Vv ** 2) / 2
expr(it, 2, sp.expand(h), [U, Vv], {'no-square': 2 - (2 * U ** 2 + 4 * Vv ** 2) / 2, 'inverse-map': 2 - ((U / 2) ** 2 + 4 * Vv ** 2) / 2})
vol = 2 * pi * sp.integrate((2 - 2 * rr ** 2) * 2 * rr, (rr, 0, 1))
volc = mp.quad(lambda xx: mp.quad(lambda yy: 2 - (xx * xx + 4 * yy * yy) / 2, [-mp.sqrt(1 - xx * xx / 4), mp.sqrt(1 - xx * xx / 4)]), [-2, 2])
ok(abs(float(volc) - 2 * math.pi) < 1e-6, 'tent: volume in x, y agrees')
expr(it, 3, vol, [], {'no-jacobian': vol / 2, 'no-r': 2 * pi * sp.integrate((2 - 2 * rr ** 2) * 2, (rr, 0, 1)), 'carried': vol / 4})
zm = 2 * pi * sp.integrate((2 - 2 * rr ** 2) ** 2 / 2 * 2 * rr, (rr, 0, 1))
zmc = mp.quad(lambda xx: mp.quad(lambda yy: (2 - (xx * xx + 4 * yy * yy) / 2) ** 2 / 2, [-mp.sqrt(1 - xx * xx / 4), mp.sqrt(1 - xx * xx / 4)]), [-2, 2])
ok(abs(float(zmc) - 4 * math.pi / 3) < 1e-6, 'tent: z moment in x, y agrees')
expr(it, 4, zm, [], {'no-half': 2 * zm, 'no-jacobian': zm / 2})
num(it, 5, zm / vol, None, {'roof': vol / (2 * pi), 'no-half': 2 * zm / vol, 'flipped': vol / zm})

it = M5['p-triangle-field']
num(it, 1, 8, None, {'inverse': sp.Rational(1, 8), 'sum': 6})
tot = sp.integrate(4 * U * (2 * Vv) ** 2 * 8, (Vv, 0, 1 - U), (U, 0, 1))
direct = sp.integrate(X * Y ** 2, (Y, 0, 2 - X / 2), (X, 0, 4))
ok(tot == direct == sp.Rational(32, 15), 'field: the total both ways')
num(it, 2, tot, None, {'no-jacobian': tot / 8, 'square-two': tot / 2, 'inverse': tot / 64})
num(it, 3, tot / 4, None, {'uv-area': tot / sp.Rational(1, 2), 'carried': tot / 8 / 4})
grid = max(i / 400 * (j / 400) ** 2 for i in range(1601) for j in range(801) if i / 400 + 2 * j / 400 <= 4 + 1e-12)
num(it, 4, sp.Rational(64, 27), None, {'corner': 0, 'mid-edge': 2})
ok(abs(grid - 64 / 27) < 1e-3, 'field: grid maximum')
num(it, 5, (tot / 4) / sp.Rational(64, 27), None, {'mid-edge': tot / 4 / 2, 'inverted': sp.Rational(64, 27) / (tot / 4), 'total': tot / sp.Rational(64, 27)})

print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
