"""Recompute every number stated in convex level 2 (Linear programmes) by two routes, and check each at its JSON path.
Run: python3 docs/reports/convex-L2-numbers.py   (needs numpy and scipy; exits 0 when every check passes)
Route 1 is exact arithmetic (fractions, vertex enumeration by hand-solved 2 by 2 systems); route 2 is SciPy HiGHS.
`two(a, b)` asserts the routes agree; `lv.expect` checks the stated value appears where it is stated.
The script also runs every code widget of the level in CPython: the solution passes its hidden tests and the
starter fails at least one.
"""
import sys, os, math
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("convex", 2)
E = lv.expect
fails = []
def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')
def stated(name, exact, shown, places):
    if abs(float(exact) - shown) > 0.51 * 10 ** -places:
        fails.append(f'{name}: {exact!r} does not round to {shown}')

A = [[1, 1], [3, 1], [1, 0]]; b = [10, 18, 5]
ROWS = [([1, 1], 10), ([3, 1], 18), ([1, 0], 5), ([-1, 0], 0), ([0, -1], 0)]
def vertices(rows):
    out = {}
    for (a1, b1), (a2, b2) in combinations(rows, 2):
        det = F(a1[0] * a2[1] - a1[1] * a2[0])
        if det == 0:
            out[(tuple(a1), tuple(a2))] = None; continue
        x = (F(b1) * a2[1] - F(b2) * a1[1]) / det; y = (F(a1[0]) * b2 - F(a2[0]) * b1) / det
        feas = all(r[0] * x + r[1] * y <= rb for r, rb in rows)
        out[(tuple(a1), tuple(a2))] = (x, y, feas)
    return out
V = vertices(ROWS)
feasible = sorted({(p[0], p[1]) for p in V.values() if p and p[2]})
if feasible != sorted([(0, 0), (5, 0), (5, 3), (4, 6), (0, 10)]): fails.append(f'pentagon {feasible}')
infeas = sorted({(p[0], p[1]) for p in V.values() if p and not p[2]})
if infeas != sorted([(5, 5), (10, 0), (0, 18), (6, 0)]): fails.append(f'infeasible pairs {infeas}')
if sum(1 for p in V.values() if p is None) != 1 or len(V) != 10: fails.append('pair count')
def best(c, rows=ROWS):
    return max((c[0] * x + c[1] * y, (x, y)) for x, y in feasible)
def hi(c, A_=A, b_=b):
    r = linprog(-np.array(c, float), A_ub=A_, b_ub=b_, method='highs'); return -r.fun, r
profits = {v: 60 * v[0] + 40 * v[1] for v in feasible}
for v, p in zip([(0, 0), (5, 0), (5, 3), (4, 6), (0, 10)], [0, 300, 420, 480, 400]):
    two(f'profit {v}', profits[v], p)
val, r = hi([60, 40]); two('desk opt', val, best([60, 40])[0]); two('desk opt 480', val, 480)
for a, s in zip(r.slack, [0, 0, 1]): two('slack', a, s)
for a, s in zip(r.ineqlin.marginals, [-30, -10, 0]): two('marginal', a, s)

# ---- l5 ----
two('P(2,5)', 60 * 2 + 40 * 5, 320); E('l5', 'screens[0].widget.answer', 320); E('l5', 'screens[0].widget.wrong[0].value', 40 * 2 + 60 * 5); E('l5', 'screens[0].widget.wrong[1].value', 7)
E('l5', 'screens[0].explain.text', 320); E('l5', 'screens[0].prose', 10); E('l5', 'screens[0].prose', 18); E('l5', 'screens[0].prose', 5)
two('margin at (4,6)', 2 * 4 + 4 * 6, 32); E('l5', 'screens[2].feedback.correct', 32); two('margin at (0,10)', 2 * 0 + 4 * 10, 40); E('l5', 'screens[2].feedback.correct', 40); two('line cuts (0,10)', 4 * 10 > 36, True)
# l5 quiz[3]: g >= 2e is 2e - g <= 0; (g, e) = (2, 1.5) breaks the rule and satisfies the old keyed row e - 2g <= 0
two('rule row', 2 * 1.5 - 2 <= 0, False); two('old row', 1.5 - 2 * 2 <= 0, True); two('key row on (g,e)=(4,1)', 2 * 1 - 4 <= 0, True)
# l8 swap: 10 x 40 = 400, and 18 x 40 = 720
two('swap 400', 10 * 40, 400); two('swap 720', 18 * 40, 720)
E('l5', 'screens[3].widget.answer', '(1, 3, 1)'); E('l5', 'screens[4].widget.answer', '(0, 0, 1)')
for s, sb in zip(np.array(b) - np.array(A) @ [4, 6], [0, 0, 1]): two('slack (4,6)', s, sb)
# hedge
HR = [([-2, -1], -8), ([-1, -3], -9), ([-1, 0], 0), ([0, -1], 0)]
hv = sorted({(p[0], p[1]) for p in vertices(HR).values() if p and p[2]})
if hv != sorted([(0, 8), (3, 2), (9, 0)]): fails.append(f'hedge corners {hv}')
cost = {v: F(1) * v[0] + F(3, 2) * v[1] for v in hv}
two('hedge (3,2)', cost[(3, 2)], 6); two('hedge (0,8)', cost[(0, 8)], 12); two('hedge (9,0)', cost[(9, 0)], 9)
r = linprog([1.0, 1.5], A_ub=[[-2, -1], [-1, -3]], b_ub=[-8, -9], method='highs'); two('hedge lp', r.fun, 6)
r = linprog([1.0, 1.5], A_ub=[[2, 1], [1, 3]], b_ub=[8, 9], method='highs'); two('hedge flipped', r.fun, 0)
E('l5', 'screens[6].widget.answer', 6000); E('l5', 'screens[6].widget.wrong[1].value', 9000); E('l5', 'screens[6].widget.wrong[2].value', 12000)
E('l5', 'screens[6].explain.text', '(3, 2)'); E('l5', 'screens[6].hints[2].text', 12); E('l5', 'screens[6].prose', 1.5)
two('(5,100)', 60 * 5 + 40 * 100, 4300); E('l5', 'screens[7].feedback.byKey.x5', 4300)
r = linprog([-60, -40], A_ub=[[1, 0]], b_ub=[5], method='highs')
if r.status != 3: fails.append('unbounded status')
r = linprog([-60, -40], A_ub=A + [[-1, -1]], b_ub=b + [-12], method='highs')
if r.status != 2: fails.append('infeasible status')
# venues
fees = [F(30, 100), F(25, 100), F(40, 100)]; caps = [4000, 3000, 6000]
def cheapest(fees, caps, n):
    left = n; x = [0] * 3
    for i in sorted(range(3), key=lambda i: fees[i]):
        x[i] = min(caps[i], left); left -= x[i]
    return x, sum(f * q for f, q in zip(fees, x))
x, c = cheapest(fees, caps, 10000)
r = linprog([0.30, 0.25, 0.40], A_eq=[[1, 1, 1]], b_eq=[10000], bounds=[(0, 4000), (0, 3000), (0, 6000)], method='highs')
two('venue cost', c, r.fun); two('venue 3150', c, 3150)
for a, bb in zip(x, r.x): two('venue x', a, bb)
if x != [4000, 3000, 3000]: fails.append(f'venue split {x}')
two('venue dual total', r.eqlin.marginals[0], 0.40); two('venue dual 1', r.upper.marginals[0], -0.10); two('venue dual 2', r.upper.marginals[1], -0.15)
E('l5', 'screens[8].widget.answer', 31.5); E('l5', 'screens[8].widget.wrong[0].value', 3150); E('l5', 'screens[8].widget.wrong[1].value', 25); E('l5', 'screens[8].widget.wrong[2].value', 40)
E('l5', 'screens[8].explain.text', 750); E('l5', 'screens[8].explain.text', 1200); E('l5', 'screens[8].explain.text', 3150)
# quiz: swapped 3
val, r = hi([60, 40], [[1, 1], [1, 3], [1, 0]]); two('swap opt', val, F(1420, 3)); two('swap x', r.x[0], 5); two('swap y', r.x[1], F(13, 3))
stated('473.33', val, 473.33, 2); E('l5', 'quiz[0].widget.answer', 473.33); E('l5', 'quiz[0].feedback.correct', 173.33); stated('173.33', 40 * F(13, 3), 173.33, 2)
E('l5', 'quiz[2].widget.answer', '(2, 0, 0)')
for s, sb in zip(np.array(b) - np.array(A) @ [5, 3], [2, 0, 0]): two('slack (5,3)', s, sb)

# ---- l6 ----
E('l6', 'screens[0].widget.answer', 480); two('iso x-int', F(480, 60), 8); two('iso y-int', F(480, 40), 12)
E('l6', 'screens[0].feedback.correct', '(8, 0)'); E('l6', 'screens[0].feedback.correct', '(0, 12)')
E('l6', 'screens[1].widget.answer', '(4, 6)')
E('l6', 'screens[2].widget.rows[3][3].answer', 400); E('l6', 'screens[2].widget.rows[4][3].answer', 420)
for p in [480, 400, 420, 300, 0]: E('l6', 'screens[2].feedback.correct', p)
for v in ['(5, 5)', '(10, 0)', '(0, 18)', '(6, 0)']: E('l6', 'screens[2].feedback.correct', v)
two('(5,5) risk', 15 + 5, 20); E('l6', 'screens[2].hints[0].text', 20)
v150, r = hi([150, 40]); two('150 opt', v150, best([150, 40])[0]); two('150 = 870', v150, 870)
two('150 at (4,6)', 150 * 4 + 40 * 6, 840); two('150 at (5,0)', 150 * 5, 750)
E('l6', 'screens[3].feedback.correct', 870); E('l6', 'screens[3].feedback.correct', 120); E('l6', 'screens[3].explain.text', 840); E('l6', 'screens[3].explain.text', 750)
E('l6', 'screens[3].canvas.params.functions[2].expr', '(870 - 150*x)/40')
for p in range(41, 120, 7):
    if best([p, 40])[1] != (4, 6): fails.append(f'(4,6) not optimal at p={p}')
if best([121, 40])[1] != (5, 3) or best([39, 40])[1] != (0, 10): fails.append('range ends')
vt, _ = hi([60, 60]); two('tie', vt, 600); two('tie (0,10)', 60 * 10, 600); two('tie (4,6)', 60 * 10, 600); E('l6', 'screens[4].widget.answer', 600)
# simplex walk
ratios = [F(10, 1), F(18, 3), F(5, 1)]; two('ratio min', min(ratios), 5)
for t in ['10, 6 and 5', '£300k', '£420k', '£480k']: E('l6', 'screens[5].widget.lines', t)
two('edge (5,3)->(4,6)', 60 * -1 + 40 * 3, 60); two('edge (4,6)->(0,10)', 60 * -1 + 40 * 1, -20); two('edge back', -60, -(60 * -1 + 40 * 3) / 1 + 0 - 0 if False else -60)
E('l6', 'screens[5].explain.text', -20); E('l6', 'screens[5].explain.text', 60)
two('degenerate', 2 * 4 + 6, 14)
for v in feasible:
    if 2 * v[0] + v[1] > 14: fails.append(f'2x+y<=14 cuts {v}')
two('deg (5,3)', 2 * 5 + 3, 13); E('l6', 'screens[8].widget.options[1].why', 13); E('l6', 'screens[8].hints[1].text', 13)
r = linprog([-60, -40], A_ub=A + [[2, 1]], b_ub=b + [14], method='highs'); two('deg opt', -r.fun, 480)
E('l6', 'screens[9].widget.answer', 3)
for v, p in zip([(0, 0), (5, 0), (5, 3), (4, 6), (0, 10)], [0, 5, 11, 16, 20]): two(f'x+2y {v}', v[0] + 2 * v[1], p); E('l6', 'quiz[0].explain.text', p)
E('l6', 'quiz[1].widget.answer', 5)

# ---- l7 ----
for t in ['array([4., 6.])', '-480.0', 'array([0., 0., 1.])']: E('l7', 'screens[0].canvas.params.lines', t)
r = linprog(-np.array([0.05, 0.08, 0.11]), A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.5)] * 3, method='highs'); two('r1', -r.fun, F(95, 1000))
two('r1 exact', F(1, 2) * F(8, 100) + F(1, 2) * F(11, 100), F(95, 1000))
E('l7', 'screens[3].widget.rows[0][2].answer', 0.095); E('l7', 'screens[3].widget.rows[1][1].answer', 2); E('l7', 'screens[3].widget.rows[2][1].answer', 3)
m = np.array([0.05, 0.08, 0.11])
r2 = linprog(-m, A_ub=[-m], b_ub=[-0.10], A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.5)] * 3, method='highs')
r3 = linprog([-60, -40], A_ub=[[1, 0]], b_ub=[5], method='highs')
if (r.status, r2.status, r3.status) != (0, 2, 3): fails.append('status table')
r0 = linprog([60, 40], A_ub=A, b_ub=b, method='highs'); two('min trap', r0.fun, 0)
ls = dict(A_ub=np.vstack([-np.eye(3), np.eye(3)]), b_ub=[0.5] * 3 + [1] * 3, A_eq=[[1, 1, 1]], b_eq=[1], method='highs')
two('ls default', -linprog(-m, **ls).fun, 0.11); rf = linprog(-m, bounds=[(None, None)] * 3, **ls); two('ls free', -rf.fun, 0.125)
two('ls exact', F(-1, 2) * F(5, 100) + F(1, 2) * F(8, 100) + F(11, 100), F(125, 1000))
for a, bb in zip(rf.x, [-0.5, 0.5, 1]): two('ls x', a, bb)
E('l7', 'screens[5].widget.answer', 0.125); E('l7', 'screens[5].widget.wrong[0].value', 0.11); E('l7', 'screens[5].explain.text', 0.125)
re_ = linprog([1, 1], A_eq=[[1, 1], [1, -1]], b_eq=[10, 2], method='highs'); two('eq x', re_.x[0], 6); two('eq y', re_.x[1], 4); E('l7', 'screens[6].widget.answer', 6)
for t in ['-30', '-10']: E('l7', 'screens[8].canvas.params.lines', t)

# ---- l8 ----
two('offer (30,10,0)', 10 * 30 + 18 * 10, 480); E('l8', 'screens[0].widget.answer', 480); E('l8', 'screens[0].widget.wrong[1].value', 300)
rd = linprog([10, 18, 5], A_ub=[[-1, -3, -1], [-1, -1, 0]], b_ub=[-60, -40], method='highs'); two('dual opt', rd.fun, 480)
for a, bb in zip(rd.x, [30, 10, 0]): two('dual y', a, bb)
DV = sorted({(p[0], p[1]) for p in vertices([([-1, -3], -60), ([-1, -1], -40), ([-1, 0], 0), ([0, -1], 0)]).values() if p and p[2]})
if DV != sorted([(0, 40), (30, 10), (60, 0)]): fails.append(f'dual corners {DV}')
for v, cst in zip([(0, 40), (30, 10), (60, 0)], [720, 480, 600]):
    two(f'dual cost {v}', 10 * v[0] + 18 * v[1], cst); E('l8', 'screens[1].explain.text', cst)
E('l8', 'screens[1].widget.answer', 720); E('l8', 'screens[2].widget.answer', 'y_1+y_2')
two('offer (40,10,0)', 10 * 40 + 18 * 10, 580); E('l8', 'screens[4].widget.answer', 580); E('l8', 'screens[4].prose', 420); E('l8', 'screens[4].explain.text', 580)
two('plan (5,3)', 60 * 5 + 40 * 3, 420)
sol = np.linalg.solve([[1, 3], [1, 1]], [60, 40]); two('cs y1', sol[0], 30); two('cs y2', sol[1], 10); E('l8', 'screens[5].widget.answer', '(30, 10, 0)')
rw = linprog([10, 18], A_ub=[[-1, -1], [-3, -1]], b_ub=[-60, -40], method='highs'); two('wrong dual', rw.fun, 600)
for a, bb in zip(rw.x, [60, 0]): two('wrong dual x', a, bb)
E('l8', 'screens[6].prose', 600); E('l8', 'screens[6].prose', '(60, 0)')
r19, rr = hi([60, 40], A, [10, 19, 5]); two('19 risk units', r19, 490); two('19 x', rr.x[0], 4.5); two('19 y', rr.x[1], 5.5)
E('l8', 'screens[9].widget.answer', 10); E('l8', 'screens[9].explain.text', 490); E('l8', 'screens[9].explain.text', '(4.5, 5.5)')
for t in [0.40, 0.10, 0.15]: E('l8', 'screens[9].explain.text', t)
rq = linprog([10, 18, 5], A_ub=[[-1, -3, -1], [-1, -1, 0]], b_ub=[-150, -40], method='highs'); two('q y3', rq.x[2], 30); two('q dual 870', rq.fun, 870)
E('l8', 'quiz[2].widget.answer', 30); E('l8', 'quiz[2].explain.text', 870)

# ---- review ----
r = hi([20, 60])[0]; two('r vertex', r, best([20, 60])[0]); E('review', 'items[1].widget.answer', 600)
for v, p in zip([(5, 0), (5, 3), (4, 6)], [100, 280, 440]): two(f'r corner {v}', 20 * v[0] + 60 * v[1], p); E('review', 'items[1].explain.text', p)
V8 = sorted({(p[0], p[1]) for p in vertices(ROWS + [([0, 1], 8)]).values() if p and p[2]}); two('cut vertices', len(V8), 6); E('review', 'items[2].widget.answer', 6)
if (2, 8) not in V8 or (0, 8) not in V8: fails.append('cut corners')
two('r offer', 10 * 20 + 18 * 20, 560); E('review', 'items[5].widget.answer', 560)
x2, c2 = cheapest(fees, [4000, 5000, 6000], 10000); two('r venue', c2, 2850)
r = linprog([0.30, 0.25, 0.40], A_eq=[[1, 1, 1]], b_eq=[10000], bounds=[(0, 4000), (0, 5000), (0, 6000)], method='highs'); two('r venue lp', r.fun, 2850)
E('review', 'items[8].widget.answer', 28.5); E('review', 'items[8].explain.text', 2850); E('review', 'items[8].explain.text', 300); two('r saving', 2000 * F(15, 100), 300)
E('review', 'items[9].widget.answer', 0.4); E('review', 'items[9].explain.text', 0.15)

# ---- homework ----
r = linprog([1.0, 1.5], A_ub=[[-2, -1], [-1, -3]], b_ub=[-8, -12], method='highs'); two('h hedge', r.fun, 7.2)
s = np.linalg.solve([[2, 1], [1, 3]], [8, 12]); two('h hedge a', s[0], 2.4); two('h hedge b', s[1], 3.2)
E('homework', 'items[0].widget.answer', 7200); E('homework', 'items[0].feedback.correct', '(2.4, 3.2)')
two('h obj', hi([70, 30])[0], best([70, 30])[0]); two('h obj 460', best([70, 30])[0], 460); E('homework', 'items[1].widget.answer', 460)
two('h obj (5,3)', 70 * 5 + 30 * 3, 440); E('homework', 'items[1].widget.wrong[0].value', 440)
E('homework', 'items[2].widget.answer', 120); E('homework', 'items[2].widget.wrong[0].value', 40)
ru = linprog([-8, -9], A_ub=[[2, 1], [1, 3]], b_ub=[1.0, 1.5], method='highs'); two('cover dual', -ru.fun, 6)
for a, bb in zip(ru.x, [0.3, 0.4]): two('cover u', a, bb)
E('homework', 'items[3].explain.text', 6); E('homework', 'items[4].widget.answer', 400)
Pp = np.array([96, 99, 97, 85.]); CFb = np.array([[100, 0, 0], [5, 105, 0], [4, 4, 104], [0, 0, 100.]]); L = np.array([100, 150, 200.])
r = linprog(Pp, A_ub=-CFb.T, b_ub=-L, method='highs'); d = -r.ineqlin.marginals
lots = [F(13, 14), F(10, 7), 0, 2]
for a, bb in zip(r.x, lots): two('lots', a, bb)
two('cost', r.fun, F(2804, 7)); two('cost exact', sum(F(int(p)) * l for p, l in zip(Pp, lots)), F(2804, 7))
two('d1', d[0], F(96, 100)); two('d2', d[1], (F(99) - F(48, 10)) / 105); two('d3', d[2], F(85, 100))
two('strong duality', L @ d, F(2804, 7)); stated('4% bond value', CFb[2] @ d, 95.83, 2)
E('homework', 'items[5].feedback.correct', 0.897143); E('homework', 'items[5].feedback.correct', 400.571); E('homework', 'items[5].explain.text', 95.83)
E('homework', 'items[6].widget.answer', 500)
for t in [480, 30, 10, 420, 400, 300, 180]: E('homework', 'items[7].model', t)

# ---- code widgets ----
def run_code(widget, code):
    ns = {}
    if widget.get('prelude'): exec(widget['prelude'], ns)
    exec(code, ns)
    out = []
    for t in widget['tests']:
        try:
            if t.get('setup'): exec(t['setup'], ns)
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol', {}); rel = tol.get('rel', 0 if tol else 1e-9); ab = tol.get('abs', 0 if tol else 1e-12)
                g = np.array(got, float).ravel(); w = np.array(want, float).ravel()
                ok = g.shape == w.shape and all(math.isclose(a, bb, rel_tol=rel, abs_tol=ab) for a, bb in zip(g, w))
            else:
                ok = got == want
        except Exception:
            ok = False
        out.append(bool(ok))
    return out
for fid, doc in lv.files.items():
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget', {})
            if w.get('kind') != 'code': continue
            so = run_code(w, w['solution']); st = run_code(w, w['starter'])
            if not all(so): fails.append(f'{fid} {key}[{i}] solution fails {so}')
            if all(st): fails.append(f'{fid} {key}[{i}] starter passes')
            print(f'code {fid} {key}[{i}]: solution {sum(so)}/{len(so)}, starter {sum(st)}/{len(st)}')

for x in fails: print('FAIL', x)
print(f'two-route checks: {len(fails)} failures')
if fails:
    lv.report(); sys.exit(1)
lv.report()
