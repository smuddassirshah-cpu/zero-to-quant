"""Recompute every number in app/content/courses/measure-prob/problems-<n>.json twice.

Method 1 is exact (fractions, closed forms, sympy). Method 2 is independent: enumeration of the finite
spaces (balls, digit strings, coin paths, capital paths, the news tree), numerical integration or a long partial sum,
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
    s = s.replace('\\sqrt', 'sqrt').replace('\\left', '').replace('\\right', '').replace(' ', '').replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac')
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

    # p-quote-ladder (session AF, replaces p-reciprocal-grid)
    r4 = F(2, 5)
    rng = random.Random(11)
    us = [1 - rng.random() for _ in range(400000)]          # uniform on (0, 1]
    def rung(u):
        n = 0
        while not (r4 ** (n + 1) < u <= r4 ** n):
            n += 1
        return n
    Ns = [rung(u) for u in us]
    pN = lambda k: r4 ** k - r4 ** (k + 1)
    num_part(it, 'p-quote-ladder', 1, float(pN(2)), 0.16 - 0.064, 3)
    ok(abs(sum(1 for x in Ns if x == 2) / len(Ns) - 0.096) < 0.002, 'ladder: simulated P(N = 2) near 0.096')
    wrong_is(it, 'p-quote-ladder', 1, 'rung', 0.16)
    wrong_is(it, 'p-quote-ladder', 1, 'next-rung', 0.064)
    wrong_is(it, 'p-quote-ladder', 1, 'swap', 0.4 * 0.6 ** 2)
    expr_part(it, 'p-quote-ladder', 2, sp.Rational(3, 5) * sp.Rational(2, 5) ** SYM['k'])
    ok(all(pN(k) == F(3, 5) * r4 ** k for k in range(12)), 'ladder: band length 0.6 x 0.4^k')
    p3 = F(3, 5) / (1 - r4 ** 3)
    p3b = sum(pN(3 * j) for j in range(60))
    num_part(it, 'p-quote-ladder', 3, float(p3), float(p3b), 4, eps=1e-12)
    ok(p3 == F(25, 39), 'ladder: P(N in 3Z) = 25/39')
    ok(abs(sum(1 for x in Ns if x % 3 == 0) / len(Ns) - float(p3)) < 0.003, 'ladder: simulated P(N in 3Z)')
    wrong_is(it, 'p-quote-ladder', 3, 'no-zero', float(p3 - F(3, 5)), 4)
    wrong_is(it, 'p-quote-ladder', 3, 'third', 1 / 3, 4)
    wrong_is(it, 'p-quote-ladder', 3, 'two-terms', float(pN(0) + pN(3)), 4)
    ok(abs(0.6 / 0.936 - float(p3)) < 1e-12, 'ladder: printed 0.6/0.936')
    choice_key(it, 'p-quote-ladder', 4, 'all-b')
    ok(r4 < F(1, 2) < 1, 'ladder: U <= 0.5 cuts the band (0.4, 1] of N = 0')
    p5 = sum((r4 ** k - r4 ** k / 2) for k in range(200))     # band k keeps [0.5 * 0.4^k, 0.4^k]
    ok(all(r4 ** k / 2 > r4 ** (k + 1) for k in range(50)), 'ladder: cut-off sits above each band floor')
    sim5 = sum(1 for u, x in zip(us, Ns) if r4 ** x <= 2 * u) / len(us)
    num_part(it, 'p-quote-ladder', 5, float(F(5, 6)), float(p5), 4, eps=1e-12)
    ok(abs(sim5 - 5 / 6) < 0.003, f'ladder: simulated P(X <= 2U) {sim5:.4f} near 5/6')
    ok(all(F(1, 2) * r4 ** k / pN(k) == F(5, 6) for k in range(10)), 'ladder: each band keeps 5/6 of its chance')
    wrong_is(it, 'p-quote-ladder', 5, 'half-band', 0.5)
    wrong_is(it, 'p-quote-ladder', 5, 'complement', 1 / 6, 4)

    # p-no-double-four
    a = [1, 10]
    for n in range(2, 6):
        a.append(9 * a[-1] + 9 * a[-2])
    brute = {n: sum(1 for t in itertools.product('0123456789', repeat=n) if '44' not in ''.join(t)) for n in (2, 3, 4)}
    ok(a[2] == brute[2] == 99 and a[3] == brute[3] == 981 and a[4] == brute[4] == 9720, 'digits: recursion matches brute force')
    num_part(it, 'p-no-double-four', 1, a[3] / 1000, brute[3] / 1000, 3)
    ok(1000 - (10 + 10 - 1) == 981, 'digits: inclusion-exclusion 19 strings hold 44')
    wrong_is(it, 'p-no-double-four', 1, 'overlap', 1 - 0.02)
    ok(abs(0.99 ** 2 - 0.98) <= 0.0002, 'digits: the 0.99^2 slip falls in the overlap band')
    wrong_is(it, 'p-no-double-four', 1, 'first-pair', 0.99)
    num_part(it, 'p-no-double-four', 2, a[4] / 10 ** 4, brute[4] / 10 ** 4, 3)
    ok(9 * 981 == 8829 and 9 * 99 == 891, 'digits: printed products')
    wrong_is(it, 'p-no-double-four', 2, 'one-term', 9 * 981 / 10 ** 4)
    wrong_is(it, 'p-no-double-four', 2, 'square', 0.981 ** 2, 4)
    b1 = 0.99 ** 100
    b2 = math.exp(100 * math.log1p(-0.01))
    num_part(it, 'p-no-double-four', 3, b1, b2, 3)
    wrong_is(it, 'p-no-double-four', 3, 'all-places', 0.99 ** 199, 4)
    wrong_is(it, 'p-no-double-four', 3, 'all-digits', 0.99 ** 200, 3)
    # the bound holds: exact P(D_200) from the recursion is below it
    aa = [F(1), F(1)]
    for n in range(2, 201):
        aa.append(F(9, 10) * aa[-1] + F(9, 100) * aa[-2])
    ok(float(aa[200]) <= b1, f'digits: exact P(D_200) {float(aa[200]):.4f} below the bound')
    ok(aa[3] == F(981, 1000) and aa[4] == F(9720, 10 ** 4), 'digits: chance recursion matches')
    for n in range(201, 3001):
        aa.append(F(9, 10) * aa[-1] + F(9, 100) * aa[-2])
    ok(float(aa[3000]) < 1e-11 and 0.99 ** 1500 < 1e-6, 'digits: P(D_n) and the bound fall to 0')
    num_part(it, 'p-no-double-four', 4, 0, round(float(aa[3000]), 9))
    wrong_is(it, 'p-no-double-four', 4, 'complement', 1)
    choice_key(it, 'p-no-double-four', 5, 'sub')
    wrong_is(it, 'p-no-double-four', 2, 'independent', 0.981 * 0.99)
    ok(abs(0.981 * 0.99 - 0.97119) < 1e-12, 'digits: independent slip 0.97119')
    txt = json.dumps(it['p-no-double-four'])
    ok('77' not in txt and '44' in txt and '444' in txt, 'digits: block 44 throughout, no 77 left')

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
    # p-settlement-fails (session AF, replaces p-billed-hours)
    pk = lambda k: F(16, 25) * (k + 1) * F(1, 5) ** k
    ok(sum(pk(k) for k in range(400)) > 1 - F(1, 10 ** 200) and abs(float(sum(pk(k) for k in range(400))) - 1) < 1e-15, 'fails: chances add to 1')
    sS = sp.Symbol('s')
    Gs = 16 / (5 - sS) ** 2
    kk = sp.Symbol('kk', integer=True, nonnegative=True)
    Gser = sp.summation(sp.Rational(16, 25) * (kk + 1) * (sS / 5) ** kk, (kk, 0, sp.oo))
    ok(all(abs(float(Gser.subs(sS, v)) - float(Gs.subs(sS, v))) < 1e-12 for v in (0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 3)), 'fails: G(s) = 16/(5 - s)^2 from the series')
    e1 = float(F(16, 25) / F(3, 4) ** 2)
    e2 = float(sum(pk(k) * F(5, 4) ** k for k in range(300)))
    num_part(it, 'p-settlement-fails', 1, e1, e2, 4, eps=1e-12)
    ok(F(16, 25) / F(9, 16) == F(256, 225) and Gs.subs(sS, sp.Rational(5, 4)) == sp.Rational(256, 225), 'fails: E[1.25^N] = 256/225 = G(1.25)')
    wrong_is(it, 'p-settlement-fails', 1, 'jensen', 1.25 ** 0.5, 4)
    wrong_is(it, 'p-settlement-fails', 1, 'no-k', 0.64 / 0.75, 4)
    choice_key(it, 'p-settlement-fails', 2, 'mct')
    ok(sp.simplify(sp.diff(Gs, sS) - 32 / (5 - sS) ** 3) == 0 and sp.simplify(sp.diff(Gs, sS, 2) - 96 / (5 - sS) ** 4) == 0, 'fails: printed G\' and G\'\'')
    EN = float(sum(k * pk(k) for k in range(400)))
    num_part(it, 'p-settlement-fails', 3, float(sp.diff(Gs, sS).subs(sS, 1)), EN, 3, eps=1e-12)
    ok(abs(EN - 2 * 0.2 / 0.8) < 1e-12, 'fails: E[N] = rq/p for the negative binomial')
    ok(all(float(sp.diff(Gs, sS).subs(sS, v)) < 0.5 for v in (0.9, 0.99, 0.999)), 'fails: G\'(s) rises towards 0.5 from below')
    wrong_is(it, 'p-settlement-fails', 3, 'one', float(Gs.subs(sS, 1)))
    wrong_is(it, 'p-settlement-fails', 3, 'at-zero', float(pk(1)), 3)
    ok(pk(1) == F(32, 125), 'fails: G\'(0) = P(N = 1) = 32/125')
    wrong_is(it, 'p-settlement-fails', 3, 'square', 32 / 16)
    EN2 = float(sum(k * k * pk(k) for k in range(400)))
    fall = float(sp.diff(Gs, sS, 2).subs(sS, 1))
    num_part(it, 'p-settlement-fails', 4, fall + 0.5, EN2, 3, eps=1e-12)
    ok(abs(EN2 - (0.4 / 0.64 + 0.25)) < 1e-12, 'fails: E[N^2] = Var + mean^2 for the negative binomial')
    wrong_is(it, 'p-settlement-fails', 4, 'falling', fall, 3)
    wrong_is(it, 'p-settlement-fails', 4, 'variance', EN2 - EN ** 2, 3)
    wrong_is(it, 'p-settlement-fails', 4, 'mean-sq', EN ** 2, 3)
    choice_key(it, 'p-settlement-fails', 5, 'inf')
    ok(all(pk(k) * 6 ** k == F(16, 25) * (k + 1) * F(6, 5) ** k for k in range(30)) and float(sum(pk(k) * 6 ** k for k in range(300))) > 1e15 and Gs.subs(sS, 6) == 16 and abs(6 ** 0.5 - 2.449) < 1e-3, 'fails: E[6^N] terms are 0.64(k+1)1.2^k, partial sums grow without bound; G(6) = 16 only formally; 6^0.5 = 2.45')

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

    # p-boom-bust (session AF, replaces p-root-of-uniform)
    n_ = SYM['n']
    up, dn = sp.Rational(8, 5), sp.Rational(2, 5)
    e_root = (sp.sqrt(up) + sp.sqrt(dn)) / 2
    ok(sp.simplify(e_root - sp.sqrt(sp.Rational(9, 10))) == 0, 'boom: E[sqrt M_1] = sqrt(0.9)')
    expr_part(it, 'p-boom-bust', 1, sp.Rational(9, 10) ** (n_ / 2))
    pathsE = lambda n, f: sum(math.comb(n, k) * f(1.6 ** k * 0.4 ** (n - k)) for k in range(n + 1)) / 2 ** n
    ok(abs(pathsE(4, math.sqrt) - 0.81) < 1e-12 and abs(pathsE(7, math.sqrt) - 0.9 ** 3.5) < 1e-12, 'boom: E[sqrt M_n] by enumeration')
    ok(abs(pathsE(6, lambda x: x) - 1) < 1e-12, 'boom: E[M_n] = 1')
    b1 = 0.9 ** 2 / math.sqrt(0.5)
    b2 = pathsE(4, math.sqrt) / math.sqrt(0.5)
    num_part(it, 'p-boom-bust', 2, b1, b2, 4)
    ok(b1 > 1, 'boom: the bound is above 1')
    wrong_is(it, 'p-boom-bust', 2, 'no-root', 0.81)
    wrong_is(it, 'p-boom-bust', 2, 'epsilon', 0.81 / 0.5)
    wrong_is(it, 'p-boom-bust', 2, 'markov-m', pathsE(4, lambda x: x) / 0.5)
    ex = sum(math.comb(4, k) for k in range(5) if 1.6 ** k * 0.4 ** (4 - k) > 0.5) / 16
    ex2 = sum(1 for p in itertools.product((1.6, 0.4), repeat=4) if math.prod(p) > 0.5) / 16
    num_part(it, 'p-boom-bust', 3, ex, ex2, 4)
    ok(abs(1.6 ** 2 * 0.4 ** 2 - 0.4096) < 1e-12 and abs(1.6 ** 3 * 0.4 - 1.6384) < 1e-12, 'boom: printed 0.4096 and 1.6384')
    wrong_is(it, 'p-boom-bust', 3, 'two-ups', 11 / 16)
    wrong_is(it, 'p-boom-bust', 3, 'all-up', 1 / 16)
    wrong_is(it, 'p-boom-bust', 3, 'three-only', 4 / 16)
    t1 = 10 * 0.9 ** 100 / (1 - math.sqrt(0.9))
    t2 = sum(0.9 ** (n / 2) / 0.1 for n in range(200, 6000))
    num_part(it, 'p-boom-bust', 4, t1, t2, 5, eps=1e-9)
    ok(round(0.9 ** 100, 8) == 0.00002656 and round(1 - math.sqrt(0.9), 4) == 0.0513 and round(math.sqrt(0.9), 4) == 0.9487, 'boom: printed 0.00002656, 0.0513, 0.9487')
    ok(all(abs(round(10 * a / b, 5) - 0.005176) <= 5e-6 for a in (0.9 ** 100, 0.00002656) for b in (1 - math.sqrt(0.9), 0.0513, 1 - 0.9487)), 'boom: part 4 carried forward with each printed figure stays in the band')
    wrong_is(it, 'p-boom-bust', 4, 'one-day', 10 * 0.9 ** 100, 6)
    wrong_is(it, 'p-boom-bust', 4, 'no-root', t1 / 10, 6)
    wrong_is(it, 'p-boom-bust', 4, 'epsilon', t1 * 10, 5)
    ok(all(10 * 0.9 ** (m / 2) / (1 - math.sqrt(0.9)) > 10 * 0.9 ** ((m + 1) / 2) / (1 - math.sqrt(0.9)) for m in range(1, 400)) and 10 * 0.9 ** 500 / 0.0513 < 1e-20, 'boom: the tail bound falls to 0')
    ms1 = 1.36 ** 10
    ms2 = pathsE(10, lambda x: x * x)
    num_part(it, 'p-boom-bust', 5, ms1, ms2, 2, eps=1e-9)
    ok(abs((2.56 + 0.16) / 2 - 1.36) < 1e-12, 'boom: E[M_1^2] = 1.36')
    wrong_is(it, 'p-boom-bust', 5, 'mean-sq', 1)
    wrong_is(it, 'p-boom-bust', 5, 'added', 1.36 * 10)
    wrong_is(it, 'p-boom-bust', 5, 'one-day', 1.36)

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


# ---------------------------------------------------------------- level 3
def level3():
    it = load(3)
    if it is None:
        return
    structural(it, 3)
    # p-nested-forecasts
    pr = [F(1, 10), F(3, 20), F(1, 4), F(1, 5), F(1, 5), F(1, 10)]
    x = [-3, 1, 5, 2, 6, -4]
    G = [[0], [1, 2], [3, 4], [5]]
    H = [[0, 1, 2], [3, 4, 5]]
    ok(sum(pr) == 1, 'forecasts: chances add to 1')
    def ce(at):
        y = [None] * 6
        for A in at:
            m = sum(pr[i] * x[i] for i in A) / sum(pr[i] for i in A)
            for i in A:
                y[i] = m
        return y
    def proj(at):   # method 2: weighted least squares onto the indicators of the atoms
        B = np.array([[1.0 if i in A else 0.0 for A in at] for i in range(6)])
        W = np.sqrt(np.array([float(q) for q in pr]))
        coef = np.linalg.lstsq(B * W[:, None], np.array(x, float) * W, rcond=None)[0]
        return B @ coef
    yG, yH = ce(G), ce(H)
    pG, pH = proj(G), proj(H)
    def count_events(at):
        fam = {frozenset()}
        for A in at:
            fam |= {f | frozenset(A) for f in fam}
        return fam
    eG, eH = count_events(G), count_events(H)
    ok(eH <= eG, 'forecasts: H is inside G')
    num_part(it, 'p-nested-forecasts', 1, 2 ** 4 - 2 ** 2, len(eG - eH))
    wrong_is(it, 'p-nested-forecasts', 1, 'all', 16)
    wrong_is(it, 'p-nested-forecasts', 1, 'atoms', 4 - 2)
    num_part(it, 'p-nested-forecasts', 2, float(yG[1]), float(pG[1]), 1)
    wrong_is(it, 'p-nested-forecasts', 2, 'unweighted', (1 + 5) / 2)
    wrong_is(it, 'p-nested-forecasts', 2, 'no-divide', float(pr[1] * 1 + pr[2] * 5))
    tower = (pr[0] * yG[0] + (pr[1] + pr[2]) * yG[1]) / (pr[0] + pr[1] + pr[2])
    num_part(it, 'p-nested-forecasts', 3, float(tower), float(pH[0]), 1)
    ok(tower == yH[0], 'forecasts: tower property on the cut atom')
    wrong_is(it, 'p-nested-forecasts', 3, 'unweighted', float((yG[0] + yG[1]) / 2))
    wrong_is(it, 'p-nested-forecasts', 3, 'finer', float(yG[1]))
    mse = lambda y: sum(pr[i] * (x[i] - y[i]) ** 2 for i in range(6))
    mG = mse(yG)
    num_part(it, 'p-nested-forecasts', 4, float(mG), float(sum(float(pr[i]) * (x[i] - pG[i]) ** 2 for i in range(6))), 2)
    wrong_is(it, 'p-nested-forecasts', 4, 'one-atom', float(pr[1] * (1 - yG[1]) ** 2 + pr[2] * (5 - yG[2]) ** 2))
    EX = sum(pr[i] * x[i] for i in range(6))
    ok(EX == F(23, 10), 'forecasts: E[X] = 2.3 as printed')
    wrong_is(it, 'p-nested-forecasts', 4, 'overall-mean', float(mse([EX] * 6)))
    ok(yH[3] == F(12, 5) and yH[0] == F(11, 5), 'forecasts: E[X|H] is 2.2 and 2.4 as printed')
    gap = sum(pr[i] * (yG[i] - yH[i]) ** 2 for i in range(6))
    num_part(it, 'p-nested-forecasts', 5, float(gap), float(mse(yH) - mG), 2)
    ok([float(q) for q in (pr[0] * (yG[0] - yH[0]) ** 2, (pr[1] + pr[2]) * (yG[1] - yH[1]) ** 2, (pr[3] + pr[4]) * (yG[3] - yH[3]) ** 2, pr[5] * (yG[5] - yH[5]) ** 2)] == [2.704, 0.676, 1.024, 4.096], 'forecasts: printed gap terms')
    wrong_is(it, 'p-nested-forecasts', 5, 'mse-h', float(mse(yH)))
    wrong_is(it, 'p-nested-forecasts', 5, 'one-side', 2.704 + 0.676)

    # p-doob-split
    sv = sp.Symbol('s')
    Xs = {1: F(7, 10), -1: F(3, 10)}
    drift = sp.expand(sum(sp.Rational(q.numerator, q.denominator) * ((sv + st) ** 2 - sv ** 2) for st, q in Xs.items()))
    SYM['s'] = sv
    expr_part(it, 'p-doob-split', 1, drift)
    ok(sp.simplify(drift - (sp.Rational(4, 5) * sv + 1)) == 0, 'doob: drift of S^2 is 0.8s + 1')
    A = lambda path: sum(F(4, 5) * sum(path[:k]) + 1 for k in range(len(path)))   # S_k = sum of first k steps
    num_part(it, 'p-doob-split', 2, float(A([1, 1, -1])), 1 + 1.8 + 2.6, 1)
    wrong_is(it, 'p-doob-split', 2, 'one-more', float(A([1, 1, -1]) + F(4, 5) * 1 + 1))
    wrong_is(it, 'p-doob-split', 2, 'shifted', 1.8 + 2.6 + 1.8)
    wrong_is(it, 'p-doob-split', 2, 'fair', 3)
    ok(A([-1, -1, 1]) == F(3, 5), 'doob: A_3 on down, down, up is 0.6')
    choice_key(it, 'p-doob-split', 3, 'pred')
    paths = list(itertools.product([1, -1], repeat=3))
    ES2 = sum(np.prod([float(Xs[st]) for st in pth]) * sum(pth) ** 2 for pth in paths)
    EA = sum(np.prod([float(Xs[st]) for st in pth]) * float(A(list(pth))) for pth in paths)
    num_part(it, 'p-doob-split', 4, ES2, EA, 2)
    ok(abs(3 * 0.84 + 1.2 ** 2 - ES2) < 1e-12, 'doob: variance check 3.96')
    # M is a martingale: E[M_{n+1} - M_n | F_n] = 0 on every prefix
    for pre in itertools.chain.from_iterable(itertools.product([1, -1], repeat=r) for r in range(3)):
        pre = list(pre)
        Mn = sum(pre) ** 2 - A(pre)
        nxt = sum(float(Xs[st]) * float(sum(pre + [st]) ** 2 - A(pre + [st])) for st in (1, -1))
        ok(abs(nxt - float(Mn)) < 1e-12, f'doob: M is a martingale after {pre}')
    wrong_is(it, 'p-doob-split', 4, 'fair', 3)
    wrong_is(it, 'p-doob-split', 4, 'mean-squared', 1.2 ** 2)
    wrong_is(it, 'p-doob-split', 4, 'path', 5.4)

    # p-two-ups-stop
    res = []
    for pth in itertools.product([1, -1], repeat=4):
        S, T = 0, 4
        for k in range(4):
            S += pth[k]
            if k >= 1 and pth[k] == 1 and pth[k - 1] == 1:
                T = k + 1
                break
        res.append((T, S))
    q = F(1, 16)
    PT = {t: sum(q for T, S in res if T == t) for t in (2, 3, 4)}
    ok(PT[2] == F(1, 4) and PT[3] == F(1, 8) and PT[4] == F(5, 8), 'stop: P(T) by enumeration')
    num_part(it, 'p-two-ups-stop', 1, float(PT[3]), 0.5 ** 3, 3)
    wrong_is(it, 'p-two-ups-stop', 1, 'any-pair', 0.25)
    wrong_is(it, 'p-two-ups-stop', 1, 'four-days', 1 / 16)
    ET = sum(q * T for T, S in res)
    num_part(it, 'p-two-ups-stop', 2, float(ET), 2 * 0.25 + 3 * 0.125 + 4 * 0.625, 3)
    wrong_is(it, 'p-two-ups-stop', 2, 'any-pair', 2 * 0.25 + 3 * 0.25 + 4 * 0.5)
    wrong_is(it, 'p-two-ups-stop', 2, 'equal', 3)
    ES = sum(q * S for T, S in res)
    num_part(it, 'p-two-ups-stop', 3, float(ES), 0, 3)
    wrong_is(it, 'p-two-ups-stop', 3, 'early-only', 2 * 0.25 + 1 * 0.125)
    ES2 = sum(q * S * S for T, S in res)
    num_part(it, 'p-two-ups-stop', 4, float(ES2), float(ET), 3)
    wrong_is(it, 'p-two-ups-stop', 4, 'fixed-day', 4)
    wrong_is(it, 'p-two-ups-stop', 4, 'square-of-mean', 0)
    E4 = sum(q * S for T, S in res if T == 4)
    num_part(it, 'p-two-ups-stop', 5, float(E4), 0 - (2 * 0.25 + 1 * 0.125), 3)
    ok(all(S == 2 for T, S in res if T == 2) and all(S == 1 for T, S in res if T == 3), 'stop: early stops earn 2 and 1')
    wrong_is(it, 'p-two-ups-stop', 5, 'sign', 0.625)
    wrong_is(it, 'p-two-ups-stop', 5, 'conditional', float(E4 / PT[4]))

    # p-trial-stake (session AF, replaces p-red-card-call)
    # paths: (chance, news list, X); news decides in order trial, approval, sales
    paths = [(F(2, 5), ('fail',), 20), (F(3, 5) * F(1, 4), ('ok', 'refuse'), 40),
             (F(3, 5) * F(3, 4) * F(4, 5), ('ok', 'approve', 'strong'), 100), (F(3, 5) * F(3, 4) * F(1, 5), ('ok', 'approve', 'weak'), 50)]
    ok(sum(p for p, _, _ in paths) == 1, 'trial: chances add to 1')
    def Mn(n, news):
        pre = news[:n]
        grp = [(p, x) for p, nw, x in paths if nw[:n] == pre]
        return sum(p * x for p, x in grp) / sum(p for p, _ in grp)
    M1ok = Mn(1, ('ok',))
    num_part(it, 'p-trial-stake', 1, float(M1ok), 0.75 * (0.8 * 100 + 0.2 * 50) + 0.25 * 40, 2)
    wrong_is(it, 'p-trial-stake', 1, 'approved', float(Mn(2, ('ok', 'approve'))))
    wrong_is(it, 'p-trial-stake', 1, 'no-refusal', 0.75 * 90)
    wrong_is(it, 'p-trial-stake', 1, 'unweighted', (100 + 50 + 40) / 3, 2)
    M0 = Mn(0, ())
    ok(M0 == F(109, 2) and abs(0.6 * 77.5 + 0.4 * 20 - 54.5) < 1e-12, 'trial: printed M_0 = 0.6 x 77.5 + 0.4 x 20 = 54.5 (tower)')
    ok([float(p) for p, _, _ in paths] == [0.4, 0.15, 0.36, 0.09], 'trial: printed end chances 0.4, 0.15, 0.36, 0.09')
    # martingale check at every node
    for n in range(0, 3):
        for news in {nw[:n] for _, nw, _ in paths if len(nw) > n}:
            kids = [(p, nw) for p, nw, _ in paths if nw[:n] == news and len(nw) > n]
            tot = sum(p for p, _ in kids)
            ok(sum(p * Mn(n + 1, nw) for p, nw in kids) / tot == Mn(n, news), f'trial: E[M_{n+1} | F_{n}] = M_{n} at {news}')
    def sale(rule):
        out = []
        for p, nw, x in paths:
            T = 3
            for n in range(0, 4):
                if rule(Mn(min(n, len(nw)), nw)):
                    T = n
                    break
            out.append((p, T, Mn(min(T, len(nw)), nw), x))
        return out
    s80 = sale(lambda m: m >= 80)
    PT2 = sum(p for p, T, _, _ in s80 if T == 2)
    num_part(it, 'p-trial-stake', 2, float(PT2), 0.6 * 0.75, 2)
    ok(all(T in (2, 3) for _, T, _, _ in s80), 'trial: the 80 rule sells at 2 or 3')
    wrong_is(it, 'p-trial-stake', 2, 'at-success', 0.6)
    wrong_is(it, 'p-trial-stake', 2, 'strong', 0.36)
    wrong_is(it, 'p-trial-stake', 2, 'approval', 0.75)
    choice_key(it, 'p-trial-stake', 3, 'both')
    sl = sale(lambda m: m <= 45)
    ok(sum(p * m for p, _, m, _ in s80) == M0 == sum(p * m for p, _, m, _ in sl) == F(109, 2), 'trial: both rules have mean sale price 54.5 (optional stopping, by enumeration)')
    EMT2 = sum(p * m * m for p, _, m, _ in s80)
    v1 = float(EMT2 - M0 ** 2)
    v2 = 0.45 * 8100 + 0.4 * 400 + 0.15 * 1600 - 54.5 ** 2
    num_part(it, 'p-trial-stake', 4, v1, v2, 2)
    VX = float(sum(p * x * x for p, _, x in paths) - M0 ** 2)
    ok(abs(VX - 1254.75) < 1e-9 and abs(float(EMT2) - 4045) < 1e-9 and abs(54.5 ** 2 - 2970.25) < 1e-9, 'trial: printed 1254.75, 4045, 2970.25')
    wrong_is(it, 'p-trial-stake', 4, 'hold', VX)
    wrong_is(it, 'p-trial-stake', 4, 'no-mean', float(EMT2))
    wrong_is(it, 'p-trial-stake', 4, 'gap', VX - v1)
    ok(abs(float(sum(p * (x - m) ** 2 for p, _, m, x in s80)) - (VX - v1)) < 1e-9, 'trial: the gap 180 is E[(X - M_T)^2]')

    lv = Level('measure-prob', 3)
    lv.check_wrongs('problems')
    ok(all(r_[0] for r_ in lv.results), 'level 3: numbers_lib check_wrongs')


level1()
level2()
level3()
print(f'{checks} checks, {len(fails)} failures')
sys.exit(1 if fails else 0)
