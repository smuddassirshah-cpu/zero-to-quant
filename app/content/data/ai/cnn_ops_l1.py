"""cnn level 1 ops: valid 1-D and 2-D convolution as Tensor ops for the frozen autograd.py (v1.0).

Deep learning's "convolution" is the sliding dot product with no flip (cross-correlation), and so are these:
    conv1d(x, k)[t]     = sum_j k[j] * x[t + j],              t = 0 .. n - m
    conv2d(x, k)[i, j]  = sum_a sum_b k[a, b] * x[i + a, j + b]  (valid positions only)
Each op records its parents and a backward closure, as every op in autograd.py does, so loss.backward() reaches the
input and the kernel. The plain-array helpers correlate1d and correlate2d do the forward pass alone.
Shipped verbatim beside autograd.py: from cnn_ops_l1 import conv1d, conv2d, correlate1d, correlate2d.
"""
__version__ = "1.0"

import numpy as np
from autograd import Tensor


def _t(x):
    return x if isinstance(x, Tensor) else Tensor(x)


def correlate1d(x, k):
    """Valid sliding dot product of two 1-D arrays: n - m + 1 outputs (none when the kernel is longer)."""
    x = np.asarray(x, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    n, m = x.shape[0], k.shape[0]
    if m > n:
        return np.zeros(0)
    return np.array([x[t:t + m] @ k for t in range(n - m + 1)])


def correlate2d(x, k):
    """Valid sliding dot product of a 2-D array with a 2-D kernel: (H - kh + 1, W - kw + 1) outputs."""
    x = np.asarray(x, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    oh, ow = x.shape[0] - k.shape[0] + 1, x.shape[1] - k.shape[1] + 1
    if oh < 1 or ow < 1:
        return np.zeros((max(oh, 0), max(ow, 0)))
    win = np.lib.stride_tricks.sliding_window_view(x, k.shape)
    return np.einsum('ijab,ab->ij', win, k)


def conv1d(x, k):
    """Tensor op: valid 1-D convolution (no flip). Backward: dk = correlate1d(x, g); dx = full np.convolve(g, k)."""
    x, k = _t(x), _t(k)
    if x.data.ndim != 1 or k.data.ndim != 1:
        raise ValueError("conv1d needs a 1-D signal and a 1-D kernel")
    if k.shape[0] > x.shape[0]:
        raise ValueError("the kernel is longer than the signal: no valid position")
    out = Tensor(correlate1d(x.data, k.data), (x, k), "conv1d")

    def _backward():
        g = out.grad
        k.grad += correlate1d(x.data, g)
        x.grad += np.convolve(g, k.data)  # each input entry collects g[t] * k[j] from every window it sits in
    out._backward = _backward
    return out


def conv2d(x, k):
    """Tensor op: valid 2-D convolution (no flip) of one 2-D channel. Backward: dk sums window * g; dx adds k[a, b] * g back."""
    x, k = _t(x), _t(k)
    if x.data.ndim != 2 or k.data.ndim != 2:
        raise ValueError("conv2d needs a 2-D image and a 2-D kernel")
    kh, kw = k.shape
    oh, ow = x.shape[0] - kh + 1, x.shape[1] - kw + 1
    if oh < 1 or ow < 1:
        raise ValueError("the kernel is larger than the image: no valid position")
    out = Tensor(correlate2d(x.data, k.data), (x, k), "conv2d")

    def _backward():
        g = out.grad
        win = np.lib.stride_tricks.sliding_window_view(x.data, (kh, kw))
        k.grad += np.einsum('ijab,ij->ab', win, g)
        for a in range(kh):
            for b in range(kw):
                x.grad[a:a + oh, b:b + ow] += k.data[a, b] * g  # overlapping windows add
    out._backward = _backward
    return out
