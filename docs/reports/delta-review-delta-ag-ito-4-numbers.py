#!/usr/bin/env python3
"""Delta read review-delta-ag-ito-4: ito/problems-4.json after the re-author and fix pass.

Scope: p-band-wait (all five parts), and the text fixes on p-two-date-product
part 2 and p-dividend-hedge (stem, parts 3 and 4). Imports no earlier script.

Routes for p-band-wait (X = 30 + 2W, exit at 0 or 50), none of them the author's
chain of stopped martingales:
  A. cubic solutions of the boundary-value problems (1/2)s^2 u'' = -g, checked by
     substitution in sympy, in exact fractions;
  B. the absorbing random walk on whole pips with time step 1/4 minute, solved as
     a linear system (its exit law and exit times equal the continuous ones);
  C. the Laplace transform sinh(xk)/sinh(Lk) of the exit time at each edge,
     differentiated at 0 by a series;
  D. a simulation of the walk, fixed seed, wide tolerance: prints a NOTE, never fails.

Exits 0 always. A failing check prints a FINDING line. A finding of the review
prints FINDING while the content is as the review describes, `resolved` after.
"""
import json
import math
import os
from fractions import Fraction as F

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito', 'problems-4.json')
SET = os.environ.get('DELTA_SET', SET)      # a scratch copy, when a fix is tried
data = json.load(open(SET, encoding='utf-8'))
items = {it['id']: it for it in data['items']}

n_checks = 0
n_fail = 0


def check(name, ok, detail=''):
    global n_checks, n_fail
    n_checks += 1
    if not ok:
        n_fail += 1
        print('FINDING check failed: %s %s' % (name, detail))


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def takes(widget, v):
    return abs(float(v) - widget['answer']) <= widget['tol']['abs'] + 1e-12


def wrong_hit(widget, v):
    return [w['id'] for w in widget.get('wrong', [])
            if abs(float(v) - w['value']) <= w['tol']['abs'] + 1e-12]


# ---------------------------------------------------------------- p-band-wait
x0, L, sig = 30, 50, 2
s2 = sig * sig

# Route A: boundary-value problems, exact.
x = sp.symbols('x')
h = x / L                                   # chance of the top: (1/2)s2 h'' = 0
u_tau = x * (L - x) / s2                    # (1/2)s2 u'' = -1
w_top = x * (L**2 - x**2) / (3 * s2 * L)    # (1/2)s2 w'' = -h
w_bot = sp.expand((L - x) * (L**2 - (L - x)**2) / (3 * s2 * L))  # (1/2)s2 w'' = -(1-h)
v_int = x * (L**2 - x**2) / (3 * s2)        # (1/2)s2 v'' = -x  : E int_0^tau X dt
for nm, fn, rhs in (('h', h, 0), ('u_tau', u_tau, -1), ('w_top', w_top, -h),
                    ('w_bot', w_bot, -(1 - h)), ('v_int', v_int, -x)):
    check('A ode ' + nm, sp.simplify(sp.Rational(s2, 2) * sp.diff(fn, x, 2) - rhs) == 0)
    check('A bc ' + nm, fn.subs(x, 0) == 0 and (fn.subs(x, L) == (1 if nm == 'h' else 0)))
P = F(x0, L)
Etau = F(x0 * (L - x0), s2)
A = F(x0 * (L**2 - x0**2), 3 * s2 * L)
B = F((L - x0) * (L**2 - (L - x0)**2), 3 * s2 * L)
Eint = F(x0 * (L**2 - x0**2), 3 * s2)
EX3 = P * L**3
# d(X^3) = 3X^2 dX + 3X (dX)^2, (dX)^2 = 4 dt: X^3 - 12 int X dt is a martingale.
c = 3 * s2
EtauX_from_int = Eint                        # tX - int X dt is a martingale
check('A E[X^3] by the integral identity', EX3 == x0**3 + c * Eint, str(EX3))
check('A A + B = E[tau]', A + B == Etau)
check('A E[tau X_tau] = 50 A', L * A == EtauX_from_int)
top = A / P
bot = B / (1 - P)
check('A P = 3/5', P == F(3, 5))
check('A E[tau] = 150', Etau == 150)
check('A E[X^3] = 75000', EX3 == 75000)
check('A E[tau X] = 4000', EtauX_from_int == 4000)
check('A A = 80', A == 80)
check('A top = 400/3', top == F(400, 3))
check('A floor = 175', bot == 175)
check('A closed form (L^2 - x^2)/(3 s2)', F(L**2 - x0**2, 3 * s2) == top)
check('A closed form x(2L - x)/(3 s2)', F(x0 * (2 * L - x0), 3 * s2) == bot)

# Route B: random walk on pips, dt = 1/s2 minutes a step. Linear systems.
dt = 1.0 / s2
n = L - 1
T = np.zeros((n, n))
for i in range(n):
    if i > 0:
        T[i, i - 1] = 0.5
    if i < n - 1:
        T[i, i + 1] = 0.5
I = np.eye(n)
lev = np.arange(1, L, dtype=float)
e_top = np.zeros(n)
e_top[-1] = 0.5
hB = np.linalg.solve(I - T, e_top)
tauB = np.linalg.solve(I - T, np.full(n, dt))
wB = np.linalg.solve(I - T, dt * hB)
vB = np.linalg.solve(I - T, dt * lev)
k = x0 - 1
check('B P', close(hB[k], 0.6, 1e-9))
check('B E[tau]', close(tauB[k], 150, 1e-7))
check('B A', close(wB[k], 80, 1e-7))
check('B E int X', close(vB[k], 4000, 1e-5))
check('B E[X^3]', close(hB[k] * L**3, 75000, 1e-4))
check('B top', close(wB[k] / hB[k], 400 / 3, 1e-7))
check('B floor', close((tauB[k] - wB[k]) / (1 - hB[k]), 175, 1e-7))
# the walk's cube gains 3 X_k a step, that is 12 X_k dt: the same c
check('B c = 12', close(((x0 + 1)**3 + (x0 - 1)**3) / 2 - x0**3, 12 * x0 * dt))

# Route C: Laplace transform of the exit time on each edge.
lam = sp.symbols('lam', positive=True)
kk = sp.sqrt(2 * lam) / sig
top_lt = sp.sinh(x0 * kk) / sp.sinh(L * kk)
bot_lt = sp.sinh((L - x0) * kk) / sp.sinh(L * kk)
ser_t = sp.series(top_lt, lam, 0, 2).removeO()
ser_b = sp.series(bot_lt, lam, 0, 2).removeO()
check('C P', sp.nsimplify(ser_t.coeff(lam, 0)) == sp.Rational(3, 5))
check('C A', sp.nsimplify(-ser_t.coeff(lam, 1)) == 80)
check('C B', sp.nsimplify(-ser_b.coeff(lam, 1)) == 70)

# Route D: simulation, fixed seed. A NOTE only.
rng = np.random.default_rng(20261117)
N = 20000
pos = np.full(N, x0)
steps = np.zeros(N)
alive = np.ones(N, dtype=bool)
guard = 0
while alive.any() and guard < 200000:
    idx = np.nonzero(alive)[0]
    pos[idx] += rng.choice((-1, 1), size=idx.size)
    steps[idx] += 1
    alive[idx] = (pos[idx] > 0) & (pos[idx] < L)
    guard += 1
tm = steps * dt
hit_top = pos == L
sim = (hit_top.mean(), tm.mean(), tm[hit_top].mean(), tm[~hit_top].mean(),
       (tm * pos).mean(), (pos.astype(float)**3).mean())
exact = (0.6, 150, 400 / 3, 175, 4000, 75000)
names = ('P', 'E[tau]', 'E[tau|top]', 'E[tau|floor]', 'E[tau X]', 'E[X^3]')
for nm, sv, ev in zip(names, sim, exact):
    flag = 'agrees' if abs(sv - ev) <= 0.05 * ev else 'outside 5%, read by eye'
    print('NOTE simulation %s: %.4f against %.4f (%s)' % (nm, sv, ev, flag))

# Keys, bands and slips, from the JSON.
pb = items['p-band-wait']
parts = pb['parts']
keys = [EX3, EtauX_from_int, A, top, bot]
typed = [['75000'], ['4000'], ['80'], ['133.33'], ['175']]
for i, (kv, ty) in enumerate(zip(keys, typed)):
    wd = parts[i]['widget']
    check('key part %d' % (i + 1), abs(float(kv) - wd['answer']) < 1e-5, str(wd['answer']))
    for t in ty:
        check('typed part %d %s' % (i + 1, t), takes(wd, t) and not wrong_hit(wd, t))
check('part 4 refuses 133.3', not takes(parts[3]['widget'], '133.3'))
check('part 4 refuses 133.34', not takes(parts[3]['widget'], '133.34'))

slips = [
    {'start-cube': x0**3, 'swapped': (1 - P) * L**3, 'sure-top': L**3},
    {'no-half': F(EX3 - x0**3, 6 * s2), 'sigma-unsquared': F(EX3 - x0**3, 3 * sig),
     'no-start': F(EX3, c), 'unit-c': F(EX3 - x0**3, 3)},
    {'squared-level': F(4000, L * L), 'no-divide': 4000},
    {'times-p': A * P, 'joint': A, 'swapped': A / (1 - P)},
    {'wrong-weight': (Etau - top) / (1 - P), 'no-condition': Etau - A,
     'top-chance': (Etau - A) / P},
]
forms = [0, 0, 0, 2, 0]   # asked places
for i, sl in enumerate(slips):
    wd = parts[i]['widget']
    got = {w['id']: w for w in wd['wrong']}
    check('slip ids part %d' % (i + 1), set(got) == set(sl), str(sorted(got)))
    for sid, val in sl.items():
        if sid not in got:
            continue
        w = got[sid]
        check('slip %d %s value' % (i + 1, sid), abs(float(val) - w['value']) < 1e-5,
              '%s against %s' % (float(val), w['value']))
        typed_v = round(float(val), forms[i])
        check('slip %d %s typed %s routed' % (i + 1, sid, typed_v),
              wrong_hit(wd, typed_v) == [sid] and not takes(wd, typed_v))
        check('slip %d %s has a line' % (i + 1, sid), sid in parts[i]['feedback']['byKey'])
        # no rounding tie at the asked places
        scaled = float(val) * 10**forms[i]
        check('slip %d %s off a tie' % (i + 1, sid), abs(scaled - math.floor(scaled) - 0.5) > 1e-6)
    bands = [(wd['answer'] - wd['tol']['abs'], wd['answer'] + wd['tol']['abs'])] + \
            [(w['value'] - w['tol']['abs'], w['value'] + w['tol']['abs']) for w in wd['wrong']]
    for a in range(len(bands)):
        for b in range(a + 1, len(bands)):
            check('bands apart part %d' % (i + 1),
                  bands[a][1] < bands[b][0] or bands[b][1] < bands[a][0])
    for w in wd['wrong']:
        check('slip band not wider than value', 2 * w['tol']['abs'] <= abs(w['value']))
# a learner who carries 133.33 into the wrong-weight slip
check('wrong-weight from 133.33', wrong_hit(parts[4]['widget'], round((150 - 133.33) / 0.4, 0)) == ['wrong-weight'])
for i, f_ in enumerate(forms):
    q = parts[i]['question']
    check('form stated part %d' % (i + 1),
          ('whole number' in q) if f_ == 0 else ('2 decimal places' in q))

# Printed numbers and claims of p-band-wait.
blob = json.dumps(pb, ensure_ascii=False)
for s in ('2{,}500X_\\\\tau', '75{,}000', '30/50 = 0.6', '125{,}000', '12X_t', '30^3 = 27{,}000',
          '48{,}000/12', '4{,}000 = 50A', '80/0.6', '1{,}600/12', '150 - 80 = 70',
          '70/0.4 = 175', 'c = 24', 'c = 6', 'c = 3'):
    check('printed ' + s, s in blob)
check('X^3 = 2500 X on the edges', all(v**3 == 2500 * v for v in (0, 50)))
check('48000/12', F(75000 - 27000, 12) == 4000)
check('1600/12 = top', F(1600, 12) == top)
check('drift of X^3 positive in the band', 12 * 1 > 0)
check('starts nearer the top', L - x0 < x0)
check('far edge slower', bot > top and bot > Etau > top)
check('c slips', (6 * s2, 3 * sig, 3) == (24, 6, 3))
# optional stopping: |M at t^tau| <= 50^3 + 12*50*tau, of finite mean 125000 + 600*150
check('dominating bound finite', L**3 + c * L * Etau == 215000)

# ------------------------------------------------- p-two-date-product part 2
tp = items['p-two-date-product']['parts'][1]
v1 = 0.3**2
check('two-date 0.09', close(v1, 0.09))
check('two-date key', close(v1 * (1 + 2 + 2), tp['widget']['answer']))
check('two-date no-cov', close(v1 * 3, 0.27) and close(0.27 + 2 * 0.09, 0.45))
# another route: the covariance matrix of (W_1, W_2) and the vector (1, 1)
cov = np.array([[1.0, 1.0], [1.0, 2.0]]) * v1
check('two-date by the matrix', close(np.ones(2) @ cov @ np.ones(2), 0.45))
check('two-date generic as given', tp['feedback']['generic'] ==
      'Not quite. One year of $\\sigma^2$ is 0.09. Count the years in $\\text{Var}(X) + \\text{Var}(Y) + 2\\,\\text{Cov}(X, Y)$: one, two and twice one.')
check('two-date no-cov as given', tp['feedback']['byKey']['no-cov'] ==
      'That is 0.27, the answer for independent logs. Year 1 sits in both logs and adds $2 \\times 0.09$.')
check('two-date 0.27 is the no-cov slip',
      [w['value'] for w in tp['widget']['wrong'] if w['id'] == 'no-cov'] == [0.27])

# ------------------------------------------------------------ p-dividend-hedge
dv = items['p-dividend-hedge']
r, q, S, Tm = 0.045, 0.02, 120.0, 0.75
V = lambda rem: S * math.exp(-q * rem)
Vt_fd = (V(Tm - 1e-6) - V(Tm + 1e-6)) / 2e-6       # t up means time left down
check('dividend V', close(V(Tm), 118.2134, 5e-5))
check('dividend V_t by a difference', close(Vt_fd, dv['parts'][2]['widget']['answer'], 1e-6))
check('dividend V_t > 0 (gains with time)', Vt_fd > 0)
check('dividend equation', close(Vt_fd + (r - q) * V(Tm) - r * V(Tm), 0, 1e-6))
Kf = V(Tm) / math.exp(-r * Tm)
check('dividend K', close(Kf, dv['parts'][3]['widget']['answer'], 1e-5) and round(Kf, 2) == 122.27)
check('dividend K = S e^{(r-q)T}', close(Kf, S * math.exp((r - q) * Tm)))
check('dividend prose as given', dv['prose'] ==
      'A share pays its holder a steady dividend: over each $dt$, $\\Delta$ shares pay cash $q\\Delta S\\,dt$. The rate $q$ is the dividend yield. The claim $V(t, S)$ receives no dividends. The share follows $dS = \\mu S\\,dt + \\sigma S\\,dW$, and cash earns $r$. A desk sells one claim and holds $\\Delta = V_S$ shares.')
check('dividend part 3 question as given',
      'A claim delivers one share at $T$, and its holder receives none of the dividends paid before then. Its value is $V = Se^{-q(T - t)}$, so $V_S = e^{-q(T - t)}$ and $V_{SS} = 0$.' in dv['parts'][2]['question'])
check('dividend plus as given', dv['parts'][2]['feedback']['byKey']['plus'] ==
      'That uses $r + q$ in the equation, which flips the sign. The claim gains value with time, as fewer dividends are left to miss.')
check('dividend part 4 explain as given', dv['parts'][3]['explain']['text'] ==
      'The forward is worth $Se^{-qT} - Ke^{-rT}$, so $K = Se^{(r - q)T}$. The growth rate $r - q$ is the bracket of part 2. Here $K = 120e^{0.025 \\times 0.75} \\approx 122.27$.')
check('no dividend dates left', 'dividend dates' not in json.dumps(dv))
check('no Q drift r - q left', 'Under $Q$ the share grows' not in json.dumps(dv, ensure_ascii=False))

# ------------------------------------------------------- findings of the review
def finding(n, cls, open_, text):
    print('%s %d (%s): %s' % ('FINDING' if open_ else 'resolved', n, cls, text))


finding(1, 'reuse', '(12 - c)x' in parts[1]['explain']['text']
        or 'halves the second derivative' in parts[1]['feedback']['byKey']['no-half'],
        'p-band-wait part 2 explain and no-half retell l13 screen 0 with sigma^2 folded in')
finding(2, 'misleading', 'the stopped process keeps its starting value' in parts[1]['question'],
        'p-band-wait part 2: the mean, not the process, keeps the starting value')
finding(3, 'continuity', 'As a check, $(50^2 - 30^2)/12' in parts[3]['explain']['text'],
        'p-band-wait part 4 explain uses a closed form it does not name')

print('%d checks, %d failed' % (n_checks, n_fail))
