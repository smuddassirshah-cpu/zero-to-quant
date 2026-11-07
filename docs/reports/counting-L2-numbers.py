"""Second-reader number check for counting level 2 (l5 to l8, review-2, homework-2), written by the session V reader
(docs/reviews/review-counting-1-3.md). Every count is found twice: method 1 enumerates (itertools: distinct
permutations, grid routes as R/U words, seatings, dice, cards, weak orders), method 2 uses the lesson's formula.
Long words (MISSISSIPPI, STATISTICS) are enumerated letter by letter as a tree of words, counted leaf by leaf.
A check marked FINDING fails while the content is wrong and passes once the fix in the review lands.
Run: python3 docs/reports/counting-L2-numbers.py   (exits 0 when every check passes)
"""
import itertools as it
import math
import os
import sys
from fractions import Fraction as Fr
from functools import lru_cache
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("counting", 2)
C, F = math.comb, math.factorial
L = lambda f: lv.files[f]


def two(label, brute, formula):
    lv.claim(brute == formula, f'{label}: brute {brute} = formula {formula}')
    return formula


def E(f, path, *vals):
    for v in vals:
        lv.expect(f, path, v)


def distinct(word):
    return len(set(it.permutations(word)))


def words_tree(word):
    """Count distinct arrangements by building them letter by letter (each leaf is one word)."""
    counts = tuple(sorted(word.count(c) for c in set(word)))

    @lru_cache(None)
    def go(cs):
        if sum(cs) == 0:
            return 1
        return sum(go(tuple(sorted(cs[:i] + (cs[i] - 1,) + cs[i + 1:]))) for i in range(len(cs)) if cs[i])
    return go(counts)


def multinom(word):
    out = F(len(word))
    for c in set(word):
        out //= F(word.count(c))
    return out


def adjacent(seq, a, b):
    return abs(seq.index(a) - seq.index(b)) == 1


def routes(r, u):
    return [w for w in set(it.permutations('R' * r + 'U' * u))]


def cells(word):
    x = y = 0; out = [(0, 0)]
    for s in word:
        x, y = (x + 1, y) if s == 'R' else (x, y + 1)
        out.append((x, y))
    return out


def rc(cell, rows):            # canvas id rRcC -> (x, y) with Start at the bottom left
    r, c = cell[1:].split('c')
    return (int(c) - 1, rows - int(r))


def circular(people):
    seen = set()
    for s in it.permutations(people):
        i = s.index(people[0]); seen.add(s[i:] + s[:i])
    return seen


def weak_orders(n):
    """Every ranking of n items with ties allowed: tuples of block levels 0..k-1 with no gap."""
    for lev in it.product(range(n), repeat=n):
        if set(lev) == set(range(max(lev) + 1)):
            yield lev


# ---------------- l5 repeats ----------------
E('l5', 'screens[1].widget.answer', two('l5 EGG', distinct('EGG'), multinom('EGG')))
E('l5', 'screens[1].widget.wrong', F(3), 27)
lab = [c for row in L('l5-repeats')['screens'][2]['canvas']['params']['cells'] for c in row]
lv.claim(len(set(lab)) == 6 and {x.replace(' ', '').replace('₁', '').replace('₂', '') for x in lab} == {'GEG', 'EGG', 'GGE'}, 'l5 s2: the 6 labelled orders cover EGG, GEG, GGE')
ans = L('l5-repeats')['screens'][2]['widget']['answer']
lv.claim(all(L('l5-repeats')['screens'][2]['canvas']['params']['cells'][int(a[1]) - 1][int(a[3]) - 1].replace(' ', '').translate({ord('₁'): None, ord('₂'): None}) == 'GEG' for a in ans) and len(ans) == 2, 'l5 s2 key cells read GEG')
grid = L('l5-repeats')['screens'][3]['canvas']['params']['cells']
flat = [c for row in grid for c in row]
lv.claim(len(set(flat)) == 24 and set(flat) == {''.join(p) for p in it.permutations(['B', 'K', 'O₁', 'O₂'])}, 'l5 s3: the grid lists all 24 labelled orders of BOOK once')
lv.claim(all(row[i].replace('O₁', 'X').replace('O₂', 'O₁').replace('X', 'O₂') == row[i + 1] for row in grid for i in (0, 2, 4)), 'l5 s3: each pair of twins sits side by side')
E('l5', 'screens[3].widget.answer', two('l5 BOOK', distinct('BOOK'), multinom('BOOK')))
E('l5', 'screens[3].widget.wrong', 24, 6)
E('l5', 'screens[4].widget.answer', two('l5 ERROR', distinct('ERROR'), multinom('ERROR')))
E('l5', 'screens[4].widget.wrong', 120 // 2, 120 // 3, 120)
E('l5', 'screens[5].widget.answer', two('l5 BANANA', distinct('BANANA'), multinom('BANANA')))
E('l5', 'screens[5].widget.wrong', 720 // 6, 720 // 2, 720 // 8, 720)
rt = routes(3, 2)
E('l5', 'screens[6].widget.answer', two('l5 routes 3R 2U', len(rt), C(5, 2)))
E('l5', 'screens[6].widget.wrong', 120, 120 // 6, 12, 5)
shade = [rc(c, 3) for c in L('l5-repeats')['screens'][6]['canvas']['state']['shade']['route']]
lv.claim(shade == cells('RURRU'), 'l5 s6: the shaded cells are the route R U R R U')
E('l5', 'screens[7].widget.options', two('l5 coloured tiles', distinct(['B', 'Ob', 'Oo', 'K']), F(4)), 12, 6, 48)
miss = two('l5 MISSISSIPPI', words_tree('MISSISSIPPI'), multinom('MISSISSIPPI'))
lv.claim(F(4) * F(4) * F(2) == 1152 and F(11) == 39916800, 'l5 s8: 4!4!2! = 1152, 11! = 39916800')
E('l5', 'screens[8].widget.lines[3].text', miss)
E('l5', 'screens[8].explain.text', 1152, 39916800, miss)
lv.claim(miss == 34650, 'l5 s8: 11!/(4!4!2!) = 34650')
lv.expect('l5', 'screens[8].widget.lines[3].text', '34\\,650')
lv.expect('l5', 'screens[8].explain.text', '\\tfrac{39\\,916\\,800}{1152} = 34\\,650')
weeks = [w for w in it.product('UD', repeat=5) if w.count('D') == 2]
E('l5', 'screens[9].widget.answer', two('l5 weeks with 2 downs', len(weeks), C(5, 2)))
E('l5', 'screens[9].widget.wrong', 120 // 6, 120, 32)
lv.claim(all(50 + w.count('U') - w.count('D') == 51 for w in weeks), 'l5 s9: every 2-down week ends at £51.00')
E('l5', 'quiz[0].widget.options', two('l5 LEVEL', distinct('LEVEL'), multinom('LEVEL')), 60, 15, 120)
E('l5', 'quiz[1].widget.answer', two('l5 four coins', distinct('1111'), 1))
E('l5', 'quiz[1].widget.wrong', 24, 6)
E('l5', 'quiz[2].widget.answer', two('l5 routes 4R 3U', len(routes(4, 3)), C(7, 3)))
E('l5', 'quiz[2].widget.wrong', 5040, 5040 // 24, 7)
E('l5', 'quiz[3].widget.options', two('l5 6 steps 4 up', sum(1 for w in it.product('UD', repeat=6) if w.count('U') == 4), C(6, 4)), 30, 64, 360)

# ---------------- l6 together or apart ----------------
g1 = L('l6-together-or-apart')['screens'][1]
cell = lambda g, i: g['canvas']['params']['cells'][int(i[1]) - 1][int(i[3]) - 1]
lv.claim(sorted(cell(g1, i) for i in g1['widget']['answer']) == sorted(''.join(s) for s in it.permutations('ABC') if adjacent(s, 'A', 'B')), 'l6 s1 key = the seatings with A and B adjacent')
lv.claim(sorted(cell(g1, i) for i in g1['widget']['wrong'][0]['set']) == ['ABC', 'CAB'], 'l6 s1 one-way set = Ana on the left of Ben')
g2 = L('l6-together-or-apart')['screens'][2]
lv.claim(sorted(cell(g2, i) for i in g2['widget']['answer']) == sorted(''.join(s) for s in it.permutations('ABCD') if 'AB' in ''.join(s)), 'l6 s2 key = the 6 seatings containing AB')
lv.claim(sorted(cell(g2, i) for i in g2['widget']['wrong'][0]['set']) == sorted(''.join(s) for s in it.permutations('ABCD') if adjacent(s, 'A', 'B')), 'l6 s2 both-ways set = the 12 with A, B adjacent')
lv.claim(all('BA' in cell(g2, k) for k in g2['feedback']['byKey'] if k.startswith('r')), 'l6 s2 byKey cells all hold the block BA')
together5 = two('l6 5 in a row, A B together', sum(1 for s in it.permutations('ABCDE') if adjacent(s, 'A', 'B')), F(4) * 2)
E('l6', 'screens[3].widget.answer', together5)
E('l6', 'screens[3].widget.wrong', 24, 120, 240)
trio = two('l6 6 in a row, ABC together', sum(1 for s in it.permutations('ABCDEF') if max(map(s.index, 'ABC')) - min(map(s.index, 'ABC')) == 2), F(4) * F(3))
E('l6', 'screens[4].widget.answer', trio)
E('l6', 'screens[4].widget.wrong', 24, 48, 720)
apart5 = two('l6 5 in a row, A B apart', sum(1 for s in it.permutations('ABCDE') if not adjacent(s, 'A', 'B')), F(5) - 48)
E('l6', 'screens[5].widget.answer', apart5)
E('l6', 'screens[5].widget.wrong', 48, 120, 120 - 24)
rnd5 = two('l6 round table of 5', len(circular('ABCDE')), F(4))
E('l6', 'screens[6].widget.answer', rnd5)
E('l6', 'screens[6].widget.wrong', 120, 12, 119)
mir = set()
for s in circular('ABCDE'):
    r = tuple(reversed(s)); i = r.index('A'); mir.add(min(s, r[i:] + r[:i]))
lv.claim(len(mir) == 12, 'l6 s6: treating mirror images as one gives 12 (the slip value)')
nodes = L('l6-together-or-apart')['screens'][6]['canvas']['params']['nodes']
left = [n['label'] for n in nodes[:5]]; right = [n['label'] for n in nodes[5:]]
lv.claim(right == left[-1:] + left[:-1], 'l6 s6 canvas: the right table is everyone moved one seat round')
t7 = [n['label'].split()[1] for n in L('l6-together-or-apart')['screens'][7]['canvas']['params']['nodes']]
lv.claim(t7[5:] == t7[4:5] + t7[:4], 'l6 s7 canvas: right table is one seat round')
E('l6', 'screens[7].widget.options', two('l6 numbered seats', len(list(it.permutations('ABCDE'))), 120), 24, 600, 12)
for n in range(3, 9):
    lv.claim(F(n) - 2 * F(n - 1) == (n - 2) * F(n - 1), f'l6 s8: n! - 2(n-1)! = (n-2)(n-1)! at n = {n}')
lv.claim(3 * 24 == apart5, 'l6 s8: (n-2)(n-1)! = 72 at n = 5')
tie = two('l6 transfer ranking with A = B', sum(1 for lev in weak_orders(5) if lev[0] == lev[1] and len(set(lev)) == 4), F(4))
E('l6', 'screens[9].widget.options', tie, 48, 60, 120)
E('l6', 'quiz[0].widget.options', two('l6 quiz 6 in a row, pair together', sum(1 for s in it.permutations(range(6)) if adjacent(s, 0, 1)), F(5) * 2), 120, 720, 480)
E('l6', 'quiz[1].widget.answer', two('l6 round table of 6', len(circular('ABCDEF')), F(5)))
E('l6', 'quiz[1].widget.wrong', 720, 60)
E('l6', 'quiz[2].widget.answer', two('l6 quiz 6 apart', sum(1 for s in it.permutations(range(6)) if not adjacent(s, 0, 1)), 720 - 240))
E('l6', 'quiz[2].widget.wrong', 240, 720 - 120, 720)
rp = two('l6 round 4, A B neighbours', sum(1 for s in circular('ABCD') if adjacent(s + s[:1], 'A', 'B') or {s[0], s[-1]} == {'A', 'B'}), 2 * 2)
E('l6', 'quiz[3].widget.options', rp, 12, 2, 6)

# ---------------- l7 complements ----------------
dice2 = list(it.product(range(1, 7), repeat=2))
no6 = two('l7 two dice no 6', sum(1 for d in dice2 if 6 not in d), 5 * 5)
E('l7', 'screens[1].widget.answer', no6)
E('l7', 'screens[1].widget.wrong', 36 - 6, 36 - 12, 11)
lv.claim(sum(1 for d in dice2 if 6 in d) == 11 == len(L('l7-what-you-do-not-want')['screens'][2]['widget']['answer']), 'l7 s2: 11 outcomes with a 6')
d3 = two('l7 three dice at least one 6', sum(1 for d in it.product(range(1, 7), repeat=3) if 6 in d), 6 ** 3 - 5 ** 3)
E('l7', 'screens[3].widget.answer', d3)
E('l7', 'screens[3].widget.wrong', 3 * 36, 125, 216, 18)
p0 = two('l7 PINs with a 0', sum(1 for p in it.product(range(10), repeat=4) if 0 in p), 10 ** 4 - 9 ** 4)
E('l7', 'screens[4].widget.answer', p0)
E('l7', 'screens[4].widget.wrong', 4000, 6561, 10000, 1000)
lv.expect('l7', 'screens[4].explain.text', '$10^4 = 10\\,000$. No 0: $9^4 = 6561$. So $10\\,000 - 6561 = 3439$')
lv.expect('l7', 'screens[4].feedback.correct', '$10\\,000 - 6561 = 3439$')
lv.expect('l7', 'screens[4].hints[2].text', '$10^4 - 9^4 = 10\\,000 - 6561$')
v5 = L('l7-what-you-do-not-want')['screens'][5]['canvas']['params']['values']
lv.claim(sum(v5.values()) == 30 and v5['A'] + v5['AB'] + v5['B'] == 26 == 30 - v5['none'], 'l7 s5 venn: 11 + 7 + 8 = 26 = 30 - 4')
v6 = L('l7-what-you-do-not-want')['screens'][6]['canvas']['params']['values']
lv.claim(v6['A'] + v6['AB'] == 22 and v6['B'] + v6['AB'] == 15 and sum(v6.values()) == 40, 'l7 s6 venn regions match 22, 15, 9, 40')
E('l7', 'screens[6].widget.answer', 22 + 15 - 9)
E('l7', 'screens[6].widget.wrong', 22 + 15, 22 + 15 - 18, 40 - 28, 40 - 22 - 15)
lv.claim('and then the 9' not in lv.text('l7', 'screens[6].feedback.byKey.minus-all') and 40 - 22 - 15 == 3,
         'l7 s6 byKey.minus-all: the slip is 40 - 22 - 15 = 3 (no extra "then the 9")')
lv.expect('l7', 'screens[6].feedback.byKey.minus-all', '$40 - 22 - 15 = 3$')
E('l7', 'screens[6].explain.text', 13, 6, 28)
E('l7', 'screens[8].widget.answer', two('l7 weeks with a down day', sum(1 for w in it.product('UD', repeat=5) if 'D' in w), 2 ** 5 - 1))
E('l7', 'screens[8].widget.wrong', 32, 5, 1, 10)
v9 = L('l7-what-you-do-not-want')['screens'][9]['canvas']['params']['values']
lv.claim(v9['A'] + v9['AB'] == 60 and v9['B'] + v9['AB'] == 45 and sum(v9.values()) == 250, 'l7 s9 venn regions match 60, 45, 20, 250')
E('l7', 'screens[9].widget.answer', 250 - (60 + 45 - 20))
E('l7', 'screens[9].widget.wrong', 250 - 60 - 45, 85, 230)
E('l7', 'quiz[0].widget.options', two('l7 1..100 by 2 or 5', sum(1 for k in range(1, 101) if k % 2 == 0 or k % 5 == 0), 50 + 20 - 10), 70, 50, 40)
E('l7', 'quiz[1].widget.answer', two('l7 three coins a head', sum(1 for w in it.product('HT', repeat=3) if 'H' in w), 7))
E('l7', 'quiz[1].widget.wrong', 8, 3, 6)
E('l7', 'quiz[2].widget.options', two('l7 weeks >= 2 downs', sum(1 for w in it.product('UD', repeat=5) if w.count('D') >= 2), 32 - 1 - 5), 31, 30, 10)
hands2 = list(it.combinations(range(52), 2))
noace = sum(1 for h in hands2 if min(h) >= 4)
two('l7 C(52,2)', len(hands2), 1326); two('l7 C(48,2)', noace, 1128)
E('l7', 'quiz[3].widget.answer', two('l7 two-card hands with an ace', sum(1 for h in hands2 if min(h) < 4), 1326 - 1128))
E('l7', 'quiz[3].widget.wrong', 4 * 51, 1128)
lv.claim(4 * 51 - 198 == sum(1 for h in hands2 if max(h) < 4) == 6, 'l7 quiz[3]: 204 over-counts the 6 two-ace hands')

# ---------------- l8 counts to chances ----------------
pr = list(it.combinations('ABCDE', 2))
lv.claim(Fr(sum(1 for p in pr if set(p) == {'A', 'B'}), len(pr)) == Fr(1, 10), 'l8 s1: P(AB) = 1/10')
lv.claim(Fr(sum(1 for p in pr if 'C' in p), len(pr)) == Fr(2, 5), 'l8 s2: P(C picked) = 4/10 = 2/5')
lv.claim(len(L('l8-counts-to-chances')['screens'][2]['widget']['answer']) == 4, 'l8 s2: 4 cells hold C')
nei = Fr(sum(1 for p in pr if not set(p) & {'A', 'B'}), len(pr))
E('l8', 'screens[3].widget.answer', float(two('l8 neither A nor B', nei, Fr(3, 10))))
E('l8', 'screens[3].widget.wrong', 0.7, (3 / 5) ** 2, 3 / 5)
ports = [(s, b) for s in it.combinations(range(8), 3) for b in it.combinations(range(5), 2)]
E('l8', 'screens[4].widget.answer', two('l8 portfolios 3 of 8 and 2 of 5', len(ports), C(8, 3) * C(5, 2)))
E('l8', 'screens[4].widget.wrong', 56 + 10, C(13, 5), 336 * 20)
s1 = Fr(sum(1 for s, b in ports if 0 in s), len(ports))
E('l8', 'screens[5].widget.answer', float(two('l8 P(S1 in)', s1, Fr(3, 8))))
E('l8', 'screens[5].widget.wrong', 1 / 8, round(1 / 560, 4), 0.5)
lv.claim(sum(1 for s, b in ports if 0 in s) == 210, 'l8 s5: 210 portfolios hold S1')
thr = Fr(sum(1 for w in rt if (1, 1) in cells(w)), len(rt))
lv.claim(rc('r2c2', 3) == (1, 1), 'l8 s6: marked cell r2c2 is one right, one up')
E('l8', 'screens[6].widget.answer', float(two('l8 routes through marked cell', thr, Fr(6, 10))))
E('l8', 'screens[6].widget.wrong', 0.5, round(1 / 12, 4), 0.2, 0.3)
tech = Fr(sum(1 for p in pr if set(p) <= set('ABC')), len(pr))
lv.claim(tech == Fr(3, 10) == Fr(6, 20), 'l8 s7: tech pairs 3/10 = 6/20')
E('l8', 'screens[7].widget.options', 6, 3, 9, 25)
paths = list(it.product('ud', repeat=4))
leaves = L('l8-counts-to-chances')['screens'][9]['canvas']['params']['leaves']
lv.claim(all(leaves['-'.join(p)] == f'£{100 + 5 * (p.count("u") - p.count("d")):.2f}' for p in paths), 'l8 s9 tree: every leaf price is 100 + 5(ups - downs)')
end100 = Fr(sum(1 for p in paths if p.count('u') == 2), len(paths))
E('l8', 'screens[9].widget.answer', float(two('l8 price ends at £100', end100, Fr(6, 16))))
E('l8', 'screens[9].widget.wrong', 1 / 5, 1 / 16, 0.5, 6)
lv.claim(len({p.count('u') for p in paths}) == 5, 'l8 s9: five end prices')
hearts = Fr(sum(1 for h in hands2 if h[0] // 13 == 0 and h[1] // 13 == 0), len(hands2))
lv.claim(hearts == Fr(1, 17) and Fr(13 * 12, 1326) == Fr(2, 17), 'l8 quiz[0]: P(two hearts) = 78/1326 = 1/17; mixed count 2/17')
E('l8', 'quiz[0].explain.text', 78, 1326)
E('l8', 'quiz[1].widget.answer', two('l8 committee 2 of 6 and 1 of 4', sum(1 for _ in it.product(it.combinations(range(6), 2), range(4))), 60))
E('l8', 'quiz[1].widget.wrong', 15 + 4, C(10, 3))
lv.claim(C(10, 3) == 6 * 5 * 4 == 120, 'l8 quiz[1] byKey.pooled: both routes give 120')
up2 = Fr(sum(1 for p in it.product('ud', repeat=5) if p.count('u') == 2), 32)
E('l8', 'quiz[2].widget.answer', float(two('l8 5 steps 2 ups', up2, Fr(10, 32))))
E('l8', 'quiz[2].widget.wrong', round(1 / 6, 4), 1 / 32, 0.4)
r42 = routes(4, 2)
first = Fr(sum(1 for w in r42 if w[0] == 'R'), len(r42))
lv.claim(first == Fr(2, 3) and len(r42) == 15, 'l8 quiz[3]: 10 of 15 routes start with R')

# ---------------- review-2 ----------------
E('review', 'items[0].widget.answer', two('review-2 COFFEE', distinct('COFFEE'), multinom('COFFEE')))
E('review', 'items[0].widget.wrong', 360, 720)
def dict_in_order(s):
    return all(s.index(k + 1) == s.index(k) + 1 for k in (0, 1))
def dict_together(s):
    return max(map(s.index, (0, 1, 2))) - min(map(s.index, (0, 1, 2))) == 2
shelf = two('review-2 dictionary 1 2 3 in order, 6 books', sum(1 for s in it.permutations(range(6)) if dict_in_order(s)), F(4))
shelf_any = two('review-2 dictionary volumes any order, 6 books', sum(1 for s in it.permutations(range(6)) if dict_together(s)), F(4) * F(3))
E('review', 'items[1].widget.options', shelf, shelf_any, F(6), F(5))
lv.claim(shelf == 24 and shelf_any == 144, 'review-2 items[1]: 4! = 24 with the block fixed, 4! x 3! = 144 with it free')
lv.expect('review', 'items[1].prose', 'volumes 1, 2 and 3 of a dictionary')
lv.expect('review', 'items[1].explain.text', 24)
E('review', 'items[2].widget.answer', two('review-2 codes with a 7', sum(1 for p in it.product(range(10), repeat=3) if 7 in p), 1000 - 729))
E('review', 'items[2].widget.wrong', 300, 729, 1000)
pr6 = list(it.combinations(range(6), 2))
en = Fr(sum(1 for p in pr6 if set(p) & {0, 1}), len(pr6))
E('review', 'items[3].widget.answer', float(two('review-2 at least one energy', en, Fr(9, 15))))
E('review', 'items[3].widget.wrong', 0.4, round(1 / 15, 4), round(1 - (4 / 6) ** 2, 4))
E('review', 'items[4].widget.answer', 120 - (70 + 50 - 30))
E('review', 'items[4].widget.wrong', 0, 90)
E('review', 'items[5].widget.options', two('review-2 round table of 7', len(circular('ABCDEFG')), F(6)), 5040, 360, 120)
E('review', 'items[6].widget.answer', two('review-2 routes 4R 4U', len(routes(4, 4)), C(8, 4)))
E('review', 'items[6].widget.wrong', 40320, 40320 // 24, 16)
lv.expect('review', 'items[6].explain.text', '\\tfrac{40\\,320}{576} = 70')
s7 = Fr(sum(1 for p in it.product('ud', repeat=7) if p.count('u') == 5), 128)
E('review', 'items[7].widget.answer', float(two('review-2 7 steps 5 ups', s7, Fr(21, 128))))
E('review', 'items[7].widget.wrong', round(1 / 8, 4), round(1 / 128, 4), 21)
lv.claim(abs(21 / 128 - 0.1640625) < 1e-12 and C(7, 5) == 21 == F(7) // (F(5) * F(2)) and 2 ** 7 == 128, 'review-2 items[7]: 21/128 = 0.1640625, C(7,5) = 7!/(5!2!) = 21')
lv.expect('review', 'items[7].explain.text', '\\tfrac{21}{128} \\approx 0.164')
ends = two('review-2 Ana not left, Ben not right', sum(1 for s in it.permutations('ABCDE') if s[0] != 'A' and s[-1] != 'B'), 120 - (24 + 24 - 6))
E('review', 'items[8].widget.answer', ends)
E('review', 'items[8].widget.wrong', 120 - 48, 96, 42)

# ---------------- homework-2 ----------------
st = two('homework-2 STATISTICS', words_tree('STATISTICS'), multinom('STATISTICS'))
E('homework', 'items[0].widget.answer', st)
E('homework', 'items[0].widget.wrong', st * 2, F(10), F(10) // 18)
two_pairs = two('homework-2 two pairs together in 7', sum(1 for s in it.permutations(range(7)) if adjacent(s, 0, 1) and adjacent(s, 2, 3)), F(5) * 2 * 2)
E('homework', 'items[1].widget.options', two_pairs, F(5) * 2, F(5), F(7))
lv.claim(two_pairs == 480 and F(5) * 2 == 240 and F(5) == 120 and F(7) == 5040, 'homework-2 items[1]: 5! x 2 x 2 = 480; slips 240, 120, 5040')
lv.expect('homework', 'items[1].prose', 'The two quants must sit together, and so must the two salespeople')
h5 = 0; t5 = 0
for h in it.combinations(range(52), 5):
    t5 += 1; h5 += h[0] < 4
two('homework-2 C(52,5)', t5, 2598960)
E('homework', 'items[2].widget.answer', two('homework-2 5-card hands with an ace', h5, C(52, 5) - C(48, 5)))
E('homework', 'items[2].widget.wrong', 4 * C(51, 4), C(48, 5))
sb = Fr(sum(1 for s, b in ports if 0 in s and 0 in b), len(ports))
E('homework', 'items[3].widget.answer', float(two('homework-2 S1 and B1', sb, Fr(84, 560))))
E('homework', 'items[3].widget.wrong', 0.375, 0.4, 0.775)
lv.claim(sb == Fr(3, 8) * Fr(2, 5), 'homework-2 items[3]: 3/8 x 2/5')
anytie = two('homework-2 exactly one tied pair', sum(1 for lev in weak_orders(5) if sorted(lev.count(k) for k in set(lev)) == [1, 1, 1, 2]), C(5, 2) * F(4))
E('homework', 'items[4].widget.options', anytie, 24, 480, 1200)
E('homework', 'items[5].widget.answer', two('homework-2 1..1000 by 3 or 7', sum(1 for k in range(1, 1001) if k % 3 == 0 or k % 7 == 0), 333 + 142 - 47))
E('homework', 'items[5].widget.wrong', 475, 381, 572)
r44 = routes(4, 4)
avoid = Fr(sum(1 for w in r44 if (2, 2) not in cells(w)), len(r44))
lv.claim(rc('r3c3', 5) == (2, 2), 'homework-2 items[6]: centre r3c3 is two right, two up')
E('homework', 'items[6].widget.answer', round(float(two('homework-2 avoid the centre', avoid, Fr(34, 70))), 4))
E('homework', 'items[6].widget.wrong', round(36 / 70, 4), round(1 - 12 / 70, 4), 0.96)
for n in range(3, 9):
    people = tuple(range(n))
    apart = sum(1 for s in circular(people) if not ({s[0], s[-1]} == {0, 1} or adjacent(s, 0, 1)))
    two(f'homework-2 longform apart at round table, n = {n}', apart, (n - 3) * F(n - 2))
c8 = circular(tuple(range(8)))
tog8 = Fr(sum(1 for s in c8 if {s[0], s[-1]} == {0, 1} or adjacent(s, 0, 1)), len(c8))
lv.claim(tog8 == Fr(2, 7), 'homework-2 longform (b): P(together) at n = 8 is 2/7')
E('homework', 'items[8].model', 2, 7, 0.286)
rep = Fr(sum(1 for p in it.product(range(10), repeat=4) if len(set(p)) < 4), 10000)
E('homework', 'items[9].widget.answer', float(two('homework-2 PIN with a repeat', rep, Fr(4960, 10000))))
E('homework', 'items[9].widget.wrong', 0.504, round(1 - 210 / 10000, 3))

lv.claim(F(10) == 3628800 and F(10) // (6 * 6 * 2) == 50400 and C(52, 5) == 2598960 and C(48, 5) == 1712304 and C(52, 5) - C(48, 5) == 886656,
         'homework-2: 10!/(3!3!2!) = 50400; C(52,5) = 2598960; C(48,5) = 1712304; difference 886656')
lv.expect('homework', 'items[0].explain.text', '\\tfrac{3\\,628\\,800}{6 \\times 6 \\times 2} = 50\\,400')
lv.expect('homework', 'items[2].prose', '$\\binom{52}{5} = 2\\,598\\,960$')
lv.expect('homework', 'items[2].feedback.correct', '$\\binom{48}{5} = 1\\,712\\,304$')
lv.expect('homework', 'items[2].explain.text', '$2\\,598\\,960 - 1\\,712\\,304 = 886\\,656$')
lv.expect('homework', 'items[9].prose', 'from all 10,000')
lv.expect('homework', 'items[9].explain.text', '\\tfrac{5040}{10\\,000} = 0.496')
m3 = sum(1 for n in range(1, 1001) if n % 3 == 0)
m7 = sum(1 for n in range(1, 1001) if n % 7 == 0)
m21 = sum(1 for n in range(1, 1001) if n % 21 == 0)
lv.claim((m3, m7, m21) == (333, 142, 47) and m3 + m7 - m21 == 428, 'homework-2 items[5]: 333, 142, 47 and 428 by enumeration')
lv.expect('homework', 'items[5].explain.text', '$333 + 142 - 47 = 428$')
lv.expect('review', 'items[8].explain.text', '$24 + 24 - 6 = 42$ seatings break a rule')
lv.check_wrongs()
lv.report()
