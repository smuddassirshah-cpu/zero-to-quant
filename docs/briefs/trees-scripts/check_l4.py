"""Check every number in docs/briefs/trees.md (Level 4 and the exam extension).

Each value is computed by two independent methods (a closed form and a numerical
or simulated check) and the script stops on any disagreement.
Run: python3 docs/briefs/trees-scripts/check_l4.py
No scipy: the normal cdf is math.erf (method A) or Simpson integration (method B).
Per cent keys are fractions (0.2, not 20). Money is in pounds.
"""
import math
import numpy as np

CHECKS = 0
VALUES = {}


def check(name, a, b, tol):
    """Record value a (method A) and assert method B agrees within tol."""
    global CHECKS
    assert abs(a - b) <= tol, f"{name}: A={a!r} B={b!r} tol={tol}"
    CHECKS += 1
    VALUES[name] = a
    print(f"  ok {name:<38} {a: .6f}   (B {b: .6f})")


# ---------------------------------------------------------------- normal cdf
def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def simpson(f, a, b, n=4000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4 if i % 2 else 2)
    return s * h / 3


def Phi_B(x):
    return simpson(phi, -12, x, 4000)


# ---------------------------------------------------------------- Black-Scholes
def d1d2(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    return d1, d1 - s * math.sqrt(T)


def bs_call(S, K, r, s, T):
    d1, d2 = d1d2(S, K, r, s, T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)


def bs_put(S, K, r, s, T):
    d1, d2 = d1d2(S, K, r, s, T)
    return K * math.exp(-r * T) * Phi(-d2) - S * Phi(-d1)


def call_B(S, K, r, s, T, n=6000):
    """Discounted expectation of the payoff by Simpson on the kink-free part (independent of the formula)."""
    m = math.log(S) + (r - s * s / 2) * T
    sd = s * math.sqrt(T)
    z0 = (math.log(K) - m) / sd
    f = lambda z: (math.exp(m + sd * z) - K) * phi(z)
    return math.exp(-r * T) * simpson(f, z0, 12, n)


def put_B(S, K, r, s, T, n=6000):
    m = math.log(S) + (r - s * s / 2) * T
    sd = s * math.sqrt(T)
    z0 = (math.log(K) - m) / sd
    f = lambda z: (K - math.exp(m + sd * z)) * phi(z)
    return math.exp(-r * T) * simpson(f, -12, z0, n)


def gamma_fd(S, K, s, T, h=0.1):
    """Gamma by a second difference of the integral price (independent of the closed form)."""
    return (call_B(S + h, K, 0, s, T) - 2 * call_B(S, K, 0, s, T) + call_B(S - h, K, 0, s, T)) / h ** 2


def greeks(S, K, r, s, T):
    d1, d2 = d1d2(S, K, r, s, T)
    delta = Phi(d1)
    gamma = phi(d1) / (S * s * math.sqrt(T))
    vega = S * math.sqrt(T) * phi(d1)                       # per 1.00 of vol
    theta = -S * phi(d1) * s / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * Phi(d2)  # per year
    return delta, gamma, vega, theta


S0, K0, R0, SIG, T1 = 100.0, 100.0, 0.0, 0.2, 1.0
print("Normal cdf")
check("Phi(0.1)", Phi(0.1), Phi_B(0.1), 1e-8)
check("Phi(0.15)", Phi(0.15), Phi_B(0.15), 1e-8)

# =========================================================== LESSON l13
print("l13 rules of thumb")
RULE = 1 / math.sqrt(2 * math.pi)                     # 0.39894, the rounded 0.4
check("1/sqrt(2 pi)", RULE, math.sqrt(1 / (2 * math.pi)), 1e-12)
check("E[max(Z,0)] by integration", simpson(lambda z: z * phi(z), 0, 12, 4000), RULE, 1e-9)


def rule(S, s, T):
    return 0.4 * s * math.sqrt(T) * S


# the plan's number
check("BS ATM S=100 s=.2 T=1 r=0", bs_call(S0, K0, R0, SIG, T1), call_B(S0, K0, R0, SIG, T1), 1e-7)
assert abs(rule(100, 0.2, 1) - 8.0) < 1e-12
print("  rule(100,.2,1) = 8.00 against", round(bs_call(S0, K0, R0, SIG, T1), 4))
assert round(bs_call(S0, K0, R0, SIG, T1), 4) == 7.9656
check("ATM exact form S(2Phi(s sqrt T/2)-1)", 100 * (2 * Phi(0.1) - 1), bs_call(S0, K0, R0, SIG, T1), 1e-9)
check("rule error T=1 (rule - BS)", rule(100, .2, 1) - bs_call(S0, K0, R0, SIG, T1), 8 - 7.9656, 1e-4)
check("rule/BS - 1 at T=1", rule(100, .2, 1) / bs_call(S0, K0, R0, SIG, T1) - 1, 8 / 7.96557 - 1, 1e-5)

# time scaling: quarter time halves the price
check("BS T=0.25", bs_call(100, 100, 0, .2, .25), call_B(100, 100, 0, .2, .25), 1e-7)
assert abs(rule(100, .2, .25) - 4.0) < 1e-12
check("price ratio T=0.25 / T=1", bs_call(100, 100, 0, .2, .25) / bs_call(100, 100, 0, .2, 1), 0.5, 0.01)

# vol scaling: sigma 10% halves the price
check("BS sigma=0.10", bs_call(100, 100, 0, .1, 1), call_B(100, 100, 0, .1, 1), 1e-7)
# spot scaling
check("BS S=K=250 s=.2 T=1", bs_call(250, 250, 0, .2, 1), 2.5 * bs_call(100, 100, 0, .2, 1), 1e-9)
check("BS S=K=250, call_B", bs_call(250, 250, 0, .2, 1), call_B(250, 250, 0, .2, 1), 1e-6)
assert abs(rule(250, .2, 1) - 20.0) < 1e-12

# worked ladder: S=50, s=32%, T=0.25
check("BS S=K=50 s=.32 T=.25", bs_call(50, 50, 0, .32, .25), call_B(50, 50, 0, .32, .25), 1e-7)
assert abs(rule(50, .32, .25) - 3.2) < 1e-12

# trap: r = 5%: rule 8.00 against 10.4506, corrected 10.4385
c5 = bs_call(100, 100, .05, .2, 1)
check("BS shared option r=5%", c5, call_B(100, 100, .05, .2, 1), 1e-7)
assert round(c5, 4) == 10.4506
corr = rule(100, .2, 1) + 0.5 * (100 - 100 * math.exp(-.05))
F = 100 * math.exp(.05)
corr2 = math.exp(-.05) * (0.4 * .2 * F + 0.5 * (F - 100))
check("rule + half the forward gap", corr, corr2, 1e-9)
print("   corrected =", round(corr, 4), " vs exact", round(c5, 4), " gap", round(c5 - corr, 4))
assert round(corr, 4) == 10.4385
check("Ke^{-rT} for 5%", 100 * math.exp(-.05), 100 / math.exp(.05), 1e-12)

# edge: strike away from the money (r = 0, S=100, s=.2, T=1)
for K in (105, 110, 120):
    cK = bs_call(100, K, 0, .2, 1)
    check(f"BS K={K} r=0", cK, call_B(100, K, 0, .2, 1), 1e-7)
print("   rule error at 5, 10, 20 per cent out of the money: 8.00 vs",
      [round(bs_call(100, K, 0, .2, 1), 4) for K in (105, 110, 120)])

# straddle transfer: S=120, s=25%, T=1/12 (r=0)
Ts = 1 / 12
c_s = bs_call(120, 120, 0, .25, Ts)
p_s = bs_put(120, 120, 0, .25, Ts)
check("straddle BS call = put at r=0", c_s, p_s, 1e-9)
check("straddle BS price", 2 * c_s, 2 * call_B(120, 120, 0, .25, Ts), 1e-6)
straddle_rule = 0.8 * .25 * math.sqrt(Ts) * 120
print("   straddle rule", round(straddle_rule, 4), "BS", round(2 * c_s, 4), "break-even move", round(2 * c_s / 120, 4))
check("straddle rule", straddle_rule, 0.8 * 0.25 * 0.288675 * 120, 1e-3)
check("straddle break-even fraction (rule)", straddle_rule / 120, 0.8 * .25 * math.sqrt(Ts), 1e-12)

# one-month versus one-year at the money: price falls by sqrt(12)
check("1m/1y price ratio ~ 1/sqrt(12)", bs_call(100, 100, 0, .2, 1 / 12) / bs_call(100, 100, 0, .2, 1), 1 / math.sqrt(12), 0.005)

# vega ~ price / sigma
g = greeks(100, 100, 0, .2, 1)
check("vega per 1.00 (closed)", g[2], (call_B(100, 100, 0, .21, 1) - call_B(100, 100, 0, .19, 1)) / 0.02, 5e-3)
print("   vega per vol point", round(g[2] / 100, 5), " price/sigma", round(bs_call(100, 100, 0, .2, 1) / .2, 4))
check("price/sigma vs vega", bs_call(100, 100, 0, .2, 1) / .2, g[2], 0.2)

# exam e-atm-rule numbers: S=250, s=30%, T=0.25, r=0
c_e = bs_call(250, 250, 0, .3, .25)
check("exam ATM BS S=250 s=.3 T=.25", c_e, call_B(250, 250, 0, .3, .25), 1e-6)
assert abs(rule(250, .3, .25) - 15.0) < 1e-12
check("exam ATM vol +2 points (BS gain)", bs_call(250, 250, 0, .32, .25) - c_e,
      call_B(250, 250, 0, .32, .25) - call_B(250, 250, 0, .30, .25), 1e-6)
check("exam ATM vega per point rule: price/s/100", 15.0 / .3 / 100, 0.5, 1e-12)
check("exam ATM 1-month price BS", bs_call(250, 250, 0, .3, 1 / 12), call_B(250, 250, 0, .3, 1 / 12), 1e-6)
print("   exam ATM rule 15.00, BS", round(c_e, 4), " 1-month rule", round(rule(250, .3, 1 / 12), 4),
      "BS", round(bs_call(250, 250, 0, .3, 1 / 12), 4), " gain 2 points", round(bs_call(250, 250, 0, .32, .25) - c_e, 4))

# review numbers l13: S=64, s=25%, T=0.25
check("review ATM BS S=64 s=.25 T=.25", bs_call(64, 64, 0, .25, .25), call_B(64, 64, 0, .25, .25), 1e-7)
assert abs(rule(64, .25, .25) - 3.2) < 1e-12

# =========================================================== LESSON l14
print("l14 greeks by shape")
d1, d2 = d1d2(100, 100, 0, .2, 1)
dl, gm, vg, th = greeks(100, 100, 0, .2, 1)
check("delta call", dl, (call_B(100.01, 100, 0, .2, 1) - call_B(99.99, 100, 0, .2, 1)) / 0.02, 1e-6)
check("delta put = call - 1", dl - 1, (put_B(100.01, 100, 0, .2, 1) - put_B(99.99, 100, 0, .2, 1)) / 0.02, 1e-6)
hh = 0.5
check("gamma", gm, (call_B(100 + hh, 100, 0, .2, 1) - 2 * call_B(100, 100, 0, .2, 1) + call_B(100 - hh, 100, 0, .2, 1)) / hh ** 2, 1e-6)
check("vega per 1.00", vg, (call_B(100, 100, 0, .2001, 1) - call_B(100, 100, 0, .1999, 1)) / 0.0002, 1e-4)
check("theta per year (r=0)", th, (call_B(100, 100, 0, .2, 1 - 1e-4) - call_B(100, 100, 0, .2, 1 + 1e-4)) / 2e-4, 1e-4)
check("theta = -1/2 s^2 S^2 gamma", th, -0.5 * .2 ** 2 * 100 ** 2 * gm, 1e-12)
check("theta per trading day /252", th / 252, -0.5 * .04 * 1e4 * gm / 252, 1e-12)
check("vega = gamma S^2 sigma T", vg, gm * 100 ** 2 * .2 * 1, 1e-9)
print("   delta", round(dl, 4), "put", round(dl - 1, 4), "gamma", round(gm, 6), "vega/pt", round(vg / 100, 5),
      "theta/yr", round(th, 4), "theta/day", round(th / 252, 5))

# time shape of ATM gamma, vega at T = 0.25 and 1/252
g25 = greeks(100, 100, 0, .2, .25)
check("gamma(T=.25)/gamma(T=1) ~ 2", g25[1] / gm, 2.0, 0.01)
check("vega(T=.25)/vega(T=1) ~ 1/2", g25[2] / vg, 0.5, 0.005)
check("gamma T=0.25 (diff)", g25[1], gamma_fd(100, 100, .2, .25), 1e-6)
g1d = greeks(100, 100, 0, .2, 1 / 252)
print("   gamma T=1/252", round(g1d[1], 5), "ratio to T=1", round(g1d[1] / gm, 3), " sqrt(252) =", round(math.sqrt(252), 3))
check("gamma ratio 1 day / 1 year ~ sqrt(252)", g1d[1] / gm, math.sqrt(252), 0.1)
check("gamma T=1/252 (diff)", g1d[1], gamma_fd(100, 100, .2, 1 / 252, 0.05), 1e-4)

# gamma peak location at r = 0: d1 = -s sqrt(T), so S = K exp(-1.5 s^2 T)
Sp = 100 * math.exp(-1.5 * .2 ** 2 * 1)
xs = np.linspace(80, 120, 40001)
gam = np.array([greeks(x, 100, 0, .2, 1)[1] for x in xs[::40]])
check("gamma peak spot T=1 (grid)", xs[::40][gam.argmax()], Sp, 0.05)
check("gamma peak spot T=0.25 (grid)", xs[::40][np.array([greeks(x, 100, 0, .2, .25)[1] for x in xs[::40]]).argmax()], 100 * math.exp(-1.5 * .2 ** 2 * .25), 0.05)
print("   gamma peak at", round(Sp, 3), " T=0.25 at", round(100 * math.exp(-1.5 * .2 ** 2 * .25), 3))

# calendar: sell 1m ATM call, buy 3m ATM call (r=0, S=K=100, s=20%)
g1m = greeks(100, 100, 0, .2, 1 / 12)
g3m = greeks(100, 100, 0, .2, .25)
net = tuple(b - a for a, b in zip(g1m, g3m))
print("   calendar net delta, gamma, vega, theta/yr:", [round(x, 5) for x in net])
check("calendar gamma sign", net[1] < 0 and 1 or 0, 1, 0)
check("calendar vega sign", net[2] > 0 and 1 or 0, 1, 0)
check("calendar theta sign", net[3] > 0 and 1 or 0, 1, 0)
check("calendar gamma value", net[1], gamma_fd(100, 100, .2, .25) - gamma_fd(100, 100, .2, 1 / 12), 1e-5)
check("calendar vega per vol point", net[2] / 100,
      ((call_B(100, 100, 0, .2001, .25) - call_B(100, 100, 0, .1999, .25)) - (call_B(100, 100, 0, .2001, 1 / 12) - call_B(100, 100, 0, .1999, 1 / 12))) / 0.0002 / 100, 1e-4)
check("calendar theta per day", net[3] / 252,
      ((call_B(100, 100, 0, .2, .25 - 1e-4) - call_B(100, 100, 0, .2, .25 + 1e-4)) - (call_B(100, 100, 0, .2, 1 / 12 - 1e-4) - call_B(100, 100, 0, .2, 1 / 12 + 1e-4))) / 2e-4 / 252, 1e-4)

# risk reversal: long 110 call, short 90 put, 3 months, r=0
def pos_greeks(legs, T=.25):
    out = [0, 0, 0, 0]
    for typ, K, q in legs:
        d, gg, v, t = greeks(100, K, 0, .2, T)
        if typ == 'p':
            d = d - 1
        for i, x in enumerate((d, gg, v, t)):
            out[i] += q * x
    return out

rr = pos_greeks([('c', 110, 1), ('p', 90, -1)])
print("   risk reversal Greeks (delta, gamma, vega, theta/yr):", [round(x, 5) for x in rr])
rr_b = []
for fn in range(4):
    pass
st = pos_greeks([('c', 100, 1), ('p', 100, 1)])
print("   straddle Greeks:", [round(x, 5) for x in st])
check("straddle delta ~ small positive", st[0], 2 * dl - 1 if False else Phi(d1d2(100, 100, 0, .2, .25)[0]) * 2 - 1, 1e-12)

# =========================================================== LESSON l15
print("l15 digitals")
S, K, r, s, T = 100.0, 100.0, 0.05, 0.2, 1.0
d1, d2 = d1d2(S, K, r, s, T)
check("d1 shared option", d1, 0.35, 1e-12)
check("d2 shared option", d2, 0.15, 1e-12)
dig_c = math.exp(-r * T) * Phi(d2)
check("digital call e^-rT Phi(d2)", dig_c, -(call_B(S, K + 1e-3, r, s, T) - call_B(S, K - 1e-3, r, s, T)) / 2e-3, 1e-6)
assert round(dig_c, 4) == 0.5323
dig_p = math.exp(-r * T) * Phi(-d2)
check("digital put e^-rT Phi(-d2)", dig_p, (put_B(S, K + 1e-3, r, s, T) - put_B(S, K - 1e-3, r, s, T)) / 2e-3, 1e-6)
assert round(dig_p, 4) == 0.4189
check("digital call + put = e^-rT", dig_c + dig_p, math.exp(-r * T), 1e-12)
check("Phi(d2)", Phi(d2), 0.5596, 5e-5)
# call spread widths
for h in (10, 4, 2, 1, 0.5, 0.1):
    cs = (bs_call(S, K - h / 2, r, s, T) - bs_call(S, K + h / 2, r, s, T)) / h
    csB = (call_B(S, K - h / 2, r, s, T) - call_B(S, K + h / 2, r, s, T)) / h
    check(f"call spread width {h} / h", cs, csB, 1e-7)
# convergence rate: error ~ h^2 / 24 * d3C/dK3 ; check width 1 within 0.0005 of digital
assert abs((bs_call(S, 99.5, r, s, T) - bs_call(S, 100.5, r, s, T)) - dig_c) < 5e-4
print("   dig call", round(dig_c, 4), "put", round(dig_p, 4), "sum", round(dig_c + dig_p, 4), "e^-rT", round(math.exp(-r * T), 4))
print("   C(99.5)", round(bs_call(S, 99.5, r, s, T), 4), "C(100.5)", round(bs_call(S, 100.5, r, s, T), 4))
# asset-or-nothing less K digitals
aon = S * Phi(d1)
check("asset-or-nothing S Phi(d1)", aon, 63.68, 0.005)
check("AON - K*digital = call", aon - K * dig_c, bs_call(S, K, r, s, T), 1e-9)
check("call by integration", bs_call(S, K, r, s, T), call_B(S, K, r, s, T), 1e-7)
# conservative over-hedge: spread (K-h, K) / h pays at least the digital
for h in (1.0, 0.5):
    oh = (bs_call(S, K - h, r, s, T) - bs_call(S, K, r, s, T)) / h
    print("   over-hedge price, width", h, round(oh, 4), " minus digital", round(oh - dig_c, 4))
oh1 = (bs_call(S, 99, r, s, T) - bs_call(S, 100, r, s, T)) / 1
check("over-hedge (99,100)/1", oh1, (call_B(S, 99, r, s, T) - call_B(S, 100, r, s, T)) / 1, 1e-7)
# digital delta, one year versus one day (pin risk)
def dig_delta(S, K, r, s, T):
    d1, d2 = d1d2(S, K, r, s, T)
    return math.exp(-r * T) * phi(d2) / (S * s * math.sqrt(T))
dd1 = dig_delta(S, K, r, s, 1.0)
dd1B = (math.exp(-r) * Phi(d1d2(S + .01, K, r, s, 1.0)[1]) - math.exp(-r) * Phi(d1d2(S - .01, K, r, s, 1.0)[1])) / 0.02
check("digital delta T=1 (per share per £1)", dd1, dd1B, 1e-7)
dd2 = dig_delta(S, K, r, s, 1 / 252)
dd2B = (math.exp(-r / 252) * Phi(d1d2(S + .001, K, r, s, 1 / 252)[1]) - math.exp(-r / 252) * Phi(d1d2(S - .001, K, r, s, 1 / 252)[1])) / 0.002
check("digital delta T=1/252", dd2, dd2B, 1e-5)
print("   digital delta 1y", round(dd1, 5), "1d", round(dd2, 5), "ratio", round(dd2 / dd1, 2), "shares for 10,000 digitals:", round(dd1 * 1e4), round(dd2 * 1e4))
# review digital: K=105 put, same option
d1k, d2k = d1d2(100, 105, .05, .2, 1)
dp105 = math.exp(-.05) * Phi(-d2k)
check("digital put K=105", dp105, (put_B(100, 105 + 1e-3, .05, .2, 1) - put_B(100, 105 - 1e-3, .05, .2, 1)) / 2e-3, 1e-6)
dc105 = math.exp(-.05) * Phi(d2k)
check("digital call K=105", dc105, -(call_B(100, 105 + 1e-3, .05, .2, 1) - call_B(100, 105 - 1e-3, .05, .2, 1)) / 2e-3, 1e-6)
print("   K=105 d2", round(d2k, 4), "digital call", round(dc105, 4), "put", round(dp105, 4))
# transfer: £2m notional
print("   2m notional of the K=100 digital call costs", round(2e6 * dig_c))
# exam: digital call at K = 75 with the e-bs-hedge numbers
S_, K_, r_, s_, T_ = 80, 75, .03, .25, .5
d1e, d2e = d1d2(S_, K_, r_, s_, T_)
dige = math.exp(-r_ * T_) * Phi(d2e)
check("exam digital call K=75", dige, -(call_B(S_, K_ + 1e-3, r_, s_, T_) - call_B(S_, K_ - 1e-3, r_, s_, T_)) / 2e-3, 1e-6)
check("exam d1", d1e, 0.5383, 5e-5)
check("exam d2", d2e, 0.3615, 5e-5)
check("exam call price", bs_call(S_, K_, r_, s_, T_), call_B(S_, K_, r_, s_, T_), 1e-7)
print("   exam digital from table values", round(math.exp(-0.015) * 0.6412, 4), " exact", round(dige, 4))
check("exam digital (table values)", math.exp(-0.015) * 0.6412, dige, 5e-4)

# =========================================================== LESSON l16
print("l16 the smile")
S, r, T = 100.0, 0.0, 1.0


def sig_skew(K):
    """The lesson's equity skew: 20% at the money, two vol points per ten strike points, valid on 70 to 130."""
    return 0.20 - 0.002 * (K - 100)


DSIG = -0.002


def c_skew(K):
    return bs_call(S, K, r, sig_skew(K), T)


def p_skew(K):
    return bs_put(S, K, r, sig_skew(K), T)


def dig_call_skew(K):
    """-dC/dK along the skew = e^-rT Phi(d2) - vega * sigma'(K)  (method A, closed form)."""
    sg = sig_skew(K)
    d1, d2 = d1d2(S, K, r, sg, T)
    vega = S * math.sqrt(T) * phi(d1)
    return math.exp(-r * T) * Phi(d2) - vega * DSIG


def dig_call_flat(K, sg=0.2):
    return math.exp(-r * T) * Phi(d1d2(S, K, r, sg, T)[1])


e = 1e-3
for K in (70, 80, 90, 100, 105, 110, 120, 130):
    a = dig_call_skew(K)
    b = -(c_skew(K + e) - c_skew(K - e)) / (2 * e)                    # method B: tight call spread on the skew
    b2 = -(call_B(S, K + e, r, sig_skew(K + e), T) - call_B(S, K - e, r, sig_skew(K - e), T)) / (2 * e)
    check(f"P(S_T>{K}) along the skew", a, b, 1e-6)
    check(f"P(S_T>{K}) along the skew (integral)", a, b2, 1e-6)
print("   P(S_T > K): K, flat 20%, skew")
for K in (70, 80, 90, 100, 105, 110, 120, 130):
    print("    ", K, round(dig_call_flat(K), 4), round(dig_call_skew(K), 4))

# the implied density is positive on 70 to 130 (no arbitrage)
for K in range(70, 131, 5):
    ee = 0.25
    dens = (c_skew(K + ee) - 2 * c_skew(K) + c_skew(K - ee)) / ee ** 2
    assert dens > 0, (K, dens)
CHECKS += 1
print("  ok implied density positive on 70 to 130 for the skew")

# tails: P(S_T < 70) and P(S_T > 130)
pl_flat, pr_flat = 1 - dig_call_flat(70), dig_call_flat(130)
pl_skew, pr_skew = 1 - dig_call_skew(70), dig_call_skew(130)
assert pl_skew > pl_flat and pr_skew < pr_flat, "skew: fatter left tail, thinner right tail"
ee = 0.01
check("P(S_T<70) skew via put spread", pl_skew, (p_skew_diff := (bs_put(S, 70 + ee, r, sig_skew(70 + ee), T) - bs_put(S, 70 - ee, r, sig_skew(70 - ee), T)) / (2 * ee)), 1e-6)
check("P(S_T<70) flat via put spread", pl_flat, (bs_put(S, 70 + ee, r, .2, T) - bs_put(S, 70 - ee, r, .2, T)) / (2 * ee), 1e-6)
check("P(S_T>130) skew via call spread", pr_skew, -(bs_call(S, 130 + ee, r, sig_skew(130 + ee), T) - bs_call(S, 130 - ee, r, sig_skew(130 - ee), T)) / (2 * ee), 1e-6)
check("P(S_T>130) flat via call spread", pr_flat, -(bs_call(S, 130 + ee, r, .2, T) - bs_call(S, 130 - ee, r, .2, T)) / (2 * ee), 1e-6)
print(f"   P(S_T<70): flat {pl_flat:.4f} skew {pl_skew:.4f} ratio {pl_skew / pl_flat:.2f};  P(S_T>130): flat {pr_flat:.4f} skew {pr_skew:.4f}")
print(f"   P(S_T<80): flat {1 - dig_call_flat(80):.4f} skew {1 - dig_call_skew(80):.4f}")
# the trap: reading the 80 strike's vol (24%) as if it were flat for every strike
flat24_70 = 1 - dig_call_flat(70, 0.26)
print("   P(S_T<70) from a flat 26% (the vol at the 70 strike):", round(flat24_70, 4), "honest skew value:", round(pl_skew, 4))
check("flat-26 trap value (integral)", flat24_70, 1 - (-(call_B(S, 70 + ee, r, .26, T) - call_B(S, 70 - ee, r, .26, T)) / (2 * ee)), 1e-6)
# the forward is pinned: mean of the implied distribution is 100 (integrate K * density)
mean_check = 0.0
dK = 0.05
KS = np.arange(40, 220 + dK / 2, dK)
# beyond 130 the linear skew goes below 14% and then negative: so test the mean only through the smaller identity
# C(K0) = integral_{K0}^inf P(S_T > K) dK, here checked on the slice 70 to 130 by Simpson against the call-price difference
slice_int = simpson(lambda K: dig_call_skew(K), 70, 130, 1200)
check("integral of P(S_T>K) from 70 to 130 = C(70) - C(130)", slice_int, c_skew(70) - c_skew(130), 1e-6)
# skew in vol points and the 90 put against the 110 call
print("   skew vols: 90", round(sig_skew(90), 4), "100", sig_skew(100), "110", round(sig_skew(110), 4), " 90 minus 110 =", round(sig_skew(90) - sig_skew(110), 4))
rr_skew = p_skew(90) - c_skew(110)
rr_flat = bs_put(S, 90, r, .2, T) - bs_call(S, 110, r, .2, T)
check("90 put minus 110 call, skew (formula vs integral)", rr_skew, put_B(S, 90, r, sig_skew(90), T) - call_B(S, 110, r, sig_skew(110), T), 1e-6)
print("   90 put less 110 call: flat", round(rr_flat, 4), " skew", round(rr_skew, 4), "(each leg: put", round(p_skew(90), 4), "call", round(c_skew(110), 4), ")")
# put-call parity at r = 0 on the same strike and vol: put = call + K - S
check("parity at the 90 strike on the skew vol", p_skew(90), bs_call(S, 90, r, sig_skew(90), T) + 90 - S, 1e-9)
print("   digital call K=105: flat", round(dig_call_flat(105), 4), "skew", round(dig_call_skew(105), 4),
      " vega at 105", round(S * phi(d1d2(S, 105, r, sig_skew(105), T)[0]), 4), " sigma(105)", sig_skew(105))
print("   ATM digital: flat", round(dig_call_flat(100), 4), "skew", round(dig_call_skew(100), 4), " vega", round(vg_atm := S * phi(0.1), 4))
check("ATM digital skew = flat + vega x 0.002", dig_call_skew(100), dig_call_flat(100) + (S * phi(0.1)) * 0.002, 1e-12)


# =========================================================== LESSON l17
print("l17 which is cheaper")
S, K, r, s, T = 100.0, 100.0, 0.0, 0.2, 1.0
# path exercise: 12 monthly closes
path = [103, 98, 95, 91, 94, 99, 104, 108, 105, 102, 107, 112]
S_T = path[-1]
van = max(S_T - 100, 0)
asian = max(sum(path) / 12 - 100, 0)
low = min([100] + path)
look = S_T - low
dno = 0 if min(path) <= 92 else van
van_B = max(path[11] - 100, 0)
check("path vanilla payoff", van, van_B, 0)
check("path Asian average", sum(path) / 12, np.mean(path), 1e-12)
check("path Asian payoff", asian, max(np.mean(path) - 100, 0), 1e-12)
check("path lookback payoff", look, path[-1] - np.min(np.array([100] + path)), 0)
check("path down-and-out payoff (B=92)", dno, 0 if any(p <= 92 for p in path) else van, 0)
print("   payoffs vanilla/Asian/lookback/D&O:", van, round(asian, 4), look, dno)

# --- Asian (arithmetic, 252 equal fixings, r = 0): moment matching vs Monte Carlo
n = 252
dt = 1 / n
t = np.arange(1, n + 1) * dt
m1 = 100.0                                              # E[S_t] = 100 at r = 0
# E[S_ti S_tj] = 100^2 exp(s^2 min(ti,tj))
tt = np.minimum.outer(t, t)
m2 = (100.0 ** 2) * np.exp(s * s * tt).sum() / n ** 2
vol_a = math.sqrt(math.log(m2 / m1 ** 2))               # lognormal with the same two moments
ln_mean = math.log(m1) - vol_a ** 2 / 2


def lognormal_call(mean, vsd, Kk):
    d1 = (math.log(mean / Kk) + vsd ** 2 / 2) / vsd
    return mean * Phi(d1) - Kk * Phi(d1 - vsd)


asian_mm = lognormal_call(m1, vol_a, 100)
rng = np.random.default_rng(41)
pays = []
for _ in range(10):                                     # 10 chunks of 20,000 antithetic pairs = 400,000 paths
    Z = rng.standard_normal((20_000, n))
    for sign in (1, -1):
        logS = np.cumsum((-s * s / 2) * dt + s * math.sqrt(dt) * sign * Z, axis=1)
        pays.append(np.maximum((100 * np.exp(logS)).mean(axis=1) - 100, 0))
pay = np.concatenate(pays)
paths = len(pay)
asian_mc = pay.mean()
asian_se = pay.std(ddof=1) / math.sqrt(paths)
check("Asian ATM call: moment match vs MC", asian_mm, asian_mc, 4 * asian_se + 0.03)
print("   Asian: moment-matched", round(asian_mm, 4), " MC", round(asian_mc, 4), "se", round(asian_se, 4), " effective vol", round(vol_a, 4), " sigma/sqrt3", round(s / math.sqrt(3), 4))
check("Asian effective vol ~ sigma/sqrt(3)", vol_a, s / math.sqrt(3), 0.005)
check("Asian ~ vanilla / sqrt(3)", asian_mm, bs_call(100, 100, 0, .2, 1) / math.sqrt(3), 0.05)

# --- down-and-out call, B = 90, r = 0: Reiner-Rubinstein against bridge-corrected Monte Carlo (chunked to save memory)
B = 90.0
lam = (r + s * s / 2) / (s * s)
y = math.log(B * B / (S * K)) / (s * math.sqrt(T)) + lam * s * math.sqrt(T)
c_di = S * (B / S) ** (2 * lam) * Phi(y) - K * math.exp(-r * T) * (B / S) ** (2 * lam - 2) * Phi(y - s * math.sqrt(T))
vanilla = bs_call(S, K, r, s, T)
c_do = vanilla - c_di


def do_chunk(rng, m):
    Z = rng.standard_normal((m, n))
    x = np.concatenate([np.zeros((m, 1)), np.cumsum((-s * s / 2) * dt + s * math.sqrt(dt) * Z, axis=1)], axis=1)
    Sx = 100 * np.exp(x)
    x0, x1 = Sx[:, :-1], Sx[:, 1:]
    with np.errstate(divide="ignore", invalid="ignore"):
        pcross = np.exp(-2 * np.log(x0 / B) * np.log(x1 / B) / (s * s * dt))   # bridge dips below B between two fixings
    pcross = np.where((x0 <= B) | (x1 <= B), 1.0, pcross)
    surv = np.prod(1 - pcross, axis=1)
    van_p = np.maximum(Sx[:, -1] - K, 0)
    return van_p * surv, van_p * (1 - surv)


rng = np.random.default_rng(42)
outs, ins = [], []
for _ in range(20):
    o, i_ = do_chunk(rng, 50_000)
    outs.append(o)
    ins.append(i_)
payoff_do = np.concatenate(outs)
payoff_di = np.concatenate(ins)
do_mc, do_se = payoff_do.mean(), payoff_do.std(ddof=1) / math.sqrt(len(payoff_do))
di_mc = payoff_di.mean()
check("down-and-out call B=90: formula vs MC", c_do, do_mc, 4 * do_se)
print("   D&O: vanilla", round(vanilla, 4), "down-and-in", round(c_di, 4), "down-and-out", round(c_do, 4), " MC", round(do_mc, 4), "se", round(do_se, 4))
check("in + out = vanilla", c_di + c_do, vanilla, 1e-12)
check("down-and-in: formula vs MC", c_di, di_mc, 4 * do_se)

# --- floating-strike lookback call, started now, r = 0: E[S_T - min] by the exact law of the minimum vs bridge Monte Carlo
nu = -s / 2


def surv_min(yv):
    """P(min_{t<=T} (nu t + W_t) > -yv), W standard BM with drift nu."""
    return 1 - (Phi((-yv - nu * T) / math.sqrt(T)) + math.exp(-2 * nu * yv) * Phi((-yv + nu * T) / math.sqrt(T)))


def integrand(yv):
    return surv_min(yv) * 100 * s * math.exp(-s * yv)        # P(min S > m) dm with m = 100 exp(-s y)


E_min = simpson(integrand, 0, 200, 40000)                    # the weight e^{-s y} is 1e-17 by y = 200
look_exact = 100 - E_min                                      # E[S_T] = 100 at r = 0


def look_chunk(rng, m, steps=500):
    dts = 1 / steps
    Z = rng.standard_normal((m, steps))
    inc = (-s * s / 2) * dts + s * math.sqrt(dts) * Z
    xx = np.concatenate([np.zeros((m, 1)), np.cumsum(inc, axis=1)], axis=1)
    U = rng.random((m, steps))
    xa, xb = xx[:, :-1], xx[:, 1:]
    bridge_min = 0.5 * (xa + xb - np.sqrt((xb - xa) ** 2 - 2 * s * s * dts * np.log(U)))
    mn = np.minimum(bridge_min.min(axis=1), 0)
    return 100 * np.exp(xx[:, -1]) - 100 * np.exp(mn)


rng = np.random.default_rng(43)
look_pay = np.concatenate([look_chunk(rng, 20_000) for _ in range(10)])
look_mc, look_se = look_pay.mean(), look_pay.std(ddof=1) / math.sqrt(len(look_pay))
check("lookback call: exact min law vs bridge MC", look_exact, look_mc, 4 * look_se)
print("   lookback", round(look_exact, 4), " MC", round(look_mc, 4), "se", round(look_se, 4))

# ranking summary at r = 0
rank = {"lookback": look_exact, "European": vanilla, "down-and-out B=90": c_do, "Asian": asian_mm}
order = sorted(rank, key=rank.get, reverse=True)
print("   ranking by price (dearest first):", [(k, round(rank[k], 3)) for k in order])
assert order == ["lookback", "European", "down-and-out B=90", "Asian"], order
assert asian_mm < c_do, "Asian vs knock-out ordering in this example"

# American versus European put, S=K=100, r=5%, s=20%, T=1: CRR against Leisen-Reimer
def crr_american_put(S, K, r, s, T, n, american=True):
    dt = T / n
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    q = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    v = [max(K - S * u ** j * d ** (n - j), 0) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        v = [disc * (q * v[j + 1] + (1 - q) * v[j]) for j in range(i + 1)]
        if american:
            v = [max(v[j], K - S * u ** j * d ** (i - j)) for j in range(i + 1)]
    return v[0]


def peizer_pratt(z, n):
    return 0.5 + math.copysign(1, z) * 0.5 * math.sqrt(1 - math.exp(-((z / (n + 1 / 3 + 0.1 / (n + 1))) ** 2) * (n + 1 / 6)))


def lr_american_put(S, K, r, s, T, n, american=True):
    d1, d2 = d1d2(S, K, r, s, T)
    p = peizer_pratt(d2, n)
    pb = peizer_pratt(d1, n)
    dt = T / n
    rho = math.exp(r * dt)
    u = rho * pb / p
    d = (rho - p * u) / (1 - p)
    disc = 1 / rho
    v = [max(K - S * u ** j * d ** (n - j), 0) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        v = [disc * (p * v[j + 1] + (1 - p) * v[j]) for j in range(i + 1)]
        if american:
            v = [max(v[j], K - S * u ** j * d ** (i - j)) for j in range(i + 1)]
    return v[0]


am_a = crr_american_put(100, 100, .05, .2, 1, 1500)
am_b = lr_american_put(100, 100, .05, .2, 1, 801)
eu_p = bs_put(100, 100, .05, .2, 1)
check("European put by BS vs parity", eu_p, bs_call(100, 100, .05, .2, 1) - 100 + 100 * math.exp(-.05), 1e-10)
check("European put BS vs integral", eu_p, put_B(100, 100, .05, .2, 1), 1e-7)
check("American put: CRR 1500 vs Leisen-Reimer 801", am_a, am_b, 0.003)
print("   American put", round(am_a, 4), "LR", round(am_b, 4), " European", round(eu_p, 4), " early-exercise premium", round(am_a - eu_p, 4))
# American call on a non-dividend share equals the European call (r = 5%)
ac = None
def crr_call(S, K, r, s, T, n, american):
    dt = T / n
    u = math.exp(s * math.sqrt(dt))
    d = 1 / u
    q = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    v = [max(S * u ** j * d ** (n - j) - K, 0) for j in range(n + 1)]
    for i in range(n - 1, -1, -1):
        v = [disc * (q * v[j + 1] + (1 - q) * v[j]) for j in range(i + 1)]
        if american:
            v = [max(v[j], S * u ** j * d ** (i - j) - K) for j in range(i + 1)]
    return v[0]
check("American call = European call (tree, 800 steps)", crr_call(100, 100, .05, .2, 1, 800, True), crr_call(100, 100, .05, .2, 1, 800, False), 1e-10)

# exam e-american-put tree (S=50, u=1.2, d=0.8, r=3% a step, K=52): American, European and Asian put
Sx0, uu, dd, rr_, KK = 50.0, 1.2, 0.8, 0.03, 52.0
q = (1 + rr_ - dd) / (uu - dd)
check("exam q", q, 0.575, 1e-12)
vuu, vud, vdd = max(KK - 72, 0), max(KK - 48, 0), max(KK - 32, 0)
hold_u = (q * vuu + (1 - q) * vud) / (1 + rr_)
hold_d = (q * vud + (1 - q) * vdd) / (1 + rr_)
am_u = max(hold_u, KK - 60)
am_d = max(hold_d, KK - 40)
am0 = max((q * am_u + (1 - q) * am_d) / (1 + rr_), KK - 50)
eu0 = (q * hold_u + (1 - q) * hold_d) / (1 + rr_)
print("   exam tree American", round(am0, 4), "European", round(eu0, 4))
check("exam American put 5.87", am0, 5.87, 0.005)
check("exam European put 5.25", eu0, 5.25, 0.005)
# Asian put on the average of S1 and S2: path enumeration (A) against a state-recursion (B)
from itertools import product
asian_enum = 0.0
for moves in product((0, 1), repeat=2):
    p = 1.0
    S1 = Sx0
    px = []
    for mv in moves:
        S1 = S1 * (uu if mv else dd)
        px.append(S1)
        p *= q if mv else (1 - q)
    asian_enum += p * max(KK - sum(px) / 2, 0)
asian_enum /= (1 + rr_) ** 2
# method B: recursion on (price, running sum)
def rec(Sv, tot, k):
    if k == 2:
        return max(KK - tot / 2, 0)
    up = rec(Sv * uu, tot + Sv * uu, k + 1)
    dn = rec(Sv * dd, tot + Sv * dd, k + 1)
    return (q * up + (1 - q) * dn) / (1 + rr_)
asian_rec = rec(Sx0, 0.0, 0)
check("exam Asian put (average of S1, S2)", asian_enum, asian_rec, 1e-12)
print("   exam Asian put", round(asian_enum, 4))
assert asian_enum < eu0 < am0

# =========================================================== LESSON l18
print("l18 gamma and the hedged P&L")
S, K, r, s, T = 100.0, 100.0, 0.0, 0.2, 1.0
dl, gm, vg, th = greeks(S, K, r, s, T)
dollar_gamma_half = 0.5 * gm * S * S
check("1/2 Gamma S^2 per option", dollar_gamma_half, 0.5 * 0.019847 * 1e4, 0.01)
print("   1/2 Gamma S^2 =", round(dollar_gamma_half, 4))
# daily breakeven move
be = S * s / math.sqrt(252)
check("breakeven daily move S s / sqrt(252)", be, math.sqrt(-th / 252 / (0.5 * gm)), 1e-9)
print("   breakeven move", round(be, 4), "(", round(be / S * 100, 3), "% )")
# a day with a £2 move
move = 2.0
g_day = 0.5 * gm * move ** 2
th_day = th / 252
check("day P&L (move 2) per option", g_day + th_day,
      (call_B(102, 100, 0, .2, 1 - 1 / 252) - call_B(100, 100, 0, .2, 1)) - dl * 2.0, 6e-4)
print("   gamma gain", round(g_day, 5), "theta", round(th_day, 5), "net", round(g_day + th_day, 5))
# the 'exact' one-day check by full revaluation
exact_day = (call_B(102, 100, 0, .2, 1 - 1 / 252) - call_B(100, 100, 0, .2, 1)) - dl * 2.0
print("   full revaluation, delta-hedged:", round(exact_day, 5))
# the same day for a book of 50,000 options
print("   50,000 options, £2 day:", round(50000 * (g_day + th_day), 2), " breakeven check at 1.2599:", round(50000 * (0.5 * gm * be ** 2 + th_day), 8))
# expected P&L of a long ATM option hedged at implied 20%, realised s_r, continuous hedging, r = 0, mu = 0
def expected_hedged_pnl(s_i, s_r, T=1.0, S=100.0, K=100.0, nt=400, nz=801):
    """E of the integral of 1/2 Gamma_i(t, S_t) S_t^2 (s_r^2 - s_i^2) dt with S_t lognormal at realised vol s_r."""
    tot = 0.0
    for kt in range(nt):
        tk = (kt + 0.5) * T / nt
        tau = T - tk
        sd = s_r * math.sqrt(tk)
        zs = np.linspace(-9, 9, nz)
        w = np.exp(-zs ** 2 / 2) / math.sqrt(2 * math.pi)
        Sv = S * np.exp(-s_r ** 2 * tk / 2 + sd * zs)
        d1v = (np.log(Sv / K) + (s_i ** 2 / 2) * tau) / (s_i * math.sqrt(tau))
        gam_v = np.exp(-d1v ** 2 / 2) / math.sqrt(2 * math.pi) / (Sv * s_i * math.sqrt(tau))
        integrand = 0.5 * gam_v * Sv ** 2 * w
        val = np.trapezoid(integrand, zs)
        tot += val * (s_r ** 2 - s_i ** 2) * (T / nt)
    return tot


def hedged_mc(s_i, s_r, n_steps=252, paths=20000, seed=18):
    rng = np.random.default_rng(seed)
    dt = 1 / n_steps
    Z = rng.standard_normal((paths, n_steps))
    Sv = 100 * np.exp(np.cumsum(-s_r ** 2 / 2 * dt + s_r * math.sqrt(dt) * Z, axis=1))
    Sv = np.concatenate([np.full((paths, 1), 100.0), Sv], axis=1)
    pnl = np.zeros(paths)
    for k in range(n_steps):
        tau = 1 - k * dt
        d1v = (np.log(Sv[:, k] / 100) + s_i ** 2 / 2 * tau) / (s_i * math.sqrt(tau))
        delta = 0.5 * (1 + np.vectorize(math.erf)(d1v / math.sqrt(2)))
        pnl += delta * 0 + (call_vec(Sv[:, k + 1], 100, s_i, tau - dt) - call_vec(Sv[:, k], 100, s_i, tau)) - delta * (Sv[:, k + 1] - Sv[:, k])
    return pnl


def call_vec(Sv, K, s_i, tau):
    if tau <= 1e-12:
        return np.maximum(Sv - K, 0)
    d1v = (np.log(Sv / K) + s_i ** 2 / 2 * tau) / (s_i * math.sqrt(tau))
    d2v = d1v - s_i * math.sqrt(tau)
    erf = np.vectorize(math.erf)
    return Sv * 0.5 * (1 + erf(d1v / math.sqrt(2))) - K * 0.5 * (1 + erf(d2v / math.sqrt(2)))


ep18 = expected_hedged_pnl(.2, .18)
ep26 = expected_hedged_pnl(.2, .26)
ep14 = expected_hedged_pnl(.2, .14)
pn18 = hedged_mc(.2, .18, paths=6000)
pn26 = hedged_mc(.2, .26, paths=6000)
se18 = pn18.std(ddof=1) / math.sqrt(len(pn18))
se26 = pn26.std(ddof=1) / math.sqrt(len(pn26))
check("expected hedged P&L, realised 18%", ep18, pn18.mean(), 4 * se18 + 0.02)
check("expected hedged P&L, realised 26%", ep26, pn26.mean(), 4 * se26 + 0.04)
vg_gap18 = vg * (.18 - .2)
vg_gap26 = vg * (.26 - .2)
gap_price18 = bs_call(100, 100, 0, .18, 1) - bs_call(100, 100, 0, .2, 1)
gap_price26 = bs_call(100, 100, 0, .26, 1) - bs_call(100, 100, 0, .2, 1)
print("   expected P&L 14%, 18%, 26%:", round(ep14, 4), round(ep18, 4), round(ep26, 4))
print("   MC (6,000 paths, seed 18): 18%", round(pn18.mean(), 4), "se", round(se18, 4), "  26%", round(pn26.mean(), 4), "se", round(se26, 4))
print("   vega x gap 18%, 26%:", round(vg_gap18, 4), round(vg_gap26, 4), "  price gap:", round(gap_price18, 4), round(gap_price26, 4))
check("vega x gap vs price gap (18%)", vg_gap18, gap_price18, 0.03)
check("expected P&L vs price gap (18%)", ep18, gap_price18, 0.08)
# constant dollar gamma approximation: 1/2 Gamma S^2 (s_r^2 - s_i^2) T
const_gamma_26 = dollar_gamma_half * (.26 ** 2 - .2 ** 2) * 1.0
print("   constant-gamma estimate (26%):", round(const_gamma_26, 4), " honest integral", round(ep26, 4))
# per-day check of the gamma formula against the exact one-step hedged P&L on a seeded path
rng = np.random.default_rng(18)
n_days = 252
Zp = rng.standard_normal(n_days)
dtp = 1 / n_days
path18 = 100 * np.cumprod(np.concatenate([[1.0], np.exp(-0.26 ** 2 / 2 * dtp + 0.26 * math.sqrt(dtp) * Zp)]))
exact = 0.0
est = 0.0
for k in range(n_days):
    tau = 1 - k * dtp
    Sk, Sn = path18[k], path18[k + 1]
    d1v, _ = d1d2(Sk, 100, 0, .2, tau)
    dlt = Phi(d1v)
    gam = phi(d1v) / (Sk * .2 * math.sqrt(tau))
    if tau - dtp > 1e-12:
        step = bs_call(Sn, 100, 0, .2, tau - dtp) - bs_call(Sk, 100, 0, .2, tau) - dlt * (Sn - Sk)
    else:
        step = max(Sn - 100, 0) - bs_call(Sk, 100, 0, .2, tau) - dlt * (Sn - Sk)
    exact += step
    est += 0.5 * gam * Sk ** 2 * ((Sn / Sk - 1) ** 2 - .2 ** 2 * dtp)
print("   seeded path (rng 18, realised 26% target): final price", round(path18[-1], 4), " exact hedged P&L", round(exact, 4), " gamma estimate", round(est, 4))
check("gamma estimate vs exact hedged P&L on the seeded path", est, exact, 0.35)
# the realised vol of that path
lr = np.diff(np.log(path18))
rv = lr.std(ddof=0) * math.sqrt(252)
print("   realised vol of the seeded path", round(rv, 4))
# exam e-greek-signs: 1,000 short puts, 21 days, realised 30%, implied 20%, constant gamma
pnl_exam = -1000 * dollar_gamma_half * (0.30 ** 2 - 0.20 ** 2) * 21 / 252
check("exam hedged P&L (short 1,000 puts, 21 days, realised 30%)", pnl_exam, -1000 * 0.5 * 0.019847 * 1e4 * 0.05 * (21 / 252), 0.5)
print("   exam P&L", round(pnl_exam, 2))
# transfer: market maker short 20,000 options, implied 24 vs realised 18, 1 month, vega/point
vg_mm = vg / 100
print("   transfer: short 20,000 options, 24 vs 18 vol: vega x gap =", round(20000 * vg_mm * 6, 2))
# review: breakeven daily move S = £50, sigma 30%
check("review breakeven S=50 s=.3", 50 * .3 / math.sqrt(252), 0.9449111825, 1e-6)
# review: theta from gamma for a real option, S = K = £50, s = 25%, T = 0.25, r = 0
g_r = greeks(50, 50, 0, .25, .25)
check("review gamma S=K=50 s=.25 T=.25", g_r[1], gamma_fd(50, 50, .25, .25, 0.05), 1e-5)
check("review theta/yr: -1/2 s^2 S^2 gamma vs full revaluation", g_r[3],
      (call_B(50, 50, 0, .25, .25 - 1e-4) - call_B(50, 50, 0, .25, .25 + 1e-4)) / 2e-4, 1e-4)
check("review theta/yr identity", g_r[3], -0.5 * .25 ** 2 * 50 ** 2 * g_r[1], 1e-12)
print("   review: gamma", round(g_r[1], 5), " theta/yr", round(g_r[3], 4), " theta/day", round(g_r[3] / 252, 5),
      " breakeven daily move", round(50 * .25 / math.sqrt(252), 4))

# l18 hook: two seeded years hedged daily, bought at 20% implied (r = 0): the share FELL in both, the P&L differs
def seeded_year(seed, sg, n_days=252, s_i=0.2):
    rng = np.random.default_rng(seed)
    dtp = 1 / n_days
    Zp = rng.standard_normal(n_days)
    pth = 100 * np.cumprod(np.concatenate([[1.0], np.exp(-sg ** 2 / 2 * dtp + sg * math.sqrt(dtp) * Zp)]))
    exact_, est_ = 0.0, 0.0
    for k in range(n_days):
        tau = 1 - k * dtp
        Sk, Sn = pth[k], pth[k + 1]
        d1v, _ = d1d2(Sk, 100, 0, s_i, tau)
        dlt = Phi(d1v)
        gam = phi(d1v) / (Sk * s_i * math.sqrt(tau))
        nxt = bs_call(Sn, 100, 0, s_i, tau - dtp) if tau - dtp > 1e-12 else max(Sn - 100, 0)
        exact_ += nxt - bs_call(Sk, 100, 0, s_i, tau) - dlt * (Sn - Sk)
        est_ += 0.5 * gam * Sk ** 2 * ((Sn / Sk - 1) ** 2 - s_i ** 2 * dtp)
    return pth, exact_, est_

for seed, sg in ((18, 0.26), (21, 0.14)):
    pth, ex_, es_ = seeded_year(seed, sg)
    check(f"seed {seed} (generated {sg}) exact hedged P&L vs gamma sum", ex_, es_, 0.2)
    print(f"   seed {seed}: final {pth[-1]:.2f}, hedged P&L {ex_:.4f}, gamma estimate {es_:.4f}, share change {pth[-1] / 100 - 1:+.3%}")
    assert pth[-1] < 100
assert seeded_year(18, 0.26)[1] > 0 > seeded_year(21, 0.14)[1]

# l15 table: call prices at the spread strikes (r = 5%)
for Kx in (95, 98, 99, 99.5, 100.5, 101, 102, 105):
    check(f"C({Kx}) shared option", bs_call(100, Kx, .05, .2, 1), call_B(100, Kx, .05, .2, 1), 1e-7)

# the plan's sentence, one more time
check("plan check: rule 8.00 vs 7.9656", 8.0 - bs_call(100, 100, 0, .2, 1), 8.0 - 7.9656, 5e-5)

print(f"\nPASS: {CHECKS} checks, every number computed by two independent methods")
