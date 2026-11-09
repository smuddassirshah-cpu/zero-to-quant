"""Recompute every number and symbolic step of the pdes level 1 performance task (h-derive-lazy-walk).

Run: python3 docs/reports/pdes-1-perf-numbers.py   (exits 0 when every check passes)
The symbolic half needs sympy (skipped with a note if it is missing); every other check uses
the standard library and numpy only. Each number is computed by two independent routes:
a closed formula, and either exact iteration of the walk's distribution, a seeded simulation,
or the walk's Fourier multiplier.
"""
import cmath, json, math, os, sys
from fractions import Fraction as F
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'pdes', 'homework-1.json')
fails = []

def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (': ' + detail if detail else ''))
    if not ok:
        fails.append(name)

def close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))

# ------------------------------------------------------------ 0. the item and the homework
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
perf = [it for it in items if it.get('performance')]
check('homework-1 has 6 to 12 items', 6 <= len(items) <= 12, f'{len(items)} items')
check('exactly one performance task', len(perf) == 1)
it = perf[0]
check('task is h-derive-lazy-walk, a derivation longform at difficulty 5, skill pe-heat',
      it['id'] == 'h-derive-lazy-walk' and it['performance'] == 'derivation' and it['kind'] == 'longform'
      and it['difficulty'] == 5 and it['skills'] == ['pe-heat'])
check('it is the last item', items[-1]['id'] == 'h-derive-lazy-walk')
check('no starter, steps, order, derive, hints, parts or tags',
      not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts', 'tags')))
pts = [r['points'] for r in it['rubric']]
req = [i for i, r in enumerate(it['rubric']) if r.get('required')]
check('rubric has 3 to 5 rows summing to 10', 3 <= len(pts) <= 5 and sum(pts) == 10, f'{pts}')
# 702 sweep: rows 3 (scaling) and 4 (the numbers) are now required; row 1 is optional in the prompt
check('required rows 2, 3 and 4, not every row', req == [1, 2, 3])
# a pass is 7 of 10 with the required row ticked; leaving out the scaling row must fail
check('dropping the scaling-and-bounds row fails the pass', sum(pts) - pts[2] < 7, f'{sum(pts) - pts[2]}')
check('dropping row 1 or row 4 alone still passes', sum(pts) - pts[0] >= 7 and sum(pts) - pts[3] >= 7)
check('homework keeps a difficulty 5, a longform and an order item',
      any(i.get('difficulty') == 5 for i in items if i is not it)
      and any(i.get('kind') == 'longform' for i in items)
      and any(i.get('widget', {}).get('kind') == 'order' for i in items))
check('title has no $', '$' not in it['title'])
alltext = it['prompt'] + it['model'] + ''.join(r['text'] for r in it['rubric'])
check('no exclamation mark, em-dash or en-dash', not any(ch in alltext for ch in '!—–'))
check('no lesson cited by number', 'lesson ' not in alltext.lower())

# ------------------------------------------------------------ 1. the stated numbers, route A: closed formulas
dx, dt, p, q, t = F(1, 10), F(4, 1000), F(45, 100), F(35, 100), F(1)
r = 1 - p - q
D = (p + q) * dx**2 / (2 * dt)
c = (p - q) * dx / dt
n = t / dt
m1 = (p - q) * dx                 # mean of one step
m2 = (p + q) * dx**2              # mean square of one step
v1 = m2 - m1**2                   # variance of one step
mean, var = n * m1, n * v1
gap = 2 * D * t - var
check('r = 0.2', r == F(1, 5))
check('D = 0.8 x 0.01 / 0.008 = 1', D == 1 and F(8, 10) * F(1, 100) / F(8, 1000) == 1)
check('D = (1 - r) dx^2 / (2 dt) agrees', (1 - r) * dx**2 / (2 * dt) == D)
check('c = 0.1 x 0.1 / 0.004 = 2.5', c == F(5, 2) and F(1, 10) * F(1, 10) / F(4, 1000) == F(5, 2))
check('n = t / dt = 250', n == 250)
check('step mean 0.01, mean square 0.008, square of mean 0.0001, variance 0.0079',
      m1 == F(1, 100) and m2 == F(8, 1000) and m1**2 == F(1, 10000) and v1 == F(79, 10000))
check('walk mean 2.5 = ct', mean == F(5, 2) and mean == c * t)
check('walk variance 1.975, equation 2Dt = 2', var == F(1975, 1000) and 2 * D * t == 2)
check('gap 0.025 = n (p-q)^2 dx^2 = c^2 dt t', gap == F(1, 40) and gap == n * (p - q)**2 * dx**2 and gap == c**2 * dt * t)
check('scaling: dt = (1 - r) dx^2 / (2D) and p - q = c(1 - r) dx / (2D) give the stated walk',
      (1 - r) * dx**2 / (2 * D) == dt and c * (1 - r) * dx / (2 * D) == p - q == F(1, 10))
check('remainder identity (p + q) dx^3 / (6 dt) = D dx / 3', (p + q) * dx**3 / (6 * dt) == D * dx / 3)
check('fair walk r = 0, p = q = 1/2: c = 0 and D = dx^2/(2 dt)',
      (F(1, 2) - F(1, 2)) * dx / dt == 0 and (F(1, 2) + F(1, 2)) * dx**2 / (2 * dt) == dx**2 / (2 * dt))

# ------------------------------------------------------------ 2. the stated numbers, route B: exact iteration of the walk
def walk_dist(p, q, n):
    """Exact distribution after n steps on sites -n..n (float64)."""
    P = np.zeros(2 * n + 1); P[n] = 1.0
    r = 1.0 - p - q
    for _ in range(n):
        Q = r * P
        Q[1:] += p * P[:-1]      # stepped right from the left neighbour
        Q[:-1] += q * P[1:]      # stepped left from the right neighbour
        P = Q
    return P

P = walk_dist(0.45, 0.35, 250)
xs = 0.1 * np.arange(-250, 251)
mu = float((P * xs).sum()); va = float((P * (xs - mu)**2).sum())
check('iterated walk: total probability 1', close(float(P.sum()), 1.0, 1e-12))
check('iterated walk: mean 2.5', close(mu, 2.5, 1e-10), f'{mu:.12f}')
check('iterated walk: variance 1.975', close(va, 1.975, 1e-10), f'{va:.12f}')
# swapping the pairing (p with the right neighbour) flips the drift: mean -2.5
Pw = walk_dist(0.35, 0.45, 250)
check('wrong pairing gives mean -2.5, which the check rejects', close(float((Pw * xs).sum()), -2.5, 1e-10))

# seeded simulation: 200,000 walkers, 250 steps
rng = np.random.default_rng(20261107)
steps = rng.choice(np.array([0.1, -0.1, 0.0]), p=[0.45, 0.35, 0.2], size=(200_000, 250))
X = steps.sum(axis=1)
se_m = math.sqrt(1.975 / X.size); se_v = 1.975 * math.sqrt(2 / (X.size - 1))
check('simulation: mean within 4 standard errors of 2.5', abs(X.mean() - 2.5) < 4 * se_m, f'{X.mean():.4f} (se {se_m:.4f})')
check('simulation: variance within 4 standard errors of 1.975', abs(X.var(ddof=1) - 1.975) < 4 * se_v, f'{X.var(ddof=1):.4f} (se {se_v:.4f})')

# ------------------------------------------------------------ 3. symbolic expansion (sympy), route A: Taylor series of a generic u
try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False
    print('skip symbolic half: sympy not installed (run with a venv that has it)')

if HAVE_SYMPY:
    x, tt, h, k, ps, qs, Ds, cs, tau = sp.symbols('x t h k p q D c tau', real=True)
    u = sp.Function('u')
    rs = 1 - ps - qs
    rhs = ps * u(x - h) + qs * u(x + h) + rs * u(x)
    ser = sp.series(rhs, h, 0, 9).removeO().doit()
    ser = sp.expand(ser)
    coeff = {j: sp.simplify(ser.coeff(h, j)) for j in range(9)}
    check('zeroth order: (p + q + r) u = u', sp.simplify(coeff[0] - u(x)) == 0)
    check('first order: -(p - q) h u_x', sp.simplify(coeff[1] + (ps - qs) * sp.diff(u(x), x)) == 0)
    check('second order: (p + q) h^2 u_xx / 2', sp.simplify(coeff[2] - (ps + qs) / 2 * sp.diff(u(x), x, 2)) == 0)
    # time side: u(t + dt) = u + dt u_t + dt^2 u_tt / 2 + ...
    w = sp.Function('w')
    tser = sp.expand(sp.series(w(tt + tau), tau, 0, 3).removeO().doit())
    check('time side: u + dt u_t + dt^2 u_tt / 2', sp.simplify(tser - (w(tt) + tau * sp.diff(w(tt), tt) + tau**2 / 2 * sp.diff(w(tt), tt, 2))) == 0)
    # the scaling: solve D and c for dt and p - q
    dts, a = sp.symbols('dt a', positive=True)   # a = p + q = 1 - r
    sol = sp.solve([sp.Eq(Ds, a * h**2 / (2 * dts)), sp.Eq(cs, (ps - qs) * h / dts)], [dts, ps], dict=True)[0]
    check('scaling: dt = (1 - r) h^2 / (2D)', sp.simplify(sol[dts] - a * h**2 / (2 * Ds)) == 0)
    check('scaling: p - q = c (1 - r) h / (2D)', sp.simplify(sol[ps] - qs - cs * a * h / (2 * Ds)) == 0)
    # each order j over dt, under the scaling, is c h^(j-1)/j! (odd) or 2D h^(j-2)/j! (even), times the derivative
    sub = {ps: qs + cs * a * h / (2 * Ds)}
    dtv = a * h**2 / (2 * Ds)
    good = True
    for j in range(1, 9):
        raw = sp.simplify((ser.coeff(h, j) * h**j / dtv).subs(sub).subs(qs, (a - cs * a * h / (2 * Ds)) / 2))
        der = sp.diff(u(x), x, j)
        want = (-1)**j * (cs * h**(j - 1) if j % 2 else 2 * Ds * h**(j - 2)) / sp.factorial(j) * der
        if sp.simplify(raw - want) != 0:
            good = False; print('   order', j, raw, want)
    check('order j over dt is c h^(j-1)/j! (odd j) or 2D h^(j-2)/j! (even j)', good)
    lim1 = sp.limit(sp.simplify(ser.coeff(h, 1) * h / dtv).subs(sub).subs(qs, (a - cs * a * h / (2 * Ds)) / 2) / sp.diff(u(x), x), h, 0)
    lim2 = sp.limit(sp.simplify(ser.coeff(h, 2) * h**2 / dtv).subs(sub).subs(qs, (a - cs * a * h / (2 * Ds)) / 2) / sp.diff(u(x), x, 2), h, 0)
    check('limits of the kept terms: -c u_x and D u_xx', sp.simplify(lim1 + cs) == 0 and sp.simplify(lim2 - Ds) == 0)
    check('orders 3 to 8 over dt tend to 0', all(sp.limit(((cs * h**(j - 1)) if j % 2 else 2 * Ds * h**(j - 2)) / sp.factorial(j), h, 0) == 0 for j in range(3, 9)))
    check('time remainder over dt: dt u_tt / 2 tends to 0', sp.limit(dtv / 2, h, 0) == 0)
    check('space remainder bound: (p + q) h^3 / (6 dt) = D h / 3', sp.simplify(a * h**3 / (6 * dtv) - Ds * h / 3) == 0)
    # the shifted kernel solves u_t + c u_x = D u_xx, with mean ct and variance 2Dt
    T = sp.symbols('T', positive=True); Dp = sp.symbols('Dp', positive=True)
    v = sp.exp(-(x - cs * T)**2 / (4 * Dp * T)) / sp.sqrt(4 * sp.pi * Dp * T)
    check('shifted kernel solves u_t + c u_x = D u_xx', sp.simplify(sp.diff(v, T) + cs * sp.diff(v, x) - Dp * sp.diff(v, x, 2)) == 0)
    M1 = sp.simplify(sp.integrate(x * v, (x, -sp.oo, sp.oo)))
    M2 = sp.simplify(sp.integrate((x - cs * T)**2 * v, (x, -sp.oo, sp.oo)))
    check('shifted kernel: mean ct, variance 2Dt', sp.simplify(M1 - cs * T) == 0 and sp.simplify(M2 - 2 * Dp * T) == 0)
    # the variance gap, symbolically: n (p - q)^2 h^2 = c^2 dt t
    nn = sp.symbols('n', positive=True)
    check('gap n (p - q)^2 h^2 = c^2 dt t with t = n dt', sp.simplify((nn * (cs * dts / h)**2 * h**2) - cs**2 * dts * (nn * dts)) == 0)

# ------------------------------------------------------------ 4. route B for the expansion: exact rationals on polynomials (no sympy)
def taylor_rhs_poly(coeffs, x0, h, p, q):
    """p u(x0 - h) + q u(x0 + h) + r u(x0) for u = sum c_k x^k, exactly."""
    uval = lambda y: sum(ck * y**kk for kk, ck in enumerate(coeffs))
    return p * uval(x0 - h) + q * uval(x0 + h) + (1 - p - q) * uval(x0)

def taylor_pred_poly(coeffs, x0, h, p, q):
    """u - (p - q) h u' + (p + q) h^2 u''/2 - (p - q) h^3 u'''/6 + ... exactly (finite for a polynomial)."""
    deg = len(coeffs) - 1
    def deriv(j):
        return sum(ck * math.perm(kk, j) * x0**(kk - j) for kk, ck in enumerate(coeffs) if kk >= j)
    total = F(0)
    for j in range(deg + 1):
        w = (p + q) if j % 2 == 0 and j > 0 else (-(p - q) if j % 2 else 1)
        total += w * h**j * deriv(j) / math.factorial(j)
    return total

ok = True
for coeffs in ([F(1)], [F(0), F(1)], [F(2), F(-3), F(5)], [F(1), F(0), F(0), F(7)], [F(k + 1, k + 2) for k in range(7)]):
    for x0 in (F(3, 7), F(-2, 5)):
        if taylor_rhs_poly(coeffs, x0, F(1, 10), F(9, 20), F(7, 20)) != taylor_pred_poly(coeffs, x0, F(1, 10), F(9, 20), F(7, 20)):
            ok = False
check('exact rationals: the weighted expansion matches on five polynomials', ok)

# ------------------------------------------------------------ 5. route B for the limit: the walk's Fourier multiplier
# for u = e^{i xi x}, one tick multiplies by m = p e^{-i xi h} + q e^{i xi h} + r; per unit time log(m)/dt
# must tend to the equation's symbol -i c xi - D xi^2, with an error that shrinks like h
Dv, cv, rv, xi = 1.0, 2.5, 0.2, 1.3
errs = []
for j in range(6):
    h = 0.1 / 2**j
    dtv = (1 - rv) * h * h / (2 * Dv)
    d = cv * dtv / h
    pv, qv = (1 - rv + d) / 2, (1 - rv - d) / 2
    mval = pv * cmath.exp(-1j * xi * h) + qv * cmath.exp(1j * xi * h) + rv
    errs.append(abs(cmath.log(mval) / dtv - (-1j * cv * xi - Dv * xi * xi)))
ratios = [errs[i] / errs[i + 1] for i in range(len(errs) - 1)]
check('Fourier multiplier tends to the symbol -i c xi - D xi^2', errs[-1] < 1e-3 and all(e2 < e1 for e1, e2 in zip(errs, errs[1:])),
      ', '.join(f'{e:.2e}' for e in errs))
check('its error shrinks like dt, a factor near 4 per halving of h', all(rt > 3.5 for rt in ratios), ', '.join(f'{rt:.2f}' for rt in ratios))
check('at the stated walk (h = 0.1) p = 0.45 and q = 0.35', close((1 - rv + cv * 0.8 * 0.01 / 2 / 0.1) / 2, 0.45, 1e-12))

# ------------------------------------------------------------ 6. the limit by iterating the walk, D = 1 and c = 2.5 held fixed
def gauss(x, m, s2):
    return np.exp(-(x - m)**2 / (2 * s2)) / np.sqrt(2 * np.pi * s2)

sup, gaps = [], []
for j in range(4):
    h = 0.1 / 2**j
    dtv = 0.8 * h * h / 2
    nsteps = int(round(1.0 / dtv))
    d = 2.5 * dtv / h
    Pj = walk_dist((0.8 + d) / 2, (0.8 - d) / 2, nsteps)
    xj = h * np.arange(-nsteps, nsteps + 1)
    vj = float((Pj * (xj - (Pj * xj).sum())**2).sum())
    gaps.append(2.0 - vj)
    sup.append(float(np.max(np.abs(Pj / h - gauss(xj, 2.5, 2.0)))))
check('variance gap is c^2 dt t at each step: 0.025, 0.00625, ...',
      all(close(g, 6.25 * 0.8 * (0.1 / 2**j)**2 / 2, 1e-8) for j, g in enumerate(gaps)), ', '.join(f'{g:.6f}' for g in gaps))
check('density error against N(ct, 2Dt) falls on each halving of dx', all(b < a for a, b in zip(sup, sup[1:])) and sup[-1] < 0.002,
      ', '.join(f'{s:.5f}' for s in sup))

# ------------------------------------------------------------ 7. the wrong scalings named in the model
cs_fixed = [0.1 * (0.1 / 2**j) / (0.8 * (0.1 / 2**j)**2 / 2) for j in range(4)]
check('a fixed bias 0.1 makes c grow like 1/dx: 2.5, 5, 10, 20', all(close(a, b, 1e-9) for a, b in zip(cs_fixed, [2.5, 5, 10, 20])))
Ds_lin = [0.8 * (0.1 / 2**j)**2 / (2 * 0.004 * (1 / 2**j)) for j in range(4)]
check('dt shrinking like dx sends D to 0: 1, 0.5, 0.25, 0.125', all(close(a, b, 1e-9) for a, b in zip(Ds_lin, [1, 0.5, 0.25, 0.125])))

# ------------------------------------------------------------ 8. the figures as written in the item
model, rub = it['model'], ' '.join(r['text'] for r in it['rubric'])
for s in ['D = 0.8 \\times 0.01/0.008 = 1', 'c = 0.1 \\times 0.1/0.004 = 2.5', 'n = t/\\Delta t = 250', '(p - q)\\Delta x = 0.01',
          '(p + q)\\Delta x^2 = 0.008', '0.008 - 0.0001 = 0.0079', 'the variance is 1.975', 'mean $ct = 2.5$', 'variance $2Dt = 2$',
          'c^2\\Delta t\\,t = 0.025', 'r = 0.2', '\\tfrac13 D\\,\\Delta x', '\\tfrac12\\Delta t\\max|u_{tt}|']:
    check('model states ' + s, s in model)
for s in ['$D = 1$', '$c = 2.5$', 'mean 2.5', 'variance 1.975', 'c^2\\Delta t\\,t = 0.025', '$2Dt = 2$']:
    check('rubric states ' + s, s in rub)
for s in ['\\Delta x = 0.1', '\\Delta t = 0.004', 'p = 0.45', 'q = 0.35', 't = 1']:
    check('prompt states ' + s, s in it['prompt'])

print()
print(f'{len(fails)} failures' if fails else 'all checks passed')
sys.exit(1 if fails else 0)
