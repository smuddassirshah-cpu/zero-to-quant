"""Recompute every number stated in numerics level 4 (One option, three ways) by a second method, and check
that each stated value appears in the lesson JSON at its path (app/tools/numbers_lib.py).
Run: python3 docs/reports/numerics-L4-numbers.py   (needs numpy and scipy; exits 0 when every check passes)
Routes. Black-Scholes by math.erf, checked against scipy.integrate.quad over the lognormal density. Explicit grids by
an own loop, and their stability by the bound. Implicit and Crank-Nicolson by scipy.linalg.solve_banded (the lessons
used the Thomas algorithm). Gauss-Legendre by leggauss, checked against quad. Exact Monte Carlo variances by closed
form and by quad over z. Seeded estimates by NumPy's default_rng (CPython; the same values came from Pyodide 0.27.7's
NumPy 2.0.2 to 1e-14), each checked against the closed form within 3 SE and with a second seed. The barrier by its
closed form, the Broadie-Glasserman shift and simulation; the Asian control by its closed form and the simulated
geometric mean. Every code widget's solution must pass its hidden tests here, and its starter must fail one.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad
from scipy.linalg import solve_banded
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('numerics', 4)
fails = []


def check(name, got, want, tol):
    if not abs(float(got) - float(want)) <= tol:
        fails.append(f'{name}: computed {got!r}, stated {want!r} (tol {tol})')


def E(f, path, stated, computed=None, tol=None, fmt=None):
    """stated appears at path; computed (if given) rounds to it within tol (default: half the last digit)."""
    if computed is not None:
        if tol is None:
            s = repr(float(stated)); d = len(s.split('.')[1]) if '.' in s and 'e' not in s else 0
            tol = 0.5 * 10 ** -d + 1e-12
        check(f'{f} {path}', computed, stated, tol)
    lv.expect(f, path, stated, fmt=fmt)


# ---------- closed forms, two ways ----------
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs(S, K, r, s, T, kind='call'):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    if kind == 'call':
        return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)
    return K * math.exp(-r * T) * Phi(-d2) - S * Phi(-d1)


def bs_quad(S, K, r, s, T, kind='call'):
    m, v = (r - s * s / 2) * T, s * math.sqrt(T); zs = (math.log(K / S) - m) / v
    pay = (lambda z: S * math.exp(m + v * z) - K) if kind == 'call' else (lambda z: K - S * math.exp(m + v * z))
    a, b = (zs, 12) if kind == 'call' else (-12, zs)
    return math.exp(-r * T) * quad(lambda z: pay(z) * norm.pdf(z), a, b, epsabs=1e-13, epsrel=1e-13)[0]


B = bs(100, 100, .05, .2, 1); BP = bs(100, 95, .04, .3, .5, 'put')
check('BS quad call', bs_quad(100, 100, .05, .2, 1), B, 1e-10); check('BS quad put', bs_quad(100, 95, .04, .3, .5, 'put'), BP, 1e-10)
check('BS 10.450584', B, 10.450584, 5e-7); check('put 5.170209', BP, 5.170209, 5e-7)
d1 = (0.05 + 0.02) / 0.2; gamma_bs = norm.pdf(d1) / (100 * 0.2); check('d1', d1, 0.35, 1e-12)
check('gamma bs', gamma_bs, 0.018762, 5e-7)
h = 1e-3; check('gamma by differences', (bs(100 + h, 100, .05, .2, 1) - 2 * B + bs(100 - h, 100, .05, .2, 1)) / h ** 2, gamma_bs, 1e-5)


# ---------- grids ----------
def explicit(S0, K, r, s, T, Smax, M, N, kind='call'):
    dS, dt = Smax / M, T / N; j = np.arange(M + 1); S = j * dS
    V = np.maximum(S - K, 0.0)
    a = 0.5 * dt * (s * s * j * j - r * j); b = -dt * (s * s * j * j + r); c = 0.5 * dt * (s * s * j * j + r * j)
    with np.errstate(all='ignore'):
        for n in range(N):
            V[1:-1] = a[1:-1] * V[:-2] + (1 + b[1:-1]) * V[1:-1] + c[1:-1] * V[2:]
            V[0] = 0.0; V[-1] = Smax - K * math.exp(-r * (n + 1) * dt)
    return float(np.interp(S0, S, V)), V, S


def theta(S0, K, r, s, T, Smax, M, N, th, start=0, kind='call', full=False):
    dS, dt = Smax / M, T / N; j = np.arange(M + 1); S = j * dS
    V = np.maximum(S - K, 0.0) if kind == 'call' else np.maximum(K - S, 0.0)
    al = 0.5 * (s * s * j * j - r * j)[1:-1]; be = -(s * s * j * j + r)[1:-1]; ga = 0.5 * (s * s * j * j + r * j)[1:-1]
    for n in range(N):
        t = 1.0 if n < start else th
        disc = K * math.exp(-r * (n + 1) * dt)
        lo, hi = (0.0, Smax - disc) if kind == 'call' else (disc, 0.0)
        rhs = V[1:-1] + (1 - t) * dt * (al * V[:-2] + be * V[1:-1] + ga * V[2:])
        rhs[0] += t * dt * al[0] * lo; rhs[-1] += t * dt * ga[-1] * hi
        ab = np.zeros((3, M - 1)); ab[0, 1:] = -t * dt * ga[:-1]; ab[1] = 1 - t * dt * be; ab[2, :-1] = -t * dt * al[1:]
        V = np.concatenate(([lo], solve_banded((1, 1), ab, rhs), [hi]))
    p = float(np.interp(S0, S, V))
    return (p, V, S) if full else p


L13, L14, L15, L16, L17 = 'l13', 'l14', 'l15', 'l16', 'l17'
p500, V500, S500 = explicit(100, 100, .05, .2, 1, 200, 100, 500)
check('explicit = theta 0', theta(100, 100, .05, .2, 1, 200, 100, 500, 0.0), p500, 1e-10)
E(L13, 'screens[1].widget.accept', 10.4428, p500); E(L13, 'screens[1].explain.text', 10.442791, p500)
E(L13, 'screens[1].explain.text', 10.450584, B); E(L13, 'screens[1].explain.text', -0.0078, p500 - B)
# hand step at j = 50
dt = 0.002; j = 50
a50, b50, c50 = 0.5 * dt * (.04 * j * j - .05 * j), 1 - dt * (.04 * j * j + .05), 0.5 * dt * (.04 * j * j + .05 * j)
E(L13, 'screens[3].explain.text', 0.0975, a50); E(L13, 'screens[3].explain.text', 0.7999, b50); E(L13, 'screens[3].explain.text', 0.1025, c50)
E(L13, 'screens[3].explain.text', 0.205, a50 * 0 + b50 * 0 + c50 * 2); E(L13, 'screens[3].explain.text', 0.9999, a50 + b50 + c50, 1e-9)
E(L13, 'screens[3].hints[2].text', 100.05, .04 * 2500 + .05)
p1700 = explicit(100, 100, .05, .2, 1, 200, 200, 1700)[0]
E(L13, 'screens[4].prose', 10.4487, p1700); E(L13, 'screens[4].explain.text', 10.44873, p1700)
E(L13, 'screens[4].explain.text', -0.0019, p1700 - B); E(L13, 'screens[4].widget.answer', -0.0019, p1700 - B)
check('ratio 4.2', (p500 - B) / (p1700 - B), 4.2, 0.05)
E(L13, 'screens[5].widget.answer', 401, math.ceil(.04 * 100 ** 2 + .05), 0); E(L13, 'screens[5].explain.text', 400.05, .04 * 1e4 + .05)
p300 = explicit(100, 100, .05, .2, 1, 200, 100, 300); p250 = explicit(100, 100, .05, .2, 1, 200, 100, 250)
E(L13, 'screens[5].explain.text', 379169, p300[0], 1); E(L13, 'screens[5].explain.text', '4.5 \\times 10^{30}'); check('4.5e30', p250[0] / 1e30, 4.5, 0.05)
check('blow-up starts at the top', int(np.argmax(np.abs(p300[1]))) >= 90, True, 0)
p330 = explicit(100, 100, .05, .2, 1, 200, 100, 330)
E(L13, 'quiz[1].prose', 10.4439, p330[0]); lv.expect(L13, 'quiz[1].prose', '7.5 \\times 10^{14}'); check('7.5e14', np.abs(p330[1]).max() / 1e14, 7.5, 0.05)
check('N=400 unstable by the bound', 1 / 400 > 1 / (.04 * 1e4 + .05), True, 0)
p_m200 = explicit(100, 100, .05, .2, 1, 200, 200, 500)[0]
E(L13, 'screens[6].explain.text', '4.1 \\times 10^{277}'); check('4.1e277', p_m200 / 1e277, 4.1, 0.05)
E(L13, 'screens[6].explain.text', 1601, math.ceil(.04 * 200 ** 2 + .05), 0); E(L13, 'screens[7].widget.options[0].text', 3601, math.ceil(.04 * 300 ** 2 + .05), 0)
E(L13, 'screens[7].widget.options[1].text', 1201); E(L13, 'screens[7].widget.options[3].text', 694, round(401 * math.sqrt(3)), 1)
E(L13, 'screens[7].explain.text', 27, 3 * 9, 0)
E(L13, 'quiz[0].widget.answer', 101, math.ceil(.04 * 2500 + .05), 0)
fwd = []
for N in (500, 1000):
    dS, dtt = 2.0, 1 / N; jj = np.arange(101); S = jj * dS; V = S - 100.0
    a = 0.5 * dtt * (.04 * jj * jj - .05 * jj); b = -dtt * (.04 * jj * jj + .05); c = 0.5 * dtt * (.04 * jj * jj + .05 * jj)
    for n in range(N):
        V[1:-1] = a[1:-1] * V[:-2] + (1 + b[1:-1]) * V[1:-1] + c[1:-1] * V[2:]
        V[0] = -100 * math.exp(-.05 * (n + 1) * dtt); V[-1] = 200 - 100 * math.exp(-.05 * (n + 1) * dtt)
    fwd.append(V[50] - (100 - 100 * math.exp(-.05)))
lv.expect(L13, 'quiz[2].explain.text', '2.4 \\times 10^{-4}'); check('forward error', fwd[0], 2.4e-4, 5e-6); check('forward halves', fwd[0] / fwd[1], 2.0, 0.01)
check('share exact', explicit(100, 0, .05, .2, 1, 200, 100, 500)[0], 100, 1e-9)
# l14
for nu, cn in ((20, -0.951), (80, -0.9876)):
    check(f'cn factor {nu}', (1 - 2 * nu) / (1 + 2 * nu), cn, 5e-4 if nu == 20 else 5e-5)
E(L14, 'screens[1].widget.options[0].text', -0.951, (1 - 40) / 41); E(L14, 'screens[1].widget.options[1].text', 0.012, 1 / 81)
E(L14, 'screens[1].widget.options[2].text', -79, 1 - 80, 0); E(L14, 'quiz[2].widget.answer', -0.9876, (1 - 160) / 161)
check('88% after ten steps', abs((1 - 160) / 161) ** 10, 0.88, 0.005)
E(L14, 'screens[6].widget.options[1].why', -0.988, (1 - 160) / 161)
imp = {N: theta(100, 100, .05, .2, 1, 200, 100, N, 1.0) - B for N in (25, 50, 100)}
cnv = {N: theta(100, 100, .05, .2, 1, 200, 100, N, 0.5) - B for N in (25, 50, 100)}
for N, wi, wc in ((25, -0.0519, -0.0095), (50, -0.0309, -0.0098), (100, -0.0204, -0.00987)):
    check(f'implicit {N}', imp[N], wi, 5e-5); check(f'cn {N}', cnv[N], wc, 5e-5 if N < 100 else 5e-6)
    E(L14, 'screens[5].canvas.params.rows', round(imp[N], 4))
E(L14, 'screens[5].canvas.params.rows', round(cnv[100], 5))
c200 = theta(100, 100, .05, .2, 1, 200, 200, 200, 0.5) - B; c400 = theta(100, 100, .05, .2, 1, 200, 400, 400, 0.5) - B
E(L14, 'screens[5].explain.text', -0.00246, c200, 5e-6); E(L14, 'screens[5].explain.text', -0.000616, c400, 5e-7)
E(L14, 'quiz[0].widget.answer', 4.0, c200 / c400, 0.02)
for N, want in ((25, -0.042), (50, -0.021), (100, -0.0105)):
    E(L14, 'screens[5].explain.text', want, imp[N] - cnv[100], 5e-4)
E(L14, 'screens[5].hints[0].text', -0.0099, cnv[100], 1e-4)
pc, Vc, Sg = theta(100, 100, .05, .2, 1, 200, 400, 10, 0.5, full=True)
pi_, Vi, _ = theta(100, 100, .05, .2, 1, 200, 400, 10, 1.0, full=True)
pr, Vr, _ = theta(100, 100, .05, .2, 1, 200, 400, 10, 0.5, 2, full=True)
G = lambda V: (V[201] - 2 * V[200] + V[199]) / 0.25
E(L14, 'screens[6].explain.text', 1.2526, G(Vc)); E(L14, 'screens[6].explain.text', 10.2767, pc); E(L14, 'screens[6].widget.options[2].text', 0.01957, G(Vi))
E(L14, 'screens[6].explain.text', 0.01904, G(Vr)); E(L14, 'screens[6].explain.text', 10.4324, pr); E(L14, 'screens[6].question', 0.018762, gamma_bs)
E(L14, 'screens[6].explain.text', 67, G(Vc) / gamma_bs, 0.5); E(L14, 'screens[6].widget.options[2].why', 0.105, B - pi_)
check('implicit gamma 4% high', G(Vi) / gamma_bs - 1, 0.04, 0.005); E(L14, 'screens[6].widget.options[3].why', 1.5, 100 * (G(Vr) / gamma_bs - 1), 0.05)
E(L14, 'screens[6].prose', 80, 0.5 * .04 * 200 ** 2 * 0.1, 1e-9); E(L14, 'screens[10].widget.answer', 66.8, G(Vc) / gamma_bs)
E(L14, 'screens[10].explain.text', 0.17, B - pc); E(L14, 'screens[9].canvas.params.rows', 10.432399, pr)
E(L14, 'screens[9].canvas.params.rows', 10.398664, theta(100, 100, .05, .2, 1, 200, 100, 25, 1.0)); E(L14, 'screens[9].canvas.params.rows', 10.44071, theta(100, 100, .05, .2, 1, 200, 100, 100, 0.5))
E(L14, 'screens[8].explain.text', 1200, 3 * 400, 0); check('dense 21 million', 400 ** 3 / 3 / 1e6, 21, 0.5)
for th, want in ((0.0, 10.4428), (1.0, 10.4386), (0.5, 10.4407)):
    E(L14, 'quiz[1].prose', want, theta(100, 100, .05, .2, 1, 200, 100, 500, th))
E(L14, 'quiz[1].prose', 0.4, 0.5 * .04 * 100 ** 2 * 0.002, 1e-12)
# pivots of the 4 by 4
A = np.array([[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]], float); dvec = np.array([1, 0, 0, 1], float)
piv = [2.0]
for k in range(1, 4):
    piv.append(2 - 1 / piv[-1])
for v, s in zip(piv[1:], (1.5, 1.33, 1.25)):
    E(L14, 'screens[3].explain.text', s, v, 0.005)
check('x = ones', np.abs(np.linalg.solve(A, dvec) - 1).max(), 0, 1e-12)

# ---------- Monte Carlo: exact moments two ways ----------
D = math.exp(-.05); STz = lambda z: 100 * np.exp(.03 + .2 * z)
Ez = lambda g, pts=(-0.15,): quad(lambda z: g(z) * norm.pdf(z), -12, 12, points=list(pts), limit=400)[0]
Y = lambda z: D * max(STz(z) - 100, 0); X = lambda z: D * STz(z)
EY2_cf = math.exp(-.1) * (1e4 * math.exp(.14) * Phi(.35 + .2) - 2e4 * math.exp(.05) * Phi(.35) + 1e4 * Phi(.15))
VY = EY2_cf - B * B; check('E[Y^2] by quad', Ez(lambda z: Y(z) ** 2), EY2_cf, 1e-7)
s_exact = math.sqrt(VY)
E(L15, 'screens[1].prose', 14.7194, s_exact)
for n, txt in ((100, 1.472), (1000, 0.465), (10000, 0.147), (100000, 0.0465)):
    E(L15, 'screens[1].feedback.correct', txt, s_exact / math.sqrt(n))
E(L15, 'screens[0].explain.text', 0.329, 14.72 / math.sqrt(2000)); E(L15, 'screens[3].widget.answer', 2166609, math.ceil((s_exact / 0.01) ** 2), 0)
E(L15, 'screens[3].hints[1].text', 1471.94, 14.7194 / 0.01, 1e-6); E(L15, 'screens[3].explain.text', 14.719404, s_exact); E(L15, 'screens[3].explain.text', 2166609, math.ceil((s_exact / 0.01) ** 2), 0)
check('rounded s gives 2,166,608', math.ceil((14.7194 / 0.01) ** 2), 2166608, 0); E(L15, 'screens[4].widget.answer', 0.0465, 0.147 / math.sqrt(10))
E(L15, 'screens[4].feedback.correct', 3.16, math.sqrt(10)); E(L15, 'screens[9].widget.answer', 800000, 50000 * (0.04 / 0.01) ** 2, 1e-6)
E(L15, 'quiz[1].widget.answer', 90000, 2500 * (0.30 / 0.05) ** 2, 1e-6)


def mc_call(n, seed, S0=100, K=100, r=.05, s=.2, T=1):
    z = np.random.default_rng(seed).standard_normal(n)
    y = math.exp(-r * T) * np.maximum(S0 * np.exp((r - s * s / 2) * T + s * math.sqrt(T) * z) - K, 0)
    return y.mean(), y.std(ddof=1) / math.sqrt(n)


m0, se0 = mc_call(100000, 0); m1, se1 = mc_call(100000, 1)
check('plain seed 0 within 3 SE', abs(m0 - B) < 3 * se0, True, 0); check('SE near exact', se0, s_exact / math.sqrt(1e5), 3e-4)
E(L15, 'screens[5].prose', 10.4362, m0); E(L15, 'screens[5].prose', 0.0465, se0); E(L15, 'screens[5].prose', -0.31, (m0 - B) / se0)
E(L15, 'screens[5].prose', 10.3578, m1); E(L15, 'screens[5].prose', 0.0464, se1); E(L15, 'screens[5].widget.answer', 10.345, m0 - 1.96 * se0)
E(L15, 'screens[5].explain.text', -2.0, (m1 - B) / se1, 0.005); check('seed 1 interval misses', m1 + 1.96 * se1 < B, True, 0)
E(L15, 'screens[5].hints[1].text', 0.0912, 1.96 * se0)


def dao(S, K, H, r, s, T):
    lam = (r + s * s / 2) / (s * s); y = math.log(H * H / (S * K)) / (s * math.sqrt(T)) + lam * s * math.sqrt(T)
    return bs(S, K, r, s, T) - (S * (H / S) ** (2 * lam) * Phi(y) - K * math.exp(-r * T) * (H / S) ** (2 * lam - 2) * Phi(y - s * math.sqrt(T)))


E(L15, 'screens[6].prose', 8.6655, dao(100, 100, 90, .05, .2, 1))
# second route for the continuous barrier: quad over the killed density, by the reflection principle in log space
mu = .03; sg = .2; b_ = math.log(0.9)
dens = lambda x: (norm.pdf((x - mu) / sg) - math.exp(2 * mu * b_ / sg ** 2) * norm.pdf((x - 2 * b_ - mu) / sg)) / sg
check('barrier by quad', D * quad(lambda x: (100 * math.exp(x) - 100) * dens(x), 0, 3, epsabs=1e-12)[0], dao(100, 100, 90, .05, .2, 1), 1e-8)


def barrier_mc(m, n, seed):
    rng = np.random.default_rng(seed); dtm = 1 / m; x = np.full(n, math.log(100)); alive = np.ones(n, bool)
    for _ in range(m):
        x = x + (.05 - .02) * dtm + .2 * math.sqrt(dtm) * rng.standard_normal(n); alive &= x > math.log(90)
    y = D * np.maximum(np.exp(x) - 100, 0) * alive
    return y.mean(), y.std(ddof=1) / math.sqrt(n)


rows = lv.text(L15, 'screens[6].canvas.params.rows')
for m, sim, shift in ((12, 9.572, 9.580), (52, 9.152, 9.174), (252, 8.936, 8.914)):
    pm, sem = barrier_mc(m, 200000, 0)
    check(f'barrier {m}', pm, sim, 5e-4); check(f'barrier se {m}', sem, 0.033, 5e-4)
    bg = dao(100, 100, 90 * math.exp(-0.5826 * .2 * math.sqrt(1 / m)), .05, .2, 1); check(f'BG {m}', bg, shift, 5e-4)
    check(f'barrier MC near shift {m}', abs(pm - bg) < 3 * sem, True, 0)
    lv.expect(L15, 'screens[6].canvas.params.rows', sim); lv.expect(L15, 'screens[6].canvas.params.rows', shift)
check('monthly seed 1 agrees', abs(barrier_mc(12, 200000, 1)[0] - 9.572) < 3 * 0.033, True, 0)
E(L15, 'screens[6].explain.text', 9.58, dao(100, 100, 90 * math.exp(-0.5826 * .2 * math.sqrt(1 / 12)), .05, .2, 1), 0.005)
E('review', 'items[5].explain.text', 0.49, 9.152 - 8.6655, 0.005); E('review', 'items[5].explain.text', 0.01, 0.033 / math.sqrt(10), 0.0005)
E('homework', 'items[4].widget.answer', 89.34, 90 * math.exp(-0.5826 * .2 / math.sqrt(252))); E('homework', 'items[4].explain.text', 0.00734, 0.5826 * .2 / math.sqrt(252))

# ---------- l16: control variates and antithetics ----------
VX = Ez(lambda z: X(z) ** 2, ()) - 1e4; check('Var X closed form', VX, 1e4 * (math.exp(.04) - 1), 1e-6)
EYX_cf = D * D * (1e4 * math.exp(.14) * Phi(.35 + .2) - 100 * 100 * math.exp(.05) * Phi(.35))   # E[S_T (S_T - K)^+] discounted twice
CYX = Ez(lambda z: Y(z) * X(z)) - B * 100; check('Cov closed form', CYX, EYX_cf - B * 100, 1e-6)
rho = CYX / math.sqrt(VY * VX); bstar = CYX / VX; vrf = 1 / (1 - rho ** 2)
E(L16, 'screens[1].explain.text', 274.91, CYX); E(L16, 'screens[1].explain.text', 408.11, VX); E(L16, 'screens[2].explain.text', 216.66, VY)
E(L16, 'screens[1].widget.answer', 0.6736, bstar); E(L16, 'screens[4].prose', 0.9245, rho); E(L16, 'screens[4].widget.answer', 6.88, vrf)
E(L16, 'screens[2].explain.text', 31.48, VY * (1 - rho ** 2)); E(L16, 'screens[2].widget.lines[5].why', 74.95, VY - 2 * CYX + VX)
E(L16, 'screens[4].explain.text', 315000, 2166609 / vrf, 600); E(L16, 'screens[0].explain.text', 2.6, math.sqrt(vrf), 0.05)
E(L16, 'screens[2].feedback.byKey.d1', 0.64, Phi(.35), 0.005); E(L16, 'screens[3].explain.text', 5.3, 1 / (1 - .81), 0.05); E(L16, 'screens[3].explain.text', 50, 1 / (1 - .99 ** 2), 0.5)
E(L16, 'quiz[0].widget.answer', 5.26, 1 / (1 - .81)); E('review', 'items[6].widget.answer', 10.26, 1 / (1 - .95 ** 2))
E(L16, 'screens[11].widget.answer', 36, 36000 * (1 - .9995 ** 2), 0.1); E('homework', 'items[3].widget.answer', 39600, 1e6 * (1 - .98 ** 2), 1e-6)
E('homework', 'items[3].explain.text', 25.3, 1 / (1 - .98 ** 2))
zc = np.random.default_rng(0).standard_normal(100000)
y = D * np.maximum(STz(zc) - 100, 0); x = D * STz(zc); bh = np.cov(y, x)[0, 1] / np.var(x, ddof=1); adj = y - bh * (x - 100)
cv0, cse0 = adj.mean(), adj.std(ddof=1) / math.sqrt(1e5)
E(L16, 'screens[5].prose', 0.67307, bh); E(L16, 'screens[5].prose', 10.4484, cv0); E(L16, 'screens[5].prose', 0.0178, cse0)
E(L16, 'screens[5].widget.answer', 6.86, (se0 / cse0) ** 2); E(L16, 'screens[5].explain.text', 0.12, abs((cv0 - B) / cse0))
check('cv seed 0 within 3 SE', abs(cv0 - B) < 3 * cse0, True, 0)
z1 = np.random.default_rng(1).standard_normal(100000); y1 = D * np.maximum(STz(z1) - 100, 0); x1 = D * STz(z1)
a1 = y1 - np.cov(y1, x1)[0, 1] / np.var(x1, ddof=1) * (x1 - 100); cv1, cse1 = a1.mean(), a1.std(ddof=1) / math.sqrt(1e5)
E(L17, 'screens[3].prose', 10.4275, cv1); E(L17, 'screens[3].prose', 0.0177, cse1); E(L17, 'screens[3].widget.answer', -1.3, (cv1 - B) / cse1, 0.005)
CYa = Ez(lambda z: Y(z) * Y(-z)) - B * B
E(L16, 'screens[6].prose', -0.501, CYa / VY); E(L16, 'screens[6].prose', 54.06, (VY + CYa) / 2); E(L16, 'screens[6].prose', 108.33, VY / 2)
E(L16, 'screens[6].widget.answer', 2.0, (VY / 2) / ((VY + CYa) / 2), 0.01)
R = lambda z: Y(z) - bstar * (X(z) - 100); VR = Ez(lambda z: R(z) ** 2) - B * B; CR = Ez(lambda z: R(z) * R(-z)) - B * B
E(L16, 'screens[6].explain.text', 30.67, (VR + CR) / 2); check('VR = Var(Y)(1 - rho^2)', VR, VY * (1 - rho ** 2), 1e-6)
za = np.random.default_rng(0).standard_normal(50000); ya = (D * np.maximum(STz(za) - 100, 0) + D * np.maximum(STz(-za) - 100, 0)) / 2
E(L16, 'screens[6].explain.text', 10.4721, ya.mean()); E(L16, 'screens[6].explain.text', 0.0329, ya.std(ddof=1) / math.sqrt(50000))
P = bs(100, 100, .05, .2, 1, 'put'); Str = B + P; Ys = lambda z: D * abs(STz(z) - 100)
VS = Ez(lambda z: Ys(z) ** 2) - Str ** 2; CS = Ez(lambda z: Ys(z) * Ys(-z)) - Str ** 2
E(L16, 'screens[8].prose', 16.0241, Str); check('straddle by quad', Ez(Ys), Str, 1e-8)
E(L16, 'screens[8].explain.text', 0.645, CS / VS); E(L16, 'screens[8].explain.text', 175.1, VS); E(L16, 'screens[8].explain.text', 144.0, (VS + CS) / 2)
E(L16, 'screens[8].explain.text', 87.6, VS / 2); E(L16, 'screens[8].explain.text', 0.61, (VS / 2) / ((VS + CS) / 2))
# Asian: closed form two ways (formula and simulated geometric mean)
m = 12; t = np.arange(1, m + 1) / m; mu_g = math.log(100) + .03 * t.mean(); v_g = .04 / m ** 2 * np.minimum.outer(t, t).sum()
Gcf = D * (math.exp(mu_g + v_g / 2) * Phi((mu_g - math.log(100) + v_g) / math.sqrt(v_g)) - 100 * Phi((mu_g - math.log(100)) / math.sqrt(v_g)))
E(L16, 'screens[7].prose', 5.9402, Gcf)


def asian(n, seed):
    zz = np.random.default_rng(seed).standard_normal((n, m)); dtm = 1 / m
    lg = math.log(100) + np.cumsum(.03 * dtm + .2 * math.sqrt(dtm) * zz, axis=1)
    ya_ = D * np.maximum(np.exp(lg).mean(axis=1) - 100, 0); xa = D * np.maximum(np.exp(lg.mean(axis=1)) - 100, 0)
    b = np.cov(ya_, xa)[0, 1] / np.var(xa, ddof=1); aa = ya_ - b * (xa - Gcf)
    return aa.mean(), aa.std(ddof=1) / math.sqrt(n), ya_.mean(), ya_.std(ddof=1) / math.sqrt(n), np.corrcoef(ya_, xa)[0, 1], xa.mean(), xa.std(ddof=1) / math.sqrt(n)


A0, A1 = asian(100000, 0), asian(100000, 1)
check('geometric simulated', abs(A0[5] - Gcf) < 3 * A0[6], True, 0)
E(L16, 'screens[7].explain.text', 6.1561, A0[0]); E(L16, 'screens[7].canvas.params.rows', 0.00075, A0[1], 5e-6); E(L16, 'screens[7].explain.text', 6.1558, A1[0])
E(L16, 'screens[7].canvas.params.rows', 0.00074, A1[1], 5e-6); E(L16, 'screens[7].canvas.params.rows', 6.1722, A0[2]); E(L16, 'screens[7].canvas.params.rows', 0.0269, A0[3])
E(L16, 'screens[7].prose', 0.9996, A0[4]); E(L16, 'screens[7].widget.answer', 1281, (A0[3] / A0[1]) ** 2, 1); check('plain Asian within 1 SE', abs(A0[2] - A0[0]) < A0[3], True, 0)
check('seeds agree', abs(A0[0] - A1[0]) < 3 * math.hypot(A0[1], A1[1]), True, 0)
# put control slope sign (l16 quiz)
zp = np.random.default_rng(0).standard_normal(100000); STp = 100 * np.exp((.04 - .045) * .5 + .3 * math.sqrt(.5) * zp)
yp = math.exp(-.02) * np.maximum(95 - STp, 0); xp = math.exp(-.02) * STp; bp = np.cov(yp, xp)[0, 1] / np.var(xp, ddof=1)
E(L16, 'quiz[2].explain.text', -0.292, bp); ap = yp - bp * (xp - 100); mp_, msp = ap.mean(), ap.std(ddof=1) / math.sqrt(1e5)

# ---------- l17 ----------
def gl(S0, K, r, s, T, kind, n):
    mm, v = (r - s * s / 2) * T, s * math.sqrt(T); zs = (math.log(K / S0) - mm) / v
    a, b = (zs, 8) if kind == 'call' else (-8, zs); xg, wg = np.polynomial.legendre.leggauss(n); z = (b - a) / 2 * xg + (a + b) / 2
    pay = S0 * np.exp(mm + v * z) - K if kind == 'call' else K - S0 * np.exp(mm + v * z)
    return math.exp(-r * T) * (b - a) / 2 * float(np.sum(wg * pay * norm.pdf(z)))


def crr(S0, K, r, s, T, n, kind='call'):
    dtn = T / n; u = math.exp(s * math.sqrt(dtn)); p = (math.exp(r * dtn) - 1 / u) / (u - 1 / u); k = np.arange(n + 1)
    V = np.maximum(S0 * u ** (n - 2 * k) - K, 0) if kind == 'call' else np.maximum(K - S0 * u ** (n - 2 * k), 0)
    for _ in range(n):
        V = math.exp(-r * dtn) * (p * V[:-1] + (1 - p) * V[1:])
    return float(V[0])


cnc = theta(100, 100, .05, .2, 1, 200, 400, 200, .5, 2); glc = gl(100, 100, .05, .2, 1, 'call', 32)
E(L17, 'screens[0].widget.rows', 10.44992, cnc); E(L17, 'summary.ideas[0]', '-6.6 \\times 10^{-4}'); check('cn err', cnc - B, -6.6e-4, 5e-6)
E(L17, 'screens[0].canvas.params.lines', 10.450583572185, glc, 5e-13); lv.expect(L17, 'screens[0].question', '-2.6 \\times 10^{-13}'); check('gl err', glc - B, -2.6e-13, 5e-14)
check('gl vs quad', glc, bs_quad(100, 100, .05, .2, 1), 1e-10)
t500, t1000, t1001, t2000 = (crr(100, 100, .05, .2, 1, n) for n in (500, 1000, 1001, 2000))
E(L17, 'screens[0].widget.rows', 10.446585, t500); E(L17, 'screens[0].feedback.correct', -0.0022, cv0 - B); E(L17, 'screens[0].feedback.correct', -0.004, t500 - B)
E(L17, 'screens[0].feedback.correct', -0.00066, cnc - B, 5e-6)
E(L17, 'screens[4].prose', -0.004, t500 - B); E(L17, 'screens[4].prose', -0.002, t1000 - B); E(L17, 'screens[4].prose', 0.0018, t1001 - B)
E(L17, 'screens[4].explain.text', -0.001, t2000 - B); E(L17, 'quiz[2].explain.text', '-10^{-4}'); check('zigzag average', ((t1000 + t1001) / 2 - B) / 1e-4, -1.2, 0.1)
for (M, N), s in (((200, 100), -2.65), ((400, 200), -6.64), ((800, 400), -1.66)):
    e = theta(100, 100, .05, .2, 1, 200, M, N, .5, 2) - B; check(f'cn ref {M}', e / 10 ** math.floor(math.log10(abs(e))), s, 0.005)
    lv.expect(L17, 'screens[2].canvas.params.rows', s)
e1600 = theta(100, 100, .05, .2, 1, 200, 1600, 800, .5, 2) - B
E(L17, 'screens[2].widget.answer', -4.15, e1600 * 1e5, 0.01); E(L17, 'screens[2].explain.text', -4.15, -1.66e-4 / 4 * 1e5, 1e-9)
cnp = theta(100, 95, .04, .3, .5, 190 * 200 / 190, 400, 200, .5, 2, kind='put'); glp = gl(100, 95, .04, .3, .5, 'put', 32); tp = crr(100, 95, .04, .3, .5, 1000, 'put')
E(L17, 'screens[5].canvas.params.rows', 5.170209, BP); E(L17, 'screens[5].canvas.params.rows', 5.169608, cnp); E(L17, 'screens[5].canvas.params.rows', 5.170208971851, glp, 5e-13)
E(L17, 'screens[5].canvas.params.rows', 5.1672, mp_); E(L17, 'screens[5].canvas.params.rows', 0.0181, msp); E(L17, 'screens[5].canvas.params.rows', 5.170502, tp)
E(L17, 'screens[5].widget.answer', -0.17, (mp_ - BP) / msp, 0.005); check('put MC within 3 SE', abs(mp_ - BP) < 3 * msp, True, 0)
check('put gl vs quad', glp, bs_quad(100, 95, .04, .3, .5, 'put'), 1e-10)
off = {M: theta(100, 100, .05, .2, 1, 300, M, 200, .5, 2) - B for M in (390, 400, 420)}
E(L17, 'screens[6].explain.text', 9.1, off[400] * 1e4); check('off grid flips sign', off[390] < 0 < off[400] and off[420] < 0, True, 0)
for M in (390, 420):
    E(L17, 'screens[6].canvas.params.rows', round(off[M], 5))
E(L17, 'quiz[0].explain.text', 0.035, 1.96 * cse0); E(L17, 'screens[9].widget.options[1].text', 0.035, 1.96 * cse0)
E('review', 'items[8].widget.options[1].why', 0.12, gl(100, 100, .05, .2, 1, 'call', 1) * 0 + (lambda: (lambda x, w: 8 * float(np.sum(w * D * np.maximum(100 * np.exp(.03 + .2 * 8 * x) - 100, 0) * norm.pdf(8 * x))))(*np.polynomial.legendre.leggauss(32)) - B)(), 0.005)

# ---------- review and homework ----------
E('review', 'items[0].widget.answer', 901, math.ceil(.04 * 150 ** 2 + .05), 0); E('review', 'items[1].widget.answer', -0.00049, -0.0078 / 16, 1e-5)
E('review', 'items[1].explain.text', -0.00045, explicit(100, 100, .05, .2, 1, 200, 400, 6401)[0] - B, 5e-6)
E('review', 'items[1].explain.text', 6401, math.ceil(.04 * 400 ** 2 + .05), 0); E('review', 'items[2].feedback.correct', -0.98, (1 - 100) / 101); E('review', 'items[2].explain.text', 2, 100 * (1 - 99 / 101), 0.05)
E('review', 'items[4].widget.answer', 640000, 40000 * (0.12 / 0.03) ** 2, 1e-6); E('review', 'items[9].widget.answer', 0.0244, 1 / 41)
E('homework', 'items[0].widget.answer', 0.4879, 1 - 0.002 * (.04 * 6400 + .05)); E('homework', 'items[0].explain.text', 0.2158, 1 - 0.002 * (.04 * 99 ** 2 + .05))
E('homework', 'items[0].explain.text', 0.0198, 1 - 0.0025 * (.04 * 99 ** 2 + .05)); E('homework', 'items[0].explain.text', 393, math.ceil(.04 * 99 ** 2 + .05), 0)
E('homework', 'items[5].widget.answer', 63, 2 * 32 - 1, 0)
E('homework', 'items[7].model', 5.61, math.sqrt(VY * (1 - rho ** 2))); E('homework', 'items[7].model', 14.72, s_exact)

# ---------- remaining stated values ----------
E(L16, 'screens[4].hints[1].text', 0.85471, rho ** 2); E(L14, 'quiz[2].explain.text', 1.2, 100 * (1 - 159 / 161), 0.05)
E(L14, 'quiz[2].explain.text', 88, 100 * (159 / 161) ** 10, 0.5); E(L15, 'screens[1].explain.text', 31.62, math.sqrt(1000)); E(L15, 'screens[1].explain.text', 316.2, math.sqrt(1e5))
E(L16, 'screens[7].hints[1].text', 35.9, 0.0269 / 0.00075, 0.05); E(L16, 'screens[7].explain.text', 0.02692, A0[3]); E(L16, 'screens[7].explain.text', 0.000752, A0[1])
E('review', 'items[0].explain.text', 2.25, 901 / 401, 0.005); E(L17, 'screens[3].hints[1].text', -0.023, cv1 - B, 5e-4); E(L17, 'screens[5].hints[1].text', -0.003, mp_ - BP, 5e-4)
hw = lv.files['homework-4']['items'][6]['widget']; nsh = {}; exec(hw['solution'], nsh)
rep = nsh['price_report'](100, 95, .04, .3, .5, 'put', 0.005)
E('homework', 'items[6].explain.text', 320, rep['fd'][2] / 160, 0); E('homework', 'items[6].explain.text', '-9.4 \\times 10^{-4}'); check('hw fd err', rep['fd'][0] - BP, -9.4e-4, 5e-6)
check('hw fd estimate honest', rep['fd'][1], abs(rep['fd'][0] - BP), 5e-6); E('homework', 'items[6].explain.text', 16, rep['quad'][2], 0)
E('homework', 'items[6].explain.text', 2560000, rep['mc'][2], 0); E('homework', 'items[6].explain.text', 0.0036, rep['mc'][1])


def mulberry(seed):
    st = [seed & 0xFFFFFFFF]
    def nxt():
        st[0] = (st[0] + 0x6D2B79F5) & 0xFFFFFFFF; t = st[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def walk_caption(seed, run=0):
    """The walk canvas's paths (walk.js: one uniform, then a Box-Muller normal, per step) and the payoff panel."""
    rng = mulberry((seed * 7919 + run * 104729) & 0xFFFFFFFF); ys = []
    for _ in range(2000):
        x = 4.60517
        for _ in range(50):
            rng(); u = 0.0
            while u <= 1e-12:
                u = rng()
            x += 0.0006 + 0.028284 * math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * rng())
        ys.append(D * max(math.exp(x) - 100, 0))
    ys = np.array(ys); return ys.mean(), ys.std(ddof=1) / math.sqrt(2000)


wm, wse = walk_caption(5)
check('walk caption SE inside the answer band', abs(wse - 0.33) <= 0.03, True, 0); check('walk SE near exact', wse, 14.7194 / math.sqrt(2000), 0.03)
check('walk mean within 3 SE', abs(wm - B) < 3 * wse, True, 0); E(L15, 'screens[0].widget.answer', 0.33, wse, 0.03)

# ---------- code widgets: solution passes, starter fails ----------
def run_tests(src, w):
    ok = []
    for case in w['tests']:
        ns = {}
        try:
            exec(src, ns)
            if case.get('setup'):
                exec(case['setup'], ns)
            if case.get('compare') == 'raises':
                try:
                    eval(case['call'], ns); ok.append(False)
                except Exception as e:
                    ok.append(type(e).__name__ == case['expect'])
                continue
            got = eval(case['call'], ns); want = eval(case['expect'], ns)
            if case.get('compare') == 'equal':
                ok.append(got == want)
            else:
                tol = case.get('tol', {}); g, wv = np.ravel(np.asarray(got, float)), np.ravel(np.asarray(want, float))
                ok.append(g.shape == wv.shape and bool(np.all(np.abs(g - wv) <= np.maximum(tol.get('abs', 0), tol.get('rel', 1e-9 if not tol else 0) * np.abs(wv)))))
        except Exception:
            ok.append(False)
    return ok


widgets = []
for ref, doc in lv.files.items():
    for i, s in enumerate(doc.get('screens', []) + doc.get('items', [])):
        w = s.get('widget') or {}
        if w.get('kind') == 'code':
            widgets.append((ref, i, w))
for ref, i, w in widgets:
    good = run_tests(w['solution'], w); bad = run_tests(w['starter'], w)
    if not all(good):
        fails.append(f'{ref} #{i}: solution fails tests {[k for k, v in enumerate(good) if not v]}')
    if all(bad):
        fails.append(f'{ref} #{i}: starter passes every test')
print(f'code widgets checked: {len(widgets)}')

for f in fails:
    print('BAD', f)
print(f'second-method checks: {len(fails)} failures')
lv.report()
sys.exit(1 if fails else 0)
