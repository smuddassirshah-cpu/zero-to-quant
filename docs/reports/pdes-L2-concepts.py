"""Concept checks for pdes L2 (l5 to l8, review-2, homework-2).

Separation of variables and every Fourier claim are checked symbolically or by quadrature;
Gibbs's constant, the peak heights and locations by a fine grid; the explicit scheme's
stability limit by running it on both sides of lambda = 1/2 and by von Neumann factors; its
order of accuracy by halving the grid; the semi-discrete system by a matrix exponential; the
corridor option by the series, the method of images and a daily-monitored simulation. Each
assert names the ledger row (docs/reports/audit-pdes-1-3-ledger.md). Run from the repo root:
    python3 -I docs/reports/pdes-L2-concepts.py
"""
import json, math, os
import numpy as np
import sympy as sp
from scipy import integrate, special, linalg, optimize, stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.normpath(os.path.join(ROOT, "..", "app", "content", "courses", "pdes"))


def load(name):
    with open(os.path.join(COURSE, name)) as f:
        return json.load(f)


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


x, t = sp.symbols("x t", real=True)
lam, D, L = sp.symbols("lambda D L", positive=True)

# =============================== l5 ===============================
# l5 screens[0]: 3 e^{-t} sin x + e^{-9t} sin 3x solves u_t = u_xx with zero ends; value at (pi/2, 0.5)
u5 = 3 * sp.exp(-t) * sp.sin(x) + sp.exp(-9 * t) * sp.sin(3 * x)
assert sp.simplify(sp.diff(u5, t) - sp.diff(u5, x, 2)) == 0 and u5.subs(x, 0) == 0 and sp.simplify(u5.subs(x, sp.pi)) == 0, "l5 screens[0]: hook solves the rod"
assert abs(3 * math.exp(-0.5) - math.exp(-4.5) - 1.8085) < 5e-5, "l5 screens[0]: 1.8085"
# l5 screens[1] derive: X T separates into T' = -lambda D T and X'' + lambda X = 0; product solves the equation
Xk = sp.sin(sp.sqrt(lam) * x)
Tk = sp.exp(-lam * D * t)
assert sp.simplify(sp.diff(Xk * Tk, t) - D * sp.diff(Xk * Tk, x, 2)) == 0, "l5 screens[1] line a5: the two ODEs give a solution"
assert sp.simplify(sp.diff(Tk, t) + lam * D * Tk) == 0 and sp.simplify(sp.diff(Xk, x, 2) + lam * Xk) == 0, "l5 screens[1] line a5"
assert abs(math.exp(-2) - 0.1353) < 5e-5, "l5 screens[2]: T(1) = e^{-2}"
# l5 screens[3]: X = sin(sqrt(lam) x)/sqrt(lam) has X(0) = 0, X'(0) = 1; X(pi) = 0 in [2, 5.5] only at lam = 4
Xs = sp.sin(sp.sqrt(lam) * x) / sp.sqrt(lam)
assert Xs.subs(x, 0) == 0 and sp.simplify(sp.diff(Xs, x).subs(x, 0)) == 1
roots = [la for la in np.linspace(2, 5.5, 3501) if abs(math.sin(math.sqrt(la) * math.pi)) < 1e-3]
assert roots and all(abs(r - 4) < 0.01 for r in roots), "l5 screens[3]: X(pi) = 0 at lambda = 4 in the range"
assert abs(math.sin(math.sqrt(9) * math.pi)) < 1e-12 and abs(math.sin(math.sqrt(1) * math.pi)) < 1e-12, "l5 screens[3].explain: 1, 9 also"
# l5 screens[4]: lambda = -4: X = c1 e^{2x} + c2 e^{-2x}; X(0) = 0 forces c2 = -c1; X(pi) ~ 535 c1
c1, c2 = sp.symbols("c1 c2")
Xn = c1 * sp.exp(2 * x) + c2 * sp.exp(-2 * x)
sol = sp.solve([Xn.subs(x, 0), Xn.subs(x, sp.pi)], [c1, c2])
assert sol == {c1: 0, c2: 0}, "l5 screens[4]: only the zero solution for lambda = -4"
assert abs((math.exp(2 * math.pi) - math.exp(-2 * math.pi)) - 535) < 1 and abs((math.exp(2 * math.pi) - math.exp(-2 * math.pi)) / 4 - 134) < 0.5, "l5 screens[4]: about 535 c1; canvas about 134"
# lambda = 0: c1 + c2 x with both ends 0 forces 0
assert sp.solve([c1, c1 + c2 * sp.pi], [c1, c2]) == {c1: 0, c2: 0}, "l5 screens[4].explain: lambda = 0 gives nothing"
# homework-2 h-no-lambda: lambda = int X'^2 / int X^2 >= 0 (Rayleigh quotient) for the modes
for kk in [1, 2, 3]:
    Xm = sp.sin(kk * sp.pi * x / L)
    rq = sp.simplify(sp.integrate(sp.diff(Xm, x) ** 2, (x, 0, L)) / sp.integrate(Xm ** 2, (x, 0, L)))
    assert sp.simplify(rq - (kk * sp.pi / L) ** 2) == 0, f"homework-2 h-no-lambda line s4 / l5 screens[5]: lambda_k = (k pi/L)^2 for k = {kk}"
assert abs(math.pi ** 2 - 9.8696) < 5e-5 and abs((2 * math.pi / 3) ** 2 - 4.3865) < 5e-5, "l5 quiz q-lambda2; review-2 r-lambda-len4"
# l5 screens[6] trap: half-life ln2/9; ratio at t = 0.5 of the hook's two parts
assert abs(math.log(2) / 9 - 0.0770) < 5e-5 and abs(math.log(2) / 3 - 0.231) < 5e-4, "l5 screens[6]"
assert abs(math.exp(-4.5) / (3 * math.exp(-0.5)) - 0.006105) < 1e-6, "l5 screens[6].explain: 0.006105"
assert abs(math.exp(-4.5) / math.exp(-0.5) - 0.0183) < 5e-5, "l5 quiz q-ratio"
# l5 screens[7]: insulated ends: cos kx modes, constant mode never decays
u7 = 1 + sp.exp(-4 * t) * sp.cos(2 * x)
assert sp.simplify(sp.diff(u7, t) - sp.diff(u7, x, 2)) == 0 and sp.diff(u7, x).subs(x, 0) == 0 and sp.simplify(sp.diff(u7, x).subs(x, sp.pi)) == 0, "l5 screens[7]: 1 + e^{-4t} cos 2x solves the insulated rod"
assert abs(1 + math.exp(-1) - 1.3679) < 5e-5, "l5 screens[7]: 1.3679"
# l5 screens[8] code
l5 = load("l5-separation-of-variables.json")
check_code("l5 screens[8] code", l5["screens"][8]["widget"])
assert abs(2 * (2 * math.pi / math.pi) ** 2 - 8) < 1e-12, "l5 screens[9]: rate D lambda_2 = 8"
assert abs(math.exp(-1.6) / math.exp(-0.1) - 0.2231) < 5e-5, "l5 screens[10]: e^{-1.5}"
assert abs(0.5 * 1 * 2 - 1) < 1e-12, "l5 quiz q-fade: rate 0.5, time 2"

# =============================== l6 ===============================
b = sp.symbols("b", real=True)
sq = sp.Piecewise((-1, x < 0), (1, True))
E = sp.integrate((sq - b * sp.sin(x)) ** 2, (x, -sp.pi, sp.pi))
assert sp.simplify(sp.expand(E) - (2 * sp.pi - 8 * b + sp.pi * b ** 2)) == 0, "l6 screens[0].explain: E(b) = 2pi - 8b + pi b^2"
bbest = sp.solve(sp.diff(E, b), b)[0]
assert sp.simplify(bbest - 4 / sp.pi) == 0 and abs(float(E.subs(b, bbest)) - 1.1902) < 5e-5 and abs(float(E.subs(b, 1)) - 1.4248) < 5e-5, "l6 screens[0].explain: best b = 4/pi, errors 1.1902 and 1.4248"
assert sp.integrate(sp.sin(3 * x) ** 2, (x, -sp.pi, sp.pi)) == sp.pi and sp.integrate(sp.sin(2 * x) * sp.sin(3 * x), (x, -sp.pi, sp.pi)) == 0, "l6 screens[1]: orthogonality"
kk = sp.symbols("k", integer=True, positive=True)
bk_sq = sp.simplify(sp.integrate(sq * sp.sin(kk * x), (x, -sp.pi, sp.pi)) / sp.pi)
assert sp.simplify(bk_sq - 2 * (1 - (-1) ** kk) / (kk * sp.pi)) == 0, "l6 screens[3]: b_k = 2(1 - (-1)^k)/(k pi)"
assert abs(4 / math.pi * (1 - 1 / 3 + 1 / 5) - 1.1035) < 5e-5 and abs(4 / math.pi * (1 - 1 / 3) - 0.8488) < 5e-5, "l6 screens[4]: partial sums at pi/2"
ak_abs = sp.simplify(sp.integrate(sp.Abs(x) * sp.cos(kk * x), (x, -sp.pi, sp.pi)) / sp.pi)
assert sp.simplify(ak_abs - 2 * ((-1) ** kk - 1) / (sp.pi * kk ** 2)) == 0, "l6 screens[5]: a_k of |x|"
assert abs(-4 / (9 * math.pi) + 0.1415) < 5e-5 and sp.integrate(sp.Abs(x), (x, -sp.pi, sp.pi)) / sp.pi == sp.pi, "l6 screens[5], [6]: a_3, a_0 = pi"
# l6 screens[7]: complex coefficient c_k = (a_k - i b_k)/2 (direct integral for f = x, k = 2)
ck = sp.integrate(x * sp.exp(-2 * sp.I * x), (x, -sp.pi, sp.pi)) / (2 * sp.pi)
assert sp.simplify(ck - sp.I / 2) == 0, "l6 screens[7]: c_2 = i/2 for f = x"
bk_x = sp.simplify(sp.integrate(x * sp.sin(kk * x), (x, -sp.pi, sp.pi)) / sp.pi)
assert sp.simplify(bk_x - 2 * (-1) ** (kk + 1) / kk) == 0, "l6 screens[7].prose, quiz q-x-b3: b_k = 2(-1)^{k+1}/k"
ck_gen = sp.integrate(x * sp.exp(-sp.I * kk * x), (x, -sp.pi, sp.pi)) / (2 * sp.pi)
assert sp.simplify(ck_gen - (0 - sp.I * bk_x) / 2) == 0, "l6 screens[7].prose: c_k = (a_k - i b_k)/2"
l6 = load("l6-fourier-series.json")
check_code("l6 screens[8] code", l6["screens"][8]["widget"])
# l6 screens[9]: odd function has a_k = 0
assert all(sp.integrate(x ** 3 * sp.cos(n * x), (x, -sp.pi, sp.pi)) == 0 for n in range(0, 4)), "l6 screens[9]: x^3 has no cosines"
# l6 screens[10] transfer: discrete orthogonality on twelve months
mm = np.arange(12)
pm = 60 + 15 * np.cos(2 * np.pi * mm / 12) + 4 * np.sin(4 * np.pi * mm / 12)
assert abs(pm.sum() - 720) < 1e-9 and abs((pm * np.cos(2 * np.pi * mm / 12)).sum() - 90) < 1e-9 and abs((pm * np.sin(4 * np.pi * mm / 12)).sum() - 24) < 1e-9, "l6 screens[10]: sums 720, 90, 24"
assert abs((np.cos(2 * np.pi * mm / 12) ** 2).sum() - 6) < 1e-9 and abs((np.sin(4 * np.pi * mm / 12) ** 2).sum() - 6) < 1e-9, "l6 screens[10].explain: each squared sums to 6"
assert abs(pm[1] - 76.45) < 0.005, "l6 screens[10] canvas values"
assert abs(math.pi / 4 - 0.7854) < 5e-5, "l6 quiz q-leibniz"

# =============================== l7 ===============================
def sq_partial(xx, M):
    s = np.zeros_like(xx)
    for j in range(1, M + 1):
        kq = 2 * j - 1
        s += 4 / (math.pi * kq) * np.sin(kq * xx)
    return s
xg = np.linspace(1e-6, math.pi / 2, 400001)
peaks = {M: sq_partial(xg, M).max() for M in [5, 10, 50, 400]}
assert abs(peaks[5] - 1.1823) < 5e-5 and abs(peaks[10] - 1.1798) < 5e-5 and abs(peaks[50] - 1.1790) < 5e-5, "l7 screens[0]: peaks 1.1823, 1.1798, 1.1790"
gibbs = 2 / math.pi * special.sici(math.pi)[0]
assert abs(gibbs - 1.17898) < 5e-6 and abs(peaks[400] - gibbs) < 2e-5, "l7 screens[1]: limit (2/pi) Si(pi) = 1.17898 (sim: l7_gibbs)"
assert abs((gibbs - 1) / 2 - 0.0895) < 5e-5, "l7 screens[1]: 8.95% of the jump"
for M in [5, 10, 50]:
    argmax = xg[sq_partial(xg, M).argmax()]
    assert abs(argmax - math.pi / (2 * M)) < 2e-5, f"l7 screens[0] hints, quiz q-peak-place: first peak at pi/(2M) for M = {M}"
assert peaks[5] > peaks[10] > peaks[50] > gibbs, "l7 screens[0].explain: never falls below about 1.179"
# the overshoot is pointwise convergent but not uniform: at fixed x = 0.1 the sum tends to 1, the sup stays
assert abs(sq_partial(np.array([0.1]), 400)[0] - 1) < 0.01 and peaks[400] > 1.17, "l7 screens[6] trap: pointwise, not uniform (sim: l7_pointwise)"
# l7 screens[2]: slopes -1 and -2 on log axes
ks = np.arange(1, 40, 2)
assert abs(np.polyfit(np.log(ks), np.log(4 / (math.pi * ks)), 1)[0] + 1) < 1e-12 and abs(np.polyfit(np.log(ks), np.log(4 / (math.pi * ks ** 2)), 1)[0] + 2) < 1e-12, "l7 screens[2]"
# l7 screens[3]: |x| error at 0
err_abs = lambda N: math.pi / 2 - 4 / math.pi * sum(1 / (2 * j - 1) ** 2 for j in range(1, N + 1))
assert abs(err_abs(1) - 0.2976) < 5e-5 and abs(err_abs(5) - 0.0635) < 5e-5 and abs(err_abs(50) - 0.0064) < 5e-5, "l7 screens[3]: 0.2976, 0.0635, 0.0064"
# l7 screens[4]: tail bound
assert abs(sum(1 / k ** 2 for k in range(11, 2000000)) - 0.095166) < 2e-6 and sum(1 / k ** 2 for k in range(11, 2000000)) < 0.1, "l7 screens[4].explain: tail 0.095166 < 1/10"
assert sp.integrate(x ** -2, (x, sp.Symbol("N", positive=True), sp.oo)) == 1 / sp.Symbol("N", positive=True), "l7 screens[4]: int_N^inf x^-2 = 1/N"
assert err_abs(50) < 4 / (math.pi * 99), "l7 screens[4].explain: error below 4/(pi K)"
# l7 screens[5]: Parseval for f = x
assert sp.integrate(x ** 2, (x, -sp.pi, sp.pi)) / sp.pi == 2 * sp.pi ** 2 / 3 and sp.summation(4 / kk ** 2, (kk, 1, sp.oo)) == 2 * sp.pi ** 2 / 3, "l7 screens[5]: Parseval gives pi^2/6"
assert abs(math.pi ** 2 / 6 - 1.644934) < 1e-6 and abs(math.pi ** 2 / 8 - 1.2337) < 5e-5, "l7 screens[5], quiz q-odd-sum"
# l7 screens[7]: f = x series at pi gives 0
assert all(abs(math.sin(k * math.pi)) < 1e-12 for k in range(1, 50)), "l7 screens[7]: every sin k pi = 0"
l7 = load("l7-when-fourier-converges.json")
check_code("l7 screens[8] code", l7["screens"][8]["widget"])
assert abs(0.01 * (20 / 200) ** 2 - 1e-4) < 1e-15 and abs(0.01 * (20 / 2000) - 1e-4) < 1e-15, "l7 screens[10]: N = 200 for the call, 2,000 for the digital"
# l7 generalise claim "at a point where f is continuous the series converges to f": the Dirichlet-Jordan theorem needs
# piecewise smoothness (or bounded variation). No finite computation can exhibit du Bois-Reymond's continuous function
# with a divergent series, so this row rests on the source (ledger: l7 screens[9].prose, summary.ideas[0]).

# =============================== l8 ===============================
def rod_series(xx, tt, u0=100, K=2001):
    s = 0.0
    for k in range(1, K + 1, 2):
        s += 4 * u0 / (k * math.pi) * math.exp(-k * k * tt) * math.sin(k * xx)
    return s
t50 = optimize.brentq(lambda tt: rod_series(math.pi / 2, tt) - 50, 0.5, 1.5)
assert abs(t50 - 0.9345) < 5e-5 and abs(math.log(8 / math.pi) - 0.9347) < 5e-5, "l8 screens[0]: 0.9345 exact, 0.9347 one term"
# l8 screens[2]: nonzero ends: b_k formula is the sine series of 80 - 30x/pi
bk_ne = sp.simplify(sp.integrate((80 - 30 * x / sp.pi) * sp.sin(kk * x), (x, 0, sp.pi)) * 2 / sp.pi)
assert sp.simplify(bk_ne - sp.Rational(2) / sp.pi * (80 * (1 - (-1) ** kk) + 30 * (-1) ** kk) / kk) == 0, "l8 screens[2].prose: b_k"
assert abs(30 / math.pi - 9.5493) < 5e-5 and abs(260 / math.pi - 82.7606) < 5e-5, "l8 screens[2]: b_2, b_1"


def rod_ne(xx, tt, K=2001):
    s = 20 + 30 * xx / math.pi
    for k in range(1, K + 1):
        bkv = 2 / math.pi * (80 * (1 - (-1) ** k) + 30 * (-1) ** k) / k
        s += bkv * math.exp(-k * k * tt) * math.sin(k * xx)
    return s
assert abs(rod_ne(math.pi / 2, 1) - 65.4425) < 5e-5, "l8 screens[2].explain: u(pi/2, 1) = 65.4425"


def explicit_rod(u0, N, lam, t_end, left, right):
    dxv = math.pi / N
    n = int(math.ceil(t_end / (lam * dxv * dxv) - 1e-12))
    mu = (t_end / n) / (dxv * dxv)
    u = np.full(N + 1, float(u0)); u[0], u[-1] = left, right
    for _ in range(n):
        u[1:-1] = u[1:-1] + mu * (u[2:] - 2 * u[1:-1] + u[:-2])
    return u
assert abs(explicit_rod(100, 200, 0.4, 1, 20, 50)[100] - 65.4410) < 5e-5, "l8 screens[2].explain: explicit 200 intervals gives 65.4410 (sim: l8_explicit_ne)"
# l8 screens[3]: tridiagonal eigenvalues -(4/dx^2) sin^2(k dx/2)
N = 10
dxv = math.pi / N
A = (np.diag(-2 * np.ones(N - 1)) + np.diag(np.ones(N - 2), 1) + np.diag(np.ones(N - 2), -1)) / dxv ** 2
ev = np.sort(np.linalg.eigvalsh(A))[::-1]
assert np.allclose(ev, [-(4 / dxv ** 2) * math.sin(k * dxv / 2) ** 2 for k in range(1, N)]), "l8 screens[3].prose: eigenvalues of the grid"
assert abs(ev[2] + 8.3532) < 5e-5, "l8 screens[3]: -8.3532 for k = 3"
N = 100
dxv = math.pi / N
A = (np.diag(-2 * np.ones(N - 1)) + np.diag(np.ones(N - 2), 1) + np.diag(np.ones(N - 2), -1)) / dxv ** 2
ev = np.sort(np.linalg.eigvalsh(A))[::-1]
assert abs(ev[0] + 0.999918) < 1e-6 and abs(ev[1] + 3.998684) < 1e-6 and abs(ev[2] + 8.993340) < 1e-6, "l8 screens[3].explain: N = 100 eigenvalues"
uexp = linalg.expm(A * 1.0) @ np.full(N - 1, 100.0)
assert abs(uexp[N // 2 - 1] - 46.834596) < 1e-6, "l8 screens[3].explain: stiff solve gives 46.834596 (semi-discrete exact)"
assert abs(rod_series(math.pi / 2, 1) - 46.834628) < 1e-6, "l8 screens[8] test: series 46.834628"
# l8 screens[4]: Euler on u' = Au multiplies mode k by 1 - 4 lam sin^2(k dx/2); the explicit scheme
N = 10; dxv = math.pi / N
A = (np.diag(-2 * np.ones(N - 1)) + np.diag(np.ones(N - 2), 1) + np.diag(np.ones(N - 2), -1)) / dxv ** 2
for lamv in [0.4, 0.5, 0.6]:
    G = np.eye(N - 1) + lamv * dxv ** 2 * A
    evG = np.sort(np.linalg.eigvalsh(G))
    want = sorted(1 - 4 * lamv * math.sin(k * dxv / 2) ** 2 for k in range(1, N))
    assert np.allclose(evG, want), f"l8 screens[4]: factor 1 - 4 lam sin^2 at lam = {lamv}"
fac = lambda lamv, k=9: 1 - 4 * lamv * math.sin(k * math.pi / 20) ** 2
assert abs(fac(0.6) + 1.3413) < 5e-5 and abs(fac(0.4) + 0.5608) < 5e-5 and abs(fac(0.5) + 0.9511) < 5e-5, "l8 screens[5]: factors -0.5608, -0.9511, -1.3413"
assert abs(1 - 4 * 0.6 * 0.9755 + 1.34) < 0.005, "l8 quiz q-blow"
# the live 9 by 9 scheme: lam = 0.6 for 20 steps and lam = 0.4 for 25 steps
def live(lamv, n):
    M = np.diag((1 - 2 * lamv) * np.ones(9)) + np.diag(lamv * np.ones(8), 1) + np.diag(lamv * np.ones(8), -1)
    return np.linalg.matrix_power(M, n) @ np.full(9, 100.0)
assert abs(live(0.6, 20)[4] - 1160.98) < 0.01, "l8 screens[5].explain: 1,160.98 after 20 steps at lam = 0.6 (sim: l8_live)"
assert abs(live(0.4, 25)[4] - 46.5197) < 5e-5, "l8 screens[5].explain: 46.5197 at lam = 0.4, 25 steps"
t25 = 25 * 0.4 * dxv ** 2
assert abs(rod_series(math.pi / 2, t25) - 47.4487) < 5e-5, "l8 screens[5].explain: series 47.4487 at that time"
assert abs((linalg.expm(A * t25) @ np.full(9, 100.0))[4] - 47.4357) < 5e-5, "l8 screens[5].explain: nine points exactly 47.4357"
# explicit scheme blows up past the limit and stays bounded below it (the empirical stability claim)
assert abs(live(0.6, 60)[4]) > 1e5 and abs(live(0.5, 2000)).max() <= 100 + 1e-9 and abs(live(0.4, 2000)).max() <= 100 + 1e-9, "l8 screens[4]: stable iff lam <= 1/2 on this grid (sim: l8_stability)"
assert abs(math.pi / 10) ** 2 / 2 - 0.0493 < 2e-4 and abs((math.pi / 20) ** 2 / (2 * 0.5) - 0.0247) < 2e-4, "l8 quiz q-dt; review-2 r-stable-step"
# order of accuracy: with lam fixed at 0.4, halving dx should cut the error by about 4 (second order in dx, first in dt)
errs = [abs(explicit_rod(100, N_, 0.4, 1, 0, 0)[N_ // 2] - rod_series(math.pi / 2, 1)) for N_ in [50, 100, 200, 400]]
ratios = [errs[i] / errs[i + 1] for i in range(3)]
assert all(3.5 < r_ < 4.5 for r_ in ratios), f"l8 screens[8].explain: closing on the series as the grid refines, second order: ratios {ratios} (sim: l8_order)"
# l8 screens[6] trap, [7] edge, [9] generalise
assert abs(400 / math.pi * math.exp(-0.1) - 115.2075) < 5e-5 and abs(rod_series(math.pi / 2, 0.1) - 99.9112) < 5e-5 and abs(rod_series(math.pi / 2, 0.1, K=7) - 99.9070) < 5e-5, "l8 screens[6]: 115.2075, 99.9112, 99.9070"
assert rod_series(math.pi / 2, 0.1) <= 100, "l8 screens[6]: maximum principle holds for the full series"
assert abs(100 * gibbs - 117.9) < 0.01, "l8 screens[7]: 117.9"
assert abs(math.exp(-8) / 3 - 0.000112) < 1e-6, "l8 screens[9].explain: k = 3 term is 0.000112 of the first at t = 1"
assert abs(400 / (3 * math.pi) * math.exp(-9) - 0.005238) < 1e-6 and abs(400 / math.pi * math.exp(-1) - 400 / (3 * math.pi) * math.exp(-9) - 46.8346) < 1.1e-4, "l8 quiz q-centre (46.8347 from the rounded terms, 46.8346 exact: within the 0.0006 tolerance)"
l8 = load("l8-heat-on-a-rod.json")
ns8 = check_code("l8 screens[8] code", l8["screens"][8]["widget"])
# l8 screens[10] transfer: corridor option by the series, by the method of images, and by simulation
Lc, Dc, Tc = 0.4, 0.02, 1.0
P_series = sum(4 / (k * math.pi) * math.exp(-Dc * (k * math.pi / Lc) ** 2 * Tc) * math.sin(k * math.pi / 2) for k in range(1, 200, 2))
assert abs(Dc * (math.pi / Lc) ** 2 - 1.2337) < 5e-5 and abs(4 / math.pi * math.exp(-1.2337) - 0.37078) < 2e-5, "l8 screens[10]: first term 0.37078"
assert abs(P_series - 0.370777) < 1e-6 and abs(-(4 / (3 * math.pi)) * math.exp(-Dc * (3 * math.pi / Lc) ** 2) + 6e-6) < 1e-6, "l8 screens[10].explain: P = 0.370777, k = 3 term about -6e-6"
# method of images: P(stay in (-a, a)) for BM with variance 2Dt from 0
a = Lc / 2
sd = math.sqrt(2 * Dc * Tc)
P_images = sum((-1) ** n * (stats.norm.cdf((a - 2 * n * a) / sd) - stats.norm.cdf((-a - 2 * n * a) / sd)) for n in range(-30, 31))
assert abs(P_images - P_series) < 1e-9, "l8 screens[10].explain: method of images gives the same (derivation)"
# the series is the survival probability of a delta start at the middle (sine series of delta: (2/L) sin(k pi/2))
rng = np.random.default_rng(5)
paths = 20000
inc = rng.standard_normal((paths, 252)) * 0.2 / math.sqrt(252)
logp = inc.cumsum(axis=1)
survive = (np.abs(logp).max(axis=1) < 0.2).mean()
assert abs(survive - 0.40) < 0.012 and survive > P_series, "l8 screens[10].explain: daily monitoring survives with frequency about 0.40 (sim: l8_daily)"
# a log price that is driftless under the pricing measure is not the zero-rate risk-neutral one (drift -sigma^2/2):
# the drifted survival probability differs from 0.3708 (ledger: l8 screens[10].prose, homework-2 h-corridor-wide)
mu_q = -0.5 * 0.2 ** 2
inc_q = inc + mu_q / 252
survive_q_mc = (np.abs(inc_q.cumsum(axis=1)).max(axis=1) < 0.2).mean()
# continuous-time value by the drifted series: u = e^{(mu x)/(2D) - mu^2 t/(4D)} w, w heat with absorbing ends
P_drift = sum(math.exp(-mu_q ** 2 * Tc / (4 * Dc)) * (2 / Lc) * math.exp(-Dc * (k * math.pi / Lc) ** 2 * Tc) * math.sin(k * math.pi / 2)
              * integrate.quad(lambda y: math.exp(mu_q * (y - Lc / 2) / (2 * Dc)) * math.sin(k * math.pi * y / Lc), 0, Lc)[0] for k in range(1, 60))
assert 0.001 < P_series - P_drift < 0.003 and abs(P_drift - 0.3693) < 5e-4, f"ledger l8 screens[10]: risk-neutral drift -sigma^2/2 lowers the continuous value to {P_drift:.4f}, outside the item's 0.02 pound tolerance on 37.08 (sim: l8_drift)"
mu_w, Dw_, Lw_ = -0.5 * 0.25 ** 2, 0.25 ** 2 / 2, 0.6
P_drift_w = sum(math.exp(-mu_w ** 2 / (4 * Dw_)) * (2 / Lw_) * math.exp(-Dw_ * (k * math.pi / Lw_) ** 2) * math.sin(k * math.pi / 2)
                * integrate.quad(lambda y: math.exp(mu_w * (y - Lw_ / 2) / (2 * Dw_)) * math.sin(k * math.pi * y / Lw_), 0, Lw_)[0] for k in range(1, 60))
assert 0.001 < 0.54036 - P_drift_w < 0.004, f"ledger homework-2 h-corridor-wide: risk-neutral drift gives {P_drift_w:.4f} against 0.5404 (sim: hw2_drift)"
assert survive_q_mc < survive, "sim: l8_drift (daily)"
# review-2
assert abs(math.exp(-0.5 * (36 - 9) * 0.3) - 0.0174) < 5e-5 and abs(3 / math.pi - 0.9549) < 5e-5 and abs(math.pi ** 2 / 3 - 3.2899) < 5e-5, "review-2 r-decay-ratio, r-b4, r-mean-x2"
# review-2 r-parseval: |x| energy split
assert sp.integrate(sp.Abs(x) ** 2, (x, -sp.pi, sp.pi)) / sp.pi == 2 * sp.pi ** 2 / 3, "review-2 r-parseval: left side 2 pi^2/3"
S4odd = sum(1 / k ** 4 for k in range(1, 400000, 2))
assert abs(16 / math.pi ** 2 * S4odd + math.pi ** 2 / 2 - 2 * math.pi ** 2 / 3) < 1e-9 and abs(S4odd - math.pi ** 4 / 96) < 1e-9 and abs(math.pi ** 4 / 96 - 1.0147) < 5e-5, "review-2 r-parseval: pi^4/96"
assert abs(rod_series(math.pi / 2, 0.3) - 91.4857) < 5e-5 and abs(400 / math.pi * math.exp(-0.3) - 94.3239) < 5e-5 and abs(0.4 * 91.4857 - 36.5943) < 5e-5, "review-2 r-linearity"
# homework-2
hw2 = load("homework-2.json")
check_code("homework-2 h-heat-rod code", hw2["items"][0]["widget"])
# h-heat-rod test values are the closed forms: PARAB sine coefficients 32/(k^3 pi^3) for odd k
bk_par = sp.simplify(sp.integrate(x * (2 - x) * sp.sin(kk * sp.pi * x / 2), (x, 0, 2)))
assert abs(float(bk_par.subs(kk, 1)) - 1.03205) < 1e-5 and abs(float(bk_par.subs(kk, 3)) - 0.038224) < 1e-6 and float(bk_par.subs(kk, 2)) == 0, "homework-2 h-heat-rod test: parabola coefficients"
assert abs(rod_series(math.pi / 3, 0.2) - 90.13026) < 1e-5 and abs(rod_series(math.pi / 4, 0.3) - 68.70398) < 1e-5, "homework-2 h-heat-rod tests: 90.13026, 68.70398"
# h-centre-nonzero: ends 10 and 70
bk_h = lambda k: 2 / math.pi * (90 * (1 - (-1) ** k) + 60 * (-1) ** k) / k
assert abs(bk_h(1) - 76.3944) < 5e-5 and abs(bk_h(3) - 25.4648) < 5e-5, "homework-2 h-centre-nonzero: b_1, b_3"
assert abs(40 + bk_h(1) * math.exp(-1) - bk_h(3) * math.exp(-9) - 68.1008) < 5e-5, "homework-2 h-centre-nonzero: 68.1008"


def rod_ne2(xx, tt, K=2001):
    s = 10 + 60 * xx / math.pi
    for k in range(1, K + 1):
        s += bk_h(k) * math.exp(-k * k * tt) * math.sin(k * xx)
    return s
assert abs(rod_ne2(math.pi / 2, 1) - 68.1008) < 5e-5, "homework-2 h-centre-nonzero: full series agrees to four places"
assert abs(explicit_rod(100, 200, 0.4, 1, 10, 70)[100] - 68.0994) < 5e-5, "homework-2 h-centre-nonzero.explain: explicit 68.0994 (sim: hw2_explicit)"
assert abs(3 * gibbs - 3.537) < 5e-4, "homework-2 h-gibbs-true: 3.537"
# h-parseval-x2: a_k = 4(-1)^k/k^2 and the energy 2 pi^4/5
ak_x2 = sp.simplify(sp.integrate(x ** 2 * sp.cos(kk * x), (x, -sp.pi, sp.pi)) / sp.pi)
assert sp.simplify(ak_x2 - 4 * (-1) ** kk / kk ** 2) == 0 and sp.integrate(x ** 4, (x, -sp.pi, sp.pi)) / sp.pi == 2 * sp.pi ** 4 / 5, "homework-2 h-parseval-x2: a_k and the energy"
assert abs(math.pi ** 4 / 90 - 1.0823) < 5e-5 and abs(16 * math.pi ** 4 / 90 - (2 * math.pi ** 4 / 5 - 2 * math.pi ** 4 / 9)) < 1e-9, "homework-2 h-parseval-x2: pi^4/90"
assert math.ceil(1 / (0.4 * (math.pi / 100) ** 2) - 1e-12) == 2534 and abs(1 / (0.4 * (math.pi / 100) ** 2) - 2533.03) < 0.01, "homework-2 h-step-count"
assert abs((1 / 2534) / (math.pi / 100) ** 2 - 0.39985) < 5e-6, "homework-2 h-step-count.explain: lambda 0.39985"
# h-corridor-wide
Dw, Lw = 0.25 ** 2 / 2, 0.6
assert abs(Dw - 0.03125) < 1e-12 and abs(Dw * (math.pi / Lw) ** 2 - 0.8567) < 5e-5, "homework-2 h-corridor-wide: D, rate"
Pw = 4 / math.pi * math.exp(-Dw * (math.pi / Lw) ** 2) - 4 / (3 * math.pi) * math.exp(-Dw * (3 * math.pi / Lw) ** 2)
assert abs(4 / math.pi * math.exp(-Dw * (math.pi / Lw) ** 2) - 0.54055) < 1e-5 and abs(Pw - 0.54036) < 1e-5, "homework-2 h-corridor-wide: 0.54055, 0.54036"
assert abs(100 * math.exp(-0.8567) - 42.45) < 0.01 and abs(100 * (4 / math.pi) * math.exp(-0.0625 * (math.pi / Lw) ** 2) - 22.95) < 0.02, "homework-2 h-corridor-wide byKey"
# h-colleague-terms model: start 80
f80 = lambda tt, K: rod_series(math.pi / 2, tt, u0=80, K=K)
assert abs(320 / math.pi * math.exp(-0.1) - 92.17) < 0.005 and abs(-320 / (3 * math.pi) * math.exp(-0.9) + 13.80) < 0.005, "homework-2 h-colleague-terms model 1, 2"
assert abs(f80(0.1, 3) - 78.36) < 0.005 and abs(320 / (5 * math.pi) * math.exp(-2.5) - 1.67) < 0.005 and abs(-320 / (3 * math.pi) * math.exp(-9) + 0.0042) < 5e-5, "model 2"
assert abs(f80(0.1, 2001) - 79.9289) < 5e-5 and abs(f80(0.1, 7) - 79.9256) < 5e-5 and abs(f80(1, 2001) - 37.4677) < 5e-5 and abs(f80(1, 1) - 37.4719) < 5e-5, "model 3"
assert abs(320 / (11 * math.pi) * math.exp(-121 * 0.1) - 5.1e-5) < 2e-6 and 320 / (9 * math.pi) * math.exp(-81 * 0.1) > 1e-3, "model 4: k = 11 is the first term below 1e-3 at t = 0.1"
assert f80(0.1, 2001) <= 80 and f80(0.1, 1) > 80, "model 1: the maximum principle bounds the true solution by 80; one term breaks it"

print("pdes-L2-concepts: all checks passed")
