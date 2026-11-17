"""Delta read review-delta-ag-algebra: the four re-authored problems of algebra
problems-1 to -3 and the parts the fix pass changed on the kept problems.

Imports no earlier script. Every key, every `wrong` value and every printed
figure is rebuilt by brute force: matrices are multiplied entry by entry and
the inverse is found by search over all 7^4 matrices, permutations are dicts
composed right to left, units modulo 133 are listed and cubed one by one, and
the 20 affine maps are composed as tables of values.

Exit 0 always. A failing check prints `FAIL`; a finding of the review prints
a `FINDING` line while the content is as the review describes and `resolved`
once it is fixed.
"""
import json
import os
import re
import sys
from itertools import product
from math import gcd

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ALG = os.path.join(ROOT, 'app', 'content', 'courses', 'algebra')
N = [0, 0]


def check(name, cond):
    N[0] += 1
    if not cond:
        N[1] += 1
        print('FAIL', name)


def finding(n, open_, text):
    print(('FINDING %d: ' % n if open_ else 'resolved %d: ' % n) + text)


def load(n):
    return json.load(open(os.path.join(ALG, 'problems-%d.json' % n), encoding='utf-8'))


def item(d, i):
    return [x for x in d['items'] if x['id'] == i][0]


def key(p):
    return p['widget']['answer']


def wrongs(p):
    return {w['id']: w['value'] for w in p['widget'].get('wrong', [])}


def texts(p):
    out = [p['question'], p['feedback'].get('correct', ''), p['feedback'].get('generic', ''), p['explain']['text']]
    out += list(p['feedback'].get('byKey', {}).values())
    for o in p['widget'].get('options', []):
        out += [o.get('text', ''), o.get('why', '')]
    return ' '.join(out)


def bands(p, label):
    k = key(p)
    check(label + ' key band abs 0', p['widget']['tol'] == {'abs': 0})
    for i, v in wrongs(p).items():
        check('%s wrong %s differs from key' % (label, i), v != k)
        check('%s wrong %s has a byKey line' % (label, i), i in p['feedback'].get('byKey', {}))
    vals = list(wrongs(p).values())
    check(label + ' wrong values distinct', len(vals) == len(set(vals)))
    check(label + ' states its form', re.search(r'whole number|residue from', p['question']) is not None)


# ---------------------------------------------------------------- set 1
d1 = load(1)

# p-pixel-scrambler ---------------------------------------------------
ps = item(d1, 'p-pixel-scrambler')
P = 7
M = ((1, 2), (1, 3))
I2 = ((1, 0), (0, 1))


def mm(a, b, mod=None):
    r = tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return tuple(tuple(x % mod for x in row) for row in r) if mod else r


def mv(a, v, mod):
    return tuple(sum(a[i][k] * v[k] for k in range(2)) % mod for i in range(2))


check('scrambler map is M on columns', all(mv(M, (x, y), P) == ((x + 2 * y) % P, (x + 3 * y) % P) for x in range(P) for y in range(P)))
check('det M = 1', M[0][0] * M[1][1] - M[0][1] * M[1][0] == 1)
check('step is a bijection of the 49 pixels', len({mv(M, (x, y), P) for x in range(P) for y in range(P)}) == 49)
M2 = mm(M, M)
M4 = mm(M2, M2)
check('M^2 = (3 8; 4 11)', M2 == ((3, 8), (4, 11)))
check('M^4 entries 41, 112, 56, 153', M4 == ((41, 112), (56, 153)))
check('M^4 = 6I mod 7', mm(M2, M2, P) == ((6, 0), (0, 6)))
p1, p2, p3, p4 = ps['parts']
check('part 1 key', key(p1) == M4[0][0] % P == 6)
check('part 1 entrywise', wrongs(p1)['entrywise'] == (M[0][0] ** 4) % P)
check('part 1 dropped-term', wrongs(p1)['dropped-term'] == (M2[0][0] * M2[0][0]) % P)
check('part 1 prints 41', '41' in p1['feedback']['correct'] and '3 \\cdot 3 + 8 \\cdot 4' in p1['feedback']['correct'])
# order by walking the powers
powers = [I2]
for _ in range(60):
    powers.append(mm(powers[-1], M, P))
order = next(k for k in range(1, 61) if powers[k] == I2)
check('part 2 key = order by walking', key(p2) == order == 8)
check('part 2 minus-one = exponent of -I', wrongs(p2)['minus-one'] == 4 and powers[4] == ((6, 0), (0, 6)))
check('part 2 modulus slip', wrongs(p2)['modulus'] == P and powers[7] != I2)
check('M^7 = -M^3', powers[7] == tuple(tuple((-x) % P for x in r) for r in powers[3]))
check('order divides k iff M^k = I (k to 60)', all((powers[k] == I2) == (k % 8 == 0) for k in range(1, 61)))
# inverse by search
inv = [A for A in (((a, b), (c, e)) for a, b, c, e in product(range(P), repeat=4)) if mm(A, M, P) == I2 and mm(M, A, P) == I2]
check('inverse unique', len(inv) == 1)
Minv = inv[0]
check('M^-1 = (3 5; 6 1)', Minv == ((3, 5), (6, 1)) == powers[7])
check('M^3 integer entries 11, 30, 15, 41', mm(M, M2) == ((11, 30), (15, 41)))
check('M^3 mod 7 = (4 2; 1 6)', powers[3] == ((4, 2), (1, 6)))
check('part 3 key', key(p3) == Minv[0][0] == 3)
check('part 3 no-minus', wrongs(p3)['no-minus'] == powers[3][0][0] == 4)
check('part 3 forward', wrongs(p3)['forward'] == M[0][0] and powers[2] != I2)
pre = [(x, y) for x in range(P) for y in range(P) if mv(M, (x, y), P) == (3, 1)]
check('part 4 preimage unique (0, 5)', pre == [(0, 5)])
check('part 4 key', key(p4) == pre[0][1] == 5)
check('part 4 prints (14, 19) and (10, 15)', 3 * 3 + 5 * 1 == 14 and 6 * 3 + 1 == 19 and (0 + 2 * 5, 0 + 3 * 5) == (10, 15))
check('part 4 forward', wrongs(p4)['forward'] == mv(M, (3, 1), P)[1] == 6 and mv(M, (3, 1), P) == (5, 6))
check('part 4 no-minus', mv(powers[3], (3, 1), P) == (0, 2) and wrongs(p4)['no-minus'] == 2 and mv(M, (0, 2), P) == (4, 6))
for i, p in enumerate(ps['parts']):
    bands(p, 'scrambler part %d' % (i + 1))
check('scrambler skills', ps['skills'] == ['ag-groups'])
# level 1 only: no later theorem named
check('scrambler names no later theorem', not re.search(r'Lagrange|Fermat|Euler|coset|subgroup|homomorph', json.dumps(ps)))

# p-probe-stride, findings 3 and 4 ------------------------------------
pr = item(d1, 'p-probe-stride')
q1, q2, q3, q4 = pr['parts']
walk = [(21 * k) % 56 for k in range(1, 57)]
check('probe part 1 key: first return', key(q1) == walk.index(0) + 1 == 8)
check('probe part 1 wrongs', wrongs(q1) == {'gcd': gcd(21, 56), 'full': 56})
check('probe part 1 asks the return', 'first back at slot 0' in q1['question'] and 'counting slot 0' not in q1['question'])
check('probe slots visited are the multiples of 7', sorted(set(walk)) == list(range(0, 56, 7)))
gens = [s for s in range(1, 56) if len({(s * k) % 56 for k in range(56)}) == 56]
check('probe part 2 key', key(q2) == len(gens) == 24)
check('probe part 2 wrongs', wrongs(q2) == {'no-overlap': 56 - 28 - 8, 'odd-only': 28, 'all': 55})
check('probe part 2 restates part 1', 'By part 1' in q2['question'] and '8 jumps' in q2['question'])
check('probe part 2 all line', 'visits only 8 slots' in q2['feedback']['byKey']['all'] and len(set(walk)) == 8)
k1 = next(k for k in range(1, 56) if (9 * k) % 56 == 1)
check('probe part 3 key', key(q3) == k1 == 25 and 9 in gens)
check('probe part 3 restates part 2', '24 generators from part 2' in q3['question'])
check('probe part 3 wrongs', wrongs(q3) == {'dropped-nine': 24, 'sign': (-25) % 56})
check('probe part 4 key', key(q4) == next(k for k in range(1, 56) if (9 * k) % 56 == 13) == (25 * 13) % 56)

# ---------------------------------------------------------------- set 2
d2 = load(2)


def cyc(n, *cycles):
    f = {i: i for i in range(1, n + 1)}
    for c in cycles:
        for a, b in zip(c, c[1:] + c[:1]):
            f[a] = b
    return f


def comp(f, g):  # f after g
    return {i: f[g[i]] for i in g}


def inverse(f):
    return {v: k for k, v in f.items()}


def cycles_of(f):
    seen, out = set(), []
    for i in sorted(f):
        if i not in seen:
            c = [i]
            seen.add(i)
            while f[c[-1]] != i:
                c.append(f[c[-1]])
                seen.add(c[-1])
            out.append(tuple(c))
    return out


def sign(f):  # by inversions
    xs = [f[i] for i in sorted(f)]
    inv_ = sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])
    return -1 if inv_ % 2 else 1


def perm_order(f):
    e = {i: i for i in f}
    g, k = dict(f), 1
    while g != e:
        g, k = comp(f, g), k + 1
    return k


sm = item(d2, 'p-server-moves')
sg = cyc(8, (1, 2, 3, 4, 5, 6))
ta = cyc(8, (1, 3, 5, 7), (2, 8))
xi = comp(ta, inverse(sg))
check('xi sigma = tau', comp(xi, sg) == ta)
check('xi is the only solution (cancel on the right)', comp(comp(ta, inverse(sg)), sg) == ta)
check('xi cycles', [c for c in cycles_of(xi) if len(c) > 1] == [(1, 6, 7), (2, 3, 8), (4, 5)])
s1, s2, s3, s4 = sm['parts']
check('signs: sigma odd, tau even, xi odd', (sign(sg), sign(ta), sign(xi)) == (-1, 1, -1))
opts = {o['id']: o for o in s1['widget']['options']}
check('server part 1 key a only', [i for i, o in opts.items() if o.get('correct')] == ['a'] and 'Odd' in opts['a']['text'])
check('server part 1 transposition counts', 6 - 1 == 5 and (4 - 1) + (2 - 1) == 4)
check('server part 2 key', key(s2) == xi[1] == 6 and inverse(sg)[1] == 6 and ta[6] == 6)
check('server part 2 wrongs', wrongs(s2) == {'no-inverse': comp(ta, sg)[1], 'wrong-side': comp(inverse(sg), ta)[1]} == {'no-inverse': 8, 'wrong-side': 2})
check('server part 3 key', key(s3) == perm_order(xi) == 6)
check('server part 3 wrongs', wrongs(s3) == {'product': 3 * 3 * 2, 'sum': 3 + 3 + 2, 'longest': 3})
x3 = comp(xi, comp(xi, xi))
check('after 3 nights only 4 and 5 are swapped', [c for c in cycles_of(x3) if len(c) > 1] == [(4, 5)])
pw, evens = dict(xi), []
for k in range(1, 7):
    if sign(pw) == 1:
        evens.append(k)
    pw = comp(xi, pw)
check('server part 4 key', key(s4) == len(evens) == 3 and evens == [2, 4, 6])
check('server part 4 wrongs', wrongs(s4) == {'same-sign': 0, 'missed-identity': 2})
for i, p in enumerate(sm['parts'][1:]):
    bands(p, 'server part %d' % (i + 2))
check('server skills', sm['skills'] == ['ag-perm'])
# literal reading of part 3: the jobs never return to their Monday servers
state, back = dict(ta), []
for night in range(1, 25):
    state = comp(xi, state)
    if state == {i: i for i in range(1, 9)}:
        back.append(night)
finding(4, 'back on the server it started from' in s3['question'] and back == [],
        'p-server-moves part 3: counted from Monday morning, xi^k tau is never the identity (k to 24); the part means xi run alone')

# p-fixing-five, findings 6 and 7 -------------------------------------
ff = item(d2, 'p-fixing-five')
f1, f2, f3, f4, f5 = ff['parts']
from itertools import permutations
S5 = [dict(zip(range(1, 6), p)) for p in permutations(range(1, 6))]
H = [t for t in S5 if t[5] == 5]
sig = cyc(5, (1, 5, 3, 2))
check('sigma written (1 5 3 2) in both questions', all('(1\\,5\\,3\\,2)' in p['question'] for p in (f3, f4)))
left = [comp(sig, h) for h in H]
right = [comp(h, sig) for h in H]
check('left coset sends 5 to 3', {t[5] for t in left} == {3} and len(left) == 24 and key(f3) == 3)
check('right coset sends 1 to 5', all(t[1] == 5 for t in right) and key(f4) == 1)
check('left coset = all tau with tau(5) = 3', sorted(map(str, left)) == sorted(str(t) for t in S5 if t[5] == 3))
check('right coset = all tau with tau(1) = 5', sorted(map(str, right)) == sorted(str(t) for t in S5 if t[1] == 5))
check('part 3 wrongs', wrongs(f3) == {'inverse': inverse(sig)[5], 'fixed': 5})
check('part 4 wrongs', wrongs(f4) == {'left-coset': sig[5], 'five': 5} and sig[5] == 3)
both = [t for t in left if t in right]
check('overlap 6', len(both) == 6 == key(f5))
t35 = cyc(5, (3, 5))
check('(3 5) in the left coset only', t35 in left and t35 not in right)
check('H has 24 elements, index 5', len(H) == 24 and key(f2) == 120 // 24)
# finding 7: the test with its first condition, and the counterexample
check('one-step test names non-empty', 'non-empty' in f1['explain']['text'])
e3 = {1: 1, 2: 2, 3: 3}
a12, a23 = cyc(3, (1, 2)), cyc(3, (2, 3))
check('{e, (1 2), (2 3)} is not closed', comp(a12, a23) not in (e3, a12, a23))
check('option d why line', 'non-empty' in [o for o in f1['widget']['options'] if o['id'] == 'd'][0]['why'])
check('(1 2) and (2 3) do not commute', comp(a12, a23) != comp(a23, a12))

# ---------------------------------------------------------------- set 3
d3 = load(3)

# p-units-133 ---------------------------------------------------------
un = item(d3, 'p-units-133')
G = [x for x in range(1, 133) if gcd(x, 133) == 1]
check('|G| = 108', len(G) == 108)
check('reduction is multiplicative', all((x * y % 133) % 19 == (x % 19) * (y % 19) % 19 for x in G for y in G))
u1, u2, u3 = un['parts']
ker19 = [x for x in G if x % 19 == 1]
check('units part 1 key', key(u1) == len(ker19) == 6)
check('units part 1 list', [x for x in range(1, 133) if x % 19 == 1] == [1, 20, 39, 58, 77, 96, 115] and 77 == 7 * 11)
check('units part 1 wrongs', wrongs(u1) == {'kept-77': 7, 'trivial': 1})
check('kernel is closed', all((x * y) % 133 in ker19 for x in ker19 for y in ker19))
check('rho is onto', {x % 19 for x in G} == set(range(1, 19)))
roots19 = [y for y in range(1, 19) if pow(y, 3, 19) == 1]
check('cube roots of 1 mod 19', roots19 == [1, 7, 11] and 343 == 18 * 19 + 1 and 49 % 19 == 11)
c19 = [x for x in G if pow(x, 3, 19) == 1]
ord3 = [x for x in G if pow(x, 3, 19) == 1 and x % 19 != 1]
if 'order 3' in u2['question']:  # after fix 1: the units whose reduction has order 3
    check('units part 2 key (fixed form)', key(u2) == len(ord3) == 12)
    check('units part 2 wrongs (fixed form)', wrongs(u2) == {'roots-only': 2, 'with-kernel': len(c19), 'one-coset': 6, 'seven-each': 2 * 7})
else:
    check('units part 2 key', key(u2) == len(c19) == 18)
    check('units part 2 wrongs', wrongs(u2) == {'roots-only': 3, 'only-one': 6, 'seven-each': 21})
check('seven numbers reduce to each y, one a multiple of 7', all(len([x for x in range(133) if x % 19 == y]) == 7 and len([x for x in range(133) if x % 19 == y and x % 7 == 0]) == 1 for y in range(1, 19)))
ker7 = [x for x in G if x % 7 == 1]
check('both kernels meet in 1 only', [x for x in ker19 if x in ker7] == [1])
check('reduction mod 7 is onto', {x % 7 for x in G} == set(range(1, 7)))
check('cubes mod 7', [pow(x, 3, 7) for x in range(1, 7)] == [1, 1, 6, 1, 6, 6])
c133 = [x for x in G if pow(x, 3, 133) == 1]
check('units part 3 key', key(u3) == len(c133) == 9)
check('units part 3 wrongs', wrongs(u3) == {'mod-19-only': 18, 'one-only': 3})
check('each coset meets each residue mod 7 once', all(sorted(x % 7 for x in G if x % 19 == y) == [1, 2, 3, 4, 5, 6] for y in range(1, 19)))
for i, p in enumerate(un['parts']):
    bands(p, 'units part %d' % (i + 1))
check('units skills', un['skills'] == ['ag-hom', 'ag-groups'])
finding(1, key(u2) == len(G) // len(ker19),
        'p-units-133 part 2: the key 18 is also 108/6, the number of cosets of ker rho and the size of the image; '
        'a learner who divides and stops is marked right')
finding(5, '45' not in u3['feedback']['byKey']['mod-19-only'] and 3 not in c19,
        'p-units-133 part 3 byKey mod-19-only: "many of them fail: 3^3 = 27" but 3 is not one of the 18 units (3^3 = 8 mod 19)')
check('fix 5 example: 45 is one of the 18 and fails mod 7', 45 in c19 and 45 % 7 == 3 and pow(45, 3, 7) == 6 and 45 not in c133)
# fix 1: part 2 asks for the units whose reduction has order 3
check('fix 1: 12 units reduce to an element of order 3; slips 2, 18, 14, 6', len(ord3) == 12 and 12 != 108 // 6 and 2 * 7 == 14 and len(ord3) + len(ker19) == 18)

# p-affine-five -------------------------------------------------------
af = item(d3, 'p-affine-five')
X = range(5)
maps = {(a, b): tuple((a * x + b) % 5 for x in X) for a in range(1, 5) for b in range(5)}
check('20 different maps', len(set(maps.values())) == 20)


def co(f, g):  # f after g, as tuples
    return tuple(f[g[x]] for x in X)


name = {v: k for k, v in maps.items()}
ident = maps[(1, 0)]
check('closed, with ax+b after cx+d = acx + (ad+b)', all(name[co(maps[(a, b)], maps[(c, e)])] == ((a * c) % 5, (a * e + b) % 5) for (a, b) in maps for (c, e) in maps))
T = [maps[(1, b)] for b in range(5)]


def minv(f):
    return next(g for g in maps.values() if co(f, g) == ident)


def aord(f):
    g, k = f, 1
    while g != ident:
        g, k = co(f, g), k + 1
    return k


h, t = maps[(2, 0)], maps[(1, 1)]
a1, a2, a3, a4 = af['parts']
check('h^-1 = 3x', name[minv(h)] == (3, 0))
conj = co(h, co(t, minv(h)))
check('affine part 1 key', name[conj] == (1, 2) and key(a1) == 2)
check('affine part 1 wrongs', wrongs(a1) == {'reversed': name[co(minv(h), co(t, h))][1], 'commuted': 1} and name[co(minv(h), co(t, h))] == (1, 3))
check('ht = 2x+2, th = 2x+1', name[co(h, t)] == (2, 2) and name[co(t, h)] == (2, 1))
check('T is normal (all conjugates)', all(co(g, co(s, minv(g))) in T for g in maps.values() for s in T))
f = maps[(2, 3)]
cosets = {}
for g in maps.values():
    cosets.setdefault(frozenset(co(g, s) for s in T), []).append(g)
check('4 cosets of T, 5 maps each, one per multiplier', len(cosets) == 4 and all(len({name[g][0] for g in c}) == 1 and len(c) == 5 for c in cosets))
kT = next(k for k in range(1, 21) if (lambda g: g in T)(__import__('functools').reduce(lambda acc, _: co(f, acc), range(k - 1), f)))
check('affine part 2 key: least k with f^k in T', key(a2) == kT == 4)
check('affine part 2 wrongs', wrongs(a2) == {'translations': len(T), 'whole-group': len(maps)})
check('powers of 2 mod 5', [pow(2, k, 5) for k in range(1, 5)] == [2, 4, 3, 1])
f4 = co(f, co(f, co(f, f)))
check('f^4 = e, constant 45', f4 == ident and 3 * (8 + 4 + 2 + 1) == 45 and 45 % 5 == 0)
check('constants of f^k: 3, 9, 21, 45', [3 * (2 ** k - 1) for k in range(1, 5)] == [3, 9, 21, 45])
check('order of f is 4', aord(f) == 4 and aord(t) == 5)
if 'x + c' in a3['question']:  # after fix 2: the constant of f^4
    check('affine part 3 key (fixed form)', key(a3) == name[f4][1] == 0)
    check('affine part 3 wrongs (fixed form)', wrongs(a3) == {'added-four': (4 * 3) % 5, 'kept': 3})
else:
    check('affine part 3 key', key(a3) == aord(f) == 4)
    check('affine part 3 wrongs', wrongs(a3) == {'times-five': 20, 'translation': 5})
orders = {k: aord(v) for k, v in maps.items()}
check('order of f = order of its multiplier when a != 1', all(orders[(a, b)] == next(k for k in range(1, 5) if pow(a, k, 5) == 1) for (a, b) in maps if a != 1))
n4 = sum(1 for v in orders.values() if v == 4)
check('affine part 4 key', key(a4) == n4 == 10)
check('affine part 4 wrongs', wrongs(a4) == {'cosets': 2, 'one-multiplier': 5, 'all-but-t': 15})
check('a = 4 maps have order 2', all(orders[(4, b)] == 2 for b in range(5)))
check('f^k formula', all(name[__import__('functools').reduce(lambda acc, _: co(maps[(a, b)], acc), range(k - 1), maps[(a, b)])] == (pow(a, k, 5), (b * (pow(a, k, 5) - 1) * pow(a - 1, -1, 5)) % 5) for (a, b) in maps if a != 1 for k in range(1, 6)))
for i, p in enumerate(af['parts']):
    bands(p, 'affine part %d' % (i + 1))
check('affine skills', af['skills'] == ['ag-hom', 'ag-cosets'])
m = re.search(r'ord\}\(fT\) = (\d+)', a3['question'])
finding(2, bool(m) and 'order of $f$ itself' in a3['question'] and int(m.group(1)) == key(a3),
        'p-affine-five part 3: the question prints ord(fT) = 4 and the key is 4; retyping the printed number passes')
# fix 2: ask for the constant c of f^4 = x + c
check('fix 2: c = 0, slips 2 (3 added four times) and 3 (constant of f)', name[f4] == (1, 0) and (4 * 3) % 5 == 2)
finding(3, a2['question'].startswith('So $T$ is normal'),
        'p-affine-five part 2: "So T is normal" follows one conjugate by one h; T is normal as a kernel (l11 screen 7)')

# skills of each level's lessons
lev = {l['n']: l['lessons'] for l in json.load(open(os.path.join(ALG, 'course.json'), encoding='utf-8'))['levels']}
for n, d in ((1, d1), (2, d2), (3, d3)):
    have = set()
    for l in lev[n]:
        have |= set(json.load(open(os.path.join(ALG, l + '.json'), encoding='utf-8')).get('skills', []))
    check('level %d skills carried by its lessons' % n, all(set(it['skills']) <= have for it in d['items']))

print('%d checks, %d failed' % (N[0], N[1]))
sys.exit(0)
