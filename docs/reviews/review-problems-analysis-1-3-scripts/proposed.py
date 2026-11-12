"""Second read, analysis problems-1 to -3: the numbers of the proposed fixes, each by two routes.

Run from the repo root: <venv>/bin/python docs/reviews/review-problems-analysis-1-3-scripts/proposed.py   (exit 0)
"""
import math
import sys
from fractions import Fraction as Fr

checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    print(("ok   " if cond else "FAIL ") + label)
    fails += not cond


# ---- finding 1: p-cube-root-twenty with four halvings (review-1 asks the left end after 3 halvings of [2, 3])
lo, hi = Fr(2), Fr(3)
trail = []
for _ in range(4):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if m ** 3 < 20 else (lo, m)
    trail.append((float(lo), float(hi)))
print("trail", trail)
ok((lo, hi) == (Fr(43, 16), Fr(11, 4)), "after four halvings [2.6875, 2.75]")
ok(round(float(Fr(43, 16) ** 3), 2) == 19.41, "2.6875^3 = 19.41 (to 2 places), below 20")
ok(2.6875 < 20 ** (1 / 3) < 2.75, "route 2: the root 2.7144 lies inside")
miss = 43 ** 3 - 20 * 16 ** 3
ok(43 ** 3 == 79507 and 20 * 16 ** 3 == 81920 and miss == -2413, "miss -2413")
ok(Fr(43, 16) ** 3 - 20 == Fr(miss, 16 ** 3), "route 2: (p/q)^3 - 20 = miss/q^3")
print("slips: sign", -miss, "squares", 43 ** 2 - 20 * 16 ** 2, "no-twenty", 43 ** 3 - 16 ** 3)
s = Fr(43, 16)
top, bot = 3 * s ** 2 + 3 * s + 1, 20 - s ** 3
print("3s^2", float(3 * s ** 2), "3s", float(3 * s), "top", float(top), "s^3", float(s ** 3), "bottom", float(bot), "bound", float(top / bot))
n = math.floor(top / bot) + 1
ok(n == 53 and round(float(top / bot), 2) == 52.16, "bound 52.16, n = 53")
ok((s + Fr(1, 53)) ** 3 < 20 and round(float((s + Fr(1, 53)) ** 3), 2) == 19.82, "(2.6875 + 1/53)^3 = 19.82 < 20")
print("slips: round-down", n - 1, "; +1 dropped", float((top - 1) / bot), "->", math.floor((top - 1) / bot) + 1, "; 3s^2 only", float(3 * s ** 2 / bot), "->", math.floor(3 * s ** 2 / bot) + 1)
ok(math.floor((top - 1) / bot) + 1 == 51 and math.floor(3 * s ** 2 / bot) + 1 == 37, "slip values 51 and 37")

# ---- finding 3: p-sum-law-band with new sequences, limits and band (l7 uses limits 3 and 2, the band 5 +/- 0.1 and halves of 0.05)
a = lambda i: Fr(8 * i + 3, 2 * i + 5)
b = lambda i: Fr(3 * i - 1, i + 1)
ok(all(4 - a(i) == Fr(17, 2 * i + 5) and 3 - b(i) == Fr(4, i + 1) for i in range(1, 3000)), "gaps 17/(2n+5) and 4/(n+1), both terms below their limits")
ok(a(1) == Fr(11, 7) and b(1) == 1, "first terms 11/7 and 1")
g1 = lambda i: Fr(17, 2 * i + 5)
g2 = lambda i: Fr(4, i + 1)
gs = lambda i: g1(i) + g2(i)
first = lambda g, e: max(i for i in range(1, 3000) if not g(i) < e) + 1
half, full = Fr(2, 100), Fr(4, 100)
N1, N2 = first(g1, half), first(g2, half)
ok(N1 == 423 and Fr(850 - 5, 2) == Fr(845, 2), "N1 = 423 (2n + 5 > 850, n > 422.5)")
ok(N2 == 200 and g2(199) == half, "N2 = 200 (n > 199; the gap at 199 is 0.02 exactly)")
print("gap of a at 422:", float(g1(422)), "; full-band slips:", first(g1, full), first(g2, full), "; min", min(N1, N2), "sum", N1 + N2)
ok(first(g1, full) == 211 and first(g2, full) == 100, "full-band slips 211 and 100")
Nt = first(gs, full)
print("true N", Nt, "gap at N-1", float(gs(Nt - 1)), "gap at N", float(gs(Nt)))
# route 2: the quadratic 0.04 (2n+5)(n+1) = 17(n+1) + 4(2n+5)
A_, B_, C_ = Fr(8, 100), Fr(28, 100) - 25, Fr(20, 100) - 37
root = (-B_ + math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
ok(math.floor(root) + 1 == Nt, f"true N by the quadratic (root {root:.3f})")
ok(Nt == 311, "true N = 311")

print(f"{checks - fails} of {checks} checks passed")
sys.exit(1 if fails else 0)
