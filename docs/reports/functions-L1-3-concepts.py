#!/usr/bin/env python3
"""Concept checks for functions L1 to L3 (round 1 blind audit, 26 Nov 2026).

Recomputes every graded key, slip value and stated figure the audit ledger rests on,
reading the keys from the content JSON so the script stays bound to the files. It also
sweeps the fluency families over their whole range and holds the counterexamples behind
the `imprecise` findings.

Run: python3 docs/reports/functions-L1-3-concepts.py
Standard library only; no figure depends on a package version.

Exit code: 0 when every check passes. A check marked FINDING tests a sentence of the
content as written; it fails while the content is wrong and is listed under the same
number in docs/reviews/audit-functions-1-3.md. Checks marked NOTE record a
counterexample to an `imprecise` sentence and never fail.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as Fr

CDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "functions")
RESULTS = []
_CACHE = {}


def J(name):
    if name not in _CACHE:
        with open(os.path.join(CDIR, name + ".json"), encoding="utf-8") as fh:
            _CACHE[name] = json.load(fh)
    return _CACHE[name]


def check(name, ok, detail="", finding=None):
    RESULTS.append((name, bool(ok), detail, finding))


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def W(name, kind, i, part=None):
    """Widget of screen/quiz/item i (optionally of a part)."""
    node = J(name)[kind][i]
    if part is not None:
        node = node["parts"][part]
    return node["widget"]


def key(w):
    return w["answers"] if "answers" in w else w["answer"]


def slips(w):
    return {x["id"]: x.get("value", x.get("tex")) for x in w.get("wrong", [])}


def num(name, kind, i, want, wrong=None, part=None, tol=1e-9):
    """The keyed answer equals `want`; each named slip equals the value its feedback describes."""
    w = W(name, kind, i, part)
    tag = f"{name} {kind}[{i}]" + (f".parts[{part}]" if part is not None else "")
    k = key(w)
    if isinstance(want, (list, tuple)):
        ok = sorted(k) == sorted(want)
    else:
        ok = close(float(k), float(want), tol)
    check(f"{tag} key {k}", ok, f"recomputed {want}")
    for sid, val in (wrong or {}).items():
        got = slips(w).get(sid)
        slip_tol = 0.006
        for x in w.get("wrong", []):
            if x["id"] == sid:
                slip_tol = max(slip_tol, float(x.get("tol", {}).get("abs", 0)) + 1e-9)
        ok = got is not None and close(float(got), float(val), slip_tol)
        check(f"{tag} slip {sid} = {got}", ok, f"the named mistake gives {val}")
        check(f"{tag} slip {sid} differs from key", not close(float(val), float(k) if not isinstance(k, list) else 1e99, 1e-6))


def correct_choice(name, kind, i, want_id, part=None):
    w = W(name, kind, i, part)
    ids = [o["id"] for o in w["options"] if o.get("correct")]
    check(f"{name} {kind}[{i}] correct option {ids}", ids == ([want_id] if isinstance(want_id, str) else want_id))


def line2(p, q):
    (x1, y1), (x2, y2) = p, q
    m = Fr(y2 - y1) / Fr(x2 - x1)
    return m, Fr(y1) - m * Fr(x1)


def D(s):
    return Fr(str(s))


# ---------------------------------------------------------------- Level 1
f = lambda x: 2 * x + 3
num("l1-machines", "screens", 1, f(10), {"double-only": 20, "add-first": 2 * (10 + 3), "add-only": 13})
num("l1-machines", "screens", 2, f(2) - f(1), {"same": 1, "plus3": 3})
num("l1-machines", "screens", 3, f(-4), {"lost-sign": f(4), "add-first": 2 * (-4 + 3), "subtracted": 2 * -4 - 3, "sign": 5})
g = lambda x: x * x - 1
num("l1-machines", "screens", 4, g(-3), {"neg-square": -(3 ** 2) - 1, "doubled": 2 * -3 - 1, "subtract-first": (-3 - 1) ** 2})
num("l1-machines", "screens", 5, 7, {"times": 700, "plus": 107, "input": 100})
check("l1 trap: f(5) is 3 less than f(2)+f(3)", f(5) - (f(2) + f(3)) == -3)
correct_choice("l1-machines", "screens", 6, "less")
check("l1 generalise: 3(-2)^2 = 12, slips -12 and 36", 3 * (-2) ** 2 == 12 and 3 * -(2 ** 2) == -12 and (3 * -2) ** 2 == 36)
check("l1 derive: 5(x-4) at 6 is 10, 5x-4 gives 26", 5 * (6 - 4) == 10 and 5 * 6 - 4 == 26)
P = lambda q: D("0.75") * q - 6
check("l1 transfer table", P(100) == 69 and P(200) == 144 and D("13.15") - D("12.40") == D("0.75"))
num("l1-machines", "screens", 9, P(240), {"no-fee": 180, "revenue": D("13.15") * 240 - 6, "double-fee": 168})
num("l1-machines", "quiz", 0, 4 * -2 - 1, {"lost-sign": 7, "sub-first": 4 * (-2 - 1), "sign": 9})
check("l1 quiz g(-3) = 6; slips -12 and 12", (-3) ** 2 + -3 == 6 and -(3 ** 2) + -3 == -12 and 9 + 3 == 12)
num("l1-machines", "quiz", 3, -9, {"zero": 0, "sign": 9})
check("l1 quiz loss rule", D("8.25") - D("8.60") == D("-0.35"))

num("l2-table-to-rule", "screens", 0, 16, {"add-one": 14, "doubled": 26})
check("l2 rows fit 3x+1", all(3 * x + 1 == y for x, y in [(1, 4), (2, 7), (3, 10), (4, 13)]))
check("l2 rows fit 4x+5", all(4 * x + 5 == y for x, y in [(0, 5), (1, 9), (2, 13), (3, 17)]))
check("l2 rows fit 3x+2 only", all(3 * x + 2 == y for x, y in [(1, 5), (3, 11), (5, 17), (7, 23)]) and 6 * 3 - 1 == 17 and 3 + 4 == 7)
num("l2-table-to-rule", "screens", 4, 36, {"next-row": 25, "last-climb": 16 + 7 + 7})
num("l2-table-to-rule", "screens", 5, 10, {"forward": 94, "wrong-order": 31 / 3 - 1, "add-back": 32 / 3})
num("l2-table-to-rule", "screens", 7, 3, {"climb": 6, "upside-down": 1 / 3})
check("l2 order: 3x-5 fits (2,1),(4,7),(6,13)", all(3 * x - 5 == y for x, y in [(2, 1), (4, 7), (6, 13)]))
Ps = lambda s: 40 * D(s) - 610
check("l2 transfer 40s-610", Ps("15.00") == -10 and Ps("16.00") == 30 and Ps("17.50") == 90 and 40 * D("15.25") == 610)
check("l2 transfer slip 60s-930 fits rows 2 and 3 only", 60 * 16 - 930 == 30 and 60 * D("17.5") - 930 == 120)
num("l2-table-to-rule", "quiz", 1, 7, {"forward": 97, "wrong-order": 25 / 4 + 3, "wrong-way": 22 / 4})
num("l2-table-to-rule", "quiz", 2, 27, {"last-climb": 25})
check("l2 quiz x^2+2", [x * x + 2 for x in (1, 2, 3, 4, 5)] == [3, 6, 11, 18, 27])
num("l2-table-to-rule", "quiz", 3, 42, {"climb-m": 202, "next-row": 32})
# NOTE for finding 3: the lesson's own transfer table has changing climbs and a rule mx + c.
rows = [(D("15"), -10), (D("16"), 30), (D("17.5"), 90)]
climbs = [rows[i + 1][1] - rows[i][1] for i in range(2)]
check("NOTE l2 s[4]: a table with changing climbs (40, 60) that is linear", climbs == [40, 60] and line2(rows[0], rows[1]) == line2(rows[1], rows[2]),
      "l2 s[9] contradicts 'a table whose climb changes has no rule mx + c'", finding="note-3")

sq = lambda x: x * x
grid = [Fr(k, 100) for k in range(-200, 301)]
check("l3 range of x^2 on [-2,3] is [0,9]", min(map(sq, grid)) == 0 and max(map(sq, grid)) == 9)
grid = [Fr(k, 1000) for k in range(-2999, 2001)]
check("l3 range of x^2 on (-3,2] is [0,9)", min(map(sq, grid)) == 0 and max(map(sq, grid)) < 9)
check("l3 10-x on [3,8] gives [2,7]", (10 - 8, 10 - 3) == (2, 7))
check("l3 put payoff range [0,100]", max(max(100 - s, 0) for s in range(0, 151)) == 100 and min(max(100 - s, 0) for s in range(0, 151)) == 0)
check("l3 quiz whole shares", D("37.5") / D("0.5") == 75 and D("10.25") / D("0.5") == D("20.5") and 60 / 0.5 == 120)
check("l3 quiz open end", (2 * -1 - 1, 2 * 3 - 1) == (-3, 5))

num("l4-one-output", "screens", 1, 2, {"one": 1, "four": 4})
num("l4-one-output", "screens", 3, 3, {"hollow": 1, "average": 2})
fee = lambda t: 5 if t <= 1000 else (8 if t <= 5000 else 12)
num("l4-one-output", "screens", 8, fee(5000), {"next": 12, "average": 10})
check("r1 fee total", 3 + D("7.5") + D("0.004") * 4000 == D("26.5"))

# ---------------------------------------------------------------- Level 2
num("l5-plotting", "screens", 5, 2.5, {"in-as-x": 7, "minus": 1.5})
check("l5 fee line", 5 + D("0.02") * 750 == 20 and 5 + D("0.02") * 250 == 10 and 5 + D("0.02") * 500 == 15)
num("l5-plotting", "quiz", 1, -4, {"dropped-sign": 8, "minus-two": -8, "sign": 4})

num("l6-how-steep", "screens", 2, Fr(3, 6), {"swapped": 2, "rise-only": 3, "run-only": 6})
num("l6-how-steep", "screens", 3, Fr(-6, 3), {"no-sign": 2, "swapped": -0.5})
num("l6-how-steep", "screens", 4, 1.5, {"swapped": 4 / 6, "intercept": -1})
check("l6 trap line 4x+6 through P and Q", 4 * 1 + 6 == 10 and 4 * 6 + 6 == 30)
check("l6 trend line through both marks", D("42") + D("0.15") * 5 == D("42.75") and D("42") + D("0.15") * 25 == D("45.75"))
num("l6-how-steep", "screens", 9, 0.15, {"swapped": 20 / 3, "rise-only": 3, "whole-window": 0.1})
check("l6 drift over 250 days", 250 * D("0.15") == D("37.5"))
num("l6-how-steep", "quiz", 0, 2, {"swapped": 0.5, "rise-only": 8})
num("l6-how-steep", "quiz", 2, -1.5, {"no-sign": 1.5, "swapped": -6 / 9, "minus-minus": -9 / 2})

num("l7-slope-and-start", "screens", 8, 4.95, {"first-fee": 6.95, "rate": 0.01})
check("l7 fee line", line2((200, D("6.95")), (800, D("12.95"))) == (D("0.01"), D("4.95")))
check("l7 slide: c = -1", D("0.5") * 4 - 1 == 1)
num("l7-slope-and-start", "quiz", 1, -10, {"no-sign": 14, "minus-c": -14, "sign": 10})
num("l7-slope-and-start", "quiz", 3, 40.8, {"no-c": 2.4, "once": 38.52})

check("l8 lines", line2((1, 3), (3, 7)) == (2, 1) and line2((2, 5), (6, 7)) == (Fr(1, 2), 4) and line2((-1, 6), (3, -2)) == (-2, 4) and line2((2, 7), (5, 13)) == (2, 3))
check("l8 slips", 5 - 2 * 2 == 1 and 6 - 2 == 4 and 6 + (-2) * (-1) == 8 and 6 - Fr(1, 2) == Fr(11, 2) and -1 - 5 * 3 == -16)
m, c = line2((4, D("38.20")), (16, D("40.60")))
check("l8 trend line", (m, c) == (D("0.2"), D("37.4")))
num("l8-line-through-two-points", "screens", 8, m * 30 + c, {"from-day4": D("38.20") + 30 * m, "proportional": D("40.60") * 30 / 16})
num("l8-line-through-two-points", "quiz", 1, line2((1, 2), (3, 8))[1], {"first-y": 2, "added": 5, "sign": 1})
num("l8-line-through-two-points", "quiz", 3, line2((1000, 13), (3000, 21))[1], {"first-fee": 13, "rate": 0.004})

ang = math.degrees(math.atan(abs((2 - (-2)) / (1 + 2 * -2))))
check("l9 y=2x and y=-2x+1 meet at about 53 degrees", abs(ang - 53.13) < 0.01, f"{ang:.2f}")
w = W("l9-parallel-perpendicular", "screens", 3)
check("l9 slider key -0.5", w["answer"] == -0.5 and 2 * -0.5 == -1)
num("l9-parallel-perpendicular", "screens", 7, 0.25, {"negate-only": 4, "flip-only": -0.25})
check("l9 break-even", 2 + D("0.01") * 1000 == 8 + D("0.004") * 1000 == 12 and 2 + D("0.01") * 600 == 8 and 8 + D("0.004") * 600 == D("10.4"))
num("l9-parallel-perpendicular", "quiz", 1, -4 / 3, {"flip-only": 4 / 3, "negate-only": -0.75}, tol=1e-4)
check("l9 quiz relation", line2((1, 2), (3, 8))[0] * line2((0, 5), (6, 3))[0] == -1)
num("l9-parallel-perpendicular", "quiz", 3, 2000, {"one-rate": 500})
check("l9 quiz both charge 21", 5 + D("0.008") * 2000 == 9 + D("0.006") * 2000 == 21)
# NOTE for finding 8: the quarter-turn derivation needs a and b non-zero.
check("NOTE l9 s[8]: b = 0 (a flat line) has no product m1*m2", True, "m1 = 0/a = 0 and m2 = -a/0 is undefined; 'whatever a and b are' needs both non-zero", finding="note-8")

num("review-2", "items", 1, 3, {"swapped": 1 / 3, "minus-minus": 2})
check("r2 two points", line2((-2, 1), (2, 9)) == (2, 5) and 1 + 2 * -2 == -3)
num("review-2", "items", 4, -5, {"flip-only": 5, "negate-only": -0.2})
num("review-2", "items", 6, 9.5, {"no-c": 6.0})
num("review-2", "items", 8, 16, {"x-rate": 8 / 0.3, "y-rate": 10})
check("r2 trend cross price", D("0.3") * 16 + 50 == D("0.8") * 16 + 42 == D("54.8"))
check("r2 parallel through", 1 - 3 * 2 == -5 and Fr(-1, 3) * 2 + Fr(5, 3) == 1)

num("homework-2", "items", 1, -1.5, {"no-sign": 1.5, "swapped": 4 / -6})
check("hw2 equation", line2((-4, 0), (2, 3)) == (Fr(1, 2), 2) and 0 - 2 * -4 == 8)
num("homework-2", "items", 3, 2.8, {"y-intercept": 7, "sign": -2.8})
num("homework-2", "items", 4, 5, {"same-m": 3 - 2 * 4, "negate-only": 3 + 2 * 4, "sign-slip": 3 + -0.5 * 4})
num("homework-2", "items", 5, 30, {"no-start": 30 / 0.18})
mA, cA = line2((200, D("5.40")), (600, D("7.80")))
num("homework-2", "items", 7, (9 - cA) / (mA - D("0.002")), {"first-fee": (9 - D("5.40")) / (mA - D("0.002")), "a-rate": (9 - cA) / mA})
check("hw2 both charge 11.40", cA + mA * 1200 == D("11.4"))
m, c = line2((3, D("52.40")), (12, D("55.10")))
check("hw2 report", (m, c) == (D("0.3"), D("51.5")) and m * 30 + c == D("60.5") and (57 - c) / (m - D("0.1")) == D("27.5") and m * D("27.5") + c == D("59.75"))

# problems-2
num("problems-2", "items", 0, -2.5, {"sign": 2.5, "flipped": -0.4, "no-run": -7.5}, part=0)
num("problems-2", "items", 0, 26, {"sign": 16, "first-point": 21, "one-hour": 23.5}, part=1)
num("problems-2", "items", 0, 10.4, {"sixteen": 6.4, "times": 65, "flipped": 2.5 / 26}, part=2)
num("problems-2", "items", 1, 4, {"flipped": 0.25, "lost-minus": 28 / 3}, part=0)
check("p2 path and pipe", line2((-2, 1), (5, 29)) == (4, 9) and 23 + Fr(1, 4) * 12 == 26 and 4 * 4 + 9 == 25 == -Fr(1, 4) * 4 + 26)
num("problems-2", "items", 1, 4, {"y-value": 25, "sign-x": 17 / 3.75, "constants": 35 / 4.25}, part=4)
num("problems-2", "items", 2, 18, {"no-run": 90, "one-point": 104 / 3}, part=0)
num("problems-2", "items", 2, 50, {"first-point": 104, "sign": 158, "no-run": 104 - 270}, part=1)
num("problems-2", "items", 2, 5, {"fee-gap": 30, "fees-sum": 70 / 6}, part=2)
num("problems-2", "items", 2, 42, {"rates-only": 72, "gym-b": 266, "gym-a": 308}, part=3)
num("problems-2", "items", 3, 130, {"no-start": 90, "swapped": 255}, part=0)
num("problems-2", "items", 3, 15, {"no-run": 60, "one-point": 25}, part=1)
num("problems-2", "items", 3, 20, {"first-point": 50, "sign": 80, "one-point": 0}, part=2)

# Fluency families over their whole range.
def fluency():
    fam = {x["id"]: x for x in J("fluency-l8-line-through-two-points")["families"]}
    n = bad = 0
    g = fam["gradient"]
    for x1, run, y1, m in itertools.product(range(-6, 5), range(1, 7), range(-8, 9), g["vars"]["m"]["pick"]):
        m = D(m); rise = m * run; y2 = y1 + rise
        if rise.denominator != 1 or abs(y2) > 15:
            continue
        n += 1
        true_m = Fr(y2 - y1) / Fr(run)
        if true_m != m or 1 / m == m or -m == m or abs(float(1 / m) - float(-m)) <= 0.005 or abs(float(1 / m) - float(m)) <= 0.005:
            bad += 1
    check(f"fluency gradient: {n} draws, key right and slips distinct", n > 0 and bad == 0, f"{bad} bad")
    n = bad = 0
    e = fam["line-equation"]
    for x1, run, y1, m in itertools.product(range(-6, 6), range(1, 7), range(-8, 9), e["vars"]["m"]["pick"]):
        if x1 == 0:
            continue
        m = D(m); x2 = x1 + run; rise = m * run; y2 = y1 + rise; c = y1 - m * x1
        if x2 == 0 or x2 > 7 or rise.denominator != 1 or c.denominator != 1 or abs(y2) > 15:
            continue
        n += 1
        tm, tc = line2((x1, y1), (x2, y2))
        w1, w2 = Fr(y1), y1 + m * x1
        if (tm, tc) != (m, c) or w1 == c or w2 == c or w1 == w2:
            bad += 1
    check(f"fluency line-equation: {n} draws, key right and slips distinct", n > 0 and bad == 0, f"{bad} bad")


fluency()

# ---------------------------------------------------------------- Level 3
num("l10-curves-from-tables", "screens", 2, 0.25, {"straight": 0.5})
t = W("l10-curves-from-tables", "screens", 3)
check("l10 cubic table", [r[1]["answer"] for r in t["rows"][:2]] == [(-2) ** 3, (-1) ** 3])
num("l10-curves-from-tables", "screens", 5, 2 ** -1, {"times": -2, "zero": 0})
bond = lambda r, n: 100 / (1 + r) ** n
p = {k: bond(k / 100, 10) for k in (2, 4, 6, 8)}
check("l10 bond prices", [round(p[k], 2) for k in (2, 4, 6, 8)] == [82.03, 67.56, 55.84, 46.32])
num("l10-curves-from-tables", "screens", 9, round(p[6] - p[8], 2), {"same": 14.47})
check("NOTE l10 s[9]: the fall from 2% to 4% is 14.48 to the penny; 14.47 is the gap of the rounded prices",
      round(p[2] - p[4], 2) == 14.48 and round(82.03 - 67.56, 2) == 14.47, f"exact {p[2] - p[4]:.4f}", finding="note-10")
num("l10-curves-from-tables", "quiz", 0, 6, {"neg": -12})
num("l10-curves-from-tables", "quiz", 2, 3 ** -2, {"times": -6, "neg": -9}, tol=6e-4)
# NOTE for finding 9: a curve can cross a line it approaches.
h = lambda x: x / (x * x + 1)
check("NOTE l10 s[4]: y = x/(x^2+1) reaches its asymptote y = 0 at x = 0", h(0) == 0 and abs(h(1e6)) < 1e-5 and abs(h(-1e6)) < 1e-5,
      "'approaches but never reaches' is not the definition", finding="note-9")

q = lambda x: x * x - 2 * x - 3
check("l11 landmarks of x^2-2x-3", q(-1) == q(3) == 0 and q(1) == -4 and q(0) == -3 and all(q(1) < q(1 + k / 10) for k in range(-30, 31) if k))
num("l11-reading-a-graph", "screens", 4, -3, {"root-left": -1, "root-right": 3, "turn": -4})
hh = lambda x: x ** 3 - 3 * x * x + 4
check("l11 cubic turning points and roots", hh(0) == 4 and hh(2) == 0 and hh(-1) == 0 and all(hh(a / 10) > hh((a + 1) / 10) for a in range(0, 20)) and all(hh(a / 10) < hh((a + 1) / 10) for a in list(range(-20, 0)) + list(range(20, 35))))
check("l11 x^2-x-2 roots", [x for x in range(-5, 6) if x * x - x - 2 == 0] == [-1, 2] and (0 - 5) * (0 + 2) == -10)
smile = lambda x: 0.01 * (x - 105) ** 2 + 18
num("l11-reading-a-graph", "screens", 9, min(range(80, 126), key=smile), {"spot": 100, "value": 18})
num("l11-reading-a-graph", "quiz", 1, 8, {"root": 2, "root-big": 4, "turn": 9 - 18 + 8})
num("l11-reading-a-graph", "quiz", 3, (4 - 2) * (4 - 6), {"x": 4, "int": 12})
check("l11 quiz roots of x^2+2x-3", [x for x in range(-6, 6) if x * x + 2 * x - 3 == 0] == [-3, 1] and (-1) ** 2 - 2 - 3 == -4)

walk = lambda x: min(80 * x, 800, 800 - 80 * (x - 15))
check("l12 walk", walk(10) == walk(12) == walk(15) == 800 and walk(25) == 0)
num("l12-graphs-that-tell-stories", "screens", 3, 2 * 3, {"avg": 3, "height": 9})
num("l12-graphs-that-tell-stories", "screens", 4, (0 - 800) / (25 - 15), {"pos": 80, "rise": -800})
bill = lambda x: min(0.3 * x, 10 + 0.2 * x)
check("l12 tariff", close(bill(100), 30) and close(bill(200), 50))
num("l12-graphs-that-tell-stories", "screens", 5, (bill(200) - bill(100)) / 100, {"avg": 0.25, "first": 0.3})
price = lambda x: 100 + 6 * x - x * x
check("l12 high at 3 hours, gradient 0 there, 6 at the open", price(3) == 109 and max(price(k / 4) for k in range(25)) == 109 and 6 - 2 * 3 == 0)


def max_drawdown(v):
    best = peak = 0
    peak = v[0]
    for x in v:
        peak = max(peak, x)
        best = max(best, peak - x)
    return best


v = J("l12-graphs-that-tell-stories")["screens"][9]["canvas"]["params"]["series"][0]["values"]
num("l12-graphs-that-tell-stories", "screens", 9, max_drawdown(v), {"max-min": max(v) - 90, "trough": 90})
num("l12-graphs-that-tell-stories", "quiz", 1, (240 - 600) / 12, {"pos": 30, "rise": -360})
v2 = J("l12-graphs-that-tell-stories")["quiz"][2]["canvas"]["params"]["series"][0]["values"]
d2 = [b - a for a, b in zip(v2, v2[1:])]
check("l12 quiz fastest fall is day 2 to 3", d2 == [150, 50, -80, -20, 60] and d2.index(min(d2)) == 2)
num("l12-graphs-that-tell-stories", "quiz", 3, 16 / 4, {"inst": 8, "dist": 16})
# NOTE for finding 11: highest and lowest points where the gradient is not 0.
strad = lambda s: max(s - 100, 0) + max(100 - s, 0) - 8
low = min(range(80, 121), key=strad)
check("NOTE l12 summary: the l13 straddle is lowest at a corner (gradients -1 and +1), and x^2 on [-2,3] is highest at an end (gradient 6)",
      low == 100 and strad(99) - strad(100) == 1 and strad(101) - strad(100) == 1 and max(range(-2, 4), key=sq) == 3,
      "'at a highest or lowest point the gradient is 0' needs a smooth curve away from its ends", finding="note-11")

check("l13 x^2 = x+2", [x for x in range(-5, 6) if x * x == x + 2] == [-1, 2])
num("l13-solving-with-graphs", "screens", 4, max(x for x in range(-5, 6) if x * x - 3 == 2 * x), {"height": 6, "smaller": -1})
lo, hi = -3.0, -1.0
for _ in range(80):
    mid = (lo + hi) / 2
    if 2 ** mid - (mid + 2) > 0:
        lo = mid
    else:
        hi = mid
w = W("l13-solving-with-graphs", "screens", 5)
check("l13 2^x = x+2 left root about -1.69", abs(lo + 1.6901) < 1e-3 and abs(w["answer"] - lo) <= w["tol"]["abs"] and abs(2 ** lo - 0.31) < 0.005, f"{lo:.4f}")
check("l13 x^2-2x-3 = 5", [x for x in range(-5, 6) if q(x) == 5] == [-2, 4])
check("l13 x^2+x-6 = 0 via y = 6-x", [(x, x * x) for x in range(-5, 6) if x * x == 6 - x] == [(-3, 9), (2, 4)])
legs = J("l13-solving-with-graphs")["screens"][9]["canvas"]["params"]["legs"]
prem = sum(D(l["premium"]) for l in legs)
check("l13 straddle premium 8, break-evens 92 and 108", prem == 8 and [s for s in range(80, 121) if strad(s) == 0] == [92, 108])
num("l13-solving-with-graphs", "quiz", 1, 3, {"height": 5})
# FINDING 1: l13 s[7] option b. "You moved the terms without changing their signs" would give y = -x - 2, not the option y = x - 2.
opt = [o for o in W("l13-solving-with-graphs", "screens", 7)["options"] if o["id"] == "b"][0]
no_sign_change = lambda x: -x - 2          # x^2 - x - 2 = 0 with -x and -2 moved across unchanged
option_b = lambda x: x - 2
diagnosis_matches = all(no_sign_change(x) == option_b(x) for x in range(-3, 4))
says_unchanged = "without changing their signs" in opt["why"]
check("FINDING 1 l13 s[7] option b: the named mistake produces the option", diagnosis_matches or not says_unchanged,
      "moving -x and -2 across unchanged gives y = -x - 2; y = x - 2 changes the sign of x only", finding="1")

num("review-3", "items", 0, (-2) ** 3 + 5, {"pos": 13, "times": -1, "square": 9, "sign": 3})
num("review-3", "items", 2, 2.5, {"avg": 3, "rise": 15})
sols = [x for x in range(-6, 7) if x * x - 2 * x == x + 4]
num("review-3", "items", 3, min(sols), {"height": 3, "larger": 4, "sign": 1})
num("review-3", "items", 5, (0 + 4) * (0 - 2), {"sign": 8, "root": -4})
pr = lambda x: 100 + 8 * x - x * x
check("r3 rising fastest", (pr(1), pr(4), pr(6)) == (107, 116, 112) and (8 - 2, 8 - 8, 8 - 12) == (6, 0, -4))
check("r3 2^x + x = 3 at x = 1 only", 2 ** 1 + 1 == 3)

num("homework-3", "items", 0, 6 / -4, {"pos": 1.5, "flip": -4 / 6})
num("homework-3", "items", 1, 25 - 50 + 16, {"x": 5, "int": 16, "sign": 9})
v3 = J("homework-3")["items"][3]["canvas"]["params"]["series"][0]["values"]
num("homework-3", "items", 3, max_drawdown(v3), {"order": 380 - 150, "last": 60, "first": 50})
num("homework-3", "items", 4, 60 - 5 - 4, {"no-premium": 56, "breakeven": 55})
check("hw3 cubic x^3 = x+6 has one real root, 2", [x for x in range(-10, 11) if x ** 3 == x + 6] == [2] and 2 * 2 - 4 * 3 < 0)
check("hw3 gradient equals average at t = 2", 2 * 2 == 16 / 4)
b5 = {k: bond(k / 100, 5) for k in (0, 2, 4, 6)}
check("hw3 bond table", [round(b5[k], 2) for k in (0, 2, 4, 6)] == [100.0, 90.57, 82.19, 74.73] and [round((1 + k / 100) ** 5, 5) for k in (2, 4, 6)] == [1.10408, 1.21665, 1.33823])
est = 4 + (82.19 - 80) / (82.19 - 74.73) * 2
exact = (100 / 80) ** 0.2 - 1
check("hw3 bond estimate 4.6%, exact 4.56%, chord overestimates", round(est, 1) == 4.6 and round(exact * 100, 2) == 4.56 and est > exact * 100 and round(bond(0.046, 5), 2) == 79.86)
# NOTE for finding 2: convex is not the same as flattening.
e2 = [2 ** k for k in range(6)]
steps = [b - a for a, b in zip(e2, e2[1:])]
check("NOTE hw3 model (c): y = 2^x is convex and steepens", all(b > a for a, b in zip(steps, steps[1:])),
      "'the curve is flattening, which is what convex means' holds only for a falling curve", finding="note-2")

# problems-1
num("problems-1", "items", 0, Fr(46, 40), {"per-row": 46, "first-row": 43 / 40, "flipped": 40 / 46}, part=0)
E = lambda x: D("1.15") * x - 3
check("p1 kiosk rows", (E(40), E(80), E(120)) == (43, 89, 135) and 46 * 40 - 1797 == 43)
num("problems-1", "items", 0, E(300), {"no-fee": 345, "plus-fee": 348}, part=2)
num("problems-1", "items", 0, (227 + 3) / D("1.15"), {"minus-fee": 224 / 1.15, "no-fee": 227 / 1.15, "forward": E(227)}, part=3)
F = lambda d: 60 - D("0.15") * d
num("problems-1", "items", 1, F(120), {"added": 78, "used": 18}, part=0)
num("problems-1", "items", 1, 400, {"times": 9}, part=1)
num("problems-1", "items", 1, [F(400), F(0)], part=3)
num("problems-1", "items", 1, [F(240), F(80)], part=4)
hs = lambda t: 45 - 5 * (t - 2) ** 2
num("problems-1", "items", 2, hs(0), {"neg-square": 45 - 5 * -4, "no-square": 45 - 5 * -2, "whole-square": 45 - (5 * -2) ** 2}, part=0)
num("problems-1", "items", 2, max(t for t in range(-5, 12) if hs(t) == 0), {"other-root": -1, "no-root": 11, "no-two": 3}, part=1)
num("problems-1", "items", 2, [min(hs(k / 10) for k in range(51)), max(hs(k / 10) for k in range(51))], part=2)
num("problems-1", "items", 2, [t for t in range(-5, 12) if hs(t) == 40], part=3)
num("problems-1", "items", 3, 5, {"per-row": 10, "with-29": 6, "height-over-week": 17}, part=1)
check("p1 sapling 5w+12", all(5 * wk + 12 == y for wk, y in [(1, 17), (3, 27), (4, 32), (6, 42)]) and 10 * 1 + 7 == 17)
num("problems-1", "items", 3, (72 - 12) / 5, {"first-row": 11, "no-c": 14.4, "forward": 372, "per-row": 6.5}, part=3)

# review-1, homework-1
num("review-1", "items", 0, 5 - 2 * -3, {"lost-sign": -1, "sub-first": (5 - 2) * -3})
check("r1 table rule", all(3 * x + 3 == y for x, y in [(2, 9), (5, 18), (8, 27)]) and 9 * 5 - 9 == 36 and 9 * 2 - 9 == 9)
num("review-1", "items", 4, 9.5 * 2 - 4, {"forward": (9.5 + 4) / 2, "wrong-order": (9.5 - 4) * 2})
num("review-1", "items", 7, (D("23.85") - D("24.60")) * 120 - D("4.5"), {"gain-sign": 85.5, "fee-added": -85.5, "no-fee": -90, "sign": 94.5})
check("hw1 table", all(7 - 2 * x == y for x, y in [(-2, 11), (1, 5), (4, -1), (7, -7)]))
num("homework-1", "items", 1, 7 - 20, {"climb-m": -6 * 10 + (11 - 12), "sign": 27, "sign2": 13})
gr = [Fr(k, 100) for k in range(1, 401)]
check("hw1 range of (x-1)^2 on (0,4] is [0,9]", min((x - 1) ** 2 for x in gr) == 0 and max((x - 1) ** 2 for x in gr) == 9 and (2 - 1) ** 2 == 1)
f3 = lambda x: 3 * x - 2
check("hw1 f(a)+f(b)-f(a+b) = -2 for all a, b", all(f3(a) + f3(b) - f3(a + b) == -2 for a in range(-5, 6) for b in range(-5, 6)))
num("homework-1", "items", 4, -4.5, {"payoff": 0, "strike": -120, "sign": 4.5})
check("hw1 inverse check", Fr(2 * 2 + 5, 3) == 3 and Fr(3 * 3 - 5, 2) == 2 and all(Fr(3 * Fr(2 * x + 5, 3) - 5, 2) == x for x in range(-5, 6)))
num("homework-1", "items", 6, 3 + D("7.5") + D("0.004") * 4000, {"boundaries-up": D("7.5") + D("0.004") * 2500 + 16, "percent": 3 + D("7.5") + D("0.4") * 4000})
PQ = lambda n: D("0.65") * n - 15
check("hw1 longform", (PQ(10), PQ(100), PQ(1000), PQ(1), PQ(23), PQ(24)) == (D("-8.5"), 50, 635, D("-14.35"), D("-0.05"), D("0.6")) and all(PQ(n) != 0 for n in range(1, 1001)) and (50 + 15) / D("0.65") == 100)

# problems-3
Pb = lambda x: -5 * x * x + 60 * x - 100
check("p3 bakery", all(Pb(x) == -5 * (x - 2) * (x - 10) for x in range(-3, 14)) and max(range(0, 13), key=Pb) == 6)
num("problems-3", "items", 0, Pb(0), {"sign": 100, "zero": 0}, part=0)
num("problems-3", "items", 0, 6, {"half-top": 5, "half-gap": 4}, part=2)
num("problems-3", "items", 0, Pb(6), {"from-five": Pb(5), "from-four": Pb(4), "sign-square": 180 + 360 - 100}, part=4)
num("problems-3", "items", 1, 0.5 * 25, {"no-square": 2.5, "whole-square": 6.25, "no-half": 25}, part=0)
num("problems-3", "items", 1, 2.5, {"times": 62.5, "distance": 12.5}, part=1)
num("problems-3", "items", 1, 6, {"no-half": 3, "lost-t": math.sqrt(6)}, part=2)
num("problems-3", "items", 1, 18, {"from-three": 9, "no-half": 36}, part=3)
N = lambda t: 200 * 2 ** t
M = lambda t: 1000 + 300 * t
num("problems-3", "items", 2, N(3), {"times-three": 1200, "two-doublings": 800}, part=0)
num("problems-3", "items", 2, M(3) - N(3), {"m-value": 1900, "from-1200": 700}, part=1)
signs = [N(k / 1000) > M(k / 1000) for k in range(0, 12001)]
check("p3 cultures cross exactly once for 0 <= t <= 12, between 3 and 4", sum(a != b for a, b in zip(signs, signs[1:])) == 1 and not signs[3000] and signs[4000])
check("p3 cultures figures", abs(2 ** 3.3 - 9.849) < 5e-4 and abs(2 ** 3.4 - 10.556) < 5e-4 and round(M(3.3) - N(3.3)) == 20 and round(N(3.4) - M(3.4)) == 91)
cross = next(k / 1000 for k in range(3000, 4000) if N(k / 1000) >= M(k / 1000))
w = W("problems-3", "items", 2, 3)
check("p3 crossing about 3.32", abs(cross - 3.32) < 0.005 and abs(w["answer"] - cross) <= w["tol"]["abs"], f"{cross}")
ht = lambda x: x ** 3 - 12 * x * x + 36 * x
check("p3 track", all(ht(x) == x * (x - 6) ** 2 for x in range(-2, 10)) and ht(2) == ht(8) == 32 and [x for x in range(0, 9) if ht(x) == 32] == [2, 8] and all(ht(a / 10) > ht((a + 1) / 10) for a in range(20, 60)))
num("problems-3", "items", 3, ht(4), {"all-plus": 400, "cube-as-times": 12 - 192 + 144}, part=0)

# ---------------------------------------------------------------- report
fails = [r for r in RESULTS if not r[1]]
for name, ok, detail, finding in RESULTS:
    if not ok or (finding and str(finding).startswith("note")):
        print(("ok  " if ok else "FAIL"), name, "|", detail)
print(f"functions L1-3 concepts: {len(RESULTS)} checks, {len(RESULTS) - len(fails)} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
