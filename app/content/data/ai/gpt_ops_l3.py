"""gpt level 3 ops: training the tiny GPT with autograd.py (v1.0), seq_ops_l4.py and gpt_ops_l2.py.

Weights are gpt_ops_l2's dict of float64 arrays ("wte", "h0.qkv_w", ...). The forward pass with gradients is
seq_ops_l4.lm_logits on gpt_ops_l2.to_model of Tensors, so training and the plain NumPy forward pass agree.
    init_weights(seed, config=None, sd=0.02)       matrices N(0, sd^2) from default_rng(seed) in gpt_ops_l2.shapes order,
                                                   gains (names ending "_g") 1, other vectors 0
    get_batch(data, B, T, rng)                     (X, Y): B windows of T ids from rng.integers(0, len(data) - T, B), Y shifted by one
    loss_and_grads(weights, X, Y, n_head=4)        (mean cross-entropy in nats, {name: gradient array})
    adam_init(weights)                             {"t": 0, "m": {name: zeros}, "v": {name: zeros}}
    adam_update(weights, grads, state, lr)         new weights after one bias-corrected Adam step (nt_ops_l1.adam_step);
                                                   state["t"] goes up by one and its moments are replaced
    train(weights, data, steps, lr, B=16, T=32, seed=1, warmup=0, n_head=4)
                                                   Adam for `steps` steps on batches from default_rng(seed); with warmup > 0 the rate
                                                   follows nt_ops_l1.warmup_cosine(t, lr, warmup, steps). Returns (weights, losses)
    eval_loss(weights, data, T=32, n_head=4)       mean loss over the non-overlapping windows of T + 1 characters that fit in data
    bigram_loss(train_ids, val_ids, alpha=1.0, V=65)   add-alpha bigram counts from train_ids, mean -ln p on val_ids's pairs
Recomputed in docs/reports/gpt-L3-numbers.py. Frozen once merged: later levels and courses import it, never edit it.
"""
__version__ = "1.0"

import numpy as np

from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step, warmup_cosine
from seq_ops_l4 import lm_logits
import gpt_ops_l2 as G


def init_weights(seed, config=None, sd=0.02):
    """Small random weights for a model of `config` (gpt_ops_l2.CONFIG by default)."""
    g = np.random.default_rng(seed)
    w = {}
    for k, s in G.shapes(config or G.CONFIG):
        if k.endswith("_g"):
            w[k] = np.ones(s)
        elif len(s) == 1:
            w[k] = np.zeros(s)
        else:
            w[k] = g.standard_normal(s) * sd
    return w


def get_batch(data, B, T, rng):
    """B random windows of T ids and their targets, the same windows shifted by one."""
    data = np.asarray(data)
    ix = rng.integers(0, len(data) - T, B)
    X = np.stack([data[i:i + T] for i in ix])
    Y = np.stack([data[i + 1:i + T + 1] for i in ix])
    return X, Y


def loss_and_grads(weights, X, Y, n_head=4):
    """Mean cross-entropy of the next-character predictions and the gradient of every array."""
    P = {k: Tensor(v) for k, v in weights.items()}
    V = weights["head_w"].shape[1]
    loss = cross_entropy(lm_logits(np.asarray(X), G.to_model(P), n_head).reshape(-1, V), np.asarray(Y).reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in weights}


def adam_init(weights):
    return {"t": 0, "m": {k: np.zeros_like(v) for k, v in weights.items()}, "v": {k: np.zeros_like(v) for k, v in weights.items()}}


def adam_update(weights, grads, state, lr):
    """One Adam step on every array; updates `state` and returns the new weights."""
    names = list(weights)
    state["t"] += 1
    new, m, v = adam_step([weights[k] for k in names], [grads[k] for k in names], [state["m"][k] for k in names],
                          [state["v"][k] for k in names], state["t"], lr)
    state["m"] = dict(zip(names, m))
    state["v"] = dict(zip(names, v))
    return dict(zip(names, new))


def train(weights, data, steps, lr, B=16, T=32, seed=1, warmup=0, n_head=4):
    rng = np.random.default_rng(seed)
    state = adam_init(weights)
    losses = []
    for t in range(1, steps + 1):
        X, Y = get_batch(data, B, T, rng)
        loss, grads = loss_and_grads(weights, X, Y, n_head)
        rate = warmup_cosine(t, lr, warmup, steps) if warmup > 0 else lr
        weights = adam_update(weights, grads, state, rate)
        losses.append(loss)
    return weights, losses


def eval_loss(weights, data, T=32, n_head=4):
    data = np.asarray(data)
    n = (len(data) - 1) // T
    X = data[:n * T].reshape(n, T)
    Y = data[1:n * T + 1].reshape(n, T)
    return G.mean_loss(weights, X, Y, n_head)


def bigram_loss(train_ids, val_ids, alpha=1.0, V=65):
    C = np.zeros((V, V))
    np.add.at(C, (np.asarray(train_ids)[:-1], np.asarray(train_ids)[1:]), 1)
    P = (C + alpha) / (C + alpha).sum(1, keepdims=True)
    v = np.asarray(val_ids)
    return float(-np.log(P[v[:-1], v[1:]]).mean())
