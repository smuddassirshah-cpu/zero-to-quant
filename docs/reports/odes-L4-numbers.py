"""odes level 4: recompute every stated number twice and find it at its JSON path.
Route 1 is the closed form or exact arithmetic; route 2 is independent: SciPy quad or solve_ivp, a brute-force
step loop, numpy roots, or a second formula. `stated()` checks both routes against the printed figure, then asks
numbers_lib to find that figure at the path where the lesson states it. Exits 0 when everything matches.
Run: python3 docs/reports/odes-L4-numbers.py
"""
import math, os, sys
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("odes", 4)
bad = []


def stated(ref, path, r1, r2, dp=None, scale=1.0, fmt=None, tol=None, show=None):
    """r1, r2: two routes to the true value. The figure printed is r1*scale rounded to dp places."""
    v = r1 * scale
    t = tol if tol is not None else (0.5 * 10 ** -dp + 1e-12 if dp is not None else 1e-9 * max(1, abs(v)))
    shown = show if show is not None else (round(v, dp) if dp is not None else v)
    ok = abs(r2 * scale - shown) <= t and abs(v - shown) <= t
    if not ok:
        bad.append(f'{ref} {path}: routes {r1!r} and {r2!r} do not give {shown}')
        print('BAD route', ref, path, r1, r2, shown)
    lv.expect(ref, path, shown, fmt=fmt)


def same(ref, path, value, fmt=None):
    """A value already checked twice above, stated again at another path."""
    lv.expect(ref, path, value, fmt=fmt)


def lap(f, s, b=None):
    """Route 2 for a transform: adaptive quadrature to 60/s (the tail beyond is below e^-60 of the scale)."""
    return quad(lambda t: math.exp(-s * t) * f(t), 0, b if b is not None else 60 / s, limit=400)[0]


def ivp(f, y0, T):
    return solve_ivp(f, (0, T), y0, rtol=1e-12, atol=1e-14).y[:, -1]


def euler_loop(f, y0, h, n):
    y = np.array(y0, dtype=float)
    for k in range(n):
        y = y + h * np.asarray(f(k * h, y))
    return y


def rk4_loop(f, y0, h, n):
    y = np.array(y0, dtype=float)
    t = 0.0
    for _ in range(n):
        k1 = np.asarray(f(t, y)); k2 = np.asarray(f(t + h / 2, y + h / 2 * k1))
        k3 = np.asarray(f(t + h / 2, y + h / 2 * k2)); k4 = np.asarray(f(t + h, y + h * k3))
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    return y


def R(z):
    return 1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24


def trap(f, s, T=50, n=200000):
    t = np.linspace(0, T, n + 1); g = np.exp(-s * t) * f(t); h = T / n
    return h * (g.sum() - (g[0] + g[-1]) / 2)


# ---------------- l14 ----------------
pv = lap(lambda t: 1, 0.04)
stated("l14", "screens[0].widget.answer", 1 / 0.04, pv, 0)
stated("l14", "screens[0].widget.wrong[0].value", 1 / 4, 1 / 0.04 / 100, 2)
same("l14", "screens[0].explain.text", 25)
same("l14", "screens[1].prose", 25)
stated("l14", "screens[3].widget.answer", 1 / 2 ** 2, lap(lambda t: t, 2), 2)
stated("l14", "screens[3].widget.wrong[0].value", 1 / 2, lap(lambda t: 1, 2), 1)
stated("l14", "screens[3].widget.wrong[1].value", 2 ** 2, 1 / lap(lambda t: t, 2), 0)
same("l14", "screens[3].explain.text", 0.25)
stated("l14", "screens[4].widget.rows[0][2].answer", 2 / 1 ** 3, lap(lambda t: t * t, 1), 0)
stated("l14", "screens[4].widget.rows[1][2].answer", 3 / (1 + 9), lap(lambda t: math.sin(3 * t), 1, 80), 1)
stated("l14", "screens[4].widget.rows[2][2].answer", 1 / (1 + 4), lap(lambda t: math.cos(2 * t), 1, 80), 1)
same("l14", "screens[4].explain.text", 0.3); same("l14", "screens[4].explain.text", 0.2)
stated("l14", "screens[5].prose", 5 / (0.06 - 0.02), 5 * lap(lambda t: math.exp(0.02 * t), 0.06), 0)
stated("l14", "screens[5].widget.options[0].text", 5 / (0.01 - 0.02), -500.0, 0)
stated("l14", "screens[5].widget.options[1].text", 500, abs(5 / (0.01 - 0.02)), 0)
stated("l14", "screens[5].widget.options[3].text", (5 / 0.01) * (1 / (0.01 - 0.02)), -50000.0, 0)
stated("l14", "screens[6].widget.options[2].why", 11, 11, 0)                      # 10!/s^11
stated("l14", "screens[9].prose", 50, 50, 0)
tv = [trap(lambda t: np.exp(-t), 1), trap(lambda t: t, 2), trap(lambda t: np.sin(3 * t), 1), trap(lambda t: np.cos(2 * t), 1), trap(lambda t: t ** 2, 1)]
for i, (v, ex) in enumerate(zip(tv, [0.5, 0.25, 0.3, 0.2, 2.0])):
    tol = 1e-5 if i == 4 else 1e-6
    ok = abs(v - ex) < tol
    print(('ok ' if ok else 'BAD'), f'trapezium case {i}: {v!r} within {tol} of {ex}')
    if not ok:
        bad.append(f'trapezium {i}')
    lv.expect("l14", f"screens[9].widget.tests[{i}].expect", ex)
stated("l14", "screens[9].widget.tests[5].expect", 5 / (0.06 - 0.02), 125.0, 0)
stated("l14", "screens[9].widget.tests[6].expect", 1 / 0.04, pv, 0)
for i, v in enumerate(tv[:3]):
    if abs(v - [0.5, 0.25, 0.3][i]) >= 1e-7:
        bad.append('feedback says within 1e-7')
same("l14", "screens[9].feedback.correct", 0.5)
same("l14", "screens[9].explain.text", 200000)
claim = 100 * 0.02 / (0.04 + 0.02)
stated("l14", "screens[10].widget.answer", claim, 100 * lap(lambda t: 0.02 * math.exp(-0.02 * t), 0.04), 2)
stated("l14", "screens[10].widget.wrong[0].value", 100 * 0.02 / 0.04, 100 * lap(lambda t: 0.02, 0.04), 0)
stated("l14", "screens[10].widget.wrong[1].value", 100, 100 * quad(lambda t: 0.02 * math.exp(-0.02 * t), 0, np.inf)[0], 0)
same("l14", "screens[10].explain.text", 33.33)
stated("l14", "quiz[0].widget.answer", 1 / (5 - 3), lap(lambda t: math.exp(3 * t), 5), 1)
stated("l14", "quiz[0].widget.wrong[0].value", 1 / (5 + 3), lap(lambda t: math.exp(-3 * t), 5), 3)
stated("l14", "quiz[2].widget.answer", 3 / 25, lap(lambda t: math.sin(3 * t), 4, 40), 2)
stated("l14", "quiz[2].widget.wrong[0].value", 4 / 25, lap(lambda t: math.cos(3 * t), 4, 40), 2)
same("l14", "quiz[2].explain.text", 0.12)

# ---------------- l15 ----------------
y1 = 2 - 2 * math.exp(-2)
stated("l15", "screens[1].widget.answer", y1, ivp(lambda t, y: [4 - 2 * y[0]], [0], 1)[0], 4)
stated("l15", "screens[1].widget.wrong[0].value", 2 - 2 * math.exp(-1), ivp(lambda t, y: [2 - y[0]], [0], 1)[0] * 1, 4)
stated("l15", "screens[1].hints[2].text", math.exp(-2), math.exp(-2.0), 6)
stated("l15", "screens[1].hints[2].text", 2 * math.exp(-2), 2 / math.e ** 2, 6)
same("l15", "screens[1].explain.text", 1.7293, fmt="1.7293")
same("l15", "screens[1].canvas.state.points[0].y", 1.2642)
num_ = np.array([0.06, 0.02]); den = np.array([1, 0.5, 0])
p = np.roots(den); r = np.polyval(num_, p) / np.polyval(np.polyder(den), p)
stated("l15", "screens[2].explain.text", 0.04, float(r[p.argmax()].real), 2)        # residue at 0 is theta
stated("l15", "screens[2].explain.text", 0.02, float(r[p.argmin()].real), 2)        # residue at -0.5 is r0 - theta
p2 = np.roots([1, 3, 2, 0]); r2 = 2 / np.polyval(np.polyder([1, 3, 2, 0]), p2)
for row, pole in enumerate([0, -1, -2]):
    k = int(np.argmin(abs(p2 - pole)))
    cover = 2 / np.prod([pole - q for q in [0, -1, -2] if q != pole])
    stated("l15", f"screens[3].widget.rows[{row}][1].answer", cover, float(r2[k].real), 0)
y2 = 1 - 2 * math.exp(-1) + math.exp(-2)
stated("l15", "screens[3].explain.text", y2, ivp(lambda t, y: [y[1], 2 - 3 * y[1] - 2 * y[0]], [0, 0], 1)[0], 6)
osc = math.exp(-1) * (math.cos(2) + 0.5 * math.sin(2))
osc2 = ivp(lambda t, y: [y[1], -2 * y[1] - 5 * y[0]], [1, 0], 1)[0]
stated("l15", "screens[4].explain.text", osc, osc2, 6)
po = np.roots([1, 2, 5])
stated("l15", "screens[4].canvas.state.points[0].y", 2, float(po.imag.max()), 0)
stated("l15", "screens[4].canvas.state.points[0].x", -1, float(po.real.max()), 0)
stated("l15", "quiz[1].widget.answer", 1 / 3, 1 / (1 + 2), 4)
stated("l15", "quiz[1].widget.wrong[0].value", 1 / (-2 - 1), -1 / 3, 4)
same("l15", "quiz[1].explain.text", 0.3333)
# code tests
stated("l15", "screens[8].widget.tests[0].expect", y1, ivp(lambda t, y: [4 - 2 * y[0]], [0], 1)[0], tol=1e-9)
stated("l15", "screens[8].widget.tests[4].expect", y2, ivp(lambda t, y: [y[1], 2 - 3 * y[1] - 2 * y[0]], [0, 0], 1)[0], tol=1e-9)
stated("l15", "screens[8].widget.tests[5].expect", osc, osc2, tol=1e-9)
vas1 = 0.04 + 0.02 * math.exp(-0.5)
stated("l15", "screens[8].widget.tests[6].expect", vas1, ivp(lambda t, y: [0.5 * (0.04 - y[0])], [0.06], 1)[0], tol=1e-9)
pc = np.roots([1, 2, 5]); rc = np.polyval([1, 2], pc) / np.polyval([2, 2], pc); kk = int(np.argmax(pc.imag))
for part, want in [(rc[kk].real, 0.5), (rc[kk].imag, -0.25)]:
    if abs(part - want) > 1e-12:
        bad.append('complex residue')
lv.expect("l15", "screens[8].widget.tests[3].expect", "(0.5-0.25j)")
fl = 0.04 / 0.05 + 0.02 / 0.55
fl2 = lap(lambda t: 0.04 + 0.02 * math.exp(-0.5 * t), 0.05)
stated("l15", "screens[9].widget.answer", fl, fl2, 4)
stated("l15", "screens[9].widget.wrong[0].value", 0.04 / 0.05, lap(lambda t: 0.04, 0.05), 1)
stated("l15", "screens[9].hints[2].text", 0.02 / 0.55, lap(lambda t: 0.02 * math.exp(-0.5 * t), 0.05), 6)
same("l15", "screens[9].explain.text", 0.8364)

# ---------------- l16 ----------------
stated("l16", "screens[0].widget.rows[1][1].answer", 1 + 0.5, euler_loop(lambda t, y: y, [1.0], 0.5, 1)[0], 1)
stated("l16", "screens[0].widget.rows[2][1].answer", 1.5 ** 2, euler_loop(lambda t, y: y, [1.0], 0.5, 2)[0], 2)
stated("l16", "screens[0].explain.text", math.e, math.exp(1.0), 6)
stated("l16", "screens[0].explain.text", math.e - 2.25, math.exp(1) - euler_loop(lambda t, y: y, [1.0], 0.5, 2)[0], 2)
q = 1.25 ** 4
stated("l16", "screens[1].widget.answer", q, euler_loop(lambda t, y: y, [1.0], 0.25, 4)[0], 4)
stated("l16", "screens[1].explain.text", math.e - q, math.exp(1) - euler_loop(lambda t, y: y, [1.0], 0.25, 4)[0], 2)
m = (1 + 0.05 / 12) ** 12
stated("l16", "screens[2].widget.answer", m, euler_loop(lambda t, y: 0.05 * y, [1.0], 1 / 12, 12)[0], 6)
stated("l16", "screens[2].widget.wrong[0].value", math.exp(0.05), ivp(lambda t, y: [0.05 * y[0]], [1.0], 1)[0], 6)
stated("l16", "screens[2].hints[1].text", 1 + 0.05 / 12, 1.0041666667, 7)
E = {h: math.e - (1 + h) ** round(1 / h) for h in [0.1, 0.05, 0.025, 0.0125, 0.01]}
E2 = {h: math.exp(1) - euler_loop(lambda t, y: y, [1.0], h, round(1 / h))[0] for h in E}
for h, j in [(0.1, None), (0.05, None), (0.01, None)]:
    stated("l16", "screens[3].prose", E[h], E2[h], 6)
stated("l16", "screens[3].widget.answer", E[0.1] / E[0.05], E2[0.1] / E2[0.05], 2)
stated("l16", "screens[3].widget.wrong[1].value", E[0.05] / E[0.1], E2[0.05] / E2[0.1], 2)
hs = [0.1, 0.05, 0.025, 0.0125]
sl = np.polyfit(np.log(hs), np.log([E[h] for h in hs]), 1)[0]
sl2 = (math.log(E2[0.0125]) - math.log(E2[0.1])) / (math.log(0.0125) - math.log(0.1))
stated("l16", "screens[3].explain.text", sl, sl, 3)
if abs(sl2 - sl) > 0.02:
    bad.append('order slope routes')
vq = 0.04 + 0.02 * (1 - 0.125) ** 4
vq2 = euler_loop(lambda t, y: 0.5 * (0.04 - y), [0.06], 0.25, 4)[0]
stated("l16", "screens[4].widget.answer", vq, vq2, 6)
stated("l16", "screens[4].widget.wrong[1].value", vas1, ivp(lambda t, y: [0.5 * (0.04 - y[0])], [0.06], 1)[0], 6)
stated("l16", "screens[4].widget.wrong[0].value", 0.06 + 0.5 * (0.04 - 0.06), euler_loop(lambda t, y: 0.5 * (0.04 - y), [0.06], 1, 1)[0], 2)
for k, path, shown in [(1, "screens[4].hints[0].text", 5.75), (2, "screens[4].hints[1].text", 5.5313), (3, "screens[4].hints[1].text", 5.3398), (4, "screens[4].hints[2].text", 5.1724)]:
    # 5.53125 exactly: printed half-up as 5.5313
    stated("l16", path, 0.04 + 0.02 * 0.875 ** k, euler_loop(lambda t, y: 0.5 * (0.04 - y), [0.06], 0.25, k)[0], 4, scale=100, show=shown, tol=0.00005 + 1e-9)
stated("l16", "screens[4].prose", vas1, vas1, 4, scale=100)
vm = 0.04 + 0.02 * (1 - 0.5 / 12) ** 12
stated("l16", "screens[4].explain.text", vm, euler_loop(lambda t, y: 0.5 * (0.04 - y), [0.06], 1 / 12, 12)[0], 4, scale=100)
rad = math.sqrt(1.01) ** 63
rad2 = float(np.hypot(*euler_loop(lambda t, z: np.array([z[1], -z[0]]), [1.0, 0.0], 0.1, 63)))
stated("l16", "screens[5].widget.answer", rad, rad2, 4)
stated("l16", "screens[5].widget.wrong[1].value", 1.01 ** 63, rad2 ** 2, 4)
same("l16", "screens[5].explain.text", 1.3681)
st = (1 - 10 * 0.25) ** 4
stated("l16", "screens[6].widget.answer", st, euler_loop(lambda t, y: -10 * y, [1.0], 0.25, 4)[0], 4)
stated("l16", "screens[6].widget.wrong[1].value", -st, -euler_loop(lambda t, y: -10 * y, [1.0], 0.25, 4)[0], 4)
stated("l16", "screens[6].explain.text", math.exp(-10), ivp(lambda t, y: [-10 * y[0]], [1.0], 1)[0], 7)
for i in range(5):
    stated("l16", f"screens[6].canvas.params.series[1].values[{i}]", (1 - 2.5) ** i, euler_loop(lambda t, y: -10 * y, [1.0], 0.25, i)[0], tol=1e-12)
stated("l16", "screens[7].widget.answer", 2 / 10, brentq(lambda h: abs(1 - 10 * h) - 1, 0.15, 0.3), 1)
stated("l16", "screens[7].prose", 1 - 10 * 0.05, 0.5, 1)
stated("l16", "screens[8].widget.tests[0].expect", 1.1 ** 10, euler_loop(lambda t, y: y, [1.0], 0.1, 10)[0], tol=1e-9)
stated("l16", "screens[8].widget.tests[3].expect", rad, rad2, tol=1e-9)
stated("l16", "screens[8].widget.tests[6].expect", sl, sl, tol=1e-9)
stated("l16", "screens[8].widget.tests[7].expect", math.log(0.01 / 0.0025) / math.log(2), 2.0, tol=1e-12)
same("l16", "screens[8].feedback.correct", 1.368117)
Lm = 200000 - 100000 * 1.005 ** 12
Lm2 = euler_loop(lambda t, L: 0.06 * L - 12000, [100000.0], 1 / 12, 12)[0]
Lc = 200000 - 100000 * math.exp(0.06)
stated("l16", "screens[9].widget.answer", Lm, Lm2, 2)
stated("l16", "screens[9].widget.wrong[0].value", Lc, ivp(lambda t, L: [0.06 * L[0] - 12000], [100000.0], 1)[0], 2, tol=0.006)
stated("l16", "screens[9].hints[2].text", 1.005 ** 12, (1 + 0.06 / 12) ** 12, 7)
stated("l16", "screens[9].explain.text", Lm - Lc, Lm2 - Lc, 2)
stated("l16", "quiz[0].widget.answer", 1 + 0.1 * (0 + 1), euler_loop(lambda t, y: t + y, [1.0], 0.1, 1)[0], 1)
stated("l16", "quiz[0].widget.wrong[0].value", 1.01 / 0.9, brentq(lambda y: y - 1 - 0.1 * (0.1 + y), 1, 2), 4)
stated("l16", "quiz[2].widget.answer", 2 / 50, brentq(lambda h: abs(1 - 50 * h) - 1, 0.03, 0.06), 2)
stated("l16", "quiz[3].prose" if False else "quiz[3].question", math.e - 1.02 ** 50, math.exp(1) - euler_loop(lambda t, y: y, [1.0], 0.02, 50)[0], 3)
stated("l16", "quiz[3].explain.text", E[0.01], E2[0.01], 6)

# ---------------- l17 ----------------
mid10 = (1 + 0.1 + 0.005) ** 10
mid10b = 1.0
for _ in range(10):
    mid10b = mid10b + 0.1 * (mid10b + 0.05 * mid10b)
stated("l17", "screens[0].widget.answer", 1 + 0.1 * 1.05, 1.105, 3)
stated("l17", "screens[0].explain.text", mid10, mid10b, 6)
stated("l17", "screens[0].explain.text", math.e - mid10, math.e - mid10b, 6)
stated("l17", "screens[0].explain.text", E[0.1], E2[0.1], 6)
stated("l17", "screens[1].widget.answer", R(0.5) ** 2, rk4_loop(lambda t, y: y, [1.0], 0.5, 2)[0], 4)
stated("l17", "screens[1].hints[2].text", R(0.5), rk4_loop(lambda t, y: y, [1.0], 0.5, 1)[0], 7)
k1, k2 = 1.0, 1 + 0.05 * 1.0
k3 = 1 + 0.05 * k2; k4 = 1 + 0.1 * k3
stated("l17", "screens[2].widget.rows[1][1].answer", k2, 1.05, 2)
stated("l17", "screens[2].widget.rows[2][1].answer", k3, 1.0525, 4)
stated("l17", "screens[2].widget.rows[3][1].answer", k4, 1.10525, 5)
y1rk = 1 + 0.1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
stated("l17", "screens[2].widget.rows[4][1].answer", y1rk, R(0.1), 7)
stated("l17", "screens[2].explain.text", y1rk, rk4_loop(lambda t, y: y, [1.0], 0.1, 1)[0], 10)
stated("l17", "screens[2].explain.text", k1 + 2 * k2 + 2 * k3 + k4, 6 * (R(0.1) - 1) / 0.1 + 0, 5)
e10 = math.e - R(0.1) ** 10; e20 = math.e - R(0.05) ** 20
e10b = math.e - rk4_loop(lambda t, y: y, [1.0], 0.1, 10)[0]; e20b = math.e - rk4_loop(lambda t, y: y, [1.0], 0.05, 20)[0]
stated("l17", "screens[3].prose", R(0.1) ** 10, rk4_loop(lambda t, y: y, [1.0], 0.1, 10)[0], 7)
stated("l17", "screens[3].prose", e10, e10b, 3, scale=1e6, fmt="2.084")
stated("l17", "screens[3].prose", e20, e20b, 3, scale=1e7, fmt="1.358")
stated("l17", "screens[3].widget.answer", e10 / e20, e10b / e20b, 2)
same("l17", "screens[3].explain.text", 15.35)
stated("l17", "screens[4].prose", E[0.1] * 0 + (math.e - (1 + 1e-5) ** 100000), math.exp(1) - (1 + 1e-5) ** 100000, 2, scale=1e5, fmt="1.36")
stated("l17", "screens[4].widget.answer", 100000 / (4 * 10), 2500, 0)
stated("l17", "screens[4].widget.wrong[0].value", 100000 / 10, 10000, 0)
stated("l17", "screens[4].explain.text", e10, e10b, 2, scale=1e6, fmt="2.08")
same("l17", "screens[4].explain.text", 2500)
if not abs(math.e - R(0.5) ** 2) < 0.001:
    bad.append('l17 explore: within 0.001 of e')
same("l17", "screens[1].explain.text", 0.001)
g = abs(complex(R(0.1j)))
rk_rad = float(np.hypot(*rk4_loop(lambda t, z: np.array([z[1], -z[0]]), [1.0, 0.0], 0.1, 63)))
stated("l17", "screens[5].widget.options[0].text", g ** 63, rk_rad, 7)
stated("l17", "screens[5].explain.text", 1 - g, 1 - math.sqrt(1 - 0.1 ** 6 / 72 + 0.1 ** 8 / 576), 1, scale=1e9, fmt="6.9")
same("l17", "screens[5].prose", 1.3681)
hsb = [0.1, 0.05, 0.025, 0.0125]
def bug(h):
    y = 1.0
    for _ in range(round(1 / h)):
        a = y; b = y + h / 2 * a; c = y + h / 2 * a; d = y + h * c
        y = y + h / 6 * (a + 2 * b + 2 * c + d)
    return y
eb = [math.e - bug(h) for h in hsb]
ob = np.polyfit(np.log(hsb), np.log(eb), 1)[0]
ob2 = (math.log(eb[-1]) - math.log(eb[0])) / (math.log(hsb[-1]) - math.log(hsb[0]))
stated("l17", "screens[6].prose", ob, ob2, 2, tol=0.01)
stated("l17", "screens[6].canvas.params.lines[7]", ob, ob, 3)
stated("l17", "screens[6].prose", bug(0.1), bug(0.1), 5)
zl = brentq(lambda z: abs(R(-z)) - 1, 2, 3)
zl2 = brentq(lambda z: abs(1 - z + z * z / 2 - z ** 3 / 6 + z ** 4 / 24) - 1, 2.5, 2.9)
stated("l17", "screens[7].prose", R(-2.5), rk4_loop(lambda t, y: -y, [1.0], 2.5, 1)[0], 4)
stated("l17", "screens[7].prose", R(-3), rk4_loop(lambda t, y: -y, [1.0], 3, 1)[0], 3)
stated("l17", "screens[7].prose", zl, zl2, 4)
stated("l17", "screens[7].widget.answer", zl / 10, zl2 / 10, 4)
stated("l17", "screens[7].explain.text", zl / 2, zl2 / 2, 1)
stated("l17", "screens[8].widget.answer", math.log2(8), 3, 0)
stated("l17", "screens[9].widget.tests[0].expect", R(0.1), rk4_loop(lambda t, y: y, [1.0], 0.1, 1)[0], tol=1e-12)
stated("l17", "screens[9].widget.tests[1].expect", R(0.1) ** 10, rk4_loop(lambda t, y: y, [1.0], 0.1, 10)[0], tol=1e-9)
stated("l17", "screens[9].widget.tests[3].expect", 1 ** 4 / 4, rk4_loop(lambda t, y: t ** 3, [0.0], 0.5, 2)[0], tol=1e-12)
ro7 = rk4_loop(lambda t, z: np.array([z[1], -2 * z[1] - 5 * z[0]]), [1.0, 0.0], 1 / 7, 7)[0]
ro6 = rk4_loop(lambda t, z: np.array([z[1], -2 * z[1] - 5 * z[0]]), [1.0, 0.0], 1 / 6, 6)[0]
ro5 = rk4_loop(lambda t, z: np.array([z[1], -2 * z[1] - 5 * z[0]]), [1.0, 0.0], 1 / 5, 5)[0]
stated("l17", "screens[9].widget.tests[4].expect", ro7, ro7, tol=1e-9)
if not (abs(ro7 - osc2) < 5e-5 and abs(ro6 - osc2) >= 5e-5 and abs(ro5 - osc2) >= 5e-5):
    bad.append('seven RK4 steps is the smallest count for the oscillator')
stated("l17", "screens[9].widget.tests[7].expect", g ** 63, rk_rad, tol=1e-9)
stated("l17", "screens[9].widget.tests[8].expect", R(-3), 1.375, tol=1e-12)
same("l17", "screens[9].prose", 0.014164)
for i, t in enumerate([1, 2, 0.5, 3]):
    stated("l17", f"screens[10].widget.tests[{i}].expect", math.exp(-t) * (math.cos(2 * t) + 0.5 * math.sin(2 * t)),
           ivp(lambda s, y: [y[1], -2 * y[1] - 5 * y[0]], [1, 0], t)[0], tol=1e-9)
stated("l17", "screens[11].widget.answer", math.ceil(40 / zl), math.ceil(40 / zl2), 0)
stated("l17", "screens[11].widget.wrong[1].value", math.floor(40 / zl), 14, 0)
stated("l17", "screens[11].explain.text", 40 / zl, 40 / zl2, 2)
stated("l17", "screens[11].feedback.byKey.floor", 40 / 14, 40 / 14, 3)
stated("l17", "quiz[0].widget.answer", R(-0.1), rk4_loop(lambda t, y: -y, [1.0], 0.1, 1)[0], 6)
stated("l17", "quiz[1].widget.answer", 1 + 0.2 * 1.1, 1.22, 2)
stated("l17", "quiz[3].explain.text", R(-3), 1.375, 3)

# ---------------- l18 ----------------
k, th, r0, T = 0.5, 0.04, 0.06, 5.0
B = (1 - math.exp(-k * T)) / k
I = th * T + (r0 - th) * B
I2 = quad(lambda t: th + (r0 - th) * math.exp(-k * t), 0, T)[0]
D = math.exp(-I)
sysf = lambda t, y: [k * (th - y[0]), y[0]]
D2 = math.exp(-ivp(sysf, [r0, 0.0], T)[1])
stated("l18", "screens[0].widget.answer", 100 * D, 100 * D2, 2)
stated("l18", "screens[0].widget.wrong[0].value", 100 * math.exp(-th * T), 100 * math.exp(-quad(lambda t: th, 0, T)[0]), 2)
stated("l18", "screens[0].widget.wrong[1].value", 100 * math.exp(-r0 * T), 100 * math.exp(-quad(lambda t: r0, 0, T)[0]), 2)
stated("l18", "screens[0].explain.text", I, I2, 6)
stated("l18", "screens[0].explain.text", 100 * D, 100 * D2, 4)
stated("l18", "screens[1].widget.answer", B, quad(lambda t: math.exp(-k * t), 0, T)[0], 6)
stated("l18", "screens[1].widget.wrong[0].value", B / 2, (1 - math.exp(-2.5)) / 1, 6)
stated("l18", "screens[1].hints[1].text", math.exp(-2.5), math.exp(-k * T), 6)
stated("l18", "screens[1].explain.text", D, D2, 6)

def eul_D(n):
    y = euler_loop(lambda t, y: np.array([k * (th - y[0]), y[0]]), [r0, 0.0], T / n, n)
    return math.exp(-y[1])

def eul_D_formula(n):
    return math.exp(-(0.2 + 0.04 * (1 - (1 - 2.5 / n) ** n)))

for n, path in [(10, "screens[2].widget.answer"), (100, "screens[2].explain.text"), (1000, "screens[2].explain.text")]:
    stated("l18", path, eul_D(n), eul_D_formula(n), 6)
n163 = next(n for n in range(1, 400) if abs(eul_D(n) - D) < 5e-5)
stated("l18", "screens[3].widget.answer", n163, next(n for n in range(1, 400) if abs(eul_D_formula(n) - D) < 5e-5), 0)
stated("l18", "screens[3].explain.text", 1e6 * (D - eul_D(162)), 1e6 * (D - eul_D_formula(162)), 2)
stated("l18", "screens[3].explain.text", 1e6 * (D - eul_D(163)), 1e6 * (D - eul_D_formula(163)), 2)
stated("l18", "screens[3].widget.wrong[0].value", 100, 100, 0)
stated("l18", "screens[3].feedback.byKey.hundred", 1e6 * (D - eul_D(100)), 1e6 * (D - eul_D_formula(100)), 0)

def rk_D(n):
    return math.exp(-rk4_loop(lambda t, y: np.array([k * (th - y[0]), y[0]]), [r0, 0.0], T / n, n)[1])

def rk_D2(n):   # route 2: RK4 on a linear system is the matrix polynomial P(hA) per step, on z = (r, I, 1)
    A = np.array([[-k, 0, k * th], [1, 0, 0], [0, 0, 0]]); M = (T / n) * A
    P = np.eye(3) + M + M @ M / 2 + M @ M @ M / 6 + M @ M @ M @ M / 24
    z = np.linalg.matrix_power(P, n) @ np.array([r0, 0.0, 1.0])
    return math.exp(-z[1])

for row, n in enumerate([1, 2, 4, 8]):
    stated("l18", f"screens[4].canvas.params.rows[{row}][1]", rk_D(n), rk_D2(n), 6)
    e6 = 1e6 * abs(rk_D(n) - D)
    e6b = 1e6 * abs(rk_D2(n) - D2)
    dp = 0 if e6 > 100 else (1 if e6 > 1 else 2)
    stated("l18", f"screens[4].canvas.params.rows[{row}][2]", e6, e6b, dp)
if not (abs(rk_D2(4) - D) < 5e-5 and abs(rk_D2(2) - D) >= 5e-5):
    bad.append('RK4 four steps, second route')
stated("l18", "screens[4].widget.answer", next(n for n in [1, 2, 4, 8] if abs(rk_D(n) - D) < 5e-5), next(n for n in [1, 2, 4, 8] if abs(rk_D2(n) - D) < 5e-5), 0)
stated("l18", "screens[4].explain.text", rk_D(4), rk_D(4), 6)
stated("l18", "screens[4].explain.text", 50 / (1e6 * abs(rk_D(4) - D)), 50 / (1e6 * abs(rk_D(4) - D)), 1)
stated("l18", "screens[4].explain.text", abs(rk_D(10) - D), abs(rk_D(10) - D2), 1, scale=1e7, fmt="2.6")
for n, e in [(2, 618.0), (4, 1964.6), (8, 1015.1), (16, 508.2), (32, 253.7)]:
    stated("l18", "screens[5].canvas.state.points", 1e6 * (D - eul_D(n)), 1e6 * (D - eul_D_formula(n)), 1)
stated("l18", "screens[5].prose", D - eul_D(2), D - eul_D_formula(2), 5)
stated("l18", "screens[5].prose", D - eul_D(4), D - eul_D_formula(4), 5)
stated("l18", "screens[5].widget.options[2].why", 2.5 * 0.5, 1.25, 2)
stated("l18", "screens[5].widget.options[2].why", 1 - 1.25, -0.25, 2)
stated("l18", "screens[6].prose", eul_D(60), eul_D_formula(60), 6)
stated("l18", "screens[6].prose", 100 * eul_D(60), 100 * eul_D_formula(60), 4)
stated("l18", "screens[6].widget.options[0].text", D - eul_D(60), D - eul_D_formula(60), 2, scale=1e4, fmt="1.35")
stated("l18", "screens[6].widget.options[3].why", 0.5 / 12, k / 12, 4)
stated("l18", "screens[6].explain.text", n163, n163, 0)
stated("l18", "screens[6].canvas.params.rows[1][2]", round(eul_D(60), 4), round(eul_D_formula(60), 4), 4)
sig = 0.01
var = sig ** 2 / k ** 2 * (T - 2 * B + (1 - math.exp(-2 * k * T)) / (2 * k))
A = (th - sig ** 2 / (2 * k * k)) * (B - T) - sig ** 2 * B * B / (4 * k)
Pn, Pn2 = math.exp(-I + var / 2), math.exp(A - B * r0)
stated("l18", "screens[7].prose", var / 2 / sig ** 2, 0.5 * (T - 2 * B + (1 - math.exp(-5)) / 1) / k ** 2, 3)
stated("l18", "screens[7].prose", Pn, Pn2, 6)
stated("l18", "screens[7].prose", 100 * Pn, 100 * Pn2, 4)
stated("l18", "screens[7].widget.answer", 100 * (Pn - D), 100 * (Pn2 - D2), 4)
same("l18", "screens[7].canvas.params.functions[0].expr", 4.643204)
for i, (args, val) in enumerate([((0.06, 0.5, 0.04, 5), None), (None, None), ((0.04, 0.5, 0.04, 5), None), ((0.02, 1.0, 0.05, 3), None)]):
    if args is None:
        continue
    a, kk_, tt, TT = args
    ex1 = math.exp(-(tt * TT + (a - tt) * (1 - math.exp(-kk_ * TT)) / kk_))
    ex2 = math.exp(-ivp(lambda t, y: [kk_ * (tt - y[0]), y[0]], [a, 0.0], TT)[1])
    stated("l18", f"screens[9].widget.tests[{i}].expect", ex1, ex2, tol=1e-9)
stated("l18", "screens[9].widget.tests[4].expect", rk_D(4), rk_D(4), tol=1e-12)
stated("l18", "screens[9].widget.tests[6].expect", D, rk_D(50), tol=1e-9)
def steps(method):
    n = 1
    while abs(method(n) - D) >= 5e-5:
        n *= 2
    return n
stated("l18", "screens[9].widget.tests[7].expect", steps(rk_D), steps(rk_D2), 0)
stated("l18", "screens[9].widget.tests[8].expect", steps(eul_D), steps(eul_D_formula), 0)
for i, args in enumerate([(0.06, 0.5, 0.04, 5), (0.04, 0.5, 0.04, 5), (0.02, 1.0, 0.05, 3), (0.1, 2.0, 0.03, 10)]):
    a, kk_, tt, TT = args
    ex1 = math.exp(-(tt * TT + (a - tt) * (1 - math.exp(-kk_ * TT)) / kk_))
    ex2 = math.exp(-ivp(lambda t, y: [kk_ * (tt - y[0]), y[0]], [a, 0.0], TT)[1])
    stated("l18", f"screens[10].widget.tests[{i}].expect", ex1, ex2, tol=1e-9)
same("l18", "screens[10].canvas.params.lines[1]", 1.78e-12)    # measured in Pyodide 0.27.7 (SciPy 1.14.1) and CPython (SciPy 1.18.1)
for row, n, e in [(1, 2, 3.9e-4), (2, 4, 1.4e-5), (3, 8, 6.7e-7)]:
    stated("l18", f"screens[11].canvas.params.lines[{row}]", rk_D(n), rk_D2(n), 6)
    stated("l18", f"screens[11].canvas.params.lines[{row}]", abs(rk_D(n) - D), abs(rk_D2(n) - D2), show=e, tol=e * 0.05)
stated("l18", "quiz[0].widget.answer", math.exp(-0.25), math.exp(-quad(lambda t: 0.05, 0, 5)[0]), 4)
for i, v in [(0, 0.78918), (1, 0.789134), (2, 0.78908), (3, 0.78929)]:
    lv.expect("l18", f"quiz[1].widget.options[{i}].text", v, fmt='{:.6f}')
stated("l18", "quiz[1].widget.options[1].why", D - eul_D(100), D - eul_D_formula(100), 1, scale=1e5, fmt="8.1")
stated("l18", "quiz[1].widget.options[3].why", 0.789290 - D, 0.78929 - D2, 1, scale=1e5, fmt="7.5")
stated("l18", "quiz[1].feedback.correct", D - 0.78918, D2 - 0.78918, 1, scale=1e5, fmt="3.5")
if not (abs(0.78918 - D) < 5e-5 and min(abs(v - D) for v in [0.789134, 0.78908, 0.78929]) >= 5e-5):
    bad.append('quiz band options')
stated("l18", "quiz[2].widget.answer", 100 * 8.1 / 4, 100 * (D - eul_D(100)) / 4e-5, show=200, tol=10)   # "about 200", widget tol 10
stated("l18", "quiz[3].explain.text", abs(rk_D(8) - D), abs(rk_D(8) - D2), 1, scale=1e7, fmt="6.7")

# ---------------- review-4 ----------------
stated("review", "items[0].widget.answer", 6 / 2 ** 4, lap(lambda t: t ** 3, 2), 3)
stated("review", "items[0].widget.wrong[0].value", 1 / 2 ** 4, lap(lambda t: t ** 3, 2) / 6, 4)
stated("review", "items[1].widget.answer", 2 / (0.05 - 0.03), lap(lambda t: 2 * math.exp(0.03 * t), 0.05), 0)
stated("review", "items[1].widget.wrong[0].value", 2 / 0.08, lap(lambda t: 2 * math.exp(-0.03 * t), 0.05), 0)
ry = 2 * math.exp(-1) - math.exp(-2)
pr = np.roots([1, 3, 2]); rr = np.polyval([1, 3], pr) / np.polyval([2, 3], pr)
ry2 = float(np.real(np.sum(rr * np.exp(pr))))
stated("review", "items[3].widget.answer", ry, ry2, 4)
stated("review", "items[3].widget.wrong[0].value", 2 * math.exp(-1) + math.exp(-2), ry2 + 2 * math.exp(-2), 4)
stated("review", "items[3].explain.text", 2 * math.exp(-1), 2 / math.e, 4)
stated("review", "items[3].explain.text", math.exp(-2), 1 / math.e ** 2, 4)
stated("review", "items[4].widget.answer", 0.5 ** 2, euler_loop(lambda t, y: -2 * y, [1.0], 0.25, 2)[0], 2)
stated("review", "items[4].widget.wrong[0].value", math.exp(-1), ivp(lambda t, y: [-2 * y[0]], [1.0], 0.5)[0], 4)
ev = np.linalg.eigvals([[-2, 1], [1, -2]])
stated("review", "items[5].widget.answer", 2 / 3, 2 / max(abs(ev)), 4)
stated("review", "items[5].widget.wrong[0].value", 2 / 1, 2 / min(abs(ev)), 0)
stated("review", "items[6].widget.answer", 48 / 16, 4.8e-5 / 2 ** 4 * 1e6, 0)
stated("review", "items[6].widget.wrong[0].value", 48 / 2, 24, 0)
stated("review", "items[6].widget.wrong[1].value", 48 / 4, 12, 0)
stated("review", "items[7].widget.answer", zl / 25, zl2 / 25, 4)
stated("review", "items[7].widget.wrong[0].value", 2 / 25, brentq(lambda h: abs(1 - 25 * h) - 1, 0.05, 0.1), 2)
stated("review", "items[8].widget.answer", 60 * 1.35 / 0.5, 60 * (D - eul_D(60)) / 5e-5, 0, tol=1.5)
stated("review", "items[8].widget.wrong[0].value", 60 * math.sqrt(1.35 / 0.5), 60 * math.sqrt(2.7), 0)
stated("review", "items[8].explain.text", n163, n163, 0)
stated("review", "items[9].widget.options[3].why", D - eul_D(100), D - eul_D_formula(100), 1, scale=1e5, fmt="8.1")

# ---------------- homework-4 ----------------
stated("homework", "items[0].widget.answer", 1 / 9, lap(lambda t: t * math.exp(-2 * t), 1), 4)
stated("homework", "items[0].widget.wrong[0].value", 1 / 1 ** 2, lap(lambda t: t, 1), 0)
stated("homework", "items[3].widget.answer", 2 / 20, brentq(lambda h: abs(1 - 20 * h) - 1, 0.05, 0.2), 1)
stated("homework", "items[4].widget.answer", e10 / 16, e10b / 16, 2, scale=1e7)
stated("homework", "items[4].widget.wrong[0].value", e10 / 2, e10b / 2, 2, scale=1e7)
stated("homework", "items[4].explain.text", e20, e20b, 3, scale=1e7, fmt="1.358")
stated("homework", "items[4].explain.text", e10 / e20, e10b / e20b, 2)

def match(f, y0, Tm, exact, kk=0, tol=5e-5, max_n=65536, route=rk4_loop):
    prev, n = None, 1
    while n <= max_n:
        v = float(np.atleast_1d(route(f, y0, Tm / n, n))[kk])
        if prev is not None and abs(v - prev) < tol and abs(v - exact) < tol:
            return n, v
        prev, n = v, 2 * n
    return None
bond = lambda t, y: np.array([0.5 * (0.04 - y[0]), -y[0] * y[1]])
oscf = lambda t, y: np.array([y[1], -2 * y[1] - 5 * y[0]])
mb = match(bond, [0.06, 1.0], 5, D, kk=1); mo = match(oscf, [1.0, 0.0], 1, osc); me = match(lambda t, y: y, [1.0], 1, math.e)
stated("homework", "items[5].widget.tests[1].expect", mb[0], mb[0], 0)
stated("homework", "items[5].widget.tests[2].expect", mb[1], float(rk4_loop(bond, [0.06, 1.0], 5 / 8, 8)[1]), tol=1e-12)
stated("homework", "items[5].widget.tests[3].expect", mo[0], mo[0], 0)
stated("homework", "items[5].widget.tests[4].expect", mo[1], float(rk4_loop(oscf, [1.0, 0.0], 1 / 16, 16)[0]), tol=1e-12)
stated("homework", "items[5].widget.tests[5].expect", me[0], me[0], 0)
if match(oscf, [1.0, 0.0], 1, 0.0145, max_n=4096) is not None or abs(0.0145 - osc) < 5e-5:
    bad.append('planted closed form should never match')
stated("homework", "items[5].widget.tests[0].expect", R(0.1) ** 10, rk4_loop(lambda t, y: y, [1.0], 0.1, 10)[0], tol=1e-9)
neu = next(n for n in range(15000, 17000) if abs(euler_loop(oscf, [1.0, 0.0], 1 / n, n)[0] - osc) < 5e-5)
if not 15500 <= neu <= 16500:
    bad.append(f'Euler on the oscillator needs {neu}, not about 16,000')
print('Euler steps for the oscillator:', neu)
same("homework", "items[5].widget.how", 16000)
for path in ["items[6].model", "items[6].rubric"]:
    pass
stated("homework", "items[6].model", D, D2, 6)
stated("homework", "items[6].model", eul_D(60), eul_D_formula(60), 6)
stated("homework", "items[6].model", D - eul_D(60), D - eul_D_formula(60), 2, scale=1e4, fmt="1.35")
stated("homework", "items[6].model", (D - eul_D(60)) / 5e-5, (D - eul_D_formula(60)) / 5e-5, 1)
stated("homework", "items[6].model", 1e4 * (D - eul_D(60)), 1e4 * (D2 - eul_D_formula(60)), 2)   # pence
stated("homework", "items[6].model", 60 * 1.35 / 0.5, 162, 0)
stated("homework", "items[6].model", n163, n163, 0)
stated("homework", "items[6].model", rk_D(4), rk_D(4), 6)
stated("homework", "items[6].model", rk_D(4) - D, rk_D2(4) - D, 1, scale=1e5, fmt="1.4")
if abs(rk_D(4) - rk_D(8)) >= 5e-5:
    bad.append('model: 4 and 8 step runs agree')
stated("homework", "items[7].explain.text", 100 * 0.02 / 0.06, claim, 2)
stated("homework", "items[7].widget.options[1].why", 0.06 - 0.05, 0.01, 2)

for b in bad:
    print('BAD', b)
print(f'routes: {len(bad)} disagreements')
if bad:
    lv.results.append((False, 'route disagreements', ''))
lv.report()
