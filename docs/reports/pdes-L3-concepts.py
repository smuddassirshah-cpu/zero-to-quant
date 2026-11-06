"""Concept checks for pdes L3 (l9 to l12, review-3, homework-3).

The Black-Scholes to heat-equation change of variables is verified symbolically, including the
sign of the time variable; the Gaussian lemma and the formula it yields by quadrature and
algebra; Feynman-Kac by substitution and by the lesson's own seeded simulations; the explicit
scheme's blow-up past lambda = 1/2 and the Crank-Nicolson order, Richardson, Rannacher and
boundary claims by running the lesson's pricer and an independent S-grid solver. Each assert
names the ledger row (docs/reports/audit-pdes-1-3-ledger.md). Run from the repo root:
    python3 -I docs/reports/pdes-L3-concepts.py
"""
import json, math, os
import numpy as np
import sympy as sp
from scipy import integrate, stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.normpath(os.path.join(ROOT, "..", "app", "content", "courses", "pdes"))
Phi = stats.norm.cdf
phi = stats.norm.pdf


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


def bs_call(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)


def bs_put(S, K, r, sig, T):
    return bs_call(S, K, r, sig, T) - S + K * math.exp(-r * T)


C0 = bs_call(100, 100, 0.05, 0.2, 1)
assert abs(C0 - 10.4505836) < 5e-8, "l9/l10/l12: the formula gives 10.4505836"

# =============================== l9: the change of variables, symbolically ===============================
S, t, K, r, sig, T = sp.symbols("S t K r sigma T", positive=True)
x, tau = sp.symbols("x tau", real=True)
kk = 2 * r / sig ** 2
alpha = -(kk - 1) / 2
beta = -(kk + 1) ** 2 / 4
xS = sp.log(S / K)
tauT = sig ** 2 * (T - t) / 2
# evaluate the operator on a concrete u that solves the heat equation and on one that does not
heat_sol = sp.exp(-tau) * sp.sin(x) + sp.exp(-4 * tau) * sp.cos(2 * x) + x ** 2 + 2 * tau
assert sp.simplify(sp.diff(heat_sol, tau) - sp.diff(heat_sol, x, 2)) == 0
Vc = (K * sp.exp(alpha * x + beta * tau) * heat_sol).subs({x: xS, tau: tauT})
BSc = sp.diff(Vc, t) + sig ** 2 * S ** 2 / 2 * sp.diff(Vc, S, 2) + r * S * sp.diff(Vc, S) - r * Vc
assert sp.simplify(BSc) == 0, "l9 summary.formula: V = K e^{alpha x + beta tau} u with u_tau = u_xx solves Black-Scholes (exact, every r, sigma)"
# the sign of time: tau = sigma^2 t / 2 instead makes the same u fail (backward heat)
Vw = (K * sp.exp(alpha * x + beta * tau) * heat_sol).subs({x: xS, tau: sig ** 2 * t / 2})
BSw = sp.diff(Vw, t) + sig ** 2 * S ** 2 / 2 * sp.diff(Vw, S, 2) + r * S * sp.diff(Vw, S) - r * Vw
assert sp.simplify(BSw) != 0, "l9 screens[1] byKey.forward, quiz q-backward: tau = sigma^2 t/2 runs the heat equation backwards"
anti = sp.exp(tau) * sp.sin(x)  # solves u_tau = -u_xx
Vb = (K * sp.exp(alpha * x - beta * tau) * anti).subs({x: xS, tau: sig ** 2 * t / 2})  # the time sign flips beta too
BSb = sp.diff(Vb, t) + sig ** 2 * S ** 2 / 2 * sp.diff(Vb, S, 2) + r * S * sp.diff(Vb, S) - r * Vb
assert sp.simplify(BSb) == 0, "l9 quiz q-backward: with tau = sigma^2 t/2 the transformed equation is u_tau = -u_xx"
# the intermediate equation v_tau = v_xx + (k - 1) v_x - k v  (l9 screens[3], [4])
vfun = sp.exp(alpha * x + beta * tau) * heat_sol
assert sp.simplify(sp.diff(vfun, tau) - (sp.diff(vfun, x, 2) + (kk - 1) * sp.diff(vfun, x) - kk * vfun)) == 0, "l9 screens[4].explain: v_tau = v_xx + (k-1) v_x - k v"
# chain rule: S V_S = K v_x and S^2 V_SS = K (v_xx - v_x), with a concrete v
vc = sp.exp(2 * x) * sp.sin(3 * x) + x ** 3
VKc = K * vc.subs(x, xS)
assert sp.simplify(S * sp.diff(VKc, S) - K * sp.diff(vc, x).subs(x, xS)) == 0, "l9 screens[2] line c2: S V_S = K v_x"
assert sp.simplify(S ** 2 * sp.diff(VKc, S, 2) - K * (sp.diff(vc, x, 2) - sp.diff(vc, x)).subs(x, xS)) == 0, "l9 screens[2] line c4: S^2 V_SS = K(v_xx - v_x)"
# alpha and beta from the u_x and u terms (l9 screens[5], [6])
a_, b_, k_ = sp.symbols("a b k")
assert sp.solve(2 * a_ + (k_ - 1), a_)[0] == -(k_ - 1) / 2, "l9 screens[5]: alpha"
assert sp.simplify((a_ ** 2 + (k_ - 1) * a_ - k_).subs(a_, -(k_ - 1) / 2) + (k_ + 1) ** 2 / 4) == 0, "l9 screens[6]: beta = -(k+1)^2/4"
assert (2.5, -0.75, -3.0625) == (2 * 0.05 / 0.04, -(2.5 - 1) / 2, -(3.5) ** 2 / 4), "l9: k, alpha, beta for our option"
assert abs(2 * 0.03 / 0.0625 - 0.96) < 1e-12 and abs(-(1.96) ** 2 / 4 + 0.9604) < 1e-12, "l9 quiz q-coeff, q-beta"
assert abs(0.5 * 0.09 * 2 - 0.09) < 1e-12 and abs(0.5 * 0.04 * 1 - 0.02) < 1e-12, "l9 quiz q-tau, screens[1].explain"
# start value u(x, 0) = e^{-alpha x} max(e^x - 1, 0) = max(e^{1.75x} - e^{0.75x}, 0)
xx = np.linspace(-0.6, 0.6, 7)
assert np.allclose(np.exp(0.75 * xx) * np.maximum(np.exp(xx) - 1, 0), np.maximum(np.exp(1.75 * xx) - np.exp(0.75 * xx), 0)), "l9 screens[7].prose: the start"
# price from u(0, 0.02) = 0.111107
assert abs(100 * math.exp(-3.0625 * 0.02) * 0.111107 - 10.4506) < 5e-5 and abs(math.exp(-0.06125) - 0.940588) < 1e-6, "l9 screens[7]: 10.4506"
# r = 0 edge case: price depends on sigma^2 T only; 100(2 Phi(0.1) - 1) = 7.9656
assert abs(100 * (2 * Phi(0.1) - 1) - 7.9656) < 5e-5 and abs(bs_call(100, 100, 0, 0.2, 1) - bs_call(100, 100, 0, 0.4, 0.25)) < 1e-12 and abs(bs_call(100, 100, 0, 0.1, 4) - 7.9656) < 5e-5, "l9 screens[8], [10]: same sigma^2 T, same price"
assert bs_call(100, 100, 0, 0.4, 0.5) > 7.97 and bs_call(100, 100, 0, 0.2, 0.5) < 7.96, "l9 screens[10] options c, d"
l9 = load("l9-black-scholes-to-heat.json")
check_code("l9 screens[9] code", l9["screens"][9]["widget"])
# homework-3 h-chain explain numbers and h-r0-sigma
assert abs(2 * 0.02 / 0.0625 - 0.64) < 1e-12 and abs(-(0.64 - 1) / 2 - 0.18) < 1e-12 and abs(-(1.64) ** 2 / 4 + 0.6724) < 1e-12, "homework-3 h-chain.explain"
assert abs(bs_call(100, 100, 0, 0.16, 1) - 6.3763) < 5e-5 and abs(math.sqrt(0.0256 / 2.25) - 0.1067) < 5e-5, "homework-3 h-r0-sigma"
# review-3 r-k, r-beta, r-sd
assert abs(0.08 / 0.09 - 0.8889) < 5e-5 and abs(-(1.8889) ** 2 / 4 + 0.8920) < 5e-5 and abs(math.sqrt(2 * 0.0225) - 0.2121) < 5e-5, "review-3 r-k, r-beta, r-sd"

# =============================== l10: the Gaussian lemma and the formula ===============================
def I_lemma(a, x0, tau0):
    f = lambda y: math.exp(a * y) * math.exp(-(x0 - y) ** 2 / (4 * tau0)) / math.sqrt(4 * math.pi * tau0)
    return integrate.quad(f, 0, x0 + 20 * math.sqrt(2 * tau0) + 5)[0]
for a, x0, tau0 in [(1.75, 0, 0.02), (0.75, 0, 0.02), (1.75, 0.1, 0.02), (0.3, -0.2, 0.05), (2.2, 0.4, 0.01)]:
    assert abs(I_lemma(a, x0, tau0) - math.exp(a * x0 + a * a * tau0) * Phi((x0 + 2 * a * tau0) / math.sqrt(2 * tau0))) < 1e-9, f"l10 screens[1] line l4: lemma at a={a}, x={x0}, tau={tau0}"
# completing the square (line l2), symbolically
a_s, y_s = sp.symbols("a y", real=True)
assert sp.simplify(a_s * y_s - (y_s - x) ** 2 / (4 * tau) - (-(y_s - x - 2 * a_s * tau) ** 2 / (4 * tau) + a_s * x + a_s ** 2 * tau)) == 0, "l10 screens[1] line l2: completing the square"
assert abs(2 * 1.75 * 0.02 / 0.2 - 0.35) < 1e-12 and abs(math.exp(1.75 ** 2 * 0.02) - 1.0632) < 5e-5 and abs(math.exp(0.75 ** 2 * 0.02) - 1.0113) < 5e-5, "l10 screens[2]: arguments and factors"
I1, I2 = math.exp(1.75 ** 2 * 0.02) * Phi(0.35), math.exp(0.75 ** 2 * 0.02) * Phi(0.15)
assert abs(I1 - 0.67706) < 1e-5 and abs(I2 - 0.56595) < 1e-5 and abs(I1 - I2 - 0.11111) < 1e-5, "l10 screens[2].explain: 0.67706 - 0.56595 = 0.11111"
# undoing the variables gives Black-Scholes exactly (l10 screens[3]): algebra of the exponents
a1, a2 = (kk + 1) / 2, (kk - 1) / 2
assert sp.simplify(alpha + a1 - 1) == 0 and sp.simplify(beta + a1 ** 2) == 0 and sp.simplify(alpha + a2) == 0 and sp.simplify(beta + a2 ** 2 + kk) == 0, "l10 screens[3] line t1: the four exponent identities"
assert sp.simplify(kk * tauT.subs(t, 0) - r * T) == 0, "l10 screens[3] line t4: k tau = rT"
d_arg = (xS + 2 * a1 * tauT) / sp.sqrt(2 * tauT)
assert sp.simplify(d_arg.subs(t, 0) - (sp.log(S / K) + (r + sig ** 2 / 2) * T) / (sig * sp.sqrt(T))) == 0, "l10 screens[3] line t5: the argument is d_1"
d_arg2 = (xS + 2 * a2 * tauT) / sp.sqrt(2 * tauT)
assert sp.simplify(d_arg2.subs(t, 0) - (sp.log(S / K) + (r - sig ** 2 / 2) * T) / (sig * sp.sqrt(T))) == 0, "l10 screens[3] line t5: d_2"
# the kernel price at several (S, K, r, sigma, T) agrees with the formula: the whole route numerically
def call_kernel(S0, K0, r0, s0, T0):
    k0 = 2 * r0 / s0 ** 2
    al, be = -(k0 - 1) / 2, -(k0 + 1) ** 2 / 4
    x0 = math.log(S0 / K0); tau0 = 0.5 * s0 ** 2 * T0
    u0 = I_lemma((k0 + 1) / 2, x0, tau0) - I_lemma((k0 - 1) / 2, x0, tau0)
    return K0 * math.exp(al * x0 + be * tau0) * u0
for args in [(100, 100, 0.05, 0.2, 1), (110, 100, 0.05, 0.2, 1), (100, 120, 0.03, 0.25, 0.5), (90, 100, 0.01, 0.4, 2)]:
    assert abs(call_kernel(*args) - bs_call(*args)) < 1e-8, f"l10 screens[3]: kernel route equals the formula at {args}"
assert abs(bs_call(110, 100, 0.05, 0.2, 1) - 17.6630) < 5e-5 and abs(110 * 0.7958 - 95.1229 * 0.7345 - 17.67) < 0.005, "l10 screens[4]: 17.6630, 17.67 from rounded values"
# trap: a kernel of variance tau (not 2 tau) prices at 6.6810
def call_kernel_var(S0, K0, r0, s0, T0, c):
    k0 = 2 * r0 / s0 ** 2
    al, be = -(k0 - 1) / 2, -(k0 + 1) ** 2 / 4
    x0 = math.log(S0 / K0); tau0 = 0.5 * s0 ** 2 * T0
    f = lambda y: (math.exp((k0 + 1) / 2 * y) - math.exp((k0 - 1) / 2 * y)) * stats.norm.pdf(y, x0, math.sqrt(c * tau0))
    return K0 * math.exp(al * x0 + be * tau0) * integrate.quad(f, 0, 5)[0]
assert abs(call_kernel_var(100, 100, 0.05, 0.2, 1, 1) - 6.6810) < 5e-5 and abs(call_kernel_var(100, 100, 0.05, 0.2, 1, 2) - C0) < 1e-8, "l10 screens[5] trap: variance tau gives 6.6810, variance 2 tau the formula"
assert abs((C0 - 6.6810) / C0 - 0.36) < 0.005, "l10 screens[5] byKey: 36% low"
# edge: tau -> 0 returns the start value at x0 = 0.2
u_edge = lambda tau0: integrate.quad(lambda y: (math.exp(1.75 * y) - math.exp(0.75 * y)) * stats.norm.pdf(y, 0.2, math.sqrt(2 * tau0)), 0, 5)[0]
assert abs(u_edge(0.02) - 0.3471) < 5e-5 and abs(u_edge(0.0005) - 0.2591) < 5e-5 and abs(math.exp(0.35) - math.exp(0.15) - 0.2572) < 5e-5, "l10 screens[6]: 0.3471, 0.2591, limit 0.2572"
assert abs(100 * (math.exp(0.2) - 1) - 22.14) < 0.005, "l10 screens[6].explain: payoff 22.14"
# put: lemma over y < 0 and parity
def put_kernel(S0, K0, r0, s0, T0):
    k0 = 2 * r0 / s0 ** 2
    al, be = -(k0 - 1) / 2, -(k0 + 1) ** 2 / 4
    x0 = math.log(S0 / K0); tau0 = 0.5 * s0 ** 2 * T0
    f = lambda y: (math.exp((k0 - 1) / 2 * y) - math.exp((k0 + 1) / 2 * y)) * math.exp(-(x0 - y) ** 2 / (4 * tau0)) / math.sqrt(4 * math.pi * tau0)
    return K0 * math.exp(al * x0 + be * tau0) * integrate.quad(f, -8, 0)[0]
assert abs(put_kernel(100, 100, 0.05, 0.2, 1) - 5.5735) < 5e-5 and abs(C0 - 100 + 100 * math.exp(-0.05) - 5.5735) < 5e-5, "l10 screens[7]: put 5.5735 by the kernel and by parity"
Pform = lambda S0, K0, r0, s0, T0: K0 * math.exp(-r0 * T0) * Phi(-(math.log(S0 / K0) + (r0 - s0 ** 2 / 2) * T0) / (s0 * math.sqrt(T0))) - S0 * Phi(-(math.log(S0 / K0) + (r0 + s0 ** 2 / 2) * T0) / (s0 * math.sqrt(T0)))
assert abs(Pform(100, 100, 0.05, 0.2, 1) - put_kernel(100, 100, 0.05, 0.2, 1)) < 1e-8, "l10 screens[7].prose: K e^{-rT} Phi(-d2) - S Phi(-d1)"
assert abs(17.6630 - 110 + 95.1229 - 2.7859) < 5e-5 and abs(Pform(110, 100, 0.05, 0.2, 1) - 2.7859) < 5e-5, "l10 quiz q-put"
l10 = load("l10-formula-from-the-kernel.json")
check_code("l10 screens[8] code", l10["screens"][8]["widget"])
assert abs(bs_call(100, 120, 0.03, 0.25, 0.5) - 1.766906460) < 1e-9, "l10 screens[8] test"
# transfer: digital price e^{-rT} Phi(d2); Phi(d1) is the delta
d1_0 = (0.07) / 0.2
assert abs(Phi(d1_0) - 0.6368) < 5e-5 and abs(Phi(d1_0 - 0.2) - 0.5596) < 5e-5 and abs(5000 * math.exp(-0.05) * Phi(0.15) - 2661.6) < 0.1, "l10 screens[9]: 2,661.62"
delta_fd = (bs_call(100.001, 100, 0.05, 0.2, 1) - bs_call(99.999, 100, 0.05, 0.2, 1)) / 0.002
assert abs(delta_fd - Phi(d1_0)) < 1e-6, "l10 screens[9].prose: Phi(d1) is the hedge (delta)"
# Phi(d2) = risk-neutral P(S_T > K): Monte Carlo
rng = np.random.default_rng(0)
ST = 100 * np.exp(0.03 + 0.2 * rng.standard_normal(2000000))
assert abs((ST > 100).mean() - Phi(0.15)) < 2e-3, "l10 quiz q-d2: Phi(d2) is the risk-neutral exercise chance (sim: l10_d2)"
assert abs(math.sqrt(2 * 0.08) - 0.4) < 1e-12 and abs((0.1 + 0.07) / 0.2 - 0.85) < 1e-12, "l10 quiz q-width, q-arg"

# =============================== l11: Feynman-Kac ===============================
# u = E f(x + W_t) solves u_t = u_xx / 2 for f = x^2 and x^3 (symbolic), E W^2 = t, E W^3 = 0
u2, u3 = x ** 2 + tau, x ** 3 + 3 * x * tau
assert sp.simplify(sp.diff(u2, tau) - sp.diff(u2, x, 2) / 2) == 0 and sp.simplify(sp.diff(u3, tau) - sp.diff(u3, x, 2) / 2) == 0, "l11 screens[1], quiz q-cube"
W = sp.symbols("W", real=True)
tt = sp.symbols("t", positive=True)
Ew = lambda expr: sp.integrate(expr * sp.exp(-W ** 2 / (2 * tt)) / sp.sqrt(2 * sp.pi * tt), (W, -sp.oo, sp.oo))
assert sp.simplify(Ew((x + W) ** 2) - (x ** 2 + tt)) == 0 and sp.simplify(Ew((x + W) ** 3) - (x ** 3 + 3 * x * tt)) == 0, "l11 screens[1], q-cube: the expectations"
# Feynman-Kac derivation (screens[2]): drift of M = e^{-rs} V(s, X_s) by Ito
s_, Xv, mu_, sg_, r_ = sp.symbols("s X mu sigma r", real=True)
Vf = sp.Function("V")(s_, Xv)
dM_drift = sp.diff(sp.exp(-r_ * s_) * Vf, s_) + mu_ * sp.diff(sp.exp(-r_ * s_) * Vf, Xv) + sg_ ** 2 / 2 * sp.diff(sp.exp(-r_ * s_) * Vf, Xv, 2)
assert sp.simplify(dM_drift - sp.exp(-r_ * s_) * (sp.diff(Vf, s_) + mu_ * sp.diff(Vf, Xv) + sg_ ** 2 / 2 * sp.diff(Vf, Xv, 2) - r_ * Vf)) == 0, "l11 screens[2] line f2: Ito drift of e^{-rs} V"
# the Black-Scholes price is the discounted expectation under drift r (the statement of Feynman-Kac for the call)
rng = np.random.default_rng(123)
z = rng.standard_normal(4000000)
STq = 100 * np.exp((0.05 - 0.02) + 0.2 * z)
mc = math.exp(-0.05) * np.maximum(STq - 100, 0)
assert abs(mc.mean() - C0) < 3 * mc.std() / math.sqrt(len(z)), "l11 screens[3].explain: V = e^{-rT} E[(S_T - K)^+] under drift r (sim: l11_fk)"
# the Black-Scholes formula satisfies the PDE (the 'solves' direction), checked by finite differences at several points
def bs_pde_resid(S0, t0):
    h, dtt = 1e-3, 1e-5
    Vt = (bs_call(S0, 100, 0.05, 0.2, 1 - (t0 + dtt)) - bs_call(S0, 100, 0.05, 0.2, 1 - (t0 - dtt))) / (2 * dtt)
    VS = (bs_call(S0 + h, 100, 0.05, 0.2, 1 - t0) - bs_call(S0 - h, 100, 0.05, 0.2, 1 - t0)) / (2 * h)
    VSS = (bs_call(S0 + h, 100, 0.05, 0.2, 1 - t0) - 2 * bs_call(S0, 100, 0.05, 0.2, 1 - t0) + bs_call(S0 - h, 100, 0.05, 0.2, 1 - t0)) / h ** 2
    return Vt + 0.5 * 0.04 * S0 ** 2 * VSS + 0.05 * S0 * VS - 0.05 * bs_call(S0, 100, 0.05, 0.2, 1 - t0)
assert all(abs(bs_pde_resid(S0, t0)) < 1e-4 for S0, t0 in [(90, 0.2), (100, 0.5), (115, 0.7)]), "l11 screens[3]: the expectation solves the Black-Scholes equation"
# seeded numbers from the lesson's own code
l11 = load("l11-feynman-kac.json")
ns11 = check_code("l11 screens[9] code", l11["screens"][9]["widget"])
mcp = ns11["mc_price"](ns11["CALL"], 100, 0.05, 0.2, 1, 100000, 11)
assert abs(mcp[0] - 10.4534) < 5e-5 and abs(mcp[1] - 0.0465) < 5e-5, "l11 screens[4]: 10.4534, standard error 0.0465"
assert abs(0.0465 * math.sqrt(50) - 0.33) < 0.005 and abs((10.4534 - C0) / 0.0465 - 0.06) < 0.005, "l11 screens[4]: 0.33; within 0.06 standard errors"
hm = ns11["heat_mc"](lambda y: y ** 2, 1, 0.5, 100000, 5)
assert abs(hm[0] - 1.5001) < 5e-5 and abs(hm[1] - 0.0050) < 5e-5, "l11 screens[1].explain: 1.5001, se 0.0050"
hm3 = ns11["heat_mc"](lambda y: y ** 3, 1, 0.5, 100000, 5)
assert abs(hm3[0] - 2.5016) < 5e-5 and abs(hm3[1] - 0.0124) < 5e-5, "l11 quiz q-cube.explain"
# real drift 12% with discount 5%: exact 15.5261; same seeded draws 15.5343
mu_real = 0.12
exact_real = lambda m: math.exp(-0.05) * (100 * math.exp(m) * Phi((m + 0.02) / 0.2) - 100 * Phi((m - 0.02) / 0.2))
assert abs(exact_real(0.12) - 15.5261) < 5e-5 and abs(exact_real(0.12) / C0 - 1.49) < 0.005, "l11 screens[5]: 15.5261, 49% too high"
rng11 = np.random.default_rng(11)
z11 = rng11.standard_normal(100000)
assert abs(np.mean(math.exp(-0.05) * np.maximum(100 * np.exp(0.12 - 0.02 + 0.2 * z11) - 100, 0)) - 15.5343) < 5e-5, "l11 screens[5] byKey.real: 15.5343 on the same draws"
assert abs(np.mean(np.maximum(100 * np.exp(0.05 - 0.02 + 0.2 * z11) - 100, 0)) - 10.9893) < 5e-5 and abs(C0 * math.exp(0.05) - 10.9864) < 5e-5, "l11 screens[6]: 10.9893 sample, 10.9864 limit"
assert abs(100 * math.exp(0.05) - 105.13) < 0.005, "l11 screens[5] byKey.zero: forward 105.13"
# Vasicek bond: closed form, no-noise, and the seeded simulation
def vasicek(r0, kap, th, sg, T0):
    B = (1 - math.exp(-kap * T0)) / kap
    A = (th - sg ** 2 / (2 * kap ** 2)) * (B - T0) - sg ** 2 * B ** 2 / (4 * kap)
    return math.exp(A - B * r0)
assert abs(vasicek(0.06, 0.5, 0.04, 0.01, 5) - 0.789581) < 1e-6 and abs(vasicek(0.06, 0.5, 0.04, 0.0, 5) - 0.789215) < 1e-6, "l11 screens[7]: 0.789581 and 0.789215"
assert abs((0.789581 - 0.789215) / 0.000171 - 2.14) < 0.01, "l11 screens[7]: 2.14 standard errors"
# no noise: e^{-int r} along the deterministic path r(t) = theta + (r0 - theta) e^{-kappa t}
det = integrate.quad(lambda s: 0.04 + 0.02 * math.exp(-0.5 * s), 0, 5)[0]
assert abs(math.exp(-det) - 0.789215) < 1e-6, "l11 screens[7]: the no-noise price is the deterministic discount"
# Jensen: E e^{-X} >= e^{-E X}, so noise raises the price
assert vasicek(0.06, 0.5, 0.04, 0.01, 5) > vasicek(0.06, 0.5, 0.04, 0.0, 5), "l11 screens[7].explain: noise raises the price (Jensen)"
vb = ns11["vasicek_bond_mc"](0.06, 0.5, 0.04, 0.01, 5, 500, 20000, 21)
assert abs(vb[0] - 0.789530) < 2e-6 and abs(vb[1] - 0.000171) < 2e-6, "l11 screens[7].explain, prose: simulation 0.789530, se 0.000171"
# sigma = 0: the forward
assert abs(math.exp(-0.05) * (100 * math.exp(0.05) - 100) - 4.8771) < 5e-5 and abs(100 - 100 * math.exp(-0.05) - 4.8771) < 5e-5 and abs(C0 - 4.8771 - 5.5735) < 5e-5, "l11 screens[8]: 4.8771; volatility adds 5.5735"
assert 100 ** 10 == 10 ** 20, "l11 screens[10]"
assert abs(Phi((math.log(100 / 110) + 0.03) / 0.2) - 0.3720) < 5e-5 and abs(math.exp(-0.05) * 0.3720 - 0.354) < 5e-4, "l11 quiz q-digital"
# review-3 r-drift: mu = 8%: 12.4745 exact; million draws with rng(11) about 12.4735
assert abs(exact_real(0.08) - 12.4745) < 5e-5 and abs(exact_real(0.08) * math.exp(0.05) - 13.114) < 5e-4, "review-3 r-drift"
z1m = np.random.default_rng(11).standard_normal(1000000)
mc8 = np.mean(math.exp(-0.05) * np.maximum(100 * np.exp(0.08 - 0.02 + 0.2 * z1m) - 100, 0))
assert abs(mc8 - 12.4735) < 5e-4, "review-3 r-drift.explain: 12.4735 on a million draws"
assert abs(14.70 / math.sqrt(20000) - 0.104) < 5e-4, "review-3 r-se"
# homework-3 h-drift-sim limits
assert abs(exact_real(0.09) - 13.1997) < 5e-5 and abs(C0 * math.exp(0.05) * math.exp(-0.06) - 10.3466) < 5e-5 and abs(exact_real(0.09) * math.exp(0.05 - 0.09) - 12.6821) < 5e-5, "homework-3 h-drift-sim: 13.1997, 10.3466, 12.6821"
za = np.random.default_rng(2).standard_normal(1000000)
anti = 0.5 * (np.maximum(100 * np.exp(0.03 + 0.2 * za) - 100, 0) + np.maximum(100 * np.exp(0.03 - 0.2 * za) - 100, 0)) * math.exp(-0.05)
assert abs(anti.mean() - C0) < 0.03, "homework-3 h-drift-sim option anti: antithetic pairs converge to the price (sim: hw3_anti)"
# homework-3 h-vasicek
assert abs(vasicek(0.03, 0.8, 0.05, 0.015, 3) - 0.8807) < 5e-5 and abs(vasicek(0.03, 0.8, 0.05, 0.0, 3) - 0.8805) < 5e-5 and abs(math.exp(-0.09) - 0.9139) < 5e-5, "homework-3 h-vasicek: 0.8807, 0.8805, 0.9139"
Bv = (1 - math.exp(-2.4)) / 0.8
assert abs(Bv - 1.1366) < 5e-5 and abs((0.05 - 0.015 ** 2 / (2 * 0.64)) * (Bv - 3) - 0.015 ** 2 * Bv ** 2 / 3.2 + 0.0929) < 5e-5, "homework-3 h-vasicek: B, A"
vb7 = ns11["vasicek_bond_mc"](0.03, 0.8, 0.05, 0.015, 3, 300, 200000, 7)
assert abs(vb7[0] - 0.880800) < 2e-6 and abs(vb7[1] - 0.000043) < 2e-6, "homework-3 h-vasicek.explain: 0.880800, se 0.000043"

# =============================== l12: the pricer ===============================
l12 = load("l12-four-decimal-pricer.json")
ns12a = check_code("l12 screens[8] code", l12["screens"][8]["widget"])
cn = ns12a["cn_heat_price"]
ns12b = check_code("l12 screens[9] code", l12["screens"][9]["widget"])
expl = ns12b["explicit_heat_price"]
# explicit scheme: lambda = 50/n; prices at 110, 100 steps; blow-up at 96 and 90 (bypassing the guard with an
# independent implementation of the same scheme)


def explicit_raw(S0, K0, r0, s0, T0, nx, nt, L=1.0):
    k0 = 2 * r0 / s0 ** 2
    al, be = -(k0 - 1) / 2, -(k0 + 1) ** 2 / 4
    a1_, a2_ = (k0 + 1) / 2, (k0 - 1) / 2
    tau_end = 0.5 * s0 ** 2 * T0
    xg = np.linspace(-L, L, nx + 1)
    h = xg[1] - xg[0]
    dt = tau_end / nt
    lamv = dt / h ** 2
    uu = np.maximum(np.exp(a1_ * xg) - np.exp(a2_ * xg), 0.0)
    t0 = 0.0
    for _ in range(nt):
        t0 += dt
        new = uu.copy()
        new[1:-1] = uu[1:-1] + lamv * (uu[:-2] - 2 * uu[1:-1] + uu[2:])
        new[0] = 0.0
        new[-1] = math.exp(a1_ * L + a1_ ** 2 * t0) - math.exp(a2_ * L + a2_ ** 2 * t0)
        uu = new
    x0 = math.log(S0 / K0)
    return K0 * math.exp(al * x0 + be * tau_end) * float(np.interp(x0, xg, uu)), lamv
for n_, lam_, price_ in [(110, 0.4545, 10.4480), (100, 0.5, 10.4298), (96, 0.5208, -31.99), (90, 0.5556, -1446998)]:
    p_, l_ = explicit_raw(100, 100, 0.05, 0.2, 1, 100, n_)
    assert abs(l_ - lam_) < 5e-5 and abs(l_ - 50 / n_) < 1e-12, f"l12 screens[0]: lambda = 50/n at n = {n_}"
    assert abs(p_ - price_) < max(0.005, 2e-6 * abs(price_)), f"l12 screens[0] table: price {price_} at {n_} steps (sim: l12_explicit_table), got {p_}"
assert abs(expl(100, 100, 0.05, 0.2, 1, 100, 110) - 10.448014224) < 1e-6, "l12 screens[9] test: the lesson's explicit pricer agrees"
s2top = math.sin(99 * math.pi / 200) ** 2
assert abs(s2top - 0.99975) < 5e-6 and abs(1 - 4 * 0.5208 * s2top + 1.083) < 1e-3 and abs(1 - 4 * (50 / 90) * s2top + 1.2217) < 5e-5, "l12 screens[1]: factors -1.0828 and -1.2217"
assert 2000 < 1.0828 ** 96 < 2200, "l12 screens[1].explain: (-1.0828)^96 about 2100"
# von Neumann: the explicit factor leaves [-1, 1] exactly when lambda > 1/(4 s^2) ~ 0.5
assert abs(1 - 4 * 0.5 * s2top) <= 1 and abs(1 - 4 * 0.5208 * s2top) > 1, "l12 screens[0].explain: the factor curve crosses -1 at lambda = 0.5"
# Crank-Nicolson factor and unconditional stability
g = lambda lamv, s2: (1 - 2 * lamv * s2) / (1 + 2 * lamv * s2)
lams = np.logspace(-3, 4, 200)
assert all(abs(g(lv, s2)) < 1 for lv in lams for s2 in [1e-4, 0.5, 0.99975, 1.0]), "l12 screens[2] line g5: |g| < 1 for every lambda > 0"
s2_400 = math.sin(399 * math.pi / 800) ** 2
assert abs(g(200, s2_400) + 0.9950) < 5e-5, "l12 screens[2].explain, [6]: g = -0.9950 at lambda = 200"
# CN mode factor from the scheme itself (g1 to g4): apply one CN step to a discrete mode on 400 intervals
nxm = 400
xm = np.linspace(-1, 1, nxm + 1)
h_ = xm[1] - xm[0]
km = 3 * math.pi / 2
mode = np.sin(km * (xm + 1))
lam_m = 1.3
Am = np.diag((1 + 2 * 0.5 * lam_m) * np.ones(nxm - 1)) + np.diag(-0.5 * lam_m * np.ones(nxm - 2), 1) + np.diag(-0.5 * lam_m * np.ones(nxm - 2), -1)
rhs_m = mode[1:-1] + 0.5 * lam_m * (mode[:-2] - 2 * mode[1:-1] + mode[2:])
new_m = np.linalg.solve(Am, rhs_m)
s2m = math.sin(km * h_ / 2) ** 2
assert np.allclose(new_m, g(lam_m, s2m) * mode[1:-1], atol=1e-9), "l12 screens[2] lines g1 to g4: the CN step multiplies a mode by (1 - 2 lam s^2)/(1 + 2 lam s^2)"
# CN convergence table with n_t = n_x / 5
prices = {nx_: cn(100, 100, 0.05, 0.2, 1, nx_, nx_ // 5) for nx_ in [100, 200, 400, 800, 1600]}
want = {100: 10.4427214, 200: 10.4486123, 400: 10.4500869, 800: 10.4504574, 1600: 10.4505511}
for nx_, p_ in want.items():
    assert abs(prices[nx_] - p_) < 5e-8, f"l12 screens[3] table: CN price on {nx_} intervals"
errs = [(C0 - prices[nx_]) * 1e6 for nx_ in [100, 200, 400, 800, 1600]]
assert abs(errs[0] - 7862.2) < 0.1 and abs(errs[1] - 1971.3) < 0.1 and abs(errs[2] - 496.6) < 0.2 and abs(errs[3] - 126.1) < 0.2 and abs(errs[4] - 32.5) < 0.1, "l12 screens[3]: errors times 1e6"
ratios = [errs[i] / errs[i + 1] for i in range(4)]
assert all(abs(rr - ww) < 0.01 for rr, ww in zip(ratios, [3.99, 3.97, 3.94, 3.88])), f"l12 screens[3].explain: ratios 3.99, 3.97, 3.94, 3.88 (second order), got {ratios}"
assert errs[4] < 50 < errs[3], "l12 screens[3].explain, [5]: only the 1,600 grid is within 5e-5"
rich = lambda vc, vf, p=2: vf + (vf - vc) / (2 ** p - 1)
assert abs(rich(prices[100], prices[200]) - 10.4505760) < 1e-7 and abs(C0 - rich(prices[100], prices[200]) - 7.6e-6) < 2e-7, "l12 screens[4]: Richardson 10.4505760, 7.6e-6 below"
assert abs(rich(prices[200], prices[400]) - 10.4505785) < 1e-7, "l12 screens[4].explain: 10.4505785 from 200 and 400"
# trap: 400 by 4 gives 10.0085 with negative gamma; Rannacher 10.4492 with positive gamma; 1600 by 50 still 0.0308 off


def cn_grid(S0, K0, r0, s0, T0, nx, nt, L=1.0, rannacher=False):
    """Same scheme as the lesson, returning the price on every node of an S grid for gamma."""
    k0 = 2 * r0 / s0 ** 2
    al, be = -(k0 - 1) / 2, -(k0 + 1) ** 2 / 4
    a1_, a2_ = (k0 + 1) / 2, (k0 - 1) / 2
    tau_end = 0.5 * s0 ** 2 * T0
    xg = np.linspace(-L, L, nx + 1)
    h = xg[1] - xg[0]
    dt = tau_end / nt
    uu = np.maximum(np.exp(a1_ * xg) - np.exp(a2_ * xg), 0.0)
    edge = lambda t0: math.exp(a1_ * L + a1_ ** 2 * t0) - math.exp(a2_ * L + a2_ ** 2 * t0)

    def step(uu, t0, dt, theta):
        lamv = dt / h ** 2
        inner = uu[1:-1]
        rhs = inner + (1 - theta) * lamv * (uu[:-2] - 2 * inner + uu[2:])
        right = edge(t0 + dt)
        rhs[-1] += theta * lamv * right
        n = nx - 1
        M = np.diag((1 + 2 * theta * lamv) * np.ones(n)) + np.diag(-theta * lamv * np.ones(n - 1), 1) + np.diag(-theta * lamv * np.ones(n - 1), -1)
        new = uu.copy()
        new[1:-1] = np.linalg.solve(M, rhs)
        new[0], new[-1] = 0.0, right
        return new
    t0 = 0.0
    n_cn = nt
    if rannacher:
        for _ in range(2):
            uu = step(uu, t0, dt / 2, 1.0); t0 += dt / 2
        n_cn = nt - 1
    for _ in range(n_cn):
        uu = step(uu, t0, dt, 0.5); t0 += dt
    Sg = K0 * np.exp(xg)
    Vg = K0 * np.exp(al * xg + be * tau_end) * uu
    return Sg, Vg
Sg, Vg = cn_grid(100, 100, 0.05, 0.2, 1, 400, 4)
assert abs(Vg[200] - 10.0085) < 5e-5 and abs(Vg[200] - cn(100, 100, 0.05, 0.2, 1, 400, 4)) < 1e-9, "l12 screens[6] trap: 10.0085 at 400 by 4 (dense solve agrees with Thomas)"
gam = (Vg[2:] - 2 * Vg[1:-1] + Vg[:-2]) / ((Sg[2:] - Sg[:-2]) / 2) ** 2
assert gam.min() < -0.1, "l12 screens[6]: gamma goes negative beside the strike (sim: l12_gamma)"
Sg2, Vg2 = cn_grid(100, 100, 0.05, 0.2, 1, 400, 4, rannacher=True)
gam2 = (Vg2[2:] - 2 * Vg2[1:-1] + Vg2[:-2]) / ((Sg2[2:] - Sg2[:-2]) / 2) ** 2
assert abs(Vg2[200] - 10.4492) < 5e-5 and (gam2[150:250] > 0).all(), "l12 screens[6].explain: Rannacher 10.4492, every gamma positive near the strike"
true_gamma = lambda S0: phi((math.log(S0 / 100) + 0.07) / 0.2) / (S0 * 0.2)
assert abs(true_gamma(100) - 0.01876) < 5e-6 and all(true_gamma(S0) > 0 for S0 in np.linspace(50, 200, 50)), "l12 screens[6] option formula why: gamma positive everywhere"
assert abs(C0 - cn(100, 100, 0.05, 0.2, 1, 1600, 50) - 0.0308) < 5e-4, "l12 screens[6].explain: 1,600 intervals with 50 steps still 0.0308 off"
assert abs(C0 - 10.0085 - 0.44) < 0.005, "l12 screens[6].explain: wrong by 44 pence"
# the implicit half step's factor (quiz q-rannacher): 1/(1 + 4 lam s^2)
assert abs(1 / (1 + 4 * 100 * s2_400) - 0.0025) < 1e-4, "l12 quiz q-rannacher: implicit factor near 0 for large lambda"
# edge: 101 intervals interpolates at the strike: 10.4694; 201 intervals and 20 steps: 0.0031 off
assert abs(cn(100, 100, 0.05, 0.2, 1, 101, 20) - 10.4694) < 5e-5 and abs(cn(100, 100, 0.05, 0.2, 1, 101, 20) - C0 - 0.0188) < 5e-4 and abs(C0 - cn(100, 100, 0.05, 0.2, 1, 100, 20) - 0.0079) < 5e-5, "l12 screens[7]: 10.4694, errors 0.0188 above and 0.0079 below"
assert abs(0.018829 / 0.007862 - 2.39) < 0.005, "l12 screens[7]: ratio 2.4"
assert abs(cn(100, 100, 0.05, 0.2, 1, 201, 20) - C0 - 0.0031) < 5e-4, "l12 screens[7].explain: 201 intervals still 0.0031 off"
# linear interpolation error across a cell is h^2 u_xx / 8 (midpoint)
f_ = lambda s: s ** 2
assert abs((f_(0) + f_(0.1)) / 2 - f_(0.05) - 0.1 ** 2 * 2 / 8) < 1e-15, "l12 screens[7].explain: interpolation adds h^2 u_xx / 8"
# screens[8].explain: the S-grid solve to 300 (600 intervals, 200 steps) gives 10.4500, 0.0006 below


def cn_S(S0, K0, r0, s0, T0, Smax, nS, nt):
    Sg = np.linspace(0, Smax, nS + 1)
    dS = Sg[1] - Sg[0]
    dt = T0 / nt
    Vv = np.maximum(Sg - K0, 0.0)
    i = np.arange(1, nS)
    a_ = 0.5 * s0 ** 2 * Sg[i] ** 2 / dS ** 2 - 0.5 * r0 * Sg[i] / dS
    b_ = -s0 ** 2 * Sg[i] ** 2 / dS ** 2 - r0
    c_ = 0.5 * s0 ** 2 * Sg[i] ** 2 / dS ** 2 + 0.5 * r0 * Sg[i] / dS
    Lm = np.diag(b_) + np.diag(c_[:-1], 1) + np.diag(a_[1:], -1)
    Id = np.eye(nS - 1)
    Aimp = Id - 0.5 * dt * Lm
    Aexp = Id + 0.5 * dt * Lm
    tt0 = 0.0
    for _ in range(nt):
        tt0 += dt
        rhs = Aexp @ Vv[1:-1]
        rhs[0] += 0.5 * dt * a_[0] * (0.0 + 0.0)
        new_edge = Smax - K0 * math.exp(-r0 * (T0 - tt0))
        old_edge = Vv[-1]
        rhs[-1] += 0.5 * dt * c_[-1] * (new_edge + old_edge) - 0.5 * dt * c_[-1] * old_edge * 0  # explicit half already in Aexp @ V (uses old edge) -> add only new edge half
        Vv[1:-1] = np.linalg.solve(Aimp, rhs)
        Vv[0], Vv[-1] = 0.0, new_edge
    return float(np.interp(S0, Sg, Vv))
pS = cn_S(100, 100, 0.05, 0.2, 1, 300, 600, 200)
assert abs(pS - 10.4500) < 2e-4 and abs(C0 - pS - 0.0006) < 2e-4, f"l12 screens[8].explain: S-grid solve gives 10.4500, 0.0006 below (independent solver, got {pS:.5f})"
# screens[9]: Richardson at S = 110 off the node lands 0.0012 below
p110 = rich(cn(110, 100, 0.05, 0.2, 1, 200, 40), cn(110, 100, 0.05, 0.2, 1, 400, 80))
assert abs(bs_call(110, 100, 0.05, 0.2, 1) - p110 - 0.0012) < 2e-4, "l12 screens[9].explain: off the node Richardson lands 0.0012 below"
assert abs(ns12b["price_to_4dp"](100, 100, 0.05, 0.2, 1)[0] - C0) < 1e-5, "l12 screens[9]: Richardson on 200 and 400 within 1e-5 at the strike node"
# quiz q-steps: 200 intervals, dx = 0.01, dt <= dx^2/2 -> 400 steps
assert 0.02 / (0.01 ** 2 / 2) == 400, "l12 quiz q-steps"
# quiz q-boundary: narrowing to [-0.5, 0.5] at the same spacing shifts by -3.2e-6; widening to 1.5 by 4e-11
pw = cn(100, 100, 0.05, 0.2, 1, 200, 40)
pn = cn(100, 100, 0.05, 0.2, 1, 100, 40, L=0.5)
pwide = cn(100, 100, 0.05, 0.2, 1, 300, 40, L=1.5)
assert abs((pn - pw) * 1e6 + 3.2) < 0.1 and abs(pn - 10.4486091) < 5e-8, "l12 quiz q-boundary: -3.2e-6"
assert abs(pwide - pw) < 1e-10, "l12 quiz q-boundary.explain: widening changes the price by about 4e-11"
# q-order
assert abs(496.6 / 126.1 - 3.94) < 0.005, "l12 quiz q-order"
# review-3 r-rich, r-agree, r-put, r-decay
C2 = bs_call(100, 100, 0.03, 0.25, 0.5)
assert abs(C2 - 7.7602567) < 5e-8 and abs(cn(100, 100, 0.03, 0.25, 0.5, 200, 40) - 7.7576434) < 5e-8 and abs(cn(100, 100, 0.03, 0.25, 0.5, 400, 80) - 7.7596032) < 5e-8, "review-3 r-rich: the two CN prices"
assert abs(rich(7.7576434, 7.7596032) - 7.7602565) < 1e-7 and abs(C2 - rich(7.7576434, 7.7596032) - 2e-7) < 1e-7, "review-3 r-rich: 7.7602565, 2e-7 below"
assert abs(10.45058 - 10.45054 - 4e-5) < 1e-12, "review-3 r-agree"
assert abs(C2 - 100 + 100 * math.exp(-0.015) - 6.2715) < 5e-5 and abs(100 * math.exp(-0.015) - 98.5112) < 5e-5 and abs(100 - 98.5112 - 1.4888) < 5e-5, "review-3 r-put"
assert abs(0.5 * (3 * math.pi / 4) ** 2 - 2.7758) < 5e-5 and abs(math.exp(-2.7758) - 0.0623) < 5e-5, "review-3 r-decay"
# homework-3 h-put-4dp code and numbers
hw3 = load("homework-3.json")
nsp = check_code("homework-3 h-put-4dp code", hw3["items"][0]["widget"])
assert abs(bs_put(100, 100, 0.06, 0.2, 0.75) - 4.7751999) < 5e-8 and abs(nsp["price_put_4dp"](100, 100, 0.06, 0.2, 0.75)[0] - 4.7752000) < 5e-8, "homework-3 h-put-4dp.explain: 4.7752000 against 4.7751999"
assert abs(bs_put(120, 120, 0.04, 0.2, 0.75) - 6.5076262) < 5e-8 and abs(nsp["price_put_4dp"](120, 120, 0.04, 0.2, 0.75)[0] - 6.5076263) < 5e-8, "homework-3 h-put-4dp.explain: 6.5076263 against 6.5076262"
assert abs(bs_put(90, 90, 0.05, 0.25, 0.4) - 4.768697) < 5e-7, "homework-3 h-put-4dp test 3"
# the put's heat start and left edge (prose): u0 = e^{-alpha x} max(1 - e^x, 0) = max(e^{a2 x} - e^{a1 x}, 0)
k25 = 2.5
assert np.allclose(np.exp(0.75 * xx) * np.maximum(1 - np.exp(xx), 0), np.maximum(np.exp((k25 - 1) / 2 * xx) - np.exp((k25 + 1) / 2 * xx), 0)), "homework-3 h-put-4dp.prose: the put's start"
# homework-3 h-explicit
lam_e = (0.02 / 12) / 0.05 ** 2
assert abs(lam_e - 0.6667) < 5e-5 and abs(math.sin(39 * math.pi / 80) ** 2 - 0.99846) < 5e-6 and abs(1 - 4 * lam_e * 0.99846 + 1.6626) < 5e-5 and abs(1.6626 ** 12 - 446) < 1, "homework-3 h-explicit"
# homework-3 h-sequence: CN errors for (100, 100, 0.03, 0.25, 0.5) on 400, 800, 1600; Richardson 200/400 at 2e-7
e400 = C2 - cn(100, 100, 0.03, 0.25, 0.5, 400, 80)
e800 = C2 - cn(100, 100, 0.03, 0.25, 0.5, 800, 160)
e1600 = C2 - cn(100, 100, 0.03, 0.25, 0.5, 1600, 320)
assert abs(e400 - 6.535e-4) < 5e-7 and abs(e800 - 1.635e-4) < 5e-7 and abs(e1600 - 4.10e-5) < 5e-7, "homework-3 h-sequence: 6.535e-4, 1.635e-4, 4.10e-5"
assert e1600 < 5e-5 < e800 and abs(400 * math.sqrt(6.535e-4 / 5e-5) - 1446) < 1, "homework-3 h-sequence: 1,600 is the first; 1,446 is the crossing"
assert 200 * 40 + 400 * 80 == 40000 and 1600 * 320 == 512000, "homework-3 h-sequence.explain: node-steps"
# homework-3 h-colleague model (T = 0.5)
C5 = bs_call(100, 100, 0.05, 0.2, 0.5)
assert abs(C5 - 6.8887286) < 5e-8, "homework-3 h-colleague: closed form 6.8887286"
assert abs(cn(100, 100, 0.05, 0.2, 0.5, 400, 4) - 6.5728) < 5e-5 and abs(cn(100, 100, 0.05, 0.2, 0.5, 400, 4, rannacher=True) - 6.8837) < 5e-5 and abs(C5 - 6.8837 - 0.0050) < 5e-5, "homework-3 h-colleague model 1, 3: 6.5728, Rannacher 6.8837"
lam5 = (0.01 / 4) / 0.005 ** 2
assert abs(lam5 - 100) < 1e-9 and abs(g(100, s2_400) + 0.9900) < 5e-5 and abs(1 / (1 + 2 * 100 * s2_400) - 0.005) < 1e-4, "homework-3 h-colleague model 2, 3: lambda 100, g -0.9900, implicit factor 0.005"
assert abs(C5 - cn(100, 100, 0.05, 0.2, 0.5, 1600, 50) - 0.0185) < 5e-4, "homework-3 h-colleague model 3: 1,600 by 50 still 0.0185 off"
seq5 = {nx_: cn(100, 100, 0.05, 0.2, 0.5, nx_, nx_ // 5) for nx_ in [100, 200, 400, 800, 1600]}
want5 = {100: 6.8760493, 200: 6.8855674, 400: 6.8879388, 800: 6.8885312, 1600: 6.8886792}
for nx_, p_ in want5.items():
    assert abs(seq5[nx_] - p_) < 5e-8, f"homework-3 h-colleague model 4: CN price on {nx_} intervals"
errs5 = [C5 - seq5[n_] for n_ in [100, 200, 400, 800, 1600]]
assert all(abs(e_ - w_) / w_ < 0.01 for e_, w_ in zip(errs5, [1.27e-2, 3.16e-3, 7.90e-4, 1.97e-4, 4.93e-5])), "homework-3 h-colleague model 4: the errors"
assert abs(rich(seq5[100], seq5[200]) - 6.8887402) < 2e-7 and abs(rich(seq5[100], seq5[200]) - C5 - 1.2e-5) < 1e-6, "homework-3 h-colleague model 4: Richardson 6.8887402, 1.2e-5 above"
Sg5, Vg5 = cn_grid(100, 100, 0.05, 0.2, 0.5, 400, 4)
gam5 = (Vg5[2:] - 2 * Vg5[1:-1] + Vg5[:-2]) / ((Sg5[2:] - Sg5[:-2]) / 2) ** 2
i995 = np.argmin(np.abs(Sg5[1:-1] - 99.5))
assert abs(gam5[i995] + 0.277) < 0.01, "homework-3 h-colleague model 1: gamma -0.277 near 99.5"
assert abs(phi((math.log(0.995) + 0.035) / (0.2 * math.sqrt(0.5))) / (99.5 * 0.2 * math.sqrt(0.5)) - 0.027) < 1e-3, "homework-3 h-colleague model 1: true gamma 0.027"

print("pdes-L3-concepts: all checks passed")
