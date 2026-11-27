"""makemore method B: the same runs written with one-hot matrix products instead of index lookups and np.add.at.
Prints the figures that mk.py prints, for comparison."""
import os, sys
# names.txt: argument 1, else the app copy (engine A3), else ./dl/names.txt. MD5 401b3c4cac9e28a586ed15e81256680d.
_HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = next(p for p in ([sys.argv[1]] if len(sys.argv) > 1 else []) + [os.path.join(_HERE, '..', '..', '..', 'app', 'content', 'data', 'makemore', 'names.txt'), 'dl/names.txt'] if os.path.exists(p))

import math, sys
import numpy as np
words = open(NAMES).read().splitlines()
chars = sorted(set(''.join(words))); stoi = {s: i + 1 for i, s in enumerate(chars)}; stoi['.'] = 0
rng = np.random.default_rng(42); perm = rng.permutation(len(words)); n1, n2 = int(0.8 * len(words)), int(0.9 * len(words))
tr = [words[i] for i in perm[:n1]]; dv = [words[i] for i in perm[n1:n2]]
def bigr(ws):
    xs, ys = [], []
    for w in ws:
        cs = [0] + [stoi[c] for c in w] + [0]
        xs += cs[:-1]; ys += cs[1:]
    return np.array(xs), np.array(ys)
# one-layer net, one-hot product form
xs, ys = bigr(tr[:500]); X1 = np.eye(27)[xs]; Y1 = np.eye(27)[ys]
W = np.random.default_rng(2147483647).standard_normal((27, 27)); losses = []
for k in range(101):
    z = X1 @ W; z -= z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
    losses.append(-(Y1 * np.log(p)).sum(1).mean())
    W -= 50.0 * X1.T @ ((p - Y1) / len(ys))
print('B one-layer net on 500 names: steps 0, 10, 50, 99, 100 ->', [round(losses[i], 4) for i in (0, 10, 50, 99, 100)])
# MLP, one-hot product form for the embedding
def build(ws):
    X, Y = [], []
    for w in ws:
        ctx = [0, 0, 0]
        for ch in w + '.':
            X.append(ctx); Y.append(stoi[ch]); ctx = ctx[1:] + [stoi[ch]]
    return np.array(X), np.array(Y)
Xtr, Ytr = build(tr); Xdv, Ydv = build(dv)
g = np.random.default_rng(0)
C = g.standard_normal((27, 10)); W1 = g.standard_normal((30, 100)) * (5 / 3) / math.sqrt(30); b1 = np.zeros(100)
W2 = g.standard_normal((100, 27)) * 0.01; b2 = np.zeros(27)
I = np.eye(27)
def loss_of(X, Y):
    E = np.concatenate([I[X[:, j]] @ C for j in range(3)], axis=1); h = np.tanh(E @ W1 + b1); z = h @ W2 + b2
    m = z.max(1, keepdims=True); lse = np.log(np.exp(z - m).sum(1)) + m[:, 0]
    return float((lse - z[np.arange(len(Y)), Y]).mean())
gb = np.random.default_rng(1); marks = {}
for k in range(1, 40001):
    ix = gb.integers(0, len(Xtr), 32); X, Y = Xtr[ix], Ytr[ix]; lr = 0.1 if k <= 30000 else 0.01
    oh = [I[X[:, j]] for j in range(3)]
    E = np.concatenate([o @ C for o in oh], axis=1); h = np.tanh(E @ W1 + b1); z = h @ W2 + b2
    p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); p[np.arange(32), Y] -= 1; dz = p / 32
    dW2 = h.T @ dz; db2 = dz.sum(0); dpre = (dz @ W2.T) * (1 - h ** 2); dW1 = E.T @ dpre; db1 = dpre.sum(0)
    dE = dpre @ W1.T; dC = sum(oh[j].T @ dE[:, 10 * j:10 * j + 10] for j in range(3))
    C -= lr * dC; W1 -= lr * dW1; b1 -= lr * db1; W2 -= lr * dW2; b2 -= lr * db2
    if k in (200, 1000, 3000, 10000, 20000, 30000, 40000):
        marks[k] = (round(loss_of(Xtr, Ytr), 4), round(loss_of(Xdv, Ydv), 4))
print('B MLP (train, dev) at steps', marks)
