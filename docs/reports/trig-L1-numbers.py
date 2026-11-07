"""Number recompute for trig level 1 (Triangles): l1 to l5, review-1, homework-1. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names, recomputed from the slip), the numeric
options of choice items and the numbers stated in prose, hints, feedback and explanations are recomputed here, most of
them two ways (method 1 the formula, method 2 coordinates, the other ratio or the inverse). Pure standard library.
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it.
Run from anywhere:  python3 docs/reports/trig-L1-numbers.py
Failing checks on the current content are findings in docs/reviews/review-trig-1-3.md.
"""
import sys, os
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt, radians, degrees, pi, hypot, isclose
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("trig", 1)
S = lambda d: sin(radians(d)); C = lambda d: cos(radians(d)); Tn = lambda d: tan(radians(d))
aS = lambda x: degrees(asin(x)); aC = lambda x: degrees(acos(x)); aT = lambda x: degrees(atan(x))


def node(f, path):
    return _walk(lv._file(f)[1], path)[0]


def K(f, w, val, nd=None):
    """The widget's key equals the recomputed value, and agrees with it within the widget's tolerance."""
    n = node(f, w)
    a = n['answer']
    tol = n.get('tol', {})
    t = tol.get('abs', 0) if isinstance(tol, dict) else tol
    lv.claim(abs(a - val) <= max(t, 1e-9) + 1e-9, f'{f} {w}: key {a} within {t} of {val:.6g}')
    if nd is not None:
        lv.claim(round(val, nd) == round(a, nd), f'{f} {w}: key {a} is {val:.6g} rounded to {nd} dp')


def W(f, w, wid, val, nd=2):
    """The wrong[] entry with this id holds the value its slip gives (to nd places)."""
    ws = node(f, w).get('wrong', [])
    hit = [x for x in ws if x.get('id') == wid]
    if not hit:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    x = hit[0]
    if 'value' in x:
        lv.claim(round(x['value'], nd) == round(val, nd), f'{f} {w} wrong {wid}: {x["value"]} = {val:.6g}')
    else:
        lo, hi = (x['from'], x['to']) if 'from' in x else tuple(x['region']['x'])
        lv.claim(lo <= val <= hi, f'{f} {w} wrong {wid}: region [{lo}, {hi}] holds the slip {val:.4g}')


def O(f, w, i, val, nd=2):
    """Option i of a choice widget shows val (to nd places)."""
    lv.expect(f, f'{w}.options[{i}].text', round(val, nd))


T = lv.expect

# ---------- l1 squares on the sides ----------
f = 'l1'
lv.claim(isclose(hypot(4, 3), 5), 'l1 s1: arc lands 5 along'); lv.claim(1 + 5 == 6, 'l1 s1: P target x = O.x + 5 = 6')
lv.claim(1 + 4 + 3 == 8, 'l1 s1: added slip lands at x = 8')
K(f, 'screens[2].widget', hypot(6, 8)); W(f, 'screens[2].widget', 'added', 6 + 8); W(f, 'screens[2].widget', 'squares', 36 + 64)
K(f, 'screens[3].widget', 3 ** 2 + 4 ** 2); W(f, 'screens[3].widget', 'frame', 49); W(f, 'screens[3].widget', 'triangles', 4 * 6); W(f, 'screens[3].widget', 'sides', 3 + 4)
K(f, 'screens[4].widget', 7 * 7 - 4 * (3 * 4 / 2)); W(f, 'screens[4].widget', 'one-triangle', 49 - 6)
K(f, 'screens[5].widget', hypot(12, 5)); W(f, 'screens[5].widget', 'added', 17); W(f, 'screens[5].widget', 'no-root', 169)
W(f, 'screens[5].widget', 'subtracted', sqrt(144 - 25)); W(f, 'screens[5].widget', 'difference', 7)
K(f, 'screens[6].widget', sqrt(100 - 36)); W(f, 'screens[6].widget', 'added', sqrt(136)); W(f, 'screens[6].widget', 'subtracted-lengths', 4)
W(f, 'screens[6].widget', 'no-root', 64); W(f, 'screens[6].widget', 'sum', 16)
c6 = node(f, 'screens[6].canvas.state.points'); lv.claim(isclose(hypot(c6[2]['x'] - c6[0]['x'], c6[2]['y'] - c6[0]['y']), 10), 'l1 s6: canvas OB is 10')
K(f, 'screens[7].widget', sqrt(2), 3); W(f, 'screens[7].widget', 'added', 2); W(f, 'screens[7].widget', 'half', 1.5)
O(f, 'screens[8].widget', 0, sqrt(625 - 49)); O(f, 'screens[8].widget', 1, sqrt(625 + 49)); O(f, 'screens[8].widget', 2, 18); O(f, 'screens[8].widget', 3, 32)
p = {q['id']: (q['x'], q['y']) for q in node(f, 'screens[8].canvas.state.points')}
lv.claim(isclose(hypot(p['Q'][0] - p['P'][0], p['Q'][1] - p['P'][1]), 7, abs_tol=1e-6), 'l1 s8: canvas PQ = 7')
lv.claim(isclose(hypot(p['R'][0] - p['Q'][0], p['R'][1] - p['Q'][1]), 24, abs_tol=1e-6), 'l1 s8: canvas QR = 24 (method 2)')
K(f, 'screens[10].widget', hypot(1.2, 0.5)); W(f, 'screens[10].widget', 'added', 1.7); W(f, 'screens[10].widget', 'no-root', 1.69); W(f, 'screens[10].widget', 'difference', 0.7)
T(f, 'screens[10].explain.text', 0.4 - (-0.8)); T(f, 'screens[10].explain.text', 1.5 - 1.0)
O(f, 'quiz[0].widget', 0, hypot(8, 15)); O(f, 'quiz[0].widget', 1, 23); O(f, 'quiz[0].widget', 2, 289); O(f, 'quiz[0].widget', 3, sqrt(225 - 64))
K(f, 'quiz[1].widget', sqrt(169 - 25)); W(f, 'quiz[1].widget', 'added', sqrt(194)); W(f, 'quiz[1].widget', 'lengths', 8); W(f, 'quiz[1].widget', 'no-root', 144)
lv.claim(36 + 64 == 100 and 11 ** 2 == 121, 'l1 q2: 6,8,11 is not right-angled'); lv.claim(36 + 64 < 121, 'l1 q2: largest angle obtuse (cosine rule sign)')
K(f, 'quiz[3].widget', hypot(8 - 2, 11 - 3)); W(f, 'quiz[3].widget', 'added', 14); W(f, 'quiz[3].widget', 'no-root', 100)

# ---------- l2 ratios that stay ----------
f = 'l2'
K(f, 'screens[1].widget', 3 * 12 / 4); W(f, 'screens[1].widget', 'added', 3 + 8); W(f, 'screens[1].widget', 'same', 3); W(f, 'screens[1].widget', 'across', 12)
T(f, 'screens[2].explain.text', 0.6); lv.claim(isclose(3 / 5, 6 / 10), 'l2 s2: 3/5 = 6/10')
T(f, 'screens[3].hints[2].text', round(2.5 / hypot(1, 2.5), 3)); T(f, 'screens[3].hints[2].text', round(0.75 / hypot(1, 0.75), 3))
O(f, 'screens[4].widget', 0, 6 / 8); O(f, 'screens[4].widget', 1, 6 / 10, 1); O(f, 'screens[4].widget', 2, 8 / 10, 1); O(f, 'screens[4].widget', 3, 8 / 6)
O(f, 'screens[5].widget', 0, 8 / 10, 1); O(f, 'screens[5].widget', 2, 8 / 6)
T(f, 'screens[6].explain.text', round(3 / sqrt(10), 3)); T(f, 'screens[6].explain.text', round(1 / sqrt(10), 3))
pr = {q['id']: (q['x'], q['y']) for q in node(f, 'screens[7].canvas.state.points')}
lv.claim(isclose(hypot(pr['Q'][0] - pr['P'][0], pr['Q'][1] - pr['P'][1]), 6) and isclose(hypot(pr['R'][0] - pr['Q'][0], pr['R'][1] - pr['Q'][1]), 8), 'l2 s7: canvas PQ = 6, QR = 8, so cos R = 8/10')
K(f, 'screens[9].widget', 1.00 / 4 * 10); W(f, 'screens[9].widget', 'unscaled', 1.0); W(f, 'screens[9].widget', 'added', 1 + 6)
W(f, 'screens[9].widget', 'flipped', 4 / 1 * 10); W(f, 'screens[9].widget', 'gap', 103 - 100)
# The chart on l2 screens[9] has no equal scales (params.equal absent); the explanation calls the gradient the tangent of the
# angle on the chart and says the window length cannot change it. l3 screens[9] says the drawn angle changes when an axis stretches.
eq = node(f, 'screens[9].canvas.params').get('equal', False)
lv.stated(f, 'screens[9].explain.text', 'that is the tangent of its angle on a chart', eq)
lv.stated(f, 'screens[9].explain.text', 'A gradient is a tangent, so the length of the window does not change it', eq)
K(f, 'quiz[1].widget', 0.6); W(f, 'quiz[1].widget', 'scaled', 0.6 * 4); W(f, 'quiz[1].widget', 'side', 0.6 * 20); W(f, 'quiz[1].widget', 'quarter', 0.6 / 4)
T(f, 'quiz[0].explain.text', round(12 / 13, 3)); T(f, 'quiz[2].explain.text', round(8 / 15, 3))
lv.claim(5 ** 2 + 12 ** 2 == 13 ** 2 and 8 ** 2 + 15 ** 2 == 17 ** 2, 'l2 quiz: 5,12,13 and 8,15,17 are right-angled')

# ---------- l3 sides and angles ----------
f = 'l3'
K(f, 'screens[1].widget', 20 * Tn(35)); W(f, 'screens[1].widget', 'sine', 20 * S(35)); W(f, 'screens[1].widget', 'equal', 20)
T(f, 'screens[1].prose', round(Tn(35), 3))
K(f, 'screens[2].widget', 6 * S(70), 2); W(f, 'screens[2].widget', 'divided', 6 / S(70)); W(f, 'screens[2].widget', 'cos', 6 * C(70)); W(f, 'screens[2].widget', 'tan', 6 * Tn(70))
K(f, 'screens[3].widget', 30 / S(40), 2); W(f, 'screens[3].widget', 'multiplied', 30 * S(40)); W(f, 'screens[3].widget', 'cos', 30 / C(40)); W(f, 'screens[3].widget', 'ground', 30 / Tn(40))
T(f, 'screens[4].explain.text', round(3 / C(25), 2)); T(f, 'screens[4].explain.text', round(C(25), 4))
K(f, 'screens[5].widget', aT(1.5 / 4)); T(f, 'screens[5].explain.text', round(aT(0.375), 2)); W(f, 'screens[5].widget', 'steep', 45)
K(f, 'screens[6].widget', aS(4.2 / 5), 1); W(f, 'screens[6].widget', 'tan', aT(0.84), 1); W(f, 'screens[6].widget', 'cos', aC(0.84), 1); W(f, 'screens[6].widget', 'ratio', 0.84)
lv.claim(isclose(90 - aS(0.84), aC(0.84)), 'l3 s6: top angle 90 - 57.1 = acos(0.84) (method 2)')
O(f, 'screens[7].widget', 0, 12 * Tn(15)); O(f, 'screens[7].widget', 1, 12 * S(15)); O(f, 'screens[7].widget', 2, 12 / Tn(15)); O(f, 'screens[7].widget', 3, 12 / C(15))
K(f, 'screens[9].widget', aT(4 / 5), 1); W(f, 'screens[9].widget', 'flipped', aT(5 / 4), 1); W(f, 'screens[9].widget', 'gradient', 0.8); W(f, 'screens[9].widget', 'sine', aS(0.8), 1)
O(f, 'quiz[0].widget', 0, 8 * C(25)); O(f, 'quiz[0].widget', 1, 8 * S(25)); O(f, 'quiz[0].widget', 2, 8 / C(25)); O(f, 'quiz[0].widget', 3, 8 * Tn(25))
K(f, 'quiz[1].widget', aT(0.7), 1); W(f, 'quiz[1].widget', 'flipped', aT(10 / 7), 1); W(f, 'quiz[1].widget', 'sine', aS(0.7), 1); W(f, 'quiz[1].widget', 'cosine', aC(0.7), 1)
T(f, 'quiz[2].explain.text', round(3.5 / 3, 2)); T(f, 'quiz[2].widget.options[2].text', round(aT(3.5 / 3), 1))
K(f, 'quiz[3].widget', 50 * Tn(32), 2); W(f, 'quiz[3].widget', 'sine', 50 * S(32), 1); W(f, 'quiz[3].widget', 'divided', 50 / Tn(32)); W(f, 'quiz[3].widget', 'cosine', 50 * C(32), 1)

# ---------- l4 exact values ----------
f = 'l4'
lv.claim(isclose(S(45), 1 / sqrt(2)) and isclose(C(45), sqrt(2) / 2) and isclose(Tn(45), 1), 'l4: 45 degree exact values')
lv.claim(isclose(S(30), 0.5) and isclose(C(30), sqrt(3) / 2) and isclose(Tn(30), 1 / sqrt(3)), 'l4: 30 degree exact values')
lv.claim(isclose(S(60), sqrt(3) / 2) and isclose(C(60), 0.5) and isclose(Tn(60), sqrt(3)), 'l4: 60 degree exact values')
lv.claim(isclose(hypot(1, 1), sqrt(2)) and isclose(sqrt(2 ** 2 - 1 ** 2), sqrt(3)), 'l4 s2, s4: diagonal sqrt 2, height sqrt 3 (method 2: Pythagoras)')
lv.claim(60 + 60 + 90 == 210, 'l4 s1: 60, 60 and the right angle make 210')
T(f, 'screens[4].explain.text', round(sqrt(3), 3)); T(f, 'screens[6].feedback.correct', round(1 / sqrt(2), 3))
T(f, 'screens[9].explain.text', round(sqrt(3) / 2, 3)); T(f, 'screens[9].explain.text', round(S(60) / S(30), 2))
T(f, 'screens[9].feedback.byKey.double', 1.5); T(f, 'screens[9].feedback.byKey.double', 3)   # 0.5 * 3 and 0.5 * 6 if sine were proportional
lv.claim(isclose(4 * S(60), 2 * sqrt(3)) and isclose(4 * C(60), 2) and isclose(4 * S(45), 2 * sqrt(2)) and isclose(4 * Tn(60), 4 * sqrt(3)), 'l4 s11: components and slips')
lv.claim(isclose(2 ** 2 + (2 * sqrt(3)) ** 2, 16), 'l4 s11: check 4 + 12 = 16')
T(f, 'screens[11].explain.text', round(2 * sqrt(3), 2))
lv.claim(isclose(10 * S(45), 5 * sqrt(2)) and isclose(10 / sqrt(2), 5 * sqrt(2)), 'l4 q2: 10 sin 45 = 10/sqrt2 = 5 sqrt 2')
T(f, 'quiz[2].explain.text', round(5 * sqrt(2), 2))
K(f, 'quiz[3].widget', 20 * sqrt(3), 2); W(f, 'quiz[3].widget', 'sine', 20 * S(60)); W(f, 'quiz[3].widget', 't30', 20 * Tn(30)); W(f, 'quiz[3].widget', 'hyp', 20 / C(60))
lv.claim(isclose(20 * Tn(60), 20 * sqrt(3)), 'l4 q3: calculator agrees with the exact form')

# ---------- l5 no right angle ----------
f = 'l5'
T(f, 'screens[0].explain.canvas.caption', round(sqrt(9 + 16 - 24 * C(120)), 2)); T(f, 'screens[0].explain.canvas.caption', 37)
cf, bf = 3 * C(60), 3 * S(60)
T(f, 'screens[1].prose', round(bf, 3)); K(f, 'screens[1].widget', hypot(bf, 4 - cf), 2)
lv.claim(isclose(hypot(bf, 4 - cf), sqrt(9 + 16 - 24 * C(60))), 'l5 s1: two triangles agree with the cosine rule (method 2)')
W(f, 'screens[1].widget', 'pyth', 5); W(f, 'screens[1].widget', 'whole-base', hypot(bf, 4)); W(f, 'screens[1].widget', 'height', bf)
c2 = 25 + 49 - 70 * C(40)
K(f, 'screens[3].widget', sqrt(c2), 2); W(f, 'screens[3].widget', 'no-term', sqrt(74)); W(f, 'screens[3].widget', 'no-root', c2); W(f, 'screens[3].widget', 'order', sqrt((74 - 70) * C(40)))
T(f, 'screens[3].hints[2].text', round(70 * 0.766, 2))
K(f, 'screens[4].widget', aC(12 / 60), 1); W(f, 'screens[4].widget', 'wrong-side', aC((36 + 49 - 25) / 84), 1); W(f, 'screens[4].widget', 'ratio', 0.2)
lv.claim((25 + 36 + 49) / 60 > 1, 'l5 s4: the plus slip gives a cosine above 1 (no angle)')
h = 10 * S(40)
T(f, 'screens[5].prose', round(h, 3)); K(f, 'screens[5].widget', h / S(65), 2)
lv.claim(isclose(h / S(65), 10 * S(40) / S(65)), 'l5 s5: sine rule form agrees')
W(f, 'screens[5].widget', 'times', h * S(65)); W(f, 'screens[5].widget', 'height', h); W(f, 'screens[5].widget', 'swapped', 10 * S(65) / S(40))
K(f, 'screens[7].widget', sqrt(144 + 81 - 216 * C(60)), 2); W(f, 'screens[7].widget', 'pyth', 15); W(f, 'screens[7].widget', 'no-root', 117)
W(f, 'screens[7].widget', 'bearing', sqrt(225 - 216 * C(130)))
# bearings 070 and 130 as vectors: method 2 for AL
A7 = (12 * S(70), 12 * C(70)); L7 = (9 * S(130), 9 * C(130))
lv.claim(isclose(hypot(A7[0] - L7[0], A7[1] - L7[1]), sqrt(117)), 'l5 s7: AL from bearing coordinates = sqrt 117 (method 2)')
O(f, 'screens[8].widget', 0, 10 * S(45) / S(30)); O(f, 'screens[8].widget', 1, 10 * S(30) / S(45)); O(f, 'screens[8].widget', 2, 10 * S(105) / S(30)); O(f, 'screens[8].widget', 3, 10, 0)
v = 0.2 ** 2 + 0.15 ** 2 - 2 * 0.2 * 0.15 * C(60)
K(f, 'screens[9].widget', sqrt(v), 4); W(f, 'screens[9].widget', 'pyth', sqrt(0.0625), 4); W(f, 'screens[9].widget', 'diff', 0.05, 4)
W(f, 'screens[9].widget', 'no-root', v, 4); W(f, 'screens[9].widget', 'sum', 0.35, 4)
a9 = (0.2, 0); b9 = (0.15 * C(60), 0.15 * S(60))
lv.claim(isclose(hypot(a9[0] - b9[0], a9[1] - b9[1]), sqrt(v)), 'l5 s9: spread arrow length (method 2)')
K(f, 'quiz[0].widget', sqrt(36 + 64 - 96 * 0.5), 2); W(f, 'quiz[0].widget', 'pyth', 10); W(f, 'quiz[0].widget', 'no-root', 52); W(f, 'quiz[0].widget', 'plus', sqrt(148))
O(f, 'quiz[1].widget', 0, 12 * S(70) / S(50)); O(f, 'quiz[1].widget', 1, 12 * S(50) / S(70)); O(f, 'quiz[1].widget', 2, 12 * S(60) / S(50))
lv.claim(isclose(sqrt(a := 4 + 9 - 12 * C(180)), 5), 'l5 q3: C = 180 gives c = a + b (2 + 3 = 5)')

# ---------- review-1 ----------
f = 'review'
K(f, 'items[0].widget', hypot(9, 12)); W(f, 'items[0].widget', 'added', 21); W(f, 'items[0].widget', 'no-root', 225); W(f, 'items[0].widget', 'subtracted', sqrt(144 - 81))
lv.claim(20 ** 2 + 21 ** 2 == 29 ** 2, 'review-1 i1: 20, 21, 29 is right-angled'); T(f, 'items[1].explain.text', round(20 / 29, 3))
K(f, 'items[2].widget', 39 * 5 / 13); W(f, 'items[2].widget', 'added', 5 + 26); W(f, 'items[2].widget', 'ground', 36); W(f, 'items[2].widget', 'tan', 39 * 5 / 12)
K(f, 'items[3].widget', 40 * Tn(28), 2); W(f, 'items[3].widget', 'sine', 40 * S(28)); W(f, 'items[3].widget', 'divided', 40 / Tn(28))
K(f, 'items[5].widget', aC(32 / 112), 1); W(f, 'items[5].widget', 'opp8', aC((49 + 81 - 64) / 126), 1); W(f, 'items[5].widget', 'opp7', aC((64 + 81 - 49) / 144), 1)
W(f, 'items[5].widget', 'ratio', 32 / 112)
lv.claim(isclose(aC(32 / 112) + aC(66 / 126) + aC(96 / 144), 180), 'review-1 i5: three angles add to 180 (method 2)')
K(f, 'items[6].widget', aT(12 / 5), 1); W(f, 'items[6].widget', 'flipped', aT(5 / 12), 1); W(f, 'items[6].widget', 'gradient', 12 / 5, 1); W(f, 'items[6].widget', 'length', hypot(5, 12))
lv.claim(isclose(hypot(5, 12), 13) and round(aT(12 / 5), 1) == 67.4 and round(aT(5 / 12) + aT(12 / 5), 6) == 90, 'review-1 i6: 5, 12, 13 and the angles 67.4 and 22.6 (method 2: complementary)')
T(f, 'items[6].explain.text', 67.4); T(f, 'items[6].feedback.correct', 67.4)
lv.claim(round(degrees(atan2(14 - 2, 6 - 1)), 1) == 67.4, 'review-1 i6: angle by atan2 on the coordinates (1, 2) to (6, 14)')
lv.claim(isclose(6 * C(30), 3 * sqrt(3)) and isclose(6 * S(30), 3) and isclose(6 * C(30) * 2, 6 * sqrt(3)), 'review-1 i7: key 3 sqrt 3 and slips 3, 6 sqrt 3')
T(f, 'items[7].explain.text', round(3 * sqrt(3), 2))
K(f, 'items[8].widget', 10 * S(50) / S(70), 2); W(f, 'items[8].widget', 'pairing', 10 * S(60) / S(70)); W(f, 'items[8].widget', 'pyth', 10)
# method 2: coordinates. A = (0, 0), B = (10, 0); L on bearing 030 from A and 320 from B
t = 10 / (S(30) - S(320) * C(30) / C(320))
Lx, Ly = t * S(30), t * C(30)
lv.claim(isclose(hypot(Lx, Ly), 10 * S(50) / S(70)), 'review-1 i8: AL from bearing coordinates (method 2)')

# ---------- homework-1 ----------
f = 'homework'
K(f, 'items[0].widget', hypot(60, 34), 2); W(f, 'items[0].widget', 'added', 94); W(f, 'items[0].widget', 'no-root', 4756, 0); W(f, 'items[0].widget', 'subtracted', sqrt(3600 - 1156))
O(f, 'items[1].widget', 0, 4 * C(12)); O(f, 'items[1].widget', 1, 4 * S(12)); O(f, 'items[1].widget', 2, 4 / C(12)); O(f, 'items[1].widget', 3, 4 * Tn(12))
K(f, 'items[2].widget', aT(0.35), 2); W(f, 'items[2].widget', 'flipped', 90 - aT(0.35)); W(f, 'items[2].widget', 'sine', aS(0.35)); W(f, 'items[2].widget', 'gradient', 0.35)
th = atan(0.25)
K(f, 'items[3].widget', 2 * cos(th), 3); W(f, 'items[3].widget', 'vertical', 2); W(f, 'items[3].widget', 'sine', 2 * sin(th), 3); W(f, 'items[3].widget', 'divided', 2 / cos(th), 3)
lv.claim(isclose(2 * cos(th), 2 / sqrt(1 + 0.25 ** 2)), 'homework-1 i3: 2 cos(atan 0.25) = 2 / sqrt(1.0625) (method 2)')
lv.claim(isclose(10 + 10 * S(30) + 10 * S(60), 15 + 5 * sqrt(3)), 'homework-1 i4: perimeter 15 + 5 sqrt 3')
lv.claim(isclose(10 * S(30) + 10 * S(60), 5 + 5 * sqrt(3)) and isclose(10 + 5 + 10 * sqrt(3), 15 + 10 * sqrt(3)) and isclose(10 + 2 * 10 / sqrt(2), 10 + 10 * sqrt(2)), 'homework-1 i4: slips')
T(f, 'items[4].explain.text', round(15 + 5 * sqrt(3), 2))
K(f, 'items[6].widget', hypot(5, 8), 2); W(f, 'items[6].widget', 'added', 13); W(f, 'items[6].widget', 'no-root', 89); W(f, 'items[6].widget', 'sixty', sqrt(89 - 80 * C(60)))
P1 = (5 * S(60), 5 * C(60)); P2 = (P1[0] + 8 * S(150), P1[1] + 8 * C(150))
lv.claim(isclose(hypot(*P2), sqrt(89)), 'homework-1 i6: distance from bearing coordinates (method 2)')
hh = 20 / (sqrt(3) - 1)
K(f, 'items[7].widget', hh, 2); lv.claim(isclose(hh, 10 * (sqrt(3) + 1)), 'homework-1 i7: 20/(sqrt3 - 1) = 10(sqrt3 + 1)')
lv.claim(isclose(Tn(30), hh / (hh + 20)) and isclose(Tn(45), hh / hh), 'homework-1 i7: both elevation angles hold (method 2)')
W(f, 'items[7].widget', 'one-triangle', 20); W(f, 'items[7].widget', 'tan30', 20 * Tn(30)); W(f, 'items[7].widget', 'sixty', 20 * sqrt(3))
s120 = 0.0625 + 0.04 - 2 * 0.25 * 0.2 * C(120)
T(f, 'items[8].model', round(s120, 4)); T(f, 'items[8].model', round(sqrt(s120), 4)); T(f, 'items[8].model', round(sqrt(0.1025), 4))
T(f, 'items[8].model', round((0.0625 + 0.04 - 0.09) / 0.1, 3)); T(f, 'items[8].model', round(180 - aC(0.125), 2)); T(f, 'items[8].model', round(aC(0.125), 2))
lv.claim(isclose(0.0625 + 0.04 - 0.1 * 0.125, 0.09) and isclose(sqrt(0.09), 0.3), 'homework-1 i8: check at 30% gives 0.09')
# method 2: vector addition, arrows 60 degrees apart, then 97.18 apart gives 0.30
vadd = lambda ang: hypot(0.25 + 0.2 * C(ang), 0.2 * S(ang))
lv.claim(isclose(vadd(60), sqrt(s120)) and isclose(vadd(90), sqrt(0.1025)) and isclose(vadd(180 - aC(0.125)), 0.30), 'homework-1 i8: vector sum of the arrows gives 39.05%, 32.02% and 30% (method 2)')
lv.claim(vadd(90) < vadd(60), 'homework-1 i8: the portfolio is smaller at 90 degrees than at 60 (c)')
lv.claim(sum(r['points'] for r in node(f, 'items[8].rubric')) == 10, 'homework-1 i8: rubric sums to 10')

# ---------- fix pass (second-reader findings): numbers in new or reworded text ----------
f = 'l2'
T(f, 'screens[9].explain.text', 0.25); T(f, 'screens[9].explain.text', 2.5)
lv.claim(isclose(1.00 / 4, 0.25) and isclose(0.25 * 10, 2.5), 'l2 s9: 0.25 a day and 2.50 over 10 days')
lv.claim(isclose(6 / 8, 0.75) and isclose(Tn(aT(6 / 8)), 0.75), 'l2 s5: the 0.75 option is 6/8, the tangent of the angle at O (method 2: inverse)')
f = 'l5'
lv.claim(isclose(2 * 6 * 8 * C(60), 48) and isclose(36 + 64 - 48, 52), 'l5 q0: take away 2ab cos C = 48, leaving 52')
lv.claim((25 + 36 + 49) / 60 > 1 and isclose((25 + 36 + 49) / (2 * 5 * 6), 110 / 60), 'l5 s4: adding c^2 gives a cosine above 1, so no learner types 0 for that slip (finding 6)')
lv.claim('plus' not in node(f, 'screens[4].feedback.byKey') and all(x['id'] != 'plus' for x in node(f, 'screens[4].widget.wrong')), 'l5 s4: the plus slip is removed')
f = 'l4'
lv.claim(isclose(10 * sqrt(2) / 2, 5 * sqrt(2)) and round(5 * sqrt(2), 2) == 7.07 and isclose(10 * S(45), 5 * sqrt(2)) and 50 + 50 == 100, 'l4 q2: 10/sqrt2 = 10 sqrt2 / 2 = 5 sqrt2 = 7.07; 50 + 50 = 100')
T(f, 'quiz[2].explain.text', 7.07); T(f, 'quiz[2].explain.text', '5\\sqrt{2}')
T(f, 'screens[2].prose', '**surd**')
f = 'homework'
lv.claim(round(sqrt(3) - 1, 4) == 0.7321 and round(20 / 0.7321, 2) == 27.32 and round(hh, 2) == 27.32, 'homework-1 i7: 20 / 0.7321 = 27.32')
T(f, 'items[7].explain.text', 0.7321); T(f, 'items[7].explain.text', 27.32)

lv.check_wrongs()
lv.report()
