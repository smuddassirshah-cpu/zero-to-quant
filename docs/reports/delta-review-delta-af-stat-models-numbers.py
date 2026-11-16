#!/usr/bin/env python3
"""Delta read, session AF, stat-models problem sets 1 to 4.

Recomputes every key, every `wrong` value and the printed numbers of the seven
re-authored problems and of the parts the two fix passes changed. It imports
nothing from the author's or the readers' scripts. Second routes: listing all
1,024 win patterns and a seeded simulation (two looks), scipy's ranks and all
4,096 sign patterns with the tied ranks (signed ranks), quadrature of the
kernel estimate, scipy's Gamma log density and a simulated first step
(Metropolis), a simulated Gibbs sampler and simulated AR(1) chains (four
books).

Exit 0. A check that fails on the content prints a FINDING line; a number
check that fails prints FAIL as well and is counted.
"""
import itertools
import json
import math
import os
import re
import sys

import numpy as np
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get(
    "DELTA_CONTENT",
    os.path.join(HERE, "..", "..", "app", "content", "courses", "stat-models"),
)
SETS = {n: json.load(open(os.path.join(BASE, f"problems-{n}.json"))) for n in (1, 2, 3, 4)}
ITEMS = {it["id"]: it for s in SETS.values() for it in s["items"]}

checks = 0
fails = 0
findings = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", label)
        print("FINDING number check failed:", label)


def finding(cond, label):
    """A claim or rule check: True is clean, False is a finding."""
    global checks, findings
    checks += 1
    if not cond:
        findings += 1
        print("FINDING", label)


def part(pid, k):
    return ITEMS[pid]["parts"][k - 1]


def key(pid, k):
    return part(pid, k)["widget"]["answer"]


def wrong(pid, k):
    return {w["id"]: w for w in part(pid, k)["widget"].get("wrong", [])}


def texts(pid, k):
    p = part(pid, k)
    out = [p["question"]]
    fb = p.get("feedback", {})
    out += [fb.get("correct", ""), fb.get("generic", "")]
    out += list(fb.get("byKey", {}).values())
    out.append(p.get("explain", {}).get("text", ""))
    for o in p["widget"].get("options", []):
        out += [o.get("text", ""), o.get("why", "")]
    return " ".join(out)


def near(a, b, tol):
    return abs(a - b) <= tol + 1e-12


def numeric(pid, k, value, slips, printed=None, feed=None):
    """Key, slips, bands. `printed`: the value the feedback prints.
    `feed`: values a learner reaches from rounded earlier parts."""
    w = part(pid, k)["widget"]
    tol = w["tol"]["abs"]
    ok(near(w["answer"], value, tol / 10 + 1e-9), f"{pid} p{k} key {w['answer']} vs {value}")
    ws = wrong(pid, k)
    ok(set(ws) == set(slips), f"{pid} p{k} slip ids {sorted(ws)} vs {sorted(slips)}")
    bands = [(w["answer"] - tol, w["answer"] + tol, "key")]
    for sid, v in slips.items():
        if sid not in ws:
            continue
        e = ws[sid]
        ok(near(e["value"], v, e["tol"]["abs"] / 2), f"{pid} p{k} slip {sid} {e['value']} vs {v}")
        bands.append((e["value"] - e["tol"]["abs"], e["value"] + e["tol"]["abs"], sid))
    for (a, b, n1), (c, d, n2) in itertools.combinations(bands, 2):
        ok(b < c or d < a, f"{pid} p{k} bands {n1} and {n2} meet")
    for v in ([printed] if printed is not None else []) + list(feed or []):
        ok(near(w["answer"], v, tol), f"{pid} p{k} key band takes {v}")


def has(pid, k, s):
    ok(s in texts(pid, k), f"{pid} p{k} prints {s!r}")


# ---------------------------------------------------------------- set 1
# p-rfq-busy-minutes
P = "p-rfq-busy-minutes"
m_q, v_q, m_b = 2.5, 4.0, 7.5
phi = v_q / m_q
numeric(P, 1, phi, {"inverted": m_q / v_q, "excess": v_q - m_q}, printed=1.6)
numeric(P, 2, phi * m_b, {"poisson": m_b, "mu-squared": phi * m_b**2}, printed=12.0)
alpha = optimize.brentq(lambda a: m_q + a * m_q**2 - phi * m_q, 0, 5)
numeric(P, 3, alpha, {"no-poisson-part": v_q / m_q**2, "mu-not-squared": (v_q - m_q) / m_q}, printed=0.24)
numeric(P, 4, m_b + alpha * m_b**2, {"extra-only": alpha * m_b**2, "alpha-mu": m_b + alpha * m_b}, printed=21.0)
opts = {o["id"]: o for o in part(P, 5)["widget"]["options"]}
ok(opts["nb"].get("correct") is True and sum(1 for o in opts.values() if o.get("correct")) == 1, f"{P} p5 key nb")
ok(abs(21.0 - 20.6) < abs(12.0 - 20.6) and abs(21.0 - 20.6) < abs(7.5 - 20.6), f"{P} p5 nearest model")
ok(7.5 < 20.6 / 2, f"{P} p5 'well under half'")
# both variance functions agree at 2.5 only
ok(abs((m_q + alpha * m_q**2) - phi * m_q) < 1e-12, f"{P} match at quiet mean")

# changed parts of the kept problems, set 1
P = "p-ipo-underwriter"
p_lr = stats.chi2.sf(10.357, 1)
ok(near(key(P, 4), p_lr, 1e-5), f"{P} p4 key")
ok(near(p_lr, 2 * stats.norm.sf(math.sqrt(10.357)), 1e-12), f"{P} p4 chi2_1 as a normal tail")
ok(round(stats.chi2.cdf(10.357, 1), 4) == 0.9987 and round(p_lr, 4) == 0.0013, f"{P} p4 printed tails")
ok(near(wrong(P, 4)["two-df"]["value"], math.exp(-10.357 / 2), 5e-5), f"{P} p4 two-df")
finding(
    "\\Phi(" in part(P, 4)["question"] or "P(\\chi^2_1 >" in part(P, 4)["question"],
    f"{P} p4: a chi-squared tail to 4 places with no source named (r5-lr gives none either; "
    f"it reduces to 2(1 - Phi(3.2182)), Phi(3.2182) = {stats.norm.cdf(math.sqrt(10.357)):.5f})",
)

P = "p-settlement-fails"
se = math.sqrt(58 / 840)
ok(abs(58 / 840 - (1 / 30 + 1 / 28)) < 1e-15, f"{P} 58/840 = 1/30 + 1/28")
ok(round(se, 4) == 0.2628 and round(58 / 840, 3) == 0.069, f"{P} p2 printed")
M = np.array([[58.0, 28.0], [28.0, 28.0]])
ok(abs(np.linalg.det(M) - 840) < 1e-9 and abs(np.linalg.inv(M)[1, 1] - 58 / 840) < 1e-12, f"{P} p2 inverse")
phih = 17.6 / 8
seq = math.sqrt(phih) * se
ok(round(seq, 5) == 0.38975 and round(math.sqrt(2.2), 4) == 1.4832, f"{P} p3 printed")
ok(near(key(P, 3), 0.8473 / seq, 1e-4), f"{P} p3 key")
ok(round(0.2628 * 2.2, 4) == 0.5782, f"{P} p3 shown product 0.5782")
ok(near(wrong(P, 3)["phi-not-root"]["value"], 0.8473 / (se * 2.2), 1e-3), f"{P} p3 phi-not-root")
ok(near(wrong(P, 3)["ten-df"]["value"], 0.8473 / (se * math.sqrt(1.76)), 1e-3), f"{P} p3 ten-df")
lo = math.exp(0.84730 - 1.96 * 0.38975)
ok(near(key(P, 4), lo, 1e-4) and round(0.84730 - 1.96 * 0.38975, 4) == 0.0834, f"{P} p4 key and 0.0834")
t8 = stats.t.ppf(0.975, 8)
ok(round(t8, 3) == 2.306 and round(math.exp(0.84730 - t8 * 0.38975), 3) == 0.950, f"{P} p4 t_8 end")
ok("1.96" in part(P, 4)["question"], f"{P} p4 names 1.96")

P = "p-recon-breaks"
ok(round((3 - math.exp(2)) / math.exp(2), 3) == -0.594, f"{P} p2 no-eta -0.594")
ok(round(2 + (3 - math.exp(2)) / math.exp(2), 4) == 1.4060, f"{P} p3 1.4060")
b = 2.0
for _ in range(60):
    b = b + (3 - math.exp(b)) / math.exp(b)
ok(near(key(P, 3), b, 1e-6) and abs(b - math.log(3)) < 1e-12, f"{P} p3 fixed point")
ok(round(9.3333 / 5, 4) == 1.8667 and round(9.3333 / 5, 2) == 1.87, f"{P} p4 printed")

# ---------------------------------------------------------------- set 2
P = "p-signal-variants"
means = {"A": 0.3, "B": 1.4, "C": 2.2, "D": 3.8, "E": 0.9, "F": 1.2}
k_, n_ = 6, 9
ssw = 172.8
dfw = k_ * n_ - k_
msw = ssw / dfw
numeric(P, 1, msw, {"n-minus-one": ssw / 53, "all-months": ssw / 54}, printed=3.6)
pairs = math.comb(k_, 2)
numeric(P, 2, 0.05 / pairs, {"per-variant": 0.05 / 6, "halved": 0.05 / 30}, printed=0.0033)
sed = math.sqrt(2 * msw / n_)
numeric(P, 3, sed, {"variance": 2 * msw / n_, "one-mean": math.sqrt(msw / n_)}, printed=0.8944)
tcrit = stats.t.ppf(1 - 0.05 / pairs / 2, dfw)
ok(round(tcrit, 4) == 3.0892, f"{P} p4 critical value {tcrit:.5f}")
has(P, 4, "3.0892")
bar = 3.0892 * 0.8944
numeric(
    P, 4, 3.0892 * sed,
    {"variance": 3.0892 * 0.8, "one-mean": 3.0892 * 0.6325, "normal-five": 1.96 * 0.8944},
    printed=2.763, feed=[bar],
)
gaps = sorted((round(abs(a - b), 10) for a, b in itertools.combinations(means.values(), 2)), reverse=True)
count = lambda c: sum(1 for g in gaps if g >= c)
numeric(P, 5, count(2.763), {"normal-five": count(1.753), "one-mean": count(1.954), "variance": count(2.471)}, printed=2)
ok(gaps[:4] == [3.5, 2.9, 2.6, 2.4], f"{P} p5 largest gaps {gaps[:4]}")
ok(all(abs(g - c) > 0.05 for g in gaps for c in (2.763, 2.471, 1.954, 1.753)), f"{P} p5 no gap on a bar")
grand = sum(means.values()) / 6
F = (n_ * sum((m - grand) ** 2 for m in means.values()) / 5) / msw
ok(stats.f.sf(F, 5, dfw) < 0.05, f"{P} prose: the ANOVA rejects at 5% (F = {F:.3f})")

P = "p-two-looks"
pats = list(itertools.product((0, 1), repeat=10))
late = lambda p: sum(p) >= 9
early = lambda p: sum(p[:5]) == 5
nA = sum(1 for p in pats if late(p))
nB = sum(1 for p in pats if early(p))
nAB = sum(1 for p in pats if late(p) and early(p))
nStop = sum(1 for p in pats if early(p) or late(p))
ok((nA, nB, nAB, nStop) == (11, 32, 6, 37), f"{P} pattern counts {(nA, nB, nAB, nStop)}")
p1, p2 = nA / 1024, nB / 1024
numeric(P, 1, p1, {"exactly-nine": 10 / 1024, "eight-or-more": 56 / 1024}, printed=0.0107)
ok(abs(stats.binom.sf(8, 10, 0.5) - p1) < 1e-15 and abs(stats.binom.sf(7, 10, 0.5) - 56 / 1024) < 1e-15, f"{P} p1 binomial")
numeric(P, 2, p2, {"two-sided": 2 / 32}, printed=0.0313)
numeric(
    P, 3, p1 + p2,
    {"independent": 1 - (1 - p1) * (1 - p2), "product": p1 * p2},
    printed=0.0420, feed=[0.0107 + 0.0313],
)
ok(near(wrong(P, 3)["independent"]["value"], 1 - (1 - 0.0107) * (1 - 0.0313), 1e-4), f"{P} p3 independent from rounded")
numeric(
    P, 4, nStop / 1024,
    {"bound": 0.0420, "independent": 1 - (1 - p1) * (1 - p2), "day-ten": p1},
    printed=0.0361,
)
# the plan as run: stop at day 5 on five wins, else test at day 10
rng = np.random.default_rng(20261116)
N = 2_000_000
wins = rng.integers(0, 2, size=(N, 10), dtype=np.int8)
e = wins[:, :5].sum(axis=1) == 5
t = wins.sum(axis=1) >= 9
sim = (e | (~e & t)).mean()
se_sim = math.sqrt(37 / 1024 * (1 - 37 / 1024) / N)
ok(abs(sim - 37 / 1024) < 4 * se_sim, f"{P} p4 simulated rate {sim:.5f} vs {37/1024:.5f}")
ok(abs(t.mean() - p1) < 4 * math.sqrt(p1 / N) and abs(e.mean() - p2) < 4 * math.sqrt(p2 / N), f"{P} p1, p2 simulated")
ok(abs((e & t).mean() - 6 / 1024) < 4 * math.sqrt(6 / 1024 / N), f"{P} both looks reject, simulated")
ok(round(37 / 1024 / p1, 2) == 3.36 and round((p1 + p2) / p1, 2) == 3.91, f"{P} 'over three times', 'nearly four times'")
finding(
    "is the chance that both looks reject" not in part(P, 3)["feedback"]["byKey"]["product"],
    f"{P} p3 `product`: 0.0003 is the product of the two chances, not 'the chance that both looks reject'; "
    f"that chance is 6/1024 = {6/1024:.4f}, since the looks share days 1 to 5",
)
finding(
    "already risk nearly four times" not in part(P, 3)["explain"]["text"],
    f"{P} p3 explain: 'Two looks already risk nearly four times' states the bound ({(p1+p2)/p1:.2f} times) as the risk; "
    f"the rate is {37/1024/p1:.2f} times",
)

P = "p-twin-books"
ok(round(math.sqrt(720), 4) == 26.8328 and 225 + 225 + 2 * 135 == 720 and 2 * 225 * 0.4 == 180, f"{P} p1 plus-rho")
ok(round(15 * math.sqrt(2), 4) == 21.2132 and round(math.sqrt(180), 4) == 13.4164, f"{P} p1 printed")
ok(round(13.4164 / math.sqrt(120), 5) == 1.22474 and round(14.1 / math.sqrt(120), 5) == 1.28715, f"{P} p3 printed")
z975, z80 = stats.norm.ppf(0.975), stats.norm.ppf(0.8)
ok(round(z975, 5) == 1.95996 and round(z80, 5) == 0.84162, f"{P} quantiles")
ok(round(z975 * math.sqrt(180 / 120), 4) == 2.4005, f"{P} p2 no-power 2.4005 unrounded")
finding(
    "1.95996 \\times 1.22474$" not in part(P, 2)["feedback"]["byKey"]["no-power"],
    f"{P} p2 `no-power`: the shown product 1.95996 x 1.22474 is {1.95996*1.22474:.5f}, 2.4004 to 4 places; "
    f"the line prints 2.4005 (the unrounded value)",
)
tt = 2.9 / (14.1 / math.sqrt(120))
ok(round(tt, 4) == 2.2530, f"{P} p3 t")
tail = stats.t.sf(2.2530, 119)
ok(round(tail, 4) == 0.0130 and near(key(P, 4), 2 * tail, 1e-5), f"{P} p4 tail and key")
ok(near(key(P, 4), 2 * 0.0130, part(P, 4)["widget"]["tol"]["abs"]), f"{P} p4 key takes 2 x 0.0130")
finding(
    "= 0.0130$." not in part(P, 4)["question"],
    f"{P} p4: the question gives the tail 0.0130, which doubles to 0.0260; the feedback prints 0.0261 "
    f"(tail to 5 places: {tail:.5f})",
)

# ---------------------------------------------------------------- set 3
P = "p-hedge-ranks"
d = np.array([float(x.replace("$", "")) for x in re.findall(r"\$?-?\d+\.\d\$?", ITEMS[P]["prose"])])
ok(len(d) == 12, f"{P} twelve months read from the prose")
r = stats.rankdata(np.abs(d))
wp, wm = r[d > 0].sum(), r[d < 0].sum()
low = stats.rankdata(np.abs(d), method="min")
high = stats.rankdata(np.abs(d), method="max")
# the positive 0.9 at the lower or the upper of its two places
numeric(P, 1, wp, {"tie-low": low[d > 0].sum(), "tie-high": high[d > 0].sum(), "w-minus": wm}, printed=8.5)
ok(len(d[d > 0]) == 2 and wp == 8.5 and wp + wm == 78, f"{P} p1 ranks {sorted(r[d > 0])}")
for v, rk in zip(d[d > 0], r[d > 0]):
    ok(f"{v:g}" in part(P, 1)["feedback"]["correct"] and f"{rk:g}" in part(P, 1)["feedback"]["correct"], f"{P} p1 feedback names {v:g} and its rank {rk:g}")
n = 12
var = n * (n + 1) * (2 * n + 1) / 24
ok(var == sum(k * k for k in range(1, 13)) / 4 == 162.5, f"{P} p2 variance as sum of r^2/4")
numeric(P, 2, math.sqrt(var), {"variance": var, "six-divisor": math.sqrt(650)}, printed=12.7475)
mean = n * (n + 1) / 4
z = (wp - mean) / math.sqrt(var)
numeric(
    P, 3, z,
    {"w-minus": (wm - mean) / math.sqrt(var), "variance": (wp - mean) / var, "no-centre": wp / math.sqrt(var)},
    printed=-2.393, feed=[(8.5 - 39) / 12.7475],
)
pz = stats.norm.cdf(z)
numeric(P, 4, pz, {"two-sided": 2 * pz, "upper": 1 - pz}, printed=0.0084, feed=[stats.norm.cdf(-2.393)])
# exact null: all 4,096 sign patterns, with the tied ranks as they are
sums = np.array([sum(c) for c in itertools.product(*[(0.0, x) for x in r])])
p_exact = (sums <= wp + 1e-9).mean()
sums_untied = np.array([sum(c) for c in itertools.product(*[(0, x) for x in range(1, 13)])])
ok(abs(sums.var() - (r**2).sum() / 4) < 1e-9 and abs(sums.mean() - 39) < 1e-12, f"{P} null mean and variance by listing")
ok(abs(sums_untied.var() - 162.5) < 1e-9, f"{P} untied null variance by listing")
ok(p_exact < 0.01 and pz < 0.01, f"{P} p4 'at the 1% level': exact {p_exact:.5f}, normal {pz:.5f}")
w_sc = stats.wilcoxon(d, alternative="less", correction=False, method="approx") if hasattr(stats, "wilcoxon") else None
ok(w_sc is not None and abs(w_sc.statistic - wp) < 1e-9, f"{P} scipy W+ {w_sc.statistic}")
z_tie = (wp - mean) / math.sqrt((r**2).sum() / 4)
ok(abs(w_sc.pvalue - stats.norm.cdf(z_tie)) < 1e-9, f"{P} scipy's normal p uses the tie-corrected variance")
ok(abs(stats.norm.cdf(z_tie) - pz) < 1e-4, f"{P} the tie moves p by under 0.0001 ({stats.norm.cdf(z_tie):.5f})")
print(f"  note {P}: exact one-sided p with the tie {p_exact:.5f} ({int(round(p_exact*4096))} of 4096), normal {pz:.5f}")
finding(
    "\\Phi(" in part(P, 4)["question"],
    f"{P} p4: a normal tail to 4 places with no source named (Phi(2.393) = {stats.norm.cdf(2.393):.5f})",
)
# reuse: l10 screen 5 has 12 days, W- = 8, W+ = 70; l10 quiz 0 has a tie for ranks 3 and 4
finding(
    not (len(d) == 12 and sorted(r[d > 0])[0] == 3.5),
    f"{P} p1: twelve values, a tie for ranks 3 and 4 and a small rank sum of 8.5 against 69.5 "
    f"(l10 screen 5: twelve days, 8 against 70; l10 quiz q-ties: ranks 3 and 4 give 3.5)",
)

P = "p-spread-day-tail"
x = np.array([-5.6, -1.3, -0.2, 0.6, 1.1, 1.7, 2.4, 8.8])
ok(all(f"{abs(v)}" in ITEMS[P]["prose"] for v in x), f"{P} data in prose")
med = np.median(x)
mad = np.median(np.abs(x - med))
ok(abs(med - 0.85) < 1e-12 and abs(mad - 1.3) < 1e-12, f"{P} median and MAD")
ok(abs(stats.median_abs_deviation(x) - 1.3) < 1e-12, f"{P} scipy MAD")
s = x.std(ddof=1)
rob = 1.4826 * mad
numeric(P, 1, rob, {"raw": mad, "plain-sd": s}, printed=1.9274)
rule = lambda sp: 1.06 * sp * len(x) ** (-0.2)
h = rule(rob)
numeric(P, 2, h, {"plain-sd": rule(s), "raw-mad": rule(mad), "no-n": 1.06 * rob}, printed=1.3479, feed=[rule(1.9274)])
ok(round(8 ** (-0.2), 5) == 0.65975 and round(1.06 * 8 ** (-0.2), 4) == 0.6993, f"{P} p2 printed factors")
share = lambda hh: stats.norm.cdf((-4 - x) / hh).mean()
kde_q = lambda hh: integrate.quad(lambda t: stats.norm.pdf((t - x) / hh).mean() / hh, -60, -4)[0]
ok(abs(share(h) - kde_q(h)) < 1e-8, f"{P} p3 share by quadrature")
numeric(
    P, 3, share(h),
    {"plain-sd": share(rule(s)), "raw-mad": share(rule(mad)), "empirical": 1 / 8},
    printed=0.1135, feed=[share(1.3479)],
)
ok(round(stats.norm.cdf(1.6 / 1.3479), 4) == 0.8824 and round(stats.norm.cdf(-2.7 / 1.3479), 4) == 0.0226, f"{P} p3 two bumps")
six = lambda hh: stats.norm.cdf((-4 - x[1:7]) / hh).sum() / 8
ok(six(rule(s)) > 10 * six(h), f"{P} p3 plain-sd line: six ordinary days {six(rule(s)):.4f} against {six(h):.4f}")
ok(stats.norm.cdf(1.6 / h) / 8 / share(h) > 0.95, f"{P} p3 'nearly all from the -5.6 day'")
fit = stats.norm.cdf((-4 - med) / rob)
ok(round((-4 - med) / rob, 4) == -2.5164 and round(fit, 5) == 0.00593, f"{P} p4 printed")
finding(
    "0.85)/1.9274\\big)" not in part(P, 4)["feedback"]["correct"],
    f"{P} p4 feedback: the shown quotient (-4 - 0.85)/1.9274 is {(-4 - 0.85)/1.9274:.5f}, -2.5163 to 4 places; "
    f"the line prints -2.5164 (from the unrounded 1.92738)",
)
classic = stats.norm.cdf((-4 - x.mean()) / s)
numeric(
    P, 4, share(h) / fit,
    {"empirical-share": 0.125 / 0.00593, "classic-normal": 0.1135 / classic},
    printed=19.1, feed=[0.1135 / 0.00593],
)
ok(abs(x.mean() - 0.9375) < 1e-12, f"{P} p4 mean 0.9375")
# a learner with a printed normal table reads z to 2 places
tab = lambda zz: round(stats.norm.cdf(round(zz, 2)), 4)
tab_share = sum(tab((-4 - v) / 1.3479) for v in x) / 8
tab_ratio = 0.1135 / tab((-4 - 0.85) / 1.9274)
finding(
    "\\Phi(" in part(P, 3)["question"] or near(key(P, 3), round(tab_share, 4), part(P, 3)["widget"]["tol"]["abs"]),
    f"{P} p3: eight normal areas with no source named; a table reader gets {tab_share:.4f}, "
    f"outside {key(P, 3):.6f} +/- 0.0001",
)
finding(
    "\\Phi(" in part(P, 4)["question"] or near(key(P, 4), round(tab_ratio, 1), part(P, 4)["widget"]["tol"]["abs"]),
    f"{P} p4: the normal fit's tail has no source; a table reader gets {tab_ratio:.1f}, outside {key(P, 4):.2f} +/- 0.1",
)

P = "p-five-weeks-flip"
wk = [-0.4, 0.8, 1.2, 2.5, 9.0]
four = [np.array([a * 0.4, b * 0.8, 1.2, 2.5, 9.0]) for a in (1, -1) for b in (1, -1)]
ok(sorted(round(v.mean(), 2) for v in four) == [2.3, 2.46, 2.62, 2.78], f"{P} p4 four means")
ok(all(np.median(v) == 1.2 for v in four), f"{P} p4 four medians 1.2")
allp = [np.array(wk) * np.array(sg) for sg in itertools.product((1, -1), repeat=5)]
ok(sum(1 for v in allp if v.mean() >= np.mean(wk) - 1e-12) == 2, f"{P} mean count 2")
ok(sum(1 for v in allp if np.median(v) >= 1.2 - 1e-12) == 4, f"{P} median count 4")
alt = [np.array([-0.4, 0.8, 1.2, 2.5, 2.6]) * np.array(sg) for sg in itertools.product((1, -1), repeat=5)]
ok(
    sum(1 for v in alt if v.mean() >= 1.34 - 1e-12) == 2 and sum(1 for v in alt if np.median(v) >= 1.2 - 1e-12) == 4,
    f"{P} p4 counts with 2.6 in place of 9.0",
)

# ---------------------------------------------------------------- set 4
P = "p-iceberg-refills"
a_post, b_post = 5 + 36, 2 + 14
logk = lambda lam: 40 * math.log(lam) - 16 * lam
mode = optimize.minimize_scalar(lambda l: -logk(l), bounds=(0.1, 10), method="bounded", options={"xatol": 1e-10}).x
ok(abs(mode - 2.5) < 1e-6, f"{P} p1 mode by optimisation {mode:.6f}")
numeric(
    P, 1, (a_post - 1) / b_post,
    {"mean": a_post / b_post, "mle": 36 / 14, "prior-mode": 4 / 2, "swapped": (14 + 4) / (36 + 2)},
    printed=2.5,
)
lp = lambda lam: stats.gamma.logpdf(lam, a_post, scale=1 / b_post)
up = lp(2.9) - lp(2.5)
dn = lp(2.1) - lp(2.5)
ok(abs(up - (logk(2.9) - logk(2.5))) < 1e-10, f"{P} p2 scipy against the kernel")
numeric(
    P, 2, up,
    {"power-41": 41 * math.log(2.9 / 2.5) - 6.4, "as-scale": 40 * math.log(2.9 / 2.5) - 0.4 / 16, "reversed": -up},
    printed=-0.4632,
)
ok(round(40 * math.log(2.9 / 2.5), 4) == 5.9368 and round(dn, 4) == -0.5741, f"{P} printed 5.9368, -0.5741")
au, ad = min(1, math.exp(up)), min(1, math.exp(dn))
ok(round(au, 4) == 0.6293 and round(ad, 4) == 0.5632, f"{P} p3 acceptance chances")
numeric(
    P, 3, (au + ad) / 2,
    {"up-only": au, "down-only": ad, "sum": au + ad, "stay": 1 - (au + ad) / 2},
    printed=0.5962, feed=[(0.6293 + 0.5632) / 2, (math.exp(-0.4632) + math.exp(-0.5741)) / 2],
)
drift = 0.4 * (au - ad) / 2
numeric(
    P, 4, drift,
    {"no-half": 0.4 * (au - ad), "no-step": (au - ad) / 2, "sign": -drift},
    printed=0.0132, feed=[0.2 * (0.6293 - 0.5632)],
)
rng = np.random.default_rng(41)
N = 4_000_000
prop = 2.5 + 0.4 * rng.choice((-1.0, 1.0), size=N)
acc = np.log(rng.uniform(size=N)) < (40 * np.log(prop / 2.5) - 16 * (prop - 2.5))
ok(abs(acc.mean() - (au + ad) / 2) < 4 * 0.5 / math.sqrt(N), f"{P} p3 simulated first step {acc.mean():.5f}")
step = np.where(acc, prop - 2.5, 0.0)
ok(abs(step.mean() - drift) < 4 * step.std() / math.sqrt(N), f"{P} p4 simulated drift {step.mean():.5f}")
ok(all(logk(2.5 + dx) < logk(2.5) for dx in (-2, -0.4, -0.01, 0.01, 0.4, 3)), f"{P} every move from the peak is downhill")

P = "p-four-books"
s2, tau2, pr2, J = 2.0**2, 1.0**2, 1.5**2, 4
slope1 = (1 / tau2) / (1 / tau2 + 1 / s2)
numeric(P, 1, slope1, {"estimate-weight": 1 - slope1, "sd-weights": 1 / (1 + 1 / 2)}, printed=0.8)
ok(abs(slope1 - s2 / (s2 + tau2)) < 1e-15, f"{P} p1 lesson 18's B = 4/5")
slope2 = (J / tau2) / (J / tau2 + 1 / pr2)
phi = slope1 * slope2
numeric(
    P, 2, phi,
    {"square": slope1**2, "mu-slope": slope2, "no-quarter": slope1 * (1 / tau2) / (1 / tau2 + 1 / pr2), "first-slope": slope1},
    printed=0.72,
)
ok(round(1 / pr2, 4) == 0.4444 and abs(slope2 - 0.9) < 1e-12, f"{P} p2 printed")
ess = 10000 * (1 - phi) / (1 + phi)
numeric(
    P, 3, ess,
    {"no-plus-phi": 10000 * (1 - phi), "one-chain": ess / 4, "independent": 10000, "square": 10000 * 0.36 / 1.64},
    printed=1627.9,
)
# posterior sd of mu: ybar | mu ~ N(mu, (s2 + tau2)/J)
post_var = 1 / (J / (s2 + tau2) + 1 / pr2)
psd = math.sqrt(post_var)
ok(round(psd, 4) == 0.8964, f"{P} p4 posterior sd {psd:.5f}")
has(P, 4, "0.8964")
mcse = psd / math.sqrt(ess)
numeric(
    P, 4, mcse,
    {
        "independent": psd / 100,
        "one-chain": psd / math.sqrt(ess / 4),
        "no-plus-phi": psd / math.sqrt(2800),
        "square": psd / math.sqrt(10000 * 0.36 / 1.64),
    },
    printed=0.0222, feed=[0.8964 / math.sqrt(1627.9)],
)
ok(round(math.sqrt(1627.9), 2) == 40.35, f"{P} p4 root 40.35")
per_chain = (0.0222 / 0.01) ** 2 * 10000 / 4
exact_chain = (psd / 0.01) ** 2 * (1 + phi) / (1 - phi) / 4
numeric(
    P, 5, round(per_chain, -2),
    {"total": round(4 * per_chain, -2), "linear": 0.0222 / 0.01 * 2500, "no-ar": round((psd / 0.01) ** 2 / 4, -2)},
    printed=12300, feed=[per_chain, exact_chain],
)
ok(round((0.0222 / 0.01) ** 2, 2) == 4.93 and round(exact_chain / ((psd / 0.01) ** 2 / 4), 1) == 6.1, f"{P} p5 printed 4.93, 'six times'")
ok(near(wrong(P, 5)["total"]["value"], 4 * exact_chain, wrong(P, 5)["total"]["tol"]["abs"]), f"{P} p5 total takes the exact run")
lin = wrong(P, 5)["linear"]
finding(
    abs(round(lin["value"], -2) - lin["value"]) < lin["tol"]["abs"] - 1,
    f"{P} p5 `linear`: 5,550 to the nearest hundred is a tie (5,500 or 5,600), each exactly {lin['tol']['abs']} from the "
    f"slip value, on the edge of its band; the unrounded slip is {mcse/0.01*2500:.0f}",
)
# the Gibbs sampler itself, on planted estimates
rng = np.random.default_rng(72)
y = np.array([1.9, -0.6, 3.1, 0.8])
T = 400_000
mu = np.empty(T)
m = 0.0
for i in range(T):
    th = (m / tau2 + y / s2) / (1 / tau2 + 1 / s2) + math.sqrt(1 / (1 / tau2 + 1 / s2)) * rng.standard_normal(J)
    m = (th.sum() / tau2) / (J / tau2 + 1 / pr2) + math.sqrt(1 / (J / tau2 + 1 / pr2)) * rng.standard_normal()
    mu[i] = m
mu = mu[1000:]
r1 = np.corrcoef(mu[:-1], mu[1:])[0, 1]
r2 = np.corrcoef(mu[:-2], mu[2:])[0, 1]
ok(abs(r1 - 0.72) < 0.01 and abs(r2 - 0.72**2) < 0.012, f"{P} Gibbs lag-1 {r1:.4f}, lag-2 {r2:.4f}")
ok(abs(mu.std() - psd) < 0.01, f"{P} Gibbs sd of mu {mu.std():.4f} vs {psd:.4f}")
post_mean = (J * y.mean() / (s2 + tau2)) * post_var
ok(abs(mu.mean() - post_mean) < 5 * psd / math.sqrt(len(mu) * 0.28 / 1.72), f"{P} Gibbs mean {mu.mean():.4f} vs {post_mean:.4f}")
# Monte Carlo error of the mean of four chains of 2,500: exact AR(1) variance and simulation
nn = 2500
g = sum(2 * (1 - k / nn) * phi**k for k in range(1, nn))
exact_se = psd * math.sqrt((1 + g) / nn / 4)
ok(abs(exact_se - mcse) / mcse < 0.002, f"{P} exact finite-n error {exact_se:.5f} vs rule {mcse:.5f}")
rng = np.random.default_rng(17)
R = 3000
xx = psd * rng.standard_normal(R * 4)
tot = xx.copy()
inn = psd * math.sqrt(1 - phi**2)
for _ in range(nn - 1):
    xx = phi * xx + inn * rng.standard_normal(R * 4)
    tot += xx
pooled = (tot / nn).reshape(R, 4).mean(axis=1)
ok(abs(pooled.std() - mcse) < 4 * mcse / math.sqrt(2 * R), f"{P} simulated error of the pooled mean {pooled.std():.5f}")
ok(round(1 / math.sqrt(ess) * 40) == 1 and round(2 * mcse, 2) == 0.04, f"{P} p4 'a fortieth', '+/- 0.04'")

# changed lines of the kept problems, set 4
P = "p-etf-tracking"
ok(round(math.sqrt(0.04 + 0.0625), 4) == 0.3202 and 1 / 0.04 == 25 and 1 / 0.0625 == 16, f"{P} p1 line")
pm = (25 * -0.3 + 16 * -0.82) / 41
ok(round(pm, 4) == -0.5029 and round((-0.3 - 0.82) / 2, 2) == -0.56, f"{P} p2 lines")
pred_sd = math.sqrt(1.5**2 / 20 + 1 / 41)
ok(round(1.5 / math.sqrt(20), 4) == 0.3354 and round(pred_sd**2, 4) == 0.1369 and round(pred_sd, 4) == 0.3700, f"{P} p3 lines")
zs = {1.3435: 0.9104, 1.4821: 0.9308, 3.1825: 0.9993}
for zz, v in zs.items():
    ok(round(stats.norm.cdf(zz), 4) == v and f"\\Phi({zz}) = {v}" in part(P, 4)["question"], f"{P} p4 Phi({zz})")
ok(round((-0.5029 + 1) / 0.3700, 4) == 1.3435 and round((-0.5029 + 1) / 0.3354, 4) == 1.4821, f"{P} p4 the z values offered")
ok(near(key(P, 4), 1 - 0.9104, 1e-4) and near(wrong(P, 4)["plug-in"]["value"], 1 - 0.9308, 1e-4), f"{P} p4 bands take the given values")

P = "p-quality-six-markets"
ok(round(0.5 / (0.5 + math.sqrt(0.21)), 4) == 0.5218 and round(0.25 / 0.46, 4) == 0.5435, f"{P} p3 line")
ok(round(0.9 - 0.5435 * 1.1, 4) == 0.3022 and round(1 - 0.5435, 4) == 0.4565 and round(0.9 - 0.3022, 4) == 0.5978, f"{P} p4 lines")
shr = 0.9 - 0.5435 * 1.1 + 0  # kept-b slip
keep = 0.9 + (1 - 0.25 / 0.46) * (-0.2 - 0.9)
ok(round(keep, 4) == 0.3978, f"{P} p4 shrunk mean {keep:.4f}")
zs = {0.7956: 0.7869, 0.8680: 0.8073, 1.1776: 0.8805}
for zz, v in zs.items():
    ok(round(stats.norm.cdf(zz), 4) == v and f"\\Phi({zz}) = {v}" in part(P, 5)["question"].replace("0.8680", "0.868"), f"{P} p5 Phi({zz})")
post_sd6 = math.sqrt((1 - 0.25 / 0.46) * 0.25)
ok(round(keep / post_sd6, 4) == 1.1776, f"{P} p5 the key's z {0.3978/post_sd6:.4f}")
ok(near(key(P, 5), 0.8805, 1e-4) and near(wrong(P, 5)["lower"]["value"], 1 - 0.8805, 1e-4), f"{P} p5 bands take the given values")

# ------------------------------------------------- rules over every numeric part in scope
SCOPE = [
    "p-rfq-busy-minutes", "p-signal-variants", "p-two-looks", "p-hedge-ranks",
    "p-spread-day-tail", "p-iceberg-refills", "p-four-books",
]
for pid in SCOPE:
    for k, p in enumerate(ITEMS[pid]["parts"], 1):
        w = p["widget"]
        if w["kind"] != "numeric":
            continue
        q = p["question"]
        mdp = re.search(r"Give (\d) decimal places?", q)
        if mdp:
            dp = int(mdp.group(1))
            v = w["answer"] * 10**dp
            finding(
                abs(v - math.floor(v) - 0.5) > 0.005,
                f"{pid} p{k}: the key {w['answer']} is on a rounding tie at {dp} places",
            )
            ok(near(w["answer"], round(w["answer"], dp), w["tol"]["abs"]), f"{pid} p{k} band takes the key to {dp} places")
        ok("Give" in q or w["tol"]["abs"] == 0, f"{pid} p{k} states its form")
        ids = set(wrong(pid, k))
        ok(ids == set(p["feedback"].get("byKey", {})), f"{pid} p{k} each slip has its line")

print(f"{checks} checks, {fails} number checks failed, {findings + fails} FINDING lines")
sys.exit(0)
