#!/usr/bin/env python3
"""Fix-pass read of limits-thm level 4 (commit 309e891c).

Recomputes every number, shown product and event stated in the strings the fixer
changed, and checks voice gates on those strings. Exits 0 on correct content.
A check that fails because the content is wrong stays failing.
Run from anywhere: python3 docs/reports/limits-thm-L4-fixread.py
"""
import itertools
import json
import math
import os
import re
import sys

import numpy as np
import sympy as sp
from scipy import stats

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                    "app", "content", "courses", "limits-thm")
FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(f"{name} {detail}")
        print(f"FAIL {name} {detail}")


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return json.load(fh)


def strings(node, path=""):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from strings(v, f"{path}.{k}" if path else k)


def find(doc, fragment):
    return [(p, s) for p, s in strings(doc) if fragment in s]


def words(sentence):
    return len([w for w in re.split(r"\s+", sentence.strip()) if w])


def sentences(text):
    # split on full stops followed by a space and a capital or $; keeps maths intact enough
    flat = re.sub(r"\$\$.*?\$\$", " MATH. ", text, flags=re.S)
    flat = re.sub(r"\$[^$]*\$", "MATH", flat)
    return [s for s in re.split(r"(?<=[.?:])\s+(?=[A-Z\"])", flat) if s.strip()]


def voice(name, text, explain=False):
    check(f"voice no exclamation: {name}", "!" not in re.sub(r"\\!", "", text))
    check(f"voice no em-dash: {name}", "—" not in text and "–" not in text)
    for s in sentences(text):
        check(f"voice sentence <= 35 words: {name}", words(s) <= 35, f"({words(s)}) {s[:60]}")
    if explain:
        n = len([s for s in re.split(r"(?<=[.?])\s+(?=[A-Z$\"])", re.sub(r"\$[^$]*\$", "M", text)) if s.strip()])
        check(f"voice explain <= 3 sentences: {name}", n <= 3, f"({n})")
    check(f"voice no lesson number: {name}", not re.search(r"\b[Ll]esson \d|\bl1[4-9]\b", text))
    for us in ("color", "center", "favor", "standardized", "normalized", "factorize"):
        check(f"voice British: {name}", us not in text.lower(), us)


def expect(doc, fragment, name, explain=False, count=1):
    hits = find(doc, fragment)
    check(f"present: {name}", len(hits) >= count, f"found {len(hits)}")
    for p, s in hits:
        voice(f"{name} @ {p}", s, explain=explain and p.endswith("explain.text"))
    return hits


rng = np.random.default_rng(20261112)
Phi = stats.norm.cdf

# ---------------------------------------------------------------- homework-4
hw = load("homework-4.json")
expect(hw, "so the mean usually lands within 0.003 of $\\tfrac13$", "hw order-stat explain", explain=True)
sd_23 = math.sqrt(stats.beta(2, 4).var())            # 2nd smallest of 5 uniforms is Beta(2, 4)
check("hw sd of X(2) of 5 is 0.18", round(sd_23, 2) == 0.18, f"{sd_23:.4f}")
se = 0.18 / math.sqrt(20000)
check("hw 0.18/sqrt(20000) ~ 0.0013", round(se, 4) == 0.0013, f"{se:.5f}")
reps = 400
means = np.sort(rng.random((reps, 20000, 5)), axis=2)[:, :, 1].mean(axis=1)
share = float(np.mean(np.abs(means - 1 / 3) < 0.003))
check("hw mean usually within 0.003 of 1/3", share > 0.95, f"share {share:.3f}")
check("hw mean always within test tol 0.01", float(np.max(np.abs(means - 1 / 3))) < 0.01)
for n_, k_ in ((5, 2), (9, 3), (1, 1), (10, 10)):      # hidden tests: k/(n+1) within 0.01
    sd = math.sqrt(stats.beta(k_, n_ - k_ + 1).var()) / math.sqrt(20000)
    check(f"hw test tol 0.01 is > 4 sd for n={n_},k={k_}", 0.01 > 4 * sd, f"{sd:.5f}")

# ---------------------------------------------------------------- l14
l14 = load("l14-joint-densities.json")
expect(l14, "\\tfrac{\\lambda_A}{\\lambda_A + \\lambda_B} = \\tfrac{1}{1+2}", "l14 race rule", explain=True)
expect(l14, "For other pairs it can fail, as $Y = X^2$ shows.", "l14 uncorrelated explain", explain=True)
expect(l14, "Zero covariance does not prove independence either, though for jointly normal pairs it does.", "l14 trap")
x, y, lam, mu_ = sp.symbols("x y lambda mu", positive=True)
pA = sp.integrate(sp.integrate(2 * sp.exp(-x - 2 * y), (y, x, sp.oo)), (x, 0, sp.oo))
check("l14 P(A first) = 1/3 from density 2e^{-x-2y}", pA == sp.Rational(1, 3), str(pA))
gen = sp.simplify(sp.integrate(sp.integrate(lam * sp.exp(-lam * x) * mu_ * sp.exp(-mu_ * y), (y, x, sp.oo)), (x, 0, sp.oo)))
check("l14 race rule lambda_A/(lambda_A+lambda_B)", sp.simplify(gen - lam / (lam + mu_)) == 0, str(gen))
check("l14 A is the rate-1 clock (marginal of x)", sp.integrate(2 * sp.exp(-x - 2 * y), (y, 0, sp.oo)) == sp.exp(-x))
# the A-first polygon lies above the diagonal y > x
poly = [s for s in l14["screens"] if s.get("question") == "What is the chance that A defaults first?"][0]
pts = poly["canvas"]["state"]["polygons"][0]["points"]
check("l14 polygon is y >= x", all(p[1] >= p[0] for p in pts))
check("l14 key 1/3", abs(poly["widget"]["answer"] - 1 / 3) < 1e-9)
# Y = X^2 with X uniform on [-1, 1]: covariance 0, dependent
u = sp.symbols("u")
cov = sp.integrate(u**3 / 2, (u, -1, 1)) - sp.integrate(u / 2, (u, -1, 1)) * sp.integrate(u**2 / 2, (u, -1, 1))
check("l14 Cov(X, X^2) = 0", cov == 0)
# a non-normal pair that is uncorrelated AND independent exists, so 'can fail' (not 'fails') is right
check("l14 exponential pair factors (independent, not jointly normal)",
      sp.simplify(2 * sp.exp(-x - 2 * y) - sp.exp(-x) * 2 * sp.exp(-2 * y)) == 0)

# ---------------------------------------------------------------- l15
l15 = load("l15-new-variables.json")
expect(l15, "The bars average about 0.5.", "l15 bars question")
cov_hits = expect(l15, "strictly increasing or strictly decreasing and $x = g^{-1}(y)$ differentiable", "l15 change of variables prose")
expect(l15, "You divided by the 2 from the exponent where you should multiply.", "l15 inv why")
expect(l15, "The 2 from the exponent multiplies:", "l15 inv feedback")
expect(l15, "A strictly increasing or strictly decreasing $g$ with $g' \\ne 0$ keeps a density.", "l15 atom explain", explain=True)
expect(l15, "$100 \\times 0.09516 = 9.516$ defaults on average.", "l15 defaults feedback")
expect(l15, "For strictly monotone $g$ with a differentiable inverse it gives", "l15 summary")
sims = -np.log(rng.random(400000)) / 2
check("l15 mean of -ln(U)/2 is 0.5", abs(sims.mean() - 0.5) < 0.005, f"{sims.mean():.4f}")
check("l15 |dx/dy| of e^{-2y} is 2e^{-2y}", sp.simplify(sp.Abs(sp.diff(sp.exp(-2 * y), y)) - 2 * sp.exp(-2 * y)) == 0)
check("l15 wrong option is the right one divided by 4 (2 -> 1/2)", sp.Rational(1, 2) == sp.Rational(1) / 2)
p5 = 1 - math.exp(-0.1)
check("l15 1 - e^{-0.1} = 0.09516", round(p5, 5) == 0.09516, f"{p5:.6f}")
check("l15 100 x 0.09516 = 9.516", round(100 * 0.09516, 3) == 9.516)
# density of -ln(U)/2 against 2e^{-2y}
ks = stats.kstest(sims[:50000], stats.expon(scale=0.5).cdf).pvalue
check("l15 Y = -ln(U)/2 is Exp(2)", ks > 0.001, f"p {ks:.4f}")
check("l15 P(S <= 105) = 0.6915", round(Phi(0.5), 4) == 0.6915)
# The CDF identity quoted in the prose. For the screen's own map (decreasing) F_Y(y) = 1 - F_U(x).
yy = 0.3
F_Y = 1 - math.exp(-2 * yy)
F_U_at_x = math.exp(-2 * yy)
decreasing_identity_holds = abs(F_Y - F_U_at_x) < 1e-9
prose = cov_hits[0][1] if cov_hits else ""
states_plain_identity = "F_Y(y) = F_X(x)" in prose and "1 - F_X" not in prose and "strictly decreasing" in prose
check("l15 prose: F_Y(y) = F_X(x) is offered for decreasing g as well, where F_Y(y) = 1 - F_X(x)",
      decreasing_identity_holds or not states_plain_identity,
      f"F_Y({yy}) = {F_Y:.4f} but F_U(e^(-2y)) = {F_U_at_x:.4f}")

# ---------------------------------------------------------------- l16
l16 = load("l16-adding-densities.json")
expect(l16, "Flip $Y$'s density and slide it so that it covers $[t - 1, t]$.", "l16 slide prose")
expect(l16, "That is the joint density of both fills at 0.5, a pair that adds to 1, not 0.5.", "l16 prod why")
expect(l16, "Not quite right. Count every split of 0.5 into $x$ and $0.5 - x$.", "l16 generic")
expect(l16, "The density at 0.5 adds up every split $x$ and $0.5 - x$.", "l16 prod feedback")
expect(l16, "Two independent strategies have daily P&L", "l16 normals prose")
expect(l16, "Desk B only loses, independently of desk A.", "l16 desks prose")
slide = [s for s in l16["screens"] if s.get("title") == "Slide one density over the other"][0]
fy = [f for f in slide["canvas"]["params"]["functions"] if f["id"] == "fy"][0]
check("l16 canvas flipped copy sits on [t-1, t]", fy["domain"] == ["t - 1", "t"], str(fy["domain"]))
# f_Y(t - x) with Y ~ U(0, 1) is 1 exactly for x in [t-1, t]
for t_ in (0.3, 0.5, 1.4):
    xs = np.linspace(-1.5, 2.5, 4001)
    on = ((t_ - xs) >= 0) & ((t_ - xs) <= 1)
    check(f"l16 support of f_Y(t-x) at t={t_}", abs(xs[on].min() - (t_ - 1)) < 2e-3 and abs(xs[on].max() - t_) < 2e-3)
tot = rng.random(400000) + rng.random(400000)
dens = np.mean(np.abs(tot - 0.5) < 0.01) / 0.02
check("l16 density of U1+U2 at 0.5 is 0.5", abs(dens - 0.5) < 0.03, f"{dens:.3f}")
check("l16 pair (0.5, 0.5) adds to 1 and has joint density 1", 0.5 + 0.5 == 1.0)
check("l16 sum N(2,9)+N(1,16) is N(3,25) only if independent", slide is not None and math.isclose(math.sqrt(9 + 16), 5))

# ---------------------------------------------------------------- l17
l17 = load("l17-smallest-and-largest.json")
expect(l17, "$1 - (e^{-0.2})^5 = 1 - e^{-1} = 0.6321$.", "l17 first-default accept")
expect(l17, "None default within 10 years with chance $(e^{-0.2})^5 = e^{-1}$.", "l17 first-default hint")
expect(l17, "0.9063 is $5 \\times 0.181269$.", "l17 five feedback")
expect(l17, "For independent continuous draws a tie has probability 0, so the maximum comes from one draw alone.", "l17 ties prose")
expect(l17, "That includes a maximum of 1 or 2 as well.", "l17 dice cdf feedback")
expect(l17, "1 - 0.982136^{20} \\approx 0.3027", "l17 best20 accept")
expect(l17, "$\\Phi(2.1) = 0.982136$", "l17 best20 hint")
expect(l17, "$1 - 0.982136^{20}$.", "l17 best20 step")
expect(l17, "$1 - 0.982136^{20} = 0.3027$.", "l17 best20 correct")
expect(l17, "0.3573 is $20 \\times 0.017864$.", "l17 times feedback")
expect(l17, "For $n$ independent draws with CDF $F$:", "l17 summary idea")
expect(l17, "For independent continuous draws ties have chance 0.", "l17 summary note")
check("l17 (e^-0.2)^5 = e^-1", math.isclose(math.exp(-0.2) ** 5, math.exp(-1)))
check("l17 1 - e^-1 = 0.6321", round(1 - math.exp(-1), 4) == 0.6321)
check("l17 1 - e^-0.2 = 0.181269", round(1 - math.exp(-0.2), 6) == 0.181269)
check("l17 5 x 0.181269 = 0.9063", round(5 * 0.181269, 4) == 0.9063, f"{5 * 0.181269}")
check("l17 Phi(2.1) = 0.982136", round(Phi(2.1), 6) == 0.982136, f"{Phi(2.1):.7f}")
check("l17 1 - 0.982136^20 = 0.3027", round(1 - 0.982136 ** 20, 4) == 0.3027, f"{1 - 0.982136 ** 20:.5f}")
check("l17 20 x 0.017864 = 0.3573", round(20 * 0.017864, 4) == 0.3573, f"{20 * 0.017864}")
check("l17 1 - 0.982136 = 0.017864", round(1 - 0.982136, 6) == 0.017864)
keys = {}
for s in l17["screens"]:
    w = s.get("widget", {})
    if w.get("kind") == "numeric":
        keys[s.get("question", "")] = w
k1 = [w for q, w in keys.items() if "at least one of the five" in q][0]
k2 = [w for q, w in keys.items() if "best of the 20" in q][0]
check("l17 first-default key 0.6321 within tol", abs(k1["answer"] - (1 - math.exp(-1))) < k1["tol"]["abs"])
check("l17 best20 key 0.3027 within tol", abs(k2["answer"] - (1 - Phi(2.1) ** 20)) < k2["tol"]["abs"])
for w in (k1, k2):
    for wr in w["wrong"]:
        check("l17 slip does not overlap key", abs(wr["value"] - w["answer"]) > wr["tol"]["abs"] + w["tol"]["abs"])
dice = list(itertools.product(range(1, 7), repeat=2))
check("l17 P(max <= 3) = 1/4 = (1/2)^2", sum(max(d) <= 3 for d in dice) / 36 == 0.25)
check("l17 max <= 3 is max in {1,2,3}", {max(d) for d in dice if max(d) <= 3} == {1, 2, 3})
check("l17 P(max = 3) = 5/36", sum(max(d) == 3 for d in dice) == 5)
# F(t)^n needs independence: comonotone draws break it
check("l17 F^n fails without independence (same draw repeated)", abs(0.5 - 0.5 ** 3) > 0.1)
draws = rng.random((200000, 5))
check("l17 continuous iid draws: no ties in simulation", bool(np.all(np.diff(np.sort(draws, axis=1), axis=1) > 0)))
mx = rng.standard_normal((200000, 20)).max(axis=1)
check("l17 sim P(best of 20 >= 2.1) ~ 0.3027", abs(np.mean(mx >= 2.1) - 0.3027) < 0.005, f"{np.mean(mx >= 2.1):.4f}")

# ---------------------------------------------------------------- l18
l18 = load("l18-gamma-beta.json")
expect(l18, "Trades arrive as a Poisson process at 2 a minute, so each gap is exponential with mean half a minute.", "l18 Poisson prose")
expect(l18, "Six independent standard normal returns are squared and added.", "l18 chi-square question")
expect(l18, "With $V$ chi-square on $n$ degrees of freedom and independent of $Z$,", "l18 t prose")
expect(l18, "the share of time a long fair random walk spends positive.", "l18 arcsine explain", explain=True)
expect(l18, "A sum of $n$ independent squared standard normals is chi-square (Gamma with $a = \\tfrac n2$, $\\lambda = \\tfrac12$).", "l18 summary chi-square")
expect(l18, "With $Z$ independent of $V$, $\\tfrac{Z}{\\sqrt{V/n}}$ has the $t$ distribution", "l18 summary t")
gaps = rng.exponential(0.5, (200000, 3)).sum(axis=1)
check("l18 third arrival is Gamma(3, rate 2)", stats.kstest(gaps[:50000], stats.gamma(3, scale=0.5).cdf).pvalue > 0.001)
z = rng.standard_normal((300000, 6))
v = (z ** 2).sum(axis=1)
check("l18 Var of sum of 6 squared normals = 12", abs(v.var() - 12) < 0.3, f"{v.var():.3f}")
check("l18 chi-square(6) = Gamma(3, rate 1/2)", abs(stats.chi2(6).var() - stats.gamma(3, scale=2).var()) < 1e-9)
# dependent standard normals: sum of squares is not chi-square(6) (variance 72, not 12)
zz = rng.standard_normal(300000)
check("l18 independence needed for chi-square", abs((6 * zz ** 2).var() - 12) > 20)
# t needs Z independent of V
zz = rng.standard_normal((400000, 6))
V5 = (zz[:, :5] ** 2).sum(axis=1)
t_ind = zz[:, 5] / np.sqrt(V5 / 5)
t_dep = zz[:, 0] / np.sqrt(V5 / 5)                  # Z is one of the terms of V
p_true = 2 * stats.t(5).sf(2)
check("l18 independent Z, V gives t(5) tails", abs(np.mean(np.abs(t_ind) > 2) - p_true) < 0.003)
check("l18 dependent Z, V does not give t(5) tails", abs(np.mean(np.abs(t_dep) > 2) - p_true) > 0.01,
      f"{np.mean(np.abs(t_dep) > 2):.4f} vs {p_true:.4f}")
check("l18 normal two-sided tail beyond 2 = 0.0455", round(2 * stats.norm.sf(2), 4) == 0.0455)
check("l18 arcsine CDF at 0.25 = 1/3", math.isclose(2 / math.pi * math.asin(0.5), 1 / 3))
steps = rng.choice([-1, 1], size=(20000, 1000))
share_pos = (np.cumsum(steps, axis=1) > 0).mean(axis=1)
f_low = np.mean(share_pos < 0.25)
check("l18 long walk: share of time positive below 0.25 about 1/3", abs(f_low - 1 / 3) < 0.03, f"{f_low:.3f}")
short = (np.cumsum(steps[:, :4], axis=1) > 0).mean(axis=1)
check("l18 short walk is not arcsine (so 'long' matters)", abs(np.mean(short < 0.25) - 1 / 3) > 0.03)

# ---------------------------------------------------------------- l19
l19 = load("l19-generating-functions.json")
expect(l19, "Independence is enough for the product rule. Without it $E[e^{tX}e^{tY}]$ can fail to split, so check independence first.", "l19 product explain", explain=True)
expect(l19, "Let $X_i$ be independent and identically distributed with mean $\\mu$ and sd $\\sigma$", "l19 CLT prose")
expect(l19, "Chernoff bounds a tail by $\\min_{t > 0} e^{-ta}M(t)^n$.", "l19 summary Chernoff")
expect(l19, "P(S \\ge a) \\le \\min_{t > 0} e^{-ta}M(t)^n", "l19 formula")
t = sp.symbols("t", real=True)
M = sp.Rational(1, 2) + sp.exp(t) / 2
check("l19 product expands to 0.25 + 0.5e^t + 0.25e^{2t}",
      sp.simplify(sp.expand(M ** 2) - (sp.Rational(1, 4) + sp.exp(t) / 2 + sp.exp(2 * t) / 4)) == 0)
check("l19 dependent case fails: Y = X gives M(2t) != M(t)^2", sp.simplify(M.subs(t, 2 * t) - M ** 2) != 0)
# independence sufficient, not necessary: X = Y = Cauchy has phi_{X+Y} = phi_X phi_Y; for MGFs a
# finite example of dependent X, Y whose MGF of the sum is the product
best = None
vals = [-1, 0, 1]
base = np.full((3, 3), 1 / 9)
eps = 1 / 18
pert = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]]) * eps   # rows, columns and anti-diagonals sum to 0
joint = base + pert
sum_pmf = {}
ind_pmf = {}
for i, a in enumerate(vals):
    for j, b in enumerate(vals):
        sum_pmf[a + b] = sum_pmf.get(a + b, 0) + joint[i, j]
        ind_pmf[a + b] = ind_pmf.get(a + b, 0) + 1 / 9
check("l19 dependent pair with product MGF exists (independence not necessary)",
      all(abs(sum_pmf[k] - ind_pmf[k]) < 1e-12 for k in sum_pmf) and abs(joint[0, 1] - 1 / 9) > 1e-3
      and np.allclose(joint.sum(axis=0), 1 / 3) and np.allclose(joint.sum(axis=1), 1 / 3) and joint.min() > 0)
# Chernoff: 100 fair +-1 trades, S >= a. t > 0 is needed; a negative t does not bound the upper tail.
n_, a_ = 100, 20
exact = sum(math.comb(100, k) for k in range(60, 101)) / 2 ** 100       # S = 2k - 100 >= 20
ts = np.linspace(0.001, 2, 4000)
bound = float(np.min(np.exp(-ts * a_) * np.cosh(ts) ** n_))
check("l19 Chernoff bound with t > 0 is above the exact tail", bound >= exact, f"{bound:.4f} vs {exact:.4f}")
exact_low = sum(math.comb(100, k) for k in range(40, 101)) / 2 ** 100    # P(S >= -20), large
neg = float(np.exp(1.0 * -20) * np.cosh(-1.0) ** n_)                     # 'bound' at a = -20 is fine for t>0 only
unrestricted = float(np.min(np.exp(-np.linspace(-2, 2, 8001) * (-20)) * np.cosh(np.linspace(-2, 2, 8001)) ** n_))
check("l19 unrestricted min over t fails as an upper-tail bound (a = -20)", unrestricted < exact_low,
      f"{unrestricted:.4f} vs {exact_low:.4f}")

# ---------------------------------------------------------------- problems-4
pr = load("problems-4.json")
expect(pr, "$X_{(3)} > 0.5$ exactly when at least 2 of the 4 quotes are above 0.5.", "p-dealer-quotes explain", explain=True)
expect(pr, "You divided the exponent by 4. Multiplying four copies multiplies the exponent by 4: $-\\tfrac12 \\times 4 = -2$.", "p-part-errors power")
# enumeration with a threshold other than 0.5: X(3) > c  <=>  at least 2 of 4 above c
for c in (0.3, 0.5, 0.8):
    p_enum = 0.0
    ok_event = True
    for pattern in itertools.product([0, 1], repeat=4):       # 1 = above c
        pr_pat = math.prod((1 - c) if b else c for b in pattern)
        # representative values: below -> distinct values under c, above -> over c
        vals4 = sorted((c + 0.01 * (i + 1)) if b else (c - 0.01 * (i + 1)) for i, b in enumerate(pattern))
        third_above = vals4[2] > c
        ok_event &= (third_above == (sum(pattern) >= 2))
        ok_event &= (third_above != (sum(pattern) <= 1))
        p_enum += pr_pat * third_above
    check(f"p-dealer X(3) > c iff at least 2 above (c={c})", ok_event)
    check(f"p-dealer enumeration matches Beta(3,2) tail (c={c})", abs(p_enum - stats.beta(3, 2).sf(c)) < 1e-12)
check("p-dealer fails with 0 or 1 above: (1+4)/16", (math.comb(4, 0) + math.comb(4, 1)) / 16 == 5 / 16)
xs = sp.symbols("xs")
check("p-dealer Beta(3,2) integral = 11/16", sp.integrate(12 * xs**2 * (1 - xs), (xs, sp.Rational(1, 2), 1)) == sp.Rational(11, 16))
check("p-dealer Beta(3,2) density is 12x^2(1-x)", math.isclose(1 / sp.beta(3, 2), 12))
q = rng.random((400000, 4))
check("p-dealer sim 0.6875", abs(np.mean(np.sort(q, axis=1)[:, 2] > 0.5) - 0.6875) < 0.003)
dealer = [p for p in pr["problems"] if p["id"] == "p-dealer-quotes"][0] if "problems" in pr else None
if dealer is None:
    dealer = [p for _, p in [(0, x_) for x_ in pr.get("items", [])] if p.get("id") == "p-dealer-quotes"][0]
check("p-dealer prose states uniform and independent", "uniform" in dealer["prose"] and "independently" in dealer["prose"])
last = dealer["parts"][-1]["widget"]
check("p-dealer key 0.6875", abs(last["answer"] - 11 / 16) < 1e-12)
check("p-part-errors: -1/2 / 4 = -1/8 is the wrong option", sp.Rational(-1, 2) / 4 == sp.Rational(-1, 8))
check("p-part-errors: -1/2 x 4 = -2", sp.Rational(-1, 2) * 4 == -2)

# ---------------------------------------------------------------- review-4
rv = load("review-4.json")
expect(rv, "1 - 0.97725^{10} \\approx 0.2056", "r-best10 accept")
expect(rv, "$1 - 0.97725^{10} = 0.2056$.", "r-best10 correct")
expect(rv, "0.2275 is $10 \\times 0.02275$.", "r-best10 times")
hits = expect(rv, "That is not the chance that a reported best of 2 is luck, which also depends on how common skill is.", "r-best10 explain", explain=True)
check("r-best10 Phi(2) = 0.97725", round(Phi(2), 5) == 0.97725, f"{Phi(2):.6f}")
check("r-best10 0.97725^10 = 0.7944", round(0.97725 ** 10, 4) == 0.7944, f"{0.97725 ** 10:.5f}")
check("r-best10 1 - 0.97725^10 = 0.2056", round(1 - 0.97725 ** 10, 4) == 0.2056)
check("r-best10 10 x 0.02275 = 0.2275", round(10 * 0.02275, 4) == 0.2275)
check("r-best10 about one time in five", abs(1 - Phi(2) ** 10 - 0.2) < 0.01)
items = rv.get("items") or rv.get("questions") or rv.get("quiz") or []
b10 = [p for p, s in strings(rv) if s == "r-best10"]
check("r-best10 item found", len(b10) == 1)


def node_at(doc, path):
    cur = doc
    for tok in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        cur = cur[int(tok[1:-1])] if tok.startswith("[") else cur[tok]
    return cur


item = node_at(rv, b10[0].rsplit(".", 1)[0]) if b10 else {}
w = item.get("widget", {})
check("r-best10 key 0.2056 within tol of exact", abs(w.get("answer", 0) - (1 - Phi(2) ** 10)) < w.get("tol", {}).get("abs", 0))
check("r-best10 prose says independent and skill-free", "independent" in item.get("prose", "") and "skill-free" in item.get("prose", ""))
# P(best >= 2 | no skill) is not P(no skill | best >= 2): the second moves with the share of skilled searches
def p_luck(prior_skill, shift=1.0):
    p_null = 1 - Phi(2) ** 10
    p_alt = 1 - Phi(2 - shift) ** 10
    return (1 - prior_skill) * p_null / ((1 - prior_skill) * p_null + prior_skill * p_alt)
check("r-best10 P(luck | best >= 2) depends on how common skill is", abs(p_luck(0.1) - p_luck(0.9)) > 0.3,
      f"{p_luck(0.1):.3f} vs {p_luck(0.9):.3f}")
check("r-best10 explain does not read 0.2056 as P(luck | result)",
      all("pitches this good is luck" not in s for _, s in strings(rv)))
mx10 = rng.standard_normal((400000, 10)).max(axis=1)
check("r-best10 sim", abs(np.mean(mx10 >= 2) - 0.2056) < 0.003)

print(f"{N[0]} checks, {len(FAILS)} failed")
sys.exit(1 if FAILS else 0)
