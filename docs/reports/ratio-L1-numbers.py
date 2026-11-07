"""Number recompute for ratio level 1 (Percentages): l1 to l4, review-1, homework-1. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names, recomputed from the slip) and the numbers
stated in prose, hints, feedback and explanations are recomputed here. Pure standard library.
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it.
Run from anywhere:  python3 docs/reports/ratio-L1-numbers.py
Failing checks on the current content are findings in docs/reviews/review-ratio-1-3.md (numbers given there).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("ratio", 1)


def node(f, path):
    return _walk(lv._file(f)[1], path)[0]


def K(f, w, val, nd=None):
    """The widget's key equals the recomputed value (rounded as the content rounds it)."""
    lv.expect(f, f'{w}.answer', round(val, nd) if nd is not None else val)


def W(f, w, wid, val, nd=None):
    """The wrong[] entry with this id holds the value its slip gives."""
    ws = node(f, w).get('wrong', [])
    ids = [x.get('id') for x in ws]
    if wid not in ids:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    lv.expect(f, f'{w}.wrong[{ids.index(wid)}].value', round(val, nd) if nd is not None else val)


def R(f, w, wid, val):
    """A slider or drag-point wrong region (from/to or region.x) contains the slip value."""
    ws = node(f, w).get('wrong', [])
    hit = [x for x in ws if x.get('id') == wid]
    if not hit:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    x = hit[0]
    lo, hi = (x['from'], x['to']) if 'from' in x else tuple(x['region']['x'])
    lv.claim(lo <= val <= hi, f'{f} {w} wrong {wid}: region [{lo}, {hi}] holds the slip {val}')


def D(f, w, val):
    """A drag-point target or slider answer."""
    n = node(f, w)
    t = n['points'][0]['target'][0] if 'points' in n else n['answer']
    lv.claim(abs(t - val) < 1e-9, f'{f} {w}: target {t} = {val}')


T = lv.expect

# ---------- l1 out of a hundred ----------
f = 'l1-'
shaded = len(node(f, 'screens[1].canvas.state.shade'))
lv.claim(shaded == 37, 'l1 screens[1]: 37 cells shaded')
K(f, 'screens[1].widget', shaded / 100)
W(f, 'screens[1].widget', 'count', shaded)
W(f, 'screens[1].widget', 'thousandths', shaded / 1000)
W(f, 'screens[1].widget', 'rows', 30 / 100)
T(f, 'screens[1].hints[2].text', 30); T(f, 'screens[1].hints[2].text', 37)
D(f, 'screens[2].widget', 45 / 100)
K(f, 'screens[3].widget', 6 * 10 / 100)
W(f, 'screens[3].widget', 'rows', 6 / 100)          # typed 6
W(f, 'screens[3].widget', 'decimal', 0.6 / 100)     # typed 0.6
q = node(f, 'screens[4].canvas.state.shade')
lv.claim(len(q) == 75, 'l1 screens[4]: 75 cells shaded (three quarters)')
K(f, 'screens[4].widget', 3 / 4)
W(f, 'screens[4].widget', 'digits', 34 / 100)
W(f, 'screens[4].widget', 'decimal', 0.75 / 100)
D(f, 'screens[5].widget', 40 / 100); R(f, 'screens[5].widget', 'four-hundredths', 4 / 100)
D(f, 'screens[6].widget', 125 / 100); R(f, 'screens[6].widget', 'thousandths', 125 / 1000); R(f, 'screens[6].widget', 'capped', 1)
T(f, 'screens[7].explain.text', 0.5 / 100)
T(f, 'screens[8].hints[1].text', 0.085 * 100)
T(f, 'screens[9].widget.lines[1].text', 3 / 8)
T(f, 'screens[9].widget.lines[2].text', round(3 / 8 * 100, 1))
K(f, 'screens[10].widget', -0.008)
W(f, 'screens[10].widget', 'one-place', -0.8 / 10)   # typed -8
W(f, 'screens[10].widget', 'decimal', -0.008 / 100)  # typed -0.008
W(f, 'screens[10].widget', 'sign', 0.008)
K(f, 'quiz[0].widget', 7 / 25)
W(f, 'quiz[0].widget', 'digits', 0.725)              # typed 72.5
W(f, 'quiz[0].widget', 'flipped', 25 / 7, 4)         # typed 357.14
K(f, 'quiz[1].widget', 2.5 / 100)
W(f, 'quiz[1].widget', 'one-place', 0.25); W(f, 'quiz[1].widget', 'no-scale', 2.5)
T(f, 'quiz[2].explain.text', 3 / 5 * 100); T(f, 'quiz[2].explain.text', 0.065 * 100)
lv.claim(max(3 / 5, 0.61, 0.59, 0.065) == 0.61, 'l1 quiz[2]: 0.61 is the largest')
K(f, 'quiz[3].widget', 1.2)
W(f, 'quiz[3].widget', 'twelve', 0.12); W(f, 'quiz[3].widget', 'rise', 0.2)

# ---------- l2 building percentages ----------
f = 'l2-'
A = 240
K(f, 'screens[1].widget', A / 10)
W(f, 'screens[1].widget', 'hundred', A / 100); W(f, 'screens[1].widget', 'times', A * 10)
D(f, 'screens[2].widget', 0.3 * A); R(f, 'screens[2].widget', 'pounds', 30); R(f, 'screens[2].widget', 'third', A / 3)
K(f, 'screens[3].widget', A / 100)
W(f, 'screens[3].widget', 'ten', A / 10); W(f, 'screens[3].widget', 'thousand', A / 1000)
K(f, 'screens[4].widget', 0.15 * A)
W(f, 'screens[4].widget', 'divide', A / 15); W(f, 'screens[4].widget', 'one-and-five', 0.11 * A); W(f, 'screens[4].widget', 'ten-only', 0.1 * A)
T(f, 'screens[4].feedback.byKey.divide', round(100 / 15, 1))
K(f, 'screens[5].widget', 0.17 * A, 2)
W(f, 'screens[5].widget', 'one-once', 0.16 * A, 2)
# byKey: "You took 10% seven times, which is 70%" -> 7 x 10% of 240 = 168 (the content holds 192 = 80%)
W(f, 'screens[5].widget', 'seven-tens', 7 * 0.1 * A, 2)
K(f, 'screens[6].widget', 0.99 * A, 2)
W(f, 'screens[6].widget', 'one', 0.01 * A); W(f, 'screens[6].widget', 'ninety', 0.9 * A)
# trap: 4% of 300
lv.claim(0.04 * 300 == 12, 'l2 screens[7]: 4% of £300 is £12')
T(f, 'screens[7].widget.options[0].text', 300 / 4)
T(f, 'screens[7].widget.options[2].text', 4 * 30)
T(f, 'screens[7].widget.options[3].text', 1.2)
# why for £1.20 says "You took 4 lots of 10p": 4 x 10p = 40p, not £1.20 (4 x 30p is)
lv.stated(f, 'screens[7].widget.options[3].why', 'You took 4 lots of 10p', abs(4 * 0.10 - 1.20) < 1e-9)
T(f, 'screens[8].hints[1].text', round(0.23 * 80, 2))
T(f, 'screens[8].widget.options[1].why', round(100 / 23, 1))
lv.claim(23 * 8 == 2.3 * 80, 'l2 screens[8]: 23 x 8 is 230% of £80')
T(f, 'screens[9].widget.lines[3].text', 0.175 * 80)
T(f, 'screens[9].widget.lines[2].text', 0.025 * 80)
K(f, 'screens[10].widget', 0.02 * 1850)
W(f, 'screens[10].widget', 'twenty', 0.2 * 1850); W(f, 'screens[10].widget', 'half', 1850 / 2); W(f, 'screens[10].widget', 'small', 0.002 * 1850)
T(f, 'screens[10].explain.text', 1850 + 37)
lv.claim(abs((1887 - 1850) / 1850 - 0.02) < 1e-12, 'l2 screens[10]: the shares must rise 2% to cover the fee')
K(f, 'quiz[0].widget', 0.15 * 60); W(f, 'quiz[0].widget', 'divide', 60 / 15); W(f, 'quiz[0].widget', 'ten', 6)
K(f, 'quiz[1].widget', 0.03 * 450, 2); W(f, 'quiz[1].widget', 'divide', 450 / 3); W(f, 'quiz[1].widget', 'tens', 0.3 * 450)
K(f, 'quiz[2].widget', 0.005 * 2000); W(f, 'quiz[2].widget', 'no-scale', 0.5 * 2000); W(f, 'quiz[2].widget', 'five', 0.05 * 2000)
K(f, 'quiz[3].widget', 0.95 * 40); W(f, 'quiz[3].widget', 'gap', 0.05 * 40); W(f, 'quiz[3].widget', 'added', 1.05 * 40)

# ---------- l3 what percentage ----------
f = 'l3-'
K(f, 'screens[1].widget', 18 / 25)
W(f, 'screens[1].widget', 'raw', 0.18); W(f, 'screens[1].widget', 'flipped', 25 / 18, 4)
D(f, 'screens[2].widget', 7 / 20)
K(f, 'screens[3].widget', 13 / 50); W(f, 'screens[3].widget', 'raw', 0.13); W(f, 'screens[3].widget', 'halved', 6.5 / 100)
K(f, 'screens[4].widget', 9 / 40); W(f, 'screens[4].widget', 'raw', 0.09); W(f, 'screens[4].widget', 'flipped', 40 / 9, 4)
T(f, 'screens[4].explain.text', 100 / 40)
K(f, 'screens[5].widget', 500 / 400); W(f, 'screens[5].widget', 'flipped', 400 / 500); W(f, 'screens[5].widget', 'rise', 100 / 400)
T(f, 'screens[6].explain.text', 5 - 4); T(f, 'screens[6].widget.options[3].why', 0.01 * 4)
T(f, 'screens[6].widget.options[2].why', 4 + 25)
lv.claim(round(15 / 25, 2) == 0.6 and round(10 / 15 * 100, 1) == 66.7 and 15 / 10 == 1.5 and 10 / 25 == 0.4, 'l3 screens[7]: 60%, 66.7%, 150%, 40%')
T(f, 'screens[8].widget.options[1].why', round(40 / 6 * 100))
T(f, 'screens[8].hints[1].text', 6 / 40 * 100)
T(f, 'screens[9].widget.lines[2].text', 3 / 40); T(f, 'screens[9].explain.text', 7.5 * 2.4)
tot = 4000 + 3500 + 3750 + 1250
lv.claim(tot == 12500, 'l3 screens[10]: the positions add to £12,500')
K(f, 'screens[10].widget', 3500 / tot)
W(f, 'screens[10].widget', 'rest', 3500 / (tot - 3500), 4); W(f, 'screens[10].widget', 'largest', 3500 / 4000)
T(f, 'screens[10].explain.text', 4000 / tot * 100); T(f, 'screens[10].explain.text', 30 - 28)
K(f, 'quiz[0].widget', 45 / 60); W(f, 'quiz[0].widget', 'raw', 0.45); W(f, 'quiz[0].widget', 'flipped', 60 / 45, 4)
K(f, 'quiz[1].widget', 3.5 - 2.5); W(f, 'quiz[1].widget', 'relative', 100 / 3.5, 2)
# relative slip band: 28.57 +- 0.01 misses a learner who types 28.6 (the next item's own accept)
rel = node(f, 'quiz[1].widget')['wrong'][0]
lv.claim(abs(28.6 - rel['value']) <= rel['tol']['abs'], 'l3 quiz[1]: the relative slip band holds 28.6, as rounded in quiz[2]')
K(f, 'quiz[2].widget', 1 / 3.5, 4)
W(f, 'quiz[2].widget', 'points', 0.01); W(f, 'quiz[2].widget', 'new-whole', 1 / 2.5)
T(f, 'quiz[2].widget.accept', round(100 / 3.5, 1))
K(f, 'quiz[3].widget', 26 / 40); W(f, 'quiz[3].widget', 'ratio', 26 / 14, 4); W(f, 'quiz[3].widget', 'down', 14 / 40)

# ---------- l4 multipliers ----------
f = 'l4-'
K(f, 'screens[1].widget', 60 * 0.85); W(f, 'screens[1].widget', 'discount', 0.15 * 60); W(f, 'screens[1].widget', 'pounds', 60 - 15)
lv.claim(len(node(f, 'screens[1].canvas.state.shade.keep')) == 17, 'l4 screens[1]: 17 parts of 5% kept')
D(f, 'screens[2].widget', 0.85); R(f, 'screens[2].widget', 'cut-only', 0.15); R(f, 'screens[2].widget', 'rise', 1.15)
K(f, 'screens[3].widget', 1.15); W(f, 'screens[3].widget', 'rise-only', 0.15); W(f, 'screens[3].widget', 'tenths', 1.5); W(f, 'screens[3].widget', 'whole', 15)
K(f, 'screens[4].widget', 240 * 1.08, 2); W(f, 'screens[4].widget', 'rise-only', 0.08 * 240, 2)
W(f, 'screens[4].widget', 'tenths', 240 * 1.8, 2); W(f, 'screens[4].widget', 'pounds', 248)
K(f, 'screens[5].widget', 350 * 0.94, 2); W(f, 'screens[5].widget', 'fall-only', 0.06 * 350, 2)
W(f, 'screens[5].widget', 'rise', 350 * 1.06, 2); W(f, 'screens[5].widget', 'pounds', 344)
lv.claim(round(80 * 1.05, 2) == 84 and round(80 * 1.5, 2) == 120 and round(80 * 0.05, 2) == 4, 'l4 screens[7]: £84, £120, £4')
lv.claim(round(1 - 0.035, 3) == 0.965, 'l4 screens[8]: 1 - 0.035 = 0.965')
K(f, 'screens[10].widget', 3750 * 1.072, 2)
W(f, 'screens[10].widget', 'return-only', 0.072 * 3750, 2); W(f, 'screens[10].widget', 'tenths', 3750 * 1.72, 2); W(f, 'screens[10].widget', 'pounds', 3757.2)
T(f, 'screens[10].explain.text', round(3750 * 0.928, 2)); T(f, 'screens[10].explain.text', round(1 - 0.072, 3))
K(f, 'quiz[0].widget', 1.12); W(f, 'quiz[0].widget', 'rise-only', 0.12); W(f, 'quiz[0].widget', 'tenths', 1.2)
K(f, 'quiz[1].widget', 45 * 0.8); W(f, 'quiz[1].widget', 'cut-only', 9); W(f, 'quiz[1].widget', 'rise', 45 * 1.2, 2)
K(f, 'quiz[3].widget', 1200 * 1.025, 2); W(f, 'quiz[3].widget', 'rise-only', 30); W(f, 'quiz[3].widget', 'tenths', 1200 * 1.25)
W(f, 'quiz[3].widget', 'pounds', 1202.5)

# ---------- review-1 ----------
f = 'review'
K(f, 'items[0].widget', 0.07); W(f, 'items[0].widget', 'seventy', 0.7); W(f, 'items[0].widget', 'decimal', 0.07 / 100)
K(f, 'items[1].widget', 0.35 * 120, 2); W(f, 'items[1].widget', 'divide', 120 / 35, 4); W(f, 'items[1].widget', 'thirty', 36)
K(f, 'items[2].widget', 600 / 2400); W(f, 'items[2].widget', 'flipped', 2400 / 600); W(f, 'items[2].widget', 'part-part', 600 / 1800, 4)
K(f, 'items[3].widget', 85 * 0.96, 2); W(f, 'items[3].widget', 'fall-only', 3.4); W(f, 'items[3].widget', 'rise', 85 * 1.04, 2)
W(f, 'items[3].widget', 'pounds', 81)
D(f, 'items[4].widget', 5 / 8); R(f, 'items[4].widget', 'small', 0.0625)
K(f, 'items[5].widget', 2350 * 1.02, 2); W(f, 'items[5].widget', 'fee-only', 47); W(f, 'items[5].widget', 'tenths', 2350 * 1.2, 2)
W(f, 'items[5].widget', 'pounds', 2352)
T(f, 'items[6].explain.text', 15 - 12); T(f, 'items[6].widget.options[2].text', 3 / 15 * 100)
T(f, 'items[6].widget.options[3].why', round(0.03 * 12, 2))
K(f, 'items[7].widget', 0.0045); W(f, 'items[7].widget', 'one-place', 0.045); W(f, 'items[7].widget', 'three', 0.45)
T(f, 'items[8].explain.text', 54 / 90 * 100); T(f, 'items[8].explain.text', 66 / 120 * 100)
T(f, 'items[8].widget.options[2].text', 66 - 54)

# ---------- homework-1 ----------
f = 'homework'
vals = [0.004, 0.04, 0.045, 0.4]
lv.claim(vals == sorted(vals), 'homework-1 items[0]: 0.4%, 0.04, 4.5%, 2/5 is smallest first')
K(f, 'items[1].widget', 0.175 * 64, 2); W(f, 'items[1].widget', 'divide', 64 / 17.5, 4); W(f, 'items[1].widget', 'tenths', 64 * 1.75, 2)
T(f, 'items[1].feedback.byKey.divide', round(100 / 17.5, 1))
P = {'a': 2800, 'b': 4200, 'c': 1400, 'd': 5600}
lv.claim(sum(P.values()) == 14000, 'homework-1 items[2]: positions add to £14,000')
flag = {k for k, v in P.items() if v / 14000 >= 0.3}
corr = {o['id'] for o in node(f, 'items[2].widget')['options'] if o.get('correct')}
lv.claim(flag == corr, 'homework-1 items[2]: the flagged set is B and the bond fund')
K(f, 'items[3].widget', 2000 * 1.05 - 2000 * 1.02, 2)
W(f, 'items[3].widget', 'no-fee', 100); W(f, 'items[3].widget', 'sale', 2100); W(f, 'items[3].widget', 'points', 3)
T(f, 'items[3].explain.text', round(60 / 2040 * 100, 1))
T(f, 'items[4].explain.text', 1.5 - 0.75)
T(f, 'items[4].widget.options[3].why', round(0.0075 * 1.5, 2))
K(f, 'items[5].widget', 12400 * (1 - 0.0275), 2)
W(f, 'items[5].widget', 'sign', 12400 * 1.0275, 2); W(f, 'items[5].widget', 'tenths', 12400 * 0.725, 2); W(f, 'items[5].widget', 'loss-only', 12400 * 0.0275, 2)
# long-form rebalance
fee = 0.02 * 3000; cash = 5000 - 3000 - fee; sh = 12000; bo = 6000; tot = sh + bo + cash
m = lv.text(f, 'items[7].model')
for v in (fee, cash, tot, round(sh / tot * 100, 2), round(bo / tot * 100, 2), round(cash / tot * 100, 2),
          round(sh / tot * 100 - 45, 2), round((sh / tot * 100 - 45) / 45 * 100, 1), sh * 1.08, bo * 0.98,
          sh * 1.08 + bo * 0.98 + cash, sh * 1.08 + bo * 0.98 + cash - tot, round((sh * 1.08 + bo * 0.98 + cash - tot) / tot * 100, 2),
          round((sh * 1.08 + bo * 0.98 + cash - 20000) / 20000 * 100, 1)):
    T(f, 'items[7].model', round(v, 2))
lv.claim(round(sh / tot * 100, 2) + round(bo / tot * 100, 2) + round(cash / tot * 100, 2) == 100.00, 'homework-1 items[7]: rounded weights sum to 100.00%')
D(f, 'items[8].widget', 0.005)

lv.check_wrongs()
lv.report()
