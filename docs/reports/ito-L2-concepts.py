"""Concept checks for ito level 2 (lessons l5 to l8, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/ito-L2-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-ito-1-3-ledger.md).
"""
import math
import numpy as np
from scipy.stats import norm, kurtosis, skew

rng = np.random.default_rng(20261107)
failures = []


def check(cond, name):
    if cond:
        print("ok   ", name)
    else:
        print("FAIL ", name)
        failures.append(name)


def cond_regress(diff, ws, tol=None):
    """Regress diff on 1, ws, ws^2: every coefficient within 4.5 standard errors of 0
    means E[diff | W_s] = 0 is not rejected (a martingale); a large t-statistic rejects it."""
    A = np.vstack([np.ones_like(ws), ws, ws ** 2]).T
    c, *_ = np.linalg.lstsq(A, diff, rcond=None)
    resid = diff - A @ c
    cov = np.linalg.inv(A.T @ A) * (resid @ resid) / (len(diff) - 3)
    tstat = np.abs(c) / np.sqrt(np.diag(cov))
    return bool(np.all(tstat < 4.5))


# ---------------------------------------------------------------- l5: sums on the reference path
Wref = np.concatenate([[0.0], np.cumsum(np.random.default_rng(3).standard_normal(4096) * math.sqrt(1 / 4096))])
d = np.diff(Wref)
left = float(np.sum(Wref[:-1] * d)); mid = float(np.sum((Wref[:-1] + Wref[1:]) / 2 * d)); right = float(np.sum(Wref[1:] * d))
check(abs(left + 0.355507) < 1e-6 and abs(mid - 0.146693) < 1e-6 and abs(right - 0.648893) < 1e-6, "reference_path_sums: left, mid, right (l5 screens[1], [2])")
check(abs(mid - Wref[-1] ** 2 / 2) < 1e-12, "reference_path_sums: midpoint sum = W_1^2 / 2 exactly (l5 screens[2].explain)")
check(abs((right - left) - np.sum(d ** 2)) < 1e-12 and abs(right - left - 1.0044) < 1e-4, "reference_path_sums: right - left = QV = 1.0044 (l5 screens[1])")
check(abs(mid - (left + right) / 2) < 1e-12, "reference_path_sums: midpoint halfway between left and right (l5 screens[1])")
check(abs((mid - left) - np.sum(d ** 2) / 2) < 1e-12 and abs(mid - left - 0.5022) < 5e-5, "reference_path_sums: mid - left = QV/2 = 0.5022 (l5 screens[10], homework-2 items[0])")
W4 = Wref[::1024]
check(abs(float(np.sum(W4[:-1] * np.diff(W4))) + 0.185297) < 1e-6, "reference_path_sums: four-step left sum -0.1853 (l5 screens[0])")
check(abs(0.5 * (Wref[-1] ** 2 - 1) + 0.3533) < 5e-4 and abs(left - 0.5 * (Wref[-1] ** 2 - np.sum(d ** 2))) < 1e-12, "reference_path_sums: limit 1/2 (W_1^2 - 1) = -0.3533 and the exact identity (l5 screens[3], [4])")
check(abs(Wref[-1] ** 2 - 2 * left - 1.0044) < 1e-4, "reference_path_sums: W_1^2 - 2 int W dW = QV (l6 screens[0])")
# homework-2 coarsened grids
for n in (8, 64, 512):
    Wc = np.random.default_rng(11).standard_normal(512) * math.sqrt(1 / 512)
    Wc = np.concatenate([[0.0], np.cumsum(Wc)])[:: 512 // n]
    dc = np.diff(Wc)
    check(abs(np.sum((Wc[:-1] + Wc[1:]) / 2 * dc) - np.sum(Wc[:-1] * dc) - np.sum(dc ** 2) / 2) < 1e-12, "reference_path_sums: mid - left = QV/2 on seed 11 at n=%d (homework-2 items[0])" % n)

# ito_integral_moments
P, N = 200_000, 100
dW = rng.standard_normal((P, N)) * math.sqrt(1 / N)
W = np.hstack([np.zeros((P, 1)), np.cumsum(dW, axis=1)])
I = np.sum(W[:, :-1] * dW, axis=1)
check(abs(I.mean()) < 4 * I.std() / math.sqrt(P), "ito_integral_moments: E int W dW = 0 (l5 screens[6])")
check(abs(np.mean(I ** 2) - 0.5 * (1 - 1 / N)) < 4 * 1.9 / math.sqrt(P), "ito_integral_moments: E (int W dW)^2 = (n-1)/(2n) -> 1/2 (l5 screens[7], [9])")
check(abs(0.5 * (1 - 1 / 10) - 0.45) < 1e-12 and abs(0.5 * (1 - 1 / 100) - 0.495) < 1e-12, "ito_integral_moments: exact 0.45 at n=10, 0.495 at n=100 (l5 screens[9])")
M = W[:, -1] ** 2 / 2
check(abs(np.mean(M) - 0.5) < 0.01 and abs(np.mean(M ** 2) - 0.75) < 0.02, "ito_integral_moments: midpoint sum has mean 1/2 and second moment 3/4 (l5 screens[6], [9])")
check(abs(np.var(rng.standard_normal(1_000_000) ** 2) - 2) < 0.02, "ito_integral_moments: Var(Z^2) = 2 (l5 screens[7].explain)")
# over [0, 2]: E (int W dW)^2 = 2 ; Var(W_2^2) = 8
W2 = math.sqrt(2) * rng.standard_normal(1_000_000)
check(abs(np.var(W2 ** 2) / 4 - 2) < 0.05, "ito_integral_moments: E (int_0^2 W dW)^2 = Var(W_2^2)/4 = 2 (l5 quiz[2])")
# Var(int_0^1 W^2 dW) = 1 (fine grid, left point)
J = np.sum(W[:, :-1] ** 2 * dW, axis=1)
exact_J = sum(3 * (k / N) ** 2 / N for k in range(N))   # (N-1)(2N-1)/(2N^2) -> 1
print("    Var(int W^2 dW): sim %.4f, grid-exact %.4f, limit 1" % (np.var(J), exact_J))
check(abs(J.mean()) < 4 * J.std() / math.sqrt(P) and abs(np.var(J) - exact_J) < 0.05, "ito_integral_moments: Var(int W^2 dW) = int 3t^2 dt = 1 (homework-2 items[3])")
# l8 code: mean changes at t = 1
Z1 = rng.standard_normal(1_000_000)
check(abs(np.mean(Z1 ** 2) - 1) < 0.01 and abs(np.mean(np.exp(Z1)) - math.exp(0.5)) < 0.01 and abs(np.mean(Z1 ** 3)) < 0.02 and abs(np.mean(np.exp(Z1 - 0.5)) - 1) < 0.01,
      "ito_integral_moments: mean changes 1, e^{1/2} - 1 = 0.6487, 0, 0 (l8 screens[9])")

# wiener_integral_normal: int f dW ~ N(0, int f^2)
tgrid = (np.arange(N) + 0.5) / N
K = np.sum(tgrid * dW, axis=1)
check(abs(K.var() - 1 / 3) < 0.01 and abs(K.mean()) < 0.005 and abs(skew(K)) < 0.02 and abs(kurtosis(K)) < 0.05, "wiener_integral_normal: int t dW ~ N(0, 1/3) (l5 screens[8])")
check(abs((125 - 8) / 3 - 39) < 1e-12 and abs(sum((2 + (k + 0.5) * 3 / N) ** 2 * 3 / N for k in range(N)) - 39) < 0.01, "wiener_integral_normal: Var int_0^3 (2+t) dW = 39 (review-2 items[1])")
K2 = np.sum((0.1 + 0.2 * tgrid) * dW, axis=1)
check(abs(0.01 + 0.02 + 0.04 / 3 - 0.0433) < 5e-5 and abs(K2.var() - 0.04333) < 0.0015 and abs(math.sqrt(0.04333) - 0.2082) < 5e-5, "wiener_integral_normal: int sigma(t) dW has variance 0.0433, sd 0.2082 (l7 screens[7])")
check(abs(9 * 4 - 36) < 1e-12, "wiener_integral_normal: Var(3 W_4) = 36 (l5 quiz[3])")

# ---------------------------------------------------------------- l6: Ito drift values
def ito_drift(f_t, f_x, f_xx, a, b):
    return f_t + a * f_x + 0.5 * b ** 2 * f_xx
check(ito_drift(0, 200, 2, 8, 20) == 2000, "ito_drift_values: d(S^2) dt coefficient 2000 = (2mu + sigma^2) S^2 (l6 screens[3])")
check(abs(ito_drift(0, 0.01, -0.0001, 8, 20) - 0.06) < 1e-12, "ito_drift_values: d(ln S) drift 0.06 (l6 screens[5])")
check(ito_drift(0, 12, 12, 0, 1) == 6 and ito_drift(0, 4 * 8, 12 * 4, 0, 1) == 24, "ito_drift_values: W^3 drift 3W = 6, W^4 drift 6W^2 = 24 at W = 2 (l8 screens[2], l6 quiz[0])")
check(abs(ito_drift(0, math.exp(2), math.exp(2), 0, 1) - 3.6945) < 5e-5, "ito_drift_values: e^W drift e^2/2 = 3.6945 (l8 screens[2])")
check(ito_drift(-1, 4, 2, 0, 1) == 0 and ito_drift(-4, 4, 2, 0, 1) == -3, "ito_drift_values: W^2 - t drift 0, W^2 - 4t drift -3 (l8 screens[2], quiz[0])")
check(abs(ito_drift(-0.05 * 100, 1, 0, 0.08 * 100, 0.2 * 100) - 3) < 1e-12 and abs(ito_drift(-0.05 * 100, 1, 0, 0.12 * 100, 0.2 * 100) - 7) < 1e-12, "ito_drift_values: discounted share drift (mu - r) S = 3 and 7 (l8 screens[6], review-2 items[8])")
check(ito_drift(0, 100, 2, 2.5, 15) == 475 and 15 * 100 == 1500 and abs(ito_drift(0, 1 / 100, -1 / 100 ** 2, 5, 30) - 0.005) < 1e-12, "ito_drift_values: S^2 at 50 (475, 1500), ln S (0.005, 0.3) (homework-2 items[1])")
check(ito_drift(-9, 6, 2, 0, 1) == -8, "ito_drift_values: e^{-t} W^2 drift -8 at t = 0, W = 3 (review-2 items[2])")
check(ito_drift(3, 5, 0, 8, 20) == 3 + 5 * 8 and ito_drift(1, 4, 0, 8, 20) == 1 + 4 * 8, "ito_drift_values: linear f has no Ito term (l6 screens[8], quiz[3])")
# W^3 - 3tW, exp(theta W - theta^2 t/2) drift 0 symbolically at a few points
for w, t in ((2.0, 1.0), (-1.0, 0.3)):
    check(abs(ito_drift(-3 * w, 3 * w ** 2 - 3 * t, 6 * w, 0, 1)) < 1e-12, "ito_drift_values: W^3 - 3tW has zero drift (homework-1 items[3])")
    th = 2.0
    f = math.exp(th * w - th ** 2 * t / 2)
    check(abs(ito_drift(-th ** 2 / 2 * f, th * f, th ** 2 * f, 0, 1)) < 1e-12, "ito_drift_values: exp(theta W - theta^2 t/2) has zero drift (l8 screens[3])")
    check(abs(ito_drift(-f, th * f, th ** 2 * f, 0, 1) - f) < 1e-12, "ito_drift_values: e^{2W - t} drifts at +Z (review-2 items[7])")

# gbm_power_moments: E S^p = S0^p exp((p mu + p(p-1) sigma^2 / 2) t)
S0, mu, sig = 100.0, 0.08, 0.2
def moment(p, S0, mu, sig, t):
    return S0 ** p * math.exp((p * mu + 0.5 * p * (p - 1) * sig ** 2) * t)
check(abs(moment(2, 100, 0.08, 0.2, 1) - 12214.03) < 5e-3, "gbm_power_moments: E S_1^2 = 10^4 e^{0.2} = 12,214.03 (l6 screens[4])")
check(abs(moment(2, 100, 0.08, 0.2, 1) - math.exp(2 * (math.log(100) + 0.06) + 2 * 0.04)) < 1e-6, "gbm_power_moments: lognormal check e^{2m + 2v} (l6 screens[4].explain)")
check(abs(moment(3, 100, 0.08, 0.2, 1) - 1433329) < 1, "gbm_power_moments: E S_1^3 = 1,433,329 (homework-2 items[2])")
check(abs(moment(2, 80, 0.05, 0.25, 1.5) - 8166.6) < 0.05 and abs(moment(2, 50, 0.1, 0.3, 2) - 4465.1) < 0.05, "gbm_power_moments: 8166.6 and 4465.1 (review-2 items[3], l6 quiz[2])")
ST = S0 * np.exp((mu - sig ** 2 / 2) + sig * rng.standard_normal(2_000_000))
sd_sq = math.sqrt(moment(4, 100, 0.08, 0.2, 1) - moment(2, 100, 0.08, 0.2, 1) ** 2)
check(abs(np.mean(ST ** 2) - 12214.03) < 4 * sd_sq / math.sqrt(2_000_000), "gbm_power_moments sim: E S^2 (l6 screens[4], [9])")
check(abs(sd_sq / math.sqrt(100_000) - 16.1) < 0.3, "gbm_power_moments: se of the mean of S^2 on 100,000 draws is about 16.1 (l6 screens[9])")
check(abs(np.mean(ST ** 3) - 1433329) < 4 * ST.__pow__(3).std() / math.sqrt(2_000_000), "gbm_power_moments sim: E S^3 (homework-2 items[2])")

# simple_vs_log_gap: seeded year (seed 4, 252 steps)
dt = 1 / 252
dW4 = np.random.default_rng(4).standard_normal(252) * math.sqrt(dt)
steps = (mu - sig ** 2 / 2) * dt + sig * dW4
S = 100 * np.exp(np.concatenate([[0.0], np.cumsum(steps)]))
simple = np.sum(np.diff(S) / S[:-1]); logret = math.log(S[-1] / 100)
check(abs(S[-1] - 129.683264) < 1e-6 and abs(simple - 0.27986) < 5e-5 and abs(logret - 0.25992) < 5e-5, "simple_vs_log_gap: 0.27986 against 0.25992 on the seeded year (l6 screens[7], homework-2 items[7])")
check(abs(simple - logret - 0.0199) < 5e-5 and abs(simple - logret - 0.5 * np.sum(np.diff(np.log(S)) ** 2)) < 0.001, "simple_vs_log_gap: gap 0.0199 is about half the sum of squared log steps (l6 screens[7].explain)")
check(abs(0.5 * sig ** 2 - 0.02) < 1e-12 and abs(0.5 * 0.4 ** 2 - 0.08) < 1e-12, "simple_vs_log_gap: 1/2 sigma^2 T = 0.02 and 0.08 (homework-2 items[7])")
# continuous-time identity on many paths: int dS/S - ln(S_T/S_0) -> sigma^2 T / 2
gaps = []
for s in range(200):
    dWp = rng.standard_normal(4096) * math.sqrt(1 / 4096)
    Sp = 100 * np.exp(np.concatenate([[0.0], np.cumsum((mu - sig ** 2 / 2) / 4096 + sig * dWp)]))
    gaps.append(np.sum(np.diff(Sp) / Sp[:-1]) - math.log(Sp[-1] / 100))
gaps = np.array(gaps)
check(abs(gaps.mean() - 0.02) < 0.001 and gaps.std() < 0.002, "simple_vs_log_gap: the gap is 0.02 on every fine path, not noise (l6 screens[7].options[2].why)")

# atm_call_gamma
S_, K_, r_, T_ = 100.0, 100.0, 0.05, 1.0
d1 = (math.log(S_ / K_) + (r_ + sig ** 2 / 2) * T_) / (sig * math.sqrt(T_)); d2 = d1 - sig * math.sqrt(T_)
gamma = norm.pdf(d1) / (S_ * sig * math.sqrt(T_))
check(abs(gamma - 0.018762) < 5e-7, "atm_call_gamma: Gamma = 0.018762 (l6 screens[10])")
conv = 0.5 * sig ** 2 * S_ ** 2 * gamma
check(abs(conv - 3.7524) < 5e-5 and abs(conv / 252 - 0.0149) < 5e-5, "atm_call_gamma: convexity term 3.7524 a year, 0.0149 a day (l6 screens[10])")
V = S_ * norm.cdf(d1) - K_ * math.exp(-r_ * T_) * norm.cdf(d2)
delta = norm.cdf(d1)
theta = -S_ * norm.pdf(d1) * sig / (2 * math.sqrt(T_)) - r_ * K_ * math.exp(-r_ * T_) * norm.cdf(d2)
check(abs(theta + conv + r_ * S_ * delta - r_ * V) < 1e-9, "atm_call_gamma: BS PDE theta + convexity = r (V - S delta), so gamma offsets decay net of carry (l6 screens[10].explain)")

# ---------------------------------------------------------------- l7: seeded year and Euler
W1 = float(np.sum(dW4))
check(abs(W1 - 0.9996) < 5e-5 and abs(100 * math.exp(0.06 + 0.2 * W1) - 129.68) < 5e-3, "seeded_year: W_1 = 0.9996, S_1 = 129.68 (l7 screens[0])")
euler = 100 * np.cumprod(1 + mu * dt + sig * dW4)
check(abs(euler[-1] - 129.690755) < 1e-6 and abs(euler[-1] - S[-1] - 0.0075) < 5e-5, "seeded_year: Euler ends 129.690755, gap 0.0075 (l7 screens[1], [8])")
check(abs(100 * math.exp(0.08 + 0.2 * W1) - 132.30) < 5e-3 and abs(132.30 - 129.68 - 2.62) < 1e-9, "seeded_year: no-drag guess 132.30, gap 2.62 (l7 screens[1], [5])")
check(abs(100 * 1.025 ** 2 - 105.0625) < 1e-9 and abs(100 * math.exp(0.05) - 105.1271) < 5e-5, "seeded_year: sigma = 0 Euler 105.0625 vs exact 105.1271 (l7 screens[8])")
# Euler at m = 4 on the same increments
dW4m = dW4.reshape(4, 63).sum(axis=1)
e4 = 100 * np.prod(1 + mu / 4 + sig * dW4m)
check(abs(abs(e4 - S[-1]) - 0.82) < 0.01, "seeded_year: Euler gap 0.82 at m = 4 (l7 screens[1])")

# euler_strong_order: mean |Euler - exact| halves when steps quadruple
def euler_error(steps_list, seed, paths=500):
    Nn = max(steps_list)
    r_ = np.random.default_rng(seed)
    fine = r_.standard_normal((paths, Nn)) * math.sqrt(1 / Nn)
    exact = 100 * np.exp(0.06 + 0.2 * fine.sum(axis=1))
    out = []
    for m in steps_list:
        dWm = fine.reshape(paths, m, Nn // m).sum(axis=2)
        eu = 100 * np.prod(1 + 0.08 / m + 0.2 * dWm, axis=1)
        out.append(float(np.mean(np.abs(eu - exact))))
    return out
errs = euler_error([252, 1008, 4032], 1)
check(all(abs(a - b) < 1e-4 for a, b in zip(errs, [0.1533, 0.0744, 0.0391])), "euler_strong_order: seed-1 gaps 0.1533, 0.0744, 0.0391 (l7 screens[9])")
errs2 = euler_error([63, 252, 1008, 4032], 77, paths=4000)
ratios = [errs2[i] / errs2[i + 1] for i in range(3)]
check(all(1.7 < q < 2.3 for q in ratios), "euler_strong_order: four times the steps halves the error, order sqrt(dt) (l7 screens[9].explain), ratios %s" % [round(q, 2) for q in ratios])
# log of Euler recovers the drag: sum y^2 -> sigma^2 T
y = mu * dt + sig * dW4
check(abs(np.sum(np.log1p(y)) - (np.sum(y) - 0.5 * np.sum(y ** 2))) < 0.002 and abs(np.sum(y ** 2) - sig ** 2) < 0.005, "euler_strong_order: ln(1+y) ~ y - y^2/2 and sum y^2 ~ sigma^2 T (l7 screens[6])")

# gbm_probabilities
check(abs((math.log(1.3) - 0.06) / 0.2 - 1.0118) < 5e-5 and abs(1 - norm.cdf(1.0118) - 0.1558) < 5e-5, "gbm_probabilities: z = 1.0118, P(S_1 > 130) = 0.1558 (l7 screens[3], [4])")
check(abs(math.exp(0.02) - 1 - 0.0202) < 5e-5 and abs(100 * math.exp(0.08 + 0.02) - 110.52) < 5e-3, "gbm_probabilities: no-drag mean 110.52, 2.02% too high (l7 screens[5])")
check(abs(norm.cdf(-1.8) - 0.0359) < 5e-5, "gbm_probabilities: P(Euler negative) = Phi(-1.8) (l7 screens[10])")
check(abs(norm.cdf((math.log(0.8) - 0.02875) / 0.25) - 0.1568) < 5e-5, "gbm_probabilities: P(S_1 < 80) = 0.1568 (review-2 items[6])")
check(abs(math.exp(0.09) - 1 - 0.0942) < 5e-5 and abs(200 * math.exp(-0.13) - 175.62) < 5e-3 and abs(50 * math.exp(0.205) - 61.38) < 5e-3, "gbm_probabilities: 9.42%, 175.62, 61.38 (l7 quiz[3], review-2 items[5], l7 quiz[2])")
z1 = rng.standard_normal(1_000_000)
check(abs((1.08 + 0.6 * z1 < 0).mean() - 0.0359) < 4 * math.sqrt(0.0359 * 0.9641 / 1_000_000), "gbm_probabilities sim: Euler negative 3.59% (l7 screens[10])")

# ---------------------------------------------------------------- l8: martingales
# exponential_martingale
for th, t in ((0.5, 2.0), (1.0, 1.0), (2.0, 1.0), (0.3, 4.0)):
    Wt = math.sqrt(t) * rng.standard_normal(2_000_000)
    Zt = np.exp(th * Wt - th ** 2 * t / 2)
    check(abs(Zt.mean() - 1) < 4 * Zt.std() / math.sqrt(2_000_000), "exponential_martingale: E exp(theta W - theta^2 t/2) = 1 at theta=%.1f, t=%.0f (l8 screens[3], [9])" % (th, t))
Wt = math.sqrt(2) * rng.standard_normal(2_000_000)
check(abs(np.mean(np.exp(0.5 * Wt)) - math.exp(0.25)) < 0.005 and abs(math.exp(0.25) - 1.2840) < 5e-5 and abs(np.mean(np.exp(Wt)) - math.e) < 0.03, "exponential_martingale: E e^{0.5 W_2} = 1.2840, E e^{W_2} = e (l8 screens[4], quiz[2])")
# conditional check on the exponential martingale and its wrong corrections
s_, t_ = 0.6, 1.5
ws = math.sqrt(s_) * rng.standard_normal(1_000_000)
wt = ws + math.sqrt(t_ - s_) * rng.standard_normal(1_000_000)
check(cond_regress(np.exp(2 * wt - 2 * t_) - np.exp(2 * ws - 2 * s_), ws, tol=0.05), "exponential_martingale: e^{2W - 2t} is a martingale (review-2 items[7])")
check(not cond_regress(np.exp(2 * wt - t_) - np.exp(2 * ws - s_), ws, tol=0.05), "exponential_martingale: e^{2W - t} is not (review-2 items[7])")
check(not cond_regress(np.exp(wt - 2 * t_) - np.exp(ws - 2 * s_), ws, tol=0.05), "exponential_martingale: e^{W - 2t} is not (review-2 items[7])")
check(abs(sum(math.exp(2 * x) * 0.001 for x in np.arange(0, 1, 0.001)) * 1 - (math.e ** 2 - 1) / 2) < 0.01, "exponential_martingale: E int e^{2W_s - s} ds = e^t - 1 is finite (homework-2 items[8] check)")

# hermite_martingales (homework-2 items[4]) and the l8 table: exact conditional expectations with sympy.
# E[f(W_t, t) | W_s = w] = E_D[f(w + D, t)] with D ~ N(0, t - s); a martingale returns f(w, s).
import sympy as sp
w, D, s_sym, t_sym = sp.symbols("w D s t", real=True)
tau = sp.symbols("tau", positive=True)
dens = sp.exp(-D ** 2 / (2 * tau)) / sp.sqrt(2 * sp.pi * tau)
def cond_exp(f):
    val = sp.integrate(f(w + D, t_sym) * dens, (D, -sp.oo, sp.oo))
    return sp.simplify(val.subs(tau, t_sym - s_sym))
cands = [
    ("W^4 - 6tW^2 + 3t^2", lambda x, t: x ** 4 - 6 * t * x ** 2 + 3 * t ** 2, True),
    ("e^{3W - 4.5t}", lambda x, t: sp.exp(3 * x - sp.Rational(9, 2) * t), True),
    ("e^{t/2} cos W", lambda x, t: sp.exp(t / 2) * sp.cos(x), True),
    ("W^2 + t", lambda x, t: x ** 2 + t, False),
    ("e^{W - t}", lambda x, t: sp.exp(x - t), False),
    ("W^4 - 3t^2", lambda x, t: x ** 4 - 3 * t ** 2, False),
    ("W^2 - t", lambda x, t: x ** 2 - t, True),
    ("W^2", lambda x, t: x ** 2, False),
    ("W^3", lambda x, t: x ** 3, False),
    ("e^W", lambda x, t: sp.exp(x), False),
    ("W^3 - 3tW", lambda x, t: x ** 3 - 3 * t * x, True),
    ("e^{2W - 2t}", lambda x, t: sp.exp(2 * x - 2 * t), True),
    ("e^{2W - t}", lambda x, t: sp.exp(2 * x - t), False),
]
for name, f, is_m in cands:
    gap = sp.simplify(cond_exp(f) - f(w, s_sym))
    is_zero = gap == 0 or sp.simplify(gap.subs({w: sp.Rational(7, 5), s_sym: sp.Rational(3, 10), t_sym: sp.Rational(9, 4)})) == 0
    check(is_zero == is_m, "hermite_martingales: %s is %sa martingale, exact conditional gap %s (homework-2 items[4], l8 screens[2], review-2 items[7])" % (name, "" if is_m else "not ", gap))

# conditional_cube and conditional square
D = math.sqrt(0.5) * rng.standard_normal(2_000_000)
check(abs(np.mean((1 + D) ** 3) - 2.5) < 0.01, "conditional_cube: E[W_1^3 | W_.5 = 1] = 2.5 (l8 screens[5])")
D2 = math.sqrt(2) * rng.standard_normal(2_000_000)
check(abs(np.mean((2 + D2) ** 3) - 20) < 0.05 and abs(np.mean((2 + D2) ** 2) - 6) < 0.02, "conditional_cube: E[W_3^3 | W_1 = 2] = 20, E[W_3^2 | W_1 = 2] = 6 (homework-2 items[6], l8 quiz[1])")
# Markov forecast: E[W_1 | W_.5 = 0.8] = 0.8 (regression of W_1 on W_.5 has slope 1, intercept 0)
w5 = math.sqrt(0.5) * rng.standard_normal(1_000_000); w1 = w5 + math.sqrt(0.5) * rng.standard_normal(1_000_000)
A = np.vstack([np.ones_like(w5), w5]).T
c, *_ = np.linalg.lstsq(A, w1, rcond=None)
check(abs(c[0]) < 0.005 and abs(c[1] - 1) < 0.005, "conditional_cube: E[W_1 | W_.5] = W_.5 (l8 screens[0])")

# gamblers_ruin: fair +-1 walk from 0 stopped at +a or -b: P(+a) = b/(a+b)
def ruin(a, b, n=200_000):
    pos = np.zeros(n, dtype=int); alive = np.ones(n, dtype=bool); hits = np.zeros(n, dtype=bool)
    for _ in range(4000):
        if not alive.any():
            break
        step = rng.integers(0, 2, n) * 2 - 1
        pos[alive] += step[alive]
        up = alive & (pos >= a); down = alive & (pos <= -b)
        hits |= up; alive &= ~(up | down)
    assert not alive.any()
    return hits.mean()
for a, b, p in ((7, 3, 0.3), (4, 1, 0.2), (6, 2, 0.25)):
    est = ruin(a, b)
    check(abs(est - p) < 4 * math.sqrt(p * (1 - p) / 200_000), "gamblers_ruin: P(+%d before -%d) = %.2f (l8 screens[7], quiz[3], review-2 items[9])" % (a, b, p))

print()
if failures:
    print("%d check(s) failed:" % len(failures))
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("all checks passed")
