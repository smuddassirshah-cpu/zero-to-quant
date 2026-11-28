"""nn-train level 4 ops: the course's experiment set-up (a fixed data split, three seed streams, one training run) and
Student's t distribution without SciPy, for autograd.py (v1.0), nt_ops_l1.py, nt_ops_l2.py and nt_ops_l3.py.

    course_data(split_seed=0)          (X, y, tr, va, te): spirals(600, seed=0) from nt_ops_l1; the rows are split
                                       400 / 100 / 100 by np.random.default_rng(split_seed).permutation(600)
    seed_streams(seed)                 (init_rng, batch_rng, dropout_rng): three independent generators,
                                       [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(3)]
    init_params(rng, hidden=16, ln=False)
        [W1, b1, W2, b2, W3, b3] for the 2-h-h-2 net, W (fan_in, fan_out) ~ N(0, 1/fan_in) drawn in that order, b = 0;
        with ln, [g1, c1, g2, c2] (ones and zeros) are appended for the two layer norms
    net_logits(params, X, ln=False, p=0.0, rng=None)
        logits as a Tensor: X @ W + b, then layernorm (when ln), tanh, then dropout (when p > 0 and rng is given) on each
        hidden layer; with rng None nothing is dropped (evaluation)
    train_run(config, seed, split_seed=0, steps=300, batch=32, every=6, batch_seed=None)
        one run of `config` (keys opt "sgd" or "adam", lr, ln, p, hidden) from seed_streams(seed); each step draws
        batch_rng.choice(400, batch, replace=False) training rows; returns dict(val, test, train, val_curve,
        train_curve) with losses in nats, the curves every `every` steps; batch_seed, when given, takes the batch
        stream from seed_streams(batch_seed) instead (a seed that does not fix the batch order)
    t_cdf(x, df), t_quantile(q, df)    Student's t with df degrees of freedom, by the regularised incomplete beta
                                       (continued fraction) and bisection; agree with scipy.stats.t to about 1e-12
Shipped verbatim beside autograd.py and nt_ops_l1 to l3: from nt_ops_l4 import seed_streams, train_run, t_quantile.
"""
__version__ = "1.0"

import math

import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import spirals, sgd_step, adam_step
from nt_ops_l2 import layernorm
from nt_ops_l3 import dropout


def course_data(split_seed=0):
    X, y = spirals(600, seed=0, noise=0.05)
    order = np.random.default_rng(split_seed).permutation(600)
    return X, y, order[:400], order[400:500], order[500:]


def seed_streams(seed):
    return tuple(np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(3))


def init_params(rng, hidden=16, ln=False):
    params = []
    for a, b in ((2, hidden), (hidden, hidden), (hidden, 2)):
        params += [rng.standard_normal((a, b)) / math.sqrt(a), np.zeros(b)]
    if ln:
        params += [np.ones(hidden), np.zeros(hidden), np.ones(hidden), np.zeros(hidden)]
    return params


def net_logits(params, X, ln=False, p=0.0, rng=None):
    ts = [q if isinstance(q, Tensor) else Tensor(q) for q in params]
    h = X if isinstance(X, Tensor) else Tensor(X)
    for i in range(3):
        h = h @ ts[2 * i] + ts[2 * i + 1]
        if i < 2:
            if ln:
                h = layernorm(h, ts[6 + 2 * i], ts[7 + 2 * i])
            h = h.tanh()
            if p > 0 and rng is not None:
                h, _ = dropout(h, p, rng=rng)
    return h


def _loss(params, X, y, ln):
    return cross_entropy(net_logits(params, X, ln), y).item()


def train_run(config, seed, split_seed=0, steps=300, batch=32, every=6, batch_seed=None):
    X, y, tr, va, te = course_data(split_seed)
    ln, p, opt, lr = bool(config.get("ln")), float(config.get("p", 0.0)), config["opt"], config["lr"]
    init_rng, batch_rng, drop_rng = seed_streams(seed)
    if batch_seed is not None:
        batch_rng = seed_streams(batch_seed)[1]
    params = init_params(init_rng, config.get("hidden", 16), ln)
    m = [np.zeros_like(q) for q in params]
    v = [np.zeros_like(q) for q in params]
    val_curve, train_curve = [], []
    for t in range(1, steps + 1):
        rows = tr[batch_rng.choice(len(tr), batch, replace=False)]
        ts = [Tensor(q) for q in params]
        loss = cross_entropy(net_logits(ts, X[rows], ln, p, drop_rng), y[rows])
        loss.backward()
        grads = [q.grad for q in ts]
        if opt == "adam":
            params, m, v = adam_step(params, grads, m, v, t, lr)
        else:
            params = sgd_step(params, grads, lr)
        if every and t % every == 0:
            val_curve.append(_loss(params, X[va], y[va], ln))
            train_curve.append(_loss(params, X[tr], y[tr], ln))
    return {"val": _loss(params, X[va], y[va], ln), "test": _loss(params, X[te], y[te], ln),
            "train": _loss(params, X[tr], y[tr], ln), "val_curve": val_curve, "train_curve": train_curve}


def _betacf(a, b, x):
    tiny = 1e-300
    c, d = 1.0, 1.0 - (a + b) * x / (a + 1.0)
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for k in range(1, 500):
        for num in (k * (b - k) * x / ((a + 2 * k - 1) * (a + 2 * k)),
                    -(a + k) * (a + b + k) * x / ((a + 2 * k) * (a + 2 * k + 1))):
            d = 1.0 + num * d
            d = 1.0 / (d if abs(d) > tiny else tiny)
            c = 1.0 + num / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
        if abs(d * c - 1.0) < 1e-16:
            break
    return h


def _betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lead = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return lead * _betacf(a, b, x) / a
    return 1.0 - lead * _betacf(b, a, 1.0 - x) / b


def t_cdf(x, df):
    if x * x < df:
        half = 0.5 * _betainc(0.5, df / 2.0, x * x / (df + x * x))
        return 0.5 + half if x >= 0 else 0.5 - half
    tail = 0.5 * _betainc(df / 2.0, 0.5, df / (df + x * x))
    return 1.0 - tail if x >= 0 else tail


def t_quantile(q, df):
    if not 0 < q < 1:
        raise ValueError("q must be in (0, 1)")
    lo, hi = -1e4, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13 * max(1.0, abs(mid)):
            break
    return 0.5 * (lo + hi)
