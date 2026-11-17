"""Recompute every number in app/content/courses/algebra/problems-1.json to problems-3.json twice.

Method 1 works by a rule (Euler's phi, gcd and lcm, the order formula n/gcd(k, n), Lagrange, the first
isomorphism theorem, Euclid's back-substitution). Method 2 is a brute enumeration over the group itself (every
element of Z_n, D_8, D_6, S_5 or S_10 as needed, composed right to left). For each numeric part the script checks
that the two methods agree, that the JSON key equals the value, that every `wrong` value equals its named slip
recomputed here, has a byKey line and differs from the key. Numeric sets check the set and each slip set. Choice
parts check the keyed option and verify each option's claim where it is a fact about the group. Figures stated in
feedback and explain are checked as text (numbers_lib.Level.expect), and numbers_lib.Level.check_wrongs runs over
each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-algebra-numbers.py
"""
import json, os, sys
from math import gcd, factorial, lcm
from itertools import permutations
from sympy import totient

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'algebra')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(lv):
    d = json.load(open(os.path.join(COURSE, f'problems-{lv}.json')))
    return d, {it['id']: it for it in d['items']}


SETS = {lv: load(lv) for lv in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{lv}.json'))}


def part(lv, iid, p):
    return SETS[lv][1][iid]['parts'][p - 1]


def num(lv, iid, p, rule, brute, slips):
    if lv not in SETS:
        return
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w['kind'] == 'numeric' and 'answer' in w, f'{tag} numeric')
    ok(rule == brute, f'{tag} methods agree {rule} vs {brute}')
    ok(w['answer'] == rule, f'{tag} key {w["answer"]} == {rule}')
    ok(w['tol'] == {'abs': 0}, f'{tag} integer band')
    got = {x['id']: x['value'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag} slip ids {sorted(got)} vs {sorted(slips)}')
    by = pt['feedback'].get('byKey', {})
    for k, v in slips.items():
        ok(got.get(k) == v, f'{tag} slip {k} {got.get(k)} == {v}')
        ok(v != rule, f'{tag} slip {k} differs from key')
        ok(k in by, f'{tag} slip {k} has byKey')
    ok(len(set(got.values())) == len(got), f'{tag} slips distinct')


def numset(lv, iid, p, rule, brute, slips):
    if lv not in SETS:
        return
    pt = part(lv, iid, p)
    w, tag = pt['widget'], f'L{lv} {iid} p{p}'
    ok(w.get('unordered') is True, f'{tag} unordered')
    ok(sorted(rule) == sorted(brute) == sorted(w['answers']), f'{tag} set {w["answers"]} vs {rule} {brute}')
    got = {x['id']: sorted(int(t) for t in x['value'].split(',')) for x in w.get('wrong', [])}
    by = pt['feedback'].get('byKey', {})
    ok('count' in by, f'{tag} count line')
    for k, v in slips.items():
        ok(got.get(k) == sorted(v), f'{tag} slip {k} {got.get(k)} == {sorted(v)}')
        ok(sorted(v) != sorted(rule) and len(v) == len(rule), f'{tag} slip {k} wrong set, right count')
        ok(k in by, f'{tag} slip {k} has byKey')


def key(lv, iid, p, cid):
    if lv not in SETS:
        return
    opts = part(lv, iid, p)['widget']['options']
    ok([o['id'] for o in opts if o.get('correct')] == [cid], f'L{lv} {iid} p{p} key {cid}')
    ok(all(o.get('correct') or o.get('why') for o in opts), f'L{lv} {iid} p{p} every distractor has why')


def units(n):
    return [a for a in range(1, n) if gcd(a, n) == 1]


def mord(a, n):
    k, x = 1, a % n
    while x != 1:
        x, k = x * a % n, k + 1
    return k


def aord(a, n):
    k = 1
    while a * k % n:
        k += 1
    return k


def dihedral(n):
    """Elements (k, f) = r^k s^f with s r = r^-1 s, products right to left."""
    G = [(k, f) for k in range(n) for f in range(2)]

    def mul(a, b):
        (k1, f1), (k2, f2) = a, b
        return ((k1 + k2) % n, f2) if f1 == 0 else ((k1 - k2) % n, (f1 + f2) % 2)
    return G, mul


def gorder(x, mul, e):
    y, m = x, 1
    while y != e:
        y, m = mul(y, x), m + 1
    return m


# ============================================================ level 1
# p-probe-stride: Z_56
num(1, 'p-probe-stride', 1, 56 // gcd(21, 56), len({21 * k % 56 for k in range(56)}),
    {'gcd': gcd(21, 56), 'full': 56})
num(1, 'p-probe-stride', 2, int(totient(56)), sum(1 for s in range(1, 56) if len({s * k % 56 for k in range(56)}) == 56),
    {'no-overlap': 56 - 28 - 8, 'odd-only': 28, 'all': 55})
ok(sum(1 for s in range(56) if s % 2 and s % 7 == 0) == 4, 'L1 odd multiples of 7 below 56: 4')
# Euclid: 56 = 6*9 + 2, 9 = 4*2 + 1, 1 = 25*9 - 4*56
ok(56 == 6 * 9 + 2 and 9 == 4 * 2 + 1 and 25 * 9 - 4 * 56 == 1 and 225 == 4 * 56 + 1, 'L1 Euclid lines for 9 mod 56')
num(1, 'p-probe-stride', 3, pow(9, -1, 56), next(k for k in range(1, 56) if 9 * k % 56 == 1),
    {'dropped-nine': 24, 'sign': (-25) % 56})
ok(24 * 9 % 56 == 48, 'L1 24*9 = 216 = 48 mod 56')
num(1, 'p-probe-stride', 4, 13 * 25 % 56, next(k for k in range(1, 56) if 9 * k % 56 == 13),
    {'times-stride': 13 * 9 % 56, 'from-24': 13 * 24 % 56, 'from-31': 13 * 31 % 56})
ok(13 * 25 == 325 == 5 * 56 + 45 and 9 * 45 == 405 == 7 * 56 + 13, 'L1 325 and 405 identities')

# p-octagon-orders: D_8 (16 elements)
G8, m8 = dihedral(8)
e8 = (0, 0)
prod = m8((3, 1), (5, 1))
ok(prod[1] == 0, 'L1 octagon product is a turn')
num(1, 'p-octagon-orders', 1, (3 - 5) % 8, prod[0], {'added': (3 + 5) % 8, 'reversed': 5 - 3})
num(1, 'p-octagon-orders', 2, 8 // gcd(6, 8), gorder((6, 0), m8, e8), {'all-eight': 8, 'half-turn': 2})
ok(m8((6, 0), (6, 0)) == (4, 0), 'L1 r^12 = r^4')
inv = [y for y in G8 if m8(prod, y) == e8][0]
num(1, 'p-octagon-orders', 3, (5 - 3) % 8, inv[0], {'self-inverse': 6, 'commuted': (5 + 3) % 8})
ok(m8((5, 1), (3, 1)) == (2, 0), 'L1 (r^5 s)(r^3 s) = r^2')
x4 = sum(1 for x in G8 if m8(m8(x, x), m8(x, x)) == e8)
x2 = sum(1 for x in G8 if m8(x, x) == e8)
num(1, 'p-octagon-orders', 4, 8 + len([k for k in range(8) if 4 * k % 8 == 0]), x4,
    {'squares': x2, 'turns-only': 4, 'flips-only': 8})
ok([gorder((k, 0), m8, e8) for k in (0, 2, 4, 6)] == [1, 4, 2, 4], 'L1 orders of e, r^2, r^4, r^6')

# p-shifted-product: a * b = a + b + ab mod 19
st = lambda a, b: (a + b + a * b) % 19  # noqa: E731
ok(all(st(18, b) == 18 for b in range(19)), 'L1 18 absorbs')
ok(all(st(a, b) != 18 for a in range(18) for b in range(18)), 'L1 G = 0..17 closed')
ok(all(st(st(a, b), c) == st(a, st(b, c)) for a in range(19) for b in range(19) for c in range(19)), 'L1 star associative')
num(1, 'p-shifted-product', 1, (19 * 5 + 18 - 19 * 5) % 19 if False else (18 + 19 * 5) % 19, st(18, 5),
    {'product': 18 * 5 % 19, 'sum': (18 + 5) % 19})
ok(18 + 5 + 90 == 113 == 5 * 19 + 18, 'L1 113 = 5*19 + 18')
num(1, 'p-shifted-product', 2, (pow(5, -1, 19) * 15) % 19, next(b for b in range(18) if st(4, b) == 0),
    {'plain-inverse': pow(4, -1, 19), 'negative': (-4) % 19})
ok(st(4, 15) == 3 and 4 + 15 + 60 == 79, 'L1 4*15 = 79 = 3')


def star_order(a):
    x, m = a, 1
    while x != 0:
        x, m = st(x, a), m + 1
    return m


num(1, 'p-shifted-product', 3, mord(2, 19), star_order(1), {'half': 9, 'sixth': 6, 'modulus': 19})
ok(pow(2, 6, 19) == 7 and pow(2, 9, 19) == 18 and (pow(2, 9, 19) - 1) == 17, 'L1 2^6 = 7, 2^9 = 18, element 17')
num(1, 'p-shifted-product', 4, int(totient(18)), sum(1 for a in range(18) if star_order(a) == 18),
    {'non-identity': 17, 'phi-modulus': int(totient(19)), 'odd': 9})
ok(star_order(st(1, 1)) == 9 and st(1, 1) == 3, 'L1 1*1 = 3 has order 9')
ok(18 // gcd(3, 18) == 6 and 18 // gcd(9, 18) == 2, 'L1 orders of the 3rd and 9th powers')
ok([k for k in range(1, 18) if gcd(k, 18) == 1] == [1, 5, 7, 11, 13, 17], 'L1 exponents coprime to 18')

# ============================================================ level 2
# p-desk-rota: sigma in S_10
row = [7, 9, 10, 6, 8, 2, 3, 1, 4, 5]
sig = {k + 1: v for k, v in enumerate(row)}


def cycles(s):
    seen, cs = set(), []
    for i in sorted(s):
        if i in seen:
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = s[j]
        cs.append(c)
    return cs


cs = cycles(sig)
ok(cs == [[1, 7, 3, 10, 5, 8], [2, 9, 4, 6]], f'L2 cycle form {cs}')
k, x = 1, sig[1]
while x != 1:
    x, k = sig[x], k + 1
num(2, 'p-desk-rota', 1, len(cs[0]), k, {'other-cycle': 4, 'all-desks': 10})
pw, m = dict(sig), 1
while any(pw[i] != i for i in pw):
    pw, m = {i: sig[pw[i]] for i in pw}, m + 1
num(2, 'p-desk-rota', 2, lcm(6, 4), m, {'product': 24, 'sum': 10})
inversions = sum(1 for i in range(1, 11) for j in range(i + 1, 11) if sig[i] > sig[j])
ok((5 + 3) % 2 == 0 and inversions % 2 == 0 and (10 - len(cs)) == 8, f'L2 sigma even ({inversions} inversions)')
key(2, 'p-desk-rota', 3, 'a')
num(2, 'p-desk-rota', 4, factorial(10) // 2 // lcm(6, 4), (factorial(10) // 2) // m,
    {'in-s10': factorial(10) // 12, 'product-order': factorial(10) // 2 // 24})
ok(factorial(10) // 2 == 1814400, 'L2 |A_10| = 1,814,400')

# p-units-21-cosets
U21 = units(21)
num(2, 'p-units-21-cosets', 1, int(totient(21)), len(U21), {'no-sevens': 20 - 6, 'no-threes': 20 - 2, 'all': 20})
H = [1, 4, 16]
ok(all(a * pow(b, -1, 21) % 21 in H for a in H for b in H), 'L2 H passes the one-step test')
num(2, 'p-units-21-cosets', 2, 4 * 4 % 21, 4 * pow(16, -1, 21) % 21, {'no-inverse': 4 * 16 % 21, 'inverse-only': pow(16, -1, 21)})
cos = {frozenset(g * h % 21 for h in H) for g in U21}
num(2, 'p-units-21-cosets', 3, 12 // 3, len(cos), {'subtracted': 9, 'size': 3})
numset(2, 'p-units-21-cosets', 4, [2 * h % 21 for h in H], sorted(next(c for c in cos if 2 in c)),
       {'added': [h + 2 for h in H]})
key(2, 'p-units-21-cosets', 5, 'a')


def is_subgroup(S):
    return 1 in S and all(a * b % 21 in S for a in S for b in S)


A = set(H) | {2, 8, 11}
ok(is_subgroup(A) and A == {pow(2, k, 21) for k in range(6)} and len(A) == 6, 'L2 H u 2H = <2>, 6 elements')
ok(not is_subgroup({2, 5, 8, 11, 17, 20}) and {5 * h % 21 for h in H} == {5, 17, 20}, 'L2 2H u 5H not a subgroup')
ok(not is_subgroup(set(H) | {2, 5, 10}) and 2 * 10 % 21 == 20, 'L2 H u {2,5,10} not closed')
ok(not is_subgroup({2, 8, 11}), 'L2 2H not a subgroup')

# p-fixing-five: S_5
S5 = [dict(zip(range(1, 6), p)) for p in permutations(range(1, 6))]
comp = lambda a, b: {i: a[b[i]] for i in range(1, 6)}  # noqa: E731
tup = lambda t: tuple(t[i] for i in range(1, 6))  # noqa: E731
HS = [t for t in S5 if t[5] == 5]
ok(all(comp(a, {v: k for k, v in b.items()})[5] == 5 for a in HS for b in HS), 'L2 one-step test on H')
key(2, 'p-fixing-five', 1, 'a')
t12, t23 = {1: 2, 2: 1, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 3, 3: 2, 4: 4, 5: 5}
ok(tup(comp(t12, t23)) != tup(comp(t23, t12)), 'L2 (1 2) and (2 3) do not commute')
ok(tup(comp(t12, t23)) not in {tup({i: i for i in range(1, 6)}), tup(t12), tup(t23)}, 'L2 {e,(12),(23)} not closed')
lcos = {frozenset(tup(comp(g, h)) for h in HS) for g in S5}
num(2, 'p-fixing-five', 2, factorial(5) // factorial(4), len(lcos), {'size': 24, 'subtracted': 96})
sg = {1: 5, 5: 3, 3: 1, 2: 4, 4: 2}
L = [comp(sg, h) for h in HS]
R = [comp(h, sg) for h in HS]
ok(len({t[5] for t in L}) == 1, 'L2 sigma H sends 5 to one point')
num(2, 'p-fixing-five', 3, sg[5], L[0][5], {'inverse': 1, 'fixed': 5})
ok({v: k for k, v in sg.items()}[5] == 1, 'L2 sigma^-1(5) = 1')
pts = {i for t in R for i in t if t[i] == 5}
ok(len(pts) == 1, 'L2 H sigma sends one point to 5')
num(2, 'p-fixing-five', 4, {v: k for k, v in sg.items()}[5], pts.pop(), {'left-coset': 3, 'five': 5})
ok(all(t[5] != 5 for t in R), 'L2 no element of H sigma fixes 5')
both = {tup(t) for t in L} & {tup(t) for t in R}
num(2, 'p-fixing-five', 5, factorial(3), len(both), {'disjoint': 0, 'equal': 24, 'half': 12})
t35 = {1: 1, 2: 2, 3: 5, 4: 4, 5: 3}
ok(tup(t35) in {tup(t) for t in L} and tup(t35) not in {tup(t) for t in R}, 'L2 (3 5) in sigma H, not in H sigma')

# ============================================================ level 3
# p-fifteen-times: Z_24 -> Z_36
phi = lambda x: 15 * x % 36  # noqa: E731
ok(15 * 24 % 36 == 0 and 15 * 24 == 360 == 10 * 36, 'L3 well defined')
ok(all(phi((a + b) % 24) == (phi(a) + phi(b)) % 36 for a in range(24) for b in range(24)), 'L3 homomorphism')
ker = [x for x in range(24) if phi(x) == 0]
num(3, 'p-fifteen-times', 1, 24 // 12, len(ker), {'in-z36': len([x for x in range(36) if 15 * x % 36 == 0]), 'one': 1})
im = {phi(x) for x in range(24)}
num(3, 'p-fifteen-times', 2, 24 // len(ker), len(im), {'target': 36 // 2, 'from-three': 24 // 3})
ok(im == set(range(0, 36, 3)), 'L3 image is the multiples of 3')
numset(3, 'p-fifteen-times', 3, [(35 % 12), (35 % 12) + 12], [x for x in range(24) if phi(x) == 21],
       {'no-inverse': [7, 19]})
ok(pow(5, -1, 12) == 5 and 15 * 11 == 165 == 4 * 36 + 21, 'L3 5^-1 = 5 mod 12; 165 = 4*36 + 21')
kk = next(k for k in range(1, 25) if 2 * k % 24 in ker)
num(3, 'p-fifteen-times', 4, 36 // gcd(phi(2), 36), kk, {'in-z24': aord(2, 24), 'in-target': aord(2, 36)})
ok(phi(2) == 30, 'L3 phi(2) = 30')

# p-powers-of-seven
num(3, 'p-powers-of-seven', 1, int(totient(45)), len(units(45)), {'no-fives': 30, 'no-threes': 36, 'all': 44})
ok(45 - 15 - 9 + 3 == 24 and 45 * 2 // 3 == 30 and 45 * 4 // 5 == 36, 'L3 inclusion-exclusion for 45')
ok(pow(7, 2, 45) == 4 and pow(7, 3, 45) == 28, 'L3 prose powers')
pw7 = {k: pow(7, k, 45) for k in range(13)}
ok((pw7[4], pw7[6], pw7[8], pw7[12]) == (16, 19, 31, 1) and 28 ** 2 == 784 and 19 ** 2 == 361, 'L3 powers 4, 6, 8, 12')
num(3, 'p-powers-of-seven', 2, min(d for d in (1, 2, 3, 4, 6, 8, 12, 24) if pow(7, d, 45) == 1), mord(7, 45),
    {'euler': 24, 'six': 6})
ok(pw7[6] != 1, 'L3 7^6 is not 1')
num(3, 'p-powers-of-seven', 3, (pw7[8] * pw7[3]) % 45, pow(7, 2027, 45), {'used-44': pow(7, 2027 % 44, 45), 'added': (pw7[8] + pw7[3]) % 45})
ok(2027 == 12 * 168 + 11 and 2027 % 44 == 3 and 31 * 28 == 868 == 19 * 45 + 13, 'L3 2027 and 868 identities')
num(3, 'p-powers-of-seven', 4, 13 * 20 % 45, next(x for x in range(45) if 7 * x % 45 == 20),
    {'times-seven': 7 * 20 % 45, 'from-28': 28 * 20 % 45})
ok(7 * 13 == 91 and 91 % 45 == 1 and 260 == 5 * 45 + 35 and 245 == 5 * 45 + 20 and 7 * 28 % 45 == 16, 'L3 inverse and checks')

# p-hexagon-quotient: D_6
G6, m6 = dihedral(6)
e6 = (0, 0)
num(3, 'p-hexagon-quotient', 1, 12 // 6, 12 // 6, {'image-size': 6, 'product': 72})
order2 = [z for z in G6 if z != e6 and m6(z, z) == e6]
normal2 = [z for z in order2 if all(m6(m6(g, z), [y for y in G6 if m6(g, y) == e6][0]) == z for g in G6)]
ok(normal2 == [(3, 0)], f'L3 the only normal subgroup of order 2 is <r^3> ({normal2})')
conj = m6(m6((0, 1), (3, 0)), (0, 1))
num(3, 'p-hexagon-quotient', 2, (-3) % 6, conj[0], {'negative': -3, 'identity': 0})
ok(all(m6(m6((1, 0), (j, 1)), (5, 0)) == ((j + 2) % 6, 1) for j in range(6)), 'L3 r (r^j s) r^-1 = r^(j+2) s')
N = [e6, (3, 0)]
Nset = frozenset(N)
coset = lambda g: frozenset(m6(g, x) for x in N)  # noqa: E731
cosets = {coset(g) for g in G6}


def cord(A):
    g0 = next(iter(A))
    g, mm = g0, 1
    while coset(g) != Nset:
        g, mm = m6(g, g0), mm + 1
    return mm


num(3, 'p-hexagon-quotient', 3, next(k for k in range(1, 7) if (k % 6, 0) in N), cord(coset((1, 0))), {'order-of-r': 6, 'two': 2})
ords = sorted(cord(A) for A in cosets)
ok(ords == [1, 2, 2, 2, 3, 3], f'L3 coset orders {ords}')
num(3, 'p-hexagon-quotient', 4, 6 // 2, ords.count(2), {'cyclic': 1, 'flips': 6, 'all-but-e': 5})

# ============================================================ set shape
LESSONS = {1: {'p-probe-stride': ['l3', 'l4'], 'p-octagon-orders': ['l1', 'l2', 'l4'], 'p-shifted-product': ['l2', 'l3', 'l4']},
           2: {'p-desk-rota': ['l7', 'l8', 'l9'], 'p-units-21-cosets': ['l5', 'l6', 'l7'], 'p-fixing-five': ['l5', 'l6', 'l7', 'l8']},
           3: {'p-fifteen-times': ['l10', 'l11', 'l12'], 'p-powers-of-seven': ['l10', 'l12', 'l13'], 'p-hexagon-quotient': ['l10', 'l11', 'l12']}}
LEVEL_LESSONS = {1: {'l1', 'l2', 'l3', 'l4'}, 2: {'l5', 'l6', 'l7', 'l8', 'l9'}, 3: {'l10', 'l11', 'l12', 'l13'}}
SKILLS = {1: {'ag-groups'}, 2: {'ag-cosets', 'ag-perm'}, 3: {'ag-hom', 'ag-cosets', 'ag-groups'}}
for lv, (d, items) in SETS.items():
    ok(3 <= len(d['items']) <= 5, f'L{lv} 3 to 5 problems')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'L{lv} has a difficulty 5')
    parts = [p for it in d['items'] for p in it['parts']]
    typed = sum(1 for p in parts if p['widget']['kind'] in ('numeric', 'expression'))
    ok(3 * typed >= 2 * len(parts), f'L{lv} typed share {typed}/{len(parts)}')
    ok(set().union(*LESSONS[lv].values()) == LEVEL_LESSONS[lv], f'L{lv} every lesson drawn on')
    ok(all(len(v) >= 2 for v in LESSONS[lv].values()), f'L{lv} each problem draws on two lessons')
    for it in d['items']:
        ok(3 <= it['difficulty'] <= 5 and 3 <= len(it['parts']) <= 5, f'L{lv} {it["id"]} difficulty and part count')
        ok(set(it['skills']) <= SKILLS[lv], f'L{lv} {it["id"]} skills from the level')

# ============================================================ stated figures (numbers_lib)
for lv in SETS:
    lv_obj = Level('algebra', lv)
    lv_obj.check_wrongs('problems')
    P = lambda i, p, f: f'items[{i}].parts[{p}].{f}'  # noqa: E731
    if lv == 1:
        lv_obj.expect('problems', P(0, 0, 'feedback.correct'), 8)
        lv_obj.expect('problems', P(0, 1, 'feedback.correct'), 24)
        lv_obj.expect('problems', P(0, 2, 'feedback.correct'), 25)
        lv_obj.expect('problems', P(0, 3, 'feedback.correct'), 45)
        lv_obj.expect('problems', P(1, 0, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(1, 1, 'feedback.correct'), 4)
        lv_obj.expect('problems', P(1, 2, 'feedback.correct'), 2)
        lv_obj.expect('problems', P(1, 3, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(2, 0, 'feedback.correct'), 113)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 18)
        lv_obj.expect('problems', P(2, 3, 'feedback.correct'), 6)
    if lv == 2:
        lv_obj.expect('problems', P(0, 0, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(0, 1, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(0, 3, 'feedback.correct'), 151200)
        lv_obj.expect('problems', P(1, 0, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(1, 1, 'feedback.correct'), 16)
        lv_obj.expect('problems', P(1, 2, 'feedback.correct'), 4)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 5)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 4, 'feedback.correct'), 6)
    if lv == 3:
        lv_obj.expect('problems', P(0, 0, 'feedback.correct'), 2)
        lv_obj.expect('problems', P(0, 1, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(0, 2, 'feedback.correct'), 23)
        lv_obj.expect('problems', P(0, 3, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(1, 0, 'feedback.correct'), 24)
        lv_obj.expect('problems', P(1, 1, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(1, 2, 'feedback.correct'), 13)
        lv_obj.expect('problems', P(1, 3, 'feedback.correct'), 35)
        lv_obj.expect('problems', P(2, 0, 'feedback.correct'), 2)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 3, 'feedback.correct'), 3)
    rc = lv_obj.report()
    ok(rc in (0, None), f'L{lv} numbers_lib report')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
