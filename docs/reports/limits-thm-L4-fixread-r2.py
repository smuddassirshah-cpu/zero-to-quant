"""Fix-pass read, limits-thm level 4, round 2: recompute every number in the
text changed by commit d646294b. Exits 0 when all checks pass."""
import json, math, re, sys
from pathlib import Path
import numpy as np
from scipy import stats

fails = []
def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.6g}, text {want}")
    if not ok:
        fails.append(name)

N, T = stats.norm, stats.t(29)
# homework-4 best of 50 (one-sided throughout)
check("hw 1-Phi(2.6)", N.sf(2.6), 0.0047, 5e-5)
check("hw max>=2.6 normal", 1 - N.cdf(2.6) ** 50, 0.208, 1e-3)
check("hw median best", N.ppf(0.5 ** (1 / 50)), 2.20, 6e-3)
rng = np.random.default_rng(1)
check("hw mean best (sim)", rng.standard_normal((400000, 50)).max(axis=1).mean(), 2.25, 6e-3)
check("hw 0.99^(1/50)", 0.99 ** (1 / 50), 0.99980, 5e-6)
check("hw cut-off", N.ppf(0.99 ** (1 / 50)), 3.54, 6e-3)
check("hw Bonferroni z", N.isf(0.01 / 50), 3.54, 6e-3)
check("hw t29 tail", T.sf(2.6), 0.0073, 5e-5)
check("hw t29 max", 1 - T.cdf(2.6) ** 50, 0.31, 6e-3)
check("hw t29 median best", T.ppf(0.5 ** (1 / 50)), 2.32, 6e-3)
check("hw t29 cut-off", T.ppf(0.99 ** (1 / 50)), 4.0, 6e-2)
# l15: standard error of an exponential sample mean, relative to the mean
check("l15 rel SE at 1e5", 1 / math.sqrt(1e5), 0.003, 2e-4)
check("l15 P(mean within 1%)", 1 - 2 * N.sf(0.01 * math.sqrt(1e5)), 1.0, 2e-3)
m = rng.exponential(1.0, (2000, 100000)).mean(axis=1)
check("l15 sim share within 1%", float(np.mean(np.abs(m - 1) < 0.01)), 1.0, 5e-3)
check("l15 default chance", 1 - math.exp(-0.1), 0.0952, 5e-5)
# l17
p1 = 1 - math.exp(-0.02)
check("l17 one issuer", p1, 0.0198, 5e-5)
check("l17 five times", 5 * p1, 0.0990, 5e-5)
check("l17 first default", 1 - math.exp(-0.1), 0.0952, 5e-5)
check("l17 density of max", 5 * 0.9 ** 4, 3.2805, 1e-9)
check("l17 P(max>0.8)", 1 - 0.8 ** 5, 2 / 3, 0.01)
# l18
r = stats.t(5).sf(2) / N.sf(2)
print(f"     l18 ratio t5/normal beyond 2: {r:.3f}")
if not r > 2: fails.append("l18 ratio")
# l19
a, b = stats.poisson(2).pmf(3), stats.poisson(1.5).pmf(3)
check("l19 Poisson(2) at 3", a, 0.1804, 5e-5)
check("l19 Poisson(1.5) at 3", b, 0.1255, 5e-5)
check("l19 slip", a + b, 0.306, 1e-3)
conv = sum(stats.poisson(2).pmf(k) * stats.poisson(1.5).pmf(3 - k) for k in range(4))
check("l19 convolution", conv, 0.2158, 5e-5)
cb = lambda n, a: min(math.exp(-k / 100 * a) * math.cosh(k / 100) ** n for k in range(301))
check("l19 Chernoff(100,30)", cb(100, 30), 0.0104, 2e-4)
ex = sum(math.comb(100, k) for k in range(65, 101)) / 2 ** 100
if not ex <= cb(100, 30): fails.append("chernoff is a bound")
# l19 Cauchy: density ~ 1/(pi x^2), tail probability ~ 1/(pi x)
x = 1e4
check("Cauchy pdf * pi x^2", stats.cauchy.pdf(x) * math.pi * x * x, 1.0, 1e-6)
check("Cauchy sf * pi x", stats.cauchy.sf(x) * math.pi * x, 1.0, 1e-6)
# problems-4
check("p4 int_0^inf e^-y", 1.0, 1.0, 0)
check("p4 E[Y|X=.5]", 0.5 + 1, 1.5, 0)

# voice: longest sentence in each changed string (words; TeX spans count as one word)
new = [
 "Independence needs a density that factors on a support that is an $x$ range times a $y$ range, a rectangle when both are intervals.",
 "At 100,000 draws the standard error of the sample mean is about 0.3% of $M$, so the mean lands within a percent of it.",
 "$M$ is the MGF of $N$, so $Z$ in distribution, given that the MGF exists near 0: MGFs that converge near 0 to an MGF force the distributions to converge",
 "For a sum of $n$ independent copies, each with MGF $M$, Chernoff bounds a tail by $m$.",
]
for s in new:
    w = len(re.sub(r"\$[^$]*\$", "X", s).split())
    print(f"     words {w}: {s[:50]}")
    if w > 35: fails.append("long sentence")
sys.exit(1 if fails else 0)
