"""representations level 1: seeded factor-model returns for the stock-embedding lessons.

factor_returns(seed=7, days=500, lone=False, twin=False) -> (R, sectors)
    R is a days-by-stocks NumPy array of daily returns; sectors is an integer array, one label a stock.
    30 stocks in 3 sectors of 10 (labels 0, 1, 2). Each return is a market move times a loading
    drawn from U(0.7, 1.3), plus a sector move times another such loading, plus noise of 1.2%;
    the market and sector moves have a daily spread of 1%. Stock 9 moves from sector 0 to
    sector 2 halfway through (a business that changed); its label stays 0.
    twin=True adds stock 30, an exact copy of stock 0 (label 0).
    lone=True adds a last stock with noise only, spread 1.5% (label -1).
NumPy only; no state is kept between calls.
"""
import numpy as np

__version__ = "1.0"


def factor_returns(seed=7, days=500, lone=False, twin=False):
    g = np.random.default_rng(seed)
    n, k = 30, 3
    sectors = np.repeat(np.arange(k), n // k)
    bm = g.uniform(0.7, 1.3, n)
    bs = g.uniform(0.7, 1.3, n)
    m = g.standard_normal(days) * 0.01
    f = g.standard_normal((k, days)) * 0.01
    e = g.standard_normal((n, days)) * 0.012
    S = np.repeat(sectors[:, None], days, axis=1)
    S[9, days // 2:] = 2
    R = bm[:, None] * m + bs[:, None] * f[S, np.arange(days)] + e
    rows, labels = [R], list(sectors)
    if twin:
        rows.append(R[:1].copy())
        labels.append(sectors[0])
    if lone:
        rows.append(g.standard_normal((1, days)) * 0.015)
        labels.append(-1)
    return np.vstack(rows).T, np.array(labels)
