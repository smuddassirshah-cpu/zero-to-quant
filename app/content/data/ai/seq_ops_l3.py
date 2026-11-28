"""sequence level 3 ops: masks, heads and scaled attention on Tensors, built on autograd.py (v1.0) and seq_ops_l2.py.

causal_mask(T): a T by T array, 0 on and below the diagonal and -inf above it (add it to the scores).
permute(x, axes): reorder the axes of a Tensor, as np.transpose(x, axes), negative axes allowed; backward applies the inverse order.
split_heads(x, h): (..., T, d) -> (..., h, T, d/h), cutting the feature axis into h heads.
merge_heads(x): (..., h, T, dh) -> (..., T, h*dh), the inverse of split_heads.
attention(Q, K, V, mask=None): softmax(Q K^T / sqrt(d) + mask) V on Tensors, the softmax along the last axis.
  `mask` is a NumPy array; a query row whose mask is -inf everywhere gets weights 0 (output 0, gradient 0), not NaN.
Gradient-checked in docs/reports/sequence-L3-numbers.py. Frozen once merged: later levels and courses import it, never edit it.
v1.1: permute normalises negative axes (the backward was wrong for them); a fully masked softmax row gives zeros, not NaN.
Every other behaviour and signature is as in v1.0; `axes` is required, as is a NumPy array for `mask`.
"""
__version__ = "1.1"

import numpy as np

from autograd import Tensor, _wrap
from seq_ops_l2 import softmax, swap_last


def causal_mask(T):
    """T by T float array: 0 where key j <= query i, -inf where j > i."""
    return np.triu(np.full((T, T), -np.inf), 1)


def permute(x, axes):
    """np.transpose of a Tensor by `axes`; backward transposes the gradient by the inverse permutation."""
    x = _wrap(x)
    axes = tuple(int(a) % x.data.ndim for a in axes)
    inv = tuple(np.argsort(axes))
    out = Tensor(np.transpose(x.data, axes), (x,), "permute")

    def _backward():
        x.grad += np.transpose(out.grad, inv)
    out._backward = _backward
    return out


def _masked_softmax(x, axis=-1):
    """seq_ops_l2.softmax, except that a slice with every entry at -inf gives weights 0 and gradient 0 (not NaN)."""
    x = _wrap(x)
    m = x.data.max(axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    z = np.exp(x.data - m)
    tot = z.sum(axis=axis, keepdims=True)
    s = z / np.where(tot > 0, tot, 1.0)
    out = Tensor(s, (x,), "softmax")

    def _backward():
        g = out.grad
        x.grad += s * (g - (g * s).sum(axis=axis, keepdims=True))
    out._backward = _backward
    return out


def split_heads(x, h):
    """(..., T, d) -> (..., h, T, d // h): head k holds features k*d/h to (k+1)*d/h - 1."""
    x = _wrap(x)
    *lead, T, d = x.shape
    if d % h:
        raise ValueError(f"width {d} does not split into {h} heads")
    y = x.reshape(*lead, T, h, d // h)
    n = len(lead)
    return permute(y, tuple(range(n)) + (n + 1, n, n + 2))


def merge_heads(x):
    """(..., h, T, dh) -> (..., T, h * dh), undoing split_heads."""
    x = _wrap(x)
    *lead, h, T, dh = x.shape
    n = len(lead)
    y = permute(x, tuple(range(n)) + (n + 1, n, n + 2))
    return y.reshape(*lead, T, h * dh)


def attention(Q, K, V, mask=None):
    """Scaled dot-product attention on Tensors: softmax(Q K^T / sqrt(d) + mask) V, d the last axis of Q."""
    Q, K, V = _wrap(Q), _wrap(K), _wrap(V)
    S = (Q @ swap_last(K)) * (1.0 / np.sqrt(Q.shape[-1]))
    if mask is not None:
        S = S + np.asarray(mask, dtype=np.float64)
    return _masked_softmax(S, axis=-1) @ V
