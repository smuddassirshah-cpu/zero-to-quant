"""estimation L2 hw2-pareto-tail (numbers, two routes) and L3 h-bump-interval (code: shipped, starter, reader
solution, valid variants, planted slips, replay margins). Run with the venv Python: python -I est_two.py"""
import sys, pathlib, math, random
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1

# ---------- L2: Pareto with x_m = 1 known
xs = [1.5, 1.2, 3.0, 1.1, 2.4, 1.8]
logs = [math.log(v) for v in xs]
check("logs 0.4055 0.1823 1.0986 0.0953 0.8755 0.5878", [round(v, 4) for v in logs] == [0.4055, 0.1823, 1.0986, 0.0953, 0.8755, 0.5878])
S = sum(logs)
check("S = 3.2450 (also ln of the product 23.5224)", round(S, 4) == 3.2450 and abs(S - math.log(math.prod(xs))) < 1e-12)
a_mle, a_unb = 6 / S, 5 / S
check("MLE 1.85, unbiased 1.54", round(a_mle, 2) == 1.85 and round(a_unb, 2) == 1.54)
# route 2 for the MLE: maximise the log-likelihood on a fine grid
ll = lambda a: 6 * math.log(a) - (a + 1) * S
grid = max((k / 10000 for k in range(1, 100000)), key=ll)
check("grid maximiser agrees with 6/S", abs(grid - a_mle) < 1e-4)
for a, want in ((a_mle, 0.014), (a_unb, 0.029), (1.85, 0.014), (1.54, 0.029)):
    check(f"10^-{a:.4f} rounds to {want}", round(10 ** -a, 3) == want)
# tail chance route 2: integrate the density from 10 to infinity
from scipy import integrate
for a in (a_mle, a_unb):
    v = integrate.quad(lambda x: a * x ** (-a - 1), 10, math.inf)[0]
    check(f"P(X > 10) by quadrature at alpha {a:.4f}", abs(v - 10 ** -a) < 1e-9)
check("about half as likely: 0.0142 / 0.0288 near 0.49", abs((10 ** -a_mle) / (10 ** -a_unb) - 0.49) < 0.01)
# E[1/S] = alpha/(n-1) for S ~ Gamma(n, alpha): quadrature and simulation
from scipy import stats
for n, a in ((2, 1.3), (6, 1.85), (10, 0.7)):
    q = integrate.quad(lambda s: stats.gamma.pdf(s, n, scale=1 / a) / s, 0, math.inf)[0]
    check(f"E[1/S] n={n} alpha={a} quadrature = alpha/(n-1)", abs(q - a / (n - 1)) < 1e-7)
rng = random.Random(11)
n, a, T = 6, 1.7, 200000
tot = 0.0
for _ in range(T):
    # Pareto by inversion, X = U^(-1/alpha)
    tot += n / sum(math.log((1 - rng.random()) ** (-1 / a)) for _ in range(n))
m = tot / T
check(f"simulated E[alpha hat] {m:.4f} near n alpha/(n-1) = {n * a / (n - 1):.4f}", abs(m - n * a / (n - 1)) < 0.01)
check("unbiased multiple (n-1)/n of it near alpha", abs(m * (n - 1) / n - a) < 0.01)
# ln X exponential: P(ln X > y) = e^{-alpha y} by quadrature
check("P(ln X > 0.7) = e^{-0.7 alpha}", abs(integrate.quad(lambda x: 2.0 * x ** -3.0, math.exp(0.7), math.inf)[0] - math.exp(-1.4)) < 1e-10)
check("n = 6: MLE averages 6/5 of the truth, 20% high", abs(6 / 5 - 1.2) < 1e-12)

# ---------- L3 code
it = item("estimation", "homework-3.json", "h-bump-interval")
w = it["widget"]
sol = w["solution"]
print("L3 h-bump-interval")
f, _ = summary(w, sol, "shipped solution", "all"); check("shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("starter fails", len(f) > 0)
mine = r'''
import random
def bump_interval(delays, level):
    m, n = max(delays), len(delays)
    tail = (1 - level) / 2
    # P(M <= u theta) = u^n: theta is at least M / (1 - tail)^(1/n) and at most M / tail^(1/n)
    return (m * (1 - tail) ** (-1 / n), m * tail ** (-1 / n))
def bump_coverage(theta, n, level, trials, seed):
    rng = random.Random(seed)
    inside = 0
    for _ in range(trials):
        d = [rng.uniform(0, theta) for _ in range(n)]
        lo, hi = bump_interval(d, level)
        inside += lo <= theta <= hi
    return inside / trials
'''
f, _ = summary(w, mine, "reader solution (powers -1/n, rng.uniform)", "all"); check("reader solution passes", f == [])
logs_v = r'''
import random, math
def bump_interval(delays, level):
    m, n = max(delays), len(delays)
    a = 1 - level
    return [math.exp(math.log(m) - math.log(1 - a / 2) / n), math.exp(math.log(m) - math.log(a / 2) / n)]
def bump_coverage(theta, n, level, trials, seed):
    rng = random.Random(seed)
    res = []
    for _ in range(trials):
        d = []
        for _ in range(n):
            d.append(theta * rng.random())
        lo, hi = bump_interval(d, level)
        res.append(lo < theta < hi)
    return sum(res) / len(res)
'''
f, _ = summary(w, logs_v, "variant: logs, list return, strict inequality", "all"); check("log variant passes", f == [])
plants = [
    ("shortest interval [M, M/a^(1/n)]", [("return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)", "return m, m / a ** (1 / n)")]),
    ("a not halved", [("return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)", "return m / (1 - a) ** (1 / n), m / a ** (1 / n)")]),
    ("power n not 1/n", [("return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)", "return m / (1 - a / 2) ** n, m / (a / 2) ** n")]),
    ("last delay not the largest", [("m = max(delays)", "m = delays[-1]")]),
    ("ends swapped", [("return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)", "return m / (a / 2) ** (1 / n), m / (1 - a / 2) ** (1 / n)")]),
    ("reseeded each trial", [("    for _ in range(trials):\n", "    for _ in range(trials):\n        rng = random.Random(seed)\n")]),
    ("count returned, not share", [("return hits / trials", "return hits")]),
    ("delays on [0, 1) not [0, theta)", [("theta * rng.random()", "rng.random()")]),
    ("level used as the tail chance", [("a = 1 - level", "a = level")]),
]
for name, pairs in plants:
    f, _ = summary(w, patched(sol, *pairs), "plant: " + name)
    check("plant caught: " + name, len(f) > 0)
# normal approximation (x bar +- z s / sqrt n, theta = 2 x bar): a plausible slip
norm = r'''
import random, statistics, math
def bump_interval(delays, level):
    n = len(delays); m = statistics.fmean(delays)
    s = statistics.stdev(delays) if n > 1 else 0.0
    z = statistics.NormalDist().inv_cdf(0.5 + level / 2)
    return 2 * (m - z * s / math.sqrt(n)), 2 * (m + z * s / math.sqrt(n))
def bump_coverage(theta, n, level, trials, seed):
    rng = random.Random(seed); h = 0
    for _ in range(trials):
        lo, hi = bump_interval([theta * rng.random() for _ in range(n)], level); h += lo <= theta <= hi
    return h / trials
'''
f, _ = summary(w, norm, "plant: normal approximation on 2 x bar"); check("plant caught: normal approximation", len(f) > 0)

# replay margins: the closest endpoint to theta in the two exact-replay tests (an equivalent formula never flips a trial)
def margins(theta, n, level, trials, seed):
    rng = random.Random(seed); a = 1 - level; best = 1.0; hits = 0
    for _ in range(trials):
        d = [theta * rng.random() for _ in range(n)]; m = max(d)
        lo, hi = m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)
        best = min(best, abs(lo - theta) / theta, abs(hi - theta) / theta); hits += lo <= theta <= hi
    return hits / trials, best
for args, want in (((10.0, 5, 0.95, 2000, 1), 0.947), ((250.0, 20, 0.9, 1500, 11), 0.9026666666666666)):
    share, best = margins(*args)
    print(f"  replay {args}: share {share}, closest endpoint {best:.2e} of theta")
    check(f"replay {args} = {want}, margin over 1e-9", share == want and best > 1e-9)
for args, lv, tol in (((3.0, 2, 0.8, 5000, 7), 0.8, 0.02), ((1.0, 1, 0.5, 4000, 3), 0.5, 0.03)):
    share, _ = margins(*args)
    sd = math.sqrt(lv * (1 - lv) / args[3])
    print(f"  tolerance test {args}: share {share}, off by {abs(share - lv):.4f} = {abs(share - lv) / sd:.2f} sd; tolerance {tol} = {tol / sd:.2f} sd")
    check(f"tolerance test {args} passes with room", abs(share - lv) < tol / 2)
# other seeds: how often a correct but differently ordered draw would miss the tolerance (exact binomial)
for n_tr, lv, tol in ((5000, 0.8, 0.02), (4000, 0.5, 0.03)):
    from scipy import stats as _st
    ks = range(n_tr + 1)
    p_out = sum(_st.binom.pmf(k, n_tr, lv) for k in ks if not abs(k / n_tr - lv) < tol)  # the test needs abs(share - level) < tol
    print(f"  {n_tr} trials at level {lv}: chance a fresh seed misses +-{tol}: {p_out:.1e}")
    check("fresh-seed miss chance under 1e-3", p_out < 1e-3)
# test values by a second route (exact law): lo, hi for test 2 and test 3
check("one delay 4.0 at 95%: 4/0.975 and 4/0.025", abs(4 / 0.975 - 4.102564102564103) < 1e-12 and abs(4 / 0.025 - 160) < 1e-9)
d = [(7 * k) % 50 + 0.5 for k in range(50)]
check("test 4 data: max 49.5, 50 values", max(d) == 49.5 and len(d) == 50)
check("test 4 ends", abs(49.5 / 0.995 ** (1 / 50) - 49.50496266515682) < 1e-9 and abs(49.5 / 0.005 ** (1 / 50) - 55.03333083744145) < 1e-9)
# exact coverage by integration: P(lo <= theta <= hi) = P(a/2 <= (M/theta)^n <= 1 - a/2) = 1 - a
for n, lv in ((1, 0.5), (2, 0.8), (5, 0.95), (20, 0.9)):
    a = 1 - lv
    cov = integrate.quad(lambda u: n * u ** (n - 1), (a / 2) ** (1 / n), (1 - a / 2) ** (1 / n))[0]
    check(f"exact coverage n={n} level={lv}", abs(cov - lv) < 1e-9)
print("failures:", bad)
sys.exit(1 if bad else 0)
