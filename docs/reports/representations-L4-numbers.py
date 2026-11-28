"""representations level 4 (Diffusion): every stated number recomputed by a second route.

Route A is the generator (NumPy, the autograd, nt_ops_l1.adam_step). Route B here is independent: schedules by sums
of logs instead of running products, Fractions for the small cases, every noise predictor retrained with a
hand-written backward pass and a hand-written Adam, and its own forward pass and sampler. Long training runs are
compared with thresholds and with the stated rounding, never to more places than both routes agree on. Every code
widget's hidden tests are rerun in CPython with the model solution and with an independent twin. Run through
`node tools/run-number-scripts.mjs --only representations-L4` (one BLAS thread); strict coverage.
"""
import json, math, os, sys, hashlib
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from scipy.optimize import brentq
from numbers_lib import Level, ZQ_LIB
from autograd import Tensor, grad_check
import representations_ops_l4 as ops

lv = Level("representations", 4, coverage="strict")
F = lv.files


def given(vals, why):
    for v in vals:
        lv.literal(str(v), why=why)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def sha(name):
    return hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest()


lv.claim(sha('autograd.py').startswith('5917d4ec91f7') and sha('nt_ops_l1.py').startswith('9c1391a33624'), 'autograd.py and nt_ops_l1.py byte-identical to the frozen v1.0')


def abar_logs(betas):
    return np.exp(np.cumsum(np.log1p(-np.asarray(betas, float))))


# ------------------------------------------------------------------ module checks
Pg = [Tensor(p + 0.05 * np.random.default_rng(1).standard_normal(np.shape(p))) for p in ops.init_denoiser(6, 2)]
Xg = ops.two_rings(10, 3); tg = np.arange(1, 11)
gerr = grad_check(lambda: ((ops.eps_model(Pg, Xg, tg, 50) - 0.5) ** 2).sum() / 10, Pg)
lv.claim(gerr < 1e-6, f'eps_model through the autograd: gradient check, relative error {gerr:.1e}')
g0 = np.random.default_rng(4); th = g0.uniform(0, 2 * np.pi, 4); rr = np.array([0.8, 1.6, 0.8, 1.6])
lv.claim(np.allclose(ops.two_rings(4, 4), np.c_[rr * np.cos(th), rr * np.sin(th)] + 0.03 * g0.standard_normal((4, 2)), atol=0), 'two_rings: angles then noise, even rows inner')
X2k = ops.two_rings(20000, 9)
lv.claim(abs(X2k.var(0).mean() - 0.8) < 0.02, 'ring data: variance about 0.8 per coordinate', covers=[0.8])

# ------------------------------------------------------------------ hand-backprop trainer and sampler (route B)
def fwd_b(P, X, t, T):
    W1, w1t, b1, W2, b2, W3, b3 = P
    u = (np.broadcast_to(np.asarray(t, float), (len(X),)) / T)[:, None]
    a1 = X @ W1 + u @ w1t + b1; h1 = np.maximum(a1, 0)
    a2 = h1 @ W2 + b2; h2 = np.maximum(a2, 0)
    return h2 @ W3 + b3, (u, a1, h1, a2, h2)


def adam_b(p, g, st, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m, v = st
    m[:] = b1 * m + (1 - b1) * g
    v[:] = b2 * v + (1 - b2) * g * g
    return p - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps)


def train_b(X0, P0, betas, steps, lr, seed, notime=False, trace=False):
    T = len(betas); ab = abar_logs(betas)
    P = [np.array(p, float) for p in P0]
    sts = [(np.zeros_like(p), np.zeros_like(p)) for p in P]
    g = np.random.default_rng(seed); tr = []
    for step in range(1, steps + 1):
        idx = g.integers(0, len(X0), 256); tt = g.integers(1, T + 1, 256); e = g.standard_normal((256, 2))
        a = ab[tt - 1][:, None]
        xt = np.sqrt(a) * X0[idx] + np.sqrt(1 - a) * e
        out, (u, a1, h1, a2, h2) = fwd_b(P, xt, np.zeros(256) if notime else tt, T)
        tr.append(float(((out - e) ** 2).sum() / 256))
        d = 2 * (out - e) / 256
        gW3, gb3 = h2.T @ d, d.sum(0)
        da2 = (d @ P[5].T) * (a2 > 0)
        gW2, gb2 = h1.T @ da2, da2.sum(0)
        da1 = (da2 @ P[3].T) * (a1 > 0)
        G = [xt.T @ da1, u.T @ da1, da1.sum(0), gW2, gb2, gW3, gb3]
        P = [adam_b(p, gg, st, step, lr) for p, gg, st in zip(P, G, sts)]
    return (P, tr) if trace else P


def sample_b(P, betas, n, seed, noise=True, upward=False):
    T = len(betas); ab = abar_logs(betas); g = np.random.default_rng(seed)
    x = g.standard_normal((n, 2)); frames = {T: x.copy()}
    order = range(1, T + 1) if upward else range(T, 0, -1)
    for t in order:
        e = fwd_b(P, x, t, T)[0]
        x = (x - betas[t - 1] / np.sqrt(1 - ab[t - 1]) * e) / np.sqrt(1 - betas[t - 1])
        if noise and ((t > 1) if not upward else (t < T)):
            x = x + np.sqrt(betas[t - 1]) * g.standard_normal((n, 2))
        frames[t - 1] = x.copy()
    return x, frames


def share_b(S, radii=(0.8, 1.6), band=0.1):
    r = np.hypot(S[:, 0], S[:, 1])
    return float(np.mean([min(abs(x - c) for c in radii) < band for x in r]))


X0 = ops.two_rings(2000, 0)
b50 = ops.linear_schedule(50)
ab50 = abar_logs(b50)
lv.claim(np.allclose(ab50, np.cumprod(1 - b50), rtol=1e-12), 'abar by sum of logs equals the running product')
FD = json.load(open(os.path.join(DATA, 'representations-l15-denoiser.json')))
Pst_f = [np.array(a) for a in FD['start']]; Ptr_f = [np.array(a) for a in FD['trained']]
Pb1, tr1 = train_b(X0, ops.init_denoiser(64, 0), b50, 300, 2e-3, 1, trace=True)
d1 = max(float(np.abs(a - b).max()) for a, b in zip(Pb1, Pst_f))
lv.claim(d1 < 1e-5, f'starting weights: 300 hand-backprop steps reproduce the file to {d1:.1e}', covers=[300, 0.002, 256])
Pb2, tr2 = train_b(X0, Pst_f, b50, 11700, 2e-3, 2, trace=True)
d2 = max(float(np.abs(a - b).max()) for a, b in zip(Pb2, Ptr_f))
lv.claim(d2 < 1e-2, f'trained weights: 11,700 more hand-backprop steps stay within {d2:.1e} of the file (a long run: compared loosely)', covers=[12000, 11700, 64])
crv = tr1 + tr2
sm = [float(np.mean(crv[i:i + 100])) for i in range(0, len(crv), 100)]
lv.claim(max(abs(a - b) for a, b in zip(sm, FD['loss_per_100'])) < 0.02, 'recorded loss curve reproduced within 0.02')

# ------------------------------------------------------------------ l13
l13 = F['l13-adding-noise']
lv.expect('l13', 'screens', round(float(ab50[-1]), 4), fmt='{:.4f}')
lv.expect('l13', 'screens[0].explain.text', round(math.sqrt(ab50[-1]), 3), fmt='{:.3f}')
X3 = ops.two_rings(300, 3); E3 = np.random.default_rng(4).standard_normal((300, 2))
fr = l13['screens'][0]['canvas']['controls'][0]['frames']
ok = True
for k, t in enumerate([0, 5, 10, 20, 30, 50]):
    if t:
        a = ab50[t - 1]; pt = math.sqrt(a) * X3[7] + math.sqrt(1 - a) * E3[7]
        ok &= abs(fr[k]['points']['p7']['x'] - pt[0]) < 1e-3
        lv.expect('l13', f'screens[0].canvas.controls[0].frames[{k}].caption', round(float(a), 3), fmt='{:.3f}')
lv.claim(ok, 'noised frames follow the closed form (spot check of point 7)')
x1 = (math.sqrt(0.8) * 1.6 + math.sqrt(0.2) * 0.5, -math.sqrt(0.2))
lv.expect('l13', 'screens[1].widget.rows[0][1].answer', round(x1[0], 4))
lv.expect('l13', 'screens[1].widget.rows[1][1].answer', round(x1[1], 4))
lv.expect('l13', 'screens[1].widget.rows[0][1].wrong[0].value', round(1.6 + math.sqrt(0.2) * 0.5, 4))
lv.claim(close(math.sqrt(0.8), 0.8944, 1e-4) and close(math.sqrt(0.2), 0.4472, 1e-4), 'roots 0.8944 and 0.4472; pieces 1.431, 0.224, 0.447', covers=[0.8944, 0.4472, 1.431, 0.224, 0.447, 0.2, 0.5, 1.6])
lv.claim(Fr(9, 10) * Fr(8, 10) * Fr(7, 10) == Fr(504, 1000), 'toy schedule: 0.504; 0.72', covers=[0.504, 0.72, 0.9, 0.8, 0.7, 0.1, 0.3, 0.4])
bho = np.linspace(1e-4, 0.02, 1000); aho = abar_logs(bho)
lv.expect('l13', 'screens[4].prose', round(float(aho[499]), 4), fmt='{:.4f}')
lv.expect('l13', 'screens[4].prose', round(float(aho[999]) * 1e5, 1), fmt='{:.1f}')
lv.expect('l13', 'screens[4].widget.answer', round(math.sqrt(aho[499]), 2))
lv.expect('l13', 'screens[4].explain.text', round(math.sqrt(aho[999]), 4), fmt='{:.4f}')
lv.claim(abs(aho[499] - 0.0786) < 5e-5 and abs(aho[999] - 4.0e-5) < 5e-7, 'Ho et al.: 0.0786 and 4.0e-5, as the brief quotes', covers=[1000, 500, 0.02, 4.0e-5, 1e-4])
lv.expect('l13', 'screens[5].widget.answer', round(math.sqrt(ab50[-1]), 3))
lv.expect('l13', 'screens[5].explain.text', round(math.sqrt(1 - ab50[-1]), 3), fmt='{:.3f}')
lv.claim(abs(ab50[-1] - 0.0045) < 5e-5, 'our schedule: 0.0045, as the brief quotes', covers=[0.0045])
v20 = ab50[19] * 0.8 + 1 - ab50[19]
lv.expect('l13', 'screens[6].widget.answer', round(v20, 2))
lv.expect('l13', 'screens[6].prose', round(float(ab50[19]), 4), fmt='{:.4f}')
lv.expect('l13', 'screens[6].hints[1].text', round(1 - float(ab50[19]), 4), fmt='{:.4f}')
sb = sum(Fr(1, 1000) + Fr(199, 1000) * Fr(i, 49) for i in range(50))
lv.claim(sb == Fr(5025, 1000), 'the 50 betas add up to 5.025 (Fractions)', covers=[5.025])
lv.expect('l13', 'screens[7].widget.answer', round(0.8 + float(sb), 3))
lv.expect('l13', 'screens[8].widget.answer', round(0.99 ** 50, 3))
lv.claim(close(math.exp(50 * math.log(0.99)), 0.99 ** 50, 1e-12), '0.99^50 by logs', covers=[0.01, 0.99])
given([0.8, 1.6, 0.03, 300, 20000, 0.05, 1e-3, 0.2], 'ring radii, noise, point counts and schedule ends are settings')
lv.claim(close(0.95 * 0.9 * 0.8, 0.684, 1e-12), 'quiz 0.684; slip 0.65', covers=[0.684, 0.65, 0.95, 0.05])
lv.claim(close(math.sqrt(0.36), 0.6, 1e-12) and close(math.sqrt(0.64), 0.8, 1e-12), 'quiz 0.6 and 0.8', covers=[0.6, 0.36, 0.64])

# ------------------------------------------------------------------ l14
a20 = float(ab50[19])
lv.expect('l14', 'screens[0].prose', round(a20, 3), fmt='{:.3f}')
def lik(xt, x0, a):
    d2 = sum((xt[i] - math.sqrt(a) * x0[i]) ** 2 for i in range(2))
    return math.exp(-d2 / (2 * (1 - a)))
ratio = lik((0.55, 0.35), (0.8, 0), a20) / lik((0.55, 0.35), (0, 1.6), a20)
lv.claim(round(ratio) == 2 and ratio > 1, f'A is about 2 times as likely as B ({ratio:.3f})', covers=[2])
lv.expect('l14', 'screens[0].hints[1].text', round(math.sqrt(a20), 3), fmt='{:.3f}')
lv.expect('l14', 'screens[0].widget.options', round(math.sqrt(1 - a20), 2), fmt='{:.2f}')
lv.expect('l14', 'screens[0].hints[1].text', round(math.sqrt(a20) * 0.8, 2), fmt='{:.2f}')
lv.expect('l14', 'screens[0].hints[1].text', round(math.sqrt(a20) * 1.6, 2), fmt='{:.2f}')
given([0.55, 0.35], 'the noised point is given')
lv.claim(close(0.2 ** 2 + 0.3 ** 2, 0.13, 1e-12), 'loss 0.13 = 0.04 + 0.09', covers=[0.13, 0.04, 0.09, 0.065, 0.3, 1.2, 0.9])
xt2 = (math.sqrt(a20) * 1.6 + math.sqrt(1 - a20) * 0.5, -math.sqrt(1 - a20))
lv.expect('l14', 'screens[2].widget.rows[0][1].answer', round(xt2[0], 4))
lv.expect('l14', 'screens[2].widget.rows[1][1].answer', round(xt2[1], 4))
lv.expect('l14', 'screens[2].widget.rows[0][1].wrong[0].value', round(a20 * 1.6 + (1 - a20) * 0.5, 4))
lv.expect('l14', 'screens[2]', round(a20, 4), fmt='{:.4f}')
lv.expect('l14', 'screens[2].hints[1].text', round(math.sqrt(a20), 3), fmt='{:.3f}')
lv.expect('l14', 'screens[2].hints[1].text', round(math.sqrt(1 - a20), 3), fmt='{:.3f}')
lv.claim(close(math.sqrt(a20) ** 2, a20, 1e-12) and close(math.sqrt(1 - a20) ** 2, 1 - a20, 1e-12), 'roots of abar_20 and 1 - abar_20', covers=[round(math.sqrt(a20), 4), round(math.sqrt(1 - a20), 4), round(1 - a20, 4)])
lend = float(np.mean(FD['loss_per_100'][-10:]))
lv.claim(abs(float(np.mean(sm[-10:])) - lend) < 0.02, f'loss settles near {lend:.2f} by both routes', covers=[round(lend, 1), round(lend, 2), round(FD['loss_per_100'][0], 1)])
XT = ops.two_rings(4000, 7); ts = [1, 5, 10, 20, 30, 40, 50]
lt = []
for t in ts:
    gg = np.random.default_rng(100 + t); ee = gg.standard_normal(XT.shape)
    xx = math.sqrt(ab50[t - 1]) * XT + math.sqrt(1 - ab50[t - 1]) * ee
    lt.append(float(((fwd_b(Ptr_f, xx, t, 50)[0] - ee) ** 2).sum(1).mean()))
bars = F['l14-predict-the-noise']['screens'][4]['canvas']['state']['values']
lv.claim(all(abs(bars[str(t)] - round(v, 3)) < 2e-3 for t, v in zip(ts, lt)), 'loss by step, by an independent forward pass', covers=[4000] + [round(v, 2) for v in lt])
lv.expect('l14', 'screens[4]', round(math.sqrt(1 - ab50[0]), 3), fmt='{:.3f}')
trno = train_b(X0, ops.init_denoiser(64, 0), b50, 12000, 2e-3, 2, notime=True, trace=True)[1]
lno = float(np.mean(trno[-1000:]))
stated_no = float(F['l14-predict-the-noise']['screens'][5]['prose'].split('is ')[1].split(',')[0])
lv.claim(abs(lno - stated_no) < 0.02 and lno - lend > 0.1, f'no-time loss {lno:.3f} by hand backprop against the stated {stated_no}; the gap holds', covers=[stated_no, round(lend, 2), round(stated_no - round(lend, 2), 2)])
lv.claim(np.std(trno[-1000:]) / math.sqrt(1000) < 0.01, 'batch-to-batch wobble of the average about 0.01 or less', covers=[0.01])
given([0.02, 0.6, 0.0, 1.0, 0.25, 0.7, 0.125], 'l14 quiz values and the plain-number slips are given in the prompts')

# ------------------------------------------------------------------ l15
Sb, frb = sample_b(Ptr_f, b50, 1000, 5)
shares = {t: share_b(frb[t]) for t in (50, 30, 20, 10, 5, 0)}
lv.claim(abs(shares[0] - 0.704) <= 0.002, f'ring share of 1,000 samples {shares[0]:.3f} (stated 0.70 and 0.704)', covers=[0.70, 0.704, 1000])
lv.claim(abs(shares[20] - 0.242) <= 0.003, 'share at step 20 about 0.24', covers=[0.24])
t1 = 10; b10 = b50[t1 - 1]; a10 = ab50[t1 - 1]
mean1 = [(v - b10 / math.sqrt(1 - a10) * e) / math.sqrt(1 - b10) for v, e in ((0.9, 0.3), (0.2, -0.5))]
xp = [m + math.sqrt(b10) * z for m, z in zip(mean1, (0.1, 0.4))]
lv.expect('l15', 'screens[1].widget.rows[0][1].answer', round(xp[0], 4))
lv.expect('l15', 'screens[1].widget.rows[1][1].answer', round(xp[1], 4))
lv.expect('l15', 'screens[1].widget.rows[0][1].wrong[0].value', round(mean1[0], 4))
lv.expect('l15', 'screens[1].prose', round(b10, 5), fmt='{:.5f}')
lv.expect('l15', 'screens[1].prose', round(a10, 5), fmt='{:.5f}')
lv.expect('l15', 'screens[1].hints[0].text', round(b10 / math.sqrt(1 - a10), 4), fmt='{:.4f}')
lv.expect('l15', 'screens[1].hints[0].text', round(1 / math.sqrt(1 - b10), 4), fmt='{:.4f}')
lv.expect('l15', 'screens[1].hints[1].text', round(math.sqrt(b10), 4), fmt='{:.4f}')
lv.expect('l15', 'screens[1].explain.text', round(mean1[1], 3), fmt='{:.3f}')
lv.expect('l15', 'screens[1].explain.text', round(mean1[0], 3), fmt='{:.3f}')
base = sum(math.exp(-lo * lo / 1.6) - math.exp(-hi * hi / 1.6) for lo, hi in ((0.7, 0.9), (1.5, 1.7)))
lv.expect('l15', 'screens[2].widget.answer', round(base, 2) if False else round(shares[0], 2))
lv.expect('l15', 'screens[2].widget.wrong[0].value', round(base, 2))
lv.claim(abs(base - 0.214) < 0.001, 'round normal baseline 0.21 (Rayleigh)', covers=[0.21, 0.214, 0.1])
Snn = sample_b(Ptr_f, b50, 1000, 5, noise=False)[0]
o_nn = float(np.mean(np.hypot(Snn[:, 0], Snn[:, 1]) > 1.2)); o_s = float(np.mean(np.hypot(Sb[:, 0], Sb[:, 1]) > 1.2))
lv.claim(o_nn < 0.005 and abs(o_s - 0.501) < 0.005, f'without the noise {100 * o_nn:.0f}% reach the outer ring, with it {100 * o_s:.0f}%', covers=[0, 50])
Sup = sample_b(Ptr_f, b50, 1000, 5, upward=True)[0]
lv.claim(abs(share_b(Sup) - 0.219) <= 0.003, f'upward chain share {share_b(Sup):.3f}', covers=[0.22])
for start, want in (((3.5, 3.5), 1.68), ((0.0, 0.0), 1.67)):
    gg = np.random.default_rng(9); x = np.array([start], float)
    for t in range(50, 0, -1):
        e = fwd_b(Ptr_f, x, t, 50)[0]
        x = (x - b50[t - 1] / np.sqrt(1 - ab50[t - 1]) * e) / np.sqrt(1 - b50[t - 1])
        if t > 1:
            x = x + np.sqrt(b50[t - 1]) * gg.standard_normal(x.shape)
    lv.claim(abs(math.hypot(*x[0]) - want) < 0.006, f'tail run from {start} ends at radius {math.hypot(*x[0]):.3f}', covers=[want])
lv.claim(close(math.hypot(3.5, 3.5), 4.95, 1e-3), 'the two starts are 4.9 apart', covers=[4.9, 3.5])
lv.expect('l15', 'screens[5].explain.text', round(math.sqrt(ab50[-1]), 3), fmt='{:.3f}')
qm = (1.0 - 0.19 / 0.6 * 0.4) / 0.9
lv.expect('l15', 'quiz[0].widget.answer', round(qm, 3))
lv.claim(close(0.19 / 0.6 * 0.4, 0.1267, 1e-3), 'quiz piece 0.1267', covers=[0.1267, 0.19, 0.64, 0.6, 0.9])
given([0.55, 0.3, 0.7, 2.0, 0.85, 1.65, 1.5, 0.5, 5.0, 0.01, 1.0], 'how-line thresholds and code-test inputs are settings of the hidden tests, which this script runs')

# ------------------------------------------------------------------ l16: retrain the other schedules by hand backprop
end = float(ab50[-1])
def matched_b(T):
    if T == 1:
        return np.array([1 - end])
    b1 = 1e-3 * 50 / T
    bt = brentq(lambda x: float(np.sum(np.log1p(-np.linspace(b1, x, T)))) - math.log(end), b1, 0.999)
    return np.linspace(b1, bt, T)


sh = {50: shares[0]}
for T in (1, 10, 200):
    bT = matched_b(T)
    lv.claim(abs(float(abar_logs(bT)[-1]) - end) < 1e-9, f'T = {T}: matched schedule ends at abar {end:.4f}')
    PT = train_b(X0, ops.init_denoiser(64, 0), bT, 12000, 2e-3, 2)
    sh[T] = share_b(sample_b(PT, bT, 1000, 5)[0])
stated = {1: 0.006, 10: 0.547, 50: 0.704, 200: 0.814}
for T in stated:
    lv.claim(abs(sh[T] - stated[T]) <= 0.01, f'ring share at T = {T}: hand backprop {sh[T]:.3f} against stated {stated[T]} (long runs: within 0.01)', covers=[stated[T], round(stated[T], 2)])
lv.claim(sh[1] < sh[10] < sh[50] < sh[200], 'shares rise with T in this toy', covers=[1, 10, 50, 200])
lv.claim(abs((stated[200] - stated[50]) - 0.11) < 0.005 and abs((stated[50] - stated[10]) - 0.16) < 0.005, 'gains 0.11 and 0.16', covers=[0.11, 0.16, round(stated[200] / stated[50], 2)])
snr50 = end / (1 - end)
lv.expect('l16', 'screens[1].widget.answer', round(snr50, 4))
lv.expect('l16', 'screens[1].widget.wrong[0].value', round(1 / snr50, 4))
lv.expect('l16', 'screens[2].widget.answer', round(0.9 ** 10, 3))
lv.claim(close(math.exp(10 * math.log(0.9)), 0.9 ** 10, 1e-12), '0.9^10 by logs; about 0.35', covers=[0.35])
lv.expect('l16', 'screens[2].canvas.params.rows[2][1]', round(float(abar_logs(matched_b(200))[-1]), 4))
lv.expect('l16', 'screens[7].widget.answer', round(math.sqrt(0.99 ** 50), 3))
lv.expect('l16', 'screens[7].prose', round(0.99 ** 50, 3), fmt='{:.3f}')
lv.claim(close(0.2 / 0.8, 0.25, 1e-12) and 200 / 50 == 4, 'quiz 0.25, 4 times', covers=[0.25, 4.0, 4, 0.2, 0.8, 0.3])
lv.literal('1,000', why='the 1,000-step proposal in the trap is a scenario figure')
lv.claim(1000 / 200 == 5 and 200 / 10 == 20, 'five times 200, 20 times 10', covers=[5, 20])
lv.claim(len(F['l16-the-schedule']['screens'][0]['canvas']['params']['points']) == 300, '300 samples shown', covers=[300])

# ------------------------------------------------------------------ code widgets
TW = {
 'alpha_bar': '''def alpha_bar(betas):
    return np.exp(np.cumsum(np.log1p(-np.asarray(betas, float))))
def noise_step(x, beta, eps):
    return np.array([np.sqrt(1 - beta) * a + np.sqrt(beta) * b for a, b in zip(np.ravel(x), np.ravel(eps))]).reshape(np.shape(x))
''',
 'noise_to': '''def noise_to(x0, t, abar, eps):
    a = list(abar)[t - 1]
    return np.sqrt(a) * np.asarray(x0, float) + np.sqrt(1 - a) * np.asarray(eps, float)
''',
 'make_batch': '''def make_batch(X0, abar, n, seed):
    r = np.random.default_rng(seed); X0 = np.asarray(X0, float); abar = np.asarray(abar, float)
    i = r.integers(0, len(X0), n); t = r.integers(1, len(abar) + 1, n); e = r.standard_normal((n, 2))
    out = np.array([np.sqrt(abar[t[k] - 1]) * X0[i[k]] + np.sqrt(1 - abar[t[k] - 1]) * e[k] for k in range(n)])
    return out, t, e
''',
 'noise_loss': '''def noise_loss(params, xt, t, eps, T=50):
    out = _fwd(params, np.asarray(xt, float), np.asarray(t), T)[0]
    return float(np.mean([((np.asarray(e) - o) ** 2).sum() for e, o in zip(eps, out)]))
''',
 'train_denoiser': '''def train_denoiser(X0, params, abar, steps, lr, seed):
    abar = np.asarray(abar, float); betas = 1 - abar / np.concatenate([[1.0], abar[:-1]])
    return _train(np.asarray(X0, float), params, betas, steps, lr, seed)
''',
 'reverse_step': '''def reverse_step(x, t, params, betas, abar, z):
    x = np.asarray(x, float); e = _fwd(params, x, t, len(betas))[0]
    m = (x - betas[t - 1] / np.sqrt(1 - abar[t - 1]) * e) / np.sqrt(1 - betas[t - 1])
    return m + (np.sqrt(betas[t - 1]) * np.asarray(z, float) if t > 1 else 0)
''',
 'sample': '''def sample(params, betas, n, seed):
    return _sample(params, np.asarray(betas, float), n, seed)[0]
''',
 'ring_share': '''def ring_share(S, radii, band):
    import math as _m
    c = 0
    for x, y in S:
        r = _m.hypot(x, y)
        c += any(abs(r - q) < band for q in radii)
    return c / len(S)
''',
 'linear_betas': '''def linear_betas(b1, bT, T):
    return np.array([b1 + (bT - b1) * k / (T - 1) if T > 1 else b1 for k in range(T)])
def snr(abar):
    return np.array([a / (1 - a) for a in np.ravel(abar)])
''',
 'end_gap': '''def end_gap(abar):
    a = list(abar)[-1]
    return float(a), float(a) ** 0.5
''',
 'ddpm_sampler': '''def ddpm_sampler(eps_model, betas, n, seed):
    betas = np.asarray(betas, float); ab = np.exp(np.cumsum(np.log1p(-betas))); r = np.random.default_rng(seed)
    x = r.standard_normal((n, 2))
    for t in range(len(betas), 0, -1):
        e = np.asarray(eps_model(x, t), float)
        x = (x - betas[t - 1] / np.sqrt(1 - ab[t - 1]) * e) / np.sqrt(1 - betas[t - 1])
        if t > 1:
            x = x + np.sqrt(betas[t - 1]) * r.standard_normal((n, 2))
    return x
''',
 'steps_to_noise': '''def steps_to_noise(betas, thresh):
    a = 1.0
    for k, b in enumerate(betas):
        a *= (1 - b)
        if a < thresh:
            return k + 1
    return None
''',
}
HELP = {'_fwd': fwd_b, '_train': train_b, '_sample': sample_b}


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
            want = eval(t['expect'], {'None': None})
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
lv.claim(n_code == 12, 'twelve code widgets in the level')
# thresholds with margin across seeds (route B)
XB = ops.two_rings(4000, 11)
gb = np.random.default_rng(12); ib = gb.integers(0, 4000, 4000); tb = gb.integers(1, 51, 4000); eb = gb.standard_normal((4000, 2))
xb = np.sqrt(ab50[tb - 1])[:, None] * XB[ib] + np.sqrt(1 - ab50[tb - 1])[:, None] * eb
linit = float(((fwd_b(ops.init_denoiser(64, 0), xb, tb, 50)[0] - eb) ** 2).sum(1).mean())
lv.claim(abs(linit - 2.3) < 0.05, f'the untrained net scores about 2.3 on the fixed batch ({linit:.3f})', covers=[2.3])
for sd in range(4):
    Pq = train_b(X0, ops.init_denoiser(64, 0), b50, 120, 2e-3, sd)
    lq = float(((fwd_b(Pq, xb, tb, 50)[0] - eb) ** 2).sum(1).mean())
    lv.claim(lq < 0.77, f'train_denoiser threshold 0.8 after 120 steps holds with margin, seed {sd}: {lq:.3f}')
for sd in (5, 6, 7, 8):
    S_ = sample_b(Ptr_f, b50, 1000, sd)[0]
    o_ = float(np.mean(np.hypot(S_[:, 0], S_[:, 1]) > 1.2))
    lv.claim(share_b(S_) > 0.62 and 0.38 < o_ < 0.62, f'sample thresholds (share 0.55, outer 30% to 70%) hold with margin, seed {sd}')
def gauss_eps(mu, s, betas):
    ab = abar_logs(betas); mu = np.asarray(mu, float)
    return lambda x, t: np.sqrt(1 - ab[t - 1]) * (x - np.sqrt(ab[t - 1]) * mu) / (ab[t - 1] * s * s + 1 - ab[t - 1])
nsd = {}
exec('import numpy as np\n' + TW['ddpm_sampler'], nsd)
for sd in (4, 14, 24):
    B = np.linspace(1e-3, 0.1, 100)
    S_ = nsd['ddpm_sampler'](gauss_eps([1.0, -1.0], 0.5, B), B, 20000, sd)
    lv.claim(np.all(np.abs(S_.mean(0) - [1, -1]) < 0.03) and np.all(np.abs(S_.std(0) - 0.5) < 0.03), f'Gaussian planted check (0.05) holds with margin, seed {sd}')
    B2 = np.linspace(1e-3, 0.06, 150)
    S_ = nsd['ddpm_sampler'](gauss_eps([0.0, 2.0], 0.8, B2), B2, 20000, sd + 1)
    lv.claim(np.all(np.abs(S_.mean(0) - [0, 2]) < 0.05) and np.all(np.abs(S_.std(0) - 0.8) < 0.05), f'second Gaussian check (0.08) holds with margin, seed {sd + 1}')
lv.literal('6, 9, 12, 5, 4, 3, 2, 0.05, 0.08, 0.8, 1e-9, 20,000, 4,000, 300, 120', why='test counts, places, sample sizes and tolerances in how lines are settings of the hidden tests, which this script runs')

# ------------------------------------------------------------------ review, problems, homework
lv.claim(Fr(8, 10) * Fr(75, 100) * Fr(5, 10) == Fr(3, 10), 'review: 0.3', covers=[0.3, 0.05, 0.5, 0.2, 0.25, 0.8, 0.75])
lv.claim(close(math.sqrt(0.49), 0.7, 1e-12), 'review: 0.7; noise slip', covers=[0.7, 0.49, 0.51, round(math.sqrt(0.51), 4)])
lv.claim(close(0.8 * 1.0 + 0.6 * -0.5, 0.5, 1e-12), 'review: 0.5 = 0.8 - 0.3; slips', covers=[0.5, 0.3, round(0.64 - 0.36 * 0.5, 4), 1.1, 1.0, 0.64, 0.36])
lv.claim(close((0.5 - 0.19 / 0.8 * 0.4) / 0.9, 0.45, 1e-12), 'review: 0.45; 0.095', covers=[0.45, 0.095, round(0.5 - 0.19 / 0.8 * 0.4, 3), round((0.5 - 0.19 / 0.6 * 0.4) / 0.9, 3), 0.19, 0.4, 0.9, 0.8, 0.6])
lv.claim(close(0.75 / 0.25, 3, 1e-12) and 1 + 2 == 3, 'review: 3 and 3', covers=[3, round(1 / 3, 4), 0.75, 2, 1])
aP = abar_logs([0.04, 0.1, 0.2])
lv.expect('problems', 'items[0].parts[0].widget.answer', round(float(aP[2]), 4))
x3 = [math.sqrt(aP[2]) * v + math.sqrt(1 - aP[2]) * e for v, e in ((1.0, 0.2), (-0.5, 0.6))]
lv.expect('problems', 'items[0].parts[1].widget.answer', round(x3[0], 3))
m3 = (x3[0] - 0.2 / math.sqrt(1 - aP[2]) * 0.2) / math.sqrt(0.8)
lv.expect('problems', 'items[0].parts[2].widget.answer', round(m3, 3))
lv.expect('problems', 'items[0].parts[2]', round(x3[0], 4), fmt='{:.4f}')
lv.expect('problems', 'items[0].parts[2]', round(1 - float(aP[2]), 4), fmt='{:.4f}')
lv.expect('problems', 'items[0].parts[2].explain.text', round(0.2 / math.sqrt(1 - aP[2]), 4), fmt='{:.4f}')
lv.claim(close(math.sqrt(aP[2]), 0.8314, 1e-4) and close(math.sqrt(1 - aP[2]) * 0.2, 0.1111, 1e-3), 'pieces 0.8314 and 0.1111', covers=[0.8314, 0.1111, 0.96, 0.864, 0.66, 0.04, 0.1, 0.2, 0.6, 0.5, 1.0])
lv.claim(close(0.8 * 2, 1.6, 1e-12) and close(0.64 * 0.25 + 0.36, 0.52, 1e-12), 'problem 2: 1.6 and 0.52; slips 2.0, 1.28, 0.76, 1.0', covers=[1.6, 0.52, 2.0, 1.28, 0.76, 1.0, 0.25, 0.5])
eh = math.sqrt(0.36) * (1.0 - 1.6) / 0.52
lv.expect('problems', 'items[1].parts[2].widget.answer', round(eh, 3))
lv.expect('problems', 'items[1].parts[2].widget.wrong[1].value', round((1.0 - 1.6) / 0.52, 3))
lv.claim(close(1.0 - 1.6, -0.6, 1e-12), 'problem 2: -0.6', covers=[0.6])
a20p = math.exp(20 * math.log(0.95))
lv.expect('problems', 'items[2].parts[0].widget.answer', round(a20p, 3))
lv.expect('problems', 'items[2].parts[1].widget.answer', round(round(a20p, 3) / (1 - round(a20p, 3)), 3))
nn = math.ceil(math.log(0.01) / math.log(0.95))
lv.expect('problems', 'items[2].parts[2].widget.answer', nn)
lv.expect('problems', 'items[2].parts[2]', round(math.log(0.01) / math.log(0.95), 1), fmt='{:.1f}')
lv.expect('problems', 'items[2].parts[3].widget.answer', 1000 * nn)
lv.claim(0.95 ** (nn - 1) > 0.01 > 0.95 ** nn, f'{nn - 1} steps are not enough, {nn} are', covers=[nn - 1, 100, 0.95, 0.01, 20000, 4.5, round(1 - a20p, 3), round((1 - round(a20p, 3)) / round(a20p, 3), 3)])
lv.claim(close(0.1 / 0.9, 0.1111, 1e-3), 'homework SNR 0.1111; slips 9 and 0.1', covers=[0.1111, 9.0, 0.1, 0.9])
mh = (1.2 - 0.36 / 0.6 * 0.5) / 0.8
lv.expect('homework', 'items[5].widget.answer', round(mh, 3))
lv.claim(close(0.36 / 0.6 * 0.5, 0.3, 1e-12), 'homework pieces 0.3', covers=[0.3, round(1.2 - 0.36 / 0.6 * 0.5, 3), round((1.2 - 0.36 / 0.8 * 0.5) / 0.8, 3), 1.2, 0.36, 0.64, 0.6, 0.8, 0.5])
lv.claim(5000 * 200 - 5000 * 50 == 750000, 'homework cost: 1,000,000 and 250,000, saving 750,000', covers=[750000, 250000, 1000000, 5000, 200, 50, 150])
given([15, 100, 50000], 'scenarios: years, stocks and synthetic days are given')
lv.expect('l16', 'screens[1].hints[1].text', round(1 - end, 4), fmt='{:.4f}')
lv.check_wrongs()
lv.report()
