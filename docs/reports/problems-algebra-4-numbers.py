"""Recompute every number in app/content/courses/algebra/problems-4.json twice.

Method 1 works by a rule (ad - bc, Euclid's back-substitution, the adjugate, Wilson read off x^16 - 1, the rational
root test and exact long division with fractions, the discriminant). Method 2 is brute force (search Z_29 for the
inverse, multiply matrices out, multiply 1 to 16 out, evaluate x^16 - 1 at every residue, test every candidate in f,
multiply the factors back, find real roots numerically with numpy). For each numeric part the script checks that the
two methods agree, that the JSON key equals the value, that every `wrong` value equals its named slip recomputed here,
has a byKey line and differs from the key. Choice parts check the keyed option and verify each option's claim.
Figures stated in feedback and explain are checked as text (numbers_lib.Level.expect), and
numbers_lib.Level.check_wrongs runs as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-algebra-4-numbers.py
"""
import json, os, sys
from fractions import Fraction as F
from math import factorial, gcd
import numpy as np
import sympy as sp

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


DOC = json.load(open(os.path.join(COURSE, 'problems-4.json'), encoding='utf8'))
ITEMS = {it['id']: it for it in DOC['items']}


def part(iid, p):
    return ITEMS[iid]['parts'][p - 1]


def num(iid, p, rule, brute, slips, tol=0):
    pt = part(iid, p)
    w, tag = pt['widget'], f'{iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} numeric')
    ok(abs(rule - brute) < 1e-12, f'{tag} methods agree {rule} vs {brute}')
    ok(abs(w['answer'] - rule) < 1e-12, f'{tag} key {w["answer"]} == {rule}')
    ok(w['tol'] == {'abs': tol}, f'{tag} band {w["tol"]}')
    got = {x['id']: x['value'] for x in w.get('wrong', [])}
    ok(set(got) == set(slips), f'{tag} slip ids {sorted(got)} vs {sorted(slips)}')
    by = pt['feedback'].get('byKey', {})
    for k, v in slips.items():
        ok(k in got and abs(got[k] - v) < 1e-12, f'{tag} slip {k} {got.get(k)} == {v}')
        ok(abs(v - rule) > 2 * tol + 1e-9, f'{tag} slip {k} differs from key')
        ok(k in by, f'{tag} slip {k} has byKey')
    ok(len(set(got.values())) == len(got), f'{tag} slips distinct')


def key(iid, p, cid):
    opts = part(iid, p)['widget']['options']
    ok([o['id'] for o in opts if o.get('correct')] == [cid], f'{iid} p{p} key {cid}')
    ok(all(o.get('correct') or o.get('why') for o in opts), f'{iid} p{p} every distractor has why')


def inv_brute(a, n):
    return next(k for k in range(n) if a * k % n == 1)


# ============================================================ p-cipher-29
P = 29
K = [[9, 4], [5, 7]]
ok(sp.isprime(P), '29 is prime, so Z_29 is a field')
key('p-cipher-29', 1, 'det')
# option claims: [[1,1],[1,1]] has det 0; diag(1,0) diag(0,1) = 0; K does not commute with every matrix
ok(1 * 1 - 1 * 1 == 0, 'all-ones matrix has det 0')
ok((np.array([[1, 0], [0, 0]]) @ np.array([[0, 0], [0, 1]]) == 0).all(), 'zero divisor in M_2')
E = np.array([[0, 1], [0, 0]])
Kn = np.array(K)
ok(not ((Kn @ E - E @ Kn) % P == 0).all(), 'K does not commute with E_12')
# brute: K is a unit of M_2(Z_29) -- find its inverse by search over column solutions
detK = (K[0][0] * K[1][1] - K[0][1] * K[1][0]) % P
detK_sym = int(sp.Matrix(K).det() % P)
num('p-cipher-29', 2, detK, detK_sym, {'added': (63 + 20) % P, 'reversed': (20 - 63) % P})
ok(63 - 20 == 43 and 43 - 29 == 14 and 83 % 29 == 25 and (-43) % 29 == 15, 'p2 stated figures')
inv = pow(detK, -1, P)
num('p-cipher-29', 3, inv, inv_brute(detK, P), {'from-added': pow(25, -1, P), 'sign': (-inv) % P})
ok(29 == 2 * 14 + 1 and 14 * 27 == 378 == 13 * 29 + 1, 'p3 Euclid line and check')
ok(14 * 2 % 29 == 28, 'p3 14*2 = 28 = -1')
ok(25 * 7 % 29 == 1, 'p3 7 is the inverse of 25')
adj = [[K[1][1], -K[0][1]], [-K[1][0], K[0][0]]]
Kinv = [[inv * adj[i][j] % P for j in range(2)] for i in range(2)]
Kinv_sym = (sp.Matrix(K).inv_mod(P)).tolist()
ok(Kinv == Kinv_sym == [[15, 8], [10, 11]], f'K^-1 {Kinv} {Kinv_sym}')
ok(((Kn @ np.array(Kinv)) % P == np.eye(2, dtype=int)).all(), 'K K^-1 = I mod 29')
num('p-cipher-29', 4, Kinv[1][0], int(Kinv_sym[1][0]),
    {'sign': inv * 5 % P, 'swapped': inv * (-4) % P, 'unscaled': (-5) % P})
ok(2 * (-5) % P == 19, 'p4 sign slip of part 3 also gives 19')
ok(27 * (-5) == -135 and -135 + 145 == 10 and 5 * 29 == 145, 'p4 stated figures')
# p5: plaintext GO = (6, 14)
pt = [6, 14]
c = [(K[0][0] * pt[0] + K[0][1] * pt[1]) % P, (K[1][0] * pt[0] + K[1][1] * pt[1]) % P]
ok(c == [23, 12], f'ciphertext of GO is {c}')
p2 = (Kinv[1][0] * c[0] + Kinv[1][1] * c[1]) % P
p2_brute = next(b for a in range(P) for b in range(P)
                if [(9 * a + 4 * b) % P, (5 * a + 7 * b) % P] == c)
num('p-cipher-29', 5, p2, p2_brute,
    {'used-K': (5 * 23 + 7 * 12) % P, 'column': (23 * Kinv[0][1] + 12 * Kinv[1][1]) % P,
     'from-19': (19 * 23 + 11 * 12) % P})
ok(10 * 23 + 11 * 12 == 362 == 12 * 29 + 14 and 230 + 132 == 362, 'p5 stated sum')
ok(15 * 23 + 8 * 12 == 441 and 441 % 29 == 6, 'p5 top row gives 6')
ok(23 * 8 + 12 * 11 == 316 and 316 % 29 == 26, 'p5 column slip 26')
ok(19 * 23 + 11 * 12 == 569 and 569 % 29 == 18, 'p5 from-19 slip 569 -> 18')
ok(chr(ord('A') + 6) + chr(ord('A') + 14) == 'GO', 'symbols 6 and 14 read GO')

# ============================================================ p-sixteen-factorial
Q = 17
ok(sp.isprime(Q), '17 is prime')
roots = [a for a in range(Q) if (pow(a, 16, Q) - 1) % Q == 0]
num('p-sixteen-factorial', 1, Q - 1, len(roots), {'with-zero': 17, 'real': len([r for r in (-1, 1)])})
ok((0 ** 16 - 1) == -1, 'f(0) = -1')
key('p-sixteen-factorial', 2, 'peel')
x = sp.symbols('x')
prod = sp.Poly(sp.prod([x - a for a in range(1, 17)]), x, modulus=Q)
ok(prod == sp.Poly(x ** 16 - 1, x, modulus=Q), 'x^16 - 1 = prod (x - a) in Z_17[x]')
ok(len([a for a in range(3) if (a * a + 1) % 3 == 0]) == 0, 'x^2 + 1 has no root in Z_3 (splits option)')
w16 = factorial(16) % Q
const = 1
for a in range(1, 17):
    const = const * (-a) % Q
num('p-sixteen-factorial', 3, (-1) % Q, w16, {'plus-one': 1})
ok(const == (-1) % Q, 'constant term of the product is -1')
num('p-sixteen-factorial', 4, w16 * pow(16, -1, Q) % Q, factorial(15) % Q, {'kept': 16})
ok(pow(16, -1, Q) == 16, '16 is its own inverse mod 17')
num('p-sixteen-factorial', 5, pow(15, -1, Q), factorial(14) % Q,
    {'sign': pow(2, -1, Q), 'times': 15})
ok(pow(2, -1, Q) == 9 == (-8) % Q == 16 * 8 % Q, 'sign slip: 2^-1 = 9 = -8 = 16 * 15^-1')
ok(15 * 8 == 120 == 7 * 17 + 1 and (-2) * 8 == -16 and (-16) % 17 == 1, 'p5 stated figures')

# ============================================================ p-three-year-return
coef = [8, -6, -1, -5]                       # f = 8x^3 - 6x^2 - x - 5
fx = lambda t: sum(cf * t ** (3 - i) for i, cf in enumerate(coef))
# break-even: -8 x^3 + 6 x^2 + 1 x + 5 = 0 is -f
ok([-c for c in coef] == [-8, 6, 1, 5], 'f is minus the year-3 value of the flows')
divs = lambda n: [d for d in range(1, n + 1) if n % d == 0]
cands = sorted({F(u, v) for u in divs(5) for v in divs(8)})
num('p-three-year-return', 1, len(cands), len(divs(5)) * len(divs(8)),
    {'with-negatives': 2 * len(cands), 'added': len(divs(5)) + len(divs(8))})
rts = [c for c in cands if fx(c) == 0]
ok(rts == [F(5, 4)], f'only root among candidates {rts}')
r = float(rts[0] - 1)
npv = -8 + 6 / 1.25 + 1 / 1.25 ** 2 + 5 / 1.25 ** 3
ok(abs(npv) < 1e-12, 'NPV at 25% is 0')
num('p-three-year-return', 2, r, 6 / 4.8 - 1, {'gave-x': 1.25, 'discount': 1 - 1 / 1.25}, tol=0.0001)
ok(6 / 1.25 == 4.8 and abs(1 / 1.25 ** 2 - 0.64) < 1e-12 and abs(5 / 1.25 ** 3 - 2.56) < 1e-12, 'p2 check figures')
ok(F(8) * F(125, 64) == F(125, 8) and F(6) * F(25, 16) == F(75, 8) and F(5, 4) == F(10, 8) and F(5) == F(40, 8)
   and F(125 - 75 - 10 - 40, 8) == 0, 'p2 eighths')
q, rem = sp.div(sp.Poly(8 * x ** 3 - 6 * x ** 2 - x - 5, x), sp.Poly(4 * x - 5, x))
ok(q == sp.Poly(2 * x ** 2 + x + 1, x) and rem.is_zero, f'quotient {q} remainder {rem}')
ok(sp.expand((4 * x - 5) * (2 * x ** 2 + x + 1)) == 8 * x ** 3 - 6 * x ** 2 - x - 5, 'expansion check')
ok(sp.expand(8 * x ** 3 - 6 * x ** 2 - x - 5 - 2 * x ** 2 * (4 * x - 5)) == 4 * x ** 2 - x - 5, 'first step leaves 4x^2 - x - 5')
ok(sp.expand(4 * x ** 2 - x - 5 - x * (4 * x - 5)) == 4 * x - 5, 'second step leaves 4x - 5')
ok(sp.div(sp.Poly(8 * x ** 3 - 6 * x ** 2 - x - 5, x), sp.Poly(x - sp.Rational(5, 4), x))[0]
   .as_expr() == 8 * x ** 2 + 4 * x + 4, 'by-root slip is the quotient by x - 5/4')
pt3 = part('p-three-year-return', 3)
ok(pt3['widget']['answer'] == '2x^2+x+1' and pt3['widget']['wrong'][0]['tex'] == '8x^2+4x+4', 'p3 JSON key and slip')
disc = 1 ** 2 - 4 * 2 * 1
real = [z for z in np.roots(coef) if abs(z.imag) < 1e-9]
num('p-three-year-return', 4, 1 if disc < 0 else 3, len(real), {'cubic': 3})
ok(disc == -7, 'discriminant -7')
ok(gcd(5, 8) == 1, '5 shares no factor with 8')

# ============================================================ numbers_lib text checks
lv = Level('algebra', 4)
T = lambda i, p, f: f'items[{i}].parts[{p}].{f}'
for i, p, v in [(0, 1, 14), (0, 2, 27), (0, 3, 10), (0, 4, 14), (1, 0, 16), (1, 2, 16), (1, 3, 1), (1, 4, 8),
                (2, 0, 8), (2, 1, 25), (2, 3, 1)]:
    lv.expect('problems', T(i, p, 'feedback.correct'), v)
for i, p, v in [(0, 1, 43), (0, 2, 378), (0, 3, 145), (0, 4, 441), (1, 4, 8), (2, 1, 2.56), (2, 3, -7)]:
    lv.expect('problems', T(i, p, 'explain.text'), v)
lv.claim(all(s in DOC['items'][2]['prose'] for s in ['£8,000', '£6,000', '£1,000', '£5,000']), 'p3 flows in prose')
lv.check_wrongs('problems')
bad = [r for r in lv.results if not r[0]]
ok(not bad, f'numbers_lib: {len(lv.results) - len(bad)} of {len(lv.results)}')

# fix pass: finding 1, 2, 4, 5
ok(DOC['items'][2]['parts'][2]['widget'].get('form') == 'expanded', 'p3 part 3 has form expanded')
ok(sorted({x * x % 17 for x in range(17)}) == [0, 1, 2, 4, 8, 9, 13, 15, 16] and 3 not in {x * x % 17 for x in range(17)}, 'x^2 - 3 has no root mod 17')
ok(8 - 2 == 6 and 2 + 4 == 6, 'added slip 6 equals leaving out whole numbers 1 and 5')
ok(14 * 2 % 29 == 28 and 15 * 2 % 29 == 1, 'sign slip 2 is -14^-1 and 15^-1')

print(f'{checks - len(fails)} of {checks} checks passed')
sys.exit(1 if fails else 0)
