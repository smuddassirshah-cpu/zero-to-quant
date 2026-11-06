"""Concept checks for pdes L1 (l1 to l4, review-1, homework-1).

Every analytic claim is checked symbolically (sympy) or by quadrature, every empirical claim
by simulation, and every code widget's solution is run against its hidden tests with the
starter run as well. Each assert names the ledger row it covers
(docs/reports/audit-pdes-1-3-ledger.md). Run from the repo root:
    python3 -I docs/reports/pdes-L1-concepts.py
Exit 0 means the content is correct as far as these checks reach. A check marked
EXPECTED_FAIL fails because the content is wrong; the corrected assert sits beside it.
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy import stats, integrate, special

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(ROOT, "..", "app", "content", "courses", "pdes")
COURSE = os.path.normpath(COURSE)
Phi = stats.norm.cdf


def load(name):
    with open(os.path.join(COURSE, name)) as f:
        return json.load(f)


# ---------- code widget harness (shared pattern with the other two scripts) ----------
def run_case(ns, case):
    local = dict(ns)
    if case.get("setup"):
        exec(case["setup"], local)
    cmp = case.get("compare", "isclose")
    if cmp == "raises":
        try:
            eval(case["call"], local)
            return False
        except Exception as e:
            return type(e).__name__ == case["expect"]
    try:
        got = eval(case["call"], local)
    except Exception:
        return False
    exp = eval(case["expect"], local)
    if cmp == "equal":
        return got == exp
    tol = case.get("tol", {})
    a, r = tol.get("abs", 1e-6), tol.get("rel", 0)

    def close(g, e):
        return abs(float(g) - float(e)) <= max(a, r * abs(float(e)))
    if isinstance(exp, (list, tuple)):
        return len(got) == len(exp) and all(close(g, e) for g, e in zip(got, exp))
    return close(got, exp)


def check_code(label, w):
    base = {"np": np, "math": math}
    if w.get("prelude"):
        exec(w["prelude"], base)
    sol = dict(base)
    exec(w["solution"], sol)
    if w.get("prelude"):
        exec(w["prelude"], sol)
    fails = [i for i, c in enumerate(w["tests"]) if not run_case(sol, c)]
    assert not fails, f"{label}: solution fails tests {fails}"
    st = dict(base)
    try:
        exec(w["starter"], st)
        if w.get("prelude"):
            exec(w["prelude"], st)
        passes = sum(run_case(st, c) for c in w["tests"])
    except Exception:
        passes = 0
    assert passes < len(w["tests"]), f"{label}: starter passes every test"
    return sol


def bs_call(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)


# =============================== l1 ===============================
x, t, D = sp.symbols("x t D", positive=True)
# l1 screens[0]: the call surface numbers (10.45 at tau = 1, about 1.18 at tau = 0.02, 6.89 at tau = 0.5)
assert abs(bs_call(100, 100, 0.05, 0.2, 1) - 10.4506) < 6e-5, "l1 screens[0].explain: 10.45"
assert abs(bs_call(100, 100, 0.05, 0.2, 0.02) - 1.18) < 0.01, "l1 screens[0].explain: about 1.18"
assert abs(bs_call(100, 100, 0.05, 0.2, 0.5) - 6.89) < 0.005, "l1 screens[10].hints: 6.89"

# l1 screens[1]: e^{-t} sin x solves u_t = u_xx; at (pi/2, 1) both are -e^{-1}
u = sp.exp(-t) * sp.sin(x)
assert sp.simplify(sp.diff(u, t) - sp.diff(u, x, 2)) == 0, "l1 screens[1].explain: u_t = u_xx everywhere"
assert abs(float(sp.diff(u, t).subs({x: sp.pi / 2, t: 1})) + math.exp(-1)) < 1e-12, "l1 screens[1].explain: -0.367879"

# l1 screens[3]: candidates' residuals
res = lambda f: sp.simplify(sp.diff(f, t) - sp.diff(f, x, 2))
assert res(sp.exp(-4 * t) * sp.sin(2 * x)) == 0, "l1 screens[3] option a: residual 0"
assert sp.simplify(res(sp.exp(-t) * sp.sin(2 * x)) - 3 * sp.exp(-t) * sp.sin(2 * x)) == 0, "l1 screens[3] option b why: residual 3e^{-t} sin 2x"
assert res(sp.exp(-2 * t) * sp.sin(2 * x)) != 0 and res(sp.exp(-4 * t) * sp.sin(x)) != 0, "l1 screens[3] options c, d"

# l1 screens[4]: transport f(x - 2t) solves u_t + 2u_x = 0; u(3,1) = e^{-1}
g = sp.Function("g")
v = g(x - 2 * t)
assert sp.simplify(sp.diff(v, t) + 2 * sp.diff(v, x)) == 0, "l1 screens[4].prose: f(x - 2t) solves transport"
assert abs(math.exp(-(3 - 2) ** 2) - 0.3679) < 5e-5, "l1 screens[4]: u(3,1) = e^{-1}"
assert abs(math.exp(-(5 - 3) ** 2) - 0.0183) < 5e-5, "l1 quiz q-transport: e^{-4}"
assert abs(math.exp(-9) - 0.000123) < 1e-6, "l1 screens[4].byKey.unmoved: e^{-9}"

# l1 screens[5], [7], [9], quiz: discriminant B^2 - 4AC and type
disc = lambda A, B, C: B * B - 4 * A * C
assert disc(1, 0, 0) == 0 and disc(4, 0, -1) == 16 and disc(1, 0, 1) == -4, "l1 screens[5] table"
assert disc(1, 0, -1) == 4 > 0 and disc(1, 0, 1) < 0, "l1 screens[7]: -4x at x = -1 hyperbolic, x = 1 elliptic"
assert disc(1, 2, 1) == 0, "l1 screens[9]: cross term parabolic"
assert disc(3, 4, 1) == 4 > 0, "review-1 r-classify: hyperbolic"
assert disc(1, 0, 1 - 2) == 4 > 0, "l1 quiz q-tricomi: hyperbolic at x = 1"
# Black-Scholes principal part: A = sigma^2 S^2/2, B = C = 0 -> parabolic for every S > 0
S_, sig_ = sp.symbols("S sigma", positive=True)
assert disc(sig_ ** 2 * S_ ** 2 / 2, 0, 0) == 0, "l1 screens[10].prose: Black-Scholes parabolic"
# characteristic quadratic A m^2 + B m + C has the same discriminant (l1 screens[9].prose)
m = sp.symbols("m")
A_, B_, C_ = sp.symbols("A B C")
assert sp.discriminant(A_ * m ** 2 + B_ * m + C_, m) == B_ ** 2 - 4 * A_ * C_, "l1 screens[9].prose: same discriminant"

# l1 screens[6] trap: Black-Scholes is linear (superposition), u u_x is not
V1, V2 = sp.Function("V1")(S_, t), sp.Function("V2")(S_, t)
r_ = sp.symbols("r", positive=True)
Lop = lambda V: sp.diff(V, t) + sig_ ** 2 * S_ ** 2 / 2 * sp.diff(V, S_, 2) + r_ * S_ * sp.diff(V, S_) - r_ * V
assert sp.simplify(Lop(V1 + V2) - Lop(V1) - Lop(V2)) == 0, "l1 screens[6]: sums of solutions are solutions"
Nop = lambda U: sp.diff(U, t) + U * sp.diff(U, x)
U1, U2 = sp.Function("U1")(x, t), sp.Function("U2")(x, t)
assert sp.simplify(Nop(U1 + U2) - Nop(U1) - Nop(U2)) != 0, "l1 screens[6] table: u u_x breaks linearity"

# l1 quiz q-residual: (1 - t) sin x has residual -t sin x
assert sp.simplify(res((1 - t) * sp.sin(x)) + t * sp.sin(x)) == 0, "l1 quiz q-residual: residual -t sin x"
# l1 screens[8] code tests (heat_residual expected 1.386870 etc.)
l1 = load("l1-equations-in-two-variables.json")
check_code("l1 screens[8] code", l1["screens"][8]["widget"])
assert abs(3 * math.exp(-0.2) * math.sin(0.6) - 1.386870) < 1e-5, "l1 screens[8] test: 3e^{-t} sin 2x at (0.3, 0.2)"

# =============================== l2 ===============================
# l2 screens[0]: spread of a +-1 walk is sqrt(n): 5 at 25, 10 at 100 (simulation)
rng = np.random.default_rng(1)
steps = rng.choice([-1, 1], size=(200000, 100))
pos = steps.cumsum(axis=1)
assert abs(pos[:, 24].std() - 5) < 0.05 and abs(pos[:, 99].std() - 10) < 0.1, "l2 screens[0]: sd 5 then 10 (sim: l2_walk_sd)"

# l2 screens[1]: averaging rule gives the binomial rows
p = np.array([0, 0, 1, 0, 0.0])
avg = lambda p: 0.5 * np.roll(p, 1) + 0.5 * np.roll(p, -1)
assert np.allclose(avg(p), [0, .5, 0, .5, 0]) and np.allclose(avg(avg(p)), [.25, 0, .5, 0, .25]), "l2 screens[1]: 1/4, 1/2, 1/4"

# l2 screens[2] derive: Taylor expansion of the averaging rule gives u_t = (dx^2 / 2 dt) u_xx
dx, dt = sp.symbols("dx dt", positive=True)
uf = sp.Function("u")
lhs = uf(x, t) + dt * sp.diff(uf(x, t), t)  # first order in time
rhs = sp.Rational(1, 2) * (uf(x, t) - dx * sp.diff(uf(x, t), x) + dx ** 2 / 2 * sp.diff(uf(x, t), x, 2)) \
    + sp.Rational(1, 2) * (uf(x, t) + dx * sp.diff(uf(x, t), x) + dx ** 2 / 2 * sp.diff(uf(x, t), x, 2))
assert sp.simplify(rhs - uf(x, t) - dx ** 2 / 2 * sp.diff(uf(x, t), x, 2)) == 0, "l2 screens[2] line a4: u_x terms cancel"
assert sp.simplify(sp.solve(sp.Eq(lhs, rhs), sp.diff(uf(x, t), t))[0] - dx ** 2 / (2 * dt) * sp.diff(uf(x, t), x, 2)) == 0, "l2 screens[2] line a5: D = dx^2/(2 dt)"
assert abs(0.1 ** 2 / (2 * 0.005) - 1) < 1e-12, "l2 screens[3] trap: D = 1"
assert abs(0.2 ** 2 / (2 * 0.01) - 2) < 1e-12 and abs(0.01 ** 2 / 0.02 - 0.005) < 1e-12, "l2 screens[9], quiz q-d-small"
assert abs(0.3 ** 2 / 0.06 - 1.5) < 1e-12, "review-1 r-d-walk"

# l2 screens[4]: variance at t = 2 is 400 steps * 0.01 = 4 = 2Dt (sim)
w = rng.choice([-0.1, 0.1], size=(100000, 400)).sum(axis=1)
assert abs(w.var() - 4) < 0.05, "l2 screens[4]: variance 4 = 2Dt (sim: l2_var)"

# l2 screens[5]: log derivative of the kernel and the kernel solving the heat equation
k = sp.exp(-x ** 2 / (4 * D * t)) / sp.sqrt(4 * sp.pi * D * t)
assert sp.simplify(sp.diff(k, t) / k - (-1 / (2 * t) + x ** 2 / (4 * D * t ** 2))) == 0, "l2 screens[5]: u_t/u"
assert sp.simplify(sp.diff(k, x) / k + x / (2 * D * t)) == 0, "l2 screens[5].explain: u_x/u"
assert sp.simplify(sp.diff(k, x, 2) / k - (x ** 2 / (4 * D ** 2 * t ** 2) - 1 / (2 * D * t))) == 0, "l2 screens[5].explain: u_xx/u"
assert sp.simplify(sp.diff(k, t) - D * sp.diff(k, x, 2)) == 0, "l2 screens[5].explain: Gaussian solves u_t = D u_xx"

# l2 screens[6]: P(S_100 = 0) exact and the density at 0
assert abs(math.comb(100, 50) / 2 ** 100 - 0.079589) < 5e-7, "l2 screens[6]: 0.079589"
assert abs(1 / math.sqrt(200 * math.pi) - 0.0399) < 5e-5, "l2 screens[6].prose: 0.0399"
assert abs(2 * 0.0399 - 0.0798) < 1e-9, "l2 screens[6].explain: density times spacing 2"

# l2 screens[7]: biased walk gives u_t + c u_x = D u_xx with c = (2q - 1) dx / dt
q = sp.symbols("q", positive=True)
rhs_b = q * (uf(x, t) - dx * sp.diff(uf(x, t), x) + dx ** 2 / 2 * sp.diff(uf(x, t), x, 2)) \
    + (1 - q) * (uf(x, t) + dx * sp.diff(uf(x, t), x) + dx ** 2 / 2 * sp.diff(uf(x, t), x, 2))
ut_b = sp.solve(sp.Eq(lhs, rhs_b), sp.diff(uf(x, t), t))[0]
assert sp.simplify(ut_b + (2 * q - 1) * dx / dt * sp.diff(uf(x, t), x) - dx ** 2 / (2 * dt) * sp.diff(uf(x, t), x, 2)) == 0, "l2 screens[7]: c = (2q-1)dx/dt"
assert abs((2 * 0.55 - 1) * 0.1 / 0.005 - 2) < 1e-12, "l2 screens[7]: c = 2"

# l2 screens[8] code
l2 = load("l2-heat-equation.json")
check_code("l2 screens[8] code", l2["screens"][8]["widget"])

# l2 screens[10] transfer: D = sigma^2/2, sd over three months 0.1
assert abs(math.sqrt(2 * 0.02 * 0.25) - 0.1) < 1e-12, "l2 screens[10]: sqrt(2Dt) = 0.1"
# l2 quiz
assert abs(math.exp(-0.5) / math.sqrt(2 * math.pi) - 0.2420) < 5e-5, "l2 quiz q-phi"
assert abs(math.comb(3, 2) / 8 - 0.375) < 1e-12, "l2 quiz q-three-steps"

# =============================== l3 ===============================
kern = lambda y, tt, DD=1.0: np.exp(-y ** 2 / (4 * DD * tt)) / np.sqrt(4 * np.pi * DD * tt)
assert abs(kern(0, 1) - 0.282) < 5e-4 and abs(kern(0, 4) - 0.141) < 5e-4, "l3 screens[0]: peak 0.282 at t = 1, 0.141 at t = 4"
assert abs(kern(0, 4) / kern(0, 1) - 0.5) < 1e-12, "l3 screens[0].explain: quadrupling t halves the peak"
# kernel is the density of sqrt(2Dt) Z: area 1, variance 2Dt
area, _ = integrate.quad(lambda y: kern(y, 0.7, 1.3), -40, 40)
var, _ = integrate.quad(lambda y: y * y * kern(y, 0.7, 1.3), -40, 40)
assert abs(area - 1) < 1e-9 and abs(var - 2 * 1.3 * 0.7) < 1e-8, "l3 screens[2].prose: area 1, variance 2Dt"
assert abs(math.sqrt(2 * 1 * 8) - 4) < 1e-12 and abs(0.447214 ** 2 * 80 - 16) < 1e-4, "l3 screens[2]: width 4; 80 steps of N(0, 0.2)"

# l3 screens[1], [3], quiz q-step-d, review r-step-neg: step start gives Phi(x / sqrt(2Dt))
def heat_line(u0, x0, tt, DD=1.0, n=40001):
    wdt = math.sqrt(2 * DD * tt)
    y = np.linspace(x0 - 12 * wdt, x0 + 12 * wdt, n)
    f = kern(x0 - y, tt, DD) * u0(y)
    return np.trapezoid(f, y)
STEP = lambda y: np.where(y > 0, 1.0, np.where(y == 0, 0.5, 0.0))
for x0, tt, DD in [(0, 0.5, 1), (1, 0.5, 1), (2, 2, 0.5), (-1, 1, 1), (0, 2, 1)]:
    val, _ = integrate.quad(lambda y: kern(x0 - y, tt, DD), 0, x0 + 15 * math.sqrt(2 * DD * tt))
    assert abs(val - Phi(x0 / math.sqrt(2 * DD * tt))) < 1e-8, f"l3 step start at ({x0},{tt},{DD}) = Phi(x/sqrt(2Dt))"
assert abs(Phi(1) - 0.8413) < 5e-5 and abs(Phi(2 / math.sqrt(2)) - 0.9214) < 5e-5 and abs(Phi(-1 / math.sqrt(2)) - 0.2398) < 5e-5, "l3 screens[3], quiz q-step-d, review r-step-neg"

# l3 screens[4], [5]: bump e^{-x^2} spreads to e^{-x^2/(1+4t)}/sqrt(1+4t) (closed form checked by sympy and by quadrature)
bump = sp.exp(-x ** 2 / (1 + 4 * t)) / sp.sqrt(1 + 4 * t)
assert sp.simplify(sp.diff(bump, t) - sp.diff(bump, x, 2)) == 0, "l3 screens[4].prose: closed form solves u_t = u_xx"
assert sp.simplify(bump.subs(t, 0) - sp.exp(-x ** 2)) == 0, "l3 screens[4].prose: closed form matches the start"
BUMP = lambda y: np.exp(-y ** 2)
assert abs(heat_line(BUMP, 0, 1) - 1 / math.sqrt(5)) < 1e-7 and abs(heat_line(BUMP, 1, 1) - 0.366148) < 1e-6, "l3 screens[4]: u(0,1) = 1/sqrt5; u(1,1) = 0.366148"
tot, _ = integrate.quad(lambda y: math.exp(-y * y / 9) / 3, -60, 60)
assert abs(tot - math.sqrt(math.pi)) < 1e-9 and abs(math.sqrt(math.pi) - 1.7725) < 5e-5, "l3 screens[5]: total heat conserved, sqrt(pi)"
# general Gaussian start (homework-1 h-gauss-general): a / sqrt(a^2 + 2Dt)
a_ = 2.0
assert abs(heat_line(lambda y: np.exp(-y ** 2 / (2 * a_ ** 2)), 0, 2, 0.5) - a_ / math.sqrt(a_ ** 2 + 2 * 0.5 * 2)) < 1e-7, "homework-1 h-gauss-general: a/sqrt(a^2+2Dt)"
assert abs(2 / math.sqrt(6) - 0.8165) < 5e-5, "homework-1 h-gauss-general: 0.8165"

# l3 screens[6] trap: width grows like sqrt t
assert abs(math.sqrt(2 * 2) / math.sqrt(2 * 1) - math.sqrt(2)) < 1e-12, "l3 screens[6]: factor sqrt 2"
assert abs(0.5 * math.sqrt(9) - 1.5) < 1e-12, "review-1 r-width-later"

# l3 screens[7], quiz q-back, review r-back: mode sin kx scales by e^{-k^2 D t} forwards
mode = sp.exp(-100 * D * t) * sp.sin(10 * x)
assert sp.simplify(sp.diff(mode, t) - D * sp.diff(mode, x, 2)) == 0, "l3 screens[7].prose: sin 10x decays by e^{-100Dt}"
assert abs(math.exp(10) - 22026.47) < 0.01 and abs(math.exp(9) - 8103) < 1 and abs(math.exp(8) - 2981) < 1, "l3 screens[7], quiz q-back, review r-back"
# backward heat is ill-posed: a 1e-6 error in sin 10x data at t = 0.1 becomes e^{10} * 1e-6 at t = 0 (spectral solve)
assert abs(1e-6 * math.exp(100 * 0.1) - 0.0220) < 1e-4, "l3 screens[7].explain: tiny error destroys the answer"

# l3 screens[8] code
l3 = load("l3-heat-kernel.json")
check_code("l3 screens[8] code", l3["screens"][8]["widget"])
assert abs(kern(1, 0.5, 0.5) - 0.207554) < 1e-6, "l3 screens[8] test: kernel(1, 0.5, 0.5)"

# l3 screens[10] transfer, quiz
assert abs(Phi(1) - Phi(-1) - 0.6827) < 5e-5, "l3 screens[10]: 0.6827"
assert abs(1 / math.sqrt(4 * math.pi) - 0.2821) < 5e-5 and abs(math.sqrt(0.5) - 0.7071) < 5e-5, "l3 quiz q-peak, q-width"
assert abs(1 / math.sqrt(3 * math.pi) - 0.3257) < 5e-5, "review-2 r-kernel-peak (same formula)"

# =============================== l4 ===============================
# l4 screens[0]: the series in the canvas equals 20 + 30x/pi at large t and 100 at t -> 0 (interior)
xs = np.linspace(0.05, math.pi - 0.05, 200)


def rod_series_l4(xx, tt, K=400):
    s = 20 + 30 * xx / math.pi
    for kk in range(1, K + 1):
        b = (2 / math.pi) * (80 * (1 - math.cos(kk * math.pi)) / kk + 30 * math.cos(kk * math.pi) / kk)
        s = s + b * math.exp(-kk * kk * tt) * np.sin(kk * xx)
    return s
assert np.abs(rod_series_l4(xs, 1e-4, 2000) - 100).max() < 0.5, "l4 screens[0] canvas: start 100 (series coefficients)"
assert abs(rod_series_l4(np.array([math.pi / 2]), 6)[0] - 35) < 0.5 and abs(rod_series_l4(np.array([math.pi / 2]), 25)[0] - 35) < 1e-6, "l4 screens[0]: middle tends to 35 = 20 + 30/2 (within the widget tol 0.5 at the slider end t = 6)"
# steady state solves u_xx = 0 with the end values: a line
assert sp.diff(20 + 30 * x / sp.pi, x, 2) == 0, "l4 screens[0].explain: u_xx = 0 is a line"

# l4 screens[2]: insulated rod from u0 = x settles at the average 1/2; the cosine series in the canvas is that of x
cos_series = lambda xx, tt, M=200: 0.5 - (4 / math.pi ** 2) * sum(math.cos((2 * mm - 1) * math.pi * xx) * math.exp(-(2 * mm - 1) ** 2 * math.pi ** 2 * tt) / (2 * mm - 1) ** 2 for mm in range(1, M + 1))
assert all(abs(cos_series(xx, 0, 2000) - xx) < 2e-3 for xx in [0.1, 0.5, 0.9]), "l4 screens[2] canvas: cosine series of x"
assert abs(cos_series(0.3, 0.4) - 0.5) < 0.01 and abs(cos_series(0.3, 3) - 0.5) < 1e-9, "l4 screens[2]: settles at 0.5 (widget tol 0.01 at the slider end t = 0.4)"
assert abs(integrate.quad(lambda s: s, 0, 2)[0] / 2 - 1) < 1e-12, "review-1 r-insulated-avg: 1"

# l4 screens[3] derive: energy argument for w = difference; E' = -2D int w_x^2 for a Dirichlet mode
wmode = sp.exp(-sp.pi ** 2 * t) * sp.sin(sp.pi * x)
E = sp.integrate(wmode ** 2, (x, 0, 1))
assert sp.simplify(E - sp.exp(-2 * sp.pi ** 2 * t) / 2) == 0, "l4 quiz q-energy: E = e^{-2 pi^2 t}/2"
assert sp.simplify(sp.diff(E, t) + 2 * sp.integrate(sp.diff(wmode, x) ** 2, (x, 0, 1))) == 0, "l4 screens[3] line e5: E' = -2 D int w_x^2 (D = 1)"
assert abs(0.5 * math.exp(-2 * math.pi ** 2 * 0.1) - 0.069456) < 1e-6, "l4 quiz q-energy: 0.069456"
# integration by parts identity with w = 0 at both ends (line e4)
# for a concrete w with w(0) = w(L) = 0 the boundary term vanishes and int w w_xx = -int w_x^2
L_ = sp.Integer(2)
wf = x * (L_ - x) * (3 + sp.sin(x))
assert wf.subs(x, 0) == 0 and wf.subs(x, L_) == 0
assert sp.simplify(sp.integrate(wf * sp.diff(wf, x, 2), (x, 0, L_)) + sp.integrate(sp.diff(wf, x) ** 2, (x, 0, L_))) == 0, "l4 screens[3] line e4: integration by parts with w = 0 at both ends"
# with insulated ends (w_x = 0 at both ends) the boundary term also vanishes (line d1 why)
wn = sp.cos(sp.pi * x / L_) * (5 + x ** 2 * (L_ - x) ** 2)
assert sp.simplify(sp.diff(wn, x).subs(x, 0)) == 0 and sp.simplify(sp.diff(wn, x).subs(x, L_)) == 0
assert sp.simplify(sp.integrate(wn * sp.diff(wn, x, 2), (x, 0, L_)) + sp.integrate(sp.diff(wn, x) ** 2, (x, 0, L_))) == 0, "l4 screens[3] d1 why: insulated ends still give E' = -2D int w_x^2"

# l4 screens[5], quiz q-put-half, homework h-far-boundary: put at S = 0 is K e^{-r(T-t)}; call boundary
assert abs(100 * math.exp(-0.05) - 95.1229) < 5e-5 and abs(100 * math.exp(-0.025) - 97.531) < 5e-4, "l4 screens[5], quiz q-put-half"
# the canvas put formula tends to K e^{-r tau} as S -> 0
put_bs = lambda S, K, r, sig, T: K * math.exp(-r * T) * Phi(-(math.log(S / K) + (r - sig ** 2 / 2) * T) / (sig * math.sqrt(T))) - S * Phi(-(math.log(S / K) + (r + sig ** 2 / 2) * T) / (sig * math.sqrt(T)))
assert abs(put_bs(1e-6, 100, 0.05, 0.2, 1) - 100 * math.exp(-0.05)) < 1e-6, "l4 screens[5]: V(0,t) = K e^{-r(T-t)}"
assert abs(bs_call(300, 120, 0.04, 0.2, 0.75) - (300 - 120 * math.exp(-0.03))) < 1e-6, "homework-1 h-far-boundary: large-S asymptote S - K e^{-r(T-t)}"
assert abs(300 - 120 * math.exp(-0.03) - 183.5465) < 5e-5, "homework-1 h-far-boundary: 183.5465"

# l4 screens[6] trap: amplification 0.1 e^{100 t}: 2202.65 at t = 0.1, forward 4.54e-6
assert abs(0.1 * math.exp(10) - 2202.65) < 0.01 and abs(0.1 * math.exp(-10) - 4.54e-6) < 1e-8, "l4 screens[6]: 2,202.65 and 4.54e-6"

# l4 screens[7]: rod at 100 with ends at 0: series is the sine series of 100 (Gibbs at t = 0, smooth for t > 0)
sine100 = lambda xx, tt, M: sum(400 / (math.pi * (2 * mm - 1)) * math.exp(-(2 * mm - 1) ** 2 * tt) * math.sin((2 * mm - 1) * xx) for mm in range(1, M + 1))
assert abs(sine100(1.0, 0, 3000) - 100) < 0.1, "l4 screens[7] canvas: series of 100"
# smoothness for t > 0: the k-th coefficient decays like e^{-k^2 t}, so the series converges uniformly with all derivatives
assert 400 / (math.pi * 61) * math.exp(-61 ** 2 * 0.01) < 1e-15, "l4 screens[7].explain: smooth for every t > 0 (terms vanish)"

# l4 screens[8] code: explicit scheme with Dirichlet and Neumann (ghost point) ends; lam > 0.5 refused
l4 = load("l4-boundary-conditions.json")
ns4 = check_code("l4 screens[8] code", l4["screens"][8]["widget"])
# discrete maximum principle holds for lam <= 1/2 and fails above it (homework-1 h-unstable)
def explicit_dir(u, lam, n):
    u = np.array(u, float)
    for _ in range(n):
        u[1:-1] = u[1:-1] + lam * (u[2:] - 2 * u[1:-1] + u[:-2])
    return u
assert np.allclose(explicit_dir([0, 1, 0, 0, 0], 0.6, 1), [0, -0.2, 0.6, 0, 0]), "homework-1 h-unstable: step 1"
assert abs(explicit_dir([0, 1, 0, 0, 0], 0.6, 2)[2] + 0.24) < 1e-12, "homework-1 h-unstable: -0.24"
assert abs(explicit_dir([0, 1, 0, 0, 0], 0.4, 2)[2] - 0.16) < 1e-12, "homework-1 h-unstable byKey.stable: 0.16"
rng = np.random.default_rng(3)
u0r = rng.uniform(0, 1, 60); u0r[0] = u0r[-1] = 0
for lam in [0.1, 0.3, 0.5]:
    uu = explicit_dir(u0r, lam, 300)
    assert uu.min() >= -1e-12 and uu.max() <= u0r.max() + 1e-12, f"l4/hw1: discrete maximum principle at lam = {lam} (sim: l4_dmp)"
uu = explicit_dir(u0r, 0.6, 300)
assert uu.min() < -1 or uu.max() > 1e3, "homework-1 h-unstable.explain: lam = 0.6 breaks the bound and grows (sim: l4_blowup)"
# von Neumann: growth factor 1 - 4 lam sin^2(theta/2) lies in [-1, 1] for all theta iff lam <= 1/2
th = np.linspace(0, math.pi, 10001)
assert (np.abs(1 - 4 * 0.5 * np.sin(th / 2) ** 2) <= 1 + 1e-12).all() and (np.abs(1 - 4 * 0.51 * np.sin(th / 2) ** 2) > 1).any(), "l4 screens[8].explain: limit lam <= 1/2"

# l4 screens[9] generalise: backward problem fails stability (two final profiles 1e-6 apart give starts far apart)
# spectral: u(x,0) coefficient = u(x,1) coefficient * e^{k^2}; perturb mode k = 5 by 1e-6
assert 1e-6 * math.exp(25) > 1e4, "l4 screens[9] option back: backward problem not stable"
# l4 screens[10] transfer: knock-out barriers are Dirichlet zeros (definition); checked against the method of images in L2 script

# review-1 r-sd-time
assert abs(math.sqrt(6) - 2.4495) < 5e-5, "review-1 r-sd-time"
# homework-1 h-profile code
hw1 = load("homework-1.json")
check_code("homework-1 h-profile code", hw1["items"][0]["widget"])
# homework-1 h-drift: v(x,t) = u(x - ct, t) solves v_t + c v_x = D v_xx when u solves the heat equation (sympy)
c_ = sp.symbols("c")
uu_ = sp.Function("u")
vv = uu_(x - c_ * t, t)
heat_sub = {sp.Derivative(uu_(x - c_ * t, t), t): D * sp.diff(uu_(x - c_ * t, t), x, 2)}
expr = sp.diff(vv, t) + c_ * sp.diff(vv, x) - D * sp.diff(vv, x, 2)
# u_t(x - ct, t) appears as the second-slot derivative; replace by D u_xx
xi = sp.symbols("xi")
ufun = uu_(xi, t)
vt = sp.diff(ufun, t).subs(xi, x - c_ * t) - c_ * sp.diff(ufun, xi).subs(xi, x - c_ * t)
vx = sp.diff(ufun, xi).subs(xi, x - c_ * t)
vxx = sp.diff(ufun, xi, 2).subs(xi, x - c_ * t)
assert sp.simplify(vt + c_ * vx - (sp.diff(ufun, t).subs(xi, x - c_ * t))) == 0, "homework-1 h-drift lines s2 to s4: v_t + c v_x = u_t"
# with u_t = D u_xx the right side is D v_xx: line s5 is the heat equation itself, so nothing further to check
assert sp.simplify(vxx - sp.diff(ufun, xi, 2).subs(xi, x - c_ * t)) == 0, "homework-1 h-drift line s3: v_xx = u_xx"
# homework-1 h-wellposed: sign-flipped heat equation grows modes like e^{k^2 pi^2 t}
m5 = sp.exp(sp.pi ** 2 * t) * sp.sin(sp.pi * x)
assert sp.simplify(sp.diff(m5, t) + sp.diff(m5, x, 2)) == 0, "homework-1 h-wellposed option back why: u_t = -u_xx grows modes"
# homework-1 h-colleague model: sigma = 20%: D = 0.02, sd 0.2 after one year, 0.4 after four; dx = sigma sqrt(dt)
assert abs(math.sqrt(2 * 0.02 * 1) - 0.2) < 1e-12 and abs(math.sqrt(2 * 0.02 * 4) - 0.4) < 1e-12, "homework-1 h-colleague model 3"
assert abs((0.2 * math.sqrt(0.01)) ** 2 / (2 * 0.01) - 0.02) < 1e-12, "homework-1 h-colleague model 4: dx = sigma sqrt(dt) gives D = sigma^2/2"
# dx = dt walk: D = dx/2 -> 0 (model 2, quiz q-d-small)
assert all(abs(h * h / (2 * h) - h / 2) < 1e-15 for h in [0.1, 0.01, 0.001]), "homework-1 h-colleague model 2: D = dx/2 -> 0"

print("pdes-L1-concepts: all checks passed")
