#!/usr/bin/env python3
"""Numbers of the fix of finding 1 (review-problems-odes-4.md): p-test-rig renumbered to
y'' + 6y' + 8y = 24e^{-8t}, y(0) = y'(0) = 0, read from proposed-p-test-rig.json beside this file.
Every key, slip and printed number of the replacement item is recomputed (sympy exact, then numerically).
With an output path it also writes a copy of problems-4.json with the item replaced, for the engine probe.

<scratchpad>/venv/bin/python docs/reviews/review-problems-odes-4-scripts/proposed.py [out.json]
"""
import json
import math
import os
import re
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = json.load(open(os.path.join(HERE, "proposed-p-test-rig.json")))
checks = fails = 0


def ok(c, m):
    global checks, fails
    checks += 1
    if not c:
        fails += 1
        print("FAIL", m)


S = sp.Symbol("s")
t = sp.Symbol("t", positive=True)


def tex(x):
    while "\\frac" in x:
        x = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", x)
    x = re.sub(r"e\^\{([^{}]*)\}", r"exp(\1)", x)
    x = re.sub(r"e\^\(([^()]*)\)", r"exp(\1)", x)
    x = x.replace("^", "**")
    x = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", x)
    x = re.sub(r"\)\(", ")*(", x)
    return sp.sympify(x, locals={"s": S, "t": t, "exp": sp.exp}, rational=True)


eq = lambda a, b: sp.simplify(a - b) == 0
W = lambda k: NEW["parts"][k - 1]["widget"]
wr = lambda k: {x["id"]: x for x in W(k)["wrong"]}
TXT = json.dumps(NEW, ensure_ascii=False).replace("\\\\", "\\")

force = 24 * sp.exp(-8 * t)
F = sp.laplace_transform(force, t, S, noconds=True)
ok(eq(F, 24 / (S + 8)) and eq(tex(W(1)["answer"]), F), "part 1: 24/(s+8)")
ok(eq(tex(wr(1)["sign"]["tex"]), 24 / (S - 8)) and eq(tex(wr(1)["no-factor"]["tex"]), 1 / (S + 8)), "part 1 slips")
Y = F / (S**2 + 6 * S + 8)
ok(eq(Y, 24 / ((S + 2) * (S + 4) * (S + 8))) and eq(tex(W(2)["answer"]), Y) and all(eq(tex(a), Y) for a in W(2)["accept"]), "part 2 key and accepts")
ok(eq(tex(wr(2)["carried-sign"]["tex"]), (24 / (S - 8)) / (S**2 + 6 * S + 8)) and eq(tex(wr(2)["root-signs"]["tex"]), 24 / ((S + 8) * (S - 2) * (S - 4))), "part 2 slips")
res = {p: sp.residue(Y, S, p) for p in (-2, -4, -8)}
ok(res == {-2: 2, -4: -3, -8: 1} and sum(res.values()) == 0, "residues 2, -3, 1; sum 0")
ok(W(3)["answer"] == -3 and wr(3)["sign"]["value"] == 3 and wr(3)["other-pole"]["value"] == 2, "part 3 key and slips")
ok(sp.Rational(24, (-4 + 2) * (-4 + 8)) == -3 and sp.Rational(24, 2 * 6) == 2 and sp.Rational(24, (-6) * (-4)) == 1, "cover-up sums as printed")
y = 2 * sp.exp(-2 * t) - 3 * sp.exp(-4 * t) + sp.exp(-8 * t)
ok(eq(sp.inverse_laplace_transform(Y, S, t).subs(sp.Heaviside(t), 1), y), "y by inverse transform")
ok(eq(sp.diff(y, t, 2) + 6 * sp.diff(y, t) + 8 * y, force) and y.subs(t, 0) == 0 and sp.diff(y, t).subs(t, 0) == 0, "y satisfies the equation and the starting values")
ok(eq(tex(W(4)["answer"]), y) and all(eq(tex(a), y) for a in W(4)["accept"]), "part 4 key and accepts")
ok(eq(tex(wr(4)["exp-sign"]["tex"]), y.subs(t, -t)) and eq(tex(wr(4)["carried-sign"]["tex"]), 2 * sp.exp(-2 * t) + 3 * sp.exp(-4 * t) + sp.exp(-8 * t)), "part 4 slips")
ok(tex(wr(4)["carried-sign"]["tex"]).subs(t, 0) == 6 and (2 - 3 + 1, -4 + 12 - 8) == (0, 0), "y(0) = 6 for the slip; printed checks")
u = sp.Symbol("u", positive=True)
yu = 2 * u - 3 * u**2 + u**4
ok(eq(y.subs(t, -sp.log(u) / 2), yu), "y = 2u - 3u^2 + u^4 with u = e^(-2t)")
ok(sp.expand(yu - u * (1 - u) ** 2 * (u + 2)) == 0, "y = u(1 - u)^2(u + 2), never negative on (0, 1]")
ok(sp.expand(sp.diff(yu, u) - 2 * (u - 1) * (2 * u**2 + 2 * u - 1)) == 0, "dy/du = 2(u - 1)(2u^2 + 2u - 1)")
roots = [r for r in sp.solve(2 * u**2 + 2 * u - 1, u) if 0 < r < 1]
ok(roots == [(sp.sqrt(3) - 1) / 2], "the root in (0, 1) is (sqrt 3 - 1)/2")
peak = sp.simplify(yu.subs(u, roots[0]))
ok(eq(peak, (6 * sp.sqrt(3) - 9) / 4), "peak (6 sqrt 3 - 9)/4")
tp = sp.log(1 + sp.sqrt(3)) / 2
ok(eq(sp.exp(-2 * tp), roots[0]), "peak time ln(1 + sqrt 3)/2")
g = np.linspace(0, 10, 2000001)
yg = 2 * np.exp(-2 * g) - 3 * np.exp(-4 * g) + np.exp(-8 * g)
ok(abs(yg.max() - float(peak)) < 1e-10 and abs(g[yg.argmax()] - float(tp)) < 1e-5 and yg.min() > -1e-15, "peak by grid; y never negative")
w5 = W(5)
ok(abs(w5["answer"] - float(peak)) <= 5e-5 and round(float(peak), 3) == 0.348, "part 5 key 0.3481, prints 0.348")
slips = {"u-value": float(roots[0]), "time": float(tp), "at-one": float(y.subs(t, 1))}
for i, x in wr(5).items():
    ok(abs(slips[i] - x["value"]) <= x["tol"]["abs"], f"part 5 wrong {i} = {slips[i]:.6f}")
    ok(abs(x["value"] - w5["answer"]) > x["tol"]["abs"] + w5["tol"]["abs"], f"part 5 wrong {i} clear of the key band")
ok(round(float(roots[0]), 4) == 0.3660 and round(float(tp), 4) == 0.5025, "0.3660 and 0.5025")
ok(round(float(tp), 3) == 0.503, "0.503 s as printed")
for p in NEW["parts"]:
    for x in p["widget"].get("wrong", []):
        ok(x["id"] in p["feedback"]["byKey"], f"wrong {x['id']} has a line")
# not a shift or scale of lesson 15's example: poles not equally spaced, residues not in the ratio 1 : -2 : 1
ok((-4) - (-8) != (-2) - (-4) and [res[-2], res[-4], res[-8]] != [res[-2], -2 * res[-2], res[-2]], "not l15's Y shifted and scaled")
print(f"{checks} checks, {fails} failures")
if len(sys.argv) > 1:
    doc = json.load(open("app/content/courses/odes/problems-4.json"))
    doc["items"][0] = NEW
    json.dump(doc, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)
sys.exit(1 if fails else 0)
