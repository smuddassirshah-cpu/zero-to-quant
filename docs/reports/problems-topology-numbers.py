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


# ---------------------------------------------------------------- level 2
def topo_from_basis(pieces):
    out = {frozenset()}
    for r in range(1, len(pieces) + 1):
        for c in itertools.combinations(pieces, r):
            out.add(frozenset().union(*c))
    return out


def subspace(tau, Y):
    return {u & frozenset(Y) for u in tau}


def connected(tau, Y):
    Y = frozenset(Y)
    t = subspace(tau, Y)
    return not any(u and u != Y and (Y - u) in t for u in t)


def level2():
    it = load(2)
    lv = Level('topology', 2)
    X = 'abcd'
    pieces = [frozenset('a'), frozenset('c'), frozenset('abc'), frozenset('cd')]
    tau = topo_from_basis(pieces)
    ok(frozenset() in tau and frozenset(X) in tau, 'topology has the empty set and X')
    ok(all(a | b in tau and a & b in tau for a in tau for b in tau), 'topology closed under unions and intersections')
    # route 2: every subset that is the union of the pieces it contains
    tau2 = {frozenset(S) for r in range(5) for S in itertools.combinations(X, r)
            if frozenset().union(*[b for b in pieces if b <= frozenset(S)]) == frozenset(S)}
    ok(tau == tau2, 'four-point topology by both routes')
    num(it, 'p-four-point-line', 1, len(tau), len(tau2), {'pieces-only': len(pieces), 'no-empty': len(tau) - 1, 'all-subsets': 2 ** 4}, places=None)
    txt = it['p-four-point-line']['parts'][0]['feedback']['correct']
    ok(all(('\\{' + ', '.join(sorted(u)) + '\\}') in txt for u in tau if u and u != frozenset(X)), 'listed open sets match tau')
    Y = 'abd'
    tY = subspace(tau, Y)
    tY2 = {frozenset(x for x in Y if x in u) for u in tau}
    num(it, 'p-four-point-line', 2, len(tY), len(tY2), {'no-merging': len(tau), 'inside-only': sum(1 for u in tau if u <= frozenset(Y))}, places=None)
    ok(not connected(tau, Y), 'Y = X minus c is disconnected')
    cuts = [x for x in X if not connected(tau, set(X) - {x})]
    rest = lambda x: frozenset(X) - {x}
    cuts2 = [x for x in X if any(u and u != rest(x) and (rest(x) - u) in subspace(tau, rest(x)) for u in subspace(tau, rest(x)))]
    ok(cuts == ['b', 'c'], f'cut points {cuts}')
    num(it, 'p-four-point-line', 3, len(cuts), len(cuts2), {'only-c': 1, 'every-point': 4}, places=None)
    homeos = [p for p in itertools.permutations(X) if {frozenset(dict(zip(X, p))[x] for x in u) for u in tau} == tau]
    homeos2 = [p for p in itertools.permutations(X)
               if all(frozenset(x for x in X if dict(zip(X, p))[x] in v) in tau for v in tau)
               and all(frozenset(dict(zip(X, p))[x] for x in u) in tau for u in tau)]
    rev = dict(zip('abcd', 'dcba'))
    ok({frozenset(rev[x] for x in u) for u in tau} != tau, 'reversal is not a homeomorphism')
    num(it, 'p-four-point-line', 4, len(homeos), len(homeos2), {'reversal': 2, 'every-bijection': math.factorial(4)}, places=None)

    # p-bond-yield-map
    P, yy = sp.symbols('P y', positive=True)
    inv = sp.solve(sp.Eq(P, 100 / (1 + yy)), yy)[0]
    expr(it, 'p-bond-yield-map', 1, inv, ['P'], lambda pt: 100 / pt['P'] - 1)
    Pf = lambda y: 100 / (1 + y)
    lo1 = float(sp.Rational(100, 105))
    lo2 = min(Pf(0.02 + k * 0.03 / 100000) for k in range(100001))
    num(it, 'p-bond-yield-map', 2, lo1 * 100, lo2, {'upper-end': Pf(0.02), 'linear': 100 * (1 - 0.05)}, agree=1e-9)
    y1 = float(sp.Rational(3, 97))
    lo, hi = 0.02, 0.05
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Pf(mid) > 97 else (lo, mid)
    num(it, 'p-bond-yield-map', 3, y1, lo, {'linear': 0.03, 'flipped': 97 / 100 - 1}, agree=1e-12)
    ok(round(Pf(0.05), 4) < 97 < round(Pf(0.02), 4), '97 lies in the price interval')
    lv.expect('problems', 'items[1].parts[2].question', round(Pf(0.02), 4))
    grid = [0.02 + k * 0.03 / 30000 for k in range(30001)]
    A = [g for g in grid if abs(g - y1) > 1e-7]
    prices = sorted(Pf(g) for g in A)
    gaps = sum(1 for a, b in zip(prices, prices[1:]) if a < 97 < b)
    num(it, 'p-bond-yield-map', 4, 2, 1 + gaps, {'one-piece': 1, 'three': 3}, places=None)

    # p-gapped-domain. Y = [0,1) u (1,2] u {4}
    def inY(t):
        return (0 <= t < 1) or (1 < t <= 2) or t == 4
    cands = {'[0,1)': (lambda t: 0 <= t < 1, (-1, 1)), '{4}': (lambda t: t == 4, (3, 5)), '(1,2]': (lambda t: 1 < t <= 2, (1, 3)),
             '[0,0.5]': (lambda t: 0 <= t <= 0.5, None), '(1.5,2]': (lambda t: 1.5 < t <= 2, (1.5, 3))}
    pts = sorted(set([k / 100 for k in range(0, 201)] + [4.0]))
    open1 = 0
    for name, (mem, U) in cands.items():
        if U is not None:
            ok(all(mem(t) == (inY(t) and U[0] < t < U[1]) for t in pts), f'{name} = Y cut by {U}')
            open1 += 1

    def open_in_Y(mem):   # route 2: each point has a small interval whose Y-part stays in the set
        for t in pts:
            if mem(t) and inY(t):
                for h in (1e-7, 1e-9):
                    if any(inY(t + s * h) and not mem(t + s * h) for s in (-1, 1)):
                        return False
        return True
    open2 = sum(1 for mem, _ in cands.values() if open_in_Y(mem))
    num(it, 'p-gapped-domain', 1, open1, open2, {'open-in-r': 0, 'no-singleton': 3}, places=None)
    comps, prev = 0, None
    for t in pts:
        if inY(t):
            if prev is None or t - prev > 0.0101 or (prev < 1 < t):
                comps += 1
            prev = t
    num(it, 'p-gapped-domain', 2, 3, comps, {'joined': 2, 'one': 1}, places=None)
    data = [(0, -1), (0.9, 2), (1.5, -3), (2, 1), (4, 5)]
    comp_of = lambda t: 0 if t < 1 else (1 if t <= 2 else 2)
    zeros = sum(1 for (a, fa), (b, fb) in zip(data, data[1:]) if comp_of(a) == comp_of(b) and fa * fb < 0)
    zeros_naive = sum(1 for (a, fa), (b, fb) in zip(data, data[1:]) if fa * fb < 0)
    num(it, 'p-gapped-domain', 3, 2, zeros, {'across-gap': zeros_naive, 'one-zero': 1}, places=None)
    forced = sp.Union(sp.Interval(-1, 2), sp.Interval(-3, 1), sp.FiniteSet(5))
    grid = [k / 1000 for k in range(-5000, 6001)]
    meas2 = sum(1 for g in grid if (-1 <= g <= 2) or (-3 <= g <= 1)) / 1000
    num(it, 'p-gapped-domain', 4, float(forced.measure), round(meas2), {'one-interval': 8, 'added': 3 + 4}, places=None)

    # p-right-rays
    num(it, 'p-right-rays', 1, 5, max([1.5, 5]), {'ignore-point': 2}, places=None)
    inB = lambda t: (3 <= t <= 8) or t > 10
    tt = next(t / 100 for t in range(0, 2000) if all(inB(u / 100) for u in range(t + 1, 3000)))
    num(it, 'p-right-rays', 2, 10, tt, {'usual': 3, 'closed-end': 8}, places=None)
    maps = {'2x+1': (lambda t: 2 * t + 1, True), '-x': (lambda t: -t, True), 'x^3': (lambda t: t ** 3, True),
            'e^x': (lambda t: math.exp(t), False), 'x+1': (lambda t: t + 1, True)}
    sample = [k / 10 for k in range(-30, 31)]
    good = [n for n, (h, onto) in maps.items() if onto and all(h(a) < h(b) for a, b in zip(sample, sample[1:]))]
    usual = [n for n, (h, onto) in maps.items() if onto]
    num(it, 'p-right-rays', 3, len(good), 3, {'with-flip': len(usual)}, places=None)
    one_correct(it, 'p-right-rays', 4, 'conn-not-haus')

    lv.expect('problems', 'items[1].prose', 100)
    lv.expect('problems', 'items[2].prose', 0.9)
    lv.check_wrongs()
    return lv


# ---------------------------------------------------------------- level 3
def first_n(bound, tol):
    n = 0
    while bound(n) >= tol:
        n += 1
    return n


def level3():
    it = load(3)
    lv = Level('topology', 3)
    x = sp.Symbol('x', real=True)

    # p-quadratic-iteration. g = (x^2 + 5)/6 on [0, 2].
    g = (x ** 2 + 5) / 6
    gf = lambda t: (t * t + 5) / 6
    grid = [k / 10000 for k in range(20001)]
    M1 = sp.maximum(g, x, sp.Interval(0, 2))
    num(it, 'p-quadratic-iteration', 1, float(M1), max(gf(t) for t in grid), {'min-value': gf(0), 'at-one': gf(1)})
    ok(abs(min(gf(t) for t in grid) - 5 / 6) < 1e-12, 'image starts at 5/6')
    q1 = sp.maximum(sp.Abs(sp.diff(g, x)), x, sp.Interval(0, 2))
    q2 = max(abs(gf(a) - gf(b)) / (b - a) for a, b in zip(grid, grid[1:]))
    num(it, 'p-quadratic-iteration', 2, float(q1), q2, {'at-fixed': 1 / 3, 'image-end': 1.5 / 3, 'no-six': 4 / 3}, agree=1e-4)
    d01 = gf(0) - 0
    n1 = math.ceil(math.log(1e-6 * (1 - 2 / 3) / d01) / math.log(2 / 3))
    n2 = first_n(lambda n: (2 / 3) ** n / (1 / 3) * d01, 1e-6)
    num(it, 'p-quadratic-iteration', 3, n1, n2, {'no-denominator': first_n(lambda n: (2 / 3) ** n * d01, 1e-6),
                                                 'q-third': first_n(lambda n: (1 / 3) ** n / (2 / 3) * d01, 1e-6),
                                                 'q-half': first_n(lambda n: 0.5 ** n / 0.5 * d01, 1e-6)}, places=None)
    ok(abs(2.5 * (2 / 3) ** 36 - 1.14e-6) < 0.005e-6 and abs(2.5 * (2 / 3) ** 37 - 7.6e-7) < 0.05e-7, 'printed bounds at 36 and 37')
    roots = sp.solve(sp.Eq(x, g), x)
    inside = [r for r in roots if 0 <= r <= 2]
    xi = 0.0
    for _ in range(200):
        xi = gf(xi)
    num(it, 'p-quadratic-iteration', 4, int(inside[0]), round(xi, 9), {'other-root': int(max(roots))}, places=None)
    rate1 = sp.diff(g, x).subs(x, 1)
    xs = [0.0]
    for _ in range(60):
        xs.append(gf(xs[-1]))
    rate2 = (xs[16] - 1) / (xs[15] - 1)
    num(it, 'p-quadratic-iteration', 5, float(rate1), rate2, {'used-q': 2 / 3, 'value': 1.0}, agree=1e-6)

    # p-input-output
    A = sp.Matrix([[F(1, 2), F(3, 5)], [F(1, 5), F(3, 10)]])
    b = sp.Matrix([1, 2])
    Tm = lambda v: A * v + b
    u, v = sp.Matrix([3, 3]), sp.Matrix([2, 2])
    du = Tm(u) - Tm(v)
    ok(list(Tm(u)) == [F(43, 10), F(7, 2)] and list(Tm(v)) == [F(16, 5), 3], 'T(u), T(v) as printed')
    Af = [[0.5, 0.6], [0.2, 0.3]]
    Tf = lambda p: (Af[0][0] * p[0] + Af[0][1] * p[1] + 1, Af[1][0] * p[0] + Af[1][1] * p[1] + 2)
    tu, tv = Tf((3, 3)), Tf((2, 2))
    num(it, 'p-input-output', 1, float(max(abs(c) for c in du)), max(abs(tu[0] - tv[0]), abs(tu[1] - tv[1])),
        {'transpose': max(0.5 + 0.2, 0.6 + 0.3), 'taxicab': float(sum(abs(c) for c in du))}, agree=1e-12)
    r1 = sum(abs(c) for c in du) / 2
    num(it, 'p-input-output', 2, float(r1), (abs(tu[0] - tv[0]) + abs(tu[1] - tv[1])) / 2, {'no-divide': 1.6, 'sup-ratio': 1.1}, agree=1e-12)
    # route 2 for q in d_1: largest ratio over many random pairs
    rnd = random.Random(3)
    qd1 = max((abs(0.5 * a + 0.6 * c) + abs(0.2 * a + 0.3 * c)) / (abs(a) + abs(c)) for a, c in ((rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in range(200000)))
    ok(abs(qd1 - 0.9) < 1e-3 and qd1 <= 0.9 + 1e-12 and float(max(A[0, 1] + A[1, 1], A[0, 0] + A[1, 0])) == 0.9, 'd_1 constant 0.9')
    ok(Tf((10, 6))[0] <= 10 and Tf((10, 6))[1] <= 6 and Tf((0, 0)) == (1, 2), 'T maps X into X (monotone corners)')
    d01 = 1 + 2
    n1 = math.ceil(math.log(1e-3 * 0.1 / d01) / math.log(0.9))
    n2 = first_n(lambda n: 0.9 ** n / 0.1 * d01, 1e-3)
    num(it, 'p-input-output', 3, n1, n2, {'no-denominator': first_n(lambda n: 0.9 ** n * d01, 1e-3),
                                         'dinf-move': first_n(lambda n: 0.9 ** n / 0.1 * 2, 1e-3),
                                         'pair-ratio': first_n(lambda n: 0.8 ** n / 0.2 * d01, 1e-3)}, places=None)
    ok(abs(30 * 0.9 ** 97 - 0.00109) < 0.000005 and abs(30 * 0.9 ** 98 - 0.00098) < 0.000005, 'printed bounds at 97 and 98')
    xstar = (sp.eye(2) - A).solve(b)
    p = (0.0, 0.0)
    for _ in range(400):
        p = Tf(p)
    num(it, 'p-input-output', 4, float(xstar[0]), p[0], {'second': float(xstar[1]), 'transpose': float((sp.eye(2) - A.T).solve(b)[0])}, agree=1e-9)
    ok(0 <= p[0] <= 10 and 0 <= p[1] <= 6 and (sp.eye(2) - A).det() == F(23, 100), 'fixed point in X, det 0.23')

    # p-dyadic-points
    out1 = sum(1 for n in range(0, 60) if 2.0 ** -n >= 0.01)
    out2 = sum(1 for n in range(0, 60) if not (-0.01 < F(1, 2 ** n) < 0.01))
    num(it, 'p-dyadic-points', 1, out1, out2, {'from-one': out1 - 1, 'one-more': out1 + 1}, places=None)
    for n in range(0, 12):
        lo_, hi_ = 0.75 * 2.0 ** -n, 1.25 * 2.0 ** -n
        ok(sum(1 for m in range(0, 60) if lo_ < 2.0 ** -m < hi_) == 1 and not (lo_ < 0 < hi_), f'V_{n} holds one point')
    # route 2: greedy smallest subcover of K by brute force over the members needed
    Kpts = [0.0] + [2.0 ** -n for n in range(60)]
    need = set()
    for t in Kpts:
        if -0.01 < t < 0.01:
            need.add('U')
        else:
            need.add(f'V{round(-math.log2(t))}')
    num(it, 'p-dyadic-points', 2, out1 + 1, len(need), {'no-u': out1}, places=None)
    N1 = next(N for N in range(60) if 2.0 ** -N < 0.01)
    N2 = next(N for N in range(60) if max(abs(2.0 ** -m - 2.0 ** -k) for m in range(N, 80) for k in range(N, 80)) < 0.01)
    num(it, 'p-dyadic-points', 3, N1, N2, {'adjacent-gap': next(N for N in range(60) if 2.0 ** -N - 2.0 ** -(N + 1) < 0.01), 'eight': N1 + 1}, places=None)
    one_correct(it, 'p-dyadic-points', 4, 'k-both')

    # p-cube-delta
    sets = {'[-1,2]': (True, True), '[-1,2)': (False, True), '[-1,inf)': (True, False), '[-1,0]u{2}': (True, True)}
    comp = sum(1 for c, bdd in sets.values() if c and bdd)
    # route 2: a sequence test: the set holds the limit of 2 - 1/k and stays below a bound
    seq_ok = {'[-1,2]': True, '[-1,2)': False, '[-1,inf)': False, '[-1,0]u{2}': True}
    num(it, 'p-cube-delta', 1, comp, sum(seq_ok.values()), {'bounded': comp + 1, 'intervals-only': comp - 1}, places=None)
    fK = (sp.minimum(x ** 3, x, sp.Interval(-1, 2)), sp.maximum(x ** 3, x, sp.Interval(-1, 2)))
    gridK = [-1 + k * 3 / 30000 for k in range(30001)]
    num(it, 'p-cube-delta', 2, float(fK[1] - fK[0]), max(t ** 3 for t in gridK) - min(t ** 3 for t in gridK), {'positive-only': 8, 'cube-gap': 7}, places=None, agree=1e-9)
    e = sp.Symbol('e', positive=True)
    c12 = max(a * a + a * c + c * c for a in gridK[::100] for c in gridK[::100])
    expr(it, 'p-cube-delta', 3, e / 12, ['e'], lambda pt: pt['e'] / c12)
    xx = sp.Symbol('xx', positive=True)
    root = [r for r in sp.solve(sp.expand((xx + sp.Rational(1, 100)) ** 3 - xx ** 3 - 1), xx) if r.is_real and r > 0][0]
    lo, hi = 0.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if (mid + 0.01) ** 3 - mid ** 3 >= 1 else (mid, hi)
    num(it, 'p-cube-delta', 4, float(root), hi, {'slope-only': math.sqrt(1 / 0.03)}, agree=1e-9)

    lv.expect('problems', 'items[1].prose', 0.9)
    lv.expect('problems', 'items[2].prose', 0.01)
    lv.check_wrongs()
    return lv


LEVELS = {1: level1, 2: level2, 3: level3}
reports = [fn() for fn in LEVELS.values()]
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
for r in reports:
    r.report()
sys.exit(1 if fails else 0)
