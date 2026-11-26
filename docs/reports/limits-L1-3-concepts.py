#!/usr/bin/env python3
"""Concept checks for limits L1 to L3 (round 1 blind audit, 26 Nov 2026).

Every graded key, slip value and stated number that the audit ledger rests on is
recomputed here with sympy (exact) or mpmath/NumPy, and compared with the value read
from the content JSON. The course has no code widgets, so nothing is run in Pyodide.

Run from the repository root:
    python docs/reports/limits-L1-3-concepts.py
Written on CPython 3.x with sympy 1.14 and NumPy 2.x (newer than CI's pins; no figure
here depends on the version).

Exit code: 0 when every check passes. A check marked FINDING tests a sentence of the
content as written; it fails while the content is wrong and is listed under the same
number in docs/reviews/audit-limits-1-3.md. Findings whose defect is a missing
hypothesis are demonstrated by a counterexample check that PASSES (the counterexample
exists); those are labelled "counterexample for finding N" and do not change the exit code.
"""
import itertools
import json
import math
import os
import sys

import numpy as np
import sympy as sp

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "limits")
RESULTS = []
_cache = {}


def load(name):
    if name not in _cache:
        with open(os.path.join(ROOT, name + ".json")) as fh:
            _cache[name] = json.load(fh)
    return _cache[name]


def node(name, loc):
    """loc like 's3', 'q1', 'i4', 'i2.p1' -> the screen/quiz/item/part dict."""
    d = load(name)
    part = None
    if "." in loc:
        loc, part = loc.split(".")
    kind, idx = loc[0], int(loc[1:])
    n = {"s": d.get("screens"), "q": d.get("quiz"), "i": d.get("items")}[kind][idx]
    if part:
        n = n["parts"][int(part[1:])]
    return n


def check(name, ok, detail="", finding=None):
    RESULTS.append((name, bool(ok), detail, finding))


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def key(name, loc, value, tol=None):
    """The graded numeric key at loc equals the recomputed value (within the widget's display rounding)."""
    w = node(name, loc)["widget"]
    ans = w["answer"]
    t = tol if tol is not None else 5e-5 * max(1.0, abs(float(value)))
    check(f"{name} {loc} key {ans}", close(ans, value, t), f"recomputed {float(value):.6g}")


def slip(name, loc, wid, value, tol=None):
    """The wrong[] entry `wid` equals the value its named mistake produces."""
    w = node(name, loc)["widget"]
    hit = [x for x in w.get("wrong", []) if x.get("id") == wid]
    if not hit:
        check(f"{name} {loc} slip {wid} exists", False, "no such wrong id")
        return
    v = hit[0]["value"]
    t = tol if tol is not None else 6e-4 * max(1.0, abs(float(value)))
    check(f"{name} {loc} slip {wid} = {v}", close(v, value, t), f"recomputed {float(value):.6g}")


def expr_key(name, loc, expr, sym):
    """The expression key parses to the recomputed sympy expression."""
    from sympy.parsing.latex import parse_latex  # noqa: F401  (not used: keys are simple)
    raise NotImplementedError


x, h, t, y, a, u = sp.symbols("x h t y a u")

# --------------------------------------------------------------------------- level 1
# l1
f = (x**2 - 1) / (x - 1)
check("l1 s0 table and limit 2", sp.limit(f, x, 1) == 2 and all(
    close(f.subs(x, xv), fv) for xv, fv in [(0.9, 1.9), (0.99, 1.99), (0.999, 1.999), (1.001, 2.001), (1.01, 2.01), (1.1, 2.1)]))
key("l1-getting-closer", "s0", 2)
g = (sp.sqrt(x) - 1) / (x - 1)
rows = node("l1-getting-closer", "s2")["canvas"]["params"]["rows"]
check("l1 s2 table of (sqrt x - 1)/(x - 1)", all(abs(float(g.subs(x, r[0])) - float(r[1])) < 6e-7 for r in rows))
key("l1-getting-closer", "s2", sp.limit(g, x, 1))
check("l1 s3 limit of 1 + x^2/2 at 2 is 3", (1 + sp.Rational(1, 2) * 4) == 3)
check("l1 s4 one-sided limits 1 and 3", sp.limit(x / 2 + 1, x, 0) == 1 and sp.limit(3 + x / 3, x, 0) == 3)
k = sp.Integer(1)
check("l1 s5 sin(1/x) runs A and B", all(abs(math.sin(2 * math.pi * n)) < 1e-9 and abs(math.sin(2 * math.pi * n + math.pi / 2) - 1) < 1e-9 for n in range(1, 50)))
check("l1 s5 no limit of sin(1/x) at 0", sp.limit(sp.sin(1 / x), x, 0).has(sp.AccumBounds))
check("l1 s6 limit 4 for 5-(x-3)^2 at 2", 5 - (2 - 3) ** 2 == 4)
check("l1 s8 f(1+h) = 2+h", sp.simplify(f.subs(x, 1 + h) - (2 + h)) == 0)
p = 100.12
rows = node("l1-getting-closer", "s9")["canvas"]["right"]["params"]["rows"]
ok = True
for r in rows:
    s_, b_, a_, m_ = [float(c.replace("£", "")) for c in r]
    ok &= close(b_, round(p - s_ / 4, 2), 1e-9) and close(a_, round(p + 3 * s_ / 4, 2), 1e-9) and close(m_, round((b_ + a_) / 2, 2), 1e-9)
check("l1 s9 bid/ask/mid rows", ok)
key("l1-getting-closer", "s9", 100.12)
for wid, v in [("last-mid", 100.13), ("first-mid", 100.22), ("last-bid", 100.11)]:
    slip("l1-getting-closer", "s9", wid, v)
c = (x**3 - 8) / (x - 2)
rows = node("l1-getting-closer", "q0")["canvas"]["params"]["rows"]
check("l1 q0 table", all(abs(float(c.subs(x, sp.Rational(str(r[0])))) - float(r[1])) < 1e-9 for r in rows))
key("l1-getting-closer", "q0", sp.limit(c, x, 2))
check("l1 q3 cos(1/x) at 1/(n pi) flips", [round(math.cos(n * math.pi)) for n in (1, 2, 3, 4)] == [-1, 1, -1, 1])

# l2
check("l2 s0-s2 limit 6", sp.limit((x**2 - 9) / (x - 3), x, 3) == 6)
check("l2 s1 hole at height 2a", sp.limit((x**2 - a**2) / (x - a), x, a) == 2 * a)
key("l2-computing-limits", "s3", sp.limit((x**2 + x - 6) / (x - 2), x, 2))
slip("l2-computing-limits", "s3", "other-root", -2 + 3)
slip("l2-computing-limits", "s3", "wrong-factor", 2 - 3)
key("l2-computing-limits", "s4", sp.limit((x**2 + 3) / (x + 1), x, 1))
slip("l2-computing-limits", "s4", "flipped", 0.5)
q = (x + 1) / (x - 1)
check("l2 s5 f(1.01)=201, f(0.99)=-199, one-sided infinities differ",
      close(q.subs(x, sp.Rational(101, 100)), 201) and close(q.subs(x, sp.Rational(99, 100)), -199)
      and sp.limit(q, x, 1, "+") == sp.oo and sp.limit(q, x, 1, "-") == -sp.oo)
check("l2 s6 limit 10", sp.limit((x**2 - 25) / (x - 5), x, 5) == 10)
P = 100 + sp.Rational(1, 2) * t**2
check("l2 s9 average rate 2 + h/2", sp.simplify((P.subs(t, 2 + h) - P.subs(t, 2)) / h - (2 + h / 2)) == 0)
key("l2-computing-limits", "s9", 2)
slip("l2-computing-limits", "s9", "price", P.subs(t, 2))
slip("l2-computing-limits", "s9", "hour", 2.5)
key("l2-computing-limits", "q0", sp.limit((x**2 - 16) / (x - 4), x, 4))
key("l2-computing-limits", "q1", 3 * 4 - 1)
slip("l2-computing-limits", "q1", "square-all", (3 * 2) ** 2 - 1)
key("l2-computing-limits", "q2", sp.limit((x**2 + 2 * x - 3) / (x**2 - 1), x, 1))
key("l2-computing-limits", "q3", sp.limit(((3 + h) ** 2 - 9) / h, h, 0))
check("l2 q4 no limit at -2", sp.limit((x + 5) / (x + 2), x, -2, "+") == sp.oo and sp.limit((x + 5) / (x + 2), x, -2, "-") == -sp.oo)
# counterexample for finding 3: a 0/0 form whose limit fails without a non-zero number over 0 at the first substitution
cx_top, cx_bot = x - 1, (x - 1) ** 2
check("counterexample for finding 3: (x-1)/(x-1)^2 is 0/0 at 1 and has no limit",
      cx_top.subs(x, 1) == 0 and cx_bot.subs(x, 1) == 0
      and sp.limit(cx_top / cx_bot, x, 1, "+") == sp.oo and sp.limit(cx_top / cx_bot, x, 1, "-") == -sp.oo)

# l3
g0 = sp.Rational(1, 2) * (x + 4) ** 2 + 1
check("l3 s0 graph: hole height 1, drop 3 to 1, smooth join at 2, asymptote at 3",
      g0.subs(x, -4) == 1 and g0.subs(x, -2) == 3 and abs(-2) - 1 == 1
      and abs(2) - 1 == 1 and 1 / sp.Integer(3 - 2) == 1 and sp.diff(1 / (3 - x), x).subs(x, 2) == 1
      and sp.limit(1 / (3 - x), x, 3, "-") == sp.oo and sp.limit(1 / (3 - x), x, 3, "+") == -sp.oo)
key("l3-without-lifting", "s1", 2 + 1)
check("l3 s4 repair value 4", sp.limit((x**2 - 4) / (x - 2), x, 2) == 4)
check("l3 s7 bottom zero only at +-3", set(sp.solve(x**2 - 9, x)) == {-3, 3})
check("l3 s8 limit 3", sp.limit((x**2 + x - 2) / (x - 1), x, 1) == 3)
key("l3-without-lifting", "s9", 98.15)
check("l3 s9 gap 1.85", close(100 - 98.15, 1.85))
check("l3 q0 hole at 2 with height 1/4, asymptote at -2", sp.limit((x - 2) / (x**2 - 4), x, 2) == sp.Rational(1, 4)
      and sp.limit((x - 2) / (x**2 - 4), x, -2, "+") == sp.oo)
key("l3-without-lifting", "q1", sp.solve(sp.Eq(4 + a, 3 * 2 - 1), a)[0])
key("l3-without-lifting", "q3", 50 + 4.99)

# l4
f = (3 * x + 2) / (x + 1)
rows = node("l4-far-out", "s0")["canvas"]["params"]["rows"]
check("l4 s0 table", all(abs(float(f.subs(x, int(str(r[0]).replace(",", "")))) - float(r[1])) < 6e-7 for r in rows))
key("l4-far-out", "s0", sp.limit(f, x, sp.oo))
tot = lambda v: v * v + 50 * v + 1000
check("l4 s1 shares at 10 and 1000; crossover points 20 and 50",
      tot(10) == 1600 and close(100 / 1600, 0.0625) and close(1e6 / tot(1000), 0.9515, 5e-5)
      and 50 * 20 == 1000 and 50**2 == 50 * 50 and 1000 / tot(100) < 0.1 and 50 * 30 > max(900, 1000))
f = (2 * x**2 + 50 * x) / (x**2 + 1000)
key("l4-far-out", "s2", sp.limit(f, x, sp.oo))
crit = [c_ for c_ in sp.solve(sp.diff(f, x), x) if c_.is_real and c_ > 0][0]
check("l4 s2 hump: maximum about 2.27 near x = 100, f(1000) = 2.048",
      abs(float(f.subs(x, crit)) - 2.27) < 0.006 and 70 < float(crit) < 110 and abs(float(f.subs(x, 1000)) - 2.048) < 5e-4,
      f"max {float(f.subs(x, crit)):.4f} at x = {float(crit):.1f}")
slip("l4-far-out", "s2", "hump", f.subs(x, crit), 0.006)
slip("l4-far-out", "s2", "small", 50 / 1000)
key("l4-far-out", "s3", sp.limit((5 * x + 3) / (2 * x - 7), x, sp.oo))
slip("l4-far-out", "s3", "consts", -3 / 7)
check("l4 s3 value 2.510 at 1000", abs(5003 / 1993 - 2.510) < 5e-4)
check("l4 s4 limit 0", sp.limit((4 * x**2 + 1) / (x**3 - 2), x, sp.oo) == 0)
r = lambda v: v**3 / 2**v
check("l4 s5 x^3/2^x: limit 0, peak at 4, ratio at 10 and 20, growth factor below 2 from x = 4",
      sp.limit(x**3 / 2**x, x, sp.oo) == 0 and max(range(1, 30), key=r) == 4
      and abs(r(10) - 0.98) < 0.005 and abs(r(20) - 0.0076) < 5e-5 and r(20) < 0.01
      and all((1 + 1 / v) ** 3 < 2 for v in range(4, 200)) and (1 + 1 / 3) ** 3 > 2)
check("l4 s6 squeeze sin x / x to 0", sp.limit(sp.sin(x) / x, x, sp.oo) == 0)
f = (x**2 + 1000 * x) / (x**2 + 1)
check("l4 s7 table and limit 1", sp.limit(f, x, sp.oo) == 1 and abs(float(f.subs(x, 10)) - 100.0) < 0.05
      and abs(float(f.subs(x, 100)) - 11.0) < 0.05 and abs(float(f.subs(x, 1000)) - 2.0) < 0.05
      and abs(float(f.subs(x, 100000)) - 1.01) < 0.005)
key("l4-far-out", "s8", sp.limit((7 * x**4 - x) / (2 * x**4 + 3 * x**3), x, sp.oo))
slip("l4-far-out", "s8", "inverted", 2 / 7)
slip("l4-far-out", "s8", "power", 7 / 3)
check("l4 s9 limit 1/2", sp.limit((3 * x**2 - x) / (6 * x**2 + 5), x, sp.oo) == sp.Rational(1, 2))
rows = node("l4-far-out", "s10")["canvas"]["params"]["rows"]
check("l4 s10 compounding table", all(abs(1000 * (1 + 0.05 / int(r[0])) ** int(r[0]) - float(str(r[1]).replace("£", "").replace(",", ""))) < 0.006 for r in rows))
key("l4-far-out", "s10", 1000 * math.exp(0.05), 0.006)
tb = [float(str(r[1]).replace("£", "").replace(",", "")) for r in rows]  # the table as printed (half-up pence)
check("l4 s10 gains 63p, 32p, 21p and 11p to the limit",
      [round(100 * (tb[i_ + 1] - tb[i_])) for i_ in range(3)] == [63, 32, 21]
      and round(100 * (round(1000 * math.exp(.05), 2) - 1051.16)) == 11)
avg = lambda n: sum(0.02 if i % 2 == 0 else -0.01 for i in range(n)) / n
check("l4 s11 running average: even n exactly 0.5%, odd n 0.5% + 1.5%/n",
      all(close(avg(n), 0.005 if n % 2 == 0 else 0.005 + 0.015 / n, 1e-12) for n in range(1, 400)))
key("l4-far-out", "s11", 0.005)
slip("l4-far-out", "s11", "mid", (avg(3) + avg(2)) / 2)
# empirical claim (l4 s11 explain): with random returns the running average settles on the expected return
rng = np.random.default_rng(20261126)
draws = rng.normal(0.005, 0.02, size=(2000, 20000))
dev_small = np.abs(draws[:, :200].mean(axis=1) - 0.005)
dev_big = np.abs(draws.mean(axis=1) - 0.005)
check("l4 s11 law of large numbers (Monte Carlo, 2,000 paths): |mean - mu| shrinks about 10x from n=200 to n=20,000",
      dev_big.mean() < 0.15 * dev_small.mean() and (dev_big < 0.001).mean() > 0.99,
      f"mean abs dev {dev_small.mean():.5f} -> {dev_big.mean():.5f}")
key("l4-far-out", "q0", sp.limit((6 * x**3 + x) / (2 * x**3 - 5), x, sp.oo))
check("l4 q1 limit 0", sp.limit((x + 4) / (x**2 - 3), x, sp.oo) == 0)
check("l4 q2 x^5/1.1^x: 1.1^10 about 2.6, factor crossover about 52, limit 0",
      abs(1.1**10 - 2.6) < 0.01 and abs(1 / (1.1 ** 0.2 - 1) - 52) < 0.1
      and sp.limit(x**5 / sp.Rational(11, 10) ** x, x, sp.oo) == 0)
key("l4-far-out", "q3", math.exp(0.1))

# review-1, homework-1, problems-1
rows = node("review-1", "i0")["canvas"]["params"]["rows"]
check("review-1 i0 table of (e^x - 1)/x", all(abs((math.exp(v) - 1) / v - float(r[1])) < 6e-7
      for r in rows for v in [float(str(r[0]).replace("−", "-"))]))
key("review-1", "i1", sp.limit((x**2 + 3 * x + 2) / (x + 1), x, -1))
slip("review-1", "i1", "sign", 1 + 2)
check("review-1 i2 hole 1/2 at 1", sp.limit((x - 1) / (x**2 - 1), x, 1) == sp.Rational(1, 2))
key("review-1", "i3", sp.limit((4 * x**3 - x) / (2 * x**3 + 7 * x**2), x, sp.oo))
slip("review-1", "i3", "seven", 4 / 7)
key("review-1", "i4", 1 + 1)
slip("review-1", "i4", "value", -1)
slip("review-1", "i4", "avg", (2 + -1) / 2)
key("review-1", "i5", sp.solve(sp.Eq(2 + a, 1 + 3), a)[0])
key("review-1", "i6", sp.limit(((1 + h) ** 3 - 1) / h, h, 0))
key("review-1", "i7", 2000 * math.exp(0.1), 0.006)
slip("review-1", "i7", "e-one", 2000 * math.e, 0.006)
check("review-1 i8 squeeze x sin(1/x) to 0", sp.limit(x * sp.sin(1 / x), x, 0) == 0)
key("homework-1", "i0", sp.limit((x**3 - 27) / (x - 3), x, 3))
rows = node("homework-1", "i1")["canvas"]["params"]["rows"]
check("homework-1 i1 table of sin x / x", all(abs(math.sin(v) / v - float(r[1])) < 6e-7
      for r in rows for v in [float(str(r[0]).replace("−", "-"))]))
key("homework-1", "i2", sp.limit((sp.sqrt(x) - 3) / (x - 9), x, 9), 1e-5)
b = sp.symbols("b")
sol = sp.solve([sp.Eq(a + b, 1), sp.Eq(3 * a + b, 12)], [a, b])
check("homework-1 i3 a = 5.5, b = -4.5", sol[a] == sp.Rational(11, 2) and sol[b] == sp.Rational(-9, 2))
e4 = sp.sqrt(x**2 + 6 * x) - x
key("homework-1", "i4", sp.limit(e4, x, sp.oo))
slip("homework-1", "i4", "inf-guess", e4.subs(x, 100), 0.005)
check("homework-1 i4 value 2.99955 at 10,000", abs(float(e4.subs(x, 10000)) - 2.99955) < 5e-6)
check("homework-1 i5 quotient 12 + 6h + h^2", sp.expand(((2 + h) ** 3 - 8) / h) == 12 + 6 * h + h**2)
check("homework-1 i6 limit 5/2", sp.limit((5 * x**2 - 3 * x) / (2 * x**2 + x + 4), x, sp.oo) == sp.Rational(5, 2))
key("homework-1", "i7", 12.5)
slip("homework-1", "i7", "fee", 12.50 + 9.99)
fh = (x**2 - x - 2) / (x - 2)
check("homework-1 i8 model: table 2.9, 2.99, 3.01, 3.1; limit 3; f(x)/x to 1",
      [float(fh.subs(x, v)) for v in (sp.Rational(19, 10), sp.Rational(199, 100), sp.Rational(201, 100), sp.Rational(21, 10))] == [2.9, 2.99, 3.01, 3.1]
      and sp.limit(fh, x, 2) == 3 and sp.limit(fh / x, x, sp.oo) == 1)
key("problems-1", "i0.p0", 2 + 0.5 * 10)
key("problems-1", "i0.p1", 7 - 4)
key("problems-1", "i0.p2", 0.4)
rr = (2 * x**2 - 2 * x - 12) / (x**2 - 9)
key("problems-1", "i1.p0", sp.limit(rr, x, 3), 1e-5)
slip("problems-1", "i1.p0", "lost-two", sp.Rational(5, 6))
key("problems-1", "i1.p2", sp.limit(rr, x, sp.oo))
slip("problems-1", "i1.p2", "constants", 12 / 9)
gap = sp.simplify(2 - 2 * (x + 2) / (x + 3))
first = next(n for n in range(4, 1000) if gap.subs(x, n) < sp.Rational(1, 100))
key("problems-1", "i1.p3", first)
check("problems-1 i1.p3 gap at 197 is exactly 0.01", gap.subs(x, 197) == sp.Rational(1, 100))
slip("problems-1", "i1.p3", "no-shift", next(n for n in range(4, 1000) if sp.Rational(2, n) < sp.Rational(1, 100)))
slip("problems-1", "i1.p3", "lost-two", next(n for n in range(4, 1000) if sp.Rational(1, n + 3) < sp.Rational(1, 100)))
key("problems-1", "i2.p0", 2)
key("problems-1", "i2.p1", sp.solve(sp.Eq(8 + 2 * b - 6, 0), b)[0])
slip("problems-1", "i2.p1", "dropped-six", sp.solve(sp.Eq(8 + 2 * b, 0), b)[0])
slip("problems-1", "i2.p1", "from-half", sp.solve(sp.Eq(2 + 2 * b - 6, 0), b)[0])
ff = (2 * x**2 - x - 6) / (x**2 - x - 2)
key("problems-1", "i2.p3", sp.limit(ff, x, 2), 1e-5)
check("problems-1 i2.p2 top at -1 is -3", (2 * x**2 - x - 6).subs(x, -1) == -3)
slip("problems-1", "i2.p3", "bottom-slip", sp.Rational(7, 1))
slip("problems-1", "i2.p3", "top-slip", sp.Rational(1, 3))
key("problems-1", "i3.p0", 4 / 20)
key("problems-1", "i3.p1", sp.limit(50 + 4 * sp.sin(t) / t, t, sp.oo))
key("problems-1", "i3.p2", 4 / 0.01)

# --------------------------------------------------------------------------- level 2
s = 5 * t**2
dq = lambda fn, at, hv: (fn.subs(t, at + hv) - fn.subs(t, at)) / hv
key("l5-instant-speed", "s1", dq(s, 1, 2))
slip("l5-instant-speed", "s1", "half-run", 45 / 2)
check("l5 s2-s5 averages 20 + 5h and 30 + 5h; table; left quotient 19.5",
      sp.simplify(dq(s, 2, h) - (20 + 5 * h)) == 0 and sp.simplify(dq(s, 3, h) - (30 + 5 * h)) == 0
      and [float(dq(s, 2, sp.Rational(1, 10**n))) for n in (1, 2, 3)] == [20.5, 20.05, 20.005]
      and float(dq(s, 2, -sp.Rational(1, 10))) == 19.5 and float(s.subs(t, sp.Rational(19, 10))) == 18.05)
key("l5-instant-speed", "s4", dq(s, 2, -sp.Rational(1, 10)))
key("l5-instant-speed", "s5", sp.diff(s, t).subs(t, 3))
slip("l5-instant-speed", "s5", "wide", dq(s, 3, 1))
slip("l5-instant-speed", "s5", "from-start", 45 / 3)
P = 100 + 5 * t - t**2
rows = node("l5-instant-speed", "s9")["canvas"]["params"]["rows"]
exp_rows = [(3, 106.00, 0.00), (2.5, 106.25, 0.50), (2.1, 106.09, 0.90), (1.9, 105.89, 1.10)]
check("l5 s9 window table and rate 1 - h",
      all(close(P.subs(t, sp.Rational(str(tv))), pv, 1e-9) and close(dq(P, 2, sp.Rational(str(tv)) - 2), rv, 1e-9) for tv, pv, rv in exp_rows)
      and sp.simplify(dq(P, 2, h) - (1 - h)) == 0 and [r[-1] for r in rows] == ["£0.00", "£0.50", "£0.90", "£1.10"])
key("l5-instant-speed", "s9", sp.diff(P, t).subs(t, 2))
key("l5-instant-speed", "q0", dq(s, 1, 1))

C = 50 + 2 * x + sp.Rational(1, 10) * x**2
check("l6 s2, s5, s9 expansions", sp.expand(((a + h) ** 2 - a**2) / h) == 2 * a + h
      and sp.expand((x + h) ** 3) == x**3 + 3 * x**2 * h + 3 * x * h**2 + h**3
      and sp.expand(((x + h) ** 3 - x**3) / h) == 3 * x**2 + 3 * x * h + h**2)
check("l6 s10 difference quotient 2 + 0.2q + 0.1h", sp.simplify((C.subs(x, x + h) - C) / h - (2 + x / 5 + h / 10)) == 0)
key("l6-first-principles", "s10", sp.diff(C, x).subs(x, 20))
slip("l6-first-principles", "s10", "average", C.subs(x, 20) / 20)
slip("l6-first-principles", "s10", "one-more", C.subs(x, 21) - C.subs(x, 20))
slip("l6-first-principles", "s10", "total", C.subs(x, 20))
key("l6-first-principles", "q0", (4.1**2 - 16) / 0.1, 1e-9)
C2 = 100 + 4 * x + sp.Rational(1, 2) * x**2
key("l6-first-principles", "q3", sp.diff(C2, x).subs(x, 10))
slip("l6-first-principles", "q3", "average", C2.subs(x, 10) / 10)
slip("l6-first-principles", "q3", "one-more", C2.subs(x, 11) - C2.subs(x, 10))
# counterexample for finding 6 ("the cube climbs everywhere except x = 0"; "where f rises, f' > 0"):
# x^3 is strictly increasing through 0, where its slope is 0.
check("counterexample for finding 6: x^3 is strictly increasing through 0 although its slope there is 0",
      all((-hv) ** 3 < 0 < hv**3 for hv in (1e-9, 1e-3, 0.5)) and sp.diff(x**3, x).subs(x, 0) == 0)

rows = node("l7-power-rule", "s1")["canvas"]["params"]["rows"]
check("l7 s1 slope table n x^(n-1) at 1, 2, 3", all([int(v) for v in r[1:]] == [n * xv ** (n - 1) for xv in (1, 2, 3)] for n, r in enumerate(rows, start=1)))
check("l7 s2 derivative 12x^3 - 4x, slope 8 at 1", sp.diff(3 * x**4 - 2 * x**2 + 7, x) == 12 * x**3 - 4 * x and (12 - 4) == 8)
key("l7-power-rule", "s3", sp.diff(1 / x, x).subs(x, 2))
slip("l7-power-rule", "s3", "power-kept", -1 / 2)
slip("l7-power-rule", "s3", "power-up", -1)
key("l7-power-rule", "s4", sp.diff(sp.sqrt(x), x).subs(x, 4))
slip("l7-power-rule", "s4", "power-kept", 0.5 * 4**0.5)
slip("l7-power-rule", "s4", "no-half", 1 / 2)
check("l7 s5 derivative of 1/x^3 is -3/x^4", sp.simplify(sp.diff(x**-3, x) + 3 / x**4) == 0)
V = 80 + sp.Rational(4, 5) * t**2
key("l7-power-rule", "s8", sp.diff(V, t).subs(t, 4))
slip("l7-power-rule", "s8", "height", V.subs(t, 4))
slip("l7-power-rule", "s8", "since-trough", (V.subs(t, 4) - 80) / 4)
slip("l7-power-rule", "s8", "whole", (V.subs(t, 5) - 80) / 5)
slip("l7-power-rule", "s8", "gain", V.subs(t, 4) - 80)
f = 5 * x**3 - 4 * x + 9
key("l7-power-rule", "q1", sp.diff(f, x).subs(x, 2))
slip("l7-power-rule", "q1", "kept-constant", 15 * 4 - 4 + 9)
slip("l7-power-rule", "q1", "height", f.subs(x, 2))
slip("l7-power-rule", "q1", "dropped-linear", 60)
key("l7-power-rule", "q2", sp.diff(x**-2, x).subs(x, 1))
slip("l7-power-rule", "q2", "bottom", 1 / 2)
key("l7-power-rule", "q3", sp.diff(x * sp.sqrt(x), x).subs(x, 4))
slip("l7-power-rule", "q3", "power-kept", 1.5 * 4**1.5)
slip("l7-power-rule", "q3", "product-split", 1 * 1 / (2 * 2))

f = 5 - (x - 3) ** 2
check("l8 s1-s2 slope graph 6 - 2x; slopes 6, 3, 0, -3, -6", sp.expand(sp.diff(f, x)) == 6 - 2 * x
      and [sp.diff(f, x).subs(x, v) for v in (0, sp.Rational(3, 2), 3, sp.Rational(9, 2), 6)] == [6, 3, 0, -3, -6]
      and sp.expand(f) == -x**2 + 6 * x - 4)
f = x**3 - 3 * x
check("l8 s3 slopes 9, 0, -3, 0, 9", [sp.diff(f, x).subs(x, v) for v in (-2, -1, 0, 1, 2)] == [9, 0, -3, 0, 9])
f = 6 - (x - 4) ** 2
pts = node("l8-slope-graph", "s4")["canvas"]["state"]["points"]
xs = {p_["id"]: p_["x"] for p_ in pts}
check("l8 s4 slopes B 6, D 3, A 0, C -3; C and D share a height; B lowest",
      [sp.diff(f, x).subs(x, sp.Rational(str(xs[k_]))) for k_ in "BDAC"] == [6, 3, 0, -3]
      and f.subs(x, sp.Rational(str(xs["C"]))) == f.subs(x, sp.Rational(str(xs["D"])))
      and min("ABCD", key=lambda k_: f.subs(x, sp.Rational(str(xs[k_])))) == "B", str(xs))
check("l8 s5 one-sided slopes: corner -1/1, cusp -inf/+inf, vertical tangent +inf both sides",
      sp.limit(sp.diff(sp.Rational(3, 2) * sp.sqrt(x), x), x, 0, "+") == sp.oo
      and sp.limit(sp.diff(sp.Rational(3, 2) * sp.sqrt(-x), x), x, 0, "-") == -sp.oo
      and sp.limit(sp.diff(sp.cbrt(x), x), x, 0, "+") == sp.oo)
check("l8 s7 secant of x^3 from 1 to 1.5 is 4.75; slope 3 at 1", (1.5**3 - 1) / 0.5 == 4.75 and 3 * 1**2 == 3)
Vt = 5 * sp.log(1 + sp.exp((x - 100) / 5))
dl = sp.diff(Vt, x)
check("l8 s8 toy call: delta is the logistic target; deltas 0.02, 0.12, 0.50, 0.88, 0.98; V(90) = 0.63; V above payoff",
      sp.simplify(dl - 1 / (1 + sp.exp((100 - x) / 5))) == 0
      and [round(float(dl.subs(x, v)), 2) for v in (80, 90, 100, 110, 120)] == [0.02, 0.12, 0.50, 0.88, 0.98]
      and round(float(Vt.subs(x, 90)), 2) == 0.63
      and all(float(Vt.subs(x, v)) > max(v - 100, 0) for v in range(80, 121)))
from math import erf, sqrt, log
N = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
ok = True
for sig, T, r_ in itertools.product((0.1, 0.2, 0.4, 0.8), (1 / 52, 0.25, 1.0), (0.0, 0.02, 0.05)):
    d1 = (r_ + sig * sig / 2) * T / (sig * sqrt(T))
    d2 = d1 - sig * sqrt(T)
    ok &= N(d1) > 0.5 and N(d1) > N(d2)
check("l8 s8 and homework-2 i8: Black-Scholes at-the-money call delta N(d1) > 0.5 and N(d1) > N(d2) (r >= 0, no dividends, 36 cases)", ok)
key("l8-slope-graph", "q3", sp.diff(4 * x**2, x).subs(x, sp.Rational(3, 2)))
slip("l8-slope-graph", "q3", "cancelled", 4 * 1.5)
slip("l8-slope-graph", "q3", "height", 4 * 1.5**2)
# FINDING 1: "Only corners, cusps and vertical tangents lack a derivative" (l8 s6, why of option 3).
# The step function (0 for x < 0, 1 for x >= 0) has slope 0 on both sides of 0, so it has no corner, cusp or vertical
# tangent there, yet (f(h) - f(0))/h = -1/h for h < 0 is unbounded: no derivative. x sin(1/x) (0 at 0) is continuous at 0
# and its quotient sin(1/h) has no limit.
step_left = sp.limit((0 - 1) / h, h, 0, "-")
osc = sp.limit(sp.sin(1 / h), h, 0)
check("l8 s6: every point with no derivative is a corner, a cusp or a vertical tangent (content claim)",
      "Only corners, cusps and vertical tangents lack a derivative" not in node("l8-slope-graph", "s6")["widget"]["options"][2]["why"]
      or not (step_left == sp.oo and osc.has(sp.AccumBounds)),
      "the step function at its jump and x sin(1/x) at 0 have no derivative and are none of the three", finding=1)

key("review-2", "i0", (16 - 1) / 3)
key("review-2", "i1", sp.diff(t**3, t).subs(t, 2))
check("review-2 i1 slips 19 and 4", 12 + 6 + 1 == 19 and 8 / 2 == 4)
check("review-2 i2 quotient 6x + 3h", sp.expand((3 * (x + h) ** 2 - 3 * x**2) / h) == 6 * x + 3 * h)
check("review-2 i3 derivative 12x^2 - 5", sp.diff(4 * x**3 - 5 * x + 2, x) == 12 * x**2 - 5)
key("review-2", "i4", sp.diff(6 * sp.sqrt(x), x).subs(x, 9))
check("review-2 i4 slips 2 and 9", 6 / 3 == 2 and 3 * 3 == 9)
check("review-2 i5/i7 stationary points", set(sp.solve(sp.diff(x**3 - 3 * x, x), x)) == {-1, 1}
      and sp.diff(x**3 - 3 * x, x).subs(x, 0) == -3 and set(sp.solve(sp.diff(x**3 - 12 * x, x), x)) == {-2, 2})
key("homework-2", "i0", sp.diff(sp.Rational(49, 10) * t**2, t).subs(t, 3))
check("homework-2 i0 slips 14.7, 34.3, 44.1", close(4.9 * 9 / 3, 14.7) and close(29.4 + 4.9, 34.3) and close(4.9 * 9, 44.1))
check("homework-2 i1 derivative of 1/x from the quotient", sp.limit((1 / (x + h) - 1 / x) / h, h, 0) == -1 / x**2)
check("homework-2 i2 derivative", sp.simplify(sp.diff(2 * sp.sqrt(x) - 3 / x + x**4 / 4, x) - (1 / sp.sqrt(x) + 3 / x**2 + x**3)) == 0)
Cm = 2000 + 15 * x + sp.Rational(2, 100) * x**2
key("homework-2", "i3", sp.diff(Cm, x).subs(x, 250))
check("homework-2 i3 slips 28, 25.02, 7000", Cm.subs(x, 250) == 7000 and Cm.subs(x, 250) / 250 == 28
      and Cm.subs(x, 251) - Cm.subs(x, 250) == sp.Rational(2502, 100))
check("homework-2 i4 slope graph x^2 - 4", sp.diff(x**3 / 3 - 4 * x, x) == x**2 - 4)
Vc = 4 + sp.Rational(1, 2) * (x - 100) + sp.Rational(25, 1000) * (x - 100) ** 2
key("homework-2", "i5", sp.diff(Vc, x).subs(x, 104))
check("homework-2 i5 slips 6.4 and 0.6", Vc.subs(x, 104) == sp.Rational(64, 10) and 0.5 + 0.025 * 4 == 0.6)
Pm = 100 + 6 * t - t**3 / 3
avg_rate = (Pm.subs(t, 3) - Pm.subs(t, 0)) / 3
tm = [v for v in sp.solve(sp.Eq(sp.diff(Pm, t), avg_rate), t) if v > 0][0]
key("homework-2", "i6", tm)
check("homework-2 i6 average rate 3; flat at sqrt 6", avg_rate == 3 and abs(float(sp.sqrt(6)) - 2.4495) < 5e-5)
key("homework-2", "i7", sp.diff(5 * x**-2, x).subs(x, -1))
check("homework-2 i7 slip -2.5", sp.Rational(5, 2 * -1) == sp.Rational(-5, 2))
gq = lambda hv: ((2 + hv) ** -4 - 2**-4) / hv
check("homework-2 i8 model: |h|/h is +-1; x|x| quotient |h| to 0",
      sp.limit(sp.Abs(h) / h, h, 0, "+") == 1 and sp.limit(sp.Abs(h) / h, h, 0, "-") == -1 and sp.limit(sp.Abs(h), h, 0) == 0)
check("homework-2 i9 model numbers: g'(2) = -0.125; quotients -0.1235, -0.1266, -0.1248, -0.1252; g(2.01), g(1.99); g'(-2) = 0.125",
      sp.diff(x**-4, x).subs(x, 2) == -sp.Rational(1, 8) and round(gq(0.01), 4) == -0.1235 and round(gq(-0.01), 4) == -0.1266
      and round(gq(0.001), 4) == -0.1248 and round(gq(-0.001), 4) == -0.1252
      and round(2.01**-4, 6) == 0.061265 and round(1.99**-4, 6) == 0.063766
      and sp.diff(x**-4, x).subs(x, -2) == sp.Rational(1, 8) and abs(gq(0.01) + 0.125) < 0.002 and abs(gq(-0.01) + 0.125) < 0.002)
Nn = 3 * t**2 + 4 * t
key("problems-2", "i0.p0", (Nn.subs(t, 4) - Nn.subs(t, 1)) / 3)
check("problems-2 i0 quotient 16 + 3h, slips", sp.expand((Nn.subs(t, 2 + h) - Nn.subs(t, 2)) / h) == 16 + 3 * h
      and Nn.subs(t, 4) / 4 == 16 and sp.Rational(57, 4) == sp.Rational(1425, 100))
key("problems-2", "i0.p2", sp.diff(Nn, t).subs(t, 2))
key("problems-2", "i0.p3", sp.solve(sp.Eq(sp.diff(Nn, t), 34), t)[0])
slip("problems-2", "i0.p3", "no-bring-down", sp.solve(sp.Eq(3 * t + 4, 34), t)[0])
slip("problems-2", "i0.p3", "dropped-four", sp.solve(sp.Eq(6 * t, 34), t)[0])
Vf = 2 * t**3 - 9 * t**2 + 12 * t + 500
check("problems-2 i1: V' = 6(t-1)(t-2); V(3) = 509; lowest slope -1.5 at 1.5; V(1.5) = 504.5",
      sp.expand(sp.diff(Vf, t) - 6 * (t - 1) * (t - 2)) == 0 and Vf.subs(t, 3) == 509
      and sp.diff(Vf, t).subs(t, sp.Rational(3, 2)) == -sp.Rational(3, 2) and Vf.subs(t, sp.Rational(3, 2)) == sp.Rational(1009, 2))
key("problems-2", "i1.p3", -1.5)
check("problems-2 i2: left quotient 4 + 0.5h; draft m=3, b=-4 meets 8; m = 4, b = -8 is the tangent",
      sp.expand((sp.Rational(1, 2) * (4 + h) ** 2 - 8) / h) == 4 + h / 2 and 3 * 4 - 4 == 8
      and sp.diff(x**2 / 2, x).subs(x, 4) == 4 and 4 * 4 - 8 == 8)
key("problems-2", "i2.p2", 4)
key("problems-2", "i2.p3", -8)
Pp = 5 / x
key("problems-2", "i3.p0", (Pp.subs(x, sp.Rational(4, 100)) - 100) / sp.Rational(-1, 100))
key("problems-2", "i3.p1", (Pp.subs(x, sp.Rational(49, 1000)) - 100) / sp.Rational(-1, 1000), 0.01)
key("problems-2", "i3.p2", sp.diff(Pp, x).subs(x, sp.Rational(5, 100)))
slip("problems-2", "i3.p2", "no-square", -5 / 0.05)
check("problems-2 i3.p3 slope -3125 at 0.04", sp.diff(Pp, x).subs(x, sp.Rational(4, 100)) == -3125)

# --------------------------------------------------------------------------- level 3
key("l9-products-quotients", "s1", sp.Rational(42, 10) * sp.Rational(31, 10) - 12)
check("l9 s2 corner share about 7% at t = 0.4 and under 1% at 0.04", abs(2 * .4**2 / (10 * .4 + 2 * .4**2) - 0.074) < 0.001 and 2 * .04**2 / (10 * .04 + 2 * .04**2) < 0.01)
A = (4 + 2 * t) * (3 + t)
check("l9 s3 growth 6t + 4t + 2t^2", sp.expand(A - 12) == 10 * t + 2 * t**2)
key("l9-products-quotients", "s3", sp.diff(A, t).subs(t, 0))
slip("l9-products-quotients", "s3", "not-limit", 10 + 2 * 0.1)
key("l9-products-quotients", "s4", 0.5 * 2 + 5 * 3)
check("l9 s5 derivative 8x^3 + 3x^2, slope 11 at 1", sp.expand(sp.diff(x**3 * (2 * x + 1), x)) == 8 * x**3 + 3 * x**2 and 8 + 3 == 11)
check("l9 s7 derivative of x^2 * x^3", sp.diff(x**2 * x**3, x) == 5 * x**4)
U, Vv = sp.Function("u")(x), sp.Function("v")(x)
check("l9 s9 quotient rule from u = qv", sp.simplify(sp.diff(U / Vv, x) - (sp.diff(U, x) * Vv - U * sp.diff(Vv, x)) / Vv**2) == 0)
f = x / (x + 1)
key("l9-products-quotients", "s10", sp.diff(f, x).subs(x, 1))
slip("l9-products-quotients", "s10", "no-square", sp.Rational(1 * 2 - 1 * 1, 2))
key("l9-products-quotients", "s11", 0.05 * 10000 + 40 * 200)
slip("l9-products-quotients", "s11", "corner", 0.05 * 200)
check("l9 q0 derivative", sp.expand(sp.diff(x**4 * (x**2 + 1), x)) == 6 * x**5 + 4 * x**3)
gg = x**2 / (x + 1)
key("l9-products-quotients", "q1", sp.diff(gg, x).subs(x, 1))
slip("l9-products-quotients", "q1", "no-square", sp.Rational(2 * 2 - 1, 2))
key("l9-products-quotients", "q2", (1 * 2.5 - 50 * 0.1) / 2.5**2)
slip("l9-products-quotients", "q2", "tops-bottoms", 1 / 0.1)
slip("l9-products-quotients", "q2", "no-square", (1 * 2.5 - 50 * 0.1) / 2.5)
check("l9 q2 growth rates 2% and 4%", close(1 / 50, 0.02) and close(0.1 / 2.5, 0.04))

key("l10-inside-function", "s1", -8 * 0.05)
slip("l10-inside-function", "s1", "added", -8 + 0.05)
slip("l10-inside-function", "s1", "divided", -8 / 0.05)
check("l10 s2 slopes 2.4, 6.22, product 14.93 at x = 1.2", close(2 * 1.2, 2.4) and round(3 * 1.44**2, 2) == 6.22
      and round(6 * 1.2**5, 2) == 14.93 and round(2.4 + 6.22, 2) == 8.62 and round(6.22 / 2.4, 2) == 2.59)
key("l10-inside-function", "s3", sp.diff((x**2 + 1) ** 3, x).subs(x, 1))
slip("l10-inside-function", "s3", "outer-at-x", 3 * 1**2 * 2)
slip("l10-inside-function", "s3", "added", 2 + 12)
check("l10 s4-s6, s8 chain-rule keys",
      sp.simplify(sp.diff((3 * x + 1) ** 2, x) - 6 * (3 * x + 1)) == 0
      and sp.simplify(sp.diff((3 * x**2 + 1) ** 5, x) - 30 * x * (3 * x**2 + 1) ** 4) == 0
      and sp.simplify(sp.diff(sp.sqrt(x**2 + 1), x) - x / sp.sqrt(x**2 + 1)) == 0
      and sp.simplify(sp.diff((x**2 + 1) ** 3, x) - 6 * x * (x**2 + 1) ** 2) == 0 and 6 * 4 == 24 and 3 * 4 == 12)
key("l10-inside-function", "s7", sp.diff((x**2 - 4) ** 3, x).subs(x, 0))
slip("l10-inside-function", "s7", "outside-only", 3 * 16)
Pb = 100 * (1 + y / 2) ** -20
d = sp.diff(Pb, y).subs(y, sp.Rational(4, 100))
key("l10-inside-function", "s10", d, 0.006)
slip("l10-inside-function", "s10", "no-inside", 2 * d, 0.006)
slip("l10-inside-function", "s10", "kept-power", -1000 * 1.02**-20, 0.006)
check("l10 s10 tangent fall 6.60 and true fall 6.27 for +0.01", round(float(-d) * 0.01, 2) == 6.60
      and round(float(Pb.subs(y, 0.04) - Pb.subs(y, 0.05)), 2) == 6.27)
key("l10-inside-function", "q1", sp.diff(sp.sqrt(4 * x + 1), x).subs(x, 2), 1e-4)
slip("l10-inside-function", "q1", "no-inside", sp.Rational(1, 6))
key("l10-inside-function", "q2", 100 * 3 * 0.3)

key("l11-standard-derivatives", "s2", math.log(2), 6e-4)
slip("l11-standard-derivatives", "s2", "flipped", 1 / math.log(2))
check("l11 s1-s2 values: e, e^2, 2 ln 2, ln 3", round(math.e, 2) == 2.72 and round(math.e**2, 2) == 7.39
      and round(2 * math.log(2), 3) == 1.386 and round(math.log(3), 3) == 1.099)
key("l11-standard-derivatives", "s3", sp.diff(sp.log(x), x).subs(x, 4))
check("l11 s4 nine slopes of sin", [round(math.cos(i * math.pi / 4), 2) + 0.0 for i in range(9)] == [1, 0.71, 0, -0.71, -1, -0.71, 0, 0.71, 1])
check("l11 s5 cos is sin shifted left by pi/2 and its slope is -sin",
      sp.simplify(sp.cos(x) - sp.sin(x + sp.pi / 2)) == 0 and sp.simplify(sp.cos(x + sp.pi / 2) + sp.sin(x)) == 0)
check("l11 s6 slope of 2^x: 2^x ln 2; 5.55 at 3; the power-rule slip gives 12", sp.simplify(sp.diff(2**x, x) - 2**x * sp.log(2)) == 0
      and round(8 * math.log(2), 2) == 5.55 and 3 * 2**2 == 12)
check("l11 s8 slope of exp(-x^2) and -2/e", sp.simplify(sp.diff(sp.exp(-x**2), x) + 2 * x * sp.exp(-x**2)) == 0 and round(-2 / math.e, 2) == -0.74)
check("l11 s9 slope of ln(5x) is 1/x; ln 5 = 1.61", sp.simplify(sp.diff(sp.log(5 * x), x) - 1 / x) == 0 and round(math.log(5), 2) == 1.61)
pv = 1000 * sp.exp(-sp.Rational(5, 100) * t)
key("l11-standard-derivatives", "s10", sp.diff(pv, t).subs(t, 10), 0.006)
slip("l11-standard-derivatives", "s10", "no-inside", pv.subs(t, 10), 0.006)
check("l11 q0 slope of x e^x is zero at -1, a minimum", sp.solve(sp.diff(x * sp.exp(x), x), x) == [-1] and sp.diff(x * sp.exp(x), x, 2).subs(x, -1) > 0)
key("l11-standard-derivatives", "q1", 2 / 50)
key("l11-standard-derivatives", "q3", 1 / 1.05, 5e-5)
slip("l11-standard-derivatives", "q3", "value", math.log(1.05), 5e-5)
# counterexample for finding 5: other functions equal to their own slope
check("counterexample for finding 5: 3e^x and 0 are their own slope graphs", sp.diff(3 * sp.exp(x), x) == 3 * sp.exp(x) and sp.diff(sp.Integer(0), x) == 0)

Y = sp.Function("y")(x)
def implicit(eq):
    return sp.solve(sp.diff(eq, x), sp.diff(Y, x))[0]
yp = implicit(x**2 + Y**2 - 25)
check("l12 s1-s3 circle slope -x/y", sp.simplify(yp + x / Y) == 0)
key("l12-implicit", "s2", yp.subs(Y, -4).subs(x, 3))
yp = implicit(x**2 + 4 * Y**2 - 25)
key("l12-implicit", "s4", yp.subs(Y, 2).subs(x, 3))
slip("l12-implicit", "s4", "circle-rule", -3 / 2)
slip("l12-implicit", "s4", "flipped", -4 * 2 / 3, 1e-3)
yp = implicit(x**2 + Y**2 + 3 * Y - 22)
check("l12 s6: slope -4/9; centre (0, -1.5), radius slope 9/4; slips -10/3, -2/3, -4/3",
      yp.subs(Y, 3).subs(x, 2) == -sp.Rational(4, 9) and sp.Rational(3 + sp.Rational(3, 2), 2) == sp.Rational(9, 4)
      and sp.Rational(-(4 + 6), 3) == -sp.Rational(10, 3) and sp.Rational(-4, 6) == -sp.Rational(2, 3) and 22 + sp.Rational(9, 4) == sp.Rational(97, 4))
fol = x**3 + Y**3 - 6 * x * Y
yp = implicit(fol)
check("l12 s7 folium slope (2y - x^2)/(y^2 - 2x)", sp.simplify(yp - (2 * Y - x**2) / (Y**2 - 2 * x)) == 0)
key("l12-implicit", "s8", yp.subs(Y, 3).subs(x, 3))
slip("l12-implicit", "s8", "no-chain", sp.Rational(27 + 27 - 18, 18))
slip("l12-implicit", "s8", "dropped-y", sp.Rational(18 - 27, 27), 1e-3)
slip("l12-implicit", "s8", "dropped-xy", sp.Rational(-27, 27 - 18))
# counterexample for finding 2 ("a zero denominator in y' flags a vertical tangent", l12 s5 explain and summary):
# on the lesson's own curve x^3 + y^3 = 6xy the denominator y^2 - 2x is zero at (0, 0), where the numerator is zero too
# and the branch y = x^2/6 + x^5/1296 + ... has a horizontal tangent.
num0, den0 = (2 * y - x**2).subs({x: 0, y: 0}), (y**2 - 2 * x).subs({x: 0, y: 0})
resid = sp.expand((x**3 + (x**2 / 6 + x**5 / 1296) ** 3 - 6 * x * (x**2 / 6 + x**5 / 1296)))
check("counterexample for finding 2: at (0,0) on the folium y' is 0/0 and one branch is flat (curve satisfied to order x^8)",
      den0 == 0 and num0 == 0 and sp.Poly(resid, x).monoms()[-1][0] >= 9)
w1, W2 = sp.symbols("w1"), sp.Function("w2")(sp.symbols("w1"))
var = sp.Rational(4, 100) * w1**2 + sp.Rational(1, 100) * W2**2
dw = sp.solve(sp.diff(var, w1), sp.diff(W2, w1))[0]
key("l12-implicit", "s9", dw.subs(W2, sp.Rational(4, 10)).subs(w1, sp.Rational(3, 10)))
check("l12 s9 variance 0.0052 at (0.3, 0.4)", var.subs(W2, sp.Rational(4, 10)).subs(w1, sp.Rational(3, 10)) == sp.Rational(52, 10000))
slip("l12-implicit", "s9", "ignored-vol", -0.3 / 0.4)
key("l12-implicit", "q0", -5 / 12, 1e-4)
key("l12-implicit", "q2", implicit(x * Y - 12).subs(Y, 4).subs(x, 3), 1e-4)
key("l12-implicit", "q3", implicit(Y**2 - x**3).subs(Y, 8).subs(x, 4))
slip("l12-implicit", "q3", "no-two", sp.Rational(48, 8))

f = (x**2 + 1) * (x**3 - 2)
key("review-3", "i0", sp.diff(f, x).subs(x, 2))
check("review-3 i0 expansion 5x^4 + 3x^2 - 4x", sp.expand(sp.diff(f, x)) == 5 * x**4 + 3 * x**2 - 4 * x)
check("review-3 i1, i2, i5 keys", sp.simplify(sp.diff((2 * x - 5) ** 4, x) - 8 * (2 * x - 5) ** 3) == 0
      and sp.simplify(sp.diff(x / (x**2 + 1), x) - (1 - x**2) / (x**2 + 1) ** 2) == 0
      and (x / (x**2 + 1)).subs(x, 1) == sp.Rational(1, 2)
      and sp.simplify(sp.diff(x**2 * sp.log(x), x) - (2 * x * sp.log(x) + x)) == 0)
Pz = 100 * (1 + y) ** -3
key("review-3", "i3", sp.diff(Pz, y).subs(y, sp.Rational(5, 100)), 0.006)
slip("review-3", "i3", "kept-power", -300 * 1.05**-3, 0.006)
key("review-3", "i4", -4 * math.exp(-0.2), 6e-5)
slip("review-3", "i4", "no-inside", 100 * math.exp(-0.2), 6e-4)
yp = implicit(x**2 + x * Y + Y**2 - 7)
key("review-3", "i6", yp.subs(Y, 2).subs(x, 1))
slip("review-3", "i6", "no-y-prime", -(2 + 2 + 4) / 1)
slip("review-3", "i6", "dropped-y", sp.Rational(-2, 5))
Pt = 40 * sp.exp(sp.Rational(6, 100) * t) * (1 + sp.Rational(2, 100) * t)
key("review-3", "i7", sp.diff(sp.log(Pt), t).subs(t, 0))
slip("review-3", "i7", "price-rate", sp.diff(Pt, t).subs(t, 0) / 100)
check("homework-3 i0, i1, i2, i5, i6 keys",
      sp.simplify(sp.diff(x**2 * sp.exp(3 * x), x) - (2 * x * sp.exp(3 * x) + 3 * x**2 * sp.exp(3 * x))) == 0
      and sp.simplify(sp.diff(sp.log(x**2 + 1), x) - 2 * x / (x**2 + 1)) == 0
      and sp.simplify(sp.diff(sp.tan(x), x) - 1 / sp.cos(x) ** 2) == 0
      and sp.simplify(sp.diff(sp.log(sp.cos(x)), x) + sp.tan(x)) == 0
      and sp.simplify(sp.diff(x**x, x) - x**x * (sp.log(x) + 1)) == 0)
P5 = 100 * (1 + y) ** -5
key("homework-3", "i3", (-sp.diff(P5, y) / P5).subs(y, sp.Rational(4, 100)), 6e-5)
var = sp.Rational(4, 100) * w1**2 + sp.Rational(1, 100) * W2**2 + sp.Rational(2, 100) * w1 * W2
dw = sp.solve(sp.diff(var, w1), sp.diff(W2, w1))[0]
at = lambda e_: e_.subs(W2, sp.Rational(4, 10)).subs(w1, sp.Rational(3, 10))
key("homework-3", "i4", at(dw), 6e-5)
check("homework-3 i4 cross term 2 * 0.5 * 0.2 * 0.1 = 0.02", close(2 * 0.5 * 0.2 * 0.1, 0.02))
slip("homework-3", "i4", "no-cross", -3)
slip("homework-3", "i4", "dropped-w1", -0.032 / 0.008)
slip("homework-3", "i4", "flipped", 1 / at(dw))
check("homework-3 i7 model numbers", round(100 * math.exp(-0.2), 2) == 81.87 and round(-500 * math.exp(-0.2), 2) == -409.37
      and round(-500 * math.exp(-0.2) * 0.001, 4) == -0.4094 and round(100 * math.exp(-0.205), 4) == 81.4647
      and round(100 * math.exp(-0.205) - 100 * math.exp(-0.2), 4) == -0.4083
      and round(-409.37 * 0.002, 4) == -0.8187)
Pq, Iq = 30 * sp.exp(sp.Rational(7, 100) * t), 1500 * sp.exp(sp.Rational(5, 100) * t)
key("problems-3", "i0.p0", sp.diff(Pq, t).subs(t, 0))
key("problems-3", "i0.p1", sp.diff(Pq / Iq, t).subs(t, 0), 1e-9)
slip("problems-3", "i0.p1", "no-square", 900 / 1500)
slip("problems-3", "i0.p1", "rates", 2.1 / 75)
slip("problems-3", "i0.p1", "no-chain", (30 * 1500 - 30 * 75) / 1500**2)
key("problems-3", "i0.p2", (sp.diff(Pq / Iq, t) / (Pq / Iq)).subs(t, 0), 1e-9)
Rv = x * (50 - x) ** 2
key("problems-3", "i1.p0", sp.diff((50 - x) ** 2, x).subs(x, 20))
key("problems-3", "i1.p1", sp.diff(Rv, x).subs(x, 20))
check("problems-3 i1.p2 R'(p) = (50 - p)(50 - 3p)", sp.simplify(sp.diff(Rv, x) - (50 - x) * (50 - 3 * x)) == 0)
key("problems-3", "i1.p3", sp.Rational(50, 3), 1e-5)
yp = sp.solve(sp.diff(sp.Rational(8, 10) * sp.log(x) + sp.Rational(2, 10) * sp.log(Y), x), sp.diff(Y, x))[0]
key("problems-3", "i2.p0", yp.subs(Y, 1600).subs(x, 100))
ynew = 1600 * sp.Rational(100, 200) ** 4
key("problems-3", "i2.p1", ynew)
key("problems-3", "i2.p2", yp.subs(Y, ynew).subs(x, 200))
key("problems-3", "i2.p3", (1600 - ynew) / 100)
check("problems-3 i2 slips -16, -4, -0.25, 800, 400, -16, -8, 33",
      -1600 / 100 == -16 and -0.25 * 16 == -4 and -4 * 100 / 1600 == -0.25 and 1600 / 2 == 800 and 1600 / 4 == 400
      and -4 * 800 / 200 == -16 and -4 * 200 / 100 == -8 and (64 + 2) / 2 == 33)
sf = 1 + sp.Rational(3, 10) * sp.cos(sp.pi * t / 6)
key("problems-3", "i3.p1", sp.diff(sf, t).subs(t, 3), 6e-6)
Dm = (200 + 5 * t) * sf
key("problems-3", "i3.p2", sp.diff(Dm, t).subs(t, 3), 6e-3)
check("problems-3 i3 slips -0.7854, -59.5, -33.77", round(5 * -0.05 * math.pi, 4) == -0.7854 and 5 - 215 * 0.3 == -59.5 and round(-215 * 0.05 * math.pi, 2) == -33.77)

# counterexamples for the remaining hypothesis findings
check("counterexample for finding 7: substitution gives a number that is not the limit (l1 s6: k(2) = 1, limit 4)",
      sp.limit(5 - (x - 3) ** 2, x, 2) == 4 and 1 != 4)
check("counterexample for finding 8: sin(1/x) near 0 is bounded (no asymptote) and has no one-sided limits (no hole, no jump)",
      sp.limit(sp.sin(1 / x), x, 0, "+").has(sp.AccumBounds) and sp.limit(sp.sin(1 / x), x, 0, "-").has(sp.AccumBounds))
check("counterexample for finding 9: cbrt(x^3) = x has slope 1 at 0 although the inside link x^3 is flat there",
      sp.diff(x**3, x).subs(x, 0) == 0 and sp.limit(sp.diff(sp.cbrt(u), u), u, 0, "+") == sp.oo
      and all(abs((hv**3) ** (1 / 3) / hv - 1) < 1e-9 for hv in (1e-3, 1e-6)))
tan0 = sp.diff(x**3 - 3 * x, x).subs(x, 0) * x  # tangent to x^3 - 3x at 0 is y = -3x
check("counterexample for finding 10: the tangent to x^3 - 3x at 0 crosses the curve (curve - tangent = x^3 changes sign)",
      sp.expand(x**3 - 3 * x - tan0) == x**3)
check("counterexample for finding 12: for x^2 * x^3, u'v' = 6x^3 is not zero; the corner's share is u'v' h, which vanishes",
      sp.diff(x**2, x) * sp.diff(x**3, x) == 6 * x**3
      and sp.limit(sp.expand(((x + h) ** 2 - x**2) * ((x + h) ** 3 - x**3)) / h, h, 0) == 0
      and sp.limit(sp.expand(((x + h) ** 2 - x**2) * ((x + h) ** 3 - x**3)) / h**2, h, 0) == 6 * x**3)
check("counterexample for finding 4: a function with no jump whose change does not shrink (sin(1/x), 0 at 0)",
      sp.limit(sp.sin(1 / h) - 0, h, 0).has(sp.AccumBounds))

# --------------------------------------------------------------------------- structural sweeps
# 1. Every order widget's key is the listed order of its lines (the lines were judged in listed order).
def walk(o, path=""):
    if isinstance(o, dict):
        yield path, o
        for k_, v_ in o.items():
            yield from walk(v_, f"{path}.{k_}")
    elif isinstance(o, list):
        for i_, v_ in enumerate(o):
            yield from walk(v_, f"{path}[{i_}]")

FILES = ["l1-getting-closer", "l2-computing-limits", "l3-without-lifting", "l4-far-out", "l5-instant-speed",
         "l6-first-principles", "l7-power-rule", "l8-slope-graph", "l9-products-quotients", "l10-inside-function",
         "l11-standard-derivatives", "l12-implicit", "review-1", "review-2", "review-3", "homework-1", "homework-2",
         "homework-3", "problems-1", "problems-2", "problems-3"]
n_order = 0
bad = []
for fn in FILES:
    for pth, o in walk(load(fn)):
        if isinstance(o.get("lines"), list) and isinstance(o.get("answer"), list) and o["lines"] and isinstance(o["lines"][0], dict):
            n_order += 1
            if [l_["id"] for l_ in o["lines"]] != o["answer"]:
                bad.append(f"{fn}{pth}")
check(f"order widgets: key equals the listed (logical) order in all {n_order}", not bad and n_order >= 12, ", ".join(bad))

# 2. No numeric slip sits inside its key's tolerance, and no two slips of one widget coincide.
bad = []
for fn in FILES:
    for pth, o in walk(load(fn)):
        if isinstance(o.get("answer"), (int, float)) and isinstance(o.get("wrong"), list):
            tol = (o.get("tol") or {}).get("abs", 0)
            vals = [w_["value"] for w_ in o["wrong"] if isinstance(w_.get("value"), (int, float))]
            if any(abs(v_ - o["answer"]) <= tol for v_ in vals) or len(set(vals)) != len(vals):
                bad.append(f"{fn}{pth}")
check("numeric widgets: every slip value is outside the key's tolerance and distinct", not bad, ", ".join(bad))

# 3. Fluency families: brute-force every variable draw; key equals the recomputed value; slips never equal the key.
def draws(spec):
    names, pools = [], []
    for nm, sp_ in spec.items():
        if "int" in sp_:
            lo, hi = sp_["int"]
            pool = [v_ for v_ in range(lo, hi + 1) if v_ not in sp_.get("not", [])]
        else:
            pool = sp_["pick"]
        names.append(nm)
        pools.append(pool)
    for combo in itertools.product(*pools):
        yield dict(zip(names, combo))

def ev(expr, env):
    return eval(expr.replace("^", "**"), {"gcd": lambda a_, b_: math.gcd(int(a_), int(b_)), "abs": abs, "sign": lambda v_: (v_ > 0) - (v_ < 0)}, dict(env))

A_, B_, C_, D_, K_, M_, N_ = sp.symbols("A B C D K M N", nonzero=True)
def family(fname, idx, recompute, slips):
    """recompute(env) -> exact key from my own derivation (Fractions), or None if the item is ill-posed;
    slips(env) -> the slip values. Checks the content's key expression against it on every draw."""
    F = load(fname)["families"][idx]
    key_expr = F["widget"]["answer"].strip("{}")
    n = 0
    for env in draws(F["vars"]):
        env = {k_: (Fr(v_) if isinstance(v_, int) else v_) for k_, v_ in env.items()}
        for nm, ex in F.get("let", {}).items():
            env[nm] = ev(ex, env)
        if not all(ev(w_, env) for w_ in F.get("where", [])):
            continue
        n += 1
        kv = recompute(env)
        if kv is None or ev(key_expr, env) != kv or any(s_ == kv for s_ in slips(env)):
            check(f"{fname} family {idx} draw {env}", False, "key wrong or a slip equals the key")
            return
    check(f"{fname} family {idx}: {n} draws, key recomputed, no slip equals the key", n > 0)

from fractions import Fraction as Fr
def lim_cancel(a_, p_, q_):
    """x^2 + p x + q = (x - a)(x + a + p) + remainder; returns the cofactor's value at a, or None."""
    return (2 * a_ + p_) if a_ * a_ + p_ * a_ + q_ == 0 else None
family("fluency-l2-computing-limits", 0, lambda e: lim_cancel(e["a"], e["p"], e["q"]), lambda e: [0, 1, e["a"] - e["b"]])
def two_quads(e):
    t_, b_ = lim_cancel(e["a"], e["p1"], e["q1"]), lim_cancel(e["a"], e["p2"], e["q2"])
    return None if t_ is None or b_ in (None, 0) else t_ / b_
family("fluency-l2-computing-limits", 1, two_quads, lambda e: [1 / two_quads(e), 1])
family("fluency-l2-computing-limits", 2, lambda e: 2 * e["k"] * e["a"] if e["c"] == e["k"] * e["a"] ** 2 else None, lambda e: [0, 2 * e["a"]])
family("fluency-l7-power-rule", 3, lambda e: 3 * e["a"] * e["k"] ** 2 + 2 * e["b"] * e["k"] + e["c"], lambda e: [e["fk"], e["np"]])
family("fluency-l9-products-quotients", 2, lambda e: 2 * e["k"] * (e["q"] * e["k"] + e["r"]) + (e["k"] ** 2 + e["p"]) * e["q"], lambda e: [e["pd"], e["one"]])
ell = lambda e: -(2 * e["a"] * e["p"]) / (2 * e["b"] * e["q"]) if e["c"] == e["a"] * e["p"] ** 2 + e["b"] * e["q"] ** 2 else None
family("fluency-l12-implicit", 0, ell, lambda e: [-ell(e), 1 / ell(e)])
circ = lambda e: -(2 * e["p"]) / (2 * e["q"] + e["k"]) if e["c"] == e["p"] ** 2 + e["q"] ** 2 + e["k"] * e["q"] else None
family("fluency-l12-implicit", 1, circ, lambda e: [-(2 * e["p"] + e["k"]) / (2 * e["q"]), -e["p"] / e["q"]])
xyc = lambda e: -(2 * e["p"] + e["k"] * e["q"]) / (e["k"] * e["p"] + 2 * e["q"])
family("fluency-l12-implicit", 2, xyc, lambda e: [-(2 * e["p"] + e["k"] * e["q"]) / (2 * e["q"]), -(2 * e["p"]) / (e["k"] * e["p"] + 2 * e["q"])])
check("fluency-l12 symbolic slopes: ellipse, circle with a y term, xy term",
      sp.simplify(implicit(A_ * x**2 + B_ * Y**2 - C_) + A_ * x / (B_ * Y)) == 0
      and sp.simplify(implicit(x**2 + Y**2 + K_ * Y - C_) + 2 * x / (2 * Y + K_)) == 0
      and sp.simplify(implicit(x**2 + K_ * x * Y + Y**2 - C_) + (2 * x + K_ * Y) / (K_ * x + 2 * Y)) == 0)
# Expression families: the key formula and each slip formula, symbolically in the family's parameters.
check("fluency-l7 families 0-2 symbolic keys",
      sp.expand(sp.diff(A_ * x**3 + B_ * x**2 + C_ * x + D_, x) - (3 * A_ * x**2 + 2 * B_ * x + C_)) == 0
      and sp.simplify(sp.diff(A_ / x**N_, x) - (-N_ * A_ * x ** (-N_ - 1))) == 0
      and sp.simplify(sp.diff(K_ * x ** (M_ / N_), x) - (K_ * M_ / N_) * x ** ((M_ - N_) / N_)) == 0)
check("fluency-l9 families 0-1 symbolic keys",
      sp.simplify(sp.diff(x**N_ * (A_ * x + B_), x) - ((N_ + 1) * A_ * x**N_ + N_ * B_ * x ** (N_ - 1))) == 0
      and sp.simplify(sp.diff((A_ * x + B_) / (C_ * x + D_), x) - (A_ * D_ - B_ * C_) / (C_ * x + D_) ** 2) == 0)
check("fluency-l10 families 0-2 symbolic keys",
      sp.simplify(sp.diff((A_ * x + B_) ** N_, x) - N_ * A_ * (A_ * x + B_) ** (N_ - 1)) == 0
      and sp.simplify(sp.diff((A_ * x**2 + B_) ** N_, x) - 2 * A_ * N_ * x * (A_ * x**2 + B_) ** (N_ - 1)) == 0
      and sp.simplify(sp.diff(sp.sqrt(A_ * x**2 + B_), x) - A_ * x / sp.sqrt(A_ * x**2 + B_)) == 0)
check("fluency-l11 families 0-3 symbolic keys",
      sp.simplify(sp.diff(A_ * sp.exp(K_ * x), x) - A_ * K_ * sp.exp(K_ * x)) == 0
      and sp.simplify(sp.diff(M_ * sp.log(A_ * x + B_), x) - M_ * A_ / (A_ * x + B_)) == 0
      and sp.simplify(sp.diff(A_ * sp.sin(K_ * x), x) - A_ * K_ * sp.cos(K_ * x)) == 0
      and sp.simplify(sp.diff(A_ * sp.cos(K_ * x), x) + A_ * K_ * sp.sin(K_ * x)) == 0)
fl = {f_: load(f_)["families"] for f_ in ("fluency-l10-inside-function", "fluency-l11-standard-derivatives")}
check("fluency-l10/l11: the 'forgot the inside' slip can never equal the key (inside factor never 1, or guarded)",
      fl["fluency-l10-inside-function"][0]["wrong"][0].get("when") == "a != 1"
      and 1 in fl["fluency-l11-standard-derivatives"][0]["vars"]["k"]["not"]
      and fl["fluency-l11-standard-derivatives"][1]["vars"]["a"]["int"][0] >= 2
      and fl["fluency-l11-standard-derivatives"][2]["vars"]["k"]["int"][0] >= 2
      and fl["fluency-l11-standard-derivatives"][3]["vars"]["k"]["int"][0] >= 2)

# --------------------------------------------------------------------------- report
fails = [r_ for r_ in RESULTS if not r_[1]]
plain = [r_ for r_ in fails if r_[3] is None]
found = [r_ for r_ in fails if r_[3] is not None]
for nm, ok_, det, fnd in RESULTS:
    if not ok_:
        print(("FINDING %s " % fnd if fnd else "FAIL ") + nm + (": " + det if det else ""))
print(f"{len(RESULTS)} checks: {len(RESULTS) - len(fails)} pass, {len(found)} fail as findings, {len(plain)} fail otherwise")
sys.exit(1 if fails else 0)
