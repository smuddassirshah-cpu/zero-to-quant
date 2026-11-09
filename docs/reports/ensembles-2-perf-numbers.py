"""Numbers in ensembles homework-2 item hw-floor-derive (performance task, L2).

Every stated number is computed by the closed form in exact fractions, again by
the covariance matrix 1'S1/B^2, and by a seeded simulation of equicorrelated
forecasts. The rubric's passing tick sets are enumerated. Run from anywhere:
    python3 docs/reports/ensembles-2-perf-numbers.py
Needs NumPy. Exits 0 when every check passes.
"""
import itertools
import json
import os
import re
import sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, "..", "..", "app", "content", "courses", "ensembles", "homework-2.json")
hw = json.load(open(HW, encoding="utf-8"))
item = next(i for i in hw["items"] if i["id"] == "hw-floor-derive")
w = item["widget"]
text = w["prompt"] + "\n" + w["model"] + "\n" + " ".join(r["text"] for r in w["rubric"]) + "\n" + item["explain"]["text"]
fails = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


def shown(s):
    check(f"'{s}' appears in the item", s in text)


# ---- inputs --------------------------------------------------------------
S1, R1 = F(40), F(1, 5)      # first forest: variance 40 bp^2, correlation 0.2
S2, R2 = F(50), F(2, 25)     # second forest: variance 50 bp^2, correlation 0.08
for s in ["40 bp²", "correlation 0.2", "100 trees", "1,000", "50 bp²", "correlation 0.08"]:
    shown(s)


def closed(s2, r, B):
    return r * s2 + (1 - r) * s2 / B


def matrix(s2, r, B):
    S = float(s2) * ((1 - float(r)) * np.eye(B) + float(r) * np.ones((B, B)))
    one = np.ones(B)
    return one @ S @ one / B ** 2


# ---- route A (exact) against route B (matrix) -----------------------------
for s2, r in [(S1, R1), (S2, R2)]:
    for B in [1, 3, 4, 100, 1000]:
        a, b = closed(s2, r, B), matrix(s2, r, B)
        check(f"closed form = matrix, s2={s2}, rho={r}, B={B}: {float(a):.6f}", abs(float(a) - b) < 1e-9)

# stated values, exact
check("floor 1 = 8", R1 * S1 == 8)
check("(1-rho)s2 = 32", (1 - R1) * S1 == 32)
check("Var at 100 = 8.32", closed(S1, R1, 100) == F(832, 100))
check("Var at 1000 = 8.032", closed(S1, R1, 1000) == F(8032, 1000))
check("drop = 0.288", closed(S1, R1, 100) - closed(S1, R1, 1000) == F(288, 1000))
pct = (closed(S1, R1, 100) - closed(S1, R1, 1000)) / closed(S1, R1, 100)
check(f"drop about 3.5% ({float(pct):.4%})", round(float(pct) * 100, 1) == 3.5)
check("tenfold target 0.832", closed(S1, R1, 100) / 10 == F(832, 1000))
check("0.832 below the floor 8", F(832, 1000) < R1 * S1)
check("floor 2 = 4", R2 * S2 == 4)
check("(1-rho)s2 = 46", (1 - R2) * S2 == 46)
check("forest 2 at 1000 = 4.046", closed(S2, R2, 1000) == F(4046, 1000))
check("gap at 1000 = 3.986", closed(S1, R1, 1000) - closed(S2, R2, 1000) == F(3986, 1000))
check("crossing B = 14/4 = 3.5", (F(46) - F(32)) / (F(8) - F(4)) == F(7, 2))
v13, v23 = closed(S1, R1, 3), closed(S2, R2, 3)
v14, v24 = closed(S1, R1, 4), closed(S2, R2, 4)
check(f"B=3: forest 2 {float(v23):.2f} > forest 1 {float(v13):.2f}", round(float(v23), 2) == 19.33 and round(float(v13), 2) == 18.67 and v23 > v13)
check("B=4: forest 2 15.5 < forest 1 16", v24 == F(31, 2) and v14 == 16)
first_win = next(B for B in range(1, 10000) if closed(S2, R2, B) < closed(S1, R1, B))
check(f"first B where forest 2 wins = {first_win}", first_win == 4)
check("forest 2 wins for every B from 4 to 100000", all(closed(S2, R2, B) < closed(S1, R1, B) for B in range(4, 100001, 97)))
# limit: exact decrease to the floor, staying above it
seq = [closed(S1, R1, B) for B in [1, 10, 100, 10 ** 4, 10 ** 8]]
check("variance decreases in B and stays above the floor", all(x > y for x, y in zip(seq, seq[1:])) and all(x > 8 for x in seq))
check("gap to floor at B = 1e8 is 32e-8", seq[-1] - 8 == F(32, 10 ** 8))
# ends
for s2, r in [(S1, R1), (S2, R2)]:
    check("B=1 gives sigma^2", closed(s2, r, 1) == s2)
    check("rho=0 gives sigma^2/B", closed(s2, 0, 7) == s2 / 7)
    check("rho=1 gives sigma^2 for every B", all(closed(s2, 1, B) == s2 for B in [1, 5, 1000]))
for s in ["8.32", "8.032", "0.288", "3.5%", "0.832", "4.046", "3.986", "B > 3.5", "19.33", "18.67", "15.5", "4 trees on",
          "0.2 \\times 40 = 8", "0.08 \\times 50 = 4", "= 32", "= 46"]:
    shown(s)

# ---- route C: seeded simulation --------------------------------------------
# X_b = mu + sigma (sqrt(rho) Z + sqrt(1 - rho) E_b): identically distributed,
# variance sigma^2, every pair correlation rho, not independent.
rng = np.random.default_rng(20261109)


def sim_avg(s2, r, B, reps, mu=0.0, chunk=4000, z=None, e=None):
    out = []
    done = 0
    while done < reps:
        n = min(chunk, reps - done)
        Z = rng.standard_normal(n)
        E = rng.standard_normal((n, B))
        X = mu + np.sqrt(float(s2)) * (np.sqrt(float(r)) * Z[:, None] + np.sqrt(1 - float(r)) * E)
        out.append(X.mean(axis=1))
        done += n
    return np.concatenate(out)


def near(name, est_sample, target, k=4.0):
    v = est_sample.var(ddof=1)
    se = v * np.sqrt(2.0 / (len(est_sample) - 1))
    check(f"sim {name}: {v:.4f} vs {float(target):.4f} (se {se:.4f})", abs(v - float(target)) < k * se)
    return v, se


# pairwise covariance and single variance
Z = rng.standard_normal(400000)
E = rng.standard_normal((400000, 2))
X = np.sqrt(40) * (np.sqrt(0.2) * Z[:, None] + np.sqrt(0.8) * E)
c = np.cov(X.T)
check(f"sim single variance {c[0,0]:.3f} near 40", abs(c[0, 0] - 40) < 0.5)
check(f"sim pair covariance {c[0,1]:.3f} near rho*s2 = 8", abs(c[0, 1] - 8) < 0.3)
check(f"sim pair correlation {c[0,1]/np.sqrt(c[0,0]*c[1,1]):.4f} near 0.2", abs(c[0, 1] / np.sqrt(c[0, 0] * c[1, 1]) - 0.2) < 0.01)

v100, se100 = near("forest 1, B=100", sim_avg(S1, R1, 100, 200000), closed(S1, R1, 100))
v1000, se1000 = near("forest 1, B=1000", sim_avg(S1, R1, 1000, 100000), closed(S1, R1, 1000))
check(f"sim: B=1000 well below tenfold claim 0.832 (est {v1000:.3f})", v1000 > 7.5)
check("sim: drop from 100 to 1000 trees is small, under 8%", (v100 - v1000) / v100 < 0.08)
vlim, selim = near("forest 1, B=10000 (limit)", sim_avg(S1, R1, 10000, 10000, chunk=500), 8)
near("forest 2, B=1000", sim_avg(S2, R2, 1000, 100000), closed(S2, R2, 1000))

# crossing: common random numbers for the two forests at B = 3 and B = 4
for B, first_better in [(3, True), (4, False)]:
    n = 2_000_000
    Z = rng.standard_normal(n)
    E = rng.standard_normal((n, B)).mean(axis=1)
    a1 = np.sqrt(40) * (np.sqrt(0.2) * Z + np.sqrt(0.8) * E)
    a2 = np.sqrt(50) * (np.sqrt(0.08) * Z + np.sqrt(0.92) * E)
    d = a1 ** 2 - a2 ** 2  # mean zero, so E[a^2] is the variance
    se = d.std(ddof=1) / np.sqrt(n)
    check(f"sim B={B}: var1 {a1.var():.3f} (closed {float(closed(S1,R1,B)):.3f}), var2 {a2.var():.3f} (closed {float(closed(S2,R2,B)):.3f})",
          abs(a1.var() - float(closed(S1, R1, B))) < 0.1 and abs(a2.var() - float(closed(S2, R2, B))) < 0.1)
    check(f"sim B={B}: forest 1 better is {first_better} (diff {d.mean():.3f}, se {se:.3f})",
          (d.mean() < -4 * se) if first_better else (d.mean() > 4 * se))

# bias: averaging keeps the mean; MSE = bias^2 + var
mu, f = 1.5, 0.5
avg = sim_avg(S1, R1, 100, 200000, mu=mu)
check(f"sim mean of average {avg.mean():.4f} near tree mean 1.5", abs(avg.mean() - mu) < 4 * np.sqrt(8.32 / len(avg)))
mse = ((avg - f) ** 2).mean()
check(f"sim MSE {mse:.4f} near bias^2 + var = {1 + 8.32}", abs(mse - (1 + 8.32)) < 0.1)

# ---- rubric ---------------------------------------------------------------
rub = w["rubric"]
pts = [r["points"] for r in rub]
req = [bool(r.get("required")) for r in rub]
check("rubric sums to 10", sum(pts) == 10)
check("3 to 5 rows", 3 <= len(rub) <= 5)
check("not every row required", not all(req))
passes = [s for k in range(len(rub) + 1) for s in itertools.combinations(range(len(rub)), k)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
for s in passes:
    print("     pass:", [i + 1 for i in s], sum(pts[i] for i in s))
named = {0: "assumptions", 1: "derivation", 2: "limit and colleague", 3: "second forest"}
for i, nm in named.items():
    check(f"no pass skips row {i + 1} ({nm})", all(i in s for s in passes))

# ---- homework shape -------------------------------------------------------
items = hw["items"]
check(f"homework holds {len(items)} items, 6 to 12", 6 <= len(items) <= 12)
check("one performance item", sum(1 for i in items if i.get("performance")) == 1)
check("a difficulty 5 item", any(i.get("difficulty") == 5 for i in items))
check("difficulties 3 to 5", all(3 <= i.get("difficulty", 0) <= 5 for i in items))
check("no em or en dash, no exclamation", not re.search("[–—!]", json.dumps(item, ensure_ascii=False)))

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
