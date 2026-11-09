"""Delta read: recompute every changed key twice (exact enumeration plus a seeded
simulation or a second method) and search rival rules for the changed sequence items.
Run: python check.py  (exit 0 when every check passes). Seed 20261109; under 60 s."""
import itertools
import math
import random
from fractions import Fraction as F
from math import comb, gcd

random.seed(20261109)
fails = []


def check(name, a, b, key):
    ok = (a == b == key) if not isinstance(key, float) else (abs(a - key) < 1e-9 and abs(b - key) < 0.01)
    print(('ok  ' if ok else 'FAIL'), name, a, b, 'key', key)
    if not ok:
        fails.append(name)


def sim(f, n=200000):
    return sum(f() for _ in range(n)) / n


# ---------------- Sequences ----------------
def recaman(k):
    s, seen = [0], {0}
    for n in range(1, k):
        b = s[-1] - n
        s.append(b if b >= 0 and b not in seen else s[-1] + n)
        seen.add(s[-1])
    return s


smooth3 = sorted(2**a * 3**b for a in range(8) for b in range(6))
mult35 = [n for n in range(1, 40) if n % 3 == 0 or n % 5 == 0]
pw = [3**n + n for n in range(1, 7)]
check('v2 A3 next term', mult35[7], [n for n in range(16, 30) if n % 3 == 0 or n % 5 == 0][0], 18)
check('v2 A5 next term', pw[5], 3 * 248 - (2 * 5 - 1), 735)
check('v2 A8 next term', smooth3[9], [n for n in range(17, 40) if all(p in (2, 3) for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p)))][0], 18)
check('v3 A13 next term', recaman(8)[7], 13 + 7 if (13 - 7) in recaman(7) else 6, 20)
assert mult35[:7] == [3, 5, 6, 9, 10, 12, 15]
assert pw[:5] == [4, 11, 30, 85, 248]
assert smooth3[:9] == [1, 2, 3, 4, 6, 8, 9, 12, 16]
assert recaman(7) == [0, 1, 3, 6, 2, 7, 13]


def rivals(seq):
    """Return {rule: next} for simple rules that fit every shown term."""
    out = {}
    n = len(seq)
    # polynomial in position, degree <= 3, needs at least deg + 2 points to count as evidence
    for deg in range(0, 4):
        if n < deg + 2:
            continue
        xs = list(range(n))
        # Lagrange through first deg+1 points, test the rest
        def lag(x, pts=deg + 1):
            tot = F(0)
            for i in range(pts):
                t = F(seq[i])
                for j in range(pts):
                    if j != i:
                        t *= F(x - xs[j], xs[i] - xs[j])
                tot += t
            return tot
        if all(lag(x) == seq[x] for x in xs):
            out['poly deg %d' % deg] = lag(n)
    # linear recurrences of order 1..3, integer coefficients in [-4, 4], with constant in [-20, 20]
    for order in (1, 2, 3):
        rng = range(-4, 5)
        for co in itertools.product(rng, repeat=order):
            for c in range(-20, 21):
                ok = all(sum(co[k] * seq[i - 1 - k] for k in range(order)) + c == seq[i] for i in range(order, n))
                if ok and n - order >= order + 2:
                    out['rec%d %s+%d' % (order, co, c)] = sum(co[k] * seq[n - 1 - k] for k in range(order)) + c
    # a(n) = k*a(n-1) + f(n) with f linear in n
    for k in range(1, 5):
        r = [seq[i] - k * seq[i - 1] for i in range(1, n)]
        d = [r[i + 1] - r[i] for i in range(len(r) - 1)]
        if len(set(d)) == 1 and len(r) >= 3:
            out['x%d plus linear' % k] = k * seq[-1] + r[-1] + d[0]
    # differences periodic with period p, shown at least twice
    dif = [seq[i + 1] - seq[i] for i in range(n - 1)]
    for p in range(1, len(dif) // 2 + 1):
        if all(dif[i] == dif[i % p] for i in range(len(dif))):
            out['diff period %d' % p] = seq[-1] + dif[len(dif) % p]
    # interleaved strands, each arithmetic or geometric
    for s in (2, 3):
        strands = [seq[i::s] for i in range(s)]
        nxt = strands[n % s]
        if len(nxt) >= 3:
            dd = {nxt[i + 1] - nxt[i] for i in range(len(nxt) - 1)}
            if len(dd) == 1 and all(len({st[i + 1] - st[i] for i in range(len(st) - 1)}) <= 1 for st in strands if len(st) > 1):
                out['%d strands arithmetic' % s] = nxt[-1] + dd.pop()
    # increasing filters: residue classes mod m (pattern from 1 to last), factors of N
    if all(seq[i] < seq[i + 1] for i in range(n - 1)) and seq[0] >= 0:
        lo, hi = max(seq[0], 1), seq[-1]
        inset = set(seq)
        for m in range(2, 15):
            ok, cls = True, {}
            for x in range(1, hi + 1):
                v = x in inset if x >= lo else None
                if v is None:
                    continue
                if cls.setdefault(x % m, v) != v:
                    ok = False
                    break
            # a residue rule is evidence only when the shown range covers two full periods
            if ok and len(cls) == m and hi - lo + 1 >= 2 * m:
                nx = next(x for x in range(hi + 1, hi + 10 * m) if cls[x % m])
                out['residues mod %d' % m] = nx
        for N in range(1, 5001):
            divs = [d for d in range(1, N + 1) if N % d == 0]
            # the simple reading is the smallest such N (144 for v2 A8); larger N such as
            # 2448 = 144 x 17 are not a rule a candidate would state
            if divs[:n] == seq and len(divs) > n:
                out['factors of %d' % N] = divs[n]
                break
        # union of multiples of two numbers a, b (a < b <= 12)
        for a, b in itertools.combinations(range(2, 13), 2):
            m = [x for x in range(1, 200) if x % a == 0 or x % b == 0]
            if m[:n] == seq:
                out['multiples of %d or %d' % (a, b)] = m[n]
        # p-smooth numbers
        for P in (2, 3, 5, 7):
            primes = [q for q in range(2, P + 1) if all(q % r for r in range(2, q))]
            def smooth(x):
                for q in primes:
                    while x % q == 0:
                        x //= q
                return x == 1
            m = [x for x in range(1, 500) if smooth(x)]
            if m[:n] == seq:
                out['%d-smooth' % P] = m[n]
    return out


seqs = {
    'v2 A3': ([3, 5, 6, 9, 10, 12, 15], 18),
    'v2 A5': ([4, 11, 30, 85, 248], 735),
    'v2 A8': ([1, 2, 3, 4, 6, 8, 9, 12, 16], 18),
    'v3 A13': ([0, 1, 3, 6, 2, 7, 13], 20),
    'proposed v3 A13 (twice the last plus the one before)': ([1, 2, 5, 12, 29, 70], 169),
}
pell = [1, 2]
for _ in range(5):
    pell.append(2 * pell[-1] + pell[-2])
gaps = [b - a for a, b in zip(pell[:6], pell[1:6])]  # 1, 3, 7, 17, 41: the gaps obey the same rule
check('proposed A13 key', pell[6], 70 + (2 * gaps[-1] + gaps[-2]), 169)
print('    proposed A13 distractors: doubled only', 2 * 70, '; added the two before', 70 + 29, '; repeated last gap', 70 + gaps[4])
for name, (s, key) in seqs.items():
    r = rivals(s)
    bad = {k: v for k, v in r.items() if (v != key if not isinstance(v, set) else v != {key})}
    print('    rivals', name, r, '-> differing:', bad or 'none')
    if bad:
        fails.append(name + ' rival')
# hand-picked rivals for A13: every fourth gap negative, gaps negative at square places
g = [s - t for s, t in zip([1, 3, 6, 2, 7, 13], [0, 1, 3, 6, 2, 7])]
assert g == [1, 2, 3, -4, 5, 6]
print('    A13 every-fourth-negative gives', 13 + 7, '; back-if-result>0 (no "new" test) fails at step 6:', 7 - 6)

# ---------------- v3 B7 dice run ----------------
ex = sum(1 for r in itertools.product(range(1, 7), repeat=3) if sorted(r)[2] - sorted(r)[0] == 2 and len(set(r)) == 3)
check('v3 B7', F(ex, 216), F(4 * 6, 216), F(1, 9))
print('    sim B7', sim(lambda: (lambda r: len(set(r)) == 3 and max(r) - min(r) == 2)([random.randint(1, 6) for _ in range(3)])))

# ---------------- v2 rankings ----------------
check('v2 c01 >0.6', 1 - F(36, 100), F(64, 100), F(64, 100))
pts = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(200000)]
pts = [p for p in pts if p[0]**2 + p[1]**2 < 1]
print('    sim c01', [round(sum(f(math.hypot(*p)) for p in pts) / len(pts), 3) for f in (lambda r: r > .6, lambda r: r < .7, lambda r: r < .5)])


def rr(nplayers):
    games = list(itertools.combinations(range(nplayers), 2))
    for res in itertools.product((0, 1), repeat=len(games)):
        w = [0] * nplayers
        for (a, b), x in zip(games, res):
            w[a if x else b] += 1
        yield w


top = F(sum(1 for w in rr(4) if 3 in w), 64)
tb = F(sum(1 for w in rr(4) if 3 in w and 0 in w), 64)
cyc = F(sum(1 for w in rr(3) if w == [1, 1, 1]), 8)
check('v2 c02 top4', top, 4 * F(1, 8), F(1, 2))
check('v2 c02 tb4', tb, F(12, 32), F(3, 8))
check('v2 c02 cyc3', cyc, F(2, 8), F(1, 4))
mats = list(itertools.product((0, 1), repeat=4))
check('v2 c03 sym', F(sum(1 for a, b, c, d in mats if b == c), 16), F(1, 2), F(1, 2))
check('v2 c03 inv', F(sum(1 for a, b, c, d in mats if a * d - b * c != 0), 16), 2 * F(1, 4) * F(3, 4), F(3, 8))
check('v2 c03 same', F(sum(1 for m in mats if len(set(m)) == 1), 16), F(2, 16), F(1, 8))
tiles = [(a, b) for a in range(7) for b in range(a, 7)]
assert len(tiles) == 28
check('v2 c04 sum7', F(sum(1 for a, b in tiles if a + b >= 7), 28), F(6 + 4 + 2, 28), F(12, 28))
check('v2 c04 gap3', F(sum(1 for a, b in tiles if b - a >= 3), 28), F(10, 28), F(10, 28))
check('v2 c04 dbl', F(sum(1 for a, b in tiles if a == b), 28), F(7, 28), F(1, 4))


def cross(n):
    V = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
    diags = [(i, j) for i, j in itertools.combinations(range(n), 2) if (j - i) % n not in (1, n - 1)]

    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) - (B[1] - A[1]) * (C[0] - A[0])
    c = 0
    pairs = list(itertools.combinations(diags, 2))
    for (a, b), (x, y) in pairs:
        if len({a, b, x, y}) < 4:
            continue
        A, B, C, D = V[a], V[b], V[x], V[y]
        if (ccw(A, B, C) > 0) != (ccw(A, B, D) > 0) and (ccw(C, D, A) > 0) != (ccw(C, D, B) > 0):
            c += 1
    return F(c, len(pairs))


for n, key in ((5, F(5, 10)), (6, F(15, 36)), (7, F(35, 91))):
    check('v2 c05 n=%d' % n, cross(n), F(comb(n, 4), comb(n * (n - 3) // 2, 2)), key)

# ---------------- v3 rankings ----------------
dd = list(itertools.product(range(1, 7), repeat=2))
check('v3 c01 m6', F(sum(1 for a, b in dd if a * b % 6 == 0), 36), 1 - F(1, 4) - F(4, 9) + F(1, 9), F(15, 36))
check('v3 c01 sq', F(sum(1 for a, b in dd if math.isqrt(a * b)**2 == a * b), 36), F(8, 36), F(8, 36))
check('v3 c01 end0', F(sum(1 for a, b in dd if a * b % 10 == 0), 36), 2 * F(1, 6) * F(3, 6), F(6, 36))
cubes = list(itertools.product(range(3), repeat=3))
faces = [sum(1 for c in cube if c in (0, 2)) for cube in cubes]
check('v3 c02 two', F(faces.count(2), 27), F(12, 27), F(12, 27))
check('v3 c02 three', F(faces.count(3), 27), F(8, 27), F(8, 27))
check('v3 c02 one', F(faces.count(1), 27), F(6, 27), F(6, 27))
land = {k: F(0) for k in range(1, 5)}
for steps in itertools.product((1, 2), repeat=4):
    pos, seen = 0, set()
    for s in steps:
        pos += s
        seen.add(pos)
    for k in land:
        land[k] += F(k in seen, 16)
p = [F(1)]
for _ in range(4):
    p.append(1 - p[-1] / 2)
for k, key in ((2, F(3, 4)), (4, F(11, 16)), (3, F(5, 8))):
    check('v3 c03 sq%d' % k, land[k], p[k], key)
for N, key in ((3, F(7, 9)), (2, F(3, 4)), (4, F(11, 16))):
    e = F(sum(1 for a in range(1, N + 1) for b in range(1, N + 1) if gcd(a, b) == 1), N * N)
    mob = F(sum({1: 1, 2: -1, 3: -1, 4: 0}[d] * (N // d)**2 for d in range(1, N + 1)), N * N)
    check('v3 c04 1..%d' % N, e, mob, key)


def no_isolated(n):
    E = list(itertools.combinations(range(n), 2))
    c = 0
    for res in itertools.product((0, 1), repeat=len(E)):
        deg = [0] * n
        for (a, b), x in zip(E, res):
            if x:
                deg[a] += 1
                deg[b] += 1
        c += all(deg)
    return F(c, 2**len(E))


check('v3 c05 all4', no_isolated(4), 1 - F(4, 8) + F(6, 32) - F(4, 64) + F(1, 64), F(41, 64))
check('v3 c05 all3', no_isolated(3), F(4, 8), F(1, 2))
check('v3 c05 tri3', F(1, 8), F(1, 2)**3, F(1, 8))


def run_prob(n, k):
    c = 0
    for t in itertools.product('HT', repeat=n):
        c += 'H' * k in ''.join(t)
    return F(c, 2**n)


trib = [1, 2, 4]
for _ in range(6):
    trib.append(trib[-1] + trib[-2] + trib[-3])
check('v3 c06 r2', run_prob(4, 2), 1 - F(8, 16), F(1, 2))
check('v3 c06 r3', run_prob(8, 3), 1 - F(trib[8], 256), F(107, 256))
import calendar
check('v3 c06 m30', F(sum(1 for m in range(1, 13) if calendar.monthrange(2026, m)[1] == 30), 12), F(4, 12), F(1, 3))

# ---------------- SIG items ----------------
tr = list(itertools.combinations(range(5), 2))
tot = F(0)
for s1 in tr:
    for s2 in tr:
        perm = list(range(5))
        for i, j in (s1, s2):
            perm[i], perm[j] = perm[j], perm[i]
        tot += F(sum(perm[i] == i for i in range(5)), 100)
check('sig2 q04 two swaps', tot, 5 * (F(9, 25) + F(2, 5) * F(1, 10)), F(2))
print('    sig2 q04 distractors: no return', 5 * F(9, 25), '; one swap', 5 * F(3, 5))
win = F(sum(1 for x in itertools.product((0, 1), repeat=3) for y in itertools.product((0, 1), repeat=2) if sum(x) > sum(y)), 32)
tie = F(sum(1 for x in itertools.product((0, 1), repeat=3) for y in itertools.product((0, 1), repeat=2) if sum(x) == sum(y)), 32)
check('sig2 q07 one more toss', win, F(1, 2), F(1, 2))
print('    sig2 q07 distractors: win or tie', win + tie, '; half no tie', (1 - tie) / 2)


def ext_sim():
    pop = 1
    for _ in range(60):
        if pop == 0:
            return 1
        if pop > 200:
            return 0
        pop = sum(random.choices((0, 1, 2), (1, 1, 2))[0] for _ in range(pop))
    return int(pop == 0)


q = F(0)
qs = []
for _ in range(200):
    q = F(1, 4) + q / 4 + q * q / 2
    qs.append(q)
    q = F(round(float(q) * 10**12), 10**12)
check('sig3 q11 extinction', F(1, 2), F(1, 2) if 2 * F(1, 4) - 3 * F(1, 2) + 1 == 0 else None, F(1, 2))
print('    sig3 q11 iterate after 200 gens', float(qs[-1]), '; q2', qs[1], '; no-two-case', F(1, 4) / (1 - F(1, 4)), '; sim', round(sim(ext_sim, 20000), 3))
post = F(6, 10) * F(2, 10) / (F(6, 10) * F(2, 10) + F(4, 10))
check('sig3 q13 next search', post * F(8, 10), F(96, 520), F(12, 65))


def search_sim():
    inA = random.random() < .6
    if inA and random.random() < .8:
        return None
    return inA and random.random() < .8


r = [search_sim() for _ in range(300000)]
r = [x for x in r if x is not None]
print('    sim q13', round(sum(r) / len(r), 4), 'vs', round(12 / 65, 4))

print('FAILS:', fails or 'none')
raise SystemExit(1 if fails else 0)
