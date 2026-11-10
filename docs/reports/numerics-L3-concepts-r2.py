#!/usr/bin/env python3
"""Round-2 blind concept audit, numerics level 3 (l9 to l12, review-3, homework-3).

Independent experiments for every empirical claim. Exit 0 when the content is
right. A check that fails because the content is wrong is EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
Run from anywhere: python3 docs/reports/numerics-L3-concepts-r2.py
"""
import json, math, os, struct, sys, warnings
from fractions import Fraction
import numpy as np
import sympy as sp
from scipy.stats import norm
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'numerics')
FAILS, XFAILS, PASSES = [], [], []


def check(name, cond, note=''):
    (PASSES if cond else FAILS).append(name)
    print(('ok    ' if cond else 'FAIL  ') + name + (' | ' + note if note else ''))


def expected_fail(name, cond, note):
    """cond states the content's claim. It is expected to be False."""
    if cond:
        FAILS.append(name + ' (unexpectedly passed)')
        print('FAIL  ' + name + ' | claim now holds, remove the EXPECTED_FAIL | ' + note)
    else:
        XFAILS.append(name)
        print('EXPECTED_FAIL ' + name + ' | ' + note)


# ---------------------------------------------------------------- code tasks
def _close(a, b, tol):
    rel = (tol or {}).get('rel', 1e-9); ab = (tol or {}).get('abs', 0.0)
    if isinstance(a, (list, tuple, np.ndarray)) or isinstance(b, (list, tuple, np.ndarray)):
        a = np.asarray(a, dtype=float).ravel(); b = np.asarray(b, dtype=float).ravel()
        return a.shape == b.shape and all(math.isclose(x, y, rel_tol=rel, abs_tol=ab) for x, y in zip(a, b))
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)


def run_tests(w, source):
    out = []
    for t in w.get('tests', []):
        ns = {'__learner_source__': source, 'np': np, 'math': math}
        try:
            exec(w.get('prelude', ''), ns); exec(source, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); ok = False
                except Exception as e:
                    ok = type(e).__name__ == t['expect']
            else:
                got = eval(t['call'], ns); exp = t['expect']
                if isinstance(exp, str):
                    exp = eval(exp, ns)
                if t.get('compare') == 'isclose':
                    ok = _close(got, exp, t.get('tol'))
                else:
                    ok = got == tuple(exp) if isinstance(got, tuple) else bool(np.all(got == exp))
        except Exception:
            ok = False
        out.append(ok)
    return out


def code_tasks(fname):
    found = []

    def walk(o, p):
        if isinstance(o, dict):
            if 'solution' in o and 'tests' in o:
                found.append((p, o))
            for k, v in o.items():
                walk(v, p + '.' + k if p else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, '%s[%d]' % (p, i))
    walk(json.load(open(os.path.join(BASE, fname))), '')
    return found


def solution_ns(fname, idx=0):
    w = code_tasks(fname)[idx][1]
    ns = {'np': np, 'math': math}
    exec(w.get('prelude', ''), ns); exec(w['solution'], ns)
    return ns


from scipy.integrate import solve_ivp, quad

warnings.simplefilter('ignore')
FILES = ('l9-quadrature.json', 'l10-gaussian-quadrature.json', 'l11-step-size.json', 'l12-stiff-equations.json', 'homework-3.json')
for f in FILES:
    for p, w in code_tasks(f):
        s, st = run_tests(w, w['solution']), run_tests(w, w['starter'])
        check('code:%s:%s solution passes %d tests, starter fails' % (f, p, len(s)), all(s) and not all(st))
rng = np.random.default_rng(33)
BSV = 10.450583572185565


def trap(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x)
    return (b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)


def simp(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x)
    return (b - a) / n / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


I = math.e - 1
slope = lambda ns, es: float(np.polyfit(np.log(ns), np.log(np.abs(es)), 1)[0])

# ------------------------------------------------------------------ l9
te = [trap(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16)]
sm = [simp(np.exp, 0, 1, n) - I for n in (2, 4, 8, 16)]
check('l9:trapezium_errors_order_2', np.allclose(te, [0.0356, 0.00894, 0.00224, 0.000559], rtol=5e-3) and abs(math.log2(te[2] / te[3]) - 2) < 0.01 and all(e > 0 for e in te))
check('l9:simpson_errors_order_4', np.allclose(sm, [5.79e-4, 3.70e-5, 2.33e-6, 1.46e-7], rtol=5e-3) and abs(math.log2(sm[2] / sm[3]) - 4) < 0.02
      and abs(slope([2, 16], [sm[0], sm[3]]) + 3.98) < 0.01)
check('l9:trapezium_error_formula', abs(1 / (16 * 12) * I - 0.00895) < 1e-5 and abs(te[1] - 1 / (16 * 12) * I) < 2e-5)
T4, T8 = trap(np.exp, 0, 1, 4), trap(np.exp, 0, 1, 8)
check('l9:richardson_is_simpson', abs((4 * T8 - T4) / 3 - simp(np.exp, 0, 1, 8)) < 1e-14 and abs((4 * T8 - T4) / 3 - 1.7182841547) < 1e-9
      and abs((4 * 1.7272219 - 1.7539311) / 3 - 1.7183188) < 1e-6)
c_ = -(te[0]) / 0.25           # T = I + c h^2 with h = 1/2
check('l9:average_leaves_five_eighths', abs(((te[0] + te[1]) / 2) / te[0] - 5 / 8) < 0.01)
ok = True
for _ in range(500):
    co = rng.normal(size=4); a, b = sorted(rng.uniform(-3, 3, 2))
    pf = lambda x: co[0] + co[1] * x + co[2] * x ** 2 + co[3] * x ** 3
    ex = sum(co[k] * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k in range(4))
    ok &= abs(simp(pf, a, b, 2) - ex) < 1e-10 * (1 + abs(ex))
check('l9:simpson_exact_for_cubics_one_panel (500 random cubics)', ok and abs(simp(lambda x: x ** 3 - x, 0, 2, 2) - 2) < 1e-14
      and abs(simp(lambda x: 4 * x ** 3 - x, 0, 1, 2) - 0.5) < 1e-14 and abs(simp(lambda x: x ** 4, 0, 1, 2) - 0.2) > 1e-3)
gk = lambda z: math.exp(-0.05) * np.maximum(100 * np.exp(0.03 + 0.2 * z) - 100, 0) * np.exp(-z ** 2 / 2) / math.sqrt(2 * math.pi)
NS = (16, 32, 64, 128)
sk = [simp(gk, -8, 8, n) - BSV for n in NS]
ss = [simp(gk, -0.15, 8, n) - BSV for n in NS]
check('l9:simpson_with_kink_inside', np.allclose(sk, [0.600, 0.116, 0.0108, -0.00644], rtol=5e-3))
check('l9:simpson_split_at_kink_is_order_4', np.allclose(ss, [9.26e-3, 5.10e-4, 3.10e-5, 1.92e-6], rtol=5e-3) and abs(math.log2(ss[2] / ss[3]) - 4) < 0.05)
NL = [2 ** k for k in range(4, 13)]
sl_s = slope(NL, [simp(gk, -8, 8, n) - BSV for n in NL])
sl_t = slope(NL, [trap(gk, -8, 8, n) - BSV for n in NL])
check('l9:kink_inside_drops_simpson_to_about_h^2', -2.6 < sl_s < -1.6, 'fitted slope %.2f over n = 16 to 4096' % sl_s)
expected_fail('l9:s9_trapezium_has_a_lower_order_than_simpson_with_the_kink_inside', sl_t > sl_s + 0.5,
              'with the kink inside, both rules are erratic and second order: fitted slopes %.2f (trapezium) and %.2f (Simpson). A kink does not lower the trapezium rule\'s order. '
              '# corrected: assert abs(sl_t - sl_s) < 0.5' % (sl_t, sl_s))
fk = lambda x: np.abs(x - 1 / math.pi)
Ik = quad(fk, 0, 1, points=[1 / math.pi], epsabs=1e-15)[0]
NK = [10 * 2 ** k for k in range(9)]
check('l9:trapezium_keeps_order_2_through_a_kink', -2.5 < slope(NK, [trap(fk, 0, 1, n) - Ik for n in NK]) < -1.6)
tail = 100 * norm.cdf(-7.8) - 100 * math.exp(-0.05) * norm.cdf(-8)
check('l9/l10:tail_beyond_8', abs(tail - 2.5e-13) < 1e-14)
check('l9/hw3:doubling_counts', 3.7e-5 / 16 ** 4 < 1e-9 < 3.7e-5 / 16 ** 3 and 0.02 / 4 ** 4 < 1e-4 < 0.02 / 4 ** 3 and 0.02 / 16 ** 2 < 1e-4 < 0.02 / 16)

# ------------------------------------------------------------------ l10
gl = lambda f, a, b, n: (lambda x, w: (b - a) / 2 * np.sum(w * f((b - a) / 2 * x + (a + b) / 2)))(*np.polynomial.legendre.leggauss(n))
ok = True
for n in range(1, 9):
    x, w = np.polynomial.legendre.leggauss(n)
    ok &= abs(w.sum() - 2) < 1e-13
    for d in range(2 * n + 1):
        exact = (1 - (-1) ** (d + 1)) / (d + 1)
        err = abs(np.sum(w * x ** d) - exact)
        ok &= (err < 1e-13) if d <= 2 * n - 1 else (err > 1e-6)
    ok &= np.allclose(np.sort(x), np.sort(np.polynomial.legendre.Legendre.basis(n).roots()), atol=1e-12)
check('l10:gauss_legendre_exact_to_degree_2n-1_and_not_2n (n = 1 to 8)', bool(ok))
x2, w2 = np.polynomial.legendre.leggauss(2); x3, w3 = np.polynomial.legendre.leggauss(3)
check('l10:two_and_three_node_rules', np.allclose(x2, [-1 / 3 ** 0.5, 1 / 3 ** 0.5]) and np.allclose(w2, 1) and np.allclose(x3, [-0.6 ** 0.5, 0, 0.6 ** 0.5])
      and np.allclose(w3, [5 / 9, 8 / 9, 5 / 9]) and abs(np.sum(w2 * x2 ** 4) - 2 / 9) < 1e-14 and abs(np.sum(w3 * x3 ** 6) - 0.24) < 1e-14
      and abs(gl(lambda x: x ** 3 + 2 * x ** 2 + 1, -1, 1, 2) - 10 / 3) < 1e-14)
ok = True
for _ in range(300):
    a, b = sorted(rng.uniform(-4, 4, 2)); co = rng.normal(size=6)
    ex = sum(co[k] * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k in range(6))
    ok &= abs(gl(lambda x: sum(co[k] * x ** k for k in range(6)), a, b, 3) - ex) < 1e-9 * (1 + abs(ex))
check('l10:mapping_keeps_exactness (300 random quintics and intervals)', ok and abs(np.sum(w3 * 1.0) * 1 / gl(lambda x: 0 * x + 1.0, 0, 4, 3) - 0.5) < 1e-14)
gs = [gl(gk, -0.15, 8, n) - BSV for n in (8, 16, 32)]
gkk = [gl(gk, -8, 8, n) - BSV for n in (8, 16, 32, 64)]
check('l10:gauss_split_errors', abs(gs[0] + 1.32e-3) < 1e-5 and abs(gs[1] + 2.0e-9) < 1e-10 and abs(gs[2] + tail) < 5e-14)
check('l10:gauss_with_kink_inside_is_slow', np.allclose(gkk, [3.90, 0.927, 0.120, -0.036], rtol=5e-3) and abs(gkk[3]) > abs(sk[2]))


def dens(S):
    zz = (np.log(S / 100) - 0.03) / 0.2
    return np.exp(-zz * zz / 2) / (S * 0.2 * math.sqrt(2 * math.pi))


es_ = {top: [math.exp(-0.05) * gl(lambda S: (S - 100) * dens(S), 100, top, n) - BSV for n in (64, 128)] for top in (200, 300, 400)}
check('l10:truncation_in_S_space', abs(es_[200][0] + 0.0483) < 1e-4 and abs(es_[200][1] - es_[200][0]) < 1e-9 and abs(es_[300][1] + 9.2e-6) < 1e-7 and abs(es_[400][1] + 1.8e-9) < 1e-10)
# s[8]: Monte Carlo error falls like 1/sqrt(n); a binomial tree like 1/n
rmse = []
for n in (1000, 4000, 16000, 64000):
    est = [math.exp(-0.05) * np.mean(np.maximum(100 * np.exp(0.03 + 0.2 * rng.standard_normal(n)) - 100, 0)) for _ in range(300)]
    rmse.append(float(np.sqrt(np.mean((np.array(est) - BSV) ** 2))))
check('l10:monte_carlo_error_like_n^-1/2 (300 replications per n)', abs(slope([1000, 4000, 16000, 64000], rmse) + 0.5) < 0.06, 'RMSE %s' % [float('%.3g' % v) for v in rmse])


def crr(n):
    dt = 1.0 / n; u = math.exp(0.2 * math.sqrt(dt)); d = 1 / u; q = (math.exp(0.05 * dt) - d) / (u - d)
    v = np.maximum(100 * u ** np.arange(n, -1, -1) * d ** np.arange(0, n + 1) - 100, 0)
    for _ in range(n):
        v = math.exp(-0.05 * dt) * (q * v[:-1] + (1 - q) * v[1:])
    return v[0]


NT = [50, 100, 200, 400, 800]
check('l10:binomial_tree_error_like_1/n', abs(slope(NT, [crr(n) - BSV for n in NT]) + 1) < 0.1)
bs_call = lambda K: 100 * norm.cdf((math.log(100 / K) + 0.07) / 0.2) - K * math.exp(-0.05) * norm.cdf((math.log(100 / K) + 0.03) / 0.2)
check('l10/hw3:closed_forms', abs(bs_call(100) - BSV) < 1e-12 and abs(bs_call(100) - 100 + 100 * math.exp(-0.05) - 5.573526) < 1e-6 and abs(bs_call(200) - 0.004799) < 1e-6
      and abs(bs_call(100) - bs_call(110) - 4.410495) < 1e-6 and abs(math.exp(-0.05) * norm.cdf(0.15) - 0.532325) < 1e-6 and abs(100 - 100 * math.exp(-0.05) - 4.877058) < 1e-6
      and norm.pdf(8) < 1e-14)

# ------------------------------------------------------------------ l11
kap, th, sig, tau = 0.5, 0.04, 0.1, 5.0
gam = math.sqrt(kap ** 2 + 2 * sig ** 2)
den = (gam + kap) * (math.exp(gam * tau) - 1) + 2 * gam
B5 = 2 * (math.exp(gam * tau) - 1) / den
A5 = (2 * gam * math.exp((kap + gam) * tau / 2) / den) ** (2 * kap * th / sig ** 2)
cir = lambda t, y: np.array([1 - 0.5 * y[0] - 0.005 * y[0] ** 2, -0.02 * y[0]])


def rk4(f, y0, h, n, t=0.0):
    y = np.array(y0, float)
    for _ in range(n):
        k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    return y


def euler(f, y0, h, n, t=0.0):
    y = np.array(y0, float)
    for _ in range(n):
        y = y + h * f(t, y); t += h
    return y


ref = solve_ivp(cir, [0, 5], [0, 0], rtol=1e-13, atol=1e-15, method='DOP853').y[:, -1]
check('l11:cir_closed_form_solves_the_riccati_odes', abs(B5 - 1.812959) < 1e-6 and abs(ref[0] - B5) < 1e-10 and abs(math.exp(ref[1]) - A5) < 1e-10
      and abs(100 * A5 * math.exp(-B5 * 0.06) - 79.1020) < 1e-4)
N4 = (5, 10, 20, 40)
ee = [euler(cir, [0, 0], 5 / n, n)[0] - B5 for n in N4]
re = [rk4(cir, [0, 0], 5 / n, n)[0] - B5 for n in N4]
check('l11:global_orders', abs(slope([5, 40], [ee[0], ee[3]]) + 0.99) < 0.02 and abs(slope([5, 40], [re[0], re[3]]) + 4.18) < 0.03
      and np.allclose(np.abs([ee[0], ee[3], re[0], re[3]]), [0.0964, 0.0124, 3.49e-4, 5.83e-8], rtol=5e-3) and abs(ee[1] - 0.0493) < 1e-4)
loc = lambda meth, h: abs(meth(lambda t, y: y, [1.0], h, 1)[0] - math.exp(h))
check('l11:local_error_is_one_order_higher', abs(math.log2(loc(rk4, 0.2) / loc(rk4, 0.1)) - 5) < 0.1 and abs(math.log2(loc(euler, 0.02) / loc(euler, 0.01)) - 2) < 0.05)
Cc = abs(re[1]) / 0.5 ** 4
n65 = math.ceil(5 / (1e-8 / Cc) ** 0.25)
check('l11:step_for_tolerance', abs(Cc - 2.81e-4) < 1e-6 and n65 == 65 and abs(rk4(cir, [0, 0], 5 / 65, 65)[0] - B5) < 1e-8 and abs(abs(rk4(cir, [0, 0], 5 / 65, 65)[0] - B5) - 8.2e-9) < 1e-10
      and Cc * (5 / 64) ** 4 > 1e-8 and math.ceil(5 / (1e-3 / (abs(ee[1]) / 0.5))) == 494 and math.ceil(1 / (1e-9 / 1e-3) ** 0.25) == 32)
y10, y20 = rk4(cir, [0, 0], 0.5, 10)[0], rk4(cir, [0, 0], 0.25, 20)[0]
check('l11:richardson_error_estimate', abs((y10 - y20) / 15 + 1.10e-6) < 1e-8 and abs((y20 - B5) + 9.84e-7) < 1e-9 and abs(((y10 - y20) / 15) / (y20 - B5) - 1) < 0.13)
# adaptive controller, written from the screen's description
t, y, h, acc, rej, hs = 0.0, np.array([1.0]), 0.1, 0, 0, []
fq = lambda t, y: y * y
while t < 0.95 - 1e-15:
    h = min(h, 0.95 - t)
    big = rk4(fq, y, h, 1, t); half = rk4(fq, rk4(fq, y, h / 2, 1, t), h / 2, 1, t + h / 2)
    err = float(np.max(np.abs(half - big))) / 15; scale = 1e-8 * max(1.0, float(np.max(np.abs(half))))
    if err <= scale:
        t += h; y = half + (half - big) / 15; acc += 1; hs.append(h)
    else:
        rej += 1
    h *= 5.0 if err == 0 else min(5.0, max(0.2, 0.9 * (scale / err) ** 0.2))
check('l11:adaptive_run', acc == 38 and rej == 1 and (acc + rej) * 12 == 468 and abs(hs[0] - 0.070) < 1e-3 and abs(hs[-2] - 0.0043) < 1e-4 and abs(hs[-1] - 0.0021) < 1e-4
      and abs(abs(y[0] / 20 - 1) - 2.4e-8) < 2e-9, 'accepted %d, rejected %d, relative error %.2e' % (acc, rej, y[0] / 20 - 1))
check('l11:local_tolerance_is_not_a_global_error', abs(y[0] / 20 - 1) > 1e-8)
check('l11:fixed_step_comparison', abs(abs(rk4(fq, [1.0], 0.95 / 400, 400)[0] / 20 - 1) - 7e-8) < 1e-8)
check('l11/hw3:controller_formula', abs(0.9 * 0.01 * (1e-8 / 3.2e-7) ** 0.2 - 0.0045) < 1e-12)
floor_ = [abs(rk4(lambda t, y: y, [1.0], 1.0 / n, n)[0] - math.e) for n in (10, 100, 1000, 10000, 100000)]
check('l11:rounding_floor_near_1e-14', floor_[0] / floor_[1] > 5000 and all(1e-16 < v < 1e-13 for v in floor_[2:]), str([float('%.1e' % v) for v in floor_]))

# ------------------------------------------------------------------ l12
Am = np.array([[-0.5, 0.0], [50.0, -50.0]]); cv = np.array([0.02, 0.0]); y0 = np.array([0.06, 0.03])
exact = lambda t: 4 + 100 / 49.5 * math.exp(-0.5 * t) - (1 + 100 / 49.5) * math.exp(-50 * t)
fine = solve_ivp(lambda t, y: Am @ y + cv, [0, 1], y0, method='Radau', rtol=1e-12, atol=1e-14).y[1, -1]
check('l12:exact_solution', abs(exact(1) - 5.2253) < 1e-4 and abs(100 * fine - exact(1)) < 1e-7 and sorted(np.linalg.eigvals(Am).real) == [-50.0, -0.5])


def eul_sys(h):
    y = y0.copy()
    for _ in range(round(1 / h)):
        y = y + h * (Am @ y + cv)
    return 100 * y[1]


check('l12:euler_runs', abs(eul_sys(0.04) - 8.2393) < 1e-3 and abs(eul_sys(0.05) + 10038) < 1 and abs(eul_sys(0.02) - 5.2222) < 1e-4 and abs(eul_sys(0.01) - exact(1)) < 0.01
      and abs(1.5 ** 20 - 3300) < 30)
check('l12:euler_stability_limit', all(abs(1 - 50 * h) < 1 for h in (0.001, 0.02, 0.0399)) and abs(1 - 50 * 0.04) == 1 and abs(1 - 50 * 0.05) == 1.5 and 2 / 0.5 == 4
      and 2 / 200 == 0.01 and 2 / 100 == 0.02)


def lin_path(L, Rm, h, n):
    y, out = y0.copy(), []
    for _ in range(n):
        y = np.linalg.solve(L, Rm @ y + h * cv); out.append(100 * y[1])
    return out


I2 = np.eye(2)
ie = lin_path(I2 - 0.25 * Am, I2, 0.25, 4); tr = lin_path(I2 - 0.125 * Am, I2 + 0.125 * Am, 0.25, 4)
check('l12:implicit_euler_and_trapezoidal_paths', np.allclose(ie, [5.5720, 5.5796, 5.4176, 5.2611], atol=1e-4) and np.allclose(tr, [7.9696, 3.9891, 6.5346, 4.3941], atol=1e-4)
      and np.allclose([exact(t) for t in (0.25, 0.5, 0.75, 1)], [5.7828, 5.5733, 5.3885, 5.2253], atol=1e-4)
      and abs(lin_path(I2 - 0.025 * Am, I2 + 0.025 * Am, 0.05, 20)[-1] - 5.22528) < 1e-5)
R = {'euler': lambda z: 1 + z, 'implicit': lambda z: 1 / (1 - z), 'trap': lambda z: (1 + z / 2) / (1 - z / 2), 'rk4': lambda z: 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24}
check('l12:factors', abs(R['implicit'](-12.5) - 0.0741) < 1e-4 and abs(R['trap'](-12.5) + 0.7241) < 1e-4 and abs(R['euler'](-2.5)) == 1.5 and abs(R['implicit'](-2.5) - 0.286) < 1e-3
      and abs(R['trap'](-2.5) + 0.111) < 1e-3 and abs(R['rk4'](-2.5) - 0.648) < 1e-3 and abs(R['implicit'](-10) - 0.0909) < 1e-4 and abs(R['trap'](-40) + 0.905) < 1e-3
      and abs(math.exp(-12.5) - 4e-6) < 3e-7)
check('l12:rk4_real_axis_limit', abs(brentq(lambda z: abs(R['rk4'](z)) - 1, -3, -2.5) + 2.7853) < 1e-4 and abs(2.7853 / 50 - 0.0557) < 1e-4)
zs = -rng.uniform(0, 60, 40000) + 1j * rng.uniform(-60, 60, 40000)
check('l12:implicit_methods_stable_on_whole_left_half_plane (40000 random z)', np.all(np.abs(R['implicit'](zs)) <= 1) and np.all(np.abs(R['trap'](zs)) <= 1))
far = 4.0 * np.exp(1j * np.linspace(0, 2 * np.pi, 720))
check('l12:explicit_regions_are_bounded', np.all(np.abs(R['euler'](far)) > 1) and np.all(np.abs(R['rk4'](far)) > 1))
check('l12:L_stability_limits', abs(R['trap'](-1e9) + 1) < 1e-8 and abs(R['implicit'](-1e9)) < 1e-8)
nfev = {}
for m in ('RK45', 'Radau', 'BDF'):
    s = solve_ivp(lambda t, y: Am @ y + cv, [0, 10], y0, method=m, rtol=1e-6, atol=1e-9)
    nfev[m] = (s.nfev, abs(s.y[1, -1] - (0.04 + (0.02 * 50 / 49.5) * math.exp(-5))))
check('l12:solve_ivp_costs', nfev['RK45'][0] > 2 * nfev['BDF'][0] and nfev['RK45'][0] > nfev['Radau'][0] and all(v[1] < 1e-6 for v in nfev.values()),
      'nfev here: %s (the lesson quotes 1,172, 422 and 226 for SciPy 1.14.1)' % {k: v[0] for k, v in nfev.items()})


def bs_rate(m):
    S = np.linspace(0, 300, m + 1)[1:-1]; dS = 300 / m
    a = 0.5 * 0.04 * S ** 2 / dS ** 2; bb = 0.05 * S / (2 * dS)
    M = np.diag(-2 * a - 0.05) + np.diag((a + bb)[:-1], 1) + np.diag((a - bb)[1:], -1)
    return float(np.max(np.abs(np.linalg.eigvals(M))))


check('l12:fastest_rate_scales_like_1/dS^2', abs(bs_rate(120) / bs_rate(60) - 4) < 0.3 and abs(bs_rate(240) / bs_rate(120) - 4) < 0.2 and abs(bs_rate(480) / bs_rate(240) - 4) < 0.1,
      'ratios %.2f and %.2f; rate at 240 nodes %.0f against sigma^2 Smax^2 / dS^2 = %.0f' % (bs_rate(120) / bs_rate(60), bs_rate(240) / bs_rate(120), bs_rate(240), 0.04 * 300 ** 2 / (300 / 240) ** 2))
check('r3:misc', abs(math.log2(0.0120 / 0.0030) - 2) < 1e-12 and abs((4 * 2.0010 - 2.0040) / 3 - 2.0) < 1e-12 and abs(3.2e-6 / 16 - 2e-7) < 1e-18 and 1e8 * 2.2e-16 < 1e-7)

print('\n%d checks passed, %d failed, %d EXPECTED_FAIL' % (len(PASSES), len(FAILS), len(XFAILS)))
for n in XFAILS:
    print('  EXPECTED_FAIL', n)
sys.exit(1 if FAILS else 0)
