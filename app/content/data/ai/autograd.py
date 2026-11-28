"""backprop level 4 autograd: a small array autograd in NumPy, shared by every later AI course.

A Tensor holds a float64 array `data` and a gradient `grad` of the same shape. Each operation
records its parents (`_prev`), a short name (`_op`) and a `_backward` closure that adds the
operation's share of the gradient into each parent. `backward()` on a size-1 tensor visits the
graph in reverse topological order, built with an explicit stack (no recursion).
Shipped verbatim; a later course that needs another op writes it in a module of its own.
"""
__version__ = "1.0"

import numpy as np


def _noop():
    pass


def _wrap(x):
    return x if isinstance(x, Tensor) else Tensor(x)


def unbroadcast(grad, shape):
    """Sum `grad` down to `shape`: over the leading axes broadcasting added, then over every axis where `shape` has 1."""
    shape = tuple(shape)
    grad = np.asarray(grad)
    extra = grad.ndim - len(shape)
    if extra > 0:
        grad = grad.sum(axis=tuple(range(extra)))
    axes = tuple(i for i, s in enumerate(shape) if s == 1 and grad.shape[i] != 1)
    if axes:
        grad = grad.sum(axis=axes, keepdims=True)
    return grad


class Tensor:
    __array_ufunc__ = None  # ndarray (op) Tensor defers to the Tensor's reflected method

    def __init__(self, data, _prev=(), _op=""):
        if isinstance(data, Tensor):
            data = data.data
        self.data = np.asarray(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data)
        self._prev = tuple(_prev)
        self._op = _op
        self._backward = _noop

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, op={self._op!r})"

    @property
    def shape(self):
        return self.data.shape

    def item(self):
        if self.data.size != 1:
            raise ValueError(f"item() needs a tensor of size 1, not shape {self.shape}")
        return float(self.data.reshape(()))

    def zero_grad(self):
        if self.grad.shape == self.data.shape:
            self.grad.fill(0.0)
        else:
            self.grad = np.zeros_like(self.data)

    # ---- elementwise binary operations (NumPy broadcasting; backward sums back with unbroadcast) ----
    def __add__(self, other):
        other = _wrap(other)
        out = Tensor(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += unbroadcast(out.grad, self.shape)
            other.grad += unbroadcast(out.grad, other.shape)
        out._backward = _backward
        return out

    def __radd__(self, other):
        return _wrap(other) + self

    def __sub__(self, other):
        other = _wrap(other)
        out = Tensor(self.data - other.data, (self, other), "-")

        def _backward():
            self.grad += unbroadcast(out.grad, self.shape)
            other.grad -= unbroadcast(out.grad, other.shape)
        out._backward = _backward
        return out

    def __rsub__(self, other):
        return _wrap(other) - self

    def __neg__(self):
        out = Tensor(-self.data, (self,), "neg")

        def _backward():
            self.grad -= out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = _wrap(other)
        out = Tensor(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += unbroadcast(other.data * out.grad, self.shape)
            other.grad += unbroadcast(self.data * out.grad, other.shape)
        out._backward = _backward
        return out

    def __rmul__(self, other):
        return _wrap(other) * self

    def __truediv__(self, other):
        other = _wrap(other)
        out = Tensor(self.data / other.data, (self, other), "/")

        def _backward():
            self.grad += unbroadcast(out.grad / other.data, self.shape)
            other.grad -= unbroadcast(out.grad * self.data / other.data ** 2, other.shape)
        out._backward = _backward
        return out

    def __rtruediv__(self, other):
        return _wrap(other) / self

    def __pow__(self, k):
        if isinstance(k, Tensor):
            raise TypeError("the power k in a ** k must be a Python number, not a Tensor")
        out = Tensor(self.data ** k, (self,), f"**{k}")

        def _backward():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _backward
        return out

    # ---- matrix product: backward G B^T and A^T G (stacks of matrices broadcast as np.matmul does) ----
    def __matmul__(self, other):
        other = _wrap(other)
        if self.data.ndim < 2 or other.data.ndim < 2:
            raise ValueError("@ needs tensors of at least 2 dimensions: reshape a vector to (n, 1) or (1, n) first")
        out = Tensor(self.data @ other.data, (self, other), "@")

        def _backward():
            self.grad += unbroadcast(out.grad @ np.swapaxes(other.data, -1, -2), self.shape)
            other.grad += unbroadcast(np.swapaxes(self.data, -1, -2) @ out.grad, other.shape)
        out._backward = _backward
        return out

    def __rmatmul__(self, other):
        return _wrap(other) @ self

    # ---- reductions ----
    def sum(self, axis=None, keepdims=False):
        out = Tensor(self.data.sum(axis=axis, keepdims=keepdims), (self,), "sum")

        def _backward():
            g = out.grad
            if axis is not None and not keepdims:
                g = np.expand_dims(g, axis)
            self.grad += np.broadcast_to(g, self.shape)
        out._backward = _backward
        return out

    def mean(self, axis=None, keepdims=False):
        out = Tensor(self.data.mean(axis=axis, keepdims=keepdims), (self,), "mean")
        n = self.data.size // max(out.data.size, 1)

        def _backward():
            g = out.grad / n
            if axis is not None and not keepdims:
                g = np.expand_dims(g, axis)
            self.grad += np.broadcast_to(g, self.shape)
        out._backward = _backward
        return out

    # ---- elementwise functions ----
    def tanh(self):
        t = np.tanh(self.data)
        out = Tensor(t, (self,), "tanh")

        def _backward():
            self.grad += (1.0 - t * t) * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Tensor(np.maximum(self.data, 0.0), (self,), "relu")

        def _backward():
            self.grad += (self.data > 0) * out.grad  # slope 0 at exactly 0
        out._backward = _backward
        return out

    def exp(self):
        e = np.exp(self.data)
        out = Tensor(e, (self,), "exp")

        def _backward():
            self.grad += e * out.grad
        out._backward = _backward
        return out

    def log(self):
        out = Tensor(np.log(self.data), (self,), "log")

        def _backward():
            self.grad += out.grad / self.data
        out._backward = _backward
        return out

    # ---- shape operations ----
    def reshape(self, *shape):
        out = Tensor(self.data.reshape(*shape), (self,), "reshape")

        def _backward():
            self.grad += out.grad.reshape(self.shape)
        out._backward = _backward
        return out

    @property
    def T(self):
        out = Tensor(self.data.T, (self,), "T")

        def _backward():
            self.grad += out.grad.T
        out._backward = _backward
        return out

    def __getitem__(self, idx):
        if isinstance(idx, Tensor):
            raise TypeError("index with an integer array or a tuple of them, not a Tensor")
        out = Tensor(self.data[idx], (self,), "index")

        def _backward():
            np.add.at(self.grad, idx, out.grad)  # repeated indices add, as in an embedding lookup
        out._backward = _backward
        return out

    # ---- the backward pass ----
    def backward(self):
        if self.data.size != 1:
            raise ValueError(f"backward() needs a tensor of size 1 (a loss), not shape {self.shape}")
        order, seen, stack = [], set(), [(self, False)]
        while stack:
            node, parents_done = stack.pop()
            if parents_done:
                order.append(node)
                continue
            if id(node) in seen:
                continue
            seen.add(id(node))
            stack.append((node, True))
            for p in node._prev:
                if id(p) not in seen:
                    stack.append((p, False))
        self.grad = np.ones_like(self.data)
        for node in reversed(order):
            node._backward()


def softmax(x, axis=-1):
    """Softmax of a plain array along `axis`, largest entry subtracted first; no gradient (for sampling and reporting)."""
    x = x.data if isinstance(x, Tensor) else np.asarray(x, dtype=np.float64)
    z = np.exp(x - x.max(axis=axis, keepdims=True))
    return z / z.sum(axis=axis, keepdims=True)


def cross_entropy(logits, targets):
    """Mean over the n rows of -log softmax(z_i)[y_i], in nats, by log-sum-exp; backward (softmax(z) - onehot(y)) / n."""
    logits = _wrap(logits)
    z = logits.data
    y = np.asarray(targets)
    if z.ndim != 2:
        raise ValueError(f"logits must be 2-D (n, K), not shape {z.shape}")
    if y.ndim != 1 or y.shape[0] != z.shape[0]:
        raise ValueError(f"targets must be 1-D of length {z.shape[0]}, not shape {y.shape}")
    if not np.issubdtype(y.dtype, np.integer):
        raise TypeError("targets must be integer class indices")
    n = z.shape[0]
    rows = np.arange(n)
    m = z.max(axis=1, keepdims=True)
    e = np.exp(z - m)
    s = e.sum(axis=1, keepdims=True)
    lse = (m + np.log(s))[:, 0]
    out = Tensor(np.mean(lse - z[rows, y]), (logits,), "cross_entropy")

    def _backward():
        p = e / s
        p[rows, y] -= 1.0
        logits.grad += p * (out.grad / n)
    out._backward = _backward
    return out


def concat(tensors, axis=0):
    """Join tensors along `axis`; backward hands each its own slice of the gradient."""
    tensors = [_wrap(t) for t in tensors]
    out = Tensor(np.concatenate([t.data for t in tensors], axis=axis), tuple(tensors), "concat")

    def _backward():
        start = 0
        for t in tensors:
            size = t.data.shape[axis]
            cut = [slice(None)] * out.data.ndim
            cut[axis] = slice(start, start + size)
            t.grad += out.grad[tuple(cut)]
            start += size
    out._backward = _backward
    return out


def sgd_step(params, lr):
    """One gradient-descent step in place, outside the graph. It does not zero the gradients."""
    for p in params:
        p.data -= lr * p.grad


def grad_check(f, params, h=1e-5):
    """Global relative error between backprop and central differences of f() over every entry of every parameter."""
    params = list(params)
    for p in params:
        p.zero_grad()
    f().backward()
    analytic = [p.grad.copy() for p in params]
    worst, scale = 0.0, 1e-12
    for p, g in zip(params, analytic):
        for i in np.ndindex(p.data.shape):
            keep = p.data[i]
            p.data[i] = keep + h
            up = f().item()
            p.data[i] = keep - h
            down = f().item()
            p.data[i] = keep
            num = (up - down) / (2 * h)
            worst = max(worst, abs(g[i] - num))
            scale = max(scale, abs(g[i]), abs(num))
    return worst / scale
