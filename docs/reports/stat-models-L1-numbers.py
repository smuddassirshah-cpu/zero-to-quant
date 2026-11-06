"""Recompute every number stated in stat-models level 1 and check it at its JSON path.

Run: python3 docs/reports/stat-models-L1-numbers.py   (NumPy only; exits 0 when every check passes)

Each fitted value is computed twice: by this script's own IRLS, Newton or profile fits in NumPy, and by
statsmodels 0.14.4 / SciPy 1.14.1 in Pyodide 0.27.7 (NumPy 2.0.2), whose results are pasted in SM below.
The datasets use np.random.default_rng(seed) in the brief's order of draws; NumPy 2.0.2 (Pyodide) and the
local NumPy give identical streams for these seeds (checked: every dataset matched byte for byte).
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("stat-models", 1)


def expit(x):
    return 1 / (1 + np.exp(-x))


def chk(f, path, v, dp=None):
    lv.expect(f, path, (round(v, dp) if dp else int(round(v))) if dp is not None else v)


def agree(a, b, tol=1e-6, what=''):
    a, b = np.atleast_1d(np.asarray(a, float)), np.atleast_1d(np.asarray(b, float))
    if not np.all(np.abs(a - b) <= tol):
        print('BAD agreement', what, a, b)
        sys.exit(1)


# ---------- special functions (pure Python) ----------
def chi2_sf(x, k):
    if k == 1:
        return math.erfc(math.sqrt(x / 2))
    if k == 2:
        return math.exp(-x / 2)
    raise ValueError


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; c = 1 + aa / c; d = 1 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; c = 1 + aa / c; d = 1 / d; de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def betainc(a, b, x):
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


def f_sf(F, d1, d2):
    return betainc(d2 / 2, d1 / 2, d2 / (d2 + d1 * F))


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


# ---------- data ----------
rng = np.random.default_rng(11); L = rng.uniform(0, 1, 300); y1 = rng.binomial(1, expit(-6 + 10 * L))
X1 = np.column_stack([np.ones(300), L])
L12 = np.array([0.10, 0.20, 0.30, 0.35, 0.40, 0.50, 0.55, 0.60, 0.70, 0.80, 0.85, 0.95]); y12 = np.array([0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1.0])
X12 = np.column_stack([np.ones(12), L12])
rng = np.random.default_rng(23); v = rng.uniform(10, 40, 120); t = np.where(v > 25, rng.choice([5, 15], 120), rng.choice([30, 60], 120)); y2 = rng.poisson(t * np.exp(-0.5 + 0.06 * v))
X2 = np.column_stack([np.ones(120), v])
rng = np.random.default_rng(61); x3 = rng.normal(0, 1, 200); z3 = rng.normal(0, 1, 200); lam = rng.gamma(2.0, 0.5 * np.exp(1.5 + 0.4 * x3)); y3 = rng.poisson(lam)
X3 = np.column_stack([np.ones(200), x3]); X3z = np.column_stack([np.ones(200), x3, z3])
rng = np.random.default_rng(13); dd = rng.integers(0, 6, 500); fl = rng.binomial(1, expit(1.2 - 0.8 * dd)); Xf = np.column_stack([np.ones(500), dd])
x6 = np.arange(6.0); y6 = np.array([0, 0, 1, 0, 1, 1.0]); X6 = np.column_stack([np.ones(6), x6])
xs = np.arange(1, 7.0); ys = np.array([0, 0, 0, 1, 1, 1.0]); Xs = np.column_stack([np.ones(6), xs])

# statsmodels / SciPy in Pyodide (second computation)
SM = dict(ols=[-0.198849, 1.154923], d1=[-5.451164308995994, 8.690639009216971], d1se=[0.6113276792765376, 0.9689939179424305], d1iter=6,
          d12=[-3.721961708778537, 6.133700299510535], d12se=[2.148486722973753, 3.5486519938433054], d12ll=-5.853040559781917,
          fill=[1.2938176166660813, -0.972966654113978], fillse=[0.20258, 0.090413],
          d2=[-0.47859278790894677, 0.05913496159076384], d2se=[0.03852063362306456, 0.0015338677027787316], d2dev=111.22889544489959,
          d2no=[4.583922353677266, -0.020324374175238122], logt=[-0.356171, 0.057307, 0.976228], logtse=[0.120743, 0.002296, 0.022235],
          six=[-3.0350689646265123, 1.214027585850605], sixse=[2.5457112130828934, 0.9125848383120105], sixdev=4.955973670099225,
          d3=[1.4334307985486983, 0.3854102222821626], d3dev=631.3708912525251, d3pear=625.317438667392, d3zdev=625.8138622619642, d3zpear=618.8258954946053,
          d3zp=0.019082, nb_alpha=0.542248, nb_llf1=-498.1779126805123, nb_llf2=-497.58636734220283, pen=[-3.510915, 5.424648], sep=[-144.318226, 41.233779])


# ---------- own fits ----------
def irls(X, y, fam, off=None, tol=1e-12, it=100, hist=False):
    off = np.zeros(len(y)) if off is None else off
    b = np.zeros(X.shape[1])
    if fam == 'pois':
        b[0] = np.log(y.sum() / np.exp(off).sum())
    out = []
    for _ in range(it):
        eta = X @ b + off
        mu = expit(eta) if fam == 'bin' else np.exp(eta)
        W = mu * (1 - mu) if fam == 'bin' else mu
        z = eta - off + (y - mu) / W
        nb = np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (W * z))
        out.append(nb.copy())
        if np.max(np.abs(nb - b)) < tol:
            b = nb
            break
        b = nb
    eta = X @ b + off; mu = expit(eta) if fam == 'bin' else np.exp(eta); W = mu * (1 - mu) if fam == 'bin' else mu
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ (W[:, None] * X))))
    return (b, se, out) if hist else (b, se)


def bdev(X, y, b):
    eta = X @ b
    return 2 * np.sum(np.logaddexp(0, eta) - y * eta)


def pdev(y, mu):
    yl = np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0.0)
    return 2 * np.sum(yl - (y - mu))


def ll12(b0, b1):
    eta = b0 + b1 * L12
    return -np.sum(np.logaddexp(0, eta) - y12 * eta)


# OLS on D1
ols = np.linalg.lstsq(X1, y1, rcond=None)[0]; agree(ols, SM['ols'], 5e-7, 'ols')
fv = X1 @ ols; out01 = int(((fv < 0) | (fv > 1)).sum())
cross0 = -ols[0] / ols[1]
b1, se1 = irls(X1, y1, 'bin'); agree(b1, SM['d1'], 1e-9, 'd1'); agree(se1, SM['d1se'], 1e-6, 'd1se')
b12, se12 = irls(X12, y12, 'bin'); agree(b12, SM['d12'], 1e-9); agree(se12, SM['d12se'], 1e-6)
# grid search as a third check of the D12 peak
gb0 = np.linspace(-3.8, -3.65, 301); gb1 = np.linspace(6.0, 6.25, 301)
G = np.array([[ll12(a, b) for b in gb1] for a in gb0]); i, j = np.unravel_index(np.argmax(G), G.shape)
agree([gb0[i], gb1[j]], b12, 1e-3, 'grid')
bf, sef = irls(Xf, fl, 'bin'); agree(bf, SM['fill'], 1e-9); agree(sef, SM['fillse'], 1e-6)
b2, se2 = irls(X2, y2, 'pois', np.log(t)); agree(b2, SM['d2'], 1e-9); agree(se2, SM['d2se'], 1e-6)
b2n, _ = irls(X2, y2, 'pois'); agree(b2n, SM['d2no'], 1e-9)
blt, selt = irls(np.column_stack([X2, np.log(t)]), y2, 'pois'); agree(blt, SM['logt'], 5e-7); agree(selt, SM['logtse'], 1e-6)
b6, se6, h6 = irls(X6, y6, 'bin', hist=True); agree(b6, SM['six'], 1e-9); agree(se6, SM['sixse'], 5e-6)
b3, se3 = irls(X3, y3, 'pois'); agree(b3, SM['d3'], 1e-9)
b3z, se3z = irls(X3z, y3, 'pois')
mu3 = np.exp(X3 @ b3); mu3z = np.exp(X3z @ b3z)
dev3, dev3z = pdev(y3, mu3), pdev(y3, mu3z); agree([dev3, dev3z], [SM['d3dev'], SM['d3zdev']], 1e-8)
pear3 = np.sum((y3 - mu3) ** 2 / mu3); pear3z = np.sum((y3 - mu3z) ** 2 / mu3z); agree([pear3, pear3z], [SM['d3pear'], SM['d3zpear']], 1e-8)
mu2 = np.exp(X2 @ b2 + np.log(t)); pear2 = np.sum((y2 - mu2) ** 2 / mu2)

# NB2 by profile likelihood over alpha, IRLS for beta at each alpha (independent of statsmodels' optimiser)
def nb_fit(X, alpha):
    b = np.array([np.log(y3.mean())] + [0.0] * (X.shape[1] - 1))
    for _ in range(200):
        eta = X @ b; mu = np.exp(eta); W = mu / (1 + alpha * mu); z = eta + (y3 - mu) / mu
        nb = np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (W * z))
        if np.max(np.abs(nb - b)) < 1e-12:
            b = nb; break
        b = nb
    mu = np.exp(X @ b); r = 1 / alpha
    lg = np.array([math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1) for k in y3])
    return np.sum(lg + r * np.log(r / (r + mu)) + y3 * np.log(mu / (r + mu)))


def golden(fn, a, b):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(120):
        if fn(c) > fn(d):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    return (a + b) / 2


a1 = golden(lambda a: nb_fit(X3, a), 0.1, 2.0); a2 = golden(lambda a: nb_fit(X3z, a), 0.1, 2.0)
llnb1, llnb2 = nb_fit(X3, a1), nb_fit(X3z, a2)
agree(a1, SM['nb_alpha'], 5e-6, 'alpha'); agree([llnb1, llnb2], [SM['nb_llf1'], SM['nb_llf2']], 1e-6, 'nb llf')
lr_nb = 2 * (llnb2 - llnb1)

# penalised (scikit-learn C = 1) Newton
bp = np.zeros(2)
for _ in range(100):
    mu = expit(X1 @ bp); W = mu * (1 - mu)
    g = X1.T @ (y1 - mu) - np.array([0, bp[1]]); Hm = X1.T @ (W[:, None] * X1) + np.diag([0, 1.0])
    bp = bp + np.linalg.solve(Hm, g)
agree(bp, SM['pen'], 5e-7, 'pen')

# IRLS iterates
def iterates(X, y, n, fixedW=False):
    b = np.zeros(X.shape[1]); out = []
    for _ in range(n):
        eta = X @ b; mu = expit(eta); W = np.full(len(y), 0.25) if fixedW else mu * (1 - mu); z = eta + (y - mu) / W
        b = np.linalg.solve(X.T @ (W[:, None] * X), X.T @ (W * z)); out.append(b.copy())
    return out


it6 = iterates(X6, y6, 6); it6f = iterates(X6, y6, 3, True); itd1 = iterates(X1, y1, 7)
devd1 = [bdev(X1, y1, b) for b in itd1]
with np.errstate(all='ignore'):
    itsep = iterates(Xs, ys, 11)
# Poisson IRLS from the start, and the double-offset slip
bpois = np.array([np.log(y2.sum() / t.sum()), 0.0])
eta0 = np.log(15) + bpois[0]; mu0 = np.exp(eta0); zrow = bpois[0] + (41 - mu0) / mu0; zwrong = eta0 + (41 - mu0) / mu0
bw = bpois.copy()
for _ in range(2):
    eta = X2 @ bw + np.log(t); mu = np.exp(eta); z = eta + (y2 - mu) / mu
    bw = np.linalg.solve(X2.T @ (mu[:, None] * X2), X2.T @ (mu * z))
# Poisson(2)
k = np.arange(0, 80); pmf = np.exp(-2 + k * np.log(2) - np.array([math.lgamma(i + 1) for i in k]))
eln = float(np.sum(pmf * np.log(k + 1))); sim = float(np.log(np.random.default_rng(5).poisson(2, 1_000_000) + 1).mean())
agree(eln, sim, 5e-4, 'pois2 sim')

B0, B1 = b1
p = lambda l: expit(B0 + B1 * l)
me = lambda l: B1 * p(l) * (1 - p(l)) * 0.01 * 100      # points per 0.01
F0, F1 = bf
R0, R1 = b2
phi = pear3z / 197
drop = dev3 - dev3z

# ================= l1 =================
f = 'l1'
chk(f, 'screens[0].prose', 300); chk(f, 'screens[0].prose', int(y1.sum()))
for path in ['screens[0].feedback', 'screens[0].explain']:
    chk(f, path, ols[0], 4 if 'feedback' in path else 6); chk(f, path, ols[1], 4 if 'feedback' in path else 6)
chk(f, 'screens[0].explain', ols[0] * 100, 1)
chk(f, 'screens[0].widget', ols[0], 3); chk(f, 'screens[0].widget', ols[0] + ols[1], 3)
chk(f, 'screens[1].prose', ols[0], 6); chk(f, 'screens[1].widget.answer', cross0, 4); chk(f, 'screens[1].widget.wrong[0].value', -ols[0], 4)
chk(f, 'screens[1].widget.wrong[1].value', (1 - ols[0]) / ols[1], 4); chk(f, 'screens[1].explain', out01); chk(f, 'screens[1].explain', 100 * out01 / 300, 1)
chk(f, 'screens[1].explain', (1 - ols[0]) / ols[1], 3); chk(f, 'screens[1].explain', cross0, 4)
chk(f, 'screens[4].widget', 0.2 * 0.8, 2); chk(f, 'screens[4].widget', y3.mean(), 3); chk(f, 'screens[4].explain', y3.mean(), 3)
chk(f, 'screens[5].prose', y3.mean(), 3); chk(f, 'screens[5].prose', y3.var(ddof=1), 3)
chk(f, 'screens[5].widget.answer', y3.var(ddof=1) / y3.mean(), 3); chk(f, 'screens[5].widget.wrong[0].value', y3.mean() / y3.var(ddof=1), 4)
chk(f, 'screens[5].widget.wrong[1].value', math.sqrt(y3.var(ddof=1)) / y3.mean(), 4); chk(f, 'screens[5].feedback', math.sqrt(y3.var(ddof=1)), 3)
chk(f, 'screens[5].explain', y3.var(ddof=1) / y3.mean(), 2); chk(f, 'screens[5].explain', int((y3 == 0).sum()))
chk(f, 'screens[6].explain', math.exp(-2) * 100, 1); chk(f, 'screens[6].explain', eln, 4); chk(f, 'screens[6].explain', math.log(3), 4)
chk(f, 'screens[6].hints', math.exp(-2) * 100, 1); chk(f, 'screens[6].explain', math.exp(-2), 4)
chk(f, 'screens[7].prose', eln, 4); chk(f, 'screens[7].prose', sim, 4); chk(f, 'screens[7].prose', math.log(3), 4)
chk(f, 'screens[7].explain', eln, 4)
pd05 = float(p(0.05)); el = pd05 * 0.45 * 1e6; el_line = (ols[0] + ols[1] * 0.05) * 0.45 * 1e6
chk(f, 'screens[9].prose', el_line, 0); chk(f, 'screens[9].prose', (ols[0] + ols[1] * 0.05) * 100, 1)
chk(f, 'screens[9].widget.answer', el, 0); chk(f, 'screens[9].widget.wrong[0].value', el_line, 0); chk(f, 'screens[9].widget.wrong[1].value', pd05 * 1e6, 0)
chk(f, 'screens[9].widget.accept', pd05 * 100, 4); chk(f, 'screens[9].hints', B0 + B1 * 0.05, 4); chk(f, 'screens[9].hints', pd05, 6)
chk(f, 'screens[9].explain', pd05 * 100, 3); chk(f, 'screens[9].explain', el, 0); chk(f, 'screens[9].explain', el_line, 0)
chk(f, 'screens[9].question', B0, 6); chk(f, 'screens[9].question', B1, 6)
chk(f, 'quiz[2].widget.answer', 0.21, 2); chk(f, 'quiz[3].widget', out01)

# ================= l2 =================
f = 'l2'
chk(f, 'screens[0].feedback', b12[0], 6); chk(f, 'screens[0].feedback', b12[1], 6); chk(f, 'screens[0].explain', ll12(*b12), 6)
chk(f, 'screens[1].prose', ll12(-3, 6), 6); chk(f, 'screens[1].prose', ll12(-4, 8), 6)
chk(f, 'screens[1].widget.answer', ll12(0, 0), 6); agree(ll12(0, 0), 12 * math.log(0.5), 1e-12)
chk(f, 'screens[1].widget.wrong[0].value', math.log(0.5), 4); chk(f, 'screens[1].explain', ll12(*b12) - ll12(0, 0), 2)
chk(f, 'screens[2].widget.answer', -ll12(*b12) / 12, 4)
chk(f, 'screens[3].widget.answer', math.exp(0.1 * B1), 4); chk(f, 'screens[3].widget.wrong[0].value', 0.1 * B1, 4)
chk(f, 'screens[3].widget.wrong[1].value', math.exp(B1), 0); chk(f, 'screens[3].explain', 0.1 * B1, 6)
chk(f, 'screens[4].widget.answer', p(0.5), 4); chk(f, 'screens[4].widget.wrong[0].value', (B0 + B1 * 0.5) / 100, 6)
chk(f, 'screens[4].widget.wrong[1].value', math.exp(B0 + B1 * 0.5), 4); chk(f, 'screens[4].hints', B0 + B1 * 0.5, 6)
chk(f, 'screens[4].feedback', p(0.7) * 100, 2); chk(f, 'screens[4].explain', -B0 / B1, 4); chk(f, 'screens[4].explain', B0 + B1 * 0.5, 4)
chk(f, 'screens[5].widget.answer', me(0.5), 4); chk(f, 'screens[5].widget.wrong[1].value', B1 * 0.25, 2); chk(f, 'screens[5].hints', p(0.5), 4)
chk(f, 'screens[5].hints', me(0.5), 4); chk(f, 'screens[5].hints', me(0.5) / 100, 6)
chk(f, 'screens[6].prose', p(0.2), 4); chk(f, 'screens[6].hints', p(0.2) * (1 - p(0.2)), 4); chk(f, 'screens[6].explain', me(0.2), 2); chk(f, 'screens[6].explain', me(0.5), 2)
chk(f, 'screens[7].prose', B1 / se1[1], 2); chk(f, 'screens[7].widget.answer', B1 - 1.96 * se1[1], 4); chk(f, 'screens[7].widget.wrong[0].value', B1 + 1.96 * se1[1], 4)
chk(f, 'screens[7].widget.wrong[1].value', B1 - se1[1], 4); chk(f, 'screens[7].explain', se12[1], 6); chk(f, 'screens[7].feedback', B1 + 1.96 * se1[1], 3)
chk(f, 'screens[9].widget.tests', bdev(X12, y12, np.array([0.0, 800.0])) / 2, 0)
chk(f, 'screens[9].explain', bdev(X12, y12, np.array([0.0, 800.0])) / 2, 0)
chk(f, 'screens[10].explain', se12[1], 6)
chk(f, 'screens[11].prose', int(fl.sum())); chk(f, 'screens[11].prose', F0, 6); chk(f, 'screens[11].prose', F1, 6)
chk(f, 'screens[11].prose', sef[0], 6); chk(f, 'screens[11].prose', SM['fillse'][1], 6)
chk(f, 'screens[11].widget.answer', expit(F0 + 2 * F1), 4); chk(f, 'screens[11].feedback', expit(F0) * 100, 2)
chk(f, 'screens[11].explain', math.exp(F1), 4); chk(f, 'screens[11].hints', F0 + 2 * F1, 6)
chk(f, 'quiz[0].widget.answer', -B0 / B1, 4); chk(f, 'quiz[0].widget.wrong[0].value', -B1 / B0, 4)
chk(f, 'quiz[1].explain', bp[1], 2); chk(f, 'quiz[1].widget', bp[0], 6); chk(f, 'quiz[1].widget', bp[1], 6)
chk(f, 'quiz[2].widget', b12[1] / se12[1], 2); chk(f, 'quiz[2].feedback', 2 * norm_sf(b12[1] / se12[1]), 2)

# ================= l3 =================
f = 'l3'
chk(f, 'screens[1].prose', R0, 6); chk(f, 'screens[1].prose', R1, 6); chk(f, 'screens[1].widget.answer', math.exp(10 * R1), 4)
chk(f, 'screens[1].widget.wrong[1].value', math.exp(R1), 4); chk(f, 'screens[1].explain', math.exp(10 * R1), 4)
chk(f, 'screens[2].widget.answer', 15 * math.exp(R0 + 20 * R1), 2); chk(f, 'screens[2].widget.wrong[0].value', math.exp(R0 + 20 * R1), 3)
chk(f, 'screens[2].widget.wrong[1].value', 60 * math.exp(R0 + 20 * R1), 2); chk(f, 'screens[2].explain', math.exp(R0 + 20 * R1), 4)
chk(f, 'screens[2].hints', R0 + 20 * R1, 6)
chk(f, 'screens[3].explain', int(y2.sum()))
chk(f, 'screens[4].prose', blt[2], 6); chk(f, 'screens[4].prose', selt[2], 6); chk(f, 'screens[4].widget.answer', (blt[2] - 1) / selt[2], 4)
chk(f, 'screens[4].widget.wrong[0].value', SM['logt'][2] / SM['logtse'][2], 3)
chk(f, 'screens[5].prose', b2n[1], 6); chk(f, 'screens[5].prose', math.exp(10 * b2n[1]), 4); chk(f, 'screens[5].explain', math.exp(10 * R1), 4)
chk(f, 'screens[6].widget.answer', -5 * math.exp(R0 + 20 * R1), 4); chk(f, 'screens[6].explain', -5 * math.exp(R0 + 20 * R1), 2)
chk(f, 'screens[7].widget.wrong[0].value', math.sqrt(12), 4)
chk(f, 'screens[8].widget.tests', float(np.sum(np.exp(np.log(t)) - y2 * np.log(t))), 9)
chk(f, 'screens[8].widget.tests', float(np.sum(np.exp(np.full(120, 0.1)) - y2 * 0.1)), 9); chk(f, 'screens[8].explain', int(t.sum()))
chk(f, 'screens[9].explain', R1, 6); chk(f, 'screens[9].explain', se2[1], 6)
chk(f, 'screens[10].widget.answer', 15 * math.exp(R0 + 30 * R1), 2); chk(f, 'screens[10].explain', math.exp(R0 + 30 * R1), 4); chk(f, 'screens[10].hints', R0 + 30 * R1, 6)
chk(f, 'quiz[0].widget.answer', math.log(30), 4); chk(f, 'quiz[0].widget.wrong[1].value', math.log10(30), 4)
chk(f, 'quiz[1].widget', math.exp(-0.05), 3); chk(f, 'quiz[1].explain', 100 * (1 - math.exp(-0.05)), 2)

# ================= l4 =================
f = 'l4'
chk(f, 'screens[1].widget.answer', it6[0][1], 1); chk(f, 'screens[1].feedback', it6[0][0])
cx = np.sum((x6 - x6.mean()) * np.where(y6 > 0, 2, -2)); chk(f, 'screens[1].widget.accept', cx); chk(f, 'screens[1].widget.accept', np.sum((x6 - 2.5) ** 2), 1)
chk(f, 'screens[1].widget.wrong[0].value', np.linalg.lstsq(X6, y6, rcond=None)[0][1], 1)
for kk in range(1, 5):
    chk(f, 'screens[2].canvas', it6[kk][0], 6); chk(f, 'screens[2].canvas', it6[kk][1], 6)
for kk, b in enumerate(it6[:5]):
    chk(f, 'screens[2].canvas', bdev(X6, y6, b), 6)
chk(f, 'screens[2].prose', bdev(X6, y6, b6), 6); chk(f, 'screens[2].prose', b6[0], 6)
w0 = expit(-2) * (1 - expit(-2)); chk(f, 'screens[2].widget.answer', w0, 3); chk(f, 'screens[2].widget.accept', expit(-2), 4)
mu6 = expit(X6 @ b6); A = X6.T @ ((mu6 * (1 - mu6))[:, None] * X6)
chk(f, 'screens[3].canvas', A[0, 0], 6); chk(f, 'screens[3].canvas', A[0, 1], 6); chk(f, 'screens[3].canvas', A[1, 1], 6)
chk(f, 'screens[3].widget.answer', se6[1], 4); chk(f, 'screens[3].hints', np.linalg.det(np.round(A, 6)), 6); chk(f, 'screens[3].widget.wrong[0].value', 1 / math.sqrt(A[1, 1]), 4)
chk(f, 'screens[3].explain', SM['sixse'][0], 6); chk(f, 'screens[3].explain', SM['sixse'][1], 6); chk(f, 'screens[3].explain', np.linalg.inv(A)[1, 1], 5)
chk(f, 'screens[4].widget', it6f[1][0], 6); chk(f, 'screens[4].widget', it6[1][1], 6)
for b in itd1[:6]:
    chk(f, 'screens[5].canvas', b[0], 6); chk(f, 'screens[5].canvas', b[1], 6)
for d_ in devd1[:6]:
    chk(f, 'screens[5].prose', d_, 3)
agree(round(devd1[4] - devd1[5], 10), 1.85e-9, 1e-10, 'dev change 6')
chk(f, 'screens[6].canvas', it6f[1][0], 6); chk(f, 'screens[6].canvas', it6f[2][1], 6); chk(f, 'screens[6].prose', it6[1][0], 6); chk(f, 'screens[6].explain', it6f[1][1], 6)
chk(f, 'screens[7].prose', bpois[0], 6); chk(f, 'screens[7].canvas', eta0, 6); chk(f, 'screens[7].canvas', mu0, 3)
chk(f, 'screens[7].widget.answer', zrow, 4); chk(f, 'screens[7].widget.wrong[0].value', zwrong, 4); chk(f, 'screens[7].widget.wrong[1].value', (41 - mu0) / mu0, 4)
chk(f, 'screens[7].feedback', pdev(y2, mu2), 6); chk(f, 'screens[7].explain', bw[0], 6); chk(f, 'screens[7].explain', bw[1], 6)
for kk in (0, 2, 4, 9):
    chk(f, 'screens[8].canvas', itsep[kk][1], 4)
chk(f, 'screens[8].explain', itsep[9][1], 4); chk(f, 'screens[8].explain', SM['sep'][1], 2)
agree(np.isnan(itsep[10]).all(), True, 0, 'sep nan at 11')
chk(f, 'screens[9].widget.tests', SM['six'][0])
chk(f, 'quiz[0].widget.answer', expit(1) * (1 - expit(1)), 4); chk(f, 'quiz[1].widget.answer', math.log(4) + 0.5, 4)

# ================= l5 =================
f = 'l5'
chk(f, 'screens[0].widget.answer', 200 * math.exp(-y3.mean()), 3); chk(f, 'screens[0].widget.wrong[0].value', math.exp(-y3.mean()), 4)
dsm = 2 * ((2 * math.log(2 / 3) + 1) + 1 + (5 * math.log(5 / 4) - 1))
chk(f, 'screens[1].widget.answer', dsm, 4); chk(f, 'screens[1].widget.wrong[0].value', dsm / 2, 4); chk(f, 'screens[1].widget.wrong[1].value', dsm - 2, 4)
chk(f, 'screens[2].prose', b3[0], 6); chk(f, 'screens[2].prose', b3[1], 6); chk(f, 'screens[2].prose', dev3, 3); chk(f, 'screens[2].prose', pear3, 3)
chk(f, 'screens[2].widget.answer', pear3 / 198, 3); chk(f, 'screens[2].widget.wrong[0].value', dev3 / 198, 4); chk(f, 'screens[2].widget.wrong[1].value', pear3 / 200, 4)
chk(f, 'screens[3].prose', drop, 3); chk(f, 'screens[3].widget.answer', chi2_sf(drop, 1), 4); chk(f, 'screens[3].explain', SM['d3zp'], 4)
chk(f, 'screens[4].prose', phi, 3); chk(f, 'screens[4].widget.answer', drop / phi, 3); chk(f, 'screens[4].feedback', f_sf(drop / phi, 1, 197), 3)
chk(f, 'screens[4].explain', math.sqrt(phi), 2); chk(f, 'screens[4].explain', -2.344 / math.sqrt(phi), 2)
chk(f, 'screens[5].widget', b3[1], 4); chk(f, 'screens[5].widget', b3z[1], 4)
chk(f, 'screens[6].prose', SM['nb_alpha'], 4); chk(f, 'screens[6].widget.answer', y3.mean() + a1 * y3.mean() ** 2, 2); chk(f, 'screens[6].explain', lr_nb, 3)
chk(f, 'screens[6].explain', chi2_sf(lr_nb, 1), 3)
ll1 = -bdev(X1, y1, b1) / 2
chk(f, 'screens[8].prose', ll1, 5); chk(f, 'screens[8].widget.answer', -2 * ll1, 3); chk(f, 'screens[8].explain', -2 * ll1 / 298, 3)
size = 2 * norm_sf(1.96 / math.sqrt(phi))
chk(f, 'screens[10].prose', math.sqrt(phi), 3); chk(f, 'screens[10].prose', 1.96 / math.sqrt(phi), 3)
chk(f, 'screens[10].widget.answer', 20 * size, 3); chk(f, 'screens[10].widget.accept', size, 4); chk(f, 'screens[10].explain', 100 * size, 1)
chk(f, 'quiz[1].widget.answer', chi2_sf(6, 2), 4)

# ================= review and homework =================
f = 'review'
chk(f, 'items[1].widget.answer', math.exp(0.35), 4); chk(f, 'items[1].widget.wrong[1].value', expit(0.35), 4)
zr = -1 + (1 - expit(-1)) / (expit(-1) * (1 - expit(-1))); chk(f, 'items[3].widget.answer', zr, 4); agree(zr, math.e, 1e-12)
chk(f, 'items[4].widget.answer', chi2_sf(3.2, 1), 4); chk(f, 'items[6].widget.answer', 0.42, 2)
f = 'homework'
chk(f, 'items[0].widget.tests', SM['d2'][1])
chk(f, 'items[3].widget.answer', 9.6 / (768 / 240), 1); chk(f, 'items[3].feedback', f_sf(3.0, 1, 240), 3); chk(f, 'items[3].explain', chi2_sf(9.6, 1), 3)
chk(f, 'items[4].widget.answer', 100 * (expit(F0 + F1) - expit(F0 + 2 * F1)), 2); chk(f, 'items[4].explain', F0 + F1, 6)
chk(f, 'items[4].explain', 100 * (expit(F0 + 4 * F1) - expit(F0 + 5 * F1)), 2)
chk(f, 'items[5].widget.answer', 60 * math.exp(R0 + 15 * R1), 2); chk(f, 'items[5].explain', math.log(60) + R0 + 15 * R1, 6)
chk(f, 'items[7].widget.answer', chi2_sf(lr_nb, 1), 4); chk(f, 'items[7].widget.wrong[0].value', chi2_sf(lr_nb / 2, 1), 4)
chk(f, 'items[2].model', pear2 / 118, 2); chk(f, 'items[2].model', math.exp(10 * (R1 - 1.96 * se2[1])), 2); chk(f, 'items[2].model', math.exp(10 * (R1 + 1.96 * se2[1])), 2)
print('D2 Pearson', round(pear2, 3), 'NB alpha', round(a1, 6), 'LR', round(lr_nb, 4))
lv.report()
