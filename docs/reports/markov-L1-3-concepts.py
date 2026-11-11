#!/usr/bin/env python3
"""Concept audit checks for markov levels 1 to 3 (round 1).

Run from anywhere: python3 docs/reports/markov-L1-3-concepts.py
Needs numpy only. Exits 0 when every check passes. A check tagged FINDING fails while the
content still carries the audited sentence and the mathematics contradicts it; it passes
once the sentence is gone, so the fix pass turns the script green.
"""
import json, math, os, random, sys
from fractions import Fraction as F
from math import comb
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'markov')
def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as fh:
        return json.load(fh)
RAW = {}
def raw(name):
    if name not in RAW:
        with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as fh:
            RAW[name] = json.dumps(json.load(fh), ensure_ascii=False)
    return RAW[name]

fails = []
def check(label, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + label + (('  [' + detail + ']') if detail else ''))
    if not ok:
        fails.append(label)
def finding(label, sentence, file, contradicted, detail=''):
    """Fails while `sentence` is still in `file` and the maths contradicts it."""
    present = sentence in raw(file)
    check('FINDING ' + label, not (present and contradicted), detail + ('' if present else ' (sentence no longer present)'))
def close(a, b, tol=1e-9):
    return abs(a - b) <= tol

def stationary(P):
    P = np.array(P, float); n = len(P)
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    return np.linalg.lstsq(A, np.r_[np.zeros(n), 1], rcond=None)[0]
def n_stationary(P):
    P = np.array(P, float)
    return len(P) - np.linalg.matrix_rank(P.T - np.eye(len(P)))
mp = np.linalg.matrix_power

# ------------------------------------------------------------------ level 1
W = np.array([[.6, .3, .1], [.3, .4, .3], [.2, .5, .3]])
l2 = load('l2-transition-matrix')
_d = l2['screens'][1]['canvas']['derive']
bars = _d['values'] if 'values' in _d else {k: _d['values.' + k] for k in 'SCR'}
okb = True
for k in range(11):
    row = mp(W, k)[2]
    for j, key in enumerate('SCR'):
        shown = json.loads(bars[key].split('[k]')[0])[k]
        okb &= abs(shown - row[j]) < 6e-4
check('l2 s1 bars equal row Rain of P^k, k = 0..10', okb)
check('l2 s3 P^2 shown', np.allclose(mp(W, 2), [[.47, .35, .18], [.36, .4, .24], [.33, .41, .26]]))
R = np.array([[.9, .09, .01], [.05, .85, .1], [0, 0, 1]])
check('l2 s8 / l3 s9 default by year 1..5', np.allclose([mp(R, k)[0, 2] for k in range(1, 6)], [.01, .028, .051895, .0800, .1111], atol=6e-5),
      str([round(mp(R, k)[0, 2], 5) for k in range(1, 6)]))
R3 = np.array([[.8, .15, .05], [.2, .7, .1], [.1, .3, .6]])
check('l2 s9 after([0,1,0], R3, 5)', np.allclose(mp(R3, 5)[1], [0.428785, 0.4122775, 0.1589375]))
B = np.array([[.9, .1], [.2, .8]])
check('l2 s9 test after([1,0], B, 3)', np.allclose(mp(B, 3)[0], [.781, .219]))
# l3 five-state chain
C5 = np.zeros((5, 5)); ix = {c: i for i, c in enumerate('ABCDE')}
for a, b, w in [('A', 'A', .5), ('A', 'B', .5), ('B', 'A', .3), ('B', 'C', .3), ('B', 'D', .4), ('C', 'C', 1), ('D', 'D', .6), ('D', 'E', .4), ('E', 'D', .7), ('E', 'E', .3)]:
    C5[ix[a], ix[b]] = w
r20 = mp(C5, 20)[0]
check('l3 s1 bars at k = 20', np.allclose(r20, [.001, .001, .428, .363, .207], atol=1.5e-3), str(np.round(r20, 4)))
check('l3 s2 f_A = 0.65 (loop, or A-B-A; B has no loop)', close(.5 + .5 * .3, .65))
G = np.array([[1, 0, 0, 0, 0], [.5, 0, .5, 0, 0], [0, .5, 0, .5, 0], [0, 0, .5, 0, .5], [0, 0, 0, 0, 1]])
check('l3 s5 game over within 4 bets from 2', close(mp(G, 4)[2, 0] + mp(G, 4)[2, 4], .75))
# l4
check('l4 s6 gap after k steps is 0.7^k', all(close(mp(B, k)[0, 0] - mp(B, k)[1, 0], .7 ** k) for k in range(13)))
seq = 'UUUUUUDDDU' + 'UUUUUUUDUU'
pairs = [a + b for a, b in zip(seq, seq[1:])]
check('l4 s8 counts 13, 2, 2, 2', [pairs.count(x) for x in ('UU', 'UD', 'DU', 'DD')] == [13, 2, 2, 2])
check('l4 s9 expected position 5.7, long run 9.667', close(.2 * 12.5 + .8 * 4, 5.7) and close(2 / 3 * 12.5 + 4 / 3, 9.6667, 1e-3))
# geometric run conventions (finding B): L counts periods in the state, P(L = n) = p^(n-1)(1-p)
p = .85
e_total_given_4 = 4 + p / (1 - p)        # E[L | L >= 4]: weeks in drawdown, the 4th being the last one observed
e_from_now_incl = 1 / (1 - p)            # weeks still to come if the present week is counted
check('l4 s10 key 6.67 is the count including the present week; 5.67 further weeks if it is not counted',
      close(e_from_now_incl, 6.6667, 1e-3) and close(e_total_given_4 - 4, 5.6667, 1e-3))
finding('l4 s10: "more weeks" keyed 6.67 without saying the present week counts (5.67 is the other valid reading)',
        'How many more weeks is the drawdown expected to last?', 'l4-regimes', True)
# finding C: l1 s4 option feedback
cyc = ['Open', 'Closed', 'Pre-open']
finding('l1 s4: "stopped one step early" gives Open, not Pre-open (8 steps or going backwards give Pre-open)',
        'You stopped one step early or went round backwards.', 'l1-only-now', cyc[6 % 3] != 'Pre-open' and cyc[8 % 3] == 'Pre-open')
# homework-1 long item
Ph = np.array([[.95, .05], [.15, .85]])
check('hw1 long: P^4 stressed row and position', np.allclose(mp(Ph, 4)[1], [.4428, .5572]) and close(mp(Ph, 4)[1] @ [24, 8], 15.0848, 1e-4))
Pb = np.array([[.85, .12, .03], [.1, .75, .15], [0, 0, 1]])
check('hw1 credit-b', np.allclose([mp(Pb, k)[1, 2] for k in (1, 2, 3)], [.15, .2655, .356475]))

# ------------------------------------------------------------------ level 2
check('l5 s3 pi = (0.2, 0.5, 0.3)', np.allclose(stationary([[.75, .25, 0], [.1, .75, .15], [0, .25, .75]]), [.2, .5, .3]))
Pl5 = [[0.9, 0.1], [0.2, 0.8]]
def share_in_bull(days, seed):
    rng = random.Random(seed); state = 1; bull = 0
    for _ in range(days):
        state = 0 if rng.random() < Pl5[state][0] else 1
        bull += (state == 0)
    return bull / days
got = [share_in_bull(200000, s) for s in (1, 2, 7)]
check('l5 s7 quoted shares for seeds 1, 2, 7', np.allclose(got, [0.666255, 0.668935, 0.66784], atol=5e-7), str(got))
check('l5 s7 examples', close(share_in_bull(10, 3), .5) and close(share_in_bull(1, 1), 1.0))
# finding A: reducible chain with a unique stationary distribution (the lesson 5 loan chain)
PD = [[.97, .03], [0, 1]]
finding('l6 summary: "A reducible chain has several closed classes and many stationary distributions" (Perf/Def is reducible with one)',
        'A reducible chain has several closed classes and many stationary distributions.', 'l6-always-settle', n_stationary(PD) == 1,
        'stationary solutions of the Perf/Def chain: dimension %d' % n_stationary(PD))
finding('l6 s6 feedback: "This chain is reducible, so it has many"',
        'This chain is reducible, so it has many, and the start picks the limit.', 'l6-always-settle', n_stationary(PD) == 1)
E5 = np.zeros((5, 5)); ix = {c: i for i, c in enumerate('ABCDE')}
for a, b, w in [('E', 'A', .5), ('E', 'C', .5), ('A', 'A', .5), ('A', 'B', .5), ('B', 'A', .25), ('B', 'B', .75), ('C', 'C', .8), ('C', 'D', .2), ('D', 'C', .2), ('D', 'D', .8)]:
    E5[ix[a], ix[b]] = w
lim = mp(E5, 400)
check('l6 s5/s6 limits from E, A, C', np.allclose(lim[4], [1 / 6, 1 / 3, .25, .25, 0]) and close(lim[0, 1], 2 / 3) and close(lim[2, 0], 0))
check('l6 s5 two-class chain has a 2-dimensional set of stationary vectors', n_stationary(E5) == 2)
check('l6 s9 pi = (1/4, 1/2, 1/4)', np.allclose(stationary([[0, 1, 0], [.5, 0, .5], [0, 1, 0]]), [.25, .5, .25]))
def absorb(P):
    P = np.array(P, float); ends = [i for i in range(len(P)) if P[i, i] == 1]; mv = [i for i in range(len(P)) if P[i, i] != 1]
    N = np.linalg.inv(np.eye(len(mv)) - P[np.ix_(mv, mv)])
    H = np.zeros(P.shape); t = np.zeros(len(P))
    for a in ends: H[a, a] = 1
    H[np.ix_(mv, ends)] = N @ P[np.ix_(mv, ends)]; t[mv] = N @ np.ones(len(mv))
    return H, t, N
H, t, N = absorb([[.85, .14, .01], [.05, .9, .05], [0, 0, 1]])
check('l7 s4 years to default 30 and 25', np.allclose(t, [30, 25, 0]))
H, t, N = absorb([[1, 0, 0, 0], [.25, .5, .25, 0], [0, .25, .5, .25], [0, 0, 0, 1]])
check('l7 s6 lazy walk t_1 = 4', close(t[1], 4))
H, t, N = absorb([[.6, .3, 0, .1], [0, .5, .4, .1], [0, 0, 1, 0], [0, 0, 0, 1]])
check('l7 s8 / l8 s8 order queue t_B = 4, h_B = 0.6, h_F = 0.8', close(t[0], 4) and close(H[0, 2], .6) and close(H[1, 2], .8))
H, t, N = absorb([[.3, .1, .5, .1], [.2, .4, .2, .2], [0, 0, 1, 0], [0, 0, 0, 1]])
check('l8 s4 N and H; review-2 t = (1.75, 2.25)', np.allclose(N, [[1.5, .25], [.5, 1.75]]) and np.allclose(H[:2, 2:], [[.8, .2], [.6, .4]]) and np.allclose(t[:2], [1.75, 2.25]))
H, t, N = absorb([[1, 0, 0, 0], [F(1, 3), 0, F(2, 3), 0], [0, F(1, 3), 0, F(2, 3)], [0, 0, 0, 1]])
check('l8 s3 h = (4/7, 6/7); hw2 t = (15/7, 12/7)', np.allclose(H[1:3, 3], [4 / 7, 6 / 7]) and np.allclose(t[1:3], [15 / 7, 12 / 7]))
TENNIS = [[0, 0.6, 0.4, 0, 0], [0, 1, 0, 0, 0], [0.6, 0, 0, 0, 0.4], [0, 0, 0, 1, 0], [0, 0, 0.6, 0.4, 0]]
SIX = [[0.5, 0.3, 0.2, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0.1, 0.2, 0.4, 0.1, 0.2, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0.3, 0.3, 0.3, 0.1], [0, 0, 0, 0, 0, 1]]
H, t, N = absorb(TENNIS)
check('hw2 code: TENNIS expected values', np.allclose(H[2], [0, 9 / 13, 0, 4 / 13, 0]) and np.allclose(H[0], [0, 57 / 65, 0, 8 / 65, 0]) and np.allclose(H[4], [0, 27 / 65, 0, 38 / 65, 0]) and np.allclose(t, [33 / 13, 0, 50 / 13, 0, 43 / 13]))
H, t, N = absorb(SIX)
check('hw2 code: SIX expected values', np.allclose(H[0], [0, 68 / 83, 0, 13 / 83, 0, 2 / 83]) and np.allclose(H[2], [0, 91 / 166, 0, 65 / 166, 0, 5 / 83]) and np.allclose(H[4], [0, 39 / 166, 0, 99 / 166, 0, 14 / 83]) and np.allclose(t, [270 / 83, 0, 260 / 83, 0, 230 / 83, 0]))
H, t, N = absorb([[0, 1, 0], [.9, 0, .1], [0, 0, 1]])
check('hw2 code: CYCLE t = (20, 19)', np.allclose(t, [20, 19, 0]))
def simulate_absorb(P, start, runs, seed):
    rng = random.Random(seed); n = len(P); counts = [0] * n
    for _ in range(runs):
        s = start
        while P[s][s] != 1:
            u, acc = rng.random(), 0.0
            for j in range(n):
                acc += P[s][j]
                if u < acc: break
            s = j
        counts[s] += 1
    return [c / runs for c in counts]
check('hw2 code: seeded simulations within 0.02 of exact', np.allclose(simulate_absorb(TENNIS, 2, 30000, 1), [0, 9 / 13, 0, 4 / 13, 0], atol=.02) and np.allclose(simulate_absorb(SIX, 4, 30000, 5), [0, 39 / 166, 0, 99 / 166, 0, 14 / 83], atol=.02))
# hw2 HTH: exact 10; pattern HH 6; block trials would give 24
A = np.array([[.5, -.5, 0], [0, .5, -.5], [-.5, 0, 1]]); tt = np.linalg.solve(A, [1, 1, 1])
check('hw2 HTH t = (10, 8, 6)', np.allclose(tt, [10, 8, 6]))
finding('hw2 HTH feedback: "as if each block of three days were a fresh trial" would give 3 x 8 = 24 days, not 8',
        'as if each block of three days were a fresh trial', 'homework-2', 3 * 8 != 8)
def mulberry(seed):
    a = seed & 0xFFFFFFFF
    def imul(x, y): return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF
    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF; t = a
        t = imul(t ^ (t >> 15), t | 1); t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r
r = mulberry(7); tot = 0
for _ in range(200000):
    st = 0; n = 0
    while st < 3:
        h = r() < .5; n += 1
        st = (1 if h else 0) if st == 0 else ((1 if h else 2) if st == 1 else (3 if h else 0))
    tot += n
hth = tot / 200000
check('hw2 HTH: mulberry32 seed 7, 200,000 runs (H when u < 0.5) is within 0.05 of 10; quoted 9.995', abs(hth - 10) < .05, 'got %.4f' % hth)
# problems-2
check('p2 band pi = (4, 20, 5)/29', np.allclose(stationary([[.5, .5, 0], [.1, .8, .1], [0, .4, .6]]), np.array([4, 20, 5]) / 29))
H, t, N = absorb([[0, .4, .4, .2], [.5, 0, .2, .3], [0, 0, 1, 0], [0, 0, 0, 1]])
check('p2 rfq q = 0.6, t = (1.75, 1.875)', close(H[0, 2], .6) and np.allclose(t[:2], [1.75, 1.875]))
H, t, N = absorb([[0, .3, .5, .2], [.5, 0, .2, .3], [0, 0, 1, 0], [0, 0, 0, 1]])
check('p2 rfq tight q = 0.6588, 1.53 rounds', close(H[0, 2], .56 / .85) and close(t[0], 1.3 / .85))
H, t, N = absorb([[.5, .3, .1, .1], [0, .6, .25, .15], [0, 0, 1, 0], [0, 0, 0, 1]])
check('p2 merger h = (0.575, 0.625), t = (3.5, 2.5)', np.allclose(H[:2, 2], [.575, .625]) and np.allclose(t[:2], [3.5, 2.5]))
P4 = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [.25, 0, .5, .25], [0, 0, 0, 1]])
check('hw2 periodic-reducible: P(X_k = 1) from 3 alternates near 1/6 and 1/3', close(mp(P4, 200)[2, 0], 1 / 6, 1e-6) and close(mp(P4, 201)[2, 0], 1 / 3, 1e-6))

# ------------------------------------------------------------------ level 3
def binom_cdf(n, p, k):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))
def ruin_up(i, N, p):
    if p == .5: return i / N
    r = (1 - p) / p; return (1 - r ** i) / (1 - r ** N)
def returns0(n2):   # expected visits to 0 in steps 1..n2 of a fair walk
    return sum(comb(2 * k, k) / 4 ** k for k in range(1, n2 // 2 + 1))
check('l9 s8/quiz: about 7 returns in 100 steps', abs(returns0(100) - 7.04) < .01, '%.3f' % returns0(100))
m = 5000; lg = math.lgamma(2 * m + 1) - 2 * math.lgamma(m + 1) - 2 * m * math.log(2)
check('l9 quiz: about 79 returns in 10,000 steps (closed form (2m+1) C(2m,m)/4^m - 1)', abs((2 * m + 1) * math.exp(lg) - 1 - 78.8) < .1, '%.2f' % ((2 * m + 1) * math.exp(lg) - 1))
check('l9 s9 exact P(P&L < 0) = 0.097', abs(binom_cdf(1000, .52, 499) - .097) < 6e-4, '%.4f' % binom_cdf(1000, .52, 499))
check('l9 s7 P(S_20 = 4)', close(comb(20, 12) / 2 ** 20, .1201, 5e-5))
# finding G: variance of a sum needs only zero covariances
# X1 fair +-1; X2 = X1 * Z with Z fair +-1 independent; X3 = X2 * X1 = Z ... use pairwise-uncorrelated but dependent steps:
# X1, X2 independent fair +-1, X3 = X1 * X2: pairwise independent, not independent; Var(X1 + X2 + X3) = 3 all the same.
vals = [(a, b, a * b) for a in (-1, 1) for b in (-1, 1)]
var3 = sum((sum(v)) ** 2 for v in vals) / 4 - (sum(sum(v) for v in vals) / 4) ** 2
finding('l9 s6: "The variance needs independence" (dependent steps with zero covariances add the same way)',
        'The variance needs independence, so that the covariance terms vanish.', 'l9-coin-flip-walk', close(var3, 3.0), 'Var(X1+X2+X1X2) = %g' % var3)
check('l10 s4 P_50 = 0.1192, flip 0.8808, s5 ten-pound bets 0.450, s7 0.31', close(ruin_up(50, 100, .49), .11917, 1e-5) and close(ruin_up(50, 100, .51), .8808, 5e-5) and close(ruin_up(5, 10, .49), .450, 5e-4) and close(ruin_up(20, 40, .49), .3100, 5e-5))
dur = (50 - 100 * ruin_up(50, 100, .49)) / (.51 - .49)
check('l10: mean length of the 49% game from 50 of 100 is about 1,904 bets ("thousands" is loose but fair)', abs(dur - 1904) < 1, '%.1f' % dur)
check('l10 quiz 9/13; review-3 0.4493, 0.7317; hw3 roulette 0.3680', close(ruin_up(2, 4, .6), 9 / 13) and close((49 / 51) ** 20, .4493, 5e-5) and close(ruin_up(5, 10, .55), .7317, 5e-5) and close(ruin_up(10, 20, 18 / 37), .3680, 5e-5))
def paths_touch(n, k, m):   # brute force for small n
    cnt = 0
    for mask in range(1 << n):
        s = 0; mx = 0
        for i in range(n):
            s += 1 if mask >> i & 1 else -1; mx = max(mx, s)
        cnt += (s == k and mx >= m)
    return cnt
check('l11 s3: 28 of 70 paths to (8,0) touch 2; s4: all 56 to (8,2)', paths_touch(8, 0, 2) == 28 and paths_touch(8, 2, 2) == 56)
def max_ge(n, m):
    return sum(1 for mask in range(1 << n) if max(np.cumsum([1 if mask >> i & 1 else -1 for i in range(n)])) >= m)
check('l11 s5: 130 of 256 reach 2; s7: 6 of 16', max_ge(8, 2) == 130 and max_ge(4, 2) == 6)
check('l11 quiz: 45 of 252 touch 3 (n = 10); knock-out 29/64', paths_touch(10, 0, 3) == 45 and max_ge(6, 2) == 29)
# finding H: the count formula C(n, (n+2m-k)/2) is for k <= m only
finding('l11 s3: formula for paths to (n,k) touching m is stated "in general" but fails for k > m (n=6, k=4, m=2: 6 paths, formula gives 20)',
        'In general: $$\\\\#\\\\{\\\\text{paths to } (n, k) \\\\text{ touching } m\\\\}', 'l11-reflection', paths_touch(6, 4, 2) == 6 and comb(6, (6 + 4 - 4) // 2) == 20)
check('l11 s8 ballot: 42 of 210', sum(1 for mask in range(1 << 10) if bin(mask).count('1') == 6 and min(np.cumsum([1 if mask >> i & 1 else -1 for i in range(10)])) > 0) == 42)
p_le = lambda n, s: binom_cdf(n, .5, (n + s) // 2)     # P(S_n <= s)
check('l11 s9: 0.2517 + 0.1316 = 0.3833', close(p_le(20, -4), .2517, 5e-5) and close(p_le(20, -6), .1316, 5e-5))
def touch_prob(n, m, p):
    if m <= 0: return 1.0
    dist = {0: 1.0}; hit = 0.0
    for _ in range(n):
        new = {}
        for s, pr in dist.items():
            for step, q in ((1, p), (-1, 1 - p)):
                t2 = s + step
                if t2 >= m: hit += pr * q
                else: new[t2] = new.get(t2, 0.0) + pr * q
        dist = new
    return hit
exp = {(10, 3, .5): 0.34375, (20, 5, .5): 0.26317596435546875, (4, 2, .5): .375, (10, 3, .55): 0.4522591693984376, (20, 5, .45): 0.1504314999977528, (30, 4, .6): 0.8220312744287963}
check('hw3 touch_prob expected values', all(math.isclose(touch_prob(*k), v, rel_tol=1e-9) for k, v in exp.items()))
refl = lambda n, m, p: 2 * (1 - binom_cdf(n, p, (n + m + (1 if (n + m) % 2 else 0)) // 2 - 1)) if (n + m) % 2 else None
r1055 = (1 - binom_cdf(10, .55, 6)) * 2            # S_10 >= 3 and > 3 both mean K >= 7
r2055 = (1 - binom_cdf(20, .55, 12)) * 2           # S_20 >= 5 and > 5 both mean K >= 13
check('hw3: reflection misapplied at p = 0.55 gives 0.5321 (n=10, m=3) and 0.504 against 0.410 (n=20, m=5)',
      close(r1055, .5321, 5e-5) and close(r2055, .504, 6e-4) and close(touch_prob(20, 5, .55), .410, 6e-4), '%.4f %.4f %.4f' % (r1055, r2055, touch_prob(20, 5, .55)))
# hw3 tilt identity: P(max >= m) = P(S_n >= m) + E[(q/p)^(S_n - m); S_n > m]
n_, m_, p_ = 20, 5, .55; q_ = 1 - p_
tilt = sum(comb(n_, k) * p_ ** k * q_ ** (n_ - k) * ((1 if 2 * k - n_ >= m_ else 0) + ((q_ / p_) ** (2 * k - n_ - m_) if 2 * k - n_ > m_ else 0)) for k in range(n_ + 1))
check('hw3 long: the (q/p)^(S_n - m) weighting repairs reflection for p = 0.55', close(tilt, touch_prob(n_, m_, p_), 1e-12))
def hit_prob(n, m, trials, seed):
    rng = random.Random(seed); hits = 0
    for _ in range(trials):
        s = 0; hit = s >= m
        for _ in range(n):
            s += 1 if rng.random() < 0.5 else -1
            if s >= m: hit = True
        hits += hit
    return hits / trials
check('l12 s6 hidden tests pass for the taught solution', abs(hit_prob(10, 3, 20000, 1) - .34375) < .015 and abs(hit_prob(20, 5, 20000, 2) - .263176) < .015 and abs(hit_prob(4, 2, 20000, 3) - .375) < .015 and abs(hit_prob(1, 1, 20000, 4) - .5) < .015 and round(hit_prob(10, 3, 20000, 1), 2) == .34)
check('l12 s5 352/1024; s9 26.32; review-3 1093/4096', close(touch_prob(10, 3, .5), 352 / 1024) and close(100 * touch_prob(20, 5, .5), 26.32, 5e-3) and close(touch_prob(12, 4, .5), 1093 / 4096))
Phi = lambda z: .5 * (1 + math.erf(z / math.sqrt(2)))
check('l12 s3 Phi(-0.79) = 0.21, Phi(-0.05) = 0.48; l9 quiz Phi(-1.27) = 0.10', close(Phi(-.79), .21, 5e-3) and close(Phi(-.05), .48, 5e-4) and close(Phi(-1.27), .10, 5e-3))
l12 = load('l12-price-paths')
a = l12['screens'][0]['canvas']['left']['params']['series'][0]['values']
big = [i for i in range(1, len(a)) if a[i] / a[i - 1] - 1 < -.06]
check('l12 s0: Chart A falls of over 6% (simple) on days 71 and 106 only', big == [71, 106], str(big))
ra = l12['screens'][8]['canvas']['left']['params']['series'][0]['values']
big_log = [i + 1 for i, x in enumerate(ra) if x <= -6]
check('l12 s8 returns panel: falls beyond 6% on days 71, 106 and 115 (hint says "one fall of 6.5%")', big_log == [71, 106, 115], str(big_log))
# problems-3
check('p3 maker: exact P(P&L < 0) about 0.020', abs(binom_cdf(400, .55, 199) - .020) < 1.5e-3, '%.4f' % binom_cdf(400, .55, 199))
check('p3 barrier: 794 end at or below -4; touch 1588/4096', sum(comb(12, k) for k in range(5)) == 794 and close(touch_prob(12, 3, .5), 1588 / 4096))
check('p3 stake: 0.5026 and 0.5515', close(ruin_up(6, 10, .48), .5026, 5e-5) and close(ruin_up(3, 5, .48), .5515, 5e-5))
# finding L: the note's "fair price" uses up-chance 0.5 on a multiplicative tree, which is not a fair bet on the share
growth = .5 * 1.1 + .5 / 1.1
qrn = (1 - 1 / 1.1) / (1.1 - 1 / 1.1)
def touch_down(n, m, p):   # touching -m with up-chance p
    return touch_prob(n, m, 1 - p)
finding('p3 barrier note: "With no interest the fair price is the expected pay-out" under up-chance 0.5, though the share then grows %.4f a day on average; with the up-chance %.4f that makes the share a fair bet the note is worth %.2f, not 61.23'
        % (growth, qrn, 100 * (1 - touch_down(12, 3, qrn))),
        'With no interest the fair price is the expected pay-out.', 'problems-3', abs(growth - 1) > 1e-3)

# ------------------------------------------------------------------ seeded canvases (engine walk.js replicated)
def walk_paths(seed, paths, steps, p=.5, start=0):
    rng = mulberry((seed * 7919) & 0xFFFFFFFF); out = []
    for _ in range(paths):
        a = [start]
        for _ in range(steps):
            u = rng()
            g = 0.0
            while g <= 1e-12: g = rng()      # the engine draws a normal after each uniform
            rng()
            a.append(a[-1] + (1 if u < p else -1))
        out.append(a)
    return out
def first_hit(a, lo, hi):
    for i, v in enumerate(a):
        if (hi is not None and v >= hi) or (lo is not None and v <= lo): return i
    return -1
w = walk_paths(43, 1, 10)[0]
check('l9 s0: seed 43 path ends at 2', w[-1] == 2, str(w[-1]))
w = walk_paths(61, 1, 100)[0]
check('l9 s8: seed 61 path sits at 10 after 100 steps and is not below 0 after step 1', w[-1] == 10 and min(w[1:]) >= 0, 'end %d, min after step 1 %d' % (w[-1], min(w[1:])))
ws = walk_paths(11, 30, 150, start=3); hs = [first_hit(a, 0, 10) for a in ws]
check('l10 s0: 9 of 30 games reach 10 (all finished)', all(h >= 0 for h in hs) and sum(1 for a, h in zip(ws, hs) if a[h] >= 10) == 9,
      'unfinished %d, reached 10: %d' % (sum(h < 0 for h in hs), sum(1 for a, h in zip(ws, hs) if h >= 0 and a[h] >= 10)))
def mean_len(seed, paths, steps, start, lo, hi):
    hs = [first_hit(a, lo, hi) for a in walk_paths(seed, paths, steps, start=start)]
    return sum(h if h >= 0 else steps for h in hs) / paths, sum(h < 0 for h in hs)
m5, u5 = mean_len(6, 20, 120, 5, 0, 10); m1, u1 = mean_len(6, 20, 120, 1, 0, 10)
check('l10 s1: batch means about 25 bets from 5 and 7 from 1', round(m5) == 25 and round(m1) == 7, 'from 5: %.2f (%d unfinished), from 1: %.2f (%d unfinished)' % (m5, u5, m1, u1))
m50, u50 = mean_len(28, 20, 8000, 50, 0, 100)
check('l10 s3: the 20 games averaged 2,398 bets', round(m50) == 2398, '%.1f (%d unfinished)' % (m50, u50))
m0, u0 = mean_len(8, 20, 400, 0, -10, 10)
check('l10 s8: these 20 paths averaged 102', round(m0) == 102, '%.1f (%d unfinished)' % (m0, u0))
ws = walk_paths(32, 40, 10); hits = sum(max(a) >= 3 for a in ws)
check('l12 s5: 13 of 40 touch +3; bold path touches 3 on day 7 and ends at 0', hits == 13 and first_hit(ws[0], None, 3) == 7 and ws[0][-1] == 0, 'hits %d, first touch %d, end %d' % (hits, first_hit(ws[0], None, 3), ws[0][-1]))
w = walk_paths(781, 1, 200, start=100)[0]
check('l12 s7: seed 781 path goes from 100 to 140 in 200 days', w[-1] == 140, 'end %d, min %d' % (w[-1], min(w)))
ws = walk_paths(10, 40, 20); hits = sum(max(a) >= 5 for a in ws)
check('l12 s9: 10 of 40 touch +5', hits == 10, str(hits))

# ------------------------------------------------------------------ Monte Carlo of the headline theorems
rs = np.random.default_rng(20261111)
steps = rs.choice([-1, 1], size=(200000, 20)); S = steps.cumsum(axis=1)
est = (S.max(axis=1) >= 5).mean()
check('MC: reflection P(max_{j<=20} S_j >= 5) = 0.2632 (200,000 fair walks, 4 se = 0.004)', abs(est - .263176) < .004, '%.4f' % est)
steps = np.where(rs.random((200000, 20)) < .55, 1, -1); S = steps.cumsum(axis=1)
est = (S.max(axis=1) >= 5).mean()
check('MC: with p = 0.55 the touch chance is 0.410, not the 0.504 of the fair formula', abs(est - .410) < .005 and abs(est - .504) > .05, '%.4f' % est)
# gambler's ruin, biased: p = 0.48, i = 3, N = 5
pos = np.full(200000, 3); alive = np.ones(200000, bool); nsteps = np.zeros(200000)
while alive.any():
    mv = np.where(rs.random(alive.sum()) < .48, 1, -1); pos[alive] += mv; nsteps[alive] += 1
    alive &= (pos > 0) & (pos < 5)
check('MC: ruin formula 0.5515 for p = 0.48, i = 3, N = 5', abs((pos == 5).mean() - .5515) < .005, '%.4f' % (pos == 5).mean())
pos = np.full(100000, 5); alive = np.ones(100000, bool); nsteps = np.zeros(100000)
while alive.any():
    mv = rs.choice([-1, 1], size=alive.sum()); pos[alive] += mv; nsteps[alive] += 1
    alive &= (pos > 0) & (pos < 8)
check('MC: fair walk from 5 on 0..8 exits at 8 with chance 5/8 after 15 steps on average', abs((pos == 8).mean() - .625) < .007 and abs(nsteps.mean() - 15) < .25, '%.4f, %.2f' % ((pos == 8).mean(), nsteps.mean()))
# long-run share of time for the periodic Long/Flat/Short rule and non-convergence of P^k
PF = np.array([[0, 1, 0], [.5, 0, .5], [0, 1, 0]])
check('l6 s9: P(Flat) is 1 on day 100 and 0 on day 101 from Flat', close(mp(PF, 100)[1, 1], 1) and close(mp(PF, 101)[1, 1], 0))
# geometric run length is memoryless: P(L > 14 + n | L > 14) = P(L > n)
L = rs.geometric(.1, size=2_000_000)
check('MC: bull run memoryless, P(L > 15 | L > 14) = 0.9 and E[L - 14 | L > 14] = 10', abs((L > 15).sum() / (L > 14).sum() - .9) < .003 and abs((L[L > 14] - 14).mean() - 10) < .1)

print()
print('%d check(s) failing' % len(fails))
for f in fails: print('  -', f)
sys.exit(1 if fails else 0)
