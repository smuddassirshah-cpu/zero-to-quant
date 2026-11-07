"""Number recompute for trig level 2 (The unit circle): l6 to l9, review-2, homework-2. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names), drag and slider targets, numeric option
texts and stated numbers are recomputed, most two ways (method 1 the formula, method 2 the unit-circle point or a
fraction of a turn). Pure standard library.  Run from anywhere:  python3 docs/reports/trig-L2-numbers.py
"""
import sys, os
from math import sin, cos, tan, asin, acos, atan, sqrt, radians, degrees, pi, isclose
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("trig", 2)
S = lambda d: sin(radians(d)); C = lambda d: cos(radians(d))


def node(f, path):
    return _walk(lv._file(f)[1], path)[0]


def K(f, w, val, nd=None):
    n = node(f, w)
    a = n['answer'] if 'answer' in n else n['points'][0]['target']
    a = a[0] if isinstance(a, list) else a
    tol = n.get('tol', n.get('points', [{}])[0].get('tol', 0) if 'points' in n else 0)
    t = tol.get('abs', 0) if isinstance(tol, dict) else tol
    lv.claim(abs(a - val) <= max(t, 1e-9) + 1e-9, f'{f} {w}: key {a} within {t} of {val:.6g}')
    if nd is not None:
        lv.claim(round(val, nd) == round(a, nd), f'{f} {w}: key {a} is {val:.6g} to {nd} dp')


def W(f, w, wid, val, nd=2):
    ws = node(f, w).get('wrong', [])
    hit = [x for x in ws if x.get('id') == wid]
    if not hit:
        return lv.claim(False, f'{f} {w}: wrong id {wid} exists')
    x = hit[0]
    if 'value' in x:
        lv.claim(round(x['value'], nd) == round(val, nd), f'{f} {w} wrong {wid}: {x["value"]} = {val:.6g}')
    else:
        r = x.get('region', {})
        lo, hi = (x['from'], x['to']) if 'from' in x else tuple(r.get('angle', r.get('x')))
        lv.claim(lo <= val <= hi, f'{f} {w} wrong {wid}: region [{lo}, {hi}] holds the slip {val:.4g}')


T = lv.expect

# ---------- l6 beyond 90 ----------
f = 'l6'
K(f, 'screens[1].widget', 180 - 30); lv.claim(isclose(S(150), S(30)), 'l6 s1: sin 150 = sin 30 (method 2)')
W(f, 'screens[1].widget', 'start', 30); W(f, 'screens[1].widget', 'below', 210); W(f, 'screens[1].widget', 'top', 90)
T(f, 'screens[2].explain.text', -0.5); lv.claim(isclose(C(120), -0.5), 'l6 s2: cos 120 = -0.5')
lv.claim(isclose(C(120), -C(60)) and round(S(120), 2) == 0.87, 'l6 s3: (cos 120, sin 120) = (-0.5, 0.87)')
K(f, 'screens[4].widget', S(225)); W(f, 'screens[4].widget', 'no-sign', -S(225), 4); W(f, 'screens[4].widget', 'zero', 0)
lv.claim(isclose(S(225), -S(45)) and isclose(C(225), S(225)), 'l6 s4: 225 point is the 45 point through the centre')
lv.claim(C(300) > 0 and S(300) < 0 and isclose(C(300), 0.5) and round(S(300), 2) == -0.87, 'l6 s5: signs and values at 300')
K(f, 'screens[6].widget', 180); W(f, 'screens[6].widget', 'bottom', 270); W(f, 'screens[6].widget', 'start', 0); W(f, 'screens[6].widget', 'top', 90)
lv.claim(isclose(S(150), 0.5) and S(150) > 0, 'l6 s7: sin 150 = +0.5')
lv.claim(S(240) < 0 and C(240) < 0, 'l6 s8: 240 is in the third quadrant')
lv.claim(isclose(-C(30), C(150)) and round(-C(30), 2) == -0.87, 'l6 s9: cos 150 = -cos 30 = -0.87')
K(f, 'screens[10].widget', 10000 * C(135), 2); W(f, 'screens[10].widget', 'no-sign', -10000 * C(135)); W(f, 'screens[10].widget', 'degrees', 10000 * cos(135), 1)
lv.claim(isclose(10000 * S(135), 7071.067811865476), 'l6 s10: long 7,071.07 of B')
lv.claim(isclose(S(210), -0.5) and round(C(210), 2) == -0.87, 'l6 q0: sin 210 = -0.5, cos 210 = -0.87')
lv.claim(isclose(C(180), -1) and abs(S(180)) < 1e-12, 'l6 q2: (cos 180, sin 180) = (-1, 0)')
lv.claim(isclose(S(140), S(40)) and isclose(S(220), -S(40)) and isclose(S(320), -S(40)) and isclose(S(50), C(40)), 'l6 q3: 140, 220, 320, 50')

# ---------- l7 arc length ----------
f = 'l7'
K(f, 'screens[0].widget', 2 * pi / 4, 4); W(f, 'screens[0].widget', 'deg', 90); W(f, 'screens[0].widget', 'whole', 2 * pi, 4)
W(f, 'screens[0].widget', 'half', pi, 4); W(f, 'screens[0].widget', 'radius', 1); W(f, 'screens[0].widget', 'fraction', 0.25)
lv.claim(round(degrees(1), 1) == 57.3 and 2 * sin(radians(30)) == 1.0000000000000000 or isclose(2 * sin(radians(30)), 1), 'l7 s1: 1 rad = 57.3 deg; chord at 60 deg = radius')
T(f, 'screens[1].widget.options[2].why', round(pi / 4, 2)); T(f, 'screens[1].widget.options[3].why', round(pi / 2, 2))
lv.claim(isclose(3 * pi / 2, 4.71238898038469) and round(3 * pi / 2, 4) == 4.7124, 'l7 s3: 3 pi / 2 = 4.7124')
K(f, 'screens[3].widget', 3 * pi / 2); W(f, 'screens[3].widget', 'quarter', pi / 2); W(f, 'screens[3].widget', 'half', pi)
lv.claim(isclose(45 * pi / 180, pi / 4) and isclose(180 / 45 * pi, 4 * pi), 'l7 s4: 45 deg = pi/4; inverted slip 4 pi')
K(f, 'screens[5].widget', 2 * 180 / pi, 2); W(f, 'screens[5].widget', 'wrong-way', 2 * pi / 180, 4); W(f, 'screens[5].widget', 'two-pi', 360); W(f, 'screens[5].widget', 'sixty', 120)
K(f, 'screens[6].widget', 5 * pi / 2 - 2 * pi, 4); W(f, 'screens[6].widget', 'start', 0); W(f, 'screens[6].widget', 'start2', 2 * pi - 0.01); W(f, 'screens[6].widget', 'half', pi)
T(f, 'screens[7].widget.options[0].why', round(6 * 180 / pi, 1)); T(f, 'screens[7].explain.text', round(2 * pi - 6, 2))
lv.claim(6 < 2 * pi and 6 > 1.5 * pi, 'l7 s7: 6 rad is just short of a full turn')
K(f, 'screens[10].widget', 2 * pi / 12, 4); W(f, 'screens[10].widget', 'degrees', 30); W(f, 'screens[10].widget', 'turns', 1 / 12, 4); W(f, 'screens[10].widget', 'times', 24 * pi, 3)
lv.claim(isclose(150 * pi / 180, 5 * pi / 6) and isclose(150 / 90 * pi, 5 * pi / 3) and isclose(degrees(5 * pi / 3), 300), 'l7 q0: 5pi/6; slip 5pi/3 = 300 deg')
K(f, 'quiz[1].widget', 3 * 180 / pi, 2); W(f, 'quiz[1].widget', 'wrong-way', 3 * pi / 180, 4); W(f, 'quiz[1].widget', 'pi-180', 540)
K(f, 'quiz[2].widget', 2 * pi / 3, 4); W(f, 'quiz[2].widget', 'degrees', 2 * 60); W(f, 'quiz[2].widget', 'no-r', pi / 3, 4)
T(f, 'quiz[3].widget.options[2].why', round(360 / (2 * pi), 1))

# ---------- l8 unrolling ----------
f = 'l8'
lv.claim([round(sin(k * pi / 2)) for k in range(5)] == [0, 1, 0, -1, 0], 'l8 s0: heights 0, 1, 0, -1, 0 at quarter turns')
T(f, 'screens[1].explain.canvas.caption', round(3 * pi / 2, 2)); T(f, 'screens[1].explain.canvas.caption', -1.00)
K(f, 'screens[4].widget', sin(13 * pi / 6)); W(f, 'screens[4].widget', 'neg', -0.5); W(f, 'screens[4].widget', 'zero', 0); W(f, 'screens[4].widget', 'cos', cos(pi / 6), 3)
K(f, 'screens[5].widget', pi / 2, 4); W(f, 'screens[5].widget', 'pi', 3.1); W(f, 'screens[5].widget', 'one', 1)
lv.claim(all(isclose(sin(x + pi / 2), cos(x), abs_tol=1e-12) for x in [0.1 * k for k in range(63)]), 'l8 s5: sin(x + pi/2) = cos x at 63 points')
T(f, 'screens[6].prose', round(cos(2), 2)); T(f, 'screens[6].widget.options[2].text', round(sin(2), 2))
lv.claim(isclose(sin(13 * pi / 6), 0.5), 'l8 s7: sin 13pi/6 = 0.5')
K(f, 'screens[9].widget', 9); lv.claim(isclose(sin(pi * 9 / 6), -1), 'l8 s9: angle 3pi/2 at m = 9')
lv.claim(min(range(12), key=lambda m: 100 + 30 * sin(pi * m / 6)) == 9, 'l8 s9: lowest month by scan is 9 (method 2)')
W(f, 'screens[9].widget', 'half', 6); W(f, 'screens[9].widget', 'peak', 3); W(f, 'screens[9].widget', 'radians', 3 * pi / 2)
lv.claim(isclose(6 / pi * 4.71, 9, abs_tol=0.01) and cos(pi * 6 / 6) < 0, 'l8 s9: 4.71 rad back to 9 months; at m = 6 demand is falling')
T(f, 'screens[9].explain.text', 100 - 30)
K(f, 'quiz[2].widget', sin(5 * pi / 2)); W(f, 'quiz[2].widget', 'zero', 0); W(f, 'quiz[2].widget', 'neg', -1)
lv.claim(isclose(cos(pi), -1), 'l8 q1: cos pi = -1')

# ---------- l9 stretching a wave ----------
f = 'l9'
lv.claim(isclose(min(sin(k / 100) + 3 for k in range(629)), 2, abs_tol=1e-4), 'l9 s0: sin x + 3 has lowest point 2 (scan)')
lv.claim(isclose(2 * pi / 2, pi), 'l9 s1, s2: b = 2 gives period pi')
K(f, 'screens[3].widget', 2 * pi / (pi / 2)); W(f, 'screens[3].widget', 'inverted', 0.25); W(f, 'screens[3].widget', 'two', 2)
lv.claim(isclose(2 * pi / 0.25, 8 * pi), 'l9 s3: b = 1/4 gives period 8 pi')
K(f, 'screens[4].widget', 4 - 1.5); W(f, 'screens[4].widget', 'no-shift', -1.5); W(f, 'screens[4].widget', 'midline', 4); W(f, 'screens[4].widget', 'max', 5.5); W(f, 'screens[4].widget', 'double', 1)
lv.claim(isclose(min(1.5 * sin(k / 100) + 4 for k in range(629)), 2.5, abs_tol=1e-4), 'l9 s4: lowest value by scan (method 2)')
K(f, 'screens[5].widget', 5 * pi / 6 - pi / 2, 4); W(f, 'screens[5].widget', 'wrong-way', -pi / 3); W(f, 'screens[5].widget', 'peak', 5 * pi / 6)
lv.claim(all(isclose(sin(3 * (x + 2 * pi / 3)), sin(3 * x), abs_tol=1e-12) for x in (0.2, 1.3, 2.4)), 'l9 s6: sin 3x repeats after 2pi/3')
lv.claim(isclose(2 * pi / (pi / 6), 12), 'l9 s7: period 12')
lv.claim(isclose(2 * pi / 2, pi) and isclose(2 * pi / 4, pi / 2), 'l9 s8: b = 2 gives pi, b = 4 gives pi/2')
dem = lambda m: 100 + 20 * sin(pi * m / 6); prc = lambda m: 100 + 8 * sin(pi * (m - 2) / 6)
pk_d = max(range(12), key=dem); pk_p = max(range(12), key=prc)
K(f, 'screens[9].widget', pk_p - pk_d); lv.claim((pk_d, pk_p) == (3, 5), 'l9 s9: peaks at months 3 and 5 by scan')
W(f, 'screens[9].widget', 'lead', 15 - 5); W(f, 'screens[9].widget', 'radians', 2 * pi / 6, 4); W(f, 'screens[9].widget', 'period', 12)
K(f, 'quiz[2].widget', 5 + 2); W(f, 'quiz[2].widget', 'amp-only', 2); W(f, 'quiz[2].widget', 'b', 5 + 3); W(f, 'quiz[2].widget', 'mid', 5)
lv.claim(isclose(2 * pi / 0.5, 4 * pi), 'l9 q1: period of sin(x/2)')

# ---------- review-2 ----------
f = 'review'
lv.claim(isclose(C(240), -0.5) and round(S(240), 2) == -0.87, 'review-2 i0: (cos 240, sin 240)')
lv.claim(isclose(270 * pi / 180, 3 * pi / 2) and isclose(180 / 270 * pi, 2 * pi / 3) and isclose(270 / 360 * pi, 3 * pi / 4), 'review-2 i1: 3pi/2 and the slips')
lv.claim(all(isclose(sin(x + pi), -sin(x), abs_tol=1e-12) for x in (0.3, 1.1, 2.9)), 'review-2 i2: sin(x + pi) = -sin x')
K(f, 'items[3].widget', 2 * pi / 4, 4); W(f, 'items[3].widget', 'stretch', 8 * pi, 4); W(f, 'items[3].widget', 'keep', 2 * pi, 4); W(f, 'items[3].widget', 'amp', 2 * pi / 3, 4)
K(f, 'items[5].widget', 5 * 72 * pi / 180, 4); W(f, 'items[5].widget', 'degrees', 5 * 72); W(f, 'items[5].widget', 'no-r', 72 * pi / 180, 4)
lv.claim(isclose(10 * pi / 5, 2 * pi), 'review-2 i5: a fifth of 10 pi is 2 pi (method 2)')
K(f, 'items[6].widget', cos(7 * pi / 6), 3); W(f, 'items[6].widget', 'no-sign', -cos(7 * pi / 6), 3); W(f, 'items[6].widget', 'sin', sin(7 * pi / 6))
lv.claim((7 + 1) / 2 == 4 and 7 - 4 == 3 and isclose(2 * pi / (pi / 4), 8), 'review-2 i7: d = 4, a = 3, b = pi/4')
K(f, 'items[8].widget', 2 * pi / 5, 4); W(f, 'items[8].widget', 'degrees', 72); W(f, 'items[8].widget', 'turns', 0.2); W(f, 'items[8].widget', 'times', 10 * pi, 4)

# ---------- homework-2 ----------
f = 'homework'
lv.claim(isclose(C(300), 0.5) and round(S(300), 2) == -0.87, 'homework-2 i0: (cos 300, sin 300)')
K(f, 'items[1].widget', 2.5 * 180 / pi, 2); W(f, 'items[1].widget', 'wrong-way', 2.5 * pi / 180, 4); W(f, 'items[1].widget', 'pi-180', 450)
lv.claim(pi / 2 < 2.5 < pi, 'homework-2 i1: 2.5 rad in the second quadrant')
lv.claim(isclose(210 * pi / 180, 7 * pi / 6) and isclose(7 * pi / 6, pi + pi / 6), 'homework-2 i2: 7pi/6')
K(f, 'items[3].widget', -sqrt(1 - 0.36)); W(f, 'items[3].widget', 'no-sign', 0.8); W(f, 'items[3].widget', 'subtract', -0.4); W(f, 'items[3].widget', 'square', 0.64)
lv.claim(isclose(S(210), -S(30)), 'homework-2 i4: sin 210 = -sin 30')
K(f, 'items[5].widget', 3.20 + 0.40 * sin(7 * pi / 6)); W(f, 'items[5].widget', 'no-sign', 3.4); W(f, 'items[5].widget', 'degrees', 3.20 + 0.40 * S(7 * pi / 6), 4); W(f, 'items[5].widget', 'mid', 3.2)
T(f, 'items[5].feedback.byKey.degrees', round(7 * pi / 6, 2))
lv.claim(all(sin(pi * m / 6) < 0 for m in (6.5, 8, 10, 11.5)), 'homework-2 i5: below average from month 6 to 12')
K(f, 'items[6].widget', 2 * pi * 3 / 20, 4); W(f, 'items[6].widget', 'days', 3); W(f, 'items[6].widget', 'degrees', 360 * 3 / 20); W(f, 'items[6].widget', 'no-2pi', 0.15)
K(f, 'items[7].widget', 10 * (C(200) - C(30)), 2); W(f, 'items[7].widget', 'no-sign', 10 * (-C(200) - C(30)), 2)
W(f, 'items[7].widget', 'sine', 10 * (S(200) - S(30)), 2); W(f, 'items[7].widget', 'reversed', 10 * (C(30) - C(200)), 2)
T(f, 'items[7].explain.text', round(10 * C(30), 2)); T(f, 'items[7].explain.text', round(10 * C(200), 2)); T(f, 'items[7].explain.text', round(10 * (C(200) - C(30)), 2))
lv.claim(isclose(10 * cos(radians(200)) - 10 * cos(radians(30)), -18.05718, abs_tol=1e-5) and isclose((10 * (C(200) - C(30))), 10 * (-2 * sin(radians(115)) * sin(radians(85)))), 'homework-2 i7: change in east coordinate by the sum-to-product form (method 2)')
K(f, 'items[8].widget', 4 - 3); W(f, 'items[8].widget', 'peak-month', 4); W(f, 'items[8].widget', 'sign', 4 + 3)
lv.claim(max(range(12), key=lambda m: sin(pi * (m - 1) / 6)) == 4 and min(range(12), key=lambda m: sin(pi * (m - 1) / 6)) == 10, 'homework-2 i8: peak 4, trough 10 (method 2)')
R = lambda m: 60000 + 24000 * sin(pi * (m - 2) / 6)
lv.claim(round(R(5)) == 84000 and round(R(11)) == 36000 and round(R(3)) == 72000, 'homework-2 i9: model hits 84,000, 36,000 and 72,000')
T(f, 'items[9].model', 72000); T(f, 'items[9].model', round(pi / 6, 4))

# ---------- fix pass (second-reader findings): numbers in new or reworded text ----------
f = 'l7'
lv.claim(round(2 * pi, 2) == 6.28 and round(pi, 5) == 3.14159 and round(pi / 2, 2) == 1.57, 'l7 s0: circumference 2 pi r, pi = 3.14159, 2 pi = 6.28, pi/2 = 1.57')
T(f, 'screens[3].feedback.byKey.quarter', 1.57)
f = 'l6'
lv.claim(round(C(135), 4) == -0.7071, 'l6 s10: cos 135 = -0.7071')
T(f, 'screens[10].feedback.byKey.degrees', -0.7071)
lv.claim(isclose(S(0), 0, abs_tol=1e-12) and isclose(C(0), 1) and isclose(S(90), 1) and isclose(C(90), 0, abs_tol=1e-12) and isclose(C(180), -1) and isclose(S(270), -1), 'l6 summary: axis values')
f = 'l9'
lv.claim(all(isclose(sin(2 * pi / b * b), 0, abs_tol=1e-9) for b in (0.5, 2, 3)), 'l9 s8: x = 2 pi / b closes one wave (bx = 2 pi)')
f = 'homework'
T(f, 'items[7].explain.text', round(10 * C(30), 2)); T(f, 'items[7].explain.text', -18.06)
lv.claim(round(degrees(2.5), 1) == 143.2, 'homework-2 i1: 2.5 rad = 143.2 degrees')

lv.check_wrongs()
lv.report()
