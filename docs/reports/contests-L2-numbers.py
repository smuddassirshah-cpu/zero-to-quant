"""Second-reader number check for contests level 2 (Contest maths): l5 to l8, review-2, homework-2.

Every value is recomputed here by a method independent of the content's own solution, then looked up in the text.
Checks that fail mark a finding in docs/reviews/review-contests-1-2.md and test the corrected value only.
Run: python3 docs/reports/contests-L2-numbers.py   (about a minute: it sieves to 2e6 and builds 1e6 factorials)
"""
import itertools, json, math, os, random, sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

sys.set_int_max_str_digits(0)
lv = Level('contests', 2)
E = lv.expect
P = 10**9 + 7
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'contests')
doc = {f: json.load(open(os.path.join(SRC, f + '.json'))) for f in ('l6-gcd-and-primes', 'l8-invariants')}


def is_prime(n):                       # deterministic Miller-Rabin for n < 3.3e24
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def euclid_steps(a, b):
    n = 0
    while b:
        a, b, n = b, a % b, n + 1
    return n


def mults_by_squaring(e):              # squarings plus multiplications of the l5 loop
    return e.bit_length() + bin(e).count('1')


# ---------- l5 ----------
E('l5', 'screens[0].prose', '3 \\cdot 10^{17}')
assert round(10**18 * math.log10(2) / 1e17) == 3
digits = [pow(7, k, 10) for k in (2, 3, 4, 5, 2031)]
for k, v in zip((1, 2, 3, 4, 5), digits):
    E('l5', f'screens[0].widget.rows[{k}][1].answer', v)
E('l5', 'screens[0].hints[2].text', 2031 // 4)
E('l5', 'screens[1].feedback.correct', (5 + 4) % 7)
E('l5', 'screens[2].widget.answer', 38 * 45 % 7)
E('l5', 'screens[2].widget.accept', 38 * 45 // 7)
E('l5', 'screens[2].widget.wrong[0].value', (38 % 7) * (45 % 7))
E('l5', 'screens[2].widget.wrong[2].value', 38 % 7 + 45 % 7)
for a in range(2, 7):
    E('l5', f'screens[3].widget.rows[{a - 1}][1].answer', pow(a, -1, 7))
E('l5', 'screens[3].explain.text', 5 * pow(4, -1, 7) % 7)
E('l5', 'screens[4].widget.answer', pow(3, 5, 7))
E('l5', 'screens[4].widget.wrong[0].value', 3**5)
E('l5', 'screens[4].feedback.byKey.full', 3**5 // 7)
E('l5', 'screens[5].widget.options[0].text', pow(3, 8, 7))
E('l5', 'screens[5].feedback.correct', pow(3, 13, 7))
E('l5', 'screens[5].explain.text', 2 * (10**18).bit_length())   # bound: one squaring and at most one product per bit
E('l5', 'screens[6].widget.tests[6].expect', pow(3, 100000, P))
lv._rec(mults_by_squaring(100000) <= 40, f'l5 power_mod e=1e5 needs {mults_by_squaring(100000)} <= 40 multiplications', '')
E('l5', 'screens[6].widget.tests[8].expect', pow(2, 10**18, P))
E('l5', 'screens[6].widget.tests[9].expect', pow(10**18, 10**18 + 3, P))
E('l5', 'screens[6].explain.text', (10**18).bit_length())
E('l5', 'screens[7].widget.tests[5].expect', (P + 1) // 2)
E('l5', 'screens[8].canvas.params.lines[0]', round((P - 1)**2 / 1e18, 1), fmt='{:.1f}·10¹⁸')
E('l5', 'screens[8].widget.tests[4].expect', 123456789 * 987654321 % P)
E('l5', 'screens[8].widget.tests[5].expect', 10**18 * 3 % P)
E('l5', 'screens[8].widget.tests[7].expect', (-10**18) * (-10**18) % P)
E('l5', 'screens[8].canvas.params.lines[5]', -3 % 7)
E('l5', 'screens[9].prose', 30 % 7)
E('l5', 'screens[9].widget.options[2].why', pow(5, -1, 7))
E('l5', 'screens[9].feedback.correct', (30 % 7) * pow(5, -1, 7) % 7)
E('l5', 'screens[10].widget.options[1].why', (3 - 5) % 7)
E('l5', 'screens[10].widget.options[2].why', abs(3 - 5))
h = 0
trail = []
for x in (5, 10**9, 3):
    h = (31 * h + x) % P
    trail.append(h)
E('l5', 'screens[11].widget.answer', trail[-1])
E('l5', 'screens[11].hints[2].text', trail[1])
E('l5', 'screens[11].hints[1].text', 31 * 5 + 10**9)
E('l5', 'screens[11].widget.wrong[0].value', 31 * (31 * 5 + 10**9) + 3)
E('l5', 'screens[11].widget.wrong[1].value', 31 * trail[1])
E('l5', 'quiz[1].widget.answer', pow(4, -1, 11))
E('l5', 'quiz[1].feedback.byKey.self', 16 % 11)
assert pow(4, 9, 11) == pow(4, -1, 11)
E('l5', 'quiz[2].widget.options[2].why', (10**18).bit_length())
E('l5', 'quiz[3].widget.options[0].text', '2 \\cdot 10^9 + 14')
assert (2 * 10**9 + 14) % P == 0
E('l5', 'quiz[3].widget.options[3].why', pow(2, -1, P))
assert P < 2**30 and is_prime(P) and is_prime(2**31 - 1)

# ---------- l6 ----------
E('l6', 'screens[0].widget.points[0].target', math.lcm(84, 36))
E('l6', 'screens[0].feedback.byKey.gcd', math.gcd(84, 36))
E('l6', 'screens[0].explain.text', 84 * 36)
E('l6', 'screens[0].explain.text', 84 * 36 // math.lcm(84, 36), fmt='12th')
E('l6', 'screens[2].widget.rows[1][2].answer', 462 % 147)
E('l6', 'screens[2].widget.rows[2][2].answer', 147 % 21)
E('l6', 'screens[2].explain.text', 1071 // 21)
E('l6', 'screens[2].explain.text', 462 // 21)
E('l6', 'screens[4].widget.answer', euclid_steps(89, 55))
F = [0, 1]
while len(F) < 90:
    F.append(F[-1] + F[-2])
E('l6', 'screens[4].explain.text', euclid_steps(F[88], F[87]))
E('l6', 'screens[5].widget.tests[11].call', F[88])
E('l6', 'screens[5].widget.tests[11].call', F[87])
E('l6', 'screens[5].widget.tests[5].expect', math.gcd(10**18, 6 * 10**17))
# sieve grid: the tappable set is every number <= 100 not crossed by 2, 3 or 5; the answer is what 7 still crosses
cell = lambda v: f'r{(v - 1) // 10 + 1}c{(v - 1) % 10 + 1}'
w6 = doc['l6-gcd-and-primes']['screens'][6]['widget']
standing = {v for v in range(2, 101) if v in (2, 3, 5) or all(v % q for q in (2, 3, 5))}
lv._rec(set(w6['only']) == {cell(v) for v in standing}, 'l6 screens[6] tappable set = numbers left by 2, 3, 5', '')
lv._rec(set(w6['answer']) == {cell(v) for v in standing if v % 7 == 0 and v > 7}, 'l6 screens[6] answer = 49, 77, 91', '')
primes100 = [v for v in range(2, 101) if is_prime(v)]
E('l6', 'screens[6].explain.text', len(primes100))
# primes by a bytearray sieve (a different construction from the content's list-of-flags sieve)
N = 2 * 10**6
b = bytearray([1]) * (N + 1)
b[0] = b[1] = 0
for p in range(2, math.isqrt(N) + 1):
    if b[p]:
        b[p * p::p] = bytes(len(range(p * p, N + 1, p)))
E('l6', 'screens[7].widget.tests[7].expect', sum(b[:10**6 + 1]))
E('l6', 'screens[7].widget.tests[9].expect', sum(b))
E('l6', 'screens[7].widget.tests[8].expect', sum(i for i in range(1_500_000) if b[i]))
E('l6', 'screens[7].explain.text', sum(i for i in range(1_500_000) if b[i]))
E('l6', 'screens[7].widget.tests[5].expect', len(primes100))
assert is_prime(1_000_003) and is_prime(999_983) and is_prime(999_999_999_989)
E('l6', 'screens[8].prose', 1_000_003 - 2)
E('l6', 'screens[8].widget.answer', math.isqrt(1_000_003))
E('l6', 'screens[8].widget.wrong[0].value', 1_000_003 - 1)
E('l6', 'screens[8].widget.wrong[1].value', 1_000_003 // 2)
E('l6', 'screens[8].feedback.byKey.half', round((1_000_003 // 2) / 1000))
E('l6', 'screens[8].widget.accept', round(math.sqrt(1_000_003), 4))
E('l6', 'screens[8].hints[1].text', 1001**2)
E('l6', 'screens[10].explain.text', '10^{24}')
E('l6', 'screens[11].widget.answer', math.lcm(14, 21))
E('l6', 'screens[11].widget.wrong[0].value', 14 * 21)
E('l6', 'screens[11].widget.wrong[1].value', math.gcd(14, 21))
E('l6', 'quiz[0].widget.options[0].text', math.gcd(0, 15))
E('l6', 'quiz[1].widget.answer', math.lcm(6, 10))
E('l6', 'quiz[2].widget.answer', sum(1 for v in range(31) if is_prime(v)))
E('l6', 'quiz[3].widget.options[0].text', max(p for p in range(2, 201) if is_prime(p) and p * p <= 200))
E('l6', 'quiz[3].widget.options[1].why', round(math.sqrt(200), 1))
# finding: the Fibonacci explanation says every quotient was 1; the last one is 2 (2 = 2 x 1)
E('l6', 'screens[4].explain.text', 'Every quotient but the last was 1')
# finding: no sieve test sits at n = p^2, so p * p < n passes; the fix adds sieve(49)[-1] == 47
E('l6', 'screens[7].widget.tests', 'sieve(49)[-1]')
assert max(v for v in range(50) if is_prime(v)) == 47

# ---------- l7 ----------
grid = {}
for x in range(4):
    for y in range(4):
        grid[x, y] = 1 if x == 0 or y == 0 else grid[x - 1, y] + grid[x, y - 1]
E('l7', 'screens[0].widget.rows[0][1].answer', grid[2, 2])
E('l7', 'screens[0].widget.rows[1][1].answer', grid[2, 3])
E('l7', 'screens[0].widget.rows[2][1].answer', grid[3, 3])
E('l7', 'screens[1].explain.text', len(str(math.comb(2000, 1000))))
fact13 = [math.factorial(i) % 13 for i in range(7)]
for i in (4, 5, 6):
    E('l7', f'screens[2].widget.rows[{i}][1].answer', fact13[i])
E('l7', 'screens[2].explain.text', math.factorial(6) // 13)
inv13 = [pow(f, -1, 13) for f in fact13]
for i in range(6):
    E('l7', f'screens[3].widget.rows[{i}][2].answer', inv13[i])
E('l7', 'screens[3].prose', pow(5, 11, 13))
E('l7', 'screens[3].explain.text', 6 * 11 // 13)
E('l7', 'screens[4].widget.answer', math.comb(6, 3) % 13)
E('l7', 'screens[4].widget.wrong[2].value', fact13[6] * inv13[3] * inv13[3])
E('l7', 'screens[4].widget.wrong[1].value', fact13[6] * fact13[3] * fact13[3] % 13)
E('l7', 'screens[5].widget.answer', math.comb(7, 2))
E('l7', 'screens[5].widget.wrong[0].value', 3**5)
E('l7', 'screens[5].widget.wrong[1].value', math.comb(5, 2))
E('l7', 'screens[5].widget.wrong[2].value', math.comb(7, 3))
# factorials to 1e6 with one pow per inverse (a different construction from the content's backward loop)
M = 10**6
fa = [1] * (M + 1)
for i in range(1, M + 1):
    fa[i] = fa[i - 1] * i % P
E('l7', 'screens[6].widget.tests[4].expect', fa[M])
inv = lambda v: pow(v, P - 2, P)
C = lambda n, k: fa[n] * inv(fa[k]) % P * inv(fa[n - k]) % P if 0 <= k <= n else 0
E('l7', 'screens[7].widget.tests[6].expect', C(1000, 500))
E('l7', 'screens[8].widget.tests[4].expect', C(2000, 1000))
E('l7', 'screens[8].widget.tests[5].expect', C(10**6, 5 * 10**5))
r = random.Random(7)
qs = []
for _ in range(10**5):
    n = r.randint(0, 10**6)
    qs.append((n, r.randint(-1, n + 1)))
E('l7', 'screens[8].widget.tests[6].expect', sum(C(n, k) for n, k in qs) % P)
lg = (math.lgamma(10**6 + 1) - 2 * math.lgamma(5 * 10**5 + 1)) / math.log(10)
assert 0.05 < lg % 1 < 0.95                       # far from a digit boundary
E('l7', 'screens[9].hints[2].text', math.floor(lg) + 1)
E('l7', 'screens[10].explain.text', '2 \\cdot 10^6')
assert 2000**2 // 2 == 2 * 10**6
E('l7', 'screens[11].widget.answer', math.comb(10, 6))
E('l7', 'screens[11].widget.wrong[0].value', 2**10)
E('l7', 'screens[11].widget.wrong[1].value', math.perm(10, 4))
E('l7', 'screens[11].explain.text', len(str(math.comb(252, 126))))
E('l7', 'quiz[0].widget.wrong[0].value', math.comb(7, 5))
E('l7', 'quiz[2].widget.answer', math.comb(6, 2))
E('l7', 'quiz[2].widget.wrong[0].value', 3**4)
E('l7', 'quiz[2].widget.wrong[1].value', math.comb(4, 2))
E('l7', 'quiz[3].explain.text', '2 \\cdot 10^5')

# ---------- l8 ----------
def bfs(start):
    seen, q = {start}, deque([start])
    while q:
        s = q.popleft()
        for i in range(3):
            if s[i] >= 2:
                t = tuple(s[j] - 2 if j == i else s[j] + 1 for j in range(3))
                if t not in seen:
                    seen.add(t)
                    q.append(t)
    return seen
R = bfs((3, 2, 1))
E('l8', 'screens[1].prose', 'all nine positions')
lv._rec(len(R) == 9 and not any(6 in s for s in R), f'l8 token game: {len(R)} positions, none with all six', '')
lv._rec(all((a - b) % 3 == 1 for a, b, c in R), 'l8 (A - B) mod 3 = 1 on every reachable position', '')
# finding: the generic feedback's "take two from the fullest box" loops 3,2,1 -> 1,3,2 -> 2,1,3 -> 3,2,1
s, path = (3, 2, 1), []
for _ in range(6):
    i = max(range(3), key=lambda j: s[j])
    s = tuple(s[j] - 2 if j == i else s[j] + 1 for j in range(3))
    path.append(s)
lv._rec((1, 0, 5) not in path, 'l8 fullest-box strategy never reaches 1, 0, 5 (so the old feedback is wrong)', str(path))
E('l8', 'screens[0].feedback.generic', '4, 0, 2')
dark = doc['l8-invariants']['screens'][3]['canvas']['state']['shade']['dark']['ids']
E('l8', 'screens[3].widget.answer', len(dark))
lv._rec(len(dark) == 32 - 2 and 'r1c1' not in dark and 'r8c8' not in dark, 'l8 chessboard: 30 shaded left', '')


def finals(xs):
    if len(xs) == 1:
        return {xs[0]}
    out = set()
    for i, j in itertools.combinations(range(len(xs)), 2):
        rest = [xs[k] for k in range(len(xs)) if k not in (i, j)] + [abs(xs[i] - xs[j])]
        out |= finals(rest)
    return out
fin = finals([3, 5, 6, 9])
lv._rec(fin == {1, 5, 7}, f'l8 difference game from 3, 5, 6, 9 ends in {sorted(fin)}', '')
r = random.Random(3)
E('l8', 'screens[8].widget.tests[7].expect', sum(r.randint(0, 10**9) for _ in range(200000)) % 2)
E('l8', 'screens[7].explain.text', 90)
assert 80 <= euclid_steps(F[88], F[87]) <= 90
E('l8', 'screens[10].canvas.params.lines[2]', 10000 - 30 * 52)
E('l8', 'screens[10].hints[1].text', 8440 + 30 * 55)
E('l8', 'screens[10].hints[2].text', 8990 + 10 * 55)
E('l8', 'screens[10].explain.text', 8990 + 20 * 55)
E('l8', 'quiz[0].widget.options[0].text', sum(range(1, 11)))
E('l8', 'quiz[3].widget.options[0].text', math.gcd(10, 4))
# finding: final_parity tests use 10**18 while the prose bounds the numbers at 10^9
E('l8', 'screens[8].prose', 'from 0 to $10^{18}$')

# ---------- review-2 ----------
E('review', 'items[0].widget.options[0].text', int(math.fmod(3 - 5, 7)))
E('review', 'items[0].feedback.correct', (3 - 5) % 7)
E('review', 'items[1].widget.answer', math.gcd(252, 198))
E('review', 'items[1].widget.wrong[0].value', 252 % 198)
E('review', 'items[2].widget.answer', pow(3, -1, P))
E('review', 'items[2].widget.accept', 3 * pow(3, -1, P))
E('review', 'items[3].widget.answer', pow(3, 10**18, 7))
E('review', 'items[3].widget.wrong[0].value', pow(3, 10**18 % 7, 7))
E('review', 'items[4].widget.answer', sum(1 for v in range(51) if is_prime(v)))
E('review', 'items[5].widget.answer', math.lcm(4, 6, 10))
E('review', 'items[5].widget.wrong[0].value', 4 * 6 * 10)
E('review', 'items[6].widget.answer', math.comb(13, 3))
E('review', 'items[6].widget.wrong[0].value', 4**10)
E('review', 'items[6].widget.wrong[1].value', math.comb(10, 3))
E('review', 'items[6].widget.wrong[2].value', math.comb(13, 4))
E('review', 'items[8].explain.text', len(bfs((4, 1, 1))))
lv._rec(not any(6 in s for s in bfs((4, 1, 1))), 'review-2 tokens from 4, 1, 1 never all in one box', '')
x, y, moves = 12, 7, 0
while (x, y) != (1, 1):
    x, y = (x - y, y) if x > y else (x, y - x)
    moves += 1
E('review', 'items[9].widget.answer', moves)

# ---------- homework-2 ----------
G = lambda n: sum(math.gcd(i, n) for i in range(1, n + 1))


def G_div(n):                          # sum over d | n of d * phi(n / d), from a factorisation by Miller-Rabin checks
    fs, m, d = {}, n, 2
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    phi = lambda p, j: 1 if j == 0 else p**j - p**(j - 1)
    tot = 1
    for p, a in fs.items():
        tot *= sum(p**k * phi(p, a - k) for k in range(a + 1))
    return tot
for n in (6, 12, 97):
    E('homework', 'items[0].widget.tests', G(n))
E('homework', 'items[0].widget.tests[5].expect', G(720720))
for i, n in ((6, 2**40), (7, 10**12), (8, 999983 * 1000003), (9, 999999999989)):
    E('homework', f'items[0].widget.tests[{i}].expect', G_div(n))
E('homework', 'items[0].explain.text', G_div(10**12))
Z = lambda k: sum(k // 5**j for j in range(1, 40))


def small_k(m):                        # Legendre's digit-sum form Z(k) = (k - s5(k)) / 4, searched over multiples of 5
    lo, hi = 0, 5 * m + 5
    while lo < hi:
        mid = (lo + hi) // 2
        if Z(mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo
assert all(small_k(m) == next(k for k in itertools.count() if Z(k) >= m) for m in range(0, 120))
for i, m in ((1, 1), (2, 4), (3, 5), (4, 6), (5, 7), (6, 24), (7, 25), (9, 10**12 - 1), (10, 10**12)):
    E('homework', f'items[1].widget.tests[{i}].expect', small_k(m))
E('homework', 'items[1].widget.tests[8].expect', str([small_k(m) for m in range(100, 106)]))
E('homework', 'items[1].feedback.correct', math.ceil(math.log2(5 * 10**12)))
E('homework', 'items[1].feedback.correct', round(math.log(5 * 10**12, 5)))
E('homework', 'items[1].explain.text', Z(24))
E('homework', 'items[1].explain.text', Z(25))
E('homework', 'items[2].explain.text', ', '.join(str(3 * i % 7) for i in range(1, 7)))
E('homework', 'items[4].widget.answer', pow(3, 200, 13))
E('homework', 'items[4].explain.text', 200 % 12)
E('homework', 'items[5].widget.answer', math.comb(12 - 6 + 2, 2))
E('homework', 'items[5].widget.wrong[0].value', math.comb(14, 2))
E('homework', 'items[5].widget.wrong[1].value', math.comb(12 - 3 + 2, 2))
E('homework', 'items[6].feedback.correct', 5 - 3)
rub = json.load(open(os.path.join(SRC, 'homework-2.json')))['items'][3]['widget']['rubric']
lv._rec(sum(x['points'] for x in rub) == 10, 'homework-2 items[3] rubric totals 10 points', '')
# finding: answering 0 moves gets "The gcd is 1, so it is reachable", the reasoning l8 calls a trap
E('homework', 'items[0].prose', 'G(p^a)')        # anchor so a missing file fails loudly
txt = json.load(open(os.path.join(SRC, 'review-2.json')))['items'][9]['feedback']['byKey']['gcd']
lv._rec('so it is reachable' not in txt, 'review-2 items[9] byKey gcd does not infer reachability from the gcd', txt)

lv.check_wrongs()
lv.report()
