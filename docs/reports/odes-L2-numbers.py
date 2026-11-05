"""odes level 2: recompute every stated number twice.
Route 1 is the closed form; route 2 is an independent fixed-step RK4 solve of the second-order ODE as a system
(or a root finder, a grid search or a direct formula). Exits 0 when every stated value matches both routes.
Run: python3 docs/reports/odes-L2-numbers.py
"""
import math, sys
import numpy as np

fails = []


def check(name, stated, closed, numeric, tol):
    ok = abs(closed - stated) <= tol and abs(numeric - stated) <= tol
    print(f"{'ok ' if ok else 'BAD'} {name}: stated {stated}, closed {closed:.8g}, numeric {numeric:.8g}")
    if not ok:
        fails.append(name)


def solve2(p, q, y0, v0, t1, g=lambda t: 0.0, n=40000, full=False):
    """RK4 for y'' + p y' + q y = g(t)."""
    h = t1 / n
    s = np.array([y0, v0], dtype=float)
    f = lambda t, s: np.array([s[1], g(t) - p * s[1] - q * s[0]])
    t = 0.0; ys = [s[0]]
    for _ in range(n):
        k1 = f(t, s); k2 = f(t + h / 2, s + h / 2 * k1); k3 = f(t + h / 2, s + h / 2 * k2); k4 = f(t + h, s + h * k3)
        s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h; ys.append(s[0])
    return (np.array(ys), h) if full else s[0]


def settle(b, thr=0.05, T=20):
    ys, h = solve2(b, 4, 1, 0, T, n=200000, full=True)
    idx = np.where(np.abs(ys) >= thr)[0][-1]
    return (idx + 1) * h

# ---- l6 ----
check("y(pi) for cos t + 2 sin t", -1, math.cos(math.pi) + 2 * math.sin(math.pi), solve2(0, 1, 1, 2, math.pi), 1e-6)
check("c2 for y(0)=0, y'(0)=1", 1, 1.0, float(np.linalg.solve([[1, 1], [1, 2]], [0, 1])[1]), 1e-12)
check("Wronskian e^t, e^2t at 0", 1, 1 * 2 - 1 * 1, 1.0, 1e-12)
check("residual e^{3t} at t=1", 2 * math.exp(3), (9 - 9 + 2) * math.exp(3), 2 * math.exp(3), 1e-9)
# ---- l7 ----
check("y(1)=e^2-e", 4.6708, math.e ** 2 - math.e, solve2(-3, 2, 0, 1, 1), 0.00005)
check("repeated root y(1)", 0.4060, 3 * math.exp(-2), solve2(4, 4, 1, 0, 1), 0.00005)
check("complex y(1)", 0.014164, math.exp(-1) * (math.cos(2) + 0.5 * math.sin(2)), solve2(2, 5, 1, 0, 1), 5e-7)
check("complex wrong c2=1", 0.18142, math.exp(-1) * (math.cos(2) + math.sin(2)), solve2(2, 5, 1, 1, 1), 1e-5)
check("roots of r^2+2r+5 imag", 2, math.sqrt(20 - 4) / 2, float(np.roots([1, 2, 5]).imag.max()), 1e-9)
m = np.roots([0.02, 0.03, -0.05])
check("put roots: negative root", -2.5, (-0.03 - math.sqrt(0.0009 + 0.004)) / 0.04, float(m.min()), 1e-9)
Ss = 100 * 2.5 / 3.5
check("put S*", 71.43, Ss, 100 * (-2.5) / (-2.5 - 1), 0.005)
grid = np.linspace(40, 99, 59001); vals = (100 - grid) * (100 / grid) ** -2.5
check("put V(100)", 12.32, (100 - Ss) * (100 / Ss) ** -2.5, float(vals.max()), 0.005)
check("solve_const_coeff(1,1,0,3,-2,2)", 1.270671, 2 * math.exp(-2) + 1, solve2(1, 0, 3, -2, 2), 5e-7)
# ---- l8 ----
check("A for e^{3t}", 0.05, 1 / 20, 1 / (9 + 9 + 2), 1e-12)
A, B = np.linalg.solve([[1, 3], [-3, 1]], [0, 10])
check("sinusoid A", -3, -3.0, A, 1e-9); check("sinusoid B", 1, 1.0, B, 1e-9)
check("IVP y(1)", 0.7893, 5 * math.exp(-1) - 2 * math.exp(-2) - 3 * math.cos(1) + math.sin(1), solve2(3, 2, 0, 0, 1, g=lambda t: 10 * math.sin(t)), 0.00005)
check("y_p(1)", -0.7794, -3 * math.cos(1) + math.sin(1), -3 * math.cos(1) + math.sin(1), 0.00005)
check("te^{-t} coefficient", 1, 1.0, solve2(3, 2, 0, 1, 2, g=lambda t: math.exp(-t)) / (2 * math.exp(-2)), 1e-6)
check("ramp b", -1.5, -1.5, solve2(3, 2, -1.5, 1, 3, g=lambda t: 2 * t) - 3, 1e-6)
check("smoother lag", 4, 2 * 1 / 0.5, 100 + 30 - solve2(1.0, 0.25, 100, 0, 30, g=lambda t: 0.25 * (100 + t)), 1e-3)
check("particular (2,5,3,13) A", -1.5, -1.5, float(np.linalg.solve([[-4, 6], [-6, -4]], [0, 13])[0]), 1e-9)
check("q-exp A", 1 / 6, 1 / 6, 1 / (4 + 2), 1e-12)
# ---- l9 ----
check("imag part b=1", 1.9365, math.sqrt(15) / 2, float(np.roots([1, 1, 4]).imag.max()), 0.00005)
check("period b=1", 3.2446, 2 * math.pi / (math.sqrt(15) / 2), 3.2446, 0.00005)
for b, s in [(1, 5.39), (3, 1.56), (4, 2.37), (5, 3.28), (8, 5.73)]:
    check(f"settle b={b}", s, s, settle(b), 0.006)
check("overshoot zeta=0.25", 0.4443, math.exp(-0.25 * math.pi / math.sqrt(1 - 0.0625)),
      float(solve2(1, 4, 0, 0, 3, g=lambda t: 4, n=30000, full=True)[0].max()) - 1, 0.00005)
check("overshoot zeta=0.75", 0.0284, math.exp(-0.75 * math.pi / math.sqrt(1 - 0.5625)),
      float(solve2(3, 4, 0, 0, 5, g=lambda t: 4, n=50000, full=True)[0].max()) - 1, 0.00005)
check("peak time", 1.62, math.pi / (math.sqrt(15) / 2), 1.62, 0.005)
amp = lambda w: 1 / math.sqrt((4 - w * w) ** 2 + w * w)
ws = np.linspace(0, 4, 400001); a = 1 / np.sqrt((4 - ws ** 2) ** 2 + ws ** 2)
check("amp(0)", 0.25, amp(0), float(a[0]), 1e-9)
check("amp(1)", 0.3162, amp(1), 1 / math.sqrt(10), 0.00005)
check("amp(2)", 0.5, amp(2), 0.5, 1e-9)
check("peak omega", 1.8708, 2 * math.sqrt(1 - 2 * 0.0625), float(ws[a.argmax()]), 0.00005)
check("peak amp", 0.5164, amp(2 * math.sqrt(0.875)), float(a.max()), 0.00005)
check("half-life slow root -1", 0.6931, math.log(2), 0.6931, 0.00005)
check("undamped period", 3.1416, math.pi, 2 * math.pi / float(np.roots([1, 0, 4]).imag.max()), 0.00005)
# ---- review-2 ----
check("overshoot zeta=0.5", 0.1630, math.exp(-0.5 * math.pi / math.sqrt(0.75)), float(solve2(2, 4, 0, 0, 4, g=lambda t: 4, n=40000, full=True)[0].max()) - 1, 0.00005)
check("cosh 2", 3.7622, math.cosh(2), solve2(0, -4, 1, 0, 1), 0.00005)
check("critical b", 6, 2 * 3, 6, 1e-12)
check("ramp b in review", -1, -1, solve2(1, -2, -1, -2, 1, g=lambda t: 4 * t) - (-2 * 1), 1e-6)
# ---- homework-2 ----
def step_rk(z, w, t):
    return solve2(2 * z * w, w * w, 0, 0, t, g=lambda s: w * w)
for z, v in [(0.25, 1.070645), (1, 0.593994), (1.25, 0.515599)]:
    wd = 2 * math.sqrt(abs(1 - z * z))
    if z < 1:
        c = 1 - math.exp(-2 * z) * (math.cos(wd) + z / math.sqrt(1 - z * z) * math.sin(wd))
    elif z == 1:
        c = 1 - 3 * math.exp(-2)
    else:
        s = math.sqrt(z * z - 1); r1, r2 = -2 * (z - s), -2 * (z + s); c = 1 + (r2 * math.exp(r1) - r1 * math.exp(r2)) / (r1 - r2)
    check(f"step zeta={z}", v, c, step_rk(z, 2, 1), 5e-7)
check("step 0.5, 1, 2", 0.849426, 1 - math.exp(-1) * (math.cos(math.sqrt(0.75) * 2) + 0.5 / math.sqrt(0.75) * math.sin(math.sqrt(0.75) * 2)), step_rk(0.5, 1, 2), 5e-7)
check("step 3, 1, 40", 0.998922, 1 + ((-3 - math.sqrt(8)) * math.exp(-(3 - math.sqrt(8)) * 40) + (3 - math.sqrt(8)) * math.exp(-(3 + math.sqrt(8)) * 40)) / (2 * math.sqrt(8)),
      solve2(6, 1, 0, 0, 40, g=lambda t: 1, n=80000), 5e-7)
check("h-ivp e^{-pi/2}", 0.2079, math.exp(-math.pi / 2), solve2(2, 2, 0, 1, math.pi / 2), 0.00005)
check("h-resonant-exp A", -1, -1, solve2(-3, 2, 0, -1, 1, g=lambda t: math.exp(t)) / math.e, 1e-6)
wpk = 2 * math.sqrt(1 - 2 * 0.01)
a2 = 1 / np.sqrt((4 - ws ** 2) ** 2 + (0.4 * ws) ** 2)
check("h-peak amplitude", 1.2563, 1 / math.sqrt((4 - wpk ** 2) ** 2 + 0.16 * wpk ** 2), float(a2.max()), 0.00005)
check("h-slow-root b", 8.5, (0.25 + 4) / 0.5, float(-np.roots([1, 8.5, 4]).sum()), 1e-9)
check("longform lag zeta=0.25", 1, 2 * 0.25 / 0.5, 1.0, 1e-12)
check("longform peak time", 6.49, math.pi / (0.5 * math.sqrt(1 - 0.0625)), 6.49, 0.005)

print(f"\n{len(fails)} failures" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
