"""Reference sketch of the backprop level 4 contract (docs/briefs/backprop.md), written by the brief writer only to show that the
contract is coherent and that its stated checks pass. The canonical app/content/data/ai/autograd.py is the level 4 author's."""
__version__ = "ref"
import numpy as np

def unbroadcast(grad, shape):
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and grad.shape[i] != 1:
            grad = grad.sum(axis=i, keepdims=True)
    return grad

def _t(x):
    return x if isinstance(x, Tensor) else Tensor(x)

class Tensor:
    def __init__(self, data, _prev=(), _op=''):
        self.data = np.asarray(data, dtype=np.float64); self.grad = np.zeros_like(self.data)
        self._prev = tuple(_prev); self._op = _op; self._backward = lambda: None
    shape = property(lambda self: self.data.shape)
    T = property(lambda self: self._unary(self.data.T, lambda g: g.T, 'T'))
    def item(self): return float(self.data)
    def _unary(self, out_data, back, op):
        out = Tensor(out_data, (self,), op)
        def b(): self.grad = self.grad + back(out.grad)
        out._backward = b; return out
    def __add__(self, o):
        o = _t(o); out = Tensor(self.data + o.data, (self, o), '+')
        def b():
            self.grad = self.grad + unbroadcast(out.grad, self.shape); o.grad = o.grad + unbroadcast(out.grad, o.shape)
        out._backward = b; return out
    __radd__ = __add__
    def __mul__(self, o):
        o = _t(o); out = Tensor(self.data * o.data, (self, o), '*')
        def b():
            self.grad = self.grad + unbroadcast(o.data * out.grad, self.shape); o.grad = o.grad + unbroadcast(self.data * out.grad, o.shape)
        out._backward = b; return out
    __rmul__ = __mul__
    def __neg__(self): return self * -1.0
    def __sub__(self, o): return self + (-_t(o))
    def __rsub__(self, o): return _t(o) + (-self)
    def __pow__(self, k): return self._unary(self.data ** k, lambda g: g * k * self.data ** (k - 1), f'**{k}')
    def __truediv__(self, o): return self * (_t(o) ** -1.0)
    def __rtruediv__(self, o): return _t(o) * (self ** -1.0)
    def __matmul__(self, o):
        o = _t(o); out = Tensor(self.data @ o.data, (self, o), '@')
        def b(): self.grad = self.grad + out.grad @ o.data.T; o.grad = o.grad + self.data.T @ out.grad
        out._backward = b; return out
    def sum(self, axis=None, keepdims=False):
        def back(g):
            if axis is not None and not keepdims: g = np.expand_dims(g, axis)
            return np.broadcast_to(g, self.shape).copy()
        return self._unary(self.data.sum(axis=axis, keepdims=keepdims), back, 'sum')
    def mean(self, axis=None, keepdims=False):
        n = self.data.size if axis is None else self.data.shape[axis]
        return self.sum(axis, keepdims) * (1.0 / n)
    def tanh(self):
        t = np.tanh(self.data); return self._unary(t, lambda g: g * (1 - t * t), 'tanh')
    def relu(self): return self._unary(np.maximum(self.data, 0), lambda g: g * (self.data > 0), 'relu')
    def exp(self):
        e = np.exp(self.data); return self._unary(e, lambda g: g * e, 'exp')
    def log(self): return self._unary(np.log(self.data), lambda g: g / self.data, 'log')
    def reshape(self, *shape): return self._unary(self.data.reshape(*shape), lambda g: g.reshape(self.shape), 'reshape')
    def __getitem__(self, idx):
        def back(g):
            z = np.zeros_like(self.data); np.add.at(z, idx, g); return z
        return self._unary(self.data[idx], back, 'index')
    def zero_grad(self): self.grad = np.zeros_like(self.data)
    def backward(self):
        if self.data.size != 1: raise ValueError('backward() needs a tensor of size 1')
        order, seen, stack = [], set(), [(self, False)]
        while stack:
            node, done = stack.pop()
            if done: order.append(node); continue
            if id(node) in seen: continue
            seen.add(id(node)); stack.append((node, True))
            for p in node._prev:
                if id(p) not in seen: stack.append((p, False))
        self.grad = np.ones_like(self.data)
        for node in reversed(order): node._backward()

def softmax(x, axis=-1):
    z = np.exp(x - x.max(axis=axis, keepdims=True)); return z / z.sum(axis=axis, keepdims=True)

def cross_entropy(logits, targets):
    y = np.asarray(targets, dtype=int); z = logits.data; n = z.shape[0]
    m = z.max(axis=1, keepdims=True); lse = np.log(np.exp(z - m).sum(axis=1)) + m[:, 0]
    out = Tensor((lse - z[np.arange(n), y]).mean(), (logits,), 'ce')
    def b():
        p = softmax(z, axis=1); p[np.arange(n), y] -= 1; logits.grad = logits.grad + p / n * out.grad
    out._backward = b; return out

def concat(tensors, axis=0):
    out = Tensor(np.concatenate([t.data for t in tensors], axis=axis), tuple(tensors), 'concat')
    def b():
        cuts = np.cumsum([t.shape[axis] for t in tensors])[:-1]
        for t, g in zip(tensors, np.split(out.grad, cuts, axis=axis)): t.grad = t.grad + g
    out._backward = b; return out

def sgd_step(params, lr):
    for p in params: p.data -= lr * p.grad

def grad_check(f, params, h=1e-5):
    for p in params: p.zero_grad()
    f().backward(); an = [p.grad.copy() for p in params]; nu = []
    for p in params:
        g = np.zeros_like(p.data)
        for i in np.ndindex(p.data.shape):
            old = p.data[i]; p.data[i] = old + h; fp = f().item(); p.data[i] = old - h; fm = f().item(); p.data[i] = old
            g[i] = (fp - fm) / (2 * h)
        nu.append(g)
    diff = max(np.abs(a - b).max() for a, b in zip(an, nu))
    scale = max(max(np.abs(a).max() for a in an), max(np.abs(b).max() for b in nu), 1e-12)
    return diff / scale

if __name__ == '__main__':
    import random
    rng = np.random.default_rng(3)
    A = Tensor(rng.standard_normal((3, 4))); B = Tensor(rng.standard_normal((4, 2))); bias = Tensor(rng.standard_normal(2))
    print('matmul + broadcast + tanh + mean:', f"{grad_check(lambda: ((A @ B + bias).tanh() ** 2).mean(), [A, B, bias]):.1e}")
    X = Tensor(rng.standard_normal((5, 3))); c = Tensor(rng.standard_normal((5, 1)))
    print('column broadcast, -, /, exp, log:', f"{grad_check(lambda: ((X - c) / (c * c + 1.0)).exp().sum(axis=1).log().mean(), [X, c]):.1e}")
    C = Tensor(rng.standard_normal((27, 4))); idx = np.array([[1, 2, 1], [0, 1, 26]]); W = Tensor(rng.standard_normal((12, 27))); y = np.array([3, 1])
    print('index with repeats + reshape + cross_entropy:', f"{grad_check(lambda: cross_entropy(C[idx].reshape(2, 12) @ W, y), [C, W]):.1e}")
    P = Tensor(rng.standard_normal((2, 3))); Q = Tensor(rng.standard_normal((2, 2)))
    print('concat + relu + T + reused tensor:', f"{grad_check(lambda: (concat([P, Q], axis=1).relu().T @ P).sum() + (P * P).sum(), [P, Q]):.1e}")
    v = Tensor(np.array([0.5])); out = v
    for _ in range(2000): out = (out * 0.999).tanh() + 0.001
    out.sum().backward(); print('2000-node chain backward without recursion: grad', float(v.grad[0]) != 0.0)
    try:
        Tensor(np.ones(2)).backward(); print('FAIL: size check')
    except ValueError: print('size-1 check raises ValueError: ok')
    # the backprop L3 course network rebuilt with Tensor: loss at step 0 must be 5.556800
    r = random.Random(42); sizes = [2, 3, 1]; Ws, bs = [], []
    for nin, nout in zip(sizes, sizes[1:]):
        rows = [([r.uniform(-1, 1) for _ in range(nin)], r.uniform(-1, 1)) for _ in range(nout)]
        Ws.append(Tensor(np.array([w for w, _ in rows]).T)); bs.append(Tensor(np.array([b for _, b in rows])))
    Xd = np.array([[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]]); Yd = np.array([[1.0], [1.0], [-1.0], [-1.0]])
    def loss():
        a = Tensor(Xd)
        for Wl, bl in zip(Ws, bs): a = (a @ Wl + bl).tanh()
        return ((a - Yd) ** 2).sum()
    print('course 2-3-1 net, loss at step 0:', round(loss().item(), 6), 'grad check', f"{grad_check(loss, Ws + bs):.1e}")
    for k in range(200):
        for p in Ws + bs: p.zero_grad()
        L = loss(); L.backward(); sgd_step(Ws + bs, 0.05)
    print('after 200 steps at 0.05:', round(loss().item(), 6))
    print('float32 tanh layer check, h=1e-3 (expected to fail 1e-6):', end=' ')
    X32 = rng.standard_normal((4, 3)).astype(np.float32); W32 = rng.standard_normal((3, 2)).astype(np.float32)
    an = (X32.T @ (1 - np.tanh(X32 @ W32) ** 2)); h = np.float32(1e-3); nm = np.zeros_like(W32)
    for i in range(3):
        for j in range(2):
            Wp = W32.copy(); Wp[i, j] += h; Wm = W32.copy(); Wm[i, j] -= h; nm[i, j] = (np.tanh(X32 @ Wp).sum() - np.tanh(X32 @ Wm).sum()) / (2 * h)
    print(f'{float(np.abs(nm - an).max() / np.abs(an).max()):.1e}')
