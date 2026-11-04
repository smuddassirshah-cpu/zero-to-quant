"""Items of topic-3.2, part C: the pdes items P1 to P8 (plan numbers)."""
import math
from helpers import *
from build_ito import expr

P = {}

# ---------------------------------------------------------------- P1
P[1] = item(
    "e-kernel-peak", 2, ["pe-heat"], ["kernel-peak"], 60,
    title="The height of the kernel",
    prose="Heat obeys $u_t = Du_{xx}$ on the line, with $D = 0.45$. It starts as a unit point source at $x = 0$.",
    question="What is the peak value $u(0, t)$ at $t = 2.5$? Give four decimal places.",
    widget=numeric(0.26596, abs_=0.0005, placeholder="a decimal", label="Peak height",
                   wrong=[("variance-dt", 0.3761, 0.0005), ("no-t", 0.4205, 0.0005)], accept="0.2660 within 0.0005"),
    feedback=fb("The kernel is $\\Phi_t(x) = e^{-x^2/(4Dt)}/\\sqrt{4\\pi Dt}$. At $x = 0$ and $Dt = 1.125$ that is $0.2660$.",
                "The peak is the kernel at $x = 0$: one over $\\sqrt{4\\pi Dt}$.",
                {"variance-dt": "You used $1/\\sqrt{2\\pi Dt}$, which takes the variance as $Dt$. The variance is $2Dt$.",
                 "no-t": "You left $t$ out and used $1/\\sqrt{4\\pi D}$. The peak falls like $1/\\sqrt{t}$."}),
    explain="The kernel is a normal density with variance $2Dt = 2.25$ and sd 1.5. Its peak is $1/(1.5\\sqrt{2\\pi}) = 1/\\sqrt{4\\pi \\cdot 1.125} = 0.2660$.")

# ---------------------------------------------------------------- P2
P[2] = item(
    "e-slab-heat", 3, ["pe-heat"], ["kernel-average"], 120,
    title="Heat at the centre of a slab",
    prose="Heat obeys $u_t = Du_{xx}$ on the whole line, with $D = 0.4$. It starts at $u_0 = 1$ on $[-1.2, 1.2]$ and 0 elsewhere.",
    question="What is $u(0, 0.75)$? Give four decimal places.",
    widget=numeric(0.87866, abs_=0.0005, placeholder="a decimal", label="Temperature",
                   wrong=[("sd-sqrt-dt", 0.9715, 0.0005), ("sd-two-dt", 0.9545, 0.0005)], accept="0.8787 within 0.0005"),
    feedback=fb("The kernel has sd $\\sqrt{2Dt} = 0.7746$, so $u = P(|Z| < 1.2/0.7746) = P(|Z| < 1.549) = 0.8787$.",
                "The solution is the kernel average of $u_0$: a normal chance of landing in the slab.",
                {"sd-sqrt-dt": "You used the sd $\\sqrt{Dt} = 0.5477$. The kernel's variance is $2Dt$, so the sd is $0.7746$.",
                 "sd-two-dt": "You used the sd $2Dt = 0.6$. The variance is $2Dt$, and the sd is its square root."}),
    explain="At $x = 0$, $u$ is the kernel's mass on $[-1.2, 1.2]$. The kernel is $N(0, 2Dt)$ with $2Dt = 0.6$. So $u = 2\\Phi(1.549) - 1 = 0.8787$.")

# ---------------------------------------------------------------- P5
P[5] = item(
    "e-rod-centre", 3, ["pe-fourier", "pe-heat"], ["rod-centre"], 150,
    title="The centre of a rod",
    prose="A rod of length 3 has both ends held at 0, with $u_t = 0.3\\,u_{xx}$. It starts as $u(x, 0) = 4\\sin(\\pi x/3) + 2\\sin(\\pi x)$.",
    question="What is the temperature at the centre $x = 1.5$ at $t = 0.5$? Give three decimal places.",
    widget=numeric(2.9382, abs_=0.01, placeholder="a decimal", label="Temperature",
                   wrong=[("one-rate", 1.697, 0.01), ("sign-dropped", 3.848, 0.01)], accept="2.938 within 0.01"),
    feedback=fb("Each mode decays by $e^{-Dk^2t}$. The centre value is $4e^{-0.1645} - 2e^{-1.4804} = 2.938$.",
                "Decay each sine mode by its own rate, then evaluate each sine at $x = 1.5$.",
                {"one-rate": "You used the first mode's decay for both modes. The mode $\\sin(\\pi x)$ has $k = \\pi$ and decays nine times faster.",
                 "sign-dropped": "You added the second term. At $x = 1.5$, $\\sin(\\pi x) = \\sin(1.5\\pi) = -1$."}),
    explain="The modes have $k = \\pi/3$ and $k = \\pi$, so they decay by $e^{-0.3(\\pi/3)^2 \\cdot 0.5} = 0.8483$ and $e^{-0.3\\pi^2 \\cdot 0.5} = 0.2275$. At the centre the first sine is $+1$ and the second is $-1$. So $u = 4 \\cdot 0.8483 - 2 \\cdot 0.2275 = 2.938$.")

# ---------------------------------------------------------------- P4
P[4] = parts_item(
    "e-jump-gibbs", 3, ["pe-fourier"], ["gibbs"], 150,
    title="A jump and its Fourier series",
    prose="A function on a period jumps from 1 to 7 at one point. It is smooth either side of the jump, and its Fourier series converges.",
    question="Two follow-up questions.",
    parts=[
        dict(question="What value does the Fourier series take at the jump? Give one decimal place.",
             widget=numeric(4, abs_=0, placeholder="a number", label="Value at the jump",
                            wrong=[("right-limit", 7, 0), ("left-limit", 1, 0)], accept="4"),
             feedback=fb("At a jump the series converges to the midpoint, $(1 + 7)/2 = 4$.",
                         "At a jump the series takes the average of the two one-sided limits.",
                         {"right-limit": "You gave the right-hand limit. The series settles at the average of both sides.",
                          "left-limit": "You gave the left-hand limit. The series settles at the average of both sides."})),
        dict(question="As the number of terms grows, what is the peak of the partial sums just beside the jump? Give three decimal places.",
             widget=numeric(7.5369, abs_=0.01, placeholder="a decimal", label="Peak",
                            wrong=[("no-overshoot", 7.0, 0.01), ("share-of-level", 7.626, 0.01)], accept="7.537 within 0.01"),
             feedback=fb("The overshoot is $\\tfrac1\\pi\\mathrm{Si}(\\pi) - \\tfrac12 = 8.949\\%$ of the jump 6, so the peak is $7 + 0.537 = 7.537$.",
                         "The Gibbs overshoot is 8.949% of the size of the jump, not of the level.",
                         {"no-overshoot": "You gave 7, the limit of the function. The partial sums overshoot it and keep doing so.",
                          "share-of-level": "You took 8.949% of 7. The overshoot is a share of the jump, which is 6."}))],
    explain="At a jump the series converges to the midpoint. Just beside it the partial sums overshoot by about 8.949% of the jump size, however many terms are used. That is $0.0895 \\cdot 6 = 0.537$ above 7.")

# ---------------------------------------------------------------- P6
P[6] = parts_item(
    "e-heat-change", 3, ["pe-bs"], ["heat-change"], 150,
    title="Constants that turn Black-Scholes into heat",
    prose="Take $r = 6\\%$, $\\sigma = 25\\%$ and $T = 0.75$, so $k = 2r/\\sigma^2 = 1.92$. With $x = \\ln(S/K)$ and $\\tau = \\tfrac12\\sigma^2(T - t)$, the scaled value $v = V/K$ solves $v_\\tau = v_{xx} + (k - 1)v_x - kv$. Put $v = e^{\\alpha x + \\beta\\tau}u$ so that $u_\\tau = u_{xx}$.",
    question="Two follow-up questions.",
    parts=[
        dict(question="What is $\\alpha$, the constant that removes the $v_x$ term? Give three decimal places.",
             widget=numeric(-0.46, abs_=0.0005, placeholder="a decimal", label="alpha",
                            wrong=[("sign", 0.46, 0.0005), ("k-over-two", -0.96, 0.0005)], accept="-0.460 within 0.0005"),
             feedback=fb("$\\alpha = -(k - 1)/2 = -0.46$.",
                         "The $v_x$ term cancels when $2\\alpha + (k - 1) = 0$.",
                         {"sign": "You gave $+0.46$. Cancelling the $v_x$ term needs $2\\alpha = -(k - 1)$.",
                          "k-over-two": "You used $-k/2$. The coefficient of $v_x$ is $k - 1$, so $\\alpha = -(k - 1)/2$."})),
        dict(question="What is $\\beta$? Give four decimal places.",
             widget=numeric(-2.1316, abs_=0.0005, placeholder="a decimal", label="beta",
                            wrong=[("k-minus-one-squared", -0.2116, 0.0005), ("half-sum", -1.46, 0.0005)], accept="-2.1316 within 0.0005"),
             feedback=fb("$\\beta = -(k + 1)^2/4 = -2.92^2/4 = -2.1316$.",
                         "Collect the $u$ terms: $\\beta = \\alpha^2 + (k - 1)\\alpha - k$.",
                         {"k-minus-one-squared": "You used $-(k - 1)^2/4$, which forgets the $-kv$ term. Together they make $-(k + 1)^2/4$.",
                          "half-sum": "You used $-(k + 1)/2$. The constant is a square: $-(k + 1)^2/4$."}))],
    explain="Substituting $v = e^{\\alpha x + \\beta\\tau}u$ gives $u_\\tau = u_{xx} + (2\\alpha + k - 1)u_x + (\\alpha^2 + (k - 1)\\alpha - k - \\beta)u$. Both brackets must vanish. That gives $\\alpha = -0.46$ and $\\beta = -2.1316$.")

# ---------------------------------------------------------------- P7
P[7] = item(
    "e-fk-square", 3, ["pe-fk"], ["feynman-kac"], 150,
    title="A Feynman-Kac value",
    prose="A process has $dX = 0.5\\,dt + 1.2\\,dW$. A payoff $h(x) = x^2$ is paid at the horizon, discounted at $r = 10\\%$. The process starts at $x = 2$ with 2 years to go.",
    question="What is the value $V$ by Feynman-Kac? Give four decimal places.",
    widget=numeric(9.72652, abs_=0.0005, placeholder="a decimal", label="Value",
                   wrong=[("no-discounting", 11.88, 0.0005), ("no-variance-term", 7.3686, 0.0005)], accept="9.7265 within 0.0005"),
    feedback=fb("$X_T \\sim N(3, 2.88)$, so $E[X_T^2] = 9 + 2.88 = 11.88$, and $V = e^{-0.2} \\cdot 11.88 = 9.7265$.",
                "Take $E[X_T^2]$ for the normal law of $X_T$, then discount by $e^{-rT}$.",
                {"no-discounting": "You did not discount. $E[X_T^2] = 11.88$, and the value is $e^{-0.2}$ times that.",
                 "no-variance-term": "You squared the mean only, $3^2 = 9$. The second moment adds the variance $1.44 \\cdot 2 = 2.88$."}),
    explain="The value is $V = e^{-rT}E[h(X_T)]$. Here $X_T$ has mean $2 + 0.5 \\cdot 2 = 3$ and variance $1.44 \\cdot 2 = 2.88$. So $E[X_T^2] = 11.88$ and $V = e^{-0.2} \\cdot 11.88 = 9.7265$.")

# ---------------------------------------------------------------- P3
P[3] = item(
    "e-coefficient-k", 4, ["pe-fourier"], ["fourier-coefficient"], 180,
    title="A sine coefficient",
    prose="The function $f(x) = x(\\pi - x)$ on $(0, \\pi)$ is extended as an odd function. Its sine series has $b_k = \\tfrac2\\pi\\int_0^\\pi f(x)\\sin kx\\,dx$ for whole numbers $k \\ge 1$.",
    question="Give $b_k$ as an expression in $k$.",
    widget=expr("\\frac{4(1-(-1)^k)}{\\pi k^3}",
                accept=["\\frac{4-4(-1)^k}{\\pi k^3}", "\\frac{4(1-\\cos k\\pi)}{\\pi k^3}"],
                wrong=[("one-over-pi", "\\frac{2(1-(-1)^k)}{\\pi k^3}"), ("k-squared", "\\frac{4(1-(-1)^k)}{\\pi k^2}")],
                integers=["k"]),
    feedback=fb("Integrating by parts twice gives $b_k = \\tfrac{4(1 - (-1)^k)}{\\pi k^3}$. It is 0 for even $k$.",
                "Integrate by parts twice. Each time a factor $1/k$ appears.",
                {"one-over-pi": "You used the factor $1/\\pi$ in place of $2/\\pi$. The integral gives $2(1 - (-1)^k)/k^3$, and the prefactor doubles it.",
                 "k-squared": "You lost a power of $k$. Two integrations by parts give $1/k^3$, not $1/k^2$."}),
    explain="Two integrations by parts give $\\int_0^\\pi x(\\pi - x)\\sin kx\\,dx = 2(1 - (-1)^k)/k^3$. Multiplying by $2/\\pi$ gives $b_k$. The values are $8/\\pi = 2.5465$ at $k = 1$, 0 at $k = 2$ and $0.0943$ at $k = 3$.")


# ---------------------------------------------------------------- P8 code
def explicit_heat(u0, D, dx, T):
    dt_max = dx * dx / (2 * D)
    steps = max(1, math.ceil(T / dt_max - 1e-9))
    dt = T / steps
    lam = D * dt / (dx * dx)
    u = list(u0)
    n = len(u)
    for _ in range(steps):
        new = u[:]
        for i in range(1, n - 1):
            new[i] = u[i] + lam * (u[i + 1] - 2 * u[i] + u[i - 1])
        u = new
    return u


def sine_mix(n, dx):
    return [round(math.sin(math.pi * i * dx) + 0.5 * math.sin(3 * math.pi * i * dx), 12) if 0 < i < n - 1 else 0.0 for i in range(n)]


SINE = [0.0] + [math.sin(math.pi * i * 0.05) + 0.5 * math.sin(3 * math.pi * i * 0.05) for i in range(1, 20)] + [0.0]
# clean the end values (sin(pi) is 1e-16, not 0)
SINE[0] = 0.0
SINE[20] = 0.0
SPIKE = [0.0] * 21
SPIKE[10] = 1.0
WIDE = [0.0] + [math.exp(-((i * 0.04 - 1.0) ** 2) / (2 * 0.2 ** 2)) for i in range(1, 50)] + [0.0]
SMALL_T_U = [0.0, 0.5, 1.0, 0.5, 0.0]
BIG_D_U = [0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0]
CEIL_U = [0.0, 3.0, 6.0, 3.0, 0.0]


def fmt(xs):
    return "[" + ", ".join(repr(round(x, 12)) for x in xs) + "]"


SINE_R = [round(x, 12) for x in SINE]
SINE_L = "[" + ", ".join(repr(x) for x in SINE_R) + "]"
WIDE_R = [round(x, 12) for x in WIDE]
WIDE_L = "[" + ", ".join(repr(x) for x in WIDE_R) + "]"

STARTER = '''def explicit_heat(u0, D, dx, T):
    """Run the explicit scheme on the grid values u0 (the two ends stay 0).
    Use equal steps, as few as keep lambda = D*dt/dx**2 at most 1/2.
    Return the final list of grid values."""
    dt_max = dx * dx / (2 * D)      # the largest stable step
    steps = int(T / dt_max)
    dt = T / steps
    lam = D * dt / (dx * dx)
    u = list(u0)
    for _ in range(steps):
        new = u[:]
        for i in range(1, len(u) - 1):
            new[i] = u[i] + lam * (u[i + 1] - 2 * u[i] + u[i - 1])
        u = new
    return u
'''

SOLUTION = '''import math

def explicit_heat(u0, D, dx, T):
    dt_max = dx * dx / (2 * D)
    steps = max(1, math.ceil(T / dt_max - 1e-9))
    dt = T / steps
    lam = D * dt / (dx * dx)
    u = list(u0)
    for _ in range(steps):
        new = u[:]
        for i in range(1, len(u) - 1):
            new[i] = u[i] + lam * (u[i + 1] - 2 * u[i] + u[i - 1])
        u = new
    return u
'''

# tests: (call, expect literal, tolerance)
_t = []
_t.append(("explicit_heat(SINE, 0.15, 0.05, 0.43)", SINE_R and fmt(explicit_heat(SINE_R, 0.15, 0.05, 0.43))))
_t.append(("explicit_heat(SPIKE, 0.15, 0.05, 0.43)", fmt(explicit_heat(SPIKE, 0.15, 0.05, 0.43))))
_t.append(("explicit_heat(WIDE, 0.08, 0.04, 1.12)[25]", repr(explicit_heat(WIDE_R, 0.08, 0.04, 1.12)[25])))
_t.append(("explicit_heat([0.0, 0.5, 1.0, 0.5, 0.0], 0.2, 0.25, 0.001)", fmt(explicit_heat(SMALL_T_U, 0.2, 0.25, 0.001))))
_t.append(("explicit_heat([0.0] * 11, 0.3, 0.1, 2.0)", fmt([0.0] * 11)))
_t.append(("explicit_heat([0.0, 1.0, 2.0, 3.0, 2.0, 1.0, 0.0], 3.0, 0.1, 2.0)", fmt(explicit_heat(BIG_D_U, 3.0, 0.1, 2.0))))
_t.append(("explicit_heat([0.0, 3.0, 6.0, 3.0, 0.0], 0.2, 0.1, 0.3)", fmt(explicit_heat(CEIL_U, 0.2, 0.1, 0.3))))
_t.append(("len(explicit_heat([0.0, 1.0, 0.0], 0.1, 1.0, 0.5))", "3"))

PRELUDE = ("import math\nSINE = " + SINE_L + "\n"
           "SPIKE = [0.0] * 21\nSPIKE[10] = 1.0\n"
           "WIDE = " + WIDE_L + "\n")

CODE_WIDGET = {
    "kind": "code", "language": "python", "starter": STARTER, "solution": SOLUTION, "prelude": PRELUDE,
    "examples": [
        {"call": "explicit_heat([0.0, 1.0, 0.0], 0.1, 1.0, 0.5)", "expect": "[0.0, 0.9, 0.0]", "compare": "isclose", "tol": {"abs": 1e-9}}],
    "tests": [],
    "how": "Check runs 8 hidden tests on grids from 3 to 51 points. They hold a sine mix, a spike and a wide bump. They also hold a short time, an all-zero start, a case needing 1,200 steps and a `ceil` rounding trap. Each list must match to $10^{-9}$.",
}
for call, expect in _t:
    case = {"call": call, "expect": expect, "compare": "isclose", "tol": {"abs": 1e-9}}
    CODE_WIDGET["tests"].append(case)

P[8] = item(
    "e-explicit-code", 5, ["pe-fd"], ["explicit-scheme"], 480,
    title="The explicit heat scheme",
    prose="The explicit scheme steps $u_i^{n+1} = u_i^n + \\lambda(u_{i+1}^n - 2u_i^n + u_{i-1}^n)$ with $\\lambda = D\\,\\Delta t/\\Delta x^2$. It is stable only when $\\lambda \\le \\tfrac12$. The grid list `u0` has its two end values fixed at 0.",
    question="Write `explicit_heat(u0, D, dx, T)`. Use the fewest equal time steps that keep $\\lambda \\le \\tfrac12$, run them, and return the final list of grid values.",
    widget=CODE_WIDGET,
    feedback=fb("The step count is the ceiling of $T/\\Delta t_{\\max}$ with $\\Delta t_{\\max} = \\Delta x^2/(2D)$. A floor leaves $\\lambda$ above one half.",
                "Run the examples, then test a case where $T/\\Delta t_{\\max}$ is not a whole number."),
    explain="The largest stable step is $\\Delta x^2/(2D)$, so use $\\lceil T/\\Delta t_{\\max}\\rceil$ equal steps with a small guard for rounding. Update only the interior points, so the ends stay 0. A floor takes one step too few, and $\\lambda$ passes one half.")

ITEMS = P
