"""representations level 2: seeded data and a small tanh autoencoder for the autoencoder lessons.

arc(n=200, noise=0.05, seed=0, full=False) -> X, shape (n, 2)
    g = default_rng(seed); angles t = g.uniform(0, pi, n) (0 to 2 pi when full=True); then
    X = (cos t, sin t) + noise * g.standard_normal((n, 2)). Points along a half circle (or a full one) of radius 1.
init_tanh_ae(d, hidden, k, seed) -> list of 8 arrays [W1, b1, W2, b2, W3, b3, W4, b4]
    Encoder d -> hidden (tanh) -> k, decoder k -> hidden (tanh) -> d. g = default_rng(seed); the four weight
    matrices, in that order, are g.standard_normal((fan_in, fan_out)) / sqrt(fan_in); the biases are zeros.
tanh_ae_encode(params, X) -> Z = tanh(X W1 + b1) W2 + b2, the codes (n, k)
tanh_ae_forward(params, X) -> X_hat = tanh(Z W3 + b3) W4 + b4
    Both accept NumPy arrays or autograd Tensors (the tanh is the Tensor's own when it has one).
odd_day_panel(seed=3, regime=False) -> (R, kind)
    750 days by 10 stocks of daily returns in per cent. Stocks 0 to 4 form sector A, 5 to 9 sector B.
    A normal day: market move m ~ N(0, 1) times a loading in U(0.8, 1.2), plus the stock's sector move
    (sd 0.7) times a loading in U(0.8, 1.2), plus noise of sd 0.3. Days 0 to 499 train, 500 to 599 validate,
    600 to 749 test. Planted on test days: 8 odd days (kind 1), when each stock moves on its own (sd 1.5, no
    market or sector move), and one market-wide fall (kind 2, day 700), when the market move is -6.
    regime=True: from day 650 the two sectors swap their sector moves for stocks 0, 1, 5 and 6 (a lasting change).
    kind[d] is 0 for every other day. The first 650 days do not depend on `regime`.
NumPy only; no state is kept between calls.
"""
import numpy as np

__version__ = "1.0"

ODD_DAYS = (606, 619, 633, 648, 671, 688, 714, 737)
FALL_DAY = 700


def arc(n=200, noise=0.05, seed=0, full=False):
    g = np.random.default_rng(seed)
    t = g.uniform(0.0, 2 * np.pi if full else np.pi, n)
    return np.stack([np.cos(t), np.sin(t)], axis=1) + noise * g.standard_normal((n, 2))


def init_tanh_ae(d, hidden, k, seed):
    g = np.random.default_rng(seed)
    out = []
    for fi, fo in ((d, hidden), (hidden, k), (k, hidden), (hidden, d)):
        out.append(g.standard_normal((fi, fo)) / np.sqrt(fi))
        out.append(np.zeros(fo))
    return out


def _tanh(a):
    return a.tanh() if hasattr(a, 'tanh') else np.tanh(a)


def tanh_ae_encode(params, X):
    W1, b1, W2, b2 = params[:4]
    return _tanh(X @ W1 + b1) @ W2 + b2


def tanh_ae_forward(params, X):
    W3, b3, W4, b4 = params[4:]
    return _tanh(tanh_ae_encode(params, X) @ W3 + b3) @ W4 + b4


def odd_day_panel(seed=3, regime=False):
    g = np.random.default_rng(seed)
    days, n = 750, 10
    lm = g.uniform(0.8, 1.2, n)
    ls = g.uniform(0.8, 1.2, n)
    sector = np.array([0] * 5 + [1] * 5)
    m = g.standard_normal(days)
    s = 0.7 * g.standard_normal((days, 2))
    eps = 0.3 * g.standard_normal((days, n))
    own = 1.5 * g.standard_normal((days, n))
    kind = np.zeros(days, dtype=int)
    m[FALL_DAY] = -6.0
    kind[FALL_DAY] = 2
    sec = np.tile(sector, (days, 1))
    if regime:
        swap = np.array([0, 1, 5, 6])
        sec[650:, swap] = 1 - sec[650:, swap]
    R = m[:, None] * lm[None, :] + np.take_along_axis(s, sec, axis=1) * ls[None, :] + eps
    for d in ODD_DAYS:
        R[d] = own[d]
        kind[d] = 1
    return R, kind
