"""Number check for ai-basics level 4 (l13 to l16, review-4, homework-4, problems-4).
Method A: every count by a dictionary over the pairs, every chance and temperature row in exact fractions (square roots
as exact surds checked by squaring, then floats). Method B: the same counts by a second scan (str.count on the joined
pair text, or a nested loop over positions), chances and temperature rows in floats by a separate formula. Each stated
figure must agree between the two and appear at the path where it is stated. Code widgets: each solution passes its
hidden tests in CPython, the starter fails one, and each mutant fails the test it names. The seed-7 runs are recomputed
with random.Random(7) (the same Mersenne Twister as Pyodide; the code widget's hidden test checks it in the browser).
Run: <venv>/bin/python docs/reports/ai-basics-L4-numbers.py   (exits 0 when every check passes)
"""
import math
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("ai-basics", 4)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
TEXT = "the cat sat on the mat . the cat ate the jam . the dog sat on the cat ."
W = TEXT.split()


def doc(f):
    return lv._file(f)[1]


def scr(f, title):
    d = doc(f)
    return f"screens[{[i for i, s in enumerate(d['screens']) if s.get('title') == title][0]}]"


def item(f, iid):
    d = doc(f)
    return f"items[{[i for i, s in enumerate(d['items']) if s.get('id') == iid][0]}]"


def quiz(f, iid):
    d = doc(f)
    return f"quiz[{[i for i, s in enumerate(d['quiz']) if s.get('id') == iid][0]}]"


def node(f, path):
    n = doc(f)
    for part in path.replace(']', '').replace('[', '.').split('.'):
        if part:
            n = n[int(part)] if part.isdigit() else n[part]
    return n


# ---------------- counting, two ways ----------------
def rows_a(words):                       # method A: dictionary, next words in first-seen order
    r = {}
    for a, b in zip(words, words[1:]):
        r.setdefault(a, {})
        r[a][b] = r[a].get(b, 0) + 1
    return r


def count_b(words, a, b):                # method B: nested scan over positions
    return sum(1 for i in range(len(words) - 1) if words[i] == a and words[i + 1] == b)


def row(words, a):
    ra = rows_a(words).get(a, {})
    for b, c in ra.items():
        lv.claim(c == count_b(words, a, b), f'count {a}->{b} two ways ({c})')
    lv.claim(sum(ra.values()) == sum(1 for i in range(len(words) - 1) if words[i] == a), f'row total for {a} two ways')
    return ra


def chances_a(counts):
    t = sum(counts)
    return [F(c, t) for c in counts]


def chances_b(counts):
    t = 0.0
    for c in counts:
        t += c
    return [c / t for c in counts]


def ch(counts):
    a, b = chances_a(counts), chances_b(counts)
    lv.claim(all(abs(float(x) - y) < 1e-12 for x, y in zip(a, b)) and sum(a) == 1, f'chances {counts} two ways')
    return a


def temp_a(chs, power):                  # exact for power 2; power 0.5 via floats of exact surds
    if power == 1:
        return [F(c) for c in chs]
    if power == 2:
        r = [F(c) ** 2 for c in chs]
        return [x / sum(r) for x in r]
    r = [math.sqrt(F(c).numerator) / math.sqrt(F(c).denominator) for c in chs]
    return [x / sum(r) for x in r]


def temp_b(chs, power):
    r = [float(c) ** power for c in chs]
    s = 0.0
    for x in r:
        s += x
    return [x / s for x in r]


def tp(chs, power):
    a, b = temp_a(chs, power), temp_b(chs, power)
    lv.claim(all(abs(float(x) - y) < 1e-12 for x, y in zip(a, b)), f'temperature power {power} on {chs} two ways')
    return a


def first_above(chs, u):                 # the sampling rule, exact
    t = F(0)
    for i, c in enumerate(chs):
        t += F(c)
        if F(str(u)) < t:
            return i
    return len(chs) - 1


def first_above_b(chs, u):               # method B: count running totals at or below u
    tot, k = 0.0, 0
    for c in chs:
        tot += float(c)
        if tot <= u + 1e-12:
            k += 1
    return min(k, len(chs) - 1)


def sample(chs, u):
    a, b = first_above(chs, u), first_above_b(chs, u)
    lv.claim(a == b, f'sample {chs} u={u} two ways')
    return a


# ---------------- the course text ----------------
lv.claim(len(W) == 20 and len(set(W)) == 9, '20 words, 9 different')
R = rows_a(W)
lv.claim(sum(sum(r.values()) for r in R.values()) == 19 == len(W) - 1, '19 pairs, counts add to 19')
the = row(W, 'the')
lv.claim(list(the.items()) == [('cat', 3), ('mat', 1), ('jam', 1), ('dog', 1)], 'row the: cat 3, mat 1, jam 1, dog 1 in first-seen order')
lv.claim(row(W, 'cat') == {'sat': 1, 'ate': 1, '.': 1} and row(W, 'sat') == {'on': 2} and row(W, 'dog') == {'sat': 1}
         and row(W, 'jam') == {'.': 1} and row(W, '.') == {'the': 2} and 'the' not in R['cat'], 'rows cat, sat, dog, jam, "." and the(cat) = 0')
CT = ch([3, 1, 1, 1])
lv.claim(CT == [F(1, 2), F(1, 6), F(1, 6), F(1, 6)], 'the row chances 1/2, 1/6, 1/6, 1/6')
lv.claim([sum(CT[:k + 1]) for k in range(4)] == [F(1, 2), F(2, 3), F(5, 6), 1], 'running totals 1/2, 2/3, 5/6, 1')
lv.claim([sample(CT, u) for u in (0.1, 0.5, 0.62, 0.9, 0.0)] == [0, 1, 1, 3, 0], 'u 0.1 cat, 0.5 mat, 0.62 mat, 0.9 dog, 0 cat')
tot = 0.0
for c in [1 / 2, 1 / 6, 1 / 6, 1 / 6]:
    tot = tot + c
lv.claim(tot == 0.9999999999999999 == 1 - 2 ** -53 and repr(tot) == '0.9999999999999999', 'float running total 0.9999999999999999')
lv.claim(1 / 2 + 1 / 6 + 1 / 6 + 1 / 6 == tot, 'the plain sum left to right gives the same (Python 3.12 sum() is compensated and gives 1.0; the lesson uses a loop)')
TH = tp(CT, 2)
T2 = tp(CT, 0.5)
lv.claim(TH == [F(3, 4), F(1, 12), F(1, 12), F(1, 12)], 'temperature 1/2: 3/4, 1/12 x3')
lv.claim(round(T2[0], 3) == 0.366 and round(T2[1], 4) == 0.2113 and abs(T2[0] - (math.sqrt(3) - 1) / 2) < 1e-12, 'temperature 2: 0.366, 0.2113 (cat = (sqrt3 - 1)/2)')
lv.claim(round(math.sqrt(0.5), 4) == 0.7071 and round(math.sqrt(1 / 6), 4) == 0.4082 and round(math.sqrt(.5) + 3 * math.sqrt(1 / 6), 4) == 1.9319, 'roots 0.7071, 0.4082, total 1.9319')
lv.claim(round(0.7071 / 1.9319, 3) == 0.366 and round(0.4082 / 1.9319, 3) == 0.211, 'printed 0.7071 / 1.9319 = 0.366, 0.4082 / 1.9319 = 0.211')
lv.claim(sum(F(1, 36) for _ in range(3)) + F(1, 4) == F(1, 3), 'squares add to 1/3')

# ---------------- l13 ----------------
lv.claim(node('l13', scr('l13', 'What comes next?') + '.widget.answer') == [f'c{i + 1}' for i, w in enumerate(W) if w == 'the'], 'l13 hook taps the six words after the')
tab = node('l13', scr('l13', 'Walk the pairs') + '.widget.rows')
lv.claim([(r[0], r[1]['answer']) for r in tab] == list(the.items()), 'l13 explore row for the')
pairs_the = [i + 1 for i in range(19) if W[i] == 'the']
lv.claim(pairs_the == [1, 5, 8, 11, 14, 18] and [i + 1 for i in range(19) if W[i] == 'the' and W[i + 1] == 'cat'] == [1, 8, 18], 'pairs 1, 8, 18 are the cat; 5, 11, 14 mat, jam, dog')
lv.expect('l13', scr('l13', 'Walk the pairs') + '.hints', 18)
lv.expect('l13', scr('l13', 'A next-word table') + '.widget.answer', R['sat']['on'])
lv.claim(count_b(W, 'sat', 'on') == 2 and [i for i, w in enumerate(W) if w == 'sat'] == [2, 15], 'sat at c2 and c15, both before on')
rc = node('l13', scr('l13', 'The row for cat') + '.widget.rows')
lv.claim([(r[0].strip('“”'), r[1]['answer']) for r in rc] == [('sat', 1), ('ate', 1), ('.', 1), ('on', 0)], 'l13 cat row with on 0')
lv.claim(count_b(W, 'cat', 'on') == 0 and any(W[i] == 'cat' and W[i + 2] == 'on' for i in range(18)), 'on comes two after cat, never straight after')
lv.expect('l13', scr('l13', 'How many pairs?') + '.widget.answer', len(W) - 1)
lv.claim(len(W) // 2 == 10, 'no-overlap slip 10')
lv.expect('l13', scr('l13', 'Which way round?') + '.widget.answer', count_b(W, 'cat', 'the'))
lv.claim(count_b(W, 'the', 'cat') == 3, 'backwards slip 3')
trows = node('l13', scr('l13', 'Which way round?') + '.canvas.params.rows')
cols = [c.strip('“”') for c in node('l13', scr('l13', 'Which way round?') + '.canvas.params.columns')[1:]]
lv.claim(all((int(cell) if cell else 0) == count_b(W, r[0].strip('“”'), c) for r in trows for c, cell in zip(cols, r[1:])), 'l13 full table cells two ways')
short = "the dog sat on the mat".split()
lv.claim([w for w in set(short) if not rows_a(short).get(w)] == ['mat'], 'empty row: mat')
lv.expect('l13', scr('l13', 'The whole table') + '.widget.answer', 101 - 1)
lv.expect('l13', scr('l13', 'A trader\'s keyboard') + '.widget.answer', 14 + 9 + 5 + 2)
lv.claim(sum([14, 9, 5, 2]) == 30, 'keyboard 30 by sum()')
q = "up up down up down down up".split()
lv.expect('l13', quiz('l13', 'q-pairs-seven') + '.widget.answer', len(q) - 1)
lv.expect('l13', quiz('l13', 'q-up-down') + '.widget.answer', row(q, 'up')['down'])
lv.claim(' '.join(q).count('up down') == 2 and q.count('down') == 3, 'up down 2 by str.count; 3 downs')

# ---------------- l14 ----------------
lv.expect('l14', scr('l14', 'How likely is cat?') + '.widget.answer', float(CT[0]))
lv.claim(F(3, 20) == F('0.15') and F(3, 4) == F('0.75'), 'hook slips 3/20 and 3/4')
tb = node('l14', scr('l14', 'Count over row total') + '.widget.rows')
lv.claim([abs(r[1]['answer'] - float(c)) <= r[1]['tol']['abs'] for r, c in zip(tb, CT)] == [True] * 4, 'l14 table chances')
lv.expect('l14', scr('l14', 'The row for cat') + '.widget.answer', 0.3333)
lv.claim(ch([1, 1, 1])[1] == F(1, 3), 'ate after cat 1/3')
lv.expect('l14', scr('l14', 'The row for sat') + '.widget.answer', float(ch([2])[0]))
FUND = "the fund rose . the price fell . the fund fell . the fund rose .".split()
fr = row(FUND, 'fund')
lv.claim(len(FUND) == 16 and fr == {'rose': 2, 'fell': 1} and [i for i, w in enumerate(FUND) if w == 'fund'] == [1, 9, 13], 'fund text: 16 words, rose 2 fell 1 at c1, c9, c13')
lv.expect('l14', scr('l14', 'A text of your own') + '.widget.answer', 0.6667)
lv.claim(abs(float(ch([2, 1])[0]) - 0.6667) < 0.0005 and F(2, 16) == F('0.125'), 'rose 2/3; words slip 2/16')
lv.expect('l14', scr('l14', 'Which total?') + '.widget.answer', 0.1667)
lv.claim(F(1, 20) == F('0.05') and abs(1 / 19 - 0.0526) < 0.0001 and F(3, 20) + 3 * F(1, 20) == F(6, 20), 'trap slips 1/20, 1/19, 1/4; 20-word chances add to 6/20')
lv.expect('l14', scr('l14', 'Chances from a row') + '.widget.answer', float(ch([4, 3, 1])[0]))
UPD = {'up': {'up': 68, 'down': 62}, 'down': {'up': 61, 'down': 58}}
lv.claim(68 + 62 == 130 and 68 + 61 == 129 and 68 + 62 + 61 + 58 == 249, 'share table totals 130, 129, 249')
lv.claim(round(68 / 130, 3) == 0.523 and round(68 / 129, 3) == 0.527 and round(68 / 249, 3) == 0.273, 'share chances 0.523, slips 0.527, 0.273')
lv.claim(abs(float(F(68, 130)) - 0.523) < 0.0005, 'share 68/130 exact')
lv.expect('l14', scr('l14', 'Up after up') + '.widget.answer', 0.523)
lv.expect('l14', quiz('l14', 'q-two-two') + '.widget.answer', float(ch([2, 2])[0]))
lv.expect('l14', quiz('l14', 'q-five-three-two') + '.widget.answer', float(ch([5, 3, 2])[1]))

# ---------------- l15 ----------------
lv.expect('l15', scr('l15', 'Sampling') + '.widget.answer', 'dog')
lv.claim(sample(CT, 0.9) == 3, 'u 0.9 dog')
lv.expect('l15', scr('l15', 'A running total') + '.widget.answer', 0.8333)
CC = ch([1, 1, 1])
seq = ['the']
for u in (0.1, 0.5, 0.9):
    r = rows_a(W)[seq[-1]]
    seq.append(list(r)[sample(ch(list(r.values())), u)])
lv.claim(seq == ['the', 'cat', 'ate', 'the'], 'by hand 0.1, 0.5, 0.9: the cat ate the')
seq = ['the']
for u in (0.9, 0.5, 0.1):
    r = rows_a(W)[seq[-1]]
    seq.append(list(r)[sample(ch(list(r.values())), u)])
lv.claim(seq == ['the', 'dog', 'sat', 'on'], 'reversed: the dog sat on')
TABLE = {k: (list(v), [float(x) for x in ch(list(v.values()))]) for k, v in rows_a(W).items()}


def gen(start, us):
    out = [start]
    for u in us:
        ws, cs = TABLE[out[-1]]
        out.append(ws[first_above(cs, u)])
    return out


rng = random.Random(7)
runs = [' '.join(gen('the', [rng.random() for _ in range(11)])) for _ in range(4)]
lv.claim(node('l15', scr('l15', 'Four runs') + '.canvas.params.lines') == runs, 'seed-7 runs recomputed')
lv.claim(all(count_b(W, a, b) > 0 for r in runs for a, b in zip(r.split(), r.split()[1:])), 'every pair in the runs is in the text')
lv.claim('ate the cat' not in TEXT and 'the cat ate the cat sat on the mat' not in TEXT, 'ate the cat and the second run are new')
greedy = ['the']
for _ in range(7):
    ws, cs = TABLE[greedy[-1]]
    greedy.append(ws[cs.index(max(cs))])
lv.claim(' '.join(greedy) == 'the cat sat on the cat sat on', 'greedy loop')
lv.expect('l15', scr('l15', 'Sampling in one rule') + '.widget.answer', float(600 * CT[0]))
lv.claim(600 * CT[1] == 100 and 600 / 4 == 150, 'slips 100 and 150')
FT = [F('0.55'), F('0.35'), F('0.10')]
lv.claim(sample(FT, 0.6) == 1 and [sum(FT[:k + 1]) for k in range(3)] == [F('0.55'), F('0.9'), 1], 'FTSE u 0.6 fell; totals 0.55, 0.9, 1')
lv.claim(sample(CT, 0.5) == 1, 'quiz u 0.5 mat')
UF = [F('0.2'), F('0.5'), F('0.3')]
lv.expect('l15', quiz('l15', 'q-running') + '.widget.answer', float(UF[0] + UF[1]))
lv.claim(sample(UF, 0.7) == 2, 'quiz u 0.7 down (exact boundary)')

# ---------------- l16 ----------------
lv.claim(node('l16', scr('l16', 'Square and rescale') + '.widget.rows')[0][3]['answer'] == float(TH[0])
         and abs(node('l16', scr('l16', 'Square and rescale') + '.widget.rows')[1][3]['answer'] - float(TH[1])) < 0.0005, 'l16 table 3/4, 1/12')
lv.expect('l16', scr('l16', 'Temperature 2') + '.widget.answer', round(T2[0], 3))
lv.expect('l16', scr('l16', 'A tie stays a tie') + '.widget.answer', 0.3333)
lv.claim(tp(CC, 2) == CC and F(1, 3) ** 2 == F(1, 9), 'tie stays a tie, slip 1/9')
lv.claim(tp([1], 0.5) == [1.0] and tp([1], 2) == [1], 'certain row stays 1')
lv.claim(len("unbelievable") == 12 and len("an") + len("unbelievable") + len("rally") == 19 and len("an unbelievable rally") == 21, 'tokens: 12, 19 characters, 21 with spaces')
tok = node('l16', scr('l16', 'Three ways to split') + '.widget.rows')
lv.claim([r[1]['answer'] for r in tok] == [len("an unbelievable rally".split()), 5, len("anunbelievablerally")], 'three splits 3, 5, 19')
lv.claim(''.join(node('l16', scr('l16', 'Three ways to split') + '.canvas.right.params.cells')) == 'anunbelievablerally', 'character cells')
lv.expect('l16', scr('l16', 'Drafting a contract') + '.widget.answer', float(TH[0]))
lv.expect('l16', quiz('l16', 'q-half-half') + '.widget.answer', float(tp([F(1, 2), F(1, 2)], 2)[0]))
lv.expect('l16', quiz('l16', 'q-quarter') + '.widget.answer', float(tp([F(1, 4), F(3, 4)], 2)[1]))
lv.claim(0.0625 + 0.5625 == 0.625 and 0.5625 / 0.625 == 0.9, 'quarter: squares 0.0625, 0.5625, total 0.625')
lv.expect('l16', quiz('l16', 'q-stock') + '.widget.answer', len('stock'))
frames = node('l16', scr('l16', 'The temperature dial') + '.canvas.controls')[0]['frames']
lv.claim([round(frames[k]['values']['cat'], 4) for k in range(3)] == [0.75, 0.5, 0.366], 'dial frames 0.75, 0.5, 0.366')

# ---------------- review-4 ----------------
lv.expect('review', item('review', 'r-twelve') + '.widget.answer', 11)
lv.expect('review', item('review', 'r-temp-half') + '.widget.answer', round(float(tp([F('0.6'), F('0.4')], 2)[0]), 3))
lv.claim(round(0.36 / 0.52, 3) == 0.692, '0.36/0.52')
log = "buy sell buy buy sell hold buy".split()
lv.expect('review', item('review', 'r-buy-sell') + '.widget.answer', row(log, 'buy')['sell'])
lv.claim(count_b(log, 'sell', 'buy') == 1 and log.count('buy') == 4, 'buy-sell slips 1 and 4')
lv.claim(sample([F('0.4'), F('0.25'), F('0.35')], 0.65) == 2, 'r-pick-down: down (boundary 0.65)')
lv.expect('review', item('review', 'r-six-three-one') + '.widget.answer', float(ch([6, 3, 1])[0]))
lv.expect('review', item('review', 'r-stockholders') + '.widget.answer', len('stockholders'))
names = open(os.path.join(ROOT, 'app', 'content', 'data', 'ai', 'names.txt')).read().split()
nn = sum(1 for n in names for ch_ in n if ch_ == 'n')
nend = sum(1 for n in names if n.endswith('n'))
nend_b = sum(1 for n in names for a, b in zip(n + '.', (n + '.')[1:]) if a == 'n' and b == '.')
lv.claim(len(names) == 32033 and nn == 18327 and nend == nend_b == 6763, 'names: 32,033, n 18,327 times, n then end 6,763 (two ways)')
lv.expect('review', item('review', 'r-names-n') + '.widget.answer', round(6763 / 18327, 3))
lv.claim(round(6763 / 32033, 3) == 0.211, 'names slip 0.211')
lv.expect('review', item('review', 'r-temp-two') + '.widget.answer', round(float(tp([F('0.64'), F('0.36')], 0.5)[0]), 3))
lv.claim(round(0.4096 / (0.4096 + 0.1296), 2) == 0.76, 'temp-two squared slip 0.76')
dd = "up up down up down down up up".split()
lv.expect('review', item('review', 'r-down-down') + '.widget.answer', 0.3333)
lv.claim(ch([row(dd, 'down')['up'], row(dd, 'down')['down']])[1] == F(1, 3) and F(dd.count('down'), 8) == F(3, 8), 'down after down 1/3; slip 3/8')

# ---------------- homework-4 ----------------
lv.expect('homework', item('homework', 'h-temp-row') + '.widget.answer', 0.6667)
lv.claim(tp(ch([2, 1, 1]), 2)[0] == F(2, 3) and sum(x ** 2 for x in ch([2, 1, 1])) == F(3, 8), 'counts 2,1,1 at T 1/2: 2/3, squares 3/8')
lv.expect('homework', item('homework', 'h-emma') + '.widget.answer', len('.emma.') - 1)
lv.claim(sample(CT, 0.5) == 1, 'h-at-or-above: 0.5 gives mat')
FRESH = "buy low . sell high . buy the dip . sell the news . buy the rumour .".split()
lv.claim(row(FRESH, 'buy') == {'low': 1, 'the': 2} and row(FRESH, '.') == {'sell': 2, 'buy': 2} and tp(ch([1, 2]), 2) == [F(1, 5), F(4, 5)], 'fresh text rows; buy at power 2: 1/5, 4/5')

# ---------------- problems-4 ----------------
P1 = "buy the dip . sell the news . buy the dip . buy the rumour .".split()
p1 = row(P1, 'the')
lv.claim(len(P1) == 16 and p1 == {'dip': 2, 'news': 1, 'rumour': 1}, 'p-dip rows')
lv.expect('problems', item('problems', 'p-dip') + '.parts[0].widget.answer', sum(p1.values()))
lv.expect('problems', item('problems', 'p-dip') + '.parts[1].widget.answer', float(ch([2, 1, 1])[0]))
lv.claim(sample(ch([2, 1, 1]), 0.6) == 1, 'p-dip u 0.6 news')
lv.expect('problems', item('problems', 'p-dip') + '.parts[3].widget.answer', 0.6667)
P2 = "up up down up up up down down up up".split()
lv.expect('problems', item('problems', 'p-days') + '.parts[0].widget.answer', len(P2) - 1)
lv.claim(row(P2, 'up') == {'up': 4, 'down': 2} and row(P2, 'down') == {'up': 2, 'down': 1}, 'p-days rows')
lv.expect('problems', item('problems', 'p-days') + '.parts[1].widget.answer', 0.6667)
lv.expect('problems', item('problems', 'p-days') + '.parts[2].widget.answer', 0.3333)
BOE = [F('0.81'), F('0.09'), F('0.09'), F('0.01')]
b2 = tp(BOE, 0.5)
lv.claim([round(x, 4) for x in b2] == [0.5625, 0.1875, 0.1875, 0.0625] and abs(sum([0.9, 0.3, 0.3, 0.1]) - 1.6) < 1e-12, 'BoE temperature 2 exact: 0.5625, 0.1875, 0.1875, 0.0625')
lv.expect('problems', item('problems', 'p-boe') + '.parts[0].widget.answer', round(b2[0], 4))
lv.expect('problems', item('problems', 'p-boe') + '.parts[1].widget.answer', round(b2[3], 4))
lv.claim(sample(b2, 0.6) == 1 and sample(BOE, 0.6) == 0, 'BoE u 0.6: cut at T 2, hold at T 1')
bh = tp(BOE, 2)
lv.expect('problems', item('problems', 'p-boe') + '.parts[4].widget.answer', round(float(bh[0]), 4))
lv.claim(sum(x ** 2 for x in BOE) == F('0.6724') and round(0.6561 / 0.6724, 4) == 0.9758, 'BoE squares total 0.6724, hold 0.9758')


# ---------------- code widgets: solution, starter and mutants ----------------
def run_code(f, path):
    w = node(f, path)['widget'] if 'widget' in node(f, path) else node(f, path)
    pre = w.get('prelude', '')

    def passes(src, t):
        ns = {}
        try:
            exec(pre, ns)
            exec(src, ns)
            ns['__learner_source__'] = src
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            exp = eval(t['expect'], {})
        except Exception:
            return False

        def same(a, b):
            if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
                return isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
            if t.get('compare') == 'isclose' and not isinstance(a, str):
                return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)
            return a == b
        return same(got, exp)

    def first_fail(src):
        for k, t in enumerate(w['tests']):
            if not passes(src, t):
                return k + 1
        return None
    lv.claim(first_fail(w['solution']) is None, f'{f} {path}: solution passes every hidden test')
    lv.claim(first_fail(w['starter']) is not None, f'{f} {path}: starter fails a hidden test')
    lv.claim(len(w.get('mutants', [])) >= 2, f'{f} {path}: at least two mutants')
    for m in w.get('mutants', []):
        lv.claim(first_fail(m['source']) == m['test'], f'{f} {path}: mutant first fails test {m["test"]} ({m["symptom"][:40]})')
    return w


run_code('l13', scr('l13', 'Counting pairs in code'))
run_code('l14', scr('l14', 'Chances in code'))
run_code('l15', scr('l15', 'Picking in code'))
gw = run_code('l15', scr('l15', 'Writing in code'))
lv.claim(eval(gw['tests'][-1]['expect']) == runs[1], 'the seed-7 test is the second console run')
run_code('l16', scr('l16', 'Temperature in code'))
run_code('homework', item('homework', 'h-row-chances'))
bw = run_code('homework', item('homework', 'h-bigram-writer'))

# bigram_writer expectations a second way: exact fractions, rows by rows_a, and no u within 0.01 of a boundary
def writer_b(text, start, us, power):
    words = text.split()
    rr = rows_a(words)
    out = [start]
    for u in us:
        if out[-1] not in rr:
            break
        cs = list(rr[out[-1]].values())
        p = tp(ch(cs), power)
        tots = [sum(p[:k + 1]) for k in range(len(p))]
        lv.claim(all(abs(float(t) - u) > 0.01 for t in tots[:-1]) or u == 0.5, f'writer u={u} clear of boundaries (0.5 is the boundary test)')
        out.append(list(rr[out[-1]])[first_above(p, u) if power == 2 or power == 1 else first_above_b(p, u)])
    return out


for t in bw['tests']:
    if t.get('setup'):
        continue
    lv.claim(eval(t['call'], {'bigram_writer': writer_b}) == eval(t['expect']), f'bigram_writer two ways: {t["call"][:60]}')

lv.check_wrongs()
sys.exit(lv.report())
