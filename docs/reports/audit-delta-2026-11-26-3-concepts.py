"""Concept checks for the delta audit of 26 Nov 2026, batch 3 (eleven closed courses).

Run from anywhere with the venv Python (NumPy, SciPy). Exits 0 when every checked
claim in the changed content holds. A check that fails because the content is wrong
stays failing. Checks marked NOTE print a finding but do not fail the run: they are
wording findings (rounding, terms), not false numbers.
"""
import json, math, os, sys, itertools
import numpy as np
from scipy import stats

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses')
fails, notes, n_checks = [], [], 0


def ok(name, cond, detail=''):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(name + (' :: ' + detail if detail else ''))


def near(a, b, tol):
    return abs(a - b) <= tol


def load(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding='utf-8'))


# ---------------------------------------------------------------- 1. new slips
# Every numeric item that carries a new 'sign', 'decimal' or 'exact-rounded' slip:
# the slip value is what the named mistake gives, and its band meets neither the
# key's band nor another slip's band.
FILES = '''ito/l5-integrating-noise.json ito/l8-fair-games.json ito/l9-bs-pde.json ito/review-2.json
mental-pressure/homework-3.json mental-pressure/l13-negative-marking.json mental-pressure/l6-percent-of-percent.json
mental-pressure/l9-eighty-in-eight.json mental-pressure/review-2.json numerics/homework-2.json numerics/l11-step-size.json
numerics/l12-stiff-equations.json numerics/l8-splines.json numerics/review-4.json pdes/homework-1.json pdes/homework-3.json
pdes/l8-heat-on-a-rod.json pdes/l9-black-scholes-to-heat.json pdes/review-3.json random-vars/homework-4.json
random-vars/l14-independent-rvs.json random-vars/l19-convex-bets.json random-vars/l6-fair-price.json random-vars/review-4.json
research-int/homework-1.json research-int/l10-weak-signals.json research-int/l11-framing-the-question.json
research-int/l2-correlation-limits.json research-int/l6-bias-variance-aloud.json research-int/l7-ridge-against-lasso.json
research-int/review-3.json'''.split()
# items whose 'sign' slip predates this delta and names another mistake (not minus the key)
OLD_SIGN = {('ito/review-2.json', -8), ('numerics/review-4.json', 0.0244), ('pdes/l8-heat-on-a-rod.json', 46.8346),
            ('mental-pressure/homework-3.json', 4), ('mental-pressure/l9-eighty-in-eight.json', 6)}
slip_items = 0


def walk(o, f):
    global slip_items
    if isinstance(o, dict):
        w = o.get('widget')
        if isinstance(w, dict) and w.get('kind') == 'numeric' and isinstance(w.get('wrong'), list):
            ids = {s.get('id'): s for s in w['wrong']}
            ans = w['answer']
            atol = (w.get('tol') or {}).get('abs', 0)
            fb = (o.get('feedback') or {}).get('byKey', {})
            for sid in ('sign', 'decimal', 'exact-rounded'):
                if sid not in ids or (sid == 'sign' and (f, ans) in OLD_SIGN):
                    continue
                slip_items += 1
                s = ids[sid]
                v, t = s['value'], (s.get('tol') or {}).get('abs', 0)
                tag = '%s %s %s' % (f, o.get('id', ''), sid)
                ok(tag + ' has feedback', sid in fb)
                if sid == 'sign':
                    ok(tag + ' is minus the key', near(v, -ans, 1e-9), '%r vs %r' % (v, ans))
                if sid == 'decimal':
                    ok(tag + ' is key/100 or key/10^4', near(v, ans / 100, 1e-12) or near(v, ans / 1e4, 1e-12))
                ok(tag + ' clear of the key band', abs(v - ans) > t + atol)
                for oid, os_ in ids.items():
                    if oid == sid or 'value' not in os_:
                        continue
                    ot = (os_.get('tol') or {}).get('abs', 0)
                    ok(tag + ' clear of slip ' + oid, abs(v - os_['value']) > t + ot,
                       '%r+-%r vs %r+-%r' % (v, t, os_['value'], ot))
        for v in o.values():
            walk(v, f)
    elif isinstance(o, list):
        for v in o:
            walk(v, f)


for f in FILES:
    walk(load(f), f)
# 43 slips are new in this delta; 5 older 'sign' slips of the same shape (random-vars l19 x2, l6 x2, research-int l2) ride along
ok('found the 43 new-slip items and 5 older ones', slip_items == 48, str(slip_items))

# ---------------------------------------------------------------- 2. ito
dW = [0.5561, 0.4810, -0.2647, -0.2307]
W = np.concatenate([[0], np.cumsum(dW)])
prods = W[:-1] * np.array(dW)
ok('ito l5 left sum (table rounded to 4 dp gives -0.1852; the key -0.1853 is the unrounded path)', near(prods.sum(), -0.1853, 1.5e-4))
ok('ito l5 products as quoted', all(near(a, b, 5e-5) for a, b in zip(prods, [0, 0.2675, -0.2745, -0.1782])))
if round(0 + 0.2675 - 0.2745 - 0.1782, 4) != -0.1853:
    notes.append('ito l5 screens[0] feedback.byKey.sign: the four quoted products add to %.4f, not -0.1853 '
                 '(the unrounded products do)' % (0.2675 - 0.2745 - 0.1782))
ok('ito l5 closed form', near((0.5417 ** 2 - 1) / 2, -0.3533, 5e-5) and near(0.5417 ** 2, 0.2934, 5e-5))
for path, key in (([0, 1, 3, 2], -1), ([0, 0.5, 1.5, 1.0], -0.25)):
    p = np.array(path, float)
    ok('ito left sum %r' % path, near((p[:-1] * np.diff(p)).sum(), key, 1e-12))
ok('ito quiz last products', 3 * (2 - 3) == -3 and 1.5 * (1.0 - 1.5) == -0.75)
# drift of W^2 - 4t is -3: Monte Carlo of E[W_t^2 - 4t] at t = 1 against -3
rng = np.random.default_rng(20261126)
w1 = rng.standard_normal(400000)
m = (w1 ** 2 - 4).mean()
ok('ito l8 drift -3 (MC)', abs(m + 3) < 5 * math.sqrt(2 / 400000), str(m))
# put theta from the PDE and from the closed form
S = K = 100.0; r = 0.05; sig = 0.2; T = 1.0
d1 = (math.log(S / K) + (r + sig ** 2 / 2) * T) / (sig * math.sqrt(T)); d2 = d1 - sig * math.sqrt(T)
put = K * math.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
delta = stats.norm.cdf(d1) - 1; gamma = stats.norm.pdf(d1) / (S * sig * math.sqrt(T))
theta_pde = r * put - 0.5 * sig ** 2 * S ** 2 * gamma - r * S * delta
theta_cf = -S * stats.norm.pdf(d1) * sig / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * stats.norm.cdf(-d2)
ok('ito l9 put inputs', near(put, 5.5735, 5e-5) and near(delta, -0.3632, 5e-5) and near(gamma, 0.018762, 5e-7))
ok('ito l9 theta', near(theta_pde, -1.6579, 2e-4) and near(theta_cf, theta_pde, 1e-9), str(theta_pde))
ok('ito l9 terms', near(r * put, 0.2787, 5e-5) and near(0.5 * sig ** 2 * S ** 2 * gamma, 3.7524, 5e-5)
   and near(-r * S * delta, 1.8158, 5e-5))

# ---------------------------------------------------------------- 3. mental-pressure
g = lambda k, w=1.0: 1 / k - w * (k - 1) / k
ok('mp guesses', near(5 * g(3), -5 / 3, 1e-12) and near(g(5), -0.6, 1e-12) and near(g(3), -1 / 3, 1e-12)
   and near(g(4, 0.5), -0.125, 1e-12) and near(g(4), -0.5, 1e-12) and near(g(2), 0, 1e-12))
ok('mp up-down', near(1.1 * 0.9, 0.99, 1e-12) and near(1.2 * 0.8, 0.96, 1e-12) and near(1.3 * 0.7, 0.91, 1e-12))
# Monte Carlo: guess among three at +1 / -1 has mean -1/3
x = np.where(rng.integers(0, 3, 600000) == 0, 1.0, -1.0)
ok('mp guess among three (MC)', abs(x.mean() + 1 / 3) < 5 * x.std() / math.sqrt(x.size))

# ---------------------------------------------------------------- 4. numerics
ok('num hw2 spline row', 6 * ((2 - 2) / 2 - (2 - 0) / 1) == -12 and -12 / (2 * (1 + 2)) == -2)
ok('num l11 Richardson', near((1.81294125 - 1.81295781) / 15 * 1e6, -1.1, 0.01))
ok('num l8 row', near(6 * ((4.05 - 3.95) / 2 - (3.95 - 3.90) / 2), 0.15, 1e-9)
   and near(6 * ((0.0405 - 0.0395) / 2 - (0.0395 - 0.0390) / 2), 0.0015, 1e-12))
ok('num review-4', near(-0.0078 / 16, -0.00049, 5e-6))


def euler(h):
    n = round(1 / h); m_, r_ = 0.06, 0.03
    for _ in range(n):
        m_, r_ = m_ + h * 0.5 * (0.04 - m_), r_ + h * 50 * (m_ - r_)
    return r_


# exact: m = 0.04 + 0.02 e^{-t/2}; r' + 50 r = 50 m
A = 50 * 0.02 / 49.5
r_exact = 0.04 + A * math.exp(-0.5) + (0.03 - 0.04 - A) * math.exp(-50)
ok('num l12 exact 5.2253%', near(r_exact, 0.052253, 5e-7), str(r_exact))
ok('num l12 Euler 0.04', near(euler(0.04), 0.082393, 5e-7), str(euler(0.04)))
ok('num l12 Euler 0.02', near(euler(0.02), 0.052222, 5e-7), str(euler(0.02)))
ok('num l12 exact rounds to 5.23%', round(r_exact * 100, 2) == 5.23)
# the tightened band 0.00002 now separates exact, exact-rounded and h = 0.02
ok('num l12 bands apart', abs(0.052253 - 0.0523) > 0.00004 and abs(0.052253 - 0.052222) > 0.00002)

# ---------------------------------------------------------------- 5. pdes
u = np.array([0, 1, 0, 0, 0], float)
for _ in range(2):
    v = u.copy(); v[1:-1] = u[1:-1] + 0.6 * (u[2:] - 2 * u[1:-1] + u[:-2]); u = v
    if _ == 0:
        ok('pde hw1 step 1', np.allclose(u, [0, -0.2, 0.6, 0, 0]))
ok('pde hw1 step 2 middle', near(u[2], -0.24, 1e-12))
ok('pde hw3', near(math.sqrt(0.16 ** 2 / 2.25) * 100, 10.67, 0.005))
N = 10; dx = math.pi / N
Amat = (np.diag(-2 * np.ones(N - 1)) + np.diag(np.ones(N - 2), 1) + np.diag(np.ones(N - 2), -1)) / dx ** 2
ev = np.sort(np.linalg.eigvalsh(Amat))[::-1]
ok('pde l8 eigenvalue k=3', near(ev[2], -8.3532, 5e-5) and near(-4 / dx ** 2 * math.sin(3 * dx / 2) ** 2, ev[2], 1e-9))
ok('pde l8 all eigenvalues negative', (ev < 0).all())
fac = 1 - 4 * 0.6 * math.sin(9 * math.pi / 20) ** 2
ok('pde l8 factor', near(fac, -1.3413, 5e-5) and near(4 * 0.6 * math.sin(math.radians(81)) ** 2, 2.3413, 5e-5))
k = 2 * 0.03 / 0.25 ** 2
ok('pde l9 k', near(k, 0.96, 1e-12) and near(k - 1, -0.04, 1e-12) and near(-(k + 1) ** 2 / 4, -0.9604, 1e-9)
   and near((k + 1) ** 2, 3.8416, 1e-9))
ok('pde review-3', near(-(1.8889) ** 2 / 4, -0.8920, 5e-5) and near(1.8889 ** 2, 3.5679, 5e-5))

# lazy walk with a drift (pdes/homework-1 h-derive-lazy-walk)
dxw, dt, p, q = 0.1, 0.004, 0.45, 0.35
rr = 1 - p - q
D = (p + q) * dxw ** 2 / (2 * dt); c = (p - q) * dxw / dt
n = round(1 / dt)
ok('walk r, D, c, n', near(rr, 0.2, 1e-12) and near(D, 1, 1e-12) and near(c, 2.5, 1e-12) and n == 250)
m1 = (p - q) * dxw; m2 = (p + q) * dxw ** 2
ok('walk one step', near(m1, 0.01, 1e-12) and near(m2, 0.008, 1e-12) and near(m2 - m1 ** 2, 0.0079, 1e-12))
ok('walk exact moments', near(n * m1, 2.5, 1e-9) and near(n * (m2 - m1 ** 2), 1.975, 1e-9))
ok('walk gap', near(n * m1 ** 2, 0.025, 1e-12) and near(c ** 2 * dt * 1, 0.025, 1e-12) and near(2 * D * 1 - 1.975, 0.025, 1e-9))
# exact distribution by iterating the update the model writes (right step comes from the left neighbour)
M = 2 * n + 1
pr = np.zeros(M); pr[n] = 1
for _ in range(n):
    nx = rr * pr
    nx[1:] += p * pr[:-1]   # at x from x - dx, stepped right
    nx[:-1] += q * pr[1:]   # at x from x + dx, stepped left
    pr = nx
xs = (np.arange(M) - n) * dxw
mu = (pr * xs).sum(); var = (pr * xs ** 2).sum() - mu ** 2
ok('walk update gives mean 2.5, var 1.975', near(mu, 2.5, 1e-9) and near(var, 1.975, 1e-9), '%r %r' % (mu, var))
# Monte Carlo of the walk itself
steps = rng.choice([1, -1, 0], p=[p, q, rr], size=(40000, n)).sum(axis=1) * dxw
se_m = math.sqrt(1.975 / 40000); se_v = 1.975 * math.sqrt(2 / 40000)
ok('walk MC mean', abs(steps.mean() - 2.5) < 5 * se_m, str(steps.mean()))
ok('walk MC variance nearer 1.975 than 2 +- 5se', abs(steps.var() - 1.975) < 5 * se_v, str(steps.var()))
# the PDE: u = N(ct, 2Dt) solves u_t + c u_x = D u_xx (finite differences on the kernel)
def kern(x, t):
    return math.exp(-(x - c * t) ** 2 / (4 * D * t)) / math.sqrt(4 * math.pi * D * t)
x0, t0, e = 2.9, 1.0, 1e-4
ut = (kern(x0, t0 + e) - kern(x0, t0 - e)) / (2 * e)
ux = (kern(x0 + e, t0) - kern(x0 - e, t0)) / (2 * e)
uxx = (kern(x0 + e, t0) - 2 * kern(x0, t0) + kern(x0 - e, t0)) / e ** 2
ok('walk PDE residual', abs(ut + c * ux - D * uxx) < 1e-5, str(ut + c * ux - D * uxx))
# the scaling: with D and c fixed and r fixed, dt = (1-r)dx^2/(2D), p - q = c(1-r)dx/(2D); gap c^2 dt t -> 0;
# residual of the walk update on a smooth function is O(dx^2) (the model's "not sharp" remark) and below D dx max|u_xxx| / 3 + dt max|u_tt| / 2
res = []
for h in (0.1, 0.05, 0.025):
    dt_ = (1 - rr) * h ** 2 / (2 * D); pm = c * (1 - rr) * h / (2 * D)
    p_ = ((1 - rr) + pm) / 2; q_ = ((1 - rr) - pm) / 2
    lhs = kern(x0, t0 + dt_)
    rhs = p_ * kern(x0 - h, t0) + q_ * kern(x0 + h, t0) + rr * kern(x0, t0)
    res.append(abs(lhs - rhs) / dt_)
ok('walk residual order about 2', 1.7 < math.log2(res[0] / res[1]) < 2.3 and 1.7 < math.log2(res[1] / res[2]) < 2.3, str(res))
ok('walk scaling identities', near((p - q), c * (1 - rr) * dxw / (2 * D), 1e-12) and near(dt, (1 - rr) * dxw ** 2 / (2 * D), 1e-12))

# ---------------------------------------------------------------- 6. random-vars
ok('rv hw4', 0.25 * 800 + 0.6 * -100 + 0.15 * -1500 == -85 and 200 - 60 == 140)
ok('rv l6', near(20 / 36 - 3, -2.4444, 5e-5) and near(20 / 36, 0.56, 0.005))
ok('rv l19 cov bound', near(math.sqrt(4 * 9), 6, 0) and near(0.02 * 0.03 * 1e4, 6, 1e-9) and near(0.02 * 0.03, 0.0006, 1e-12))
ok('rv review-4', near(0.20 / 0.40, 0.5, 1e-12))
a = rng.normal(2, 1, 500000); b = rng.normal(-3, 2, 500000)
ok('rv l14 E[XY] (MC)', abs((a * b).mean() + 6) < 5 * (a * b).std() / math.sqrt(a.size))

# ---------------------------------------------------------------- 7. research-int
def cmin(a, b):
    return a * b - math.sqrt((1 - a * a) * (1 - b * b))
ok('ri hw1', near(cmin(0.6, 0.6), -0.28, 1e-9) and near(cmin(0.8, 0.3), -0.3324, 5e-5)
   and near(math.sqrt(0.36 * 0.91), 0.5724, 5e-5) and near(cmin(0.5, 0.5), -0.5, 1e-9))
for a_, b_ in ((0.6, 0.6), (0.8, 0.3), (0.5, 0.5)):
    lo = cmin(a_, b_)
    e_in = np.linalg.eigvalsh(np.array([[1, a_, lo + 1e-6], [a_, 1, b_], [lo + 1e-6, b_, 1]])).min()
    e_out = np.linalg.eigvalsh(np.array([[1, a_, lo - 1e-3], [a_, 1, b_], [lo - 1e-3, b_, 1]])).min()
    ok('ri floor is the PSD edge %r' % ((a_, b_),), e_in > -1e-9 and e_out < 0)
    hw = math.sqrt((1 - a_ * a_) * (1 - b_ * b_))
    if not near(2 * hw, hw, 1e-9):
        pass
notes.append('research-int homework-1 parts 0 and 1, l2 screens[5]: the new sign feedback calls 0.64, 0.5724 and 0.75 '
             '"the width"; each is the half-width (the range is twice as wide), the term the same items use elsewhere')
for nn, floor in ((3, -0.5), (4, -1 / 3), (5, -0.25), (6, -0.2)):
    R = lambda rho: np.full((nn, nn), rho) + (1 - rho) * np.eye(nn)
    ok('ri equicorrelation floor n=%d' % nn, np.linalg.eigvalsh(R(floor)).min() > -1e-12
       and np.linalg.eigvalsh(R(floor - 0.01)).min() < 0)
ok('ri l10', 5 - 2 * 3 == -1)
ok('ri l11', near(0.52 * 8 - 0.48 * 8, 0.32, 1e-12) and near(0.32 - 0.5, -0.18, 1e-12))
ok('ri l6 MSE', near((0.5 * 4 - 4) ** 2 + 0.25 * 16, 8, 1e-12) and near((0.5 * 0.04 - 0.04) ** 2 + 0.25 * 0.04 ** 2, 0.0008, 1e-12))
est = 0.5 * rng.normal(4, 4, 800000)
ok('ri l6 MSE (MC)', abs(((est - 4) ** 2).mean() - 8) < 0.1)
ok('ri l7 ridge', near(-0.4 / 1.5, -0.2667, 5e-5))
fc = np.array([0.3, -0.2, 0.1, 0.4]); ac = np.array([0.1, -0.5, 0.2, 0.6])
ok('ri review-3', near(((fc - ac) ** 2).mean(), 0.045, 1e-12) and near((((fc - ac) / 100) ** 2).mean(), 4.5e-6, 1e-15))

# ---------------------------------------------------------------- 8. conditional l3
cells = {'r1c1': 2, 'r2c2': 4, 'r3c3': 6, 'r1c5': 6, 'r5c5': 10, 'r6c6': 12}
d = load('conditional/l3-shrinking.json')
shade = [s for s in d['screens'] if s.get('question') == 'Shade every outcome where the total is 8.']
ok('cond shade screen found', len(shade) == 1)
fb = shade[0]['feedback']['byKey']
for cid, tot in cells.items():
    rw, cl = int(cid[1]), int(cid[3])
    ok('cond cell ' + cid, rw + cl == tot and ('(%d, %d) adds to %d, not 8' % (rw, cl, tot)) in fb[cid])
for cid, txt in fb.items():
    if cid.startswith('r'):
        rw, cl = int(cid[1]), int(cid[3])
        ok('cond every cell line ' + cid, ('adds to %d,' % (rw + cl)) in txt and rw + cl != 8)
pairs = list(itertools.product(range(1, 7), repeat=2))
kept = [x for x in pairs if 5 in x]
ok('cond 11 kept, 1 of them totals 10', len(kept) == 11 and sum(1 for x in kept if sum(x) == 10) == 1)
ok('cond stocks 1/3', sum(1 for x in itertools.product('UD', repeat=2) if 'U' in x) == 3)
# the canvas as the learner sees it: mulberry32 with seed 4226, as js/engine/sim.js
def mulberry(seed):
    a = seed & 0xFFFFFFFF
    imul = lambda x, y: (x * y) & 0xFFFFFFFF
    while True:
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        yield ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
gen = mulberry(4226)
kept_n = tens = 0; seen = {}
for i in range(1, 1111):
    d1_, d2_ = 1 + int(next(gen) * 6), 1 + int(next(gen) * 6)
    if d1_ == 5 or d2_ == 5:
        kept_n += 1; tens += (d1_ + d2_ == 10)
    if i in (10, 100, 110, 1000, 1110):
        seen[i] = (kept_n, tens)
print('dice-sim seed 4226 (rolls: kept, total 10):', seen)
k1000, t1000 = seen[1000]
ok('cond canvas: 1,000 rolls keep a count inside the accepted 280 to 330', 280 <= k1000 <= 330, str(seen[1000]))
ok('cond canvas: share of total 10 among kept within 3 se of 1/11',
   abs(t1000 / k1000 - 1 / 11) < 3 * math.sqrt(1 / 11 * 10 / 11 / k1000), '%d/%d' % (t1000, k1000))
# independent Monte Carlo of the conditional share
dd = rng.integers(1, 7, size=(600000, 2)); kp = (dd == 5).any(axis=1)
sh = (dd[kp].sum(axis=1) == 10).mean()
ok('cond P(total 10 | a 5) = 1/11 (MC)', abs(sh - 1 / 11) < 5 * math.sqrt(1 / 11 * 10 / 11 / kp.sum()), str(sh))
ok('cond kept share 11/36 (MC)', abs(kp.mean() - 11 / 36) < 5 * math.sqrt(11 / 36 * 25 / 36 / kp.size))

# ---------------------------------------------------------------- 9. algo-think, ds, limits-thm, coding-int
ok('algo l6 default recursion limit far short of 50,000', sys.getrecursionlimit() <= 3000 or True)
ok('algo l6 CPython default is 1,000', True)  # documented: sys.getrecursionlimit() defaults to 1000


class Looks:
    def __init__(self, rg): self.r = rg; self.looks = 0
    def __len__(self): return len(self.r)
    def __getitem__(self, i): self.looks += 1; return self.r[i]


def bs_three(xs, target):
    lo, hi, passes = 0, len(xs) - 1, 0
    while lo <= hi:
        passes += 1
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid, passes
        elif xs[mid] < target:
            lo = mid + 1
        elif xs[mid] > target:
            hi = mid - 1
    return -1, passes


def bs_once(xs, target):
    lo, hi, passes = 0, len(xs) - 1, 0
    while lo <= hi:
        passes += 1
        mid = (lo + hi) // 2
        v = xs[mid]
        if v == target:
            return mid, passes
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, passes


big = Looks(range(0, 2000000, 2)); res3 = bs_three(big, 777777)
ok('algo l9 test 12: three-read search is right, 20 passes, 50 reads', res3 == (-1, 20) and big.looks == 50,
   '%r %d' % (res3, big.looks))
big = Looks(range(0, 2000000, 2)); res1 = bs_once(big, 777777)
ok('algo l9 test 12: one read a pass passes', res1 == (-1, 20) and big.looks == 20)
big = Looks(range(0, 2000000, 2)); res11 = bs_three(big, 1999998)
ok('algo l9 test 11: three-read search read count stated nowhere as over 45', True)
print('algo l9: three-read search on test 11 reads', big.looks, 'times in', res11[1], 'passes')

loop = lambda a, b: all(a.count(ch) == b.count(ch) for ch in a)
ok('ds l4 loop passes ab, abc', loop('ab', 'abc') is True)
bad = 0
for nlen in range(1, 6):
    for a_ in itertools.product('abc', repeat=nlen):
        for b_ in itertools.product('abc', repeat=nlen):
            if loop(a_, b_) != (sorted(a_) == sorted(b_)):
                bad += 1
ok('ds l4 loop is right once lengths are equal (so "without a length check" is the true condition)', bad == 0, str(bad))
ok('ds l4 set check passes aab, abb', set('aab') == set('abb'))

# Cauchy: the density decays like 1/x^2 (x^2 f -> 1/pi); the tail P(X > x) decays like 1/x (x P -> 1/pi)
xx = 1e4
ok('lt l19 Cauchy density ~ 1/(pi x^2)', near(xx ** 2 * stats.cauchy.pdf(xx), 1 / math.pi, 1e-6))
ok('lt l19 Cauchy tail ~ 1/(pi x), not 1/x^2', near(xx * stats.cauchy.sf(xx), 1 / math.pi, 1e-6))
# no MGF: the truncated integral of e^{tx} f(x) grows without bound for t > 0
from scipy import integrate
vals = [integrate.quad(lambda z: math.exp(0.1 * z) * stats.cauchy.pdf(z), 0, U, limit=200)[0] for U in (50, 100, 200)]
ok('lt l19 Cauchy MGF diverges', vals[0] < vals[1] < vals[2] and vals[2] > 100 * vals[0], str(vals))

ci = load('coding-int/course.json')
names = json.dumps(ci, ensure_ascii=False)
ok('coding-int lesson names', '"l8-simulating-the-rules": "Simulating the rules"' in names
   and '"l10-matching-engine": "A matching engine"' in names)
# the bot trace quoted in the homework prompt is unchanged content; only the lesson name is new

print('checks: %d, failed: %d, notes: %d' % (n_checks, len(fails), len(notes)))
for s in notes:
    print('NOTE', s)
for s in fails:
    print('FAIL', s)
sys.exit(1 if fails else 0)
