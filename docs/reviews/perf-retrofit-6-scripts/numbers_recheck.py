"""Reader recheck of the two longform items' numbers and claims, by routes other than the authors'.
contests hw3-due-order: EDD optimality by random search against brute force; the model's block swap
(positions k and m) and the textbook adjacent-inversion swap each never raise the maximum; the counterexamples.
ensembles hw-floor-derive: exact fractions, the B x B covariance matrix summed, and a seeded simulation of
equicorrelated forecasts (one shared factor). Venv Python, from this folder."""
import sys, random, itertools
from fractions import Fraction as F
import numpy as np

bad = 0
def check(name, ok, detail=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    bad += not ok

# ---------------- contests ----------------
def lmax(order, p, d, r=None):
    t, worst = 0, 0
    for j in order:
        if r is not None:
            t = max(t, r[j])
        t += p[j]
        worst = max(worst, t - d[j], 0)
    return worst

rng = random.Random(2026)
edd_ok = block_ok = adj_ok = True
for trial in range(20000):
    n = rng.randint(1, 6)
    p = [rng.randint(1, 6) for _ in range(n)]
    d = [rng.randint(0, 20) for _ in range(n)]
    best = min(lmax(o, p, d) for o in itertools.permutations(range(n)))
    G = sorted(range(n), key=lambda j: (d[j], rng.random()))
    edd_ok &= lmax(G, p, d) == best
    # model's swap: random order O, first difference k with G, swap positions k and m
    O = list(range(n)); rng.shuffle(O)
    for k in range(n):
        if O[k] != G[k]:
            break
    else:
        continue
    # make O agree with G up to k-1 (the model's setting)
    pre = G[:k]; rest = [j for j in O if j not in pre]; O = pre + rest
    if O[k] == G[k]:
        continue
    m = O.index(G[k])
    O2 = O[:]; O2[k], O2[m] = O2[m], O2[k]
    block_ok &= lmax(O2, p, d) <= lmax(O, p, d)
    # textbook route: any adjacent inversion (d of the first > d of the second) swapped never raises Lmax
    for i in range(n - 1):
        if d[O[i]] > d[O[i + 1]]:
            O3 = O[:]; O3[i], O3[i + 1] = O3[i + 1], O3[i]
            adj_ok &= lmax(O3, p, d) <= lmax(O, p, d)
check("contests: EDD with random tie order equals brute force, 20,000 instances, n <= 6", edd_ok)
check("contests: the model's swap of positions k and m never raises the maximum (O agreeing with G before k)", block_ok)
check("contests: an adjacent inversion swapped never raises the maximum", adj_ok)

# counterexamples, every order and integer start delay up to 10
def best_with_ready(p, d, r):
    best = None
    for o in itertools.permutations(range(len(p))):
        for waits in itertools.product(range(11), repeat=len(p)):
            t, worst = 0, 0
            for j, wt in zip(o, waits):
                t = max(t + wt, r[j]); t += p[j]; worst = max(worst, t - d[j], 0)
            best = worst if best is None else min(best, worst)
    return best
pA = [5, 1]; dA = [7, 6]; rA = [0, 5]
check("contests: ready-time case, greedy (B, A) late 4", lmax([1, 0], pA, dA, rA) == 4)
check("contests: ready-time case, best 0", best_with_ready(pA, dA, rA) == 0)
pB = [4, 1]; dB = [10, 2]; rB = [0, 1]
# never-wait rule: at each free moment run the ready job due first
t, left, worst = 0, {0, 1}, 0
while left:
    ready = [j for j in left if rB[j] <= t]
    if not ready:
        t = min(rB[j] for j in left); continue
    j = min(ready, key=lambda j: dB[j]); t += pB[j]; worst = max(worst, t - dB[j], 0); left.remove(j)
check("contests: never-wait rule late 3", worst == 3, str(worst))
check("contests: waiting gives 0", best_with_ready(pB, dB, rB) == 0)
pC = [5, 1]; dC = [1, 2]
def tot(o, p, d):
    t = s = 0
    for j in o:
        t += p[j]; s += max(0, t - d[j])
    return s
check("contests: total lateness A,B 8 and B,A 5", tot([0, 1], pC, dC) == 8 and tot([1, 0], pC, dC) == 5)
check("contests: worst lateness A,B 4 and B,A 5", lmax([0, 1], pC, dC) == 4 and lmax([1, 0], pC, dC) == 5)

# ---------------- ensembles ----------------
def var_avg(s2, rho, B):
    return rho * s2 + (1 - rho) * s2 / B
A100, A1000 = var_avg(F(40), F(1, 5), 100), var_avg(F(40), F(1, 5), 1000)
check("ensembles: 8.32 and 8.032", A100 == F(832, 100) and A1000 == F(8032, 1000))
check("ensembles: gain 0.288, about 3.5%", A100 - A1000 == F(288, 1000) and round(float((A100 - A1000) / A100) * 100, 1) == 3.5,
      f"{float((A100 - A1000) / A100):.4%}")
check("ensembles: tenfold target 0.832 below floor 8", A100 / 10 == F(832, 1000) and A100 / 10 < 8)
B2 = var_avg(F(50), F(2, 25), 1000)
check("ensembles: second forest 4.046, gap 3.986", B2 == F(4046, 1000) and A1000 - B2 == F(3986, 1000))
cross = [B for B in range(1, 50) if var_avg(F(50), F(2, 25), B) < var_avg(F(40), F(1, 5), B)]
check("ensembles: second forest ahead exactly from B = 4", cross == list(range(4, 50)))
check("ensembles: B = 3 gives 19.33 against 18.67; B = 4 gives 15.5 against 16",
      round(float(var_avg(50, 0.08, 3)), 2) == 19.33 and round(float(var_avg(40, 0.2, 3)), 2) == 18.67
      and var_avg(F(50), F(2, 25), 4) == F(31, 2) and var_avg(F(40), F(1, 5), 4) == 16)
# route 2: sum the covariance matrix
for s2, rho, B, want in [(40, 0.2, 100, 8.32), (40, 0.2, 1000, 8.032), (50, 0.08, 1000, 4.046)]:
    C = np.full((B, B), rho * s2); np.fill_diagonal(C, s2)
    check(f"ensembles: covariance matrix route s2={s2} rho={rho} B={B}", abs(C.sum() / B ** 2 - want) < 1e-9)
# route 3: simulation, one shared factor gives equicorrelation; the mean is unchanged by averaging
g = np.random.default_rng(7)
N, B = 20000, 100
z0 = g.standard_normal((N, 1)); z = g.standard_normal((N, B))
X = 1.5 + np.sqrt(40) * (np.sqrt(0.2) * z0 + np.sqrt(0.8) * z)
v = X.mean(axis=1).var()
check("ensembles: simulated variance at B = 100 near 8.32", abs(v - 8.32) < 0.25, f"{v:.3f}")
check("ensembles: simulated mean of the average equals one tree's mean", abs(X.mean(axis=1).mean() - X[:, 0].mean()) < 0.1)
# the exact hypotheses: common variance and pairwise covariance suffice; identical distribution is not used.
# Two trees from different laws (normal and a scaled uniform) with the same mean, variance and covariance.
u = g.uniform(-1, 1, (200000,)) * np.sqrt(3 * 40)      # variance 40, uniform
w = g.standard_normal(200000)
n2 = np.sqrt(40) * (0.2 * u / np.sqrt(40) + np.sqrt(1 - 0.04) * w)   # variance 40, corr 0.2 with u, not uniform
vv = ((u + n2) / 2).var()
check("ensembles: non-identical laws with common variance and correlation give the same Var of the average",
      abs(vv - var_avg(40, 0.2, 2)) < 0.4, f"{vv:.3f} against {var_avg(40, 0.2, 2)}")
print("bad:", bad)
sys.exit(1 if bad else 0)
