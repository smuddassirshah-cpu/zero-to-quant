#!/usr/bin/env python3
"""Delta read review-delta-af-garch: the two re-authored garch problems and the
parts the session AF fix pass changed (docs/reviews/review-problems-garch-1-3.md).

Imports no earlier script. Every key, wrong value and printed number in scope is
rebuilt from the part's text by a second route where one exists: day-by-day sums
for the closed forms, a brute search for each "first" and "smallest" count,
scipy's normal for the tails, numeric integration for the moments, a simulation
for the kurtosis of the rescaled day, the exact ACF formula for the alpha.
Each band is rebuilt with the engine's rule (|typed - answer| <= tol.abs, a
unit of % dividing the typed number by 100) and fed what a learner types from
the rounded working the part prints and from the unrounded carry.

Exit 0 always; a FINDING line prints while the content is as the review
describes and `resolved` once it is fixed.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
GARCH = os.path.join(HERE, "..", "..", "app", "content", "courses", "garch")
SETS = {n: json.load(open(os.path.join(GARCH, f"problems-{n}.json"))) for n in (1, 2, 3)}

checks = 0
failed = 0
findings = 0


def ok(cond, what):
    global checks, failed
    checks += 1
    if not cond:
        failed += 1
        print("FAIL", what)


def finding(n, open_, what):
    global findings
    if open_:
        findings += 1
        print(f"FINDING {n}: {what}")
    else:
        print(f"resolved {n}: {what}")


def item(n, pid):
    for it in SETS[n]["items"]:
        if it["id"] == pid:
            return it
    raise KeyError(pid)


def part(n, pid, k):
    return item(n, pid)["parts"][k - 1]


def typed(p, x):
    """What the engine compares: a % part divides the typed number by 100."""
    return x / 100.0 if p["widget"].get("unit") == "%" else x


def takes(p, x):
    w = p["widget"]
    return abs(typed(p, x) - w["answer"]) <= w["tol"]["abs"] + 1e-12


def wrong(p, wid):
    for w in p["widget"]["wrong"]:
        if w["id"] == wid:
            return w
    raise KeyError(wid)


def hits_wrong(p, wid, x):
    w = wrong(p, wid)
    return abs(typed(p, x) - w["value"]) <= w["tol"]["abs"] + 1e-12


def key_is(p, value, what, rel=2e-6):
    ok(math.isclose(p["widget"]["answer"], value, rel_tol=rel, abs_tol=1e-9), f"{what}: key {p['widget']['answer']} against {value}")


def wrong_is(p, wid, value, what, rel=2e-5):
    w = wrong(p, wid)
    ok(math.isclose(w["value"], value, rel_tol=rel, abs_tol=1e-9), f"{what}: wrong {wid} {w['value']} against {value}")
    # a wrong band never overlaps the key band
    a, t = p["widget"]["answer"], p["widget"]["tol"]["abs"]
    ok(abs(w["value"] - a) > t + w["tol"]["abs"], f"{what}: wrong {wid} band clear of the key band")


def says(p, text, what):
    blob = json.dumps(p, ensure_ascii=False)
    ok(text in blob, f"{what}: text {text!r} present")


def rnd(x, places):
    return float(f"{x:.{places}f}")


# --------------------------------------------------------------------------
# problems-1 P1  p-stale-alarm (re-authored)
# --------------------------------------------------------------------------
it = item(1, "p-stale-alarm")
ok("14.5%" in it["prose"] and "2.1%" in it["prose"] and "3 screen sds" in it["prose"], "stale-alarm stem numbers")
day = 14.5 / math.sqrt(252)
p = part(1, "p-stale-alarm", 1)
key_is(p, 3 * day / 100, "alarm level")
ok(takes(p, 2.74), "alarm: 2.74 taken")
ok(takes(p, rnd(3 * 0.9134, 2)), "alarm: 3 x 0.9134 taken")
ok(abs(rnd(day, 4) - 0.9134) < 1e-9 and abs(rnd(math.sqrt(252), 4) - 15.8745) < 1e-9, "0.9134 and 15.8745")
wrong_is(p, "annual", 0.435, "alarm")
wrong_is(p, "calendar", 3 * 14.5 / math.sqrt(365) / 100, "alarm")
wrong_is(p, "one-sd", day / 100, "alarm")
wrong_is(p, "two-fifty-two", 3 * 14.5 / 252 / 100, "alarm")
for wid, x in (("annual", 43.5), ("calendar", 2.28), ("one-sd", 0.91), ("two-fifty-two", 0.17)):
    ok(hits_wrong(p, wid, x) and not takes(p, x), f"alarm: slip {wid} typed {x} routed")

p = part(1, "p-stale-alarm", 2)
z_r = 2.74 / 2.1
z_u = 3 * day / 2.1
tail_r = 2 * stats.norm.sf(z_r)
tail_u = 2 * stats.norm.sf(z_u)
# second route: integrate the storm day's density beyond the alarm level
num, _ = integrate.quad(lambda r: stats.norm.pdf(r, 0, 2.1), 3 * day, 60)
ok(abs(2 * num - tail_u) < 1e-9, "storm tail by integration")
key_is(p, tail_r, "alarm chance (from the 2.74 the question restates)", rel=2e-5)
ok(abs(tail_u - p["widget"]["answer"]) < p["widget"]["tol"]["abs"] / 5, "alarm chance: unrounded carry well inside the band")
ok(takes(p, rnd(100 * tail_r, 1)) and takes(p, rnd(100 * tail_u, 1)), "alarm chance: rounded and unrounded carry both give a taken value")
ok(takes(p, rnd(100 * 2 * stats.norm.sf(1.305), 1)), "alarm chance: the printed 1.305 gives a taken value")
ok(rnd(100 * tail_r, 1) == 19.2 and rnd(z_r, 3) == 1.305, "19.2 and 1.305")
wrong_is(p, "one-tail", tail_r / 2, "alarm chance", rel=1e-4)
wrong_is(p, "normal", 2 * stats.norm.sf(3), "alarm chance", rel=1e-3)
wrong_is(p, "inside", 1 - tail_r, "alarm chance", rel=1e-4)
ok(hits_wrong(p, "one-tail", 9.6) and hits_wrong(p, "normal", 0.27) and hits_wrong(p, "inside", 80.8), "alarm chance slips routed")

p = part(1, "p-stale-alarm", 3)
key_is(p, 19.2 / 0.27, "alarm ratio", rel=1e-5)
for x in (rnd(19.2 / 0.27, 1), rnd(100 * tail_u / 0.27, 1), rnd(tail_u / (2 * stats.norm.sf(3)), 1)):
    ok(takes(p, x), f"alarm ratio: {x} taken")
wrong_is(p, "one-tail", 19.2 / 0.135, "alarm ratio")
wrong_is(p, "percent", 19.2 / 0.0027, "alarm ratio")
ok(abs(5 * 0.0027 - 0.0135) < 1e-12 and abs(5 * 0.192 - 0.96) < 1e-12, "week counts 0.0135 and 0.96")

p = part(1, "p-stale-alarm", 4)
scale = 2.1 / 0.9134
m2, _ = integrate.quad(lambda x: x**2 * stats.norm.pdf(x, 0, scale), -80, 80)
m4, _ = integrate.quad(lambda x: x**4 * stats.norm.pdf(x, 0, scale), -80, 80)
ok(abs(m4 / m2**2 - 3) < 1e-7, "kurtosis of x by integration is 3")
rng = np.random.default_rng(20261116)
xs = rng.normal(0, 2.1, 2_000_000) / 0.9134
ok(abs(np.mean(xs**4) / np.mean(xs**2) ** 2 - 3) < 0.03, "kurtosis of x by simulation is 3")
key_is(p, 3, "kurtosis")
ok(rnd(scale, 3) == 2.299, "2.299")
wrong_is(p, "excess", 0, "kurtosis")
wrong_is(p, "no-divide", 3 * 2.299**4, "kurtosis", rel=2e-4)
ok(hits_wrong(p, "no-divide", rnd(m4, 2)) and hits_wrong(p, "no-divide", rnd(3 * 2.299**4, 2)), "fourth moment slip routed from both carries")

# reuse finding 1: two lines of part 4 against l3 quiz 0 and l3 screen 10
fb = part(1, "p-stale-alarm", 4)["feedback"]
finding(1, fb["byKey"]["excess"].startswith("0 is the excess kurtosis. The question asks for the raw figure")
        or "both carry the same scale" in fb["generic"],
        "problems-1 p-stale-alarm part 4: `excess` and `generic` retell l3 quiz 0 and l3 screen 10")

# --------------------------------------------------------------------------
# problems-1, changed parts
# --------------------------------------------------------------------------
p = part(1, "p-stale-prices-scaling", 1)
ok(rnd(1.96 / math.sqrt(1200), 4) == 0.0566 and takes(p, 0.0566), "band 0.0566")
ok(hits_wrong(p, "no-root", rnd(1.96 / 1200, 4)), "1.96/1200 routed")
p = part(1, "p-stale-prices-scaling", 4)
var_true = 252 + 2 * 251 * 0.12
ok(abs(var_true - 312.24) < 1e-9, "312.24")
# second route: the banded covariance matrix of 252 days
C = np.eye(252) + 0.12 * (np.eye(252, k=1) + np.eye(252, k=-1))
ok(abs(C.sum() - 312.24) < 1e-9, "312.24 from the covariance matrix")
ok(takes(p, rnd(21.20 / 19.05, 3)) and takes(p, rnd(math.sqrt(312.24 / 252), 3)), "factor: both carries taken")
ok(rnd(100 * (312.24 / 252 - 1), 1) == 23.9, "pairs add 23.9%")
ok(rnd(math.sqrt(312.24 / 252), 3) == 1.113, "1.113")

p = part(1, "p-eight-day-window", 3)
ok(rnd(math.sqrt(252) * 1.785, 2) == 28.34, "rounded s gives 28.34")
ok(takes(p, 28.34) and takes(p, 28.33), "finding 5: 28.34 and 28.33 both taken")
ok(not takes(p, 28.32) and not takes(p, 28.35), "band no wider than the two roundings")
ok(hits_wrong(p, "calendar", 34.10) and not takes(p, 34.10), "calendar slip 34.10 routed")
ok(hits_wrong(p, "zero-mean", 26.55), "zero-mean slip routed")
ok(rnd(math.sqrt(365) * 1.785, 2) == 34.10, "34.10 from the printed s")

p = part(1, "p-big-day-indicator", 4)
n, pbig, m = 1500, 0.05, 75
rej = []
for k in range(0, 76):
    q = k / m
    rho = (q - pbig) / (1 - pbig)
    if (n - 1) * rho * rho > 3.841:
        rej.append(k)
ok(0 in rej and all(k not in rej for k in range(1, 8)) and 8 in rej, "finding 7: count 0 rejects, 1 to 7 do not, 8 does")
ok(min(k for k in rej if k > pbig * m) == 8 == p["widget"]["answer"], "smallest count above 3.75 is 8")
ok("smallest count above that" in p["question"], "question limited to counts above 3.75")
ok(rnd(1499 * ((7 / 75 - 0.05) / 0.95) ** 2, 2) == 3.12 and rnd((7 / 75 - 0.05) / 0.95, 4) == 0.0456, "7 days: 0.0456 and 3.12")
ok(rnd(math.sqrt(3.841 / 1499), 4) == 0.0506 and rnd(1.96 / math.sqrt(1500), 4) == 0.0506, "0.0506 twice")

# --------------------------------------------------------------------------
# problems-2, changed parts
# --------------------------------------------------------------------------
p = part(2, "p-two-filters-one-score", 3)
from fractions import Fraction as F
d2 = F(4, 100) + F(7, 100) * F(625, 100) + F(9, 10) * F(144, 100)
d3 = F(4, 100) + F(7, 100) * F(25, 100) + F(9, 10) * d2
ok(d2 == F(17735, 10000) and d3 == F(165365, 100000), "finding 8: day 3 is exactly 1.65365")
ok(takes(p, 1.6536) and takes(p, 1.6537), "finding 8: both roundings of the tie taken")
ok(not takes(p, 1.6535) and not takes(p, 1.6538), "tie band no wider")
for wid, x in (("one-step", 1.3535), ("stopped", 1.7735), ("no-omega", 1.6137)):
    ok(hits_wrong(p, wid, x) and not takes(p, x), f"day 3 slip {wid} routed")

p = part(2, "p-weekly-gas-arch", 1)
V = 6.0 / 0.65
ok(takes(p, rnd(V, 2)), "V = 9.23 taken")
p = part(2, "p-weekly-gas-arch", 3)
ok(abs(6.0 + 0.35 * 144 - 56.4) < 1e-9 and takes(p, rnd(6.0 + 0.35 * 56.4, 2)), "25.74")
ok(rnd(0.35 * (56.4 - 9.23), 2) == 16.51, "gap 16.51")
p = part(2, "p-weekly-gas-arch", 5)
om = rnd(V * 0.08, 4)
ok(om == 0.7385, "omega 0.7385")
ok(takes(p, rnd(0.7385 + 0.12 * 144 + 0.80 * 9.2308, 2)) and takes(p, rnd(V * 0.08 + 17.28 + 0.8 * V, 2)), "25.40 from both carries")
ok(rnd(0.80 * 9.2308, 4) == 7.3846, "7.3846")

it = item(2, "p-silver-moment-fit")
ok("0.25 at lag 3" in it["prose"] and "0.24 at lag 4" in it["prose"] and "2.89" in it["prose"], "silver stem")
phi = 0.24 / 0.25


def rho1(alpha, phi_):
    beta = phi_ - alpha
    return alpha * (1 - phi_ * beta) / (1 - phi_**2 + alpha**2)


a_star = optimize.brentq(lambda a: phi**2 * rho1(a, phi) - 0.25, 0.01, 0.5)
ok(abs(a_star - 0.1278) < 5e-4, f"finding 14: lag-3 ACF 0.25 needs alpha {a_star:.4f}")
ok(rnd(a_star, 2) == 0.13, "alpha to 2 places is 0.13")
lag3 = phi**2 * rho1(0.13, phi)
lag4 = phi * lag3
ok(abs(lag3 - 0.25) < 0.01 and abs(lag4 - 0.24) < 0.01, f"alpha 0.13 gives lag 3 {lag3:.4f}, lag 4 {lag4:.4f}")
ok(abs(phi**2 * rho1(0.09, phi) - 0.25) > 0.08, "the old alpha 0.09 did not fit the stem")
ok(3 * 0.13**2 + 2 * 0.13 * 0.83 + 0.83**2 < 1, "fourth moment exists, so the ACF does")
# second route: simulate the fitted model and read the ACF of r^2
rng = np.random.default_rng(22)
N = 1_500_000
z = rng.standard_normal(N)
s2 = np.empty(N)
r2 = np.empty(N)
s2[0] = 2.89
r2[0] = s2[0] * z[0] ** 2
for t in range(1, N):
    s2[t] = 0.1156 + 0.13 * r2[t - 1] + 0.83 * s2[t - 1]
    r2[t] = s2[t] * z[t] ** 2
d = r2 - r2.mean()
acf = lambda k: float(np.dot(d[k:], d[:-k]) / np.dot(d, d))
ok(abs(acf(3) - lag3) < 0.04 and abs(acf(4) / acf(3) - 0.96) < 0.03, f"simulated ACF: lag 3 {acf(3):.3f}, ratio {acf(4)/acf(3):.3f}")
ok(abs(r2.mean() - 2.89) < 0.08, "simulated variance near the targeted 2.89")

p = part(2, "p-silver-moment-fit", 2)
h = math.log(0.5) / math.log(0.96)
ok(takes(p, rnd(h, 2)) and rnd(h, 2) == 16.98, "half-life 16.98")
ok(hits_wrong(p, "mean-age", 25) and hits_wrong(p, "half-mean", 12.5), "half-life slips")
ok(3.3 < h / 5 < 3.6, "about three and a half trading weeks")
p = part(2, "p-silver-moment-fit", 4)
v = 0.1156 + 0.13 * 4.5**2 + 0.83 * 2.89
ok(abs(v - 5.1468) < 5e-5, "5.1468")
key_is(p, math.sqrt(v) / 100, "silver vol", rel=3e-5)
ok(takes(p, 2.27) and takes(p, rnd(math.sqrt(5.1468), 2)), "2.27 taken")
wrong_is(p, "variance", v / 100, "silver vol")
wrong_is(p, "no-square", math.sqrt(0.1156 + 0.13 * 4.5 + 0.83 * 2.89) / 100, "silver vol")
wrong_is(p, "annual", math.sqrt(v) * math.sqrt(252) / 100, "silver vol")
ok(rnd(100 * (math.sqrt(v) / 1.7 - 1), 0) == 33, "33% above 1.70%")
ok(abs(0.13 * 20.25 - 2.6325) < 1e-9 and rnd(0.83 * 2.89, 4) == 2.3987, "2.6325 and 2.3987")
ok("\\alpha = 0.13" in p["question"] and "\\beta = 0.83" in p["question"], "question carries the new pair")

it = item(2, "p-crash-then-quiet")
ok("exactly 0.4%" in it["prose"], "crash stem: 0.4% quiet days")
e1 = 0.95 * 1.21 + 0.05 * 36
p = part(2, "p-crash-then-quiet", 1)
key_is(p, e1, "EWMA after fall")
ok(rnd(36 / 1.21, 0) == 30 and rnd(e1 / 1.21, 1) == 2.4, "30 times, 2.4 times")
wrong_is(p, "swapped", 0.05 * 1.21 + 0.95 * 36, "EWMA after fall")
p = part(2, "p-crash-then-quiet", 3)
e2 = 0.95 * 2.9495 + 0.05 * 0.4**2
key_is(p, e2, "EWMA two days on", rel=2e-5)
ok(takes(p, rnd(e2, 4)), "2.8100 taken")
wrong_is(p, "no-news", 0.95 * 2.9495, "EWMA two days on", rel=2e-5)
wrong_is(p, "abs", 0.95 * 2.9495 + 0.05 * 0.4, "EWMA two days on", rel=2e-5)
ok(hits_wrong(p, "no-news", 2.8020) and hits_wrong(p, "abs", 2.8220), "EWMA slips routed")
arch_q = 0.8 + 0.45 * 0.16
ok(abs(arch_q - 0.872) < 1e-12, "ARCH 0.872")
p = part(2, "p-crash-then-quiet", 4)
e = 2.9495
first = None
for k in range(1, 200):
    e = 0.95 * e + 0.05 * 0.16
    ok(abs(e - (0.16 + 0.95**k * (2.9495 - 0.16))) < 1e-9, f"closed form at k={k}") if k in (1, 13, 26, 27) else None
    if first is None and e < arch_q:
        first = k
ok(first == 27 == p["widget"]["answer"], "first quiet day below 0.872 is 27")
ok(rnd(0.16 + 0.95**26 * 2.7895, 2) == 0.90, "about 0.90 after 26 days")
ok(rnd(0.712 / 2.7895, 4) == 0.2552 and rnd(math.log(0.2552) / math.log(0.95), 1) == 26.6, "0.2552 and 26.6")
e, nf = 2.9495, None
for k in range(1, 200):
    e = 0.95 * e
    if e < arch_q:
        nf = k
        break
ok(nf == 24 == wrong(p, "no-floor")["value"], "no-floor slip 24")
ok(wrong(p, "round-down")["value"] == 26, "round-down 26")

# --------------------------------------------------------------------------
# problems-3, changed parts
# --------------------------------------------------------------------------
p = part(3, "p-forecasts-to-parameters", 3)
v30 = 0.49 + 0.93**29 * 0.2
ok(rnd(0.93**29 * 0.2, 4) == 0.0244 and rnd(v30, 4) == 0.5144, "0.0244 and 0.5144")
ok(takes(p, rnd(math.sqrt(v30), 4)) and takes(p, rnd(math.sqrt(0.5144), 4)), "0.7172 taken from both carries")
ok(hits_wrong(p, "power-30", rnd(math.sqrt(0.49 + 0.93**30 * 0.2), 4)), "power-30 routed")
ok(hits_wrong(p, "no-long-run", rnd(math.sqrt(0.0244), 4)) or hits_wrong(p, "no-long-run", rnd(math.sqrt(0.93**29 * 0.2), 4)), "no-long-run routed")
p = part(3, "p-forecasts-to-parameters", 4)
var30 = 2.3263 * 0.7172 / 100 * 8e6
ok(takes(p, round(var30)) and takes(p, round(2.3263 * math.sqrt(v30) / 100 * 8e6)), "VaR day 30: both carries taken")
ok(round(1.6449 * 0.7172 / 100 * 8e6) == 94378, "z95 figure 94,378")
ok(round(2.3263 * math.sqrt(0.69) / 100 * 8e6) == 154590, "tomorrow 154,590")
ok(rnd(100 * (1 - var30 / 154590), 0) == 14, "down by 14%")

it = item(3, "p-bank-index-flat-var")
v1 = 0.06 + 0.06 * 16 + 0.91 * 2.25
sig = math.sqrt(v1)
p = part(3, "p-bank-index-flat-var", 1)
ok(abs(v1 - 3.0675) < 1e-9 and takes(p, rnd(sig, 4)), "1.7514")
ok(hits_wrong(p, "no-omega", rnd(math.sqrt(0.96 + 2.0475), 4)) and hits_wrong(p, "variance", 3.0675), "part 1 slips routed")
p = part(3, "p-bank-index-flat-var", 2)
ann = 1.7514 * math.sqrt(252)
ok(rnd(ann, 3) == 27.803 and takes(p, rnd(11 / ann, 4)) and takes(p, rnd(11 / (sig * math.sqrt(252)), 4)), "weight 0.3956")
ok(rnd(11 / 1.7514, 2) == 6.28 and rnd(1.7514 * 252, 0) == 441, "6.28 and 441%")
p = part(3, "p-bank-index-flat-var", 3)
ok(round(1.6449 * 0.3956 * 0.017514 * 15e6) == 170951, "z95 figure 170,951")
ok(takes(p, round(2.3263 * 0.3956 * 0.017514 * 15e6, -2)), "flat VaR from the rounded carry taken")
p = part(3, "p-bank-index-flat-var", 4)
floor_old = math.sqrt(0.06 / (1 - 0.91))
cap_at = 11 / (1.25 * math.sqrt(252))
ok(floor_old > cap_at and rnd(cap_at, 4) == 0.5543, f"finding 22: first fit's floor {floor_old:.4f}% is above the cap point {cap_at:.4f}%")
ok("refitted" in p["question"] and "0.50%" in p["question"] and "after a long calm" not in p["question"].lower(), "finding 22: the 0.50% comes from a new fit")
w_un = 11 / (0.50 * math.sqrt(252))
ok(rnd(0.50 * math.sqrt(252), 2) == 7.94 and rnd(w_un, 2) == 1.39 and w_un > 1.25, "7.94, 1.39, cap binds")
key_is(p, 2.3263 * 1.25 * 0.005 * 15e6, "capped VaR")
ok(takes(p, 218100) and takes(p, 218091), "218,100 and 218,091 taken")
wrong_is(p, "no-cap", 2.3263 * (11 / math.sqrt(252)) / 100 * 15e6, "capped VaR")
wrong_is(p, "cap-1", 2.3263 * 0.005 * 15e6, "capped VaR")
ok(hits_wrong(p, "no-cap", 241800) and hits_wrong(p, "cap-1", 174500), "capped VaR slips routed at the nearest 100")
ok("1.44" not in json.dumps(it), "the 1.44 of the old part 4 is gone (finding 9)")

it = item(3, "p-recalibrate-short-var")
ok("upper tail" in it["prose"], "finding 23 prose")
ok(abs(stats.norm.ppf(0.9575) - 1.7224) < 5e-5 and abs(stats.norm.pdf(1.96) - 0.058441) < 5e-7, "stem constants")
ll = lambda q: stats.binom.logpmf(17, 400, q)
LR = 2 * (ll(17 / 400) - ll(0.025))
p = part(3, "p-recalibrate-short-var", 1)
ok(takes(p, rnd(LR, 3)), "LR 4.168")
s0 = 383 * math.log(0.975) + 17 * math.log(0.025)
s1 = 383 * math.log(1 - 0.0425) + 17 * math.log(0.0425)
ok(rnd(s0, 3) == -72.408 and rnd(s1, 3) == -70.324 and rnd(s1 - s0, 3) == 2.084, "scores and the gap 2.084")
ok(rnd(stats.chi2.sf(LR, 1), 3) == 0.041, "p-value 0.041")
c_r, c_u = 1.1379, 1.96 / 1.7224
p = part(3, "p-recalibrate-short-var", 3)
ok(takes(p, round(1.96 * c_r * 0.0115 * 3e6)) and takes(p, round(1.96 * c_u * 0.0115 * 3e6)), "finding 26: VaR from rounded and unrounded c taken")
ok(round(1.96 * c_r * 0.0115 * 3e6) == 76945 and round(1.96 * c_u * 0.0115 * 3e6) == 76948, "76,945 and 76,948")
ok(hits_wrong(p, "uncorrected", 67620) and hits_wrong(p, "inverted", round(67620 / c_r)), "VaR slips routed from the rounded c")
finding(2, not hits_wrong(p, "inverted", round(67620 / c_u)),
        "problems-3 p-recalibrate-short-var part 3: the `inverted` band (1.5) refuses the slip made with the unrounded c, "
        f"£{round(67620 / c_u):,}; the key band was widened to 5 for the same carry")
p = part(3, "p-recalibrate-short-var", 4)
es_r = c_r * 0.0115 * 0.058441 / 0.025 * 3e6
es_u = c_u * 0.0115 * 0.058441 / 0.025 * 3e6
ok(takes(p, round(es_r)) and takes(p, round(es_u)), "finding 26: ES from rounded and unrounded c taken")
# second route: the mean loss beyond the VaR by integration
tail, _ = integrate.quad(lambda x: x * stats.norm.pdf(x), 1.96, 40)
ok(abs(tail / stats.norm.sf(1.96) - 0.058441 / 0.025) < 2e-3, "ES multiplier 2.3376 by integration")
ok(hits_wrong(p, "no-divide", round(es_r * 0.025)) and hits_wrong(p, "no-divide", round(es_u * 0.025)), "no-divide routed from both carries")
ok(round(es_r * 0.025) == 2294, "2,294")
ok(hits_wrong(p, "uncorrected", round(0.0115 * 0.058441 / 0.025 * 3e6)), "uncorrected ES routed")

# --------------------------------------------------------------------------
# problems-3 P4  p-monthly-sleeve (re-authored)
# --------------------------------------------------------------------------
it = item(3, "p-monthly-sleeve")
ok(all(s in it["prose"] for s in ("0.81", "0.965", "2.56", "1.75", "21 trading days", "9% a year")), "sleeve stem numbers")
VL, ph, gap = 0.81, 0.965, 2.56 - 0.81
ok(abs(gap - 1.75) < 1e-12, "gap 1.75")
daily = [VL + ph ** (h - 1) * gap for h in range(1, 85)]
# second route: step the expected recursion with omega = VL (1 - phi)
s, stepped = 2.56, []
for _ in range(84):
    stepped.append(s)
    s = VL * (1 - ph) + ph * s
ok(max(abs(a - b) for a, b in zip(daily, stepped)) < 1e-12, "forecast path by recursion")
M = [sum(daily[21 * i: 21 * (i + 1)]) for i in range(4)]
p = part(3, "p-monthly-sleeve", 1)
key_is(p, M[0], "month 1 variance", rel=2e-6)
ok(takes(p, rnd(M[0], 2)) and rnd(M[0], 2) == 43.35, "43.35 taken")
ok(rnd((1 - ph**21) / 0.035, 4) == 15.0505 and rnd(gap * (1 - ph**21) / 0.035, 2) == 26.34 and rnd(21 * VL, 2) == 17.01, "15.0505, 26.34, 17.01")
ok(takes(p, rnd(17.01 + 1.75 * 15.0505, 2)), "printed working gives a taken value")
wrong_is(p, "flat", 21 * 2.56, "month 1 variance")
wrong_is(p, "long-run", 21 * VL, "month 1 variance")
wrong_is(p, "powers-from-one", 21 * VL + gap * sum(ph**k for k in range(1, 22)), "month 1 variance")

p = part(3, "p-monthly-sleeve", 2)
tgt = 9 / math.sqrt(12)
w1_r = tgt / math.sqrt(43.35)
w1_u = tgt / math.sqrt(M[0])
ok(rnd(tgt, 3) == 2.598 and rnd(math.sqrt(43.35), 3) == 6.584, "2.598 and 6.584")
for x in (rnd(w1_r, 4), rnd(w1_u, 4), rnd(2.598 / 6.584, 4), rnd(9 / math.sqrt(12 * 43.35), 4)):
    ok(takes(p, x), f"weight: {x} taken")
ok(abs(tgt - 9 * math.sqrt(21 / 252)) < 1e-12, "a month is a twelfth of 252 days")
wrong_is(p, "monthly", 9 / math.sqrt(43.35), "weight")
wrong_is(p, "variance", tgt / 43.35, "weight")
wrong_is(p, "flat-month", tgt / math.sqrt(53.76), "weight")
wrong_is(p, "times-252", 9 / math.sqrt(43.35 * 252), "weight")
ok(rnd(100 * (1 - w1_r), 0) == 61 or rnd(100 * (1 - w1_r), 0) == 60, "the other 61% in cash")

p = part(3, "p-monthly-sleeve", 3)
key_is(p, M[1], "month 2 variance", rel=2e-6)
m2_r = 17.01 + 0.4732 * 26.34
ok(rnd(ph**21, 4) == 0.4732, "0.4732")
ok(takes(p, rnd(M[1], 2)) and takes(p, rnd(m2_r, 2)) and takes(p, rnd(17.01 + ph**21 * (43.35 - 17.01), 2)), "29.47 taken from every carry")
wrong_is(p, "one-step", 17.01 + ph * 26.34, "month 2 variance")
wrong_is(p, "no-long-run", ph**21 * 43.35, "month 2 variance", rel=1e-4)
wrong_is(p, "power-20", 17.01 + ph**20 * 26.34, "month 2 variance", rel=1e-4)
ok(abs((M[2] - 17.01) / (M[1] - 17.01) - ph**21) < 1e-9, "month 3 keeps 47% of month 2's excess")

p = part(3, "p-monthly-sleeve", 4)
w = [tgt / math.sqrt(m) for m in M]
ok(w[0] < w[1] < w[2] < w[3], "the weight rises at each reset")
bought_u = w[3] - w[0]
# as the part prints it: month 4 from 29.47 and 0.4732, less the 0.3946 of part 2
m4_r = 17.01 + 0.4732**2 * (29.47 - 17.01)
w4_r = 2.598 / math.sqrt(rnd(m4_r, 2))
ok(rnd(0.4732**2, 4) == 0.2239 and rnd(29.47 - 17.01, 2) == 12.46 and rnd(m4_r, 2) == 19.80 and rnd(w4_r, 4) == 0.5839, "0.2239, 12.46, 19.80, 0.5839")
for x in (rnd(bought_u, 3), rnd(w4_r - 0.3946, 3), rnd(0.5839 - 0.3946, 3), rnd(tgt / math.sqrt(M[3]) - 0.3946, 3)):
    ok(takes(p, x), f"bought: {x} taken")
key_is(p, tgt / math.sqrt(M[3]) - 0.3946, "bought", rel=5e-5)
wrong_is(p, "last-weight", w[3], "bought", rel=5e-5)
wrong_is(p, "two-resets", w[2] - 0.3946, "bought", rel=1e-4)
wrong_is(p, "long-run", tgt / math.sqrt(17.01) - 0.3946, "bought", rel=1e-4)
ok(rnd(tgt / math.sqrt(17.01), 3) == 0.630, "long-run weight 0.630")
ok(rnd((w[3] - 0.3946) / (tgt / math.sqrt(17.01) - 0.3946), 1) == 0.8, "four fifths of the way")
buys = [w[1] - 0.3946, w[2] - w[1], w[3] - w[2]]
ok(rnd(buys[1], 4) == 0.0643 and rnd(buys[2], 4) == 0.0410, "second and third buys 0.0643 and 0.0410")
printed_first = 0.0839 if "0.0839" in p["explain"]["text"] else 0.0840
ok(rnd(buys[0], 4) == 0.0840 or abs(buys[0] - 0.08395) < 2e-5, f"first buy from the part's 0.3946 is {buys[0]:.5f}")
finding(3, printed_first == 0.0839,
        f"problems-3 p-monthly-sleeve part 4 explain: first buy printed 0.0839; from the 0.3946 the part states it is {buys[0]:.4f}, "
        f"and 0.0839 + 0.0643 + 0.0410 = 0.1892, not the 0.5839 - 0.3946 = 0.1893 beside it")

print(f"{checks} checks, {failed} failed, {findings} FINDING line(s)")
sys.exit(0)
