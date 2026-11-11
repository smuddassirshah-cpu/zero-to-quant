#!/usr/bin/env python3
"""Fix-pass read, conditional levels 1 to 3, round 3 (diff of commit 7bbee00d).

Run from the repo root with no arguments. Exits 0 when the changed content is correct.
Every number is computed from the item's own givens, not copied from the content.
"""
import json
import random
import sys
from fractions import Fraction as F
from math import comb

ROOT = "app/content/courses/conditional/"
fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + detail if detail and not ok else ""))
    if not ok:
        fails.append(name)


def load(name):
    with open(ROOT + name, encoding="utf-8") as fh:
        return json.load(fh)


def tail(n, p, k):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def band(w):
    return (w["value"] - w["tol"]["abs"], w["value"] + w["tol"]["abs"])


def bands_disjoint(widget):
    key = (widget["answer"] - widget["tol"]["abs"], widget["answer"] + widget["tol"]["abs"])
    bs = [("key", key)] + [(w["id"], band(w)) for w in widget.get("wrong", [])]
    bad = []
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i][1], bs[j][1]
            if a[0] <= b[1] + 1e-12 and b[0] <= a[1] + 1e-12:
                bad.append((bs[i][0], bs[j][0]))
    return bad


# ---------------------------------------------------------------- l17 screens[5]
s = load("l17-correlated-defaults.json")["screens"][5]
P = s["canvas"]["params"]
lv0 = {b["id"]: float(b["p"]) for b in P["levels"][0]["branches"]}
lv1 = {b["id"]: {k: float(v) for k, v in b["p"].items()} for b in P["levels"][1]["branches"]}
leaves = {k: float(v) for k, v in P["leaves"].items()}

check("l17 first-level branches sum to 1", abs(sum(lv0.values()) - 1) < 1e-12)
for r in lv0:
    check(f"l17 second-level branches under {r} sum to 1", abs(sum(lv1[b][r] for b in lv1) - 1) < 1e-12)
check("l17 leaf set is every path", set(leaves) == {f"{r}-{b}" for r in lv0 for b in lv1})
for path, v in leaves.items():
    r, b = path.split("-")
    check(f"l17 leaf {path} is the product on its path", abs(v - lv0[r] * lv1[b][r]) < 1e-9, f"{v} vs {lv0[r] * lv1[b][r]}")
check("l17 leaves sum to 1", abs(sum(leaves.values()) - 1) < 1e-9)

# regime tails from the caption's own trials: 10 at 0.2, 10 at 0.0125
q, pb, pg, n = 0.2, 0.2, 0.0125, 10
check("l17 marginal default chance is 0.05", abs(q * pb + (1 - q) * pg - 0.05) < 1e-12)
tr, tn = tail(n, pb, 3), tail(n, pg, 3)
check("l17 recession tail rounds to 0.3222", round(tr, 4) == lv1["t"]["r"], str(tr))
check("l17 normal tail rounds to 0.0002", round(tn, 4) == lv1["t"]["n"], str(tn))
exact = q * tr + (1 - q) * tn
w = s["widget"]
shown = leaves["r-t"] + leaves["n-t"]
check("l17 key equals the two highlighted leaves added", abs(w["answer"] - shown) < 1e-9, str(shown))
check("l17 exact mixture tail inside key band", abs(exact - w["answer"]) <= w["tol"]["abs"], str(exact))
slips = {x["id"]: x["value"] for x in w["wrong"]}
check("l17 slip indep is the binomial(10, 0.05) tail", abs(slips["indep"] - tail(10, 0.05, 3)) < 5e-5)
check("l17 slip rec is the recession branch", slips["rec"] == lv1["t"]["r"])
check("l17 slip avg is the unweighted mean of the tails", abs(slips["avg"] - (lv1["t"]["r"] + lv1["t"]["n"]) / 2) < 1e-9)
check("l17 slip recw is the recession leaf to 4 places", abs(slips["recw"] - leaves["r-t"]) < 5e-5)
check("l17 key and slip bands disjoint", not bands_disjoint(w), str(bands_disjoint(w)))
check("l17 point hint highlights the recession 3-or-more path", s["hints"][1]["highlight"] == ["r-t"])
check("l17 explanation highlights both 3-or-more paths and shows leaves",
      sorted(s["explain"]["canvas"]["highlight"]) == ["n-t", "r-t"] and s["explain"]["canvas"]["values"] is True)
check("l17 leaves hidden before the answer", s["canvas"]["state"]["values"] is False)
check("l17 5.6 times the independent tail", round(w["answer"] / slips["indep"], 1) == 5.6)
check("l17 recession path carries most (over 99%)", leaves["r-t"] / shown > 0.99)
for txt in (w["accept"], s["hints"][2]["text"], s["feedback"]["correct"], s["explain"]["text"]):
    check("l17 string carries the tree's sum", "0.2 \\times 0.3222 + 0.8 \\times 0.0002" in txt, txt)

# Monte Carlo of the regime model: separates 0.0646 from the independent 0.0115 and from 0.0644 +- nothing needed
random.seed(20261111)
N = 400_000
hit = 0
for _ in range(N):
    p = pb if random.random() < q else pg
    k = sum(random.random() < p for _ in range(n))
    hit += k >= 3
est = hit / N
se = (exact * (1 - exact) / N) ** 0.5
check("l17 simulation agrees with the key (4 s.e.)", abs(est - w["answer"]) < 4 * se + w["tol"]["abs"], f"{est} se {se}")

# ---------------------------------------------------------------- l8 screens[2]
s8 = load("l8-base-rates.json")["screens"][2]
w8 = s8["widget"]
key8 = F(1, 100) * F(9, 10) + F(99, 100) * F(5, 100)
check("l8 key is 0.0585 exactly", key8 == F(585, 10000) and w8["answer"] == 0.0585)
check("l8 question asks for 4 places", "to 4 places" in s8["question"])
check("l8 key and slip bands disjoint", not bands_disjoint(w8), str(bands_disjoint(w8)))
right4 = round(float(key8), 4)
check("l8 right answer to 4 places is in the key band", abs(right4 - w8["answer"]) <= w8["tol"]["abs"])
check("l8 right answer to 4 places is in no slip band",
      all(not (band(x)[0] <= right4 <= band(x)[1]) for x in w8["wrong"]))
sl8 = {x["id"]: x["value"] for x in w8["wrong"]}
check("l8 slips follow from the tree",
      sl8["ill-only"] == 0.009 and abs(sl8["unweighted"] - (0.009 + 0.05)) < 1e-12 and abs(sl8["rates"] - 0.95) < 1e-12)

# ---------------------------------------------------------------- l11 screens[8]
s11 = load("l11-updating-twice.json")["screens"][8]
post = F(1, 2) * F(49, 100) / (F(1, 2) * F(49, 100) + F(1, 2) * F(9, 100))
check("l11 key 49/58", abs(float(post) - s11["widget"]["answer"]) < 1e-4)
check("l11 slip one is a single call", s11["widget"]["wrong"][0]["value"] == 0.7 and float(post) > 0.7)
check("l11 stem states independence given the direction", "Whichever way it goes, one analyst's mistake" in s11["prose"])
# with errors positively dependent given the direction, the second call adds less: independence is what the key needs
check("l11 key needs conditional independence", F(1, 2) * F(7, 10) / (F(1, 2) * F(7, 10) + F(1, 2) * F(3, 10)) == F(7, 10))

# ---------------------------------------------------------------- review-2 items[5]
r2 = load("review-2.json")["items"][5]
odds = F(1, 9)
check("review-2 key 0.5", (odds * 9) / (1 + odds * 9) == F(1, 2) and r2["widget"]["answer"] == 0.5)
added = odds * 6 / (1 + odds * 6)
check("review-2 slip added is 0.4", added == F(2, 5) and r2["widget"]["wrong"][2]["value"] == 0.4)
check("review-2 stem states independence in both states", "Battle or no battle, the two signals arise independently" in r2["prose"])

# ---------------------------------------------------------------- problems-2 items[1]
p2 = load("problems-2.json")["items"][1]
check("problems-2 stem states independence given the truth", "Given the truth, the two arise independently" in p2["prose"])
o1 = F(15, 85) * 3
o2 = o1 * 6
check("problems-2 part 3 key 54/71", abs(float(o2 / (1 + o2)) - p2["parts"][2]["widget"]["answer"]) < 5e-5)
rs = F(15, 85) * 9
check("problems-2 ratio-sum slip 27/44", abs(float(rs / (1 + rs)) - p2["parts"][2]["widget"]["wrong"][1]["value"]) < 5e-5)
need, o = 0, o2
while o / (1 + o) < F(95, 100):
    o *= 3
    need += 1
check("problems-2 part 4 key is 2", need == p2["parts"][3]["widget"]["answer"])
# joint check that ratios multiply under conditional independence: P(D | delay, exit) from the joint table
pd = F(15, 100)
num = pd * F(6, 10) * F(3, 10)
den = num + (1 - pd) * F(2, 10) * F(5, 100)
check("problems-2 joint table gives 54/71", num / den == F(54, 71))
# a dependent case: exit certain once there is a delay, in both states; the exit then adds nothing
num_d = pd * F(6, 10) * 1
den_d = num_d + (1 - pd) * F(2, 10) * 1
check("problems-2 dependent exit leaves 9/26, below 54/71", num_d / den_d == F(9, 26) and F(9, 26) < F(54, 71))

# ---------------------------------------------------------------- l15 summary
s15 = load("l15-pairwise.json")["summary"]["formula"]["note"]
check("l15 note names the default meaning", "mutually independent is meant" in s15)
# pairwise without triple (two coins: first H, second H, match), and triple without pairwise (a standard counterexample)
omega = [(a, b) for a in (0, 1) for b in (0, 1)]
A = {x for x in omega if x[0] == 1}
B = {x for x in omega if x[1] == 1}
C = {x for x in omega if x[0] == x[1]}
pr = lambda e: F(len(e), len(omega))
check("l15 pairwise holds, triple fails", pr(A & B) == pr(A) * pr(B) and pr(A & C) == pr(A) * pr(C)
      and pr(B & C) == pr(B) * pr(C) and pr(A & B & C) != pr(A) * pr(B) * pr(C))
om8 = range(1, 9)
A2, B2, C2 = {1, 2, 3, 4}, {1, 2, 3, 5}, {1, 6, 7, 8}
p8 = lambda e: F(len(e), 8)
check("l15 triple holds, a pair fails", p8(A2 & B2 & C2) == p8(A2) * p8(B2) * p8(C2) and p8(A2 & B2) != p8(A2) * p8(B2))

print()
if fails:
    print(f"{len(fails)} check(s) failed")
    sys.exit(1)
print("all checks passed")
