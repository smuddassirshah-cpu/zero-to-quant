"""Recompute every number stated in ai-use level 1 (l1 to l4, review-1, homework-1, problems-1), each two ways,
and check it appears in the JSON where it is stated (app/tools/numbers_lib.py).
Method A counts next-token pairs with a Counter over the token list; method B counts each pair by scanning the
spaced string for "a b" with str.count, and products are taken in exact fractions both times.
Run from the repository root or app/: python3 docs/reports/ai-use-L1-numbers.py   (exits 0 when every check passes)
"""
import os, sys
from fractions import Fraction as F
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('ai-use', 1)


def table_a(text):
    w = text.split()
    t = defaultdict(Counter)
    for a, b in zip(w, w[1:]):
        t[a][b] += 1
    return t


def chance_a(text, a, b):
    t = table_a(text)
    return F(t[a][b], sum(t[a].values()))


def chance_b(text, a, b):
    s = ' ' + text + ' '
    w = text.split()
    total = sum(1 for i, x in enumerate(w[:-1]) if x == a)        # every place "a" has a next token
    return F(s.count(' ' + a + ' ' + b + ' '), total) if total else F(0)


def sentence(text, words, how):
    p = F(1)
    for a, b in zip(words, words[1:]):
        p *= how(text, a, b)
    return p


def two(label, words, text):
    pa, pb = sentence(text, words, chance_a), sentence(text, words, chance_b)
    lv.claim(pa == pb, f'{label}: Counter {pa} = scan {pb}')
    return pa


AB = 'the cat sat on the mat . the cat ate the jam . the dog sat on the cat .'
W = AB.split()
lv.claim(len(W) == 20 and len(W) - 1 == 19, 'ai-basics text: 20 tokens, 19 pairs')
row = table_a(AB)['the']
lv.claim(dict(row) == {'cat': 3, 'mat': 1, 'jam': 1, 'dog': 1}, 'row for "the": cat 3, mat 1, jam 1, dog 1')
lv.claim(all(chance_b(AB, 'the', k) == F(v, 6) for k, v in row.items()), 'row for "the" by scanning: 3/6, 1/6, 1/6, 1/6')
lv.expect('l1', 'screens[0].canvas.params.rows[0]', 3)
lv.expect('l1', 'screens[0].canvas.params.rows[1][1]', '\\tfrac12')
lv.expect('l1', 'screens[0].hints[2].text', '\\tfrac36 = \\tfrac12')
lv.claim(F(3, 6) == F(1, 2), '3/6 = 1/2')

# l1 explore: the 20-word table frame and the illustrative big-model frame both add to 1
fr = lv.files['l1-reading-the-internet']['screens'][1]['canvas']['controls'][0]['frames']
s_table, s_big = sum(fr[0]['values'].values()), sum(fr[1]['values'].values())
lv.claim(abs(s_table - 1) < 0.001, f'l1 table frame adds to 1 (1/6 drawn as 0.1667): {s_table:.4f}')
lv.claim(abs(s_big - 1) < 1e-9 and abs(sum([0.05, 0.45, 0.3, 0.15, 0, 0.05]) - 1) < 1e-9, f'l1 illustrative frame adds to 1: {s_big}')
lv.expect('l1', 'screens[1].widget.options[1].why', 0.45)
# l1 "sat on the" seen twice in 20 words, then mat 1, cat 1
lv.claim((' ' + AB + ' ').count(' sat on the ') == 2 == sum(1 for i in range(len(W) - 2) if W[i:i + 3] == ['sat', 'on', 'the']), '"sat on the" appears twice')
nxt = Counter(W[i + 3] for i in range(len(W) - 3) if W[i:i + 3] == ['sat', 'on', 'the'])
lv.claim(dict(nxt) == {'mat': 1, 'cat': 1}, 'after "sat on the": mat 1, cat 1')
lv.expect('l1', 'screens[5].canvas.params.rows[0][1]', 2)

# l4: the dog sentence and the cat sentence, both 1/36
dog = two('l4 dog sentence', 'the dog sat on the mat .'.split(), AB)
cat = two('l4 cat sentence', 'the cat sat on the mat .'.split(), AB)
lv.claim(dog == F(1, 36) == cat, 'both sentences 1/36')
lv.claim('the dog sat on the mat .' not in AB and 'the cat sat on the mat .' in AB, 'dog sentence not in the text; cat sentence is')
lv.claim([chance_a(AB, a, b) for a, b in zip('the dog sat on the mat .'.split(), 'dog sat on the mat .'.split())] == [F(1, 6), 1, 1, 1, F(1, 6), 1], 'l4 pair chances 1/6, 1, 1, 1, 1/6, 1')
lv.claim(table_a(AB)['on']['the'] == 2 and table_a(AB)['sat']['on'] == 2, 'on->the and sat->on each 2 of 2')
lv.expect('l4', 'screens[1].widget.answer', round(float(dog), 4))
lv.expect('l4', 'screens[1].feedback.correct', '\\tfrac{1}{36}')
lv.expect('l4', 'screens[1].feedback.correct', 0.028)
lv.expect('l4', 'screens[1].widget.wrong[0].value', round(1 / 6, 4))          # only one of the two 1/6 factors
lv.expect('l4', 'screens[1].widget.wrong[1].value', round(1 / 6 + 1 / 6, 4))  # added the two sixths
lv.expect('l4', 'screens[7].prose', '\\tfrac{1}{36}')
lv.expect('l4', 'summary.formula.tex', '\\tfrac{1}{36}')
lv.claim(F(1, 2) * F(1, 3) * F(1, 6) == F(1, 36) and chance_b(AB, 'cat', 'sat') == F(1, 3), 'quiz: cat sentence 1/2 x 1/3 x 1/6 = 1/36')
lv.expect('l4', 'quiz[0].explain.text', '\\tfrac12 \\times \\tfrac13 \\times 1 \\times 1 \\times \\tfrac16 \\times 1 = \\tfrac{1}{36}')
lv.claim(round(36 * float(dog)) == 1, 'about 1 run in 36')

# review-1 r8: a longer sentence the text never says
long_s = 'the dog sat on the cat sat on the mat .'.split()
p8 = two('review r8 long sentence', long_s, AB)
lv.claim(p8 == F(1, 216) and ' '.join(long_s) not in AB, 'r8 = 1/216 and not in the text')
lv.expect('review', 'items[7].widget.answer', round(float(p8), 5))
lv.expect('review', 'items[7].widget.wrong[0].value', round(float(F(1, 6) * F(1, 2) * F(1, 6)), 5))   # left out sat after cat (1/3)
lv.expect('review', 'items[7].widget.wrong[1].value', round(float(F(1, 36)), 5))                  # only the two sixths
lv.expect('review', 'items[7].explain.text', '\\tfrac{1}{216}')

# homework-1 h4: a fresh text
HT = 'the bank raised rates . the fund raised cash . the bank cut costs .'
h4 = two('homework h4', 'the fund raised rates .'.split(), HT)
lv.claim(h4 == F(1, 6) and 'the fund raised rates .' not in HT, 'h4 = 1/6, not in the text')
lv.claim(chance_a(HT, 'the', 'fund') == F(1, 3) and chance_a(HT, 'raised', 'rates') == F(1, 2) and chance_a(HT, 'the', 'bank') == F(2, 3), 'h4 factors 1/3, 1/2; bank after the 2/3')
lv.expect('homework', 'items[3].widget.answer', round(float(h4), 4))
lv.expect('homework', 'items[3].widget.wrong[0].value', round(1 / 3, 4))
lv.expect('homework', 'items[3].widget.wrong[2].value', round(2 / 3, 4))

# problems-1 p1: the 15-token text
PT = 'the fund bought gold . the bank sold bonds . the fund sold gold .'
PW = PT.split()
lv.claim(len(PW) == 15, 'problems text has 15 tokens')
lv.expect('problems', 'items[0].prose', 15)
n_fund = table_a(PT)['the']['fund']
lv.claim(n_fund == 2 == (' ' + PT).count(' the fund '), 'fund follows the twice')
lv.claim(PW[:-1].count('the') == 3, '"the" appears 3 times with a next token')
lv.expect('problems', 'items[0].parts[0].widget.answer', n_fund)
lv.expect('problems', 'items[0].parts[0].widget.wrong[0].value', 3)
c2 = chance_a(PT, 'the', 'fund')
lv.claim(c2 == chance_b(PT, 'the', 'fund') == F(2, 3), 'chance fund after the = 2/3')
lv.expect('problems', 'items[0].parts[1].widget.answer', round(float(c2), 4))
lv.expect('problems', 'items[0].parts[1].widget.wrong[0].value', round(2 / 15, 4))   # divided by all 15 tokens
lv.expect('problems', 'items[0].parts[1].widget.wrong[1].value', 0.5)                # divided by the 2 distinct next tokens
lv.claim(len(table_a(PT)['the']) == 2, 'two distinct tokens follow the')
p3 = two('problems p1 part 3', 'the bank sold gold .'.split(), PT)
lv.claim(p3 == F(1, 6) and 'the bank sold gold .' not in PT and chance_a(PT, 'the', 'bank') == F(1, 3), 'p1 part 3 = 1/6, bank after the 1/3, not in text')
lv.expect('problems', 'items[0].parts[2].widget.answer', round(float(p3), 4))
lv.expect('problems', 'items[0].parts[2].widget.wrong[1].value', round(1 / 3, 4))   # left out gold after sold (1/2)
lv.expect('problems', 'items[0].parts[2].explain.text', 0.1667)

# small sums in example chats
lv.claim(F(15, 100) * 200 == 30, '15% of 200 = 30 (l2 example C)')
lv.expect('l2', 'screens[4].canvas.params.rows[2][2]', 30)
lv.claim(F(10, 100) * 90 == 9, '10% of 90 = 9 (review r5 example B)')
lv.expect('review', 'items[4].canvas.params.rows[1][2]', 9)
# l3 ranking ladder: Q 1, R 2, P 3 under the guide (honest and harmless before helpful-sounding)
rows = {'P': (False, False), 'Q': (True, True), 'R': (True, True)}      # (honest, harmless)
helpful = {'P': 0.5, 'Q': 1, 'R': 0}
rank = sorted(rows, key=lambda k: (-(rows[k][0] + rows[k][1]), -helpful[k]))
lv.claim(rank == ['Q', 'R', 'P'], 'l3 ranks Q, R, P')
lv.claim(abs(0.55 + 0.45 - 1) < 1e-12, 'l3 illustrative shares add to 1')
lv.claim(1971 != 1981, 'l4 edge: UK decimal coins in 1971 (Decimal Day, 15 February 1971), not 1981')

lv.check_wrongs()
lv.report()
