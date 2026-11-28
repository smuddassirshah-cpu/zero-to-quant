"""representations level 5 ops: planted-partition graphs, the normalised adjacency and a small graph network.

Built on the frozen autograd.py (v1.0) and nt_ops_l1.adam_step. A graph is a symmetric 0/1 NumPy array A with a zero
diagonal; a dense adjacency product is a matmul, so no new autograd op is needed.
    planted_partition(n, p_in, p_out, seed)   (A, y): nodes 0 to n//2 - 1 in community 0, the rest in 1; each pair i < j
                                               linked when a uniform draw from default_rng(seed) (one n-by-n table) is
                                               below p_in (same community) or p_out (different)
    node_features(y, shift=0.6, seed=0)       X (n, 2): standard normal noise from default_rng(seed), the first column
                                               moved by -shift for community 0 and +shift for community 1
    normalised_adjacency(A)                   D~^(-1/2) (A + I) D~^(-1/2), where D~ holds the degrees of A + I
    gcn_init(sizes, seed=0)                   one weight matrix a layer, N(0, 1/fan_in) from default_rng(seed); no biases
    gcn_logits(A_hat, X, params)              A_hat X W1, ReLU, A_hat H W2, ... (no ReLU after the last); a Tensor
    train_gcn_params(A_hat, X, y, train_idx, layers=2, hidden=16, steps=200, lr=0.05, seed=0)
                                               full-batch Adam on the mean cross-entropy of the training nodes only;
                                               returns (params, losses), the losses before each step
    predict(A_hat, X, params)                 the arg-max class of every node, an integer array
Every function returns new arrays and leaves its inputs unchanged.
"""
__version__ = "1.0"

import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def planted_partition(n, p_in, p_out, seed):
    g = np.random.default_rng(seed)
    y = (np.arange(n) >= n // 2).astype(int)
    U = g.random((n, n))
    P = np.where(y[:, None] == y[None, :], p_in, p_out)
    A = np.triu((U < P).astype(float), 1)
    return A + A.T, y


def node_features(y, shift=0.6, seed=0):
    y = np.asarray(y)
    X = np.random.default_rng(seed).standard_normal((len(y), 2))
    X[:, 0] += shift * (2 * y - 1)
    return X


def normalised_adjacency(A):
    At = np.asarray(A, dtype=float) + np.eye(len(A))
    s = 1.0 / np.sqrt(At.sum(axis=1))
    return s[:, None] * At * s[None, :]


def gcn_init(sizes, seed=0):
    g = np.random.default_rng(seed)
    return [g.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]


def gcn_logits(A_hat, X, params):
    A_hat = np.asarray(A_hat, dtype=float)
    h = X if isinstance(X, Tensor) else Tensor(X)
    for k, W in enumerate(params):
        h = A_hat @ (h @ W)
        if k < len(params) - 1:
            h = h.relu()
    return h


def train_gcn_params(A_hat, X, y, train_idx, layers=2, hidden=16, steps=200, lr=0.05, seed=0):
    y = np.asarray(y, dtype=np.int64)
    tr = np.asarray(train_idx)
    X = np.asarray(X, dtype=float)
    sizes = [X.shape[1]] + [hidden] * (layers - 1) + [int(y.max()) + 1]
    W = gcn_init(sizes, seed)
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        loss = cross_entropy(gcn_logits(A_hat, X, P)[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    return W, losses


def predict(A_hat, X, params):
    return gcn_logits(A_hat, X, params).data.argmax(axis=1)
