#!/usr/bin/env python3
"""Concept audit checks, mm-games level 1 (l1 to l4, review-1, homework-1).

Exits 0 when the content is correct. A check that fails because the content
is wrong is marked EXPECTED_FAIL: it is listed, the corrected assert sits in a
comment beside it, and it does not change the exit code.
Run from the repo root: python3 docs/reports/mm-games-L1-concepts.py
"""
import json, math, os, random, sys
from fractions import Fraction as F
from itertools import product
from math import comb, isclose, sqrt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'mm-games')
FAILS, XFAILS, PASSES = [], [], [0]


def check(name, cond, expected_fail=False):
    if cond:
        PASSES[0] += 1
        if expected_fail:
            print(f'NOTE  {name}: marked EXPECTED_FAIL but passes (content fixed?)')
    elif expected_fail:
        XFAILS.append(name); print(f'EXPECTED_FAIL  {name}')
    else:
        FAILS.append(name); print(f'FAIL  {name}')


def load(name):
    return json.load(open(os.path.join(CDIR, name + '.json')))


def run_code_widget(label, w):
    """Solution passes every example and hidden test in CPython; starter fails."""
    def run(src):
        ok = 0; cases = w.get('examples', []) + w['tests']
        for c in cases:
            ns = {}
            try:
                exec(w.get('prelude', '') + '\n' + src, ns)
                if c.get('setup'): exec(c['setup'], ns)
                got = eval(c['call'], ns); exp = eval(str(c['expect']), ns)
                mode = c.get('compare', 'equal')
                if mode == 'isclose':
                    rel = (c.get('tol') or {}).get('rel', 1e-9)
                    good = isclose(float(got), float(exp), rel_tol=rel, abs_tol=1e-12)
                elif mode == 'fraction':
                    good = isinstance(got, (F, int)) and F(got) == F(exp)
                else:
                    good = got == exp
            except Exception:
                good = False
            ok += bool(good)
        return ok, len(cases)
    ok, n = run(w['solution'])
    check(f'{label}: solution passes {ok}/{n}', ok == n)
    ok2, _ = run(w['starter'])
    check(f'{label}: starter fails', ok2 < n)


def dice_pmf(n):
    pmf = {}
    for r in product(range(1, 7), repeat=n):
        pmf[sum(r)] = pmf.get(sum(r), 0) + F(1, 6 ** n)
    return pmf


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


# ---------- l1: counting and calibration ----------
digits = lambda n: sum(len(str(i)) for i in range(1, n + 1))
check('l1 digits 1..300 = 792', digits(300) == 792)
check('l1 digits 1..1000 = 2893', digits(1000) == 2893)
check('l1 digits 1..500 = 1392', digits(500) == 1392)
check('l1 3n-108 on 100..999', all(digits(n) == 3 * n - 108 for n in range(100, 1000)))
check('l1 digits 10000 = 38894', digits(10000) == 38894)
squares = lambda n: sum((n + 1 - k) ** 2 for k in range(1, n + 1))
check('l1 squares 8x8 = 204, 4x4 = 30', squares(8) == 204 and squares(4) == 30)
check('l1 rectangles = 1296', comb(9, 2) ** 2 == 1296)
truths = [792, 204, 365 * 86400, 7 * 24 * 60, 366 * 24, comb(52, 5), math.factorial(8), 2893, comb(30, 2), 1296]
check('l1 table truths', truths == [792, 204, 31536000, 10080, 8784, 2598960, 40320, 2893, 435, 1296])
iv = [(500, 900), (64, 150), (30e6, 35e6), (8000, 12000), (8000, 9000), (1e5, 1e6), (1000, 50000), (2500, 3500), (400, 500), (200, 1000)]
miss = [i for i, ((lo, hi), t) in enumerate(zip(iv, truths)) if not lo <= t <= hi]
check('l1 misses are rows 1, 5, 9 and all above the high end', miss == [1, 5, 9] and all(truths[i] > iv[i][1] for i in miss))
p9 = F(9, 10)
check('l1 P(hits<=7 of 10 at 0.9) about 7%', abs(float(binom_cdf(7, 10, p9)) - 0.0702) < 5e-4)
check('l1 P(0 misses in 20) about 12%', abs(0.9 ** 20 - 0.1216) < 5e-4)
check('review-1 P(hits<=38 of 50) about 0.0032', abs(float(binom_cdf(38, 50, p9)) - 0.0032) < 1e-4)
# Monte Carlo of the calibration reading: calibrated 90% ranges, 10 at a time
rng = random.Random(11); N = 200000
low7 = sum(sum(rng.random() < 0.9 for _ in range(10)) <= 7 for _ in range(N)) / N
check('l1 sim: 7 or fewer hits in 10 happens about 7% of the time', abs(low7 - 0.0702) < 0.003)
# 7 of 10 does not reject calibration at 5% (homework-1 returns 'calibrated' for it); l1 s4 calls it overconfident outright
# (corrected claim, fix pass) l1 s4 now calls 7 of 10 "a warning, not proof"; P(hits <= 7) = 0.0702 > 0.05
check('l1 s4: 7 of 10 is a warning, not proof: P(hits <= 7) = 0.070 > 0.05  (corrected claim, fix pass)',
      float(binom_cdf(7, 10, p9)) > 0.05 and abs(float(binom_cdf(7, 10, p9)) - 0.0702) < 5e-4
      and 'warning, not proof' in load('l1-unknown-quantity')['screens'][4]['explain']['text'])

# ---------- l2: dice fair values ----------
E = lambda fn, n: F(sum(fn(r) for r in product(range(1, 7), repeat=n)), 6 ** n)
check('l2 E one, two, three dice', (E(sum, 1), E(sum, 2), E(sum, 3)) == (F(7, 2), 7, F(21, 2)))
p3 = dice_pmf(3)
check('l2 three-dice bars', [round(float(p3[k]), 4) for k in range(3, 11)] == [0.0046, 0.0139, 0.0278, 0.0463, 0.0694, 0.0972, 0.1157, 0.125])
check('l2 sixes contract = 5', E(lambda r: 10 * r.count(6), 3) == 5)
check('l2 at least one six = 10*91/216', abs(10 * 91 / 216 - 4.213) < 1e-3)
check('l2 max of two = 161/36, min = 91/36', E(max, 2) == F(161, 36) and E(min, 2) == F(91, 36))
check('l2 E[X^2] = 91/6, gap = Var = 35/12', E(lambda r: r[0] ** 2, 1) == F(91, 6) and F(91, 6) - F(49, 4) == F(35, 12))
check('l2 sds', all(abs(sqrt(n * 35 / 12) - v) < 5e-5 for n, v in [(1, 1.7078), (2, 2.4152), (3, 2.9580), (100, 17.0783)]))
check('l2 added sds 3.4157, 5.1235', abs(2 * sqrt(35 / 12) - 3.4157) < 1e-4 and abs(3 * sqrt(35 / 12) - 5.1235) < 1e-4)
# "multiplying fair values works only for independent dice": an uncorrelated but dependent pair also multiplies.
# X uniform on {-1, 0, 1}, Y = X^2: E[XY] = E[X^3] = 0 = E[X]E[Y], yet Y is a function of X.
xs = [-1, 0, 1]
# (corrected claim, fix pass) l2 s5 now says multiplying is "safe for independent dice": sufficient, and the dependent pair shows it is not necessary
l2c = load('l2-dice-sum')
check('l2 s5: independence is sufficient for E[XY] = E[X]E[Y]; a dependent pair can also multiply  (corrected claim, fix pass)',
      F(sum(x ** 3 for x in xs), 3) == F(sum(xs), 3) * F(sum(x * x for x in xs), 3)
      and 'only' not in l2c['screens'][5]['explain']['text'] and 'only' not in l2c['summary']['ideas'][2]
      and 'only' not in l2c['screens'][5]['feedback']['byKey']['product-of-means'])
# 100 dice: share within 350 +- 17, exact by convolution
pm = {0: F(1)}
for _ in range(100):
    nx = {}
    for s, p in pm.items():
        for f in range(1, 7):
            nx[s + f] = nx.get(s + f, 0) + p / 6
    pm = nx
share = float(sum(p for s, p in pm.items() if abs(s - 350) <= 17))
check(f'l2 100 dice: 350 +- 17 holds about two thirds (exact {share:.4f})', 0.64 < share < 0.71)
check('l2 quiz first die 6 -> 13', 6 + E(sum, 2) == 13)
check('l2 trade: sell 2 at 11.50 vs 10.50 = +2; settle 14 = -5', 2 * (11.5 - 10.5) == 2 and 2 * (11.5 - 14) == -5)
run_code_widget('l1 s9 code', load('l1-unknown-quantity')['screens'][9]['widget'])
run_code_widget('l2 s9 code', load('l2-dice-sum')['screens'][9]['widget'])

# ---------- l3: width ----------
p2 = dice_pmf(2)
cov2 = lambda lo, hi: sum(p for s, p in p2.items() if lo <= s <= hi)
cov3 = lambda lo, hi: sum(p for s, p in p3.items() if lo <= s <= hi)
check('l3 coverages two dice', (cov2(6, 8), cov2(5, 9), cov2(4, 10)) == (F(4, 9), F(2, 3), F(5, 6)))
check('l3 formula 1-(6-k)(5-k)/36 for k=0..5', all(cov2(7 - k, 7 + k) == 1 - F((6 - k) * (5 - k), 36) for k in range(6)))
check('l3 off-centre width 2 holds 15', cov2(5, 7) == cov2(7, 9) == F(15, 36) and cov2(4, 8) == F(23, 36))
check('l3 three dice: 10..11 quarter, 9..12 = 13/27, 8..13 = 73/108', (cov3(10, 11), cov3(9, 12), cov3(8, 13)) == (F(1, 4), F(13, 27), F(73, 108)))
check('l3 7 +- 2.42 holds 5..9', cov2(math.ceil(7 - 2.4152), math.floor(7 + 2.4152)) == F(2, 3))
# "a range should sit on the fair value, where the chance is densest": false for a skewed payout (max of two dice)
pmx = {}
for r in product(range(1, 7), repeat=2):
    pmx[max(r)] = pmx.get(max(r), 0) + F(1, 36)
best = max(((lo, lo + 1) for lo in range(1, 6)), key=lambda q: pmx[q[0]] + pmx[q[1]])
# (corrected claim, fix pass) l3 s3 now ties "fair value = densest" to the symmetric two-dice total only
cnt2 = {}
for r in product(range(1, 7), repeat=2):
    cnt2[sum(r)] = cnt2.get(sum(r), 0) + 1
win = {c: cnt2.get(c - 1, 0) + cnt2.get(c, 0) + cnt2.get(c + 1, 0) for c in range(3, 12)}
check('l3 s3: fair value is densest only for a symmetric total (two dice: centre 7 holds 16, 6 or 8 hold 15); larger of two dice fair 4.47, densest 5 to 6  (corrected claim, fix pass)',
      best == (5, 6) and float(E(max, 2)) < 5 and max(win, key=win.get) == 7 and win[7] == 16 and win[6] == win[8] == 15
      and 'symmetric' in load('l3-how-wide')['screens'][3]['explain']['text'])


def toy_profit(h):
    loss = sum(2 * F(6 - d, 36) * max(d - h, 0) for d in range(1, 6))
    return 0.5 * h * max(0, 1 - h / 4) - 0.5 * float(loss)


check('l3 toy game: profit(0) about -0.97, profit(1) about -0.18, profit(2.5) about 0.27',
      abs(toy_profit(0) + 0.972) < 2e-3 and abs(toy_profit(1) + 0.181) < 2e-3 and abs(toy_profit(2.5) - 0.274) < 2e-3)
grid = [i / 100 for i in range(0, 501)]
hbest = max(grid, key=toy_profit)
check(f'l3 toy game: peak near h = 2.7, about 0.28 (found h = {hbest}, {toy_profit(hbest):.3f})', abs(hbest - 2.67) < 0.02 and abs(toy_profit(hbest) - 0.278) < 2e-3)
check('l3 toy game: profit(5) = 0', toy_profit(5) == 0)
# Monte Carlo of the toy game as the prose states it
rng = random.Random(5)


def toy_sim(h, n=200000):
    tot = 0.0
    for _ in range(n):
        s = rng.randint(1, 6) + rng.randint(1, 6)
        if rng.random() < 0.5:
            tot -= max(abs(s - 7) - h, 0)
        elif rng.random() < max(0, 1 - h / 4):
            tot += h
    return tot / n


check('l3 toy game sim matches the curve at h = 1 and h = 2.7', abs(toy_sim(1) - toy_profit(1)) < 0.01 and abs(toy_sim(2.7) - toy_profit(2.7)) < 0.01)
check('l3 both sides trade: +2', (10.5 - 9.5) + (11.5 - 10.5) == 2)
check('l3 results day half-width 0.60', abs(0.03 * 20 - 0.6) < 1e-12)
run_code_widget('l3 s10 code', load('l3-how-wide')['screens'][10]['widget'])

# ---------- l4: Fermi ----------
check('l4 pool', 50 * 25 * 2 * 1000 == 2500000)
check('l4 desk 80,000; low 10,000; high 640,000', (500 * 20 * 8, 250 * 10 * 4, 1000 * 40 * 16) == (80000, 10000, 640000))
check('l4 487*23*8.5 = 95208.5', 487 * 23 * 8.5 == 95208.5)
check('l4 quiz minutes', 252 * 8.5 * 60 == 128520 and 365 * 8.5 * 60 == 186150)
check('l4 heartbeats', 70 * 60 * 24 * 365 * 80 == 2943360000)
check('l4 80,000 nearest power of ten is 10^5', round(math.log10(80000)) == 5)
# Worst case versus typical error of a product.
# Each factor's log error independent and normal, with its 90% range a factor of 2 either way.
rng = random.Random(3); z90 = 1.6448536269514722; sig = math.log(2) / z90
logs = sorted(abs(sum(rng.gauss(0, sig) for _ in range(3))) for _ in range(200000))
f90 = math.exp(logs[int(0.9 * len(logs))])
inside8 = sum(l <= math.log(8) for l in logs) / len(logs)
print(f'      l4: three independent factors each 90% within x2: product 90% within x{f90:.2f}; x8 holds {inside8:.4f}')
check('l4 sim: independent errors give about a factor 2^sqrt(3) = 3.3 at 90%', abs(f90 - 2 ** sqrt(3)) < 0.08)
# (corrected claim, fix pass) l4 s4/s5 now call 8 the worst case and about 3 the usual factor
l4c = load('l4-fermi')
check('l4 s4/s5: 8 is the worst case; independent errors give about x3.3 at 90% and x8 holds over 99%  (corrected claim, fix pass)',
      inside8 > 0.99 and abs(f90 - 3.32) < 0.1 and 'at worst' in l4c['screens'][5]['explain']['text']
      and 'same way' in l4c['screens'][4]['explain']['text'] and 'about 3' in l4c['screens'][5]['explain']['text'])
run_code_widget('l4 s9 code', load('l4-fermi')['screens'][9]['widget'])
check('l4 trade +30; transfer 400', 3 * (90 - 80) == 30 and 40 * 5 * 2 == 400)

# ---------- review-1 ----------
check('r1 sevens in 1..100 = 20', sum(str(i).count('7') for i in range(1, 101)) == 20)
check('r1 gap of two dice = 35/18', E(lambda r: abs(r[0] - r[1]), 2) == F(35, 18))
check('r1 max of three = 119/24; six is largest in 91/216', E(max, 3) == F(119, 24) and 216 - 125 == 91)
check('r1 scaled sd 24.15', abs(10 * sqrt(35 / 6) - 24.15) < 5e-3)
check('r1 +-24 on 10*(S-7) holds 2/3', sum(p for s, p in p2.items() if abs(10 * (s - 7)) <= 24) == F(2, 3))
check('r1 coins: 160000/2.3 about 70,000; 1609.344/0.02303 = 69,880, about 69,900 (fix pass)', round(160000 / 2.3, -4) == 70000 and round(1609.344 / 0.02303) == 69880)
# The 12-sided pound coin (in use since 2017) is 23.43 mm corner to corner, 23.03 mm edge to edge (Royal Mint specification).
# 22.5 mm was the round pound, withdrawn in October 2017.
# (corrected claim, fix pass) review-1 now uses the 12-sided coin across its flats, 23.03 mm (Royal Mint), since coins laid edge to edge touch flat to flat
r1x = load('review-1')['items'][7]['explain']['text']
check('r1 coins: 12-sided coin 2.303 cm across the flats gives 69,880, about 69,900 (across the corners, 2.343 cm, would give 68,687)  (corrected claim, fix pass)',
      round(160934.4 / 2.303) == 69880 and round(160934.4 / 2.303, -2) == 69900 and round(160934.4 / 2.343) == 68687
      and '2.303 cm' in r1x and '69,900' in r1x and '2.25' not in r1x)
check('r1 error factor 18', 2 * 2 * 1.5 * 3 == 18)
check('r1 chess ledger +36', 2 * (220 - 204) + (204 - 200) == 36)
for label, fn, n, quoted in [('gap', lambda a: abs(a[0] - a[1]), 2, 1.945), ('max3', max, 3, 4.958)]:
    r = random.Random(1); m = sum(fn([r.randint(1, 6) for _ in range(n)]) for _ in range(200000)) / 200000
    check(f'r1 sim {label} with Random(1): {m:.4f} within 0.004 of the quoted {quoted}', abs(m - quoted) < 0.004)

# ---------- homework-1 ----------
hw = load('homework-1')
run_code_widget('hw1 dice_market', hw['items'][0]['widget'])
run_code_widget('hw1 calibration_score', hw['items'][1]['widget'])
pmf50 = [comb(50, k) * p9 ** k * (1 - p9) ** (50 - k) for k in range(51)]
check('hw1 50 of 50 two-sided p about 0.008', abs(float(sum(q for q in pmf50 if q <= pmf50[50])) - 0.00837) < 1e-4)
check('hw1 14 of 20 p about 0.011', abs(float(binom_cdf(14, 20, p9)) - 0.01125) < 1e-4)
check('hw1 digit sum 1..100 = 901', sum(sum(map(int, str(i))) for i in range(1, 101)) == 901)
check('hw1 distinct faces 91/36, three distinct 120/216', E(lambda r: len(set(r)), 3) == F(91, 36) and 6 * 5 * 4 == 120)
r = random.Random(1); m = sum(len({r.randint(1, 6) for _ in range(3)}) for _ in range(200000)) / 200000
check(f'hw1 sim distinct faces {m:.4f} near 2.528', abs(m - 2.528) < 0.004)
check('hw1 fermi low 1,000,000 high 36,000,000', (1000 * 1000, 4000 * 9000) == (1000000, 36000000))
check('hw1 ledger: +4 at 7, +8 at 9', 3 * (7 - 6) + (8 - 7) == 4 and 3 * (9 - 6) + (8 - 9) == 8)
prod_pays = [a * b for a in range(1, 7) for b in range(1, 7)]
mu = sum(prod_pays) / 36; sdp = sqrt(sum((x - mu) ** 2 for x in prod_pays) / 36)
print(f'      hw1: product of two dice has sd {sdp:.2f}')
# (corrected claim, fix pass) hw1 now says the product is too spread out around 12.25, sd about 8.9.
# Widest allowed quote around centre 12.5 is 8 to 17, which holds only 14 of 36 rolls.
in817 = sum(1 for x in prod_pays if 8 <= x <= 17)
check('hw1 explain: the product of two dice is too spread out around 12.25 (sd 8.94); 8 to 17 holds 12 of 36  (corrected claim, fix pass)',
      8.9 < sdp < 9.0 and mu == 12.25 and in817 == 12 and 'spread out' in load('homework-1')['items'][0]['explain']['text'])
check('hw1 mock model: running totals and +26', [sum((9 - k) ** 2 for k in range(1, j + 1)) for j in range(1, 9)] == [64, 113, 149, 174, 190, 199, 203, 204] and 230 - 204 == 26)

print(f'\n{PASSES[0]} checks passed, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL')
for x in XFAILS:
    print('  EXPECTED_FAIL:', x)
sys.exit(1 if FAILS else 0)
