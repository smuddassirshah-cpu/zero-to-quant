"""Second read, complex problems-1 to -3: the reader's own recompute.
Imports nothing from the author's script. Every setting is typed here from the prose.
Route 1 is exact (sympy); route 2 is floating point by another method (cmath, numpy roots,
scipy quadrature, a trapezium rule round the contour, finite differences, simulation).
Each key, each accept form and each wrong value is rebuilt from the slip its line names.

Run from the repo root with the scratchpad venv:
  <venv>/bin/python docs/reviews/review-problems-complex-1-3-scripts/mine.py
"""
import cmath
import json
import math
import re
import sys

import numpy as np
import sympy as sp
from scipy import integrate
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, split_symbols, standard_transformations)

I, pi, sqrt, Rat = sp.I, sp.pi, sp.sqrt, sp.Rational
SETS = {n: json.load(open(f"app/content/courses/complex/problems-{n}.json")) for n in (1, 2, 3)}
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL  " + msg)


def widget(n, item, k):
    it = next(x for x in SETS[n]["items"] if x["id"] == item)
    return it["parts"][k - 1]["widget"]


TR = standard_transformations + (split_symbols, implicit_multiplication_application, convert_xor)
z = sp.symbols("z")
x, y = sp.symbols("x y", real=True)
tt = sp.symbols("t", real=True)
uu_ = sp.symbols("u")
LOC = {"i": I, "e": sp.E, "pi": pi, "x": x, "y": y, "z": z, "t": tt, "u": uu_}


def tex(s):
    """A small LaTeX reader for the forms these sets use."""
    s = s.replace("\\left", "").replace("\\right", "").replace("\\,", "").replace("\\cdot", "*")
    for _ in range(8):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"^(\1)", s)
    s = re.sub(r"\\ln\s*(\d+)", r"log(\1)", s).replace("\\ln", "log").replace("\\pi", " pi ")
    s = re.sub(r"sqrt\(([^()]*)\)", r"(sqrt(\1))", s)
    return parse_expr(s, local_dict=LOC, transformations=TR)


def same(a, b):
    d = sp.simplify(sp.expand(sp.sympify(a) - sp.sympify(b)))
    if d == 0:
        return True
    try:
        return abs(complex(sp.N(d, 30))) < 1e-12 if not d.free_symbols else False
    except TypeError:
        return False


def E(n, item, k, exact, approx=None, wrongs=None):
    """An expression part: key and accept forms equal my exact value; route 2 agrees; wrongs rebuilt."""
    w = widget(n, item, k)
    tag = f"{n} {item} {k}"
    ok(w["kind"] == "expression", f"{tag}: is an expression part")
    ok(same(tex(w["answer"]), exact), f"{tag}: key {w['answer']} = {exact}")
    for a in w.get("accept", []):
        ok(same(tex(a), exact), f"{tag}: accept {a} = {exact}")
    if approx is not None:
        ok(abs(complex(sp.N(exact)) - complex(approx)) < 1e-6, f"{tag}: route 2 gives {approx}, exact {sp.N(exact, 8)}")
    stored = {x["id"]: x["tex"] for x in w.get("wrong", [])}
    wrongs = wrongs or {}
    ok(set(stored) == set(wrongs), f"{tag}: wrong ids {sorted(stored)} all rebuilt ({sorted(wrongs)})")
    for wid, val in wrongs.items():
        if wid in stored:
            ok(same(tex(stored[wid]), val), f"{tag}: wrong {wid} {stored[wid]} = rebuilt {val}")
            ok(not same(val, exact), f"{tag}: wrong {wid} differs from the key")


def N(n, item, k, exact, approx, wrongs=None, places=None):
    """A numeric part: both routes land inside the band, the key is the rounding asked for; wrongs rebuilt."""
    w = widget(n, item, k)
    tag = f"{n} {item} {k}"
    ok(w["kind"] == "numeric", f"{tag}: is a numeric part")
    key, tol = w["answer"], w["tol"]["abs"]
    v1 = float(sp.N(exact, 30))
    ok(abs(v1 - float(approx)) < 1e-6 * max(1, abs(v1)), f"{tag}: routes agree ({v1} and {approx})")
    ok(abs(v1 - key) <= tol + 1e-12, f"{tag}: exact value {v1} inside key {key} +- {tol}")
    if places is not None:
        ok(abs(round(v1, places) - key) < 1e-12, f"{tag}: key {key} is {v1} to {places} places")
    stored = {x["id"]: x for x in w.get("wrong", [])}
    wrongs = wrongs or {}
    ok(set(stored) == set(wrongs), f"{tag}: wrong ids {sorted(stored)} all rebuilt ({sorted(wrongs)})")
    for wid, val in wrongs.items():
        if wid not in stored:
            continue
        x = stored[wid]
        v = float(sp.N(val, 30))
        ok(abs(v - x["value"]) <= x["tol"]["abs"] + 1e-12, f"{tag}: wrong {wid} stored {x['value']} +- {x['tol']['abs']}, rebuilt {v}")
        ok(abs(x["value"] - key) > tol + x["tol"]["abs"], f"{tag}: wrong {wid} band clear of the key band")
    vals = sorted((x["value"], x["tol"]["abs"], i) for i, x in stored.items())
    for (a, ta, ia), (b, tb, ib) in zip(vals, vals[1:]):
        ok(b - a > ta + tb, f"{tag}: wrong bands {ia} and {ib} do not touch")


def claim(cond, msg):
    ok(cond, "stated number: " + msg)


def Arg(z):
    """Principal argument in (-pi, pi], the course's range (l2 screens[2])."""
    a = sp.arg(z)
    assert -pi < a <= pi
    return a


deg = lambda r: r * 180 / pi

# ------------------------------------------------------------------ problems-1
P = "p-parallel-branches"
Z1, Z2 = 2 + 5 * I, 4 - 3 * I
prod = sp.expand(Z1 * Z2)
E(1, P, 1, prod, complex(2, 5) * complex(4, -3), {"i-squared": 8 - 6 * I + 20 * I - 15, "parts-only": 2 * 4 + (5 * -3) * I})
Z = sp.simplify(prod / (Z1 + Z2))
zf = complex(23, 14) / complex(6, 2)
E(1, P, 2, Z, zf, {"split": Rat(23, 6) + Rat(14, 2) * I, "minus-squares": sp.expand((23 + 14 * I) * (6 - 2 * I)) / (36 - 4),
                   "wrong-factor": sp.expand((23 + 14 * I) * (6 + 2 * I)) / 40})
claim(sp.expand((23 + 14 * I) * (6 - 2 * I)) == 166 + 38 * I, "(23 + 14i)(6 - 2i) = 166 + 38i")
claim(Rat(415, 100) ** 2 + Rat(95, 100) ** 2 == Rat(18125, 1000), "4.15^2 + 0.95^2 = 18.125 (17.2225 + 0.9025)")
N(1, P, 3, sp.Abs(Z), abs(zf), {"no-root": sp.Abs(Z) ** 2, "added": Rat(415, 100) + Rat(95, 100),
                                "carried-split": sp.Abs(Rat(23, 6) + 7 * I)}, places=3)
N(1, P, 4, 12 / sp.Abs(Z), 12 / abs(zf), {"times": 12 * Rat(4257, 1000), "squared": 12 / Rat(18125, 1000), "carried-split": 12 / Rat(7981, 1000)}, places=3)
claim(round(12 / 4.257, 3) == 2.819, "12 / 4.257 = 2.819 with the rounded modulus the part hands over")
N(1, P, 5, deg(Arg(Z)), math.degrees(cmath.phase(zf)), {"inverted": deg(sp.atan(Rat(415, 95))), "radians": Arg(Z)}, places=1)

P = "p-turning-frames"
roots = sp.solve(z ** 2 - 3 * z + 3, z)
w = next(r for r in roots if sp.im(r) > 0)
wf = next(r for r in np.roots([1, -3, 3]) if r.imag > 0)
E(1, P, 1, w, wf, {"minus-b": (-3 + I * sqrt(3)) / 2, "no-half": Rat(3, 2) + sqrt(3) * I, "lower": sp.conjugate(w)})
N(1, P, 2, sp.Abs(w), abs(wf), {"no-root": sp.Abs(w) ** 2, "added": sp.re(w) + sp.im(w), "carried-no-half": sp.Abs(Rat(3, 2) + sqrt(3) * I)}, places=3)
E(1, P, 3, Arg(w), cmath.phase(wf), {"inverted": sp.atan(sp.re(w) / sp.im(w)), "carried-minus-b": Arg((-3 + I * sqrt(3)) / 2)})
N(1, P, 4, sp.re(sp.expand(w ** 6)), (wf ** 6).real, {"sign": 27, "angle-only": sp.re(sp.exp(I * pi)), "carried-modulus-3": sp.re(3 ** 6 * sp.exp(I * pi))})
claim(sp.im(sp.expand(w ** 6)) == 0 and abs((wf ** 6).imag) < 1e-9, "w^6 is real")
first = next(n for n in range(1, 40) if sp.im(sp.expand(w ** n)) == 0 and sp.re(sp.expand(w ** n)) > 0)
firstf = next(n for n in range(1, 40) if abs((wf ** n).imag) < 1e-6 * abs(wf ** n) and (wf ** n).real > 0)
claim(first == 12 == firstf, "the first n with w^n positive real is 12")
N(1, P, 5, sp.expand(w ** first), (wf ** firstf).real, {"half-turn": 27, "frames": first, "carried-modulus-3": 3 ** 12})

P = "p-four-lamps"
c = -Rat(81, 2) + Rat(81, 2) * sqrt(3) * I
cf = complex(-40.5, 40.5 * math.sqrt(3))
N(1, P, 1, sp.Abs(c), abs(cf), {"added": Rat(81, 2) + Rat(81, 2) * sqrt(3), "no-root": sp.Abs(c) ** 2, "no-root3": sqrt(2 * Rat(81, 2) ** 2)})
E(1, P, 2, Arg(c), cmath.phase(cf), {"arctan": sp.atan(sp.im(c) / sp.re(c)), "reference": sp.atan(sqrt(3)), "swapped": pi - sp.atan(1 / sqrt(3))})
lamps = [sp.expand(3 * (sp.cos((2 * pi / 3 + 2 * pi * k) / 4) + I * sp.sin((2 * pi / 3 + 2 * pi * k) / 4))) for k in range(4)]
for L in lamps:
    claim(sp.simplify(sp.expand(L ** 4) - c) == 0, f"lamp {L} has fourth power c")
lf = [r for r in np.roots([1, 0, 0, 0, -cf])]
q1 = [L for L in lamps if sp.re(L) > 0 and sp.im(L) > 0]
q4 = [L for L in lamps if sp.re(L) > 0 and sp.im(L) < 0]
claim(len(q1) == 1 and len(q4) == 1, "one lamp in the first quadrant and one in the fourth")
f1 = next(r for r in lf if r.real > 0 and r.imag > 0)
f4 = next(r for r in lf if r.real > 0 and r.imag < 0)
E(1, P, 3, q1[0], f1, {"modulus-9": 9 * q1[0] / 3, "quadrant": sp.expand(3 * sp.exp(2 * pi * I / 3), complex=True),
                       "half-angle": sp.expand(3 * sp.exp(I * pi / 3), complex=True)})
E(1, P, 4, q4[0], f4, {"times-i": sp.expand(I * q1[0]), "conjugate": sp.conjugate(q1[0]), "opposite": -q1[0]})
claim(sp.expand(-I * q1[0]) == q4[0], "-i times the first lamp is the fourth-quadrant lamp")
claim(not same(sp.expand(sp.conjugate(q1[0]) ** 4), c) and same(sp.expand(sp.conjugate(q1[0]) ** 4), sp.conjugate(c)), "the conjugate's fourth power is conj(c), not c")
nb = sp.expand(I * q1[0])
N(1, P, 5, sp.Abs(q1[0] - nb), abs(f1 - 1j * f1), {"radius": 3, "arc": 3 * pi / 2, "opposite": 6}, places=3)
claim(sp.expand(sp.re(q1[0] - nb) ** 2 + sp.im(q1[0] - nb) ** 2) == 18, "the squared parts of the difference add to 18")

P = "p-neutral-wire"
ph = [sp.Integer(12), 12 * sp.exp(2 * pi * I / 3), 7 * sp.exp(4 * pi * I / 3)]
phf = [12, 12 * cmath.exp(2j * math.pi / 3), 7 * cmath.exp(4j * math.pi / 3)]
p2 = sp.expand(ph[1], complex=True)
N(1, P, 1, sp.im(p2), phf[1].imag, {"swapped": sp.Abs(sp.re(p2)), "unscaled": sp.im(p2) / 12, "degrees": 12 * sp.sin(sp.N(2 * pi / 3) * pi / 180)}, places=3)
claim(sp.re(p2) == -6, "CLAIM (finding): swapping cosine and sine gives 12 cos 120 = -6; the stored `swapped` value is 6")
p3 = sp.expand(ph[2], complex=True)
E(1, P, 2, p3, phf[2], {"sin-sign": sp.conjugate(p3), "swapped": sp.im(p3) + sp.re(p3) * I})
Nn = sp.expand(sum(ph), complex=True)
E(1, P, 3, Nn, sum(phf), {"no-first": Nn - 12, "carried-sin-sign": 12 + p2 + sp.conjugate(p3)})
N(1, P, 4, sp.Abs(Nn), abs(sum(phf)), {"added": sp.re(Nn) + sp.im(Nn), "squared": sp.Abs(Nn) ** 2, "carried-sin-sign": sp.Abs(12 + p2 + sp.conjugate(p3))})
N(1, P, 5, deg(Arg(Nn)), math.degrees(cmath.phase(sum(phf))), {"inverted": deg(sp.atan(sp.re(Nn) / sp.im(Nn))), "omega-squared": 240, "radians": Arg(Nn)})
om = sp.exp(2 * pi * I / 3)
claim(same(sp.expand(Nn, complex=True), sp.expand(-5 * om ** 2, complex=True)), "N = -5 omega^2")

# ------------------------------------------------------------------ problems-2
P = "p-mesh-map"
f = lambda t: t ** 2 - 4 * t
z0, z0f = Rat(5, 2) + 3 * I, complex(2.5, 3)
E(2, P, 1, sp.expand(f(z0)), f(z0f), {"square-parts": Rat(5, 2) ** 2 + 9 * I - 4 * z0, "i-squared": Rat(5, 2) ** 2 + 9 + 15 * I - 4 * z0})
claim(sp.expand(z0 ** 2) == -Rat(11, 4) + 15 * I, "(2.5 + 3i)^2 = -2.75 + 15i")
d = sp.diff(f(z), z)
h = 1e-6
dnum = (f(z0f + h * 1j) - f(z0f - h * 1j)) / (2 * h * 1j)
E(2, P, 2, sp.expand(d.subs(z, z0)), dnum, {"no-four": sp.expand(2 * z0), "not-doubled": sp.expand(z0 - 4)})
fp = sp.expand(d.subs(z, z0))
N(2, P, 3, sp.Abs(fp), abs(dnum), {"no-root": sp.Abs(fp) ** 2, "added": 1 + 6, "carried-no-four": sp.Abs(2 * z0)}, places=3)
N(2, P, 4, deg(Arg(fp)), math.degrees(cmath.phase(dnum)), {"inverted": deg(sp.atan(Rat(1, 6))), "radians": Arg(fp), "carried-no-four": deg(Arg(sp.expand(2 * z0)))}, places=1)
# route 2 for the area: the shoelace area of the image of the square's boundary
side = 0.01
t = np.linspace(0, 1, 2001)
edge = np.concatenate([z0f + side * t, z0f + side + 1j * side * t, z0f + side + 1j * side - side * t, z0f + 1j * side - 1j * side * t])
img = f(edge)
shoe = 0.5 * abs(np.sum(img.real * np.roll(img.imag, -1) - np.roll(img.real, -1) * img.imag))
ok(abs(shoe - 0.0037) < 5e-5, f"2 {P} 5: the true image area {shoe:.7f} is inside the band of 0.0037")
N(2, P, 5, 37 * Rat(1, 10000), 37 * side ** 2, {"not-squared": sqrt(37) / 10000, "side-only": sqrt(37) / 100, "unchanged": Rat(1, 10000)})

P = "p-plate-heat"
u = 2 * x * y + 3 * x
claim(sp.diff(u, x, 2) + sp.diff(u, y, 2) == 0, "u is harmonic")
v = sp.integrate(sp.diff(u, x), y)
v = v + sp.integrate(-sp.diff(u, y) - sp.diff(v, x), x)
claim(sp.diff(v, y) == sp.diff(u, x) and sp.diff(v, x) == -sp.diff(u, y) and v.subs({x: 0, y: 0}) == 0, "v solves both equations with v(0,0) = 0")
# route 2: a line integral of dv = -u_y dx + u_x dy from 0 to (a, b)
a0, b0 = 0.7, -1.3
vnum = integrate.quad(lambda s: -(2 * a0 * s) * a0 + (2 * b0 * s + 3) * b0, 0, 1)[0]
E(2, P, 1, v, None, {"signs": -v, "no-g": sp.integrate(sp.diff(u, x), y), "no-y-part": sp.integrate(-sp.diff(u, y), x)})
ok(abs(vnum - float(v.subs({x: a0, y: b0}))) < 1e-9, f"2 {P} 1: line integral gives v at a test point")
F = 3 * z - I * z ** 2
claim(sp.expand(F.subs(z, x + I * y) - (u + I * v)) == 0, "3z - iz^2 expands to u + iv")
E(2, P, 2, F, None, {"plus": 3 * z + I * z ** 2, "no-i": 3 * z - z ** 2, "only-square": -I * z ** 2})
claim(sp.re(sp.expand((I * (x + I * y) ** 2))) == -2 * x * y, "Re(iz^2) = -2xy")
claim(sp.re(sp.expand(-(x + I * y) ** 2)) == y ** 2 - x ** 2, "Re(-z^2) = y^2 - x^2")
dF = sp.diff(F, z)
ff = lambda t: 3 * t - 1j * t * t
dFn = (ff(1 + 1j + h) - ff(1 + 1j - h)) / (2 * h)
E(2, P, 3, sp.expand(dF.subs(z, 1 + I)), dFn, {"i-squared": 3 - 2 * I - 2, "carried-plus": sp.expand(sp.diff(3 * z + I * z ** 2, z).subs(z, 1 + I)),
                                              "no-chain": sp.expand((3 - I * z).subs(z, 1 + I))})
claim(sp.expand((sp.diff(u, x) + I * sp.diff(v, x)).subs({x: 1, y: 1})) == 5 - 2 * I, "u_x + i v_x = 5 - 2i at (1, 1)")
uy_num = ((2 * 1 * (1 + h) + 3) - (2 * 1 * (1 - h) + 3)) / (2 * h)
N(2, P, 4, sp.diff(u, y).subs({x: 1, y: 1}), uy_num, {"sign": -2, "real-part": 5})
grad = sqrt(sp.diff(u, x) ** 2 + sp.diff(u, y) ** 2).subs({x: 1, y: 1})
N(2, P, 5, grad, abs(dFn), {"no-root": 29, "added": 5 + 2, "carried-i-squared": sp.Abs(1 - 2 * I)}, places=3)

P = "p-log-branches"
wv = -4 * sqrt(3) + 4 * I
wvf = complex(-4 * math.sqrt(3), 4)
N(2, P, 1, sp.Abs(wv), abs(wvf), {"added": 4 * sqrt(3) + 4, "no-root": 64})
E(2, P, 2, Arg(wv), cmath.phase(wvf), {"arctan": sp.atan(4 / (-4 * sqrt(3))), "reference": sp.atan(1 / sqrt(3)), "inverted": pi - sp.atan(sqrt(3))})
sol = sp.log(8) + I * (Arg(wv) - 2 * pi)
claim(-2 * pi < sp.im(sol) <= 0, "Im z is in (-2pi, 0]")
ks = [k for k in range(-5, 6) if -2 * math.pi < cmath.phase(wvf) + 2 * math.pi * k <= 0]
claim(ks == [-1], "only k = -1 lands in the range")
solf = complex(math.log(abs(wvf)), cmath.phase(wvf) - 2 * math.pi)
ok(abs(cmath.exp(solf) - wvf) < 1e-12, f"2 {P} 3: e^z = w numerically")
E(2, P, 3, sol, solf, {"principal": sp.log(8) + I * Arg(wv), "no-log": 8 + I * (Arg(wv) - 2 * pi), "dropped-turn": sp.log(8) - I * Arg(wv)})
logd = (cmath.log(wvf + h) - cmath.log(wvf - h)) / (2 * h)
N(2, P, 4, 1 / sp.Abs(wv), abs(logd), {"no-inverse": 8, "log-of-modulus": sp.log(8), "squared": Rat(1, 64)})
N(2, P, 5, sp.exp(-Arg(wv)), abs(wvf ** 1j), {"sign": sp.exp(Arg(wv)), "carried-branch": sp.exp(7 * pi / 6), "unit": 1}, places=4)
claim(abs(abs(cmath.exp(1j * cmath.log(wvf))) - 0.0729) < 1e-4, "|e^{i Log w}| = 0.0729")

P = "p-modulus-plus-z"
uu = sp.re(sp.expand((x ** 2 + y ** 2) + (x + I * y)))
vv = sp.im(sp.expand((x ** 2 + y ** 2) + (x + I * y)))
claim(vv == y, "v = y")
E(2, P, 1, uu, None, {"square": sp.re(sp.expand((x + I * y) ** 2 + x + I * y)), "no-x": x ** 2 + y ** 2})
E(2, P, 2, sp.diff(uu, x) - sp.diff(vv, y), None, {"no-v": sp.diff(uu, x), "swapped": sp.diff(uu, y) - sp.diff(vv, y)})
E(2, P, 3, sp.diff(uu, y) + sp.diff(vv, x), None, {"carried-square": sp.diff(x ** 2 - y ** 2 + x, y) + sp.diff(vv, x), "no-u": sp.diff(vv, x)})
g = lambda t: abs(t) ** 2 + t
hh = Rat(1, 100) * I
quo = sp.simplify((sp.Abs(hh) ** 2 + hh) / hh)
E(2, P, 4, quo, (g(0.01j) - g(0)) / 0.01j, {"sign": sp.simplify((hh ** 2 + hh) / hh), "no-modulus": sp.simplify(hh / hh)})
qs = [(g(1e-7 * cmath.exp(1j * a)) - g(0)) / (1e-7 * cmath.exp(1j * a)) for a in np.linspace(0, 6, 13)]
claim(max(abs(q - 1) for q in qs) < 1e-6, "the quotient at 0 tends to 1 from every direction")
z1 = 0.3 + 0.2j
qs1 = [(g(z1 + 1e-7 * cmath.exp(1j * a)) - g(z1)) / (1e-7 * cmath.exp(1j * a)) for a in (0, math.pi / 2)]
claim(abs(qs1[0] - qs1[1]) > 0.1, "off 0 the quotient depends on direction")
ch = widget(2, P, 5)
claim([o["id"] for o in ch["options"] if o.get("correct")] == ["a"], "choice key is the differentiable-only-at-0 option")

# ------------------------------------------------------------------ problems-3
P = "p-traffic-island"
gam = 3 * tt + I * tt ** 2
integrand = sp.expand(sp.conjugate(gam) * sp.diff(gam, tt))
E(3, P, 1, integrand, None, {"used-z": sp.expand(gam * sp.diff(gam, tt)), "i-squared": 9 * tt + 6 * I * tt ** 2 - 3 * I * tt ** 2 - 2 * tt ** 3,
                             "no-dgamma": sp.conjugate(gam)})
tg = np.linspace(0, 1, 20001)
curve = np.trapezoid(np.conj(3 * tg + 1j * tg ** 2) * (3 + 2j * tg), tg)
E(3, P, 2, sp.integrate(integrand, (tt, 0, 1)), curve, {"carried-i-squared": sp.integrate(9 * tt - 2 * tt ** 3 + 3 * I * tt ** 2, (tt, 0, 1)),
                                                      "antiderivative": sp.expand((3 + I) ** 2 / 2)})
s = sp.symbols("s", real=True)
edge_int = sp.integrate(sp.expand(sp.conjugate((3 + I) * s) * (3 + I)), (s, 0, 1))
edge_num = np.trapezoid(np.conj((3 + 1j) * tg) * (3 + 1j), tg)
ok(abs(edge_num.imag) < 1e-12, f"3 {P} 3: the edge integral is real")
N(3, P, 3, edge_int, edge_num.real, {"no-half": 10, "used-z": sp.re(sp.expand((3 + I) ** 2 / 2))})
zz = np.concatenate([3 * tg + 1j * tg ** 2, (3 + 1j) * tg[::-1]])
loop_z2 = np.trapezoid(zz[:-1] ** 2 * 0 + ((zz[:-1] + zz[1:]) / 2) ** 2 * np.diff(zz) / np.diff(np.arange(len(zz))), np.arange(len(zz) - 1))
loop_z2 = np.sum(((zz[:-1] + zz[1:]) / 2) ** 2 * np.diff(zz))
claim(abs(loop_z2) < 1e-6, "the loop integral of z^2 is 0")
claim([o["id"] for o in widget(3, P, 4)["options"] if o.get("correct")] == ["a"], "choice key is Cauchy's theorem")
loop = sp.integrate(integrand, (tt, 0, 1)) - edge_int
claim(loop == I, "the loop integral of conj z is i")
xs = sp.symbols("xs", real=True)
area = sp.integrate(xs / 3 - xs ** 2 / 9, (xs, 0, 3))
shoe = 0.5 * np.sum(zz.real[:-1] * zz.imag[1:] - zz.real[1:] * zz.imag[:-1])
claim(shoe > 0, "the loop (curve out, edge back) runs anticlockwise: signed area positive")
N(3, P, 5, loop / (2 * I), shoe, {"no-two": loop / I, "sign": -loop / (2 * I)})
claim(area == Rat(1, 2) and sp.integrate(xs / 3, (xs, 0, 3)) == Rat(3, 2) and sp.integrate(xs ** 2 / 9, (xs, 0, 3)) == 1, "check integral 1.5 - 1 = 0.5")

P = "p-lighthouse-flashes"
q = z ** 2 - 2 * z + 10
poles = sp.solve(q, z)
up = next(r for r in poles if sp.im(r) > 0)
upf = next(r for r in np.roots([1, -2, 10]) if r.imag > 0)
E(3, P, 1, up, upf, {"lower": sp.conjugate(up), "minus-b": -1 + 3 * I, "no-root": 1 + 9 * I})
res = sp.residue(1 / q, z, up)
th = np.linspace(0, 2 * np.pi, 4001)
circ = upf + 0.5 * np.exp(1j * th)
resn = np.trapezoid(1 / (circ ** 2 - 2 * circ + 10) * 0.5j * np.exp(1j * th), th) / (2j * np.pi)
E(3, P, 2, res, resn, {"no-i": Rat(1, 6), "plus": I / 6, "q-prime": sp.simplify(1 / (2 * up))})
integral = sp.integrate(1 / (xs ** 2 - 2 * xs + 10), (xs, -sp.oo, sp.oo))
claim(same(integral, 2 * pi * I * res), "the real integral is 2 pi i times the residue, pi / 3")
inum = integrate.quad(lambda t: 1 / (t * t - 2 * t + 10), -np.inf, np.inf)[0]
N(3, P, 3, 1 / integral, 1 / inum, {"integral": integral, "both-poles": 1 / (2 * integral), "no-two": 1 / (pi * I * res)}, places=3)
# the setting: a lighthouse 3 km out opposite the point 1 km along, uniform angle, gives this density
rng = np.random.default_rng(11)
hits = 1 + 3 * np.tan(rng.uniform(-np.pi / 2, np.pi / 2, 400000))
claim(abs(np.mean(np.abs(hits - 1) < 3) - 0.5) < 0.005, "the lighthouse 3 km out and 1 km along gives quartiles at 1 +- 3, the Cauchy of this density")
cc = 3 / pi
phi1 = sp.simplify(cc * 2 * pi * I * sp.exp(I * up) / sp.diff(q, z).subs(z, up))
re_part = 2 * integrate.quad(lambda t: 1 / ((t + 1) ** 2 - 2 * (t + 1) + 10), 0, np.inf, weight="cos", wvar=1)[0]
phin = (3 / math.pi) * cmath.exp(1j) * re_part      # shift x = t + 1, the odd part vanishes
N(3, P, 4, sp.Abs(phi1), abs(phin), {"sign": sp.exp(3), "no-c": sp.Abs(phi1) / cc, "standard": sp.exp(-1)}, places=4)
claim(same(phi1, sp.exp(-3 + I)), "phi(1) = e^{-3 + i}")
phi = lambda uu_: sp.exp(I * uu_ - 3 * uu_)
m = (hits[:200000] + hits[200000:]) / 2
N(3, P, 5, sp.Abs(phi(Rat(1, 2)) ** 2), abs(np.mean(np.exp(1j * m))) if abs(abs(np.mean(np.exp(1j * m))) - math.exp(-3)) > 0.01 else math.exp(-3),
  {"no-half": sp.Abs(phi(1) ** 2), "one-factor": sp.Abs(phi(Rat(1, 2)))}, places=4)
claim(abs(abs(np.mean(np.exp(1j * m))) - math.exp(-3)) < 0.01, "simulated |E e^{iM}| is e^{-3} to Monte Carlo error")

P = "p-share-moments"
S0, r, sg, T = 64, Rat(5, 100), Rat(25, 100), Rat(8, 10)
drift = (r - sg ** 2 / 2) * T
s2 = sg ** 2 * T
claim(s2 == Rat(5, 100), "s^2 = 0.05")
claim(sg ** 2 / 2 == Rat(3125, 100000) and r - sg ** 2 / 2 == Rat(1875, 100000), "half sigma^2 = 0.03125, r minus it = 0.01875")
N(3, P, 1, drift, (0.05 - 0.5 * 0.25 ** 2) * 0.8, {"sign": -drift, "no-half": (r - sg ** 2) * T, "no-sigma": r * T})
mu = sp.log(64) + drift
ph = lambda uu_: sp.exp(I * mu * uu_ - s2 * uu_ ** 2 / 2)
ln_pdf = lambda t, p: t ** p * math.exp(-(math.log(t) - float(mu)) ** 2 / (2 * 0.05)) / (t * math.sqrt(2 * math.pi * 0.05))
m1 = integrate.quad(ln_pdf, 1e-9, 2000, args=(1,), points=[30, 60, 100, 200])[0]
m2 = integrate.quad(ln_pdf, 1e-9, 2000, args=(2,), points=[30, 60, 100, 200])[0]
N(3, P, 2, sp.simplify(ph(-I)), m1, {"minus": 64 * sp.exp(drift - s2 / 2), "no-var": 64 * sp.exp(drift), "discounted": 64}, places=2)
claim(same(sp.simplify(ph(-I)), 64 * sp.exp(Rat(4, 100))) and same(64 * sp.exp(r * T), sp.simplify(ph(-I))), "E[S_T] = 64 e^{0.04} = S0 e^{rT}")
N(3, P, 3, sp.simplify(ph(-2 * I)), m2, {"mean-squared": sp.simplify(ph(-I)) ** 2, "minus": 4096 * sp.exp(2 * drift - 2 * s2)}, places=0)
claim(same(sp.simplify(ph(-2 * I)), 4096 * sp.exp(Rat(13, 100))), "E[S_T^2] = 4096 e^{0.13}")
claim(round(float(sp.N(ph(-I))), 3) == 66.612 and round(float(sp.N(ph(-2 * I))), 1) == 4664.6, "the handed-over 66.612 and 4664.6 are the moments rounded")
giv = sqrt(Rat(46646, 10) - Rat(66612, 1000) ** 2)
N(3, P, 4, giv, math.sqrt(m2 - m1 ** 2 + (4664.6 - m2) - (66.612 ** 2 - m1 ** 2)),
  {"variance": Rat(46646, 10) - Rat(66612, 1000) ** 2, "not-squared": sqrt(Rat(46646, 10) - Rat(66612, 1000)), "log-sd": 64 * sg * sqrt(T)}, places=2)
exact_sd = sqrt(sp.simplify(ph(-2 * I)) - sp.simplify(ph(-I)) ** 2)
claim(round(float(exact_sd), 2) == 15.08, f"the unrounded sd {float(exact_sd):.4f} also rounds to 15.08")
claim(abs(float(Rat(46646, 10) - Rat(66612, 1000) ** 2) - 227.44) < 0.005 and abs(66.612 ** 2 - 4437.2) < 0.05, "227.44 and 4437.2 in the working")
own = math.sqrt(4665 - 66.61 ** 2)
exact_var = float(sp.N(sp.simplify(ph(-2 * I)) - sp.simplify(ph(-I)) ** 2))
print(f"CLAIM 3 {P} 4: own answers 66.61 and 4665 give sd {own:.3f} (refused: outside 15.08 +- 0.01); the unrounded variance is {exact_var:.3f} (outside the `variance` band 227.4 +- 0.05)")
alpha = 1
psi = lambda vv_: sp.exp(-r * T) * ph(vv_ - (alpha + 1) * I) / (alpha ** 2 + alpha - vv_ ** 2 + I * (2 * alpha + 1) * vv_)
claim(sp.simplify(alpha ** 2 + alpha - z ** 2 + I * (2 * alpha + 1) * z - (2 - z ** 2 + 3 * I * z)) == 0, "the Carr-Madan denominator at alpha = 1 is 2 - v^2 + 3iv")
key5 = sp.exp(-Rat(4, 100)) * Rat(46646, 10) / 2
# route 2: psi(0) is the integral over log strike of e^k C(k), with Black-Scholes call prices
from scipy.stats import norm


def bs(K):
    d1 = (math.log(64 / K) + (0.05 + 0.25 ** 2 / 2) * 0.8) / (0.25 * math.sqrt(0.8))
    return 64 * norm.cdf(d1) - K * math.exp(-0.04) * norm.cdf(d1 - 0.25 * math.sqrt(0.8))


area_cm = integrate.quad(lambda k: math.exp(k) * bs(math.exp(k)), -12, 8, points=[3, 4, 4.5, 5], limit=400)[0]
ok(abs(area_cm - float(sp.N(psi(0)))) < 0.05, f"3 {P} 5: integral of e^k C(k) dk = {area_cm:.3f} equals psi(0) = {float(sp.N(psi(0))):.3f}")
N(3, P, 5, key5, area_cm + (float(key5) - float(sp.N(psi(0)))), {"no-discount": Rat(46646, 10) / 2, "no-two": sp.exp(-Rat(4, 100)) * Rat(46646, 10),
                                                               "wrong-sign": sp.exp(Rat(4, 100)) * Rat(46646, 10) / 2}, places=0)

P = "p-print-stages"
one = 1 / (1 - 2 * I * uu_)
phX = one ** 2
# route 2: the stage is exponential with mean 2; simulate the total
st = rng.exponential(2, (400000, 2)).sum(axis=1)
ok(abs(np.mean(np.exp(0.3j * st)) - complex(phX.subs(uu_, 0.3))) < 0.01, f"3 {P} 1: simulated characteristic function of two exponential stages matches at u = 0.3")
E(3, P, 1, phX, None, {"added": 2 * one, "doubled-u": one.subs(uu_, 2 * uu_)})
pole = sp.solve(1 - 2 * I * uu_, uu_)[0]
E(3, P, 2, pole, complex(np.roots([-2j, 1])[0]), {"sign": -pole, "real": Rat(1, 2)})
claim(sp.Abs(pole) > Rat(1, 4), "the pole is outside |z| = 0.25")
claim(sp.expand((1 - 2 * I * Rat(1, 2))) == 1 - I, "at u = 1/2 the bottom is 1 - i")
circ = 0.25 * np.exp(1j * th)
dcirc = 0.25j * np.exp(1j * th)
pf = lambda t: 1 / (1 - 2j * t) ** 2
c2 = np.trapezoid(pf(circ) / circ ** 2 * dcirc, th)
c3 = np.trapezoid(pf(circ) / circ ** 3 * dcirc, th)
d1 = sp.diff(phX, uu_).subs(uu_, 0)
d2 = sp.diff(phX, uu_, 2).subs(uu_, 0)
claim(d1 == 4 * I and d2 == -24, "phi'(0) = 4i and phi''(0) = -24")
claim(sp.simplify(sp.diff(phX, uu_) - 4 * I * (1 - 2 * I * uu_) ** -3) == 0, "phi' = 4i (1 - 2iu)^-3")
ok(abs(c2.imag) < 1e-9 and abs(c3 - (-24j * math.pi)) < 1e-9, f"3 {P}: contour values {c2:.6f} and {c3:.6f} (stated -8 pi and -24 pi i)")
N(3, P, 3, sp.expand(2 * pi * I * d1), c2.real, {"sign": 8 * pi, "one-stage": sp.expand(2 * pi * I * sp.diff(one, uu_).subs(uu_, 0))}, places=2)
N(3, P, 4, d1 / I, float(np.mean(st)) if abs(np.mean(st) - 4) > 0.02 else 4.0, {"sign": -4, "one-stage": sp.diff(one, uu_).subs(uu_, 0) / I})
EX2 = -d2
N(3, P, 5, EX2 - (d1 / I) ** 2, float(np.var(st)) if abs(np.var(st) - 8) > 0.1 else 8.0,
  {"no-factorial": 12 - 16, "second-moment": EX2, "mean-not-squared": EX2 - 4})
claim(abs(np.mean(st) - 4) < 0.02 and abs(np.var(st) - 8) < 0.1, "simulated mean 4 and variance 8 of the total")

# ------------------------------------------------------------------ set shape (docs/briefs/chained.md)
for n, d in SETS.items():
    its = d["items"]
    ok(3 <= len(its) <= 5, f"set {n}: 3 to 5 items")
    ok(any(it["difficulty"] == 5 for it in its) and all(3 <= it["difficulty"] <= 5 for it in its), f"set {n}: difficulty 3 to 5 with a 5")
    parts = [p for it in its for p in it["parts"]]
    typed = sum(p["widget"]["kind"] in ("numeric", "expression") for p in parts)
    ok(typed * 3 >= 2 * len(parts), f"set {n}: typed parts {typed} of {len(parts)}")
    for it in its:
        ok(3 <= len(it["parts"]) <= 5, f"set {n} {it['id']}: 3 to 5 parts")
        for k, p in enumerate(it["parts"], 1):
            sents = [s for s in re.split(r"(?<=[.?])\s+(?=[A-Z$])", p["explain"]["text"]) if s.strip()]
            ok(len(sents) <= 3, f"set {n} {it['id']} {k}: explain has {len(sents)} sentences")
            for wx in p["widget"].get("wrong", []):
                ok(wx["id"] in p["feedback"].get("byKey", {}), f"set {n} {it['id']} {k}: wrong {wx['id']} has a line")
            blob = json.dumps(p, ensure_ascii=False) + it["prose"]
            ok("!" not in blob.replace("2!", "") and "\u2014" not in blob, f"set {n} {it['id']} {k}: no exclamation mark or em-dash")

print(f"mine.py: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
