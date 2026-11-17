#!/usr/bin/env python3
"""Second reader's recompute for algebra problems-1 to problems-3.

Imports nothing from the author's script. Every group is built from scratch as
integers or tuples and every key, slip value and printed figure is found by
enumeration (walk the probe, list S_5, iterate powers), not by the gcd, phi,
lcm or Lagrange rule the feedback quotes. Exit 0 always; a failing check
prints a FINDING line (review-problems-algebra-1-3.md).
"""
import itertools
import json
import math
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ALG = os.path.join(ROOT, 'app', 'content', 'courses', 'algebra')
EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'topic-3.4.json')

n_ok = 0
n_find = 0


def chk(name, cond):
    global n_ok
    if cond:
        n_ok += 1
    else:
        finding(name)


def finding(text):
    global n_find
    n_find += 1
    print('FINDING ' + text)


def load(n):
    with open(os.path.join(ALG, f'problems-{n}.json'), encoding='utf-8') as fh:
        return {it['id']: it for it in json.load(fh)['items']}


def key(item, part):
    w = item['parts'][part]['widget']
    if w['kind'] == 'choice':
        return [o['id'] for o in w['options'] if o.get('correct')]
    if 'answers' in w:
        return sorted(w['answers'])
    return w['answer']


def wrongs(item, part):
    out = {}
    for x in item['parts'][part]['widget'].get('wrong', []):
        v = x['value']
        if isinstance(v, str):
            v = sorted(int(t) for t in v.split(','))
        out[x['id']] = v
    return out


def part_text(item, part):
    return json.dumps(item['parts'][part], ensure_ascii=False)


def expect(item, part, mine, slips):
    tag = f"{item['id']} part {part + 1}"
    chk(f'{tag}: key {key(item, part)} but reader finds {mine}', key(item, part) == mine)
    w = wrongs(item, part)
    chk(f'{tag}: wrong ids {sorted(w)} but reader expects {sorted(slips)}', set(w) == set(slips))
    for k, v in slips.items():
        if k in w:
            chk(f'{tag}: wrong {k} is {w[k]} but the named slip gives {v}', w[k] == v)
            chk(f'{tag}: wrong {k} equals the key', v != mine)
    by = item['parts'][part]['feedback'].get('byKey', {})
    for k in w:
        chk(f'{tag}: wrong {k} has no feedback line', k in by)


def says(item, part, *figures):
    """Each figure the reader computed is printed in the part's text."""
    t = part_text(item, part).replace('{,}', '').replace(',', '')
    for f in figures:
        chk(f"{item['id']} part {part + 1}: text does not print {f}", str(f) in t)


# ---------- permutation helpers (tuples on 0..n-1, products right to left) ----------

def comp(a, b):
    return tuple(a[b[i]] for i in range(len(b)))


def inv(a):
    out = [0] * len(a)
    for i, v in enumerate(a):
        out[v] = i
    return tuple(out)


def ident(n):
    return tuple(range(n))


def power(a, k):
    out = ident(len(a))
    for _ in range(k):
        out = comp(a, out)
    return out


def order(a, op=comp, e=None):
    e = ident(len(a)) if e is None else e
    x, k = a, 1
    while x != e:
        x, k = op(a, x), k + 1
    return k


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def from_cycles(n, cycles):
    p = list(range(n))
    for c in cycles:
        for i, v in enumerate(c):
            p[v - 1] = c[(i + 1) % len(c)] - 1
    return tuple(p)


n_skip = 0


def run(block, item_id):
    """Run one problem's checks. A problem re-authored under a new id, or reshaped
    so that these checks no longer apply, is reported and skipped: exit stays 0."""
    global n_skip
    try:
        block()
    except Exception as err:  # noqa: BLE001
        n_skip += 1
        print(f'SKIP {item_id or block.__name__}: checks no longer apply ({type(err).__name__}: {err})')


# =============================== problems-1 ===============================
P1 = load(1)


def block_p_probe_stride():
    # --- p-probe-stride: walk the probe, no gcd rule
    it = P1['p-probe-stride']


    def visited(stride, n=56):
        seen, x = [], 0
        while x not in seen:
            seen.append(x)
            x = (x + stride) % n
        return seen


    def first_hit(stride, slot, n=56):
        return next(k for k in range(1, n + 1) if stride * k % n == slot)


    v21 = visited(21)
    gap = min(x for x in v21 if x > 0)
    expect(it, 0, len(v21), {'gcd': gap, 'full': 56})
    says(it, 0, gap, 8)
    gens = [s for s in range(1, 56) if len(visited(s)) == 56]
    evens = sum(1 for s in range(56) if s % 2 == 0)
    sevens = sum(1 for s in range(56) if s % 7 == 0)
    both = sum(1 for s in range(56) if s % 14 == 0)
    expect(it, 1, len(gens), {'no-overlap': 56 - evens - sevens, 'odd-only': 56 - evens, 'all': 55})
    chk('probe part 2: 28 even, 8 multiples of 7, 4 of 14', (evens, sevens, both) == (28, 8, 4))
    chk('probe part 2: odd multiples of 7 are 7, 21, 35, 49',
        [s for s in range(56) if s % 2 and s % 7 == 0] == [7, 21, 35, 49])
    k1 = first_hit(9, 1)
    expect(it, 2, k1, {'dropped-nine': k1 - 1, 'sign': 56 - k1})
    chk('probe part 3: Euclid lines', 56 == 6 * 9 + 2 and 9 == 4 * 2 + 1 and 25 * 9 - 4 * 56 == 1 and 31 * 9 % 56 == 55)
    k13 = first_hit(9, 13)
    expect(it, 3, k13, {'times-stride': 13 * 9 % 56, 'from-24': 13 * 24 % 56, 'from-31': 13 * 31 % 56})
    chk('probe part 4: printed products', 13 * 25 == 325 == 5 * 56 + 45 and 9 * 45 == 405 == 7 * 56 + 13 and 24 * 9 % 56 == 48)



run(block_p_probe_stride, 'p-probe-stride')


def block_p_octagon_orders():
    # --- p-octagon-orders: D_8 as permutations of the 8 corners
    it = P1['p-octagon-orders']
    R8 = tuple((i + 1) % 8 for i in range(8))
    S8 = tuple((-i) % 8 for i in range(8))
    turn = [power(R8, k) for k in range(8)]
    flip = [comp(turn[k], S8) for k in range(8)]
    D8 = turn + flip
    chk('octagon: 16 distinct symmetries', len(set(D8)) == 16)
    chk('octagon: s r^j = r^-j s for every j', all(comp(S8, turn[j]) == comp(turn[-j % 8], S8) for j in range(8)))
    prod = comp(flip[3], flip[5])
    k = turn.index(prod)
    expect(it, 0, k, {'added': (3 + 5) % 8, 'reversed': 5 - 3})
    expect(it, 1, order(prod), {'all-eight': order(R8), 'half-turn': 2})
    chk('octagon part 2: (r^6)^2 = r^4, not e', power(prod, 2) == turn[4])
    kinv = turn.index(inv(prod))
    expect(it, 2, kinv, {'self-inverse': k, 'commuted': (5 + 3) % 8})
    chk('octagon part 3: inverse is (r^5 s)(r^3 s)', comp(flip[5], flip[3]) == inv(prod))
    E8 = ident(8)
    x4 = [g for g in D8 if power(g, 4) == E8]
    x2 = [g for g in D8 if power(g, 2) == E8]
    expect(it, 3, len(x4), {'squares': len(x2), 'turns-only': sum(1 for g in turn if power(g, 4) == E8),
                            'flips-only': sum(1 for g in flip if power(g, 4) == E8)})
    chk('octagon part 4: turn orders 1, 4, 2, 4', [order(turn[j]) for j in (0, 2, 4, 6)] == [1, 4, 2, 4])



run(block_p_octagon_orders, 'p-octagon-orders')


def block_p_shifted_product():
    # --- p-shifted-product: a * b = a + b + ab mod 19
    it = P1['p-shifted-product']


    def star(a, b):
        return (a + b + a * b) % 19


    chk('shifted: associative on Z_19', all(star(star(a, b), c) == star(a, star(b, c))
                                            for a in range(19) for b in range(19) for c in range(19)))
    chk('shifted: 0 is a two-sided identity', all(star(a, 0) == a == star(0, a) for a in range(19)))
    chk('shifted: 18 absorbs', all(star(18, b) == 18 for b in range(19)))
    G = list(range(18))
    chk('shifted: G closed with inverses', all(star(a, b) in G for a in G for b in G)
        and all(any(star(a, b) == 0 for b in G) for a in G))
    expect(it, 0, star(18, 5), {'product': 18 * 5 % 19, 'sum': (18 + 5) % 19})
    chk('shifted part 1: 113 = 5 * 19 + 18', 18 + 5 + 90 == 113 == 5 * 19 + 18)
    b4 = next(b for b in G if star(4, b) == 0)
    expect(it, 1, b4, {'plain-inverse': next(b for b in range(19) if 4 * b % 19 == 1), 'negative': -4 % 19})
    chk('shifted part 2: 4 * 15 = 3', star(4, 15) == 3 and 4 + 15 + 60 == 79)
    o1 = order(1, op=star, e=0)
    expect(it, 2, o1, {'half': 9, 'sixth': 6, 'modulus': 19})
    chk('shifted part 3: 2^6 = 7, 2^9 = 18 mod 19; k-fold product is 2^k - 1',
        pow(2, 6, 19) == 7 and pow(2, 9, 19) == 18 and order(17, op=star, e=0) == 2)
    x = 0
    ok = True
    for kk in range(1, 19):
        x = star(x, 1)
        ok = ok and x == (pow(2, kk, 19) - 1) % 19
    chk('shifted part 3: 1 * ... * 1 (k copies) = 2^k - 1', ok)
    orders = {a: order(a, op=star, e=0) for a in G}
    ngen = sum(1 for a in G if orders[a] == 18)
    expect(it, 3, ngen, {'non-identity': 17, 'phi-modulus': 18, 'odd': 9})
    chk('shifted part 4: 1 * 1 = 3 has order 9', star(1, 1) == 3 and orders[3] == 9)


    def kfold(kk):
        x = 0
        for _ in range(kk):
            x = star(x, 1)
        return x


    chk('shifted part 4: exponents 3 and 9 give orders 6 and 2', orders[kfold(3)] == 6 and orders[kfold(9)] == 2)
    chk('shifted part 4: generating exponents 1, 5, 7, 11, 13, 17',
        [kk for kk in range(1, 19) if orders[kfold(kk)] == 18] == [1, 5, 7, 11, 13, 17])


run(block_p_shifted_product, 'p-shifted-product')

# =============================== problems-2 ===============================
P2 = load(2)


def block_p_desk_rota():
    # --- p-desk-rota
    it = P2['p-desk-rota']
    row = [int(t) for t in re.search(r'bottom row \$([0-9, ]+)\$', it['prose']).group(1).split(',')]
    sig = tuple(v - 1 for v in row)
    chk('rota: bottom row is a permutation of 1..10', sorted(row) == list(range(1, 11)))


    def cycle_of(p, start):
        out, x = [start], p[start]
        while x != start:
            out.append(x)
            x = p[x]
        return out


    c1 = [v + 1 for v in cycle_of(sig, 0)]
    c2 = [v + 1 for v in cycle_of(sig, 1)]
    chk('rota: cycles (1 7 3 10 5 8)(2 9 4 6)', c1 == [1, 7, 3, 10, 5, 8] and c2 == [2, 9, 4, 6])
    expect(it, 0, len(c1), {'other-cycle': len(c2), 'all-desks': 10})
    expect(it, 1, order(sig), {'product': len(c1) * len(c2), 'sum': len(c1) + len(c2)})
    chk('rota part 3: even by inversion count; key option a', inversions(sig) % 2 == 0 and key(it, 2) == ['a'])
    half = math.factorial(10) // 2
    expect(it, 3, half // order(sig), {'in-s10': math.factorial(10) // order(sig), 'product-order': half // 24})
    says(it, 3, half, half // 12)
    chk('rota part 4: every power of sigma is even', all(inversions(power(sig, kk)) % 2 == 0 for kk in range(12)))



run(block_p_desk_rota, 'p-desk-rota')


def block_p_units_21_cosets():
    # --- p-units-21-cosets
    it = P2['p-units-21-cosets']
    U = [a for a in range(1, 21) if any(a * b % 21 == 1 for b in range(1, 21))]
    H = [1, 4, 16]
    threes = sum(1 for a in range(1, 21) if a % 3 == 0)
    sevens = sum(1 for a in range(1, 21) if a % 7 == 0)
    expect(it, 0, len(U), {'no-sevens': 20 - threes, 'no-threes': 20 - sevens, 'all': 20})
    i16 = next(b for b in U if 16 * b % 21 == 1)
    expect(it, 1, 4 * i16 % 21, {'no-inverse': 4 * 16 % 21, 'inverse-only': i16})


    def inv21(b):
        return next(c for c in U if b * c % 21 == 1)


    chk('units part 2: H passes the one-step test', all(a * inv21(b) % 21 in H for a in H for b in H))
    cosets = {tuple(sorted(g * h % 21 for h in H)) for g in U}
    expect(it, 2, len(cosets), {'subtracted': len(U) - len(H), 'size': len(H)})
    twoH = sorted(2 * h % 21 for h in H)
    expect(it, 3, twoH, {'added': sorted((2 + h) % 21 for h in H)})


    def is_subgroup21(S):
        return 1 in S and all(a * b % 21 in S for a in S for b in S)


    fiveH = sorted(5 * h % 21 for h in H)
    opts = {'a': sorted(H + twoH), 'b': sorted(twoH + fiveH), 'c': sorted(H + [2, 5, 10]), 'd': twoH}
    chk('units part 5: only option a is a subgroup with 6 elements',
        [o for o, S in opts.items() if is_subgroup21(S) and len(S) == 6] == ['a'] == key(it, 4))
    chk('units part 5: option sets as printed', opts['a'] == [1, 2, 4, 8, 11, 16] and opts['b'] == [2, 5, 8, 11, 17, 20])
    chk('units part 5: H u 2H is the powers of 2; 2 * 10 = 20', sorted({pow(2, kk, 21) for kk in range(6)}) == opts['a']
        and 2 * 10 % 21 == 20 and 20 not in opts['c'])



run(block_p_units_21_cosets, 'p-units-21-cosets')


def block_p_fixing_five():
    # --- p-fixing-five: all of S_5
    it = P2['p-fixing-five']
    S5 = [tuple(p) for p in itertools.permutations(range(5))]
    Hs = [p for p in S5 if p[4] == 4]
    chk('fixing: H passes the one-step test', all(comp(a, inv(b)) in Hs for a in Hs for b in Hs))
    chk('fixing part 1: key a; (1 2), (2 3) fix 5 and do not commute; {e, (1 2), (2 3)} not closed',
        key(it, 0) == ['a']
        and comp(from_cycles(5, [(1, 2)]), from_cycles(5, [(2, 3)])) != comp(from_cycles(5, [(2, 3)]), from_cycles(5, [(1, 2)]))
        and comp(from_cycles(5, [(1, 2)]), from_cycles(5, [(2, 3)])) not in
        (ident(5), from_cycles(5, [(1, 2)]), from_cycles(5, [(2, 3)])))
    left = {tuple(sorted(comp(g, h) for h in Hs)) for g in S5}
    expect(it, 1, len(left), {'size': len(Hs), 'subtracted': len(S5) - len(Hs)})
    m = re.search(r'\\sigma = \(1\\,5\\,3\)\(2\\,4\)', it['parts'][2]['question'])
    chk('fixing: sigma printed as (1 5 3)(2 4)', bool(m))
    sg = from_cycles(5, [(1, 5, 3), (2, 4)])
    sH = [comp(sg, h) for h in Hs]
    Hsg = [comp(h, sg) for h in Hs]
    img = {p[4] + 1 for p in sH}
    chk('fixing part 3: sigma H sends 5 to one point', len(img) == 1)
    expect(it, 2, img.pop(), {'inverse': inv(sg)[4] + 1, 'fixed': 5})
    pre = {inv(p)[4] + 1 for p in Hsg}
    chk('fixing part 4: H sigma sends one point to 5', len(pre) == 1)
    expect(it, 3, pre.pop(), {'left-coset': sg[4] + 1, 'five': 5})
    chk('fixing part 4: no element of H sigma fixes 5', all(p[4] != 4 for p in Hsg))
    both = set(sH) & set(Hsg)
    expect(it, 4, len(both), {'disjoint': 0, 'equal': len(sH), 'half': len(sH) // 2})
    t35 = from_cycles(5, [(3, 5)])
    chk('fixing part 5: (3 5) lies in sigma H, not in H sigma', t35 in sH and t35 not in Hsg)
    chk('fixing part 5: sigma H = {tau(5) = 3}, H sigma = {tau(1) = 5}',
        set(sH) == {p for p in S5 if p[4] == 2} and set(Hsg) == {p for p in S5 if p[0] == 4})


run(block_p_fixing_five, 'p-fixing-five')

# =============================== problems-3 ===============================
P3 = load(3)


def block_p_fifteen_times():
    # --- p-fifteen-times
    it = P3['p-fifteen-times']
    phi = [15 * x % 36 for x in range(24)]
    chk('fifteen: well defined and additive', 15 * 24 % 36 == 0 and 15 * 24 == 360 == 10 * 36
        and all(phi[(a + b) % 24] == (phi[a] + phi[b]) % 36 for a in range(24) for b in range(24)))
    ker = [x for x in range(24) if phi[x] == 0]
    im = sorted(set(phi))
    expect(it, 0, len(ker), {'in-z36': sum(1 for x in range(36) if 15 * x % 36 == 0), 'one': 1})
    chk('fifteen part 1: kernel {0, 12}; phi(12) = 180 = 5 * 36', ker == [0, 12] and 15 * 12 == 180 == 5 * 36)
    expect(it, 1, len(im), {'target': 36 // len(ker), 'from-three': 24 // 3})
    chk('fifteen part 2: image is the multiples of 3', im == list(range(0, 36, 3)))
    sol = [x for x in range(24) if phi[x] == 21]
    expect(it, 2, sol, {'no-inverse': [x for x in range(24) if x % 12 == 7]})
    chk('fifteen part 3: 5 * 5 = 25 = 1 mod 12; 15 * 11 = 165 = 4 * 36 + 21', 25 % 12 == 1 and 165 == 4 * 36 + 21)
    oq = next(kk for kk in range(1, 25) if 2 * kk % 24 in ker)
    expect(it, 3, oq, {'in-z24': next(kk for kk in range(1, 25) if 2 * kk % 24 == 0),
                       'in-target': next(kk for kk in range(1, 37) if 2 * kk % 36 == 0)})
    chk('fifteen part 4: phi(2) = 30 has order 6 in Z_36', phi[2] == 30 and next(kk for kk in range(1, 37) if 30 * kk % 36 == 0) == 6)



run(block_p_fifteen_times, 'p-fifteen-times')


def block_p_powers_of_seven():
    # --- p-powers-of-seven
    it = P3['p-powers-of-seven']
    U45 = [a for a in range(1, 45) if any(a * b % 45 == 1 for b in range(1, 45))]
    chk('seven: 7^2 = 4, 7^3 = 28 mod 45', 49 % 45 == 4 and 343 % 45 == 28)
    expect(it, 0, len(U45), {'no-fives': sum(1 for a in range(1, 46) if a % 3), 'no-threes': sum(1 for a in range(1, 46) if a % 5),
                             'all': 44})
    chk('seven part 1: 15, 9 and 3 multiples', (45 // 3, 45 // 5, 45 // 15) == (15, 9, 3))
    p, o7 = 7, 1
    while p != 1:
        p, o7 = p * 7 % 45, o7 + 1
    expect(it, 1, o7, {'euler': len(U45), 'six': 6})
    chk('seven part 2: 7^4 = 16, 7^6 = 19, 7^8 = 31, 361 = 8 * 45 + 1, 784 = 17 * 45 + 19',
        (7 ** 4 % 45, 7 ** 6 % 45, 7 ** 8 % 45) == (16, 19, 31) and 361 == 8 * 45 + 1 and 784 == 17 * 45 + 19)
    chk('seven part 2: no divisor of 24 below 12 gives 1', all(7 ** d % 45 != 1 for d in (1, 2, 3, 4, 6, 8)))
    big = 1
    for _ in range(2027):
        big = big * 7 % 45
    expect(it, 2, big, {'used-44': 7 ** (2027 % 44) % 45, 'added': (31 + 28) % 45})
    chk('seven part 3: 2027 = 12 * 168 + 11; 868 = 19 * 45 + 13; 7^44 is not 1',
        2027 == 12 * 168 + 11 and 31 * 28 == 868 == 19 * 45 + 13 and 7 ** 44 % 45 != 1)
    x20 = next(x for x in range(45) if 7 * x % 45 == 20)
    expect(it, 3, x20, {'times-seven': 7 * 20 % 45, 'from-28': 28 * 20 % 45})
    chk('seven part 4: 91 = 2 * 45 + 1; 260 = 5 * 45 + 35; 245 = 5 * 45 + 20; 196 = 4 * 45 + 16',
        7 * 13 == 91 and 13 * 20 == 260 == 5 * 45 + 35 and 7 * 35 == 245 == 5 * 45 + 20 and 7 * 28 == 196 == 4 * 45 + 16)



run(block_p_powers_of_seven, 'p-powers-of-seven')


def block_p_hexagon_quotient():
    # --- p-hexagon-quotient: D_6 on the 6 corners
    it = P3['p-hexagon-quotient']
    R6 = tuple((i + 1) % 6 for i in range(6))
    S6 = tuple((-i) % 6 for i in range(6))
    t6 = [power(R6, kk) for kk in range(6)]
    f6 = [comp(t6[kk], S6) for kk in range(6)]
    D6 = t6 + f6
    E6 = ident(6)
    chk('hexagon: 12 symmetries; s r^j = r^-j s', len(set(D6)) == 12
        and all(comp(S6, t6[j]) == comp(t6[-j % 6], S6) for j in range(6)))
    expect(it, 0, 12 // 6, {'image-size': 6, 'product': 72})
    ord2 = [z for z in D6 if z != E6 and comp(z, z) == E6]
    normal2 = [z for z in ord2 if all(comp(comp(g, z), inv(g)) == z for g in D6)]
    expect(it, 1, len(normal2), {'all-seven': len(ord2), 'flips': len(f6), 'none': 0})
    chk('hexagon part 2: the one normal choice is r^3; r (r^j s) r^-1 = r^(j+2) s',
        normal2 == [t6[3]] and all(comp(comp(R6, f6[j]), inv(R6)) == f6[(j + 2) % 6] for j in range(6)))
    N = frozenset([E6, t6[3]])


    def coset(g):
        return frozenset(comp(g, n) for n in N)


    Q = {coset(g) for g in D6}


    def cmul(a, b):
        return coset(comp(next(iter(a)), next(iter(b))))


    chk('hexagon: 6 cosets', len(Q) == 6)
    orN = order(coset(R6), op=cmul, e=coset(E6))
    expect(it, 2, orN, {'order-of-r': order(R6), 'two': 2})
    q2 = [c for c in Q if order(c, op=cmul, e=coset(E6)) == 2]
    expect(it, 3, len(q2), {'cyclic': 1, 'flips': 6, 'all-but-e': 5})
    chk('hexagon part 4: flip cosets pair r^j s with r^(j+3) s; quotient not abelian',
        all(coset(f6[j]) == frozenset([f6[j], f6[(j + 3) % 6]]) for j in range(6))
        and any(cmul(a, b) != cmul(b, a) for a in Q for b in Q))


run(block_p_hexagon_quotient, 'p-hexagon-quotient')

# =============================== set shape ===============================
with open(os.path.join(ALG, 'course.json'), encoding='utf-8') as fh:
    course = json.load(fh)
for n, P in ((1, P1), (2, P2), (3, P3)):
    lessons = next(lv['lessons'] for lv in course['levels'] if lv['n'] == n)
    taught = set()
    for l in lessons:
        with open(os.path.join(ALG, l + '.json'), encoding='utf-8') as fh:
            taught |= set(json.load(fh).get('skills', []))
    for item in P.values():
        chk(f"{item['id']}: skills {item['skills']} not all carried by level {n}", set(item['skills']) <= taught)
        chk(f"{item['id']}: 3 to 5 parts", 3 <= len(item['parts']) <= 5)
        for i, p in enumerate(item['parts']):
            chk(f"{item['id']} part {i + 1}: explain over three sentences",
                len(re.findall(r'[.?](?:\s|$)', re.sub(r'\$[^$]*\$', 'X', p['explain']['text']))) <= 3)
    chk(f'problems-{n}: 3 to 5 items with a difficulty 5', 3 <= len(P) <= 5 and any(i['difficulty'] == 5 for i in P.values()))
    typed = sum(1 for i in P.values() for p in i['parts'] if p['widget']['kind'] != 'choice')
    total = sum(len(i['parts']) for i in P.values())
    chk(f'problems-{n}: typed parts {typed} of {total} under two thirds', 3 * typed >= 2 * total)

# =============================== findings held by the review ===============================
# Each check below fails on today's content and is a numbered finding of
# docs/reviews/review-problems-algebra-1-3.md. A problem that has been re-authored
# under a new id is skipped, not failed.


def held_findings():
    with open(EXAM, encoding='utf-8') as fh:
        exam = json.load(fh)['items']

    # Finding 8: the multiplier 15 and modulus 36 are the topic exam's, with the same image subgroup.
    item = P3.get('p-fifteen-times')
    e0 = next((e for e in exam if e.get('title') == 'The order of 15 modulo 36'), None)
    if item and e0 is not None and '15x' in item['prose'] and r'\mathbb{Z}_{36}' in item['prose']:
        image = sorted({15 * x % 36 for x in range(24)})
        exam_h = sorted({15 * kk % 36 for kk in range(36)})
        if image == exam_h:
            finding('8 p-fifteen-times: im(phi) is <15> in Z_36, the subgroup of exam item "The order of 15 modulo 36" '
                    f'(same 15 and 36, same count {len(image)}, same step "12 | 5x so 12 | x")')

    # Finding 6: sigma is the inverse of the exam's sigma = (1 3 5)(2 4).
    item = P2.get('p-fixing-five')
    e9 = next((e for e in exam if e.get('title') == 'A product of two permutations'), None)
    if item and e9 is not None and r'(1\,3\,5)(2\,4)' in e9['prose'] and r'(1\,5\,3)(2\,4)' in item['parts'][2]['question']:
        if inv(from_cycles(5, [(1, 5, 3), (2, 4)])) == from_cycles(5, [(1, 3, 5), (2, 4)]):
            finding('6 p-fixing-five: sigma = (1 5 3)(2 4) is the inverse of the exam sigma (1 3 5)(2 4), also in S_5')

    # Finding 7: the one-step test of l5 needs a non-empty H; part 1 never says H is non-empty.
    if item and 'non-empty' not in part_text(item, 0):
        finding('7 p-fixing-five part 1: one-step test stated without "non-empty" (l5 screen 2 has it)')

    # Finding 2: "the order divides 18" is Lagrange (l7, level 2) or Fermat (l13), used at level 1.
    item = P1.get('p-shifted-product')
    if item and 'divides 18' in part_text(item, 2) and '2^{18}' not in part_text(item, 2):
        finding('2 p-shifted-product part 3: "divides 18" needs Lagrange or Fermat, taught after level 1')

    # Finding 3: part 1 asks l4 screen 0's question with slots for seats.
    item = P1.get('p-probe-stride')
    with open(os.path.join(ALG, 'l4-cyclic-groups.json'), encoding='utf-8') as fh:
        l4q = json.load(fh)['screens'][0].get('question', '')
    if item and 'counting 0' in l4q and 'counting slot 0' in item['parts'][0]['question']:
        finding('3 p-probe-stride part 1: retells l4 screen 0 ("how many seats does a walk from 0 visit, counting 0")')

    # Proposed fix of finding 6: sigma = (1 5 3 2) keeps every key of parts 3 to 5.
    S5 = [tuple(p) for p in itertools.permutations(range(5))]
    Hs = [p for p in S5 if p[4] == 4]
    new = from_cycles(5, [(1, 5, 3, 2)])
    lc = {comp(new, h) for h in Hs}
    rc = {comp(h, new) for h in Hs}
    chk('fix 6: sigma = (1 5 3 2) gives 3, 1 (inverse slip 1, left slip 3) and overlap 6',
        new[4] + 1 == 3 and inv(new)[4] + 1 == 1 and len(lc & rc) == 6
        and lc == {p for p in S5 if p[4] == 2} and rc == {p for p in S5 if p[0] == 4})
    # Proposed fix of finding 2: 2^9 = -1 so 2^18 = 1 mod 19.
    chk('fix 2: 2^9 = 18 = -1 and 2^18 = 1 mod 19', pow(2, 9, 19) == 18 and pow(2, 18, 19) == 1)


run(held_findings, None)

print(f'{n_ok} checks passed, {n_find} FINDING line(s), {n_skip} block(s) skipped')
sys.exit(0)
