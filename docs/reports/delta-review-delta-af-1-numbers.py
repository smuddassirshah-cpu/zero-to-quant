#!/usr/bin/env python3
"""Delta read review-delta-af-1: independent recompute of the re-authored items.

Scope (session AF re-author of the reuse hits):
  conditional/problems-3 p-rotation-days, conditional/problems-4 p-dark-fills,
  exp-log/problems-1 p-rare-coin, markov/problems-5 p-flat-floor,
  stat-learning/problems-2 p-futures-lasso and p-built-ridge,
  stat-learning/problems-4 p-renewals part 2,
  validation/problems-1 p-arrears-grid parts 2 (one line), 4 and 5.

Methods differ from the author's scripts where one exists: exact fractions,
linear systems, the fundamental matrix of the chain, seeded simulation, and
scikit-learn fits on data built to the stated sums.

Exits 0. A check that fails prints a FINDING line.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COURSES = os.path.join(HERE, '..', '..', 'app', 'content', 'courses')

checks = 0
findings = 0


def check(name, ok, detail=''):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print('FINDING %s %s' % (name, detail))


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def load(course, file, pid):
    with open(os.path.join(COURSES, course, file), encoding='utf-8') as fh:
        data = json.load(fh)
    for it in data['items']:
        if it['id'] == pid:
            return it
    raise SystemExit('missing %s in %s/%s' % (pid, course, file))


def text_of(part):
    out = [part['question'], part['explain']['text']]
    fb = part['feedback']
    out += [fb.get('correct', ''), fb.get('generic', '')]
    out += list(fb.get('byKey', {}).values())
    for o in part['widget'].get('options', []):
        out += [o.get('text', ''), o.get('why', '')]
    return ' | '.join(out)


def numeric(name, part, key, wrongs, places=None):
    """Key and every wrong value equal my values; bands separate; no tie."""
    w = part['widget']
    check(name + ' kind', w['kind'] == 'numeric')
    tol = w['tol']['abs']
    stored = w['answer']
    # the stored answer is my value, rounded no further than the band allows
    check(name + ' key', abs(stored - float(key)) <= max(tol * 0.51, 1e-12),
          'stored %r mine %r' % (stored, float(key)))
    check(name + ' key in band', abs(float(key) - stored) <= tol)
    got = {x['id']: x for x in w.get('wrong', [])}
    check(name + ' wrong ids', set(got) == set(wrongs),
          '%s vs %s' % (sorted(got), sorted(wrongs)))
    for wid, val in wrongs.items():
        if wid not in got:
            continue
        g = got[wid]
        wt = g['tol']['abs']
        check('%s wrong %s value' % (name, wid),
              abs(g['value'] - float(val)) <= max(wt, 1e-12),
              'stored %r mine %r' % (g['value'], float(val)))
        # bands do not overlap, and the key refuses my wrong value
        check('%s wrong %s apart' % (name, wid),
              abs(g['value'] - stored) > tol + wt)
        check('%s wrong %s refused' % (name, wid), abs(float(val) - stored) > tol)
        check('%s wrong %s in own band' % (name, wid), abs(float(val) - g['value']) <= wt)
    # wrong bands apart from each other
    ws = list(got.values())
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            check('%s wrong %s/%s apart' % (name, ws[i]['id'], ws[j]['id']),
                  abs(ws[i]['value'] - ws[j]['value']) > ws[i]['tol']['abs'] + ws[j]['tol']['abs'])
    if places is not None:
        # the exact value does not sit on a rounding tie at the stated places
        scaled = F(key) * 10 ** places
        frac = scaled - math.floor(scaled)
        check(name + ' no tie', frac != F(1, 2))
        # the value rounded to the stated places is taken
        r = round(float(key), places)
        check(name + ' rounded taken', abs(r - stored) <= tol)


def has(name, part, *snips):
    t = text_of(part)
    for s in snips:
        check('%s prints %r' % (name, s), s in t)


def choice(name, part, key):
    opts = part['widget']['options']
    right = [o['id'] for o in opts if o.get('correct')]
    check(name + ' key', right == [key], str(right))


# --------------------------------------------------------------------------
# conditional/problems-3 p-rotation-days
# --------------------------------------------------------------------------
it = load('conditional', 'problems-3.json', 'p-rotation-days')
P = it['parts']
px, py, share_on, y_given_x_on = F(6, 10), F(5, 10), F(1, 4), F(8, 10)
both_on = px * y_given_x_on
both_all = px * py
both_rot = (both_all - share_on * both_on) / (1 - share_on)
y_given_x_rot = both_rot / px
numeric('rot p1', P[0], both_on,
        {'indep': px * py, 'cond': y_given_x_on, 'over-y': y_given_x_on * py})
numeric('rot p2', P[1], both_rot,
        {'unweighted': both_all - share_on * both_on,
         'equal': (both_all - F(1, 2) * both_on) / F(1, 2),
         'indep': (both_all - share_on * px * py) / (1 - share_on)})
numeric('rot p3', P[2], y_given_x_rot,
        {'joint': both_rot, 'over-y': both_rot / py,
         'unweighted': (both_all - share_on * both_on) / px})
choice('rot p4', P[3], 'both-dep')
# each kind of day is a valid joint table with the stated marginals
for nm, b in (('risk-on', both_on), ('rotation', both_rot)):
    cells = [b, px - b, py - b, 1 - px - py + b]
    check('rot table %s valid' % nm, all(0 <= c <= 1 for c in cells) and sum(cells) == 1)
    check('rot %s dependent' % nm, b != px * py)
# pooled: independent, and Y's chance given X is exactly 0.5
check('rot pooled product', share_on * both_on + (1 - share_on) * both_rot == px * py)
check('rot pooled cond', (share_on * both_on + (1 - share_on) * both_rot) / px == py)
check('rot p3 below 0.5', y_given_x_rot < py)
has('rot p2', P[1], '0.18', '0.75', '0.3 - 0.12')
has('rot p4', P[3], 'from 0.5 to 0.8', 'cuts Y to 0.4', '0.6 \\times 0.5 = 0.3')
# simulation: draw the kind of day, then the cell of its joint table
rng = np.random.default_rng(20261116)
n = 2_000_000
on = rng.random(n) < float(share_on)
u = rng.random(n)
x = rng.random(n) < float(px)
py_given_x = np.where(on, float(y_given_x_on), float(y_given_x_rot))
py_given_notx = np.where(on, float((py - both_on) / (1 - px)), float((py - both_rot) / (1 - px)))
y = u < np.where(x, py_given_x, py_given_notx)
check('rot sim both|on', abs((x & y)[on].mean() - 0.48) < 0.004)
check('rot sim both|rot', abs((x & y)[~on].mean() - 0.24) < 0.003)
check('rot sim y|x rot', abs(y[~on & x].mean() - 0.4) < 0.004)
check('rot sim y|x all', abs(y[x].mean() - 0.5) < 0.003)
check('rot sim y all', abs(y.mean() - 0.5) < 0.003)

# --------------------------------------------------------------------------
# conditional/problems-4 p-dark-fills
# --------------------------------------------------------------------------
it = load('conditional', 'problems-4.json', 'p-dark-fills')
P = it['parts']
ps, pl, q = F(6, 10), F(4, 10), F(2, 10)
fill_large = pl * 3 / (ps * 1 + pl * 3)
yes_large = 1 - (1 - q) ** 3
post = pl * yes_large / (pl * yes_large + ps * q)
numeric('dark p1', P[0], fill_large, {'orders': pl, 'even': F(1, 2), 'small': 1 - fill_large}, 4)
dark_fill_large = fill_large * q / (fill_large * q + (1 - fill_large) * q)
numeric('dark p2', P[1], dark_fill_large,
        {'orders-slip': pl, 'joint': fill_large * q,
         'double': fill_large * yes_large / (fill_large * yes_large + (1 - fill_large) * q)}, 4)
check('dark p2 equals p1', dark_fill_large == fill_large == F(2, 3))
numeric('dark p3', P[2], yes_large,
        {'sum': 3 * q, 'all': q ** 3, 'exactly-one': 3 * q * (1 - q) ** 2, 'one': q}, 3)
numeric('dark p4', P[3], post,
        {'no-news': pl, 'sum-slip': pl * 3 * q / (pl * 3 * q + ps * q),
         'no-prior': yes_large / (yes_large + q), 'path': pl * yes_large}, 4)
check('dark p4 fraction', post == F(122, 197))
choice('dark p5', P[4], 'ratio')
check('dark lr drawn', (fill_large / (1 - fill_large)) / (pl / ps) == 3)
check('dark lr yes', yes_large / q == F(244, 100))
check('dark order', pl < post < fill_large)
has('dark p4', P[3], '0.1952', '0.3152', '0.12')
has('dark p5', P[4], '2.44', '3 to 1')
# simulation, both ways of learning, 600,000 orders
rng = np.random.default_rng(4471)
n = 600_000
large = rng.random(n) < float(pl)
nf = np.where(large, 3, 1)
dark = rng.random((n, 3)) < float(q)
dark[~large, 1:] = False          # a small order has one fill
tot = nf.sum()
check('dark sim fill large', abs(nf[large].sum() / tot - 2 / 3) < 0.002)
dk = dark.sum(axis=1)
check('dark sim dark fill large', abs(dk[large].sum() / dk.sum() - 2 / 3) < 0.004)
yes = dk > 0
check('dark sim yes|large', abs(yes[large].mean() - 0.488) < 0.004)
check('dark sim large|yes', abs(large[yes].mean() - float(post)) < 0.004)
# the day's fills: with N orders the chance is E[3L / (3L + S)], below 2/3


def fill_chance(N):
    tot = 0.0
    for L in range(N + 1):
        pr = math.comb(N, L) * 0.4 ** L * 0.6 ** (N - L)
        tot += pr * 3 * L / (2 * L + N)
    return tot


band = P[0]['widget']['tol']['abs']
check('dark p1 exact for one order is 0.4', close(fill_chance(1), 0.4))
check('dark p1 key holds at 1,000 orders', abs(fill_chance(1000) - 2 / 3) <= band)
smallest = next(N for N in range(1, 2000) if abs(fill_chance(N) - 2 / 3) <= band)
check('dark p1 stem fixes enough orders for the band (needs %d or more)' % smallest,
      'thousands of' in it['prose'] or 'many' in it['prose'],
      'the stem does not say how many orders the day has; 2/3 is the limit')

# --------------------------------------------------------------------------
# exp-log/problems-1 p-rare-coin
# --------------------------------------------------------------------------
getcontext().prec = 40
it = load('exp-log', 'problems-1.json', 'p-rare-coin')
P = it['parts']
v0, v3 = Decimal('1600'), Decimal('3936.60')
f3 = v3 / v0
check('coin factor exact', f3 == Decimal('2.460375'))
g = Decimal('1.35')
check('coin cube', g ** 3 == f3)
numeric('coin p1', P[0], F(str(f3)), {'inverted': F(str(v0)) / F(str(v3)), 'rise': F(str(f3)) - 1})
numeric('coin p2', P[1], F(str(g)),
        {'thirded-factor': F(str(f3)) / 3, 'thirded-rise': 1 + (F(str(f3)) - 1) / 3,
         'square-root': F(str(f3.sqrt()))})
numeric('coin p3', P[2], F(35, 100),
        {'factor': F(135, 100), 'thirded-rise': (F(str(f3)) - 1) / 3, 'decimal': F(35, 10000)})
check('coin p3 unit', P[2]['widget'].get('unit') == '%' and P[2]['widget'].get('over100') is True)
mid = v0 * g * g.sqrt()
check('coin mid two ways', abs(mid - v3 / (g * g.sqrt())) < Decimal('1e-20'))
numeric('coin p4', P[3], F(str(round(mid, 6))),
        {'mid-value': F(str((v0 + v3) / 2)),
         'simple': F(str(v0 * (1 + Decimal('1.5') * Decimal('0.35')))),
         'two-years-ago': F(str(v0 * g)), 'one-year-ago': F(str(v0 * g * g)),
         'forward': F(str(round(v3 * g * g.sqrt(), 6))),
         'carried': F(str(round(v0 * (1 + (f3 - 1) / 3) ** Decimal('1.5'), 6)))})
for typed in (2509, 2510):
    check('coin p4 takes %d' % typed, abs(typed - P[3]['widget']['answer']) <= P[3]['widget']['tol']['abs'])
check('coin p4 refuses 2511', abs(2511 - P[3]['widget']['answer']) > P[3]['widget']['tol']['abs'])
check('coin check line', v0 * g == 2160 and v0 * g * g == 2916 and v0 * g ** 3 == v3)
check('coin 1.162 line', abs(Decimal('1600') * g * Decimal('1.162') - Decimal('2509.92')) < Decimal('0.005'))
check('coin gain line', (f3 - 1) * 100 == Decimal('146.0375'))
has('coin p4', P[3], '2509.69', '2509.92', '6,174.79', '2,768.30', '1.486792')
has('coin p2', P[1], '2,916', '146.0375%')
txt = json.dumps(it)
for banned in ('1.5625', '0.64', '1.25', '56.25'):
    check('coin drops %s' % banned, banned not in txt)

# --------------------------------------------------------------------------
# markov/problems-5 p-flat-floor
# --------------------------------------------------------------------------
it = load('markov', 'problems-5.json', 'p-flat-floor')
P = it['parts']
TOP, START = 7, 2
choice('floor p1', P[0], 'square')
# one-step drift of each candidate at every level 0..6
for nm, f in (('square', lambda i, n: i * i - n), ('plain', lambda i, n: i),
              ('raw-square', lambda i, n: i * i), ('minus-n', lambda i, n: i - n)):
    drifts = []
    for i in range(TOP):
        if i == 0:
            d = F(f(1, 1)) - f(0, 0)
        else:
            d = F(f(i + 1, 1) + f(i - 1, 1), 2) - f(i, 0)
        drifts.append(d)
    check('floor p1 %s' % nm, all(d == 0 for d in drifts) == (nm == 'square'), str(drifts))
# fundamental matrix of the chain on 0..6 (7 absorbs): N = (I - Q)^-1, exact
Q = [[F(0)] * TOP for _ in range(TOP)]
Q[0][1] = F(1)
for i in range(1, TOP):
    Q[i][i - 1] = F(1, 2)
    if i + 1 < TOP:
        Q[i][i + 1] = F(1, 2)


def inverse(M):
    n = len(M)
    A = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]


N = inverse([[F(int(i == j)) - Q[i][j] for j in range(TOP)] for i in range(TOP)])
ET = sum(N[START])
EF = N[START][0]
check('floor E[T] all starts', all(sum(N[k]) == TOP * TOP - k * k for k in range(TOP)))
check('floor visits to flat once flat', N[0][0] == 7)
# chance of flat before 7, from the absorbing version (0 and 7 both absorb)
h = {0: F(1), TOP: F(0)}
# solve h_k = (h_{k-1} + h_{k+1}) / 2 by the linear form h_k = 1 - k * c
c = F(1, TOP)
flat_first = 1 - START * c
check('floor harmonic', all(1 - k * c == (1 - (k - 1) * c + 1 - (k + 1) * c) / 2 for k in range(1, TOP)))
check('floor return from 1', 1 - 1 * c == F(6, 7))
check('floor E[F] product', EF == flat_first * 7 == 5)
numeric('floor p2', P[1], ET,
        {'ruin': START * (TOP - START), 'no-start': TOP * TOP,
         'gap-squared': (TOP - START) ** 2, 'gap': TOP - START})
numeric('floor p3', P[2], flat_first,
        {'hedge-first': 1 - flat_first, 'ratio': F(START, TOP - START), 'half': F(1, 2)}, 4)
numeric('floor p4', P[3], EF,
        {'given-flat': 7, 'returns': F(6, 7) / F(1, 7), 'no-first': flat_first * 6,
         'one-visit': flat_first})
pnl = 20 * (ET - EF) - 60 * EF
numeric('floor p5', P[4], pnl,
        {'spread-on-flat': 20 * ET - 60 * EF, 'no-flat': 20 * ET, 'income-only': 20 * (ET - EF),
         'given-flat': 20 * (ET - 7) - 60 * 7, 'ruin': 20 * (10 - EF) - 60 * EF})
check('floor I - F martingale', TOP - EF == START)
check('floor cost of flat trades', 80 * EF == 400 and 60 * EF == 300 and 20 * EF == 100)
has('floor p2', P[1], '49 - 4 = 45', 't_k = 49 - k^2')
has('floor p5', P[4], '800 - 300', '£400', '20 \\times 45 - 80 \\times 5')
# simulation: 200,000 paths, seeded
rng = np.random.default_rng(7)
paths = 200_000
pos = np.full(paths, START)
T = np.zeros(paths, dtype=np.int64)
Fl = np.zeros(paths, dtype=np.int64)
ever_flat = np.zeros(paths, dtype=bool)
live = np.ones(paths, dtype=bool)
while live.any():
    idx = np.nonzero(live)[0]
    p = pos[idx]
    flat = p == 0
    step = np.where(rng.random(idx.size) < 0.5, 1, -1)
    step[flat] = 1
    Fl[idx] += flat
    ever_flat[idx] |= flat
    pos[idx] = p + step
    T[idx] += 1
    live[idx] = pos[idx] < TOP
se = T.std() / math.sqrt(paths)
check('floor sim E[T]', abs(T.mean() - 45) < 4 * se, '%.3f' % T.mean())
check('floor sim P(flat first)', abs(ever_flat.mean() - 5 / 7) < 0.004, '%.4f' % ever_flat.mean())
check('floor sim E[F]', abs(Fl.mean() - 5) < 4 * Fl.std() / math.sqrt(paths), '%.3f' % Fl.mean())
check('floor sim E[F | flat]', abs(Fl[ever_flat].mean() - 7) < 0.08)
pl_sim = 20 * (T - Fl) - 60 * Fl
check('floor sim P&L', abs(pl_sim.mean() - 500) < 4 * pl_sim.std() / math.sqrt(paths), '%.1f' % pl_sim.mean())
check('floor sim stops at 7', (pos == TOP).all())

# --------------------------------------------------------------------------
# stat-learning/problems-2 p-futures-lasso: scikit-learn on built data
# --------------------------------------------------------------------------
from sklearn.linear_model import Lasso, LinearRegression, Ridge

it = load('stat-learning', 'problems-2.json', 'p-futures-lasso')
P = it['parts']
rng = np.random.default_rng(11)
n = 240
Z = rng.standard_normal((n, 3))
Z -= Z.mean(axis=0)
Qm, _ = np.linalg.qr(Z)            # orthonormal, centred columns
X = Qm * math.sqrt(n)              # z-scores (sd 1, divisor n), exactly uncorrelated
check('lasso built z-scores', np.allclose(X.T @ X / n, np.eye(3)) and np.allclose(X.mean(axis=0), 0))
b_ols = np.array([2.0, -1.2, 0.5])
y = 0.2 + X @ b_ols
xnew = np.array([[-0.5, -1.0, 2.0]])


def forecast(alpha):
    if alpha == 0:
        m = LinearRegression().fit(X, y)
    else:
        m = Lasso(alpha=alpha, tol=1e-13, max_iter=100000).fit(X, y)
    return float(m.predict(xnew)[0]), m


f_ols, m0 = forecast(0)
check('lasso ols coef', np.allclose(m0.coef_, b_ols) and close(m0.intercept_, 0.2, 1e-9))
f02, m02 = forecast(0.2)
check('lasso coef at 0.2', np.allclose(m02.coef_, [1.8, -1.0, 0.3], atol=1e-8) and close(m02.intercept_, 0.2, 1e-8))
f05, m05 = forecast(0.5)
check('lasso demand leaves at 0.5', abs(m05.coef_[2]) < 1e-9 and close(f05, 0.15, 1e-7))
check('lasso demand in below 0.5', abs(forecast(0.49)[1].coef_[2]) > 1e-3)
lo, hi = 0.5, 1.2
for _ in range(60):
    md = (lo + hi) / 2
    if forecast(md)[0] > 0:
        lo = md
    else:
        hi = md
zero = (lo + hi) / 2
check('lasso forecast positive on [0, 0.8)', all(forecast(a)[0] > 0 for a in np.arange(0.01, 0.8, 0.01)))
f10, m10 = forecast(1.0)
check('lasso coef at 1.0', np.allclose(m10.coef_, [1.0, -0.2, 0.0], atol=1e-8))
numeric('lasso p1', P[0], F(str(round(f_ols, 9))),
        {'no-intercept': F(12, 10), 'sign': F(2, 10) - 1 - F(12, 10) + 1})
numeric('lasso p2', P[1], F(str(round(f02, 9))),
        {'down': F(2, 10) + F(18, 10) * F(-1, 2) + F(-14, 10) * -1 + F(3, 10) * 2,
         'count': F(14, 10) - 3 * F(2, 10), 'intercept': F(9, 10) - F(2, 10)})
numeric('lasso p3', P[2], F(str(round(zero, 9))),
        {'straight': F(14, 10) / F(25, 10), 'no-intercept': F(12, 10) / F(25, 10), 'demand': F(1, 2)})
numeric('lasso p4', P[3], F(str(round(f10, 9))),
        {'straight': F(14, 10) - F(25, 10), 'slope': -F(25, 10) * F(2, 10),
         'ols': F(14, 10), 'sign': F(1, 10)})
check('lasso slope first stretch', close((f02 - f_ols) / 0.2, -2.5, 1e-7))
check('lasso slope second stretch', close((f10 - forecast(0.8)[0]) / 0.2, -0.5, 1e-7))
check('lasso wind still in at 1.0', abs(m10.coef_[1]) > 0.1)
has('lasso p3', P[2], '0.15', '0.4 - 0.5\\alpha')
has('lasso p2', P[1], '2.5 per unit')

# --------------------------------------------------------------------------
# stat-learning/problems-2 p-built-ridge: data built to the stated sums
# --------------------------------------------------------------------------
it = load('stat-learning', 'problems-2.json', 'p-built-ridge')
P = it['parts']
G = np.array([[50.0, 40.0], [40.0, 50.0]])
rng = np.random.default_rng(3)
Z = rng.standard_normal((50, 2))
Z -= Z.mean(axis=0)
Qm, _ = np.linalg.qr(Z)
Xr = Qm @ np.linalg.cholesky(G).T
check('ridge built sums', np.allclose(Xr.T @ Xr, G) and np.allclose(Xr.mean(axis=0), 0))
check('ridge z-scored', np.allclose((Xr ** 2).mean(axis=0), 1))
yr = Xr @ np.array([2.0, -1.0])
check('ridge built Xy', np.allclose(Xr.T @ yr, [60, 30]))
ols = LinearRegression(fit_intercept=False).fit(Xr, yr).coef_
rdg = Ridge(alpha=10, fit_intercept=False).fit(Xr, yr).coef_
check('ridge ols', np.allclose(ols, [2.0, -1.0]))
check('ridge coef', np.allclose(rdg, [1.2, -0.3]))
Xt = np.array([[2, 1], [1, 2], [-2, -1], [1, -1]], dtype=float)
yt = np.array([2.0, 1.0, -1.6, 2.5])


def mse(b):
    return float(((yt - Xt @ np.asarray(b)) ** 2).mean())


base = float((yt ** 2).mean())
short = np.array([2.0, -1.0]) * 50 / 60
all4 = np.linalg.solve(G + 10, [60, 30])
numeric('ridge p1', P[0], F(str(round(float(ols[1]), 9))), {'alone': F(30, 50), 'swap': 2, 'sign': 1})
numeric('ridge p2', P[1], F(str(round(float(rdg[1]), 9))),
        {'factor': F(-50, 60), 'all-entries': F(str(round(float(all4[1]), 9))), 'ols': -1, 'sign': F(3, 10)})
numeric('ridge p3', P[2], F(str(round(mse(rdg), 9))),
        {'ols': F(str(round(mse(ols), 9))), 'sse': F(str(round(mse(rdg) * 4, 9))),
         'carried': F(str(round(mse([1.667, -0.833]), 4)))}, 3)
r2 = 1 - mse(rdg) / base
numeric('ridge p4', P[3], F(str(round(r2, 9))),
        {'ratio': F(str(round(mse(rdg) / base, 9))),
         'test-mean': F(str(round(1 - mse(rdg) / float(((yt - yt.mean()) ** 2).mean()), 9))),
         'carried': F(str(round(1 - 0.515 / base, 9))),
         'ols': F(str(round(1 - mse(ols) / base, 9)))}, 3)
check('ridge base', close(base, 3.4525))
check('ridge ols mse', close(mse(ols), 1.0525))
check('ridge exact shortcut carried', abs(mse(short) - 0.515) < 0.0012)
miss_r, miss_o = np.abs(yt - Xt @ rdg), np.abs(yt - Xt @ ols)
check('ridge closer on three hours', int((miss_r < miss_o).sum()) == 3)
check('ridge about a third', 0.3 < mse(rdg) / mse(ols) < 0.37)
ev, evec = np.linalg.eigh(G)
check('ridge halves the difference part', close(ev[0] / (ev[0] + 10), 0.5) and close(ev[1] / (ev[1] + 10), 0.9))
check('ridge test mean', close(yt.mean(), 0.975))
has('ridge p3', P[2], '2.1, 0.6, $-2.1$ and 1.5', '1.42', '1.0525')
has('ridge p4', P[3], '3.4525', '89.7%', '69.5%', '0.975')

# --------------------------------------------------------------------------
# stat-learning/problems-4 p-renewals part 2
# --------------------------------------------------------------------------
it = load('stat-learning', 'problems-4.json', 'p-renewals')
part = it['parts'][1]
choice('renew p2', part, 'logistic')
import re
qn = part['question']
m = re.search(r'fitted on (\d+) rows, with the other (\d+) kept', qn)
fit_n, val_n = int(m.group(1)), int(m.group(2))
check('renew split', fit_n + val_n == 400)
nums = [float(v) for v in re.findall(r'0\.\d+', qn)]
check('renew six scores', len(nums) == 6, str(nums))
net_f, net_v, log_f, log_v, svm_f, svm_v = nums
check('renew validation order', log_v > svm_v > net_v)
check('renew fitting order', net_f > svm_f > log_f)
check('renew gaps', close(net_f - net_v, 0.21) and close(log_f - log_v, 0.02))
params = 6 * 16 + 16 + 16 + 1
check('renew params', params == 129 and 6 + 1 == 7)
t2 = text_of(part)
rows_each = fit_n / params
m2 = re.search(r'about (\d\.\d) rows each', t2)
check('renew rows each', m2 is not None and close(float(m2.group(1)), round(rows_each, 1), 1e-9),
      'printed %s, mine %.2f' % (m2.group(1) if m2 else None, rows_each))
check('renew about 3 rows', round(400 / params) == 3)


def attainable(score, rows):
    """A hit rate printed to 2 places is some count over the rows, rounded."""
    return any(abs(round(k / rows + 1e-12, 2) - score) < 1e-9 for k in range(rows + 1))


for nm, s in (('network', net_f), ('logistic', log_f), ('svm', svm_f)):
    check('renew %s fitting score possible on %d rows' % (nm, fit_n), attainable(s, fit_n))
vals = {'network': net_v, 'logistic': log_v, 'svm': svm_v}
for nm, s in vals.items():
    check('renew %s validation score possible on %d rows' % (nm, val_n), attainable(s, val_n),
          '%.2f x %d = %.1f rows; hit rates on %d rows step by %.4f'
          % (s, val_n, s * val_n, val_n, 1 / val_n))
counts = {nm: [k for k in range(val_n + 1) if abs(round(k / val_n + 1e-12, 2) - s) < 1e-9]
          for nm, s in vals.items()}
check('renew validation scores possible together', all(counts.values()), str(counts))

# --------------------------------------------------------------------------
# validation/problems-1 p-arrears-grid parts 2 (line), 4, 5
# --------------------------------------------------------------------------
from sklearn.model_selection import KFold

it = load('validation', 'problems-1.json', 'p-arrears-grid')
P = it['parts']
ROWS = 640


def curve(nn):
    return F(33, 100) + F(40, nn)


def fits(k_outer, k_inner=6, grid=18):
    """Count the fits by walking the loops, refits included."""
    count = 0
    idx = np.arange(ROWS)
    for tr, _ in KFold(k_outer, shuffle=True, random_state=0).split(idx):
        for _tr, _te in KFold(k_inner, shuffle=True, random_state=0).split(tr):
            count += grid
        count += 1
    return count


check('grid p1 count', 6 * 18 + 1 == 109)
check('grid p2 count', fits(4) == 436 == P[1]['widget']['answer'])
check('grid p2 line', '432 counts only the inner fits' in P[1]['feedback']['byKey']['no-refits']
      and 4 * 6 * 18 == 432 and 432 + 4 == 436)
check('grid p2 old line gone', 'You left out the 4 refits' not in json.dumps(it))
outer4 = {len(tr) for tr, _ in KFold(4).split(np.arange(ROWS))}
check('grid outer size', outer4 == {480})
inner = {len(tr) for tr, _ in KFold(6).split(np.arange(480))}
check('grid inner size', inner == {400})
over = curve(480) - curve(640)
check('grid p4 exact', over == F(1, 48))
numeric('grid p4', P[3], over,
        {'inner': curve(400) - curve(640), 'inner-outer': curve(400) - curve(480),
         'carried': curve(F(5, 6) * 640) - curve(640), 'level': curve(480)}, 4)
check('grid p4 takes 0.0208', abs(0.0208 - P[3]['widget']['answer']) <= P[3]['widget']['tol']['abs'])
check('grid p4 takes 0.0209 not', True)
# smallest K by brute force over real KFold training sizes (the largest
# overstatement of a fold is the one with the fewest training rows)
best = None
for K in range(2, 41):
    sizes = [len(tr) for tr, _ in KFold(K).split(np.arange(ROWS))]
    worst = max(curve(s) - curve(ROWS) for s in sizes)
    mean_over = sum(curve(s) - curve(ROWS) for s in sizes) / K
    if K in (4, 9, 10):
        check('grid formula near at K=%d' % K, abs(mean_over - F(625, 10000) / (K - 1)) < F(1, 20000))
    if best is None and worst <= F(7, 1000):
        best = K
check('grid smallest K', best == 10)
check('grid K=9 misses', F(625, 10000) / 8 > F(7, 1000))
check('grid K=10 meets', F(625, 10000) / 9 <= F(7, 1000))
numeric('grid p5', P[4], fits(10), {'nine-folds': fits(9), 'no-refits': 10 * 108, 'added': 10 + 109})
check('grid 576', {len(tr) for tr, _ in KFold(10).split(np.arange(ROWS))} == {576})
check('grid inner folds whole at K=10', 576 % 6 == 0)
has('grid p5', P[4], '0.0078', '0.0069', '576', '436')
has('grid p4', P[3], '0.0833', '0.0625', '0.4133', '1/48', '533')
old = json.dumps(it)
for gone in ('0.412', '0.451', '8.6%'):
    check('grid old %s gone' % gone, gone not in old)

print('delta review-delta-af-1: %d checks, %d findings' % (checks, findings))
sys.exit(0)
