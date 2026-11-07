"""Concept checks for ito level 3 (lessons l9 to l12, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/ito-L3-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-ito-1-3-ledger.md).
A check that fails because the content is wrong is marked EXPECTED_FAIL and
carries the corrected assert in a comment beside it.
"""
import math
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(20261108)
failures = []


def check(cond, name):
    if cond:
        print("ok   ", name)
    else:
        print("FAIL ", name)
        failures.append(name)


def bs(S, K, r, sig, T, q=0.0):
    d1 = (math.log(S / K) + (r - q + sig ** 2 / 2) * T) / (sig * math.sqrt(T)); d2 = d1 - sig * math.sqrt(T)
    call = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put = call - S * math.exp(-q * T) + K * math.exp(-r * T)
    delta = norm.cdf(d1); gamma = norm.pdf(d1) / (S * sig * math.sqrt(T))
    theta_c = -S * norm.pdf(d1) * sig / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)
    theta_p = -S * norm.pdf(d1) * sig / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)
    vega = S * norm.pdf(d1) * math.sqrt(T)
    return dict(d1=d1, d2=d2, call=call, put=put, delta=delta, gamma=gamma, theta_c=theta_c, theta_p=theta_p, vega=vega)


def pde_residual(price, S, r, sig, T, h=0.01, dt=1e-4):
    v0 = price(S, T); up = price(S + h, T); dn = price(S - h, T)
    v_s = (up - dn) / (2 * h); v_ss = (up - 2 * v0 + dn) / h ** 2
    v_t = -(price(S, T + dt) - price(S, T - dt)) / (2 * dt)
    return v_t + r * S * v_s + 0.5 * sig ** 2 * S ** 2 * v_ss - r * v0


# ---------------------------------------------------------------- l9: Greeks and the PDE
g = bs(100, 100, 0.05, 0.2, 1)
check(abs(g["delta"] - 0.6368) < 5e-5 and abs(g["gamma"] - 0.018762) < 5e-7 and abs(g["theta_c"] + 6.4140) < 5e-5 and abs(g["call"] - 10.4506) < 5e-5,
      "bs_greeks: delta 0.6368, gamma 0.018762, theta -6.4140, V 10.4506 (l9 screens[0], [1])")
terms = (g["theta_c"], 0.05 * 100 * g["delta"], 0.5 * 0.04 * 1e4 * g["gamma"], 0.05 * g["call"])
check(abs(terms[1] - 3.1842) < 5e-5 and abs(terms[2] - 3.7524) < 5e-5 and abs(terms[3] - 0.5225) < 5e-5 and abs(terms[0] + terms[1] + terms[2] - terms[3]) < 1e-9,
      "bs_greeks: the four terms sum to 0 (l9 screens[1])")
Pi = -g["call"] + 100 * g["delta"]
check(abs(Pi - 53.2325) < 5e-5 and abs(0.05 * Pi - 2.6616) < 5e-5 and abs((6.4140 - 3.7524) - 2.6616) < 1e-9, "bs_greeks: hedged book 53.2325 earns r Pi = 2.6616 = -theta - gamma term (l9 screens[3])")
check(abs(0.12 * Pi - 6.3879) < 5e-4, "bs_greeks: the mu distractor 6.3879 (l9 screens[3])")
fwd = lambda S, T: S - 100 * math.exp(-0.05 * T)
check(abs(fwd(100, 1) - 4.8771) < 5e-5 and abs(-0.05 * 100 * math.exp(-0.05) + 4.7561) < 5e-5 and all(abs(pde_residual(fwd, 100, 0.05, s, 1)) < 1e-6 for s in (0.2, 0.4, 0.8)),
      "bs_greeks: a forward satisfies the PDE for every sigma (l9 screens[4])")
callp = lambda S, T: bs(S, 100, 0.05, 0.2, T)["call"]
res = pde_residual(callp, 100, 0.05, 0.2, 1)
check(abs(res) < 1e-5, "bs_greeks: PDE residual of the call by central differences is tiny (%.2e) (l9 screens[5])" % res)
check(all(pde_residual(lambda S, T: bs(S, 100, 0.05, 0.2, T)["put"], s, 0.05, 0.2, 1) < 1e-5 for s in (80, 100, 120)), "bs_greeks: the put satisfies the PDE (homework-3 items[2])")
check(abs(pde_residual(lambda S, T: bs(S, 100, 0.05, 0.3, T)["call"], 100, 0.05, 0.2, 1)) > 1e-2, "bs_greeks: a call priced at 30% fails the 20% equation (homework-3 items[2])")
payoff = lambda S, T: max(S - 100, 0)
check(abs(pde_residual(payoff, 80, 0.05, 0.2, 1)) < 1e-9 and abs(pde_residual(payoff, 120, 0.05, 0.2, 1) - 5) < 1e-6, "bs_greeks: the payoff passes at 80 and has residual 5 at 120 (homework-3 items[2])")
check(abs(0.04 * 5 - 0.04 * 50 * 0.6 - 0.5 * 0.09 * 2500 * 0.02 + 3.25) < 1e-9, "bs_greeks: V_t = -3.25 (l9 quiz[0])")
check(abs(0.03 * 6 - 0.03 * 80 * 0.5 - 0.5 * 0.16 * 6400 * 0.03 + 16.38) < 1e-9, "bs_greeks: V_t = -16.38 (review-3 items[0])")
check(abs(g["put"] - 5.5735) < 5e-5 and abs(g["delta"] - 1 + 0.3632) < 5e-5 and abs(g["theta_p"] + 1.6579) < 5e-5 and abs(0.05 * g["put"] + 0.05 * 100 * 0.3632 - 3.7524 + 1.6579) < 2e-4,
      "bs_greeks: put V 5.5735, delta -0.3632, theta -1.6579 from the equation (l9 quiz[3])")
check(abs(g["vega"] / 100 - 0.3752) < 5e-5, "bs_greeks: vega 0.3752 per volatility point (homework-3 items[6])")
check(abs(bs(110, 100, 0.03, 0.25, 0.5)["delta"] - 0.7619) < 5e-5 and abs(bs(90, 100, 0.05, 0.3, 2)["theta_c"] + 5.593) < 5e-4, "bs_greeks: other settings (l9 screens[5] tests)")

# gamma_theta: daily P&L of the delta-hedged long call
theta_day = g["theta_c"] / 252; carry_day = (0.05 * 100 * g["delta"] - 0.05 * g["call"]) / 252
check(abs(theta_day + 0.025452) < 5e-7 and abs(carry_day - 0.010562) < 5e-7, "gamma_theta: theta -0.025452 and carry +0.010562 per call per day (l9 screens[7])")
pnl = (0.5 * g["gamma"] * 4 + theta_day + carry_day) * 1000
check(abs(pnl - 22.634) < 5e-3, "gamma_theta: a 2 pound day earns 22.63 (l9 screens[7])")
be = 0.2 * 100 / math.sqrt(252)
check(abs(be - 1.26) < 5e-3 and abs(0.5 * g["gamma"] * be ** 2 * 1000 - 14.89) < 0.02 and abs(14.89 - (25.452 - 10.562)) < 0.01, "gamma_theta: break-even move 1.26 (l9 screens[7].explain)")
check(abs((0.5 * g["gamma"] * 0.25 + theta_day + carry_day) * 1000 + 12.5) < 0.1, "gamma_theta: a 0.50 day loses about 12.50 (l9 screens[7].explain)")
check(abs(0.5 * 0.04 * 1e4 * g["gamma"] + g["theta_c"] - 0.05 * (g["call"] - 100 * g["delta"])) < 1e-9, "gamma_theta: gamma term + theta = r (V - S delta) (l9 screens[6])")
check(abs(0.3 * 50 / math.sqrt(252) - 0.9449) < 5e-5, "gamma_theta: break-even 0.9449 at r = 0 (review-3 items[1])")
# r = 0: expected gamma P&L over a day equals -theta over a day (simulated daily moves of size sigma S sqrt(dt))
g0 = bs(50, 50, 0.0, 0.3, 1)
moves = 0.3 * 50 * math.sqrt(1 / 252) * rng.standard_normal(1_000_000)
check(abs(np.mean(0.5 * g0["gamma"] * moves ** 2) + g0["theta_c"] / 252) < 1e-4, "gamma_theta: E[1/2 Gamma dS^2] = -theta dt when r = 0 (l9 screens[6], review-3 items[1])")

# ---------------------------------------------------------------- l10: Girsanov
mu, r, sig, S0 = 0.12, 0.05, 0.2, 100.0
theta = (mu - r) / sig
check(abs(theta - 0.35) < 1e-12 and abs((0.08 - 0.03) / 0.25 - 0.2) < 1e-12 and abs((0.10 - 0.04) / 0.2 - 0.3) < 1e-12, "girsanov: theta = (mu - r)/sigma (l10 screens[1], quiz[1], review-3 items[2])")
check(abs(100 * math.exp(0.07) - 107.25) < 5e-3 and abs(100 * math.exp(-0.05) - 95.12) < 5e-3, "girsanov: discounted averages 107.25 and 95.12 (l10 screens[0])")
Zw = lambda w, th=theta, T=1.0: math.exp(-th * w - th ** 2 * T / 2)
check(abs(Zw(1) - 0.6628) < 5e-5 and abs(Zw(-1) - 1.3348) < 5e-5 and abs((Zw(1) + Zw(-1)) / 2 - 0.9988) < 5e-5 and abs(Zw(-2) - 1.8941) < 5e-5, "girsanov: weights 0.6628, 1.3348, 1.8941 (l10 screens[4], quiz[3])")
check(abs(math.exp(0.3 - 0.045) - 1.2905) < 5e-5, "girsanov: weight 1.2905 (review-3 items[2])")
W1 = rng.standard_normal(2_000_000)
Z = np.exp(-theta * W1 - theta ** 2 / 2)
check(abs(Z.mean() - 1) < 4 * Z.std() / math.sqrt(2_000_000), "girsanov: E_P[Z_T] = 1 (l10 screens[3])")
STp = S0 * np.exp((mu - sig ** 2 / 2) + sig * W1)
check(abs(STp.mean() - 112.75) < 0.05 and abs(np.mean(Z * STp) - 105.13) < 0.05, "girsanov: E_P S_1 = 112.75, E_Q S_1 = E_P[Z S_1] = 105.13 (l10 screens[4], [5])")
check(abs(np.mean(Z * np.exp(-r) * STp) - 100) < 0.05, "girsanov: discounted share is a Q-martingale (l10 screens[2])")
# reweighted P-draws price the call; Q-paths have the same volatility (QV) as P-paths
price_rw = np.mean(Z * math.exp(-r) * np.maximum(STp - 100, 0))
check(abs(price_rw - 10.4506) < 4 * np.std(Z * math.exp(-r) * np.maximum(STp - 100, 0)) / math.sqrt(2_000_000), "girsanov: reweighted P-draws give the Black-Scholes price (l10 screens[7])")
realP = np.mean(math.exp(-r) * np.maximum(STp - 100, 0))
check(abs(realP - 15.53) < 0.03 and abs(np.mean(math.exp(-mu) * np.maximum(STp - 100, 0)) - 14.48) < 0.03, "girsanov: P-average discounted at r is 15.53, at mu 14.48 (l10 screens[8], l11 screens[4])")
check(abs(10.4506 * math.exp(0.05) - 10.99) < 5e-3, "girsanov: forgetting the discount gives 10.99 (l11 screens[4])")
# log-path QV is unchanged by reweighting: realised variance on P-paths equals sigma^2 whatever the weight
dWp = rng.standard_normal((20_000, 252)) * math.sqrt(1 / 252)
logS = np.cumsum((mu - sig ** 2 / 2) / 252 + sig * dWp, axis=1)
qv = np.sum(np.diff(np.hstack([np.zeros((20_000, 1)), logS]), axis=1) ** 2, axis=1)
Zp = np.exp(-theta * dWp.sum(axis=1) - theta ** 2 / 2)
check(abs(qv.mean() - sig ** 2) < 1e-3 and abs(np.mean(Zp * qv) - sig ** 2) < 1e-3, "girsanov: realised variance is sigma^2 under P and under Q: only the drift changes (l10 screens[5])")
check(abs(100 * math.exp(0.03) - 103.05) < 5e-3 and abs(50 * math.exp(0.04) - 52.04) < 5e-3 and abs(50 * math.exp(0.10) - 55.26) < 5e-3, "girsanov: E_Q S_1 = 103.05, 52.04; E_P 55.26 (l10 quiz[2], review-3 items[3])")
# homework-3 items[3]: average weight on the exercise event
mu3, r3, s3 = 0.09, 0.03, 0.25
pA = 1 - norm.cdf((math.log(1.1) - (mu3 - s3 ** 2 / 2)) / s3); qA = 1 - norm.cdf((math.log(1.1) - (r3 - s3 ** 2 / 2)) / s3)
check(abs(pA - 0.4419) < 5e-5 and abs(qA - 0.3497) < 5e-5 and abs(qA / pA - 0.7913) < 5e-5, "girsanov: P(A) 0.4419, Q(A) 0.3497, ratio 0.7913 (homework-3 items[3])")
th3 = (mu3 - r3) / s3
S3 = 100 * np.exp((mu3 - s3 ** 2 / 2) + s3 * W1); Z3 = np.exp(-th3 * W1 - th3 ** 2 / 2); A = S3 > 110
check(abs(np.mean(Z3[A]) - 0.7913) < 0.005, "girsanov sim: average weight on A = Q(A)/P(A) (homework-3 items[3])")

# ---------------------------------------------------------------- l11: Monte Carlo pricing
def mc_call(S0, K, r, sig, T, n, seed, antithetic=False):
    rg = np.random.default_rng(seed); z = rg.standard_normal(n)
    pay = lambda zz: np.maximum(S0 * np.exp((r - sig ** 2 / 2) * T + sig * math.sqrt(T) * zz) - K, 0)
    x = pay(z)
    if antithetic:
        x = (x + pay(-z)) / 2
    x = math.exp(-r * T) * x
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(n))
p, se = mc_call(100, 100, 0.05, 0.2, 1, 100_000, 11)
pa, sea = mc_call(100, 100, 0.05, 0.2, 1, 100_000, 11, True)
check(abs(p - 10.4534) < 5e-5 and abs(se - 0.0465) < 5e-5 and abs(pa - 10.4590) < 5e-5 and abs(sea - 0.0232) < 5e-5, "mc_pricing: seed-11 plain and antithetic (l11 screens[3])")
p1, se1 = mc_call(100, 100, 0.05, 0.2, 1, 1000, 11); p2, se2 = mc_call(100, 100, 0.05, 0.2, 1, 10_000, 11)
check(abs(p1 - 10.7168) < 5e-5 and abs(se1 - 0.4661) < 5e-5 and abs(se2 - 0.1478) < 5e-5 and abs(se1 / math.sqrt(10) - 0.1474) < 5e-5 and abs(se1 / 10 - 0.0466) < 5e-5, "mc_pricing: se falls like 1/sqrt(n) (l11 screens[2])")
check(abs(p - 10.4506) < 2 * se and abs(pa - 10.4506) < 2 * sea, "mc_pricing: both runs inside two se of the formula (l11 screens[3], [5])")
check(abs(math.exp(-0.05) * norm.cdf(0.15) - 0.5323) < 5e-5 and abs(math.exp(-0.05) * 0.6915 - 0.6577) < 5e-4 and abs(math.exp(-0.05) * 0.6368 - 0.6058) < 5e-4, "mc_pricing: digital 0.5323 and its distractors (l11 screens[7])")
z11 = np.random.default_rng(11).standard_normal(100_000)
dig = math.exp(-0.05) * (100 * np.exp(0.03 + 0.2 * z11) > 100)
check(abs(dig.mean() - 0.5320) < 5e-5 and abs(dig.std(ddof=1) / math.sqrt(100_000) - 0.0015) < 5e-5, "mc_pricing: digital simulation 0.5320 (0.0015) (l11 screens[7], [8])")
check(abs(6.20 * math.exp(-0.02) - 6.0772) < 5e-5 and abs(0.40 * math.exp(-0.06) - 0.3767) < 5e-5 and abs(0.42 * math.exp(-0.02) - 0.4117) < 5e-5 and (7.10 / 0.01) ** 2 == 504100 and abs(0.06 * math.sqrt(25000) - 9.49) < 5e-3 and round((0.06 * math.sqrt(25000) / 0.02) ** 2) == 225000,
      "mc_pricing: discounting and se arithmetic (l11 quiz, screens[9], review-3 items[4], [6])")
# BS formula as the Q-expectation, Phi(d2) as the exercise probability
check(abs(g["d1"] - 0.35) < 1e-12 and abs(g["d2"] - 0.15) < 1e-12 and abs(norm.cdf(0.15) - 0.5596) < 5e-5 and abs(63.68 - 95.12 * 0.5596 - 10.4506) < 0.01, "mc_pricing: d1 = 0.35, d2 = 0.15, Phi(d2) = 0.5596 (l11 screens[6])")
STq = 100 * np.exp(0.03 + 0.2 * W1)
check(abs(np.mean(STq > 100) - norm.cdf(0.15)) < 0.002 and abs(np.mean(STq * (STq > 100)) - 100 * math.exp(0.05) * norm.cdf(0.35)) < 0.1, "mc_pricing: Q(S_T > K) = Phi(d2), E_Q[S_T 1] = S0 e^{rT} Phi(d1) (l11 screens[6])")

# antithetic_not_always_half (was EXPECTED_FAIL): the summary said antithetic pairs halve the standard error on the same draws.
# At the money the ratio is 2.00; out of the money (homework-3 items[4]) it is 1.66.
po, seo = mc_call(80, 85, 0.03, 0.35, 1, 100_000, 17); poa, seoa = mc_call(80, 85, 0.03, 0.35, 1, 100_000, 17, True)
check(abs(seo - 0.0617) < 5e-5 and abs(seoa - 0.0372) < 5e-5 and abs((seo / seoa) ** 2 * 100_000 - 275_000) < 2000, "antithetic_not_always_half: 0.0617 -> 0.0372, worth 275,000 plain draws (homework-3 items[4])")
check(abs(se / sea - 2) < 0.05, "antithetic_not_always_half: at the money the ratio is about 2 (l11 screens[3])")
# Corrected claim (fix pass): the content now says the pairs halve the se for this call and cut it by less out of the money.
# Own computation (Glasserman 4.2): on the same n draws the se ratio is sqrt(2 / (1 + rho)), rho = corr(payoff(z), payoff(-z)).
# At the money rho is about -0.50 (ratio 2); for the l11 call at K = 120 and for homework-3 items[4] it is less than 2.
def anti_ratio(S0, K, r, sig, T, n, seed):
    zz = np.random.default_rng(seed).standard_normal(n)
    pay = lambda v: np.maximum(S0 * np.exp((r - sig ** 2 / 2) * T + sig * math.sqrt(T) * v) - K, 0)
    rho = np.corrcoef(pay(zz), pay(-zz))[0, 1]
    return math.sqrt(2 / (1 + rho))
r_atm = anti_ratio(100, 100, 0.05, 0.2, 1, 100_000, 11); r_120 = anti_ratio(100, 120, 0.05, 0.2, 1, 100_000, 11)
check(abs(r_atm - se / sea) < 0.02 and abs(r_atm - 2) < 0.05 and 1.3 < seo / seoa < 1.9 and 1.3 < r_120 < 1.9,
      "antithetic_not_always_half (corrected claim, fix pass): ratio %.2f at the money, %.2f at K = 120, %.2f for homework-3 items[4] (l11 screens[3].prose, summary.ideas[1])" % (r_atm, r_120, seo / seoa))

# crr_convergence
def crr(S0, K, r, sig, T, n):
    dt = T / n; u = math.exp(sig * math.sqrt(dt)); d = 1 / u; q = (math.exp(r * dt) - d) / (u - d)
    total = 0.0
    for j in range(n + 1):
        total += math.comb(n, j) * q ** j * (1 - q) ** (n - j) * max(S0 * u ** j * d ** (n - j) - K, 0)
    return math.exp(-r * T) * total
c100, c500, c101 = crr(100, 100, 0.05, 0.2, 1, 100), crr(100, 100, 0.05, 0.2, 1, 500), crr(100, 100, 0.05, 0.2, 1, 101)
check(abs(c100 - 10.4306) < 5e-5 and abs(c500 - 10.4466) < 5e-5 and abs(c101 - 10.4680) < 5e-5, "crr_convergence: 10.4306, 10.4466, odd 101 steps 10.4680 (l11 screens[5], [8])")
gaps = [crr(100, 100, 0.05, 0.2, 1, n) - 10.4506 for n in (100, 200, 400, 800)]
check(all(1.7 < gaps[i] / gaps[i + 1] < 2.3 for i in range(3)), "crr_convergence: the even-step gap falls like 1/n (l11 screens[5].explain), ratios %s" % [round(gaps[i] / gaps[i + 1], 2) for i in range(3)])
check(abs(crr(100, 100, 0.05, 0.2, 1, 1) - 12.1623) < 5e-5 and abs(crr(100, 100, 0.05, 0.2, 1, 2) - 9.5405) < 5e-5, "crr_convergence: 1 and 2 steps (l11 screens[8] tests)")

# power_claim (review-3 items[5])
check(abs(1e4 * math.exp(0.09) - 10941.74) < 5e-3 and abs(1e4 * math.exp(0.14) - 11502.74) < 5e-3 and abs(1e4 * math.exp(0.22) - 12460.77) < 5e-3, "power_claim: 10,941.74 and distractors (review-3 items[5])")
powV = lambda S, T: S ** 2 * math.exp((0.05 + 0.04) * T)
check(all(abs(pde_residual(powV, s, 0.05, 0.2, 0.7, h=0.1)) < 1e-4 for s in (50, 100, 150)), "power_claim: S^2 e^{(r + sigma^2)(T - t)} solves the PDE (review-3 items[5].explain)")
check(abs(np.mean(math.exp(-0.05) * STq ** 2) - 10941.74) < 4 * np.std(STq ** 2) * math.exp(-0.05) / math.sqrt(2_000_000), "power_claim sim: e^{-rT} E_Q S_T^2 (review-3 items[5])")

# ---------------------------------------------------------------- l12: reflection and barriers
check(abs(2 * (1 - norm.cdf(1)) - 0.3173) < 5e-5 and abs(2 * (1 - norm.cdf(2)) - 0.0455) < 5e-5, "reflection: P(max W >= 1) = 0.3173, level 2: 0.0455 (l12 screens[0], quiz[3])")
# exact reflection law by simulation with a fine grid plus Brownian-bridge correction (continuous monitoring),
# in batches to keep memory small
nsteps, P, batch = 1000, 200_000, 10_000
a = 1.0
cont_hits = 0.0; disc_hits = 0.0
for _ in range(P // batch):
    W = np.cumsum(rng.standard_normal((batch, nsteps)) * math.sqrt(1 / nsteps), axis=1)
    Wprev = np.hstack([np.zeros((batch, 1)), W[:, :-1]])
    disc_hits += (W.max(axis=1) >= a).sum()
    # bridge: P(cross between grid points | endpoints) = exp(-2 (a - x)(a - y) / dt) for x, y < a
    pc = np.exp(-2 * np.clip(a - Wprev, 0, None) * np.clip(a - W, 0, None) / (1 / nsteps))
    cont_hits += (1 - np.prod(1 - np.where((Wprev < a) & (W < a), pc, 1.0), axis=1)).sum()
    del W, Wprev, pc
cont, disc = cont_hits / P, disc_hits / P
check(abs(cont - 0.3173) < 4 * math.sqrt(0.3173 * 0.6827 / P), "reflection sim: continuous touch probability 0.3173 (l12 screens[0])")
check(disc < 0.3173 and abs(disc - 2 * (1 - norm.cdf(1 + 0.5826 / math.sqrt(nsteps)))) < 4 * math.sqrt(0.31 * 0.69 / P), "reflection sim: a discrete walk touches less, and BGK's shift predicts it (l12 screens[1], [2])")
def touch_mc(a, n_steps, paths, seed):
    rg = np.random.default_rng(seed); z = rg.standard_normal((paths, n_steps))
    return float(np.mean(np.cumsum(z * math.sqrt(1 / n_steps), axis=1).max(axis=1) >= a))
check(touch_mc(1, 1000, 5000, 13) == 0.3102 and touch_mc(1, 100, 5000, 13) == 0.2852 and touch_mc(1, 10, 5000, 13) == 0.2496, "reflection: seed-13 estimates 0.3102, 0.2852, 0.2496 (l12 screens[1])")
check(abs(1 + 0.5826 / math.sqrt(1000) - 1.0184) < 5e-5 and abs(2 * (1 - norm.cdf(1.0184)) - 0.3085) < 5e-5, "reflection: BGK shift 1.0184, corrected 0.3085 (l12 screens[2])")
check(abs(2 * (1 - norm.cdf(1.5 + 0.5826 / math.sqrt(250))) - 0.1243) < 5e-5 and abs(2 * (1 - norm.cdf(1.2 + 0.5826 / math.sqrt(500))) - 0.2202) < 5e-5, "reflection: 0.1243 and 0.2202 (review-3 items[9], homework-3 items[5])")
check(abs(-(-1.4603545) / math.sqrt(2 * math.pi) - 0.5826) < 5e-4, "reflection: beta = -zeta(1/2)/sqrt(2 pi) = 0.5826 (l12 screens[2])")

# barrier_formula
def dic(S, K, B, r, sig, T):
    lam = (r + sig ** 2 / 2) / sig ** 2
    y = math.log(B ** 2 / (S * K)) / (sig * math.sqrt(T)) + lam * sig * math.sqrt(T)
    return S * (B / S) ** (2 * lam) * norm.cdf(y) - K * math.exp(-r * T) * (B / S) ** (2 * lam - 2) * norm.cdf(y - sig * math.sqrt(T))
lam = 0.07 / 0.04; y = math.log(0.81) / 0.2 + lam * 0.2
check(abs(lam - 1.75) < 1e-12 and abs(y + 0.7036) < 5e-5 and abs(0.9 ** 3.5 - 0.6916) < 5e-5 and abs(0.9 ** 1.5 - 0.853815) < 5e-6, "barrier_formula: lambda, y, powers (l12 screens[3])")
cdi = dic(100, 100, 90, 0.05, 0.2, 1)
check(abs(cdi - 1.7851) < 5e-5 and abs(g["call"] - cdi - 8.6655) < 5e-5, "barrier_formula: c_di 1.7851, c_do 8.6655 (l12 screens[3])")
check(abs(g["call"] - dic(100, 100, 100, 0.05, 0.2, 1)) < 1e-9, "barrier_formula: barrier at the start price gives c_di = c, so c_do = 0 (l12 screens[5])")
bgk = lambda B, sig, dt: B * math.exp(-0.5826 * sig * math.sqrt(dt))
check(abs(0.5826 * 0.2 / math.sqrt(252) - 0.0073) < 5e-5 and abs(bgk(90, 0.2, 1 / 252) - 89.3418) < 5e-5 and abs(g["call"] - dic(100, 100, bgk(90, 0.2, 1 / 252), 0.05, 0.2, 1) - 8.9139) < 5e-5,
      "barrier_formula: shifted barrier 89.3418 and daily price 8.9139 (l12 screens[8], [9])")
check(abs(bgk(80, 0.25, 1 / 52) - 78.40) < 5e-3 and abs(bgk(95, 0.3, 1 / 12) - 90.33) < 5e-3, "barrier_formula: 78.40 and 90.33 (l12 quiz[2], review-3 items[7])")
check(abs(bs(100, 100, 0.04, 0.25, 1)["call"] - dic(100, 100, 85, 0.04, 0.25, 1) - 10.5828) < 5e-5 and abs(bs(100, 100, 0.04, 0.25, 1)["call"] - dic(100, 100, bgk(85, 0.25, 1 / 252), 0.04, 0.25, 1) - 10.7695) < 5e-5,
      "barrier_report: continuous 10.5828 and shifted 10.7695 at B = 85 (homework-3 items[1])")

# barrier_touch_measure: P(min S <= 90 within a year) under Q and under P (closed form with drift, and simulation)
def touch_below(B, S, nu, sig, T):
    b = math.log(B / S)
    return norm.cdf((b - nu * T) / (sig * math.sqrt(T))) + math.exp(2 * nu * b / sig ** 2) * norm.cdf((b + nu * T) / (sig * math.sqrt(T)))
pq = touch_below(90, 100, 0.05 - 0.02, 0.2, 1); pp = touch_below(90, 100, 0.12 - 0.02, 0.2, 1)
print("    touch probability of 90: Q %.3f, P (mu = 12%%) %.3f" % (pq, pp))
check(pq > 0.5, "barrier_touch_measure: under Q more than half the paths touch 90 (l12 screens[3].explain, as read under Q)")
check(pp < 0.5, "barrier_touch_measure: under the real drift of 12% fewer than half touch 90, so the claim depends on the measure (l12 screens[3].explain, finding)")
# simulate with bridge correction under Q to confirm the closed form (batched)
nst, b = 1000, math.log(0.9)
hits = 0.0
for _ in range(10):
    X = np.cumsum(0.03 / nst + 0.2 * rng.standard_normal((10_000, nst)) * math.sqrt(1 / nst), axis=1)
    Xp = np.hstack([np.zeros((10_000, 1)), X[:, :-1]])
    pcq = np.exp(-2 * np.clip(Xp - b, 0, None) * np.clip(X - b, 0, None) / (0.04 / nst))
    hits += (1 - np.prod(1 - np.where((Xp > b) & (X > b), pcq, 1.0), axis=1)).sum()
    del X, Xp, pcq
check(abs(hits / 100_000 - pq) < 4 * math.sqrt(0.25 / 100_000), "barrier_touch_measure sim: closed-form touch probability under Q (l12 screens[3])")

# barrier_daily: the seeded run and a high-precision daily-monitored price
def dao_mc(S0, K, B, r, sig, T, steps, paths, seed):
    if B >= S0:
        return 0.0, 0.0, 0.0
    rg = np.random.default_rng(seed); dt = T / steps
    z = rg.standard_normal((paths, steps))
    S = S0 * np.exp(np.cumsum((r - sig ** 2 / 2) * dt + sig * math.sqrt(dt) * z, axis=1))
    alive = S.min(axis=1) > B
    pay = math.exp(-r * T) * np.maximum(S[:, -1] - K, 0)
    x = pay * alive
    return float(x.mean()), float(x.std(ddof=1) / math.sqrt(paths)), float(pay.mean())
m, s_, van = dao_mc(100, 100, 90, 0.05, 0.2, 1, 252, 20_000, 12)
check(abs(m - 8.8510) < 5e-5 and abs(s_ - 0.1034) < 5e-5 and abs(van - 10.4128) < 5e-5 and abs(van - m - 1.5617) < 2e-4, "barrier_daily: seed-12 daily 8.8510 (0.1034), vanilla 10.4128, knock-in 1.5617 by parity (l12 screens[4], [6], [7])")
check(abs(dao_mc(100, 100, 90, 0.05, 0.2, 1, 12, 20_000, 12)[0] - 9.5712) < 5e-5 and abs(dao_mc(100, 100, 90, 0.05, 0.2, 1, 52, 20_000, 12)[0] - 9.0885) < 5e-5, "barrier_daily: monthly 9.5712, weekly 9.0885 (l12 screens[4])")
check(dao_mc(100, 100, 100, 0.05, 0.2, 1, 252, 2000, 12) == (0.0, 0.0, 0.0), "barrier_daily: barrier at the start returns 0 (l12 screens[5])")
acc = []
for k in range(60):
    acc.append(dao_mc(100, 100, 90, 0.05, 0.2, 1, 252, 50_000, 1000 + k)[0])
hp = float(np.mean(acc)); hp_se = float(np.std(acc, ddof=1) / math.sqrt(len(acc)))
print("    daily-monitored down-and-out, 3 million paths: %.4f (se %.4f); BGK 8.9139; continuous 8.6655" % (hp, hp_se))
check(abs(hp - 8.9139) < max(0.01, 4 * hp_se), "barrier_daily: 3 million daily paths agree with the shifted-barrier price 8.9139 to about a penny (l12 screens[8])")
check(hp - 8.6655 > 10 * hp_se, "barrier_daily: the daily price is above the continuous one by far more than noise (l12 screens[4])")
# in-out parity path by path and the end-price-only bug (quiz[0])
rg = np.random.default_rng(5); zq = rg.standard_normal((20_000, 252))
Sq = 100 * np.exp(np.cumsum((0.05 - 0.02) / 252 + 0.2 * math.sqrt(1 / 252) * zq, axis=1))
payq = math.exp(-0.05) * np.maximum(Sq[:, -1] - 100, 0); hitq = Sq.min(axis=1) <= 90
check(abs(np.mean(payq * hitq) + np.mean(payq * ~hitq) - np.mean(payq)) < 1e-12, "barrier_daily: in-out parity holds path by path (l12 screens[7], homework-3 items[1])")
check(np.mean(payq * (Sq[:, -1] > 90)) > np.mean(payq * ~hitq) + 0.5, "barrier_daily: testing only the final price overprices the knock-out (l12 quiz[0])")
check(abs((8.9139 - 8.6655) * 1000 - 248.4) < 1e-9 and abs((8.8510 - 8.6655) * 1000 - 185.5) < 1e-9, "barrier_daily: 248.40 and 185.50 (l12 screens[10])")

# barrier_report (homework-3 items[1]) seed 5
def report(seed):
    S0, K, B, r_, sig_, T, steps, paths = 100, 100, 85, 0.04, 0.25, 1, 252, 20000
    dt = T / steps
    van_ = bs(S0, K, r_, sig_, T)["call"]
    cont = van_ - dic(S0, K, B, r_, sig_, T); bg = van_ - dic(S0, K, bgk(B, sig_, dt), r_, sig_, T)
    rg = np.random.default_rng(seed); z = rg.standard_normal((paths, steps))
    S = S0 * np.exp(np.cumsum((r_ - sig_ ** 2 / 2) * dt + sig_ * math.sqrt(dt) * z, axis=1))
    hit = S.min(axis=1) <= B; pay = math.exp(-r_ * T) * np.maximum(S[:, -1] - K, 0)
    out = pay * ~hit; inn = pay * hit
    mc = out.mean(); se_ = out.std(ddof=1) / math.sqrt(paths)
    return [cont, mc, se_, bg, (mc - bg) / se_, inn.mean() + out.mean() - pay.mean()]
rep = report(5)
check(all(abs(a - b) < 5e-5 for a, b in zip(rep, [10.5828, 10.7510, 0.1292, 10.7695, -0.143, 0.0])), "barrier_report: seed-5 report (homework-3 items[1])")

print()
if failures:
    print("%d check(s) failed:" % len(failures))
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print("all checks passed")
