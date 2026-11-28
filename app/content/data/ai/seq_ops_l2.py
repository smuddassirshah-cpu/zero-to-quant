"""sequence level 2 ops: the two pieces attention needs that autograd.py (v1.0) lacks.

softmax(x, axis=-1): a differentiable softmax on a Tensor along any axis (the largest entry is subtracted first).
swap_last(x): swap the last two axes of a Tensor (K^T for a stack of matrices; Tensor.T reverses every axis).
Both work on Tensors of any number of dimensions, in float64, and are gradient-checked in docs/reports/sequence-L2-numbers.py.
Frozen once merged: later levels and courses import them, never edit them.
"""
__version__ = "1.0"

import numpy as np

from autograd import Tensor, _wrap


def softmax(x, axis=-1):
    """Softmax of a Tensor along `axis`; backward s * (g - sum(g * s along axis))."""
    x = _wrap(x)
    z = np.exp(x.data - x.data.max(axis=axis, keepdims=True))
    s = z / z.sum(axis=axis, keepdims=True)
    out = Tensor(s, (x,), "softmax")

    def _backward():
        g = out.grad
        x.grad += s * (g - (g * s).sum(axis=axis, keepdims=True))
    out._backward = _backward
    return out


def swap_last(x):
    """Swap the last two axes of a Tensor of 2 or more dimensions; backward swaps the gradient back."""
    x = _wrap(x)
    if x.data.ndim < 2:
        raise ValueError("swap_last needs a tensor of at least 2 dimensions")
    out = Tensor(np.swapaxes(x.data, -1, -2), (x,), "swap_last")

    def _backward():
        x.grad += np.swapaxes(out.grad, -1, -2)
    out._backward = _backward
    return out
