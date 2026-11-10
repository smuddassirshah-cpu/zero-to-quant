"""Concept checks for ito level 4 (lessons l13 to l17, review-4, homework-4).

Run from the repo root: python3 -I docs/reports/ito-L4-concepts.py
Each check names the ledger row it supports (docs/reports/audit-ito-4-ledger.md).
A check that fails because the content is wrong or imprecise is marked
EXPECTED_FAIL, carries the corrected assert in a comment beside it, is listed
in the output, and does not change the exit code.
"""
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import integrate
from scipy.stats import norm

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
COURSE = os.path.join(ROOT, "app", "content", "courses", "ito")
rng = np.random.default_rng(20261110)
failures = []
expected = []


def check(cond, name):
    if cond:
        print("ok   ", name)
    else:
        print("FAIL ", name)
        failures.append(name)


def xfail(cond, name):
    """A check of a claim the content makes that is false or imprecise."""
    if cond:
        print("ok   ", name, "(was EXPECTED_FAIL: content now agrees)")
    else:
        print("EXPECTED_FAIL", name)
        expected.append(name)


def close(a, b, tol=6e-5):
    return abs(a - b) <= tol


def load(name):
    with open(os.path.join(COURSE, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- code widgets
def run_widget(label, widget):
    def passes(src):
        env = {}
        try:
            exec(src, env)
        except Exception:
            return 0
        n = 0
        for t in widget["tests"]:
            try:
                got = eval(t["call"], env)
            except Exception:
                continue
            exp = t["expect"]
            if isinstance(exp, str):
                exp = eval(exp, env)
            tol = t.get("tol", {}).get("abs", 0)
            if t.get("compare") == "isclose":
                g = np.atleast_1d(np.array(got, dtype=float))
                e = np.atleast_1d(np.array(exp, dtype=float))
                ok = g.shape == e.shape and bool(np.all(np.abs(g - e) <= tol + 1e-12))
            else:
                ok = got == exp
            n += bool(ok)
        return n
    total = len(widget["tests"])
    s = passes(widget["solution"])
    st = passes(widget["starter"])
    check(s == total, f"{label}: solution passes {s}/{total} hidden tests")
    check(st < total, f"{label}: starter fails ({st}/{total} pass)")
    env = {}
    exec(widget["solution"], env)
    for ex in widget.get("examples", []):
        got = np.atleast_1d(np.array(eval(ex["call"], env), dtype=float))
        e = np.atleast_1d(np.array(eval(ex["expect"], env) if isinstance(ex["expect"], str) else ex["expect"], dtype=float))
        check(bool(np.all(np.abs(got - e) <= ex.get("tol", {}).get("abs", 0) + 1e-12)),
              f"{label}: example {ex['call'][:40]}")
    return env


l13, l14, l15, l16, l17 = (load(n) for n in (
    "l13-martingale-or-not", "l14-hitting-and-exit", "l15-moments-quickly",
    "l16-pricing-in-a-minute", "l17-derivation-aloud"))
hw = load("homework-4")
env13 = run_widget("l13.s8", l13["screens"][8]["widget"])
env14 = run_widget("l14.s8", l14["screens"][8]["widget"])
env15 = run_widget("l15.s7", l15["screens"][7]["widget"])
env16 = run_widget("l16.s8", l16["screens"][8]["widget"])
env17 = run_widget("l17.s8", l17["screens"][8]["widget"])
envh1 = run_widget("hw.h-exit-report", hw["items"][1]["widget"])
envh2 = run_widget("hw.h-quick-prices", hw["items"][2]["widget"])

# ------------------------------------------------------------------ lesson 13
t, x, c, a, b, s, mu, sig = sp.symbols("t x c a b s mu sigma", real=True)


def drift(f, m=0):
    return sp.simplify(sp.diff(f, t) + m * sp.diff(f, x) + sp.Rational(1, 2) * sp.diff(f, x, 2))


check(drift(x**3 - c*t*x) == sp.simplify((3 - c)*x), "l13.s0 drift of W^3 - ctW is (3-c)W")
vals = [drift(f).subs({t: 1, x: 2}) for f in (x**2 + t, sp.exp(4*x - 8*t), x**3 - 3*t*x, x**4)]
check(vals == [2, 0, 0, 24], "l13.s2 drifts 2, 0, 0, 24 at t=1, W=2")
check(drift(sp.exp(4*x - 8*t)) == 0 and drift(x**3 - 3*t*x) == 0, "l13.s2 two martingales have zero drift everywhere")
check(sp.solve(drift(x**4 - 6*t*x**2 + c*t**2), c) == [3], "l13.s3 c = 3 for W^4 - 6tW^2 + ct^2")
check(sp.solve(sp.simplify(drift(sp.exp(5*x + c*t)) / sp.exp(5*x + c*t)), c) == [-sp.Rational(25, 2)], "l13.s4 c = -12.5")
z = sp.symbols("z")
Ez = lambda e: sp.integrate(sp.expand(e) * sp.exp(-z**2/2) / sp.sqrt(2*sp.pi), (z, -sp.oo, sp.oo))
check(Ez((2 + z)**3) == 14, "l13.s5 E[W_2^3 | W_1 = 2] = 14")
w0 = sp.symbols("w0")
check(sp.expand(Ez((w0 + sp.sqrt(t - s)*z)**3) - (w0**3 + 3*(t - s)*w0)) == 0, "l13.quiz3 E[W_t^3|W_s] = W_s^3 + 3(t-s)W_s")
check(sp.simplify(drift(sp.exp(c*x), mu) / sp.exp(c*x) - (mu*c + c**2/2)) == 0, "l13.s7 drift of e^{cX} is (mu c + c^2/2) f")
check(set(sp.solve(mu*c + c**2/2, c)) == {0, -2*mu}, "l13.s7 nonzero root c = -2 mu")
check(drift(t*x**2).subs({t: 2, x: 3}) == 11, "l13.quiz0 drift of tW^2 is 11")
check(sp.solve(sp.simplify(drift(sp.exp(c*t)*sp.cos(2*x)) / (sp.exp(c*t)*sp.cos(2*x))), c) == [2], "l13.quiz1 c = 2")
check(sp.simplify(3*t**2 - (6*t*t - 3*t**2)) == 0, "l13.s3/quiz2 E[W^4] = 6t*t - 3t^2 = 3t^2")
# s6: tW_t - int W ds equals int s dW (no drift); check on simulated paths
n, T, P = 400, 1.5, 20000
dW = rng.standard_normal((P, n)) * math.sqrt(T / n)
W = np.cumsum(dW, axis=1)
tt = np.arange(1, n + 1) * T / n
Wprev = np.hstack([np.zeros((P, 1)), W[:, :-1]])
M = T * W[:, -1] - (Wprev * (T / n)).sum(axis=1)
I = ((tt - T / n) * dW).sum(axis=1)  # left-point sum of s dW
check(np.max(np.abs(M - I - (T / n) * W[:, -1])) < 1e-9, "l13.s6 tW - int W ds = int s dW pathwise (discrete identity)")
h = n // 2
Mh = tt[h - 1] * W[:, h - 1] - (Wprev[:, :h] * (T / n)).sum(axis=1)
slope = np.mean((M - Mh) * W[:, h - 1])
check(abs(slope) < 4 * np.std((M - Mh) * W[:, h - 1]) / math.sqrt(P), "l13.s6 increment of tW - int W ds uncorrelated with the past")
N_inc = (T * W[:, -1] - T**2 / 2) - (tt[h - 1] * W[:, h - 1] - tt[h - 1]**2 / 2)
check(abs(N_inc.mean()) > 0.5, "l13.s6 wrong option tW - t^2/2 has a moving mean")
# s8 stated outputs
mm = env13["martingale_mean"]
r = mm(lambda t_, x_: np.exp(x_ - t_ / 2), 2.0, 100000, 4)
check(close(round(r[0], 4), 0.9955) and close(round(r[1], 4), 0.0074), "l13.s8 feedback 0.9955 (se 0.0074)")
r = mm(lambda t_, x_: np.exp(x_), 2.0, 100000, 4)
check(abs(r[0] - math.e) < 3 * r[1], "l13.s8 e^W at T=2 has mean about 2.7")
idr = env13["ito_drift"]
errs = [abs(idr(lambda t_, x_: x_**3, 1.0, 2.0) - 6), abs(idr(lambda t_, x_: x_**2 + t_, 1.0, 0.7) - 2),
        abs(idr(lambda t_, x_: x_**4 - 6*t_*x_**2 + 3*t_**2, 2.0, -1.1))]
check(max(errs) < 5e-6, f"l13.s8 central differences accurate to about 1e-7 here (max error {max(errs):.1e})")
check(close(math.exp(1), 2.7183, 5e-5) and close(math.exp(2), 7.3891, 5e-5) and close(math.exp(-1), 0.3679, 5e-5), "l13.s9 e, e^2, 1/e")

# optional stopping: "a finite mean time" is not enough for a general martingale.
# M_t = exp(2W_t - 2t), tau = first time W_t = t - 1. E[tau] = 1 (finite) yet E[M_tau] = e^-2.
dt, P = 2e-3, 20000
xw = np.zeros(P); tau = np.full(P, np.nan); alive = np.ones(P, bool); k = 0
while alive.any() and k < 40000:
    k += 1
    idx = np.flatnonzero(alive)
    xw[idx] += math.sqrt(dt) * rng.standard_normal(idx.size)
    hit = xw[idx] <= k * dt - 1
    tau[idx[hit]] = k * dt
    alive[idx[hit]] = False
done = ~np.isnan(tau)
Mtau = np.where(done, np.exp(2 * (np.where(done, tau, 0) - 1) - 2 * np.where(done, tau, 0)), 0.0)
check(done.mean() > 0.999 and abs(np.nanmean(tau) - 1) < 0.1, f"l14.s1/hw.x1 line-hitting time has finite mean (about {np.nanmean(tau):.2f})")
# Was EXPECTED_FAIL: the content said optional stopping needs "a bounded stopped value or a finite mean time".
# The content now says: a bounded stopped process with tau finite; for W and W^2 - t a finite E[tau] is enough.
# Here M_tau = e^-2 is bounded and E[tau] = 1, yet E[M_tau] != M_0 = 1, while Wald's two identities hold for W.
Wtau, ttau = xw[done], tau[done]
check(abs(Mtau.mean() - 1) > 0.5 and abs(Mtau.mean() - math.exp(-2)) < 0.02
      and abs(Wtau.mean()) < 0.03 and abs((Wtau**2).mean() - ttau.mean()) < 0.08,
      f"l14.s1.x1 / hw.h-stopping.x1: finite mean time fails for exp(2W - 2t) but holds for W and W^2 - t "
      f"(E[W_tau] = {Wtau.mean():.3f}, E[W_tau^2] - E[tau] = {(Wtau**2).mean() - ttau.mean():.3f}) (corrected claim, fix pass)")
check(abs(Mtau.mean() - math.exp(-2)) < 0.02, f"exponential martingale stopped at a finite-mean time has mean e^-2 ({Mtau.mean():.4f})")

# ------------------------------------------------------------------ lesson 14
A, B = sp.symbols("a b", positive=True)
k = 2 * mu / sig**2
Pd = (1 - sp.exp(k*B)) / (sp.exp(-k*A) - sp.exp(k*B))
u = sp.Function("u")
scale = lambda y: sp.exp(-k*y)
Px = (scale(x) - scale(-B)) / (scale(A) - scale(-B))  # chance of a first, from x
check(sp.simplify(sig**2/2*sp.diff(Px, x, 2) + mu*sp.diff(Px, x)) == 0 and sp.simplify(Px.subs(x, A)) == 1
      and sp.simplify(Px.subs(x, -B)) == 0 and sp.simplify(Px.subs(x, 0) - Pd) == 0,
      "l14.s4 P solves (sigma^2/2)u'' + mu u' = 0 with u(a)=1, u(-b)=0")
Ex = ((A + B) * Px - (x + B)) / mu  # E[tau] from x by Wald
check(sp.simplify(sig**2/2*sp.diff(Ex, x, 2) + mu*sp.diff(Ex, x) + 1) == 0 and sp.simplify(Ex.subs(x, A)) == 0
      and sp.simplify(Ex.subs(x, -B)) == 0, "l14.s5 Wald E[tau] solves (sigma^2/2)u'' + mu u' = -1 with zero boundary")
P1 = Pd.subs(sig, 1)
check(sp.simplify(sp.limit(P1, mu, 0) - B/(A + B)) == 0, "l14.s4 P tends to b/(a+b) as mu -> 0")
check(sp.simplify(sp.limit(sp.diff(P1, mu), mu, 0) - A*B/(A + B)) == 0, "l14.s4 slope at mu = 0 is ab/(a+b)")
check(sp.simplify(sp.limit(Ex.subs({x: 0, sig: 1}), mu, 0) - A*B) == 0, "l14.s1 E[tau] -> ab as mu -> 0")
hp, et = env14["hit_prob"], env14["exit_time"]
check(close(hp(1, 2, -0.5), 0.3348), "l14.s4 flipped-drift value 0.3348")
check(close(hp(1, 1, 0.5), 0.7311) and close(et(1, 1, 0.5), 0.9242) and close(hp(1, 1, 0.5), 1/(1 + math.exp(-1))), "l14.s5 P 0.7311, E 0.9242")
check(close(hp(1, 2, 0.5), 0.9100) and close(et(1, 2, 0.5), 1.4598), "l14.s7 P 0.9100, E 1.4598")
check(close(hp(2, 1.5, 0.05), 0.4717) and close(2*hp(2, 1.5, 0.05) - 1.5*(1 - hp(2, 1.5, 0.05)), 0.1509), "l14.s9 P 0.4717, profit 0.1509")
check(abs(0.05 * math.sqrt(252) - 0.8) < 0.01, "l14.s9 Sharpe near 0.8 a year (252 days)")
check(close(math.exp(-0.25), 0.7788) and close(math.exp(-1), 0.3679) and close(math.exp(-0.5), 0.6065), "l14.quiz2 values")
check(sp.limit(Pd.subs({mu: -sp.Rational(1, 2), sig: 2, A: 1}), B, sp.oo) == sp.exp(-sp.Rational(1, 4)), "l14.quiz2 b -> infinity gives e^{-2|mu|a/sigma^2}")
check(close(hp(1.5, 2.5, 0.2, 0.7), 0.9046) and close(et(1.5, 2.5, 0.2, 0.7), 5.5924) and close(hp(1.5, 2.5, 0.2, 1.0), 0.7920), "hw.h-exit-drift 0.9046, 5.5924, 0.7920")
check(close(math.exp(-0.4), 0.6703) and close(math.exp(-0.9), 0.4066) and close(math.exp(-0.6), 0.5488), "review.r-ever values")
# one barrier: P(tau > t) = 2 Phi(a/sqrt t) - 1, whose integral diverges like sqrt T
surv = lambda T_: integrate.quad(lambda v: 2*norm.cdf(1/math.sqrt(v)) - 1, 0, T_, limit=200)[0]
check(surv(1e6) / surv(1e4) > 9.5, "l14.s3 one barrier: E[min(tau, T)] grows like sqrt T, so E[tau] is infinite")
check(2*norm.cdf(1/math.sqrt(1e12)) - 1 < 1e-5, "l14.s3 one barrier is reached with probability 1 (driftless)")


def exit_sim(a_, b_, mu_, sg, dt_, paths):
    xx = np.zeros(paths); alive = np.ones(paths, bool); tau_ = np.zeros(paths); up = np.zeros(paths, bool); kk = 0
    while alive.any():
        kk += 1
        idx = np.flatnonzero(alive)
        xx[idx] += mu_*dt_ + sg*math.sqrt(dt_)*rng.standard_normal(idx.size)
        hu = xx[idx] >= a_; hd = xx[idx] <= -b_
        d = idx[hu | hd]; tau_[d] = kk*dt_; up[idx[hu]] = True; alive[d] = False
    return up.mean(), tau_.mean(), math.sqrt(up.mean()*(1 - up.mean())/paths), tau_.std(ddof=1)/math.sqrt(paths)


ps, es, sp_, se_ = exit_sim(1, 1, 0.5, 1.0, 0.001, 40000)
gap = es - et(1, 1, 0.5)
check(abs(gap - 0.03) < 3*se_ + 0.005 and gap > 3*se_, f"l14.s8 long-run E[tau] gap about 0.03 at dt=0.001 (got {gap:.4f}, se {se_:.4f})")
sh = 0.5826*math.sqrt(0.001)
check(abs(et(1 + sh, 1 + sh, 0.5) - et(1, 1, 0.5) - gap) < 3*se_ + 0.003, "l14.s8/hw barrier shift 0.5826 sigma sqrt(dt) explains the gap")
r = env14["hit_sim"](1, 1, 0.5, 1.0, 0.001, 5000, 1)
check(close(r[1] - 0.9242, 0.0212, 2e-4) and abs((r[1] - 0.9242) - 0.03) < r[3], "l14.s8 seed-1 gap 0.021 is within one standard error of 0.03")
ps, es, sp_, se_ = exit_sim(1.5, 1, 0.3, 1.0, 0.01, 150000)
check(abs((ps - hp(1.5, 1, 0.3)) - 0.012) < 3*sp_ + 0.002, f"hw.h-exit-report chance gap about +0.012 at dt=0.01 (got {ps - hp(1.5, 1, 0.3):.4f}, se {sp_:.4f})")
check(es - et(1.5, 1, 0.3) > 5*se_, "hw.h-exit-report simulated exit is late (bias, one sign)")
ps, es, sp_, se_ = exit_sim(1, 2, 0.0, 0.1, 1.0, 20000)
check(abs(ps - 2/3) < 0.03, f"l14.s0 share reaching +1 before -2 is about 2/3 with step 0.1 ({ps:.3f})")

# ------------------------------------------------------------------ lesson 15
check(Ez(z**4) == 3 and Ez(z**6) == 15 and Ez(z**8) == 105, "l15.s0 E[Z^4]=3, E[Z^6]=15, E[Z^8]=105")
ser = sp.series(sp.exp(s**2/2), s, 0, 8).removeO()
check([ser.coeff(s, j) for j in (2, 4, 6)] == [sp.Rational(1, 2), sp.Rational(1, 8), sp.Rational(1, 48)], "l15.s0 series coefficients 1/2, 1/8, 1/48")
z1, z2 = sp.symbols("z1 z2")


def E2(expr):
    """E over independent standard normals z1, z2."""
    e = sp.expand(expr); tot = 0
    for term in sp.Add.make_args(e):
        cf, mon = term.as_independent(z1, z2)
        p1, p2 = sp.degree(mon, z1), sp.degree(mon, z2)
        m = lambda p: 0 if p % 2 else sp.factorial2(p - 1) if p else 1
        tot += cf * m(p1) * m(p2)
    return sp.simplify(tot)


S_, T_ = sp.symbols("s t", positive=True)
Ws = lambda ss: sp.sqrt(ss)*z1
Wt = lambda ss, ts: sp.sqrt(ss)*z1 + sp.sqrt(ts - ss)*z2
check(E2(Ws(1)**2 * Wt(1, 2)**2) == 4, "l15.s1 E[W_1^2 W_2^2] = 4")
check(sp.simplify(E2(Ws(S_)**2 * Wt(S_, T_)**2) - (2*S_**2 + S_*T_)) == 0, "l15.s6 E[W_s^2 W_t^2] = 2s^2 + st")
check(E2(Ws(1) * Wt(1, 2)**3) == 6, "l15.s5 E[W_1 W_2^3] = 6")
check(E2((Ws(2) + Wt(2, 3))**2) == 9 and E2((Ws(1) + Wt(1, 2))**2) == 5 and E2(Ws(2)*Wt(2, 5)) == 2, "l15.s4/s8 Var(W2+W3)=9, Var(W1+W2)=5, E[W2W5]=2")
check(E2(Ws(2)**2 * Wt(2, 3)**2) == 14 and E2(Ws(2)**4 * Wt(2, 3)**2) == 132, "review.r-s2t2 = 14, hw.h-moments = 132")
odd = {(p, q): E2(Ws(1)**p * Wt(1, 2)**q) for p in range(0, 6) for q in range(0, 6) if (p + q) % 2 == 1}
# Was EXPECTED_FAIL: l15.s5 prose said a product across two times "can still be odd in total and nonzero".
# The content now says: each power can be odd and the mean nonzero; symmetry gives zero only for an odd total power.
even_odd = {(p, q): E2(Ws(1)**p * Wt(1, 2)**q) for p in (1, 3, 5) for q in (1, 3, 5)}
check(all(v == 0 for v in odd.values()) and all(v != 0 for v in even_odd.values()),
      "l15.s5 prose: odd total power gives 0 (15 cases); each power odd, total even, is nonzero (9 cases) (corrected claim, fix pass)")
check(all(v == 0 for v in odd.values()), "every two-time moment of odd total power is 0 (15 cases, e.g. E[W_1 W_2^2])")
check(E2(Ws(1) * Wt(1, 2)**2) == 0 and E2(Ws(1)**2 * Wt(1, 2)) == 0,
      "l15.s5 explain is too narrow: symmetry also kills E[W_1 W_2^2] and E[W_1^2 W_2], not only single odd powers")
u1, u2, TT = sp.symbols("u1 u2 T", positive=True)
varint = 2*sp.integrate(sp.integrate(u1, (u1, 0, u2)), (u2, 0, TT))  # double integral of min(u1, u2)
check(sp.simplify(varint - TT**3/3) == 0, "l15.s3 Var(int_0^T W dt) = T^3/3 from the covariance min(s,t)")
check(sp.integrate((TT - t)**2, (t, 0, TT)) == TT**3/3, "l15.s3 by parts route int (T-t)^2 dt agrees")
check(close(2.5**3/3, 5.2083) and 2.5 > math.sqrt(3) and close(2.5**2/2, 3.125), "l15.s3 5.2083, T > sqrt 3, slip 3.125")
check(sp.integrate(t, (t, 0, 1)) == sp.Rational(1, 2), "hw.h-moments Cov(W_1, int_0^1 W dt) = 1/2")
check(sp.integrate((1 + t)**2, (t, 0, 1)) == sp.Rational(7, 3) and sp.integrate(t**2, (t, 0, 2)) == sp.Rational(8, 3), "l15.s2/s8 isometry 8/3 and 7/3")
# random integrand: Var(int_0^2 W dW) = 2 = Var((W_2^2 - 2)/2)
check(sp.Rational(1, 4)*(Ez((sp.sqrt(2)*z)**4) - 4) == 2, "l15.quiz3 Var(int_0^2 W dW) = 2 via (W^2 - t)/2")
n, P = 400, 40000
dW = rng.standard_normal((P, n))*math.sqrt(2/n); W = np.cumsum(dW, axis=1)
Wprev = np.hstack([np.zeros((P, 1)), W[:, :-1]])
v = (Wprev*dW).sum(axis=1).var(ddof=1)
check(abs(v - 2) < 0.1, f"l15.quiz3 simulated Var(int W dW) about 2 ({v:.3f})")
v = (W*(2/n)).sum(axis=1).var(ddof=1)
check(abs(v - 8/3) < 0.12, f"l15.s3 simulated Var(int_0^2 W dt) about 8/3 ({v:.3f}), not T^2/2 = 2")
r = env15["mc_moment"](4, 2.0, 200000, 5)
check(close(round(r[0], 4), 12.0189) and close(round(r[1], 4), 0.0876) and abs(r[0] - 12) < 3*r[1], "l15.s7 seed-5 moment 12.0189 (se 0.0876), within 3 se")

# ------------------------------------------------------------------ lesson 16


def bs(S, K, r_, sg, T):
    d1 = (math.log(S/K) + (r_ + sg**2/2)*T)/(sg*math.sqrt(T)); d2 = d1 - sg*math.sqrt(T)
    call = S*norm.cdf(d1) - K*math.exp(-r_*T)*norm.cdf(d2)
    return dict(d1=d1, d2=d2, call=call, put=call - S + K*math.exp(-r_*T), dig=math.exp(-r_*T)*norm.cdf(d2))


def q_price(payoff, S, r_, sg, T):
    f = lambda zz: payoff(S*math.exp((r_ - sg**2/2)*T + sg*math.sqrt(T)*zz))*norm.pdf(zz)
    return math.exp(-r_*T)*integrate.quad(f, -12, 12, limit=400, points=[0])[0]


m = bs(100, 100, 0.05, 0.2, 1)
check(close(m["d2"], 0.15) and close(norm.cdf(0.15), 0.559618, 1e-6) and close(m["dig"], 0.5323), "l16.s0 d2 = 0.15, Q-chance 0.5596, digital 0.5323")
check(close(q_price(lambda v: float(v > 100), 100, 0.05, 0.2, 1), 0.5323, 1e-4), "l16.s0 digital call = discounted Q-probability (quadrature)")
check(close(math.exp(-0.05)*norm.cdf((0.12 - 0.02)/0.2), 0.6577), "l16.s0 real-drift slip 0.6577")
check(close(100 - 100*math.exp(-0.05), 4.8771) and close(100*math.exp(0.05), 105.1271), "l16.s1 forward value 4.8771, forward price 105.1271")
check(close(q_price(lambda v: v - 100, 100, 0.05, 0.2, 1), 4.8771, 1e-4) and close(q_price(lambda v: v - 100, 100, 0.05, 0.45, 1), 4.8771, 1e-4), "l16.s1 forward value is free of sigma")
check(close(math.exp(-0.05)*norm.cdf(-0.15), 0.4189) and close(0.5323 + 0.4189, 0.9512, 1.1e-4), "l16.s2 digital put 0.4189; pair sums to the bond")
for nn in (2, 3, 0.5):
    cf = 100**nn*math.exp(-0.05 + nn*(0.05 - 0.02) + nn*nn*0.04/2)
    check(abs(q_price(lambda v: v**nn, 100, 0.05, 0.2, 1)/cf - 1) < 1e-6, f"l16.s3/s7 power formula matches quadrature, n = {nn}")
check(close(6400*math.exp(0.15375), 7463.68, 0.006) and close(6400*math.exp(0.06), 6795.75, 0.006) and close(6400*math.exp(0.21375), 7925.20, 0.006) and close(math.exp(0.09375), 1.0983), "l16.s4 7,463.68, 6,795.75, 7,925.20, 1.0983")
check(close(100*norm.cdf(m["d1"]), 63.6831) and close(100*m["dig"], 53.2325) and close(m["call"], 10.4506), "l16.s5 asset-or-nothing 63.6831, digitals 53.2325, call 10.4506")
check(close(q_price(lambda v: v*(v > 100), 100, 0.05, 0.2, 1), 63.6831, 2e-4), "l16.s5 asset-or-nothing call is S Phi(d1) (quadrature)")
check(close(1 - math.exp(-0.05), 0.0488) and close(1000*(1 - math.exp(-0.05)), 48.77, 0.006), "l16.s9 miss 0.0488, 48.77 per 1,000")
# Was EXPECTED_FAIL: l16.s9 feedback said "the junior forgot to discount the put" (that would be 0.4404, not 0.4677).
# The content now says the junior took the put as 1 less the call, not e^{-rT} less the call.
dcall = math.exp(-0.05)*norm.cdf(0.15)
check(close(dcall, 0.5323) and close(1 - dcall, 0.4677) and close(math.exp(-0.05) - dcall, 0.4189)
      and not close(norm.cdf(-0.15), 0.4677, 5e-4),
      "l16.s9 feedback: junior's put 0.4677 = 1 - call, the right put e^{-rT} - call = 0.4189 (corrected claim, fix pass)")
check(close(100*math.exp(0.1), 110.5171) and close(math.exp(-0.05)*(math.log(100) + 0.03), 4.4091) and close(math.exp(-0.05)*math.log(100), 4.3806), "l16.quiz0/quiz1 values")
check(close(q_price(math.log, 100, 0.05, 0.2, 1), 4.4091, 1e-4), "l16.quiz1 log payoff by quadrature")
check(close(1e6*math.exp(0.22), 1246076.73, 0.006) and close(1e6*math.exp(0.10), 1105170.92, 0.006) and close(1e6*math.exp(0.27), 1309964.45, 0.006), "l16.quiz3 cube values")
r = env16["mc_price"](lambda v: v**2, 100, 0.05, 0.2, 1, 1000000, 16)
zsc = (r[0] - env16["power_price"](100, 0.05, 0.2, 1, 2))/r[1]
check(close(round(r[0], 2), 10948.77, 0.006) and close(round(r[1], 2), 4.56, 0.006), "l16.s8 seed-16 price 10,948.77, se 4.56")
# Was EXPECTED_FAIL: l16.s8 feedback said "within 1.5 standard errors"; the gap is 1.54.
# The content now says "about 1.5 standard errors away".
check(1.45 <= abs(zsc) < 1.55 and close((10948.77 - 10941.74)/4.56, 1.5417, 1e-4),
      f"l16.s8 feedback: simulation about 1.5 standard errors away (z = {zsc:.3f}) (corrected claim, fix pass)")
# quiz q-sigma explain: "Every nonlinear payoff does" (depend on sigma). Counter-example at one spot:
F = 100*math.exp(0.05)
odd_pay = lambda v: math.sqrt(v/F)*math.log(v/F)
prices = [q_price(odd_pay, 100, 0.05, sg, 1) for sg in (0.1, 0.2, 0.4, 0.8)]
# Was EXPECTED_FAIL: the explain said "Every nonlinear payoff does"; it now names the three: the digital, the square, the call.
sgs = (0.1, 0.2, 0.4, 0.8)
three = [[q_price(pf, 100, 0.05, sg, 1) for sg in sgs]
         for pf in (lambda v: float(v > 100), lambda v: v**2, lambda v: max(v - 100, 0.0))]
check(all(max(ps) - min(ps) > 1e-3 for ps in three) and max(abs(p) for p in prices) < 1e-8,
      "l16.quiz2 explain: digital, square and call prices move with sigma; not every nonlinear payoff does (corrected claim, fix pass)")
check(max(abs(p) for p in prices) < 1e-8, "payoff sqrt(S/F) ln(S/F) has price 0 at this spot for sigma = 0.1 to 0.8")
# review r-dig110
d = bs(60, 64, 0.04, 0.3, 2)
check(close(d["d2"], -0.1757) and close(norm.cdf(d["d2"]), 0.4303) and close(d["dig"], 0.3972) and close(d["d1"], 0.2486) and close(math.exp(-0.08)*norm.cdf(d["d1"]), 0.5522), "review.r-dig110 values")
e2 = bs(100, 102, 0.05, 0.2, 1)
# Was EXPECTED_FAIL: the explain said a strike above today's price makes finishing above it less likely than a coin flip.
# The content now compares the strike 64 with the Q-median S_0 e^{(r - sigma^2/2)T} = 59.40.
qmed = 60*math.exp((0.04 - 0.3**2/2)*2)
check(norm.cdf(e2["d2"]) > 0.5 and close(qmed, 59.40, 0.005) and close(60*math.exp(-0.01), qmed, 1e-9)
      and 64 > qmed and norm.cdf(d["d2"]) < 0.5,
      f"review.r-dig110 explain: K above the Q-median 59.40 gives Q(S_T > K) below one half; K=102 > S_0 still gives {norm.cdf(e2['d2']):.4f} (corrected claim, fix pass)")
check(60*math.exp((0.04 - 0.045)*2) < 64 < 60*math.exp(0.08), "review.r-dig110: strike 64 is above the Q-median 59.40 and below the forward 65.00")
check(close(10*math.exp(-0.0625), 9.3941) and close(10*math.exp(-0.04), 9.6079) and close(10*math.exp(0.0175), 10.1765) and close(q_price(math.sqrt, 100, 0.04, 0.3, 2), 9.3941, 1e-4), "review.r-sqrt values and quadrature")
qp = envh2["quick_prices"]
check(close(qp(40, 38, 0.02, 0.15, 0.25)[1] + qp(40, 38, 0.02, 0.15, 0.25)[2], math.exp(-0.005), 1e-12) and close(math.exp(-0.005), 0.9950), "hw.h-quick-prices pair sums to 0.9950")

# ------------------------------------------------------------------ lesson 17
terms = env17["pde_terms"](100, 100, 0.05, 0.2, 1)
check(close(terms[0], -6.4140) and close(terms[1], 3.1842) and close(terms[2], 3.7524) and close(terms[3], 0.5225) and abs(terms[4]) < 1e-10, "l17.s6 four terms and zero residual")
check(close(0.05*100*math.exp(-0.05)*norm.cdf(0.15), 2.6616) and close(norm.pdf(0.35), 0.375240, 1e-6) and close(norm.pdf(0.35)/(100*0.2), 0.018762, 1e-6) and close(norm.cdf(0.35), 0.6368), "l17.s6 given values 2.6616, 0.375240, 0.018762, 0.6368")
check(close(-6.4140 + 3.1842 + 3.7524 - 0.5225, 0.0001, 1e-9), "l17.s6 rounded terms sum to 0.0001")
check(close(terms[2], -terms[0] - 2.6616, 1e-4), "l17.s6 explain: gamma term = theta cost less interest 2.6616")
# symbolic: BS call solves the PDE; forward solves it; forward also solves the flawed equation without gamma
S, K, r_, sg, tau = sp.symbols("S K r sigma tau", positive=True)
Phi = lambda y: (1 + sp.erf(y/sp.sqrt(2)))/2
d1 = (sp.log(S/K) + (r_ + sg**2/2)*tau)/(sg*sp.sqrt(tau)); d2 = d1 - sg*sp.sqrt(tau)
Vc = S*Phi(d1) - K*sp.exp(-r_*tau)*Phi(d2)
resid = lambda V: -sp.diff(V, tau) + r_*S*sp.diff(V, S) + sg**2*S**2/2*sp.diff(V, S, 2) - r_*V
num = sp.lambdify((S, K, r_, sg, tau), resid(Vc))
check(max(abs(num(*p)) for p in [(100, 100, .05, .2, 1), (120, 105, .04, .3, .5), (80, 90, .03, .25, 2), (55, 70, .01, .6, 3)]) < 1e-10, "l17 Black-Scholes call satisfies the equation (symbolic derivatives, four markets)")
Vp = Vc - S + K*sp.exp(-r_*tau)
nump = sp.lambdify((S, K, r_, sg, tau), resid(Vp))
check(abs(nump(100, 110, .05, .2, 1)) < 1e-10, "l17.s9 the put satisfies the same equation")
Vf = S - K*sp.exp(-r_*tau)
check(sp.simplify(resid(Vf)) == 0, "l17.s7 forward satisfies the equation")
flawed = lambda V: -sp.diff(V, tau) + r_*S*sp.diff(V, S) - r_*V
check(sp.simplify(flawed(Vf)) == 0, "l17.s0: forward also satisfies the candidate's flawed equation, so the forward check cannot catch the dropped gamma term")
check(abs(sp.lambdify((S, K, r_, sg, tau), flawed(Vc))(100, 100, .05, .2, 1)) > 3, "l17.s0: the call does not satisfy the flawed equation (residual -3.75)")
check(close(-0.03*90*math.exp(-0.015), -2.6598) and close(80 - 90*math.exp(-0.015), -8.6601) and close(-0.03*(80 - 90*math.exp(-0.015)), 0.2598), "l17.s7 V_t -2.6598, V -8.6601, -rV 0.2598")
check(close(0.04*8 - 0.04*80*0.5 - 0.5*0.0625*6400*0.01, -3.28), "l17.quiz0 V_t = -3.28")
p = bs(100, 110, 0.05, 0.2, 1)
gam = norm.pdf(p["d1"])/(100*0.2); dlt = norm.cdf(p["d1"]) - 1
th = 0.05*p["put"] - 0.05*100*dlt - 0.5*0.04*1e4*gam
th_cf = -100*norm.pdf(p["d1"])*0.2/2 + 0.05*110*math.exp(-0.05)*norm.cdf(-p["d2"])
check(close(p["put"], 10.6753) and close(dlt, -0.5504) and close(gam, 0.019788, 1e-6) and close(th, -0.6721) and close(th_cf, -0.6721), "l17.quiz1 put values and theta -0.6721 (equation and closed form)")
check(close(0.5338 - 3.9576, -3.4238, 1e-4) and close(0.5*0.09*1e4*0.0125, 5.625) and close(0.5*0.3*1e4*0.0125, 18.75), "l17.quiz1/quiz3 slips")
# local volatility: the hedge argument gives the same equation with sigma(t,S) inside (symbolic residual of the book)
tt_, Sx, D = sp.symbols("t S Delta")
V = sp.Function("V")(tt_, Sx); sgf = sp.Function("sigma")(tt_, Sx); mut = sp.Symbol("mu_t")
dV_dt = sp.diff(V, tt_) + mut*Sx*sp.diff(V, Sx) + sgf**2*Sx**2/2*sp.diff(V, Sx, 2)
book_dt = (-dV_dt + D*mut*Sx).subs(D, sp.diff(V, Sx))
book_dW = (-sgf*Sx*sp.diff(V, Sx) + D*sgf*Sx).subs(D, sp.diff(V, Sx))
check(sp.simplify(book_dW) == 0 and not sp.simplify(book_dt).has(mut), "l17.s4/s5/hw: at Delta = V_S the dW term and mu_t cancel, also for sigma(t, S) and a path-dependent mu_t")
pde = sp.simplify(book_dt - r_*(-V + Sx*sp.diff(V, Sx)))
target = -(sp.diff(V, tt_) + r_*Sx*sp.diff(V, Sx) + sgf**2*Sx**2/2*sp.diff(V, Sx, 2) - r_*V)
check(sp.simplify(pde - target) == 0, "l17.s1 d(book) = r book dt is the Black-Scholes equation")
check(sp.simplify(sp.diff(sp.exp(-r_*(TT - t)), t) - r_*sp.exp(-r_*(TT - t))) == 0, "hw.h-aloud bond check V_t = rV")
# homework hermite
check(sp.expand(drift(x**5 + a*t*x**3 + b*t**2*x) - ((a + 10)*x**3 + (3*a + 2*b)*t*x)) == 0, "hw.h-hermite drift (a+10)W^3 + (3a+2b)tW")
check(drift(x**5 - 10*t*x**3 + 15*t**2*x) == 0 and drift(x**5 - 10*t*x**3).subs({t: 1, x: 1}) == -30, "hw.h-hermite a=-10, b=15; drift -30 without the last term")
check(drift(x**3 + t*x).subs(x, sp.Rational(3, 2)) == 6 and sp.solve(c + sp.Rational(9, 8), c) == [-sp.Rational(9, 8)], "review.r-drift 6, r-expconst -1.125")
check(3*1/0.25 == 12 and sp.integrate((3 - t)**2, (t, 0, 3)) == 9, "review.r-exit-sigma 12 days, r-timeavg 9")

print()
print(f"{len(expected)} EXPECTED_FAIL (content findings):")
for e in expected:
    print("  -", e)
print(f"{len(failures)} unexpected failures")
for f in failures:
    print("  -", f)
sys.exit(1 if failures else 0)
