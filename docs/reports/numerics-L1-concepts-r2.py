#!/usr/bin/env python3
"""Round-2 blind concept audit, numerics level 1 (l1 to l4, review-1, homework-1).

Independent experiments for every empirical claim. Exit 0 when the content is
right. A check that fails because the content is wrong is EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
Run from anywhere: python3 docs/reports/numerics-L1-concepts-r2.py
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


def txt(fname, *path):
    """The content's text at a JSON path, for the fix-pass checks."""
    o = json.load(open(os.path.join(BASE, fname)))
    for p in path:
        o = o[p]
    return o


warnings.simplefilter('ignore')
for f in ('l1-floating-point.json', 'l2-cancellation.json', 'l3-conditioning.json', 'l4-stability.json', 'homework-1.json'):
    for p, w in code_tasks(f):
        s, st = run_tests(w, w['solution']), run_tests(w, w['starter'])
        check('code:%s:%s solution passes %d tests, starter fails' % (f, p, len(s)), all(s) and not all(st))

U, EPS = 2.0 ** -53, 2.0 ** -52

# ------------------------------------------------------------------ l1
eps, halvings = 1.0, 0
while 1.0 + eps / 2 > 1.0:
    eps /= 2; halvings += 1
check('l1:eps_loop_52', halvings == 52 and eps == EPS == np.finfo(float).eps)
toy = sorted((1 + m / 8) * 2.0 ** p for p in range(-1, 3) for m in range(8))
check('l1:toy_format', len(toy) == 32 and toy[0] == 0.5 and toy[-1] == 7.5 and min(v for v in toy if v > 4) == 4.5
      and toy[1] - toy[0] == 1 / 16 and toy[9] - toy[8] == 1 / 8)


def fields(x):
    b = int.from_bytes(struct.pack('>d', x), 'big')
    return b >> 63, (b >> 52) & 0x7FF, (b & (2 ** 52 - 1)) / 2 ** 52


check('l1:decode_minus_6.5', fields(-6.5) == (1, 1025, 0.625) and hex(int.from_bytes(struct.pack('>d', -6.5), 'big') & (2 ** 52 - 1)) == '0xa000000000000')
check('l1:decode_100.25', fields(100.25) == (0, 1029, 0.56640625))
check('l1:spacing', abs(np.spacing(100.0) - 1.42e-14) < 1e-16 and abs(np.spacing(1e6) - 1.16e-10) < 1e-12
      and all(np.spacing(2.0 ** k * 1.3) == 2.0 ** (k - 52) for k in range(-20, 70)))
check('l1:integers_to_2^53', float(2 ** 53) + 1 == float(2 ** 53) and float(2 ** 53 - 1) + 1 == float(2 ** 53)
      and np.spacing(2.0 ** 52) == 1 and np.spacing(2.0 ** 53) == 2)
fi = np.finfo(float)
check('l1:limits', abs(fi.tiny - 2.225074e-308) < 1e-314 and abs(fi.max - 1.797693e308) < 1e302 and 5e-324 == 2.0 ** -1074 and 5e-324 / 2 == 0.0)
try:
    math.exp(710); raised = False
except OverflowError:
    raised = True
with warnings.catch_warnings(record=True) as wlist:
    warnings.simplefilter('always')
    v = np.exp(710.0)
check('l1:overflow_math_raises_numpy_inf_with_warning', raised and np.isinf(v) and any(issubclass(x.category, RuntimeWarning) for x in wlist)
      and abs(math.exp(709) - 8.218407e307) < 1e302)
rng = np.random.default_rng(11)
worst = Fraction(0)
for _ in range(20000):
    num, den = int(rng.integers(1, 10 ** 15)), int(rng.integers(1, 10 ** 15))
    q = Fraction(num, den)
    worst = max(worst, abs(Fraction(num / den) - q) / q)       # one correctly rounded division
check('l1:rounding_model_delta_le_u (20000 random reals)', worst <= Fraction(1, 2 ** 53), 'worst %.3e, u %.3e' % (float(worst), U))
check('l1:stored_101.37_not_exact', Fraction(101.37) != Fraction(10137, 100))
check('l1:time_gap_256ns', np.spacing(1.7e18) == 256.0 and float(1.7e18) + 100 == float(1.7e18) and 2 ** 60 < 1.7e18 < 2 ** 61)
check('l1:float32_gap_near_20000', np.spacing(np.float32(20000.0)) == 2.0 ** -9 and float(np.float32(20000.01)) == 20000.009765625
      and float(np.finfo(np.float32).eps) == 2.0 ** -23)
hund = np.round(np.arange(20000, 20001, 0.01), 2)
q0 = txt('l1-floating-point.json', 'quiz', 0, 'explain', 'text')
check('l1:quiz0_level_rounds_to_its_hundredth_but_a_hundredth_move_is_2.3_per_cent_off (corrected claim, fix pass)',
      np.all(np.round(hund.astype(np.float32).astype(float), 2) == hund)
      and abs(float(Fraction(20000.01) - Fraction(float(np.float32(20000.01)))) - 0.00023) < 5e-6
      and abs((float(np.float32(20000.01)) - float(np.float32(20000.0))) / 0.01 - 1) * 100 - 2.3 < 0.05
      and 'off by 0.00023' in q0 and 'still rounds to its hundredth' in q0 and 'wrong by 2.3%' in q0 and 'third decimal' not in q0,
      'every hundredth from 20,000.00 to 20,000.99 survives a float32 round trip; the one-hundredth move is 0.009765625')
check('fix1:float32_one_hundredth_move_is_2.3_per_cent_off', float(np.float32(20000.02)) - float(np.float32(20000.01)) == 0.009765625
      and abs(0.009765625 / 0.01 - 1 + 0.0234) < 1e-4 and abs(20000.01 - 20000.009765625 - 0.00023) < 1e-5)
check('l1:stored_tenth_error', abs(float(Fraction(0.1) - Fraction(1, 10)) - 5.55e-18) < 1e-20
      and abs(float((Fraction(0.1) - Fraction(1, 10)) / Fraction(1, 10)) - 5.55e-17) < 1e-19)
check('hw1:hex_word_is_10', struct.unpack('>d', bytes.fromhex('4024000000000000'))[0] == 10.0)
check('hw1:float32_integers_to_2^24', np.float32(2 ** 24) + np.float32(1) == np.float32(2 ** 24)
      and all(np.float32(n) + np.float32(1) == n + 1 for n in (2 ** 23, 2 ** 24 - 2, 2 ** 24 - 1)))
check('r1:float32_gap_at_1e6_and_penny', np.spacing(np.float32(1e6)) == 0.0625 and np.float32(1e6) + np.float32(0.01) == np.float32(1e6))
check('r1:0.01_exponent', fields(0.01)[1] == 1016 and abs((1 + fields(0.01)[2]) - 1.28) < 1e-12)

# ------------------------------------------------------------------ l2
b = 1e8
tb = (b - math.sqrt(b * b - 4)) / 2
check('l2:textbook_root_no_digit', abs(tb - 7.450581e-9) < 1e-14 and abs(tb / 1e-8 - 1 + 0.255) < 1e-3)
errs = []
for k in range(1, 9):
    bb = 10.0 ** k
    st = 2 / (bb + math.sqrt(bb * bb - 4))
    errs.append(max(abs((bb - math.sqrt(bb * bb - 4)) / 2 - st) / st, 1e-17))
slope = np.polyfit(range(1, 9), np.log10(errs), 1)[0]
check('l2:error_grows_like_b^2', 1.7 < slope < 2.3, 'slope %.2f decades per decade' % slope)
check('l2:conjugate_root_full_precision', abs(2 / (b + math.sqrt(b * b - 4)) / 1e-8 - 1) < 1e-15)
check('l2:expm1', abs((math.exp(1e-10) - 1) / math.expm1(1e-10) - 1 - 8.27e-8) < 1e-10 and abs(math.expm1(1e-10) - 1.00000000005e-10) < 1e-24)


def onepass(x):
    n = len(x)
    return (sum(v * v for v in x) - sum(x) ** 2 / n) / (n - 1)


check('l2:one_pass_variance', onepass([1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]) == 0.0
      and abs(onepass([1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16]) - 29.33) < 0.01 and np.spacing(1e18) == 128.0)
check('l2:float32_gap_at_1e9', np.spacing(np.float32(1e9)) == 64.0)
fd = [abs((math.exp(1 + 10.0 ** -k) - math.e) / 10.0 ** -k - math.e) for k in range(1, 16)]
check('l2:forward_bump_V', int(np.argmin(fd)) + 1 == 8 and abs(fd[7] - 6.6e-9) < 1e-10 and abs(fd[14] - 0.39) < 0.01 and abs(fd[0] - 0.14) < 0.01)
h, m, c, e = sp.symbols('h m c epsilon', positive=True)
hs = sp.solve(sp.diff(m * h / 2 + 2 * e * c / h, h), h)
check('l2:best_forward_bump_formula', len(hs) == 1 and sp.simplify(hs[0] - 2 * sp.sqrt(e * c / m)) == 0 and abs(2 * math.sqrt(EPS) - 2.98e-8) < 1e-10)
cd = {k: abs((math.exp(1 + 10.0 ** -k) - math.exp(1 - 10.0 ** -k)) / (2 * 10.0 ** -k) - math.e) for k in range(2, 12)}
check('l2:central_best_near_eps^(1/3)', min(cd, key=cd.get) in (5, 6) and abs(EPS ** (1 / 3) - 6.06e-6) < 1e-8 and abs(cd[5] - 5.9e-11) < 3e-11)
hs4 = sp.solve(sp.diff(h ** 2 / 12 * m + 4 * e * c / h ** 2, h), h)
check('hw1:second_difference_best_bump', sp.simplify(hs4[0] - (48 * e * c / m) ** sp.Rational(1, 4)) == 0 and abs((48 * EPS) ** 0.25 - 3.21e-4) < 1e-6)


def bs(S, K, r, s, T, kind='c'):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    cc = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return cc if kind == 'c' else cc - S + K * math.exp(-r * T)


def vega(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return S * math.sqrt(T) * norm.pdf(d1)


V = lambda S: bs(S, 100, 0.05, 0.2, 1.0)
delta = norm.cdf((0.05 + 0.02) / 0.2)
gamma = norm.pdf(0.35) / (100 * 0.2)
de = {hh: abs((V(100 + hh) - V(100)) / hh - delta) for hh in (1.0, 0.01, 1e-12)}
check('l2:delta_bumps', abs(delta - 0.636831) < 1e-6 and min(de, key=de.get) == 0.01 and abs(de[1.0] - 9.3e-3) < 2e-4 and abs(de[0.01] - 9.4e-5) < 3e-6
      and 1e-3 < de[1e-12] < 2e-2, 'errors %s' % {k: float('%.3g' % v) for k, v in de.items()})
ge = {hh: abs((V(100 + hh) - 2 * V(100) + V(100 - hh)) / hh ** 2 - gamma) for hh in (1.0, 0.01, 1e-4, 1e-6)}
check('l2:gamma_bumps', abs(gamma - 0.0187620) < 1e-7 and min(ge, key=ge.get) == 0.01 and ge[1e-6] > 1e-3 and abs(ge[1.0] - 2.3e-6) < 2e-7)
# (corrected claim, fix pass) l2 screens[9].hints[1]: the numerator's rounding error does not grow with 1/h; the estimate's does.
import mpmath as _mp
_mp.mp.dps = 40
def _Vm(S):
    S = _mp.mpf(S); d1 = (_mp.log(S / 100) + _mp.mpf('0.07')) / _mp.mpf('0.2')
    return S * _mp.ncdf(d1) - 100 * _mp.e ** _mp.mpf('-0.05') * _mp.ncdf(d1 - _mp.mpf('0.2'))
_num = {hh: abs(float((V(100 + hh) - 2 * V(100) + V(100 - hh)) - (_Vm(100 + hh) - 2 * _Vm(100) + _Vm(100 - hh)))) for hh in (1.0, 0.1, 0.01, 1e-3, 1e-4)}
check('l2:s9_hint1_numerator_error_is_flat_estimate_error_grows_like_1/h^2 (corrected claim, fix pass)',
      max(_num.values()) < 100 * EPS * V(100) and 'in the estimate grows like' in txt('l2-cancellation.json', 'screens', 9, 'hints', 1, 'text'),
      'numerator rounding errors %s, all below 100 eps V for h from 1 to 1e-4' % ['%.1e' % v for v in _num.values()])
check('l2:model_best_delta_bump', abs(2 * math.sqrt(EPS * V(100) / gamma) - 7e-7) < 1e-7)
check('l2:log1p', abs(math.log(1 + 1e-12) - 1.000089e-12) < 1e-18 and abs(math.log1p(1e-12) - 9.999999999995e-13) < 1e-25)
ok = True
for _ in range(20000):
    y = float(rng.uniform(0.1, 1e6)); x = float(rng.uniform(y / 2, 2 * y))
    ok &= Fraction(x - y) == Fraction(x) - Fraction(y)
check('l2:sterbenz_exact (20000 random pairs)', ok and 1.5 - 1.25 == 0.25)
neg = zero = 0
swing = []
two = []
for _ in range(200):
    x = 1e9 + rng.normal(0, 3, 250)
    v = float(np.mean(x * x) - np.mean(x) ** 2)
    neg += v < 0; zero += v == 0; swing.append(abs(v)); two.append(float(np.var(x, ddof=1)))
check('l2/hw1:one_pass_noise_can_be_negative_or_zero (200 simulated years)', neg > 20 and zero > 20 and 100 < max(swing) < 1000 and 6 < min(two) and max(two) < 13,
      'negative %d, zero %d, max |v| %.0f, two-pass %.1f to %.1f' % (neg, zero, max(swing), min(two), max(two)))
check('r1:sqrt_difference', abs(1 / (math.sqrt(1e12 + 1) + 1e6) - 5e-7) < 1e-12)
ns = solution_ns('homework-1.json')
pen = [np.float32(0.01)] * 10 ** 6
tot = np.float32(0)
for v in pen:
    tot = tot + v
check('hw1:float32_pennies', abs(float(tot) - 9865.22) < 0.01 and abs(float(ns['kahan_total'](pen)) - 10000) < 0.005)

# ------------------------------------------------------------------ l3
A = np.array([[1, 1], [1, 1.0001]])
x1, x2 = np.linalg.solve(A, [2, 2.0001]), np.linalg.solve(A, [2, 2.0002])
check('l3:meeting_point_moves', np.allclose(x1, [1, 1], atol=1e-8) and np.allclose(x2, [0, 2], atol=1e-8))
ratio = (np.linalg.norm(x2 - x1) / np.linalg.norm(x1)) / (0.0001 / np.linalg.norm([2, 2.0001]))
sv = np.linalg.svd(A, compute_uv=False)
check('l3:measured_ratio_and_kappa', abs(ratio - 28285) < 5 and abs(sv[0] / sv[1] - 40002) < 0.01 and abs(1 / np.linalg.det(A) - 10000) < 1e-6)
Uu = np.linalg.svd(A)[0]
dx = np.linalg.solve(A, Uu[:, 1] * 1e-9)
worst_ratio = (np.linalg.norm(dx) / np.linalg.norm(x1)) / (1e-9 / np.linalg.norm([2, 2.0001]))
check('l3:worst_direction_reaches_kappa_for_this_b', abs(worst_ratio / 40002 - 1) < 1e-6)
mx = 0
for _ in range(20000):
    bb = rng.normal(size=2); db = rng.normal(size=2) * 1e-7
    xx = np.linalg.solve(A, bb); dd = np.linalg.solve(A, db)
    mx = max(mx, (np.linalg.norm(dd) / np.linalg.norm(xx)) / (np.linalg.norm(db) / np.linalg.norm(bb)))
check('l3:bound_never_exceeded_and_not_always_met (20000 random b, db)', mx <= 40002.0001 and ratio < 40002, 'largest ratio seen %.0f' % mx)
xs = sp.symbols('x', positive=True)
kap = lambda f: sp.simplify(xs * sp.diff(f, xs) / f)
check('l3:function_condition_numbers', kap(sp.sqrt(xs)) == sp.Rational(1, 2) and kap(sp.exp(xs)) == xs and kap(xs ** 2) == 2
      and abs(float(kap(xs - 1).subs(xs, 1.0001)) - 10001) < 1e-6 and abs(float(kap(sp.log(xs)).subs(xs, 1.0001)) - 10000.5) < 0.01
      and sp.limit(kap(sp.exp(xs) - 1), xs, 0) == 1)
H8 = np.array([[1 / (j + k + 1) for k in range(8)] for j in range(8)])
check('l3:hilbert8', abs(np.linalg.cond(H8) / 1.53e10 - 1) < 0.01 and abs(math.log10(np.linalg.cond(H8)) - 10.2) < 0.05 and abs(math.log10(40002) - 4.6) < 0.005)
res = np.array([2, 2.0001]) - A @ np.array([0.0, 2.0])
check('l3:small_residual_large_error', np.allclose(res, [0, -0.0001], atol=1e-12))
for r in (0.95, 0.99, 0.3):
    check('l3:corr_kappa_r=%s' % r, abs(np.linalg.cond([[1, r], [r, 1]]) - (1 + r) / (1 - r)) < 1e-9 * (1 + r) / (1 - r))
check('l3:corr_kappa_formula_with_|r|_and_r>=0 (corrected claim, fix pass)',
      all(abs(np.linalg.cond([[1, r], [r, 1]]) - (1 + abs(r)) / (1 - abs(r))) < 1e-6 * (1 + abs(r)) / (1 - abs(r)) for r in (-0.95, -0.3, 0.0, 0.3, 0.95, 0.99))
      and '1 + |r|}{1 - |r|' in txt('l3-conditioning.json', 'screens', 4, 'explain', 'text')
      and 'for $r \\ge 0$' in txt('l3-conditioning.json', 'quiz', 0, 'prose'),
      'kappa of [[1, r], [r, 1]] is (1 + |r|)/(1 - |r|): eigenvalues 1 + r and 1 - r')
p60, v60 = bs(100, 60, 0.05, 0.2, 1.0, 'p'), vega(100, 60, 0.05, 0.2, 1.0)
iv = lambda q: brentq(lambda s: bs(100, 60, 0.05, s, 1.0, 'p') - q, 1e-4, 5, xtol=1e-14)
up1, dn1, up5 = 100 * (iv(p60 + 0.01) - 0.2), 100 * (0.2 - iv(p60 - 0.01)), 100 * (iv(p60 + 0.05) - 0.2)
check('l3:put60_price_vega_first_order', abs(p60 - 0.0113) < 5e-5 and abs(v60 - 0.588) < 5e-4 and abs(0.01 / v60 * 100 - 1.70) < 0.005
      and abs(0.01 / vega(100, 100, 0.05, 0.2, 1.0) * 100 - 0.027) < 5e-4 and 1 < up1 < 4 and 1 < dn1 < 4,
      'true moves for a 0.01 error: +%.2f and -%.2f vol points (first-order 1.70)' % (up1, dn1))
q3, s9 = txt('l3-conditioning.json', 'quiz', 3, 'explain', 'text'), txt('l3-conditioning.json', 'screens', 9, 'explain', 'text')
check('l3:quiz3_and_s9_true_moves_of_the_60_put (corrected claim, fix pass)',
      abs(up5 - 4.1) < 0.05 and p60 - 0.05 < 0 and abs(up1 - 1.3) < 0.05 and abs(dn1 - 3.3) < 0.05 and abs(0.01 / p60 * 100 - 89) < 0.5
      and '4.1 points' in q3 and 'no vol at all' in q3 and '8.5' not in q3
      and '1.3 points up and 3.3 down' in s9 and '89%' in s9,
      '+0.05 moves the vol %.2f points, -0.05 makes the price negative; +-0.01 give +%.2f and -%.2f' % (up5, up1, dn1))
check('l3:quiz3_atm', abs(0.05 / vega(100, 100, 0.05, 0.2, 1.0) * 100 - 0.133) < 1e-3)

# ------------------------------------------------------------------ l4
s, t, terms = 0.0, 1.0, []
for k in range(1, 120):
    s += t; terms.append(t); t *= -20 / k
check('l4:series_e^-20', s == 6.147561828914626e-09 and abs((s - math.exp(-20)) / math.exp(-20) - 1.983) < 1e-3)
check('l4:reordering_does_not_help', abs(sum(sorted(terms, key=abs)) / math.exp(-20) - 1) > 0.5)
check('l4:largest_term', abs(max(terms) - 4.31e7) < 1e5 and abs(math.log10(max(terms)) - math.log10(math.exp(-20)) - 16.3) < 0.05)
s2, t = 0.0, 1.0
for k in range(1, 120):
    s2 += t; t *= 20 / k
check('l4:reciprocal_series_stable', abs(1 / s2 / math.exp(-20) - 1) < 8 * U)
check('l4:no_nearby_x', abs(math.log(s) + 18.907) < 1e-3)
e8 = 1e-8
check('l4:lauchli_gram_singular', 1 + e8 * e8 == 1.0 and 1 + 1e-14 != 1.0 and abs(1e-14 / EPS - 45) < 0.1)
L8 = np.array([[1, 1], [e8, 0], [0, e8]]); L7 = np.array([[1, 1], [1e-7, 0], [0, 1e-7]])
check('l4:lauchli_kappa', abs(np.linalg.cond(L8) / 1.41e8 - 1) < 0.01 and abs(math.log10(np.linalg.cond(L8) ** 2) - 16.3) < 0.01
      and abs(np.linalg.cond(L7) ** 2 * U - 0.02) < 0.003 and np.linalg.cond(L8) ** 2 * U > 1)
n4 = solution_ns('l4-stability.json')
try:
    r8 = n4['lstsq_normal'](L8, [2, e8, e8]); fail8 = not np.allclose(r8, [1, 1])
except Exception:
    fail8 = True
check('l4:normal_equations_fail_at_1e-8_work_at_1e-7', fail8 and np.allclose(n4['lstsq_normal'](L7, [2, 1e-7, 1e-7]), [1, 1], atol=1e-6)
      and np.allclose(n4['lstsq_qr'](L8, [2, e8, e8]), [1, 1], atol=1e-9) and np.allclose(np.linalg.lstsq(L8, [2, e8, e8], rcond=None)[0], [1, 1], atol=1e-9))
for trial in range(200):
    M = rng.normal(size=(8, 4)) @ np.diag(10.0 ** rng.uniform(-3, 0, 4))
    if abs(np.linalg.cond(M.T @ M) / np.linalg.cond(M) ** 2 - 1) > 1e-4 or abs(np.linalg.cond(np.linalg.qr(M)[1]) / np.linalg.cond(M) - 1) > 1e-8:
        check('l4:gram_squares_kappa_qr_keeps_it', False); break
else:
    check('l4:gram_squares_kappa_qr_keeps_it (200 random matrices)', True)
tt = np.linspace(0, 1, 100); A15 = np.vander(tt, 15, increasing=True); b15 = np.exp(np.sin(4 * tt)) / 2006.787453080206
xq, xn, xl = n4['lstsq_qr'](A15, b15)[-1], n4['lstsq_normal'](A15, b15)[-1], np.linalg.lstsq(A15, b15, rcond=None)[0][-1]
check('l4:trefethen_bau_fit', abs(np.linalg.cond(A15) / 2.27e10 - 1) < 0.01 and abs(xq - 1) < 2.5e-6 and abs(xl - 1) < 2.5e-6 and abs(xn - 1) > 0.5,
      'QR %.10f, lstsq %.10f, normal equations %.3f on this machine' % (xq, xl, xn))
yr = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30.0]); D = np.vander(yr, 4, increasing=True)
Ds = np.vander((yr - yr.mean()) / yr.std(), 4, increasing=True)
check('l4:yield_design_conditioning', abs(np.linalg.cond(D) / 2.98e4 - 1) < 0.01 and abs(np.linalg.cond(D.T @ D) / 8.88e8 - 1) < 0.01 and abs(np.linalg.cond(Ds) - 13.3) < 0.05)
# quiz[1].o[1].why: "An ill-conditioned problem rules [forward accuracy] out for any algorithm."
xa, ya = 1.0 + 2.0 ** -40, 1.0
kappa_sub = (abs(xa) + abs(ya)) / abs(xa - ya)
why1 = txt('l4-stability.json', 'quiz', 1, 'widget', 'options', 1, 'why')
check('l4:quiz1_backward_stable_promises_only_about_kappa_u (corrected claim, fix pass)',
      kappa_sub > 1e12 and Fraction(xa - ya) == Fraction(xa) - Fraction(ya)
      and 'for any algorithm' not in why1 and 'backward stable algorithm does not promise it' in why1 and '\\kappa u' in why1,
      'x - y with kappa %.1e is exact (Sterbenz), so the limit is on what a backward stable method promises, not on every algorithm' % kappa_sub)
# homework-1 items[8]: kappa of the sample variance is about 2 xbar / s
xb = 1e9 + rng.normal(0, 3, 250)
s0 = np.var(xb, ddof=1)
amp = []
for _ in range(4000):
    eta = 1e-12
    xp = xb * (1 + eta * rng.choice([-1, 1], 250))
    amp.append(abs(np.var(xp, ddof=1) / s0 - 1) / eta)
check('hw1:variance_kappa_about_2xbar_over_s (4000 random perturbations)', 0.2 < max(amp) / (2 * 1e9 / math.sqrt(s0)) < 1.5,
      'largest amplification %.2e against 2*xbar/s = %.2e' % (max(amp), 2e9 / math.sqrt(s0)))
check('hw1:one_pass_error_scale', 1 < U * (1e9 / 3) ** 2 < 100 and abs(2e9 / math.sqrt(10) / 6e8 - 1) < 0.1)
check('r1:e^-30_series', abs(30.0 ** 30 / math.factorial(30) / 7.8e11 - 1) < 0.01 and abs(math.exp(-30) / 9.4e-14 - 1) < 0.01)
check('hw1:normal_equations_digits', abs(16 - math.log10(9e10) - 5.0) < 0.1 and abs(16 - math.log10(3e5) - 10.5) < 0.05)

print('\n%d checks passed, %d failed, %d EXPECTED_FAIL' % (len(PASSES), len(FAILS), len(XFAILS)))
for n in XFAILS:
    print('  EXPECTED_FAIL', n)
sys.exit(1 if FAILS else 0)
