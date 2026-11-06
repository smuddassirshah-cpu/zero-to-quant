"""Recompute every number stated in topology level 3 (Compact and complete) by two routes, and check each at its JSON path.
Run: python3 docs/reports/topology-L3-numbers.py   (standard library only; exits 0 when every check passes)
Route 1 is a closed form or an exact loop; route 2 is independent (brute force over subsets, a sliding window,
bisection, a logarithm formula, Newton on Phi, a dense grid). The script also runs every code widget of the level in
CPython (solution passes, starter fails) and prints the margin at each stopping boundary, since Pyodide must land on
the same integer count.
"""
import sys, os, math, json, re
from fractions import Fraction as F
from itertools import combinations
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("topology", 3)
E = lv.expect
fails = []
HERE = os.path.dirname(os.path.abspath(__file__))


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def bisect(f, a, b):
    fa = f(a)
    for _ in range(200):
        c = (a + b) / 2
        if (f(c) < 0) == (fa < 0): a, fa = c, f(c)
        else: b = c
    return (a + b) / 2


Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
phi = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def first_n(pred, start=0):
    n = start
    while not pred(n): n += 1
    return n


# ================= l9 =================
I = [(-0.1, 0.35), (0.3, 0.65), (0.6, 1.1), (0.1, 0.32), (0.4, 0.62), (0.5, 0.58)]
grid = [k / 20000 for k in range(20001)]
def covers(idx, ints=I):
    return all(any(ints[i][0] < x < ints[i][1] for i in idx) for x in grid)
def greedy(ints, a, b):
    out, x = [], a
    while True:
        best = None
        for k, (lo, hi) in enumerate(ints):
            if lo < x < hi and (best is None or hi > ints[best][1]): best = k
        if best is None: return None
        out.append(best); x = ints[best][1]
        if x > b: return sorted(out)
smallest = [c for r in range(1, 7) for c in combinations(range(6), r) if covers(c)]
m = min(len(c) for c in smallest)
assert [c for c in smallest if len(c) == m] == [(0, 1, 2)] and greedy(I, 0, 1) == [0, 1, 2]
E("l9", "screens[0].widget.answer", "I3"); E("l9", "screens[0].explain.text", 0.35); E("l9", "screens[0].explain.text", 0.65)
E("l9", "screens[0].feedback.byKey.I2", 0.35)
# Lebesgue number: sliding windows against the closed form (the narrowest overlap)
def leb(ints, step=1e-4):
    L, k = 1.0, 0
    while k * step <= 1:
        x = k * step
        L = min(L, max(hi - x for lo, hi in ints if lo < x < hi)); k += 1
    return L
two('lebesgue', leb(I[:3]), min(I[0][1] - I[1][0], I[1][1] - I[2][0]), 1e-3)
E("l9", "screens[6].widget.answer", 0.05); E("l9", "screens[6].explain.text", 0.05); E("l9", "screens[6].explain.text", 0.025)
E("l9", "screens[6].widget.wrong[0].value", 0.025); E("l9", "screens[6].widget.wrong[1].value", round(I[1][1] - I[1][0], 2))
E("l9", "quiz[1].widget.answer", 0.025); E("l9", "quiz[1].widget.wrong[0].value", 0.05); E("l9", "quiz[1].widget.wrong[1].value", 0.1)
# scenario grid
pts_ = [F(-10) + F(1, 2) * k for k in range(41)]
assert pts_[-1] == 10 and len(pts_) == 41
worst_gap = max(min(abs(F(x, 1000) - p) for p in pts_) for x in range(-10000, 10001))
assert worst_gap == F(1, 4)
E("l9", "screens[10].widget.rows[0][1].answer", 41); E("l9", "screens[10].widget.rows[1][1].answer", 20000 * 0.25)
E("l9", "screens[10].widget.rows[0][1].wrong[0].value", 40); E("l9", "screens[10].widget.rows[1][1].wrong[0].value", 10000)
for v in (41, 0.25, 5000): E("l9", "screens[10].explain.text", v)
E("l9", "screens[10].prose", 20000)
# Review findings 1 and 2: interval membership (open intervals) and the ball cover at grid midpoints
inside = lambda x: [k + 1 for k, (lo, hi) in enumerate(I) if lo < x < hi]
assert inside(0.35) == [2], inside(0.35)          # only I2 holds 0.35 (I1 ends there, open)
assert inside(0.6) == [2, 5], inside(0.6)         # I5 holds 0.6 too, so the hint must not claim I2 alone
assert '0.6' not in lv.text("l9", "screens[0].hints[2].text"), 'hint still claims 0.6'
def ball_cover(r):                                 # open balls of radius r at -10, -9.5, ..., 10 against every 0.005 step and every midpoint
    mids = [F(-10) + F(1, 2) * k + F(1, 4) for k in range(40)]
    pts = mids + [F(x, 1000) for x in range(-10000, 10001, 5)]
    return all(any(abs(p - c) < r for c in pts_) for p in pts)
assert not ball_cover(F(1, 4)), 'radius 0.25 open balls must miss the midpoints'
assert ball_cover(F(3, 10)), 'radius 0.3 open balls must cover the interval'
assert '0.3%' in lv.text("l9", "screens[10].explain.text") and 'open balls' in lv.text("l9", "screens[10].explain.text")
# Review finding 13 and the whole level: each wrong value's slip, typed to the answer's own rounding, must lie outside the
# answer tolerance and inside its own (both 3 s.f. roundings of 1/32 are tried). The l13 screen asks for 3 s.f.
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
def sf3(x, mode):
    d = Decimal(repr(x)); e = d.adjusted() - 2
    return float(d.quantize(Decimal(1).scaleb(e), rounding=mode))
_w = json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', 'l13-fixed-point-iteration.json')))['screens'][11]['widget']
_ans, _atol = _w['answer'], _w['tol']['abs']
assert _ans == 0.0308 and abs(_ans - (1 - math.exp(-1 / 32))) < 5e-5
for _x in _w['wrong']:
    for _m in (ROUND_HALF_UP, ROUND_HALF_EVEN):
        _r = sf3(_x['value'], _m)
        if abs(_r - _ans) <= _atol + 1e-9: fails.append(f"l13 wrong {_x['id']} typed to 3 s.f. ({_r}) is graded correct")
        if abs(_r - _x['value']) > _x['tol']['abs'] + 1e-12: fails.append(f"l13 wrong {_x['id']} typed to 3 s.f. ({_r}) is outside its own tolerance")
# The same test for every numeric wrong whose question states a rounding ("four decimal places", "3 significant figures"):
# the slip typed that way must lie outside the answer tolerance and inside its own tolerance.
_N = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}
def _typed(x, dp, sig, mode):
    d = Decimal(repr(x))
    q = d.adjusted() - (sig - 1) if sig else -dp
    return float(d.quantize(Decimal(1).scaleb(q), rounding=mode))
for _f in ['l9-open-covers', 'l10-compact-images', 'l11-complete-spaces', 'l12-contraction-mapping', 'l13-fixed-point-iteration', 'homework-3', 'review-3']:
    def _scan(o, f=_f):
        if isinstance(o, dict):
            w = o.get('widget')
            if isinstance(o.get('question'), str) and isinstance(w, dict) and w.get('kind') == 'numeric' and w.get('wrong'):
                m = re.search(r'(\w+) (decimal places|significant figures)', o['question'])
                if m and (m.group(1) in _N or m.group(1).isdigit()):
                    n = _N.get(m.group(1)) or int(m.group(1)); sig = m.group(2).startswith('sig')
                    a = w['answer']; at = (w.get('tol') or {}).get('abs', 0) + 1e-9
                    for x in w['wrong']:
                        wt = (x.get('tol') or {}).get('abs', 1e-9) + 1e-12
                        for mode in (ROUND_HALF_UP, ROUND_HALF_EVEN):
                            r = _typed(x['value'], None if sig else n, n if sig else None, mode)
                            if abs(r - a) <= at: fails.append(f"{f}: wrong {x['id']} typed as asked ({r}) is graded correct")
                            elif abs(r - x['value']) > wt: fails.append(f"{f}: wrong {x['id']} typed as asked ({r}) is outside its own tolerance")
            for v in o.values(): _scan(v)
        elif isinstance(o, list):
            for v in o: _scan(v)
    _scan(json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', _f + '.json'))))

# ================= l10 =================
f = lambda x: x * math.exp(-x)
mx = max(f(k / 10000) for k in range(30001))
two('max xe^-x', mx, 1 / math.e, 1e-8); two('peak by f\'=0', bisect(lambda x: (1 - x) * math.exp(-x), 0.5, 2), 1)
E("l10", "screens[0].widget.answer", round(1 / math.e, 4)); E("l10", "screens[0].widget.wrong[0].value", round(f(3), 4)); E("l10", "screens[0].widget.wrong[1].value", 1)
E("l10", "screens[0].explain.text", 0.3679); E("l10", "screens[0].explain.text", 0.1494)
# sqrt uniform delta: at eps = 0.1 delta = 0.01, and eps itself fails at 0
assert math.sqrt(0.01) <= 0.1 + 1e-12 and math.sqrt(0.0101) > 0.1 and math.sqrt(0.1) > 0.1
E("l10", "screens[5].explain.text", 0.01); E("l10", "quiz[0].widget.answer", 0.01)
E("l10", "quiz[0].widget.wrong[0].value", 0.1); E("l10", "quiz[0].widget.wrong[1].value", round(math.sqrt(0.1), 4))
s1, s2 = 0.2, 0.1
vol = lambda w, r: math.sqrt(w * w * s1 * s1 + (1 - w) ** 2 * s2 * s2 + 2 * w * (1 - w) * r * s1 * s2)
w3 = (s2 ** 2 - 0.3 * s1 * s2) / (s1 ** 2 + s2 ** 2 - 2 * 0.3 * s1 * s2)
w3b = min((k / 100000 for k in range(100001)), key=lambda w: vol(w, 0.3))
two('minvol w', w3, w3b, 1e-4); two('minvol exact', w3, F(4, 38))
E("l10", "screens[10].widget.answer", round(w3, 4)); E("l10", "screens[10].widget.wrong[0].value", 0.01 / 0.05); E("l10", "screens[10].widget.wrong[1].value", round(1 - w3, 4))
E("l10", "screens[10].feedback.correct", round(100 * vol(w3, 0.3), 3)); E("l10", "screens[10].explain.text", round(100 * vol(w3, 0.3), 3))
w6 = (s2 ** 2 - 0.6 * s1 * s2) / (s1 ** 2 + s2 ** 2 - 2 * 0.6 * s1 * s2)
two('rho 0.6 w', w6, -1 / 13)
E("l10", "screens[11].prose", round(w6, 4))
assert min((k / 10000 for k in range(10001)), key=lambda w: vol(w, 0.6)) == 0 and math.isclose(vol(0, 0.6), 0.1)

# ================= l11 =================
ramp = lambda n: (lambda x: min(1, max(0, n * (x - 0.5))))
def d1_num(fn, gn, m=200000):
    h = 1 / m; return h * sum(abs(fn((k + 0.5) * h) - gn((k + 0.5) * h)) for k in range(m))
for n, mm, v in [(4, 8, 0.0625), (5, 10, 0.05), (10, 20, 0.025)]:
    two(f'd1 ramps {n},{mm}', abs(1 / (2 * n) - 1 / (2 * mm)), v); two(f'd1 ramps {n},{mm} by sum', d1_num(ramp(n), ramp(mm)), v, 1e-6)
E("l11", "screens[0].widget.answer", 0.0625); E("l11", "screens[0].explain.text", 0.0625)
E("l11", "screens[0].widget.wrong[0].value", 0.5); E("l11", "screens[0].widget.wrong[1].value", 1 / 8)
supgap = max(abs(ramp(4)(k / 100000) - ramp(8)(k / 100000)) for k in range(100001))
two('sup gap', supgap, 0.5, 1e-4)
E("l11", "screens[5].widget.answer", 0.5); E("l11", "screens[5].widget.wrong[0].value", 0.0625); E("l11", "screens[5].widget.wrong[1].value", 1)
two('arctan d(10,100)', math.atan(100) - math.atan(10), 0.089669, 1e-6)
E("l11", "screens[6].prose", 0.089669)
for eps, N in [(0.1, 10), (0.01, 100), (0.001, 1000)]:
    two(f'tail N {eps}', first_n(lambda n: math.pi / 2 - math.atan(n) < eps, 1), math.floor(1 / math.tan(eps)) + 1)
    assert first_n(lambda n: math.pi / 2 - math.atan(n) < eps, 1) == N
    E("l11", "screens[6].explain.text", N)
E("l11", "screens[6].widget.answer", 100); E("l11", "screens[6].widget.wrong[0].value", 10); E("l11", "screens[6].widget.wrong[1].value", 1000)
E("l11", "screens[6].widget.accept", round(1 / math.tan(0.01), 3))
xs = [math.atan(n) for n in range(1, 2001)]
fN = lambda xs, eps: first_n(lambda N: max(xs[N - 1:]) - min(xs[N - 1:]) < eps, 1)
assert fN(xs, 0.01) == 96 and fN(xs, 0.1) == 10
# second route for the finite-list count: the tail of an increasing list has width xs[-1] - xs[N-1]
assert first_n(lambda N: xs[-1] - xs[N - 1] < 0.01, 1) == 96
E("l11", "screens[9].explain.text", 96); E("l11", "screens[9].explain.text", 100)
rr = [1 / (2 * n) for n in range(1, 1001)]
assert fN(rr, 0.01) == 48 == first_n(lambda N: rr[N - 1] - rr[-1] < 0.01, 1)
E("l11", "screens[10].widget.answer", 0.025); E("l11", "screens[10].widget.wrong[0].value", 0.5); E("l11", "screens[10].widget.wrong[1].value", 0.05)
E("l11", "screens[11].explain.text", 0.5)
E("l11", "quiz[1].widget.answer", 1000); E("l11", "quiz[1].widget.wrong[0].value", 100); E("l11", "quiz[1].widget.wrong[1].value", 1001)
E("l11", "quiz[1].explain.text", round(1 / math.tan(0.001), 4))

# ================= l12 =================
T = lambda x: 0.5 * x + 1
a, b = [0], [10]
for _ in range(4): a.append(T(a[-1])); b.append(T(b[-1]))
assert a == [0, 1, 1.5, 1.75, 1.875] and b == [10, 6, 4, 3, 2.5]
two('gap 3', b[3] - a[3], 10 * 0.5 ** 3)
E("l12", "screens[0].widget.answer", 1.25); E("l12", "screens[0].widget.wrong[0].value", b[2] - a[2]); E("l12", "screens[0].widget.wrong[1].value", b[4] - a[4])
for v in (1.875, 2.5, 1.25): E("l12", "screens[0].explain.text", v)
ap = lambda q, d, tol: first_n(lambda n: q ** n / (1 - q) * d < tol)
apl = lambda q, d, tol: math.ceil(math.log(tol * (1 - q) / d) / math.log(q))
for args, v in [((0.5, 1, 1e-6), 21), ((math.sin(1), 1 - math.cos(1), 1e-6), 87), ((1.02 / 1.06, 5 / 1.06, 0.01), 246)]:
    assert ap(*args) == apl(*args) == v, (args, ap(*args), apl(*args))
E("l12", "screens[5].widget.answer", 21); E("l12", "screens[5].widget.wrong[0].value", 20); E("l12", "screens[5].widget.wrong[1].value", 6)
E("l12", "screens[5].explain.text", round(2 * 0.5 ** 20 * 1e6, 1)); E("l12", "screens[5].explain.text", round(2 * 0.5 ** 21 * 1e7, 1))
E("l12", "screens[5].canvas.params.rows[0][1]", round(2 * 0.5 ** 19 * 1e6, 1)); E("l12", "screens[5].canvas.params.rows[1][1]", round(2 * 0.5 ** 20 * 1e6, 1))
# the matrix map
A = [[0.6, 0.6], [0, 0.3]]; bb = [1, 1]
row = max(sum(abs(v) for v in r) for r in A); col = max(abs(A[0][j]) + abs(A[1][j]) for j in range(2))
# spectral norm: sqrt of the largest eigenvalue of A^T A, closed form for 2x2, against a power iteration
AtA = [[A[0][0] ** 2 + A[1][0] ** 2, A[0][0] * A[0][1] + A[1][0] * A[1][1]], [A[0][0] * A[0][1] + A[1][0] * A[1][1], A[0][1] ** 2 + A[1][1] ** 2]]
tr, det = AtA[0][0] + AtA[1][1], AtA[0][0] * AtA[1][1] - AtA[0][1] ** 2
s2n = math.sqrt((tr + math.sqrt(tr * tr - 4 * det)) / 2)
v = [1.0, 0.0]
for _ in range(200):
    w = [AtA[0][0] * v[0] + AtA[0][1] * v[1], AtA[1][0] * v[0] + AtA[1][1] * v[1]]; nrm = math.hypot(*w); v = [w[0] / nrm, w[1] / nrm]
two('spectral norm', s2n, math.sqrt(nrm), 1e-9)
assert math.isclose(row, 1.2) and math.isclose(col, 0.9)
fy = F(1) / (1 - F(3, 10)); fx = (F(6, 10) * fy + 1) / (1 - F(6, 10))
assert (fx, fy) == (F(65, 14), F(10, 7))
E("l12", "screens[6].widget.rows[0][1].answer", 1.2); E("l12", "screens[6].widget.rows[1][1].answer", 0.9)
E("l12", "screens[6].widget.rows[2][1].answer", round(float(fx), 4)); E("l12", "screens[6].widget.rows[3][1].answer", round(float(fy), 4))
E("l12", "screens[6].explain.text", round(s2n, 4)); E("l12", "screens[6].explain.text", F(65, 14))
X = [0.0, 0.0]; its = []
for _ in range(3): X = [0.6 * X[0] + 0.6 * X[1] + 1, 0.3 * X[1] + 1]; its.append(X)
assert [round(c, 4) for c in its[1]] == [2.2, 1.3] and [round(c, 4) for c in its[2]] == [3.1, 1.39]
d01 = 2.0
assert ap(0.9, d01, 1e-6) == apl(0.9, d01, 1e-6) == 160
X = [0.0, 0.0]; n31 = None
for n in range(1, 200):
    X = [0.6 * X[0] + 0.6 * X[1] + 1, 0.3 * X[1] + 1]
    if abs(X[0] - fx) + abs(X[1] - fy) < 1e-6: n31 = n; break
assert n31 == 31
E("l12", "screens[6].explain.text", 160); E("l12", "screens[6].explain.text", 31)
# trap facts
g = lambda x: x + 1 / x
assert g(1) == 2 and g(2) == 2.5 and math.cos(2) < -0.41
E("l12", "screens[7].widget.options[1].why", 2.5); E("l12", "screens[7].widget.options[2].why", round(math.cos(2), 2))
# Gordon
q = 1.02 / 1.06
V = 0.0; Vs = []
for _ in range(400): V = (5 + 1.02 * V) / 1.06; Vs.append(V)
assert [round(x, 2) for x in Vs[:3]] == [4.72, 9.26, 13.62]
two('gordon', 5 / (0.06 - 0.02), bisect(lambda v: (5 + 1.02 * v) / 1.06 - v, 0, 1000))
true_n = first_n(lambda n: 125 - Vs[n - 1] < 0.01, 1)
assert true_n == 246 == ap(q, 5 / 1.06, 0.01)
print('margin Gordon: 125 q^245 =', 125 * q ** 245, ' 125 q^246 =', 125 * q ** 246)
for v in (4.72, 9.26, 13.62, 125): E("l12", "screens[10].prose", v)
E("l12", "screens[10].prose", round(q, 4))
E("l12", "screens[10].widget.answer", 246); E("l12", "screens[10].widget.wrong[0].value", 245); E("l12", "screens[10].widget.wrong[1].value", 21)
E("l12", "screens[10].feedback.byKey.off", round(125 * q ** 245, 4)); E("l12", "screens[10].hints[1].text", round(math.log(0.01 / 125) / math.log(q), 1))
for k, row_ in enumerate(json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', 'l12-contraction-mapping.json')))['screens'][10]['canvas']['params']['rows']):
    assert row_[1] == f'{Vs[k]:.2f}' and row_[2] == f'{125 - Vs[k]:.2f}', row_
q7 = 1.07 / 1.06
E("l12", "screens[11].explain.text", round(q7, 4))
V = 0.0; V7 = []
for _ in range(100): V = (5 + 1.07 * V) / 1.06; V7.append(V)
assert f'{V7[0]:.2f}' == '4.72' and f'{V7[9]:.1f}' == '49.2' and f'{V7[99]:.0f}' == '779', (V7[9], V7[99])
two('repelling point', 5 / (0.06 - 0.07), -500)
E("l12", "quiz[2].widget.answer", round(0.8 ** 10 / 0.2 * 0.4, 4)); E("l12", "quiz[2].widget.wrong[0].value", round(0.8 ** 10 * 0.4, 4)); E("l12", "quiz[2].widget.wrong[1].value", round(0.8 ** 10 / 1.8 * 0.4, 4))

# ================= l13 =================
xstar = bisect(lambda x: math.cos(x) - x, 0, 1)
x = 0.0
for _ in range(200): x = math.cos(x)
two('dottie', xstar, x)
E("l13", "screens[0].widget.answer", round(xstar, 6)); E("l13", "screens[0].explain.text", round(xstar, 6))
x = 1.0; its = []
for _ in range(5): x = math.cos(x); its.append(round(x, 4))
assert its == [0.5403, 0.8576, 0.6543, 0.7935, 0.7014]
E("l13", "screens[1].explain.text", 0.5403)
two('q sin 1', math.sin(1), max(math.sin(k / 10000) for k in range(10001)))
E("l13", "screens[3].widget.answer", round(math.sin(1), 4)); E("l13", "screens[3].widget.wrong[0].value", round(math.cos(1), 4)); E("l13", "screens[3].widget.wrong[1].value", round(math.sin(math.pi / 180), 4))
E("l13", "screens[4].widget.answer", 87); E("l13", "screens[4].widget.wrong[0].value", 86); E("l13", "screens[4].widget.wrong[1].value", 32)
E("l13", "screens[4].prose", round(1 - math.cos(1), 4)); E("l13", "screens[4].hints[0].text", round((1 - math.cos(1)) / (1 - math.sin(1)), 3))
E("l13", "screens[4].hints[1].text", round(math.log(1e-6 * (1 - math.sin(1)) / (1 - math.cos(1))) / math.log(math.sin(1)), 1))
qq = math.sin(1); dd = 1 - math.cos(1)
E("l13", "screens[4].canvas.params.rows[0][1]", round(qq ** 80 / (1 - qq) * dd * 1e6, 1)); E("l13", "screens[4].canvas.params.rows[1][1]", round(qq ** 86 / (1 - qq) * dd * 1e6, 2))
E("l13", "screens[4].feedback.byKey", round(qq ** 86 / (1 - qq) * dd * 1e6, 2)); E("l13", "screens[4].explain.text", round(qq ** 87 / (1 - qq) * dd * 1e7, 1))
x = 1.0; n_post = None; n_true = None
for n in range(1, 200):
    xn = math.cos(x)
    if n_post is None and qq / (1 - qq) * abs(xn - x) < 1e-6: n_post = n
    if n_true is None and abs(xn - xstar) < 1e-6: n_true = n
    x = xn
assert (n_post, n_true) == (39, 32)
for v in (87, 39, 32): E("l13", "screens[5].prose", v)
E("l13", "screens[5].widget.answer", round(math.sin(xstar), 4)); E("l13", "screens[5].widget.wrong[0].value", 0.8415); E("l13", "screens[5].widget.wrong[1].value", round(xstar, 4))
E("l13", "screens[5].explain.text", 0.6736)
# Newton
N = lambda x: x / 2 + 1 / x
x = 1.0; nw = []
for _ in range(4): x = N(x); nw.append(x)
errs = [abs(v - math.sqrt(2)) for v in nw]
assert [round(v, 6) for v in nw[1:]] == [1.416667, 1.414216, 1.414214] and errs[3] < 1e-6 < errs[2]
assert ap(0.5, 0.5, 1e-6) == apl(0.5, 0.5, 1e-6) == 20
assert max(abs(0.5 - 1 / (k / 1000) ** 2) for k in range(1000, 2001)) == 0.5
E("l13", "screens[6].widget.answer", 20); E("l13", "screens[6].widget.wrong[0].value", 4); E("l13", "screens[6].widget.wrong[1].value", 21)
E("l13", "screens[6].explain.text", round(errs[2] * 1e6, 1)); E("l13", "screens[6].explain.text", round(errs[3] * 1e12, 1))
# Picard: iterates of T(y)(t) = 1 + int_0^t y from y0 = 1 are Taylor polynomials; integrate exactly with Fractions
poly = [F(1)]
for _ in range(3): poly = [F(1)] + [c / (k + 1) for k, c in enumerate(poly)]
P3 = sum(float(c) * 0.5 ** k for k, c in enumerate(poly))
two('P3(1/2)', P3, sum(0.5 ** k / math.factorial(k) for k in range(4)))
E("l13", "screens[7].widget.answer", round(P3, 4)); E("l13", "screens[7].widget.wrong[0].value", round(math.exp(0.5), 4)); E("l13", "screens[7].widget.wrong[1].value", 1.625)
E("l13", "screens[7].explain.text", round(P3, 7)); E("l13", "screens[7].explain.text", round(math.exp(0.5), 7)); E("l13", "screens[7].explain.text", round(math.exp(0.5) - P3, 7))
E("l13", "screens[9].prose", round(math.cos(0.5), 4))
x = 0.5
for _ in range(100): x = math.cos(x)
two('cos from 0.5', x, xstar, 1e-9)
# implied volatility contraction
C = lambda s: 100 * (2 * Phi(s / 2) - 1)
M = 100 * phi(0)
Tv = lambda s: s - (C(s) - 8) / M
qv = 1 - math.exp(-1 / 32)
two('q iv', qv, 1 - 100 * phi(0.25) / M)
assert max(abs(1 - 100 * phi(s / 2) / M) for s in [0.1 + k * 0.4 / 4000 for k in range(4001)]) <= qv + 1e-12
iv = bisect(lambda s: C(s) - 8, 0.01, 1)
s = 0.1; ss = []
for _ in range(3): s = Tv(s); ss.append(s)
assert abs(ss[2] - iv) < 1e-8
E("l13", "screens[11].prose", round(M, 4)); E("l13", "screens[11].prose", round(Tv(0.1), 6)); E("l13", "screens[11].prose", round(Tv(0.5), 6))
for k, sv in enumerate(ss): E("l13", f"screens[11].canvas.params.rows[{k}][1]", round(sv, 6))
E("l13", "screens[11].widget.answer", round(qv, 4)); E("l13", "screens[11].widget.wrong[0].value", round(1 - qv, 4)); E("l13", "screens[11].widget.wrong[1].value", 1 / 32)
E("l13", "screens[11].explain.text", round(100 * iv, 4))
gold = (math.sqrt(5) - 1) / 2
two('golden', gold, bisect(lambda x: 1 / (1 + x) - x, 0.5, 1))
E("l13", "quiz[0].widget.answer", round(gold, 6)); E("l13", "quiz[0].widget.wrong[0].value", round(1 + gold, 6)); E("l13", "quiz[0].widget.wrong[1].value", round(-1 - gold, 6))

# ================= review =================
R = [(-0.1, 0.4), (0.3, 0.7), (0.2, 0.5), (0.6, 1.2), (0.65, 0.9)]
best = min(len(c) for r in range(1, 6) for c in combinations(range(5), r) if covers(c, R))
assert best == 3 and greedy(R, 0, 1) == [0, 1, 3]
E("review", "items[0].widget.answer", 3); E("review", "items[0].widget.wrong[0].value", 5); E("review", "items[0].widget.wrong[1].value", 2)
assert ap(0.5, 2, 0.001) == apl(0.5, 2, 0.001) == 12 and first_n(lambda n: 0.5 ** n * 2 < 0.001) == 11
E("review", "items[5].widget.answer", 12); E("review", "items[5].widget.wrong[0].value", 11)
E("review", "items[5].explain.text", round(4 * 0.5 ** 11, 5)); E("review", "items[5].explain.text", round(4 * 0.5 ** 12, 5))
two('half sin constant', max(abs(0.5 * math.cos(k / 1000)) for k in range(-4000, 4001)), 0.5)
E("review", "items[6].widget.answer", 0.5); E("review", "items[6].widget.wrong[0].value", 1); E("review", "items[6].widget.wrong[1].value", 1.5)
E("review", "items[8].widget.answer", 0.05); E("review", "items[8].widget.wrong[0].value", 0.5); E("review", "items[8].widget.wrong[1].value", 0.1)

# ================= homework =================
gq = lambda x: 1 / (1 + x)
assert ap(4 / 9, 0.5, 1e-6) == apl(4 / 9, 0.5, 1e-6) == 17
x = 1.0; it5 = []
for _ in range(5): x = gq(x); it5.append(x)
assert [round(v, 6) for v in it5] == [0.5, 0.666667, 0.6, 0.625, 0.615385]
x = 1.0; nt = None
for n in range(1, 60):
    x = gq(x)
    if abs(x - gold) < 1e-6: nt = n; break
assert nt == 14
E("homework", "items[1].parts[0].widget.answer", 17); E("homework", "items[1].parts[0].widget.wrong[0].value", 14); E("homework", "items[1].parts[0].widget.wrong[1].value", 15)
E("homework", "items[1].parts[0].explain.text", 0.9)
E("homework", "items[1].parts[1].widget.rows[2][1].answer", 0.6); E("homework", "items[1].parts[1].widget.rows[4][1].answer", round(it5[4], 6))
E("homework", "items[1].parts[2].widget.answer", 14); E("homework", "items[1].parts[2].explain.text", round(gold ** 2, 3))
E("homework", "items[1].parts[3].widget.answer", round(gold, 6))
assert first_n(lambda n: math.pi / 2 - math.atan(n) < 0.05, 1) == 20 == math.floor(1 / math.tan(0.05)) + 1
E("homework", "items[3].widget.answer", 20); E("homework", "items[3].widget.wrong[0].value", 19); E("homework", "items[3].widget.accept", round(1 / math.tan(0.05), 3))
for v in (39, 87, 15, 17, 246): E("homework", "items[4].explain.text", v)
E("homework", "items[4].explain.text", round(125 * q ** 246, 4))
two('min var rho 0', 0.01 / 0.05, min((k / 100000 for k in range(100001)), key=lambda w: vol(w, 0)), 1e-4)
E("homework", "items[6].widget.answer", 0.2); E("homework", "items[6].widget.wrong[0].value", 0.8); E("homework", "items[6].widget.wrong[1].value", round(0.1 / 0.3, 4))


# ================= code widgets: solution passes, starter fails =================
def run_widget(w, code):
    ns = {}
    try:
        exec(w.get('prelude', ''), ns); exec(code, ns)
    except Exception:
        return False
    for t in w['tests']:
        try:
            exec(t.get('setup', '') or '', ns)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); return False
                except Exception as ex:
                    if type(ex).__name__ != t['expect']: return False
                continue
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol', {})
                if not math.isclose(got, want, rel_tol=tol.get('rel', 0 if tol else 1e-9), abs_tol=tol.get('abs', 0 if tol else 1e-12)): return False
            elif got != want:
                return False
        except Exception:
            return False
    return True


widgets = []
def collect(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code': widgets.append(o)
        for v in o.values(): collect(v)
    elif isinstance(o, list):
        for v in o: collect(v)
for f_ in ['l9-open-covers', 'l11-complete-spaces', 'l12-contraction-mapping', 'l13-fixed-point-iteration', 'homework-3']:
    collect(json.load(open(os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology', f_ + '.json'))))
assert len(widgets) == 5
for w_ in widgets:
    if not run_widget(w_, w_['solution']): fails.append('a code solution fails its tests: ' + w_['tests'][0]['call'])
    if run_widget(w_, w_['starter']): fails.append('a code starter passes its tests: ' + w_['tests'][0]['call'])
# stopping-rule margins (Pyodide must land on the same counts)
x = 1.0
for n in range(1, 40):
    xn = math.cos(x); b_ = qq / (1 - qq) * abs(xn - x); x = xn
    if n in (38, 39): print(f'margin cos a posteriori step {n}: {b_:.3e} (tol 1e-6)')

# Review findings 3 and 10: the unguarded l12 loop at q = 1 and q > 1; |sin| reaches 1 on [0, 2]
def _unguarded(q, d01, tol):
    n = 0
    while q ** n / (1 - q) * d01 >= tol: n += 1
    return n
try: _unguarded(1, 1, 0.01); fails.append('l12 unguarded q = 1 did not raise')
except ZeroDivisionError: pass
assert _unguarded(1.5, 1, 0.01) == 0
assert max(abs(math.sin(k / 10000)) for k in range(20001)) > 0.99999999 and 0 < math.pi / 2 < 2
assert abs(0.5 ** 20 * 2 - 1.9e-6) < 5e-8 and 0.5 ** 20 < 1e-6 and 125 * (0.02 / 1.06 * 0 + (1.02 / 1.06) ** 245) > 0.01
lv.check_wrongs()
for f_ in fails: print('FAIL', f_)
if fails: sys.exit(1)
lv.report()
