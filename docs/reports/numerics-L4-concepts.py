#!/usr/bin/env python3
"""Concept audit, numerics level 4 (l13 to l17, review-4, homework-4) and the
delta read of four level 2 and 3 code widgets (bisect, safe_newton,
implied_vols, gl_call_price / gl_put_price, ytm_book).

Run from the repo root: python3 docs/reports/numerics-L4-concepts.py
Exits 0 when every claim that the content states correctly checks out.
A check that fails because the content is wrong is marked EXPECTED_FAIL: it
is listed in the output, does not change the exit code, and carries the
corrected assert in a comment beside it.

Independent of docs/reports/numerics-L4-numbers.py: the pricers here are
written afresh (SciPy banded solver, own CRR tree, own quadrature) and are
only compared with the lesson solutions, which are loaded from the JSON.
Written under CPython with NumPy 2.5; the app runs Pyodide 0.27.7 with
NumPy 2.0.2. default_rng(seed).standard_normal is stream-stable across
those versions, but the last one or two printed digits of a float can differ.
"""
import json, math, os, sys, time, warnings
import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from scipy.stats import norm
from scipy import integrate

warnings.simplefilter('ignore')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, 'app', 'content', 'courses', 'numerics')
FAILS, XFAILS, NPASS = [], [], [0]


def chk(name, cond, detail=''):
    if cond:
        NPASS[0] += 1
    else:
        FAILS.append(name)
        print(f'FAIL  {name}  {detail}')


def near(name, got, want, tol):
    chk(name, abs(got - want) <= tol, f'got {got!r}, content says {want!r}')


def xfail(name, content_claim_holds, detail):
    """content_claim_holds is the truth of the claim as the content states it."""
    if content_claim_holds:
        FAILS.append(name + ' (EXPECTED_FAIL now passes: content was fixed, update this check)')
        print(f'FAIL  {name}: expected-fail check now passes')
    else:
        XFAILS.append(name)
        print(f'EXPECTED_FAIL  {name}  {detail}')


def load(f):
    return json.load(open(os.path.join(C, f + '.json')))


def widgets(doc):
    out = {}
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget') or {}
            if 'solution' in w:
                out[f'{key}[{i}]'] = w
    return out


def close(a, b, tol):
    if hasattr(a, 'tolist'): a = a.tolist()
    if hasattr(b, 'tolist'): b = b.tolist()
    if isinstance(b, dict):
        return isinstance(a, dict) and set(a) == set(b) and all(close(a[k], b[k], tol) for k in b)
    if isinstance(b, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(b, str) or b is None:
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if tol is None:
            return a == b
        return abs(a - b) <= tol.get('abs', 0) + tol.get('rel', 0) * abs(b)
    return a == b


def run_tests(src, tests):
    ns = {}
    try:
        exec(src, ns)
    except Exception as e:
        return [f'load error {type(e).__name__}'] * len(tests), ns
    res = []
    for t in tests:
        cmp_ = t.get('compare', 'isclose')
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            if cmp_ == 'raises':
                try:
                    v = eval(t['call'], ns)
                    res.append(f'no error, value {v!r}')
                except Exception as e:
                    res.append(True if any(k.__name__ == t['expect'] for k in type(e).__mro__) else f'raised {type(e).__name__}')
                continue
            got = eval(t['call'], ns)
            exp = t['expect']
            if isinstance(exp, str):
                try:
                    exp = eval(exp, ns)
                except Exception:
                    pass
            tol = None if cmp_ == 'equal' else (t.get('tol') or {'abs': 1e-9, 'rel': 1e-9})
            res.append(True if close(got, exp, tol) else f'got {got!r}, expected {exp!r}')
        except Exception as e:
            res.append(f'{type(e).__name__}: {e}')
    return res, ns


NS = {}


def widget_check(fname, path, min_starter_fail=None):
    """Solution passes every hidden test and example; starter fails the tests."""
    w = widgets(load(fname))[path]
    pre = w.get('prelude', '') + '\n'
    tests = w.get('tests', [])
    rs, ns = run_tests(pre + w['solution'], tests + w.get('examples', []))
    bad = [(t['call'], r) for t, r in zip(tests + w.get('examples', []), rs) if r is not True]
    chk(f'{fname} {path}: solution passes {len(rs)} tests and examples', not bad, str(bad[:2]))
    rt, _ = run_tests(pre + w['starter'], tests)
    nfail = sum(r is not True for r in rt)
    need = len(tests) if min_starter_fail is None else min_starter_fail
    chk(f'{fname} {path}: starter fails at least {need} of {len(tests)} tests', nfail >= need, f'fails {nfail}')
    NS[(fname, path)] = ns
    return ns


# ---------------------------------------------------------------- own pricers
def bs(S, K, r, sig, T, kind='call'):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    c = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return c if kind == 'call' else c - S + K * math.exp(-r * T)


def march(S0, K, r, sig, T, Smax, M, N, theta, implicit_start=0, kind='call', full=False):
    """Theta-scheme with a SciPy banded solve; independent of the lesson code."""
    dS, dt = Smax / M, T / N
    j = np.arange(M + 1.0)
    S = j * dS
    if kind == 'call':
        V = np.maximum(S - K, 0.0)
    elif kind == 'put':
        V = np.maximum(K - S, 0.0)
    else:                                   # forward
        V = S - K
    al = 0.5 * (sig ** 2 * j ** 2 - r * j)
    be = -(sig ** 2 * j ** 2 + r)
    ga = 0.5 * (sig ** 2 * j ** 2 + r * j)
    vmax = np.abs(V).max()
    for n in range(N):
        th = 1.0 if n < implicit_start else theta
        disc = K * math.exp(-r * (n + 1) * dt)
        lo, hi = {'call': (0.0, Smax - disc), 'put': (disc, 0.0), 'forward': (-disc, Smax - disc)}[kind]
        LV = al[1:-1] * V[:-2] + be[1:-1] * V[1:-1] + ga[1:-1] * V[2:]
        rhs = V[1:-1] + (1 - th) * dt * LV
        if th == 0.0:
            inner = rhs
        else:
            rhs[0] += th * dt * al[1] * lo
            rhs[-1] += th * dt * ga[-2] * hi
            ab = np.zeros((3, M - 1))
            ab[0, 1:] = -th * dt * ga[1:-2]
            ab[1] = 1 - th * dt * be[1:-1]
            ab[2, :-1] = -th * dt * al[2:-1]
            inner = solve_banded((1, 1), ab, rhs)
        V = np.concatenate(([lo], inner, [hi]))
        vmax = max(vmax, np.abs(V).max()) if np.all(np.isfinite(V)) else float('inf')
    if full:
        return S, V
    return float(np.interp(S0, S, V))


def crr(S0, K, r, sig, T, n):
    dt = T / n
    u = math.exp(sig * math.sqrt(dt)); d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    k = np.arange(n + 1)
    from scipy.stats import binom
    ST = S0 * u ** k * d ** (n - k)
    return float(math.exp(-r * T) * np.sum(binom.pmf(k, n, p) * np.maximum(ST - K, 0.0)))


def crr_put(S0, K, r, sig, T, n):
    return crr(S0, K, r, sig, T, n) - S0 + K * math.exp(-r * T)


def doc_call(S, K, H, r, sig, T):
    """Down-and-out call, H < K, continuous barrier (Reiner and Rubinstein; Hull ch. 26)."""
    lam = (r + sig * sig / 2) / sig ** 2
    y = math.log(H * H / (S * K)) / (sig * math.sqrt(T)) + lam * sig * math.sqrt(T)
    cdi = S * (H / S) ** (2 * lam) * norm.cdf(y) - K * math.exp(-r * T) * (H / S) ** (2 * lam - 2) * norm.cdf(y - sig * math.sqrt(T))
    return bs(S, K, r, sig, T) - cdi


S0, K0, R, SIG, T1 = 100.0, 100.0, 0.05, 0.2, 1.0
BS0 = bs(S0, K0, R, SIG, T1)
t0 = time.time()

# =============================================================== PART A
print('--- Part A: code widgets, solution against hidden tests, starter fails')
ns13 = widget_check('l13-finite-differences', 'screens[8]')
ns14a = widget_check('l14-implicit-and-crank-nicolson', 'screens[8]')
ns14 = widget_check('l14-implicit-and-crank-nicolson', 'screens[9]')
ns15 = widget_check('l15-monte-carlo-error', 'screens[8]')
ns16 = widget_check('l16-control-variates', 'screens[9]')
ns16b = widget_check('l16-control-variates', 'screens[10]', min_starter_fail=4)  # the starter ships geometric_asian_call
ns17 = widget_check('l17-three-ways', 'screens[8]')
nsh4 = widget_check('homework-4', 'items[6]')

print('--- l13 explicit finite differences')
near('formula 10.450584', BS0, 10.450584, 5e-7)
ex = ns13['explicit_bs']
near('lesson explicit = own march, M=100 N=500', ex(100, 100, R, SIG, 1, 200, 100, 500), march(100, 100, R, SIG, 1, 200, 100, 500, 0.0), 1e-10)
near('grid 10.442791', march(100, 100, R, SIG, 1, 200, 100, 500, 0.0), 10.442791, 5e-7)
near('one step 0.2050', march(100, 100, R, SIG, 0.002, 200, 100, 1, 0.0), 0.2050, 5e-5)
near('formula at tau 0.002 is 0.3618', bs(100, 100, R, SIG, 0.002), 0.3618, 5e-5)
near('tau 0.1: grid 2.7481', march(100, 100, R, SIG, 0.1, 200, 100, 50, 0.0), 2.7481, 5e-5)
near('tau 0.1: formula 2.7737', bs(100, 100, R, SIG, 0.1), 2.7737, 5e-5)
near('tau 0.5: grid 6.8775', march(100, 100, R, SIG, 0.5, 200, 100, 250, 0.0), 6.8775, 5e-5)
near('tau 0.5: formula 6.8887', bs(100, 100, R, SIG, 0.5), 6.8887, 5e-5)
a50, b50, c50 = 0.5 * 0.002 * (0.04 * 2500 - 0.05 * 50), -0.002 * (0.04 * 2500 + 0.05), 0.5 * 0.002 * (0.04 * 2500 + 0.05 * 50)
chk('weights at j=50', abs(a50 - 0.0975) < 1e-12 and abs(1 + b50 - 0.7999) < 1e-12 and abs(c50 - 0.1025) < 1e-12)
near('weights sum to 1 - r dt', a50 + 1 + b50 + c50, 0.9999, 1e-12)
e100 = march(100, 100, R, SIG, 1, 200, 100, 500, 0.0) - BS0
e200 = march(100, 100, R, SIG, 1, 200, 200, 1700, 0.0) - BS0
near('error at dS=2 is -0.0078', e100, -0.0078, 5e-5)
near('M=200 N=1700 gives 10.4487', e200 + BS0, 10.4487, 5e-5)
near('error at dS=1 is -0.0019', e200, -0.0019, 5e-5)
# what is space error, what is time error (l13 screens[4].explain, summary.ideas[1])
space100 = march(100, 100, R, SIG, 1, 200, 100, 20000, 0.5, 2) - BS0      # time error negligible
space200 = march(100, 100, R, SIG, 1, 200, 200, 20000, 0.5, 2) - BS0
time100 = e100 - space100
print(f'   M=100: space error {space100:.5f}, explicit time error at N=500 {time100:+.5f};'
      f' M=200: space {space200:.5f}, time at N=1700 {e200 - space200:+.5f}')
chk('the dS^2 term is the larger part of the error at both grids', abs(space100) > 3 * abs(time100) and abs(space200) > 3 * abs(e200 - space200))
near('space error quarters (ratio 4.0)', space100 / space200, 4.0, 0.05)
# the measured ratio 4.2 mixes a 4.0 space ratio with a 3.4 time ratio
near('measured ratio of total errors', e100 / e200, 4.2, 0.1)
S, V = march(100, 100, R, SIG, 1, 200, 100, 330, 0.0, full=True)
near('N=330 price 10.4439', float(np.interp(100, S, V)), 10.4439, 5e-5)
chk('N=330 largest value about 7.5e14, near the top', 7.0e14 < np.abs(V).max() < 8.0e14 and S[np.abs(V).argmax()] > 180, f'{np.abs(V).max():.3g} at {S[np.abs(V).argmax()]}')
near('N=300 price 379,169', march(100, 100, R, SIG, 1, 200, 100, 300, 0.0), 379169, 1)
v250 = march(100, 100, R, SIG, 1, 200, 100, 250, 0.0)
chk('N=250 price about 4.5e30', 4.45e30 < abs(v250) < 4.55e30, f'{v250:.3g}')
S, V = march(100, 100, R, SIG, 1, 200, 100, 500, 0.0, full=True)
near('N=500 largest value 104.88 at Smax', V.max(), 104.88, 5e-3)
v277 = ex(100, 100, R, SIG, 1, 200, 200, 500)
chk('M=200 N=500 about 4.1e277', 4.05e277 < abs(v277) < 4.15e277, f'{v277:.3g}')
chk('bounds: N >= 401, 1601, 3601, 101, 901', [math.ceil(0.04 * m * m + 0.05) for m in (100, 200, 300, 50, 150)] == [401, 1601, 3601, 101, 901])
# is the bound necessary? ("safe only while", l13 summary.ideas[2])
def radius(M, N):
    """Spectral radius of the explicit step matrix I + dt L on the interior nodes."""
    j = np.arange(1.0, M)
    dt = 1.0 / N
    G = np.diag(1 - dt * (0.04 * j ** 2 + 0.05)) + np.diag(0.5 * dt * (0.04 * j ** 2 + 0.05 * j)[:-1], 1) \
        + np.diag(0.5 * dt * (0.04 * j ** 2 - 0.05 * j)[1:], -1)
    return np.abs(np.linalg.eigvals(G)).max()
stable_N = [N for N in range(340, 402) if radius(100, N) <= 1 + 1e-12]
print(f'   M=100: the step matrix has spectral radius <= 1 from N = {min(stable_N)} (the bound says 401);'
      f' frozen-coefficient von Neumann at j = M-1 gives N >= {0.04 * 99 ** 2 + 0.025:.2f}')
chk('the bound is sufficient: spectral radius <= 1 for N >= 401', all(radius(100, N) <= 1 + 1e-12 for N in (401, 450, 500)) and radius(200, 1601) <= 1 + 1e-12)
chk('well below the bound the step matrix amplifies', radius(100, 330) > 1.05 and radius(100, 300) > 1.2)
xfail('l13 "safe only while dt <= 1/(sigma^2 M^2 + r)": some N below 401 are stable too',
      min(stable_N) >= 401, f'spectral radius <= 1 from N = {min(stable_N)}')
# corrected assert: assert min(stable_N) < 401   (the bound is sufficient and close to sharp, not necessary)
# growth reaches S = 100 if the unstable march carries on (quiz[1])
chk('N=330 step size, twice as long a march: blow-up reaches S=100', abs(march(100, 100, R, SIG, 2, 200, 100, 660, 0.0)) > 1e3)
# where the explicit grid's error is largest (l13 screens[4].explain)
S, V = march(100, 100, R, SIG, 1, 200, 100, 500, 0.0, full=True)
errS = np.array([V[j] - bs(S[j], 100, R, SIG, 1) for j in range(35, 66)])
chk('explicit error is largest in size near the strike', 90 <= S[35 + np.abs(errS).argmax()] <= 110, f'{S[35 + np.abs(errS).argmax()]}')
# l13 screens[9]: is the European error a fair allowance for a barrier on the same explicit grid?
def explicit_doc(M, N, H=90.0):
    dS, dt = 200 / M, 1.0 / N
    j = np.arange(M + 1.0); S = j * dS
    V = np.where(S > H, np.maximum(S - 100, 0.0), 0.0)
    a = 0.5 * dt * (0.04 * j ** 2 - 0.05 * j); b = -dt * (0.04 * j ** 2 + 0.05); c = 0.5 * dt * (0.04 * j ** 2 + 0.05 * j)
    for n in range(N):
        V[1:-1] = a[1:-1] * V[:-2] + (1 + b[1:-1]) * V[1:-1] + c[1:-1] * V[2:]
        V[S <= H] = 0.0
        V[-1] = 200 - 100 * math.exp(-0.05 * (n + 1) * dt)
    return float(np.interp(100, S, V))
eb = explicit_doc(100, 500) - doc_call(100, 100, 90, R, SIG, 1)
print(f'   explicit grid M=100 N=500: European error {e100:+.4f}, down-and-out (H = 90 on a node) error {eb:+.4f}')
chk('the barrier error on the same grid is of the same size as the European error (within a factor of 3)', abs(e100) / 3 < abs(eb) < 3 * abs(e100), f'{eb}')
near('K=0 call returns the share exactly', ex(100, 0, R, SIG, 1, 200, 100, 500), 100.0, 1e-9)
near('forward: time-step error 2.4e-4', abs(march(100, 100, R, SIG, 1, 200, 100, 500, 0.0, kind='forward') - (100 - 100 * math.exp(-R))), 2.4e-4, 5e-6)
near('h4: 1+b at j=80, N=500', 1 - 0.002 * (0.04 * 6400 + 0.05), 0.4879, 5e-5)
near('h4: 1+b at j=99, N=500', 1 - 0.002 * (0.04 * 9801 + 0.05), 0.2158, 5e-5)
near('h4: 1+b at j=99, N=400', 1 - 0.0025 * (0.04 * 9801 + 0.05), 0.0198, 5e-5)
chk('h4: centre weight at j=99 negative below N=393', 1 - (0.04 * 9801 + 0.05) / 392 < 0 < 1 - (0.04 * 9801 + 0.05) / 393)
e400 = march(100, 100, R, SIG, 1, 200, 400, 6401, 0.0) - BS0
near('review: explicit M=400 N=6401 error -0.00045', e400, -0.00045, 5e-6)

print('--- l14 implicit and Crank-Nicolson')
th = ns14['theta_bs']
for (M, N, wi, wc) in [(100, 25, -0.0519, -0.00950), (100, 50, -0.0309, -0.00980), (100, 100, -0.0204, -0.00987)]:
    near(f'implicit error M={M} N={N}', march(100, 100, R, SIG, 1, 200, M, N, 1.0) - BS0, wi, 5e-5)
    near(f'CN error M={M} N={N}', march(100, 100, R, SIG, 1, 200, M, N, 0.5) - BS0, wc, 5e-6)
    near(f'lesson theta_bs = own march M={M} N={N}', th(100, 100, R, SIG, 1, 200, M, N, 0.5), march(100, 100, R, SIG, 1, 200, M, N, 0.5), 1e-9)
cn200 = march(100, 100, R, SIG, 1, 200, 200, 200, 0.5) - BS0
cn400 = march(100, 100, R, SIG, 1, 200, 400, 400, 0.5) - BS0
near('CN error M=N=200', cn200, -0.00246, 5e-6)
near('CN error M=N=400', cn400, -0.000616, 5e-7)
near('CN ratio 4.0', cn200 / cn400, 4.0, 0.05)
imp = [march(100, 100, R, SIG, 1, 200, 100, N, 1.0) - BS0 + 0.0099 for N in (25, 50, 100)]
chk('implicit remainders -0.042, -0.021, -0.0105 halve', all(abs(a - b) < 6e-4 for a, b in zip(imp, (-0.042, -0.021, -0.0105))), str(imp))
def gamma_at(S, V, s0=100.0):
    j = int(round(s0 / (S[1] - S[0])))
    return (V[j + 1] - 2 * V[j] + V[j - 1]) / (S[1] - S[0]) ** 2
gam = norm.pdf(0.35) / (100 * 0.2)
near('formula gamma 0.018762', gam, 0.018762, 5e-7)
for label, theta, start, wp, wg, tg in [('CN', 0.5, 0, 10.2767, 1.2526, 5e-5), ('implicit', 1.0, 0, 10.3457, 0.01957, 5e-6), ('CN after 2 implicit', 0.5, 2, 10.4324, 0.01904, 5e-6)]:
    S, V = march(100, 100, R, SIG, 1, 200, 400, 10, theta, start, full=True)
    near(f'N=10 {label}: price', float(np.interp(100, S, V)), wp, 5e-5)
    near(f'N=10 {label}: gamma', gamma_at(S, V), wg, tg)
near('nu at the strike, M=400 N=10', 0.04 * 1e4 * 0.1 / (2 * 0.25), 80, 1e-9)
chk('CN factors -0.951, -0.980, -0.9876', abs(-39 / 41 + 0.951) < 5e-4 and abs(-99 / 101 + 0.980) < 5e-4 and abs(-159 / 161 + 0.9876) < 5e-5)
near('after ten steps 88% is left', (159 / 161) ** 10, 0.88, 5e-3)
near('nu <= 0.4 at every node for M=100 N=500', 0.04 * 100 ** 2 * 0.002 / 2, 0.4, 1e-12)
for theta, want in [(0.0, 10.4428), (1.0, 10.4386), (0.5, 10.4407)]:
    near(f'M=100 N=500 theta={theta}', march(100, 100, R, SIG, 1, 200, 100, 500, theta), want, 5e-5)
# theta-scheme factor stays in (-1, 1] for theta >= 1/2 and tends to -(1-theta)/theta
z = np.logspace(-6, 8, 2000)
for theta in (0.5, 0.6, 0.75, 1.0):
    g = (1 - (1 - theta) * z) / (1 + theta * z)
    chk(f'theta={theta}: factor in (-1, 1]', g.max() <= 1 and g.min() >= -1 - 1e-7)
    near(f'theta={theta}: limit', g[-1], -(1 - theta) / theta, 1e-6)
chk('theta=0.4 leaves [-1, 1] for large z', ((1 - 0.6 * z) / (1 + 0.4 * z)).min() < -1)
# Thomas: operation count of the lesson solution (l14 "about 3M operations")
class F(float):
    ops = 0
    def _w(self, o, f):
        F.ops += 1
        return F(f(float(self), float(o)))
    def __add__(s, o): return s._w(o, lambda a, b: a + b)
    def __sub__(s, o): return s._w(o, lambda a, b: a - b)
    def __rsub__(s, o): return s._w(o, lambda a, b: b - a)
    def __mul__(s, o): return s._w(o, lambda a, b: a * b)
    def __rmul__(s, o): return s._w(o, lambda a, b: a * b)
    def __truediv__(s, o): return s._w(o, lambda a, b: a / b)
    def __rtruediv__(s, o): return s._w(o, lambda a, b: b / a)
src = widgets(load('l14-implicit-and-crank-nicolson'))['screens[8]']['solution'].replace('list(map(float, v))', 'list(map(F, v))')
nsF = {'F': F}
exec(src, nsF)
n = 399
F.ops = 0
nsF['thomas']([-1.0] * n, [2.5] * n, [-1.0] * n, [1.0] * n)
print(f'   Thomas, n = {n}: {F.ops} arithmetic operations = {F.ops / n:.2f} n (3 multiplies, 2 divides, 3 subtracts a row)')
xfail('l14 "about 3M operations" for Thomas (1,200 for M = 400)', abs(F.ops / n - 3) < 0.5, f'counted {F.ops / n:.1f} n')
# corrected assert: assert abs(F.ops / n - 8) < 0.1     (8 operations a row: 3 multiplies, 2 divides, 3 subtracts;
#   so "about 5M multiplications and divisions", 2,000 for M = 400, against M^3/3 multiplications for a dense solve)
near('dense solve M^3/3 at M=400 is 21 million', 400 ** 3 / 3, 21e6, 0.5e6)
A = np.diag([2.0] * 4) + np.diag([-1.0] * 3, 1) + np.diag([-1.0] * 3, -1)
chk('4 by 4 system has x = (1,1,1,1)', np.allclose(np.linalg.solve(A, [1, 0, 0, 1]), 1))

print('--- l15 Monte Carlo error')
f_pay = lambda zz: math.exp(-R) * np.maximum(100 * np.exp(0.03 + 0.2 * zz) - 100, 0.0)
x_sh = lambda zz: math.exp(-R) * 100 * np.exp(0.03 + 0.2 * zz)
E = lambda g: integrate.quad(lambda zz: g(zz) * norm.pdf(zz), -12, 12, points=[-0.15, 0.15], epsabs=1e-12, epsrel=1e-12, limit=400)[0]
EY, EY2 = E(f_pay), E(lambda q: f_pay(q) ** 2)
varY = EY2 - EY ** 2
s_exact = math.sqrt(varY)
near('E[Y] = Black-Scholes', EY, BS0, 1e-8)
near('s = 14.7194', s_exact, 14.7194, 5e-5)
chk('SE table 1.472, 0.465, 0.147, 0.0465', all(abs(14.7194 / math.sqrt(n) - w) < 5e-4 for n, w in [(100, 1.472), (1000, 0.465), (1e4, 0.147), (1e5, 0.0465)]))
chk('paths for a penny: 2,166,609 unrounded, 2,166,608 from 14.7194', math.ceil((s_exact / 0.01) ** 2) == 2166609 and math.ceil((14.7194 / 0.01) ** 2) == 2166608)
mc = ns15['mc_call']
p0, se0 = mc(100, 100, R, SIG, 1, 100_000, 0)
p1, se1 = mc(100, 100, R, SIG, 1, 100_000, 1)
chk('seed 0: 10.4362, 0.0465, -0.31 SE', abs(p0 - 10.4362) < 5e-5 and abs(se0 - 0.0465) < 5e-5 and abs((p0 - BS0) / se0 + 0.31) < 5e-3)
chk('seed 1: 10.3578, 0.0464, -2.00 SE, interval misses', abs(p1 - 10.3578) < 5e-5 and abs((p1 - BS0) / se1 + 2.00) < 5e-3 and p1 + 1.96 * se1 < BS0)
near('seed 0 lower end 10.3450', p0 - 1.96 * se0, 10.3450, 5e-5)
# coverage of the 95% interval: "misses in one run in 20"
rng = np.random.default_rng(2024)
zz = rng.standard_normal((20000, 2000))
yy = f_pay(zz)
m_, s_ = yy.mean(axis=1), yy.std(axis=1, ddof=1) / math.sqrt(2000)
miss = np.mean(np.abs(m_ - BS0) > 1.96 * s_)
print(f'   95% interval, n = 2,000 paths, 20,000 runs: misses {miss:.4f} (binomial SE 0.0015)')
chk('95% interval misses about one run in 20', 0.044 < miss < 0.060, f'{miss}')
del zz, yy
# barrier: continuous closed form, Broadie-Glasserman-Kou shift, and a simulation
near('down-and-out continuous 8.6655', doc_call(100, 100, 90, R, SIG, 1), 8.6655, 5e-5)
for m, want in [(12, 9.580), (52, 9.174), (252, 8.914)]:
    near(f'shifted closed form, {m} dates', doc_call(100, 100, 90 * math.exp(-0.5826 * SIG * math.sqrt(1 / m)), R, SIG, 1), want, 5e-4)
def sim_barrier(m, n, seed, also_euro=False):
    rng = np.random.default_rng(seed)
    alive = np.ones(n, bool)
    logS = np.full(n, math.log(100.0))
    dt = 1 / m
    for _ in range(m):
        logS += (R - SIG ** 2 / 2) * dt + SIG * math.sqrt(dt) * rng.standard_normal(n)
        alive &= logS > math.log(90.0)
    euro = math.exp(-R) * np.maximum(np.exp(logS) - 100, 0.0)
    y = euro * alive
    if also_euro:
        return y, euro
    return y.mean(), y.std(ddof=1) / math.sqrt(n)
for m, want_sim, shifted in [(12, 9.572, 9.580), (52, 9.152, 9.174), (252, 8.936, 8.914)]:
    npth = {12: 2_000_000, 52: 1_000_000, 252: 400_000}[m]
    pm, sem = sim_barrier(m, npth, 77 + m)
    print(f'   barrier on {m} dates, {npth:,} own paths: {pm:.3f} (SE {sem:.3f}); content {want_sim} (0.033), shifted {shifted}')
    chk(f'{m} dates: own simulation agrees with the content figure (4 SE of the difference)', abs(pm - want_sim) < 4 * math.hypot(sem, 0.033))
    chk(f'{m} dates: discrete price is above the continuous 8.6655 by many SE (bias, not noise)', pm - 8.6655 > 6 * sem)
    chk(f'{m} dates: SE at 200,000 paths is about 0.033', abs(sem * math.sqrt(npth / 200_000) - 0.033) < 0.002)
    chk(f'{m} dates: own simulation agrees with the shifted closed form (4 SE plus 1p for the approximation)', abs(pm - shifted) < 4 * sem + 0.01)
near('BS(110, 100, 3%, 25%, 0.5)', bs(110, 100, 0.03, 0.25, 0.5), 14.46696108, 5e-8)
chk('grid rate n^(-2/d): d=12 gives -1/6; tie at d=4', abs(-2 / 12 + 1 / 6) < 1e-15 and 2 / 4 == 0.5)

print('--- l16 control variates and antithetics')
varX = E(lambda q: x_sh(q) ** 2) - 100.0 ** 2
cov = E(lambda q: f_pay(q) * x_sh(q)) - EY * 100
rho = cov / math.sqrt(varY * varX)
near('Var(Y) 216.66', varY, 216.66, 5e-3)
near('Var(X) 408.11', varX, 408.11, 5e-3)
near('Var(X) = S0^2 (e^(sigma^2 T) - 1)', varX, 1e4 * (math.exp(0.04) - 1), 1e-6)
near('Cov 274.91', cov, 274.91, 5e-3)
near('b* 0.6736', cov / varX, 0.6736, 5e-5)
near('rho 0.92450', rho, 0.92450, 5e-6)
near('residual variance 31.48', varY * (1 - rho ** 2), 31.48, 5e-3)
near('factor 6.88', 1 / (1 - rho ** 2), 6.88, 5e-3)
near('b = 1 leaves 74.95', varY - 2 * cov + varX, 74.95, 1e-2)
near('paths with the control, about 315,000', 2166609 * (1 - rho ** 2), 315000, 500)
near('sqrt(31.48) = 5.61', math.sqrt(varY * (1 - rho ** 2)), 5.61, 5e-3)
chk('factor 5.26 at 0.9, 50 at 0.99, 10.26 at 0.95, 1,000 at 0.9995, 25.3 at 0.98',
    abs(1 / 0.19 - 5.26) < 5e-3 and abs(1 / (1 - 0.99 ** 2) - 50) < 0.5 and abs(1 / (1 - 0.9025) - 10.26) < 5e-3
    and abs(1 / (1 - 0.9995 ** 2) - 1000) < 1 and abs(1 / (1 - 0.98 ** 2) - 25.3) < 0.05)
cv = ns16['mc_control']
pc, sec, bhat = cv(100, 100, R, SIG, 1, 100_000, 0)
chk('seed 0 control: 10.4484, 0.017764, b 0.67307, 0.12 SE away', abs(pc - 10.4484) < 5e-5 and abs(sec - 0.017764) < 5e-7 and abs(bhat - 0.67307) < 5e-6 and abs((BS0 - pc) / sec - 0.12) < 6e-3)
near('observed factor 6.86', (se0 / sec) ** 2, 6.86, 5e-3)
pc1, sec1, _ = cv(100, 100, R, SIG, 1, 100_000, 1)
chk('seed 1 control: 10.4275, 0.0177, -1.30 SE', abs(pc1 - 10.4275) < 5e-5 and abs(sec1 - 0.0177) < 5e-5 and abs((pc1 - BS0) / sec1 + 1.30) < 6e-3)
# antithetic pairs
c_pair = E(lambda q: f_pay(q) * f_pay(-q)) - EY ** 2
near('pair correlation -0.501', c_pair / varY, -0.501, 5e-4)
near('pair-mean variance 54.06', 0.5 * varY * (1 + c_pair / varY), 54.06, 1e-2)
near('two independent paths 108.33', varY / 2, 108.33, 5e-3)
A_ = lambda q: 0.5 * (f_pay(q) + f_pay(-q)); XA = lambda q: 0.5 * (x_sh(q) + x_sh(-q))
vA, vXA = E(lambda q: A_(q) ** 2) - EY ** 2, E(lambda q: XA(q) ** 2) - 1e4
cA = E(lambda q: A_(q) * XA(q)) - EY * 100
near('pairs and control together leave 3.78', vA - cA ** 2 / vXA, 3.78, 1e-2)
pa, sea = ns16['mc_antithetic'](100, 100, R, SIG, 1, 100_000, 0)
chk('seed 0 pairs: 10.4721, 0.0329', abs(pa - 10.4721) < 5e-5 and abs(sea - 0.0329) < 5e-5)
# l16 screens[9].explain: "Count the error over pairs, not payoffs, or it comes out too small."
zz = np.random.default_rng(0).standard_normal(50_000)
pooled = np.concatenate([f_pay(zz), f_pay(-zz)])
naive = pooled.std(ddof=1) / math.sqrt(100_000)
print(f'   antithetic call, seed 0: SE over 50,000 pairs {sea:.4f}; SE over 100,000 payoffs as if independent {naive:.4f}')
xfail('l16 screens[9].explain: counting the antithetic call\'s error over payoffs gives too small an SE', naive < sea,
      f'over payoffs {naive:.4f} is larger than over pairs {sea:.4f}: the pairs are negatively correlated')
# corrected assert: assert naive > sea     (too large for the call; too small only when the pair correlation is positive)
strad = lambda q: math.exp(-R) * np.abs(100 * np.exp(0.03 + 0.2 * q) - 100)
ES = E(strad); vS = E(lambda q: strad(q) ** 2) - ES ** 2
cS = (E(lambda q: strad(q) * strad(-q)) - ES ** 2) / vS
near('straddle 16.0241', ES, 16.0241, 5e-5)
near('straddle variance 175.1', vS, 175.1, 0.05)
near('straddle pair correlation +0.645', cS, 0.645, 5e-4)
near('straddle pair-mean variance 144.0', 0.5 * vS * (1 + cS), 144.0, 0.05)
near('straddle efficiency 0.61', (vS / 2) / (0.5 * vS * (1 + cS)), 0.61, 5e-3)
dig = lambda q: (q > -0.15) * 1.0
Ed = E(dig)
chk('digital: pair correlation negative', E(lambda q: dig(q) * dig(-q)) - Ed ** 2 < 0)
putp = lambda q: math.exp(-R) * np.maximum(100 - 100 * np.exp(0.03 + 0.2 * q), 0.0)
Ep = E(putp)
chk('put: pair correlation negative', E(lambda q: putp(q) * putp(-q)) - Ep ** 2 < 0)
# l16 summary.trap: "for a payoff that rises on both sides they increase the variance"
s70 = lambda q: math.exp(-R) * np.abs(100 * np.exp(0.03 + 0.2 * q) - 70)
E70 = integrate.quad(lambda q: s70(q) * norm.pdf(q), -12, 12, points=[(math.log(0.7) - 0.03) / 0.2, -(math.log(0.7) - 0.03) / 0.2], epsabs=1e-12, limit=400)[0]
I70 = lambda g: integrate.quad(lambda q: g(q) * norm.pdf(q), -12, 12, points=[(math.log(0.7) - 0.03) / 0.2, -(math.log(0.7) - 0.03) / 0.2], epsabs=1e-12, limit=400)[0]
v70 = I70(lambda q: s70(q) ** 2) - E70 ** 2
c70 = (I70(lambda q: s70(q) * s70(-q)) - E70 ** 2) / v70
print(f'   |S_T - 70| (rises on both sides of 70): pair correlation {c70:+.3f}')
xfail('l16 summary.trap: antithetics increase the variance of any payoff that rises on both sides', c70 > 0,
      f'|S_T - 70| has pair correlation {c70:+.3f}, so the pairs help')
# corrected assert: assert c70 < 0     ("can increase": the sign of Cov(f(Z), f(-Z)) decides)
# Asian
ag = ns16b['asian_geometric_cv']; geo = ns16b['geometric_asian_call']
near('geometric Asian 5.9402', geo(100, 100, R, SIG, 1, 12), 5.9402, 5e-5)
zz = np.random.default_rng(0).standard_normal((100_000, 12))
logS = math.log(100) + np.cumsum(0.03 / 12 + 0.2 * math.sqrt(1 / 12) * zz, axis=1)
ya = math.exp(-R) * np.maximum(np.exp(logS).mean(axis=1) - 100, 0.0)
xg = math.exp(-R) * np.maximum(np.exp(logS.mean(axis=1)) - 100, 0.0)
chk('Asian plain seed 0: 6.1722 (0.0269)', abs(ya.mean() - 6.1722) < 5e-5 and abs(ya.std(ddof=1) / math.sqrt(1e5) - 0.0269) < 5e-5)
near('Asian rho 0.9996', np.corrcoef(ya, xg)[0, 1], 0.9996, 5e-5)
near('geometric closed form = mean of its simulated payoff (3 SE)', xg.mean(), geo(100, 100, R, SIG, 1, 12), 3 * xg.std() / math.sqrt(1e5))
a0, a1 = ag(100, 100, R, SIG, 1, 12, 100_000, 0), ag(100, 100, R, SIG, 1, 12, 100_000, 1)
chk('Asian control: 6.1561 (0.00075) and 6.1558 (0.00074)', abs(a0[0] - 6.1561) < 5e-5 and abs(a0[1] - 0.00075) < 5e-6 and abs(a1[0] - 6.1558) < 5e-5 and abs(a1[1] - 0.00074) < 5e-6)
near('Asian factor 1,281', (ya.std(ddof=1) / math.sqrt(1e5) / a0[1]) ** 2, 1281, 15)
del zz, logS
# bias from estimating b on the same paths (l16 screens[1], [5], [10], quiz[1])
rng = np.random.default_rng(99)
for npath, reps in [(10, 400_000), (40, 200_000)]:
    zz = rng.standard_normal((reps, npath))
    y, x = f_pay(zz), x_sh(zz)
    yc, xc = y - y.mean(axis=1, keepdims=True), x - x.mean(axis=1, keepdims=True)
    b = (yc * xc).sum(axis=1) / (xc * xc).sum(axis=1)
    est = y.mean(axis=1) - b * (x.mean(axis=1) - 100)
    fixed = y.mean(axis=1) - 0.6736 * (x.mean(axis=1) - 100)
    bias, se_b = est.mean() - BS0, est.std() / math.sqrt(reps)
    bias_f, se_f = fixed.mean() - BS0, fixed.std() / math.sqrt(reps)
    print(f'   n = {npath}: bias with b from the same paths {bias:+.4f} (SE {se_b:.4f}); with fixed b {bias_f:+.4f} (SE {se_f:.4f})')
    chk(f'n={npath}: fixed b is unbiased', abs(bias_f) < 4 * se_f)
    if npath == 10:
        chk('n=10: b from the same paths is biased (more than 5 SE)', abs(bias) > 5 * se_b)
        bias10 = bias
    else:
        chk('the bias shrinks about like 1/n', abs(bias) < abs(bias10) / 2.5 + 3 * se_b)
del zz
# l16 screens[11]: "a control with rho = 0.9995, as a European is for a barrier"
for m in (12, 252):
    yb, ye = sim_barrier(m, 400_000, 5, also_euro=True)
    rb = np.corrcoef(yb, ye)[0, 1]
    print(f'   down-and-out call (H = 90, {m} dates) against the European call payoff: rho = {rb:.4f}, factor {1 / (1 - rb * rb):.1f}')
    if m == 252:
        xfail('l16 screens[11]: a European control has rho = 0.9995 with a barrier option (the course\'s own H = 90 barrier)', rb > 0.999,
              f'rho = {rb:.3f}, a factor of {1 / (1 - rb * rb):.0f}, not 1,000')
        # corrected assert: assert 0.90 < rb < 0.99
zz = np.random.default_rng(0).standard_normal(100_000)
STp = 100 * np.exp((0.04 - 0.045) * 0.5 + 0.3 * math.sqrt(0.5) * zz)
yp, xp = math.exp(-0.02) * np.maximum(95 - STp, 0), math.exp(-0.02) * STp
near('put control slope -0.292', np.cov(yp, xp)[0, 1] / np.var(xp, ddof=1), -0.292, 5e-4)

print('--- l17 three ways, review-4, homework-4')
src17 = widgets(load('l17-three-ways'))['screens[8]']['solution']
cn_price, gl_price, mc_price = ns17['cn_price'], ns17['gl_price'], ns17['mc_price']
near('console: bs', BS0, 10.450583572185565, 1e-12)
near('console: cn', cn_price(100, 100, R, SIG, 1, 'call', 200, 400, 200), 10.449919918096366, 1e-11)
near('console: gl', gl_price(100, 100, R, SIG, 1, 'call', 32), 10.450583572185309, 2e-13)
m0 = mc_price(100, 100, R, SIG, 1, 'call', 100_000, 0)
chk('console: mc', abs(m0[0] - 10.448367800848034) < 1e-11 and abs(m0[1] - 0.017763955941256515) < 1e-13)
near('console: crr 500', crr(100, 100, R, SIG, 1, 500), 10.446585136446535, 1e-8)
near('lesson cn_price = own march', cn_price(100, 100, R, SIG, 1, 'call', 200, 400, 200), march(100, 100, R, SIG, 1, 200, 400, 200, 0.5, 2), 1e-9)
near('GL error -2.6e-13', gl_price(100, 100, R, SIG, 1, 'call', 32) - BS0, -2.6e-13, 1e-13)
for (M, N, want, tol) in [(200, 100, -2.65e-3, 5e-6), (400, 200, -6.64e-4, 5e-7), (800, 400, -1.66e-4, 5e-7), (1600, 800, -4.15e-5, 5e-8)]:
    near(f'CN error M={M} N={N}', march(100, 100, R, SIG, 1, 200, M, N, 0.5, 2) - BS0, want, tol)
for n, want in [(500, -0.0040), (1000, -0.0020), (1001, 0.0018), (2000, -0.0010)]:
    near(f'tree error at {n} steps', crr(100, 100, R, SIG, 1, n) - BS0, want, 5e-5)
near('tree 1,000 price', crr(100, 100, R, SIG, 1, 1000), 10.448584, 5e-7)
near('tree 1,001 price', crr(100, 100, R, SIG, 1, 1001), 10.452335, 5e-7)
near('average of 1,000 and 1,001 errs near -1e-4', (crr(100, 100, R, SIG, 1, 1000) + crr(100, 100, R, SIG, 1, 1001)) / 2 - BS0, -1e-4, 5e-5)
chk('tree errors are about 2/n pounds', all(abs(abs(crr(100, 100, R, SIG, 1, n) - BS0) * n - 2) < 0.25 for n in (500, 1000, 1001, 2000)))
chk('even trees below, odd above (this option)', all((crr(100, 100, R, SIG, 1, n) - BS0 < 0) == (n % 2 == 0) for n in range(200, 260)))
PBS = bs(100, 95, 0.04, 0.3, 0.5, 'put')
near('put: Black-Scholes 5.170209', PBS, 5.170209, 5e-7)
near('put: CN 5.169608', march(100, 95, 0.04, 0.3, 0.5, 200, 400, 200, 0.5, 2, kind='put'), 5.169608, 5e-7)
near('put: lesson CN = own march', cn_price(100, 95, 0.04, 0.3, 0.5, 'put', 200, 400, 200), march(100, 95, 0.04, 0.3, 0.5, 200, 400, 200, 0.5, 2, kind='put'), 1e-9)
near('put: GL', gl_price(100, 95, 0.04, 0.3, 0.5, 'put', 32), 5.170208971851, 5e-12)
mp = mc_price(100, 95, 0.04, 0.3, 0.5, 'put', 100_000, 0)
chk('put: MC 5.1672 (0.0181), -0.17 SE', abs(mp[0] - 5.1672) < 5e-5 and abs(mp[1] - 0.0181) < 5e-5 and abs((mp[0] - PBS) / mp[1] + 0.17) < 6e-3)
near('put: tree 1,000', crr_put(100, 95, 0.04, 0.3, 0.5, 1000), 5.170502, 5e-7)
for M, want in [(390, -0.00151), (400, 0.00091), (420, -0.00131)]:
    near(f'Smax=300 M={M} N=200 error', march(100, 100, R, SIG, 1, 300, M, 200, 0.5, 2) - BS0, want, 5e-6)
near('interpolation of a convex curve a third of the way between nodes adds about +0.0012', 0.5 * gam * 0.75 ** 2 * (1 / 3) * (2 / 3), 0.0012, 1e-4)
# a kink between nodes: same grid, strike moved on to and off a node, spot on a node (S0 = 99.75 is node 133)
on = march(99.75, 99.75, R, SIG, 1, 300, 400, 200, 0.5, 2) - bs(99.75, 99.75, R, SIG, 1)
off = march(99.75, 100.0, R, SIG, 1, 300, 400, 200, 0.5, 2) - bs(99.75, 100.0, R, SIG, 1)
print(f'   Smax=300, M=400, spot on a node: error with the strike on a node {on:+.5f}, a third of the way off {off:+.5f} (shift {off - on:+.5f})')
near('the off-node kink alone adds about +0.0012', off - on, 0.0012, 2e-4)
x32, w32 = np.polynomial.legendre.leggauss(32)
zq = 8 * x32
near('review: 32 nodes with the kink inside err by about 0.12', abs(math.exp(-R) * 8 * np.sum(w32 * np.maximum(100 * np.exp(0.03 + 0.2 * zq) - 100, 0) * norm.pdf(zq)) - BS0), 0.12, 0.01)
near('review: z* = -0.15', (math.log(1.0) - 0.03) / 0.2, -0.15, 1e-12)
near('homework: shifted daily barrier 89.34', 90 * math.exp(-0.5826 * 0.2 / math.sqrt(252)), 89.34, 5e-3)
near('homework: monthly slip 87.02', 90 * math.exp(-0.5826 * 0.2 / math.sqrt(12)), 87.02, 5e-3)
rep = nsh4['price_report'](100, 95, 0.04, 0.3, 0.5, 'put', 0.005)
chk('homework put: grid stops at M = 320, error -9.4e-4, estimate honest', rep['fd'][2] == 320 * 160 and abs(rep['fd'][0] - PBS + 9.4e-4) < 5e-5 and 0.5 < abs(rep['fd'][0] - PBS) / rep['fd'][1] < 2, str(rep['fd']))
chk('homework put: quadrature stops at 16 nodes', rep['quad'][2] == 16, str(rep['quad']))
chk('homework put: MC stops at 2,560,000 paths, SE 0.0036', rep['mc'][2] == 2_560_000 and abs(rep['mc'][1] - 0.0036) < 5e-5, str(rep['mc']))
near('homework: BS 120 call', bs(100, 120, R, SIG, 1), 3.2474774165608125, 1e-10)

# =============================================================== PART B (delta)
print('--- Delta: bisect (l5), safe_newton and implied_vols (l6), Gauss-Legendre pricers (l10), ytm_book (homework-2)')
ns5 = widget_check('l5-bisection-and-newton', 'screens[8]')
ns6 = widget_check('l6-safe-root-finder', 'screens[7]')
ns6v = widget_check('l6-safe-root-finder', 'screens[8]')
ns10 = widget_check('l10-gaussian-quadrature', 'screens[7]')
nsh2 = widget_check('homework-2', 'items[6]')

bis = ns5['bisect']
chk('bisect: root at either end is returned', bis(lambda x: x, 0.0, 1.0, 1e-9) == (0.0, 2) and bis(lambda x: x - 1, 0.0, 1.0, 1e-9) == (1.0, 2))
r_, c_ = bis(lambda x: x * x - 2, 1, 2, 1e-12)
chk('bisect: x^2 - 2 to 1e-12 in 42 calls', abs(r_ - math.sqrt(2)) < 1e-12 and c_ == 42, f'{c_}')
chk('l5 explain: the secant method calls f 9 times, Newton 6 times', ns5['secant'](lambda x: x * x - 2, 1.0, 2.0, 1e-12)[1] == 9 and ns5['newton'](lambda x: x * x - 2, lambda x: 2 * x, 1.0, 1e-12)[1] == 6)
for tol in (1e-17, 0.0, -1.0):
    r_, c_ = bis(lambda x: x * x - 2, 1.0, 2.0, tol)
    chk(f'bisect: tol = {tol} stops, within one float gap', abs(r_ - math.sqrt(2)) <= 2.3e-16 and c_ < 60, f'{r_!r} {c_}')
r_, c_ = bis(lambda x: x - 1e-300, -1.0, 2.0, 0.0)
chk('bisect: root near zero, tol 0, stops (walks through the subnormals)', abs(r_ - 1e-300) < 1e-310 and c_ < 2200, f'{r_!r} {c_}')
for g in (lambda x: x * x + 1, lambda x: 1e-200 * (x * x + 1), lambda x: -1e-200 * (x * x + 1)):
    try:
        bis(g, 0.0, 1.0, 1e-9); ok_ = False
    except ValueError:
        ok_ = True
    chk('bisect: no sign change raises ValueError, tiny values included', ok_)
chk('bisect: an exact zero at a midpoint is still found (rising and falling f)',
    abs(bis(lambda x: x - 1, 0.0, 2.0, 1e-12)[0] - 1) < 1e-12 and abs(bis(lambda x: 1 - x, 0.0, 2.0, 1e-12)[0] - 1) < 1e-12)
chk('bisect: error is at most tol / 2', all(abs(bis(lambda x: x ** 3 - q, 0.0, 3.0, 1e-6)[0] - q ** (1 / 3)) <= 0.5e-6 for q in (0.5, 2.0, 7.0, 20.0)))
r_, c_ = bis(lambda x: x * x - 2, 2.0, 1.0, 1e-12)
print(f'   bisect with the ends swapped, bisect(f, 2.0, 1.0, 1e-12): returns {r_} after {c_} calls')
xfail('bisect (delta): a bracket given as (hi, lo) is either solved or refused', abs(r_ - math.sqrt(2)) < 1e-9,
      f'returns the first midpoint {r_} with no error')
# corrected assert: assert abs(bisect(lambda x: x * x - 2, 2.0, 1.0, 1e-12)[0] - 2 ** 0.5) < 1e-12

sn = ns6['safe_newton']
chk('safe_newton: root at either end is returned', sn(lambda x: x, lambda x: 1.0, 0.0, 1.0) == 0.0 and sn(lambda x: x - 1, lambda x: 1.0, 0.0, 1.0) == 1.0)
for g in (lambda x: x * x + 1, lambda x: 1e-200 * (x * x + 1)):
    try:
        sn(g, lambda x: 2 * x, 0.0, 1.0); ok_ = False
    except ValueError:
        ok_ = True
    chk('safe_newton: no sign change raises ValueError', ok_)
near('safe_newton: Newton cycle x^3 - 2x + 2 forced to the root', sn(lambda x: x ** 3 - 2 * x + 2, lambda x: 3 * x * x - 2, -3.0, 0.0), -1.769292354238631, 1e-9)
xs = [0.0]
for _ in range(4):
    xs.append(xs[-1] - (xs[-1] ** 3 - 2 * xs[-1] + 2) / (3 * xs[-1] ** 2 - 2))
chk('plain Newton from 0 cycles 0, 1, 0, 1', xs == [0.0, 1.0, 0.0, 1.0, 0.0])
near('safe_newton: (x-1)^9 with default ftol stops near 1.046', sn(lambda x: (x - 1) ** 9, lambda x: 9 * (x - 1) ** 8, 0.0, 3.0), 1.046, 2e-3)
chk('every x within 0.046 of 1 has residual below 1e-12', 0.046 ** 9 < 1e-12 < 0.047 ** 9)
for xtol in (1e-10, 1e-17):
    r_ = sn(lambda x: x * x - 2, lambda x: 2 * x, 0.0, 2.0, xtol=xtol, ftol=0.0)
    chk(f'safe_newton: xtol = {xtol}, ftol = 0 stops within a float gap of the root', abs(r_ - math.sqrt(2)) <= max(xtol, 4.5e-16), f'{r_!r}')
try:
    sn(lambda x: x * x - 2, lambda x: 2 * x, 0.0, 2.0, xtol=0.0, ftol=0.0); msg = 'returned'
except RuntimeError:
    msg = 'RuntimeError'
print(f'   safe_newton with xtol = 0 and ftol = 0: {msg} (no step is below 0; documented as RuntimeError after maxit)')
chk('safe_newton: xtol = 0 and ftol = 0 ends in RuntimeError or a root, never a hang', msg in ('RuntimeError', 'returned'))
try:
    sn(lambda x: math.atan(x - 12345.678), lambda x: 1 / (1 + (x - 12345.678) ** 2), -1e10, 3e10, maxit=20); ok_ = False
except RuntimeError:
    ok_ = True
chk('safe_newton: non-convergence at the cap raises RuntimeError', ok_)
# robustness: random monotone and non-monotone functions, wide brackets
rng = np.random.default_rng(8)
worst = 0
for _ in range(3000):
    a, b_, c3 = rng.normal(size=3)
    root = rng.uniform(-5, 5)
    f = lambda x, a=a, b_=b_, c3=c3, root=root: (x - root) * (1 + a * a * (x - root) ** 2) * math.exp(0.1 * b_ * (x - root)) + 0 * c3
    h = 1e-6
    df = lambda x, f=f: (f(x + 1e-6) - f(x - 1e-6)) / 2e-6
    L, U = root - rng.uniform(0.1, 50), root + rng.uniform(0.1, 50)
    cnt = [0]
    def fc(x, f=f):
        cnt[0] += 1
        return f(x)
    r_ = sn(fc, df, L, U, ftol=0.0)
    worst = max(worst, cnt[0])
    if abs(r_ - root) > 1e-8:
        chk('safe_newton fuzz: root found', False, f'{r_} vs {root}')
        break
else:
    chk('safe_newton fuzz: 3,000 random brackets all solved to 1e-8', True)
print(f'   safe_newton fuzz: most calls of f on one problem = {worst}')
# the zero-slope sentinel `lo - 1.0` with the ends given as (hi, lo)
try:
    r_ = sn(lambda x: x ** 3 - 1, lambda x: 3 * x * x, 4.0, -4.0)
    chk('safe_newton: ends swapped and a zero slope at the start still reach the root', abs(r_ - 1) < 1e-9, f'{r_}')
except Exception as e:
    chk('safe_newton: ends swapped and a zero slope at the start still reach the root', False, repr(e))

iv, bsp = ns6v['implied_vols'], ns6v['bs_price']
K11 = list(range(75, 130, 5)); kinds11 = ['p'] * 5 + ['c'] * 6
P11 = [0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003]
v11 = iv(P11, K11, 100.0, 0.05, 1 / 12, kinds11)
ref = [brentq(lambda s, k=k, p=p, kd=kd: float(bsp(100.0, k, 0.05, 1 / 12, s, kd)) - p, 1e-4, 5, xtol=1e-14) for k, p, kd in zip(K11, P11, kinds11)]
chk('implied_vols: the eleven quotes agree with brentq to 1e-10', np.max(np.abs(v11 - ref)) < 1e-10, f'{np.max(np.abs(v11 - ref)):.2e}')
chk('implied_vols: call quoted below its bound gives NaN, alone and in a vector', np.isnan(iv([5.0], [95], 100.0, 0.05, 1 / 12, ['c'])[0]) and np.isnan(iv([2.5121, 5.0], [100, 95], 100.0, 0.05, 1 / 12, ['c', 'c'])[1]))
near('lower bound of the 95 call is 5.395', 100 - 95 * math.exp(-0.05 / 12), 5.395, 5e-4)
# which strikes take a midpoint first (explain: "the 75 and 80 puts")
s0v = np.full(11, 0.2)
f0 = bsp(100.0, K11, 0.05, 1 / 12, s0v, np.array(kinds11)) - np.array(P11)
new0 = s0v - f0 / ns6v['bs_vega'](100.0, np.array(K11, float), 0.05, 1 / 12, s0v)
first_mid = [k for k, n_ in zip(K11, new0) if not (1e-4 < n_ < 5.0)]
chk('implied_vols: only the 75 and 80 puts bisect on the first step', first_mid == [75, 80], str(first_mid))
# fuzz: wide range of strikes, vols and maturities, with a few impossible quotes mixed in
rng = np.random.default_rng(12)
worst_err, n_checked, not_conv = 0.0, 0, 0
for _ in range(300):
    n_ = 40
    T_ = float(rng.choice([1 / 252, 1 / 52, 1 / 12, 0.5, 2.0, 10.0]))
    Ks = rng.uniform(60, 160, n_)
    sg = rng.uniform(0.02, 3.0, n_)
    kd = np.where(Ks < 100, 'p', 'c')
    P = bsp(100.0, Ks, 0.03, T_, sg, kd)
    badq = rng.random(n_) < 0.1
    P = np.where(badq, -1.0, P)
    out = iv(P, Ks, 100.0, 0.03, T_, kd)
    # only quotes whose vol is recoverable in double precision: time value well above rounding
    vega = ns6v['bs_vega'](100.0, Ks, 0.03, T_, sg)
    good = ~badq & (vega > 1e-3) & (P > 1e-8)
    chk_nan = np.all(np.isnan(out[badq]))
    if not chk_nan:
        chk('implied_vols fuzz: impossible quotes give NaN', False)
    err = np.abs(out[good] - sg[good])
    worst_err = max(worst_err, float(err.max()) if err.size else 0.0)
    n_checked += int(good.sum())
    not_conv += int(np.sum(err > 1e-6))
print(f'   implied_vols fuzz: {n_checked} recoverable quotes, worst error {worst_err:.2e}, {not_conv} above 1e-6')
chk('implied_vols fuzz: every recoverable quote solved to 1e-6, with bad quotes mixed in', not_conv == 0)
# at the iteration cap the unsolved strikes come back as numbers, not NaN and not an error
capped = iv(P11, K11, 100.0, 0.05, 1 / 12, kinds11, maxit=3)
n_wrong = int(np.sum(np.abs(capped - v11) > 1e-6))
print(f'   implied_vols with maxit = 3: {n_wrong} of 11 strikes are returned unconverged, as plain numbers; worst miss {np.nanmax(np.abs(capped - v11)):.3f}')
xfail('implied_vols (delta): strikes still unsolved at the iteration cap are flagged (NaN), not returned as numbers',
      n_wrong == 0 or bool(np.all(np.isnan(capped[np.abs(capped - v11) > 1e-6]))), f'{n_wrong} unconverged vols returned silently')
# corrected assert (after the fix `return np.where(ok & ~live, s, np.nan)`):
#   assert np.all(np.isnan(capped) | (np.abs(capped - v11) < 1e-6))

glc, glp = ns10['gl_call_price'], ns10['gl_put_price']
worst_gl = 0.0
for K_ in (20, 50, 80, 100, 120, 200, 400, 1000):
    for T_, sg_ in ((1 / 52, 0.2), (1.0, 0.2), (0.5, 0.6), (5.0, 0.3)):
        e_c = abs(glc(100, K_, 0.05, sg_, T_, 64) - bs(100, K_, 0.05, sg_, T_))
        e_p = abs(glp(100, K_, 0.05, sg_, T_, 64) - bs(100, K_, 0.05, sg_, T_, 'put'))
        worst_gl = max(worst_gl, e_c, e_p)
print(f'   Gauss-Legendre pricers, 64 nodes, strikes 20 to 1,000, four (T, sigma) pairs: worst error against Black-Scholes {worst_gl:.2e}')
chk('GL pricers: deep in and out of the money strikes within 1e-8 at 64 nodes', worst_gl < 1e-8)
chk('GL pricers: kink beyond +8 gives a call of 0 and the put its forward value', glc(100, 1e6, 0.05, 0.2, 1 / 52, 32) == 0.0 and abs(glp(100, 1e6, 0.05, 0.2, 1 / 52, 32) - (1e6 * math.exp(-0.05 / 52) - 100)) < 1e-4)
chk('GL pricers: kink below -8 gives a put of 0', glp(100, 50, 0.05, 0.2, 1 / 52, 32) == 0.0)
near('GL: one-week call at 50, kink at z* about -25', (math.log(0.5) - (0.05 - 0.02) / 52) / (0.2 * math.sqrt(1 / 52)), -25, 0.1)
near('GL: far call z* = 3.32, a short smooth piece', (math.log(2) - 0.03) / 0.2, 3.32, 5e-3)
chk('GL: 16 nodes reach 1e-8 at the money; parity holds', abs(glc(100, 100, R, SIG, 1, 16) - BS0) < 1e-8 and abs(glc(100, 100, R, SIG, 1, 16) - glp(100, 100, R, SIG, 1, 16) - (100 - 100 * math.exp(-R))) < 1e-8)
near('GL: cut at z = 8 loses about S0 e^(rT) N(-(8 - s)) = 3e-13', 100 * math.exp(R) * norm.cdf(-(8 - 0.2)) * math.exp(-R), 3.1e-13, 1e-13)

yb = nsh2['ytm_book']
def price_of(y, c, n):
    return sum(100 * c / (1 + y) ** k for k in range(1, n + 1)) + 100 / (1 + y) ** n
chk('ytm_book: the 95 bond, a zero and a par bond', abs(yb([95.0], [0.05], [5])[0] - 0.0619322827) < 1e-10 and abs(yb([60.0], [0.0], [10])[0] - ((100 / 60) ** 0.1 - 1)) < 1e-10 and abs(yb([100.0], [0.04], [7])[0] - 0.04) < 1e-10)
chk('ytm_book: price above the cash flows gives NaN; price equal to them gives yield 0', np.isnan(yb([130.0], [0.05], [5])[0]) and abs(yb([125.0], [0.05], [5])[0]) < 1e-10)
chk('ytm_book: price below the value at 100% gives NaN; equal gives 1', np.isnan(yb([price_of(1.0, 0.05, 5) - 0.01], [0.05], [5])[0]) and abs(yb([price_of(1.0, 0.05, 5)], [0.05], [5])[0] - 1) < 1e-9)
rng = np.random.default_rng(21)
n_ = 5000
nn, cc, yy_ = rng.integers(1, 51, n_), rng.uniform(0, 0.15, n_), rng.uniform(0, 0.95, n_)
pp = np.array([price_of(y, c, int(n)) for y, c, n in zip(yy_, cc, nn)])
bad_ = rng.random(n_) < 0.1
pp2 = np.where(bad_, 100 * cc * nn + 100 + 1.0, pp)
out = yb(pp2, cc, nn)
chk('ytm_book fuzz: 5,000 bonds, yields 0 to 95%, bad prices mixed in', np.all(np.isnan(out[bad_])) and np.max(np.abs(out[~bad_] - yy_[~bad_])) < 1e-9, f'{np.nanmax(np.abs(out[~bad_] - yy_[~bad_])):.2e}')
capped = yb(pp[:200], cc[:200], nn[:200], maxit=2)
n_wrong = int(np.sum(np.abs(capped - yy_[:200]) > 1e-6))
print(f'   ytm_book with maxit = 2: {n_wrong} of 200 bonds are returned unconverged, as plain numbers')
xfail('ytm_book (delta): bonds still unsolved at the iteration cap are flagged (NaN), not returned as numbers',
      n_wrong == 0 or bool(np.all(np.isnan(capped[np.abs(capped - yy_[:200]) > 1e-6]))), f'{n_wrong} unconverged yields returned silently')
# corrected assert (after the fix `return np.where(ok & ~live, y, np.nan)`):
#   assert np.all(np.isnan(capped) | (np.abs(capped - yy_[:200]) < 1e-6))

print(f'--- {NPASS[0]} checks passed, {len(XFAILS)} EXPECTED_FAIL, {len(FAILS)} failed, {time.time() - t0:.0f} s')
for x in XFAILS:
    print('EXPECTED_FAIL:', x)
for x in FAILS:
    print('FAILED:', x)
sys.exit(1 if FAILS else 0)
