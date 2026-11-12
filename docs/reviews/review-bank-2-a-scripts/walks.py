"""co-spurious-two-walks: the share of independent random-walk pairs (500 steps) whose levels regression has |t| > 1.96,
on 20,000 pairs, to see how far the printed 88.0% (1,000 seeded pairs) is from the long-run figure."""
import numpy as np
rng = np.random.default_rng(7)
R, n = 20000, 500
a = rng.normal(size=(R, n)).cumsum(axis=1); b = rng.normal(size=(R, n)).cumsum(axis=1)
a -= a.mean(axis=1, keepdims=True); b -= b.mean(axis=1, keepdims=True)
r = (a * b).sum(axis=1) / np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))
t = r * np.sqrt((n - 2) / (1 - r * r))
p = (np.abs(t) > 1.96).mean()
print('share beyond 1.96: %.4f (se %.4f)' % (p, np.sqrt(p * (1 - p) / R)))
