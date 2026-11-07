"""Second-read number and claim checks for proof level 3 (l10 to l15, review-3, homework-3).
Run from the repo root: python3 docs/reports/proof-L3-numbers.py  (exits 0 when every check passes).
Every key and wrong value is recomputed. Every claim a proof proves is brute-forced over a range, every
bracket identity is checked by evaluation at many points, and every code item is run in CPython.
The performance task has its own script, docs/reports/proof-3-perf-numbers.py.
lv.stated checks fail while a false sentence is in the text and pass once it is reworded.
"""
import math, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('proof', 3)
F = lambda pre: lv.files[[k for k in lv.files if k.startswith(pre)][0]]
Z = range(-3000, 3001)
K = range(-300, 301)
even = lambda n: n % 2 == 0
odd = lambda n: n % 2 == 1
imp = lambda p, q: (not p) or q


def isprime(m):
    return m > 1 and all(m % d for d in range(2, int(m ** 0.5) + 1))


def run_code(fid, path, w):
    pre = w.get('prelude', '')
    for label, src in (('solution', w['solution']), ('starter', w['starter'])):
        res = []
        for t in w.get('examples', []) + w['tests']:
            g = {}
            exec(pre, g)
            exec(src, g)
            exec(t.get('setup', ''), g)
            try:
                res.append(eval(t['call'], g) == eval(t['expect']))
            except Exception:
                res.append(False)
        lv.claim(all(res) if label == 'solution' else not all(res), f'{fid} {path} {label}: {sum(res)} of {len(res)} cases pass')


# ---------- l10 ----------
lv.claim([c['answer'] for r in F('l10')['screens'][0]['widget']['rows'] for c in r[1:]] == [2 + 4, 8 + 10, -6 + 12, 0 + 14], 'l10 sums 6, 18, 6, 14')
lv.claim(all(even(a + b) for a in range(-200, 201, 2) for b in range(-200, 201, 2)), 'even + even is even (brute force)')
lv.claim(all((2 * j + 1) + (2 * k + 1) == 2 * (j + k + 1) for j in K for k in K), 'odd + odd = 2(j + k + 1)')
lv.claim(all((2 * j + 1) * (2 * k + 1) == 2 * (2 * j * k + j + k) + 1 for j in K for k in K), 'odd x odd = 2(2jk + j + k) + 1')
lv.claim(all(even(n * n + n) for n in Z) and all((2 * k + 1) ** 2 + (2 * k + 1) == 2 * (2 * k + 1) * (k + 1) for k in K), 'n^2 + n even for every n; odd-case algebra')
lv.claim(all(4 * k * k + 2 * k == 2 * (2 * k * k + k) for k in K), 'even case 4k^2 + 2k = 2(2k^2 + k)')
lv.claim(all((a + b) / 2 >= math.sqrt(a * b) - 1e-12 for a in [i / 4 for i in range(0, 200)] for b in [i / 3 for i in range(0, 150)]), 'AM-GM on a grid of a, b >= 0')
lv.claim(all(abs((math.sqrt(a) - math.sqrt(b)) ** 2 - (a - 2 * math.sqrt(a * b) + b)) < 1e-9 for a in range(0, 50) for b in range(0, 50)), 'expansion of (sqrt a - sqrt b)^2')
lv.claim(all((abs((a + b) / 2 - math.sqrt(a * b)) < 1e-12) == (a == b) for a in range(0, 40) for b in range(0, 40)), 'AM-GM equality only when a = b (integer grid)')
lv.expect('l10', 'screens[10].widget.answer', round(math.sqrt(1.5 * 0.5), 3))
lv.claim(f'{math.sqrt(0.75):.4f}' == '0.8660' and 100 * 1.5 * 0.5 == 75 and 1.5 * 0.5 == 0.75, 'l10 transfer: sqrt 0.75 = 0.8660, £75, wrong 0.75')
lv.expect('l10', 'quiz[3].widget.answer', round(100 * 1.2 * 0.8, 6))
lv.claim(f'{math.sqrt(0.96):.4f}' == '0.9798' and 100 * 1.2 == 120, 'l10 quiz: sqrt 0.96 = 0.9798; wrong 120')
lv.claim(all(c % a == 0 for a in range(1, 13) for b in range(a, 80, a) for c in range(b, 300, b)), 'divisibility is transitive (brute force)')

# ---------- l11 ----------
lv.claim(all(imp(even(n * n), even(n)) for n in Z), 'if n^2 even then n even')
lv.claim(all(imp(odd(n), odd(n * n)) for n in Z) and all((2 * k + 1) ** 2 == 2 * (2 * k * k + 2 * k) + 1 for k in K), 'contrapositive: n odd gives n^2 = 2(2k^2 + 2k) + 1')
lv.claim(all(imp(even(3 * n + 1), odd(n)) for n in Z) and all(3 * (2 * k) + 1 == 2 * (3 * k) + 1 for k in K), 'if 3n + 1 even then n odd; 6k + 1 = 2(3k) + 1')
lv.claim([3 * n + 1 for n in range(0, 6)] == [1, 4, 7, 10, 13, 16], 'l11 table of 3n + 1')
lv.claim(all(imp(even(n * n - 6 * n + 5), odd(n)) for n in Z) and all(4 * k * k - 12 * k + 5 == 2 * (2 * k * k - 6 * k + 2) + 1 for k in K), 'if n^2 - 6n + 5 even then n odd; bracket 2k^2 - 6k + 2')
lv.claim(all(imp(odd(n * n), odd(n)) for n in Z) and all(imp(odd(n), odd(n * n)) for n in Z), 'l11 trap: claim and its converse both true')
lv.claim(all(imp(a + b >= 100, a >= 50 or b >= 50) for a in range(-150, 151) for b in range(-150, 151)), 'if a + b >= 100 then a >= 50 or b >= 50')
lv.claim(all(imp(L1 + L2 > 100, L1 > 50 or L2 > 50) for L1 in range(-200, 201) for L2 in range(-200, 201)), 'two-position risk rule (brute force over losses)')
lv.claim(all(imp(even(7 * n + 4), even(n)) for n in Z) and all(7 * (2 * k + 1) + 4 == 14 * k + 11 == 2 * (7 * k + 5) + 1 for k in K), 'if 7n + 4 even then n even; 14k + 11 = 2(7k + 5) + 1')
lv.claim(all(imp(even(n ** 3), even(n)) for n in Z) and all((2 * k + 1) ** 3 == 2 * (4 * k ** 3 + 6 * k * k + 3 * k) + 1 for k in K), 'if n^3 even then n even; cube bracket')
lv.claim(all(n + 2 == 2 * (n // 2 + 1) for n in range(-400, 401, 2)) and all((2 * m + 1) - 2 == 2 * (m - 1) + 1 for m in K), 'l11 n + 2 even; contrapositive rearrangement')

# ---------- l12 ----------
lv.expect('l12', 'screens[0].widget.answer', 99 ** 2 - 2 * 70 ** 2)
lv.claim(Fr(140, 99) ** 2 < 2 < Fr(99, 70) ** 2 and 1.414 < 140 / 99 < math.sqrt(2) < 99 / 70 < 1.4145 and f'{99 / 70:.5f}' == '1.41429', 'l12 140/99 < sqrt 2 < 99/70, all inside the zoomed line')
lv.claim(not any(p * p == 2 * q * q for q in range(1, 3000) for p in (int(q * math.sqrt(2)), int(q * math.sqrt(2)) + 1)), 'no p/q with q < 3000 squares to 2')
lv.claim(all(imp((2 * r) ** 2 == 2 * q * q, q * q == 2 * r * r) for r in range(1, 60) for q in range(1, 90)), 'p = 2r in p^2 = 2q^2 gives q^2 = 2r^2')
N6 = 2 * 3 * 5 * 7 * 11 * 13 + 1
lv.claim(N6 == 30031 and all(N6 % p == 1 for p in (2, 3, 5, 7, 11, 13)), 'l12 30031 leaves remainder 1 on the first six primes')
lv.expect('l12', 'screens[7].widget.answer', N6 // 59)
lv.claim(59 * 509 == N6 and isprime(59) and isprime(509) and 59 * 500 == 29500 and N6 - 29500 == 531 == 59 * 9, 'l12 30031 = 59 x 509, both prime; hints 29500 and 531')
lv.expect('l12', 'quiz[0].widget.answer', 2 * 3 * 5 * 7 + 1)
lv.claim(isprime(211) and 2 + 3 + 5 + 7 + 1 == 18, 'l12 211 is prime; wrong 18')
lv.claim(all(k > 1 and any(isprime(d) and k % d == 0 for d in range(2, k + 1)) for k in range(2, 3000)), 'every integer above 1 has a prime factor (2..2999)')
lv.claim(all(min(d for d in range(2, k + 1) if k % d == 0) == min(d for d in range(2, k + 1) if k % d == 0 and isprime(d)) for k in range(2, 2000)), 'the smallest divisor above 1 is prime (2..1999)')
lv.expect('l12', 'screens[11].widget.answer', 96 - 95)
lv.claim(100 - 96 == 4 and 100 - 95 == 5 and 95 + 96 == 191, 'l12 arbitrage wrongs 4, 5, 191')
lv.claim(all(imp((2 * r) ** 2 == 4 * q * q, r * r == q * q) for r in range(1, 50) for q in range(1, 50)) and 2 ** 2 == 4 * 1 ** 2, 'sqrt 4 copy: r^2 = q^2, and p = 2, q = 1 works')
lv.claim(all((p * p == 9 * q * q) <= (p % 3 == 0) for p in range(1, 200) for q in range(1, 70)) and 3 ** 2 == 9 * 1 ** 2, 'sqrt 9 copy: 3 divides p; p = 3, q = 1 works')
lv.claim(all(isprime(n) for n in [59, 509]) and N6 > 13, 'Euclid N exceeds every listed prime')
# l12 screens[10]: the conclusion drops "with no arbitrage" and generalises from 95 and 96 (review finding).
lv.stated('l12', 'screens[10].widget.lines[4].text', 'So two bonds with the same payments cannot have different prices', False)

# ---------- l13 ----------
lv.claim([c['answer'] for r in F('l13')['screens'][0]['widget']['rows'] for c in r[2:]] == [n * n for n in range(1, 6)], 'l13 sums of odd numbers 1, 4, 9, 16, 25')
lv.claim(all(sum(range(1, 2 * n, 2)) == n * n for n in range(0, 1500)), 'sum of first n odd numbers is n^2 (n < 1500)')
lv.claim(all(k * k + 2 * k + 1 == (k + 1) ** 2 for k in K) and all((k + 2) ** 2 == k * k + 4 * k + 4 for k in K), 'l13 (k + 1)^2 and wrong (k + 2)^2 expansion')
lv.claim(all(Fr(k * (k + 1), 2) + (k + 1) == Fr((k + 1) * (k + 2), 2) for k in K), 'Gauss step bracket k + 2')
lv.claim(all(Fr((k + 1) * (k + 2), 2) - Fr((k + 1) ** 2, 2) == Fr(k + 1, 2) for k in K), 'l13 why: (k + 1)^2/2 is short by (k + 1)/2')
lv.claim(all(sum(range(1, n + 1)) == n * (n + 1) // 2 for n in range(0, 2000)) and 100 * 101 // 2 == 5050, 'Gauss formula (n < 2000); 5050')
lv.expect('l13', 'quiz[2].widget.answer', sum(range(1, 101)))
lv.claim(all(sum(2 ** i for i in range(n)) == 2 ** n - 1 for n in range(0, 200)) and all(2 ** k - 1 + 2 ** k == 2 ** (k + 1) - 1 for k in range(0, 200)), 'geometric sum 2^n - 1 and its step')
lv.claim([sum(2 ** i for i in range(n)) for n in range(1, 6)] == [1, 3, 7, 15, 31], 'l13 doubling table')
lv.claim(all(k * k + 3 * k + 3 == (k + 1) ** 2 + (k + 1) + 1 == (k * k + k + 1) + 2 * (k + 1) for k in K) and all(odd(n * n + n + 1) for n in Z), 'l13 trap algebra; n^2 + n + 1 is never even')
ok = [n for n in range(1, 400) if 2 ** n > n * n]
lv.claim(ok[:3] == [1, 5, 6] and all(n in ok for n in range(5, 400)) and all(n not in ok for n in (2, 3, 4)), '2^n > n^2: true at 1, false at 2, 3, 4, true from 5 (to 399)')
lv.expect('l13', 'screens[7].widget.answer', min(n0 for n0 in range(1, 50) if all(2 ** n > n * n for n in range(n0, 400))))
lv.claim(all(k * k >= 2 * k + 1 for k in range(3, 2000)) and not 2 * 2 >= 2 * 2 + 1, 'k^2 >= 2k + 1 holds for k >= 3, fails at k = 2')
lv.claim(all(2 ** (k + 1) > (k + 1) ** 2 for k in range(5, 300) if 2 ** k > k * k), 'the 2^n > n^2 step holds from 5 on')
lv.claim(all((4 ** n - 1) % 3 == 0 for n in range(1, 300)) and all(4 * (4 ** k - 1) + 3 == 4 ** (k + 1) - 1 for k in range(0, 100)), '3 divides 4^n - 1; step box 3')
lv.claim(4 ** 1 - 4 + 1 == 1 and 4 - 4 + 4 == 4, 'l13 quiz wrongs 1 and 4 lines')
V = [1000.0]
for n in range(10):
    V.append(V[-1] * 1.05)
lv.claim(all(abs(V[n] - 1000 * 1.05 ** n) < 1e-9 for n in range(11)) and f'{V[2]:.2f}' == '1102.50', 'l13 V_n = 1000 x 1.05^n; V_2 = 1102.50')
lv.expect('l13', 'screens[10].widget.answer', round(1000 * 1.05 ** 10, 2))
lv.claim(f'{1.05 ** 10:.6f}' == '1.628895' and f'{1000 * 1.05 ** 9:.2f}' == '1551.33' and f'{1000 * 1.05 ** 10 - 1500:.2f}' == '128.89', 'l13 1.628895; wrong 1551.33; gap £128.89')
lv.claim(all((1 + r) ** n >= 1 + n * r - 1e-12 for r in [i / 20 for i in range(-20, 41)] for n in range(0, 40)), "Bernoulli's inequality for r >= -1 (grid)")
w = F('l13')['screens'][8]['widget']
run_code('l13', 'screens[8]', w)
lv.claim(sum(range(1, 2 * 5 - 1, 2)) == 16, 'l13 hint: range(1, 2n - 1, 2) gives 16 for n = 5')

# ---------- l14 ----------
f41 = lambda n: n * n + n + 41
lv.claim([c['answer'] for r in F('l14')['screens'][0]['widget']['rows'] for c in r[1:]] == [f41(n) for n in range(6)] and all(isprime(f41(n)) for n in range(6)), 'l14 values 41 to 71, all prime')
lv.claim(all(isprime(f41(n)) for n in range(40)) and not isprime(f41(40)), 'n^2 + n + 41 prime for n = 0 to 39, not at 40')
lv.expect('l14', 'screens[1].widget.answer', f41(40))
lv.claim(f41(40) == 41 ** 2 and 1600 + 41 == 1641 and 1600 + 80 + 41 == 1721, 'l14 1681 = 41^2; wrongs 1641, 1721')
lv.claim(min(n for n in range(3, 100, 2) if not isprime(n)) == 9, 'smallest odd counterexample is 9')
lv.claim(all(((a + b) ** 2 == a * a + b * b) == (a * b == 0) for a in range(-30, 31) for b in range(-30, 31)), '(a + b)^2 = a^2 + b^2 exactly when ab = 0')
lv.claim([isprime(2 ** p - 1) for p in (2, 3, 5, 7, 11)] == [True] * 4 + [False], '2^p - 1 prime for p = 2, 3, 5, 7, not 11')
lv.expect('l14', 'screens[6].widget.answer', 2047 // 23)
lv.claim(23 * 89 == 2047 and 23 * 90 == 2070 and 2070 - 23 == 2047, 'l14 2047 = 23 x 89; hints')
lv.claim([n for n in range(1, 11) if isprime(n) and not odd(n)] == [2], 'only prime in 1..10 that is not odd is 2')
run_code('l14', 'screens[8]', F('l14')['screens'][8]['widget'])
fm = lambda n: n * n - n + 41
lv.claim(all(isprime(fm(n)) for n in range(41)) and not isprime(fm(41)), 'n^2 - n + 41 prime for 0..40, fails at 41')
lv.expect('l14', 'screens[10].widget.answer', 0.5 * 0.08 + 0.5 * 0.05)
lv.claim(0.08 + 0.05 == 0.13 and 0.5 * 0.08 + 0.5 * 0.10 > 0.08, 'l14 wrong 13%; a 10% stock would raise the average')
lv.expect('l14', 'quiz[3].widget.answer', f41(41) // 41)
lv.claim(f41(41) == 1763 == 41 * 43 and not isprime(1763), 'l14 1763 = 41 x 43')
lv.claim(not isprime(9) and odd(9) and odd(81) and 9 % 3 == 0 and 6 % 3 == 0 and even(6), 'l14 quiz on 9: refutes two claims; 6 refutes the third')

# ---------- l15 ----------
lv.claim(all((2 * k + 1) + (2 * k + 1) == 4 * k + 2 == 2 * (2 * k + 1) for k in K), 'l15 write-up B line 3 is sound algebra')
lv.claim(all((a == b) == (a + 3 == b + 3) for a in range(-50, 51) for b in range(-50, 51)) and (-2) ** 2 == 2 ** 2 and abs(-3) == abs(3), 'l15 adding 3 reverses; squaring and |.| do not')
lv.claim(all(2 ** n >= n + 1 for n in range(1, 500)) and all(2 * (k + 1) >= k + 2 for k in range(0, 500)), 'l15 quiz 2^n >= n + 1 and its step')
lv.claim(all(L <= 10000 for L in [sum(c) for c in [(2000,) * 5, (2000, 1999, 0, -50, 2000)]]) and 5 * 2000 == 10000, 'l15 risk note: five losses at most £2,000 sum to at most £10,000')
lv.claim(1 ** 2 == 1 and 0 ** 2 == 0 and 2 ** 2 != 2, 'l15 witnesses n = 1 and n = 0 for n^2 = n')
lv.claim(all(even(x * (x + 1)) for x in Z) and any(x * x == 4 for x in range(-5, 6)), 'l15 claims A and B are true')

# ---------- review-3 ----------
lv.claim(all((2 * j + 1) * (2 * k + 3) == 4 * j * k + 6 * j + 2 * k + 3 == 2 * (2 * j * k + 3 * j + k + 1) + 1 for j in K for k in range(-60, 61)), 'review-3 bracket 2jk + 3j + k + 1')
lv.claim(all(imp(even(n * n + 1), odd(n)) for n in Z) and all((2 * k) ** 2 + 1 == 2 * (2 * k * k) + 1 for k in K), 'review-3 contrapositive claim true')
fact = lambda n: math.prod(range(1, n + 1))
lv.expect('review', 'items[4].widget.answer', min(n for n in range(1, 50) if fact(n) > 2 ** n))
lv.claim(all(fact(n) > 2 ** n for n in range(4, 300)) and [fact(n) for n in (1, 2, 3, 4)] == [1, 2, 6, 24], 'n! > 2^n from 4 on (to 299)')
lv.claim(all(Fr(3 ** k - 1, 2) + 3 ** k == Fr(3 ** (k + 1) - 1, 2) for k in range(0, 100)) and all(sum(3 ** i for i in range(n)) == (3 ** n - 1) // 2 for n in range(0, 100)), 'review-3 base-3 geometric sum and step')
lv.claim([n for n in range(-10, 11) if n * n > 4 and not n > 2] == [-10, -9, -8, -7, -6, -5, -4, -3], 'review-3 counterexamples are n <= -3')
lv.claim(math.sqrt(3 + 6) == 3 and math.sqrt(-2 + 6) == 2 != -2 and all(x + 6 == x * x for x in (3, -2)), 'review-3 x = 3 works, x = -2 is added by squaring')
lv.claim(all((3 * m + 1) ** 2 == 3 * (3 * m * m + 2 * m) + 1 and (3 * m + 2) ** 2 == 3 * (3 * m * m + 4 * m + 1) + 1 for m in K) and all(imp(n * n % 3 == 0, n % 3 == 0) for n in Z), 'if 3 divides n^2 then 3 divides n; expansions')

# ---------- homework-3 ----------
sq = lambda n: n * (n + 1) * (2 * n + 1) // 6
lv.claim(all(sum(i * i for i in range(1, n + 1)) == sq(n) for n in range(0, 1500)), 'sum of squares formula (n < 1500)')
lv.claim(all(k * (2 * k + 1) + 6 * (k + 1) == 2 * k * k + 7 * k + 6 == (k + 2) * (2 * k + 3) for k in K), 'homework-3 bracket (k + 2)(2k + 3)')
lv.claim(all(k * (2 * k + 1) + (k + 1) == 2 * k * k + 2 * k + 1 for k in K), 'homework-3 wrong nosix: 2k^2 + 2k + 1')
lv.expect('homework', 'items[2].widget.answer', sq(10))
lv.claim(10 * 11 * 21 == 2310 and sum(range(1, 11)) == 55 and sq(1) == 1, 'homework-3 2310 and 55; base case 1')
lv.claim(all(imp(p * p % 3 == 0, p % 3 == 0) for p in Z) and 36 % 4 == 0 and 6 % 4 != 0, 'homework-3 lemma; 4 divides 36 but not 6')
lv.claim(not any(p * p == 3 * q * q for q in range(1, 3000) for p in (int(q * math.sqrt(3)), int(q * math.sqrt(3)) + 1)), 'no p/q with q < 3000 squares to 3')
run_code('homework-3', 'items[6]', F('homework')['items'][6]['widget'])
lv.claim(all(imp(even(5 * n + 3), odd(n)) for n in Z) and all(5 * (2 * k) + 3 == 2 * (5 * k + 1) + 1 for k in K), 'homework-3 exit (b) claim and algebra')
lv.claim(all(0 < Fr(p, 2 * q) < Fr(p, q) for p in range(1, 30) for q in range(1, 30)), 'homework-3 exit (c): 0 < r/2 < r')
f11 = lambda n: n * n - n + 11
lv.claim([f11(n) for n in range(11)] == [11, 11, 13, 17, 23, 31, 41, 53, 67, 83, 101] and all(isprime(f11(n)) for n in range(11)) and f11(11) == 121 == 11 * 11, 'homework-3 exit (e) values and 121')

# Induction steps assume P(k) "for some k" (review finding): pass once reworded to an arbitrary k.
lv.stated('l13', 'screens[2].widget.lines[1].text', 'for some $k \\ge 1$', False)


# ---------- fix pass: the new wording must be present (a revert fails these) ----------
def has(ref, path, phrase, present=True):
    t = lv.text(ref, path)
    lv.claim((phrase in t) == present, f'{ref} {path} {"has" if present else "lacks"} {phrase!r}')

has('l12', 'screens[10].widget.lines[0].text', 'trade at prices $a < b$')
has('l12', 'screens[10].widget.lines[1].text', 'we receive $b - a > 0$ now')
has('l12', 'screens[10].widget.lines[4].text', 'So with no arbitrage, two bonds with the same payments have the same price.')
lv.claim(all(b - a > 0 and (100 - 100) == 0 for a in range(1, 100) for b in range(a + 1, 101)), 'fix pass l12: for every a < b the cash now is b - a > 0 and the cash in a year is 0')
has('l12', 'screens[6].widget.lines[3].text', 'its smallest divisor above 1 is a prime factor, and by the line above it is not in the list')
has('l13', 'screens[2].prose', 'for every $k \\ge 1$, if it holds for $k$ then it holds for $k + 1$')
for ref, path in [('l13', 'screens[2].widget.lines[1].text'), ('l13', 'screens[9].widget.lines[1].text'), ('homework', 'items[0].widget.lines[1].text'), ('homework', 'items[3].widget.lines[1].text')]:
    has(ref, path, 'be arbitrary, and assume')
    has(ref, path, 'for some $k', present=False)
has('l13', 'quiz[3].widget.options[3].why', 'one arbitrary $k$, not for every $n$ at once')
has('homework', 'items[8].model', 'Step: let $k \\ge 1$ be an arbitrary whole number, and assume $k^3 - k = 3a$ for an integer $a$.')
has('homework', 'items[8].model', 'for some whole number $k$', present=False)
has('homework', 'items[8].rubric', 'the step from an arbitrary $k$ to $k + 1$')
has('homework', 'items[9].model', 'Step: let $k \\ge 1$ be arbitrary, and assume $1 + 2 + \\dots + 2^{k-1} = 2^k - 1$.')
has('homework', 'items[9].model', 'for some $k \\ge 1$', present=False)
has('l14', 'quiz[2].explain.text', '“every odd number greater than 1 is prime”')
has('l14', 'screens[7].explain.text', 'inside “P: prime” and outside “Q: odd”')
has('review', 'items[1].explain.text', 'so it proves only that an odd number squared is odd')
has('review', 'items[5].feedback.byKey.exp', 'You added the exponents, as if multiplying $3^k$ by $3^k$.')
lv.claim(all(3 ** k + 2 * 3 ** k == 3 * 3 ** k == 3 ** (k + 1) and 3 ** k * 3 ** k == 3 ** (2 * k) for k in range(1, 60)), 'fix pass review-3: 3^k + 2 x 3^k = 3^(k+1); 3^k x 3^k = 3^(2k)')
lv.claim(all((3 * m + 1) ** 2 == 3 * (3 * m * m + 2 * m) + 1 and (3 * m + 2) ** 2 == 3 * (3 * m * m + 4 * m + 1) + 1 for m in range(0, 500)), 'fix pass homework-3 item 5: remainder-1 squares')
has('homework', 'items[5].widget.options[0].text', 'Contrapositive, by the remainders 1 and 2 on division by 3')

lv.check_wrongs()
lv.report()
