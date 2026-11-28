"""sequence level 3 ops: masks, heads and scaled attention on Tensors, built on autograd.py (v1.0) and seq_ops_l2.py.

causal_mask(T): a T by T array, 0 on and below the diagonal and -inf above it (add it to the scores).
permute(x, axes): reorder the axes of a Tensor, as np.transpose(x, axes); backward applies the inverse order.
split_heads(x, h): (..., T, d) -> (..., h, T, d/h), cutting the feature axis into h heads.
merge_heads(x): (..., h, T, dh) -> (..., T, h*dh), the inverse of split_heads.
attention(Q, K, V, mask=None): softmax(Q K^T / sqrt(d) + mask) V on Tensors, the softmax along the last axis.
Gradient-checked in docs/reports/sequence-L3-numbers.py. Frozen once merged: later levels and courses import it, never edit it.
"""
__version__ = "1.0"

import numpy as np

from autograd import Tensor, _wrap
from seq_ops_l2 import softmax, swap_last


def causal_mask(T):
    """T by T float array: 0 where key j <= query i, -inf where j > i."""
    return np.triu(np.full((T, T), -np.inf), 1)


def permute(x, axes):
    """np.transpose of a Tensor by `axes`; backward transposes the gradient by the inverse permutation."""
    x = _wrap(x)
    axes = tuple(axes)
    inv = tuple(np.argsort(axes))
    out = Tensor(np.transpose(x.data, axes), (x,), "permute")

    def _backward():
        x.grad += np.transpose(out.grad, inv)
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
    return softmax(S, axis=-1) @ V
