"""Recompute every number stated in analysis level 5 (Integration and metric spaces) by two routes, and check each at its JSON path.
Run: python3 docs/reports/analysis-L5-numbers.py   (standard library only; exits 0 when every check passes)
Route 1 is exact arithmetic with fractions.Fraction (or a closed form); route 2 is a direct float computation
(brute-force sums, finite differences, grid maxima). `two(name, a, b)` asserts the routes agree; `E` (lv.expect)
checks the stated value appears where it is stated. The script also
  - runs every code widget of the level in CPython: the solution passes its hidden tests and the starter fails one;
  - checks every numeric `wrong[]` value lies outside the answer's band (|wrong - answer| > tol + wrong tol, rule 581),
    and every slider wrong range misses the answer band;
  - checks each expression answer against an independent formula at sample points.
"""
import sys, os, math, json, re
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("analysis", 5)
E = lv.expect
doc = lambda ref: lv._file(ref)[1]
fails = []
def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')
def rounds(name, exact, shown, places):
    if abs(float(exact) - shown) > 0.51 * 10 ** -places:
        fails.append(f'{name}: {float(exact)!r} does not round to {shown}')

def riemann(f, a, b, n, rule):
    w = (b - a) / n
    xs = [a + k * w for k in range(n + 1)]
    pts = xs[1:] if rule == 'right' else xs[:-1]
    return sum(f(x) for x in pts) * w

# ---------------- l20 ----------------
sq = lambda x: x * x
U4, L4 = riemann(sq, F(0), F(1), 4, 'right'), riemann(sq, F(0), F(1), 4, 'left')
two('U4', U4, riemann(sq, 0.0, 1.0, 4, 'right')); two('L4', L4, (0 + 1 + 4 + 9) / 64)
assert U4 == F(15, 32) and L4 == F(7, 32)
E('l20', 'screens[0].widget.rows[4][1].answer', 0.46875); E('l20', 'screens[0].widget.rows[4][2].answer', 0.21875)
E('l20', 'screens[0].feedback.correct', '\\tfrac{15}{32}'); E('l20', 'screens[0].feedback.correct', '\\tfrac{7}{32}')
two('sum tops', sum(F(k, 4) ** 2 for k in range(1, 5)), 1.875); two('sum bottoms', sum(F(k, 4) ** 2 for k in range(4)), 0.875)
E('l20', 'screens[0].widget.rows[4][1].wrong[0].value', 1.875); E('l20', 'screens[0].widget.rows[4][2].wrong[0].value', 0.875)
two('gap4', U4 - L4, 0.25); E('l20', 'screens[0].explain.text', '\\tfrac14')
U10, L10 = riemann(sq, F(0), F(1), 10, 'right'), riemann(sq, F(0), F(1), 10, 'left')
two('U10', U10, 0.385); two('L10', L10, 0.285); two('gap10', U10 - L10, 0.1)
E('l20', 'screens[1].widget.answer', 0.1); E('l20', 'screens[1].widget.wrong[1].value', 0.385); E('l20', 'screens[1].widget.accept', 0.285)
two('square slip', 0.1 ** 2, 0.01); E('l20', 'screens[1].widget.wrong[0].value', 0.01)
for n in range(1, 60):
    Un, Ln = riemann(sq, F(0), F(1), n, 'right'), riemann(sq, F(0), F(1), n, 'left')
    assert Un == F((n + 1) * (2 * n + 1), 6 * n * n) and Ln == F((n - 1) * (2 * n - 1), 6 * n * n) and Un - Ln == F(1, n)
    assert Un == F(1, 3) + F(1, 2 * n) + F(1, 6 * n * n) and Ln == F(1, 3) - F(1, 2 * n) + F(1, 6 * n * n)
two('6n numerators', (2 * 7 ** 2 + 3 * 7 + 1) - (2 * 7 ** 2 - 3 * 7 + 1), 6 * 7)
nmin = next(n for n in range(1, 1000) if F(1, n) < F(1, 100)); two('n gap<0.01', nmin, 101); two('n by ceil', math.floor(1 / 0.01) + 1, 101)
E('l20', 'screens[3].widget.answer', 101); E('l20', 'screens[3].widget.wrong[0].value', 100); E('l20', 'screens[3].widget.wrong[1].value', 10)
rounds('1/101', F(1, 101), 0.0099, 4); E('l20', 'screens[3].feedback.correct', 0.0099)
two('gap20', F(1, 20), 0.05); E('l20', 'screens[3].canvas.state.caption', 0.05)
U2, L2 = riemann(sq, F(0), F(1), 2, 'right'), riemann(sq, F(0), F(1), 2, 'left')
two('U2', U2, 0.625); two('L2', L2, 0.125)
for v in (0.625, 0.46875, 0.125, 0.21875): E('l20', 'screens[4].explain.canvas.caption', v)
inv = lambda x: 1 / x
Ui, Li = riemann(inv, F(1), F(2), 4, 'left'), riemann(inv, F(1), F(2), 4, 'right')
assert Ui == F(319, 420) and Li == F(533, 840)
two('U 1/x', Ui, (1 + 1 / 1.25 + 1 / 1.5 + 1 / 1.75) / 4); two('L 1/x', Li, (1 / 1.25 + 1 / 1.5 + 1 / 1.75 + 0.5) / 4)
rounds('U 1/x', Ui, 0.7595, 4); rounds('L 1/x', Li, 0.6345, 4); rounds('heights', Ui * 4, 3.0381, 4)
assert Ui * 4 == F(319, 105)
two('gap 1/x', Ui - Li, F(1, 4) * (1 - F(1, 2))); assert Ui - Li == F(1, 8)
rounds('ln2', math.log(2), 0.6931, 4); assert Li < math.log(2) < Ui
E('l20', 'screens[5].widget.answer', 0.7595); E('l20', 'screens[5].widget.wrong[0].value', 0.6345); E('l20', 'screens[5].widget.wrong[1].value', 3.0381)
E('l20', 'screens[5].explain.text', 0.6931); E('l20', 'screens[5].explain.text', '\\tfrac{319}{420}'); E('l20', 'screens[5].explain.text', '\\tfrac{533}{840}')
E('l20', 'screens[5].explain.text', '\\tfrac18'); E('l20', 'screens[5].feedback.byKey', '\\tfrac{533}{840}'); E('l20', 'screens[5].feedback.byKey', '\\tfrac{319}{105}')
# uniform continuity of x^2 on [0, 1]: |x^2 - y^2| <= 2|x - y|, delta = eps/2; proof route n >= 201
gridmax = max(abs(a * a - b * b) / abs(a - b) for a in [k / 50 for k in range(51)] for b in [k / 50 + 0.001 for k in range(50)])
assert gridmax <= 2
delta = 0.01 / 2; two('delta', delta, 0.005)
nproof = next(n for n in range(1, 1000) if F(1, n) < F(5, 1000)); two('n proof', nproof, 201); two('n proof 2', math.floor(1 / 0.005) + 1, 201)
E('l20', 'screens[9].explain.text', 0.005); E('l20', 'screens[9].explain.text', 201); E('l20', 'screens[9].explain.text', 101)
E('l20', 'quiz[0].widget.answer', 201); E('l20', 'quiz[0].widget.wrong[0].value', 200); E('l20', 'quiz[0].widget.wrong[1].value', 101)
# Asian option: path 100 -> 110 over a year, 250 fixings
path = lambda t: 100 + 10 * t
gapA = riemann(path, F(0), F(1), 250, 'right') - riemann(path, F(0), F(1), 250, 'left')
two('asian gap', gapA, 10 / 250); two('asian 0.04', gapA, 0.04)
E('l20', 'screens[11].widget.answer', 0.04); E('l20', 'screens[11].widget.wrong[0].value', 10); E('l20', 'screens[11].widget.wrong[1].value', 0.00016)
two('double divide', 10 / 250 / 250, 0.00016)
# quiz: x on [0, 1], five pieces
Ux5, Lx5 = riemann(lambda x: x, F(0), F(1), 5, 'right'), riemann(lambda x: x, F(0), F(1), 5, 'left')
two('U x5', Ux5, (0.2 + 0.4 + 0.6 + 0.8 + 1) * 0.2); two('L x5', Lx5, 0.4)
E('l20', 'quiz[2].widget.answer', 0.6); E('l20', 'quiz[2].widget.wrong[0].value', 0.4); E('l20', 'quiz[2].widget.wrong[1].value', 3)
# spike quiz: U <= 2/n
for n in range(1, 30):
    xs = [F(k, n) for k in range(n + 1)]
    Usp = sum((1 if xs[k] <= F(1, 2) <= xs[k + 1] else 0) * F(1, n) for k in range(n))
    assert Usp <= F(2, n)

# ---------------- l21 ----------------
Fcube = lambda x: x ** 3 / 3
two('strip h=0.1', (Fcube(1.6) - Fcube(1.5)) / 0.1, sum(((1.5 + (k + 0.5) * 1e-5) ** 2) * 1e-5 for k in range(10000)) / 0.1, 1e-7)
rounds('strip 0.1', (F(16, 10) ** 3 - F(15, 10) ** 3) / 3 / F(1, 10), 2.4033, 4)
rounds('strip 0.01', (F(151, 100) ** 3 - F(15, 10) ** 3) / 3 / F(1, 100), 2.2650, 4)
two('f(1.5)', 1.5 ** 2, 2.25); two('F(1.5)', Fcube(F(3, 2)), 1.125)
E('l21', 'screens[0].widget.answer', 2.25); E('l21', 'screens[0].widget.wrong[0].value', 2.4033); E('l21', 'screens[0].widget.wrong[1].value', 1.125)
E('l21', 'screens[0].explain.text', 2.4033); E('l21', 'screens[0].explain.text', '2.2650')
rounds('F(1.6)-F(1.2)', Fcube(F(16, 10)) - Fcube(F(12, 10)), 0.7893, 4); two('M*width', 4 * 0.4, 1.6)
E('l21', 'screens[1].explain.text', 0.7893); E('l21', 'screens[1].explain.text', 1.6)
# chain rule screen: F(x) = sin(x^2), F' = 2x cos(x^2); finite difference check
for x in (0.4, 1.1, 2.3):
    h = 1e-6
    two(f'Fprime {x}', (math.sin((x + h) ** 2) - math.sin((x - h) ** 2)) / (2 * h), 2 * x * math.cos(x * x), 1e-6)
E('l21', 'screens[5].widget.answer', '2x\\cos(x^2)'); two('1.2^2', 1.2 ** 2, 1.44); E('l21', 'screens[5].canvas.state.caption', 1.44)
# jump: F = 0 then x - 1
Fj = lambda x: max(0.0, x - 1)
two('left slope', (Fj(1) - Fj(1 - 1e-6)) / 1e-6, 0); two('right slope', (Fj(1 + 1e-6) - Fj(1)) / 1e-6, 1, 1e-6)
# trap: G = -1/x on [-1, 1]
G = lambda x: -F(1) / x
two('G(1)-G(-1)', G(F(1)) - G(F(-1)), -2); two('odd G', 2 * G(F(1)), -2)
E('l21', 'screens[9].widget.answer', -2); E('l21', 'screens[9].widget.wrong[0].value', 2); E('l21', 'screens[9].widget.wrong[1].value', 0)
d = F(1, 7); two('tail integral', 1 / d - 1, sum(1 / ((float(d) + (k + 0.5) * (1 - float(d)) / 200000) ** 2) * (1 - float(d)) / 200000 for k in range(200000)), 1e-6)
# forward curve
I = lambda T: 0.03 * T + 0.001 * T * T
two('f(5)', (I(5 + 1e-6) - I(5 - 1e-6)) / 2e-6, 0.03 + 0.002 * 5, 1e-7); two('f(5)=0.04', 0.03 + 0.002 * 5, 0.04)
two('avg rate', I(5) / 5, 0.035); two('integral 5', I(5), 0.175); rounds('DF5', math.exp(-I(5)), 0.8395, 4)
E('l21', 'screens[11].widget.answer', 0.04); E('l21', 'screens[11].widget.wrong[0].value', 0.035); E('l21', 'screens[11].widget.wrong[1].value', 0.175)
E('l21', 'screens[11].explain.text', 0.8395); E('l21', 'screens[11].feedback.byKey.avg', '3.5%')
# quiz
for x in (0.5, 1.3):
    h = 1e-4
    Fl = lambda X: sum(math.exp((X + (k + 0.5) * (1 - X) / 4000) ** 2) * (1 - X) / 4000 for k in range(4000))  # int_X^1 e^{t^2} dt
    two(f'lower limit {x}', (Fl(x + h) - Fl(x - h)) / (2 * h), -math.exp(x * x), 1e-3)
E('l21', 'quiz[0].widget.answer', '-e^{x^2}')
two('lipschitz', 3 * 0.2, 0.6); E('l21', 'quiz[1].widget.answer', 0.6); E('l21', 'quiz[1].widget.wrong[0].value', 3); E('l21', 'quiz[1].widget.wrong[1].value', 0.2)
two('int x^2 0..3', F(27, 3), riemann(lambda x: (x + 1.5e-5) ** 2, 0.0, 3.0, 100000, 'left'), 1e-4)
E('l21', 'quiz[3].widget.answer', 9); E('l21', 'quiz[3].widget.wrong[0].value', 27); E('l21', 'quiz[3].widget.wrong[1].value', 6)

# ---------------- l22 ----------------
p, q = (1, 2), (4, 6)
two('euclid', math.hypot(3, 4), math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))); two('euclid 5', math.hypot(3, 4), 5)
two('taxi', sum(abs(a - b) for a, b in zip(p, q)), 7); two('max', max(abs(a - b) for a, b in zip(p, q)), 4)
E('l22', 'screens[0].widget.rows[0][1].answer', 5); E('l22', 'screens[0].widget.rows[1][1].answer', 7); E('l22', 'screens[0].widget.rows[2][1].answer', 4)
E('l22', 'screens[0].widget.rows[0][1].wrong[0].value', 25); E('l22', 'screens[0].widget.rows[2][1].wrong[0].value', 3)
supgap = max(x / 10000 - (x / 10000) ** 2 for x in range(10001)); two('d(x,x^2)', supgap, F(1, 4))
two('area x-x^2', F(1, 2) - F(1, 3), 0.1667, 1e-3)
E('l22', 'screens[4].widget.answer', 0.25); E('l22', 'screens[4].widget.wrong[0].value', 0.5); E('l22', 'screens[4].widget.wrong[1].value', 0.1667)
sqd = lambda x, y: (x - y) ** 2
two('d(0,2)', sqd(0, 2), 4); two('d01+d12', sqd(0, 1) + sqd(1, 2), 2); two('d(0,3)', sqd(0, 3), 9); two('d05+d53', sqd(0, 5) + sqd(5, 3), 29)
E('l22', 'screens[6].prose', 29); E('l22', 'screens[6].prose', 9); E('l22', 'screens[6].widget.options[0].text', 4)
two('|1-(-1)^2|', abs(1 - (-1) ** 2), 0); E('l22', 'screens[7].widget.answer', -1)
A, B, C = (1, -1, 0), (1, 0, -1), (0, 1, -1)
def rho(u, v): return sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))
def rho2(u, v):
    n = len(u); mu, mv = sum(u) / n, sum(v) / n
    su = math.sqrt(sum((a - mu) ** 2 for a in u) / n); sv = math.sqrt(sum((b - mv) ** 2 for b in v) / n)
    return sum((a - mu) * (b - mv) for a, b in zip(u, v)) / n / (su * sv)
for nm, (u, v), r in [('AB', (A, B), 0.5), ('BC', (B, C), 0.5), ('AC', (A, C), -0.5)]:
    two('rho ' + nm, rho(u, v), r); two('rho2 ' + nm, rho2(u, v), r)
dAC = math.sqrt(2 * (1 - rho(A, C)))
unit = lambda u: [a / math.sqrt(sum(b * b for b in u)) for a in u]
two('sqrt3', dAC, math.dist(unit(A), unit(C))); rounds('sqrt3', dAC, 1.732, 3)
two('1-rho AC', 1 - rho(A, C), 1.5); assert 1.5 > 0.5 + 0.5 and dAC <= 1 + 1
two('AB dist', math.sqrt(2 * (1 - rho(A, B))), math.dist(unit(A), unit(B))); two('AB 1', math.sqrt(2 * (1 - rho(A, B))), 1)
E('l22', 'screens[11].widget.answer', 1.732); E('l22', 'screens[11].widget.wrong[0].value', 1.5); E('l22', 'screens[11].widget.wrong[1].value', 3)
E('l22', 'screens[11].canvas.params.rows[2][1]', -0.5)
two('max gap quiz', max(abs(-1 - 2), abs(3 - (-1))), 4); two('taxi quiz', 3 + 4, 7)
E('l22', 'quiz[0].widget.answer', 4); E('l22', 'quiz[0].widget.wrong[0].value', 7); E('l22', 'quiz[0].widget.wrong[1].value', 5)
cube_gap = max(x / 100000 - (x / 100000) ** 3 for x in range(100001)); two('d(x,x^3)', cube_gap, 2 / (3 * math.sqrt(3)), 1e-8)
rounds('d(x,x^3)', 2 / (3 * math.sqrt(3)), 0.385, 3); rounds('1/sqrt3', 1 / math.sqrt(3), 0.577, 3); two('area x-x^3', F(1, 2) - F(1, 4), 0.25)
E('l22', 'quiz[3].widget.answer', 0.385); E('l22', 'quiz[3].widget.wrong[0].value', 0.577); E('l22', 'quiz[3].widget.wrong[1].value', 0.25)
# metric checks behind the quiz claims (exhaustive on small grids)
pts = [k / 4 for k in range(-8, 9)]
def is_metric(P, d, eps=1e-12):
    return all(d(x, y) >= 0 and ((d(x, y) == 0) == (x == y)) and d(x, y) == d(y, x) for x in P for y in P) and \
        all(d(x, z) <= d(x, y) + d(y, z) + eps for x in P for y in P for z in P)
assert is_metric(pts, lambda x, y: math.sqrt(abs(x - y)))
assert is_metric(pts, lambda x, y: 0 if x == y else abs(x) + abs(y))
assert not is_metric([0, 1, 2], sqd)

# ---------------- l23 ----------------
two('r at 0.9', min(0.9, 1 - 0.9), 0.1); E('l23', 'screens[0].widget.answer', 0.1)
rr = 1 - math.sqrt(0.85)
two('disc room', rr, 1 - math.hypot(0.6, 0.7)); rounds('disc room', rr, 0.0780, 4); rounds('|p|', math.sqrt(0.85), 0.9220, 4)
E('l23', 'screens[2].widget.answer', 0.0780); E('l23', 'screens[2].widget.wrong[0].value', 0.9220); E('l23', 'screens[2].widget.wrong[1].value', 0.3)
rounds('ray end x', 0.6 / math.sqrt(0.85), 0.6508, 4); rounds('ray end y', 0.7 / math.sqrt(0.85), 0.7593, 4)
two('square room', min(1 - 0.6, 1 - 0.7), 0.3); two('square room 2', 1 - max(0.6, 0.7), 0.3)
E('l23', 'screens[3].widget.answer', 0.3); E('l23', 'screens[3].widget.wrong[0].value', 0.4); E('l23', 'screens[3].widget.wrong[1].value', 0.0780)
two('q radius', min(4.5 - 2, 5 - 4.5), 0.5); E('l23', 'quiz[0].widget.answer', 0.5); E('l23', 'quiz[0].widget.wrong[0].value', 2.5); E('l23', 'quiz[0].widget.wrong[1].value', 3)
two('q min radius', min(0.3, 0.1), 0.1); E('l23', 'quiz[3].widget.answer', 0.1); E('l23', 'quiz[3].widget.wrong[1].value', 0.4)

# ---------------- l24 ----------------
n24 = next(n for n in range(1, 1000) if F(1, n) < F(1, 100)); two('cover n', n24, 101); rounds('1/101', 1 / 101, 0.0099, 4)
E('l24', 'screens[9].widget.answer', 101); E('l24', 'screens[9].widget.wrong[0].value', 100); E('l24', 'screens[9].widget.wrong[1].value', 10); E('l24', 'screens[9].explain.text', 0.0099)
ret = lambda w2: 0.05 * (1 - w2) + 0.08 * w2
two('sup return', max(ret(k / 10 ** 6) for k in range(1, 10 ** 6)), 0.08, 1e-7); two('equal weight', ret(0.5), 0.065)
assert all(ret(k / 1000) < 0.08 for k in range(1, 1000))
E('l24', 'screens[11].widget.answer', 0.08); E('l24', 'screens[11].widget.wrong[0].value', 0.065); E('l24', 'screens[11].widget.wrong[1].value', 0.05)
n1001 = next(n for n in range(1, 5000) if F(1, n) < F(1, 1000)); two('cover 1001', n1001, 1001)
E('l24', 'quiz[2].widget.answer', 1001); E('l24', 'quiz[2].widget.wrong[0].value', 1000)
two('max x^2 on [-1,2]', max((-1 + 3 * k / 3000) ** 2 for k in range(3001)), 4); E('l24', 'quiz[3].widget.answer', 4)
two('1/sqrt2', 1 / math.sqrt(2), 0.7071, 1e-4)

# ---------------- review ----------------
cube = lambda x: x ** 3
two('r cube U', riemann(cube, F(0), F(1), 2, 'right'), F(9, 16)); two('r cube U float', riemann(cube, 0.0, 1.0, 2, 'right'), 0.5625)
two('r cube L', riemann(cube, F(0), F(1), 2, 'left'), 0.0625); two('r cube tops', F(1, 8) + 1, 1.125)
E('review', 'items[0].widget.answer', 0.5625); E('review', 'items[0].widget.wrong[0].value', 0.0625); E('review', 'items[0].widget.wrong[1].value', 1.125)
for x in (0.7, 1.6):
    h = 1e-6; Hf = lambda X: X ** 3 * math.log(X ** 3) - X ** 3 + 1  # an antiderivative of ln t from 1 to X^3
    two(f'r ftc {x}', (Hf(x + h) - Hf(x - h)) / (2 * h), 3 * x * x * math.log(x ** 3), 1e-5)
    two(f'r ftc 9x2 {x}', 3 * x * x * math.log(x ** 3), 9 * x * x * math.log(x))
E('review', 'items[2].widget.answer', '3x^2\\ln(x^3)')
fstep = lambda t: 2 if t < 1 else -1
two('r step F', riemann(fstep, 0.0, 2.5, 250000, 'left'), 2 - 1.5, 1e-4); two('r step exact', F(2) - F(3, 2), 0.5)
E('review', 'items[3].widget.answer', 0.5); E('review', 'items[3].widget.wrong[0].value', 3.5); E('review', 'items[3].widget.wrong[1].value', -1)
dd = lambda x, y: (x - y) ** 2 + abs(x - y)
two('r d02', dd(0, 2), 6); two('r d01+d12', dd(0, 1) + dd(1, 2), 4); E('review', 'items[4].prose', 6); E('review', 'items[4].prose', 4)
two('r disc', 1 - math.hypot(0.3, 0.4), 0.5); two('r disc sq', 0.3 ** 2 + 0.4 ** 2, 0.25)
E('review', 'items[5].widget.answer', 0.5); E('review', 'items[5].widget.wrong[0].value', 0.6); E('review', 'items[5].widget.wrong[1].value', 0.25)
worst = max(abs(math.sqrt(x / 1000) - math.sqrt(y / 1000)) / math.sqrt(abs(x - y) / 1000) for x in range(0, 1001, 7) for y in range(0, 1001, 11) if x != y)
assert worst <= 1 + 1e-12
two('r root delta', 0.1 ** 2, 0.01); rounds('sqrt 0.1', math.sqrt(0.1), 0.3162, 4)
E('review', 'items[8].widget.answer', 0.01); E('review', 'items[8].widget.wrong[0].value', 0.1); E('review', 'items[8].widget.wrong[1].value', 0.3162)

# ---------------- homework ----------------
lin = lambda x: x
Ul, Ll = riemann(lin, F(0), F(2), 8, 'right'), riemann(lin, F(0), F(2), 8, 'left')
two('h U', Ul, 2.25); two('h L', Ll, 1.75); two('h tops', sum(F(k, 4) for k in range(1, 9)), 9)
E('homework', 'items[0].widget.answer', 2.25); E('homework', 'items[0].widget.wrong[0].value', 1.75); E('homework', 'items[0].widget.wrong[1].value', 9)
for n in range(1, 40):
    assert riemann(lin, F(0), F(2), n, 'right') - riemann(lin, F(0), F(2), n, 'left') == F(4, n)
two('h gap 8', Ul - Ll, 0.5); E('homework', 'items[1].widget.answer', '\\frac{4}{n}'); E('homework', 'items[1].prose', '\\tfrac12')
for x in (0.6, 2.2):
    h = 1e-6; Gf = lambda X: math.log(X * X) - math.log(X)
    two(f'h two limits {x}', (Gf(x + h) - Gf(x - h)) / (2 * h), 1 / x, 1e-6)
E('homework', 'items[2].widget.answer', '\\frac{1}{x}')
gm = max(abs(a + b) for a in [k / 100 for k in range(301)] for b in [k / 100 for k in range(301)]); two('h factor', gm, 6)
two('h delta', 0.03 / 6, 0.005); E('homework', 'items[5].widget.answer', 0.005)
E('homework', 'items[5].widget.wrong[0].value', 0.015); E('homework', 'items[5].widget.wrong[1].value', 0.18); two('h times', 0.03 * 6, 0.18); two('h half', 0.03 / 2, 0.015)
E('homework', 'items[9].model', 201); E('homework', 'items[9].model', 101); E('homework', 'items[9].model', 0.005)
assert sum(r['points'] for r in doc('homework')['items'][9]['rubric']) == 10
# h-which-metrics claims
assert is_metric(pts, lambda x, y: min(1, abs(x - y))) and is_metric(pts, lambda x, y: abs(x ** 3 - y ** 3), 1e-9)
assert not is_metric([0, 1, 2], lambda x, y: abs(x - y) ** 2) and abs(math.sin(0) - math.sin(math.pi)) < 1e-12 and abs(1 - 2 * 1) == 1

# ---------------- code widgets: solution passes, starter fails ----------------
def run_code(widget, src):
    ns = {}
    exec(src, ns)
    ok = True
    for t in widget['tests']:
        if t.get('setup'): exec(t['setup'], ns)
        try:
            got = eval(t['call'], ns); exp = eval(t['expect'], ns)
        except Exception:
            ok = False; continue
        if t.get('compare') == 'isclose':
            good = all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) for a, b in zip(got, exp)) if isinstance(exp, (list, tuple)) else math.isclose(got, exp, rel_tol=1e-9)
        else:
            good = got == exp
        ok = ok and good
    return ok
codes = [('l20', 'screens[10]'), ('l22', 'screens[10]'), ('homework', 'items[7]')]
for ref, path in codes:
    node = doc(ref)
    for key, idx in re.findall(r'(\w+)\[(\d+)\]', path): node = node[key][int(idx)]
    w = node['widget']
    if not run_code(w, w['solution']): fails.append(f'{ref} {path}: solution fails its tests')
    if run_code(w, w['starter']): fails.append(f'{ref} {path}: starter passes its tests')

# ---------------- rule 581: wrong values outside the answer band ----------------
def walk(o, p=''):
    if isinstance(o, dict):
        yield p, o
        for k, v in o.items(): yield from walk(v, f'{p}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f'{p}[{i}]')
bands = 0
for ref in ['l20', 'l21', 'l22', 'l23', 'l24', 'review', 'homework']:
    for p, o in walk(doc(ref)):
        if 'answer' in o and isinstance(o.get('answer'), (int, float)) and isinstance(o.get('wrong'), list):
            ta = o['tol']['abs'] if isinstance(o.get('tol'), dict) else (o.get('tol') or 0)
            for w in o['wrong']:
                if 'value' in w:
                    tw = (w.get('tol') or {}).get('abs', 0); bands += 1
                    if not abs(w['value'] - o['answer']) > ta + tw: fails.append(f'{ref}{p}: wrong {w["id"]} inside the answer band')
                if 'from' in w:
                    bands += 1
                    if w['from'] <= o['answer'] + ta and w['to'] >= o['answer'] - ta: fails.append(f'{ref}{p}: slider range {w["id"]} meets the answer band')
print(f'wrong-value bands checked: {bands}')

if fails:
    print('\n'.join(fails))
lv.report()
sys.exit(1 if fails else 0)
