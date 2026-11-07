"""Second-route checks of the longform items: ito L3 h-derive-black, ito L4 h-aloud-unknown-drift,
alpha L3 h-overlap-aloud. Venv Python (sympy, numpy). Exits 0 when every check holds."""
import math, sys
import numpy as np
import sympy as sp

fails = 0
def check(name, ok, info=""):
    global fails
    fails += not ok
    print(("  ok   " if ok else "  FAIL ") + name + (f"  [{info}]" if info else ""))

N = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))

print("ito L3 h-derive-black")
t, s, r, mu, sig, TF, T, K = sp.symbols("t s r mu sigma T_F T K", real=True)
f = s * sp.exp(r * (TF - t))
check("f_t = -r f, f_ss = 0", sp.simplify(sp.diff(f, t) + r * f) == 0 and sp.diff(f, s, 2) == 0)
driftF = sp.diff(f, t) + mu * s * sp.diff(f, s) + sp.Rational(1, 2) * sig**2 * s**2 * sp.diff(f, s, 2)
check("dF drift (mu - r) F, diffusion sigma F", sp.simplify(driftF - (mu - r) * f) == 0 and sp.simplify(sig * s * sp.diff(f, s) - sig * f) == 0)
F = sp.symbols("F", positive=True)
Vt, VF, VFF, V = sp.symbols("V_t V_F V_FF V")
Delta = F * VF / s
dW = -sig * F * VF + Delta * sig * s
dt = -(Vt + (mu - r) * F * VF + sp.Rational(1, 2) * sig**2 * F**2 * VFF) + mu * Delta * s
check("dW coefficient zero at Delta = F V_F / S", sp.simplify(dW) == 0)
check("mu cancels in the dt coefficient", sp.diff(sp.expand(dt), mu) == 0)
eq = sp.expand(dt - r * (-V + Delta * s))
check("no arbitrage gives -(V_t + 1/2 s^2 F^2 V_FF - r V)", sp.simplify(eq + (Vt + sp.Rational(1, 2) * sig**2 * F**2 * VFF - r * V)) == 0)
check("e^{0.06} = 1.0618", f"{math.exp(0.06):.4f}" == "1.0618", f"{math.exp(0.06):.6f}")
Vfwd = sp.exp(-r * (T - t)) * (F - K)
check("e^{-r(T-t)}(F - K) solves the equation", sp.simplify(sp.diff(Vfwd, t) + sp.Rational(1, 2) * sig**2 * F**2 * sp.diff(Vfwd, F, 2) - r * Vfwd) == 0)
check("static replication e^{r(T_F-T)} S - K e^{-r(T-t)} equals it", sp.simplify(sp.exp(r * (TF - T)) * s - K * sp.exp(-r * (T - t)) - Vfwd.subs(F, f)) == 0)
# change of variables with a general V
Vf = sp.Function("V")
U = Vf(t, f)
bs = sp.diff(U, t) + r * s * sp.diff(U, s) + sp.Rational(1, 2) * sig**2 * s**2 * sp.diff(U, s, 2) - r * U
Fs = sp.Symbol("Fs", positive=True)
lhs = sp.simplify(bs)
# compare with V_t + 1/2 sig^2 F^2 V_FF - r V evaluated at F = f, by a concrete smooth V
Vc = lambda tt, FF: sp.exp(-2 * tt) * FF**3 + sp.sin(tt) * sp.log(FF)
Uc = Vc(t, f)
bsc = sp.diff(Uc, t) + r * s * sp.diff(Uc, s) + sp.Rational(1, 2) * sig**2 * s**2 * sp.diff(Uc, s, 2) - r * Uc
blk = (sp.diff(Vc(t, F), t) + sp.Rational(1, 2) * sig**2 * F**2 * sp.diff(Vc(t, F), F, 2) - r * Vc(t, F)).subs(F, f)
check("U(t,S) = V(t, S e^{r(T_F-t)}) turns Black-Scholes into the forward equation", sp.simplify(bsc - blk) == 0)
# second route: a seeded discrete hedge of a call on the forward, shares e^{r(T_F - t)} V_F, under two drifts
def hedge_err(muv, steps, seed, S0=100.0, rr=0.04, sg=0.25, Tx=1.0, TFx=1.5, Kx=105.0, paths=4000):
    rng = np.random.default_rng(seed)
    S = np.full(paths, S0); dt_ = Tx / steps
    def vfun(tt, Fv):
        v = sg * math.sqrt(Tx - tt); d1 = (np.log(Fv / Kx) + v * v / 2) / v
        Nd1 = 0.5 * (1 + np.vectorize(math.erf)(d1 / math.sqrt(2))); Nd2 = 0.5 * (1 + np.vectorize(math.erf)((d1 - v) / math.sqrt(2)))
        return math.exp(-rr * (Tx - tt)) * (Fv * Nd1 - Kx * Nd2), math.exp(-rr * (Tx - tt)) * Nd1
    Fv = S * math.exp(rr * (TFx - 0)); V0, VF0 = vfun(0.0, Fv)
    sh = math.exp(rr * TFx) * VF0; cash = V0 - sh * S
    for i in range(steps):
        tt = i * dt_
        S = S * np.exp((muv - sg**2 / 2) * dt_ + sg * math.sqrt(dt_) * rng.standard_normal(paths))
        cash = cash * math.exp(rr * dt_)
        tn = tt + dt_
        if i + 1 < steps:
            _, VFn = vfun(tn, S * math.exp(rr * (TFx - tn)))
            new = math.exp(rr * (TFx - tn)) * VFn
            cash -= (new - sh) * S; sh = new
    pay = np.maximum(S * math.exp(rr * (TFx - Tx)) - Kx, 0)
    return float(np.sqrt(np.mean((sh * S + cash - pay) ** 2))), V0[0] if hasattr(V0, "__len__") else V0
for muv in (0.0, 0.3):
    e1, v0 = hedge_err(muv, 50, 1); e2, _ = hedge_err(muv, 400, 1)
    check(f"discrete hedge error shrinks like 1/sqrt(steps), mu = {muv}", 2.0 < e1 / e2 < 4.0, f"rms {e1:.4f} -> {e2:.4f}, price {float(v0):.4f}")

print("ito L4 h-aloud-unknown-drift")
S_, Vs, Vss, C, D_, m = sp.symbols("S V_S V_SS C Delta mu_t")
book_dW = -sig * S_ * Vs + D_ * sig * S_
book_dt = -(Vt + m * S_ * Vs + sp.Rational(1, 2) * sig**2 * S_**2 * Vss) + D_ * m * S_ + r * (V - D_ * S_)
check("dW coefficient sigma S (Delta - V_S)", sp.simplify(book_dW - sig * S_ * (D_ - Vs)) == 0)
left = sp.expand(book_dt.subs(D_, Vs))
check("at Delta = V_S the dt term is free of mu_t", sp.diff(left, m) == 0)
check("and equals -V_t - 1/2 s^2 S^2 V_SS + r V - r S V_S", sp.simplify(left - (-Vt - sp.Rational(1, 2) * sig**2 * S_**2 * Vss + r * V - r * S_ * Vs)) == 0)
check("£1 at T: e^{-r(T-t)} solves", sp.simplify(sp.diff(sp.exp(-r * (T - t)), t) - r * sp.exp(-r * (T - t))) == 0)
# second route: self-financing Black-Scholes delta hedge of a call under path-dependent drifts
def bs(tt, Sv, rr, sg, Tx, Kx):
    v = sg * math.sqrt(Tx - tt); d1 = (np.log(Sv / Kx) + (rr + sg**2 / 2) * (Tx - tt)) / v
    Nf = np.vectorize(lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2))))
    return Sv * Nf(d1) - Kx * math.exp(-rr * (Tx - tt)) * Nf(d1 - v), Nf(d1)
def path_hedge(drift, steps, seed, S0=100.0, rr=0.03, sg=0.2, Tx=1.0, Kx=100.0, paths=4000):
    rng = np.random.default_rng(seed); dt_ = Tx / steps
    S = np.full(paths, S0); run_max = S.copy(); avg = S.copy()
    V0, dl = bs(0.0, S, rr, sg, Tx, Kx); cash = V0 - dl * S; book0 = cash + dl * S - V0
    for i in range(steps):
        mu_t = drift(S, run_max, avg, i * dt_)
        S = S * np.exp((mu_t - sg**2 / 2) * dt_ + sg * math.sqrt(dt_) * rng.standard_normal(paths))
        run_max = np.maximum(run_max, S); avg = avg + (S - avg) / (i + 2)
        cash = cash * math.exp(rr * dt_)
        if i + 1 < steps:
            _, new = bs((i + 1) * dt_, S, rr, sg, Tx, Kx); cash -= (new - dl) * S; dl = new
    err = dl * S + cash - np.maximum(S - Kx, 0)
    return float(np.sqrt(np.mean(err**2))), float(np.max(np.abs(book0)))
drifts = {
    "constant 8%": lambda S, M, A, tt: 0.08,
    "chases its running maximum": lambda S, M, A, tt: np.where(S >= M * 0.98, 0.6, -0.4),
    "mean-reverts to its own past average": lambda S, M, A, tt: 2.0 * np.log(A / S),
}
for name, dfun in drifts.items():
    e1, b0 = path_hedge(dfun, 50, 7); e2, _ = path_hedge(dfun, 800, 7)
    check(f"zero-cost book, hedge error shrinks, drift {name}", b0 < 1e-12 and 3.0 < e1 / e2 < 5.5, f"rms {e1:.4f} -> {e2:.4f}")

print("alpha L3 h-overlap-aloud")
h, n, tval = 63, 756, 9.5
check("sum_{k=1}^{62} (1 - k/63) = 31 = (h - 1)/2", abs(sum(1 - k / h for k in range(1, h)) - 31) < 1e-12)
check("1 + 2 * 31 = 63", 1 + 2 * 31 == h)
Fexact = 1 + 2 / n * sum((n - k) * (1 - k / h) for k in range(1, h))
check("finite-n factor with end effects about 61.2 (author) / 61.25", abs(Fexact - 61.25) < 0.01, f"{Fexact:.3f}")
check("sqrt 63 = 7.94, 9.5/7.94 = 1.2", f"{math.sqrt(63):.2f}" == "7.94" and f"{tval / math.sqrt(63):.1f}" == "1.2", f"{tval / math.sqrt(63):.4f}")
check("756/12 = 63", 756 / 12 == 63)
Es2 = (n - Fexact) / (n - 1)          # E[s^2] / sigma^2 for a stationary series
honest_rms = tval / (math.sqrt(Fexact) / math.sqrt(Es2))
check("with end effects and the low bias of s^2, honest t 1.16 (still 'about 1.2', below 2)", 1.1 < honest_rms < 1.25, f"E[s^2]/sigma^2 = {Es2:.3f}, t = {honest_rms:.3f}")
# Newey-West with Bartlett weights 1 - k/(L+1), as h-newey-west defines it, against the true triangle 1 - k/63
def nw_factor(L):
    return 1 + 2 * sum((1 - k / (L + 1)) * max(1 - k / h, 0) for k in range(1, L + 1))
f62 = nw_factor(62)
check("population Newey-West factor at 62 lags is 42, not 63", abs(f62 - 42.0) < 0.01, f"{f62:.2f}; SE low by {1 - math.sqrt(f62 / 63):.0%}")
# seeded simulation: daily noise, each IC the mean of the next 63 days; NW(62) t against the true t
rng = np.random.default_rng(31)
ratios, nwratio, nw_vs_s = [], [], []
for _ in range(1500):
    e = rng.standard_normal(n + h)
    c = np.convolve(e, np.ones(h) / h, mode="valid")[:n]
    d = c - c.mean()
    g = [d @ d / n] + [d[k:] @ d[:-k] / n for k in range(1, 63)]
    nw = (g[0] + 2 * sum((1 - k / 63) * g[k] for k in range(1, 63))) / n
    true_var = Fexact * (1 / h) / n          # sigma^2 = 1/h for a mean of h unit normals
    nwratio.append(math.sqrt(nw / true_var))
    nw_vs_s.append(math.sqrt(nw) / (c.std(ddof=1) / math.sqrt(n)))
    ratios.append(math.sqrt(true_var) / (c.std(ddof=1) / math.sqrt(n)))
med = float(np.median(ratios))
check("simulated median inflation sqrt(true var)/(s/sqrt n) near 8.2 to 8.5", 7.9 < med < 8.7, f"{med:.2f}; t {tval / med:.2f}")
nwm = float(np.median(nwratio))
check("NW(62) standard error runs well below the true one (median ratio under 0.8)", nwm < 0.8, f"median NW SE / true SE = {nwm:.2f}; NW(62) t from a naive 9.5 about {tval / float(np.median(nw_vs_s)):.2f}")
print("FAILURES:", fails)
sys.exit(1 if fails else 0)
