"""Second reader's recomputation of garch problems-1 to problems-3.

Run: <scratchpad>/venv/bin/python docs/reports/problems-garch-numbers-read.py
Imports nothing from the author's script. Every key and every `wrong` value is typed here from the
prose and rebuilt, by another route where one exists (a transition matrix, a covariance matrix, a
stepped recursion, a brute search, scipy's binomial and normal, a numeric integral).
Exits 0. A check that fails on the content prints a FINDING line (review-problems-garch-1-3.md).
"""
import json
import math
import os
import re

import numpy as np
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "garch")
SETS = {n: json.load(open(os.path.join(COURSE, f"problems-{n}.json"))) for n in (1, 2, 3)}

n_ok = 0
findings = []


def check(name, cond, detail=""):
    global n_ok
    if cond:
        n_ok += 1
    else:
        findings.append(f"FINDING {name} {detail}")


def close(a, b, tol=None):
    tol = tol if tol is not None else 1e-4 * max(1.0, abs(b))
    return abs(a - b) <= tol


def part(n, i, j):
    return SETS[n]["items"][i]["parts"][j - 1]


def expect(n, i, j, key, wrong, tol=None):
    """key and wrong values (mine) against the file's; then the bands."""
    w = part(n, i, j)["widget"]
    tag = f"problems-{n} items[{i}] part {j}"
    check(f"{tag} key", close(w["answer"], key, tol), f"file {w['answer']} mine {key}")
    ktol = w["tol"]["abs"]
    file_wrong = {x["id"]: x for x in w.get("wrong", [])}
    check(f"{tag} wrong ids", set(file_wrong) == set(wrong), f"file {sorted(file_wrong)} mine {sorted(wrong)}")
    for wid, val in wrong.items():
        if wid not in file_wrong:
            continue
        x = file_wrong[wid]
        check(f"{tag} wrong {wid}", close(x["value"], val, tol), f"file {x['value']} mine {val}")
        # the key band refuses the slip, and the two bands do not meet
        check(f"{tag} wrong {wid} refused", abs(x["value"] - w["answer"]) > ktol + x["tol"]["abs"],
              f"key {w['answer']} +- {ktol}, slip {x['value']} +- {x['tol']['abs']}")
    vals = sorted((x["value"], x["tol"]["abs"]) for x in w.get("wrong", []))
    for (a, ta), (b, tb) in zip(vals, vals[1:]):
        check(f"{tag} slip bands apart", b - a > ta + tb or a == b, f"{a} and {b}")


def takes(n, i, j, typed, why):
    """a value a learner would type (in the widget's own unit) is accepted."""
    w = part(n, i, j)["widget"]
    v = typed / 100 if w.get("unit") == "%" else typed
    check(f"problems-{n} items[{i}] part {j} takes {typed} ({why})", abs(v - w["answer"]) <= w["tol"]["abs"] + 1e-12,
          f"key {w['answer']} tol {w['tol']['abs']}")


R252 = math.sqrt(252)
Z99 = stats.norm.ppf(0.99)
Z95 = stats.norm.ppf(0.95)

# ---------------------------------------------------------------- problems-1
# P1 two regimes: route 2 is the transition matrix and its stationary vector
P = np.array([[0.99, 0.01], [0.04, 0.96]])
evals, evecs = np.linalg.eig(P.T)
pi = np.real(evecs[:, np.argmax(np.real(evals))])
pi = pi / pi.sum()
spell_q = sum(k * 0.99 ** (k - 1) * 0.01 for k in range(1, 20000))
spell_t = sum(k * 0.96 ** (k - 1) * 0.04 for k in range(1, 20000))
expect(1, 0, 1, spell_q, {"stay": 99, "turbulent": spell_t})
expect(1, 0, 2, pi[1], {"ratio": 25 / 100, "quiet": pi[0], "leave": 0.04})
check("P1 share by spells", close(pi[1], spell_t / (spell_q + spell_t)))


def mixvol(wq, wt, sq=0.6, st=1.8):
    return math.sqrt(252 * (wq * sq ** 2 + wt * st ** 2)) / 100


expect(1, 0, 3, mixvol(0.8, 0.2), {"mix-sd": R252 * (0.8 * 0.6 + 0.2 * 1.8) / 100, "share-25": mixvol(0.75, 0.25),
                                    "swapped": mixvol(0.2, 0.8)})


def mixkurt(wq, wt, three=3.0):
    # fourth moment by numeric integration of the mixture density when three == 3
    var = wq * 0.36 + wt * 3.24
    if three == 3.0:
        f = lambda x: x ** 4 * (wq * stats.norm.pdf(x, 0, 0.6) + wt * stats.norm.pdf(x, 0, 1.8))
        m4 = integrate.quad(f, -40, 40, points=[-2, 0, 2])[0]
    else:
        m4 = wq * 0.6 ** 4 + wt * 1.8 ** 4
    return m4 / var ** 2


expect(1, 0, 4, mixkurt(0.8, 0.2) - 3, {"raw": mixkurt(0.8, 0.2), "share-25": mixkurt(0.75, 0.25) - 3,
                                         "no-three": mixkurt(0.8, 0.2, 1.0) - 3, "normal": 0})
check("P1 stated 0.936, 0.9675, 6.6096", close(0.8 * 0.36 + 0.2 * 3.24, 0.936) and close(math.sqrt(0.936), 0.9675)
      and close(3 * (0.8 * 0.1296 + 0.2 * 10.4976), 6.6096))
takes(1, 0, 3, 15.36, "printed")
takes(1, 0, 4, 4.54, "printed")

# P2 stale prices: route 2 is the quadratic form 1' C 1 with a banded covariance matrix
def sum_sd(n, rho=0.12, sd=1.2, band=1, both=True):
    C = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            if a == b:
                C[a, b] = sd ** 2
            elif abs(a - b) <= band and (both or a < b):
                C[a, b] = rho * sd ** 2
    return math.sqrt(C.sum())


expect(1, 1, 1, 1.96 / math.sqrt(1200), {"no-root": 1.96 / 1200, "no-196": 1 / math.sqrt(1200)})
expect(1, 1, 2, sum_sd(5) / 100, {"ten-pairs": sum_sd(5, band=9) / 100, "one-way": sum_sd(5, both=False) / 100,
                                  "root-five": math.sqrt(5) * 1.2 / 100})
expect(1, 1, 3, sum_sd(252) / 100, {"one-way": sum_sd(252, both=False) / 100, "root-rule": R252 * 1.2 / 100})
ratio = sum_sd(252) / (R252 * 1.2)
expect(1, 1, 4, ratio, {"variance": ratio ** 2, "upside-down": 1 / ratio, "one-way": sum_sd(252, both=False) / (R252 * 1.2)})
takes(1, 1, 4, round(21.20 / 19.05, 3), "from the restated 21.20 and 19.05")
check("P2 stated 8.5824, 449.63, 312.24, 2.68", close(sum_sd(5) ** 2, 8.5824) and close(sum_sd(252) ** 2, 449.63, 0.005)
      and close(252 + 502 * 0.12, 312.24) and close(math.sqrt(5) * 1.2, 2.68, 0.005))

# P3 eight-day window: numpy's own estimators
r = np.array([0.9, -0.4, 1.6, -0.7, 0.3, -4.1, 1.1, 0.5])
check("P3 prose sum, mean, squares", close(r.sum(), -0.8) and close(r.mean(), -0.1) and close((r ** 2).sum(), 22.38))
zm = math.sqrt((r ** 2).mean())
expect(1, 2, 1, zm / 100, {"seven": math.sqrt((r ** 2).sum() / 7) / 100, "no-root": (r ** 2).mean() / 100,
                           "abs": np.abs(r).mean() / 100})
s = r.std(ddof=1)
expect(1, 2, 2, s / 100, {"population": r.std(ddof=0) / 100, "no-mean": math.sqrt(8 / 7 * (r ** 2).mean()) / 100,
                          "variance": r.var(ddof=1) / 100})
expect(1, 2, 3, R252 * s / 100, {"zero-mean": R252 * zm / 100, "calendar": math.sqrt(365) * s / 100})
check("P3 fourth powers 267.7186", close(((r - r.mean()) ** 4).sum(), 267.7186, 5e-4))
k = stats.kurtosis(r, fisher=True, bias=True)
expect(1, 2, 4, k, {"raw": k + 3, "sample-var": ((r - r.mean()) ** 4).mean() / r.var(ddof=1) ** 2 - 3})
# the part tells the learner to use s = 1.785%; that value must be accepted at the stated 2 places
takes(1, 2, 3, round(R252 * 1.785, 2), "sqrt(252) x the restated 1.785, to 2 places")
check("P3 part 3 accept line: sqrt(252) x 1.785 prints 28.33", round(R252 * 1.785, 2) == 28.33, f"it is {R252 * 1.785:.4f}")

# P4 big-day indicator: route 2 is the correlation of a long two-state chain built from p and q
p, q, n = 75 / 1500, 18 / 75, 1500
# stationary chain with P(1) = p and P(1 | 1) = q has P(1 | 0) = p(1 - q)/(1 - p); exact lag-1 correlation
p10 = p * (1 - q) / (1 - p)
rho = q - p10
expect(1, 3, 1, q, {"all-days": 18 / 1500, "base": p})
expect(1, 3, 2, rho, {"no-divide": q - p, "ratio": q / p})
check("P4 formula (q - p)/(1 - p)", close(rho, (q - p) / (1 - p)))
expect(1, 3, 3, (n - 1) * rho ** 2, {"no-square": (n - 1) * rho, "from-019": (n - 1) * 0.19 ** 2})


def lm(count):
    qq = count / 75
    return (n - 1) * ((qq - p) / (1 - p)) ** 2


crit = stats.chi2.ppf(0.95, 1)
check("chi2 critical 3.841", close(crit, 3.841, 5e-4))
above = min(c for c in range(4, 76) if lm(c) > crit)
expect(1, 3, 4, above, {"round-down": above - 1, "rho-as-q": round(math.sqrt(crit / (n - 1)) * 75)})
check("P4 part 4: the smallest count that rejects is the key", min(c for c in range(0, 76) if lm(c) > crit) == part(1, 3, 4)["widget"]["answer"],
      f"a count of 0 gives LM = {lm(0):.3f} > 3.841 (autocorrelation {-p / (1 - p):.4f}), so 0 is the smallest count that rejects")
check("P4 stated 3.12 at 7", close(lm(7), 3.12, 0.005))

# ---------------------------------------------------------------- problems-2
# P1 two filters
def ewma(v, ret, lam):
    return lam * v + (1 - lam) * ret ** 2


def garch(v, ret, om, al, be):
    return om + al * ret ** 2 + be * v


e2 = ewma(1.44, -2.5, 0.92)
e3 = ewma(e2, 0.5, 0.92)
g2 = garch(1.44, -2.5, 0.04, 0.07, 0.90)
g3 = garch(g2, 0.5, 0.04, 0.07, 0.90)
expect(2, 0, 1, e2, {"swapped": 0.08 * 1.44 + 0.92 * 6.25, "no-square": 0.92 * 1.44 + 0.08 * -2.5, "decimal": e2 / 1e4})
expect(2, 0, 2, e3, {"old-return": ewma(e2, -2.5, 0.92), "from-start": ewma(1.44, 0.5, 0.92)})
expect(2, 0, 3, g3, {"one-step": garch(1.44, 0.5, 0.04, 0.07, 0.90), "stopped": g2, "no-omega": garch(g2, 0.5, 0, 0.07, 0.90),
                     "decimal": g3 / 1e4}, tol=6e-5)
# exact value is 1.65365, a tie at the fourth place: both roundings must be taken
check("P1 part 3 exact value is a tie", close(g3, 1.65365, 1e-9))
takes(2, 0, 3, 1.6537, "tie rounded up")
takes(2, 0, 3, 1.6536, "tie rounded down, as float arithmetic and round-half-even give")
ll = lambda v, ret: stats.norm.logpdf(ret, 0, math.sqrt(v))
d = ll(e3, -3.2) - ll(g3, -3.2)
expect(2, 0, 4, d, {"sign": -d, "no-half": 2 * d, "log-only": -0.5 * (math.log(e3) - math.log(g3))}, tol=1e-4)
takes(2, 0, 4, round(ll(1.6988, -3.2) - ll(1.6537, -3.2), 3), "from the restated values")
check("P1 stated scores -4.198, -4.267", close(ll(e3, -3.2), -4.198, 5e-4) and close(ll(g3, -3.2), -4.267, 5e-4))

# P2 weekly ARCH: route 2 steps the expectation recursion to its fixed point
V = 5.0
for _ in range(400):
    V = 6.0 + 0.35 * V
expect(2, 1, 1, V, {"omega": 6.0, "over-alpha": 6 / 0.35, "times": 6 * 0.35, "decimal": V / 1e4})
expect(2, 1, 2, math.sqrt(52 * V) / 100, {"days": math.sqrt(252 * V) / 100, "omega": math.sqrt(52 * 6) / 100})
takes(2, 1, 2, round(math.sqrt(52 * 9.23), 2), "from the restated 9.23")
nw = 6 + 0.35 * 144
expect(2, 1, 3, 6 + 0.35 * nw, {"next-week": nw, "alpha-sq": V + 0.35 ** 2 * (nw - V), "level": V, "decimal": (6 + 0.35 * nw) / 1e4})
om = V * (1 - 0.12 - 0.80)
expect(2, 1, 4, om, {"alpha-only": V * 0.12, "arch-omega": 6 * 0.08, "decimal": om / 1e4})
gn = garch(V, 12, om, 0.12, 0.80)
expect(2, 1, 5, gn, {"no-beta": om + 0.12 * 144, "swapped": om + 0.80 * 144 + 0.12 * V, "arch": nw, "decimal": gn / 1e4})
takes(2, 1, 5, round(0.7385 + 0.12 * 144 + 0.80 * 9.2308, 2), "from the restated values")

# P3 silver moment fit
phi = 0.24 / 0.25
expect(2, 2, 1, phi, {"upside-down": 0.25 / 0.24, "difference": 0.25 - 0.24})
hl = optimize.brentq(lambda h: phi ** h - 0.5, 1, 100)
expect(2, 2, 2, hl, {"mean-age": 1 / (1 - phi), "half-mean": 0.5 / (1 - phi)})
om3 = 2.89 * (1 - phi)
expect(2, 2, 3, om3, {"times-p": 2.89 * phi, "sample": 2.89, "decimal": om3 / 1e4})
v4 = garch(2.89, 4.5, om3, 0.09, 0.87)
expect(2, 2, 4, math.sqrt(v4) / 100, {"variance": v4 / 100, "no-square": math.sqrt(om3 + 0.09 * 4.5 + 0.87 * 2.89) / 100,
                                      "annual": R252 * math.sqrt(v4) / 100})


def garch_acf1(al, be):
    ph = al + be
    return al * (1 - ph * be) / (1 - ph ** 2 + al ** 2)


# claim: "The lag-1 ACF then points to alpha = 0.09". The prose's lag-3 value 0.25 fixes the lag-1 value.
rho1_data = 0.25 / phi ** 2
alpha_data = optimize.brentq(lambda a: garch_acf1(a, phi - a) - rho1_data, 0.01, 0.19)
check("P3 part 4: alpha = 0.09 agrees with the ACF in the prose", abs(alpha_data - 0.09) < 0.005,
      f"lag-3 ACF 0.25 and persistence 0.96 give lag-1 ACF {rho1_data:.4f} and alpha {alpha_data:.4f}; alpha 0.09 gives lag-3 ACF {garch_acf1(0.09, 0.87) * phi ** 2:.4f}")
# the proposed fix: alpha 0.13, beta 0.83
v4f = garch(2.89, 4.5, om3, 0.13, 0.83)
check("fix P3 part 4 numbers", close(v4f, 5.1468) and close(math.sqrt(v4f), 2.2687) and round(alpha_data, 2) == 0.13
      and close(math.sqrt(om3 + 0.13 * 4.5 + 0.83 * 2.89), 1.7605) and close(R252 * math.sqrt(v4f), 36.0138, 1e-3)
      and close(0.13 * 20.25, 2.6325) and close(0.83 * 2.89, 2.3987) and round(100 * (math.sqrt(v4f) / 1.7 - 1)) == 33,
      f"{v4f} {math.sqrt(v4f)} {alpha_data}")

# P4 crash then quiet: route 2 iterates the filter day by day
e1 = ewma(1.21, -6, 0.95)
expect(2, 3, 1, e1, {"swapped": 0.05 * 1.21 + 0.95 * 36, "no-square": 0.95 * 1.21 + 0.05 * -6, "decimal": e1 / 1e4})
arch_fall, arch_quiet = 0.8 + 0.45 * 36, 0.8 + 0.45 * 0.25
rt = math.sqrt(arch_fall / e1)
expect(2, 3, 2, rt, {"variance": rt ** 2, "upside-down": 1 / rt})
expect(2, 3, 3, ewma(e1, 0.5, 0.95), {"no-news": 0.95 * e1, "abs": 0.95 * e1 + 0.05 * 0.5, "decimal": ewma(e1, 0.5, 0.95) / 1e4})


def days_below(start, quiet, level, lam=0.95, floor=True):
    v, kk = start, 0
    while v >= level:
        v = lam * v + ((1 - lam) * quiet ** 2 if floor else 0)
        kk += 1
    return kk


kq = days_below(e1, 0.5, arch_quiet)
expect(2, 3, 4, kq, {"round-down": kq - 1, "no-floor": days_below(e1, 0.5, arch_quiet, floor=False)})
check("P4 stated 0.9125, 0.2454, 27.4", close(arch_quiet, 0.9125) and close((arch_quiet - 0.25) / (e1 - 0.25), 0.2454, 5e-5)
      and close(math.log((arch_quiet - 0.25) / (e1 - 0.25)) / math.log(0.95), 27.4, 0.05))
# the proposed fix: quiet days of 0.4%
e3f = ewma(e1, 0.4, 0.95)
aqf = 0.8 + 0.45 * 0.16
check("fix P4 numbers (0.4% quiet days)", close(e3f, 2.810025, 1e-9) and close(aqf, 0.872) and days_below(e1, 0.4, aqf) == 27
      and days_below(e1, 0.4, aqf, floor=False) == 24 and close(0.95 * e1 + 0.05 * 0.4, 2.822025, 1e-9)
      and close((aqf - 0.16) / (e1 - 0.16), 0.2552, 5e-5), f"{e3f} {aqf} {days_below(e1, 0.4, aqf)} {days_below(e1, 0.4, aqf, floor=False)}")

# ---------------------------------------------------------------- problems-3
# P1 forecasts to parameters: route 2 is a root find on the three printed forecasts
f1, f2, f3 = 0.69, 0.676, 0.66298
ph = (f3 - f2) / (f2 - f1)
VL = f1 - (f2 - f1) / (ph - 1)
sol = optimize.fsolve(lambda x: [x[0] + x[1] * (f1 - x[0]) - f2, x[0] + x[1] ** 2 * (f1 - x[0]) - f3], [0.5, 0.9])
check("P1 solve agrees", close(sol[0], VL) and close(sol[1], ph))
expect(3, 0, 1, ph, {"inverted": 1 / ph, "levels": f2 / f1}, tol=1e-4)
expect(3, 0, 2, VL, {"average": (f1 + f2 + f3) / 3, "gap": f1 - VL, "decimal": VL / 1e4})


def step_fc(first, vl, phi_, h):
    v = first
    for _ in range(h - 1):
        v = vl + phi_ * (v - vl)
    return v


v30 = step_fc(f1, VL, ph, 30)
expect(3, 0, 3, math.sqrt(v30) / 100, {"power-30": math.sqrt(step_fc(f1, VL, ph, 31)) / 100, "variance": v30 / 100,
                                       "no-long-run": math.sqrt(v30 - VL) / 100}, tol=2e-7)
var30 = 2.3263 * 0.007172 * 8e6
expect(3, 0, 4, var30, {"part3-slip": 2.3263 * 0.007160 * 8e6, "variance": 2.3263 * 0.005144 * 8e6,
                        "z95": 1.6449 * 0.007172 * 8e6, "tomorrow": 2.3263 * math.sqrt(f1) / 100 * 8e6}, tol=1.0)
takes(3, 0, 4, round(Z99 * math.sqrt(v30) / 100 * 8e6), "unrounded vol and quantile")
check("z 2.3263, 1.6449", close(Z99, 2.3263, 5e-5) and close(Z95, 1.6449, 5e-5))
# "the VaR the model expects to report": E[sigma] is below sqrt(E[sigma^2]) (Jensen); noted in the review, no number here

# P2 bank index
vt = garch(2.25, -4.0, 0.06, 0.06, 0.91)
st = math.sqrt(vt)
expect(3, 1, 1, st / 100, {"no-square": math.sqrt(0.06 + 0.06 * -4.0 + 0.91 * 2.25) / 100, "no-omega": math.sqrt(vt - 0.06) / 100,
                           "variance": vt / 100}, tol=2e-7)
wgt = lambda sd_daily, target=11, cap=1.25: min(target / (sd_daily * R252), cap)
expect(3, 1, 2, wgt(st), {"daily": min(11 / st, 1.25), "times-252": 11 / (st * 252), "from-today": wgt(1.5)}, tol=1e-5)
takes(3, 1, 2, round(11 / (1.7514 * R252), 4), "from the restated 1.7514")
flat = Z99 * 0.11 / R252 * 15e6
expect(3, 1, 3, flat, {"no-weight": 2.3263 * 0.017514 * 15e6, "z95": 1.6449 * 0.3956 * 0.017514 * 15e6}, tol=60)
takes(3, 1, 3, round(2.3263 * 0.3956 * 0.017514 * 15e6, -2), "restated values, nearest 100")
calm = 2.3263 * wgt(0.48) * 0.0048 * 15e6
expect(3, 1, 4, calm, {"no-cap": flat, "cap-1": 2.3263 * 1.0 * 0.0048 * 15e6}, tol=60)
# claim: a forecast of 0.48% a day from this GARCH. Its variance can never fall below omega/(1 - beta).
floor_var = 0.06 / (1 - 0.91)
check("P2 part 4: the stated GARCH can forecast 0.48% a day", 0.48 ** 2 >= floor_var,
      f"with every return 0 the variance settles at omega/(1 - beta) = {floor_var:.4f} %2, a vol of {math.sqrt(floor_var):.4f}%; 0.48% is a variance of {0.48 ** 2:.4f}")
check("P2 stated 0.5543, 0.6929, 7.62, 1.44", close(11 / (1.25 * R252), 0.5543, 5e-5) and close(11 / R252, 0.6929, 5e-5)
      and close(0.48 * R252, 7.62, 0.005) and close(11 / (0.48 * R252), 1.44, 0.005))
# the proposed fix: a refitted model forecasting 0.50%
check("fix P2 part 4 numbers (0.50%)", close(2.3263 * 1.25 * 0.005 * 15e6, 218090.63, 0.01) and close(0.5 * R252, 7.94, 0.005)
      and close(11 / (0.5 * R252), 1.39, 0.005) and close(2.3263 * 1.0 * 0.005 * 15e6, 174472.5, 0.01), "")

# P3 recalibrated short VaR
lr = lambda x, nn, pp: -2 * (stats.binom.logpmf(x, nn, pp) - stats.binom.logpmf(x, nn, x / nn))
expect(3, 2, 1, lr(17, 400, 0.025), {"at-0.01": lr(17, 400, 0.01), "half": lr(17, 400, 0.025) / 2})
check("P3 stated scores, p-value, quantiles", close(383 * math.log(0.975) + 17 * math.log(0.025), -72.408, 5e-4)
      and close(383 * math.log(0.9575) + 17 * math.log(0.0425), -70.324, 5e-4) and close(stats.chi2.sf(lr(17, 400, 0.025), 1), 0.041, 5e-4)
      and close(stats.norm.ppf(0.9575), 1.7224, 5e-5) and close(stats.norm.pdf(1.96), 0.058441, 5e-7))
c_exact = optimize.brentq(lambda c: stats.norm.sf(1.96 / c) - 0.0425, 0.5, 2)
c = 1.9600 / 1.7224
expect(3, 2, 2, c, {"inverted": 1 / c, "rates": 0.0425 / 0.025}, tol=6e-5)
check("P3 c by root find", close(c_exact, c, 2e-4))
expect(3, 2, 3, 1.96 * 1.1379 * 0.0115 * 3e6, {"uncorrected": 1.96 * 0.0115 * 3e6, "inverted": 1.96 * 0.0115 * 3e6 / 1.1379}, tol=0.1)
es_factor = integrate.quad(lambda x: x * stats.norm.pdf(x), 1.96, 40)[0] / 0.025
check("ES factor 2.3376", close(es_factor, 0.058441 / 0.025, 2e-4) and close(es_factor, 2.3376, 2e-4))
expect(3, 2, 4, 1.1379 * 0.0115 * 0.058441 / 0.025 * 3e6, {"uncorrected": 0.0115 * 0.058441 / 0.025 * 3e6,
                                                           "no-divide": 1.1379 * 0.0115 * 0.058441 * 3e6}, tol=0.1)
# a learner who keeps c = 1.96/1.7224 in the calculator
takes(3, 2, 3, round(1.96 * c * 0.0115 * 3e6), "c carried unrounded")
takes(3, 2, 4, round(c * 0.0115 * 0.058441 / 0.025 * 3e6), "c carried unrounded")

# P4 index fund back in
VL4, ph4, t4 = 0.64, 0.977, 4.0
tgt = 14 / R252
w1 = min(tgt / math.sqrt(t4), 1)
expect(3, 3, 1, w1, {"daily": min(14 / 2, 1), "variance": 14 / (4.0 * R252)}, tol=1e-5)
v20 = step_fc(t4, VL4, ph4, 20)
expect(3, 3, 2, math.sqrt(v20) / 100, {"power-20": math.sqrt(step_fc(t4, VL4, ph4, 21)) / 100, "variance": v20 / 100,
                                       "no-long-run": math.sqrt(v20 - VL4) / 100}, tol=2e-7)
ws = [min(tgt / math.sqrt(step_fc(t4, VL4, ph4, h)), 1) for h in range(1, 21)]
bought = sum(abs(b - a) for a, b in zip(ws, ws[1:]))
expect(3, 3, 3, bought, {"day-20-weight": ws[-1], "sum": ws[-1] + ws[0],
                         "part2-slip": tgt / math.sqrt(step_fc(t4, VL4, ph4, 21)) - ws[0]}, tol=5e-5)
takes(3, 3, 3, round(0.88192 / 1.6731 - 0.4410, 3), "from the restated values")
first = next(h for h in range(1, 2000) if tgt / math.sqrt(step_fc(t4, VL4, ph4, h)) >= 1)
h0 = next(h for h in range(1, 2000) if ph4 ** (h - 1) * t4 <= 7 / 9)
hv = next(h for h in range(1, 2000) if 0.8 + ph4 ** (h - 1) * 1.2 <= tgt)
expect(3, 3, 4, first, {"h-minus-1": first - 1, "no-long-run": h0, "vol-gap": hv})
check("P4 stated 7/9, 0.04101, 137.27, 12.70, 0.0043", close(tgt ** 2, 7 / 9) and close((7 / 9 - 0.64) / 3.36, 0.04101, 5e-6)
      and close(math.log((7 / 9 - 0.64) / 3.36) / math.log(0.977), 137.27, 0.005) and close(0.8 * R252, 12.70, 0.005)
      and close(bought * 0.05, 0.0043, 5e-5))

# ---------------------------------------------------------------- numbers printed in the review's replacement texts
v26 = 0.16 + 0.95 ** 26 * (e1 - 0.16)
check("fix texts, set 1", close(R252 * 1.785, 28.336, 5e-4) and close(math.sqrt(365) * s, 34.10, 0.005)
      and close(100 * (312.24 / 252 - 1), 23.9, 0.05) and abs(0.28336 - R252 * s / 100) < 0.00011 and abs(0.28336 - 0.2834) < 0.00011
      and abs(0.28336 - 0.2833) < 0.00011 and close(0.05 * 75, 3.75))
check("fix texts, set 2", close(v26, 0.90, 0.005) and close(math.log(0.2552) / math.log(0.95), 26.6, 0.05) and close(e1 / 1.21, 2.4, 0.05)
      and close(0.05 * 1.21 + 0.95 * 36, 34.2605) and 27 / 5 > 5, f"{v26}")
check("fix texts, set 3", close(0.93 ** 29 * 0.2, 0.0244, 5e-5) and close(1.7514 * 252, 441, 0.5) and close(1.7514 * R252, 27.80, 0.005)
      and close(11 / 1.7514, 6.28, 0.005) and close(lr(17, 400, 0.025) / 2, 2.084, 5e-4) and close(1.1379 * 0.0115 * 0.058441 * 3e6, 2294, 0.5)
      and close(1.6449 * 0.007172 * 8e6, 94378, 0.5) and close(1.6449 * 0.3956 * 0.017514 * 15e6, 170951, 0.5)
      and abs(1.96 * c * 0.0115 * 3e6 - 76944.8) < 5 and abs(c * 0.0115 * 0.058441 / 0.025 * 3e6 - 91770.02) < 5)

# ---------------------------------------------------------------- shape, forms and skills
course = json.load(open(os.path.join(COURSE, "course.json")))
for n, d in SETS.items():
    its = d["items"]
    check(f"problems-{n} 3 to 5 items", 3 <= len(its) <= 5)
    check(f"problems-{n} a difficulty 5", any(i["difficulty"] == 5 for i in its) and all(3 <= i["difficulty"] <= 5 for i in its))
    kinds = [p["widget"]["kind"] for i in its for p in i["parts"]]
    check(f"problems-{n} two thirds typed", sum(k in ("numeric", "expression") for k in kinds) * 3 >= 2 * len(kinds))
    for ii, it in enumerate(its):
        check(f"problems-{n} items[{ii}] 3 to 5 parts", 3 <= len(it["parts"]) <= 5)
        for jj, p in enumerate(it["parts"], 1):
            qn = p["question"]
            check(f"problems-{n} items[{ii}] part {jj} states its form",
                  bool(re.search(r"decimal place|whole number|a decimal|nearest £", qn)), qn[-60:])
            check(f"problems-{n} items[{ii}] part {jj} explain at most 3 sentences",
                  len(re.findall(r"[.?](?:\s|$)", re.sub(r"\$[^$]*\$", "X", p["explain"]["text"]))) <= 3)
            if jj > 1:
                check(f"problems-{n} items[{ii}] part {jj} restates a value", bool(re.search(r"part \d|parts \d|from part|the same|Using|With|Take", qn)), qn[:50])

for f in findings:
    print(f)
print(f"{n_ok} checks passed, {len(findings)} FINDING line(s)")
