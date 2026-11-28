"""Recompute every number stated in nn-train level 1 (Optimisers) and check each at its JSON path.

Run: <venv>/bin/python docs/reports/nn-train-L1-numbers.py   (NumPy only; about a minute; exits 0 when every check passes)
     ZQ_NUMBERS_STRICT=1 makes an on-screen number that no check compared fail the run (the AI strand's rule).

Route A: the shipped modules, app/content/data/ai/autograd.py (frozen v1.0) and nt_ops_l1.py, as the lessons use them.
Route B: this script's own NumPy, with the network's gradients written by hand (no autograd), its own spiral generator,
optimisers and schedule, and closed forms (geometric series, eigenvalues of the heavy-ball iteration) beside simulations.
Every training figure on screen comes from route B and is checked against route A on the runs that both make.
Every code widget is run in CPython with the page's judge: the solution passes, the starter fails, and each mutant first
fails the hidden test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
APP = os.path.join(ROOT, 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level  # noqa: E402

sys.path.insert(0, DATA)
import nt_ops_l1 as A  # noqa: E402

lv = Level('nn-train', 1)
E = lv.expect
COV = []


def cov(*vals):
    COV.extend(vals)


def agree(label, a, b, rel=1e-9):
    ok = abs(a - b) <= rel * max(1e-12, abs(a), abs(b))
    lv.claim(ok, f'{label}: routes agree ({a!r}, {b!r})')
    return b


# ---------------- frozen and shipped files ----------------
AG = open(os.path.join(DATA, 'autograd.py'), 'rb').read()
lv.claim(hashlib.sha256(AG).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0 (SHA-256 5917d4ec91f7...)')
OPS = open(os.path.join(DATA, 'nt_ops_l1.py'), 'rb').read()
print('nt_ops_l1.py SHA-256', hashlib.sha256(OPS).hexdigest(), len(OPS), 'bytes')
shipped = []


def walk(node):
    if isinstance(node, dict):
        for key in ('data', 'files'):
            if isinstance(node.get(key), dict):
                for k, v in node[key].items():
                    if k.endswith('.py'):
                        shipped.append((key, k, v))
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for doc in lv.files.values():
    walk(doc)
lv.claim(all(key == 'data' and v == f'content/data/ai/{k}' for key, k, v in shipped) and len(shipped) >= 4,
         f'every shipped module ({len(shipped)}) is sent by path from the data folder, so the page gets the canonical bytes')

# ---------------- route B: data, network and gradients by hand ----------------


def spirals_b(n=400, seed=0, noise=0.05):
    g = np.random.default_rng(seed)
    m = n // 2
    parts, labs = [], []
    for k in (0, 1):
        t = np.sqrt(g.random(m)) * 2 * np.pi
        r = t / (2 * np.pi)
        ang = t + k * np.pi
        pts = np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1) + noise * g.standard_normal((m, 2))
        parts.append(pts)
        labs.append(np.full(m, k))
    X, y = np.concatenate(parts), np.concatenate(labs)
    o = g.permutation(2 * m)
    return X[o], y[o]


def init_b(sizes=(2, 16, 16, 2), seed=0):
    g = np.random.default_rng(seed)
    out = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        out += [g.standard_normal((a, b)) * (1 / math.sqrt(a)), np.zeros(b)]
    return out


def loss_grads_b(P, X, y, scale=1.0):
    W1, b1, W2, b2, W3, b3 = P
    h1 = np.tanh(X @ W1 + b1)
    h2 = np.tanh(h1 @ W2 + b2)
    z = h2 @ W3 + b3
    z = z - z.max(axis=1, keepdims=True)
    lse = np.log(np.exp(z).sum(axis=1))
    p = np.exp(z - lse[:, None])
    n = len(X)
    loss = np.mean(lse - z[np.arange(n), y])
    d = p.copy()
    d[np.arange(n), y] -= 1
    d *= scale / n
    gW3, gb3 = h2.T @ d, d.sum(0)
    d2 = (d @ W3.T) * (1 - h2 ** 2)
    gW2, gb2 = h1.T @ d2, d2.sum(0)
    d1 = (d2 @ W2.T) * (1 - h1 ** 2)
    gW1, gb1 = X.T @ d1, d1.sum(0)
    return loss * scale, [gW1, gb1, gW2, gb2, gW3, gb3]


def full_b(P, X, y):
    return loss_grads_b(P, X, y)[0]


Xs, ys = spirals_b()
XA, yA = A.spirals()
lv.claim(np.array_equal(Xs, XA) and np.array_equal(ys, yA), 'spiral data: two generators agree exactly')
P0 = init_b()
lv.claim(all(np.array_equal(a, b) for a, b in zip(P0, A.init_net())), 'initial weights: two routes agree')
la, ga = A.loss_and_grads(A.init_net(), XA, yA)
lb, gb = loss_grads_b(P0, Xs, ys)
agree('starting full loss', la, lb, 1e-12)
lv.claim(max(float(np.max(np.abs(a - b))) for a, b in zip(ga, gb)) < 1e-12, 'autograd gradients equal the hand-written backward pass')


def train_b(opt, steps, seed, lr, schedule=None, scale=1.0, beta=0.9):
    X, y = Xs, ys
    P = init_b()
    g = np.random.default_rng(seed)
    s1 = [np.zeros_like(p) for p in P]
    s2 = [np.zeros_like(p) for p in P]
    for t in range(steps):
        idx = g.choice(len(X), 32, replace=False)
        _, G = loss_grads_b(P, X[idx], y[idx], scale)
        r = schedule(t) if schedule else lr
        if opt == 'sgd':
            P = [p - r * q for p, q in zip(P, G)]
        elif opt == 'momentum':
            s1 = [beta * v - r * q for v, q in zip(s1, G)]
            P = [p + v for p, v in zip(P, s1)]
        else:
            s1 = [0.9 * m + 0.1 * q for m, q in zip(s1, G)]
            s2 = [0.999 * v + 0.001 * q * q for v, q in zip(s2, G)]
            c1, c2 = 1 - 0.9 ** (t + 1), 1 - 0.999 ** (t + 1)
            P = [p - r * (m / c1) / (np.sqrt(v / c2) + 1e-8) for p, m, v in zip(P, s1, s2)]
    return P


def final_b(*a, **k):
    with np.errstate(all='ignore'):
        return full_b(train_b(*a, **k), Xs, ys)


def train_a(opt, steps, seed, lr, schedule=None, beta=0.9):
    """route A: the module's optimisers and autograd gradients"""
    X, y = XA, yA
    P = A.init_net()
    g = np.random.default_rng(seed)
    s1 = [np.zeros_like(p) for p in P]
    s2 = [np.zeros_like(p) for p in P]
    for t in range(steps):
        idx = g.choice(len(X), 32, replace=False)
        _, G = A.loss_and_grads(P, X[idx], y[idx])
        r = schedule(t) if schedule else lr
        if opt == 'sgd':
            P = A.sgd_step(P, G, r)
        elif opt == 'momentum':
            P, s1 = A.momentum_step(P, s1, G, r, beta)
        else:
            P, s1, s2 = A.adam_step(P, G, s1, s2, t + 1, r)
    return A.full_loss(P, X, y)


SEEDS = (1, 2, 3, 4, 5)
for opt, lr in (('sgd', 0.5), ('momentum', 0.3), ('adam', 0.1)):
    agree(f'{opt} at {lr}, 300 steps, seed 1', train_a(opt, 300, 1, lr), final_b(opt, 300, 1, lr), 1e-7)
agree('adam with warm-up and cosine, 300 steps, seed 2', train_a('adam', 300, 2, 0, lambda t: A.warmup_cosine(t, 0.1, 15, 300)),
      final_b('adam', 300, 2, 0, lambda t: A.warmup_cosine(t, 0.1, 15, 300)), 1e-7)

# ================= l1-noisy-steps =================
L1 = 'l1-noisy-steps'
pe = np.array([loss_grads_b(P0, Xs[i:i + 1], ys[i:i + 1])[1][0][0, 0] for i in range(400)])
sig, gfull = float(pe.std()), float(pe.mean())
agree('full gradient of the first weight = mean of row gradients', gfull, float(gb[0][0, 0]), 1e-9)
g5 = np.random.default_rng(5)
d8 = [pe[g5.integers(0, 400, 8)].mean() for _ in range(200)]
d128 = [pe[g5.integers(0, 400, 128)].mean() for _ in range(200)]
sd8, sd128 = float(np.std(d8, ddof=1)), float(np.std(d128, ddof=1))
F1 = lv._file(L1)[1]
lv.claim(np.allclose(F1['screens'][0]['canvas']['params']['dataSets'][0], d8, rtol=0, atol=1e-12) and np.allclose(F1['screens'][0]['canvas']['params']['dataSets'][1], d128, rtol=0, atol=1e-12),
         'l1 hook: the two histograms hold these 200 draws each')
pred = sig / math.sqrt(128)
E(L1, 'screens[1].widget.answer', round(pred, 4))
E(L1, 'screens[1].widget.wrong[0].value', round(sig / 128, 4))
E(L1, 'screens[1].widget.wrong[1].value', round(sig / math.sqrt(8), 4))
E(L1, 'screens[1].widget.wrong[2].value', round(sig / 16, 4))
lv.claim(abs(sd128 - pred) < 0.15 * pred and abs(sd8 - sig / math.sqrt(8)) < 0.15 * sig / math.sqrt(8), 'the measured sds sit near sigma/sqrt(B)')
lv.claim(3.0 < sd8 / sd128 < 5.0, f'ratio of the spreads is about 4 ({sd8 / sd128:.2f})')
cov(sig, gfull, sd8, sd128, pred, sd8 / sd128, math.sqrt(128), 128 / 8, 0.25, 4, 16)
# one step by hand
x3, y3 = np.array([1.0, 2.0, 3.0]), np.array([2.0, 3.0, 5.0])
gr = float(np.mean((1.0 * x3 - y3) * x3))
E(L1, 'screens[2].widget.answer', 1 - 0.1 * gr)
E(L1, 'screens[2].widget.wrong[0].value', 1 - 0.1 * float(np.sum((x3 - y3) * x3)))
E(L1, 'screens[2].widget.wrong[1].value', 1 + 0.1 * gr)
E(L1, 'screens[2].widget.wrong[2].value', 1 - 0.1 * float((1 - 2) * 1))
cov(gr, -9, 0.3)


# per epoch, full batch against batch 32, 8 and 128
def per_epoch_b(B, lr, epochs, seed=1):
    P = init_b()
    out = [full_b(P, Xs, ys)]
    for e in range(epochs):
        order = np.random.default_rng(seed * 1000 + e).permutation(400)
        for i in range(0, 400, B):
            idx = order[i:i + B]
            _, G = loss_grads_b(P, Xs[idx], ys[idx])
            P = [p - lr * q for p, q in zip(P, G)]
        out.append(full_b(P, Xs, ys))
    return out


gd = per_epoch_b(400, 0.5, 20)
e32, e8, e128 = per_epoch_b(32, 0.5, 20), per_epoch_b(8, 0.5, 20), per_epoch_b(128, 0.5, 20)
lv.claim(np.allclose(F1['screens'][3]['canvas']['params']['series'][0]['values'], np.round(gd, 4), atol=1e-12)
         and np.allclose(F1['screens'][3]['canvas']['params']['series'][1]['values'], np.round(e32, 4), atol=1e-12), 'l1 screen 3: both curves recomputed')
lv.claim(np.allclose(F1['screens'][6]['canvas']['params']['series'][0]['values'], np.round(e8, 4), atol=1e-12)
         and np.allclose(F1['screens'][6]['canvas']['params']['series'][1]['values'], np.round(e128, 4), atol=1e-12), 'l1 trap: both curves recomputed')
E(L1, 'screens[3].widget.answer', 20 * math.ceil(400 / 32))
lv.claim(len(range(0, 400, 32)) == 13 and len(range(0, 400, 128)) == 4 and len(range(0, 400, 8)) == 50, '13, 4 and 50 batches an epoch')
lv.claim(e8[1] < e128[1] and e8[20] < e128[20], 'batch 8 is ahead of batch 128 per epoch at epochs 1 and 20')
cov(e32[20], gd[20], e8[1], e128[1], e8[20], e128[20], 8000, 384, 250, 13)
# the band on least squares
gl = np.random.default_rng(7)
Xr = gl.standard_normal((1000, 3))
yr = Xr @ np.array([1.5, -2.0, 0.5]) + 0.5 * gl.standard_normal(1000)
Lls = lambda w: 0.5 * float(np.mean((Xr @ w - yr) ** 2))  # noqa: E731
wstar = np.linalg.solve(Xr.T @ Xr, Xr.T @ yr)
Lstar = Lls(wstar)
agree('least-squares minimum: normal equations against lstsq', Lstar, Lls(np.linalg.lstsq(Xr, yr, rcond=None)[0]), 1e-12)
band = {}
for lr in (0.05, 0.1, 0.2, 0.4):
    rng = np.random.default_rng(11)
    w = np.zeros(3)
    h = [Lls(w)]
    for t in range(300):
        idx = rng.integers(0, 1000, 8)
        w = w - lr * (Xr[idx].T @ (Xr[idx] @ w - yr[idx]) / 8)
        h.append(Lls(w))
    band[lr] = float(np.mean(np.array(h[101:]) - Lstar))
lv.claim(band[0.05] < band[0.1] < band[0.2] < band[0.4], 'the band grows with every doubling of the step')
lv.claim(1.5 < band[0.2] / band[0.1] < 2.5, f'doubling 0.1 to 0.2 roughly doubles the band ({band[0.2] / band[0.1]:.2f})')
cov(Lstar, *band.values(), band[0.2] / band[0.1])
# the sweep
STEADY = (0.1, 0.3, 0.5, 1.0, 1.5)
sw = {lr: [final_b('sgd', 300, s, lr) for s in SEEDS] for lr in STEADY + (2.0, 4.0)}
for lr in STEADY:
    E(L1, f'screens[5].canvas.state.values.s{str(lr).replace(".", "")}', round(float(np.mean(sw[lr])), 4))
    agree(f'sweep at {lr}, seed 3, both routes', train_a('sgd', 300, 3, lr), sw[lr][2], 1e-9)
lv.claim(min(STEADY, key=lambda k: np.mean(sw[k])) == 0.5, 'step 0.5 has the lowest mean full loss of the steady runs')
sw2a = [train_a('sgd', 300, s, 2.0) for s in SEEDS]
lv.claim(max(abs(a - b) / b for a, b in zip(sw2a, sw[2.0])) > 0.01, 'at 2 the two routes disagree by more than 1% on some seed: the runs are unstable')
sw4a = [train_a('sgd', 300, s, 4.0) for s in SEEDS]
start = full_b(P0, Xs, ys)
lv.claim(sum(x > start for x in sw[4.0]) >= 4 and sum(x > start for x in sw4a) >= 4, 'at 4 most seeds blow up (above the starting loss) in both routes')
cov(*[float(np.mean(sw[k])) for k in STEADY])
E(L1, 'screens[7].widget.answer', 0.05 * 256 / 32)
E(L1, 'screens[7].widget.wrong[0].value', round(0.05 * math.sqrt(8), 4))
E(L1, 'screens[7].widget.wrong[1].value', 0.05 / 8)
sig_r = float(np.std(-yr * Xr[:, 0]))
cov(sig_r, sig_r / 8)
E(L1, 'screens[9].widget.answer', (0.8 / 0.01) ** 2)
cov(80, 6400 / 1e6, 0.0064, 0.64)
E(L1, 'quiz[0].widget.answer', 0.02 / math.sqrt(64 / 16))
E(L1, 'quiz[2].widget.answer', math.ceil(50000 / 64))
cov(50000 / 64, 781 * 64)
lv.literal('400', why='the spiral data set size, a stated choice')
lv.literal('1,000', why='least-squares rows, steps and loss scales are stated choices')
lv.literal('1,000,000', why='the transfer desk\'s row count, a stated scenario')
lv.literal('300', why='run length in steps, a stated choice')
lv.literal('200', why='number of minibatch draws in the hook, a stated choice')
lv.literal('50,000', why='a stated data set size in the quiz')
lv.literal('256', why='a stated batch size in the generalise screen')

# ================= l2-momentum =================
L2 = 'l2-momentum'
Hd = np.array([1.0, 10.0])


def hb_b(s, beta, n, x0=(10.0, 1.0)):
    """closed form: each coordinate follows x_{k+1} = (1 + beta - s lam) x_k - beta x_{k-1}, x_1 = (1 - s lam) x_0"""
    out = np.zeros((n + 1, 2))
    for j, lam in enumerate(Hd):
        a = 1 + beta - s * lam
        prev, cur = x0[j], (1 - s * lam) * x0[j]
        out[0, j] = prev
        if n >= 1:
            out[1, j] = cur
        for k in range(2, n + 1):
            prev, cur = cur, a * cur - beta * prev
            out[k, j] = cur
    return out


def hb_loop(s, beta, n):
    x, v = np.array([10.0, 1.0]), np.zeros(2)
    for _ in range(n):
        v = beta * v - s * Hd * x
        x = x + v
    return x


agree('heavy ball: recurrence against the loop at beta 0.4', float(np.linalg.norm(hb_b(2 / 11, 0.4, 20)[-1])), float(np.linalg.norm(hb_loop(2 / 11, 0.4, 20))), 1e-9)
grid = np.round(np.arange(0, 0.951, 0.01), 2)
d20 = [float(np.linalg.norm(hb_b(2 / 11, b, 20)[-1])) for b in grid]
bb = float(grid[int(np.argmin(d20))])
gd20 = float(np.linalg.norm(hb_b(2 / 11, 0, 20)[-1]))
E(L2, 'screens[0].widget.answer', bb)
cov(gd20, min(d20), d20[90], 9 / 11, 2 / 11)
agree('plain descent at 2/11 after 20 steps: sqrt(101) (9/11)^20', gd20, math.sqrt(101) * (9 / 11) ** 20, 1e-9)
E(L2, 'screens[1].widget.answer', sum(0.9 ** k for k in range(5000)))
cov(1 / (1 - 0.99), 1 / 1.9)
E(L2, 'screens[2].widget.answer', hb_b(0.1, 0.5, 2)[2, 0])
lv.claim(np.allclose(hb_b(0.1, 0.5, 2), [[10, 1], [9, 0], [7.6, -0.5]]), 'two hand steps: (9, 0) then (7.6, -0.5)')
cov(8.1, 8.5, 7.1, -1.4, -0.5, 0.9)
sk = math.sqrt(10)
bhb, shb = ((sk - 1) / (sk + 1)) ** 2, 4 / (1 + sk) ** 2
M = lambda lam: np.array([[1 + bhb - shb * lam, -bhb], [1, 0]])  # noqa: E731
rate = max(max(abs(np.linalg.eigvals(M(1)))), max(abs(np.linalg.eigvals(M(10)))))
agree('heavy-ball rate: sqrt(beta) against the iteration matrix eigenvalues', math.sqrt(bhb), rate, 1e-6)
E(L2, 'screens[3].widget.answer', round(bhb, 3))
cov(bhb, shb, math.sqrt(bhb), (sk - 1), (sk + 1), sk, math.sqrt(bhb) ** 20, (9 / 11) ** 20)
hbrel = float(np.linalg.norm(hb_b(shb, bhb, 20)[-1]) / math.sqrt(101))
cov(hbrel)
lv.claim(hbrel > math.sqrt(bhb) ** 20, 'the measured heavy-ball iterates lag the asymptotic factor')
# spiral runs
sp = {k: [final_b(o, 300, s, lr) for s in SEEDS] for k, o, lr in (('sgd002', 'sgd', 0.02), ('mom002', 'momentum', 0.02), ('sgd02', 'sgd', 0.2), ('mom03', 'momentum', 0.3))}
cov(sp['mom002'][0], sp['sgd002'][0], sp['sgd02'][0], float(np.mean(sp['mom03'])))
lv.claim(abs(sp['mom002'][0] - sp['sgd02'][0]) < abs(sp['mom002'][0] - sp['sgd002'][0]), 'momentum at 0.02 ends closer to SGD at 0.2 than at 0.02')
agree('momentum at 0.3, seed 5, both routes', train_a('momentum', 300, 5, 0.3), sp['mom03'][4], 1e-8)
lv.claim(max(sp['mom03']) < 0.1, 'momentum at 0.3 trains steadily on all five seeds')
F2 = lv._file(L2)[1]
lv.claim(abs(F2['screens'][4]['canvas']['params']['series'][1]['values'][-1] - round(sp['mom002'][0], 4)) < 1e-12, 'the momentum curve ends at seed 1\'s final loss')
d99 = float(np.linalg.norm(hb_b(2 / 11, 0.99, 20)[-1]))
cov(d99, float(np.linalg.norm(hb_b(2 / 11, 0.99, 100)[-1])))
lv.claim(d99 > gd20, 'beta 0.99 ends further away than plain descent')
k2 = (2 * 1.9) / (2 * 0.1)
r2 = (math.sqrt(k2) - 1) / (math.sqrt(k2) + 1)
n2 = math.ceil(math.log(1000) / math.log(1 / r2))
E(L2, 'screens[8].widget.answer', n2)
lv.claim(n2 == next(k for k in range(1, 200) if r2 ** k <= 1e-3), 'heavy-ball count by direct search')
lv.claim(math.ceil(math.log(1000) / math.log(1 / 0.9)) == 66, 'plain descent needs 66 steps at rate 0.9')
cov(k2, r2, math.sqrt(19), math.log(1000), math.log(1 / r2), math.log(1000) / math.log(1 / r2), 0.9, 66)
E(L2, 'quiz[0].widget.answer', 1 / (1 - 0.8))
E(L2, 'quiz[2].widget.answer', round(9 / 11, 3))
cov(99 / 101, (9 / 11) ** 2)

# ================= l3-adam =================
L3 = 'l3-adam'


def rec_b(opt, lr, scale):
    P = init_b()
    g = np.random.default_rng(1)
    a = [np.zeros_like(p) for p in P]
    b = [np.zeros_like(p) for p in P]
    out = [full_b(P, Xs, ys)]
    for t in range(50):
        idx = g.choice(400, 32, replace=False)
        _, G = loss_grads_b(P, Xs[idx], ys[idx], scale)
        if opt == 'sgd':
            P = [p - lr * q for p, q in zip(P, G)]
        else:
            a = [0.9 * m + 0.1 * q for m, q in zip(a, G)]
            b = [0.999 * v + 0.001 * q * q for v, q in zip(b, G)]
            P = [p - lr * (m / (1 - 0.9 ** (t + 1))) / (np.sqrt(v / (1 - 0.999 ** (t + 1))) + 1e-8) for p, m, v in zip(P, a, b)]
        with np.errstate(all='ignore'):
            out.append(full_b(P, Xs, ys))
    return out


hs1, hs1000, ha1, ha1000 = rec_b('sgd', 0.5, 1.0), rec_b('sgd', 0.5, 1000.0), rec_b('adam', 0.1, 1.0), rec_b('adam', 0.1, 1000.0)
cov(hs1000[1], ha1[-1], ha1000[-1])
lv.claim(hs1000[1] > 50 and abs(ha1000[-1] - ha1[-1]) < 1e-4, 'SGD on the scaled loss is above 50 nats after one step; Adam ends within 1e-4 of its unscaled run')
E(L3, 'screens[1].widget.answer', 0.1)
E(L3, 'screens[1].widget.wrong[1].value', round(0.1 * 0.1 * 0.003 / math.sqrt(0.001 * 0.003 ** 2), 4))
cov(0.1 / math.sqrt(0.001))
w, m, v, ws, mh2, vh2 = 1.0, 0.0, 0.0, [1.0], None, None
for t in range(1, 4):
    gg = 2 * w
    m, v = 0.9 * m + 0.1 * gg, 0.999 * v + 0.001 * gg * gg
    if t == 2:
        mh2, vh2 = m / (1 - 0.9 ** 2), v / (1 - 0.999 ** 2)
    w -= 0.1 * (m / (1 - 0.9 ** t)) / (math.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
    ws.append(w)
wa, ma, va = [np.array(1.0)], [np.array(0.0)], [np.array(0.0)]
for t in range(1, 4):
    wa, ma, va = A.adam_step(wa, [2 * wa[0]], ma, va, t, 0.1)
agree('three Adam steps: hand loop against the module', ws[3], float(wa[0]), 1e-12)
E(L3, 'screens[2].widget.answer', round(ws[2], 4))
cov(ws[1], ws[2], ws[3], mh2, math.sqrt(vh2), 0.1 * mh2 / math.sqrt(vh2), mh2 / math.sqrt(vh2), 0.36, 0.007236, 0.19, 0.001999, 3.24, 0.004, 0.2, 4, 0.72)
fac = {t: (1 - 0.9 ** t) / math.sqrt(1 - 0.999 ** t) for t in (1, 10, 100, 1000)}


def sim_factor(T):
    mm = vv = 0.0
    for _ in range(T):
        mm, vv = 0.9 * mm + 0.1, 0.999 * vv + 0.001
    return (mm / math.sqrt(vv)) / ((mm / (1 - 0.9 ** T)) / math.sqrt(vv / (1 - 0.999 ** T)))


agree('step-10 factor: closed form against a simulated constant gradient', fac[10], sim_factor(10), 1e-12)
E(L3, 'screens[3].widget.answer', round(fac[10], 2))
cov(*fac.values(), 1 - 0.9 ** 10, 1 - 0.999 ** 10, math.sqrt(1 - 0.999 ** 10), 1 - 0.9 ** 100, 1 - 0.999 ** 100, 1 - 0.999 ** 1000, 1 / math.sqrt(1 - 0.999 ** 10))
tun = {o: [final_b(o, 300, s, lr) for s in SEEDS] for o, lr in (('sgd', 0.5), ('momentum', 0.3), ('adam', 0.1))}
low = [min(tun, key=lambda o: tun[o][i]) for i in range(5)]
E(L3, 'screens[4].widget.answer', low.count('adam'))
lv.claim(low == ['momentum', 'adam', 'adam', 'adam', 'adam'], 'lowest by seed: momentum, then Adam on seeds 2 to 5')
lv.claim(all(tun['momentum'][i] < tun['sgd'][i] and tun['adam'][i] < tun['sgd'][i] for i in range(5)), 'momentum and Adam end below SGD on every seed')
cov(tun['adam'][0], tun['momentum'][0], tun['sgd'][1], tun['momentum'][1], tun['adam'][1])
AST = (0.003, 0.01, 0.03, 0.1)
asw = {lr: [final_b('adam', 300, s, lr) for s in SEEDS] for lr in AST + (0.5,)}
for lr in AST:
    E(L3, f'screens[5].canvas.state.values.a{str(lr).replace(".", "")}', round(float(np.mean(asw[lr])), 4))
lv.claim(min(AST, key=lambda k: np.mean(asw[k])) == 0.1, 'Adam\'s sweep is lowest at 0.1')
a05 = [train_a('adam', 300, s, 0.5) for s in SEEDS]
lv.claim(min(asw[0.5]) > 0.2 and min(a05) > 0.2, 'Adam at 0.5 ends above 0.2 nats on every seed, in both routes')
cov(*[float(np.mean(asw[k])) for k in AST], 0.2)
E(L3, 'screens[9].widget.answer', 1200 / 0.4)
cov(0.4 / 1200)
lv.literal('1,200', why='the transfer\'s price level and gradient, a stated scenario')
E(L3, 'quiz[0].widget.answer', 1 - 0.9 ** 2)
E(L3, 'quiz[2].widget.answer', 0.003)
cov(0.003 * 0.02, 0.81, 2 * 0.003 * 0.02 / 40 * 0.025)

# ================= l4-schedules =================
L4 = 'l4-schedules'


def wc_b(t, lmax, w, T):
    t = min(max(t, 0), T)
    return lmax * t / w if t < w else lmax * (1 + math.cos(math.pi * (t - w) / (T - w))) / 2


for t, a, w_, T in ((75, 0.2, 0, 300), (5, 0.1, 20, 300), (160, 0.1, 20, 300), (230, 0.1, 20, 300), (450, 0.2, 0, 300), (1050, 0.003, 100, 2000)):
    agree(f'warmup_cosine({t}, {a}, {w_}, {T})', A.warmup_cosine(t, a, w_, T), wc_b(t, a, w_, T), 1e-12)


def ls_run(f, seed):
    rng = np.random.default_rng(seed)
    w = np.zeros(3)
    h = [Lls(w) - Lstar]
    for t in range(300):
        idx = rng.integers(0, 1000, 8)
        w = w - f(t) * (Xr[idx].T @ (Xr[idx] @ w - yr[idx]) / 8)
        h.append(Lls(w) - Lstar)
    return h


SCH = {'const': lambda t: 0.2, 'step': lambda t: 0.2 if t < 180 else 0.02, 'cos': lambda t: wc_b(t, 0.2, 0, 300)}
fin = {k: float(np.mean([ls_run(f, s)[-1] for s in range(11, 21)])) for k, f in SCH.items()}
fin_each = {k: [ls_run(f, s)[-1] for s in range(11, 21)] for k, f in SCH.items()}
lv.claim(all(fin_each['step'][i] < fin_each['const'][i] and fin_each['cos'][i] < fin_each['const'][i] for i in range(10)), 'both decays end below the constant rate on all ten seeds')
lv.claim(5 < fin['const'] / fin['step'] < 20 and 5 < fin['const'] / fin['cos'] < 20, 'about ten times lower')
cov(*fin.values(), fin['const'] / 10, fin['const'] / 100)
E(L4, 'screens[3].widget.answer', round(fin['const'] / 10, 5))
r11 = {k: ls_run(f, 11) for k, f in SCH.items()}
cov(r11['const'][150], r11['cos'][150], r11['const'][-1], r11['cos'][-1])
lv.claim(r11['const'][150] < r11['cos'][150] and r11['const'][-1] > r11['cos'][-1], 'trap: the constant run is lower at step 150 and higher at step 300 (seed 11)')
E(L4, 'screens[1].widget.answer', round(wc_b(75, 0.2, 0, 300), 4))
cov(math.cos(math.pi / 4), 1 + math.cos(math.pi / 4), 0.1 * (1 + math.cos(75 / 300)), 0.85)
E(L4, 'screens[2].widget.rows[0][1].answer', wc_b(5, 0.1, 20, 300))
E(L4, 'screens[2].widget.rows[1][1].answer', wc_b(160, 0.1, 20, 300))
E(L4, 'screens[2].widget.rows[2][1].answer', round(wc_b(230, 0.1, 20, 300), 4))
cov(round(0.1 * (1 + math.cos(math.pi * 160 / 300)) / 2, 4), 0.05 * (1 + math.sin(0.75 * math.pi)), 0.75, -0.7071, 210, 280)
E(L4, 'screens[4].widget.answer', 0.1 / (0.1 * 1 / 20))
spw = {k: [final_b('adam', 300, s, 0, f) for s in SEEDS] for k, f in (('cos', lambda t: wc_b(t, 0.1, 0, 300)), ('wcos', lambda t: wc_b(t, 0.1, 15, 300)))}
cov(float(np.mean(spw['cos'])), float(np.mean(spw['wcos'])), min(spw['wcos']), max(spw['wcos']))
lv.claim(max(spw['wcos']) < 0.03, 'warm-up and cosine end below 0.03 on all five seeds (the l4 test threshold)')
E(L4, 'screens[5].widget.answer', 0.1 * (1 + math.cos(math.pi * 450 / 300)))
cov(1.5, 600)
E(L4, 'screens[9].widget.answer', round(wc_b(1050, 0.003, 100, 2000), 6))
cov(round(0.0015 * (1 + math.cos(math.pi * 1050 / 2000)), 6), 1900, 950, (1050 - 100) / 1900)
E(L4, 'quiz[0].widget.answer', round(0.2 * (1 + math.cos(math.pi / 4)), 4))
E(L4, 'quiz[1].widget.answer', 0.002 * 30 / 100)
cov(0.002 * 70 / 100, 0.7071)
lv.literal('2,000', why='the monthly retrain\'s run length, a stated scenario')
lv.literal('550', why='a schedule length stated in a review item')

# ================= review, problems, homework =================
E('review', 'items[1].widget.answer', 0.5 - 0.2 * np.mean([(0.5 * 2 - 1) * 2, (0.5 * 1 - 3) * 1]))
E('review', 'items[3].widget.answer', round(((2 - 1) / (2 + 1)) ** 2, 3))
E('review', 'items[5].widget.answer', round((1 - 0.81) / math.sqrt(1 - 0.999 ** 2), 2))
E('review', 'items[6].widget.answer', round(0.025 * (1 + math.cos(3 * math.pi / 4)), 4))
E('review', 'items[7].widget.answer', wc_b(300, 0.01, 50, 550))
cov(-1.25, -2.5, 0.0447, math.sqrt(1 - 0.999 ** 2), 0.2929, 0.998001, 1 / 3)
ev = np.linalg.eigvalsh(np.array([[4.25, 3.75], [3.75, 4.25]]))
E('problems', 'items[0].parts[0].widget.answer', float(ev.max()))
E('problems', 'items[0].parts[1].widget.answer', round((16 - 1) / (16 + 1), 4))
E('problems', 'items[0].parts[3].widget.answer', next(k for k in range(1, 100) if 0.6 ** k <= 1e-3))
sb = 2 / (ev.min() + ev.max())
E('problems', 'items[0].parts[4].widget.answer', next(B for B in range(1, 10 ** 6) if sb * 2 / math.sqrt(B) <= 0.01))
cov(sb, sb * 200, (sb * 200) ** 2, 0.6 ** 13, 0.6 ** 14, 6.908 / 0.511, math.log(1 / 0.6), next(k for k in range(1, 100) if (15 / 17) ** k <= 1e-3), 8.5)
mm, vv = 0.9 * 0.4 + 0.1 * (-2), 0.999 * 0.016 + 0.001 * 4
E('problems', 'items[1].parts[0].widget.answer', mm)
mh, vh = mm / 0.19, vv / (1 - 0.999 ** 2)
E('problems', 'items[1].parts[1].widget.answer', round(mh, 4))
E('problems', 'items[1].parts[2].widget.answer', round(0.01 * mh / (math.sqrt(vh) + 1e-8), 6))
E('problems', 'items[1].parts[3].widget.answer', round(0.002 * mh / (math.sqrt(vh) + 1e-8), 6))
cov(vv, vh, math.sqrt(vh), mh / math.sqrt(vh), 0.36, -0.2)
E('problems', 'items[2].parts[1].widget.answer', round(wc_b(1200, 0.08, 0, 4000), 4))
E('problems', 'items[2].parts[2].widget.answer', round(1.5 / math.sqrt(50), 4))
E('problems', 'items[2].parts[3].widget.answer', round(wc_b(1200, 0.08, 0, 4000) * 1.5 / math.sqrt(50), 4))
cov(math.cos(0.3 * math.pi), 1 + math.cos(0.3 * math.pi), math.sqrt(50), 2.25 / 50, 1.5)
lv.literal('20,000', why='the problem\'s data set size, a stated scenario')
f5 = (1 - 0.9 ** 5) / math.sqrt(1 - 0.999 ** 5)
E('homework', 'items[3].widget.answer', round(f5, 2))
cov(1 - 0.9 ** 5, math.sqrt(1 - 0.999 ** 5))
lv.literal('512', why='a stated batch size in the homework')

# ---------------- code widgets: solution, starter, mutants ----------------


def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def nan(x):
        try:
            return bool(x != x)
        except Exception:
            return False

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        if nan(x) and nan(y):
            return True
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
        return (nan(x) and nan(y)) or bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def first_fail(w, src):
    cwd, d = os.getcwd(), tempfile.mkdtemp()
    os.chdir(d)
    try:
        for k, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(d, k))
        sys.path.insert(0, d)
        for mod in [m for m in sys.modules if m == 'autograd' or m.startswith('nt_ops')]:
            sys.modules.pop(mod)
        ns = {'__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                if c.get('compare') == 'raises':
                    return i + 1
                t = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception as e:  # noqa
                ok = c.get('compare') == 'raises' and type(e).__name__ == c.get('expect')
            if not ok:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        sys.path.remove(d)
        shutil.rmtree(d, ignore_errors=True)
        for mod in [m for m in sys.modules if m == 'autograd' or m.startswith('nt_ops')]:
            sys.modules.pop(mod)
        sys.path.insert(0, DATA)


nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab = f'{fid} {u.get("title") or u.get("id")}'
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')
# training thresholds the hidden tests use, on five seeds
lv.claim(max(tun['sgd']) < 0.2, f'l3 test threshold: SGD at 0.5 ends below 0.2 on all five seeds (worst {max(tun["sgd"]):.4f})')
cov(*[x for v in tun.values() for x in v])

# settings and given figures stated on screen (no computation behind them)
lv.literal('0.999', why='Adam\'s beta2, a stated setting')
lv.literal('10^-8', why='Adam\'s epsilon, a stated setting')
lv.literal('3.75', why='an entry of the given Hessian in problems-1')
lv.literal('0.31', why='a stated minibatch loss in a review scenario')
for lit in ('10^-3', '10^-4', '10^-6'):
    lv.literal(lit, why='a tolerance or target stated in a question, hint or how line')
lv.literal('0.99', why='a stated momentum setting')
cov(32, 128, 50, 30, 160, 230, 180, 450, 1050, 500, 99, 101, 10, 8, 2, 0.02 * math.sqrt(8), 512 / 64, 0.001 * 4 ** 2, 1.5 ** 2,
    float(f'{hbrel:.1e}'), 70 / 100, float(f'{math.sqrt(bhb) ** 20:.1e}'))
lv.claim(True, 'route B values', covers=COV)
lv.check_wrongs()
lv.report()
