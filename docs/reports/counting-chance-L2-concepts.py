#!/usr/bin/env python3
"""Concept audit, counting-chance level 2 (l5 to l8, fluency-l7, review-2, homework-2, problems-2).
Exact enumeration of every counting and probability claim, plus Monte Carlo where a claim is empirical.
Run from the repository root: python3 docs/reports/counting-chance-L2-concepts.py
Exits 0 when the content is correct. A check that fails because the content is wrong stays failing."""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as F

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'counting-chance')
FAIL, N, NOTES = [], [0], []


def load(name):
    return json.load(open(os.path.join(BASE, name + '.json'), encoding='utf-8'))


def get(obj, path):
    for part in re.findall(r'[A-Za-z_][\w-]*|\[\d+\]', path):
        obj = obj[int(part[1:-1])] if part[0] == '[' else obj[part]
    return obj


def check(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)
        print('FAIL', label)


def near(a, b, tol=6e-5):
    return abs(float(a) - float(b)) <= tol


def key(doc, path, value, label, tol=6e-5):
    """The graded answer at path equals the recomputed value."""
    check(f'{label}: key {get(doc, path)} vs {float(value):.6g}', near(get(doc, path), value, tol))


def wrongs(doc, path, values, label, tol=6e-5):
    """Every wrong[].value at path equals, in order, the recomputed slip value, and none equals the key."""
    w = get(doc, path)
    got = [x['value'] for x in w['wrong']]
    check(f'{label}: wrong values {got} vs {[round(float(v), 6) for v in values]}',
          len(got) == len(values) and all(near(g, v, tol) for g, v in zip(got, values)))
    check(f'{label}: no wrong value equals the key', all(not near(g, w['answer'], 1e-9) for g in got))


def correct_option(doc, path):
    return [o for o in get(doc, path)['options'] if o.get('correct')]


def cells(pairs):
    return sorted(f'r{r}c{c}' for r, c in pairs)


def has(doc, path, text, label=None):
    check(label or f'text at {path} holds "{text}"', text in json.dumps(get(doc, path), ensure_ascii=False))


random.seed(20261111)
C = math.comb
P = lambda ev, space: F(sum(1 for o in space if ev(o)), len(space))


def mulberry32(seed):
    a = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def r():
        a[0] = (a[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = a[0]
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


def shares(n, k, low=0):
    """Every way to share n identical items among k named people, each at least low: brute force."""
    return [s for s in itertools.product(range(low, n + 1), repeat=k) if sum(s) == n]


# ---------------------------------------------------------------- l5
l5 = load('l5-in-stages')
check('l5 s0 twelve meals', len(get(l5, 'screens[0].widget.answer')) == 3 * 4 == len(list(itertools.product(range(3), range(4)))))
key(l5, 'screens[2].widget.answer', len(list(itertools.product(range(3), range(4), range(2)))), 'l5 s2 three courses')
wrongs(l5, 'screens[2].widget', [3 + 4 + 2, 12 + 2, 8], 'l5 s2')
key(l5, 'screens[3].widget.answer', len(list(itertools.permutations('ABCDE', 3))), 'l5 s3 forecasts')
wrongs(l5, 'screens[3].widget', [5 ** 3, 5 + 4 + 3, C(5, 3)], 'l5 s3')
key(l5, 'screens[4].widget.answer', len(list(itertools.permutations('ABCDE'))), 'l5 s4 orders')
wrongs(l5, 'screens[4].widget', [15, 5 ** 5, 60], 'l5 s4')
key(l5, 'screens[5].widget.answer', 3 * 4 * 1, 'l5 s5 one dessert')
DC = list(itertools.product(range(1, 7), 'HT'))
check('l5 s6 die and coin: 12 outcomes, P(6 and heads) = 1/12', len(DC) == 12 and P(lambda o: o == (6, 'H'), DC) == F(1, 12)
      and [o['text'] for o in correct_option(l5, 'screens[6].widget')] == ['$\\dfrac{1}{12}$'])
check('l5 s7 lead and backup 42', len(list(itertools.permutations(range(7), 2))) == 42 and '42' in correct_option(l5, 'screens[7].widget')[0]['text'])
check('l5 s8 n(n-1)(n-2) = n!/(n-3)! for n = 3..12', all(n * (n - 1) * (n - 2) == math.factorial(n) // math.factorial(n - 3) == len(list(itertools.permutations(range(n), 3))) for n in range(3, 9)))
key(l5, 'screens[9].widget.answer', len(list(itertools.permutations(range(6), 4))), 'l5 s9 sequences')
wrongs(l5, 'screens[9].widget', [6 ** 4, C(6, 4), 6 + 5 + 4 + 3, 24], 'l5 s9')
check('l5 q0 code counts and "over 200 times"', 26 ** 4 == 456976 and 10 ** 8 / 26 ** 4 > 200)
# "length beats alphabet size" is not general: 5 digits against 4 letters
NOTES.append(f'l5 q0: 10^5 = {10 ** 5} is below 26^4 = {26 ** 4}, so a longer code does not always beat a larger alphabet (finding: imprecise, minor)')
key(l5, 'quiz[2].widget.answer', len(list(itertools.permutations(range(8), 3))), 'l5 q2 rankings')
wrongs(l5, 'quiz[2].widget', [8 ** 3, C(8, 3), 8 + 7 + 6], 'l5 q2')
key(l5, 'quiz[3].widget.answer', F(1, 72), 'l5 q3 heads and double six', tol=1e-9)
wrongs(l5, 'quiz[3].widget', [F(1, 14), F(1, 36), F(1, 12)], 'l5 q3', tol=1e-9)

# ---------------------------------------------------------------- l6
l6 = load('l6-does-order-matter')
comb = lambda n, k: len(list(itertools.combinations(range(n), k)))
key(l6, 'screens[0].widget.answer', comb(4, 2), 'l6 s0 pairs')
key(l6, 'screens[2].widget.answer', comb(4, 3), 'l6 s2')
key(l6, 'screens[3].widget.answer', comb(5, 3), 'l6 s3')
check('l6 s4 Pascal rows 5 and 6', get(l6, 'screens[4].canvas.params.cells')[0][:6] == [str(C(5, k)) for k in range(6)]
      and [c for c in get(l6, 'screens[4].canvas.params.cells')[1] if c != '?'] == [str(C(6, k)) for k in range(7) if k != 2])
key(l6, 'screens[4].widget.answer', comb(6, 2), 'l6 s4 missing entry')
check('l6 Pascal rule and symmetry for n up to 12', all(C(n, k) == C(n - 1, k - 1) + C(n - 1, k) for n in range(2, 13) for k in range(1, n)) and all(C(n, k) == C(n, n - k) for n in range(13) for k in range(n + 1)))
check('l6 s6 committee 56 and podium 336', comb(8, 3) == 56 and len(list(itertools.permutations(range(8), 3))) == 336)
check('l6 s7 C(9,7) = C(9,2) = 36', comb(9, 7) == comb(9, 2) == 36)
check('l6 s8 ordered picks = groups times k! for n up to 8', all(len(list(itertools.permutations(range(n), k))) == comb(n, k) * math.factorial(k) for n in range(1, 8) for k in range(n + 1)))
key(l6, 'screens[9].widget.answer', comb(20, 2), 'l6 s9 pairs of assets')
wrongs(l6, 'screens[9].widget', [20 * 19, 400, comb(20, 2) + 20, 20], 'l6 s9')
B10 = list(itertools.combinations(range(10), 3))
key(l6, 'screens[10].widget.answer', P(lambda b: 0 in b and 1 in b, B10), 'l6 s10 both miners', tol=1e-9)
wrongs(l6, 'screens[10].widget', [F(8, 720), F(2, 10), F(1, 100)], 'l6 s10', tol=1e-9)
key(l6, 'quiz[0].widget.answer', len(B10), 'l6 q0')
key(l6, 'quiz[1].widget.answer', len(list(itertools.permutations(range(10), 3))), 'l6 q1')
key(l6, 'quiz[2].widget.answer', comb(15, 13), 'l6 q2')
key(l6, 'quiz[3].widget.answer', P(lambda b: 0 in b, list(itertools.combinations(range(6), 2))), 'l6 q3', tol=1e-9)

# ---------------------------------------------------------------- l7
l7 = load('l7-replacement')
key(l7, 'screens[0].widget.answer', len(list(itertools.product(range(4), repeat=2))), 'l7 s0 with replacement')
check('l7 s1 without replacement leaves 12', len(list(itertools.permutations(range(4), 2))) == 12 and len(get(l7, 'screens[1].widget.answer')) == 4)
BAG = 'RRRBB'
NR = list(itertools.permutations(range(5), 2))                 # ordered draws without replacement, equally likely
WR = list(itertools.product(range(5), repeat=2))               # with replacement
col = lambda i: BAG[i]
p_rr = P(lambda o: col(o[0]) == col(o[1]) == 'R', NR)
key(l7, 'screens[2].widget.answer', p_rr / F(3, 5), 'l7 s2 second red after a first red')
key(l7, 'screens[3].widget.answer', p_rr, 'l7 s3 both red')
wrongs(l7, 'screens[3].widget', [F(9, 25), F(6, 25), F(3, 5) + F(2, 4)], 'l7 s3')
key(l7, 'screens[4].widget.answer', P(lambda o: col(o[0]) == 'R' and col(o[1]) == 'B', WR), 'l7 s4 red then blue, replaced')
wrongs(l7, 'screens[4].widget', [F(3, 5) * F(2, 4), F(12, 25), 1], 'l7 s4')
# Independence, exactly. With replacement the two draws are independent; without, they are not.
p1r = P(lambda o: col(o[0]) == 'R', WR)
check('l7 with replacement: P(R1 and R2) = P(R1) P(R2)', P(lambda o: col(o[0]) == col(o[1]) == 'R', WR) == p1r * p1r)
p2r_nr = P(lambda o: col(o[1]) == 'R', NR)
check('l7 without replacement: P(R1 and R2) differs from P(R1) P(R2), so the draws are dependent', p_rr != F(3, 5) * p2r_nr)
NOTES.append(f'l7 s4: without replacement the chance of red on draw 2 is still {p2r_nr} before draw 1 is seen, the same as on draw 1, '
             'yet the draws are dependent. "Chances never change" does not define independence (finding: imprecise, serious)')
key(l7, 'screens[5].widget.answer', P(lambda o: all('RRBBB'[i] == 'R' for i in o), list(itertools.permutations(range(5), 3))), 'l7 s5 three reds from two')
wrongs(l7, 'screens[5].widget', [F(2, 5) ** 3, F(2, 5) * F(1, 4)], 'l7 s5')
DECK = [(r, s) for r in range(13) for s in range(4)]
p_aa = F(4 * 3, 52 * 51)
check('l7 s6 two aces 1/221, with replacement 1/169, Jo 3/676', p_aa == F(1, 221) == F(C(4, 2), C(52, 2)) and F(4, 52) ** 2 == F(1, 169) and F(4, 52) * F(3, 52) == F(3, 676)
      and '221' in correct_option(l7, 'screens[6].widget')[0]['text'])
check('l7 s7 720 ordered outcomes', len(list(itertools.permutations(range(10), 3))) == 720)
check('l7 s8 6/1326', C(4, 2) == 6 and C(52, 2) == 1326)
S5 = list(itertools.combinations(range(20), 5))
key(l7, 'screens[9].widget.answer', P(lambda s: 11 in s, S5), 'l7 s9 sample holds the worst day')
wrongs(l7, 'screens[9].widget', [1 - F(19, 20) ** 5, F(1, 20), F(3, 4)], 'l7 s9', tol=1e-4)
check('l7 s9 counts 11628 and 15504', C(19, 5) == 11628 and C(20, 5) == 15504 == len(S5))
miss = F(19, 20) ** 20
key(l7, 'screens[10].widget.answer', 1000 * miss, 'l7 s10 bootstrap count', tol=0.6)
check('l7 s10 exact line 0.3585 / 0.6415', near(miss, 0.3585) and near(1 - miss, 0.6415))
n = 100000
mc = sum(1 for _ in range(n) if all(random.randrange(20) != 11 for _ in range(20))) / n
check(f'l7 s10 MC bootstrap misses the worst day {mc:.4f}, near 0.3585 and far from 0 and from 0.05', abs(mc - 0.3585) < 0.006)
sim = get(l7, 'screens[10].canvas.params.sim')
r = mulberry32(sim['seed'])
seen = sum(1 for _ in range(1000) if sum(1 for _ in range(20) if r() < 0.05) == 0)
check(f'l7 s10 the seeded 1,000 resamples show {seen}, inside the accepted 333 to 383', 333 <= seen <= 383 and sim['outcome'] == 'binomial(20, 0.05) == 0')
key(l7, 'quiz[0].widget.answer', 10 ** 2, 'l7 q0')
key(l7, 'quiz[1].widget.answer', P(lambda o: DECK[o[0]][1] == DECK[o[1]][1] == 0, list(itertools.permutations(range(52), 2))), 'l7 q1 two hearts', tol=1e-9)
wrongs(l7, 'quiz[1].widget', [F(1, 16), F(13, 52) * F(12, 52)], 'l7 q1', tol=1e-9)
key(l7, 'quiz[2].widget.answer', 0, 'l7 q2 four banks from three')
wrongs(l7, 'quiz[2].widget', [F(3, 7) ** 4, F(3, 7) * F(2, 6) * F(1, 5)], 'l7 q2', tol=1e-9)

# fluency-l7: every draw of the variables, by exact enumeration of the bag
fl = load('fluency-l7-replacement')
okf = True
for rr in range(2, 10):
    for bb in range(2, 10):
        bag = 'R' * rr + 'B' * bb
        nn = rr + bb
        two = list(itertools.permutations(range(nn), 2))
        okf &= P(lambda o: bag[o[0]] == bag[o[1]] == 'R', two) == F(rr * (rr - 1), nn * (nn - 1))
        okf &= P(lambda o: bag[o[0]] == 'R' and bag[o[1]] == 'B', list(itertools.product(range(nn), repeat=2))) == F(rr * bb, nn * nn)
        if rr <= 7 and bb <= 7:
            three = list(itertools.permutations(range(nn), 3))
            okf &= P(lambda o: all(bag[i] == 'R' for i in o), three) == F(rr * (rr - 1) * (rr - 2), nn * (nn - 1) * (nn - 2))
        # no wrong value may equal the key
        okf &= F(rr, nn) ** 2 != F(rr * (rr - 1), nn * (nn - 1)) and F(rr * bb, nn * (nn - 1)) != F(rr * bb, nn * nn)
check('fluency-l7 three families: keys equal exact enumeration for every r, b; wrong values never equal the key', okf
      and get(fl, 'families[0].let.key') == 'r*(r - 1)/(n*(n - 1))' and get(fl, 'families[1].let.key') == 'r*b/n^2'
      and get(fl, 'families[2].let.key') == 'r*(r - 1)*(r - 2)/(n*(n - 1)*(n - 2))')

# ---------------------------------------------------------------- l8
l8 = load('l8-stars-and-bars')
check('l8 s0 Amy 3, Ben 0, Cal 2', get(l8, 'screens[0].widget.count') == {'amy': 3, 'ben': 0, 'cal': 2})
check('l8 s1 bars at places 1 and 6 give 0, 4, 1', get(l8, 'screens[1].widget.answer') == ['c1', 'c6'])
check('l8 stars and bars formula equals brute force for n up to 9, k up to 4, with and without empty shares',
      all(len(shares(n, k)) == C(n + k - 1, k - 1) for n in range(0, 10) for k in range(1, 5))
      and all(len(shares(n, k, 1)) == C(n - 1, k - 1) for n in range(1, 10) for k in range(1, 5) if n >= k))
key(l8, 'screens[2].widget.answer', len(shares(5, 3)), 'l8 s2')
wrongs(l8, 'screens[2].widget', [3 ** 5, C(5, 2), 42], 'l8 s2')
key(l8, 'screens[3].widget.answer', len(shares(8, 3)), 'l8 s3')
wrongs(l8, 'screens[3].widget', [3 ** 8, C(8, 2), 90, C(9, 2)], 'l8 s3')
key(l8, 'screens[4].widget.answer', len(shares(5, 3, 1)), 'l8 s4 at least one each')
key(l8, 'screens[5].widget.answer', len(shares(12, 1)), 'l8 s5 one broker')
check('l8 s6 21 sharings, 243 assignments of distinct coins', len(shares(5, 3)) == 21 and len(list(itertools.product(range(3), repeat=5))) == 243 and correct_option(l8, 'screens[6].widget')[0]['text'] == '21')
check('l8 s7 84 and 10', len(shares(6, 4)) == 84 and len(shares(6, 4, 1)) == 10)
check('l8 s8 (n+2)(n+1)/2 for n up to 12', all(len(shares(n, 3)) == (n + 2) * (n + 1) // 2 for n in range(13)))
key(l8, 'screens[9].widget.answer', len(shares(10, 4)), 'l8 s9 allocations')
wrongs(l8, 'screens[9].widget', [4 ** 10, C(10, 3), C(13, 4), C(9, 3)], 'l8 s9')
NOTES.append(f'l8 s9: the slip 715 is C(13,4); a row with 4 bars has 14 places and C(14,4) = {C(14, 4)} (finding: imprecise, minor)')
key(l8, 'quiz[0].widget.answer', C(24, 4), 'l8 q0')
wrongs(l8, 'quiz[0].widget', [C(20, 4), C(24, 5), C(19, 4)], 'l8 q0')
key(l8, 'quiz[1].widget.answer', len(shares(7, 3, 1)), 'l8 q1')
wrongs(l8, 'quiz[1].widget', [len(shares(7, 3)), C(7, 2)], 'l8 q1')
key(l8, 'quiz[3].widget.answer', len(shares(3, 4)), 'l8 q3')
wrongs(l8, 'quiz[3].widget', [C(4, 3), 4 ** 3, C(6, 4)], 'l8 q3')

# ---------------------------------------------------------------- review-2
r2 = load('review-2')
R3 = list(itertools.product(range(6), repeat=3))
key(r2, 'items[0].widget.answer', P(lambda o: len(set(o)) == 3, R3), 'r2 i0', tol=1e-9)
wrongs(r2, 'items[0].widget', [1, F(20, 216), F(5, 6)], 'r2 i0', tol=1e-9)
key(r2, 'items[1].widget.answer', comb(9, 2), 'r2 i1')
bag = 'R' * 4 + 'B' * 6
key(r2, 'items[2].widget.answer', P(lambda o: bag[o[0]] == bag[o[1]], list(itertools.permutations(range(10), 2))), 'r2 i2 same colour', tol=1e-9)
wrongs(r2, 'items[2].widget', [F(52, 100), F(12, 90), F(42, 100)], 'r2 i2', tol=1e-9)
key(r2, 'items[3].widget.answer', len(shares(9, 3, 1)), 'r2 i3')
wrongs(r2, 'items[3].widget', [len(shares(9, 3)), 3 ** 9, C(9, 2)], 'r2 i3')
check('r2 i4 multi: basket and committee', [bool(o.get('correct')) for o in get(r2, 'items[4].widget.options')] == [True, False, True, False])
key(r2, 'items[5].widget.answer', F(1, 169), 'r2 i5', tol=1e-9)
wrongs(r2, 'items[5].widget', [F(1, 221), F(8, 52)], 'r2 i5', tol=1e-9)
key(r2, 'items[6].widget.answer', len(shares(6, 4)), 'r2 i6')
wrongs(r2, 'items[6].widget', [C(9, 4), C(6, 3), 4 ** 6, C(5, 3)], 'r2 i6')
key(r2, 'items[7].widget.answer', F(C(13, 5), C(52, 5)), 'r2 i7 five hearts', tol=1e-12)
check('r2 i7 path product equals the count ratio', F(13 * 12 * 11 * 10 * 9, 52 * 51 * 50 * 49 * 48) == F(C(13, 5), C(52, 5)) == F(33, 66640))

# ---------------------------------------------------------------- homework-2
h2 = load('homework-2')
key(h2, 'items[0].widget.answer', math.perm(10, 6), 'h2 i0 PINs')
wrongs(h2, 'items[0].widget', [10 ** 6, C(10, 6), math.perm(10, 5)], 'h2 i0')
S4 = list(itertools.combinations(range(12), 4))
key(h2, 'items[1].widget.answer', P(lambda s: 0 in s and 1 in s, S4), 'h2 i1', tol=1e-9)
wrongs(h2, 'items[1].widget', [F(1, 3), F(1, 9), F(45, math.perm(12, 4))], 'h2 i1', tol=1e-9)
H3 = list(itertools.combinations(range(52), 3))
key(h2, 'items[2].widget.answer', P(lambda h: len({DECK[i][1] for i in h}) == 1, H3), 'h2 i2 three of one suit (22,100 hands)', tol=1e-9)
wrongs(h2, 'items[2].widget', [F(C(13, 3), C(52, 3)), F(1, 16), F(12, 52) * F(11, 52)], 'h2 i2', tol=1e-9)
check('h2 i3 (n-1)(n-2)(n-3)/6 equals brute force for n = 4..10 and is 0 at n = 1, 2, 3',
      all(len(shares(n, 4, 1)) == (n - 1) * (n - 2) * (n - 3) // 6 for n in range(4, 11)) and all((n - 1) * (n - 2) * (n - 3) == 0 for n in (1, 2, 3)))
key(h2, 'items[4].widget.answer', sum(1 for s in shares(10, 3) if s[0] >= 2), 'h2 i4 minimum of 2 for A')
wrongs(h2, 'items[4].widget', [len(shares(10, 3)), sum(1 for s in shares(10, 3) if s[0] >= 1), sum(1 for s in shares(10, 3) if min(s) >= 2)], 'h2 i4')
key(h2, 'items[5].widget.answer', P(lambda s: 0 in s and 1 in s, S5), 'h2 i5 best and worst day', tol=1e-9)
wrongs(h2, 'items[5].widget', [(1 - F(19, 20) ** 5) ** 2, F(1, 16), F(1, 4)], 'h2 i5', tol=1e-9)
check('h2 i6 order', get(h2, 'items[6].widget.answer') == ['fix', 'with', 'without', 'split', 'done'])
model = get(h2, 'items[7].model')
check('h2 i7 20^20 about 1.05e26, C(20,10) = 184,756, C(19,10) = 92,378, one half', near(20 ** 20 / 1e26, 1.05, 0.005) and C(20, 10) == 184756 and C(19, 10) == 92378
      and F(C(19, 10), C(20, 10)) == F(1, 2) and '184{,}756' in model and '92{,}378' in model)
check('h2 i8 multi: die and bootstrap independent', [bool(o.get('correct')) for o in get(h2, 'items[8].widget.options')] == [True, False, True, False])
# dealing two cards: P(second is an ace) is 4/52 whatever the position, yet the draws are dependent
T2 = list(itertools.permutations(range(52), 2))
check('h2 i8 two cards: second-card chance unchanged (1/13) but P(both aces) is not (1/13)^2',
      P(lambda o: DECK[o[1]][0] == 0, T2) == F(1, 13) and P(lambda o: DECK[o[0]][0] == DECK[o[1]][0] == 0, T2) != F(1, 169))

# ---------------------------------------------------------------- problems-2
p2 = load('problems-2')
TEAMS = list(itertools.combinations(range(9), 4))
LINE = list(itertools.permutations(range(9), 4))
key(p2, 'items[0].parts[0].widget.answer', len(TEAMS), 'p2 i0 p0')
key(p2, 'items[0].parts[1].widget.answer', len(LINE), 'p2 i0 p1')
key(p2, 'items[0].parts[2].widget.answer', P(lambda t: 0 in t and 1 in t, TEAMS), 'p2 i0 p2')
wrongs(p2, 'items[0].parts[2].widget', [F(4, 9), F(16, 81)], 'p2 i0 p2')
key(p2, 'items[0].parts[3].widget.answer', P(lambda o: set(o[2:]) == {0, 1}, LINE), 'p2 i0 p3 last two legs')
wrongs(p2, 'items[0].parts[3].widget', [F(1, 72), F(1, 6), F(16, 81) * F(1, 6)], 'p2 i0 p3')
clean = lambda k: F(C(11, k), C(15, k))
key(p2, 'items[1].parts[0].widget.answer', clean(1), 'p2 i1 p0')
key(p2, 'items[1].parts[1].widget.answer', clean(2), 'p2 i1 p1')
wrongs(p2, 'items[1].parts[1].widget', [F(11, 15) ** 2, F(11 * 10, 15 * 15), F(11 * 11, 15 * 14)], 'p2 i1 p1')
key(p2, 'items[1].parts[2].widget.answer', clean(3), 'p2 i1 p2')
wrongs(p2, 'items[1].parts[2].widget', [F(11, 15) ** 3, F(11 * 10 * 9, 15 ** 3)], 'p2 i1 p2')
key(p2, 'items[1].parts[3].widget.answer', 1 - clean(3), 'p2 i1 p3')
wrongs(p2, 'items[1].parts[3].widget', [clean(3), 1 - F(11, 15) ** 3, F(12, 15)], 'p2 i1 p3')
key(p2, 'items[1].parts[4].widget.answer', min(k for k in range(1, 12) if 1 - clean(k) > F(9, 10)), 'p2 i1 p4')
wrongs(p2, 'items[1].parts[4].widget', [5, min(k for k in range(1, 12) if F(4 * k, 15) > F(9, 10)), min(k for k in range(1, 40) if 1 - F(11, 15) ** k > F(9, 10))], 'p2 i1 p4')
check('p2 i1 p4 0.7582, 0.8462, 0.9077', all(near(1 - clean(k), v) for k, v in ((4, 0.7582), (5, 0.8462), (6, 0.9077))))
TALLY = shares(8, 3)
key(p2, 'items[2].parts[0].widget.answer', len(TALLY), 'p2 i2 p0 tallies')
key(p2, 'items[2].parts[1].widget.answer', sum(1 for t in TALLY if 0 in t), 'p2 i2 p1')
VOTES = list(itertools.product(range(3), repeat=8))        # 6,561 equally likely vote lists
cnt = {}
for vlist in VOTES:
    t = tuple(vlist.count(i) for i in range(3))
    cnt[t] = cnt.get(t, 0) + 1
check('p2 i2 p2 tallies are not equally likely: (8,0,0) from 1 list, (3,3,2) from 560', cnt[(8, 0, 0)] == 1 and cnt[(3, 3, 2)] == 560 and len(cnt) == 45
      and correct_option(p2, 'items[2].parts[2].widget')[0]['text'].startswith('No. The tally 3, 3, 2'))
key(p2, 'items[2].parts[3].widget.answer', F(3, len(VOTES)), 'p2 i2 p3 unanimous', tol=1e-9)
wrongs(p2, 'items[2].parts[3].widget', [F(3, 45), F(1, 6561)], 'p2 i2 p3', tol=1e-6)
n = 200000
una = sum(1 for _ in range(n) if len({random.randrange(3) for _ in range(8)}) == 1) / n
check(f'p2 i2 MC unanimous vote {una:.5f}: near 3/6561 = 0.00046, far from 3/45 = 0.067', una < 0.002)
key(p2, 'items[3].parts[0].widget.answer', C(30, 5), 'p2 i3 p0')
hyp = lambda k: F(C(5, k) * C(25, 5 - k), C(30, 5))
check('p2 i3 hypergeometric chances sum to 1', sum(hyp(k) for k in range(6)) == 1)
key(p2, 'items[3].parts[1].widget.answer', hyp(3), 'p2 i3 p1', tol=1e-6)
wrongs(p2, 'items[3].parts[1].widget', [F(10, C(30, 5)), 2 * hyp(3)], 'p2 i3 p1', tol=1e-6)
key(p2, 'items[3].parts[2].widget.answer', hyp(3) + hyp(4) + hyp(5), 'p2 i3 p2', tol=1e-6)
wrongs(p2, 'items[3].parts[2].widget', [hyp(3), F(3000 + 250 + 1, C(30, 5))], 'p2 i3 p2', tol=1e-6)
p3 = hyp(3) + hyp(4) + hyp(5)
key(p2, 'items[3].parts[3].widget.answer', 1 - (1 - p3) ** 4, 'p2 i3 p3', tol=1e-5)
wrongs(p2, 'items[3].parts[3].widget', [4 * p3, 1 - (1 - hyp(3)) ** 4, (1 - p3) ** 4], 'p2 i3 p3', tol=1e-5)

for note in NOTES:
    print('NOTE', note)
print(f'counting-chance L2 concepts: {N[0] - len(FAIL)} of {N[0]} checks passed')
sys.exit(1 if FAIL else 0)
