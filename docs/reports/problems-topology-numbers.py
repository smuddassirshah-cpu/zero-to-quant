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


def num(items, iid, k, m1, m2, slips, places=4, agree=1e-9, shown=None):
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
    if shown is not None:   # an exact fraction: the TeX form is printed in both texts
        ok(shown in part['feedback']['correct'], f'{tag}: {shown} not printed in feedback.correct')
        ok(shown in part['explain']['text'], f'{tag}: {shown} not printed in explain')
        return
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

    # p-signal-bands (re-authored, session AH): tau = the usual open sets U of R with U = -U.
    # Sets are unions of pieces (lo, hi, closed-left, closed-right); a point is (a, a, True, True).
    INF = float('inf')
    def to_sp(pcs):
        out = sp.EmptySet
        for lo, hi, lc, rc in pcs:
            L = -sp.oo if lo == -INF else sp.nsimplify(lo)
            R = sp.oo if hi == INF else sp.nsimplify(hi)
            out = out | (sp.FiniteSet(L) if lo == hi else sp.Interval(L, R, not lc, not rc))
        return out
    def mem(pcs):
        return lambda t: any((lo < t < hi) or (lc and t == lo) or (rc and t == hi) for lo, hi, lc, rc in pcs)
    xs = sp.Symbol('x', real=True)
    def sp_open(S):          # route 1: open when it meets none of its boundary points
        return (S.boundary & S) == sp.EmptySet
    def sp_mirror(S):
        return sp.imageset(sp.Lambda(xs, -xs), S) == S
    GRID = [F(k, 64) for k in range(-6 * 64, 6 * 64 + 1)]
    def grid_open(m):        # route 2: every grid point inside has its neighbours a hair away inside too
        return all(m(float(t) - 1e-9) and m(float(t) + 1e-9) for t in GRID if m(float(t)))
    def grid_mirror(m):
        return all(m(float(t)) == m(float(-t)) for t in GRID)
    p1sets = {'(-2,2)': [(-2, 2, False, False)], '(0,3)': [(0, 3, False, False)],
              '(-3,-1)u(1,3)': [(-3, -1, False, False), (1, 3, False, False)],
              '[-1,1]': [(-1, 1, True, True)], '(-2,1)': [(-2, 1, False, False)]}
    in_tau1 = [n for n, pc in p1sets.items() if sp_open(to_sp(pc)) and sp_mirror(to_sp(pc))]
    in_tau2 = [n for n, pc in p1sets.items() if grid_open(mem(pc)) and grid_mirror(mem(pc))]
    ok(in_tau1 == in_tau2 == ['(-2,2)', '(-3,-1)u(1,3)'], f'signal p1: sets in tau {in_tau1} / {in_tau2}')
    usual1 = [n for n, pc in p1sets.items() if sp_open(to_sp(pc))]
    mirror1 = [n for n, pc in p1sets.items() if sp_mirror(to_sp(pc))]
    ok(usual1 == [n for n, pc in p1sets.items() if grid_open(mem(pc))], 'signal p1: usual-open sets by both routes')
    num(it, 'p-signal-bands', 1, len(in_tau1), len(in_tau2), {'usual': len(usual1), 'symmetric': len(mirror1)}, places=None)
    ok(mem(p1sets['(-2,1)'])(-1.5) and not mem(p1sets['(-2,1)'])(1.5) and mem(p1sets['(0,3)'])(1) and not mem(p1sets['(0,3)'])(-1),
       'signal p1: the witnesses -1.5 and 1 named in feedback')
    # tau is a topology: unions and intersections of symmetric open sets are symmetric open (spot check on the two members)
    A1, A2 = to_sp(p1sets['(-2,2)']), to_sp(p1sets['(-3,-1)u(1,3)'])
    ok(all(sp_open(S) and sp_mirror(S) for S in (A1 | A2, A1 & A2)), 'signal: union and meet of the two members lie in tau')
    # part 2: h into (R, tau) is continuous exactly when |h| is (U = {x : |x| in W}).
    sgn = lambda t: 1 if t >= 0 else -1
    maps = {'t': lambda t: t, 's': sgn, 'floor': math.floor, 't+s': lambda t: t + sgn(t), '2+s': lambda t: 2 + sgn(t)}
    size_cont = {'t': True, 's': True, 'floor': False, 't+s': True, '2+s': False}       # route 1, by hand: |h| = |t|, 1, jumps, 1+|t|, jumps
    usual_cont = {'t': True, 's': False, 'floor': False, 't+s': False, '2+s': False}
    TG = [k / 50 for k in range(-200, 201)]
    def preimage_open(h, a, b):   # route 2: h^{-1}({x : a < |x| < b}) open, tested at grid points by tiny steps
        m = lambda t: a < abs(h(t)) < b
        return all(m(t - 1e-9) and m(t + 1e-9) for t in TG if m(t))
    Ws = [(a / 4, b / 4) for a in range(-1, 16) for b in range(a + 1, 17)]
    cont2 = {n: all(preimage_open(h, a, b) for a, b in Ws) for n, h in maps.items()}
    ok(cont2 == size_cont, f'signal p2: continuity into tau by preimages {cont2}')
    jump = lambda h: any(abs(h(t + 1e-9) - h(t - 1e-9)) > 1e-6 for t in TG)
    ok({n: not jump(h) for n, h in maps.items()} == usual_cont, 'signal p2: usual continuity by sampling')
    ok({n: not jump(lambda t, h=h: abs(h(t))) for n, h in maps.items()} == size_cont, 'signal p2: |h| continuous by sampling')
    ok(all(abs(abs(t + sgn(t)) - (1 + abs(t))) < 1e-12 for t in TG), 'signal p2: |t + s(t)| = 1 + |t|')
    two_valued = dict(size_cont, **{'2+s': True})
    num(it, 'p-signal-bands', 2, sum(size_cont.values()), sum(cont2.values()),
        {'usual': sum(usual_cont.values()), 'two-valued': sum(two_valued.values())}, places=None)
    # part 3: A is connected in tau exactly when |A| is an interval or a point.
    p3sets = {'{-2,2}': [(-2, -2, True, True), (2, 2, True, True)], '{1,2}': [(1, 1, True, True), (2, 2, True, True)],
              '(-1,0)u(0,1)': [(-1, 0, False, False), (0, 1, False, False)],
              '[-3,-2]u[1,2]': [(-3, -2, True, True), (1, 2, True, True)],
              '[-4,-3]u[1,2]': [(-4, -3, True, True), (1, 2, True, True)], '[-1,2]': [(-1, 2, True, True)]}
    def sizes(S):
        return ((S | sp.imageset(sp.Lambda(xs, -xs), S)) & sp.Interval(0, sp.oo))
    def sp_conn(S):          # route 1: an interval or a single point
        return isinstance(S, sp.Interval) or (isinstance(S, sp.FiniteSet) and len(S) == 1)
    conn1 = {n: sp_conn(sizes(to_sp(pc))) for n, pc in p3sets.items()}
    CG = [k / 80 for k in range(0, 400)]   # cut levels, end points among them
    def split_by_level(pc, c, absolute=True):     # route 2: {|x| < c} and {|x| > c} (or x < c, x > c) split A
        m = mem(pc)
        pts = [k / 400 for k in range(-2400, 2401)]
        val = (lambda t: abs(t)) if absolute else (lambda t: t)
        inA = [t for t in pts if m(t)]
        return any(val(t) < c for t in inA) and any(val(t) > c for t in inA) and not any(abs(val(t) - c) < 1e-12 for t in inA)
    conn2 = {n: not any(split_by_level(pc, c) for c in CG) for n, pc in p3sets.items()}
    ok(conn1 == conn2, f'signal p3: connected sets by both routes {conn1} {conn2}')
    usual3 = {n: sp_conn(to_sp(pc)) for n, pc in p3sets.items()}
    usual3b = {n: not any(split_by_level(pc, c, absolute=False) for c in [k / 80 - 5 for k in range(800)]) for n, pc in p3sets.items()}
    ok(usual3 == usual3b, 'signal p3: usual connectedness by both routes')
    joined = dict(conn1, **{'[-4,-3]u[1,2]': True})
    num(it, 'p-signal-bands', 3, sum(conn1.values()), sum(conn2.values()),
        {'usual': sum(usual3.values()), 'joined': sum(joined.values())}, places=None)
    ok([str(sizes(to_sp(p3sets[n]))) for n in ('{-2,2}', '(-1,0)u(0,1)', '[-3,-2]u[1,2]', '[-1,2]')] ==
       ['{2}', 'Interval.open(0, 1)', 'Interval(1, 3)', 'Interval(0, 2)'], 'signal p3: the sizes named in explain')
    ok(split_by_level(p3sets['[-4,-3]u[1,2]'], 2.5) and not split_by_level(p3sets['{-2,2}'], 2.5), 'signal p3: the cut at 2.5 in the joined line')
    # part 4: |p| is continuous, so it takes 4; the two jump paths in the why lines are continuous into tau and miss 0 and 4.
    one_correct(it, 'p-signal-bands', 4, 'size-four')
    T4 = [k / 1000 for k in range(1001)]
    pA = lambda t: -3 - 2 * t if t < 0.5 else 3 + 2 * t
    pB = lambda t: -3 - 2 * t if t < 1 else 5
    for nm, pth in (('half-jump', pA), ('end-jump', pB)):
        ok(pth(0) == -3 and pth(1) == 5, f'signal p4: {nm} runs from -3 to 5')
        ok(all(abs(abs(pth(t)) - (3 + 2 * t)) < 1e-12 for t in T4), f'signal p4: {nm} has size 3 + 2t')
    ok(all(pA(t) != 0 for t in T4) and min(abs(pA(t)) for t in T4) >= 3, 'signal p4: the half-jump path never reads 0')
    ok(all(pB(t) < 0 for t in T4[:-1]) and pB(1) == 5, 'signal p4: the end-jump path never reads 4')
    ok(abs(pA(0.4999999) + 4) < 1e-5 and pA(0.5) == 4, 'signal p4: the path jumps from -4 to 4 at one half')
    tstar = (4 - 3) / 2
    ok(abs(abs(pA(tstar)) - 4) < 1e-12, 'signal p4: size 4 is reached at t = 1/2 on the jump path')

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
    # chain (fix pass): part 2's B uses 2c with c = part 1's key, part 3 uses c and k = part 2's key, part 4 uses c
    c1 = 5
    ok(2 * c1 == tt, 'right-rays: 2c from part 1 is the left end of part 2')
    k2 = int(tt)
    maps = {'x+c': (lambda t: t + c1, True), 'c-x': (lambda t: c1 - t, True), 'x^3': (lambda t: t ** 3, True),
            'e^x': (lambda t: math.exp(t), False), 'x-k': (lambda t: t - k2, True)}
    sample = [k / 10 for k in range(-30, 31)]
    good = [n for n, (h, onto) in maps.items() if onto and all(h(a) < h(b) for a, b in zip(sample, sample[1:]))]
    usual = [n for n, (h, onto) in maps.items() if onto]
    num(it, 'p-right-rays', 3, len(good), 3, {'with-flip': len(usual)}, places=None)
    qs = [p_['question'] for p_ in it['p-right-rays']['parts']]
    ok('from part 1' in qs[1] and '2c' in qs[1], 'right-rays part 2 cites part 1 and uses c')
    ok('$c$ from part 1' in qs[2] and '$k$ from part 2' in qs[2] and '$x - k$' in qs[2], 'right-rays part 3 cites parts 1 and 2')
    ok('from part 1' in qs[3] and '(-\\infty, c]' in qs[3], 'right-rays part 4 cites part 1')
    # part 4 subspace (-inf, 5]: open sets are the whole set and (t, 5]; two non-empty open sets always meet (route 2: grid)
    opens = [(t_ / 2, 5.0) for t_ in range(-20, 10)]
    ok(all(max(a[0], b[0]) < 5.0 for a in opens for b in opens), 'right-rays part 4: any two non-empty open sets of (-inf, 5] meet')
    one_correct(it, 'p-right-rays', 4, 'conn-not-haus')

    lv.expect('problems', 'items[1].parts[3].question', 5)
    lv.expect('problems', 'items[1].parts[3].question', -3)
    lv.expect('problems', 'items[1].parts[2].feedback.byKey.joined', 2.5)
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

    # p-kernel-equation. T(f)(x) = 1 + (x/2) int_0^1 t f(t) dt on (C[0, 1], d_inf).
    t_, c_ = sp.symbols('t c')
    q1 = sp.Rational(1, 2) * sp.integrate(t_, (t_, 0, 1))
    # route 2: the constant gap f - g = 1 attains the bound; midpoint rule for the integral, x = 1
    nmid = 4000
    integ = lambda fn: sum(fn((k + 0.5) / nmid) for k in range(nmid)) / nmid
    q2 = 0.5 * integ(lambda s: s * 1.0)
    num(it, 'p-kernel-equation', 1, float(q1), q2, {'no-t': 0.5 * integ(lambda s: 1.0), 'x-averaged': float(q1) / 2}, places=4, agree=1e-8, shown=r'\tfrac14')
    c1 = sp.solve(sp.Eq(c_, sp.Rational(1, 2) * sp.integrate(t_ * (1 + c_ * t_), (t_, 0, 1))), c_)[0]
    cc = 0.0
    for _ in range(80):                         # route 2: iterate T on the coefficient of x
        cc = 0.5 * integ(lambda s: s * (1 + cc * s))
    num(it, 'p-kernel-equation', 2, float(c1), cc, {'one-step': 0.25,
                                                   'no-t': float(sp.solve(sp.Eq(c_, sp.Rational(1, 2) * sp.integrate(1 + c_ * t_, (t_, 0, 1))), c_)[0]),
                                                   'no-square': float(sp.solve(sp.Eq(c_, sp.Rational(1, 2) * (sp.Rational(1, 2) + c_ / 2)), c_)[0])},
        places=4, agree=1e-8, shown=r'\tfrac{3}{10}')
    xg = [k / 1000 for k in range(1001)]
    e1 = sp.Abs(c1 - sp.Rational(1, 4))
    e2 = max(abs((1 + cc * xv) - (1 + xv / 4)) for xv in xg)
    num(it, 'p-kernel-equation', 3, float(e1), e2, {'at-half': float(e1) / 2, 'added': 0.25 + float(c1)}, places=4, agree=1e-8, shown=r'\tfrac{1}{20}')
    ok(abs(1 + 0.5 * integ(lambda s: s * 1.0) - 1.25) < 1e-9, 'kernel: f_1 = 1 + x/4')
    bound = q1 / (1 - q1) * sp.Rational(1, 4)
    r1 = bound / e1
    r2 = (q2 / (1 - q2) * max(abs(xv / 4) for xv in xg)) / e2
    num(it, 'p-kernel-equation', 4, float(r1), r2, {'no-denominator': float(q1 * sp.Rational(1, 4) / e1), 'inverted': float(1 / r1),
                                                   'over-one-minus': float(sp.Rational(1, 4) / (1 - q1) / e1)}, places=4, agree=1e-6, shown=r'\tfrac53')
    ok(bound == sp.Rational(1, 12) and e1 < bound, 'kernel: the bound 1/12 holds over the true error 1/20')
    lv.expect('problems', 'items[0].parts[2].explain.text', 0.05)
    lv.expect('problems', 'items[0].parts[1].explain.text', 0.3)

    # p-trapping-interval. T(x) = 0.2 e^x on B_r = [-r, r].
    r_ = sp.Symbol('r', positive=True)
    qexpr = 0.2 * sp.exp(r_)
    qsym = sp.maximum(sp.diff(sp.Rational(1, 5) * sp.exp(x), x), x, sp.Interval(-1, 1))   # the max of T' on [-1, 1] sits at 1
    ok(sp.simplify(qsym - sp.Rational(1, 5) * sp.E) == 0, 'trap: |T\'| largest at the right end')
    part = it['p-trapping-interval']['parts'][0]
    wq = part['widget']
    forms = {'0.2e^{r}': lambda rv: 0.2 * math.exp(rv), '\\frac{e^{r}}{5}': lambda rv: math.exp(rv) / 5,
             '\\frac{1}{5}e^{r}': lambda rv: math.exp(rv) / 5, '0.2e^r': lambda rv: 0.2 * math.exp(rv), 'e^r/5': lambda rv: math.exp(rv) / 5,
             '0.2e^{-r}': lambda rv: 0.2 * math.exp(-rv), '0.2': lambda rv: 0.2, 'e^{r}': lambda rv: math.exp(rv)}
    def ratio_sup(rv):                          # route 2: largest |T(x) - T(y)| / |x - y| over a grid of B_r
        pts = [-rv + 2 * rv * k / 400 for k in range(401)]
        return max(abs(0.2 * math.exp(a) - 0.2 * math.exp(b)) / (b - a) for a, b in zip(pts, pts[1:]))
    for rv in (0.3, 0.8, 1.4):
        ok(0 < float(qexpr.subs(r_, rv)) - ratio_sup(rv) < 5e-3 * ratio_sup(rv), f'trap: q at r = {rv} is the sup of the grid ratios, never reached')
        for tex in [wq['answer']] + wq['accept']:
            ok(abs(forms[tex](rv) - float(qexpr.subs(r_, rv))) < 1e-12, f'trap p1: form {tex}')
        for wr in wq['wrong']:
            ok(abs(forms[wr['tex']](rv) - float(qexpr.subs(r_, rv))) > 1e-3, f'trap p1: wrong {wr["id"]} equals the key')
    ok(all(wr['id'] in part['feedback']['byKey'] for wr in wq['wrong']), 'trap p1: byKey lines')
    one_correct(it, 'p-trapping-interval', 2, 'triangle')
    ok(abs(0.5 * 1 + 5 - 5.5) < 1e-12 and abs(0.5 * -1 + 5 - 4.5) < 1e-12, 'trap p2: x/2 + 5 sends [-1, 1] to [4.5, 5.5]')
    hfun = lambda rv: rv - 0.2 * rv * math.exp(rv) - 0.2
    rs1 = float(sp.nsolve(r_ - 0.2 * r_ * sp.exp(r_) - 0.2, r_, 0.27))
    lo, hi = 0.2, 0.5                           # route 2: bisection, and a scan for the first sign change
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if hfun(mid) < 0 else (lo, mid)
    first = next(k / 100000 for k in range(1, 200000) if hfun(k / 100000) >= 0)
    ok(abs(first - lo) < 2e-5, 'trap p3: the first sign change is the bisection root')
    num(it, 'p-trapping-interval', 3, rs1, lo, {'no-q': 0.2, 'q-at-zero': 0.2 / 0.8}, agree=1e-9)
    ok(hfun(0.27) < 0 and abs(hfun(0.27) + 0.0007) < 0.00005 and hfun(0.272) > 0, 'trap p3: printed trial values')
    ok(abs(0.2 * math.exp(0.2711) - 0.2623) < 5e-5 and abs((1 - 0.2 * math.exp(rs1)) * rs1 - 0.2) < 1e-9, 'trap p3: printed q and room')
    ok(abs(0.2 * math.exp(rs1) - 0.26) < 0.005, 'trap p3: q about 0.26')
    ok(hfun(0.2712) > 0 and hfun(0.2711) < 0 and (1 - 0.2 * math.exp(0.2712)) * 0.2712 >= 0.2, 'trap p4: part 2 condition holds at 0.2712, fails at 0.2711')
    xs_ = [0.0]
    for _ in range(80):
        xs_.append(0.2 * math.exp(xs_[-1]))
    xstar = -float(sp.LambertW(-sp.Rational(1, 5)))
    num(it, 'p-trapping-interval', 4, xstar, xs_[-1], {'one-step': 0.2, 'radius': round(rs1, 4)}, agree=1e-12)
    ok([round(v, 4) for v in xs_[1:5]] == [0.2, 0.2443, 0.2553, 0.2582], 'trap p4: printed iterates')
    ok(xstar <= rs1 and abs(xs_[12] - xstar) < 5e-5, 'trap p4: x* in B_r; a dozen steps fix 4 places')

    # p-coin-paths. Paths in {u, d}^N, d = 2^-k at the first difference, V = sum x_k 2^-k.
    kmin = next(k for k in range(1, 30) if F(1, 2 ** k) < F(1, 10))
    # route 2: brute force over 6-day prefixes: classes of the relation d < 0.1
    pre6 = [''.join(p_) for p_ in itertools.product('ud', repeat=6)]
    dist = lambda a, b: next((F(1, 2 ** (i + 1)) for i in range(6) if a[i] != b[i]), F(0))
    classes = {frozenset(b for b in pre6 if dist(a, b) < F(1, 10)) for a in pre6}
    num(it, 'p-coin-paths', 1, 2 ** (kmin - 1), len(classes), {'four-days': 2 ** kmin, 'two-days': 2 ** (kmin - 2)}, places=None)
    Vf = lambda s: sum(F(1, 2 ** (i + 1)) for i, ch in enumerate(s) if ch == 'u')
    gap1 = F(1, 16) + sum(F(1, 2 ** k) for k in range(5, 200))           # finite sum, tail 2^-199
    gap_exact = F(1, 16) + F(1, 16)
    best = max(abs(Vf(a + 'u' + t1) - Vf(a + 'd' + t2)) for a in (''.join(p_) for p_ in itertools.product('ud', repeat=3)) for t1 in ('u' * 40, 'd' * 40) for t2 in ('u' * 40, 'd' * 40))
    num(it, 'p-coin-paths', 2, float(gap_exact), float(gap1), {'day-only': 1 / 16, 'day-three': 2 * F(1, 8)}, places=4, agree=1e-12, shown=r'\tfrac18')
    ok(abs(float(best) - 1 / 8) < 1e-9, 'coin p2: brute force over prefixes and long tails')
    ok(all(abs(Vf(a) - Vf(b)) <= 2 * dist(a, b) + F(1, 2 ** 6) for a in pre6 for b in pre6), 'coin p2: |V - V\'| <= 2d on 6-day prefixes')
    # p3: paths with V = 5/8, by the two binary forms; route 2: long prefixes within 2^-30 of 5/8
    two = [s for s in ('udu' + 'd' * 40, 'udd' + 'u' * 40) if abs(Vf(s) - F(5, 8)) < F(1, 2 ** 40)]
    near = {s[:6] for s in (''.join(p_) for p_ in itertools.product('ud', repeat=12)) if abs(Vf(s) - F(5, 8)) <= F(1, 2 ** 12)}
    num(it, 'p-coin-paths', 3, len(two), len(near), {'one-path': 1}, places=None)
    vn = [sum(F(1, 2 ** (2 * j - 1)) for j in range(1, n + 1)) for n in range(1, 40)]
    lim1 = sp.Rational(1, 2) / (1 - sp.Rational(1, 4))
    num(it, 'p-coin-paths', 4, float(lim1), float(vn[-1]), {'down-first': float(sp.Rational(1, 4) / (1 - sp.Rational(1, 4))), 'first-day': 0.5, 'all-days': 1.0},
        places=4, agree=1e-9, shown=r'\tfrac23')
    om = lambda n: 'ud' * n + 'd' * 10
    ok(all(dist(om(m)[:6], om(n)[:6]) == (F(1, 2 ** (2 * min(m, n) + 1)) if 2 * min(m, n) < 6 else 0) for m in range(1, 4) for n in range(1, 4) if m != n),
       'coin p4: omega_m, omega_n agree on 2 min(m, n) days')
    lv.expect('problems', 'items[2].parts[0].question', 0.1)
    lv.expect('problems', 'items[1].parts[3].question', 0.2711)

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
    dl = sp.Rational(1, 12)
    cub = sp.expand((xx + dl) ** 3 - xx ** 3)
    ok(cub == xx ** 2 / 4 + xx / 48 + sp.Rational(1, 1728), 'cube p4: the printed expansion')
    root = [r for r in sp.solve(cub - 1, xx) if r.is_real and r > 0][0]
    lo, hi = 0.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if (mid + 1 / 12) ** 3 - mid ** 3 >= 1 else (mid, hi)
    num(it, 'p-cube-delta', 4, float(root), hi, {'slope-only': math.sqrt(1 / (3 / 12))}, agree=1e-9)
    ok(abs(float(root) + 1 / 12 - 2.0415) < 5e-5 and float(root) + 1 / 12 > 2, 'cube p4: the pair reaches past the end of K')
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
