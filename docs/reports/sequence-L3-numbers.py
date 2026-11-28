"""Recompute every number stated in sequence level 3 (Self-attention) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only sequence-L3
(NumPy only; about a minute; strict coverage; exits 0 when every check passes).
`--write` retrains the names model and rewrites app/content/data/ai/sequence-attn-names.json (then exits).

The causal self-attention model (width 32, context 8, one or 4 heads, learned positions, a linear readout over makemore's
27 symbols, no residual) is trained here with a hand-written NumPy backward pass and Adam, from seed 0, 3,000 steps of 64
windows; route B checks that backward pass against autograd.py with seq_ops_l2.py and seq_ops_l3.py on a batch, recomputes
the dev loss of the shipped (rounded) weights with the autograd forward, and retrains seeds 1 and 2 to assert the threshold.
The bigram's 2.4514 nats on the dev names is recomputed from makemore's split. The new module seq_ops_l3.py is
gradient-checked. Every code widget is run in CPython with the page's judge (solution, starter, mutants).
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
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

sys.path.insert(0, DATA)
from autograd import Tensor, grad_check  # noqa: E402
import seq_ops_l2 as S2  # noqa: E402
import seq_ops_l3 as S3  # noqa: E402

WFILE = os.path.join(DATA, 'sequence-attn-names.json')

# ---------------- the causal self-attention model on names (trained here; --write ships the weights) ----------------
NAMES = open(os.path.join(DATA, 'names.txt')).read().splitlines()
SYM = '.abcdefghijklmnopqrstuvwxyz'
IX = {c: i for i, c in enumerate(SYM)}
_perm = np.random.default_rng(42).permutation(len(NAMES))
TRN = [NAMES[i] for i in _perm[:25626]]
DEV = [NAMES[i] for i in _perm[25626:28829]]
CTX, WIDTH = 8, 32


def windows(names):
    """Rows of 8 tokens and 8 targets (-1 = not scored). Each next symbol of each name, the end mark included, is scored once, with up to 8 tokens of context."""
    Xs, Ys = [], []
    for w in names:
        x = [0] + [IX[c] for c in w]
        y = [IX[c] for c in w] + [0]
        n = len(x)
        Xs.append(x[:CTX] + [0] * (CTX - min(n, CTX)))
        Ys.append(y[:CTX] + [-1] * (CTX - min(n, CTX)))
        for j in range(CTX, n):
            Xs.append(x[j - CTX + 1:j + 1])
            Ys.append([-1] * (CTX - 1) + [y[j]])
    return np.array(Xs), np.array(Ys)


def init_model(seed):
    g = np.random.default_rng(seed)
    s = 1 / math.sqrt(WIDTH)
    return {'E': g.standard_normal((27, WIDTH)) * 0.3, 'P': g.standard_normal((CTX, WIDTH)) * 0.3,
            'Wq': g.standard_normal((WIDTH, WIDTH)) * s, 'Wk': g.standard_normal((WIDTH, WIDTH)) * s, 'Wv': g.standard_normal((WIDTH, WIDTH)) * s,
            'Wo': g.standard_normal((WIDTH, WIDTH)) * s, 'U': g.standard_normal((WIDTH, 27)) * s, 'c': np.zeros(27)}


def np_forward(p, X, heads, mask=True, pos=True, cache=False):
    """logits (B, T, 27) of: x = E[tok] + P[pos]; heads of scaled causal attention; merge; Wo; readout U, c."""
    X = np.asarray(X)
    B, Tn = X.shape
    hd = WIDTH // heads
    x = p['E'][X] + (p['P'][:Tn] if pos else 0.0)
    q, k, v = x @ p['Wq'], x @ p['Wk'], x @ p['Wv']
    sh = lambda a: a.reshape(B, Tn, heads, hd).transpose(0, 2, 1, 3)  # noqa: E731
    qh, kh, vh = sh(q), sh(k), sh(v)
    S = qh @ kh.transpose(0, 1, 3, 2) / math.sqrt(hd)
    if mask:
        S = S + np.triu(np.full((Tn, Tn), -np.inf), 1)
    S = S - S.max(-1, keepdims=True)
    A = np.exp(S)
    A /= A.sum(-1, keepdims=True)
    o = (A @ vh).transpose(0, 2, 1, 3).reshape(B, Tn, WIDTH)
    hh = o @ p['Wo']
    logits = hh @ p['U'] + p['c']
    return (logits, (x, qh, kh, vh, A, o, hh)) if cache else logits


def nll_rows(logits, Y):
    m = Y >= 0
    L = logits - logits.max(-1, keepdims=True)
    lse = np.log(np.exp(L).sum(-1))
    return (lse - np.take_along_axis(L, np.where(m, Y, 0)[..., None], -1)[..., 0]) * m, m, L, lse


def np_loss_grad(p, X, Y, heads, mask=True):
    B, Tn = X.shape
    hd = WIDTH // heads
    logits, (x, qh, kh, vh, A, o, hh) = np_forward(p, X, heads, mask, cache=True)
    nll, m, L, lse = nll_rows(logits, Y)
    n = m.sum()
    P_ = np.exp(L - lse[..., None])
    P_[np.arange(B)[:, None], np.arange(Tn)[None], np.where(m, Y, 0)] -= 1
    dlog = P_ * m[..., None] / n
    g = {'U': hh.reshape(-1, WIDTH).T @ dlog.reshape(-1, 27), 'c': dlog.sum((0, 1))}
    dh = dlog @ p['U'].T
    g['Wo'] = o.reshape(-1, WIDTH).T @ dh.reshape(-1, WIDTH)
    doh = (dh @ p['Wo'].T).reshape(B, Tn, heads, hd).transpose(0, 2, 1, 3)
    dA = doh @ vh.transpose(0, 1, 3, 2)
    dvh = A.transpose(0, 1, 3, 2) @ doh
    dS = A * (dA - (dA * A).sum(-1, keepdims=True)) / math.sqrt(hd)
    un = lambda a: a.transpose(0, 2, 1, 3).reshape(B, Tn, WIDTH)  # noqa: E731
    dq, dk, dv = un(dS @ kh), un(dS.transpose(0, 1, 3, 2) @ qh), un(dvh)
    xf = x.reshape(-1, WIDTH)
    g['Wq'], g['Wk'], g['Wv'] = xf.T @ dq.reshape(-1, WIDTH), xf.T @ dk.reshape(-1, WIDTH), xf.T @ dv.reshape(-1, WIDTH)
    dx = dq @ p['Wq'].T + dk @ p['Wk'].T + dv @ p['Wv'].T
    g['E'] = np.zeros_like(p['E'])
    np.add.at(g['E'], X, dx)
    g['P'] = np.zeros_like(p['P'])
    g['P'][:Tn] = dx.sum(0)
    return float(nll.sum() / n), g


def train_model(seed, heads, steps=3000, lr=3e-3, bs=64, mask=True, record=False):
    p = init_model(seed)
    rng = np.random.default_rng(seed)
    mo = {k: np.zeros_like(v) for k, v in p.items()}
    ve = {k: np.zeros_like(v) for k, v in p.items()}
    hist = []
    for t in range(1, steps + 1):
        ix = rng.integers(0, len(XTR), bs)
        loss, g = np_loss_grad(p, XTR[ix], YTR[ix], heads, mask)
        hist.append(loss)
        for k in p:
            mo[k] = 0.9 * mo[k] + 0.1 * g[k]
            ve[k] = 0.999 * ve[k] + 0.001 * g[k] ** 2
            p[k] -= lr * (mo[k] / (1 - 0.9 ** t)) / (np.sqrt(ve[k] / (1 - 0.999 ** t)) + 1e-8)
    return (p, hist) if record else p


def np_dev_loss(p, X, Y, heads, mask=True, pos=True):
    tot, n = 0.0, 0
    for i in range(0, len(X), 2048):
        nll, m, _, _ = nll_rows(np_forward(p, X[i:i + 2048], heads, mask, pos), Y[i:i + 2048])
        tot += float(nll.sum())
        n += int(m.sum())
    return tot / n, n


XTR, YTR = windows(TRN)
XDV, YDV = windows(DEV)


def rounded(p):
    return {k: np.round(v, 6) for k, v in p.items()}


if '--write' in sys.argv:
    out = {'about': 'sequence level 3: one causal self-attention layer over makemore names (width 32, context 8, learned positions, linear readout, no residual), '
                    'trained by docs/reports/sequence-L3-numbers.py --write: seed 0, Adam 0.003, 3,000 steps of 64 windows; weights rounded to 6 places. '
                    'Weights trained on Andrej Karpathy\'s makemore names list (MIT licence).',
           'vocab': SYM, 'context': CTX, 'width': WIDTH}
    for heads in (1, 4):
        pm = rounded(train_model(0, heads))
        out[f'h{heads}'] = {k: v.tolist() for k, v in pm.items()}
        out[f'dev_h{heads}'] = round(np_dev_loss(pm, XDV, YDV, heads)[0], 6)
    with open(WFILE, 'w') as f:
        json.dump(out, f, separators=(',', ':'))
    print('wrote', WFILE, os.path.getsize(WFILE), 'bytes', out['dev_h1'], out['dev_h4'])
    sys.exit(0)


lv = Level('sequence', 3, coverage='strict')
E = lv.expect
LIT = lv.literal
LN2 = math.log(2)
e = math.e


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a), abs(b)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


def F(fid):
    return lv._file(fid)[1]


def sm(s, axis=-1):
    s = np.asarray(s, float)
    z = np.exp(s - s.max(axis=axis, keepdims=True))
    return z / z.sum(axis=axis, keepdims=True)


# ---------------- frozen and new modules ----------------
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'autograd.py'), 'rb').read()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'seq_ops_l2.py'), 'rb').read()).hexdigest().startswith('fa2bed08afe4'), 'seq_ops_l2.py is level 2\'s, unchanged')
OPS = open(os.path.join(DATA, 'seq_ops_l3.py'), 'rb').read()
print('seq_ops_l3.py SHA-256', hashlib.sha256(OPS).hexdigest(), len(OPS), 'bytes')
g = np.random.default_rng(0)
A_ = Tensor(g.standard_normal((2, 3, 4)))
Wt = g.standard_normal((4, 2, 3))
lv.claim(grad_check(lambda: (S3.permute(A_, (2, 0, 1)) * Wt).sum(), [A_]) < 1e-6, 'permute: gradient against central differences')
Xs = Tensor(g.standard_normal((5, 8)))
lv.claim(np.array_equal(S3.merge_heads(S3.split_heads(Xs, 4)).data, Xs.data) and S3.split_heads(Xs, 4).shape == (4, 5, 2), 'split then merge is the identity; (5, 8) splits to (4, 5, 2)')
lv.claim(np.array_equal(S3.split_heads(Xs, 4).data[2], Xs.data[:, 4:6]), 'head 2 holds features 4 and 5')
W3 = g.standard_normal((4, 5, 2))
lv.claim(grad_check(lambda: (S3.split_heads(Xs, 4) * W3).sum(), [Xs]) < 1e-6, 'split_heads: gradient')
Xb = Tensor(g.standard_normal((2, 5, 8)))
W4 = g.standard_normal((2, 5, 8))
lv.claim(grad_check(lambda: (S3.merge_heads(S3.split_heads(Xb, 2)) * W4).sum(), [Xb]) < 1e-6, 'split and merge on a batch: gradient')
Qt, Kt, Vt = (Tensor(g.standard_normal((2, 6, 4))) for _ in range(3))
Wv = g.standard_normal((2, 6, 4))
lv.claim(grad_check(lambda: (S3.attention(Qt, Kt, Vt, S3.causal_mask(6)) * Wv).sum(), [Qt, Kt, Vt]) < 1e-6, 'masked attention: gradient with the mask fixed')
cm = S3.causal_mask(32)
lv.claim(int((cm == 0).sum()) == 32 * 33 // 2 == 528 and int(np.isneginf(cm).sum()) == 496, 'causal_mask(32): 528 zeros, 496 at -inf', covers=[528, 496])
lv.claim(int((S3.causal_mask(4) == 0).sum()) == 10, 'causal_mask(4): 10 allowed pairs')

# ---------------- the model: hand backward against the autograd; shipped weights ----------------


def ag_loss(P, X, Y, heads):
    T = X.shape[1]
    x = P['E'][X] + P['P'][np.arange(T)]
    q, k, v = (S3.split_heads(x @ P[w], heads) for w in ('Wq', 'Wk', 'Wv'))
    h = S3.merge_heads(S3.attention(q, k, v, S3.causal_mask(T))) @ P['Wo']
    z = (h @ P['U'] + P['c']).reshape(-1, 27)
    keep = Y.reshape(-1) >= 0
    from autograd import cross_entropy
    return cross_entropy(z[np.nonzero(keep)[0]], Y.reshape(-1)[keep])


for heads in (1, 4):
    pm = init_model(3)
    Xb_, Yb_ = XTR[:40], YTR[:40]
    lh, gh = np_loss_grad(pm, Xb_, Yb_, heads)
    P = {k: Tensor(v.copy()) for k, v in pm.items()}
    la = ag_loss(P, Xb_, Yb_, heads)
    la.backward()
    lv.claim(abs(la.item() - lh) < 1e-12 and all(np.allclose(P[k].grad, gh[k], rtol=1e-8, atol=1e-12) for k in pm), f'{heads} head(s): hand-written backward equals the autograd with seq_ops_l3')
WJ = json.load(open(WFILE))
M = {h: {k: np.array(v) for k, v in WJ[f'h{h}'].items()} for h in (1, 4)}
print('weights file', os.path.getsize(WFILE), 'bytes')
lv.claim(os.path.getsize(WFILE) < 262144, 'weights file under 256 KB')
dev = {}
for heads in (1, 4):
    re_ = rounded(train_model(0, heads))
    lv.claim(max(float(np.abs(re_[k] - M[heads][k]).max()) for k in re_) < 1e-4, f'{heads} head(s): retrained seed 0 matches the shipped weights')
    dA, n = np_dev_loss(M[heads], XDV, YDV, heads)
    P = {k: Tensor(v) for k, v in M[heads].items()}
    tot = 0.0
    for i in range(0, len(XDV), 1000):
        tot += ag_loss(P, XDV[i:i + 1000], YDV[i:i + 1000], heads).item() * int((YDV[i:i + 1000] >= 0).sum())
    two(f'{heads} head(s): dev loss by NumPy and by the autograd', dA, tot / int((YDV >= 0).sum()), 1e-9)
    lv.claim(n == 22807 and abs(round(dA, 6) - WJ[f'dev_h{heads}']) < 1e-12, f'{heads} head(s): {n} dev symbols, dev loss {dA:.6f} as stored')
    dev[heads] = dA
for heads in (1, 4):
    for seed in (1, 2):
        d_ = np_dev_loss(train_model(seed, heads), XDV, YDV, heads)[0]
        lv.claim(d_ < 2.4514 - 0.08, f'{heads} head(s), seed {seed}: dev {d_:.4f}, below the bigram with a margin of 0.08')

# the bigram on the same dev names (makemore's add-one counts on the training names)
N = np.ones((27, 27))
for w in TRN:
    s = [0] + [IX[c] for c in w] + [0]
    for a, b in zip(s, s[1:]):
        N[a, b] += 1
Pb = N / N.sum(1, keepdims=True)
big = float(np.mean([-math.log(Pb[a, b]) for w in DEV for s in [[0] + [IX[c] for c in w] + [0]] for a, b in zip(s, s[1:])]))
lv.claim(round(big, 4) == 2.4514, f'bigram dev loss {big:.4f}, as makemore states', covers=[2.4514])
lv.claim(round(big / LN2, 4) == 3.5366, 'bigram in bits', covers=[3.5366])

# ---------------- l9 ----------------
L9 = 'l9-'
X5 = np.array([[1.0, 0.0], [0.0, 1.0], [0.6, 0.8], [1.0, 0.0], [0.0, 1.0]])
A5 = sm(X5 @ X5.T / math.sqrt(2), 1)
loop = np.array([[math.exp(X5[i] @ X5[j] / math.sqrt(2)) for j in range(5)] for i in range(5)])
loop /= loop.sum(1, keepdims=True)
lv.claim(np.allclose(A5, loop), 'toy attention: vectorised against a loop')
lv.claim(np.allclose(F(L9)['screens'][0]['canvas']['params']['matrices'][0]['rows'], np.round(A5, 3)), 'the heat matrix holds the toy weights')
for v in A5[3]:
    E(L9, 'screens[0].explain.text', round(float(v), 3))
E(L9, 'screens[2].widget.answer', round(float(A5[4, 1]), 4)); E(L9, 'screens[2].widget.wrong[1].value', round(float(sm([0, 1, 0.8, 0, 1])[1]), 4))
for v in A5[4]:
    E(L9, 'screens[2].explain.text', round(float(v), 4))
lv.claim(round(math.exp(1 / math.sqrt(2)), 3) == 2.028 and round(math.exp(0.8 / math.sqrt(2)), 4) == 1.7607 and round(0.8 / math.sqrt(2), 4) == 0.5657 and round(2 + 2 * math.exp(1 / math.sqrt(2)) + math.exp(0.8 / math.sqrt(2)), 3) == 7.817, 'shown exponentials', covers=[2.028, 1.7607, 0.5657, 0.7071, 7.817])
perm = [4, 3, 2, 1, 0]
Op = sm(X5[perm] @ X5[perm].T / math.sqrt(2), 1) @ X5[perm]
lv.claim(np.allclose(Op, (A5 @ X5)[perm]), 'reversing the input reverses the outputs')
two('121 scores', 11 * 11, 121); two('busy day', (160 / 40) ** 2, 16)
lv.claim(160 ** 2 == 25600 and 40 ** 2 == 1600, 'scores 25,600 and 1,600', covers=[25600, 1600])

# ---------------- l10 ----------------
L10 = 'l10-'
p0, h0 = train_model(0, 1, steps=300, mask=False, record=True)
p1, h1 = train_model(0, 1, steps=300, mask=True, record=True)
fr = F(L10)['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(fr[0]['series']['run']['values'] == [round(float(np.mean(h0[i:i + 10])), 4) for i in range(0, 300, 10)] and fr[1]['series']['run']['values'] == [round(float(np.mean(h1[i:i + 10])), 4) for i in range(0, 300, 10)], 'hook frames: the two recorded runs, averaged over tens of steps')
E(L10, 'screens[0].explain.text', round(float(np.mean(h0[-50:])), 2)); E(L10, 'screens[0].explain.text', round(float(np.mean(h1[-50:])), 2))
E(L10, 'screens[0].explain.text', round(np_dev_loss(p0, XDV, YDV, 1)[0], 2))
lv.claim(np.mean(h0[-50:]) < 0.5 and np.mean(h1[-50:]) > 2.2, 'unmasked run far below the bigram, masked run near it')
two('T = 32 pairs', 32 * 33 / 2, 528)
lv.claim(32 * 33 == 1056 and 32 * 32 == 1024 and 32 * 31 / 2 == 496, 'shown 1,056 and 1,024', covers=[1056, 1024])
w2 = sm([1.0, 2.0])
two('masked row', float(w2[0]), 1 / (1 + e)); E(L10, 'screens[3].widget.answer', round(float(w2[0]), 4)); E(L10, 'screens[3].explain.text', round(float(w2[1]), 4)); E(L10, 'screens[3].widget.wrong[0].value', round(float(sm([1, 2, 5, 3])[0]), 4))
E(L10, 'screens[5].prose', round(dev[1], 4)); E(L10, 'screens[5].widget.answer', round(dev[1] / LN2, 4)); E(L10, 'screens[5].widget.wrong[2].value', round(dev[1] / math.log(10), 4))
E(L10, 'screens[5].canvas', round(dev[4], 4)); E(L10, 'screens[5].canvas', round(dev[4] / LN2, 4)); E(L10, 'screens[5].explain.text', round(big / LN2 - dev[1] / LN2, 4))
lv.claim(round(LN2, 4) == 0.6931, 'ln 2', covers=[0.6931])
af = sm([1, 2, 5, 3])
E(L10, 'screens[6].widget.answer', round(float(af[0] + af[1]), 4)); E(L10, 'screens[6].explain.text', round(float(af[2] + af[3]), 4))
for v in af:
    E(L10, 'screens[6].canvas', round(float(v), 4))
lv.claim(abs(sum(af) - 1) < 1e-12, 'full softmax sums to 1')
E(L10, 'quiz[1].widget.wrong[0].value', round(float(sm([0, 0, 9])[0]), 4))
st0 = np_loss_grad(init_model(0), XTR[:256], YTR[:256], 1)[0]
lv.claim(round(st0, 2) == 3.38, f'graded start: loss {st0:.4f}, about 3.38', covers=[3.38])

# ---------------- l11 ----------------
two('head width', 64 / 4, 16); two('feature 37', 37 // 16, 2)
lv.claim(4 * 64 * 64 == 16384 and 64 * 64 == 4096 and 3 * 4096 == 12288, 'attention weights 16,384 = 4 x 4,096', covers=[16384, 4096, 12288])

# ---------------- l12 ----------------
L12 = 'l12-'


def last_p(model, s, pos):
    return sm(np_forward(model, np.array([[IX[c] for c in s]]), 1, pos=pos)[0, -1])


pa0, pb0, pa1, pb1 = last_p(M[1], '.mar', False), last_p(M[1], '.amr', False), last_p(M[1], '.mar', True), last_p(M[1], '.amr', True)
i_ = IX['i']
lv.claim(abs(pa0[i_] - pb0[i_]) < 1e-12, '.mar and .amr: equal chances of i without positions')
E(L12, 'screens[0].explain.text', round(float(pa0[i_]), 4)); E(L12, 'screens[0].explain.text', round(float(pa1[i_]), 4)); E(L12, 'screens[0].explain.text', round(float(pb1[i_]), 4))
E(L12, 'screens[0].widget.wrong[0].value', round(float(abs(pa1[i_] - pb1[i_])), 4))
two('sin 3', math.sin(3), float(np.sin(3.0))); E(L12, 'screens[1].widget.answer', round(math.sin(3), 4)); E(L12, 'screens[1].explain.text', round(math.cos(3), 4))
E(L12, 'screens[1].widget.wrong[1].value', round(math.sin(math.radians(3)), 4))
ang = 5 / 10000 ** (2 / 32)
lv.claim(round(10000 ** (2 / 32), 4) == 1.7783 and round(ang, 4) == 2.8117, '10000^(2/32) = 1.7783, angle 2.8117', covers=[1.7783, 2.8117])
E(L12, 'screens[2].widget.answer', round(math.sin(ang), 4)); E(L12, 'screens[2].explain.text', round(math.cos(ang), 4)); E(L12, 'screens[2].widget.wrong[1].value', round(math.sin(5 / 10000 ** (4 / 32)), 4))
dot1 = sum(math.cos(1 / 10000 ** (2 * i / 32)) for i in range(16))
PE = np.zeros((20, 32))
for t in range(20):
    for i in range(16):
        PE[t, 2 * i], PE[t, 2 * i + 1] = math.sin(t / 10000 ** (2 * i / 32)), math.cos(t / 10000 ** (2 * i / 32))
lv.claim(all(abs(PE[t] @ PE[t + 1] - dot1) < 1e-9 for t in range(19)) and all(abs(PE[t] @ PE[t] - 16) < 1e-9 for t in range(20)), 'offset 1 gives the same dot product at every t; self dot 16')
E(L12, 'screens[3].feedback.correct', round(dot1, 2))

# ---------------- review, problems, homework ----------------
two('55 pairs', 10 * 11 / 2, 55); two('review row', float(sm([2.0, 0.0])[0]), 1 / (1 + math.exp(-2)))
E('review', 'items[1].widget.answer', round(1 / (1 + math.exp(-2)), 4)); E('review', 'items[1].explain.text', round(1 / (1 + math.exp(2)), 4)); E('review', 'items[1].widget.wrong[0].value', round(float(sm([2, 0, 7])[0]), 4))
E('review', 'items[3].widget.answer', round(math.sin(2), 4)); E('review', 'items[3].widget.wrong[0].value', round(math.cos(2), 4)); E('review', 'items[3].widget.wrong[1].value', round(math.sin(math.radians(2)), 4))
lv.claim(4 * 48 * 48 == 9216 and 48 * 48 == 2304, 'review count', covers=[9216, 2304])
E('review', 'items[7].prose', round(dev[4], 4)); E('review', 'items[7].widget.answer', round(dev[4] / LN2, 4)); E('review', 'items[7].widget.wrong[1].value', round(dev[4] / math.log(10), 4))
xs = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
Aw = sm(xs @ xs.T / math.sqrt(2) + np.triu(np.full((3, 3), -np.inf), 1), 1)
Awl = np.array([[math.exp(xs[i] @ xs[j] / math.sqrt(2)) if j <= i else 0.0 for j in range(3)] for i in range(3)])
Awl /= Awl.sum(1, keepdims=True)
lv.claim(np.allclose(Aw, Awl), 'problem weights: masked softmax against a loop')
E('problems', 'items[0].parts[0].widget.answer', round(float(Aw[1, 0]), 4)); E('problems', 'items[0].parts[1].widget.answer', round(float(Aw[2, 2]), 4)); E('problems', 'items[0].parts[2].widget.answer', round(float(Aw[2] @ xs[:, 0]), 4))
E('problems', 'items[0].parts[0].explain.text', round(float(Aw[1, 1]), 4)); E('problems', 'items[0].parts[0].widget.wrong[0].value', round(float(sm(xs @ xs.T / math.sqrt(2), 1)[1, 0]), 4))
E('problems', 'items[0].parts[1].widget.wrong[0].value', round(float(sm([1, 1, 2])[2]), 4)); E('problems', 'items[0].parts[2].widget.wrong[0].value', round(2 / 3, 4))
lv.claim(round(math.sqrt(2), 4) == 1.4142, 'sqrt 2', covers=[1.4142])
Y3 = xs.copy()
Y3[2] = 0
O_ = sm(xs @ xs.T / math.sqrt(2) + np.triu(np.full((3, 3), -np.inf), 1), 1) @ xs
O2 = sm(Y3 @ Y3.T / math.sqrt(2) + np.triu(np.full((3, 3), -np.inf), 1), 1) @ Y3
lv.claim(int(sum(not np.allclose(O_[i], O2[i]) for i in range(3))) == 1, 'changing token 3 moves one output')
lv.claim(8 * 528 == 4224 and 64 // 8 == 8, '4,224 weights', covers=[4224])
E('problems', 'items[1].parts[2].widget.wrong[1].value', 8 * 1024); E('problems', 'items[1].parts[3].widget.wrong[0].value', 8 * 4 * 64 * 64)
two('10000^(1/4)', 10000 ** 0.25, 10.0); E('problems', 'items[2].parts[1].widget.answer', round(math.sin(2), 4)); E('problems', 'items[2].parts[2].widget.answer', round(math.cos(2), 4)); E('problems', 'items[2].parts[1].widget.wrong[1].value', round(math.sin(20), 4))
E('problems', 'items[3].parts[0].widget.answer', round(2.4514 - dev[1], 4)); E('problems', 'items[3].parts[0].widget.wrong[0].value', round(dev[1] / 2.4514, 4))
E('problems', 'items[3].parts[1].widget.answer', round((2.4514 - dev[1]) / LN2, 4)); E('problems', 'items[3].parts[1].widget.wrong[0].value', round((2.4514 - dev[1]) * LN2, 4))
E('problems', 'items[3].parts[2].widget.answer', round(math.exp(dev[1]), 2)); E('problems', 'items[3].parts[2].widget.wrong[0].value', round(2 ** dev[1], 2)); E('problems', 'items[3].parts[2].widget.wrong[1].value', round(math.exp(2.4514), 2))
E('problems', 'items[3].parts[3].widget.answer', round(7 * (2.4514 - dev[1]) / LN2, 2)); E('problems', 'items[3].parts[3].widget.wrong[0].value', round(6 * (2.4514 - dev[1]) / LN2, 2))
lv.claim(round(dev[1], 6) == WJ['dev_h1'], 'the 6-place dev loss printed in the working', covers=[WJ['dev_h1']])
lv.claim(128 * 129 // 2 == 8256 and 128 * 128 == 16384, 'homework pairs', covers=[8256])
E('homework', 'items[1].widget.answer', round(math.cos(7), 4)); E('homework', 'items[1].widget.wrong[0].value', round(math.sin(7), 4)); E('homework', 'items[1].widget.wrong[1].value', round(math.cos(math.radians(7)), 4))
E('homework', 'items[3].widget.answer', round(math.exp(dev[4]), 2)); E('homework', 'items[3].widget.wrong[0].value', round(2 ** dev[4], 2)); E('homework', 'items[3].explain.text', round(math.exp(dev[4]), 1))
lv.claim(round(dev[4], 6) == WJ['dev_h4'], 'the 6-place 4-head dev loss', covers=[WJ['dev_h4']])
lv.claim(round(math.exp(-1), 2) == 0.37, 'e^-1 is 0.37', covers=[0.37])

# the homework reference against an explicit loop over heads and positions
hw = F('homework')['items'][7]['widget']
ns = {}
exec(hw['prelude'], ns)
ns2 = {}
exec(hw['solution'], ns2)


def loop_ref(X, prm, h):
    T, d = X.shape
    w = d // h
    x = X + prm['P'][:T]
    Q, K, V = x @ prm['Wq'], x @ prm['Wk'], x @ prm['Wv']
    out = np.zeros((T, d))
    for hd in range(h):
        sl = slice(hd * w, (hd + 1) * w)
        for t in range(T):
            wt = sm([float(Q[t, sl] @ K[j, sl]) / math.sqrt(w) for j in range(t + 1)])
            out[t, sl] = sum(wt[j] * V[j, sl] for j in range(t + 1))
    return out @ prm['Wo']


for X_, P_, h_ in ((ns['X6'], ns['P6'], 2), (ns['X6'], ns['P6'], 4), (ns['X5'], ns['P5'], 3), (ns['X6'][:1], ns['P6'], 2), (ns['X6'], ns['P6'], 8)):
    lv.claim(np.allclose(ns2['causal_mha_forward'](X_, P_, h_), loop_ref(X_, P_, h_), rtol=1e-10, atol=1e-12), f'causal_mha_forward equals a loop over heads and positions (T = {X_.shape[0]}, h = {h_})')

# ---------------- code widgets ----------------


def judge(a, ex, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(close(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(close(p_, q_) for p_, q_ in zip(x, yv))
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(yv), rel_tol=rt, abs_tol=at) or float(x) == float(yv)
        except Exception:
            return x == yv

    def same(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(same(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x, yv))
        return bool(x == yv)
    return close(a, ex) if cmp == 'isclose' else same(a, ex)


def purge():
    for m in [m for m in sys.modules if m in ('autograd', 'seq_ops_l2', 'seq_ops_l3')]:
        sys.modules.pop(m)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    try:
        for kk, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(dd, kk))
        sys.path.insert(0, dd)
        purge()
        ns = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns)
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    if c.get('compare') == 'raises':
                        try:
                            eval(c['call'], ns)
                            ok = False
                        except Exception as ex:
                            ok = c['expect'] in [k.__name__ for k in type(ex).__mro__]
                    else:
                        got = eval(c['call'], ns)
                        t = c.get('tol')
                        ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
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
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')

lv.claim(32 * 33 / 2 == 528 and 32 * 31 / 2 == 496 and 6 * 7 / 2 == 21 and 10 * 11 / 2 == 55 and 128 * 129 / 2 == 8256, 'the T(T + 1)/2 workings', covers=[33 / 2, 31 / 2, 7 / 2, 11 / 2, 129 / 2])
lv.claim(37 // 16 == 2 and 37 % 4 == 1 and 47 - 32 == 15, 'feature 37 by 16 and by 4', covers=[37 / 4, 37 / 16])
lv.claim(16 / 64 == 1 / 4 and 2 * 32 == 64, 'a quarter of the width; concatenation doubles 32', covers=[1 / 4, 2])
lv.claim(math.sin(3 / 1) == math.sin(3) and math.sin(2 / 1) == math.sin(2), 'angles t/1', covers=[3 / 1, 2 / 1])
lv.claim(2 / 32 == 0.0625 and 2 / 8 == 0.25, 'exponents 2/32 and 2/8', covers=[2 / 32, 2 / 8])
lv.claim(round(float(Aw[2, 0]), 4) == 0.2483, 'problem weight 0.2483', covers=[0.2483])
lv.check_wrongs()
for t_, why in [('33', 'T + 1 for T = 32, in the working'), ('37', 'the feature asked about, a given'), ('47', 'the last feature of head 2, 2 x 16 + 15'), ('10000', 'the sinusoid constant of Vaswani et al.'),
                ('60', 'days in the transfer, a given'), ('39', 'the last of 40 positions, a given'), ('four times', 'a distractor\'s wrong claim, answered in its why'), ('3,000', 'training steps, a setting'), ('0.6', 'a given weight and embedding entry'), ('0.8', 'a given embedding entry'), ('0.5', 'a given weight'), ('500', 'trades on the tape, a given'),
                ('160', 'headlines on a busy day, a given'), ('40', 'headlines and tokens, givens'), ('2.75', 'the graded threshold, set with a margin above 2.6899'), ('2.6899', 'the reference\'s tenth loss, from the solution run'),
                ('10^-6', 'test tolerances'), ('10^-9', 'test tolerances'), ('1.5', 'a given key'), ('22,807', 'dev symbols, checked above'), ('128', 'a given context'), ('120', 'a given width'),
                ('96', 'a given width'), ('64', 'given widths'), ('48', 'a given width'), ('256', 'training windows in the graded run, a setting')]:
    LIT(t_, why=why)
lv.report()
