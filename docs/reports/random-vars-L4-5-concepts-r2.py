#!/usr/bin/env python3
"""Round 2 concept audit, random-vars levels 4 and 5 (l13 to l20, review-4/5,
homework-4/5, problems-4/5). Independent recomputation of every graded key,
wrong option and slip value, plus exact enumerations and Monte Carlo checks of
the empirical and structural claims. Written blind, before reading any earlier
review or script for these files.

Exit 0 on correct content. A check that fails because the content is wrong
stays failing: see docs/reviews/audit-random-vars-4-5-r2.md for the list of
checks that fail on purpose.

Run from the repo root: python3 docs/reports/random-vars-L4-5-concepts-r2.py
"""
import json, math, os, random, sys, itertools
from fractions import Fraction as F
from math import comb, factorial, log, sqrt, exp

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                    'app', 'content', 'courses', 'random-vars')
FAILS = []
N = 0


def load(name):
    with open(os.path.join(ROOT, name + '.json')) as fh:
        return json.load(fh)


def chk(label, got, want, tol=1e-9):
    global N
    N += 1
    ok = (got == want) if isinstance(want, (bool, str, list, tuple)) else abs(float(got) - float(want)) <= tol
    if not ok:
        FAILS.append(f'{label}: got {got!r}, want {want!r}')
        print('FAIL', label, got, want)


def key(w):
    return w['answer']


def slip(w, sid):
    for s in w.get('wrong', []):
        if s['id'] == sid:
            return s['value']
    raise KeyError(sid)


def opt(w, oid):
    for o in w['options']:
        if o['id'] == oid:
            return o
    raise KeyError(oid)


def correct_ids(w):
    return [o['id'] for o in w['options'] if o.get('correct')]


def cells(canvas):
    return [[float(F(c)) if c not in ('?',) else None for c in row] for row in canvas['params']['cells']]


def run_code(widget, label):
    """Solution passes every example and hidden test; the starter fails."""
    def run(src):
        env = {}
        exec(src, env)
        res = []
        for t in widget.get('examples', []) + widget['tests']:
            got = eval(t['call'], env)
            want = t['expect']
            if isinstance(want, str):          # content stores expected values as Python literals
                want = eval(want, {})
            if t['compare'] == 'isclose':
                res.append(math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12))
            else:
                res.append(got == want)
        return res
    chk(label + ' solution passes', all(run(widget['solution'])), True)
    try:
        starter_ok = all(run(widget['starter']))
    except Exception:
        starter_ok = False
    chk(label + ' starter fails', starter_ok, False)
    env = {}
    exec(widget['solution'], env)
    return env


rng = random.Random(20261112)

# --------------------------------------------------------------- l13
L = load('l13-joint-tables')
S = L['screens']
T = [[0.12, 0.06, 0.02], [0.10, 0.30, 0.10], [0.03, 0.09, 0.18]]
row = [sum(r) for r in T]
col = [sum(T[i][j] for i in range(3)) for j in range(3)]
chk('l13 cells sum', sum(row), 1)
c4 = cells(S[4]['canvas'])
for i in range(3):
    for j in range(3):
        chk(f'l13 canvas cell {i}{j}', c4[i][j], T[i][j])
    chk(f'l13 row total {i}', c4[i][3], row[i])
    chk(f'l13 col total {i}', c4[3][i], col[i])
chk('l13 s1 answer row', S[1]['widget']['answer'], ['r1c1', 'r1c2', 'r1c3'])
chk('l13 s2 answer col', S[2]['widget']['answer'], ['r1c3', 'r2c3', 'r3c3'])
chk('l13 s3 P(Y=-2)', S[3]['widget']['rows'][0][1]['answer'], col[0])
chk('l13 s3 P(Y=0)', S[3]['widget']['rows'][1][1]['answer'], col[1])
chk('l13 s4 key 0.60', float(opt(S[4]['widget'], 'right')['text'].strip('$')), T[0][0] / row[0])
chk('l13 s4 col slip 0.48', float(opt(S[4]['widget'], 'col')['text'].strip('$')), T[0][0] / col[0])
chk('l13 s4 marg slip', float(opt(S[4]['widget'], 'marg')['text'].strip('$')), col[0])
chk('l13 s5 0.30', S[5]['widget']['rows'][1][2]['answer'], T[0][1] / row[0])
chk('l13 s5 0.10', S[5]['widget']['rows'][2][2]['answer'], T[0][2] / row[0])
chk('l13 s5 six times', (T[0][0] / row[0]) / (T[0][2] / row[0]), 6)
chk('l13 s6 right', [round(x / row[2], 2) for x in T[2]], [0.10, 0.30, 0.60])
colsopt = [round(T[2][j] / col[j], 2) for j in range(3)]
chk('l13 s6 cols option', colsopt, [0.12, 0.20, 0.60])
chk('l13 s6 cols add to 0.92', sum(colsopt), 0.92)
chk('l13 s8 keys', [r[1]['answer'] for r in S[8]['widget']['rows']], [0.6, 0.5, 0.2308])
chk('l13 s8 0.12/0.52', 0.12 / 0.52, 0.2308, 5e-5)
chk('l13 s9 key', key(S[9]['widget']), 0.30 / 0.40)
chk('l13 s9 marg slip is P(B=2)', slip(S[9]['widget'], 'marg'), 0.05 + 0.05 + 0.30)
Q = L['quiz']
chk('l13 q0', key(Q[0]['widget']), 0.10 + 0.30)
chk('l13 q1', key(Q[1]['widget']), 0.30 / 0.40)
chk('l13 q1 reversed', slip(Q[1]['widget'], 'reversed'), 0.30 / 0.50)
chk('l13 q2 adds to 0.9', 0.5 + 0.3 + 0.1, 0.9)
# q3: two joint tables with the same margins and different cells exist
A = [[0.25, 0.25], [0.25, 0.25]]
B = [[0.4, 0.1], [0.1, 0.4]]
chk('l13 q3 same margins differ inside', [sum(r) for r in A] == [sum(r) for r in B] and A != B, True)

# --------------------------------------------------------------- l14
L = load('l14-independent-rvs')
S = L['screens']
AB = [[0.06, 0.08, 0.06], [0.15, 0.20, 0.15], [0.09, 0.12, 0.09]]
CD = [[0.08, 0.06, 0.06], [0.13, 0.22, 0.15], [0.09, 0.12, 0.09]]
rA = [sum(r) for r in AB]
cA = [sum(AB[i][j] for i in range(3)) for j in range(3)]
chk('l14 AB independent', all(abs(AB[i][j] - rA[i] * cA[j]) < 1e-12 for i in range(3) for j in range(3)), True)
chk('l14 CD same margins', [round(sum(r), 10) for r in CD] == [round(x, 10) for x in rA]
    and [round(sum(CD[i][j] for i in range(3)), 10) for j in range(3)] == [round(x, 10) for x in cA], True)
diff = [f'r{i+1}c{j+1}' for i in range(3) for j in range(3) if abs(CD[i][j] - rA[i] * cA[j]) > 1e-9]
chk('l14 s3 failing cells', sorted(diff), sorted(S[3]['widget']['answer']))
chk('l14 s0 key', float(opt(S[0]['widget'], 'right')['text'].strip('$')), 0.12 / 0.30)
chk('l14 s0 col slip', float(opt(S[0]['widget'], 'col')['text'].strip('$')), 0.12 / 0.40)
prod_rows = S[2]['widget']['rows']
for i in (1, 2):
    for j in (1, 2, 3):
        chk(f'l14 s2 product {i}{j}', prod_rows[i][j]['answer'], rA[i] * cA[j - 1])
EX = sum(i * rA[i] for i in range(3)); EY = sum(j * cA[j] for j in range(3))
EXY = sum(i * j * AB[i][j] for i in range(3) for j in range(3))
chk('l14 s4 E[X]', EX, 1.1); chk('l14 s4 E[Y]', EY, 1.0)
chk('l14 s4 key', key(S[4]['widget']), EXY)
chk('l14 s4 slip sum', slip(S[4]['widget'], 'sum'), EX + EY)
chk('l14 s4 slip unweighted', slip(S[4]['widget'], 'unweighted'), 0.20 + 0.15 + 0.12 + 0.09)
LP = [[0.30, 0.15, 0.05], [0.18, 0.11, 0.01], [0.12, 0.04, 0.04]]
rL = [sum(r) for r in LP]; cL = [sum(LP[i][j] for i in range(3)) for j in range(3)]
failing = [(i, j) for i in range(3) for j in range(3) if abs(LP[i][j] - rL[i] * cL[j]) > 1e-9]
chk('l14 s5 four fail', failing, [(1, 1), (1, 2), (2, 1), (2, 2)])
chk('l14 s5 P(Y=2|X=2)', LP[2][2] / rL[2], 0.20)
# Y = X^2
xs = [-1, 0, 1]
exy = sum(F(1, 3) * x ** 3 for x in xs); ex = sum(F(1, 3) * x for x in xs); ey = sum(F(1, 3) * x * x for x in xs)
chk('l14 s6 cov 0', exy - ex * ey, 0)
chk('l14 s6 slip ey', slip(S[6]['widget'], 'ey'), float(ey), 1e-4)
chk('l14 s6 slip var(Y)', slip(S[6]['widget'], 'var'), float(ey - ey ** 2), 1e-4)
chk('l14 s7 dependent', F(1, 3) != F(1, 3) * F(1, 3), True)
# shared volatility regime
vals = [-3, -1, 1, 3]
J = {(a, b): 0.0 for a in vals for b in vals}
for a in (-3, 3):
    for b in (-3, 3):
        J[(a, b)] = 0.125
for a in (-1, 1):
    for b in (-1, 1):
        J[(a, b)] = 0.125
cj = cells(S[9]['canvas'])
chk('l14 s9 canvas', [[J[(a, b)] for b in vals] for a in vals], cj)
chk('l14 s9 corr 0', sum(a * b * p for (a, b), p in J.items()), 0)
chk('l14 s9 key', key(S[9]['widget']), J[(3, 3)] / sum(J[(3, b)] for b in vals))
chk('l14 s9 prod slip', slip(S[9]['widget'], 'prod'), 0.25 * 0.25)
chk('l14 s10 key', key(S[10]['widget']), 0.6 * 0.5 + 0.4 * 0.5)
chk('l14 s10 one-cell slip is A misses B fills', slip(S[10]['widget'], 'one-cell'), 0.4 * 0.5)
chk('l14 s10 both slip', slip(S[10]['widget'], 'both'), 0.6 * 0.5)
Q = L['quiz']
q0 = [[0.28, 0.42], [0.12, 0.18]]
chk('l14 q0 independent', all(abs(q0[i][j] - sum(q0[i]) * (q0[0][j] + q0[1][j])) < 1e-12 for i in range(2) for j in range(2)), True)
chk('l14 q0 key', correct_ids(Q[0]['widget']), ['right'])
chk('l14 q1', key(Q[1]['widget']), 2 * -3)
chk('l14 q3', key(Q[3]['widget']), 0.3 * 0.6)
chk('l14 q3 both', slip(Q[3]['widget'], 'both'), 0.7 * 0.4)
# summary note: in a 2 by 2 table one matching cell forces all four
a_, b_ = 0.37, 0.61
c11 = a_ * b_
chk('l14 2x2 one cell is enough', abs((a_ - c11) - a_ * (1 - b_)) < 1e-12 and abs((1 - a_ - b_ + c11) - (1 - a_) * (1 - b_)) < 1e-12, True)

# --------------------------------------------------------------- l15
L = load('l15-given-information')
S = L['screens']
T = [[0.10, 0.08, 0.02], [0.10, 0.25, 0.15], [0.03, 0.09, 0.18]]
ys = [-2, 0, 2]
row = [sum(r) for r in T]; col = [sum(T[i][j] for i in range(3)) for j in range(3)]
cm = [sum(y * p for y, p in zip(ys, r)) / s for r, s in zip(T, row)]
EYall = sum(y * c for y, c in zip(ys, col))
chk('l15 cond means', [round(x, 10) for x in cm], [-0.8, 0.2, 1.0])
chk('l15 E[Y]', EYall, 0.24)
chk('l15 s0 joint slip', float(opt(S[0]['widget'], 'joint')['text'].strip('$')), sum(y * p for y, p in zip(ys, T[0])))
chk('l15 s2 keys', [S[2]['widget']['rows'][1][2]['answer'], S[2]['widget']['rows'][2][2]['answer']], [0.2, 1.0])
chk('l15 s3 key', key(S[3]['widget']), row[2])
chk('l15 s3 cell slip', slip(S[3]['widget'], 'cell'), T[2][2])
chk('l15 s3 py slip', slip(S[3]['widget'], 'py'), col[2])
p0 = [x / row[1] for x in T[1]]
mse = lambda g: sum(p * (y - g) ** 2 for y, p in zip(ys, p0))
chk('l15 s4 mse 0.2', mse(0.2), 1.96); chk('l15 s4 mse 0.24', mse(0.24), 1.9616); chk('l15 s4 mse 0', mse(0), 2.0)
chk('l15 s4 mean minimises', min((mse(g / 1000), g / 1000) for g in range(-2000, 2001))[1], 0.2)
chk('l15 s5 joint slip 0.30', sum(y * p for y, p in zip(ys, T[2])), 0.30)
chk('l15 s5 cols slip 0.77', round(sum(y * T[2][j] / col[j] for j, y in enumerate(ys)), 2), 0.77)
chk('l15 s6 key', key(S[6]['widget']), (1 * 0.12 + 2 * 0.09) / 0.30)
chk('l15 s6 ex slip', slip(S[6]['widget'], 'ex'), 1.1)
dn = [0.3, 0.4, 0.2, 0.1, 0]; up = [0, 0.1, 0.3, 0.4, 0.2]; yy = [-2, -1, 0, 1, 2]
chk('l15 s8 down', S[8]['widget']['rows'][0][1]['answer'], sum(a * b for a, b in zip(yy, dn)))
chk('l15 s8 up', S[8]['widget']['rows'][1][1]['answer'], sum(a * b for a, b in zip(yy, up)))
chk('l15 s8 slope through the two points is 0.8', (0.7 - (-0.9)) / 2, 0.8)
chk('l15 s9 key', key(S[9]['widget']), 100 * 0.3 + 300 * 0.3 + 500 * 0.2)
chk('l15 s9 flat', slip(S[9]['widget'], 'flat'), (0 + 100 + 300 + 500) / 4)
chk('l15 s9 small', slip(S[9]['widget'], 'small'), 70)
chk('l15 s9 about three times', round(220 / 70), 3)
Q = L['quiz']
chk('l15 q0', key(Q[0]['widget']), 10 * 0.40 / 0.50)
chk('l15 q0 all', slip(Q[0]['widget'], 'all'), 10 * 0.60)
chk('l15 q3', key(Q[3]['widget']), 0.25 + 1 + 1)
chk('l15 q3 plain', slip(Q[3]['widget'], 'plain'), 7 / 3, 1e-4)

# --------------------------------------------------------------- l16
L = load('l16-averaging-averages')
S = L['screens']
chk('l16 s0 key', float(opt(S[0]['widget'], 'right')['text'].strip('$')), 0.2 * -0.8 + 0.5 * 0.2 + 0.3 * 1.0)
chk('l16 s0 plain', float(opt(S[0]['widget'], 'plain')['text'].strip('$')), round((-0.8 + 0.2 + 1.0) / 3, 2))
chk('l16 s0 mult', float(opt(S[0]['widget'], 'mult')['text'].strip('$')), -0.8 * 0.2 * 1.0)
chk('l16 s1 key', key(S[1]['widget']), 120 / 300)
chk('l16 s1 half -30', 120 * 0.5 - 180 * 0.5, -30)
chk('l16 s1 flip', slip(S[1]['widget'], 'flip'), 180 / 300)
chk('l16 s4 key', key(S[4]['widget']), 1 / 0.25)
chk('l16 s4 third slip: E = 1/4 + 3/4 E', slip(S[4]['widget'], 'third'), 0.25 / 0.25)
# two heads in a row: E = 1/2(1+E) + 1/4*2 + 1/4(2+E)
E = F(3, 2) / (1 - F(3, 4))
chk('l16 s5 key', key(S[5]['widget']), E)
chk('l16 s5 slip three is wait for one head plus one toss', slip(S[5]['widget'], 'three'), 2 + 1)


def wait_pattern(pat, r):
    s = ''
    while not s.endswith(pat):
        s += 'H' if r.random() < 0.5 else 'T'
    return len(s)


m = sum(wait_pattern('HH', rng) for _ in range(200000)) / 200000
chk('l16 s5 MC HH wait 6', m, 6, 0.06)
chk('l16 s6 key', float(opt(S[6]['widget'], 'right')['text'].strip('$')), 6)
chk('l16 s7 1/p values', [1 / 0.5, 1 / 0.25, round(1 / (1 / 6), 9), 1 / 1], [2, 4, 6, 1])
env = run_code(S[8]['widget'], 'l16 s8 code')
got = [env['average_wait'](0.5, 50000, 1), env['average_wait'](1 / 6, 50000, 2), env['average_wait'](0.2, 50000, 3)]
txt = S[8]['explain']['text']
for g in got:
    chk(f'l16 s8 stated average {g:.5f} in explain', f'{g:.5f}' in txt, True)
# "about six standard errors": tolerance over sd/sqrt(n)
for p_, tol_ in ((0.5, 0.05), (1 / 6, 0.15), (0.2, 0.12)):
    se = sqrt(1 - p_) / p_ / sqrt(50000)
    chk(f'l16 s8 tolerance in SEs p={p_:.3f}', 5.5 < tol_ / se < 8.5, True)
chk('l16 s9 key', key(S[9]['widget']), 1 / 0.2)
chk('l16 s10 key', key(S[10]['widget']), 0.7 * 400 + 0.3 * -500)
chk('l16 s10 plain', slip(S[10]['widget'], 'plain'), (400 - 500) / 2)
chk('l16 s10 more than half taken back', 150 / 280 > 0.5, True)
Q = L['quiz']
chk('l16 q1', key(Q[1]['widget']), 0.5 * 2000 + 0.35 * 10000 + 0.15 * 45000)
chk('l16 q1 plain', slip(Q[1]['widget'], 'plain'), (2000 + 10000 + 45000) / 3)
chk('l16 q1 grade C 60%', 0.15 * 45000 / 11250, 0.6)
chk('l16 q2', key(Q[2]['widget']), 3)
chk('l16 q3', float(opt(Q[3]['widget'], 'right')['text'].strip('$')), 0.25 * 2 + 0.75 * 6)

# --------------------------------------------------------------- l17
L = load('l17-variance-given-information')
S = L['screens']
inside = 0.8 * 100 ** 2 + 0.2 * 300 ** 2
mean = 0.8 * 120 + 0.2 * -180
between = 0.8 * (120 - mean) ** 2 + 0.2 * (-180 - mean) ** 2
chk('l17 s0 key', key(S[0]['widget']), inside)
chk('l17 s0 sdmix', slip(S[0]['widget'], 'sdmix'), (0.8 * 100 + 0.2 * 300) ** 2)
chk('l17 mean 60', mean, 60)
chk('l17 s2 key', key(S[2]['widget']), between)
chk('l17 s2 unweighted', slip(S[2]['widget'], 'unweighted'), (60 ** 2 + 240 ** 2) / 2)
chk('l17 s2 centre slip is 60^2', slip(S[2]['widget'], 'centre'), mean ** 2)
chk('l17 s3 key', key(S[3]['widget']), inside + between)
chk('l17 s3 sd', round(sqrt(40400)), 201); chk('l17 s3 161', round(sqrt(26000)), 161)
# the explore simulation's outcome rule, replayed: variance settles near 40,400, not 26,000
xs_ = [((120 if rng.random() < 0.5 else -480) if rng.random() < 0.2 else (220 if rng.random() < 0.5 else 20)) for _ in range(400000)]
mu_ = sum(xs_) / len(xs_)
v_ = sum((x - mu_) ** 2 for x in xs_) / len(xs_)
chk('l17 s1 MC variance 40,400', v_, 40400, 600)
T = [[0.10, 0.08, 0.02], [0.10, 0.25, 0.15], [0.03, 0.09, 0.18]]
cv = []
for r in T:
    s = sum(r); p = [x / s for x in r]
    m1 = sum(y * q for y, q in zip(ys, p)); cv.append(sum(y * y * q for y, q in zip(ys, p)) - m1 ** 2)
chk('l17 s4 cond vars', [round(x, 10) for x in cv], [1.76, 1.96, 1.8])
chk('l17 s4 keys', [S[4]['widget']['rows'][1][1]['answer'], S[4]['widget']['rows'][2][1]['answer']], [1.96, 1.8])
# die then coins: exact pmf of H
pmf = {}
for n in range(1, 7):
    for h in range(n + 1):
        pmf[h] = pmf.get(h, 0) + F(1, 6) * comb(n, h) * F(1, 2) ** n
EH = sum(h * p for h, p in pmf.items()); VH = sum(h * h * p for h, p in pmf.items()) - EH ** 2
chk('l17 s5 Var(H) from its own pmf', VH, F(77, 48))
chk('l17 s5 keys', [r[1]['answer'] for r in S[5]['widget']['rows']], [0.875, 0.7292, 1.6042])
chk('l17 s5 35/48', float(F(35, 48)), 0.7292, 5e-5); chk('l17 s5 77/48', float(F(77, 48)), 1.6042, 5e-5)
chk('l17 s6 key', key(S[6]['widget']), 0.2 * 1.76 + 0.5 * 1.96 + 0.3 * 1.8)
chk('l17 s6 plain', slip(S[6]['widget'], 'plain'), (1.76 + 1.96 + 1.8) / 3)
vce = 0.2 * 0.64 + 0.5 * 0.04 + 0.3 * 1.0 - 0.24 ** 2
chk('l17 s6 Var(E[Y|X])', vce, 0.3904)
chk('l17 s6 Var(Y) two ways', 1.872 + vce, 4 * (0.23 + 0.35) - 0.24 ** 2)
chk('l17 s7 20% steadier', round(1 - sqrt(26000) / sqrt(40400), 1), 0.2)
chk('l17 s8 key', key(S[8]['widget']), 0.8 * 1 + 0.2 * 9 + 0.8 * 0.1 ** 2 + 0.2 * 0.4 ** 2)
chk('l17 s8 overall mean 0', 0.8 * 0.1 + 0.2 * -0.4, 0)
chk('l17 s10 key', key(S[10]['widget']), 14400 / 40400, 5e-5)
chk('l17 s10 ratio slip', slip(S[10]['widget'], 'ratio'), 14400 / 26000, 5e-5)
chk('l17 s10 6 sds', (120 - -480) / 100, 6); chk('l17 s10 1 sd', (-180 - -480) / 300, 1)
Q = L['quiz']
chk('l17 q0', key(Q[0]['widget']), 8)
chk('l17 q1', key(Q[1]['widget']), 4 + 25)
chk('l17 q1 double', slip(Q[1]['widget'], 'double'), 4 + 4 + 25)
chk('l17 q2 q3 keys', correct_ids(Q[2]['widget']) + correct_ids(Q[3]['widget']), ['zero', 'ge'])

# --------------------------------------------------------------- l18
L = load('l18-random-sums')
S = L['screens']
nv, npr = [15, 20, 25], [0.4, 0.2, 0.4]
EN = sum(n * p for n, p in zip(nv, npr)); VN = sum(n * n * p for n, p in zip(nv, npr)) - EN ** 2
chk('l18 E[N] Var(N)', [EN, round(VN, 9)], [20, 20])
chk('l18 fill mean sd', [(35 - 25) / 2, (35 + 25) / 2], [5, 30])
chk('l18 s0 key', key(S[0]['widget']), EN * 5)
chk('l18 s2 key', key(S[2]['widget']), 25 * 900)
chk('l18 s2 squared', slip(S[2]['widget'], 'squared'), 25 ** 2 * 900)
chk('l18 s2 sd slip', slip(S[2]['widget'], 'sd'), 25 * 30)
chk('l18 s3 keys', [r[1]['answer'] for r in S[3]['widget']['rows']], [EN * 900, VN * 25, EN * 900 + VN * 25])
chk('l18 s3 sd 136.01', round(sqrt(18500), 2), 136.01)
chk('l18 s4 key', key(S[4]['widget']), sqrt(18000), 0.005)
# exact variance of the random sum by enumeration over N and the number of +35 fills
ex1 = ex2 = F(0)
for n, p in zip(nv, [F(2, 5), F(1, 5), F(2, 5)]):
    for k in range(n + 1):
        s = 35 * k - 25 * (n - k); w = p * comb(n, k) * F(1, 2) ** n
        ex1 += w * s; ex2 += w * s * s
chk('l18 exact mean', ex1, 100); chk('l18 exact variance 18,500', ex2 - ex1 ** 2, 18500)
chk('l18 s5 key', key(S[5]['widget']), 3.5 * 0.25 + 35 / 12 * 0.25, 5e-5)
chk('l18 s5 squared slip', slip(S[5]['widget'], 'squared'), 3.5 ** 2 * 0.25)
chk('l18 s8 key', key(S[8]['widget']), EN * 900)
env = run_code(S[9]['widget'], 'l18 s9 code')
simv = env['random_sum']([15, 20, 25], [0.4, 0.2, 0.4], [35, -25], [0.5, 0.5], 20000, 8)[1]
chk('l18 s9 stated sample variance in explain', f'{simv}' in S[9]['explain']['text'], True)
chk('l18 s10 key', key(S[10]['widget']), 24 * 900 + 64 * 25)
chk('l18 s10 Var(N)', 0.8 * 16 + 0.2 * 256, 64)
chk('l18 s10 by total variance', 0.8 * 18000 + 0.2 * 36000 + 0.8 * 20 ** 2 + 0.2 * 80 ** 2, 23200)
chk('l18 s10 squared', slip(S[10]['widget'], 'squared'), 24 ** 2 * 900)
chk('l18 s10 sd', slip(S[10]['widget'], 'sd'), sqrt(23200), 0.005)
Q = L['quiz']
chk('l18 q0', key(Q[0]['widget']), 10 * 5 + 4 * 9)
chk('l18 q0 swapped = E[N]E[X]^2 + Var(N)Var(X)', slip(Q[0]['widget'], 'swapped'), 10 * 9 + 4 * 5)
chk('l18 q1', key(Q[1]['widget']), 20 * 100)
chk('l18 q3', key(Q[3]['widget']), sqrt(12 * 9e6 + 16 * 4e6), 1)
chk('l18 q3 fixed', slip(Q[3]['widget'], 'fixed'), sqrt(12 * 9e6), 1)
# Dependence between the count and the terms: the formulas CAN fail, and CAN still hold.
# (a) busy days have worse fills: N=10 with fills +-1 mean 1 ... N=30 with mean -1
#     pooled E[X] over fills is not what E[S]/E[N] needs.
ES = 0.5 * 10 * 1 + 0.5 * 30 * -1          # true mean
EXfill = (0.5 * 10 * 1 + 0.5 * 30 * -1) / 20  # mean of a randomly chosen fill
EXday = 0.5 * 1 + 0.5 * -1                  # mean fill on a randomly chosen day
chk('l18 dependence can break E[S] = E[N]E[X] (day-average X)', abs(ES - 20 * EXday) > 1, True)
# (b) dependent but the formulas still hold: the fill's SIGN pattern depends on N while each
#     fill given N keeps the same mean and variance and stays independent of the others:
#     N=1 -> fill is +-1 fair coin; N=2 -> fill is +-1 fair coin too but drawn as -(coin).
#     Trivially same law, so use a real dependence: N = 1 + [X_1 > 0] (N depends on the first term).
#     S = X_1 + (X_2 if X_1>0). E[S] = 0 + 0.5*0 = 0 = E[N]E[X] (Wald, N a stopping time).
tot = 0.0; tot2 = 0.0; cnt = 0
for x1 in (-1, 1):
    for x2 in (-1, 1):
        s = x1 + (x2 if x1 > 0 else 0)
        tot += 0.25 * s
chk('l18 Wald: mean formula holds for a stopping-time N that depends on the terms', tot, 1.5 * 0)

# --------------------------------------------------------------- l19
L = load('l19-convex-bets')
S = L['screens']
chk('l19 s0 key', key(S[0]['widget']), 100 * 1.1 * 0.9)
chk('l19 s2 key', key(S[2]['widget']), 0.5 * log(0.99), 5e-6)
chk('l19 s3 key', key(S[3]['widget']), (4 + 64) / 2 - 25)
chk('l19 s4 key', key(S[4]['widget']), 300 / 17.5, 0.005)
chk('l19 s4 mean slip', slip(S[4]['widget'], 'mean'), 70 / 3, 0.005)
chk('l19 s4 E[1/X] >= 1/E[X]', (0.1 + 0.05 + 0.025) / 3 > 3 / 70, True)
chk('l19 s5 key', key(S[5]['widget']), 10)
chk('l19 s6 hint', [(1 + 3) / 2, round(sqrt(5), 3)], [2, 2.236])
# second-order gap for sqrt: sigma^2 / (8 mu^1.5), checked on a tight distribution
mu, d = 100.0, 1.0
gap = sqrt(mu) - (sqrt(mu - d) + sqrt(mu + d)) / 2
chk('l19 s6 second-order gap', gap, d * d / (8 * mu ** 1.5), 1e-8)
# s7: convex / concave directions on random positive X, and either way for the product pair
ok = True
for _ in range(2000):
    x = [rng.uniform(0.01, 5) for _ in range(4)]; w = [rng.random() for _ in range(4)]; t = sum(w); w = [a / t for a in w]
    m_ = sum(a * b for a, b in zip(w, x))
    ok &= sum(a * exp(b) for a, b in zip(w, x)) >= exp(m_) - 1e-12
    ok &= sum(a * sqrt(b) for a, b in zip(w, x)) <= sqrt(m_) + 1e-12
    ok &= sum(a * b ** 3 for a, b in zip(w, x)) >= m_ ** 3 - 1e-12
    ok &= sum(a / b for a, b in zip(w, x)) >= 1 / m_ - 1e-12
    ok &= sum(a * log(b) for a, b in zip(w, x)) <= log(m_) + 1e-12
chk('l19 s7 Jensen directions (2000 random pmfs)', ok, True)
acc = {s['id']: s['accepts'] for s in S[7]['widget']['slots']}
tok = {t['id']: t['text'] for t in S[7]['widget']['tokens']}
chk('l19 s7 keys', [tok[acc[k][0]] for k in 'abcd'], ['left ≥ right', 'left ≤ right', 'left ≥ right', 'either way'])
chk('l19 s9 key', key(S[9]['widget']), (-27 + 1) / 2 - (-1) ** 3)
chk('l19 s9 mirror +12', (-1 + 27) / 2 - 1 ** 3, 12)
chk('l19 s10 key', key(S[10]['widget']), sqrt(4 * 9))
g = 0.5 * (log(1.07) + log(0.95))
chk('l19 s11 mean sd', [round((0.07 - 0.05) / 2, 10), round((0.07 + 0.05) / 2, 10)], [0.01, 0.06])
chk('l19 s11 key', key(S[11]['widget']), g, 5e-6)
chk('l19 s11 nohalf', slip(S[11]['widget'], 'nohalf'), 0.01 - 0.06 ** 2)
chk('l19 s11 drag', slip(S[11]['widget'], 'drag'), 0.06 ** 2 / 2)
chk('l19 s11 e^0.982', round(exp(120 * g), 2), 2.67)
chk('l19 s11 1.01^120', round(1.01 ** 120, 2), 3.30)
# typical path: the median of 120 fair +7/-5 months is 60 ups
chk('l19 s11 median path', round(1.07 ** 60 * 0.95 ** 60, 2), 2.67)
Q = L['quiz']
chk('l19 q1', key(Q[1]['widget']), 5 - 4)
chk('l19 q2', key(Q[2]['widget']), 200 / 25)
chk('l19 q keys', correct_ids(Q[0]['widget']) + correct_ids(Q[3]['widget']), ['lt', 'none'])

# --------------------------------------------------------------- l20
L = load('l20-many-categories')
S = L['screens']
chk('l20 s0 key', key(S[0]['widget']), comb(10, 5))
chk('l20 s0 ordered', slip(S[0]['widget'], 'ordered'), 10 * 9 * 8 * 7 * 6)


def multi(counts, probs):
    n = sum(counts); o = factorial(n)
    for c in counts:
        o //= factorial(c)
    pr = 1.0
    for c, p in zip(counts, probs):
        pr *= p ** c
    return o * pr


chk('l20 s1 records', S[1]['widget']['rows'][0][1]['answer'], factorial(10) // (120 * 2 * 6))
chk('l20 s1 chance', S[1]['widget']['rows'][1][1]['answer'], multi([5, 2, 3], [0.5, 0.2, 0.3]), 5e-5)
chk('l20 s2 key', key(S[2]['widget']), 252 / 1024, 5e-5)
# covariance of up and down counts by exact enumeration
cov = 0.0; eu = ed = 0.0
for u in range(11):
    for dd in range(11 - u):
        p = multi([u, 10 - u - dd, dd], [0.5, 0.2, 0.3]); eu += u * p; ed += dd * p; cov += u * dd * p
chk('l20 s3 Cov = -1.5', cov - eu * ed, -1.5, 1e-9)
chk('l20 s4 binomials', [round(comb(10, 4) / 1024, 4), round(comb(10, 4) * 0.3 ** 4 * 0.7 ** 6, 4)], [0.2051, 0.2001])
chk('l20 s4 product 0.0410', round(0.2051 * 0.2001, 4), 0.0410)
chk('l20 s4 key', key(S[4]['widget']), multi([4, 2, 4], [0.5, 0.2, 0.3]), 5e-5)
chk('l20 s4 rho', round(-1.5 / sqrt(2.5 * 2.1), 2), -0.65)
chk('l20 s5 key', key(S[5]['widget']), 3 / 0.4)
chk('l20 s5 fails slip', slip(S[5]['widget'], 'fails'), 3 * 0.6 / 0.4)
V = 1.5 / 0.4
chk('l20 s6 1.5 is var of cond means', 0.4 * 0.6 * 2.5 ** 2, 1.5)
chk('l20 s6 key', key(S[6]['widget']), 3 * V)
nb = lambda t, r, p: comb(t - 1, r - 1) * p ** r * (1 - p) ** (t - r)
chk('l20 s7 P(T=5)', S[7]['widget']['rows'][0][1]['answer'], nb(5, 3, 0.4), 5e-5)
chk('l20 s7 P(T<=6)', S[7]['widget']['rows'][1][1]['answer'], sum(nb(t, 3, 0.4) for t in range(3, 7)), 5e-5)
chk('l20 s7 = at least 3 wins in 6', sum(nb(t, 3, 0.4) for t in range(3, 7)), sum(comb(6, k) * 0.4 ** k * 0.6 ** (6 - k) for k in range(3, 7)))
chk('l20 s7 canvas pmf', all(abs(a - nb(t, 3, 0.4)) < 1e-12 for a, t in zip(S[7]['canvas']['params']['params']['probs'], S[7]['canvas']['params']['params']['values'])), True)
chk('l20 s8 0.2304', comb(5, 3) * 0.4 ** 3 * 0.6 ** 2, 0.2304)
chk('l20 s8 0.3174', round(sum(nb(t, 3, 0.4) for t in range(3, 6)), 4), 0.3174)
chk('l20 s9 key', key(S[9]['widget']), multi([6, 0, 4], [0.6, 0, 0.4]), 5e-5)
chk('l20 s9 one slip', slip(S[9]['widget'], 'one'), 0.6 ** 6 * 0.4 ** 4, 5e-5)
# FAILS ON PURPOSE (finding 1): the screen's tree still shows the earlier stock, 0.5 / 0.2 / 0.3,
# while the prose and the key use 0.6 / 0 / 0.4.
tree = [b['p'] for b in S[9]['canvas']['params']['levels'][0]['branches']]
chk('l20 s9 canvas tree matches the prose chances 0.6 / 0 / 0.4', tree, [0.6, 0, 0.4])
run_code(S[10]['widget'], 'l20 s10 code')
chk('l20 s11 key', key(S[11]['widget']), sum(comb(10, k) * 0.4 ** k * 0.6 ** (10 - k) for k in range(3)), 5e-5)
chk('l20 s11 = P(T>10)', 1 - sum(nb(t, 3, 0.4) for t in range(3, 11)), sum(comb(10, k) * 0.4 ** k * 0.6 ** (10 - k) for k in range(3)))
Q = L['quiz']
chk('l20 q0', key(Q[0]['widget']), multi([2, 1, 1], [0.5, 0.3, 0.2]))
chk('l20 q1', key(Q[1]['widget']), -20 * 0.25 * 0.4)
chk('l20 q1 var slip', slip(Q[1]['widget'], 'var'), 20 * 0.25 * 0.75)
chk('l20 q2', key(Q[2]['widget']), nb(4, 2, 0.5))
# MC: negative binomial mean and variance r/p, r(1-p)/p^2
ts = []
for _ in range(200000):
    t = w = 0
    while w < 3:
        t += 1; w += rng.random() < 0.4
    ts.append(t)
mt = sum(ts) / len(ts); vt = sum((t - mt) ** 2 for t in ts) / len(ts)
chk('l20 MC E[T] 7.5', mt, 7.5, 0.04); chk('l20 MC Var(T) 11.25', vt, 11.25, 0.25)

# --------------------------------------------------------------- review-4
R = load('review-4')['items']
T = [[0.15, 0.25, 0.20], [0.05, 0.10, 0.25]]
chk('rev4 0', key(R[0]['widget']), 0.20 + 0.25)
chk('rev4 1', float(opt(R[1]['widget'], 'right')['text'].strip('$')), 0.25 / 0.40)
chk('rev4 1 rev', float(opt(R[1]['widget'], 'rev')['text'].strip('$')), round(0.25 / 0.45, 3))
G = [[0.20, 0.14, 0.06], [0.30, 0.16, 0.14]]
rg = [sum(r) for r in G]; cg = [G[0][j] + G[1][j] for j in range(3)]
chk('rev4 2', sorted(f'r{i+1}c{j+1}' for i in range(2) for j in range(3) if abs(G[i][j] - rg[i] * cg[j]) > 1e-9), sorted(R[2]['widget']['answer']))
x4 = [-2, -1, 1, 2]
chk('rev4 3 cov 0', sum(x ** 3 for x in x4) / 4 - (sum(x4) / 4) * (sum(x * x for x in x4) / 4), 0)
chk('rev4 4', key(R[4]['widget']), (-0.05 + 0.25) / 0.40)
chk('rev4 5', key(R[5]['widget']), 0.6 * (1 / 12) + 0.4 * 0.5)
chk('rev4 5 weak mean', (-0.15 + 0.20) / 0.60, 1 / 12)
chk('rev4 5 plain', slip(R[5]['widget'], 'plain'), (1 / 12 + 0.5) / 2, 1e-4)
chk('rev4 5 mult', slip(R[5]['widget'], 'mult'), 1 / 24, 1e-4)
chk('rev4 6', key(R[6]['widget']), 1 / 0.4)
chk('rev4 6 heads slip', slip(R[6]['widget'], 'heads'), 1 / 0.6, 1e-4)
chk('rev4 7', -0.125 + 0.625, 0.5)

# --------------------------------------------------------------- review-5
R = load('review-5')['items']
chk('rev5 0', key(R[0]['widget']), 25 + 100)
chk('rev5 1', key(R[1]['widget']), 6 * 4 + 9 * 9)
chk('rev5 1 swap', slip(R[1]['widget'], 'swap'), 6 * 9 + 9 * 4)
chk('rev5 2 example', [F(1, 2) * (1 + F(1, 3)), F(1, 2)], [F(2, 3), F(1, 2)])
chk('rev5 3', key(R[3]['widget']), multi([3, 1, 1], [0.6, 0.3, 0.1]), 5e-6)
chk('rev5 4', key(R[4]['widget']), sqrt(5), 5e-4)
chk('rev5 5', key(R[5]['widget']), 0.01 - 0.04 ** 2 / 2)
chk('rev5 5 exact 0.9165%', round(50 * (log(1.05) + log(0.97)), 4), 0.9165)
chk('rev5 6', key(R[6]['widget']), 20 * 100 + 100 * 4)
chk('rev5 6 sd slip close to sd', abs(slip(R[6]['widget'], 'sd') - sqrt(2400)) < 0.5, True)
chk('rev5 7', key(R[7]['widget']), 2 * 0.8 / 0.04)
chk('rev5 8', key(R[8]['widget']), 4 * 5 + 12 * 9)
chk('rev5 8 geometric moments', [1 / 0.25, 0.75 / 0.0625], [4, 12])
chk('rev5 9 keys', correct_ids(R[9]['widget']), ['a', 'b', 'c'])

# --------------------------------------------------------------- homework-4
H = load('homework-4')['items']
chk('hw4 0', [r[1]['answer'] for r in H[0]['widget']['rows']], [0.9, 0.6, 0.3, 0.0952])
chk('hw4 0 last', 0.06 / 0.63, 0.0952, 5e-5)
chk('hw4 1', key(H[1]['widget']), 0.6 * (0.12 / 0.40))
chk('hw4 2 keys', correct_ids(H[2]['widget']), ['a', 'c'])
chk('hw4 3 E[B|A=a]=0', all(abs(sum(b * J[(a, b)] for b in vals)) < 1e-12 for a in vals), True)
chk('hw4 3 key', correct_ids(H[3]['widget']), ['right'])
# head then tail: two-state equations and Monte Carlo
EHs = 2; E0 = (1 + 0.5 * EHs) / 0.5
chk('hw4 5 key', key(H[5]['widget']), E0)
m = sum(wait_pattern('HT', rng) for _ in range(200000)) / 200000
chk('hw4 5 MC HT wait 4', m, 4, 0.04)
# In a race, HT and HH are equally likely to appear first (finding: "beats" misleads)
first = 0
for _ in range(100000):
    s = ''
    while not (s.endswith('HT') or s.endswith('HH')):
        s += 'H' if rng.random() < 0.5 else 'T'
    first += s.endswith('HT')
chk('hw4 5 race HT v HH is even', first / 100000, 0.5, 0.01)
chk('hw4 7', key(H[7]['widget']), 0.25 * 800 + 0.6 * -100 + 0.15 * -1500)
chk('hw4 7 plain', slip(H[7]['widget'], 'plain'), (800 - 100 - 1500) / 3, 0.005)
# two sixes in a row: a = 1 + b/6 + 5a/6, b = 1 + 5a/6
a = F(7, 6) / (1 - F(35, 36)); b = 1 + F(5, 6) * a
chk('hw4 8 a=42 b=36', [a, b], [42, 36])
chk('hw4 8 model states 42', '$a = 42$' in H[8]['model'], True)


def wait66(r):
    n = run = 0
    while run < 2:
        n += 1
        run = run + 1 if r.random() < 1 / 6 else 0
    return n


m = sum(wait66(rng) for _ in range(100000)) / 100000
chk('hw4 8 MC two sixes 42', m, 42, 0.6)

# --------------------------------------------------------------- homework-5
H = load('homework-5')['items']
chk('hw5 0', key(H[0]['widget']), 0.75 * 4 + 0.25 * 36 + 0.75 * 1 + 0.25 * 9)
chk('hw5 0 mean 0', 0.75 * 1 + 0.25 * -3, 0)
chk('hw5 2', key(H[2]['widget']), 30 * 25 + 45 * 64)
chk('hw5 2 sd 60.25', round(sqrt(3630), 2), 60.25)
acc = {s['id']: s['accepts'] for s in H[3]['widget']['slots']}
tok = {t['id']: t['text'] for t in H[3]['widget']['tokens']}
chk('hw5 3 keys', [tok[acc[k][0]] for k in 'abcd'], ['left ≤ right', 'left ≥ right', 'left ≥ right', 'left ≤ right'])
chk('hw5 4', key(H[4]['widget']), -sqrt(0.4 * 0.35 / (0.6 * 0.65)), 5e-4)
chk('hw5 4 by parts', -7 / sqrt(12 * 11.375), -sqrt(0.4 * 0.35 / (0.6 * 0.65)))
chk('hw5 5', key(H[5]['widget']), 4 + 2 / 0.4)
# MC of hw5 5: condition on exactly one win in the first four trades
tot = cnt = 0
for _ in range(400000):
    first4 = [rng.random() < 0.4 for _ in range(4)]
    if sum(first4) != 1:
        continue
    t, w = 4, 1
    while w < 3:
        t += 1; w += rng.random() < 0.4
    tot += t; cnt += 1
chk('hw5 5 MC 9', tot / cnt, 9, 0.06)
env = run_code(H[6]['widget'], 'hw5 6 code')
chk('hw5 6 exact p=0.2', env['book_exact'](F(1, 5)), (120, 23200))
chk('hw5 7 1.012^120', round(1.012 ** 120, 2), 4.18)
chk('hw5 7 ln 1.012', round(log(1.012), 5), 0.01193)
chk('hw5 7 rate', 0.012 - 0.07 ** 2 / 2, 0.00955)
chk('hw5 7 e^1.146', round(exp(120 * 0.00955), 1), 3.1)
chk('hw5 7 roughly a quarter lower', 0.2 < 1 - exp(1.146) / 1.012 ** 120 < 0.3, True)
# Step 5: a regime mixture with the same mean and sd has a lower E[ln(1+R)] than the one-regime
# two-point return. Calm +-s1 (chance 0.8), volatile +-s2 (0.2), 0.8 s1^2 + 0.2 s2^2 = 0.07^2.
base = 0.5 * (log(1.012 + 0.07) + log(1.012 - 0.07))
okm = True
for s1 in (0.02, 0.03, 0.04, 0.05, 0.06):
    s2 = sqrt((0.07 ** 2 - 0.8 * s1 ** 2) / 0.2)
    mix = 0.8 * 0.5 * (log(1.012 + s1) + log(1.012 - s1)) + 0.2 * 0.5 * (log(1.012 + s2) + log(1.012 - s2))
    okm &= mix < base
chk('hw5 7 mixture with the same sd lowers E[ln(1+R)]', okm, True)
chk('hw5 8', H[8]['widget']['answer'], 'm b + v a^{2}')

# --------------------------------------------------------------- problems-4
P = load('problems-4')['items']
pw = lambda i, j: P[i]['parts'][j]['widget']
V = {(1, 0): 0.36, (1, 1): 0.18, (1, 2): 0.06, (2, 0): 0.12, (2, 1): 0.20, (2, 2): 0.08}
chk('p4 vans sum', sum(V.values()), 1)
chk('p4 0.0', key(pw(0, 0)), V[(1, 1)] + V[(2, 1)])
chk('p4 0.1', key(pw(0, 1)), 0.08 / 0.40)
chk('p4 0.1 reversed', slip(pw(0, 1), 'reversed'), 0.08 / 0.14, 0.005)
chk('p4 0.1 wrong-row', slip(pw(0, 1), 'wrong-row'), 0.08 / 0.60, 0.005)
chk('p4 0.2 key', correct_ids(pw(0, 2)), ['no'])
chk('p4 0.2 cell differs', abs(0.36 - 0.60 * 0.48) > 0.05, True)
chk('p4 0.3', key(pw(0, 3)), (0.20 + 0.16) / 0.40)
chk('p4 0.3 row-one', slip(pw(0, 3), 'row-one'), (0.18 + 0.12) / 0.60)
chk('p4 0.4', key(pw(0, 4)), 6 * (0.6 * 0.5 + 0.4 * 0.9))
chk('p4 0.4 carried', slip(pw(0, 4), 'carried'), 6 * (0.6 * 0.5 + 0.4 * 0.36), 0.005)
chk('p4 0.4 column check', 0.38 + 2 * 0.14, 0.66)
px = [0.5, 0.3, 0.2]; py = [0.7, 0.3]
chk('p4 1.0', key(pw(1, 0)), px[1] * py[1])
ps2 = px[2] * py[0] + px[1] * py[1]
chk('p4 1.1', key(pw(1, 1)), ps2)
chk('p4 1.2', key(pw(1, 2)), (2 * px[2] * py[0] + px[1] * py[1]) / ps2, 5e-5)
chk('p4 1.2 prior', slip(pw(1, 2), 'prior'), 0.3 + 0.4)
chk('p4 1.3 key', correct_ids(pw(1, 3)), ['yes'])
chk('p4 1.3 P(Y=1|S=2) moved', px[1] * py[1] / ps2 > 0.3, True)
chk('p4 1.3 S=2 likelier when route 2 late', px[1] > px[2], True)
# Counterexample to "any total that depends on Y moves its chances": two fair independent bits.
# P(Y=1 | X+Y=1) = 1/2 = P(Y=1). (finding: the why line overstates)
chk('p4 1.3 counterexample: S=1 leaves a fair bit at 1/2', F(1, 4) / (F(1, 4) + F(1, 4)), F(1, 2))
chk('p4 1.4', key(pw(1, 4)), 2 - (2 * px[2] * py[0] + px[1] * py[1]) / ps2, 5e-5)
chk('p4 1.4 = 9/23', float(F(9, 23)), key(pw(1, 4)), 5e-5)
Yg = [0.12, 0.05, 0.03]; Og = [0.64, 0.12, 0.04]
chk('p4 insurer sum', sum(Yg) + sum(Og), 1)
chk('p4 2.0', key(pw(2, 0)), 0.03 / 0.07, 5e-5)
chk('p4 2.1', key(pw(2, 1)), (0.05 + 0.06) / 0.20)
chk('p4 2.1 older', slip(pw(2, 1), 'older'), (0.12 + 0.08) / 0.80)
chk('p4 2.2', key(pw(2, 2)), 0.2 * 0.55 + 0.8 * 0.25)
chk('p4 2.2 swapped', slip(pw(2, 2), 'swapped'), 0.8 * 0.55 + 0.2 * 0.25)
chk('p4 2.3', key(pw(2, 3)), 2000 * 0.55 - 2000 * 0.31)
chk('p4 2.3 carried', slip(pw(2, 3), 'carried'), 2000 * 0.55 - 2000 * 0.4)
chk('p4 2.4', key(pw(2, 4)), 2000 * 0.31 - 2000 * 0.25)
chk('p4 2.4 balance', 0.2 * 480, 0.8 * 120)
mm = 2.1 / 0.5
chk('p4 3.1', key(pw(3, 1)), mm)
chk('p4 3.1 carried', slip(pw(3, 1), 'carried'), 1.5 / 0.5)
chk('p4 3.1 sign', slip(pw(3, 1), 'sign'), 2.1 / 1.5)
chk('p4 3.2', key(pw(3, 2)), 0.6 * 2 + 0.4 * 5 + mm)
chk('p4 3.2 unscaled', slip(pw(3, 2), 'unscaled'), 0.3 * (2 + mm) + 0.2 * (5 + mm))
mB = (0.7 * 1.5 + 0.3 * 3) / 0.7
chk('p4 3.3 mB', round(mB, 4), 2.7857)
chk('p4 3.3', key(pw(3, 3)), 0.5 + 0.5 * (3.2 + mB), 5e-5)
chk('p4 3.4', key(pw(3, 4)), 5 - 3.2)
chk('p4 3.4 kept-m', slip(pw(3, 4), 'kept-m'), 5 - 7.4)
# MC of the retry time
tt = 0.0
for _ in range(300000):
    t = 0.0
    while True:
        u = rng.random()
        if u < 0.5:
            t += 1; break
        t += 2 if u < 0.8 else 5
    tt += t
chk('p4 3 MC m = 4.2', tt / 300000, 4.2, 0.03)

# --------------------------------------------------------------- problems-5
P = load('problems-5')['items']
pw = lambda i, j: P[i]['parts'][j]['widget']
en = 0.7 * 40 + 0.3 * 10; vn = 0.7 * 40 + 0.3 * 10 + 0.7 * (40 - en) ** 2 + 0.3 * (10 - en) ** 2
chk('p5 0.0', key(pw(0, 0)), en); chk('p5 0.1', key(pw(0, 1)), vn)
chk('p5 0.1 unsquared', slip(pw(0, 1), 'unsquared'), 31 + 0.7 * 9 + 0.3 * 21, 0.05)
chk('p5 0.1 carried', slip(pw(0, 1), 'carried'), 31 + 225)
chk('p5 0.2', key(pw(0, 2)), en * 1.5)
chk('p5 0.3', key(pw(0, 3)), en * 0.25 + vn * 2.25)
chk('p5 0.3 carried', slip(pw(0, 3), 'carried'), 31 * 0.25 + 31 * 2.25)
chk('p5 0.4', key(pw(0, 4)), vn * 2.25 / (en * 0.25 + vn * 2.25), 5e-5)
chk('p5 0.4 between', slip(pw(0, 4), 'between'), 189 * 2.25 / 502.75, 5e-5)
sp = {30: 0.25, 40: 0.5, 60: 0.25}
ev = sum(v * p for v, p in sp.items())
chk('p5 1.0', key(pw(1, 0)), ev)
chk('p5 1.1', key(pw(1, 1)), 12 / ev * 60, 0.005)
et = sum(12 / v * 60 * p for v, p in sp.items())
chk('p5 1.2', key(pw(1, 2)), et)
chk('p5 1.3 key', correct_ids(pw(1, 3)), ['jensen'])
tm = {24: 0.25, 18: 0.5, 12: 0.25}
pover = sum(math.prod(tm[t] for t in c) for c in itertools.product(tm, repeat=4) if sum(c) > 80)
chk('p5 1.4', key(pw(1, 4)), pover, 5e-5); chk('p5 1.4 = 37/256', pover, 37 / 256)
chk('p5 1.4 no flight total equals 80', any(sum(c) == 80 for c in itertools.product(tm, repeat=4)), False)
chk('p5 1.4 slow-count', slip(pw(1, 4), 'slow-count'), 1 - 0.75 ** 4 - 4 * 0.25 * 0.75 ** 3, 5e-5)
chk('p5 1.4 one-more-slow', slip(pw(1, 4), 'one-more-slow'),
    sum(math.prod(tm[t] for t in c) for c in itertools.product(tm, repeat=4) if sum(c) > 72), 5e-5)
chk('p5 1.4 about one day in seven', round(1 / pover), 7)
chk('p5 2.0', key(pw(2, 0)), nb(5, 2, 0.1), 1e-9)
chk('p5 2.1', key(pw(2, 1)), 0.6 * 20 + 0.4 * 10)
chk('p5 2.1 pooled', slip(pw(2, 1), 'pooled'), 2 / 0.14, 0.005)
chk('p5 2.2', key(pw(2, 2)), 0.6 * 180 + 0.4 * 40)
chk('p5 2.3', key(pw(2, 3)), 124 + 0.6 * 16 + 0.4 * 36)
chk('p5 2.4', key(pw(2, 4)), 24 / 148, 5e-5)
chk('p5 2.4 carried', slip(pw(2, 4), 'carried'), 4.8 / 128.8, 5e-5)
# exact Var(T) for the mixed batch from the pmf
e1 = e2 = 0.0
for t in range(2, 4000):
    p = 0.6 * nb(t, 2, 0.1) + 0.4 * nb(t, 2, 0.2); e1 += t * p; e2 += t * t * p
chk('p5 2 exact E[T] 16, Var(T) 148', [round(e1, 6), round(e2 - e1 ** 2, 6)], [16, 148])
elr = 0.5 * (log(1.5) + log(0.6)); vlr = (0.5 * (log(1.5) - log(0.6))) ** 2
chk('p5 3.0', key(pw(3, 0)), elr, 5e-5)
chk('p5 3.0 log10 slip', slip(pw(3, 0), 'log10'), 0.5 * math.log10(0.9), 5e-5)
chk('p5 3.1', key(pw(3, 1)), 4 * elr, 5e-4)
chk('p5 3.2 Var(ln R)', round(vlr, 4), 0.2099)
chk('p5 3.2', key(pw(3, 2)), 4 * vlr + 2 * elr ** 2, 5e-4)
ew = 0.25 * 1.05 ** 2 + 0.5 * 1.05 ** 4 + 0.25 * 1.05 ** 6
chk('p5 3.3 E[W]', round(ew, 4), 1.2184); chk('p5 3.3 ln E[W]', round(log(ew), 4), 0.1975)
chk('p5 3.3 key', correct_ids(pw(3, 3)), ['both'])
pl = 0.0
for n, pn in ((2, 0.25), (4, 0.5), (6, 0.25)):
    for k in range(n + 1):
        if 1.5 ** k * 0.6 ** (n - k) < 1:
            pl += pn * comb(n, k) / 2 ** n
        # "exactly when at most half the rounds are up" holds for N = 2, 4, 6
        chk(f'p5 3.4 W<1 iff k<=N/2 (N={n},k={k})', (1.5 ** k * 0.6 ** (n - k) < 1) == (k <= n / 2), True)
chk('p5 3.4', key(pw(3, 4)), pl, 5e-5); chk('p5 3.4 = 89/128', pl, 89 / 128)
# ... but not as a general rule (finding: the explain's "so ... exactly when" is true only for small N)
chk('p5 3.4 general counterexample N=20, k=11 still loses', 1.5 ** 11 * 0.6 ** 9 < 1, True)

print(f'{N} checks, failures: {len(FAILS)}')
for f in FAILS:
    print('  -', f)
sys.exit(1 if FAILS else 0)
