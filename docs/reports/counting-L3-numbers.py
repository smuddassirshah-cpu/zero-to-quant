"""Second-reader number check for counting level 3 (l9 to l13, review-3, homework-3: vectors), written by the session V
reader (docs/reviews/review-counting-1-3.md). Each value is found twice: method 1 by components (end minus start,
row by row), method 2 by an independent route (math.hypot and atan2 for lengths and angles, the cosine rule for the
dot product, walking unit steps on the grid for a move). Canvases are read from the JSON so the diagram and the text agree.
A check marked FINDING fails while the content is wrong and passes once the fix in the review lands.
Run: python3 docs/reports/counting-L3-numbers.py   (exits 0 when every check passes)
"""
import math
import os
import sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("counting", 3)
L = lambda f: lv.files[f]
sub = lambda b, a: tuple(x - y for x, y in zip(b, a))
add = lambda a, b: tuple(x + y for x, y in zip(a, b))
mul = lambda k, a: tuple(k * x for x in a)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
mag = lambda a: math.sqrt(dot(a, a))


def two(label, a, b, tol=1e-9):
    ok = a == b if not isinstance(a, float) and not isinstance(b, float) else abs(a - b) < tol
    lv.claim(ok, f'{label}: {a} = {b}')
    return b


def walk(a, b):
    """Method 2 for a move: step one unit at a time from a to b and count signed steps."""
    x = y = 0
    while a[0] + x != b[0]:
        x += 1 if b[0] > a[0] else -1
    while a[1] + y != b[1]:
        y += 1 if b[1] > a[1] else -1
    return (x, y)


def ang(a, b):
    return math.degrees(math.acos(dot(a, b) / (mag(a) * mag(b))))


def ang2(a, b):                     # method 2: difference of polar angles
    d = abs(math.degrees(math.atan2(a[1], a[0]) - math.atan2(b[1], b[0])))
    return min(d, 360 - d)


def parallel(u, v):
    return u[0] * v[1] - u[1] * v[0] == 0


def vecs(f, i):
    return {v['id']: v for v in L(f)['screens'][i]['canvas']['params']['vectors']}


def E(f, path, *vals):
    for v in vals:
        lv.expect(f, path, v)


# ---------------- l9 arrows ----------------
m = two('l9 s1 move A(1,1) to B(4,3)', sub((4, 3), (1, 1)), walk((1, 1), (4, 3)))
lv.claim(tuple(vecs('l9-arrows', 1)['m']['v']) == m and tuple(vecs('l9-arrows', 1)['m']['from']) == (1, 1), 'l9 s1 canvas arrow is (3, 2) from (1, 1)')
lv.claim(round(mag(m), 1) == round(math.hypot(3, 2), 1) == 3.6, 'l9 s1: the length is about 3.6')
v4 = vecs('l9-arrows', 4)
lv.claim(tuple(v4['A']['v']) == tuple(v4['D']['v']) == tuple(v4['u']['v']) == (2, 1) and tuple(v4['B']['v']) == (-2, -1) and tuple(v4['Cc']['v']) == (1, 2), 'l9 s4 canvas: A and D equal u; B reversed; C swapped')
ab = two('l9 s5 drone A(1,4) to B(6,1)', sub((6, 1), (1, 4)), walk((1, 4), (6, 1)))
lv.claim([r[1]['answer'] for r in L('l9-arrows')['screens'][5]['widget']['rows']] == list(ab), 'l9 s5 table key is (5, -3)')
pq = two('l9 s6 P(4,3) to Q(1,5)', sub((1, 5), (4, 3)), walk((4, 3), (1, 5)))
lv.claim(pq == (-3, 2) and sub((4, 3), (1, 5)) == (3, -2) and add((4, 3), (1, 5)) == (5, 8), 'l9 s6 options: (-3, 2), back (3, -2), added (5, 8)')
v7 = vecs('l9-arrows', 7)
lv.claim(tuple(v7['ab']['v']) == sub(tuple(v7['b']['v']), tuple(v7['a']['v'])) and tuple(v7['ab']['from']) == tuple(v7['a']['v']), 'l9 s7 canvas: AB = b - a, drawn from the head of a')
trade = two('l9 s8 trade', sub((150, 450), (300, 200)), (-150, 250))
lv.claim([r[1]['answer'] for r in L('l9-arrows')['screens'][8]['widget']['rows']] == list(trade), 'l9 s8 table key is (-150, 250)')
v8 = vecs('l9-arrows', 8)
lv.claim(tuple(v8['trade']['v']) == mul(0.01, trade) and tuple(v8['after']['v']) == (1.5, 4.5), 'l9 s8 canvas in hundreds matches')
ship = two('l9 quiz ship', sub((4, -1), (-2, 3)), walk((-2, 3), (4, -1)))
lv.claim(ship == (6, -4) and add((4, -1), (-2, 3)) == (2, 2), 'l9 quiz[0]: (6, -4); added (2, 2)')

# ---------------- l10 adding ----------------
v0 = vecs('l10-adding-arrows', 0)
u0, w0 = tuple(v0['u']['v']), tuple(v0['v']['v'])
lv.claim((u0, w0) == ((3, 1), (1, 2)), 'l10 s0 canvas: u = (3, 1), v = (1, 2)')
lv.claim(add(u0, w0) == tuple(L('l10-adding-arrows')['screens'][0]['widget']['points'][0]['target']) == (4, 3), 'l10 s0 target (4, 3)')
lv.claim((u0[0] * w0[0], u0[1] * w0[1]) == (3, 2), 'l10 s0 multiplied slip region (3, 2)')
lv.claim(add((3, 1), (1, 3)) == (4, 4), 'l10 s1 explain: (3,1) + (1,3) = (4,4)')
s2 = two('l10 s2 a + b', add((-2, 5), (4, -3)), (2, 2))
lv.claim([r[1]['answer'] for r in L('l10-adding-arrows')['screens'][2]['widget']['rows']] == list(s2), 'l10 s2 table key')
lv.claim(mul(-3, (2, -1)) == (-6, 3) and mul(3, (2, -1)) == (6, -3), 'l10 s3: k = -3; 3u = (6, -3)')
u4 = (2, -1)
opts = {'a': (4, -2), 'b': (-6, 3), 'c': (1, -0.5), 'd': (1, -2), 'e': (2, 1)}
lv.claim({k for k, v in opts.items() if parallel(u4, v)} == {'a', 'b', 'c'}, 'l10 s4: exactly a, b, c are parallel to u')
lv.claim((1 / 2, -2 / -1) == (0.5, 2.0) and (2 / 2, 1 / -1) == (1.0, -1.0), 'l10 s4 byKey: d needs k = 1/2 and 2; e needs 1 and -1')
lv.claim(sub((4, 1), (1, 3)) == (3, -2) and sub((1, 3), (4, 1)) == (-3, 2) and add((4, 1), (1, 3)) == (5, 4), 'l10 s5: u - v = (3, -2); reverse (-3, 2); sum (5, 4)')
lv.claim(sub((1, 3), (4, 1)) == walk((4, 1), (1, 3)) == (-3, 2), 'l10 s6: D = v - u = (-3, 2)')
lv.claim(add(mul(2, (1, -3)), (4, 5)) == (6, -1), 'l10 s7: 2(1,-3) + (4,5) = (6, -1)')
lv.claim_text('l10', 'screens[7].widget.options[1].why', 'doubled only the top entry', add((2 * 1, -3), (4, 5)) == (5, -1),
              'FINDING l10 s7 option b: doubling only the top entry gives (6, 2); (5, -1) comes from doubling only the bottom')
lv.claim(add((1, -6), (4, 5)) == (5, -1), 'l10 s7: doubling only the bottom entry gives (5, -1)')
lv.claim(mul(2, add((1, -3), (4, 5))) == (10, 4) and add((2, 6), (4, 5)) == (6, 11), 'l10 s7 options c (10, 4) and d (6, 11)')
port = add(mul(0.6, (1.20, -0.30)), mul(0.4, (0.80, 0.50)))
two('l10 s9 value exposure', round(port[1], 10), 0.02); two('l10 s9 market exposure', round(port[0], 10), 1.04)
E('l10', 'screens[9].widget.wrong', round(-0.30 + 0.50, 2), round((-0.30 + 0.50) / 2, 2), 1.04, round(0.6 * 0.30 + 0.4 * 0.50, 2))
E('l10', 'screens[9].explain.text', 0.72, -0.18, 0.32, 0.20)
lv.claim(add((3, -1), (-5, 4)) == (-2, 3) and sub((3, -1), (-5, 4)) == (8, -5), 'l10 quiz[0]: (-2, 3); subtracted (8, -5)')
lv.claim(parallel((6, -4), (-3, 2)) and not parallel((6, -4), (4, -6)) and not parallel((6, -4), (6, 4)) and not parallel((6, -4), (3, -1)), 'l10 quiz[2]: only (-3, 2) is parallel to m')
lv.claim((3 / 6, -1 / -4) == (0.5, 0.25), 'l10 quiz[2] option d: k = 1/2 and 1/4')
coef = lambda ca, cb: (ca, cb)
lv.claim(coef(2 * 1 - 1, 2 * 3 + 1) == (1, 7) and coef(2 - 1, 6 - 1) == (1, 5) and coef(2 - 1, 3 + 1) == (1, 4) and coef(2 + 1, 6 - 1) == (3, 5), 'l10 quiz[3]: a + 7b; slips a + 5b, a + 4b, 3a + 5b')

# ---------------- l11 how long ----------------
for v, want in (((3, 4), 5), ((-5, 12), 13), ((6, 8), 10), ((-6, -8), 10), ((-8, 15), 17), ((4, -3), 5)):
    two(f'l11 |{v}|', mag(v), float(math.hypot(*v)))
    lv.claim(abs(mag(v) - want) < 1e-9, f'l11 |{v}| = {want}')
E('l11', 'screens[0].widget.wrong', 7, 12, 1)
E('l11', 'screens[1].widget.options', round(math.sqrt(29), 2), round(math.sqrt(50), 2), round(math.sqrt(17), 2))
E('l11', 'screens[2].widget.wrong', 7, 17, round(math.sqrt(144 - 25), 3))
lv.claim(sub((7, 10), (1, 2)) == (6, 8), 'l11 s3: AB = (6, 8)')
E('l11', 'screens[3].widget.wrong', 14, round(mag((8, 12)), 2), round(mag((7, 10)), 2))
th = two('l11 s4 angle of (4, 3)', math.degrees(math.atan(3 / 4)), math.degrees(math.atan2(3, 4)))
E('l11', 'screens[4].widget.answer', round(th, 1))
E('l11', 'screens[4].widget.wrong', round(90 - th, 1), 0.75, round(math.radians(th), 2))
lv.claim(all(abs(x - y) < 1e-12 for x, y in zip(mul(1 / 5, (3, 4)), (0.6, 0.8))) and abs(mag((3 / 7, 4 / 7)) - 5 / 7) < 1e-12 and abs(mag((0.75, 1)) - 1.25) < 1e-12, 'l11 s5: unit (0.6, 0.8); 3/7 slip has length 5/7; (0.75, 1) has length 1.25')
lv.claim(add((6, 8), (6, -8)) == (12, 0) and round(math.sqrt(36 + 64 + 36 + 64), 1) == 14.1, 'l11 s7: |u + v| = 12; four squares give 14.1')
lv.claim(mag((12, 0)) < mag((6, 8)) + mag((6, -8)), 'l11 s7: |u + v| < |u| + |v| here')
r = (0.03, -0.04)
two('l11 s9 |r|', round(mag(r), 10), round(math.hypot(*r), 10))
E('l11', 'screens[9].widget.wrong', 0.07, -0.01, 0.01)
E('l11', 'screens[9].hints', 0.0009, 0.0016, '0.0025')
lv.claim(abs(0.03 ** 2 + 0.04 ** 2 - 0.0025) < 1e-15, 'l11 s9: 0.0009 + 0.0016 = 0.0025')
E('l11', 'quiz[0].widget.options', 17, 7, 23, round(math.sqrt(225 - 64), 1))
lv.claim(sub((5, -4), (-1, 4)) == (6, -8) and add((5, -4), (-1, 4)) == (4, 0), 'l11 quiz[2]: PQ = (6, -8), added (4, 0)')
lv.claim(abs(mag((5 / 13, -12 / 13)) - 1) < 1e-12, 'l11 quiz[3]: unit m has length 1')
v9 = L('l11-how-long')['screens'][9]['canvas']['params']['vectors'][0]['v']
lv.claim(tuple(v9) in ((3, -4), (0.03, -0.04)), f'l11 s9 canvas vector {v9}')

# ---------------- l12 proving ----------------
A, B, Cc = (1, 1), (3, 2), (7, 4)
lv.claim(sub(Cc, A) == mul(3, sub(B, A)) and not parallel(sub((7, 6), A), sub(B, A)), 'l12 s0: AC = 3AB; (7, 6) is off the line')
lv.claim(not parallel((4, 4), (2, 1)) and not parallel((2, 2), (2, 1)) and parallel((-4, -2), (2, 1)), 'l12 s1 option whys: (4,4), (2,2) off; (-4,-2) on')
A, B, Cc = (2, 1), (4, 4), (8, 10)
lv.claim(sub(Cc, A) == mul(3, sub(B, A)) and sub(Cc, B) == mul(2, sub(B, A)), 'l12 s2: k = 3; BC = 2AB')
lv.claim((8 / 4, 10 / 4) == (2.0, 2.5), 'l12 s2 positions slip: 10/4 = 2.5')
A, B, Cc = (0, 1), (2, 2), (6, 5)
lv.claim(sub(B, A) == (2, 1) and sub(Cc, A) == (6, 4) and not parallel((2, 1), (6, 4)), 'l12 s3: rows need k = 3 and 4')
a, b = (6, 2), (2, 4)
lv.claim(mul(0.5, sub(b, a)) == (-2, 1) and sub(b, a) == (-4, 2), 'l12 s4: MN = (-2, 1), AB = (-4, 2)')
v4 = vecs('l12-proving-with-vectors', 4)
lv.claim(all(k in v4 for k in ('mn', 'AB')), 'l12 s4 canvas has mn and AB')
lv.claim(sub((4, 4), (0, 2)) == mul(2, sub((2, 1), (0, 0))) and not parallel(sub((0, 2), (0, 0)), (2, 1)), 'l12 s5: CD = 2AB; AC = (0, 2) not a multiple')
P0, Q0, R0 = (0, 100.00), (3, 104.50), (7, 110.50)
pq, qr = sub(Q0, P0), sub(R0, Q0)
k = Fr(4, 3)
lv.claim(abs(qr[0] - float(k) * pq[0]) < 1e-9 and abs(qr[1] - float(k) * pq[1]) < 1e-9, 'l12 s8: QR = 4/3 PQ')
E('l12', 'screens[8].widget.answer', round(float(k), 4))
E('l12', 'screens[8].widget.wrong', 0.75, round(7 / 3, 4))
price = [w for w in L('l12-proving-with-vectors')['screens'][8]['widget']['wrong'] if w['id'] == 'price'][0]['value']
lv.claim(abs(price - 110.50 / 104.50) <= 0.0005,
         f'FINDING l12 s8 wrong "price" {price} equals 110.50 / 104.50 = {110.50 / 104.50:.4f}')
lv.claim(pq[1] / pq[0] == qr[1] / qr[0] == 1.5, 'l12 s8: a steady £1.50 a day')
lv.claim(sub((7, 11), (1, 2)) == mul(3, sub((3, 5), (1, 2))) and sub((7, 11), (3, 5)) == mul(2, sub((3, 5), (1, 2))), 'l12 quiz[0]: AC = 3AB, BC = 2AB')
lv.claim((1 + 3 * 3) == 10 and 1 + 9 - 1 == 9 and (4 + 3, 4 + 2) == (7, 6), 'l12 quiz[1]: t = 10; slips 9, and (6, 7)')
lv.claim(sub((4, 2), (1, 4)) == (3, -2) and mul(-2, (3, -2)) == (-6, 4), 'l12 quiz[2]: AB = (3, -2), (-6, 4) = -2AB')
a, b = (5.0, 1.0), (1.0, 7.0)
OP = add(a, mul(0.25, sub(b, a)))
lv.claim(all(abs(x - y) < 1e-12 for x, y in zip(OP, add(mul(0.75, a), mul(0.25, b)))), 'l12 quiz[3]: OP = 3/4 a + 1/4 b')

# ---------------- l13 portfolio ----------------
p, d = (30, 20), (2.00, -1.50)
two('l13 s0 P&L', dot(p, d), 30.0)
E('l13', 'screens[0].widget.wrong', 30 * 2 + 20 * 1.5, 60, 2 - 1.5, 50)
p = (3, 2)
lv.claim(dot(p, (2, -3)) == 0 and dot(p, (-3, -2)) == -13 and dot(p, (3, 2)) == 13 and dot(p, (1, 0)) == 3, 'l13 s1: 0, -13, 13, 3')
lv.claim(dot((4, -1), (2, 3)) == 5 and 4 * 2 + 1 * 3 == 11 and (4 - 1) * (2 + 3) == 15, 'l13 s2: 5; slips 11, 15, 8')
pq13 = add((30, 20), (10, -5))
two('l13 s3 combined', dot(pq13, (0.80, -0.40)), dot((30, 20), (0.80, -0.40)) + dot((10, -5), (0.80, -0.40)))
E('l13', 'screens[3].widget.wrong', round(dot((30, 20), (0.8, -0.4)), 6), round(dot((10, -5), (0.8, -0.4)), 6), round(dot((40, 25), (0.8, -0.4)), 6))
u, v = (3, 4), (4, 3)
c = dot(u, v) / (mag(u) * mag(v))
two('l13 s4 cos', round(c, 10), 0.96)
two('l13 s4 angle', round(ang(u, v), 6), round(ang2(u, v), 6))
lv.claim(round(ang(u, v), 1) == 16.3, 'l13 s4: angle 16.3 degrees')
cos_rule = (mag(u) ** 2 + mag(v) ** 2 - mag(sub(u, v)) ** 2) / (2 * mag(u) * mag(v))
two('l13 s4 cos by the cosine rule', round(cos_rule, 10), 0.96)
lv.claim(dot((200, 300), (6, -4)) == 0 and 200 * 6 + 300 * 4 == 2400, 'l13 s5: 0; slip 2400')
lv.claim(abs(dot((30, 20), (1.20, -0.90)) - 18) < 1e-9 and abs(30 * 1.2 + 20 * 0.9 - 54) < 1e-9, 'l13 s6: 18; slip 54')
lv.claim(dot((-1, -1), (-1, -1)) == 2, 'l13 s7 why: (-1,-1).(-1,-1) = 2')
r, mm = (3, 1), (2, 1)
beta = Fr(dot(r, mm), dot(mm, mm))
lv.claim(beta == Fr(7, 5) and dot(sub(r, mul(float(beta), mm)), mm) == 0 or abs(dot(sub(r, mul(float(beta), mm)), mm)) < 1e-12, 'l13 s9: beta = 7/5 and the residual is perpendicular')
E('l13', 'screens[9].widget.wrong', 7, 1.5, round(7 / math.sqrt(5), 4))
w, rt = (0.5, 0.3, 0.2), (0.02, -0.01, 0.04)
two('l13 quiz[0] portfolio return', round(dot(w, rt), 10), 0.015)
lv.claim(round(sum(rt), 4) == 0.05 and round(sum(rt) / 3, 4) == 0.0167 and round(0.010 + 0.003 + 0.008, 4) == 0.021, 'l13 quiz[0] slips 5%, 1.67%, 2.1%')
lv.claim(dot((2, -3), (6, 4)) == 0, 'l13 quiz[1]: perpendicular')
two('l13 quiz[2] angle', round(ang((1, 0), (1, 1)), 6), round(ang2((1, 0), (1, 1)), 6))
lv.claim(dot((3, -2), (-1, 4)) == -11 and (3 - 2) * (-1 + 4) == 3, 'l13 quiz[3]: -11; slip 3')

# ---------------- review-3 ----------------
lv.claim(sub((-1, 4), (3, -2)) == walk((3, -2), (-1, 4)) == (-4, 6), 'review-3 items[0]: (-4, 6)')
lv.claim(sub(mul(3, (1, -2)), (4, -5)) == (-1, -1) and add(mul(3, (1, -2)), (4, -5)) == (7, -11) and sub((1, -2), (4, -5)) == (-3, 3), 'review-3 items[1]: (-1,-1); slips (7,-11), (-3,3)')
lv.claim(sub((4, 9), (-2, 1)) == (6, 8), 'review-3 items[2]: AB = (6, 8)')
E('review', 'items[2].widget.wrong', 14, round(mag((4, 9)), 2))
lv.claim(all(abs(x - y) < 1e-12 for x, y in zip(mul(0.1, (-6, 8)), (-0.6, 0.8))) and (round(-6 / 14, 2), round(8 / 14, 2)) == (-0.43, 0.57), 'review-3 items[3]: (-0.6, 0.8); slip (-0.43, 0.57)')
lv.claim(sub((9, 12 - 1), (1, -1)) == mul(4, sub((3, 2), (1, -1))) and (12 - 1, 3 * 3 - 1) == (11, 8), 'review-3 items[4]: t = 11; k = 3 slip gives 8')
lv.claim(round(mag((5, 0)) ** 2 + 144, 6) == 169 and round(math.sqrt(144 - 25), 1) == 10.9, 'review-3 items[6]: 13; slip sqrt(119) = 10.9')
lv.claim(abs(dot((100, -50), (0.40, 1.20)) + 20) < 1e-9, 'review-3 items[7]: -20')
E('review', 'items[7].widget.wrong', round(100 * 0.4 + 50 * 1.2, 6), 40)
a, b = (2, 1), (-1, 3)
th = two('review-3 items[8] angle', round(ang(a, b), 6), round(ang2(a, b), 6))
E('review', 'items[8].widget.answer', round(th, 1))
E('review', 'items[8].widget.wrong', round(1 / math.sqrt(50), 4), round(math.degrees(math.acos(1 / math.sqrt(5))), 1))

# ---------------- homework-3 ----------------
lv.claim(sub((300, 200, 400), (500, 200, 0)) == (-200, 0, 400) and add((300, 200, 400), (500, 200, 0)) == (800, 400, 400), 'homework-3 items[0]: (-200, 0, 400); slip (800, 400, 400)')
ex = add(add(mul(0.5, (1.10, 0.20)), mul(0.3, (0.90, -0.40))), mul(0.2, (1.30, 0.60)))
two('homework-3 items[1] value', round(ex[1], 10), 0.1); two('homework-3 items[1] market', round(ex[0], 10), 1.08)
E('homework', 'items[1].widget.wrong', round(0.20 - 0.40 + 0.60, 2), 1.08, round(0.10 + 0.12 + 0.12, 2))
two('homework-3 items[2] |r|', round(mag((0.01, -0.02, 0.02)), 10), 0.03)
lv.claim(sub((5, 7), (1, 1)) == mul(2, sub((3, 4), (1, 1))), 'homework-3 items[3]: a = 5')
lv.claim(sub((5, 7), (3, 4)) == mul(1, sub((3, 4), (1, 1))), 'homework-3 items[3]: from B, BP = (a - 3, 3) = 1 x AB, still a = 5')
lv.claim_text('homework', 'items[3].feedback.byKey.from-b', 'You measured the 6 from B', 3 + 1 * 2 == 7,
              'FINDING homework-3 items[3] byKey.from-b: measuring from B still gives a = 5; the slip that gives 7 is a - 1 = 6')
lv.claim(300 * 2 + (-200) * 3 == 0 and 3 * 300 / 2 == 450, 'homework-3 items[4]: b = -200; slip 450')
r3, m3 = (3, -2, 1), (2, -1, 1)
lv.claim(Fr(dot(r3, m3), dot(m3, m3)) == Fr(3, 2) and round(9 / math.sqrt(6), 3) == 3.674 and round(Fr(6 - 2 + 1, 6).__float__(), 3) == 0.833, 'homework-3 items[5]: beta 1.5; slips 3.674, 0.833')
lv.claim((3 * 2 - 2, -3 + 4) == (4, 1) and (6 - 2, -3 - 4) == (4, -7) and (6 - 2, -3 + 2) == (4, -1), 'homework-3 items[6]: 4a + b; slips 4a - 7b, 4a - b')
u, v = (6, 8), (6, -8)
lv.claim(dot(u, v) == -28 and mag(u) ** 2 + mag(v) ** 2 + 2 * dot(u, v) == 144 == mag(add(u, v)) ** 2, 'homework-3 longform: -28, 144, 12')

lv.check_wrongs()
lv.report()
