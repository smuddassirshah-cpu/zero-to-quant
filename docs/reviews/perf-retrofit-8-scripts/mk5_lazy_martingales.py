"""markov L5 h-build-lazy-martingales, second read. Run from this folder with the venv Python.
Every model line re-derived with SymPy and with exact Fractions over all paths of
up to 8 moves (the one-step means of both martingales, for several p, q); the
uniqueness claims; the ruin chance three ways (optional stopping, first-step
equations solved exactly, the exact law of S at stopping by dynamic programming);
the block bound on P(T > n) and the E[T] bound that condition (2) needs (MK5-2)."""
import itertools, sys
from fractions import Fraction as F
import sympy as sp

bad = 0


def check(c, m):
    global bad
    print(("ok   " if c else "FAIL ") + m)
    bad += not c


p, q, th, a, b, i0 = sp.symbols("p q theta a b i", real=True)
r = 1 - p - q
mu = p - q
EX2 = p + q
sig2 = sp.expand(EX2 - mu ** 2)
check(sp.simplify(sig2 - (p + q - (p - q) ** 2)) == 0, "sigma^2 = p + q - (p - q)^2")
check(sp.expand((p + q) ** 2 - (p - q) ** 2 - 4 * p * q) == 0, "with p + q = 1, 1 - (p - q)^2 = 4pq")

# one-step change of (S - a n)^2 - b n, as a polynomial in Z = S_n - a n
Z = sp.symbols("Z")
change = sp.expand(sum(pr * ((Z + x - a) ** 2 - b) for x, pr in [(1, p), (-1, q), (0, r)]) - Z ** 2)
want = sp.expand(2 * (mu - a) * Z + sum(pr * (x - a) ** 2 for x, pr in [(1, p), (-1, q), (0, r)]) - b)
check(sp.simplify(change - want) == 0, "one-step change 2(mu - a)Z + E[(X - a)^2] - b")
sol = sp.solve([sp.Poly(change, Z).coeffs()[0], change.subs(Z, 0)], [a, b], dict=True)
check(len(sol) == 1 and sp.simplify(sol[0][a] - mu) == 0 and sp.simplify(sol[0][b] - sig2) == 0, "change 0 for two values of Z only at a = p - q, b = sigma^2")

# power: E[theta^X] = 1 exactly at theta = 1 and q/p
ex = p * th + r + q / th
check(sp.expand(sp.factor(sp.expand(th * (ex - 1)))) == sp.expand((th - 1) * (p * th - q)), "theta(E[theta^X] - 1) = (theta - 1)(p theta - q)")
check(set(sp.solve(sp.Eq(ex, 1), th)) == {1, q / p}, "roots 1 and q/p, r drops out")

# exact check over all paths of 8 moves, several (p, q)
for pp, qq in [(F(3, 10), F(2, 10)), (F(1, 5), F(1, 2)), (F(1, 2), F(1, 3)), (F(3, 5), F(2, 5))]:
    rr = 1 - pp - qq
    m, s2 = pp - qq, pp + qq - (pp - qq) ** 2
    T = qq / pp
    ok = True
    for n in range(0, 8):
        for path in itertools.product([1, -1, 0], repeat=n):
            S = 2 + sum(path)
            M1 = (S - m * n) ** 2 - s2 * n
            nxt1 = sum(pr * ((S + x - m * (n + 1)) ** 2 - s2 * (n + 1)) for x, pr in [(1, pp), (-1, qq), (0, rr)])
            nxt2 = sum(pr * T ** (S + x) for x, pr in [(1, pp), (-1, qq), (0, rr)])
            ok &= (nxt1 == M1) and (nxt2 == T ** S)
    check(ok, "p = %s, q = %s: both one-step means hold exactly on every path to n = 7" % (pp, qq))

# part 3
P3, Q3 = F(3, 10), F(2, 10)
TH = Q3 / P3
Pr = (1 - TH ** 2) / (1 - TH ** 5)
check(TH == F(2, 3) and Pr == F(135, 211) and F(5, 9) / F(211, 243) == F(135, 211), "theta = 2/3, P = (5/9)/(211/243) = 135/211")
check(round(float(Pr), 3) == 0.640 and P3 ** 5 == F(243, 100000) and float(P3 ** 5) == 0.00243, "135/211 = 0.640 and 0.3^5 = 0.00243")
h = sp.symbols("h0:6")
eqs = [sp.Eq(h[0], 0), sp.Eq(h[5], 1)] + [sp.Eq(h[k], sp.Rational(3, 10) * h[k + 1] + sp.Rational(2, 10) * h[k - 1] + sp.Rational(5, 10) * h[k]) for k in range(1, 5)]
hs = sp.solve(eqs, h)
check(hs[h[2]] == sp.Rational(135, 211), "first-step equations with the pause: h_2 = 135/211")
eqs2 = [sp.Eq(h[0], 0), sp.Eq(h[5], 1)] + [sp.Eq(h[k], sp.Rational(6, 10) * h[k + 1] + sp.Rational(4, 10) * h[k - 1]) for k in range(1, 5)]
check(sp.solve(eqs2, h)[h[2]] == sp.Rational(135, 211), "the no-pause walk with up chance 0.6 gives the same 135/211")

# exact law of S at time n by dynamic programming; block bound; E[T]
dist = {2: F(1)}
hit5 = F(0)
tail = []
ET = F(0)
for n in range(1, 401):
    ET += sum(dist.values())          # adds P(T > n - 1)
    new = {}
    for s, pr in dist.items():
        for x, px in [(1, P3), (-1, Q3), (0, 1 - P3 - Q3)]:
            new[s + x] = new.get(s + x, 0) + pr * px
    hit5 += new.pop(5, 0)
    new.pop(0, None)
    dist = new
    tail.append(sum(dist.values()))
check(all(float(tail[5 * k - 1]) <= (1 - 0.00243) ** k for k in range(1, 80)), "P(T > 5k) <= (1 - 0.00243)^k for k = 1 to 79")
check(abs(float(hit5) - 135 / 211) < 1e-12, "P(hit 5 by n = 400) = %.12f, the tail beyond is %.1e" % (float(hit5), float(tail[-1])))
check(float(ET) < 5 / 0.00243, "E[T] about %.2f (sum to n = 400), under the bound 5 / 0.00243 = %.0f, so condition (2) also holds" % (float(ET), 5 / 0.00243))
check(abs(float(ET) - (5 * 135 / 211 - 2) / 0.1) < 1e-6, "E[T] = %.6f matches Wald, (5P - 2)/(p - q)" % float(ET))
print("problems:", bad)
sys.exit(1 if bad else 0)
