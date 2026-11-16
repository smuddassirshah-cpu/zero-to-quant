"""Second reader's recomputation of convex problems-1 to problems-3.

Imports nothing from the author's script. Every function, matrix and programme is typed from the
problem's prose. Route 1 is a closed form in exact fractions or sympy; route 2 is a solver, a grid
or an enumeration (scipy linprog on the full programme, SLSQP, brentq, every lattice point,
a finite difference of the optimal value).
Exit 0 always on a clean run of the script; a failing check prints a FINDING line (CI rule,
session AE). Claims found false or unsafe by reading are also printed as FINDING lines.
Run: <venv>/bin/python docs/reports/problems-convex-numbers-read.py
"""
import itertools
import json
import math
import os
import re
import sys
import warnings
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy.optimize import brentq, linprog, minimize, minimize_scalar

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'convex')
SETS = {n: json.load(open(os.path.join(CDIR, f'problems-{n}.json'))) for n in (1, 2, 3)}
checks = 0
findings = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        findings.append(msg)


def claim(msg):
    findings.append(msg)


def item(n, iid):
    return next(i for i in SETS[n]['items'] if i['id'] == iid)


def band(w):
    t = w.get('tol', {})
    a = w['answer'] if 'answer' in w else w['value']
    return a - t.get('abs', 0), a + t.get('abs', 0)


def inb(x, b):
    return b[0] - 1e-12 <= x <= b[1] + 1e-12


def strict_in(x, b):
    """As the engine tests it: |x - centre| <= tol in doubles, no slack."""
    c = (b[0] + b[1]) / 2
    return abs(x - c) <= (b[1] - b[0]) / 2


def num(n, iid, part, mine, mine2, slips, dp=None, printed=()):
    """mine, mine2: the key by two routes. slips: {id: value rebuilt from the slip}.
    dp: places the part asks for. printed: values the feedback prints that the key must take."""
    p = item(n, iid)['parts'][part - 1]
    w = p['widget']
    tag = f'problems-{n} {iid} p{part}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    kb = band(w)
    ok(abs(mine - mine2) <= 1e-6 * max(1, abs(mine)), f'{tag}: my two routes differ {mine} {mine2}')
    ok(abs(w['answer'] - mine) <= 2e-6 * max(1, abs(mine)), f'{tag}: key {w["answer"]} against mine {mine}')
    if dp is not None:
        for r in (math.floor(mine * 10 ** dp + 0.5) / 10 ** dp, round(mine, dp)):
            ok(strict_in(r, kb), f'{tag}: key band refuses the {dp}-place rounding {r}')
    for v in printed:
        ok(strict_in(v, kb), f'{tag}: key band refuses the printed value {v}')
    wr = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wr) == set(slips), f'{tag}: slip ids {sorted(wr)} against mine {sorted(slips)}')
    bk = p['feedback'].get('byKey', {})
    for sid, val in slips.items():
        if sid not in wr:
            continue
        ok(abs(wr[sid]['value'] - val) <= 2e-6 * max(1, abs(val)), f'{tag}: slip {sid} {wr[sid]["value"]} against mine {val}')
        sb = band(wr[sid])
        ok(sb[1] < kb[0] or sb[0] > kb[1], f'{tag}: slip {sid} band meets the key band')
        ok(sid in bk, f'{tag}: slip {sid} has no feedback line')
        if dp is not None:
            ups = math.floor(abs(val) * 10 ** dp + 0.5) / 10 ** dp * (1 if val >= 0 else -1)
            for r in (ups, round(val, dp)):
                ok(strict_in(r, sb), f'{tag}: slip {sid} band refuses its own {dp}-place rounding {r} (value {wr[sid]["value"]}, tol {wr[sid].get("tol")})')
        for oid, o in wr.items():
            if oid != sid:
                ob = band(o)
                ok(sb[1] < ob[0] or sb[0] > ob[1], f'{tag}: slip bands {sid} and {oid} meet')
    # the part states a form
    q = p['question']
    ok(bool(re.search(r'Give |whole number|decimal|places|nearest', q)), f'{tag}: the question states no form for its number')


def choice(n, iid, part, right):
    w = item(n, iid)['parts'][part - 1]['widget']
    tag = f'problems-{n} {iid} p{part}'
    c = [o['id'] for o in w['options'] if o.get('correct')]
    ok(c == [right], f'{tag}: keyed option {c} against mine {right}')
    for o in w['options']:
        if not o.get('correct'):
            ok(bool(o.get('why')), f'{tag}: option {o["id"]} has no why')


def expr(n, iid, part, mine, syms, slips):
    """Expression parts: the key, every accept form and every wrong form, compared symbolically."""
    from sympy.parsing.latex import parse_latex  # noqa: F401  (not used: forms are simple enough to read)
    w = item(n, iid)['parts'][part - 1]['widget']
    tag = f'problems-{n} {iid} p{part}'

    def rd(s):
        s = s.replace('\\lambda', 'L').replace('\\frac{L}{2}', '(L/2)').replace('\\frac{10-L}{2}', '((10-L)/2)')
        s = s.replace('^', '**').replace(' ', '')
        s = re.sub(r'(\d)([A-Za-z(])', r'\1*\2', s)
        return sp.sympify(s, locals=syms)
    ok(sp.simplify(rd(w['answer']) - mine) == 0, f'{tag}: key {w["answer"]} against mine {mine}')
    for a in w.get('accept', []):
        ok(sp.simplify(rd(a) - mine) == 0, f'{tag}: accept form {a} is not the key')
    wr = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(wr) == set(slips), f'{tag}: slip ids {sorted(wr)} against mine {sorted(slips)}')
    for sid, val in slips.items():
        if sid in wr:
            ok(sp.simplify(rd(wr[sid]) - val) == 0, f'{tag}: slip {sid} {wr[sid]} against mine {val}')
            ok(sp.simplify(val - mine) != 0, f'{tag}: slip {sid} equals the key')


def says(n, iid, part, field, text):
    p = item(n, iid)['parts'][part - 1]
    blob = json.dumps(p, ensure_ascii=False) if field == '*' else json.dumps(p.get(field), ensure_ascii=False)
    ok(text in blob, f'problems-{n} {iid} p{part}: text not found: {text}')


# ------------------------------------------------------------------ set 1
# p-shortfall-and-fee: C(x) = 2(x-3)^2 + 5|x|
def C(x):
    return 2 * (x - 3) ** 2 + 5 * abs(x)


gap = F(1, 2) * C(F(-1)) + F(1, 2) * C(F(3)) - C(F(1, 2) * -1 + F(1, 2) * 3)
gap2 = np.mean([C(-1.0), C(3.0)]) - C(1.0)
wrongC = lambda x: 2 * (x - 3) ** 2 + 5 * x          # |x| read as x
num(1, 'p-shortfall-and-fee', 1, float(gap), gap2,
    {'abs-dropped': 0.5 * wrongC(-1) + 0.5 * wrongC(3) - wrongC(1), 'reversed': -float(gap)}, dp=0)
ok(C(-1) == 37 and C(3) == 15 and C(1) == 13, 'p-shortfall p1: C(-1), C(3), C(1) are not 37, 15, 13')
choice(1, 'p-shortfall-and-fee', 2, 'sum')
# convexity on a grid of chords, and no second derivative at 0
g = np.linspace(-4, 6, 81)
ok(all(0.5 * C(a) + 0.5 * C(b) - C((a + b) / 2) >= -1e-12 for a in g for b in g), 'p-shortfall p2: a midpoint chord fails')
h = 1e-6
ok(abs((C(h) - C(0)) / h - (C(0) - C(-h)) / h) > 9, 'p-shortfall p2: no kink at 0')
# a dent from two convex pieces (the "pieces" why): min(x^2, (x-2)^2) pieces glued at 1
ok(0.5 * 0.25 + 0.5 * 0.25 < 1.0, 'pieces why: no dent example')
x = sp.symbols('x', positive=True)
st = sp.solve(sp.diff(2 * (x - 3) ** 2 + 5 * x, x), x)[0]
st2 = minimize_scalar(C, bounds=(-10, 10), method='bounded', options={'xatol': 1e-10}).x
num(1, 'p-shortfall-and-fee', 3, float(st), st2,
    {'no-fee': 3.0, 'fee-sign': float(sp.solve(4 * (x - 3) - 5, x)[0]), 'no-chain': float(sp.solve(2 * (x - 3) + 5, x)[0])},
    printed=(1.75,))
num(1, 'p-shortfall-and-fee', 4, float(C(F(7, 4))), min(C(v) for v in np.linspace(-5, 8, 130001)),
    {'half': (1.75 - 3) ** 2 + 5 * 1.75, 'no-fee': 2 * (1.75 - 3) ** 2}, dp=3)
ok(C(0) == 18 and C(3) == 15, 'p-shortfall p4: C(0), C(3)')
capmin = min(C(v) for v in np.linspace(-5, 1.2, 62001))
num(1, 'p-shortfall-and-fee', 5, float(C(F(6, 5))), capmin,
    {'unconstrained': 11.875, 'at-zero': C(0), 'fee-dropped': 2 * (1.2 - 3) ** 2}, dp=2)
ok(abs(4 * (1.2 - 3) + 5 - (-2.2)) < 1e-12, "p-shortfall p5: C'(1.2) is not -2.2")
ok(abs(C(1.2) - C(1.75) - 0.605) < 1e-12, 'p-shortfall p5: the limit does not cost 0.605')
ok(all(4 * (v - 3) + 5 < 0 for v in np.linspace(1e-9, 1.2, 100)) and all(4 * (v - 3) - 5 < 0 for v in np.linspace(-5, -1e-9, 100)),
   "p-shortfall p5: C' is not negative below 1.2")

# p-worst-scenario: removed in the session AF fix pass. The problem was re-authored as p-account-target
# (review finding 4); its checks here, and FINDING lines 1, 2 and 7, went with it. The delta reader checks the new problem.

# p-two-futures-hedge: covariance of (P, F1, F2)
S3 = np.array([[6, 1, 1], [1, 1, 3], [1, 3, 10.0]])
ok(np.linalg.eigvalsh(S3).min() > 0, 'p-two-futures prose: the covariance matrix of (P, F1, F2) is not positive definite')


def Vq(a, b_, sign=-1):
    v = np.array([1, sign * a, sign * b_])
    return v @ S3 @ v


def Vp(a, b_):
    return a * a + 6 * a * b_ + 10 * b_ * b_ - 2 * a - 2 * b_ + 6


ok(all(abs(Vq(a, b_) - Vp(a, b_)) < 1e-9 for a in (-2, 0, 1.5, 7) for b_ in (-2, 0, 3)), 'p-two-futures prose: V is not Var(P - aF1 - bF2)')
a, b_ = sp.symbols('a b')
Vs = a ** 2 + 6 * a * b_ + 10 * b_ ** 2 - 2 * a - 2 * b_ + 6
H = sp.hessian(Vs, (a, b_))
Hn = np.array(H, dtype=float)
ev = np.linalg.eigvalsh(Hn)
num(1, 'p-two-futures-hedge', 1, float(H.det()), float(np.prod(ev)), {'half-cross': 2 * 20 - 3 ** 2, 'no-two': 1 * 10 - 3 ** 2}, dp=0)
choice(1, 'p-two-futures-hedge', 2, 'strict')
ok(abs(ev.sum() - 22) < 1e-9 and abs(ev[0] - 0.18) < 0.005 and abs(ev[1] - 21.82) < 0.005, 'p-two-futures p2: eigenvalues 0.18 and 21.82, sum 22')
ok(2 * 20 - 7 ** 2 == -9, 'p-two-futures p2: 7ab determinant')
sol = sp.solve([sp.diff(Vs, a), sp.diff(Vs, b_)], (a, b_))
sol2 = np.linalg.solve(Hn, [2, 2])
bs = sp.symbols('bs')
slip_b = 2  # the sign slip the line names: b = +2, then a = 1 - 3b
num(1, 'p-two-futures-hedge', 3, float(sol[a]), sol2[0], {'gave-b': float(sol[b_]), 'sign': 1 - 3 * slip_b}, dp=0)
num(1, 'p-two-futures-hedge', 4, float(Vs.subs(sol)), Vq(7, -2), {'unhedged': Vp(0, 0), 'no-constant': Vp(7, -2) - 6}, dp=0)
rb = minimize(lambda v: Vp(v[0], v[1]), [0.0, 1.0], bounds=[(None, None), (0, None)], method='L-BFGS-B')
num(1, 'p-two-futures-hedge', 5, float(sp.Min(*[Vs.subs({a: 1, b_: 0})])), rb.fun, {'free': 1.0, 'clip': Vp(7, 0)}, dp=0)
ok(abs(rb.x[0] - 1) < 1e-4 and abs(rb.x[1]) < 1e-6 and 6 * 1 + 20 * 0 - 2 == 4, 'p-two-futures p5: edge optimum (1, 0), V_b = 4')
# FINDING (misleading): which way the hedge trades
best = np.array([1, -7, 2.0])  # P - 7 F1 + 2 F2: the position the minimiser describes
ok(abs(best @ S3 @ best - 1) < 1e-9, 'p-two-futures: P - 7F1 + 2F2 does not have variance 1')
held = np.array([1, 7, -2.0])  # holding 7 of F1 and selling 2 of F2, as the text words it
hedge_text = json.dumps(item(1, 'p-two-futures-hedge'), ensure_ascii=False)
if abs(held @ S3 @ held - 1) > 1e-9 and ('may not sell' in hedge_text or 'needs a sale' in hedge_text):
    claim(f'problems-1 p-two-futures-hedge prose, p3, p4, p5: V is Var(P - aF1 - bF2), so a = 7 is 7 contracts SOLD and b = -2 is 2 BOUGHT. '
          f'The text says the hedge "holds" a, "needs a sale of 2 contracts of F2" and "may not sell F2, so b >= 0". '
          f'Holding 7 and selling 2 gives variance {held @ S3 @ held:.0f}, not 1; the ban b >= 0 forbids buying F2.')

# ------------------------------------------------------------------ set 2
# p-parking-cash: full programme in (d, b, n)
c3 = [-40, -46, -50]
full = linprog(c3, A_ub=[[-1, 0, 0], [0, 0.5, 1]], b_ub=[-6, 8], A_eq=[[1, 1, 1]], b_eq=[20], method='highs')
B, N = sp.symbols('b n')
inc = sp.expand(40 * (20 - B - N) + 46 * B + 50 * N)
expr(2, 'p-parking-cash', 1, inc, {'b': B, 'n': N}, {'no-800': 6 * B + 10 * N, 'no-subtract': 800 + 46 * B + 50 * N})
corners = {(0, 0): 0, (14, 0): 84, (12, 2): 92, (0, 8): 80}
for (bb, nn), add in corners.items():
    ok(bb + nn <= 14 and 0.5 * bb + nn <= 8 and 6 * bb + 10 * nn == add, f'p-parking p2: corner {(bb, nn)} or its gain {add}')
num(2, 'p-parking-cash', 2, float(sp.solve([B + N - 14, B / 2 + N - 8], (B, N))[B]), full.x[1], {'notes': full.x[2], 'all-bills': 14.0}, dp=0)
run = linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1]], b_ub=[14, 8])
num(2, 'p-parking-cash', 3, -(6 * 12 + 10 * 2), run.fun, {'sign': -run.fun, 'with-800': run.fun - 800, 'income': 800 - run.fun}, dp=0)
ok(abs(-full.fun - 892) < 1e-7, 'p-parking p3: the income is not 892')
fl = linprog(c3, A_ub=[[-1, 0, 0], [0, 0.5, 1], [0, 0, -1]], b_ub=[-6, 8, -5], A_eq=[[1, 1, 1]], b_eq=[20], method='highs')
num(2, 'p-parking-cash', 4, 800 + 6 * 6 + 10 * 5, -fl.fun, {'old-plan': 892, 'notes-corner': 800 + 80, 'no-800': 86}, dp=0)
ok(np.allclose(fl.x, [9, 6, 5]), 'p-parking p4: the plan is not (6, 5)')
mx = linprog([0, 0, -1], A_ub=[[-1, 0, 0], [0, 0.5, 1]], b_ub=[-6, 8], A_eq=[[1, 1, 1]], b_eq=[20], method='highs')


def floor_status(f):
    return linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1], [0, -1]], b_ub=[14, 8, -f]).status


num(2, 'p-parking-cash', 5, 8.0, -mx.fun, {'overnight-only': 14.0, 'whole-pot': 20.0, 'current': 5.0}, dp=0)
ok(floor_status(8) == 0 and floor_status(8.01) == 2 and floor_status(5) == 0, 'p-parking p5: status at floors 5, 8 and 8.01')
at8 = linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1], [0, -1]], b_ub=[14, 8, -8])
ok(np.allclose(at8.x, [0, 8]) and 800 - at8.fun == 880, 'p-parking p5: plan (0, 8) earning 880 at a floor of 8')

# p-whole-blocks
lp = linprog([-6, -5], A_ub=[[4, 3], [1, 3]], b_ub=[19, 8], method='highs')
xs = F(11, 3)
ys = (8 - xs) / 3
num(2, 'p-whole-blocks', 1, float(6 * xs + 5 * ys), -lp.fun, {'capital-corner': 6 * 4.75, 'risk-corner': 5 * 8 / 3}, dp=2, printed=(29.22,))
ok(ys == F(13, 9) and 6 * xs + 5 * ys == F(263, 9), 'p-whole-blocks p1: corner (11/3, 13/9), carry 263/9')
lattice = {(i, j): 6 * i + 5 * j for i in range(6) for j in range(4) if 4 * i + 3 * j <= 19 and i + 3 * j <= 8}
rd = (math.floor(xs), math.floor(ys))
num(2, 'p-whole-blocks', 2, 6 * rd[0] + 5 * rd[1], lattice[(3, 1)], {'capital-plan': 6 * math.floor(4.75)}, dp=0)
num(2, 'p-whole-blocks', 3, math.floor(F(263, 9)), math.floor(-lp.fun + 1e-9), {'round-up': math.ceil(F(263, 9)), 'rounded-plan': 23}, dp=0)
bestl = max(lattice, key=lattice.get)
num(2, 'p-whole-blocks', 4, 4, bestl[0], {'rounded': 3, 'two-each': 2}, dp=0)
ok(lattice[bestl] == 29 and sum(v == 29 for v in lattice.values()) == 1 and lattice[(4, 0)] == 24 and lattice[(2, 2)] == 22,
   'p-whole-blocks p4: (4, 1) is not the one plan at 29, or the listed carries')
ok(4 * 4 + 3 * 1 == 19 and 4 + 3 == 7 and 4 * 3 + 3 == 15 and 3 + 3 == 6, 'p-whole-blocks: capital and risk used by (4, 1) and (3, 1)')

# p-three-strategies
cP = [6, 7, 4]
AP = np.array([[3, 1, 2], [2, 3, 1.0]])
pr = linprog([-v for v in cP], A_ub=AP, b_ub=[10, 10], method='highs')
du = linprog([10, 10], A_ub=-AP.T, b_ub=[-v for v in cP], method='highs')
u, v = sp.symbols('u v')
expr(2, 'p-three-strategies', 1, u + 3 * v, {'u': u, 'v': v}, {'momentum': 3 * u + 2 * v, 'swapped': 3 * u + v})
# dual corners by enumeration of row pairs (rows and axes)
rows = [(3, 2, 6), (1, 3, 7), (2, 1, 4), (1, 0, 0), (0, 1, 0)]
dcorners = set()
allpts = {}
for r1, r2 in itertools.combinations(rows, 2):
    M = np.array([r1[:2], r2[:2]], dtype=float)
    if abs(np.linalg.det(M)) < 1e-12:
        continue
    pt = np.linalg.solve(M, [r1[2], r2[2]])
    feas = all(rr[0] * pt[0] + rr[1] * pt[1] >= rr[2] - 1e-9 for rr in rows)
    allpts[tuple(np.round(pt, 6))] = feas
    if feas:
        dcorners.add(tuple(np.round(pt, 6)))
ok(dcorners == {(0, 4), (1, 2), (7, 0)}, f'p-three p2: dual corners {dcorners}')
unchecked = np.linalg.solve([[3, 2], [1, 3]], [6, 7])
ok(np.allclose(unchecked, [4 / 7, 15 / 7]) and abs(2 * unchecked[0] + unchecked[1] - 23 / 7) < 1e-12, 'p-three p2: the unchecked point')
num(2, 'p-three-strategies', 2, min(10 * p[0] + 10 * p[1] for p in dcorners), du.fun,
    {'corner-04': 40.0, 'corner-70': 70.0, 'unchecked': 10 * unchecked.sum()}, dp=0)
choice(2, 'p-three-strategies', 3, 'momentum')
ok(3 * 1 + 2 * 2 == 7 > 6 and 1 + 3 * 2 == 7 and 2 * 1 + 2 == 4, 'p-three p3: dual rows at (1, 2)')
x23 = np.linalg.solve([[1, 2], [3, 1]], [10, 10])
num(2, 'p-three-strategies', 4, x23[0], pr.x[1], {'value': pr.x[2], 'var-only': 10 / 3}, dp=0)
ok(abs(pr.x[0]) < 1e-9 and abs(-pr.fun - 30) < 1e-9 and abs(du.fun - 30) < 1e-9, 'p-three p4: x1 = 0 and both values 30')


def x1_at(c1):
    return linprog([-c1, -7, -4], A_ub=AP, b_ub=[10, 10], method='highs').x[0]


thr = brentq(lambda c1: (x1_at(c1) > 1e-9) - 0.5, 6, 9, xtol=1e-9)
num(2, 'p-three-strategies', 5, 3 * 1 + 2 * 2, round(thr, 6), {'current': 6.0, 'margin-only': 3.0, 'gap': 1.0}, dp=0)
ok(x1_at(6.99) < 1e-9 and x1_at(7.01) > 1e-6, 'p-three p5: momentum does not enter just above 7')
ok(-1 > -2 and -1 < -1 / 3, 'p-three p2: slopes')

# ------------------------------------------------------------------ set 3
# p-capital-price
lam, x1, x2 = sp.symbols('L x1 x2')
P1 = 10 * x1 - x1 ** 2
P2 = 8 * x2 - x2 ** 2 / 2
c1 = sp.solve(sp.diff(P1 - lam * x1, x1), x1)[0]
c2 = sp.solve(sp.diff(P2 - lam * x2, x2), x2)[0]
expr(3, 'p-capital-price', 1, c1, {'L': lam}, {'no-half': 10 - lam, 'sign': 5 + lam / 2})
ok(sp.simplify(c2 - (8 - lam)) == 0, 'p-capital p1: the credit desk does not pick 8 - lambda')
gsym = sp.simplify((P1 + P2 - lam * (x1 + x2 - 6)).subs({x1: c1, x2: c2}))


def g_num(l):
    r_ = minimize(lambda z: -(10 * z[0] - z[0] ** 2 + 8 * z[1] - z[1] ** 2 / 2 - l * (z[0] + z[1] - 6)), [1, 1], method='BFGS')
    return -r_.fun


asks = float((P1 + P2).subs({x1: c1, x2: c2}).subs(lam, 3))
num(3, 'p-capital-price', 2, float(gsym.subs(lam, 3)), g_num(3.0), {'no-rent': asks - 3 * 8.5, 'ask-profit': asks}, dp=2)
ok(sp.simplify(sp.diff(gsym, lam) - (6 - c1 - c2)) == 0, "p-capital p3: g' is not 6 - x1 - x2")
ls = sp.solve(sp.diff(gsym, lam), lam)[0]
ls2 = minimize_scalar(g_num, bounds=(0, 10), method='bounded', options={'xatol': 1e-9}).x
num(3, 'p-capital-price', 3, float(ls), round(ls2, 5), {'no-half': float(sp.solve(6 - (10 - lam) - (8 - lam), lam)[0]), 'trial': 3.0}, dp=2)


def best_profit(cap):
    r_ = minimize(lambda z: -(10 * z[0] - z[0] ** 2 + 8 * z[1] - z[1] ** 2 / 2), [1, 1], method='SLSQP',
                  constraints=[{'type': 'ineq', 'fun': lambda z: cap - z[0] - z[1]}], options={'ftol': 1e-14})
    return -r_.fun, r_.x


p6, x6 = best_profit(6.0)
num(3, 'p-capital-price', 4, float((P1 + P2).subs({x1: c1, x2: c2}).subs(lam, ls)), round(p6, 6),
    {'trial-cap': float(gsym.subs(lam, 3)), 'no-limit': float((P1 + P2).subs({x1: 5, x2: 8}))}, dp=2)
ok(np.allclose(x6, [8 / 3, 10 / 3], atol=1e-5) and abs(float(gsym.subs(lam, ls)) - p6) < 1e-6, 'p-capital p4: split (8/3, 10/3), zero gap')
p63, _ = best_profit(6.3)
est = F(122, 3) + F(3, 10) * F(14, 3)
num(3, 'p-capital-price', 5, float(est), p6 + 0.3 * (best_profit(6.0 + 1e-4)[0] - best_profit(6.0 - 1e-4)[0]) / 2e-4,
    {'trial-price': float(F(122, 3) + F(3, 10) * 3), 'per-desk': float(F(122, 3) + 2 * F(3, 10) * F(14, 3))}, dp=2, printed=(42.07,))
ok(abs(p63 - 42.04) < 0.005 and abs((13 - 6.3) / 1.5 - 4.47) < 0.005 and p63 < float(est), 'p-capital p5: re-solve 42.04 at price 4.47, below the estimate')

# p-no-borrowing: removed in the session AF fix pass. The problem was re-authored as p-style-fit
# (main-session ruling, review findings 16, 17, 20); its checks here, and FINDING line 4, went with it.

# p-variance-limit
w = sp.symbols('w')
Sv = sp.Matrix([[F(1, 100), F(5, 1000)], [F(5, 1000), F(625, 10000)]])  # gilts, equities
wt = sp.Matrix([1 - w, w])
Vw = sp.expand((wt.T * Sv * wt)[0])
expr(3, 'p-variance-limit', 1, Vw, {'w': w},
     {'no-cov': sp.expand(F(1, 100) * (1 - w) ** 2 + F(625, 10000) * w ** 2), 'single-cov': sp.expand(F(1, 100) * (1 - w) ** 2 + F(5, 1000) * w * (1 - w) + F(625, 10000) * w ** 2)})
Vf = sp.lambdify(w, Vw)
roots = sorted(sp.solve(Vw - F(16, 1000), w))
top = brentq(lambda t: Vf(t) - 0.016, 0.08, 1)
num(3, 'p-variance-limit', 2, float(roots[1]), top, {'other-root': float(roots[0]), 'min-var': float(sp.solve(sp.diff(Vw, w), w)[0]), 'no-limit': 1.0}, printed=(0.4,))
ok(abs(Vf(1.0) - 0.0625) < 1e-12 and abs(0.04 + 0.06 * 0.4 - 0.064) < 1e-12, 'p-variance p2: all-equity variance, return 6.4%')


def wstar(limit):
    return brentq(lambda t: Vf(t) - limit, 0.08, 1, xtol=1e-14)


mu = 0.06 / float(sp.diff(Vw, w).subs(w, F(2, 5)))
hh = 1e-7
mu_fd = (0.06 * wstar(0.016 + hh) - 0.06 * wstar(0.016 - hh)) / (2 * hh)
num(3, 'p-variance-limit', 3, mu, round(mu_fd, 5), {'inverted': 0.04 / 0.06, 'half-derivative': 0.06 / (0.0625 * 0.4 - 0.01)}, dp=2)
choice(3, 'p-variance-limit', 4, 'convex')
ok(Vf(0.0) < 0.016 and sp.diff(Vw, w, 2) > 0, 'p-variance p4: Slater point w = 0, V convex')
rise = 1e4 * 0.06 * (wstar(0.0162) - 0.4)
num(3, 'p-variance-limit', 5, round(1e4 * mu * 0.0002), round(rise), {'inverted': round(1e4 * 0.0002 / mu), 'variance-step': 2.0}, dp=0)
ok(abs(rise - 2.98) < 0.005 and abs(wstar(0.0162) - 0.405) < 0.0005, f'p-variance p5: exact rise {rise}')

# ------------------------------------------------------------------ structure
for n in (1, 2, 3):
    for it in SETS[n]['items']:
        ok(3 <= len(it['parts']) <= 5 and 3 <= it['difficulty'] <= 5, f'problems-{n} {it["id"]}: parts or difficulty out of range')
        for k, p in enumerate(it['parts'][1:], start=2):
            ok(bool(re.search(r'[Pp]art \d|[Pp]arts \d|[Uu]sing', p['question'])), f'problems-{n} {it["id"]} p{k}: the question does not point back to an earlier part')
    ok(any(it['difficulty'] == 5 for it in SETS[n]['items']), f'problems-{n}: no difficulty 5')
    parts = [p for it in SETS[n]['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(3 * typed >= 2 * len(parts), f'problems-{n}: typed parts {typed} of {len(parts)}')

for f in findings:
    print('FINDING', f)
print(f'problems-convex-numbers-read: {checks} checks, {len(findings)} FINDING line(s)')
sys.exit(0)
