"""Delta read of the two holes fix passes: every changed graded answer, band and wrong value recomputed by the reader,
by two routes each, and compared with the files as they stand. Also searches each re-authored item for numbers of its
old version. A check that fails because the content is wrong stays failing and is a finding (marked FINDING).

<scratchpad>/venv/bin/python docs/reviews/review-delta-holes-scripts/recompute.py      (from the repo root)"""
import json
import math
import re
from fractions import Fraction as F
from itertools import combinations_with_replacement, product

import sympy as sp

C = 'app/content/'
checks = fails = 0
finds = []


def load(p):
    return json.load(open(C + p + '.json'))


def item(doc, iid):
    return next(i for i in doc['items'] if i['id'] == iid)


def ok(cond, msg, finding=False):
    global checks, fails
    checks += 1
    if not cond:
        if finding:
            finds.append(msg)
            print('FINDING', msg)
        else:
            fails += 1
            print('FAIL   ', msg)


def near(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


def wrongs(w):
    return {x['id']: x for x in w.get('wrong', [])}


def key(w, want, band=None, name=''):
    """the stored answer is my value (within 1e-4 or to the places stored); the band takes my value"""
    a, tol = float(w['answer']), w.get('tol', {}).get('abs', 0)
    ok(abs(float(want) - a) <= tol + 1e-12, f'{name}: key {a} takes my value {float(want):.6g} (band {tol})')
    if band is not None:
        ok(near(tol, band), f'{name}: band is {band} (file {tol})')


def wr(w, wid, want, name='', dp=None):
    x = wrongs(w).get(wid)
    ok(x is not None, f'{name}: wrong entry {wid} exists')
    if x is None:
        return
    v, tol = float(x['value']), (x.get('tol') or {}).get('abs', 1e-9)
    ok(abs(float(want) - v) <= tol + 1e-12, f'{name}: wrong {wid} {v} takes my value {float(want):.6g} (band {tol})')
    a, at = float(w['answer']), w.get('tol', {}).get('abs', 0)
    ok(abs(v - a) > at + tol, f'{name}: wrong {wid} band is clear of the answer band')


def text_of(o):
    if isinstance(o, str):
        return o
    if isinstance(o, dict):
        return '\n'.join(text_of(v) for v in o.values())
    if isinstance(o, list):
        return '\n'.join(text_of(v) for v in o)
    return str(o)


def stale(it, pats, name):
    t = text_of({k: v for k, v in it.items() if k != 'id'})   # the item id is kept by rule
    for p in pats:
        m = re.search(p, t)
        ok(m is None, f'{name}: old-version text /{p}/ is still in the item' + (f': "...{t[max(0, m.start() - 50):m.end() + 30]}..."'.replace('\n', ' ') if m else ''), finding=True)


def says(o, s, name):
    ok(s in text_of(o), f'{name}: text holds "{s}"')


# ---------------------------------------------------------------- number-sense problems-4
ns = load('courses/number-sense/problems-4')
it = item(ns, 'p-hall-tiles')
P = [p['widget'] for p in it['parts']]
A, B = 360, 600
g = math.gcd(A, B)
g2 = max(d for d in range(1, A + 1) if A % d == 0 and B % d == 0)
ok(g == g2 == 120, 'hall: HCF two routes 120')
key(P[0], g, 0, 'hall 1')
lcm = A * B // g
wr(P[0], 'lcm', lcm, 'hall 1')
wr(P[0], 'missing-prime', 2 ** 3 * 3, 'hall 1')
ok(sp.factorint(360) == {2: 3, 3: 2, 5: 1} and sp.factorint(600) == {2: 3, 3: 1, 5: 2}, 'hall: prime forms of the explanation')
nf = sum(1 for d in range(1, 121) if 120 % d == 0)
ok(nf == (3 + 1) * 2 * 2 == 16 == sum(1 for d in range(1, 601) if A % d == 0 and B % d == 0), 'hall: 16 sides two routes')
key(P[1], nf, 0, 'hall 2')
wr(P[1], 'indices-multiplied', 3 * 1 * 1, 'hall 2')
wr(P[1], 'indices-added', 4 + 2 + 2, 'hall 2')
wr(P[1], 'lcm-carried', sum(1 for d in range(1, lcm + 1) if lcm % d == 0), 'hall 2')
key(P[2], (A // g) * (B // g), 0, 'hall 3')
ok(A * B // g ** 2 == 15, 'hall: 15 tiles by area')
wr(P[2], 'rows-added', A // g + B // g, 'hall 3')
wr(P[2], 'small-tile-carried', (A // 24) * (B // 24), 'hall 3')
key(P[3], F(A * B, 10000), 0.0005, 'hall 4')
ok(F(15 * 120 * 120, 10000) == F(216, 10) == F(36, 10) * 6, 'hall: 21.6 two routes')
wr(P[3], 'hundred', A * B / 100, 'hall 4')
wr(P[3], 'cm-squared', A * B, 'hall 4')
stale(it, [r'\b108\b', r'23\.328', r'\b12 cm', r'\bhall\b'], 'p-hall-tiles')

it = item(ns, 'p-lawn-pond')
P = [p['widget'] for p in it['parts']]
basin = math.pi * 2.5 ** 2
ok(near(basin, math.pi * 25 / 4) and near(basin, sp.N(sp.pi * sp.Rational(5, 2) ** 2)), 'basin area two routes')
key(P[0], basin, 0.02, 'basin 1')
for v, lab in [(19.63, 'printed'), (19.64, 'rounded up'), (3.14 * 6.25, 'pi 3.14'), (22 / 7 * 6.25, 'pi 22/7'), (round(22 / 7 * 6.25, 2), '22/7 to 2dp'), (19.635, '3dp')]:
    ok(abs(v - P[0]['answer']) <= 0.02, f'basin 1: band takes {lab} {v:.4f}')
for v, lab in [(19.6, '1dp'), (19.66, 'neighbour'), (19.61, 'neighbour')]:
    ok(abs(v - P[0]['answer']) > 0.02, f'basin 1: band refuses {lab} {v}')
wr(P[0], 'diameter', math.pi * 25, 'basin 1')
wr(P[0], 'circumference', math.pi * 5, 'basin 1')
key(P[1], 154 - 19.63, 0.02, 'basin 2')
for v in [154 - 19.63, round(154 - basin, 2), 154 - 19.64, 154 - 19.625, 134.38]:
    ok(abs(v - P[1]['answer']) <= 0.02, f'basin 2: band takes {v:.3f}')
wr(P[1], 'circumference-carried', 154 - 15.71, 'basin 2')
wr(P[1], 'perimeter', 2 * (14 + 11) - 19.63, 'basin 2')
key(P[2], math.ceil(134.37 / 15), 0, 'basin 3')
ok(8 * 15 < 134.37 <= 9 * 15 and round(134.37 / 15, 2) == 8.96, 'basin 3: 8.96, 9 tins cover 135')
wr(P[2], 'rounded-down', math.floor(134.37 / 15), 'basin 3')
wr(P[2], 'circumference-carried', math.ceil(138.29 / 15), 'basin 3')
wr(P[2], 'whole-courtyard', math.ceil(154 / 15), 'basin 3')
ok(round(134.37 / 15) == 9, 'basin 3 NOTE: nearest rounding also gives 9, so the part does not tell rounding up from rounding to nearest')
stale(it, [r'28\.27', r'79\.73', r'\blawn\b', r'\bpond\b', r'whole-lawn'], 'p-lawn-pond')

it = item(ns, 'p-meshing-gears')
w = it['parts'][3]['widget']
key(w, 240 * math.pi * 0.06, 0.5, 'gears 4')
ok(round(4 * 60 * math.pi * 6 / 100) == 45, 'gears 4: second route')
wr(w, 'radius', 240 * 2 * math.pi * 0.06, 'gears 4')
wr(w, 'centimetres', 240 * math.pi * 6, 'gears 4')
says(it['parts'][3], '4 \\times 60 = 240', 'gears 4')
ok(w.get('unit') == 'm', 'gears 4 unit m')

it = item(ns, 'p-cycle-commute')
ok(it['parts'][3]['widget'].get('unit') == 'km/h' and it['parts'][4]['widget'].get('unit') == 'm/s', 'cycle units')
key(it['parts'][3]['widget'], F(9, 1) / F(27, 60), 0, 'cycle 4')
key(it['parts'][4]['widget'], 20 * 1000 / 3600, 0.005, 'cycle 5')

# ---------------------------------------------------------------- quadratics problems-4
qd = load('courses/quadratics/problems-4')
it = item(qd, 'p-windy-ride')
v = sp.symbols('v')
tot = sp.together(sp.Rational(16) / v + 9 / (v - 2))
num, den = sp.fraction(tot)
ok(sp.expand(num - (25 * v - 32)) == 0 and sp.expand(den - v * (v - 2)) == 0, 'windy 1: top 25v - 32 over v(v - 2)')
ok(it['parts'][0]['widget']['answer'] == '25v-32', 'windy 1 key')
roots = sp.solve(sp.Eq(tot, sp.Rational(7, 2)), v)
ok(set(roots) == {8, sp.Rational(8, 7)}, 'windy 2: roots 8 and 8/7')
ratio = sp.simplify((9 / (v - 2)) / (16 / v))
ok(sp.simplify(ratio - 9 * v / (16 * (v - 2))) == 0, 'windy 4: ratio is 9v / 16(v - 2) (sympy)')
for x in [3, 5, 8, 11, F(1, 3), F(7, 2)]:
    ok((F(9) / (x - 2)) / (F(16) / x) == F(9) * x / (16 * (x - 2)), f'windy 4: ratio at v = {x}')
w4 = it['parts'][3]['widget']
ok(w4['answer'] == '9v' and w4.get('form') is None, 'windy 4: key 9v, no form')
tx = {x['id']: x['tex'] for x in w4['wrong']}
ok(tx.get('not-flipped') == '144' and tx.get('dropped-v') == '9' and 'whole' in tx, 'windy 4: wrong entries 144, 9, whole')
ok(9 * 16 == 144, 'windy 4: not-flipped is 9 x 16')
w5 = it['parts'][4]['widget']
key(w5, F(9 * 8, 16 * 6), 0.005, 'windy 5')
ok(F(9, 6) / F(16, 8) == F(3, 4), 'windy 5: 1.5 h over 2 h')
wr(w5, 'upside-down', F(96, 72), 'windy 5')
wr(w5, 'small-root', F(9) * F(8, 7) / (16 * (F(8, 7) - 2)), 'windy 5')
ok(F(16, 8) + F(9, 6) == F(7, 2), 'windy: 3.5 hours at v = 8')
says(it['parts'][3], 'time out is $\\dfrac{16}{v}$', 'windy 4 restates the two times')
says(it['parts'][4], '\\dfrac{9v}{16(v - 2)}', 'windy 5 restates the ratio of part 4')
ok(it['parts'][2]['widget'].get('unit') == 'km/h', 'windy 3 unit')

it = item(qd, 'p-storage-crate')
x = sp.symbols('x')
V = x ** 3 + 4 * x ** 2 + x - 6
q, r = sp.div(V, x + 2)
ok(r == 0 and sp.expand(q - (x ** 2 + 2 * x - 3)) == 0, 'crate 2: quotient')
ok(it['parts'][1]['widget']['answer'] == 'x^2+2x-3' and it['parts'][1]['widget']['form'] == 'expanded', 'crate 2 key and form')
says(it['parts'][1], 'multiplied out', 'crate 2 asks for the form')
key(it['parts'][4]['widget'], V.subs(x, sp.Rational(7, 2)), 0.0005, 'crate 5')
ok(F(11, 2) * F(13, 2) * F(5, 2) == F(89375, 1000), 'crate 5 second route')
ok(it['parts'][4]['widget'].get('unit') == 'm³', 'crate 5 unit')
it = item(qd, 'p-park-pond')
key(it['parts'][0]['widget'], math.hypot(4 + 2, 11 - 3), 0, 'pond 1')
ok(it['parts'][0]['widget'].get('unit') == 'm', 'pond 1 unit')

# ---------------------------------------------------------------- exams 0.1 and 0.2
e2 = load('exams/topic-0.2')
it = item(e2, 'e-diameter-ends')
Ax, Ay, Bx, By = -4, -6, 6, 18
cx, cy = F(Ax + Bx, 2), F(Ay + By, 2)
ok((cx, cy) == (1, 6), 'circle: the centre given is the midpoint of AB')
r2 = (Ax - cx) ** 2 + (Ay - cy) ** 2
ok(r2 == 169 == (Bx - cx) ** 2 + (By - cy) ** 2 and (Bx - Ax) ** 2 + (By - Ay) ** 2 == 676 == 26 ** 2, 'circle: r squared 169 from both ends, diameter 26')
X, Y = sp.symbols('x y')
ok(sp.expand((X - 1) ** 2 + (Y - 6) ** 2 - 169 - (X ** 2 + Y ** 2 - 2 * X - 12 * Y - 132)) == 0, 'circle: the accept form is the key expanded')
w = it['widget']
ok(w['answer'] == '(x-1)^2+(y-6)^2=169' and w['accept'] == ['x^2+y^2-2x-12y-132=0'], 'circle key and accept')
tx = {x['id']: x['tex'] for x in w['wrong']}
ok(tx == {'signs': '(x+1)^2+(y+6)^2=169', 'radius-not-squared': '(x-1)^2+(y-6)^2=13', 'full-diameter': '(x-1)^2+(y-6)^2=676'}, 'circle wrong entries')
ok(sum(1 for a, b in product(range(-30, 31), repeat=2) if (a - 1) ** 2 + (b - 6) ** 2 == 169) == 12, 'circle: 12 lattice points, so A and B are two of them')

e1 = load('exams/topic-0.1')
w = item(e1, 'e-pit-area')['widget']
key(w, 625 / math.pi, 0.5, 'pit')
ok(near(math.pi * (50 / (2 * math.pi)) ** 2, 625 / math.pi), 'pit second route')
wr(w, 'rounded-radius', math.pi * 8 ** 2, 'pit')
ok(abs(3.14 * 64 - 201) <= 0.5 and abs(22 / 7 * 64 - 201) <= 0.5, 'pit: 8 m radius with 3.14 or 22/7 still on rounded-radius')
for pi_ in (math.pi, 3.14, 22 / 7):
    ok(abs(pi_ * (50 / (2 * pi_)) ** 2 - 199) <= 0.5 and abs(pi_ * round(50 / (2 * pi_), 2) ** 2 - 199) <= 0.5, f'pit: 199 with pi = {pi_:.4f}, radius exact or to 2 places')
ok(w.get('unit') == 'm²' and w.get('placeholder') == 'a number', 'pit unit and placeholder')
w = item(e1, 'e-feed-updates')['widget']
key(w, 15 * 6.5 * 3600, 0.5, 'feed')
wr(w, 'six-fifty', 15 * (6 * 3600 + 50 * 60), 'feed')
ok(sum(15 for _ in range(6 * 3600 + 50 * 60)) == 369000, 'feed: six-fifty by counting seconds')
w = item(e1, 'e-plan-hall')['widget']
key(w, 9 * 2 * 6.5 * 2, 0.05, 'plan hall')
ok(w.get('unit') == 'm²' and w.get('placeholder') == 'a number', 'plan hall unit and placeholder')
ok(item(e1, 'e-five-counts')['title'] == 'Four summaries, five days', 'five counts title')
def one_mode(c):
    cnt = sorted((c.count(z) for z in set(c)), reverse=True)
    return c.count(10) == cnt[0] and (len(cnt) == 1 or cnt[0] > cnt[1])


sols = [c for c in combinations_with_replacement(range(0, 41), 5) if sum(c) == 40 and c[2] == 9 and c[4] - c[0] == 7 and one_mode(c)]
ok(sols == [(3, 8, 9, 10, 10)], f'five counts: one solution {sols}')

# ---------------------------------------------------------------- stat-learning problems-4
sl = load('courses/stat-learning/problems-4')
it = item(sl, 'p-one-unit')
P = [p['widget'] for p in it['parts']]


def net(w1, b1=-1.0, vv=2.0, d=1.0, xx=8.0, y=10.0):
    h = max(0.0, w1 * xx + b1)
    yh = vv * h + d
    return yh, 0.5 * (yh - y) ** 2


yh, L0 = net(0.5)
ok(yh == 7 and L0 == 4.5, 'unit: prediction 7, loss 4.5')
eps = 1e-6
grad = (net(0.5 + eps)[1] - net(0.5 - eps)[1]) / (2 * eps)
ok(near(grad, -48, 1e-5) and (7 - 10) * 2 * 8 == -48, 'unit 3: slope -48, chain rule and central difference')
key(P[2], -48, 0, 'unit 3')
eta = 0.002
w1 = 0.5 - eta * (-48)
key(P[3], w1, 0.0005, 'unit 4')
ok(near(w1, 0.596), 'unit 4: 0.596')
yh1, L1 = net(w1)
ok(near(yh1, 8.536) and near(L1, 1.071648) and L1 < L0, f'unit 4: the step takes the prediction to {yh1:.4f} and the loss to {L1:.4f}, down from 4.5')
says(it['parts'][3], 'from 7 to 8.536 hours and the loss falls from 4.5 to about 1.07', 'unit 4 explain')
ok(near(net(0.5 + 0.01 * 48)[1], 0.5 * (7 + 768 * 0.01 - 10) ** 2) and net(0.98)[1] > L0, 'unit: the old step 0.01 raised the loss (10.95)')
ok(near(6 / 768, 0.0078125) and net(0.5 + 48 * 0.0078)[1] < L0 < net(0.5 + 48 * 0.0079)[1], 'unit: largest step that does not raise the loss is 6/768')
wr(P[3], 'uphill', 0.5 + eta * (-48), 'unit 4')
wr(P[3], 'no-rate', 0.5 + 48, 'unit 4')
wr(P[3], 'carried', 0.5 - eta * (-9), 'unit 4')
ok((7 - 10) * 3 == -9, 'unit: -9 is the slope for v, part 3 slip slope-for-v')
# every slip of part 3 carried into part 4, and whether it has its own line
for wid, sl3 in [(x['id'], x['value']) for x in P[2]['wrong']]:
    c = 0.5 - eta * sl3
    hit = [x['id'] for x in P[3]['wrong'] if abs(x['value'] - c) <= x['tol']['abs']]
    print(f'   note unit 4: part 3 slip {wid} ({sl3}) carried gives {c:.3f}: lands on {hit or "the generic line"}')
knot = 1 / w1
key(P[4], knot, 0.0005, 'unit 5')
ok(near(sp.nsolve(sp.Symbol('x') * 0.596 - 1, 1.5), knot, 1e-9) and round(knot, 3) == 1.678, 'unit 5: knot 1.678 two routes')
wr(P[4], 'old-knot', 1 / 0.5, 'unit 5')
wr(P[4], 'sign', -1 / w1, 'unit 5')
wr(P[4], 'carried', 1 / 0.518, 'unit 5')
ok(round(10 / 0.518, 1) == 19.3 and round(10 * knot, 1) == 16.8, 'unit 5: 20 km to about 16.8 km')
says(it['parts'][4], 'from 20 km to about 16.8 km', 'unit 5 explain')
ok(P[0].get('unit') == 'h', 'unit 1 unit h')
stale(it, [r'0\.98\b', r'1\.02\b', r'1\.695', r'0\.59\b', r'\\eta = 0\.01\b', r'10\.2 km'], 'p-one-unit')

it = item(sl, 'p-order-sizes')
P = [p['widget'] for p in it['parts']]
orders = [2, 4, 6, 18, 22, 26]


def kstep(cs):
    gs = [[], []]
    for o in orders:
        gs[0 if abs(o - cs[0]) <= abs(o - cs[1]) else 1].append(o)
    return [F(sum(g_), len(g_)) for g_ in gs], gs


c1, g1 = kstep([3, 8])
ok(c1 == [3, 18], 'orders 1: one round gives 3 and 18')
key(P[0], c1[1], 0, 'orders 1')
wr(P[0], 'percent-sign', 0.18, 'orders 1')
cs, hist = c1, [c1]
while True:
    nx, gs = kstep(cs)
    if nx == cs:
        break
    cs = nx
    hist.append(cs)
ok(cs == [4, 22] and gs == [[2, 4, 6], [18, 22, 26]], 'orders 2: settles at 4 and 22')
key(P[1], cs[1], 0, 'orders 2')
wr(P[1], 'percent-sign', 0.22, 'orders 2')
inertia = lambda cc, gg: sum((o - cc[i]) ** 2 for i in (0, 1) for o in gg[i])
key(P[2], inertia([4, 22], gs), 0, 'orders 3')
wr(P[2], 'not-settled', inertia([3, 18], g1), 'orders 3')
wr(P[2], 'carried', inertia([3, 18], gs), 'orders 3')
ok(1 + 1 + 144 + 0 + 16 + 64 == 226 and 1 + 1 + 9 + 0 + 16 + 64 == 91, 'orders 3: 226 and 91 by hand')

it = item(sl, 'p-spam-filter')
w = it['parts'][3]['widget']
nw = math.hypot(0.9, -1.2)
ok(near(nw, 1.5) and near(math.sqrt(0.81 + 1.44), 1.5), 'spam 4: norm 1.5')
key(w, 1 / nw, 0.0005, 'spam 4')
ok(all(near(a / b, 0.6) for a, b in [(0.9, 1.5), (-1.2, -2), (0.3, 0.5)]), 'spam 4: the refit is 0.6 times the old (w, b): the same centre line')
# geometry: a point on the new edge w.x + b = 1, its distance from the centre line by projection
px = (1 - 0.3) / 0.9
ok(near(abs(0.9 * px + 0.3) / nw, 2 / 3) and near(0.4 * 5 / 3, 2 / 3), 'spam 4: margin 2/3 by geometry and as 0.4 x 5/3')
wr(w, 'gave-norm', nw, 'spam 4')
wr(w, 'street-width', 2 / nw, 'spam 4')
wr(w, 'unchanged', 0.4, 'spam 4')
ok(w['kind'] == 'numeric', 'spam 4 is typed')
typed = sum(1 for i in sl['items'] for p in i['parts'] if p['widget']['kind'] != 'choice')
ok(typed == 17 and sum(len(i['parts']) for i in sl['items']) == 19, f'stat-learning set: {typed} of 19 parts typed')
says(it, 'w \\cdot x + b = \\pm 1', 'spam prose')

# ---------------------------------------------------------------- testing problems-4
ts = load('courses/testing/problems-4')
it = item(ts, 'p-disk-failures')
w = it['parts'][4]['widget']
nmin = next(n for n in range(3, 10000) if F(n - 2, n) >= F(99, 100))
ok(nmin == 200 and F(198, 200) == F(99, 100) and F(197, 199) < F(99, 100), 'disk 5: smallest n with (n - 2)/n >= 0.99 is 200')
key(w, nmin, 0, 'disk 5')
wr(w, 'numerator', 198, 'disk 5')
wr(w, 'efficiency-now', F(38, 40), 'disk 5')
# the estimator's variance: exact from the gamma moments E[1/S] and E[1/S^2]
n, lam = sp.symbols('n lam', positive=True)
E1 = lam / (n - 1)
E2 = lam ** 2 / ((n - 1) * (n - 2))
ok(sp.simplify((n - 1) * E1 - lam) == 0 and sp.simplify((n - 1) ** 2 * E2 - lam ** 2 - lam ** 2 / (n - 2)) == 0, 'disk 5: (n - 1)/sum is unbiased with variance lam^2/(n - 2)')
s_ = sp.symbols('s', positive=True)
dens = lam ** 5 * s_ ** 4 * sp.exp(-lam * s_) / sp.factorial(4)
ok(sp.simplify(sp.integrate(dens / s_, (s_, 0, sp.oo)) - lam / 4) == 0 and sp.simplify(sp.integrate(dens / s_ ** 2, (s_, 0, sp.oo)) - lam ** 2 / 12) == 0, 'disk 5: the gamma moments by integration at n = 5')
says(it['parts'][4], 'At the 40 gaps seen it is 0.95', 'disk 5 explain')
says(item(ts, 'p-website-signups')['parts'][0], 'The largest value is sufficient for a uniform on $(0, \\theta)$. Poisson', 'signups 1 why')

# ---------------------------------------------------------------- exams 1.6 and 2.1
x6 = load('exams/topic-1.6')
it = item(x6, 's-pareto-losses')
nn, S = 80, -32
th = sp.symbols('theta', positive=True)
ell = nn * sp.log(th) + (th - 1) * S
mle = sp.solve(sp.diff(ell, th), th)
ok(mle == [sp.Rational(5, 2)], 's-pareto 2: MLE 5/2 by calculus')
grid = max((nn * math.log(t / 1000) + (t / 1000 - 1) * S, t / 1000) for t in range(1, 10000))[1]
ok(near(grid, 2.5, 1e-3), 's-pareto 2: MLE by a grid search')
P = [p['widget'] for p in it['parts']]
key(P[1], 2.5, 0.005, 's-pareto 2')
wr(P[1], 'upside-down', 32 / 80, 's-pareto 2')
wr(P[1], 'exponent', 2.5 + 1, 's-pareto 2')
wr(P[1], 'sign', -2.5, 's-pareto 2')
import mpmath as mp
for t0 in (2.5, 1.3, 4.0):
    f = lambda z, t=t0: t * z ** (t - 1)
    lnf = lambda z, t: mp.log(t) + (t - 1) * mp.log(z)
    ok(near(mp.quad(f, [0, 1]), 1, 1e-9), f's-pareto: the density integrates to 1 on (0, 1) at theta = {t0}')
    d2 = lambda z, t=t0: mp.diff(lambda u: lnf(z, u), t, 2)
    d1 = lambda z, t=t0: mp.diff(lambda u: lnf(z, u), t)
    ok(near(-mp.quad(lambda z: d2(z) * f(z), [0, 1]), 1 / t0 ** 2, 1e-6), f's-pareto 3: I = 1/theta^2 by the second derivative at theta = {t0}')
    ok(near(mp.quad(lambda z: d1(z) ** 2 * f(z), [0, 0.01, 1]), 1 / t0 ** 2, 1e-6), f's-pareto 3: I by the squared score at theta = {t0}')
key(P[2], F(25, 4) / 80, 0.0001, 's-pareto 3')
wr(P[2], 'sd', math.sqrt(6.25 / 80), 's-pareto 3')
wr(P[2], 'info', 80 / 6.25, 's-pareto 3')
wr(P[2], 'theta-not-squared', 2.5 / 80, 's-pareto 3')
ok(round(math.sqrt(6.25 / 80), 2) == 0.28, 's-pareto 3: standard error about 0.28')
ok(near(mp.quad(lambda z: mp.log(z) * 2.5 * z ** 1.5, [0, 0.01, 1]), F(S, nn), 1e-9), 's-pareto: mean of ln x at theta 2.5 is -0.4, the data given')
stale(it, [r'\\alpha', r'Pareto', r'\blosses\b', r'£', r'x > 1', r'1\.5\b'], 's-pareto-losses')
opt = {o['id']: o for o in P[0]['options']}
ok(opt['a'].get('correct') is True and 'uniform on $(0, \\theta)$' in opt['c']['why'] and '0 < x < 1' in opt['c']['why'], 's-pareto 1: key a, option c line')

it = item(x6, 's-pool-rates')
cell = it['widget']['rows'][0][0]
lr = 2 * (90 * math.log(90 / 75) + 60 * math.log(60 / 75))
ll = lambda a, b: 90 * math.log(a) - a + 60 * math.log(b) - b
ok(near(lr, 2 * (ll(90, 60) - ll(75, 75))), 'pool: -2 ln Lambda two routes')
key(cell, lr, 0.005, 'pool')
for dp, inside in [(5, True), (4, True), (3, False), (2, False)]:
    vv = 2 * (90 * round(math.log(1.2), dp) + 60 * round(math.log(0.8), dp))
    ok((abs(vv - cell['answer']) <= 0.005) == inside, f'pool: logs to {dp} places give {vv:.4f}, {"inside" if inside else "outside"} the band')
ok(near(2 * (90 * 0.182 + 60 * -0.223), 6.0) and near(2 * 15 ** 2 / 75, 6.0), 'pool: logs to 3 places give 6.00, Pearson is 6.00')
says(it, 'Keep 5 decimal places in each logarithm', 'pool question')
ok(round(90 * math.log(1.2), 2) == 16.41 and round(60 * math.log(0.8), 2) == -13.39, 'pool explain 16.41 and 13.39')

x1 = load('exams/topic-2.1')
ids = [i['id'] for i in x1['items']]
ok('e-odds-update' in ids and 'e-report-which' not in ids and 'e-oob-overlap' not in ids, 'topic-2.1: e-odds-update in, e-report-which out, e-oob-overlap out')
it = item(x1, 'e-odds-update')
w = it['widget']
odds = F(1, 9) * sp.exp(sp.Rational(9, 10))
p1 = float(odds / (1 + odds))
p2 = 1 / (1 + math.exp(-(math.log(0.1 / 0.9) + 0.45 * 2)))
ok(near(p1, p2) and round(p1, 3) == 0.215, f'odds: probability {p1:.5f} two routes')
key(w, p1, 0.0015, 'odds')
wr(w, 'prob-times', 0.1 * math.exp(0.9), 'odds')
wr(w, 'odds-as-prob', float(odds), 'odds')
r_ = round(0.111 * 2.46, 3)
ok(abs(r_ / (1 + r_) - w['answer']) <= 0.0015 and abs(0.273 / 1.273 - w['answer']) <= 0.0015, 'odds: the explanation\'s rounded figures land inside the band')
ok(w.get('unit') == '%' and it['difficulty'] == 3, 'odds unit % and difficulty 3')
ramp = {}
for i in x1['items']:
    ramp[i['difficulty']] = ramp.get(i['difficulty'], 0) + 1
print('   note topic-2.1 difficulty counts:', dict(sorted(ramp.items())), 'items', len(ids))
for iid in ('e-spline-slope', 'e-kmeans-spreads'):
    ok(item(x1, iid)['widget'].get('placeholder') == 'a number', f'{iid} placeholder')

print(f'recompute: {checks} checks, {fails} failures, {len(finds)} findings (content faults left failing)')
raise SystemExit(1 if fails else 0)
