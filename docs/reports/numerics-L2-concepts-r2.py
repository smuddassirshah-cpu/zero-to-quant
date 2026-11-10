#!/usr/bin/env python3
"""Round-2 blind concept audit, numerics level 2 (l5 to l8, review-2, homework-2).

Independent experiments for every empirical claim. Exit 0 when the content is
right. A check that fails because the content is wrong is EXPECTED_FAIL: it is
reported, the exit code is unchanged, and the corrected assert sits beside it.
Run from anywhere: python3 docs/reports/numerics-L2-concepts-r2.py
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
    """The content's text or value at a JSON path, for the fix-pass checks."""
    o = json.load(open(os.path.join(BASE, fname)))
    for p in path:
        o = o[p]
    return o


import mpmath as mp
from scipy.interpolate import CubicSpline

warnings.simplefilter('ignore')
FILES = ('l5-bisection-and-newton.json', 'l6-safe-root-finder.json', 'l7-interpolation.json', 'l8-splines.json', 'homework-2.json')
for f in FILES:
    for p, w in code_tasks(f):
        s, st = run_tests(w, w['solution']), run_tests(w, w['starter'])
        check('code:%s:%s solution passes %d tests, starter fails' % (f, p, len(s)), all(s) and not all(st))
rng = np.random.default_rng(22)
R2 = 2 ** 0.5
f2 = lambda x: x * x - 2

# ------------------------------------------------------------------ l5
x, ne = 1.0, []
for k in range(4):
    x = x - f2(x) / (2 * x); ne.append(abs(x - R2))
a, b, se = 1.0, 2.0, []
for k in range(6):
    c = b - f2(b) * (b - a) / (f2(b) - f2(a)); a, b = b, c; se.append(abs(c - R2))
check('l5:newton_error_table', np.allclose(ne, [0.0858, 0.00245, 2.12e-6, 1.59e-12], rtol=5e-3))
check('l5:secant_error_table', np.allclose(se[:5], [0.0809, 0.0142, 4.21e-4, 2.12e-6, 3.16e-10], rtol=5e-3) and se[5] < 1e-12 and se[4] > 1e-12)
order = lambda e0, e1, e2: math.log(e2 / e1) / math.log(e1 / e0)
check('l5:newton_order_estimates', abs(order(*ne[:3]) - 1.98) < 0.02 and abs(order(*ne[1:]) - 2.0) < 0.02
      and abs(ne[3] / ne[2] ** 2 - 0.3535) < 2e-3 and abs(1 / (2 * R2) - 0.353553) < 1e-6 and abs(ne[1] / ne[0] ** 2 - 0.3333) < 1e-3)
check('l5:secant_order_estimates', abs(order(*se[1:4]) - 1.50) < 0.02 and abs(order(*se[2:5]) - 1.67) < 0.02)
mp.mp.dps = 3000
a, b, r2, es = mp.mpf(1), mp.mpf(2), mp.sqrt(2), []
for k in range(14):
    c = b - (b * b - 2) * (b - a) / ((b * b - 2) - (a * a - 2)); a, b = b, c; es.append(abs(c - r2))
ps = [float(mp.log(es[k + 1] / es[k]) / mp.log(es[k] / es[k - 1])) for k in range(8, 13)]
check('l5:secant_order_tends_to_golden_ratio (3000-digit arithmetic)', all(abs(p - (1 + 5 ** 0.5) / 2) < 0.01 for p in ps), 'late estimates %s' % [round(p, 4) for p in ps])
x, es = mp.mpf(1), []
for k in range(8):
    x = x - (x * x - 2) / (2 * x); es.append(abs(x - r2))
check('l5:newton_order_2_simple_root (3000-digit arithmetic)', all(abs(float(mp.log(es[k + 1] / es[k]) / mp.log(es[k] / es[k - 1])) - 2) < 0.01 for k in range(3, 7)))
x, es = 2.0, []
for k in range(30):
    x = x - (x - 1) ** 2 / (2 * (x - 1)); es.append(abs(x - 1))
check('l5:newton_order_1_at_double_root', all(abs(es[k + 1] / es[k] - 0.5) < 1e-9 for k in range(25)))
halvings = lambda w, tol: next(k for k in range(200) if w / 2 ** k < tol)
check('l5/l6/r2/hw2:bisection_counts', halvings(0.2, 1e-10) == 31 and halvings(1, 1e-6) == 20 and halvings(1, 1e-12) == 40 and halvings(4.9999, 1e-10) == 36
      and halvings(1, 1e-9) == 30 and halvings(4.9999, 1e-8) == 29 and abs(5 / 2 ** 10 - 0.00488) < 1e-5)
mids, lo, hi = [], 1.0, 2.0
for k in range(4):
    m = (lo + hi) / 2; mids.append(abs(m - R2)); lo, hi = (m, hi) if f2(m) < 0 else (lo, m)
check('l5:midpoint_error_not_monotone_width_bounds_it', np.allclose(mids, [0.0858, 0.164, 0.0392, 0.0233], rtol=5e-3) and mids[1] > mids[0])
try:
    f2(0.0) / (2 * 0.0); zde = False
except ZeroDivisionError:
    zde = True
check('l5:newton_from_0_divides_by_zero', zde)
check('l5/r2/hw2:efficiency', abs(2 ** 0.5 - 1.414) < 1e-3 and abs(2 ** (2 / 3) - 1.587) < 1e-3 and abs(1 / math.log2((1 + 5 ** 0.5) / 2) - 1 - 0.44) < 5e-3)
n5 = solution_ns('l5-bisection-and-newton.json')
P = lambda y: sum(5 / (1 + y) ** t for t in range(1, 6)) + 100 / (1 + y) ** 5 - 95
dP = lambda y: sum(-5 * t / (1 + y) ** (t + 1) for t in range(1, 6)) - 500 / (1 + y) ** 6
ytrue = brentq(P, 0, 0.2, xtol=1e-15)
y, path = 0.05, []
for k in range(3):
    y = y - P(y) / dP(y); path.append(y)
check('l5:bond_yield_newton_path', abs(ytrue - 0.06193228) < 1e-8 and np.allclose(path, [0.0615487, 0.06193188, 0.061932283], atol=5e-9) and abs(path[2] - ytrue) / ytrue < 1e-10)
check('l5:call_counts_42_9_6', n5['bisect'](f2, 1, 2, 1e-12)[1] == 42 and n5['secant'](f2, 1.0, 2.0, 1e-12)[1] == 9 and n5['newton'](f2, lambda x: 2 * x, 1.0, 1e-12)[1] == 6
      and n5['newton'](P, dP, 0.05, 1e-12)[1] == 4)
# s[9]: table says bisection costs 31 evaluations per bond; the lesson's own bisect counts the two end checks.
nb = n5['bisect'](P, 0.0, 0.2, 1e-10)[1]
cnt9 = [0]
def P9(y):
    cnt9[0] += 1
    return P(y)
n5['bisect'](P9, 0.0, 0.2, 1e-10)
s9w = txt('l5-bisection-and-newton.json', 'screens', 9)
check('l5:s9_bisection_costs_33_evaluations_per_bond (corrected claim, fix pass)',
      nb == 33 and cnt9[0] == 33 and 2 + halvings(0.2, 1e-10) == 33
      and s9w['canvas']['params']['rows'][1][1] == '33' and '33 evaluations' in s9w['prose']
      and abs(s9w['widget']['answer'] - 33 / 8) < 1e-12 and abs(s9w['widget']['wrong'][0]['value'] - 33 / 4) < 1e-12,
      'returned count %d, instrumented count %d, formula 2 + %d; key 33/8 = 4.125, distractor 33/4 = 8.25' % (nb, cnt9[0], halvings(0.2, 1e-10)))
# sign change needs continuity
bl = n5['bisect'](lambda x: 1 / x, -1.0, 2.0, 1e-9)[0]
check('l5:sign_change_without_continuity_gives_no_root', abs(bl) < 1e-8, 'bisect on 1/x over [-1, 2] ends at the pole, %.1e' % bl)
# endpoint roots and the product test (finding: wrong, in bisect and safe_newton)
n6 = solution_ns('l6-safe-root-finder.json', 0)


def honest(fn):
    """True when fn() returns a root of its f (to 1e-6) or raises ValueError."""
    try:
        r, fv = fn()
        return abs(fv) < 1e-6
    except ValueError:
        return True


P125 = lambda y: sum(5 / (1 + y) ** t for t in range(1, 6)) + 100 / (1 + y) ** 5 - 125     # yield is exactly 0
rb = n5['bisect'](P125, 0.0, 0.2, 1e-10)[0]
check('l5:bisect_root_at_lower_end_is_found_or_refused (corrected claim, fix pass)', honest(lambda: (rb, P125(rb))) and rb == 0.0
      and n5['bisect'](lambda x: x - 1, 0.0, 1.0, 1e-9)[0] == 1.0,
      'zero-yield bond: bisect returns %.4f where f = %.1f; a root at hi is returned too' % (rb, P125(rb)))
rs = n6['safe_newton'](lambda x: -x, lambda x: -1.0, 0.0, 1.0, ftol=0.0)
check('l6:safe_newton_root_at_lower_end_is_found_or_refused (corrected claim, fix pass)', honest(lambda: (rs, -rs)) and rs == 0.0
      and n6['safe_newton'](lambda x: x - 1, lambda x: 1.0, 0.0, 1.0, ftol=0.0) == 1.0,
      'f(x) = -x on [0, 1]: safe_newton returns %.6f' % rs)
tiny = lambda x: 1e-200 * (x * x + 1)
w5_sol_text = txt('l5-bisection-and-newton.json', 'screens', 8, 'widget', 'solution')
w6_sol_text = txt('l6-safe-root-finder.json', 'screens', 7, 'widget', 'solution')
check('l5/l6:same_sign_values_that_underflow_are_refused (corrected claim, fix pass)',
      1e-200 * 1e-200 == 0.0
      and honest(lambda: (n5['bisect'](tiny, 0.0, 1.0, 1e-9)[0], 1.0)) and honest(lambda: (n6['safe_newton'](tiny, lambda x: 2e-200 * x, 0.0, 1.0, ftol=0.0), 1.0))
      and honest(lambda: (n6['safe_newton'](tiny, lambda x: 2e-200 * x, 0.0, 1.0), 1.0))
      and 'flo * fhi' not in w5_sol_text + w6_sol_text,
      'the product 1e-200 * 1e-200 is 0.0; the solvers now compare signs and raise ValueError')
# (corrected claim, fix pass, audit round 3) the round-2 fix gains the stop at `mid == lo or mid == hi`: the
# lesson's 15th hidden test asks bisect to end for tol = 1e-17, below the 2.2e-16 gap between doubles near 1.41.
FIX_BISECT = '''
def bisect(f, lo, hi, tol):
    flo, fhi = f(lo), f(hi)
    calls = 2
    if flo == 0:
        return lo, calls
    if fhi == 0:
        return hi, calls
    if (flo > 0) == (fhi > 0):
        raise ValueError('no sign change')
    while hi - lo >= tol:
        mid = (lo + hi) / 2
        if mid == lo or mid == hi:
            break
        fm = f(mid)
        calls += 1
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2, calls
'''
FIX_NEWTON = '''
def newton(f, df, x0, tol, maxit=50):
    x, calls = x0, 0
    for _ in range(maxit):
        fx = f(x)
        calls += 1
        step = fx / df(x)
        x -= step
        if abs(step) < tol:
            return x, calls
    raise RuntimeError('no convergence')
'''
FIX_SAFE = '''
def safe_newton(f, df, lo, hi, xtol=1e-10, ftol=1e-12, maxit=100):
    flo, fhi = f(lo), f(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if (flo > 0) == (fhi > 0):
        raise ValueError('no sign change')
    x = 0.5 * (lo + hi)
    step = older = abs(hi - lo)
    for _ in range(maxit):
        fx = f(x)
        if abs(fx) <= ftol:
            return x
        if (fx > 0) == (flo > 0):
            lo, flo = x, fx
        else:
            hi = x
        d = df(x)
        new = x - fx / d if d != 0 else lo - 1.0
        if not (min(lo, hi) < new < max(lo, hi)) or abs(new - x) > 0.5 * older:
            new = 0.5 * (lo + hi)
        older, step = step, abs(new - x)
        if step < xtol:
            return new
        x = new
    raise RuntimeError('no convergence')
'''
w5 = code_tasks('l5-bisection-and-newton.json')[0][1]
src5 = w5['solution']
i0, i1 = src5.index('def bisect'), src5.index('def secant')
j0, j1 = src5.index('def newton'), src5.index('def observed_order')
fixed5 = src5[:i0] + FIX_BISECT.strip() + '\n\n' + src5[i1:j0] + FIX_NEWTON.strip() + '\n\n' + src5[j1:]
w6 = code_tasks('l6-safe-root-finder.json')[0][1]
check('fix:proposed_bisect_and_newton_pass_the_hidden_tests', all(run_tests(w5, fixed5)))
check('fix:proposed_safe_newton_passes_the_hidden_tests', all(run_tests(w6, FIX_SAFE)))
nf = {}
exec(fixed5, nf); exec(FIX_SAFE, nf)
try:
    nf['bisect'](tiny, 0.0, 1.0, 1e-9); refused = False
except ValueError:
    refused = True
check('fix:proposed_code_handles_end_roots_and_underflow', nf['bisect'](P125, 0.0, 0.2, 1e-10)[0] == 0.0 and nf['safe_newton'](lambda x: -x, lambda x: -1.0, 0.0, 1.0) == 0.0
      and nf['safe_newton'](lambda x: x - 1, lambda x: 1.0, 0.0, 1.0) == 1.0 and refused and nf['bisect'](f2, 1, 2, 1e-12)[1] == 42)
# plain newton in l5 has no iteration cap
cyc = lambda x: x ** 3 - 2 * x + 2
x, seen = 0.0, []
for k in range(10000):
    step = cyc(x) / (3 * x * x - 2); x -= step; seen.append(x)
try:
    n5['newton'](cyc, lambda x: 3 * x * x - 2, 0.0, 1e-12); n5_capped = False
except RuntimeError:
    n5_capped = True
check('l5:taught_newton_is_capped_and_raises_on_x^3-2x+2_from_0 (corrected claim, fix pass)',
      abs(step) > 0.5 and seen[-2:] == [1.0, 0.0] and n5_capped and 'while True' not in w5_sol_text,
      'plain Newton steps cycle 1, 0, 1, 0 for 10,000 steps; the lesson\'s newton now stops at maxit = 50 with RuntimeError')
try:
    nf['newton'](cyc, lambda x: 3 * x * x - 2, 0.0, 1e-12); capped = False
except RuntimeError:
    capped = True
check('fix:proposed_newton_raises_on_the_cycle', capped)

# ------------------------------------------------------------------ l6
nv = solution_ns('l6-safe-root-finder.json', 1)
K = np.arange(75.0, 130.0, 5.0); kinds = np.array(['p'] * 5 + ['c'] * 6)
P11 = np.array([0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003])
price = lambda i, s: float(nv['bs_price'](100.0, K[i:i + 1], 0.05, 1 / 12, s, kinds[i:i + 1])[0])
vg = lambda i, s: float(nv['bs_vega'](100.0, K[i:i + 1], 0.05, 1 / 12, s)[0])
first = [0.2 - (price(i, 0.2) - P11[i]) / vg(i, 0.2) for i in range(11)]
check('l6:first_newton_steps', abs(first[0] - 2724) < 1 and abs(first[1] - 18.14) < 0.01 and abs(first[2] - 0.89) < 0.01 and sum(v > 5 for v in first) == 2)
conv = []
for i in range(11):
    s = 0.2
    with np.errstate(all='ignore'):
        for k in range(40):
            s = s - (price(i, s) - P11[i]) / vg(i, s)
            if not np.isfinite(s):
                break
    conv.append(bool(np.isfinite(s) and abs(price(i, s) - P11[i]) < 1e-9))
check('l6:plain_newton_fails_on_two_strikes_only', conv == [False, False] + [True] * 9)
s3 = 0.3 - (price(0, 0.3) - 0.0766) / vg(0, 0.3); s5 = 0.5 - (price(0, 0.5) - 0.0766) / vg(0, 0.5)
check('l6:tangent_from_0.3_and_0.5', abs(s3 - 2.53) < 0.05 and abs(s5 - 0.482) < 2e-3)
iv = nv['implied_vols'](P11, K, 100.0, 0.05, 1 / 12, kinds)
bq = np.array([brentq(lambda s: price(i, s) - P11[i], 1e-4, 5, xtol=1e-14) for i in range(11)])
check('l6:safe_solver_matches_brentq_to_1e-10', np.max(np.abs(iv - bq)) < 1e-10 and abs(iv[0] - 0.480564) < 1e-6 and abs(iv[10] - 0.212383) < 1e-6)
iters = {}
for i in (0, 1, 2, 5, 10):
    for m in range(1, 40):
        r1 = nv['implied_vols'](P11[i:i + 1], K[i:i + 1], 100.0, 0.05, 1 / 12, kinds[i:i + 1], maxit=m)
        r2 = nv['implied_vols'](P11[i:i + 1], K[i:i + 1], 100.0, 0.05, 1 / 12, kinds[i:i + 1], maxit=m + 1)
        if r1[0] == r2[0]:
            iters[int(K[i])] = m; break
check('l6:iteration_counts', iters == {75: 9, 80: 9, 85: 8, 100: 2, 125: 6}, str(iters))
src6 = w6['solution']
nohalf = {}
exec(src6.replace(' or abs(new - x) > 0.5 * older', ''), nohalf)
try:
    nohalf['safe_newton'](lambda x: (x - 1) ** 9, lambda x: 9 * (x - 1) ** 8, 0.0, 3.0, ftol=0.0); needs = False
except RuntimeError:
    needs = True
check('l6:ninefold_root_needs_the_halving_rule', needs and abs(n6['safe_newton'](lambda x: (x - 1) ** 9, lambda x: 9 * (x - 1) ** 8, 0.0, 3.0, ftol=0.0) - 1) < 1e-9)
x, cyc_path = 0.0, []
for k in range(6):
    x = x - cyc(x) / (3 * x * x - 2); cyc_path.append(x)
check('l6:newton_cycles_0_1_and_bracket_fixes_it', cyc_path == [1.0, 0.0] * 3 and abs(n6['safe_newton'](cyc, lambda x: 3 * x * x - 2, -3.0, 0.0) + 1.769292354238631) < 1e-9)
# default ftol stops on the residual
rd = n6['safe_newton'](lambda x: (x - 1) ** 9, lambda x: 9 * (x - 1) ** 8, 0.0, 3.0)
how7 = txt('l6-safe-root-finder.json', 'screens', 7, 'widget', 'how')
pro7 = txt('l6-safe-root-finder.json', 'screens', 7, 'prose')
check('l6:default_ftol_stops_near_1.046_on_the_ninefold_root_and_the_lesson_says_so (corrected claim, fix pass)',
      abs(rd - 1.046) < 5e-4 and (rd - 1) ** 9 <= 1e-12 and abs(1e-12 ** (1 / 9) - 0.0464) < 1e-4 and 0.046 ** 9 < 1e-12
      and 'stops near 1.046' in how7 and 'within 0.046 of 1 has a residual below 1e-12' in how7 and 'bounds the residual, not the error' in pro7,
      'default call returns %.4f; (x - 1)^9 is below 1e-12 for |x - 1| < 1e-12^(1/9) = %.4f' % (rd, 1e-12 ** (1 / 9)))
# clipping to the edge can bounce for ever (arctan on [-5, 5], Newton clipped)
x, clip_path = 5.0, []
for k in range(50):
    x = float(np.clip(x - math.atan(x) * (1 + x * x), -5, 5)); clip_path.append(x)
check('l6:clipped_newton_can_bounce_between_edges', clip_path == [-5.0, 5.0] * 25)
check('l6:call_and_put_bounds', abs(100 - 95 * math.exp(-0.05 / 12) - 5.3950) < 1e-4 and abs(110 * math.exp(-0.05 / 12) - 100 - 9.5426) < 1e-4
      and bool(np.isnan(nv['implied_vols']([5.0], [95], 100.0, 0.05, 1 / 12, ['c'])[0])))
v125 = vg(10, iv[10])
lo125 = brentq(lambda s: price(10, s) - 0.00025, 1e-4, 5); hi125 = brentq(lambda s: price(10, s) - 0.00035, 1e-4, 5)
check('l6:rounded_quote_explains_the_gap', abs(v125 - 0.0218) < 1e-4 and abs(0.00005 / v125 - 0.0023) < 1e-4 and lo125 < 0.2103 < hi125
      and abs(0.0001 / 0.0218 * 100 - 0.46) < 0.01)
q6 = nv['bs_price'](100.0, np.array([100.0]), 0.05, 1 / 12, 6.0, np.array(['c']))
# (corrected claim, fix pass) the solver returns NaN exactly when the price is not strictly inside the range that
# vols 0.0001 to 5 give (prices from vols in the bracket, some of them flattened onto a bound in floating point).
vin = rng.uniform(0.001, 4.99, 400); Kin = rng.uniform(70, 130, 400); kin = np.where(rng.uniform(size=400) < 0.5, 'p', 'c')
Pin = nv['bs_price'](100.0, Kin, 0.05, 1 / 12, vin, kin)
Pin[:40] = Pin[:40] * rng.uniform(0.0, 1.0, 40)          # some stale quotes below their bounds
ivin = nv['implied_vols'](Pin, Kin, 100.0, 0.05, 1 / 12, kin)
inside = (nv['bs_price'](100.0, Kin, 0.05, 1 / 12, np.full(400, 1e-4), kin) < Pin) & (Pin < nv['bs_price'](100.0, Kin, 0.05, 1 / 12, np.full(400, 5.0), kin))
with np.errstate(invalid='ignore'):
    fit = np.abs(nv['bs_price'](100.0, Kin, 0.05, 1 / 12, ivin, kin) - Pin) < 1e-8
ex9 = txt('l6-safe-root-finder.json', 'screens', 9, 'explain', 'text')
check('l6:s9_NaN_exactly_when_the_price_is_not_inside_the_bracket_range (corrected claim, fix pass)',
      bool(np.isnan(nv['implied_vols'](q6, [100.0], 100.0, 0.05, 1 / 12, ['c'])[0])) and bool(np.all(np.isnan(ivin) == ~inside)) and bool(np.all(fit[inside]))
      and 'cannot fail on a valid quote' not in ex9 and 'not strictly inside the range that vols 0.0001 to 5 give' in ex9,
      'vol 6 gives NaN; of 400 random quotes, %d NaNs, each exactly where the price is not strictly inside the bracket range; the rest reprice to 1e-8' % int(np.isnan(ivin).sum()))
K1k = np.linspace(80, 120, 1000); kinds1k = np.where(K1k < 100, 'p', 'c'); true1k = 0.2 + 0.001 * (K1k - 100) ** 2 / 10
P1k = nv['bs_price'](100.0, K1k, 0.05, 1 / 12, true1k, kinds1k)
check('l6:thousand_strikes_recovered', np.max(np.abs(nv['implied_vols'](P1k, K1k, 100.0, 0.05, 1 / 12, kinds1k) - true1k)) < 1e-8)

# ------------------------------------------------------------------ l7


def bary(xs, ys, x):
    xs = np.asarray(xs, float); x = np.atleast_1d(np.asarray(x, float))
    w = np.array([1 / np.prod(xj - np.delete(xs, j)) for j, xj in enumerate(xs)])
    out = np.empty(len(x))
    for i, xv in enumerate(x):
        d = xv - xs
        out[i] = ys[np.argmin(np.abs(d))] if np.any(d == 0) else np.sum(w * np.asarray(ys) / d) / np.sum(w / d)
    return out


rf = lambda x: 1 / (1 + 25 * x ** 2)
g = np.linspace(-1, 1, 4001)
eqn = lambda n: np.linspace(-1, 1, n + 1)
chn = lambda n: np.cos(np.arange(n + 1) * np.pi / n)
maxerr = lambda fn, nodes: float(np.max(np.abs(bary(nodes, fn(nodes), g) - fn(g))))
E = {n: maxerr(rf, eqn(n)) for n in (4, 8, 10, 20)}
C = {n: maxerr(rf, chn(n)) for n in (4, 8, 10, 20)}
check('l7:runge_equal_spacing_grows', abs(E[10] - 1.9157) < 1e-3 and abs(E[20] - 59.82) < 0.02 and abs(E[8] - 1.0452) < 1e-3 and E[4] < E[8] < E[10] < E[20])
check('l7:chebyshev_errors_fall', np.allclose([C[4], C[8], C[10], C[20]], [0.4600, 0.2047, 0.1322, 0.0177], atol=2e-4))
p95 = bary(eqn(10), rf(eqn(10)), 0.95)[0]
check('l7:p10_at_0.95', abs(p95 - 1.9236) < 1e-4 and abs(rf(0.95) - 0.0424) < 1e-4)
check('l7:equal_spacing_is_fine_for_e^x (so "for some smooth functions")', maxerr(np.exp, eqn(20)) < 1e-9 and maxerr(np.exp, eqn(20)) < maxerr(np.exp, eqn(10)) < maxerr(np.exp, eqn(4)))
xs = rng.uniform(-1, 1, 6); ys = rng.normal(size=6)
check('l7:interpolant_unique (barycentric = Vandermonde solve)', np.allclose(bary(xs, ys, g), np.polyval(np.polyfit(xs, ys, 5), g), atol=1e-6))
c4 = np.array([0.0, 0.3, 1.1, 2.0])
check('l7:cubic_reproduced_by_4_points', np.max(np.abs(bary(c4, c4 ** 3, np.linspace(-1, 3, 101)) - np.linspace(-1, 3, 101) ** 3)) < 1e-12)
prod = lambda nodes, x: np.abs(np.prod(np.atleast_1d(x)[:, None] - nodes[None, :], axis=1))
check('l7:node_product', abs(prod(eqn(10), 0.95)[0] - 0.00845) < 1e-5 and abs(prod(eqn(10), 0.05)[0] - 6.71e-5) < 1e-7
      and abs(prod(eqn(10), 0.95)[0] / prod(eqn(10), 0.05)[0] - 126) < 1 and all(prod(chn(n), g).max() <= 2.0 ** (1 - n) for n in (4, 8, 10, 12, 20)))


def lebesgue(nodes, grid):
    tot = np.zeros(len(grid))
    for j in range(len(nodes)):
        tot += np.abs(bary(nodes, np.eye(len(nodes))[j], grid))
    return tot


check('l7:lebesgue_constants', abs(lebesgue(eqn(10), g).max() - 29.9) < 0.05 and abs(lebesgue(chn(10), g).max() - 2.42) < 0.01)
worst = 0
for _ in range(3000):
    d = rng.uniform(-1, 1, 11) * 1e-3
    worst = max(worst, np.max(np.abs(bary(eqn(10), d, g[::8]))))
check('l7:data_error_amplification_bounded_by_lebesgue (3000 random error vectors)', worst <= 0.0299, 'largest seen %.4f against the bound 0.0299' % worst)
kk = np.linspace(75, 125, 5001)
swing = bary(np.linspace(75, 125, 11), 0.001 * (-1.0) ** np.arange(11), kk)
im = int(np.argmax(np.abs(swing)))
lam_there = lebesgue(np.linspace(75, 125, 11), kk[im:im + 1])[0] * 0.001
check('l7:s8_hint0_alternating_is_close_to_not_the_worst_case (corrected claim, fix pass)',
      abs(swing[im]) < lam_there and lam_there - abs(swing[im]) < 0.001
      and 'close to the worst case' in txt('l7-interpolation.json', 'screens', 8, 'hints', 0, 'text'),
      'alternating %.4f against the Lebesgue worst case %.4f at the same strike' % (abs(swing[im]), lam_there))
check('l7:alternating_quote_errors', abs(abs(swing[im]) - 0.0292) < 1e-4 and min(abs(kk[im] - 76.6), abs(kk[im] - 123.4)) < 0.1 and abs(swing[im]) < lam_there <= 0.0299,
      'alternating signs give %.4f; the worst sign pattern at that strike gives %.4f' % (abs(swing[im]), lam_there))

# ------------------------------------------------------------------ l8
t = np.array([1, 2, 3, 5, 7, 10, 20, 30.0]); z = np.array([4.1, 3.95, 3.9, 3.95, 4.05, 4.25, 4.7, 4.8])
cs = CubicSpline(t, z, bc_type='natural')
n8 = solution_ns('l8-splines.json')
check('l8:M_values_match_scipy', np.allclose(cs(t, 2)[1:-1], [0.1372, 0.0510, 0.0033, 0.0107, -0.0047, -0.0041], atol=5e-5)
      and np.allclose(n8['natural_spline_M'](t, z), cs(t, 2), atol=1e-12))
h = np.diff(t)
rhs = [6 * ((z[i + 1] - z[i]) / h[i] - (z[i] - z[i - 1]) / h[i - 1]) for i in range(1, 7)]
T6 = np.array([[4, 1, 0, 0, 0, 0], [1, 6, 2, 0, 0, 0], [0, 2, 8, 2, 0, 0], [0, 0, 2, 10, 3, 0], [0, 0, 0, 3, 26, 10], [0, 0, 0, 0, 10, 40.0]])
check('l8:tridiagonal_system', np.allclose(rhs, [0.60, 0.45, 0.15, 0.10, -0.13, -0.21], atol=1e-9) and np.allclose(np.linalg.solve(T6, rhs), cs(t, 2)[1:-1], atol=1e-12))
from scipy.linalg import solve_banded
ab = np.zeros((3, 6)); ab[0, 1:] = np.diag(T6, 1); ab[1] = np.diag(T6); ab[2, :-1] = np.diag(T6, -1)
check('l8:banded_solve_gives_the_same_M_and_the_text_names_it (corrected claim, fix pass)',
      np.allclose(solve_banded((1, 1), ab, rhs), cs(t, 2)[1:-1], atol=1e-12)
      and 'banded solver handles in $O(n)$' in txt('l8-splines.json', 'screens', 2, 'explain', 'text')
      and 'with a banded solver' in txt('l8-splines.json', 'summary', 'ideas', 1)
      and 'solve_banded' in txt('l8-splines.json', 'screens', 7, 'prose') and 'np.linalg.solve' in txt('l8-splines.json', 'screens', 7, 'widget', 'solution'),
      'the lesson solves densely with np.linalg.solve; solve_banded gives the same M in O(n)')
pol = bary(t, z, [4, 15, 25])
check('l8:degree_7_polynomial_wiggles', np.allclose(pol, [3.9103, 5.1921, -2.58], atol=5e-3))
check('l8:spline_values_and_forwards', abs(cs(4) - 3.9114) < 1e-4 and abs(cs(15) - 4.5297) < 1e-4 and abs(cs(4) + 4 * cs(4, 1) - 4.0273) < 1e-4
      and abs(cs(15) + 15 * cs(15, 1) - 5.2010) < 1e-4)
check('l8:straight_line_forward_jumps_12.5bp', abs((3.95 + 5 * 0.05) - (3.95 + 5 * 0.025) - 0.125) < 1e-12)
fw = lambda x: cs(x) + x * cs(x, 1)
check('l8:spline_forward_continuous_at_knots', all(abs(fw(k + 1e-9) - fw(k - 1e-9)) < 1e-6 for k in t[1:-1]))
z2 = z.copy(); z2[3] += 0.1
cs2 = CubicSpline(t, z2, bc_type='natural')
moves = [100 * float(cs2(x) - cs(x)) for x in (4, 6, 8.5, 15)]
check('l8:bump_is_global', np.allclose(moves, [5.51, 6.42, -2.67, 3.25], atol=0.01) and np.all(np.abs(cs2(t, 2)[1:-1] - cs(t, 2)[1:-1]) > 1e-6))
check('l8:line_gives_line', np.allclose(CubicSpline(t, 2 + 0.3 * t, bc_type='natural')(np.linspace(1, 30, 50)), 2 + 0.3 * np.linspace(1, 30, 50)))
check('l8/hw2:small_splines', abs(CubicSpline([0, 1, 2], [0, 1, 0], bc_type='natural')(1, 2) + 3) < 1e-12 and abs(CubicSpline([0, 1, 3], [0, 2, 2], bc_type='natural')(1, 2) + 2) < 1e-12)
check('l8:zero_prices', abs(100 * math.exp(-4 * float(cs(4)) / 100) - 85.5169) < 1e-4 and abs(100 * math.exp(-4 * 0.03925) - 85.4704) < 1e-4
      and abs(100 / 1.03925 ** 4 - 85.7274) < 1e-4)
se_ = [float(np.max(np.abs(CubicSpline(eqn(n), rf(eqn(n)), bc_type='natural')(g) - rf(g)))) for n in (10, 20, 40, 80)]
check('l8:spline_has_no_runge_swings_on_equal_spacing', se_[0] > se_[1] > se_[2] > se_[3] and se_[3] < 1e-3, 'max errors %s' % [float('%.2g' % v) for v in se_])
# hw2: slope formulas of the spline pieces at a knot
k = 3
left = (z[k] - z[k - 1]) / h[k - 1] + h[k - 1] / 6 * (cs(t, 2)[k - 1] + 2 * cs(t, 2)[k])
right = (z[k + 1] - z[k]) / h[k] - h[k] / 6 * (2 * cs(t, 2)[k] + cs(t, 2)[k + 1])
check('hw2:slope_formulas', abs(left - cs(t[k], 1)) < 1e-12 and abs(right - cs(t[k], 1)) < 1e-12)
nh = solution_ns('homework-2.json')
check('hw2:ytm_book_zero_yield_and_nan', abs(nh['ytm_book']([125.0], [0.05], [5])[0]) < 1e-9 and bool(np.isnan(nh['ytm_book']([130.0], [0.05], [5])[0])))

print('\n%d checks passed, %d failed, %d EXPECTED_FAIL' % (len(PASSES), len(FAILS), len(XFAILS)))
for n in XFAILS:
    print('  EXPECTED_FAIL', n)
sys.exit(1 if FAILS else 0)
