"""Concept checks for measure-prob level 3 (lessons l9 to l13, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/measure-prob-L3-concepts.py
Each assert names the ledger row it backs (docs/reports/audit-measure-prob-1-3-ledger.md).
"""
import json
import math
import os
import sys
from fractions import Fraction
from itertools import product

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'measure-prob')
rng = np.random.default_rng(20261106)
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print('FAIL', msg)


def load(name):
    with open(os.path.join(COURSE, name + '.json')) as f:
        return json.load(f)


def close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_code_widget(widget, code):
    passed = 0
    tests = widget['tests']
    prelude = widget.get('prelude', '')
    for t in tests:
        ns = {}
        mode = t.get('compare', 'isclose')
        try:
            exec(prelude, ns)
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            if mode == 'raises':
                try:
                    eval(t['call'], ns)
                    ok = False
                except Exception as e:
                    ok = type(e).__name__ == t['expect']
            else:
                got = eval(t['call'], ns)
                exp = t['expect']
                if isinstance(exp, str):
                    try:
                        exp = eval(exp, ns)
                    except Exception:
                        pass
                if mode == 'fraction':
                    ok = Fraction(got) == Fraction(exp)
                elif mode == 'isclose':
                    ok = close(got, exp)
                else:
                    ok = got == exp
        except Exception:
            ok = False
        passed += bool(ok)
    return passed, len(tests)


def code_checks(doc, path, label):
    w = doc
    for p in path:
        w = w[p]
    sp, n = run_code_widget(w, w['solution'])
    st, _ = run_code_widget(w, w['starter'])
    check(sp == n, f'{label}-code-solution: solution passes {sp} of {n} hidden tests')
    check(st < n, f'{label}-code-starter: starter passes {st} of {n}, must fail at least one')


OUT3 = [''.join(p) for p in product('HT', repeat=3)]
OUT4 = [''.join(p) for p in product('HT', repeat=4)]


def atoms(outcomes, X):
    groups = {}
    for w in outcomes:
        groups.setdefault(X(w), []).append(w)
    return [groups[v] for v in sorted(groups)]


def is_measurable(Y, ats):
    return all(len({Y(w) for w in a}) == 1 for a in ats)


# ---------------------------------------------------------------- l9-information
l9 = load('l9-information')
heads = lambda w: w.count('H')
check(sorted(len(a) for a in atoms(OUT3, heads)) == [1, 1, 3, 3] and 2 ** 4 == 16, 'l9-atoms: sigma(S_3) has atoms 1,3,3,1 and 16 events')
check(len(atoms(OUT3, lambda w: w[:2].count('H'))) == 3, 'l9-atoms: sigma(S_2) has 3 atoms, 8 events')
check(len(atoms(OUT3, lambda w: w[:2])) == 4 and len(atoms(OUT3, lambda w: w)) == 8, 'l9-atoms: F_2 has 4 atoms, F_3 has 8')
check(is_measurable(lambda w: w[:2].count('H'), atoms(OUT3, lambda w: w[:2])), 'l9-atoms: S_2 is F_2-measurable')
check(not is_measurable(heads, atoms(OUT3, lambda w: w[:2])), 'l9-atoms: S_3 is not F_2-measurable')
check(not is_measurable(lambda w: w[0] == 'H', atoms(OUT3, heads)), 'l9-atoms: first toss is not sigma(S_3)-measurable')
check(is_measurable(lambda w: heads(w) >= 2, atoms(OUT3, heads)), 'l9-atoms: at least two heads is sigma(S_3)-measurable')
check(not is_measurable(lambda w: w[0] == 'H', atoms(OUT3, lambda w: w[:2].count('H'))), 'l9-atoms: first toss H is not in sigma(S_2)')
check(sorted(len(a) for a in atoms(OUT4, heads)) == [1, 1, 4, 4, 6] and 2 ** 5 == 32, 'l9-atoms: sigma(S_4) has 5 atoms (1,4,6,4,1), 32 events')
check(len(atoms([''.join(p) for p in product('HT', repeat=5)], lambda w: w[:4])) == 16, 'l9-atoms: F_4 in five tosses has 16 atoms')
# lookback payoff on the two-step tree
paths = {'UU': [100, 120, 144], 'UD': [100, 120, 96], 'DU': [100, 80, 96], 'DD': [100, 80, 64]}
check(max(paths['UD']) == 120 and max(paths['DU']) == 100, 'l9-lookback: running maxima 120 and 100')
check(not is_measurable(lambda w: max(0, max(paths[w]) - 100), atoms(list(paths), lambda w: paths[w][-1])),
      'l9-lookback: lookback payoff is not sigma(S_2)-measurable')
code_checks(l9, ['screens', 8, 'widget'], 'l9')

# ---------------------------------------------------------------- l10-condexp-projection
l10 = load('l10-condexp-projection')
P3 = [Fraction(1, 3)] * 3
X3 = [3, 1, 5]
err = lambda a, b: Fraction((3 - a) ** 2 + (1 - a) ** 2 + (5 - b) ** 2, 3)
check(err(2, 5) == Fraction(2, 3) and all(err(2, 5) <= err(Fraction(a, 10), Fraction(b, 10)) for a in range(61) for b in range(61)),
      'l10-projection: (2,2,5) minimises the mean-square error on the plane, error 2/3')
check(err(3, 3) == Fraction(8, 3) and err(2, 3) > err(2, 5), 'l10-projection: (3,3,3) has error 8/3; (2,2,3) is worse than (2,2,5)')
res = [3 - 2, 1 - 2, 5 - 5]
check(res[0] * 1 + res[1] * 1 + res[2] * 0 == 0 and res[2] == 0, 'l10-projection: residual (1,-1,0) is orthogonal to the plane (a,a,b)')
check(sum(p * x for p, x in zip(P3[:2], X3[:2])) == Fraction(4, 3) == sum(p * 2 for p in P3[:2]), 'l10-projection: E[X 1_A] = E[Y 1_A] = 4/3 on A')
# market table
JT = np.array([[0.10, 0.08, 0.02], [0.10, 0.25, 0.15], [0.03, 0.09, 0.18]])
xv = np.array([-1, 0, 1])
yv = np.array([-2, 0, 2])
rows = JT.sum(axis=1)
cond = (JT * yv).sum(axis=1) / rows
check(np.allclose(cond, [-0.8, 0.2, 1.0]), 'l10-table: E[Y|X] = -0.8, 0.2, 1.0')
check(abs((JT.sum(axis=0) * yv).sum() - 0.24) < 1e-12, 'l10-table: E[Y] = 0.24')
exy = (JT * np.outer(xv, yv)).sum()
check(abs(exy - 0.46) < 1e-12 and abs((rows * xv * cond).sum() - 0.46) < 1e-12, 'l10-table: E[XY] = E[X E[Y|X]] = 0.46')
check(abs((rows * xv * (cond - cond)).sum()) < 1e-12 and abs(exy - (rows * xv * cond).sum()) < 1e-12, 'l10-table: residual orthogonal to X')
vary = (JT.sum(axis=0) * yv ** 2).sum() - 0.24 ** 2
condvar = (JT * yv ** 2).sum(axis=1) / rows - cond ** 2
check(abs(vary - 2.2624) < 1e-12 and np.allclose(condvar, [1.76, 1.96, 1.8]), 'l10-table: Var(Y) = 2.2624, conditional variances 1.76, 1.96, 1.8')
vexp = (rows * cond ** 2).sum() - 0.24 ** 2
check(abs(vexp - 0.3904) < 1e-12 and abs((rows * condvar).sum() - 1.872) < 1e-12 and abs(vexp + (rows * condvar).sum() - vary) < 1e-12,
      'l10-table: total variance splits 0.3904 + 1.872 = 2.2624')
check(abs(-1 * cond[0] - 0.8) < 1e-12, 'l10-table: E[XY | X = -1] = 0.8 = X E[Y|X]')
check(abs((rows * xv).sum() * 0.24 - 0.024) < 1e-12, 'l10-table: E[X]E[Y] = 0.024 differs from E[XY], so not independent')
# Monte Carlo: tower and taking out what is known on the table
idx = rng.choice(9, size=400_000, p=JT.flatten())
xs = xv[idx // 3]
ys = yv[idx % 3]
check(abs((xs * ys).mean() - 0.46) < 0.01, 'l10-table: E[XY] = 0.46 (MC)')
mc_cond = [ys[xs == v].mean() for v in xv]
check(np.allclose(mc_cond, [-0.8, 0.2, 1.0], atol=0.02), 'l10-table: conditional means (MC)')
# Longstaff-Schwartz regression
S = np.array([90, 95, 105, 110.0])
C = np.array([12, 8, 3, 1.0])
slope = ((S - S.mean()) * (C - C.mean())).sum() / ((S - S.mean()) ** 2).sum()
check(abs(slope + 0.54) < 1e-12 and abs(C.mean() + slope * (92 - S.mean()) - 10.32) < 1e-9, 'l10-lsm: slope -0.54, fit 10.32 at 92')
check(np.allclose(np.polyfit(S, C, 1), [slope, C.mean() - slope * S.mean()]), 'l10-lsm: least-squares line agrees with polyfit')
code_checks(l10, ['screens', 9, 'widget'], 'l10')

# ---------------------------------------------------------------- l11-filtrations
l11 = load('l11-filtrations')
moves = lambda path: [1 if c == 'H' else -1 for c in path]
gains = lambda H, path: sum(h * m for h, m in zip(H, moves(path)))
momentum = lambda path, k: 1 if k > 1 and path[k - 2] == 'H' else 0
check([momentum('HHTH', k) for k in range(1, 5)] == [0, 1, 1, 0] and gains([0, 1, 1, 0], 'HHTH') == 0, 'l11-gains: momentum (0,1,1,0) gains 0 on HHTH')
check(gains([1, 1, -1, 1], 'HHTH') == 4, 'l11-gains: look-ahead gains 4 on HHTH')
dip = lambda path, k: 1 if k > 1 and path[k - 2] == 'T' else 0
check([dip('TTHTH', k) for k in range(1, 6)] == [0, 1, 1, 0, 1] and gains([0, 1, 1, 0, 1], 'TTHTH') == 1, 'l11-gains: buy-the-dip gains 1 on TTHTH')
trend = lambda path, k: 0 if k == 1 else (1 if path[k - 2] == 'H' else -1)
check(gains([trend('HHHHT', k) for k in range(1, 6)], 'HHHHT') == 2, 'r3-trend: trend rule gains 2 on HHHHT')
# every predictable rule averages 0 over all paths of the fair walk; look-ahead averages 1 per step
for rule, name, expect in ((momentum, 'momentum', 0), (dip, 'dip', 0), (trend, 'trend', 0), (lambda p, k: 1, 'hold', 0)):
    avg = Fraction(sum(gains([rule(w, k) for k in range(1, 7)], w) for w in (''.join(p) for p in product('HT', repeat=6))), 64)
    check(avg == expect, f'l11-predictable: {name} rule averages {expect} over all 64 paths (martingale transform)')
look = lambda p, k: 1 if p[k - 1] == 'H' else -1
avg_look = Fraction(sum(gains([look(w, k) for k in range(1, 7)], w) for w in (''.join(p) for p in product('HT', repeat=6))), 64)
check(avg_look == 6, 'l11-lookahead: look-ahead averages 1 per step (6 over 6 tosses)')
Xmc = rng.choice([-1, 1], size=(100_000, 10))
check(abs((Xmc * Xmc).sum(axis=1).mean() - 10) < 1e-9, 'l11-lookahead: H_n = X_n earns exactly 10 over 10 tosses (MC)')
Hm = np.concatenate([np.zeros((100_000, 1)), (Xmc[:, :-1] == 1).astype(float)], axis=1)
check(abs((Hm * Xmc).sum(axis=1).mean()) < 0.03, 'l11-predictable: momentum averages 0 over 10 tosses (MC)')
code_checks(l11, ['screens', 7, 'widget'], 'l11')

# ---------------------------------------------------------------- l12-martingales-defined
l12 = load('l12-martingales-defined')


def doob(f, n, p):
    p = Fraction(p)
    out = {}

    def go(prefix):
        if len(prefix) == n:
            out[prefix] = Fraction(f(prefix))
        else:
            out[prefix] = p * go(prefix + 'H') + (1 - p) * go(prefix + 'T')
        return out[prefix]
    go('')
    return out


def is_mart(values, n, p):
    p = Fraction(p)
    return all(p * values[w + 'H'] + (1 - p) * values[w + 'T'] == values[w] for w in values if len(w) < n)


half = Fraction(1, 2)
d = doob(lambda w: 1 if heads(w) >= 2 else 0, 3, half)
check([d[k] for k in ('', 'H', 'T', 'HH', 'HT', 'TH', 'TT')] == [half, Fraction(3, 4), Fraction(1, 4), 1, half, half, 0], 'l12-doob: forecaster values')
check(is_mart(d, 3, half), 'l12-doob: the Doob martingale passes the one-step check (tower)')
d2 = doob(heads, 3, half)
check(d2['H'] == 2 and d2['T'] == 1 and d2[''] == Fraction(3, 2), 'l12-doob: heads count forecast 2 after H, 1 after T, 1.5 at root')
d3 = doob(heads, 3, Fraction(4, 5))
check(d3['H'] == Fraction(13, 5) and d3['T'] == Fraction(8, 5) and d3[''] == Fraction(12, 5), 'r3-doob: p = 0.8 gives 2.6, 1.6 and 2.4')
check(doob(lambda w: 1 if heads(w) >= 2 else 0, 3, Fraction(3, 5))[''] == Fraction(81, 125), 'l12-doob: P(>= 2 heads) = 81/125 at p = 3/5')


def build(n, g):
    return {''.join(w)[:k]: g(''.join(w)[:k]) for w in product('HT', repeat=n) for k in range(n + 1)}


Sw = lambda w: w.count('H') - w.count('T')
check(is_mart(build(4, Sw), 4, half), 'l12-square-martingale: S_n is a martingale')
check(is_mart(build(4, lambda w: Sw(w) ** 2 - len(w)), 4, half), 'l12-square-martingale: S_n^2 - n is a martingale')
check(not is_mart(build(4, lambda w: Sw(w) ** 2), 4, half), 'l12-square-martingale: S_n^2 is not')
check(is_mart(build(5, lambda w: Sw(w) ** 3 - 3 * len(w) * Sw(w)), 5, half), 'r3-cube: S_n^3 - 3 n S_n is a martingale')
check(not is_mart(build(5, lambda w: Sw(w) ** 3 - 3 * Sw(w)), 5, half), 'r3-cube: S_n^3 - 3 S_n is not')
check(not is_mart(build(5, lambda w: Sw(w) ** 3 - len(w) - 3 * Sw(w)), 5, half), 'r3-cube: S_n^3 - n - 3 S_n is not')
check(not is_mart(build(5, lambda w: Sw(w) ** 2 + Sw(w)), 5, half), 'r3-cube: S_n^2 + S_n is not')
p6 = Fraction(3, 5)
check(is_mart(build(4, lambda w: Sw(w) - Fraction(len(w), 5)), 4, p6) and not is_mart(build(4, Sw), 4, p6), 'l12-drift: S_n - n/5 is a martingale at p = 0.6, S_n is not')
check(is_mart(build(4, lambda w: Sw(w) - Fraction(len(w), 2)), 4, Fraction(3, 4)), 'l12-drift: c = 0.5 at p = 0.75 (quiz)')
# h-mart at p = 2/3
p23 = Fraction(2, 3)
check(is_mart(build(4, lambda w: Sw(w) - Fraction(len(w), 3)), 4, p23), 'h3-mart: S_n - n/3 is a martingale')
check(is_mart(build(4, lambda w: (Sw(w) - Fraction(len(w), 3)) ** 2 - Fraction(8 * len(w), 9)), 4, p23), 'h3-mart: centred square minus 8n/9 is a martingale')
check(not is_mart(build(4, lambda w: Sw(w) ** 2 - len(w)), 4, p23), 'h3-mart: S_n^2 - n is not at p = 2/3')
check(is_mart(build(4, lambda w: Fraction(1, 2) ** Sw(w)), 4, p23), 'h3-mart: (1/2)^{S_n} is a martingale at p = 2/3')
# one-step-back trap: X_3 = X_1 when X_2 = 0
vals = {'': 0}
for x1 in (1, -1):
    vals[('H' if x1 == 1 else 'T')] = x1
    for x2 in (x1 + 1, x1 - 1):
        key = ('H' if x1 == 1 else 'T') + ('H' if x2 > x1 else 'T')
        vals[key] = x2
        x3 = x1 if x2 == 0 else x2
        vals[key + 'H'] = x3
        vals[key + 'T'] = x3
check(not is_mart(vals, 3, half), 'l12-one-step-back: the process fails the martingale check given the full history')
check(vals['HT' + 'H'] == 1 and vals['TH' + 'H'] == -1, 'l12-one-step-back: on X_1 = 1, X_2 = 0 the next value is 1 (and -1 after T, H)')
# E[X_3 | X_2 = 0] = 0 yet E[X_3 | X_1, X_2] = X_1 on X_2 = 0
check((vals['HTH'] + vals['THH']) / 2 == 0, 'l12-one-step-back: E[X_3 | X_2 = 0] = 0 (one step back passes)')
# discounted price
disc_up, disc_dn = 120 / 1.05, 80 / 1.05
q = (1.05 - 0.8) / (1.2 - 0.8)
check(abs(q - 0.625) < 1e-12 and abs(q * disc_up + (1 - q) * disc_dn - 100) < 1e-9, 'l12-discounted: q = 0.625 gives a martingale')
check(abs(0.7 * disc_up + 0.3 * disc_dn - 102.86) < 0.005, 'l12-discounted: p = 0.7 gives 102.86')
code_checks(l12, ['screens', 7, 'widget'], 'l12')

# ---------------------------------------------------------------- l13-stopping-times
l13 = load('l13-stopping-times')


def ruin_mc(k, N, n_paths, max_steps=20000):
    pos = np.full(n_paths, k, dtype=int)
    t = np.zeros(n_paths, dtype=int)
    alive = np.ones(n_paths, dtype=bool)
    for _ in range(max_steps):
        if not alive.any():
            break
        step = rng.choice([-1, 1], size=alive.sum())
        pos[alive] += step
        t[alive] += 1
        alive = (pos > 0) & (pos < N)
    return pos, t, alive


pos, t, alive = ruin_mc(3, 10, 200_000)
check(not alive.any(), 'l13-ruin: every walk from 3 exits (0,10) within the step cap (T finite a.s.)')
check(abs(pos.mean() - 3) < 0.03, 'l13-ruin: E[S_T] = 3, the start (MC)')
check(abs((pos == 10).mean() - 0.3) < 0.005, 'l13-ruin: P(hit 10) = 3/10 (MC)')
check(abs(t.mean() - 21) < 0.3, 'l13-ruin: E[T] = 21 = 3 x 7 (MC)')
check(abs((pos ** 2).mean() - 30) < 0.3 and abs((pos ** 2 - t).mean() - 9) < 0.3, 'l13-ruin: E[S_T^2] = 30 and E[S_T^2 - T] = 9 (MC)')
pos4, t4, _ = ruin_mc(4, 12, 100_000)
check(abs((pos4 == 12).mean() - 1 / 3) < 0.006 and abs(t4.mean() - 32) < 0.6, 'l13-ruin: from 4 with ends 0, 12: P = 1/3, E[T] = 32 (MC)')
pos6, t6, _ = ruin_mc(6, 15, 100_000)
check(abs((pos6 == 15).mean() - 0.4) < 0.006 and abs(t6.mean() - 54) < 1.0, 'r3-ruin: from 6 with ends 0, 15: P = 0.4, E[T] = 54 (MC)')
posb, tb, _ = ruin_mc(3, 4, 100_000)
check(abs((posb == 4).mean() - 0.75) < 0.006 and abs(tb.mean() - 3) < 0.1, 'l13-ruin: stops at -3/+1 from 0: P = 3/4, E[T] = 3 (MC)')
# exact gambler's ruin via linear system agrees with k/N and k(N-k)
for k, N in ((3, 10), (4, 12), (6, 15)):
    A = np.zeros((N - 1, N - 1))
    for i in range(1, N):
        A[i - 1, i - 1] = 1
        if i - 1 >= 1:
            A[i - 1, i - 2] = -0.5
        if i + 1 <= N - 1:
            A[i - 1, i] = -0.5
    bP = np.zeros(N - 1)
    bP[-1] = 0.5
    Pk = np.linalg.solve(A, bP)[k - 1]
    Tk = np.linalg.solve(A, np.ones(N - 1))[k - 1]
    check(abs(Pk - k / N) < 1e-9 and abs(Tk - k * (N - k)) < 1e-9, f'l13-ruin: exact P = {k}/{N} and E[T] = {k * (N - k)} by first-step analysis')
# no floor: stop at first hit of +1 from 0
n_paths, cap = 100_000, 100_000
pos_ = np.zeros(n_paths, dtype=int)
mn = np.zeros(n_paths, dtype=int)
alive = np.ones(n_paths, dtype=bool)
for _ in range(cap):
    if not alive.any():
        break
    pos_[alive] += rng.choice([-1, 1], size=alive.sum())
    mn = np.minimum(mn, pos_)
    alive = pos_ < 1
hit = ~alive
check(hit.mean() > 0.99, 'l13-no-floor: nearly every walk hits +1 within 100,000 steps (recurrence)')
check((pos_[hit] == 1).all(), 'l13-no-floor: S_T = 1 on every path that stopped')
# P(min before hitting 1 <= -m) = 1/(m+1), so E[sup |S_{T and n}|] = sum 1/(m+1) diverges
for m in (1, 2, 5, 10):
    check(abs((mn <= -m).mean() - 1 / (m + 1)) < 0.01, f'l13-no-floor: P(dip to -{m} before +1) = 1/{m + 1} (MC)')
check((-mn.astype(float)).mean() > 5, 'l13-no-floor: mean depth of the dip is large (diverges with the cap: no integrable dominator)')
# maximum of the first 10 steps: E[M_10] = 1067/512, reflection principle
def max_mean(N):
    total = Fraction(0)
    for steps in product((1, -1), repeat=N):
        s = m = 0
        for x in steps:
            s += x
            m = max(m, s)
        total += m
    return total / 2 ** N


check(max_mean(10) == Fraction(1067, 512) and abs(float(Fraction(1067, 512)) - 2.084) < 5e-4, 'l13-max: E[M_10] = 1067/512 = 2.084')
check(max_mean(4) == Fraction(19, 16) and abs(19 / 16 * 0.5 - 0.5938) < 5e-5, 'l13-max: E[M_4] = 19/16, so 0.5938 pounds at 0.50 a step')
check(max_mean(2) == Fraction(3, 4) and max_mean(0) == 0, 'l13-max: E[M_2] = 3/4, E[M_0] = 0')
# reflection principle P(M_n = m) = P(S_n = m) + P(S_n = m + 1)
from collections import Counter
cnt = Counter()
for steps in product((1, -1), repeat=10):
    s = m = 0
    for x in steps:
        s += x
        m = max(m, s)
    cnt[m] += 1
pS = lambda m: Fraction(math.comb(10, (10 + m) // 2), 1024) if (10 + m) % 2 == 0 and -10 <= m <= 10 else Fraction(0)
check(all(Fraction(cnt[m], 1024) == pS(m) + pS(m + 1) for m in range(0, 11)), 'l13-max: reflection principle P(M = m) = P(S_10 = m) + P(S_10 = m + 1)')
check(abs(10 * math.comb(10, 5) / 1024 - 2.4609) < 5e-5, 'l13-max: E|S_10| = 2.4609')
code_checks(l13, ['screens', 8, 'widget'], 'l13')
# stopped_mean on the biased walk equals (2p-1) E[T] (Wald)
S_ = lambda w: w.count('H') - w.count('T')


def stopped_stats(N, rule, p):
    p = Fraction(p)
    total = Fraction(0)
    et = Fraction(0)
    for steps in product('HT', repeat=N):
        prob = Fraction(1)
        for c in steps:
            prob *= p if c == 'H' else 1 - p
        s = 0
        T = N
        for k, c in enumerate(steps):
            s += 1 if c == 'H' else -1
            if rule(''.join(steps[:k + 1])):
                T = k + 1
                break
        total += s * prob
        et += T * prob
    return total, et


m_, et_ = stopped_stats(10, lambda w: S_(w) == 1, Fraction(3, 5))
check(m_ == Fraction(6043193, 9765625) and m_ == (2 * Fraction(3, 5) - 1) * et_, 'l13-wald: stopped mean 6043193/9765625 equals (2p-1) E[T]')

# ---------------------------------------------------------------- review-3, homework-3
check(Fraction(35, 12) - Fraction(1, 4) == Fraction(8, 3) and sum((x - (3 if x % 2 else 4)) ** 2 for x in range(1, 7)) / 6 == 8 / 3,
      'r3-die: mean-square error 8/3 = Var(X) - Var(E[X|G])')
check(sorted(len(a) for a in atoms(OUT4, lambda w: w[:3].count('H'))) == [2, 2, 6, 6], 'h3-atoms: sigma(Y) atoms 2, 6, 6, 2 (largest 6)')
check(not is_measurable(heads, atoms(OUT4, lambda w: w[:3].count('H'))), 'h3-atoms: Z is not sigma(Y)-measurable')
check(all(len({w[:3] for w in a}) == len(a) // 2 for a in atoms(OUT4, lambda w: w[:3].count('H'))), 'h3-atoms: each atom pairs three-toss paths with both values of toss 4')
pr = [Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(4, 10)]
xx = [10, 20, 30, 40]
y1 = sum(p * x for p, x in zip(pr[:2], xx[:2])) / sum(pr[:2])
y2 = sum(p * x for p, x in zip(pr[2:], xx[2:])) / sum(pr[2:])
Y = [y1, y1, y2, y2]
e2 = sum(p * (x - y) ** 2 for p, x, y in zip(pr, xx, Y))
check(y1 == Fraction(50, 3) and y2 == Fraction(250, 7) and e2 == Fraction(500, 21), 'h3-proj: forecasts 50/3, 250/7, error 500/21')
check(e2 == sum(p * x * x for p, x in zip(pr, xx)) - sum(p * y * y for p, y in zip(pr, Y)) and sum(p * x * x for p, x in zip(pr, xx)) == 1000,
      'h3-proj: E[X^2] - E[Y^2] = 1000 - 976.19 equals the error (Pythagoras)')
A_rule = lambda path, k: 0 if k == 1 else (2 if path[k - 2] == 'T' else 0)
check([A_rule('HTTHTH', k) for k in range(1, 7)] == [0, 0, 2, 2, 0, 2] and gains([0, 0, 2, 2, 0, 2], 'HTTHTH') == 2, 'h3-gains: A gains 2')
check(gains([2 * m for m in moves('HTTHTH')], 'HTTHTH') == 12, 'h3-gains: B gains 12')
avgA = Fraction(sum(gains([A_rule(w, k) for k in range(1, 7)], w) for w in (''.join(p) for p in product('HT', repeat=6))), 64)
check(avgA == 0, 'h3-gains: A averages 0 over all paths')
hw3 = load('homework-3')
code_checks(hw3, ['items', 5, 'widget'], 'h3')


def exit_stats(k, N, p):
    p = Fraction(p)
    if p == Fraction(1, 2):
        return Fraction(k, N), Fraction(k * (N - k))
    r = (1 - p) / p
    P = (1 - r ** k) / (1 - r ** N)
    return P, (N * P - k) / (2 * p - 1)


# biased ruin by first-step analysis agrees with the formulas
for k, N, p in ((3, 10, Fraction(3, 5)), (2, 8, Fraction(2, 3)), (4, 9, Fraction(1, 3)), (1, 4, Fraction(9, 10))):
    pf = float(p)
    A = np.zeros((N - 1, N - 1))
    for i in range(1, N):
        A[i - 1, i - 1] = 1
        if i - 1 >= 1:
            A[i - 1, i - 2] = -(1 - pf)
        if i + 1 <= N - 1:
            A[i - 1, i] = -pf
    bP = np.zeros(N - 1)
    bP[-1] = pf
    Pk = np.linalg.solve(A, bP)[k - 1]
    Tk = np.linalg.solve(A, np.ones(N - 1))[k - 1]
    P_, T_ = exit_stats(k, N, p)
    check(abs(Pk - float(P_)) < 1e-9 and abs(Tk - float(T_)) < 1e-9, f'h3-exit-stats: k={k}, N={N}, p={p}: formulas agree with first-step analysis')
# Wald for the die: first 5 or 6
rolls = rng.integers(1, 7, size=(200_000, 60))
stop = np.argmax(rolls >= 5, axis=1)
Tdie = stop + 1
tot = np.array([rolls[i, :Tdie[i]].sum() for i in range(20_000)])
check(abs(Tdie.mean() - 3) < 0.03 and abs(tot.mean() - 10.5) < 0.15, 'h3-wald: E[T] = 3 and E[sum] = 10.5 = 3.5 x 3 (MC)')

print(f'{len(failures)} failing checks')
sys.exit(1 if failures else 0)
