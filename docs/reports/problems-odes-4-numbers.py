"""Recompute every stated number in odes problems-4 (level 4).

Each key is found twice: exactly (sympy: Laplace transforms, apart,
dsolve, exact limits) and by a second route (numerical quadrature, direct
time stepping, scipy solve_ivp, brute-force search). Each wrong value is
rebuilt from its slip and shown to differ from its key. Exit 0 when all hold.
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp

fails = []


def check(name, a, b, tol=1e-9):
    ok = abs(complex(a) - complex(b)) <= tol
    if not ok:
        fails.append(name)
    print(("ok  " if ok else "FAIL"), name, a, b)


def truth(name, cond):
    if not cond:
        fails.append(name)
    print(("ok  " if cond else "FAIL"), name)


def differs(name, key, wrongs, keytol):
    for w in wrongs:
        if abs(w - key) <= keytol:
            fails.append(f"{name} wrong {w} inside key band")
    print("ok   wrongs differ:", name)


s, t = sp.symbols("s t", positive=True)
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "..", "..", "app", "content", "courses", "odes", "problems-4.json")))
items = {i["id"]: i for i in d["items"]}

# ------------------------------------------------ p-test-rig (y'' + 6y' + 8y = 24e^-8t)
F = sp.laplace_transform(24 * sp.exp(-8 * t), t, s, noconds=True)
check("rig L{24e^-8t} exact", sp.simplify(F - 24 / (s + 8)), 0)
check("rig L{24e^-8t} at s=1 by quadrature", quad(lambda u: math.exp(-u) * 24 * math.exp(-8 * u), 0, 60)[0], 24 / 9, 1e-8)
Y = sp.simplify(F / (s**2 + 6 * s + 8))
check("rig Y exact", sp.simplify(Y - 24 / ((s + 2) * (s + 4) * (s + 8))), 0)
check("rig factor", sp.expand((s + 2) * (s + 4) - (s**2 + 6 * s + 8)), 0)
res = {p: sp.limit((s - p) * Y, s, p) for p in (-2, -4, -8)}
check("rig residue -2", res[-2], 2); check("rig residue -4", res[-4], -3); check("rig residue -8", res[-8], 1)
check("rig residues sum (y(0)=0)", sum(res.values()), 0)
check("rig apart (route 2)", sp.simplify(sp.apart(Y, s) - (2 / (s + 2) - 3 / (s + 4) + 1 / (s + 8))), 0)
differs("rig part3", -3, [3, 2], 0)
# not l15's example shifted and scaled: poles not equally spaced
truth("rig poles unequally spaced (not l15 shifted)", (-4) - (-8) != (-2) - (-4))
tt = sp.symbols("tt", real=True)
yy = sp.Function("y")
sol = sp.dsolve(yy(tt).diff(tt, 2) + 6 * yy(tt).diff(tt) + 8 * yy(tt) - 24 * sp.exp(-8 * tt), yy(tt),
                ics={yy(0): 0, yy(tt).diff(tt).subs(tt, 0): 0}).rhs
ykey = 2 * sp.exp(-2 * tt) - 3 * sp.exp(-4 * tt) + sp.exp(-8 * tt)
check("rig y(t) dsolve vs key", sp.simplify(sol - ykey), 0)
check("rig y(t) factored form (u = e^-2t)", sp.simplify(ykey - sp.exp(-2 * tt) * (1 - sp.exp(-2 * tt))**2 * (sp.exp(-2 * tt) + 2)), 0)
check("rig y'(0)", sp.diff(ykey, tt).subs(tt, 0), 0)
num = solve_ivp(lambda u, z: [z[1], 24 * math.exp(-8 * u) - 6 * z[1] - 8 * z[0]], [0, 5], [0, 0], rtol=1e-11, atol=1e-13, dense_output=True)
check("rig y(1) numeric vs closed", num.sol(1)[0], float(ykey.subs(tt, 1)), 1e-8)
check("rig carried-sign y(0)", 2 + 3 + 1, 6)
grid = np.linspace(0, 5, 500001); yv = num.sol(grid)[0]
peak = (6 * math.sqrt(3) - 9) / 4
check("rig peak exact", peak, 0.348076, 1e-6)
check("rig peak by grid search", yv.max(), peak, 1e-8); check("rig peak time grid", grid[yv.argmax()], 0.5 * math.log(1 + math.sqrt(3)), 1e-4)
check("rig u at peak", (math.sqrt(3) - 1) / 2, 0.3660, 5e-5)
check("rig slip time", round(0.5 * math.log(1 + math.sqrt(3)), 4), 0.5025)
check("rig slip y(1)", round(float(ykey.subs(tt, 1)), 4), 0.2161)
differs("rig part5", 0.3481, [0.366 + 0.0005, 0.5025 + 0.0005, 0.2161 + 0.0005], 0.0005)

# ------------------------------------------------ p-skydiver-check
V = sp.simplify((sp.Rational(49, 5) / s) / (s + sp.Rational(1, 5)))
check("sky V exact", sp.simplify(V - sp.Rational(49, 5) / (s * (s + sp.Rational(1, 5)))), 0)
check("sky V alt form 49/(s(5s+1))", sp.simplify(V - 49 / (s * (5 * s + 1))), 0)
r0 = sp.limit(s * V, s, 0); r1 = sp.limit((s + sp.Rational(1, 5)) * V, s, -sp.Rational(1, 5))
check("sky residue 0", r0, 49); check("sky residue -0.2", r1, -49)
vt = 49 * (1 - sp.exp(-tt / 5))
v2 = float(vt.subs(tt, 2))
check("sky v(2) closed", round(v2, 4), 16.1543)
f = lambda v: 9.8 - 0.2 * v
v2n = solve_ivp(lambda u, z: [f(z[0])], [0, 2], [0], rtol=1e-12, atol=1e-12).y[0, -1]
check("sky v(2) solve_ivp", v2n, v2, 1e-8)
check("sky e^-0.4 stated", round(math.exp(-0.4), 6), 0.670320); check("sky 1-e^-0.4 stated", round(1 - math.exp(-0.4), 6), 0.329680)
check("sky slip no-divide", round(9.8 * (1 - math.exp(-0.4)), 4), 3.2309)
check("sky slip carried-constant", round(9.8 * math.exp(-0.4), 4), 6.5691)
check("sky slip carried-sign", round(49 * (math.exp(0.4) - 1), 4), 24.0994)
differs("sky part2", 16.1543, [3.2309, 6.5691, 24.0994], 0.0001 + 0.0001)
def euler(n, T=2.0):
    h = T / n; v = 0.0
    for _ in range(n):
        v += h * f(v)
    return v
def rk4(n, T=2.0, weights=(1, 2, 2, 1), scale=None):
    h = T / n; v = 0.0
    for _ in range(n):
        k1 = f(v); k2 = f(v + h / 2 * k1); k3 = f(v + h / 2 * k2); k4 = f(v + h * k3)
        ks = (k1, k2, k3, k4)
        v += (scale if scale is not None else h / 6) * sum(w * k for w, k in zip(weights, ks))
    return v
check("sky Euler 2 steps", euler(2), 17.64, 1e-12)
check("sky Euler 2 steps exact fractions", sp.Rational(49, 5) + (sp.Rational(49, 5) - sp.Rational(1, 5) * sp.Rational(49, 5)), sp.Rational(441, 25))
check("sky Euler slip same-slope (one step h=2)", euler(1), 19.6, 1e-12)
check("sky Euler error stated", round(17.64 - v2, 4), 1.4857)
differs("sky part3", 17.64, [19.6], 0.005 + 0.005)
check("sky RK4 one step", round(rk4(1), 4), 16.1504)
k1 = sp.Rational(49, 5); fx = lambda v: sp.Rational(49, 5) - sp.Rational(1, 5) * v
k2 = fx(k1); k3 = fx(k2); k4 = fx(2 * k3)
check("sky k2", k2, 7.84); check("sky k3", k3, 8.232); check("sky k4", k4, 6.5072); check("sky 2*k3", 2 * k3, 16.464)
check("sky weighted sum", k1 + 2 * k2 + 2 * k3 + k4, 48.4512); check("sky RK4 exact", sp.Rational(1, 3) * (k1 + 2 * k2 + 2 * k3 + k4), 16.1504)
check("sky RK4 slip plain-mean", round(rk4(1, weights=(1, 1, 1, 1), scale=2 / 4), 4), 16.1896)
check("sky RK4 slip no-h", round(rk4(1, scale=1 / 6), 4), 8.0752)
differs("sky part4", 16.1504, [16.1896, 8.0752], 0.0002)
e1 = abs(rk4(1) - v2)
check("sky RK4 1-step error stated 0.0039", round(e1, 4), 0.0039)
pred = {n: 0.0039 / (n ** 4) for n in (1, 2, 4, 8)}
first_pred = next(n for n in (1, 2, 4, 8) if pred[n] < 5e-5)
first_true = next(n for n in (1, 2, 4, 8) if abs(rk4(n) - v2) < 5e-5)
check("sky first n predicted", first_pred, 4); check("sky first n actual", first_true, 4)
check("sky stated pred n=2", round(pred[2], 5), 0.00024); check("sky stated pred n=4", round(pred[4], 6), 0.000015)
check("sky stated actual n=2", round(abs(rk4(2) - v2), 6), 0.000207); check("sky stated actual n=4", round(abs(rk4(4) - v2), 7), 0.0000119)
first_order = next(n for n in (2 ** k for k in range(12)) if 0.0039 / n < 5e-5)
check("sky slip first-order", first_order, 128)
truth("sky slip half-unit: n=2 below 5e-4 not 5e-5", pred[2] < 5e-4 and pred[2] > 5e-5)
differs("sky part5", 4, [2, 128], 0)

# ------------------------------------------------ p-dose-simulator
A = sp.Matrix([[-6, 0], [6, -sp.Rational(1, 2)]])
ev = sorted(A.eigenvals().keys())
check("dose eigenvalue -6", ev[0], -6); check("dose eigenvalue -0.5", ev[1], -0.5)
evn = sorted(np.linalg.eigvals(np.array([[-6, 0], [6, -0.5]])).real)
check("dose eigenvalues numpy", evn[0], -6, 1e-12); check("dose eigenvalues numpy 2", evn[1], -0.5, 1e-12)
check("dose Euler factor h=0.5", 1 + 0.5 * (-6), -2); check("dose slip slow-mode factor", 1 + 0.5 * (-0.5), 0.75)
g = 1.0
for _ in range(3):
    g = g + 0.5 * (-6 * g)
check("dose Euler gut after 3 steps of 0.5 (factor cubed)", g, (-2) ** 3)
hh = sp.symbols("hh", positive=True)
lim_e = sp.solve(sp.Eq(1 - 6 * hh, -1), hh)[0]
check("dose Euler limit exact 1/3", lim_e, sp.Rational(1, 3))
hs = np.linspace(0.001, 1, 100000); ok_e = hs[np.abs(1 - 6 * hs) < 1]
check("dose Euler limit by scan", ok_e.max(), 1 / 3, 2e-5)
check("dose Euler limit 4dp", round(1 / 3, 4), 0.3333)
check("dose slip slow-mode limit", 2 / 0.5, 4); check("dose slip no-two", round(1 / 6, 4), 0.1667)
differs("dose part3", 0.3333, [4, 0.1667], 0.0001 + 0.0001)
R = lambda z: 1 - z + z**2 / 2 - z**3 / 6 + z**4 / 24
zs = np.linspace(0.001, 4, 400001); zmax = zs[np.abs(R(zs)) < 1].max()
check("dose RK4 region edge 2.7853", round(zmax, 4), 2.7853)
check("dose RK4 limit", round(2.7853 / 6, 4), 0.4642)
check("dose RK4 limit from scanned edge", round(zmax / 6, 4), 0.4642)
check("dose slip RK4 slow-mode", round(2.7853 / 0.5, 4), 5.5706)
differs("dose part4", 0.4642, [5.5706, 0.3333], 0.0002)
n_e = next(n for n in range(1, 1000) if 24 / n < 1 / 3)
n_r = next(n for n in range(1, 1000) if 24 / n < 2.7853 / 6)
check("dose Euler fewest stable steps", n_e, 73); check("dose RK4 fewest stable steps", n_r, 52)
check("dose 24/0.4642 stated", round(24 / (2.7853 / 6), 1), 51.7)
truth("dose n=72 not stable (|1-6h| = 1)", abs(1 - 6 * (24 / 72)) >= 1 - 1e-12)
check("dose readings Euler", n_e * 1, 73); check("dose readings RK4", n_r * 4, 208)
check("dose cheaper", min(n_e, 4 * n_r), 73)
# second route: simulate the fast mode for 24 h with each step count
grow = lambda n, factor: abs(factor(24 / n)) ** n
truth("dose Euler 73 steps decays", grow(73, lambda h: 1 - 6 * h) < 1)
truth("dose RK4 52 steps decays", grow(52, lambda h: R(6 * h)) < 1 and grow(51, lambda h: R(6 * h)) > 1)
check("dose gain under 40%", round((2.7853 / 6) / (1 / 3), 3), 1.393)
differs("dose part5", 73, [208, 72, 52], 0)

# ------------------------------------------------ keys stored in the JSON
want = {
    "p-test-rig": [24 / (s + 8), 24 / ((s + 2) * (s + 4) * (s + 8)), -3, ykey, 0.3481],
    "p-skydiver-check": [V, 16.1543, 17.64, 16.1504, 4],
    "p-dose-simulator": [[-6, -0.5], -2, 0.3333, 0.4642, 73],
}
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def from_tex(tx):
    import re
    tx = re.sub(r"\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{(.*)\}$", r"(\1)/(\2)", tx)
    tx = re.sub(r"e\^\{([^}]*)\}", r"exp(\1)", tx)
    return parse_expr(tx, local_dict={"s": s, "t": tt, "exp": sp.exp}, transformations=TR)
for iid, vals in want.items():
    for k, (part, w) in enumerate(zip(items[iid]["parts"], vals), 1):
        wd = part["widget"]; name = f"key {iid} part {k}"
        if "answers" in wd:
            truth(name, sorted(wd["answers"]) == sorted(w))
        elif isinstance(wd["answer"], (int, float)):
            check(name, wd["answer"], w, wd["tol"]["abs"] + 1e-12)
        else:
            got = from_tex(wd["answer"])
            check(name, sp.simplify(got - w), 0)
check("every part keyed", sum(len(i["parts"]) for i in d["items"]), 15)

print("\n%d failures" % len(fails))
for f_ in fails:
    print("  ", f_)
sys.exit(1 if fails else 0)
