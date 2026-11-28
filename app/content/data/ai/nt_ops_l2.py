"""nn-train level 2 ops: the sigmoid, initialisation scales, batch normalisation and layer normalisation, for autograd.py (v1.0).

Each op takes and returns autograd Tensors (plain arrays are wrapped as constants) and adds its gradient into its inputs
with a backward checked against central differences in float64 (docs/reports/nn-train-L2-numbers.py).
    sigmoid(x)                                   1 / (1 + e^-x), elementwise, stable for large |x|
    lecun_sd(fan_in), he_sd(fan_in)              1/sqrt(fan_in) and sqrt(2/fan_in)
    init_layer(fan_in, fan_out, act="tanh", seed=0)          (W, b): W ~ N(0, sd^2) with he_sd for "relu", lecun_sd otherwise; b = 0
    batchnorm(x, gamma, beta, eps=1e-5, mode="train", running=None, momentum=0.1)
        x (N, D). "train": each column normalised by its batch mean and variance (divided by N), then gamma * xhat + beta;
        returns (out, running) with running = (mean, var) moved a share `momentum` towards the batch's (from (0, 1) when None).
        "eval": uses `running` instead of the batch and leaves it unchanged.
    layernorm(x, gamma, beta, eps=1e-5)          each row (the last axis) normalised by its own mean and variance; any leading shape
Shipped verbatim beside autograd.py: from nt_ops_l2 import sigmoid, he_sd, lecun_sd, init_layer, batchnorm, layernorm.
"""
__version__ = "1.0"

import math

import numpy as np
from autograd import Tensor


def _t(x):
    return x if isinstance(x, Tensor) else Tensor(x)


def sigmoid(x):
    x = _t(x)
    s = np.where(x.data >= 0, 1 / (1 + np.exp(-np.abs(x.data))), np.exp(-np.abs(x.data)) / (1 + np.exp(-np.abs(x.data))))
    out = Tensor(s, (x,), "sigmoid")

    def _backward():
        x.grad += out.grad * s * (1 - s)
    out._backward = _backward
    return out


def lecun_sd(fan_in):
    return 1 / math.sqrt(fan_in)


def he_sd(fan_in):
    return math.sqrt(2 / fan_in)


def init_layer(fan_in, fan_out, act="tanh", seed=0):
    sd = he_sd(fan_in) if act == "relu" else lecun_sd(fan_in)
    W = np.random.default_rng(seed).standard_normal((fan_in, fan_out)) * sd
    return W, np.zeros(fan_out)


def batchnorm(x, gamma, beta, eps=1e-5, mode="train", running=None, momentum=0.1):
    x, gamma, beta = _t(x), _t(gamma), _t(beta)
    n = x.data.shape[0]
    rm, rv = (np.zeros(x.data.shape[1]), np.ones(x.data.shape[1])) if running is None else (np.asarray(running[0], dtype=float), np.asarray(running[1], dtype=float))
    if mode == "train":
        mu = x.data.mean(axis=0)
        var = ((x.data - mu) ** 2).mean(axis=0)
        new_running = ((1 - momentum) * rm + momentum * mu, (1 - momentum) * rv + momentum * var)
    elif mode == "eval":
        mu, var, new_running = rm, rv, (rm, rv)
    else:
        raise ValueError(f"mode must be 'train' or 'eval', not {mode!r}")
    inv = 1 / np.sqrt(var + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "batchnorm")

    def _backward():
        g = out.grad
        gamma.grad += (g * xhat).sum(axis=0)
        beta.grad += g.sum(axis=0)
        dxhat = g * gamma.data
        if mode == "train":
            x.grad += inv / n * (n * dxhat - dxhat.sum(axis=0) - xhat * (dxhat * xhat).sum(axis=0))
        else:
            x.grad += dxhat * inv
    out._backward = _backward
    return out, new_running


def layernorm(x, gamma, beta, eps=1e-5):
    x, gamma, beta = _t(x), _t(gamma), _t(beta)
    d = x.data.shape[-1]
    mu = x.data.mean(axis=-1, keepdims=True)
    var = ((x.data - mu) ** 2).mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(var + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "layernorm")

    def _backward():
        g = out.grad
        lead = tuple(range(g.ndim - 1))
        gamma.grad += (g * xhat).sum(axis=lead) if lead else g * xhat
        beta.grad += g.sum(axis=lead) if lead else g
        dxhat = g * gamma.data
        x.grad += inv / d * (d * dxhat - dxhat.sum(axis=-1, keepdims=True) - xhat * (dxhat * xhat).sum(axis=-1, keepdims=True))
    out._backward = _backward
    return out
