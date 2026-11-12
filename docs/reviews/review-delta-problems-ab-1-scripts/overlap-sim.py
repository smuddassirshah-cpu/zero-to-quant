#!/usr/bin/env python3
"""p-overlap-signal part 4 (regression problems-3): my own simulation of the claims the fix pass added.
   503 days, the next-5-day return regressed on two signals with a constant, no true effect.
   (a) signals that are 5-day rolling averages: the naive t of signal A should have sd near sqrt(3.4) = 1.844;
   (b) independent daily signals: sd near 1, so the factor needs the overlapping signal (the sentence added to the prose);
   (c) HAC (Newey-West, Bartlett weights, 4 and 8 lags), hand-coded: share of |t| > 1.96 "about one time in ten".
   Run from the repo root with the scratchpad venv python; seeded; under a minute."""
import sys
import numpy as np

rng = np.random.default_rng(20261112)
RUNS, N, H = 2000, 503, 5
fails = 0


def roll(z):                      # 5-day rolling sums ending at each day
    c = np.cumsum(np.insert(z, 0, 0.0))
    return c[H:] - c[:-H]


def fit(y, X, lags):
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ y
    e = y - X @ b
    n, k = X.shape
    t_naive = b[1] / np.sqrt(e @ e / (n - k) * XtXi[1, 1])
    out = [t_naive]
    u = X * e[:, None]
    for L in lags:
        S = u.T @ u
        for j in range(1, L + 1):
            G = u[j:].T @ u[:-j]
            S += (1 - j / (L + 1)) * (G + G.T)
        V = XtXi @ S @ XtXi * n / (n - k)
        out.append(b[1] / np.sqrt(V[1, 1]))
    return out


def run(overlap_signal):
    ts = []
    for _ in range(RUNS):
        m = N + 2 * H
        r = rng.standard_normal(m)
        za, zb = rng.standard_normal(m), rng.standard_normal(m)
        fwd = roll(r)[H:H + N]                     # sum of days t+1 .. t+5
        if overlap_signal:
            A, B = roll(za)[:N] / H, roll(zb)[:N] / H   # average of days t-4 .. t
        else:
            A, B = za[H - 1:H - 1 + N], zb[H - 1:H - 1 + N]
        X = np.column_stack([np.ones(N), A, B])
        ts.append(fit(fwd, X, (4, 8)))
    return np.array(ts)


def check(cond, msg):
    global fails
    print(('ok      ' if cond else 'FAIL    ') + msg)
    fails += not cond


a = run(True)
b = run(False)
sd_a, sd_b = a[:, 0].std(), b[:, 0].std()
rej = (np.abs(a) > 1.96).mean(axis=0)
check(abs(sd_a - np.sqrt(3.4)) < 0.1, f'(a) rolling-average signals: naive t has sd {sd_a:.3f} (formula 1.844)')
check(abs(sd_b - 1) < 0.07, f'(b) independent daily signals: naive t has sd {sd_b:.3f} (no inflation)')
check(0.07 < rej[1] < 0.16 and 0.07 < rej[2] < 0.16, f'(c) HAC rejects a true zero in {rej[1]:.1%} (4 lags) and {rej[2]:.1%} (8 lags) of runs; naive {rej[0]:.1%}')
check(a[:, 1].std() > 1.1, f'    HAC t has sd {a[:, 1].std():.2f} (4 lags), {a[:, 2].std():.2f} (8 lags): "only part of the way"')
print(f'overlap-sim: {fails} failures')
sys.exit(1 if fails else 0)
