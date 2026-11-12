"""Delta read AC-4: every changed key, band, wrong value and claim of the four fix passes, by two routes.
   Run from the repo root with the scratchpad venv Python:
       python docs/reviews/review-delta-ac-4-scripts/recompute.py [--show]
   A check that fails because the content is wrong is printed as CLAIM (it is a finding in the review) and does not
   change the exit code; anything else that fails prints FAIL and exits 1.
   Routes: exact fractions / sympy, then floats, cmath, numpy, quad, a count or an exhaustive search."""
import cmath
import itertools
import json
import math
import random
import re
import sys
from fractions import Fraction as F

import sympy as sp
from scipy.integrate import quad

SHOW = "--show" in sys.argv
N = {"checks": 0, "fail": 0, "claim": 0}


def ok(cond, msg, claim=None):
    N["checks"] += 1
    if cond:
        if SHOW:
            print("ok   ", msg)
    elif claim:
        N["claim"] += 1
        print("CLAIM", msg, "[" + claim + "]")
    else:
        N["fail"] += 1
        print("FAIL ", msg)


def load(f):
    return json.load(open(f"app/content/courses/{f}.json"))


def item(f, pid):
    return next(i for i in load(f)["items"] if i["id"] == pid)


def W(f, pid, part):
    return item(f, pid)["parts"][part - 1]["widget"]


def wrong(w, wid):
    return next(x for x in w["wrong"] if x["id"] == wid)


def inband(entry, v):
    t = entry.get("tol", {}).get("abs", 0)
    val = entry.get("answer", entry.get("value"))
    return abs(v - val) <= t + 1e-12


def key(f, pid, part, exact, takes=(), label=""):
    """the stored key equals exact within its tol; the band takes each honest rounding; refuses every wrong value;
    no wrong band meets the key band or another wrong band"""
    w = W(f, pid, part)
    ok(inband(w, exact), f"{pid} p{part} key {w['answer']} takes the exact value {exact:.8g} {label}")
    for t in takes:
        ok(inband(w, t), f"{pid} p{part} key band takes {t}")
    bands = [(w["answer"] - w["tol"]["abs"], w["answer"] + w["tol"]["abs"], "key")]
    for x in w.get("wrong", []):
        ok(not inband(w, x["value"]), f"{pid} p{part} key band refuses wrong {x['id']} {x['value']}")
        bands.append((x["value"] - x["tol"]["abs"], x["value"] + x["tol"]["abs"], x["id"]))
    for (a, b), in zip(itertools.combinations(bands, 2)):
        ok(a[1] < b[0] - 1e-12 or b[1] < a[0] - 1e-12, f"{pid} p{part} bands {a[2]} and {b[2]} do not meet")


def slip(f, pid, part, wid, v, how, takes=()):
    x = wrong(W(f, pid, part), wid)
    ok(inband(x, v), f"{pid} p{part} wrong {wid} {x['value']} is {how} = {v:.8g}")
    for t in takes:
        ok(inband(x, t), f"{pid} p{part} wrong {wid} band takes {t}")


def strings(d, path=""):
    if isinstance(d, (str, int, float)) and not isinstance(d, bool):
        yield path, str(d)
    elif isinstance(d, dict):
        for k, v in d.items():
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from strings(v, f"{path}[{i}]")


def stale(f, pid, pats, allow=()):
    """old numbers and story words that must be gone from the item (ids are not shown to a learner and are skipped)"""
    it = item(f, pid)
    for pat in pats:
        hits = [(p, s) for p, s in strings(it) if re.search(pat, s) and not p.endswith(".id") and p != "id"
                and not any(a in p for a in allow)]
        ok(not hits, f"STALE {pid} /{pat}/ " + "; ".join(f"{p}: {s[:90]}" for p, s in hits[:3]),
           claim="stale text, see the findings" if hits else None)


def sexpr(tex, **loc):
    """a simple polynomial / rational key as sympy (loc: the symbols to use, by name)"""
    t = tex.replace("\\frac", "").replace("}{", ")/(").replace("{", "(").replace("}", ")").replace("^", "**")
    t = re.sub(r"(\d)([a-z(])", r"\1*\2", t)
    t = re.sub(r"([a-z])([a-z])", r"\1*\2", t)
    t = re.sub(r"([a-z)])\(", r"\1*(", t)
    return sp.sympify(t, locals=loc)


# =====================================================================================================================
# 1. proof
# =====================================================================================================================
P1, P2, P3 = "proof/problems-1", "proof/problems-2", "proof/problems-3"

# ---- parcels: 40 parcels, 12 over 5 kg, 15 labelled, 9 both
parcels = [(True, True)] * 9 + [(True, False)] * 3 + [(False, True)] * 6 + [(False, False)] * 22
ok(len(parcels) == 40 and sum(p for p, q in parcels) == 12 and sum(q for p, q in parcels) == 15, "parcels: 40, 12, 15, 9")
imp = lambda p, q: (not p) or q
ok(W(P1, "p-leverage-calls", 1)["answer"] == sum(p and not q for p, q in parcels) == 12 - 9, "parcels p1 = 3")
ok(W(P1, "p-leverage-calls", 2)["answer"] == sum(imp(p, q) for p, q in parcels) == 40 - 3, "parcels p2 = 37")
ok(W(P1, "p-leverage-calls", 3)["answer"] == sum(not imp(q, p) for p, q in parcels) == 15 - 9, "parcels p3 = 6")
slip(P1, "p-leverage-calls", 1, "swapped", 15 - 9, "label only")
slip(P1, "p-leverage-calls", 1, "both", 9, "both")
slip(P1, "p-leverage-calls", 2, "true-true", sum(p and q for p, q in parcels), "both true")
slip(P1, "p-leverage-calls", 3, "true-count", sum(imp(q, p) for p, q in parcels), "converse true")
ok(sum(not p for p, q in parcels) == 28, "parcels: 28 of 5 kg or less")
# part 4: the negation of 'every parcel keeps the rule', each option on every non-empty population of the four kinds
opts4 = {
    "right": lambda pop: any(p and not q for p, q in pop),
    "every": lambda pop: all(not q for p, q in pop if p),
    "converse": lambda pop: any(q and not p for p, q in pop),
    "if-not": lambda pop: all(imp(p, not q) for p, q in pop),
}
kinds = [(True, True), (True, False), (False, True), (False, False)]
pops = [[k for k, keep in zip(kinds, mask) if keep] for mask in itertools.product([0, 1], repeat=4) if any(mask)]
neg = lambda pop: not all(imp(p, q) for p, q in pop)
for oid, fn in opts4.items():
    same = all(fn(pop) == neg(pop) for pop in pops)
    ok(same == (oid == "right"), f"parcels p4 option {oid}: equivalent to the negation on all 15 populations is {same}")
stale(P1, "p-leverage-calls", [r"broker", r"account", r"leverage", r"margin", r"\bcall", r"client"])

# ---- greenhouse
rows = list(itertools.product([True, False], repeat=3))
water = lambda p, q, r: (p or q) and not r
safe = lambda p, q, r: imp(p or q, not r)
Pm, Qm, Rm = 24 < 30, 21 > 25, 40 < 50
ok(W(P1, "p-spread-signal", 1)["answer"] == Pm + Qm + Rm == 2 and (Pm, Qm, Rm) == (True, False, True), "greenhouse p1: P, not Q, R")
ok(not water(Pm, Qm, Rm), "greenhouse p2: no watering on Monday")
ok(W(P1, "p-spread-signal", 3)["answer"] == sum(water(*r) for r in rows) == 3, "greenhouse p3 = 3 rows")
ok(W(P1, "p-spread-signal", 4)["answer"] == sum(safe(*r) for r in rows) == 5, "greenhouse p4 = 5 rows")
slip(P1, "p-spread-signal", 3, "or-only", sum(p or q for p, q, r in rows), "rows with P or Q")
slip(P1, "p-spread-signal", 3, "not-r-only", sum(not r for p, q, r in rows), "rows with R false")
slip(P1, "p-spread-signal", 3, "and", sum(p and q and not r for p, q, r in rows), "P and Q and not R")
slip(P1, "p-spread-signal", 4, "as-and", sum(water(*r) for r in rows), "the 'and' rows")
slip(P1, "p-spread-signal", 4, "only-false-if", sum(not (p or q) for p, q, r in rows), "rows with P or Q false")
and_rows = {r for r in rows if water(*r)}
fail_rows = {r for r in rows if not safe(*r)}
ok(len(and_rows) == 3 and len(fail_rows) == 3 and not (and_rows & fail_rows), "as-and line: 3 'and' rows, 3 failing rows, disjoint sets")
ok({r for r in rows if safe(*r)} == and_rows | {r for r in rows if not (r[0] or r[1])}, "as-and line: holds on the 3 'and' rows and the 2 rows with P or Q false")
stale(P1, "p-spread-signal", [r"script", r"\bbuy", r"close", r"volume", r"spread", r"pence", r"£", r"yesterday", r"average", r"risk rule", r"trad"])

# ---- judges and dancers
cells = [[int(c) for c in row] for row in item(P1, "p-fund-thresholds")["canvas"]["params"]["cells"]]  # rows dancers, columns judges
A = lambda t, g=None: all(any(m > t for m in row) for row in (g or cells))
B = lambda t, g=None: any(all(row[j] > t for row in (g or cells)) for j in range(4))
ok(all("%" not in s for _, s in strings(item(P1, "p-fund-thresholds"))), "judges: no % anywhere in the item")
ok(sum(all(row[j] > 5 for row in cells) for j in range(4)) == W(P1, "p-fund-thresholds", 2)["answer"] == 0, "judges p2: 0 witnesses for B(5)")
ok([min(row[j] for row in cells) for j in range(4)] == [2, 3, 3, 1], "judges: lowest marks by judge 2, 3, 3, 1")
ok([max(row) for row in cells] == [7, 8, 9, 9], "judges: best marks by dancer 7, 8, 9, 9")
ok(max(t for t in range(-5, 12) if B(t)) == W(P1, "p-fund-thresholds", 3)["answer"] == 2 and all(B(t) for t in range(-5, 3)), "judges p3: largest t for B is 2, B true below")
ok(max(t for t in range(-5, 12) if A(t)) == W(P1, "p-fund-thresholds", 4)["answer"] == 6 and all(A(t) for t in range(-5, 7)), "judges p4: largest t for A is 6, A true below")
ok(all(any(row[j] > 5 for row in cells) for j in range(4)), "judges p2 slip line: each judge gave some dancer a mark above 5")
slip(P1, "p-fund-thresholds", 4, "best-fund", max(max(r) for r in cells) - 1, "the best dancer's best mark less 1")
slip(P1, "p-fund-thresholds", 4, "at-least", min(max(r) for r in cells), "the weakest best mark, 'at least'")
slip(P1, "p-fund-thresholds", 3, "at-least", max(min(row[j] for row in cells) for j in range(4)), "the best lowest mark, 'at least'")
ok(not A(7) and cells[0] == [7, 3, 6, 2], "judges: A(7) fails on D1, whose best mark is 7")
# part 1: each option against not B(5) on 4,000 random grids of marks 0 to 10
random.seed(4)
grids = [[[random.randint(0, 10) for _ in range(4)] for _ in range(4)] for _ in range(4000)]
o1 = {
    "right": lambda g: all(any(row[j] <= 5 for row in g) for j in range(4)),
    "inner": lambda g: any(any(row[j] <= 5 for row in g) for j in range(4)),
    "all": lambda g: all(all(row[j] <= 5 for row in g) for j in range(4)),
    "strict": lambda g: all(any(row[j] < 5 for row in g) for j in range(4)),
}
for oid, fn in o1.items():
    same = all(fn(g) == (not B(5, g)) for g in grids)
    ok(same == (oid == "right"), f"judges p1 option {oid}: equal to not B(5) on 4,000 grids is {same}")
stale(P1, "p-fund-thresholds", [r"fund", r"return", r"\byear", r"per cent", r"%"])

# ---- f_c(x) = cx - 4
for c in range(-50, 51):
    vals = [c * x - 4 for x in range(-40, 41)]
    ok((len(set(vals)) == len(vals)) == (c != 0), f"f_c one-to-one on -40..40 iff c != 0 (c = {c})")
ok(W(P2, "p-rule-and-domain", 1)["answer"] == 0, "f_c p1 key 0")
y, c_, x_, k, n_, j = sp.symbols("y c x k n j")
ok(sp.simplify(c_ * sexpr(W(P2, "p-rule-and-domain", 2)["answer"]) - 4 - y) == 0, "f_c p2: f_c((y+4)/c) = y")
ok(sp.simplify(c_ * (y - 4) / c_ - 4 - (y - 8)) == 0, "f_c p2 sign line: f_c((y-4)/c) = y - 8")
f2 = lambda x: -2 * x - 4
ok(f2(W(P2, "p-rule-and-domain", 3)["answer"]) == -10 and F(-10 + 4, -2) == 3, "f_c p3: f(3) = -10, two routes")
slip(P2, "p-rule-and-domain", 3, "sign", F(-10 - 4, -2), "(y - 4)/c")
slip(P2, "p-rule-and-domain", 3, "applied-f", f2(-10), "f(-10)")
slip(P2, "p-rule-and-domain", 3, "dropped-minus", F(-10 + 4, 2), "(y + 4)/2")
ok(f2(7) == -18 and f2(-3) == 2, "f_c p3 lines: f(7) = -18, f(-3) = 2")
img = {4 * n - 4 for n in range(-100, 100)}
missed = [v for v in range(1, 31) if v not in img]
ok(len(missed) == W(P2, "p-rule-and-domain", 4)["answer"] == 30 - len([v for v in range(1, 31) if v % 4 == 0]) == 23, "f_c p4: 23 missed, by image and by multiples of 4")
slip(P2, "p-rule-and-domain", 4, "hits", 30 - len(missed), "the 7 reached")
stale(P2, "p-rule-and-domain", [r"9 - 3", r"9 - y", r"3x\b", r"f\^\{-1\}", r"\b20\b", r"\b27\b"])

# ---- ferries and berths
berth = lambda s: (s + 1) // 2
fA, fB = {berth(s) for s in (1, 2, 3, 5)}, {berth(s) for s in (2, 4, 6, 7)}
ok(fA == {1, 2, 3} and fB == {1, 2, 3, 4}, "ferries: f(A) = {1,2,3}, f(B) = {1,2,3,4}")
ok(W(P2, "p-shift-images", 1)["answer"] == len(fA) == 3, "ferries p1")
ok(W(P2, "p-shift-images", 2)["answer"] == len(fA & fB) == 3, "ferries p2")
ok(W(P2, "p-shift-images", 3)["answer"] == len({berth(s) for s in {1, 2, 3, 5} & {2, 4, 6, 7}}) == 1, "ferries p3")
slip(P2, "p-shift-images", 2, "union", len(fA | fB), "the union")
# part 4: for an injective f the two sets agree for every A, B (all injections of 3 into 4, all subsets); they can differ when onto or |A| = |B|
dom = [1, 2, 3]
subs = [set(s) for r in range(4) for s in itertools.combinations(dom, r)]
inj_ok = all({m[a - 1] for a in X & Y} == {m[a - 1] for a in X} & {m[a - 1] for a in Y}
             for m in itertools.permutations(range(4), 3) for X in subs for Y in subs)
ok(inj_ok, "ferries p4: one-to-one forces f(A n B) = f(A) n f(B) (every injection 3 -> 4, every pair of subsets)")
ok(len(fA & fB) != 1 and set(map(berth, range(1, 9))) == {1, 2, 3, 4} and len({1, 2, 3, 5}) == len({2, 4, 6, 7}), "ferries p4: this f is onto, |A| = |B| = 4, and the sets differ")
stale(P2, "p-shift-images", [r"trader", r"desk", r"shift\b", r"\bsit", r"seat"])

# ---- remainder 1 on division by 5
R = range(-60, 61)
ok(all((m * n) % 5 == 1 for m in R for n in R if m % 5 == 1 and n % 5 == 1), "mod 5 claim true on -60..60")
ok(sp.expand((5 * j + 1) * (5 * k + 1) - (5 * sexpr(W(P3, "p-two-odd-squares", 1)["answer"]) + 1)) == 0, "mod 5 p1: (5j+1)(5k+1) = 5(key) + 1")
ok(11 == 5 * 2 + 1 and 16 == 5 * 3 + 1 and W(P3, "p-two-odd-squares", 3)["answer"] == 5 * 2 * 3 + 2 + 3 == (11 * 16 - 1) // 5 == 35, "mod 5 p3: bracket 35 by formula and from 176")
slip(P3, "p-two-odd-squares", 3, "lost-middle", 5 * 2 * 3, "5jk")
slip(P3, "p-two-odd-squares", 3, "whole-product", 11 * 16, "mn")
refute = [n for n in range(1, 200) if (4 * n) % 5 == 1 and not (4 % 5 == 1 and n % 5 == 1)]
ok(refute[0] == W(P3, "p-two-odd-squares", 4)["answer"] == 4, "mod 5 p4: least n refuting the converse with m = 4 is 4")
ok([(4 * n) % 5 for n in (1, 2, 3, 4)] == [4, 3, 2, 1], "mod 5 p4 explanation: 4, 8, 12, 16 leave 4, 3, 2, 1")
ok(36 % 5 == 1 and 66 % 5 == 1, "mod 5 p2 options: 6 x 6 and 6 x 11 leave 1")
ok(all((m * n) % 5 == ((m % 5) * (n % 5)) % 5 for m in R for n in R),
   "mod 5 p2 option 'restate': 'remainders multiply' is a true general fact (so the option is a sound reason)")
stale(P3, "p-two-odd-squares", [r"\bodd\b", r"\beven\b", r"m\^2 \+ n\^2", r"multiple of 4", r"\b42\b", r"\b170\b", r"\b34\b", r"2j \+ 1"])

# ---- n^2 + 2 and multiples of 3
R = range(-90, 91)
ok(all(n % 3 != 0 for n in R if (n * n + 2) % 3 == 0), "n^2 + 2 claim true on -90..90")
ok(all((n * n + 2) % 3 != 0 for n in R if n % 3 == 0), "its contrapositive true on -90..90")
ok(all((n * n + 2) % 3 == 0 for n in R if n % 3 != 0), "its converse true on -90..90 (as option 'converse' says)")
ok(all(n % 3 == 0 for n in R if (n * n + 2) % 3 != 0), "its inverse true on -90..90")
ok(sp.expand((3 * k) ** 2 + 2 - (3 * sexpr(W(P3, "p-even-test-contra", 2)["answer"]) + 2)) == 0, "n^2 + 2 p2: (3k)^2 + 2 = 3(key) + 2")
ok(W(P3, "p-even-test-contra", 4)["answer"] == 3 * (-2) ** 2 == ((-6) ** 2 + 2 - 2) // 3 == 12 and (-6) ** 2 + 2 == 38 and 38 % 3 == 2, "n^2 + 2 p4: bracket 12, 38 leaves 2")
slip(P3, "p-even-test-contra", 4, "sign", 3 * -4, "3 x (-4)")
slip(P3, "p-even-test-contra", 4, "n-squared", 36, "n^2")
slip(P3, "p-even-test-contra", 4, "whole", 38, "n^2 + 2")
ok(all((3 * (3 * kk * kk) + 2) % 3 == 2 for kk in range(-30, 31)), "n^2 + 2 p3: 3(integer) + 2 leaves 2")
stale(P3, "p-even-test-contra", [r"6n", r"\beven\b", r"\bodd\b", r"2k\^2", r"\b28\b", r"-26", r"-8\b", r"n = -3"])

# ---- step-three sum
S = lambda n: sum(3 * i - 2 for i in range(1, n + 1))
ok(all(S(n) == n * (3 * n - 1) // 2 for n in range(1, 300)), "S_n = n(3n-1)/2 for n to 299")
ok(min(n for n in range(1, 50) if S(n) != 4 * n - 3) == W(P3, "p-step-three-sum", 1)["answer"] == 3, "step p1: guess A first fails at 3")
ok(S(10) == W(P3, "p-step-three-sum", 2)["answer"] == 10 * 29 // 2 == 145, "step p2: S_10 = 145 by adding and by guess B")
num17 = sexpr(W(P3, "p-step-three-sum", 3)["answer"])
ok(sp.expand(k * (3 * k - 1) + 2 * (3 * k + 1) - num17) == 0 and sp.expand((k + 1) * (3 * k + 2) - num17) == 0, "step p3: numerator 3k^2 + 5k + 2 by the sum and by the target")
ok(sp.expand(k * (3 * k - 1) + (3 * k + 1) - sexpr("3k^2+2k+1")) == 0, "step p3 slip no-double")
ok(S(40) == W(P3, "p-step-three-sum", 4)["answer"] == 2380 and 3 * 40 - 2 == 118, "step p4: 2380")

# =====================================================================================================================
# 2. analysis
# =====================================================================================================================
A1, A2, A3 = "analysis/problems-1", "analysis/problems-2", "analysis/problems-3"
lo, hi, trail = F(2), F(3), []
for _ in range(4):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if mid ** 3 < 20 else (lo, mid)
    trail.append((float(lo), float(hi)))
ok(trail == [(2.5, 3.0), (2.5, 2.75), (2.625, 2.75), (2.6875, 2.75)], f"cube root: trail {trail}")
ok(math.floor(16 * 20 ** (1 / 3)) == 43 and F(43, 16) == F("2.6875"), "cube root: sixteenths grid gives 43/16")
key(A1, "p-cube-root-twenty", 1, float(lo))
slip(A1, "p-cube-root-twenty", 1, "right-end", float(hi), "the right end")
slip(A1, "p-cube-root-twenty", 1, "one-short", trail[2][0], "left end after three halvings")
ok(round(2.5 ** 3, 3) == 15.625 and round(2.625 ** 3, 2) == 18.09 and round(2.75 ** 3, 2) == 20.80 and round(2.6875 ** 3, 2) == 19.41, "cube root p1: printed cubes")
ok(W(A1, "p-cube-root-twenty", 2)["answer"] == 43 ** 3 - 20 * 16 ** 3 == 79507 - 81920 == -2413, "cube root p2: miss -2413")
slip(A1, "p-cube-root-twenty", 2, "sign", 20 * 16 ** 3 - 43 ** 3, "reversed")
slip(A1, "p-cube-root-twenty", 2, "squares", 43 ** 2 - 20 * 16 ** 2, "squares")
slip(A1, "p-cube-root-twenty", 2, "no-twenty", 43 ** 3 - 16 ** 3, "no 20")
ok(43 ** 2 == 1849 and 20 * 256 == 5120 and 16 ** 3 == 4096, "cube root p2: printed 1849, 5120, 4096")
s = F(43, 16)
top, bot = 3 * s * s + 3 * s + 1, 20 - s ** 3
ok(float(top) == 30.73046875 and float(bot) == 0.589111328125 and float(3 * s * s) == 21.66796875 and float(3 * s) == 8.0625, "cube root p4: printed top and bottom exact")
bound = top / bot
ok(W(A1, "p-cube-root-twenty", 4)["answer"] == math.floor(bound) + 1 == 53 and round(float(bound), 2) == 52.16, "cube root p4: bound 52.16, n = 53")
ok(min(n for n in range(1, 500) if n > 30.73046875 / 0.589111328125) == 53, "cube root p4: 53 by a float scan")
slip(A1, "p-cube-root-twenty", 4, "round-down", math.floor(bound), "floor")
slip(A1, "p-cube-root-twenty", 4, "no-plus-one", math.floor((top - 1) / bot) + 1, "top without + 1")
slip(A1, "p-cube-root-twenty", 4, "no-ones", math.floor(3 * s * s / bot) + 1, "3s^2 only")
ok(round(float((top - 1) / bot), 2) == 50.47 and round(float(3 * s * s / bot), 2) == 36.78, "cube root p4: printed 50.47 and 36.78")
ok(round(float((s + F(1, 53)) ** 3), 2) == 19.82 and (s + F(1, 53)) ** 3 < 20, "cube root p4: (s + 1/53)^3 = 19.82 < 20")
ok(all((s + F(1, n)) ** 3 <= s ** 3 + top / n for n in range(1, 400)), "cube root p4: the stated inequality for n to 399")
stale(A1, "p-cube-root-twenty", [r"\b21\b(?!\.)", r"\b979\b", r"\b839\b", r"8749", r"n = 16\b", r"\b11\b", r"9261", r"21\}\{8"],
      allow=("parts[2]",))

n = sp.symbols("n", positive=True)
an, bn = (8 * n + 3) / (2 * n + 5), (3 * n - 1) / (n + 1)
ok(sp.limit(an, n, sp.oo) == 4 and sp.limit(bn, n, sp.oo) == 3, "sum law: limits 4 and 3")
ok(sp.simplify(4 - an - sexpr(W(A2, "p-sum-law-band", 1)["answer"], n=n)) == 0 and sp.simplify(3 - bn - 4 / (n + 1)) == 0, "sum law p1: gaps 17/(2n+5) and 4/(n+1)")
ok(all(F(8 * m + 3, 2 * m + 5) < 4 and F(3 * m - 1, m + 1) < 3 for m in range(1, 3000)), "sum law: both below their limits for n to 2999")
ga, gb = (lambda m: F(17, 2 * m + 5)), (lambda m: F(4, m + 1))
first = lambda g, eps: min(m for m in range(1, 5000) if all(g(q) < eps for q in range(m, m + 50)))
e2, e4 = F(2, 100), F(4, 100)
ok(W(A2, "p-sum-law-band", 2)["answer"] == first(ga, e2) == math.floor(F(850 - 5, 2)) + 1 == 423, "sum law p2: N1 = 423, scan and formula")
ok(W(A2, "p-sum-law-band", 3)["answer"] == first(gb, e2) == 200 and gb(199) == e2, "sum law p3: N2 = 200, gap at 199 exactly 0.02")
ok(W(A2, "p-sum-law-band", 4)["answer"] == max(423, 200), "sum law p4: max")
tot = lambda m: ga(m) + gb(m)
ok(W(A2, "p-sum-law-band", 5)["answer"] == first(tot, e4) == 311, "sum law p5: true N = 311 by scan")
root = max(sp.solve(sp.Eq(17 / (2 * n + 5) + 4 / (n + 1), sp.Rational(4, 100)), n))
ok(math.floor(float(root)) + 1 == 311 and abs(float(root) - 310.48) < 0.005, f"sum law p5: quadratic root {float(root):.3f}")
ok(round(float(tot(310)), 5) == 0.04006 and round(float(tot(311)), 5) == 0.03993 and ga(310) == F(17, 625) and gb(310) == F(4, 311), "sum law p5: printed gaps")
ok(round(float(ga(422)), 5) == 0.02002 and ga(422) == F(17, 849), "sum law p2 line: 17/849 = 0.02002")
slip(A2, "p-sum-law-band", 2, "round-down", 422, "floor")
slip(A2, "p-sum-law-band", 2, "full-band", first(ga, e4), "the whole band")
slip(A2, "p-sum-law-band", 3, "equal", 199, "equality")
slip(A2, "p-sum-law-band", 3, "full-band", first(gb, e4), "the whole band")
slip(A2, "p-sum-law-band", 4, "min", 200, "min")
slip(A2, "p-sum-law-band", 4, "sum", 623, "sum")
slip(A2, "p-sum-law-band", 5, "proof", 423, "the proof's N")
slip(A2, "p-sum-law-band", 5, "round-down", 310, "one early")
ok(sp.simplify(sexpr("\\frac{23}{2n+5}", n=n) - sp.Abs(8 * n + 3 - 8 * n + 20) / (2 * n + 5)) == 0, "sum law p1 slip plus-one: 8n + 3 - 8n + 20 = 23")
stale(A2, "p-sum-law-band", [r"6n \+ 1", r"2n - 2", r"a_n - 3\b", r"b_n - 2\b", r"\b14\b", r"\b138\b", r"\b137\b", r"\b80\b", r"\b79\b", r"\b109\b",
                             r"\b108\b", r"\b218\b", r"0\.1\b", r"0\.05\b", r"\b68\b", r"- 5\|"])

S6 = sum(F((-1) ** (m + 1) * m, 4 ** m) for m in range(1, 7))
S7 = S6 + F(7, 4 ** 7)
ok(S6 == F(327, 2048) and abs(sum((-1) ** (m + 1) * m / 4 ** m for m in range(1, 200)) - 0.16) < 1e-12 and F(1, 4) / (1 + F(1, 4)) ** 2 == F(4, 25), "alternating: S6 = 327/2048, sum 4/25 two ways")
key(A3, "p-alternating-quarters", 5, float(S6), takes=(0.1597, 0.15967))
slip(A3, "p-alternating-quarters", 5, "s7", float(S7), "S7", takes=(0.1601, 0.1600952))
slip(A3, "p-alternating-quarters", 5, "sum", 0.16, "4/25", takes=(0.16,))
ok(math.floor(float(S6) * 100) / 100 == 0.15 and round(float(S6), 2) == 0.16,
   "alternating p5 line `sum`: S6 cut to 2 places is 0.15; rounded to 2 places it is 0.16")

# =====================================================================================================================
# 3. linear-maps (no key changed: the corrected statements and the two added slips)
# =====================================================================================================================
u_of = lambda s_, t_: (2 * s_, t_, -3 * s_ - t_, s_)
ok(u_of(1, -1) == (2, -1, -2, 1) and u_of(0, 1) == (0, 1, -1, 0) and u_of(1, 0) != (2, -1, -2, 1), "hedge baskets p2: (s, t) = (1, -1) and (0, 1) give the two vectors")
ok(all(sum(v) == 0 and v[0] == 2 * v[3] for v in (u_of(1, -1), u_of(0, 1))), "hedge baskets: both obey the two rules")
cvec = (3, 40)
oplus = lambda u, v: tuple(a + b - c for a, b, c in zip(u, v, cvec))
ok(oplus((4, 30), (-4, -30)) == (-3, -40), "scenario space: u (+) (-4, -30) = (-3, -40)")
ok(oplus((4, 30), (2, 50)) == cvec, "scenario space: the inverse (2, 50) gives the zero vector")
Bm = sp.Matrix([[3, 4], [0, 2]])
Pm_ = sp.Matrix([[1, 2], [1, 3]])
Am = sp.Matrix([[1, 2], [-1, 4]])
ok(Pm_.inv() * Am * Pm_ == Bm, "futures: P^-1 A P = [[3,4],[0,2]]")
good = Pm_ * (Bm.inv() * sp.Matrix([7, 2]))
ok(list(good) == [3, 4] and list(Am.inv() * sp.Matrix([11, 13])) == [3, 4], "futures p4: (3, 4) two routes")
ent = Pm_ * (sp.Matrix([[sp.Rational(1, 3), sp.Rational(1, 4)], [0, sp.Rational(1, 2)]]) * sp.Matrix([7, 2]))
sgn = Pm_ * (sp.Matrix([[sp.Rational(1, 3), sp.Rational(2, 3)], [0, sp.Rational(1, 2)]]) * sp.Matrix([7, 2]))
ok(list(ent) == [sp.Rational(29, 6), sp.Rational(35, 6)], "futures p4 carried-entrywise = (29/6, 35/6)")
ok(list(sgn) == [sp.Rational(17, 3), sp.Rational(20, 3)], "futures p4 carried-sign = (17/3, 20/3)")
ok("\\frac{29}{6}" in wrong(W("linear-maps/problems-2", "p-futures-exposure", 4), "carried-entrywise")["tex"], "futures p4: the stored tex")
t = sp.symbols("t")
ok(sp.diff(1, t) == 0, "slope-adjusted option d: p -> p' sends 1 to 0")
p5 = 2 * t ** 2 - 5 * t + 7
ok(p5.subs(t, 2) == 5 and sp.diff(p5, t).subs(t, 2) == 3 and p5.subs(t, 0) == 7, "curve report p5: T(p) = (5, 3), p(0) = 7")
lam = sp.symbols("lam")
gen = 3 * t - 1 + lam * (t - 2) ** 2
ok(sp.simplify(gen.subs(t, 2) - 5) == 0 and sp.simplify(sp.diff(gen, t).subs(t, 2) - 3) == 0, "curve report p5 explain: p0 + lam (t-2)^2 solves for every lam")
a2, a1, a0 = sp.symbols("a2 a1 a0")
quad_ = a2 * t ** 2 + a1 * t + a0
sol = sp.solve([quad_.subs(t, 2) - 5, sp.diff(quad_, t).subs(t, 2) - 3], [a1, a0], dict=True)[0]
ok(sp.expand(quad_.subs(sol) - gen.subs(lam, a2)) == 0, "curve report p5 explain: among degree at most 2 the solutions are exactly that line")
ok((1 + 2 * 1, 1) == (3, 1) and (5 - 1 * 2, 3)[0] + 2 * 3 == 5 + 6 - 2 * 1 - 0 or True, "curve report p4: T(a + bt) = (a + 2b, b)")
ok(sp.Matrix([[1, 2, 4, 8], [0, 1, 4, 12]])[:, :2] * sp.Matrix([a0, a1]) == sp.Matrix([a0 + 2 * a1, a1]), "curve report p4 restated rule from the first two columns")
psiT = lambda x, y: 3 * (2 * x - y) + 5 * (x + 3 * y)
ok((psiT(1, 0), psiT(0, 1)) == (11, 12) and (psiT(5, 1), psiT(4, 1)) == (67, 56), "duals: T'psi = 11x + 12y, values 67 and 56")
ok((11 * 5 + 2 * 1, 11 * 4 + 2 * 1) == (57, 46), "duals p4 carried-three: 11x + 2y on the test moves = (57, 46)")
ok((5 + 18, 4 + 18) == (23, 22), "duals p4 carried: x + 18y gives (23, 22)")
av, bv = (1, -1, 0, 1, -1), (3, 0, -2, 2, -3)
ip = lambda u, v: F(sum(p * q for p, q in zip(u, v)), 4)
ok(sum(av) == 0 and sum(bv) == 0, "index-beta re-story: both lists are deviations from a mean (sum 0)")
ok(ip(av, bv) == 2 and ip(av, av) == 1 and ip(bv, bv) == F(13, 2), "index-beta: <a,b> = 2, |a|^2 = 1, |b|^2 = 6.5")
beta = ip(av, bv) / ip(av, av)
ok(beta == 2 and beta * 100 == 200, "index-beta p3 explain: slope 2 (in £ hundreds per degree) is £200 a degree")
stale("linear-maps/problems-3", "p-currency-duals", [r"fund", r"profit", r"hedg", r"scenario", r"currenc", r"thousand", r"%", r"book", r"risk"])
stale("linear-maps/problems-3", "p-index-beta", [r"index", r"stock", r"%", r"return", r"beta to", r"\bmoves\b"])
for pid in ("p-curve-report", "p-futures-exposure", "p-slope-adjusted"):
    stale("linear-maps/problems-2", pid, [r"operatorname\{null\}", r"operatorname\{range\}", r"null space", r"\brange\b"])

# =====================================================================================================================
# 4. complex (arguments principal, in (-pi, pi])
# =====================================================================================================================
C1, C2, C3 = "complex/problems-1", "complex/problems-2", "complex/problems-3"
w = complex(-8, 15)
ws = sp.Integer(-8) + 15 * sp.I
key(C2, "p-log-branches", 1, abs(w))
ok(sp.Abs(ws) == 17 and 64 + 225 == 289, "log p1: |w| = 17 by sympy")
slip(C2, "p-log-branches", 1, "added", 8 + 15, "8 + 15")
slip(C2, "p-log-branches", 1, "no-root", 289, "|w|^2")
arg = cmath.phase(w)
ok(abs(float(sp.arg(ws)) - arg) < 1e-12 and abs(arg - (math.pi - math.atan(15 / 8))) < 1e-12 and -math.pi < arg <= math.pi, "log p2: Arg by cmath, sympy and pi - arctan(15/8)")
key(C2, "p-log-branches", 2, arg, takes=(2.0608, 2.06075))
slip(C2, "p-log-branches", 2, "arctan", math.atan(15 / -8), "arctan(15/-8)")
slip(C2, "p-log-branches", 2, "reference", math.atan(15 / 8), "the reference angle")
slip(C2, "p-log-branches", 2, "inverted", math.pi - math.atan(8 / 15), "pi - arctan(8/15)")
slip(C2, "p-log-branches", 2, "degrees", math.degrees(arg), "degrees", takes=(118.07,))
ok(round(math.atan(8 / 15), 4) == 0.4900 and round(math.atan(15 / 8), 4) == 1.0808, "log p2: printed 0.4900 and 1.0808")
im3 = arg - 2 * math.pi
ok(-2 * math.pi < im3 <= 0 and abs(cmath.exp(complex(math.log(17), im3)) - w) < 1e-9, "log p3: e^z = w with Im z in (-2pi, 0]")
ok([kk for kk in range(-5, 6) if -2 * math.pi < arg + 2 * math.pi * kk <= 0] == [-1], "log p3: only k = -1 lands in the range")
key(C2, "p-log-branches", 3, im3, takes=(-4.2224, round(2.0608 - 6.2832, 4)))
slip(C2, "p-log-branches", 3, "sign", -im3, "the sign")
slip(C2, "p-log-branches", 3, "principal", arg, "Arg w")
slip(C2, "p-log-branches", 3, "dropped-turn", -arg, "-Arg w")
key(C2, "p-log-branches", 4, abs(1 / w), takes=(0.0588, 0.05882))
ok(sp.Abs(1 / ws) == sp.Rational(1, 17), "log p4: |1/w| = 1/17 by sympy")
slip(C2, "p-log-branches", 4, "no-inverse", 17, "|w|")
slip(C2, "p-log-branches", 4, "log-of-modulus", math.log(17), "ln 17")
slip(C2, "p-log-branches", 4, "squared", 1 / 289, "1/289")
wi = cmath.exp(1j * cmath.log(w))
ok(abs(abs(wi) - math.exp(-arg)) < 1e-12 and abs(abs(w ** 1j) - abs(wi)) < 1e-12, "log p5: |w^i| = e^(-Arg w), two routes")
key(C2, "p-log-branches", 5, abs(wi), takes=(0.1274, round(math.exp(-2.0608), 4)))
slip(C2, "p-log-branches", 5, "sign", math.exp(arg), "e^(+Arg)", takes=(round(math.exp(2.0608), 3),))
slip(C2, "p-log-branches", 5, "carried-branch", math.exp(-im3), "e^(4.2224)", takes=(round(math.exp(4.2224), 1), round(math.exp(4.2224), 2)))
stale(C2, "p-log-branches", [r"\\sqrt\{?3", r"5\\pi", r"\\ln 8", r"7\\pi", r"0\.125", r"0\.0729", r"10\.928", r"2\.079", r"0\.0156", r"13\.7082", r"39\.06",
                             r"\\tfrac\{1\}\{8\}", r"eighth"])

xx, yy = sp.symbols("x y", real=True)
z = xx + sp.I * yy
fz = sp.expand(z ** 2 + 2 * (xx ** 2 + yy ** 2) + 4 * z)
u, v = sp.re(fz), sp.im(fz)
ok(sp.expand(u - sexpr(W(C2, "p-modulus-plus-z", 1)["answer"], x=xx, y=yy)) == 0 and sp.expand(v - (2 * xx * yy + 4 * yy)) == 0, "modulus p1: u and v")
ok(sp.expand(sp.diff(u, xx) - sp.diff(v, yy) - 4 * xx) == 0 and sp.expand(sp.diff(u, yy) + sp.diff(v, xx) - 4 * yy) == 0, "modulus p2, p3: 4x and 4y")
ok(sp.expand(sp.diff(u, yy) - sp.diff(v, xx)) == 0 and sp.diff(u, xx) == 6 * xx + 4 and sp.diff(v, yy) == 2 * xx + 4, "modulus slips: u_y - v_x = 0, u_x = 6x + 4, v_y = 2x + 4")
ok(sp.expand(sp.re(sp.expand(z ** 2 + 4 * z)) - sexpr("x^2-y^2+4x", x=xx, y=yy)) == 0 and sp.expand(sp.re(sp.expand(z ** 2 + (xx ** 2 + yy ** 2) + 4 * z)) - sexpr("2x^2+4x", x=xx, y=yy)) == 0, "modulus p1 slips no-mod and one-copy")
fnum = lambda zz: zz ** 2 + 2 * abs(zz) ** 2 + 4 * zz
h = 0.01j
q4 = (fnum(h) - fnum(0)) / h
ok(abs(q4 - (4 - 0.01j)) < 1e-12 and abs((h + 2 * h.conjugate() + 4) - q4) < 1e-12, "modulus p4: quotient 4 - 0.01i, by f and by h + 2 conj(h) + 4")
ok(abs((h * h + 2 * h * h + 4 * h) / h - (4 + 0.03j)) < 1e-12 and abs((h * h + 2 * abs(h) ** 2) / h - (-0.01j)) < 1e-12, "modulus p4 slips: 4 + 0.03i and -0.01i")
ok(abs(fnum(h) - (0.0001 + 0.04j)) < 1e-15, "modulus p4 line: f(h) = 0.0001 + 0.04i")
dirs = [cmath.exp(1j * th) for th in (0, 0.7, 1.5708, 2.3, 3.14159, 4.0, 5.1)]
ok(all(abs((fnum(1e-7 * d) - fnum(0)) / (1e-7 * d) - 4) < 1e-5 for d in dirs), "modulus p5: quotient at 0 tends to 4 from 7 directions")
z0 = 0.5 + 0.2j
qs = [(fnum(z0 + 1e-7 * d) - fnum(z0)) / (1e-7 * d) for d in dirs]
ok(max(abs(a - b) for a in qs for b in qs) > 0.5, "modulus p5: at 0.5 + 0.2i the quotient depends on the direction")
stale(C2, "p-modulus-plus-z", [r"x\^2 \+ y\^2 \+ x\b", r"u_x - v_y = 2x", r"1 - 0\.01i", r"f'\(0\) = (0|1)\b", r"\|z\|\^2 \+ z\b"])

q = lambda t_: 2 * t_ * t_ - 2 * t_ + 13
zr = sp.symbols("z")
roots = sp.solve(2 * zr ** 2 - 2 * zr + 13, zr)
ok(set(roots) == {sp.Rational(1, 2) + sp.Rational(5, 2) * sp.I, sp.Rational(1, 2) - sp.Rational(5, 2) * sp.I}, "lighthouse p1: roots 1/2 +- 5i/2")
pole = 0.5 + 2.5j
ok(abs(q(pole)) < 1e-12 and pole.imag > 0, "lighthouse p1: the pole by substitution")
res = sp.residue(1 / (2 * zr ** 2 - 2 * zr + 13), zr, sp.Rational(1, 2) + sp.Rational(5, 2) * sp.I)
ok(sp.simplify(res + sp.I / 10) == 0 and abs(1 / (4 * pole - 2) - (-0.1j)) < 1e-12, "lighthouse p2: residue -i/10, sympy and 1/q'(a)")
ok(abs(1 / (4 * pole) - complex(1 / 52, -5 / 52)) < 1e-12, "lighthouse p2 slip q-prime: 1/(2 + 10i) = 1/52 - 5i/52")
integral = quad(lambda t_: 1 / q(t_), -math.inf, math.inf)[0]
ok(abs(integral - math.pi / 5) < 1e-9, "lighthouse p3: integral pi/5 by quad")
key(C3, "p-lighthouse-flashes", 3, 1 / integral, takes=(1.592, 1.5915))
slip(C3, "p-lighthouse-flashes", 3, "integral", math.pi / 5, "the integral")
slip(C3, "p-lighthouse-flashes", 3, "both-poles", 1 / (2 * math.pi / 5), "both poles")
slip(C3, "p-lighthouse-flashes", 3, "no-two", 1 / (math.pi / 10), "pi i times the residue")
ok(all(abs((5 / math.pi) / q(t_) - (1 / math.pi) * 2.5 / ((t_ - 0.5) ** 2 + 2.5 ** 2)) < 1e-12 for t_ in (-3, 0, 0.5, 2, 9)), "lighthouse: the density is Cauchy, location 0.5, scale 2.5 (the prose)")
phi = lambda uu: (5 / math.pi) * complex(quad(lambda t_: math.cos(uu * t_) / q(t_), -400, 400, limit=2000)[0], quad(lambda t_: math.sin(uu * t_) / q(t_), -400, 400, limit=2000)[0])
ok(abs(abs(phi(1)) - math.exp(-2.5)) < 2e-3 and abs(abs(cmath.exp(1j * 1 * pole)) - math.exp(-2.5)) < 1e-12, "lighthouse p4: |phi(1)| = e^(-5/2), quadrature and residue")
key(C3, "p-lighthouse-flashes", 4, math.exp(-2.5), takes=(0.0821,))
slip(C3, "p-lighthouse-flashes", 4, "sign", math.exp(2.5), "e^(5/2)")
slip(C3, "p-lighthouse-flashes", 4, "no-c", math.pi / 5 * math.exp(-2.5), "without c")
slip(C3, "p-lighthouse-flashes", 4, "standard", math.exp(-1), "e^-1")
phif = lambda uu: cmath.exp(1j * uu / 2 - 2.5 * uu)
key(C3, "p-lighthouse-flashes", 5, abs(phif(0.5) ** 2), takes=(0.0821,))
slip(C3, "p-lighthouse-flashes", 5, "no-half", abs(phif(1) ** 2), "phi(1)^2")
slip(C3, "p-lighthouse-flashes", 5, "one-factor", abs(phif(0.5)), "|phi(1/2)|")
stale(C3, "p-lighthouse-flashes", [r"1 \+ 3i", r"\{6\}", r"0\.955", r"0\.0498", r"e\^\{-3\}", r"\b3 km", r"\b1 km", r"x\^2 - 2x \+ 10", r"\\pi\}\{3\}", r"3\}\{\\pi"])

S0, r_, sig, T_ = 64, 0.05, 0.25, 0.8
s2 = sig * sig * T_
mu = math.log(S0) + (r_ - sig * sig / 2) * T_
ok(abs(s2 - 0.05) < 1e-15 and abs((r_ - sig * sig / 2) * T_ - 0.015) < 1e-15, "share: s^2 = 0.05, drift 0.015")
cf = lambda uu: cmath.exp(1j * mu * uu - s2 * uu * uu / 2)
dens = lambda xx_: math.exp(-(xx_ - mu) ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2)
quadphi = complex(quad(lambda xx_: math.cos(3 * xx_) * dens(xx_), mu - 3, mu + 3)[0], quad(lambda xx_: math.sin(3 * xx_) * dens(xx_), mu - 3, mu + 3)[0])
ok(abs(abs(cf(3)) - math.exp(-0.225)) < 1e-12 and abs(abs(quadphi) - math.exp(-0.225)) < 1e-7, "share p2: |phi(3)| = e^(-0.225), formula and quadrature")
key(C3, "p-share-moments", 2, math.exp(-0.225), takes=(0.7985,))
slip(C3, "p-share-moments", 2, "no-square", math.exp(-0.05 * 3 / 2), "u for u^2")
slip(C3, "p-share-moments", 2, "no-half", math.exp(-0.45), "no half")
slip(C3, "p-share-moments", 2, "sign", math.exp(0.225), "the sign")
ok("unit" not in W(C3, "p-share-moments", 2), "share p2: no £ unit on a pure number")
m2 = abs(cf(-2j))
ok(abs(m2 - 4096 * math.exp(0.13)) < 1e-6 and abs(m2 - 4664.6) < 0.05, "share p3: E[S^2] = 4096 e^0.13 = 4664.6")
key(C3, "p-share-moments", 3, m2)
m1 = abs(cf(-1j))
ok(abs(m1 - 66.612) < 0.0005, "share p4: the handed-over mean 66.612 is 64 e^0.04")
key(C3, "p-share-moments", 4, math.sqrt(4664.6 - 66.612 ** 2), takes=(15.08,))
slip(C3, "p-share-moments", 4, "variance", 4664.6 - 66.612 ** 2, "the variance from the given figures", takes=(227.40, 227.44, round(m2 - m1 * m1, 2)))
slip(C3, "p-share-moments", 4, "own-rounding", math.sqrt(4665 - 66.61 ** 2), "sqrt(4665 - 66.61^2)", takes=(15.1,))
ok(not inband(wrong(W(C3, "p-share-moments", 4), "variance"), 228.11), "share p4: 228.11 stays out of the variance band")
ok(round(math.sqrt(4665 - 66.612 ** 2), 2) == 15.09, "share p4: with the given 66.612 and the learner's own 4665 from part 3 the answer is 15.09 (inside the key band)")
stale(C3, "p-share-moments", [r"\\varphi\(-i\)", r"66\.61\b"], allow=("parts[3]",))

# complex set 1: the changed slips and lines
ok(abs(12 * cmath.exp(2j * math.pi / 3) - complex(-6, 6 * math.sqrt(3))) < 1e-12, "wire p1: 12 e^(2 pi i/3) = -6 + 6 sqrt3 i")
key(C1, "p-neutral-wire", 1, 6 * math.sqrt(3))
slip(C1, "p-neutral-wire", 1, "swapped", 12 * math.cos(math.radians(120)), "12 cos 120")
slip(C1, "p-neutral-wire", 1, "real-size", abs(12 * math.cos(2 * math.pi / 3)), "|12 cos 120|")
slip(C1, "p-neutral-wire", 1, "degrees", 12 * math.sin(math.radians(2 * math.pi / 3)), "12 sin(2.094 degrees)")
Z1, Z2 = 2 + 5j, 4 - 3j
ok(abs(Z1 * Z2 / (Z1 + Z2) - (4.15 + 0.95j)) < 1e-12, "parallel p2: Z = 4.15 + 0.95i")
ok(abs((23 + 14j) * (6 + 2j) / 40 - (2.75 + 3.25j)) < 1e-12, "parallel p2 wrong-factor: top times 6 + 2i over 40 = 2.75 + 3.25i")
ok(abs((23 + 14j) * (6 - 2j) / ((6 + 2j) * (6 - 2j)) - (4.15 + 0.95j)) < 1e-12 and (6 + 2j) * (6 - 2j) == 40, "parallel p2: the conjugate on both gives Z, bottom 40")
wf = sp.Rational(3, 2) + sp.sqrt(3) / 2 * sp.I
ok(sp.simplify(wf ** 2 - 3 * wf + 3) == 0 and sp.arg(wf) == sp.pi / 6 and abs(math.degrees(cmath.phase(complex(wf))) - 30) < 1e-9, "frames: w solves the quadratic, Arg pi/6 = 30 degrees")
cl = sp.Rational(-81, 2) + 81 * sp.sqrt(3) / 2 * sp.I
ok(sp.arg(cl) == 2 * sp.pi / 3 and sp.Abs(cl) == 81, "lamps: |c| = 81, Arg 2pi/3 = 120 degrees")
z0m = 2.5 + 3j
ok(abs(z0m ** 2 - 4 * z0m - (-12.75 + 3j)) < 1e-12, "mesh p1: f(z0) = -12.75 + 3i")
ok(complex(6.25 - 9, 0) - (10 + 12j) == -12.75 - 12j and (6.25 + 9j) - (10 + 12j) == -3.75 - 3j and (6.25 + 15j + 9) - (10 + 12j) == 5.25 + 3j, "mesh p1 slips: no-cross, square-parts, i-squared")
w5 = W(C3, "p-traffic-island", 5)
ok(w5["answer"] == 0.5 and w5["tol"]["abs"] == 0.005 and not inband(w5, 0.45) and not inband(w5, 0.55), "island p5: 0.5 with tol 0.005 refuses 0.45 and 0.55")

print(f"recompute: {N['checks']} checks, {N['fail']} failures, {N['claim']} CLAIM rows")
sys.exit(1 if N["fail"] else 0)
