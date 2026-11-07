"""Reader's recompute of the numbers in research-int h2-pca-aloud and
coding-int h4-pairs-aloud, by routes other than the authors'."""
import itertools
import math
import random
import numpy as np
from harness import item, check, finish

# research-int h2-pca-aloud
lam = [20.6, 3.1, 2.4] + list(np.linspace(0.85, 0.17, 47))
check(abs(sum(lam) - 50) < 0.1, f'eigenvalues sum to about 50 ({sum(lam):.2f}) with a straight fall 0.85 to 0.17')
cum = np.cumsum(lam) / 50
k80 = int(np.searchsorted(cum, 0.8 - 1e-12) + 1)
check(k80 == 23, f'80% rule keeps {k80} components')
edge = (1 + math.sqrt(50 / 500)) ** 2
check(round(edge, 2) == 1.73, f'noise edge {edge:.4f}')
check([round(100 * x / 50) for x in (20.6, 3.1, 2.4)] == [41, 6, 5], 'shares 41%, 6%, 5%')
resid = (50 - 26.1) / 47
check(round(resid, 2) == 0.51 and round(resid * edge, 2) == 0.88, f'residual noise {resid:.4f}, scaled bar {resid * edge:.4f}')
alt = (1 - 20.6 / 50) * edge
check(alt > 0.85, f'the other common scaling, (1 - 20.6/50) x edge = {alt:.3f}, also leaves the fourth (0.85) below')
rho = (20.6 - 1) / 49
check(abs(rho - 0.4) < 1e-12 and abs(1 + 49 * 0.6 - 30.4) < 1e-12, f'rho {rho}, stressed eigenvalue 30.4')
check(round(100 * 30.4 / 50) == 61, 'stressed share 61%')
R = np.full((50, 50), 0.6); np.fill_diagonal(R, 1)
ev, vec = np.linalg.eigh(R)
check(abs(ev[-1] - 30.4) < 1e-9 and np.allclose(np.abs(vec[:, -1]), 1 / math.sqrt(50)),
      'equicorrelation: top eigenvalue 30.4 and the loadings stay equal (only the eigenvalue grows)')
rng = np.random.default_rng(11)
tops = [np.linalg.eigvalsh(np.corrcoef(rng.standard_normal((500, 50)), rowvar=False))[-1] for _ in range(40)]
check(1.6 < float(np.mean(tops)) < 1.9, f'pure-noise top eigenvalue, 40 seeded runs: mean {np.mean(tops):.3f}')
# raw returns weighted by a correlation eigenvector are not uncorrelated when volatilities differ
vol = np.diag([0.1, 0.3, 0.5]); C = np.array([[1, .5, .2], [.5, 1, .4], [.2, .4, 1]])
_, V = np.linalg.eigh(C)
cov_raw = V.T @ (vol @ C @ vol) @ V
check(abs(cov_raw[0, 1]) > 1e-3, f'baskets of raw returns on correlation eigenvectors correlate (cov {cov_raw[0, 1]:.4f}); only standardised baskets are uncorrelated')

# coding-int h4-pairs-aloud
def brute(a, t):
    return sum(1 for i, j in itertools.combinations(range(len(a)), 2) if a[i] + a[j] == t)
def plan_a(a, t):
    seen, p = {}, 0
    for x in a:
        p += seen.get(t - x, 0); seen[x] = seen.get(x, 0) + 1
    return p
def two_pointers(a, t):
    a = sorted(a); i, j, p = 0, len(a) - 1, 0
    while i < j:
        s = a[i] + a[j]
        if s < t: i += 1
        elif s > t: j -= 1
        elif a[i] == a[j]:
            k = j - i + 1; p += k * (k - 1) // 2; break
        else:
            ri = 1
            while i + ri < j and a[i + ri] == a[i]: ri += 1
            rj = 1
            while j - rj > i and a[j - rj] == a[j]: rj += 1
            p += ri * rj; i += ri; j -= rj
    return p
def many(a, t):
    c = {}
    for x in a: c[x] = c.get(x, 0) + 1
    return sum(c[v] * c.get(t - v, 0) for v in c if v < t - v) + sum(c[v] * (c[v] - 1) // 2 for v in c if 2 * v == t)
check(brute([4, 6, 5, 5, 1, 9, 5], 10) == 5, 'example gives 5')
rng = random.Random(3)
ok = all(brute(a, t) == plan_a(a, t) == two_pointers(a, t) == many(a, t)
         for a, t in ((([rng.randrange(0, 12) for _ in range(rng.randrange(0, 15))]), rng.randrange(0, 24)) for _ in range(3000)))
check(ok, 'brute force, plan A, two pointers and the many-targets sum agree on 3,000 lists')
check(200000 * 199999 // 2 == 19999900000 and 19999900000 > 2 ** 31 - 1 == 2147483647, '19,999,900,000 exceeds int (2,147,483,647)')
finish()
