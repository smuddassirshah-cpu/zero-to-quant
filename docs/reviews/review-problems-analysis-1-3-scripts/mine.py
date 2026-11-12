"""Second read, analysis problems-1 to -3: the reader's own recompute.

Imports nothing from the author's script. Every sequence, set and series is typed here from the prose.
Route 1 is exact (fractions, sympy); route 2 is another method (brute search, floats, mpmath, direct iteration).
Each key, each wrong value and each number printed in a feedback or explanation line is compared with the JSON.

Run from the repo root with the scratchpad venv:
  <venv>/bin/python docs/reviews/review-problems-analysis-1-3-scripts/mine.py
Exit 0 when every check passes. CLAIM lines are findings of the review, not failures.
"""
import json
import math
import sys
from fractions import Fraction as Fr

import mpmath as mp
import sympy as sp

BASE = "app/content/courses/analysis/"
SETS = {n: json.load(open(f"{BASE}problems-{n}.json")) for n in (1, 2, 3)}
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", label)


def part(n, item, k):
    for it in SETS[n]["items"]:
        if it["id"] == item:
            return it["parts"][k - 1]
    raise KeyError(item)


def key(n, item, k, mine, label=None):
    """The stored key equals the reader's value and the band refuses nothing honest."""
    w = part(n, item, k)["widget"]
    ok(abs(w["answer"] - float(mine)) <= w["tol"]["abs"] + 1e-12, f"{n} {item} part {k} key {w['answer']} vs {mine}")


def wrong(n, item, k, wid, mine):
    w = part(n, item, k)["widget"]
    hit = [x for x in w["wrong"] if x["id"] == wid]
    ok(len(hit) == 1, f"{n} {item} part {k} wrong id {wid} present")
    if hit:
        ok(abs(hit[0]["value"] - float(mine)) <= hit[0]["tol"]["abs"] + 1e-12, f"{n} {item} part {k} wrong {wid} {hit[0]['value']} vs {mine}")
        # the slip's band must not touch the key's band
        ok(abs(hit[0]["value"] - w["answer"]) > hit[0]["tol"]["abs"] + w["tol"]["abs"], f"{n} {item} part {k} wrong {wid} band clear of key")
        ok(wid in part(n, item, k)["feedback"].get("byKey", {}), f"{n} {item} part {k} wrong {wid} has a line")


# ---------------------------------------------------------------- set 1
# p-cube-root-twenty
lo, hi = Fr(2), Fr(3)
trail = []
for _ in range(4):
    m = (lo + hi) / 2
    if m ** 3 < 20:
        lo = m
    else:
        hi = m
    trail.append((lo, hi))
ok(trail == [(Fr(5, 2), Fr(3)), (Fr(5, 2), Fr(11, 4)), (Fr(21, 8), Fr(11, 4)), (Fr(43, 16), Fr(11, 4))], "bisection trail, four halvings")
key(1, "p-cube-root-twenty", 1, lo)
wrong(1, "p-cube-root-twenty", 1, "right-end", hi)
wrong(1, "p-cube-root-twenty", 1, "one-short", trail[2][0])
# route 2: floats against the true root
r = 20 ** (1 / 3)
ok(2.6875 < r < 2.75, "cube root of 20 in [2.6875, 2.75]")
ok(round(2.5 ** 3, 3) == 15.625 and round(2.75 ** 3, 2) == 20.80 and round(2.625 ** 3, 2) == 18.09 and round(2.6875 ** 3, 2) == 19.41, "cubes printed")
key(1, "p-cube-root-twenty", 2, 43 ** 3 - 20 * 16 ** 3)
ok(43 ** 3 == 79507 and 20 * 16 ** 3 == 81920 and 79507 - 81920 == -2413, "miss")
ok(Fr(43, 16) ** 3 - 20 == Fr(-2413, 4096), "miss, route 2: (p/q)^3 - 20 = miss / q^3")
wrong(1, "p-cube-root-twenty", 2, "sign", 20 * 16 ** 3 - 43 ** 3)
wrong(1, "p-cube-root-twenty", 2, "squares", 43 ** 2 - 20 * 16 ** 2)
wrong(1, "p-cube-root-twenty", 2, "no-twenty", 43 ** 3 - 16 ** 3)
k, q, p, s, n, N, eps = sp.symbols("k q p s n N varepsilon", positive=True)
# p = 2k in p^3 = 20 q^3
sol = sp.solve(sp.Eq((2 * k) ** 3, 20 * q ** 3), q ** 3)[0]
ok(sp.simplify(5 * sol - 2 * k ** 3) == 0, "5q^3 = 2k^3")
ok(sp.simplify(5 * sp.Rational(1, 20) * (2 * k ** 3) - k ** 3 / 2) == 0, "cube-two slip: 2k^3 = 20q^3 gives k^3/2")
ok(sp.simplify(5 * (8 * k ** 3) / 20 * 2 - 4 * k ** 3) == 0, "half-only: 10q^3 = 4k^3")
# no fraction has cube 20, route 2: brute search
ok(all(pp ** 3 != 20 * qq ** 3 for qq in range(1, 400) for pp in range(2 * qq, 3 * qq + 1)), "no p/q with q < 400 cubes to 20")
# the inequality (s + 1/n)^3 <= s^3 + (3s^2 + 3s + 1)/n for n >= 1: difference is 3s(1/n - 1/n^2) + (1/n - 1/n^3) >= 0
diff = sp.expand(s ** 3 + (3 * s ** 2 + 3 * s + 1) / n - (s + 1 / n) ** 3)
ok(sp.simplify(diff - (3 * s * (n - 1) / n ** 2 + (n ** 2 - 1) / n ** 3)) == 0, "cube bound identity")
sv = Fr(43, 16)
top, bot = 3 * sv ** 2 + 3 * sv + 1, 20 - sv ** 3
ok(float(top) == 30.73046875 and float(bot) == 0.589111328125, "top and bottom at 2.6875")
ok(float(3 * sv ** 2) == 21.66796875 and float(3 * sv) == 8.0625 and float(sv ** 3) == 19.410888671875, "pieces at 2.6875")
bound = top / bot
ok(round(float(bound), 2) == 52.16, "bound 52.16")
key(1, "p-cube-root-twenty", 4, math.floor(bound) + 1)
wrong(1, "p-cube-root-twenty", 4, "round-down", math.floor(bound))
ok(math.floor((top - 1) / bot) + 1 == 51 and round(float((top - 1) / bot), 2) == 50.47, "dropping +1 gives 50.47, so 51")
wrong(1, "p-cube-root-twenty", 4, "no-plus-one", math.floor((top - 1) / bot) + 1)
ok(round(float(3 * sv ** 2 / bot), 2) == 36.78, "no-ones bound 36.78")
wrong(1, "p-cube-root-twenty", 4, "no-ones", math.floor(3 * sv ** 2 / bot) + 1)
ok(round(float((sv + Fr(1, 53)) ** 3), 2) == 19.82 and (sv + Fr(1, 53)) ** 3 < 20, "(2.6875 + 1/53)^3 = 19.82 < 20")
# the bound is sufficient at every n beyond it (route 2: direct test), and is not the least n with s + 1/n in S
ok(all((sv + Fr(1, nn)) ** 3 < 20 for nn in range(53, 2000)), "every n >= 53 puts 2.6875 + 1/n in S")
least = min(nn for nn in range(1, 100) if (sv + Fr(1, nn)) ** 3 < 20)
print(f"NOTE 1 p-cube-root-twenty part 4: the least n with 2.6875 + 1/n in S is {least}; the part asks for the least n beyond the bound, 53")

# p-climbing-fractions
a = lambda nn: Fr(5 * nn - 4, nn + 1)
ok([a(i) for i in range(1, 5)] == [Fr(1, 2), Fr(2), Fr(11, 4), Fr(16, 5)], "first terms of A")
ok(all(a(i) < a(i + 1) < 5 for i in range(1, 5000)), "A climbs and stays below 5")
key(1, "p-climbing-fractions", 1, min(a(i) for i in range(1, 5000)))
wrong(1, "p-climbing-fractions", 1, "n-zero", Fr(5 * 0 - 4, 0 + 1))
wrong(1, "p-climbing-fractions", 1, "sup", 5)
ok(sp.simplify(5 - (5 * n - 4) / (n + 1) - 9 / (n + 1)) == 0, "gap 9/(n+1)")
ok(all(5 - a(i) == Fr(9, i + 1) for i in range(1, 200)), "gap, route 2")
ok(sp.simplify((5 * (n + 1) - (5 * n + 4)) - 1) == 0, "minus-four slip gives 1/(n+1)")
thr = sp.solve(sp.Eq(9 / (n + 1), eps), n)[0]
ok(sp.simplify(thr - (9 / eps - 1)) == 0 and sp.simplify(thr - (9 - eps) / eps) == 0, "threshold 9/eps - 1 and its accept form")
e = Fr(4, 1000)
ok(9 / e - 1 == 2249, "bound 2249")
first = min(i for i in range(1, 5000) if a(i) > 5 - e)
key(1, "p-climbing-fractions", 5, first)
ok(first == 2250 and a(2249) == 5 - e, "2249 gives 4.996 exactly, 2250 is the first above")
wrong(1, "p-climbing-fractions", 5, "equal", 2249)
wrong(1, "p-climbing-fractions", 5, "no-minus-one", math.floor(9 / e) + 1)
ok(f"{9 / 2251:.7f}" == "0.0039982", "gap 9/2251")

# p-diagonal-fraction
rows = ["70329", "18096", "42571", "96053", "33418"]
diag = [rows[i][i] for i in range(5)]
ok(diag == list("78558"), "diagonal digits")
x = "".join("4" if d == "5" else "5" for d in diag)
key(1, "p-diagonal-fraction", 1, Fr(int(x), 10 ** 5))
wrong(1, "p-diagonal-fraction", 1, "diagonal", Fr(int("".join(diag)), 10 ** 5))
wrong(1, "p-diagonal-fraction", 1, "all-five", Fr(55555, 10 ** 5))
wrong(1, "p-diagonal-fraction", 1, "swapped", Fr(int("".join("5" if d == "5" else "4" for d in diag)), 10 ** 5))
A_, B_ = Fr(55445, 10 ** 5), Fr(55446, 10 ** 5)
# x = 0.55445 d6 d7 ... with digits 4 or 5: between 0.55445444... and 0.55445555...
ok(A_ < A_ + Fr(4, 9 * 10 ** 5) and A_ + Fr(5, 9 * 10 ** 5) < B_, "0.55445 < x < 0.55446")
nn_ = math.floor(1 / (B_ - A_)) + 1
key(1, "p-diagonal-fraction", 2, nn_)
ok(1 / (B_ - A_) == 100000, "1/(b - a) = 100000 exactly")
wrong(1, "p-diagonal-fraction", 2, "equal", 100000)
mm_ = math.floor(nn_ * A_) + 1
ok(nn_ * A_ == Fr(5544555445, 10 ** 5), "na = 55445.55445")
key(1, "p-diagonal-fraction", 3, mm_)
wrong(1, "p-diagonal-fraction", 3, "floor", math.floor(nn_ * A_))
wrong(1, "p-diagonal-fraction", 3, "used-b", math.floor(nn_ * B_) + 1)
ok(A_ < Fr(mm_, nn_) < B_, "a < m/n < b")
key(1, "p-diagonal-fraction", 4, Fr(mm_, nn_))
ok(f"{mm_ / nn_:.7f}" == "0.5544545" and mp.nstr(mp.mpf(mm_) / nn_, 10) == "0.5544544555", "m/n to 7 and 10 places")
wrong(1, "p-diagonal-fraction", 4, "n-slip", Fr(mm_, 100000))
# 7-place rounding and truncation both inside the band
w = part(1, "p-diagonal-fraction", 4)["widget"]
ok(all(abs(v - w["answer"]) <= w["tol"]["abs"] for v in (0.5544545, 0.5544544)), "7-place round and cut accepted")

# ---------------------------------------------------------------- set 2
an = lambda i: Fr(8 * i + 3, 2 * i + 5)
bn = lambda i: Fr(3 * i - 1, i + 1)
ok(sp.limit((8 * n + 3) / (2 * n + 5), n, sp.oo) == 4 and sp.limit((3 * n - 1) / (n + 1), n, sp.oo) == 3, "limits 4 and 3")
ok(all(4 - an(i) == Fr(17, 2 * i + 5) and 3 - bn(i) == Fr(4, i + 1) for i in range(1, 400)), "gaps 17/(2n+5) and 4/(n+1), both below the limit")
ok(3 + 4 * 5 == 23, "plus-one slip top is 23 in size")
half = Fr(2, 100)


def first_for_good(gap, e_, top=4000):
    """Least N with gap(n) < e for every n in [N, top]; gaps here fall, checked separately."""
    bad = [i for i in range(1, top) if not gap(i) < e_]
    return (max(bad) + 1) if bad else 1


g1 = lambda i: Fr(17, 2 * i + 5)
g2 = lambda i: Fr(4, i + 1)
gs = lambda i: g1(i) + g2(i)
ok(all(g1(i) > g1(i + 1) and g2(i) > g2(i + 1) for i in range(1, 4000)), "both gaps fall")
N1, N2 = first_for_good(g1, half), first_for_good(g2, half)
key(2, "p-sum-law-band", 2, N1)
ok(sp.Rational(850 - 5, 2) == sp.Rational(845, 2) and N1 == 423, "n > 422.5")
wrong(2, "p-sum-law-band", 2, "round-down", 422)
ok(f"{17 / 849:.5f}" == "0.02002", "gap at 422")
wrong(2, "p-sum-law-band", 2, "full-band", first_for_good(g1, 2 * half))
key(2, "p-sum-law-band", 3, N2)
ok(g2(199) == half, "gap at 199 is 0.02 exactly")
wrong(2, "p-sum-law-band", 3, "equal", 199)
wrong(2, "p-sum-law-band", 3, "full-band", first_for_good(g2, 2 * half))
key(2, "p-sum-law-band", 4, max(N1, N2))
wrong(2, "p-sum-law-band", 4, "min", min(N1, N2))
wrong(2, "p-sum-law-band", 4, "sum", N1 + N2)
ok(all(abs(an(i) + bn(i) - 7) == gs(i) for i in range(1, 400)), "|a_n + b_n - 7| is the sum of the gaps")
Ntrue = first_for_good(gs, 2 * half)
ok(Ntrue == 311 and N2 == 200, "true N 311, N2 200")
key(2, "p-sum-law-band", 5, Ntrue)
ok(f"{float(gs(310)):.5f}" == "0.04006" and f"{float(gs(311)):.5f}" == "0.03993", "sum gap at 310 and 311")
wrong(2, "p-sum-law-band", 5, "proof", max(N1, N2))
wrong(2, "p-sum-law-band", 5, "round-down", Ntrue - 1)
# route 2: the quadratic 0.04 (2n+5)(n+1) = 17(n+1) + 4(2n+5)
roots = sp.solve(sp.Eq(sp.Rational(4, 100) * (2 * n + 5) * (n + 1), 17 * (n + 1) + 4 * (2 * n + 5)), n)
ok(len(roots) == 1 and math.floor(roots[0]) + 1 == Ntrue, "true N by the quadratic")

# p-root-recursion
seq = [mp.mpf(1)]
mp.mp.dps = 30
for _ in range(40):
    seq.append(mp.sqrt(4 * seq[-1] + 21))
ok(seq[1] == 5, "a_2 = 5")
key(2, "p-root-recursion", 1, seq[2])
ok(mp.nstr(seq[2], 4) == "6.403" and abs(seq[2] ** 2 - 41) < 1e-20, "a_3 = sqrt 41 = 6.403")
wrong(2, "p-root-recursion", 1, "no-root", 41)
wrong(2, "p-root-recursion", 1, "a2", 5)
ok(all(seq[i] < seq[i + 1] < 7 for i in range(30)), "terms rise and stay below 7")
L = sp.symbols("L")
ok(set(sp.solve(sp.Eq(L ** 2, 4 * L + 21), L)) == {7, -3} and sp.sqrt(4 * 7 + 21) == 7, "limit equation roots 7 and -3; 7 solves the unsquared form")
key(2, "p-root-recursion", 3, 7)
ok(abs(seq[40] - 7) < mp.mpf(10) ** -15, "iteration reaches 7")
wrong(2, "p-root-recursion", 3, "other-root", -3)
wrong(2, "p-root-recursion", 3, "bound-only", 4 * 7 + 21)
ok(all(abs((7 - seq[i + 1]) - 4 * (7 - seq[i]) / (7 + seq[i + 1])) < mp.mpf(10) ** -20 for i in range(30)), "7 - a_{n+1} = 4(7 - a_n)/(7 + a_{n+1})")
key(2, "p-root-recursion", 4, Fr(4, 8))
wrong(2, "p-root-recursion", 4, "no-term", Fr(4, 7))
wrong(2, "p-root-recursion", 4, "used-a2", Fr(4, 12))
ok(all(7 - seq[i] <= 6 * mp.mpf(0.5) ** i for i in range(40)), "7 - a_n <= 6 (1/2)^(n-1)")


def first_pow(c, ratio, e_, shift=1):
    i = 1
    while not c * ratio ** (i - shift) < e_:
        i += 1
    return i


key(2, "p-root-recursion", 5, first_pow(6, Fr(1, 2), Fr(1, 1000)))
ok(2 ** 12 == 4096 and 2 ** 13 == 8192, "powers of 2")
wrong(2, "p-root-recursion", 5, "no-six", first_pow(1, Fr(1, 2), Fr(1, 1000)))
wrong(2, "p-root-recursion", 5, "power-n", first_pow(6, Fr(1, 2), Fr(1, 1000), shift=0))
wrong(2, "p-root-recursion", 5, "slip-4", first_pow(6, Fr(4, 7), Fr(1, 1000)))
true_first = min(i + 1 for i in range(40) if 7 - seq[i] < mp.mpf("0.001"))
ok(true_first == 9 and mp.nstr(seq[8], 5) == "6.9997", "a_9 = 6.9997 is the first term within 0.001")

# p-two-strands-cauchy
c = lambda i: (-1) ** i * (2 - Fr(3, i))
ok([c(i) for i in range(1, 5)] == [1, Fr(1, 2), -1, Fr(5, 4)], "first terms")
ok(sp.limit(2 - 3 / n, n, sp.oo) == 2, "bracket tends to 2")
ok(abs(float(c(10 ** 6)) - 2) < 1e-5 and abs(float(c(10 ** 6 + 1)) + 2) < 1e-5, "strands near 2 and -2")
key(2, "p-two-strands-cauchy", 1, 2)
key(2, "p-two-strands-cauchy", 2, -2)
wrong(2, "p-two-strands-cauchy", 2, "first", c(1))
step = lambda i: abs(c(i + 1) - c(i))
ok(all(step(i) == (2 - Fr(3, i)) + (2 - Fr(3, i + 1)) for i in range(2, 500)), "step formula for n >= 2")
ok(step(1) == Fr(1, 2), "step at n = 1 is 0.5 (formula starts at n = 2)")
key(2, "p-two-strands-cauchy", 3, 4)
ok(abs(float(step(10 ** 6)) - 4) < 1e-5 and all(step(i) < step(i + 1) < 4 for i in range(2, 500)), "steps rise to 4")
key(2, "p-two-strands-cauchy", 4, min(i for i in range(1, 500) if step(i) >= 3))
ok(step(5) == Fr(29, 10) and f"{float(step(6)):.3f}" == "3.071" and f"{float(step(7)):.3f}" == "3.196", "steps at 5, 6, 7")
ok(2 - Fr(3, 5) == Fr(14, 10) and 2 - Fr(3, 6) == Fr(15, 10), "1.4 + 1.5")
ok(all(abs(c(i)) < 2 for i in range(1, 2000)), "|a_n| < 2 for every n")
# the Cauchy condition fails for every eps below 4 and holds at 4, so 'only for eps below 3' is false
ok(all(abs(c(i) - c(j)) < 4 for i in range(1, 80) for j in range(1, 80)), "all pairs under 4 apart")

# ---------------------------------------------------------------- set 3
t = lambda i: Fr(1, (i + 1) * (i + 3))
ok([t(i) for i in (1, 2, 3)] == [Fr(1, 8), Fr(1, 15), Fr(1, 24)], "first terms")
ok(sp.simplify(1 / ((n + 1) * (n + 3)) - sp.Rational(1, 2) * (1 / (n + 1) - 1 / (n + 3))) == 0, "c = 1/2")
key(3, "p-telescoping-tail", 1, Fr(1, 2))
SN = lambda M: Fr(5, 12) - Fr(1, 2 * (M + 2)) - Fr(1, 2 * (M + 3))
run = Fr(0)
good = True
for i in range(1, 1200):
    run += t(i)
    good &= run == SN(i)
ok(good, "S_N formula against the running sum, N = 1 to 1199")
ok(sp.summation(1 / ((n + 1) * (n + 3)), (n, 1, sp.oo)) == sp.Rational(5, 12), "sum 5/12 (sympy)")
key(3, "p-telescoping-tail", 3, Fr(5, 12))
wrong(3, "p-telescoping-tail", 3, "no-half", Fr(5, 6))
wrong(3, "p-telescoping-tail", 3, "one-start", Fr(1, 4))
tail = lambda M: Fr(5, 12) - SN(M)
Nt = min(i for i in range(1, 5000) if tail(i) < Fr(1, 1000))
key(3, "p-telescoping-tail", 4, Nt)
ok(f"{float(tail(997)):.7f}" == "0.0010005" and f"{float(tail(998)):.7f}" == "0.0009995", "tails at 997, 998")
wrong(3, "p-telescoping-tail", 4, "one-term", min(i for i in range(1, 5000) if Fr(1, 2 * (i + 2)) < Fr(1, 1000)))
wrong(3, "p-telescoping-tail", 4, "no-half", min(i for i in range(1, 5000) if Fr(1, i + 2) + Fr(1, i + 3) < Fr(1, 1000)))
wrong(3, "p-telescoping-tail", 4, "round-down", Nt - 1)
ok(sp.expand((n + 1) * (n + 3)) == n ** 2 + 4 * n + 3, "(n+1)(n+3)")
s2 = mp.nsum(lambda j: 1 / (j ** 2 + 4 * j + 7), [1, mp.inf])
ok(0 < s2 < mp.mpf(5) / 12, f"second series sums to {mp.nstr(s2, 6)}, below 5/12")
ok(sp.limit((n ** 2 + 4 * n + 7) / ((n + 1) ** 2 + 4 * (n + 1) + 7), n, sp.oo) == 1, "its ratios tend to 1")

# p-alternating-quarters
u = lambda i: Fr(i, 4 ** i)
ok([u(1), u(2), u(3)] == [Fr(1, 4), Fr(2, 16), Fr(3, 64)], "first sizes")
ok(sp.limit(((n + 1) / 4 ** (n + 1)) / (n / 4 ** n), n, sp.oo) == sp.Rational(1, 4), "ratio limit 1/4")
ok(all(u(i + 1) / u(i) == Fr(i + 1, 4 * i) for i in range(1, 50)) and all(u(i) > u(i + 1) for i in range(1, 200)), "ratio (n+1)/(4n); sizes decrease")
key(3, "p-alternating-quarters", 1, Fr(1, 4))
key(3, "p-alternating-quarters", 3, u(5))
ok(u(5) == Fr(5, 1024) and f"{float(u(5)):.4f}" == "0.0049", "a_5")
wrong(3, "p-alternating-quarters", 3, "a4", u(4))
wrong(3, "p-alternating-quarters", 3, "a6", u(6))
nb = min(i for i in range(1, 50) if u(i + 1) < Fr(1, 1000))
key(3, "p-alternating-quarters", 4, nb)
ok(u(6) == Fr(6, 4096) and u(7) == Fr(7, 16384) and f"{float(u(6)):.5f}" == "0.00146" and f"{float(u(7)):.5f}" == "0.00043", "a_6 and a_7")
wrong(3, "p-alternating-quarters", 4, "index", min(i for i in range(1, 50) if u(i) < Fr(1, 1000)))
PS = lambda M: sum((-1) ** (i + 1) * u(i) for i in range(1, M + 1))
key(3, "p-alternating-quarters", 5, PS(6))
ok(PS(6) == Fr(327, 2048) and 1024 - 512 + 192 - 64 + 20 - 6 == 654 and f"{float(PS(6)):.4f}" == "0.1597", "S_6 = 327/2048")
wrong(3, "p-alternating-quarters", 5, "s4", PS(4))
wrong(3, "p-alternating-quarters", 5, "sizes", sum(u(i) for i in range(1, 7)))
wrong(3, "p-alternating-quarters", 5, "s7", PS(7))
S_true = sp.summation((-1) ** (n + 1) * n / 4 ** n, (n, 1, sp.oo))
ok(S_true == sp.Rational(4, 25), "sum 4/25 (sympy)")
xq = Fr(1, 4)
ok(xq / (1 + xq) ** 2 == Fr(4, 25), "sum 4/25 (closed form x/(1+x)^2)")
ok(all(abs(Fr(4, 25) - PS(i)) <= u(i + 1) for i in range(1, 40)), "|S - S_n| <= a_{n+1}")
ok(abs(Fr(4, 25) - PS(6)) < Fr(43, 100000), "sum within 0.00043 of S_6")
true_n = min(i for i in range(1, 40) if abs(Fr(4, 25) - PS(i)) < Fr(1, 1000))
print(f"NOTE 3 p-alternating-quarters part 4: the true error is first below 0.001 at n = {true_n}; the bound certifies n = {nb}")
w5 = part(3, "p-alternating-quarters", 5)["widget"]
s7 = [x for x in w5["wrong"] if x["id"] == "s7"][0]
ok(abs(0.16 - s7["value"]) > s7["tol"]["abs"], "0.16 (the sum, and S_6 to 2 places) lies outside the s7 band")
wrong(3, "p-alternating-quarters", 5, "sum", Fr(4, 25))
ok(abs(0.1601 - s7["value"]) <= s7["tol"]["abs"] and abs(0.1597 - s7["value"]) > s7["tol"]["abs"], "0.1601 stays in s7, 0.1597 stays out")

# p-cube-root-greedy
mp.mp.dps = 30
eta = mp.altzeta(mp.mpf(1) / 3)
ok(mp.nstr(eta, 4) == "0.5718", f"sum in the usual order {mp.nstr(eta, 8)}")
ok(abs(mp.nsum(lambda j: (-1) ** (j + 1) / mp.cbrt(j), [1, mp.inf]) - eta) < 1e-10, "sum, route 2 (nsum)")
cb = lambda i: 1 / mp.cbrt(i)


def greedy(T, count):
    pos, neg, total, out = 1, 2, mp.mpf(0), []
    for _ in range(count):
        if total <= T:
            term = cb(pos)
            pos += 2
        else:
            term = -cb(neg)
            neg += 2
        total += term
        out.append((term, total))
    return out


gr = greedy(mp.mpf("0.2"), 4)
ok(gr[0][0] == 1, "first term 1")
key(3, "p-cube-root-greedy", 2, gr[1][1])
ok(mp.nstr(cb(2), 4) == "0.7937" and mp.nstr(gr[1][1], 4) == "0.2063", "second term and total")
wrong(3, "p-cube-root-greedy", 2, "positive", 1 + cb(3))
wrong(3, "p-cube-root-greedy", 2, "square-root", 1 - 1 / mp.sqrt(2))
key(3, "p-cube-root-greedy", 3, gr[2][0])
ok(mp.nstr(cb(4), 4) == "0.63" and mp.nstr(gr[2][1], 4) == "-0.4237", "third term -0.6300, total -0.4237")
wrong(3, "p-cube-root-greedy", 3, "sign", cb(4))
wrong(3, "p-cube-root-greedy", 3, "positive", cb(3))
wrong(3, "p-cube-root-greedy", 3, "odd-neg", -cb(3))
key(3, "p-cube-root-greedy", 4, gr[3][1])
ok(mp.nstr(cb(3), 4) == "0.6934" and mp.nstr(gr[3][1], 4) == "0.2697", "fourth term and total")
# the rounded route the part invites: -0.4237 + 0.6934
w4 = part(3, "p-cube-root-greedy", 4)["widget"]
ok(abs((-0.4237 + 0.6934) - w4["answer"]) <= w4["tol"]["abs"], "rounded route accepted")
wrong(3, "p-cube-root-greedy", 4, "negative-again", gr[2][1] - cb(6))
wrong(3, "p-cube-root-greedy", 4, "skipped", gr[2][1] + cb(5))
key(3, "p-cube-root-greedy", 5, Fr(1, 5))
long = greedy(mp.mpf("0.2"), 200000)
ok(abs(long[-1][1] - mp.mpf("0.2")) < 0.03, f"greedy total after 200,000 terms {mp.nstr(long[-1][1], 5)}")
wrong(3, "p-cube-root-greedy", 5, "original", mp.mpf("0.5718"))
wrong(3, "p-cube-root-greedy", 5, "last-total", mp.mpf("0.2697"))
ok(all(cb(i) >= mp.mpf(1) / i for i in range(1, 500)), "each size is at least 1/n")

# ---------------------------------------------------------------- shape of each set (brief chained.md)
for sn, d in SETS.items():
    items = d["items"]
    ok(3 <= len(items) <= 5, f"set {sn} item count")
    ok(any(it["difficulty"] == 5 for it in items) and all(3 <= it["difficulty"] <= 5 for it in items), f"set {sn} difficulty")
    typed = total = 0
    for it in items:
        ok(3 <= len(it["parts"]) <= 5, f"{it['id']} part count")
        for pi, p_ in enumerate(it["parts"], 1):
            total += 1
            kind = p_["widget"]["kind"]
            typed += kind in ("numeric", "expression")
            ex = p_["explain"]["text"]
            ok("!" not in json.dumps(p_) and "—" not in json.dumps(p_, ensure_ascii=False), f"{it['id']} part {pi} voice marks")
            if kind == "choice":
                ok(sum(1 for o in p_["widget"]["options"] if o.get("correct")) == 1, f"{it['id']} part {pi} one correct option")
                ok(all("why" in o for o in p_["widget"]["options"] if not o.get("correct")), f"{it['id']} part {pi} every wrong option has a why")
    ok(3 * typed >= 2 * total, f"set {sn} typed share {typed}/{total}")

print(f"{checks - fails} of {checks} checks passed")
sys.exit(1 if fails else 0)
