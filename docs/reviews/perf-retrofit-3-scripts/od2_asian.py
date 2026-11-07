"""opt-dash L2 h-asian-cv: shipped solution, starter, a reader solution by another route, reader-planted bugs,
and the item's numbers (6.156, 97.74, 0.0604, 0.0245, six times) by a second route."""
import sys, math
import numpy as np
from harness import item, summary, run

w = item("opt-dash", "homework-2.json", "h-asian-cv")["widget"]
base = w["solution"]

READER = '''
import math
import numpy as np
def asian_cv(S, K, r, sigma, T, n_fix, n_paths, seed, q=0.0):
    if n_paths < 2:
        raise ValueError("two paths at least")
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, n_fix))
    dt = T / n_fix
    disc = math.exp(-r * T)
    ys, xs = [], []
    for row in z:                          # path by path, price multiplied step by step
        s, tot = S, 0.0
        for e in row:
            s *= math.exp((r - q - 0.5 * sigma * sigma) * dt + sigma * math.sqrt(dt) * e)
            tot += s
        a = tot / n_fix
        ys.append(disc * max(a - K, 0.0)); xs.append(disc * a)
    y, x = np.array(ys), np.array(xs)
    g = math.exp((r - q) * dt)              # E[X] as a geometric sum of forwards
    ex = disc * S * g * (g ** n_fix - 1) / (g - 1) / n_fix if g != 1 else disc * S
    b = np.polyfit(x, y, 1)[0]              # weight as the least-squares slope
    adj = y - b * (x - ex)
    return float(adj.mean()), float(np.std(adj, ddof=1) / math.sqrt(n_paths))
'''

BUGS = {
    "weight fixed at 1": base.replace("b = np.cov(y, x)[0, 1] / np.var(x, ddof=1)", "b = 1.0"),
    "control mean from the same paths": base.replace("adj = y - b * (x - ex)", "adj = y - b * (x - x.mean())"),
    "Euler steps for the path": base.replace(
        "logs = np.cumsum((r - q - sigma ** 2 / 2) * dt + sigma * sqrt(dt) * z, axis=1)\n    A = S * np.exp(logs).mean(axis=1)",
        "A = S * np.cumprod(1 + (r - q) * dt + sigma * sqrt(dt) * z, axis=1).mean(axis=1)"),
    "q left out of the paths": base.replace("np.cumsum((r - q - sigma", "np.cumsum((r - sigma"),
    "error with ddof=0": base.replace("adj.std(ddof=1)", "adj.std()"),
}
VARIANTS = {
    "weight with mixed ddof (np.var default)": base.replace("np.var(x, ddof=1)", "np.var(x)"),
}
bad = 0
print("opt-dash L2 h-asian-cv")
f, _ = summary(w, base, "shipped solution"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
f, _ = summary(w, READER, "reader path loop, geometric E[X], polyfit weight"); bad += bool(f)
for name, src in VARIANTS.items():
    f, _ = summary(w, src, "variant: " + name); bad += bool(f)
for name, src in BUGS.items():
    assert src != base, name
    f, _ = summary(w, src, "bug: " + name); bad += not f
bad += any(x[0] != "pass" for x in run(w, base, "examples"))

# numbers by a second route
g = {}
exec(w["prelude"], g); exec(base, g)
S, K, r, sig, T, n = 100, 100, 0.05, 0.2, 1.0, 12
t = np.arange(1, n + 1) / n
ex = math.exp(-r * T) * S * np.exp(r * t).mean()
print(f"  E[X] = {ex:.4f} (explain 97.74)"); bad += f"{ex:.2f}" != "97.74"
p, se = g["asian_cv"](S, K, r, sig, T, n, 20_000, 0)
pse = g["plain_asian_se"](S, K, r, sig, T, n, 20_000, 0)
print(f"  se {se:.4f} (0.0245), plain {pse:.4f} (0.0604), ratio^2 {(pse / se) ** 2:.2f} (about six)")
bad += f"{se:.4f}" != "0.0245" or f"{pse:.4f}" != "0.0604" or round((pse / se) ** 2) != 6
# 6.156 by a geometric-average control (exact closed form), 2,000,000 paths
rng = np.random.default_rng(12345)
dt = T / n
tot_y, tot_y2, m = 0.0, 0.0, 0
ys, gs = [], []
for _ in range(10):
    z = rng.standard_normal((200_000, n))
    logs = np.log(S) + np.cumsum((r - sig ** 2 / 2) * dt + sig * math.sqrt(dt) * z, axis=1)
    ys.append(math.exp(-r * T) * np.maximum(np.exp(logs).mean(axis=1) - K, 0))
    gs.append(math.exp(-r * T) * np.maximum(np.exp(logs.mean(axis=1)) - K, 0))
y, gg = np.concatenate(ys), np.concatenate(gs)
mu_g = math.log(S) + (r - sig ** 2 / 2) * t.mean()
var_g = sig ** 2 * sum(min(a, b) for a in t for b in t) / n ** 2
d2 = (mu_g - math.log(K)) / math.sqrt(var_g); d1 = d2 + math.sqrt(var_g)
cdf = lambda v: 0.5 * (1 + math.erf(v / math.sqrt(2)))
geo = math.exp(-r * T) * (math.exp(mu_g + var_g / 2) * cdf(d1) - K * cdf(d2))
bb = np.cov(y, gg)[0, 1] / np.var(gg, ddof=1)
adj = y - bb * (gg - geo)
pr, pe = adj.mean(), adj.std(ddof=1) / math.sqrt(len(adj))
print(f"  arithmetic Asian by geometric control: {pr:.4f} +- {pe:.4f} (test 7 uses 6.156)")
bad += abs(pr - 6.156) > 0.002
print("FAILURES:", bad)
sys.exit(1 if bad else 0)
