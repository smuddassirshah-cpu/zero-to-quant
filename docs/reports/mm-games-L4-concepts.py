#!/usr/bin/env python3
"""Concept checks for mm-games level 4 (l14 to l18, review-4, homework-4).

Blind concept audit, docs/reviews/audit-mm-games-4.md. Pure standard library.
Usage: python3 docs/reports/mm-games-L4-concepts.py
Exit 0 when every claim checked here holds. A FAIL is a content claim that is
false as stated and stays failing until the content changes. A NOTE shows a
counterexample behind an `imprecise` finding and does not change the exit code.
"""
import json, math, os, random, itertools
from fractions import Fraction as Fr
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'mm-games')
FILES = ['l14-quoting-an-interval', 'l15-arbitrage-in-a-book', 'l16-several-contracts',
         'l17-options-on-a-game', 'l18-betting-board', 'review-4', 'homework-4']
J = {f: json.load(open(os.path.join(BASE, f + '.json'), encoding='utf-8')) for f in FILES}
fails, notes, passed = [], [], [0]
random.seed(20261110)


def ok(cond, label):
    if cond:
        passed[0] += 1
    else:
        fails.append(label)
        print('FAIL', label)


def note(label):
    notes.append(label)
    print('NOTE', label)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def units(f):
    j = J[f]
    out = [('screens[%d]' % i, s) for i, s in enumerate(j.get('screens', []))]
    out += [('quiz[%d]' % i, s) for i, s in enumerate(j.get('quiz', []))]
    out += [('items[%d]' % i, s) for i, s in enumerate(j.get('items', []))]
    return out


def ans(f, path):
    return dict(units(f))[path]['widget']['answer']


def key(f, path, value, tol=None):
    """The graded key equals an independent recomputation, to its own tolerance."""
    w = dict(units(f))[path]['widget']
    t = tol if tol is not None else max((w.get('tol') or {}).get('abs', 0), 1e-9)
    ok(close(w['answer'], value, t), '%s %s key %r vs recomputed %r' % (f, path, w['answer'], value))


# ---------------------------------------------------------------- 0. generic
# No wrong[] slip value may sit inside the tolerance of the key.
for f in FILES:
    for path, s in units(f):
        w = s.get('widget') or {}
        if w.get('kind') == 'numeric':
            t = (w.get('tol') or {}).get('abs', 0)
            for x in w.get('wrong', []):
                if 'value' in x:
                    tx = (x.get('tol') or {}).get('abs', 0)
                    ok(abs(x['value'] - w['answer']) > t + tx, '%s %s wrong %s overlaps key' % (f, path, x['id']))

# ---------------------------------------------------------------- 1. l14 ranges
Z = NormalDist().inv_cdf(0.95)
ok(close(Z, 1.6449, 1e-4), 'z(0.95) is 1.645')
ok(close(NormalDist().cdf(1.645) - NormalDist().cdf(-1.645), 0.90, 5e-4), '1.645 sd holds 0.90')
ok(close(2 * NormalDist().cdf(1) - 1, 0.68, 5e-3), '1 sd holds 0.68')
ok(close(2 * NormalDist().cdf(2) - 1, 0.95, 5e-3), '2 sd holds 0.95 to two places')
key('l14-quoting-an-interval', 'screens[0]', 50 + Z * 10)
key('l14-quoting-an-interval', 'screens[1]', 200 - Z * 30)
key('l14-quoting-an-interval', 'screens[11]', 102.40 - Z * 1.20)
key('l14-quoting-an-interval', 'quiz[0]', 1000 + Z * 100)
key('review-4', 'items[1]', 60 + Z * 5)
ok(close(round(102.40 + Z * 1.2, 2), 104.37), 'morning range upper end 104.37')
ok(close(21 * 0.1, 2.1), 'about two misses in a 21-day month')


def score(lo, hi, x, alpha=0.1):
    w = 2 / alpha
    return (hi - lo) + w * max(0, lo - x) + w * max(0, x - hi)


key('l14-quoting-an-interval', 'screens[2]', score(4000, 6000, 5050))
ok(score(5000, 5100, 5050) == 100, '5,000 to 5,100 scores 100')
key('l14-quoting-an-interval', 'screens[4]', 20 * (25 - 30))
key('l14-quoting-an-interval', 'screens[5]', score(30, 40, 25))
key('l14-quoting-an-interval', 'screens[9]', score(20, 24, 25))
key('l14-quoting-an-interval', 'quiz[1]', score(3000, 4000, math.factorial(7)))
ok(score(4000, 6000, 5040) == 2000, '4,000 to 6,000 on 5,040 scores 2,000')
key('review-4', 'items[2]', score(100, 140, 95))
ok(score(90, 140, 95) == 50, '90 to 140 on 95 scores 50')
ok(close(2 / 0.05, 40), 'a 95% range weighs misses at 40')

# The interval (Winkler) score is minimised in expectation by the 5% and 95% points.
# Monte Carlo on a normal belief N(50, 10): compare multipliers k of the sd.
xs = [random.gauss(50, 10) for _ in range(200000)]


def mean_score(k):
    lo, hi = 50 - 10 * k, 50 + 10 * k
    return sum(score(lo, hi, x) for x in xs) / len(xs)


grid = {k: mean_score(k) for k in (1.0, 1.3, 1.5, 1.645, 1.8, 2.0, 2.5)}
ok(min(grid, key=grid.get) == 1.645, 'interval score: honest 5 and 95 per cent points beat narrower and wider ranges (MC) ' + repr(grid))
# Asymmetric check on a skewed belief (lognormal): the optimum is the 5% and 95% quantiles.
ys = sorted(math.exp(random.gauss(0, 1)) for _ in range(40000))
q = lambda p: ys[int(p * len(ys))]
sub = ys[::8]
best = min(((sum(score(q(a), q(b), y) for y in sub) / len(sub), a, b)
            for a in (0.01, 0.03, 0.05, 0.08, 0.12) for b in (0.88, 0.92, 0.95, 0.97, 0.99)))
ok((best[1], best[2]) == (0.05, 0.95), 'interval score optimum on a skewed belief is (5%%, 95%%), got %r' % (best,))

# Calibration: ten independent 90% ranges.
pmf = [math.comb(10, k) * 0.9 ** k * 0.1 ** (10 - k) for k in range(11)]
key('l14-quoting-an-interval', 'screens[6]', pmf[9] + pmf[10])
ok(close(sum(pmf[:7]), 0.0128, 5e-5), 'six or fewer hits has chance 0.0128')
ok(close(pmf[6], 0.0112, 5e-5) and close(pmf[7], 0.0574, 5e-5) and close(pmf[8], 0.1937, 5e-5)
   and close(pmf[5], 0.0015, 5e-5), 'bar heights for 5 to 8 hits')
hits = [sum(random.random() < 0.9 for _ in range(10)) for _ in range(200000)]
ok(abs(sum(h >= 9 for h in hits) / len(hits) - 0.7361) < 0.005, 'MC: 9 or more hits about 0.736')
ok(abs(sum(h <= 6 for h in hits) / len(hits) - 0.0128) < 0.0015, 'MC: 6 or fewer hits about 0.013')
if 'a calibrated set does that only 1.3%' in J['l14-quoting-an-interval']['summary']['ideas'][2]:
    note('l14 summary.ideas[2]: exactly six hits has chance %.4f; 1.3%% is six or fewer' % pmf[6])
# A calibrated month: 4 or more misses in 21 days is not rare, so "more misses mean the sd was too low" overstates.
p4 = 1 - sum(math.comb(21, k) * 0.1 ** k * 0.9 ** (21 - k) for k in range(4))
note('l14 screens[11].explain: a calibrated 90%% range misses 4+ days in 21 with chance %.3f' % p4)


def primes_below(n):
    return sum(all(m % d for d in range(2, int(m ** 0.5) + 1)) for m in range(2, n))


ok(primes_below(50) == 15 and primes_below(100) == 25 and primes_below(200) == 46, 'prime counts 15, 25, 46')
ok(20 * (25 - 30) * 2 == -200, 'opening 30 to 40 costs 200 over two turns')
ok(20 * (46 - 50) * 2 == -160, 'review: 50 to 60 costs 160 over two turns')
key('l14-quoting-an-interval', 'screens[8]', 10 ** 9.5 / 1e9, 0.01)
ok(close(10 ** 8.5 / 1e6, 316.2, 0.1), 'lower end 316 million')
pairs = [((1, 5), 3), ((10, 20), 25), ((3, 4), 4), ((0, 100), 99), ((50, 60), 61), ((7, 9), 8),
         ((2, 2), 2), ((30, 35), 33), ((5, 15), 4), ((40, 41), 40)]
key('l14-quoting-an-interval', 'quiz[2]', sum(lo <= t <= hi for (lo, hi), t in pairs))
ok(sum(lo < t < hi for (lo, hi), t in pairs) == 4, 'open-interval slip counts 4')

# ---------------------------------------------------------------- 2. l15 arbitrage


def cross(asks, bids):
    a, b = [list(x) for x in asks], [list(x) for x in bids]
    i = j = 0
    n, pr = 0, Fr(0)
    while i < len(a) and j < len(b) and a[i][0] < b[j][0]:
        k = min(a[i][1], b[j][1])
        n += k
        pr += k * (b[j][0] - a[i][0])
        a[i][1] -= k
        b[j][1] -= k
        i += a[i][1] == 0
        j += b[j][1] == 0
    return n, pr


D = lambda s: Fr(str(s))
n, pr = cross([(D(103.0), 5), (D(103.5), 10), (D(104.0), 10)], [(D(104.0), 8), (D(103.8), 10), (D(103.2), 10)])
ok((n, pr) == (15, D(8.6)), 'two dealers: 15 units for 8.60')
rows = J['l15-arbitrage-in-a-book']['screens'][1]['widget']['rows']
ok([r[3]['answer'] for r in rows] == [5, 1.5, 2.1, 8.6], 'walk table keys 5, 1.5, 2.1, 8.6')
n, pr = cross([(D(50.0), 4), (D(50.5), 6)], [(D(51.0), 5), (D(50.2), 10)])
ok((n, pr) == (5, D(4.5)), 'quiz cross: 5 units, 4.50')
key('l15-arbitrage-in-a-book', 'quiz[0]', 5)
n, pr = cross([(D(20.0), 3), (D(20.2), 5)], [(D(20.4), 4), (D(20.1), 6)])
ok((n, pr) == (4, D(1.4)), 'review cross: 4 units, 1.40')
key('review-4', 'items[3]', 1.4)
ok(close(1.4 + 4 * (20.1 - 20.2), 1.0), 'review cross slip 1.0')
# sum-of-dice set
key('l15-arbitrage-in-a-book', 'screens[2]', 7.2 - (3.5 + 3.6))
ok(close(3.4 + 3.4 - 7.6, -0.8), 'reverse set loses 0.8')
ok(all((a + b) - a - b == 0 for a in range(1, 7) for b in range(1, 7)), 'B + C pays A on every roll')
cash = -3 * 6.9 + 2 * 7.1 - 3 * 6.9
ok(close(cash, -27.2) and close(cash + 4 * 7, 0.8), 'dealer ledger: cash -27.20, P&L +0.80')
key('l15-arbitrage-in-a-book', 'screens[4]', cash + 28)


def board(odds):
    imp = [Fr(1, o + 1) for o in odds]
    return sum(imp)


ok(board([2, 3, 4]) == Fr(47, 60) and [60 // (o + 1) for o in (2, 3, 4)] == [20, 15, 12], 'board 2,3,4: 47/60, stakes 20, 15, 12')
key('l15-arbitrage-in-a-book', 'screens[5]', 60 - 47)
ok(board([1, 2, 5]) == 1, 'evens, 2 to 1, 5 to 1 sum to exactly 1')
ok(board([1, 3, 4]) == Fr(19, 20), 'evens, 3 to 1, 4 to 1 sum to 19/20')
key('l15-arbitrage-in-a-book', 'screens[9]', 20 - 19)
ok(board([1, 2, 3]) == Fr(13, 12), 'quiz board sums to 13/12')
key('l15-arbitrage-in-a-book', 'quiz[1]', 13 / 12, 5e-5)
ok(board([1, 4, 4]) == Fr(9, 10), 'review board sums to 9/10')
key('review-4', 'items[4]', 10 - 9)
# Dutch book is riskless across ALL outcomes only if one listed outcome must happen.
stakes = [20, 15, 12]
ok(all(s * (o + 1) - sum(stakes) == 13 for s, o in zip(stakes, (2, 3, 4))), 'each listed outcome returns 60 on 47')
note('l15 screens[9], summary.ideas[2], review-4 items[4]: "exclusive" without "one of them must happen": '
     'if a fourth, unlisted outcome occurs the same stakes lose %d, so sum < 1 alone is not an arbitrage' % sum(stakes))
note('l15 quiz[1]: overround 13/12 - 1 = 1/12 of the payout; the bookmaker keeps 1 - 12/13 = 1/13 of the stakes on a balanced book')
key('l15-arbitrage-in-a-book', 'screens[8]', 1000 * 1.25 * 0.92 * 0.88 - 1000, 1e-6)
note('l15 screens[8] wrong "rev": going round the other way at the reciprocal rates gives %.2f, not -12' % (1000 / 1.012 - 1000))
key('l15-arbitrage-in-a-book', 'quiz[2]', 1.30 * 150 * 0.0052, 1e-6)
ok(close(1 / 1.014, 0.9862, 5e-5), 'fx quiz reverse slip 0.9862')
key('l15-arbitrage-in-a-book', 'screens[11]', 20000 * (50.12 - 50.05 - 0.03), 1e-6)

# ---------------------------------------------------------------- 3. l16 contracts
PAY = {'A': [1, 2, 3, 4, 5, 6], 'E': [0, 2, 0, 4, 0, 6], 'F': [1, 0, 3, 0, 5, 0], 'H': [0, 0, 0, 4, 5, 6],
       'L': [1, 2, 3, 0, 0, 0], 'U': [1] * 6, 'Q': [1, 4, 9, 16, 25, 36]}
fair = {k: Fr(sum(v), 6) for k, v in PAY.items()}
ok(fair == {'A': Fr(7, 2), 'E': Fr(2), 'F': Fr(3, 2), 'H': Fr(5, 2), 'L': Fr(1), 'U': Fr(1), 'Q': Fr(91, 6)}, 'fair values of the family')
key('l16-several-contracts', 'screens[0]', 2)
ok([c['answer'] for c in J['l16-several-contracts']['screens'][1]['widget']['rows'][6][1:]] == [3.5, 2, 1.5], 'fair row keys')
ok(all(PAY['E'][f] + PAY['F'][f] == PAY['A'][f] == PAY['H'][f] + PAY['L'][f] for f in range(6)), 'E+F = A = H+L on every face')
key('l16-several-contracts', 'screens[3]', 2.1 + 1.6 - 3.2)
ok(close(2.2 + 1.7 - 3.1, 0.8) and close(3.0 - 2.3 - 1.8, -1.1), 'ladder slips 0.8 and -1.1')
ok(close(3.6 - 1.4, 2.2) and close(3.4 - 1.6, 1.8), 'synthetic E band 1.8 to 2.2')
cash = 3 * 2.1 + 1 * 2.1 - 3 * 1.9
ok(close(cash, 2.7), 'E ledger cash +2.70')
key('l16-several-contracts', 'screens[5]', cash - 2)
key('l16-several-contracts', 'screens[6]', 10 * (1.6 + 1.4 - 3.3))
dev = [Fr((f - Fr(7, 2)) ** 2) for f in range(1, 7)]
ok(all(d == PAY['Q'][i] - 7 * PAY['A'][i] + Fr(49, 4) for i, d in enumerate(dev)), '(face-3.5)^2 = Q - 7A + 12.25 on every face')
ok(sum(dev) / 6 == Fr(35, 12) == fair['Q'] - 7 * fair['A'] + Fr(49, 4), 'squared-deviation contract worth 35/12')
key('l16-several-contracts', 'screens[7]', 35 / 12, 5e-5)
key('l16-several-contracts', 'screens[9]', 2.5)
key('l16-several-contracts', 'screens[11]', 6 - (102 - 100))
ok(close(4.5 - 6 + 2, 0.5), 'put at 4.5: sell put, buy call, sell future locks 0.50')
key('l16-several-contracts', 'quiz[0]', 1 / 3, 5e-5)
key('l16-several-contracts', 'quiz[1]', 20 * (3.6 - 2.5 - 1.0), 1e-6)
key('review-4', 'items[5]', sum(2 * x for x in PAY['F']) / 6)
key('review-4', 'items[6]', 3.6 - 1.8 - 1.5)
ok(close(1.6 + 1.4 - 3.8, -0.8) and close(3.7 - 1.7 - 1.45, 0.55), 'review contract slips')


def no_arb_three(qA, qE, qF):
    """True when neither parity trade through A, E, F locks a profit."""
    return qE[0] + qF[0] <= qA[1] and qA[0] <= qE[1] + qF[1]


opts = {o['id']: o for o in J['l16-several-contracts']['screens'][2]['widget']['options']}
ok(no_arb_three((3.3, 3.7), (1.8, 2.2), (1.3, 1.7)), 'keyed quote set has no arbitrage')
ok(not no_arb_three((3.3, 3.7), (3.8, 4.2), (1.3, 1.7)) and not no_arb_three((3.3, 3.7), (3.3, 3.7), (3.3, 3.7)),
   'options "evens" and "same" can be traded through')
if 'E 2.3 to 2.7' in opts['skewE']['text'] and no_arb_three((3.3, 3.7), (2.3, 2.7), (1.3, 1.7)):
    note('l16 screens[2] option skewE: E 2.3 to 2.7 cannot be traded through for a sure profit either '
         '(bids 2.3 + 1.3 = 3.6 < A ask 3.7), so it is "consistent" by the explain\'s own test; it only loses on average')

# ---------------------------------------------------------------- 4. l17 options
SUMS = [a + b for a in range(1, 7) for b in range(1, 7)]
call = lambda k: Fr(sum(max(s - k, 0) for s in SUMS), 36)
put = lambda k: Fr(sum(max(k - s, 0) for s in SUMS), 36)
ok(call(7) == put(7) == Fr(35, 36) and call(8) == Fr(5, 9) and put(8) == Fr(14, 9), '7 and 8 strike values')
ok(all(call(k) - put(k) == 7 - k for k in range(1, 14)), 'parity C - P = 7 - K at every strike')
ok(all((max(s - k, 0) - max(k - s, 0)) == s - k for s in SUMS for k in range(1, 14)), 'call less put pays S - K on every roll')
key('l17-options-on-a-game', 'screens[0]', 35 / 36, 5e-5)
ok(close(15 / 36, 0.4167, 5e-5) and close(35 / 15, 2.3333, 5e-5), 'chance 15/36 and conditional payoff 35/15')
key('l17-options-on-a-game', 'screens[1]', 35 / 18, 5e-5)
key('l17-options-on-a-game', 'screens[2]', 14 / 9, 5e-5)
ok(put(9) == Fr(41, 18) and call(9) == Fr(5, 18) == put(5), '9-put 41/18, 9-call 5/18 = 5-put')
key('l17-options-on-a-game', 'screens[9]', 5 / 18, 5e-5)
key('l17-options-on-a-game', 'quiz[0]', 5 / 18, 5e-5)
ok(call(2) == 5 and put(2) == 0 and call(12) == 0, 'edge strikes 2 and 12')
key('l17-options-on-a-game', 'quiz[1]', 5)
key('l17-options-on-a-game', 'quiz[2]', float(call(8) + put(8)), 5e-5)
strad = {k: call(k) + put(k) for k in range(2, 13)}
ok(min(strad, key=strad.get) == 7, 'straddle is cheapest at strike 7')
ok(put(6) == Fr(5, 9) and call(6) == Fr(14, 9), '6-put 5/9 and 6-call 14/9')
key('review-4', 'items[7]', 5 / 9, 5e-5)
key('review-4', 'items[8]', 14 / 9, 5e-5)
key('homework-4', 'items[5]', 35 / 36, 5e-5)
key('homework-4', 'items[6]', 1 / 6, 5e-5)
# conditional values after the first die
cond = [Fr(sum(max(d + e - 7, 0) for e in range(1, 7)), 6) for d in range(1, 7)]
ok(cond == [0, Fr(1, 6), Fr(1, 2), 1, Fr(5, 3), Fr(5, 2)] and sum(cond) / 6 == Fr(35, 36), 'tree leaves and their average')
key('l17-options-on-a-game', 'screens[7]', 2.5)
ok(Fr(sum(abs(4 + e - 7) for e in range(1, 7)), 6) == Fr(3, 2), 'straddle after a first die of 4 is worth 1.5')
cash = -1.8 + 3 * 2.0 - 1.5
ok(close(cash, 2.7) and close(cash - abs(8 - 7), 1.7), 'straddle model run: cash 2.70, P&L 1.70')
key('l17-options-on-a-game', 'screens[4]', cash - abs(10 - 7))
key('l17-options-on-a-game', 'screens[6]', 7 - (0.8 + 7.1 - 1.1))
ok(all(-max(s - 7, 0) + max(7 - s, 0) + s == 7 for s in SUMS), 'short call, long put, long sum pays 7 on every roll')
ok(close(7 - (0.75 + 7.0 - 1.15), 0.4), 'parity slip at mids 0.4')
key('homework-4', 'items[7]', 0.2)
ok(close(0.7 + 6.9 - 1.2 - 7, -0.6), 'reverse parity trade loses 0.6')
key('l17-options-on-a-game', 'screens[8]', 10 * (2.0 - abs(11 - 7)))
ok(10 * (2.0 - 5) == -30, 'ten short straddles at 2 or 12 lose 30')
key('l17-options-on-a-game', 'screens[11]', 120 - 118)
# Monte Carlo of the 7-call and the straddle
rolls = [random.randint(1, 6) + random.randint(1, 6) for _ in range(400000)]
ok(abs(sum(max(s - 7, 0) for s in rolls) / len(rolls) - 35 / 36) < 0.01, 'MC: 7-call about 0.972')
ok(abs(sum(abs(s - 7) for s in rolls) / len(rolls) - 35 / 18) < 0.01, 'MC: 7-straddle about 1.944')
win = Fr(sum(abs(s - 7) < 2 for s in SUMS), 36)
lose = Fr(sum(abs(s - 7) > 2 for s in SUMS), 36)
if 'earns small sums often and loses large ones rarely' in J['l17-options-on-a-game']['screens'][8]['explain']['text']:
    note('l17 screens[8].explain: a straddle sold at 2.0 gains on %s of rolls (at most 2), loses on %s (at most 3), '
         'breaks even on the rest: neither "often" against "rarely" nor "small" against "large"' % (win, lose))
if 'Strikes far from 7 are cheap' in J['l17-options-on-a-game']['quiz'][0]['explain']['text']:
    note('l17 quiz[0].explain: "Strikes far from 7 are cheap" fails for the 2-call (worth 5) and the 12-put (worth 5)')
# mock round
ok(close(2 * 1.1 - 2 * 0.2, 1.8) and close(2 * 1.1 - 2 * 0.9, 0.4), 'mock round: +1.80, stale bid +0.40')
key('homework-4', 'items[8]', 1.8)
ok(close(2.2 - 2 * 5, -7.8) and close(0.8 + 7.1 - 7, 0.9) and close(2 * (1.1 - 1 / 6), 1.87, 5e-3), 'mock narration numbers')
ok(all(max(7 - s, 0) + s == 7 + max(s - 7, 0) for s in SUMS), 'put plus sum pays 7 plus the call')

# ---------------------------------------------------------------- 5. l18 Kelly
BETS = [(1, 0.55), (2, 0.4), (3, 0.2), (1, 0.6)]
edge = [p * b - (1 - p) for b, p in BETS]
kel = [max(0.0, p - (1 - p) / b) for b, p in BETS]
ok(all(close(a, b) for a, b in zip(edge, [0.1, 0.2, -0.2, 0.2])), 'edges 0.1, 0.2, -0.2, 0.2')
ok(all(close(a, b) for a, b in zip(kel, [0.1, 0.1, 0, 0.2])), 'Kelly fractions 0.1, 0.1, 0, 0.2')
ok([r[3]['answer'] for r in J['l18-betting-board']['screens'][1]['widget']['rows']] == [0.1, 0.2, -0.2, 0.2], 'edge table keys')
ok([r[3]['answer'] for r in J['l18-betting-board']['screens'][2]['widget']['rows']] == [10, 10, 0, 20], 'stake table keys')
ev = sum(100 * k * e for k, e in zip(kel, edge))
key('l18-betting-board', 'screens[3]', ev)
ok(close(ev - 10 * 0.2, 5), 'slip: staking 10 on c gives 5')
ok(J['l18-betting-board']['screens'][4]['widget']['answer'] == {'a': 7.5, 'b': 7.5, 'd': 15}, 'capped stakes 7.5, 7.5, 15')
key('l18-betting-board', 'screens[5]', 0.75 * ev)
key('l18-betting-board', 'screens[6]', 100 + 10 - 10 + 20)
key('l18-betting-board', 'screens[7]', 0.2 * 120)
key('l18-betting-board', 'screens[8]', 120 - 12 + 2 * 12 - 24)
ok(close(120 - 12 + 12 - 24, 96) and close(120 - 10 + 20 - 20, 110), 'round two slips 96 and 110')
key('l18-betting-board', 'screens[9]', (0.3 - 0.7 / 3) * 120, 1e-6)
key('l18-betting-board', 'screens[11]', 0.1 * 800000)
key('l18-betting-board', 'quiz[0]', 0)
key('l18-betting-board', 'quiz[1]', 10)
key('l18-betting-board', 'quiz[2]', 200 * 0.2 * 0.2 + 200 * (0.25 - 0.75 / 4) * (0.25 * 4 - 0.75), 1e-6)
key('review-4', 'items[9]', 50 * 0.25 * 15 / 22.5, 0.005)
# Kelly maximises expected log growth (grid), and beats it by simulation.
g = lambda f, b, p: p * math.log(1 + f * b) + (1 - p) * math.log(1 - f)
for b, p in [(1, 0.55), (2, 0.4), (1, 0.6), (3, 0.3), (4, 0.25)]:
    fs = p - (1 - p) / b
    ok(all(g(fs, b, p) >= g(fs + d, b, p) for d in (-0.05, -0.01, 0.01, 0.05)), 'Kelly fraction maximises log growth at %s to 1, p=%s' % (b, p))
ok(g(0.2, 1, 0.5) < 0 and close(0.5 - 0.5 / 1, 0), 'a fair bet has no positive-growth stake')
ok(0.70 < g(0.1, 1, 0.6) / g(0.2, 1, 0.6) < 0.80, 'half Kelly keeps about three quarters of the growth')


def sim(f, n=4000, paths=300):
    tot = 0.0
    for _ in range(paths):
        w = 0.0
        for _ in range(n):
            w += math.log(1 + f) if random.random() < 0.6 else math.log(1 - f)
        tot += w / n
    return tot / paths


s1, s2, s3 = sim(0.1), sim(0.2), sim(0.4)
ok(s2 > s1 > 0 and s2 > s3, 'MC: on evens at 0.6, Kelly 0.2 outgrows 0.1 and 0.4 (%.4f, %.4f, %.4f)' % (s1, s2, s3))
# Ruin is impossible when a fraction below 1 is at risk: the worst round keeps 60%.
ok(1 - sum(kel) > 0, 'worst round multiplies the bankroll by %.2f, never 0' % (1 - sum(kel)))
# Joint Kelly for a, b, d settled together (independent bets): a little lower than one at a time.
LIVE = [(1, 0.55), (2, 0.4), (1, 0.6)]
OUT = []
for wins in itertools.product((True, False), repeat=3):
    pr = 1.0
    for (b, p), w in zip(LIVE, wins):
        pr *= p if w else 1 - p
    OUT.append((pr, [b if w else -1 for (b, p), w in zip(LIVE, wins)]))


def growth(f):
    return sum(pr * math.log(1 + sum(fi * x for fi, x in zip(f, xs_))) for pr, xs_ in OUT)


def grad(f):
    return [sum(pr * xs_[i] / (1 + sum(fi * x for fi, x in zip(f, xs_))) for pr, xs_ in OUT) for i in range(3)]


f = [0.1, 0.1, 0.2]
for _ in range(20000):
    f = [fi + 0.01 * gi for fi, gi in zip(f, grad(f))]
ok(all(abs(x) < 1e-7 for x in grad(f)), 'joint Kelly converged')
ok(all(0.85 * k < fi < k for fi, k in zip(f, [0.1, 0.1, 0.2])),
   'joint Kelly is a little lower than one-at-a-time Kelly: %s' % [round(x, 4) for x in f])
# Under a cap of 0.3 of the bankroll, equal scaling is a rule of thumb, not the growth optimum.
h = [0.075, 0.075, 0.15]
for _ in range(40000):
    gr = grad(h)
    m = sum(gr) / 3
    h = [hi + 0.01 * (gi - m) for hi, gi in zip(h, gr)]      # move along the plane sum(h) = 0.3
ok(abs(sum(h) - 0.3) < 1e-9 and growth(h) >= growth([0.075, 0.075, 0.15]), 'capped optimum found')
note('l18 screens[4]: under the 30 cap the growth-optimal stakes on 100 are %s (growth %.5f), equal scaling 7.5, 7.5, 15 '
     'gives %.5f; equal scaling is a simple rule, close to but not the optimum'
     % ([round(100 * x, 2) for x in h], growth(h), growth([0.075, 0.075, 0.15])))

# ---------------------------------------------------------------- 6. code widgets


def same(a, b, cmp, tol):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y, cmp, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k], cmp, tol) for k in a)
    if cmp == 'isclose' and isinstance(a, (int, float, Fr)) and isinstance(b, (int, float, Fr)) and not isinstance(a, bool):
        return abs(a - b) <= max(tol, 1e-9 * max(abs(a), abs(b)))
    return a == b and (cmp == 'isclose' or type(a) == type(b) or isinstance(a, (int, float, Fr)))


def run(w, src):
    env = {}
    exec(w.get('prelude', '') + '\n' + src, env)
    res = []
    for t in w['tests']:
        try:
            got = eval(t['call'], env)
            exp = eval(t['expect'], env)
            res.append(same(got, exp, t.get('compare', 'equal'), (t.get('tol') or {}).get('abs', 1e-9)))
        except Exception:
            res.append(False)
    return res


ncode = 0
for fname in FILES:
    for path, s in units(fname):
        w = s.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        ncode += 1
        ok(all(run(w, w['solution'])), '%s %s solution passes all hidden tests' % (fname, path))
        ok(not all(run(w, w['starter'])), '%s %s starter fails the hidden tests' % (fname, path))
ok(ncode == 7, 'seven code widgets found (%d)' % ncode)

# find_arb (l16) and find_all_arb (homework) test only for a constant payoff. A dominance arbitrage is missed.
w16 = J['l16-several-contracts']['screens'][10]['widget']
env = {}
exec(w16['prelude'] + '\n' + w16['solution'], env)
r = env['find_arb'](env['PAY'], {'L': (Fr('3.2'), Fr('3.3'))}, {'L': -1})
if r == 0:
    note('l16 screens[10] find_arb: selling L (pays at most 3) at a bid of 3.2 never loses and gains at least 0.20 on '
         'every face, yet the "same payoff on every face" test returns 0; the lesson\'s definition of arbitrage '
         '(payoffs that cancel) is narrower than the standard one (never lose, sometimes gain)')

# ---------------------------------------------------------------- 7. claims false as stated
t = J['review-4']['items'][2]['explain']['text']
if 'Five more units of width would have saved 90' in t:
    ok(score(100, 140, 95) - score(95, 140, 95) == 90,
       'review-4 items[2].explain: "Five more units of width would have saved 90" (95 to 140 scores %d, saving %d; '
       '90 to 140 is ten more units)' % (score(95, 140, 95), score(100, 140, 95) - score(95, 140, 95)))

# ---------------------------------------------------------------- 8. fix-pass text (audit fix pass)
if 'Ten more units of width would have saved 90' in t:
    ok(score(100, 140, 95) - score(90, 140, 95) == 90, 'review-4 items[2].explain: ten more units (90 to 140) save 90')
if 'E 2.5 to 2.9' in opts['skewE']['text']:
    ok(not no_arb_three((3.3, 3.7), (2.5, 2.9), (1.3, 1.7)) and close(2.5 + 1.3 - 3.7, 0.1),
       'l16 screens[2] skewE (E 2.5 to 2.9) is traded through for 0.10 a set')
ok(r == Fr(1, 5), 'l16 find_arb: selling L at 3.2 locks 0.20 on the worst face')
gain = sum(1 for s in SUMS if abs(s - 7) < 2)
loss = sum(1 for s in SUMS if abs(s - 7) > 2)
if 'gains only on sums 6 to 8, 16 rolls in 36, and loses on 12' in J['l17-options-on-a-game']['screens'][8]['explain']['text']:
    ok(gain == 16 and loss == 12, 'l17 screens[8].explain: short straddle at 2.0 gains on 16 rolls, loses on 12')

print('%d checks passed, %d failed, %d notes' % (passed[0], len(fails), len(notes)))
raise SystemExit(1 if fails else 0)
