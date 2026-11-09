"""Second read of the three analysis derivations: every number in the models and
rubrics recomputed by two routes (Fractions or sympy, and mpmath), and the claims
the models make about smallest k, N and K checked by brute force.
Exit 0 when every expectation below holds. Run from this folder with the venv Python."""
import sys, math
from fractions import Fraction as F
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


# ---------- L1 binary fractions in (1/3, 0.34) ----------
a, b = F(1, 3), F(34, 100)
check(b - a == F(1, 150) and F(102 - 100, 300) == F(1, 150), "L1 b - a = 1/150 (two routes)")
k = next(k for k in range(20) if 2**k > 1 / (b - a))
check(k == 8 and (150).bit_length() == 8 and 2**7 == 128 and 2**8 == 256, "L1 the proof's k = 8 (by search and by bit length)")
m = math.floor(2**k * a) + 1
check(m == 86 and 2**k * a == F(256, 3), "L1 m = 86, least integer above 256/3")
check(F(86, 256) == F(43, 128) and float(F(86, 256)) == 0.3359375 and a < F(86, 256) < b, "L1 86/256 = 43/128 = 0.3359375 lies in (1/3, 0.34)")
works = [j for j in range(0, 9) if any(a < F(n, 2**j) < b for n in range(0, 2**j + 1))]
check(works == [7, 8], f"L1 brute force over every numerator: k works exactly for {works}; smallest is 7")
check(F(21, 64) == F(328125, 10**6) and F(22, 64) == F(34375, 10**5) and F(21, 64) < a and F(22, 64) > b, "L1 k = 6: 21/64 = 0.328125 < 1/3 and 22/64 = 0.34375 > 0.34")
# the proof's recipe on many random pairs: k from 2^k > 1/(b-a), m least integer above 2^k a
import random
random.seed(7)
ok = True
for _ in range(2000):
    x = F(random.randint(-10**6, 10**6), random.randint(1, 10**4)); y = x + F(1, random.randint(1, 10**6))
    kk = next(j for j in range(80) if 2**j > 1 / (y - x)); mm = math.floor(2**kk * x) + 1
    ok &= x < F(mm, 2**kk) < y
check(ok, "L1 the recipe lands strictly inside 2,000 random gaps")
# the float remark: every double is m/2^k, but not every m/2^k is a double
check(F(0.1).denominator & (F(0.1).denominator - 1) == 0, "L1 a float such as 0.1 is m/2^k (denominator a power of 2)")
check(float(2**53 + 1) != 2**53 + 1, "L1 2^53 + 1 (m = 2^53 + 1, k = 0) is a binary fraction no double holds (AN1-1)")

# ---------- L2 a_{n+1} = (a_n^2 + 4)/5 ----------
seq = [F(2)]
for _ in range(13):  # exact terms a_1 to a_14 (digits double each step)
    seq.append((seq[-1] ** 2 + 4) / 5)
check(seq[1] == F(8, 5), "L2 a_2 = 8/5")
check(all(1 < seq[i + 1] < seq[i] <= 2 for i in range(13)), "L2 1 < a_{n+1} < a_n <= 2 for n = 1 to 13 (exact)")
check(all(0 < seq[n - 1] - 1 <= F(3, 5) ** (n - 1) for n in range(1, 15)), "L2 0 < a_n - 1 <= (3/5)^(n-1) for n = 1 to 14 (exact)")
x = sp.symbols("x")
check(sp.expand((x**2 + 4) / 5 - 1 - (x - 1) * (x + 1) / 5) == 0 and sp.expand((x**2 + 4) / 5 - x - (x - 1) * (x - 4) / 5) == 0, "L2 both factorisations are identities")
check(sorted(sp.solve(sp.Eq(x, (x**2 + 4) / 5), x)) == [1, 4], "L2 the fixed points are 1 and 4")
p13, p14 = F(3, 5) ** 13, F(3, 5) ** 14
check(abs(float(p13) - 0.001306) < 5e-7 and abs(float(p14) - 0.000784) < 5e-7 and p13 > F(1, 1000) > p14, f"L2 (3/5)^13 = {float(p13):.7f} > 0.001 > (3/5)^14 = {float(p14):.7f}")
Nb = next(n for n in range(1, 100) if F(3, 5) ** (n - 1) < F(1, 1000))
check(Nb == 15 and math.ceil(1 + math.log(1e-3) / math.log(0.6)) == 15, "L2 N = 15 from the bound (search and logarithms)")
first = next(n for n in range(1, 15) if seq[n - 1] - 1 < F(1, 1000))
check(first == 10, "L2 first n with a_n - 1 < 0.001 is 10")
check(abs(float(seq[8] - 1) - 0.00167) < 5e-6 and abs(float(seq[9] - 1) - 0.00067) < 5e-6, f"L2 a_9 - 1 = {float(seq[8] - 1):.6f}, a_10 - 1 = {float(seq[9] - 1):.6f}")
mp_seq = [mp.mpf(2)]
for _ in range(40):
    mp_seq.append((mp_seq[-1] ** 2 + 4) / 5)
check(all(0 < mp_seq[n - 1] - 1 <= mp.mpf(3) ** (n - 1) / mp.mpf(5) ** (n - 1) for n in range(1, 41)), "L2 the bound holds for n = 1 to 40 at 40 digits")
check(abs(mp_seq[9] - 1 - mp.mpf(seq[9].numerator) / seq[9].denominator + 1) < 1e-30, "L2 a_10 by mpmath matches the Fraction")
check(abs((mp_seq[30] - 1) / (mp_seq[29] - 1) - 0.4) < 1e-3, "L2 near the limit the gap ratio is about 2/5")

# ---------- L3 sum 1/(n (ln n)^2) ----------
X = sp.symbols("X", positive=True)
f = 1 / (x * sp.log(x) ** 2)
check(sp.simplify(sp.diff(-1 / sp.log(x), x) - f) == 0, "L3 d/dx(-1/ln x) = 1/(x (ln x)^2)")
check(sp.limit(1 / sp.log(2) - 1 / sp.log(X), X, sp.oo) == 1 / sp.log(2) and abs(1 / math.log(2) - 1.4427) < 5e-5, "L3 the integral from 2 tends to 1/ln 2 = 1.4427")
q = mp.quad(lambda t: 1 / (t * mp.log(t) ** 2), [2, 10, 100, 1e3, 1e4, 1e5, 1e6])
check(abs(q - (1 / mp.log(2) - 1 / mp.log(10**6))) < 1e-15, "L3 quadrature on [2, 10^6] agrees with 1/ln 2 - 1/ln 10^6")
check(sp.simplify(sp.diff(f, x) + (sp.log(x) + 2) / (x**2 * sp.log(x) ** 3)) == 0, "L3 f' = -(ln x + 2)/(x^2 (ln x)^3) < 0 on [2, oo): f decreases")
e10 = math.exp(10)
check(abs(e10 - 22026.4658) < 1e-4 and math.log(22027) > 10 > math.log(22026), f"L3 e^10 = {e10:.4f}; ln 22027 = {math.log(22027):.6f}, ln 22026 = {math.log(22026):.6f}")
check(abs(math.log(22027) - 10.000024) < 5e-7 and abs(math.log(22026) - 9.999979) < 5e-7, "L3 the model's 10.000024 and 9.999979")
ratio_ok = all(1 - 1 / (n * math.log(n)) <= math.log(n) / math.log(n + 1) < 1 for n in range(2, 20000))
check(ratio_ok, "L3 1 - 1/(n ln n) <= ln n / ln(n+1) < 1 for n = 2 to 19,999")


G = lambda t: 1 / (t * mp.log(t) ** 2)


def tail(K):  # sum over n > K by Euler-Maclaurin from K + 1: integral + f/2 - f'/12 + f'''/720
    a = mp.mpf(K + 1)
    return 1 / mp.log(a) + G(a) / 2 - mp.diff(G, a) / 12 + mp.diff(G, a, 3) / 720


def tail_direct(K, M=400000):  # a second route: direct sum to M, Euler-Maclaurin after
    return mp.fsum(G(mp.mpf(n)) for n in range(K + 1, M + 1)) + tail(M)


t26, t27 = tail(22026), tail(22027)
check(abs(t26 - tail_direct(22026)) < 1e-15, f"L3 tail after 22,026 by two routes: {mp.nstr(t26, 12)}")
check(t26 < 0.1 and t27 < 0.1 and tail(22025) > 0.1, f"L3 true tails: after 22,025 {mp.nstr(tail(22025), 10)}, 22,026 {mp.nstr(t26, 10)}, 22,027 {mp.nstr(t27, 10)}")
true_min = next(K for K in range(22000, 22100) if tail(K) < 0.1)
print(f"info L3 the true smallest K with tail < 0.1 is {true_min}")
check(true_min == 22026, "L3 so the model's '22,026 or 22,027' holds; the true value is 22,026")
for K in (100, 5000, 22025):
    check(1 / mp.log(K + 1) <= tail(K) <= 1 / mp.log(K), f"L3 1/ln(K+1) <= tail <= 1/ln K at K = {K}")

print(f"\n{len(BAD)} failures")
sys.exit(1 if BAD else 0)
