"""Second-read number and claim checks for proof level 2 (l6 to l9, review-2, homework-2).
Run from the repo root: python3 docs/reports/proof-L2-numbers.py  (exits 0 when every check passes).
Every key and wrong value is recomputed; set laws, function counts and the composite claims are
brute-forced over every case on small sets. lv.stated checks fail while a false sentence is in the text.
"""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('proof', 2)
F = lambda pre: lv.files[[k for k in lv.files if k.startswith(pre)][0]]


def cell_ids(grid_rows, pred):
    return [f'r{i + 1}c{j + 1}' for i, r in enumerate(grid_rows) for j, v in enumerate(r) if pred(int(v))]


def subsets(s):
    s = list(s)
    return [set(c) for k in range(len(s) + 1) for c in itertools.combinations(s, k)]


def functions(A, B):
    A = list(A)
    return [dict(zip(A, img)) for img in itertools.product(list(B), repeat=len(A))]


inj = lambda f: len(set(f.values())) == len(f)
onto = lambda f, B: set(f.values()) == set(B)

# ---------- l6 ----------
d6 = F('l6')
g = d6['screens'][0]['canvas']['params']['cells']
lv.claim(d6['screens'][0]['widget']['answer'] == cell_ids(g, lambda v: v % 3 == 0), 'l6 multiples of 3 on 1..20 are the six tapped cells')
lv.expect('l6', 'screens[1].widget.answer', len([n for n in range(1, 21) if n % 3 == 0]))
lv.expect('l6', 'screens[2].widget.answer', len({1, 2, 2, 3}))
lv.claim(d6['screens'][3]['widget']['answer'] == cell_ids(g, lambda v: v % 6 == 0) and {6, 12, 18} <= {n for n in range(1, 21) if n % 3 == 0}, 'l6 S = {6, 12, 18} and S is a subset of A')
lv.claim(13 == 3 * 4 + 1 and 20 == 3 * 6 + 2 and 10 == 3 * 3 + 1 and 9 == 6 + 3 and 15 == 12 + 3, 'l6 feedback remainders')
pts = {'p1': -0.5, 'p2': 0, 'p3': 0.25, 'p4': 0.75, 'p5': 1, 'p6': 1.5}
lv.claim(d6['screens'][4]['widget']['answer'] == [k for k, x in pts.items() if 0 <= x < 1], 'l6 points in [0, 1): 0, 0.25, 0.75')
by_size = [sum(1 for s in subsets('abc') if len(s) == k) for k in range(4)]
lv.claim([r[1]['answer'] for r in d6['screens'][5]['widget']['rows']] == by_size + [sum(by_size)] and sum(by_size) == 2 ** 3, 'l6 subsets of {a, b, c} by size 1, 3, 3, 1; total 8 = 2^3')
lv.claim(all(set() <= s for s in subsets(range(5))), 'empty set is a subset of every subset of a 5-set')
lv.claim(all(x % 3 == 0 for x in range(-6000, 6001, 6)), 'every multiple of 6 in -6000..6000 is a multiple of 3')
lv.claim([s[0] for s in d6['screens'][10]['canvas']['params']['rows'] if float(s[1]) < 10] == ['Avonmore Mining', 'Bridgegate Bank', 'Dunmore Energy', 'Fenwick Insurance'], 'l6 screen 1: P/E below 10')
lv.claim([s[0].split()[0] for s in d6['screens'][10]['canvas']['params']['rows'] if float(s[1]) < 10 and float(s[2].rstrip('%')) > 5] == ['Avonmore', 'Bridgegate', 'Fenwick'], 'l6 screen 2: also yield above 5%')
lv.expect('l6', 'quiz[0].widget.answer', len([frozenset()]))
lv.claim({3, 1, 2} == {1, 2, 3} == {1, 2, 2, 3, 3} != {1, 2} and {1, 2, 3, 4} != {1, 2, 3}, 'l6 quiz equal sets')
lv.claim([n for n in range(1, 21) if n % 5 == 0] == [5, 10, 15, 20], 'l6 F = {5, 10, 15, 20}')
lv.expect('l6', 'quiz[3].widget.answer', len(subsets('abcd')))

# ---------- l7 ----------
U = set(range(1, 13))
A, B, C = {n for n in U if n % 2 == 0}, {n for n in U if n % 3 == 0}, {n for n in U if n % 4 == 0}
fmt = lambda s: ', '.join(map(str, sorted(s))) if s else 'empty'
v = F('l7')['screens'][0]['canvas']['params']['values']
lv.claim(v == {'A': fmt(A - B), 'AB': fmt(A & B), 'B': fmt(B - A), 'none': fmt(U - A - B)}, 'l7 two-set venn regions match 1..12')
v3 = F('l7')['screens'][10]['canvas']['params']['values']
want3 = {'A': A - B - C, 'B': B - A - C, 'C': C - A - B, 'AB': (A & B) - C, 'AC': (A & C) - B, 'BC': (B & C) - A, 'ABC': A & B & C, 'none': U - A - B - C}
lv.claim(v3 == {k: fmt(s) for k, s in want3.items()}, 'l7 three-set venn regions match, two empty')
lv.expect('l7', 'screens[3].widget.answer', len(A | B))
lv.claim(len(A) + len(B) - len(A & B) == len(A | B) == 8 and len(A) + len(B) == 10 and 10 - 2 * 2 == 6, 'l7 inclusion-exclusion 6 + 4 - 2 = 8; wrongs 10 and 6')
lv.claim(U - A == {1, 3, 5, 7, 9, 11} and U - B == (A - B) | (U - A - B), 'l7 A^c and B^c regions')
lv.claim(U - (A | B) == {1, 5, 7, 11} and len((U - A) | (U - B)) == 10 and (U - A) | (U - B) == U - (A & B), 'l7 trap: 4 against 10; colleague set is (A cap B)^c')
lv.expect('l7', 'screens[6].widget.answer', len(U - (A & B)))
lv.claim(A & (B | C) == {4, 6, 8, 12} == (A & B) | (A & C), 'l7 distributive example {4, 6, 8, 12}')
S5 = subsets(range(1, 5))
Ux = set(range(1, 5))
lv.claim(all(Ux - (X | Y) == (Ux - X) & (Ux - Y) and Ux - (X & Y) == (Ux - X) | (Ux - Y) for X in S5 for Y in S5), 'De Morgan for sets, every pair of subsets of a 4-set')
lv.claim(all(X & (Y | Z) == (X & Y) | (X & Z) for X in S5 for Y in S5 for Z in S5), 'distributive law, every triple of subsets of a 4-set')
lv.claim(not all(Ux - (X | Y) == (Ux - X) | (Ux - Y) for X in S5 for Y in S5), 'the colleague form fails for some pair')
lv.expect('l7', 'screens[11].widget.answer', 100 - (40 + 25 - 10))
lv.claim(40 - 10 == 30 and 25 - 10 == 15 and 100 - 65 == 35 and 100 - 75 == 25, 'l7 transfer regions 30, 15; wrongs 35, 25')
lv.claim(B - A == {3, 9} and A - B == {2, 4, 8, 10}, 'l7 quiz B minus A')
lv.expect('l7', 'quiz[1].widget.answer', 5 + 7 - 0)
lv.claim(100 - 12 == 88 and 600 - 12 == 588, 'l7 complement depends on the universe: 88 and 588')

# ---------- l8 ----------
T, D = ['Ana', 'Ben', 'Cal'], ['Rates', 'FX', 'Equities', 'Credit']
lv.expect('l8', 'screens[1].widget.answer', len(list(itertools.product(T, D))))
lv.expect('l8', 'screens[6].widget.answer', len(functions(T, D)))
lv.claim(3 * 4 == 12 and 3 ** 4 == 81 and 4 * 3 * 2 == 24, 'l8 wrongs 12, 81, 24')
lv.expect('l8', 'quiz[0].widget.answer', len(functions([], D)))
lv.expect('l8', 'quiz[2].widget.answer', len(functions('ab', range(5))))
lv.claim(2 ** 5 == 32 and 2 * 5 == 10 and 5 * 4 == 20, 'l8 quiz wrongs 32, 10, 20')
lv.claim({'a', 'a', 'b'} == {'a', 'b'}, 'l8 image of {(1, a), (2, a), (3, b)} is {a, b}')
seat = {'Ana': 'FX', 'Ben': 'Rates', 'Cal': 'FX'}
lv.claim(set(seat.values()) == {'FX', 'Rates'}, 'l8 image of the seating is {FX, Rates}')
lv.claim(0.5 ** 2 == 0.25 and 2 ** 2 == 4, 'l8 pair (0.5, 0.25) and f(2) = g(2) = 4')

# ---------- l9 ----------
f = lambda x: 3 * x + 2
finv = lambda y: (y - 2) / 3
lv.claim(all(abs(f(finv(y)) - y) < 1e-9 and abs(finv(f(y)) - y) < 1e-9 for y in [i / 4 for i in range(-400, 401)]), 'l9 f^-1 = (y - 2)/3 inverts f both ways')
lv.claim(all((f(a) == f(b)) == (a == b) for a in range(-60, 61) for b in range(-60, 61)), 'l9 f one-to-one on an integer grid')
lv.expect('l9', 'screens[7].widget.answer', finv(11))
lv.claim(f(11) == 35 and abs((11 + 2) / 3 - 4.3333) < 1e-4 and finv(-4) == -2 and f(-4) == -10 and abs((-4 + 2) / 3 + 0.6667) < 1e-4, 'l9 wrongs 35, 13/3; f^-1(-4) = -2; wrongs -10, -2/3')
lv.expect('l9', 'quiz[0].widget.answer', finv(-4))
lv.expect('l9', 'screens[9].widget.answer', sum(1 for h in functions(T, D) if inj(h)))
lv.claim(not any(onto(h, D) for h in functions(T, D) if inj(h)) and 4 ** 3 == 64 and 3 * 2 == 6, 'l9 none of the 24 is onto; wrongs 64, 6')
lv.expect('l9', 'quiz[1].widget.answer', sum(1 for h in functions('xyz', 'pqr') if inj(h)))
lv.claim(all(onto(h, 'pqr') for h in functions('xyz', 'pqr') if inj(h)) and 3 ** 3 == 27, 'l9 3 to 3: one-to-one forces onto; wrong 27')
lv.claim(all(abs(5 * ((y + 1) / 5) - 1 - y) < 1e-9 for y in range(-50, 51)) and 5 * 1 - 1 == 4 and 5 * 2 - 1 == 9, 'l9 h onto witness (y + 1)/5; h(1) = 4, h(2) = 9')
lv.expect('l9', 'quiz[3].widget.answer', 250 / 1.25)
lv.claim(250 * 1.25 == 312.5 and 200 * 1.25 == 250, 'l9 converter: wrong 312.5; £200 to $250')
lv.claim(5000 > 1024, 'l9 pigeonhole: 5,000 ids into 1,024 buckets')
sq = lambda x: x * x
lv.claim(sq(-2) == sq(2) == 4 and not any(abs(sq(i / 10) + 1) < 1e-9 for i in range(-100, 101)), 'l9 x^2 on R: not one-to-one, misses -1')
lv.claim(all(abs((y ** 0.5) ** 2 - y) < 1e-9 for y in [i / 8 for i in range(0, 200)]), 'l9 sqrt inverts x^2 on [0, inf)')

# ---------- review-2 ----------
U10 = set(range(1, 11))
Pr = {2, 3, 5, 7}
Od = {n for n in U10 if n % 2}
lv.claim(F('review')['items'][1]['canvas']['params']['values'] == {'A': fmt(Pr - Od), 'AB': fmt(Pr & Od), 'B': fmt(Od - Pr), 'none': fmt(U10 - Pr - Od)}, 'review-2 venn: primes and odds in 1..10')
lv.claim(U10 - (Pr & Od) == {1, 2, 4, 6, 8, 9, 10}, 'review-2 (A cap B)^c has seven numbers')
lv.expect('review', 'items[3].widget.answer', 30 - (18 + 15 - 7))
lv.claim(18 + 15 - 7 == 26 and 30 - 18 - 15 == -3 and 30 - 18 - 15 - 7 == -10, 'review-2 wrongs 26, -3, -10')
fr = {'a': 'x', 'b': 'y', 'c': 'z', 'd': 'y'}
lv.claim(onto(fr, 'xyz') and not inj(fr), 'review-2 arrows: onto, not one-to-one')
lv.claim(all(x % 2 == 0 for x in range(-4000, 4001, 4)), 'every multiple of 4 is even (brute force)')
h = lambda x: 2 * x - 6
lv.claim(all(h((y + 6) / 2) == y for y in range(-50, 51)) and (4 + 6) / 2 == 5 and h(5) == 4, 'review-2 h^-1(y) = (y + 6)/2; h^-1(4) = 5')
lv.expect('review', 'items[7].widget.answer', sum(1 for q in functions('ab', range(5)) if inj(q)))
lv.claim(5 ** 2 == 25 and 2 ** 5 == 32 and len(list(itertools.combinations(range(5), 2))) == 10, 'review-2 wrongs 25, 32, C(5, 2) = 10')

# ---------- homework-2 ----------
X = [1, frozenset({1}), frozenset({1, 2})]
lv.claim(1 in X and frozenset({1}) in X and all(e in X for e in {1}) and not all(e in X for e in {2}) and not all(e in X for e in {1, 2}) and frozenset({1, 2}) in X, 'homework-2 sets of sets: 1 in X, {1} in X and subset, {2}, {1, 2} not subsets')
lv.claim(all(X_ - (Y | Z) == (X_ - Y) & (X_ - Z) for X_ in S5 for Y in S5 for Z in S5), 'difference law A \\ (B u C) = (A \\ B) n (A \\ C), every triple')
lv.claim(not all(X_ - (Y | Z) == (X_ - Y) | (X_ - Z) for X_ in S5 for Y in S5 for Z in S5), 'the distractor form fails for some triple')
lv.claim(A - (B | C) == {2, 10} and B | C == {3, 4, 6, 8, 9, 12} and A - C == {2, 6, 10} and (A - B) | (A - C) == {2, 4, 6, 8, 10}, 'homework-2 diagram check {2, 10}; distractor set {2, 4, 6, 8, 10}')
gg = lambda x: 5 * x - 7
lv.claim(all(gg((y + 7) / 5) == y for y in range(-50, 51)), 'homework-2 g^-1(y) = (y + 7)/5')
lv.expect('homework', 'items[5].widget.answer', (8 + 7) / 5)
lv.claim(gg(8) == 33 and (8 - 7) / 5 == 0.2 and gg(3) == 8, 'homework-2 wrongs 33, 0.2; g(3) = 8')
n_onto = sum(1 for q in functions(range(4), range(3)) if onto(q, range(3)))
lv.expect('homework', 'items[6].widget.answer', n_onto)
lv.claim(6 * 6 == n_onto == 81 - 3 * 16 + 3 and 3 ** 4 == 81 and 4 * 3 * 2 == 24, 'homework-2 onto 4 to 3: C(4,2) x 3! = 36 = 81 - 48 + 3; wrongs 81, 6, 24')
ok_a = ok_b = True
ex_b = False
for nA, nB, nC in itertools.product(range(1, 4), repeat=3):
    for fA in functions(range(nA), range(nB)):
        for gB in functions(range(nB), range(nC)):
            comp = {a: gB[fA[a]] for a in fA}
            if inj(comp) and not inj(fA):
                ok_a = False
            if inj(fA) and inj(gB) and not inj(comp):
                ok_b = False
            if inj(comp) and not inj(gB):
                ex_b = True
lv.claim(ok_a, 'if g o f is one-to-one then f is (every f, g on sets of size 1 to 3)')
lv.claim(ok_b, 'f, g one-to-one gives g o f one-to-one (every case, sizes 1 to 3)')
lv.claim(ex_b, 'g o f one-to-one with g not one-to-one occurs (model counterexample type)')
lv.claim(inj({1: 1}) and not inj({1: 1, 2: 1}), 'homework-2 model (b): g o f on {1} one-to-one, g(1) = g(2) = 1')



# ---------- fix pass: the new wording must be present (a revert fails these) ----------
def has(ref, path, phrase, present=True):
    t = lv.text(ref, path)
    lv.claim((phrase in t) == present, f'{ref} {path} {"has" if present else "lacks"} {phrase!r}')

has('l9', 'screens[7].explain.text', r'Likewise $f^{-1}(5) = 1$, since $f(1) = 5$.')
has('l9', 'screens[7].explain.text', '-4', present=False)
lv.claim(finv(5) == 1 and f(1) == 5 and finv(11) == 3 and f(3) == 11, 'fix pass l9 explain: f^-1(5) = 1, f^-1(11) = 3')
has('l9', 'screens[4].widget.lines[0].text', 'be arbitrary, and suppose $f(a) = f(b)$')
has('l9', 'screens[3].hints[1].text', 'A proof of an implication starts by assuming its hypothesis.')
has('l7', 'screens[9].explain.text', 'A two-set Venn diagram also checks every case')
has('l7', 'screens[11].prose', '$M$')
has('homework', 'items[6].explain.text', r'$6 \times 6 = 36$ of the $3^4 = 81$ functions')
lv.claim(6 * 6 == 36 and 3 ** 4 == 81 and sum(1 for g in __import__('itertools').product(range(3), repeat=4) if len(set(g)) == 3) == 36, 'fix pass homework-2: 36 onto functions of the 81 from 4 to 3 (brute force)')
has('homework', 'items[7].widget.lines[0].text', 'be arbitrary, and suppose $f(a) = f(b)$')
has('homework', 'items[8].model', 'Let $a_1, a_2 \\in A$ be arbitrary, and suppose')
has('review', 'items[3].prose', '(set $R$)')
lv.claim(18 + 15 - 7 == 26 and 30 - 26 == 4, 'review-2 item 3: 18 + 15 - 7 = 26 trade, 4 do neither')

lv.check_wrongs()
lv.report()
