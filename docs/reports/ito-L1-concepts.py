"""Concept checks for ito level 1 (lessons l1 to l4, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/ito-L1-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-ito-1-3-ledger.md).
A check that fails because the content is wrong is marked EXPECTED_FAIL and
carries the corrected assert in a comment beside it.
"""
import math
import numpy as np
from scipy.stats import norm, t as student_t

rng = np.random.default_rng(20261106)
failures = []


def check(cond, name):
    if cond:
        print("ok   ", name)
    else:
        print("FAIL ", name)
        failures.append(name)


# ---------------------------------------------------------------- l1
# scaled_walk_var: n steps of +-1/sqrt(n) have endpoint variance 1 (exact) and in sample
for n in (4, 16, 400, 1024):
    check(abs(n * (1 / math.sqrt(n)) ** 2 - 1) < 1e-12, "scaled_walk_var exact n=%d (l1 screens[0], [2])" % n)
flips = rng.integers(0, 2, (200_000, 400)) * 2 - 1
w1 = flips.sum(axis=1) / 20.0
check(abs(w1.var(ddof=1) - 1) < 3 * math.sqrt(2 / 200_000), "scaled_walk_var sim n=400 (l1 screens[1], [8])")
# 95% of paths end within 2 of 0 (option 'same')
check(abs((np.abs(w1) < 2).mean() - 0.954) < 0.01, "scaled_walk_var: most paths within 2 of 0 (l1 screens[1]; discrete walk, continuity correction gives 0.949)")
# steps of 1/n: endpoint variance 1/n -> 0 (trap)
w_avg = flips.sum(axis=1) / 400.0
check(abs(w_avg.var() - 1 / 400) < 3 * (1 / 400) * math.sqrt(2 / 200_000) + 1e-5, "scaled_walk_var: 1/n scaling flattens (l1 screens[5])")

# scaled_walk_code: se of a sample variance of N(0,1) on 10,000 draws is about 0.014
check(abs(math.sqrt(2 / 9999) - 0.014) < 0.0005, "scaled_walk_code se 0.014 (l1 screens[8].explain)")

# biased_walk_moments: p = 1/2 + mu sqrt(dt)/2 gives step mean mu dt, variance dt(1 - mu^2 dt); n steps end at mean mu
mu, n = 1.0, 400
dt = 1 / n
p = 0.5 + 0.5 * mu * math.sqrt(dt)
step_mean = (2 * p - 1) * math.sqrt(dt)
step_var = dt - step_mean ** 2
check(abs(step_mean - mu * dt) < 1e-12 and abs(n * step_mean - mu) < 1e-12, "biased_walk_moments mean (l1 screens[6])")
check(abs(n * step_var - (1 - mu ** 2 * dt)) < 1e-12 and n * step_var > 0.99, "biased_walk_moments variance about 1 (l1 screens[6].explain)")
u = rng.random((100_000, n))
steps = np.where(u < p, 1.0, -1.0) * math.sqrt(dt)
end = steps.sum(axis=1)
check(abs(end.mean() - 1.0) < 3 * end.std() / math.sqrt(100_000), "biased_walk_moments sim mean 1 (l1 screens[6])")

# normal probabilities used in l1
check(abs((1 - norm.cdf(1)) - 0.1587) < 5e-5, "P(W_1 > 1) = 0.1587 (l1 screens[4], quiz[1])")
check(abs(2 * (1 - norm.cdf(1)) - 0.3173) < 5e-5, "two-sided 0.3173 (l1 screens[4].byKey.two)")

# var_scaling_autocorr: 10-day variance of an AR(1) daily P&L exceeds 10 sigma^2 iff phi > 0
def var_sum_ar1(phi, h=10):
    # Var(sum_{i=1}^h X_i) with unit marginal variance and rho_k = phi^k
    return h + 2 * sum((h - k) * phi ** k for k in range(1, h))
check(var_sum_ar1(0.3) > 10 and var_sum_ar1(-0.3) < 10 and abs(var_sum_ar1(0.0) - 10) < 1e-12,
      "var_scaling_autocorr: positive autocorrelation understates, negative overstates (l1 screens[9], quiz[3])")

# var_scaling_fat_tails: with iid Student t(3) daily moves, 10-day 99% quantile / (sqrt(10) * 1-day 99% quantile) != 1
daily = student_t.rvs(3, size=(400_000, 10), random_state=rng)
q1 = np.quantile(daily[:, 0], 0.99)
q10 = np.quantile(daily.sum(axis=1), 0.99)
ratio = q10 / (math.sqrt(10) * q1)
check(abs(ratio - 1) > 0.05, "var_scaling_fat_tails: sqrt(10) rule fails for t(3) tails, ratio %.3f (l1 screens[9].explain)" % ratio)
# and for normal tails it holds
daily_n = rng.standard_normal((400_000, 10))
ratio_n = np.quantile(daily_n.sum(axis=1), 0.99) / (math.sqrt(10) * np.quantile(daily_n[:, 0], 0.99))
check(abs(ratio_n - 1) < 0.03, "var_scaling_fat_tails: sqrt(10) rule holds for normal tails (l1 screens[9])")

# ---------------------------------------------------------------- l2
# cov_min: Cov(W_s, W_t) = min(s, t), Corr = sqrt(s/t); simulated on 100 steps
N, P = 100, 200_000
dW = rng.standard_normal((P, N)) * math.sqrt(1 / N)
W = np.hstack([np.zeros((P, 1)), np.cumsum(dW, axis=1)])
c = np.cov(W[:, 30], W[:, 70])[0, 1]
se = math.sqrt((0.3 * 0.7 + 0.09) / P)
check(abs(c - 0.3) < 4 * se, "cov_min: Cov(W_.3, W_.7) = 0.3 (l2 screens[2], [9])")
c2 = np.cov(W[:, 50], W[:, 100])[0, 1]
check(abs(c2 - 0.5) < 4 * math.sqrt((0.5 + 0.25) / P), "cov_min: Cov(W_.5, W_1) = 0.5 (l2 screens[9])")
r = np.corrcoef(W[:, 25], W[:, 100])[0, 1]
check(abs(r - 0.5) < 0.01, "cov_min: Corr(W_s, W_t) = sqrt(s/t) (l2 screens[1], [3])")
check(abs(math.sqrt((0.21 + 0.09) / 10_000) - 0.0055) < 1e-4, "cov_min: se 0.0055 on 10,000 paths (l2 screens[9].explain)")

# var_linear_combos
V = np.cov(np.vstack([W[:, 100], W[:, 50]]))  # scale: W_1 and W_.5 ~ (W_2, W_1) scaled by 1/2
# use exact covariance algebra instead: Var(aW_1 + bW_2 + cW_3) with Cov = min
def var_lin(coefs):
    ts = [1, 2, 3]
    return sum(a * b * min(ts[i], ts[j]) for i, a in enumerate(coefs) for j, b in enumerate(coefs))
check(abs(var_lin([2, -1, 0]) - 2) < 1e-12, "var_linear_combos: Var(2W_1 - W_2) = 2 (l2 screens[5])")
check(abs(var_lin([1, 1, 0]) - 5) < 1e-12, "var_linear_combos: Var(W_1 + W_2) = 5 (l2 quiz[1])")
check(abs(var_lin([1, 1, 1]) - 14) < 1e-12, "var_linear_combos: Var(W_1 + W_2 + W_3) = 14 (review-1 items[2])")
check(abs(4 / math.sqrt(4 * 9) - 2 / 3) < 1e-12 and abs(4 / 6 - 0.6667) < 5e-5, "Corr(W_4, W_9) = 2/3 (review-1 items[3])")
check(abs(5 / math.sqrt(50) - 0.7071) < 5e-5, "Corr(5-day, 10-day) = sqrt(0.5) (l2 screens[10])")

# difference quotient sd 1/sqrt(dt)
for d, sd in ((0.01, 10), (1e-4, 100), (1e-6, 1000)):
    check(abs(math.sqrt(d) / d - sd) < 1e-6, "sd of dW/dt = 1/sqrt(dt) at dt=%g (l2 screens[7])" % d)

# sqrt_t_Z_not_bm: X_t = sqrt(t) Z has Cov(X_1, X_2) = sqrt(2) not 1
Z = rng.standard_normal(P)
check(abs(np.cov(Z, math.sqrt(2) * Z)[0, 1] - math.sqrt(2)) < 0.02, "sqrt_t_Z_not_bm: Cov(X_1, X_2) = sqrt(2) (l2 screens[8])")

# brownian_scaling: 2W_{t/4} has Var t; W_{2t}, sqrt2 W_t have 2t; W_t + t has mean t
tt = 0.8
check(abs(4 * (tt / 4) - tt) < 1e-12 and abs(2 * tt - tt) > 0.1, "brownian_scaling (l2 quiz[3])")
X = 2 * W[:, 25]  # 2 W_{1/4}: should have variance 1
check(abs(X.var() - 1) < 4 * math.sqrt(2 / P), "brownian_scaling sim: 2W_{1/4} has variance 1 (l2 quiz[3])")

# ---------------------------------------------------------------- l3
# reference_path_qv: seed-3 path, 4096 steps
Wref = np.concatenate([[0.0], np.cumsum(np.random.default_rng(3).standard_normal(4096) * math.sqrt(1 / 4096))])
def qv(Wp, step):
    d = np.diff(Wp[::step]); return float(np.sum(d ** 2))
def tv(Wp, step):
    d = np.diff(Wp[::step]); return float(np.sum(np.abs(d)))
check(abs(qv(Wref, 1024) - 0.6640) < 5e-4, "reference_path_qv: four increments give 0.664 (l3 screens[0])")
check([round(qv(Wref, 4096 // m), 4) for m in (16, 64, 256, 1024, 4096)] == [0.5908, 0.8868, 0.9718, 1.008, 1.0044],
      "reference_path_qv: table (l3 screens[1], [2])")
check(abs(tv(Wref, 1) - 51.3601) < 1e-3 and abs(tv(Wref, 4) - 25.7785) < 1e-3, "reference_path_qv: lengths 51.36 and 25.78 (l3 screens[1], [3])")
check(abs(qv(np.linspace(0, 1, 101), 1) - 0.01) < 1e-12, "reference_path_qv: straight line 0.01 (l3 screens[2])")

# total_variation_growth: E|dW| = sqrt(2 dt / pi); m of them add to sqrt(2m/pi); 51.06 at 4096
check(abs(math.sqrt(2 * 4096 / math.pi) - 51.06) < 0.01, "total_variation_growth: sqrt(2m/pi) = 51.06 (l3 screens[3].explain)")
absmean = np.abs(rng.standard_normal(1_000_000) * math.sqrt(1 / 4096)).mean()
check(abs(absmean - math.sqrt(2 / (4096 * math.pi))) < 3 * math.sqrt(1 / 4096) * 0.6 / 1000, "total_variation_growth: E|dW| = sqrt(2dt/pi) (l3 screens[3])")
check(abs(math.sqrt(2 * 4096 / math.pi) / math.sqrt(2 * 1024 / math.pi) - 2) < 1e-12, "total_variation_growth: four times the steps doubles the length (l3 screens[3])")

# qv_moments: E (dW)^2 = dt, E (dW)^4 = 3 dt^2, Var (dW)^2 = 2 dt^2; sum has mean T, variance 2 T dt
dt = 1 / 64
sq = (rng.standard_normal(2_000_000) * math.sqrt(dt)) ** 2
check(abs(sq.mean() - dt) < 4 * math.sqrt(2) * dt / math.sqrt(2_000_000), "qv_moments: E(dW)^2 = dt (l3 screens[4])")
check(abs(sq.var() - 2 * dt ** 2) < 0.02 * 2 * dt ** 2, "qv_moments: Var(dW)^2 = 2 dt^2 (l3 screens[4])")
check(abs(np.mean(sq ** 2) - 3 * dt ** 2) < 0.02 * 3 * dt ** 2, "qv_moments: E(dW)^4 = 3 dt^2 (l3 screens[4])")
# many paths: sd of QV at m steps is sqrt(2/m) on [0, 1]
Wq = np.hstack([np.zeros((50_000, 1)), np.cumsum(rng.standard_normal((50_000, 1024)) * math.sqrt(1 / 1024), axis=1)])
for m in (16, 64, 256, 1024):
    d = np.diff(Wq[:, :: 1024 // m], axis=1)
    q = np.sum(d ** 2, axis=1)
    check(abs(q.std(ddof=1) / math.sqrt(2 / m) - 1) < 0.05 and abs(q.mean() - 1) < 4 * math.sqrt(2 / m) / math.sqrt(50_000),
          "qv_moments: QV at m=%d has mean 1 and sd sqrt(2/m) (l3 screens[5], homework-1 items[0])" % m)
check(abs(math.sqrt(2 / 4096) - 0.0221) < 5e-5 and abs(math.sqrt(2 / 16) - 0.354) < 5e-4, "qv_moments: sd 0.0221 and 0.354 (l3 screens[5])")
check(abs(2 * 2 * 0.02 - 0.08) < 1e-12 and abs(math.sqrt(2 * 0.5 * 0.01) - 0.1) < 1e-12, "qv_moments: 0.08 and 0.1 (l3 quiz[2], review-1 items[5])")

# smooth_qv: f = t^2 on [0, 1], m steps: sum (df)^2 = m(4m^2 - 1)/3 / m^4 -> about 4/(3m)
m = 100
s_odd = sum((2 * k + 1) ** 2 for k in range(m))
check(s_odd == 1_333_300 and abs(s_odd / m ** 4 - 0.0133) < 5e-5, "smooth_qv: 1,333,300 / 10^8 = 0.0133 (l3 screens[7])")
check(abs(s_odd / m ** 4 / (4 / (3 * m)) - 1) < 1e-4, "smooth_qv: about 4/(3m), falls like 1/m (l3 screens[7].explain)")

# cross_variation_terms: sum |dW| dt is about T sqrt(2 dt / pi) -> 0; sum dt^2 = T dt -> 0
for mm in (64, 4096):
    dtm = 1 / mm
    d = np.diff(Wref[:: 4096 // mm])
    check(abs(np.sum(np.abs(d)) * dtm - math.sqrt(2 * dtm / math.pi)) < 0.2 * math.sqrt(2 * dtm / math.pi),
          "cross_variation_terms: sum |dW| dt about sqrt(dt) at m=%d (l3 screens[8])" % mm)
    check(abs(mm * dtm ** 2 - dtm) < 1e-15, "cross_variation_terms: sum dt^2 = T dt at m=%d (l3 screens[8])" % mm)

# cubic_variation: Var (dW)^3 = 15 dt^3; sum has variance 15 T dt^2 -> 0
cube = (rng.standard_normal(2_000_000) * math.sqrt(dt)) ** 3
check(abs(cube.var() / (15 * dt ** 3) - 1) < 0.05 and abs(cube.mean()) < 4 * cube.std() / math.sqrt(2_000_000), "cubic_variation: mean 0, variance 15 dt^3 (l3 quiz[1])")
d = np.diff(W, axis=1)
check(abs(np.sum(d ** 3, axis=1).var() / (15 * (1 / N) ** 2) - 1) < 0.1, "cubic_variation: sum variance 15 T dt^2 (l3 quiz[1])")

# realised volatility: sqrt(0.02036 / 0.5) and sqrt(0.0144 / 0.25)
check(abs(math.sqrt(0.02036 / 0.5) - 0.2018) < 5e-5 and abs(math.sqrt(0.0144 / 0.25) - 0.24) < 1e-9, "realised volatility (l3 screens[10], homework-1 items[7])")
# drift contribution to sum r^2 over a quarter: m^2 T^2 / n
mlog, T, nn = 0.06, 0.25, 63
r = mlog * T / nn + 0.2 * math.sqrt(T / nn) * rng.standard_normal((200_000, nn))
check(abs(np.sum(r ** 2, axis=1).mean() - (0.04 * T + mlog ** 2 * T ** 2 / nn)) < 1e-5, "drift adds m^2 T^2 / 63 to sum r^2 (homework-1 items[7].explain)")

# ---------------------------------------------------------------- l4
# gbm_moments: mean S0 e^{mu t}, median S0 e^{(mu - s^2/2) t}, mode S0 e^{(mu - 3 s^2 / 2) t}, Var S0^2 e^{2 mu t}(e^{s^2 t} - 1)
S0, mu, sig = 100.0, 0.08, 0.2
check(abs(S0 * math.exp(mu) - 108.33) < 5e-3 and abs(S0 * math.exp(mu - sig ** 2 / 2) - 106.18) < 5e-3, "gbm_moments: mean 108.33, median 106.18 (l4 screens[1], [2])")
check(abs(S0 * math.exp(0.08 - 0.005) - 107.79) < 5e-3 and abs(S0 * math.exp(0.08 - 0.18) - 90.48) < 5e-3, "gbm_moments: medians 107.79 and 90.48 (l4 screens[1])")
check(abs(S0 * math.exp(mu - sig ** 2 / 2 - sig ** 2) - 102.02) < 5e-3, "gbm_moments: mode 102.02 (l4 screens[10])")
var_exact = S0 ** 2 * math.exp(2 * mu) * (math.exp(sig ** 2) - 1)
check(abs(var_exact - 478.92) < 5e-3 and abs(math.sqrt(var_exact) - 21.88) < 5e-3, "gbm_moments: Var 478.92, sd 21.88 (review-1 items[7])")
check(abs(1e4 * math.exp(0.2) - 12214.03) < 5e-3, "gbm_moments: E[S_1^2] = 10^4 e^{0.2} (review-1 items[7])")
check(abs(math.sqrt(var_exact) / 100 - 0.22) < 5e-3, "gbm_moments: se of the mean on 10,000 paths 0.22 (l4 screens[9])")
ST = S0 * np.exp((mu - sig ** 2 / 2) + sig * rng.standard_normal(2_000_000))
check(abs(ST.mean() - S0 * math.exp(mu)) < 4 * math.sqrt(var_exact / 2_000_000), "gbm_moments sim: mean (l4 screens[2])")
check(abs(np.median(ST) - 106.18) < 0.05, "gbm_moments sim: median (l4 screens[2])")
check(abs(ST.var() - var_exact) < 0.03 * var_exact, "gbm_moments sim: variance (review-1 items[7])")
check(abs(50 * math.exp(0.11) - 55.81) < 5e-3 and abs(50 * math.exp(0.2) - 61.07) < 5e-3, "gbm_moments: 55.81 and 61.07 (l4 quiz[0], quiz[1])")
check(abs(0.5 * 0.3 ** 2 - 0.045) < 1e-12, "gbm_moments: flat median at mu = sigma^2/2 = 4.5% (l4 quiz[3])")

# gbm_prob_below
def prob_below(S0, K, mu, sig, T):
    return norm.cdf((math.log(K / S0) - (mu - sig ** 2 / 2) * T) / (sig * math.sqrt(T)))
check(abs(prob_below(100, 100, 0.08, 0.2, 1) - 0.3821) < 5e-5, "gbm_prob_below: 0.3821 (l4 screens[3])")
check(abs(prob_below(100, 100, 0.08, 0.6, 1) - 0.5662) < 5e-5, "gbm_prob_below: 0.5662 (l4 screens[4])")
check(abs(1 - prob_below(100, 120, 0.08, 0.2, 1) - 0.2704) < 5e-5, "gbm_prob_below: P(S_1 > 120) = 0.2704 (review-1 items[6])")
check(abs((ST < 100).mean() - 0.3821) < 4 * math.sqrt(0.38 * 0.62 / 2_000_000), "gbm_prob_below sim (l4 screens[3])")
ST6 = S0 * np.exp((0.08 - 0.18) + 0.6 * rng.standard_normal(2_000_000))
check(abs((ST6 < 100).mean() - 0.5662) < 4 * math.sqrt(0.25 / 2_000_000), "gbm_prob_below sim sigma 60% (l4 screens[4])")
check(abs(ST6.mean() - 108.33) < 4 * ST6.std() / math.sqrt(2_000_000), "gbm_prob_below: the mean still rises to 108.33 at 60% (l4 screens[4])")
check(abs(norm.cdf(-1) - 0.1587) < 5e-5, "P(X_4 < 0) = Phi(-1) (homework-1 items[6])")

# euler_vs_exact: Z = -6, dt = 1: exact 31.98, Euler -12; small-step gap of order sigma^2 dt
check(abs(100 * math.exp(0.06 - 1.2) - 31.98) < 5e-3 and abs(100 * (1 + 0.08 - 1.2) - (-12)) < 1e-9, "euler_vs_exact: 31.98 and -12 (l4 screens[6])")
zs = rng.standard_normal(200_000)
for h in (1 / 252, 1 / 1008):
    exact = np.exp((mu - sig ** 2 / 2) * h + sig * math.sqrt(h) * zs)
    euler = 1 + mu * h + sig * math.sqrt(h) * zs
    gap = np.abs(exact - euler).mean()
    check(gap < 2 * sig ** 2 * h, "euler_vs_exact: Euler gap is O(sigma^2 dt) at dt=%.5f (l4 screens[6].explain)" % h)

# additive_update_not_first_order (EXPECTED_FAIL): the content claims "all three agree to first order".
# The additive update S + mu dt + sigma sqrt(dt) Z differs from the exact step by about (S - 1) sigma sqrt(dt) |Z|,
# which is order sqrt(dt), not order dt, for S = 100. The assert below states the content's claim and fails.
h = 1 / 252
S = 100.0
exact = S * np.exp((mu - sig ** 2 / 2) * h + sig * math.sqrt(h) * zs)
additive = S + mu * h + sig * math.sqrt(h) * zs
gap_add = np.abs(exact - additive).mean()
check(gap_add < 2 * S * sig ** 2 * h, "EXPECTED_FAIL additive_update_not_first_order: content says the additive update agrees to first order, gap %.3f vs O(dt) %.4f (l4 quiz[2].explain)" % (gap_add, S * sig ** 2 * h))
# corrected assert, ready to enable once the explain is fixed:
# check(gap_add > 10 * S * sig ** 2 * h, "additive update disagrees at order sqrt(dt) for S = 100 (l4 quiz[2].explain)")

# ---------------------------------------------------------------- review-1 and homework-1
# w_fourth_moment: E W_t^4 = 3 t^2
check(abs(np.mean((math.sqrt(0.7) * zs) ** 4) - 3 * 0.49) < 0.05 * 3 * 0.49, "w_fourth_moment: E W_t^4 = 3 t^2 (review-1 items[0])")

# martingale_conditional_means: E[f(W_t) | W_s = w] against f(w) for candidate martingales
s_, t_ = 0.6, 1.5
ws = math.sqrt(s_) * rng.standard_normal(1_000_000)
D = math.sqrt(t_ - s_) * rng.standard_normal(1_000_000)
wt = ws + D
def cond_slope(f_t, f_s):
    # regression of f_t - f_s on f_s: a martingale has zero intercept and zero slope
    A = np.vstack([np.ones_like(f_s), f_s]).T
    coef, *_ = np.linalg.lstsq(A, f_t - f_s, rcond=None)
    return coef
for name, ft, fs, is_mart in (
    ("W^2 - t", wt ** 2 - t_, ws ** 2 - s_, True),
    ("W^3 - 3tW", wt ** 3 - 3 * t_ * wt, ws ** 3 - 3 * s_ * ws, True),
    ("exp(W - t/2)", np.exp(wt - t_ / 2), np.exp(ws - s_ / 2), True),
    ("W^2", wt ** 2, ws ** 2, False),
    ("W + 2t", wt + 2 * t_, ws + 2 * s_, False),
    ("|W|", np.abs(wt), np.abs(ws), False),
    ("W^3", wt ** 3, ws ** 3, False),
    ("tW", t_ * wt, s_ * ws, False),
    ("exp(W)", np.exp(wt), np.exp(ws), False),
):
    diff = ft - fs
    se = diff.std() / math.sqrt(len(diff))
    mean_zero = abs(diff.mean()) < 4 * se
    # also conditional: regress diff on fs and on ws
    coef = cond_slope(ft, fs)
    A = np.vstack([np.ones_like(ws), ws, ws ** 2]).T
    c2, *_ = np.linalg.lstsq(A, diff, rcond=None)
    cond_zero = mean_zero and abs(coef[1]) < 0.01 and abs(c2[1]) < 0.02 and abs(c2[2]) < 0.02
    check(cond_zero == is_mart, "martingale_conditional_means: %s is %sa martingale (review-1 items[4], homework-1 items[3])" % (name, "" if is_mart else "not "))
check(abs(np.abs(ws).mean() - math.sqrt(2 * s_ / math.pi)) < 0.003, "E|W_t| = sqrt(2t/pi) (review-1 items[4].options[3].why)")

# integrated_bm_var: Var(int_0^T W dt) = T^3/3, mean 0, normal
for T, nsteps in ((2.0, 200),):
    dWT = rng.standard_normal((200_000, nsteps)) * math.sqrt(T / nsteps)
    WT = np.cumsum(dWT, axis=1)
    A_ = WT.sum(axis=1) * (T / nsteps)  # right-point Riemann sum
    check(abs(A_.var() - T ** 3 / 3) < 0.03 * T ** 3 / 3, "integrated_bm_var: Var = T^3/3 = 2.6667 (review-1 items[8], homework-1 items[2])")
    check(abs(A_.mean()) < 4 * A_.std() / math.sqrt(200_000), "integrated_bm_var: mean 0 (review-1 items[8])")
check(abs(2 * (2.0 ** 3 / 6) - 8 / 3) < 1e-12, "integrated_bm_var: 2 int_0^T t^2/2 dt = T^3/3 (homework-1 items[2])")

# both_positive: P(W_1 > 0, W_2 > 0) = 3/8
X = rng.standard_normal(2_000_000); Y = rng.standard_normal(2_000_000)
pb = ((X > 0) & (X + Y > 0)).mean()
check(abs(pb - 0.375) < 4 * math.sqrt(0.375 * 0.625 / 2_000_000), "both_positive: 3/8 (homework-1 items[4])")
check(abs(0.25 + math.asin(1 / math.sqrt(2)) / (2 * math.pi) - 0.375) < 1e-12, "both_positive: Sheppard 1/4 + asin(rho)/(2 pi) (homework-1 items[4])")

# mixed_fourth_moment: E[W_s^2 W_t^2] = 2 s^2 + s t
s_, t_ = 0.7, 1.9
ws = math.sqrt(s_) * rng.standard_normal(2_000_000)
wt = ws + math.sqrt(t_ - s_) * rng.standard_normal(2_000_000)
val = np.mean(ws ** 2 * wt ** 2)
check(abs(val - (2 * s_ ** 2 + s_ * t_)) < 0.03 and abs(2 * s_ ** 2 + s_ * t_ - 2.31) < 1e-9, "mixed_fourth_moment: 2 s^2 + s t = 2.31 (homework-1 items[5])")

# bridge_variance: Var(B_t - t B_1) = t (1 - t)
nb = 100
dB = rng.standard_normal((200_000, nb)) * math.sqrt(1 / nb)
B = np.hstack([np.zeros((200_000, 1)), np.cumsum(dB, axis=1)])
tgrid = np.linspace(0, 1, nb + 1)
bridge = B - tgrid * B[:, -1:]
for k in (25, 50, 75):
    tk = tgrid[k]
    check(abs(bridge[:, k].var() - tk * (1 - tk)) < 0.02 * 0.25, "bridge_variance: t(1-t) at t=%.2f (homework-1 items[1])" % tk)
check(np.all(np.abs(bridge[:, -1]) < 1e-12) and np.all(bridge[:, 0] == 0), "bridge_variance: pinned at both ends (homework-1 items[1])")

print()
if failures:
    print("%d check(s) failed:" % len(failures))
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("all checks passed")
