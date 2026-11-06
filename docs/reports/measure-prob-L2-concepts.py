"""Concept checks for measure-prob level 2 (lessons l5 to l8, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/measure-prob-L2-concepts.py
Each assert names the ledger row it backs (docs/reports/audit-measure-prob-1-3-ledger.md).
"""
import json
import math
import os
import sys
from fractions import Fraction

import numpy as np
from scipy.stats import norm
from scipy.integrate import quad

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'measure-prob')
rng = np.random.default_rng(20261106)
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print('FAIL', msg)


def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)


def close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_code_widget(widget, code):
    """Run a code widget's hidden tests against `code` (engine compare modes). Returns (passed, total)."""
    passed = 0
    tests = widget['tests']
    for t in tests:
        ns = {}
        mode = t.get('compare', 'isclose')
        try:
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            if mode == 'raises':
                try:
                    eval(t['call'], ns)
                    ok = False
                except Exception as e:
                    ok = type(e).__name__ == t['expect']
            else:
                got = eval(t['call'], ns)
                exp = t['expect']
                if isinstance(exp, str):
                    try:
                        exp = eval(exp, ns)
                    except Exception:
                        pass
                if mode == 'fraction':
                    ok = Fraction(got) == Fraction(exp)
                elif mode == 'isclose':
                    ok = close(got, exp)
                else:
                    ok = got == exp
        except Exception:
            ok = False
        passed += bool(ok)
    return passed, len(tests)


def code_checks(doc, path, label):
    w = doc
    for p in path:
        w = w[p]
    sp, n = run_code_widget(w, w['solution'])
    st, _ = run_code_widget(w, w['starter'])
    check(sp == n, f'{label}-code-solution: solution passes {sp} of {n} hidden tests')
    check(st < n, f'{label}-code-starter: starter passes {st} of {n}, must fail at least one')


# ---------------------------------------------------------------- l5-lebesgue-integral
l5 = load('l5-lebesgue-integral')


def dyadic_mean(n):
    N = 2 ** n
    return sum(k / N * (math.sqrt((k + 1) / N) - math.sqrt(k / N)) for k in range(N))


means = [dyadic_mean(n) for n in range(1, 7)]
stated = [0.1464, 0.2317, 0.2794, 0.3052, 0.3188, 0.3259]
check(all(abs(m - s) < 5e-5 for m, s in zip(means, stated)), 'l5-dyadic-means: E[phi_n] for n = 1..6')
check(abs(means[0] - 0.5 * (1 - 1 / math.sqrt(2))) < 1e-12, 'l5-dyadic-means: E[phi_1] = (1/2) P(U >= 1/sqrt 2)')
gaps = [1 / 3 - m for m in means]
check(all(gaps[i + 1] < gaps[i] for i in range(5)) and all(0.4 < gaps[i + 1] / gaps[i] < 0.6 for i in range(5)),
      'l5-dyadic-means: gap to 1/3 roughly halves each step')
check(all(dyadic_mean(n) <= dyadic_mean(n + 1) for n in range(10)) and 1 / 3 - dyadic_mean(12) < 1e-3,
      'l5-dyadic-means: means rise to 1/3 (staircase from below)')
# Monte Carlo: phi_n <= U^2 pointwise and E[U^2] = 1/3
U = rng.random(400_000)
X = U ** 2
check(abs(X.mean() - 1 / 3) < 0.002, 'l5-dyadic-means: E[U^2] = 1/3 (MC)')
check((np.floor(2 ** 4 * X) / 2 ** 4 <= X).all(), 'l5-dyadic-means: phi_4 never rises above X')
# layer-cake
check(abs(quad(lambda t: 1 - math.sqrt(t), 0, 1)[0] - 1 / 3) < 1e-9, 'l5-layer-cake: int_0^1 (1 - sqrt t) dt = 1/3')
check(abs(quad(lambda t: (1 + t) ** -3, 0, np.inf)[0] - 0.5) < 1e-9, 'l5-layer-cake: int (1+t)^-3 = 1/2 (quiz q-tail)')
check(abs(quad(lambda t: (1 + t) ** -2, 0, np.inf)[0] - 1.0) < 1e-9, 'l5-layer-cake: int (1+t)^-2 = 1 (byKey one)')
# MC layer-cake for a heavy tail with finite mean: P(X > t) = (1+t)^-3 -> X = U^{-1/3} - 1
Xh = U ** (-1 / 3) - 1
check(abs(Xh.mean() - 0.5) < 0.01, 'l5-layer-cake: E[X] = 1/2 for P(X > t) = (1+t)^-3 (MC)')
# St Petersburg caps
K = rng.geometric(0.5, size=1_000_000)
for m in (1, 3, 5, 10):
    check(abs(np.minimum(2.0 ** K, 2.0 ** m).mean() - (m + 1)) < 0.02 + 0.3 * (m >= 5), f'l5-st-petersburg-cap: E[min(X, 2^{m})] = {m + 1} (MC)')
check(sum(Fraction(2 ** k, 2 ** k) for k in range(1, 11)) + Fraction(2 ** 10, 2 ** 10) == 11, 'l5-st-petersburg-cap: exact m + 1 at m = 10')
check(abs(10 * math.exp(-2) - 1.3534) < 5e-5, 'l5-tranche: 10 e^{-2} = 1.3534')
Lx = rng.exponential(10, 1_000_000)
check(abs(np.maximum(Lx - 20, 0).mean() - 10 * math.exp(-2)) < 0.02, 'l5-tranche: E[(L-20)^+] = 10e^{-2} (MC)')
code_checks(l5, ['screens', 9, 'widget'], 'l5')

# ---------------------------------------------------------------- l6-monotone-convergence
l6 = load('l6-monotone-convergence')
for n, v in ((1, 0.7869), (2, 1.2642), (4, 1.7293), (10, 1.9865)):
    check(abs(2 * (1 - math.exp(-n / 2)) - v) < 5e-5, f'l6-capped-exp: E[min(X, {n})] = {v}')
Xe = rng.exponential(2, 1_000_000)
check(abs(np.minimum(Xe, 4).mean() - 2 * (1 - math.exp(-2))) < 0.01, 'l6-capped-exp: E[min(X, 4)] (MC)')
check(abs(np.minimum(Xe, 40).mean() - 2) < 0.01, 'l6-capped-exp: cap 40 is within 0.01 of E[X] = 2 (MC)')
Ng = rng.geometric(0.2, 1_000_000)
check(abs(Ng.mean() - 5) < 0.02, 'l6-tail-sum: E[N] = 5 for fill chance 0.2 (MC)')
check(abs(sum(0.8 ** k for k in range(2000)) - 5) < 1e-9, 'l6-tail-sum: sum 0.8^k = 5')
check(abs(sum((Ng > k).mean() for k in range(int(Ng.max()) + 1)) - Ng.mean()) < 1e-9, 'l6-tail-sum: sum P(N > k) equals E[N] (MC identity)')
# downward MCT fails: X_n = 1/(nU)
ints = [quad(lambda u: 1 / u, a, 1)[0] for a in (1e-3, 1e-6, 1e-9)]
check(all(abs(v + math.log(a)) < 1e-6 for v, a in zip(ints, (1e-3, 1e-6, 1e-9))) and ints[2] > 20, 'l6-downward-fails: int_a^1 du/u = -ln a grows without bound')
# years_to_reach and dividend stream
x = 1.03 / 1.08
n_needed = math.ceil(math.log(40) / math.log(1 / x))
check(n_needed == 78 and abs(math.log(40) / math.log(1 / x) - 77.82) < 0.01, 'l6-dividend-years: first year past 39 is 78')
partial = lambda n: sum(2 * 1.03 ** (k - 1) / 1.08 ** k for k in range(1, n + 1))
check(partial(77) < 39 <= partial(78), 'l6-dividend-years: partial sums bracket 39 at years 77 and 78')
check(abs(2 / (0.08 - 0.03) - 40) < 1e-12 and abs(partial(5000) - 40) < 1e-9, 'l6-dividend-years: full value 40')
code_checks(l6, ['screens', 7, 'widget'], 'l6')

# ---------------------------------------------------------------- l7-dominated-convergence
l7 = load('l7-dominated-convergence')
Us = rng.random(1_000_000)
for n in (4, 20, 100):
    Xn = n * (Us < 1 / n)
    check(abs(Xn.mean() - 1) < 0.02, f'l7-spike: E[X_{n}] = 1 (MC)')
check((20 * (0.3 < 1 / 20)) == 0, 'l7-spike: X_20(0.3) = 0')
sup = np.ceil(1 / Us) - 1  # largest n with n < 1/U
check(np.all(sup <= 1 / Us) and np.all(sup >= 1 / Us - 1), 'l7-spike-sup: sup_n X_n = ceil(1/U) - 1 is about 1/U')
check(sup.mean() > 5 and (np.ceil(1 / rng.random(10_000_000)) - 1).mean() > sup.mean() * 0.9,
      'l7-spike-sup: E[sup_n X_n] is large (infinite in the limit; MC sample means grow with n)')
check(abs(quad(lambda u: 2 * u ** (-1 / 3), 0, 1)[0] - 3) < 1e-9, 'r2-dom: E[2U^{-1/3}] = 3')
check(abs((Us ** 9).mean() - 0.1) < 0.002, 'l7-u-power: E[U^9] = 1/10 (MC)')
check(abs((Us ** 19).mean() - 0.05) < 0.002, 'l7-u-power: E[U^19] = 1/20 (MC)')
# thin spike n 1{U < 1/n^2}: sup about 1/sqrt U, mean 2; E[X_n] = 1/n
sup2 = np.floor(1 / np.sqrt(Us))  # largest n with n^2 <= 1/U ... n < 1/sqrt U
check(abs(sup2.mean() - 2) < 0.6 and sup2.mean() < 3, 'l7-thin-spike: E[sup_n X_n] is finite, near E[1/sqrt U] = 2 (MC)')
check(abs((10 * (Us < 1 / 100)).mean() - 0.1) < 0.005, 'l7-thin-spike: E[X_10] = 1/10 (MC)')
# pathwise delta of the call, DCT licence
S0, Kc, r, sig, T = 100, 100, 0.05, 0.2, 1
d1 = (math.log(S0 / Kc) + (r + sig ** 2 / 2) * T) / (sig * math.sqrt(T))
d2 = d1 - sig * math.sqrt(T)
check(abs(d1 - 0.35) < 1e-12 and abs(d2 - 0.15) < 1e-12, 'l7-pathwise-delta: d1 = 0.35, d2 = 0.15')
check(abs(norm.cdf(0.35) - 0.6368) < 5e-5 and abs(norm.cdf(0.15) - 0.5596) < 5e-5, 'l7-pathwise-delta: Phi values')
Z = rng.standard_normal(2_000_000)
M = np.exp((r - sig ** 2 / 2) * T + sig * math.sqrt(T) * Z)
check(abs(M.mean() - math.exp(r * T)) < 0.003, 'l7-pathwise-delta: E[M] = e^{rT} under the pricing measure (MC)')
check(abs((math.exp(-r * T) * M).mean() - 1) < 0.003, 'l7-pathwise-delta: E[Y] = 1 (MC)')
pw = (math.exp(-r * T) * M * (S0 * M > Kc)).mean()
check(abs(pw - norm.cdf(d1)) < 0.003, 'l7-pathwise-delta: E[e^{-rT} M 1{S_T > K}] = Phi(d1) (MC)')
# finite-difference delta of the Black-Scholes price agrees (the swap is licensed)
bs = lambda s: s * norm.cdf((math.log(s / Kc) + (r + sig ** 2 / 2) * T) / (sig * math.sqrt(T))) - Kc * math.exp(-r * T) * norm.cdf((math.log(s / Kc) + (r - sig ** 2 / 2) * T) / (sig * math.sqrt(T)))
check(abs((bs(100.01) - bs(99.99)) / 0.02 - norm.cdf(d1)) < 1e-6, 'l7-pathwise-delta: BS finite difference equals Phi(d1)')
check(abs(bs(100) - 10.4506) < 5e-5, 'l8-crr-convergence: Black-Scholes call 10.4506')
# digital delta
dig = lambda s: math.exp(-r * T) * norm.cdf((math.log(s / Kc) + (r - sig ** 2 / 2) * T) / (sig * math.sqrt(T)))
dd = math.exp(-r * T) * norm.pdf(d2) / (S0 * sig * math.sqrt(T))
check(abs(dd - 0.018762) < 5e-7 and abs(norm.pdf(0.15) - 0.394479) < 5e-7, 'l7-digital-delta: e^{-rT} phi(d2)/(S0 sigma sqrt T) = 0.018762')
check(abs((dig(100.01) - dig(99.99)) / 0.02 - dd) < 1e-6, 'l7-digital-delta: finite difference of the digital price agrees')
check(abs(math.exp(-0.05) * norm.cdf(0.15) - 0.5323) < 5e-5, 'l7-digital-delta: digital price 0.5323')
# the digital's difference quotients: mean about 0.0188 for every h, pathwise derivative 0 a.s.
for h in (1.0, 0.1, 0.01):
    q = (math.exp(-r * T) * (((S0 + h) * M > Kc) & (S0 * M <= Kc))).mean() / h
    check(abs(q - dd) < 0.004, f'l7-digital-delta: quotient mean at h={h} stays near 0.0188 (MC)')
check((np.abs(np.log(Kc / (S0 * M))) > 1e-12).all(), 'l7-digital-delta: S_0 M = K on no sampled path (null event)')
# sup over h of the quotients is not integrable: bound e^{-rT}/(K/M - S0) on paths with K/M > S0
gap = Kc / M - S0
means_by_cut = [(1 / gap[(gap > eps) & (gap < 1)]).mean() for eps in (1e-1, 1e-2, 1e-3, 1e-4)]
check(all(means_by_cut[i + 1] > means_by_cut[i] + 1.5 for i in range(3)), 'l7-digital-delta: E[1/gap; gap > eps] grows like ln(1/eps): no integrable dominator for the quotients')
# pathwise MC with the lesson's seed 7 reproduces the stated numbers
z7 = np.random.default_rng(7).standard_normal(100_000)
st7 = S0 * np.exp((r - sig ** 2 / 2) * T + sig * math.sqrt(T) * z7)
x7 = math.exp(-r * T) * (st7 > Kc) * st7 / S0
check(abs(x7.mean() - 0.635956) < 1e-6 and abs(x7.std(ddof=1) / math.sqrt(100_000) - 0.001822) < 1e-6,
      'l7-pathwise-mc: seed-7 estimate 0.635956, s.e. 0.001822')
check(abs(x7.mean() - norm.cdf(d1)) < x7.std(ddof=1) / math.sqrt(100_000), 'l7-pathwise-mc: within one standard error of Phi(0.35)')
lr7 = math.exp(-r * T) * (st7 > Kc) * z7 / (S0 * sig * math.sqrt(T))
check(abs(lr7.mean() - 0.018679) < 1e-6 and abs(lr7.std(ddof=1) / math.sqrt(100_000) - 0.000088) < 1e-6,
      'l7-lr-delta: seed-7 LR estimate 0.018679, s.e. 0.000088')
check(abs((dd - 0.018679) / 0.000088 - 0.94) < 0.01 and abs(dd / 0.000088 - 213) < 1, 'l7-lr-delta: 0.94 and 213 standard errors')
code_checks(l7, ['screens', 8, 'widget'], 'l7')

# ---------------------------------------------------------------- l8-modes-of-convergence
l8 = load('l8-modes-of-convergence')


def typewriter(n, omega):
    k = n.bit_length() - 1
    j = n - 2 ** k
    return 1 if j / 2 ** k <= omega < (j + 1) / 2 ** k else 0


check([n for n in range(1, 16) if typewriter(n, 0.3)] == [1, 2, 5, 10], 'l8-typewriter: X_n(0.3) = 1 at n = 1, 2, 5, 10')
check(sum(typewriter(n, 0.3) for n in range(1, 1024)) == 10, 'l8-typewriter: 10 hits up to n = 1023 (one per row)')
for om in (0.0, 0.3, 0.5, 0.7, 0.999):
    check(sum(typewriter(n, om) for n in range(1, 2 ** 14)) == 14, f'l8-typewriter: every omega is hit once per row (omega={om})')
check(100 .bit_length() - 1 == 6 and Fraction(1, 64) == Fraction(1, 2 ** 6), 'l8-typewriter: E[X_100^2] = 1/64')
# MC: P(X_n != 0) = 2^-k and E[X_n^2] = 2^-k, but X_n(omega) does not converge for any omega
Uw = rng.random(200_000)
for n in (10, 100, 1000):
    k = n.bit_length() - 1
    j = n - 2 ** k
    xn = ((j / 2 ** k <= Uw) & (Uw < (j + 1) / 2 ** k)).astype(float)
    check(abs(xn.mean() - 2.0 ** -k) < 0.003, f'l8-typewriter: P(X_{n} != 0) = 2^-{k} (MC)')
# spike modes
for n in (20, 200):
    xn = n * (Uw < 1 / n)
    check(abs((xn != 0).mean() - 1 / n) < 0.003 and abs((xn ** 2).mean() - n) < 0.1 * n, f'l8-spike-modes: P != 0 is 1/{n}, E[X^2] = {n} (MC)')
# reflection
Zr = rng.standard_normal(1_000_000)
check(abs((-Zr <= 1).mean() - norm.cdf(1)) < 0.002 and abs(norm.cdf(1) - 0.8413) < 5e-5, 'l8-reflection: F_{-Z}(1) = Phi(1) = 0.8413 (MC)')
check(abs((np.abs(-Zr - Zr) > 1).mean() - 2 * (1 - norm.cdf(0.5))) < 0.002 and abs(2 * (1 - norm.cdf(0.5)) - 0.6171) < 5e-5,
      'l8-reflection: P(|X_n - Z| > 1) = P(|Z| > 0.5) = 0.6171 for every n (MC)')
check(abs(((-Zr - Zr) ** 2).mean() - 4) < 0.02, 'l8-reflection: E[(X_n - Z)^2] = 4 (MC)')
# in distribution to a constant implies in probability: typewriter and spike both converge in prob
# Chebyshev
check(abs(0.04 / 0.25 - 0.16) < 1e-12 and abs((1 / 400) / 0.01 - 0.25) < 1e-12, 'l8-chebyshev: 0.16 and 0.25 bounds')
check(abs(((Zr / 10) ** 2).mean() - 0.01) < 0.0005, 'l8-zn: E[(Z/10)^2] = 0.01 (MC)')
code_checks(l8, ['screens', 9, 'widget'], 'l8')


# CRR tree convergence to Black-Scholes
def crr_call(S, Kx, rr, s, TT, n):
    dt = TT / n
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(rr * dt) - d) / (u - d)
    j = np.arange(n + 1)
    ST = S * u ** j * d ** (n - j)
    from scipy.special import comb
    probs = comb(n, j) * p ** j * (1 - p) ** (n - j)
    return math.exp(-rr * TT) * float(np.sum(probs * np.maximum(ST - Kx, 0)))


stated_tree = {10: 10.2534, 20: 10.3513, 50: 10.4107, 100: 10.4306, 200: 10.4406, 500: 10.4466, 1000: 10.4486}
for n, v in stated_tree.items():
    check(abs(crr_call(100, 100, 0.05, 0.2, 1, n) - v) < 5e-5, f'l8-crr-convergence: CRR price at {n} steps is {v}')
g100 = 10.4506 - 10.4306
g500 = 10.4506 - 10.4466
check(abs(g100 / g500 - 5) < 0.01, 'l8-crr-convergence: gap ratio 5 for 5x the steps (error ~ 1/n)')
check(abs((10.4506 - crr_call(100, 100, 0.05, 0.2, 1, 1000)) * 1000 - (10.4506 - crr_call(100, 100, 0.05, 0.2, 1, 100)) * 100) < 0.5,
      'l8-crr-convergence: n * error roughly constant (O(1/n))')

# ---------------------------------------------------------------- review-2
check(abs(quad(lambda t: (1 + t) ** -2, 4, np.inf)[0] - 0.2) < 1e-9, 'r2-layer: int_4^inf (1+t)^-2 = 1/5')
check(abs(sum(0.75 ** k for k in range(1, 500)) - 3) < 1e-9, 'r2-heavy: sum 0.75^k = 3')
xr = 1.02 / 1.07
check(math.ceil(math.log(20) / math.log(1 / xr)) == 63 and abs(math.log(20) / math.log(1 / xr) - 62.6) < 0.05, 'r2-dividend-years: 63')
ps = lambda n: sum(3 * 1.02 ** (k - 1) / 1.07 ** k for k in range(1, n + 1))
check(ps(62) < 57 <= ps(63) and abs(3 / 0.05 - 60) < 1e-12, 'r2-dividend-years: partial sums bracket 57; value 60')
# digital delta review item
S0r, Kr, rr_, sr, Tr = 100, 105, 0.03, 0.25, 0.5
d2r = (math.log(S0r / Kr) + (rr_ - sr ** 2 / 2) * Tr) / (sr * math.sqrt(Tr))
ddr = math.exp(-rr_ * Tr) * norm.pdf(d2r) / (S0r * sr * math.sqrt(Tr))
check(abs(ddr - 0.0214) < 5e-5 and abs(ddr - 0.021379762050349284) < 1e-9, 'r2-digital-delta: exact delta 0.0214')
d1r = d2r + sr * math.sqrt(Tr)
check(abs(norm.cdf(d1r) - 0.45907764450186667) < 1e-9, 'h2-lr-exact: call delta 0.4591 for the review digital set-up')
d2r2 = (math.log(100 / 115) + (0.03 - 0.25 ** 2 / 2) * 0.5) / (0.25 * math.sqrt(0.5))
check(abs(math.exp(-0.015) * norm.pdf(d2r2) / (100 * 0.25 * math.sqrt(0.5)) - 0.01621892246124238) < 1e-9, 'h2-lr-exact: K = 115 digital delta')
xm = 2 * 20 * (Uw < 1 / 400)
check(abs((xm != 0).mean() - 1 / 400) < 0.001 and abs((xm ** 2).mean() - 4) < 0.5, 'r2-mode: P(X_20 != 0) = 1/400 and E[X_20^2] = 4 (MC)')

# ---------------------------------------------------------------- homework-2
check(abs(math.exp(-25 / 8) - 0.0439) < 5e-5, 'h2-tranche: P(L > 25) = 0.0439')
check(abs(8 * (math.exp(-1.25) - math.exp(-3.125)) - 1.9405) < 5e-5, 'h2-tranche: expected tranche loss 1.9405')
L8 = rng.exponential(8, 1_000_000)
check(abs(np.minimum(np.maximum(L8 - 10, 0), 15).mean() - 1.9405) < 0.02, 'h2-tranche: E[min((L-10)^+, 15)] (MC)')
check(abs(8 * math.exp(-1.25) - 2.292) < 5e-4, 'h2-tranche: no-detach value 2.292')
check(abs(19 + 1e6 / 2 ** 19 - 20.9073) < 5e-5, 'h2-capped-sp: 19 + 10^6 / 2^19 = 20.9073')
check(abs(np.minimum(2.0 ** K, 1e6).mean() - 20.9073) < 0.5, 'h2-capped-sp: capped St Petersburg mean (MC, 1e6 draws)')
# h-modes: B = sqrt(n) 1{U < 1/n}
for n in (10, 1000):
    xb = math.sqrt(n) * (Uw < 1 / n)
    check(abs((xb ** 2).mean() - 1) < 0.1 and abs((xb != 0).mean() - 1 / n) < 0.003, f'h2-modes: B has E[X_n^2] = 1 and P != 0 = 1/{n} (MC)')
check(abs(((-Zr - Zr) ** 2).mean() - 4) < 0.02, 'h2-modes: C on odd n has E[(X_n - Z)^2] = 4 (MC)')
# h-nu: n U^n
check(abs(24 * quad(lambda u: u ** 24, 0, 1)[0] - 0.96) < 1e-9, 'h2-nu: E[X_24] = 24/25')
check(abs((24 * Uw ** 24).mean() - 0.96) < 0.01, 'h2-nu: E[24 U^24] = 0.96 (MC)')
check(abs((1000 * Uw ** 1000).mean() - 1000 / 1001) < 0.25, 'h2-nu: E[n U^n] -> 1 (MC, n = 1000, s.e. 0.05)')
check((1000 * Uw[Uw < 0.99] ** 1000).max() < 1e-1, 'h2-nu: X_n(U) -> 0 away from U = 1')
ns = np.arange(1, 20001)
delta = 1e-3
mx = (ns * (1 - delta) ** ns).max()
check(abs(mx - 1 / (math.e * delta)) / mx < 0.01, 'h2-nu: max_n n(1-delta)^n is about 1/(e delta)')
supn = np.array([(ns[:2000] * u ** ns[:2000]).max() for u in Uw[:20000]])
check(supn.mean() > 1.5 and (supn * (1 - Uw[:20000])).max() > 0.3, 'h2-nu: sup_n n U^n behaves like 1/(e(1-U)) near 1 (MC)')
hw2 = load('homework-2')
code_checks(hw2, ['items', 7, 'widget'], 'h2')
# LR weight is the S0-derivative of the log density of S_T
f = lambda s0, st: norm.pdf((math.log(st / s0) - (r - sig ** 2 / 2) * T) / (sig * math.sqrt(T))) / (st * sig * math.sqrt(T))
st_ = 110.0
zz = (math.log(st_ / 100) - (r - sig ** 2 / 2) * T) / (sig * math.sqrt(T))
num = (math.log(f(100.001, st_)) - math.log(f(99.999, st_))) / 0.002
check(abs(num - zz / (100 * sig * math.sqrt(T))) < 1e-6, 'h2-code: Z/(S0 sigma sqrt T) is d log f / d S0')

print(f'{len(failures)} failing checks')
sys.exit(1 if failures else 0)
