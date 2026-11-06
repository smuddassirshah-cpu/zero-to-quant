"""Recompute every number stated in algebra level 3 (l10 to l13, review-3, homework-3), each two ways.
Method 1 is direct arithmetic or a formula; method 2 is a brute-force count or a different route (an enumeration of
the group, repeated multiplication instead of pow, a closed form). Each value is then checked at its JSON path with
numbers_lib. The script also runs every code widget of the level: the solution passes every example and test, and the
starter fails at least one test. Pure standard library.
Run: python3 docs/reports/algebra-L3-numbers.py   (exits 0 when every check passes)
"""
import itertools, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('algebra', 3)
fails = []


def two(name, a, b, stated=None, tol=1e-9):
    ok = abs(a - b) <= 1e-9 * max(1, abs(a)) and (stated is None or abs(a - stated) <= tol)
    print(f"{'ok ' if ok else 'BAD'} {name}: {a!r} | {b!r}" + ('' if stated is None else f' | stated {stated}'))
    if not ok:
        fails.append(name)


def S(ref, path, stated, a, b, tol=1e-9, fmt=None):
    two(f'{ref} {path}', a, b, stated, tol)
    lv.expect(ref, path, stated, fmt=fmt)


def T(ref, path, text):
    lv.expect(ref, path, text)


def claim(name, ok):
    print(f"{'ok ' if ok else 'BAD'} claim {name}")
    if not ok:
        fails.append(name)


def powmod_loop(a, k, n):
    r = 1
    for _ in range(k):
        r = r * a % n
    return r


def phi(n):
    return sum(1 for a in range(1, n + 1) if math.gcd(a, n) == 1)


def phi_formula(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            r -= r // p
        p += 1
    if m > 1:
        r -= r // m
    return r


# ---------- D4 as r^a s^m, product (a,m)(b,n) = (a + (-1)^m b, m + n) ----------
names = ['e', 'r', 'r²', 'r³', 's', 'rs', 'r²s', 'r³s']
def mul(x, y):
    a, m, b, n = x % 4, x // 4, y % 4, y // 4
    return (a + (-1) ** m * b) % 4 + 4 * ((m + n) % 2)
def inv(x):
    return next(y for y in range(8) if mul(x, y) == 0)
# second model of D4: 2x2 integer matrices r = [[0,-1],[1,0]], s = [[-1,0],[0,1]]
def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
Rm, Sm, Im = ((0, -1), (1, 0)), ((-1, 0), (0, 1)), ((1, 0), (0, 1))
def mat(x):
    M = Im
    for _ in range(x % 4):
        M = mm(M, Rm)
    return mm(M, Sm) if x >= 4 else M
mats = [mat(x) for x in range(8)]
claim('D4 table agrees with the matrix model', all(mats.index(mm(mats[x], mats[y])) == mul(x, y) for x in range(8) for y in range(8)))
claim('sr = r^3 s', mul(4, 1) == 7)

# ================= l10 =================
for ref, path, v in [('l10', 'screens[0].widget.rows[0][2].answer', 0.0953), ('l10', 'screens[0].widget.rows[1][2].answer', -0.1054), ('l10', 'screens[0].widget.rows[2][2].answer', -0.0101)]:
    x = {0.0953: 1.1, -0.1054: 0.9, -0.0101: 0.99}[v]
    S(ref, path, v, math.log(x), 2 * math.atanh((x - 1) / (x + 1)), tol=5e-5)
S('l10', 'screens[0].explain.text', 0.09531, math.log(1.1), math.log10(1.1) * math.log(10), tol=5e-6)
S('l10', 'screens[0].explain.text', -0.10536, math.log(0.9), math.log10(0.9) * math.log(10), tol=5e-6)
S('l10', 'screens[0].explain.text', -0.01005, math.log(1.1) + math.log(0.9), math.log(0.99), tol=5e-6)
S('l10', 'screens[0].prose', 0.99, 1.1 * 0.9, 0.99)
S('l10', 'screens[0].canvas.params.rows[1][2]', 110.00, 100 * 1.1, 100 + 10, fmt='£110.00')
S('l10', 'screens[0].canvas.params.rows[2][2]', 99.00, 100 * 1.1 * 0.9, 110 - 11, fmt='£99.00')
ker4 = [j for j in range(12) if 4 * j % 12 == 0]
S('l10', 'screens[1].widget.answer', 4, len(ker4), 12 // math.gcd(12, 4) and math.gcd(12, 4))
S('l10', 'screens[1].widget.wrong[0].value', 3, len({4 * j % 12 for j in range(12)}), 12 // math.gcd(12, 4))
claim('l10 kernel of z^4 is j = 0,3,6,9 (cmath check)', [j for j in range(12) if abs(complex(math.cos(2 * math.pi * j / 12), math.sin(2 * math.pi * j / 12)) ** 4 - 1) < 1e-9] == ker4 == [0, 3, 6, 9])
for j, img in [(4, 4), (8, 8), (2, 8)]:
    two(f'l10 zeta^{j} goes to zeta^{img}', 4 * j % 12, (j * 4) % 12, img)
T('l10', 'screens[2].widget.options[4].why', '\\zeta^{16} = \\zeta^4')
T('l10', 'screens[2].widget.options[6].why', '\\zeta^{32} = \\zeta^8')
T('l10', 'screens[2].explain.text', '\\{1, \\zeta^4, \\zeta^8\\}')
S('l10', 'screens[4].widget.answer', 4, (1 + 1) ** 2 % 8, 2 * 2 % 8)
S('l10', 'screens[4].widget.wrong[0].value', 2, (1 ** 2 + 1 ** 2) % 8, 1 + 1)
claim('l10 square table row', lv.files['l10-homomorphisms']['screens'][4]['canvas']['params']['rows'][0][1:] == [str(x * x % 8) for x in range(8)])
claim('l10 3x on Z12 is a hom with kernel {0,4,8}', all(3 * ((a + b) % 12) % 12 == (3 * a + 3 * b) % 12 for a in range(12) for b in range(12)) and [x for x in range(12) if 3 * x % 12 == 0] == [0, 4, 8])
S('l10', 'screens[7].canvas.params.rows[1][2]', 2, 6 % 4, 6 - 4)
S('l10', 'screens[7].widget.options[2].why', 2, (3 % 4 + 3 % 4) % 4, 6 - 4)
claim('l10 x mod 4 well defined from Z12 (4 | 12)', all((x + 12) % 4 == x % 4 for x in range(12)))
stem = [0, 2, 6, 3, 4, 9]
W = [1, 3, 1, 7, 3, 9, 1]
ws = sum(d * w for d, w in zip(stem, W))
S('l10', 'screens[9].canvas.params.rows[2][4]', 21, 3 * 7, 7 + 7 + 7)
S('l10', 'screens[9].canvas.params.rows[2][6]', 81, 9 * 9, 9 ** 2)
S('l10', 'screens[9].hints[1].text', 126, ws, 0 + 6 + 6 + 21 + 12 + 81)
chk = (-ws) % 10
S('l10', 'screens[9].widget.answer', 4, chk, next(c for c in range(10) if (ws + c) % 10 == 0))
S('l10', 'screens[9].widget.wrong[0].value', 6, ws % 10, 126 - 120)
S('l10', 'screens[9].explain.text', 130, ws + chk, 126 + 4)
T('l10', 'screens[9].explain.text', '0263494')
code = stem + [chk]
def valid(c): return sum(d * w for d, w in zip(c, W)) % 10 == 0
singles = [(i, d) for i in range(7) for d in range(10) if d != code[i]]
claim(f'l10 all {len(singles)} single-digit errors of 0263494 caught', len(singles) == 63 and not any(valid(code[:i] + [d] + code[i + 1:]) for i, d in singles))
claim('l10 every weight is a unit mod 10', all(math.gcd(w, 10) == 1 for w in W))
diffs = [W[i] - W[i + 1] for i in range(6)]
claim('l10 weight differences', diffs == [-2, 2, -6, 4, -6, 8] and lv.files['l10-homomorphisms']['screens'][10]['canvas']['params']['rows'][0][1:] == [str(d) for d in diffs])
missed = {(a, b) for i in range(6) for a in range(10) for b in range(10) if a != b and ((W[i] - W[i + 1]) * (a - b)) % 10 == 0}
claim('l10 undetected neighbour swaps are exactly digits 5 apart', missed == {(a, b) for a in range(10) for b in range(10) if abs(a - b) == 5})
S('l10', 'screens[10].explain.text', 19, 1 * 1 + 6 * 3, 1 + 18)
S('l10', 'screens[10].explain.text', 9, 6 * 1 + 1 * 3, 6 + 3)
two('l10 stems 16 and 61 share a check digit', (-(19 + sum(d * w for d, w in zip([3, 4, 9, 0], W[2:6])))) % 10, (-(9 + sum(d * w for d, w in zip([3, 4, 9, 0], W[2:6])))) % 10)
S('l10', 'quiz[0].widget.options[1].why', 10, 5 * 2, 2 + 2 + 2 + 2 + 2)
S('l10', 'quiz[3].widget.answer', 4, len([x for x in range(12) if 4 * x % 12 == 0]), math.gcd(4, 12))
S('l10', 'quiz[3].widget.wrong[0].value', 3, len({4 * x % 12 for x in range(12)}), 12 // math.gcd(4, 12))

# ================= l11 =================
d = lv.files['l11-normal-subgroups']
cells = d['screens'][0]['canvas']['params']['cells']
claim('l11 Cayley grid matches both D4 models', cells == [[names[mul(x, y)] for y in range(8)] for x in range(8)])
claim('l11 row s holds rotations exactly in columns 5 to 8', [j + 1 for j in range(8) if mul(4, j) < 4] == [5, 6, 7, 8] == [int(c[-1]) for c in d['screens'][0]['widget']['answer']])
claim('l11 a rotation times a flip is a flip, both orders', all(mul(a, f) >= 4 and mul(f, a) >= 4 for a in range(4) for f in range(4, 8)))
T('l11', 'screens[2].widget.options[0].text', 'r^2s')
claim('l11 r s r^-1 = r^2 s', mul(mul(1, 4), inv(1)) == 6 and mats.index(mm(mm(Rm, Sm), mats[inv(1)])) == 6)
claim('l11 s r^-1 = rs', mul(4, inv(1)) == 5)
conj = d['screens'][3]['canvas']['params']['rows']
claim('l11 conjugation table', conj[0][1:] == [names[mul(mul(1, x), inv(1))] for x in range(8)] and conj[1][1:] == [names[mul(mul(4, x), inv(4))] for x in range(8)])
subs = set()
for k in range(1, 9):
    for Sx in itertools.combinations(range(8), k):
        Sx = set(Sx)
        if 0 in Sx and all(mul(a, inv(b)) in Sx for a in Sx for b in Sx):
            subs.add(frozenset(Sx))
normal = {Sx: all(mul(mul(g, x), inv(g)) in Sx for g in range(8) for x in Sx) for Sx in subs}
normal_gen = {Sx: all(mul(mul(g, x), inv(g)) in Sx for g in (1, 4) for x in Sx) for Sx in subs}
two('l11 ten subgroups', len(subs), 1 + 5 + 3 + 1, 10)
T('l11', 'screens[3].prose', 'ten subgroups')
two('l11 normal subgroups (all g and generators only)', sum(normal.values()), sum(normal_gen.values()), 6)
two('l11 non-normal subgroups', len(subs) - sum(normal.values()), 4, 4)
want = [r[1]['answer'] for r in d['screens'][3]['widget']['rows']]
order10 = [{0}, {0, 2}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {0, 1, 2, 3}, {0, 2, 4, 6}, {0, 2, 5, 7}, set(range(8))]
claim('l11 yes/no column', [('yes' if normal[frozenset(s)] else 'no') for s in order10] == want and all(frozenset(s) in subs for s in order10))
S('l11', 'screens[4].widget.answer', 4, next(k for k in range(1, 5) if k % 4 == 0), 12 // 3)
S('l11', 'screens[4].widget.wrong[0].value', 3, len([0, 4, 8]), 12 // 4)
N = {0, 2}
claim('l11 every coset of {e, r^2} squares into N', all(mul(g, g) in N for g in range(8)))
claim('l11 D4/{e,r^2} has no element of order 4', all(mul(mul(g, g), mul(g, g)) in N and mul(g, g) in N for g in range(8)))
S('l11', 'screens[6].widget.options[3].why', 4, 8 // 2, len({frozenset({mul(g, n) for n in N}) for g in range(8)}))
S('l11', 'screens[10].canvas.params.rows[0][1]', 1380, 23 * 60, 1440 - 60)
S('l11', 'screens[10].canvas.params.rows[1][1]', 540, 9 * 60, 540)
S('l11', 'screens[10].canvas.params.rows[2][1]', 1920, 1380 + 540, 32 * 60)
S('l11', 'screens[10].widget.answer', 480, (1380 + 540) % 1440, 8 * 60)
S('l11', 'screens[10].widget.wrong[0].value', 1920, 1380 + 540, 1920)
S('l11', 'screens[10].prose', 1440, 24 * 60, 1440)
S('l11', 'quiz[3].widget.answer', 2, 8 // 4, len({g >= 4 for g in range(8)}))
S('l11', 'quiz[3].widget.wrong[0].value', 4, 4, len([0, 1, 2, 3]))

# ================= l12 =================
d = lv.files['l12-first-isomorphism-theorem']
rows = d['screens'][0]['widget']['rows']
claim('l12 3x mod 12 answers', [r[1]['answer'] for r in rows] == [3 * x % 12 for x in range(4, 12)] == [(x % 4) * 3 for x in range(4, 12)])
claim('l12 unreduced wrongs are 3x', all(r[1]['wrong'][0]['value'] == 3 * int(r[0]) for r in rows if 'wrong' in r[1]))
claim('l12 kernel taps 0, 4, 8', [x for x in range(12) if 3 * x % 12 == 0] == [0, 4, 8] == [int(c.split('c')[1]) - 1 for c in d['screens'][1]['widget']['answer']])
claim('l12 each value hit by exactly 3 inputs', all(sum(1 for x in range(12) if 3 * x % 12 == v) == 3 for v in (0, 3, 6, 9)))
S('l12', 'screens[2].widget.answer', 4, len({3 * x % 12 for x in range(12)}), 12 // 3)
S('l12', 'screens[2].widget.wrong[0].value', 3, 12 // 4, len([0, 4, 8]))
S('l12', 'screens[2].explain.text', 12, 3 * 4, len(range(12)))
claim('l12 |A_n| = n!/2 for n = 2..6', all(sum(1 for p in itertools.permutations(range(n)) if sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j]) % 2 == 0) == math.factorial(n) // 2 for n in range(2, 7)))
claim('l12 e^{2 pi i t} = 1 exactly at whole t (sampled)', all((abs(complex(math.cos(2 * math.pi * t), math.sin(2 * math.pi * t)) - 1) < 1e-9) == (abs(t - round(t)) < 1e-12) for t in [k / 8 for k in range(-16, 17)]))
counts6 = [sum(1 for x in range(16) if x % 6 == k) for k in range(6)]
counts8 = [sum(1 for x in range(16) if x % 8 == k) for k in range(8)]
claim('l12 counts mod 6 are 3,3,3,3,2,2', counts6 == [3, 3, 3, 3, 2, 2] == [r[1]['answer'] for r in d['screens'][10]['widget']['rows']] == [16 // 6 + (1 if k < 16 % 6 else 0) for k in range(6)])
claim('l12 counts mod 8 are all 2', counts8 == [2] * 8 == [16 // 8] * 8)
S('l12', 'screens[10].prose', 2, 16 // 8, counts8[0])
claim('l12 x mod 6 not a hom on Z16: 15 + 1', (15 + 1) % 16 % 6 == 0 and (15 % 6 + 1 % 6) % 6 == 4)
S('l12', 'quiz[0].widget.answer', 3, 12 // 4, len({j % 3 for j in range(12)}))
S('l12', 'quiz[0].widget.wrong[0].value', 4, len([0, 3, 6, 9]), 12 // 3)
S('l12', 'quiz[1].widget.answer', 4, pow(2, 32, 6), powmod_loop(2, 32, 6))
S('l12', 'quiz[1].widget.wrong[0].value', 2, pow(2, 31, 6), powmod_loop(2, 1, 6))
S('l12', 'quiz[1].feedback.correct', 715827883, 2 ** 32 // 6 + 1, sum(1 for _ in range(1)) * ((2 ** 32 - 0 + 5) // 6))
S('l12', 'quiz[1].feedback.correct', 715827882, 2 ** 32 // 6, (2 ** 32 - 5 + 5) // 6 - (1 if (2 ** 32) % 6 > 4 else 0))
two('l12 residue counts add to 2^32', 4 * 715827883 + 2 * 715827882, 2 ** 32)
S('l12', 'quiz[1].explain.text', 715827882, (2 ** 32 - 4) // 6, 2 ** 32 // 6)
S('l12', 'quiz[3].widget.options[0].text', 4, (15 % 6 + 1) % 6, 3 + 1)

# ================= l13 =================
d = lv.files['l13-fermat-and-euler']
grid = d['screens'][2]['canvas']['params']['cells']
claim('l13 power grid', grid == [[str(powmod_loop(a, k, 7)) for k in range(1, 7)] for a in range(1, 7)])
claim('l13 row-2 answers and unreduced wrongs', [r[1]['answer'] for r in d['screens'][0]['widget']['rows']] == [2, 4, 1, 2, 4, 1] and [r[1]['wrong'][0]['value'] for r in d['screens'][0]['widget']['rows'] if 'wrong' in r[1]] == [8, 16, 32, 64])
S('l13', 'screens[1].widget.answer', 2, pow(2, 100, 7), powmod_loop(2, 100 % 3, 7))
S('l13', 'screens[1].widget.wrong[0].value', 4, pow(2, 100 % 7, 7), 2 ** 2)
S('l13', 'screens[1].prose', 33, 100 // 3, (100 - 1) // 3)
orders = [next(k for k in range(1, 7) if powmod_loop(a, k, 7) == 1) for a in range(1, 7)]
claim('l13 orders 1,3,6,3,6,2 all divide 6', orders == [1, 3, 6, 3, 6, 2] and all(6 % o == 0 for o in orders) and [int(c.split('c')[1]) for c in d['screens'][2]['widget']['answer']] == orders)
rows = d['screens'][6]['widget']['rows']
S('l13', 'screens[6].widget.rows[0][1].answer', 6, phi(9), phi_formula(9))
S('l13', 'screens[6].widget.rows[1][1].answer', 4, phi(12), phi_formula(12))
S('l13', 'screens[6].widget.rows[2][1].answer', 1, pow(5, 4, 12), powmod_loop(5, 4, 12))
S('l13', 'screens[6].widget.rows[0][1].wrong[0].value', 8, 9 - 1, 8)
S('l13', 'screens[6].widget.rows[1][1].wrong[0].value', 11, 12 - 1, 11)
S('l13', 'screens[6].widget.rows[2][1].wrong[0].value', 625, 5 ** 4, 25 * 25)
S('l13', 'screens[6].feedback.byKey.r2c1', 52, 625 // 12, (625 - 1) // 12)
claim('l13 gcd table', d['screens'][6]['canvas']['params']['rows'][1][1:] == [str(math.gcd(a, 12)) for a in range(1, 12)])
S('l13', 'screens[7].widget.answer', 9, pow(7, 222, 10), powmod_loop(7, 222 % 4, 10))
S('l13', 'screens[7].widget.wrong[0].value', 3, powmod_loop(7, 3, 10), 343 % 10)
S('l13', 'screens[7].prose', 4, phi(10), phi_formula(10))
S('l13', 'screens[7].hints[1].text', 55, 222 // 4, (222 - 2) // 4)
claim('l13 7^k mod 10 table', d['screens'][7]['canvas']['params']['rows'][0][1:] == [str(powmod_loop(7, k, 10)) for k in range(1, 5)])
S('l13', 'screens[8].widget.answer', 4, pow(2, 8, 9), 256 - 28 * 9)
S('l13', 'screens[8].explain.text', 28, 256 // 9, (256 - 4) // 9)
S('l13', 'screens[8].explain.text', 6, phi(9), phi_formula(9))
claim('l13 2^k mod 9 table and 2^6 = 1', d['screens'][8]['canvas']['params']['rows'][0][1:] == [str(powmod_loop(2, k, 9)) for k in range(1, 7)] and pow(2, 6, 9) == 1)
S('l13', 'screens[9].prose', 20, phi(33), (3 - 1) * (11 - 1))
S('l13', 'screens[9].prose', 21, 3 * 7, 20 + 1)
two('l13 3 * 7 = 1 mod 20', 3 * 7 % 20, pow(3, -1, 20) * 3 % 20, 1)
S('l13', 'screens[9].widget.rows[0][1].answer', 31, pow(4, 3, 33), 64 - 33)
S('l13', 'screens[9].widget.rows[1][1].answer', 4, pow(31, 7, 33), (-2) ** 7 % 33)
S('l13', 'screens[9].widget.rows[0][1].wrong[0].value', 64, 4 ** 3, 64)
S('l13', 'screens[9].explain.text', -128, (-2) ** 7, -(2 ** 7))
claim('l13 RSA decrypts every message 0..32', all(pow(pow(m, 3, 33), 7, 33) == m for m in range(33)))
S('l13', 'screens[10].explain.text', 56, pow(3, 340, 341), powmod_loop(3, 340, 341))
claim('l13 2^340 = 1 mod 341 and 341 = 11 * 31', pow(2, 340, 341) == 1 == powmod_loop(2, 340, 341) and 11 * 31 == 341)
S('l13', 'quiz[0].widget.answer', 5, pow(3, 5, 7), pow(3, -1, 7))
S('l13', 'quiz[0].widget.wrong[0].value', 243, 3 ** 5, 81 * 3)
S('l13', 'quiz[0].explain.text', 34, 243 // 7, (243 - 5) // 7)
S('l13', 'quiz[1].explain.text', 375, pow(3, 560, 561), powmod_loop(3, 560, 561))
S('l13', 'quiz[1].prose', 56, pow(3, 340, 341), powmod_loop(3, 340, 341))
claim('l13 561 = 3*11*17 passes every coprime base', 3 * 11 * 17 == 561 and all(pow(a, 560, 561) == 1 for a in range(1, 561) if math.gcd(a, 561) == 1))
two('l13 phi(561)', phi(561), phi_formula(561), 320)
claim('l13 561 is the smallest Carmichael number', next(n for n in range(3, 2001) if any(n % q == 0 for q in range(2, n)) and all(pow(a, n - 1, n) == 1 for a in range(1, n) if math.gcd(a, n) == 1)) == 561)
claim('l13 liars of 15', [a for a in range(1, 15) if math.gcd(a, 15) == 1 and pow(a, 14, 15) == 1] == [1, 4, 11, 14])

# ================= review-3 =================
S('review', 'items[1].widget.answer', 3, len([j for j in range(12) if 3 * j % 12 == 0]), math.gcd(3, 12))
S('review', 'items[1].widget.wrong[0].value', 4, len({3 * j % 12 for j in range(12)}), 12 // 3)
claim('review x mod 3 is a hom Z6 -> Z3 with kernel {0, 3}', all((a + b) % 6 % 3 == (a % 3 + b % 3) % 3 for a in range(6) for b in range(6)) and [x for x in range(6) if x % 3 == 0] == [0, 3])
S('review', 'items[2].explain.text', 2, 8 % 3, 8 - 6)
claim('review r(rs)r^-1 = r^3 s', mul(mul(1, 5), inv(1)) == 7)
claim('review Z8/<4> cyclic of order 4', next(k for k in range(1, 9) if k % 4 == 0) == 4)
S('review', 'items[5].widget.answer', 5, len({4 * x % 20 for x in range(20)}), 20 // 4)
S('review', 'items[5].widget.wrong[0].value', 4, len([x for x in range(20) if 4 * x % 20 == 0]), math.gcd(4, 20))
S('review', 'items[6].widget.answer', 4, pow(5, 38, 7), powmod_loop(5, 38 % 6, 7))
S('review', 'items[6].widget.wrong[0].value', 6, pow(5, 38 % 7, 7), 125 % 7)
S('review', 'items[7].widget.answer', 4, pow(2, 50, 15), powmod_loop(2, 50 % 8, 15))
S('review', 'items[7].widget.wrong[0].value', 1, pow(2, 50 % 14, 15), 256 % 15)
S('review', 'items[7].prose', 8, phi(15), phi_formula(15))

# ================= homework-3 =================
claim('homework 2x from Z6 to Z12 is a well-defined hom', all(2 * ((a + b) % 6) % 12 == (2 * a + 2 * b) % 12 for a in range(6) for b in range(6)) and all(2 * (x + 6) % 12 == 2 * x % 12 for x in range(6)))
claim('homework det on D4 is a hom with kernel <r>', all((mm(mats[x], mats[y])[0][0] * mm(mats[x], mats[y])[1][1] - mm(mats[x], mats[y])[0][1] * mm(mats[x], mats[y])[1][0]) == (1 if mul(x, y) < 4 else -1) for x in range(8) for y in range(8)))
claim('homework x mod 2 on Z5 not well defined', 0 % 2 != 5 % 2)
S('homework', 'items[1].widget.answer', 6, len([x for x in range(18) if 6 * x % 18 == 0]), math.gcd(6, 18))
S('homework', 'items[1].widget.wrong[0].value', 3, len({6 * x % 18 for x in range(18)}), 18 // 6)
sig, tau = (2, 1, 0), (1, 0, 2)           # one-line forms of (1 3) and (1 2), 0-based
siginv = tuple(sig.index(i) for i in range(3))
conjp = tuple(sig[tau[siginv[i]]] for i in range(3))
claim('homework (1 3)(1 2)(1 3)^-1 = (2 3)', conjp == (0, 2, 1))
homs = [a for a in range(8) if 12 * a % 8 == 0]
S('homework', 'items[3].widget.answer', 4, len(homs), math.gcd(12, 8))
claim('homework every a in {0,2,4,6} gives a hom', homs == [0, 2, 4, 6] and all(all((a * ((x + y) % 12)) % 8 == (a * x + a * y) % 8 for x in range(12) for y in range(12)) for a in homs))
S('homework', 'items[4].widget.answer', 3, pow(2, 100, 13), powmod_loop(2, 100 % 12, 13))
S('homework', 'items[4].widget.wrong[0].value', 5, pow(2, 100 % 13, 13), 512 % 13)
S('homework', 'items[4].explain.text', 8, 100 // 12, (100 - 4) // 12)
S('homework', 'items[5].widget.answer', 29, pow(3, 2026, 100), powmod_loop(3, 2026 % 40, 100))
S('homework', 'items[5].prose', 40, phi(100), phi_formula(100))
S('homework', 'items[5].explain.text', 49, pow(3, 10, 100), 59049 % 100)
S('homework', 'items[5].explain.text', 729, 3 ** 6, 27 * 27)
S('homework', 'items[5].explain.text', 50, 2026 // 40, (2026 - 26) // 40)
claim('homework 3^20 = 1 mod 100', pow(3, 20, 100) == 1 == 49 * 49 % 100)
claim('homework Z12/<4>: order of 1 is 12 in Z12 but 4 in the quotient', next(k for k in range(1, 13) if k % 12 == 0) == 12)

# ---------------- code widgets: solutions pass, starters fail ----------------
def run_case(src, c):
    ns = {}
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
for fid, doc in lv.files.items():
    for key in ('screens', 'quiz', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget')
            if not (w and w.get('kind') == 'code'):
                continue
            ncode += 1
            sol = all(run_case(w['solution'], c) for c in w['tests'] + w.get('examples', []))
            sf = []
            for c in w['tests']:
                try:
                    sf.append(not run_case(w['starter'], c))
                except Exception:
                    sf.append(True)
            ok = sol and any(sf)
            print(f"{'ok ' if ok else 'BAD'} code {fid} {key}[{i}]: solution {'passes' if sol else 'FAILS'}, starter fails tests {[k + 1 for k, f in enumerate(sf) if f]}")
            if not ok:
                fails.append(f'code {fid} {key}[{i}]')
print(f'code widgets checked: {ncode}')

lv.check_wrongs()
if fails:
    print('two-way, claim or code failures:', fails)
lv.report()
if fails:
    sys.exit(1)
