"""Check every number added to exams/topic-1.7.json (trees L4 extension).
Two methods per value: closed form (math.erf) and Simpson integration / enumeration.
Run: python3 docs/briefs/trees-scripts/check_exam_1_7.py
"""
import math, itertools
N = 0
def check(name, a, b, tol):
    global N
    assert abs(a - b) <= tol, f"{name}: A={a!r} B={b!r}"
    N += 1
def Phi_a(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def Phi_b(x, n=20000):
    lo = -10.0; h = (x - lo) / n
    f = lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi)
    s = f(lo) + f(x) + sum((4 if i % 2 else 2) * f(lo + i * h) for i in range(1, n))
    return s * h / 3
def call(S, K, r, s, T, Phi=Phi_a):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2)

# item 1 e-atm-rule
rule = 0.4 * 0.3 * math.sqrt(0.25) * 250
check("rule 15.00", rule, 0.4 * 0.3 * 0.5 * 250, 1e-12)
ex = call(250, 250, 0, .3, .25)
check("exact 14.95", ex, call(250, 250, 0, .3, .25, Phi_b), 1e-6); assert round(ex, 2) == 14.95 and abs(ex - 15) < 0.1
check("no-root 30.00", 0.4 * .3 * 250, 30.0, 1e-12)
check("time-not-root 7.50", 0.4 * .3 * .25 * 250, 7.5, 1e-12)
gain = call(250, 250, 0, .32, .25) - call(250, 250, 0, .30, .25)
check("gain exact 0.9944", gain, call(250, 250, 0, .32, .25, Phi_b) - call(250, 250, 0, .30, .25, Phi_b), 1e-6)
assert abs(gain - 1.0) <= 0.05 and round(gain, 4) == 0.9944
check("gain approx 15/0.3*0.02", 15 / 0.3 * 0.02, 1.0, 1e-12)
check("points-as-units 100", 15 / 0.3 * 2, 100.0, 1e-12)
check("one-point 0.50", 15 / 0.3 * 0.01, 0.5, 1e-12)
r1 = 0.4 * .3 * math.sqrt(1 / 12) * 250
check("month rule 8.6603", r1, 15 / math.sqrt(3), 1e-9); assert round(r1, 2) == 8.66
ex1 = call(250, 250, 0, .3, 1 / 12)
check("month exact 8.6347", ex1, call(250, 250, 0, .3, 1 / 12, Phi_b), 1e-6); assert abs(ex1 - 8.66) <= 0.1 and round(ex1, 4) == 8.6347
check("by-time 5.00", 15 / 3, 5.0, 1e-12)

# item 2 e-greek-signs
check("gamma peak 94.18", 100 * math.exp(-1.5 * .04), 94.1765, 1e-3)
def gam(S, K=100, s=.2, T=1):
    d1 = (math.log(S / K) + s * s * T / 2) / (s * math.sqrt(T)); return math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi) / (S * s * math.sqrt(T))
grid = [60 + i * 0.01 for i in range(8000)]
check("argmax gamma", max(grid, key=gam), 94.18, 0.02)
assert gam(100) > 0.0197 and round(gam(100), 4) == 0.0198 and gam(94.18) > gam(100) > gam(60) and gam(100) > gam(160)
pnl = -1000 * 0.5 * 0.0198 * 1e4 * (.28 ** 2 - .2 ** 2) * 21 / 252
check("pnl -316.80", pnl, -99000 * 0.0384 / 12, 1e-9)
check("pnl with 0.019847", -1000 * .5 * 0.019847 * 1e4 * .0384 / 12, -317.56, 0.01)
check("no-half", 2 * pnl, -633.6, 1e-9); check("vol-gap", -99000 * .08 / 12, -660, 1e-9); check("no-time", -99000 * .0384, -3801.6, 1e-9)

# item 3 e-bs-hedge parts 2
d1 = (math.log(80 / 75) + (.03 + .25 ** 2 / 2) * .5) / (.25 * math.sqrt(.5)); d2 = d1 - .25 * math.sqrt(.5)
disc = math.exp(-.015)
dig = disc * Phi_a(d2)
check("digital 0.6316", dig, disc * Phi_b(d2), 1e-6); assert round(dig, 4) == 0.6316
check("digital from table 0.6317", disc * 0.6412, 0.6317, 1e-4); assert abs(0.6316 - 0.6317) <= 0.0008
check("Phi(d2) 0.6412", Phi_a(d2), 0.6412, 6e-4)
check("no-discount ~0.6412", Phi_a(d2), 0.6412, 6e-4)
check("d1-slip 0.6943", disc * Phi_a(d1), 0.6943, 5e-4); check("d1-slip table", disc * .7048, 0.6943, 1e-4)
check("put-slip 0.3535", disc * (1 - Phi_a(d2)), 0.3535, 5e-4)
# limit of call spread / width
w = 1e-3
cs = (call(80, 75 - w / 2, .03, .25, .5) - call(80, 75 + w / 2, .03, .25, .5)) / w
check("call spread limit", cs, dig, 1e-5)

# item 4 american put, Asian
S0, u, d, R, K = 50, 1.2, .8, 1.03, 52
q = (R - d) / (u - d); check("q 0.575", q, .575, 1e-12)
asian_enum = 0
for p in itertools.product([u, d], repeat=2):
    s1 = S0 * p[0]; s2 = s1 * p[1]; pr = (q if p[0] == u else 1 - q) * (q if p[1] == u else 1 - q)
    asian_enum += pr * max(K - (s1 + s2) / 2, 0)
asian_enum /= R ** 2
# recursion on (price, running sum)
def V(t, S, sm):
    if t == 2: return max(K - sm / 2, 0)
    return (q * V(t + 1, S * u, sm + S * u) + (1 - q) * V(t + 1, S * d, sm + S * d)) / R
asian_rec = V(0, S0, 0)
check("asian 4.5669", asian_enum, asian_rec, 1e-9); assert round(asian_enum, 2) == 4.57
check("asian formula", (.2444 * 8 + .1806 * 16) / 1.03 ** 2, 4.57, 0.01)
check("q(1-q) 0.2444", q * (1 - q), .2444, 5e-5); check("(1-q)^2 0.1806", (1 - q) ** 2, .1806, 5e-5)
# american and european
def Vam(S, t):
    h = max(K - S, 0)
    if t == 2: return h
    return max(h, (q * Vam(S * u, t + 1) + (1 - q) * Vam(S * d, t + 1)) / R)
def Veu(S, t):
    if t == 2: return max(K - S, 0)
    return (q * Veu(S * u, t + 1) + (1 - q) * Veu(S * d, t + 1)) / R
check("american 5.87", Vam(S0, 0), 5.87, 0.005); check("european 5.25", Veu(S0, 0), 5.25, 0.005)
assert Vam(S0, 0) > Veu(S0, 0) > asian_enum
# fix pass 2026-11-05: rounded learner answers against the widened tolerances
check("d1 rounded 0.54 accepted at tol 0.005", abs(0.54 - 0.5383) <= 0.005, True, 0)
check("d2 rounded 0.36 accepted at tol 0.005", abs(0.36 - 0.3615) <= 0.005, True, 0)
check("sigma-denominator slip 0.3807 still outside d2 tol", abs(0.3807 - 0.3615) > 0.005, True, 0)
check("digital 0.632 (three places) accepted at tol 0.0008", abs(0.632 - 0.6316) <= 0.0008, True, 0)
print(f"PASS: {N} checks")
