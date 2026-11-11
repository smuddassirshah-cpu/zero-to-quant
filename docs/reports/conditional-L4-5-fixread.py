#!/usr/bin/env python3
"""Fix-pass read, conditional levels 4 and 5 (round 1).

Derives each changed item's answer from the protocol as now worded, by exact
enumeration, and compares it with the graded key, the wrong[] values and the
numbers quoted in feedback. Run from the repo root; exits 0 on correct content.
"""
import json
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path("app/content/courses/conditional")
fails = []


def load(name):
    return json.loads((ROOT / f"{name}.json").read_text(encoding="utf-8"))


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def item(name, needle, key="prose"):
    hits = [d for d in walk(load(name)) if isinstance(d.get(key), str) and needle in d[key] and "widget" in d]
    if len(hits) != 1:
        fails.append(f"{name}: {len(hits)} items match {needle!r}")
        return None
    return hits[0]


def check(label, cond):
    print(("ok   " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def numeric(name, needle, exact, wrong=None, key="prose"):
    it = item(name, needle, key)
    if it is None:
        return
    w = it["widget"]
    tol = w["tol"]["abs"]
    check(f"{name} [{needle[:28]}] key {w['answer']} = {float(exact):.5f}", abs(w["answer"] - float(exact)) <= tol)
    slips = {s["id"]: s for s in w.get("wrong", [])}
    for s in slips.values():
        check(f"{name} [{needle[:28]}] slip {s['id']} is not the answer",
              abs(s["value"] - float(exact)) > tol + s["tol"]["abs"])
    for sid, val in (wrong or {}).items():
        check(f"{name} [{needle[:28]}] slip {sid} = {float(val):.5f}",
              sid in slips and abs(slips[sid]["value"] - float(val)) <= slips[sid]["tol"]["abs"])


def choice(name, needle, right_text):
    it = item(name, needle)
    if it is None:
        return
    right = [o for o in it["widget"]["options"] if o.get("correct")]
    check(f"{name} [{needle[:28]}] correct option holds {right_text}",
          len(right) == 1 and right_text in right[0]["text"])


def posterior(worlds, hypothesis):
    """worlds: list of (weight, outcome) already filtered by the evidence."""
    total = sum(w for w, _ in worlds)
    return sum(w for w, o in worlds if hypothesis(o)) / total


# ---- Monty Hall: host knows, must open a goat door other than yours, random tie-break
def monty(n_doors=3, pick=1, shut=None, tie="random"):
    """Posterior that the car is behind `pick`, given the host left `shut` closed."""
    others = [d for d in range(1, n_doors + 1) if d != pick]
    worlds = []
    for car in range(1, n_doors + 1):
        prior = F(1, n_doors)
        if car == pick:
            # host leaves one of the other doors shut
            if tie == "random":
                like = F(1, len(others))
            else:  # host always leaves the lowest-numbered other door shut (opens the highest)
                like = F(1) if shut == min(others) else F(0)
        else:
            like = F(1) if car == shut else F(0)
        worlds.append((prior * like, car))
    return posterior(worlds, lambda c: c == pick)


stay3 = monty(3, 1, shut=2)
check("Monty, 3 doors, random tie-break: stay 1/3, switch 2/3", stay3 == F(1, 3))
check("Monty, host always opens door 3 when he can: doors equal", monty(3, 1, shut=2, tie="fixed") == F(1, 2))
choice("l18-monty-hall", "He always opens another door to show a goat", "Switch")
choice("review-4", "He always shows a goat, picking at random", "\\dfrac{1}{3}")
numeric("l18-monty-hall", "The host opens 98 other doors", 1 - monty(100, 1, shut=57),
        {"half": F(1, 2), "one-door": F(1, 100)})
ex = item("review-4", "He always shows a goat, picking at random")
if ex:
    check("review-4 explain names 1/2 and 1 likelihoods",
          "\\tfrac{1}{2}$ from car 1" in ex["explain"]["text"] and "chance 1 from car 2" in ex["explain"]["text"])

# ---- Bertrand: clerk answers a fixed question about the whole box
boxes = {"GG": "GG", "GS": "GS", "SS": "SS"}
clerk = [(F(1, 3), b) for b in boxes if "G" in b]
numeric("l19-bertrands-box", "His rule is to say whether the box holds", posterior(clerk, lambda b: b == "GG"),
        {})
drawn = [(F(1, 3) * F(b.count("G"), 2), b) for b in boxes]
check("Bertrand, coin drawn at random is gold: GG 2/3", posterior(drawn, lambda b: b == "GG") == F(2, 3))
cards = ["RR", "BB", "RB"]
choice("l19-bertrands-box", "Does it have at least one red side", "\\dfrac{1}{2}")
check("three cards, yes to 'any red side?': RR 1/2",
      posterior([(F(1, 3), c) for c in cards if "R" in c], lambda c: c == "RR") == F(1, 2))

# ---- Two children and details: a yes to a question fixed in advance
def two_kids(k, q_special=None):
    """P(two boys | yes to 'is at least one a boy with the detail?'), k equally likely detail values."""
    types = [(s, d) for s in "BG" for d in range(k)]
    fam = [(F(1, len(types) ** 2), f) for f in product(types, repeat=2)
           if any(c == ("B", 0) for c in f)]
    return posterior(fam, lambda f: f[0][0] == "B" and f[1][0] == "B"), len(fam)


check("two children, yes to 'at least one boy?': 1/3", two_kids(1)[0] == F(1, 3))
p7, n7 = two_kids(7)
check("Tuesday boy: 27 families, 13/27", n7 == 27 and p7 == F(13, 27))
numeric("l21-tuesday-boy", "at least one child is a boy born on a Tuesday", 27, key="question")
check("morning boy (k=2) is above 1/3", two_kids(2)[0] == F(3, 7) and F(3, 7) > F(1, 3))
choice("l21-tuesday-boy", "Is at least one child a boy born in the morning", "Higher")
choice("l21-tuesday-boy", "at least one is a boy born in January", "\\dfrac{23}{47}")
check("January boy: 23/47", two_kids(12)[0] == F(23, 47))
numeric("l21-tuesday-boy", "born on the night shift", two_kids(3)[0], {"third": F(1, 3), "half": F(1, 2)})
choice("l21-tuesday-boy", "at least one is a boy with a certain detail", "365")
check("k = 365 is closest to 1/2 of the four details",
      abs(two_kids(365)[0] - F(1, 2)) < min(abs(two_kids(k)[0] - F(1, 2)) for k in (1, 2, 7)))
numeric("review-4", "at least one is a girl", two_kids(1)[0], {"half": F(1, 2), "prior": F(1, 4)})
numeric("review-4", "a boy born in winter", two_kids(4)[0], {"third": F(1, 3), "half": F(1, 2)})

fam3 = [f for f in product("BG", repeat=3) if "B" in f]
check("three children, yes to 'at least one boy?': 1/7", F(sum(f == ("B",) * 3 for f in fam3), len(fam3)) == F(1, 7))
choice("l20-two-children", "A family has three children", "\\dfrac{1}{7}")


def trait(q):
    """P(BB | yes to 'at least one boy with the trait?'), trait chance q whatever the sex."""
    worlds = []
    for sexes in product("BG", repeat=2):
        for has in product((True, False), repeat=2):
            w = F(1, 4)
            for h in has:
                w *= q if h else 1 - q
            if any(s == "B" and h for s, h in zip(sexes, has)):
                worlds.append((w, sexes))
    return posterior(worlds, lambda s: s == ("B", "B"))


numeric("homework-4", "at least one child is a left-handed boy", trait(F(1, 10)), {"third": F(1, 3), "half": F(1, 2)})
for q in (F(1, 10), F(1, 7), F(1, 3), F(1)):
    check(f"trait formula (2-q)/(4-q) at q={q}", trait(q) == (2 - q) / (4 - q))


def two_trades(p):
    worlds = [((p if a else 1 - p) * (p if b else 1 - p), (a, b))
              for a, b in product((True, False), repeat=2) if a or b]
    return posterior(worlds, lambda o: o == (True, True))


numeric("l20-two-children", "Did at least one of your trades make money", two_trades(F(3, 5)),
        {"first": F(3, 5), "prior": F(9, 25), "half": F(1, 2)})
numeric("homework-4", "You ask whether at least one of them won", two_trades(F(11, 20)),
        {"first": F(11, 20), "prior": F(121, 400)})

# ---- 10:17 check: a question fixed in advance about one minute of 390
p, m = F(3, 5), 390
worlds = []
for (w1, w2) in product((True, False), repeat=2):
    for (t1, t2) in product((True, False), repeat=2):  # placed at 10:17 or not
        wt = (p if w1 else 1 - p) * (p if w2 else 1 - p)
        wt *= (F(1, m) if t1 else 1 - F(1, m)) * (F(1, m) if t2 else 1 - F(1, m))
        if (w1 and t1) or (w2 and t2):
            worlds.append((wt, (w1, w2)))
exact = posterior(worlds, lambda o: o == (True, True))
check("10:17 check: exact answer 779/1299", exact == F(779, 1299))
choice("l21-tuesday-boy", "A compliance check asks one question", "0.60")
it = item("l21-tuesday-boy", "A compliance check asks one question")
if it:
    check("10:17 explain quotes 779/1299 and 3/7", "\\tfrac{779}{1299}" in it["explain"]["text"]
          and "\\tfrac{3}{7}" in it["explain"]["text"])
# a report that picks a winner at random and names its minute: likelihood 1/m from every family with a winner
named = [(wt * F(1, m), o) for wt, o in
         [((p if a else 1 - p) * (p if b else 1 - p), (a, b)) for a, b in product((True, False), repeat=2)]
         if o[0] or o[1]]
check("report naming a winner's minute: stays at 3/7", posterior(named, lambda o: o == (True, True)) == F(3, 7))

# ---- Roulette slips
numeric("l22-gamblers-fallacy", "A European roulette wheel has 18 red", F(18, 37),
        {"half": F(1, 2), "left": F(18, 37 - 8), "american": F(18, 38)})

# ---- p-values and false discoveries
numeric("l23-prosecutors-fallacy", "20 of the 1,000 strategies have a real edge",
        F(980) * F(1, 100) / (F(980) * F(1, 100) + 20 * F(1, 2)),
        {"swap": F(1, 100), "prior": F(98, 100), "edge": F(10) / (F(98, 10) + 10)})
numeric("l23-prosecutors-fallacy", "Suppose none of them has a real edge", 10)
hw = [d for d in walk(load("homework-5")) if d.get("id") == "h-long-pvalue"][0]
post = F(6) / (6 + F(49, 10))
check("homework-5 P(edge | pass) = 6/10.9 = 0.55", round(float(post), 2) == 0.55 and "\\dfrac{6}{10.9}" in hw["model"])


def edge_post(share, power, alpha):
    return share * power / (share * power + (1 - share) * alpha)


base = edge_post(F(10, 500), F(6, 10), F(1, 100))
check("homework-5 (c): larger share of real edges raises the posterior", edge_post(F(20, 500), F(6, 10), F(1, 100)) > base)
check("homework-5 (c): more power raises the posterior", edge_post(F(10, 500), F(8, 10), F(1, 100)) > base)
check("homework-5 (c): fewer false passes raises the posterior", edge_post(F(10, 500), F(6, 10), F(1, 200)) > base)

# ---- Simpson: hospitals and the two houses
x = (F(720) + 140) / 1000
y = (F(190) + 600) / 1000
check("l24 hospitals: X 0.86 overall, Y 0.79, Y ahead in both risk groups",
      x == F(86, 100) and y == F(79, 100) and F(600, 800) > F(140, 200) and F(190, 200) > F(720, 800))
r_all = F(40 * 7 + 10 * -6, 50)
s_all = F(25 * 8 + 25 * -2, 50)
check("problems-5 two houses: R 4.4, S 3.0 over all launches", r_all == F(44, 10) and s_all == 3)
l24 = load("l24-simpsons-paradox")
p5 = [d for d in walk(load("problems-5")) if d.get("id") == "p-two-houses"][0]
p5_text = " ".join(d["explain"]["text"] for d in walk(p5) if isinstance(d.get("explain"), dict))
check("l24 trap states both halves of the rule",
      "affects both the choice and the outcome" in l24["summary"]["trap"]
      and "never by one the choice itself changes" in l24["summary"]["trap"])
check("problems-5 explain applies the same rule to survival",
      "Survival is a result of the returns" in p5_text and "overall average is the fair comparison" in p5_text)

# ---- Survivorship gap: sign and size
for ps, es, ef in ((F(6, 10), 9, -3), (F(1, 2), 8, -2), (F(8, 10), 7, -6)):
    overall = ps * es + (1 - ps) * ef
    check(f"l25 bias = failure rate x shortfall ({ps}, {es}, {ef})", es - overall == (1 - ps) * (es - ef) and es > overall)

print(f"\n{len(fails)} failing checks")
sys.exit(1 if fails else 0)
