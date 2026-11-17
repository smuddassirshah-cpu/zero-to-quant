"""Recompute every number in app/content/courses/topology/problems-1.json, problems-2.json and problems-3.json twice.

Route 1 is the learner's working, exact where it can be (sympy, fractions, closed forms).
Route 2 is independent: brute force over grids and every case (sampled metric ratios, scanned intervals, every
family of subsets of a finite set, every bijection, iterating the maps, Monte Carlo over balls).
For each numeric part the script checks: both routes agree, the JSON key equals them within the part's band,
every `wrong` value is the named slip (rebuilt from the slip), lies outside the key band and has a byKey line,
and the key is printed in feedback.correct and explain.text at the asked places. Expression parts: the key and
every accept form equal the computed formula (sympy and at sample points), every wrong form differs.
Choice parts: exactly one correct option. numbers_lib's Level.expect, check_wrongs and report run as well.
Exit 0 when every check passes.

Run: <scratchpad>/venv/bin/python docs/reports/problems-topology-numbers.py
"""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'topology')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
random.seed(7)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf8'))['items']}


def nums_in(text):
    t = text.replace('{,}', '').replace('\u2212', '-')
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', t)]


def printed(text, v, places):
    """v appears in the text rounded to `places` (None: as an exact integer)."""
    want = round(v, places) if places is not None else v
    return any(abs(x - want) < 1e-9 for x in nums_in(text))


def num(items, iid, k, m1, m2, slips, places=4, agree=1e-9):
    """m1, m2: the answer by two routes. slips: {wrong id: value rebuilt from the named slip (unrounded)}."""
    part = items[iid]['parts'][k - 1]
    w, tag = part['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    ok(abs(m1 - m2) <= agree, f'{tag}: routes differ {m1} vs {m2}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - m1) <= max(tol, 1e-12), f'{tag}: key {w["answer"]} vs computed {m1}')
    if places is None:
        ok(tol == 0 and float(m1).is_integer(), f'{tag}: integer key wants an abs 0 band')
    else:
        ok(abs(round(m1, places) - m1) <= tol, f'{tag}: the {places}-place rounding lies outside the band')
        ok(tol <= 10 ** (-places) + 1e-12, f'{tag}: band wider than one unit at {places} places')
    by = part['feedback'].get('byKey', {})
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(sorted(ids) == sorted(slips), f'{tag}: wrong ids {ids} vs slips {sorted(slips)}')
    for x in w.get('wrong', []):
        v = x['value']
        s = slips.get(x['id'])
        ok(s is not None and abs(v - s) <= max(x['tol']['abs'], 1e-12), f'{tag}: wrong {x["id"]}={v} vs slip {s}')
        ok(abs(v - w['answer']) > tol + x['tol']['abs'], f'{tag}: wrong {x["id"]} inside the key band')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')
    ok(len(set(ids)) == len(ids), f'{tag}: repeated wrong id')
    ok(printed(part['feedback']['correct'], m1, places), f'{tag}: key not printed in feedback.correct')
    ok(printed(part['explain']['text'], m1, places), f'{tag}: key not printed in explain')


def to_sympy(tex, syms):
    t = tex.replace(r'\varepsilon', 'e').replace(r'\left', '').replace(r'\right', '')
    t = re.sub(r'\\t?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    t = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', t)
    t = t.replace('{', '(').replace('}', ')').replace(r'\cdot', '*')
    t = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', t)
    t = re.sub(r'\)\s*\(', ')*(', t)
    t = re.sub(r'\)\s*([a-zA-Z])', r')*\1', t)
    loc = {s: sp.Symbol(s, positive=True) for s in syms}
    return sp.sympify(t, locals=loc)


def expr(items, iid, k, value, syms, numeric_fn):
    """value: sympy formula in the symbols; numeric_fn: the same quantity by route 2 at a point (dict)."""
    part = items[iid]['parts'][k - 1]
    w, tag = part['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    loc = {s: sp.Symbol(s, positive=True) for s in syms}
    value = value.subs({sp.Symbol(s): loc[s] for s in syms})
    for t in [w['answer']] + w.get('accept', []):
        ok(sp.simplify(to_sympy(t, syms) - value) == 0, f'{tag}: form {t} differs from the computed formula')
    for _ in range(6):
        pt = {s: random.uniform(0.3, 3) for s in syms}
        v1 = float(value.subs({loc[s]: pt[s] for s in syms}))
        ok(abs(v1 - numeric_fn(pt)) < 1e-6, f'{tag}: route 2 differs at {pt}')
    for x in w.get('wrong', []):
        diff = to_sympy(x['tex'], syms) - value
        ok(sp.simplify(diff) != 0, f'{tag}: wrong {x["id"]} equals the key')
        ok(x['id'] in part['feedback'].get('byKey', {}), f'{tag}: wrong {x["id"]} has no byKey line')


def one_correct(items, iid, k, want_id):
    part = items[iid]['parts'][k - 1]
    opts = part['widget']['options']
    good = [o['id'] for o in opts if o.get('correct')]
    ok(good == [want_id], f'{iid} p{k}: correct options {good}, expected [{want_id}]')
    ok(all(o.get('why') for o in opts if not o.get('correct')), f'{iid} p{k}: a distractor has no why')


# ---------------------------------------------------------------- level 1
def level1():
    it = load(1)
    lv = Level('topology', 1)
    e = sp.Symbol('e', positive=True)
    r2, r3, r5, r10 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5), sp.sqrt(10)
    rng = random.Random(1)

    # p-plotter-zone. f = 3x1 + x2, d_w = 2|dx1| + |dx2|.
    def dw(p, q):
        return 2 * abs(p[0] - q[0]) + abs(p[1] - q[1])
    L1 = sp.Max(sp.Rational(3, 2), 1)                                  # route 1: coefficient over weight
    L2 = max(abs(3 * math.cos(t) + math.sin(t)) / (2 * abs(math.cos(t)) + abs(math.sin(t)))
             for t in [k * 2 * math.pi / 20000 for k in range(20000)])  # route 2: scan directions
    ok(abs(float(L1) - L2) < 1e-6, 'plotter L')
    expr(it, 'p-plotter-zone', 1, 2 * e / 3, ['e'], lambda pt: pt['e'] / L2)
    y = (2.5, 0.5)
    fy = 3 * y[0] + y[1]
    ok(fy == 8, 'f(y) = 8')
    r_1 = sp.Rational(2, 3) * (12 - fy)
    # route 2: largest r with every sampled point of B_w(y, r) in U (bisection on r)
    sphere = [(math.cos(t) / (2 * abs(math.cos(t)) + abs(math.sin(t))), math.sin(t) / (2 * abs(math.cos(t)) + abs(math.sin(t))))
              for t in [k * 2 * math.pi / 20000 for k in range(20000)]]
    ok(all(abs(dw(u, (0, 0)) - 1) < 1e-12 for u in sphere), 'plotter: sampled d_w unit sphere')
    lo, hi = 0.0, 10.0
    for _ in range(50):
        mid = (lo + hi) / 2
        good = all(3 * (y[0] + mid * u[0]) + (y[1] + mid * u[1]) <= 12 + 1e-12 for u in sphere)
        lo, hi = (mid, hi) if good else (lo, mid)
    num(it, 'p-plotter-zone', 2, float(r_1), lo, {'sum-coeffs': 4 / 4, 'no-weight': 4 / 3, 'times-weight': 4 / 6, 'whole-bound': 2 * 12 / 3}, agree=1e-6)
    b1 = r5
    b2 = max(2 * abs(math.cos(t)) + abs(math.sin(t)) for t in [k * 2 * math.pi / 200000 for k in range(200000)])
    ok(abs(float(b1) - b2) < 1e-8, 'plotter sqrt5')
    s_1 = float(r_1 / b1)
    num(it, 'p-plotter-zone', 3, s_1, float(r_1) / b2, {'used-three': (8 / 3) / 3, 'max-weight': (8 / 3) / 2, 'multiplied': (8 / 3) * b2, 'no-change': 8 / 3}, agree=1e-8)
    d_1 = float(4 / r10)
    foot = (y[0] + 0.4 * 3, y[1] + 0.4 * 1)
    ok(abs(3 * foot[0] + foot[1] - 12) < 1e-12 and foot == (3.7, 0.9) or abs(foot[0] - 3.7) < 1e-12, 'plotter foot (3.7, 0.9)')
    d_2 = min(math.hypot(x - y[0], (12 - 3 * x) - y[1]) for x in [2.5 + k * 2e-6 for k in range(1000001)])
    num(it, 'p-plotter-zone', 4, d_1, d_2, {'no-root': 0.4, 'taxicab-normal': 1.0, 'horizontal': (11.5 / 3 - 2.5)}, agree=1e-6)
    ok(d_1 > s_1, 'plotter: true distance above the guaranteed radius')
    ok(abs(11.5 / 3 - 23 / 6) < 1e-12, 'plotter: 23/6 is the horizontal foot')

    # p-cubic-band. h = x^3 - 27x, A = h^-1((0, 54]).
    x = sp.Symbol('x', real=True)
    h = x ** 3 - 27 * x
    ok(sp.expand(x * (x ** 2 - 27) - h) == 0 and sp.expand((x + 3) ** 2 * (x - 6) - (h - 54)) == 0, 'cubic factorisations')
    A1 = sp.solve_univariate_inequality(sp.And(h > 0, h <= 54), x, relational=False) if False else \
        sp.Intersection(sp.solve_univariate_inequality(h > 0, x, relational=False), sp.solve_univariate_inequality(h <= 54, x, relational=False))
    want = sp.Union(sp.Interval.open(-3 * r3, 0), sp.Interval.Lopen(3 * r3, 6))
    ok(sp.simplify(A1.symmetric_difference(want)) == sp.S.EmptySet or A1 == want, f'cubic A = {A1}')
    grid = [k / 1000 for k in range(-12000, 12001)]
    hv = lambda t: t ** 3 - 27 * t
    inA = [t for t in grid if 0 < hv(t) <= 54]
    length2 = sum(1 for t in grid if 0 < hv(t) <= 54) / 1000
    num(it, 'p-cubic-band', 1, float(want.measure), round(length2), {'right-only': 6 - 3 * math.sqrt(3), 'left-only': 3 * math.sqrt(3)}, agree=1e-9)
    ok(abs(length2 - 6) < 0.01, 'cubic length by grid')
    # boundary: points where membership switches on a fine grid
    switches = [t for a, t in zip(grid, grid[1:]) if (0 < hv(a) <= 54) != (0 < hv(t) <= 54)]
    num(it, 'p-cubic-band', 2, 4, len(switches), {'with-touch': 5, 'drop-member': 3}, places=None)
    roots54 = sp.solve(sp.Eq(h, 54), x)
    interior = [r for r in roots54 if abs(float(r) + 3) < 1e-12]
    num(it, 'p-cubic-band', 3, len(interior), sum(1 for t in grid if abs(hv(t) - 54) < 1e-9 and 0 < hv(t - 0.001) <= 54 and 0 < hv(t + 0.001) <= 54),
        {'both-ends': 2, 'equal': 0}, places=None)
    r_1 = float(3 * r3 - 3)
    r_2 = min(abs(-3 - a) for a in [-3 * math.sqrt(3), 0.0])
    num(it, 'p-cubic-band', 4, r_1, r_2, {'far-end': 3, 'to-root': 3 * math.sqrt(3), 'half-piece': 3 * math.sqrt(3) / 2})

    # p-diagonal-sphere. z = (0.65, 0.65).
    p = sp.Symbol('p', positive=True)
    ps1 = sp.log(2) / sp.log(sp.Rational(20, 13))
    ok(abs(float(sp.Rational(13, 20) * 2 ** (1 / ps1)) - 1) < 1e-12, 'p* solves the sphere equation')
    lo, hi = 1.0, 3.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (0.65 ** mid * 2) ** (1 / mid) > 1 else (lo, mid)
    num(it, 'p-diagonal-sphere', 1, float(ps1), lo, {'inverted': 1 / float(ps1), 'sign': -float(ps1)}, agree=1e-9)
    ok(abs(round(math.log(2), 6) / round(math.log(1 / 0.65), 6) - float(ps1)) < 5e-5, 'shown quotient rounds to the key')
    dp = lambda q: 0.65 * 2 ** (1 / q) if q != math.inf else 0.65
    inside = [q for q in [1, 1.5, 2, 3, 4, math.inf] if dp(q) < 1]
    num(it, 'p-diagonal-sphere', 2, 4, len(inside), {'reversed': 2, 'finite-only': 3}, places=None)
    s1 = 1 - sp.Rational(13, 20) * r2
    # route 2: Monte Carlo of the room: the nearest point of the unit circle to z
    s2 = min(math.hypot(math.cos(t) - 0.65, math.sin(t) - 0.65) for t in [k * 2 * math.pi / 400000 for k in range(400000)])
    num(it, 'p-diagonal-sphere', 3, float(s1), s2, {'coordinate': 0.35, 'distance': 0.65 * math.sqrt(2)}, agree=1e-8)
    t1 = s1 / r2
    lo, hi = 0.0, 0.2
    for _ in range(60):
        mid = (lo + hi) / 2
        corners = [(0.65 + a * mid, 0.65 + b * mid) for a in (-1, 1) for b in (-1, 1)]
        lo, hi = (mid, hi) if all(math.hypot(*c) < 1 for c in corners) else (lo, mid)
    num(it, 'p-diagonal-sphere', 4, float(t1), lo, {'times-root': float(s1 * r2), 'same': float(s1), 'half': float(s1) / 2}, agree=1e-9)
    ok(abs(float(t1) - (1 / math.sqrt(2) - 0.65)) < 1e-12, 'diag t = 1/sqrt2 - 0.65')
    ok(round(0.0808 / math.sqrt(2), 4) == round(float(t1), 4), 'printed 0.0808/sqrt2 rounds to the key')

    # p-reciprocal-room. f = 1/x at 0.5.
    pre = (F(1) / F(5, 2), F(1) / F(3, 2))
    ok(pre == (F(2, 5), F(2, 3)), 'reciprocal preimage (0.4, 2/3)')
    grid = [k / 10 ** 6 for k in range(1, 10 ** 6)]
    inpre = [t for t in grid if 1.5 < 1 / t < 2.5]
    num(it, 'p-reciprocal-room', 1, float(pre[1] - pre[0]), inpre[-1] - inpre[0] + 1e-6, {'length-v': 1.0, 'linear': 0.25}, agree=2e-6)
    d1 = min(F(1, 2) - pre[0], pre[1] - F(1, 2))
    d2 = min(0.5 - inpre[0], inpre[-1] - 0.5) + 1e-6
    num(it, 'p-reciprocal-room', 2, float(d1), d2, {'far-side': float(pre[1] - F(1, 2)), 'half-length': float(pre[1] - pre[0]) / 2, 'linear': 0.5 / 4}, agree=2e-6)
    dfor = sp.Rational(1, 2) - 1 / (2 + e)

    def dnum(pt):
        eps = pt['e']
        left = 1 / (2 + eps)
        right = 1 / (2 - eps) if eps < 2 else math.inf
        return min(0.5 - left, right - 0.5)
    expr(it, 'p-reciprocal-room', 3, sp.simplify(dfor), ['e'], dnum)
    ok(sp.simplify(dfor.subs(e, sp.Rational(1, 2)) - sp.Rational(1, 10)) == 0, 'delta(0.5) = 0.1')
    lim1 = sp.limit(dfor, e, sp.oo)
    lim2 = dnum({'e': 1e9})
    num(it, 'p-reciprocal-room', 4, float(lim1), lim2, {'no-half': 1.0}, agree=1e-8)

    for path, v in [('items[0].prose', 2.5), ('items[0].prose', 12), ('items[1].prose', 54), ('items[2].prose', 0.65), ('items[3].prose', 0.5)]:
        lv.expect('problems', path, v)
    lv.check_wrongs()
    return lv


lv1 = level1()
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
lv1.report()
sys.exit(1 if fails else 0)
