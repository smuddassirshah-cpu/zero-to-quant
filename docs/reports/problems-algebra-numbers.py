"""Recompute every number in app/content/courses/algebra/problems-1.json to problems-3.json twice.

Method 1 works by a rule (Euler's phi, gcd and lcm, the order formula n/gcd(k, n), Lagrange, the first
isomorphism theorem, Euclid's back-substitution). Method 2 is a brute enumeration over the group itself (every
element of Z_n, D_8, S_5, S_8, Z_133^x, the 2 by 2 matrices modulo 7 or the 20 maps ax + b on Z_5 as needed,
composed right to left; the re-authored problems of session AF are p-pixel-scrambler, p-server-moves, p-units-133, p-affine-five). For each numeric part the script checks
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

# p-pixel-scrambler: M = [[1, 2], [1, 3]] on (Z_7)^2
def mm(X, Y, n=7):
    return tuple(tuple(sum(X[i][k] * Y[k][j] for k in range(2)) % n for j in range(2)) for i in range(2))


def mv(X, v, n=7):
    return tuple(sum(X[i][k] * v[k] for k in range(2)) % n for i in range(2))


def mpow(X, k):
    R = ((1, 0), (0, 1))
    for _ in range(k):
        R = mm(R, X)
    return R


BIG = 10 ** 9
MM, I2 = ((1, 2), (1, 3)), ((1, 0), (0, 1))
ok(MM[0][0] * MM[1][1] - MM[0][1] * MM[1][0] == 1, 'L1 det M = 1')
M2 = mm(MM, MM, BIG)
ok(M2 == ((3, 8), (4, 11)), 'L1 M^2 over Z')
ok(mm(M2, M2, BIG) == ((41, 112), (56, 153)), 'L1 M^4 over Z: 41, 112, 56, 153')
M4 = mpow(MM, 4)
ok(M4 == ((6, 0), (0, 6)), 'L1 M^4 = 6I = -I mod 7')
num(1, 'p-pixel-scrambler', 1, (3 * 3 + 8 * 4) % 7, M4[0][0],
    {'entrywise': (1 ** 4) % 7, 'dropped-term': (3 * 3) % 7})
ordM = next(k for k in range(1, 100) if mpow(MM, k) == I2)
num(1, 'p-pixel-scrambler', 2, 8 if mpow(MM, 8) == I2 and mpow(MM, 4) != I2 else -1, ordM, {'minus-one': 4, 'modulus': 7})
ok(mm(MM, M2, BIG) == ((11, 30), (15, 41)), 'L1 M^3 over Z: 11, 30, 15, 41')
M3 = mpow(MM, 3)
ok(M3 == ((4, 2), (1, 6)) and mpow(MM, 7) == tuple(tuple(-x % 7 for x in r) for r in M3), 'L1 M^7 = -M^3 mod 7')
ok(mpow(MM, 7) != I2 and mpow(MM, 2) != I2, 'L1 M^7 and M^2 are not I')
Minv = mpow(MM, 7)
ok(Minv == ((3, 5), (6, 1)) and mm(Minv, MM) == I2, 'L1 M^-1 = [[3, 5], [6, 1]]')
adj = ((MM[1][1] % 7, -MM[0][1] % 7), (-MM[1][0] % 7, MM[0][0] % 7))
ok(adj == Minv, 'L1 adjugate agrees with M^7')
num(1, 'p-pixel-scrambler', 3, adj[0][0], Minv[0][0], {'no-minus': M3[0][0], 'forward': MM[0][0]})
pre = [v for v in [(x, y) for x in range(7) for y in range(7)] if mv(MM, v) == (3, 1)]
ok(pre == [(0, 5)] and mv(Minv, (3, 1)) == (0, 5), 'L1 the pixel sent to (3, 1) is (0, 5)')
ok((9 + 5, 18 + 1) == (14, 19) and (0 + 2 * 5, 0 + 3 * 5) == (10, 15), 'L1 part 4 printed sums')
num(1, 'p-pixel-scrambler', 4, mv(Minv, (3, 1))[1], pre[0][1],
    {'forward': mv(MM, (3, 1))[1], 'no-minus': mv(M3, (3, 1))[1]})
ok(mv(MM, (3, 1)) == (5, 6) and mv(M3, (3, 1)) == (0, 2) and mv(MM, (0, 2)) == (4, 6), 'L1 part 4 slip pixels')

# ============================================================ level 2
# p-server-moves: S_8, xi sigma = tau
def cyc(n, cs):
    p = {i: i for i in range(1, n + 1)}
    for c in cs:
        for i, a in enumerate(c):
            p[a] = c[(i + 1) % len(c)]
    return p


def cycles(s):
    seen, out = set(), []
    for i in sorted(s):
        if i in seen or s[i] == i:
            seen.add(i)
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = s[j]
        out.append(c)
    return out


def sgn_inv(s):
    k = sorted(s)
    return (-1) ** sum(1 for a in range(len(k)) for b in range(a + 1, len(k)) if s[k[a]] > s[k[b]])


c8 = lambda a, b: {i: a[b[i]] for i in range(1, 9)}  # noqa: E731
i8 = lambda a: {v: k for k, v in a.items()}  # noqa: E731
sig = cyc(8, [(1, 2, 3, 4, 5, 6)])
tau = cyc(8, [(1, 3, 5, 7), (2, 8)])
xi = c8(tau, i8(sig))
ok(c8(xi, sig) == tau, 'L2 xi sigma = tau')
sols = [p for p in permutations(range(1, 9)) if c8(dict(zip(range(1, 9), p)), sig) == tau]
ok(len(sols) == 1 and dict(zip(range(1, 9), sols[0])) == xi, 'L2 xi is the unique solution (all of S_8)')
ok(cycles(xi) == [[1, 6, 7], [2, 3, 8], [4, 5]], f'L2 xi cycle form {cycles(xi)}')
ok(sgn_inv(sig) == -1 and sgn_inv(tau) == 1 and sgn_inv(xi) == -1, 'L2 signs by inversions: sigma odd, tau even, xi odd')
ok((-1) ** 5 == sgn_inv(sig) and (-1) ** (3 + 1) == sgn_inv(tau), 'L2 transposition counts 5 and 3 + 1')
key(2, 'p-server-moves', 1, 'a')
ok(sgn_inv(xi) * sgn_inv(sig) == sgn_inv(tau), 'L2 sign of a product')
num(2, 'p-server-moves', 2, tau[i8(sig)[1]], xi[1], {'no-inverse': c8(tau, sig)[1], 'wrong-side': c8(i8(sig), tau)[1]})
ok(i8(sig)[1] == 6 and tau[6] == 6 and tau[2] == 8 and i8(sig)[3] == 2, 'L2 part 2 printed images')
pw = [xi]
while pw[-1] != cyc(8, []):
    pw.append(c8(pw[-1], xi))
num(2, 'p-server-moves', 3, lcm(3, 3, 2), len(pw), {'product': 3 * 3 * 2, 'sum': 3 + 3 + 2, 'longest': 3})
x3 = pw[2]
ok(x3[4] == 5 and x3[5] == 4 and all(x3[i] == i for i in (1, 2, 3, 6, 7, 8)), 'L2 xi^3 is the swap (4 5)')
evens = [k + 1 for k, p in enumerate(pw) if sgn_inv(p) == 1]
num(2, 'p-server-moves', 4, sum(1 for k in range(1, 7) if (-1) ** k == 1), len(evens), {'same-sign': 0, 'missed-identity': 2})
ok(evens == [2, 4, 6], 'L2 even powers are xi^2, xi^4, xi^6')
ok(c8(pw[1], pw[1]) == pw[3] and c8(pw[3], pw[1]) == pw[5], 'L2 <xi^2> = {xi^2, xi^4, e}')

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
# p-units-133: rho(x) = x mod 19 on Z_133^x
U133 = units(133)
ok(len(U133) == int(totient(133)) == 6 * 18 == 108, 'L3 |Z_133^x| = 108')
ok(all((a * b % 133) % 19 == (a % 19) * (b % 19) % 19 for a in U133 for b in U133), 'L3 rho is a homomorphism')
K19 = [x for x in U133 if x % 19 == 1]
cand = [1 + 19 * j for j in range(7)]
num(3, 'p-units-133', 1, len([c for c in cand if gcd(c, 133) == 1]), len(K19), {'kept-77': len(cand), 'trivial': 1})
ok(K19 == [1, 20, 39, 58, 96, 115] and cand == [1, 20, 39, 58, 77, 96, 115] and 77 == 7 * 11, 'L3 kernel listed')
ok({x % 19 for x in U133} == set(range(1, 19)) and 108 // 6 == 18, 'L3 rho onto, 18 cosets')
roots19 = [y for y in range(1, 19) if pow(y, 3, 19) == 1]
ok(roots19 == [1, 7, 11] and 7 ** 3 == 343 == 18 * 19 + 1 and 49 % 19 == 11, 'L3 cube roots of 1 mod 19')
L = [x for x in U133 if pow(x, 3, 19) == 1]
ord3 = [y for y in range(1, 19) if y != 1 and pow(y, 3, 19) == 1]
M3 = [x for x in U133 if x % 19 != 1 and pow(x, 3, 19) == 1]
num(3, 'p-units-133', 2, len(ord3) * len(K19), len(M3), {'roots-only': len(ord3), 'with-kernel': len(L), 'one-coset': 6, 'seven-each': len(ord3) * 7})
ok(ord3 == [7, 11] and len(M3) + len(K19) == len(L) == 18, 'L3 order-3 residues 7, 11; 12 + 6 = 18')
ok(all(sum(1 for x in U133 if x % 19 == y) == 6 for y in range(1, 19)), 'L3 each value taken by 6 units')
ok(all(sum(1 for c in range(1, 133) if c % 19 == y) == 7 for y in range(1, 19)), 'L3 seven numbers below 133 per residue')
roots7 = [x for x in range(1, 7) if pow(x, 3, 7) == 1]
ok(roots7 == [1, 2, 4] and [pow(x, 3, 7) for x in range(1, 7)] == [1, 1, 6, 1, 6, 6], 'L3 cubes mod 7')
K7 = [x for x in U133 if x % 7 == 1]
ok(sorted(set(K7) & set(K19)) == [1], 'L3 kernels meet in 1')
ok(all(len({x % 7 for x in U133 if x % 19 == y}) == 6 for y in roots19), 'L3 each coset meets each residue mod 7 once')
all3 = [x for x in U133 if pow(x, 3, 133) == 1]
num(3, 'p-units-133', 3, len(roots19) * len(roots7), len(all3), {'mod-19-only': len(L), 'one-only': len(roots19)})
ok(27 % 7 == 6 and 8 % 7 == 1 and 64 % 7 == 1, 'L3 slip lines: 3^3 = 6, 2^3 = 1, 4^3 = 1 mod 7')
ok(45 in U133 and 45 in L and 45 % 7 == 3 and pow(45, 3, 19) == 1 and pow(3, 3, 7) == 6 and 45 == 2 * 19 + 7, 'L3 45 is one of the 18 and fails mod 7')
ok(sum(1 for x in L if x not in all3) == 9 and pow(11, 3, 19) == pow(7, 6, 19) == 1, 'L3 nine of the 18 fail; 11^3 = 7^6 = 1')

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

# p-affine-five: x -> ax + b on Z_5
AFF = [(a, b) for a in range(1, 5) for b in range(5)]
af = lambda f, g: (f[0] * g[0] % 5, (f[0] * g[1] + f[1]) % 5)  # noqa: E731  f after g
ev = lambda f, x: (f[0] * x + f[1]) % 5  # noqa: E731
ok(all(ev(af(f, g), x) == ev(f, ev(g, x)) for f in AFF for g in AFF for x in range(5)), 'L3 composition rule')
ok(len(AFF) == 20 and all(af(f, g)[0] == f[0] * g[0] % 5 for f in AFF for g in AFF), 'L3 |G| = 20, mu a homomorphism')
eA = (1, 0)
ainv = lambda f: next(g for g in AFF if af(f, g) == eA)  # noqa: E731
T = [f for f in AFF if f[0] == 1]
h, t = (2, 0), (1, 1)
ok(ainv(h) == (3, 0), 'L3 h^-1 = 3x')
conj = af(af(h, t), ainv(h))
num(3, 'p-affine-five', 1, (2 * 3 * 0 + 2 * 1) % 5, conj[1] if conj[0] == 1 else -1,
    {'reversed': af(af(ainv(h), t), h)[1], 'commuted': 1})
ok(af(h, t) == (2, 2) and af(t, h) == (2, 1), 'L3 ht = 2x + 2, th = 2x + 1')
ok(all(af(af(g, x), ainv(g)) in T for g in AFF for x in T), 'L3 T is normal')
f = (2, 3)


def cos(g):
    return frozenset(af(g, x) for x in T)


Tset = frozenset(T)
k, g = 1, f
while cos(g) != Tset:
    g, k = af(g, f), k + 1
num(3, 'p-affine-five', 2, mord(2, 5), k, {'translations': 5, 'whole-group': 20})
ok(len({cos(g) for g in AFF}) == 4, 'L3 |G/T| = 4')


def aorder(f):
    g, m = f, 1
    while g != eA:
        g, m = af(g, f), m + 1
    return m


f4 = af(af(f, f), af(f, f))
ok(f4 == eA and 16 + 0 == 16 and 3 * (8 + 4 + 2 + 1) == 45 and 45 % 5 == 0, 'L3 f^4 = 16x + 45 = x')
fk = [f]
for _ in range(3):
    fk.append(af(f, fk[-1]))
ok([g[1] for g in fk] == [3, 9 % 5, 21 % 5, 45 % 5] and [3, 9, 21, 45] == [3 * (2 ** k - 1) for k in range(1, 5)], 'L3 constants of f^k are 3, 9, 21, 45')
num(3, 'p-affine-five', 3, 0, fk[3][1] if fk[3][0] == 1 else -1, {'added-four': (4 * 3) % 5, 'kept': 3})
ok(aorder(f) == 4 and all(aorder(g) % 4 == 0 for g in [f]), 'L3 ord(f) = 4')
ok(aorder((1, 3)) == 5, 'L3 a translation has order 5')
ok(all(aorder(g) == mord(g[0], 5) for g in AFF if g[0] != 1), 'L3 order of ax + b is ord(a) for a != 1')
o4 = [g for g in AFF if aorder(g) == 4]
num(3, 'p-affine-five', 4, sum(5 for a in range(1, 5) if mord(a, 5) == 4), len(o4),
    {'cosets': 2, 'one-multiplier': 5, 'all-but-t': 20 - 5})
ok(sorted({g[0] for g in o4}) == [2, 3] and aorder((4, 0)) == 2 and 3 ** 2 % 5 == 4 and 81 % 5 == 1, 'L3 multipliers of order 4 are 2 and 3; a = 4 has order 2')

# ============================================================ set shape
LESSONS = {1: {'p-probe-stride': ['l3', 'l4'], 'p-octagon-orders': ['l1', 'l2', 'l4'], 'p-pixel-scrambler': ['l1', 'l2', 'l3', 'l4']},
           2: {'p-server-moves': ['l8', 'l9'], 'p-units-21-cosets': ['l5', 'l6', 'l7'], 'p-fixing-five': ['l5', 'l6', 'l7', 'l8']},
           3: {'p-units-133': ['l10', 'l12'], 'p-powers-of-seven': ['l10', 'l12', 'l13'], 'p-affine-five': ['l10', 'l11', 'l12']}}
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
        lv_obj.expect('problems', P(2, 0, 'feedback.correct'), 41)
        lv_obj.expect('problems', P(2, 0, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 8)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 3, 'feedback.correct'), 19)
        lv_obj.expect('problems', P(2, 3, 'feedback.correct'), 5)
    if lv == 2:
        lv_obj.expect('problems', P(0, 1, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(0, 2, 'feedback.correct'), 6)
        lv_obj.expect('problems', P(0, 3, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(1, 0, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(1, 1, 'feedback.correct'), 16)
        lv_obj.expect('problems', P(1, 2, 'feedback.correct'), 4)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 5)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 3)
        lv_obj.expect('problems', P(2, 4, 'feedback.correct'), 6)
    if lv == 3:
        lv_obj.expect('problems', P(0, 0, 'feedback.correct'), 115)
        lv_obj.expect('problems', P(0, 1, 'feedback.correct'), 18)
        lv_obj.expect('problems', P(0, 2, 'feedback.correct'), 9)
        lv_obj.expect('problems', P(1, 0, 'feedback.correct'), 24)
        lv_obj.expect('problems', P(1, 1, 'feedback.correct'), 12)
        lv_obj.expect('problems', P(1, 2, 'feedback.correct'), 13)
        lv_obj.expect('problems', P(1, 3, 'feedback.correct'), 35)
        lv_obj.expect('problems', P(2, 0, 'feedback.correct'), 2)
        lv_obj.expect('problems', P(2, 1, 'feedback.correct'), 4)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 45)
        lv_obj.expect('problems', P(2, 2, 'feedback.correct'), 4)
        lv_obj.expect('problems', P(2, 3, 'feedback.correct'), 10)
    rc = lv_obj.report()
    ok(rc in (0, None), f'L{lv} numbers_lib report')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
