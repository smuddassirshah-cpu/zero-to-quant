"""backprop L3: a scalar Value MLP (method A) against a NumPy hand-gradient MLP (method B), same init."""
import math, random, time
import numpy as np

class Value:
    def __init__(self, data, children=(), op=''):
        self.data = data; self.grad = 0.0; self._back = lambda: None; self._prev = set(children); self._op = op
    def __add__(self, o):
        o = o if isinstance(o, Value) else Value(o); out = Value(self.data + o.data, (self, o), '+')
        def b(): self.grad += out.grad; o.grad += out.grad
        out._back = b; return out
    __radd__ = __add__
    def __mul__(self, o):
        o = o if isinstance(o, Value) else Value(o); out = Value(self.data * o.data, (self, o), '*')
        def b(): self.grad += o.data * out.grad; o.grad += self.data * out.grad
        out._back = b; return out
    __rmul__ = __mul__
    def __neg__(self): return self * -1
    def __sub__(self, o): return self + (-o)
    def __pow__(self, k):
        out = Value(self.data ** k, (self,), f'**{k}')
        def b(): self.grad += k * self.data ** (k - 1) * out.grad
        out._back = b; return out
    def tanh(self):
        t = math.tanh(self.data); out = Value(t, (self,), 'tanh')
        def b(): self.grad += (1 - t * t) * out.grad
        out._back = b; return out
    def backward(self):
        topo, seen = [], set()
        def build(v):
            if v not in seen:
                seen.add(v)
                for c in v._prev: build(c)
                topo.append(v)
        build(self); self.grad = 1.0
        for v in reversed(topo): v._back()

def init_params(sizes, seed):
    r = random.Random(seed); layers = []
    for nin, nout in zip(sizes, sizes[1:]):
        layers.append([([r.uniform(-1, 1) for _ in range(nin)], r.uniform(-1, 1)) for _ in range(nout)])
    return layers

X = [[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]]; Y = [1.0, 1.0, -1.0, -1.0]
sizes = [2, 3, 1]; raw = init_params(sizes, 42)

def run_value(steps, lr):
    layers = [[([Value(w) for w in ws], Value(b)) for ws, b in L] for L in raw]
    params = [p for L in layers for ws, b in L for p in ws + [b]]
    losses = []
    for k in range(steps + 1):
        loss = Value(0.0)
        for x, y in zip(X, Y):
            a = [Value(v) for v in x]
            for li, L in enumerate(layers):
                a = [(sum((w * ai for w, ai in zip(ws, a)), b)).tanh() for ws, b in L]
            loss = loss + (a[0] - y) ** 2
        losses.append(loss.data)
        if k == steps: break
        for p in params: p.grad = 0.0
        loss.backward()
        if k == 0: g0 = [p.grad for p in params]
        for p in params: p.data -= lr * p.grad
    return losses, g0, [p.data for p in params]

def run_numpy(steps, lr):
    W = [np.array([ws for ws, b in L]) for L in raw]; B = [np.array([b for ws, b in L]) for L in raw]
    Xa = np.array(X); Ya = np.array(Y); losses = []
    for k in range(steps + 1):
        acts = [Xa]
        for Wl, bl in zip(W, B): acts.append(np.tanh(acts[-1] @ Wl.T + bl))
        out = acts[-1][:, 0]; loss = ((out - Ya) ** 2).sum(); losses.append(loss)
        if k == steps: break
        d = (2 * (out - Ya))[:, None]; gW = [None] * len(W); gB = [None] * len(W)
        for l in range(len(W) - 1, -1, -1):
            dz = d * (1 - acts[l + 1] ** 2); gW[l] = dz.T @ acts[l]; gB[l] = dz.sum(0); d = dz @ W[l]
        if k == 0: g0 = [g for l in range(len(W)) for i in range(W[l].shape[0]) for g in list(gW[l][i]) + [gB[l][i]]]
        for l in range(len(W)): W[l] -= lr * gW[l]; B[l] -= lr * gB[l]
    return losses, g0

t0 = time.time(); la, ga, pa = run_value(200, 0.05); ta = time.time() - t0
lb, gb = run_numpy(200, 0.05)
print('params', len(pa), f'Value run 200 steps {ta:.3f} s native')
for k in (0, 1, 10, 50, 100, 200):
    print(f'  step {k}: Value {la[k]:.6f} numpy {lb[k]:.6f}'); assert abs(la[k] - lb[k]) < 1e-9
print('max |grad diff| at step 0:', max(abs(a - b) for a, b in zip(ga, gb)))
print('first-step gradients (Value):', [round(g, 6) for g in ga])
# gradient check by central differences on the Value net at the initial point
def loss_at(flat):
    it = iter(flat); layers = [[([next(it) for _ in ws], next(it)) for ws, b in L] for L in raw]
    s = 0.0
    for x, y in zip(X, Y):
        a = x
        for L in layers: a = [math.tanh(sum(w * ai for w, ai in zip(ws, a)) + b) for ws, b in L]
        s += (a[0] - y) ** 2
    return s
flat0 = [p for L in raw for ws, b in L for p in ws + [b]]
for h in (1e-2, 1e-4, 1e-6):
    num = []
    for i in range(len(flat0)):
        fp = flat0.copy(); fp[i] += h; fm = flat0.copy(); fm[i] -= h; num.append((loss_at(fp) - loss_at(fm)) / (2 * h))
    rel = max(abs(a - b) / max(abs(a), abs(b), 1e-12) for a, b in zip(num, ga))
    print(f'  gradient check h={h:g}: max relative error {rel:.1e}')
# accuracy by sign
print('predictions after 200 steps:', end=' ')
it = iter(pa); layers = [[([next(it) for _ in ws], next(it)) for ws, b in L] for L in raw]
for x in X:
    a = x
    for L in layers: a = [math.tanh(sum(w * ai for w, ai in zip(ws, a)) + b) for ws, b in L]
    print(round(a[0], 4), end=' ')
print()
# a bad learning rate
for lr in (0.2, 0.5, 2.0):
    l2, _, _ = run_value(50, lr); print(f'lr {lr}: losses at 0, 10, 50:', round(l2[0], 4), round(l2[10], 4), round(l2[50], 4))
# Value expression from L1 through the class
a, b, c, f = Value(1.5), Value(-2.0), Value(4.0), Value(-3.0); L = (a * b + c) * f; L.backward()
print('L1 expression via Value:', L.data, a.grad, b.grad, c.grad, f.grad)
x, y = Value(2.0), Value(3.0); g = (x + y) * x; g.backward(); print('branch via Value:', g.data, x.grad, y.grad)
