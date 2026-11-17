#!/usr/bin/env python3
"""Second read of app/content/courses/algebra/problems-4.json (review-problems-algebra-4.md).

Every key, every wrong value and every number printed in a feedback or explain line is typed
here from the prose and recomputed without the author's script: brute force over residues,
exact fractions, polynomial arithmetic on coefficient lists. Exit 0 always; a failing check
prints a FINDING line.
"""
import json
import re
from fractions import Fraction as Fr
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SET = json.loads((ROOT / 'app/content/courses/algebra/problems-4.json').read_text())
ITEMS = {it['id']: it for it in SET['items']}
n_checks = 0
n_find = 0


def check(name, ok, detail=''):
    global n_checks, n_find
    n_checks += 1
    if not ok:
        n_find += 1
        print(f'FINDING {name} {detail}')


def part(item, k):
    return ITEMS[item]['parts'][k - 1]


def key(item, k):
    return part(item, k)['widget']['answer']


def wrongs(item, k):
    return {w['id']: w.get('value', w.get('tex')) for w in part(item, k)['widget'].get('wrong', [])}


def text(item, k):
    p = part(item, k)
    fb = p['feedback']
    bits = [p['question'], fb['correct'], fb['generic'], p['explain']['text']] + list(fb.get('byKey', {}).values())
    bits += [o.get('text', '') + ' ' + o.get('why', '') for o in p['widget'].get('options', [])]
    return ' '.join(bits)


def has(item, k, *needles):
    t = text(item, k)
    for s in needles:
        check(f'{item} part {k} prints {s!r}', s in t)


def numeric_shape(item, k, value, slips):
    w = part(item, k)['widget']
    check(f'{item} part {k} key', w['answer'] == value, f"file {w['answer']} mine {value}")
    got = wrongs(item, k)
    check(f'{item} part {k} wrong ids', set(got) == set(slips), f'{sorted(got)} against {sorted(slips)}')
    tol = w['tol']['abs']
    for wid, v in slips.items():
        check(f'{item} part {k} wrong {wid}', got.get(wid) == v, f'file {got.get(wid)} mine {v}')
        check(f'{item} part {k} wrong {wid} outside key band', abs(v - value) > tol + 1e-12)
        check(f'{item} part {k} wrong {wid} has a line', wid in part(item, k)['feedback'].get('byKey', {}))
    vals = [value] + list(slips.values())
    check(f'{item} part {k} wrong values distinct', len(set(vals)) == len(vals))
    check(f'{item} part {k} states its form', 'Give ' in part(item, k)['question'])


# ---------------------------------------------------------------- p-cipher-29
P = 29
K = [[9, 4], [5, 7]]
C = (23, 12)


def inv_search(a, p):
    hits = [b for b in range(p) if a * b % p == 1]
    return hits[0] if len(hits) == 1 else None


def matmul(A, B, p):
    return [[sum(A[i][t] * B[t][j] for t in range(2)) % p for j in range(2)] for i in range(2)]


I2 = [[1, 0], [0, 1]]
# the inverse by search over all 29^4 matrices is slow; search each row instead: row r of Kinv solves r K = e_r
Kinv = []
for e in ((1, 0), (0, 1)):
    sols = [(a, b) for a in range(P) for b in range(P)
            if ((a * K[0][0] + b * K[1][0]) % P, (a * K[0][1] + b * K[1][1]) % P) == e]
    check('cipher: each row of the inverse is unique', len(sols) == 1)
    Kinv.append(list(sols[0]))
check('cipher: K Kinv = I and Kinv K = I', matmul(K, Kinv, P) == I2 and matmul(Kinv, K, P) == I2)
check('cipher: Kinv is (15 8; 10 11)', Kinv == [[15, 8], [10, 11]], str(Kinv))

det = (9 * 7 - 4 * 5) % P
numeric_shape('p-cipher-29', 2, det, {'added': (9 * 7 + 4 * 5) % P, 'reversed': (4 * 5 - 9 * 7) % P})
check('cipher: 63 - 20 = 43 = 29 + 14', 9 * 7 == 63 and 4 * 5 == 20 and 43 - 29 == 14 and 63 + 20 == 83 and 83 % P == 25)
has('p-cipher-29', 2, '63 - 20 = 43', '83 \\equiv 25', '-43 \\equiv 15')

dinv = inv_search(det, P)
numeric_shape('p-cipher-29', 3, dinv, {'from-added': inv_search(25, P), 'sign': (-dinv) % P})
check('cipher: 14 * 27 = 378 = 13 * 29 + 1', 14 * 27 == 378 == 13 * 29 + 1 and 29 == 2 * 14 + 1 and 14 * 2 == 28)
check('cipher: 2 is also the inverse of 15, the reversed determinant', inv_search(15, P) == 2)
has('p-cipher-29', 3, '14 \\cdot 27 = 378 = 13 \\cdot 29 + 1', '29 = 2 \\cdot 14 + 1')

numeric_shape('p-cipher-29', 4, Kinv[1][0],
              {'sign': 27 * 5 % P, 'swapped': 27 * (-4) % P, 'unscaled': (-5) % P})
check('cipher: sign slip two ways', 27 * 5 % P == (2 * -5) % P == 19)
check('cipher: -135 + 145 = 10', 27 * -5 == -135 and 5 * 29 == 145 and -135 + 145 == 10)
check('cipher: part 5 stem row (10, 11)', Kinv[1] == [10, 11] and '(10, 11)' in part('p-cipher-29', 5)['question'])

plain = [(p1, p2) for p1 in range(P) for p2 in range(P)
         if ((9 * p1 + 4 * p2) % P, (5 * p1 + 7 * p2) % P) == C]
check('cipher: one plaintext pair codes to (23, 12)', plain == [(6, 14)], str(plain))
numeric_shape('p-cipher-29', 5, plain[0][1],
              {'used-K': (5 * 23 + 7 * 12) % P, 'column': (23 * Kinv[0][1] + 12 * Kinv[1][1]) % P,
               'from-19': (19 * 23 + 11 * 12) % P})
check('cipher: 362, 441, 569 and their residues',
      10 * 23 + 11 * 12 == 362 == 12 * 29 + 14 and 15 * 23 + 8 * 12 == 441 and 441 % P == 6
      and 19 * 23 + 11 * 12 == 569 and 230 + 132 == 362)
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
check('cipher: 6 and 14 read GO', ALPHA[6] + ALPHA[14] == 'GO')
has('p-cipher-29', 5, '441 \\equiv 6', '362 = 12 \\cdot 29 + 14', 'GO')

# part 1 claims
opts = {o['id']: o for o in part('p-cipher-29', 1)['widget']['options']}
check('cipher part 1: key is det', [i for i, o in opts.items() if o.get('correct')] == ['det'])
# det criterion checked on a smaller field by brute force (all of M_2(Z_5)): unit exactly when det is non-zero
Q = 5
ok = True
mats = [[[a, b], [c, d]] for a, b, c, d in product(range(Q), repeat=4)]
for M in mats:
    d5 = (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % Q
    adj = [[M[1][1], -M[0][1] % Q], [-M[1][0] % Q, M[0][0]]]
    is_unit = d5 != 0 and matmul(M, [[x * inv_search(d5, Q) % Q for x in r] for r in adj], Q) == I2
    if (d5 != 0) != is_unit:
        ok = False
    if d5 == 0 and matmul(M, adj, Q) != [[0, 0], [0, 0]]:
        ok = False
check('claim: over Z_5 a 2 by 2 matrix is a unit exactly when det is non-zero (625 matrices)', ok)
centre = [M for M in mats if all(matmul(M, N, Q) == matmul(N, M, Q) for N in mats)]
check('claim: only multiples of I commute with every matrix (Z_5)', len(centre) == Q and all(M[0][1] == M[1][0] == 0 and M[0][0] == M[1][1] for M in centre))
check('claim: (1 1; 1 1) has determinant 0', 1 * 1 - 1 * 1 == 0)
check('claim: (1 0; 0 0)(0 0; 0 1) = 0', matmul([[1, 0], [0, 0]], [[0, 0], [0, 1]], P) == [[0, 0], [0, 0]])
check('claim for the fix of finding 3: (0 1; 0 0)^2 = 0', matmul([[0, 1], [0, 0]], [[0, 1], [0, 0]], P) == [[0, 0], [0, 0]])
L14 = json.loads((ROOT / 'app/content/courses/algebra/l14-rings.json').read_text())
canvas = json.dumps(L14['screens'][6].get('canvas', {}))
check('reuse: the zero-divisor pair of part 1 "field" is not the l14 screens[6] canvas pair (finding 3)',
      not ('[[1, 0], [0, 0]]' in canvas and '[[0, 0], [0, 1]]' in canvas
           and '1&0\\\\0&0' in opts['field']['why'] and '0&0\\\\0&1' in opts['field']['why']))

# ---------------------------------------------------------- p-sixteen-factorial
p = 17
roots = [a for a in range(p) if (pow(a, 16, p) - 1) % p == 0]
numeric_shape('p-sixteen-factorial', 1, len(roots), {'with-zero': p, 'real': 2})
check('factorial: roots are 1 to 16 and f(0) = -1', roots == list(range(1, 17)) and (0 ** 16 - 1) == -1)


def polymul(f, g, m):
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] = (out[i + j] + a * b) % m
    return out


prod_poly = [1]
for a in range(1, 17):
    prod_poly = polymul(prod_poly, [(-a) % p, 1], p)
target = [(-1) % p] + [0] * 15 + [1]
check('factorial: (x-1)...(x-16) = x^16 - 1 in Z_17[x]', prod_poly == target)
fact = 1
facts = {}
for a in range(1, 17):
    fact *= a
    facts[a] = fact
numeric_shape('p-sixteen-factorial', 3, facts[16] % p, {'plus-one': 1})
check('factorial: 16! is 20922789888000', facts[16] == 20922789888000)
numeric_shape('p-sixteen-factorial', 4, facts[15] % p, {'kept': facts[16] % p})
numeric_shape('p-sixteen-factorial', 5, facts[14] % p, {'sign': (-inv_search(15, p)) % p, 'times': 1 * 15 % p})
check('factorial: 15 * 8 = 120 = 7 * 17 + 1, 2^-1 = 9, 16 * 15^-1 = 9',
      15 * 8 == 120 == 7 * 17 + 1 and inv_search(2, p) == 9 and 16 * inv_search(15, p) % p == 9
      and inv_search(16, p) == 16 and (-2 * 8) % p == 1)
has('p-sixteen-factorial', 5, '15 \\cdot 8 = 120 = 7 \\cdot 17 + 1', '2^{-1} = 9')
o2 = {o['id']: o for o in part('p-sixteen-factorial', 2)['widget']['options']}
check('factorial part 2: key is peel', [i for i, o in o2.items() if o.get('correct')] == ['peel'])
check('claim: x^2 + 1 has no root in Z_3', not [a for a in range(3) if (a * a + 1) % 3 == 0])
check('claim for the fix of finding 2: x^2 - 3 has no root in Z_17', not [a for a in range(p) if (a * a - 3) % p == 0])
# peel: after dividing by (x - 1) the quotient still vanishes at 2..16
q = [1]
for a in range(2, 17):
    q = polymul(q, [(-a) % p, 1], p)
check('claim: f / (x - 1) is x^15 + ... + 1 and vanishes at 2 to 16', q == [1] * 16 and all(sum(pow(b, i, p) for i in range(16)) % p == 0 for b in range(2, 17)))
L17 = json.loads((ROOT / 'app/content/courses/algebra/l17-roots-and-factors.json').read_text())
lesson = L17['screens'][3]['explain']['text']
mine = part('p-sixteen-factorial', 2)['explain']['text']
check('reuse: part 2 explain does not retell the l17 screens[3] explain (finding 2)',
      not ('(b - a)q(b) = 0' in lesson and re.search(r'0 = f\(b\) = \(b - 1\)g\(b\)', mine)))

# ---------------------------------------------------------- p-three-year-return
f = [-5, -1, -6, 8]          # lowest degree first


def ev(poly, x):
    return sum(Fr(c) * x ** i for i, c in enumerate(poly))


div5 = [d for d in range(1, 6) if 5 % d == 0]
div8 = [d for d in range(1, 9) if 8 % d == 0]
cands = sorted({Fr(u, v) for u in div5 for v in div8})
numeric_shape('p-three-year-return', 1, len(cands), {'with-negatives': 2 * len(cands), 'added': len(div5) + len(div8)})
check('return: 6 is also the count without the whole numbers 1 and 5 (finding 4)',
      len([c for c in cands if c.denominator != 1]) != wrongs('p-three-year-return', 1).get('added')
      or 'whole numbers included' in part('p-three-year-return', 1)['question'])
rts = [c for c in cands + [-c for c in cands] if ev(f, c) == 0]
check('return: 5/4 is the only rational root', rts == [Fr(5, 4)])
w2 = part('p-three-year-return', 2)['widget']
check('return part 2 key 0.25, unit %, over100', w2['answer'] == float(rts[0] - 1) and w2.get('unit') == '%' and w2.get('over100') is True)
w2w = wrongs('p-three-year-return', 2)
check('return part 2 wrongs', w2w == {'gave-x': 1.25, 'discount': float(1 - 1 / rts[0])}, str(w2w))
check('return part 2 bands apart', all(abs(v - 0.25) > 2 * w2['tol']['abs'] for v in w2w.values()))
check('return: cash flows value to 8 at 25%', Fr(6) / Fr(5, 4) + Fr(1) / Fr(5, 4) ** 2 + Fr(5) / Fr(5, 4) ** 3 == 8
      and Fr(6) / Fr(5, 4) == Fr(24, 5) and 1 / Fr(5, 4) ** 2 == Fr(16, 25) and 5 / Fr(5, 4) ** 3 == Fr(64, 25))
check('return: break-even equation is the stated cubic', all(8 * x ** 3 - (6 * x ** 2 + x + 5) == ev(f, x) for x in (Fr(1), Fr(5, 4), Fr(7, 3))))
check('return: f(5/4) terms 125/8 - 75/8 - 10/8 - 40/8', 8 * Fr(5, 4) ** 3 == Fr(125, 8) and 6 * Fr(5, 4) ** 2 == Fr(75, 8) and Fr(5, 4) == Fr(10, 8) and 5 == Fr(40, 8))
has('p-three-year-return', 2, '4.8 + 0.64 + 2.56 = 8')
# long division by 4x - 5, steps typed out
rem = [Fr(c) for c in f]
quo = [Fr(0)] * 3
steps = []
for d in (2, 1, 0):
    c = rem[d + 1] / 4
    quo[d] = c
    rem[d + 1] -= 4 * c
    rem[d] -= -5 * c
    steps.append([int(x) for x in rem])
check('return: quotient 2x^2 + x + 1, remainder 0', quo == [1, 1, 2] and not any(rem))
check('return: division leaves 4x^2 - x - 5, then 4x - 5, then 0', steps == [[-5, -1, 4, 0], [-5, 4, 0, 0], [0, 0, 0, 0]])
w3 = part('p-three-year-return', 3)['widget']
check('return part 3 key text', w3['answer'].replace(' ', '') == '2x^2+x+1' and w3['wrong'][0]['tex'] == '8x^2+4x+4')
check('return: quotient by x - 5/4 is 8x^2 + 4x + 4', [4 * c for c in quo] == [4, 4, 8])
check('return part 3: the stem shows an expression equal to the key, so the widget needs a form (finding 1)', 'form' in w3)
disc = 1 * 1 - 4 * 2 * 1
check('return: discriminant -7', disc == -7 and '-7' in text('p-three-year-return', 4))
# real roots by sign changes on a fine exact grid, and by the derivative: f' = 24x^2 - 12x - 1
grid = [Fr(i, 1000) for i in range(-20000, 20001)]
signs = [ev(f, x) for x in grid]
nz = [v for v in signs if v != 0]
changes = sum(1 for a, b in zip(nz, nz[1:]) if (a < 0) != (b < 0))
check('return: the one sign change is at the exact zero 5/4', [x for x, v in zip(grid, signs) if v == 0] == [Fr(5, 4)])
numeric_shape('p-three-year-return', 4, changes, {'cubic': 3})
check('return: 2x^2 + x + 1 is at least 7/8', min(2 * x * x + x + 1 for x in grid) >= Fr(7, 8))

# ------------------------------------------------------------------ set shape
check('set: 3 problems, 14 parts', len(SET['items']) == 3 and sum(len(i['parts']) for i in SET['items']) == 14)
course = json.loads((ROOT / 'app/content/courses/algebra/course.json').read_text())
lv = next(l for l in course['levels'] if l['n'] == 4)
lesson_skills = set()
for lid in lv['lessons']:
    L = json.loads((ROOT / f'app/content/courses/algebra/{lid}.json').read_text())
    for blk in L.get('screens', []) + L.get('quiz', []):
        lesson_skills.update(blk.get('skills', []))
    lesson_skills.update(L.get('skills', []))
for it in SET['items']:
    check(f"set: skills of {it['id']} are carried by level 4", not lesson_skills or set(it['skills']) <= lesson_skills, str(it['skills']))
    check(f"set: {it['id']} difficulty 3 to 5", 3 <= it['difficulty'] <= 5)
    for k, pt in enumerate(it['parts'][1:], start=2):
        if it['parts'][k - 2]['widget']['kind'] == 'choice' and it['id'] == 'p-cipher-29':
            continue   # part 2 computes det K from the prose; part 1 is the judgement it serves
        check(f"chain: {it['id']} part {k} restates part {k - 1}", f'from part {k - 1}' in pt['question'])
check('set: one difficulty 5', any(i['difficulty'] == 5 for i in SET['items']))
typed = sum(1 for i in SET['items'] for q in i['parts'] if q['widget']['kind'] in ('numeric', 'expression'))
check('set: typed parts at least two thirds', typed * 3 >= 14 * 2, str(typed))

print(f'{n_checks} checks, {n_find} FINDING line(s)')
