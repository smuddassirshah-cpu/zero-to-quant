#!/usr/bin/env python3
"""Concept audit, round 2: markov levels 1 to 3 (blind reader).

Run from the repo root: python3 docs/reports/markov-L1-3-concepts-r2.py
Recomputes graded keys, wrong[] slips and stated numbers by exact arithmetic,
reproduces the seeded walk canvases from the engine's generator (mulberry32,
app/js/engine/sim.js and canvas/walk.js), runs each code solution against its
hidden tests (and checks the starter fails), and confirms the main results by
exact dynamic programming or seeded Monte Carlo.
Exits 0 when every check passes. A check that fails because the content is
wrong is left failing on purpose and is a finding (see the audit).
"""
import json, math, os, random, sys
from fractions import Fraction as F
from math import comb, sqrt, erf

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CD = os.path.join(ROOT, 'app', 'content', 'courses', 'markov')
_cache = {}
def J(f):
    if f not in _cache:
        _cache[f] = json.load(open(os.path.join(CD, f + '.json')))
    return _cache[f]

n_checks = 0
fails = []
def ok(cond, label):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(label)
        print('FAIL', label)
def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol

def item(f, loc):
    d = J(f)
    part = None
    if '.' in loc:
        loc, part = loc.split('.')
    kind, i = loc[0], int(loc[1:])
    it = {'s': d.get('screens'), 'q': d.get('quiz'), 'i': d.get('items')}[kind][i]
    if part is not None:
        it = it['parts'][int(part[1:])]
    return it

def K(f, loc, ans, tol=None, **wrong):
    """Check a numeric key and each named slip value against a recomputation."""
    w = item(f, loc)['widget']
    t = tol if tol is not None else (w.get('tol', {}).get('abs', 0) or 1e-9)
    ok(close(w['answer'], ans, max(t, 1e-9)), f'{f} {loc} key {w["answer"]} vs {float(ans):.6g}')
    have = {x['id']: x for x in w.get('wrong', [])}
    for k, v in wrong.items():
        k = k.replace('_', '-')
        if k not in have:
            ok(False, f'{f} {loc} wrong id {k} missing')
            continue
        tw = have[k].get('tol', {}).get('abs', 0) or 1e-9
        ok(close(have[k]['value'], v, max(tw, 1e-9)), f'{f} {loc} slip {k} {have[k]["value"]} vs {float(v):.6g}')
    # no slip value may fall inside the key's tolerance
    for k, x in have.items():
        if 'value' in x:
            ok(abs(x['value'] - w['answer']) > t, f'{f} {loc} slip {k} collides with key')

def T(f, loc, *cells):
    """Check the editable cells of a table widget, in reading order."""
    w = item(f, loc)['widget']
    got = [c for row in w['rows'] for c in row if isinstance(c, dict) and c.get('edit')]
    ok(len(got) == len(cells), f'{f} {loc} table cell count')
    for c, v in zip(got, cells):
        ok(close(c['answer'], v, max(c.get('tol', {}).get('abs', 0), 1e-9)), f'{f} {loc} cell {c["answer"]} vs {float(v):.6g}')

def correct(f, loc):
    w = item(f, loc)['widget']
    return [o['id'] for o in w['options'] if o.get('correct')]

def mat(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mpow(A, k):
    R = [[F(int(i == j)) for j in range(len(A))] for i in range(len(A))]
    for _ in range(k):
        R = mat(R, A)
    return R
def Fm(rows):
    return [[F(str(x)) for x in r] for r in rows]
def solve(A, b):
    """Gaussian elimination over fractions."""
    n = len(A)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        M[c] = [x / M[c][c] for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                M[r] = [x - M[r][c] * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]
def stationary(P):
    n = len(P)
    A = [[(P[j][i] - (1 if i == j else 0)) for j in range(n)] for i in range(n - 1)] + [[1] * n]
    return solve(A, [0] * (n - 1) + [1])
def absorb(P):
    """H and t for an absorbing chain given as fractions."""
    n = len(P)
    ends = [i for i in range(n) if P[i][i] == 1]
    mov = [i for i in range(n) if P[i][i] != 1]
    A = [[(1 if i == j else 0) - P[i][j] for j in mov] for i in mov]
    t = solve(A, [1] * len(mov)) if mov else []
    H = {e: solve(A, [P[i][e] for i in mov]) for e in ends} if mov else {}
    return mov, ends, t, H
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
def ruin(i, N, p):
    if p == F(1, 2):
        return F(i, N)
    r = (1 - p) / p
    return (1 - r ** i) / (1 - r ** N)
def touch(n, m, p):
    """Exact chance a +-1 walk from 0 reaches m >= 1 (or m <= -1) within n steps."""
    if m < 0:
        return touch(n, -m, 1 - p)
    dist, hit = {0: 1.0}, 0.0
    for _ in range(n):
        new = {}
        for s, pr in dist.items():
            for st, q in ((1, p), (-1, 1 - p)):
                if s + st >= m:
                    hit += pr * q
                else:
                    new[s + st] = new.get(s + st, 0.0) + pr * q
        dist = new
    return hit
def binom_ge(n, k, p=0.5):
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(max(k, 0), n + 1))

# ---------- the engine's seeded generator ----------
M32 = 0xFFFFFFFF
def imul(a, b):
    return (a * b) & M32
def mulberry32(seed):
    a = [int(seed) & M32]
    def nxt():
        a[0] = (a[0] + 0x6D2B79F5) & M32
        t = a[0]
        t = imul(t ^ (t >> 15), t | 1)
        t = (t ^ ((t + imul(t ^ (t >> 7), t | 61)) & M32)) & M32
        return ((t ^ (t >> 14)) & M32) / 4294967296
    return nxt
def walk_paths(seed, paths, steps, p=0.5, start=0, run=0):
    """canvas/walk.js: per path, per step, one uniform then one Box-Muller normal (two more uniforms)."""
    rng = mulberry32((seed * 7919 + run * 104729) & M32)
    out = []
    for _ in range(paths):
        us = []
        for _ in range(steps):
            us.append(rng())
            u = 0.0
            while u <= 1e-12:
                u = rng()
            rng()
        a = [start]
        for u in us:
            a.append(a[-1] + (1 if u < p else -1))
        out.append(a)
    return out
def first_hit(a, lo, hi):
    for i, x in enumerate(a):
        if (hi is not None and x >= hi) or (lo is not None and x <= lo):
            return i
    return -1

# =====================================================================
# Level 1
# =====================================================================
W = Fm([[0.6, 0.3, 0.1], [0.3, 0.4, 0.3], [0.2, 0.5, 0.3]])
BB = Fm([[0.9, 0.1], [0.2, 0.8]])
CR = Fm([[0.9, 0.09, 0.01], [0.05, 0.85, 0.1], [0, 0, 1]])
f = 'l1-only-now'
ok(item(f, 's0')['widget']['answer'] == ['C'], 'l1 s0 most likely after Rain')
path = 'SRRSSCRCCCCCSSSC'
ok(path[1] == 'R' and path[6] == 'R' and path[2] == 'R' and path[7] == 'C' and path[0] == 'S' and path[5] == 'C', 'l1 s1 days quoted')
idx = {'S': 0, 'C': 1, 'R': 2}
ok(all(W[idx[a]][idx[b]] > 0 for a, b in zip(path, path[1:])), 'l1 s1 path is possible under the chain')
K(f, 's2', 0.3, into_rain=1 - 0.1 - 0.3, one_arrow=0.7, loop=0.4)
K(f, 's3', 0.2 * 0.6, added=0.8, second=0.6, first=0.2, from_rain_twice=0.04)
ok(correct(f, 's4') == ['closed'], 'l1 s4 7 steps from Open')
ok(correct(f, 's5') == ['cannot'], 'l1 s5')
ok(sorted(item(f, 's6')['widget']['answer']) == ['UD', 'UU'], 'l1 s6')
K(f, 's8', 0.3 * 0.6 * 0.35, added=1.25, last=0.35, direct=0.15, two=0.105)
K(f, 's9', 0.45 * 0.6, from_up=0.36, down_row=0.2025, used_055=0.33, added=1.05)
px = item(f, 's9')['canvas']['params']['series'][0]['values']
ok(all(min(abs(b / a - 1.01), abs(b / a - 0.99)) < 2e-4 for a, b in zip(px, px[1:])), 'l1 s9 series moves 1% a day')
K(f, 'q0', 0.09, added=0.6, one=0.3)
K(f, 'q1', 0.01, minus_b=0.93, minus_a=0.08)
K(f, 'q3', 8, two=2, three=3, six=6, four=4)

f = 'l2-transition-matrix'
W2, W3 = mpow(W, 2), mpow(W, 3)
c = item(f, 's1')['canvas']['derive']
for name, col in (('S', 0), ('C', 1), ('R', 2)):
    vals = json.loads(c['values.' + name].rsplit('[', 1)[0])
    for k, v in enumerate(vals):
        exact = float(mpow(W, k)[2][col])
        ok(abs(v - exact) < 0.00051, f'l2 s1 bar {name} k={k} {v} vs {exact:.5f}')
K(f, 's1', W2[2][0], one_day=0.2, later=W3[2][0], rain=W2[2][2])
lv = item(f, 's2')['canvas']['params']['leaves']
ok(close(lv['S-S'], 0.12) and close(lv['C-S'], 0.15) and close(lv['R-S'], 0.06), 'l2 s2 leaves')
C2 = item(f, 's3')['canvas']['params']['matrices'][2]['rows']
ok(all(close(C2[i][j], W2[i][j]) for i in range(3) for j in range(3)), 'l2 s3 P squared')
K(f, 's3', W2[0][2], squared=0.01, one_path=0.06, rain_row=W2[2][2], one_step=0.1)
pi0 = [F('0.7'), 0, F('0.3')]
pi1 = [sum(pi0[i] * W[i][j] for i in range(3)) for j in range(3)]
ok([float(x) for x in pi1] == [0.48, 0.36, 0.16], 'l2 s4 pi1')
K(f, 's4', pi1[2], col_conv=sum(W[2][j] * pi0[j] for j in range(3)), col_sum=0.7, sunny_only=0.07, rain_only=0.09)
ok(correct(f, 's5') == ['I'], 'l2 s5')
K(f, 's6', W2[0][0], squared=0.36, one_step=0.6, forgot_rain=0.45)
ok(close(0.36 + 0.09 + 0.01, 0.46), 'l2 s6 squared row sum')
CR2, CR3 = mpow(CR, 2), mpow(CR, 3)
ok([float(x) for x in CR2[0]] == [0.8145, 0.1575, 0.028], 'l2 s8 row A of P squared')
K(f, 's8', CR3[0][2], three_times=0.03, no_migration=1 - 0.99 ** 3, two_years=0.028, cubed=1e-6)
ok(float(CR3[0][2]) == 0.051895 and close(0.1575 * 0.1, 0.01575) and close(0.8145 * 0.01, 0.008145), 'l2 s8 routes')
K(f, 'q0', mpow(BB, 2)[1][0], squared=0.04, one_path=0.18, other=0.16)
K(f, 'q1', 0.55, row=0.5, col_sum=1.1, bull_only=0.45)
# quiz[0] 'squared' and quiz[3] 'entry' feedback say an entrywise product keeps one path/route.
# Off the diagonal p_ij^2 is not the chance of any two-step path from i to j (the lesson's own trap says so).
p = BB
two_step_paths_bear_bull = [p[1][0] * p[0][0], p[1][1] * p[1][0]]
ok(p[1][0] ** 2 in two_step_paths_bear_bull, 'FINDING 1 (fails on purpose) l2 quiz[0] byKey.squared: 0.2^2 "keeps one path", yet it is the chance of no two-step path from bear to bull')
# quiz[3] option 'entry': (P^2)_ij (P^3)_ij "keeps one route through the middle". A route is (P^2)_im (P^3)_mj for one m.
P2, P3 = mpow(W, 2), mpow(W, 3)
off_diag = [P2[i][j] * P3[i][j] in [P2[i][m] * P3[m][j] for m in range(3)] for i in range(3) for j in range(3) if i != j]
on_diag = [P2[i][i] * P3[i][i] in [P2[i][m] * P3[m][i] for m in range(3)] for i in range(3)]
ok(all(on_diag) and not any(off_diag), 'l2 quiz[3] option entry (finding 2, imprecise): an entrywise product is a route term on the diagonal only')

f = 'l3-never-leave'
L3 = Fm([[0.5, 0.5, 0, 0, 0], [0.3, 0, 0.3, 0.4, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0.6, 0.4], [0, 0, 0, 0.7, 0.3]])
c = item(f, 's1')['canvas']['derive']
for col, name in enumerate('ABCDE'):
    vals = json.loads(c['right:values.' + name].rsplit('[', 1)[0])
    for k, v in enumerate(vals):
        ok(abs(v - float(mpow(L3, k)[0][col])) < 0.00051, f'l3 s1 bar {name} k={k}')
P20 = mpow(L3, 20)
ok(abs(float(P20[0][2]) - 0.43) < 0.005 and abs(float(P20[0][3] + P20[0][4]) - 0.57) < 0.005, 'l3 s1 0.43 and 0.57')
K(f, 's2', 0.5 + 0.5 * 0.3, loop_only=0.5, added=0.8, always=1, via_b=0.15)
ok(sorted(item(f, 's3')['widget']['answer']) == ['A', 'B'], 'l3 s3 transient')
G4 = Fm([[1, 0, 0, 0, 0], [0.5, 0, 0.5, 0, 0], [0, 0.5, 0, 0.5, 0], [0, 0, 0.5, 0, 0.5], [0, 0, 0, 0, 1]])
G44 = mpow(G4, 4)
K(f, 's5', G44[2][0] + G44[2][4], two_bets=0.5, certain=1, one_end=G44[2][4], quarter=0.25)
ok(item(f, 's6')['widget']['answer'] == ['def'], 'l3 s6')
CR4, CR5 = mpow(CR, 4), mpow(CR, 5)
bars = item(f, 's9')['canvas']['state']['values']
for k, key in enumerate(['y1', 'y2', 'y3', 'y4', 'y5'], 1):
    ok(abs(bars[key] - float(mpow(CR, k)[0][2])) < 0.00006, f'l3 s9 bar {key}')
K(f, 's9', CR3[0][2] - CR2[0][2], cumulative=CR3[0][2], one_step=0.01, year2=0.018, summed=0.01 + 0.028 + 0.0519)
K(f, 'q1', 0.7, one=1, three=0.3)
K(f, 'q3', CR5[0][2] - CR4[0][2], cumulative=CR5[0][2], summed=0.1911)

f = 'l4-regimes'
ok(correct(f, 's0') == ['right'] and close(mpow(BB, 3)[0][0], 0.781) and close(0.9 ** 3, 0.729), 'l4 s0')
ok(abs(sum(n * 0.9 ** (n - 1) * 0.1 for n in range(1, 4000)) - 10) < 1e-9, 'l4 s2 geometric mean 10')
K(f, 's3', 5, recip_stay=1.25, bull=10, leave=0.2, odds=4)
K(f, 's4', F(2, 3), stay=0.9, half=0.5, bear=F(1, 3))
ok(stationary(BB) == [F(2, 3), F(1, 3)], 'l4 s4 steady state')
ok(abs(1 - 0.9 ** 14 - 0.77) < 0.005, 'l4 s5 0.77')
for k in range(13):
    Pk = mpow(BB, k)
    ok(close(Pk[0][0] - Pk[1][0], F(7, 10) ** k), f'l4 s6 gap k={k}')
K(f, 's6', 9, eight=8, mean=10, five=5, two=2)
ok(0.7 ** 8 > 0.05 > 0.7 ** 9, 'l4 s6 threshold')
seq = ''.join(item(f, 's8')['canvas']['left']['params']['cells'] + item(f, 's8')['canvas']['right']['params']['cells'])
cnt = {a + b: 0 for a in 'UD' for b in 'UD'}
for a, b in zip(seq, seq[1:]):
    cnt[a + b] += 1
T(f, 's8', cnt['UU'], cnt['UD'], F(cnt['UU'], cnt['UU'] + cnt['UD']), cnt['DU'], cnt['DD'], F(cnt['DD'], cnt['DU'] + cnt['DD']))
ok(seq.count('U') == 16 and len(seq) == 20, 'l4 s8 16 U periods')
K(f, 's9', 0.2 * 12.5 + 0.8 * 4, bull_row=0.9 * 12.5 + 0.1 * 4, long_run=F(2, 3) * F(25, 2) + F(1, 3) * 4, today=4, avg=8.25)
K(f, 's10', 1 / 0.15, subtract=1 / 0.15 - 4, total=1 / 0.15 + 4, leave=0.15, recip_stay=1 / 0.85)
K(f, 'q0', 20, recip=1 / 0.95, odds=19)
K(f, 'q1', 0.4, trace=1.4, det_ish=0.48, diff=0.2)
K(f, 'q2', 0.75, stay=0.95, half=0.5, bear=0.25)

f = 'fluency-l2-transition-matrix'
fam = J(f)['families']
ok(fam[0]['let']['key'] == 'if(i == 0, a, b)*if(j == 0, a, 1 - a) + if(i == 0, 1 - a, 1 - b)*if(j == 0, b, 1 - b)', 'fluency family 0 key is (P^2)_ij')
ok(fam[1]['let']['key'].startswith('a1*if(j == 1, a1') and 'a3*if(j == 1, c1' in fam[1]['let']['key'], 'fluency family 1 key is row Sunny times column j')
ok(fam[2]['let']['key'] == 'u*if(j == 0, a, 1 - a) + (1 - u)*if(j == 0, b, 1 - b)', 'fluency family 2 key is pi P')
for r in fam[1]['vars']['r1']['pick'] + fam[1]['vars']['r2']['pick'] + fam[1]['vars']['r3']['pick']:
    ok(close(sum(r), 1), 'fluency family 1 rows add to 1')

f = 'review-1'
K(f, 'i1', 0.6, column=0.8, one_only=0.85)
K(f, 'i2', 0.34, col_conv=0.9 * 0.2 + 0.1 * 0.8, unweighted=1.1, today=0.2)
K(f, 'i3', W2[1][2], squared=0.09, one_path=0.12, one_step=0.3)
ok(W[1][2] * W[2][2] == F('0.09'), 'review-1 i3: here 0.3 squared is the path Cloudy, Rain, Rain')
ok(correct(f, 'i4') == ['s3'], 'review-1 i4')
K(f, 'i5', 0.75, one_bet=0.5, win_end=0.25, certain=1)
K(f, 'i6', 4, recip=4 / 3, odds=3)
ok(abs(1 - 0.9 ** 10 - 0.65) < 0.005 and correct(f, 'i7') == ['right'], 'review-1 i7')
K(f, 'i8', 2.5, ratio=1.5, recip_stay=1 / 0.6, total=25)

f = 'homework-1'
K(f, 'i0', 8, none=0, twelve=12, four=4)
OF = Fm([[0.7, 0.3], [0.4, 0.6]])
K(f, 'i1', mpow(OF, 2)[0][0], squared=0.49, one=0.7, col=0.58)
ok(mpow(OF, 2)[0][0] > stationary(OF)[0], 'homework-1 i1 persistence remark')
R3 = Fm([[0.8, 0.15, 0.05], [0.2, 0.7, 0.1], [0.1, 0.3, 0.6]])
v0 = [F('0.5'), F('0.4'), F('0.1')]
v1 = [sum(v0[i] * R3[i][j] for i in range(3)) for j in range(3)]
v2 = [sum(v1[i] * R3[i][j] for i in range(3)) for j in range(3)]
T(f, 'i2', *v1, *v2)
CB = Fm([[0.85, 0.12, 0.03], [0.1, 0.75, 0.15], [0, 0, 1]])
T(f, 'i3', 0.15, mpow(CB, 2)[1][2], mpow(CB, 3)[1][2], mpow(CB, 3)[1][2] - mpow(CB, 2)[1][2])
ok(sorted(correct(f, 'i4')) == ['s3', 's4', 's5'], 'homework-1 i4')
h = F('0.3') / (1 - F('0.2'))
K(f, 'i5', F('0.6') + F('0.4') * h, no_loop2=0.72, loop=0.6, one=1)
ok(item(f, 'i7')['widget']['answer'] == 'a+b-1', 'homework-1 i7')
ok(close(0.25 + 0.75 * 0.8 ** 4, 0.5572) and close(0.4428 * 24 + 0.5572 * 8, 15.0848), 'homework-1 longform (d), (e)')
SC = Fm([[0.95, 0.05], [0.15, 0.85]])
ok([float(x) for x in mpow(SC, 2)[1]] == [0.27, 0.73] and abs(float(mpow(SC, 4)[1][1]) - 0.5572) < 5e-5 and stationary(SC) == [F(3, 4), F(1, 4)], 'homework-1 longform matrix')
ok(190 + 10 + 9 + 51 == 260 and abs(200 / 261 - 0.766) < 0.0005, 'homework-1 longform counts')

f = 'problems-1'
K(f, 'i0.p0', 0.7, of_all=14 / 60, over_stays=14 / 48, into_d=0.5)
K(f, 'i0.p1', 0.7 * 0.7 + 0.3 * 0.15, stay_path=0.49, d_stays=0.49 + 0.3 * 0.85, row_twice=0.58)
K(f, 'i0.p2', 1 / 0.3, used_stay=1 / 0.7, further=0.7 / 0.3, two_step=1 / (1 - 0.535))
K(f, 'i0.p3', F(1, 3), equal=0.5, swapped=F(2, 3), stay_ratio=0.7 / 1.55)
TL = Fm([[0.7, 0.3, 0], [0.4, 0, 0.6], [0, 0, 1]])
K(f, 'i1.p0', 0.3 * 0.4 * 0.3 * 0.6, iid=0.3 * 0.7 * 0.3 * 0.3, last_loss=0.3 * 0.4 * 0.3 * 0.3, win_after_loss=0.3 * 0.7 * 0.3 * 0.6)
K(f, 'i1.p1', mpow(TL, 2)[0][2], loss_squared=0.09, one_step=0.6, path_l=0.21)
K(f, 'i1.p2', mpow(TL, 3)[0][2], new_only=0.126, no_step=0.39, loss_low=0.243)
K(f, 'i1.p3', mpow(TL, 4)[0][2] - mpow(TL, 3)[0][2], cumulative=mpow(TL, 4)[0][2], trade_three=0.126, from_w=0.366)
MC = Fm([[0.9, 0.1, 0], [0.5, 0.3, 0.2], [0, 0, 1]])
K(f, 'i2.p0', 0.5 + 0.3 * 0.5, on_day_two=mpow(MC, 2)[1][0], one_day=0.5, added=0.8)
K(f, 'i2.p1', F(5, 7), two_days=0.65, one_day=0.5, no_x=0.625)
K(f, 'i2.p2', F(34, 35), loop_only=0.9, one_day=0.95, two_days=0.965, via_m=F(1, 14))
ok(correct(f, 'i2.p3') == ['liquidated'], 'problems-1 margin p3')
K(f, 'i3.p0', 1 / 0.3, used_stay=1 / 0.7, further=7 / 3, calm=20)
K(f, 'i3.p1', F(6, 7), stay_ratio=0.95 / 1.65, used_stay=20 / (20 + 1 / 0.7), swapped=F(1, 7), equal=0.5)
K(f, 'i3.p2', F(10, 7), equal=-2.5, used_stay=(20 * 3 - 8 / 0.7) / (20 + 1 / 0.7), sign=F(26, 7), swapped=F(-45, 7))
K(f, 'i3.p3', -4.7, stays=-8, calm_row=2.45, long_run=F(10, 7), swapped=-0.3)
K(f, 'i3.p4', F(6, 7) * F('2.45'), ignores_switch=F(18, 7), unweighted=2.45, always_on=F(10, 7), gain=4.7 / 7)

# =====================================================================
# Level 2
# =====================================================================
f = 'l5-where-it-settles'
for k in (0, 1, 5, 30):
    Pk = mpow(BB, k)
    ok(close(Pk[0][0], 2 / 3 + 0.7 ** k / 3) and close(Pk[1][0], 2 / 3 - 2 * 0.7 ** k / 3), f'l5 s0 closed form k={k}')
T(f, 's1', F(2, 3), F(1, 3))
SG = Fm([[0.95, 0.05], [0.15, 0.85]])
K(f, 's2', stationary(SG)[0], half=0.5, swap=0.25, ratio=3, diag=0.95)
V3 = Fm([[0.75, 0.25, 0], [0.1, 0.75, 0.15], [0, 0.25, 0.75]])
pv = stationary(V3)
T(f, 's3', pv[1] / pv[0], pv[2] / pv[0], *pv)
ok(correct(f, 's4') == ['right'] and abs(0.97 ** 100 - 0.048) < 0.0005, 'l5 s4')
ok(correct(f, 's5') == ['right'] and pv[2] == F(3, 10) and abs(1 / sqrt(3) - 0.577) < 0.0005, 'l5 s5')
K(f, 's8', F(2, 3) * F('0.02') - F(1, 3) * F('0.03'), simple=-0.005, diag=0.015, swapped=F(1, 3) * F('0.02') - F(2, 3) * F('0.03'))
ok(correct(f, 'q0') == ['right'] and stationary(Fm([[0.6, 0.4], [0.2, 0.8]]))[0] == F(1, 3), 'l5 q0')
K(f, 'q1', 0.55, same=0.5, bear=0.45)
K(f, 'q2', 150, even=100, diag=180, swap=50)

f = 'l6-always-settle'
SL = Fm([[0.1, 0.9], [0.9, 0.1]])
for k in (0, 1, 2, 7, 20):
    ok(close(mpow(SL, k)[0][0], 0.5 + 0.5 * (-0.8) ** k), f'l6 s2 closed form k={k}')
ok(abs(0.5 + 0.5 * 0.8 ** 20 - 0.506) < 0.0005, 'l6 s2 0.506')
K(f, 's1', 0.5, one=1, zero=0)
ok(correct(f, 's3') == ['right'] and 100 % 3 == 1, 'l6 s3')
E5 = Fm([[0.5, 0.5, 0, 0, 0], [0.25, 0.75, 0, 0, 0], [0, 0, 0.8, 0.2, 0], [0, 0, 0.2, 0.8, 0], [0.5, 0, 0.5, 0, 0]])  # A, B, C, D, E
lim = mpow(E5, 200)
ok(abs(float(lim[4][1]) - 1 / 3) < 1e-9 and abs(float(lim[0][1]) - 2 / 3) < 1e-9 and lim[2][1] == 0, 'l6 s5 limits by start')
K(f, 's5', F(1, 3), inside=F(2, 3), fifth=0.2, half=0.5)
her = [F(1, 6), F(1, 3), F(1, 4), F(1, 4), 0]
ok([sum(her[i] * E5[i][j] for i in range(5)) for j in range(5)] == her, 'l6 s6 her vector is stationary')
ok(all(abs(float(lim[4][j]) - float(her[j])) < 1e-9 for j in range(5)), 'l6 s6 it is the limit from E')
ok(correct(f, 's7') == ['right'], 'l6 s7')
LFS = Fm([[0, 1, 0], [0.5, 0, 0.5], [0, 1, 0]])
ok(stationary(LFS) == [F(1, 4), F(1, 2), F(1, 4)] and mpow(LFS, 100)[1][1] == 1 and mpow(LFS, 101)[1][1] == 0, 'l6 s9')
T(f, 's9', 0.5, 0, 1)
K(f, 'q1', 2, one=1, three=3)
K(f, 'q2', F(5, 9), half=0.5, stay=0.2, swap=F(4, 9))
ok(correct(f, 'q3') == ['right'] and 10 % 4 == 2, 'l6 q3')

f = 'l7-how-long'
def walk_chain(N, up=F(1, 2), stay=F(0)):
    P = [[F(0)] * (N + 1) for _ in range(N + 1)]
    P[0][0] = P[N][N] = F(1)
    for i in range(1, N):
        P[i][i + 1] = up * (1 - stay); P[i][i - 1] = (1 - up) * (1 - stay); P[i][i] = stay
    return P
mov, ends, t3, H3 = absorb(walk_chain(3))
K(f, 's1', t3[0], one=1, half=0.5, three=3)
T(f, 's3', *absorb(walk_chain(4))[2])
IG = Fm([[0.85, 0.14, 0.01], [0.05, 0.9, 0.05], [0, 0, 1]])
T(f, 's4', *absorb(IG)[2])
ok(sorted(correct(f, 's5')) == ['a2', 'cinf', 'x0'], 'l7 s5')
lazy = walk_chain(3, stay=F(1, 2))
ok(correct(f, 's6') == ['right'] and absorb(lazy)[2][0] == 4, 'l7 s6 lazy walk 4')
ok(solve([[F(1, 4), 0], [0, F(1, 4)]], [F(5, 4), F(5, 4)])[0] == 5, 'l7 s6 slip 5 with t = 1 at the ends')
OQ = Fm([[0.6, 0.3, 0, 0.1], [0, 0.5, 0.4, 0.1], [0, 0, 1, 0], [0, 0, 0, 1]])  # Back, Front, Filled, Cancelled
mov, ends, tq, Hq = absorb(OQ)
K(f, 's8', tq[0], back_only=2.5, add=4.5, cancel=10, front=tq[1])
K(f, 'q0', 5, inv=1.25, four=4, p=0.8)
K(f, 'q3', 3, back=2, four=4)

f = 'l8-which-end'
ok(correct(f, 's0') == ['right'] and H3[3] == [F(1, 3), F(2, 3)] and abs(0.5 ** 12 - 0.0002) < 0.00005, 'l8 s0')
T(f, 's3', *absorb(walk_chain(3, up=F(2, 3)))[3][3])
LN = Fm([[0.3, 0.1, 0.5, 0.1], [0.2, 0.4, 0.2, 0.2], [0, 0, 1, 0], [0, 0, 0, 1]])
mov, ends, tl, Hl = absorb(LN)
T(f, 's4', Hl[2][0], Hl[3][0], Hl[2][1], Hl[3][1])
N = item(f, 's4')['canvas']['right']['params']['matrices'][0]['rows']
ok(N == [[1.5, 0.25], [0.5, 1.75]] and solve([[F('0.7'), F('-0.1')], [F('-0.2'), F('0.6')]], [1, 0]) == [F(3, 2), F(1, 2)], 'l8 s4 (I-Q)^-1')
ok(close(0.7 * 0.6 - 0.1 * 0.2, 0.4), 'l8 s4 det')
ok(correct(f, 's6') == ['right'] and absorb(walk_chain(4))[3][4] == [F(1, 4), F(1, 2), F(3, 4)], 'l8 s6')
ok(correct(f, 's7') == ['right'], 'l8 s7')
T(f, 's8', Hq[2][1], Hq[2][0])
K(f, 'q0', 0.75, low=0.25, half=0.5)
K(f, 'q1', 0.6, one_minute=0.3, stay=0.5, plus1=2.6)
K(f, 'q3', 0.2, raw=0.1, row1=0.6, colB=0.8)

f = 'review-2'
K(f, 'i0', 0.25, swap=0.75, diag=0.7, half=0.5)
SP = Fm([[0.7, 0.3, 0], [0.3, 0.5, 0.2], [0, 0.4, 0.6]])
ps = stationary(SP)
K(f, 'i1', ps[0] + 2 * ps[1] + 3 * ps[2], simple=2, col=0.3 + 1.0 + 0.6)
ok(sorted(correct(f, 'i2')) == ['half', 'loop', 'reg'] and stationary(Fm([[0, 1], [0.5, 0.5]])) == [F(1, 3), F(2, 3)], 'review-2 i2')
K(f, 'i3', 0.4, step=0.2, unique=0.5, other=0.6)
K(f, 'i4', absorb(walk_chain(5))[2][1], dist=2, four=4, nine=9)
K(f, 'i5', tl[1], geo=1 / 0.6, a=tl[0], drop=0)
K(f, 'i6', 0.8, year=0.2, carry=0.75)
hd = absorb(walk_chain(3, up=F(1, 3)))[3][3]
K(f, 'i7', hd[1], fair=F(2, 3), step=F(1, 3), up=F(6, 7), h1=hd[0])

f = 'homework-2'
TR = Fm([[0.7, 0.2, 0.1], [0.3, 0.6, 0.1], [0.3, 0.1, 0.6]])
T(f, 'i0', *stationary(TR))
K(f, 'i1', 0.002, simple=-0.02 / 3, row=0.01)
PR = Fm([[0, 1, 0, 0], [1, 0, 0, 0], [0.25, 0, 0.5, 0.25], [0, 0, 0, 1]])
ok(sorted(correct(f, 'i3')) == ['half', 'join', 'many'], 'homework-2 i3 key')
ok(abs(float(mpow(PR, 200)[2][0]) - 1 / 6) < 1e-9 and abs(float(mpow(PR, 201)[2][0]) - 1 / 3) < 1e-9, 'homework-2 i3 alternates near 1/6 and 1/3')
T(f, 'i4', *absorb(walk_chain(3, up=F(2, 3)))[2])
LB = Fm([[0.75, 0.10, 0.10, 0.05], [0.25, 0.50, 0.10, 0.15], [0, 0, 1, 0], [0, 0, 0, 1]])
mov, ends, tb, Hb = absorb(LB)
ok(tb == [6, 5] and Hb[2] == [F(3, 5), F(1, 2)] and close(0.4 * (6 * 0.4 + 4 * 0.5), 1.76), 'homework-2 loan book longform')
ok(solve([[F('0.25'), F('-0.10')], [F('-0.25'), F('0.50')]], [1, 0]) == [5, F(5, 2)], 'homework-2 loan book inverse column')
HTH = Fm([[0.5, 0.5, 0, 0], [0, 0.5, 0.5, 0], [0.5, 0, 0, 0.5], [0, 0, 0, 1]])
K(f, 'i7', absorb(HTH)[2][0], eight=8, hh=6)
ok(absorb(HTH)[2] == [10, 8, 6], 'homework-2 HTH t values')
ok(absorb(Fm([[0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0, 1]]))[2][0] == 6, 'homework-2 HH takes 6')
# explain: "With the engine's mulberry32 generator and seed 7, 200,000 simulated runs average 9.995"
def hth_mean(seed, runs, head=lambda u: u < 0.5):
    rng, tot = mulberry32(seed), 0
    for _ in range(runs):
        s, n = 0, 0
        while s < 3:
            n += 1
            hh = head(rng())
            s = (1 if hh else 0) if s == 0 else ((1 if hh else 2) if s == 1 else (3 if hh else 0))
        tot += n
    return tot / runs
m1, m2 = hth_mean(7, 200000), hth_mean(7, 200000, lambda u: u >= 0.5)
ok(abs(m1 - 10) < 0.06 and abs(m2 - 10) < 0.06, 'homework-2 HTH Monte Carlo agrees with 10')
ok(round(m1, 3) == 9.995, f'homework-2 HTH seeded mean (mulberry32, seed 7, H if u < 0.5): {m1:.3f}')
HTH_SEED_NOTE = f'mulberry32 seed 7, 200,000 runs: H if u < 0.5 gives {m1:.3f}; H if u >= 0.5 gives {m2:.3f}; content says 9.995'

f = 'problems-2'
BD = Fm([[0.5, 0.5, 0], [0.1, 0.8, 0.1], [0, 0.4, 0.6]])
pb = stationary(BD)
K(f, 'i0.p0', mpow(BD, 2)[1][2], squared=0.01, one_path=0.08, one_step=0.1)
K(f, 'i0.p1', pb[0] / pb[1], inverted=5, no_move=0.1, row=1)
K(f, 'i0.p2', pb[1], equal=F(1, 3), stay=0.8, no_move_carry=1 / 1.35, no_self=1 / 0.45)
ok(pb == [F(4, 29), F(20, 29), F(5, 29)] and correct(f, 'i0.p3') == ['yes'], 'problems-2 band pi')
ok(all(abs(float(mpow(BD, 60)[i][j]) - float(pb[j])) < 1e-4 for i in range(3) for j in range(3)), 'problems-2 band P^60 near pi')
K(f, 'i0.p4', F(7, 29), equal=F(5, 3), sign=F(47, 29), stay=-0.2, outside_only=F(27, 29))
ST = Fm([[0.5, 0.3, 0, 0.2], [0, 0.9, 0.1, 0], [0, 0.4, 0.6, 0], [0, 0, 0, 1]])
K(f, 'i1.p0', mpow(ST, 2)[0][1], test_test=0.15, on_on=0.27, squared=0.09)
K(f, 'i1.p1', 0.8, stay=0.9, swapped=0.2, equal=0.5, stay_ratio=0.9 / 1.3)
K(f, 'i1.p2', 0.6, one_week=0.3, two_weeks=0.45, carry=0.42, total=0.8)
K(f, 'i1.p3', 0.48, ignores_shut=0.8, live_only=0.6, two_step=0.42, whole_chain=0)
ok(abs(float(mpow(ST, 300)[0][1]) - 0.48) < 1e-9, 'problems-2 trial limit 0.48')
RF = Fm([[0, 0.4, 0.4, 0.2], [0.5, 0, 0.2, 0.3], [0, 0, 1, 0], [0, 0, 0, 1]])
mov, ends, tr, Hr = absorb(RF)
ok(item(f, 'i2.p0')['widget']['answer'] == '0.2+0.5q', 'problems-2 rfq h_C')
K(f, 'i2.p1', Hr[2][0], direct=0.4, one_pass=0.48, no_direct=0.5, walk=0.65)
K(f, 'i2.p2', tr[0], one_pass=1.4, no_one=0, geometric=1 / 0.6, counter=tr[1])
RF2 = Fm([[0, 0.3, 0.5, 0.2], [0.5, 0, 0.2, 0.3], [0, 0, 1, 0], [0, 0, 0, 1]])
mov, ends, tr2, Hr2 = absorb(RF2)
K(f, 'i2.p3', Hr2[2][0], one_pass=0.56, old_hc=0.65, direct=0.5, old_q=0.6)
ok(correct(f, 'i2.p4') == ['old'] and abs(float(Hr2[2][0]) * 40 - 26.35) < 0.005 and abs(float(tr2[0]) - 1.53) < 0.005, 'problems-2 rfq p4')
MA = Fm([[0.5, 0.3, 0.1, 0.1], [0, 0.6, 0.25, 0.15], [0, 0, 1, 0], [0, 0, 0, 1]])
mov, ends, tm, Hm = absorb(MA)
K(f, 'i3.p0', Hm[2][1], one_month=0.25, over_stay=0.25 / 0.6, leave=0.4)
K(f, 'i3.p1', Hm[2][0], no_loop=0.2875, direct=0.4, loop_once=0.43125)
K(f, 'i3.p2', tm[0], no_loop=1.75, no_review=2, no_one=1.5, added=4.5)
val = Hm[2][0] * 10 + (1 - Hm[2][0]) * 6
K(f, 'i3.p3', val, review_h=8.5, even=8, no_withdraw=5.75, swapped=7.7)
K(f, 'i3.p4', val - F('0.02') * tm[0], no_cost=8.3, review_time=8.25, one_month=8.28, carry_added=8.21)

# =====================================================================
# Level 3
# =====================================================================
f = 'l9-coin-flip-walk'
w = walk_paths(43, 1, 10)[0]
ok(w[-1] == 2, f'l9 s0 seeded path (seed 43) ends at 2: got {w[-1]}')
K(f, 's0', 6, end=2, downs=4, half=5)
K(f, 's2', 20, ups=60, excess=10, step=0.2)
K(f, 's3', 10, added=100, mean=0, half=50)
K(f, 's4', sqrt(96), fair=10, coin=sqrt(24), var=96)
K(f, 's5', 0, pos=50, four_n=200, fair=12.5)
K(f, 's7', comb(20, 12) / 2 ** 20, k4=comb(20, 4) / 2 ** 20, k14=comb(20, 14) / 2 ** 20)
ok(comb(20, 12) == 125970, 'l9 s7 125970')
w = walk_paths(61, 1, 100)[0]
ok(w[100] == 10 and min(w[1:]) >= 0, f'l9 s8 seeded path (seed 61) sits at 10 and is not below 0 after the start: end {w[100]}, min {min(w[1:])}')
def exp_returns(n):
    return sum(comb(2 * k, k) / 4 ** k for k in range(1, n // 2 + 1))
ok(abs(exp_returns(100) - 7) < 0.5 and abs(exp_returns(10000) - 79) < 0.5, f'l9 expected returns {exp_returns(100):.2f}, {exp_returns(10000):.2f}')
K(f, 's9', sqrt(998.4), var=998.4, coin=sqrt(249.6), mean=40)
exact_down = sum(comb(1000, k) * 0.52 ** k * 0.48 ** (1000 - k) for k in range(0, 500))
ok(abs(exact_down - 0.097) < 0.0006 and abs(Phi(-40 / 31.6) - 0.10) < 0.005, f'l9 P(down) exact {exact_down:.4f}')
ok(correct(f, 'q0') == ['three'], 'l9 q0')
K(f, 'q1', 30, coin=7.5, mean=-20, fair=40)
K(f, 'q2', Phi(-40 / 31.6), never=0, half=0.5, one_sd=Phi(-1))
# Monte Carlo: mean and variance of S_n
rng = random.Random(20261112)
xs = [sum(1 if rng.random() < 0.6 else -1 for _ in range(100)) for _ in range(20000)]
mu = sum(xs) / len(xs); var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
ok(abs(mu - 20) < 0.3 and abs(var - 96) < 4, f'l9 Monte Carlo mean {mu:.2f} var {var:.1f}')

f = 'l10-gamblers-ruin'
ws = walk_paths(11, 30, 150, start=3)
hits = [first_hit(a, 0, 10) for a in ws]
ups = sum(1 for a, h in zip(ws, hits) if h >= 0 and a[h] >= 10)
ok(ups == 9, f'l10 s0 seeded batch (seed 11): {ups} of 30 reach 10; unfinished {hits.count(-1)}')
ok(correct(f, 's0') == ['three-tenths'], 'l10 s0')
def tau_mean(seed, paths, steps, start, lo, hi):
    ws = walk_paths(seed, paths, steps, start=start)
    hs = [first_hit(a, lo, hi) for a in ws]
    return sum(h if h >= 0 else steps for h in hs) / paths, hs.count(-1)
m5, u5 = tau_mean(6, 20, 120, 5, 0, 10); m1, u1 = tau_mean(6, 20, 120, 1, 0, 10)
ok(round(m5) == 25 and round(m1) == 7, f'l10 s1 seeded batch (seed 6): mean {m5:.2f} from 5 ({u5} unfinished), {m1:.2f} from 1')
K(f, 's3', 2500, distance=50, target=100, i_times_n=5000)
m50, u50 = tau_mean(28, 20, 8000, 50, 0, 100)
ok(round(m50) == 2398, f'l10 s3 seeded batch (seed 28): mean {m50:.1f}, unfinished {u50}')
p49 = F(49, 100)
K(f, 's4', ruin(50, 100, p49), fair=0.5, p=0.49, flip=ruin(50, 100, F(51, 100)))
r = 51 / 49
ok(abs(r ** 50 - 7.39) < 0.005 and abs(r ** 100 - 54.6) < 0.05 and abs(r ** 20 - 2.23) < 0.005 and abs(r ** 40 - 4.95) < 0.005, 'l10 powers of r')
ok(abs(float(ruin(5, 10, p49)) - 0.450) < 0.0005 and correct(f, 's5') == ['bold'], 'l10 s5 0.450')
# duration of the unfair game, to judge "thousands of bets"
D49 = (50 - 100 * float(ruin(50, 100, p49))) / (0.51 - 0.49)
mov, ends, t49, H49 = absorb(walk_chain(100, up=p49))
ok(abs(D49 - 1904) < 1 and abs(float(t49[49]) - D49) < 1e-6, f'l10 s4 unfair game lasts {D49:.0f} bets on average (finding 7, imprecise: text says thousands)')
ok(correct(f, 's6') == ['one'], 'l10 s6')
K(f, 's7', ruin(20, 40, p49), fair=0.5, p=0.49, small_bets=ruin(50, 100, p49))
K(f, 's8', 100, ten=10, twenty=20, four_hundred=400)
m0, u0 = tau_mean(8, 20, 400, 0, -10, 10)
ok(round(m0) == 102, f'l10 s8 seeded batch (seed 8): mean {m0:.2f}, unfinished {u0}')
K(f, 'q1', 12, prob=0.25, i_n=16, dist=6)
K(f, 'q2', ruin(2, 4, F(3, 5)), fair=0.5, p=0.6, inverted=ruin(2, 4, F(2, 5)))
# first-step check of D_i = i(N - i) and of the ruin formula against the linear system
for N_, up in ((10, F(1, 2)), (8, F(1, 2)), (10, p49), (5, F(12, 25))):
    mov, ends, tt, HH = absorb(walk_chain(N_, up=up))
    for i in range(1, N_):
        ok(HH[N_][i - 1] == ruin(i, N_, up), f'ruin formula N={N_} i={i}')
        if up == F(1, 2):
            ok(tt[i - 1] == i * (N_ - i), f'duration N={N_} i={i}')

f = 'l11-reflection'
def paths_to(n, k):
    return comb(n, (n + k) // 2) if (n + k) % 2 == 0 and abs(k) <= n else 0
def brute_touch(n, k, m):
    """Count n-step paths ending at k that touch level m (m > 0), by enumeration."""
    c = 0
    for bits in range(2 ** n):
        s, mx = 0, 0
        for j in range(n):
            s += 1 if (bits >> j) & 1 else -1
            mx = max(mx, s)
        if s == k and mx >= m:
            c += 1
    return c
K(f, 's0', 15, all=64, three_ups=20, steps=6)
ok(item(f, 's1')['widget']['answer'] == ['p4'] and correct(f, 's2') == ['right'], 'l11 s1, s2')
K(f, 's3', brute_touch(8, 0, 2), all=70, to_two=56)
ok(item(f, 's3')['widget']['wrong'][1]['value'] == 70 - 28, 'l11 s3 not')
K(f, 's4', brute_touch(8, 2, 2), none=0, mirror4=28, all8=70)
reach = sum(brute_touch(8, k, 2) for k in range(-8, 9, 2))
K(f, 's5', reach, end_only=93, half=128, fell_back=37)
for n_, m_ in ((8, 2), (4, 2), (6, 2), (10, 3), (12, 4), (9, 3)):
    tot = sum(brute_touch(n_, k, m_) for k in range(-n_, n_ + 1)) if n_ <= 12 else None
    rule = sum(paths_to(n_, k) for k in range(m_, n_ + 1)) + sum(paths_to(n_, k) for k in range(m_ + 1, n_ + 1))
    ok(tot == rule and close(touch(n_, m_, 0.5), rule / 2 ** n_), f'reflection rule n={n_} m={m_}')
# finding 5 (imprecise): the count C(n, (n + 2m - k)/2) for k <= m needs a level above the start
ok(paths_to(4, -4) == 1 and comb(4, (4 + 2 * (-2) - (-4)) // 2) == 6, 'l11 s3 formula miscounts for a level below the start')
K(f, 's7', F(6, 16), end_only=F(5, 16), over=F(1, 16), half=0.5)
# ballot count: 6 wins and 4 losses, P&L above 0 after every day
from itertools import combinations
cnt_ballot = 0
for downs in combinations(range(10), 4):
    s, good = 0, True
    for j in range(10):
        s += -1 if j in downs else 1
        if s <= 0:
            good = False; break
    cnt_ballot += good
K(f, 's8', cnt_ballot, start_up=126, touch=84, all=210)
ok(comb(9, 5) == 126 and comb(9, 6) == 84 and F(cnt_ballot, 210) == F(6 - 4, 6 + 4), 'l11 s8 ballot')
le4, le6 = 1 - binom_ge(20, 9), 1 - binom_ge(20, 8)
ok(abs(le4 - 0.2517) < 5e-5 and abs(le6 - 0.1316) < 5e-5, 'l11 s9 given tail values')
K(f, 's9', touch(20, -4, 0.5), end_only=le4, beyond=le6, double=2 * le4)
K(f, 'q0', brute_touch(10, 0, 3), all=252, mirror3=210)
ok(correct(f, 'q1') == ['all'] and brute_touch(6, 4, 2) == 6, 'l11 q1')
first4 = touch(4, 2, 0.5) - touch(3, 2, 0.5)
K(f, 'q2', first4, end=0.25, max=0.375, one=0.0625)
ok(close(first4, 2 / 4 * comb(4, 3) / 16), 'l11 q2 hitting time theorem')
K(f, 'q3', touch(6, 2, 0.5), end_only=F(22, 64), exact2=F(15, 64))

f = 'l12-price-paths'
A = item(f, 's0')['canvas']['left']['params']['series'][0]['values']
Bv = item(f, 's0')['canvas']['right']['params']['series'][0]['values']
ok(all(abs(abs(b - a) - 1) < 1e-9 for a, b in zip(Bv, Bv[1:])) and len(Bv) == 121, 'l12 s0 chart B moves 1 a day for 120 days')
ra = item(f, 's8')['canvas']['left']['params']['series'][0]['values']
ok(all(abs(math.log(b / a) * 100 - r_) < 0.02 for a, b, r_ in zip(A, A[1:], ra)), 'l12 s8 panel is the log returns of chart A, in %')
big = [d + 1 for d, (a, b) in enumerate(zip(A, A[1:])) if b / a - 1 < -0.06]
ok(big == [71, 106], f'l12 s0 falls of over 6% (simple returns) on days {big}')
ok(any(abs(r_ + 6.5) < 0.005 for r_ in ra), 'l12 s8 hint: a fall of 6.5% is in the panel')
K(f, 's2', 0.01 * sqrt(250), linear=2.5, mean=0.125, daily=0.01)
K(f, 's3', Phi(-12.5 / 15.81), half=0.5, daily=Phi(-0.05), never=0)
K(f, 's4', 125, added=130, three_ups=100 * 1.25 ** 3, back=100)
ok(abs(math.log(1.25) - 0.2231) < 5e-5 and close(1.25 * 0.8, 1), 'l12 s4 logs')
ws = walk_paths(32, 40, 10)
h32 = [first_hit(a, None, 3) for a in ws]
ok(sum(1 for h in h32 if h >= 0) == 13, f'l12 s5 seeded batch (seed 32): {sum(1 for h in h32 if h >= 0)} of 40 touch +3')
ok(h32[0] == 7 and ws[0][10] == 0, f'l12 s5 bold path touches 3 on day {h32[0]} and ends at {ws[0][10]}')
K(f, 's5', touch(10, 3, 0.5), end_only=176 / 1024, sim=13 / 40, half=0.5)
ok(comb(10, 7) + comb(10, 8) + comb(10, 9) + 1 == 176 and close(touch(20, 5, 0.5), 0.26317596435546875), 'l12 s5, s6 exact values')
ok(abs(sqrt(0.34375 * 0.65625 / 20000) - 0.003) < 0.0005, 'l12 s6 standard error')
w = walk_paths(781, 1, 200, start=100)[0]
ok(w[200] == 140, f'l12 s7 seeded path (seed 781) ends at {w[200]}')
dd = max(max(w[:i + 1]) - w[i] for i in range(201))
ok(dd <= 8, f'l12 s7 "hardly a dip": largest fall from a peak is {dd}')
ok(sorted(correct(f, 's8')) == ['cluster', 'tails'], 'l12 s8')
ws = walk_paths(10, 40, 20)
t10 = sum(1 for a in ws if first_hit(a, None, 5) >= 0)
ok(t10 == 10, f'l12 s9 seeded batch (seed 10): {t10} of 40 touch +5')
ge6 = binom_ge(20, 13)
K(f, 's9', 100 * 2 * ge6, end_only=100 * ge6, half=50, prob=2 * ge6)
ok(abs(ge6 - 0.1316) < 5e-5, 'l12 s9 given value')
K(f, 'q0', 0.1, none=0, daily=0.0004)
K(f, 'q1', 0.1, linear=0.5, daily=0.02, var=0.01)
K(f, 'q2', 6, paths=32, days=5, pairs=10)
# "fair price": expected pay-out equals the no-arbitrage price only when the modelled walk is itself a fair bet.
# s9 uses an additive fair walk with no interest (a martingale), so 100 x P(touch) is the replication price there.
# A walk with p = 0.55 (s6 explain, "the same code prices a walk with drift") is not: its price still uses 0.5.
price_fair = 100 * touch(20, 5, 0.5); payout_drift = 100 * touch(20, 5, 0.55)
ok(abs(price_fair - 26.32) < 0.005 and payout_drift > price_fair + 10, 'l12 pricing note numbers')
PRICE_NOTE = f'l12 (finding, imprecise): expected pay-out of the one-touch at p = 0.55 is {payout_drift:.2f}; its replication price stays {price_fair:.2f}'

f = 'review-3'
K(f, 'i0', sqrt(396), fair=20, coin=sqrt(99), var=396)
K(f, 'i1', 0.25, ratio=F(1, 3), half=0.5, flip=0.75)
K(f, 'i2', brute_touch(12, 2, 4), all=792, diff=572, to_four=495)
K(f, 'i3', 0.06, linear=0.24, daily=0.015)
K(f, 'i4', (49 / 51) ** 20, certain=1, one_bet=0.49, inverse=(51 / 49) ** 20)
K(f, 'i5', 252 / 1024, half=0.5, one_path=1 / 1024, eleven=1 / 11)
K(f, 'i6', touch(12, 4, 0.5), end_only=binom_ge(12, 8), double=2 * binom_ge(12, 8), beyond=binom_ge(12, 9))
ok(F(794 + 299, 4096) == F(1093, 4096), 'review-3 i6 1093/4096')
K(f, 'i7', ruin(5, 10, F(11, 20)), bold=0.55, fair=0.5, inverted=1 - ruin(5, 10, F(11, 20)))
K(f, 'i8', 144, added=140, cube=172.8, ups_only=120)

f = 'homework-3'
ok(item(f, 'i0')['widget']['answer'] == 'i(20-i)' and item(f, 'i1')['widget']['answer'] == '0.84n', 'homework-3 expressions')
ok(all(absorb(walk_chain(20))[2][i - 1] == i * (20 - i) for i in range(1, 20)), 'homework-3 i0 D_i')
K(f, 'i3', paths_to(10, 2) - brute_touch(10, 2, 4), touch=45, all=210, wrong_mirror=90)
T9 = touch(9, 3, 0.5) - touch(8, 3, 0.5)
K(f, 'i4', T9, end_at_3=84 / 512, no_avoid=56 / 512, by_8=56 / 256)
ok(close(T9, 28 / 512) and close(T9, 3 / 9 * comb(9, 6) / 512), 'homework-3 i4 28/512')
pr = F(18, 37)
K(f, 'i5', ruin(10, 20, pr), fair=0.5, single=18 / 37, flip=1 - ruin(10, 20, pr))
ok(abs((19 / 18) ** 10 - 1.717) < 0.0005 and abs(1 / 37 - 0.027) < 0.0005, 'homework-3 i5 r^10 and edge')
ok(abs(touch(10, 3, 0.55) - 0.4523) < 5e-5 and abs(2 * binom_ge(10, 7, 0.55) - 0.5321) < 5e-5, 'homework-3 i6 explain numbers')
naive = 2 * binom_ge(20, 13, 0.55); exact55 = touch(20, 5, 0.55)
ok(abs(naive - 0.504) < 0.0006 and abs(exact55 - 0.410) < 0.0006, f'homework-3 longform part 3: {naive:.4f}, {exact55:.4f}')
tilt = binom_ge(20, 13, 0.55) + sum(comb(20, k) * 0.55 ** k * 0.45 ** (20 - k) * (0.45 / 0.55) ** (2 * k - 20 - 5) for k in range(13, 21))
ok(close(tilt, exact55, 1e-12), 'homework-3 longform tilted reflection formula')
K(f, 'i8', 4 * 0.9984 / 0.0016, linear=50, one_sd=624, thousand=1000)

f = 'problems-3'
K(f, 'i0.p0', 3.96, no_mean=4, unit_steps=0.99, mean=0.2)
K(f, 'i0.p1', sqrt(1584), no_mean=40, variance=1584, unit_steps=sqrt(396), no_n=sqrt(3.96))
K(f, 'i0.p2', Phi(-2.01), variance=Phi(-80 / 1584), complement=0.9778, one_trade=Phi(-80 / 1.99))
ex = sum(comb(400, k) * 0.55 ** k * 0.45 ** (400 - k) for k in range(0, 200))
ok(abs(ex - 0.020) < 0.001, f'problems-3 exact binomial P(down) {ex:.4f}')
nmin = (2.33 * sqrt(3.96) / 0.2) ** 2
K(f, 'i0.p3', math.ceil(nmin), no_mean=math.ceil((2.33 * 2 / 0.2) ** 2), five_percent=math.ceil((1.645 * sqrt(3.96) / 0.2) ** 2), root=24, two_sd=math.ceil((2 * sqrt(3.96) / 0.2) ** 2))
K(f, 'i1.p0', paths_to(12, -4), end_minus_two=792, mirror=220, end_zero=924)
K(f, 'i1.p1', brute_touch(12, 2, 3), all_paths=792, wrong_mirror=220, none=0)  # mirror image of ending -2 touching -3
ok(sum(paths_to(12, k) for k in range(-12, -3, 2)) == 794, 'problems-3 794')
K(f, 'i1.p2', touch(12, -3, 0.5), end_only=794 / 4096, level_two=2 * 1586 / 4096, plus_two=(794 + 495) / 4096)
K(f, 'i1.p3', 100 * (1 - touch(12, -3, 0.5)), pays_on_touch=38.77, end_only=100 * (1 - 794 / 4096), face=100)
q = (1 - 1 / 1.1) / (1.1 - 1 / 1.1)
ok(abs(q - 0.476) < 0.0005 and abs(100 * (1 - touch(12, -3, q)) - 55.57) < 0.02, f'problems-3 risk-neutral price {100 * (1 - touch(12, -3, q)):.2f} at q = {q:.4f}')
ok(correct(f, 'i1.p4') == ['simulate'], 'problems-3 i1 p4')
p48 = F(12, 25)
K(f, 'i2.p0', -4, half=-2, win_only=48, loss_only=-52)
K(f, 'i2.p1', ruin(6, 10, p48), fair=0.6, r_inverted=ruin(6, 10, 1 - p48))
K(f, 'i2.p2', ruin(3, 5, p48), fair=0.6, r_inverted=ruin(3, 5, 1 - p48), same=ruin(6, 10, p48))
K(f, 'i2.p3', 1000 * ruin(3, 5, p48) - 600, hundreds=1000 * ruin(6, 10, p48) - 600, wealth=1000 * ruin(3, 5, p48), fair=0, target_only=400)
K(f, 'i3.p0', F(5, 8), swapped=F(3, 8), equal=0.5, ratio=0.6)
K(f, 'i3.p1', 15, width=8, product=40, square=25, target_sq=9)
K(f, 'i3.p2', 0, target_only=1.875, stop_only=-1.875, target=3)
K(f, 'i3.p3', -600, no_cost=0, one_day=-40, product_days=-1600, ticks=187.5)
ok(correct(f, 'i3.p4') == ['two-six'] and (2 * 6, 4 * 4, 3 * 5) == (12, 16, 15), 'problems-3 exits')

# =====================================================================
# Code widgets: the solution passes every hidden test, the starter fails
# =====================================================================
def run_code(w, src):
    env = {}
    exec(w.get('prelude', '') + '\n' + src, env)
    res = []
    for t in w['tests']:
        try:
            got = eval(t['call'], env)
            exp = eval(t['expect'], env) if isinstance(t['expect'], str) else t['expect']
            if t.get('compare') == 'isclose':
                tol = t.get('tol', {}).get('abs')
                def cmp(a, b):
                    if isinstance(a, (list, tuple)):
                        return len(a) == len(b) and all(cmp(x, y) for x, y in zip(a, b))
                    return abs(a - b) <= tol if tol else math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
                res.append(cmp(got, exp))
            else:
                res.append(got == exp)
        except Exception:
            res.append(False)
    return res
import io, contextlib
for f, loc in (('l2-transition-matrix', 's9'), ('l5-where-it-settles', 's7'), ('l12-price-paths', 's6'), ('homework-1', 'i8'), ('homework-2', 'i8'), ('homework-3', 'i6')):
    w = item(f, loc)['widget']
    with contextlib.redirect_stdout(io.StringIO()):
        good = run_code(w, w['solution'])
        try:
            bad = run_code(w, w['starter'])
        except Exception:
            bad = [False]
    ok(all(good), f'{f} {loc} solution passes its tests: {good}')
    ok(not all(bad), f'{f} {loc} starter fails')
env = {}
exec(item('l5-where-it-settles', 's7')['widget']['solution'], env)
got = [env['share_in_bull'](200000, s) for s in (1, 2, 7)]
ok(got == [0.666255, 0.668935, 0.66784], f'l5 s7 seeded shares {got}')
env = {}
exec(item('l12-price-paths', 's6')['widget']['solution'], env)
ok(round(env['hit_prob'](10, 3, 20000, 1), 2) == 0.34, 'l12 s6 example')
env = {}
with contextlib.redirect_stdout(io.StringIO()) as buf:
    exec(item('l2-transition-matrix', 's9')['widget']['solution'], env)
five = env['after']([0, 1, 0], env['R3'], 5)
ok([round(x, 4) for x in five] == [0.4288, 0.4123, 0.1589], f'l2 s9 five days from Normal {five}')

print(HTH_SEED_NOTE)
print(PRICE_NOTE)
print(f'{n_checks} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
