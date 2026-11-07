"""Recompute every number in the puzzles level 4 performance task (hw4-kelly-draw).
Run from the repo root: python3 docs/reports/puzzles-4-perf-numbers.py  (exits 0 when all checks pass)
Route A: exact fractions and floats from math. Route B: sympy (symbolic optimum, high-precision logs)
and a seeded numpy simulation of log growth. Without sympy or numpy their checks are skipped and reported.
"""
import json, math, os, sys, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'puzzles')
fails, n_checks, skipped = [], 0, []
def check(ok, msg):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(msg)
def r4(x):
    return round(x + 0.0, 4)

hw = json.load(open(os.path.join(COURSE, 'homework-4.json')))
items = {it['id']: it for it in hw['items']}
it = items['hw4-kelly-draw']
model, prompt = it['model'], it['prompt']

# 0. Shape: one task per level, homework limits, rubric.
check(len(hw['items']) <= 12 and len(hw['items']) >= 6, 'homework item count outside 6 to 12')
check(sum(1 for i in hw['items'] if i.get('performance')) == 1, 'not exactly one performance item in homework-4')
rev = json.load(open(os.path.join(COURSE, 'review-4.json')))
check(not any(i.get('performance') for i in rev['items']), 'review-4 also has a performance item')
check(it['performance'] == 'derivation' and it['kind'] == 'longform', 'kind wrong')
for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts'):
    check(k not in it, 'forbidden field ' + k)
rub = it['rubric']
check(3 <= len(rub) <= 5, 'rubric rows not 3 to 5')
check(sum(r['points'] for r in rub) == 10, 'rubric does not sum to 10')
check(sum(1 for r in rub if r.get('required') is True) == 1, 'not exactly one required row')
check(any(i.get('difficulty') == 5 for i in hw['items']), 'no difficulty 5 item')
check('$' not in it['title'], 'maths in title')

# 1. The setting: 6 to 5 is b = 1.2, a win pays £1.20 per £1, chances sum to 1.
b, p, r, q = F(6, 5), F(45, 100), F(25, 100), F(30, 100)
check(b == F(12, 10) and float(b) == 1.2, '6 to 5 is not 1.2')
check(p + r + q == 1, 'chances do not sum to 1')
check(p * b > q, 'bet not favourable')
for s in ('6 to 5', '£1.20', '0.45', '0.25', '0.30'):
    check(s in prompt, 'prompt lacks ' + s)

# 2. Kelly fraction, exact (route A) and by maximising g on a fine grid (route A2).
num, den = p * b - q, b * (p + q)
check(num == F(24, 100) and p * b == F(54, 100), 'pb - q != 0.54 - 0.30 = 0.24')
check(den == F(9, 10) and p + q == F(75, 100), 'b(p+q) != 1.2 x 0.75 = 0.9')
fstar = num / den
check(fstar == F(4, 15), 'f* != 4/15')
check(r4(float(fstar)) == 0.2667, 'f* not 0.2667 to 4 dp')
def g(f, p=float(p), q=float(q), b=float(b)):
    return p * math.log(1 + b * f) + q * math.log(1 - f)
grid = [i / 100000 for i in range(0, 99999)]
fgrid = max(grid, key=g)
check(abs(fgrid - float(fstar)) < 2e-5, 'grid argmax %.5f differs from 4/15' % fgrid)
# with no draw the formula is p - q/b; the conditional bet has the same peak
pc, qc = p / (p + q), q / (p + q)
check(pc - qc / b == fstar, 'conditional b-to-1 rule differs from f*')
check(all(abs(g(f) - float(p + q) * g(f, float(pc), float(qc))) < 1e-12 for f in (0.1, 0.3, 0.5)), 'g != (p+q) h')
check(fstar > 0 and fstar < 1 and num < p * b + q * b, 'f* not in (0,1)')

# 3. Multipliers and growth at f*.
check(1 + b * fstar == F(132, 100) and 1 - fstar == F(11, 15), 'multipliers at f* wrong')
t1, t2 = float(p) * math.log(1.32), float(q) * math.log(F(11, 15))
check(r4(t1) == 0.1249 and r4(-t2) == 0.0930, 'growth terms not 0.1249 and 0.0930')
gstar = g(float(fstar))
check(r4(gstar) == 0.0319 and abs((r4(t1) + r4(t2)) - 0.0319) < 1e-9, 'g(f*) not 0.0319')

# 4. Slips named in the model.
check(r4(float(p - (1 - p) / b)) == -0.0083, 'draw-as-loss slip not -0.0083')
check(p - q / b == F(1, 5), 'p - q/b not 0.2')
check(p + q != 1, 'p + q is 1, slip remark wrong')

# 5. Twice Kelly.
f2 = 2 * fstar
check(f2 == F(8, 15) and r4(float(f2)) == 0.5333, '2f* not 8/15 = 0.5333')
check(1 + b * f2 == F(164, 100) and 1 - f2 == F(7, 15), 'multipliers at 2f* wrong')
u1, u2 = float(p) * math.log(1.64), float(q) * math.log(F(7, 15))
check(r4(u1) == 0.2226 and r4(-u2) == 0.2286, 'terms at 2f* not 0.2226 and 0.2286')
g2 = g(float(f2))
check(r4(g2) == -0.0060 and abs((r4(u1) + r4(u2)) + 0.0060) < 1e-9, 'g(2f*) not -0.0060')
check(1 + f2 * num == F(1128, 1000), 'mean multiplier at 2f* not 1.128')
# exact zero of g by bisection (route A) on (f*, 1)
lo, hi = float(fstar), 0.999
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
f0 = lo
check(round(f0, 3) == 0.513 and f0 < float(f2), 'zero of g not 0.513 below 2f*')
# quadratic approximation: parabola through 0, back at 0 at twice its peak
A, B = float(num), float(p * b * b + q)
peak = A / B
check(abs((A * 2 * peak - 0.5 * B * (2 * peak) ** 2)) < 1e-12, 'parabola not zero at twice its peak')
# long shot: sign at 2f* can differ (p = 0.1 at 20 to 1)
pl, bl = 0.1, 20.0
fl = pl - (1 - pl) / bl
check(fl > 0 and g(2 * fl, pl, 1 - pl, bl) > 0, 'long-shot example does not stay positive at 2f*')
check(abs(fl - 0.055) < 1e-12 and r4(g(2 * fl, pl, 1 - pl, bl)) == 0.0114, 'long-shot g(2f*) not 0.0114')
check(r4(0.1 * math.log(1 + 20 * 0.11) + 0.9 * math.log(0.89)) == 0.0114, 'long-shot g(0.11) by hand not 0.0114')
check('g(2f^*) \\approx 0.0114 > 0' in model and '20 to 1 with $p = 0.1$' in model, 'model lacks long-shot figures')
check('h(f) = \\tfrac{p}{p + q}' in model, 'model lacks h(f)')

# 6. Every model figure is printed in the model.
for s in ('0.54 - 0.30 = 0.24', '1.2 \\times 0.75 = 0.9', '0.24 / 0.9', '\\tfrac{4}{15} \\approx 0.2667', '1.32',
          '\\tfrac{11}{15}', '0.1249 - 0.0930 = 0.0319', '-0.0083', '= 0.2', '\\tfrac{8}{15} \\approx 0.5333', '1.64',
          '\\tfrac{7}{15}', '0.2226 - 0.2286 = -0.0060', '1.128', '0.513'):
    check(s in model, 'model lacks ' + s)
rtext = ' '.join(x['text'] for x in rub)
for s in ('0.2667', '0.0319', '0.5333', '-0.0060'):
    check(s in rtext, 'rubric lacks ' + s)

# 7. Route B: sympy, symbolic optimum and second derivative, high-precision logs.
try:
    import sympy as sp
    P, Q, Bs, f = sp.symbols('p q b f', positive=True)
    G = P * sp.log(1 + Bs * f) + Q * sp.log(1 - f)
    G1 = sp.diff(G, f)
    check(sp.simplify(G1 - (P * Bs / (1 + Bs * f) - Q / (1 - f))) == 0, "g' differs")
    sol = sp.solve(sp.Eq(G1, 0), f)
    check(len(sol) == 1 and sp.simplify(sol[0] - (P * Bs - Q) / (Bs * (P + Q))) == 0, 'symbolic f* differs')
    G2 = sp.diff(G, f, 2)
    check(sp.simplify(G2 - (-P * Bs**2 / (1 + Bs * f)**2 - Q / (1 - f)**2)) == 0, "g'' differs")
    check(sp.simplify(G1.subs(f, 0) - (P * Bs - Q)) == 0, "g'(0) != pb - q")
    sub = {P: sp.Rational(45, 100), Q: sp.Rational(30, 100), Bs: sp.Rational(6, 5)}
    check(sol[0].subs(sub) == sp.Rational(4, 15), 'sympy f* != 4/15')
    check(all(G2.subs(sub).subs(f, sp.Rational(k, 100)) < 0 for k in range(0, 100)), "g'' not negative on grid")
    check(abs(sp.N(G.subs(sub).subs(f, sp.Rational(4, 15)), 30) - sp.Float('0.031887802978', 30)) < 1e-11, 'sympy g(f*)')
    check(round(float(sp.N(G.subs(sub).subs(f, sp.Rational(8, 15)), 30)), 4) == -0.0060, 'sympy g(2f*)')
    z = sp.nsolve(G.subs(sub), f, 0.5)
    check(abs(float(z) - f0) < 1e-9, 'sympy zero differs from bisection')
    # quadratic approximation of g from the series
    ser = sp.series(G, f, 0, 3).removeO()
    check(sp.simplify(ser - ((P * Bs - Q) * f - sp.Rational(1, 2) * (P * Bs**2 + Q) * f**2)) == 0, 'series differs')
except ImportError:
    skipped.append('sympy')

# 8. Route B: seeded simulation of log growth.
try:
    import numpy as np
    rng = np.random.default_rng(20261107)
    paths, bets = 4000, 1000
    u = rng.random((paths, bets))
    win, loss = u < 0.45, u >= 0.70
    nw, nl = win.sum(axis=1), loss.sum(axis=1)
    def sim(fv):
        return (nw * np.log(1 + 1.2 * fv) + nl * np.log(1 - fv)) / bets   # growth per bet on each path
    fs = np.linspace(0.0, 0.9, 901)
    means = np.array([sim(fv).mean() for fv in fs])
    fbest = fs[means.argmax()]
    check(abs(fbest - 4 / 15) <= 0.005, 'simulated argmax %.3f far from 4/15' % fbest)
    s1, s2 = sim(4 / 15), sim(8 / 15)
    se1, se2 = s1.std() / np.sqrt(paths), s2.std() / np.sqrt(paths)
    check(abs(s1.mean() - gstar) < 4 * se1, 'simulated g(f*) %.5f vs %.5f' % (s1.mean(), gstar))
    check(abs(s2.mean() - g2) < 4 * se2 and s2.mean() + 4 * se2 < 0, 'simulated g(2f*) not negative')
    check(np.median(s2) < 0 and np.median(s1) > 0, 'median path growth signs wrong')
    # per-match mean multiplier at 2f*, from the same draws
    mult = np.where(win, 1 + 1.2 * 8 / 15, np.where(loss, 7 / 15, 1.0))
    check(abs(mult.mean() - 1.128) < 4 * mult.std() / np.sqrt(mult.size), 'simulated mean multiplier not 1.128')
    # a sequential path simulation of wealth (not the count shortcut) agrees
    lw = np.zeros(paths)
    for j in range(bets):
        lw += np.log(np.where(win[:, j], 1 + 1.2 * 4 / 15, np.where(loss[:, j], 11 / 15, 1.0)))
    check(np.allclose(lw / bets, s1), 'sequential path log-wealth differs from count shortcut')
except ImportError:
    skipped.append('numpy')

print('%d checks, %d failed%s' % (n_checks, len(fails), (', skipped: ' + ', '.join(skipped)) if skipped else ''))
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
