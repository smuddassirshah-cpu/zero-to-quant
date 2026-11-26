"""Fix-pass read of a43a6c2e (measure-prob problems 1, 2, 4). Exits 0 when every check holds."""
from fractions import Fraction as F
import numpy as np
from scipy import integrate

fails = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


def poly_int(coefs):
    """Exact integral over [0, 1] of sum c_k x^k."""
    return sum(F(c) / (k + 1) for k, c in coefs.items())


# problems-4 p-recovery-reweight part 3: P has density 2x, Q has density 4x^3, Z = 2x^2.
EZ = poly_int({3: 4})    # 2x^2 * 2x
EZ2 = poly_int({5: 8})   # 4x^4 * 2x
check("E_P[Z] = 1", EZ == 1)
check("E_P[Z^2] = 8/6 = 4/3", EZ2 == F(8, 6) == F(4, 3))
check("Var_P(Z) = 1/3", EZ2 - EZ ** 2 == F(1, 3))
q = lambda f: integrate.quad(lambda x: f(x) * 2 * x, 0, 1)[0]
check("quad E_P[Z] = 1", abs(q(lambda x: 2 * x * x) - 1) < 1e-10)
check("quad Var_P(Z) = 1/3", abs(q(lambda x: 4 * x ** 4) - 1 - 1 / 3) < 1e-10)
# The replaced sentence "every density has P-mean 1" was false for the two densities themselves.
check("E_P[2X] = 4/3, not 1", poly_int({2: 4}) == F(4, 3))
check("E_P[4X^3] = 8/5, not 1", poly_int({4: 8}) == F(8, 5))
check("quad E_P[2X] and E_P[4X^3]",
      abs(q(lambda x: 2 * x) - 4 / 3) < 1e-10 and abs(q(lambda x: 4 * x ** 3) - 1.6) < 1e-10)
# Monte Carlo: X = sqrt(U) has density 2x.
rng = np.random.default_rng(13)
x = np.sqrt(rng.random(4_000_000))
z = 2 * x * x
check("MC E_P[Z] near 1", abs(z.mean() - 1) < 0.002)
check("MC Var_P(Z) near 1/3", abs(z.var() - 1 / 3) < 0.002)
check("MC E_P[2X] near 4/3", abs((2 * x).mean() - 4 / 3) < 0.002)
check("MC E_P[4X^3] near 8/5", abs((4 * x ** 3).mean() - 1.6) < 0.003)

# problems-1 p-fat-cantor part 4: the removed length tends to 1/2, so C has length 1/2 and is not null.
removed = sum(F(2) ** (n - 1) * F(1, 4) ** n for n in range(1, 60))
check("fat Cantor removed length -> 1/2 from below", removed < F(1, 2) and F(1, 2) - removed == F(1, 2 ** 60))

# problems-2 p-random-maturity part 2: quotients are bounded by T <= 4 for r, r+h in [0, 1].
T = np.linspace(0, 4, 401)
worst = -1.0
for r in np.linspace(0, 1, 41):
    for h in np.linspace(-1, 1, 81):
        if abs(h) > 1e-12 and 0 <= r + h <= 1:
            worst = max(worst, np.max(np.abs((np.exp(-(r + h) * T) - np.exp(-r * T)) / h) - T))
check("|quotient| <= T <= 4 on the grid", worst <= 1e-12)
# "Smooth paths are not enough on their own": g(r, t) = r^3 t / (r^2 + t^2)^2 for t in (0, 1].
# For each t > 0 it is smooth in r with dg/dr(0, t) = 0, yet E[g(r, .)] = r / (2 (1 + r^2)),
# whose derivative at 0 is 1/2. No integrable bound dominates the quotients g(h, t) / h.
g = lambda r, t: r ** 3 * t / (r * r + t * t) ** 2
closed = lambda r: r / (2 * (1 + r * r))
for r in (0.05, 0.3, 1.0):
    check(f"counterexample mean at r={r}", abs(integrate.quad(lambda t: g(r, t), 0, 1, points=[min(r, 1)])[0] - closed(r)) < 1e-8)
h = 1e-4
check("counterexample: d/dr E[g] at 0 is 1/2", abs((closed(h) - closed(-h)) / (2 * h) - 0.5) < 1e-6)
check("counterexample: dg/dr(0, t) = 0 for t > 0",
      all(abs((g(1e-6, t) - g(-1e-6, t)) / 2e-6) < 1e-6 for t in (0.1, 0.5, 1.0)))
# sup over h of |g(h, t) / h| is attained at h = t and equals 1 / (4 t), not integrable on (0, 1].
ts = np.array([0.01, 0.1, 0.5])
hs = np.linspace(1e-4, 2, 200001)
check("counterexample: sup_h |g(h,t)/h| = 1/(4t)",
      all(abs(np.max(g(hs, t) / hs) - 1 / (4 * t)) < 1e-6 / t for t in ts))

raise SystemExit(1 if fails else 0)
