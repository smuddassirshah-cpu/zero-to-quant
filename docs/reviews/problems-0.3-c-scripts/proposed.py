"""Second read, problems 0.3 c: the numbers of the fixes proposed in review-problems-0.3-c.md, each by two routes, and a
search of the series and trig courses and the Stage 0 exams for the new figures.

Run: <venv>/bin/python docs/reviews/problems-0.3-c-scripts/proposed.py     (from the repo root; exits 0)
"""
import glob
import math
import re
import sys
from fractions import Fraction as F
from itertools import combinations

checks = fails = 0


def say(ok, msg):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print('FAIL', msg)


D = math.radians

# --- finding S5: tin display, top row 8, 5 more each row, 10 rows; stand = rows 4 to 10
tins = [8 + 5 * i for i in range(10)]
say(all(tins[k - 1] == 5 * k + 3 for k in range(1, 11)), 'row k = 5k + 3')
say(tins[9] == 53 == 8 + 9 * 5, 'bottom row 53')
say(8 + 10 * 5 == 58 and 10 * 5 == 50, 'part 1 slips 58, 50')
say(sum(tins) == 305 == 10 * (8 + 53) // 2 == 5 * (16 + 45), 'display 305')
say(2 * 305 == 610 and 5 * 53 == 265 and 5 * (16 + 50) == 330, 'part 2 slips 610, 265, 330')
say(len(range(4, 11)) == 7 == 10 - 4 + 1 and 10 - 4 == 6, 'stand has 7 rows; slip 6')
say(tins[3] == 23 and sum(tins[3:]) == 266 == 7 * (23 + 53) // 2 == 305 - sum(tins[:3]) and sum(tins[:3]) == 39, 'stand 266 = 305 - 39')
say(6 * (23 + 53) // 2 == 228 and 305 - sum(tins[:4]) == 243 and sum(tins[:4]) == 62, 'part 4 slips 228, 243')

# --- finding S7: pizza, 11 toppings, exactly 4, then a 12th
c = lambda n, k: sum(1 for _ in combinations(range(n), k))
say(c(11, 4) == 330 == 11 * 10 * 9 * 8 // 24 and 11 * 10 * 9 * 8 == 7920 and 11 * 4 == 44 and 11 ** 4 == 14641, 'part 1: 330, ordered 7920, 44')
say(c(11, 7) == 330 and 11 * 10 * 9 * 8 * 7 * 6 * 5 == 1663200, 'part 2 (old form): 330')
say(c(11, 4) + c(11, 7) == 660, 'part 2 (new form): 660')
say(c(11, 3) == 165 and c(12, 4) == 495 == 330 + 165 and 330 + 11 == 341 and 12 * 11 * 10 * 9 == 11880, 'part 3: 495; slips 341, 660, 11880')
say([c(12, k) for k in range(5)] == [1, 12, 66, 220, 495] and sum(c(12, k) for k in range(13)) == 4096 == 2 ** 12 and 2 ** 11 == 2048, 'part 4: 4096; slips 4095, 2048')
say(8 ** 3 != 11 ** 4, 'the powers-of-eleven item also has 14641: use 11 x 4 = 44 and the ordered count as slips, not 11^4')

# --- finding T3: hexagon with sides of 8 cm
h = math.sqrt(8 ** 2 - 4 ** 2)
say(abs(h - 4 * math.sqrt(3)) < 1e-12 and abs(h ** 2 - 48) < 1e-9, 'height 4 root 3 = root 48')
A, C, Dd = (8, 0), (8 * math.cos(D(120)), 8 * math.sin(D(120))), (-8, 0)
say(abs(math.dist(A, C) - 8 * math.sqrt(3)) < 1e-12 and abs(math.dist(A, Dd) - 16) < 1e-12 and abs(math.dist(C, Dd) - 8) < 1e-12, 'AC = 8 root 3, AD = 16, CD = 8')
say(abs(math.dist(A, C) ** 2 + 64 - 256) < 1e-9 and 192 + 64 == 256 == 16 ** 2, 'AC^2 + CD^2 = 256')
say(8 * 3 + 64 == 88 and abs(64 * math.sqrt(3) + 64 - 174.85) < 0.005 and 192 + 8 == 200, 'part 3 slips 88, 174.85, 200')
say(abs(math.degrees(math.asin(8 / 16)) - 30) < 1e-9 and abs(math.degrees(math.atan(8 / 16)) - 26.57) < 0.005, 'angle CAD 30; tan slip 26.57')
say(abs(math.sqrt(64 + 16) - math.sqrt(80)) < 1e-12, 'part 1 slip root 80')

# --- finding T9: two angles with sin A = 28/53
say(28 ** 2 + 45 ** 2 == 53 ** 2 and 7 ** 2 + 24 ** 2 == 25 ** 2, 'triples 28, 45, 53 and 7, 24, 25')
Aa = math.pi - math.asin(28 / 53)
Bb = math.acos(24 / 25)
sA, cA, sB, cB = F(28, 53), F(-45, 53), F(7, 25), F(24, 25)
say(abs(math.cos(Aa) - float(cA)) < 1e-12 and abs(math.sin(Bb) - float(sB)) < 1e-12, 'cos A = -45/53, sin B = 7/25')
sAB, cAB = sA * cB + cA * sB, cA * cB - sA * sB
say(sAB == F(357, 1325) and cAB == F(-1276, 1325) and 357 ** 2 + 1276 ** 2 == 1325 ** 2, 'sin(A+B) = 357/1325, cos(A+B) = -1276/1325')
say(abs(math.sin(Aa + Bb) - float(sAB)) < 1e-12 and abs(math.cos(Aa + Bb) - float(cAB)) < 1e-12, 'the same from the angles')
say(round(float(cA), 6) == -0.849057 and round(float(sAB), 4) == 0.2694 and round(float(cAB), 4) == -0.9630, 'decimals -0.849057, 0.2694, -0.9630')
say(round(1 - 28 / 53, 6) == 0.471698 and round(2025 / 2809, 6) == 0.720897, 'part 1 slips 0.471698, 0.720897')
say(round((672 + 315) / 1325, 6) == 0.744906 and round(28 / 53 + 0.28, 6) == 0.808302, 'part 3 slips 0.744906, 0.808302')
say(round((-1080 + 196) / 1325, 6) == -0.667170 and round((1080 - 196) / 1325, 6) == 0.667170, 'part 4 slips -0.66717, 0.66717')
pr = math.degrees(math.asin(0.2694))
say(round(pr, 2) == 15.63 and round(math.degrees(Aa + Bb), 2) == 164.37 and round(180 - pr, 1) == 164.4, 'A + B = 164.37; principal 15.63')
say(round(180 + pr, 2) == 195.63 and round(360 - pr, 2) == 344.37, 'part 5 slips 195.63, 344.37')
say(round(math.degrees(Aa), 1) == 148.1 and round(math.degrees(Bb), 1) == 16.3, 'A = 148.1, B = 16.3')
say(round(math.degrees(math.acos(-0.9630)), 1) == 164.4, 'the cosine route gives 164.4')

# --- finding T11: daylight above 9.8 hours
L = lambda t: 4.4 * math.sin(math.pi / 6 * (t - 3)) + 12
grid = [k / 1000 for k in range(0, 12001)]
cross = [t for t in grid if abs(L(t) - 9.8) < 1e-9]
say(cross == [2.0, 10.0] and abs((9.8 - 12) / 4.4 + 0.5) < 1e-12, 'crossings at 2 and 10, sine -0.5')
say(round(sum(1 for t in grid if L(t) > 9.8 + 1e-9) / 1000) == 8 == 10 - 2, 'above 9.8 hours for 8 months')
say([t for t in grid if abs(L(t) - 14.2) < 1e-9] == [4.0, 8.0], 'slip: +0.5 gives 4 and 8')
say([t for t in grid if abs(math.sin(math.pi * t / 6) + 0.5) < 1e-9] == [7.0, 11.0], 'slip: no shift gives 7 and 11')
say(abs(math.pi / 6 * (2 - 3) + math.pi / 6) < 1e-12 and abs(math.pi / 6 * (10 - 3) - 7 * math.pi / 6) < 1e-12, 'angles -pi/6 and 7pi/6')

# --- finding T12: garden bed with edges 10 m and 13 m, area 25 m^2
say(0.5 * 10 * 13 == 65 and F(25, 65) == F(5, 13) and 5 ** 2 + 12 ** 2 == 13 ** 2, 'area 65 sin C; sin C = 5/13')
a1 = math.degrees(math.asin(5 / 13))
say(round(a1, 2) == 22.62 and round(180 - a1, 2) == 157.38, 'angles 22.62 and 157.38')
a2 = math.degrees(math.asin(25 / 130))
say(round(a2, 2) == 11.09 and round(180 - a2, 2) == 168.91 and round(360 - a1, 2) == 337.38, 'part 2 slips 11.09, 168.91; 337.38')
say(abs(math.cos(D(180 - a1)) + 12 / 13) < 1e-12 and round(12 / 13, 4) == 0.9231 and round(1 - 5 / 13, 6) == 0.615385 and round(144 / 169, 6) == 0.852071, 'cos C = -12/13; slips')
third = math.dist((13, 0), (10 * math.cos(D(180 - a1)), 10 * math.sin(D(180 - a1))))
say(abs(third ** 2 - 509) < 1e-9 and 100 + 169 + 240 == 509 and round(third, 2) == 22.56, 'third edge root 509 = 22.56')
say(round(math.sqrt(29), 4) == 5.3852 and round(math.sqrt(269), 4) == 16.4012 and round(math.sqrt(389), 4) == 19.7231, 'part 4 slips 5.3852, 16.4012, 19.7231')
say(third < 10 + 13, 'triangle inequality')

# --- bands proposed
say(abs(0.80795 - 0.807955) <= 6e-6 and abs(0.80796 - 0.807955) <= 6e-6 and abs(0.80798 - 0.807955) > 6e-6 and abs(0.80798 - 0.97 ** 7) <= 6e-6, 'S9: band 6e-6 takes 0.80795 and 0.80796 and sends 0.80798 to a calculator entry')
say(abs(-0.882 - -15 / 17) <= 0.0005 and abs(-0.88 - -15 / 17) > 0.0005 and abs(15 / 17 - -15 / 17) > 0.0005, 'T10 (old numbers): band 0.0005 takes -0.882')
say(abs(-0.849 - -45 / 53) <= 0.0005 and abs(-0.85 - -45 / 53) > 0.0005, 'T10 (new numbers): band 0.0005 takes -0.849 and refuses -0.85')
say(abs(0.64 - 0.6435) <= 0.005 and abs(0.6 - 0.6435) > 0.005 and abs(0.52 - 0.5236) <= 0.005 and abs(0.5 - 0.5236) > 0.005, 'T4: radian bands of 0.005 take 0.64 and 0.52 and leave 0.6 and 0.5 to their own entries')

# --- the new figures against the two courses and the Stage 0 exams
files = [f for pat in ('app/content/courses/series/*.json', 'app/content/courses/trig/*.json', 'app/content/exams/topic-0.3.json', 'app/content/exams/stage-0.json')
         for f in glob.glob(pat) if '/problems-' not in f and not f.endswith('course.json')]
text = {f: open(f).read().replace('\\\\', '\\') for f in files}   # JSON's doubled backslash, so that \sqrt reads as typed
new = {
    'tins': [r'\b305\b', r'\b266\b', r'5k \+ 3', r'8, 13, 18'],
    'pizza': [r'\b330\b', r'\b495\b', r'\b4096\b', r'binom\{11\}\{4\}', r'binom\{12\}\{4\}', r'\b7920\b'],
    'hexagon': [r'4\\sqrt\{3\}', r'8\\sqrt\{3\}', r'sqrt\{48\}', r'sqrt\{192\}'],
    'two angles': [r'\{28\}\{53\}', r'\{45\}\{53\}', r'28, 45, 53', r'\b1325\b', r'164\.4', r'164\.37'],
    'daylight': [r'9\.8 hours'],
    'garden': [r'22\.62', r'157\.38', r'\b509\b', r'22\.56', r'65\\sin'],
}
for name, pats in new.items():
    for pat in pats:
        hits = [f.split('/')[-2] + '/' + f.split('/')[-1] for f, t in text.items() if re.search(pat, t)]
        print(f'   {name:11s} {pat:22s} {"none" if not hits else ", ".join(hits)}')
print(f'proposed: {checks} checks, {fails} failures; {len(files)} files searched')
sys.exit(1 if fails else 0)
