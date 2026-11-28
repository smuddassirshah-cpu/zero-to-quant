"""nn-train level 1 ops: the course's spiral data and network, minibatches, and the three optimisers and the schedule.

Built on the frozen autograd.py (v1.0). Parameters are a list of float64 arrays; an optimiser is a plain function of the
parameter list and the gradient list, so it runs on any problem (a quadratic bowl, a network) without the autograd.
    spirals(n=400, seed=0, noise=0.05)        X (n, 2) and y (n,) in {0, 1}: two arms of one turn each, shuffled
    init_net(sizes=(2, 16, 16, 2), seed=0)    [W1, b1, W2, b2, ...]: W (fan_in, fan_out) ~ N(0, 1/fan_in), b = 0
    forward(params, X)                        logits as a Tensor; tanh on every hidden layer, X @ W + b
    loss_and_grads(params, X, y, scale=1.0)   (mean cross-entropy in nats times scale, list of gradient arrays)
    full_loss(params, X, y)                   the mean cross-entropy as a float, no gradient
    minibatch_indices(n, B, seed)             one epoch: a permutation from default_rng(seed) cut into batches of B
    sgd_step(params, grads, lr)               p - lr * g, new arrays
    momentum_step(params, vels, grads, lr, beta)              heavy ball: v = beta v - lr g, p = p + v
    adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8)   bias-corrected Adam, t counts from 1
    warmup_cosine(t, lr_max, warmup, total)   linear warm-up over `warmup` steps, then cosine to 0 at `total`, clamped
Every function returns new arrays and leaves its inputs unchanged.
Shipped verbatim beside autograd.py: from nt_ops_l1 import spirals, init_net, loss_and_grads, sgd_step, momentum_step, adam_step.
"""
__version__ = "1.0"

import math

import numpy as np
from autograd import Tensor, cross_entropy

def spirals(n=400, seed=0, noise=0.05):
    """Two interleaved spiral arms, n // 2 points each, labels 0 and 1, rows shuffled."""
    g = np.random.default_rng(seed)
    m = n // 2
    xs, ys = [], []
    for k in (0, 1):
        t = np.sqrt(g.random(m)) * 2 * np.pi
        r = t / (2 * np.pi)
        pts = np.c_[r * np.cos(t + k * np.pi), r * np.sin(t + k * np.pi)] + noise * g.standard_normal((m, 2))
        xs.append(pts)
        ys.append(np.full(m, k))
    X, y = np.vstack(xs), np.concatenate(ys)
    order = g.permutation(2 * m)
    return X[order], y[order]


def init_net(sizes=(2, 16, 16, 2), seed=0):
    """Weights drawn N(0, 1/fan_in) from default_rng(seed), layer by layer; biases zero."""
    g = np.random.default_rng(seed)
    params = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        params.append(g.standard_normal((a, b)) / math.sqrt(a))
        params.append(np.zeros(b))
    return params


def forward(params, X):
    """Logits of the tanh network as a Tensor; `params` may be arrays or Tensors."""
    h = X if isinstance(X, Tensor) else Tensor(X)
    n = len(params) // 2
    for i in range(n):
        h = h @ params[2 * i] + params[2 * i + 1]
        if i < n - 1:
            h = h.tanh()
    return h


def loss_and_grads(params, X, y, scale=1.0):
    """Mean cross-entropy (nats) times `scale`, and the gradient of that with respect to each parameter."""
    ts = [Tensor(p) for p in params]
    loss = cross_entropy(forward(ts, X), np.asarray(y, dtype=np.int64)) * scale
    loss.backward()
    return loss.item(), [t.grad.copy() for t in ts]


def full_loss(params, X, y):
    """The mean cross-entropy over all rows, as a float."""
    return cross_entropy(forward(params, X), np.asarray(y, dtype=np.int64)).item()


def minibatch_indices(n, B, seed):
    """One epoch of minibatches: default_rng(seed).permutation(n) cut into consecutive slices of B (the last may be short)."""
    order = np.random.default_rng(seed).permutation(n)
    return [order[i:i + B] for i in range(0, n, B)]


def sgd_step(params, grads, lr):
    return [p - lr * g for p, g in zip(params, grads)]


def momentum_step(params, vels, grads, lr, beta):
    """Heavy-ball momentum on lists: returns (new params, new velocities)."""
    new_v = [beta * v - lr * g for v, g in zip(vels, grads)]
    return [p + v for p, v in zip(params, new_v)], new_v


def adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    """One Adam step at step number t (from 1): returns (new params, new m, new v)."""
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1 - b1 ** t, 1 - b2 ** t
    new = [p - lr * (mi / c1) / (np.sqrt(vi / c2) + eps) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def warmup_cosine(t, lr_max, warmup, total):
    """The rate at step t (from 0): t / warmup * lr_max during warm-up, then half a cosine from lr_max to 0 at total."""
    t = min(max(t, 0), total)
    if t < warmup:
        return lr_max * t / warmup
    span = total - warmup
    if span <= 0:
        return lr_max
    return lr_max * 0.5 * (1 + math.cos(math.pi * (t - warmup) / span))
