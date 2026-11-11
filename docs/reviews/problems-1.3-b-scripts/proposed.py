"""Second read, problems 1.3 (b): the numbers of every fix the review proposes, each by two routes.

Run from the repo root with the scratchpad venv python. Exit 0 when every check holds.
"""
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
R = sp.Rational
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def near(a, b, tol, msg):
    ok(abs(float(a) - float(b)) <= tol, f'{msg}: {float(a)!r} against {float(b)!r}')


def band(v, ans, tol):
    return abs(float(v) - float(ans)) <= tol + 1e-9


x, w, w1, w2 = sp.symbols('x w w1 w2')

# finding 1: two-months part 5, the signs of the two errors
e1 = mp.log('1.08') - mp.mpf('0.0768')
e2 = mp.log('0.95') - mp.mpf('-0.05125')
ok(e1 > 0 > e2, 'the two errors have opposite signs')
near((e1 + e2) * 1e5, 11.8, 0.05, 'true gap of the sum')
near(max(e1, -e2) * 1e5, 16.10, 0.005, 'the larger single error')
ok(abs(e1 + e2) < R(1707, 10 ** 7) < R(2193, 10 ** 7), 'true gap < 17.07e-5 < 21.93e-5')

# finding 3: tail-bound part 4, band 0.008 on 11.594
a4 = R(4, 10) ** 4 / 24
ans = a4 / R(92, 100) * 10 ** 4
near(ans, 11.594, 5e-4, 'tail bound')
for typed, want in (('11.59', True), ('11.60', True), ('11.594', True), ('11.58', False), ('11.61', False), ('10.67', False), ('11.85', False), ('16', False)):
    ok(band(float(typed), 11.594, 0.008) == want, f'tail-bound band 0.008: {typed} should be {want}')
near(R(1067, 10 ** 6) / R(92, 100) * 10 ** 4, 11.598, 5e-4, 'from a_4 = 0.001067'); near(R(1067, 100) / R(92, 100), 11.598, 5e-4, 'from 10.67')

# finding 4: two-months part 4, band 0.01 on 4.86
near(R(233, 100) * R(5, 100) ** 3 / 6 * 10 ** 5, 4.854, 5e-4, 'with M = 2.33')
for typed, want in (('4.86', True), ('4.85', True), ('4.87', True), ('4.84', False), ('4.17', False), ('14.58', False), ('2.08', False)):
    ok(band(float(typed), 4.86, 0.01) == want, f'two-months band 0.01: {typed} should be {want}')

# finding 5: the "unscaled" entries, narrow bands
for val, tol, yes, no in ((0.0001707, 1e-6, ['0.000171', '0.00017', '0.0001707'], ['0.0000853', '0.000512', '0.0032', '0', '0.01']),
                          (0.0000486, 5e-7, ['0.0000486', '0.000049', '0.00004860'], ['0.0000417', '0.0001458', '0.0000208', '0']),
                          (0.0002193, 1e-6, ['0.000219', '0.00022', '0.0002193'], ['0.0001221', '0.0002124', '0.0001707', '0']),
                          (0.0011594, 5e-6, ['0.00116', '0.001159', '0.0011594'], ['0.0010667', '0.0016', '0.0011852', '0.001', '0'])):
    for t in yes:
        ok(band(float(t), val, tol), f'unscaled {val}: {t} should match')
    for t in no:
        ok(not band(float(t), val, tol), f'unscaled {val}: {t} should not match')
ok(band(0.035443, 0.0354, 0.005) and not band(0.35, 0.0354, 0.005) and not band(0.14, 0.0354, 0.005), 'one-lot band 0.005')

# finding 6: two printed terms
near(4 * 103 / 1.04 ** 5, 338.6340, 5e-5, 'loss-limit term 4'); near(sum(t * c / 1.04 ** (t + 1) for t, c in ((1, 3), (2, 3), (3, 3), (4, 103))), 354.43, 0.005, 'sum')
near(round(2.7737 + 5.3340 + 7.6932 + 338.6340, 2), 354.43, 1e-9, 'printed terms add to 354.43')
near(3 / 1.05 ** 4, 2.468107, 5e-7, 'loan term 3'); near(0.907029 + 1.727675 + 2.468107, 5.10281, 5e-6, 'printed terms add to 5.10281')

# finding 8: p-cube-root-27 on a new function, the fourth root about 16
f = x ** R(1, 4)
ok(f.subs(x, 16) == 2 and sp.diff(f, x).subs(x, 16) == R(1, 32) and sp.diff(f, x, 2).subs(x, 16) == R(-3, 2048), 'f(16) = 2, f\' = 1/32, f\'\' = -3/2048')
ok(sp.simplify(sp.diff(f, x) - R(1, 4) * x ** R(-3, 4)) == 0 and sp.simplify(sp.diff(f, x, 2) + R(3, 16) * x ** R(-7, 4)) == 0, 'the two derivative formulae')
h = R(32, 100)
Lv = 2 + h / 32
ok(Lv == R(201, 100), 'L(16.32) = 2.01')
ok((2 + h / 8, 2 + h / 4, 2 + R(1632, 100) / 32) == (R(204, 100), R(208, 100), R(251, 100)), 'part 2 slips 2.04, 2.08, 2.51')
err = R(1, 2) * R(-3, 2048) * h ** 2
ok(err == R(-75, 10 ** 6), 'predicted error -0.000075 exactly')
ok((2 * err, R(1, 2) * R(-3, 2048) * h, -err) == (R(-15, 10 ** 5), R(-3, 12800), R(75, 10 ** 6)), 'part 3 slips'); near(R(-3, 12800), -0.000234, 5e-7, 'h-not-squared')
ok(Lv + err == R(2009925, 10 ** 6), 'corrected estimate 2.009925')
ok((Lv - err, Lv + 2 * err, R(204, 100) + err) == (R(2010075, 10 ** 6), R(200985, 10 ** 5), R(2039925, 10 ** 6)), 'part 4 slips')
true = mp.mpf('16.32') ** mp.mpf('0.25')
near(true, 2.009926, 5e-7, 'true fourth root of 16.32'); near(true - mp.mpf('2.01'), -0.000074, 5e-7, 'true error of the tangent')
near(2 * mp.root(mp.mpf('1.02'), 4), true, 1e-20, 'second route')

# finding 9: p-min-variance-pair on new assets, 40% and 25%, correlation 0.3
a, b, c = R(16, 100), R(625, 10000), R(3, 10) * R(4, 10) * R(25, 100)
var = a * w ** 2 + b * (1 - w) ** 2 + 2 * c * w * (1 - w)
ok(2 * c == R(6, 100) and sp.expand(var) == R(1625, 10000) * w ** 2 - R(65, 1000) * w + R(625, 10000), 'quadratic 0.1625w^2 - 0.065w + 0.0625')
ok(sp.expand(a * w ** 2 + b * (1 - w) ** 2) == R(2225, 10000) * w ** 2 - R(125, 1000) * w + R(625, 10000), 'no-cross')
ok(sp.expand(a * w ** 2 + b * (1 - w) ** 2 + c * w * (1 - w)) == R(1925, 10000) * w ** 2 - R(95, 1000) * w + R(625, 10000), 'half-cross')
ws = sp.solve(sp.diff(var, w), w)[0]
ok(ws == R(1, 5), 'w = 0.2'); ok(R(65, 1000) / R(1625, 10000) == R(2, 5), 'no-two 0.4'); near(R(125, 1000) / R(445, 1000), 0.2809, 5e-5, 'carried 0.2809')
grid = min((float(var.subs(w, R(i, 1000))), i / 1000) for i in range(0, 1001))
near(grid[1], 0.2, 1e-9, 'grid search w'); near(grid[0], 0.056, 1e-12, 'grid search variance')
vmin = var.subs(w, ws)
ok(vmin == R(56, 1000), 'variance 0.056'); near(sp.sqrt(vmin), 0.2366, 5e-5, 'volatility 0.2366')
ok(R(1, 5) * R(4, 10) + R(4, 5) * R(25, 100) == R(28, 100), 'weighted 0.28'); ok(sp.sqrt(var.subs(w, R(2, 5))) == R(1, 4), 'carried-half 0.25')
v2 = a * w1 ** 2 + b * w2 ** 2 + 2 * c * w1 * w2
at = {w1: R(1, 5), w2: R(4, 5)}
ok(sp.diff(v2, w1) == R(32, 100) * w1 + R(6, 100) * w2 and sp.diff(v2, w1).subs(at) == R(112, 1000) == 2 * vmin, 'lambda 0.112 = 2 x 0.056')
ok(sp.diff(v2, w2).subs(at) == R(112, 1000) and R(125, 1000) * R(4, 5) + R(6, 100) * R(1, 5) == R(112, 1000), 'the other partial agrees: 0.1 + 0.012')
ok(R(32, 100) * R(1, 5) == R(64, 1000), 'no-cross 0.064')
est = vmin + R(112, 1000) * R(2, 100)
ok(est == R(5824, 10 ** 5), 'estimate 0.05824'); near(vmin * R(102, 100) ** 2, 0.0582624, 5e-8, 'exact 0.0582624')
ok(band(0.0582, 0.05824, 0.0001) and band(0.0583, 0.05824, 0.0001) and band(0.05826, 0.05824, 0.0001), 'band 0.0001 takes 0.0582, 0.0583, 0.05826')
ok(vmin + vmin * R(2, 100) == R(5712, 10 ** 5) and vmin + R(112, 1000) == R(168, 1000), 'slips 0.05712 and 0.168')
ok(not band(0.05712, 0.05824, 0.0001) and not band(0.056, 0.05824, 0.0001), 'slips outside the band')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
