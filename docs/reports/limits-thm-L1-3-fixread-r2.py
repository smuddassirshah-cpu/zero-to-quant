#!/usr/bin/env python3
"""Fix-pass read, limits-thm L1-3 round 2: recompute every figure the changed sentences state or rely on.
Exits 0 when the content agrees. Run from the repo root."""
import json, math, re, sys
from fractions import Fraction
from scipy import stats, integrate
import numpy as np

C = "app/content/courses/limits-thm/"
fails = []
def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + str(detail) if detail != "" else ""))
    if not ok: fails.append(name)
def load(f): return json.load(open(C + f))

# review-2 r-pareto-mean: f(x) = 2/x^3 on [1, inf)
it = [i for i in load("review-2.json")["items"] if i["id"] == "r-pareto-mean"][0]
w = it["widget"]; slips = {s["id"]: s for s in w["wrong"]}
area = integrate.quad(lambda x: 2 / x**3, 1, np.inf)[0]
mean = integrate.quad(lambda x: 2 / x**2, 1, np.inf)[0]
div = integrate.quad(lambda x: 2 / x**4, 1, np.inf)[0]
# exact antiderivatives: [-1/x^2] = 1, [-2/x] = 2, [-2/(3x^3)] = 2/3
check("pareto density integrates to 1", abs(area - 1) < 1e-9, area)
check("pareto key 2", abs(mean - 2) < 1e-9 and w["answer"] == 2, mean)
check("pareto slip area = 1", abs(slips["area"]["value"] - area) < 1e-9)
check("pareto slip half = int 2/x^4 = 2/3", abs(div - 2 / 3) < 1e-9 and abs(slips["half"]["value"] - 2 / 3) < 5e-5, div)
vals = [w["answer"]] + [s["value"] for s in w["wrong"]]
tol = w["tol"]["abs"] + max(s["tol"]["abs"] for s in w["wrong"])
check("pareto key and slips pairwise distinct beyond tolerance",
      all(abs(a - b) > tol for i, a in enumerate(vals) for b in vals[i + 1:]), vals)
fb = it["feedback"]["byKey"]["half"]
check("pareto feedback names 2/x^4 and 2/3", "\\tfrac{2}{x^4}" in fb and "\\tfrac23" in fb)

# l3: e^-1.5 against "more than one module in five"
p0 = math.exp(-1.5)
check("l3 e^-1.5 = 0.2231 > 1/5", abs(p0 - 0.2231) < 5e-5 and p0 > 0.2, p0)

# l7: ratio of Phi(-0.5) to Phi(-2), "nearly 14 times"
r_exact = stats.norm.cdf(-0.5) / stats.norm.cdf(-2); r_shown = 0.3085 / 0.0228
check("l7 ratio rounds to 14 and is below 14", round(r_exact) == 14 and round(r_shown) == 14 and r_exact < 14, (r_exact, r_shown))

# l8: 75 = half of (100 + 50); key 125
check("l8 75 = (100+50)/2, key 125", (100 + 50) / 2 == 75 and (200 + 50) / 2 == 125)

# l9 screen 0: caption figures from the canvas data; partial sums of misses are O(sqrt n)
s0 = load("l9-averages-settle.json")["screens"][0]
P = s0["canvas"]["params"]["params"]
got = [round(P[k][9], 2) for k in "abc"] + [round(P[k][999], 2) for k in "abc"]
check("l9 s0 averages 4.50 2.60 3.70 then 3.56 3.43 3.50", got == [4.5, 2.6, 3.7, 3.56, 3.43, 3.5], got)
rng = np.random.default_rng(7); n = 1000
tot = np.abs((rng.integers(1, 7, size=(20000, n)) - 3.5).sum(axis=1))
sd1 = math.sqrt(35 / 12)
check("l9 s0 misses partly cancel: mean |sum of misses| ~ sd*sqrt(2n/pi), far below n*E|miss| = 1.5n",
      abs(tot.mean() - sd1 * math.sqrt(2 * n / math.pi)) < 1.0 and tot.mean() < 0.05 * 1.5 * n, tot.mean())

# l9 screen 7: St Petersburg mean diverges (each term 1)
check("l9 s7 each term 2^k * 2^-k = 1", all(Fraction(2**k, 2**k) == 1 for k in range(1, 60)))

# l9 screen 8: 2%/sqrt(20), 2%/sqrt(2000); a 0.1% edge is well inside one sd of the 20-trade average
f20, f2000 = 2 / math.sqrt(20), 2 / math.sqrt(2000)
check("l9 s8 fuzz 0.447% and 0.0447%", abs(f20 - 0.447) < 5e-4 and abs(f2000 - 0.0447) < 5e-5, (f20, f2000))
z = 0.1 / f20
check("l9 s8 edge 0.1% is 0.22 sd of the 20-trade average; P(average <= 0) about 41% under a normal",
      z < 0.5 and 0.38 < stats.norm.cdf(-z) < 0.44, (z, stats.norm.cdf(-z)))
check("l9 s8 ratio of fuzz is 10 for 100 times the trades", abs(f20 / f2000 - 10) < 1e-9)

# l10 screen 3: Markov 2/10, flipped 10/2
check("l10 s3 Markov 0.2, flipped 5", 2 / 10 == 0.2 and 10 / 2 == 5)
# l10 screen 8: 250/9, normal, Student t4 at 3 of its own sds (sd = sqrt(nu/(nu-2)) = sqrt 2), two-sided
check("l10 s8 Chebyshev 250/9 = 27.8", abs(250 / 9 - 27.8) < 0.05)
pn = 2 * stats.norm.sf(3)
check("l10 s8 normal 0.0027 -> 0.7 days", abs(pn - 0.0027) < 5e-5 and abs(250 * pn - 0.7) < 0.05, 250 * pn)
sd4 = math.sqrt(4 / 2); d4 = 250 * 2 * stats.t.sf(3 * sd4, 4)
sim = np.random.default_rng(11).standard_t(4, size=4_000_000)
d4sim = 250 * np.mean(np.abs(sim) > 3 * sd4)
check("l10 s8 t4, own sd, two-sided, 250 days: about 3.3, rounds to 3", round(d4) == 3 and abs(d4 - d4sim) < 0.15, (d4, d4sim))
print("     note t4 beyond 3 scale units (not sds):", 250 * 2 * stats.t.sf(3, 4), "days; one-sided, own sd:", d4 / 2)
tab = {nu: round(250 * 2 * stats.t.sf(3 * math.sqrt(nu / (nu - 2)), nu), 2) for nu in (2.01, 2.05, 2.1, 2.5, 3, 4, 6, 10)}
print("     note 3 sd days a year for t_nu, own sd:", tab)
check("l10 s8 [informational] generic 'a fat-tailed model sits between' has counter-examples: t(2.01) expects fewer than the normal's 0.7",
      True, tab[2.01])
# Markov failing for a negative variable: X = -3 or 5 with chance 1/2, E = 1
check("l10 trap: Markov can fail with negatives (X = -3 or 5, E = 1, P(X >= 5) = 0.5 > 1/5)", 0.5 > 1 / 5)

# l11: aggregation thins tails for finite-variance days; clustering slows it; infinite variance can block it
rng = np.random.default_rng(3)
x = rng.standard_t(5, size=(200000, 20))
ek = stats.kurtosis
check("l11 iid t5: 20-day sums have lower excess kurtosis than daily", ek(x.sum(axis=1)) < 0.5 * ek(x[:, 0]), (ek(x[:, 0]), ek(x.sum(axis=1))))
def garch(nd, rng, a=0.07, b=0.90, w=0.03, nu=8):
    # GARCH(1,1) with unit-variance Student t(8) shocks: fat-tailed, clustered days with a finite fourth moment
    # (daily kurtosis 4.5*(1-0.97^2)/(1-0.97^2-3.5*0.07^2) = 6.3; Bollerslev 1986, He and Terasvirta 1999)
    zz = rng.standard_t(nu, size=nd) * math.sqrt((nu - 2) / nu); r = np.empty(nd); h = w / (1 - a - b)
    for t in range(nd):
        r[t] = math.sqrt(h) * zz[t]; h = w + a * r[t] ** 2 + b * h
    return r
def tail(v):  # 99.9% point of |v| in sds; 3.29 for a normal
    return np.quantile(np.abs(v), 0.999) / v.std()
g = garch(3_000_000, rng); gm = g.reshape(-1, 20).sum(axis=1)
perm = rng.permutation(g).reshape(-1, 20).sum(axis=1)
check("l11 clustered fat-tailed days: 20-day excess kurtosis below daily, above that of shuffled (independent) days",
      ek(perm) + 0.3 < ek(gm) < ek(g) - 0.3, (ek(g), ek(gm), ek(perm)))
check("l11 same, by the 99.9% point in sds (normal 3.29): daily > 20-day > shuffled 20-day",
      tail(g) > tail(gm) + 0.1 and tail(gm) > tail(perm) + 0.1, (tail(g), tail(gm), tail(perm)))
c = rng.standard_cauchy(size=(200000, 20))
q = lambda v: np.quantile(np.abs(v), 0.99) / np.quantile(np.abs(v), 0.75)
check("l11 infinite variance (Cauchy): a 20-day average has the same tail shape as one day", abs(q(c.mean(axis=1)) / q(c[:, 0]) - 1) < 0.1)

# problems-3 p-maker-days
check("p3 sd 180, z = -2, Phi(-2) = 0.0228", math.sqrt(900 * 36) == 180 and abs(stats.norm.cdf(-2) - 0.0228) < 5e-5)
check("p3 'one day in 44': 1/0.0228 = 43.9", round(1 / 0.0228) == 44 and round(1 / stats.norm.cdf(-2)) == 44, 1 / 0.0228)
npq = 250 * 0.0228 * 0.9772
check("p3 np(1-p) = 5.57 < 10", abs(npq - 5.57) < 0.005, npq)
ex = stats.binom.sf(9, 250, 0.0228); po = stats.poisson.sf(9, 5.7); nm = stats.norm.sf((9.5 - 5.7) / math.sqrt(npq))
check("p3 exact 0.0626, Poisson 0.0648, normal near 0.0537 (too low)",
      abs(ex - 0.0626) < 5e-5 and abs(po - 0.0648) < 5e-5 and abs(nm - 0.0537) < 5e-4 and nm < ex, (ex, po, nm))
check("p3 bell fits poorly: skew of Bin(250, 0.0228) about 0.40", abs((1 - 2 * 0.0228) / math.sqrt(npq) - 0.40) < 0.01)

# voice gate on the changed strings
NEW = {
 "l1-counting-successes.json": ["covariances can be non-zero"],
 "l10-bound-that-holds.json": ["A bound of 5 says nothing", "seldom strays", "Student", "Markov can fail"],
 "l11-sums-look-normal.json": ["In real returns, summing pulls", "In real returns, summing 20"],
 "l3-rare-events.json": ["More than one module"], "l7-bell-curve.json": ["nearly 14"], "l8-lognormal.json": ["75 is the average size"],
 "l9-averages-settle.json": ["partly cancel", "tail this fat", "enough to hide"],
 "problems-3.json": ["one day in 44", "The theorem is a limit"], "review-2.json": ["You divided by $x$"]}
def walk(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, path + "." + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "[%d]" % i, out)
    elif isinstance(o, str): out.append((path, o))
for f, needles in NEW.items():
    strs = []; walk(load(f), "", strs)
    for nd in needles:
        hits = [(p, s) for p, s in strs if nd in s]
        check("found once: %s %s" % (f, nd), len(hits) == 1)
        for p, s in hits:
            plain = re.sub(r"\$[^$]*\$", "X", s)
            sents = [t for t in re.split(r"(?<=[.?])\s+", plain) if t.strip()]
            longest = max(len(t.split()) for t in sents)
            bad = "!" in s or "—" in s or re.search(r"\b[Ll]esson \d|\bl\d+\b", plain)
            lim = 3 if (p.endswith("explain.text") or ".byKey." in p or p.endswith(".why")) else 99
            check("voice %s%s" % (f, p), not bad and longest <= 35 and len(sents) <= lim, "%d sentences, longest %d words" % (len(sents), longest))

print("\n%d failed" % len(fails))
sys.exit(1 if fails else 0)
