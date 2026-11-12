"""Numbers of the fixes proposed in review-problems-complex-1-3.md, each by two routes.
Run from the repo root with the scratchpad venv:
  <venv>/bin/python docs/reviews/review-problems-complex-1-3-scripts/proposed.py
"""
import cmath
import math
import sys

import numpy as np
import sympy as sp
from scipy import integrate

I, pi, Rat = sp.I, sp.pi, sp.Rational
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        fails += 1


def near(a, b, tol=5e-5):
    return abs(float(sp.N(a)) - b) <= tol


# finding 3: p-neutral-wire part 1, cosine and sine swapped
ok(sp.expand(12 * sp.cos(2 * pi / 3)) == -6 and abs(12 * math.cos(2 * math.pi / 3) + 6) < 1e-12, "finding 3: 12 cos 120 = -6, the swapped value")

# finding 4: p-parallel-branches part 2, the wrong-factor line
top = sp.expand((23 + 14 * I) * (6 + 2 * I))
ok(top == 110 + 130 * I and sp.expand((6 + 2 * I) ** 2) == 32 + 24 * I, "finding 4: top (23+14i)(6+2i) = 110 + 130i; bottom (6+2i)^2 = 32 + 24i, not 40")
ok(sp.simplify(top / (6 + 2 * I) ** 2 - (Rat(415, 100) + Rat(95, 100) * I)) == 0, "finding 4: top and bottom both times 6 + 2i gives Z again, so the stored slip needs the bottom taken as 40")
ok(top / 40 == Rat(11, 4) + Rat(13, 4) * I, "finding 4: (110 + 130i) / 40 = 2.75 + 3.25i, the stored value")

# finding 7: p-mesh-map part 1, each part squared with i^2 = -1 and no cross term
z0 = Rat(5, 2) + 3 * I
v = Rat(5, 2) ** 2 + (3 * I) ** 2 - 4 * z0
ok(sp.expand(v) == -Rat(51, 4) - 12 * I and abs((2.5 ** 2 - 9 - 4 * complex(2.5, 3)) - complex(-12.75, -12)) < 1e-12, "finding 7: 6.25 - 9 - (10 + 12i) = -12.75 - 12i")
ok(sp.expand(Rat(5, 2) ** 2 + 9 * I - 4 * z0) == -Rat(15, 4) - 3 * I, "finding 7: the stored -3.75 - 3i is 6.25 + 9i - (10 + 12i), the i left unsquared")

# finding 12: p-share-moments part 4
m1, m2 = 64 * sp.exp(Rat(4, 100)), 4096 * sp.exp(Rat(13, 100))
own = math.sqrt(4665 - 66.61 ** 2)
ok(round(own, 2) == 15.10 and abs(4665 - 66.61 ** 2 - 228.11) < 0.005, f"finding 12: own answers give variance {4665 - 66.61 ** 2:.2f} and sd {own:.3f}, 15.10")
ok(abs(15.10 - 15.08) > 0.01 + 0.005, "finding 12: an `own-rounding` band 15.10 +- 0.005 is clear of the key band 15.08 +- 0.01")
ex_var = float(sp.N(m2 - m1 ** 2))
giv_var = 4664.6 - 66.612 ** 2
ok(abs(ex_var - 227.47) <= 0.08 and abs(giv_var - 227.47) <= 0.08 and abs(227.4 - 227.47) < 0.08, f"finding 12: variance {giv_var:.3f} (handed-over values) and {ex_var:.3f} (unrounded) and the stored 227.4 all inside 227.47 +- 0.08")
ok(abs(228.11 - 227.47) > 0.08, "finding 12: the own-answer variance 228.11 stays outside that band (it has no line)")

# finding 14: p-lighthouse-flashes renumbered: 2.5 km out, opposite the point 0.5 km along; density c / (2x^2 - 2x + 13)
z, x = sp.symbols("z"), sp.symbols("x", real=True)
q = 2 * z ** 2 - 2 * z + 13
roots = sp.solve(q, z)
up = next(r for r in roots if sp.im(r) > 0)
upf = next(r for r in np.roots([2, -2, 13]) if r.imag > 0)
ok(up == Rat(1, 2) + Rat(5, 2) * I and abs(upf - complex(0.5, 2.5)) < 1e-12, "finding 14 part 1: pole 0.5 + 2.5i (roots (2 +- sqrt(-100)) / 4)")
ok(sp.expand(2 * (x - Rat(1, 2)) ** 2 + Rat(25, 2) - (2 * x ** 2 - 2 * x + 13)) == 0, "finding 14: 2x^2 - 2x + 13 = 2((x - 0.5)^2 + 2.5^2), the Cauchy at 0.5 with scale 2.5")
ok(sp.simplify((2 + 10 * I) / 2 - (1 + 5 * I)) == 0, "finding 14 part 1 wrong `no-four`: (2 + 10i) / 2 = 1 + 5i (divided by 2, not 2a = 4)")
res = sp.residue(1 / q, z, up)
th = np.linspace(0, 2 * np.pi, 4001)
c = upf + 0.5 * np.exp(1j * th)
resn = np.trapezoid(1 / (2 * c ** 2 - 2 * c + 13) * 0.5j * np.exp(1j * th), th) / (2j * np.pi)
ok(res == -I / 10 and abs(resn + 0.1j) < 1e-9 and sp.diff(q, z).subs(z, up) == 10 * I, "finding 14 part 2: q'(pole) = 10i, residue 1/(10i) = -i/10 = -0.1i")
ok(sp.simplify(1 / (4 * up) - (Rat(1, 52) - Rat(5, 52) * I)) == 0, "finding 14 part 2 wrong `q-prime` (q' = 4z): 1/(2 + 10i) = 1/52 - (5/52)i")
integral = sp.integrate(1 / (2 * x ** 2 - 2 * x + 13), (x, -sp.oo, sp.oo))
inum = integrate.quad(lambda t: 1 / (2 * t * t - 2 * t + 13), -np.inf, np.inf)[0]
ok(sp.simplify(integral - pi / 5) == 0 and abs(inum - math.pi / 5) < 1e-9, "finding 14 part 3: integral pi/5 = 2 pi i (-i/10)")
ok(near(5 / pi, 1.592, 5e-4) and near(pi / 5, 0.628, 5e-4) and near(5 / (2 * pi), 0.796, 5e-4) and near(10 / pi, 3.183, 5e-4),
   "finding 14 part 3: c = 5/pi = 1.592; wrongs integral 0.628, both-poles 0.796, no-two 3.183")
phi1 = sp.simplify((5 / pi) * 2 * pi * I * sp.exp(I * up) / (10 * I))
re_part = 2 * integrate.quad(lambda t: 1 / (2 * t * t + 12.5), 0, np.inf, weight="cos", wvar=1)[0]
phin = (5 / math.pi) * cmath.exp(0.5j) * re_part
ok(sp.simplify(phi1 - sp.exp(I / 2 - Rat(5, 2))) == 0 and abs(abs(phin) - math.exp(-2.5)) < 1e-8, "finding 14 part 4: phi(1) = e^{i/2 - 5/2}, size e^{-2.5}")
ok(near(sp.exp(-Rat(5, 2)), 0.0821) and near(sp.exp(Rat(5, 2)), 12.1825) and near(pi / 5 * sp.exp(-Rat(5, 2)), 0.0516) and near(sp.exp(-1), 0.3679),
   "finding 14 part 4: key 0.0821; wrongs sign 12.1825, no-c 0.0516, standard 0.3679")
phi = lambda u: sp.exp(I * u / 2 - 5 * u / 2)
ok(abs(complex(sp.N(phi(Rat(1, 2)) ** 2 - phi(1)))) < 1e-15, "finding 14 part 5: phi(1/2)^2 = phi(1)")
rng = np.random.default_rng(5)
hits = 0.5 + 2.5 * np.tan(rng.uniform(-np.pi / 2, np.pi / 2, 600000))
m = (hits[:300000] + hits[300000:]) / 2
ok(abs(abs(np.mean(np.exp(1j * m))) - math.exp(-2.5)) < 0.01 and abs(abs(np.mean(np.exp(1j * hits))) - math.exp(-2.5)) < 0.01, "finding 14 parts 4 and 5: simulated sizes are e^{-2.5} to Monte Carlo error")
ok(near(sp.exp(-5), 0.0067) and near(sp.exp(-Rat(5, 4)), 0.2865), "finding 14 part 5: key 0.0821; wrongs no-half e^{-5} = 0.0067, one-factor e^{-1.25} = 0.2865")
vals = sorted([0.0821, 12.1825, 0.0516, 0.3679]) + sorted([0.0821, 0.0067, 0.2865])
ok(min(abs(a - b) for i, a in enumerate(vals[:4]) for b in vals[:i]) > 0.0002 and abs(0.0821 - 0.0067) > 0.0002, "finding 14: the new bands of 0.0001 are apart")

print(f"proposed.py: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
