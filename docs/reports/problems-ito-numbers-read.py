"""Second reader's recompute of ito problems-1 to -3 (review-problems-ito-1-3.md).

Imports nothing from the author's script. Every key, every `wrong` value and
the printed working are rebuilt here from the prose. Phi comes from erfc and,
as a second route, from Simpson's rule on the density; lognormal chances are
also checked by seeded simulation; Ito coefficients by sympy; path sums in
exact fractions. No root finder is used, so nothing depends on a SciPy build.

Exit code is always 0 (CI runs every script in docs/reports). A failing check
prints a line starting FINDING. Lines starting PROPOSED give the numbers of the
review's fixes.

Run: <scratch>/venv/bin/python docs/reports/problems-ito-numbers-read.py
"""
import json
import math
import os
from fractions import Fraction as F

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "app", "content", "courses", "ito")
SETS = {n: json.load(open(os.path.join(BASE, f"problems-{n}.json"), encoding="utf-8")) for n in (1, 2, 3)}

checks = 0
findings = 0


def check(ok, label, detail=""):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print(f"FINDING {label} {detail}")


def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def Phi_simpson(z, n=20000):
    """Second route: Simpson's rule on the density from -12 to z."""
    a = -12.0
    h = (z - a) / n
    s = 0.0
    for i in range(n + 1):
        x = a + i * h
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * math.exp(-0.5 * x * x)
    return s * h / 3 / math.sqrt(2 * math.pi)


for zz in (-1.118034, -0.6471, -0.4188, 0.8772, 0.9196, -0.1323):
    check(abs(Phi(zz) - Phi_simpson(zz)) < 1e-9, "Phi two routes", str(zz))


def part(n, i, k):
    return SETS[n]["items"][i]["parts"][k]


def widget(n, i, k):
    return part(n, i, k)["widget"]


def numeric(n, i, k, mine, wrongs, forms=(), table_z=None, tails=1.0, label=""):
    """mine: reader's key. wrongs: {id: reader's value}. forms: entries a learner
    following the stated form types (rounded key, rounded-route values).
    table_z: for a part that names a normal table, the exact z; the reading at z
    to 2 places must fall in the key band. tails: factor applied to the tail."""
    w = widget(n, i, k)
    tag = f"problems-{n} {SETS[n]['items'][i]['id']} part {k + 1} {label}"
    key, tol = w["answer"], w["tol"]["abs"]
    check(abs(key - mine) <= max(5e-7 * max(1.0, abs(mine)) + 6e-7, tol / 100), tag + "key", f"json {key} reader {mine}")
    for v in forms:
        check(abs(v - key) <= tol, tag + "form refused", f"{v} against {key} +- {tol}")
    got = {x["id"]: x for x in w.get("wrong", [])}
    check(set(got) == set(wrongs), tag + "wrong ids", f"{sorted(got)} against {sorted(wrongs)}")
    for wid, val in wrongs.items():
        if wid not in got:
            continue
        x = got[wid]
        check(abs(x["value"] - val) <= x["tol"]["abs"], tag + f"wrong {wid}", f"json {x['value']} reader {val}")
        check(abs(x["value"] - key) > tol + x["tol"]["abs"], tag + f"wrong {wid} overlaps key")
    vals = sorted((x["value"], x["tol"]["abs"]) for x in got.values())
    for (a, ta), (b, tb) in zip(vals, vals[1:]):
        check(b - a > ta + tb, tag + "two wrong bands overlap", f"{a} {b}")
    if table_z is not None:
        zr = round(table_z, 2)
        reading = round(Phi(zr), 4)
        value = round(tails * reading if tails == 1.0 else tails * round(1 - Phi(abs(zr)), 4), 4)
        check(abs(value - key) <= tol, tag + "table reading refused",
              f"z = {zr} gives {value}, band {key} +- {tol}")


rng = np.random.default_rng(20261117)
ZN = rng.standard_normal(2_000_000)


def mc_below(level, start, logmean, sd):
    x = start * np.exp(logmean + sd * ZN)
    p = float(np.mean(x < level))
    return p, math.sqrt(p * (1 - p) / len(ZN))


# ---------------------------------------------------------------- problems-1
# p-maker-tally (fix pass: win chance 0.507, review finding 1)
n_tr, size, pw = 625, 40, F(507, 1000)
mean_tr = size * pw - size * (1 - pw)
day = n_tr * mean_tr
check(mean_tr == F(14, 25) and day == 350, "maker mean")
# second route: the binomial law of the 625 trades, summed exactly
pmf = [F(math.comb(n_tr, j)) * pw ** j * (1 - pw) ** (n_tr - j) for j in range(n_tr + 1)]
check(sum(p * (2 * j - n_tr) * size for j, p in enumerate(pmf)) == 350, "maker mean by the binomial law")
var_day = sum(p * ((2 * j - n_tr) * size) ** 2 for j, p in enumerate(pmf)) - 350 ** 2
check(var_day == 999804, "maker day variance", str(var_day))
numeric(1, 0, 0, 350, {"wins-only": 625 * 40 * 0.507, "half-edge": 175, "per-trade-count": 625 * 0.014}, forms=[350])
numeric(1, 0, 1, 625 * 1600, {"variance": 999804, "abs-sum": 625 * 40}, forms=[1000000])
sd_week = 1000 * math.sqrt(5)
numeric(1, 0, 2, sd_week, {"sd-times-t": 5000, "one-day": 1000}, forms=[2236])
z = -1750 / 2236.07
check(abs(z - (-0.7826)) < 5e-5, "maker z printed")
numeric(1, 0, 3, Phi(-1750 / sd_week),
        {"sd-times-t": Phi(-0.35), "no-drift": 0.5, "ends-up": 1 - Phi(z), "one-day": Phi(-1.75)},
        forms=[round(Phi(z), 4)])
check("table" not in part(1, 0, 3)["question"], "maker part 4 names no table")
# reuse: homework-1 h-drift-below runs X = 0.5t + W; the drift over sigma here, read from the set, must differ
ratio = widget(1, 0, 0)["answer"] / 1000
check(abs(ratio - 0.5) > 1e-12, "maker reuse",
      "drift over sigma is 0.5, the process of homework-1 h-drift-below scaled by 1,000")

# p-quarter-rally
mu, sg, s0, s_q, left = 0.13, 0.35, 45.0, 52.0, 0.75
sd_left = sg * math.sqrt(left)
numeric(1, 1, 0, sd_left, {"full-year": 0.35, "variance": sg ** 2 * left, "past-quarter": sg * math.sqrt(0.25)},
        forms=[round(sd_left, 4)])
ld = (mu - sg ** 2 / 2) * left
check(abs(ld - 0.0515625) < 1e-12, "rally log drift")
median = s_q * math.exp(ld)
mean = s_q * math.exp(mu * left)
numeric(1, 1, 1, median, {"mean": mean, "from-start": s0 * math.exp(mu - sg ** 2 / 2),
                          "whole-year": s_q * math.exp(mu - sg ** 2 / 2)}, forms=[round(median, 2)])
check(abs(median * math.exp(sg ** 2 * left / 2) - mean) < 1e-9, "rally mean two routes")
numeric(1, 1, 2, mean, {"median": median, "full-factor": median * math.exp(sg ** 2 * left),
                        "full-year": s_q * math.exp(mu)}, forms=[round(mean, 2)])
zr = (math.log(45 / 52) - 0.0515625) / 0.3031
check(abs(zr - (-0.6471)) < 5e-5, "rally z printed", str(zr))
p_exact = Phi((math.log(45 / 52) - ld) / sd_left)
numeric(1, 1, 3, p_exact,
        {"full-year-sd": Phi((math.log(45 / 52) - ld) / 0.35), "no-rally": Phi(-(mu - sg ** 2 / 2) / sg),
         "upper": 1 - p_exact}, forms=[round(Phi(zr), 4)])
p_mc, se = mc_below(45, 52, ld, sd_left)
check(abs(p_mc - p_exact) < 4 * se, "rally chance by simulation", f"{p_mc} {p_exact}")
m_mc = float(np.mean(52 * np.exp(ld + sd_left * ZN)))
check(abs(m_mc - mean) < 0.05, "rally mean by simulation", str(m_mc))

# p-realised-then-risk
qv, T, m, S, K, mu = 0.0147, F(1, 3), 84, 64.0, 60.0, 0.09
s2 = qv / float(T)
check(F(84, 252) == T and abs(s2 - 0.0441) < 1e-15, "realised sigma squared")
numeric(1, 2, 0, math.sqrt(s2), {"not-annual": math.sqrt(qv), "variance": s2, "times-days": math.sqrt(qv * 252)},
        forms=[0.21])
sd_hat = s2 * math.sqrt(2 / m)
# second route: variance of the sum of m squared N(0, s2 T/m) returns, then divide by T
var_sum = m * 2 * (s2 * float(T) / m) ** 2
check(abs(math.sqrt(var_sum) / float(T) - sd_hat) < 1e-15, "realised sd two routes")
numeric(1, 2, 1, sd_hat, {"no-sigma": math.sqrt(2 / m), "sum-not-rate": math.sqrt(var_sum), "variance": 2 * s2 ** 2 / m},
        forms=[0.006805])


def below60(sig2, drift_sig2=None):
    d2 = sig2 if drift_sig2 is None else drift_sig2
    return (math.log(K / S) - (mu - d2 / 2)) / math.sqrt(sig2)


z3 = below60(0.0441)
check(abs(z3 - (-0.6309)) < 5e-5, "realised z printed", str(z3))
numeric(1, 2, 2, Phi(z3),
        {"no-drag": Phi((math.log(K / S) - mu) / 0.21), "upper": 1 - Phi(z3),
         "not-annual": Phi((math.log(K / S) - (mu - qv / 2)) / math.sqrt(qv))},
        forms=[round(Phi(-0.6309), 4)], table_z=z3)
p_mc, se = mc_below(60, 64, mu - 0.0441 / 2, 0.21)
check(abs(p_mc - Phi(z3)) < 4 * se, "realised chance by simulation")
s2_hi = 0.0441 + 2 * 0.006805
check(abs(s2_hi - 0.05771) < 1e-12, "stressed sigma squared")
z4 = below60(s2_hi)
check(abs(z4 - (-0.5232)) < 5e-5 and abs(math.sqrt(s2_hi) - 0.2402) < 5e-5, "stressed z printed", str(z4))
numeric(1, 2, 3, Phi(below60(0.0441 + 2 * sd_hat)),
        {"unchanged": Phi(z3), "sd-on-sigma": Phi(below60((0.21 + 2 * 0.006805) ** 2)),
         "same-drift": Phi(below60(s2_hi, 0.0441))},
        forms=[round(Phi(z4), 4), round(Phi((math.log(K / S) - 0.06115) / 0.2402), 4)])

# ---------------------------------------------------------------- problems-2
# p-cable-inverse
x, mu_s, sg_s, t = sp.symbols("x mu sigma t", positive=True)
f = 1 / x
drift = sp.simplify((mu_s * x * sp.diff(f, x) + sp.Rational(1, 2) * sg_s ** 2 * x ** 2 * sp.diff(f, x, 2)) / f)
check(sp.simplify(drift - (sg_s ** 2 - mu_s)) == 0, "cable drift", str(drift))
check(sp.simplify(sg_s * x * sp.diff(f, x) / f + sg_s) == 0, "cable noise sign")
w = widget(2, 0, 0)
check(w["answer"].replace(" ", "") == "\\sigma^2-\\mu", "cable expression key", w["answer"])
check({x_["tex"] for x_ in w["wrong"]} == {"-\\mu", "\\frac{1}{2}\\sigma^2-\\mu", "\\mu-\\sigma^2"}, "cable expression wrongs")
mu, sg, X0, T = 0.02, 0.12, 1.25, 3
EY = 0.8 * math.exp(T * (sg ** 2 - mu))
# second route: the lognormal moment E[X^-1] = X0^-1 exp(-m + v/2)
check(abs(math.exp(-(mu - sg ** 2 / 2) * T + sg ** 2 * T / 2) / X0 - EY) < 1e-15, "cable mean two routes")
y_mc = float(np.mean(1 / (X0 * np.exp((mu - sg ** 2 / 2) * T + sg * math.sqrt(T) * ZN))))
check(abs(y_mc - EY) < 5e-4, "cable mean by simulation", str(y_mc))
med_y = 0.8 * math.exp(-(mu - sg ** 2 / 2) * T)
numeric(2, 0, 1, EY, {"inverse-mean": 1 / (X0 * math.exp(mu * T)), "median": med_y}, forms=[round(EY, 4)])
EX = X0 * math.exp(mu * T)
numeric(2, 0, 2, math.exp(T * sg ** 2), {"one": 1, "median-y": EX * med_y}, forms=[round(EX * EY, 4)])
numeric(2, 0, 3, sg ** 2, {"log-flat": sg ** 2 / 2, "zero": 0, "sigma": sg}, forms=[0.0144])
check(widget(2, 0, 3).get("unit") == "%", "cable percentage unit")

# p-cube-path
W = [F(0), F(3, 10), F(-2, 10), F(4, 10), F(6, 10)]
dW = [b - a for a, b in zip(W, W[1:])]
left = sum(a * a * d for a, d in zip(W, dW))
right = sum(b * b * d for b, d in zip(W[1:], dW))
cubes = sum(d ** 3 for d in dW)
mid = sum(a * d * d for a, d in zip(W, dW))
check(dW == [F(3, 10), F(-1, 2), F(3, 5), F(1, 5)], "cube moves")
check(W[-1] ** 3 == 3 * left + 3 * mid + cubes == F(216, 1000), "cube identity on the path")
check(cubes == F(126, 1000), "cube sum of cubes")
numeric(2, 1, 0, float(left), {"right-point": float(right), "ordinary": float(W[-1] ** 3 / 3),
                               "no-square": float(sum(a * d for a, d in zip(W, dW)))}, forms=[0.011])
numeric(2, 1, 1, float(mid), {"no-third": float(W[-1] ** 3 - 3 * left - cubes),
                              "no-cube": float((W[-1] ** 3 - 3 * left) / 3)}, forms=[0.019])
opts = {o["id"]: o for o in widget(2, 1, 2)["options"]}
check(opts["time-integral"].get("correct") is True and sum(1 for o in opts.values() if o.get("correct")) == 1, "cube choice key")
# the limit, by simulation on a fine grid: sum W (dW)^2 against sum W dt
g = np.random.default_rng(5).standard_normal((2000, 2000)) * math.sqrt(1 / 2000)
Wg = np.cumsum(g, axis=1) - g
gap = np.sum(Wg * g * g, axis=1) - np.sum(Wg, axis=1) / 2000
check(float(np.sqrt(np.mean(gap ** 2))) < 0.03, "cube limit by simulation", str(float(np.sqrt(np.mean(gap ** 2)))))
wv = sp.symbols("w")
check(sp.Rational(1, 2) * sp.diff(wv ** 3, wv, 2) == 3 * wv, "cube Ito coefficient")
w4 = widget(2, 1, 3)
check(w4["answer"] == "3w" and {x_["tex"] for x_ in w4["wrong"]} == {"6w", "0", "3w^2"}, "cube expression key and wrongs")
check("3\\int_0^1 W\\,dt" not in part(2, 1, 3)["question"], "cube part 4 passable backwards",
      "the question prints W_1^3 = 3 int W^2 dW + 3 int W dt and then asks for the dt coefficient 3w")

# p-results-vol
v = 0.4 ** 2 * 0.25 + 0.15 ** 2 * 0.75
grid = (np.arange(400000) + 0.5) / 400000
check(abs(float(np.mean(np.where(grid < 0.25, 0.4, 0.15) ** 2)) - v) < 1e-9, "results variance by midpoint rule")
avg = 0.4 * 0.25 + 0.15 * 0.75
numeric(2, 2, 0, v, {"average-first": avg ** 2, "no-weights": 0.16 + 0.0225, "not-squared": avg}, forms=[0.0569])
numeric(2, 2, 1, math.sqrt(v), {"time-average": avg, "plain-average": 0.275, "variance": v}, forms=[0.2385])
check(widget(2, 2, 1).get("unit") == "%", "results percentage unit")
lm = 0.06 - v / 2
check(abs(lm - 0.0315625) < 1e-12, "results log mean")
med = 72 * math.exp(lm)
numeric(2, 2, 2, med, {"mean": 72 * math.exp(0.06), "average-vol": 72 * math.exp(0.06 - avg ** 2 / 2),
                       "full-variance": 72 * math.exp(0.06 - v)}, forms=[round(med, 2)])
zv = -0.0315625 / 0.2385
check(abs(zv - (-0.1323)) < 5e-5, "results z printed", str(zv))
numeric(2, 2, 3, Phi(-lm / math.sqrt(v)),
        {"average-vol": Phi(-(0.06 - avg ** 2 / 2) / avg), "no-drag": Phi(-0.06 / 0.2385), "upper": 1 - Phi(zv)},
        forms=[round(Phi(zv), 4)], table_z=zv)
# simulate the two stretches separately
r2 = np.random.default_rng(9)
noise = 0.4 * math.sqrt(0.25) * r2.standard_normal(1_000_000) + 0.15 * math.sqrt(0.75) * r2.standard_normal(1_000_000)
p_mc = float(np.mean(lm + noise < 0))
check(abs(p_mc - Phi(-lm / math.sqrt(v))) < 4 * math.sqrt(0.25 / 1_000_000), "results chance by simulation", str(p_mc))

# ---------------------------------------------------------------- problems-3
# p-touch-note
r, sg, B, S = 0.04, 0.25, 75.0, 100.0
a_s = sp.symbols("a")
res = sp.expand((sp.Rational(1, 2) * sp.Rational(1, 16) * a_s * (a_s - 1) + sp.Rational(1, 25) * a_s - sp.Rational(1, 25)))
roots = sorted(sp.solve(res, a_s))
check(roots == [sp.Rational(-32, 25), 1], "touch roots", str(roots))
w = widget(3, 0, 0)
check(sorted(w["answers"]) == [-1.28, 1] and w.get("unordered") is True, "touch roots key")
check({x_["id"]: x_["value"] for x_ in w["wrong"]} == {"sign": "1, 1.28", "no-half": "1, -0.64"}, "touch roots wrongs")
# second route: the Laplace transform of the first passage of the log price to ln(80/100)
nu = r - sg ** 2 / 2
lam = (nu + math.sqrt(nu ** 2 + 2 * r * sg ** 2)) / sg ** 2
check(abs(lam - 1.28) < 1e-12, "touch exponent by the first-passage transform", str(lam))
V = (S / B) ** -1.28
check(abs(math.exp(-lam * math.log(S / B)) - V) < 1e-15, "touch value two routes")
opts = {o["id"]: o for o in widget(3, 0, 1)["options"]}
check(opts["negative-power"].get("correct") is True and sum(1 for o in opts.values() if o.get("correct")) == 1, "touch choice key")
numeric(3, 0, 2, V, {"sign": (S / B) ** 1.28, "no-half": (S / B) ** -0.64, "root-one": S / B}, forms=[round(V, 4)])
h = 1e-4
delta = ((S + h) / B) ** -1.28 - ((S - h) / B) ** -1.28
delta /= 2 * h
check(abs(delta - (-1.28 * V / S)) < 1e-9, "touch delta by central difference")
numeric(3, 0, 3, 10000 * delta, {"sign": -10000 * delta, "no-power": -10000 * V / S},
        forms=[-88.6, round(-1.28 * 0.6920 * 100, 1)])

# p-digital-measures and p-one-touch were re-authored in the fix pass (review findings 11 and 12);
# their checks are removed. The new p-twin-shares and p-bridge-closes are checked by the author script
# and read next by the delta reader.

# ------------------------------------------------------------ set shape
for n in (1, 2, 3):
    d = SETS[n]
    check(3 <= len(d["items"]) <= 5, f"problems-{n} item count")
    check(max(it["difficulty"] for it in d["items"]) == 5, f"problems-{n} has a 5")
    for it in d["items"]:
        check(3 <= len(it["parts"]) <= 5, f"{it['id']} part count")
        check(3 <= it["difficulty"] <= 5, f"{it['id']} difficulty")
    kinds = [p["widget"]["kind"] for it in d["items"] for p in it["parts"]]
    check(sum(k in ("numeric", "expression") for k in kinds) * 3 >= 2 * len(kinds), f"problems-{n} typed share")

# ------------------------------------------------------------ the review's fixes
# Findings 1, 4 and 10 are applied; their numbers are now checked above as keys and bands.
check(widget(2, 2, 3)["tol"]["abs"] >= abs(round(Phi(-0.13), 4) - Phi(-lm / math.sqrt(v))), "results-vol table band")

print(f"{checks} checks, {findings} FINDING line(s)")
