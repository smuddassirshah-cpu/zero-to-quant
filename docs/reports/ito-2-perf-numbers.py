"""Recompute every number and symbolic step of the ito level 2 performance task (h-derive-ito).

Run from anywhere: python3 docs/reports/ito-2-perf-numbers.py   (exits 0 when every check passes)
Each step is done twice: symbolically (sympy, two independent routes) and numerically (numpy, seeded).
If sympy is missing the symbolic half is reported as skipped and the numeric half still has to pass.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito', 'homework-2.json')
fails = []

def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))
    if not ok:
        fails.append(name)

# ---------------------------------------------------------------- 0. the item itself
hw = json.load(open(HW))
items = hw['items']
perf = [it for it in items if it.get('performance')]
check('homework-2 has 6 to 12 items', 6 <= len(items) <= 12, f'{len(items)} items')
check('exactly one performance task', len(perf) == 1)
it = perf[0]
check('task is h-derive-ito, a derivation longform at difficulty 5',
      it['id'] == 'h-derive-ito' and it['performance'] == 'derivation' and it['kind'] == 'longform' and it['difficulty'] == 5)
check('no starter, steps, order, derive, hints or parts',
      not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')))
pts = [r['points'] for r in it['rubric']]
check('rubric has 3 or more criteria summing to 10', len(pts) >= 3 and sum(pts) == 10, f'{len(pts)} criteria, {sum(pts)} points')
check('homework still has a 5, a longform and an order item',
      any(i.get('difficulty') == 5 for i in items)
      and sum(1 for i in items if i.get('kind') == 'longform') >= 1
      and any(p.get('widget', {}).get('kind') == 'order' for i in items for p in i.get('parts', [])))

# ---------------------------------------------------------------- 1. symbolic route A: the multiplication table
try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False
    print('skip symbolic checks: sympy not installed (pip install sympy)')

if HAVE_SYMPY:
    dt, dW, a, b = sp.symbols('dt dW a b')
    ft, fx, fxx, ftx, ftt = sp.symbols('f_t f_x f_xx f_tx f_tt')
    dX = a * dt + b * dW

    def table(expr):
        """Apply (dt)^2 = 0, dt dW = 0, (dW)^2 = dt: keep terms of order at most dt (dW counts 1/2)."""
        P = sp.Poly(sp.expand(expr), dt, dW)
        out = 0
        for (i, j), c in P.terms():
            order = sp.Rational(i) + sp.Rational(j, 2)
            if order > 1:
                continue                       # dt^2, dt dW, dW^3, ... all vanish
            if (i, j) == (0, 2):
                out += c * dt                   # (dW)^2 = dt
            else:
                out += c * dt**i * dW**j
        return sp.expand(out)

    target = sp.expand((ft + a * fx + sp.Rational(1, 2) * b**2 * fxx) * dt + b * fx * dW)
    full = ft * dt + fx * dX + sp.Rational(1, 2) * fxx * dX**2 + ftx * dt * dX + sp.Rational(1, 2) * ftt * dt**2
    check('step 1-5: full second-order expansion collects to the lemma', sp.simplify(table(full) - target) == 0)
    c12 = ft * dt + fx * dX + sp.Rational(1, 2) * fxx * dX**2      # first order in t, second in x (C^{1,2})
    check('C^{1,2} expansion (no f_tx, f_tt) collects to the same lemma', sp.simplify(table(c12) - target) == 0)
    check('step 2: f_x dX = a f_x dt + b f_x dW', sp.expand(fx * dX) == sp.expand(a * fx * dt + b * fx * dW))
    check('step 3: (dX)^2 = a^2 dt^2 + 2ab dt dW + b^2 dW^2',
          sp.expand(dX**2) == sp.expand(a**2 * dt**2 + 2 * a * b * dt * dW + b**2 * dW**2))
    check('step 3: (dX)^2 -> b^2 dt under the table', table(dX**2) == sp.expand(b**2 * dt))
    check('step 4: dt dX -> 0 and (dt)^2 -> 0', table(dt * dX) == 0 and table(dt**2) == 0)

    # ------------------------------------------------------------ symbolic route B: Taylor in a small parameter
    # dt = eps^2 and dW = eps z, with z^2 -> 1 in the sum (the same table, reached by real Taylor series).
    eps, z, t, x = sp.symbols('epsilon z t x')
    for name, f in [('t*x^2 + sin x', t * x**2 + sp.sin(x)), ('exp(x - t/2)', sp.exp(x - t / 2)),
                    ('x^3', x**3), ('log x', sp.log(x))]:
        shifted = f.subs({t: t + eps**2, x: x + a * eps**2 + b * eps * z}, simultaneous=True)
        ser = sp.series(shifted, eps, 0, 3).removeO()
        c1 = sp.expand(ser.coeff(eps, 1))
        c2 = sp.expand(ser.coeff(eps, 2)).subs(z**2, 1)
        drift = sp.diff(f, t) + a * sp.diff(f, x) + sp.Rational(1, 2) * b**2 * sp.diff(f, x, 2)
        ok = sp.simplify(c1 - b * sp.diff(f, x) * z) == 0 and sp.simplify(c2 - drift) == 0
        check(f'route B Taylor series agrees with the lemma for f = {name}', ok)

    # ------------------------------------------------------------ the check function
    f = sp.exp(x - t / 2)
    check('check: f_t = -f/2', sp.simplify(sp.diff(f, t) + f / 2) == 0)
    check('check: f_x = f_xx = f', sp.simplify(sp.diff(f, x) - f) == 0 and sp.simplify(sp.diff(f, x, 2) - f) == 0)
    drift = sp.diff(f, t) + 0 * sp.diff(f, x) + sp.Rational(1, 2) * 1**2 * sp.diff(f, x, 2)
    check('check: dt term -f/2 + 0 + f/2 = 0 (a = 0, b = 1)', sp.simplify(drift) == 0)
    check('check: dW term b f_x = f', sp.simplify(1 * sp.diff(f, x) - f) == 0)
    s, w = sp.symbols('s w', positive=True)
    wv = sp.symbols('wv', real=True)
    dens = sp.exp(-wv**2 / (2 * s)) / sp.sqrt(2 * sp.pi * s)
    m1 = sp.simplify(sp.integrate(sp.exp(wv - s / 2) * dens, (wv, -sp.oo, sp.oo)))
    check('E[exp(W_t - t/2)] = 1', sp.simplify(m1 - 1) == 0, str(m1))
    m2 = sp.simplify(sp.integrate(sp.exp(2 * wv - s) * dens, (wv, -sp.oo, sp.oo)))
    check('E[exp(2 W_s - s)] = e^s', sp.simplify(m2 - sp.exp(s)) == 0, str(m2))
    T = sp.symbols('T', positive=True)
    check('int_0^t e^s ds = e^t - 1', sp.simplify(sp.integrate(sp.exp(s), (s, 0, T)) - (sp.exp(T) - 1)) == 0)
    mfun = sp.Function('m')
    sol = sp.dsolve(sp.Eq(mfun(T).diff(T), -mfun(T) / 2), mfun(T), ics={mfun(0): 1})
    check('wrong chain rule: m\' = -m/2, m(0) = 1 gives e^{-t/2}', sp.simplify(sol.rhs - sp.exp(-T / 2)) == 0, str(sol.rhs))
    check('ordinary chain rule drift is f_t = -f/2 (no curvature term)', sp.simplify(sp.diff(f, t) + f / 2) == 0)

# ---------------------------------------------------------------- 2. numeric: the table on a seeded grid
rng = np.random.default_rng(3)
n = 2**16
h = 1.0 / n
dWn = rng.standard_normal(n) * math.sqrt(h)
qv = float(np.sum(dWn**2))
cross = float(np.sum(h * dWn))
dt2 = n * h * h
check('sum (dW)^2 near t = 1 (SE sqrt(2/n) = 0.0055)', abs(qv - 1) < 4 * math.sqrt(2 / n), f'{qv:.6f}')
check('sum dt dW near 0', abs(cross) < 1e-3, f'{cross:.2e}')
check('sum (dt)^2 = 1/n near 0', abs(dt2 - 1 / n) < 1e-15 and dt2 < 1e-4, f'{dt2:.2e}')

# ---------------------------------------------------------------- 3. numeric: lemma in integral form, pathwise
def lemma_gap(n, seed):
    """Itô process with adapted a, b; f(t, x) = t x^2 + sin x. Returns (Itô gap, ordinary-chain gap)."""
    r = np.random.default_rng(seed)
    h = 1.0 / n
    d = r.standard_normal(n) * math.sqrt(h)
    X = np.empty(n + 1); X[0] = 0.5
    W = np.concatenate([[0.0], np.cumsum(d)])
    tk = np.arange(n) * h
    A = np.empty(n); B = np.empty(n)
    for k in range(n):                       # a, b read only the past: adapted
        A[k] = math.cos(W[k])
        B[k] = 0.5 + 0.3 * math.sin(X[k])
        X[k + 1] = X[k] + A[k] * h + B[k] * d[k]
    Xk = X[:-1]
    f = lambda t, x: t * x**2 + np.sin(x)
    f_t = Xk**2
    f_x = 2 * tk * Xk + np.cos(Xk)
    f_xx = 2 * tk - np.sin(Xk)
    lhs = f(1.0, X[-1]) - f(0.0, X[0])
    ito = np.sum((f_t + A * f_x + 0.5 * B**2 * f_xx) * h) + np.sum(B * f_x * d)
    ordinary = np.sum((f_t + A * f_x) * h) + np.sum(B * f_x * d)
    return abs(lhs - ito), abs(lhs - ordinary), float(np.sum(0.5 * B**2 * f_xx * h))

g1 = lemma_gap(2**10, 5); g2 = lemma_gap(2**14, 5)
check('pathwise lemma gap is small at n = 2^14', g2[0] < 0.01, f'{g2[0]:.5f}')
check('pathwise lemma gap shrinks from 2^10 to 2^14', g2[0] < g1[0], f'{g1[0]:.5f} -> {g2[0]:.5f}')
check('ordinary chain rule misses about the curvature integral', abs(g2[1] - abs(g2[2])) < 0.02 and g2[1] > 10 * g2[0],
      f'ordinary gap {g2[1]:.4f}, curvature term {g2[2]:.4f}')

# exp(W - t/2): f(1, W_1) - f(0, 0) equals the left-point sum of f dW
def exp_gap(n, seed):
    r = np.random.default_rng(seed)
    h = 1.0 / n
    d = r.standard_normal(n) * math.sqrt(h)
    W = np.concatenate([[0.0], np.cumsum(d)])
    tk = np.arange(n + 1) * h
    F = np.exp(W - tk / 2)
    return abs((F[-1] - F[0]) - np.sum(F[:-1] * d))
e1, e2 = exp_gap(2**10, 9), exp_gap(2**16, 9)
check('exp(W - t/2) = 1 + left sum of f dW (gap < 0.01 at 2^16)', e2 < 0.01, f'{e1:.5f} -> {e2:.5f}')

# ---------------------------------------------------------------- 4. numeric: partials by finite differences
fe = lambda t, x: math.exp(x - t / 2)
for (t0, x0) in [(0.0, 0.0), (0.7, -0.4), (2.0, 1.3)]:
    eh = 1e-4
    ftn = (fe(t0 + eh, x0) - fe(t0 - eh, x0)) / (2 * eh)
    fxn = (fe(t0, x0 + eh) - fe(t0, x0 - eh)) / (2 * eh)
    fxxn = (fe(t0, x0 + eh) - 2 * fe(t0, x0) + fe(t0, x0 - eh)) / eh**2
    v = fe(t0, x0)
    ok = abs(ftn + v / 2) < 1e-6 * max(1, v) and abs(fxn - v) < 1e-6 * max(1, v) and abs(fxxn - v) < 1e-4 * max(1, v)
    check(f'finite differences at (t, x) = ({t0}, {x0}): f_t = -f/2, f_x = f_xx = f; drift {ftn + 0.5 * fxxn:.2e}', ok)

# ---------------------------------------------------------------- 5. numeric: Monte Carlo moments
r = np.random.default_rng(11)
N = 10**6
W1 = r.standard_normal(N)
y = np.exp(W1 - 0.5)
mean, se = float(y.mean()), float(y.std(ddof=1) / math.sqrt(N))
check('E[exp(W_1 - 1/2)] = 1 by simulation (within 4 SE)', abs(mean - 1) < 4 * se, f'{mean:.5f} (SE {se:.5f})')
check('wrong-rule mean e^{-1/2} = 0.60653 is far outside', abs(mean - math.exp(-0.5)) > 50 * se, f'{math.exp(-0.5):.5f}')
for s0 in (0.25, 0.5, 1.0):
    z = np.exp(2 * math.sqrt(s0) * r.standard_normal(N) - s0)
    m, e_ = float(z.mean()), float(z.std(ddof=1) / math.sqrt(N))
    check(f'E[exp(2 W_s - s)] = e^s at s = {s0} (within 4 SE)', abs(m - math.exp(s0)) < 4 * e_, f'{m:.4f} vs {math.exp(s0):.4f} (SE {e_:.4f})')
grid = np.linspace(0, 1, 100001)
trap = float(np.sum((np.exp(grid[1:]) + np.exp(grid[:-1])) / 2 * np.diff(grid)))
check('int_0^1 e^s ds = e - 1 = 1.71828 by quadrature', abs(trap - (math.e - 1)) < 1e-8, f'{trap:.6f}')

# ---------------------------------------------------------------- 6. the justification of model steps 3 and 4 (review P1)
# 6a. symbolic: dW ~ N(0, h), so E[dW^2] = h and Var(dW^2) = E[dW^4] - h^2 = 3h^2 - h^2 = 2h^2; n of them add to mean t, variance 2 t h.
if HAVE_SYMPY:
    hs, ns_, ts = sp.symbols('h n t', positive=True)
    zv = sp.symbols('zv', real=True)
    dens1 = sp.exp(-zv**2 / 2) / sp.sqrt(2 * sp.pi)
    m2 = sp.integrate(zv**2 * dens1, (zv, -sp.oo, sp.oo))
    m4 = sp.integrate(zv**4 * dens1, (zv, -sp.oo, sp.oo))
    check('E[Z^2] = 1 and E[Z^4] = 3', m2 == 1 and m4 == 3)
    var_one = sp.simplify((m4 - m2**2) * hs**2)                     # Var((dW)^2) for dW = sqrt(h) Z
    check('Var((dW)^2) = 2 h^2', sp.simplify(var_one - 2 * hs**2) == 0)
    check('n = t/h terms: mean t and variance 2 t h', sp.simplify(ns_.subs(ns_, ts / hs) * hs - ts) == 0
          and sp.simplify((ts / hs) * var_one - 2 * ts * hs) == 0)
# 6b. numeric: many seeded paths on a grid with h = 1/256, t = 1
rr = np.random.default_rng(21)
n6, P6 = 256, 20000
h6 = 1.0 / n6
dW6 = rr.standard_normal((P6, n6)) * math.sqrt(h6)
W6 = np.concatenate([np.zeros((P6, 1)), np.cumsum(dW6, axis=1)], axis=1)
qv6 = np.sum(dW6**2, axis=1)
se_mean = math.sqrt(2 * h6 / P6)
check('sum (dW)^2: mean 1 within 4 SE', abs(qv6.mean() - 1) < 4 * se_mean, f'{qv6.mean():.5f}')
check('sum (dW)^2: variance 2 t h within 5%', abs(qv6.var(ddof=1) / (2 * h6) - 1) < 0.05, f'{qv6.var(ddof=1):.5f} vs {2 * h6:.5f}')
g6 = np.cos(W6[:, :-1])                                          # bounded (|g| <= 1) and adapted
wsum = np.sum(g6 * (dW6**2 - h6), axis=1)
check('weighted sum g((dW)^2 - h): mean 0 within 4 SE', abs(wsum.mean()) < 4 * wsum.std(ddof=1) / math.sqrt(P6), f'{wsum.mean():.2e}')
check('weighted sum variance is at most 2 sup g^2 t h', wsum.var(ddof=1) <= 2 * 1.0 * 1.0 * h6 * 1.05, f'{wsum.var(ddof=1):.5f} <= {2 * h6:.5f}')
direct = np.sum(g6 * dW6**2, axis=1)
riem = np.sum(g6 * h6, axis=1)
check('sum g (dW)^2 is close to the Riemann sum of g ds', float(np.sqrt(np.mean((direct - riem)**2))) < 3 * math.sqrt(2 * h6), f'rms {float(np.sqrt(np.mean((direct - riem)**2))):.4f}')
# 6c. step 4 bounds: |sum dt dW| <= t max|dW|, and sum (dt)^2 = t h
cross6 = np.abs(np.sum(h6 * dW6, axis=1))
bound6 = 1.0 * np.max(np.abs(dW6), axis=1)
check('|sum dt dW| <= t max|dW| on every path', bool(np.all(cross6 <= bound6 + 1e-15)))
check('sum (dt)^2 = t h exactly', abs(n6 * h6**2 - 1.0 * h6) < 1e-15)
# 6d. the rubric flags: rows 3 and 4 required, others not, and a row 3 that names the reason
req = [bool(r.get('required')) for r in it['rubric']]
check('rubric rows 3 and 4 are required, rows 1, 2 and 5 are not', req == [False, False, True, True, False], str(req))
check('row 3 names mean t and variance 2t dt', 'mean $t$' in it['rubric'][2]['text'] and 'variance $2t\\Delta t' in it['rubric'][2]['text'])
check('model step 3 states the weighted sum and the variance bound', 'variance at most $2\\sup g^2' in it['model'] and 'f_{xx}b^2' in it['model'])

print()
if fails:
    print(f'{len(fails)} check(s) failed: ' + '; '.join(fails))
    sys.exit(1)
print('all checks passed' + ('' if HAVE_SYMPY else ' (numeric only; sympy missing)'))
