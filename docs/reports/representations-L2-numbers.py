"""representations level 2 (Autoencoders): every stated number recomputed by a second route.

Route A is the generator (NumPy, the autograd, nt_ops_l1.adam_step). Route B here is independent: closed forms
(2 x 2 eigenvalues by the quadratic formula, Fractions, the half-circle integrals by numerical quadrature), SVDs in
place of eigendecompositions, and every training run repeated with a hand-written gradient and a hand-written Adam
instead of the autograd and nt_ops_l1. The two shipped weight files are retrained here and compared. Every code
widget's hidden tests are rerun in CPython with the model solution and with an independent twin. Run through
`node tools/run-number-scripts.mjs --only representations-L2` (one BLAS thread); strict coverage.
"""
import json, math, os, sys, hashlib
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from numbers_lib import Level, ZQ_LIB
from autograd import Tensor
import representations_ops_l1 as ops1
import representations_ops_l2 as ops

lv = Level("representations", 2, coverage="strict")
F = lv.files


def given(vals, why):
    """Numbers stated as data in a prompt or scenario: covered as literals with the reason."""
    for v in vals:
        lv.literal(str(v), why=why)


def sha(name):
    return hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest()


lv.claim(sha('autograd.py').startswith('5917d4ec91f7'), 'autograd.py byte-identical to the frozen v1.0')
lv.claim(sha('nt_ops_l1.py').startswith('9c1391a33624'), 'nt_ops_l1.py byte-identical to the merged v1.0')
lv.claim(sha('representations_ops_l1.py').startswith('097ac4d78867'), 'representations_ops_l1.py unchanged')


# ------------------------------------------------------------------ route B tools
def adam_b(p, g, st, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m, v = st
    m[:] = b1 * m + (1 - b1) * g
    v[:] = b2 * v + (1 - b2) * g * g
    return p - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)


def lin_b(X, k, steps, lr, We, Wd, centre=True, trace=False):
    """Linear autoencoder by hand gradient and hand Adam from given starts."""
    X = np.asarray(X, float)
    if centre:
        X = X - X.mean(0)
    n = len(X)
    We, Wd = We.copy(), Wd.copy()
    sts = [(np.zeros_like(We), np.zeros_like(We)), (np.zeros_like(Wd), np.zeros_like(Wd))]
    tr = []
    for t in range(1, steps + 1):
        Z = X @ We
        E = Z @ Wd - X
        tr.append(float((E ** 2).sum() / n))
        gWd = 2 / n * Z.T @ E
        gWe = 2 / n * X.T @ (E @ Wd.T)
        We = adam_b(We, gWe, sts[0], t, lr)
        Wd = adam_b(Wd, gWd, sts[1], t, lr)
    E = X @ We @ Wd - X
    tr.append(float((E ** 2).sum(1).mean()))
    return (We, Wd, tr) if trace else (We, Wd)


def lin_seeded(X, k, steps, lr, seed, trace=False):
    X = np.asarray(X, float)
    d = X.shape[1]
    g = np.random.default_rng(seed)
    We = 0.1 * g.standard_normal((d, k))
    Wd = 0.1 * g.standard_normal((k, d))
    return lin_b(X, k, steps, lr, We, Wd, trace=trace)


def tanh_fwd(P, X):
    W1, b1, W2, b2, W3, b3, W4, b4 = P
    h1 = np.tanh(X @ W1 + b1)
    z = h1 @ W2 + b2
    h2 = np.tanh(z @ W3 + b3)
    return h1, z, h2, h2 @ W4 + b4


def tanh_init_b(d, h, k, seed):
    g = np.random.default_rng(seed)
    P = []
    for fi, fo in ((d, h), (h, k), (k, h), (h, d)):
        P.append(g.standard_normal((fi, fo)) / math.sqrt(fi))
        P.append(np.zeros(fo))
    return P


def tanh_b(X, h, k, steps, lr, seed):
    X = np.asarray(X, float)
    n = len(X)
    P = tanh_init_b(X.shape[1], h, k, seed)
    sts = [(np.zeros_like(p), np.zeros_like(p)) for p in P]
    for t in range(1, steps + 1):
        W1, b1, W2, b2, W3, b3, W4, b4 = P
        h1, z, h2, Xh = tanh_fwd(P, X)
        dX = 2 * (Xh - X) / n
        gW4, gb4 = h2.T @ dX, dX.sum(0)
        da2 = (dX @ W4.T) * (1 - h2 ** 2)
        gW3, gb3 = z.T @ da2, da2.sum(0)
        dz = da2 @ W3.T
        gW2, gb2 = h1.T @ dz, dz.sum(0)
        da1 = (dz @ W2.T) * (1 - h1 ** 2)
        gW1, gb1 = X.T @ da1, da1.sum(0)
        G = [gW1, gb1, gW2, gb2, gW3, gb3, gW4, gb4]
        P = [adam_b(p, gg, st, t, lr) for p, gg, st in zip(P, G, sts)]
    return P


def tanh_err(P, X):
    X = np.asarray(X, float)
    return float(((tanh_fwd(P, X)[3] - X) ** 2).sum(1).mean())


def pca_svd(X, k, Xte=None):
    """Held-out (or training) error of the top-k PCA rebuild, by SVD of the centred training rows."""
    X = np.asarray(X, float)
    mu = X.mean(0)
    _, _, Vt = np.linalg.svd(X - mu, full_matrices=False)
    V = Vt[:k].T
    T = (np.asarray(Xte, float) if Xte is not None else X) - mu
    return float(((T - T @ V @ V.T) ** 2).sum(1).mean())


def eig2(a, b, c):
    """Eigenvalues of [[a, b], [b, c]] by the quadratic formula, larger first."""
    tr, det = a + c, a * c - b * b
    s = math.sqrt(tr * tr / 4 - det)
    return tr / 2 + s, tr / 2 - s


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


# ------------------------------------------------------------------ the module: gradient check and data recipes
Pg = [Tensor(p + 0.1 * np.random.default_rng(9).standard_normal(p.shape)) for p in ops.init_tanh_ae(2, 5, 1, 3)]
Xg = ops.arc(12, 0.05, 2)
from autograd import grad_check
gerr = grad_check(lambda: ((ops.tanh_ae_forward(Pg, Xg) - Xg) ** 2).sum() / len(Xg), Pg)
lv.claim(gerr < 1e-6, f'tanh_ae_forward through the autograd: gradient check against central differences, relative error {gerr:.1e}')
Ph = [p.data for p in Pg]
h1, z, h2, Xh = tanh_fwd(Ph, Xg)
lv.claim(np.allclose(Xh, ops.tanh_ae_forward(Ph, Xg), atol=1e-14) and np.allclose(z, ops.tanh_ae_encode(Ph, Xg), atol=1e-14), 'module forward and encode equal a hand forward on arrays')
g0 = np.random.default_rng(0); t0 = g0.uniform(0, np.pi, 5); A0 = np.c_[np.cos(t0), np.sin(t0)] + 0.05 * g0.standard_normal((5, 2))
lv.claim(np.array_equal(A0, ops.arc(5, 0.05, 0)), 'arc: angles then noise from one generator, as documented')
R3, kind3 = ops.odd_day_panel(3)
Rr, kr = ops.odd_day_panel(3, regime=True)
lv.claim(R3.shape == (750, 10) and list(np.where(kind3 == 1)[0]) == list(ops.ODD_DAYS) and int(np.where(kind3 == 2)[0][0]) == 700, 'odd_day_panel(3): 750 days, 8 odd days, a fall on day 700')
lv.claim(np.array_equal(R3[:650], Rr[:650]), 'the regime switch leaves the first 650 days unchanged')
lv.claim(abs(R3[700].mean() + 6 * 1.0) < 2, 'day 700: a market move of -6')

# ------------------------------------------------------------------ l5
P8 = [(2.0, 1.4), (-1.6, -0.8), (0.6, 1.0), (-2.4, -2.0), (1.2, 0.2), (-0.4, 0.6), (3.0, 1.8), (-2.4, -2.2)]
l5 = F['l5-squeeze-and-rebuild']
pts = [(p['x'], p['y']) for p in l5['screens'][0]['canvas']['state']['points'][:8]]
lv.claim(pts == P8 and abs(sum(a for a, _ in P8)) < 1e-12 and abs(sum(b for _, b in P8)) < 1e-12, 'l5 hook: eight demeaned days as shown')
sxx = sum(Fr(str(a)) ** 2 for a, _ in P8); syy = sum(Fr(str(b)) ** 2 for _, b in P8); sxy = sum(Fr(str(a)) * Fr(str(b)) for a, b in P8)
big, small = eig2(float(sxx), float(sxy), float(syy))
TOT = float(sxx + syy)
lv.expect('l5', 'screens[0]', round(small, 2), fmt='{:.2f}')
lv.expect('l5', 'screens[0].explain.text', round(TOT, 2), fmt='{:.2f}')
lv.expect('l5', 'screens[0].feedback.byKey.axis', float(syy), fmt='{:.2f}')
lv.claim(close(TOT - float(sxx), float(syy)), 'flat line: total miss is the sum of squares of B, 16.08')
vx = float(sxy) / math.hypot(float(sxy), big - float(sxx)); vy = (big - float(sxx)) / math.hypot(float(sxy), big - float(sxx))
D_T = l5['screens'][0]['widget']['points'][0]['target']
lv.claim(abs(D_T[0] - 3 * vx) < 1e-3 and abs(D_T[1] - 3 * vy) < 1e-3, 'drag target is 3 times PC1 of the eight days')
lv.claim(l5['screens'][0]['canvas']['derive']['caption'].count(f'{float(sxx):.2f}') == 1 and f'{2 * float(sxy):.2f}' in l5['screens'][0]['canvas']['derive']['caption'], 'caption formula uses the sums 29.04 and 2 x 20.16', covers=[float(sxx), 2 * float(sxy), float(syy)])
z1 = Fr('0.8') * 2 + Fr('0.6') * Fr('1.4')
xh = (z1 * Fr('0.8'), z1 * Fr('0.6'))
lv.expect('l5', 'screens[1].widget.rows[0][1].answer', float(z1))
lv.expect('l5', 'screens[1].widget.rows[1][1].answer', float(xh[0]))
lv.expect('l5', 'screens[1].widget.rows[2][1].answer', float(xh[1]))
lv.expect('l5', 'screens[1].explain.text', round(math.hypot(2 - float(xh[0]), 1.4 - float(xh[1])), 2), fmt='{:.2f}')
lv.claim(2 + 1.4 == 3.4, 'slip: adding the returns gives 3.4', covers=[3.4, 1.6, 0.84])
X3 = [(2, 1), (-1, -1), (Fr(1, 2), -1)]
zs = [Fr('0.8') * a + Fr('0.6') * b for a, b in X3]
res = [Fr(a) ** 2 + Fr(b) ** 2 - z * z for (a, b), z in zip(X3, zs)]
lv.claim([float(z) for z in zs] == [2.2, -1.4, -0.2] and [float(x) for x in res] == [0.16, 0.04, 1.21], 'three days: codes 2.2, -1.4, -0.2 and misses 0.16, 0.04, 1.21', covers=[2.2, 1.4, 0.2, 0.16, 0.04, 1.21, 5])
mse3 = float(sum(res) / 3)
lv.expect('l5', 'screens[2].widget.answer', round(mse3, 4))
lv.expect('l5', 'screens[2].widget.wrong[0].value', float(sum(res)))
lv.expect('l5', 'screens[2].widget.wrong[1].value', round(sum(math.sqrt(float(x)) for x in res) / 3, 4))
lv.expect('l5', 'screens[2].feedback.byKey.sum', float(sum(res)), fmt='{:.2f}')
# five-stock panel by SVD
LAM5 = [3, 1, 0.5, 0.3, 0.2]
Q5 = np.linalg.qr(np.random.default_rng(5).standard_normal((5, 5)))[0]
X5 = np.random.default_rng(6).standard_normal((2000, 5)) @ np.diag(np.sqrt(LAM5)) @ Q5.T
sv = np.linalg.svd(X5 - X5.mean(0), compute_uv=False) ** 2 / 2000
errs5 = [float(sv[k:].sum()) for k in range(6)]
bars5 = l5['screens'][3]['canvas']['state']['values']
lv.claim(all(abs(bars5[f'k{k}'] - round(errs5[k], 4)) < 1e-9 for k in range(6)), 'l5 bars: PCA errors by SVD for k = 0..5', covers=[round(e, 2) for e in errs5])
share2 = errs5[2] / errs5[0]
lv.expect('l5', 'screens[3].widget.answer', round(share2, 2))
lv.expect('l5', 'screens[3].widget.wrong[0].value', round(1 - share2, 2))
lv.expect('l5', 'screens[3].widget.wrong[1].value', round(errs5[1] / errs5[0], 2))
lv.expect('l5', 'screens[3].feedback.correct', round(errs5[2], 2), fmt='{:.2f}')
lv.expect('l5', 'screens[3].feedback.correct', round(100 * share2), fmt='{:.0f}')
lv.claim(X5.shape == (2000, 5), 'five stocks, 2,000 days', covers=[2000])
We5, Wd5, tr5 = lin_seeded(X5, 2, 300, 0.05, 0, trace=True)
lv.claim(max(abs(a - b) for a, b in zip([r for r in l5['screens'][4]['canvas']['params']['series'][0]['values']], [round(x, 4) for x in tr5[::5]])) < 2e-4, 'l5 training curve: hand Adam reproduces the plotted errors every 5th step', covers=[0.05, 300])
lv.expect('l5', 'screens[4].widget.answer', round(tr5[-1], 2))
lv.expect('l5', 'screens[4].widget.wrong[0].value', round(errs5[1], 2))
lv.expect('l5', 'screens[4].widget.wrong[1].value', round(tr5[0], 2))
lv.claim(abs(tr5[-1] - errs5[2]) < 1e-6, f'trained 2-code error {tr5[-1]:.6f} equals the PCA bar {errs5[2]:.6f}')
R7, sec7 = ops1.factor_returns(7)
sv7 = np.linalg.svd(100 * (R7 - R7.mean(0)), compute_uv=False) ** 2
share3 = float(sv7[:3].sum() / sv7.sum())
lv.expect('l5', 'screens[10].prose', round(100 * share3), fmt='{:.0f}')
lv.expect('l5', 'screens[10].prose', 500 * 30)
lv.expect('l5', 'screens[10].prose', 500 * 3 + 3 * 30)
lv.claim(all(abs(l5['screens'][10]['canvas']['state']['values'][f'c{i + 1}'] - round(sv7[i] / sv7.sum(), 4)) < 1e-9 for i in range(8)), 'transfer bars: variance shares by SVD')
lv.claim(R7.shape == (500, 30), '500 days, 30 stocks', covers=[500, 30])
lv.claim(close(Fr(5) - Fr('2.2') ** 2, Fr('0.16')) and Fr('0.6') + Fr('1.6') == Fr('2.2'), 'quiz: code 2.2, miss 0.16, distance 0.4', covers=[0.16, 2.2, 0.4, 4.84, 1.6])
given([0.6], 'l5 quiz scenario: the 3-code error 0.6 is given')

# ------------------------------------------------------------------ l6
l6 = F['l6-linear-autoencoder-is-pca']
lam1, lam2 = eig2(5, 2, 2)
lv.claim(close(lam1, 6) and close(lam2, 1), 'eigen l11: eigenvalues 6 and 1', covers=[6, 1, 7])
lv.expect('l6', 'screens[2].widget.answer', round(6 / 7, 4))
lv.expect('l6', 'screens[2].feedback.correct', round(600 / 7, 1))
lv.expect('l6', 'screens[2].widget.wrong[1].value', round(1 / 6, 4))
lv.expect('l6', 'screens[2].widget.wrong[0].value', round(1 / 7, 4))
L6 = np.linalg.cholesky(np.array([[5, 2], [2, 2.]]))
X6 = np.random.default_rng(0).standard_normal((2000, 2)) @ L6.T
X6c = X6 - X6.mean(0)
c = X6c.T @ X6c / 2000
sb, ss = eig2(c[0, 0], c[0, 1], c[1, 1])
We6, Wd6, tr6 = lin_seeded(X6, 1, 300, 0.05, 0, trace=True)
lv.expect('l6', 'screens[1].prose', round(tr6[-1], 4), fmt='{:.4f}')
lv.expect('l6', 'screens[1].prose', round(sb, 4), fmt='{:.4f}')
lv.expect('l6', 'screens[1].prose', round(ss, 4), fmt='{:.4f}')
lv.claim(abs(tr6[-1] - ss) < 1e-9, f'trained error equals the sample smaller eigenvalue to 1e-9 ({tr6[-1]:.10f} against {ss:.10f})')
lv.claim(max(abs(a - round(b, 4)) for a, b in zip(l6['screens'][1]['canvas']['params']['series'][0]['values'], tr6[::5])) < 2e-4, 'l6 curve reproduced by hand Adam')
wdir = We6[:, 0] / np.linalg.norm(We6[:, 0]) * np.sign(We6[0, 0])
pc1 = np.array([2, 1]) / math.sqrt(5)
v1s = np.array([c[0, 1], sb - c[0, 0]]); v1s /= np.linalg.norm(v1s)
ang = math.degrees(math.acos(min(1.0, abs(float(wdir @ v1s)))))
lv.expect('l6', 'screens[0].explain.text', round(float(wdir[0]), 3), fmt='{:.3f}')
lv.expect('l6', 'screens[0].explain.text', round(float(wdir[1]), 3), fmt='{:.3f}')
lv.claim(ang < 1e-3, f'trained direction within 0.001 degrees of the sample PC1 ({ang:.2e})', covers=[0.001])
lv.expect('l6', 'screens[0].explain.text', round(float(pc1[0]), 3), fmt='{:.3f}')
lv.expect('l6', 'screens[0].explain.text', round(float(pc1[1]), 3), fmt='{:.3f}')
lv.claim(abs(3 * pc1[0] - 2.683) < 1e-3 and abs(3 * pc1[1] - 1.342) < 1e-3, 'PC1 at radius 3 is (2.68, 1.34)', covers=[2.68, 1.34])
lv.claim(np.allclose(np.diag([[5, 2], [2, 2]]), [5, 2]), 'eigen l11 variances 5 and 2 are the diagonal of Sigma', covers=[5, 2])


def run_start_b(se, sd):
    g = np.random.default_rng(0)
    A = se * g.standard_normal((2, 1)); B = sd * g.standard_normal((1, 2))
    A, B = lin_b(X6c, 1, 300, 0.05, A, B, centre=False)
    E = X6c @ A @ B - X6c
    return A[:, 0], B[0], float((E ** 2).sum(1).mean())


ra, rb = run_start_b(1.5, 0.1), run_start_b(0.1, 1.5)
for vec in (ra[0], ra[1], rb[0], rb[1]):
    for x in vec:
        lv.expect('l6', 'screens[4].prose', round(float(x), 2), fmt='{:.2f}')
lv.expect('l6', 'screens[4].prose', round(ra[2], 4), fmt='{:.4f}')
lv.claim(abs(ra[2] - rb[2]) < 1e-9, 'runs A and B reach the same error')
na, nb = [float(np.linalg.norm(x)) for x in ra[:2]], [float(np.linalg.norm(x)) for x in rb[:2]]
lv.expect('l6', 'screens[4].widget.options[1].why', round(nb[0], 2), fmt='{:.2f}')
lv.expect('l6', 'screens[4].widget.options[1].why', round(nb[1], 2), fmt='{:.2f}')
lv.expect('l6', 'screens[4].explain.text', round(na[0] * na[1], 2), fmt='{:.2f}')
lv.expect('l6', 'screens[4].explain.text', round(nb[0] * nb[1], 2), fmt='{:.2f}')
lv.claim(abs(float(ra[0] @ np.array([-v1s[1], v1s[0]]))) < 1e-4 and abs(float(rb[0] @ np.array([-v1s[1], v1s[0]]))) < 1e-4, 'both encoders lie along the sample PC1')
A = np.array([[Fr(2), Fr(0)], [Fr(1), Fr(1)]]); Ai = np.array([[Fr(1, 2), Fr(0)], [Fr(-1, 2), Fr(1)]])
lv.claim(all((A @ Ai)[i, j] == (1 if i == j else 0) for i in range(2) for j in range(2)), 'A times its stated inverse is I', covers=[0.5, 0.5])
edge = []
for s in (1, 2, 3):
    Xe = np.random.default_rng(s).standard_normal((2000, 2)) * math.sqrt(2)
    Ae, Be, tre = lin_seeded(Xe, 1, 300, 0.05, 0, trace=True)
    edge.append((round(math.degrees(math.atan2(Ae[1, 0], Ae[0, 0])) % 180), tre[-1]))
for a_, e_ in edge:
    lv.expect('l6', 'screens[6].prose', a_)
    lv.expect('l6', 'screens[6].explain.text', round(e_, 3), fmt='{:.3f}')
lv.claim(all(abs(e_ - 2) < 0.1 for _, e_ in edge), 'every 2I run has error near 2')
lv.claim(Fr(2) + Fr(1, 2) == Fr(5, 2), 'three stocks: one code 2.5, two codes 0.5', covers=[2.5, 0.5, 5, 7])
E11 = [(1.9, 1.2), (-3.3, -1.9), (-0.1, -1.3), (-0.7, 0.9), (0.3, 0.9), (0.7, 1.6), (-2.4, -1.7), (-2.2, -1.1), (1.9, 1.7), (3.9, -0.3)]
s11 = [sum(Fr(str(a)) ** 2 for a, _ in E11), sum(Fr(str(a)) * Fr(str(b)) for a, b in E11), sum(Fr(str(b)) ** 2 for _, b in E11)]
lv.claim(s11 == [45, 18, 18], 'eigen l11 sums 45, 18, 18', covers=[45, 18])
_, e11small = eig2(45 / 10, 18 / 10, 18 / 10)
lv.claim(close(e11small, 0.9), 'ten days with n: smaller eigenvalue 9/10 = 0.9', covers=[0.9, 9, 10])
lv.claim(Fr(3) + Fr(3, 2) + Fr(2, 5) + Fr(1, 10) == 5 and Fr(2, 5) + Fr(1, 10) == Fr(1, 2), 'quiz q-eig: 0.5, kept 4.5, one code 2.0', covers=[0.5, 4.5, 2.0, 3, 1.5, 0.4, 0.1])
lv.claim(Fr(8, 10) == Fr(4, 5), 'quiz q-share: 80% of 10, error 2', covers=[0.8, 0.2, 4.0, 8, 10, 2])
lv.literal('300', why='the number of stocks in the l6 transfer scenario is given')

# ------------------------------------------------------------------ l7
l7 = F['l7-a-curved-bottleneck']
from scipy.integrate import quad
Es = quad(lambda t: math.sin(t) / math.pi, 0, math.pi)[0]
Es2 = quad(lambda t: math.sin(t) ** 2 / math.pi, 0, math.pi)[0]
closed = Es2 - Es ** 2
lv.claim(abs(closed - (0.5 - 4 / math.pi ** 2)) < 1e-12, 'quadrature agrees with 1/2 - 4/pi^2')
lv.expect('l7', 'screens[2].widget.answer', round(closed, 4))
lv.expect('l7', 'screens[2].explain.text', round(closed + 0.05 ** 2, 4), fmt='{:.4f}')
lv.expect('l7', 'screens[2].widget.wrong[1].value', round(Es, 4))
lv.claim(abs(Es2 - 0.5) < 1e-12, 'E[sin^2 t] = 0.5 by quadrature', covers=[0.5])
given([0.05, 4], 'the noise level 0.05 and the 4 of 4/pi^2 are stated parameters of arc and the formula')
Xtr, Xte = ops.arc(200, 0.05, 0), ops.arc(200, 0.05, 1)
pca_tr, pca_te = pca_svd(Xtr, 1), pca_svd(Xtr, 1, Xte)
Pfile = [np.array(a) for a in json.load(open(os.path.join(DATA, 'representations-l7-ae.json')))['params']]
Pb = tanh_b(Xtr, 16, 1, 1000, 0.01, 0)
lv.claim(max(float(np.abs(a - b).max()) for a, b in zip(Pfile, Pb)) < 1e-5, 'representations-l7-ae.json: retrained by hand backprop and hand Adam, every weight within 1e-5', covers=[16, 1000, 0.01])
net_tr, net_te = tanh_err(Pfile, Xtr), tanh_err(Pfile, Xte)
for v, f_ in ((pca_tr, '{:.3f}'), (pca_tr, '{:.4f}'), (pca_te, '{:.4f}'), (net_tr, '{:.4f}'), (net_te, '{:.4f}')):
    lv.expect('l7', 'screens', round(v, int(f_[3])), fmt=f_)
lv.claim(close(pca_tr, float(l7['screens'][4]['canvas']['params']['rows'][0][1]), 1e-3), 'held-out table values')
share = net_te / pca_te
lv.expect('l7', 'screens[4].widget.answer', round(share, 4))
lv.expect('l7', 'screens[4].widget.wrong[0].value', round(net_tr / pca_tr, 4))
lv.expect('l7', 'screens[4].widget.wrong[1].value', round(1 - share, 4))
lv.expect('l7', 'screens[4].feedback.correct', round(100 * share, 1))
lv.expect('l7', 'screens[1].widget.options', round(pca_tr / net_tr))
lv.claim(round(pca_tr / net_tr) == 35, 'PCA error about 35 times the net\'s', covers=[35])
mu = Xtr.mean(0)
lv.expect('l7', 'screens[0]', round(float(mu[1]), 2), fmt='{:.2f}')
Zb = tanh_fwd(Pfile, Xtr)[1][:, 0]
th = np.arctan2(Xtr[:, 1], Xtr[:, 0])
rz = np.argsort(np.argsort(Zb)); rt = np.argsort(np.argsort(th))
n_ = len(rz)
spear = 1 - 6 * float(((rz - rt) ** 2).sum()) / (n_ * (n_ ** 2 - 1))
lv.expect('l7', 'screens[3]', round(abs(spear), 3), fmt='{:.3f}')
nparams = 2 * 16 + 16 + 16 * 1 + 1 + 1 * 16 + 16 + 16 * 2 + 2
lv.expect('l7', 'screens[7].widget.answer', nparams)
lv.claim(32 + 16 + 16 + 32 == 96 and 16 + 1 + 16 + 2 == 35 and nparams == 131, 'parameters: 96 weights, 35 biases, 131', covers=[96, 35, 131, 32, 65, 4])
Xf, Xft = ops.arc(15, 0.1, 3), ops.arc(400, 0.1, 1)
sm, bg = tanh_b(Xf, 4, 1, 4000, 0.01, 0), tanh_b(Xf, 64, 1, 4000, 0.01, 0)
trap = [tanh_err(sm, Xf), tanh_err(sm, Xft), tanh_err(bg, Xf), tanh_err(bg, Xft)]
trapA = [round(x, 3) for x in (F['l7-a-curved-bottleneck']['screens'][5]['canvas']['state']['values']['tr']['width 4'], F['l7-a-curved-bottleneck']['screens'][5]['canvas']['state']['values']['te']['width 4'],
                                F['l7-a-curved-bottleneck']['screens'][5]['canvas']['state']['values']['tr']['width 64'], F['l7-a-curved-bottleneck']['screens'][5]['canvas']['state']['values']['te']['width 64'])]
lv.claim(all(abs(a - b) <= 0.0015 for a, b in zip(trapA, trap)), f'trap: stated errors to 3 places agree with the hand-backprop run within 0.0015 ({trap})', covers=trapA)
lv.claim(trap[2] < trap[0] and trap[3] > trap[1], 'trap: the wide net has the lower training error and the higher held-out error (this seed)', covers=[4000, 15, 64])
lv.claim(trap[3] / trap[1] > 1.8, 'held-out error of the wide net about twice the small one', covers=[2])
Xc = ops.arc(300, 0.03, 4, full=True)
Pc = tanh_b(Xc, 16, 1, 2000, 0.01, 0)
Zc = tanh_fwd(Pc, Xc)[1][:, 0]
thc = np.arctan2(Xc[:, 1], Xc[:, 0]); oc = np.argsort(thc)
j = int(np.argmax(np.abs(np.diff(Zc[oc]))))
jump = float((thc[oc][j] + thc[oc][j + 1]) / 2)
lv.claim(0.5 < jump < 1.5, f'full circle: the code tears near 1 radian ({jump:.2f})', covers=[1])
lv.claim(tanh_err(Pc, Xc) < 0.02, f'full circle: net error under 0.02 ({tanh_err(Pc, Xc):.4f}; route A gave 0.0192)', covers=[0.02])
lv.expect('l7', 'screens[6].prose', round(pca_svd(Xc, 1), 2), fmt='{:.2f}')
lv.claim(len(Xc) == 300 and len(Xtr) == 200, '300 and 200 points', covers=[300, 200])
lv.claim(Fr(24 + 16 + 16 + 24 + 8 + 2 + 8 + 3) == 101, 'quiz parameters 101 = 80 + 21', covers=[101, 80, 21, 50, 24])
given([0.001, 0.06, 0.008, 0.02], 'l7 quiz: the two nets\' errors are given in the prompt')
lv.literal('128', why='the hidden width in the review scenario is given')

# ------------------------------------------------------------------ l8
l8 = F['l8-odd-days']
Rtr, Rva, Rte = R3[:500], R3[500:600], R3[600:]
Mf = json.load(open(os.path.join(DATA, 'representations-l8-model.json')))
gm = np.random.default_rng(0)
We8, Wd8 = lin_b(Rtr, 3, 500, 0.05, 0.1 * gm.standard_normal((10, 3)), 0.1 * gm.standard_normal((3, 10)))
lv.claim(np.abs(np.array(Mf['W_enc']) - We8).max() < 1e-5 and np.abs(np.array(Mf['W_dec']) - Wd8).max() < 1e-5 and np.abs(np.array(Mf['b_dec']) - Rtr.mean(0)).max() < 1e-6,
         'representations-l8-model.json: retrained by hand Adam, weights within 1e-5; b_dec is the training mean', covers=[500, 10, 3])


def errs_b(Rx):
    T = Rx - np.array(Mf['b_dec'])
    return ((T - (T @ np.array(Mf['W_enc'])) @ np.array(Mf['W_dec'])) ** 2).sum(1)


ev, et = errs_b(Rva), errs_b(Rte)
sv_ = np.sort(ev); pos = 0.99 * (len(sv_) - 1); thr = float(sv_[int(pos)] + (pos - int(pos)) * (sv_[int(pos) + 1] - sv_[int(pos)]))
kt = kind3[600:]
flags = [i for i in range(150) if et[i] > thr]
tp = sum(1 for i in flags if kt[i] == 1); fp = len(flags) - tp
prec = tp / len(flags)
odd_min = float(min(et[kt == 1])); norm_max = float(max(et[kt != 1]))
for v, f_ in ((thr, '{:.2f}'), (thr, '{:.4f}'), (norm_max, '{:.2f}'), (odd_min, '{:.2f}'), (prec, '{:.3f}')):
    lv.expect('l8', 'screens', round(v, int(f_[3])), fmt=f_)
lv.expect('l8', 'screens[3].prose', len(flags))
lv.expect('l8', 'screens[3].widget.answer', round(prec, 3))
lv.expect('l8', 'screens[3].widget.wrong[1].value', round(fp / 141, 3))
lv.expect('l8', 'screens[3].explain.text', round(100 * fp / 141, 1))
lv.claim(tp == 8 and fp == 3 and int((kt == 0).sum()) == 141, '8 planted caught, 3 false alarms among 141 normal days', covers=[8, 3, 141, 150, 100, 0.99, 11])
sl = l8['screens'][0]['widget']
lv.claim(sl['answer'] - sl['tol'] > norm_max and sl['answer'] + sl['tol'] < odd_min, 'slider band lies inside the gap', covers=[sl['answer'], 8])
steps8 = [round(i * sl['step'], 1) for i in range(int(round((sl['max'] - sl['min']) / sl['step'])) + 1)]
lv.claim(all((abs(v - sl['answer']) <= sl['tol'] + 1e-9) == (norm_max < v < odd_min) for v in steps8), 'the accepted slider positions are exactly the step-0.1 positions inside the gap (2.4 to 5.4)')
lv.claim(all(w_['to'] < norm_max for w_ in sl['wrong'] if w_['id'] == 'low') and all(w_['from'] > odd_min for w_ in sl['wrong'] if w_['id'] == 'high'), 'the low and high bands hold no position inside the gap')
fall = float(et[kt == 2][0]); fall_ret = float(Rte[kt == 2][0].mean())
lv.expect('l8', 'screens[4].prose', round(fall, 2), fmt='{:.2f}')
lv.expect('l8', 'screens[4].prose', round(abs(fall_ret), 1), fmt='{:.1f}')
lv.claim(np.abs(Rte).max() == np.abs(Rte[kt == 2][0]).max() or abs(fall_ret) == max(abs(Rte.mean(1))), 'day 700 has the largest average move of the test days')
lv.claim(abs(Rte.mean(1)).argmax() == list(kt).index(2), 'the biggest move in the sample is day 700', covers=[700])
e3 = [Fr(1, 100) + Fr(1, 100) + Fr(4, 100), Fr(81, 100) + Fr(121, 100) + Fr(81, 100), Fr(1, 100) + Fr(4, 100) + Fr(1, 100)]
lv.claim([float(x) for x in e3] == [0.06, 2.83, 0.06], 'three days: 0.06, 2.83, 0.06', covers=[0.06, 2.83, 0.01, 0.04, 0.81, 1.21, 2.9, 3])
V10 = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 1.4]
q90 = Fr('0.9') + Fr(1, 10) * (Fr('1.4') - Fr('0.9'))
lv.expect('l8', 'screens[2].widget.answer', float(q90))
lv.claim(9 * Fr(9, 10) == Fr(81, 10), 'position 8.1', covers=[8.1, 0.1, 0.9, 1.4])
tb = float(np.sort(et)[int(0.99 * 149)] + (0.99 * 149 - int(0.99 * 149)) * (np.sort(et)[int(0.99 * 149) + 1] - np.sort(et)[int(0.99 * 149)]))
lv.expect('l8', 'screens[5]', round(tb, 2), fmt='{:.2f}')
lv.expect('l8', 'screens[5].prose', sum(1 for x in et if x > tb))
eg = errs_b(Rr[600:])
sh = float(np.mean(eg[50:] > thr))
lv.expect('l8', 'screens[6].prose', round(100 * sh))
bf = int((eg[:50] > thr).sum()); bp = int(((eg[:50] > thr) & (kr[600:650] == 1)).sum())
lv.expect('l8', 'screens[6].prose', bf)
lv.expect('l8', 'screens[6].prose', bp)
lv.claim(len(Rr) == 750 and not np.array_equal(Rr[650:], R3[650:]), 'regime panel: the swap starts at day 650 of 750', covers=[650, 749, 600, 649])
lv.claim(500 * Fr(1, 100) == 5, 'generalise: 5 false alarms in 500', covers=[5, 495, 50, 500, 0.01])
lv.claim(close(0.04 + 0.16, 0.2), 'quiz: 0.2, sizes 0.6, mean 0.0667', covers=[0.2, 0.6, 0.0667, 0.04, 0.16, 0.5, 0.4, 1.0, 0.3])
lv.claim(Fr(6, 8) == Fr(3, 4) and Fr(6, 10) == Fr(3, 5), 'quiz recall 0.75, precision 0.6', covers=[0.75, 0.6, 6, 8, 10])
lv.claim(max(b for b in F['l8-odd-days']['screens'][0]['canvas']['params']['data']) < 8 and max(F['l8-odd-days']['screens'][3]['canvas']['params']['series'][0]['values']) <= 12, 'display caps: histogram below 8, series at most 12', covers=[8, 12])
lv.literal('4%', why='the equity fall in the l8 transfer scenario is given')
lv.claim(200 + 50 == 250, 'l8 quiz: 200 held-out and 50 test days make 250', covers=[250, 200, 50])
lv.literal('-6', why='the market move on day 700 is the planted value stated in the module docstring, checked above')
lv.claim(all(abs(l8['screens'][4]['canvas']['state']['values']['ret'][f'S{j}'] - round(Rte[kt == 2][0][j], 2)) < 1e-9 for j in range(10)), 'fall-day bars are the day 700 returns')

# ------------------------------------------------------------------ code widgets: model solution and twins in CPython
TWINS = {
 'encode_decode': '''def encode_decode(X, W_enc, W_dec):
    X = [[float(v) for v in row] for row in X]
    We = [[float(v) for v in row] for row in W_enc]; Wd = [[float(v) for v in row] for row in W_dec]
    Z = [[sum(x[i] * We[i][j] for i in range(len(x))) for j in range(len(We[0]))] for x in X]
    return np.array([[sum(z[j] * Wd[j][c] for j in range(len(z))) for c in range(len(Wd[0]))] for z in Z])
def recon_error(X, X_hat):
    tot = 0.0
    for a, b in zip(X, X_hat):
        tot += sum((float(x) - float(y)) ** 2 for x, y in zip(a, b))
    return tot / len(X)
''',
 'train_autoencoder': '''def train_autoencoder(X, k, steps, lr, seed):
    return _lin_seeded(np.asarray(X, float), k, steps, lr, seed)
''',
 'pca_recon_error': '''def pca_recon_error(X, k):
    X = np.asarray(X, float); s = np.linalg.svd(X - X.mean(0), compute_uv=False) ** 2 / len(X)
    s = np.concatenate([s, np.zeros(X.shape[1] - len(s))])
    return float(s[k:].sum())
def subspace_angle(W, V):
    W = np.asarray(W, float); V = np.asarray(V, float)
    U = np.linalg.svd(W, full_matrices=False)[0]; Q = np.linalg.svd(V, full_matrices=False)[0]
    P = U @ U.T; worst = 0.0
    R = Q - P @ Q
    s = np.linalg.svd(R, compute_uv=False)
    return float(np.degrees(np.arcsin(min(1.0, s.max()))))
''',
 'check_pca': '''def check_pca(X, k, steps, lr, seed):
    X = np.asarray(X, float)
    We, Wd = _lin_seeded(X, k, steps, lr, seed)
    Xc = X - X.mean(0)
    t = float(((Xc @ We @ Wd - Xc) ** 2).sum(1).mean())
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    return t, _pca_b(X, k), _angle_b(We, Vt[:k].T)
''',
 'make_arc': '''import representations_ops_l2 as ops
def make_arc(n, noise, seed):
    return ops.arc(n, noise, seed)
def compare_with_pca(X_tr, X_te, params):
    X_te = np.asarray(X_te, float)
    k = np.shape(params[2])[1]
    return _tanh_err([np.asarray(p) for p in params], X_te), _pca_svd(X_tr, k, X_te)
''',
 'train_tanh_ae': '''def train_tanh_ae(X, hidden, k, steps, lr, seed):
    return _tanh_b(np.asarray(X, float), hidden, k, steps, lr, seed)
''',
 'day_errors': '''def day_errors(model, R):
    R = np.asarray(R, float); out = []
    We, be, Wd, bd = [np.asarray(model[k], float) for k in ("W_enc", "b_enc", "W_dec", "b_dec")]
    for x in R:
        z = (x - bd) @ We + be
        out.append(float(((x - (z @ Wd + bd)) ** 2).sum()))
    return np.array(out)
def threshold_from_val(errors, q):
    e = sorted(float(x) for x in errors); p = q * (len(e) - 1); i = int(p)
    return e[i] if i + 1 >= len(e) else e[i] + (p - i) * (e[i + 1] - e[i])
''',
 'flag_days': '''def flag_days(errors, thr, labels):
    f = [i for i, e in enumerate(errors) if e > thr]
    hit = sum(1 for i in f if labels[i] == 1); pl = sum(1 for l in labels if l == 1)
    return f, (hit / len(f) if f else 0.0), (hit / pl if pl else 0.0)
''',
 'anomaly_detector': '''def anomaly_detector(R_train, R_val, R_test, k, q):
    R_train = np.asarray(R_train, float); mu = R_train.mean(0)
    U, s, Vt = np.linalg.svd(R_train - mu, full_matrices=False); V = Vt[:k].T
    def e(R):
        T = np.asarray(R, float) - mu
        return ((T - T @ V @ V.T) ** 2).sum(1)
    thr = np.quantile(e(R_val), q)
    return [int(i) for i in np.where(e(R_test) > thr)[0]]
''',
 'choose_k': '''def choose_k(X_train, X_val, max_err):
    X_train = np.asarray(X_train, float)
    for k in range(X_train.shape[1] + 1):
        if _pca_svd(X_train, k, X_val) <= max_err:
            return k
    return X_train.shape[1]
''',
}


def _angle_b(W, V):
    W = np.asarray(W, float); V = np.asarray(V, float)
    U = np.linalg.svd(W, full_matrices=False)[0]; Q = np.linalg.svd(V, full_matrices=False)[0]
    s = np.linalg.svd(Q - U @ U.T @ Q, compute_uv=False)
    return float(np.degrees(np.arcsin(min(1.0, s.max()))))


HELP = {'_lin_seeded': lin_seeded, '_pca_b': lambda X, k: pca_svd(X, k), '_angle_b': _angle_b, '_tanh_err': tanh_err, '_pca_svd': pca_svd, '_tanh_b': tanh_b}


def same(got, want, cmp, tol):
    def norm(v):
        if hasattr(v, 'tolist'):
            v = v.tolist()
        if isinstance(v, tuple):
            v = list(v)
        if isinstance(v, list):
            return [norm(x) for x in v]
        return v
    got, want = norm(got), norm(want)
    if cmp == 'isclose':
        def cl(a, b):
            if isinstance(a, list) or isinstance(b, list):
                return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(cl(x, y) for x, y in zip(a, b))
            if isinstance(a, bool) or isinstance(b, bool):
                return a == b
            if tol:
                return math.isclose(a, b, rel_tol=tol.get('rel', 0) or 0, abs_tol=tol.get('abs', 0) or 0) or a == b
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
        return cl(got, want)
    return got == want


def run_widget(w, src, label, skip=()):
    cwd = os.getcwd(); os.chdir(DATA)
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}
        ns.update(HELP)
        exec(ZQ_LIB, ns); exec(w.get('prelude', 'import numpy as np\n'), ns); exec('import numpy as np\n', ns); exec(src, ns)
        ok_all = True
        for k, t in enumerate(w['tests']):
            if k + 1 in skip:
                continue
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            ok = same(got, eval(t['expect']), t.get('compare', 'equal'), t.get('tol'))
            ok_all &= ok
            if not ok:
                print('   mismatch', label, 'test', k + 1, str(got)[:80], 'vs', t['expect'][:80])
        return ok_all
    finally:
        os.chdir(cwd)


def widgets(doc):
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget')
            if isinstance(w, dict) and w.get('kind') == 'code':
                yield f'{key}[{i}]', w


n_code = 0
for fid, doc in F.items():
    for path, w in widgets(doc):
        n_code += 1
        lv.claim(run_widget(w, w['solution'], f'{fid} {path}'), f'{fid} {path}: the model solution passes every hidden test in CPython')
        name = next(k for k in TWINS if f'def {k}(' in w['solution'])
        lv.claim(run_widget(w, TWINS[name], f'{fid} {path} twin'), f'{fid} {path}: an independent twin ({name}) gives the same results')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{fid} {path}: at least two mutants')
lv.claim(n_code == 10, 'ten code widgets in the level')
# thresholds of the training widgets hold across seeds (route B)
for s in range(4):
    Xb = np.random.default_rng(6 + s).standard_normal((1000, 5)) @ np.diag([1.7, 1.0, 0.7, 0.55, 0.45]) + 3
    We_, Wd_ = lin_seeded(Xb, 2, 300, 0.05, s)
    Xc_ = Xb - Xb.mean(0)
    lv.claim(float(((Xc_ @ We_ @ Wd_ - Xc_) ** 2).sum(1).mean()) < pca_svd(Xb, 2) + 0.002, f'train_autoencoder threshold holds with margin, seed {s}')
for s in range(4):
    Xa, Xb_ = ops.arc(200, 0.05, 10 + s), ops.arc(200, 0.05, 20 + s)
    Pa = tanh_b(Xa, 16, 1, 500, 0.01, s)
    e_ = tanh_err(Pa, Xb_)
    lv.claim(e_ < 0.01 and e_ < pca_svd(Xa, 1, Xb_) / 6, f'train_tanh_ae threshold (0.02, a third of PCA) holds with margin, data {10 + s}, seed {s}: {e_:.4f}')
    if s == 0:
        lv.claim(e_ < 0.01, f'the stated "well below 0.01" after 500 steps on arc seeds 10 and 20 ({e_:.4f})', covers=[0.01])
nsA = {'__name__': 'x'}
exec(F['homework-2']['items'][0]['widget']['solution'], nsA)
for s in (3, 7):
    Rs, ks = ops.odd_day_panel(s)
    nsd = {}
    exec('import numpy as np\n' + TWINS['anomaly_detector'], nsd)
    f_ = nsd['anomaly_detector'](Rs[:500], Rs[500:600], Rs[600:], 3, 0.99)
    odd = set(int(i) for i in np.where(ks[600:] == 1)[0])
    fA = nsA['anomaly_detector'](Rs[:500], Rs[500:600], Rs[600:], 3, 0.99)
    lv.claim(odd <= set(f_) and 100 not in f_ and len(f_) <= 14 and odd <= set(fA) and 100 not in fA and len(fA) <= 14, f'anomaly_detector on test panel {s}: all planted caught and the fall quiet by the SVD twin and the trained solution, {len(f_)} and {len(fA)} flags (test bound 18)')
for s in (4,):
    Rs, ks = ops.odd_day_panel(s)
    nsd = {}
    exec('import numpy as np\n' + TWINS['anomaly_detector'], nsd)
    lv.claim(len(nsd['anomaly_detector'](Rs[:400], Rs[400:500], Rs[500:600], 3, 0.99)) <= 2 and len(nsA['anomaly_detector'](Rs[:400], Rs[400:500], Rs[500:600], 3, 0.99)) <= 2, f'all-normal block of panel {s}: at most 2 alarms by both routes (test bound 4)')
lv.literal('0.001, 0.01, 0.02, 1e-9, 1e-4, 6, 7, 9, 4, 5, 18', why='test counts, places and tolerances in how lines are settings of the hidden tests, which this script runs')
given([1000, 300, 500, 3, 5], 'step counts and sizes named in how lines are the hidden tests\' own settings, which this script runs')

# ------------------------------------------------------------------ review, problems, homework
rv = F['review-2']
lv.claim(Fr(2) + 1 == 3 and Fr(3, 5) == Fr(6, 10), 'review: 3; 60% of 5', covers=[3, 4, 1, 0.6, 0.4, 1.5, 5, 2])
zr = Fr('0.6') * 3 + Fr('0.8') * 1
lv.claim(zr == Fr('2.6') and 10 - zr * zr == Fr('3.24'), 'review: code 2.6, miss 3.24', covers=[2.6, 3.24, 6.76, 10, 1.8, 0.8])
qr = Fr('0.9') + Fr(2, 10) * (Fr('1.5') - Fr('0.9'))
lv.expect('review', 'items[7].widget.answer', float(qr))
lv.claim(4 * Fr(8, 10) == Fr(16, 5), 'review quantile position 3.2', covers=[3.2, 0.2, 0.5, 0.6, 0.9, 1.5, 0.8])
lv.claim(sorted([1.9, 3.5, 1.21]) == [x for x in sorted([0.4, 1.9, 0.7, 1.2, 3.5, 1.21]) if x > 1.2], 'review flags: 1.9, 3.5, 1.21', covers=[1.9, 3.5, 1.21, 1.2, 0.4, 0.7])
given([0.0001, 0.0004, 0.07, 0.05, 1.3, 0.2, 0.4, 0.9, 25, 8], 'review scenarios: errors, columns and counts given in the prompts')
pb = F['problems-2']
a_, b_ = 4 + 1.5, 4 - 1.5
lv.claim(close(eig2(4, 1.5, 4)[0], a_) and close(eig2(4, 1.5, 4)[1], b_), 'problem 1: eigenvalues 5.5, 2.5 and 1', covers=[5.5, 2.5, 1, 9, 4, 1.5])
lv.expect('problems', 'items[0].parts[1].widget.answer', round(5.5 / 9, 4))
lv.expect('problems', 'items[0].parts[1].feedback.correct', round(550 / 9, 1))
lv.expect('problems', 'items[0].parts[1].widget.wrong[0].value', round(3.5 / 9, 4))
lv.expect('problems', 'items[0].parts[1].widget.wrong[1].value', round(5.5 / 8, 4))
lv.claim(close(b_ + 1, 3.5) and close(5.5 + b_, 8), 'problem 1: one-code error 2.5 + 1 = 3.5; the pair alone sums to 8', covers=[3.5, 8])
VAL = [Fr(x) for x in ('0.3', '0.35', '0.4', '0.5', '0.55', '0.6', '0.8', '1.1')]
pos = Fr(7) * Fr(3, 4)
thrP = VAL[5] + (pos - 5) * (VAL[6] - VAL[5])
lv.expect('problems', 'items[1].parts[0].widget.answer', float(thrP))
lv.claim(pos == Fr(21, 4), 'position 5.25', covers=[5.25, 0.25, 0.75, 0.6, 0.8, 0.2])
TEST = [Fr(x) for x in ('0.45', '2.4', '0.95', '0.62', '3.1', '0.85')]
lab = [0, 1, 0, 0, 1, 1]
fl = [i for i, e in enumerate(TEST) if e > thrP]
lv.expect('problems', 'items[1].parts[1].widget.answer', len(fl))
hits = sum(lab[i] for i in fl)
lv.expect('problems', 'items[1].parts[2].widget.answer', round(hits / len(fl), 2))
fl1 = [i for i, e in enumerate(TEST) if e > 1]
lv.expect('problems', 'items[1].parts[3].widget.answer', round(sum(lab[i] for i in fl1) / 3, 3))
given([0.3, 0.35, 0.4, 0.5, 0.55, 1.1, 0.45, 2.4, 0.95, 0.62, 3.1, 0.85, 1.0], 'problem 2: the errors and the raised threshold are given in the prompt')
lv.claim(close(round(1 / 3, 3), 0.333) and close(round(2 / 3, 3), 0.667), 'problem 2 slips 1/3 and 2/3', covers=[0.333, 0.667])
aq = 0.5 - 4 / math.pi ** 2; cq = 1 / math.pi - 4 / math.pi ** 2
aq_b = quad(lambda t: math.cos(t) ** 2 * 2 / math.pi, 0, math.pi / 2)[0] - quad(lambda t: math.cos(t) * 2 / math.pi, 0, math.pi / 2)[0] ** 2
cq_b = quad(lambda t: math.cos(t) * math.sin(t) * 2 / math.pi, 0, math.pi / 2)[0] - quad(lambda t: math.cos(t) * 2 / math.pi, 0, math.pi / 2)[0] ** 2
lv.claim(abs(aq - aq_b) < 1e-12 and abs(cq - cq_b) < 1e-12, 'quarter circle: variance and covariance by quadrature')
lv.expect('problems', 'items[2].parts[0].widget.answer', round(aq, 4))
lv.expect('problems', 'items[2].parts[1].widget.answer', round(cq, 4))
lv.expect('problems', 'items[2].parts[2].widget.answer', round(aq + cq, 4))
lv.expect('problems', 'items[2].parts[2].widget.wrong[0].value', round(aq - cq, 4))
lv.expect('problems', 'items[2].parts[1].widget.wrong[1].value', round(1 / math.pi, 4))
lv.expect('problems', 'items[2].parts[0].widget.wrong[1].value', round(2 / math.pi, 4))
lv.expect('problems', 'items[2].parts[2].question', round(aq, 4))
lv.expect('problems', 'items[2].parts[2].explain.text', round(abs(cq), 4))
lv.claim(abs(quad(lambda t: math.cos(t) ** 2 * 2 / math.pi, 0, math.pi / 2)[0] - 0.5) < 1e-12, 'quarter circle: E[cos^2] = 1/2 by quadrature', covers=[0.5])
hw = F['homework-2']
lv.expect('homework', 'items[4].widget.answer', round(0.3 / 3.6, 4))
lv.expect('homework', 'items[4].feedback.correct', round(30 / 3.6, 1))
given([2.4, 0.9, 0.2, 0.1], 'homework eigenvalues given in the prompt')
lv.claim(Fr('2.4') + Fr('0.9') + Fr('0.2') + Fr('0.1') == Fr('3.6') and Fr('0.2') + Fr('0.1') == Fr('0.3'), 'homework: total 3.6, dropped 0.3', covers=[0.3, 3.6, round(3.3 / 3.6, 4), round(0.1 / 3.6, 4)])
w_ = 10 * 32 + 32 * 3 + 3 * 32 + 32 * 10; b__ = 32 + 3 + 32 + 10
lv.expect('homework', 'items[5].widget.answer', w_ + b__ - 40)
lv.claim(w_ == 832 and b__ == 77 and w_ + b__ == 909, 'homework parameters: 832 + 77 = 909, PCA 40', covers=[832, 77, 909, 40, 320, 96, 30, 10, 792])
lv.claim(Fr(4, 12) == Fr(1, 3) and Fr(4, 5) == Fr(8, 10), 'homework precision 0.333, recall 0.8', covers=[0.333, 0.8, 0.667, 12, 5, 4])
given([500, 10, 7, 20, 2.0], 'homework scenarios: universe sizes, factor counts, the crash size and the test shift are given')
lv.literal('7%', why='the crash size in the homework scenario is given')
lv.check_wrongs()
lv.report()
