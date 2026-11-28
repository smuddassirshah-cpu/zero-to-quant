"""representations level 3: data and a small variational autoencoder for the VAE lessons.

circle_model(n, s=0.05, seed=0) -> (X, z)
    The latent variable model of l9: g = default_rng(seed); z = g.standard_normal(n); then
    X = g_circle(z) + s * g.standard_normal((n, 2)). One hidden number per point, mapped onto the unit circle.
g_circle(z) -> array (n, 2): the points (sin z, cos z), so z is the angle from the top of the circle.
init_vae(d=2, hidden=32, k=1, seed=0) -> [We, be, Wm, bm, Wv, bv, Wd, bd, Wo, bo]
    g = default_rng(seed); weight tables in that order, each g.standard_normal((fan_in, fan_out)) / sqrt(fan_in),
    shapes (d, hidden), (hidden, k), (hidden, k), (k, hidden), (hidden, d); biases zero.
vae_encode(params, X) -> (mu, logvar): h = tanh(X We + be); mu = h Wm + bm; logvar = h Wv + bv.
vae_decode(params, Z) -> X_hat = tanh(Z Wd + bd) Wo + bo, the decoder's mean.
    Both accept NumPy arrays or autograd Tensors.
circle_distance(X) -> the mean over rows of | ||x|| - 1 |, the distance to the unit circle.
S_DEC = 0.1: the decoder's fixed noise, p(x | z) = N(vae_decode(z), S_DEC^2 I).
NumPy only; no state is kept between calls.
"""
import numpy as np

__version__ = "1.0"

S_DEC = 0.1


def g_circle(z):
    z = np.asarray(z, dtype=float)
    return np.stack([np.sin(z), np.cos(z)], axis=-1)


def circle_model(n, s=0.05, seed=0):
    g = np.random.default_rng(seed)
    z = g.standard_normal(n)
    return g_circle(z) + s * g.standard_normal((n, 2)), z


def init_vae(d=2, hidden=32, k=1, seed=0):
    g = np.random.default_rng(seed)
    out = []
    for fi, fo in ((d, hidden), (hidden, k), (hidden, k), (k, hidden), (hidden, d)):
        out.append(g.standard_normal((fi, fo)) / np.sqrt(fi))
        out.append(np.zeros(fo))
    return out


def _tanh(a):
    return a.tanh() if hasattr(a, 'tanh') else np.tanh(a)


def vae_encode(params, X):
    We, be, Wm, bm, Wv, bv = params[:6]
    h = _tanh(X @ We + be)
    return h @ Wm + bm, h @ Wv + bv


def vae_decode(params, Z):
    Wd, bd, Wo, bo = params[6:]
    return _tanh(Z @ Wd + bd) @ Wo + bo


def circle_distance(X):
    X = np.asarray(X, dtype=float)
    return float(np.abs(np.sqrt((X ** 2).sum(axis=1)) - 1.0).mean())
