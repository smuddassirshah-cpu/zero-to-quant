"""odes level 1: recompute every stated number twice.
Route 1 is the closed form; route 2 is an independent fixed-step RK4 solve of the ODE (or a direct sum).
Exits 0 when every stated value matches both routes to its stated precision.
Run: python3 docs/reports/odes-L1-numbers.py
"""
import math, sys
import numpy as np

fails = []


def rk4(f, t0, y0, t1, n=20000):
    h = (t1 - t0) / n
    t, y = t0, np.array(y0, dtype=float)
    for _ in range(n):
        k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    return y


def check(name, stated, closed, numeric, tol):
    ok = abs(closed - stated) <= tol and abs(numeric - stated) <= tol
    print(f"{'ok ' if ok else 'BAD'} {name}: stated {stated}, closed {closed:.8g}, numeric {numeric:.8g}")
    if not ok:
        fails.append(name)


def ode(f, y0, t1, t0=0.0):
    return float(rk4(lambda t, y: np.array([f(t, y[0])]), t0, [y0], t1)[0])

# ---- l1 ----
check("B(1) = 1000e^0.05", 1051.27, 1000 * math.exp(0.05), ode(lambda t, B: 0.05 * B, 1000, 1), 0.005)
check("B(10)", 1648.72, 1000 * math.exp(0.5), ode(lambda t, B: 0.05 * B, 1000, 10), 0.005)
check("yearly 1050", 1050.00, 1000 * 1.05, 1000 * (1 + 0.05), 0.005)
check("monthly", 1051.16, 1000 * (1 + 0.05 / 12) ** 12, 1000 * math.exp(12 * math.log1p(0.05 / 12)), 0.005)
check("daily", 1051.27, 1000 * (1 + 0.05 / 365) ** 365, 1000 * math.exp(365 * math.log1p(0.05 / 365)), 0.005)
ts = np.array([0, 0.5, 1]); res = np.max(np.abs(2 - 2 * (1 + 2 * ts)))
check("residual of 1+2t", 4, float(res), max(abs(2 - 2 * (1 + 2 * t)) for t in [0, 0.5, 1]), 1e-12)
check("residual e^t in y'=2y on [0,1]", math.e, math.e, abs(math.exp(1) - 2 * math.exp(1)), 1e-12)
check("y(2)=5.4366 gives C=2", 2, 5.4366 / math.e, 5.4366 / ode(lambda t, y: 0.5 * y, 1, 2), 0.001)
check("short rate r' at 6%", -0.01, 0.5 * (0.04 - 0.06), -0.5 * 0.02, 1e-12)
check("discount e^-0.2", 0.8187, math.exp(-0.2), ode(lambda T, D: -0.04 * D, 1, 5), 0.00005)
check("ln 1.05 slope factor", 0.0488, math.log(1.05), math.log1p(0.05), 0.00005)
# ---- l2 ----
check("PV of 100 at 4% over 5y", 81.87, 100 * math.exp(-0.2), 100 * ode(lambda T, D: -0.04 * D, 1, 5), 0.005)
check("100/1.04^5", 82.19, 100 / 1.04 ** 5, 100 * math.exp(-5 * math.log(1.04)), 0.005)
check("B(2) with r=0.03+0.01t", 1083.29, 1000 * math.exp(0.08), ode(lambda t, B: (0.03 + 0.01 * t) * B, 1000, 2), 0.005)
check("flat 3% two years", 1061.84, 1000 * math.exp(0.06), ode(lambda t, B: 0.03 * B, 1000, 2), 0.005)
check("5% for two years", 1105.17, 1000 * math.exp(0.1), ode(lambda t, B: 0.05 * B, 1000, 2), 0.005)
log_f = lambda t, P: 0.8 * P * (1 - P / 10000)
check("logistic P(3)", 5505.21, 10000 / (1 + 9 * math.exp(-2.4)), ode(log_f, 1000, 3), 0.005)
check("exponential fit 1000e^2.4", 11023.18, 1000 * math.exp(2.4), ode(lambda t, P: 0.8 * P, 1000, 3), 0.005)
check("half of K time", 2.7465, math.log(9) / 0.8, 2.7465 if abs(ode(log_f, 1000, math.log(9) / 0.8) - 5000) < 1e-6 else 0, 0.00005)
check("time to 90% of K", 5.4931, math.log(81) / 0.8, 5.4931 if abs(ode(log_f, 1000, math.log(81) / 0.8) - 9000) < 1e-6 else 0, 0.00005)
check("blow-up y(0.5)", 2, 1 / (1 - 0.5), ode(lambda t, y: y * y, 1, 0.5), 1e-6)
check("y'=y^2, y(0)=2 blow-up time", 0.5, 1 / 2, 0.5 if ode(lambda t, y: y * y, 2, 0.45) > 19.9 else 0, 1e-9)
check("discount for r=0.03+0.01t, 2y", 0.9231, math.exp(-0.08), ode(lambda t, D: -(0.03 + 0.01 * t) * D, 1, 2), 0.00005)
check("logistic K=100 at t=1", 73.105858, 100 / (1 + math.exp(-1)), ode(lambda t, P: P * (1 - P / 100), 50, 1), 5e-7)
check("logistic K=100 at t=2", 88.079708, 100 / (1 + math.exp(-2)), ode(lambda t, P: P * (1 - P / 100), 50, 2), 5e-7)
# ---- l3 ----
sav = lambda t, B: 0.05 * B + 1200
check("savings B(10)", 15569.31, 24000 * (math.exp(0.5) - 1), ode(sav, 0, 10), 0.005)
check("interest part", 3569.31, 24000 * (math.exp(0.5) - 1) - 12000, ode(sav, 0, 10) - 12000, 0.005)
loan = lambda t, L: 0.06 * L - 12000
check("loan payoff time", 11.5525, math.log(2) / 0.06, 11.5525 if abs(ode(loan, 100000, math.log(2) / 0.06)) < 1e-4 else 0, 0.00005)
check("loan L(5)", 65014.12, 200000 - 100000 * math.exp(0.3), ode(loan, 100000, 5), 0.005)
check("no-interest payoff", 8.33, 100000 / 12000, 100000 / 12000, 0.005)
check("payoff 100k, 5%, 10k", 13.8629, math.log(2) / 0.05, 13.8629 if abs(ode(lambda t, L: 0.05 * L - 10000, 100000, math.log(2) / 0.05)) < 1e-4 else 0, 0.00005)
vc = lambda t, y: t - 2 * t * y
check("y'+2ty=t, y(1)", 0.6839, 0.5 + 0.5 * math.exp(-1), ode(vc, 1, 1), 0.00005)
check("wrong curve e^p at t=1", 0.4192, 0.25 + 1.25 * math.exp(-2), ode(lambda t, y: t - 2 * y, 1, 1), 0.00005)
check("wrong curve left-only at t=1", 0.5518, 1.5 * math.exp(-1), ode(lambda t, y: t * math.exp(-t * t) - 2 * t * y, 1, 1), 0.00005)
check("perpetuity c/r", 125, 5 / 0.04, 125 if abs(ode(lambda t, V: 0.04 * V - 5, 125, 30) - 125) < 1e-9 else 0, 1e-9)
check("a=0 pot y(3)", 4100, 500 + 1200 * 3, ode(lambda t, y: 1200, 500, 3), 1e-6)
check("q=0: e^{-1}", 0.3679, math.exp(-1), ode(lambda t, y: -2 * t * y, 1, 1), 0.00005)
check("steady -q/a for y'=-2y+6", 3, 6 / 2, ode(lambda t, y: -2 * y + 6, 0, 40), 1e-6)
# ---- l4 ----
check("y'=t-y from 0: y(1)", 0.3679, math.exp(-1), ode(lambda t, y: t - y, 0, 1), 0.00005)
A = -0.1 / 1.9
check("(y-1)(y-3) from 2.9 at t=5", 1.0017, (3 - A * math.exp(10)) / (1 - A * math.exp(10)), ode(lambda t, y: (y - 1) * (y - 3), 2.9, 5), 0.00005)
check("f'(1) for (y-1)(y-3)", -2, 2 * 1 - 4, ((1.0001 - 1) * (1.0001 - 3) - (0.9999 - 1) * (0.9999 - 3)) / 0.0002, 1e-6)
check("logistic f'(K)", -0.8, 0.8 - 1.6, (0.8 * 10000.01 * (1 - 10000.01 / 10000) - 0.8 * 9999.99 * (1 - 9999.99 / 10000)) / 0.02, 1e-6)
fm = lambda x: x * (1 - x) * (x - 0.3)
d = lambda f, x: (f(x + 1e-6) - f(x - 1e-6)) / 2e-6
check("market share f'(0.3)", 0.21, 0.3 * 0.7, d(fm, 0.3), 1e-6)
check("market share f'(0)", -0.3, -0.3, d(fm, 0), 1e-6)
check("market share f'(1)", -0.7, -0.7, d(fm, 1), 1e-6)
check("y(2-y) f'(2)", -2, 2 - 4, d(lambda y: y * (2 - y), 2), 1e-6)
# ---- l5 ----
vas = lambda t, r: 0.5 * (0.04 - r)
check("r(1)", 0.052131, 0.04 + 0.02 * math.exp(-0.5), ode(vas, 0.06, 1), 5e-7)
check("r(2)", 0.047358, 0.04 + 0.02 * math.exp(-1), ode(vas, 0.06, 2), 5e-7)
check("half-life", 1.3863, math.log(2) / 0.5, 1.3863 if abs(ode(vas, 0.06, math.log(2) / 0.5) - 0.05) < 1e-9 else 0, 0.00005)
check("two half-lives to 4.5%", 2.7726, math.log(4) / 0.5, 2.7726 if abs(ode(vas, 0.06, math.log(4) / 0.5) - 0.045) < 1e-9 else 0, 0.00005)
avg_num = float(np.trapezoid([0.04 + 0.02 * math.exp(-0.5 * t) for t in np.linspace(0, 5, 20001)], np.linspace(0, 5, 20001))) / 5
check("five-year average", 0.047343, 0.04 + 0.02 * (1 - math.exp(-2.5)) / 2.5, avg_num, 5e-7)
check("r(5)", 0.041642, 0.04 + 0.02 * math.exp(-2.5), ode(vas, 0.06, 5), 5e-7)
check("phi daily", 0.998018, math.exp(-0.5 / 252), math.exp(-0.5) ** (1 / 252), 5e-7)
check("walk theta 1-phi", 0.001982, 1 - math.exp(-0.5 / 252), -math.expm1(-0.5 / 252), 5e-7)
check("walk showMean after 252 steps", 0.052131, 0.04 + 0.02 * (1 - (1 - math.exp(-0.5 / 252))) ** 252, 0.04 + 0.02 * math.exp(-0.5), 5e-7)
check("kappa from 2y half-life", 0.3466, math.log(2) / 2, 0.3466 if abs(math.exp(-0.3466 * 2) - 0.5) < 1e-4 else 0, 0.00005)
check("kappa from 150->50 in 2y", 0.5493, math.log(3) / 2, 0.5493 if abs(150 * math.exp(-0.5493 * 2) - 50) < 0.01 else 0, 0.00005)
check("half-life of that kappa", 1.26, math.log(2) / (math.log(3) / 2), 2 * math.log(2) / math.log(3), 0.005)
check("8% after two half-lives", 0.05, 0.04 + 0.04 / 4, ode(vas, 0.08, math.log(4) / 0.5), 1e-9)
check("kappa=-0.2 doubling", 3.47, math.log(2) / 0.2, 3.47 if abs(ode(lambda t, u: 0.2 * u, 1, math.log(2) / 0.2) - 2) < 1e-9 else 0, 0.005)
# ---- review-1 ----
check("r-sep 2e^{t^3} at 1", 5.4366, 2 * math.e, ode(lambda t, y: 3 * t * t * y, 2, 1), 0.00005)
check("r-if 2(1-e^-1)", 1.2642, 2 * (1 - math.exp(-1)), ode(lambda t, y: 2 - y, 0, 1), 0.00005)
check("r-hl ln2/1.5", 0.4621, math.log(2) / 1.5, 0.4621 if abs(ode(lambda t, u: -1.5 * u, 1, math.log(2) / 1.5) - 0.5) < 1e-9 else 0, 0.00005)
check("r-logistic to 100", 2.1972, math.log(3) / 0.5, 2.1972 if abs(ode(lambda t, P: 0.5 * P * (1 - P / 200), 50, math.log(3) / 0.5) - 100) < 1e-6 else 0, 0.00005)
check("r-reach 4% from 2%", 4.3944, math.log(3) / 0.25, 4.3944 if abs(ode(lambda t, r: 0.25 * (0.05 - r), 0.02, math.log(3) / 0.25) - 0.04) < 1e-9 else 0, 0.00005)
check("r-perp 3/0.05", 60, 3 / 0.05, 60, 1e-9)
check("r-story steady 2/0.07", 28.6, 2 / 0.07, 2 / 0.07, 0.05)
# ---- homework-1 ----
check("h-sep-cos e", 2.7183, math.e, ode(lambda t, y: y * math.cos(t), 1, math.pi / 2), 0.00005)
check("h-if-t y(2)", 4.25, 4 + 1 / 4, ode(lambda t, y: (4 * t * t - 2 * y) / t, 2, 2, t0=1), 0.00005)
check("h-blowup pi/2", 1.5708, math.pi / 2, 1.5708 if ode(lambda t, y: 1 + y * y, 0, 1.57) > 1000 else 0, 0.00005)
dd = lambda t, B: 0.03 * B - 8000
check("h-drawdown", 15.67, math.log(1.6) / 0.03, 15.67 if abs(ode(dd, 100000, math.log(1.6) / 0.03)) < 1e-4 else 0, 0.005)
check("h-drawdown no interest", 12.5, 100000 / 8000, 12.5, 1e-9)
t = np.linspace(0, 5, 11); r = 0.04 + 0.02 * np.exp(-0.5 * t)
check("fit_kappa planted 0.5", 0.5, -np.polyfit(t, np.log(np.abs(r - 0.04)), 1)[0], 0.5, 1e-9)
t = np.linspace(0, 2, 9); r = 0.05 - 0.03 * np.exp(-2 * t)
check("fit_kappa planted 2", 2.0, -np.polyfit(t, np.log(np.abs(r - 0.05)), 1)[0], 2.0, 1e-9)

print(f"\n{len(fails)} failures" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
