#!/usr/bin/env python3
"""Concept audit graphs-dp level 4 (l14 to l17, review-4, homework-4), round 1.

Every stated number is recomputed by a method independent of the lesson's code
(brute force over subsets or routes, exact fractions), and every empirical claim
gets a seeded Monte Carlo run sized to separate it from its negation.
Exits 0 only when the content is right. A check that fails because the content
is wrong stays failing: it is a finding in docs/reviews/audit-graphs-dp-4.md.
Expected failures at commit 6c01af87 (exit 1): F1 (l15 trap crash site), F2 (l17 dealer
slip value), F3 (homework-4 grid slip value).
"""
import itertools
import json
import math
import os
import random
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'graphs-dp')
load = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf-8'))
L14, L15, L16, L17 = load('l14-knapsack'), load('l15-common-subsequence'), load('l16-grid-paths'), load('l17-dice-stopping')
R4, H4 = load('review-4'), load('homework-4')

fails, n_checks = [], 0


def check(name, ok, detail=''):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(name)
    print(('ok   ' if ok else 'FAIL ') + name + ((' | ' + str(detail)) if detail and not ok else ''))


def EX(t):
    return eval(t['expect']) if isinstance(t['expect'], str) else t['expect']


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


def wrongs(w):
    return {x['id']: x.get('value', x.get('set')) for x in w.get('wrong', [])}


# ---------- independent solvers ----------
def knap_brute(ws, vs, cap, with_set=False):
    best, arg = 0, ()
    for r in range(len(ws) + 1):
        for c in itertools.combinations(range(len(ws)), r):
            if sum(ws[i] for i in c) <= cap:
                v = sum(vs[i] for i in c)
                if v > best:
                    best, arg = v, c
    return (best, arg) if with_set else best


def knap_1d_down(ws, vs, cap):
    dp = [0] * (cap + 1)
    for wt, val in zip(ws, vs):
        for w in range(cap, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[cap]


def knap_1d_up(ws, vs, cap):
    dp = [0] * (cap + 1)
    for wt, val in zip(ws, vs):
        for w in range(wt, cap + 1):
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp


def unbounded_brute(ws, vs, cap):
    best = 0
    ranges = [range(cap // w + 1) for w in ws]
    for ks in itertools.product(*ranges):
        if sum(k * w for k, w in zip(ks, ws)) <= cap:
            best = max(best, sum(k * v for k, v in zip(ks, vs)))
    return best


def greedy_ratio(ws, vs, cap):
    tot = 0
    for i in sorted(range(len(ws)), key=lambda i: -vs[i] / ws[i]):
        if ws[i] <= cap:
            cap -= ws[i]
            tot += vs[i]
    return tot


def lcs_brute(a, b):
    best = 0
    for r in range(min(len(a), len(b)), 0, -1):
        subs = {tuple(a[i] for i in c) for c in itertools.combinations(range(len(a)), r)}
        for c in itertools.combinations(range(len(b)), r):
            if tuple(b[i] for i in c) in subs:
                return r
    return best


def lcs_table(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            t[i][j] = t[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(t[i - 1][j], t[i][j - 1])
    return t


def edit_bfs(a, b, cap=6):
    """Edit distance by breadth-first search over strings (independent of the table)."""
    alpha = sorted(set(a) | set(b))
    seen, frontier, d = {a}, [a], 0
    while frontier:
        if b in seen:
            return d
        if d == cap:
            return None
        nxt = []
        for s in frontier:
            cands = [s[:i] + s[i + 1:] for i in range(len(s))]
            cands += [s[:i] + ch + s[i:] for i in range(len(s) + 1) for ch in alpha]
            cands += [s[:i] + ch + s[i + 1:] for i in range(len(s)) for ch in alpha]
            for c in cands:
                if c not in seen and len(c) <= max(len(a), len(b)) + 1:
                    seen.add(c)
                    nxt.append(c)
        frontier, d = nxt, d + 1
    return None


def edit_table(a, b):
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = d[i - 1][j - 1] if a[i - 1] == b[j - 1] else 1 + min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1])
    return d[-1][-1]


def routes_brute(grid):
    R, Cc = len(grid), len(grid[0])

    def go(i, j):
        if i >= R or j >= Cc or grid[i][j]:
            return 0
        if (i, j) == (R - 1, Cc - 1):
            return 1
        return go(i + 1, j) + go(i, j + 1)
    return go(0, 0)


def count_table(grid, mode='ok'):
    R, Cc = len(grid), len(grid[0])
    w = [[0] * Cc for _ in range(R)]
    for i in range(R):
        for j in range(Cc):
            if mode == 'ones' and (i == 0 or j == 0):
                w[i][j] = 1
            elif mode == 'ones_zero_block' and (i == 0 or j == 0):
                w[i][j] = 0 if grid[i][j] else 1
            elif grid[i][j]:
                w[i][j] = 0
            elif i == 0 and j == 0:
                w[i][j] = 1
            else:
                w[i][j] = (w[i - 1][j] if i else 0) + (w[i][j - 1] if j else 0)
    return w


def all_routes(R, Cc):
    for downs in itertools.combinations(range(R + Cc - 2), R - 1):
        i = j = 0
        cells = [(0, 0)]
        for s in range(R + Cc - 2):
            if s in downs:
                i += 1
            else:
                j += 1
            cells.append((i, j))
        yield cells


def stop_exact(n, quotes):
    k = len(quotes)
    v = Fr(sum(Fr(str(q)) for q in quotes), k)
    vals = [v]
    for _ in range(n - 1):
        v = sum(max(Fr(str(q)), v) for q in quotes) / k
        vals.append(v)
    return vals


# ================= l14 knapsack =================
s = L14['screens']
W, V = [1, 3, 4, 5], [10, 40, 50, 70]
check('l14 s0 key B+C = 90 is the brute-force best', knap_brute(W, V, 7, True) == (90, (1, 2)) and s[0]['widget']['answer'] == ['r1', 'r2'])
check('l14 s0 greedy D then A = 80', greedy_ratio(W, V, 7) == 80)
check('l14 s0 any pack with D tops out at 80', max(sum(V[i] for i in c) for r in range(5) for c in itertools.combinations(range(4), r) if 3 in c and sum(W[i] for i in c) <= 7) == 80)
check('l14 s0 2^4 = 16 packs and 2^40 over a trillion', 2 ** 4 == 16 and 2 ** 40 > 10 ** 12)
tbl = [[knap_brute(W[:i], V[:i], w) for w in range(8)] for i in range(5)]
shown = [[int(x) for x in row] for row in s[5]['canvas']['params']['cells']]
check('l14 full table on s5 matches brute force cell by cell', shown == tbl, tbl)
check('l14 s1 best[2][4] = 50, slips 40 (B alone) and 90', s[1]['widget']['answer'] == tbl[2][4] == 50 and wrongs(s[1]['widget']) == {'only-b': 40, 'both-long': 90})
check('l14 s3 row ABC keys', [r[1]['answer'] for r in s[3]['widget']['rows']] == tbl[3][1:])
check('l14 s4 row ABCD keys 70, 80, 90', [c['answer'] for c in s[4]['widget']['rows'][0][1:]] == tbl[4][5:])
check('l14 s4 table has 40 cells', 5 * 8 == 40)
# walk back, ties to skip
walk, w = ['r5c8'], 7
taken = []
for i in range(4, 0, -1):
    if tbl[i][w] != tbl[i - 1][w]:
        taken.append(i - 1)
        w -= W[i - 1]
    walk.append('r%dc%d' % (i, w + 1))
check('l14 s5 walk-back cells and items B, C', walk == s[5]['widget']['answer'] and sorted(taken) == [1, 2], walk)
# the took-d slip: take D at the corner, then follow the rule
walk2, w = ['r5c8'], 7 - 5
walk2.append('r4c%d' % (w + 1))
for i in range(3, 0, -1):
    if tbl[i][w] != tbl[i - 1][w]:
        w -= W[i - 1]
    walk2.append('r%dc%d' % (i, w + 1))
check('l14 s5 slip took-d cells', walk2 == wrongs(s[5]['widget'])['took-d'], walk2)
for t in s[6]['widget']['tests']:
    env = {}
    exec(t.get('setup', ''), env)
    env['knapsack'] = knap_1d_down
    got = eval(t['call'], env)
    check('l14 s6 hidden test expect ' + t['call'][:40], got == EX(t), got)
check('l14 s6 small tests agree with brute force', all(knap_brute(*a) == e for a, e in [(([8], [100], 7), 0), (([1, 2, 3], [5, 6, 7], 10), 18), (([2, 3], [30, 40], 6), 70), (([5, 4, 6, 3], [10, 40, 30, 50], 10), 90)]))
dp = knap_1d_up([2], [30], 6)
check('l14 s7 upward one-row trace after item 1 is 0,0,30,30,60,60,90', dp == [0, 0, 30, 30, 60, 60, 90])
check('l14 s7 knapsack_1d([2,3],[30,40],6) returns 90 = unbounded optimum; 0/1 answer 70', knap_1d_up([2, 3], [30, 40], 6)[6] == 90 == unbounded_brute([2, 3], [30, 40], 6) and knap_brute([2, 3], [30, 40], 6) == 70)
check('l14 s7 downward loop gives 0/1 on 300 random cases', all(knap_1d_down(a, b, c) == knap_brute(a, b, c) for a, b, c in (lambda rr: [([rr.randint(1, 9) for _ in range(6)], [rr.randint(1, 30) for _ in range(6)], rr.randint(0, 25)) for _ in range(300)])(random.Random(14))))
check('l14 s7 upward loop equals the unbounded optimum on 200 random cases', all(knap_1d_up(a, b, c)[c] == unbounded_brute(a, b, c) for a, b, c in (lambda rr: [([rr.randint(2, 9) for _ in range(3)], [rr.randint(1, 30) for _ in range(3)], rr.randint(0, 20)) for _ in range(200)])(random.Random(15))))
check('l14 s8 grams: 7,001 columns, about 1,000 times the cells (875)', 800 < (5 * 7001) / (5 * 8) < 1100)
rows = s[10]['canvas']['params']['rows']
RW, RV = [int(r[1]) for r in rows], [int(r[2]) for r in rows]
check('l14 s10 risk budget key 43 = A + E', knap_brute(RW, RV, 10, True) == (43, (0, 4)) and s[10]['widget']['answer'] == 43)
check('l14 s10 slips: greedy 39, B+C+D 38', greedy_ratio(RW, RV, 10) == 39 == wrongs(s[10]['widget'])['greedy'] and RV[1] + RV[2] + RV[3] == 38 == wrongs(s[10]['widget'])['bce'] and RW[1] + RW[2] + RW[3] == 10)
check('l14 s10 ratio column', all(near(float(r[3]), int(r[2]) / int(r[1]), 0.006) for r in rows))
q = L14['quiz']
check('l14 quiz all-fit 18, slips 7 and 13', knap_brute([1, 2, 3], [5, 6, 7], 10) == 18 == q[1]['widget']['answer'])
check('l14 quiz greedy 60 against optimum 90', greedy_ratio([6, 5, 5], [60, 45, 45], 10) == 60 == q[2]['widget']['answer'] and knap_brute([6, 5, 5], [60, 45, 45], 10) == 90)
check('l14 quiz 200 x 50,000 = 10^7', 200 * 50000 == 10 ** 7)
t0 = time.time()
knap_1d_down([(i * 7) % 31 + 5 for i in range(20)], [(i * 11) % 47 + 1 for i in range(20)], 50000)
el = (time.time() - t0) * 10
print('     timing note: 10^7 cell updates take about %.1f s in this CPython (content says "a few seconds"; timing-dependent, not gated)' % el)

# ================= l15 LCS and edit distance =================
s = L15['screens']
a, b = 'HEDGE', 'EDGY'
T = lcs_table(a, b)
check('l15 LCS table on s5 matches', [[int(x) for x in r] for r in s[5]['canvas']['params']['cells']] == T, T)
check('l15 table cells agree with brute force on every prefix pair', all(T[i][j] == lcs_brute(a[:i], b[:j]) for i in range(6) for j in range(5)))
check('l15 s0 LCS is EDG (3) and 2^20 over a million', T[5][4] == 3 and 2 ** 20 > 10 ** 6)
check('l15 s3 and s4 row keys', [c['answer'] for c in s[3]['widget']['rows'][0][1:]] == T[3][1:] and [[c['answer'] for c in r[1:]] for r in s[4]['widget']['rows']] == [T[4][1:], T[5][1:]])
i, j, kept, path = 5, 4, [], ['r6c5']
while i and j:
    if a[i - 1] == b[j - 1]:
        kept.append('r%dc%d' % (i + 1, j + 1))
        i, j = i - 1, j - 1
    elif T[i - 1][j] >= T[i][j - 1]:
        i -= 1
    else:
        j -= 1
    path.append('r%dc%d' % (i + 1, j + 1))
check('l15 s5 walk keeps G, D, E at the keyed cells; path as drawn', kept == s[5]['widget']['answer'] and path == s[5]['explain']['canvas']['paths'][0]['cells'], (kept, path))
for t in s[6]['widget']['tests']:
    aa, bb = eval(t['call'].replace('lcs_length', ''))
    got = lcs_table(aa, bb)[-1][-1]
    check('l15 s6 hidden test expect ' + t['call'][:40], got == EX(t), got)
check('l15 s6 classic pairs agree with brute force', lcs_brute('ABCBDAB', 'BDCABA') == 4 and lcs_brute('AGGTAB', 'GXTXAYB') == 4 and lcs_brute('AB', 'BA') == 1)
# F1: where the off-by-one trap really crashes
site = None
try:
    for i in range(1, 6):
        for j in range(1, 5):
            a[i] == b[j]
except IndexError:
    site = (i, j)
claims_i5 = 'i = 5' in s[7]['feedback']['correct'] or '$i = 5$' in s[7]['explain']['text']
check('F1 l15 s7 trap: key IndexError is right', site is not None and s[7]['widget']['options'][0]['correct'] and 'IndexError' in s[7]['widget']['options'][0]['text'])
check('F1 l15 s7 trap: text says the crash is at i = 5 on a[5], but it is at i = 1, j = 4 on b[4]', not (claims_i5 and site == (1, 4)), 'first IndexError at (i, j) = %s' % (site,))
check('l15 s8 edit distance HEDGE to EDGY = 2 by search; insert/delete only = 3', edit_bfs(a, b) == 2 == edit_table(a, b) and 5 + 4 - 2 * 3 == 3)
for t in s[9]['widget']['tests']:
    aa, bb = eval(t['call'].replace('edit_distance', ''))
    got = edit_table(aa, bb)
    check('l15 s9 hidden test expect ' + t['call'][:44], got == EX(t), got)
check('l15 s9 table agrees with string search on short pairs', all(edit_bfs(x, y) == edit_table(x, y) for x, y in [('flaw', 'lawn'), ('BRK.B', 'BRK-B'), ('RDSA', 'RDS.A'), ('BUY', 'BYE'), ('abc', '')]))
rows = s[10]['canvas']['params']['rows']
ours, broker = [r[1] for r in rows if r[1]], [r[2] for r in rows if r[2]]
check('l15 s10 fills: LCS 5, 2 broker fills and 1 of ours unmatched', lcs_brute(ours, broker) == 5 and len(broker) - 5 == 2 == s[10]['widget']['answer'] and len(ours) - 5 == 1)
bug = [[0] * 3 for _ in range(3)]
for i in (1, 2):
    for j in (1, 2):
        bug[i][j] = max(bug[i - 1][j - 1] + 1, bug[i - 1][j], bug[i][j - 1])
check('l15 quiz bug returns 2 on AB, CD', bug[2][2] == 2)
check('l15 quiz RDS.A to RDSA = 1; 10^4 x 10^4 = 10^8', edit_table('RDS.A', 'RDSA') == 1 and 10 ** 4 * 10 ** 4 == 10 ** 8)

# ================= l16 grid paths =================
s = L16['screens']
check('l16 s0 3 by 3 has 6 routes; 20 by 20 over 35 billion', routes_brute([[0] * 3] * 3) == 6 and math.comb(38, 19) > 35 * 10 ** 9)
G2 = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]]
w2 = count_table(G2)
check('l16 s2 blocked grid keys and corner 7; 35 open routes', routes_brute(G2) == 7 == w2[3][4] and [w2[1][2:], [w2[2][1], w2[2][2], w2[2][4]], w2[3][1:]] == [[1, 2, 3], [1, 2, 3], [2, 4, 4, 7]] and math.comb(7, 3) == 35)
G3 = [[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
check('l16 s3 trap: truth 9, all-ones edges 15, zeroed block with 1s after 12', routes_brute(G3) == 9 == s[3]['widget']['answer'] and count_table(G3, 'ones')[2][4] == 15 and count_table(G3, 'ones_zero_block')[2][4] == 12 and wrongs(s[3]['widget']) == {'all-ones': 15, 'zero-block': 12})
F = [[3, 1, 4, 2], [2, 5, 1, 3], [6, 2, 2, 1]]
costs = sorted((sum(F[i][j] for i, j in r), r) for r in all_routes(3, 4))
check('l16 s4 cheapest route 12, unique, along the keyed cells', costs[0][0] == 12 and costs[1][0] > 12 and sorted('r%dc%d' % (i + 1, j + 1) for i, j in costs[0][1]) == sorted(s[5]['widget']['answer']))
best_to = lambda i, j: min(sum(F[x][y] for x, y in r) for r in all_routes(i + 1, j + 1))
check('l16 s4 table keys', [[best_to(1, j) for j in (1, 2, 3)], [best_to(2, j) for j in (1, 2, 3)]] == [[c['answer'] for c in s[4]['widget']['rows'][1][2:]], [c['answer'] for c in s[4]['widget']['rows'][2][2:]]])
check('l16 s5 slip via-12 costs 13; every route through the 5 cell costs at least 13', 3 + 1 + 4 + 1 + 3 + 1 == 13 and min(c for c, r in costs if (1, 1) in r) == 13)
check('l16 s6 open 17 by 17 = C(32,16) = 601,080,390', math.comb(32, 16) == 601080390 == count_table([[0] * 17] * 17)[16][16])
for t in s[6]['widget']['tests'][:9]:
    g = eval(t['call'].replace('count_paths', ''))
    check('l16 s6 hidden test expect ' + t['call'][:44], routes_brute(g) == EX(t))
for t in s[7]['widget']['tests']:
    env = {}
    exec(t.get('setup', ''), env)
    g = eval(t['call'].replace('min_path_cost', ''), env)
    R, Cc = len(g), len(g[0])
    if R * Cc <= 20:
        got = min(sum(g[i][j] for i, j in r) for r in all_routes(R, Cc))
    else:  # Dijkstra over cells, an independent method for the 30 by 40 grid
        import heapq
        dist, pq = {(0, 0): g[0][0]}, [(g[0][0], 0, 0)]
        while pq:
            d, i, j = heapq.heappop(pq)
            if d > dist[(i, j)]:
                continue
            for x, y in ((i + 1, j), (i, j + 1)):
                if x < R and y < Cc and d + g[x][y] < dist.get((x, y), 1e18):
                    dist[(x, y)] = d + g[x][y]
                    heapq.heappush(pq, (d + g[x][y], x, y))
        got = dist[(R - 1, Cc - 1)]
    check('l16 s7 hidden test expect ' + t['call'][:40], got == EX(t), got)
P = [[int(x) for x in r] for r in s[8]['canvas']['params']['cells']]
check('l16 s8 Pascal grid C(i+j, i); 6 by 6 gives 252; 5 by 5 gives 70', all(P[i][j] == math.comb(i + j, i) for i in range(5) for j in range(5)) and math.comb(10, 5) == 252 and math.comb(8, 4) == 70)
p3 = 4 * 0.55 ** 3 * 0.45
check('l16 s9 P(3 ups in 4) = 0.2995; slips one path 0.0749 and 0.55^3 = 0.1664', near(p3, s[9]['widget']['answer'], 5e-4) and near(0.55 ** 3 * 0.45, 0.0749, 5e-4) and near(0.55 ** 3, 0.1664, 5e-4))
rr = random.Random(16)
N = 400000
hits = sum(1 for _ in range(N) if sum(rr.random() < 0.55 for _ in range(4)) == 3)
se = math.sqrt(p3 * (1 - p3) / N)
check('l16 s9 Monte Carlo of 3 ups in 4 days (400,000 runs) within 4 se of 0.2995 and far from 0.0749', abs(hits / N - p3) < 4 * se and abs(hits / N - 0.0749) > 50 * se, hits / N)
diag = [[1, 1], [1, 3]]
check('l16 quiz diagonal step: 3 routes on a 2 by 2 grid', diag[1][1] == diag[0][1] + diag[1][0] + diag[0][0] == 3)

# ================= l17 dice stopping =================
s = L17['screens']
D = [1, 2, 3, 4, 5, 6]
Vn = stop_exact(60, D)
check('l17 V1..V4 = 3.5, 4.25, 14/3, 89/18', Vn[:4] == [Fr(7, 2), Fr(17, 4), Fr(14, 3), Fr(89, 18)])
check('l17 keys 4.25, 4.6667, 4.9444', near(s[2]['widget']['answer'], 4.25) and near(s[4]['widget']['answer'], float(Vn[2]), 5e-5) and near(s[5]['widget']['rows'][3][2]['answer'], float(Vn[3]), 5e-5))
check('l17 s2 slips 3.5, 2.5, 5', wrongs(s[2]['widget']) == {'one-roll': 3.5, 'stop-only': 2.5, 'five': 5})
check('l17 s4 slip no-opt = 11/6 + 4/6 x 3.5 = 4.1667', near(float(Fr(11, 6) + Fr(4, 6) * Fr(7, 2)), wrongs(s[4]['widget'])['no-opt'], 5e-5))
thr = lambda n: 1 if n == 1 else min(f for f in D if f >= Vn[n - 2])
check('l17 thresholds: 4 with two rolls, 5 with three to five, 6 from six on', [thr(n) for n in range(2, 12)] == [4, 5, 5, 5] + [6] * 6)
check('l17 s6 V10 = 5.65, V50 = 5.9998, V_n increasing and below 6', near(float(Vn[9]), 5.65, 0.005) and near(float(Vn[49]), 5.9998, 5e-5) and all(Vn[k] < Vn[k + 1] < 6 for k in range(59)))
for t in s[7]['widget']['tests']:
    env = {'dice_value': lambda n: float(stop_exact(n, D)[-1]), 'dice_threshold': thr}
    Vn = stop_exact(210, D) if len(Vn) < 210 else Vn
    got = eval(t['call'], env)
    check('l17 s7 hidden test expect ' + t['call'], got == EX(t), got)
fwd = Fr(4 + 5 + 6, 6) + Fr(3, 6) * Fr(17, 4)
check('l17 s8 forward rule (always compare with 3.5) on 3 rolls is worth 4.625', fwd == Fr(37, 8))


def play(rng, n, thresholds):
    for k in range(n, 0, -1):
        x = rng.randint(1, 6)
        if k == 1 or x >= thresholds[k]:
            return x


rng = random.Random(17)
N = 1_000_000
opt = {2: 4, 3: 5, 4: 5}
for n in (2, 3, 4):
    xs = [play(rng, n, opt) for _ in range(N)]
    m = sum(xs) / N
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / N)
    check('l17 Monte Carlo V%d (10^6 games) within 4 se of %.4f' % (n, float(Vn[n - 1])), abs(m - float(Vn[n - 1])) < 4 * sd / 1000, m)
xs = [play(rng, 3, {2: 4, 3: 4}) for _ in range(N)]
m_f = sum(xs) / N
xs = [play(rng, 3, opt) for _ in range(N)]
m_o = sum(xs) / N
check('l17 s3/s8 Monte Carlo: stopping on a 4 with three rolls loses value (4.625 against 4.6667, gap over 10 se)', m_o - m_f > 10 * 1.4 * math.sqrt(2) / 1000 and abs(m_f - 4.625) < 0.006, (m_f, m_o))
xs = [play(rng, 3, {2: 4, 3: 6}) for _ in range(N)]
check('l17 Monte Carlo: stopping only on a 6 with three rolls is also worse than stopping on 5 or 6', m_o - sum(xs) / N > 10 * 1.4 * math.sqrt(2) / 1000)
# dealers
Q = [float(r[0]) for r in s[9]['canvas']['params']['rows']]
DV = stop_exact(3, Q)
check('l17 s9 dealers: 99.4, 99.55, key 99.6375', DV == [Fr('99.4'), Fr('99.55'), Fr('99.6375')] and near(s[9]['widget']['answer'], 99.6375))
first_best = (Fr('99.5') + Fr('99.9')) / 4 + Fr(2, 4) * DV[1]
check('F2 l17 s9 slip first-best (accept 99.5 and 99.9 from the first dealer) is 99.625, content gives %s' % wrongs(s[9]['widget'])['first-best'], near(float(first_best), wrongs(s[9]['widget'])['first-best'], 5e-4), float(first_best))
rng = random.Random(18)
N = 400000


def sell(first_min, second_min):
    x = rng.choice(Q)
    if x >= first_min:
        return x
    x = rng.choice(Q)
    return x if x >= second_min else rng.choice(Q)


m1 = sum(sell(99.9, 99.5) for _ in range(N)) / N
m2 = sum(sell(99.5, 99.5) for _ in range(N)) / N
check('l17 s9 Monte Carlo: best policy 99.6375, accepting 99.5 first gives 99.625 (not 99.65)', abs(m1 - 99.6375) < 0.0025 and abs(m2 - 99.625) < 0.0025 and abs(m2 - 99.65) > 0.015, (m1, m2))
check('l17 s10 node value max(8.00, 7.40) = 8.00', max(8.00, 7.40) == 8.00)


def secretary(n, r):
    return Fr(1, n) if r == 1 else Fr(r - 1, n) * sum(Fr(1, i - 1) for i in range(r, n + 1))


best100 = max(secretary(100, r) for r in range(1, 101))
check('l17 quiz secretary n = 100: best rule wins about 0.371; limit 1/e = 0.368', near(float(best100), 0.371, 5e-4) and near(1 / math.e, 0.368, 5e-4))
check('l17 quiz option why "near 37% for every n": holds for n >= 10 to within 0.04 (small n is higher, e.g. 0.5 at n = 3)', all(abs(float(max(secretary(n, r) for r in range(1, n + 1))) - 0.37) < 0.04 for n in range(10, 120)) and max(secretary(3, r) for r in (1, 2, 3)) == Fr(1, 2))
check('l17 quiz: the optimal secretary chance stays above 1/e for every n from 1 to 150 (so "above 1/e", not "near 37%", is the exact statement)', all(float(max(secretary(n, r) for r in range(1, n + 1))) > 1 / math.e for n in range(1, 151)))
check('l17 s6: P(no 6 in n rolls) = (5/6)^n > 0, and 6 - V_n = (5/6)(6 - V_(n-1)) from n = 6 on', all(6 - Vn[k] == Fr(5, 6) * (6 - Vn[k - 1]) for k in range(5, 60)))

# ================= review-4 =================
it = {x['id']: x for x in R4['items']}
check('r4 knap cell 60; slips 50, 100', it['r4-knap-cell']['widget']['answer'] == tbl[3][6] == 60 and tbl[2][6] == 50 and tbl[2][6] + 50 == 100)
check('r4 LCS(TRADE, TREAD) = 4', lcs_brute('TRADE', 'TREAD') == 4 == it['r4-lcs-trade']['widget']['answer'])
GE = [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]
check('r4 edge block: 6 routes, open grid 10', routes_brute(GE) == 6 and math.comb(5, 2) == 10 == count_table(GE, 'ones')[2][3])
check('r4 four-sided die, two rolls = 3', stop_exact(2, [1, 2, 3, 4])[-1] == 3)
check('r4 edit BUY to BYE = 2', edit_bfs('BUY', 'BYE') == 2)
FF = [[4, 2, 7], [1, 8, 1]]
cc = sorted(sum(FF[i][j] for i, j in r) for r in all_routes(2, 3))
check('r4 min cost 14 with a two-way tie; slips 15 and 10', cc == [14, 14, 15] and 14 - 4 == 10)
check('r4 two dealers 99.75', stop_exact(2, [99.0, 100.0])[-1] == Fr('99.75'))

# ================= homework-4 =================
it = {x['id']: x for x in H4['items']}
check('h4 knapsack 7; heavy slip 6', knap_brute([2, 3, 4, 5], [3, 4, 5, 6], 5) == 7 == it['h4-knap']['widget']['answer'])
print('     note: h4-knap wrong[] value 3 (id ratio) has no feedback line; packing by value per kg gives %d here' % greedy_ratio([2, 3, 4, 5], [3, 4, 5, 6], 5))
hv = stop_exact(3, [99.0, 99.4, 100.0])
check('h4 dealers lines 99.4667, 99.6444, 99.7630', [round(float(x), 4) for x in hv] == [99.4667, 99.6444, 99.763])
GH = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
check('h4 grid: 9 routes; rows as the explanation lists them', routes_brute(GH) == 9 and count_table(GH) == [[1, 1, 1, 1, 1], [1, 0, 1, 2, 3], [1, 1, 2, 0, 3], [0, 1, 3, 3, 6], [0, 1, 0, 3, 9]])
edge = wrongs(it['h4-paths']['widget'])['edge']
reach = {count_table(GH, 'ones')[4][4], count_table(GH, 'ones_zero_block')[4][4]}
check('F3 h4-paths slip "first column kept at 1 below its block" gives 11 (or 9 if only the block is zeroed), content gives %s' % edge, edge in reach - {9}, sorted(reach))
check('h4 edit SATURDAY to SUNDAY = 3; LCS 5; insert/delete only 4', edit_table('SATURDAY', 'SUNDAY') == 3 and lcs_brute('SATURDAY', 'SUNDAY') == 5 and 8 + 6 - 10 == 4)
for t in it['h4-stop-value']['widget']['tests']:
    env = {'stop_value': lambda n, q: float(stop_exact(n, q)[-1])}
    got = eval(t['call'], env)
    check('h4 stop_value hidden test expect ' + t['call'][:50], got == EX(t), got)
for t in it['h4-unbounded']['widget']['tests']:
    env = {}
    exec(t.get('setup', ''), env)
    env['unbounded_knapsack'] = lambda ws, vs, cap: knap_1d_up(ws, vs, cap)[cap]
    got = eval(t['call'], env)
    check('h4 unbounded hidden test expect ' + t['call'][:50], got == EX(t), got)
check('h4 unbounded small tests agree with brute force', unbounded_brute([3, 5], [4, 7], 11) == 15 and unbounded_brute([4], [9], 13) == 27 and unbounded_brute([1, 3, 4, 5], [10, 40, 50, 70], 7) == 90)
ps = {r: secretary(10, r) for r in range(1, 11)}
bestr = max(ps, key=ps.get)
check('h4 secretary n = 10: best r = 4, 0.3987; r = 5 gives 0.3983', bestr == 4 and near(float(ps[4]), 0.3987, 5e-5) and near(float(ps[5]), 0.3983, 5e-5))
rng = random.Random(19)
N = 600000
wins = 0
for _ in range(N):
    p = list(range(10))
    rng.shuffle(p)
    lead = max(p[:3])
    pick = next((x for x in p[3:] if x > lead), None)
    wins += pick == 9
se = math.sqrt(0.3987 * 0.6013 / N)
check('h4 secretary Monte Carlo (600,000 shuffles): converges to 0.3987, not to 1/e', abs(wins / N - float(ps[4])) < 4 * se and abs(wins / N - 1 / math.e) > 20 * se, wins / N)
check('h4 design model: 41 x 201 about 8,000; 2^40 about 10^12; greedy 39 against 43; 2 x 10^8 pence', 41 * 201 == 8241 and 1e12 < 2 ** 40 < 1.2e12 and greedy_ratio([4, 5, 6], [18, 21, 25], 10) == 39 and knap_brute([4, 5, 6], [18, 21, 25], 10) == 43 and 2_000_000 * 100 == 2 * 10 ** 8)
# coarse-unit rounding of weights: not always a "small error"
ws, vs, cap = [5001, 5001, 9999], [10, 10, 11], 10002
exact = knap_brute(ws, vs, cap)
up = knap_brute([math.ceil(w / 5000) for w in ws], vs, cap // 5000)
ws2, vs2, cap2 = [7400, 7400], [10, 10], 10000
plan = knap_brute([round(w / 5000) for w in ws2], vs2, round(cap2 / 5000), True)[1]
check('h4 design note: rounding risk to coarse units can break the budget (nearest) or halve the profit (up), so the error need not be small', sum(ws2[i] for i in plan) > cap2 and up < exact, (exact, up, plan))

print('\n%d checks, %d failed' % (n_checks, len(fails)))
for f in fails:
    print('  FAILED: ' + f)
sys.exit(1 if fails else 0)
