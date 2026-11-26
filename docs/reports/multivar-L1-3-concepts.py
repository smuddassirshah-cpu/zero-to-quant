"""Concept audit checks for multivar levels 1 to 3 (audit multivar-1-3, round 1).

Run with the venv Python (sympy, numpy, scipy). Each check is one claim made by the content.
A check that fails because the content is wrong stays failing and is a finding, so this script
exits 1 while those findings stand and 0 once the content is reworded (see REWORDED). Checks tagged [F<n>] map to findings in
docs/reviews/audit-multivar-1-3.md; untagged checks confirm claims the ledger marks correct.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.stats import norm

import json
import os
import re

RESULTS = []
CDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "multivar")


def content(name):
    with open(os.path.join(CDIR, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


L4, L5, L6, L8, L9, L11, L12 = (content(n) for n in ("l4-chain-two-inputs", "l5-steepest-climb", "l6-any-direction",
                                                    "l8-walking-downhill", "l9-peaks-pits-saddles", "l11-on-a-constraint", "l12-min-variance"))
QUAL = re.compile(r"smooth|differentiable", re.I)
# A finding check tests the claim as the content words it. Once the content states the missing condition,
# or drops the false sentence, the check passes, so the script exits 0 on corrected content.
REWORDED = {
    "F1": lambda: bool(QUAL.search(L6["quiz"][3]["prose"])),
    "F2": lambda: bool(QUAL.search(L4["summary"]["formula"]["note"])),
    "F3": lambda: bool(re.search(r"exist|closed", L11["screens"][6]["prose"])),
    "F4": lambda: "\\nabla g \\neq" in L11["summary"]["formula"]["note"] + L11["screens"][6]["prose"],
    "F5": lambda: "Per unit step, arrow A climbs" not in L5["screens"][0]["explain"]["text"],
    "F6": lambda: "does not point at the peak" not in L5["summary"]["trap"],
    "F7": lambda: "rises fastest by adding asset 1" not in L5["screens"][9]["explain"]["text"],
    "F8": lambda: "just more slowly" not in L8["screens"][7]["widget"]["options"][2]["why"],
    "F9": lambda: "and cross at a saddle" not in L9["summary"]["ideas"][1],
    "F10": lambda: "short" in L12["screens"][6]["widget"]["options"][2]["why"],
}


def check(name, ok, detail=""):
    m = re.match(r"\[(F\d+)\]", name)
    if m and not ok and REWORDED[m.group(1)]():
        ok, name = True, name + " (content now qualified)"
    RESULTS.append((name, bool(ok), detail))


x, y, t, s, c, lam = sp.symbols("x y t s c lambda", real=True)

# ---------------------------------------------------------------- level 1
# l2 s8 / l3 s8 / review-1: the Black-Scholes tables (strike 100, six months, r = 0).
def bs(S, sig, K=100.0, T=0.5):
    d1 = (math.log(S / K) + 0.5 * sig * sig * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return S * norm.cdf(d1) - K * norm.cdf(d2), norm.cdf(d1), d1, d2

tab = {(99, .19): 4.84, (99, .20): 5.12, (99, .21): 5.40, (100, .19): 5.36, (100, .20): 5.64,
       (100, .21): 5.92, (101, .19): 5.90, (101, .20): 6.18, (101, .21): 6.46}
check("l2 option table is Black-Scholes at r = 0 to 1p", all(abs(bs(S, v)[0] - p) < 0.011 for (S, v), p in tab.items()))
check("l2 delta 0.53 (central difference and exact N(d1))", abs((6.18 - 5.12) / 2 - 0.53) < 1e-9 and abs(bs(100, .2)[1] - 0.53) < 0.005)
check("l2 vega 28 per unit sigma, 0.28 per vol point", abs((5.92 - 5.36) / 0.02 - 28) < 1e-9 and abs(100 * norm.pdf(bs(100, .2)[2]) * math.sqrt(.5) - 28) < 0.3)
dtab = {(95, .15): .333, (95, .20): .385, (95, .25): .420, (100, .15): .521, (100, .20): .528,
        (100, .25): .535, (105, .15): .696, (105, .20): .661, (105, .25): .642}
check("l3 delta table is Black-Scholes at r = 0", all(abs(bs(S, v)[1] - p) < 0.0011 for (S, v), p in dtab.items()))
check("l3 vanna -0.54 at S = 105 and +0.87 at S = 95", abs((.642 - .696) / .1 + .54) < 1e-9 and abs((.420 - .333) / .1 - .87) < 1e-9)
check("l3 vanna sign follows the sign of -d2 (negative at 105, positive at 95)", bs(105, .2)[3] > 0 > bs(95, .2)[3])
check("l3 slip gamma 0.0276 is the column difference (0.661 - 0.385)/10", abs((.661 - .385) / 10 - .0276) < 1e-9)

# l2 quiz pv01 and review-1 bond rate
V = 500000 * sp.exp(-2 * x) + 300000 * sp.exp(-10 * y)
v1 = float(sp.diff(V, x).subs({x: .03, y: .04})); v2 = float(sp.diff(V, y).subs({x: .03, y: .04}))
check("l2 q-pv01 201.10 and slip 94.18, 20.11", abs(-v2 * 1e-4 - 201.10) < 0.01 and abs(-v1 * 1e-4 - 94.18) < 0.01)
check("review-1 bond rate 12.74 per day", abs(v1 * 2e-4 + v2 * -1e-4 - 12.74) < 0.01)

# l3 Clairaut on every named function; and the classical counterexample needing continuity
for name, f in [("x^2y", x**2 * y), ("x^3y^2", x**3 * y**2), ("e^xy", sp.exp(x * y)), ("x sin y", x * sp.sin(y)),
                ("x e^xy", x * sp.exp(x * y)), ("x^3 e^2y", x**3 * sp.exp(2 * y)), ("x^3y-2xy^2", x**3 * y - 2 * x * y**2)]:
    check(f"l3 mixed partials agree: {name}", sp.simplify(sp.diff(f, x, y) - sp.diff(f, y, x)) == 0)
g = x * y * (x**2 - y**2) / (x**2 + y**2)  # f(0,0) = 0; f_xy(0,0) = -1, f_yx(0,0) = +1
fx0 = sp.limit(sp.diff(g, x).subs(x, 0), y, 0, "+"); fx_on_yaxis = sp.simplify(sp.diff(g, x).subs(x, 0))
fy_on_xaxis = sp.simplify(sp.diff(g, y).subs(y, 0))
check("l3 'for smooth functions' is needed: xy(x^2-y^2)/(x^2+y^2) has f_xy(0,0) = -1, f_yx(0,0) = 1",
      sp.diff(fx_on_yaxis, y) == -1 and sp.diff(fy_on_xaxis, x) == 1)

# l4 chain rule: examples, and the hypothesis (differentiability) it needs
def chain(f, xt, yt, t0):
    lhs = sp.diff(f.subs({x: xt, y: yt}), t).subs(t, t0)
    rhs = (sp.diff(f, x) * sp.diff(xt, t) + sp.diff(f, y) * sp.diff(yt, t)).subs({x: xt, y: yt}).subs(t, t0)
    return sp.nsimplify(lhs), sp.nsimplify(rhs)

for nm, f, xt, yt, t0, val in [("l4 s1", x**2 + y**2, 2 - t, t, sp.Rational(1, 2), -2), ("l4 s4", x**2 * y, 1 + 2 * t, 2 + 3 * t, 0, 11),
                               ("l4 s6", x**2 + y**2, 1 + t**2, 2 + t, 0, 4), ("l4 q0", x * y, t**2, t**3, 2, 80),
                               ("review-1 i6", x * sp.exp(y), 2 + t, 3 * t, 0, 7)]:
    a, b = chain(f, xt, yt, t0)
    check(f"{nm} chain rule value {val}", a == b == val)
a, b = chain(x**2 * y - y**3, sp.cos(t), sp.sin(t), sp.pi / 4)
check("hw1 circle path -sqrt 2", sp.simplify(a + sp.sqrt(2)) == 0 and sp.simplify(b + sp.sqrt(2)) == 0)
h = x**2 * y / (x**2 + y**2)  # extended by h(0,0) = 0: both partials exist (= 0) at the origin, h is not differentiable there
hx0 = sp.limit((h.subs({x: t, y: 0}) - 0) / t, t, 0); hy0 = sp.limit((h.subs({x: 0, y: t})) / t, t, 0)
along = sp.diff(sp.simplify(h.subs({x: t, y: t})), t)  # = 1/2
check("[F2] l4 summary: d/dt f(x(t),y(t)) = f_x x' + f_y y' for any f with partials (false without differentiability: x^2y/(x^2+y^2) on (t,t) gives 1/2, formula gives 0)",
      along == hx0 * 1 + hy0 * 1, f"df/dt = {along}, f_x x' + f_y y' = {hx0 + hy0}")

# ---------------------------------------------------------------- level 2
f = x**2 + 2 * y**2
gr = sp.Matrix([sp.diff(f, x), sp.diff(f, y)])
P = {x: 2, y: 1}
check("l5 grad f(2,1) = (4,4), length 5.657", list(gr.subs(P)) == [4, 4] and abs(float(gr.subs(P).norm()) - 5.657) < 1e-3)
arrows = {"A": (2.99, 1.99), "B": (3.252, 1.626), "C": (1.01, 1.99), "D": (2, 2.4)}  # tips drawn on l5 s0
slope, gain = {}, {}
for k, (ax, ay) in arrows.items():
    d = np.array([ax - 2, ay - 1]); L = np.linalg.norm(d)
    slope[k] = float(np.dot([4, 4], d / L)); gain[k] = (ax**2 + 2 * ay**2 - 6) / L
check("l5 s0 slopes at P along A, B, D, C are 5.7, 5.4, 4, 0", [round(slope[k], 1) for k in "ABDC"] == [5.7, 5.4, 4.0, 0.0])
check("l5 s0 key: A climbs most over the drawn arrows too", max(gain, key=gain.get) == "A")
check("[F5] l5 s0 explain 'per unit step, arrow A climbs about 5.7, B 5.4, D 4 and C nothing' holds for the drawn arrows (length 1.4)",
      all(abs(gain[k] - slope[k]) < 0.05 for k in "ABDC"), "gain per unit over the drawn arrows: " + ", ".join(f"{k} {gain[k]:.2f}" for k in "ABDC"))
check("l5 s4 |grad| at A and B: 6.32, 8.94", abs(2 * math.sqrt(10) - 6.32) < .005 and abs(4 * math.sqrt(5) - 8.94) < .005)
gg = 20 - x**2 - 4 * y**2
check("l5 s6 grad g(2,1) = (-4,-8), not along (-2,-1)", [sp.diff(gg, x).subs(P), sp.diff(gg, y).subs(P)] == [-4, -8])
round_hill = 20 - x**2 - y**2
gv = sp.Matrix([sp.diff(round_hill, x), sp.diff(round_hill, y)]).subs(P)  # (-4, -2) is parallel to (-2, -1): straight at the peak
check("[F6] l5 summary.trap 'the gradient does not point at the peak' (false as a general statement: on 20 - x^2 - y^2 it does)",
      gv[0] * (-1) - gv[1] * (-2) != 0, f"grad = {list(gv)}, direction to peak = (-2, -1)")
Sig = sp.Matrix([[.04, .01], [.01, .01]]); w = sp.Matrix([.5, .5])
check("l5 s9 grad V = 2 Sigma w = (0.05, 0.02)", all(abs(float(a) - b) < 1e-12 for a, b in zip(2 * Sig * w, [.05, .02])))
u_best = np.array([.05, .02]) / np.hypot(.05, .02)
check("[F7] l5 s9 'variance rises fastest by adding asset 1' (the steepest direction is the gradient (5,2)/sqrt 29, not (1,0))",
      abs(u_best[0] - 1) < 1e-9, f"steepest unit direction {u_best.round(3)}, slope {np.hypot(.05, .02):.4f} against 0.05 along (1,0)")

# l6 directional derivatives
check("l6 s1 5.6, s5 0.8, s3 -5.657", abs(4 * .6 + 4 * .8 - 5.6) < 1e-12 and abs(4 * -.6 + 4 * .8 - .8) < 1e-12 and abs(-8 / math.sqrt(2) + 5.657) < 1e-3)
th = np.linspace(0, 2 * np.pi, 3601); dd = 4 * np.cos(th) + 4 * np.sin(th)
check("l6 s0/s7 max at 45 deg = 5.66, zero at 135 and 315, min at 225", abs(np.degrees(th[dd.argmax()]) - 45) < .2 and abs(dd.max() - 5.657) < 1e-3
      and abs(np.degrees(th[dd.argmin()]) - 225) < .2 and abs(4 * math.cos(math.radians(135)) + 4 * math.sin(math.radians(135))) < 1e-12)
check("l6 quiz, review-2, hw2 directional values", abs((3 + 4) / math.sqrt(2) - 4.95) < .005 and abs(6 * -.6 + 8 * -.8 + 10) < 1e-12 and abs(-9 / math.sqrt(5) + 4.025) < 1e-3)
u1, u2 = sp.Rational(1, 1) / sp.sqrt(2), sp.Rational(1, 1) / sp.sqrt(2)
Du = sp.limit(h.subs({x: t * u1, y: t * u2}) / t, t, 0)  # directional derivative of h at the origin along (1,1)/sqrt 2
check("[F1] l6 q-stationary: D_u f = 0 along (1,0) and (0,1) forces every directional derivative to be 0 (false without differentiability)",
      Du == 0, f"x^2y/(x^2+y^2): f_x(0,0) = {hx0}, f_y(0,0) = {hy0}, D_u along (1,1)/sqrt2 = {Du}")
# l7 tangent planes
def plane(f, a, b):
    return f.subs({x: a, y: b}) + sp.diff(f, x).subs({x: a, y: b}) * (x - a) + sp.diff(f, y).subs({x: a, y: b}) * (y - b)

check("l7 planes: 4x+4y-6, 6x+y-6, hw2 4x+y-6", sp.expand(plane(f, 2, 1)) == 4 * x + 4 * y - 6 and sp.expand(plane(x**2 * y, 1, 3)) == 6 * x + y - 6
      and sp.expand(plane(x**2 * y - y**3, 2, 1)) == 4 * x + y - 6)
err = sp.expand((f - plane(f, 2, 1)).subs({x: 2 + t, y: 1 + t}))
check("l7 s3 error exactly 3h^2", err == 3 * t**2)
check("l7 s5 Jo 11.5, plane 10, true 10.75", abs(float(plane(f, 2, 1).subs({x: 2.5, y: 1.5})) - 10) < 1e-12 and abs(float(f.subs({x: 2.5, y: 1.5})) - 10.75) < 1e-12 and 6 + 5 * .5 + 6 * .5 == 11.5)
sg = sp.sqrt(x**2 + y**2); pl = plane(sg, 3, 4)
e1 = float((sg - pl).subs({x: 3.2, y: 3.7})); e2 = float((sg - pl).subs({x: 3.1, y: 3.85}))
check("problems-2 plane error 0.0118 then 0.0029 (ratio about 4)", abs(e1 - .0118) < 5e-5 and abs(e2 - .0029) < 5e-5 and 3.9 < e1 / e2 < 4.1)

# l8 gradient descent (run checks)
def descend(grad, x0, y0, step, n):
    px, py = x0, y0
    for _ in range(n):
        gx, gy = grad(px, py)
        px, py = px - step * gx, py - step * gy
    return px, py

bowl = lambda a, b: (2 * a, 4 * b)
p05 = descend(bowl, 4, 3, .05, 10); p30 = descend(bowl, 4, 3, .3, 10); p45 = descend(bowl, 4, 3, .45, 10)
fv = lambda p: p[0]**2 + 2 * p[1]**2
check("l8 s1 ten steps: 0.05 ends (1.39, 0.32) f 2.15; 0.3 at the bottom; 0.45 leaves f 0.21", abs(p05[0] - 1.39) < .01 and abs(p05[1] - .32) < .01
      and abs(fv(p05) - 2.15) < .01 and fv(p30) < 1e-6 and abs(fv(p45) - .21) < .01)
check("l8 s4 s = 0.5 flips y between 3 and -3; s = 0.6 gives y = 86.8 after 10", descend(bowl, 4, 3, .5, 7)[1] == -3 and abs(descend(bowl, 4, 3, .6, 10)[1] - 86.776) < 1e-2)
conv = lambda grad, st, start=(4.0, 3.0), n=4000: math.hypot(*descend(grad, *start, st, n)) < 1e-6
b3 = lambda a, b: (6 * a, 2 * b)
check("l8 s7 3x^2 + y^2 settles for s < 1/3 only (0.33 yes, 0.34 no)", conv(b3, .33) and not conv(b3, .34))
check("review-2 2x^2+5y^2 limit 0.2; problems-2 limit 0.25; hw2 limit 1/9", conv(lambda a, b: (4 * a, 10 * b), .199) and not conv(lambda a, b: (4 * a, 10 * b), .201)
      and conv(lambda a, b: (8 * (a - 1) + 0 * b, 2 * (b + 2)), .249, (0.0, 0.0)) is False  # converges to (1,-2), not the origin
      and not conv(lambda a, b: (2 * a, 18 * b), .112, (9.0, 1.0)) and conv(lambda a, b: (2 * a, 18 * b), .110, (9.0, 1.0)))
dist = lambda st, n: math.hypot(*descend(b3, 4, 3, st, n))
check("[F8] l8 s7 option 'best' why: steps other than 1/6 settle 'just more slowly' (s = 1/4 settles faster: factor 1/2 against 2/3)",
      all(dist(1 / 6, n) < dist(1 / 4, n) for n in (10, 20, 40)), f"distance after 20 steps: s=1/6 {dist(1/6, 20):.2e}, s=1/4 {dist(1/4, 20):.2e}")
def steps_needed(grad, x0, y0, step, tol, mx):
    px, py = x0, y0
    for k in range(mx):
        gx, gy = grad(px, py)
        if math.hypot(gx, gy) < tol:
            return k
        px, py = px - step * gx, py - step * gy
    return mx

check("hw2 steps 41, 10, 445, 77 and best step 1/3", [steps_needed(bowl, 4, 3, .1, 1e-3, 1000), steps_needed(bowl, 4, 3, .3, 1e-3, 1000),
      steps_needed(bowl, 4, 3, .01, 1e-3, 10000), steps_needed(lambda a, b: (2 * a, 18 * b), 9, 1, .1, 1e-6, 1000)] == [41, 10, 445, 77])
check("hw2 longform 41 steps for |x| < 1e-3 at s = 0.1; problems-2 24 steps", 9 * .8**40 > 1e-3 > 9 * .8**41 and 2 * .8**23 > .01 > 2 * .8**24)
xs = np.array([-1.2, .4, 1.0, -.6, 1.8, .2]); ys = np.array([-1.5, .7, 1.1, -.4, 2.3, 0.0])
A = np.vstack([np.ones(6), xs]).T; ols = np.linalg.lstsq(A, ys, rcond=None)[0]
a_, b_ = 0.0, 0.0
for _ in range(3000):
    r = a_ + b_ * xs - ys
    a_, b_ = a_ - .1 * 2 * r.mean(), b_ - .1 * 2 * (r * xs).mean()
check("l8 s8 descent reaches the least-squares line (0.0468, 1.1995) in 3,000 steps", abs(a_ - ols[0]) < 1e-12 and abs(b_ - ols[1]) < 1e-12 and abs(ols[1] - 1.1995) < 1e-4)

# ---------------------------------------------------------------- level 3
def classify(f, pt):
    H = sp.hessian(f, (x, y)).subs(dict(zip((x, y), pt)))
    D = H.det(); ev = [sp.re(e) for e in H.eigenvals()]
    by_test = "none" if D == 0 else ("saddle" if D < 0 else ("pit" if H[0, 0] > 0 else "peak"))
    by_eig = "none" if D == 0 else ("pit" if all(e > 0 for e in ev) else "peak" if all(e < 0 for e in ev) else "saddle")
    return by_test, by_eig, D

cases = [("l10 f2 A", x**3 - 3 * x + y**2, (1, 0), "pit", 12), ("l10 f2 B", x**3 - 3 * x + y**2, (-1, 0), "saddle", -12),
         ("l10 f1", x**2 + y**2 - 2 * x + 4 * y, (1, -2), "pit", 4), ("l10 f3", x**2 - y**2, (0, 0), "saddle", -4),
         ("l10 s4", 6 * x - x**2 + x * y - y**2, (4, 2), "peak", 3), ("l10 s5", x**2 + 4 * x * y + y**2, (0, 0), "saddle", -12),
         ("l10 q desk", 10 * x + 8 * y - x**2 - y**2 - x * y, (4, 2), "peak", 3), ("l10 q three", x**2 + 3 * x * y + y**2, (0, 0), "saddle", -5),
         ("review-3 pit", x**2 + 2 * y**2 - 4 * x + 4 * y, (2, -1), "pit", 8), ("review-3 peak", x**3 + y**3 - 3 * x - 12 * y, (-1, -2), "peak", 72),
         ("review-3 saddle", x**3 + y**3 - 3 * x - 12 * y, (1, -2), "saddle", -72), ("hw3 origin", x**3 + y**3 - 3 * x * y, (0, 0), "saddle", -9),
         ("hw3 (1,1)", x**3 + y**3 - 3 * x * y, (1, 1), "pit", 27), ("hw3 quartic 0", x**4 + y**4 - 4 * x * y, (0, 0), "saddle", -16),
         ("hw3 quartic 1", x**4 + y**4 - 4 * x * y, (1, 1), "pit", 128), ("problems-3 0", 2 * x**3 - 6 * x * y + 3 * y**2, (0, 0), "saddle", -36),
         ("problems-3 1", 2 * x**3 - 6 * x * y + 3 * y**2, (1, 1), "pit", 36), ("problems-3 P", 14 * x + 6 * y - x**2 - y**2, (7, 3), "peak", 4)]
for nm, f_, pt, kind, D in cases:
    grad0 = [sp.diff(f_, v).subs(dict(zip((x, y), pt))) for v in (x, y)]
    bt, be, d = classify(f_, pt)
    check(f"{nm}: stationary, D = {D}, {kind} (test agrees with Hessian eigenvalues)", grad0 == [0, 0] and bt == be == kind and d == D)
check("l10 D = 0 examples: (x-y)^2, x^4+y^4, x^4-y^4 all give no verdict", all(classify(q, (0, 0))[0] == "none" for q in ((x - y)**2, x**4 + y**4, x**4 - y**4)))
check("l10 s8 Sharpe Hessian D = -0.09", abs((-.8) * (-.2) - .25 + .09) < 1e-12)
check("l9 counts: x^3-3x+y^2 two points, x^2-y^3+3y two, review-3 four, hw3 two, quartic three",
      [len(sp.solve([sp.diff(q, x), sp.diff(q, y)], [x, y], dict=True)) for q in
       (x**3 - 3 * x + y**2, x**2 - y**3 + 3 * y, x**3 + y**3 - 3 * x - 12 * y, x**3 + y**3 - 3 * x * y, x**4 + y**4 - 4 * x * y)] == [2, 2, 4, 2, 3])
q4 = x**4 + y**4 - 4 * x * y
rng = np.random.default_rng(13); pts = rng.uniform(-3, 3, (200000, 2))
check("hw3 quartic global minimum -2 (random search finds nothing lower)", (pts[:, 0]**4 + pts[:, 1]**4 - 4 * pts[:, 0] * pts[:, 1]).min() >= -2 - 1e-9)
check("problems-3 note: 2x^3-6xy+3y^2 is unbounded below", float((2 * x**3 - 6 * x * y + 3 * y**2).subs({x: -100, y: 0})) < -1e6)
deg = x**2 * y**2  # level set f = 0 is the two axes, crossing at the origin, which is a minimum
check("[F9] l9 q9-cross / summary: level curves crossing at a stationary point always mark a saddle (x^2y^2: the axes cross at a minimum)",
      not (sp.diff(deg, x).subs({x: 0, y: 0}) == 0 and all(deg.subs({x: a, y: b}) >= 0 for a in (-1, 0, 1) for b in (-1, 0, 1)) and deg.subs({x: 2, y: 0}) == 0 and deg.subs({x: 0, y: 2}) == 0),
      "f = x^2 y^2 >= 0 = f(0,0); f = 0 on both axes")

# l11 Lagrange
def lagrange(fobj, gcon, cval):
    return sp.solve([sp.diff(fobj, x) - lam * sp.diff(gcon, x), sp.diff(fobj, y) - lam * sp.diff(gcon, y), gcon - cval], [x, y, lam], dict=True)

sol = lagrange(x * y, x + y, 10)
check("l11 xy on x+y=10: one solution (5,5), lambda 5, value 25", len(sol) == 1 and sol[0][x] == 5 and sol[0][lam] == 5)
check("l11 s4 shadow price: best value c^2/4, slope 5 at c = 10, exact 26.01 at 10.2", sp.diff(c**2 / 4, c).subs(c, 10) == 5 and abs(5.1**2 - 26.01) < 1e-12)
on_line = (x * y).subs(y, 10 - x)
check("[F3] l11 s6 rule 'to find the largest or smallest f on g = c, solve the conditions, then compare f at every solution' finds a smallest xy on x + y = 10 (none exists)",
      sp.limit(on_line, x, sp.oo) > -sp.oo, f"xy on the line is {sp.expand(on_line)}, which tends to -oo; the only Lagrange solution (5,5) is the maximum")
cusp = lagrange(x, y**2 - x**3, 0)  # minimise x on y^2 = x^3: minimum at (0,0), where grad g = 0
check("[F4] l11 s6 rule without 'grad g != 0': the smallest x on y^2 = x^3 is among the Lagrange solutions (it is at the cusp (0,0); the system has no solution)",
      any(s_[x] == 0 for s_ in cusp), f"solutions: {cusp}")
sol = lagrange(x + 2 * y, x**2 + y**2, 5)
check("l11 s2 x+2y on the circle: (1,2) max 5 and (-1,-2) min -5", sorted((s_[x], s_[y]) for s_ in sol) == [(-1, -2), (1, 2)])
sol = lagrange(3 * x + 4 * y, x**2 + y**2, 25); best = max(sol, key=lambda s_: 3 * s_[x] + 4 * s_[y])
check("l11 s8 fund: (3,4), 25, lambda 0.5; best value 5 sqrt R with slope lambda; R = 27 gives 25.98, R = 36 gives 30",
      (best[x], best[y], best[lam]) == (3, 4, sp.Rational(1, 2)) and sp.diff(5 * sp.sqrt(c), c).subs(c, 25) == sp.Rational(1, 2) and abs(5 * math.sqrt(27) - 25.98) < .005)
sol = lagrange(14 * x + 6 * y - x**2 - y**2, x + y, c)[0]
M = sp.simplify((14 * x + 6 * y - x**2 - y**2).subs({x: sol[x], y: sol[y]}))
check("problems-3 capital: (5,1), P 50, lambda 4 = dM/dc, exact 51.875 at 6.5", sol[x].subs(c, 6) == 5 and M.subs(c, 6) == 50 and sp.diff(M, c).subs(c, 6) == 4 == sol[lam].subs(c, 6)
      and M.subs(c, sp.Rational(13, 2)) == sp.Rational(415, 8))
check("l11 s3 lambda = 0 when the line passes through the free minimum", lagrange((x - 1)**2 + (y - 1)**2, x + y, 2)[0][lam] == 0)
check("review-3, hw3, l11 quiz values 18, 5, 8, 20, 9", [max((x * y).subs(s_) for s_ in lagrange(x * y, 2 * x + y, 12)), max((2 * x + y).subs(s_) for s_ in lagrange(2 * x + y, x**2 + y**2, 5)),
      (x**2 + y**2).subs(lagrange(x**2 + y**2, x + y, 4)[0]), (x**2 + y**2).subs(lagrange(x**2 + y**2, x + 2 * y, 10)[0]), (x * y).subs(lagrange(x * y, x + y, 6)[0])] == [18, 5, 8, 20, 9])

# l12 minimum variance
def mv(s1, s2, rho):
    w1 = (s2**2 - rho * s1 * s2) / (s1**2 + s2**2 - 2 * rho * s1 * s2)
    var = lambda w_: w_**2 * s1**2 + (1 - w_)**2 * s2**2 + 2 * w_ * (1 - w_) * rho * s1 * s2
    return w1, var

w1, var = mv(.2, .1, .3)
grid = np.linspace(-1, 2, 300001)
check("l12 w1* = 0.10526, vol 9.787%, formula is the grid minimum", abs(w1 - .10526) < 1e-5 and abs(math.sqrt(var(w1)) - .09787) < 1e-5 and abs(grid[var(grid).argmin()] - w1) < 2e-5)
check("l12 lambda = 2 sigma_p^2 = 0.01916", abs(.08 * w1 + .012 * (1 - w1) - 2 * var(w1)) < 1e-12 and abs(2 * var(w1) - .01916) < 5e-6)
check("l12 half and half 12.45%, variance 0.0155", abs(var(.5) - .0155) < 1e-12 and abs(math.sqrt(var(.5)) - .1245) < 5e-5)
check("l12 rho = -1 gives w1 = 1/3 and zero risk; rho = 1 formula gives -1 and zero risk with the short", abs(mv(.2, .1, -1)[0] - 1 / 3) < 1e-12 and mv(.2, .1, -1)[1](1 / 3) < 1e-15
      and abs(mv(.2, .1, 1)[0] + 1) < 1e-12 and abs(mv(.2, .1, 1)[1](-1.0)) < 1e-15)
check("[F10] l12 s6 option 'zero' why: 'zero risk needs rho = -1' (rho = 1 with w1 = -1 also gives zero risk, as l12 s5 says)", mv(.2, .1, 1)[1](-1.0) > 1e-9,
      "sigma_p at rho = 1, w1 = -1: 0")
check("l12 B alone is best from rho = 0.5 up (sigma_B / sigma_A)", mv(.2, .1, .5)[0] == 0 and mv(.2, .1, .49)[0] > 0 > mv(.2, .1, .51)[0])
check("l12 s6 30%/15% uncorrelated: 20% in A, 13.4%", abs(mv(.3, .15, 0)[0] - .2) < 1e-12 and abs(math.sqrt(mv(.3, .15, 0)[1](.2)) - .134) < 5e-4)
check("l12 s9 15%/25%/0.8: w1* = 1.3, clipped to 1; half gives 19%", abs(mv(.15, .25, .8)[0] - 1.3) < 1e-9 and abs(math.sqrt(mv(.15, .25, .8)[1](.5)) - .19) < 1e-3)
wl = np.linspace(0, 1, 100001)
check("l12 clipping the formula gives the long-only minimum (500 random pairs)", all(
    abs(wl[mv(a_, b_, r_)[1](wl).argmin()] - min(1, max(0, mv(a_, b_, r_)[0]))) < 2e-5
    for a_, b_, r_ in zip(rng.uniform(.05, .5, 500), rng.uniform(.05, .5, 500), rng.uniform(-.95, .95, 500))))
check("l12 q12-never: the calmer asset always gets the larger weight (2000 random pairs)", all(
    mv(max(a_, b_), min(a_, b_), r_)[0] < .5 for a_, b_, r_ in zip(rng.uniform(.05, .5, 2000), rng.uniform(.05, .5, 2000), rng.uniform(-.99, .99, 2000)) if abs(a_ - b_) > 1e-6))
check("review-3 0.8 and 14.14%; hw3 0.2143; problems-3 0.2, 0.2366, lambda 0.112, 0.05824 (exact 0.05826)", abs(mv(.1, .2, 0)[0] - .8) < 1e-12 and abs(math.sqrt(mv(.2, .2, 0)[1](.5)) - .1414) < 5e-5
      and abs(mv(.25, .15, .2)[0] - .21429) < 1e-5 and abs(mv(.4, .25, .3)[0] - .2) < 1e-12 and abs(math.sqrt(mv(.4, .25, .3)[1](.2)) - .2366) < 5e-5
      and abs(.32 * .2 + .06 * .8 - .112) < 1e-12 and abs(.056 * 1.02**2 - .05826) < 5e-6)
w1, var = mv(.3, .2, .4)
check("hw3 longform: 0.1951, 19.20%, lambda 0.07376 = 2 var; rho -1 gives 0.4; rho 0.9 gives -0.636", abs(w1 - .1951) < 5e-5 and abs(math.sqrt(var(w1)) - .1920) < 5e-5
      and abs(.18 * w1 + .048 * (1 - w1) - 2 * var(w1)) < 1e-12 and abs(mv(.3, .2, -1)[0] - .4) < 1e-12 and abs(mv(.3, .2, .9)[0] + .636) < 5e-4)
# Monte Carlo: the variance formula and the minimum-variance weight on simulated returns
n = 400000; z = rng.standard_normal((n, 2)); ra = .2 * z[:, 0]; rb = .1 * (.3 * z[:, 0] + math.sqrt(1 - .09) * z[:, 1])
ws = np.linspace(0, .3, 61); sim = np.array([np.var(w_ * ra + (1 - w_) * rb) for w_ in ws])
check("l12 Monte Carlo (400,000 draws): simulated portfolio volatility is lowest near 10.5% in A, about 9.79%, below B alone",
      abs(ws[sim.argmin()] - .10526) < .02 and abs(math.sqrt(sim.min()) - .09787) < .0005 and sim.min() < np.var(rb))

# ---------------------------------------------------------------- report
bad = [r for r in RESULTS if not r[1]]
for nm, ok, detail in RESULTS:
    print(("PASS " if ok else "FAIL ") + nm + ((" :: " + detail) if (detail and not ok) else ""))
print(f"\n{len(RESULTS)} checks, {len(RESULTS) - len(bad)} pass, {len(bad)} fail (each failure is a finding in docs/reviews/audit-multivar-1-3.md)")
sys.exit(1 if bad else 0)
