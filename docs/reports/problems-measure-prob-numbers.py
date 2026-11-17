"""Recompute every number in app/content/courses/measure-prob/problems-<n>.json twice.

Method 1 is exact (fractions, closed forms, sympy). Method 2 is independent: enumeration of the finite
spaces (balls, digit strings, coin paths, card orders), numerical integration or a long partial sum,
or a seeded simulation where a closed form is the first method. Each numeric part's key must equal
both values at the asked rounding and lie inside its own band; every `wrong` value is rebuilt from its
named slip, lies outside the key's band, does not reach it, does not overlap another slip and has a
byKey line. Expression keys, accept forms and slips are compared with sympy at sample points. Choice
parts check the keyed option id. The structural pass also asks every numeric part to name its form.
Run: <scratchpad>/venv/bin/python docs/reports/problems-measure-prob-numbers.py   (exit 0 when all pass)
"""
import json, os, re, sys, math, itertools, random
from fractions import Fraction as F
import sympy as sp
import numpy as np
from scipy import integrate
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob')
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('FAIL', msg)


def close(a, b, eps=1e-9):
    return abs(float(a) - float(b)) <= eps * max(1, abs(float(b)))


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    return {it['id']: it for it in json.load(open(p))['items']} if os.path.exists(p) else None


FORM = re.compile(r'decimal|place|fraction|whole number|nearest|exact', re.I)


def structural(items, n):
    for iid, it in items.items():
        ok(3 <= len(it['parts']) <= 5, f'{iid}: 3 to 5 parts')
        for k, p in enumerate(it['parts']):
            w, fb = p['widget'], p['feedback']
            tag = f'L{n} {iid} part {k + 1}'
            if w['kind'] == 'numeric':
                key, tol = w['answer'], w['tol']['abs']
                ok(FORM.search(p['question']) is not None, f'{tag}: names its form')
                seen = []
                for wr in w.get('wrong', []):
                    v, t = wr['value'], wr['tol']['abs']
                    ok(abs(v - key) > tol + t, f'{tag}: wrong {wr["id"]} clear of the key band')
                    ok(wr['id'] in fb.get('byKey', {}), f'{tag}: wrong {wr["id"]} has a byKey line')
                    for (v2, t2, i2) in seen:
                        ok(abs(v - v2) > t + t2, f'{tag}: wrong {wr["id"]} and {i2} do not overlap')
                    seen.append((v, t, wr['id']))
            elif w['kind'] == 'expression':
                for wr in w.get('wrong', []):
                    ok(wr['id'] in fb.get('byKey', {}), f'{tag}: wrong {wr["id"]} has a byKey line')
            elif w['kind'] == 'choice':
                ok(sum(1 for o in w['options'] if o.get('correct')) == 1, f'{tag}: one correct option')
                ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{tag}: every distractor has a why')


def key(items, iid, k):
    return items[iid]['parts'][k - 1]['widget']


def num_part(items, iid, k, v1, v2, places=None, eps=1e-9):
    """Both methods agree, the key is in its band, and the value at the asked rounding is taken."""
    w = key(items, iid, k)
    tag = f'{iid} part {k}'
    ok(abs(v1 - v2) <= eps * max(1, abs(v1)), f'{tag}: methods agree ({v1} vs {v2})')
    ok(abs(w['answer'] - v1) <= w['tol']['abs'] + 1e-12, f'{tag}: key {w["answer"]} within band of {v1}')
    if places is not None:
        r = round(v1, places)
        ok(abs(r - w['answer']) <= w['tol']['abs'] + 1e-12, f'{tag}: rounded {r} accepted')


def wrong_is(items, iid, k, wid, value, places=None):
    w = key(items, iid, k)
    e = [x for x in w['wrong'] if x['id'] == wid]
    ok(len(e) == 1, f'{iid} part {k}: wrong {wid} exists')
    if e:
        v = round(value, places) if places is not None else value
        ok(abs(e[0]['value'] - v) <= e[0]['tol']['abs'] + 1e-12, f'{iid} part {k}: wrong {wid} = {e[0]["value"]} is slip value {value}')


def choice_key(items, iid, k, oid):
    w = key(items, iid, k)
    ok([o['id'] for o in w['options'] if o.get('correct')] == [oid], f'{iid} part {k}: keyed option is {oid}')


SYM = {s: sp.Symbol(s) for s in ('n', 'h', 's', 'm', 'k')}


def tex(s):
    s = s.replace('\\left', '').replace('\\right', '').replace(' ', '').replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
    while '\\frac' in s:
        i = s.index('\\frac')

        def grab(j):
            depth, kk = 0, j
            while True:
                if s[kk] == '{':
                    depth += 1
                elif s[kk] == '}':
                    depth -= 1
                    if depth == 0:
                        return s[j + 1:kk], kk + 1
                kk += 1
        a, j = grab(i + 5)
        b, j = grab(j)
        s = s[:i] + f'(({a})/({b}))' + s[j:]
    s = s.replace('\\cdot', '*').replace('\\times', '*').replace('{', '(').replace('}', ')').replace('^', '**').replace('e**', 'E**')
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    return parse_expr(s, local_dict=dict(SYM, E=sp.E), transformations=standard_transformations + (implicit_multiplication_application,))


def same(e1, e2, pts=(1, 2, 3, 5, 0.5, 2.5)):
    for v in pts:
        sub = {x: v for x in SYM.values()}
        a, b = complex(e1.subs(sub).evalf()), complex(e2.subs(sub).evalf())
        if abs(a - b) > 1e-9 * max(1, abs(b)):
            return False
    return True


def expr_part(items, iid, k, truth):
    w = key(items, iid, k)
    ok(same(tex(w['answer']), truth), f'{iid} part {k}: answer equals the truth')
    for a in w.get('accept', []):
        ok(same(tex(a), truth), f'{iid} part {k}: accept {a} equals the truth')
    for wr in w.get('wrong', []):
        ok(not same(tex(wr['tex']), truth), f'{iid} part {k}: wrong {wr["id"]} differs')


# ---------------------------------------------------------------- level 1
def level1():
    it = load(1)
    if it is None:
        return
    structural(it, 1)
    # p-fat-cantor
    stage3 = F(2 ** 2, 4 ** 3)
    # method 2: build the intervals explicitly with fractions
    ivs = [(F(0), F(1))]
    removed = []
    for n in range(1, 8):
        g, new, rem = F(1, 4 ** n), [], F(0)
        for a, b in ivs:
            m = (a + b) / 2
            new += [(a, m - g / 2), (m + g / 2, b)]
            rem += g
        ivs, removed = new, removed + [rem]
    ok(removed[2] == stage3, 'fat: stage 3 removes 1/16 by construction')
    num_part(it, 'p-fat-cantor', 1, float(stage3), float(removed[2]), 4)
    wrong_is(it, 'p-fat-cantor', 1, 'one-gap', 1 / 64)
    wrong_is(it, 'p-fat-cantor', 1, 'eight-gaps', 8 / 64)
    # length of C_n from the construction against the formula
    ivs2 = [(F(0), F(1))]
    for n in range(1, 7):
        g = F(1, 4 ** n)
        ivs2 = [x for a, b in ivs2 for x in ((a, (a + b) / 2 - g / 2), ((a + b) / 2 + g / 2, b))]
        ok(sum(b - a for a, b in ivs2) == F(1, 2) + F(1, 2 ** (n + 1)), f'fat: length C_{n} matches 1/2 + 2^-(n+1)')
    expr_part(it, 'p-fat-cantor', 2, sp.Rational(1, 2) + 2 ** (-(SYM['n'] + 1)))
    num_part(it, 'p-fat-cantor', 3, 0.5, float(F(1, 2) + F(1, 2 ** 60)), 3, eps=1e-15)
    wrong_is(it, 'p-fat-cantor', 3, 'stage-three', float(F(1, 2) + F(1, 16)))
    choice_key(it, 'p-fat-cantor', 4, 'fin')

    # p-ball-machine
    P = {w: F(w, 78) for w in range(1, 13)}
    ok(sum(P.values()) == 1, 'balls: chances add to 1')
    atomsX = {}
    for w in P:
        atomsX.setdefault(w % 4, []).append(w)
    ok(len(atomsX) == 4, 'balls: 4 atoms of X')
    # method 2: count events by brute force closure on 12 points (sets as bitmasks)
    def gen_count(parts):
        fam = {0}
        for A in parts:
            fam |= {x | A for x in fam}
        return len(fam)
    mask = lambda ws: sum(1 << (w - 1) for w in ws)
    num_part(it, 'p-ball-machine', 1, 2 ** 4, gen_count([mask(v) for v in atomsX.values()]))
    wrong_is(it, 'p-ball-machine', 1, 'atoms', 4)
    wrong_is(it, 'p-ball-machine', 1, 'all', 2 ** 12)
    atomsXY = {}
    for w in P:
        atomsXY.setdefault((w % 4, w >= 10), []).append(w)
    # brute: sigma-algebra generated by the indicator sets {X=k} and {Y=1}: close under complement and union
    gens = [mask(v) for v in atomsX.values()] + [mask([w for w in P if w >= 10])]
    full = (1 << 12) - 1
    fam = {0, full}
    changed = True
    while changed:
        changed = False
        cur = list(fam | set(gens))
        for a in cur:
            for b in cur:
                for c in (a | b, full ^ a):
                    if c not in fam:
                        fam.add(c)
                        changed = True
    num_part(it, 'p-ball-machine', 2, 2 ** len(atomsXY), len(fam))
    wrong_is(it, 'p-ball-machine', 2, 'product', 2 ** 8)
    wrong_is(it, 'p-ball-machine', 2, 'side-by-side', 2 ** 6)
    F25 = sum(P[w] for w in P if w % 4 <= 2)
    ok(F25 == F(57, 78), 'balls: F_X(2.5) = 57/78')
    F25b = sum(F(w, 78) for w in range(1, 13) if w % 4 in (0, 1, 2))
    num_part(it, 'p-ball-machine', 3, float(F25), float(F25b), 4)
    ok(abs(round(float(F25), 4) - 0.7308) < 1e-12, 'balls: 57/78 rounds to 0.7308')
    wrong_is(it, 'p-ball-machine', 3, 'uniform', 9 / 12)
    wrong_is(it, 'p-ball-machine', 3, 'strict', float(sum(P[w] for w in P if w % 4 <= 1)))
    wrong_is(it, 'p-ball-machine', 3, 'complement', float(1 - F25), 4)
    for k, v in ((0, 24), (1, 15), (2, 18)):
        ok(sum(w for w in P if w % 4 == k) == v, f'balls: weight of remainder {k} is {v}/78')
    Fx = lambda x: sum(P[w] for w in P if w % 4 <= x)
    q = min(x for x in range(4) if Fx(x) >= F(3, 4))
    num_part(it, 'p-ball-machine', 4, q, next(x for x in (0, 1, 2, 3) if float(Fx(x)) >= 0.75))
    qu = min(x for x in range(4) if F(sum(1 for w in P if w % 4 <= x), 12) >= F(3, 4))
    wrong_is(it, 'p-ball-machine', 4, 'equal-chances', qu)
    choice_key(it, 'p-ball-machine', 5, 'parity')
    const_on_atoms = lambda f: all(len({f(w) for w in A}) == 1 for A in atomsX.values())
    ok(const_on_atoms(lambda w: w % 2) and not const_on_atoms(lambda w: w >= 10)
       and not const_on_atoms(lambda w: -(-w // 4)) and not const_on_atoms(lambda w: w % 3), 'balls: only parity is sigma(X)-measurable')

    # p-reciprocal-grid
    rng = random.Random(11)
    us = [1 - rng.random() for _ in range(400000)]
    Ns = [math.floor(1 / u) for u in us]
    p3 = F(1, 3) - F(1, 4)
    sim = sum(1 for x in Ns if x == 3) / len(Ns)
    ok(abs(sim - float(p3)) < 0.002, f'grid: simulated P(N=3) {sim:.4f} near 1/12')
    num_part(it, 'p-reciprocal-grid', 1, float(p3), 1 / 12, 4)
    wrong_is(it, 'p-reciprocal-grid', 1, 'third', 1 / 3, 4)
    wrong_is(it, 'p-reciprocal-grid', 1, 'two', 1 / 2 - 1 / 3, 4)
    expr_part(it, 'p-reciprocal-grid', 2, 1 / SYM['n'])
    for n in (2, 5, 9):
        ok(abs(sum(1 for x in Ns if x >= n) / len(Ns) - 1 / n) < 0.003, f'grid: simulated P(N>={n}) near 1/{n}')
    F03 = F(1, min(n for n in range(1, 100) if F(1, n) <= F(3, 10)))
    num_part(it, 'p-reciprocal-grid', 3, float(F03), sum(1 for x in Ns if 1 / x <= 0.3) / len(Ns), 2, eps=0.02)
    wrong_is(it, 'p-reciprocal-grid', 3, 'as-u', 0.3)
    wrong_is(it, 'p-reciprocal-grid', 3, 'three', 1 / 3, 4)
    left = F(1, min(n for n in range(1, 100) if F(1, n) < F(1, 5)))
    num_part(it, 'p-reciprocal-grid', 4, float(left), 1 / 6, 4)
    ok(abs(sum(1 for x in Ns if 1 / x < 0.2) / len(Ns) - 1 / 6) < 0.003, 'grid: simulated P(X<0.2) near 1/6')
    wrong_is(it, 'p-reciprocal-grid', 4, 'at-point', 0.2)
    wrong_is(it, 'p-reciprocal-grid', 4, 'jump', float(F(1, 5) - F(1, 6)), 4)
    choice_key(it, 'p-reciprocal-grid', 5, 'cont')
    ok(sum(F(1, k) - F(1, k + 1) for k in range(1, 2000)) == 1 - F(1, 2000), 'grid: jumps add to 1 - 1/K below 1')

    # p-no-double-seven
    a = [1, 10]
    for n in range(2, 6):
        a.append(9 * a[-1] + 9 * a[-2])
    brute = {n: sum(1 for t in itertools.product('0123456789', repeat=n) if '77' not in ''.join(t)) for n in (2, 3, 4)}
    ok(a[2] == brute[2] == 99 and a[3] == brute[3] == 981 and a[4] == brute[4] == 9720, 'digits: recursion matches brute force')
    num_part(it, 'p-no-double-seven', 1, a[3] / 1000, brute[3] / 1000, 3)
    ok(1000 - (10 + 10 - 1) == 981, 'digits: inclusion-exclusion 19 strings hold 77')
    wrong_is(it, 'p-no-double-seven', 1, 'overlap', 1 - 0.02)
    ok(abs(0.99 ** 2 - 0.98) <= 0.0002, 'digits: the 0.99^2 slip falls in the overlap band')
    wrong_is(it, 'p-no-double-seven', 1, 'first-pair', 0.99)
    num_part(it, 'p-no-double-seven', 2, a[4] / 10 ** 4, brute[4] / 10 ** 4, 3)
    ok(9 * 981 == 8829 and 9 * 99 == 891, 'digits: printed products')
    wrong_is(it, 'p-no-double-seven', 2, 'one-term', 9 * 981 / 10 ** 4)
    wrong_is(it, 'p-no-double-seven', 2, 'square', 0.981 ** 2, 4)
    b1 = 0.99 ** 100
    b2 = math.exp(100 * math.log1p(-0.01))
    num_part(it, 'p-no-double-seven', 3, b1, b2, 3)
    wrong_is(it, 'p-no-double-seven', 3, 'all-places', 0.99 ** 199, 4)
    wrong_is(it, 'p-no-double-seven', 3, 'all-digits', 0.99 ** 200, 3)
    # the bound holds: exact P(D_200) from the recursion is below it
    aa = [F(1), F(1)]
    for n in range(2, 201):
        aa.append(F(9, 10) * aa[-1] + F(9, 100) * aa[-2])
    ok(float(aa[200]) <= b1, f'digits: exact P(D_200) {float(aa[200]):.4f} below the bound')
    ok(aa[3] == F(981, 1000) and aa[4] == F(9720, 10 ** 4), 'digits: chance recursion matches')
    for n in range(201, 3001):
        aa.append(F(9, 10) * aa[-1] + F(9, 100) * aa[-2])
    ok(float(aa[3000]) < 1e-11 and 0.99 ** 1500 < 1e-6, 'digits: P(D_n) and the bound fall to 0')
    num_part(it, 'p-no-double-seven', 4, 0, round(float(aa[3000]), 9))
    wrong_is(it, 'p-no-double-seven', 4, 'complement', 1)
    choice_key(it, 'p-no-double-seven', 5, 'sub')

    lv = Level('measure-prob', 1)
    hand = lv.check_wrongs('problems')
    ok(all(r[0] for r in lv.results), 'level 1: numbers_lib check_wrongs')


# ---------------------------------------------------------------- level 2
def level2():
    it = load(2)
    if it is None:
        return
    structural(it, 2)
    e = math.e
    # p-billed-hours
    v1 = math.exp(-2) - math.exp(-3)
    v2 = integrate.quad(lambda t: math.exp(-t), 2, 3)[0]
    num_part(it, 'p-billed-hours', 1, v1, v2, 4)
    wrong_is(it, 'p-billed-hours', 1, 'tail', math.exp(-2), 4)
    wrong_is(it, 'p-billed-hours', 1, 'cdf', 1 - math.exp(-2), 4)
    ok(round(math.exp(-2), 4) == 0.1353 and round(math.exp(-3), 4) == 0.0498, 'hours: printed tails')
    f1 = 1 / (e - 1)
    f2 = sum(k * (math.exp(-k) - math.exp(-k - 1)) for k in range(0, 200))
    num_part(it, 'p-billed-hours', 2, f1, f2, 4)
    wrong_is(it, 'p-billed-hours', 2, 'from-zero', e / (e - 1), 4)
    wrong_is(it, 'p-billed-hours', 2, 'mean', 1)
    wrong_is(it, 'p-billed-hours', 2, 'half-lost', 0.5)
    h1 = 0.5 / (math.exp(0.5) - 1)
    h2 = sum(0.5 * k * (math.exp(-k / 2) - math.exp(-(k + 1) / 2)) for k in range(0, 400))
    num_part(it, 'p-billed-hours', 3, h1, h2, 4)
    wrong_is(it, 'p-billed-hours', 3, 'no-half', 1 / (math.exp(0.5) - 1), 4)
    wrong_is(it, 'p-billed-hours', 3, 'from-zero', 0.5 * math.exp(0.5) / (math.exp(0.5) - 1), 4)
    m = lambda h: h / (math.exp(h) - 1)
    mbrute = lambda h: sum(h * k * (math.exp(-k * h) - math.exp(-(k + 1) * h)) for k in range(0, int(60 / h)))
    nstar = min(n for n in range(1, 30) if m(2 ** -n) > 0.99)
    nstar2 = min(n for n in range(1, 12) if mbrute(2 ** -n) > 0.99)
    num_part(it, 'p-billed-hours', 4, nstar, nstar2)
    ok(round(m(1 / 32), 4) == 0.9845 and round(m(1 / 64), 4) == 0.9922, 'hours: printed means at h = 1/32, 1/64')
    wrong_is(it, 'p-billed-hours', 4, 'one-minus-h', min(n for n in range(1, 30) if 1 - 2 ** -n > 0.99))
    ok(all(m(2 ** -(n + 1)) > m(2 ** -n) for n in range(1, 12)), 'hours: the means rise with n')

    # p-compounding
    R = sp.Symbol('R')
    mom = {0: 1, 1: 0, 2: sp.Rational(1, 4), 3: 0, 4: 3 * sp.Rational(1, 16)}
    def Emean(poly):
        P = sp.Poly(sp.expand(poly), R)
        return sum(c * mom[d[0]] for d, c in zip(P.monoms(), P.coeffs()))
    g2, g4 = Emean((1 + R / 2) ** 2), Emean((1 + R / 4) ** 4)
    xs = np.linspace(-12, 12, 240001)
    dens = np.exp(-xs ** 2 / 2) / math.sqrt(2 * math.pi)
    quadE = lambda f: float(np.trapezoid(f(0.5 * xs) * dens, xs))
    num_part(it, 'p-compounding', 1, float(g2), quadE(lambda r: (1 + r / 2) ** 2), 4, eps=1e-8)
    wrong_is(it, 'p-compounding', 1, 'no-square', 1)
    wrong_is(it, 'p-compounding', 1, 'half-square', 1 + 0.25 / 2)
    num_part(it, 'p-compounding', 2, float(g4), quadE(lambda r: (1 + r / 4) ** 4), 4, eps=1e-8)
    wrong_is(it, 'p-compounding', 2, 'no-fourth', 1 + 6 * 0.25 / 16)
    wrong_is(it, 'p-compounding', 2, 'fourth-one', 1 + 6 * 0.25 / 16 + 0.0625 / 256)
    ok(abs(float(g4) - 1.094482421875) < 1e-12 and round(3 * 0.0625 / 256, 6) == 0.000732, 'compounding: printed terms')
    d1 = 2 * math.exp(0.125) * 0.6915
    d2 = quadE(lambda r: np.exp(np.abs(r)))
    ok(abs(2 * math.exp(0.125) * norm.cdf(0.5) - d2) < 1e-8, 'compounding: E e^|R| formula matches quadrature')
    num_part(it, 'p-compounding', 3, round(d1, 3), round(d2, 3), 3)
    wrong_is(it, 'p-compounding', 3, 'no-abs', math.exp(0.125), 4)
    wrong_is(it, 'p-compounding', 3, 'no-phi', 2 * math.exp(0.125), 4)
    for n in range(1, 40):
        ok(np.all(np.abs((1 + 0.5 * xs / n) ** n) <= np.exp(np.abs(0.5 * xs)) + 1e-9), f'compounding: |G_{n}| <= e^|R| on the grid') if n in (1, 2, 3, 7, 39) else None
    ok((1 - 3) == -2 and (1 - 1.5) ** 2 == 0.25 and (1 - 1) ** 3 == 0, 'compounding: G_1, G_2, G_3 at R = -3')
    choice_key(it, 'p-compounding', 4, 'dct')
    lim1 = math.exp(0.125)
    num_part(it, 'p-compounding', 5, lim1, quadE(lambda r: np.exp(r)), 4, eps=1e-8)
    ok(all(quadE(lambda r, n=n: (1 + r / n) ** n) < lim1 for n in (1, 2, 4, 8)), 'compounding: the means lie below the limit')
    wrong_is(it, 'p-compounding', 5, 'jensen', 1)
    wrong_is(it, 'p-compounding', 5, 'no-half', math.exp(0.25), 4)
    wrong_is(it, 'p-compounding', 5, 'bound', d2, 3)

    # p-root-of-uniform
    n_ = SYM['n']
    t = sp.Symbol('t')
    E4 = sp.integrate(1 - t ** 4, (t, 0, 1))
    num_part(it, 'p-root-of-uniform', 1, float(E4), integrate.quad(lambda u: u ** 0.25, 0, 1)[0], 3, eps=1e-8)
    wrong_is(it, 'p-root-of-uniform', 1, 'tail-only', 0.2)
    wrong_is(it, 'p-root-of-uniform', 1, 'jensen', 0.5 ** 0.25, 4)
    En = sp.integrate(1 - t ** n_, (t, 0, 1), conds='none')
    E2 = sp.integrate(1 - t ** (n_ / 2), (t, 0, 1), conds='none')   # P(X^2 > t) = P(U > t^(n/2))
    msd = sp.simplify(E2 - 2 * En + 1)
    expr_part(it, 'p-root-of-uniform', 2, msd)
    ok(same(msd, 2 / ((n_ + 1) * (n_ + 2))), 'root: mean-square distance is 2/((n+1)(n+2))')
    for n in (3, 10):
        ok(abs(integrate.quad(lambda u: (u ** (1 / n) - 1) ** 2, 0, 1)[0] - 2 / ((n + 1) * (n + 2))) < 1e-10, f'root: quadrature at n = {n}')
    c1 = 2 / (11 * 12) / 0.01
    c2 = integrate.quad(lambda u: (u ** 0.1 - 1) ** 2, 0, 1)[0] / 0.01
    num_part(it, 'p-root-of-uniform', 3, c1, c2, 4, eps=1e-8)
    wrong_is(it, 'p-root-of-uniform', 3, 'no-eps', 2 / 132, 4)
    wrong_is(it, 'p-root-of-uniform', 3, 'eps', 2 / 132 / 0.1, 4)
    pex = 0.9 ** 10
    us = np.random.default_rng(3).random(1_000_000)
    num_part(it, 'p-root-of-uniform', 4, pex, float(np.mean(np.abs(us ** 0.1 - 1) > 0.1)), 4, eps=0.004)
    wrong_is(it, 'p-root-of-uniform', 4, 'complement', 1 - pex, 4)
    wrong_is(it, 'p-root-of-uniform', 4, 'root', 0.9 ** 0.1, 4)
    choice_key(it, 'p-root-of-uniform', 5, 'all')

    # p-random-maturity
    r = 0.05
    V1 = (1 - math.exp(-4 * r)) / (4 * r)
    V2 = integrate.quad(lambda x: math.exp(-r * x) / 4, 0, 4)[0]
    num_part(it, 'p-random-maturity', 1, V1, V2, 4)
    wrong_is(it, 'p-random-maturity', 1, 'mean-time', math.exp(-0.1), 4)
    wrong_is(it, 'p-random-maturity', 1, 'end', math.exp(-0.2), 4)
    choice_key(it, 'p-random-maturity', 2, 'four')
    D1 = (1 - 1.2 * math.exp(-0.2)) / 0.01
    D2 = integrate.quad(lambda x: x * math.exp(-r * x) / 4, 0, 4)[0]
    rr = sp.Symbol('r', positive=True)
    Vs = (1 - sp.exp(-4 * rr)) / (4 * rr)
    D3 = float(-sp.diff(Vs, rr).subs(rr, sp.Rational(1, 20)))
    num_part(it, 'p-random-maturity', 3, D1, D2, 4)
    ok(abs(D1 - D3) < 1e-10, 'maturity: -V\'(0.05) from differentiating V matches')
    wrong_is(it, 'p-random-maturity', 3, 'jensen', 2 * math.exp(-0.1), 4)
    wrong_is(it, 'p-random-maturity', 3, 'no-discount', 2)
    dur = D1 / V1
    num_part(it, 'p-random-maturity', 4, dur, D3 / V2, 2, eps=1e-9)
    ok(abs(round(1.7523 / 0.9063, 2) - 1.93) < 1e-12 and abs(round(dur, 2) - 1.93) < 1e-12, 'maturity: printed duration 1.93')
    wrong_is(it, 'p-random-maturity', 4, 'mean', 2)
    wrong_is(it, 'p-random-maturity', 4, 'no-divide', D1, 4)
    wrong_is(it, 'p-random-maturity', 4, 'inverse', V1 / D1, 4)

    lv = Level('measure-prob', 2)
    lv.check_wrongs('problems')
    ok(all(r_[0] for r_ in lv.results), 'level 2: numbers_lib check_wrongs')


level1()
level2()
print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
