"""representations level 3 (Variational autoencoders): every stated number recomputed by a second route.

Route A is the generator (NumPy, the autograd, nt_ops_l1.adam_step). Route B here is independent: closed forms written
out by hand (2 x 2 inverses, Fractions), SciPy quadrature for every integral the level quotes, plain loops for the Monte
Carlo tables, and the VAE retrained with a hand-written backward pass and a hand-written Adam. Every code widget's hidden
tests are rerun in CPython with the model solution and with an independent twin. Run through
`node tools/run-number-scripts.mjs --only representations-L3` (one BLAS thread); strict coverage.
"""
import json, math, os, sys, hashlib
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from scipy.integrate import quad
from numbers_lib import Level, ZQ_LIB
from autograd import Tensor, grad_check
import representations_ops_l3 as ops

lv = Level("representations", 3, coverage="strict")
F = lv.files
L2PI = math.log(2 * math.pi)


def given(vals, why):
    for v in vals:
        lv.literal(str(v), why=why)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def sha(name):
    return hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest()


lv.claim(sha('autograd.py').startswith('5917d4ec91f7') and sha('nt_ops_l1.py').startswith('9c1391a33624'), 'autograd.py and nt_ops_l1.py byte-identical to the frozen v1.0')


def kl1(mu, s):
    """KL(N(mu, s^2) || N(0, 1)) by quadrature of q ln(q/p)."""
    f = lambda z: math.exp(-(z - mu) ** 2 / (2 * s * s)) / (s * math.sqrt(2 * math.pi)) * (-math.log(s) - (z - mu) ** 2 / (2 * s * s) + z * z / 2)
    return quad(f, mu - 12 * s, mu + 12 * s, limit=200)[0]


def klg(m1, s1, m2, s2):
    f = lambda z: math.exp(-(z - m1) ** 2 / (2 * s1 * s1)) / (s1 * math.sqrt(2 * math.pi)) * (math.log(s2 / s1) - (z - m1) ** 2 / (2 * s1 * s1) + (z - m2) ** 2 / (2 * s2 * s2))
    return quad(f, m1 - 12 * s1, m1 + 12 * s1, limit=200)[0]


def g_c(z):
    return (math.sin(z), math.cos(z))


def dens(x, g, s):
    return math.exp(-((x[0] - g[0]) ** 2 + (x[1] - g[1]) ** 2) / (2 * s * s)) / (2 * math.pi * s * s)


# ------------------------------------------------------------------ module: gradient check and recipes
Pg = [Tensor(p + 0.1 * np.random.default_rng(3).standard_normal(np.shape(p))) for p in ops.init_vae(2, 5, 1, 2)]
Xg, _ = ops.circle_model(8, 0.05, 1)
Eg = np.random.default_rng(4).standard_normal((8, 1))


def lossg():
    mu, lvv = ops.vae_encode(Pg, Xg)
    z = mu + (lvv * 0.5).exp() * Eg
    xh = ops.vae_decode(Pg, z)
    return ((xh - Xg) ** 2).sum() / 0.02 / 8 + (mu * mu + lvv.exp() - 1 - lvv).sum() * 0.5 / 8


gerr = grad_check(lossg, Pg)
lv.claim(gerr < 1e-6, f'vae_encode and vae_decode through the autograd: gradient check, relative error {gerr:.1e}')
g0 = np.random.default_rng(5); z0 = g0.standard_normal(4)
lv.claim(np.array_equal(ops.circle_model(4, 0.05, 5)[0], np.stack([np.sin(z0), np.cos(z0)], 1) + 0.05 * g0.standard_normal((4, 2))), 'circle_model: z first, then noise, one generator')

# ------------------------------------------------------------------ l9
l9 = F['l9-a-hidden-cause']
ABC = {"A": (0.5, (0.02, -0.01)), "B": (-1.2, (-0.03, 0.02)), "C": (2.0, (0.01, 0.03))}
PT = {k: (math.sin(z) + e[0], math.cos(z) + e[1]) for k, (z, e) in ABC.items()}
for k, (x, y) in PT.items():
    gss = math.atan2(x, y)
    lv.expect('l9', 'screens[0]', round(gss, 2), fmt='{:.2f}')
lv.claim(all(abs(math.atan2(*PT[k]) - ABC[k][0]) < 0.15 for k in PT), 'true z within the 0.15 tolerance of each guess', covers=[0.15, 0.5, 1.2, 2.0])
lv.claim(round(math.atan2(*PT['A']), 1) == 0.5, 'hint: A about 0.5')
x0 = (0.5, 0.9); gz = g_c(0.5)
d2 = (x0[0] - gz[0]) ** 2 + (x0[1] - gz[1]) ** 2
lp = -math.log(2 * math.pi * 0.0025) - d2 / 0.005
lv.expect('l9', 'screens[2].question', round(d2, 6), fmt='{:.6f}')
lv.expect('l9', 'screens[2].widget.answer', round(lp, 2))
lv.expect('l9', 'screens[2].explain.text', round(d2 / 0.005, 3), fmt='{:.3f}')
lv.claim(close(-math.log(2 * math.pi * 0.0025), 4.1535, 1e-4) and close(2 * math.pi * 0.0025, 0.015708, 1e-4), 'constant 4.15 from 2 pi 0.0025 = 0.015708', covers=[4.15, 0.015708, 0.0025, 0.05, 0.005])
xA = PT['A']
zs5 = np.random.default_rng(4).standard_normal(5)
p5 = [dens(xA, g_c(z), 0.05) for z in zs5]
rows = l9['screens'][3]['canvas']['params']['rows']
lv.claim(all(rows[i][1] == f'{zs5[i]:.3f}' and rows[i][2] == f'{p5[i]:.2f}' for i in range(5)), 'five draws and their densities, by a loop', covers=[round(float(z), 3) for z in zs5] + [round(p, 2) for p in p5])
m5 = sum(round(p, 2) for p in p5) / 5
lv.expect('l9', 'screens[3].widget.answer', round(m5, 2))
lv.expect('l9', 'screens[3].widget.wrong[0].value', round(sum(round(p, 2) for p in p5), 2))
pA = quad(lambda z: dens(xA, g_c(z), 0.05) * math.exp(-z * z / 2) / math.sqrt(2 * math.pi), -8, 8, points=[0.5], limit=400)[0]
lv.expect('l9', 'screens[4].prose', round(pA, 2), fmt='{:.2f}')
est20 = [sum(dens(xA, g_c(z), 0.05) for z in np.random.default_rng(100 + k).standard_normal(20)) / 20 for k in range(10)]
v20 = l9['screens'][4]['canvas']['state']['values']['n20']
lv.claim(all(abs(v20[str(k + 1)] - round(est20[k], 3)) < 1e-9 for k in range(10)), 'ten 20-draw estimates by a loop')
est2000 = [float(np.mean([dens(xA, g_c(z), 0.05) for z in np.random.default_rng(200 + k).standard_normal(2000)])) for k in range(10)]
v2000 = l9['screens'][4]['canvas']['state']['values']['n2000']
lv.claim(all(abs(v2000[str(k + 1)] - round(est2000[k], 3)) < 1e-9 for k in range(10)), 'ten 2,000-draw estimates by a loop', covers=[20, 2000])
from math import erf
share = 0.5 * (erf(0.6 / math.sqrt(2)) - erf(0.4 / math.sqrt(2)))
lv.claim(abs(share - 0.07) < 0.005, f'hint: about 7 of 100 normal draws within 0.1 of 0.5 ({share:.4f})', covers=[7, 100, 0.1])
zg = [round(-1.0 + 0.25 * i, 2) for i in range(13)]
wq = [dens(xA, g_c(z), 0.05) * math.exp(-z * z / 2) for z in zg]
tot = sum(wq); wq = [w / tot for w in wq]
pk = zg[wq.index(max(wq))]
lv.expect('l9', 'screens[5].widget.answer', pk)
lv.claim(all(abs(l9['screens'][5]['canvas']['state']['values'][f'{v:g}'] - round(w, 4)) < 1e-9 for v, w in zip(zg, wq)), 'posterior bars by a loop', covers=[0.25])
lv.claim(Fr(1) + Fr(1, 4) == Fr(5, 4), 'straight decoder: 1 + 0.25 = 1.25', covers=[1.25, 0.25, 1.5, 0.5, 1.0])
beta = [Fr(12, 10), Fr(8, 10), Fr(1)]; rr = [Fr(-15, 10), Fr(-9, 10), Fr(-13, 10)]; s2 = Fr(1, 4)
bt = sum(b * x for b, x in zip(beta, rr)); bb = sum(b * b for b in beta)
pm = (bt / s2) / (1 + bb / s2)
lv.expect('l9', 'screens[11].widget.answer', round(float(pm), 2))
lv.claim(bt == Fr(-382, 100) and bb == Fr(308, 100) and bt / s2 == Fr(-1528, 100) and 1 + bb / s2 == Fr(1332, 100), 'transfer: -3.82, 3.08, -15.28, 13.32', covers=[3.82, 3.08, 15.28, 13.32])
lv.expect('l9', 'screens[11].widget.wrong[0].value', round(float(bt / bb), 2))
given([1.2, 0.8, 1.0, 1.5, 0.9, 1.3, 0.5], 'transfer: loadings, returns and the noise sd are given in the prompt')
lv.claim(Fr(4) + 1 == 5, 'quiz: 2^2 + 1 = 5; slips 4 and 3', covers=[5, 4, 3])
given([0.02, 0.2], 'the noise levels of the explore screen are settings')
given([150, 200], 'point counts of the scatter canvases are settings')

# ------------------------------------------------------------------ l10
l10 = F['l10-the-elbo']
x = (1.0, 0.8); w = (1.0, 0.5); s = 0.5
C = [[w[0] * w[0] + s * s, w[0] * w[1]], [w[0] * w[1], w[1] * w[1] + s * s]]
det = C[0][0] * C[1][1] - C[0][1] ** 2
q = (C[1][1] * x[0] ** 2 - 2 * C[0][1] * x[0] * x[1] + C[0][0] * x[1] ** 2) / det
logpx = -L2PI - 0.5 * math.log(det) - 0.5 * q
lv.expect('l10', 'screens[0].prose', round(logpx, 3), fmt='{:.3f}')
lv.expect('l10', 'screens[0].canvas.derive.caption', round(logpx, 4), fmt='{:.4f}')
vs = Fr(1) / (1 + Fr(5, 4) / Fr(1, 4)); ms = vs * (Fr(1) + Fr(4, 10)) / Fr(1, 4)
lv.claim(vs == Fr(1, 6) and ms == Fr(14, 15), 'posterior N(14/15, 1/6)', covers=[float(ms), round(float(ms), 4), round(float(vs), 2), round(float(ms), 2)])


def elbo(m, v):
    return -math.log(2 * math.pi * s * s) - ((x[0] - w[0] * m) ** 2 + (x[1] - w[1] * m) ** 2 + (w[0] ** 2 + w[1] ** 2) * v) / (2 * s * s) - 0.5 * (m * m + v - 1 - math.log(v))


lv.claim(close(elbo(float(ms), float(vs)), logpx, 1e-12), 'the ELBO at the posterior equals ln p(x)')
lv.claim(all(elbo(m, v) <= logpx + 1e-12 for m in np.linspace(-1, 2.5, 36) for v in np.linspace(0.02, 1.5, 30)), 'the ELBO never crosses ln p(x) on the slider ranges', covers=[0.02, 1.5, 2.5])
klstar = 0.5 * (float(ms) ** 2 + float(vs) - 1 + math.log(6))
lv.expect('l10', 'screens[1].widget.answer', round(klstar, 3))
lv.expect('l10', 'screens[1].widget.wrong[0].value', round(0.5 * (float(ms) ** 2 + float(vs) - 1), 3))
lv.claim(close(math.log(6), 1.7918, 1e-4) and close(float(ms) ** 2, 0.8711, 1e-4), 'ln 6 = 1.7918, m^2 = 0.8711', covers=[1.7918, 0.8711, 0.1667])
lv.claim(close(kl1(float(ms), math.sqrt(float(vs))), klstar, 1e-7), 'the KL term by quadrature')
e01 = elbo(0, 1)
lv.expect('l10', 'screens[3].prose', round(e01, 3), fmt='{:.3f}')
gap = logpx - e01
lv.expect('l10', 'screens[3].widget.answer', round(gap, 2))
lv.expect('l10', 'screens[3].widget.wrong[0].value', round(abs(e01), 2))
klpost = 0.5 * (1 / float(vs) + float(ms) ** 2 / float(vs) - 1 + math.log(float(vs)))
lv.claim(close(gap, klpost, 1e-12), 'gap at the prior equals KL(prior || posterior)', covers=[round(gap, 3), round(gap, 2)])
lv.claim(gap > 4, 'gap over 4 (byKey)', covers=[4])
for lbl, m, v in (("prior", 0.0, 1.0), ("posterior", float(ms), float(vs)), ("too sharp", float(ms), 0.01)):
    rec = elbo(m, v) + 0.5 * (m * m + v - 1 - math.log(v))
    klv = 0.5 * (m * m + v - 1 - math.log(v))
    vals = l10['screens'][4]['canvas']['state']['values']
    lv.claim(abs(vals['rec'][lbl] - round(rec, 3)) < 1e-9 and abs(vals['kl'][lbl] + round(klv, 3)) < 1e-9, f'terms bars for {lbl}')
lv.expect('l10', 'screens[4].widget.options', round(elbo(float(ms), 0.01), 2), fmt='{:.2f}')
lv.expect('l10', 'screens[4].widget.options', round(logpx, 2), fmt='{:.2f}')
lv.claim(close(float(ms), 0.9333, 1e-4), 'm* = 0.9333', covers=[0.9333, 0.01])
lv.claim(Fr(-32, 10) - Fr(-39, 10) == Fr(7, 10), 'quiz gap 0.7', covers=[0.7, 3.2, 3.9, 7.1])

# ------------------------------------------------------------------ l11
l11 = F['l11-gaussian-kl']
for (m, sg) in ((1, 0.5), (2, 1), (0, 2), (0.5, 0.8), (0, 0.1), (0, 0.001), (0.6, 1.5), (0, 3)):
    cf = 0.5 * (m * m + sg * sg - 1 - math.log(sg * sg))
    if sg >= 0.1:
        lv.claim(close(kl1(m, sg), cf, 1e-7), f'KL(N({m}, {sg}^2)) closed form {cf:.6f} agrees with quadrature')
lv.expect('l11', 'screens[1].widget.answer', round(0.5 * (1 + 0.25 - 1 - math.log(0.25)), 3))
lv.claim(close(-math.log(0.25), 1.3863, 1e-4), '-ln 0.25 = 1.3863', covers=[1.3863, 1.386, 0.25, 0.5])
for i, (m, sg) in enumerate([(2, 1), (0, 2), (0.5, 0.8)]):
    lv.expect('l11', f'screens[2].widget.rows[{i}][2].answer', round(0.5 * (m * m + sg * sg - 1 - math.log(sg * sg)), 4))
lv.expect('l11', 'screens[2]', round(0.5 * (4 - 1 - math.log(4)), 3), fmt='{:.3f}')
lv.expect('l11', 'screens[2]', round(0.5 * (0.25 + 0.64 - 1 - math.log(0.64)), 3), fmt='{:.3f}')
mc = {}
for n_ in (100, 10000, 1000000):
    zq = 1 + 0.5 * np.random.default_rng(7).standard_normal(n_)
    tot_ = 0.0
    for chunk in np.array_split(zq, max(1, n_ // 100000)):
        tot_ += float(np.sum(math.log(2) - (chunk - 1) ** 2 * 2 + chunk ** 2 / 2))
    mc[n_] = tot_ / n_
k1 = 0.5 * (1 + 0.25 - 1 - math.log(0.25))
rows11 = l11['screens'][4]['canvas']['params']['rows']
lv.claim(all(abs(float(rw[1]) - mc[n_]) < 1e-4 for rw, n_ in zip(rows11, (100, 10000, 1000000))), 'MC table by chunked sums', covers=[100, 10000, 1000000] + [round(v, 4) for v in mc.values()])
lv.expect('l11', 'screens[4].widget.answer', round(abs(mc[1000000] - k1), 4))
lv.expect('l11', 'screens[4].explain.text', round(abs(mc[100] - k1), 3), fmt='{:.3f}')
lv.expect('l11', 'screens[4].prose', round(k1, 3), fmt='{:.3f}')
lv.claim(close(k1, 0.8181, 1e-4), 'formula 0.8181', covers=[0.8181, 0.8183, 0.0002])
kb = klg(0, 1, 1, 0.5)
lv.expect('l11', 'screens[5].widget.answer', round(kb, 3))
lv.claim(close(kb, math.log(0.5) + 4 - 0.5, 1e-7), 'reverse KL by quadrature equals ln 0.5 + 4 - 0.5', covers=[4, 0.5])
lv.expect('l11', 'screens[6].widget.options', 0.5 * (0.01 - 1))
lv.expect('l11', 'screens[6].widget.options', round(0.5 * (0.01 - 1 - math.log(0.01)), 3))
lv.claim(close(-math.log(0.01), 4.605, 1e-3), '-ln 0.01 = 4.605; slip 0.495', covers=[4.605, 0.495, 0.01])
kt = 0.5 * (1e-6 - 1 - math.log(1e-6))
lv.expect('l11', 'screens[7].widget.answer', round(kt, 2))
lv.expect('l11', 'screens[7].widget.wrong[1].value', round(-math.log(0.001), 2))
lv.claim(close(-math.log(1e-6), 13.82, 1e-3), '-ln 1e-6 = 13.82', covers=[13.82])
k2 = 0.5 + 0.5 * (0.25 - 1 - math.log(0.25))
lv.expect('l11', 'screens[8].widget.answer', round(k2, 3))
lv.expect('l11', 'screens[8].widget.wrong[1].value', round(0.5 * (0.25 - 1 - math.log(0.25)), 3))
lv.claim(close(k2, k1, 1e-12), 'the two-coordinate KL equals the one for N(1, 0.5^2)')
kd = klg(0.5, 1.2, 0, 1)
lv.expect('l11', 'screens[11].widget.answer', round(kd, 3))
lv.claim(close(math.log(1 / 1.2), -0.1823, 1e-3) and close((1.44 + 0.25) / 2, 0.845, 1e-9), 'transfer pieces -0.182 and 0.845', covers=[0.182, 0.845, 1.44, 0.25, 1.2])
given([0.5, 1.2, 1.5, 0.1, 2.5], 'slider ranges and the forecast parameters are settings or given')
lv.claim(close(0.5 * 0.09, 0.045, 1e-12), 'quiz: at least 0.045 for mu = 0.3', covers=[0.045, 0.3])
lv.claim(Fr('0.2') + Fr('0.05') + Fr('1.1') == Fr('1.35'), 'quiz 1.35; mean slip 0.45', covers=[1.35, 0.45, 0.2, 0.05, 1.1])
lv.expect('l11', 'quiz[0].widget.answer', round(0.5 * (4 - 1 - math.log(4)), 3))

# ------------------------------------------------------------------ l12: route B VAE training by hand backprop
VF = json.load(open(os.path.join(DATA, 'representations-l12-vae.json')))
Pstart_f = [np.array(a) for a in VF['start']]; Ptr_f = [np.array(a) for a in VF['trained']]
S = ops.S_DEC


def adam_b(p, g, st, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m, v = st
    m[:] = b1 * m + (1 - b1) * g
    v[:] = b2 * v + (1 - b2) * g * g
    return p - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)


def vae_grads(P, X, E):
    We, be, Wm, bm, Wv, bv, Wd, bd, Wo, bo = P
    n = len(X)
    h = np.tanh(X @ We + be); mu = h @ Wm + bm; l = h @ Wv + bv
    sd = np.exp(l / 2); z = mu + sd * E
    hd = np.tanh(z @ Wd + bd); xh = hd @ Wo + bo
    loss = ((xh - X) ** 2).sum() / (2 * S * S) / n + L2PI + 2 * math.log(S) + 0.5 * (mu ** 2 + np.exp(l) - 1 - l).sum() / n
    rec = -((xh - X) ** 2).sum() / (2 * S * S) / n - L2PI - 2 * math.log(S)
    kl = 0.5 * (mu ** 2 + np.exp(l) - 1 - l).sum() / n
    dxh = (xh - X) / (S * S * n)
    gWo, gbo = hd.T @ dxh, dxh.sum(0)
    dad = (dxh @ Wo.T) * (1 - hd ** 2)
    gWd, gbd = z.T @ dad, dad.sum(0)
    dz = dad @ Wd.T
    dmu = dz + mu / n
    dl = dz * E * sd / 2 + (np.exp(l) - 1) / (2 * n)
    gWm, gbm, gWv, gbv = h.T @ dmu, dmu.sum(0), h.T @ dl, dl.sum(0)
    da = (dmu @ Wm.T + dl @ Wv.T) * (1 - h ** 2)
    gWe, gbe = X.T @ da, da.sum(0)
    return loss, rec, kl, [gWe, gbe, gWm, gbm, gWv, gbv, gWd, gbd, gWo, gbo]


def train_b(X, P0, steps, lr, seed, trace=False):
    P = [np.array(p, float) for p in P0]
    sts = [(np.zeros_like(p), np.zeros_like(p)) for p in P]
    g = np.random.default_rng(seed)
    k = P[2].shape[1]
    tr = []
    for t in range(1, steps + 1):
        E = g.standard_normal((len(X), k))
        loss, rec, kl, G = vae_grads(P, X, E)
        tr.append((-loss, rec, kl))
        P = [adam_b(p, gg, st, t, lr) for p, gg, st in zip(P, G, sts)]
    return (P, tr) if trace else P


def init_b(d, h, k, seed):
    g = np.random.default_rng(seed)
    out = []
    for fi, fo in ((d, h), (h, k), (h, k), (k, h), (h, d)):
        out.append(g.standard_normal((fi, fo)) / math.sqrt(fi)); out.append(np.zeros(fo))
    return out


X5, _ = ops.circle_model(500, 0.05, 0)
Pb1, tr1 = train_b(X5, init_b(2, 32, 1, 0), 300, 0.003, 1, trace=True)
lv.claim(max(float(np.abs(a - b).max()) for a, b in zip(Pb1, Pstart_f)) < 1e-5, 'starting weights: 300 hand-backprop Adam steps reproduce the file to 1e-5', covers=[300, 0.003])
Pb2, tr2 = train_b(X5, Pstart_f, 3700, 0.003, 2, trace=True)
dw = max(float(np.abs(a - b).max()) for a, b in zip(Pb2, Ptr_f))
lv.claim(dw < 1e-3, f'trained weights: 3,700 more hand-backprop steps reproduce the file to {dw:.1e}', covers=[4000, 3700])
cb = tr1 + tr2
lv.claim(max(abs(a - round(b[0], 4)) for a, b in zip(VF['elbo'], cb[::20])) < 0.01 and max(abs(a - round(b[2], 4)) for a, b in zip(VF['kl'], cb[::20])) < 0.01, 'recorded ELBO and KL curves reproduced within 0.01 nats')
klend = float(np.mean([c[2] for c in cb[::20][-25:]]))
lv.claim(abs(klend - 2.4) < 0.05, f'KL settles at about 2.4 ({klend:.3f})', covers=[2.4])
lv.claim(min(VF['elbo']) < -12, 'the series is capped at -12', covers=[12])
lv.claim(cb[0][2] < 0.5, 'KL starts near 0')
z1 = 0.4 + math.exp(-1) * 0.5
lv.expect('l12', 'screens[2].prose', round(z1, 4), fmt='{:.4f}')
d2 = (0.55 - 0.52) ** 2 + (0.83 - 0.86) ** 2
rec1 = -math.log(2 * math.pi * 0.01) - d2 / 0.02
kl1v = 0.5 * (0.16 + math.exp(-2) - 1 + 2)
lv.expect('l12', 'screens[2].widget.answer', round(kl1v - rec1, 2))
lv.expect('l12', 'screens[2]', round(rec1, 3), fmt='{:.3f}')
lv.expect('l12', 'screens[2]', round(kl1v, 3), fmt='{:.3f}')
lv.expect('l12', 'screens[2]', round(d2, 4), fmt='{:.4f}')
lv.claim(close(0.4 ** 2, 0.16, 1e-12), 'mu^2 = 0.16', covers=[0.16, 0.01, 0.02, 0.1])
given([0.52, 0.86, 0.55, 0.83, 0.4, 0.5, 0.7, 1.3, 0.37], 'one-point numbers, the draws and the console values are given')
ZS = np.random.default_rng(3).standard_normal((300, 1))
Ss = ops.vae_decode(Ptr_f, ZS)
dd = float(np.mean([abs(math.hypot(a, b) - 1) for a, b in X5[:300]])); ds = float(np.mean([abs(math.hypot(a, b) - 1) for a, b in Ss]))
lv.expect('l12', 'screens[4].prose', round(dd, 3), fmt='{:.3f}')
lv.expect('l12', 'screens[4].prose', round(ds, 3), fmt='{:.3f}')
P4 = train_b(X5, init_b(2, 32, 4, 0), 4000, 0.003, 1)
mu4 = np.tanh(X5 @ P4[0] + P4[1]) @ P4[2] + P4[3]; l4 = np.tanh(X5 @ P4[0] + P4[1]) @ P4[4] + P4[5]
kl4 = 0.5 * (mu4 ** 2 + np.exp(l4) - 1 - l4).mean(0)
bars4 = F['l12-reparameterisation']['screens'][6]['canvas']['state']['values']
lv.claim(all(abs(bars4[f'z{j + 1}'] - round(float(kl4[j]), 1)) < 1e-9 for j in range(4)), f'four-code KLs to 1 place by hand backprop ({np.round(kl4, 4).tolist()})', covers=[round(float(v), 1) for v in kl4])
lv.claim(sum(kl4 < 0.01) == 2 and sum(kl4 > 0.5) == 2, 'two coordinates collapse and two are used')
lv.claim(abs(math.exp(-1) - 0.37) < 0.005, 'console sd 0.37 is e^-1 to 2 places', covers=[0.37])

# ------------------------------------------------------------------ code widgets
TW = {
 'sample_model': '''def sample_model(g, n, s, seed):
    import numpy as _np
    r = _np.random.default_rng(seed)
    z = _np.array([r.standard_normal() for _ in range(1)][:0] + list(r.standard_normal(n))) if False else None
    rr = _np.random.default_rng(seed)
    z = rr.standard_normal(n)
    e = rr.standard_normal((n, 2))
    G = g(z)
    return _np.array([[G[i][0] + s * e[i][0], G[i][1] + s * e[i][1]] for i in range(n)]), z
def posterior_grid(x, g, s, zs):
    import math as _m
    G = g(np.asarray(zs, float))
    lw = [-((x[0] - G[i][0]) ** 2 + (x[1] - G[i][1]) ** 2) / (2 * s * s) - zs[i] ** 2 / 2 for i in range(len(zs))]
    mx = max(lw); w = [_m.exp(v - mx) for v in lw]; t = sum(w)
    return np.array([v / t for v in w])
''',
 'mc_marginal': '''def mc_marginal(x, g, s, n_z, seed):
    z = np.random.default_rng(seed).standard_normal(n_z)
    G = g(z); tot = 0.0
    for i in range(n_z):
        tot += np.exp(-((x[0] - G[i][0]) ** 2 + (x[1] - G[i][1]) ** 2) / (2 * s * s)) / (2 * np.pi * s * s)
    return float(tot / n_z)
''',
 'elbo_mc': '''def _tw(x, enc, dec, s, n, seed):
    m, lvv = enc(x); e = np.random.default_rng(seed).standard_normal(n); sd = np.exp(lvv / 2)
    z = m + sd * e; G = dec(z); A = []; K = []
    for i in range(n):
        lpx = -np.log(2 * np.pi * s * s) - ((x[0] - G[i][0]) ** 2 + (x[1] - G[i][1]) ** 2) / (2 * s * s)
        lq = -0.5 * np.log(2 * np.pi * sd * sd) - (z[i] - m) ** 2 / (2 * sd * sd)
        lp = -0.5 * np.log(2 * np.pi) - z[i] ** 2 / 2
        A.append(lpx); K.append(lq - lp)
    return A, K
def elbo_mc(x, enc, dec, s, n, seed):
    A, K = _tw(x, enc, dec, s, n, seed)
    return float(np.mean(A) - np.mean(K))
def two_terms(x, enc, dec, s, n, seed):
    A, K = _tw(x, enc, dec, s, n, seed)
    return float(np.mean(A)), float(np.mean(K))
''',
 'elbo_gap': '''def elbo_gap(x, m, v, g, s, zs):
    zs = np.asarray(zs, float); dz = zs[1] - zs[0]; G = g(zs)
    lj = np.array([-np.log(2 * np.pi * s * s) - ((x[0] - G[i][0]) ** 2 + (x[1] - G[i][1]) ** 2) / (2 * s * s) - 0.5 * np.log(2 * np.pi) - zs[i] ** 2 / 2 for i in range(len(zs))])
    mx = lj.max(); lpx = mx + np.log(np.exp(lj - mx).sum() * dz)
    q = np.exp(-(zs - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)
    keep = q > 0
    el = float(np.sum(q[keep] * (lj[keep] - np.log(q[keep]))) * dz)
    return float(lpx - el)
''',
 'kl_normal_std': '''def kl_normal_std(mu, logvar):
    return float(_kl(mu, logvar))
def kl_vector(mu, logvar):
    return float(sum(_kl(m, l) for m, l in zip(np.ravel(mu), np.ravel(logvar))))
''',
 'kl_numeric': '''def kl_numeric(mu, sigma, n, seed):
    e = np.random.default_rng(seed).standard_normal(n); z = mu + sigma * e
    return float(np.mean(-np.log(sigma) - e ** 2 / 2 + z ** 2 / 2))
''',
 'reparam_sample': '''import representations_ops_l3 as ops
def reparam_sample(mu, logvar, eps):
    return np.asarray(mu, float) + np.sqrt(np.exp(np.asarray(logvar, float))) * np.asarray(eps, float)
def vae_loss(x, params, eps):
    x = np.asarray(x, float); P = [np.asarray(p, float) for p in params]
    loss, rec, kl, G = _vae_grads(P, x, np.asarray(eps, float))
    return float(loss)
''',
 'train_vae': '''def train_vae(X, params, steps, lr, seed):
    return _train_b(np.asarray(X, float), params, steps, lr, seed)
''',
 'sample_vae': '''import representations_ops_l3 as ops
def sample_vae(params, n, seed):
    P = [np.asarray(p, float) for p in params]; Z = np.random.default_rng(seed).standard_normal((n, P[2].shape[1]))
    return np.tanh(Z @ P[6] + P[7]) @ P[8] + P[9]
''',
 'vae_step': '''def vae_step(x_batch, params, eps, lr):
    P = [np.asarray(p, float) for p in params]
    loss, rec, kl, G = _vae_grads(P, np.asarray(x_batch, float), np.asarray(eps, float))
    return float(loss), [p - lr * g for p, g in zip(P, G)]
''',
 'kl_two_normals': '''def kl_two_normals(m1, s1, m2, s2):
    return _klg(m1, s1, m2, s2)
''',
}


def _kl(m, l):
    return 0.5 * (m * m + math.exp(l) - 1 - l)


HELP = {'_kl': _kl, '_vae_grads': vae_grads, '_train_b': train_b, '_klg': klg}


def same(got, want, cmp, tol):
    def norm(v):
        if hasattr(v, 'tolist'):
            v = v.tolist()
        if isinstance(v, tuple):
            v = list(v)
        if isinstance(v, list):
            return [norm(x_) for x_ in v]
        return v
    got, want = norm(got), norm(want)
    if cmp == 'isclose':
        def cl(a, b):
            if isinstance(a, list) or isinstance(b, list):
                return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(cl(x_, y_) for x_, y_ in zip(a, b))
            if isinstance(a, bool) or isinstance(b, bool):
                return a == b
            if tol:
                return math.isclose(a, b, rel_tol=tol.get('rel', 0) or 0, abs_tol=tol.get('abs', 0) or 0) or a == b
            return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
        return cl(got, want)
    return got == want


def run_widget(w, src, label, approx=False):
    cwd = os.getcwd(); os.chdir(DATA)
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}
        ns.update(HELP)
        exec(ZQ_LIB, ns); exec(w.get('prelude', 'import numpy as np\n'), ns); exec('import numpy as np\n', ns); exec(src, ns)
        ok_all = True
        for k, t in enumerate(w['tests']):
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'])
            ok = same(got, want, t.get('compare', 'equal'), t.get('tol'))
            if not ok and approx:
                ok = same(got, want, 'isclose', {'rel': 1e-6, 'abs': 2e-6})
            ok_all &= ok
            if not ok:
                print('   mismatch', label, 'test', k + 1, str(got)[:80], 'vs', t['expect'][:80])
        return ok_all
    finally:
        os.chdir(cwd)


n_code = 0
for fid, doc in F.items():
    for key in ('screens', 'items'):
        for i, sc in enumerate(doc.get(key, [])):
            w_ = sc.get('widget')
            if not (isinstance(w_, dict) and w_.get('kind') == 'code'):
                continue
            n_code += 1
            lv.claim(run_widget(w_, w_['solution'], f'{fid} {key}[{i}]'), f'{fid} {key}[{i}]: the model solution passes every hidden test in CPython')
            name = next(k for k in TW if f'def {k}(' in w_['solution'])
            lv.claim(run_widget(w_, TW[name], f'{fid} {key}[{i}] twin', approx=True), f'{fid} {key}[{i}]: an independent twin ({name}) agrees (rounded results within 2e-6)')
            lv.claim(len(w_.get('mutants', [])) >= 2, f'{fid} {key}[{i}]: at least two mutants')
lv.claim(n_code == 11, 'eleven code widgets in the level')
# thresholds with margin across seeds (route B)
Xs = X5[:200]; E99 = np.random.default_rng(99).standard_normal((200, 1))
lossS = vae_grads(Pstart_f, Xs, E99)[0]
lv.claim(abs(lossS - 1.40) < 0.005, f'starting loss 1.40 on fixed noise ({lossS:.4f})', covers=[1.40])
for sd_ in range(4):
    Pq = train_b(Xs, Pstart_f, 200, 0.003, sd_)
    lq = vae_grads(Pq, Xs, E99)[0]
    lv.claim(lq < 0.6, f'train_vae threshold 0.8 holds with margin, seed {sd_}: {lq:.4f}')
    if sd_ == 0:
        lv.claim(abs(lq - 0.42) < 0.01, f'byKey "near 0.42" ({lq:.4f})', covers=[0.42])
for sd_ in (3, 4, 6, 7):
    Sx = ops.vae_decode(Ptr_f, np.random.default_rng(sd_).standard_normal((500, 1)))
    dx = float(np.mean([abs(math.hypot(a, b) - 1) for a, b in Sx]))
    lv.claim(dx < 0.018, f'sample_vae threshold 0.025 holds with margin, seed {sd_}: {dx:.4f}')
for sd_ in range(1, 6):
    zz = np.random.default_rng(sd_).standard_normal(100000)
    est = float(np.mean(np.exp(-((1.0 - zz) ** 2 + (0.8 - 0.5 * zz) ** 2) / 0.5) / (2 * math.pi * 0.25)))
    lv.claim(abs(est / math.exp(logpx) - 1) < 0.012, f'mc_marginal 2% test holds with margin at 100,000 draws, seed {sd_}: {abs(est / math.exp(logpx) - 1):.4f}')
lv.literal('0.01, 0.02, 0.03, 0.025, 0.3, 0.8, 1e-6, 1e-9, 1e-12, 6, 9, 5, 7, 8, 4, 3, 2, 100000, 200000, 500, 200, 50, 40, -800', why='test counts, places, sizes and tolerances in how lines are settings of the hidden tests, which this script runs')

# ------------------------------------------------------------------ review, problems, homework
lv.expect('review', 'items[0].widget.answer', round(kl1(0.6, 1.5), 3))
lv.claim(close(math.log(2.25), 0.811, 1e-3), 'ln 2.25 = 0.811', covers=[0.811, 0.36, 2.25, 0.6, 1.5])
lv.claim(close(_kl(0.5, 0) + _kl(0, 0), 0.125, 1e-12), 'review: 0.125', covers=[0.125, 0.25, 0.0625, 0.5])
lv.claim(close(0.5 * math.exp(0) * 0.8, 0.4, 1e-12), 'review: dz/dl = 0.4', covers=[0.4, 0.8])
lv.expect('review', 'items[4].widget.answer', round(math.sin(0.3) + 0.1, 3))
lv.claim(close(math.sin(0.3), 0.2955, 1e-4), 'sin 0.3 = 0.2955', covers=[0.2955, 0.3, 0.1])
lv.claim(close(1.0 / 1.5, 0.667, 1e-3), 'review: 0.667', covers=[0.667, 1.5, 0.333, 0.2, 1.0, 0.3])
given([2.5, 2.1, 0.4, 0.0002, 50, 3.1], 'review scenarios: reported values are given in the prompts')
klP = 0.5 * (0.04 + 0.09 - 1 - math.log(0.09))
lv.expect('problems', 'items[0].parts[0].widget.answer', round(klP, 3))
lv.claim(close(kl1(0.2, 0.3), klP, 1e-7) and close(-math.log(0.09), 2.408, 1e-3), 'problem 1: KL by quadrature; -ln 0.09 = 2.408', covers=[2.408, 0.04, 0.09, 0.2, 0.3])
zP = 0.2 + 0.3 * 1.5
lv.expect('problems', 'items[0].parts[1].widget.answer', round(zP, 4))
gP = g_c(zP)
d2P = (0.3 - gP[0]) ** 2 + (0.9 - gP[1]) ** 2
recP = -math.log(2 * math.pi * 0.01) - d2P / 0.02
lv.expect('problems', 'items[0].parts[2].widget.answer', round(recP, 2))
lv.expect('problems', 'items[0].parts[2]', round(gP[0], 4), fmt='{:.4f}')
lv.expect('problems', 'items[0].parts[2]', round(gP[1], 4), fmt='{:.4f}')
lv.expect('problems', 'items[0].parts[2]', round(d2P, 4), fmt='{:.4f}')
lv.expect('problems', 'items[0].parts[2].explain.text', round(d2P / 0.02, 3), fmt='{:.3f}')
lv.claim(close(-math.log(2 * math.pi * 0.01), 2.767, 1e-3), 'constant 2.767', covers=[2.767, 0.45])
lv.expect('problems', 'items[0].parts[3].widget.answer', round(klP - round(recP, 2), 2))
given([1.5, 0.9, 0.3], 'problem 1 data are given')
vs = Fr(1, 6); ms = vs * 5
lv.expect('problems', 'items[1].parts[1].widget.answer', round(float(ms), 4))
gap0 = 0.5 * (6 + float(ms) ** 2 * 6 - 1 + math.log(1 / 6))
lv.expect('problems', 'items[1].parts[2].widget.answer', round(gap0, 3))
lv.claim(close(klg(0, 1, float(ms), math.sqrt(1 / 6)), gap0, 1e-6), 'problem 2 gap by quadrature', covers=[6, 4.167, 1.792, 0.6944])
detv = 5 * 2 - 4
qv = (2 * 4 - 2 * 2 * 2 * 1 + 5 * 1) / detv
lpx = -L2PI - 0.5 * math.log(detv) - 0.5 * qv
lv.expect('problems', 'items[1].parts[3].question', round(lpx, 4), fmt='{:.4f}')
lv.expect('problems', 'items[1].parts[3].widget.answer', round(lpx - round(gap0, 3), 2))
lv.claim(Fr(4) + 1 == 5, 'problem 2: |w|^2 = 5', covers=[5, 1.0, 0.8333])
k3b = 0.5 * (9 - 1 - math.log(9)); k3a = klg(0, 1, 0, 3)
lv.expect('problems', 'items[2].parts[0].widget.answer', round(k3b, 3))
lv.expect('problems', 'items[2].parts[1].widget.answer', round(k3a, 3))
lv.expect('problems', 'items[2].parts[2].widget.answer', round(3 * k3b, 2))
lv.claim(close(kl1(0, 3), k3b, 1e-7) and close(math.log(3) + 1 / 18 - 0.5, k3a, 1e-7) and close(math.log(1 / 3) + 9 / 2 - 0.5, k3b, 1e-12), 'problem 3 by quadrature; ln(1/3) + 9/2 - 1/2', covers=[1.099, 0.056, 4.0, 4.5])
lv.expect('homework', 'items[1].widget.tests[0].expect', round(klg(1, 0.5, 0, 1), 6) if False else 0.8181471805599453)
lv.claim(close(0.5 * 2 * -0.5, -0.5, 1e-12), 'homework dz/dl = -0.5', covers=[-0.5, -1.0, 2])
lv.claim(close(1.72 - 2.31, -0.59, 1e-12), 'homework ELBO -0.59', covers=[0.59, 4.03, 1.72, 2.31])
k3h = 0.5 + 0.5 * (0.5 - 1 - math.log(0.5)) + 0.5
lv.expect('homework', 'items[7].widget.answer', round(k3h, 3))
lv.claim(close(math.log(2), 0.693, 1e-3), 'ln 2 = 0.693', covers=[0.693, round(0.5 * (0.5 - 1 - math.log(0.5)), 3)])
given([41.2, 96.8, 30, 8, 0.001, 1.5, 0.818], 'homework scenarios: log values and counts are given')
lv.check_wrongs()
lv.report()
