"""Second reader's recompute for number-sense level 4 (independent of docs/reports/number-sense-L4-numbers.py).

Every key and wrong value is rebuilt here from the item's text by a route other than the author's
(trial division, set intersections of factor lists, the shoelace formula on the drawn vertices,
sorting the expanded frequency table, integer arithmetic), then compared with the JSON.
Checks that fail because the content is wrong stay failing and are findings in
docs/reviews/review-number-sense-4.md; the script exits 1 while any of them is unfixed.

Run from the repo root:  python docs/reviews/number-sense-4-scripts/read-numbers.py
"""
import json, math, os, sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
D = os.path.join(ROOT, 'app', 'content', 'courses', 'number-sense')
L = {k: json.load(open(os.path.join(D, f), encoding='utf8')) for k, f in {
    'l15': 'l15-building-blocks.json', 'l16': 'l16-shared-factors.json', 'l17': 'l17-around-and-inside.json',
    'l18': 'l18-circles-and-units.json', 'l19': 'l19-one-number-for-many.json', 'rev': 'review-4.json', 'hw': 'homework-4.json'}.items()}
res = []


def ck(ok, label, finding=None):
    res.append((bool(ok), label, finding))
    if not ok:
        print(('FINDING ' + str(finding) if finding else 'FAIL') + ': ' + label)


def factors(n): return [d for d in range(1, n + 1) if n % d == 0]
def is_prime(n): return len(factors(n)) == 2
def pf(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0: out.append(p); n //= p
        p += 1
    return out
def hcf(a, b): return max(set(factors(a)) & set(factors(b)))
def lcm(a, b): return next(m for m in range(max(a, b), a * b + 1, max(a, b)) if m % a == 0 and m % b == 0)
def shoelace(pts): return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2
def perim(pts): return sum(math.dist(a, b) for a, b in zip(pts, pts[1:] + pts[:1]))
def within(v, a, tol): return abs(v - a) <= (tol or {}).get('abs', 0) + 1e-9   # grade.js within()
def wr(w): return {x['id']: x['value'] for x in w.get('wrong', [])}
def cell(s, r, c): return s['widget']['rows'][r][c]
def median(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else F(xs[n // 2 - 1] + xs[n // 2], 2)


# ---------- l15 ----------
S = L['l15']['screens']
ck(sorted(int(i[3:]) for i in S[0]['widget']['answer']) == [d for d in range(1, 9) if 36 % d == 0], 'l15 s0 row lengths 1..8 dividing 36')
ck(S[1]['widget']['answer'] == len(factors(36)) == 9, 'l15 s1 nine factors of 36')
ck(S[2]['widget']['answer'] == 1 and is_prime(37), 'l15 s2 37 prime, one rectangle')
cellid = lambda n: f'r{(n - 1) // 10 + 1}c{(n - 1) % 10 + 1}'
want = {cellid(n) for n in range(1, 101) if any(n % p == 0 and n != p for p in (2, 3, 5))}
ck(set(S[3]['canvas']['state']['shade']['crossed']) == want, 'l15 s3 shading = multiples of 2, 3, 5 other than themselves')
left7 = {cellid(n) for n in range(14, 101, 7) if cellid(n) not in want}
ck(set(S[3]['widget']['answer']) == left7 == {cellid(49), cellid(77), cellid(91)}, 'l15 s3 unshaded multiples of 7 are 49, 77, 91')
ck(set(S[3]['explain']['canvas']['shade']['crossed']) == want | left7, 'l15 s3 explain shading adds 49, 77, 91')
white = [n for n in range(2, 101) if cellid(n) not in want | left7]
ck(white == [n for n in range(2, 101) if is_prime(n)] and len(white) == 25, 'l15 s3 white cells apart from 1 are the 25 primes')
ck(sum(is_prime(n) for n in range(2, 50)) == 15 and sum(is_prime(n) for n in range(2, 30)) == 10, 'l15 s3 15 primes below 50, 10 below 30')
ck(is_prime(97) and 9 ** 2 < 97 < 10 ** 2 and all(97 % p for p in (2, 3, 5, 7)), 'l15 s4 97 prime, root between 9 and 10')
for side in ('left', 'right'):
    g = S[5]['canvas'][side]['params']
    kids = {}
    for e in g['edges']: kids.setdefault(e['from'], []).append(e['to'])
    lab = {n['id']: int(n['label']) for n in g['nodes']}
    ck(all(lab[p] == math.prod(lab[k] for k in ks) for p, ks in kids.items()), f'l15 s5 {side} tree: every node is the product of its children')
    leaves = sorted(lab[n['id']] for n in g['nodes'] if n['id'] not in kids)
    ck(leaves == pf(360) == [2, 2, 2, 3, 3, 5], f'l15 s5 {side} tree leaves are the primes of 360')
    ck(all((n.get('colour') == 2) == (n['id'] not in kids) for n in g['nodes']), f'l15 s5 {side} tree: exactly the leaves are coloured')
ck([cell(S[5], r, c)['answer'] for r in range(3) for c in (1, 2)] == [3, 3, 2, 2, 1, 1], 'l15 s5 table 3, 2, 1 in both trees')
ring = {1: 'r1c1', 2: 'r1c2', 51: 'r6c1', 53: 'r6c3', 57: 'r6c7', 59: 'r6c9', 91: 'r10c1'}
ck(all(cellid(n) == c for n, c in ring.items()) and set(S[6]['widget']['answer']) == {c for n, c in ring.items() if is_prime(n)}, 'l15 s6 ringed primes are 2, 53, 59')
ck(51 == 3 * 17 and 57 == 3 * 19 and 91 == 7 * 13 and len(factors(1)) == 1, 'l15 s6 51, 57, 91 composite; 1 has one factor')
ck(S[7]['widget']['answer'] == len(factors(360)) == 24 and wr(S[7]['widget']) == {'no-plus-one': 3 * 2 * 1, 'added': 4 + 3 + 2}, 'l15 s7 24 factors of 360 and the two slips')
ck(sorted(int(x) for row in S[7]['canvas']['params']['cells'] for x in row) == factors(36), 'l15 s7 grid lists the nine factors of 36')
ok9 = {o['id']: o.get('correct', False) for o in S[9]['widget']['options']}
ck(all(ok9[f'd{n}'] == (252 % n == 0) for n in (21, 63, 7, 12, 5, 8, 24)), 'l15 s9 which lengths divide 252')
ck(pf(252) == [2, 2, 3, 3, 7] and len(factors(252)) == 18 and (252 // 21, 252 // 63, 252 // 7, 252 // 12) == (12, 4, 36, 21) and (252 % 5, 252 % 8, 252 % 24) == (2, 4, 12), 'l15 s9 252: primes, 18 factors, quotients and remainders')
Q = L['l15']['quiz']
ck(Q[0]['widget']['answer'] == len(factors(49)) == 3, 'l15 q0 49 has 3 factors')
ck([n for n in range(1, 400) if len(factors(n)) % 2] == [k * k for k in range(1, 20)], 'l15 q0 odd factor count exactly for squares (to 400)')
ck(87 == 3 * 29 and is_prime(29) and 7 * 13 == 91, 'l15 q1 87 = 3 x 29')
ck(pf(72) == [2, 2, 2, 3, 3] and 4 * 27 == 108 and 2 * 9 * 4 == 72, 'l15 q2 72 = 2^3 x 3^2; distractors')
ck(Q[3]['widget']['answer'] == len(factors(72)) == 12 and wr(Q[3]['widget']) == {'no-plus-one': 6, 'added': 7}, 'l15 q3 12 factors of 72')

# ---------- l16 ----------
S = L['l16']['screens']
ck(S[0]['widget']['points'][0]['target'] == lcm(12, 18) == 36 and S[1]['widget']['answer'] == hcf(12, 18) == 6, 'l16 s0/s1 LCM 36, HCF 6')
ck(sorted(p['x'] for p in S[0]['canvas']['state']['points'] if p['id'][0] == 'a') == list(range(12, 79, 12)) and sorted(p['x'] for p in S[0]['canvas']['state']['points'] if p['id'][0] == 'b') == list(range(18, 79, 18)), 'l16 s0 prints drawn at multiples of 12 and 18')
ck(S[2]['widget']['answer'] == lcm(4, 6) == 12 and hcf(4, 6) == 2, 'l16 s2 LCM of 4 and 6')
def venn_ok(v, a, b):
    reg = {k: sorted(int(x) for x in s.split(',')) for k, s in v['values'].items()}
    return sorted(reg['A'] + reg['AB']) == pf(a) and sorted(reg['B'] + reg['AB']) == pf(b) and not set(reg['A']) & set(reg['B']) and math.prod(reg['AB']) == hcf(a, b)
ck(venn_ok(S[3]['canvas']['params'], 84, 120), 'l16 s3 venn of 84 and 120')
ck(S[3]['widget']['answer'] == hcf(84, 120) == 12 and S[4]['widget']['answer'] == lcm(84, 120) == 840 and 12 * 840 == 84 * 120 == 10080, 'l16 s3/s4 HCF 12, LCM 840, product 10,080')
ck(wr(S[4]['widget'])['missed-two'] == 7 * 12 * 5, 'l16 s4 missed-two slip')
ck(F(84, 120) == F(7, 10) and F(5, 12) + F(7, 18) == F(29, 36) and venn_ok(S[6]['canvas']['params'], 12, 18), 'l16 s5/s6 7/10 and 29/36')
a, b, rem = 252, 198, []
while b: rem.append(a % b); a, b = b, a % b
ck(rem == [54, 36, 18, 0] and hcf(252, 198) == 18 and lcm(252, 198) == 2772 == 252 * 198 // 18, 'l16 s7 Euclid remainders 54, 36, 18, 0; LCM 2,772')
ck([cell(S[7], r, 2)['answer'] for r in range(4)] == rem, 'l16 s7 table remainders')
ck((hcf(8, 12), lcm(8, 12)) == (4, 24), 'l16 s8 8 and 12')
ck(venn_ok(S[10]['canvas']['params'], 150, 240) and S[10]['widget']['answer'] == hcf(150, 240) == 30 and lcm(150, 240) == 1200 and 150 % 90, 'l16 s10 clips of 30')
Q = L['l16']['quiz']
ck(Q[0]['widget']['answer'] == lcm(6, 4) and (hcf(8, 15), lcm(8, 15)) == (1, 120) and Q[2]['widget']['answer'] == lcm(6, 18) == 18 and F(18, 24) == F(3, 4) and lcm(18, 24) == 72, 'l16 quiz')
# alternative valid orders of the derive screen
ck(True, 'l16 s9: order c84, c120, def, prod, same, end is also a valid argument (finding, by reading)')

# ---------- l17 ----------
S = L['l17']['screens']
ck(max(range(1, 12), key=lambda x: x * (12 - x)) == 6 and 10 * 2 == 20 and 5 * 7 == 35, 'l17 s0 best pen 6 by 6')
ck((cell(S[1], 0, 1)['answer'], cell(S[1], 1, 1)['answer']) == (2 * (8 + 3), 8 * 3), 'l17 s1 perimeter 22, area 24')
poly = lambda s, i: s['canvas']['state']['polygons'][i]['points']
ck(shoelace(poly(S[2], 1)) == S[2]['widget']['answer'] == 20, 'l17 s2 triangle area by shoelace')
ck(shoelace(poly(S[3], 0)) == S[3]['widget']['answer'] == 28 and math.dist((0, 0), (3, 4)) == 5, 'l17 s3 parallelogram 28, slant 5')
ck(shoelace(poly(S[4], 0)) == S[4]['widget']['answer'] == 32, 'l17 s4 trapezium 32')
ck(shoelace(poly(S[5], 0)) == S[5]['widget']['answer'] == 48, 'l17 s5 L-shape 48')
ck(perim(poly(S[6], 0)) == S[6]['widget']['answer'] == 32 == 2 * (10 + 6) and wr(S[6]['widget']) == {'subtracted': 32 - 7, 'corner': 32 - 14, 'area': 48, 'added': 32 + 14}, 'l17 s6 L perimeter 32 and slips')
ck(S[7]['widget']['answer'] == 100 * 100, 'l17 s7 10,000')
ck(F(1100 * 550, 1000 * 500) == F(121, 100) and 1100 * 550 == 605000 and S[8]['widget']['answer'] == 1.21, 'l17 s8 1.21 (pence arithmetic)')
Q = L['l17']['quiz']
ck([q['widget']['answer'] for q in Q] == [30, 22, 81, 45], 'l17 quiz keys')

# ---------- l18 ----------
S = L['l18']['screens']
pi = math.pi
ck(all(round(r / a, 2) == 3.14 for a, r in ((7, 22), (10, 31.4), (20, 62.8))), 'l18 s0 three ratios 3.14')
ck(round(50 * pi, 1) == S[1]['widget']['answer'] == 157.1, 'l18 s1 wheel 157.1')
for n, fr in zip((4, 8, 16), S[2]['canvas']['controls'][0]['frames']):
    half = 5 * math.sin(math.pi / n)
    ps = fr['right']['polygons']
    ck(len(ps) == n and all(abs(p['sector']['cx'] - half * (i + 1)) < 1e-3 for i, p in enumerate(ps)) and all(abs((p['sector']['theta2'] - p['sector']['theta1']) - 360 / n) < 1e-6 for p in ps), f'l18 s2 {n} wedges laid head to tail at the right spacing and angle')
ck((cell(S[3], 0, 1)['answer'], cell(S[3], 0, 2)['answer'], cell(S[3], 1, 1)['answer'], cell(S[3], 1, 2)['answer']) == (30, 75, round(10 * pi, 2), round(25 * pi, 2)), 'l18 s3 pond table')
ck(S[4]['widget']['answer'] == round(4 * pi + 8, 2) == 20.57, 'l18 s4 semicircle perimeter')
ck(F(72 * 1000, 3600) == 20 == S[5]['widget']['answer'], 'l18 s5 72 km/h')
ck(cell(S[6], 0, 1)['answer'] == 2.5 * 100 * 100 and cell(S[6], 1, 1)['answer'] == 24 and 2 * (2 * 3 + 2 * 4 + 3 * 4) == 52, 'l18 s6 25,000 and 24')
ck(S[7]['widget']['answer'] == round(25 * pi, 2) and round(100 * pi, 2) == 314.16, 'l18 s7 78.54 against 314.16')
# s7 wrong entry two-r: feedback says "You doubled the radius instead of squaring it"
ck(abs(wr(S[7]['widget'])['two-r'] - pi * (2 * 5)) < 0.05 or 'doubled the radius' not in S[7]['feedback']['byKey']['two-r'], 'l18 s7 wrong two-r: "doubled the radius instead of squaring" gives pi x 10 = 31.42, the entry holds 62.83 (= 2 x pi x 10)', 'W1')
ck(F(1260000, 252) == 5000 and round(F(5000 * 10, 75)) == 667 and round(1260000 / 365) == 3452 and round(5000 / 24) == 208, 'l18 s9 5,000 a day, 667 an hour')
Q = L['l18']['quiz']
ck((Q[0]['widget']['answer'], Q[1]['widget']['answer'], Q[2]['widget']['answer']) == (round(6 * pi, 2), round(9 * pi, 2), 25), 'l18 quiz keys')

# pi tolerance probe: what a learner using 3.14, 3.142 or 22/7 (rounded as asked) gets on every pi item
print('\npi probe (value typed -> accepted / matches wrong id / generic):')
PI_ITEMS = [
    ('l18 s1 wheel', S[1]['widget'], lambda p: 50 * p, 1),
    ('l18 s3 circumference', cell(S[3], 1, 1), lambda p: 10 * p, 2),
    ('l18 s3 area', cell(S[3], 1, 2), lambda p: 25 * p, 2),
    ('l18 s4 semicircle', S[4]['widget'], lambda p: 4 * p + 8, 2),
    ('l18 s7 pond', S[7]['widget'], lambda p: 25 * p, 2),
    ('l18 q0', Q[0]['widget'], lambda p: 6 * p, 2),
    ('l18 q1', Q[1]['widget'], lambda p: 9 * p, 2),
    ('review r-circle-14', L['rev']['items'][6]['widget'], lambda p: 49 * p, 2),
    ('hw semicircle area', L['hw']['items'][1]['parts'][0]['widget'], lambda p: 60 + 4.5 * p, 2),
    ('hw semicircle perimeter', L['hw']['items'][1]['parts'][1]['widget'], lambda p: 26 + 3 * p, 2),
]
rejected = []
for name, w, f, dp in PI_ITEMS:
    row = []
    for tag, p in (('3.14', 3.14), ('3.142', 3.142), ('22/7', 22 / 7)):
        v = round(f(p) + 1e-12, dp)
        if within(v, w['answer'], w.get('tol')): r = 'ok'
        else:
            hit = [x['id'] for x in w.get('wrong', []) if within(v, x['value'], x.get('tol', w.get('tol')))]
            r = 'WRONG:' + hit[0] if hit else 'generic'
            rejected.append((name, tag, v))
        row.append(f'{tag}->{v} {r}')
    print(f'  {name:26s} key {w["answer"]} tol {w.get("tol")}: ' + '; '.join(row))
ck(not [r for r in rejected if r[1] == '3.14'], 'pi items accept the value from pi = 3.14, which l18 s1 says "is fine": rejected ' + str([r for r in rejected if r[1] == '3.14']), 'U-pi')

# ---------- l19 ----------
S = L['l19']['screens']
days = [120, -80, 40, 40, 300, -60, 60]
ck(S[0]['canvas']['params']['data'] == days and F(sum(days), 7) == 60 == S[0]['widget']['points'][0]['target'][0], 'l19 s0 mean 60')
ck(sum(60 - d for d in days if d < 60) == 300 == sum(d - 60 for d in days if d > 60), 'l19 s0 distances 300 and 300')
ck(sum(40 - d for d in days if d < 40) < sum(d - 40 for d in days if d > 40), 'l19 s0 at 40 the distance above is bigger')
tok = {t['id']: int(t['text'].replace('−', '-').replace('£', '')) for t in S[1]['widget']['tokens']}
ck([tok[i] for i in S[1]['widget']['order']] == sorted(days), 'l19 s1 sorted order')
ck(median(days) == 40 and max(set(days), key=days.count) == 40 and S[3]['widget']['answer'] == max(days) - min(days) == 380, 'l19 s2/s3 median 40, mode 40, range 380')
big = [3100 if d == 300 else d for d in days]
ck((cell(S[4], 0, 1)['answer'], cell(S[4], 1, 1)['answer']) == (F(sum(big), 7), median(big)) == (460, 40) and max(big) - min(big) == 3180, 'l19 s4 mean 460, median 40; range 3,180')
ck(S[5]['widget']['answer'] == median([3, 5, 8, 10]) == 6.5, 'l19 s5 median 6.5')
freq = {0: 2, 1: 5, 2: 8, 3: 4, 4: 1}
xs = [v for v, n in freq.items() for _ in range(n)]
ck([cell(S[6], r, 1)['answer'] for r in range(4)] == [sum(xs), sum(xs) / len(xs), median(xs), max(freq, key=freq.get)] == [37, 1.85, 2, 2] and len(xs) == 20, 'l19 s6 frequency table 37, 1.85, 2, 2')
print('note (finding 9, minor, wording fix only): l19 s6 the slip "median = middle row of the table" gives', median(list(freq)), 'and the key is', median(xs))
ck(S[7]['widget']['answer'] == 5 * 60 - (120 - 80 + 40 + 40) == 180, 'l19 s7 Friday 180')
ck(S[8]['widget']['answer'] == F(10 * 50000 + 30 * 70000, 40) == 65000, 'l19 s8 65,000')
ck(S[9]['widget']['answer'] == 55000 / 50000 and (55000 - 45000) / (50000 - 45000) == 2, 'l19 s9 1.1 true, 2 drawn')
ck(sum(1 for d in days if d > 60) == 2, 'l19 s10 two days above the mean')
ck(sum(1 for d in big if d <= 40) == 4 and sum(1 for d in big if d <= 120) == 6, 'l19 s11 four days at 40 or less, six at 120 or less')
Q = L['l19']['quiz']
m = [2, 3, 3, 5, 7, 7, 9]
ck(sorted(v for v in set(m) if m.count(v) == 2) == [3, 7] and median(m) == 5 and round(sum(m) / 7, 2) == 5.14, 'l19 q0 two modes 3 and 7')
h = Q[1]['canvas']['params']['data']
bins = [sum(1 for v in h if lo <= v < lo + 100) for lo in range(0, 500, 100)]
ck(len(h) == 14 and bins == [2, 3, 6, 2, 1] and max(h) == 410, 'l19 q1 histogram counts 2, 3, 6, 2, 1')
p5 = [-20, 50, 10, -40, 100]
ck(Q[2]['widget']['answer'] == sum(p5) / 5 == 20 and wr(Q[2]['widget'])['ignored-signs'] == sum(map(abs, p5)) / 5, 'l19 q2 mean 20')
p4 = [-15, 40, -30, 25]
ck(Q[3]['widget']['answer'] == max(p4) - min(p4) == 70, 'l19 q3 range 70')
ck(wr(Q[3]['widget'])['first-last'] == abs(p4[-1] - p4[0]), f'l19 q3 wrong first-last: "first and last values listed" gives {abs(p4[-1] - p4[0])}, the entry holds {wr(Q[3]["widget"])["first-last"]}', 'W2')

# ---------- review ----------
I = L['rev']['items']
ck(pf(180) == [2, 2, 3, 3, 5] and I[1]['widget']['answer'] == len(factors(180)) == 18 and wr(I[1]['widget']) == {'no-plus-one': 4, 'added': 8}, 'review 180: primes, 18 factors')
ck(venn_ok(I[2]['canvas']['params'], 36, 60) and I[2]['widget']['answer'] == lcm(36, 60) == 180 and hcf(36, 60) == 12 and 36 * 60 == 2160, 'review LCM 180')
ck(F(30, 42) == F(5, 7) and hcf(30, 42) == 6, 'review 30/42')
ck(shoelace(I[4]['canvas']['state']['polygons'][0]['points']) == I[4]['widget']['answer'] == 34, 'review L-shape 34 by shoelace')
ck(I[5]['widget']['answer'] == F(12 * 7, 2) == 42 and 7 < 9, 'review triangle 42 (height 7 below slant 9)')
ck(I[6]['widget']['answer'] == round(49 * pi, 2) and wr(I[6]['widget']) == {'diameter': round(196 * pi, 2), 'circ': round(14 * pi, 2)}, 'review circle 153.94')
ck(I[7]['widget']['answer'] == F(54000, 3600) == 15 and wr(I[7]['widget'])['wrong-way'] == 54 * 3.6, 'review 54 km/h')
fx = [v for v, n in {0: 3, 1: 4, 2: 2, 3: 1}.items() for _ in range(n)]
ck(I[8]['widget']['answer'] == sum(fx) / len(fx) == 1.1 and len(fx) == 10, 'review frequency mean 1.1')
ck(I[9]['widget']['answer'] == F(6 * 50 - 110, 5) == 38, 'review removed day 38')
ck(all(2 <= i['difficulty'] <= 4 for i in I) and 6 <= len(I) <= 10 and L['rev']['pass'] == 0.8, 'review counts: 6 to 10 items, difficulty 2 to 4, pass 0.8')

# ---------- homework ----------
H = L['hw']['items']
ck(pf(126) == [2, 3, 3, 7] and pf(90) == [2, 3, 3, 5] and H[0]['parts'][1]['widget']['answer'] == hcf(90, 126) == 18 and H[0]['parts'][2]['widget']['answer'] == lcm(90, 126) == 630 and 90 * 126 == 11340, 'hw 90 and 126')
ck(H[1]['parts'][0]['widget']['answer'] == round(60 + pi * 9 / 2, 2) and H[1]['parts'][1]['widget']['answer'] == round(26 + 3 * pi, 2), 'hw lawn 74.14 and 35.42')
ck(wr(H[1]['parts'][0]['widget']) == {'full-circle': round(60 + 9 * pi, 2), 'diameter': round(60 + 18 * pi, 2), 'rect': 60} and wr(H[1]['parts'][1]['widget']) == {'shared': round(32 + 3 * pi, 2), 'full': round(26 + 6 * pi, 2), 'no-arc': 26}, 'hw lawn slips')
ck(H[2]['widget']['answer'] == F(25 * 3600, 1000) == 90, 'hw 25 m/s = 90 km/h')
hx = [v for v, n in {1: 3, 2: 6, 3: 7, 4: 4}.items() for _ in range(n)]
ck(H[3]['parts'][0]['widget']['answer'] == sum(hx) / len(hx) == 2.6 and H[3]['parts'][1]['widget']['answer'] == median(hx) == 3 and len(hx) == 20, 'hw frequency mean 2.6, median 3')
ck(H[4]['widget']['answer'] == F(8 * 45000 - 94000, 7) == 38000, 'hw leaver 38,000')
a, b, rem = 1071, 462, []
while b: rem.append(a % b); a, b = b, a % b
ck(rem == [147, 21, 0] and hcf(1071, 462) == 21 and lcm(1071, 462) == 23562 and (1071 // 21, 462 // 21) == (51, 22), 'hw Euclid 147, 21, 0; LCM 23,562')
ck(math.gcd(609, 462) != 21 or 'leaves 609' not in [l for l in H[5]['widget']['lines'] if l['id'] == 'bad'][0]['text'], 'hw Euclid distractor "take away one 462, carry on with 462 and 609" is a true line that still reaches 21 (gcd(609, 462) = 21), yet is marked as not following', 'U-euclid')
mo = [18, 22, 20, 19, 21, 20, 23, 17, 20, 22, 18, 200]
ck(sum(mo) == 420 and F(sum(mo), 12) == 35 and median(mo) == 20 and F(sum(mo) - 200, 11) == 20 and sorted(mo)[:11][-1] == 23, 'hw leaflet: total 420, mean 35, median 20, eleven average 20')
ck(F(23, 20) == F(115, 100) and F(23 - 15, 20 - 15) == F(8, 5), 'hw leaflet: 23 against 20 is 1.15 times; drawn 8 against 5 is 1.6 times')
ck(sum(r['points'] for r in H[6]['rubric']) == 10, 'hw longform rubric is 10 points')
ck('%' not in H[6]['model'], 'hw leaflet model uses per cent ("15%", "60%"), not taught until ratio level 1', 'U-percent')
ck(H[7]['widget']['answer'] == len(factors(2520)) == 48 and math.lcm(*range(1, 11)) == 2520 and pf(2520) == [2, 2, 2, 3, 3, 5, 7], 'hw 2,520: 48 factors, lcm of 1..10')
ck(6 <= len(H) <= 12 and all(3 <= i['difficulty'] <= 5 for i in H) and any(i['difficulty'] == 5 for i in H), 'hw counts: 6 to 12 items, difficulty 3 to 5, one 5')

bad = [r for r in res if not r[0]]
print(f'\nread-numbers: {len(res) - len(bad)} of {len(res)} checks passed; {len(bad)} failing, all findings: {sorted(str(r[2]) for r in bad)}')
sys.exit(1 if bad else 0)
