"""Recompute every key of mock-oa-sig-2 and mock-oa-sig-3 twice, and check every distractor.

Run: <scratchpad>/venv/bin/python docs/reports/exam-mock-oa-sig-versions-numbers.py  (exit 0 when all pass)

For each item: `exact` is a closed form in Fractions; `second` is an independent method
(enumeration, a linear solve, a DP, or a seeded simulation with the stated tolerance).
The script then reads the two JSON files and checks:
  - a numeric answer equals the exact key to 1e-6; a choice's correct option shows the key
    at its printed precision;
  - every numeric `wrong` value is the named slip and lies outside the key's tolerance;
  - every choice distractor is the named slip, differs from the key, and no two options of an
    item lie within 0.01 of each other.
"""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as F
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.join(HERE, '..', '..', 'app', 'content', 'exams')
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def same(a, b, tol=F(0)):
    return abs(F(a) - F(b)) <= tol if not isinstance(a, float) and not isinstance(b, float) else abs(a - b) <= float(tol)


def solve(A, b):
    """Gaussian elimination over Fractions."""
    n = len(A)
    M = [list(map(F, row)) + [F(v)] for row, v in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                k = M[r][c] / M[c][c]
                M[r] = [x - k * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


rng = random.Random(20261109)
DIE = range(1, 7)
KEYS = {}   # (version, item id) -> (exact key, {distractor label: value})


def key(v, iid, exact, second, tol, slips):
    ok = abs(float(exact) - float(second)) <= tol
    check(ok, f'{v} {iid}: exact {float(exact):.6f} vs second {float(second):.6f} (tol {tol})')
    KEYS[(v, iid)] = (F(exact), {k: F(x) for k, x in slips.items()})


# ---------------- version 2 ----------------
v = 2
deck = [(r, s) for r in range(13) for s in range(4)]           # suits 0,1 red; 2,3 black
red = lambda c: c[1] < 2
pairs = [(a, b) for a in deck for b in deck if a != b]
same_col = F(sum(red(a) == red(b) for a, b in pairs), len(pairs))
key(v, 'q01-colour-match', 51 * F(25, 51), 51 * same_col, 0,
    {'with-replacement': F(51, 2), 'two-reds': 51 * F(26 * 25, 52 * 51), 'first-left-in': 26})

H5 = sum(F(1, k) for k in range(1, 6))
recs = sum(sum(1 for i in range(5) if p[i] == max(p[:i + 1])) for p in itertools.permutations(range(5)))
check(recs == 274, f'v2 q02 records total {recs}')
key(v, 'q02-records', H5, F(recs, 120), 0, {'half-each': F(5, 2), 'day-one': 1, 'no-day-one': H5 - 1})

G = F(4, 5)                       # G = (1/6)(4 + G)
check(G == F(1, 6) * (4 + G), 'v2 q03 first-step')
sim = 0
for _ in range(200000):
    pay = 0
    while rng.randint(1, 6) == 6:
        pay += 4
    sim += pay
key(v, 'q03-free-roll', G - 1, sim / 200000 - 1, 0.02,
    {'one-roll': F(4, 6) - 1, 'one-six': 3, 'fee-only': -1})

# two independent uniform swaps of 5 cards (fix pass): enumerate all 10 x 10 swap pairs
sw = list(itertools.combinations(range(5), 2))
home = 0
for s, t in itertools.product(sw, sw):
    p = list(range(5))
    for a, b in (s, t):
        p[a], p[b] = p[b], p[a]
    home += sum(p[i] == i for i in range(5))
one_swap = F(sum(sum(i not in s for i in range(5)) + 0 for s in sw), len(sw))
check(one_swap == 3, 'v2 q04 one swap leaves 3')
key(v, 'q04-two-swaps', 5 * (F(3, 5) ** 2 + F(2, 5) * F(1, 10)), F(home, 100), 0,
    {'no-return': 5 * F(3, 5) ** 2, 'one-swap': one_swap, 'shuffle': 1})

rolls = list(itertools.product(DIE, repeat=3))
rising = F(sum(a < b < c for a, b, c in rolls), 216)
key(v, 'q05-rising-order', F(comb(6, 3), 216), rising, 0,
    {'ties': F(1, 6), 'either': F(sum(a < b < c or a > b > c for a, b, c in rolls), 216),
     'different': F(sum(len({a, b, c}) == 3 for a, b, c in rolls), 216)})

first_and_two = F(4, 52) * F(comb(3, 1) * comb(48, 3), comb(51, 4))
two = F(comb(4, 2) * comb(48, 3), comb(52, 5))
key(v, 'q06-aces-in-a-hand', F(comb(4, 1), comb(5, 2)), first_and_two / two, 0,
    {'ignored': F(1, 13), 'one-ace': F(1, 5), 'even': F(1, 2)})

# you toss 3, colleague 2 (fix pass): exact by the tie route, second by enumerating 32 outcomes
t5 = list(itertools.product((0, 1), repeat=5))
more = sum(sum(s[:3]) > sum(s[3:]) for s in t5)
tie5 = F(sum(sum(s[:3]) == sum(s[3:]) for s in t5), 32)
tie22 = F(sum(comb(2, k) ** 2 for k in range(3)), 16)
check(more == 16 and tie22 == F(3, 8) and tie5 == F(5, 16), 'v2 q07 counts')
key(v, 'q07-one-more-toss', (1 - tie22) / 2 + tie22 / 2, F(more, 32), 0,
    {'ties-win': F(more, 32) + tie5, 'halved': (1 - tie5) / 2, 'by-tosses': F(3, 5)})

f = [0] * 1001                     # f[n]: worst-case guesses for n numbers, best strategy
for n in range(1, 1001):
    f[n] = min(1 + max(f[g - 1], f[n - g]) for g in range(1, n + 1))
kmin = next(k for k in range(1, 20) if 2 ** k - 1 >= 1000)
key(v, 'q08-guessing-game', kmin, f[1000], 0, {'log2-down': 9, 'ternary': 7, 'two-per-guess': 500})
check(2 ** 9 - 1 == 511, 'v2 q08 511')

p = F(1, 5)                        # 0.5 p + 0.5 = 0.6
check(F(1, 2) * p + F(1, 2) == F(3, 5), 'v2 q09 share')
yes = true_yes = 0
for _ in range(300000):
    t = rng.random() < 0.2
    says = t if rng.random() < 0.5 else True
    yes += says
    true_yes += says and t
key(v, 'q09-randomised-response', p / F(3, 5), true_yes / yes, 0.005,
    {'share': F(1, 5), 'said': F(3, 5), 'heads': F(1, 10) / F(3, 5)})

# remainder of the total mod 7: from r != 0 each roll goes to (r + j) mod 7, j = 1..6
idx7 = {r: r - 1 for r in range(1, 7)}
A = [[F(0)] * 6 for _ in range(6)]
for r in range(1, 7):
    A[idx7[r]][idx7[r]] += 1
    for j in DIE:
        t = (r + j) % 7
        if t:
            A[idx7[r]][idx7[t]] -= F(1, 6)
h = solve(A, [1] * 6)
first = 1 + F(1, 6) * sum(h)      # the first roll from 0 lands on 1..6
check(all(x == 6 for x in h), 'v2 q10 each non-zero remainder waits 6')
sim = 0
for _ in range(200000):
    t = n = 0
    while True:
        t += rng.randint(1, 6); n += 1
        if t % 7 == 0:
            break
    sim += n
check(abs(sim / 200000 - 7) < 0.05, 'v2 q10 simulation')
key(v, 'q10-multiple-of-seven', 1 + 6, first, 0, {'no-first': 6, 'by-mean': 2, 'long-run': F(7, 2)})

Vx = 100 - 20                       # (100 - V)^2 = 400
check((100 - Vx) ** 2 == 400 and F(Vx) == F(Vx) + F((100 - Vx) ** 2, 200) - 2, 'v2 q11 fixed point')
Vi = 50.0
for _ in range(2000):               # value iteration V <- E[max(U, V)] - 2, U uniform on 0..100
    Vi = Vi + (100 - Vi) ** 2 / 200 - 2 if Vi < 100 else Vi
check(abs(Vi - Vx) < 1e-6, 'v2 q11 value iteration')
# independent second route (fix pass): a stop-above-t rule is worth (100 + t)/2 - 2 * 100/(100 - t)
# (kept amount averages (100 + t)/2; draws are geometric with mean 100/(100 - t)); scan t, then simulate t = 80
best_t = max(range(100), key=lambda t: F(100 + t, 2) - F(200, 100 - t))
check(best_t == 80 and F(180, 2) - F(200, 20) == 80, f'v2 q11 threshold scan {best_t}')
net = 0.0
for _ in range(200000):
    n = 0
    while True:
        n += 1
        u = rng.random() * 100
        if u > 80:
            break
    net += u - 2 * n
check(abs(net / 200000 - 80) < 0.2, f'v2 q11 simulation {net / 200000}')
key(v, 'q11-cost-per-draw', Vx, net / 200000, 0.2,
    {'first-draw': 48, 'no-half': 100 - math.sqrt(200), 'average': 50})

tot = cnt = 0
for _ in range(400000):
    n = 0
    while True:
        n += 1
        r = rng.randint(1, 6)
        if r >= 5:
            break
    if r == 6:
        tot += n; cnt += 1
series = sum(F(n) * F(4, 6) ** (n - 1) * F(1, 6) for n in range(1, 400))
key(v, 'q12-conditional-wait', 3, tot / cnt, 0.02, {'plain': 6, 'five-faces': 5})
check(abs(float(series) - 1.5) < 1e-12, 'v2 q12 series 3/2')

A_ = ['r'] * 3 + ['b'] * 2
both = redd = 0
for i in range(5):
    B_ = ['r', 'r', 'b', 'b', A_[i]]
    for j in range(5):
        if B_[j] == 'r':
            redd += 1
            both += A_[i] == 'r'
check((both, redd) == (9, 13), 'v2 q13 pair counts')
post = F(3, 5) * F(3, 5) / (F(3, 5) * F(3, 5) + F(2, 5) * F(2, 5))
key(v, 'q13-transfer', post, F(both, redd), 0,
    {'prior': F(3, 5), 'joint': F(9, 25), 'red-draw': F(13, 25)})

num = den = F(0)
for buy, s1, s2 in itertools.product((True, False), (0, 1), (0, 1)):
    pr = (F(3, 10) if buy else F(7, 10)) * (F(1, 4) if s1 else F(3, 4)) * (F(1, 4) if s2 else F(3, 4))
    got = buy ^ bool(s1) ^ bool(s2)
    if got:
        den += pr
        num += pr if buy else 0
right = F(3, 4) ** 2 + F(1, 4) ** 2
key(v, 'q14-noisy-relay', F(3, 10) * right / (F(3, 10) * right + F(7, 10) * (1 - right)), num / den, 0,
    {'one-desk': F(3, 10) * F(3, 4) / (F(3, 10) * F(3, 4) + F(7, 10) * F(1, 4)), 'prior': F(3, 10), 'intact': right})

W = {}
def win(a, b):                      # Ann needs a, Bob needs b
    if a == 0: return F(1)
    if b == 0: return F(0)
    if (a, b) not in W:
        W[(a, b)] = (win(a - 1, b) + win(a, b - 1)) / 2
    return W[(a, b)]
pa = 1 - F(comb(4, 0) + comb(4, 1), 16)
key(v, 'q15-points-split', pa * 64, win(2, 3) * 64, 0,
    {'even': 32, 'by-won': F(64 * 2, 3), 'by-needed': F(64 * 3, 5)})

P1, P2, P3 = solve([[1, 0, F(-1, 3)], [F(-2, 3), 1, 0], [0, F(-2, 3), 1]], [0, F(1, 3), F(1, 3)])
b4 = solve([[1, 0, F(-1, 3)], [F(-2, 3), 1, 0], [0, F(-2, 3), 1]], [0, F(1, 3), 0])[0]   # end on 4
b5 = solve([[1, 0, F(-1, 3)], [F(-2, 3), 1, 0], [0, F(-2, 3), 1]], [0, 0, F(1, 3)])[0]   # end on 5
check(b4 == F(2, 23) and b5 == F(3, 23) and 4 * b4 + 5 * b5 == 1, 'v2 q16 fair-game check')
ok = 0
for _ in range(300000):
    m = 1
    while 0 < m < 4:
        m += 2 if rng.random() < 1 / 3 else -1
    ok += m >= 4
key(v, 'q16-uneven-steps', P1, ok / 300000, 0.005,
    {'fair': F(1, 4), 'two-wins': F(1, 9), 'no-return': F(1, 9) + F(2, 27)})

tot = F(0)
others = ['A', 'B']
for semi in [('F',), ('A',), ('B',)]:          # your semi-final opponent, each 1/3
    opp = semi[0]
    beat = {'F': F(3, 10), 'A': F(3, 5), 'B': F(3, 5)}
    rest = [x for x in ['F', 'A', 'B'] if x != opp]
    # the other semi: rest[0] vs rest[1]
    if 'F' in rest:
        o = [x for x in rest if x != 'F'][0]
        final = {'F': F(4, 5), o: F(1, 5)}
    else:
        final = {rest[0]: F(1, 2), rest[1]: F(1, 2)}
    tot += F(1, 3) * beat[opp] * sum(pf * beat[x] for x, pf in final.items())
closed = F(1, 3) * F(3, 10) * F(3, 5) + F(2, 3) * F(3, 5) * (F(4, 5) * F(3, 10) + F(1, 5) * F(3, 5))
check(tot == closed, 'v2 q17 loop matches closed form')
# independent second route (fix pass): seeded simulation of random draws and matches
beats = {('Y', 'F'): 0.3, ('Y', 'A'): 0.6, ('Y', 'B'): 0.6, ('F', 'A'): 0.8, ('F', 'B'): 0.8, ('A', 'B'): 0.5}
def play(x, y):
    p = beats[(x, y)] if (x, y) in beats else 1 - beats[(y, x)]
    return x if rng.random() < p else y
won = 0
for _ in range(400000):
    field = ['Y', 'F', 'A', 'B']
    rng.shuffle(field)
    won += play(play(field[0], field[1]), play(field[2], field[3])) == 'Y'
key(v, 'q17-knockout-draw', closed, won / 400000, 0.003, {'always-fav': F(18, 100), 'never-fav': F(36, 100)})

# ---------------- version 3 ----------------
v = 3
two_d = list(itertools.product(DIE, repeat=2))
pay = F(sum((a + b) * (2 if a == b else 1) for a, b in two_d), 36)
key(v, 'q01-doubled-payout', 7 + F(7, 6), pay, 0,
    {'no-doubling': 7, 'all-doubled': 14, 'one-double': 7 + F(7, 36)})

lev = 0
for s in itertools.product((1, -1), repeat=6):
    run = 0
    for x in s:
        run += x
        lev += run == 0
check(lev == 76, f'v3 q02 level points {lev}')
key(v, 'q02-returns-to-level', sum(F(comb(2 * k, k), 4 ** k) for k in (1, 2, 3)), F(lev, 64), 0,
    {'half-each': F(3, 2), 'toss-two': F(1, 2), 'toss-six': F(5, 16)})

key(v, 'q03-quoted-odds', F(40, 6) - F(50, 6), F(sum(40 if f_ == 6 else -10 for f_ in DIE), 6), 0,
    {'win-only': F(40, 6), 'stake-inside': F(30, 6) - F(50, 6), 'loss-only': -F(50, 6)})

inv = sum(sum(p[i] > p[j] for i in range(6) for j in range(i + 1, 6)) for p in itertools.permutations(range(6)))
key(v, 'q04-out-of-order', F(comb(6, 2), 2), F(inv, 720), 0,
    {'all-pairs': 15, 'neighbours': F(5, 2), 'per-order': 3})

roots = F(sum(b * b >= 4 * c for b, c in two_d), 36)
key(v, 'q05-dice-roots', F(0 + 1 + 2 + 4 + 6 + 6, 36), roots, 0,
    {'strict': F(sum(b * b > 4 * c for b, c in two_d), 36), 'no-four': F(sum(b * b >= c for b, c in two_d), 36)})
check(F(sum(b * b > 4 * c for b, c in two_d), 36) == F(17, 36), 'v3 q05 strict 17/36')

trip = list(itertools.permutations(range(1, 11), 3))
cond = [t for t in trip if t[0] > t[1]]
key(v, 'q06-rank-order', F(1, 3) / F(1, 2), F(sum(t[0] == max(t) for t in cond), len(cond)), 0,
    {'ignored': F(1, 3), 'even-contest': F(1, 2), 'one-order': F(1, 6)})

seq5 = list(itertools.product((0, 1), repeat=5))
third = F(sum(sum(s) == 3 and s[4] == 1 for s in seq5), 32)
key(v, 'q07-negative-binomial', F(comb(4, 2), 16) * F(1, 2), third, 0,
    {'any-order': F(comb(5, 3), 32), 'one-order': F(1, 32), 'no-fifth': F(comb(4, 2), 16)})

from functools import lru_cache
@lru_cache(None)
def mm(N, Wn, L):
    """Weighings still needed, adversary vs algorithm; N untried, Wn won only, L lost only."""
    if N == 0 and Wn == 1 and L == 1:
        return 0
    best = 10 ** 9
    moves = []
    if N >= 2: moves.append([(N - 2, Wn + 1, L + 1)])
    if N >= 1 and Wn >= 1: moves.append([(N - 1, Wn, L + 1), (N - 1, Wn, L)])      # untried vs winner
    if N >= 1 and L >= 1: moves.append([(N - 1, Wn + 1, L), (N - 1, Wn, L)])       # untried vs loser
    if Wn >= 2: moves.append([(N, Wn - 1, L)])
    if L >= 2: moves.append([(N, Wn, L - 1)])
    for outs in moves:
        best = min(best, 1 + max(mm(a, b, c) for a, b, c in outs))
    return best
key(v, 'q08-max-and-min', math.ceil(3 * 10 / 2) - 2, mm(10, 0, 0), 0,
    {'two-scans': 9 + 8, 'one-end': 9, 'one-round': 5})

pool = 1 - F(9, 10) ** 5
num = den = F(0)
for s in itertools.product((0, 1), repeat=5):
    pr = F(1)
    for x in s:
        pr *= F(1, 10) if x else F(9, 10)
    if any(s):
        den += pr
        num += pr * s[0]
key(v, 'q09-pooled-test', F(1, 10) / pool, num / den, 0,
    {'prior': F(1, 10), 'one-in-five': F(1, 5), 'pool': pool})

m = {}
for j in range(6, 0, -1):          # m_j = 1 + (1/6) sum_{i >= j} m_i
    m[j] = (1 + F(1, 6) * sum(m[i] for i in range(j + 1, 7))) / F(5, 6)
fs = 1 + F(1, 6) * sum(m.values())
check(all(m[j] == F(6, 5) ** (7 - j) for j in DIE), 'v3 q10 m_j pattern')
tail = sum(F(comb(k + 5, 5), 6 ** k) for k in range(0, 200))
key(v, 'q10-first-descent', F(6, 5) ** 6, fs, 0,
    {'e': F(math.e), 'indep': 1 + F(12, 5), 'no-last': F(6, 5) ** 6 - 1})
check(abs(float(tail) - float(F(6, 5) ** 6)) < 1e-12, 'v3 q10 tail sum')

# extinction: q = 1/4 + q/4 + q^2/2, smallest root in [0, 1]
qq = F(0)
for _ in range(200):
    qq = F(1, 4) + F(1, 4) * qq + F(1, 2) * qq ** 2
    qq = F(round(qq * 10 ** 15), 10 ** 15)
roots = sorted([(F(3) - 1) / 4, (F(3) + 1) / 4])      # (3 -+ sqrt(9 - 8)) / 4
check(roots == [F(1, 2), F(1)] and 2 * roots[0] ** 2 - 3 * roots[0] + 1 == 0, 'v3 q11 roots')
q2 = F(1, 4) + F(1, 4) * F(1, 4) + F(1, 2) * F(1, 4) ** 2
check(q2 == F(11, 32), 'v3 q11 two generations')
dead = 0
for _ in range(20000):
    pop = 1
    for _g in range(60):
        if pop == 0 or pop > 200:
            break
        new = 0
        for _i in range(pop):
            u = rng.random()
            new += 0 if u < 0.25 else (1 if u < 0.5 else 2)
        pop = new
    dead += pop == 0
check(abs(dead / 20000 - 0.5) < 0.015, f'v3 q11 simulation {dead / 20000}')
key(v, 'q11-extinction', roots[0], qq, F(1, 10 ** 9),
    {'first-step': F(1, 4), 'no-pair-term': F(1, 4) / (1 - F(1, 4)), 'two-generations': q2})
check(F(1, 3) == F(1, 4) + F(1, 4) * F(1, 3), 'v3 q11 slip q = 1/4 + q/4')
# fix pass: x < 1/2 maps below 1/2 (the map is increasing and fixes 1/2), checked on a grid
check(all(F(1, 4) + F(1, 4) * F(k, 1000) + F(1, 2) * F(k, 1000) ** 2 < F(1, 2) for k in range(500)),
      'v3 q11 map keeps [0, 1/2) below 1/2')

sim = 0.0
for _ in range(400000):
    x, y = rng.random(), rng.random()
    sim += min(x, 1 - x, y, 1 - y)
exact12 = F(1, 6)                   # int_0^{1/2} (1-2t)^2 dt = [-(1-2t)^3/6]_0^{1/2} = 1/6
check(4 * (F(1, 8) - F(1, 12)) == exact12, 'v3 q12 strip integral')
key(v, 'q12-nearest-side', exact12, sim / 400000, 0.002, {'one-way': F(1, 4), 'centre': F(1, 2)})

pa, find = F(3, 5), F(4, 5)
joint = pa * (1 - find) ** 2
one = pa * (1 - find) / (pa * (1 - find) + 1 - pa)
seq = one * (1 - find) / (one * (1 - find) + 1 - one)       # update twice
num = den = F(0)                                           # enumerate drawer and the two search results
for where, s1, s2 in itertools.product('AB', (0, 1), (0, 1)):
    pr = (pa if where == 'A' else 1 - pa)
    if where == 'A':
        pr *= (find if s1 else 1 - find) * (find if s2 else 1 - find)
    elif s1 or s2:
        pr = F(0)
    else:
        pr *= 1
    if not s1 and not s2:
        den += pr
        num += pr if where == 'A' else 0
check(one == F(3, 13) and seq == F(3, 53), 'v3 q13 sequential update')
check(joint / (joint + 1 - pa) == F(3, 53) and num / den == F(3, 53), 'v3 q13 old two-miss posterior')
# fix pass: q13-next-search, P(next search of A finds it | one miss)
nxt = one * find
num2 = den2 = F(0)                        # enumerate drawer, first search, second search
for where, s1, s2 in itertools.product('AB', (0, 1), (0, 1)):
    if where == 'A':
        pr = pa * (find if s1 else 1 - find) * (find if s2 else 1 - find)
    else:
        pr = (1 - pa) * (1 if not s1 and not s2 else 0)
    if not s1:
        den2 += pr
        num2 += pr if s2 else 0
check(nxt == F(12, 65) and num2 / den2 == F(96, 520), 'v3 q13 next search exact')
fnd = miss = 0
for _ in range(400000):
    inA = rng.random() < 0.6
    if inA and rng.random() < 0.8:
        continue                          # first search found it: not in the condition
    miss += 1
    fnd += inA and rng.random() < 0.8
check(abs(fnd / miss - 12 / 65) < 0.004, f'v3 q13 simulation {fnd / miss}')
key(v, 'q13-next-search', nxt, fnd / miss, 0.004,
    {'no-update': pa * find, 'in-A': one, 'sure-in-A': find})

desks = [1] * 50 + [2] * 30 + [4] * 20
traders = [s for s in desks for _ in range(s)]
mates = [s for s in traders if s > 1]
key(v, 'q14-size-bias', F(8, 10) / (F(6, 10) + F(8, 10)), F(sum(s == 4 for s in mates), len(mates)), 0,
    {'desks': F(20, 50), 'no-clue': F(8, 19), 'prior': F(1, 5)})

def length(p):
    E = F(0)
    for s in itertools.product((0, 1), repeat=5):
        pr = F(1)
        for x in s:
            pr *= p if x else 1 - p
        a = b = 0
        for i, x in enumerate(s):
            a += x; b += 1 - x
            if a == 3 or b == 3:
                break
        E += pr * (i + 1)
    return E
q = F(3, 5)
p3 = q ** 3 + (1 - q) ** 3
p4 = 3 * (q ** 3 * (1 - q) + (1 - q) ** 3 * q)
key(v, 'q15-series-length', 3 * p3 + 4 * p4 + 5 * (1 - p3 - p4), length(q), 0,
    {'even': length(F(1, 2)), 'full': 5, 'sweep': 3})
check(1 - p3 - p4 == 6 * q ** 2 * (1 - q) ** 2, 'v3 q15 game-five check')

ways = {s: sum(a + b == s for a, b in two_d) for s in range(2, 13)}
craps = F(ways[7] + ways[11], 36) + sum(F(ways[s], 36) * F(ways[s], ways[s] + 6) for s in (4, 5, 6, 8, 9, 10))
# second: first-step over the point states, solved as a linear system per point
craps2 = F(ways[7] + ways[11], 36)
for s in (4, 5, 6, 8, 9, 10):
    # h = P(win | point s) solves h = w/36 + (1 - w/36 - 6/36) h
    h = solve([[1 - (1 - F(ways[s], 36) - F(6, 36))]], [F(ways[s], 36)])[0]
    craps2 += F(ways[s], 36) * h
wins = 0
for _ in range(300000):
    t = rng.randint(1, 6) + rng.randint(1, 6)
    if t in (7, 11): wins += 1; continue
    if t in (2, 3, 12): continue
    while True:
        u = rng.randint(1, 6) + rng.randint(1, 6)
        if u == t: wins += 1; break
        if u == 7: break
check(abs(wins / 300000 - float(craps)) < 0.005, 'v3 q16 simulation')
key(v, 'q16-point-game', F(244, 495), craps2, 0,
    {'first-roll': F(8, 36), 'even-race': F(8, 36) + F(24, 36) * F(1, 2)})
check(craps == F(244, 495), 'v3 q16 closed form')
check(F(8, 36) == F(110, 495) and craps - F(8, 36) == F(134, 495), 'v3 q16 split shown in the explanation')

def rps_trans(n):
    """Distribution of players left after one round, over 3^n equally likely outcomes."""
    out = {}
    for g in itertools.product(range(3), repeat=n):
        s = set(g)
        if len(s) == 2:
            a, b = sorted(s)
            win_g = b if (b - a) % 3 == 1 else a      # 0 rock, 1 paper, 2 scissors: g beats g - 1
            left = sum(x == win_g for x in g)
        else:
            left = n
        out[left] = out.get(left, 0) + 1
    return out
Er = {1: F(0)}
for n in (2, 3, 4):
    tr = rps_trans(n)
    stay = F(tr.get(n, 0), 3 ** n)
    Er[n] = (1 + sum(F(c, 3 ** n) * Er[k] for k, c in tr.items() if k < n)) / (1 - stay)
check(rps_trans(4) == {4: 39, 3: 12, 2: 18, 1: 12}, f'v3 q17 transitions {rps_trans(4)}')
simr = 0
for _ in range(100000):
    n, r = 4, 0
    while n > 1:
        r += 1
        g = [rng.randrange(3) for _ in range(n)]
        s = set(g)
        if len(s) == 2:
            a, b = sorted(s)
            w = b if (b - a) % 3 == 1 else a
            n = sum(x == w for x in g)
    simr += r
check(abs(simr / 100000 - 45 / 14) < 0.03, 'v3 q17 simulation')
key(v, 'q17-elimination-rounds', F(45, 14), Er[4], 0, {'three': Er[3], 'one-exit': 3 * F(3, 2), 'two': Er[2]})


# ---------------- compare with the files ----------------
def parse(text):
    t = text.replace('−', '-').replace('£', '').replace('+', '').replace(',', '').strip()
    m = re.fullmatch(r'\$\\tfrac\{?(\d+)\}?\{?(\d+)\}?\$', t)
    if m:
        return F(int(m.group(1)), int(m.group(2))), 0
    dec = len(t.split('.')[1]) if '.' in t else 0
    return F(t), dec


for ver in (2, 3):
    d = json.load(open(os.path.join(EXAMS, f'mock-oa-sig-{ver}.json')))
    items = d['parts'][0]['items']
    check(len(items) == 17, f'v{ver}: {len(items)} items')
    for it in items:
        k = (ver, it['id'])
        check(k in KEYS, f'v{ver} {it["id"]}: no recomputation')
        if k not in KEYS:
            continue
        exact, slips = KEYS[k]
        w = it['widget']
        if w['kind'] == 'numeric':
            check(abs(w['answer'] - float(exact)) < 1e-6, f'{k}: answer {w["answer"]} vs {float(exact)}')
            check(len(w['wrong']) == len(slips), f'{k}: wrong count')
            for wr_ in w['wrong']:
                sv = slips.get(wr_['id'])
                check(sv is not None and abs(wr_['value'] - float(sv)) < 1e-6, f'{k}: wrong {wr_["id"]}')
                check(abs(wr_['value'] - float(exact)) > 0.005 + 1e-9, f'{k}: wrong {wr_["id"]} within tol of key')
        else:
            vals = []
            for o in w['options']:
                val, dec = parse(o['text'])
                vals.append((val, dec, o))
            cor = [x for x in vals if x[2].get('correct')]
            check(len(cor) == 1, f'{k}: one correct')
            val, dec, _ = cor[0]
            step = F(1, 10 ** dec) / 2 if dec else F(0)
            check(abs(val - exact) <= step + F(1, 10 ** 9), f'{k}: shown key {val} vs {float(exact)}')
            dist = [x for x in vals if not x[2].get('correct')]
            check(len(dist) == len(slips) == 3, f'{k}: distractor count')
            for sv in slips.values():
                hit = [x for x in dist if abs(x[0] - sv) <= (F(1, 10 ** x[1]) / 2 if x[1] else 0) + F(1, 10 ** 9)]
                check(len(hit) == 1, f'{k}: slip {float(sv):.4f} not shown exactly once')
            for a, b in itertools.combinations(vals, 2):
                check(abs(a[0] - b[0]) > F(1, 100), f'{k}: options {a[2]["text"]} and {b[2]["text"]} within 0.01')

if fails:
    print('\n'.join(fails))
    print(f'FAIL: {len(fails)}')
    sys.exit(1)
print(f'OK: {len(KEYS)} keys recomputed twice; distractors checked')
for (ver, iid), (ex, _) in sorted(KEYS.items()):
    print(f'v{ver} {iid:28s} {str(ex):>14s} {float(ex):.6f}')
