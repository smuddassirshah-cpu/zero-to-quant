#!/usr/bin/env python3
"""Round 2 concept audit, limits-thm levels 1 to 3: recompute and simulate.

Independent of the round 1 script. Reads the content JSON, recomputes the
claims the ledger marks "script", and runs Monte Carlo checks for the
empirical claims. Exits 0 when every check passes. Checks in the KNOWN
section fail on purpose while a finding is unfixed.

Run from anywhere: python3 docs/reports/limits-thm-L1-3-concepts-r2.py
"""
import json
import math
import os
import sys
from math import comb, exp, log, sqrt, erf

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, "..", "..", "app", "content", "courses", "limits-thm")
fails = []
count = 0


def load(name):
    with open(os.path.join(C, name + ".json")) as f:
        return json.load(f)


def ok(label, cond):
    global count
    count += 1
    if not cond:
        fails.append(label)
        print("FAIL", label)


def near(label, got, want, tol=6e-5):
    ok(f"{label}: got {got!r}, content says {want!r}", abs(got - want) <= tol)


def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def binpmf(n, p, k):
    if 0 < p < 1 and n > 500:  # logs, so large n does not overflow
        return exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1) + k * log(p) + (n - k) * log(1 - p))
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def bintail(n, p, k):
    return sum(binpmf(n, p, j) for j in range(k, n + 1))


def poispmf(lam, k):
    return exp(-lam) * lam**k / math.factorial(k)


def poistail(lam, k):
    return 1 - sum(poispmf(lam, j) for j in range(k))


def hyp(k, N, K, n):
    return comb(K, k) * comb(N - K, n - k) / comb(N, n)


def wrongs(widget):
    return {w["id"]: w.get("value") for w in widget.get("wrong", [])}


def run_code(label, widget):
    """Solution passes every hidden test; the starter fails at least one."""
    def passes(src):
        ns = {}
        try:
            exec(src, ns)
            for t in widget["tests"]:
                got = eval(t["call"], ns)
                want = eval(t["expect"]) if isinstance(t["expect"], str) else t["expect"]
                if isinstance(want, list):
                    if len(got) != len(want) or not all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) for a, b in zip(got, want)):
                        return False
                elif not math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12):
                    return False
            return True
        except Exception:
            return False
    ok(label + " solution passes its tests", passes(widget["solution"]))
    ok(label + " starter fails its tests", not passes(widget["starter"]))


rng = np.random.default_rng(20261112)

# ---------------------------------------------------------------- L1
l1 = load("l1-counting-successes")
s = l1["screens"]
near("l1 s4 P(X=3) Bin(5,.6)", binpmf(5, 0.6, 3), 0.3456)
near("l1 s5 P(X=2) Bin(4,.5)", binpmf(4, 0.5, 2), 0.375)
near("l1 s8 sd", sqrt(20 * 0.55 * 0.45), s[8]["widget"]["answer"], 2e-3)
near("l1 s8 no-q", sqrt(11), wrongs(s[8]["widget"])["no-q"], 5e-4)
t15 = bintail(20, 0.55, 15)
near("l1 s9 tail", t15, 0.0553)
ok("l1 s9 once in 18 weeks", round(1 / t15) == 18)
near("l1 s10 no defaults", 0.98**50, s[10]["widget"]["answer"])
near("l1 q2 sd", sqrt(21), 4.583, 5e-4)
run_code("l1 s9", s[9]["widget"])
# MC: positive dependence puts more weight on extreme counts than the binomial
# (l1 quiz q-same-stock, l1 s10 explain). One-factor model, marginal p = 0.4.
reps = 200_000
common = rng.standard_normal(reps)[:, None]
idio = rng.standard_normal((reps, 10))
z = sqrt(0.6) * common + sqrt(0.4) * idio
x = (z < stats.norm.ppf(0.4)).sum(axis=1)
ext_dep = np.mean((x <= 1) | (x >= 9))
ext_bin = sum(binpmf(10, 0.4, k) for k in (0, 1, 9, 10))
ok("MC l1 dependent funds land near 0 or 10 far more often", ext_dep > 3 * ext_bin)
ok("MC l1 marginal chance stays 0.4", abs(x.mean() / 10 - 0.4) < 0.005)

# ---------------------------------------------------------------- L2
l2 = load("l2-first-success")
s = l2["screens"]
near("l2 s1", 0.8 * 0.8 * 0.2, 0.128)
near("l2 s4 opt", 0.8**5, 0.328, 5e-4)
near("l2 s5 bar 10", 0.8**9 * 0.2, 0.027, 5e-4)
near("l2 s10", 1 - 0.95**10, 0.4013)
near("l2 s10 tenth", 0.95**9 * 0.05, 0.0315)
near("l2 q0", 25 / 216, 0.1157)
near("l2 q2", (5 / 6) ** 6, 0.335, 5e-4)
near("l2 q2 opt", (5 / 6) ** 10, 0.162, 5e-4)
# geometric mean 1/p by series
ok("l2 mean 1/p", abs(sum(k * 0.8 ** (k - 1) * 0.2 for k in range(1, 2000)) - 5) < 1e-9)

# ---------------------------------------------------------------- L3
l3 = load("l3-rare-events")
near("l3 s1", 0.8**10, 0.1074)
near("l3 s2 n=50", (1 - 2 / 50) ** 50, 0.1299)
near("l3 s2 n=500", (1 - 2 / 500) ** 500, 0.1348)
near("l3 s3", poispmf(2, 2), 0.2707)
near("l3 s3 ten slots", binpmf(10, 0.2, 2), 0.302, 5e-4)
near("l3 s3 500 slots", binpmf(500, 0.004, 2), 0.2712)
near("l3 s4", exp(-1.5), 0.2231)
near("l3 s8", poistail(3, 6), 0.0839)
near("l3 s8 P5", poispmf(3, 5), 0.1008)
near("l3 s8 P6", poispmf(3, 6), 0.0504)
ok("l3 s8 one hour in twelve", round(1 / poistail(3, 6)) == 12)
near("l3 s9 tail", poistail(2, 6), 0.0166)
ok("l3 s9 about 4 days", round(250 * poistail(2, 6)) == 4)
near("l3 q2 exact binomial", binpmf(1000, 0.002, 1), 0.2707)
near("l3 q3", exp(-3) / 3, 0.0166)
ok("l3 q0 once in 55 days", round(1 / exp(-4)) == 55)
# MC: clustered (mixed) Poisson has variance above the mean and a fat right tail
lam = rng.gamma(shape=1.0, scale=2.0, size=400_000)
jumps = rng.poisson(lam)
ok("MC l3 clustering gives variance above mean", jumps.var() > 2 * jumps.mean())
ok("MC l3 clustering gives more 6+ days", np.mean(jumps >= 6) > 3 * poistail(2, 6))

# ---------------------------------------------------------------- L4
l4 = load("l4-without-replacement")
s = l4["screens"]
near("l4 s2", hyp(2, 10, 4, 3), 0.3)
for N, want in ((20, 0.2817), (100, 0.3193), (1000, 0.3269)):
    near(f"l4 P0 N={N}", hyp(0, N, N // 5, 5), want)
near("l4 gap 20", 0.8**5 - hyp(0, 20, 4, 5), 0.0459, 1e-4)
near("l4 gap 100", 0.8**5 - hyp(0, 100, 20, 5), 0.0084, 1e-4)
near("l4 gap 1000", 0.8**5 - hyp(0, 1000, 200, 5), 0.0008, 1e-4)
var_h = sum((k - 1) ** 2 * hyp(k, 20, 4, 5) for k in range(5))
near("l4 s6 variance", var_h, 0.6316)
tail4 = sum(hyp(k, 100, 20, 10) for k in range(4, 11))
near("l4 s10 tail", tail4, 0.1096)
ok("l4 s10 one in nine", round(1 / tail4) == 9)
near("l4 s10 binomial", bintail(10, 0.2, 4), 0.1209)
near("l4 q0", hyp(1, 52, 4, 5), 0.2995)
near("l4 q0 binomial", binpmf(5, 1 / 13, 1), 0.2792)
run_code("l4 s10", s[10]["widget"])

# ---------------------------------------------------------------- L5
near("l5 s8 VaR", 10 - sqrt(5), 7.764, 1e-3)
u = np.linspace(0, 5, 200001)
payoff = np.trapezoid(u * (5 - u) / 100, u)
near("l5 s9 payoff", payoff, 0.2083, 1e-4)
u = np.linspace(0, 10, 200001)
near("l5 s9 strike 100", np.trapezoid(u * (10 - u) / 100, u), 1.6667, 1e-4)

# ---------------------------------------------------------------- L6
near("l6 s4 check", exp(-1.4), 0.2466)
near("l6 s9", exp(-0.1), 0.9048)
near("l6 s9 annual", 0.98**5, 0.9039)
near("l6 s10 sd", 8 / sqrt(12), 2.309, 1e-3)
near("l6 q3 median s", 60 * log(2) / 2, 20.8, 0.05)

# ---------------------------------------------------------------- L7
l7 = load("l7-bell-curve")
s = l7["screens"]
near("l7 one sd", Phi(1) - Phi(-1), 0.6827)
near("l7 s3 no-mu", Phi(-1.6), 0.0548)
near("l7 s8", Phi(-3.05 / 1.2), 0.0055)
near("l7 s8 var", Phi(-3.05 / 1.44), 0.0171)
near("l7 s9 r", (0.05 - 2.326 * 1.2) / 100, s[9]["widget"]["answer"], 1e-5)
near("l7 q2 a", Phi(-1 / 3), 0.3694)
near("l7 q2 b", Phi(2 / 3), 0.7475)
p41 = bintail(2520, 0.01, 41)
ok(f"l7 s10 41+ breaches about 1 in 450 (got 1 in {1/p41:.0f})", 380 < 1 / p41 < 520)
ratio = Phi(-0.5) / Phi(-2)
# the lesson says 13 times; the ratio is 13.56. See KNOWN below.
run_code("l7 s5", s[5]["widget"])
# fat tails: a t3 return scaled to the normal's sd breaches a normal 99% VaR more often
p_t3 = stats.t.cdf(-2.326 * sqrt(3), 3)
ok("l7 s10 fat tails breach a normal 99% VaR more than 1%", p_t3 > 0.0125)
ok("l7 s10 t3 keeps far more area beyond -3", stats.t.cdf(-3, 3) > 10 * Phi(-3))

# ---------------------------------------------------------------- L8
near("l8 s1 mean at 0.8", 100 * exp(0.32), 137.71, 6e-3)
near("l8 s2 median", exp(4.7), 109.95, 6e-3)
near("l8 s4 mean", exp(4.745), 115.01, 6e-3)
sdS = 54.164 * sqrt(exp(0.16) - 1)
near("l8 s6 normal option", 1 - Phi((50 - 50 * exp(0.08)) / sdS), 0.5732, 2e-4)
z = (log(1.2) - 0.03) / 0.2
near("l8 s8", 1 - Phi(z), 0.2231)
m1 = 100 * exp(0.05)
sd1 = m1 * sqrt(exp(0.04) - 1)
near("l8 s8 normal", 1 - Phi((120 - m1) / sd1), 0.2419, 2e-4)
near("l8 s8 no-drag", 1 - Phi((log(1.2) - 0.05) / 0.2), 0.2541)
near("l8 s8 simple", 1 - Phi((0.2 - 0.03) / 0.2), 0.1977)
near("l8 s8 no-drift", 1 - Phi(log(1.2) / 0.2), 0.181, 1e-4)
near("l8 s9", Phi(0.1), 0.5398)
near("l8 q1", 1 - Phi(0.25), 0.4013)
near("l8 q3", 100 * exp(0.055), 105.65, 6e-3)
# MC: lognormal mean, median and P(S < mean)
zz = rng.standard_normal(2_000_000)
S = 100 * np.exp(0.03 + 0.2 * zz)
ok("MC l8 mean is S0 e^m", abs(S.mean() - m1) < 0.06)
ok("MC l8 median is S0 e^(m - s^2/2)", abs(np.median(S) - 100 * exp(0.03)) < 0.06)
ok("MC l8 below mean 54% of the time", abs(np.mean(S < m1) - 0.5398) < 0.002)

# ---------------------------------------------------------------- L9
l9 = load("l9-averages-settle")
s = l9["screens"]
ser = {x["id"]: x["values"] for x in s[0]["canvas"]["params"]["series"]}
ok("l9 s0 after 10", [round(ser[k][9], 2) for k in ("ann", "ben", "cal")] == [4.5, 2.6, 3.7])
ok("l9 s0 after 1000", [round(ser[k][999], 2) for k in ("ann", "ben", "cal")] == [3.56, 3.43, 3.5])
card = s[1]["canvas"]["params"]["series"][0]["values"]
ok("l9 s1 card 100 and 2000", round(card[99], 2) == 0.5 and round(card[1999], 2) == 0.98)
# exact chance a die average is far (more than 0.25 from 3.5)


def far(n):
    pmf = np.array([1.0])
    die = np.ones(6) / 6
    for _ in range(n):
        pmf = np.convolve(pmf, die)
    tot = np.arange(n, 6 * n + 1)
    return pmf[np.abs(tot / n - 3.5) > 0.25 + 1e-12].sum()


vals = s[2]["canvas"]["state"]["values"]
near("l9 s2 far n=10", far(10), vals["n10"])
near("l9 s2 far n=100", far(100), vals["n100"])
f1000 = far(1000)
ok(f"l9 s2 far n=1000 about 0.0000034 (got {f1000:.2e})", 3.0e-6 < f1000 < 3.9e-6)
sh = s[3]["canvas"]["left"]["params"]["series"][0]["values"]
gp = s[3]["canvas"]["right"]["params"]["series"][0]["values"]
ok("l9 s3 share and gap data", abs(sh[9] - 0.491) < 1e-9 and abs(sh[99] - 0.4958) < 1e-9 and gp[9] == -18 and gp[99] == -84)
near("l9 s6", sqrt(35 / 12 / 100), 0.171, 2e-3)
stp = s[7]["canvas"]["params"]["series"][0]["values"]
ok(f"l9 s7 St Petersburg near 13 at 1,000 games (got {stp[99]})", 12 <= stp[99] <= 14)
ok(f"l9 s7 about 42 at 2,550 games (got {stp[254]})", 40 <= stp[254] <= 44)
near("l9 s9 sd", sqrt(100 - (10 / 37) ** 2) * sqrt(1e5), 3161, 1.5)
ok("l9 s9 zero is 8.5 sds below", abs((1e6 / 37) / 3161 - 8.55) < 0.05)
near("l9 q2 sd of one policy", 5000 * sqrt(0.01 * 0.99), 497, 1)
# MC: the count gap wanders while the share settles (s3 key)
steps = rng.choice([-1, 1], size=(20000, 9000)).sum(axis=1)
gap = -18 + steps
ok("MC l9 gap typically further from 0 after 10,000", np.mean(np.abs(gap) > 18) > 0.8)
ok("MC l9 positive gap is less likely than not", np.mean(gap > 0) < 0.5)
# MC: St Petersburg averages do not settle; they keep growing (about log2 n)
k = rng.geometric(0.5, size=(400, 2**16)).astype(float)
win = 2.0**k
med_small = np.median(win[:, : 2**8].mean(axis=1))
med_big = np.median(win.mean(axis=1))
ok(f"MC l9 St Petersburg median average grows ({med_small:.1f} then {med_big:.1f})", med_big > med_small + 5)
# MC: Cauchy averages do not settle (summary)
ca = rng.standard_cauchy((2000, 10000)).mean(axis=1)
iqr = np.subtract(*np.percentile(ca, [75, 25]))
ok("MC l9 Cauchy average has the spread of one draw", 1.7 < iqr < 2.3)

# ---------------------------------------------------------------- L10
near("l10 s6 normal 1.5", 2 * (1 - Phi(1.5)), 0.1336)
near("l10 s6 normal 2", 2 * (1 - Phi(2)), 0.0455)
near("l10 s6 normal 3", 2 * (1 - Phi(3)), 0.0027)
ok("l10 s9 normal n = 1,083", math.ceil((1.645 * 2 / 0.1) ** 2) == 1083)
ok("l10 s9 Chebyshev n = 4,000", abs(4 / (0.1 * 0.01) - 4000) < 1e-6)
# Markov can fail for a variable that takes negative values (s4)
ok("l10 s4 counterexample", 0.5 > 1 / 5 and 0.5 * 10 - 0.5 * 8 == 1)
# Markov bound may exceed 1 and still be valid (see KNOWN: l10 s3 flipped)
ok("l10 Markov bound above 1 is valid but empty", 2 / 1 > 1)

# ---------------------------------------------------------------- L11
l11 = load("l11-sums-look-normal")
s = l11["screens"]
P = s[0]["canvas"]["params"]["params"]
# bins of width 0.5 from -3: bin j covers [-3 + j/2, -2.5 + j/2)
for n in (1, 3, 30):
    g = stats.gamma(n)
    for j in (3, 4, 5, 9):
        lo, hi = -3 + j / 2, -2.5 + j / 2
        want = g.cdf(max(n + hi * sqrt(n), 0)) - g.cdf(max(n + lo * sqrt(n), 0))
        near(f"l11 s0 exp bars n={n} bin {j}", want, P[f"e{j}"][n], 1.5e-4)
near("l11 s2 normal below -1.5", Phi(-1.5), 0.07, 5e-3)
# uniform n=3 bars within 0.01 of the normal (Irwin-Hall by simulation-free convolution)
U = s[2]["canvas"]["right"]["params"]["params"]
normbin = [Phi(-2.5 + j / 2) - Phi(-3 + j / 2) for j in range(14)]
ok("l11 s2 uniform at 3 within 0.01 of each dash", all(abs(U[f"u{j}"][3] - normbin[j]) < 0.01 for j in range(14)))
uu = rng.random((2_000_000, 3)).mean(axis=1)
zu = (uu - 0.5) / sqrt(1 / 36)
near("MC l11 uniform n=3 middle bar", np.mean((zu >= 0) & (zu < 0.5)), U["u6"][3], 1.2e-3)
near("l11 s1 sd", sqrt(30), 5.48, 5e-3)
near("l11 s6 normal", 1 - Phi(10 / sqrt(50)), 0.0786)
near("l11 s6 exact gamma", stats.gamma(50).sf(60), 0.0844)
near("l11 s9 sd-n", Phi(-0.05), 0.4801)
near("l11 q2", 1 - Phi(20 / sqrt(100 * 35 / 12)), 0.121, 1e-3)
# MC: clustering slows the approach to normal (s8). GARCH(1,1) days with
# fat-tailed (t8) shocks, the empirically relevant case: 20-day sums are closer
# to normal than days, and less close than sums of the same days shuffled.
# Note for the audit: with normal shocks and strong clustering the 20-day
# kurtosis can exceed the daily one (printed below, not a check), so the
# lesson's claim rests on real daily returns being fat-tailed day by day.


def garch(al, be, shocks, burn=1000):
    r = np.empty(len(shocks))
    h = 1.0
    om = 1 - al - be
    for i, e in enumerate(shocks):
        r[i] = sqrt(h) * e
        h = om + al * r[i] ** 2 + be * h
    return r[burn:]


T = 600_000
sh_t = stats.t.rvs(8, size=T + 1000, random_state=rng) / sqrt(8 / 6)
r = garch(0.05, 0.90, sh_t)
shuf = rng.permutation(r)
k_day = stats.kurtosis(r)
k20_c = stats.kurtosis(r.reshape(-1, 20).sum(axis=1))
k20_i = stats.kurtosis(shuf.reshape(-1, 20).sum(axis=1))
ok(f"MC l11 20-day sums closer to normal than days ({k_day:.2f} to {k20_c:.2f})", k20_c < 0.7 * k_day)
ok(f"MC l11 clustering slows the approach ({k20_c:.2f} against {k20_i:.2f})", k20_c > k20_i + 0.2)
rn = garch(0.10, 0.85, rng.standard_normal(T + 1000))
print(f"note: normal-shock GARCH(0.10, 0.85) excess kurtosis, daily {stats.kurtosis(rn):.2f}, 20-day {stats.kurtosis(rn.reshape(-1, 20).sum(axis=1)):.2f}")

# ---------------------------------------------------------------- L12
near("l12 s1 chance", 1 - Phi(0.12 * sqrt(63)), 0.17, 5e-3)
near("l12 s2 t", 0.06 * sqrt(1008), 1.9, 1e-2)
near("l12 s2 caption", 1 - Phi(0.06 * sqrt(1008)), 0.028, 5e-4)
near("l12 s4 P(t>2.5)", 1 - Phi(2.5), 0.006, 5e-4)
ok("l12 s4 one in 160", abs(1 / (1 - Phi(2.5)) - 160) < 3)
near("l12 s5 SR", 0.05 * sqrt(252), 0.79, 5e-3)
near("l12 s7", 1 - (1 - 0.0455) ** 20, 0.606, 5e-4)
near("l12 s9", Phi(-1.26 / (0.1 * sqrt(252))), 0.2136, 1e-4)
# MC: t with the sample sd is close to N(0,1) over hundreds of days, even for
# fat-tailed (t5) daily returns (s4)
x = stats.t.rvs(5, size=(40_000, 500), random_state=rng)
tt = x.mean(axis=1) / (x.std(axis=1, ddof=1) / sqrt(500))
ok(f"MC l12 P(|t|>2) near 0.0455 (got {np.mean(np.abs(tt) > 2):.4f})", abs(np.mean(np.abs(tt) > 2) - 0.0455) < 0.006)
# MC: standard error of an annualised Sharpe ratio is about 1/sqrt(T) (s5, s8)
Ty = 4
d = 0.0005 + 0.01 * rng.standard_normal((40_000, 252 * Ty))
sr = d.mean(axis=1) / d.std(axis=1, ddof=1) * sqrt(252)
ok(f"MC l12 SE of Sharpe near 1/sqrt(T) (got {sr.std():.3f})", abs(sr.std() - 0.5) < 0.02)
ok("MC l12 a true 0.79 Sharpe clears t=2 about half the time at 6.35 years",
   abs(np.mean((0.0005 + 0.01 * rng.standard_normal((20_000, 1600))).mean(axis=1) * 40 / 0.01 > 2) - 0.5) < 0.02)

# ---------------------------------------------------------------- L13
sd = sqrt(20 * 0.55 * 0.45)
near("l13 s2", 1 - Phi(3.5 / sd), 0.0578, 1.5e-4)
near("l13 s2 at15", 1 - Phi(4 / sd), 0.0361)
near("l13 s2 at155", 1 - Phi(4.5 / sd), 0.0216)
near("l13 s4 normal", Phi(-2.5 / sd), 0.1306)
near("l13 s4 exact", 1 - bintail(20, 0.55, 9), 0.1308)
near("l13 s5 exact", binpmf(20, 0.55, 12), 0.162, 5e-4)
near("l13 s5 normal", Phi(1.5 / sd) - Phi(0.5 / sd), 0.161, 5e-4)
near("l13 s7 exact", bintail(100, 0.02, 5), 0.0508)
near("l13 s7 Poisson", poistail(2, 5), 0.0527)
near("l13 s7 normal", 1 - Phi(2.5 / 1.4), 0.0371)
near("l13 s8 exact", bintail(100, 0.5, 60), 0.0284)
near("l13 s9 exact", bintail(1000, 0.02, 30), 0.0207)
near("l13 s9 Poisson", poistail(20, 30), 0.0218)
near("l13 s9 normal", 1 - Phi(9.5 / sqrt(19.6)), 0.0159)
near("l13 s9 var", 1 - Phi(9.5 / 19.6), 0.314, 5e-4)
near("l13 q2 exact", binpmf(100, 0.5, 50), 0.0796)

# ---------------------------------------------------------------- reviews
near("r1 two hearts", hyp(2, 52, 13, 5), 0.2743)
near("r1 fpc", 1.6 * 40 / 49, 1.3061)
near("r2 lognormal sigma", sqrt(2 * log(1.1)), 0.4366)
near("r2 two years", Phi(-0.07 / (0.3 * sqrt(2))), 0.4345, 1.5e-4)
near("r2 two years no-drag", Phi(-0.16 / (0.3 * sqrt(2))), 0.353, 5e-4)
near("r2 two years no-root", Phi(-0.07 / 0.6), 0.4536)
near("r3 binom tail exact", bintail(50, 0.4, 25), 0.0978)
near("r3 window exact", sum(binpmf(40, 0.5, k) for k in range(18, 23)), 0.5704)
near("r3 flukes", 1 - 0.9772**50, 0.68, 6e-3)
near("r3 one trade", Phi(-20 / 150), 0.447, 5e-4)

# ---------------------------------------------------------------- homework
near("h1 two defaults", 1 - 0.98**50 - 50 * 0.02 * 0.98**49, 0.2642)
near("h1 bad trades", 1 - comb(45, 10) / comb(50, 10), 0.6894)
near("h1 capped wait", (1 - 0.85**10) / 0.15, 5.354, 5e-4)
m, p, q = 10, 0.15, 0.85
ET = sum(k * q ** (k - 1) * p for k in range(1, m)) + m * q ** (m - 1)
near("h1 capped wait by the series", ET, (1 - q**m) / p, 1e-12)
near("h2 two quantiles", 30 / (stats.norm.ppf(0.95) + stats.norm.ppf(0.9)), 10.25, 5e-3)
z1, z2 = (log(0.9) - 0.03) / 0.2, (log(1.1) - 0.03) / 0.2
near("h2 price band", Phi(z2) - Phi(z1), 0.3787)
sd1 = m1 * sqrt(exp(0.04) - 1)
near("h2 price band normal", Phi((110 - m1) / sd1) - Phi((90 - m1) / sd1), 0.3526, 2e-4)
near("h2 VaR", 1e6 * (1 - exp(0.03 - 2.326 * 0.2)), 352900, 60)
near("h2 VaR no-mean", 1e6 * (1 - exp(-2.326 * 0.2)), 371990, 60)
near("h2 cycles n=10", 0.95**40, 0.1285)
near("h2 cycles n=100", 0.995**400, 0.1347)
near("h3 defaults exact", bintail(400, 0.05, 30), 0.0190)
near("h3 best of 10", 1 - (1 - (1 - Phi(1.30))) ** 10, 0.64, 5e-3)
h3 = load("homework-3")
code = next(i for i in h3["items"] if i["id"] == "h-tail-code")
run_code("h3 tail code", code["widget"])


def desk(n):
    a = np.array([binpmf(n, 0.55, k) for k in range(n + 1)])
    b = np.array([binpmf(n, 0.3, k) for k in range(n + 1)])
    ca = np.cumsum(a)
    tot = 0.0
    for wb in range(n + 1):
        lim = n - 2 * wb
        if lim < 0:
            break
        tot += b[wb] * ca[min(lim, n)]
    return tot


near("h3 desk exact n=131", desk(131), 0.0528)
first = next(n for n in range(100, 200) if desk(n) <= 0.05)
ok(f"h3 desk first n at or below 0.05 is 136 (got {first})", first == 136)
ok("h3 desk stays below for larger n (to 600)", all(desk(n) <= 0.05 for n in range(136, 601)))
# MC: positive serial correlation makes sigma/sqrt(n) understate the error of a mean
phi_ar = 0.2
eps = rng.standard_normal((20_000, 378 + 200))
ar = np.empty_like(eps)
ar[:, 0] = eps[:, 0]
for i in range(1, eps.shape[1]):
    ar[:, i] = phi_ar * ar[:, i - 1] + eps[:, i]
ar = ar[:, 200:]
naive = ar.std() / sqrt(378)
ok("MC h3 positive autocorrelation: naive standard error is too small", ar.mean(axis=1).std() > 1.15 * naive)

# ---------------------------------------------------------------- problems
near("p1 no drop", 0.996**400, 0.2012)
near("p1 alarm", poistail(1.6, 4), 0.0788)
near("p1 from three", poistail(1.6, 3), 0.2166)
near("p1 from five", poistail(1.6, 5), 0.0237)
near("p1 from six", poistail(1.6, 6), 0.0060)
near("p1 session", 0.9212**30, 0.0852)
near("p1 fund 10+", bintail(12, 0.65, 10), 0.1513)
near("p1 settle var", 1.455 * 1950 / 1999, 1.4193)
near("p1 settle exact clean", hyp(0, 2000, 60, 50), 0.2139)
ok("p1 settle binomial n = 152", math.ceil(log(0.01) / log(0.97)) == 152)
near("p1 settle at 151", 1 - 0.97**151, 0.98994, 1e-5)
first = next(n for n in range(100, 200) if 1 - hyp(0, 2000, 60, n) >= 0.99)
ok(f"p1 settle exact n = 146 (got {first})", first == 146)
near("p2 digital unrounded", 1 - Phi((log(1.25) - 0.015) / 0.3), 0.2439)
near("p2 VaR", 80 - 80 * exp(0.015 - 1.645 * 0.3), 30.42, 6e-3)
near("p2 VaR two-tailed", 80 - 80 * exp(0.015 - 1.96 * 0.3), 34.89, 6e-3)
near("p2 triangle 99", 6 - sqrt(0.72), 5.15, 6e-3)
near("p2 default drag", exp(-0.05) * 40 * exp(0.04), 39.60, 6e-3)
near("p3 exact binomial", bintail(250, 0.0228, 10), 0.0626)
near("p3 Poisson", poistail(5.7, 10), 0.0648)
near("p3 calls exact", bintail(400, 0.5, 216), 0.0605)
cut = 1 - 0.95 ** (1 / 12)
ok("p3 cut-off 227 by exact binomial", bintail(400, 0.5, 227) < cut < bintail(400, 0.5, 226))
near("p3 twelve", 1 - 0.9394**12, 0.5277)
ok("p3 normal n = 62", math.ceil((1.96 * 4) ** 2) == 62)

# ---------------------------------------------------------------- KNOWN
# These fail on purpose until the finding is fixed.
r2 = load("review-2")
par = next(i for i in r2["items"] if i["id"] == "r-pareto-mean")
half = wrongs(par["widget"])["half"]
x = np.linspace(1, 4000, 4_000_001)
named = 2 / 3  # integral of (2/x^3)(1/x) from 1 to infinity
ok(f"KNOWN F1 review-2 r-pareto-mean slip 'half' is {half}, but the feedback's integral is {named:.4f}",
   abs(half - named) < 5e-4 or "times $\\tfrac{1}{x}$" not in par["feedback"]["byKey"]["half"])
ok("KNOWN F2 l1 s7 explain states independence as needed for variances to add",
   "the covariances stay and this sum is wrong" not in l1["screens"][7]["explain"]["text"])
l8 = load("l8-lognormal")
ok("KNOWN F3 l8 s0 slip 75 feedback names an unlikely route (the average of +100 and -50 is +25)",
   "then took off 50" not in l8["screens"][0]["feedback"]["byKey"]["drop"])
l10 = load("l10-bound-that-holds")
ok("KNOWN F4 l10 s3 says a probability bound cannot exceed 1",
   "A probability bound cannot exceed 1" not in l10["screens"][3]["feedback"]["byKey"]["flipped"])
ok("KNOWN F5 l10 summary trap says Markov fails (it can fail)",
   "Markov fails for variables" not in l10["summary"]["trap"])
ok(f"KNOWN F6 l7 s4 says 13 times; the ratio is {ratio:.2f}",
   "13 times likelier" not in l7["screens"][4]["explain"]["text"])
ok(f"KNOWN F7 l3 s4 says about one module in five; e^-1.5 is {exp(-1.5):.3f}",
   "About one module in five" not in l3["screens"][4]["feedback"]["byKey"]["zero"])
p3 = load("problems-3")
mk = next(i for i in p3["items"] if i["id"] == "p-maker-days")
ok("KNOWN F8 problems-3 says the theorem needs enough spread",
   "The theorem needs enough spread" not in mk["parts"][3]["widget"]["options"][2]["why"])
ok("KNOWN F9 problems-3 says a 2.3% day almost never happens",
   "almost never" not in mk["parts"][1]["explain"]["text"])
ok("KNOWN F10 l9 s0 infers settling from small steps alone",
   "moves a long average very little, so the lines settle" not in l9["screens"][0]["explain"]["text"])

ok("KNOWN F11 l11 s8 says infinite variance would block the limit entirely (it can)",
   "would block it entirely" not in l11["screens"][8]["explain"]["text"])
# t with 2 degrees of freedom has infinite variance, yet its sums are attracted
# to the normal with scaling sqrt(n log n): the kurtosis-free check below compares
# central quantile ratios of scaled sums with the normal's (finding 11 basis).
t2 = stats.t.rvs(2, size=(4000, 20000), random_state=rng).sum(axis=1)
q = np.percentile(t2, [75, 90, 97.5])
ok(f"finding 11 basis: t2 sums have normal-like quantile ratios ({q[1]/q[0]:.2f}, {q[2]/q[0]:.2f})",
   abs(q[1] / q[0] - 1.2816 / 0.6745) < 0.25 and abs(q[2] / q[0] - 1.96 / 0.6745) < 0.5)

print(f"{count} checks, {len(fails)} failed")
sys.exit(1 if fails else 0)
