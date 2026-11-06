"""Recompute every number stated in topology level 1 (Metric spaces revisited) by two routes, and check each at its JSON path.
Run: python3 docs/reports/topology-L1-numbers.py   (standard library only; exits 0 when every check passes)
Route 1 is a closed form or exact arithmetic (fractions); route 2 is independent floating point (a midpoint sum,
bisection, a brute-force search, a Monte Carlo count). `two` asserts the routes agree; `lv.expect` checks the stated,
rounded value appears where it is stated. The script also runs every code widget of the level in CPython: the
solution passes its hidden tests and the starter fails at least one.
"""
import sys, os, math, random, json
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("topology", 1)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def mid(f, a, b, m=200000):
    h = (b - a) / m
    return h * sum(f(a + (k + 0.5) * h) for k in range(m))


def bisect(f, a, b):
    fa = f(a)
    for _ in range(200):
        c = (a + b) / 2
        if (f(c) < 0) == (fa < 0): a, fa = c, f(c)
        else: b = c
    return (a + b) / 2


Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
d1 = lambda p, q: sum(abs(a - b) for a, b in zip(p, q))
d2 = lambda p, q: math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))
di = lambda p, q: max(abs(a - b) for a, b in zip(p, q))
O = (0, 0)


def ball_area_gamma(p): return 4 * math.gamma(1 + 1 / p) ** 2 / math.gamma(1 + 2 / p)


def ball_area_mid(p): return 4 * mid(lambda x: (1 - x ** p) ** (1 / p), 0, 1)


def ball_area_mc(p, n=400000, seed=1):
    r = random.Random(seed); hit = 0
    for _ in range(n):
        x, y = r.uniform(-1, 1), r.uniform(-1, 1)
        if abs(x) ** p + abs(y) ** p < 1: hit += 1
    return 4 * hit / n


# ================= l1 many distances =================
pts = {'p1': (1, 0), 'p2': (0.5, 0.5), 'p3': (-0.3, 0.7), 'p4': (0, -1), 'p5': (0.6, 0.8), 'p6': (1, 1), 'p7': (-0.5, -0.4), 'p8': (0.8, -0.4)}
on = [k for k, p in pts.items() if math.isclose(d1(O, p), 1)]
assert on == ['p1', 'p2', 'p3', 'p4'], on
assert math.isclose(d2(O, pts['p5']), 1) and math.isclose(di(O, pts['p6']), 1)
E("l1", "screens[0].widget.answer", "p4")
for k, v in [('p5', 1.4), ('p6', 2), ('p7', 0.9), ('p8', 1.2)]:
    two(f'd1 {k}', d1(O, pts[k]), v)
    E("l1", f"screens[0].feedback.byKey.{k}", v)
E("l1", "screens[0].hints[2].text", 1.4)
E("l1", "screens[0].hints[2].text", 2)
# screen 1: the shown point (-0.4, -0.6) is on the third-quadrant edge
assert math.isclose(d1(O, (-0.4, -0.6)), 1)
# screen 2: (0,0) to (2,1)
two('d2 (2,1)', d2(O, (2, 1)), math.sqrt(5))
two('d1 (2,1)', d1(O, (2, 1)), 3); two('dinf (2,1)', di(O, (2, 1)), 2)
E("l1", "screens[2].widget.rows[0][2].answer", round(math.sqrt(5), 4))
E("l1", "screens[2].widget.rows[1][2].answer", 3)
E("l1", "screens[2].widget.rows[2][2].answer", 2)
E("l1", "screens[2].widget.rows[0][2].wrong[0].value", 5)
E("l1", "screens[2].explain.text", 2.2361)
# screen 3: d_p ball areas, gamma formula vs midpoint sum vs Monte Carlo
areas = {1: 2, 2: 3.1416, 3: 3.5333, 4: 3.7081}
for p, shown in areas.items():
    g, m = ball_area_gamma(p), ball_area_mid(p)
    two(f'area p={p}', g, m, 1e-6)
    assert abs(ball_area_mc(p) - g) < 0.01, p
    assert round(g, 4) == shown, (p, g)
    E("l1", "screens[3].explain.text", shown)
E("l1", "screens[3].widget.answer", 3.7081)
E("l1", "screens[3].widget.wrong[0].value", 4)
E("l1", "screens[3].widget.wrong[1].value", 3.1416)
E("l1", "screens[3].explain.text", 4)
# screen 4 derive: the example line 2 <= 2.2361 <= 3 <= 4
E("l1", "screens[4].widget.lines[5].text", 2.2361); E("l1", "screens[4].widget.lines[5].text", 4)
# brute-force check of the chain on a grid of pairs
for a in [x / 10 for x in range(-20, 21, 3)]:
    for b in [x / 10 for x in range(-20, 21, 3)]:
        q = (a, b)
        assert di(O, q) <= d2(O, q) + 1e-12 <= d1(O, q) + 2e-12 <= 2 * di(O, q) + 3e-12
# screen 6: largest disc in the diamond = distance to x + y = 1
r_closed = 1 / math.sqrt(2)
r_search = min(d2(O, (t / 10000, 1 - t / 10000)) for t in range(0, 10001))
two('disc in diamond', r_closed, r_search, 1e-6)
E("l1", "screens[6].widget.answer", round(r_closed, 4))
E("l1", "screens[6].widget.wrong[0].value", 1); E("l1", "screens[6].widget.wrong[1].value", 0.5)
E("l1", "screens[6].feedback.byKey.one", round(d1(O, (0.7, 0.7)), 1))
E("l1", "screens[6].explain.text", 0.7071)
# largest square inside the disc: corner (r, r) on the circle
two('square in disc', 1 / math.sqrt(2), bisect(lambda r: d2(O, (r, r)) - 1, 0, 1))
# screen 7: P = (0.5, 0.5, 0.5) and the 3D volumes
P = (0.5, 0.5, 0.5); O3 = (0, 0, 0)
two('P d1', d1(O3, P), 1.5); two('P d2', d2(O3, P), math.sqrt(0.75)); two('P dinf', di(O3, P), 0.5)
E("l1", "screens[7].widget.options[0].why", 1.5)
E("l1", "screens[7].hints[2].text", 0.866)
E("l1", "screens[7].explain.text", 1.5); E("l1", "screens[7].explain.text", 0.866); E("l1", "screens[7].explain.text", 0.5)
vols = {'oct': (F(4, 3), 8 / 6), 'sph': (4 * math.pi / 3, None), 'cube': (8, 2 ** 3)}
two('octahedron volume', vols['oct'][0], 2 ** 3 / math.factorial(3))
r = random.Random(7); n = 300000
mc = sum(1 for _ in range(n) if sum(v * v for v in (r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))) < 1) * 8 / n
assert abs(mc - 4 * math.pi / 3) < 0.03
E("l1", "screens[7].explain.text", F(4, 3)); E("l1", "screens[7].explain.text", round(4 * math.pi / 3, 4)); E("l1", "screens[7].explain.text", 8)
# screen 8 trap: (0.6, 0.6) has d1 = 1.2
two('trap Q', d1(O, (0.6, 0.6)), 1.2)
E("l1", "screens[8].widget.options[1].why", 1.2); E("l1", "screens[8].hints[1].text", 1.2)
# screen 9: p = 0.5
dp = lambda p, q, s: sum(abs(a - b) ** s for a, b in zip(p, q)) ** (1 / s)
two('d_0.5 diag', dp(O, (1, 1), 0.5), 4)
two('d_0.5 legs', dp(O, (1, 0), 0.5) + dp((1, 0), (1, 1), 0.5), 2)
E("l1", "screens[9].widget.answer", 4)
E("l1", "screens[9].widget.wrong[0].value", 2); E("l1", "screens[9].widget.wrong[1].value", 1.4142)
E("l1", "screens[9].explain.text", 4); E("l1", "screens[9].explain.text", 2)
two('star area', ball_area_gamma(0.5), mid(lambda x: (1 - math.sqrt(x)) ** 2, 0, 1) * 4, 1e-6)
E("l1", "screens[9].explain.text", F(2, 3))
# screen 10 code: A = (3, 0), B = (2, 2)
two('A d2', d2(O, (3, 0)), 3); two('B d2', d2(O, (2, 2)), 2 * math.sqrt(2)); two('B d1', d1(O, (2, 2)), 4); two('B dinf', di(O, (2, 2)), 2)
E("l1", "screens[10].explain.text", 2.8284); E("l1", "screens[10].explain.text", 4)
# screen 11 transfer: rebalancing
w0 = [F(40, 100), F(30, 100), F(20, 100), F(10, 100)]; w1 = [F(25, 100), F(35, 100), F(25, 100), F(15, 100)]
D1 = sum(abs(a - b) for a, b in zip(w0, w1)); DI = max(abs(a - b) for a, b in zip(w0, w1)); D2sq = sum((a - b) ** 2 for a, b in zip(w0, w1))
two('rebal d1', D1, d1([0.4, 0.3, 0.2, 0.1], [0.25, 0.35, 0.25, 0.15])); two('rebal dinf', DI, 0.15); two('rebal d2', math.sqrt(D2sq), d2([0.4, 0.3, 0.2, 0.1], [0.25, 0.35, 0.25, 0.15]))
assert D2sq == F(3, 100)
E("l1", "screens[11].widget.rows[0][2].answer", 0.3); E("l1", "screens[11].widget.rows[1][2].answer", 0.15); E("l1", "screens[11].widget.rows[2][2].answer", round(math.sqrt(0.03), 4))
E("l1", "screens[11].feedback.correct", 2000000 * D1); E("l1", "screens[11].feedback.correct", 2000000 * DI)
E("l1", "screens[11].explain.text", 600000); E("l1", "screens[11].explain.text", 300000); E("l1", "screens[11].explain.text", 0.1732)
E("l1", "screens[11].hints[2].text", 0.3)
# quiz
E("l1", "quiz[1].widget.answer", 0.5)
two('quiz square corner', bisect(lambda r: d1(O, (r, r)) - 1, 0, 1), 0.5)
E("l1", "quiz[2].feedback.correct", round(d2(O, (0.6, 0.6)), 3)); E("l1", "quiz[2].feedback.correct", 1.2)
E("l1", "quiz[2].widget.options[1].why", 0.7)
assert d2(O, (0.9, 0.5)) > 1 and math.isclose(d2(O, (0.9, 0.5)) ** 2, 1.06)
two('d3 diag', dp(O, (1, 1), 3), 2 ** (1 / 3))
E("l1", "quiz[3].widget.answer", round(2 ** (1 / 3), 4)); E("l1", "quiz[3].widget.wrong[0].value", 1.4142); E("l1", "quiz[3].widget.wrong[1].value", 2)

# ================= l2 open balls =================
y = (0.3, 0.4)
fits = {'d2': 1 - d2(O, y), 'd1': 1 - d1(O, y), 'di': 1 - di(O, y)}
# independent route: search the largest s whose ball boundary stays inside, by sampling the ball rim
def fit_search(dist, rim, y=y):
    lo, hi = 0.0, 1.0
    for _ in range(50):
        s = (lo + hi) / 2
        ok = all(dist(O, (y[0] + s * u, y[1] + s * v)) < 1 + 1e-12 for u, v in rim)
        lo, hi = (s, hi) if ok else (lo, s)
    return lo
circ = [(math.cos(2 * math.pi * k / 720), math.sin(2 * math.pi * k / 720)) for k in range(720)]
dia = [(c / (abs(c) + abs(s)), s / (abs(c) + abs(s))) for c, s in circ]
sq = [(c / max(abs(c), abs(s)), s / max(abs(c), abs(s))) for c, s in circ]
two('fit d2', fits['d2'], fit_search(d2, circ), 1e-6); two('fit d1', fits['d1'], fit_search(d1, dia), 1e-6); two('fit dinf', fits['di'], fit_search(di, sq), 1e-6)
for i, v in enumerate([0.5, 0.3, 0.6]):
    E("l2", f"screens[0].widget.rows[{i}][2].answer", v)
    E("l2", "screens[0].explain.text", v)
E("l2", "screens[0].widget.rows[1][2].wrong[0].value", 0.7)
E("l2", "screens[2].widget.lines[4].why", 1.8); E("l2", "screens[2].widget.lines[5].why", 0.9)
s_mix = 0.3 / math.sqrt(2)
two('disc in diamond at y', s_mix, min(d2(y, (t / 10000, 1 - t / 10000)) for t in range(10001)), 1e-6)
E("l2", "screens[4].widget.answer", round(s_mix, 4)); E("l2", "screens[4].explain.text", 0.2121)
E("l2", "screens[4].widget.wrong[0].value", 0.3); E("l2", "screens[4].widget.wrong[1].value", 0.5)
E("l2", "screens[9].explain.text", 0.1); E("l2", "screens[9].explain.text", 1.8)
E("l2", "screens[11].widget.rows[0][2].answer", 0.6); E("l2", "screens[11].widget.rows[1][2].answer", 0.3)
E("l2", "screens[11].widget.rows[0][2].wrong[0].value", 0.4); E("l2", "screens[11].widget.rows[1][2].wrong[0].value", 0.7)
E("l2", "screens[11].explain.text", 0.6); E("l2", "screens[11].explain.text", 0.3)
yq = (0.2, 0.5)
two('quiz square room', 1 - di(O, yq), fit_search(di, sq, yq), 1e-6)
E("l2", "quiz[0].widget.answer", 1 - di(O, yq)); E("l2", "quiz[0].widget.wrong[0].value", round(1 - d1(O, yq), 4)); E("l2", "quiz[0].widget.wrong[1].value", 0.8)

# ================= l3 closure, interior, boundary =================
def dist_to_A(p):
    """distance from p to A = open unit disc + segment [1,2] x {0} + {(0, 1.5)}"""
    disc = max(0.0, d2(O, p) - 1)
    t = min(2, max(1, p[0])); seg = d2(p, (t, 0))
    return min(disc, seg, d2(p, (0, 1.5)))
two('(2.5,0) to A', dist_to_A((2.5, 0)), 0.5); two('(0,1.2) to disc', d2(O, (0, 1.2)) - 1, 0.2); two('(0,1.2) to point', d2((0, 1.2), (0, 1.5)), 0.3)
E("l3", "screens[0].feedback.byKey.out", 0.5); E("l3", "screens[0].feedback.byKey.out", 0.4)
E("l3", "screens[0].feedback.byKey.mid", 0.2); E("l3", "screens[0].feedback.byKey.mid", 0.3); E("l3", "screens[0].feedback.byKey.mid", 0.1)
# correlation matrix: eigenvalues 1 + 2 rho and 1 - rho; lower end by a closed form and by bisection on the smallest eigenvalue
def min_eig3(rho):
    # eigenvalues of [[1,r,r],[r,1,r],[r,r,1]] via the characteristic polynomial, by bisection search of the smallest root
    f = lambda lam: (1 - lam) ** 3 - 3 * (1 - lam) * rho ** 2 + 2 * rho ** 3
    lam = bisect(f, -3, min(1 + 2 * rho, 1 - rho) + 1e-9 if rho != 0 else 1 - 1e-9)
    return lam
low = bisect(lambda r: min(1 + 2 * r, 1 - r), -1, 0.5)
two('rho lower', low, -0.5)
two('eig at -0.5', 1 + 2 * -0.5, 0); two('eig2 at -0.5', 1 - (-0.5), 1.5)
E("l3", "screens[9].widget.answer", -0.5); E("l3", "screens[9].widget.wrong[0].value", -1); E("l3", "screens[9].widget.wrong[1].value", round(-1 / 3, 4))
E("l3", "screens[9].feedback.correct", 1.5); E("l3", "screens[9].explain.text", 0); E("l3", "screens[9].explain.text", 1.5)
low10 = bisect(lambda r: 1 + 9 * r, -1, 0.5)
two('rho lower n=10', low10, -1 / 9)
E("l3", "screens[9].explain.text", round(-1 / 9, 4))

# ================= l4 continuity =================
E("l4", "screens[1].widget.answer", 2); E("l4", "screens[1].widget.wrong[0].value", 4); E("l4", "screens[1].widget.wrong[1].value", 1)
two('sqrt 4', bisect(lambda x: x * x - 4, 0, 5), 2)
C = lambda s: 100 * (2 * Phi(s / 2) - 1)
two('C(0.2) bs', C(0.2), 100 * (Phi(0.1) - Phi(-0.1)))
lo_s = bisect(lambda s: C(s) - 7.96, 0.1, 0.3); hi_s = bisect(lambda s: C(s) - 7.98, 0.1, 0.3)
# second route: invert through the normal quantile by Newton on Phi
def qnorm(p):
    x = 0.0
    for _ in range(60):
        x -= (Phi(x) - p) / (math.exp(-x * x / 2) / math.sqrt(2 * math.pi))
    return x
two('lower vol', lo_s, 2 * qnorm((1 + 0.0796) / 2)); two('upper vol', hi_s, 2 * qnorm((1 + 0.0798) / 2))
E("l4", "screens[10].prose", round(C(0.2), 4))
E("l4", "screens[10].widget.answer", round(lo_s, 5)); E("l4", "screens[10].widget.wrong[1].value", round(hi_s, 5))
E("l4", "screens[10].feedback.correct", round(lo_s, 6), fmt="{:.6f}"); E("l4", "screens[10].feedback.correct", round(hi_s, 6), fmt="{:.6f}")
E("l4", "screens[10].explain.text", round(lo_s, 6), fmt="{:.6f}"); E("l4", "screens[10].explain.text", round(hi_s, 6), fmt="{:.6f}")
E("l4", "screens[9].widget.options[0].text", 100.5); E("l4", "screens[9].widget.options[0].text", 101.5)
# f(x, y) = x + y constants: max |f(p)-f(q)| / d over random pairs approaches 1, 2, sqrt 2
r = random.Random(3); best = [0, 0, 0]
for _ in range(20000):
    a, b = (r.uniform(-1, 1), r.uniform(-1, 1)), (r.uniform(-1, 1), r.uniform(-1, 1))
    g = abs(sum(a) - sum(b))
    for k, dd in enumerate((d1, di, d2)): best[k] = max(best[k], g / dd(a, b))
assert best[0] <= 1 + 1e-9 and 1.99 < best[1] <= 2 + 1e-9 and 1.41 < best[2] <= math.sqrt(2) + 1e-9, best

# ================= review =================
q = (3, 1)
two('r1 d2', d2(O, q), math.sqrt(10)); E("review", "items[0].widget.rows[0][1].answer", round(math.sqrt(10), 4))
E("review", "items[0].widget.rows[1][1].answer", d1(O, q)); E("review", "items[0].widget.rows[2][1].answer", di(O, q)); E("review", "items[0].widget.rows[0][1].wrong[0].value", 10)
E("review", "items[0].explain.text", 3.1623)
two('r2 diamond in disc', bisect(lambda r: d2(O, (r, 0)) - 1, 0, 2), 1)
E("review", "items[1].widget.answer", 1); E("review", "items[1].widget.wrong[0].value", 0.7071); E("review", "items[1].widget.wrong[1].value", 0.5)
yr = (-0.2, 0.5)
two('r3 room', 1 - d1(O, yr), fit_search(d1, dia, yr), 1e-6)
E("review", "items[2].widget.answer", 0.3); E("review", "items[2].widget.wrong[0].value", 1 - di(O, yr)); E("review", "items[2].widget.wrong[1].value", d1(O, yr))
E("review", "items[2].explain.text", 0.7)
# r8: 2x - y in d_inf, constant 3 by search
r = random.Random(5); best = 0
for _ in range(20000):
    a, b = (r.uniform(-1, 1), r.uniform(-1, 1)), (r.uniform(-1, 1), r.uniform(-1, 1))
    best = max(best, abs((2 * a[0] - a[1]) - (2 * b[0] - b[1])) / di(a, b))
assert 2.95 < best <= 3 + 1e-9
E("review", "items[7].feedback.correct", 3)

# ================= homework =================
r = random.Random(11); best = [0, 0, 0]
for _ in range(40000):
    a, b = (r.uniform(-1, 1), r.uniform(-1, 1)), (r.uniform(-1, 1), r.uniform(-1, 1))
    g = abs((3 * a[0] - 4 * a[1]) - (3 * b[0] - 4 * b[1]))
    for k, dd in enumerate((di, d1, d2)): best[k] = max(best[k], g / dd(a, b))
assert 6.9 < best[0] <= 7 + 1e-9 and 3.99 < best[1] <= 4 + 1e-9 and 4.99 < best[2] <= 5 + 1e-9, best
for v in (7, 4, 5): E("homework", "items[0].prose", v)
yh = (0.2, 0.1)
edges = [abs(s * yh[0] + t * yh[1] - 1) / math.sqrt(2) for s in (1, -1) for t in (1, -1)]
two('h disc in diamond', min(edges), 0.7 / math.sqrt(2))
two('h disc search', 0.7 / math.sqrt(2), min(d2(yh, (u, v)) for u, v in ((math.cos(2 * math.pi * k / 40000) / (abs(math.cos(2 * math.pi * k / 40000)) + abs(math.sin(2 * math.pi * k / 40000))), math.sin(2 * math.pi * k / 40000) / (abs(math.cos(2 * math.pi * k / 40000)) + abs(math.sin(2 * math.pi * k / 40000)))) for k in range(40000))), 1e-6)
E("homework", "items[2].widget.answer", round(0.7 / math.sqrt(2), 4)); E("homework", "items[2].explain.text", 0.495)
E("homework", "items[2].widget.wrong[0].value", 0.7); E("homework", "items[2].widget.wrong[1].value", round(0.9 / math.sqrt(2), 4))
two('star exact', F(4, 6), 4 * mid(lambda x: (1 - math.sqrt(x)) ** 2, 0, 1), 1e-6)
E("homework", "items[5].widget.answer", 0.6667); E("homework", "items[5].widget.wrong[0].value", 0.1667); E("homework", "items[5].widget.wrong[1].value", 2)
E("homework", "items[5].explain.text", 0.6667)
e = lambda t: t / (1 + t)
c = bisect(lambda t: e(t) - 0.5, 0, 10)
two('bounded metric c', c, 0.5 / (1 - 0.5))
E("homework", "items[6].widget.answer", 1); E("homework", "items[6].widget.wrong[0].value", 0.5); E("homework", "items[6].widget.wrong[1].value", round(0.5 / 1.5, 4))
# longform: max d1/d2 and d2/dinf on R^4 approach 2
r = random.Random(13); m1 = m2 = 0
for _ in range(20000):
    v = [r.uniform(-1, 1) for _ in range(4)]
    m1 = max(m1, d1([0] * 4, v) / d2([0] * 4, v)); m2 = max(m2, d2([0] * 4, v) / di([0] * 4, v))
assert 1.9 < m1 <= 2 + 1e-9 and 1.9 < m2 <= 2 + 1e-9

# ================= code widgets: solution passes, starter fails =================
def run_widget(w, code):
    ns = {}
    try:
        exec(code, ns)
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


code_widgets = []
def collect(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code': code_widgets.append(o)
        for v in o.values(): collect(v)
    elif isinstance(o, list):
        for v in o: collect(v)
for f in ['l1-many-distances', 'homework-1']:
    collect(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'topology', f + '.json'))))
assert len(code_widgets) == 2
for w in code_widgets:
    if not run_widget(w, w['solution']): fails.append('a code solution fails its tests')
    if run_widget(w, w['starter']): fails.append('a code starter passes its tests')
hw_code = code_widgets[1]
ns = {}; exec(hw_code['solution'], ns)
for p, shown in [(1, 2.0), (2, 3.1415928), (3, 3.5332781), (4, 3.7081506)]:
    v = ns['ball_area'](p, 20000)
    assert round(v, 7) == shown, (p, v)
    assert abs(v - ball_area_gamma(p)) < 2e-6
    E("homework", "items[7].explain.text", shown)
E("homework", "items[7].explain.text", round(ns['ball_area'](2, 1), 4))

# Fix pass (review-topology-1-2): the l4 norm chain as an inequality, every homework edge distance, the real p = 4 error.
r2 = math.sqrt(2)
chain_pts = [(1, 0), (0, 1), (-1, 0), (1, 1), (1, -1), (0.3, -0.7), (-2, 0.5), (0.6, 0.8), (5, 5)] + [(math.cos(k / 7), math.sin(k / 7)) for k in range(44)]
for v_ in chain_pts:
    z_ = (0, 0)
    fv = abs(v_[0] + v_[1])
    assert fv <= d1(v_, z_) + 1e-12, v_
    assert d1(v_, z_) <= 2 * di(v_, z_) + 1e-12 and d1(v_, z_) <= r2 * d2(v_, z_) + 1e-12, v_
assert not (2 * di((1, 0), (0, 0)) <= r2 * d2((1, 0), (0, 0))), 'old chain link would hold at (1, 0)'
E("l4", "screens[6].prose", "d_1 \\le 2d_\\infty"); E("l4", "screens[6].prose", "d_1 \\le \\sqrt2")
yh2 = (0.2, 0.1)
edge_d = {(s_, t_): abs(s_ * yh2[0] + t_ * yh2[1] - 1) / r2 for s_ in (1, -1) for t_ in (1, -1)}
assert sorted(round(v_, 4) for v_ in edge_d.values()) == [0.495, 0.6364, 0.7778, 0.9192], edge_d
assert round(edge_d[(1, -1)] * r2, 9) == 0.9 and round(edge_d[(-1, 1)] * r2, 9) == 1.1 and round(edge_d[(-1, -1)] * r2, 9) == 1.3
for v_ in (0.7, 0.9, 1.1, 1.3): E("homework", "items[2].explain.text", v_)
hw1_ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'topology', 'homework-1.json')))
assert 'distance to $x - y = 1$' in hw1_['items'][2]['feedback']['byKey']['other-edge']
errs_ = [abs(ns['ball_area'](p, 20000) - ball_area_gamma(p)) for p in (1, 2, 3, 4)]
assert max(errs_) < 2e-6 and max(errs_) > 1e-6, errs_
E("homework", "items[7].explain.text", "2 \\times 10^{-6}")

# Fix pass: review-1 explanations. The corner (1, 0) of the open diamond B_1(0, r) with r > 1 lies outside the open unit disc.
for r_ in (1.01, 1.5, 3):
    assert d1((1, 0), (0, 0)) < r_ and not d2((1, 0), (0, 0)) < 1
floor_img = {math.floor(x_ / 1000) for x_ in range(-499, 500)}                # f(V) for V = (-0.5, 0.5), f = floor
assert floor_img == {-1, 0}, floor_img

lv.check_wrongs()
for f_ in fails: print('FAIL', f_)
if fails: sys.exit(1)
lv.report()
