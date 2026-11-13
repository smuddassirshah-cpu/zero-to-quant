#!/usr/bin/env python3
"""Second reader's recompute for analysis problems-4 and problems-5.

Imports nothing from the author's script. Every key, every `wrong` value and
the numbers of prose, feedback and explain are typed here from the reader's own
working, then compared with the JSON. Route 1 is exact (sympy, fractions);
route 2 is a search, a grid or a direct numeric evaluation.

Exit 0 on correct content. A FINDING line is a check that fails on the content
as it stands (see docs/reviews/review-problems-analysis-4-5.md); it stays
failing until the content is fixed. The PROPOSED block checks the numbers of
the review's fixes and never affects the exit code of the content checks.
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr

import sympy as sp

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
BASE = os.path.join(ROOT, "app", "content", "courses", "analysis")
P4 = json.load(open(os.path.join(BASE, "problems-4.json")))
P5 = json.load(open(os.path.join(BASE, "problems-5.json")))

n_ok = 0
fails = []
findings = []


def ok(cond, label, finding=None):
    global n_ok
    if cond:
        n_ok += 1
    elif finding:
        findings.append(f"FINDING {finding}: {label}")
    else:
        fails.append(label)


def item(doc, iid):
    return next(i for i in doc["items"] if i["id"] == iid)


def part(doc, iid, k):
    return item(doc, iid)["parts"][k - 1]


def key(doc, iid, k):
    w = part(doc, iid, k)["widget"]
    return w.get("answer", w.get("answers"))


def tol(doc, iid, k):
    return part(doc, iid, k)["widget"].get("tol", {}).get("abs", 0)


def wrongs(doc, iid, k):
    return {w["id"]: w for w in part(doc, iid, k)["widget"].get("wrong", [])}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def text(doc, iid, k=None):
    p = item(doc, iid) if k is None else part(doc, iid, k)
    return "\n".join(strings(p))


def near(a, b, t):
    return abs(a - b) <= t + 1e-12


def check_key(doc, iid, k, mine, accepted=()):
    """Key equals mine inside the band; every listed rounding is taken."""
    a, t = key(doc, iid, k), tol(doc, iid, k)
    ok(near(a, float(mine), max(t, 1e-9) if t else 5e-8), f"{iid} part {k} key {a} vs mine {float(mine)}")
    for r in accepted:
        ok(near(a, r, t), f"{iid} part {k} refuses the rounding {r} (key {a}, tol {t})")


def check_wrong(doc, iid, k, mine):
    """Each wrong value equals my slip value, sits outside the key band, and
    no two bands overlap."""
    a, t = key(doc, iid, k), tol(doc, iid, k)
    ws = wrongs(doc, iid, k)
    ok(set(ws) == set(mine), f"{iid} part {k} wrong ids {sorted(ws)} vs mine {sorted(mine)}")
    for wid, v in mine.items():
        if wid not in ws:
            continue
        wv, wt = ws[wid]["value"], ws[wid].get("tol", {}).get("abs", 0)
        ok(near(wv, float(v), max(wt, 5e-8)), f"{iid} part {k} wrong {wid} {wv} vs mine {float(v)}")
        ok(abs(wv - a) > t + wt, f"{iid} part {k} wrong {wid} band meets the key band")
        ok(wid in part(doc, iid, k)["feedback"].get("byKey", {}), f"{iid} part {k} wrong {wid} has no line")
    vals = sorted((w["value"], w.get("tol", {}).get("abs", 0)) for w in ws.values())
    for (v1, t1), (v2, t2) in zip(vals, vals[1:]):
        ok(v2 - v1 > t1 + t2, f"{iid} part {k} two wrong bands overlap at {v1}, {v2}")


def has(doc, iid, k, *needles):
    s = text(doc, iid, k)
    for nd in needles:
        ok(nd in s, f"{iid} part {k}: expected text {nd!r}")


def smallest(pred, start=1, stop=10**6):
    for n in range(start, stop):
        if pred(n):
            return n
    raise ValueError


x, t_, k_ = sp.symbols("x t k", real=True)

# ---------------------------------------------------------------- set shape
for doc, lessons in ((P4, range(15, 20)), (P5, range(20, 25))):
    ok(3 <= len(doc["items"]) <= 5, f"{doc['id']} item count")
    ok(any(i["difficulty"] == 5 for i in doc["items"]), f"{doc['id']} has a difficulty 5")
    carried = set()
    for f in os.listdir(BASE):
        m = re.match(r"l(\d+)-", f)
        if m and int(m.group(1)) in lessons:
            carried |= set(json.load(open(os.path.join(BASE, f))).get("skills", []))
    typed = 0
    total = 0
    for it in doc["items"]:
        ok(3 <= it["difficulty"] <= 5, f"{it['id']} difficulty")
        ok(set(it["skills"]) <= carried, f"{it['id']} skills {it['skills']} not all in {sorted(carried)}")
        ok(3 <= len(it["parts"]) <= 5, f"{it['id']} part count")
        for p in it["parts"]:
            total += 1
            typed += p["widget"]["kind"] in ("numeric", "expression")
            ok("feedback" in p and "explain" in p, f"{it['id']} part lacks feedback or explain")
    ok(3 * typed >= 2 * total, f"{doc['id']} typed share {typed}/{total}")

# ====================================================== 4a p-cubic-bracket
I = "p-cubic-bracket"
f = x**3 + 6 * x - 13
ok(f.subs(x, 0) == -13 and f.subs(x, 2) == 7, f"{I} end values")
chord = sp.Rational(f.subs(x, 2) - f.subs(x, 0), 2)
ok(chord == 10, f"{I} chord slope")
cs = [r for r in sp.solve(sp.diff(f, x) - chord, x) if 0 < r < 2]
ok(len(cs) == 1 and sp.simplify(cs[0] - 2 / sp.sqrt(3)) == 0, f"{I} mean value point")
# route 2: bisection on f'(c) - 10
lo, hi = 0.0, 2.0
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 3 * mid * mid + 6 < 10 else (lo, mid)
ok(abs(lo - float(cs[0])) < 1e-12, f"{I} mean value point by bisection")
check_key(P4, I, 1, cs[0], accepted=(1.155,))
check_wrong(P4, I, 1, {"no-six": math.sqrt(10 / 3), "no-root": Fr(4, 3)})

K = max(3 * Fr(i, 1000) ** 2 + 6 for i in range(0, 2001))  # grid sup of f'
ok(K == 18 and sp.maximum(sp.diff(f, x), x, sp.Interval(0, 2)) == 18, f"{I} K")
check_key(P4, I, 2, 18)
check_wrong(P4, I, 2, {"chord": 10, "left-end": 6, "no-six": 12})

delta = Fr(9, 1000) / 18
ok(delta == Fr(1, 2000), f"{I} delta")
check_key(P4, I, 3, delta, accepted=(0.0005,))
check_wrong(P4, I, 3, {"times": Fr(9, 1000) * 18, "chord": Fr(9, 1000) / 10, "no-six": Fr(9, 1000) / 12})
# the bound really works: sample pairs closer than delta
worst = max(abs(f.subs(x, Fr(i, 4000) + Fr(49, 100000)) - f.subs(x, Fr(i, 4000))) for i in range(0, 7998, 7))
ok(worst < Fr(9, 1000), f"{I} |f(x) - f(y)| < 0.009 on sampled pairs")

halv = smallest(lambda n: Fr(2, 2**n) <= delta)
ok(halv == 12 and 2**11 == 2048 and 2**12 == 4096, f"{I} halvings")
ok(round(2 / 2**11, 5) == 0.00098 and round(2 / 2**12, 5) == 0.00049, f"{I} widths in feedback")
check_key(P4, I, 4, halv)
check_wrong(P4, I, 4, {"one-short": smallest(lambda n: Fr(1, 2**n) <= delta),
                       "eps": smallest(lambda n: Fr(2, 2**n) <= Fr(9, 1000))})
ok(halv - 1 == 11, f"{I} one-short is also 12 - 1")

bound = 18 * Fr(1, 4096)
ok(bound == Fr(9, 2048) and Fr(2, 2**12) == Fr(1, 2048), f"{I} final bound")
check_key(P4, I, 5, bound, accepted=(0.00439, 0.004395, float(Fr(9, 2048))))
check_wrong(P4, I, 5, {"full-width": 18 * Fr(1, 2048), "eps": Fr(9, 1000), "chord": 10 * Fr(1, 4096)})
# run the 12 halvings in exact fractions
a, b = Fr(0), Fr(2)
for _ in range(12):
    m = (a + b) / 2
    a, b = (m, b) if m**3 + 6 * m - 13 < 0 else (a, m)
m = (a + b) / 2
root = float(sp.nsolve(f, x, 1.5))
ok(b - a == Fr(1, 2048) and a < root < b, f"{I} bracket after 12 halvings")
ok(abs(float(m) - root) <= 1 / 4096 and abs(float(m**3 + 6 * m - 13)) <= float(bound), f"{I} midpoint obeys the bound")
has(P4, I, 5, "\\tfrac{9}{2048}", "0.00439")

# ====================================================== 4b p-quartic-roots
I = "p-quartic-roots"
h = x**4 - 8 * x**2 + 3
crit = sorted(sp.solve(sp.diff(h, x), x))
ok(crit == [-2, 0, 2], f"{I} zeros of h'")
inside = [c for c in crit if -1 < c < 3]
ok(sorted(key(P4, I, 1)) == inside == [0, 2], f"{I} part 1 key")
ok(wrongs(P4, I, 1)["lost-zero"]["value"].replace(" ", "") == "-2,2", f"{I} part 1 wrong")
cand = {c: h.subs(x, c) for c in (-1, 0, 2, 3)}
ok(cand == {-1: -4, 0: 3, 2: -13, 3: 12}, f"{I} candidate values {cand}")
grid = [Fr(i, 1000) for i in range(-1000, 3001)]
vals = [g**4 - 8 * g**2 + 3 for g in grid]
ok(max(vals) == 12 and min(vals) == -13, f"{I} grid extremes")
check_key(P4, I, 2, 12)
check_wrong(P4, I, 2, {"critical": 3, "no-three": 81 - 72})
check_key(P4, I, 3, -13)
check_wrong(P4, I, 3, {"sign": 13, "left-end": -4})
opts = {o["id"]: o for o in part(P4, I, 4)["widget"]["options"]}
ok([o for o in opts if opts[o].get("correct")] == ["at-most-three"], f"{I} part 4 key")
roots = sorted(float(r) for r in sp.real_roots(h) if -1 <= r <= 3)
ok(len(roots) == 3, f"{I} three roots in [-1, 3]: {roots}")
signs = sum(1 for u, v in zip(vals, vals[1:]) if u * v < 0 or u == 0)
ok(signs == 3, f"{I} sign changes on the grid")
ok([round(r, 2) for r in roots] == [-0.63, 0.63, 2.76], f"{I} roots in explain")
check_key(P4, I, 5, 3)
check_wrong(P4, I, 5, {"ends": 1, "degree": 4, "two": 2})

# ======================================================== 4c p-bump-series
I = "p-bump-series"
kk = sp.symbols("k", positive=True)
xx = sp.symbols("x", positive=True)
fk = xx * sp.exp(-kk**2 * xx)
peak = sp.solve(sp.diff(fk, xx), xx)
ok(peak == [1 / kk**2], f"{I} peak {peak}")
Mk = sp.simplify(fk.subs(xx, 1 / kk**2))
ok(sp.simplify(Mk - 1 / (sp.E * kk**2)) == 0, f"{I} M_k")
ok(sp.simplify(fk.subs(xx, 1 / kk) - sp.exp(-kk) / kk) == 0, f"{I} part 2 wrong one-k")
for kv in (1, 2, 5):  # route 2: grid sup
    g = max(i / 1e5 * math.exp(-kv * kv * i / 1e5) for i in range(0, 300001))
    ok(abs(g - 1 / (math.e * kv * kv)) < 1e-6, f"{I} grid sup k={kv}")
has(P4, I, 1, "\\frac{1}{k^2}")
has(P4, I, 2, "\\frac{1}{ek^2}")
# tail of 1/k^2 below 1/N
for N in (1, 5, 37, 200):
    ok(float(sp.zeta(2)) - sum(1 / j**2 for j in range(1, N + 1)) < 1 / N, f"{I} tail below 1/N at {N}")
N0 = smallest(lambda n: 1 / (math.e * n) < 0.01)
ok(N0 == 37 and round(100 / math.e, 2) == 36.79 and round(1 / (36 * math.e), 4) == 0.0102, f"{I} N")
check_key(P4, I, 3, N0)
check_wrong(P4, I, 3, {"round-down": 36, "no-e": smallest(lambda n: 1 / n < 0.01),
                       "square": smallest(lambda n: 1 / (math.e * n * n) < 0.01)})
opts = {o["id"]: o for o in part(P4, I, 4)["widget"]["options"]}
ok([o for o in opts if opts[o].get("correct")] == ["continuous"], f"{I} part 4 key")
d0 = Fr(1, 100) / 37
check_key(P4, I, 5, d0, accepted=(0.000270, float(Fr(1, 3700))))
check_wrong(P4, I, 5, {"n36": Fr(1, 3600), "whole-eps": Fr(2, 100) / 37, "one-term": Fr(1, 100)})


def S(xv, terms=4000):
    return sum(xv * math.exp(-j * j * xv) for j in range(1, terms + 1))


def S37(xv):
    return sum(xv * math.exp(-j * j * xv) for j in range(1, 38))


xs = [10 ** (-e / 10) for e in range(0, 80)]
ok(max(S(v) - S37(v) for v in xs) < 0.01, f"{I} true tail after 37 terms below 0.01")
ok(all(S37(v) <= 37 * v for v in xs), f"{I} S_37(x) <= 37x")
ok(all(S(float(d0) * j / 50) < 0.02 for j in range(0, 50)), f"{I} |S(x) - S(0)| < 0.02 in the window")
ok(S(1e-9) < 1e-4, f"{I} S continuous at 0 (S ~ sqrt(pi x)/2)")

# ========================================================= 5a p-root-sums
I = "p-root-sums"
# Fix pass: sqrt x on [0, 9] (note A ruled reuse, with finding 1 folded in).
U9 = sum(math.sqrt(j) for j in range(1, 10))
L9 = sum(math.sqrt(j) for j in range(0, 9))
ok(abs(U9 - 19.3060005) < 5e-8 and abs(U9 - L9 - 3) < 1e-12, f"{I} U_9, L_9")
check_key(P5, I, 1, U9, accepted=(19.3060,))
check_wrong(P5, I, 1, {"lower": L9, "ninth": U9 / 9})
nn = sp.symbols("n", positive=True, integer=True)
j = sp.symbols("j", integer=True)
gap = sp.simplify(sp.summation((9 / nn) * (sp.sqrt(9 * j / nn) - sp.sqrt(9 * (j - 1) / nn)), (j, 1, nn)))
ok(sp.simplify(gap - 27 / nn) == 0, f"{I} telescoped gap {gap}")
for N in (9, 10, 541):  # route 2: direct sums
    Un = sum(9 / N * math.sqrt(9 * i / N) for i in range(1, N + 1))
    Ln = sum(9 / N * math.sqrt(9 * i / N) for i in range(0, N))
    ok(abs(Un - Ln - 27 / N) < 1e-9 and Ln < 18 < Un, f"{I} sums at n={N}")
has(P5, I, 2, "\\frac{27}{n}")
integral = sp.integrate(sp.sqrt(x), (x, 0, 9))
ok(integral == 18 and abs(9 * sum(math.sqrt(9 * (i + 0.5) / 10**5) for i in range(10**5)) / 10**5 - 18) < 1e-5,
   f"{I} integral")
ok(sp.limit((sp.Rational(2, 3) * xx ** sp.Rational(3, 2)) / xx, xx, 0, "+") == 0, f"{I} G'(0+) = 0 = sqrt 0")
check_key(P5, I, 3, Fr(18), accepted=(18.0,))
check_wrong(P5, I, 3, {"no-coeff": 27, "flip": 40.5})
check_key(P5, I, 4, U9 - 18, accepted=(1.3060,))
check_wrong(P5, I, 4, {"gap": 3, "lower": 18 - L9})
# The part says "Using U_9 ~ 19.3060 ... and 18"; that rounded value gives the same 4-place answer (finding 1 cured).
from_rounded = round(19.3060 - 18, 4)
ok(from_rounded == 1.3060 and near(key(P5, I, 4), from_rounded, tol(P5, I, 4)),
   f"{I} part 4 takes the value its own stated input 19.3060 gives (key {key(P5, I, 4)}, tol {tol(P5, I, 4)})", finding="1")
ok("19.3060 - 18 = 1.3060" in text(P5, I, 4), f"{I} part 4 feedback subtraction is true", finding="1")
n0 = smallest(lambda n: Fr(27, n) < Fr(5, 100))
ok(n0 == 541, f"{I} smallest n")
check_key(P5, I, 5, n0)
check_wrong(P5, I, 5, {"equal": 540, "unit-width": smallest(lambda n: Fr(3, n) < Fr(5, 100)),
                       "no-height": smallest(lambda n: Fr(9, n) < Fr(5, 100))})
ok("[0, 4]" not in text(P5, I), f"{I} note A: no [0, 4] left", finding="A")

# ======================================================= 5b p-diamond-ball
I = "p-diamond-ball"
p = (Fr(15, 100), Fr(-40, 100))


def d1(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def d2(u, v):
    return math.hypot(float(u[0] - v[0]), float(u[1] - v[1]))


def dinf(u, v):
    return max(abs(u[0] - v[0]), abs(u[1] - v[1]))


O = (Fr(0), Fr(0))
ok(d1(O, p) == Fr(55, 100), f"{I} d1(0, p)")
check_key(P5, I, 1, d1(O, p))
check_wrong(P5, I, 1, {"signs": p[0] + p[1], "signs-size": abs(p[0] + p[1]), "straight": d2(O, p), "largest": dinf(O, p)})
r = 1 - d1(O, p)
check_key(P5, I, 2, r)
check_wrong(P5, I, 2, {"whole": d1(O, p), "straight": 1 - d2(O, p)})
edge = (Fr(375, 1000), Fr(-625, 1000))
ok(d1(O, edge) == 1 and d1(p, edge) == r and dinf(p, edge) == r / 2, f"{I} edge point")
s = float(r) / math.sqrt(2)
check_key(P5, I, 3, s, accepted=(0.3182,))
check_wrong(P5, I, 3, {"times": float(r) * math.sqrt(2), "same": r, "half": r / 2})
ok(abs(s - abs(float(p[0] - p[1]) - 1) / math.sqrt(2)) < 1e-12, f"{I} s is the true distance to the edge y1 - y2 = 1")
ok(near(key(P5, I, 3), round(0.45 / 1.414, 4), tol(P5, I, 3)), f"{I} part 3 takes the rounding from sqrt2 = 1.414")
check_key(P5, I, 4, r / 2)
check_wrong(P5, I, 4, {"times": 2 * r, "root-two": s, "same": r})
# route 2: sample the three balls and the comparison inequalities
import random

random.seed(5)
allin = True
ineq = True
for _ in range(20000):
    a1, a2 = random.uniform(-1, 1), random.uniform(-1, 1)
    q = (float(p[0]) + a1, float(p[1]) + a2)
    e1 = abs(a1) + abs(a2)
    e2 = math.hypot(a1, a2)
    ei = max(abs(a1), abs(a2))
    ineq &= e1 <= math.sqrt(2) * e2 + 1e-12 and e1 <= 2 * ei + 1e-12
    if e1 < float(r) or e2 < s or ei < float(r) / 2:
        allin &= abs(q[0]) + abs(q[1]) < 1
ok(allin and ineq, f"{I} sampled balls lie in U; d1 <= sqrt2 d2, d1 <= 2 dinf")
ok(d1(O, (p[0] + Fr(45, 100), p[1] - Fr(45, 100))) > 1, f"{I} square of half-side 0.45 pokes out")
opts = {o["id"]: o for o in part(P5, I, 5)["widget"]["options"]}
ok([o for o in opts if opts[o].get("correct")] == ["all"], f"{I} part 5 key")
# no longer l23's pair (finding 3), and the slip lines are true (finding 4)
l23 = open(os.path.join(BASE, "l23-open-and-closed.json")).read()
ok(not ("1 - 0.7 = 0.3" in l23 and key(P5, I, 1) == 0.7 and key(P5, I, 2) == 0.3),
   f"{I} parts 1 and 2 key pair is l23's '$r = 1 - 0.7 = 0.3$'", finding="3")
ok(any(abs(w["value"] + 0.25) < 1e-9 for w in wrongs(P5, I, 1).values()) and
   any(abs(w["value"] - 0.25) < 1e-9 for w in wrongs(P5, I, 1).values()),
   f"{I} part 1 slip 0.15 + (-0.4) = -0.25 and its size 0.25 both have a line", finding="4")

# =================================================== 5c p-accumulated-cubic
I = "p-accumulated-cubic"
# Fix pass: f(t) = t^2 - 12t + 27 = (t - 3)(t - 9) on [0, 15]. The reader's t^2 - 8t + 12 is functions/l11's (x - 2)(x - 6).
fi = t_**2 - 12 * t_ + 27
F = sp.integrate(fi, (t_, 0, x))
ok(sp.expand(F - (x**3 / 3 - 6 * x**2 + 27 * x)) == 0 and sp.expand(F - x * (x - 9) ** 2 / 3) == 0, f"{I} F")
has(P5, I, 1, "\\frac{x^3}{3}-6x^2+27x")
ok(sorted(sp.solve(fi, t_)) == [3, 9] == sorted(key(P5, I, 2)), f"{I} critical points")
ok(sorted(sp.solve(F, x)) == [0, 9] and wrongs(P5, I, 2)["zeros-of-big-f"]["value"].replace(" ", "") == "0,9", f"{I} zeros of F")
Fv = {c: F.subs(x, c) for c in (0, 3, 9, 15)}
ok(Fv == {0: 0, 3: 36, 9: 0, 15: 180}, f"{I} candidates {Fv}")
gridF = [Fr(i, 1000) for i in range(0, 15001)]
Fg = [g**3 / 3 - 6 * g**2 + 27 * g for g in gridF]
ok(max(Fg) == 180 and Fg.index(max(Fg)) == 15000 and max(Fg[:-1]) < 180, f"{I} max at 15 only")
check_key(P5, I, 3, Fr(180), accepted=(180.0,))
check_wrong(P5, I, 3, {"critical": 36, "no-third": 3375 - 1350 + 405})
opts = {o["id"]: o for o in part(P5, I, 4)["widget"]["options"]}
ok([o for o in opts if opts[o].get("correct")] == ["not-closed"], f"{I} part 4 key")
ok(F.subs(x, sp.Rational(29, 2)) == sp.Rational(29, 2) * sp.Rational(11, 2) ** 2 / 3
   and round(float(F.subs(x, sp.Rational(29, 2))), 2) == 146.21, f"{I} F(14.5)")
supf = max(abs(g * g - 12 * g + 27) for g in gridF)
ok(supf == 72 and abs(fi.subs(t_, 0)) == 27 and fi.subs(t_, 6) == -9, f"{I} sup |f| = 72 at 15")
n1 = smallest(lambda n: Fr(72, n) < Fr(7, 100))
ok(n1 == 1029 and round(72 / 1028, 5) == 0.07004, f"{I} n")
check_key(P5, I, 5, n1)
check_wrong(P5, I, 5, {"round-down": 1028, "left-end": smallest(lambda n: Fr(27, n) < Fr(7, 100)),
                       "no-bound": smallest(lambda n: Fr(1, n) < Fr(7, 100))})
xn = 15 - Fr(1, n1)
ok(0 < 180 - (xn**3 / 3 - 6 * xn**2 + 27 * xn) <= Fr(72, n1) < Fr(7, 100), f"{I} true gap at n = 1029")
l18 = open(os.path.join(BASE, "l18-mean-value-proved.json")).read()
ok(not ("x^2 - 4x + 3 = (x - 1)(x - 3)" in l18 and "t^2 - 4t + 3 = (t - 1)(t - 3)" in text(P5, I)),
   f"{I} integrand is l18's g(x) = x^2 - 4x + 3", finding="2")
for other in ("functions/l11-reading-a-graph.json", "quadratics/l11-meeting-the-axis.json"):
    src = open(os.path.join(ROOT, "app", "content", "courses", other)).read()
    ok("(x - 3)(x - 9)" not in src and "x^2 - 12x + 27" not in src, f"{I} (t - 3)(t - 9) is not in {other}", finding="2")

# ============================================================== finding 5
I = "p-cubic-bracket"
t45 = text(P4, I, 4) + text(P4, I, 5)
ok("root $c$" not in t45 and "f(c)" not in t45 and "|m - c|" not in t45 and "root $r$" in t45 and "f(r)" in t45,
   f"{I} parts 4 and 5 name the root r, not c (c is part 1's mean value point)", finding="5")
prop_fail = []

print(f"content checks passed: {n_ok}")
for line in findings:
    print(line)
for line in fails:
    print("FAIL", line)
print(f"proposed-fix checks failing: {len(prop_fail)} {prop_fail if prop_fail else ''}")
print(f"{len(findings)} finding line(s), {len(fails)} unexpected failure(s)")
sys.exit(1 if (findings or fails) else 0)
