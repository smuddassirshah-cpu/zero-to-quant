"""Recompute every number stated in cnn level 3 (A CNN on digits) and check each at its JSON path.

Run from app/: node tools/run-number-scripts.mjs --python <venv> --only cnn-L3   (NumPy and scikit-learn 1.6.1; exits 0 when every check passes)

Route A is the lesson generator and the shipped module cnn_ops_l3.py (autograd and im2col ops). Route B, here, is independent:
the split is rebuilt from scikit-learn's load_digits and train_test_split and compared with cnn-digits.txt byte for byte; every
forward pass on the shipped weights is recomputed with plain NumPy sliding windows and loops (no autograd, no im2col) and
compared with the module; counts and parameter totals are built from arrays; the training runs are repeated here with the
module's fit on three seeds, and only thresholds (or values recorded once, checked within a stated tolerance) are stated from
them. The rate and the margin rule are set on validation digits only: no test score is computed for a candidate. Every code widget is run: the model solution passes, the starter fails, each mutant first fails the test it names, and
the exact values in the tests are recomputed by route B.
"""
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
APP = os.path.join(ROOT, 'app')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

AI = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, AI)
from autograd import Tensor, grad_check, softmax, cross_entropy  # noqa: E402
import cnn_ops_l3 as o  # noqa: E402

T0 = time.time()
lv = Level('cnn', 3, coverage='strict')
E = lv.expect


def EA(f, path, *vals):
    for v in vals:
        E(f, path, v)


def sha(name):
    return hashlib.sha256(open(os.path.join(AI, name), 'rb').read()).hexdigest()


# =================== 1. frozen modules, shipping by path ===================
lv.claim(sha('autograd.py').startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(sha('cnn_ops_l2.py') == 'a783b130c189caf712f335e4b7f472cb180361668ea534fb6b3d88d108d5a2a7', 'cnn_ops_l2.py is the frozen level 2 module')
lv.claim(sha('nt_ops_l1.py') == '9c1391a33624604bf8547607a51ef08c39a9bee2eeef22947aa5126dbc4ff234', 'nt_ops_l1.py is the frozen nn-train level 1 module')
WIDGETS = []
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []) + doc.get('quiz', []):
        w = u.get('widget') or {}
        if w.get('kind') in ('code', 'trainer'):
            WIDGETS.append((fid, u.get('title') or u.get('id'), w))
shipped = [(k, v) for _, _, w in WIDGETS for k, v in (w.get('data') or {}).items()]
lv.claim(all(v == f'content/data/ai/{k}' and os.path.exists(os.path.join(APP, v)) for k, v in shipped) and not any(w.get('files') for _, _, w in WIDGETS),
         f'every shipped module and data file ({len(shipped)}) is sent by path from the data folder: the page gets the canonical bytes')
for name in ('cnn-digits.txt', 'cnn-w-exit.json', 'cnn-w-small.json', 'cnn-w-mlp.json', 'cnn-w-mlp-aug.json', 'cnn-w-res.json', 'cnn_ops_l3.py'):
    lv.claim(os.path.getsize(os.path.join(AI, name)) <= 256 * 1024, f'{name} is under 256 KB ({os.path.getsize(os.path.join(AI, name))} bytes)')

# =================== 2. the split, rebuilt from scikit-learn (route B) ===================
from sklearn.datasets import load_digits  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
Xs, ys = load_digits(return_X_y=True)
idx = np.arange(len(ys))
itr, ite = train_test_split(idx, test_size=0.3, random_state=0, stratify=ys)
itr2, iva = train_test_split(itr, test_size=0.2, random_state=0, stratify=ys[itr])
lab = np.empty(len(ys), dtype='<U1'); lab[itr2] = 't'; lab[iva] = 'v'; lab[ite] = 'h'
body = [lab[i] + str(ys[i]) + ''.join('0123456789abcdefg'[int(v)] for v in Xs[i]) for i in range(len(ys))]
file_lines = [ln for ln in open(os.path.join(AI, 'cnn-digits.txt'), encoding='utf8').read().splitlines() if not ln.startswith('#')]
lv.claim(file_lines == body, 'cnn-digits.txt is load_digits split 70/30 by class (seed 0), then 20% of train for validation (seed 0), in the original order')
Xt, yt, Xv, yv, Xh, yh = o.load_split(os.path.join(AI, 'cnn-digits.txt'))
lv.claim((len(yt), len(yv), len(yh), len(ys)) == (1005, 252, 540, 1797) and np.array_equal(np.sort(np.concatenate([yt, yv, yh])), np.sort(ys)),
         'split sizes 1,005, 252 and 540 of 1,797', covers=[1005, 252, 540, 1797])
lv.claim(np.array_equal(Xh.reshape(-1, 64) * 16, Xs[np.sort(ite)]) and np.array_equal(yh, ys[np.sort(ite)]), 'load_split returns the held-out images and labels of the rebuilt split')
lv.claim(abs(len(ite) / len(ys) - 0.3) < 0.001 and Xh.shape[1:] == (1, 8, 8), 'held out 30%, images 8 by 8', covers=[0.3])
SH = [(1, 0), (-1, 0), (0, 1), (0, -1)]
SH2 = [(2, 0), (-2, 0), (0, 2), (0, -2)]


# =================== 3. route B forward passes and op checks ===================
def convB(x, Wk, bk):
    """Plain NumPy: every filter at every position of the padded maps, as a sum over the 3 by 3 offsets and channels."""
    n, c, h, w = x.shape
    xp = np.pad(x, ((0, 0), (0, 0), (1, 1), (1, 1)))
    out = np.zeros((n, Wk.shape[0], h, w)) + bk[None, :, None, None]
    for a in range(3):
        for b in range(3):
            out += np.einsum('fc,nchw->nfhw', Wk[:, :, a, b], xp[:, :, a:a + h, b:b + w])
    return out


def poolB(x):
    n, c, h, w = x.shape
    out = np.empty((n, c, h // 2, w // 2))
    for i in range(h // 2):
        for j in range(w // 2):
            out[:, :, i, j] = x[:, :, 2 * i:2 * i + 2, 2 * j:2 * j + 2].max(axis=(2, 3))
    return out


def cnnB(P, X):
    Wk, bk, V, c = P
    h = poolB(np.maximum(convB(X, Wk, bk), 0))
    return h.reshape(len(X), -1) @ V + c


def mlpB(P, X):
    W1, b1, W2, b2 = P
    return np.maximum(X.reshape(len(X), -1) @ W1 + b1, 0) @ W2 + b2


def blockB(h, A1, a1, A2, a2, skip=True):
    F = convB(np.maximum(convB(h, A1, a1), 0), A2, a2)
    return h + F if skip else F


def resB(P, X, skip=True):
    Wk, bk, A1, a1, A2, a2, V, c = P
    h = poolB(blockB(np.maximum(convB(X, Wk, bk), 0), A1, a1, A2, a2, skip))
    return h.reshape(len(X), -1) @ V + c


def softB(z):
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def shiftB(X, dx, dy):
    out = np.zeros_like(X)
    for i in range(8):
        for j in range(8):
            if 0 <= i + dy < 8 and 0 <= j + dx < 8:
                out[..., i + dy, j + dx] = X[..., i, j]
    return out


def accB(fn, P, X, y):
    return float((fn(P, X).argmax(axis=1) == y).mean())


WTS = {k: o.load_weights(os.path.join(AI, f'cnn-w-{k}.json')) for k in ('exit', 'small', 'mlp', 'mlp-aug', 'res')}
FB = {'exit': cnnB, 'small': cnnB, 'mlp': mlpB, 'mlp-aug': mlpB, 'res': resB}
FA = {'exit': o.cnn_logits, 'small': o.cnn_logits, 'mlp': o.mlp_logits, 'mlp-aug': o.mlp_logits, 'res': o.res_logits}
for k in WTS:
    za, zb = FA[k](WTS[k], Xh).data, FB[k](WTS[k], Xh)
    lv.claim(np.allclose(za, zb, rtol=0, atol=1e-10), f'{k}: module forward and plain NumPy forward agree on the 540 held-out digits')
    srt = np.sort(zb, axis=1)
    lv.claim((srt[:, -1] - srt[:, -2]).min() > 1e-7, f'{k}: no held-out top score is within 1e-7 of the second, so the predictions do not depend on summation order')
nparams = {k: sum(p.size for p in WTS[k]) for k in WTS}
lv.claim(nparams == {'exit': 2730, 'small': 1370, 'mlp': 3010, 'mlp-aug': 3010, 'res': 7370}, f'parameter counts of the shipped nets {nparams}', covers=[2730, 3010, 7370])
lv.claim(2 * (16 * 16 * 9 + 16) == WTS['res'][2].size + WTS['res'][3].size + WTS['res'][4].size + WTS['res'][5].size == 4640, 'the block has 4,640 parameters (formula and arrays)', covers=[4640, 2320])
lv.claim(WTS['mlp'][0].size == 2560, 'the MLP has 2,560 first-layer weights', covers=[2560])
try:
    o.conv2d(np.zeros((1, 1, 8, 8)), np.zeros((3, 1, 3, 3)), np.zeros(1)); bias_ok = False
except ValueError:
    bias_ok = True
try:
    o.conv2d(np.zeros((1, 1, 8, 8)), np.zeros((3, 1, 3, 3)), np.zeros(3), 1, -1); pad_ok = False
except ValueError:
    pad_ok = True
lv.claim(bias_ok and pad_ok, 'cnn_ops_l3.conv2d raises ValueError for a bias that is not (F,) and for a negative padding (review notes for level 3)')
rr = np.random.default_rng(2027)
Xr = rr.standard_normal((3, 2, 8, 8))
lv.claim(all(np.array_equal(o.shift_images(Xr, dx, dy), shiftB(Xr, dx, dy)) for dx in range(-3, 4) for dy in range(-3, 4)), 'shift_images equals the loop for every shift up to 3')
yy, pp = rr.integers(0, 10, 200), rr.integers(0, 10, 200)
cmB = np.zeros((10, 10), int); np.add.at(cmB, (yy, pp), 1)
lv.claim(np.array_equal(o.confusion(yy, pp), cmB), 'confusion equals np.add.at')
PR = WTS['res']
hB = np.maximum(convB(Xh[:4], PR[0], PR[1]), 0)
lv.claim(np.allclose(o.block(hB, *PR[2:6]).data, blockB(hB, *PR[2:6]), atol=1e-10), 'block equals the plain NumPy block')
Pz = [PR[0], PR[1], PR[2], PR[3], 0 * PR[4], 0 * PR[5], PR[6], PR[7]]
lv.claim(np.allclose(o.res_logits(Pz, Xh).data, o.cnn_logits([PR[0], PR[1], PR[6], PR[7]], Xh).data, atol=1e-12), 'with the second convolution at zero the residual net equals the shallow net')
xs_ = rr.standard_normal((2, 3, 4, 4)); ps_ = [rr.standard_normal((3, 3, 3, 3)), rr.standard_normal(3), rr.standard_normal((3, 3, 3, 3)), rr.standard_normal(3)]; Ms_ = rr.standard_normal((2, 3, 4, 4))
xt_ = Tensor(xs_); ts_ = [Tensor(p) for p in ps_]
gerr = grad_check(lambda: (o.block(xt_, *ts_) * Ms_).sum(), [xt_] + ts_)
own = np.zeros_like(xs_)
for i in np.ndindex(xs_.shape):
    keep = xs_[i]; xs_[i] = keep + 1e-6; up = float((blockB(xs_, *ps_) * Ms_).sum()); xs_[i] = keep - 1e-6; dn = float((blockB(xs_, *ps_) * Ms_).sum()); xs_[i] = keep
    own[i] = (up - dn) / 2e-6
lv.claim(gerr < 1e-6 and np.abs(own - xt_.grad).max() / np.abs(own).max() < 1e-6, f'block gradient: grad_check {gerr:.1e}, plain NumPy central differences agree', covers=[1e-6])

# =================== 4. the shipped weights, by route B ===================
pX = softB(cnnB(WTS['exit'], Xh)); pred = pX.argmax(1)
cm = np.zeros((10, 10), int); np.add.at(cm, (yh, pred), 1)
accx = float((pred == yh).mean()); pc = np.diag(cm) / cm.sum(1)
accm, accs, accr, acca = (accB(FB[k], WTS[k], Xh, yh) for k in ('mlp', 'small', 'res', 'mlp-aug'))
accv = accB(cnnB, WTS['exit'], Xv, yv)
yf = yh.copy(); okk = np.flatnonzero(pred == yh)[:6]; yf[okk] = (yf[okk] + 1) % 10        # six right test labels changed: the l10 and homework plants
acc_yf = accB(cnnB, WTS['exit'], Xh, yf)
blank = softB(cnnB(WTS['exit'], np.zeros((1, 1, 8, 8))))[0]
shx = {k: [accB(FB[k], WTS[k], shiftB(Xh, dx, dy), yh) for dx, dy in SH] for k in ('exit', 'mlp', 'mlp-aug', 'small')}
c1, m1, a1 = (float(np.mean(shx[k])) for k in ('exit', 'mlp', 'mlp-aug'))
c2 = float(np.mean([accB(cnnB, WTS['exit'], shiftB(Xh, dx, dy), yh) for dx, dy in SH2]))
m2 = float(np.mean([accB(mlpB, WTS['mlp'], shiftB(Xh, dx, dy), yh) for dx, dy in SH2]))
print(f'shipped: exit {accx:.4f} (val {accv:.4f}), mlp {accm:.4f}, small {accs:.4f}, res {accr:.4f}; shifted exit {c1:.4f} mlp {m1:.4f} aug {a1:.4f}; 2 px {c2:.4f} {m2:.4f}')

# =================== 5. training runs on three seeds (every trained figure) ===================
plain = lambda P, X: o.res_logits(P, X, False)  # noqa: E731


def run(fn, P0, X, y, ep, lr, seed, val=False, **kw):
    vals = []
    cb = (lambda e, p: vals.append(o.accuracy(fn, p, Xv, yv))) if val else None
    P, L = o.fit(fn, P0, X, y, ep, lr, seed, on_epoch=cb, **kw)
    return {'P': P, 'loss': L, 'val': vals}


Xa = np.concatenate([Xt] + [o.shift_images(Xt, dx, dy) for dx, dy in SH]); ya = np.concatenate([yt] * 5)
RUN = {}
for s in range(3):
    RUN[('exit', s)] = run(o.cnn_logits, o.init_cnn(16, s), Xt, yt, 30, 0.02, s, val=(s == 0), cosine=True)
    RUN[('small', s)] = run(o.cnn_logits, o.init_cnn(8, s), Xt, yt, 10, 0.01, s, val=True)
    with np.errstate(all='ignore'):
        RUN[('div', s)] = run(o.cnn_logits, o.init_cnn(8, s), Xt, yt, 3, 3.0, s, val=True)
    RUN[('mlp', s)] = run(o.mlp_logits, o.init_mlp(40, s), Xt, yt, 30, 0.02, s, cosine=True)
    RUN[('mlpaug', s)] = run(o.mlp_logits, o.init_mlp(40, s), Xa, ya, 10, 0.02, s, cosine=True)
    RUN[('cnnaug', s)] = run(o.cnn_logits, o.init_cnn(16, s), Xa, ya, 10, 0.02, s, cosine=True)
    P0 = o.init_res(s, False, 0.01)
    RUN[('d-shallow', s)] = run(o.cnn_logits, [P0[0], P0[1], P0[6], P0[7]], Xt, yt, 6, 0.05, s, opt='sgd')
    RUN[('d-plain', s)] = run(plain, P0, Xt, yt, 6, 0.05, s, opt='sgd')
    RUN[('d-res', s)] = run(o.res_logits, P0, Xt, yt, 6, 0.05, s, opt='sgd')
for lr in (0.005, 0.01):
    RUN[('exitlr', lr)] = run(o.cnn_logits, o.init_cnn(16, 0), Xt, yt, 30, lr, 0, val=True, cosine=True)
for lr in (0.001, 0.1):
    RUN[('smalllr', lr)] = run(o.cnn_logits, o.init_cnn(8, 0), Xt, yt, 10, lr, 0, val=True)
RUN[('res', 0)] = run(o.res_logits, o.init_res(0, True), Xt, yt, 6, 0.01, 0, cosine=True)
print(f'training runs done at {time.time() - T0:.0f} s')
KIND = {'exit': cnnB, 'small': cnnB, 'cnnaug': cnnB, 'mlp': mlpB, 'mlpaug': mlpB, 'res': resB}
TE = {k: accB(KIND[k[0]], r_['P'], Xh, yh) for k, r_ in RUN.items() if k[0] in KIND}
SHM = {}
for k in [k for k in RUN if k[0] in ('exit', 'mlp', 'mlpaug', 'cnnaug')]:
    fn = KIND[k[0]]
    SHM[k] = (float(np.mean([accB(fn, RUN[k]['P'], shiftB(Xh, dx, dy), yh) for dx, dy in SH])), float(np.mean([accB(fn, RUN[k]['P'], shiftB(Xh, dx, dy), yh) for dx, dy in SH2])))
for s in range(3):
    print(f'seed {s}: exit test {TE[("exit", s)]:.4f}, shifted {SHM[("exit", s)][0]:.4f}; mlp test {TE[("mlp", s)]:.4f}, shifted {SHM[("mlp", s)][0]:.4f}; '
          f'gap {SHM[("exit", s)][0] - SHM[("mlp", s)][0]:.4f}; aug cnn {SHM[("cnnaug", s)][0]:.4f} mlp {SHM[("mlpaug", s)][0]:.4f}; small val {RUN[("small", s)]["val"][-1]:.4f}')
lv.claim(all(TE[('exit', s)] >= 0.98 for s in range(3)), 'the exit recipe scores at least 0.98 held out on all three seeds', covers=[0.98, 30, 0.02])
lv.claim(abs(TE[('exit', 0)] - accx) <= 0.005 and abs(TE[('res', 0)] - accr) <= 0.005, 'the retrained seed-0 exit and residual nets score within 0.005 of the shipped weights')
_tmp = tempfile.mkdtemp()
exact = {}
for k_, P_ in (('exit', RUN[('exit', 0)]['P']), ('small', RUN[('small', 0)]['P']), ('mlp', RUN[('mlp', 0)]['P']), ('res', RUN[('res', 0)]['P'])):
    pth = os.path.join(_tmp, f'{k_}.json'); o.save_weights(P_, pth, digits=6)
    exact[k_] = open(pth, 'rb').read() == open(os.path.join(AI, f'cnn-w-{k_}.json'), 'rb').read()
shutil.rmtree(_tmp)
lv.claim(all(exact.values()), f'the shipped exit, small, mlp and residual weight files are byte for byte what the seed-0 recipes write with save_weights(digits=6) {exact}')
lv.claim(all(np.array_equal(np.round(a, 6), b) for a, b in zip(RUN[('exit', 0)]['P'], WTS['exit'])) and all(np.array_equal(np.round(a, 6), b) for a, b in zip(RUN[('res', 0)]['P'], WTS['res'])),
         'round(retrained, 6) equals the shipped exit and residual arrays entry by entry')
lv.claim(max(float(np.abs(a - b).max()) for a, b in zip(RUN[('mlpaug', 0)]['P'], WTS['mlp-aug'])) <= 1e-6, 'the shipped augmented MLP is the seed-0 recipe within 1e-6 (the one file whose last digit can move with summation order)')
vlr = {lr: RUN[('exitlr', lr)]['val'][-1] for lr in (0.005, 0.01)}
vlr[0.02] = RUN[('exit', 0)]['val'][-1]
lv.claim(vlr[0.02] >= max(vlr[0.005], vlr[0.01]), f'rate 0.02 does best on validation of 0.005, 0.01, 0.02 (seed 0): {vlr}', covers=[0.005, 0.01, 0.02])
lv.claim(all(RUN[('small', s)]['val'][-1] >= 0.90 + 0.02 for s in range(3)), 'the 8-filter net reaches 0.90 on validation at 10 epochs on three seeds, with a margin of 0.02', covers=[0.90])
for s in range(3):
    L_ = RUN[('div', s)]['loss']
    pv = o.predict(o.cnn_logits, RUN[('div', s)]['P'], Xv)
    lv.claim(L_[0] > 4 and min(L_[1:]) > math.log(10) and len(set(pv.tolist())) == 1 and RUN[('div', s)]['val'][-1] < 0.11,
             f'rate 3, seed {s}: first-epoch loss above 4, then above ln 10, one class for every validation digit', covers=[4, 3, round(math.log(10), 2), 0.10, 252])
gaps = [SHM[('exit', s)][0] - SHM[('mlp', s)][0] for s in range(3)]
cross = [SHM[('exit', s)][0] - SHM[('mlp', q)][0] for s in range(3) for q in range(3)]
auggaps = [SHM[('cnnaug', s)][0] - SHM[('mlpaug', s)][0] for s in range(3)]


def shv(k, X, y, shifts):
    return float(np.mean([accB(KIND[k[0]], RUN[k]['P'], shiftB(X, dx, dy), y) for dx, dy in shifts]))


vcross = [shv(('exit', s), Xv, yv, SH) - shv(('mlp', q), Xv, yv, SH) for s in range(3) for q in range(3)]
vaug = [shv(('cnnaug', s), Xv, yv, SH) - shv(('mlpaug', s), Xv, yv, SH) for s in range(3)]
lv.claim(min(vcross) >= 0.17 and max(vaug) < 0.03 and 0.03 < 0.10 < 0.17,
         f'the margin rule of 0.10 is set on shifted VALIDATION digits: every CNN beats every MLP by at least 0.17 (smallest {min(vcross):.4f}) and an augmented MLP is within 0.03 ({[round(g, 4) for g in vaug]}); 0.10 sits between',
         covers=[0.17, 0.03, 0.10])
lv.claim(all(shv(('mlpaug', s), Xv, yv, SH) > 0.93 and shv(('cnnaug', s), Xv, yv, SH) > 0.96 for s in range(3)) and max(vaug) < 0.05,
         'the augmentation statements (MLP above 0.93, CNN above 0.96, gap under 0.05) hold on validation as well as on test')
vg2 = [shv(('cnnaug', s), Xv, yv, SH2) - shv(('mlpaug', s), Xv, yv, SH2) for s in range(3)]
lv.claim(all(0.06 <= round(g, 2) <= 0.10 for g in vg2) and max(vg2) > max(vaug),
         f'at two pixels, which the augmented nets never saw, the gap returns to between 0.06 and 0.10 on validation ({[round(g, 4) for g in vg2]})', covers=[0.06, 0.10])
lv.claim(all(SHM[('mlpaug', s)][0] > 0.93 for s in range(3)) and all(SHM[('cnnaug', s)][0] > 0.96 for s in range(3)) and max(auggaps) < 0.05,
         f'augmented: MLP above 0.93, CNN above 0.96, gap under 0.05 on three seeds ({[round(g, 4) for g in auggaps]})', covers=[0.93, 0.96, 0.05, 5025, 10])
lv.claim(all(SHM[('exit', s)][1] < 0.2 and SHM[('mlp', s)][1] < 0.2 for s in range(3)), 'at two pixels both nets fall below 0.2 on three seeds', covers=[0.2])
STUCK = []
for s in range(3):
    sh_, pl_, rs_ = (RUN[(k, s)]['loss'] for k in ('d-shallow', 'd-plain', 'd-res'))
    lv.claim(all(p > q for p, q in zip(pl_, sh_)) and all(p < q for p, q in zip(rs_, sh_)),
             f'seed {s}: the plain deep net’s loss is above the shallow net’s, and the residual net’s below it, at every one of 6 epochs', covers=[0.05, 0.01, 6])
    n = 0
    for v in pl_:
        if v > 2.2:
            n += 1
        else:
            break
    STUCK.append(n)
lv.claim(STUCK == [2, 3, 4], f'plain nets stay above 2.2 for {STUCK} epochs', covers=[2.2])
ft = []
for s in range(3):
    Pf, _ = o.fit(o.cnn_logits, WTS['exit'], Xa, ya, 1, 0.01, s)
    ft.append(float(np.mean([accB(cnnB, Pf, shiftB(Xv, dx, dy), yv) for dx, dy in SH])))
before_ft = float(np.mean([accB(cnnB, WTS['exit'], shiftB(Xv, dx, dy), yv) for dx, dy in SH]))
lv.claim(min(ft) >= 0.85 + 0.03 and abs(np.mean(ft) - 0.90) < 0.03 and abs(before_ft - 0.65) < 0.01,
         f'one epoch of fine-tuning on shifted copies: validation shifted {before_ft:.4f} to {[round(f, 4) for f in ft]}', covers=[0.85, 0.65, 0.90])
lv.claim(math.ceil(len(Xa) / 32) == 158 and len(Xa) == 5025, '5,025 augmented images make 158 batches of 32', covers=[158, 5025])
print(f'section 5 done at {time.time() - T0:.0f} s')


def r2(x):
    return round(float(x), 2)


def r3(x):
    return round(float(x), 3)


def r4(x):
    return round(float(x), 4)


def ceil_div(n, b):
    return len(range(0, n, b))          # route B: count the batch starts


def series(f, i, sid):
    return next(s_['values'] for s_ in lv.files[f]['screens'][i]['canvas']['params']['series'] if s_['id'] == sid)


L9, L10, L11, L12 = 'l9-reading-digits', 'l10-training-the-cnn', 'l11-a-residual-block', 'l12-shifted-digits'
lv.literal('4.0', why='the licence name CC BY 4.0, not a figure')
lv.literal('70/30', why='the stated split ratio, a convention (the 30% is checked)')
lv.literal('double', why='the chart pattern "double top", a name, not a multiple')
lv.literal('10^-9', why='a comparison tolerance of the hidden tests, set by hand')
lv.literal('10^-7', why='a comparison tolerance of the hidden tests, set by hand')

# =================== 6a. l9 ===================
pool_n = poolB(np.zeros((1, 16, 8, 8))).size
lv.claim(yh[366] == 1 and yh[34] == 8 and pred[366] == 1 and pred[34] == 1, 'image A (366) is labelled 1 and read as 1; image B (34) is labelled 8 and read as 1')
E(L9, 'screens[0]', len(ys)); E(L9, 'screens[0].feedback.correct', r2(pX[366, 1])); E(L9, 'screens[0].feedback.correct', r2(pX[366, 9])); E(L9, 'screens[0].explain.text', r2(pX[34, 1]))
EA(L9, 'screens[1]', pool_n, convB(np.zeros((1, 1, 8, 8)), np.zeros((16, 1, 3, 3)), np.zeros(16)).size, 4 * 4)
E(L9, 'screens[1].widget.answer', pool_n); E(L9, 'screens[1].widget.wrong[0].value', 16 * 8 * 8); E(L9, 'screens[1].widget.wrong[1].value', 16)
EA(L9, 'screens[2]', len(yt), pool_n, 1024, Xh[0].size, WTS['exit'][2].size + WTS['exit'][3].size)
EA(L9, 'screens[3].widget.how', 366, 0.98, len(yh))
nerr = int((pred != yh).sum()); trace = int(np.trace(cm))
E(L9, 'screens[4].widget.answer', r4(accx)); E(L9, 'screens[4].widget.wrong[0].value', r4(1 - accx)); EA(L9, 'screens[4]', trace, len(yh), r4(accx), nerr)
EA(L9, 'screens[5].widget.how', 10, len(yh))
E(L9, 'screens[6].widget.answer', r4(pc[8])); E(L9, 'screens[6].widget.wrong[0].value', r4(accx)); E(L9, 'screens[6].widget.wrong[1].value', r4(1 - pc[8]))
EA(L9, 'screens[6]', int(cm[8].sum()), int(cm[8, 8]), nerr, round(100 * 0.98)); E(L9, 'screens[6].title', round(100 * 0.98))
lv.claim(int(np.argmin(pc)) == 8 and cm[8, 1] == 2 and all(pc[k] == 1 for k in (0, 1, 4, 6, 7)), 'digit 8 is worst; two 8s read as 1; every 0, 1, 4, 6, 7 right')
F13 = np.round(WTS['exit'][0][13, 0], 2)
for v in list(F13[0]) + list(F13[2]):
    E(L9, 'screens[8].hints[2].text', float(v))
lv.claim(F13[0].min() > 0 > F13[2].max() and np.round(WTS['exit'][0][3, 0], 2)[0, :2].max() < 0 < np.round(WTS['exit'][0][3, 0], 2)[2, :2].min(), 'F13 positive on top and negative below; F3 the other way round')
E(L9, 'screens[9].widget.options[0].text', r2(blank[4])); E(L9, 'screens[9].explain.text', r2(blank.min())); E(L9, 'screens[9].explain.text', r2(blank.max()))
lv.claim(int(blank.argmax()) == 4 and np.isclose(blank.sum(), 1), 'the blank image is read as 4')
EA(L9, 'screens[9]', 0.1); EA(L9, 'screens[10]', len(yh), r4(accx), nerr, 0.1)
EA(L9, 'screens[11]', 2000, 1870 + 70, 100, 70, r2(70 / 100), r2((1870 + 70) / 2000), r2(1870 / 1900), 1900)
E(L9, 'screens[11].widget.answer', 0.70); E(L9, 'screens[11].widget.wrong[0].value', r2(1940 / 2000)); E(L9, 'screens[11].widget.wrong[1].value', r2(1870 / 1900))
EA(L9, 'summary', len(yh), r4(accx), r4(pc[8]), pool_n)
E(L9, 'quiz[0].widget.answer', 8 * 4 * 4); E(L9, 'quiz[0].widget.wrong[0].value', 8 * 8 * 8); E(L9, 'quiz[0].widget.wrong[1].value', 16 * 4 * 4)
row3 = [0, 1, 0, 48, 0, 1, 0, 0, 0, 0]
E(L9, 'quiz[1].widget.answer', round(row3[3] / sum(row3), 2)); EA(L9, 'quiz[1]', sum(row3), 48)

# =================== 6b. l10 ===================
v001, v01, v1 = series(L10, 0, 'lr0'), series(L10, 0, 'lr1'), series(L10, 0, 'lr2')
E(L10, 'screens[0]', len(yv)); E(L10, 'screens[0].feedback.correct', v01[-1]); E(L10, 'screens[0].feedback.correct', v1[-1]); E(L10, 'screens[0].feedback.correct', v001[-1])
lv.claim(v01[-1] > max(v1[-1], v001[-1]), 'rate 0.01 ends highest on the recorded curves', covers=[0.01, 0.1, 0.001])
for lr, ser in ((0.001, v001), (0.01, v01), (0.1, v1)):
    rerun = RUN[('smalllr', lr)]['val'] if lr != 0.01 else RUN[('small', 0)]['val']
    lv.claim(max(abs(a - b) for a, b in zip(ser, rerun)) <= 0.02, f'recorded curve at rate {lr} reproduces within 0.02 (largest gap {max(abs(a - b) for a, b in zip(ser, rerun)):.4f})')
steps = ceil_div(1005, 32)
E(L10, 'screens[3].widget.answer', steps); E(L10, 'screens[3].widget.wrong[0].value', 1005 // 32); E(L10, 'screens[3].widget.wrong[1].value', round(1005 / 32, 1))
EA(L10, 'screens[3]', 1005, 32 * (1005 // 32), 1005 - 32 * (1005 // 32), steps * 10)
gV = (8 * 4 * 4) * 10
E(L10, 'screens[4].widget.answer', gV); E(L10, 'screens[4].widget.wrong[0].value', 32 * 10); E(L10, 'screens[4].widget.wrong[1].value', gV + 10); EA(L10, 'screens[4]', 8 * 4 * 4)
budget5 = lv.files[L10]['screens'][5]['widget']['tests'][4]['budget'] / 1000
lv.claim(3 * 32 == 96 and len(Xt[:96]) == 96, '96 digits are 3 batches of 32', covers=[96])
EA(L10, 'screens[5].widget.how', 1005, 0.90, budget5, 0.01, 0.02)
vs = series(L10, 6, 'val'); ls = series(L10, 6, 'loss')
best = int(np.argmax(vs)) + 1
E(L10, 'screens[6].widget.answer', best); E(L10, 'screens[6].widget.wrong[0].value', int(np.argmin(ls)) + 1); EA(L10, 'screens[6]', max(vs), vs[-1])
lv.claim(max(abs(a - b) for a, b in zip(vs, RUN[('small', 0)]['val'])) <= 0.02 and max(abs(a - b) for a, b in zip(ls, RUN[('small', 0)]['loss'])) <= 0.02, 'the recorded 10-epoch curves reproduce within 0.02')
trap = lv.files[L10]['screens'][7]['canvas']['params']['rows']
tv, tt = [float(r_[1]) for r_ in trap], [float(r_[2]) for r_ in trap]
EA(L10, 'screens[7]', tt[int(np.argmax(tv))], max(tt), r4(np.mean(tt)), max(tv), len(yh))
lv.claim(tt[int(np.argmax(tv))] == accx.__round__(4), 'the trap’s chosen net scores the shipped exit figure, a made-up table built around it')
EA(L10, 'screens[8]', round(math.log(10), 2), 0.10, len(yv))
lv.claim(abs(np.bincount(yv).max() / len(yv) - 0.1) < 0.005, 'one fixed class is right about a tenth of the time on validation', covers=['a tenth', 'A tenth', 0.1])
EA(L10, 'screens[9]', 16, 0.02, 30, 32, 0.005, 0.01, 0.98, r4(accx), r4(accs), round(accx * len(yh)), len(yh), r4(acc_yf), 0.97)
lv.claim(0.97 < acc_yf < 0.98 and acc_yf == 526 / 540, 'six changed test labels leave the exit net at 526 of 540: below 0.98 and above 0.97')
lv.claim(len(np.flatnonzero(pred == yh)[:50]) == 50, 'the planted set has 50 digits the exit net reads right, one relabelled', covers=[50])
E(L10, 'screens[10].widget.answer', 1); E(L10, 'screens[10].widget.wrong[0].value', 30); E(L10, 'screens[10].widget.wrong[1].value', 0)
EA(L10, 'summary', 1005, steps, 16, 0.02, 30, 0.98, r4(accx), best)
E(L10, 'quiz[0].widget.answer', ceil_div(1257, 64)); E(L10, 'quiz[0].widget.wrong[0].value', 1257 // 64); E(L10, 'quiz[0].widget.wrong[1].value', round(1257 / 64, 1))
EA(L10, 'quiz[0]', len(yt) + len(yv), 1257 - 64 * (1257 // 64)); lv.claim(ceil_div(1257, 64) == math.ceil(1257 / 64), '1,257/64 rounds up to 20 batches', covers=[1257 / 64]); EA(L10, 'quiz[2]', round(math.log(10), 2), 0.1)

# =================== 6c. l11 ===================
sh0, pl0, rs0 = (series(L11, 0, k) for k in ('sh', 'pl', 'rs'))
lv.claim(all(max(abs(a - b) for a, b in zip(ser, RUN[(k, 0)]['loss'])) <= 0.02 for ser, k in ((sh0, 'd-shallow'), (pl0, 'd-plain'), (rs0, 'd-res'))), 'the recorded six-epoch curves reproduce within 0.02')
EA(L11, 'screens[0]', round(math.log(10), 2), r2(pl0[0]), r2(pl0[1]), r2(sh0[0]), 2.2, 10)
E(L11, 'screens[1].widget.answer', r2(rs0[2])); E(L11, 'screens[1].widget.wrong[0].value', r2(pl0[2])); E(L11, 'screens[1].widget.wrong[1].value', r2(sh0[2])); E(L11, 'screens[1].hints[2].text', r3(rs0[2]))
EA(L11, 'screens[2]', 16 * 8 * 8, pool_n)
cp = WTS['res'][2].size + WTS['res'][3].size
rows = lv.files[L11]['screens'][3]['widget']['rows']
lv.claim([r_[1]['answer'] for r_ in rows] == [cp, cp, 2 * cp, nparams['res']] and rows[0][1]['wrong'][0]['value'] == 16 * (9 + 1) and rows[1][1]['wrong'][0]['value'] == cp - 16
         and rows[3][1]['wrong'][0]['value'] == 2 * cp, 'the block table: 2,320, 2,320, 4,640, 7,370 and its slips, from the weight arrays')
EA(L11, 'screens[3]', 16 * 9, 16 * 9 + 1, cp, 2 * cp, nparams['exit'], nparams['res'])
w1, w2, x0 = 0.5, -0.4, 2.0
dydx = 1 + w2 * w1 * (w1 * x0 > 0)
E(L11, 'screens[4].widget.answer', dydx); E(L11, 'screens[4].widget.wrong[0].value', w2 * w1); E(L11, 'screens[4].widget.wrong[1].value', 1); EA(L11, 'screens[4]', 0.5, -0.4, 0.2, dydx)
lv.claim(x0 + w2 * max(w1 * x0, 0) == 1.6, 'the graph’s values: y = 1.6, F = -0.4')
proj = 32 * (16 + 1)
E(L11, 'screens[5].explain.text', proj); lv.claim(32 == 2 * 16, 'doubling 16 channels gives 32', covers=['doubles', 'twice'])
EA(L11, 'screens[8]', r4(accr), 16); EA(L11, 'screens[9]', 1e-6); EA(L11, 'screens[10].widget.how', 2.2)
EA(L11, 'summary', 2 * cp)
E(L11, 'quiz[0].widget.answer', 2 * 8 * (8 * 9 + 1)); E(L11, 'quiz[0].widget.wrong[0].value', 8 * (8 * 9 + 1)); E(L11, 'quiz[0].widget.wrong[1].value', 2 * 8 * 8 * 9); EA(L11, 'quiz[0]', 8 * 9 + 1)
E(L11, 'quiz[1].widget.answer', round(1 - 0.95, 2)); E(L11, 'quiz[1].widget.wrong[0].value', -0.95); E(L11, 'quiz[1].widget.wrong[1].value', 1.95)

# =================== 6d. l12 ===================
I2 = 51
rd = {dx: (int(cnnB(WTS['exit'], shiftB(Xh[[I2]], dx, 0)).argmax()), int(mlpB(WTS['mlp'], shiftB(Xh[[I2]], dx, 0)).argmax())) for dx in (-2, -1, 0, 1, 2)}
pR = softB(cnnB(WTS['exit'], shiftB(Xh[[I2]], 1, 0)))[0]; mR = softB(mlpB(WTS['mlp'], shiftB(Xh[[I2]], 1, 0)))[0]
lv.claim(yh[I2] == 2 and rd[0] == (2, 2) and rd[1] == (2, 3) and rd[-1] == (2, 2) and rd[2][0] != 2, f'the hook 2: reads by shift {rd}')
for k_, dx in enumerate((-2, -1, 0, 1, 2)):
    cap = lv.files[L12]['screens'][1]['canvas']['controls'][0]['frames'][k_]['caption']
    lv.claim(f'CNN reads {rd[dx][0]}' in cap and f'MLP reads {rd[dx][1]}' in cap, f'frame {dx}: the caption names both reads')
EA(L12, 'screens[0]', 64, 40, nparams['mlp'], r2(pR[2]), r2(mR[3]), WTS['mlp'][0].size)
E(L12, 'screens[1].widget.answer', 2); E(L12, 'screens[1].widget.wrong[0].value', 1); lv.claim(2 / 8 == 0.25, 'two pixels of eight is a quarter', covers=['a quarter', 8])
lv.literal('37', why='an example pixel index in a sentence about what the MLP learns, not a result')
EA(L12, 'screens[2]', nparams['mlp'], nparams['exit'], 30, 64, 40)
E(L12, 'screens[3].widget.answer', r2(c1)); E(L12, 'screens[3].widget.wrong[0].value', r2(m1)); E(L12, 'screens[3].widget.wrong[1].value', r2(accx))
for v in shx['exit']:
    E(L12, 'screens[3].hints[2].text', r3(v))
EA(L12, 'screens[3]', len(yh), r2(accx), r2(accm), 0.2)
lv.claim((accx - c1) / accx > 1 / 3 and (accm - m1) / accm > 1 / 2 and c2 < 0.2 and m2 < 0.2, 'one pixel costs the CNN over a third and the MLP over half; at two pixels both are below 0.2', covers=['a third', 0.2])
EA(L12, 'screens[4]', pool_n)
EA(L12, 'screens[5]', len(yt), 5 * len(yt), r3(a1), r2(a1), r2(m1), 0.17, 0.10, 0.06)
EA(L12, 'screens[10]', 0.17, 0.03, 0.10)
tab = lv.files[L12]['screens'][5]['canvas']['params']['rows']
lv.claim([float(r_[1]) for r_ in tab] == [r3(c1), r3(m1), r3(a1)], 'the augmentation table holds the shipped nets’ mean shifted accuracies')
for g in auggaps:
    E(L12, 'screens[5].feedback.correct', r3(g))
lv.claim(abs(r2(c1) - r2(m1) - 0.17) < 0.006, 'the gap before augmenting is about 0.17', covers=[0.17])
EA(L12, 'screens[6]', r2(accx), r2(c1), r2(m1))
ink = Xh[117, 0, :, 7]
E(L12, 'screens[7].widget.answer', int((ink > 0).sum())); E(L12, 'screens[7].widget.wrong[0].value', 8); E(L12, 'screens[7].feedback.correct', int(round(ink.sum() * 16)))
EA(L12, 'screens[9]', r3(c1), r3(m1), r3(c1 - m1), 0.17, 0.10, len(yh))
lv.claim(0.57 - 0.47 < 0.10 and (0.57 - 0.47) >= 0.10 - 1e-9 and 0.10 - (0.57 - 0.47) < 1e-9, 'floating point: 0.57 - 0.47 is a hair below 0.10, so the margin test allows 1e-9')
lv.claim(round(0.71 - 0.63, 2) == 0.08 and round(100 * (0.71 / 0.63 - 1)) == 13, 'the generalise check: a gap of 0.08, a ratio 13% up', covers=[0.08, 13, 0.71, 0.63])
E(L12, 'screens[10].prose', 0.25)
EA(L12, 'summary', r2(c1), r2(m1), 0.10, 0.2, 0.93, 0.05)
E(L12, 'quiz[1].widget.answer', round(0.58 - 0.45, 2)); EA(L12, 'quiz[1]', 0.58, 0.45); E(L12, 'quiz[1].widget.wrong[0].value', round(0.58 / 0.45, 2))
EA(L12, 'screens[11]', 20, 8, r2(accx), r2(c1))

# =================== 6e. review ===================
d12 = 12 * 4 * 4
E('review', 'items[0].widget.answer', d12 * 10 + 10); E('review', 'items[0].widget.wrong[0].value', 12 * 8 * 8 * 10 + 10); E('review', 'items[0].widget.wrong[1].value', d12 * 10); EA('review', 'items[0]', d12, 12 * 8 * 8)
row5 = [0, 0, 0, 1, 0, 51, 0, 0, 2, 1]
E('review', 'items[1].widget.answer', r4(51 / sum(row5))); E('review', 'items[1].widget.wrong[1].value', r4(51 / 540)); EA('review', 'items[1]', sum(row5), 51)
E('review', 'items[3].widget.answer', ceil_div(1257, 50)); E('review', 'items[3].widget.wrong[0].value', 1257 // 50); E('review', 'items[3].widget.wrong[1].value', r2(1257 / 50)); EA('review', 'items[3]', 1257, 1257 - 50 * 25)
vals6 = [0.950, 0.970, 0.980, 0.975, 0.985, 0.980]
E('review', 'items[4].widget.answer', int(np.argmax(vals6)) + 1); EA('review', 'items[4]', *vals6)
blk32 = 32 * (32 * 9 + 1)
E('review', 'items[5].widget.answer', 2 * blk32); E('review', 'items[5].widget.wrong[0].value', blk32); E('review', 'items[5].widget.wrong[1].value', 2 * 32 * 10); EA('review', 'items[5]', 32 * 9 + 1)
E('review', 'items[6].widget.answer', 1 + 0.7 * 2 * (2 * -1 > 0)); E('review', 'items[6].widget.wrong[0].value', 1 + 0.7 * 2); EA('review', 'items[6]', 2 * -1, 0.7 * 2)
rowp = [3, 0, 0, 5]; sp = [0, 3, 0, 0]
E('review', 'items[7].widget.answer', sum(max(rowp[2 * i:2 * i + 2]) != max(sp[2 * i:2 * i + 2]) for i in range(2)))
E('review', 'items[8].widget.answer', round(0.47 + 0.10, 2)); E('review', 'items[8].widget.wrong[0].value', round(0.47 * 1.10, 2)); EA('review', 'items[8]', 0.47, 0.10)
proj8 = 16 * (8 + 1)
E('review', 'items[9].widget.answer', proj8); E('review', 'items[9].widget.wrong[0].value', 16 * 8); E('review', 'items[9].widget.wrong[1].value', 16 * (8 * 9 + 1))

# =================== 6f. homework ===================
EA('homework', 'items[0]', 0.98, 0.10, r4(accx), r3(c1), r3(m1), r3(a1), 0.05, 0.08)
EA('homework', 'items[1].widget.how', 50, len(Xa[::50]), 5025, 158, 4, 0.85, 0.01, 0.02)
lv.claim(ceil_div(101, 32) == 4 and len(Xa[::50]) == 101, 'every 50th augmented image: 101 images, 4 steps an epoch', covers=[101])
EA('homework', 'items[1].explain.text', 0.65, 0.90)
lv.claim(abs((0.985 - 0.62) / 0.985 - 0.37) < 0.01, 'the memo’s digits example: 0.99 to 0.62', covers=[0.99, 0.62, 0.05, 50, 20, 60])
E('homework', 'items[4].widget.answer', nparams['exit'] + 2 * 2 * cp); E('homework', 'items[4].widget.wrong[0].value', nparams['res']); E('homework', 'items[4].widget.wrong[1].value', 2 * 2 * cp); EA('homework', 'items[4]', 2 * cp)
fixed = (trace + int(cm[8].sum() - cm[8, 8])) / len(yh)
E('homework', 'items[5].widget.answer', r4(fixed)); E('homework', 'items[5].widget.wrong[0].value', r4(accx)); EA('homework', 'items[5]', trace, trace + 2, len(yh), int(cm[8].sum()))
EA('homework', 'items[6]', r2(m1), r2(a1), 0.05, 0.17)

# =================== 6g. problems ===================
CMp = np.array([[88, 8, 4], [6, 90, 4], [2, 3, 95]])
accp = np.trace(CMp) / CMp.sum(); pcp = np.diag(CMp) / CMp.sum(1)
P0p = 'items[0].parts'
E('problems', f'{P0p}[0].widget.answer', r2(accp)); E('problems', f'{P0p}[0].widget.wrong[1].value', r2(1 - accp)); EA('problems', 'items[0]', int(CMp.sum()), int(np.trace(CMp)), 100, 88, 90, 95)
E('problems', f'{P0p}[1].widget.answer', r2(pcp.min())); E('problems', f'{P0p}[1].widget.wrong[1].value', r4(CMp[0, 0] / CMp[:, 0].sum())); EA('problems', f'{P0p}[1]', r2(pcp[1]), r2(pcp[2]))
fx = (np.trace(CMp) + CMp[0].sum() - CMp[0, 0]) / CMp.sum()
E('problems', f'{P0p}[2].widget.answer', r2(fx)); EA('problems', f'{P0p}[2]', int(CMp[0].sum() - CMp[0, 0]), int(np.trace(CMp) + 12))
E('problems', f'{P0p}[3].widget.answer', r4(CMp[1, 1] / CMp[:, 1].sum())); E('problems', f'{P0p}[3].widget.wrong[1].value', r2(90 / 300)); EA('problems', f'{P0p}[3]', int(CMp[:, 1].sum()), r2(pcp[1]))
P1p = 'items[1].parts'
base32 = 32 * (9 + 1) + 32 * 4 * 4 * 10 + 10
E('problems', f'{P1p}[0].widget.answer', base32); E('problems', f'{P1p}[0].widget.wrong[0].value', 32 * 8 * 8 * 10 + 10 + 320); E('problems', f'{P1p}[0].widget.wrong[1].value', 320)
EA('problems', f'{P1p}[0]', 32 * 16, 32 * 4 * 4 * 10 + 10)
E('problems', f'{P1p}[1].widget.answer', 2 * blk32); E('problems', f'{P1p}[1].widget.wrong[1].value', 2 * 32 * 32 * 9); EA('problems', f'{P1p}[1]', 32 * 9 + 1, blk32)
E('problems', f'{P1p}[2].widget.answer', base32 + 2 * blk32)
E('problems', f'{P1p}[3].widget.answer', round(1 - 0.3, 1)); E('problems', f'{P1p}[3].widget.wrong[1].value', 1.3)
P2p = 'items[2].parts'
E('problems', f'{P2p}[0].widget.answer', round(0.64 - 0.47, 2)); E('problems', f'{P2p}[0].widget.wrong[0].value', round(0.64 / 0.47, 2)); EA('problems', 'items[2].prose', 0.64, 0.47)
E('problems', f'{P2p}[2].widget.answer', ceil_div(5 * 1005, 32)); E('problems', f'{P2p}[2].widget.wrong[0].value', 5025 // 32); E('problems', f'{P2p}[2].widget.wrong[1].value', ceil_div(1005, 32))
EA('problems', f'{P2p}[2]', 5 * 1005, 32 * (5025 // 32))
E('problems', f'{P2p}[3].widget.answer', round(0.96 - 0.93, 2))
P3p = 'items[3].parts'
E('problems', f'{P3p}[0].widget.answer', ceil_div(1400, 32)); E('problems', f'{P3p}[0].widget.wrong[1].value', 1400 / 32); EA('problems', f'{P3p}[0]', 1400 - 32 * 43, 1400)
E('problems', f'{P3p}[1].widget.answer', ceil_div(1400, 32) * 25); E('problems', f'{P3p}[1].widget.wrong[1].value', 1400 * 25)
E('problems', f'{P3p}[2].widget.answer', 12 * 16 * 10); E('problems', f'{P3p}[2].widget.wrong[0].value', 12 * 16 * 10 + 10); EA('problems', f'{P3p}[2]', 12 * 16)
v25 = [float(r_[1]) for r_ in lv.files['problems-3']['items'][3]['parts'][3]['canvas']['params']['rows']]
E('problems', f'{P3p}[3].widget.answer', 21 + int(np.argmax(v25))); EA('problems', f'{P3p}[3]', max(v25), v25[3], v25[4])
print(f'section 6 done at {time.time() - T0:.0f} s')


# =================== 7. every code widget ===================
def close(a, b, tol):
    rel, ab = (tol or {}).get('rel', 1e-9), (tol or {}).get('abs', 1e-12)
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(close(a[k], b[k], tol) for k in a)
    a = a.tolist() if hasattr(a, 'tolist') else a
    b = b.tolist() if hasattr(b, 'tolist') else b
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    try:
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    except (TypeError, ValueError):
        return a == b


def passes(t, ns):
    try:
        if t.get('setup'):
            exec(t['setup'], ns)
        got = eval(t['call'], ns)
    except Exception as e:  # noqa
        return t.get('compare') == 'raises' and any(c.__name__ == t['expect'] for c in type(e).__mro__)
    if t.get('compare') == 'raises':
        return False
    exp = eval(t['expect'], ns)
    if t.get('compare') == 'isclose':
        return close(got, exp, t.get('tol'))
    got = got.tolist() if hasattr(got, 'tolist') else got
    return got == exp


def first_fail(w, src):
    cwd = os.getcwd(); d = tempfile.mkdtemp(); os.chdir(d); sys.path.insert(0, d)
    for m in ('autograd', 'cnn_ops_l2', 'cnn_ops_l3', 'nt_ops_l1'):
        sys.modules.pop(m, None)
    try:
        for k, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), k)
        ns = {'__learner_source__': src}
        exec(ZQ_LIB, ns)
        try:
            exec((w.get('prelude') or '') + '\n', ns); exec(src, ns); exec((w.get('postlude') or '') + '\n', ns)
        except Exception:  # noqa
            return -1
        for i, t in enumerate(w['tests']):
            if not passes(t, ns):
                return i + 1
        return 0
    finally:
        os.chdir(cwd); sys.path.remove(d); shutil.rmtree(d)


nw = nm = 0
with np.errstate(all='ignore'):
    for fid, lab, w in WIDGETS:
        if w['kind'] != 'code':
            continue
        nw += 1
        lv.claim(first_fail(w, w['solution']) == 0, f'{fid} {lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{fid} {lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{fid} {lab}: at least two mutants')
        for m in w.get('mutants', []):
            nm += 1
            got = first_fail(w, m['source'])
            lv.claim(got == m['test'], f'{fid} {lab} mutant "{m["symptom"][:40]}" first fails test {m["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}, at {time.time() - T0:.0f} s')


# the exact values written into the hidden tests, recomputed by route B
def tex(f, unit, k, i):
    return eval(lv._file(f)[1][unit][k]['widget']['tests'][i]['expect'])


five = [18, 34, 140, 366, 0]
lv.claim(tex(L9, 'screens', 3, 2) == pred[five].tolist() and close(tex(L9, 'screens', 3, 3), pX[366], {'abs': 1e-9}), 'l9 forward tests: five classes and the ten probabilities of image 366')
lv.claim(tex(L9, 'screens', 5, 3) == cm.tolist() and close(tex(L9, 'screens', 7, 2), pc, None) and tex(L9, 'screens', 7, 3) == 8, 'l9 confusion and per-class tests')
lv.claim(close(tex(L10, 'screens', 9, 0), accx, None) and close(tex(L10, 'screens', 9, 1), accs, None) and close(tex(L10, 'screens', 9, 2), accv, None), 'l10 evaluate tests')
Pa, _ = o.fit(o.cnn_logits, o.init_cnn(8, 3), Xt[:96], yt[:96], 1, 0.01, 3)
Pb, _ = o.fit(o.cnn_logits, o.init_cnn(8, 4), Xt[:96], yt[:96], 2, 0.02, 4)
la = float(np.mean(-np.log(softB(cnnB(Pa, Xt[:96]))[np.arange(96), yt[:96]])))
lb = float(np.mean(-np.log(softB(cnnB(Pb, Xt[:96]))[np.arange(96), yt[:96]])))
lv.claim(close(tex(L10, 'screens', 5, 1), la, {'rel': 1e-7}) and close(tex(L10, 'screens', 5, 2), lb, {'rel': 1e-7}), f'l10 exact short runs: losses {la:.6f} (3 steps at 0.01) and {lb:.6f} (6 steps at 0.02) by fit and a plain NumPy loss')
lv.claim(close(tex(L11, 'screens', 8, 2), accr, None), 'l11 block test: the residual net’s held-out accuracy')
hh = np.maximum(convB(Xh[:2], WTS['res'][0], WTS['res'][1]), 0)
lv.claim(close(tex(L11, 'screens', 8, 1), blockB(hh, *WTS['res'][2:6])[0, :, 3, 3], {'abs': 1e-9}), 'l11 block test: one output pixel by plain NumPy')
lv.claim(close(tex(L11, 'screens', 8, 6), blockB(hh - 0.5, *WTS['res'][2:6])[0, :, 3, 3], {'abs': 1e-9}) and not close(tex(L11, 'screens', 8, 6), (np.maximum(hh - 0.5, 0) + blockB(hh - 0.5, *WTS['res'][2:6]) - (hh - 0.5))[0, :, 3, 3], {'abs': 1e-9}),
         'l11 signed-input block test: one output pixel on h - 0.5 by plain NumPy, and it differs from a block that clips the identity path')
pl_rec = eval(lv.files[L11]['screens'][10]['widget']['tests'][0]['setup'].split('; _rs = ')[0].split('_pl = ')[1])
lv.claim(pl_rec == [series(L11, 0, 'pl')] + pl_rec[1:] and tex(L11, 'screens', 10, 1) == [next(i for i, v in enumerate(p_ + [0]) if v <= 2.2) for p_ in pl_rec], 'l11 curve tests: the recorded plain curves and their stuck epochs')
lv.claim(close(tex(L12, 'screens', 9, 0), shx['exit'], None) and close(tex(L12, 'screens', 9, 1), shx['mlp'], None), 'l12 shifted-accuracy tests')
lv.claim(close(tex('homework', 'items', 0, 1), [accx, accm], None) and close(tex('homework', 'items', 0, 2), shx['exit'], None) and close(tex('homework', 'items', 0, 3), shx['mlp'], None), 'homework report tests')
gapf = np.mean([accB(cnnB, WTS['exit'], shiftB(Xh, dx, dy), yf) for dx, dy in SH]) - np.mean([accB(mlpB, WTS['mlp'], shiftB(Xh, dx, dy), yf) for dx, dy in SH])
lv.claim(accB(cnnB, WTS['exit'], Xh, yf) < 0.98 and gapf >= 0.10 and c1 - a1 < 0.10 and accs < 0.98, 'homework plants: relabelled set fails only the 0.98 bar; the augmented MLP breaks the margin; the 8-filter net fails the bar')
Pf1, _ = o.fit(o.cnn_logits, WTS['exit'], Xa[::50], ya[::50], 1, 0.01, 5)
Pf2, _ = o.fit(o.cnn_logits, WTS['exit'], Xa[::50], ya[::50], 2, 0.02, 6)
lf1 = float(np.mean(-np.log(softB(cnnB(Pf1, Xa[::50]))[np.arange(101), ya[::50]])))
lf2 = float(np.mean(-np.log(softB(cnnB(Pf2, Xa[::50]))[np.arange(101), ya[::50]])))
lv.claim(close(tex('homework', 'items', 1, 2), lf1, {'rel': 1e-7}) and close(tex('homework', 'items', 1, 3), lf2, {'rel': 1e-7}), f'homework fine-tune exact runs: {lf1:.6f} and {lf2:.6f}')
_mb = [0.7 * p + 0.3 * q for p, q in zip(WTS['mlp'], WTS['mlp-aug'])]
mix = float(np.mean([accB(mlpB, _mb, shiftB(Xh, dx, dy), yh) for dx, dy in SH]))
lv.claim(accx >= 0.98 and 0.05 < c1 - mix < 0.10 and round(c1 - mix, 2) == 0.08,
         f'homework plant 9: an MLP part way to the augmented one (0.7 of the plain weights, 0.3 of the augmented) trails the CNN by {c1 - mix:.4f}, above 0.05 and below 0.10; the CNN meets the bar')
print(f'done at {time.time() - T0:.0f} s')
lv.check_wrongs()
lv.report()
