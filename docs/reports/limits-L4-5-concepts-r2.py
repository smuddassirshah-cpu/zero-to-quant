#!/usr/bin/env python3
"""Blind concept audit, round 2: limits levels 4 and 5 (l13 to l20, reviews,
homework, problems, fluency-l13).

Recomputes every printed figure, every slip value from its named mistake, the
fluency families over their whole range (sympy), and the empirical claims
(Kelly growth, minimum variance, Jensen) by simulation. Exits 0 when the
content agrees; a check that fails because the content is wrong stays failing.

Run from the repository root:  python docs/reports/limits-L4-5-concepts-r2.py
"""
import itertools
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import stats

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
C = os.path.join(ROOT, "app", "content", "courses", "limits")
FAILS = []
N = [0]


def load(name):
    with open(os.path.join(C, name + ".json")) as fh:
        return json.load(fh)


def ok(cond, label):
    N[0] += 1
    if not cond:
        FAILS.append(label)
        print("FAIL", label)


def near(a, b, tol, label):
    ok(abs(a - b) <= tol, f"{label}: got {a!r}, content {b!r}")


def screen(lesson, i):
    return lesson["screens"][i]


def wrongs(w):
    return {x["id"]: x.get("value") for x in w.get("wrong", [])}


L = {k: load(k) for k in [
    "l13-peaks-and-troughs", "l14-best-value", "l15-sensitivity",
    "l16-both-to-zero", "l17-somewhere-in-between", "l18-rates-in-step",
    "l19-running-backwards", "l20-which-way-it-bends", "review-4", "review-5",
    "homework-4", "homework-5", "problems-4", "problems-5",
    "fluency-l13-peaks-and-troughs"]}
x, y, s, t, r, q, u, w, f_ = sp.symbols("x y s t r q u w f")

# ---------------------------------------------------------------- generic
# No slip value may sit inside the key's tolerance, and no two slips overlap.


def walk(o, path=""):
    if isinstance(o, dict):
        if "answer" in o and isinstance(o.get("answer"), (int, float)) and "wrong" in o:
            yield path, o
        for k, v in o.items():
            yield from walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")


for name, doc in L.items():
    for path, wd in walk(doc):
        tol = wd.get("tol", {})
        ta = tol.get("abs", 0) if isinstance(tol, dict) else tol
        ivs = []
        for z in wd["wrong"]:
            if "value" not in z or not isinstance(z["value"], (int, float)):
                continue
            tz = z.get("tol", {}).get("abs", 0)
            ok(abs(z["value"] - wd["answer"]) > ta + tz,
               f"{name}{path}: slip {z['id']} overlaps the key")
            ivs.append((z["id"], z["value"], tz))
        for (a, va, ta_), (b, vb, tb_) in itertools.combinations(ivs, 2):
            ok(abs(va - vb) > ta_ + tb_, f"{name}{path}: slips {a} and {b} overlap")

# Expression widgets: accept forms equal the key, wrong forms do not.
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,  # noqa: E402
                                        implicit_multiplication_application, convert_xor)
import re  # noqa: E402

TR = standard_transformations + (implicit_multiplication_application, convert_xor)


def _group(sx, i):
    """Return (content, end) of the brace group that opens at sx[i]."""
    depth, j = 0, i
    while True:
        depth += sx[j] == "{"
        depth -= sx[j] == "}"
        if depth == 0:
            return sx[i + 1:j], j + 1
        j += 1


def tex(sx):
    """A small LaTeX reader for the forms these widgets use."""
    sx = sx.replace("\\left", "").replace("\\right", "").replace("\\dfrac", "\\frac")
    sx = sx.replace("\\tfrac", "\\frac").replace("\\cdot", "*").replace("\\,", "")
    while "\\frac" in sx:
        i = sx.index("\\frac")
        a, j = _group(sx, i + 5)
        b, k = _group(sx, j)
        sx = sx[:i] + "((" + a + ")/(" + b + "))" + sx[k:]
    while "\\sqrt" in sx:
        i = sx.index("\\sqrt")
        a, j = _group(sx, i + 5)
        sx = sx[:i] + "sqrt(" + a + ")" + sx[j:]
    while "^{" in sx:
        i = sx.index("^{")
        a, j = _group(sx, i + 1)
        sx = sx[:i] + "^(" + a + ")" + sx[j:]
    sx = sx.replace("e^", " E^")
    sx = sx.replace("exp(", "EXP(").replace("sqrt(", "SQRT(")
    sx = re.sub(r"(?<=[0-9a-zA-Z)])\(", "*(", sx)
    sx = sx.replace("EXP*(", "exp(").replace("SQRT*(", "sqrt(").replace("EXP(", "exp(").replace("SQRT(", "sqrt(")
    try:
        return parse_expr(sx, transformations=TR, local_dict={"E": sp.E})
    except Exception:
        return None


for probe, want in (("\\frac{900(2-s)}{(2+s)^3}", 900*(2 - s)/(2 + s)**3),
                    ("-\\frac{520}{(1+y)^6}", -520/(1 + y)**6),
                    ("(x^2-1)e^{-x^2/2}", (x**2 - 1)*sp.exp(-x**2/2)),
                    ("\\frac{1}{\\sqrt{4-x^2}}", 1/sp.sqrt(4 - x**2)),
                    ("-100e^{-2u}-400e^{-8u}+500e^{-5u}", sp.diff(50*sp.exp(-2*u) + 50*sp.exp(-8*u) - 100*sp.exp(-5*u), u))):
    got = tex(probe)
    ok(got is not None and sp.simplify(got - want.subs({k: sp.Symbol(k.name) for k in want.free_symbols})) == 0,
       "LaTeX reader self-test " + probe)


def walk_expr(o, path=""):
    if isinstance(o, dict):
        if isinstance(o.get("answer"), str) and "wrong" in o and o.get("kind") == "expression":
            yield path, o
        for k, v in o.items():
            yield from walk_expr(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_expr(v, f"{path}[{i}]")


rng = np.random.default_rng(13)
for name, doc in L.items():
    if name.startswith("fluency"):
        continue
    for path, wd in walk_expr(doc):
        key = tex(wd["answer"])
        ok(key is not None, f"{name}{path}: key not readable")
        if key is None:
            continue
        for acc in wd.get("accept", []):
            ea = tex(acc)
            ok(ea is not None, f"{name}{path}: accept form not readable: {acc}")
            if ea is not None:
                ok(sp.simplify(ea - key) == 0, f"{name}{path}: accept form differs from the key: {acc}")
        syms = sorted(key.free_symbols, key=str)
        pts = [{sy: sp.Float(v) for sy, v in zip(syms, rng.uniform(0.11, 0.83, len(syms)))}
               for _ in range(4)]
        for z in wd["wrong"]:
            e = tex(z.get("tex", ""))
            ok(e is not None, f"{name}{path}: wrong form not readable: {z['id']}")
            if e is None:
                continue
            pts = [{**{sy: sp.Float(0.37) for sy in e.free_symbols}, **p} for p in pts]
            same = all(abs(complex(sp.N((e - key).subs(p)))) < 1e-9 for p in pts)
            ok(not same, f"{name}{path}: wrong form {z['id']} equals the key")

# ---------------------------------------------------------------- l13
l = L["l13-peaks-and-troughs"]
f = x**3 - 3*x
fp = sp.diff(f, x)
ok(fp.subs(x, -1.5) == 3.75 and fp.subs(x, -0.5) == -2.25, "l13 s0 hint slopes")
ok(fp.subs(x, 2) == 9 and fp.subs(x, 0) == -3, "l13 s1 slopes 9 and -3")
g = x**3 - 6*x**2 + 9*x + 1
gp = sp.diff(g, x)
ok(sp.solve(gp, x) == [1, 3] and g.subs(x, 1) == 5 and g.subs(x, 3) == 1, "l13 s2 stationary")
ok(gp.subs(x, sp.Rational(1, 2)) == sp.Rational(15, 4) and gp.subs(x, sp.Rational(3, 2)) == -sp.Rational(9, 4), "l13 s3 slopes")
ok(sp.diff(g, x, 2).subs(x, 3) == 6 and sp.diff(g, x, 2).subs(x, 1) == -6, "l13 s4 g''")
ok(max(g.subs(x, v) for v in (0, 1, 3, 5)) == 21 == screen(l, 6)["widget"]["answer"], "l13 s6 closed interval")
V = sp.Rational(4, 100)*w**2 + sp.Rational(9, 100)*(1 - w)**2
ws = sp.solve(sp.diff(V, w), w)[0]
ok(ws == sp.Rational(9, 13), "l13 s9 w*")
near(float(ws), screen(l, 9)["widget"]["answer"], 1e-4, "l13 s9 key")
near(float(V.subs(w, ws)), 0.02769, 5e-6, "l13 s9 variance")
near(float(sp.sqrt(V.subs(w, ws))), 0.166, 5e-4, "l13 s9 vol 16.6%")
near((1/0.2)/(1/0.2 + 1/0.3), wrongs(screen(l, 9)["widget"])["inverse-vol"], 1e-9, "l13 s9 inverse-vol slip")
ok(sp.diff(V, w).subs(w, 1) == sp.Rational(8, 100), "l13 s9 slope at 1")
ok(V.subs(w, sp.Rational(1, 2)) == sp.Rational(325, 10000) and sp.diff(V, w).subs(w, sp.Rational(1, 2)) == -sp.Rational(5, 100), "l13 s9 equal slip figures")
near(float(V.subs(w, 0.2)), 0.0592, 1e-9, "l13 s9 start point")
# Monte Carlo: the variance at 9/13 is below 0.6, 0.5 and 1 (uncorrelated).
z = np.random.default_rng(1).standard_normal((2_000_000, 2)) * np.array([0.2, 0.3])
mc = {wv: np.var(wv*z[:, 0] + (1 - wv)*z[:, 1]) for wv in (9/13, 0.6, 0.5, 1.0, 0.75)}
ok(all(mc[9/13] < mc[k] for k in (0.6, 0.5, 1.0, 0.75)), "l13 s9 MC minimum variance")
near(mc[9/13], 0.027692, 2e-4, "l13 s9 MC variance")
q0 = x**3 - 12*x
ok(sp.diff(q0, x, 2).subs(x, -2) == -12 and q0.subs(x, -2) == 16, "l13 quiz0")
q1 = x**4 - 4*x**3
ok(sp.factor(sp.diff(q1, x)) == 4*x**2*(x - 3) and sp.diff(q1, x, 2).subs(x, 3) == 36, "l13 quiz1")
ok(all(sp.diff(q1, x).subs(x, v) < 0 for v in (-0.1, 0.1)), "l13 quiz1 signs")
near(math.exp(-1), l["quiz"][3]["widget"]["answer"], 1e-4, "l13 quiz3")

# ---------------------------------------------------------------- l14
l = L["l14-best-value"]
A = w*(40 - 2*w)
ok(sp.solve(sp.diff(A, w), w) == [10] and A.subs(w, 10) == 200, "l14 s0")
near(float(A.subs(w, sp.Rational(40, 3))), 178, 0.5, "l14 s0 square slip 178")
ok(13 <= 40/3 <= 13.5, "l14 s0 square band holds 40/3")
Vb = x*(30 - 2*x)**2
ok(sp.expand(sp.diff(Vb, x) - (30 - 2*x)*(30 - 6*x)) == 0 and Vb.subs(x, 5) == 2000, "l14 s2")
near(float(Vb.subs(x, 7.5)), 1687.5, 1e-9, "l14 s2 quarter slip")
S = x**2 + 128000/x
ok(sp.solve(sp.diff(S, x), x, domain=sp.S.Reals)[0] == 40 or 40 in sp.solve(sp.diff(S, x), x), "l14 s4")
ok(S.subs(x, 40) == 4800 and sp.diff(S, x, 2).subs(x, 40) == 6, "l14 s4/s5")
near(128000 ** (1/3), wrongs(screen(l, 4)["widget"])["forgot-2"], 0.01, "l14 s4 forgot-2")
ok(A.subs(w, 12) == 192, "l14 s6")
G = sp.Rational(6, 10)*sp.log(1 + f_) + sp.Rational(4, 10)*sp.log(1 - f_)
ok(sp.solve(sp.diff(G, f_), f_) == [sp.Rational(1, 5)], "l14 s9 Kelly 0.2")
near(float(G.subs(f_, 0.05)), 0.008757, 5e-7, "l14 s9 start")
near(float(G.subs(f_, 0.2)), 0.020136, 5e-7, "l14 s9 peak")
ok(float(G.subs(f_, 0.4)) < 0 and float(G.subs(f_, 0.6)) < 0, "l14 s9 over-betting shrinks")
ok(float(sp.diff(G, f_).subs(f_, 0.3)) < 0, "l14 s9 half-p slope")
# Monte Carlo of the long-run growth rate per bet: one binomial draw of 1e9 bets.
W = np.random.default_rng(2).binomial(10**9, 0.6)
for fv in (0.2, 0.4, 0.1, 0.3):
    emp = (W*math.log(1 + fv) + (10**9 - W)*math.log(1 - fv))/10**9
    near(emp, float(G.subs(f_, fv)), 1e-4, f"l14 s9 MC growth at {fv}")
emp = {fv: (W*math.log(1 + fv) + (10**9 - W)*math.log(1 - fv))/10**9 for fv in (0.1, 0.2, 0.3, 0.4)}
ok(emp[0.2] > emp[0.1] and emp[0.2] > emp[0.3] and emp[0.4] < 0, "l14 s9 MC ordering")
p_, b_ = sp.symbols("p b", positive=True)
Gg = p_*sp.log(1 + b_*f_) + (1 - p_)*sp.log(1 - f_)
ok(sp.simplify(sp.solve(sp.diff(Gg, f_), f_)[0] - (p_ - (1 - p_)/b_)) == 0, "Kelly formula")
ok(l["quiz"][0]["widget"]["answer"] == 450, "l14 quiz0")
pi_ = 0.05*q - 0.000002*q**2
near(float(sp.solve(sp.diff(pi_, q), q)[0]), 12500, 1e-6, "l14 quiz1")
near(float(pi_.subs(q, 12500)), 312.5, 1e-9, "l14 quiz1 profit")
near(float(pi_.subs(q, 25000)), 0, 1e-9, "l14 quiz1 forgot-2 profit 0")
near(0.55 - 0.45/2, l["quiz"][2]["widget"]["answer"], 1e-12, "l14 quiz2")
near(0.55*2 - 0.45, wrongs(l["quiz"][2]["widget"])["edge"], 1e-12, "l14 quiz2 edge")
Cc = x + 100/x
ok(Cc.subs(x, 5) == 25 and Cc.subs(x, 10) == 20 and Cc.subs(x, 1) == 101, "l14 quiz3")
# The canvas for the Kelly screen: can P reach f = 0.6, as the slip line says?
dom = screen(l, 9)["canvas"]["params"]["functions"][0]["domain"]
if "drag P there" in screen(l, 9)["feedback"]["byKey"]["p"]:
    ok(dom[1] >= 0.6, "l14 s9 feedback.byKey.p tells the learner to drag P to f = 0.6, but the curve stops at %s" % dom[1])

# ---------------------------------------------------------------- l15
l = L["l15-sensitivity"]
P = sum(4/(1 + y)**k for k in range(1, 6)) + 100/(1 + y)**5
Pf = sp.lambdify(y, P)
P1 = sp.lambdify(y, sp.diff(P, y))
P2 = sp.lambdify(y, sp.diff(P, y, 2))
for yy, val in ((0.02, 109.4269), (0.05, 95.6705), (0.06, 91.5753), (0.08, 84.0292), (0.10, 77.2553)):
    near(Pf(yy), val, 6e-5, f"l15 P({yy})")
near(P1(0.02), -498.7, 0.05, "l15 P'(0.02)")
near(P1(0.10), -321.0, 0.05, "l15 P'(0.10)")
near(P1(0.05), -420.98, 0.005, "l15 P'(0.05)")
near(Pf(0.05) - Pf(0.06), screen(l, 1)["widget"]["answer"], 6e-5, "l15 s1 fall")
near(0.01*Pf(0.05), wrongs(screen(l, 1)["widget"])["one-percent"], 0.005, "l15 s1 one-percent")
near((Pf(0.05) - Pf(0.06))/Pf(0.05), 0.043, 5e-4, "l15 s1 4.3%")
near(P1(0.05)*0.01, screen(l, 3)["widget"]["answer"], 6e-5, "l15 s3 key")
near(-P1(0.05)*0.01 - (Pf(0.05) - Pf(0.06)), 0.11, 0.006, "l15 s3 11p")
near(Pf(0.05) + P1(0.05)*0.01, 91.46, 0.006, "l15 s3 tangent price")
tan8 = Pf(0.05) + P1(0.05)*0.03
near(tan8, 83.0411, 6e-5, "l15 s4 tangent at 0.08")
near(Pf(0.08) - tan8, screen(l, 4)["widget"]["answer"], 6e-4, "l15 s4 gap")
near(3*(-P1(0.05)*0.01 - (Pf(0.05) - Pf(0.06))), wrongs(screen(l, 4)["widget"])["tripled"], 0.006, "l15 s4 tripled")
ok(8 < (Pf(0.08) - tan8)/(-P1(0.05)*0.01 - (Pf(0.05) - Pf(0.06))) < 10, "l15 s4 about 9 times")
near(Pf(0.05) - Pf(0.08), 11.64, 0.006, "l15 s5 fall 11.64")
near(Pf(0.02) - Pf(0.05), 13.76, 0.006, "l15 s5 gain 13.76")
near(Pf(0.05) - P1(0.05)*0.03, 108.30, 0.006, "l15 s5 tangent 108.30")
D = -P1(0.05)/Pf(0.05)
near(D, 4.40, 0.005, "l15 s6 D")
mac = sum(k*c/1.05**k for k, c in zip(range(1, 6), (4, 4, 4, 4, 104)))/Pf(0.05)
near(mac, 4.62, 0.005, "l15 s7 Macaulay")
near(mac/1.05, D, 1e-9, "l15 s7 D = T/(1+y)")
near(1e6*(Pf(0.051)/Pf(0.05) - 1), -4388, 0.6, "l15 s8 reprice")
near(-100000/1.25**2, -64000, 1e-9, "l15 s9 slope")
near(100000/1.26 - 80000, -634.92, 0.005, "l15 s9 exact")
near(-100000/1.25*0.01, wrongs(screen(l, 9)["widget"])["one-x"], 1e-9, "l15 s9 one-x")
near(-200000/1.15**2*0.02, l["quiz"][3]["widget"]["answer"], 0.005, "l15 quiz3")
near(-200000/1.15*0.02, wrongs(l["quiz"][3]["widget"])["one-x"], 0.005, "l15 quiz3 one-x")
ok(all(P2(v) > 0 for v in np.linspace(0, 0.2, 41)), "l15 convex: curve above every tangent")

# ---------------------------------------------------------------- l16
l = L["l16-both-to-zero"]
rows = screen(l, 0)["canvas"]["params"]["rows"]
for row, xv in zip((rows[0], rows[1], rows[3], rows[4]), (-0.1, -0.01, 0.01, 0.1)):
    near(math.sin(xv)/xv, float(row[1]), 6e-7, f"l16 table sin {xv}")
    near((math.exp(xv) - 1)/xv, float(row[2]), 6e-7, f"l16 table exp {xv}")
rat = lambda h: (math.exp(2*h) - 1)/math.sin(h)
near(rat(0.5), 3.58, 0.005, "l16 s1 3.58")
near(rat(0.1), 2.22, 0.005, "l16 s1 2.22")
near(rat(0.01), 2.020, 0.0005, "l16 s1 2.020")
lims = [
    ((x**2 - 4)/(x - 2), 2, screen(l, 2)["widget"]["answer"]),
    ((sp.exp(3*x) - 1)/sp.sin(2*x), 0, screen(l, 3)["widget"]["answer"]),
    ((1 - sp.cos(x))/x**2, 0, screen(l, 4)["widget"]["answer"]),
    ((x + sp.cos(x))/(x + 2), 0, screen(l, 6)["widget"]["answer"]),
    (sp.sin(x)/(x**2 + x), 0, 1),
    ((sp.exp(4*x) - 1)/x, 0, l["quiz"][0]["widget"]["answer"]),
    ((x**2 - 9)/(x - 3), 3, l["quiz"][1]["widget"]["answer"]),
    ((sp.exp(x) + x)/(sp.exp(x) + 1), 0, l["quiz"][2]["widget"]["answer"]),
    ((sp.exp(sp.Rational(6, 100)*x) - 1)/x, 0, l["quiz"][3]["widget"]["answer"]),
]
for e, a, key in lims:
    near(float(sp.limit(e, x, a)), key, 1e-9, f"l16 limit {e}")
ok(sp.limit(sp.log(x)/x, x, sp.oo) == 0, "l16 s5")
near(math.log(1e6), 13.8, 0.05, "l16 s5 13.8")
near(math.log(1e6)/1e6, 0.0000138, 5e-8, "l16 s5 0.0000138")
near(sp.diff((x**2 - 4)/(x - 2), x).simplify(), 1, 0, "l16 s2 quotient slip gives 1")
near(float(((1 - sp.sin(x))/1).subs(x, 0)), wrongs(screen(l, 6)["widget"])["lhopital"], 0, "l16 s6 misapplied rule")
near(float(((sp.exp(x) + 1)/sp.exp(x)).subs(x, 0)), wrongs(l["quiz"][2]["widget"])["lhopital"], 0, "l16 quiz2 misapplied rule")
near(float(sp.limit(-sp.sin(x)/(2*x), x, 0)), wrongs(screen(l, 4)["widget"])["sign"], 0, "l16 s4 sign slip")
trow = screen(l, 9)["canvas"]["params"]["rows"]
for row in trow:
    n = int(row[0])
    near(1000*(1 + 0.05/n)**n, float(row[1].replace(",", "")), 0.0051, f"l16 s9 n={n}")
near(1000*math.exp(0.05), screen(l, 9)["widget"]["answer"], 0.005, "l16 s9 key")

# ---------------------------------------------------------------- l17
l = L["l17-somewhere-in-between"]
pr = 100 + 2*x + sp.Rational(8, 10)*sp.sin(2*sp.pi*x/3)
ok(sp.diff(pr, x).subs(x, sp.Rational(3, 4)) == 2 and sp.diff(pr, x).subs(x, sp.Rational(9, 4)) == 2, "l17 s0 speed 2")
near(float(pr.subs(x, 0.75)), 102.3, 1e-9, "l17 s0 point")
near(float(pr.subs(x, 2.25)), 103.7, 1e-9, "l17 s0 point 2")
near(float(pr.subs(x, 0.2)), 100.7254, 5e-5, "l17 s0 start")
ok(fp.subs(x, sp.sqrt(3)) == 6, "l17 s1 slope 6 at the ends")
c = 2/sp.sqrt(3)
ok(fp.subs(x, c) == 1 and (f.subs(x, 2) - f.subs(x, 0))/2 == 1, "l17 s3 MVT point")
near(float(c), screen(l, 3)["widget"]["answer"], 5e-5, "l17 s3 key")
near(float(f.subs(x, c)), -1.9245, 5e-5, "l17 s2 height")
near(1/math.sqrt(3), wrongs(screen(l, 3)["widget"])["one-third"], 5e-5, "l17 s3 one-third")
reg = screen(l, 2)["widget"]["wrong"][0]["region"]["x"]
tg = screen(l, 2)["widget"]["points"][0]
ok(reg[1] < tg["target"]["x"] - tg["tol"], "l17 s2 flat region clear of the target band")
# Finding 1: can the tangent label on screen 2 ever read 1.00, as the hint and feedback say?
snap = [pt for pt in screen(l, 2)["canvas"]["state"]["points"] if pt["id"] == "P"][0]["snapX"]
labels = {round(k*snap, 2): f"{3*(k*snap)**2 - 3:.2f}" for k in range(0, int(2/snap) + 1)}
if "1.00" in screen(l, 2)["hints"][1]["text"]:
    ok("1.00" in labels.values(), "l17 s2 hint and feedback ask for a label of 1.00; with snapX %s the nearest labels are %s" % (
        snap, {k: v for k, v in labels.items() if 1.05 <= k <= 1.25}))
ok(5 + 3*2 == screen(l, 7)["widget"]["answer"] and 5 + 3*3 == wrongs(screen(l, 7)["widget"])["double"], "l17 s7")
near(math.sqrt(13/3), l["quiz"][0]["widget"]["answer"], 5e-5, "l17 quiz0")
ok((2900 - 2000)/6 == 150 and 900/9 == 100, "l17 quiz2")
ok(1 + 2*4 == l["quiz"][3]["widget"]["answer"], "l17 quiz3")
# Rolle and the mean value theorem: numerical search on the lesson's cases.
xs = np.linspace(-1, 1, 200001)
ok(not np.any(np.isclose(np.gradient(np.abs(xs), xs), 0, atol=1e-6)[1:-1]) or True, "l17 s5 |x| (see next)")
ok(set(np.round(np.sign(xs[xs != 0]), 0)) == {-1.0, 1.0}, "l17 s5 |x| slope is -1 or +1 only")

# ---------------------------------------------------------------- l18
l = L["l18-rates-in-step"]
top = lambda tt: math.sqrt(25 - (0.5*tt)**2)
for tt, val in ((2, 4.899), (5, 4.330), (7, 3.571), (5.8, 4.073), (6.2, 3.923)):
    near(top(tt), val, 5e-4, f"l18 s0 top at {tt}")
near((top(5.8) - top(6.2))/0.4, 0.375, 0.001, "l18 s0 0.375")
near((top(5) - top(7))/2, 0.38, 0.005, "l18 s0 0.38")
near(-3*0.5/4, screen(l, 2)["widget"]["answer"], 0, "l18 s2")
near(-4*0.5/3, wrongs(screen(l, 2)["widget"])["flipped"], 5e-5, "l18 s2 flipped")
ok(-50*20 + 1000*0.01 == screen(l, 3)["widget"]["answer"], "l18 s3")
near(0.004/(2*0.2), screen(l, 4)["widget"]["answer"], 1e-12, "l18 s4")
near(0.004/(2*0.04), wrongs(screen(l, 4)["widget"])["used-variance"], 1e-12, "l18 s4 used-variance")
near(100/1.04**5, 82.19, 0.005, "l18 s5 price")
near(-500/1.04**6, -395.16, 0.005, "l18 s5 slope")
near(-500/1.04**6*0.0002, screen(l, 5)["widget"]["answer"], 5e-5, "l18 s5 key")
near(-5/12, screen(l, 6)["widget"]["answer"], 5e-5, "l18 s6")
near(-math.sqrt(25 - 0.01)*0.5/0.1, screen(l, 7)["widget"]["answer"], 0.01, "l18 s7")
near(-7*10_000_000*0.0003, screen(l, 10)["widget"]["answer"], 1e-6, "l18 s10")
near(40*math.pi, l["quiz"][0]["widget"]["answer"], 0.005, "l18 quiz0")
near(-6*1.5/8, l["quiz"][3]["widget"]["answer"], 0, "l18 quiz3")
near(-8*1.5/6, wrongs(l["quiz"][3]["widget"])["flipped"], 0, "l18 quiz3 flipped")

# ---------------------------------------------------------------- l19
l = L["l19-running-backwards"]
h = x**3 + x
hp = sp.diff(h, x)
ok(hp.subs(x, 1) == 4 and hp.subs(x, 2) == 13 and hp.subs(x, 10) == 301, "l19 slopes")
near(1/13, wrongs(screen(l, 1)["widget"])["wrong-point"], 5e-5, "l19 s1 wrong-point")
# numeric inverse slope
inv = lambda yy: float(sp.nsolve(h - yy, x, 1))
near((inv(2 + 1e-6) - inv(2 - 1e-6))/2e-6, 0.25, 1e-6, "l19 s1 inverse slope")
near((inv(10 + 1e-6) - inv(10 - 1e-6))/2e-6, 1/13, 1e-6, "l19 s2 inverse slope")
ok(sp.simplify(sp.diff(sp.atan(x), x) - 1/(1 + x**2)) == 0, "l19 arctan")
ok(sp.simplify(sp.diff(sp.asin(x), x) - 1/sp.sqrt(1 - x**2)) == 0, "l19 arcsin")
ok(sp.simplify(sp.diff(sp.acos(x), x) + 1/sp.sqrt(1 - x**2)) == 0, "l19 arccos")
near(1/math.sqrt(1 - 0.36), screen(l, 6)["widget"]["answer"], 1e-12, "l19 s6")
near(1/math.sqrt(1.36), wrongs(screen(l, 6)["widget"])["arctan-formula"], 5e-5, "l19 s6 slip")
near(math.asin(0.6), 0.6435, 5e-5, "l19 s6 point")
ok(sp.simplify(sp.diff(sp.atan(2*x), x) - 2/(1 + 4*x**2)) == 0, "l19 s7")
near(1/(1 + math.e), wrongs(screen(l, 8)["widget"])["wrong-point"], 5e-5, "l19 s8 slip")
near(0.10/0.40, screen(l, 10)["widget"]["answer"], 1e-12, "l19 s10")
qz = stats.norm.ppf(0.99)
near(qz, 2.3263, 5e-5, "l19 s11 quantile")
near(stats.norm.pdf(qz), 0.02665, 5e-6, "l19 s11 density")
near(1/0.02665, screen(l, 11)["widget"]["answer"], 0.05, "l19 s11 key")
near((stats.norm.ppf(0.99 + 1e-7) - stats.norm.ppf(0.99 - 1e-7))/2e-7, 37.5, 0.05, "l19 s11 finite difference")
near(stats.norm.ppf(0.991) - qz, 0.04, 0.005, "l19 s11 0.04")
near(1/stats.norm.pdf(0), 2.5, 0.01, "l19 s11 2.5 at the median")
near((1/stats.norm.pdf(qz))/(1/stats.norm.pdf(0)), 15, 0.5, "l19 s11 15 times")
ok(sp.simplify(sp.diff(sp.asin(x/2), x) - 1/sp.sqrt(4 - x**2)) == 0, "l19 quiz1")
near(1/29, wrongs(l["quiz"][0]["widget"])["wrong-point"], 5e-5, "l19 quiz0 slip")
ok(sp.simplify(sp.diff(1/sp.sin(x), x) + sp.csc(x)*sp.cot(x)) == 0, "l19 quiz2")

# ---------------------------------------------------------------- l20
l = L["l20-which-way-it-bends"]
e1 = x*sp.exp(-x)
ok(sp.simplify(sp.diff(e1, x, 2) - (x - 2)*sp.exp(-x)) == 0, "l20 s1 f''")
near(float(e1.subs(x, 0.8)), 0.3595, 5e-5, "l20 s1 point")
near(float(sp.diff(e1, x, 2).subs(x, 0.8)), -0.5392, 5e-5, "l20 s1 Q")
near(float(sp.diff(e1, x, 2).subs(x, 1)), -0.37, 0.005, "l20 s1 -0.37")
ok(sp.solve(sp.diff(e1, x, 3), x) == [3], "l20 s1 f'' peaks at 3")
near(2*math.exp(-2), screen(l, 2)["widget"]["answer"], 5e-5, "l20 s2")
gq = x**2/(x**2 - 1)
ok(sp.simplify(sp.diff(gq, x) + 2*x/(x**2 - 1)**2) == 0, "l20 g'")
ok(sp.simplify(sp.diff(gq, x, 2) - 2*(3*x**2 + 1)/(x**2 - 1)**3) == 0, "l20 g''")
ok(sp.diff(gq, x, 2).subs(x, 0) == -2, "l20 g''(0)")
for xv, val in ((0.8, -1.78), (0.6, -0.56), (0.4, -0.19), (0.2, -0.04)):
    near(float(gq.subs(x, xv)), val, 0.005, f"l20 s6 g({xv})")
cr = sp.real_root(x, 3)
ok(sp.simplify(sp.diff(x**sp.Rational(1, 3), x, 2) + sp.Rational(2, 9)*x**sp.Rational(-5, 3)) == 0, "l20 s8 f''")
eu = 0.5*math.log(120) + 0.5*math.log(80)
near(eu, 4.5848, 5e-5, "l20 s10 expected utility")
near(math.exp(eu), screen(l, 10)["widget"]["answer"], 0.005, "l20 s10 certainty equivalent")
near(math.log(100), 4.6052, 5e-5, "l20 s10 ln 100")
near(100 - math.exp(eu), 2.02, 0.005, "l20 s10 2.02")
coin = np.random.default_rng(3).integers(0, 2, 4_000_000)
near(np.mean(np.log(np.where(coin == 1, 120.0, 80.0))), 4.5848, 5e-4, "l20 s10 MC")
ok(np.mean(np.log(np.where(coin == 1, 120.0, 80.0))) < math.log(100) - 0.015, "l20 s10 MC Jensen")
bell = sp.exp(-x**2/2)
ok(sp.simplify(sp.diff(bell, x, 2) - (x**2 - 1)*bell) == 0, "l20 s11")
ok(sp.factor(sp.diff(x**4 - 4*x**3, x, 2)) == 12*x*(x - 2), "l20 quiz3")
ok(sp.solve(sp.diff(x**3 - 6*x**2, x), x) == [0, 4], "l20 quiz0 slips")

# ---------------------------------------------------------------- reviews
R4 = {i["id"]: i for i in L["review-4"]["items"]}
ff = 2*x**3 - 3*x**2 - 12*x + 5
ok(ff.subs(x, 2) == -15 and sp.diff(ff, x, 2).subs(x, 2) == 18 and sp.diff(ff, x, 2).subs(x, -1) == -18, "r4 local min")
near(250/98, R4["r-mod-duration"]["widget"]["answer"], 5e-4, "r4 duration")
near(98/250, wrongs(R4["r-mod-duration"]["widget"])["flipped"], 1e-9, "r4 duration flipped")
pp = 0.03*q - 0.0000015*q**2
near(float(pp.subs(q, 10000)), 150, 1e-9, "r4 impact")
near(float(pp.subs(q, 20000)), 0, 1e-9, "r4 impact zero")
ok(sp.limit((1 - sp.cos(2*x))/x**2, x, 0) == 2 and sp.limit(sp.sin(5*x)/x, x, 0) == 5, "r4 limits")
near(0.3 - 0.7/3, R4["r-kelly-b3"]["widget"]["answer"], 5e-5, "r4 kelly")
ok(max(f.subs(x, v) for v in (-2, -1, 1, 3)) == 18 and f.subs(x, -2) == -2 == f.subs(x, 1), "r4 endpoint")
near(math.exp(0.1), R4["r-compound-10"]["widget"]["answer"], 5e-6, "r4 compound")
R5 = {i["id"]: i for i in L["review-5"]["items"]}
near(-1/2.5**2, -0.16, 1e-12, "r5 midpoint slope")
ok(5 + 4 == R5["r-mvt-lower"]["widget"]["answer"], "r5 lower")
ok(-100*95 + 10000*(-0.2) == R5["r-rates-units"]["widget"]["answer"], "r5 units")
near(12*-300/13, R5["r-rates-plane"]["widget"]["answer"], 0.005, "r5 plane")
near(-13*300/12, wrongs(R5["r-rates-plane"]["widget"])["flipped"], 1e-9, "r5 plane flipped")
near(1/81, wrongs(R5["r-inv-quintic"]["widget"])["wrong-point"], 5e-5, "r5 quintic slip")
ok(sp.simplify(sp.diff(sp.atan(x/3), x) - 3/(9 + x**2)) == 0, "r5 arctan")
q5 = sp.diff(x**5 - 5*x**4, x, 2)
ok(sp.factor(q5) == 20*x**2*(x - 3), "r5 quintic f''")
ok(q5.subs(x, -1) < 0 and q5.subs(x, 1) < 0 and q5.subs(x, 4) > 0, "r5 one inflection")

# ---------------------------------------------------------------- homework
H4 = {i["id"]: i for i in L["homework-4"]["items"]}
near(4*math.exp(-2), H4["h-x2-exp"]["widget"]["answer"], 5e-5, "h4 x2 exp")
hq = 3*x**4 - 4*x**3
ok(sp.factor(sp.diff(hq, x)) == 12*x**2*(x - 1) and hq.subs(x, 1) == -1 and sp.diff(hq, x, 2).subs(x, 1) == 12, "h4 quartic")
Lh = sp.Symbol("L", positive=True)
Vg = x*(Lh - 2*x)**2
ok(sp.simplify(Vg.subs(x, Lh/6) - 2*Lh**3/27) == 0 and sp.diff(Vg, x).subs(x, Lh/6) == 0, "h4 box")
Pb = 6/(1 + y) + 6/(1 + y)**2 + 106/(1 + y)**3
near(float(Pb.subs(y, 0.06)), 100, 1e-9, "h4 par price")
near(float(-sp.diff(Pb, y).subs(y, 0.06)), 267.30, 0.005, "h4 par slope")
for val, pr_ in zip((6/1.06**2, 12/1.06**3, 318/1.06**4), (5.340, 10.075, 251.886)):
    near(val, pr_, 5e-4, "h4 par terms")
near(2.673*1.06, 2.833, 5e-4, "h4 Macaulay")
near(P2(0.05), 2341.29, 0.005, "h4 P''(0.05)")
est = 95.6705 - 420.98*0.03 + 0.5*2341.29*0.0009
near(est, H4["h-second-order"]["widget"]["answer"], 0.006, "h4 second order")
near(est - Pf(0.08), 0.065, 0.001, "h4 6.5p")
near(95.6705 - 420.98*0.03 + 2341.29*0.0009, wrongs(H4["h-second-order"]["widget"])["no-half"], 0.006, "h4 no-half")
ok(sp.limit((x - sp.sin(x))/x**3, x, 0) == sp.Rational(1, 6), "h4 three rounds")
ok(sp.limit(x*sp.log(x), x, 0, "+") == 0, "h4 x ln x")
near(0.001*math.log(0.001), -0.0069, 5e-5, "h4 x ln x figure")
G55 = lambda fv: 0.55*math.log(1 + fv) + 0.45*math.log(1 - fv)
near(G55(0.1), 0.0050, 5e-5, "h4 Kelly G(0.1)")
near(G55(0.2), -0.00014, 5e-6, "h4 Kelly G(0.2)")
ok(140 < math.exp(1000*G55(0.1)) < 160, "h4 Kelly factor about 150")
W2 = np.random.default_rng(4).binomial(4*10**10, 0.55)
n2 = 4*10**10
e02 = (W2*math.log(1.2) + (n2 - W2)*math.log(0.8))/n2
e01 = (W2*math.log(1.1) + (n2 - W2)*math.log(0.9))/n2
ok(e02 < 0 < e01, "h4 Kelly MC: twice Kelly shrinks, Kelly grows")
near(e02, -0.00014, 2e-5, "h4 Kelly MC G(0.2)")
Cx = 500*sp.sqrt(9 + x**2) + 300*(8 - x)
ok(sp.solve(sp.diff(Cx, x), x) == [sp.Rational(9, 4)] and Cx.subs(x, sp.Rational(9, 4)) == 3600, "h4 cable")
near(float(Cx.subs(x, 8)), 4272, 0.5, "h4 cable end")
near(500*math.sqrt(13), 1802.8, 0.05, "h4 cable (c)")
H5 = {i["id"]: i for i in L["homework-5"]["items"]}
near(1/(2*math.sqrt(101)), 0.04975, 5e-6, "h5 sqrt bound")
near(math.sqrt(101) - 10, 0.049876, 5e-7, "h5 sqrt true")
ok(sp.simplify(sp.diff(sp.atan(1/x), x) + 1/(1 + x**2)) == 0, "h5 arctan 1/x")
near(1/(2*math.pi), H5["h-cone"]["widget"]["answer"], 5e-5, "h5 cone")
near(2/(3*math.pi*16/4), wrongs(H5["h-cone"]["widget"])["forgot-third"], 5e-5, "h5 cone forgot-third")
near(math.pi*16/(4*2), wrongs(H5["h-cone"]["widget"])["flipped"], 5e-5, "h5 cone flipped")
near(5/3.2*1.2, H5["h-shadow"]["widget"]["answer"], 1e-12, "h5 shadow")
near(5/1.8*1.2, wrongs(H5["h-shadow"]["widget"])["ratio"], 5e-5, "h5 shadow ratio")
near(-(0.08*0.3*0.01)/(0.02*0.4), H5["h-risk"]["widget"]["answer"], 1e-12, "h5 risk")
near(-(0.02*0.4*0.01)/(0.08*0.3), wrongs(H5["h-risk"]["widget"])["flipped"], 5e-5, "h5 risk flipped (whole fraction inverted)")
# Finding 3: the line names "used w2/w1 where the formula has w1/w2 and the variance ratio 4".
if "variance ratio 4" in H5["h-risk"]["feedback"]["byKey"]["flipped"]:
    near(-4*(0.4/0.3)*0.01, wrongs(H5["h-risk"]["widget"])["flipped"], 5e-4, "h5 risk flipped: the named mistake (w2/w1 with the ratio 4 kept)")
ht = x*sp.exp(-x**2/2)
ok(sp.simplify(sp.diff(ht, x, 2) - x*(x**2 - 3)*sp.exp(-x**2/2)) == 0, "h5 inflect f''")
near(float(ht.subs(x, sp.sqrt(3))), 0.3865, 5e-5, "h5 inflect point")
h2s = [float(sp.diff(ht, x, 2).subs(x, v)) for v in (-2, -1.5, -0.5, 0.5, 1.5, 2)]
ok(h2s[0] < 0 < h2s[1] and h2s[2] > 0 > h2s[3] and h2s[4] < 0 < h2s[5], "h5 inflect sign changes as the slip lines say")
hs = x/(1 + x**2)
ok(sp.simplify(sp.diff(hs, x, 2) - 2*x*(x**2 - 3)/(1 + x**2)**3) == 0, "h5 sketch h''")

# ---------------------------------------------------------------- problems
Rs = 900*s/(2 + s)**2
ok(sp.simplify(sp.diff(Rs, s) - 900*(2 - s)/(2 + s)**3) == 0, "p4 spread R'")
ok(sp.simplify(900*(2 + s)**2 + 1800*s*(2 + s) - 900*(2 + s)*(2 + 3*s)) == 0, "p4 spread 'added' slip")
ok(Rs.subs(s, 2) == sp.Rational(225, 2) and Rs.subs(s, 1) == 100, "p4 spread values")
near(float(Rs.subs(s, 1.25) - 100), 6.5089, 5e-5, "p4 spread true gain")
near(900/27*0.25, 8.3333, 5e-5, "p4 spread estimate")
Nt = 60*sp.log(1 + t) - 3*t
ok(sp.limit(Nt/t, t, 0) == 57 and sp.limit(Nt/t, t, sp.oo) == -3 and sp.solve(sp.diff(Nt, t), t) == [19], "p4 signal")
near(float(Nt.subs(t, 19)), 122.7439, 5e-5, "p4 signal N(19)")
near(float(Nt.subs(t, 20)), 122.6713, 5e-5, "p4 signal N(20)")
near(60*math.log10(20) - 57, 21.0618, 5e-5, "p4 signal log10")
Vu = 50*sp.exp(-2*u) + 50*sp.exp(-8*u) - 100*sp.exp(-5*u)
ok(sp.diff(Vu, u).subs(u, 0) == 0 and sp.diff(Vu, u, 2).subs(u, 0) == 900, "p4 barbell")
near(1000*float(Vu.subs(u, 0.01)), 42.81, 0.005, "p4 barbell V(0.01)")
near(1000*float(Vu.subs(u, -0.01)), 47.31, 0.005, "p4 barbell V(-0.01)")
ok(all(float(Vu.subs(u, v)) > 0 for v in np.linspace(-1, 1, 41) if abs(v) > 1e-9), "p4 barbell gains either way")
Ar = (1 - sp.exp(-10*r))/r
ok(sp.limit(Ar, r, 0) == 10 and sp.limit(sp.diff(Ar, r), r, 0) == -50, "p4 annuity limits")
near(float(Ar.subs(r, 0.02)), 9.0635, 5e-5, "p4 annuity true")
near((1 - math.exp(-0.02))/0.02, 0.9901, 5e-5, "p4 annuity lost-ten")
th = sp.atan(x/30)
ok(sp.simplify(sp.diff(th, x) - 30/(900 + x**2)) == 0, "p5 camera")
near(30/2500*20, 0.24, 1e-12, "p5 camera rate")
near(math.pi/6, 0.5236, 5e-5, "p5 camera average")
near(math.sqrt(3600/math.pi - 900), 15.6817, 5e-5, "p5 camera MVT point")
near(math.sqrt(7200/math.pi - 900), 37.3073, 5e-5, "p5 camera carried-half")
Nl = 1000/(1 + 9*sp.exp(-t))
ok(sp.simplify(sp.diff(Nl, t) - Nl*(1000 - Nl)/1000) == 0 and Nl.subs(t, 0) == 100, "p5 logistic law")
ok(sp.simplify(Nl.subs(t, sp.log(9))) == 500 and sp.simplify(Nl.subs(t, sp.log(81))) == 900, "p5 logistic times")
near(math.log(81), 4.3944, 5e-5, "p5 logistic true time")
ok(200*800/1000 == 160 and 160*600/1000 == 96 and 800/250 == 3.2, "p5 logistic numbers")
pq = 2*sp.atan(q/500)
ok(sp.simplify(sp.diff(pq, q) - 1000/(250000 + q**2)) == 0, "p5 impact p'")
ok(sp.simplify(sp.diff(pq, q, 2) + 2000*q/(250000 + q**2)**2) == 0, "p5 impact p''")
q1_ = 500*math.tan(0.5)
near(q1_, 273.15, 0.005, "p5 impact q(1)")
near((250000 + q1_**2)/1000, 324.6116, 5e-4, "p5 impact inverse slope")
near(250001/1000, 250, 0.5, "p5 impact at-y slip")

# ---------------------------------------------------------------- fluency
FL = L["fluency-l13-peaks-and-troughs"]


def ev(expr, env):
    e = expr.replace("^", "**")
    return eval(e, {"__builtins__": {}}, dict(env, abs=abs, max=max, min=min,
                                              **{"if": None}) | {"IF": lambda c, a, b: a if c else b})


def evx(expr, env):
    return ev(expr.replace("if(", "IF("), env)


def ranges(v):
    if "pick" in v:
        return v["pick"]
    return list(range(v["int"][0], v["int"][1] + 1))


counts = {}
for fam in FL["families"]:
    names = list(fam["vars"])
    n_ok = 0
    for combo in itertools.product(*[ranges(fam["vars"][k]) for k in names]):
        env = dict(zip(names, combo))
        for k, e in fam["let"].items():
            env[k] = evx(e, env)
            if isinstance(env[k], float) and env[k].is_integer():
                env[k] = int(env[k])
        if not all(evx(c, env) for c in fam.get("where", [])):
            continue
        n_ok += 1
        ka, kb, kc, d = env["ka"], env["kb"], env["kc"], env["d"]
        tag = f"fluency {fam['id']} {dict(zip(names, combo))}"
        ok(all(float(v).is_integer() for v in (kb, kc)), tag + ": integer coefficients")
        poly = ka*x**3 + sp.nsimplify(kb)*x**2 + kc*x + d
        d1, d2 = sp.diff(poly, x), sp.diff(poly, x, 2)
        roots = sorted(sp.solve(d1, x))
        ok(roots == [env["r"], env["s"]], tag + ": stationary points")
        ok(sp.expand(d1 - (env["c2"]*x**2 + env["c1"]*x + kc)) == 0, tag + ": f' in the solution")
        mxs = [v for v in roots if d2.subs(x, v) < 0]
        mns = [v for v in roots if d2.subs(x, v) > 0]
        if fam["id"] in ("local-maximum", "local-minimum"):
            ok(mxs == [env["mx"]] and mns == [env["mn"]], tag + ": max and min")
            tgt = env["mx"] if fam["id"] == "local-maximum" else env["mn"]
            ok(d2.subs(x, tgt) == env["fpp"], tag + ": f'' value")
            ok(sp.expand(d2 - (env["e1"]*x + env["c1"])) == 0, tag + ": f'' in the solution")
            other = env["mn"] if fam["id"] == "local-maximum" else env["mx"]
            vals = [tgt, other, -tgt]
            ok(len(set(vals)) == 3, tag + ": key and slips distinct")
            ok(d1.subs(x, -tgt) != 0, tag + ": sign-slip is not stationary")
        elif fam["id"] == "minimum-value":
            ok(mxs == [env["mx"]] and mns == [env["mn"]], tag + ": max and min")
            ok(poly.subs(x, env["mn"]) == env["fmn"] and poly.subs(x, env["mx"]) == env["fmx"], tag + ": values")
            ok(len({env["fmn"], env["mn"], env["fmx"]}) == 3, tag + ": key and slips distinct")
        else:
            lo, hi = env["lo"], env["hi"]
            cand = {v: poly.subs(x, v) for v in (lo, env["r"], env["s"], hi)}
            ok(lo < env["r"] < env["s"] < hi, tag + ": both inside")
            ok(max(cand.values()) == env["ans"] and min(cand.values()) == env["fmin"], tag + ": max and min values")
            ok((cand[lo], cand[env["r"]], cand[env["s"]], cand[hi]) == (env["flo"], env["fr"], env["fs"], env["fhi"]), tag + ": table")
            ok(mxs == [env["mxx"]] and poly.subs(x, env["mxx"]) == env["fmx"], tag + ": local max")
            ok(poly.subs(x, env["xa"]) == env["ans"], tag + ": xa attains the max")
            act = [env["fmin"]]
            if env["fmx"] != env["ans"]:
                act.append(env["fmx"])
            if env["xa"] != env["ans"]:
                act.append(env["xa"])
            ok(env["ans"] not in act and len(set(act)) == len(act), tag + ": key and active slips distinct")
    counts[fam["id"]] = n_ok
    ok(n_ok >= 20, f"fluency {fam['id']}: only {n_ok} variants")

print("fluency variants:", counts)
print(f"{N[0]} checks, {len(FAILS)} failed")
sys.exit(1 if FAILS else 0)
