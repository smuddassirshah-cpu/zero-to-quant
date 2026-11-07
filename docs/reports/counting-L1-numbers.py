"""Second-reader number check for counting level 1 (l1 to l4, review-1, homework-1), written by the session V reader
(docs/reviews/review-counting-1-3.md). Every count is found twice: method 1 enumerates the outcomes with itertools
(brute force), method 2 uses the formula the lesson teaches; the two must agree, and the number must appear where the
JSON states it (app/tools/numbers_lib.py). Claims that are not one number use lv.claim or lv.claim_text.
A check marked FINDING fails while the content is wrong and passes once the fix in the review lands.
Run: python3 docs/reports/counting-L1-numbers.py   (exits 0 when every check passes)
"""
import itertools as it
import math
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("counting", 1)
P, C, F = math.perm, math.comb, math.factorial


def two(label, brute, formula):
    """Method 1 (enumeration) against method 2 (formula)."""
    lv.claim(brute == formula, f'{label}: brute {brute} = formula {formula}')
    return formula


def n_tuples(*sizes):
    return sum(1 for _ in it.product(*[range(s) for s in sizes]))


def n_perm(n, r=None):
    return sum(1 for _ in it.permutations(range(n), n if r is None else r))


def n_comb(n, r):
    return sum(1 for _ in it.combinations(range(n), r))


def adjacent(seq, a, b):
    i, j = seq.index(a), seq.index(b)
    return abs(i - j) == 1


def E(f, path, *vals):
    for v in vals:
        lv.expect(f, path, v)


# ---------------- l1 choices multiply ----------------
outfits = two('l1 outfits', n_tuples(3, 2), 3 * 2)
E('l1', 'screens[1].widget.answer', outfits)
E('l1', 'screens[1].widget.wrong', 3 + 2, 3)
with_shoes = two('l1 outfits with shoes', n_tuples(3, 2, 2), 12)
blue = two('l1 blue-shirt outfits', sum(1 for s, t, o in it.product(range(3), range(2), range(2)) if s == 1), 2 * 2)
E('l1', 'screens[2].explain.text', blue, with_shoes)
lv.claim(len(lv.files['l1-choices-multiply']['screens'][2]['widget']['answer']) == blue, 'l1 s2 key taps 4 leaves')
jackets = two('l1 jackets', n_tuples(3, 2, 2, 3), 36)
E('l1', 'screens[3].widget.answer', jackets)
E('l1', 'screens[3].widget.wrong', 12 + 3, 12, 3 * 2 * 3)
meals = two('l1 meal deal', n_tuples(4, 3, 2), 24)
E('l1', 'screens[4].widget.answer', meals)
E('l1', 'screens[4].widget.wrong', 4 + 3 + 2, 3 * 2)
water = two('l1 water only', n_tuples(4, 3, 1), 12)
E('l1', 'screens[5].widget.answer', water)
E('l1', 'screens[5].widget.wrong', 24, 4 + 3 + 1, 0)
lv.claim(n_tuples(4, 3, 0) == 0, 'l1 s5 explain: a stage with 0 choices gives 0')
codes5 = two('l1 binary codes of 5', n_tuples(*[2] * 5), 2 ** 5)
codes3 = two('l1 binary codes of 3', n_tuples(*[2] * 3), 2 ** 3)
E('l1', 'screens[6].widget.answer', codes5)
E('l1', 'screens[6].widget.wrong', 5 * 2, 5 ** 2, 2 + 5, codes3)
lv.claim('added' in lv.files['l1-choices-multiply']['screens'][6]['feedback']['byKey'],
         'FINDING l1 screens[6]: wrong[] "added" (7) has a byKey line')
two_course = two('l1 two-course meals', n_tuples(3, 4), 12)
E('l1', 'screens[7].widget.options', two_course, 3 + 4, 4, 24)
lv.expect('l1', 'screens[9].explain.text', two('l1 4-digit codes', n_tuples(*[10] * 4), 10 ** 4))
runs = two('l1 sweep runs', n_tuples(4, 3, 2), 24)
E('l1', 'screens[10].widget.answer', runs * 0.40)
E('l1', 'screens[10].widget.wrong', (4 + 3 + 2) * 0.40, 6 * 0.40, runs)
lv.claim(abs(runs * 0.40 - 9.6) < 1e-9 and abs(runs * 5 * 0.40 - 48) < 1e-9, 'l1 s10: £9.60; five values would give £48.00')
settings = len(lv.files['l1-choices-multiply']['screens'][10]['canvas']['params']['levelLabels'])
lv.claim(settings == 3 and 'fifth' not in lv.text('l1', 'screens[10].explain.text'),
         f'l1 s10 explain: {settings} settings swept, so no "fifth setting"')
lv.expect('l1', 'screens[10].explain.text', 'A fourth setting with 5 values would multiply the bill by 5, to £48.00')
lv.expect('l1', 'screens[6].feedback.byKey.added', codes5)
pins = two('l1 quiz PINs', n_tuples(*[10] * 4), 10000)
E('l1', 'quiz[0].widget.options', pins, 40, 9999, n_perm(10, 4))
E('l1', 'quiz[1].widget.options', 5 + 3, 5 * 3, 5, 2)
E('l1', 'quiz[2].widget.options', two('l1 sandwiches', n_tuples(3, 5, 2), 30), 15, 3 + 5 + 2, 16)
tick = two('l1 tickers', n_tuples(26, 26, 10), 6760)
E('l1', 'quiz[3].widget.options', tick, 26 + 26 + 10, two('l1 tickers no repeat', sum(1 for a, b, c in it.product(range(26), range(26), range(10)) if a != b), 6500), 676)

# ---------------- l2 arranging ----------------
E('l2', 'screens[1].widget.answer', two('l2 3 traders', n_perm(3), F(3)))
E('l2', 'screens[1].widget.wrong', 3, 3 ** 3, 3 * 3)
lv.expect('l2', 'screens[2].explain.text', two('l2 first two of 4', n_perm(4, 2), 12))
E('l2', 'screens[3].widget.answer', two('l2 4 traders', n_perm(4), 24))
E('l2', 'screens[3].widget.wrong', 4 + 3 + 2 + 1, 16, 12, 4 ** 4)
E('l2', 'screens[4].widget.answer', two('l2 5 traders', n_perm(5), 120))
E('l2', 'screens[4].widget.wrong', 15, 25, 24, 5 ** 5)
ana_front = two('l2 Ana at front', sum(1 for s in it.permutations('ABCD') if s[0] == 'A'), F(3))
E('l2', 'screens[5].widget.answer', ana_front)
E('l2', 'screens[5].widget.wrong', 24, 24 - 6, 4)
bc = two('l2 B and C side by side', sum(1 for s in it.permutations('ABCD') if adjacent(s, 'B', 'C')), F(3) * 2)
E('l2', 'screens[6].widget.answer', bc)
E('l2', 'screens[6].widget.wrong', 6, 24, 6 + 2)
six = two('l2 6 traders', n_perm(6), 720)
E('l2', 'screens[7].widget.options', six, 12, 36, 21)
lv.claim(six // 12 == 60 and F(6) // F(3) == 4 * 5 * 6 == 120, 'l2 s7: 720 is sixty times 12; 3 to 6 multiplies by 120')
lv.claim(F(7) == 7 * F(6) == 5040, 'l2 s8: 7! = 7 x 6! = 5040')
E('l2', 'screens[8].explain.text', 720, 5040)
send = two('l2 5 sending orders', n_perm(5), 120)
E('l2', 'screens[10].widget.answer', send)
E('l2', 'screens[10].widget.wrong', 25, 15, 24, 3125)
lv.claim(send * 30 == 3600, 'l2 s10: 120 replays at 30 s is an hour')
E('l2', 'quiz[0].widget.options', 720, 36, 21, 12)
E('l2', 'quiz[1].widget.options', F(8) // F(7), F(8))
hedge_last = two('l2 hedge last', sum(1 for s in it.permutations(range(5)) if s[-1] == 0), F(4))
E('l2', 'quiz[2].widget.answer', hedge_last)
E('l2', 'quiz[2].widget.wrong', 120, 120 - 24, 5)
mojo = two('l2 Mo and Jo together', sum(1 for s in it.permutations(range(5)) if adjacent(s, 0, 1)), F(4) * 2)
E('l2', 'quiz[3].widget.options', mojo, 24, 120, F(3) * 2)

# ---------------- l3 choosing in order ----------------
awards = two('l3 P(5,3)', n_perm(5, 3), P(5, 3))
E('l3', 'screens[0].widget.answer', awards)
E('l3', 'screens[0].widget.wrong', 5 ** 3, n_comb(5, 3), 5 + 4 + 3, F(5))
E('l3', 'screens[2].widget.answer', two('l3 P(7,3)', n_perm(7, 3), P(7, 3)))
E('l3', 'screens[2].widget.wrong', 7 ** 3, C(7, 3), F(7), 7 + 6 + 5)
heads = {}
for s in it.permutations(range(5)):
    heads[s[:3]] = heads.get(s[:3], 0) + 1
lv.claim(set(heads.values()) == {F(2)} and len(heads) == F(5) // F(2) == 60, 'l3 s3: every podium heads exactly 2 of the 120 lines')
lv.claim(F(0) == 1 and F(5) // F(0) == 120 == n_perm(5, 5), 'l3 s4: 0! = 1 so 5!/0! = 120')
acct = two('l3 4-letter codes from 6', n_perm(6, 4), P(6, 4))
E('l3', 'screens[5].widget.answer', acct)
E('l3', 'screens[5].widget.wrong', 6 ** 4, C(6, 4), F(6), 6 + 5 + 4 + 3)
lv.claim(0.70 < 1 - acct / 6 ** 4 < 0.75, f'l3 s5: banning repeats removes {1 - acct / 6 ** 4:.3f}, almost three quarters')
rank = two('l3 rank 2 of 6', n_perm(6, 2), F(6) // F(4))
E('l3', 'screens[6].widget.options', rank, F(6) // F(2), C(6, 2), 36)
lv.claim(F(6) // F(2) == P(6, 4), "l3 s6: Kim's 6!/2! is the count for 4 places")
lv.claim(list(range(10, 10 - 4, -1))[-1] == 7, 'l3 s7: last factor of P(10,4) is 7')
pin_nr = two('l3 PIN no repeat', n_perm(10, 4), 5040)
E('l3', 'screens[9].widget.answer', pin_nr)
E('l3', 'screens[9].widget.wrong', 10000, C(10, 4), 10 + 9 + 8 + 7, 9 * 8 * 7 * 6)
lv.claim(0.45 < pin_nr / 10000 < 0.55, 'l3 s9: about half of 10,000')
E('l3', 'quiz[0].widget.options', two('l3 fund tiers', n_perm(10, 3), 720), C(10, 3), 1000, 27)
lv.claim(9 * 8 * 7 * 6 == F(9) // F(5) == 3024, 'l3 quiz[1]: 9x8x7x6 = 9!/5! = 3024')
lv.expect('l3', 'quiz[1].explain.text', 3024)
tk = two('l3 3-letter tickers', n_perm(26, 3), 15600)
E('l3', 'quiz[2].widget.answer', tk)
E('l3', 'quiz[2].widget.wrong', 26 ** 3, C(26, 3), 26 + 25 + 24)

# ---------------- l4 choosing without order ----------------
pairs4 = two('l4 pairs from 4', n_comb(4, 2), C(4, 2))
E('l4', 'screens[0].widget.answer', pairs4)
E('l4', 'screens[0].widget.wrong', 12, 16, 4, 8)
lv.claim(n_perm(4, 2) == 12 and n_perm(4, 2) // 2 == pairs4, 'l4 s1: 12 off-diagonal cells, 6 pairs')
E('l4', 'screens[2].widget.answer', two('l4 5 choose 2', n_comb(5, 2), C(5, 2)))
E('l4', 'screens[2].widget.wrong', 20, 25, 5)
grp = {}
for s in it.permutations(range(5), 3):
    k = frozenset(s); grp[k] = grp.get(k, 0) + 1
lv.claim(set(grp.values()) == {6} and len(grp) == 10, 'l4 s3: each committee appears 6 times among 60')
E('l4', 'screens[3].widget.answer', 6)
E('l4', 'screens[4].widget.answer', two('l4 6 choose 3', n_comb(6, 3), C(6, 3)))
E('l4', 'screens[4].widget.wrong', 120, 40, 216)
lv.claim(n_comb(5, 3) == n_comb(5, 2) == 10, 'l4 s5: 5C3 = 5C2 = 10')
E('l4', 'screens[6].widget.options', two('l4 committees of 3 from 8', n_comb(8, 3), 56), 336, 112, 512)
lv.claim(n_comb(10, 7) == n_comb(10, 3) == 120 and P(10, 3) == 720, 'l4 s7: 10C7 = 10C3 = 120')
lv.claim(F(6) // (F(3) * F(3)) == 20, 'l4 s8: 720/(6x6) = 20')
port = two('l4 portfolios 3 of 10', n_comb(10, 3), 120)
E('l4', 'screens[9].widget.answer', port)
E('l4', 'screens[9].widget.wrong', 720, 1000, 240, 27)
up2 = two('l4 quiz 2 up days', sum(1 for w in it.product('UD', repeat=5) if w.count('U') == 2), C(5, 2))
E('l4', 'quiz[0].widget.options', up2, 20, 32, 25)
E('l4', 'quiz[1].widget.options', two('l4 hold all 7', n_comb(7, 7), 1), 7, 5040, 0)
off = two('l4 12 choose 9', n_comb(12, 9), C(12, 3))
E('l4', 'quiz[2].widget.answer', off)
E('l4', 'quiz[2].widget.wrong', 1320, 660, 108)
E('l4', 'quiz[3].widget.options', two('l4 chair and deputy', n_perm(6, 2), 30), 15, 36, 11)

# ---------------- review-1 ----------------
form = two('review-1 form', n_tuples(5, 3, 2), 30)
E('review', 'items[0].widget.answer', form)
E('review', 'items[0].widget.wrong', 5 + 3 + 2, 3 * 2)
lv.claim(form == 30 and len(lv.files['review-1']['items'][0]['canvas']['params']['nodes']['children']) == 5,
         'review-1 items[0]: 5 currency branches (GBP drawn, 4 folded), 5 x 6 = 30')
lv.expect('review', 'items[0].prose', 'These have 5, 3 and 2 choices')
lv.expect('review', 'items[0].explain.text', 5 * 6)
talks = two('review-1 7 talks', n_perm(7), F(7))
E('review', 'items[1].widget.options', talks, 7 * 7, 7 + 6 + 5 + 4 + 3 + 2 + 1, F(6))
lv.claim(talks == 5040 and 7 + 6 + 5 + 4 + 3 + 2 + 1 == 28, 'review-1 items[1]: 7! = 5040, 1 + ... + 7 = 28')
E('review', 'items[2].widget.answer', two('review-1 podium of 9', n_perm(9, 3), 504))
E('review', 'items[2].widget.wrong', 729, C(9, 3), 9 + 8 + 7, F(9))
E('review', 'items[3].widget.answer', two('review-1 4 of 9', n_comb(9, 4), 126))
E('review', 'items[3].widget.wrong', P(9, 4), P(9, 4) // 4, 9 ** 4)
E('review', 'items[4].widget.answer', 4 + 6)
E('review', 'items[4].widget.wrong', 24, 2)
win2 = two('review-1 2 winning months of 6', sum(1 for w in it.product('WL', repeat=6) if w.count('W') == 2), C(6, 2))
E('review', 'items[5].widget.answer', win2)
E('review', 'items[5].widget.wrong', P(6, 2), 2 ** 6, 2)
lv.claim(win2 == 15 and C(6, 4) == 15 and 2 ** 6 == 64 and P(6, 2) == 30, 'review-1 items[5]: C(6,2) = C(6,4) = 15, 2^6 = 64, 6 x 5 = 30')
lv.expect('review', 'items[5].question', 'exactly 2 winning months')
hh = two('review-1 hedges back to back', sum(1 for s in it.permutations(range(6)) if adjacent(s, 0, 1)), F(5) * 2)
E('review', 'items[6].widget.answer', hh)
E('review', 'items[6].widget.wrong', 120, 720, F(4) * 2)
login = two('review-1 login codes', sum(1 for a, b, c, d in it.product(range(26), range(26), range(26), range(10)) if len({a, b, c}) == 3), P(26, 3) * 10)
E('review', 'items[8].widget.answer', login)
E('review', 'items[8].widget.wrong', 26 ** 3 * 10, P(26, 3), C(26, 3) * 10)

# ---------------- homework-1 ----------------
E('homework', 'items[0].widget.answer', two('homework-1 switches', n_tuples(2, 2, 2, 2, 5), 80))
E('homework', 'items[0].widget.wrong', 2 * 5, 4 * 2 * 5, 2 + 2 + 2 + 2 + 5, 5)
pin0 = two('homework-1 PIN not starting 0', sum(1 for s in it.permutations(range(10), 4) if s[0] != 0), 9 * 9 * 8 * 7)
E('homework', 'items[1].widget.answer', pin0)
E('homework', 'items[1].widget.wrong', 5040, 9 * 8 * 7 * 6, 9 * 8 * 8 * 7)
strong = two('homework-1 strong weeks', sum(1 for w in it.product('UD', repeat=5) if w.count('U') >= 4), C(5, 4) + C(5, 5))
E('homework', 'items[2].widget.answer', strong)
E('homework', 'items[2].widget.wrong', 5, 1, 10)
for n in range(2, 9):
    two(f'homework-1 pairs of {n} stocks', n_comb(n, 2), n * (n - 1) // 2)
lv.expect('homework', 'items[3].explain.text', 100 * 99 // 2)
chair = two('homework-1 committee with chair', sum(len(s) for s in it.combinations(range(10), 4)), C(10, 4) * 4)
E('homework', 'items[5].widget.options', chair, C(10, 4), P(10, 4), C(10, 4) * 10)
lv.claim(10 * C(9, 3) == chair and C(9, 3) == 84, 'homework-1 items[5]: chair first, 10 x 84 = 840')
three = two('homework-1 three hedges together', sum(1 for s in it.permutations(range(7)) if max(s.index(0), s.index(1), s.index(2)) - min(s.index(0), s.index(1), s.index(2)) == 2), F(5) * F(3))
E('homework', 'items[6].widget.answer', three)
E('homework', 'items[6].widget.wrong', 120, 5040, 240)
a = two('homework-1 longform (a)', n_comb(12, 4), 495)
b = two('homework-1 longform (b)', n_perm(12, 4), 11880)
d = two('homework-1 longform (d)', sum(1 for s in it.combinations(range(12), 4) if 0 in s), C(11, 3))
lv.claim(b == 24 * a, 'homework-1 longform (c): (b) = 24 x (a)')
E('homework', 'items[7].model', a, b, d, 24)

lv.claim(any(w['id'] == 'self' and w['tex'] == '\\frac{n(n+1)}{2}' for w in lv.files['homework-1']['items'][3]['widget']['wrong']),
         'homework-1 items[3]: the self-pairing slip n(n+1)/2 is a wrong[] entry')
lv.claim(all(n * (n + 1) // 2 == n_comb(n, 2) + n for n in range(2, 12)), 'homework-1 items[3]: n(n+1)/2 = n(n-1)/2 + n, one self-pair per stock')
lv.expect('homework', 'items[3].feedback.byKey.self', '$n(n-1)$ ordered pairs')
lv.expect('l3', 'screens[6].widget.options[3].why', '$6 \\times 6 = 36$')
lv.expect('l3', 'quiz[0].widget.options[2].why', '$10^3 = 1000$')
lv.expect('l4', 'quiz[3].widget.options[2].why', '$6 \\times 6 = 36$')
lv.claim(6 * 6 == 36 and 10 ** 3 == 1000, 'l3 and l4 slip whys: 6 x 6 = 36, 10^3 = 1000')
lv.claim(all('shuffle' not in o['widget'] for o in (lv.files['l2-arranging']['quiz'][0], lv.files['l3-choosing-in-order']['screens'][7])), 'l2 quiz[0] and l3 s7 no longer fix the option order')
lv.check_wrongs()
lv.report()
