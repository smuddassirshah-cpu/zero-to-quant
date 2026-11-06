"""Recompute every number stated in garch level 1 (Clustering) and check it at its JSON path (second read).

Run: python3 docs/reports/garch-L1-numbers.py   (NumPy, SciPy and the standard library; exits 0 when every check passes)

The data are rebuilt from the brief's generator (share B: seed 7; series A: 0.01 x seed 8; series C: the variance
break, seed 9). Every statistic is computed by hand here (ACF with the statsmodels convention, Ljung-Box, ARCH-LM by
least squares, moments), so the script needs no statsmodels; where SciPy has the same statistic it is computed a
second way and the two must agree (`two`). `E` (lv.expect) checks the stated value appears where it is stated.
A check that fails because the content is wrong is a finding in docs/reviews/review-garch.md and stays failing
until the fix pass corrects the content.
"""
import math
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("garch", 1)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
    """A claim tied to its wording: while `phrase` is in the text, the claim must hold (a fix may reword it)."""
    there = phrase in lv.text(ref, path)
    lv._rec(bool(ok) or not there, f'stated: {ref} {path} "{phrase}"', '' if ok or not there else 'the stated claim is false')


def R(x, d):
    return round(float(x), d)


def simulate_garch(omega, alpha, beta, n, seed):
    z = np.random.default_rng(seed).standard_normal(n)
    r = np.empty(n); s2 = np.empty(n)
    s2[0] = omega / (1 - alpha - beta)
    for t in range(n):
        if t > 0:
            s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
        r[t] = np.sqrt(s2[t]) * z[t]
    return r, s2


def acf(x, k):                      # statsmodels convention: demeaned, denominator n * c0
    x = np.asarray(x, float) - np.mean(x)
    c0 = x @ x
    return np.array([x[j:] @ x[:-j] / c0 for j in range(1, k + 1)])


def ljung_box(x, m):
    n = len(x); rho = acf(x, m)
    q = n * (n + 2) * np.sum(rho ** 2 / (n - np.arange(1, m + 1)))
    return q, stats.chi2.sf(q, m)


def arch_lm(x, q):
    y = np.asarray(x, float) ** 2
    Y = y[q:]; X = np.column_stack([np.ones(len(Y))] + [y[q - k:-k] for k in range(1, q + 1)])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    res = Y - X @ b
    r2 = 1 - res @ res / np.sum((Y - Y.mean()) ** 2)
    return len(Y) * r2, stats.chi2.sf(len(Y) * r2, q), r2


def rolling_sd(x, w):
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    for t in range(w - 1, len(x)):
        out[t] = np.std(x[t - w + 1:t + 1], ddof=1)
    return out


def exkurt(x):
    d = np.asarray(x, float) - np.mean(x)
    return np.mean(d ** 4) / np.mean(d ** 2) ** 2 - 3


r, s2 = simulate_garch(2e-6, 0.08, 0.90, 2000, 7)
iid = 0.01 * np.random.default_rng(8).standard_normal(2000)
C = np.where(np.arange(2000) < 1000, 0.007, 0.013) * np.random.default_rng(9).standard_normal(2000)
A10 = iid.copy(); A10[1000] = -0.10
S252 = math.sqrt(252)
sB = np.std(r, ddof=1)

# ================= l1 calm and storms =================
L = 'l1'
tv = np.sqrt(252 * s2)
storm_start = int(np.argmax(tv > 0.25))
two('storm start', storm_start, 1392)
E(L, 'screens[0].explain.text', 1392); E(L, 'screens[0].explain.canvas.right.shade[0].from', 1392)
v20B, v20A, v20C = rolling_sd(r, 20) * S252, rolling_sd(iid, 20) * S252, rolling_sd(C, 20) * S252
two('B 20-day min day', int(np.nanargmin(v20B)), 561); two('B 20-day max day', int(np.nanargmax(v20B)), 1409)
for p, v in [('screens[1].explain.text', R(100 * np.nanmin(v20B), 1)), ('screens[1].explain.text', R(100 * np.nanmax(v20B), 1)),
             ('screens[1].explain.text', R(100 * np.nanmin(v20A), 1)), ('screens[1].explain.text', R(100 * np.nanmax(v20A), 1)),
             ('screens[1].explain.text', 561), ('screens[1].explain.text', 1409)]:
    E(L, p, v)
E(L, 'screens[1].widget.options[0].text', round(100 * np.nanmin(v20B))); E(L, 'screens[1].widget.options[0].text', round(100 * np.nanmax(v20B)))
E(L, 'screens[1].widget.options[0].text', round(100 * np.nanmin(v20A))); E(L, 'screens[1].widget.options[0].text', round(100 * np.nanmax(v20A)))
claim('l1 s1 B peak is twice A highest', 1.9 < np.nanmax(v20B) / np.nanmax(v20A) < 2.2)
E(L, 'screens[1].widget.options[2].why', 49)
# five largest moves
big = sorted(np.argsort(-np.abs(r))[:5])
two('five largest days', tuple(big) == (1402, 1426, 1455, 1456, 1468), True)
for d in big:
    E(L, 'screens[2].hints[2].text', d)
    E(L, f'screens[2].canvas.state.markers[{big.index(d)}].label', f'{100 * r[d]:+.2f}%'.replace('-', '−'))
claim('three of five are rises', sum(r[d] > 0 for d in big) == 3)
E(L, 'screens[2].feedback.byKey.falls', R(100 * r[1426], 2)); E(L, 'screens[2].feedback.byKey.falls', R(100 * r[1456], 2)); E(L, 'screens[2].feedback.byKey.falls', R(100 * r[1468], 2))
E(L, 'screens[2].explain.text', 1468 - 1402); E(L, 'screens[2].widget.options[2].why', 1468 - 1402)   # fix pass 15: five days within 66 days of each other
# "five in one 66-day window would be very unlikely": exact chance for 5 random days out of 2,000
cnt = sum(math.comb(min(66, 1999 - m), 4) for m in range(2000))
claim('five random days within 66 days is very unlikely (< 1e-4)', cnt / math.comb(2000, 5) < 1e-4)
# block sds
bB = [np.std(b, ddof=1) for b in np.array_split(r, 8)]; bA = [np.std(b, ddof=1) for b in np.array_split(iid, 8)]
for i in range(8):
    E(L, f'screens[3].canvas.params.rows[{i}][2]', f'{100 * bB[i]:.3f}%'); E(L, f'screens[3].canvas.params.rows[{i}][3]', f'{100 * bA[i]:.3f}%')
    E(L, f'screens[8].canvas.params.rows[{i}][2]', f'{100 * bB[i]:.3f}%')
E(L, 'screens[3].explain.text', R(max(bB) / min(bB), 2)); E(L, 'screens[3].explain.text', R(max(bA) / min(bA), 2))
E(L, 'screens[3].feedback.correct', R(100 * min(bB), 3)); E(L, 'screens[3].feedback.correct', R(100 * max(bB), 3))
E(L, 'screens[3].feedback.correct', R(100 * min(bA), 3)); E(L, 'screens[3].feedback.correct', R(100 * max(bA), 3))
# sign against size
E(L, 'screens[4].prose', R(200 * sB, 2))


def nextday(x):
    s = np.std(x, ddof=1); big_ = np.abs(x) > 2 * s
    prev, nxt = x[:-1], x[1:]
    out = {'any': (len(nxt), np.mean(nxt > 0), np.mean(np.abs(nxt) > 2 * s))}
    for k, m in [('rise', prev > 2 * s), ('fall', prev < -2 * s), ('move', np.abs(prev) > 2 * s)]:
        out[k] = (int(m.sum()), np.mean(nxt[m] > 0), np.mean(np.abs(nxt[m]) > 2 * s))
    return out


nB, nA = nextday(r), nextday(iid)
rows = [(0, nB['any']), (1, nB['rise']), (2, nB['fall']), (3, nA['any']), (4, nA['move'])]
for i, (cnt_, up, bg) in rows:
    E(L, f'screens[4].canvas.params.rows[{i}][1]', cnt_)
    E(L, f'screens[4].canvas.params.rows[{i}][2]', f'{100 * up:.1f}%'); E(L, f'screens[4].canvas.params.rows[{i}][3]', f'{100 * bg:.1f}%')
after_big = nB['move'][2]
E(L, 'screens[4].explain.text', R(100 * after_big, 1)); E(L, 'screens[4].explain.text', R(100 * nB['any'][2], 1))
E(L, 'screens[4].explain.text', R(100 * nA['move'][2], 1)); E(L, 'screens[4].explain.text', R(100 * nA['any'][2], 1))
two('about six times', round(after_big / nB['any'][2]), 6)
E(L, 'screens[4].feedback.byKey.sign', round(100 * math.sqrt(0.25 / 49)))
E(L, 'screens[4].widget.options[1].why', R(100 * nB['fall'][1], 1)); E(L, 'screens[4].widget.options[1].why', R(100 * nB['any'][1], 1))
E(L, 'screens[10].prose', R(after_big, 3)); E(L, 'screens[10].prose', R(nB['any'][2], 3))
E(L, 'screens[10].prose', R(nB['rise'][1], 2)); E(L, 'screens[10].prose', R(nB['any'][1], 2))
E(L, 'summary.formula.note', R(after_big, 3)); E(L, 'summary.formula.note', R(nB['any'][2], 3))
E(L, 'quiz[1].explain.text', round(100 * after_big)); E(L, 'quiz[1].explain.text', R(100 * nB['any'][2], 1))
# regimes
two('storm length', 1 / (1 - 0.95), 20); E(L, 'screens[5].widget.answer', 20)
E(L, 'screens[5].feedback.byKey.leave', 1 / 0.05); E(L, 'screens[5].feedback.byKey.leave', 5)   # fix pass 17: the 5 is the exit chance read as days
E(L, 'screens[5].widget.wrong[0].value', 95); E(L, 'screens[5].widget.wrong[1].value', 1 / 0.02); E(L, 'screens[5].widget.wrong[2].value', 5)
E(L, 'quiz[0].widget.answer', round(1 / (1 - 0.9))); E(L, 'quiz[0].widget.wrong[0].value', 90); E(L, 'quiz[0].widget.wrong[1].value', 9)
# ACF of returns, Ljung-Box
rho = acf(r, 10)
for k in range(10):
    E(L, f'screens[6].canvas.state.values.{k + 1}', R(rho[k], 4))
band = 1.96 / math.sqrt(2000); E(L, 'screens[6].prose', R(band, 4))
claim('only lag 3 is outside the band', [k + 1 for k in range(10) if abs(rho[k]) > band] == [3])
E(L, 'screens[6].hints[1].text', R(rho[2] - band, 3))
Q, pQ = ljung_box(r, 10)
E(L, 'screens[6].explain.text', R(Q, 2)); E(L, 'screens[6].explain.text', R(pQ, 2)); E(L, 'screens[6].widget.options[1].why', R(pQ, 2))
E(L, 'screens[6].widget.options[0].text', R(rho[0], 4)); E(L, 'screens[6].widget.options[1].text', R(rho[2], 4))
# rolling_vol example
ex = rolling_sd([0.01, -0.02, 0.015, 0.0, -0.01], 3)[2:]
for i, v in enumerate(ex):
    E(L, f'screens[7].canvas.params.rows[{i + 2}][2]', f'{v:.6f}')
E(L, 'quiz[2].widget.answer', 59); E(L, 'quiz[2].widget.wrong[0].value', 60)
# series C
E(L, 'screens[8].prose', R(100 * np.nanmin(v20C), 1)); E(L, 'screens[8].prose', R(100 * np.nanmax(v20C), 1))
E(L, 'screens[8].widget.options[1].why', R(100 * np.nanmin(v20C), 1)); E(L, 'screens[8].widget.options[1].why', R(100 * np.nanmax(v20C), 1))
bC = [np.std(b, ddof=1) for b in np.array_split(C, 8)]
for i in range(8):
    E(L, f'screens[8].canvas.params.rows[{i}][1]', f'{100 * bC[i]:.3f}%')
E(L, 'screens[8].hints[1].text', R(100 * min(bC[:4]), 2)); E(L, 'screens[8].hints[1].text', R(100 * max(bC[:4]), 2))
E(L, 'screens[8].hints[1].text', R(100 * min(bC[4:]), 2)); E(L, 'screens[8].hints[1].text', R(100 * max(bC[4:]), 2))
for v in bB[4:]:
    E(L, 'screens[8].hints[2].text', R(100 * v, 2))
# "Within each half its blocks differ by less than 10%" (byKey.same) and "C's last four blocks agree to within 2%"
stated(L, 'screens[8].feedback.byKey.same', 'less than 10%', max(bC[:4]) / min(bC[:4]) - 1 < 0.10 and max(bC[4:]) / min(bC[4:]) - 1 < 0.10)
stated(L, 'screens[8].widget.options[3].why', 'within 2%', max(bC[4:]) / min(bC[4:]) - 1 < 0.02)
# fix pass 1 and 2: the reworded claims, in points of daily sd
E(L, 'screens[8].feedback.byKey.same', 0.07); claim("C's blocks stay within 0.07 points inside each half", 100 * (max(bC[:4]) - min(bC[:4])) <= 0.07 and 100 * (max(bC[4:]) - min(bC[4:])) <= 0.07)
E(L, 'screens[8].widget.options[3].why', 0.03); claim("C's last four blocks agree to within 0.03 points", 100 * (max(bC[4:]) - min(bC[4:])) <= 0.03)
# vol_range
E(L, 'screens[9].prose', R(np.nanmin(v20B), 4)); E(L, 'screens[9].prose', R(np.nanmax(v20B), 4))
E(L, 'screens[9].feedback.correct', R(100 * np.nanmin(v20C), 1)); E(L, 'screens[9].feedback.correct', R(100 * np.nanmax(v20C), 1))
v250A, v250B = rolling_sd(iid, 250) * S252, rolling_sd(r, 250) * S252
for v in (np.nanmin(v250A), np.nanmax(v250A), np.nanmin(v250B), np.nanmax(v250B)):
    E(L, 'screens[9].explain.text', R(100 * v, 1))
# transfer: day 1,404, trailing windows up to yesterday
true1404 = math.sqrt(252 * s2[1404]); w250 = np.std(r[1154:1404], ddof=1) * S252; w20 = np.std(r[1384:1404], ddof=1) * S252
for p in ('screens[11].prose', 'screens[11].explain.text', 'screens[11].widget.options[1].why', 'screens[11].widget.options[3].why'):
    E(L, p, R(100 * true1404, 1))
for p in ('screens[11].explain.text', 'screens[11].widget.options[1].why', 'screens[11].canvas.state.markers[0].label'):
    E(L, p, R(100 * w250, 1))
E(L, 'screens[11].widget.options[3].why', R(100 * w20, 1)); E(L, 'screens[11].hints[2].text', R(true1404 / w250, 1))
E(L, 'screens[11].widget.options[0].text', round(100 * true1404)); E(L, 'screens[11].widget.options[0].text', round(100 * w250))

# ================= l2 squared returns =================
L = 'l2'
sq, ab = acf(r ** 2, 50), acf(np.abs(r), 50)
for k in range(10):
    E(L, f'screens[2].canvas.state.values.sq.{k + 1}', R(sq[k], 4)); E(L, f'screens[2].canvas.state.values.abs.{k + 1}', R(ab[k], 4))
    E(L, f'screens[2].canvas.state.values.r.{k + 1}', R(rho[k], 4)); E(L, f'screens[3].canvas.state.values.{k + 1}', R(sq[k], 4))
for k in range(5):
    E(L, 'screens[3].prose', R(sq[k], 4))
E(L, 'screens[0].explain.text', R(sq[0], 4)); E(L, 'screens[0].feedback.correct', R(sq[0], 4)); E(L, 'screens[0].prose', R(rho[0], 4))
E(L, 'screens[0].feedback.correct', 'eight times') if round(sq[0] / band) == 8 else claim('eight times the band', False)
claim('l2 s2 every |r| and r^2 bar up to lag 10 is above 0.19', min(sq[:10].min(), ab[:10].min()) > 0.19)
E(L, 'screens[0].widget.options[2].why', round(100 * after_big)); E(L, 'screens[0].widget.options[2].why', R(100 * nB['any'][2], 1))
# |r| scatter slope, in %
x1, y1 = 100 * np.abs(r[:-1]), 100 * np.abs(r[1:])
slope = np.polyfit(x1, y1, 1)[0]; sl_signed = np.polyfit(100 * r[:-1], 100 * r[1:], 1)[0]
two('slope by cov/var', slope, np.cov(x1, y1)[0, 1] / np.var(x1, ddof=1))
E(L, 'screens[1].explain.text', R(slope, 3)); E(L, 'screens[1].feedback.correct', R(slope, 3)); E(L, 'screens[1].explain.text', R(sl_signed, 3))
E(L, 'screens[1].canvas.state.line.b', R(np.mean(y1) - slope * np.mean(x1), 3))  # the LS intercept
# Ljung-Box tables
Qs, pQs = ljung_box(r ** 2, 10)
E(L, 'screens[4].canvas.params.rows[0][1]', R(Q, 3)); E(L, 'screens[4].canvas.params.rows[0][2]', R(pQ, 4))
E(L, 'screens[4].canvas.params.rows[1][1]', R(Qs, 2)); claim('p on r^2 below 1e-300', pQs < 1e-300)
crit10 = stats.chi2.ppf(0.95, 10); E(L, 'screens[4].prose', R(crit10, 2)); E(L, 'screens[4].hints[1].text', round(Qs / crit10, -1))
E(L, 'screens[6].canvas.params.lines[2]', f'{Q:.6f}'); E(L, 'screens[6].canvas.params.lines[2]', f'{pQ:.6f}')
E(L, 'screens[6].canvas.params.lines[5]', f'{Qs:.6f}')
two('p on squares, mantissa', float(f'{pQs:.6e}'.split('e')[0]), 7.769182)
E(L, 'screens[6].feedback.byKey.agree', R(float(f'{pQs:.1e}'.split('e')[0]), 1))
QA, pA = ljung_box(iid, 10); QA2, pA2 = ljung_box(iid ** 2, 10)
for p in ('screens[5].explain.text', 'screens[8].explain.text'):
    E(L, p, R(pA, 4)); E(L, p, R(pA2, 4))
E(L, 'screens[5].feedback.correct', R(pA2, 4)); E(L, 'screens[5].canvas.params.rows[0][1]', R(pQ, 4))
# ARCH-LM
lmB, plB, r2B = arch_lm(r, 10); lmA, plA, r2A = arch_lm(iid, 10)
E(L, 'screens[7].canvas.params.rows[0][2]', R(lmB, 2)); E(L, 'screens[7].canvas.params.rows[1][2]', R(lmA, 2))
E(L, 'screens[7].canvas.params.rows[0][3]', R(float(f'{plB:.1e}'), 95)); E(L, 'screens[7].canvas.params.rows[1][3]', R(plA, 4))
E(L, 'screens[7].widget.examples[0].expect', R(lmB, 4)); E(L, 'screens[7].feedback.correct', R(lmB, 2)); E(L, 'screens[7].feedback.correct', R(lmA, 2))
E(L, 'screens[7].explain.text', R(r2B, 3)); E(L, 'screens[7].explain.text', R(r2A, 4)); E(L, 'screens[7].explain.text', R(lmB, 1))
E(L, 'summary.ideas[1]', R(lmB, 1)); E(L, 'summary.ideas[1]', round(Qs))
# |r| against r^2 table, lags 1, 10, 50
sqA, abA = acf(iid ** 2, 50), acf(np.abs(iid), 50)
for i, arr in enumerate([sq, ab, sqA, abA]):
    for j, k in enumerate([1, 10, 50]):
        E(L, f'screens[8].canvas.params.rows[{i}][{j + 1}]', f'{arr[k - 1]:.4f}' if arr[k - 1] >= 0 else f'{arr[k - 1]:.4f}')
claim('A values all inside the band', max(abs(sqA[0]), abs(sqA[9]), abs(sqA[49]), abs(abA[0]), abs(abA[9]), abs(abA[49])) < band)
claim('|r| keeps more memory at lag 50', ab[49] > sq[49])
# largest day to +10%
rb = r.copy(); rb[int(np.argmax(np.abs(r)))] = 0.10
d_sq, d_ab = acf(rb ** 2, 1)[0] - sq[0], acf(np.abs(rb), 1)[0] - ab[0]
E(L, 'screens[8].explain.text', R(abs(d_sq), 3)); E(L, 'screens[8].explain.text', R(abs(d_ab), 3))
# edge case: A with a crash
E(L, 'screens[9].widget.options[0].text', R(acf(A10 ** 2, 1)[0], 4))
for p in ('screens[9].widget.options[0].text', 'screens[9].widget.options[3].why'):
    E(L, p, R(100 * np.std(iid, ddof=1), 3)); E(L, p, R(100 * np.std(A10, ddof=1), 3))
E(L, 'screens[9].widget.options[2].why', R(ljung_box(A10 ** 2, 10)[1], 2)); E(L, 'screens[9].explain.text', R(ljung_box(A10 ** 2, 10)[1], 2))
E(L, 'screens[9].explain.text', R(exkurt(iid), 2)); E(L, 'screens[9].explain.text', R(exkurt(A10), 2))
two('excess kurtosis by scipy', exkurt(r), stats.kurtosis(r))
# quizzes
E(L, 'quiz[0].widget.answer', R(1.96 / math.sqrt(1000), 3)); E(L, 'quiz[0].widget.wrong[0].value', 1.96 / 1000)
E(L, 'quiz[0].widget.wrong[1].value', R(2 / math.sqrt(1000), 4)); E(L, 'quiz[0].explain.text', R(math.sqrt(1000), 2))
E(L, 'quiz[1].prose', R(1.96 / math.sqrt(2500), 3)); E(L, 'quiz[1].explain.text', 'nearly eight') if 7.5 < 0.30 / 0.039 < 8 else None
E(L, 'quiz[2].widget.answer', 995 * 0.02); E(L, 'quiz[2].widget.wrong[0].value', 1000 * 0.02)
E(L, 'quiz[2].feedback.correct', R(stats.chi2.ppf(0.95, 5), 2)); E(L, 'quiz[2].feedback.correct', R(stats.chi2.sf(19.9, 5), 4))

# ================= l3 fat tails =================
L = 'l3'
p3 = 2 * stats.norm.sf(3); two('2(1 - Phi(3)) by erf', p3, 1 - math.erf(3 / math.sqrt(2)))
E(L, 'screens[0].widget.answer', R(2000 * p3, 1)); E(L, 'screens[0].widget.accept', R(2000 * p3, 2)); E(L, 'screens[0].widget.accept', R(p3, 4))
E(L, 'screens[0].widget.wrong[0].value', R(1000 * p3, 1)); E(L, 'screens[0].widget.wrong[2].value', 2000 * 0.05)
z = (r - r.mean()) / sB
n3 = int(np.sum(np.abs(z) > 3)); E(L, 'screens[0].widget.wrong[1].value', n3); E(L, 'screens[0].feedback.correct', n3)
claim('28 is more than five times 5.4', n3 / (2000 * p3) > 5)
# histogram bins of 0.5
cnt0 = int(np.sum((z >= -0.5) & (z < 0))), int(np.sum((z >= 0) & (z < 0.5)))
should = int(np.sum((np.abs(z) >= 1) & (np.abs(z) < 2)))
for p in ('screens[1].explain.text', 'screens[1].widget.options[1].why'):
    E(L, p, cnt0[0]); E(L, p, cnt0[1]); E(L, p, round(2000 * (stats.norm.cdf(0.5) - 0.5)))
E(L, 'screens[1].explain.text', should); E(L, 'screens[1].explain.text', round(2000 * 2 * (stats.norm.cdf(2) - stats.norm.cdf(1))))
# kurtosis by hand
x8 = np.array([0, 0, 0, 0, 0, 0, 2, -2.0])
E(L, 'screens[2].widget.rows[0][1].answer', np.mean(x8 ** 2)); E(L, 'screens[2].widget.rows[1][1].answer', np.mean(x8 ** 4))
E(L, 'screens[2].widget.rows[2][1].answer', exkurt(x8) + 3)
kB, kA = exkurt(r), exkurt(iid)
E(L, 'screens[3].feedback.correct', R(kB, 4)); E(L, 'screens[3].feedback.correct', R(kA, 4))
E(L, 'screens[3].explain.text', R(kB, 2)); E(L, 'screens[3].explain.text', R(kB + 3, 2)); E(L, 'screens[3].explain.text', R(kA, 2))
E(L, 'screens[6].prose', R(kB, 4)); E(L, 'screens[6].widget.options[0].text', R(kB + 3, 2)); E(L, 'screens[6].hints[2].text', R(kB + 3, 4))
E(L, 'screens[6].widget.options[2].why', R(stats.kurtosis(r, bias=False), 2))
# QQ plot
(osm, osr), (slp, icp, rq) = stats.probplot(r, dist='norm')
(_, _), (_, _, rqA) = stats.probplot(iid, dist='norm')
E(L, 'screens[4].explain.text', R(rq, 4)); E(L, 'screens[4].explain.text', R(rqA, 4))
E(L, 'screens[4].explain.text', R(z.min(), 2)); E(L, 'screens[4].explain.text', R(osm[0], 2))
# the tap among: every candidate leaves the line by more than half an sd, and no other plotted point does
pts = lv._file(L)[1]['screens'][4]['canvas']['params']['points']
among = set(lv._file(L)[1]['screens'][4]['widget']['among'])
far = {p['id'] for p in pts if abs(p['y'] - p['x']) > 0.5} if isinstance(pts[0], dict) else {f'p{i}' for i, p in enumerate(pts) if abs(p[1] - p[0]) > 0.5}
claim('l3 s4: the tappable points are exactly those more than 0.5 sd off the line', far == among)
# Student's t
for nu, k in [(6, 6), (5, 9), (10, 4), (7, 5)]:
    two(f't{nu} kurtosis', 3 + 6 / (nu - 4), stats.t.stats(nu, moments='k') + 3)
E(L, 'screens[5].feedback.byKey.five', 9); E(L, 'quiz[2].widget.answer', 5); E(L, 'quiz[2].widget.wrong[1].value', 3 + 6 / 5)
# normal shocks fatten tails
pers = 0.98; th = 3 * (1 - pers ** 2) / (1 - pers ** 2 - 2 * 0.08 ** 2) - 3
for p in ('screens[7].prose', 'screens[7].explain.text', 'screens[7].canvas.state.caption'):
    E(L, p, R(th, 2))
order = np.argsort(-np.abs(r))
for i, k in enumerate([0, 1, 2, 3, 5, 10]):
    E(L, f'screens[7].canvas.params.rows[{i}][1]', f'{exkurt(np.delete(r, order[:k])):.2f}')
claim('five days carry about a third of 3.01', 0.3 < (kB - exkurt(np.delete(r, order[:5]))) / kB < 0.36)
E(L, 'screens[7].widget.options[3].why', R(kB - exkurt(np.delete(r, order[:1])), 1))
# 50-day blocks
bk = [exkurt(b) for b in np.array_split(r, 40)]
for i in range(40):
    E(L, f'screens[8].canvas.state.values.{i + 1}', R(bk[i], 3))
for p in ('screens[8].explain.text', 'screens[8].widget.options[1].why', 'quiz[3].widget.options[1].why', 'quiz[3].explain.text'):
    E(L, p, R(min(bk), 2)); E(L, p, R(max(bk), 2))
E(L, 'screens[8].explain.text', sum(b < 0 for b in bk)); E(L, 'screens[8].hints[1].text', sum(b < 0 for b in bk))
claim('every 50-day block is below 3.01', max(bk) < kB)
t4 = np.random.default_rng(12).standard_t(4, 100000)
for n_ in (1000, 10000, 50000, 100000):
    E(L, 'screens[8].explain.text', R(exkurt(t4[:n_]) + 3, 1))
# tail counts
for i, k in enumerate([2, 3, 4, 5]):
    E(L, f'screens[9].canvas.params.rows[{i}][1]', int(np.sum(np.abs(r - r.mean()) > k * sB)))
for i, (k, f) in enumerate([(2, '{:.1f}'), (4, '{:.2f}'), (5, '{:.4f}')]):
    E(L, f'screens[9].canvas.params.rows[{[0, 2, 3][i]}][2]', f.format(2000 * 2 * stats.norm.sf(k)))
E(L, 'screens[9].explain.text', R(2000 * 2 * stats.norm.sf(3), 2)); E(L, 'screens[9].explain.text', R(2000 * 2 * stats.norm.sf(4), 2))
# 5-sigma
p5 = 2 * stats.norm.sf(5); yrs = 1 / p5 / 252
E(L, 'screens[11].prose', R(p5 * 1e7, 2)); E(L, 'screens[11].widget.answer', round(yrs))
E(L, 'screens[11].widget.wrong[0].value', round(1 / p5)); E(L, 'screens[11].widget.wrong[1].value', round(2 * yrs)); E(L, 'screens[11].widget.wrong[2].value', round(1 / p5 / 365))
E(L, 'screens[11].hints[2].text', round(yrs, -1)); E(L, 'screens[11].explain.text', round(yrs, -1))
E(L, 'screens[11].prose', int(np.sum(np.abs(r - r.mean()) > 5 * sB))); E(L, 'screens[11].explain.text', round(2000 / 252))
# quizzes
x4 = np.array([1, -1, 3, -3.0]); E(L, 'quiz[0].widget.answer', exkurt(x4) + 3); E(L, 'quiz[0].widget.wrong[0].value', R(exkurt(x4), 2))
E(L, 'quiz[0].widget.wrong[1].value', R(np.mean(x4 ** 4) / (np.sum(x4 ** 2) / 3) ** 2, 4))
E(L, 'quiz[1].widget.answer', R(4.2 - 3, 1)); E(L, 'quiz[1].widget.wrong[1].value', 7.2)

# ================= l4 realised vol =================
L = 'l4'
an = {w: np.std(r[-w:], ddof=1) * S252 for w in (5, 20, 60, 250)}
zm = {w: math.sqrt(np.mean(r[-w:] ** 2)) * S252 for w in (5, 20, 60, 250)}
for i, w in enumerate((5, 20, 60, 250)):
    for p in (f'screens[0].canvas.params.rows[{i}][2]', f'screens[3].canvas.params.rows[{i}][1]', f'screens[5].canvas.params.rows[{i}][1]'):
        E(L, p, f'{100 * an[w]:.2f}%')
    for p in (f'screens[3].canvas.params.rows[{i}][2]', f'screens[5].canvas.params.rows[{i}][2]'):
        E(L, p, f'{100 * zm[w]:.2f}%')
    E(L, 'screens[5].prose', R(an[w], 4)); E(L, 'summary.ideas[0]', R(100 * an[w], 1))
E(L, 'screens[0].widget.options[2].why', 'a third')
two('1/sqrt(10) is about a third', round(1 / math.sqrt(10), 1), 0.3)
d20 = np.std(r[-20:], ddof=1)
E(L, 'screens[2].prose', R(100 * d20, 4)); E(L, 'screens[2].widget.answer', R(d20 * S252, 4))
E(L, 'screens[2].widget.wrong[0].value', R(d20 * math.sqrt(365), 4)); E(L, 'screens[2].widget.wrong[1].value', R(d20 * 252, 3))
E(L, 'screens[2].widget.wrong[2].value', R(d20, 6)); E(L, 'screens[2].hints[2].text', R(S252, 2))
m5 = np.mean(r[-5:])
E(L, 'screens[3].widget.options[0].text', R(100 * abs(m5), 2))
for p in ('screens[3].hints[1].text', 'screens[3].explain.text', 'screens[3].hints[2].text'):
    E(L, p, R(100 * m5, 2))
E(L, 'screens[3].widget.options[1].why', round(100 * (math.sqrt(5 / 4) - 1))); E(L, 'screens[3].widget.options[1].why', round(100 * (zm[5] / an[5] - 1)))
claim('-0.89% is larger than the 5-day sd left around it', abs(m5) > an[5] / S252)
claim('60 and 250 days agree to under 0.1 points', max(abs(an[60] - zm[60]), abs(an[250] - zm[250])) < 0.001)
for i, n_ in [(0, 5), (1, 20), (3, 250)]:
    E(L, f'screens[4].widget.rows[{i}][1].answer', R(1 / math.sqrt(2 * n_), 4))
E(L, 'screens[4].widget.rows[2][1]', f'{100 / math.sqrt(120):.2f}%')
E(L, 'screens[4].feedback.correct', R(15 / math.sqrt(500), 1))
E(L, 'screens[5].explain.text', R(100 * 0.02 * math.sqrt(52), 2))
# RMSE against the true variance, days 250 to 1,999, estimate from days t - w to t - 1
s2p = 1e4 * s2; rp = 100 * r
ws = [5, 10, 15, 20, 30, 40, 60, 90, 120, 180, 250]


def rmse(w, x=rp, tv_=s2p, start=250):
    est = np.array([np.var(x[t - w:t], ddof=1) for t in range(start, len(x))])
    return math.sqrt(np.mean((est - tv_[start:]) ** 2))


err = {w: rmse(w) for w in ws}
pts4 = {p['id']: p for p in lv._file(L)[1]['screens'][6]['canvas']['state']['points']}
for w in ws:
    two(f'l4 s6 plotted RMSE w={w}', pts4[f'w{w}'].get('y'), err[w], 2e-3)
E(L, 'screens[6].hints[2].text', R(err[20], 3)); claim('w20 is the minimum of the plotted windows', min(err, key=err.get) == 20)
claim('w5 more than twice the minimum', err[5] > 2 * err[20]); claim('w250 the largest', max(err, key=err.get) == 250)
claim('w15 noisier than 20 and w30 slower', err[15] > err[20] and err[30] > err[20])


def best(x, tv_, windows):
    st = max(windows)
    e = {w: np.mean((np.array([np.var(x[t - w:t], ddof=1) for t in range(st, len(x))]) - tv_[st:]) ** 2) for w in windows}
    return min(e, key=e.get)


b_all = best(r, s2, list(range(5, 251)))
for p in ('screens[6].explain.text', 'screens[7].feedback.correct'):
    E(L, p, b_all)
claim('A picks 250', best(iid, np.full(2000, 1e-4), [5, 10, 20, 40, 60, 90, 120, 180, 250]) == 250)
E(L, 'summary.ideas[2]', b_all)
# trap
for i, v in enumerate([S252, math.sqrt(365), math.sqrt(1e-4 * S252) * 100, 252]):
    E(L, f'screens[8].widget.options[{i}].text', f'{v:.2f}%' if i < 3 else '252%')
E(L, 'screens[8].hints[1].text', 252 * 1e-4); E(L, 'screens[8].hints[2].text', R(math.sqrt(0.0252), 4))
# the ghost
gA = rolling_sd(A10, 20) * S252
E(L, 'screens[9].explain.text', R(100 * gA[999], 1)); E(L, 'screens[9].explain.text', R(100 * gA[1000], 1)); E(L, 'screens[9].explain.text', R(100 * gA[1020], 1))
claim('the 20-day figure holds until day 1,019 and drops on 1,020', abs(gA[1019] - gA[1000]) < 0.01 and gA[1020] < gA[999])
# transfer: implied vol of the trees call at 12.00


def bs(S, K, rr, T, sig):
    d1 = (math.log(S / K) + (rr + sig ** 2 / 2) * T) / (sig * math.sqrt(T))
    return S * stats.norm.cdf(d1) - K * math.exp(-rr * T) * stats.norm.cdf(d1 - sig * math.sqrt(T))


from scipy.optimize import brentq  # noqa: E402
iv = brentq(lambda s: bs(100, 100, 0.05, 1, s) - 12.0, 0.01, 1)
E(L, 'screens[11].prose', R(100 * iv, 1))
# quizzes
E(L, 'quiz[0].widget.answer', R(0.02 * math.sqrt(52), 4)); E(L, 'quiz[0].widget.wrong[0].value', R(0.02 * S252, 4)); E(L, 'quiz[0].widget.wrong[1].value', 1.04)
E(L, 'quiz[1].widget.answer', R(0.10 / S252, 4)); E(L, 'quiz[1].widget.accept', R(10 / S252, 3))
E(L, 'quiz[1].widget.wrong[0].value', R(0.10 / 252, 6)); E(L, 'quiz[1].widget.wrong[1].value', R(0.10 / math.sqrt(365), 5))
E(L, 'quiz[2].widget.answer', R(20 / math.sqrt(120), 2)); E(L, 'quiz[2].widget.wrong[0].value', R(20 / math.sqrt(60), 2)); E(L, 'quiz[2].widget.wrong[1].value', R(100 / math.sqrt(120), 2))

# ================= review-1 =================
L = 'review'
E(L, 'items[0].feedback.byKey.three', R(1 / 0.03, 1)); E(L, 'items[0].feedback.byKey.three', 3)   # fix pass 17
E(L, 'items[0].widget.answer', R(1 / 0.03, 1)); E(L, 'items[0].widget.wrong[1].value', 3)
x10 = np.array([0] * 8 + [3, -3.0])
E(L, 'items[2].widget.answer', exkurt(x10)); E(L, 'items[2].widget.wrong[0].value', exkurt(x10) + 3)
E(L, 'items[2].widget.wrong[1].value', R(np.mean(x10 ** 4) / (np.sum(x10 ** 2) / 9) ** 2 - 3, 2))
E(L, 'items[3].widget.answer', R(0.015 * S252, 4)); E(L, 'items[3].widget.wrong[0].value', R(0.015 * math.sqrt(365), 4)); E(L, 'items[3].widget.wrong[1].value', 0.015 * 252)
P = [1.02, 0.97, 1.00, 1.03]
claim('review-1 items[4] P within 6% of its mean', (max(P) - min(P)) / np.mean(P) <= 0.06)
E(L, 'items[5].widget.answer', 1990 * 0.05); E(L, 'items[5].widget.wrong[1].value', 10 * 0.05); E(L, 'items[5].feedback.correct', R(crit10, 2))
E(L, 'items[6].widget.answer', 2500 * 0.0027); E(L, 'items[6].widget.wrong[0].value', 1250 * 0.0027); E(L, 'items[6].widget.wrong[1].value', R(30 / 6.75, 2))
E(L, 'items[7].widget.options[2].why', R(th, 2))
E(L, 'items[8].widget.answer', R(18 / math.sqrt(500), 1)); E(L, 'items[8].widget.accept', R(18 / math.sqrt(500), 2))
E(L, 'items[8].widget.wrong[0].value', R(18 / math.sqrt(250), 2)); E(L, 'items[8].widget.wrong[1].value', R(100 / math.sqrt(500), 2))
claim('review-1 items[9]: B 250-day error more than twice the 20-day error', err[250] > 2 * err[20])

# ================= homework-1 =================
L = 'homework'
E(L, 'items[1].widget.answer', R(0.20 / math.sqrt(52), 4)); E(L, 'items[1].widget.wrong[0].value', R(0.20 / S252, 4)); E(L, 'items[1].widget.wrong[1].value', R(0.20 / 52, 4))
E(L, 'items[3].widget.examples[0].expect', R(rq, 3)); E(L, 'items[3].widget.examples[0].expect', n3); E(L, 'items[3].widget.examples[0].expect', R(n3 / (2000 * p3), 2))
nA3 = int(np.sum(np.abs(iid - iid.mean()) > 3 * np.std(iid, ddof=1)))
E(L, 'items[3].explain.text', R(nA3 / (2000 * p3), 2)); E(L, 'items[3].explain.text', R(rqA, 4))
E(L, 'items[4].explain.text', R(stats.chi2.sf(3.2, 5), 2)); E(L, 'items[4].question', R(stats.chi2.ppf(0.95, 5), 2))
E(L, 'items[6].widget.answer', R(math.sqrt(3 / 5), 4)); E(L, 'items[6].widget.wrong[1].value', R(math.sqrt(5 / 3), 3)); E(L, 'items[6].explain.text', 9)
for v in (R(Q, 2), R(pQ, 2), R(Qs, 2), R(lmB, 1), R(sq[0], 2), R(band, 4), round(100 * after_big), R(100 * nB['any'][2], 1),
          R(kB, 2), R(kB + 3, 2), n3, R(2000 * p3, 1), R(100 * true1404, 1), R(100 * w250, 1), R(100 * w20, 1), R(exkurt(np.delete(r, order[:5])), 2)):
    E(L, 'items[7].model', v)
E(L, 'items[7].model', 'about 6,900 years'); E(L, 'items[7].model', '3 \\times 10^{-93}') if f'{plB:.0e}' == '3e-93' else claim('ARCH-LM p about 3e-93', False)

lv.check_wrongs()
for f in fails:
    print('BAD', f)
if fails:
    lv.results.append((False, 'route agreement', ''))
lv.report()
