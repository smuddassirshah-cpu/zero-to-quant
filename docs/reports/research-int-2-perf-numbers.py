"""research-int L2 performance task h2-pca-aloud: every stated number, two routes each.
Run: python3 docs/reports/research-int-2-perf-numbers.py (exit 0 when all agree)."""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np

fails = []
def check(name, a, b, stated=None, tol=1e-9, dp=None):
    ok = abs(a - b) <= tol * max(1, abs(a))
    if stated is not None and dp is not None:
        ok = ok and round(a, dp) == stated
    print(f"{'ok ' if ok else 'BAD'} {name}: {a!r} | {b!r} | stated {stated}")
    if not ok:
        fails.append(name)

p, n = 50, 500
top = [20.6, 3.1, 2.4]
# spectrum: the other 47 fall linearly from 0.85 to b, with the whole trace 50
rest = p - sum(top)
k = p - len(top)
b = 2 * rest / k - 0.85
tail = np.linspace(0.85, b, k)
ev = np.r_[top, tail]
check("trace of a correlation matrix = number of stocks", float(ev.sum()), float(F(p)), 50, dp=6)
check("lowest tail eigenvalue about 0.17", b, float(2 * F(rest).limit_denominator(1000) / k - F(85, 100)), 0.17, dp=2)
# shares, two routes (float and exact fraction)
for lam, st in zip(top, [41, 6, 5]):
    check(f"share of {lam}", 100 * lam / p, float(100 * F(str(lam)) / p), st, dp=0)
# components to reach 80%: cumsum, then the arithmetic-series formula
cum = np.cumsum(ev) / p
m1 = int(np.argmax(cum >= 0.8) + 1)
d = (0.85 - b) / (k - 1)
m2 = next(3 + j for j in range(1, k + 1) if sum(top) + j * 0.85 - d * j * (j - 1) / 2 >= 0.8 * p)
check("components that reach 80%", m1, m2, 23, dp=0)
check("cumulative share after 22 is under 80%", float(cum[21] < 0.8), 1.0)
# noise edge, formula and seeded simulation
edge = (1 + math.sqrt(p / n)) ** 2
rng = np.random.default_rng(20261107)
sims = []
for _ in range(40):
    X = rng.standard_normal((n, p))
    C = np.corrcoef(X, rowvar=False)
    sims.append(np.linalg.eigvalsh(C)[-1])
check("noise edge (1 + sqrt(0.1))^2", edge, 1 + 2 * math.sqrt(0.1) + 0.1, 1.73, dp=2)
check("simulated top noise eigenvalue near the edge", float(np.mean(sims)), edge, tol=0.06)
print("   simulated mean top eigenvalue", round(float(np.mean(sims)), 3))
# leftover noise per stock and the scaled bar
left = rest / k
check("leftover variance a stock", left, float(F(rest).limit_denominator(1000) / k), 0.51, dp=2)
check("scaled bar 0.51 x 1.73", 0.51 * 1.73, left * edge, 0.88, tol=0.01)
check("scaled bar rounds to 0.88 either way", round(0.51 * 1.73, 2), round(left * edge, 2), 0.88, dp=2)
check("2.4 clears 1.73 and 0.85 misses 0.88", float(2.4 > edge and 0.85 < round(left * edge, 2) and 0.85 < left * edge), 1.0)
check("noise components kept by the 80% rule", m1 - 3, sum(1 for x in ev[:m1] if x < left * edge), 20, dp=0)
# equicorrelation: first eigenvalue 1 + 49 rho, formula and eigvalsh
for rho, lam, sh in [(0.4, 20.6, 41), (0.6, 30.4, 61)]:
    R = np.full((p, p), rho); np.fill_diagonal(R, 1)
    top_e = float(np.linalg.eigvalsh(R)[-1])
    check(f"first eigenvalue at rho {rho}", 1 + (p - 1) * rho, top_e, lam, dp=1)
    check(f"share at rho {rho}", 100 * top_e / p, 100 * (1 + (p - 1) * rho) / p, sh, dp=0)

# item shape: rubric sums to 10, one required row, homework limits
here = os.path.dirname(os.path.abspath(__file__))
hw = json.load(open(os.path.join(here, "..", "..", "app", "content", "courses", "research-int", "homework-2.json")))
it = next(i for i in hw["items"] if i["id"] == "h2-pca-aloud")
rub = it["widget"]["rubric"]
check("rubric sums to 10", sum(r["points"] for r in rub), 10, 10, dp=0)
check("rows 1 to 3 required (three-part objective), row 4 optional", sum(2 ** k for k, r in enumerate(rub) if r.get("required")), 7, 7, dp=0)
check("homework items within 6 to 12", float(6 <= len(hw["items"]) <= 12), 1.0)
check("one performance item", sum(1 for i in hw["items"] if i.get("performance")), 1, 1, dp=0)
w = it["widget"]
check("seconds and follow-ups in range", float(15 <= w["seconds"] <= 1800 and 1 <= len(w["followUps"]) <= 5), 1.0)

if fails:
    print("FAILED:", fails); sys.exit(1)
print("all numbers agree")
