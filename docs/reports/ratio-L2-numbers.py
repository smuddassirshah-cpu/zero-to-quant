"""Number recompute for ratio level 2 (Change over time): l5 to l8, review-2, homework-2. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names, recomputed from the slip) and the numbers
stated in prose, hints, feedback and explanations are recomputed here. Pure standard library.
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it.
Run from anywhere:  python3 docs/reports/ratio-L2-numbers.py
Failing checks on the current content are findings in docs/reviews/review-ratio-1-3.md (numbers given there).
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("ratio", 2)


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


def R(f, w, wid, val):
    ws = node(f, w).get('wrong', [])
    hit = [x for x in ws if x.get('id') == wid]
    if not hit:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    x = hit[0]
    lo, hi = (x['from'], x['to']) if 'from' in x else tuple(x['region']['x'])
    lv.claim(lo <= val <= hi, f'{f} {w} wrong {wid}: region [{lo}, {hi}] holds the slip {val}')


def D(f, w, val):
    n = node(f, w)
    t = n['points'][0]['target'][0] if 'points' in n else n['answer']
    lv.claim(abs(t - val) < 1e-9, f'{f} {w}: target {t} = {val}')


T = lv.expect
pc = lambda a, b: (b - a) / a

# ---------- l5 rise or fall ----------
f = 'l5-'
D(f, 'screens[1].widget', 40 * 1.25); R(f, 'screens[1].widget', 'added-pounds', 65); R(f, 'screens[1].widget', 'rise-only', 10)
D(f, 'screens[2].widget', 40 * 0.75); R(f, 'screens[2].widget', 'fall-size', 10); R(f, 'screens[2].widget', 'wrong-way', 50); R(f, 'screens[2].widget', 'pounds', 15)
K(f, 'screens[3].widget', pc(40, 46), 4); W(f, 'screens[3].widget', 'pounds', 0.06); W(f, 'screens[3].widget', 'new-base', 6 / 46, 4); W(f, 'screens[3].widget', 'ratio', 46 / 40)
K(f, 'screens[4].widget', -pc(80, 68), 4); W(f, 'screens[4].widget', 'pounds', 0.12); W(f, 'screens[4].widget', 'new-base', 12 / 68, 4)
K(f, 'screens[5].widget', pc(12, 30)); W(f, 'screens[5].widget', 'ratio', 30 / 12); W(f, 'screens[5].widget', 'pounds', 0.18); W(f, 'screens[5].widget', 'new-base', 18 / 30)
lv.claim(10 / 50 == 0.2 and 10 / 40 == 0.25 and pc(40, 50) == 0.25, 'l5 screens[6]: 20% fall, 25% on the new price, 25% back up')
T(f, 'screens[7].feedback.correct', pc(25, 27) * 100)
T(f, 'screens[8].widget.lines[3].text', pc(40, 46))
v = node(f, 'screens[9].canvas.params.series[0].values')
K(f, 'screens[9].widget', pc(v[3], v[4]), 4)
W(f, 'screens[9].widget', 'pounds', round(v[4] - v[3], 2) / 100)
W(f, 'screens[9].widget', 'new-base', (v[4] - v[3]) / v[4], 6)
T(f, 'screens[9].hints[2].text', round(v[4] - v[3], 2))
K(f, 'quiz[1].widget', -pc(3.2, 2.4), 4); W(f, 'quiz[1].widget', 'new-base', 0.8 / 2.4, 4); W(f, 'quiz[1].widget', 'kept', 0.75)
lv.claim(pc(8, 10) == 0.25 and pc(100, 120) > 0.19999, 'l5 quiz[2]: A 25%, B 20%')
K(f, 'quiz[3].widget', pc(18, 45)); W(f, 'quiz[3].widget', 'ratio', 45 / 18); W(f, 'quiz[3].widget', 'new-base', 27 / 45); W(f, 'quiz[3].widget', 'pounds', 0.27)
lv.claim(round(pc(60, 75), 4) == 0.25 and round(15 / 75, 4) == 0.2, 'l5 quiz[0]: 25%, 20%')

# ---------- l6 before the discount ----------
f = 'l6-'
D(f, 'screens[1].widget', 64 / 0.8)
R(f, 'screens[1].widget', 'add-back', 64 * 1.2); R(f, 'screens[1].widget', 'off-again', 64 * 0.8); R(f, 'screens[1].widget', 'add-pounds', 84)
T(f, 'screens[1].feedback.byKey.add-back', round(0.2 * 64, 2))
D(f, 'screens[2].widget', 80); R(f, 'screens[2].widget', 'add-back', 64 * 1.2)
K(f, 'screens[3].widget', 45 / 0.75, 2); W(f, 'screens[3].widget', 'add-back', 45 * 1.25, 2); W(f, 'screens[3].widget', 'off-again', 45 * 0.75, 2)
W(f, 'screens[3].widget', 'divide-cut', 45 / 0.25, 2)
K(f, 'screens[4].widget', 92 / 1.15, 2); W(f, 'screens[4].widget', 'down-again', 92 * 0.85, 2); W(f, 'screens[4].widget', 'up-again', 92 * 1.15, 2)
W(f, 'screens[4].widget', 'minus-pounds', 77)
K(f, 'screens[5].widget', 150 - 150 / 1.2, 2); W(f, 'screens[5].widget', 'of-total', 0.2 * 150, 2); W(f, 'screens[5].widget', 'pre-vat', 150 / 1.2, 2)
T(f, 'screens[5].explain.text', round(25 / 150 * 100, 1))
lv.claim(round(4500 / 0.9, 2) == 5000 and round(4500 * 1.1, 2) == 4950 and round(4500 / 1.1, 2) == 4090.91 and round(4500 * 0.9, 2) == 4050,
         'l6 screens[6]: £5,000, £4,950, £4,090.91, £4,050')
T(f, 'screens[7].feedback.correct', round(65 / 1.3, 2))
K(f, 'screens[9].widget', 50.70 / 1.04, 2); W(f, 'screens[9].widget', 'took-off', 50.70 * 0.96, 3); W(f, 'screens[9].widget', 'minus-pounds', 46.7)
lv.claim(round(36 / 0.75, 2) == 48 and round(36 * 1.25, 2) == 45 and round(36 * 0.75, 2) == 27 and round(36 / 0.25, 2) == 144, 'l6 quiz[0]: options')
K(f, 'quiz[1].widget', 84 / 1.2, 2); W(f, 'quiz[1].widget', 'off', 84 * 0.8, 2); W(f, 'quiz[1].widget', 'pounds', 64)
K(f, 'quiz[2].widget', 5 / 0.25); W(f, 'quiz[2].widget', 'add', 5 * 1.75, 2); W(f, 'quiz[2].widget', 'wrongm', 5 / 0.75, 2)
lv.claim(round(33000 / 1.1, 2) == 30000 and round(33000 * 0.9, 2) == 29700 and round(33000 * 1.1, 2) == 36300, 'l6 quiz[3]: options')
T(f, 'quiz[3].explain.text', round(30000 - 33000 * 0.9, 2))

# ---------- l7 up then down ----------
f = 'l7-'
D(f, 'screens[1].widget', 100 * 1.2 * 0.8); R(f, 'screens[1].widget', 'cancel', 100); R(f, 'screens[1].widget', 'from-start', 80)
D(f, 'screens[2].widget', 100 * 0.8 * 1.2); R(f, 'screens[2].widget', 'from-start', 120)
K(f, 'screens[3].widget', 1.2 * 0.8, 4); W(f, 'screens[3].widget', 'added', 2); W(f, 'screens[3].widget', 'change', 0.04)
K(f, 'screens[4].widget', 1 - 1.1 * 0.9, 4); W(f, 'screens[4].widget', 'pounds', (50 - 49.5) / 100)
K(f, 'screens[5].widget', 100 * 1.5 * 0.5); W(f, 'screens[5].widget', 'half-start', 50)
lv.claim(round(80 * 1.1 * 0.9, 2) == 79.2 and round(80 * 0.9 * 1.1, 2) == 79.2, 'l7 screens[6]: both close at £79.20')
lv.claim(round(1.3 * 0.7, 4) == 0.91 and round(1 - 0.3 ** 2, 4) == 0.91, 'l7 screens[7]: 0.91')
lv.stated(f, 'screens[8].explain.text', 'for any real swing', False)    # p = 0 is a real swing with p^2 = 0
K(f, 'screens[9].widget', pc(8000, 10000)); W(f, 'screens[9].widget', 'same', 0.2)
# byKey "pounds": "You wrote the £2,000.00 gap as a percentage" -> a learner types 2000, the engine stores 20 (content holds 0.02, typed 2)
W(f, 'screens[9].widget', 'pounds', 2000 / 100)
T(f, 'screens[9].explain.text', 100)
lv.claim(round(200 * 0.9 * 1.1, 2) == 198, 'l7 quiz[0]: £198')
K(f, 'quiz[2].widget', 1 / 0.5 - 1); W(f, 'quiz[2].widget', 'same', 0.5)
lv.claim(round(0.5 * 1.5, 2) == 0.75, 'l7 quiz[2]: a 50% rise from half gets back to three quarters')
lv.claim(round(1.25 * 0.8, 10) == 1, 'l7 quiz[3]: 1.25 x 0.8 = 1')

# ---------- l8 growth on growth ----------
f = 'l8-'
D(f, 'screens[1].widget', 1000 * 1.1 ** 2); R(f, 'screens[1].widget', 'simple', 1200)
rows = node(f, 'screens[2].widget.rows')
lv.claim(rows[2][2]['answer'] == round(1210 * 0.1, 2) and rows[2][3]['answer'] == round(1210 * 1.1, 2), 'l8 screens[2]: year 3')
lv.claim(rows[3][1]['answer'] == 1331 and rows[3][2]['answer'] == round(1331 * 0.1, 2) and rows[3][3]['answer'] == round(1331 * 1.1, 2), 'l8 screens[2]: year 4')
K(f, 'screens[3].widget', 1000 * 1.1 ** 5, 2); W(f, 'screens[3].widget', 'simple', 1500); W(f, 'screens[3].widget', 'times-n', 1000 * 1.1 * 5, 2)
T(f, 'screens[3].explain.text', round(1000 * 1.1 ** 5 - 1500, 2))
K(f, 'screens[4].widget', 2500 * 1.04 ** 2, 2); W(f, 'screens[4].widget', 'simple', 2700); W(f, 'screens[4].widget', 'one-year', 2600)
D(f, 'screens[5].widget', round(50 * 0.9 ** 3, 2)); R(f, 'screens[5].widget', 'simple', 35); R(f, 'screens[5].widget', 'pounds', 35.5)
T(f, 'screens[5].explain.text', round((1 - 0.9 ** 3) * 100, 1))
comp = node(f, 'screens[6].canvas.params.series[0].values')
lv.claim(all(abs(comp[n] - round(1000 * 1.1 ** n, 2)) < 1e-9 for n in range(11)), 'l8 screens[6]: compound series is 1000 x 1.1^n')
T(f, 'screens[6].widget.options[0].text', round(1000 * 1.1 ** 10, 2)); T(f, 'screens[6].widget.options[2].text', 1000 * 1.1 * 10)
T(f, 'screens[7].explain.text', round(500 * 1.06 ** 3, 3)); T(f, 'screens[7].explain.text', 500 * 1.18)
K(f, 'screens[9].widget', 1.05 * 0.96 * 1.025 - 1, 4)
W(f, 'screens[9].widget', 'added', 0.035); W(f, 'screens[9].widget', 'multiplier', 1.05 * 0.96 * 1.025, 4)
pv = node(f, 'screens[9].canvas.params.series[0].values')
lv.claim(abs(pv[3] - round(200 * 1.05 * 0.96 * 1.025, 2)) < 1e-9, 'l8 screens[9]: £200 becomes £206.64')
lv.claim(round(800 * 1.05 ** 2, 2) == 882, 'l8 quiz[0]: £882')
K(f, 'quiz[1].widget', 1 - 0.8 ** 2, 4); W(f, 'quiz[1].widget', 'added', 0.4); W(f, 'quiz[1].widget', 'kept', 0.64)
K(f, 'quiz[2].widget', 10000 * 1.06 * 0.99, 2); W(f, 'quiz[2].widget', 'subtract', 10500)
lv.claim(round(1.1 ** 3, 4) == 1.331 and round(1 + 3 * 0.11, 4) == 1.33, 'l8 quiz[3]: 1.331 against 1.33')

# ---------- review-2 ----------
f = 'review'
K(f, 'items[0].widget', pc(32, 40)); W(f, 'items[0].widget', 'new-base', 8 / 40); W(f, 'items[0].widget', 'pounds', 0.08)
lv.claim(round(68 / 0.85, 2) == 80 and round(68 * 1.15, 2) == 78.2 and round(68 * 0.85, 2) == 57.8 and round(68 / 0.15, 2) == 453.33, 'review-2 items[1]: options')
K(f, 'items[2].widget', 250 * 1.1 * 0.9, 2); W(f, 'items[2].widget', 'cancel', 250); W(f, 'items[2].widget', 'fall-only', 225)
K(f, 'items[3].widget', 4000 * 1.03 ** 2, 2); W(f, 'items[3].widget', 'simple', 4240); W(f, 'items[3].widget', 'one', 4120)
K(f, 'items[4].widget', 25 / 125); W(f, 'items[4].widget', 'new-base', 25 / 100)
K(f, 'items[5].widget', pc(64, 64 / 0.8)); W(f, 'items[5].widget', 'same', 0.2)
T(f, 'items[6].explain.text', round(1.01 * 1.01 * 0.98, 6))
lv.claim(round((1 - 1.01 * 1.01 * 0.98) * 100, 2) == 0.03, 'review-2 items[6]: down about 0.03%')
K(f, 'items[7].widget', 54 - 54 / 1.2, 2); W(f, 'items[7].widget', 'of-total', 10.8); W(f, 'items[7].widget', 'pre', 45)
K(f, 'items[8].widget', math.sqrt(45 / 20) - 1, 4); W(f, 'items[8].widget', 'halved', pc(20, 45) / 2, 4); W(f, 'items[8].widget', 'total', pc(20, 45))

# ---------- homework-2 ----------
f = 'homework'
K(f, 'items[0].widget', -pc(18400, 16560), 4); W(f, 'items[0].widget', 'new-base', 1840 / 16560, 4); W(f, 'items[0].widget', 'kept', 0.9)
K(f, 'items[1].widget', 71.40 / 1.05, 2); W(f, 'items[1].widget', 'took-off', 71.40 * 0.95, 2)
K(f, 'items[2].widget', pc(1250, 3000)); W(f, 'items[2].widget', 'ratio', 3000 / 1250); W(f, 'items[2].widget', 'new-base', 1750 / 3000, 4)
K(f, 'items[3].widget', pc(120, 150)); W(f, 'items[3].widget', 'same', 30 / 150)
K(f, 'items[4].widget', 10000 * (1.08 * 0.98) ** 2, 2)
W(f, 'items[4].widget', 'net-six', 10000 * 1.06 ** 2, 2); W(f, 'items[4].widget', 'simple', 10000 * 1.12, 2); W(f, 'items[4].widget', 'no-fee', 10000 * 1.08 ** 2, 2)
T(f, 'items[4].explain.text', round(10000 * 1.08 ** 2 - round(10000 * (1.08 * 0.98) ** 2, 2), 2))
lv.claim(10000 * 1.08 ** 2 - 10000 * 1.0584 ** 2 > 400, 'homework-2 items[4]: fees cost more than 2% of the start twice')
n = next(k for k in range(1, 50) if 1.07 ** k >= 2)
K(f, 'items[6].widget', n); W(f, 'items[6].widget', 'simple', math.ceil(1 / 0.07)); W(f, 'items[6].widget', 'short', n - 1)
W(f, 'items[6].widget', 'simple-floor', math.floor(1 / 0.07))
T(f, 'items[6].explain.text', round(1000 * 1.07 ** 10, 2)); T(f, 'items[6].explain.text', round(1.07 ** 11, 3))
prod = 1.03 * 0.98 * 1.04 * 0.94 * 1.01
lv.claim(round(3 - 2 + 4 - 6 + 1, 9) == 0, 'homework-2 items[7]: the daily returns add to 0%')
K(f, 'items[7].widget', prod - 1, 6); W(f, 'items[7].widget', 'sign', 1 - prod, 6)
T(f, 'items[7].explain.text', round(1.03 * 0.98 * 1.04, 6)); T(f, 'items[7].explain.text', round(1.03 * 0.98 * 1.04 * 0.94, 6))
T(f, 'items[7].explain.text', round(prod, 6))
# AM-GM: multipliers with an arithmetic mean of 1 have a product at most 1, so "cost money even when they look balanced" holds
lv.claim(prod <= 1, 'homework-2 items[7]: returns that add to 0% compound to a loss (AM-GM)')
m = lv.text(f, 'items[8].model')
for v in (15000, 7500, 2500, 33.3, 0.75):
    T(f, 'items[8].model', v)
lv.claim(round(2500 / 7500 * 100, 1) == 33.3, 'homework-2 items[8]: 33.3% recovery')

lv.check_wrongs()
lv.report()
