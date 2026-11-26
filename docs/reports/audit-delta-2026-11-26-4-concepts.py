"""Delta audit 2026-11-26 batch 4: recompute every changed key and slip
(conditional, limits-thm, markov, random-vars problem sets) and Monte Carlo
the two new conditional problems. Exits 0 when content is correct.
The content defects found (feedback wording) are prose, not numbers; they are
recorded in docs/reviews/audit-delta-2026-11-26-4.md, not asserted here."""
import json, math, os, sys
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "app", "content", "courses") + os.sep
fails = []


def chk(name, got, want, tol=6e-4):
    ok = abs(got - want) <= tol
    print(("ok   " if ok else "FAIL ") + f"{name}: {got:.6g} vs {want}")
    if not ok:
        fails.append(name)


def prob(f, pid):
    d = json.load(open(R + f))

    def walk(o):
        if isinstance(o, dict):
            if o.get("id") == pid and "parts" in o:
                return o
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r:
                    return r
    return walk(d)


def key(p, i):
    return p["parts"][i]["widget"]["answer"]


def slip(p, i, s):
    return next(w["value"] for w in p["parts"][i]["widget"]["wrong"] if w["id"] == s)


rng = np.random.default_rng(4)

# conditional problems-3 p-two-papers
p = prob("conditional/problems-3.json", "p-two-papers")
g = 0.2 * 0.85
c = (0.11 - 0.4 * g) / 0.6
chk("papers p1", g, key(p, 0))
chk("p1 indep", 0.2 * 0.55, slip(p, 0, "indep"))
chk("p1 over-y", 0.85 * 0.55, slip(p, 0, "over-y"))
chk("papers p2", c, key(p, 1))
chk("p2 unweighted", 0.11 - 0.4 * g, slip(p, 1, "unweighted"))
chk("p2 equal", (0.11 - 0.5 * g) / 0.5, slip(p, 1, "equal"))
chk("papers p3", c / 0.2, key(p, 2))
chk("p3 over-y", c / 0.55, slip(p, 2, "over-y"))
chk("p3 unweighted", 0.042 / 0.2, slip(p, 2, "unweighted"))
chk("shifts offset", 0.4 * (0.85 - 0.55) + 0.6 * (0.35 - 0.55), 0, 1e-12)
assert 0 <= c <= 0.2 and g <= 0.2  # both joint tables are feasible
n = 4_000_000
grad = rng.random(n) < 0.4
m = rng.random(n) < 0.2
pc = np.where(m, np.where(grad, 0.85, 0.35),
              np.where(grad, (0.55 - 0.17) / 0.8, (0.55 - 0.07) / 0.8))
cod = rng.random(n) < pc
chk("MC pooled P(C|M)", cod[m].mean(), 0.55, 0.003)
chk("MC pooled P(C)", cod.mean(), 0.55, 0.002)
chk("MC P(C) graduates", cod[grad].mean(), 0.55, 0.002)
chk("MC career both", (m & cod)[~grad].mean(), 0.07, 0.001)

# conditional problems-4 p-dark-fills
p = prob("conditional/problems-4.json", "p-dark-fills")
y = 1 - 0.8 ** 3
chk("fills p1", 1.2 / 1.8, key(p, 0))
chk("p1 small", 0.6 / 1.8, slip(p, 0, "small"))
chk("fills p2", 2 / 3, key(p, 1))
chk("p2 joint", 2 / 3 * 0.2, slip(p, 1, "joint"))
chk("p2 double", 2 * y / 0.2 / (1 + 2 * y / 0.2), slip(p, 1, "double"))
chk("fills p3", y, key(p, 2), 1e-9)
chk("p3 exactly-one", 3 * 0.2 * 0.64, slip(p, 2, "exactly-one"), 1e-9)
chk("p3 all", 0.2 ** 3, slip(p, 2, "all"), 1e-9)
chk("fills p4", 0.4 * y / (0.4 * y + 0.12), key(p, 3))
chk("p4 sum-slip", 0.24 / 0.36, slip(p, 3, "sum-slip"))
chk("p4 no-prior", y / (y + 0.2), slip(p, 3, "no-prior"))
chk("p4 path", 0.4 * y, slip(p, 3, "path"))
chk("LR of a yes", y / 0.2, 2.44, 1e-9)
n = 2_000_000
large = rng.random(n) < 0.4
k = np.where(large, 3, 1)
dark = rng.binomial(k, 0.2)
chk("MC fill from large", (k * large).sum() / k.sum(), 2 / 3, 0.002)
chk("MC dark fill from large", (dark * large).sum() / dark.sum(), 2 / 3, 0.003)
chk("MC large | yes", large[dark > 0].mean(), 0.6193, 0.003)

# conditional problems-2 (skipped-a) and problems-5 (round mean)
o = 0.02 / 0.98 * 70
chk("skipped-a", o / (1 + o), 0.5882)
chk("P(error | A flags)", 0.019 / 0.0582, 0.3265)
chk("doubling round mean", 31 / 32 * 1 - 1 / 32 * 31, 0, 1e-12)

# limits-thm problems-2
chk("Phi(0.15)", norm.cdf(0.15), 0.5596, 6e-5)
chk("Phi(0.2) no-centre", norm.cdf(0.06 / 0.3), 0.5793, 6e-5)
z = rng.standard_normal(2_000_000)
chk("MC median S1", float(np.median(80 * np.exp(0.015 + 0.3 * z))), 80 * math.exp(0.015), 0.05)

# markov problems-1 and problems-3
chk("stress spell", 1 / 0.3, 3.3333)
chk("used-stay", 1 / 0.7, 1.4286)
chk("next month after stress", 0.3 * 3 + 0.7 * -8, -4.7, 1e-9)
print("note : dropping the minus on the stressed loss gives", 0.3 * 3 + 0.7 * 8, "not 4.7 (finding 1)")
chk("C(12,4)", math.comb(12, 4), 495, 0)
r = 13 / 12
p3 = (1 - r ** 3) / (1 - r ** 5)
chk("one trade", 100 * (2 * 0.48 - 1), -4, 1e-9)
chk("profit", 1000 * p3 - 600, -48.51, 0.005)
chk("wealth", 1000 * p3, 551.49, 0.005)
chk("pairs trade", 100 * (5 / 8 * 3 - 3 / 8 * 5) - 40 * 15, -600, 0)

# random-vars problems-2, -3, -5
chk("rv p2", 57 - 8 * 9.12, -15.96, 1e-9)
A = np.array([-1, -1, 2, 2])
B = np.array([-2, 2, -2, 2])
P = np.array([0.3, 0.1, 0.1, 0.5])
va = P @ A ** 2 - (P @ A) ** 2
vb = P @ B ** 2 - (P @ B) ** 2
cv = P @ (A * B) - (P @ A) * (P @ B)
h = cv / vb
hv = va + h * h * vb - 2 * h * cv
chk("VarA", va, 2.16, 1e-9)
chk("Cov", cv, 1.68, 1e-9)
chk("hedged", hv, 1.425, 1e-9)
chk("decimal VarA", va / 1e4, 0.000216, 1e-9)
chk("decimal Cov", cv / 1e4, 0.000168, 1e-9)
chk("decimal hedged", hv / 1e4, 0.0001425, 1e-9)
e = 0.5 * (math.log(1.5) + math.log(0.6))
chk("E ln R", e, -0.0527, 5e-5)
chk("E ln W (carried -0.0527, widget tol 0.0005)", 4 * e, -0.2108, 5e-4)
print("note : 0.5108 - 0.4055 =", round(0.5108 - 0.4055, 4), "is twice the slip 0.0527 (finding 3)")

sys.exit(1 if fails else 0)
