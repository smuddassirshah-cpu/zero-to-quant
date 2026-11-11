"""Numbers of the fixes proposed in review-holes-1.6-2.1.md, each worked twice.   python3 proposed.py   (needs numpy, scipy)"""
import math

import numpy as np
from scipy import optimize, stats

n_ok = 0


def expect(name, got, want, tol=1e-9):
    global n_ok
    assert abs(got - want) <= tol, (name, got, want)
    n_ok += 1
    print(f'ok  {name}: {got:.6g}')


# Finding on p-one-unit part 4: the step as set raises the loss
x, y, b1, v, d = 8, 10, -1, 2, 1
yhat = lambda w: v * max(0, w * x + b1) + d
loss = lambda w: 0.5 * (yhat(w) - y) ** 2
expect('loss before the step', loss(0.5), 4.5)
expect('prediction after the step to 0.98', yhat(0.98), 14.68)
expect('loss after the step to 0.98', loss(0.98), 10.9512)
best = optimize.minimize_scalar(loss, bounds=(0.2, 2), method='bounded').x
expect('w1 that fits the row', best, 0.6875, 1e-4)
expect('largest eta that does not raise the loss', 2 * (0.6875 - 0.5) / 48, 0.0078125)
# the fuller fix: eta = 0.002
w_new = 0.5 - 0.002 * (-48)
expect('eta 0.002: new w1', w_new, 0.596)
expect('eta 0.002: prediction', yhat(w_new), 8.536)
expect('eta 0.002: loss', loss(w_new), 1.071648)
expect('eta 0.002: knot', 1 / w_new, 1.678, 5e-4)
expect('eta 0.002: uphill', 0.5 + 0.002 * (-48), 0.404)
expect('eta 0.002: carried w1 (slope -9)', 0.5 - 0.002 * (-9), 0.518)
expect('eta 0.002: carried knot', 1 / 0.518, 1.931, 5e-4)
expect('eta 0.002: knot with the sign lost', -1 / w_new, -1.678, 5e-4)

# Finding on s-pareto-losses: the same numbers under f(x | theta) = theta x^(theta - 1) on (0, 1)
n, s = 80, -32.0
ll = lambda t: n * math.log(t) + (t - 1) * s
mle = optimize.minimize_scalar(lambda t: -ll(t), bounds=(0.1, 20), method='bounded').x
expect('power-law MLE, -n / sum ln x', -n / s, 2.5)
expect('power-law MLE, numeric', mle, 2.5, 1e-4)
h = 1e-4
info1 = -(math.log(2.5 + h) - 2 * math.log(2.5) + math.log(2.5 - h)) / h ** 2
expect('one observation information 1/theta^2', info1, 1 / 6.25, 1e-6)
expect('bound theta^2 / n', 1 / (n * info1), 0.078125, 1e-6)
rng = np.random.default_rng(7)
sim = -n / np.log(rng.random((20000, n)) ** (1 / 2.5)).sum(axis=1)      # X = U^(1/theta) has this density
expect('simulated variance of the MLE is near the bound', sim.var(), 0.078125, 0.012)
expect('slip: theta - 1 = 2.5', 2.5 + 1, 3.5)
expect('slip: sign lost', n / s, -2.5)
expect('slip: upside down', -s / n, 0.4)

# Finding on s-pool-rates: logs kept to 3 places land on the Pearson entry
expect('-2 ln Lambda, logs to 3 places', 2 * (90 * 0.182 + 60 * -0.223), 6.0, 1e-9)
expect('-2 ln Lambda, exact', 2 * (90 * math.log(1.2) + 60 * math.log(0.8)), 6.0407, 5e-5)
expect('Pearson', 15 ** 2 / 75 * 2, 6.0)

# Finding on p-order-sizes part 3: the inertia that follows from part 2's slip (groups of part 1, centres 3 and 18)
pts = [2, 4, 6, 18, 22, 26]
expect('inertia with 6 left in group 2', sum((p - 3) ** 2 for p in pts[:2]) + sum((p - 18) ** 2 for p in pts[2:]), 226)
expect('the present "carried" value', sum((p - 3) ** 2 for p in pts[:3]) + sum((p - 18) ** 2 for p in pts[3:]), 91)

# Per cent sign entries: what the grader reads when a % follows the number
expect('p-order-sizes part 1 with %', 18 / 100, 0.18)
expect('p-order-sizes part 2 with %', 22 / 100, 0.22)

# Restoring e-odds-update: its key
odds = 0.1 / 0.9 * math.exp(0.45 * 2)
expect('e-odds-update key', odds / (1 + odds), 0.2146, 5e-5)

# Bands proposed for two Fluency families: see shares.py for the shares
expect('chi-squared 5% cut-off, 1 df', stats.chi2.ppf(0.95, 1), 3.841, 5e-4)
print(n_ok, 'checks passed')
