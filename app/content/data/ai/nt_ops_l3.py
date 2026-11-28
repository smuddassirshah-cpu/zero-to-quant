"""nn-train level 3 ops: weight decay, early stopping, dropout and random features, for autograd.py (v1.0).

    decayed_sgd_step(w, g, lr, lam)              SGD on loss + lam/2 |w|^2: (1 - lr lam) w - lr g, new array
    adamw_step(params, grads, m, v, t, lr, lam, b1=0.9, b2=0.999, eps=1e-8)
        Adam with decoupled weight decay: p - lr (mhat / (sqrt(vhat) + eps) + lam p); returns (params, m, v)
    early_stop(val_losses, patience)             (stop index, best index): stop after `patience` evaluations with no new best
    dropout(x, p, mode="train", rng=None)        Tensor op; train: zero each entry with chance p, scale survivors by 1/(1 - p);
                                                 returns (out, mask) with mask the 0 or 1/(1 - p) multipliers; eval: out = x, mask None
    random_relu_features(X, p, seed)             max(0, X W) for X (n, d): p random units, W (d, p) ~ N(0, 1/d) from default_rng(seed)
    min_norm_fit(F, y)                           the least-squares fit of smallest norm, np.linalg.pinv(F) @ y
Shipped verbatim beside autograd.py: from nt_ops_l3 import decayed_sgd_step, adamw_step, early_stop, dropout.
"""
__version__ = "1.0"

import numpy as np
from autograd import Tensor


def decayed_sgd_step(w, g, lr, lam):
    return (1 - lr * lam) * np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def adamw_step(params, grads, m, v, t, lr, lam, b1=0.9, b2=0.999, eps=1e-8):
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1 - b1 ** t, 1 - b2 ** t
    new = [p - lr * ((mi / c1) / (np.sqrt(vi / c2) + eps) + lam * p) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def early_stop(val_losses, patience):
    best, best_i = float("inf"), -1
    for i, loss in enumerate(val_losses):
        if loss < best:
            best, best_i = loss, i
        elif i - best_i >= patience:
            return i, best_i
    return len(val_losses) - 1, best_i


def dropout(x, p, mode="train", rng=None):
    x = x if isinstance(x, Tensor) else Tensor(x)
    if mode == "eval" or p == 0:
        return x, None
    if not 0 <= p < 1:
        raise ValueError("p must be in [0, 1)")
    rng = np.random.default_rng() if rng is None else rng
    mask = (rng.random(x.data.shape) >= p) / (1 - p)
    out = Tensor(x.data * mask, (x,), "dropout")

    def _backward():
        x.grad += out.grad * mask
    out._backward = _backward
    return out, mask


def random_relu_features(X, p, seed):
    g = np.random.default_rng(seed)
    X = np.asarray(X, dtype=float)
    X = X.reshape(-1, 1) if X.ndim == 1 else X
    W = g.standard_normal((X.shape[1], p)) / np.sqrt(X.shape[1])
    return np.maximum(X @ W, 0)


def min_norm_fit(F, y):
    return np.linalg.pinv(np.asarray(F, dtype=float)) @ np.asarray(y, dtype=float)
