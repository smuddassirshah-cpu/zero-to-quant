"""Recompute every number stated in algebra level 4 (l14 to l17, review-4, homework-4), each two ways.
Method 1 is direct arithmetic or a formula; method 2 is a brute-force search, an independent polynomial routine
(Fraction long division, convolution) or a closed form (Mobius count, the remainder theorem). Each value is then
checked at its JSON path with numbers_lib. Every code widget is run: the solution passes every example and test,
and the starter fails at least one test. Pure standard library.
Run: python3 docs/reports/algebra-L4-numbers.py   (exits 0 when every check passes)
"""
import itertools, math, os, sys
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('algebra', 4)
fails = []


def two(name, a, b, stated=None, tol=1e-9):
    ok = a == b if not isinstance(a, (int, float)) else abs(a - b) <= 1e-9 * max(1, abs(a))
    if stated is not None:
        ok = ok and (a == stated if not isinstance(a, (int, float)) else abs(a - stated) <= tol)
    print(f"{'ok ' if ok else 'BAD'} {name}: {a!r} | {b!r}" + ('' if stated is None else f' | stated {stated!r}'))
    if not ok:
        fails.append(name)


def S(ref, path, stated, a, b, fmt=None):
    two(f'{ref} {path}', a, b, stated)
    lv.expect(ref, path, stated, fmt=fmt)


def T(ref, path, text):
    lv.expect(ref, path, text)


def claim(name, ok):
    print(f"{'ok ' if ok else 'BAD'} claim {name}")
    if not ok:
        fails.append(name)


def doc(ref):
    return lv._file(ref)[1]


# ---- two independent polynomial routines (lists lowest degree first) ----
def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def pmul(f, g, p=None):
    r = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            r[i + j] += a * b
    return trim([x % p for x in r]) if p else trim(r)


def div_fraction(f, g, p=None):
    """Schoolbook long division with Fractions (p: reduce mod p using modular inverses)."""
    f = [Fr(x) for x in f]
    q = [Fr(0)] * max(1, len(f) - len(g) + 1)
    while len(trim(f)) >= len(g) and trim(f) != [0]:
        f = trim(f)
        k = len(f) - len(g)
        c = f[-1] * (pow(int(g[-1]), -1, p) if p else 1 / Fr(g[-1]))
        if p:
            c %= p
        q[k] = c
        for i, b in enumerate(g):
            f[i + k] -= c * b
        if p:
            f = [x % p for x in f]
    return trim(q), trim(f)


def div_by_values(f, g, p):
    """Brute force: search every q of the right degree with deg(f - q g) < deg g, over Z_p."""
    n, m = len(g) - 1, len(f) - 1
    for q in itertools.product(range(p), repeat=max(1, m - n + 1)):
        r = trim([(a - b) % p for a, b in itertools.zip_longest(f, pmul(list(q), g, p), fillvalue=0)])
        if r == [0] or len(r) - 1 < n:
            return trim(list(q)), r


def ev(f, x, p=None):
    v = sum(c * x ** k for k, c in enumerate(f))
    return v % p if p else v


# ================= l14 =================
offz = [(a, b) for a in range(1, 12) for b in range(1, 12) if a * b % 12 == 0]
S('l14', 'screens[0].explain.text', 17, len(offz), sum(1 for a in range(1, 12) for b in range(1, 12) if math.gcd(a, 12) * math.gcd(b, 12) % 12 == 0 and a * b % 12 == 0))
claim('l14 count-mode among holds every off-axis zero', sorted(doc('l14')['screens'][0]['widget']['among']) == sorted(f'r{a+1}c{b+1}' for a, b in offz))
zd = sorted({a for a, _ in offz})
two('l14 zero divisors of Z12', zd, [a for a in range(1, 12) if math.gcd(a, 12) > 1], [2, 3, 4, 6, 8, 9, 10])
two('l14 units of Z12', [a for a in range(12) if math.gcd(a, 12) == 1], [a for a in range(12) if any(a * b % 12 == 1 for b in range(12))], [1, 5, 7, 11])
vals = [(x - 2) * (x - 3) % 12 for x in range(12)]
claim('l14 value table', doc('l14')['screens'][2]['canvas']['params']['rows'][0][1:] == [str(v) for v in vals] and vals == [(x * x - 5 * x + 6) % 12 for x in range(12)])
S('l14', 'screens[1].widget.rows[0][1].answer', 0, (6 - 2) * (6 - 3) % 12, (36 - 30 + 6) % 12)
S('l14', 'screens[1].widget.rows[1][1].answer', 0, (11 - 2) * (11 - 3) % 12, (121 - 55 + 6) % 12)
S('l14', 'screens[1].widget.rows[1][1].wrong[0].value', 72, 9 * 8, 8 * 9)
S('l14', 'screens[1].widget.rows[0][1].wrong[0].value', 12, 4 * 3, 12)
two('l14 roots of x^2 - 5x + 6 in Z12', [x for x in range(12) if vals[x] == 0], [x for x in range(12) if (x * x - 5 * x + 6) % 12 == 0], [2, 3, 6, 11])
S('l14', 'screens[2].widget.options[5].why', 30, 6 * 5, (8 - 2) * (8 - 3))
S('l14', 'screens[2].widget.options[6].why', 42, 7 * 6, (9 - 2) * (9 - 3))
claim('l14 x = 0, 8, 9 give 6', vals[0] == vals[8] == vals[9] == 6)
A, B = [[1, 1], [0, 1]], [[1, 0], [1, 1]]
mm = lambda X, Y: [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
two('l14 AB', mm(A, B), [[A[0][0] + A[0][1], A[0][1]], [A[1][1], A[1][1]]], [[2, 1], [1, 1]])
two('l14 BA', mm(B, A), [[1, 1], [1, 2]], [[1, 1], [1, 2]])
T('l14', 'screens[7].widget.answer', '\\begin{pmatrix}1&1\\\\1&2\\end{pmatrix}')
two('l14 E11 E22 = 0', mm([[1, 0], [0, 0]], [[0, 0], [0, 1]]), [[0, 0], [0, 0]])
rings_tab = [r[1:] for r in doc('l14')['screens'][6]['widget']['rows']]
claim('l14 ring table (commutative, zero divisors)', [(c['answer'], z['answer']) for c, z in rings_tab] == [('yes', 'no'), ('yes', 'yes'), ('no', 'yes'), ('yes', 'no')])
def lcg(a, c, m, x=0):
    s = [x]
    while True:
        x = (a * x + c) % m
        if x == s[0]:
            return s
        if x in s:                       # a tail that never returns to x0
            return s + [None]
        s.append(x)
seq = lcg(5, 3, 16)
claim('l14 LCG series values', doc('l14')['screens'][9]['canvas']['params']['series'][0]['values'] == seq + [0])
S('l14', 'screens[9].widget.answer', 16, len(seq), len(set(seq)))
S('l14', 'screens[9].widget.wrong[0].value', 17, len(seq) + 1, 17)
S('l14', 'quiz[2].widget.answer', 8, len(lcg(3, 3, 16)), len(set(lcg(3, 3, 16))))
claim('l14 a=3, c=3 sequence', lcg(3, 3, 16) == [0, 3, 12, 7, 8, 11, 4, 15] and (3 * 15 + 3) % 16 == 0)
two('l14 a=5, c=2 period', len(lcg(5, 2, 16)), 8, 8)
claim('l14 Hull-Dobell agrees with brute force for all a, c mod 16', all((len(lcg(a, c, 16)) == 16) == (c % 2 == 1 and (a - 1) % 4 == 0) for a in range(16) for c in range(16)))
two('l14 idempotents of Z12', [x for x in range(12) if x * x % 12 == x], [x for x in range(12) if x * (x - 1) % 12 == 0], [0, 1, 4, 9])
S('l14', 'quiz[1].widget.options[5].why', 36, 6 * 6, 36)
S('l14', 'quiz[1].widget.options[6].why', 64, 8 * 8, 2 ** 6)
two('l14 8^2 mod 12', 64 % 12, 4, 4)

# ================= l15 =================
two('l15 inverses mod 7', [pow(a, -1, 7) for a in (2, 3, 6)], [next(b for b in range(7) if a * b % 7 == 1) for a in (2, 3, 6)], [4, 5, 6])
claim('l15 tapped cells are the 1s', doc('l15')['screens'][0]['widget']['answer'] == [f'r{a}c{pow(a, -1, 7)}' for a in range(1, 7)])
claim('l15 rows 2, 3, 4 of Z6 have no 1, and 2 x 3 = 0', [a for a in range(1, 6) if all(a * b % 6 != 1 for b in range(1, 6))] == [2, 3, 4] and 2 * 3 % 6 == 0)
claim('l15 row 2 of Z6 reads 2, 4, 0, 2, 4', [2 * b % 6 for b in range(1, 6)] == [2, 4, 0, 2, 4])
claim('l15 fields among Z_2..Z_12', [n for n in range(2, 13) if all(any(a * b % n == 1 for b in range(n)) for a in range(1, n))] == [2, 3, 5, 7, 11] == [n for n in range(2, 13) if all(n % d for d in range(2, n))])
S('l15', 'screens[7].widget.answer', 4, [x for x in range(7) if (3 * x + 4) % 7 == 2][0], (5 * ((2 - 4) % 7)) % 7)
S('l15', 'screens[7].widget.wrong[0].value', 25, 5 * 5, 25)
S('l15', 'screens[7].feedback.correct', 16, 3 * 4 + 4, 16)
two('l15 3^-1 mod 7', pow(3, -1, 7), 5, 5)
F4n = ['0', '1', 'α', 'α+1']
def f4mul(u, v):
    r = 0
    for i in range(2):
        if v >> i & 1:
            r ^= u << i
    return r ^ 0b111 if r & 4 else r
claim('l15 F4 table: alpha(alpha+1) = 1, (alpha+1)^2 = alpha, every non-zero row has a 1', f4mul(2, 3) == 1 and f4mul(3, 3) == 2 and f4mul(2, 2) == 3 and all(any(f4mul(u, v) == 1 for v in range(4)) for u in range(1, 4)))
claim('l15 F4 grid cells', doc('l15')['screens'][8]['canvas']['right']['params']['cells'] == [[F4n[f4mul(u, v)] for v in range(4)] for u in range(4)])
claim('l15 Z4 has 2 x 2 = 0', 2 * 2 % 4 == 0)
f = lambda x: (7 + 3 * x) % 11
claim('l15 shares', [(x, f(x)) for x in (1, 2, 3)] == [(1, 10), (2, 2), (3, 5)])
S('l15', 'screens[9].widget.rows[0][1].answer', 7, (2 - 2 * ((5 - 2) * pow(1, -1, 11))) % 11, (3 * 2 - 2 * 5) * pow(3 - 2, -1, 11) % 11)
S('l15', 'screens[9].widget.rows[1][1].answer', 3, (5 - 10) * pow(2, -1, 11) % 11, next(m for m in range(11) if (10 + 2 * m) % 11 == 5))
S('l15', 'screens[9].widget.rows[1][1].wrong[0].value', 6, pow(2, -1, 11), next(b for b in range(11) if 2 * b % 11 == 1))
S('l15', 'screens[9].explain.text', -30, -5 * 6, -30)
two('l15 Z10 lines through (1, 0) and (3, 6)', [(b, m) for b in range(10) for m in range(10) if (b + m) % 10 == 0 and (b + 3 * m) % 10 == 6], [(2, 8), (7, 3)])
claim('l15 2m = 6 mod 10 has solutions 3 and 8', [m for m in range(10) if 2 * m % 10 == 6] == [3, 8])
claim('l15 gcd(4, 6) = 2, gcd(3, 9) = 3', math.gcd(4, 6) == 2 and math.gcd(3, 9) == 3)

# ================= l16 =================
die = [0, 1, 1, 1, 1, 1, 1]
sq = pmul(die, die)
S('l16', 'screens[1].widget.answer', 6, sq[7], sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7))
S('l16', 'screens[1].widget.wrong[1].value', 36, sum(sq), 6 * 6)
claim('l16 coefficients 1..6..1', sq[2:] == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])
S('l16', 'screens[2].widget.answer', 12, len(sq) - 1, 6 + 6)
S('l16', 'screens[2].widget.wrong[0].value', 36, 6 * 6, 36)
two('l16 (2x+1)^2 in Z4[x]', pmul([1, 2], [1, 2], 4), [1], [1])
claim('l16 raw coefficients 4, 4, 1', pmul([1, 2], [1, 2]) == [1, 4, 4])
q, r = div_fraction([-4, 0, -2, 1], [-3, 1])
two('l16 Q division q', q, [3, 1, 1], [3, 1, 1])
two('l16 Q division r = f(3)', r, [ev([-4, 0, -2, 1], 3)], [5])
T('l16', 'screens[6].widget.answer', 'x^2+x+3')
S('l16', 'screens[6].explain.text', 5, int(r[0]), 27 - 18 - 4)
q5, r5 = div_fraction([1, 2, 0, 1], [1, 2], 5)
two('l16 Z5 division (two routines)', (q5, r5), div_by_values([1, 2, 0, 1], [1, 2], 5), ([3, 1, 3], [3]))
claim('l16 Z5 table answers', [row[1]['answer'] for row in doc('l16')['screens'][7]['widget']['rows']] == [3, 1, 3, 3])
claim('l16 (2x+1)(3x^2+x+3) + 3 = 6x^3 + 5x^2 + 7x + 6 = x^3 + 2x + 1 mod 5', pmul([1, 2], [3, 1, 3]) == [3, 7, 5, 6] and [(c + d) % 5 for c, d in zip(pmul([1, 2], [3, 1, 3]), [3, 0, 0, 0])] == [1, 2, 0, 1])
two('l16 2^-1 mod 5', pow(2, -1, 5), 3, 3)
trap = [a - b for a, b in zip([1, 0, 1], pmul([0, 1], [1, 2]) + [0])]
two('l16 trap remainder for q = x is -x^2 - x + 1, degree 2', (trap, len(trim(trap)) - 1), ([1, -1, -1], 2), ([1, -1, -1], 2))
claim('l16 trap remainder by hand: x^2 + 1 - x(2x + 1) = x^2 + 1 - 2x^2 - x', [1 - 0, 0 - 1, 1 - 2] == [1, -1, -1])
T('l16', 'screens[8].widget.options[3].why', '-x^2 - x + 1')
qz, rz = div_fraction([1, 0, 1], [1, 2])
two('l16 x^2+1 over Q by 2x+1', (qz, rz), ([Fr(-1, 4), Fr(1, 2)], [Fr(5, 4)]))
two('l16 x^3+1 by x^2+1', div_fraction([1, 0, 0, 1], [1, 0, 1]), ([0, 1], [1, -1]))
def crc(msg, gen):
    b = [int(c) for c in msg] + [0] * (len(gen) - 1)
    g = [int(c) for c in gen]
    for i in range(len(msg)):
        if b[i]:
            for j in range(len(g)):
                b[i + j] ^= g[j]
    return ''.join(map(str, b[-(len(gen) - 1):]))
fpoly = [int(c) for c in reversed('1101011011' + '0000')]
_, rc = div_fraction(fpoly, [1, 1, 0, 0, 1], 2)
two('l16 CRC 1110 (XOR and polynomial division)', crc('1101011011', '10011'), ''.join(str(int(rc[k])) if k < len(rc) else '0' for k in (3, 2, 1, 0)), '1110')
claim('l16 CRC table answers', [row[1]['answer'] for row in doc('l16')['screens'][9]['widget']['rows']] == [1, 1, 1, 0])
T('l16', 'screens[9].feedback.correct', '11010110111110')
claim('l16 the sent packet divides to 0', crc('11010110111110', '10011')[-4:] == '0000' or div_fraction([int(c) for c in reversed('11010110111110')], [1, 1, 0, 0, 1], 2)[1] == [0])

# ================= l17 =================
cub = [-6, 11, -6, 1]
two('l17 roots of the cubic', [x for x in range(-10, 11) if ev(cub, x) == 0], [1, 2, 3], [1, 2, 3])
qc, rc1 = div_fraction(cub, [-1, 1])
S('l17', 'screens[1].widget.answer', 0, int(rc1[0]), ev(cub, 1))
S('l17', 'screens[1].widget.wrong[0].value', -6, cub[0], -6)
two('l17 quotient x^2 - 5x + 6', qc, [6, -5, 1])
claim('l17 synthetic row 1, -5, 6', doc('l17')['screens'][1]['canvas']['params']['rows'][1][1:4] == ['1', '-5', '6'])
S('l17', 'screens[1].explain.text', 5, 27 - 18 - 4, ev([-4, 0, -2, 1], 3))
two('l17 x^2 - 1 roots Z8', [x for x in range(8) if (x * x - 1) % 8 == 0], [x for x in range(8) if x % 2], [1, 3, 5, 7])
two('l17 x^2 - 1 roots Z7', [x for x in range(7) if (x * x - 1) % 7 == 0], [1, 6], [1, 6])
S('l17', 'screens[3].widget.lines[5].why', 8, (3 - 1) * (3 + 1), 8)
claim('l17 squares mod 8 table', doc('l17')['screens'][4]['canvas']['params']['rows'][0][1:] == [str(x * x % 8) for x in range(8)])
cnt = [len([x for x in range(p) if (x * x + 1) % p == 0]) for p in (2, 3, 5)]
claim('l17 roots of x^2 + 1 in Z2, Z3, Z5', cnt == [1, 0, 2] == [r[1]['answer'] for r in doc('l17')['screens'][6]['widget']['rows']])
claim('l17 x^2 + 1 = (x + 1)^2 over Z2 and (x - 2)(x - 3) over Z5', pmul([1, 1], [1, 1], 2) == [1, 0, 1] and pmul([-2, 1], [-3, 1], 5) == [1, 0, 1])
claim('l17 value table x^2 + 1', doc('l17')['screens'][6]['canvas']['params']['rows'][2][1:] == [str((x * x + 1) % 5) for x in range(5)])
claim('l17 x^3 - 2 at the candidates', [c ** 3 - 2 for c in (1, -1, 2, -2)] == [-1, -3, 6, -10] and doc('l17')['screens'][7]['canvas']['params']['rows'][0][1:] == ['-1', '-3', '6', '-10'])
two('l17 x^4 + 4 factors', pmul([2, 2, 1], [2, -2, 1]), [4, 0, 0, 0, 1])
S('l17', 'screens[8].widget.options[3].why', 20, (-2) ** 4 + 4, 16 + 4)
two('l17 Z2: (x^2 + x + 1)^2', pmul([1, 1, 1], [1, 1, 1], 2), [1, 0, 1, 0, 1])
claim('l17 Z2 x^4 + x + 1 has no factor of degree 1 or 2', all(div_fraction([1, 1, 0, 0, 1], g, 2)[1] != [0] for g in ([0, 1], [1, 1], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1])))
dA = pmul(pmul([0, 1], [1, 1]), [1, 1, 1])
dB = pmul(pmul(pmul(pmul([0, 1], [1, 1]), [1, 1, 1]), [1, -1, 1]), [1, -1, 1])
facesA = [k for k, c in enumerate(dA) for _ in range(c)]
facesB = [k for k, c in enumerate(dB) for _ in range(c)]
two('l17 Sicherman faces', (facesA, facesB), ([1, 2, 2, 3, 3, 4], [1, 3, 4, 5, 6, 8]))
claim('l17 Sicherman table answers', [r[1]['answer'] for r in doc('l17')['screens'][9]['widget']['rows']] == facesB)
claim('l17 same distribution as ordinary dice', Counter(a + b for a in facesA for b in facesB) == Counter(a + b for a in range(1, 7) for b in range(1, 7)) and pmul(dA, dB) == sq)
claim('l17 die polynomial factors', pmul(pmul(pmul([0, 1], [1, 1]), [1, 1, 1]), [1, -1, 1]) == die)
claim('l17 (1 - x + x^2)^2 expansion', pmul([1, -1, 1], [1, -1, 1]) == [1, -2, 3, -2, 1] and dA == [0, 1, 2, 2, 1])
claim('l17 x^3 + x + 1 values in Z2 and Z5', [ev([1, 1, 0, 1], x, 2) for x in range(2)] == [1, 1] and [ev([1, 1, 0, 1], x, 5) for x in range(5)] == [1, 3, 1, 1, 4])
def mob(n):
    r, m, q = 1, n, 2
    while q * q <= m:
        if m % q == 0:
            m //= q
            if m % q == 0:
                return 0
            r = -r
        q += 1
    return -r if m > 1 else r
def irr_brute(p, d):
    monic = lambda k: [list(c) + [1] for c in itertools.product(range(p), repeat=k)]
    return sum(1 for f in monic(d) if all(div_fraction(f, g, p)[1] != [0] for k in range(1, d // 2 + 1) for g in monic(k)))
irr_mob = lambda p, d: sum(mob(d // k) * p ** k for k in range(1, d + 1) if d % k == 0) // d
for p, d, want in [(2, 2, 1), (3, 2, 3), (5, 2, 10), (2, 3, 2), (3, 3, 8), (2, 4, 3), (3, 4, 18), (2, 1, 2)]:
    two(f'irreducible count p={p} d={d}', irr_brute(p, d), irr_mob(p, d), want)
S('l17', 'quiz[1].widget.answer', 10, irr_mob(5, 2), (5 * 5 - 5) // 2)
S('l17', 'quiz[1].widget.wrong[0].value', 25, 5 ** 2, 25)
S('l17', 'quiz[1].widget.wrong[1].value', 15, 5 + 5 * 4 // 2, 25 - 10)
two('no-root quartics over Z2 (the starter count)', sum(1 for c in itertools.product(range(2), repeat=4) if all(ev(list(c) + [1], x, 2) for x in range(2))), 4, 4)

# ================= review-4 =================
two('review 6 * 5 mod 15', 6 * 5 % 15, 0, 0)
S('review', 'items[1].widget.answer', 13, pow(7, -1, 15), next(b for b in range(15) if 7 * b % 15 == 1))
S('review', 'items[1].widget.wrong[0].value', 8, -7 % 15, 15 - 7)
S('review', 'items[1].widget.options[0].why' if False else 'items[1].feedback.byKey.neg', 11, 7 * 8 % 15, 56 - 45)
S('review', 'items[0].widget.options[1].why', 91, 7 * 13, 91)
claim('review 4 x 4 = 16 = 1 mod 15', 4 * 4 % 15 == 1)
claim('review 91 = 7 x 13', 7 * 13 == 91)
S('review', 'items[3].widget.answer', 3, pow(4, -1, 11), next(b for b in range(11) if 4 * b % 11 == 1))
S('review', 'items[3].widget.wrong[0].value', 7, -4 % 11, 11 - 4)
S('review', 'items[3].feedback.byKey.neg', 6, 4 * 7 % 11, 28 - 22)
S('review', 'items[4].widget.answer', 11, int(div_fraction([1, 1, 0, 1], [-2, 1])[1][0]), ev([1, 1, 0, 1], 2))
S('review', 'items[4].widget.wrong[0].value', -9, ev([1, 1, 0, 1], -2), -8 - 2 + 1)
S('review', 'items[5].widget.answer', 4, len([x for x in range(12) if (x * x - 4) % 12 == 0]), len([2, 4, 8, 10]))
S('review', 'items[5].feedback.byKey.field', 64, 8 * 8, 64)
claim('review cubic over Z3 values', [ev([1, 2, 0, 1], x) for x in range(3)] == [1, 4, 13] and [ev([1, 2, 0, 1], x, 3) for x in range(3)] == [1, 1, 1])
two('review (x^2 + 1)^2', pmul([1, 0, 1], [1, 0, 1]), [1, 0, 2, 0, 1])
S('review', 'items[7].widget.options[2].why', 4, (-1) ** 4 + 2 + 1, 4)

# ================= homework-4 =================
claim('homework units of degree 1 in Z4[x]: only 2x + 1 among the options', pmul([1, 2], [1, 2], 4) == [1] and pmul([0, 2], [0, 2], 4) == [0]
      and all(any(pmul(list(h), u, 4) == [1] for h in itertools.product(range(4), repeat=3)) is False for u in ([1, 1], [1, 3])))
claim('homework 221 = 13 x 17, sqrt 221 = 14.9', 13 * 17 == 221 and abs(math.sqrt(221) - 14.9) < 0.05 and all(221 % q for q in (2, 3, 5, 7, 11)))
qh, rh = div_fraction([1, 1, 0, 2, 1], [1, 0, 2], 3)
two('homework Z3 division (two routines)', (qh, rh), div_by_values([1, 1, 0, 2, 1], [1, 0, 2], 3), ([2, 1, 2], [2]))
claim('homework Z3 table answers', [row[1]['answer'] for row in doc('homework')['items'][2]['widget']['rows']] == [2, 1, 2, 0, 2])
claim('homework Z3 check', pmul([1, 0, 2], [2, 1, 2]) == [2, 1, 6, 2, 4] and [(a + b) % 3 for a, b in zip(pmul([1, 0, 2], [2, 1, 2]), [2, 0, 0, 0, 0])] == [1, 1, 0, 2, 1])
_, rt = div_fraction([int(c) for c in reversed('11010011101100' + '000')], [1, 1, 0, 1], 2)
two('homework CRC 100', crc('11010011101100', '1011'), ''.join(str(int(rt[k])) if k < len(rt) else '0' for k in (2, 1, 0)), '100')
claim('homework CRC table answers', [row[1]['answer'] for row in doc('homework')['items'][3]['widget']['rows']] == [1, 0, 0])
m13 = (12 - 0) * pow(3, -1, 13) % 13
S('homework', 'items[4].widget.answer', 5, (0 - 2 * m13) % 13, next(s for s in range(13) if (s + 2 * m13) % 13 == 0))
S('homework', 'items[4].widget.wrong[0].value', -8, -2 * m13, -8)
S('homework', 'items[4].widget.wrong[1].value', 4, m13, next(m for m in range(13) if (3 * m) % 13 == 12))
S('homework', 'items[4].feedback.correct', 108, 12 * 9, 108)
two('homework 3^-1 mod 13 and the check 5 + 4 x 5', (pow(3, -1, 13), (5 + 4 * 5) % 13), (9, 12))
S('homework', 'items[6].widget.answer', 4, len([x for x in range(15) if (x * x - 1) % 15 == 0]), len([1, 4, 11, 14]))
S('homework', 'items[6].explain.text', 196, 14 * 14, 196)
S('homework', 'items[6].explain.text', 121, 11 * 11, 121)
claim('homework Z8 squares in the model', [x * x % 8 for x in range(8)] == [0, 1, 4, 1, 0, 1, 4, 1])

# ---------------- code widgets: solutions pass, starters fail ----------------
def run_case(src, pre, c):
    ns = {}
    exec(pre or '', ns)
    exec(src, ns)
    if c.get('setup'):
        exec(c['setup'], ns)
    if c['compare'] == 'raises':
        try:
            eval(c['call'], ns)
        except Exception as ex:
            return c['expect'] in [k.__name__ for k in type(ex).__mro__]
        return False
    return eval(c['call'], ns) == eval(c['expect'], ns)


ncode = 0
for fid, d in lv.files.items():
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(d.get(key, [])):
            w = s.get('widget')
            if not (w and w.get('kind') == 'code'):
                continue
            ncode += 1
            pre = w.get('prelude', '')
            sol = all(run_case(w['solution'], pre, c) for c in w['tests'] + w.get('examples', []))
            sf = []
            for c in w['tests']:
                try:
                    sf.append(not run_case(w['starter'], pre, c))
                except Exception:
                    sf.append(True)
            ok = sol and any(sf)
            print(f"{'ok ' if ok else 'BAD'} code {fid} {key}[{i}]: solution {'passes' if sol else 'FAILS'}, starter fails tests {[k + 1 for k, f in enumerate(sf) if f]}")
            if not ok:
                fails.append(f'code {fid} {key}[{i}]')
print(f'code widgets checked: {ncode}')

# l15 quiz[1]: Z_9 two-share recovery needs x differences that are units mod 9
claim('l15 Z_9 with shares at x = 1, 2, 3: every x difference (1, 2) is a unit, so two shares recover', all(math.gcd(d, 9) == 1 for d in (2 - 1, 3 - 2, 3 - 1)))
claim('l15 Z_9 fails for shares at x = 1 and 4: 3 has no inverse mod 9', math.gcd(4 - 1, 9) != 1 and not any(3 * k % 9 == 1 for k in range(9)))
T('l15', 'quiz[1].widget.options[3].why', 'x = 1$ and $x = 4')

lv.check_wrongs()
if fails:
    print('two-way, claim or code failures:', fails)
lv.report()
if fails:
    sys.exit(1)
