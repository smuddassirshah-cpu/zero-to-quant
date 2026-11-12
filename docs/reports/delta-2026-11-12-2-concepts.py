#!/usr/bin/env python3
"""Concept checks for the delta audit batch 2 of 12 Nov 2026 (docs/reviews/audit-delta-2026-11-12-2.md).

Part A recomputes every new or changed slip value by the route its feedback names, and checks that no
tolerance band of a touched widget overlaps another (key or slip), as the engine grades them
(grade.js `within`: |v - x| <= abs + 1e-9, key first, then `wrong` in order).
Part B draws the three odes fluency sets with the engine sampler (node tools/fluency-sample.mjs) and
checks every key, wrong value and stated constant from the drawn variables alone, with sympy: each key
is substituted into its equation and starting values.

Run from the repository root: python3 docs/reports/delta-2026-11-12-2-concepts.py
Exit 0 on correct content. A check that fails because the content is wrong prints `FINDING n` and
keeps the exit code at 1 until the content is fixed.
"""
import json, math, os, re, subprocess, sys
from fractions import Fraction as F
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(ROOT, 'app')
C = os.path.join(APP, 'content', 'courses')
fails, findings, n_checks = [], [], 0


def check(name, ok, finding=None):
    global n_checks
    n_checks += 1
    if ok:
        return
    if finding:
        findings.append(f'FINDING {finding}: {name}')
    else:
        fails.append(name)


def load(rel):
    return json.load(open(os.path.join(C, rel), encoding='utf-8'))


def at(doc, path):
    o = doc
    for tok in re.findall(r'[A-Za-z_]+|\[\d+\]', path):
        o = o[int(tok[1:-1])] if tok.startswith('[') else o[tok]
    return o


def within(v, x, tol):
    return abs(v - x) <= (tol or {}).get('abs', 0) + 1e-9


def grade(w, v):
    """The engine's numGrade: 'ok', a slip id, or None."""
    if within(v, w['answer'], w.get('tol')):
        return 'ok'
    for s in w.get('wrong', []):
        if within(v, s['value'], s.get('tol', {'abs': 1e-9})):
            return s['id']
    return None


def bands_disjoint(w):
    pts = [('key', w['answer'], (w.get('tol') or {}).get('abs', 0))]
    pts += [(s['id'], s['value'], (s.get('tol') or {}).get('abs', 0)) for s in w.get('wrong', [])]
    bad = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a, b = pts[i], pts[j]
            if abs(a[1] - b[1]) <= a[2] + b[2] + 2e-9:
                bad.append((a[0], b[0]))
    return bad


def slip(w, sid):
    return next(s for s in w['wrong'] if s['id'] == sid)


# ---------------------------------------------------------------- Part A: the delta
def part_a():
    # (file, path to the item, slip id, route value, exact key)
    q9 = F(19, 37) ** 9
    rows = [
        ('coding-int/l7-parsing-with-a-stack.json', 'screens[4]', 'sign', abs(math.trunc(-7 / 2)), math.trunc(-7 / 2)),
        ('coding-int/l7-parsing-with-a-stack.json', 'quiz[1]', 'sign', abs(math.trunc(-8 / 3)), math.trunc(-8 / 3)),
        ('coding-int/l8-simulating-the-rules.json', 'screens[9]', 'sign', 13 - 12, 12 - 13),
        ('coding-int/review-2.json', 'items[5]', 'sign', abs(math.trunc(-9 / 4)), math.trunc(-9 / 4)),
        ('game-theory/l9-winners-curse.json', 'screens[5]', 'sign', 0.6 * 12, 0.6 * (1.6 * 30 - 60)),
        ('game-theory/review-2.json', 'items[7]', 'sign', 0.4 * (40 - 30), 0.4 * (1.5 * 20 - 40)),
        ('measure-prob/l15-likelihood-ratios.json', 'screens[5]', 'decimal', 6.73e-7 / 3.185e-5, 100 * 6.73e-7 / 3.185e-5),
        ('mm-games/l11-hedging.json', 'screens[3]', 'decimal', 2 * math.sqrt(1 - 0.8 ** 2) / 100, 2 * math.sqrt(1 - 0.8 ** 2)),
        ('mm-games/l11-hedging.json', 'quiz[1]', 'decimal', 5 * math.sqrt(1 - 0.6 ** 2) / 100, 5 * math.sqrt(1 - 0.6 ** 2)),
        ('mm-games/l17-options-on-a-game.json', 'screens[4]', 'sign2', 3 - 2.70, 2.70 - abs(4 + 6 - 7)),
        ('mm-games/review-3.json', 'items[5]', 'decimal', 2 * math.sqrt(1 - 0.9 ** 2) / 100, 2 * math.sqrt(1 - 0.9 ** 2)),
        ('puzzles/homework-4.json', 'items[6]', 'sign', float(512 * q9 - 1), float(1 - 512 * q9)),
        ('recruiting/l9-sitting-an-assessment.json', 'screens[3]', 'sign', 3 / 4 - 1 / 4, 1 / 4 - 3 / 4),
        # unit "%": the key and slips are stored as fractions (engine divides a typed 0.25 by 100)
        ('conditional/l25-survivorship.json', 'screens[9]', 'sign2', (45 - 40) / 20 / 100, (5 * 8 + 15 * (-3)) / 20 / 100),
        ('conditional/problems-5.json', 'items[3].parts[2]', 'sign', 20 * (31 / 32) ** 20 / (1 - (31 / 32) ** 20), -20 * (31 / 32) ** 20 / (1 - (31 / 32) ** 20)),
        ('conditional/review-5.json', 'items[5]', 'sign', -((1 - 0.55 ** 3) - 7 * 0.55 ** 3), (1 - 0.55 ** 3) - 7 * 0.55 ** 3),
    ]
    for f, p, sid, route, key in rows:
        w = at(load(f), p)['widget']
        s = slip(w, sid)
        check(f'{f} {p}: key {w["answer"]} is the exact value {key:.6g}', within(key, w['answer'], w.get('tol')))
        check(f'{f} {p}: slip {sid} {s["value"]} is its route value {route:.6g}', within(route, s['value'], s.get('tol')))
        check(f'{f} {p}: slip {sid} is not graded correct', grade(w, s['value']) == sid)
        bad = bands_disjoint(w)
        check(f'{f} {p}: bands overlap {bad}', not bad)

    # the routes that read their data from the item itself
    cells = at(load('coding-int/l8-simulating-the-rules.json'), 'screens[9]')['canvas']['params']['cells']
    check('coding-int l8: trades are +12 and -13', cells[3] - cells[1] == 12 and cells[6] - cells[4] == -13
          and 100 * cells[3] >= 105 * cells[1] and 100 * cells[6] <= 97 * cells[4])

    check("conditional problems-5: (31/32)^20 rounds to 0.5299", round((31 / 32) ** 20, 4) == 0.5299)
    check('conditional problems-5: 10.598/0.4701 is 22.54 to the penny', round(10.598 / 0.4701, 2) == 22.54)
    check('puzzles hw4: ten-bet slip unchanged', abs(float(1 - 1024 * F(19, 37) ** 10) + 0.3056) < 5e-5)
    check('conditional review-5: 0.55^3 = 0.166375 and 0.833625 - 7 x 0.166375 = -0.331',
          abs(0.55 ** 3 - 0.166375) < 1e-12 and abs(0.833625 - 7 * 0.166375 + 0.331) < 1e-9)
    check('conditional l25: 40 - 45 over 20 is -0.25', F(5 * 8 + 15 * -3, 20) == F(-1, 4))

    # decimal slips: the value a learner gets by typing the key with a % sign (parseNum divides by 100)
    for f, p in [('measure-prob/l15-likelihood-ratios.json', 'screens[5]'), ('mm-games/l11-hedging.json', 'screens[3]'),
                 ('mm-games/l11-hedging.json', 'quiz[1]'), ('mm-games/review-3.json', 'items[5]')]:
        w = at(load(f), p)['widget']
        check(f'{f} {p}: key typed with a % sign meets the decimal slip', grade(w, w['answer'] / 100) == 'decimal')
        txt = at(load(f), p)['feedback']['byKey']['decimal']
        m = re.match(r'([\d.]+) is ([\d.]+)% written as a decimal\. .* type ([\d.]+) without a % sign\.$', txt)
        check(f'{f} {p}: decimal line quotes the slip and the key',
              bool(m) and float(m.group(1)) == slip(w, 'decimal')['value'] and float(m.group(2)) == w['answer'] == float(m.group(3)))

    # FINDING 1: the decimal band of mm-games review-3 swallows other mistakes
    w = at(load('mm-games/review-3.json'), 'items[5]')['widget']
    var_pct = slip(w, 'var')['value'] / 100          # the variance-share slip typed as "0.38%"
    check('mm-games review-3 items[5]: the decimal band takes 0.0038, the var slip typed with a % sign, and 0.01',
          grade(w, var_pct) != 'decimal' and grade(w, 0.01) != 'decimal', finding=1)

    # FINDING 2: the sign slip of problems-5 misses the value the prompt's own route gives
    w = at(load('conditional/problems-5.json'), 'items[3].parts[2]')['widget']
    check('conditional problems-5 part 3: -22.54 is accepted', grade(w, -22.54) == 'ok')
    check('conditional problems-5 part 3: +22.54 (0.5299 x 20 / 0.4701, the prompt\'s route, sign flipped) is not met by the sign slip',
          grade(w, 22.54) == 'sign', finding=2)

    # FINDING 3: the changed tolerance of review-5 r-low-prior against its own accept line
    it = at(load('conditional/review-5.json'), 'items')
    w = next(i for i in it if i['id'] == 'r-low-prior')['widget']
    check('conditional review-5 r-low-prior: key is 6/13', within(0.3 * 0.6 / (0.3 * 0.6 + 0.7 * 0.3), w['answer'], {'abs': 5e-5}))
    check('conditional review-5 r-low-prior: bands disjoint', not bands_disjoint(w))
    m = re.search(r'\\pm ([\d.]+)', w['accept'])
    check(f'conditional review-5 r-low-prior: accept line says +/- {m.group(1) if m else "?"} but the widget takes +/- {w["tol"]["abs"]}',
          bool(m) and float(m.group(1)) == w['tol']['abs'], finding=3)


# ---------------------------------------------------------------- Part B: odes fluency
T = standard_transformations + (implicit_multiplication_application, convert_xor)
t = sp.Symbol('t')


def tex2sym(s):
    s = s.strip()
    while True:  # innermost \frac{a}{b}
        m = re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', s)
        if not m:
            break
        s = s[:m.start()] + f'(({m.group(1)})/({m.group(2)}))' + s[m.end():]
    while True:  # innermost e^{...}
        m = re.search(r'e\^\{([^{}]*)\}', s)
        if not m:
            break
        s = s[:m.start()] + f'exp({m.group(1)})' + s[m.end():]
    s = re.sub(r'\^\{([^{}]*)\}', r'^(\1)', s)
    s = re.sub(r'(?<![a-z])i(?![a-z])', 'I', s)
    return parse_expr(s, local_dict={'t': t, 'exp': sp.exp, 'I': sp.I}, transformations=T)


def same(a, b):
    return sp.simplify(a - b) == 0


def sample(setid, family, n=120):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', f'odes/{setid}', '--family', family, '--n', str(n), '--json'],
                         cwd=APP, capture_output=True, text=True)
    if out.returncode != 0:
        fails.append(f'sampler failed for {setid}/{family}: {out.stderr[:200]}')
        return []
    return json.loads(out.stdout)['items']


def wr(item, wid):
    return next((x for x in item['wrong'] if x['id'] == wid), None)


def ode_ok(y, rhs):
    """y' = rhs(y, t) identically."""
    return sp.simplify(sp.diff(y, t) - rhs(y)) == 0


def part_b():
    seen = {}

    def note(fam, it):
        seen.setdefault(fam, set()).add(it['prompt'])
        for txt in [it['prompt']] + it['solution'] + [x['line'] for x in it['wrong']]:
            check(f'{fam} seed {it["seed"]}: broken term in "{txt}"', not re.search(r'[+\-]\s*(=|\$|$)|\+-|--|\{\}', txt))

    # ---- l2 separable
    S = 'fluency-l2-separable'
    for it in sample(S, 'constant-rate'):
        v = it['vars']; k, y0 = v['k'], v['y0']; note('constant-rate', it)
        key = tex2sym(it['answer'])
        check(f'constant-rate {v}: key', same(key, y0 * sp.exp(k * t)) and ode_ok(key, lambda y: k * y) and key.subs(t, 0) == y0)
        a = tex2sym(wr(it, 'constant-added')['tex'])   # route: y = e^{kt} + C fitted to y(0)
        check(f'constant-rate {v}: constant-added', same(a, sp.exp(k * t) + (y0 - 1)) and a.subs(t, 0) == y0 and not ode_ok(a, lambda y: k * y))
        b = tex2sym(wr(it, 'start-not-used')['tex'])   # line: "That solves the equation" but misses the start
        check(f'constant-rate {v}: start-not-used', ode_ok(b, lambda y: k * y) and b.subs(t, 0) == 1 != y0)
    for it in sample(S, 'rate-that-varies'):
        v = it['vars']; a_, b_, y0 = v['a'], v['b'], v['y0']; note('rate-that-varies', it)
        key = tex2sym(it['answer'])
        rhs = lambda y: (b_ * t + a_) * y
        check(f'rate-that-varies {v}: key', same(key, y0 * sp.exp(sp.Rational(b_, 2) * t ** 2 + a_ * t)) and ode_ok(key, rhs) and key.subs(t, 0) == y0)
        w1 = tex2sym(wr(it, 'rate-kept-constant')['tex'])
        check(f'rate-that-varies {v}: rate-kept-constant', same(w1, y0 * sp.exp(a_ * t)) and not ode_ok(w1, rhs))
        w2 = tex2sym(wr(it, 'not-halved')['tex'])
        check(f'rate-that-varies {v}: not-halved', same(w2, y0 * sp.exp(b_ * t ** 2 + a_ * t)) and not ode_ok(w2, rhs))
        check(f'rate-that-varies {v}: integral stated', sp.integrate(b_ * t, t) == sp.Rational(b_, 2) * t ** 2 == it['lets']['h'] * t ** 2)
    for it in sample(S, 'square-rate'):
        v = it['vars']; k, y0 = v['k'], v['y0']; note('square-rate', it)
        key = tex2sym(it['answer'])
        rhs = lambda y: k * y ** 2
        check(f'square-rate {v}: key', same(key, y0 / (1 - k * y0 * t)) and ode_ok(key, rhs) and key.subs(t, 0) == y0)
        w1 = tex2sym(wr(it, 'solved-linear')['tex'])
        check(f'square-rate {v}: solved-linear', same(w1, y0 * sp.exp(k * t)) and ode_ok(w1, lambda y: k * y) and not ode_ok(w1, rhs))
        w2 = tex2sym(wr(it, 'sign-lost')['tex'])       # route: +1/y = kt + C, C = 1/y0
        check(f'square-rate {v}: sign-lost', same(w2, 1 / (k * t + sp.Rational(1, y0))) and not ode_ok(w2, rhs))
        # stated constants: C = -1/y0 and 1/y = 1/y0 - kt
        Cc = sp.Rational(-1, y0)
        check(f'square-rate {v}: C', sp.Rational(str(it['lets']['c'])) == Cc and same(-1 / key, k * t + Cc))
    for it in sample(S, 'discount', 200):
        v = it['vars']; p, r, yr = v['p'], v['r'], v['yr']; note('discount', it)
        key = p * math.exp(-r * yr / 100)
        check(f'discount {v}: key', abs(float(it['answer']) - key) <= 0.005 + 1e-9)
        s1 = wr(it, 'simple-discount'); s2 = wr(it, 'yearly-discount')
        check(f'discount {v}: simple', abs(float(s1['value']) - p * (1 - r * yr / 100)) < 1e-9 and abs(float(s1['value']) - key) > 0.0102)
        if s2:
            check(f'discount {v}: yearly', abs(float(s2['value']) - p / (1 + r / 100) ** yr) <= 0.005 + 1e-9
                  and abs(float(s2['value']) - float(it['answer'])) > 0.01)
            check(f'discount {v}: yearly line shows 1.0r^n', f'1.0{r}^{{{yr}}}' in s2['line'])
        check(f'discount {v}: rT stated', f'rT = {r * yr / 100:g}' in it['solution'][0])
    # every draw of discount, by enumeration: bands, and the placeholder against the key
    doc = load('odes/' + S + '.json'); fam = next(f for f in doc['families'] if f['id'] == 'discount')
    ph = float(re.search(r'[\d.]+', fam['widget']['placeholder']).group())
    leak = [(p, r, yr) for p in range(100, 901, 100) for r in range(1, 10) for yr in range(2, 11)
            if abs(round(p * math.exp(-r * yr / 100), 2) - ph) < 0.0051]
    check(f'odes l2 discount: the placeholder "{fam["widget"]["placeholder"]}" is the key of the draws (p, r, years) = {leak}', not leak, finding=5)
    for p in range(100, 901, 100):
        for r in range(1, 10):
            for yr in range(2, 11):
                key = p * math.exp(-r * yr / 100)
                check(f'discount ({p},{r},{yr}): simple band clear of key', abs(p * (1 - r * yr / 100) - key) > 0.0102 + 0.005)

    # ---- l3 integrating factor
    S = 'fluency-l3-integrating-factor'
    for it in sample(S, 'find-the-factor'):
        v = it['vars']; n, m, s = v['n'], v['m'], v['s']; note('find-the-factor', it)
        pfun = s * m * t ** n
        key = tex2sym(it['answer'])
        y = sp.Function('y')(t)
        # mu (y' + p y) must be (mu y)'
        check(f'find-the-factor {v}: key', same(key, sp.exp(sp.integrate(pfun, t))) and sp.simplify(key * (sp.diff(y, t) + pfun * y) - sp.diff(key * y, t)) == 0)
        check(f'find-the-factor {v}: prompt sign', ("y' + " if s == 1 else "y' - ") in it['prompt'])
        w1 = tex2sym(wr(it, 'e-to-the-p')['tex']); w2 = tex2sym(wr(it, 'sign-flipped')['tex'])
        check(f'find-the-factor {v}: e-to-the-p', same(w1, sp.exp(pfun)) and not same(w1, key))
        check(f'find-the-factor {v}: sign-flipped', same(w2, sp.exp(-sp.integrate(pfun, t))) and not same(w2, key))
    for it in sample(S, 'constant-coefficient'):
        v = it['vars']; a_, s, y0 = v['a'], v['s'], v['y0']; note('constant-coefficient', it)
        q = -a_ * s
        rhs = lambda y: a_ * y + q
        key = tex2sym(it['answer'])
        check(f'constant-coefficient {v}: key', ode_ok(key, rhs) and key.subs(t, 0) == y0 and same(key, (y0 - s) * sp.exp(a_ * t) + s))
        w1 = tex2sym(wr(it, 'steady-sign')['tex'])     # route: steady level taken as +q/a
        lvl = sp.Rational(q, a_)
        check(f'constant-coefficient {v}: steady-sign', same(w1, (y0 - lvl) * sp.exp(a_ * t) + lvl) and not ode_ok(w1, rhs) and a_ * s + q == 0)
        w2 = wr(it, 'inflow-dropped')
        if w2:
            w2 = tex2sym(w2['tex'])
            check(f'constant-coefficient {v}: inflow-dropped', same(w2, y0 * sp.exp(a_ * t)) and ode_ok(w2, lambda y: a_ * y) and not ode_ok(w2, rhs))
        else:
            check(f'constant-coefficient {v}: inflow-dropped withheld only at y0 = 0', y0 == 0)
    for it in sample(S, 'savings-balance', 200):
        v = it['vars']; r, d, n = v['r'], v['d'], v['n']; note('savings-balance', it)
        B = sp.Function('B')
        sol = sp.dsolve(sp.Eq(B(t).diff(t), sp.Rational(r, 100) * B(t) + d), B(t), ics={B(0): 0}).rhs
        key = float(sol.subs(t, n))
        check(f'savings {v}: key', abs(float(it['answer']) - key) <= 0.005 + 1e-6)
        check(f'savings {v}: deposits-only', float(wr(it, 'deposits-only')['value']) == d * n and abs(d * n - key) > 0.02)
        check(f'savings {v}: minus-one-dropped', abs(float(wr(it, 'minus-one-dropped')['value']) - (key + d * 100 / r)) <= 0.011)
        check(f'savings {v}: exponent stated', f'the exponent is ${r * n / 100:g}$' in it['solution'][1])
    fam = next(f for f in load('odes/' + S + '.json')['families'] if f['id'] == 'savings-balance')
    ph = float(re.search(r'[\d.]+', fam['widget']['placeholder']).group())
    leak = [(r, d, n) for r in range(2, 9) for d in range(100, 901, 100) for n in range(3, 16)
            if abs(round(d * 100 / r * (math.exp(r * n / 100) - 1), 2) - ph) < 0.0051]
    check(f'odes l3 savings: placeholder {ph} is no draw\'s key {leak}', not leak)

    # ---- l7 characteristic equation
    S = 'fluency-l7-characteristic-equation'
    R = sp.Symbol('r')
    for it in sample(S, 'real-roots'):
        v = it['vars']; r1, r2 = v['r1'], v['r2']; note('real-roots', it)
        b, c = -(r1 + r2), r1 * r2
        roots = set(sp.roots(R ** 2 + b * R + c, R).keys())
        check(f'real-roots {v}: key', {int(x) for x in it['answers']} == roots == {r1, r2} and it['lets']['b'] == b and it['lets']['c'] == c)
        f1 = {int(x) for x in wr(it, 'signs-flipped')['value'].split(',')}
        check(f'real-roots {v}: signs-flipped', f1 == set(sp.roots(R ** 2 - b * R + c, R).keys()) and f1 != roots)
        f2 = {int(x) for x in wr(it, 'not-halved')['value'].split(',')}
        disc = sp.sqrt(b * b - 4 * c)
        check(f'real-roots {v}: not-halved', f2 == {-b + disc, -b - disc} and f2 != roots)
        for rr in roots:  # e^{rt} solves the equation
            yv = sp.exp(rr * t)
            check(f'real-roots {v}: e^({rr}t) solves', sp.simplify(yv.diff(t, 2) + b * yv.diff(t) + c * yv) == 0)
    for it in sample(S, 'complex-root'):
        v = it['vars']; al, be = v['al'], v['be']; note('complex-root', it)
        b, c = -2 * al, al * al + be * be
        key = tex2sym(it['answer'])
        check(f'complex-root {v}: key', sp.expand(key ** 2 + b * key + c) == 0 and sp.im(key) > 0 and key == al + be * sp.I)
        check(f'complex-root {v}: other-root', tex2sym(wr(it, 'other-root')['tex']) == sp.conjugate(key))
        check(f'complex-root {v}: minus-b-dropped', tex2sym(wr(it, 'minus-b-dropped')['tex']) == sp.Rational(b, 2) + be * sp.I)
        check(f'complex-root {v}: not-halved', tex2sym(wr(it, 'not-halved')['tex']) == sp.Rational(-b, 2) + sp.sqrt(b * b - 4 * c))
        check(f'complex-root {v}: discriminant', it['lets']['disc'] == b * b - 4 * c == -4 * be * be and it['lets']['b2'] == 2 * be and it['lets']['nb'] == -b)
    for it in sample(S, 'fit-two-roots', 200):
        v = it['vars']; r1, r2, c1, c2 = v['r1'], v['r2'], v['c1'], v['c2']; note('fit-two-roots', it)
        b, c = -(r1 + r2), r1 * r2
        y0, v0 = c1 + c2, r1 * c1 + r2 * c2
        Y = sp.Function('y')
        sol = sp.dsolve(Y(t).diff(t, 2) + b * Y(t).diff(t) + c * Y(t), Y(t), ics={Y(0): y0, Y(t).diff(t).subs(t, 0): v0}).rhs
        key = tex2sym(it['answer'])
        check(f'fit-two-roots {v}: key', same(key, sol) and f'y(0) = {y0}$' in it['prompt'] and f"y'(0) = {v0}$" in it['prompt'])
        for wid in ('constants-swapped', 'one-constant'):
            w_ = wr(it, wid)
            if not w_:
                check(f'fit-two-roots {v}: {wid} withheld only where it is no slip', (wid == 'constants-swapped' and c1 == c2) or (wid == 'one-constant' and y0 == 0))
                continue
            e = tex2sym(w_['tex'])
            want = c2 * sp.exp(r1 * t) + c1 * sp.exp(r2 * t) if wid == 'constants-swapped' else y0 * sp.exp(r1 * t)
            check(f'fit-two-roots {v}: {wid}', same(e, want) and not same(e, key) and e.subs(t, 0) == y0)
    for it in sample(S, 'repeated-root'):
        v = it['vars']; r, y0, k = v['r'], v['y0'], v['k']; note('repeated-root', it)
        b, c, v0 = -2 * r, r * r, k + r * y0
        Y = sp.Function('y')
        sol = sp.dsolve(Y(t).diff(t, 2) + b * Y(t).diff(t) + c * Y(t), Y(t), ics={Y(0): y0, Y(t).diff(t).subs(t, 0): v0}).rhs
        key = tex2sym(it['answer'])
        check(f'repeated-root {v}: key', same(key, sol) and f"y'(0) = {v0}$" in it['prompt'])
        w1 = tex2sym(wr(it, 'rc1-forgotten')['tex']); w2 = tex2sym(wr(it, 't-term-dropped')['tex'])
        check(f'repeated-root {v}: rc1-forgotten', same(w1, (v0 * t + y0) * sp.exp(r * t)) and not same(w1, key))
        check(f'repeated-root {v}: t-term-dropped', same(w2, y0 * sp.exp(r * t)) and not same(w2, key))
        check(f'repeated-root {v}: c2 arithmetic', v0 - r * y0 == k and it['lets']['ry'] == r * y0)

    # FINDING 4: families whose key is a function of t but whose prompt never names t
    for setid, famid in [('fluency-l3-integrating-factor', 'constant-coefficient'), ('fluency-l7-characteristic-equation', 'fit-two-roots'),
                         ('fluency-l7-characteristic-equation', 'repeated-root')]:
        fam = next(f for f in load(f'odes/{setid}.json')['families'] if f['id'] == famid)
        check(f'odes {setid} {famid}: the key is written in t but the prompt does not name t',
              bool(re.search(r'\(t\)|dt', fam['prompt'])), finding=4)
    return seen


if __name__ == '__main__':
    part_a()
    seen = part_b()
    for f, s in seen.items():
        print(f'  odes {f}: {len(s)} distinct draws checked')
    print(f'{n_checks} checks, {len(fails)} failed outside the findings, {len(findings)} finding checks failing')
    for x in fails[:40]:
        print('FAIL', x)
    for x in findings:
        print(x)
    sys.exit(1 if fails or findings else 0)
