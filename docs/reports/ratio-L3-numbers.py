"""Number recompute for ratio level 3 (Ratio and proportion): l9 to l13, review-3, homework-3. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names, recomputed from the slip) and the numbers
stated in prose, hints, feedback and explanations are recomputed here. Pure standard library.
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it.
Run from anywhere:  python3 docs/reports/ratio-L3-numbers.py
Failing checks on the current content are findings in docs/reviews/review-ratio-1-3.md (numbers given there).
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("ratio", 3)


def node(f, path):
    return _walk(lv._file(f)[1], path)[0]


def K(f, w, val, nd=None):
    lv.expect(f, f'{w}.answer', round(val, nd) if nd is not None else val)


def W(f, w, wid, val, nd=None):
    ws = node(f, w).get('wrong', [])
    ids = [x.get('id') for x in ws]
    if wid not in ids:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    lv.expect(f, f'{w}.wrong[{ids.index(wid)}].value', round(val, nd) if nd is not None else val)


def band(f, w, wid, typed):
    """A learner who types `typed` (the slip at the asked rounding) lands in the wrong entry's band."""
    x = [e for e in node(f, w)['wrong'] if e['id'] == wid][0]
    lv.claim(abs(typed - x['value']) <= x.get('tol', {}).get('abs', 1e-9), f'{f} {w} wrong {wid}: band {x["value"]} +- {x.get("tol")} holds {typed}')


def R2(f, w, wid, x=None, y=None):
    hit = [e for e in node(f, w)['wrong'] if e['id'] == wid][0]['region']
    ok = (x is None or hit['x'][0] <= x <= hit['x'][1]) and (y is None or 'y' not in hit or hit['y'][0] <= y <= hit['y'][1])
    lv.claim(ok, f'{f} {w} wrong {wid}: region holds ({x}, {y})')


def D(f, w, x, y=None):
    t = node(f, w)['points'][0]['target']
    lv.claim(abs(t[0] - x) < 1e-9 and (y is None or abs(t[1] - y) < 1e-9), f'{f} {w}: target {t} = ({x}, {y})')


T = lv.expect


def share(T_, parts, k):
    return T_ / sum(parts) * parts[k]


# ---------- l9 sharing ----------
f = 'l9-'
K(f, 'screens[0].widget', share(15, [2, 3], 0)); W(f, 'screens[0].widget', 'one-round', 2); W(f, 'screens[0].widget', 'fraction', 15 * 2 / 3)
W(f, 'screens[0].widget', 'half', 7.5)
lv.claim(len(node(f, 'screens[1].widget.answer')) == 6, 'l9 screens[1]: Ana has 6 coins')
K(f, 'screens[2].widget', share(40, [3, 2], 0)); W(f, 'screens[2].widget', 'one-part', 8); W(f, 'screens[2].widget', 'dev', 16)
W(f, 'screens[2].widget', 'by-three', 40 / 3, 2)
K(f, 'screens[3].widget', share(60, [1, 2, 3], 2)); W(f, 'screens[3].widget', 'one-part', 10); W(f, 'screens[3].widget', 'by-people', 20)
W(f, 'screens[3].widget', 'by-ratio-sum', 60 / 5 * 3)
K(f, 'screens[4].widget', 14 / 2 * 5); W(f, 'screens[4].widget', 'add-gap', 14 + 3); W(f, 'screens[4].widget', 'total', 14 / 2 * 7)
W(f, 'screens[4].widget', 'frac', 14 * 2 / 5)
K(f, 'screens[5].widget', 18 / 2 * 8); W(f, 'screens[5].widget', 'diff-as-part', 18 * 8); W(f, 'screens[5].widget', 'kit', 45); W(f, 'screens[5].widget', 'jo', 27)
lv.claim(5 / 9 * 90 == 50 and 5 / 4 * 90 > 90, 'l9 screens[7]: £50; 5/4 x 90 is above £90')
for v in (7, 12, 36, 48):
    T(f, 'screens[8].widget.lines', v)
tot = 16500 + 10000
K(f, 'screens[9].widget', 16500 - share(tot, [3, 2], 0)); W(f, 'screens[9].widget', 'sold-gain', 1500); W(f, 'screens[9].widget', 'swapped', 16500 - 0.4 * tot)
T(f, 'screens[9].explain.text', tot / 5); T(f, 'screens[9].explain.text', 10000 + 600)
K(f, 'quiz[0].widget', math.floor(100 / 3 * 100) / 100); W(f, 'quiz[0].widget', 'half', 50); W(f, 'quiz[0].widget', 'third-up', 33.34)
T(f, 'quiz[0].explain.text', 100 - 33.33)
lv.claim(1 / 5 == 0.2, 'l9 quiz[1]: 20%')
K(f, 'quiz[2].widget', 1200 / 3 * 8); W(f, 'quiz[2].widget', 'larger', 2000); W(f, 'quiz[2].widget', 'wrong-part', 1200 / 5 * 8); W(f, 'quiz[2].widget', 'one-part', 400)
K(f, 'quiz[3].widget', share(1500, [2, 3, 5], 2)); W(f, 'quiz[3].widget', 'by-people', 500); W(f, 'quiz[3].widget', 'one-part', 150)
# l9 screens[1] explain: "the ratio 2 : 3 counts equal columns, not coins" while screens[0] explain says 6 : 9 still compares as 2 : 3
lv.stated(f, 'screens[1].explain.text', 'counts equal columns, not coins', 6 * 3 != 9 * 2)

# ---------- l10 scaling ----------
f = 'l10-'
D(f, 'screens[0].widget', 6, 300 / 4 * 6)
R2(f, 'screens[0].widget', 'double', 6, 600)
# byKey add-two: "You left the flour at about 300 g" -- its region is 290 to 330, which holds an unchanged 300 g
reg = [e for e in node(f, 'screens[0].widget')['wrong'] if e['id'] == 'add-two'][0]['region']['y']
lv.stated(f, 'screens[0].feedback.byKey.add-two', 'You left the flour at about 300 g', (reg[0] <= 300 <= reg[1]))
K(f, 'screens[1].widget', 300 / 4); W(f, 'screens[1].widget', 'times-four', 1200); W(f, 'screens[1].widget', 'per-six', 300 / 6)
K(f, 'screens[2].widget', 75 * 10); W(f, 'screens[2].widget', 'eight', 600); W(f, 'screens[2].widget', 'added', 306); W(f, 'screens[2].widget', 'rate', 75)
D(f, 'screens[3].widget', 2, 3)
lv.claim(math.gcd(6, 9) == 3 and math.gcd(300, 450) == 150, 'l10 screens[3]: 6 : 9 and 300 : 450 both give 2 : 3')
K(f, 'screens[4].widget', 750 / 3 * 2); W(f, 'screens[4].widget', 'multiplied', 750 * 1.5); W(f, 'screens[4].widget', 'one-part', 250); W(f, 'screens[4].widget', 'added', 749)
lv.claim(6 / 4 * 10 == 15, 'l10 screens[5]: 15 eggs')
T(f, 'screens[5].widget.options[2].text', round(4 / 6 * 10, 2))
T(f, 'screens[5].widget.options[3].why', 10 / 4)
lv.claim(3 + 2 * 2 == 7 and 3 + 2 * 4 == 11, 'l10 screens[6]: £7 and £11')
K(f, 'screens[8].widget', 45000 * 800 / 1000); W(f, 'screens[8].widget', 'additive', 45000 - 200); W(f, 'screens[8].widget', 'inverted', 45000 / 0.8)
lv.claim(math.gcd(45000, 36000) == 9000 and 45000 // 9000 == 5 and 36000 // 9000 == 4, 'l10 screens[8]: 45,000 : 36,000 = 5 : 4')
lv.claim(math.gcd(1500, 600) == 300, 'l10 quiz[0]: 1,500 : 600 divides by 300 to 5 : 2')
K(f, 'quiz[1].widget', 3 * 1000 / 250); W(f, 'quiz[1].widget', 'added', 3 + 4); W(f, 'quiz[1].widget', 'units', 3 / 4)
# 0.75 is 3 divided by 4 (scaled the wrong way); treating 1 kg as 1 g would give 3 / 250 = 0.012
lv.stated(f, 'quiz[1].feedback.byKey.units', 'You treated 1 kg as 1 g', abs(3 / 4 - 3 / 250) < 1e-9)
lv.claim([5 / 2, 10 / 4, 15 / 6] == [2.5] * 3 and 2 * 12 == 4 * 6 == 6 * 4 == 24, 'l10 quiz[2]: ratio 2.5; products 24')
# explain names "the first table": options shuffle, so the learner's first table may be another one
lv.stated(f, 'quiz[2].explain.text', 'In the first table', node(f, 'quiz[2].widget').get('shuffle') is False)
K(f, 'quiz[3].widget', 24000 / 2 * 3); W(f, 'quiz[3].widget', 'inverted', 24000 * 2 / 3); W(f, 'quiz[3].widget', 'additive', 25000)

# ---------- l11 direct or inverse ----------
f = 'l11-'
D(f, 'screens[0].widget', 8, 4 * 6 / 8)
R2(f, 'screens[0].widget', 'direct', 8, 12); R2(f, 'screens[0].widget', 'minus', 8, 2); R2(f, 'screens[0].widget', 'same', 8, 6)
D(f, 'screens[1].widget', 1200 / 40, 40); R2(f, 'screens[1].widget', 'forty', 40)
lv.claim(1200 / 25 > 40 > 1200 / 35, 'l11 screens[1]: 40 shares lies between £25 and £35')
K(f, 'screens[2].widget', 1200 / 60); W(f, 'screens[2].widget', 'direct', 80); W(f, 'screens[2].widget', 'additive', 40 - 30)
K(f, 'screens[3].widget', 1200 / 48); W(f, 'screens[3].widget', 'direct', 40 * 48 / 30); W(f, 'screens[3].widget', 'additive', 40 - 18)
rows = node(f, 'screens[4].canvas.params.rows')
c = {int(r[0]) * int(r[1]) for r in rows[:3]}
lv.claim(c == {30}, 'l11 screens[4]: every row multiplies to 30')
K(f, 'screens[4].widget', 30 / 6); W(f, 'screens[4].widget', 'direct', 15 * 3); W(f, 'screens[4].widget', 'pattern', 6 - 3)
W(f, 'screens[4].widget', 'halve', 15 / 2)
# byKey halve: "because 6 is more than 3 ... divide by 3": halving is right from 3 machines (10 h), not from 15 h
lv.stated(f, 'screens[4].feedback.byKey.halve', 'because 6 is more than 3', False)
lv.claim(40 - 5 * 2 == 30 and 40 - 5 * 4 == 20 and 2 * 30 != 4 * 20, 'l11 screens[5]: 30 l, 20 l; products 60 and 80')
lv.claim(40 * 3 == 60 * 2 == 120, 'l11 screens[6]: 40 x 3 = 60 x 2 = 120')
lv.claim(24 / 3 == 8, 'l11 screens[7]: 8 days')
K(f, 'screens[8].widget', 10000 / 62.5); W(f, 'screens[8].widget', 'direct', 400 * 2.5); W(f, 'screens[8].widget', 'additive', 400 - 37.5)
lv.claim(1 * 35 == 35 and 2 * 30 == 60, 'l11 quiz[0]: 35 and 60')
K(f, 'quiz[1].widget', 60 / 15); W(f, 'quiz[1].widget', 'direct', 10 * 15 / 6); W(f, 'quiz[1].widget', 'additive', 10 - 9)
K(f, 'quiz[2].widget', 18 / 4 * 10); W(f, 'quiz[2].widget', 'additive', 18 + 6); W(f, 'quiz[2].widget', 'inverse', 72 / 10)
K(f, 'quiz[3].widget', 72 / 6); W(f, 'quiz[3].widget', 'direct', 18 * 1.5); W(f, 'quiz[3].widget', 'additive', 16)

# ---------- l12 best buy ----------
f = 'l12-'
lv.claim(round(3.75 / 250, 4) == 0.015 and round(5.60 / 400, 4) == 0.014, 'l12 screens[0]: 1.5p and 1.4p a gram')
K(f, 'screens[1].widget', 5.60 / 400 * 100, 2); W(f, 'screens[1].widget', 'per-gram', 0.014); W(f, 'screens[1].widget', 'grams-per-pound', 400 / 5.60, 2)
K(f, 'screens[2].widget', 13.50 / 10, 2); W(f, 'screens[2].widget', 'per-kilo', 13.5); W(f, 'screens[2].widget', 'per-gram', 0.0135)
K(f, 'screens[3].widget', 150 / 2.5); W(f, 'screens[3].widget', 'decimal-time', 150 / 2.3, 2); W(f, 'screens[3].widget', 'per-minute', 1)
W(f, 'screens[3].widget', 'whole-hours', 75)
K(f, 'screens[4].widget', 4.50 / 3 - 7.00 / 5, 2); W(f, 'screens[4].widget', 'totals', 2.5); W(f, 'screens[4].widget', 'per-two', 0.2)
lv.claim(round(4.40 / 5, 2) == 0.88 and round(9.00 / 10, 2) == 0.90, 'l12 screens[5]: 88p and 90p per 100 g')
K(f, 'screens[8].widget', (1849.20 - 6) / 240, 2); W(f, 'screens[8].widget', 'fee-in', 1849.20 / 240, 3); W(f, 'screens[8].widget', 'inverted', 240 / 1849.20, 2)
band(f, 'screens[8].widget', 'fee-in', 7.71)     # the learner who includes the fee and rounds to the penny
lv.claim(round(4.20 / 6, 2) == 0.70 and round(6.50 / 10, 2) == 0.65, 'l12 quiz[0]: 70p and 65p')
K(f, 'quiz[1].widget', 18 / 0.75); W(f, 'quiz[1].widget', 'decimal', 18 / 0.45); W(f, 'quiz[1].widget', 'per-minute', 18 / 45)
K(f, 'quiz[2].widget', 3762 / 450, 2); W(f, 'quiz[2].widget', 'inverted', 450 / 3762, 2)
lv.claim(round(12 / 30, 2) == 0.40 and round(19.50 / 50, 2) == 0.39, 'l12 quiz[3]: 40p and 39p')

# ---------- l13 currencies ----------
f = 'l13-'
K(f, 'screens[0].widget', 300 * 1.16, 2); W(f, 'screens[0].widget', 'divided', 300 / 1.16, 2); W(f, 'screens[0].widget', 'added', 301.16)
D(f, 'screens[1].widget', round(580 / 1.16, 6), 580); R2(f, 'screens[1].widget', 'multiplied', 580 * 1.16); R2(f, 'screens[1].widget', 'same', 580)
T(f, 'screens[1].feedback.byKey.multiplied', round(670 * 1.16))
K(f, 'screens[2].widget', 1 / 1.16, 4); W(f, 'screens[2].widget', 'same', 1.16); W(f, 'screens[2].widget', 'subtract', 0.84); W(f, 'screens[2].widget', 'gap', 0.16)
back = 500 * 1.12 / 1.21
K(f, 'screens[3].widget', back, 2); W(f, 'screens[3].widget', 'same', 500); W(f, 'screens[3].widget', 'multiplied-back', 500 * 1.12 * 1.21, 2)
T(f, 'screens[3].explain.text', round(500 - round(back, 2), 2))
# one-rate: one rate both ways gives exactly £500, the same answer as "same"; its band 500.01 +- 0.02 overlaps "same"
ws3 = {e['id']: e for e in node(f, 'screens[3].widget')['wrong']}
lv.claim('one-rate' not in ws3 or abs(500 * 1.12 / 1.12 - ws3['one-rate']['value']) > ws3['one-rate']['tol']['abs'],
         'l13 screens[3]: the one-rate slip gives an answer other than the same slip (one rate both ways returns exactly £500)')
K(f, 'screens[4].widget', 1.16 * 160, 2); W(f, 'screens[4].widget', 'divided', 160 / 1.16, 2); W(f, 'screens[4].widget', 'added', 161.16)
lv.claim(round(1000 / 0.85, 2) == 1176.47 and round(1000 * 0.85, 2) == 850 and round(1000 * 1.15, 2) == 1150, 'l13 screens[5]: €1,176.47, €850, €1,150')
lv.claim(round(1 / 1.25, 2) == 0.80, 'l13 screens[6]: 0.80')
lv.claim(250 * 1.16 == 290 and 290 * 160 == 46400 and round(250 * 185.6, 6) == 46400, 'l13 screens[7]: €290, ¥46,400')
cost, proceeds = 200 * 58 / 1.16, 200 * 63.80 / 1.21
K(f, 'screens[8].widget', proceeds - cost, 2)
W(f, 'screens[8].widget', 'old-rate', 200 * 63.80 / 1.16 - cost, 2); W(f, 'screens[8].widget', 'euro-profit', 200 * (63.80 - 58), 2)
W(f, 'screens[8].widget', 'multiplied', 200 * 63.80 * 1.21 - 200 * 58 * 1.16, 2)
T(f, 'screens[8].explain.text', round((proceeds - cost) / cost * 100, 1)); T(f, 'screens[8].explain.text', round(63.80 / 58 - 1, 2) * 100)
K(f, 'quiz[0].widget', 87 / 1.16, 2); W(f, 'quiz[0].widget', 'multiplied', 87 * 1.16, 2)
K(f, 'quiz[1].widget', 100 / 190, 2); W(f, 'quiz[1].widget', 'same', 190); W(f, 'quiz[1].widget', 'pounds', 1 / 190, 4)
band(f, 'quiz[1].widget', 'pounds', round(1 / 190, 2))   # the pounds slip at the asked 2 decimal places is 0.01
K(f, 'quiz[2].widget', 200 - 200 * 1.10 / 1.22, 2); W(f, 'quiz[2].widget', 'rate-gap', 200 * 0.12); W(f, 'quiz[2].widget', 'none', 0)
K(f, 'quiz[3].widget', 190 / 1.16, 2); W(f, 'quiz[3].widget', 'multiplied', 190 * 1.16, 2)

# ---------- review-3 ----------
f = 'review'
K(f, 'items[0].widget', share(450, [4, 5], 1)); W(f, 'items[0].widget', 'one-part', 50); W(f, 'items[0].widget', 'smaller', 200); W(f, 'items[0].widget', 'by-two', 225)
K(f, 'items[1].widget', 640 * 1.15, 2); W(f, 'items[1].widget', 'divided', 640 / 1.15, 2); W(f, 'items[1].widget', 'added', 641.15)
lv.claim(math.gcd(math.gcd(45000, 60000), 75000) == 15000, 'review-3 items[2]: all three divide by 15,000')
K(f, 'items[3].widget', 5 * 12 / 3); W(f, 'items[3].widget', 'direct', 12 * 3 / 5); W(f, 'items[3].widget', 'additive', 14)
lv.claim(round(2.85 / 7.5, 2) == 0.38 and round(7.80 / 20, 2) == 0.39, 'review-3 items[4]: 38p and 39p per 100 ml')
K(f, 'items[5].widget', 3 / 10); W(f, 'items[5].widget', 'as-fraction', 3 / 7, 4); W(f, 'items[5].widget', 'equities', 0.7)
K(f, 'items[6].widget', 2015 / (930 / 120)); W(f, 'items[6].widget', 'inverse', 120 * 930 / 2015, 2); W(f, 'items[6].widget', 'additive', 120 + 2015 - 930)
K(f, 'items[7].widget', 430 / 0.86, 2); W(f, 'items[7].widget', 'times', 430 * 0.86, 2); W(f, 'items[7].widget', 'gap', 430 * 1.14, 2)
T(f, 'items[7].feedback.byKey.gap', round(1 / 0.86, 3))
K(f, 'items[8].widget', 300 * (1005 - 5) / 125 + 5); W(f, 'items[8].widget', 'fee-in', 1005 / 125 * 300, 2); W(f, 'items[8].widget', 'no-fee', 300 * 8)

# ---------- homework-3 ----------
f = 'homework'
p = 1260 / 3
K(f, 'items[0].widget', 11 * p); W(f, 'items[0].widget', 'diff-as-part', 1260 * 11); W(f, 'items[0].widget', 'larger', 7 * p); W(f, 'items[0].widget', 'one-part', p)
K(f, 'items[1].widget', 60 / 2 * 5); W(f, 'items[1].widget', 'ali-before', 90); W(f, 'items[1].widget', 'sixty', 60); W(f, 'items[1].widget', 'part', 30)
K(f, 'items[2].widget', 5 + (12 * 15 - 12 * 5) / 8); W(f, 'items[2].widget', 'ignore-done', 12 * 15 / 8); W(f, 'items[2].widget', 'direct', 15)
y = 1000 * 1.16 * 162 / 190
K(f, 'items[3].widget', y, 2); W(f, 'items[3].widget', 'start', 1000); W(f, 'items[3].widget', 'multiplied', 1000 * 1.16 * 162 * 190)
T(f, 'items[3].explain.text', round(1000 - round(y, 2), 2))
sh, bo = 30000 * 0.8 + 4000, 20000 * 1.05
tot = sh + bo
K(f, 'items[4].widget', 0.6 * tot - sh)
W(f, 'items[4].widget', 'no-cash', 0.6 * (tot - 4000) - (sh - 4000))
# old-total: "You aimed shares at 60% of the old £50,000" -> 30,000 - 28,000 = 2,000 (content holds 4,000)
W(f, 'items[4].widget', 'old-total', 0.6 * 50000 - sh)
# swapped: bonds given 60% -> bonds target 29,400 against 21,000 held = 8,400 (content holds 9,400)
W(f, 'items[4].widget', 'swapped', 0.6 * tot - bo)
T(f, 'items[4].explain.text', 0.6 * tot); T(f, 'items[4].explain.text', 0.4 * tot)
m = lv.text(f, 'items[6].model')
for v in (16000, 32000, 48000, round(32000 * 1.16, 2), round(1 / 1.16, 4)):
    T(f, 'items[6].model', v)
lv.claim(round(32000 / 0.8621) == 37119, 'homework-3 items[6]: 32,000 / 0.8621 = 37,119')
K(f, 'items[7].widget', round(9.95 / 0.01)); W(f, 'items[7].widget', 'rate', 0.01); W(f, 'items[7].widget', 'fee', 9.95)
K(f, 'items[8].widget', 54 / 4.5 * 7.5, 2); W(f, 'items[8].widget', 'additive', 57); W(f, 'items[8].widget', 'inverse', 54 * 4.5 / 7.5, 2)

# ---- fix pass (session V): numbers written by the fixes
lv.claim(round(1000 / 125, 2) == 8 and 300 * 8 + 5 == 2405 and round(1005 / 125 * 300, 2) == 2412, 'review-3 items[8]: 2405, 2412, 2400')
lv.claim(round(11600 / 1.16) == 10000 and round(12760 / 1.21, 2) == 10545.45 and round(12760 / 1.21 - 10000, 2) == 545.45 and round(545.45 / 10000 * 100, 1) == 5.5, 'l13 s8 explanation')
lv.claim(round(4.4 / 5 * 100) == 88 and round(9 / 10 * 100) == 90, 'l12 s5 explanation: 88p and 90p')
lv.claim(round(500 * 1.12 / 1.12, 6) == 500 and round(500 * 1.21 / 1.21, 6) == 500, 'l13 s3: one rate both ways returns 500')
lv.claim(0.75 == 3 / 4 and 3 * 4 == 12, 'l10 quiz[1]: the units slip is 3 / 4')
lv.claim(2 * 150 / 2 == 150 and 1.5 * 300 == 450, 'l10 s0: 150 g more, scale factor 1.5')
lv.claim(0.6 * 50000 == 30000 and 30000 - 28000 == 2000 and 0.6 * 49000 - 21000 == 8400, 'homework-3 items[4]: slips 2000 and 8400')
lv.claim(2.5 * 2 == 5 and 3 + 4 == 7 and 3 + 4 * 2 == 11, 'l10 fare explanation')

lv.check_wrongs()
lv.report()
