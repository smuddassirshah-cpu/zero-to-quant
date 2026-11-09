"""Reader checks for options L2 `h-strategy-card` (review-perf-retrofit-10): every expect recomputed by a second
route (exact Fractions, piecewise-linear analysis, plus a dense grid for best and worst), a reader solution written
independently, reader-planted slips, the shipped solution and the starter run on every example and hidden test
through harness10 (code.js compare rules, with each case's tol). Run from this folder with the venv Python, -I.
Exits 1 on any mismatch."""
import sys, os, random, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness10 import item, summary

bad = 0


def check(name, ok, info=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    bad += 0 if ok else 1


def expect(widget, src, label, want, which="tests"):
    global bad
    fails, r = summary(widget, src, label, which)
    if want is not None and fails != want:
        bad += 1
        print("     MISMATCH: wanted", want, "got", fails, [x[1][:60] for x in r])
    return fails


it = item("options", "homework-2.json", "h-strategy-card")
w = it["widget"]
print("options L2 h-strategy-card")


# ---------- route 2: exact rationals ----------
def card_exact(legs):
    L = [(k, F(q), F(str(s)), F(str(p))) for k, q, s, p in legs]

    def prof(S):
        t = F(0)
        for k, q, s, p in L:
            if k == "call":
                t += q * (max(S - s, 0) - p)
            elif k == "put":
                t += q * (max(s - S, 0) - p)
            else:
                t += q * (S - s)
        return t

    cost = sum(q * (s if k == "stock" else p) for k, q, s, p in L)
    knots = sorted({F(0)} | {s for k, q, s, p in L if k != "stock"})
    slope_top = prof(knots[-1] + 1) - prof(knots[-1])
    vals = [prof(x) for x in knots]
    best = math.inf if slope_top > 0 else max(vals)
    worst = -math.inf if slope_top < 0 else min(vals)
    roots = set()
    for a, b in zip(knots, knots[1:]):
        pa, pb = prof(a), prof(b)
        if pa == 0:
            roots.add(a)
        if pb == 0:
            roots.add(b)
        if pa * pb < 0:
            roots.add(a + (b - a) * pa / (pa - pb))
    if vals[-1] == 0:
        roots.add(knots[-1])
    if slope_top != 0 and vals[-1] * slope_top < 0:
        roots.add(knots[-1] - vals[-1] / slope_top)
    return {"cost": cost, "best": best, "worst": worst, "breakevens": sorted(roots)}, prof


def grid_extremes(prof, top):
    xs = [F(i, 4) for i in range(0, int(top * 4) + 4 * 50)]
    v = [prof(x) for x in xs]
    return max(v), min(v)


inf = math.inf
for i, c in enumerate(w["tests"]):
    legs = eval(c["call"][len("strategy_card("):-1])
    want = eval(c["expect"], {"float": float})
    got, prof = card_exact(legs)
    def eq(a, b):
        a = float(a)
        return a == b or math.isclose(a, b, abs_tol=1e-12)
    ok = eq(got["cost"], want["cost"]) and eq(got["best"], want["best"]) and eq(got["worst"], want["worst"])
    ok = ok and len(got["breakevens"]) == len(want["breakevens"]) and all(eq(a, b) for a, b in zip(got["breakevens"], want["breakevens"]))
    top = max([float(s) for k, q, s, p in legs] + [0])
    gmax, gmin = grid_extremes(prof, top)
    if want["best"] != inf:
        ok = ok and gmax == got["best"]
    else:
        ok = ok and prof(F(10 ** 6)) > prof(F(10 ** 5))
    if want["worst"] != -inf:
        ok = ok and gmin == got["worst"]
    else:
        ok = ok and prof(F(10 ** 6)) < prof(F(10 ** 5))
    ok = ok and all(prof(r) == 0 for r in got["breakevens"])
    check(f"test {i + 1} expect by exact rationals and a quarter-pound grid", ok, f"{got['breakevens']}")

# the examples are tests 1 and 2
check("examples are hidden tests 1 and 2", w["examples"][0]["call"] == w["tests"][0]["call"] and w["examples"][1]["call"] == w["tests"][1]["call"])
check("12 tests, 2 examples", len(w["tests"]) == 12 and len(w["examples"]) == 2)

# ---------- shipped solution and starter ----------
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution on the examples", [], "examples")
fails = expect(w, w["starter"], "starter", None)
check("starter fails every test", len(fails) == 12)

# ---------- reader solution, written from the prose ----------
READER = '''
def strategy_card(legs):
    def pnl(S):
        out = 0.0
        for kind, qty, k, prem in legs:
            if kind == "call":
                pay = max(S - k, 0.0)
            elif kind == "put":
                pay = max(k - S, 0.0)
            else:
                out += qty * (S - k)
                continue
            out += qty * (pay - prem)
        return out
    cost = sum(qty * (k if kind == "stock" else prem) for kind, qty, k, prem in legs)
    xs = sorted(set([0.0] + [float(k) for kind, qty, k, prem in legs if kind != "stock"]))
    ys = [pnl(x) for x in xs]
    up = pnl(xs[-1] + 1.0) - ys[-1]
    best = max(ys) if up <= 1e-12 else float("inf")
    worst = min(ys) if up >= -1e-12 else float("-inf")
    found = []
    def add(x):
        if not any(abs(x - y) < 1e-9 for y in found):
            found.append(x)
    for i, x in enumerate(xs):
        if abs(ys[i]) < 1e-9:
            add(x)
        if i + 1 < len(xs) and ys[i] * ys[i + 1] < 0:
            add(x - ys[i] * (xs[i + 1] - x) / (ys[i + 1] - ys[i]))
    if abs(up) > 1e-12 and ys[-1] * up < 0 and abs(ys[-1]) >= 1e-9:
        add(xs[-1] - ys[-1] / up)
    return {"cost": cost, "best": best, "worst": worst, "breakevens": sorted(found)}
'''
expect(w, READER, "reader solution", [])

# exact-equality variant (a reasonable learner choice): still passes, the tests' touches are exact in floats
EXACT_EQ = w["solution"].replace("zero = 1e-9", "zero = 1e-300")
expect(w, EXACT_EQ, "variant: exact zero test", [])

# ---------- reader-planted slips ----------
SLIPS = {
    # leaves out the £0 point: a put's best, a share's worst
    "no £0 point": w["solution"].replace("sorted({0.0} | {", "sorted(set() | {"),
    # slope counts puts as well
    "slope counts puts": w["solution"].replace('if kind != "put")', ')'),
    # cost leaves out shares
    "cost ignores shares": w["solution"].replace('cost += qty * (strike if kind == "stock" else premium)', 'cost += 0 if kind == "stock" else qty * premium'),
    # strict sign change only: misses a kink touch and an exact kink root
    "strict crossings only": w["solution"].replace("if abs(pa) < zero:\n            roots.append(a)\n        elif abs(pb) >= zero and", "if").replace("if abs(last) < zero:\n        roots.append(points[-1])\n    elif", "if").replace("(pa < 0) != (pb < 0)", "pa * pb < 0").replace("(last < 0) != (slope < 0)", "last * slope < 0"),
    # every zero-valued kink appended from both sides
    "kink root twice": w["solution"].replace("if abs(pa) < zero:\n            roots.append(a)\n        elif", "if abs(pa) < zero:\n            roots.append(a)\n        if abs(pb) < zero:\n            roots.append(b)\n        elif"),
    # no root past the top strike
    "no tail root": w["solution"].replace("elif slope != 0 and (last < 0) != (slope < 0):\n        roots.append(points[-1] - last / slope)", ""),
    # breakevens from a 1p grid
    "1p grid": w["solution"].replace('    return {"cost"', '    roots = [x / 100 for x in range(0, 40000) if abs(_profit(x / 100)) < 0.005]\n    return {"cost"'),
    # abs(qty) in the cost: short legs paid for
    "abs qty in cost": w["solution"].replace("cost += qty * (", "cost += abs(qty) * ("),
}
want = {"no £0 point": None, "slope counts puts": None, "cost ignores shares": [7, 8, 12], "strict crossings only": [9, 10],
        "kink root twice": [9, 10], "no tail root": None, "1p grid": None, "abs qty in cost": None}
for name, src in SLIPS.items():
    if src == w["solution"]:
        check(f"slip '{name}' differs from the solution", False)
        continue
    f = expect(w, src, "slip: " + name, want[name])
    check(f"slip '{name}' is caught", len(f) > 0, f"fails {f}")

# ---------- shipped against route 2 on random positions ----------
G = {}
exec(w["solution"], G)
R = {}
exec(READER, R)
random.seed(10)
mism = 0
for trial in range(3000):
    legs = []
    for _ in range(random.randint(1, 4)):
        k = random.choice(["call", "put", "call", "put", "stock"])
        q = random.choice([-3, -2, -1, 1, 2, 3])
        s = random.choice(range(60, 141, 5))
        p = 0 if k == "stock" else random.choice(range(25, 1500, 25)) / 100
        legs.append((k, q, s, p))
    ex, prof = card_exact(legs)
    knots = sorted({F(0)} | {F(str(s)) for k, q, s, p in legs if k != "stock"})
    if any(prof(a) == 0 and prof(b) == 0 for a, b in zip(knots, knots[1:])):
        continue  # a flat stretch at 0, excluded by the prose
    for fn in (G["strategy_card"], R["strategy_card"]):
        got = fn(legs)
        ok = math.isclose(got["cost"], float(ex["cost"]), abs_tol=1e-9)
        for key in ("best", "worst"):
            ok = ok and (got[key] == float(ex[key]) or math.isclose(got[key], float(ex[key]), abs_tol=1e-9))
        ok = ok and len(got["breakevens"]) == len(ex["breakevens"]) and all(math.isclose(a, float(b), abs_tol=1e-9) for a, b in zip(got["breakevens"], ex["breakevens"]))
        if not ok:
            mism += 1
            if mism < 4:
                print("     mismatch", legs, got, ex)
check("shipped and reader solutions against exact rationals on 3,000 random positions", mism == 0, f"{mism} mismatches")

print("failures:", bad)
sys.exit(1 if bad else 0)
