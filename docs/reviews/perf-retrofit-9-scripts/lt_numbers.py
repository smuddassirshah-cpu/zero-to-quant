"""Reader checks for limits-thm L1 to L3 performance tasks (review-perf-retrofit-9).
Run with the venv Python from this folder. Exits 1 on any failed check."""
import math, sys
from fractions import Fraction as F
from scipy.stats import norm, binom
import numpy as np

fails = 0
def check(name, ok, info=""):
    global fails
    print(("ok   " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    if not ok:
        fails += 1

# ---------- L1: capped wait ----------
for m in range(1, 31):
    for p in (F(3, 20), F(1, 2), F(9, 10)):
        q = 1 - p
        law = {k: q**(k-1)*p for k in range(1, m)}
        law[m] = q**(m-1)
        assert sum(law.values()) == 1
        mean_series = sum(k*v for k, v in law.items())
        # route 2: recurrence e_m = 1 + q e_{m-1}
        e = F(0)
        for _ in range(m):
            e = 1 + q*e
        assert mean_series == e == (1 - q**m)/p, (m, p)
check("L1 law sums to 1 and series = recurrence = (1-q^m)/p for m<=30, three p", True)
# route 3: Monte Carlo of min(Geo, m) by a separate sampler
rng = np.random.default_rng(1)
X = rng.geometric(0.15, 2_000_000)
T = np.minimum(X, 10)
check("L1 E[T] 5.354 (closed form)", abs((1-0.85**10)/0.15 - 5.354) < 5e-4, f"{(1-0.85**10)/0.15:.6f}")
check("L1 E[T] by simulation", abs(T.mean() - 5.354) < 0.01, f"{T.mean():.4f}")
check("L1 cancel chance 0.1969 (q^10), sim", abs(0.85**10 - 0.1969) < 5e-5 and abs((X > 10).mean() - 0.1969) < 0.002, f"{0.85**10:.6f} sim {(X>10).mean():.4f}")
check("L1 P(T=10) = 0.85^9 = 0.2316", abs(0.85**9 - 0.2316) < 5e-5 and abs((T == 10).mean() - 0.2316) < 0.002)
check("L1 1/p 6.667 and gap 1.31", abs(1/0.15 - 6.667) < 5e-4 and abs(1/0.15 - (1-0.85**10)/0.15 - 1.31) < 0.005)
check("L1 'one time in five'", abs(0.85**10 - 0.2) < 0.01)

# ---------- L2: cycles to exponential ----------
lam, t = 0.5, 4
for n in (10, 100):
    j = math.floor(n*t + 1e-12)
    exact = (1 - F(1, 2)/n) ** j       # lambda = 1/2 exactly
    v = float(exact)
    # route 2: simulate K ~ Geo(lam/n), T = K/n
    K = rng.geometric(lam/n, 2_000_000)
    sim = (K/n > t).mean()
    check(f"L2 P(T_{n}>4) exact {v:.6f} vs sim", abs(sim - v) < 0.002, f"sim {sim:.4f}")
check("L2 0.95^40 = 0.1285", abs(0.95**40 - 0.1285) < 5e-5)
check("L2 0.995^400 = 0.1347", abs(0.995**400 - 0.1347) < 5e-5)
check("L2 e^-2 = 0.1353", abs(math.exp(-2) - 0.1353) < 5e-5)
check("L2 gaps 0.0068 and 0.0007", abs(math.exp(-2)-0.95**40-0.0068) < 5e-5 and abs(math.exp(-2)-0.995**400-0.0007) < 5e-5)
# the squeeze for every n in a grid and t non-integer multiples; and the 'below' claim only when nt whole
below_whole = all((1-lam/n)**(n*tt) < math.exp(-lam*tt) for n in range(1, 400) if n > lam for tt in (1, 2, 4, 7))
check("L2 nt whole: below the limit", below_whole)
# when nt is not whole the value can lie above the limit (so the model's restriction matters)
above = [(n, tt) for n in (1, 2, 3) for tt in (0.9, 1.9) if (1-lam/n)**math.floor(n*tt) > math.exp(-lam*tt)]
check("L2 off-grid t can lie above (restriction needed)", len(above) > 0, str(above[:2]))
# convergence for fixed t by direct large n
check("L2 limit numerically", abs((1-lam/10**7)**math.floor(10**7*t) - math.exp(-2)) < 1e-6)
a, b = -0.02, 0.08
U = rng.uniform(a, b, 2_000_000)
check("L2 uniform mean 0.03, var 0.000833, sd 0.0289", abs((a+b)/2-0.03) < 1e-12 and abs((b-a)**2/12-0.000833) < 5e-7 and abs((b-a)/math.sqrt(12)-0.0289) < 5e-5)
check("L2 uniform by simulation", abs(U.mean()-0.03) < 2e-4 and abs(U.std()-0.02887) < 2e-4)
check("L2 Var algebra exact", F(4)*(F(1,1)) == 4 and all(F(aa**2+aa*bb+bb**2,3) - F(aa+bb,2)**2 == F((bb-aa)**2,12) for aa in range(-5,5) for bb in range(-5,5)))

# ---------- L3: desk guarantee ----------
check("L3 kind A mean 0.1 var 0.99", abs(0.55-0.45-0.1) < 1e-12 and abs(1-0.01-0.99) < 1e-12)
mB = F(3,10)*3 - F(7,10); vB = F(3,10)*9 + F(7,10) - mB**2
check("L3 kind B mean 0.2 var 3.36", mB == F(1,5) and vB == F(84,25))
# Bernoulli variance route: A = 2W-1, var 4 p q ; B = 4W-1, var 16 p q
check("L3 variances by 4pq and 16pq", abs(4*0.55*0.45-0.99) < 1e-12 and abs(16*0.3*0.7-3.36) < 1e-12)
ncheb = math.ceil(F(435,100) / (F(9,100)*F(5,100)))
check("L3 Chebyshev n = 967", ncheb == 967 and F(435,100)/(F(9,100)*966) > F(1,20))
zq = norm.ppf(0.95)
nn = (zq*math.sqrt(4.35)/0.3)**2
check("L3 normal n: 130.8 -> 131 (exact z and 1.645)", math.ceil(nn) == 131 and math.ceil((1.645*math.sqrt(4.35)/0.3)**2) == 131, f"{nn:.3f}")
check("L3 sqrt(4.35)=2.0857, 11.44", abs(math.sqrt(4.35)-2.0857) < 5e-5 and abs(1.645*2.0857/0.3-11.44) < 0.005)

def p_fail(n):
    """Exact P(S <= 0) for n bets of each kind. S = 2W_A + 4W_B - 2n <= 0  <=>  W_A + 2 W_B <= n."""
    pa = binom.pmf(np.arange(n+1), n, 0.55)
    cb = binom.pmf(np.arange(n+1), n, 0.3)
    ca = np.cumsum(pa)
    tot = 0.0
    for wb in range(n+1):
        lim = n - 2*wb
        if lim < 0:
            break
        tot += cb[wb]*ca[lim]
    return tot

def p_fail_int(n):
    """Same, in exact rationals (route 2)."""
    pa, qa, pb, qb = F(11,20), F(9,20), F(3,10), F(7,10)
    A = [math.comb(n,k)*pa**k*qa**(n-k) for k in range(n+1)]
    cA = []
    s = F(0)
    for x in A:
        s += x; cA.append(s)
    tot = F(0)
    for wb in range(n+1):
        lim = n - 2*wb
        if lim < 0: break
        tot += math.comb(n,wb)*pb**wb*qb**(n-wb)*cA[lim]
    return tot

vals = {n: p_fail(n) for n in range(1, 1001)}
ok_ns = [n for n in vals if vals[n] <= 0.05]
smallest = min(ok_ns)
check("L3 exact smallest n = 136", smallest == 136, f"P(135)={vals[135]:.5f} P(136)={vals[136]:.5f}")
check("L3 exact route 2 (rationals) at 135, 136", float(p_fail_int(135)) > 0.05 and float(p_fail_int(136)) <= 0.05 and abs(float(p_fail_int(136)) - vals[136]) < 1e-12, f"{float(p_fail_int(136)):.6f}")
later_bad = [n for n in range(136, 1001) if vals[n] > 0.05]
check("L3 every n >= 136 (to 1,000) also meets 0.95", not later_bad, str(later_bad[:10]))
nonmono = [n for n in range(2, 1001) if vals[n] > vals[n-1]]
print("     note: n where P(S<=0) rises with n:", nonmono[:20])
# Chebyshev 967 really suffices exactly (much more)
check("L3 at 967 exact chance far below 0.05", p_fail(967) < 1e-4, f"{p_fail(967):.2e}")
# normal at 131 vs exact at 131, and continuity correction
pn131 = norm.cdf(-0.3*131/math.sqrt(4.35*131))
print(f"     normal at 131 {pn131:.5f}, exact at 131 {vals[131]:.5f}")
cc = [n for n in range(1, 400) if norm.cdf((1 - 0.3*n)/math.sqrt(4.35*n)) <= 0.05]
print("     normal with continuity correction (S on even lattice, +1): smallest n", min(cc))
check("L3 normal without correction gives too little chance at 131", pn131 < vals[131])
# simulation route 3
rs = np.random.default_rng(3)
for n in (131, 136):
    WA = rs.binomial(n, 0.55, 2_000_000); WB = rs.binomial(n, 0.3, 2_000_000)
    S = 2*WA + 4*WB - 2*n
    check(f"L3 sim P(S<=0) at {n}", abs((S <= 0).mean() - vals[n]) < 0.001, f"{(S<=0).mean():.4f} vs {vals[n]:.4f}")
check("L3 ratio 967/136 about seven", 6.5 < 967/136 < 7.5)
# (c) counterexample variance of average with sigma_i^2 = i
check("L3 (n+1)/(2n)", all(F(sum(range(1,n+1)), n*n) == F(n+1, 2*n) for n in range(1, 50)))

print("failures:", fails)
sys.exit(1 if fails else 0)
