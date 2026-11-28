"""representations level 4: data, schedules and a small noise predictor for the diffusion lessons.

two_rings(n, seed=0, radii=(0.8, 1.6), noise=0.03) -> X, shape (n, 2)
    Even rows on the inner ring, odd rows on the outer. g = default_rng(seed); angles g.uniform(0, 2 pi, n), then
    noise * g.standard_normal((n, 2)) added. The per-coordinate variance is about 0.8, close to 1.
linear_schedule(T=50, b1=1e-3, bT=0.2) -> betas, np.linspace(b1, bT, T); beta_t is betas[t - 1].
init_denoiser(hidden=64, seed=0) -> [W1, w1t, b1, W2, b2, W3, b3]
    g = default_rng(seed); W1 (2, hidden) and w1t (1, hidden) from g.standard_normal / sqrt(3), W2 (hidden, hidden)
    from g.standard_normal / sqrt(hidden), W3 (hidden, 2) likewise; biases zero.
eps_model(params, X, t, T) -> the predicted noise, shape (n, 2)
    h = relu(X W1 + (t / T) w1t + b1); h = relu(h W2 + b2); out = h W3 + b3. t is a whole number or an array of
    n whole numbers from 1 to T. Accepts NumPy arrays or autograd Tensors for the weights.
NumPy only; no state is kept between calls.
"""
import numpy as np

__version__ = "1.0"


def two_rings(n, seed=0, radii=(0.8, 1.6), noise=0.03):
    g = np.random.default_rng(seed)
    r = np.where(np.arange(n) % 2 == 0, radii[0], radii[1])
    th = g.uniform(0.0, 2 * np.pi, n)
    return np.stack([r * np.cos(th), r * np.sin(th)], axis=1) + noise * g.standard_normal((n, 2))


def linear_schedule(T=50, b1=1e-3, bT=0.2):
    return np.linspace(b1, bT, T)


def init_denoiser(hidden=64, seed=0):
    g = np.random.default_rng(seed)
    W1 = g.standard_normal((2, hidden)) / np.sqrt(3)
    w1t = g.standard_normal((1, hidden)) / np.sqrt(3)
    W2 = g.standard_normal((hidden, hidden)) / np.sqrt(hidden)
    W3 = g.standard_normal((hidden, 2)) / np.sqrt(hidden)
    return [W1, w1t, np.zeros(hidden), W2, np.zeros(hidden), W3, np.zeros(2)]


def _relu(a):
    return a.relu() if hasattr(a, 'relu') else np.maximum(a, 0.0)


def eps_model(params, X, t, T):
    W1, w1t, b1, W2, b2, W3, b3 = params
    X = X if hasattr(X, 'relu') else np.asarray(X, dtype=float)
    n = X.shape[0]
    u = (np.broadcast_to(np.asarray(t, dtype=float), (n,)) / T)[:, None]
    h = _relu(X @ W1 + u * w1t + b1)
    h = _relu(h @ W2 + b2)
    return h @ W3 + b3
