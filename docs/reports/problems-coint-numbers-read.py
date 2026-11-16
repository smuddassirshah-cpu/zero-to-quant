#!/usr/bin/env python3
"""Second reader's recompute of coint problem sets 1 to 3.

Every key, every wrong value and the numbers printed in feedback and explain
lines are typed here from the prose and worked again, by another route where
one exists (exact fractions, enumeration, a day-by-day loop, simulation).
Nothing is imported from the author's script. Exit 0 always (CI runs every
script in docs/reports); a failing check prints a FINDING line.
"""
import itertools
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "app", "content", "courses", "coint")
SETS = {n: json.load(open(os.path.join(BASE, f"problems-{n}.json"))) for n in (1, 2, 3)}

checks = 0
findings = []


def chk(name, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        findings.append(f"{name} {detail}")
        print(f"FINDING {name} {detail}")


def item(n, pid):
    for it in SETS[n]["items"]:
        if it["id"] == pid:
            return it
    chk(f"problems-{n} {pid}", False, "item missing")
    return None


def text_of(part):
    fb = part["feedback"]
    out = [part["question"], fb.get("correct", ""), fb.get("generic", "")]
    out += list(fb.get("byKey", {}).values())
    out.append((part.get("explain") or {}).get("text", ""))
    for o in part["widget"].get("options", []):
        out += [o.get("text", ""), o.get("why", "")]
    return " ".join(out).replace("{,}", "").replace("−", "-")


def num(n, pid, k, mine, wrongs=None, printed=()):
    """Key of part k equals mine inside the band; each wrong value is rebuilt,
    lies outside the key band and its own band does not reach the key."""
    it = item(n, pid)
    if it is None:
        return
    part = it["parts"][k]
    w = part["widget"]
    tag = f"problems-{n} {pid} p[{k}]"
    chk(tag + " kind", w["kind"] == "numeric")
    if w["kind"] != "numeric":
        return
    tol = w["tol"].get("abs", 0)
    chk(tag + " key", abs(w["answer"] - mine) <= tol + 1e-12, f"file {w['answer']} mine {mine:.6g}")
    got = {x["id"]: x for x in w.get("wrong", [])}
    wrongs = wrongs or {}
    chk(tag + " wrong ids", set(got) == set(wrongs), f"file {sorted(got)} mine {sorted(wrongs)}")
    for wid, val in wrongs.items():
        if wid not in got:
            continue
        g = got[wid]
        wt = g["tol"].get("abs", 0)
        chk(f"{tag} wrong {wid}", abs(g["value"] - val) <= wt + 1e-12, f"file {g['value']} mine {val:.6g}")
        chk(f"{tag} wrong {wid} off key", abs(g["value"] - w["answer"]) > tol + wt, "band reaches the key")
        chk(f"{tag} wrong {wid} byKey", wid in part["feedback"].get("byKey", {}))
    ids = list(got)
    for a, b in itertools.combinations(ids, 2):
        chk(f"{tag} wrong {a}/{b} apart", abs(got[a]["value"] - got[b]["value"]) > got[a]["tol"].get("abs", 0) + got[b]["tol"].get("abs", 0))
    t = text_of(part)
    for p in printed:
        chk(f"{tag} prints {p}", str(p) in t, "not found in the part's lines")
    chk(tag + " form", w["answer"] == int(w["answer"]) and tol == 0 or bool(re.search(r"place|decimal|whole number|pounds|day number|fraction", part["question"])))


def choice(n, pid, k, right):
    it = item(n, pid)
    w = it["parts"][k]["widget"]
    good = [o["id"] for o in w["options"] if o.get("correct")]
    chk(f"problems-{n} {pid} p[{k}] choice", good == [right], f"file {good}")


def r2(x, d=2):
    return round(x + 1e-12, d)


# ---------------------------------------------------------------- set 1
# p-paper-mill-multiple: x walk sd 0.40, u AR(1) phi 0.8 shock sd 0.30, wrong multiple leaves 0.15x
var_u = F(9, 100) / (1 - F(64, 100))
chk("paper mill Var(u) exact", var_u == F(1, 4))
rng = np.random.default_rng(7)
u = np.zeros(400000)
e = rng.normal(0, 0.30, u.size)
for t in range(1, u.size):
    u[t] = 0.8 * u[t - 1] + e[t]
chk("paper mill sd(u) by simulation", abs(u[1000:].std() - 0.5) < 0.01, f"{u[1000:].std():.4f}")
per_day = F(15, 100) ** 2 * F(4, 10) ** 2
chk("paper mill per-day variance", per_day == F(36, 10000))
# fix pass: part 1 is now the walk part's daily variance (review finding 1); the prose states sd(u) = 0.50
num(1, "p-paper-mill-multiple", 0, float(per_day), {"sd-not-squared": 0.15 ** 2 * 0.40, "multiple-not-squared": 0.15 * 0.16, "neither-squared": 0.15 * 0.40}, ["0.0036", "0.16"])
v500 = per_day * 500 + var_u
num(1, "p-paper-mill-multiple", 1, math.sqrt(v500),
    {"no-u": math.sqrt(per_day * 500), "variance": float(v500),
     "sd-not-squared": math.sqrt(0.15 ** 2 * 0.40 * 500 + 0.25),
     "multiple-not-squared": math.sqrt(0.15 * 0.16 * 500 + 0.25)}, ["1.8", "2.05", "0.0036"])
walks = rng.normal(0, 0.40, (20000, 500)).sum(axis=1) * 0.15 + rng.normal(0, 0.5, 20000)
chk("paper mill day-500 sd by simulation", abs(walks.std() - math.sqrt(2.05)) < 0.03, f"{walks.std():.3f}")
first = next(t for t in range(1, 2000) if per_day * t + var_u > 1)
num(1, "p-paper-mill-multiple", 2, first,
    {"no-subtract": math.ceil(1 / per_day), "doubled-variance": math.ceil(F(1, 4) / per_day), "round-down": first - 1},
    ["208.3", "0.7488", "0.9988"])
choice(1, "p-paper-mill-multiple", 3, "near-true")
chk("paper mill explain 6.01", abs(float(per_day * 1600 + var_u) - 6.01) < 1e-9)

# p-cocoa-chip-levels
tt = lambda r, n: abs(r) * math.sqrt((n - 2) / (1 - r * r))
num(1, "p-cocoa-chip-levels", 0, tt(-0.45, 750),
    {"no-root": 0.45 * 748 / 0.7975, "r-squared": 0.2025 * math.sqrt(748 / 0.7975), "one-minus-r": 0.45 * math.sqrt(748 / 0.55)},
    ["937.9", "30.63"])
rmin = math.sqrt(1.96 ** 2 / (748 + 1.96 ** 2))
chk("cocoa smallest r gives t = 1.96", abs(tt(rmin, 750) - 1.96) < 1e-9)
num(1, "p-cocoa-chip-levels", 1, rmin, {"r-squared": rmin ** 2, "drop-one-minus": 1.96 / math.sqrt(748)}, ["3.8416", "751.84", "0.00511"])
num(1, "p-cocoa-chip-levels", 2, tt(-0.45, 1500), {"doubled": 2 * r2(tt(-0.45, 750)), "unchanged": tt(-0.45, 750)}, ["43.34", "19.50"])
chk("cocoa root-2 claim", abs(tt(-0.45, 1500) / tt(-0.45, 750) - math.sqrt(2)) < 0.01)
chk("cocoa proposed restated route 13.78 * sqrt(1498/748)", abs(13.78 * math.sqrt(1498 / 748) - 19.50) <= 0.01)
choice(1, "p-cocoa-chip-levels", 3, "spurious")
chk("cocoa -2.41 above -3.04", -2.41 > -3.04 > -3.34 > -3.90 and -2.41 > -2.86)
chk("cocoa proposed line: 13.78/1.96 about seven", abs(13.78 / 1.96 - 7.03) < 0.01)

# p-cable-sample-length
guide = lambda phi, n: (phi - 1) / math.sqrt((1 - phi * phi) / n)
num(1, "p-cable-sample-length", 0, -0.04, {"phi": 0.96, "sign": 0.04})
num(1, "p-cable-sample-length", 1, guide(0.96, 250),
    {"one-minus-phi": -0.04 / math.sqrt(0.04 / 250), "no-root": -0.04 / (0.0784 / 250), "sign": -guide(0.96, 250)}, ["0.0784", "0.0177"])
days = lambda phi, c: next(n for n in range(2, 100000) if guide(phi, n) <= c)
n96 = days(0.96, -3.34)
num(1, "p-cable-sample-length", 2, n96,
    {"linear": math.ceil(250 * 3.34 / abs(guide(0.96, 250))), "adf": days(0.96, -2.86), "round-down": n96 - 1},
    ["0.1429", "23.38", "546.6", "-3.338"])
chk("cable 546 days gives -3.338", r2(guide(0.96, 546), 3) == -3.338)
n98 = days(0.98, -3.34)
num(1, "p-cable-sample-length", 3, n98,
    {"doubled": 2 * n96, "phi-unchanged": math.ceil((3.34 * 0.28 / 0.02) ** 2), "one-minus-phi": math.ceil(3.34 ** 2 / 0.02)},
    ["0.1990", "0.0396", "1104.4", "0.1005"])
chk("cable over four years", n98 / 252 > 4)


def eg_stat(n, phi, g):
    x = g.normal(0, 1, n).cumsum()
    uu = np.zeros(n)
    ee = g.normal(0, 1, n)
    for t in range(1, n):
        uu[t] = phi * uu[t - 1] + ee[t]
    y = 2 + x + uu
    A = np.column_stack([np.ones(n), x])
    res = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    lag, d = res[:-1], np.diff(res)
    gam = (lag @ d) / (lag @ lag)
    s2 = ((d - gam * lag) ** 2).sum() / (len(d) - 1)
    return gam / math.sqrt(s2 / (lag @ lag))


g = np.random.default_rng(11)
miss250 = np.mean([eg_stat(250, 0.96, g) > -3.34 for _ in range(600)])
miss250_10 = np.mean([eg_stat(250, 0.96, g) > -3.04 for _ in range(600)])
hit547 = np.mean([eg_stat(547, 0.96, g) <= -3.34 for _ in range(600)])
miss98 = np.mean([eg_stat(250, 0.98, g) > -3.34 for _ in range(600)])
print(f"cable simulation: phi 0.96 on 250 days misses 5% {miss250:.2f}, misses 10% {miss250_10:.2f}; on 547 days rejects {hit547:.2f}; phi 0.98 on 250 days misses {miss98:.2f}")
chk("cable claim: a year usually misses (phi 0.96)", miss250 > 0.5 and miss250_10 > 0.5, f"{miss250:.2f} {miss250_10:.2f}")
chk("cable claim: a slow tie on one year usually fails (phi 0.98)", miss98 > 0.5, f"{miss98:.2f}")

# p-utility-step-two: re-authored in the fix pass as p-screen-real-share; its checks, and the stem FINDING of
# review finding 4, are removed with it. The new problem is checked in the author's script for the delta reader.

# ---------------------------------------------------------------- set 2
# p-cement-three-ratios: re-authored in the fix pass as p-smelter-tls; its checks are removed with it.

# p-lessor-window
a, b = 0.04, -0.08
h = math.log(0.5) / math.log(1 + b)
num(2, "p-lessor-window", 0, h, {"one-over-b": 1 / 0.08, "rough": math.log(2) / 0.08, "b-as-phi": math.log(0.5) / math.log(0.08)}, ["0.0834", "0.513", "0.472"])
# fix pass (finding 7): the explain now brackets the halving between days 8 and 9
chk("lessor 0.92^8 and 0.92^9", r2(0.92 ** 8, 3) == 0.513 and r2(0.92 ** 9, 3) == 0.472)
chk("lessor proposed line: 0.92^8 and 0.92^9", r2(0.92 ** 8, 3) == 0.513 and r2(0.92 ** 9, 3) == 0.472)
num(2, "p-lessor-window", 1, math.ceil(5 * 8.31), {"round-down": math.floor(5 * 8.31)}, ["41.6"])
chk("lessor five half-lives leave about 3%", abs(0.5 ** 5 - 0.03) < 0.005)
num(2, "p-lessor-window", 2, (-0.18 - 0.62) / 0.35, {"sign": 0.8 / 0.35, "no-mean": -0.18 / 0.35, "added-mean": (-0.18 + 0.62) / 0.35})
mu = -a / b
s = -0.18
for _ in range(5):
    s = s + a + b * s  # the regression's own expected step
chk("lessor expected path by loop equals closed form", abs(s - (mu + (-0.18 - mu) * 0.92 ** 5)) < 1e-12)
num(2, "p-lessor-window", 3, s, {"window-mean": 0.62 + (-0.18 - 0.62) * 0.92 ** 5, "zero-mean": -0.18 * 0.92 ** 5}, ["0.448", "0.659", "0.50"])

# p-three-distributors
trace, crit = [41.7, 9.8, 1.6], [29.80, 15.49, 3.84]
rank = next((i for i, (t, c) in enumerate(zip(trace, crit)) if t < c), 3)
num(2, "p-three-distributors", 0, rank, {"trends": 3 - rank, "series": 3, "none": 0})
chk("distributors proposed line: margins 11.9 and 5.69", abs(41.7 - 29.80 - 11.9) < 1e-9 and abs(15.49 - 9.8 - 5.69) < 1e-9)
v = [F(36, 100), F(-54, 100), F(27, 100)]
nv = [x / v[0] for x in v]
chk("distributors normalised vector", nv == [1, F(-3, 2), F(3, 4)])
num(2, "p-three-distributors", 1, float(nv[2]), {"raw": 0.27, "inverted": 0.36 / 0.27, "sign": -0.75})
P, Q, R = 12.40, 9.80, 6.20
sp = P - 1.5 * Q + 0.75 * R
num(2, "p-three-distributors", 2, sp, {"r-sign": P - 1.5 * Q - 0.75 * R, "no-weights": P - Q + R, "q-sign": P + 1.5 * Q + 0.75 * R}, ["14.70", "4.65"])
num(2, "p-three-distributors", 3, (2.35 - 2.05) / 0.20, {"no-mean": 2.35 / 0.20, "variance": 0.30 / 0.04})
choice(2, "p-three-distributors", 4, "no-pair")

# p-tyre-vecm
ay, ax, beta, g0 = -0.06, 0.02, 1.5, 1.50
num(2, "p-tyre-vecm", 0, ay * g0, {"sign": -ay * g0, "x-speed": ax * g0})
dg = ay * g0 - beta * ax * g0
num(2, "p-tyre-vecm", 1, dg, {"no-ratio": ay * g0 - ax * g0, "x-sign": ay * g0 + beta * ax * g0, "y-only": ay * g0, "sign": -dg})
bg = dg / g0
chk("tyre gap slope", abs(bg - (-0.09)) < 1e-12)
gap, k = 1.0, 0
while gap > 0.5:  # day-by-day decay of the expected gap
    gap *= 1 + bg
    k += 1
chk("tyre half-life bracket by loop", k - 1 < math.log(0.5) / math.log(0.91) < k and k == 8)
num(2, "p-tyre-vecm", 2, math.log(0.5) / math.log(1 + bg), {"y-only": math.log(0.5) / math.log(0.94), "rough": math.log(2) / 0.09, "one-over-b": 1 / 0.09}, ["0.0943"])
choice(2, "p-tyre-vecm", 3, "slower")
chk("tyre x does a third", abs(beta * ax / 0.09 - 1 / 3) < 1e-12 and r2(math.log(0.5) / math.log(0.94)) == 11.2)

# ---------------------------------------------------------------- set 3
# p-packaging-stop-reopen: re-authored in the fix pass as p-glassmaker-borrow; its checks are removed with it.

# p-stop-edge
unit, rt = 0.60, 0.10
win, lose = 2 * unit - rt, -(1.4 * unit) - rt
num(3, "p-stop-edge", 0, win, {"no-cost": 1.2, "cost-added": 1.3, "z-units": 2 - rt})
num(3, "p-stop-edge", 1, lose, {"no-cost": -0.84, "stop-four": -(2 * unit) - rt, "sign": -lose, "cost-wrong-way": -0.84 + rt})
pbe = F(94, 204)
chk("stop-edge break-even exact", F(110, 100) * pbe + F(-94, 100) * (1 - pbe) == 0)
num(3, "p-stop-edge", 2, float(pbe), {"swapped": 1.10 / 2.04, "no-cost": 0.84 / 2.04, "even": 0.5})
# first passage of a fair walk from 2 between 0 and 3.4: simple walk on a grid of 0.2
g2 = np.random.default_rng(5)
hits = 0
N = 20000
for _ in range(N):
    p_ = 10
    while 0 < p_ < 17:
        p_ += 1 if g2.random() < 0.5 else -1
    hits += p_ == 0
chk("stop-edge exit-first chance by simulation", abs(hits / N - 1.4 / 3.4) < 0.012, f"{hits / N:.4f}")
num(3, "p-stop-edge", 3, 1.4 / 3.4, {"swapped": 2 / 3.4, "even": 0.5})
num(3, "p-stop-edge", 4, 0.412 * win + 0.588 * lose, {"no-cost": 0.412 * 1.2 - 0.588 * 0.84, "sign": 0.10, "even": 0.5 * win + 0.5 * lose})
chk("stop-edge fair before costs, exact", F(14, 34) * F(12, 10) - F(20, 34) * F(84, 100) == 0)

# p-half-life-alarms: enumerate the 16 breach patterns
p = F(14, 100)
PA = PB = 0
for pat in itertools.product([0, 1], repeat=4):
    pr = math.prod(p if c else 1 - p for c in pat)
    PA += pr if any(pat) else 0
    PB += pr if any(pat[i] and pat[i + 1] for i in range(3)) else 0
num(3, "p-half-life-alarms", 0, float(PA), {"added": 0.56, "escape": float(1 - PA), "all-four": float(p ** 4)}, ["0.5470"])
num(3, "p-half-life-alarms", 1, float(PB), {"three-pairs": float(3 * p ** 2), "one-pair": float(p ** 2), "overlap": float(1 - (1 - p ** 2) ** 3)}, ["2.72"])
more = 40 * (0.4530 - 0.0533)
num(3, "p-half-life-alarms", 2, more, {"a-only": 40 * 0.4530, "all-43": 43 * (0.4530 - 0.0533), "b-only": 40 * 0.0533}, ["18.12", "2.13"])
chk("alarms unrounded count still in band", abs(40 * float(PA - PB) - 15.99) <= 0.01)
saving = r2(15.99 * 1.75)
num(3, "p-half-life-alarms", 3, saving - 3 * 5.00, {"no-delay": saving, "one-broken": saving - 5.00, "sign": -(saving - 15.00)}, ["27.98", "15.00"])
num(3, "p-half-life-alarms", 4, 27.98 / 3, {"no-split": 27.98, "margin": 12.98 / 3})
chk("alarms margin route", abs(5.00 + 12.98 / 3 - 27.98 / 3) < 1e-9)

# p-housebuilder-trading-years
mean = F(1890, 100) / 504
num(3, "p-housebuilder-trading-years", 0, float(mean), {"all-days": 18.90 / (4 * 252 + 504), "per-252": 18.90 / 252})
sharpe = 0.0375 / 0.55 * math.sqrt(252)
num(3, "p-housebuilder-trading-years", 1, sharpe, {"daily": 0.0375 / 0.55, "times-252": 0.0375 / 0.55 * 252, "variance": 0.0375 / 0.3025 * math.sqrt(252)}, ["0.0682", "15.87"])
T = F(504, 252)
num(3, "p-housebuilder-trading-years", 2, 1.08 * math.sqrt(T), {"times-t": 1.08 * 2, "divided": 1.08 / math.sqrt(2), "all-years": 1.08 * math.sqrt(6)}, ["0.707"])
years = (2 / 1.08) ** 2
num(3, "p-housebuilder-trading-years", 3, years, {"no-square": 2 / 1.08, "inverted": (1.08 / 2) ** 2, "four-over": 4 / 1.08}, ["1.852", "1.1664"])
tol_hb = item(3, "p-housebuilder-trading-years")["parts"][3]["widget"]["tol"]["abs"]
chk("housebuilder: the key band takes sqrt T rounded to 1.85, squared (finding 16)", abs(1.85 ** 2 - 3.43) <= tol_hb,
    f"1.85^2 = {1.85 ** 2:.4f}, band {tol_hb}")
total = 3.43 * 252
num(3, "p-housebuilder-trading-years", 4, math.ceil(total - 504), {"total": math.ceil(total), "round-down": math.floor(total - 504)}, ["864.4", "360.4"])
chk("housebuilder unrounded years give the same day count", math.ceil(years * 252 - 504) == 361)

# ---------------------------------------------------------------- shape
for n, d in SETS.items():
    its = d["items"]
    chk(f"problems-{n} 3 to 5 items", 3 <= len(its) <= 5)
    chk(f"problems-{n} one item at 5", any(i["difficulty"] == 5 for i in its) and all(3 <= i["difficulty"] <= 5 for i in its))
    parts = [p_ for i in its for p_ in i["parts"]]
    typed = sum(p_["widget"]["kind"] in ("numeric", "expression") for p_ in parts)
    chk(f"problems-{n} typed two thirds", typed * 3 >= 2 * len(parts), f"{typed}/{len(parts)}")
    for i in its:
        chk(f"problems-{n} {i['id']} 3 to 5 parts", 3 <= len(i["parts"]) <= 5)

# numbers of the proposed replacement part (review finding 1)
chk("proposed paper-mill part: 0.15^2 * 0.40^2 = 0.0036", per_day == F(36, 10000))
chk("proposed paper-mill slips 0.009, 0.024, 0.06", abs(0.15 ** 2 * 0.40 - 0.009) < 1e-12 and abs(0.15 * 0.16 - 0.024) < 1e-12 and abs(0.15 * 0.40 - 0.06) < 1e-12)
chk("proposed housebuilder lines: 1.08 * 0.707 = 0.76, 1.08 * sqrt 6 = 2.65", r2(1.08 * 0.707) == 0.76 and r2(1.08 * math.sqrt(6)) == 2.65)

print(f"{checks} checks, {len(findings)} FINDING line(s)")
sys.exit(0)
