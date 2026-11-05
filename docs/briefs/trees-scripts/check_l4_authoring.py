"""Second check for the numbers added while authoring trees level 4 (lessons l13 to l18, review-4, homework-4).

check_l4.py (the brief's script) holds the numbers the brief states. This file holds every other number that
appears on a screen, in a feedback line, in a key or in a hidden test. Each is computed twice: method A is the
closed form (math.erf), method B is an independent route (numerical integration of the payoff against the
lognormal density with scipy.integrate.quad, finite differences of those integrals, or a vectorised
recomputation with scipy.special.ndtr). Run: python3 docs/briefs/trees-scripts/check_l4_authoring.py
"""
import math
import numpy as np
from math import erf, exp, log, sqrt, pi
from scipy.integrate import quad
from scipy.special import ndtr

fails, n_ok = [], 0


def check(name, a, b, tol=1e-6):
    global n_ok
    ok = abs(a - b) <= tol
    n_ok += ok
    if not ok:
        fails.append((name, a, b))
    print(("  ok " if ok else "  FAIL ") + f"{name:<72} {a:.6f}   (B {b:.6f})")


def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def phi(x):
    return exp(-x * x / 2) / sqrt(2 * pi)


def d12(S, K, r, s, T):
    d1 = (log(S / K) + (r + s * s / 2) * T) / (s * sqrt(T))
    return d1, d1 - s * sqrt(T)


def call(S, K, r, s, T):
    d1, d2 = d12(S, K, r, s, T)
    return S * Phi(d1) - K * exp(-r * T) * Phi(d2)


def put(S, K, r, s, T):
    d1, d2 = d12(S, K, r, s, T)
    return K * exp(-r * T) * Phi(-d2) - S * Phi(-d1)


def dens(S, r, s, T):
    mu = log(S) + (r - s * s / 2) * T
    sd = s * sqrt(T)
    return lambda x: exp(-(log(x) - mu) ** 2 / (2 * sd * sd)) / (x * sd * sqrt(2 * pi))


def call_B(S, K, r, s, T):
    f = dens(S, r, s, T)
    lo, hi = max(K, 1e-9), S * 40
    v = quad(lambda x: (x - K) * f(x), lo, hi, limit=400, epsabs=1e-12)[0]
    return exp(-r * T) * v


def put_B(S, K, r, s, T):
    f = dens(S, r, s, T)
    v = quad(lambda x: (K - x) * f(x), 1e-9, K, limit=400, epsabs=1e-12)[0]
    return exp(-r * T) * v


def digital_B(S, K, r, s, T):
    f = dens(S, r, s, T)
    return exp(-r * T) * quad(f, K, S * 40, limit=400, epsabs=1e-13)[0]


def gamma_A(S, K, r, s, T):
    return phi(d12(S, K, r, s, T)[0]) / (S * s * sqrt(T))


def gamma_B(S, K, r, s, T, h=0.05):
    return (call_B(S + h, K, r, s, T) - 2 * call_B(S, K, r, s, T) + call_B(S - h, K, r, s, T)) / h ** 2


def vega_A(S, K, r, s, T):
    return S * phi(d12(S, K, r, s, T)[0]) * sqrt(T)


def vega_B(S, K, r, s, T, h=1e-4):
    return (call_B(S, K, r, s + h, T) - call_B(S, K, r, s - h, T)) / (2 * h)


def theta_A(S, K, r, s, T):
    d1, d2 = d12(S, K, r, s, T)
    return -S * phi(d1) * s / (2 * sqrt(T)) - r * K * exp(-r * T) * Phi(d2)


def theta_B(S, K, r, s, T, h=1e-5):
    return -(call_B(S, K, r, s, T + h) - call_B(S, K, r, s, T - h)) / (2 * h)


print("l13 rules of thumb")
check("rule error S=50 s=.32 T=.25: 3.2 / 3.1881 - 1 = 0.37%", 3.2 / call(50, 50, 0, .32, .25) - 1, 3.2 / call_B(50, 50, 0, .32, .25) - 1, 1e-8)
for K, v in ((105, 5.9056), (110, 4.2920), (120, 2.1473)):
    check(f"OTM call K={K} (r=0, S=100, 20%, 1y) screen 8", round(call(100, K, 0, .2, 1), 4), round(call_B(100, K, 0, .2, 1), 4), 1e-9)
    check(f"   stated value {v}", v, round(call(100, K, 0, .2, 1), 4), 1e-9)
check("rule 8.00 / call(K=110) = 1.86 (quiz q-otm)", 8 / call(100, 110, 0, .2, 1), 8 / call_B(100, 110, 0, .2, 1), 1e-7)
check("doubling vol: 1.99 times (quiz)", call(100, 100, 0, .4, 1) / call(100, 100, 0, .2, 1), call_B(100, 100, 0, .4, 1) / call_B(100, 100, 0, .2, 1), 1e-7)
check("quadrupling T: 1.99 times", call(100, 100, 0, .2, 4) / call(100, 100, 0, .2, 1), call_B(100, 100, 0, .2, 4) / call_B(100, 100, 0, .2, 1), 1e-7)
check("doubling T: 1.41 times", call(100, 100, 0, .2, 2) / call(100, 100, 0, .2, 1), call_B(100, 100, 0, .2, 2) / call_B(100, 100, 0, .2, 1), 1e-7)
check("doubling spot at fixed strike: 12.55 times (quiz says about 12.6)", call(200, 100, 0, .2, 1) / call(100, 100, 0, .2, 1), call_B(200, 100, 0, .2, 1) / call_B(100, 100, 0, .2, 1), 1e-6)
check("S=80 s=25% T=.25 rule 4.00, BS 3.9868", call(80, 80, 0, .25, .25), call_B(80, 80, 0, .25, .25), 1e-8)
check("vega rule 39.83 against true 39.695 (price / sigma)", 7.9656 / .2, 39.828, 1e-3)
check("true ATM vega 39.695 by finite difference", vega_A(100, 100, 0, .2, 1), vega_B(100, 100, 0, .2, 1), 1e-5)
check("transfer: straddle 5.77% move (6.93 / 120)", 6.93 / 120, 0.0577, 1e-4)
check("transfer: exact straddle 6.9084 / 120 = 5.76%", 2 * call(120, 120, 0, .25, 1 / 12) / 120, 2 * call_B(120, 120, 0, .25, 1 / 12) / 120, 1e-8)
check("PV gap S - K e^{-rT} = 4.877 (trap, r=5%)", 100 - 100 * exp(-.05), 100 - 100 * exp(-0.05), 1e-12)
check("r=5% price 10.4506 (screen 6)", call(100, 100, .05, .2, 1), call_B(100, 100, .05, .2, 1), 1e-7)
check("trap miss 2.45: 10.4506 - 8", call(100, 100, .05, .2, 1) - 8, call_B(100, 100, .05, .2, 1) - 8, 1e-7)
check("rule plus half gap 10.4385", .4 * .2 * 100 + .5 * (100 - 100 * exp(-.05)), 10.4385, 5e-5)
check("rule plus whole gap 12.877 (key 12.88)", 8 + 100 - 100 * exp(-.05), 12.877, 5e-4)

print("l14 greeks by shape")
check("ATM delta 0.5398 (sketch)", Phi(.1), (call_B(100.01, 100, 0, .2, 1) - call_B(99.99, 100, 0, .2, 1)) / .02, 1e-6)
for T, tag in ((1, "1y"), (.25, "3m"), (.0833, "1m"), (.0192, "1w")):
    pk = max(100 * gamma_A(x / 10, 100, 0, .2, T) for x in range(600, 1400))
    pkB = max(100 * gamma_B(x / 10, 100, 0, .2, T, h=0.02) for x in range(900, 1000, 2))
    check(f"peak gamma x100, {tag}", pk, pkB, 0.01 if T > .05 else 0.02)
check("gamma peak at 94.18 (T=1)", 100 * exp(-1.5 * .04), 94.17645, 1e-4)
check("gamma ratio K=130, T=1 over T=.25 is 6.58", gamma_A(100, 130, 0, .2, 1) / gamma_A(100, 130, 0, .2, .25), gamma_B(100, 130, 0, .2, 1, 0.1) / gamma_B(100, 130, 0, .2, .25, 0.1), 5e-3)
check("gamma K=130 T=1: 0.009572", gamma_A(100, 130, 0, .2, 1), gamma_B(100, 130, 0, .2, 1, 0.1), 2e-6)
check("gamma K=130 T=.25: 0.001454", gamma_A(100, 130, 0, .2, .25), gamma_B(100, 130, 0, .2, .25, 0.1), 2e-6)
check("vega per point at the strike 0.397 = Gamma S^2 sigma T / 100", gamma_A(100, 100, 0, .2, 1) * 1e4 * .2 / 100, vega_B(100, 100, 0, .2, 1) / 100, 1e-6)
check("vega from rounded gamma 0.0198: 0.396 (answer 0.397 tol .005)", .0198 * 1e4 * .2 / 100, .397, .005)
check("theta a day -0.01575 = -.5 s^2 S^2 Gamma / 252 against -dC/dT", -.5 * .04 * 1e4 * gamma_A(100, 100, 0, .2, 1) / 252, theta_B(100, 100, 0, .2, 1) / 252, 1e-6)
check("theta a day from rounded gamma: -0.0157 (answer -0.0158 tol .0005)", -.5 * .04 * 1e4 * .0198 / 252, -.0158, .0005)
check("gamma one day / one year = 15.95 (sqrt 252 = 15.87)", gamma_A(100, 100, 0, .2, 1 / 252) / gamma_A(100, 100, 0, .2, 1), gamma_B(100, 100, 0, .2, 1 / 252, 0.01) / gamma_B(100, 100, 0, .2, 1, 0.01), 5e-3)
check("vega one day 2.51 and one year 39.70", vega_A(100, 100, 0, .2, 1 / 252), vega_B(100, 100, 0, .2, 1 / 252), 1e-4)
check("straddle theta a year, 3 months: -15.9378", 2 * theta_A(100, 100, 0, .2, .25), 2 * theta_B(100, 100, 0, .2, .25), 1e-5)
check("desk theta a day x 10,000 = -632.45", 2 * theta_A(100, 100, 0, .2, .25) / 252 * 1e4, 2 * theta_B(100, 100, 0, .2, .25) / 252 * 1e4, 1e-2)
check("desk: -159,380 a year for the key", 2 * theta_A(100, 100, 0, .2, .25) * 1e4, -159380, 5)
check("breakeven daily move 1.2599", 100 * .2 / sqrt(252), 100 * .2 * sqrt(1 / 252), 1e-12)
check("delta at 120 strike gamma peak rounding: delta 0.5398 and put -0.4602", Phi(.1) - 1, -0.460172, 1e-5)
check("calendar net gamma -0.0292 (1m 0.0691 less 3m 0.0398 -> -0.0293 rounded legs)", gamma_A(100, 100, 0, .2, .25) - gamma_A(100, 100, 0, .2, 1 / 12), gamma_B(100, 100, 0, .2, .25, .02) - gamma_B(100, 100, 0, .2, 1 / 12, .02), 1e-5)

print("l15 digitals")
for h, v in ((20, .5330), (10, .5325)):
    A = (call(100, 100 - h / 2, .05, .2, 1) - call(100, 100 + h / 2, .05, .2, 1)) / h
    B = (call_B(100, 100 - h / 2, .05, .2, 1) - call_B(100, 100 + h / 2, .05, .2, 1)) / h
    check(f"spread over h = {h} rounds to {v}", round(A, 4), round(B, 4), 1e-9)
    check(f"   stated {v}", v, round(A, 4), 1e-9)
check("digital call 0.5323 by integration", exp(-.05) * Phi(.15), digital_B(100, 100, .05, .2, 1), 1e-7)
check("digital put 0.4189", exp(-.05) * Phi(-.15), exp(-.05) - digital_B(100, 100, .05, .2, 1), 1e-7)
check("digital call K=105 0.4400", exp(-.05) * Phi(d12(100, 105, .05, .2, 1)[1]), digital_B(100, 105, .05, .2, 1), 1e-7)
check("digital put K=105 0.5112 = 0.9512 - 0.4400", exp(-.05) - exp(-.05) * Phi(d12(100, 105, .05, .2, 1)[1]), exp(-.05) - digital_B(100, 105, .05, .2, 1), 1e-7)
check("digital put K=105 no-discount key 0.5374 = Phi(-d2)", Phi(-d12(100, 105, .05, .2, 1)[1]), 1 - 0.46257411, 1e-6)
check("over-hedge cost 0.5417", call(100, 99, .05, .2, 1) - call(100, 100, .05, .2, 1), call_B(100, 99, .05, .2, 1) - call_B(100, 100, .05, .2, 1), 1e-7)
check("over-hedge above fair 0.0094", call(100, 99, .05, .2, 1) - call(100, 100, .05, .2, 1) - exp(-.05) * Phi(.15), call_B(100, 99, .05, .2, 1) - call_B(100, 100, .05, .2, 1) - digital_B(100, 100, .05, .2, 1), 1e-7)
check("pin: 3,166 shares per 10,000 digitals one day out", 1e4 * exp(-.05 / 252) * phi(d12(100, 100, .05, .2, 1 / 252)[1]) / (100 * .2 * sqrt(1 / 252)),
      1e4 * (digital_B(100.01, 100, .05, .2, 1 / 252) - digital_B(99.99, 100, .05, .2, 1 / 252)) / .02, 1.0)
check("pin: 188 one year out", 1e4 * exp(-.05) * phi(d12(100, 100, .05, .2, 1)[1]) / (100 * .2), 1e4 * (digital_B(100.01, 100, .05, .2, 1) - digital_B(99.99, 100, .05, .2, 1)) / .02, .05)
check("£2m note 1,064,650", 2e6 * exp(-.05) * Phi(.15), 2e6 * digital_B(100, 100, .05, .2, 1), 1.0)
check("£2m note no-discount key 1,119,235", 2e6 * Phi(.15), 1119235, 1)
check("£2m note d1-slip key 1,211,544", 2e6 * exp(-.05) * Phi(.35), 1211544, 1)
check("asset-or-nothing 63.68 less 53.23 = 10.45", 100 * Phi(.35) - 100 * exp(-.05) * Phi(.15), call_B(100, 100, .05, .2, 1), 1e-6)

print("l16 smile (extra numbers)")
sg = lambda K: .2 - .002 * (K - 100)
Psk = lambda K: Phi(d12(100, K, 0, sg(K), 1)[1]) + .002 * vega_A(100, K, 0, sg(K), 1)
Csk_B = lambda K: call_B(100, K, 0, sg(K), 1)
for K in (70, 100, 110):
    check(f"P(S_T>{K}) on the skew by -dC/dK of integral prices", Psk(K), -(Csk_B(K + .01) - Csk_B(K - .01)) / .02, 2e-6)
check("flat 18% digital at K=110 is 0.2678", Phi(d12(100, 110, 0, .18, 1)[1]), digital_B(100, 110, 0, .18, 1), 1e-7)
check("vega at 110 18%: 36.2214", vega_A(100, 110, 0, .18, 1), vega_B(100, 110, 0, .18, 1), 1e-4)
check("correction 0.0724", .002 * vega_A(100, 110, 0, .18, 1), .002 * vega_B(100, 110, 0, .18, 1), 1e-6)
check("skew digital at 110 0.3402", Psk(110), -(Csk_B(110.01) - Csk_B(109.99)) / .02, 2e-6)
check("0.3402 / 0.2821 - 1 = 0.2059", Psk(110) / Phi(d12(100, 110, 0, .2, 1)[1]) - 1, 0.3402360 / 0.2821214 - 1, 1e-6)
check("digital difference key 0.0581", Psk(110) - Phi(d12(100, 110, 0, .2, 1)[1]), 0.0581146, 1e-5)
check("flat 26% chance below 70: 10.72%", 1 - Phi(d12(100, 70, 0, .26, 1)[1]), 1 - digital_B(100, 70, 0, .26, 1), 1e-7)
check("risk reversal put 80 at 24%: 2.0317", put(100, 80, 0, .24, 1), put_B(100, 80, 0, .24, 1), 1e-7)
check("risk reversal call 120 at 16%: 1.1093", call(100, 120, 0, .16, 1), call_B(100, 120, 0, .16, 1), 1e-7)
check("premium received 0.9224", put(100, 80, 0, .24, 1) - call(100, 120, 0, .16, 1), put_B(100, 80, 0, .24, 1) - call_B(100, 120, 0, .16, 1), 1e-7)
check("flat 20%: put 1.1859, call 2.1473, pay 0.9614", put(100, 80, 0, .2, 1) - call(100, 120, 0, .2, 1), put_B(100, 80, 0, .2, 1) - call_B(100, 120, 0, .2, 1), 1e-7)

print("l17 which is cheaper (extra numbers)")
path = [100, 103, 98, 95, 91, 94, 99, 104, 108, 105, 102, 107, 112]
pa = np.array(path, float)
A = [max(path[-1] - 100, 0), max(sum(path[1:]) / 12 - 100, 0), path[-1] - min(path), 0 if min(path) <= 92 else max(path[-1] - 100, 0)]
B = [max(pa[-1] - 100, 0), max(pa[1:].mean() - 100, 0), pa[-1] - pa.min(), 0 if pa.min() <= 92 else max(pa[-1] - 100, 0)]
for nme, a, b in zip(("vanilla 12", "Asian 1.5", "lookback 21", "knock-out 0"), A, B):
    check("one-path payoff " + nme, a, b, 1e-12)
check("13-point average would be 101.38", sum(path) / 13, pa.mean(), 1e-12)
check("down-and-out less than vanilla: 7.9656 - 1.4982 = 6.4674 (sum)", 7.9656 - 1.4982, 6.4674, 1e-9)
check("vanilla S=90 K=100 (up-and-out edge key 3.59)", call(90, 100, 0, .2, 1), call_B(90, 100, 0, .2, 1), 1e-7)
check("Asian quote 7.50 against the near-4.60 level; vanilla / sqrt3 = 4.60", call(100, 100, 0, .2, 1) / sqrt(3), call_B(100, 100, 0, .2, 1) / sqrt(3), 1e-7)
check("American put premium 6.0899 - 5.5735 = 0.5164 (European put)", put(100, 100, .05, .2, 1), put_B(100, 100, .05, .2, 1), 1e-7)
check("European put at r=0 equals 7.9656 (trap)", put(100, 100, 0, .2, 1), put_B(100, 100, 0, .2, 1), 1e-7)

print("l18 gamma and hedging (extra numbers)")
DT = 1 / 252
check("breakeven S=50 s=30%: 0.9449", 50 * .3 / sqrt(252), 50 * .3 * sqrt(DT), 1e-12)
check("calendar-days slip: 50 * .3 / sqrt(365) = 0.785", 50 * .3 / sqrt(365), 0.785136, 1e-5)
check("one day, £2 move: gamma gain 0.0397", .5 * gamma_A(100, 100, 0, .2, 1) * 4, .5 * gamma_B(100, 100, 0, .2, 1, 0.05) * 4, 1e-6)
check("one day net 0.0239 (gamma gain less theta)", .5 * gamma_A(100, 100, 0, .2, 1) * 4 + theta_A(100, 100, 0, .2, 1) / 252, .5 * gamma_B(100, 100, 0, .2, 1, 0.05) * 4 + theta_B(100, 100, 0, .2, 1) / 252, 1e-6)
full_A = call(102, 100, 0, .2, 1 - DT) - call(100, 100, 0, .2, 1) - Phi(.1) * 2
full_B = call_B(102, 100, 0, .2, 1 - DT) - call_B(100, 100, 0, .2, 1) - (call_B(100.01, 100, 0, .2, 1) - call_B(99.99, 100, 0, .2, 1)) / .02 * 2
check("one day full revaluation 0.0234", full_A, full_B, 1e-5)
check("variance gap 0.0276 and 0.0676", .26 ** 2 - .2 ** 2, 0.0276, 1e-12)
check("vega x gap at 18%: -0.79 (exact -0.7943)", vega_A(100, 100, 0, .2, 1) * -.02, -0.79390, 1e-4)
check("exact gap at 18%: 7.1713 less 7.9656", call(100, 100, 0, .18, 1) - call(100, 100, 0, .2, 1), call_B(100, 100, 0, .18, 1) - call_B(100, 100, 0, .2, 1), 1e-7)
check("price at 26% 10.3434, gap 2.3778", call(100, 100, 0, .26, 1) - call(100, 100, 0, .2, 1), call_B(100, 100, 0, .26, 1) - call_B(100, 100, 0, .2, 1), 1e-7)
check("constant gamma overshoot 2.74", .5 * gamma_A(100, 100, 0, .2, 1) * 1e4 * .0276, 99.238137 * .0276, 1e-5)
check("q: 1,000 options, 24% against 20%: vega x gap 1,587.8", 1000 * vega_A(100, 100, 0, .2, 1) * .04, 1000 * vega_B(100, 100, 0, .2, 1) * .04, 1e-2)
check("q: exact price gap for 1,000 options 1,586.1", 1000 * (call(100, 100, 0, .24, 1) - call(100, 100, 0, .2, 1)), 1000 * (call_B(100, 100, 0, .24, 1) - call_B(100, 100, 0, .2, 1)), 1e-3)
check("q: points slip 39.695 * 4 * 1000 = 158,780", vega_A(100, 100, 0, .2, 1) * 4 * 1000, 158780, 2.0)


def pnl_loop(path, s=.2, K=100):
    tot, est, n = 0.0, 0.0, len(path) - 1
    for k in range(n):
        tau = (n - k) * DT
        S0, S1 = path[k], path[k + 1]
        d1 = d12(S0, K, 0, s, tau)[0]
        nxt = call(S1, K, 0, s, tau - DT) if k < n - 1 else max(S1 - K, 0)
        tot += nxt - call(S0, K, 0, s, tau) - Phi(d1) * (S1 - S0)
        est += .5 * phi(d1) / (S0 * s * sqrt(tau)) * S0 ** 2 * ((S1 / S0 - 1) ** 2 - s * s * DT)
    return tot, est


def pnl_vec(path, s=.2, K=100):
    p = np.asarray(path, float)
    n = len(p) - 1
    tau = (n - np.arange(n)) * DT
    S0, S1 = p[:-1], p[1:]
    d1 = (np.log(S0 / K) + .5 * s * s * tau) / (s * np.sqrt(tau))
    c0 = S0 * ndtr(d1) - K * ndtr(d1 - s * np.sqrt(tau))
    t1 = tau - DT
    with np.errstate(all='ignore'):
        d1n = (np.log(S1 / K) + .5 * s * s * t1) / (s * np.sqrt(t1))
        c1 = S1 * ndtr(d1n) - K * ndtr(d1n - s * np.sqrt(t1))
    c1[-1] = max(S1[-1] - K, 0)
    g = np.exp(-d1 ** 2 / 2) / sqrt(2 * pi) / (S0 * s * np.sqrt(tau))
    return (c1 - c0 - ndtr(d1) * (S1 - S0)).sum(), (.5 * g * S0 ** 2 * ((S1 / S0 - 1) ** 2 - s * s * DT)).sum()


def zig(sr, up_days):
    r = sr * sqrt(DT)
    out = [100.0]
    for k in range(252):
        up = k < up_days or (k - up_days) % 2 == 0
        out.append(round(out[-1] * exp(r if up else -r), 4))
    return out


Np = [100.0]
r26 = .26 * sqrt(DT)
for k in range(252):
    Np.append(round(Np[-1] * exp(r26 if k % 2 == 0 else -r26), 4))
for nm, p in (("N", Np), ("F", zig(.26, 21))):
    a, b = pnl_loop(p), pnl_vec(p)
    check(f"path {nm} at 26%: exact hedged P&L (loop erf vs vector ndtr)", a[0], b[0], 1e-9)
print(f"      path N exact {pnl_loop(Np)[0]:.4f}, path F exact {pnl_loop(zig(.26, 21))[0]:.4f} (stated 4.82 and 0.38)")
check("path N at 26% is 4.82", round(pnl_loop(Np)[0], 2), 4.82, 1e-9)
check("path F at 26% is 0.38", round(pnl_loop(zig(.26, 21))[0], 2), 0.38, 1e-9)
Np14 = [100.0]
r14 = .14 * sqrt(DT)
for k in range(252):
    Np14.append(round(Np14[-1] * exp(r14 if k % 2 == 0 else -r14), 4))
check("path N at 14% is -4.21", round(pnl_loop(Np14)[0], 2), -4.21, 1e-9)
check("path F at 14% is -1.06", round(pnl_loop(zig(.14, 21))[0], 2), -1.06, 1e-9)
check("path F ends 43% up", zig(.26, 21)[-1] / 100 - 1, .4338, 5e-4)
check("one-step test path [100, 105]: exact -5.6647", 5 - call(100, 100, 0, .2, 1) - Phi(.1) * 5, 5 - call_B(100, 100, 0, .2, 1) - (call_B(100.01, 100, 0, .2, 1) - call_B(99.99, 100, 0, .2, 1)) / .02 * 5, 1e-5)
check("transfer 47,556 and 47,634", 20000 * (call(100, 100, 0, .26, 1) - call(100, 100, 0, .2, 1)), 20000 * (call_B(100, 100, 0, .26, 1) - call_B(100, 100, 0, .2, 1)), 1e-2)

print("review-4 and homework-4")
check("review: S=64 s=25% T=.25 rule 3.20, BS 3.1895", call(64, 64, 0, .25, .25), call_B(64, 64, 0, .25, .25), 1e-7)
g50 = gamma_A(50, 50, 0, .25, .25)
check("review: gamma S=K=50 s=25% T=.25 is 0.0637", g50, gamma_B(50, 50, 0, .25, .25, .02), 1e-6)
check("review: theta a year -4.98", -.5 * .0625 * 2500 * g50, theta_B(50, 50, 0, .25, .25), 1e-4)
check("review: theta a day -0.01975", -.5 * .0625 * 2500 * g50 / 252, theta_B(50, 50, 0, .25, .25) / 252, 1e-6)
check("review: breakeven 0.7874", 50 * .25 / sqrt(252), 50 * .25 * sqrt(DT), 1e-12)
check("review: 10,000 options, £1.20 move: +261", 1e4 * (.5 * g50 * 1.44 - .5 * .0625 * 2500 * g50 / 252), 1e4 * (.5 * gamma_B(50, 50, 0, .25, .25, .02) * 1.44 + theta_B(50, 50, 0, .25, .25) / 252), .5)
check("review: no-half slip 522 (halves dropped from both terms)", 1e4 * (g50 * 1.44 - .0625 * 2500 * g50 / 252), 522.37, .02)
up_A = call(51.2, 50, 0, .25, .25 - DT) - call(50, 50, 0, .25, .25) - Phi(d12(50, 50, 0, .25, .25)[0]) * 1.2
dn_A = call(48.8, 50, 0, .25, .25 - DT) - call(50, 50, 0, .25, .25) + Phi(d12(50, 50, 0, .25, .25)[0]) * 1.2
dl_B = (call_B(50.01, 50, 0, .25, .25) - call_B(49.99, 50, 0, .25, .25)) / .02
up_B = call_B(51.2, 50, 0, .25, .25 - DT) - call_B(50, 50, 0, .25, .25) - dl_B * 1.2
dn_B = call_B(48.8, 50, 0, .25, .25 - DT) - call_B(50, 50, 0, .25, .25) + dl_B * 1.2
check("review: full revaluation up 10,000 x = 255 (stated £255)", 1e4 * up_A, 1e4 * up_B, .05)
check("review: full revaluation down 10,000 x = 271 (stated £271)", 1e4 * dn_A, 1e4 * dn_B, .05)
check("review: digital flat at the money 0.4602 and 0.5396", Phi(-.1) + 39.695 * .002, digital_B(100, 100, 0, .2, 1) + vega_B(100, 100, 0, .2, 1) * .002, 5e-5)
for S, K, r, s, T in ((100, 100, .05, .2, 1), (100, 100, 0, .2, 1), (100, 130, .05, .2, 1), (100, 80, .03, .25, .5), (50, 50, .02, .3, .25)):
    rule_ = .4 * s * sqrt(T) * S + .5 * (S - K * exp(-r * T))
    check(f"hw1 rule_with_rate{(S, K, r, s, T)}: exact", call(S, K, r, s, T), call_B(S, K, r, s, T), 1e-7)
    check(f"hw1   error = rule - exact", rule_ - call(S, K, r, s, T), rule_ - call_B(S, K, r, s, T), 1e-7)
# hw5: the barrier-99 knock-out (0.9646, Reiner-Rubinstein against bridge Monte Carlo 0.9669) is checked in check_l4.py
check("hw8 rule 16.29 and BS 16.2377", call(320, 320, 0, .18, .5), call_B(320, 320, 0, .18, .5), 1e-6)
check("hw8 rule 0.4 s sqrt(T) S", .4 * .18 * sqrt(.5) * 320, 16.29174, 1e-4)
check("hw8 3-point rise: BS 2.7017", call(320, 320, 0, .21, .5) - call(320, 320, 0, .18, .5), call_B(320, 320, 0, .21, .5) - call_B(320, 320, 0, .18, .5), 1e-6)
check("hw8 rule / sigma x 0.03 = 2.7153", .4 * .18 * sqrt(.5) * 320 / .18 * .03, 2.71529, 1e-4)
check("hw8 short 500: +1,351.75", 500 * (call(320, 320, 0, .18, .5) - call(320, 320, 0, .15, .5)), 500 * (call_B(320, 320, 0, .18, .5) - call_B(320, 320, 0, .15, .5)), .05)
check("hw8 no-root key 11.52", .4 * .18 * .5 * 320, 11.52, 1e-9)
check("hw7 BS(0.15) - BS(0.20) = -1.9870", call(100, 100, 0, .15, 1) - call(100, 100, 0, .2, 1), call_B(100, 100, 0, .15, 1) - call_B(100, 100, 0, .2, 1), 1e-7)
check("hw7 vega x gap -1.98", 39.695 * -.05, -1.98475, 1e-5)
check("hw7 actual daily move 0.94", 100 * .15 / sqrt(252), 100 * .15 * sqrt(DT), 1e-12)
check("hw2 price gap 26% 2.3778, 18% -0.7943, 25% vs 30% -1.9759", (call(100, 100, 0, .26, 1) - call(100, 100, 0, .2, 1), call(100, 100, 0, .18, 1) - call(100, 100, 0, .2, 1), call(100, 100, 0, .25, 1) - call(100, 100, 0, .3, 1))[2],
      call_B(100, 100, 0, .25, 1) - call_B(100, 100, 0, .3, 1), 1e-7)
check("hw6 delta at the money 0.5398; vega one day 2.51 against 39.70", vega_A(100, 100, 0, .2, 1 / 252), vega_B(100, 100, 0, .2, 1 / 252), 1e-4)

# ---- Fix pass (2026-11-05): Asian figures settled by a third method, review-4 fresh inputs ----
# Convention (l17 screens 3, 8, 9): r = 0, S = K = 100, sigma = 20%, T = 1, n fixings at t = i/n, i = 1..n, average of the n closes.
# Method A: Monte Carlo with a geometric-average control variate (exact lognormal mean for the control), batch standard errors.
# Method B: plain antithetic Monte Carlo (no control variate) with another seed; agreement within four of its standard errors.
def asian_cv(n, N, B, seed):
    rng = np.random.default_rng(seed)
    t = np.arange(1, n + 1) / n
    v = (0.04 * np.minimum.outer(t, t)).mean()
    m = log(100) - .5 * .04 * t.mean()
    sd = sqrt(v)
    gp = exp(m + v / 2) * Phi((m + v - log(100)) / sd) - 100 * Phi((m + v - log(100)) / sd - sd)
    est = []
    for _ in range(B):
        z = rng.standard_normal((N // B // 2, n))
        z = np.vstack([z, -z])
        ls = np.cumsum(-.5 * .04 / n + .2 * sqrt(1 / n) * z, axis=1) + log(100)
        a = np.maximum(np.exp(ls).mean(1) - 100, 0)
        g = np.maximum(np.exp(ls.mean(1)) - 100, 0)
        c = np.cov(a, g)[0, 1] / g.var()
        est.append((a - c * (g - gp)).mean())
    est = np.array(est)
    return est.mean(), est.std(ddof=1) / sqrt(B)


def asian_plain(n, N, seed):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((N // 2, n))
    z = np.vstack([z, -z])
    ls = np.cumsum(-.5 * .04 / n + .2 * sqrt(1 / n) * z, axis=1) + log(100)
    a = np.maximum(np.exp(ls).mean(1) - 100, 0)
    return a.mean(), a.std(ddof=1) / sqrt(len(a))


for n, stated, N in ((12, 4.8887, 1_000_000), (52, 4.6687, 1_000_000), (252, 4.6159, 1_000_000)):
    mA, seA = asian_cv(n, 2_000_000, 20, 101 + n)
    mB, seB = asian_plain(n, N, 202 + n)
    check(f"l17 Asian {n} fixings: control-variate MC {mA:.4f} (se {seA:.4f}) against stated {stated}", mA, stated, 4 * seA + 5e-5)
    check(f"l17 Asian {n} fixings: plain MC {mB:.4f} (se {seB:.4f}) against control-variate MC", mB, mA, 4 * seB)
check("l17 12-fixing vol share 0.614 = 4.8887 / 7.9656", 4.8887 / 7.9656, 0.614, 5e-4)
check("l17 daily Asian £4.62 against vanilla / sqrt3 4.60: within 0.03", 4.6159, call(100, 100, 0, .2, 1) / sqrt(3), 0.03)
check("l17 screen 3 key 4.6 tol 0.1 accepts 4.62 and rejects the half slip 3.98", 4.6159 - 4.6, 0.0, 0.1)
# review-4 fresh inputs
r_, s_, T_ = .05, .2, 1.
d1_, d2_ = d12(100, 95, r_, s_, T_)
exp_ = exp(-r_ * T_)
check("review-4 digital at 95: d2 0.4065", d2_, (log(100 / 95) + .03) / .2, 1e-12)
check("review-4 digital at 95: 0.9512 x 0.6578 = 0.6257", exp_ * Phi(d2_), exp_ * ndtr(d2_), 1e-12)
check("review-4 digital at 95: price key 0.6257", exp_ * Phi(d2_), .6257, 5e-5)
check("review-4 digital at 95: no-discount slip 0.6578", Phi(d2_), .6578, 5e-5)
check("review-4 digital at 95: put slip 0.3255", exp_ * Phi(-d2_), .3255, 5e-5)
check("review-4 digital at 95: put slip by 1 - call", exp_ - exp_ * Phi(d2_), exp_ * ndtr(-d2_), 1e-12)
check("review-4 breakeven £40 at 35%: 40 x 0.35 / sqrt(252) = 0.8819", 40 * .35 / sqrt(252), 40 * .35 * sqrt(1 / 252), 1e-12)
check("review-4 breakeven key 0.88 (tol 0.01) against 0.8819", .8819, .88, .01)
check("review-4 breakeven annual slip 14 = 40 x 0.35", 40 * .35, 14, 1e-12)
check("review-4 gamma part 3: key 261 tol 7 accepts full revaluation 255 (rejects 522)", 261 - 255, 6, 7)
check("homework-4 part 3.0: d2 = (ln(100/110) - 0.0162) / 0.18 = -0.6195", (log(100 / 110) - .0162) / .18, -0.6195, 5e-5)
check("homework-4 part 3.0: Phi(-0.6195) = 0.2678", Phi(-0.6195), ndtr(-0.6195), 1e-12)
check("l16 screen 4: 0.1072 - 12.95 x 0.002 = 0.0813", .1072 - 12.95 * .002, .0813, 1e-4)
check("l17 screen 7: up-and-out vanilla at 90/100, 20%, 1y, r = 0 is 3.59", call(90, 100, 0, .2, 1), call_B(90, 100, 0, .2, 1), 1e-7)
check("l17 screen 7: the vanilla slip 3.59", call(90, 100, 0, .2, 1), 3.59, 5e-3)
check("l15 screen 1: reversed spread -0.5323", -(call(100, 99.5, .05, .2, 1) - call(100, 100.5, .05, .2, 1)), -(call_B(100, 99.5, .05, .2, 1) - call_B(100, 100.5, .05, .2, 1)), 1e-6)
check("l15 screen 8: tol 5000 around 1,064,650 excludes 1,119,235 and 1,211,544", 1119235 - 1064650 > 5000 and 1211544 - 1064650 > 5000, True, 0)

print()
print(f"{'PASS' if not fails else 'FAIL'}: {n_ok + len(fails)} checks, {n_ok} ok, {len(fails)} failed")
for f in fails:
    print("   ", f)
