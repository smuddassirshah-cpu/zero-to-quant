"""Recompute every number stated in app/content/exams/topic-3.4.json by a second route and assert it at its path.

Route A is build.py (closed forms, gcd formulas, the theorems). Route B here is independent: brute force over the
finite groups, rings and spaces (orders by repeated multiplication, kernels and images by listing, S_4 and S_6 by
enumerating every permutation, normality by conjugating with every element, irreducibility by trial division over
Z_3, topologies by testing every pair), permutations parsed from the cycle notation printed in the file, numerical
maxima on fine grids, Simpson integrals, fixed points by bisection, boundaries by sampling small balls.
A last pass reads every number in every learner-visible string of each item. Whole numbers 0 to 10 are taken as
structure (indices, exponents, "4 decimal places"); every other number must match a route-B value for that item
to its printed precision. Exits 1 on any failure.
Run: python3 docs/briefs/exam-3.4-scripts/check_numbers.py
"""
import itertools
import json
import math
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, _walk, normalise  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-3.4.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}
ALLOW = {}          # iid -> route-B values that may appear in its text


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def rec(ok, label):
    ex._rec(bool(ok), label, '')


def key(iid, value, part=None, tol=None):
    w = node(W(iid, part))
    t = tol if tol is not None else max(w['tol']['abs'] / 10, 1e-9)
    ok = abs(w['answer'] - value) <= t
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if ok else 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9)
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} wrong "{wid}" = {value!r}', '' if ok else f'found {hit}')
    allow(iid, value)


def wrong_ids(iid, want, part=None):
    w = node(W(iid, part))
    got = sorted(x['id'] for x in w.get('wrong', []))
    rec(got == sorted(want), f'{iid}{"" if part is None else f" part {part}"} wrong ids {got} = {sorted(want)}')
    fbk = node(P(iid, part) + '.feedback').get('byKey', {})
    rec(sorted(fbk) == sorted(want), f'{iid}{"" if part is None else f" part {part}"} byKey keys match the wrong ids')


def correct_id(iid, want, part=None):
    w = node(W(iid, part))
    got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    want = sorted(want if isinstance(want, list) else [want])
    rec(got == want, f'{iid}{"" if part is None else f" part {part}"} correct options {got} = {want}')
    rec(w.get('shuffle') is True, f'{iid}{"" if part is None else f" part {part}"} shuffle true')
    rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} every distractor has a why')
    if len(want) > 1:
        rec(w['kind'] == 'multi' and 'Select all that apply' in node(P(iid, part)).get('question', ''),
            f'{iid}: multi with "Select all that apply"')


def opt_text(iid, oid, part=None):
    return [o['text'] for o in node(W(iid, part))['options'] if o['id'] == oid][0]


def text_of(iid):
    return json.dumps(node(P(iid)), ensure_ascii=False)


# ------------------------------------------------------------------ helpers: permutations from printed cycles
def perm_from_cycles(s, n):
    """Parse '(1\\,3\\,5)(2\\,4)' (LaTeX thin spaces) into a dict on 1..n."""
    p = {k: k for k in range(1, n + 1)}
    for cyc in re.findall(r'\(([0-9\\, ]+)\)', s):
        pts = [int(t) for t in re.findall(r'\d+', cyc)]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            p[a] = b
    return p


def compose(a, b):          # a after b: do b, then a
    return {k: a[b[k]] for k in b}


def inverse(a):
    return {v: k for k, v in a.items()}


def perm_order(a):
    e = {k: k for k in a}
    cur, k = dict(a), 1
    while cur != e:
        cur, k = compose(a, cur), k + 1
    return k


def sign(a):
    keys = sorted(a)
    seq = [a[k] for k in keys]
    inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])
    return -1 if inv % 2 else 1


def cycles(a):
    seen, out = set(), []
    for k in sorted(a):
        if k in seen or a[k] == k:
            seen.add(k)
            continue
        c, x = [], k
        while x not in seen:
            seen.add(x)
            c.append(x)
            x = a[x]
        out.append(tuple(c))
    return out


def all_perms(n):
    return [dict(zip(range(1, n + 1), p)) for p in itertools.permutations(range(1, n + 1))]


def mul_order(a, n):
    x, k = a % n, 1
    while x != 1:
        x, k = x * a % n, k + 1
    return k


def power_mod(a, e, n):     # by repeated multiplication, not pow
    x = 1
    for _ in range(e):
        x = x * a % n
    return x


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def simpson(f, lo, hi, n=2000):
    h = (hi - lo) / n
    return h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(lo + k * h) for k in range(n + 1))


# ------------------------------------------------------------------ e-order-fifteen
iid = 'e-order-fifteen'
H = sorted({15 * k % 36 for k in range(36)})
ordB = next(k for k in range(1, 37) if 15 * k % 36 == 0)
cos_ = {frozenset((a + h) % 36 for h in H) for a in range(36)}
key(iid, ordB, 0)
wrong(iid, 'gcd', max(d for d in range(1, 16) if 15 % d == 0 and 36 % d == 0), 0)
wrong(iid, 'lcm', 15 * ordB, 0)
key(iid, len(cos_), 1)
wrong(iid, 'order', len(H), 1)
wrong_ids(iid, ['gcd', 'lcm'], 0)
wrong_ids(iid, ['order'], 1)
rec(H == list(range(0, 36, 3)) and len(H) == 12, f'{iid}: <15> is the multiples of 3, 12 of them')
rec(15 * ordB == 5 * 36 == 180, f'{iid}: 12 x 15 = 180 = 5 x 36')
rec(all(len(c) == 12 for c in cos_), f'{iid}: cosets are 3 pieces of 12')
allow(iid, 36, 15, 12, 180, 3)

# ------------------------------------------------------------------ e-cycles-bottom-row
iid = 'e-cycles-bottom-row'
row = [int(t) for t in re.search(r'bottom row \$?([0-9, ]+)\$?', node(P(iid))['prose']).group(1).split(',')]
s_ = dict(zip(range(1, 7), row))
cy = cycles(s_)
key(iid, perm_order(s_))
wrong(iid, 'product', math.prod(len(c) for c in cy))
wrong(iid, 'sum', sum(len(c) for c in cy))
wrong_ids(iid, ['product', 'sum'])
rec(cy == [(1, 3), (2, 5, 6, 4)], f'{iid}: cycles {cy} = (1 3)(2 5 6 4)')
rec(perm_from_cycles(r'(1\,3)(2\,5\,6\,4)', 6) == s_, f'{iid}: printed cycles give the bottom row')

# ------------------------------------------------------------------ e-zero-divisors-z14
iid = 'e-zero-divisors-z14'
zd = [a for a in range(1, 14) if any(a * b % 14 == 0 for b in range(1, 14))]
units = [a for a in range(1, 14) if any(a * b % 14 == 1 for b in range(14))]
key(iid, len(zd))
wrong(iid, 'evens', len([a for a in zd if a % 2 == 0]))
wrong(iid, 'zero', len(zd) + 1)
wrong_ids(iid, ['evens', 'zero'])
rec(zd == [2, 4, 6, 7, 8, 10, 12], f'{iid}: zero divisors {zd}')
rec(len(units) == 6 and len(units) + len(zd) == 13, f'{iid}: 13 non-zero = 6 units + 7 zero divisors')
rec(7 * 2 % 14 == 0, f'{iid}: 7 x 2 = 14')
allow(iid, 14, 12, 13)

# ------------------------------------------------------------------ e-jump-metric
iid = 'e-jump-metric'
d_ = lambda x, y: 0 if x == y else abs(x - y) + 1
pts = [F(k, 4) for k in range(-12, 13)]
tri = all(d_(x, z) <= d_(x, y) + d_(y, z) for x in pts for y in pts for z in pts)
symm = all(d_(x, y) == d_(y, x) for x in pts for y in pts)
pos = all((d_(x, y) > 0) == (x != y) for x in pts for y in pts)
rec(tri and symm and pos, f'{iid}: all three axioms hold on a grid of 25 rationals')
correct_id(iid, 'ok')

# ------------------------------------------------------------------ e-preimage-quadratic
iid = 'e-preimage-quadratic'
fq = lambda x: x * x - 4 * x
grid = [k / 1000 for k in range(-3000, 8001)]
pre = [x for x in grid if -3 < fq(x) < 5]
inside = lambda x: (-1 < x < 1) or (3 < x < 5)
rec(all(inside(x) for x in pre) and all((-3 < fq(x) < 5) for x in grid if inside(x)),
    f'{iid}: preimage of (-3, 5) is (-1, 1) u (3, 5) on a grid of {len(grid)} points')
rec((fq(-1), fq(1), fq(3), fq(5), fq(2)) == (5, -3, -3, 5, -4), f'{iid}: f(-1) = f(5) = 5, f(1) = f(3) = -3, f(2) = -4')
correct_id(iid, 'ok')
allow(iid, 4, 3, 5, 9)

# ------------------------------------------------------------------ e-four-point-topology
iid = 'e-four-point-topology'
X4 = frozenset({1, 2, 3, 4})


def parse_family(s):
    fam = set()
    body = s.strip('$')[2:-2]       # drop \{ and \}
    if '\\varnothing' in body:
        fam.add(frozenset())
    for m in re.findall(r'\\\{([0-9, ]+)\\\}', body):
        fam.add(frozenset(int(t) for t in m.split(',')))
    if re.search(r'(^|, )X($|,)', body.replace(' ', ' ')):
        fam.add(X4)
    return fam


def topology_faults(fam):
    out = set()
    if frozenset() not in fam or X4 not in fam:
        out.add('whole')
    for a in fam:
        for b in fam:
            if a | b not in fam:
                out.add('union')
            if a & b not in fam:
                out.add('inter')
    return out


for oid, want in [('ok', set()), ('union', {'union'}), ('inter', {'inter'}), ('whole', {'whole'})]:
    fam = parse_family(opt_text(iid, oid))
    rec(topology_faults(fam) == want, f'{iid} option {oid}: faults {sorted(topology_faults(fam))} = {sorted(want)}')
correct_id(iid, 'ok')

# ------------------------------------------------------------------ e-inverse-mod-60
iid = 'e-inverse-mod-60'
invB = next(x for x in range(60) if 17 * x % 60 == 1)
key(iid, invB)
wrong(iid, 'sign', 60 - invB)
wrong(iid, 'coef', 2)
wrong_ids(iid, ['sign', 'coef'])
rec(60 == 3 * 17 + 9 and 17 == 9 + 8 and 9 == 8 + 1, f'{iid}: the three Euclid steps')
rec(1 == 2 * 60 - 7 * 17 and 17 * invB == 901 == 15 * 60 + 1, f'{iid}: 1 = 2 x 60 - 7 x 17 and 17 x 53 = 901 = 15 x 60 + 1')
allow(iid, 17, 60, 59, 901, 15, 53, 7, 9, 8)

# ------------------------------------------------------------------ e-units-mod-17
iid = 'e-units-mod-17'
key(iid, mul_order(2, 17), 0)
wrong(iid, 'group', 16, 0)
wrong(iid, 'minus-one', 4, 0)
gensB = [g for g in range(1, 17) if mul_order(g, 17) == 16]
key(iid, len(gensB), 1)
wrong(iid, 'all', 15, 1)
wrong(iid, 'primes', len([p for p in range(2, 17) if all(p % d for d in range(2, p))]), 1)
wrong_ids(iid, ['group', 'minus-one'], 0)
wrong_ids(iid, ['all', 'primes'], 1)
rec(power_mod(2, 4, 17) == 16 and 256 == 15 * 17 + 1, f'{iid}: 2^4 = 16 = -1 and 2^8 = 256 = 15 x 17 + 1')
rec(3 in gensB, f'{iid}: 3 is a generator')
rec(len(gensB) == sum(1 for k in range(1, 17) if math.gcd(k, 16) == 1), f"{iid}: Euler's phi(16) = 8")
allow(iid, 17, 16, 256, 15)

# ------------------------------------------------------------------ e-even-or-odd
iid = 'e-even-or-odd'
even_ids = [o['id'] for o in node(W(iid))['options'] if sign(perm_from_cycles(o['text'], 6)) == 1]
correct_id(iid, even_ids)
rec(sorted(even_ids) == ['five', 'two-four'], f'{iid}: even options {even_ids}')

# ------------------------------------------------------------------ e-product-table
iid = 'e-product-table'
pr = node(P(iid))['prose']
sg = perm_from_cycles(re.search(r'\\sigma = (\([^$]*)\$', pr).group(1), 5)
ta = perm_from_cycles(re.search(r'\\tau = (\([^$]*)\$', pr).group(1), 5)
stB, tsB = compose(sg, ta), compose(ta, sg)
rows = node(W(iid))['rows']
fbk = node(P(iid) + '.feedback')['byKey']
for k in range(1, 6):
    c = rows[k - 1][1]
    rec(c['answer'] == stB[k], f'{iid} k={k}: cell {c["answer"]} = sigma tau = {stB[k]}')
    ws = c.get('wrong', [])
    rec(ws == [] if tsB[k] == stB[k] else (len(ws) == 1 and ws[0]['value'] == tsB[k] and ws[0]['id'] in fbk),
        f'{iid} k={k}: slip tau sigma = {tsB[k]} keyed on its wrong id')
rec(cycles(stB) == [(2, 5, 3)] and sign(sg) == sign(ta) == -1 and sign(stB) == 1,
    f'{iid}: sigma tau = (2 5 3); both factors odd, product even')
chain = re.findall(r'(\d) \\to (\d) \\to (\d)', node(P(iid))['explain']['text'])
rec(len(chain) == 5 and all(ta[int(a)] == int(b) and sg[int(b)] == int(c) for a, b, c in chain), f'{iid}: the five chains k -> tau(k) -> sigma(tau(k)) in the explanation')
allow(iid, *range(1, 6))

# ------------------------------------------------------------------ e-hom-z18-z12
iid = 'e-hom-z18-z12'
phi = lambda x: 2 * x % 12
rec(all(phi(x + 18) == phi(x) for x in range(18)) and all(phi((a + b) % 18) == (phi(a) + phi(b)) % 12 for a in range(18) for b in range(18)),
    f'{iid}: well defined and a homomorphism')
kerB = [x for x in range(18) if phi(x) == 0]
imB = sorted({phi(x) for x in range(18)})
key(iid, len(kerB), 0)
wrong(iid, 'in-target', len([x for x in range(12) if 2 * x % 12 == 0]), 0)
wrong(iid, 'image', len(imB), 0)
key(iid, len(imB), 1)
wrong(iid, 'target-over', 12 // len(kerB), 1)
wrong(iid, 'onto', 12, 1)
wrong_ids(iid, ['in-target', 'image'], 0)
wrong_ids(iid, ['target-over', 'onto'], 1)
rec(kerB == [0, 6, 12] and imB == [0, 2, 4, 6, 8, 10], f'{iid}: ker {kerB}, im {imB}')
allow(iid, 18, 12, 36, 17)

# ------------------------------------------------------------------ e-normal-in-s4
iid = 'e-normal-in-s4'
S4 = all_perms(4)


def gen(gs):
    e = {k: k for k in range(1, 5)}
    out = [e]
    frontier = [e]
    while frontier:
        new = []
        for a in frontier:
            for g in gs:
                b = compose(g, a)
                if b not in out:
                    out.append(b)
                    new.append(b)
        frontier = new
    return out


def normal(Hs):
    return all(compose(compose(g, h), inverse(g)) in Hs for g in S4 for h in Hs)


subs = {}
for o in node(W(iid))['options']:
    gens_ = [perm_from_cycles(c, 4) for c in re.findall(r'\((?:\d\\,)+\d\)(?:\((?:\d\\,)+\d\))*', o['text'])]
    subs[o['id']] = gen(gens_)
normal_ids = [k for k, v in subs.items() if normal(v)]
correct_id(iid, normal_ids)
rec(normal_ids == ['ok'] and len(subs['ok']) == 4, f'{iid}: only V is normal; |V| = 4')
c12 = compose(compose(perm_from_cycles(r'(1\,2)', 4), perm_from_cycles(r'(1\,2\,3\,4)', 4)), perm_from_cycles(r'(1\,2)', 4))
rec(c12 == perm_from_cycles(r'(2\,1\,3\,4)', 4) and c12 not in subs['four'], f'{iid}: (12)(1234)(12) = (2 1 3 4), outside <(1234)>')
t23 = perm_from_cycles(r'(2\,3)', 4)
rec(compose(compose(t23, perm_from_cycles(r'(1\,2)(3\,4)', 4)), t23) == perm_from_cycles(r'(1\,3)(2\,4)', 4), f'{iid}: (23) conjugates (12)(34) to (13)(24)')
t34 = perm_from_cycles(r'(3\,4)', 4)
rec(compose(compose(t34, perm_from_cycles(r'(1\,2\,3)', 4)), t34) == perm_from_cycles(r'(1\,2\,4)', 4), f'{iid}: (34) conjugates (123) to (124)')

# ------------------------------------------------------------------ e-euler-mod-14
iid = 'e-euler-mod-14'
U14 = [a for a in range(1, 14) if math.gcd(a, 14) == 1]
key(iid, power_mod(5, 100, 14))
wrong(iid, 'prime', power_mod(5, 9, 14))
wrong(iid, 'mod-n', power_mod(5, 2, 14))
wrong_ids(iid, ['prime', 'mod-n'])
ex.expect('exam', f'{P(iid)}.feedback.byKey', f'5^9 \\equiv {power_mod(5, 9, 14)}')
ex.expect('exam', f'{P(iid)}.feedback.byKey', f'5^2 = 25 \\equiv {power_mod(5, 2, 14)}')
ex.expect('exam', f'{P(iid)}.feedback.correct', f'5^4 = 625 \\equiv {power_mod(5, 4, 14)}')
rec(len(U14) == 6 and mul_order(5, 14) in (1, 2, 3, 6), f'{iid}: |Z_14^x| = 6 and ord(5) divides it')
rec(100 == 16 * 6 + 4 and 625 == 44 * 14 + 9 and 100 % 13 == 9 and 100 % 14 == 2, f'{iid}: 100 = 16 x 6 + 4, 625 = 44 x 14 + 9, 100 mod 13 = 9')
allow(iid, 14, 13, 100, 16, 625, 44, 25, 11)

# ------------------------------------------------------------------ e-remainder-z7
iid = 'e-remainder-z7'
coef = [1, 0, 0, 3, 0, 2]            # x^5 + 3x^2 + 2, highest first
acc = 0
for c in coef:                       # synthetic division by x - 4 over Z_7
    acc = (acc * 4 + c) % 7
key(iid, acc)
accm = 0
for c in coef:
    accm = (accm * 3 + c) % 7        # -4 = 3 in Z_7
wrong(iid, 'minus-four', accm)
wrong(iid, 'unreduced', sum(c * 4 ** (5 - i) for i, c in enumerate(coef)))
wrong_ids(iid, ['minus-four', 'unreduced'])
rec(16 % 7 == 2 and 64 % 7 == 1 and (1024 % 7, 3 * 16 % 7) == (2, 6), f'{iid}: 4^2 = 2, 4^3 = 1, 4^5 = 2, 3 x 4^2 = 6 mod 7')
allow(iid, 1074)

# ------------------------------------------------------------------ e-irreducible-z3
iid = 'e-irreducible-z3'


def ptrim(a):
    a = [c % 3 for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return ptrim(out)


def parse_poly(s):                   # 'x^4 + x^3 + x + 2' -> low-first coefficients
    s = s.strip('$').replace(' ', '')
    c = [0] * 6
    for t in s.split('+'):
        m = re.fullmatch(r'(\d*)x(?:\^(\d))?|(\d+)', t)
        if m.group(3):
            c[0] += int(m.group(3))
        else:
            c[int(m.group(2) or 1)] += int(m.group(1) or 1)
    return ptrim(c)


def reducible(f):
    n = len(f) - 1
    for d in range(1, n // 2 + 1):
        for tail in itertools.product(range(3), repeat=d):
            g = list(tail) + [1]
            for tail2 in itertools.product(range(3), repeat=n - d):
                h = list(tail2) + [f[-1]]
                if pmul(g, h) == f:
                    return True
    return False


irr = [o['id'] for o in node(W(iid))['options'] if not reducible(parse_poly(o['text']))]
correct_id(iid, irr)
rec(sorted(irr) == ['cubic', 'quad'], f'{iid}: irreducible options {irr}')
q4 = parse_poly(opt_text(iid, 'quartic'))
rec(pmul([1, 0, 1], [2, 1, 1]) == q4 and all(sum(c * x ** i for i, c in enumerate(q4)) % 3 for x in range(3)),
    f'{iid}: x^4 + x^3 + x + 2 = (x^2 + 1)(x^2 + x + 2) and has no root')
vals = lambda f: [sum(c * x ** i for i, c in enumerate(f)) % 3 for x in range(3)]
rec(vals(parse_poly('x^2 + x + 2')) == [2, 1, 2] and vals(parse_poly('x^3 + 2x^2 + 1')) == [1, 1, 2]
    and vals(parse_poly('x^3 + x + 2'))[2] == 0 and 8 + 2 + 2 == 12, f'{iid}: the values quoted at 0, 1, 2')
allow(iid, 12)

# ------------------------------------------------------------------ e-half-disc
iid = 'e-half-disc'
inA = lambda x, y: x * x + y * y < 1 and y >= 0


def on_boundary(x, y, r=1e-7, k=64):
    ring = [(x + r * math.cos(2 * math.pi * j / k), y + r * math.sin(2 * math.pi * j / k)) for j in range(k)] + [(x, y)]
    ins = [inA(*p) for p in ring]
    return any(ins) and not all(ins)


opts = {
    'ok': lambda x, y: (abs(x * x + y * y - 1) < 1e-12 and y >= 0) or (y == 0 and -1 <= x <= 1),
    'arc': lambda x, y: abs(x * x + y * y - 1) < 1e-12 and y >= 0,
    'corners': lambda x, y: (abs(x * x + y * y - 1) < 1e-12 and y > 0) or (y == 0 and -1 < x < 1),
    'interior': lambda x, y: x * x + y * y < 1 and y > 0,
}
tests = [(0, 0), (1, 0), (-1, 0), (0.5, 0), (0, 1), (0.6, 0.8), (0, 0.5), (0.3, 0.3), (0, -0.2), (2, 0), (-0.6, 0.8)]
truth = [on_boundary(*p) for p in tests]
right = [k for k, f in opts.items() if [bool(f(*p)) for p in tests] == truth]
correct_id(iid, right)
rec(right == ['ok'], f'{iid}: only the arc with the closed diameter matches the sampled boundary at {len(tests)} points')

# ------------------------------------------------------------------ e-two-function-metrics
iid = 'e-two-function-metrics'
hgap = lambda x: x - x ** 3
gx = [k / 200000 for k in range(200001)]
key(iid, max(hgap(x) for x in gx), 0, tol=1e-6)
wrong(iid, 'ends', max(hgap(0), hgap(1)), 0)
wrong(iid, 'midpoint', hgap(0.5), 0)
key(iid, simpson(hgap, 0, 1), 1, tol=1e-9)
wrong(iid, 'square', simpson(lambda x: hgap(x) ** 2, 0, 1), 1)
wrong_ids(iid, ['ends', 'midpoint'], 0)
wrong_ids(iid, ['square'], 1)
argm = max(gx, key=hgap)
rec(abs(argm - 1 / math.sqrt(3)) < 1e-5 and abs(simpson(lambda x: hgap(x) ** 2, 0, 1) - 8 / 105) < 1e-12, f'{iid}: peak at 1/sqrt 3, squared integral 8/105')
rec(simpson(hgap, 0, 1) <= max(hgap(x) for x in gx), f'{iid}: d_1 <= d_infinity here')
allow(iid, 0.375, 105, 0.0762, 8 / 105)

# ------------------------------------------------------------------ e-homeomorphic-pairs
iid = 'e-homeomorphic-pairs'
hm = lambda x: x / (1 - x)
hinv = lambda y: y / (1 + y)
xsamp = [k / 1000 for k in range(1, 1000)]
rec(all(hm(a) < hm(b) for a, b in zip(xsamp, xsamp[1:])) and all(abs(hinv(hm(x)) - x) < 1e-12 for x in xsamp) and hm(0.999) > 900,
    f'{iid}: x/(1 - x) is increasing on (0, 1), inverted by y/(1 + y), and unbounded')
rec(3 + 4 * 0 == 3 and 3 + 4 * 1 == 7, f'{iid}: 3 + 4x maps (0, 1) onto (3, 7)')
correct_id(iid, ['half-line', 'affine'])
allow(iid, 3, 4, 7)

# ------------------------------------------------------------------ e-connected-subsets
iid = 'e-connected-subsets'
rec(0 < math.sqrt(2) / 2 < 1, f'{iid}: sqrt(2)/2 lies in (0, 1) and is irrational')
correct_id(iid, ['glued', 'image'])

# ------------------------------------------------------------------ e-compact-subsets
iid = 'e-compact-subsets'
correct_id(iid, ['circle', 'graph'])
rec(math.hypot(1 / 10 ** 6, 1 / 10 ** 6) < 1e-5, f'{iid}: (1/n, 1/n) tends to (0, 0)')

# ------------------------------------------------------------------ e-log-metric
iid = 'e-log-metric'
dl = lambda x, y: abs(math.log(x) - math.log(y))
rec(all(abs(dl(1 / n, 1 / (2 * n)) - math.log(2)) < 1e-12 for n in (1, 10, 1000)), f'{iid}: d(1/n, 1/2n) = ln 2 for every n, so 1/n is not Cauchy')
correct_id(iid, 'ok')

# ------------------------------------------------------------------ e-which-fields
iid = 'e-which-fields'
is_field = lambda n: all(any(a * b % n == 1 for b in range(n)) for a in range(1, n))
rec(is_field(103) and not is_field(87) and 87 == 3 * 29 and 3 * 29 % 87 == 0, f'{iid}: Z_103 is a field, Z_87 is not, 87 = 3 x 29')
ok_inv = all((F(a) + F(b) * 0 == F(a)) and F(a * a - 3 * b * b) != 0 for a in range(-6, 7) for b in range(-6, 7) if (a, b) != (0, 0))
rec(ok_inv, f'{iid}: a^2 - 3b^2 is never 0 for integers (a, b) != (0, 0) in a box (sqrt 3 irrational)')
A_ = [[1, 0], [0, 0]]
B_ = [[0, 1], [0, 0]]
mm = lambda X, Y: [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
rec(mm(A_, B_) != mm(B_, A_), f'{iid}: the 2 x 2 matrices do not commute')
correct_id(iid, ['prime', 'root-three'])
allow(iid, 103, 87, 29)

# ------------------------------------------------------------------ e-max-on-circle
iid = 'e-max-on-circle'
ts_ = [2 * math.pi * k / 400000 for k in range(400000)]
best = max(math.cos(t) + 2 * math.sin(t) for t in ts_)
correct_id(iid, 'ok', 0)
key(iid, best, 1, tol=1e-6)
wrong(iid, 'corner', 1 + 2, 1)
wrong(iid, 'one-asset', 2, 1)
wrong_ids(iid, ['corner', 'one-asset'], 1)
tb = max(ts_, key=lambda t: math.cos(t) + 2 * math.sin(t))
rec(abs(math.cos(tb) - 1 / math.sqrt(5)) < 1e-4 and abs(math.sin(tb) - 2 / math.sqrt(5)) < 1e-4, f'{iid}: the best point is (1/sqrt5, 2/sqrt5)')
ex.expect('exam', f'{P(iid)}.explain.text', f'£{round(1000 * best):,}')
allow(iid, round(1000 * best), 5)

# ------------------------------------------------------------------ e-cyclic-subgroups-proof
iid = 'e-cyclic-subgroups-proof'
w = node(W(iid))
rec(w['answer'] == ['c1', 'c2', 'c3', 'c4', 'c5', 'c6'] and w['same'] == [['c3', 'c4']] and w['distractors'] == ['d1', 'd2']
    and all(l.get('why') for l in w['lines'] if l['id'] in w['distractors']), f'{iid}: order, same set and distractors with why')
ok_cyc = True
for n in range(1, 13):
    for mask in range(1, 2 ** n):
        Hs = {k for k in range(n) if mask >> k & 1}
        if 0 in Hs and all((a - b) % n in Hs for a in Hs for b in Hs):
            pos = [k for k in Hs if k > 0]
            m = min(pos) if pos else n
            ok_cyc &= Hs == {m * j % n for j in range(n)}
rec(ok_cyc, f'{iid}: every subgroup of Z_n, n <= 12, is generated by its least positive element')
V4 = gen([perm_from_cycles(r'(1\,2)(3\,4)', 4), perm_from_cycles(r'(1\,3)(2\,4)', 4)])
rec(len(V4) == 4 and max(perm_order(v) for v in V4) == 2, f'{iid}: the Klein group has order 4 and no element of order 4')

# ------------------------------------------------------------------ e-equaliser-closed
iid = 'e-equaliser-closed'
w = node(W(iid))
rec(w['answer'] == ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'] and w['same'] == [['h3', 'h4']] and w['distractors'] == ['d1', 'd2']
    and all(l.get('why') for l in w['lines'] if l['id'] in w['distractors']), f'{iid}: order, same set and distractors with why')
tauX = [set(), {'a'}, {'a', 'b'}]                 # Sierpinski space on {a, b}
tauY = [set(), {0, 1}]                            # indiscrete two-point space
fE, gE = {'a': 0, 'b': 0}, {'a': 0, 'b': 1}
cont = lambda f: all({x for x in 'ab' if f[x] in V} in tauX for V in tauY)
Eset = {x for x in 'ab' if fE[x] == gE[x]}
rec(cont(fE) and cont(gE) and ({'a', 'b'} - Eset) not in tauX, f'{iid}: into an indiscrete Y, E = {Eset} is not closed')

# ------------------------------------------------------------------ e-image-sizes
iid = 'e-image-sizes'
possible = [k for k in range(1, 29) if 28 % k == 0 and 21 % k == 0]
opt_vals = {o['id']: int(o['text']) for o in node(W(iid))['options']}
correct_id(iid, [k for k, v in opt_vals.items() if v in possible])
homs = [a for a in range(21) if 28 * a % 21 == 0]
sizes = sorted({len({x * a % 21 for x in range(28)}) for a in homs})
rec(possible == [1, 7] and sizes == [1, 7] and 3 in homs, f'{iid}: image sizes from Z_28 to Z_21 are {sizes}; x -> 3x is one')
allow(iid, 28, 21)

# ------------------------------------------------------------------ e-order-three-s6
iid = 'e-order-three-s6'
S6 = all_perms(6)
o3 = [p for p in S6 if perm_order(p) == 3]
one = [p for p in o3 if len(cycles(p)) == 1]
key(iid, len(o3))
wrong(iid, 'one-cycle', len(one))
wrong(iid, 'ordered', len(one) + 2 * (len(o3) - len(one)))
wrong_ids(iid, ['one-cycle', 'ordered'])
rec(len(one) == 40 and len(o3) - len(one) == 40 and math.comb(6, 3) == 20, f'{iid}: 40 single 3-cycles, 40 products of two, C(6,3) = 20')
allow(iid, 40, 20, 80, 120)

# ------------------------------------------------------------------ e-squares-mod-11
iid = 'e-squares-mod-11'
G11 = range(1, 11)
kerS = [x for x in G11 if x * x % 11 == 1]
sqB = sorted({x * x % 11 for x in G11})
key(iid, len(kerS), 0)
wrong(iid, 'one', 1, 0)
wrong(iid, 'image', len(sqB), 0)
key(iid, len(sqB), 1)
wrong(iid, 'onto', 10, 1)
wrong(iid, 'with-zero', len(sqB) + 1, 1)
wrong_ids(iid, ['one', 'image'], 0)
wrong_ids(iid, ['onto', 'with-zero'], 1)
k5 = [x for x in G11 if power_mod(x, 5, 11) == 1]
rec(kerS == [1, 10] and sqB == [1, 3, 4, 5, 9] and k5 == sqB, f'{iid}: kernel {kerS}, squares {sqB} = ker of x^5')
rec(3 in sqB and 2 not in sqB, f'{iid}: 3 is a square, 2 is not')
correct_id(iid, 'three', 2)
rec(power_mod(3, 5, 11) == 1 and 243 == 22 * 11 + 1 and power_mod(2, 5, 11) == 10 and 25 % 11 == 3 and 100 == 9 * 11 + 1,
    f'{iid}: 3^5 = 243 = 22 x 11 + 1, 2^5 = 32 = -1, 5^2 = 3, 10^2 = 100 = 9 x 11 + 1')
allow(iid, 11, 243, 22, 32, 25, 100, 10)

# ------------------------------------------------------------------ e-plane-contraction
iid = 'e-plane-contraction'
qB = max(F(1, 3), F(1, 4))
key(iid, float(qB), 0)
wrong(iid, 'sum', float(F(1, 3) + F(1, 4)), 0)
wrong(iid, 'product', float(F(1, 3) * F(1, 4)), 0)
# Lipschitz ratio sampled near the steepest point (y = 0) approaches 1/3 from below
lip = max(max(abs(math.sin(y + h) - math.sin(y)) / 3, abs(math.cos(1.6 + h) - math.cos(1.6)) / 4) / h for y in (0.0, 0.001) for h in (1e-6, 1e-4))
rec(lip <= 1 / 3 + 1e-12 and lip > 0.333, f'{iid}: sampled ratio {lip:.6f} sits just under 1/3')
p1 = (math.sin(0) / 3 + 2, math.cos(2) / 4)
dB = max(abs(p1[0] - 2), abs(p1[1] - 0))
cB = dB / (1 - float(qB))
nB = math.ceil(math.log(cB / 1e-6) / math.log(3))
if cB * 3.0 ** -nB >= 1e-6:
    nB += 1
key(iid, nB, 1)
wrong(iid, 'floor', nB - 1, 1)
wrong(iid, 'no-factor', math.ceil(6 * math.log(10) / math.log(3)), 1)
xfix = bisect(lambda x: math.sin(math.cos(x) / 4) / 3 + 2 - x, 1.0, 3.0)
yfix = math.cos(xfix) / 4
key(iid, xfix, 2)
wrong(iid, 'one-step', p1[0], 2)
wrong_ids(iid, ['sum', 'product'], 0)
wrong_ids(iid, ['floor', 'no-factor'], 1)
wrong_ids(iid, ['one-step'], 2)
rec(abs(math.sin(yfix) / 3 + 2 - xfix) < 1e-12 and round(yfix, 4) == -0.0967, f'{iid}: p* = ({xfix:.6f}, {yfix:.6f}) is fixed')
rec(round(dB, 5) == 0.10404 and round(cB, 4) == 0.1561 and round(cB * 3.0 ** -11 * 1e7, 1) == 8.8 and round(cB * 3.0 ** -10 * 1e6, 1) == 2.6,
    f'{iid}: 0.10404, 0.1561, 8.8e-7 at n = 11, 2.6e-6 at n = 10')
allow(iid, dB, cB, 8.8, 2.6, yfix, 1.5, float(F(7, 12)), float(F(1, 12)), 11, 13)

# ------------------------------------------------------------------ e-power-contraction-proof
iid = 'e-power-contraction-proof'
it = node(P(iid))
xs_ = bisect(lambda x: math.exp(-x) - x, 0.0, 1.0)
ugrid = [k / 100000 for k in range(1, 100001)]
rec(abs(max(u * math.exp(-u) for u in ugrid) - math.exp(-1)) < 1e-12, f'{iid}: max of u e^-u on (0, 1] is 1/e')
rec(abs((1 - math.exp(-1e-6)) / 1e-6 - 1) < 1e-6, f'{iid}: slope ratio near 0 tends to 1')
ex.expect('exam', f'{P(iid)}.model', round(math.exp(-1), 4))
ex.expect('exam', f'{P(iid)}.model', round(xs_, 4))
ex.expect('exam', f'{P(iid)}.explain.text', round(xs_, 4))
rec(sum(r_['points'] for r_ in it['rubric']) == 10, f'{iid}: rubric sums to 10')
allow(iid, math.exp(-1), xs_)


# ------------------------------------------------------------------ every level has an item on a skill first met there
LEVEL = {   # item -> (course, level of the lesson it is pitched at)
    'e-order-fifteen': ('algebra', 1), 'e-inverse-mod-60': ('algebra', 1), 'e-units-mod-17': ('algebra', 1),
    'e-cycles-bottom-row': ('algebra', 2), 'e-even-or-odd': ('algebra', 2), 'e-product-table': ('algebra', 2),
    'e-cyclic-subgroups-proof': ('algebra', 2), 'e-order-three-s6': ('algebra', 2),
    'e-hom-z18-z12': ('algebra', 3), 'e-normal-in-s4': ('algebra', 3), 'e-euler-mod-14': ('algebra', 3),
    'e-image-sizes': ('algebra', 3), 'e-squares-mod-11': ('algebra', 3),
    'e-zero-divisors-z14': ('algebra', 4), 'e-remainder-z7': ('algebra', 4), 'e-irreducible-z3': ('algebra', 4),
    'e-which-fields': ('algebra', 4),
    'e-jump-metric': ('topology', 1), 'e-preimage-quadratic': ('topology', 1), 'e-half-disc': ('topology', 1),
    'e-two-function-metrics': ('topology', 1),
    'e-four-point-topology': ('topology', 2), 'e-homeomorphic-pairs': ('topology', 2),
    'e-connected-subsets': ('topology', 2), 'e-equaliser-closed': ('topology', 2),
    'e-compact-subsets': ('topology', 3), 'e-log-metric': ('topology', 3), 'e-max-on-circle': ('topology', 3),
    'e-plane-contraction': ('topology', 3), 'e-power-contraction-proof': ('topology', 3),
}
rec(sorted(LEVEL) == sorted(idx), 'every item has a level')
CDIR = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')
all_sk = set()
for course in ('algebra', 'topology'):
    with open(os.path.join(CDIR, course, 'course.json'), encoding='utf8') as f:
        cj = json.load(f)
    all_sk |= set(cj['skills'])
    seen = set()
    for lv in cj['levels']:
        sk = set()
        for lid in lv['lessons']:
            with open(os.path.join(CDIR, course, lid + '.json'), encoding='utf8') as f:
                sk |= set(json.load(f)['skills'])
        new = sk - seen
        seen |= sk
        hits = [i for i, (c, n) in LEVEL.items() if c == course and n == lv['n'] and set(node(P(i))['skills']) & new]
        auto = [i for i in hits if node(P(i)).get('kind') != 'longform']
        rec(bool(auto), f'{course} L{lv["n"]}: new skills {sorted(new)} tested by auto items {auto}')
auto_sk = {s for it_ in items if it_.get('kind') != 'longform' for s in it_['skills']}
rec(auto_sk == all_sk == set(doc['skills']), f'every one of the {len(all_sk)} skills is on an auto-graded item and in the skills map')
ramp = Counter(it_['difficulty'] for it_ in items)
rec(len(items) == 30 and dict(ramp) == {2: 6, 3: 15, 4: 6, 5: 3}, f'30 items, ramp {dict(sorted(ramp.items()))}')
print('items per level:', dict(sorted(Counter(LEVEL.values()).items())), 'pace', sum(it_['pace'] for it_ in items), 's')


# ------------------------------------------------------------------ every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = re.sub(r'(\d)\\,(?=\d)', r'\1 ', s)     # cycle notation (1\,2\,3) is three points, not 123
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t else 0), t


for it_ in items:
    iid = it_['id']
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings(it_):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    ex._rec(not bad, f'{iid}: every stated number matches route B', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
