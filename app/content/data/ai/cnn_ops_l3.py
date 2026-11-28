"""cnn level 3 ops: the digits split, the digits CNN, a same-size MLP, a residual block, shifts and scores.

Built on the frozen autograd.py (v1.0) and cnn_ops_l2.py (v1.0); images are (N, 1, 8, 8) arrays of grey levels / 16.
    load_split(path="cnn-digits.txt")       (X_tr, y_tr, X_va, y_va, X_te, y_te): 1,005 train, 252 validation, 540 test
    conv2d(x, W, b, stride=1, pad=0)        cnn_ops_l2.conv2d after shape checks: ValueError for a bias that is not (F,),
                                            a stride below 1 or a negative padding (the frozen op lets these through)
    init_cnn(filters=16, seed=0)            [W (F, 1, 3, 3), b (F,), V (16F, 10), c (10,)]: He for the convolution,
                                            1/sqrt(fan_in) for the dense layer, biases 0, all from default_rng(seed)
    cnn_logits(params, X)                   conv 3 by 3 with padding 1, ReLU, 2 by 2 max pool, flatten, dense: (N, 10) Tensor
    init_mlp(hidden=40, seed=0)             [W1 (64, 40), b1, W2 (40, 10), b2]; mlp_logits(params, X): ReLU hidden layer
    init_res(seed=0, zero_last=True, sd=None)   [W, b, A1, a1, A2, a2, V, c]: the CNN with two 16-to-16 convolutions in
                                            a block; A1, A2 He-scaled (or sd), A2 zero when zero_last (the block starts as x)
    block(h, A1, a1, A2, a2, skip=True)     F(h) = conv(relu(conv(h))) with padding 1; returns h + F(h), or F(h) with skip=False
    res_logits(params, X, skip=True)        conv, ReLU, block, max pool, dense
    predict(logits_fn, params, X, batch=256)  class indices, in mini-batches of `batch` images (im2col memory stays small)
    accuracy(logits_fn, params, X, y)       share of rows predicted right
    confusion(y_true, y_pred, k=10)         k by k counts, row = true class, column = predicted
    shift_images(X, dx, dy)                 move every image dx pixels right and dy pixels down, zero fill
    fit(logits_fn, params, X, y, epochs, lr, seed, batch=32, cosine=False, opt="adam", on_epoch=None)
                                            Adam (nt_ops_l1.adam_step, step count from 1, never reset) or plain gradient
                                            descent (opt="sgd"); batches nt_ops_l1.minibatch_indices(n, batch, seed + epoch);
                                            cosine=True decays the rate to 0 by nt_ops_l1.warmup_cosine over every step;
                                            on_epoch(epoch, params) runs after each epoch. Returns (new params, losses): the
                                            mean training loss of each epoch. The arrays passed in are not changed.
    load_weights(path), save_weights(params, path)   a JSON list of nested lists
Shipped verbatim beside autograd.py, cnn_ops_l2.py and nt_ops_l1.py.
"""
__version__ = "1.0"

import json
import math

import numpy as np
from autograd import Tensor, cross_entropy
import cnn_ops_l2
from cnn_ops_l2 import maxpool2d
from nt_ops_l1 import adam_step, minibatch_indices, warmup_cosine

_DIGITS = "0123456789abcdefg"


def load_split(path="cnn-digits.txt"):
    """Read the split file: one image a line, a split letter (t, v, h), the label, then 64 grey levels 0 to g (16)."""
    parts = {"t": ([], []), "v": ([], []), "h": ([], [])}
    with open(path, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            xs, ys = parts[line[0]]
            ys.append(int(line[1]))
            xs.append([_DIGITS.index(ch) for ch in line[2:66]])
    out = []
    for key in "tvh":
        xs, ys = parts[key]
        out.append(np.array(xs, dtype=np.float64).reshape(-1, 1, 8, 8) / 16.0)
        out.append(np.array(ys, dtype=np.int64))
    return tuple(out)


def conv2d(x, W, b, stride=1, pad=0):
    """cnn_ops_l2.conv2d with the checks it lacks."""
    f = (W.data if isinstance(W, Tensor) else np.asarray(W)).shape[0]
    bs = (b.data if isinstance(b, Tensor) else np.asarray(b)).shape
    if bs != (f,):
        raise ValueError(f"the bias must have shape ({f},), one per filter, not {bs}")
    if stride < 1 or pad < 0:
        raise ValueError("the stride must be at least 1 and the padding at least 0")
    return cnn_ops_l2.conv2d(x, W, b, stride, pad)


def init_cnn(filters=16, seed=0):
    g = np.random.default_rng(seed)
    W = g.standard_normal((filters, 1, 3, 3)) * math.sqrt(2 / 9)
    V = g.standard_normal((16 * filters, 10)) / math.sqrt(16 * filters)
    return [W, np.zeros(filters), V, np.zeros(10)]


def cnn_logits(params, X):
    W, b, V, c = params
    h = maxpool2d(conv2d(X, W, b, 1, 1).relu(), 2)
    return h.reshape(h.shape[0], -1) @ V + c


def init_mlp(hidden=40, seed=0):
    g = np.random.default_rng(seed)
    return [g.standard_normal((64, hidden)) * math.sqrt(2 / 64), np.zeros(hidden),
            g.standard_normal((hidden, 10)) / math.sqrt(hidden), np.zeros(10)]


def mlp_logits(params, X):
    W1, b1, W2, b2 = params
    X = X.data if isinstance(X, Tensor) else np.asarray(X)
    h = (Tensor(X.reshape(X.shape[0], -1)) @ W1 + b1).relu()
    return h @ W2 + b2


def init_res(seed=0, zero_last=True, sd=None):
    g = np.random.default_rng(seed)
    W = g.standard_normal((16, 1, 3, 3)) * math.sqrt(2 / 9)
    s = math.sqrt(2 / 144) if sd is None else sd
    A1 = g.standard_normal((16, 16, 3, 3)) * s
    A2 = g.standard_normal((16, 16, 3, 3)) * s
    if zero_last:
        A2 = A2 * 0.0
    V = g.standard_normal((256, 10)) / 16.0
    return [W, np.zeros(16), A1, np.zeros(16), A2, np.zeros(16), V, np.zeros(10)]


def block(h, A1, a1, A2, a2, skip=True):
    h = h if isinstance(h, Tensor) else Tensor(h)
    F = conv2d(conv2d(h, A1, a1, 1, 1).relu(), A2, a2, 1, 1)
    return h + F if skip else F


def res_logits(params, X, skip=True):
    W, b, A1, a1, A2, a2, V, c = params
    h = conv2d(X, W, b, 1, 1).relu()
    h = maxpool2d(block(h, A1, a1, A2, a2, skip), 2)
    return h.reshape(h.shape[0], -1) @ V + c


def predict(logits_fn, params, X, batch=256):
    out = [logits_fn(params, X[i:i + batch]).data.argmax(axis=1) for i in range(0, len(X), batch)]
    return np.concatenate(out)


def accuracy(logits_fn, params, X, y):
    return float((predict(logits_fn, params, X) == np.asarray(y)).mean())


def confusion(y_true, y_pred, k=10):
    cm = np.zeros((k, k), dtype=np.int64)
    for t, p in zip(y_true, y_pred):
        cm[int(t), int(p)] += 1
    return cm


def shift_images(X, dx, dy):
    X = np.asarray(X, dtype=np.float64)
    out = np.zeros_like(X)
    h, w = X.shape[-2], X.shape[-1]
    src_r = slice(max(0, -dy), min(h, h - dy))
    dst_r = slice(max(0, dy), min(h, h + dy))
    src_c = slice(max(0, -dx), min(w, w - dx))
    dst_c = slice(max(0, dx), min(w, w + dx))
    out[..., dst_r, dst_c] = X[..., src_r, src_c]
    return out


def fit(logits_fn, params, X, y, epochs, lr, seed, batch=32, cosine=False, opt="adam", on_epoch=None):
    params = [np.array(p, dtype=np.float64) for p in params]
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    t, losses = 0, []
    total_steps = epochs * math.ceil(len(X) / batch)
    for epoch in range(epochs):
        total = 0.0
        for idx in minibatch_indices(len(X), batch, seed + epoch):
            ts = [Tensor(p) for p in params]
            loss = cross_entropy(logits_fn(ts, X[idx]), y[idx])
            loss.backward()
            t += 1
            rate = warmup_cosine(t - 1, lr, 0, total_steps) if cosine else lr
            if opt == "sgd":
                params = [p - rate * q.grad for p, q in zip(params, ts)]
            else:
                params, m, v = adam_step(params, [p.grad for p in ts], m, v, t, rate)
            total += loss.item() * len(idx)
        losses.append(total / len(X))
        if on_epoch is not None:
            on_epoch(epoch, params)
    return params, losses


def load_weights(path):
    with open(path, encoding="utf8") as f:
        return [np.array(a, dtype=np.float64) for a in json.load(f)]


def save_weights(params, path, digits=7):
    with open(path, "w", encoding="utf8") as f:
        json.dump([np.round(np.asarray(p, dtype=np.float64), digits).tolist() for p in params], f, separators=(",", ":"))
