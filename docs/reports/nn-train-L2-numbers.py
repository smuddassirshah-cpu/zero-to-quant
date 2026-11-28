"""Recompute every number stated in nn-train level 2 (Activations, initialisation and normalisation) and check each at its JSON path.

Run: <venv>/bin/python docs/reports/nn-train-L2-numbers.py   (NumPy only; under a minute; exits 0 when every check passes)
     ZQ_NUMBERS_STRICT=1 makes an on-screen number that no check compared fail the run (the AI strand's rule).

Route A: the shipped modules, autograd.py (frozen v1.0), nt_ops_l1.py (frozen at level 1) and nt_ops_l2.py, as the lessons use them.
Route B: this script's own NumPy: central differences for every op's gradient, a hand-written backward pass through the
sigmoid stack, batch norm composed from autograd primitives (mean, power) for the deep-net runs, closed forms beside
simulations. Every code widget is run in CPython with the page's judge: the solution passes, the starter fails, and each
mutant first fails the hidden test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
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
from autograd import Tensor, cross_entropy, grad_check  # noqa: E402
import nt_ops_l2 as B2  # noqa: E402
from nt_ops_l1 import spirals  # noqa: E402

lv = Level('nn-train', 2)
E = lv.expect
COV = []
EPS = 1e-5


def cov(*vals):
    COV.extend(vals)


def agree(label, a, b, rel=1e-9):
    ok = abs(a - b) <= rel * max(1e-12, abs(a), abs(b))
    lv.claim(ok, f'{label}: routes agree ({a!r}, {b!r})')
    return b


sig = lambda z: 1 / (1 + math.exp(-z))  # noqa: E731
ds = lambda z: sig(z) * (1 - sig(z))  # noqa: E731

# ---------------- frozen and shipped files ----------------
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'autograd.py'), 'rb').read()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'nt_ops_l1.py'), 'rb').read()).hexdigest() == '9c1391a33624604bf8547607a51ef08c39a9bee2eeef22947aa5126dbc4ff234', 'nt_ops_l1.py is byte-identical to level 1\'s')
OPS2 = open(os.path.join(DATA, 'nt_ops_l2.py'), 'rb').read()
print('nt_ops_l2.py SHA-256', hashlib.sha256(OPS2).hexdigest(), len(OPS2), 'bytes')
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
lv.claim(all(key == 'data' and v == f'content/data/ai/{k}' for key, k, v in shipped) and len(shipped) >= 4, f'every shipped module ({len(shipped)}) is sent by path')

# ---------------- the ops: gradients against central differences (route B) ----------------


def numgrad(f, arrs, h=1e-6):
    out = []
    for a in arrs:
        g = np.zeros_like(a)
        for i in np.ndindex(a.shape):
            old = a[i]
            a[i] = old + h
            fp = f()
            a[i] = old - h
            fm = f()
            a[i] = old
            g[i] = (fp - fm) / (2 * h)
        out.append(g)
    return out


def check_op(label, build, arrs, R):
    ts = [Tensor(a.copy()) for a in arrs]
    (build(*ts) * Tensor(R)).sum().backward()
    raw = [a.copy() for a in arrs]
    nums = numgrad(lambda: float((build(*[Tensor(a) for a in raw]).data * R).sum()), raw)
    err = max(float(np.abs(t.grad - n).max() / max(np.abs(n).max(), np.abs(t.grad).max(), 1e-12)) for t, n in zip(ts, nums))
    lv.claim(err < 1e-6, f'{label}: backward against central differences, relative error {err:.1e}')
    ts2 = [Tensor(a.copy()) for a in arrs]
    gc = grad_check(lambda: (build(*ts2) * Tensor(R)).sum(), ts2)
    lv.claim(gc < 1e-6, f'{label}: autograd grad_check {gc:.1e}')
    return err


g = np.random.default_rng(3)
Xo, Go, Bo, Ro = g.standard_normal((5, 4)), g.standard_normal(4), g.standard_normal(4), g.standard_normal((5, 4))
X3, R3 = g.standard_normal((2, 3, 4)), g.standard_normal((2, 3, 4))
ERR = {}
ERR['sigmoid'] = check_op('sigmoid', lambda x: B2.sigmoid(x), [Xo * 3], Ro)
ERR['batchnorm train'] = check_op('batchnorm, train mode', lambda x, gm, bt: B2.batchnorm(x, gm, bt)[0], [Xo, Go, Bo], Ro)
ERR['batchnorm eval'] = check_op('batchnorm, eval mode', lambda x, gm, bt: B2.batchnorm(x, gm, bt, mode='eval', running=(np.full(4, 0.3), np.full(4, 2.0)))[0], [Xo, Go, Bo], Ro)
ERR['layernorm 2-D'] = check_op('layernorm, (5, 4)', lambda x, gm, bt: B2.layernorm(x, gm, bt), [Xo, Go, Bo], Ro)
ERR['layernorm 3-D'] = check_op('layernorm, (2, 3, 4)', lambda x, gm, bt: B2.layernorm(x, gm, bt), [X3, Go, Bo], R3)
ERR['layernorm 1-D'] = check_op('layernorm, one vector', lambda x, gm, bt: B2.layernorm(x, gm, bt), [Xo[0], Go, Bo], Ro[0])
print('gradient-check errors', {k: f'{v:.1e}' for k, v in ERR.items()})
xbn = Tensor(np.array([[3.0, 1.0], [3.0, 2.0]]))
lv.claim(np.allclose(B2.batchnorm(xbn, np.ones(2), np.array([0.5, 0.0]))[0].data[:, 0], 0.5), 'batchnorm: a constant feature gives beta')
out1, run1 = B2.batchnorm(Tensor(np.array([[2.0], [4.0], [6.0], [8.0]])), np.ones(1), np.zeros(1))
lv.claim(np.allclose(run1[0], [0.5]) and np.allclose(run1[1], [1.4]), 'batchnorm: the running pair moves 0.1 of the way, from (0, 1)')
lv.claim(abs(B2.he_sd(100) - math.sqrt(0.02)) < 1e-15 and abs(B2.lecun_sd(100) - 0.1) < 1e-15, 'he_sd and lecun_sd')

# ================= l5-saturation =================
L5 = 'l5-saturation'
gq = np.random.default_rng(1)
Ws = [gq.standard_normal((100, 100)) * 0.1 for _ in range(10)]
x = gq.standard_normal((64, 100))
hs = [x]
for W in Ws:
    hs.append(1 / (1 + np.exp(-(hs[-1] @ W))))
d = 2 * hs[-1] / hs[-1].size
gnB = [0.0] * 10
for i in range(9, -1, -1):
    dz = d * hs[i + 1] * (1 - hs[i + 1])
    gnB[i] = float(np.linalg.norm(hs[i].T @ dz))
    d = dz @ Ws[i].T
ts = [Tensor(W) for W in Ws]
h = Tensor(x)
for t_ in ts:
    h = B2.sigmoid(h @ t_)
(h * h).mean().backward()
gnA = [float(np.linalg.norm(t_.grad)) for t_ in ts]
lv.claim(max(abs(a - b) / b for a, b in zip(gnA, gnB)) < 1e-9, 'hook gradient norms: autograd and the hand backward agree')
F5 = lv._file(L5)[1]
lv.claim(all(abs(F5['screens'][0]['canvas']['state']['values'][f'L{i + 1}'] - gnB[i]) <= 1e-3 * gnB[i] for i in range(10)), 'hook bars hold the ten gradient norms')
cov(gnB[0], gnB[9], gnB[9] / gnB[0], 64)
E(L5, 'screens[1].widget.answer', round(0.25 ** 10 / 1e-7, 1))
cov(0.25 ** 10, 4 ** 10, round(0.25 ** 9 / 1e-7, 1), 2.5)
E(L5, 'screens[2].widget.answer', round(1 - math.tanh(3) ** 2, 4))
cov(math.tanh(3), ds(3), 1 - math.tanh(3), 4 * 0.25)
chain = ds(0.5) * ds(-1) * ds(2) * ds(0)
E(L5, 'screens[3].widget.answer', float(f'{chain:.4g}'))
cov(ds(0.5), ds(-1), ds(2), ds(0.5) * ds(-1), ds(0.5) + ds(-1) + ds(2) + ds(0), 0.25 ** 4, 1 / chain, 800)
lv.claim(abs(1 / chain - 800) < 50, 'a factor of about 800')
E(L5, 'screens[4].widget.answer', sum(v <= 0 for v in (2.31, -0.47, 0.05, -1.92, 0.88, 0.0)))
cov(2.31, -0.47, 0.05, -1.92, 0.88, 200)
lv.literal('2.31', why='the dead-unit table is a stated example')
z52 = 0.0001 * 52000
E(L5, 'screens[7].widget.answer', round((1 - math.tanh(z52) ** 2) / 1e-4, 2))
cov(z52, math.tanh(z52), 1 - math.tanh(z52) ** 2, round((1 - math.tanh(z52)) / 1e-4, 2), 1 - math.tanh(0.3) ** 2, 52000, 0.0001)
E(L5, 'quiz[0].widget.answer', round(0.25 ** 6 / 1e-4, 2))
cov(4096, 0.25 ** 5 / 1e-4, 1.5)
cov(1000, 100, 0.1)

# ================= l6-initialisation =================
L6 = 'l6-initialisation'
ACT = {'tanh': np.tanh, 'relu': lambda z: np.maximum(z, 0), 'linear': lambda z: z}


def sd_by_layer(depth, width, w_sd, act, seed):
    gg = np.random.default_rng(seed)
    hh = gg.standard_normal((1000, width))
    out = []
    for _ in range(depth):
        hh = ACT[act](hh @ (gg.standard_normal((width, width)) * w_sd))
        out.append(float(hh.std()))
    return out


STOPS = [0.01, 0.03, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.5, 1.0]
lin = {s: sd_by_layer(10, 100, s, 'linear', 0) for s in STOPS}
for s in STOPS:
    theory = (100 * s * s) ** 5
    lv.claim(0.5 < lin[s][-1] / theory < 2.0, f'weight sd {s}: simulated sd after 10 layers {lin[s][-1]:.3g} near the theory {theory:.3g}')
    cov(float(f'{lin[s][-1]:.3g}'))
cov(lin[0.05][-1], lin[0.1][-1], lin[1.0][-1], lin[0.01][-1])
E(L6, 'screens[0].widget.answer', 0.1)
E(L6, 'screens[1].widget.answer', 100 * 1.0 ** 2)
cov(1e20, 1e10, 10)
E(L6, 'screens[2].widget.answer', 50 * 0.04 * 1)
gz = np.random.default_rng(0)
simv = float((gz.standard_normal((20000, 100)) * gz.standard_normal((20000, 100))).sum(1).var())
cov(simv, 0.2, 1 / math.sqrt(50), 20000)
lv.claim(abs(simv - 100) < 3, f'the 20,000-draw simulation is near 100 ({simv:.2f})')
E(L6, 'screens[3].widget.answer', round(math.sqrt(2 / 100), 4))
r141, r01 = sd_by_layer(10, 100, math.sqrt(0.02), 'relu', 0), sd_by_layer(10, 100, 0.1, 'relu', 0)
cov(r141[-1], r01[-1], 0.02, math.sqrt(0.5 / 100), math.sqrt(2))
zr = np.random.default_rng(5).standard_normal(400000)
agree('ReLU keeps half the second moment (simulation)', float(np.mean(np.maximum(zr, 0) ** 2)), 0.5, 0.01)


def sym_b(c, steps=100):
    X, y = spirals()
    Xb, yb = X[:32], y[:32]
    W1, b1, W2, b2 = np.full((2, 3), c), np.zeros(3), np.full((3, 2), c), np.zeros(2)
    for _ in range(steps):
        hh = np.tanh(Xb @ W1 + b1)
        z = hh @ W2 + b2
        p = np.exp(z - z.max(1, keepdims=True))
        p /= p.sum(1, keepdims=True)
        p[np.arange(32), yb] -= 1
        dz = p / 32
        dh = dz @ W2.T * (1 - hh ** 2)
        W2, b2, W1, b1 = W2 - 0.5 * hh.T @ dz, b2 - 0.5 * dz.sum(0), W1 - 0.5 * Xb.T @ dh, b1 - 0.5 * dh.sum(0)
    return W1


S05 = sym_b(0.5)
lv.claim(np.ptp(S05, axis=1).max() == 0.0 and np.abs(sym_b(0.0)).max() == 0.0, 'equal starts stay equal (0.5) and zero starts never move')
cov(*S05[:, 0].tolist(), 0.5)
E(L6, 'screens[7].widget.answer', round(0.8 * 0.5 ** 7, 6))
cov(0.8 * 0.25 ** 7, 0.8 * 0.5 ** 8, 0.8)
E(L6, 'quiz[0].widget.answer', math.sqrt(2 / 50))
E(L6, 'quiz[2].widget.answer', (100 * 0.2 ** 2) ** 10)
cov(2 ** 10, 0.04, 4)
lv.literal('1,000', why='the number of input rows in the hook, a stated choice')
lv.literal('1,048,576', why='4 to the tenth, stated in the quiz and checked by the key')

# ================= l7-batch-norm =================
L7 = 'l7-batch-norm'
SIZES = (2, 64, 64, 64, 64, 2)
Xs, ys = spirals()


def bn_route_b(h, gm, bt, run):
    mu = h.mean(axis=0, keepdims=True)
    dd = h - mu
    var = (dd * dd).mean(axis=0, keepdims=True)
    newrun = (0.9 * run[0] + 0.1 * mu.data[0], 0.9 * run[1] + 0.1 * var.data[0])
    return gm * (dd * (var + EPS) ** -0.5) + bt, newrun


def deep_run(bn, lr, seed, route):
    gg = np.random.default_rng(0)
    P = []
    for a, b in zip(SIZES[:-1], SIZES[1:]):
        P += [gg.standard_normal((a, b)) / math.sqrt(a), np.zeros(b)]
    G = [np.ones(64) for _ in range(4)] if bn else []
    Bt = [np.zeros(64) for _ in range(4)] if bn else []
    runs = [(np.zeros(64), np.ones(64)) for _ in range(4)]
    rng = np.random.default_rng(seed)
    for t in range(300):
        idx = rng.choice(400, 32, replace=False)
        tp, tg, tb = [Tensor(p) for p in P], [Tensor(p) for p in G], [Tensor(p) for p in Bt]
        hh, new = Tensor(Xs[idx]), []
        for i in range(5):
            hh = hh @ tp[2 * i] + tp[2 * i + 1]
            if i < 4:
                if bn:
                    if route == 'A':
                        hh, r = B2.batchnorm(hh, tg[i], tb[i], running=runs[i])
                    else:
                        hh, r = bn_route_b(hh, tg[i], tb[i], runs[i])
                    new.append(r)
                hh = hh.tanh()
        if bn:
            runs = new
        with np.errstate(all='ignore'):
            cross_entropy(hh, ys[idx]).backward()
        P = [p - lr * q.grad for p, q in zip(P, tp)]
        G = [p - lr * q.grad for p, q in zip(G, tg)]
        Bt = [p - lr * q.grad for p, q in zip(Bt, tb)]
    hh = Xs
    for i in range(5):
        hh = hh @ P[2 * i] + P[2 * i + 1]
        if i < 4:
            if bn:
                hh = G[i] * (hh - runs[i][0]) / np.sqrt(runs[i][1] + EPS) + Bt[i]
            hh = np.tanh(hh)
    with np.errstate(all='ignore'):
        zz = hh - hh.max(1, keepdims=True)
        return float(np.mean(np.log(np.exp(zz).sum(1)) - zz[np.arange(400), ys]))


bnA = [deep_run(True, 1.0, s, 'A') for s in (1, 2, 3, 4, 5)]
bnB = [deep_run(True, 1.0, s, 'B') for s in (1, 2, 3, 4, 5)]
plA = [deep_run(False, 1.0, s, 'A') for s in (1, 2, 3, 4, 5)]
print('batch-norm finals, op:', np.round(bnA, 4), 'composed:', np.round(bnB, 4))
# At step 1 the runs are sensitive to rounding (seed 1 ends 0.177 with the op and 0.194 composed), so the lesson states only the split.
lv.claim(min(plA) > 1 and max(bnA) < 0.25 and max(bnB) < 0.25, 'at step 1 the plain net ends above 1 nat on every seed and batch norm below 0.25, in both routes')
agree('batch norm at step 1, seed 2: op against composition', bnA[1], bnB[1], 1e-5)
cov(0.25, 1)
plS = [deep_run(False, 0.1, s, 'A') for s in (1, 2, 3)]
lv.claim(max(plS) < 0.2, 'at step 0.1 the plain net trains')
xb = np.array([2.0, 4.0, 6.0, 8.0])
xh8 = (8 - xb.mean()) / math.sqrt(xb.var() + EPS)
E(L7, 'screens[1].widget.answer', round(xh8, 4))
cov(xb.mean(), xb.var(), math.sqrt(5), 3 / 5, 3 / math.sqrt(xb.var(ddof=1)), 8 / math.sqrt(5), 1.34, 0.45)
E(L7, 'screens[2].widget.answer', round(2 * xh8 + 1, 4))
cov(xh8 + 2, 2 * xh8, math.sqrt(5), 5)
rm2 = 0.9 * (0.1 * 5) + 0.1 * 5
rv1 = 0.9 + 0.5
rv2 = 0.9 * rv1 + 0.5
E(L7, 'screens[3].widget.answer', round(rm2, 4))
cov(0.5, rv1, rv2, 0.45, 1.0)
inf8 = (8 - rm2) / math.sqrt(rv2 + EPS)
E(L7, 'screens[4].widget.answer', round(inf8, 3))
cov(8 - rm2, math.sqrt(rv2), xh8)
tr = 1.5 * 0.3 / math.sqrt(0.04 + EPS) + 0.1
E(L7, 'screens[8].widget.answer', round(tr, 2))
cov(1.5 * 0.3 + 0.1, 1.5 * 0.3 / 0.04 + 0.1, 0.3 / 0.2, 0.2)
q3 = np.array([1.0, 2.0, 6.0])
E(L7, 'quiz[0].widget.answer', round(3 / math.sqrt(q3.var() + EPS), 3))
cov(q3.var(), math.sqrt(q3.var()), 14 / 3)

# ================= l8-layer-norm =================
L8 = 'l8-layer-norm'
ex = np.array([1.0, 2.0, 3.0, 6.0])
E(L8, 'screens[1].widget.answer', round((6 - 3) / math.sqrt(ex.var() + EPS), 4))
cov(ex.var(), math.sqrt(ex.var()), 3 / math.sqrt(ex.var(ddof=1)), 3 / ex.var())
E(L8, 'screens[2].widget.answer', 32 * 10)
cov(32 * 10 * 64)
M = np.array([[1.0, 4.0, 7.0], [2.0, 5.0, 9.0], [3.0, 6.0, 14.0]])
lnM = (M - M.mean(1, keepdims=True)) / np.sqrt(M.var(1, keepdims=True) + EPS)
bnMT = ((M.T - M.T.mean(0)) / np.sqrt(M.T.var(0) + EPS)).T
lv.claim(np.allclose(lnM, bnMT), 'layer norm of X equals batch norm of X transposed, transposed back')
E(L8, 'quiz[1].widget.answer', 0.5)
E(L8, 'quiz[2].widget.answer', round(2 / math.sqrt(1.6 + EPS), 4))
cov(1.6, math.sqrt(1.6), 2 / math.sqrt(2.0), 2 / 1.6)
lv.literal('2,048', why='16 times 128, a count named in a distractor')

# ================= review, problems, homework =================
E('review', 'items[0].widget.answer', round(math.sqrt(2 / 72), 4))
cov(1 / 6, 1 / math.sqrt(72), 2 / 72, 1 / 36)
E('review', 'items[1].widget.answer', round(0.25 ** 5 / 1e-4, 2))
cov(1024, 0.25 ** 4 / 1e-4)
b3 = np.array([1.0, 2.0, 9.0])
E('review', 'items[2].widget.answer', round(5 / math.sqrt(b3.var() + EPS), 3))
cov(b3.var(), math.sqrt(b3.var()), 38 / 3)
E('review', 'items[4].widget.answer', round(1 - math.tanh(2) ** 2, 4))
cov(math.tanh(2), 1 / 15)
lv.claim(abs((1 - math.tanh(2) ** 2) - 1 / 15) < 0.005, 'tanh slope at 2 is about a fifteenth of its peak')
E('review', 'items[5].widget.answer', 64 * 0.25 ** 2)
cov(0.0625, 1 / 8, 16)
E('review', 'items[6].widget.answer', round(2 * (1 - 0.9 ** 3), 3))
cov(0.2, 0.38, 0.6, 160)
E('problems', 'items[0].parts[0].widget.answer', 256 * 0.01)
E('problems', 'items[0].parts[1].widget.answer', round(2.56 ** 5, 1))
cov(math.sqrt(2.56 ** 5), 25.6, 2.56 * 5, 2.56 ** 4)
E('problems', 'items[0].parts[2].widget.answer', 1 / math.sqrt(256))
E('problems', 'items[0].parts[3].widget.answer', round(math.sqrt(2 / 256), 4))
cov(1 / 256, math.sqrt(0.5 / 256))
E('problems', 'items[1].parts[0].widget.answer', round(ds(1), 4))
cov(sig(1), 1 - sig(1))
E('problems', 'items[1].parts[1].widget.answer', round(0.25 ** 8 / 1e-5, 2))
cov(65536, 0.25 ** 7 / 1e-5)
E('problems', 'items[1].parts[2].widget.answer', round(ds(1) ** 8 / 1e-6, 2))
cov(ds(1) ** 7 / 1e-6, 0.25 ** 8 / 1e-6, 0.25 ** 8 / ds(1) ** 8)
lv.claim(6 < 0.25 ** 8 / ds(1) ** 8 < 8, 'about seven times smaller')
xh7 = 3 / math.sqrt(5 + EPS)
E('problems', 'items[2].parts[0].widget.answer', round(xh7, 4))
E('problems', 'items[2].parts[1].widget.answer', round(0.5 * xh7 + 2, 4))
E('problems', 'items[2].parts[3].widget.answer', round(xh7, 4))
cov(3 / math.sqrt(20 / 3), 2 * xh7 + 0.5, 0.5 * xh7, 3.6, 0.4)
f6 = (100 * 0.12 ** 2) ** 6
E('homework', 'items[3].widget.answer', round(f6, 2))
cov(1.2 ** 6, 1.44, 0.0144)
lv.literal('100', why='layer width, a stated choice')
for lit in ('400', '300', '128', '256', '10^-7'):
    lv.literal(lit, why='a stated size, step count or unit in a question')
cov(float(f'{gnB[9] / gnB[0] / 1e6:.1f}'), 0.25, float(f'{0.25 ** 10:.1e}'), float(f'{1 - math.tanh(z52) ** 2:.2e}'), 2.44e-4, float(f'{lin[0.05][-1]:.1e}'), *STOPS,
    float(f'{lin[1.0][-1]:.1e}'), 8, 2, 72, 9.77e-4, 25, 20, 3, 2 / 256, 1.53e-5, 2.23e-6, 7)
lv.literal('10^-5', why='batch and layer norm epsilon, a stated setting')
lv.literal('10^-6', why='the gradient-check tolerance and step stated in how lines')
lv.literal('10^-9', why='the hidden tests\' comparison tolerance')
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

lv.claim(True, 'route B values', covers=COV)
lv.check_wrongs()
lv.report()
