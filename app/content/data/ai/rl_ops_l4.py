"""rl level 4 shared code (policy gradients), version 1.0. Frozen: later levels import it and never edit it.

The short corridor (Sutton and Barto, Example 13.1), the softmax policy and its score, and the toy execution
task of l16 with its dynamic-programming optimum and a small policy network built on autograd.py (frozen v1.0).
"""
import math

import numpy as np

from autograd import Tensor

__version__ = "1.0"

# ---- the short corridor: states 0 (S), 1 (actions reversed), 2, and 3 (G); reward -1 a step ----
GOAL = 3


def corridor_move(s, right):
    """Next state from s; right is True for the move "right". State 1 swaps the two moves; S's left wall holds."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return GOAL if right else 1


def corridor_value(p):
    """J(p) = (2p - 4) / (p (1 - p)), the expected return from S when every state moves right with chance p."""
    return (2 * p - 4) / (p * (1 - p))


def corridor_episode(p, rng, max_steps=100000):
    """One episode from S: a list of 1 (right) and 0 (left), one rng.random() a step, right when it is below p."""
    s, acts = 0, []
    while s != GOAL and len(acts) < max_steps:
        right = rng.random() < p
        acts.append(1 if right else 0)
        s = corridor_move(s, right)
    return acts


# ---- the softmax policy ----
def softmax(theta):
    """Chances from dials, the largest dial subtracted first so a dial of 1000 does not overflow."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]


def grad_log_softmax(theta, a):
    """The score: d log pi(a) / d theta_b = [b == a] - pi_b."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]


def sample(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1


# ---- the execution task of l16: sell 4 lots in 5 steps, 0, 1 or 2 lots a step ----
LOTS, STEPS, HOLD, DUMP = 4, 5, 0.5, 5.0
ACTIONS = (0, 1, 2)


def proceeds(k):
    """Selling k lots at once fills at 10 - k each: impact grows with the lots sold together."""
    return k * (10 - k)


def exec_step(lots, steps, k):
    """Sell min(k, lots). Each lot still held costs HOLD; after the last step what is left is dumped at DUMP a lot.
    Returns (lots left, steps left, reward, done)."""
    k = min(k, lots)
    lots2, steps2 = lots - k, steps - 1
    r = proceeds(k) - HOLD * lots2
    if steps2 == 0:
        r += DUMP * lots2
        lots2 = 0
    return lots2, steps2, r, steps2 == 0


def exec_dp():
    """Backward induction from the last step. Returns (best value from (LOTS, STEPS), best schedule as a list)."""
    V, best = {}, {}
    for s in range(STEPS + 1):
        for l in range(LOTS + 1):
            if s == 0:
                V[l, s] = 0.0
                continue
            outs = []
            for k in ACTIONS:
                l2, s2, r, _ = exec_step(l, s, k)
                outs.append((r + V[l2, s2], -k, k))
            v, _, k = max(outs)
            V[l, s], best[l, s] = v, k
    plan, l = [], LOTS
    for s in range(STEPS, 0, -1):
        k = min(best[l, s], l)
        plan.append(k)
        l -= k
    return V[LOTS, STEPS], plan


def features(lots, steps):
    """The state vector the network reads: lots left / 4, steps left / 5, and a constant 1."""
    return np.array([lots / LOTS, steps / STEPS, 1.0])


def policy_value(probs):
    """Exact expected proceeds from (LOTS, STEPS) of a stochastic policy; probs(lots, steps) returns 3 chances."""
    memo = {}

    def v(l, s):
        if s == 0:
            return 0.0
        if (l, s) not in memo:
            pr = probs(l, s)
            total = 0.0
            for k in ACTIONS:
                l2, s2, r, _ = exec_step(l, s, k)
                total += pr[k] * (r + v(l2, s2))
            memo[l, s] = total
        return memo[l, s]

    return v(LOTS, STEPS)


# ---- a small policy network on autograd.py ----
def log_softmax(z):
    """Differentiable log-softmax over the last axis of a Tensor; the row maximum is a constant."""
    m = Tensor(z.data.max(axis=-1, keepdims=True))
    zs = z - m
    return zs - zs.exp().sum(axis=-1, keepdims=True).log()


def init_policy(seed, hidden=8):
    """[W1 (3, hidden), b1, W2 (hidden, 3), b2], weights from np.random.default_rng(seed) with sd 0.5, biases 0."""
    rng = np.random.default_rng(seed)
    return [Tensor(rng.normal(0, 0.5, (3, hidden))), Tensor(np.zeros(hidden)),
            Tensor(rng.normal(0, 0.5, (hidden, 3))), Tensor(np.zeros(3))]


def policy_logits(params, X):
    """Logits as a Tensor in the graph: tanh(X W1 + b1) W2 + b2, for rows X of features."""
    W1, b1, W2, b2 = params
    return ((Tensor(X) @ W1 + b1).tanh()) @ W2 + b2


def policy_probs(params, X):
    """Chances as a plain array, no graph (for acting)."""
    W1, b1, W2, b2 = (p.data for p in params)
    z = np.tanh(np.asarray(X, dtype=float) @ W1 + b1) @ W2 + b2
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def run_batch(params, batch, rng):
    """Play `batch` episodes side by side with the network's chances; rng is np.random.default_rng.
    Returns X (batch*STEPS, 3), actions (batch*STEPS,), returns-to-go G (batch, STEPS), totals (batch,).
    Rows are ordered episode by episode."""
    lots = np.full(batch, LOTS)
    X = np.zeros((batch, STEPS, 3))
    A = np.zeros((batch, STEPS), dtype=int)
    R = np.zeros((batch, STEPS))
    for t in range(STEPS):
        Xt = np.stack([features(l, STEPS - t) for l in lots])
        pr = policy_probs(params, Xt)
        a = (rng.random(batch)[:, None] > pr.cumsum(axis=1)).sum(axis=1).clip(0, 2)
        for i in range(batch):
            lots[i], _, R[i, t], _ = exec_step(int(lots[i]), STEPS - t, int(a[i]))
        X[:, t], A[:, t] = Xt, a
    G = R[:, ::-1].cumsum(axis=1)[:, ::-1]
    return X.reshape(-1, 3), A.reshape(-1), G, R.sum(axis=1)


def network_value(params):
    """policy_value of the network's own chances."""
    return policy_value(lambda l, s: policy_probs(params, features(l, s)[None])[0])
