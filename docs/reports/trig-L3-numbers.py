"""Number recompute for trig level 3 (Identities and equations): l10 to l13, review-3, homework-3. Second reader, session V.

Every graded key, every numeric wrong[] value (the slip its byKey line names), drag targets, numeric option texts and
stated numbers are recomputed, most two ways (method 1 the formula, method 2 a brute-force scan of the curve or the
coordinates). Pure standard library.  Run from anywhere:  python3 docs/reports/trig-L3-numbers.py
Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text and pass once a fix rewords it:
the three printed sums in l12 that do not add up as printed are findings in docs/reviews/review-trig-1-3.md.
"""
import sys, os
from math import sin, cos, tan, asin, acos, atan, atan2, sqrt, radians, degrees, pi, isclose
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk

lv = Level("trig", 3)
S = lambda d: sin(radians(d)); C = lambda d: cos(radians(d)); Tn = lambda d: tan(radians(d))


def node(f, path):
    return _walk(lv._file(f)[1], path)[0]


def K(f, w, val, nd=None):
    n = node(f, w)
    a = n['answer'] if 'answer' in n else n['points'][0]['target']
    a = a[0] if isinstance(a, list) else a
    tol = n.get('tol', n['points'][0].get('tol', 0) if 'points' in n else 0)
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
        lo, hi = tuple(r.get('x'))
        lv.claim(lo <= val <= hi, f'{f} {w} wrong {wid}: region [{lo}, {hi}] holds the slip {val:.4g}')


def solutions(fn, k, lo, hi, step=0.01):
    """Method 2: every x in [lo, hi] (degrees) where fn(x) = k, by sign changes on a fine grid, rounded to 2 dp."""
    xs, out = [lo + i * step for i in range(int((hi - lo) / step) + 1)], []
    for a, b in zip(xs, xs[1:]):
        fa, fb = fn(a) - k, fn(b) - k
        if abs(fa) < 1e-12:
            out.append(round(a, 2))
        elif fa * fb < 0 and abs(fa - fb) < 1:
            out.append(round(a - fa * (b - a) / (fb - fa), 2))
    if abs(fn(hi) - k) < 1e-12:
        out.append(round(hi, 2))
    return sorted(set(out))


T = lv.expect

# ---------- l10 identity from the circle ----------
f = 'l10'
K(f, 'screens[0].widget', sqrt(1 - 0.36)); W(f, 'screens[0].widget', 'sub', 0.4); W(f, 'screens[0].widget', 'noroot', 0.64)
lv.claim(round(max(S(t) + C(t) for t in range(360)), 2) == 1.41 and max(range(360), key=lambda t: S(t) + C(t)) == 45, 'l10 s1: sin + cos peaks at 1.41, at 45')
lv.claim(isclose(S(210) ** 2, 0.25) and isclose(C(210) ** 2, 0.75), 'l10 s1: at 210, 0.25 + 0.75')
K(f, 'screens[2].widget', sqrt(1 - 0.28 ** 2)); W(f, 'screens[2].widget', 'sub', 0.72); W(f, 'screens[2].widget', 'noroot', 0.9216, 4)
K(f, 'screens[3].widget', -0.8); W(f, 'screens[3].widget', 'pos', 0.8); W(f, 'screens[3].widget', 'sub', -0.4); W(f, 'screens[3].widget', 'subpos', 0.4)
K(f, 'screens[4].widget', 0.8 / 0.6, 4); W(f, 'screens[4].widget', 'flip', 0.6 / 0.8); W(f, 'screens[4].widget', 'prod', 0.48)
lv.claim(isclose(Tn(degrees(acos(0.6))), 0.8 / 0.6), 'l10 s4: tan of the angle with cos 0.6 (method 2)')
lv.claim(abs(C(90)) < 1e-12 and abs(C(270)) < 1e-12 and abs(Tn(180)) < 1e-12 and abs(Tn(0)) < 1e-12, 'l10 s5: tan undefined at 90, 270; zero at 0, 180')
lv.claim(isclose(sqrt(1 - 0.36), 0.8) and isclose(1 - 0.6, 0.4), 'l10 s6: 0.8 against Sam 0.4')
lv.claim(round(S(120) + C(120), 2) == 0.37 and isclose(1 - C(120), 1.5) and round(S(120), 2) == 0.87, 'l10 s7: 0.37, 1.5 and 0.87 at 120')
lv.claim(round(S(120), 2) ** 2 - 0.75 < 0.01, 'l10 s7: 0.87 squared is about 0.75')
K(f, 'screens[9].widget', 10000 * sqrt(1 - 0.36)); W(f, 'screens[9].widget', 'sub', 4000); W(f, 'screens[9].widget', 'noroot', 6400); W(f, 'screens[9].widget', 'neg', -8000)
lv.claim(isclose(6000 ** 2 + 8000 ** 2, 10000 ** 2), 'l10 s9: A^2 + B^2 = 10,000^2')
lv.claim(isclose(-sqrt(1 - 0.28 ** 2), -0.96), 'l10 q0: sin = -0.96')
lv.claim(isclose(0.6 / -0.8, -0.75) and isclose(-0.8 / 0.6, -1.3333333333333333) and isclose(0.6 / -0.4, -1.5), 'l10 q2: -0.75 and the slips')
lv.claim(round(C(135), 2) == -0.71 and isclose(Tn(135), -1), 'l10 q3: cos 135 and tan 135')

# ---------- l11 every angle ----------
f = 'l11'
sol = solutions(S, 0.5, 0, 360)
lv.claim(sol == [30.0, 150.0], f'l11 s0: sin x = 0.5 on [0, 360] by scan: {sol}')
K(f, 'screens[0].widget', 150)
lv.claim(all(isclose(degrees(asin(k)) + 180 - degrees(asin(k)), 180) for k in (0.05, 0.5, 0.95)), 'l11 s1: the crossings add to 180 for k in the slider range')
lv.claim(solutions(S, 0.8, 0, 360) == [53.13, 126.87], 'l11 s1, s2: sin x = 0.8 by scan')
K(f, 'screens[1].widget', 180); W(f, 'screens[1].widget', 'period', 360); W(f, 'screens[1].widget', 'quarter', 90)
K(f, 'screens[2].widget', 180 - degrees(asin(0.8)), 2); W(f, 'screens[2].widget', 'plus', 180 + degrees(asin(0.8))); W(f, 'screens[2].widget', 'cosrule', 360 - degrees(asin(0.8)))
W(f, 'screens[2].widget', 'same', degrees(asin(0.8)))
lv.claim(round(S(233.13), 1) == -0.8 and round(S(306.87), 1) == -0.8, 'l11 s2: the slips have sine -0.8')
lv.claim(solutions(S, -0.5, 0, 360) == [210.0, 330.0], 'l11 s3: sin x = -0.5 by scan')
lv.claim(solutions(S, 0.5, 0, 720) == [30.0, 150.0, 390.0, 510.0], 'l11 s4: sin x = 0.5 on [0, 720] by scan')
lv.claim(isclose(S(750), 0.5) and isclose(S(330), -0.5), 'l11 s4: 750 and 330')
sc = solutions(C, 0.5, 0, 360)
lv.claim(sc == [60.0, 300.0], f'l11 s5: cos x = 0.5 by scan: {sc}'); K(f, 'screens[5].widget', 300)
lv.claim(isclose(C(120), -0.5), 'l11 s5: cos 120 = -0.5 (sinrule slip)')
st = solutions(Tn, 1, 0, 360)
lv.claim(st == [45.0, 225.0], f'l11 s6: tan x = 1 by scan: {st}')
K(f, 'screens[6].widget', 225); W(f, 'screens[6].widget', 'sinrule', 135); W(f, 'screens[6].widget', 'cosrule', 315)
s2x = solutions(lambda x: S(2 * x), 0.5, 0, 360)
lv.claim(s2x == [15.0, 75.0, 195.0, 255.0], f'l11 s7: sin 2x = 0.5 by scan: {s2x}')
K(f, 'screens[7].widget', len(s2x)); W(f, 'screens[7].widget', 'two', 2); W(f, 'screens[7].widget', 'one', 1); W(f, 'screens[7].widget', 'eight', 8)
lv.claim(all(isclose(2 * s * s - s - 1, (2 * s + 1) * (s - 1)) for s in (-1, 0, 0.3, 2)), 'l11 s8: factorisation holds')
q8 = [x for x in range(361) if abs(2 * S(x) ** 2 - S(x) - 1) < 1e-9]
lv.claim(q8 == [90, 210, 330], f'l11 s8: whole-degree roots by scan: {q8}')
lv.claim(solutions(C, -0.5, 0, 360) == [120.0, 240.0], 'l11 s9, q0: cos x = -0.5 by scan')
tt = [t / 100 for t in range(1200) if abs(4 * sin(pi * t / 600) - 4 * cos(pi * t / 600)) < 1e-9]
lv.claim(tt == [1.5, 7.5], f'l11 s11: premiums cross at {tt}')
K(f, 'screens[11].widget', 7.5); W(f, 'screens[11].widget', 'first', 1.5); W(f, 'screens[11].widget', 'sinrule', 6 * (3 / 4)); W(f, 'screens[11].widget', 'cosrule', 6 * (7 / 4))
lv.claim(abs(cos(pi * 3 / 6)) < 1e-12 and abs(cos(pi * 9 / 6)) < 1e-12 and isclose(abs(4 * sin(pi * 3 / 6)), 4), 'l11 s11: cos 0 at t = 3, 9 where gas is +-4')
lv.claim(solutions(Tn, -1, 0, 360) == [135.0, 315.0], 'l11 q1: tan x = -1 by scan')
lv.claim(solutions(lambda x: S(x) ** 2, 0.25, 0, 360) == [30.0, 150.0, 210.0, 330.0], 'l11 q2: sin^2 x = 0.25 by scan')
lv.claim(isclose(sin(5 * pi / 6), 0.5) and isclose(sin(11 * pi / 6), -0.5) and isclose(sin(7 * pi / 6), -0.5), 'l11 q3: radian options')

# ---------- l12 adding angles ----------
f = 'l12'
lv.claim(round(S(30) + S(60), 2) == 1.37, 'l12 s0: sin 30 + sin 60 = 1.37')
lv.claim(isclose(C(120), -0.5) and isclose(C(30) * C(150) + S(30) * S(150), C(120)), 'l12 s1: caption at 120 (A at 30, B at 150)')
K(f, 'screens[2].widget', C(15), 4); W(f, 'screens[2].widget', 'split', C(45) - C(30), 4); W(f, 'screens[2].widget', 'minus', C(45) * C(30) - S(45) * S(30), 4)
lv.claim(isclose(C(45) * C(30) + S(45) * S(30), C(15)) and isclose(C(15), (sqrt(6) + sqrt(2)) / 4), 'l12 s2: formula = calculator = (sqrt6 + sqrt2)/4')
# printed sums: 0.6124 + 0.3536 is 0.9660, not 0.9659 (inputs are rounded); 0.3578 + 0.5367 is 0.8945, not 0.8944
lv.stated(f, 'screens[2].explain.text', '0.6124 + 0.3536 = 0.9659', isclose(0.6124 + 0.3536, 0.9659))
lv.stated(f, 'screens[3].explain.text', '0.6124 + 0.3536 = 0.9659', isclose(0.6124 + 0.3536, 0.9659))
lv.stated(f, 'screens[9].hints[2].text', '0.3578 + 0.5367 = 0.8944', isclose(0.3578 + 0.5367, 0.8944))
K(f, 'screens[3].widget', S(75), 4); W(f, 'screens[3].widget', 'split', S(45) + S(30), 4); W(f, 'screens[3].widget', 'minus', S(45) * C(30) - C(45) * S(30), 4)
lv.claim(isclose(S(75), C(15)), 'l12 s3: sin 75 = cos 15')
K(f, 'screens[4].widget', C(75), 4); W(f, 'screens[4].widget', 'plus', C(45) * C(30) + S(45) * S(30), 4)
W(f, 'screens[4].widget', 'split', C(45) + C(30), 4); W(f, 'screens[4].widget', 'first', C(45) * C(30), 4)
K(f, 'screens[5].widget', 0.5 * S(50), 4); W(f, 'screens[5].widget', 'half', 0.25 * S(50), 4); W(f, 'screens[5].widget', 'theta', 0.5 * S(25), 4); W(f, 'screens[5].widget', 'nohalf', S(50), 3)
lv.claim(isclose(0.5 * S(50), 2 * 0.5 * C(25) * S(25)), 'l12 s5: whole triangle = two halves (method 2)')
T(f, 'screens[5].explain.canvas.caption', round(C(25), 4)); T(f, 'screens[5].explain.canvas.caption', round(S(25), 4))
K(f, 'screens[6].widget', S(120), 3); W(f, 'screens[6].widget', 'double', 2 * S(60), 3); W(f, 'screens[6].widget', 'cos', C(120)); W(f, 'screens[6].widget', 'neg', -S(120), 3)
lv.claim(isclose(2 * S(60) * C(60), S(120)), 'l12 s6: 2 sin 60 cos 60 = sin 120')
lv.claim(all(isclose(C(2 * a), 1 - 2 * S(a) ** 2) and isclose(C(2 * a), 2 * C(a) ** 2 - 1) for a in (10, 37, 140)), 'l12 s7: three forms of cos 2A')
lv.claim(all(isclose(C(a - b), C(a) * C(b) + S(a) * S(b)) for a, b in ((100, 20), (300, 10), (250, 40))), 'l12 s8: cos(a - b) formula, including a - b over 180')
ca, sa = 4 / 5, 3 / 5; cb, sb = 1 / sqrt(5), 2 / sqrt(5)
K(f, 'screens[9].widget', cb * ca + sb * sa, 4); W(f, 'screens[9].widget', 'dot', 4 * 1 + 3 * 2); W(f, 'screens[9].widget', 'sine', sb * ca - cb * sa, 4); W(f, 'screens[9].widget', 'plus', cb * ca - sb * sa, 4)
lv.claim(isclose(cb * ca + sb * sa, (4 * 1 + 3 * 2) / (5 * sqrt(5))) and round(degrees(acos(cb * ca + sb * sa)), 1) == 26.6, 'l12 s9: dot product form and 26.6 degrees (method 2)')
lv.claim(round(C(105), 4) == -0.2588 and round(C(60) * C(45) + S(60) * S(45), 4) == 0.9659 and round(C(60) + C(45), 4) == 1.2071, 'l12 q0: options')
lv.claim(isclose(2 * 0.6 * 0.8, 0.96) and isclose(0.64 - 0.36, 0.28), 'l12 q1: 0.96 and the slips')
lv.claim(isclose(2 * 0.36 - 1, -0.28) and isclose(C(2 * degrees(acos(0.6))), -0.28), 'l12 q2: cos 2A = -0.28 (method 2)')
lv.claim(all(isclose(S(x + 90), C(x)) for x in (10, 100, 230)), 'l12 q3: sin(x + 90) = cos x')

# ---------- l13 modelling a cycle ----------
f = 'l13'
D = lambda t: 200 * sin(pi / 6 * (t - 10)) + 500
K(f, 'screens[0].widget', (700 + 300) / 2); W(f, 'screens[0].widget', 'sum', 1000); W(f, 'screens[0].widget', 'peak', 700); W(f, 'screens[0].widget', 'trough', 300)
lv.claim(max(range(1, 13), key=D) == 1 and min(range(1, 13), key=D) == 7, 'l13 s1: model peaks in January, dips in July')
lv.claim(isclose(D(10), 500) and D(10.5) > 500 and isclose(D(-2), 500), 'l13 s1: rises through 500 at t = 10; c = -2 fits too')
K(f, 'screens[2].widget', D(3)); W(f, 'screens[2].widget', 'sign', 400); W(f, 'screens[2].widget', 'deg', 200 * S(pi / 6 * (3 - 10)) + 500)
T(f, 'screens[2].feedback.byKey.deg', round(-7 * pi / 6, 1))
K(f, 'screens[3].widget', 2 * pi / 6, 4); W(f, 'screens[3].widget', 'period', 6); W(f, 'screens[3].widget', 'year', pi / 6, 4); W(f, 'screens[3].widget', 'deg', 60)
K(f, 'screens[4].widget', (380 - 220) / 2); W(f, 'screens[4].widget', 'peak', 380); W(f, 'screens[4].widget', 'range', 160); W(f, 'screens[4].widget', 'mid', 300)
lv.claim(300 - 380 == -80, 'l13 s4: a = 380 would dip to -80')
tt = [t / 100 for t in range(100, 1300) if abs(D(t / 100) - 400) < 1e-9]
lv.claim(tt == [5.0, 9.0], f'l13 s5: D = 400 at {tt}')
K(f, 'screens[5].widget', 5); W(f, 'screens[5].widget', 'principal', 9); W(f, 'screens[5].widget', 'trough', 7); W(f, 'screens[5].widget', 'nosign', 10 + 1)
lv.claim(D(5.5) < 400 < D(4.5), 'l13 s5: falling through 400 in May')
lv.claim(isclose(30 * sin(pi / 2 * (1 - 1)) + 50, 50) and isclose(30 * sin(pi / 2 * (2 - 1)) + 50, 80) and isclose(30 * sin(pi / 2 * (4 - 1)) + 50, 20), 'l13 s6: the key model runs 20 to 80 and rises at t = 1')
t6 = [t / 100 for t in range(1000, 1600) if abs(D(t / 100) - 600) < 1e-9]
lv.claim(t6 == [11.0, 15.0], f'l13 s7: D = 600 at {t6}')
D8 = lambda t: 120 * sin(pi / 6 * (t - 9)) + 400
t8 = [t / 100 for t in range(900, 2100) if abs(D8(t / 100) - 460) < 1e-9]
lv.claim(t8 == [10.0, 14.0], f'l13 s8: D = 460 at {t8}')
K(f, 'screens[8].widget', 14 - 10); W(f, 'screens[8].widget', 'two', 12 - 10); W(f, 'screens[8].widget', 'six', 6); W(f, 'screens[8].widget', 'eight', 12 - 4)
lv.claim((9 - 3) / 2 == 3 and (9 + 3) / 2 == 6, 'l13 q0: a = 3, d = 6')
lv.claim(isclose(2 * pi / 4, pi / 2) and isclose(2 * pi / (pi / 4), 8), 'l13 q1: b = pi/2; the pi/4 slip gives period 8')
lv.claim(max([t / 100 for t in range(200, 1000)], key=lambda t: 5 * sin(pi / 4 * (t - 2)) + 10) == 4.0, 'l13 q2: first peak after 2 at t = 4 (scan)')
lv.claim([t / 100 for t in range(0, 1200) if abs(2 * sin(pi * t / 600) + 7 - 8) < 1e-9][:1] == [1.0], 'l13 q3: first reaches 8 at t = 1 (scan)')

# ---------- review-3 ----------
f = 'review'
K(f, 'items[0].widget', -sqrt(1 - 0.36)); W(f, 'items[0].widget', 'pos', 0.8); W(f, 'items[0].widget', 'sub', -0.4); W(f, 'items[0].widget', 'noroot', -0.64)
lv.claim(solutions(S, -0.8, 0, 360) == [233.13, 306.87], 'review-3 i1: sin x = -0.8 by scan')
K(f, 'items[2].widget', S(15), 4); W(f, 'items[2].widget', 'plus', S(45) * C(30) + C(45) * S(30), 4); W(f, 'items[2].widget', 'split', S(45) - S(30), 4)
lv.claim(isclose(0.6124 - 0.3536, 0.2588), 'review-3 i2: printed difference adds up')
lv.claim(max([t / 100 for t in range(200, 1400)], key=lambda t: 4 * sin(pi / 6 * (t - 2)) + 10) == 5.0, 'review-3 i3: peak 14 at t = 5 (scan)')
K(f, 'items[4].widget', -0.8); W(f, 'items[4].widget', 'pos', 0.8); W(f, 'items[4].widget', 'sine', 0.6); W(f, 'items[4].widget', 'tan', -0.75)
lv.claim(isclose(0.6 / -0.8, -0.75) and isclose(0.5625 * 0.64 + 0.64, 1), 'review-3 i4: tan -0.75 with cos -0.8')
r5 = [x for x in range(361) if abs(2 * C(x) ** 2 - C(x) - 1) < 1e-9]
lv.claim(r5 == [0, 120, 240, 360], f'review-3 i5: roots by scan {r5}')
K(f, 'items[5].widget', len(r5)); W(f, 'items[5].widget', 'ends', 3); W(f, 'items[5].widget', 'two', 2); W(f, 'items[5].widget', 'one', 1)
K(f, 'items[6].widget', 2 * 0.8 * -0.6); W(f, 'items[6].widget', 'pos', 0.96); W(f, 'items[6].widget', 'double', 1.6)
A6 = 180 - degrees(asin(0.8)); lv.claim(isclose(S(2 * A6), -0.96) and 180 < 2 * A6 < 360, 'review-3 i6: sin 2A by the angle (method 2)')
K(f, 'items[7].widget', 0.5 * 6 * 9 * S(150)); W(f, 'items[7].widget', 'nohalf', 27); W(f, 'items[7].widget', 'cos', 0.5 * 54 * C(150)); W(f, 'items[7].widget', 'cosabs', -0.5 * 54 * C(150))
P = lambda t: 3 * sin(pi / 6 * (t - 1)) + 20
p8 = [t / 100 for t in range(0, 1200) if abs(P(t / 100) - 21.5) < 1e-9]
lv.claim(p8 == [2.0, 6.0], f'review-3 i8: P = 21.50 at {p8}')
K(f, 'items[8].widget', 2); W(f, 'items[8].widget', 'second', 6); W(f, 'items[8].widget', 'noshift', 1); W(f, 'items[8].widget', 'deg', 1 + 30 * 6 / pi, 1)

# ---------- homework-3 ----------
f = 'homework'
lv.claim(all(isclose((S(t) + C(t)) ** 2, 1 + S(2 * t)) for t in (10, 45, 200)) and isclose(1 + S(90), 2), 'homework-3 i0: identity, maximum 2 at 45')
lv.claim(all(isclose(S(t) ** 2, (1 - C(2 * t)) / 2) for t in (30, 71, 222)) and isclose((1 - 0.5) / 2, 0.25), 'homework-3 i1: half-angle form and the 30 check')
lv.claim(solutions(S, 0.5, 0, 360) == [30.0, 150.0] and all(abs(2 * S(x) ** 2 + 3 * S(x) - 2 - (2 * S(x) - 1) * (S(x) + 2)) < 1e-12 for x in (10, 99)), 'homework-3 i2: roots 30, 150 and the factorisation')
t2 = solutions(lambda x: Tn(2 * x), sqrt(3), 0, 360)
lv.claim(t2 == [30.0, 120.0, 210.0, 300.0], f'homework-3 i3: tan 2x = sqrt 3 by scan {t2}')
K(f, 'items[3].widget', len(t2)); W(f, 'items[3].widget', 'two', 2); W(f, 'items[3].widget', 'one', 1); W(f, 'items[3].widget', 'eight', 8)
cth = (3 * 5 + 4 * -12) / (5 * 13)
K(f, 'items[4].widget', degrees(acos(cth)), 2); W(f, 'items[4].widget', 'acute', degrees(acos(-cth))); W(f, 'items[4].widget', 'dot', cth)
lv.claim(isclose(degrees(acos(cth)), degrees(atan2(4, 3)) - degrees(atan2(-12, 5))), 'homework-3 i4: angle from the two directions (method 2)')
A = lambda t: 3 * sin(pi * t / 6); B = lambda t: 3 * sin(pi / 6 * (t - 4))
eq = [t / 100 for t in range(0, 1200) if abs(A(t / 100) - B(t / 100)) < 1e-9]
lv.claim(eq == [5.0, 11.0], f'homework-3 i5: A = B at {eq}')
K(f, 'items[5].widget', 11); W(f, 'items[5].widget', 'first', 5); W(f, 'items[5].widget', 'twelve', 17); W(f, 'items[5].widget', 'half', 8)
lv.claim(round(A(8), 1) == -2.6 and round(B(8), 1) == 2.6, 'homework-3 i5: at t = 8, -2.6 and 2.6')
G = lambda t: 220 * sin(pi / 6 * (t - 11)) + 600
lv.claim(round(G(2)) == 820 and round(G(8)) == 380 and round(G(5)) == 600, 'homework-3 i6: D(2), D(8), D(5)')
lv.claim(all(isclose(220 * sin(pi / 6 * (t + 1)) + 600, G(t)) for t in (0, 3.3, 8)), 'homework-3 i6: c = -1 and c = 11 give one model')
g6 = [t / 100 for t in range(1000, 1700) if abs(G(t / 100) - 710) < 1e-9]
lv.claim(g6 == [12.0, 16.0], f'homework-3 i6: D = 710 at {g6}')
lv.claim(all(G(t / 10) > 710 for t in range(121, 160)) and G(11.9) < 710 and G(16.1) < 710, 'homework-3 i6: above 710 only between t = 12 and t = 16 (4 months)')
lv.claim(all(isclose(220 * sin(pi / 6 * (t - 5)) + 600, 1200 - G(t)) for t in (1, 3.3, 8)), 'homework-3 i6: c = 5 gives 1200 - D')
lv.claim(max(range(1, 13), key=lambda t: 220 * sin(pi / 6 * (t - 5)) + 600) == 8, 'homework-3 i6: the c = 5 curve peaks in August')
lv.claim(G(5.01) < G(4.99), 'homework-3 i6: demand is falling through May')
T(f, 'items[6].model', 'D(2) = 220'); T(f, 'items[6].model', 'D(5) = 220'); T(f, 'items[6].model', 't = 12$ or $t = 16'); T(f, 'items[6].model', 'peaking in August')
K(f, 'items[7].widget', 63 / 65, 4); W(f, 'items[7].widget', 'split', 3 / 5 + 12 / 13, 4); W(f, 'items[7].widget', 'cos', (20 - 36) / 65, 4); W(f, 'items[7].widget', 'minus', (15 - 48) / 65, 4)
lv.claim(isclose(S(degrees(asin(0.6)) + degrees(acos(5 / 13))), 63 / 65), 'homework-3 i7: by the angles (method 2)')
K(f, 'items[8].widget', 10 * 2 / sqrt(5), 2); W(f, 'items[8].widget', 'linear', 10 * 2 / 3); W(f, 'items[8].widget', 'b', 10 / sqrt(5)); W(f, 'items[8].widget', 'tan', 5)
lv.claim(isclose(10 * C(degrees(atan(0.5))), 10 * 2 / sqrt(5)) and isclose(10 * S(degrees(atan(0.5))), 10 / sqrt(5)) and round(degrees(atan(0.5)), 2) == 26.57, 'homework-3 i8: by the angle (method 2)')
lv.claim(sum(r['points'] for r in node(f, 'items[6].rubric')) == 10, 'homework-3 i6: rubric sums to 10')

# ---------- fix pass (second-reader findings): numbers in new or reworded text ----------
f = 'l12'
lv.claim(isclose(0.61237 + 0.35355, 0.96592, abs_tol=1e-9) and round(C(45) * C(30), 5) == 0.61237 and round(S(45) * S(30), 5) == 0.35355 and round(C(15), 4) == 0.9659, 'l12 s2 and s3: 0.61237 + 0.35355 = 0.96592 as printed, and cos 15 = 0.9659')
T(f, 'screens[2].explain.text', '0.61237 + 0.35355 = 0.96592'); T(f, 'screens[3].explain.text', '0.61237 + 0.35355 = 0.96592')
lv.claim(isclose(0.35777 + 0.53666, 0.89443, abs_tol=1e-9) and round(0.4472136 * 0.8, 5) == 0.35777 and round(0.8944272 * 0.6, 5) == 0.53666 and round(0.89443, 4) == 0.8944, 'l12 q: 0.35777 + 0.53666 = 0.89443, which rounds to 0.8944')
T(f, 'screens[9].hints[2].text', '0.35777 + 0.53666 = 0.89443')
lv.claim(isclose(C(300 - 10), C(70)) and 360 - 290 == 70, 'l12 s8: a - b = 290 gives the triangle angle 70 with the same cosine')
f = 'homework'
lv.claim(3 * 5 + 4 * -12 == -33 and 5 * 13 == 65 and round(degrees(acos(-33 / 65)), 2) == 120.51, 'homework-3 i4: dot -33, lengths 5 and 13, angle 120.51')
T(f, 'items[4].prose', '|\\mathbf{u}| = 5')

lv.check_wrongs()
lv.report()
