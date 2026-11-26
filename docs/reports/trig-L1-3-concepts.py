#!/usr/bin/env python3
"""Concept audit trig-1-3 (round 1): independent recomputation of the trig course.

Run from anywhere:  python docs/reports/trig-L1-3-concepts.py
Exits 0 only if every check passes. A check that fails because the content is
wrong is left failing on purpose and is a finding in docs/reviews/audit-trig-1-3.md.

Sections
  A  every numeric key, and the named slips, recomputed from the item's own data
  B  solution sets of the trigonometric equations, found by a root scan
  C  fluency families swept over their whole variable range
  D  canvas lines: every straight line drawn on a plane ends on a drawn point
  E  Monte Carlo and numerical checks of the stated rules
  F  checks tied to findings (these fail while the content is as audited)

Fix pass: the F2 gate matched '12 \\times 0.2679' as a substring, so it also
caught the fixed text '0.26795'; it is re-pointed to the old figure followed by
a non-digit. No check was changed otherwise; F1, F3, F4 and F5 skip on the
fixed text because their old wording is gone.
"""
import json, math, os, re, sys, itertools
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'trig')
fails, passed = [], 0


def ok(cond, msg):
    global passed
    if cond:
        passed += 1
    else:
        fails.append(msg)


def load(name):
    return json.load(open(os.path.join(SRC, name + '.json')))


pi = math.pi
rad = math.radians
S = lambda d: math.sin(rad(d))
C = lambda d: math.cos(rad(d))
T = lambda d: math.tan(rad(d))
aS = lambda v: math.degrees(math.asin(v))
aC = lambda v: math.degrees(math.acos(v))
aT = lambda v: math.degrees(math.atan(v))
sq = math.sqrt


def node(name, path):
    d = load(name)
    cur = d
    for part in re.findall(r'(\w+)\[(\d+)\]', path):
        cur = cur[part[0]][int(part[1])]
    return cur


def chk(name, path, key, slips=None, given=None):
    """key: the true value(s); slips: {id: value the named mistake produces}.
    given: the value a learner gets from the rounded figures the item supplies."""
    n = node(name, path)
    w = n['widget']
    tol = w.get('tol', 0)
    tol = tol.get('abs', 0) if isinstance(tol, dict) else tol
    if 'answers' in w:
        got = sorted(w['answers'])
        ok(len(got) == len(key) and all(abs(a - b) <= tol + 1e-9 for a, b in zip(got, sorted(key))),
           f'A {name} {path}: answers {got} but recomputed {sorted(key)}')
    else:
        ok(abs(w['answer'] - key) <= tol + 1e-9, f"A {name} {path}: key {w['answer']} but recomputed {key:.6f} (tol {tol})")
        if given is not None:
            ok(abs(w['answer'] - given) <= tol + 1e-9, f"A {name} {path}: key {w['answer']} rejects {given:.6f}, the value from the item's rounded figures")
    wr = {o['id']: o for o in w.get('wrong', [])}
    for sid, val in (slips or {}).items():
        if sid not in wr:
            ok(False, f'A {name} {path}: no slip {sid}')
            continue
        o = wr[sid]
        st = o.get('tol', {'abs': 0})
        st = st.get('abs', 0) if isinstance(st, dict) else st
        if 'from' in o:
            ok(o['from'] - 1e-9 <= val <= o['to'] + 1e-9, f"A {name} {path}: slip {sid} range {o['from']}..{o['to']} misses {val:.4f}")
        elif isinstance(o['value'], str):
            got = sorted(float(x) for x in o['value'].split(','))
            ok(all(abs(a - b) <= max(st, 0.011) for a, b in zip(got, sorted(val))), f'A {name} {path}: slip {sid} {got} vs {val}')
        else:
            ok(abs(o['value'] - val) <= max(st, 1e-9) + 1e-9, f"A {name} {path}: slip {sid} stored {o['value']} but the mistake gives {val:.6f} (tol {st})")
    # no slip may sit inside the key's band
    if 'answer' in w and isinstance(w['answer'], (int, float)):
        for sid, o in wr.items():
            if isinstance(o.get('value'), (int, float)):
                st = o.get('tol', {'abs': 0}); st = st.get('abs', 0) if isinstance(st, dict) else st
                ok(abs(o['value'] - w['answer']) > tol + st, f'A {name} {path}: slip {sid} overlaps the key band')


# ---------------------------------------------------------------- A: keys and slips
L = 'l1-squares-on-sides'
chk(L, 'screens[2]', sq(36 + 64), {'added': 14, 'squares': 100})
chk(L, 'screens[3]', 49 - 2 * 12, {'frame': 49, 'triangles': 24, 'sides': 7})
chk(L, 'screens[4]', 49 - 4 * 6, {'frame': 49, 'triangles': 24, 'one-triangle': 43})
chk(L, 'screens[5]', sq(144 + 25), {'added': 17, 'no-root': 169, 'subtracted': sq(144 - 25), 'difference': 7})
chk(L, 'screens[6]', sq(100 - 36), {'added': sq(136), 'subtracted-lengths': 4, 'no-root': 64, 'sum': 16})
chk(L, 'screens[7]', sq(2), {'added': 2, 'side': 1, 'half': 1.5})
chk(L, 'screens[10]', math.hypot(0.4 + 0.8, 1.5 - 1.0), {'added': 1.7, 'no-root': 1.69, 'difference': 0.7})
chk(L, 'quiz[1]', sq(169 - 25), {'added': sq(194), 'lengths': 8, 'no-root': 144})
chk(L, 'quiz[3]', math.hypot(6, 8), {'added': 14, 'no-root': 100})
tr = node(L, 'screens[8]')['canvas']['state']['points']
P, R, Q = [(p['x'], p['y']) for p in tr]
ok(abs(math.dist(P, Q) - 7) < 1e-6 and abs(math.dist(Q, R) - 24) < 1e-6 and abs(math.dist(P, R) - 25) < 1e-9, 'A l1 trap triangle is not 7, 24, 25')
ok(abs((Q[0] - P[0]) * (Q[0] - R[0]) + (Q[1] - P[1]) * (Q[1] - R[1])) < 1e-6, 'A l1 trap: no right angle at Q')
ok(abs(sq(674) - 25.96) < 0.005 and abs(sq(161) - 12.69) < 0.005, 'A l1 wrong options 25.96 / 12.69')

L = 'l2-ratios-that-stay'
chk(L, 'screens[1]', 3 * 12 / 4, {'added': 3 + 8, 'same': 3, 'across': 12})
chk(L, 'screens[9]', 10 * 1.0 / 4, {'unscaled': 1.0, 'added': 1 + 6, 'flipped': 4 / 1 * 10, 'gap': 3})
chk(L, 'quiz[1]', 12 / 20, {'scaled': 0.6 * 4, 'side': 12, 'quarter': 0.6 / 4})
ok(abs(2.5 / sq(1 + 2.5 ** 2) - 0.928) < 5e-4 and abs(3 / sq(10) - 0.949) < 5e-4 and abs(1 / sq(10) - 0.316) < 5e-4, 'A l2 captions 0.928, 0.949, 0.316')
P, R, Q = [(p['x'], p['y']) for p in node(L, 'screens[7]')['canvas']['state']['points']]
ok(abs(math.dist(P, Q) - 6) < 1e-6 and abs(math.dist(Q, R) - 8) < 1e-6 and abs(math.dist(P, R) - 10) < 1e-9, 'A l2 trap triangle is not 6, 8, 10')

L = 'l3-sides-and-angles'
chk(L, 'screens[1]', 20 * T(35), {'sine': 20 * S(35), 'equal': 20})
chk(L, 'screens[2]', 6 * S(70), {'divided': 6 / S(70), 'cos': 6 * C(70), 'tan': 6 * T(70)}, given=6 * 0.9397)
chk(L, 'screens[3]', 30 / S(40), {'multiplied': 30 * S(40), 'cos': 30 / C(40), 'ground': 30 / T(40)}, given=30 / 0.6428)
chk(L, 'screens[5]', aT(1.5 / 4), {'steep': 45})
chk(L, 'screens[6]', aS(4.2 / 5), {'tan': aT(0.84), 'cos': aC(0.84), 'ratio': 0.84})
chk(L, 'screens[9]', aT(4 / 5), {'flipped': aT(5 / 4), 'gradient': 0.8, 'sine': aS(0.8)})
chk(L, 'quiz[1]', aT(0.7), {'flipped': aT(10 / 7), 'sine': aS(0.7), 'cosine': aC(0.7)})
chk(L, 'quiz[3]', 50 * T(32), {'sine': 50 * S(32), 'divided': 50 / T(32), 'cosine': 50 * C(32)}, given=50 * 0.6249)
ok(abs(3 / C(25) - 3.31) < 0.005, 'A l3 plank 3.31')
for txt, val in (('7.25', 8 * 0.9063), ('3.38', 8 * 0.4226), ('8.83', 8 / 0.9063), ('3.73', 8 * T(25))):
    ok(abs(float(txt) - val) < 0.006, f'A l3 quiz[0] option {txt} vs {val:.4f}')
ok(abs(aT(3.5 / 3) - 49.4) < 0.05 and 3.5 / 3 > 1, 'A l3 quiz[2]')
for txt, val in (('3.11', 12 * 0.2588), ('12.42', 12 / 0.9659)):
    ok(abs(float(txt) - val) < 0.006, f'A l3 trap option {txt} vs {val:.4f}')

L = 'l4-exact-values'
chk(L, 'quiz[3]', 20 * sq(3), {'sine': 20 * S(60), 't30': 20 * T(30), 'hyp': 20 / C(60)})
ok(abs(S(30) - .5) < 1e-12 and abs(C(45) - 1 / sq(2)) < 1e-12 and abs(T(60) - sq(3)) < 1e-12 and abs(S(60) - sq(3) / 2) < 1e-12
   and abs(T(30) - 1 / sq(3)) < 1e-12 and abs(C(30) - sq(3) / 2) < 1e-12, 'A l4 exact values')
ok(abs(S(60) / S(30) - 1.73) < 0.005, 'A l4 trap: doubling 30 multiplies the sine by about 1.73')
ok(abs(4 * S(60) - 2 * sq(3)) < 1e-12 and abs(4 * T(60) - 4 * sq(3)) < 1e-12 and abs(4 * S(45) - 2 * sq(2)) < 1e-12, 'A l4 transfer options')
ok(abs(10 * S(45) - 5 * sq(2)) < 1e-12, 'A l4 quiz 5 root 2')

L = 'l5-no-right-angle'
cosr = lambda a, b, Cd: sq(a * a + b * b - 2 * a * b * C(Cd))
chk(L, 'screens[1]', cosr(3, 4, 60), {'pyth': 5, 'whole-base': math.hypot(4, 3 * S(60)), 'height': 3 * S(60)})
chk(L, 'screens[3]', cosr(5, 7, 40), {'no-term': sq(74), 'no-root': 74 - 70 * 0.7660, 'order': sq((74 - 70) * 0.7660)}, given=sq(74 - 70 * 0.7660))
chk(L, 'screens[4]', aC((25 + 36 - 49) / 60), {'wrong-side': aC((36 + 49 - 25) / 84), 'ratio': 0.2})
chk(L, 'screens[5]', 10 * S(40) / S(65), {'times': 10 * S(40) * S(65), 'height': 10 * S(40), 'swapped': 10 * S(65) / S(40)}, given=6.428 / 0.9063)
chk(L, 'screens[7]', cosr(12, 9, 60), {'pyth': 15, 'no-root': 117, 'bearing': cosr(12, 9, 130)})
chk(L, 'screens[9]', cosr(0.2, 0.15, 60), {'pyth': 0.25, 'diff': 0.05, 'no-root': 0.0325, 'sum': 0.35})
chk(L, 'quiz[0]', cosr(6, 8, 60), {'pyth': 10, 'no-root': 52, 'plus': sq(100 + 48)})
for txt, val in (('14.14', 10 * S(45) / S(30)), ('7.07', 10 * S(30) / S(45)), ('19.32', 10 * S(105) / S(30))):
    ok(abs(float(txt) - val) < 0.006, f'A l5 trap option {txt} vs {val:.4f}')
for txt, val in (('14.72', 12 * S(70) / S(50)), ('9.78', 12 * S(50) / S(70)), ('13.57', 12 * S(60) / S(50))):
    ok(abs(float(txt) - val) < 0.006, f'A l5 quiz[1] option {txt} vs {val:.4f}')
pts = {p['id']: (p['x'], p['y']) for p in node(L, 'screens[7]')['canvas']['state']['points']}
ok(abs(pts['A'][0] - 12 * S(70)) < 1e-6 and abs(pts['A'][1] - 12 * C(70)) < 1e-6, 'A l5 ship is not on bearing 070 at 12 km')
ok(abs(pts['L'][0] - 9 * S(130)) < 1e-6 and abs(pts['L'][1] - 9 * C(130)) < 1e-6, 'A l5 lighthouse is not on bearing 130 at 9 km')
pts = {p['id']: (p['x'], p['y']) for p in node(L, 'screens[8]')['canvas']['state']['points']}
A_, B_, C_ = pts['A'], pts['B'], pts['C']
ang = lambda p, q, r: math.degrees(math.acos(((q[0] - p[0]) * (r[0] - p[0]) + (q[1] - p[1]) * (r[1] - p[1])) / (math.dist(p, q) * math.dist(p, r))))
ok(abs(ang(A_, B_, C_) - 30) < 0.01 and abs(ang(C_, A_, B_) - 45) < 0.01 and abs(math.dist(B_, C_) - 10) < 0.001, 'A l5 trap drawing is not A=30, C=45, BC=10')
pts = {p['id']: (p['x'], p['y']) for p in node(L, 'screens[5]')['canvas']['state']['points']}
ok(abs(ang(pts['A'], pts['B'], pts['C']) - 40) < 0.01 and abs(ang(pts['B'], pts['A'], pts['C']) - 65) < 0.01 and abs(math.dist(pts['A'], pts['C']) - 10) < 0.001, 'A l5 sine-rule drawing')

L = 'review-1'
chk(L, 'items[0]', math.hypot(9, 12), {'added': 21, 'no-root': 225, 'subtracted': sq(144 - 81)})
chk(L, 'items[2]', 39 * 5 / 13, {'added': 5 + 26, 'ground': 36, 'tan': 39 * 5 / 12})
chk(L, 'items[3]', 40 * T(28), {'sine': 40 * S(28), 'divided': 40 / T(28)}, given=40 * 0.5317)
big = lambda a, b, c: aC((a * a + b * b - c * c) / (2 * a * b))
chk(L, 'items[5]', big(7, 8, 9), {'opp8': big(7, 9, 8), 'opp7': big(8, 9, 7), 'ratio': 32 / 112})
chk(L, 'items[6]', aT(12 / 5), {'flipped': aT(5 / 12), 'gradient': 2.4, 'length': 13})
chk(L, 'items[8]', 10 * S(50) / S(70), {'pairing': 10 * S(60) / S(70), 'pyth': 10})
pts = {p['id']: (p['x'], p['y']) for p in node(L, 'items[8]')['canvas']['state']['points']}
bearing = lambda p, q: math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])) % 360
ok(abs(bearing(pts['A'], pts['L']) - 30) < 0.01 and abs(bearing(pts['B'], pts['L']) - 320) < 0.01, 'A review-1 lighthouse bearings 030 and 320')

L = 'homework-1'
chk(L, 'items[0]', math.hypot(60, 34), {'added': 94, 'no-root': 4756, 'subtracted': sq(3600 - 1156)})
chk(L, 'items[2]', aT(0.35), {'flipped': 90 - aT(0.35), 'sine': aS(0.35), 'gradient': 0.35})
th = math.atan(0.25)
chk(L, 'items[3]', 2 * math.cos(th), {'vertical': 2, 'sine': 2 * math.sin(th), 'divided': 2 / math.cos(th)})
ok(abs(2 * math.cos(th) - 2 / sq(1 + 0.0625)) < 1e-12, 'A hw1 channel: 2/sqrt(1+0.25^2)')
chk(L, 'items[6]', math.hypot(5, 8), {'added': 13, 'no-root': 89, 'sixty': cosr(5, 8, 60)})
# drone: walk the two legs as vectors
p1 = (5 * S(60), 5 * C(60)); p2 = (p1[0] + 8 * S(150), p1[1] + 8 * C(150))
ok(abs(math.hypot(*p2) - 9.43) < 0.005, 'A hw1 drone by vectors')
chk(L, 'items[7]', 20 / (sq(3) - 1), {'one-triangle': 20, 'tan30': 20 * T(30), 'sixty': 20 * sq(3)})
h = 20 / (sq(3) - 1)
ok(abs(aT(h / h) - 45) < 1e-9 and abs(aT(h / (h + 20)) - 30) < 1e-9, 'A hw1 two elevations check')
for txt, val in (('3.91', 4 * 0.9781), ('0.83', 4 * 0.2079), ('4.09', 4 / 0.9781), ('0.85', 4 * 0.2126)):
    ok(abs(float(txt) - val) < 0.006, f'A hw1 ramp option {txt} vs {val:.4f}')
m = node(L, 'items[8]')['model']
s60 = sq(.25 ** 2 + .2 ** 2 - 2 * .25 * .2 * C(120)); s90 = math.hypot(.25, .2)
ok('0.3905' in m and abs(s60 - 0.3905) < 5e-5 and '0.3202' in m and abs(s90 - 0.3202) < 5e-5, 'A hw1 longform (b), (c)')
Cc = aC((.25 ** 2 + .2 ** 2 - .3 ** 2) / (2 * .25 * .2))
ok('82.82' in m and abs(Cc - 82.82) < 0.005 and '97.18' in m and abs(180 - Cc - 97.18) < 0.005, 'A hw1 longform (d)')

L = 'problems-1'
chk(L, 'items[0].parts[0]', math.hypot(12, 35), {'added': 47, 'used-14': math.hypot(14, 35), 'subtracted': sq(35 ** 2 - 12 ** 2)})
chk(L, 'items[0].parts[1]', 12 / 37, {'tan': 12 / 35, 'cos': 35 / 37, 'flipped': 37 / 12})
chk(L, 'items[0].parts[2]', 20 * 12 / 37, {'cos': 20 * 35 / 37, 'tan': 20 * 12 / 35, 'height': 14 - 20 * 12 / 37}, given=20 * 0.324)
chk(L, 'items[0].parts[3]', 20 * 35 / 37, {'subtracted': 20 - 6.49, 'added': math.hypot(20, 20 * 12 / 37)}, given=sq(400 - 6.49 ** 2))
chk(L, 'items[1].parts[2]', (8 * sq(3)) ** 2 + 64, {'root-as-three': 24 + 64, 'root-left': 64 * sq(3) + 64, 'cd-unsquared': 192 + 8})
chk(L, 'items[1].parts[3]', aS(8 / 16), {'angle-d': 60, 'tan': aT(.5), 'half': .5, 'radians': math.asin(.5), 'radians-whole': round(math.asin(.5))})
# hexagon by coordinates
hexp = [(8 * C(60 * k), 8 * S(60 * k)) for k in range(6)]
Ah, Bh, Ch, Dh = hexp[0], hexp[1], hexp[2], hexp[3]
ok(abs(math.dist(Ah, Ch) - 8 * sq(3)) < 1e-9 and abs(math.dist(Ah, Dh) - 16) < 1e-9 and abs(ang(Ah, Ch, Dh) - 30) < 1e-9 and abs(ang(Ch, Ah, Dh) - 90) < 1e-9, 'A problems-1 hexagon by coordinates')
AB = cosr(60, 45, 55)
chk(L, 'items[2].parts[1]', AB, {'no-root': 5625 - 5400 * 0.5736, 'plus': sq(5625 + 5400 * 0.5736), 'pythagoras': 75}, given=sq(5625 - 5400 * 0.5736))
Aang = aS(45 * S(55) / AB)
chk(L, 'items[2].parts[2]', Aang, {'wrong-side': aS(60 * 0.8192 / 50.27), 'ratio': 45 * .8192 / 50.27, 'radians': math.asin(45 * .8192 / 50.27)}, given=aS(45 * .8192 / 50.27))
ok(abs(big(60, AB, 45) - Aang) < 1e-6, 'A problems-1 lake: the sine-rule angle at A is the real (acute) angle')
chk(L, 'items[2].parts[3]', 60 * S(Aang), {'cos': 60 * C(47.2), 'used-45': 45 * S(47.2), 'tan': 60 * T(47.2)}, given=60 * S(47.2))
chk(L, 'items[3].parts[1]', 50, {'added': 70, 'subtracted': sq(1600 - 900)})
chk(L, 'items[3].parts[2]', aT(.75), {'flipped': aT(4 / 3), 'sine': aS(.75), 'ratio-tan': .75, 'ratio-sin': .6, 'radians': math.atan(.75)})
Bx, By = 40 * C(60) + 30 * C(-30), 40 * S(60) + 30 * S(-30)
chk(L, 'items[3].parts[3]', By, {'angle-aob': 50 * S(36.9), 'sixty': 50 * S(60), 'cos': 50 * C(23.1), 'added': 50 * S(96.9)}, given=50 * S(23.1))
ok(abs(By - (20 * sq(3) - 15)) < 1e-12 and abs(math.hypot(Bx, By) - 50) < 1e-12, 'A problems-1 lamp exact height')

L = 'l6-beyond-90'
chk(L, 'screens[4]', S(225), {'no-sign': -S(225), 'zero': 0})
chk(L, 'screens[10]', 10000 * C(135), {'no-sign': -10000 * C(135), 'degrees': 10000 * math.cos(135)})
ok(abs(C(120) + .5) < 1e-12 and abs(S(120) - .87) < .005 and abs(C(300) - .5) < 1e-12 and abs(S(300) + .87) < .005 and abs(C(150) + .87) < .005, 'A l6 values')
for a in np.linspace(0, 90, 181):
    ok(abs(S(180 - a) - S(a)) < 1e-12 and abs(C(180 - a) + C(a)) < 1e-12, 'A l6 mirror identities')

L = 'l7-arc-length'
chk(L, 'screens[0]', pi / 2, {'deg': 90, 'whole': 2 * pi, 'half': pi, 'radius': 1, 'fraction': .25})
chk(L, 'screens[5]', math.degrees(2), {'wrong-way': rad(2), 'two-pi': 360, 'sixty': 120})
chk(L, 'screens[10]', 2 * pi / 12, {'degrees': 30, 'turns': 1 / 12, 'times': 24 * pi})
chk(L, 'quiz[1]', math.degrees(3), {'wrong-way': rad(3), 'pi-180': 540})
chk(L, 'quiz[2]', 2 * pi / 3, {'degrees': 2 * 60, 'no-r': pi / 3})
ok(abs(math.degrees(1) - 57.3) < .05 and abs(math.degrees(6) - 343.8) < .05 and abs(2 * pi - 6 - .28) < .005 and abs(360 / (2 * pi) - 57.3) < .05, 'A l7 radian facts')
ok(abs(2 * math.sin(rad(60) / 2) - 1) < 1e-12, 'A l7: at 60 degrees the chord equals the radius')

L = 'l8-unrolling'
chk(L, 'screens[4]', math.sin(13 * pi / 6), {'neg': -.5, 'zero': 0, 'cos': math.cos(pi / 6)})
chk(L, 'screens[5]', pi / 2, {'pi': pi, 'one': 1})
xs = np.linspace(0, 2 * pi, 2001)
ok(np.max(np.abs(np.sin(xs + pi / 2) - np.cos(xs))) < 1e-12, 'A l8 sin(x + pi/2) = cos x')
tt = np.linspace(0, 12, 12001)
chk(L, 'screens[9]', float(tt[np.argmin(100 + 30 * np.sin(pi * tt / 6))]), {'half': 6, 'peak': float(tt[np.argmax(100 + 30 * np.sin(pi * tt / 6))]), 'radians': 3 * pi / 2})
chk(L, 'quiz[2]', math.sin(5 * pi / 2), {'zero': 0, 'neg': -1})
ok(abs(math.cos(2) + .42) < .005 and abs(math.sin(2) - .91) < .005, 'A l8 trap values')

L = 'l9-stretching-a-wave'
def is_period(f, p):
    """p is the smallest positive period of f: f repeats after p and after no p/k, k = 2..8."""
    x = np.linspace(-20, 20, 4001)
    rep = lambda q: np.max(np.abs(f(x + q) - f(x))) < 1e-9
    return rep(p) and not any(rep(p / k) for k in range(2, 9))
ok(is_period(lambda x: 2 * np.sin(2 * x), pi), 'A l9 period of 2 sin 2x')
ok(is_period(lambda x: np.sin(3 * x), 2 * pi / 3), 'A l9 period of sin 3x')
ok(is_period(lambda x: np.sin(x / 2), 4 * pi), 'A l9 period of sin(x/2)')
ok(is_period(lambda x: 4 * np.sin(pi * x / 6) + 10, 12), 'A l9 period 12')
ok(is_period(lambda x: np.sin(x / 4), 8 * pi), 'A l9 b = 1/4 gives 8 pi')
ok(is_period(np.sin, 2 * pi) and is_period(np.cos, 2 * pi) and is_period(np.tan, pi), 'A periods of sin, cos, tan')
ok(is_period(lambda x: 3 * np.sin(4 * x), pi / 2) and is_period(lambda x: np.sin(pi * x / 5), 10) and is_period(lambda x: np.sin(pi * x / 3), 6), 'A other periods used')
chk(L, 'screens[3]', 2 * pi / (pi / 2), {'inverted': .25, 'two': 2})
chk(L, 'screens[4]', 4 - 1.5, {'no-shift': -1.5, 'midline': 4, 'max': 5.5, 'double': 1})
chk(L, 'screens[5]', 5 * pi / 6 - pi / 2, {'wrong-way': -(5 * pi / 6 - pi / 2), 'peak': 5 * pi / 6})
t2 = np.linspace(0, 12, 12001)
lag = t2[np.argmax(100 + 8 * np.sin(pi * (t2 - 2) / 6))] - t2[np.argmax(100 + 20 * np.sin(pi * t2 / 6))]
chk(L, 'screens[9]', float(lag), {'lead': 12 - float(lag), 'radians': pi / 3, 'period': 12})
chk(L, 'quiz[2]', float(np.max(2 * np.sin(3 * xs) + 5)), {'amp-only': 2, 'b': 8, 'mid': 5})

L = 'review-2'
chk(L, 'items[3]', 2 * pi / 4, {'stretch': 8 * pi, 'keep': 2 * pi, 'amp': 2 * pi / 3})
chk(L, 'items[5]', 5 * rad(72), {'degrees': 360, 'no-r': rad(72)})
chk(L, 'items[6]', math.cos(7 * pi / 6), {'no-sign': -math.cos(7 * pi / 6), 'sin': math.sin(7 * pi / 6)})
chk(L, 'items[8]', 2 * pi / 5, {'degrees': 72, 'turns': .2, 'times': 10 * pi})
ok(np.max(np.abs(np.sin(xs + pi) + np.sin(xs))) < 1e-12, 'A review-2 sin(x + pi) = -sin x')

L = 'homework-2'
chk(L, 'items[1]', math.degrees(2.5), {'wrong-way': rad(2.5), 'pi-180': 450})
chk(L, 'items[3]', -sq(1 - .36), {'no-sign': .8, 'subtract': -.4, 'square': .64})
chk(L, 'items[5]', 3.2 + .4 * math.sin(7 * pi / 6), {'no-sign': 3.4, 'degrees': 3.2 + .4 * S(7 * pi / 6), 'mid': 3.2})
chk(L, 'items[6]', 2 * pi * 3 / 20, {'days': 3, 'degrees': 54, 'no-2pi': .15})
chk(L, 'items[7]', 10 * C(200) - 10 * C(30), {'no-sign': 9.40 - 8.66, 'sine': 10 * S(200) - 10 * S(30), 'reversed': 10 * C(30) - 10 * C(200)})
mm = np.linspace(0, 12, 12001)
cfit = [c for c in np.arange(0, 12, .5) if abs(mm[np.argmax(120 + 60 * np.sin(pi * (mm - c) / 6))] - 4) < 1e-6]
chk(L, 'items[8]', cfit[0], {'peak-month': 4, 'sign': 7})
ok(cfit == [1.0], f'A hw2 fit phase: c in [0, 12) is not unique: {cfit}')
m = node(L, 'items[9]')['model']
R = lambda t: 60000 + 24000 * math.sin(pi * (t - 2) / 6)
ok(abs(R(5) - 84000) < 1e-6 and abs(R(11) - 36000) < 1e-6 and abs(R(3) - 72000) < 1e-6 and '72000' in m, 'A hw2 longform model')

L = 'problems-2'
chk(L, 'items[0].parts[0]', 5.4 / 2.4, {'times': 5.4 * 2.4, 'flipped': 2.4 / 5.4, 'turns': 5.4 / (2 * pi * 2.4)})
chk(L, 'items[0].parts[1]', math.degrees(2.25), {'wrong-way': rad(2.25), 'no-pi': 2.25 * 180})
chk(L, 'items[0].parts[2]', 3 + 2.4 * math.sin(2.25), {'radian-mode': 3 + 2.4 * math.sin(128.9), 'degree-mode': 3 + 2.4 * S(2.25), 'cos': 3 + 2.4 * math.cos(2.25), 'no-hub': 2.4 * S(128.9)}, given=3 + 2.4 * S(128.9))
chk(L, 'items[0].parts[3]', 180 - math.degrees(2.25), {'cos-mirror': 360 - 128.9, 'half-turn': 128.9 + 180, 'minus-90': 128.9 - 90}, given=180 - 128.9)
chk(L, 'items[0].parts[4]', 2.4 * (pi - 2.25), {'degrees': 2.4 * 51.1, 'divided': 51.1 / 2.4, 'between': 5.4 - 2.14}, given=2.4 * rad(51.1))
chk(L, 'items[1].parts[0]', 2 * pi / (pi / 5), {'read-five': 5, 'b-itself': pi / 5, 'times': 2 * pi * pi / 5})
ts = np.linspace(0, 10, 100001)
h1 = lambda t: 6 + .8 * np.sin(pi * t / 5); h2 = lambda t: 6 + .8 * np.sin(pi * (t - 3) / 5)
chk(L, 'items[1].parts[1]', float(ts[np.argmax(h1(ts))]), {'angle': pi / 2, 'half': 5, 'trough': float(ts[np.argmin(h1(ts))])})
chk(L, 'items[1].parts[2]', float(ts[np.argmax(h2(ts))]), {'early': -.5, 'lag': 3})
chk(L, 'items[1].parts[3]', float(h2(5.5) - h1(5.5)), {'height': float(h1(5.5)), 'degree-mode': 6.8 - (6 + .8 * S(1.1 * pi)), 'full-swing': 1.6})
hw = lambda t: 25 * math.sin(pi / 10 * (t - 5)) + 28
ok(abs(hw(0) - 3) < 1e-9 and abs(hw(10) - 53) < 1e-9 and abs(hw(5) - 28) < 1e-9 and hw(5.1) > 28, 'A problems-2 wheel model: bottom at 0, top at 10, rising at 5')
chk(L, 'items[2].parts[0]', 25, {'diameter': 50, 'top': 53, 'hub': 28})
chk(L, 'items[2].parts[2]', 5, {'boarding': 0, 'top': 10, 'falling': 15})
chk(L, 'items[2].parts[3]', hw(8), {'degree-mode': 25 * S(.3 * pi) + 28, 'no-shift': 25 * math.sin(.8 * pi) + 28})
others = [t for t in range(0, 21) if t != 8 and abs(hw(t) - hw(8)) < 1e-9]
chk(L, 'items[2].parts[4]', others[0], {'no-shift': 7, 'half-period': 18, 'mirror-start': 2})
ok(others == [12], f'A problems-2 wheel: other times at the same height {others}')

L = 'l10-identity-from-circle'
chk(L, 'screens[0]', sq(1 - .36), {'sub': .4, 'noroot': .64})
chk(L, 'screens[2]', sq(1 - .28 ** 2), {'sub': .72, 'noroot': 1 - .28 ** 2})
chk(L, 'screens[3]', -sq(1 - .36), {'pos': .8, 'sub': -.4, 'subpos': .4})
chk(L, 'screens[4]', .8 / .6, {'flip': .6 / .8, 'prod': .48})
chk(L, 'screens[9]', 10000 * sq(1 - .36), {'sub': 4000, 'noroot': 6400, 'neg': -8000})
ok(abs(S(45) + C(45) - 1.41) < .005 and abs(S(120) + C(120) - .37) < .005 and abs(1 - C(120) - 1.5) < 1e-9, 'A l10 generalise counterexamples')
ok(abs(C(36.87) - .8) < 1e-4 and abs(S(16.26) - .28) < 1e-4 and abs(S(143.13) - .6) < 1e-4 and abs(C(53.13) - .6) < 1e-4 and abs(C(126.87) + .6) < 1e-4, 'A l10 canvas angles')

L = 'l11-every-angle'
chk(L, 'screens[1]', aS(.8) + (180 - aS(.8)), {'period': 360, 'quarter': 90})
chk(L, 'screens[2]', 180 - aS(.8), {'plus': 180 + aS(.8), 'cosrule': 360 - aS(.8), 'same': aS(.8)})
chk(L, 'screens[6]', 45 + 180, {'sinrule': 135, 'cosrule': 315})
chk(L, 'screens[11]', 6 / pi * (pi / 4 + pi), {'first': 1.5, 'sinrule': 6 / pi * (3 * pi / 4), 'cosrule': 6 / pi * (7 * pi / 4)})

L = 'l12-adding-angles'
c45, c30, s30 = .7071, .8660, .5
chk(L, 'screens[2]', C(15), {'split': c45 - c30, 'minus': c45 * c30 - c45 * s30}, given=c45 * c30 + c45 * s30)
chk(L, 'screens[3]', S(75), {'split': c45 + s30, 'minus': c45 * c30 - c45 * s30}, given=c45 * c30 + c45 * s30)
chk(L, 'screens[4]', C(75), {'plus': c45 * c30 + c45 * s30, 'split': c45 + c30, 'first': c45 * c30}, given=c45 * c30 - c45 * s30)
chk(L, 'screens[5]', .5 * S(50), {'half': .25 * S(50), 'theta': .5 * S(25), 'nohalf': S(50)})
chk(L, 'screens[6]', S(120), {'double': 2 * S(60), 'cos': C(120), 'neg': -S(120)})
u, v = np.array([4., 3.]), np.array([1., 2.])
cosuv = float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))
a_, b_ = math.atan2(3, 4), math.atan2(2, 1)
chk(L, 'screens[9]', cosuv, {'dot': float(u @ v), 'sine': math.sin(b_ - a_), 'plus': math.cos(b_ + a_)}, given=.8 * .4472 + .6 * .8944)
ok(abs(math.degrees(b_ - a_) - 26.6) < .05, 'A l12 tilts 26.6 degrees apart')
for txt, val in (('-0.2588', C(105)), ('0.9659', .5 * c45 + c30 * c45), ('1.2071', .5 + c45), ('0.2588', c30 * c45 - .5 * c45)):
    ok(abs(float(txt) - val) < 6e-4, f'A l12 quiz[0] option {txt} vs {val:.4f}')
ok(abs(2 * .6 * .8 - .96) < 1e-12 and abs(.64 - .36 - .28) < 1e-12 and abs(2 * .36 - 1 + .28) < 1e-12, 'A l12 quiz double angles')

L = 'l13-modelling-a-cycle'
D = lambda t: 200 * math.sin(pi / 6 * (t - 10)) + 500
dots = node(L, 'screens[0]')['canvas']['state']['points']
ys = [p['y'] for p in dots]
chk(L, 'screens[0]', (max(ys) + min(ys)) / 2, {'sum': 1000, 'peak': 700, 'trough': 300})
res = [p['y'] - D(p['x']) for p in dots]
ok(max(abs(r) for r in res) < 30, f'A l13 gas model misses a dot by {max(abs(r) for r in res):.1f} GWh')
# least-squares fit of a + b sin + c cos at period 12 recovers amplitude, midline and shift
X = np.array([[1, math.sin(pi * p['x'] / 6), math.cos(pi * p['x'] / 6)] for p in dots]); yv = np.array(ys, float)
co = np.linalg.lstsq(X, yv, rcond=None)[0]
amp = math.hypot(co[1], co[2]); shift = (-math.atan2(co[2], co[1]) * 6 / pi) % 12
ok(abs(co[0] - 500) < 10 and abs(amp - 200) < 10 and abs(shift - 10) < .25, f'A l13 least squares gives d={co[0]:.1f}, a={amp:.1f}, c={shift:.2f}')
for cwrong in (1, 4, 7):
    Dw = lambda t: 200 * math.sin(pi / 6 * (t - cwrong)) + 500
    ok(max(abs(p['y'] - Dw(p['x'])) for p in dots) > 150, f'A l13 option c={cwrong} would also fit')
ok(max(abs(p['y'] - (200 * math.sin(pi / 6 * (p['x'] + 2)) + 500)) for p in dots) < 30, 'A l13 c = -2 fits too')
chk(L, 'screens[2]', D(3), {'sign': 400, 'deg': 200 * S(pi / 6 * (3 - 10)) + 500})
chk(L, 'screens[3]', 2 * pi / 6, {'period': 6, 'year': pi / 6, 'deg': 60})
pw = node(L, 'screens[3]')['canvas']['state']['points']
Pw = lambda t: 80 * math.sin(pi / 3 * (t - 5.5)) + 300
ok(max(abs(p['y'] - Pw(p['x'])) for p in pw) < 20, 'A l13 power model misses a dot')
ok(max(abs(a['y'] - b['y']) for a, b in zip(pw[:6], pw[6:])) < 15, 'A l13 power data repeat every 6 months')
chk(L, 'screens[4]', 80, {'peak': 380, 'range': 160, 'mid': 300})
tg = np.linspace(1, 13, 120001)
first = float(tg[np.argmax((200 * np.sin(pi / 6 * (tg - 10)) + 500 <= 400))])
chk(L, 'screens[5]', first, {'principal': 9, 'trough': 7, 'nosign': 11})
tg = np.linspace(0, 12, 1200001)
above = float(np.mean(120 * np.sin(pi / 6 * (tg - 9)) + 400 > 460) * 12)
chk(L, 'screens[8]', above, {'two': 2, 'six': float(np.mean(120 * np.sin(pi / 6 * (tg - 9)) + 400 > 400) * 12), 'eight': 12 - above})
ok(abs(D(11) - 600) < 1e-9 and abs(D(15) - 600) < 1e-9 and D(13) > 600, 'A l13 derive: above 600 from 11 to 15')

L = 'review-3'
chk(L, 'items[0]', -sq(1 - .36), {'pos': .8, 'sub': -.4, 'noroot': -.64})
chk(L, 'items[2]', S(15), {'plus': c45 * c30 + c45 * s30, 'split': c45 - s30}, given=c45 * c30 - c45 * s30)
th = math.atan2(.6, -.8)
ok(abs(math.tan(th) + .75) < 1e-12, 'A review-3 tan = -0.75 in the second quadrant')
chk(L, 'items[4]', math.cos(th), {'pos': .8, 'sine': math.sin(th), 'tan': -.75})
Aob = 180 - aS(.8)
chk(L, 'items[6]', S(2 * Aob), {'pos': .96, 'double': 1.6})
chk(L, 'items[7]', .5 * 6 * 9 * S(150), {'nohalf': 27, 'cos': .5 * 54 * C(150), 'cosabs': -.5 * 54 * C(150)})
tg = np.linspace(0, 12, 1200001)
Pm = 3 * np.sin(pi / 6 * (tg - 1)) + 20
chk(L, 'items[8]', float(tg[np.argmax(Pm >= 21.5 - 1e-9)]), {'second': 6, 'noshift': 1, 'deg': 1 + 30 * 6 / pi})

L = 'homework-3'
u, v = np.array([3., 4.]), np.array([5., -12.])
cs = float(u @ v / (5 * 13))
chk(L, 'items[4]', aC(cs), {'acute': aC(-cs), 'dot': cs})
tg = np.linspace(0, 12, 1200001)[:-1]
dif = 3 * np.sin(pi * tg / 6) - 3 * np.sin(pi / 6 * (tg - 4))
cross = tg[np.where(np.sign(dif[:-1]) * np.sign(dif[1:]) < 0)[0]]
cross = np.array(sorted(set(np.round(np.concatenate([cross, tg[np.abs(dif) < 1e-9]]), 3))))
ok(len(cross) == 2 and abs(cross[0] - 5) < 1e-3 and abs(cross[1] - 11) < 1e-3, f'A hw3 crossings {cross}')
chk(L, 'items[5]', float(cross[-1]), {'first': float(cross[0]), 'twelve': 17, 'half': 8})
chk(L, 'items[7]', 63 / 65, {'split': 3 / 5 + 12 / 13, 'cos': 20 / 65 - 36 / 65, 'minus': 15 / 65 - 48 / 65})
chk(L, 'items[8]', 10 * math.cos(math.atan(.5)), {'linear': 10 * 2 / 3, 'b': 10 * math.sin(math.atan(.5)), 'tan': 5})
Dm = lambda t: 220 * math.sin(pi / 6 * (t - 11)) + 600
ok(abs(Dm(2) - 820) < 1e-9 and abs(Dm(8) - 380) < 1e-9 and abs(Dm(5) - 600) < 1e-9 and Dm(5.1) < 600 and abs(Dm(12) - 710) < 1e-9 and abs(Dm(16) - 710) < 1e-9 and Dm(14) > 710, 'A hw3 longform model')
ok(all(abs((220 * math.sin(pi / 6 * (t - 5)) + 600) - (1200 - Dm(t))) < 1e-9 for t in range(13)), 'A hw3 longform (d): c = 5 gives 1200 - D')

L = 'problems-3'
sA, cA, cB, sB = 28 / 53, -45 / 53, 24 / 25, 7 / 25
chk(L, 'items[0].parts[0]', cA, {'sign': -cA, 'one-minus': 1 - sA, 'no-root': 1 - sA ** 2})
chk(L, 'items[0].parts[1]', sB, {'negative': -sB, 'one-minus': 1 - cB, 'no-root': 1 - cB ** 2})
Aa, Bb = 180 - aS(sA), aC(cB)
chk(L, 'items[0].parts[2]', S(Aa + Bb), {'sign': sA * cB - cA * sB, 'sum-of-sines': sA + sB, 'cos-formula': C(Aa + Bb)})
chk(L, 'items[0].parts[3]', C(Aa + Bb), {'plus': cA * cB + sA * sB, 'sign': -cA * cB - sA * sB, 'sign2': -C(Aa + Bb)})
chk(L, 'items[0].parts[4]', Aa + Bb, {'principal': aS(.2694), 'third': 180 + aS(.2694), 'fourth': 360 - aS(.2694)})
chk(L, 'items[1].parts[1]', list(np.roots([2, -3, 1])), {'signs': list(np.roots([2, 3, 1])), 'carried': list(np.roots([1, -3, 2]))})
chk(L, 'items[2].parts[0]', (17.6 - 6.4) / 2, {'range': 11.2, 'longest': 17.6, 'midline': 12})
Lm = lambda t: 5.6 * np.sin(pi / 6 * (t - 3)) + 12
ok(abs(Lm(6) - 17.6) < 1e-9 and abs(Lm(12) - 6.4) < 1e-9, 'A problems-3 daylight model peak and trough')
chk(L, 'items[2].parts[2]', 3, {'peak': 6, 'falling': 9, 'trough': 12})
tg = np.linspace(0, 12, 1200001)
d10 = Lm(tg) - 10
cr = tg[np.where(np.sign(d10[:-1]) != np.sign(d10[1:]))[0]]
chk(L, 'items[2].parts[3]', [float(x) for x in cr], {'no-shift': [6.7, 11.3], 'above': [3.7, 8.3]})
chk(L, 'items[2].parts[4]', float(np.mean(Lm(tg) > 10) * 12), {'outside': float(np.mean(Lm(tg) < 10) * 12), 'whole-months': 8})
chk(L, 'items[3].parts[1]', [aS(25 / 65), 180 - aS(25 / 65)], {'no-half': [aS(25 / 130), 180 - aS(25 / 130)], 'cos-rule': [22.62, 337.38]})
chk(L, 'items[3].parts[2]', C(180 - aS(5 / 13)), {'sign': 12 / 13, 'one-minus': 1 - 5 / 13, 'no-root': -144 / 169})
chk(L, 'items[3].parts[3]', cosr(10, 13, 180 - aS(5 / 13)), {'sign': sq(29), 'pythagoras': sq(269), 'no-root': 509, 'no-two': sq(269 + 120)})

# ---------------------------------------------------------------- B: equation solution sets
def roots(f, lo, hi, n=720001):
    """All x in [lo, hi] with f(x) = 0, in degrees: sign changes plus tangencies."""
    x = np.linspace(lo, hi, n); y = f(x)
    out = set()
    i = np.where(np.abs(y) < 1e-7)[0]
    out |= {round(float(v), 2) for v in x[i]}
    j = np.where((np.sign(y[:-1]) * np.sign(y[1:]) < 0) & (np.abs(y[:-1] - y[1:]) < 1))[0]
    out |= {round(float((x[k] + x[k + 1]) / 2), 2) for k in j}
    res = sorted(out)
    merged = []
    for r in res:
        if not merged or r - merged[-1] > 0.1:
            merged.append(r)
    return merged

sind = lambda x: np.sin(np.radians(x)); cosd = lambda x: np.cos(np.radians(x)); tand = lambda x: np.tan(np.radians(x))
def same(a, b, tol=0.02):
    return len(a) == len(b) and all(abs(p - q) <= tol for p, q in zip(sorted(a), sorted(b)))

ok(same(roots(lambda x: sind(x) - .5, 0, 360), [30, 150]), 'B sin x = 0.5 on 0..360')
ok(same(roots(lambda x: sind(x) + .5, 0, 360), [210, 330]), 'B sin x = -0.5 on 0..360')
ok(same(roots(lambda x: sind(x) - .5, 0, 720), [30, 150, 390, 510]), 'B sin x = 0.5 on 0..720')
ok(same(roots(lambda x: cosd(x) - .5, 0, 360), [60, 300]), 'B cos x = 0.5')
ok(same(roots(lambda x: cosd(x) + .5, 0, 360), [120, 240]), 'B cos x = -0.5')
ok(same(roots(lambda x: tand(x) - 1, 0, 360), [45, 225]), 'B tan x = 1')
ok(same(roots(lambda x: tand(x) + 1, 0, 360), [135, 315]), 'B tan x = -1')
r = roots(lambda x: sind(2 * x) - .5, 0, 360)
ok(same(r, [15, 75, 195, 255]) and node('l11-every-angle', 'screens[7]')['widget']['answer'] == len(r), 'B sin 2x = 0.5 has four solutions')
ok(same(roots(lambda x: 2 * sind(x) ** 2 - sind(x) - 1, 0, 360), [90, 210, 330]), 'B 2 sin^2 x - sin x - 1 = 0')
r = roots(lambda x: sind(x) ** 2 - .25, 0, 360)
ok(same(r, [30, 150, 210, 330]), 'B sin^2 x = 0.25')
ok(roots(lambda x: sind(x) - 1.5, 0, 360) == [], 'B sin x = 1.5 has no solution')
ok(same(roots(lambda x: sind(x) + .8, 0, 360), [233.13, 306.87]), 'B sin x = -0.8')
r = roots(lambda x: 2 * cosd(x) ** 2 - cosd(x) - 1, 0, 360)
ok(same(r, [0, 120, 240, 360]) and node('review-3', 'items[5]')['widget']['answer'] == len(r), 'B 2 cos^2 x - cos x - 1 = 0 has four solutions on the closed interval')
ok(same(roots(lambda x: 2 * sind(x) ** 2 + 3 * sind(x) - 2, 0, 360), [30, 150]), 'B 2 sin^2 x + 3 sin x - 2 = 0')
r = roots(lambda x: tand(2 * x) - math.sqrt(3), 0, 360)
ok(same(r, [30, 120, 210, 300]) and node('homework-3', 'items[3]')['widget']['answer'] == len(r), 'B tan 2x = root 3')
r = roots(lambda x: 2 * cosd(x) ** 2 + 3 * sind(x) - 3, 0, 360)
ok(same(r, node('problems-3', 'items[1].parts[2]')['widget']['answers'], .05), f'B 2 cos^2 x + 3 sin x = 3: {r}')
ok(same(roots(lambda x: sind(x) - .5, 0, 360), [math.degrees(pi / 6), math.degrees(5 * pi / 6)]), 'B radians list')
# the three second-solution rules, over the whole range of k
for k in np.linspace(-0.99, 0.99, 199):
    x1 = aS(k); ok(same(roots(lambda x: sind(x) - k, 0, 360, 72001), sorted({round(v + 360 * n, 6) for v in (x1, 180 - x1) for n in (-1, 0, 1) if 0 <= v + 360 * n <= 360}), .05), f'B sine rule of thumb at k={k:.2f}')
    x1 = aC(k); ok(same(roots(lambda x: cosd(x) - k, 0, 360, 72001), sorted({x1, 360 - x1}), .05), f'B cosine rule of thumb at k={k:.2f}')
for k in np.linspace(-3, 3, 61):
    x1 = aT(k); want = sorted({v % 360 for v in (x1, x1 + 180)})
    got = [v for v in roots(lambda x: tand(x) - k, 0, 360, 720001) if abs(v - 360) > .05 or abs(k) < 1e-9]
    if abs(k) < 1e-9: want = [0, 180, 360]
    ok(same(got, want, .05), f'B tangent rule of thumb at k={k:.2f}: {got} vs {want}')
# multi and choice keys named in the content
def multi_key(name, path):
    return sorted(float(re.sub(r'[^0-9.\-−]', '', o['text']).replace('−', '-')) for o in node(name, path)['widget']['options'] if o.get('correct'))
ok(multi_key('l11-every-angle', 'screens[3]') == [210, 330], 'B l11 screens[3] multi key')
ok(multi_key('l11-every-angle', 'screens[4]') == [30, 150, 390, 510], 'B l11 screens[4] multi key')
ok(multi_key('l11-every-angle', 'screens[8]') == [90, 210, 330], 'B l11 screens[8] multi key')
ok(multi_key('homework-3', 'items[2]') == [30, 150], 'B hw3 multi key')
ok(multi_key('l10-identity-from-circle', 'screens[5]') == [90, 270], 'B l10 tangent undefined at 90 and 270')

# ---------------------------------------------------------------- C: fluency families, whole range
def fl_env():
    return dict(floor=math.floor, round=lambda v, n=0: float(Fraction(v).limit_denominator(10 ** 12)) if False else round(v + 0.0, n), sin=math.sin, cos=math.cos,
                tan=math.tan, sqrt=math.sqrt, pi=math.pi, gcd=math.gcd, abs=abs)

def grid(vars_):
    names, doms = [], []
    for k, v in vars_.items():
        names.append(k)
        if 'int' in v:
            lo, hi = v['int']; d = [x for x in range(lo, hi + 1, v.get('step', 1)) if x not in v.get('not', [])]
        else:
            d = v['pick']
        doms.append(d)
    for combo in itertools.product(*doms):
        yield dict(zip(names, combo))

def ev(expr, env):
    return eval(expr.replace('^', '**'), fl_env(), env)

def family(name, idx):
    fam = load(name)['families'][idx]
    for env in grid(fam['vars']):
        env = dict(env)
        for k, e in fam.get('let', {}).items():
            env[k] = ev(e, env)
        if all(ev(wh, env) for wh in fam.get('where', [])):
            yield fam, env

def tpl(s, env):
    """Value of a '{expr}' template (numeric)."""
    return ev(s.strip('{}'), env) if isinstance(s, str) else s

def polyval(s, env):
    """Numeric value of {poly(r; a, b)}: a*r + b with r the surd."""
    m = re.fullmatch(r'\{poly\(r; (.*), (.*)\)\}', s)
    r = math.sqrt(3) if '3' in env['r'] else math.sqrt(2)
    return ev(m.group(1), env) * r + ev(m.group(2), env)

cnt = {}
def sweep(name, idx, truth, wrongs, expr=False, tolk=None):
    n = 0
    for fam, env in family(name, idx):
        n += 1
        w = fam['widget']
        key = polyval(w['answer'], env) if expr else tpl(w['answer'], env)
        tol = 1e-9 if expr else (w['tol'].get('abs', None) if 'abs' in w['tol'] else abs(key) * w['tol']['rel'])
        t = truth(env)
        ok(abs(key - t) <= (tolk if tolk is not None else tol) + 1e-9, f"C {name} {fam['id']} {env}: key {key} vs truth {t}")
        vals = []
        for o in fam['wrong']:
            val = polyval(o['tex'], env) if expr else tpl(o['value'], env)
            wt = 1e-9 if expr else (o.get('tol', {'abs': 0}).get('abs', None) if 'abs' in o.get('tol', {'abs': 0}) else abs(val) * o['tol']['rel'])
            tw = wrongs[o['id']](env)
            ok(abs(val - tw) <= max(wt, 1e-6), f"C {name} {fam['id']} slip {o['id']} {env}: {val} vs mistake {tw}")
            ok(abs(val - key) > tol + wt, f"C {name} {fam['id']} slip {o['id']} {env}: collides with the key")
            vals.append((val, wt))
        for (v1, t1), (v2, t2) in itertools.combinations(vals, 2):
            ok(abs(v1 - v2) > max(t1, t2), f"C {name} {fam['id']} {env}: one slip's value sits in the other's band")
    cnt[(name, fam['id'])] = n
    ok(n > 0, f'C {name}[{idx}] has no cases')

F = 'fluency-l1-squares-on-sides'
sweep(F, 0, lambda e: math.hypot(e['a'], e['b']), {'forgot-the-root': lambda e: e['a'] ** 2 + e['b'] ** 2, 'added-the-sides': lambda e: e['a'] + e['b']})
sweep(F, 1, lambda e: math.sqrt(e['c'] ** 2 - e['a'] ** 2), {'added-the-squares': lambda e: math.hypot(e['c'], e['a']), 'took-away-sides': lambda e: e['c'] - e['a']})
for fam, e in itertools.chain(family(F, 0), family(F, 1)):
    ok(float(e['c']).is_integer() and e['a'] > 0 and e['b'] > 0 and e['c'] <= 100 and e['a'] ** 2 + e['b'] ** 2 == e['c'] ** 2, f'C fluency-l1 triple {e}')
sweep(F, 2, lambda e: math.hypot(e['a'], e['b']), {'forgot-the-root': lambda e: e['a'] ** 2 + e['b'] ** 2, 'added-the-sides': lambda e: e['a'] + e['b']})
sweep(F, 3, lambda e: math.sqrt(e['c'] ** 2 - e['a'] ** 2), {'added-the-squares': lambda e: math.hypot(e['c'], e['a']), 'forgot-the-root': lambda e: e['c'] ** 2 - e['a'] ** 2})
for fam, e in family(F, 3):
    ok(2 <= e['a'] < e['c'], f'C fluency-l1 short side {e}')

F = 'fluency-l3-sides-and-angles'
side = lambda e, opp: (math.sin if opp else math.cos)(rad(e['t']))
# slips are what a learner gets from the 4 dp ratios the prompt supplies; keys are checked against the true value
rside = lambda e, opp: e['sv'] if opp else e['cv']
sweep(F, 0, lambda e: e['h'] * side(e, e['w'] == 'opposite'),
      {'other-ratio': lambda e: e['h'] * rside(e, e['w'] != 'opposite'), 'divided-by-ratio': lambda e: e['h'] / rside(e, e['w'] == 'opposite')}, tolk=0.01)
sweep(F, 1, lambda e: e['d'] / side(e, e['w'] == 'opposite'),
      {'multiplied-by-ratio': lambda e: e['d'] * rside(e, e['w'] == 'opposite'), 'other-ratio': lambda e: e['d'] / rside(e, e['w'] != 'opposite')}, tolk=0.01)
sweep(F, 2, lambda e: e['a'] * math.tan(rad(e['t'])), {'used-sine': lambda e: e['a'] * e['sv'], 'divided-by-tan': lambda e: e['a'] / e['tv']}, tolk=0.02)
for i in (0, 1, 2):
    for fam, e in family(F, i):
        ok(abs(e['sv'] - math.sin(rad(e['t']))) <= 5.0001e-5 and abs(e['cv'] - math.cos(rad(e['t']))) <= 5.0001e-5, f'C fluency-l3 stated ratio wrong {e}')
# the 2 dp answer from the stated 4 dp ratio is always accepted, and so is the 2 dp true value
for i, wtol in ((0, .01), (1, .01), (2, .02)):
    for fam, e in family(F, i):
        key = tpl(fam['widget']['answer'], e)
        true = {0: lambda: e['h'] * side(e, e['w'] == 'opposite'), 1: lambda: e['d'] / side(e, e['w'] == 'opposite'), 2: lambda: e['a'] * math.tan(rad(e['t']))}[i]()
        ok(abs(round(true, 2) - key) <= wtol + 1e-9, f'C fluency-l3[{i}] {e}: the true 2 dp value {round(true, 2)} is refused (key {key})')

F = 'fluency-l4-exact-values'
sweep(F, 0, lambda e: e['h'] * side(e, e['w'] == 'opposite'),
      {'other-ratio': lambda e: e['h'] * side(e, e['w'] != 'opposite'), 'divided-by-ratio': lambda e: e['h'] / side(e, e['w'] == 'opposite')}, expr=True)
sweep(F, 1, lambda e: e['a'] * math.tan(rad(e['t'])), {'used-sine': lambda e: e['a'] * math.sin(rad(e['t'])), 'divided-by-tan': lambda e: e['a'] / math.tan(rad(e['t']))}, expr=True)
hyp45 = lambda e: e['c'] * (math.sqrt(2) if e['e'] == 1 else 1)
sweep(F, 2, lambda e: hyp45(e) / math.sqrt(2), {'halved': lambda e: hyp45(e) / 2, 'times-root-two': lambda e: hyp45(e) * math.sqrt(2)}, expr=True)
sweep(F, 3, lambda e: e['a'] * math.sin(rad(e['t'])) + e['b'] * math.cos(rad(e['t'])),
      {'swapped-values': lambda e: e['a'] * math.cos(rad(e['t'])) + e['b'] * math.sin(rad(e['t'])),
       'dropped-halves': lambda e: 2 * (e['a'] * math.sin(rad(e['t'])) + e['b'] * math.cos(rad(e['t'])))}, expr=True)

F = 'fluency-l7-arc-length'
sweep(F, 0, lambda e: e['d'] / 180, {'upside-down': lambda e: 180 / e['d'], 'used-a-full-turn': lambda e: e['d'] / 360})
for fam, e in family(F, 1):
    ok(abs(e['p'] / e['q'] * pi - rad(e['d'])) < 1e-12 and math.gcd(int(e['p']), int(e['q'])) == 1 and e['flip'] != e['k'] and e['turn'] != e['k'], f'C fluency-l7 exact {e}')
sweep(F, 2, lambda e: math.degrees(e['p'] * pi / e['q']), {'used-a-full-turn': lambda e: 360 * e['p'] / e['q'], 'dropped-pi': lambda e: math.degrees(e['p'] / e['q'])})
for fam, e in family(F, 2):
    ok(float(e['deg']).is_integer() and 0 < e['deg'] < 360, f'C fluency-l7 degrees not whole or outside a turn {e}')
sweep(F, 3, lambda e: math.degrees(e['j'] / 20), {'wrong-way-round': lambda e: rad(e['j'] / 20), 'used-a-full-turn': lambda e: 2 * math.degrees(e['j'] / 20)}, tolk=0.06)
sweep(F, 4, lambda e: 2 * pi * e['r'] * e['d'] / 360, {'used-degrees': lambda e: e['r'] * e['d'], 'wrong-way-round': lambda e: e['r'] * math.degrees(e['d'])})

# ---------------------------------------------------------------- D: canvas lines end on drawn points
LIN = re.compile(r'^\s*(-?[\d.]+)\s*\+\s*(?:\(?(-?[\d./]+)\)?)\s*\*\s*\(\s*(?:x\s*-\s*(-?[\d.]+)|(-?[\d.]+)\s*-\s*x)\s*\)\s*$')
def canvases(n):
    if isinstance(n, dict):
        if 'canvas' in n and isinstance(n['canvas'], dict) and n['canvas'].get('kind') == 'plane':
            yield n['canvas']
        for v in n.values():
            yield from canvases(v)
    elif isinstance(n, list):
        for v in n:
            yield from canvases(v)

nlines = 0
for name in sorted(f[:-5] for f in os.listdir(SRC) if f.endswith('.json') and f != 'course.json' and not f.startswith('fluency')):
    for cv in canvases(load(name)):
        st = cv.get('state', {}); pr = cv.get('params', {})
        if 'derive' in cv or pr.get('params'):
            continue  # live canvases are checked by their captions above
        pts = {p['id']: (p['x'], p['y']) for p in st.get('points', [])}
        ends = list(pts.values())
        for sg in st.get('segments', []):
            for e in (sg['from'], sg['to']):
                ends.append(pts[e] if isinstance(e, str) else tuple(e))
        fns = pr.get('functions', []) + st.get('functions', [])
        for f in fns:
            m = LIN.match(f.get('expr', ''))
            if not m or 'domain' not in f:
                continue
            y0 = float(m.group(1)); sl = float(Fraction(m.group(2)))
            g = (lambda x: y0 + sl * (x - float(m.group(3)))) if m.group(3) else (lambda x: y0 + sl * (float(m.group(4)) - x))
            for x in f['domain']:
                p = (x, g(x))
                alle = ends + [(xx, gg) for ff in fns if ff is not f for mm in [LIN.match(ff.get('expr', ''))] if mm and 'domain' in ff
                               for xx in ff['domain'] for gg in [float(mm.group(1)) + float(Fraction(mm.group(2))) * ((xx - float(mm.group(3))) if mm.group(3) else (float(mm.group(4)) - xx))]]
                if name in ('l2-ratios-that-stay', 'l3-sides-and-angles', 'homework-1') and f['id'] in ('sup', 'res', 'trend', 'low', 'high'):
                    continue  # chart lines that run the width of the chart
                nlines += 1
                ok(any(math.dist(p, q) < 0.02 for q in alle), f"D {name} line {f['id']} ends at ({p[0]:.3f}, {p[1]:.3f}), not on a drawn point")
ok(nlines > 60, f'D only {nlines} line ends checked')
# arcs: the l1 compass arc runs from B to the floor at 5 along
arc = lambda x: 1 + math.sqrt(25 - (x - 1) ** 2)
ok(abs(arc(5) - 4) < 1e-12 and abs(arc(6) - 1) < 1e-12, 'D l1 compass arc')
# chart lines over their whole region
ok(all(abs((103 + .25 * (x + 10)) - (103 + .25 * x) - 2.5) < 1e-12 for x in np.linspace(0, 10, 11)), 'D l2 resistance rises 2.50 over any 10 days')
ok(all(abs((3 + .25 * x) - (1 + .25 * x) - 2) < 1e-12 for x in np.linspace(0, 10, 11)), 'D hw1 channel vertical gap is 2 everywhere')
ok(all(abs((100 + .8 * (x + 5)) - (100 + .8 * x) - 4) < 1e-12 for x in np.linspace(0, 5, 6)), 'D l3 trend gains 4 over any 5 days')

# ---------------------------------------------------------------- E: Monte Carlo and numerical checks of stated rules
rng = np.random.default_rng(20261126)
th = rng.uniform(-720, 720, 200000)
ok(np.max(np.abs(sind(th) ** 2 + cosd(th) ** 2 - 1)) < 1e-12, 'E Pythagorean identity at 200,000 random angles')
A_, B_ = rng.uniform(-360, 360, 200000), rng.uniform(-360, 360, 200000)
ok(np.max(np.abs(sind(A_ + B_) - (sind(A_) * cosd(B_) + cosd(A_) * sind(B_)))) < 1e-12, 'E sin(A + B)')
ok(np.max(np.abs(sind(A_ - B_) - (sind(A_) * cosd(B_) - cosd(A_) * sind(B_)))) < 1e-12, 'E sin(A - B)')
ok(np.max(np.abs(cosd(A_ + B_) - (cosd(A_) * cosd(B_) - sind(A_) * sind(B_)))) < 1e-12, 'E cos(A + B)')
ok(np.max(np.abs(cosd(A_ - B_) - (cosd(A_) * cosd(B_) + sind(A_) * sind(B_)))) < 1e-12, 'E cos(A - B)')
ok(np.max(np.abs(sind(2 * th) - 2 * sind(th) * cosd(th))) < 1e-12 and np.max(np.abs(cosd(2 * th) - (1 - 2 * sind(th) ** 2))) < 1e-12
   and np.max(np.abs(cosd(2 * th) - (2 * cosd(th) ** 2 - 1))) < 1e-12, 'E double angles')
ok(np.max(np.abs(sind(th) - cosd(90 - th))) < 1e-12, 'E sin = cos of the complement')
ok(np.max(np.abs(sind(th + 180) + sind(th))) < 1e-12 and np.max(np.abs(cosd(th + 180) + cosd(th))) < 1e-12, 'E half turn flips both')
ok(np.max(np.abs((sind(th) + cosd(th)) ** 2 - (1 + sind(2 * th)))) < 1e-12, 'E (sin + cos)^2 = 1 + sin 2x')
ok(abs(np.mean(sind(np.linspace(0, 360, 360001)[:-1]) ** 2) - .5) < 1e-9, 'E sin^2 averages to one half over a cycle')
# random triangles: cosine rule, sine rule, area, largest angle faces longest side
tri = rng.uniform(-1, 1, (100000, 3, 2))
a = np.linalg.norm(tri[:, 1] - tri[:, 2], axis=1); b = np.linalg.norm(tri[:, 0] - tri[:, 2], axis=1); c = np.linalg.norm(tri[:, 0] - tri[:, 1], axis=1)
def angle_at(p, q, r):
    u, v = q - p, r - p
    return np.arccos(np.clip(np.sum(u * v, axis=1) / (np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1)), -1, 1))
Aa, Ba, Ca = angle_at(tri[:, 0], tri[:, 1], tri[:, 2]), angle_at(tri[:, 1], tri[:, 0], tri[:, 2]), angle_at(tri[:, 2], tri[:, 0], tri[:, 1])
good = np.minimum.reduce([a, b, c]) > 0.05
ok(np.max(np.abs(c ** 2 - (a ** 2 + b ** 2 - 2 * a * b * np.cos(Ca)))[good]) < 1e-9, 'E cosine rule on 100,000 random triangles (acute and obtuse)')
ok(np.max(np.abs(a / np.sin(Aa) - b / np.sin(Ba))[good] / (a / np.sin(Aa))[good]) < 1e-6, 'E sine rule on random triangles')
area = .5 * np.abs((tri[:, 1, 0] - tri[:, 0, 0]) * (tri[:, 2, 1] - tri[:, 0, 1]) - (tri[:, 2, 0] - tri[:, 0, 0]) * (tri[:, 1, 1] - tri[:, 0, 1]))
ok(np.max(np.abs(area - .5 * a * b * np.sin(Ca))) < 1e-9, 'E area = half ab sin C')
ok(np.all(np.argmax(np.stack([a, b, c]), axis=0) == np.argmax(np.stack([Aa, Ba, Ca]), axis=0)), 'E largest angle faces the longest side')
ok(np.mean(Ca > pi / 2) > .1, 'E the random triangles include obtuse ones')
# converse of Pythagoras, and the obtuse case stated in l1 quiz[2]
ok(big(6, 8, 11) > 90 and abs(big(6, 8, 10) - 90) < 1e-9, 'E 6, 8, 11 has an obtuse largest angle')
# dot product rule, l12 and hw3
uu, vv = rng.normal(size=(100000, 2)), rng.normal(size=(100000, 2))
au, av = np.arctan2(uu[:, 1], uu[:, 0]), np.arctan2(vv[:, 1], vv[:, 0])
ok(np.max(np.abs(np.cos(av - au) - np.sum(uu * vv, axis=1) / (np.linalg.norm(uu, axis=1) * np.linalg.norm(vv, axis=1)))) < 1e-9, 'E cosine of the angle between vectors is the dot product over the lengths')
# volatility as an arrow: l5 transfer and hw1 longform. 400,000 days of correlated returns
n = 400000
z1, z2 = rng.normal(size=n), rng.normal(size=n)
rA = .20 * z1; rB = .15 * (.5 * z1 + math.sqrt(.75) * z2)
ok(abs(np.corrcoef(rA, rB)[0, 1] - C(60)) < .005, 'E simulated correlation is cos 60 = 0.5')
ok(abs(np.std(rA - rB) - .1803) < .001, f'E spread volatility {np.std(rA - rB):.4f} vs cosine rule 0.1803')
ok(abs(np.std(rA - rB) - .25) > .05 and abs(np.std(rA - rB) - .05) > .05, 'E the spread is neither Pythagoras nor the difference')
rA2 = .25 * z1; rB2 = .20 * (.5 * z1 + math.sqrt(.75) * z2)
ok(abs(np.std(rA2 + rB2) - .3905) < .002, f'E volatility of the SUM of the two returns {np.std(rA2 + rB2):.4f} vs 0.3905')
# small angles: sin and tan agree for small angles (l3 trap remark), in either unit
ok(abs(S(15) - T(15)) / T(15) < .04 and abs(S(60) - T(60)) / T(60) > .4, 'E sine and tangent are close at 15 degrees, not at 60')
# sine-rule ambiguous case exists (basis for finding 3): a = 7, b = 10, A = 40 gives two triangles
sB = 10 * S(40) / 7
B1, B2 = aS(sB), 180 - aS(sB)
ok(sB < 1 and 40 + B2 < 180 and abs(7 / S(40) - 10 / S(B1)) < 1e-9 and abs(7 / S(40) - 10 / S(B2)) < 1e-9, 'E two triangles share a = 7, b = 10, A = 40')

# basis for the fix texts of findings 3, 5, 6, 7 and 10
ok(abs(S(180 - 47.2) - S(47.2)) < 1e-12 and (180 - 47.2) + 55 > 180, 'E lake: 132.8 has the same sine as 47.2 but cannot share a triangle with the 55 at P')
ok(abs(math.tan(35) - 0.474) < 5e-4 and abs(T(35) - 0.700) < 5e-4, 'E tan 35 is 0.700 in degree mode and 0.474 in radian mode')
kk = np.linspace(-1, 1, 2001)
ok(np.degrees(np.arcsin(kk)).min() >= -90 and np.degrees(np.arcsin(kk)).max() <= 90 and np.degrees(np.arccos(kk)).min() >= 0 and np.degrees(np.arccos(kk)).max() <= 180
   and abs(np.degrees(np.arctan(1e12)) - 90) < 1e-6 and abs(np.degrees(np.arctan(-1e12)) + 90) < 1e-6, 'E principal ranges: asin and atan in -90..90, acos in 0..180')
ok(abs(12 * 0.26795 - 3.2154) < 5e-5 and f'{12 * 0.26795:.2f}' == '3.22' and f'{12 / 0.26795:.2f}' == '44.78', 'E finding 7 fix: tan 15 = 0.26795 gives 3.22 and 44.78')
ok(abs(pi / 2 - 1.5) / 1.5 > .04, 'E 1.57 is not half as long again as 1 (finding 10)')

# ---------------------------------------------------------------- F: checks tied to findings (fail while the content stands)
# F1 homework-3 h3-correlation-angle: "de-meaned returns over two days" must each sum to zero
it = node('homework-3', 'items[4]')
if 'de-meaned' in it['prose'] and 'two days' in it['prose']:
    ok(abs(3 + 4) < 1e-9 and abs(5 - 12) < 1e-9, 'F1 homework-3 items[4]: u = (3, 4) and v = (5, -12) are called de-meaned two-day returns but do not sum to zero; '
       'any two de-meaned two-day series have correlation +1 or -1, never -0.51')
x2 = rng.normal(size=(100000, 2)); y2 = rng.normal(size=(100000, 2))
x2 -= x2.mean(axis=1, keepdims=True); y2 -= y2.mean(axis=1, keepdims=True)
cc = np.sum(x2 * y2, axis=1) / (np.linalg.norm(x2, axis=1) * np.linalg.norm(y2, axis=1))
ok(np.max(np.abs(np.abs(cc) - 1)) < 1e-9, 'E/F1 basis: every pair of de-meaned two-day series has correlation exactly +1 or -1')
# F2 l3 trap: the step uses the given tan 15 = 0.2679, whose product rounds to 3.21, not the keyed 3.22
t = node('l3-sides-and-angles', 'screens[7]')
if re.search(r'12 \\times 0\.2679(?!\d)', t['hints'][2]['text']):
    ok(f'{12 * 0.2679:.2f}' == '3.22', f"F2 l3 screens[7]: the hint's 12 x 0.2679 = {12 * 0.2679:.4f} rounds to {12 * 0.2679:.2f}, but the keyed option is 3.22 (true 12 tan 15 = {12 * T(15):.4f})")
    ok(f'{12 / 0.2679:.2f}' == '44.78', f'F2 l3 screens[7]: 12 / 0.2679 = {12 / 0.2679:.2f}, option says 44.78')
# F3 l6 screens[1]: the "below" feedback says the point is 0.5 from the axis anywhere in 180.5..359.5
reg = [o for o in node('l6-beyond-90', 'screens[1]')['widget']['wrong'] if o['id'] == 'below'][0]['region']['angle']
fb = node('l6-beyond-90', 'screens[1]')['feedback']['byKey']['below']
if '0.5 from the axis there' in fb:
    aa = np.linspace(reg[0], reg[1], 3591)
    frac = float(np.mean(np.abs(np.abs(sind(aa)) - .5) < .05))
    ok(frac > .9, f'F3 l6 screens[1] byKey.below: the height is within 0.05 of -0.5 on only {frac:.0%} of the region {reg}')
# F4 l10 transfer: "it never changes the total" - the total in pounds does change
ex = node('l10-identity-from-circle', 'screens[9]')['explain']['text']
if 'never changes the total' in ex:
    tot = 10000 * (np.abs(cosd(np.linspace(0, 360, 361))) + np.abs(sind(np.linspace(0, 360, 361))))
    ok(tot.max() - tot.min() < 1, f'F4 l10 screens[9]: |A| + |B| runs from {tot.min():.0f} to {tot.max():.0f} pounds as the angle turns; only A^2 + B^2 is fixed')
# F5 hw1 longform: "the portfolio's volatility" of 39.05% exceeds both stocks; as a share of the money invested it is half that
m = node('homework-1', 'items[8]')
if "portfolio's volatility is about 39.05%" in m['model']:
    w = .5
    ok(abs(np.std(w * rA2 + w * rB2) - .3905) < .002, f"F5 homework-1 items[8]: a portfolio split equally between the stocks has volatility {np.std(w * rA2 + w * rB2):.4f} of its value, "
       'not 0.3905; 39.05% is the volatility of the sum of the two returns (two units of money), which the item does not say')

print(f'{passed} checks passed, {len(fails)} failed; fluency cases swept: {sum(cnt.values())}; canvas line ends: {nlines}')
for f in fails[:60]:
    print('FAIL', f)
sys.exit(1 if fails else 0)
