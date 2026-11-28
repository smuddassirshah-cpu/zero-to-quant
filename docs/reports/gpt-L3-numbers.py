"""Recompute every number stated in gpt level 3 (Training on Tiny Shakespeare) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only gpt-L3
(NumPy only; strict coverage; about a minute and a half with one BLAS thread; exits 0 when every check passes).
`--write` trains the two-block model for interp L1 and writes gpt-w2-embed.json, gpt-w2-block0.json, gpt-w2-block1.json (then exits).

The one-block tiny GPT shipped by level 2 (gpt-w-embed.json, gpt-w-block0.json) is retrained here with a logging loop written
below (route A: the same recipe as docs/reports/gpt-L2-numbers.py) and compared with the shipped float32 weights and their
validation loss; gpt_ops_l3.train is checked against the same loop over its first steps. The two-block model uses the same recipe
(seed 0, Adam 0.003, 100 warm-up steps, cosine decay, 5,000 steps of 16 windows of 32 from the first 225,000 characters).
Every short run on screen (sweeps, the overfit test, the small GPT of the homework) is recomputed by gpt_ops_l3 and by the
logging loop. Bigram figures are recomputed by NumPy and by a pure-Python counter. Every code widget is run in CPython with the
page's judge (solution passes, starter fails, each mutant first fails its named test).
"""
import base64
import json
import math
import os
import shutil
import sys
import tempfile
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

sys.path.insert(0, DATA)
from autograd import Tensor, cross_entropy  # noqa: E402
from nt_ops_l1 import adam_step, warmup_cosine  # noqa: E402
import seq_ops_l4 as S4  # noqa: E402
import gpt_ops_l2 as G  # noqa: E402
import gpt_ops_l3 as G3  # noqa: E402

TXT = open(os.path.join(DATA, 'tiny-shakespeare.txt')).read()
IDS = np.array(G.encode(TXT))
TR, VA = IDS[:225000], IDS[225000:]
NVW = (len(VA) - 1) // 32
XV = VA[:NVW * 32].reshape(NVW, 32)
YV = VA[1:NVW * 32 + 1].reshape(NVW, 32)
CFG2 = dict(G.CONFIG, n_layer=2)


def run(config=None, steps=5000, lr=3e-3, warm=100, seed=0, bseed=1, B=16, T=32, heads=4, log_every=None):
    """Route A: the training loop written out, with Tensors kept between steps and zeroed each step."""
    w = G3.init_weights(seed, config)
    names = list(w)
    P = {k: Tensor(v) for k, v in w.items()}
    M = [np.zeros_like(P[k].data) for k in names]
    V = [np.zeros_like(P[k].data) for k in names]
    rng = np.random.default_rng(bseed)
    losses, log = [], []
    vocab = w['head_w'].shape[1]
    for t in range(1, steps + 1):
        ix = rng.integers(0, len(TR) - T, B)
        X = np.stack([TR[i:i + T] for i in ix])
        Y = np.stack([TR[i + 1:i + T + 1] for i in ix])
        for k in names:
            P[k].zero_grad()
        loss = cross_entropy(S4.lm_logits(X, G.to_model(P), heads).reshape(-1, vocab), Y.reshape(-1))
        loss.backward()
        rate = warmup_cosine(t, lr, warm, steps) if warm else lr
        new, M, V = adam_step([P[k].data for k in names], [P[k].grad for k in names], M, V, t, rate)
        for k, a in zip(names, new):
            P[k].data = a
        losses.append(loss.item())
        if log_every and t % log_every == 0:
            log.append(G.mean_loss({k: P[k].data for k in names}, XV, YV, heads))
    return {k: P[k].data for k in names}, losses, log


if '--write' in sys.argv:
    W2, _, _ = run(CFG2)
    names = [k for k, _ in G.shapes(CFG2)]
    files = {'gpt-w2-embed.json': [k for k in names if not k.startswith('h')],
             'gpt-w2-block0.json': [k for k in names if k.startswith('h0.')], 'gpt-w2-block1.json': [k for k in names if k.startswith('h1.')]}
    files['gpt-w2-embed.json'] = [k for k in names if not (k.startswith('h0.') or k.startswith('h1.'))]
    for fn, ks in files.items():
        with open(os.path.join(DATA, fn), 'w') as f:
            f.write(G.weights_json(W2, ks))
        print('wrote', fn, os.path.getsize(os.path.join(DATA, fn)))
    sys.exit(0)

lv = Level('gpt', 3, coverage='strict')
E = lv.expect
LIT = lv.literal


def F(fid):
    return lv._file(fid)[1]


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def two(label, a, b, tol=1e-9, covers=None):
    lv.claim(close(a, b, tol), f'{label}: two routes agree ({a!r} vs {b!r})', covers=[a] if covers is None else covers)
    return a


def sm(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def logsm(z):
    z = z - z.max(-1, keepdims=True)
    return z - np.log(np.exp(z).sum(-1, keepdims=True))


W = G.read_weights(os.path.join(DATA, 'gpt-w-embed.json'), os.path.join(DATA, 'gpt-w-block0.json'))


# ---------------- the long run: retrain the shipped model and log it ----------------
WR, LR_, VLOG = run(log_every=250)
lv.claim(max(float(np.abs(np.asarray(WR[k], '<f4') - W[k]).max()) for k in W) < 1e-4, 'retrained run matches the shipped float32 weights to 1e-4')
VAL = G.mean_loss(W, XV, YV)
two('validation loss: shipped weights and the retrained run', VAL, VLOG[-1], 1e-6)
TRAIN_MEANS = [round(float(np.mean(LR_[i:i + 250])), 3) for i in range(0, 5000, 250)]
lv.claim(F('l9')['screens'][7]['canvas']['params']['series'][0]['values'] == TRAIN_MEANS, 'l9 training curve: means of 250 batch losses (retrained run)', covers=TRAIN_MEANS)
lv.claim(np.allclose(F('l9')['screens'][7]['canvas']['params']['series'][1]['values'], np.round(VLOG, 3), atol=0.0015), 'l9 validation curve: the retrained run every 250 steps, to 3 places', covers=VLOG)
lv.claim(np.allclose(G3.train(G3.init_weights(0), TR, 20, 3e-3, seed=1)[1], run(steps=20, warm=0)[1], rtol=1e-10), 'gpt_ops_l3.train equals the written-out loop (20 steps, fixed rate)')
two2 = run(CFG2, steps=3, warm=0)[1]
lv.claim(np.allclose(G3.train(G3.init_weights(0, CFG2), TR, 3, 3e-3, seed=1)[1], two2, rtol=1e-10), 'two-block: gpt_ops_l3.train equals the loop (3 steps)')
W2 = G.read_weights(*[os.path.join(DATA, f) for f in ('gpt-w2-embed.json', 'gpt-w2-block0.json', 'gpt-w2-block1.json')])
V2 = G.mean_loss(W2, XV, YV)
lv.claim(sum(v.size for v in W2.values()) == 30721 and V2 < VAL - 0.02 and V2 < 2.4554, f'two-block model: 30,721 numbers, validation {V2:.4f} below the one-block {VAL:.4f}')
lv.claim(np.abs(G.forward_logits(W2, XV[:2]) - S4.lm_logits(XV[:2], G.to_model(W2), 4).data).max() < 1e-10, 'two-block forward: gpt_ops_l2 equals seq_ops_l4')
for fn in ('gpt-w2-embed.json', 'gpt-w2-block0.json', 'gpt-w2-block1.json'):
    lv.claim(os.path.getsize(os.path.join(DATA, fn)) < 262144, f'{fn} under 256 KB')

# ---------------- l9 ----------------
lv.claim(225000 - 32 - 1 == 224967 and int(np.random.default_rng(0).integers(0, 225000 - 32, 10 ** 5).max()) <= 224967, 'largest start 224,967', covers=[224967, 224968, 224999, 224966, 225000])
L40 = G3.train(G3.init_weights(0), TR, 40, 3e-3, seed=1)[1]
two('trainer: 40 steps', L40[-1], run(steps=40, warm=0)[1][-1], 1e-10, covers=[L40[0], L40[-1]])
toy = np.array([5, 1, 4, 1, 5, 9, 2, 6])
lv.claim(toy[[5, 6, 7]].tolist() == [9, 2, 6] and toy[[4, 5, 6]].tolist() == [5, 9, 2] and toy[[2, 3, 4]].tolist() == [4, 1, 5], 'toy batch rows')
m1, v1 = 0.1 * -0.2, 0.001 * 0.04
wa = 0.5 - 0.003 * (m1 / 0.1) / (math.sqrt(v1 / 0.001) + 1e-8)
wb = adam_step([np.array([0.5])], [np.array([-0.2])], [np.zeros(1)], [np.zeros(1)], 1, 0.003)[0][0][0]
two('Adam by hand', wa, float(wb), 1e-12, covers=[wa, 0.5006, 0.497, 0.003])
wq = adam_step([np.array([0.1])], [np.array([4.0])], [np.zeros(1)], [np.zeros(1)], 1, 0.01)[0][0][0]
lv.claim(abs(wq - 0.09) < 1e-6 and abs(0.1 - 0.01 * 4 - 0.06) < 1e-12, 'quiz Adam: 0.09; plain gradient descent slip 0.06', covers=[0.09, 0.06, 0.11])
XB, YB = G3.get_batch(TR, 16, 32, np.random.default_rng(0))
l0, g0 = G3.loss_and_grads(W, XB, YB)
st = G3.adam_init(W)
W1 = G3.adam_update(W, g0, st, 1e-3)
lt = cross_entropy(S4.lm_logits(XB, G.to_model({k: Tensor(v) for k, v in W.items()}), 4).reshape(-1, 65), YB.reshape(-1)).item()
two('one step: loss before', l0, lt, 1e-12)
two('one step: loss after', G.mean_loss(W1, XB, YB), float(cross_entropy(S4.lm_logits(XB, G.to_model({k: Tensor(v) for k, v in W1.items()}), 4).reshape(-1, 65), YB.reshape(-1)).item()), 1e-12)


def persistent(zero, steps=20, lr=3e-3):
    w = G3.init_weights(0)
    names = list(w)
    P = {k: Tensor(v) for k, v in w.items()}
    M = [np.zeros_like(P[k].data) for k in names]
    V = [np.zeros_like(P[k].data) for k in names]
    rng = np.random.default_rng(1)
    out = []
    for t in range(1, steps + 1):
        Xb, Yb = G3.get_batch(TR, 16, 32, rng)
        if zero:
            for k in names:
                P[k].zero_grad()
        loss = cross_entropy(S4.lm_logits(Xb, G.to_model(P), 4).reshape(-1, 65), Yb.reshape(-1))
        loss.backward()
        new, M, V = adam_step([P[k].data for k in names], [P[k].grad for k in names], M, V, t, lr)
        for k, a in zip(names, new):
            P[k].data = a
        out.append(loss.item())
    return out


ZE, NZ = persistent(True), persistent(False)
tr_ = F('l9')['screens'][6]['canvas']['params']['series']
lv.claim(tr_[0]['values'] == [round(x, 3) for x in ZE] and tr_[1]['values'] == [round(x, 3) for x in NZ], 'trap curves: zeroed and never zeroed', covers=[ZE[-1], NZ[-1], NZ[-1] - ZE[-1]])
lv.claim(ZE[:2] == NZ[:2] and ZE[2] != NZ[2], 'the two runs agree for two steps, then part')
lv.claim(np.allclose(ZE, run(steps=20, warm=0)[1]), 'zeroed persistent run equals the written-out loop')
lv.claim(16 * 32 == 512, 'batch of 16 windows: 512 predictions', covers=[512, 33])

# ---------------- l10 ----------------
HOOK = ((2.01) ** 3 - (1.99) ** 3) / 0.02
two('central difference by hand', HOOK, (8.120601 - 7.880599) / 0.02, 1e-9, covers=[HOOK, ((2.01) ** 3 - 8) / 0.01, 0.240002, HOOK * 0.02, 7.880599, 8.120601, 0.0001])
HS = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9]
E64 = [abs(((2 + h) ** 3 - (2 - h) ** 3) / (2 * h) - 12) for h in HS]
E64n = [abs(float((np.float64(2) + h) ** 3 - (np.float64(2) - h) ** 3) / (2 * h) - 12) for h in HS]
lv.claim(np.allclose(E64, E64n, rtol=1e-9, atol=0), 'float64 errors: Python floats and NumPy float64')
E32 = []
for h in HS[:6]:
    x32, h32 = np.float32(2), np.float32(h)
    E32.append(abs(float(((x32 + h32) ** 3 - (x32 - h32) ** 3) / (np.float32(2) * h32)) - 12))
pl = F('l10')['screens'][1]['canvas']['params']['functions']
lv.claim(np.allclose([p[1] for p in pl[0]['points']], np.log10(E64), atol=1e-4) and np.allclose([p[1] for p in pl[1]['points']], np.log10(E32), atol=1e-4), 'error curves plotted as log10', covers=E64 + E32)
lv.claim(int(np.argmin(E64)) == 4, 'smallest float64 error at h = 1e-5')
a_, b_ = np.array([1.0, 2.0]), np.array([1.0, 2.0001])
REL = float(np.linalg.norm(a_ - b_) / (np.linalg.norm(a_) + np.linalg.norm(b_)))
two('relative error example', REL, 1e-4 / (math.sqrt(5) + math.sqrt(1 + 2.0001 ** 2)), 1e-9, covers=[REL * 1e5, 1e-4 / math.sqrt(5) * 1e5, 10.0, math.sqrt(5), math.sqrt(1 + 2.0001 ** 2), 4.47223, 2.24])
lv.claim(round(0.2 + -0.5, 10) == -0.3, 'scatter-add: 0.2 + (-0.5)', covers=[0.3, 0.2, 0.5, 0.15])
TINY = {'V': 5, 'T': 4, 'd': 8, 'n_head': 2, 'n_layer': 1, 'mlp': 32}
XT = np.array([[0, 1, 2, 3], [3, 2, 1, 0]])
YT = np.array([[1, 2, 3, 4], [2, 1, 0, 4]])
lv.claim(sum(int(np.prod(s)) for _, s in G.shapes(TINY)) == 1005, 'tiny configuration: 1,005 numbers', covers=[1005])


def numgrad(f, x, h, one=False):
    g = np.zeros_like(x, dtype=float)
    for i in np.ndindex(x.shape):
        k = x[i]
        x[i] = k + h
        up = f()
        x[i] = k if one else k - h
        dn = f()
        x[i] = k
        g[i] = (up - dn) / (h if one else 2 * h)
    return g


def rel(a, b):
    d = np.linalg.norm(a) + np.linalg.norm(b)
    return 0.0 if d == 0 else float(np.linalg.norm(a - b) / d)


wt = G3.init_weights(0, TINY, sd=0.3)
_, gt = G3.loss_and_grads(wt, XT, YT, 2)
worst = {}
for lab, h, one, dt in [('f64', 1e-5, False, np.float64), ('f64-tiny-h', 1e-11, False, np.float64), ('f32', 1e-3, False, np.float32), ('one', 1e-5, True, np.float64)]:
    ww = {k: v.astype(dt) for k, v in wt.items()}
    worst[lab] = max(rel(gt[k], numgrad(lambda: G.mean_loss(ww, XT, YT, 2), ww[k], dt(h), one).astype(float)) for k in ww)
lv.claim(worst['f64'] < 1e-8 and 1e-5 < worst['f64-tiny-h'] < 1e-3 and 1e-3 < worst['f32'] < 1e-1 and 1e-5 < worst['one'] < 1e-4, f'trap table ranges: {worst}')
lv.claim(np.all(gt['wte'][4] == 0), 'unused row 4 of wte: gradient exactly 0', covers=[0])
lv.claim(2 * 18017 == 36034, '36,034 forward passes', covers=[36034, 18017, 18018])
lv.claim(abs((3.1 ** 2 - 2.9 ** 2) / 0.2 - 6) < 1e-12 and abs((3.1 ** 2 - 9) / 0.1 - 6.1) < 1e-9, 'quadratic: central exact 6, one-sided 6.1', covers=[6, 6.1, 9])
lv.claim(abs(1 / 3 - 0.3333) < 1e-4, 'doubled gradient: a third', covers=[1 / 3, 0.5, 1.0])

# ---------------- l11 ----------------
LRS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
SW = {lr: G3.train(G3.init_weights(0), TR, 10, lr, seed=1)[1] for lr in LRS}
lv.claim(all(np.allclose(SW[lr], run(steps=10, lr=lr, warm=0)[1], rtol=1e-10) for lr in (1e-4, 1e-2, 1e-1)), 'sweep: gpt_ops_l3.train equals the loop at three rates')
LAST = {lr: SW[lr][-1] for lr in LRS}
fr = F('l11')['screens'][1]['canvas']['controls'][0]['frames']
lv.claim(all(np.allclose(fr[i]['series']['s']['values'], SW[lr], atol=0.002) for i, lr in enumerate(LRS)), 'sweep frames (to 0.002; the 0.1 run is erratic)', covers=list(LAST.values()) + [max(SW[1e-1])] + [x for lr in LRS for x in SW[lr]])
lv.claim(min(LAST, key=LAST.get) == 1e-2 and max(SW[1e-1]) > 6.9, 'best rate 0.01; 0.1 spiked above 6.9', covers=[6.9, 0.01, 0.003])
Xo, Yo = G3.get_batch(TR, 4, 32, np.random.default_rng(5))


def over(seed, lr, steps):
    w = G3.init_weights(seed)
    s_ = G3.adam_init(w)
    out = []
    for _ in range(steps):
        l, g = G3.loss_and_grads(w, Xo, Yo)
        w = G3.adam_update(w, g, s_, lr)
        out.append(l)
    return w, out


WO, LO = over(0, 1e-2, 100)
_, LO3 = over(0, 3e-3, 100)
_, LO1 = over(1, 1e-2, 100)
VALO = G3.eval_loss(WO, VA)
two('overfit model on validation', VALO, G.mean_loss(WO, XV, YV), 1e-12, covers=[VALO, LO[-1], LO[0], LO3[-1]])
lv.claim(LO[-1] < 0.01 and LO1[-1] < 0.01 and 4 * 32 == 128, 'overfit thresholds 0.01 hold for seeds 0 and 1; 128 characters', covers=[0.01, 128])
lv.claim(F('l11')['screens'][4]['canvas']['params']['series'][1]['values'] == [round(x, 4) for x in LO], 'overfit curve')
lv.claim(f'{LO[0]:.6f}' == '4.175866', 'flat run prints the first overfit loss to 6 places', covers=[4.175866, round(LO[0], 4)])
lv.claim(round(1.1 * 4.1792, 3) > 4.5 and 0.98 * 4.0 == 3.92, 'diagnosis thresholds', covers=[0.98, 1.1, 0.1, 0.02, 4.0])
LIT('5.9', why='the colleague\'s starting loss, a given of the scenario')
lv.claim(abs(math.log(96) - 4.56) < 0.005, 'ln 96 is 4.56', covers=[4.56, 4.57])
LIT('7.9', why='a given validation loss in the quiz scenario')
LIT('0.002', why='a given training loss in the quiz scenario')

# ---------------- l12 ----------------
C = np.zeros((65, 65))
np.add.at(C, (TR[:-1], TR[1:]), 1)
cnt = Counter(zip(TXT[:224999], TXT[1:225000]))
q, u = G.encode('q')[0], G.encode('u')[0]
lv.claim(C[q].sum() == 102 == cnt[('q', 'u')] == sum(v for (a, _), v in cnt.items() if a == 'q'), 'q appears 102 times before the end, always followed by u', covers=[102, 103, 167])
PQU = 103 / 167
lv.claim(close(PQU, (C[q, u] + 1) / (C[q] + 1).sum()), 'add-one chance of u after q', covers=[PQU, 102 / 167, 1.0])
PA = {a: (102 + a) / (102 + 65 * a) for a in (0.01, 0.1, 1, 10)}
lv.claim(all(close(PA[a], (C[q, u] + a) / (C[q] + a).sum()) for a in PA), 'smoothing frames', covers=list(PA.values()) + [(1 - PA[a]) / 64 for a in PA] + [6.5, 0.01, 10])


def bigram_py(train_txt, val_txt, alpha):
    c = Counter(zip(train_txt[:-1], train_txt[1:]))
    rows = Counter(train_txt[:-1])
    tot = 0.0
    for a, b in zip(val_txt[:-1], val_txt[1:]):
        tot -= math.log((c[(a, b)] + alpha) / (rows[a] + 65 * alpha))
    return tot / (len(val_txt) - 1)


BG = two('bigram validation, add-one (NumPy and a counter)', G3.bigram_loss(TR, VA), bigram_py(TXT[:225000], TXT[225000:], 1.0))
BGT = two('bigram on its training part', G3.bigram_loss(TR, TR), bigram_py(TXT[:225000], TXT[:225000], 1.0))
BG01 = two('bigram validation, alpha 0.1', G3.bigram_loss(TR, VA, 0.1), bigram_py(TXT[:225000], TXT[225000:], 0.1))
two('bigram in bits (division by ln 2 and log2 of e^loss)', BG / math.log(2), math.log2(math.exp(BG)), covers=[BG / math.log(2), BG * math.log(2), 4.1744, 6.0224])
GV = two('GPT validation (eval_loss and the windows)', G3.eval_loss(W, VA), VAL)
GAPB = (BG - GV) / math.log(2)
two('gap in bits', GAPB, BG / math.log(2) - GV / math.log(2), covers=[GAPB, BG - GV, BG / GV])
lv.claim(abs(GAPB * NVW * 32 - 24000) < 500 and NVW * 32 == 24992, 'about 24,000 bits saved over 24,992 predictions', covers=[24000, 24992, 24999, 25000])
UNSEEN = int((C[VA[:-1], VA[1:]] == 0).sum())
cu = sum(1 for a, b in zip(TXT[225000:-1], TXT[225001:]) if cnt[(a, b)] == 0)
lv.claim(UNSEEN == cu == 45 and len({(a, b) for a, b in zip(TXT[225000:-1], TXT[225001:]) if cnt[(a, b)] == 0}) == 19, '45 unseen validation pairs of 19 kinds', covers=[45, 19, 0.002])
nll = -np.take_along_axis(logsm(G.forward_logits(W, XV)), YV[..., None], -1)[..., 0]
SD = float(nll.ravel().std(ddof=1))
SE200 = two('standard error on 200 characters', SD / math.sqrt(200), SD / 14.142135623730951, covers=[SD, SD / math.sqrt(200), SD / math.sqrt(nll.size), SD / 200, 14.14])
lv.claim(abs(SE200 / (BG - GV) - 1 / 6) < 0.01, 'a sixth of the gap')
BYPOS = nll.mean(0)
lv.claim(F('l12')['screens'][8]['canvas']['params']['series'][0]['values'] == [round(float(v), 3) for v in BYPOS], 'context curve', covers=[BYPOS[0], float(np.mean(BYPOS[8:]))])
P1 = (C + 1) / (C + 1).sum(1, keepdims=True)
rg = np.random.default_rng(0)
ids = [G.encode('F')[0]]
for _ in range(120):
    ids.append(int(rg.choice(65, p=P1[ids[-1]])))
cons = F('l12')['screens'][10]['canvas']['params']['lines']
lv.claim('\n'.join(cons) == '\n'.join(['bigram:', *G.decode(ids).split('\n'), '', 'tiny GPT:', *G.sample_text(W, 'F', 120, 1.0, None, 0).split('\n')]), 'samples: seeded bigram and GPT', covers=[120])
lv.claim(13 / 95 - 0.1368 < 5e-5 and 12 / 30 == 0.4 and abs(13 / 31 - 0.4194) < 5e-5, 'quiz add-one j', covers=[13 / 95, 0.4, 13 / 31, 12, 30, 95])
lv.claim((1.5 / 0.01) ** 2 == 22500 and 1.5 / 0.01 == 150 and 150 ** 2 == 22500, 'quiz standard error', covers=[22500, 150, 2250, 1.5, 0.01])
lv.claim(f'{BGT:.4f}' in F('l12')['screens'][6]['prose'] and f'{TRAIN_MEANS[-1]:.2f}' in F('l12')['screens'][6]['prose'], 'trap figures', covers=[BGT, TRAIN_MEANS[-1], BGT - TRAIN_MEANS[-1]])
LIT('0.80', why='the researcher\'s stated error, a given of the scenario')
LIT('0.78', why='a hypothetical baseline error in the explanation')

# ---------------- review, homework, problems ----------------
lv.claim(10000 - 65 == 9935 and 9999 - 64 == 9935, 'r-maxstart', covers=[9935, 9936, 9999, 10000])
lv.claim(abs(adam_step([np.array([0.2])], [np.array([0.05])], [np.zeros(1)], [np.zeros(1)], 1, 0.01)[0][0][0] - 0.19) < 1e-6, 'r-adam 0.19', covers=[0.19, 0.1995, 0.21])
two('r-central', math.sinh(0.1) / 0.1, (math.exp(0.1) - math.exp(-0.1)) / 0.2, covers=[math.sinh(0.1) / 0.1, (math.exp(0.1) - 1) / 0.1])
rr = 0.4 / (math.hypot(0.3, 0.8) + 0.5)
two('r-relerr', rr, np.linalg.norm([0, 0.4]) / (np.linalg.norm([0.3, -0.8]) + np.linalg.norm([0.3, -0.4])), covers=[rr, 0.8, 0.8544, 0.5])
two('r-gap', 0.56 / math.log(2), (2.46 - 1.90) / math.log(2), covers=[0.56 / math.log(2), 0.56, 0.56 * math.log(2)])
SMALL = {'V': 65, 'T': 16, 'd': 16, 'n_head': 2, 'n_layer': 1, 'mlp': 64}


def small_run(steps, lr, seed):
    w = G3.init_weights(seed, SMALL)
    s_ = G3.adam_init(w)
    rng = np.random.default_rng(seed + 1)
    out = []
    for _ in range(steps):
        X, Y = G3.get_batch(TR, 8, 16, rng)
        l, g = G3.loss_and_grads(w, X, Y, 2)
        w = G3.adam_update(w, g, s_, lr)
        out.append(l)
    return w, out


def val16(w):
    v = VA[:2001]
    n = (len(v) - 1) // 16
    return G.mean_loss(w, v[:n * 16].reshape(n, 16), v[1:n * 16 + 1].reshape(n, 16), 2)


v60 = [val16(small_run(60, 0.01, s)[0]) for s in (0, 1)]
lv.claim(max(v60) < 3.2, f'homework threshold 3.2 holds for seeds 0 and 1 ({v60})', covers=[3.2, v60[0], 4.17, 2000])
SR = {lr: small_run(10, lr, 0)[1] for lr in [1e-4, 1e-3, 1e-2, 3e-2, 1e-1, 3e-1, 1.0]}
pre = F('homework')['items'][1]['widget']['prelude']
ns_ = {}
exec(pre, ns_)
lv.claim(all(np.allclose(ns_['_RUNS'][lr], SR[lr], rtol=1e-9) for lr in SR if lr < 0.5) and all(max(ns_['_RUNS'][lr]) > 1.1 * ns_['_RUNS'][lr][0] and max(SR[lr]) > 1.1 * SR[lr][0] for lr in (1.0,)), 'find_lr: recorded stable runs equal fresh small runs; the rate-1 run diverges in both (no exact figure)')
lv.claim(abs(1.5 / math.sqrt(300) - 0.087) < 0.0005 and abs(2.38 - 1.62 - 0.76) < 1e-12, 'h-bits-gap', covers=[1.5 / math.sqrt(300), 0.76, 0.005])
for t_, why in [('4.10', 'a given sweep loss'), ('3.80', 'a given sweep loss'), ('3.20', 'a given sweep loss'), ('3.05', 'a given sweep loss'), ('4.15', 'a given starting loss'),
                ('1.62', 'a given loss'), ('2.38', 'a given loss'), ('300', 'a given text length'), ('2.48', 'nanoGPT full-text bigram from the brief: 2.4819, the planner\'s figure'),
                ('1,115,394', 'the full Tiny Shakespeare length, checked in gpt-L1-numbers.py'), ('384', 'a nanoGPT config width, a given'), ('256', 'a nanoGPT config context, a given'), ('0.8', 'a sampling temperature, a setting')]:
    LIT(t_, why=why)
two('problems ln 80', math.log(80), math.log2(80) * math.log(2), covers=[math.log(80), math.log2(80), math.log(65), 4.38, 6.32])
lv.claim(abs(adam_step([np.array([0.05])], [np.array([-0.3])], [np.zeros(1)], [np.zeros(1)], 1, 0.002)[0][0][0] - 0.052) < 1e-6, 'p1 Adam 0.052', covers=[0.052, 0.0506, 0.048])
two('p1 bits (division by ln 2 and log2 of e^loss)', 1.95 / math.log(2), math.log2(math.exp(1.95)), covers=[1.95 / math.log(2), 1.95 * math.log(2), (2.52 - 1.95) / math.log(2), 0.57, 2.52 / math.log(2) - 1.95])
L = lambda w: w ** 3 - w  # noqa: E731
lv.claim(abs(3 * 0.16 - 1 + 0.52) < 1e-12 and abs((L(0.5) - L(0.3)) / 0.2 + 0.51) < 1e-9 and abs((L(0.5) - L(0.4)) / 0.1 + 0.39) < 1e-9 and abs(L(0.5) + 0.375) < 1e-12 and abs(L(0.3) + 0.273) < 1e-12,
         'p2: slope -0.52, central -0.51, one-sided -0.39', covers=[0.52, 0.51, 0.39, 0.375, 0.273, 0.336, 0.48, 0.064 - 0.4, 0.01])
lv.claim(abs(0.26 / 0.78 - 1 / 3) < 1e-12, 'p2 relative error', covers=[0.26, 0.78, 0.3333])
lv.claim(abs(0.05 / 4.38 - 0.0114) < 5e-5 and abs(4.38 - 4.33 - 0.05) < 1e-12, 'p3 share 1.1%', covers=[0.05 / 4.38, 0.05, 4.33, 0.02])
LIT('6.1', why='the run\'s printed first loss, a given')

# ---------------- givens, counts and the printed forms of computed figures ----------------
lv.claim(len(L40) == 40 and len(ZE) == 20 and len(LR_) == 5000 and len(VLOG) == 5000 // 250 and NVW == 781 and 32 - 1 == 31, 'run lengths: 40, 20, 5,000 steps, a point every 250; 781 windows; 31 of 32',
         covers=[40, 20, 5000, 250, 781, 31])
lv.claim(XB.shape == (16, 32) and SMALL['d'] == 16 and abs(2.0 - 0.01 - 1.99) < 1e-12 and abs(0.3 / 0.02 - 15) < 1e-12, 'batch of 16, width 16, 1.99, scale 15', covers=[16, 1.99, 15, 2])
lv.claim(len(v60) == 2 and abs(math.log(2) - 0.6931) < 5e-5 and 65 - 1 == 64, '60-step runs; ln 2; 64 other characters', covers=[60, 0.6931, 64, 65, 80, 96, 200, 2.52, 1e-4 * 3])
caps = [f_['caption'] for f_ in F('l10')['screens'][1]['canvas']['controls'][0]['frames']]


def sci(e):
    m_, x_ = f'{e:.1e}'.split('e')
    return f'${m_} \\times 10^{{{int(x_)}}}$'


want = [f'$h = 10^{{-1}}$: error {sci(E64[0])} in float64, {sci(E32[0])} in float32.', f'$h = 10^{{-3}}$: error {sci(E64[2])} in float64, {sci(E32[2])} in float32.',
        f'$h = 10^{{-5}}$: error {sci(E64[4])} in float64, {sci(E32[4])} in float32.', f'$h = 10^{{-7}}$: error {sci(E64[6])} in float64.']
lv.claim(caps == want, 'explore captions print the computed errors', covers=caps)
fbc = F('l10')['screens'][2]['feedback']['correct']
lv.claim(f'{REL * 1e5:.3f}' in fbc, 'relative error printed in units of 1e-5', covers=[fbc])
LIT('2 \\times 10^{-9}', why='a given figure of the review scenario (float64 check result)')
LIT('5 \\times 10^{-3}', why='a given figure of the review scenario (float32 check result)')


# ---------------- code widgets: solution passes, starter fails, each mutant first fails its named test ----------------
def judge(a, ex, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def cl(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(cl(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(cl(p_, q_) for p_, q_ in zip(x, yv))
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(yv), rel_tol=rt, abs_tol=at) or float(x) == float(yv)
        except Exception:
            return x == yv

    def same(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x, yv))
        return bool(x == yv)
    return cl(a, ex) if cmp == 'isclose' else same(a, ex)


MODS = ('autograd', 'seq_ops_l2', 'seq_ops_l3', 'seq_ops_l4', 'nt_ops_l1', 'nt_ops_l2', 'gpt_ops_l2', 'gpt_ops_l3')


def purge():
    for m_ in [m_ for m_ in sys.modules if m_ in MODS]:
        sys.modules.pop(m_)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    try:
        for kk, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(dd, kk))
        sys.path.insert(0, dd)
        purge()
        ns_ = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns_)
                exec((w.get('prelude') or '') + '\n', ns_)
                exec(src, ns_)
                exec((w.get('postlude') or '') + '\n', ns_)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns_)
                    got = eval(c['call'], ns_)
                    t = c.get('tol')
                    ok = judge(got, eval(c['expect'], ns_), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception:
                ok = False
            if not ok:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        sys.path.remove(dd)
        shutil.rmtree(dd, ignore_errors=True)
        purge()
        sys.path.insert(0, DATA)


nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab = f'{fid} {u.get("title") or u.get("id")}'
        for k_, v_ in (w.get('data') or {}).items():
            if k_.endswith('.py'):
                lv.claim(open(os.path.join(APP, v_), 'rb').read() == open(os.path.join(DATA, k_), 'rb').read(), f'{lab}: ships {k_} byte-identical')
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')

for t_, why in [('10^-6', 'test tolerances and the gradient-check bar'), ('10^-9', 'test tolerances'), ('10^-12', 'test tolerances'), ('10^-13', 'a test floor'), ('10^-5', 'the step h'), ('10^-8', 'Adam epsilon'), ('10^-11', 'a step h in the table'), ('10^-3', 'a step h and a range end'), ('10^-4', 'a range end'), ('10^-2', 'a range end'), ('10^-1', 'a range end'), ('10^-7', 'float32 epsilon, order of magnitude')]:
    LIT(t_, why=why)
lv.check_wrongs()
lv.report()
