#!/usr/bin/env python3
"""Concept audit round 2, mm-games level 1 (l1 to l4, review-1, homework-1).
Recomputes every computable claim independently of the author scripts and runs every
code solution against its hidden tests. Exits 0 when the content is correct."""
import json, math, os, random, sys
from fractions import Fraction as F
from itertools import product
from math import comb

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
C = os.path.join(ROOT, 'app', 'content', 'courses', 'mm-games')
def load(name): return json.load(open(os.path.join(C, name + '.json')))
fails, count, notes = [], 0, []
def ok(cond, label):
    global count
    count += 1
    if not cond:
        fails.append(label); print('FAIL', label)
def close(a, b, tol=1e-9): return abs(float(a) - float(b)) <= tol
def _cmp(a, e, kind, tol):
    if kind == 'fraction': return isinstance(a, F) and a == e
    if kind == 'isclose':
        rt, at = ((tol.get('rel', 0) or 0, tol.get('abs', 0) or 0) if tol else (1e-9, 1e-12))
        def cl(x, y):
            if isinstance(x, (list, tuple)):
                return isinstance(y, (list, tuple)) and len(x) == len(y) and all(cl(p, q) for p, q in zip(x, y))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        return cl(a, e)
    fl = lambda x: [fl(i) for i in x] if isinstance(x, (list, tuple)) else x
    return fl(a) == fl(e)
def run_cases(src, w):
    out = []
    for c in w.get('examples', []) + w['tests']:
        g = {}
        try:
            exec(w.get('prelude', '') + '\n' + src, g)
            if c.get('setup'): exec(c['setup'], g)
            out.append(bool(_cmp(eval(c['call'], g), eval(str(c['expect']), g), c.get('compare', 'equal'), c.get('tol'))))
        except Exception:
            out.append(False)
    return out
def code(w, label):
    ok(all(run_cases(w['solution'], w)), label + ': solution passes every example and hidden test')
    ok(not all(run_cases(w['starter'], w)), label + ': starter fails')
    import re
    stated = re.search(r'Check runs (\d+) hidden tests', w.get('how', ''))
    ok(stated is None or int(stated.group(1)) == len(w['tests']), label + ': the stated number of hidden tests is right')
def binom_cdf(k, n, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))
def dist(n):
    d = {}
    for r in product(range(1, 7), repeat=n): d[sum(r)] = d.get(sum(r), 0) + 1
    return d

l1, l2, l3, l4 = load('l1-unknown-quantity'), load('l2-dice-sum'), load('l3-how-wide'), load('l4-fermi')
r1, h1 = load('review-1'), load('homework-1')
S1, S2, S3, S4 = l1['screens'], l2['screens'], l3['screens'], l4['screens']

# ---------- l1 ----------
digits = lambda n: sum(len(str(i)) for i in range(1, n + 1))
rows = S1[1]['widget']['rows']
ok([rows[1][2]['answer'], rows[2][1]['answer'], rows[2][2]['answer'], rows[3][2]['answer']] == [180, 201, 603, digits(300)], 'l1 s1 digit table')
squares = lambda n: sum((n + 1 - k) ** 2 for k in range(1, n + 1))
rw = S1[2]['widget']['rows']
ok([rw[2][1]['answer'], rw[7][1]['answer'], rw[8][1]['answer']] == [36, 1, squares(8)], 'l1 s2 chessboard squares')
truths = {0: digits(300), 1: squares(8), 2: 365 * 86400, 3: 7 * 24 * 60, 4: 366 * 24, 5: comb(52, 5),
          6: math.factorial(8), 7: digits(1000), 8: comb(30, 2), 9: comb(9, 2) ** 2}
iv = [(500, 900), (64, 150), (30e6, 35e6), (8000, 12000), (8000, 9000), (1e5, 1e6), (1000, 50000), (2500, 3500), (400, 500), (200, 1000)]
tab = S1[3]['canvas']['params']['rows']
ok(all(int(tab[i][2].replace(',', '')) == truths[i] for i in range(10)), 'l1 s3 the ten truths are exact')
miss = ['r%d' % i for i in range(10) if not (iv[i][0] <= truths[i] <= iv[i][1])]
ok(sorted(S1[3]['widget']['answer']) == sorted(miss), 'l1 s3 rows that miss')
ok(close(S1[4]['widget']['answer'], 1 - len(miss) / 10), 'l1 s4 hit rate')
p7 = binom_cdf(7, 10, 0.9)
ok(0.065 < p7 < 0.075 and 'about 7%' in S1[4]['explain']['text'], 'l1 s4 P(7 or fewer of 10 at 0.9) is about 7%% (%.4f)' % p7)
ok(S1[7]['widget']['answer'] == 20 * 0.1 and 0.115 < 0.9 ** 20 < 0.125 and 'about 12%' in S1[7]['explain']['text'], 'l1 s7 two misses; zero misses in 20 about 12%')
ok(all(3 * n - 108 == digits(n) for n in range(100, 1000)) and S1[8]['widget']['answer'] == '3n-108', 'l1 s8 3n-108 for every three-digit n')
ok(3 * 98 - 108 != digits(98) and 3 * 1000 - 108 != digits(1000), 'l1 s8 the formula fails below 99 and above 999, so a stated range is needed')
code(S1[9]['widget'], 'l1 s9')
ok(S1[10]['widget']['answer'] == 850 - digits(300), 'l1 s10 seller P&L = price - value')
q = l1['quiz']
ok(q[0]['widget']['answer'] == digits(500) and q[2]['widget']['answer'] == squares(4) and q[3]['widget']['answer'] == 365 * 86400, 'l1 quiz keys')
ok(q[0]['widget']['wrong'][0]['value'] == 189 + 3 * 400, 'l1 quiz fence slip')

# ---------- l2 ----------
def ev(fn, n):
    rolls = list(product(range(1, 7), repeat=n)); return F(sum(fn(r) for r in rolls), len(rolls))
ok(close(S2[0]['widget']['answer'], ev(sum, 1)) and close(S2[2]['widget']['answer'], ev(sum, 3)), 'l2 one and three dice fair values')
d3 = dist(3)
ok(d3[10] == 27 == d3[11] and max(d3.values()) == 27, 'l2 s2 10 and 11 each have 27 ways and are the modes')
ok(close(S2[3]['widget']['answer'], ev(lambda r: 10 * r.count(6), 3)), 'l2 s3 sixes contract')
ok(close(S2[3]['widget']['wrong'][0]['value'], 10 * (1 - F(5, 6) ** 3), 0.01), 'l2 s3 at-least-one slip 10 x 91/216')
six = [sum(1 for r in product(range(1, 7), repeat=3) if r.count(6) == k) for k in range(4)]
ok(six == [125, 75, 15, 1], 'l2 s3 bars 75, 15, 1')
ok(close(S2[4]['widget']['answer'], ev(max, 2), 5e-5) and ev(max, 2) == F(161, 36), 'l2 s4 larger of two = 161/36')
ok(all(sum(1 for r in product(range(1, 7), repeat=2) if max(r) == k) == 2 * k - 1 for k in range(1, 7)), 'l2 s4 larger is k in 2k-1 rolls')
ok(close(S2[5]['widget']['answer'], ev(lambda r: r[0] ** 2, 1), 5e-5), 'l2 s5 one die squared = 91/6')
var1 = ev(lambda r: r[0] ** 2, 1) - ev(sum, 1) ** 2
ok(var1 == F(35, 12) and ev(lambda r: r[0] ** 2, 1) - ev(lambda r: r[0] * r[1], 2) == var1, 'l2 s5 gap 91/6 - 49/4 is one die variance 35/12')
t = S2[6]['widget']['rows']
def var_sum(n):
    d = dist(n); tot = 6 ** n; m = sum(k * v for k, v in d.items()) / tot
    return sum(v * (k - m) ** 2 for k, v in d.items()) / tot
ok(close(t[1][1]['answer'], var_sum(2), 1e-4) and close(t[1][2]['answer'], math.sqrt(var_sum(2)), 1e-4) and close(t[2][1]['answer'], var_sum(3), 1e-4) and close(t[2][2]['answer'], math.sqrt(var_sum(3)), 1e-4), 'l2 s6 variance and sd by enumeration (variances add)')
ok(close(2 * math.sqrt(35 / 12), 3.4157, 1e-4) and close(3 * math.sqrt(35 / 12), 5.1235, 1e-4), 'l2 s6 added-sd slips')
# 100 dice: exact distribution by convolution
p = {0: F(1)}
for _ in range(100):
    nxt = {}
    for s, v in p.items():
        for f in range(1, 7): nxt[s + f] = nxt.get(s + f, 0) + v / 6
    p = nxt
m100 = sum(s * v for s, v in p.items()); sd100 = math.sqrt(sum(v * (s - m100) ** 2 for s, v in p.items()))
inside = float(sum(v for s, v in p.items() if abs(s - 350) <= 17))
ok(m100 == 350 and close(sd100, 17.078, 1e-3), 'l2 s8 100 dice mean 350, sd 17.08')
ok(0.62 < inside < 0.72, 'l2 s8 350 +/- 17 holds about two thirds (exact %.4f)' % inside)
code(S2[9]['widget'], 'l2 s9')
ok(S2[10]['widget']['answer'] == 2 * (11.5 - 10.5) and 2 * (14 - 11.5) == 5, 'l2 s10 ledger and the 14 outcome')
q = l2['quiz']
ok(q[0]['widget']['answer'] == 6 + 7 and close(q[1]['widget']['answer'], ev(min, 2), 5e-5) and ev(min, 2) + ev(max, 2) == 7, 'l2 quiz 13, 91/36, min + max = 7')
ok(abs(math.sqrt(var_sum(4)) - 3.42) < 0.005, 'l2 quiz four dice sd 3.42')

# ---------- l3 ----------
d2 = dist(2)
cov = lambda lo, hi, d, tot: F(sum(v for k, v in d.items() if lo <= k <= hi), tot)
ok(cov(6, 8, d2, 36) == F(16, 36) and cov(5, 9, d2, 36) == F(2, 3) and cov(4, 10, d2, 36) == F(5, 6), 'l3 coverage 16/36, 24/36, 30/36')
ok(close(S3[1]['widget']['answer'], F(4, 9), 5e-5) and close(S3[2]['widget']['answer'], F(5, 6), 5e-5), 'l3 s1 s2 keys')
ok(cov(5, 7, d2, 36) == F(15, 36) == cov(7, 9, d2, 36), 'l3 s3 off-centre holds 15')
ok(cov(9.5, 11.5, d3, 216) == F(1, 4), 'l3 s4 9.5 to 11.5 holds a quarter')
# toy game: exact expected profit by enumeration, independent of the content's expression
def toy(h):
    informed = sum(v * max(abs(k - 7) - h, 0) for k, v in d2.items()) / 36
    return 0.5 * h * max(0, 1 - h / 4) - 0.5 * informed
expr = S3[5]['canvas']['params']['functions'][2]['expr']
ok(all(close(eval(expr, {'x': h / 20, 'max': max}), toy(h / 20), 1e-9) for h in range(0, 101)), 'l3 s5 profit curve equals the game described in the prose')
best = max(range(0, 5001), key=lambda i: toy(i / 1000)) / 1000
ok(close(toy(0), -35 / 36) and abs(toy(2.5) - 0.27) < 0.006 and 2.5 <= best <= 3 and abs(best - 2.667) < 0.01 and abs(toy(best) - 0.28) < 0.005 and toy(5) == 0, 'l3 s5 toy game: -0.97 at 0, 0.27 at 2.5, peak 0.28 near 2.67, 0 at 5')
# Monte Carlo of the toy game as described
rng = random.Random(20261110); N = 400000; h = 2.5; tot = 0.0
for _ in range(N):
    s = rng.randint(1, 6) + rng.randint(1, 6)
    if rng.random() < 0.5:
        tot -= max(abs(s - 7) - h, 0)
    elif rng.random() < 1 - h / 4:
        tot += h
ok(abs(tot / N - toy(2.5)) < 0.01, 'l3 s5 Monte Carlo of the toy game at h = 2.5 (%.4f vs %.4f)' % (tot / N, toy(2.5)))
ok(S3[7]['widget']['answer'] == (10.5 - 9.5) + (11.5 - 10.5), 'l3 s7 round trip earns the width')
ok(all(1 - F((6 - k) * (5 - k), 36) == cov(7 - k, 7 + k, d2, 36) for k in range(0, 6)), 'l3 s9 coverage formula for k = 0..5')
ok(cov(7 - 2.42, 7 + 2.42, d2, 36) == F(2, 3), 'l3 s8 7 +/- 2.42 holds 5 to 9')
phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
ok(abs(2 * phi(1) - 1 - 0.68) < 0.005, 'l3 s8 normal one-sd coverage 0.68')
code(S3[10]['widget'], 'l3 s10')
ok(cov(8, 13, d3, 216) == F(73, 108) and cov(9, 12, d3, 216) < F(1, 2) < cov(8, 13, d3, 216), 'l3 s10 8 to 13 is the first symmetric range past a half')
ok(close(S3[11]['widget']['answer'], 0.03 * 20) and close(0.01 * 20, 0.2) and close(S3[11]['widget']['wrong'][1]['value'], 9 * 0.2), 'l3 s11 results-day half-width')
q = l3['quiz']
ok(close(q[0]['widget']['answer'], cov(9, 12, d3, 216), 5e-5) and close(q[1]['widget']['answer'], F(4, 6), 5e-5) and cov(4, 8, d2, 36) == F(23, 36), 'l3 quiz keys')

# ---------- l4 ----------
w = S4[0]['widget']['rows']
ok(w[3][1]['answer'] == 50 * 25 * 2 and w[4][1]['answer'] == 50 * 25 * 2 * 1000, 'l4 s0 pool')
ok(S4[2]['widget']['answer'] == 500 * 20 * 8 and abs(math.log10(80000) - 5) < abs(math.log10(80000) - 4), 'l4 s2 s3 80,000 is nearest 10^5 on a log scale')
w = S4[4]['widget']['rows']
ok(w[3][1]['answer'] == 250 * 10 * 4 and w[3][3]['answer'] == 1000 * 40 * 16 and 80000 / 10000 == 8 == 640000 / 80000, 'l4 s4 low and high totals, factor 8')
ok(close(487 * 23 * 8.5, 95208.5), 'l4 s5 the candidate product')
# "If the errors are independent ... usually within a factor of about 3": Monte Carlo, each factor log-uniform in [1/2, 2]
rng = random.Random(4); N = 200000
within3 = sum(abs(sum(rng.uniform(-math.log(2), math.log(2)) for _ in range(3))) <= math.log(3) for _ in range(N)) / N
ok(within3 > 0.8, 'l4 s5 three independent factor-of-2 errors: total within a factor of 3 in %.3f of draws' % within3)
ok(S4[7]['widget']['answer'] == 2 ** 4 and S4[6]['widget']['answer'] == 0, 'l4 s6 s7 keys')
code(S4[9]['widget'], 'l4 s9')
ok(S4[10]['widget']['answer'] == 3 * (90 - 80) and S4[11]['widget']['answer'] == 40 * 5 * 2, 'l4 s10 s11 keys')
q = l4['quiz']
ok(q[0]['widget']['answer'] == 252 * 8.5 * 60 and q[0]['widget']['wrong'][1]['value'] == 365 * 8.5 * 60 and q[1]['widget']['answer'] == 12 and 70 * 60 * 24 * 365 * 80 == 2943360000, 'l4 quiz keys')

# ---------- review-1 ----------
it = r1['items']
ok(it[0]['widget']['answer'] == sum(str(i).count('7') for i in range(1, 101)), 'review-1 sevens')
p38 = binom_cdf(38, 50, 0.9)
ok(abs(p38 - 0.0032) < 0.0002, 'review-1 P(38 or fewer of 50) about 0.0032 (%.5f)' % p38)
gap = ev(lambda r: abs(r[0] - r[1]), 2); mx3 = ev(max, 3)
ok(gap == F(35, 18) and close(it[2]['widget']['answer'], gap, 5e-5) and mx3 == F(119, 24) and close(it[3]['widget']['answer'], mx3, 5e-5), 'review-1 gap 35/18 and max of three 119/24')
ok(sum(1 for r in product(range(1, 7), repeat=3) if max(r) == 6) == 91, 'review-1 largest is 6 in 91 of 216')
rng = random.Random(1); g = sum(abs(rng.randint(1, 6) - rng.randint(1, 6)) for _ in range(200000)) / 200000
rng = random.Random(1); m3 = sum(max(rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)) for _ in range(200000)) / 200000
ok(abs(g - 1.945) < 0.01 and abs(m3 - 4.958) < 0.01, 'review-1 quoted simulations are consistent (%.3f, %.3f)' % (g, m3))
notes.append('review-1 simulations with random.Random(1), randint in roll order: gap %.4f (text 1.945), max %.4f (text 4.958)' % (g, m3))
ok(abs(10 * math.sqrt(var_sum(2)) - it[4]['widget']['answer']) < 0.01 and cov(7 - 2.4, 7 + 2.4, d2, 36) == F(2, 3), 'review-1 scaled sd and +/-24 holds two thirds')
ok(close(it[5]['widget']['answer'], cov(8, 13, d3, 216), 5e-5) and it[6]['widget']['answer'] == 2, 'review-1 coverage and rumour')
ok(abs(160934.4 / 2.303 - 69900) < 100 and abs(160000 / 2.3 - 69565.2) < 0.1, 'review-1 coins in a mile')
ok(it[8]['widget']['answer'] == 2 * 2 * 1.5 * 3 and it[9]['widget']['answer'] == 2 * (220 - 204) + (204 - 200), 'review-1 error factor and ledger')

# ---------- homework-1 ----------
it = h1['items']
code(it[0]['widget'], 'homework-1 dice_market')
code(it[1]['widget'], 'homework-1 calibration_score')
# independent two-sided exact binomial p-values (sum of outcomes no more likely than the observed one)
def two_sided(k, n, p):
    pmf = [F(comb(n, i)) * F(p) ** i * (1 - F(p)) ** (n - i) for i in range(n + 1)]
    return float(sum(x for x in pmf if x <= pmf[k]))
ok(abs(two_sided(7, 10, F(9, 10)) - 0.0702) < 1e-4 and abs(two_sided(14, 20, F(9, 10)) - 0.0113) < 1e-4 and abs(two_sided(50, 50, F(9, 10)) - 0.0084) < 1e-4, 'homework-1 p-values 0.070, 0.011, 0.008')
# the product of two dice: sd and no quote within width 10 holding half the rolls
pr = [a * b for a in range(1, 7) for b in range(1, 7)]
ok(abs(math.sqrt(sum((x - 12.25) ** 2 for x in pr) / 36) - 8.9) < 0.05 and max(sum(12.5 - hh <= x <= 12.5 + hh for x in pr) for hh in (0.5, 1.5, 2.5, 3.5, 4.5)) < 18, 'homework-1 product has sd 8.9 and no quote under width 10')
ok(it[3]['widget']['answer'] == squares(8) == 8 * 9 * 17 // 6 and it[3]['widget']['wrong'][2]['value'] == comb(9, 2) ** 2, 'homework-1 chess count')
run = [64, 113, 149, 174, 190, 199, 203, 204]
ok(all(sum((9 - k) ** 2 for k in range(1, i + 2)) == run[i] for i in range(8)) and '64, 113, 149, 174, 190, 199, 203, 204' in it[4]['model'] and 230 - 204 == 26, 'homework-1 mock model running total and +26')
ok(close(it[5]['widget']['answer'], sum(sum(map(int, str(i))) for i in range(1, 101)) / 100), 'homework-1 digit sum 9.01')
dist_faces = ev(lambda r: len(set(r)), 3)
ok(dist_faces == F(91, 36) and close(it[6]['widget']['answer'], dist_faces, 5e-5) and 6 * 5 * 4 == 120, 'homework-1 distinct faces')
rng = random.Random(1); df = sum(len({rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)}) for _ in range(200000)) / 200000
ok(abs(df - 2.528) < 0.01, 'homework-1 quoted simulation consistent (%.4f)' % df)
ok(it[7]['widget']['answer'] == (2000 // 2) * (3000 // 3) and 4000 * 9000 == 36000000, 'homework-1 Fermi range')
ok(it[8]['widget']['answer'] == 3 * (7 - 6) + (8 - 7) and 3 * (9 - 6) + (8 - 9) == 8, 'homework-1 two-dice ledger 4 and 8')

for nline in notes: print('NOTE', nline)
print('mm-games L1 concepts r2: %d checks, %d failed' % (count, len(fails)))
sys.exit(1 if fails else 0)
