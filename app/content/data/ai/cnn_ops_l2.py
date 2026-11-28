"""cnn level 2 ops: stride, padding, channels, im2col, and max and average pooling, for the frozen autograd.py (v1.0).

Arrays are (N, C, H, W): a batch of N images of C channels. A 3-D input (C, H, W) is treated as a batch of one and
returned without the batch axis. Convolution is the sliding dot product with no flip, as in cnn_ops_l1.
    out_size(n, k, p, s)            floor((n + 2p - k) / s) + 1
    im2col(x, k, stride, pad)       (N * oh * ow, C * k * k): one row per patch, channel-major inside a row
    col2im(cols, x_shape, k, stride, pad)   the adjoint: each row's values are ADDED back to the pixels they came from
    conv2d(x, W, b, stride=1, pad=0)        Tensor op; W (F, C, k, k), b (F,); out (N, F, oh, ow); backward by col2im
    maxpool2d(x, size), avgpool2d(x, size)  Tensor ops, windows size by size with stride size; H and W must divide.
Max pooling sends each window's gradient to its largest entry, the first one in row-major order on a tie.
Shipped verbatim beside autograd.py: from cnn_ops_l2 import out_size, im2col, col2im, conv2d, maxpool2d, avgpool2d.
"""
__version__ = "1.0"

import numpy as np
from autograd import Tensor


def _t(x):
    return x if isinstance(x, Tensor) else Tensor(x)


def out_size(n, k, p, s):
    """Output length along one axis: floor((n + 2p - k) / s) + 1; ValueError when no window fits."""
    if n + 2 * p < k:
        raise ValueError("the kernel is larger than the padded input")
    return (n + 2 * p - k) // s + 1


def im2col(x, k, stride=1, pad=0):
    """Patches of a (N, C, H, W) array as rows: shape (N * oh * ow, C * k * k)."""
    x = np.asarray(x, dtype=np.float64)
    n, c, h, w = x.shape
    oh, ow = out_size(h, k, pad, stride), out_size(w, k, pad, stride)
    xp = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    cols = np.empty((n, oh, ow, c, k, k))
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            cols[:, i, j] = xp[:, :, r:r + k, q:q + k]
    return cols.reshape(n * oh * ow, c * k * k)


def col2im(cols, x_shape, k, stride=1, pad=0):
    """Add each row of cols back into the pixels its patch came from (overlaps add), then strip the padding."""
    n, c, h, w = x_shape
    oh, ow = out_size(h, k, pad, stride), out_size(w, k, pad, stride)
    cols = np.asarray(cols, dtype=np.float64).reshape(n, oh, ow, c, k, k)
    xp = np.zeros((n, c, h + 2 * pad, w + 2 * pad))
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            xp[:, :, r:r + k, q:q + k] += cols[:, i, j]
    return xp[:, :, pad:pad + h, pad:pad + w]


def conv2d(x, W, b, stride=1, pad=0):
    """Tensor op: every filter of W over every channel of x, plus its bias. One matrix product forward and back."""
    x, W, b = _t(x), _t(W), _t(b)
    squeeze = x.data.ndim == 3
    xd = x.data[None] if squeeze else x.data
    n, c, h, w = xd.shape
    f, c2, k, k2 = W.shape
    if c2 != c or k2 != k:
        raise ValueError(f"filters {W.shape} do not fit an input of {c} channels")
    oh, ow = out_size(h, k, pad, stride), out_size(w, k, pad, stride)
    cols = im2col(xd, k, stride, pad)                       # (n*oh*ow, c*k*k)
    Wm = W.data.reshape(f, -1)                              # (f, c*k*k)
    y = (cols @ Wm.T + b.data).reshape(n, oh, ow, f).transpose(0, 3, 1, 2)
    out = Tensor(y[0] if squeeze else y, (x, W, b), "conv2d")

    def _backward():
        g = out.grad[None] if squeeze else out.grad
        gm = g.transpose(0, 2, 3, 1).reshape(-1, f)          # (n*oh*ow, f)
        W.grad += (gm.T @ cols).reshape(W.shape)
        b.grad += gm.sum(axis=0)
        dx = col2im(gm @ Wm, xd.shape, k, stride, pad)
        x.grad += dx[0] if squeeze else dx
    out._backward = _backward
    return out


def _windows(xd, size):
    n, c, h, w = xd.shape
    if h % size or w % size:
        raise ValueError(f"a {h} by {w} map does not split into {size} by {size} windows")
    return xd.reshape(n, c, h // size, size, w // size, size).transpose(0, 1, 2, 4, 3, 5).reshape(n, c, h // size, w // size, size * size)


def maxpool2d(x, size=2):
    """Tensor op: the largest entry of each size by size window; backward routes to the first largest entry."""
    x = _t(x)
    squeeze = x.data.ndim == 3
    xd = x.data[None] if squeeze else x.data
    win = _windows(xd, size)
    arg = win.argmax(axis=-1)                                # first largest, row-major inside the window
    y = np.take_along_axis(win, arg[..., None], axis=-1)[..., 0]
    out = Tensor(y[0] if squeeze else y, (x,), "maxpool2d")

    def _backward():
        g = out.grad[None] if squeeze else out.grad
        gw = np.zeros(win.shape)
        np.put_along_axis(gw, arg[..., None], g[..., None], axis=-1)
        n, c, hh, ww, _ = gw.shape
        dx = gw.reshape(n, c, hh, ww, size, size).transpose(0, 1, 2, 4, 3, 5).reshape(xd.shape)
        x.grad += dx[0] if squeeze else dx
    out._backward = _backward
    return out


def avgpool2d(x, size=2):
    """Tensor op: the mean of each size by size window; backward spreads each gradient equally over its window."""
    x = _t(x)
    squeeze = x.data.ndim == 3
    xd = x.data[None] if squeeze else x.data
    y = _windows(xd, size).mean(axis=-1)
    out = Tensor(y[0] if squeeze else y, (x,), "avgpool2d")

    def _backward():
        g = out.grad[None] if squeeze else out.grad
        dx = np.repeat(np.repeat(g, size, axis=2), size, axis=3) / (size * size)
        x.grad += dx[0] if squeeze else dx
    out._backward = _backward
    return out
