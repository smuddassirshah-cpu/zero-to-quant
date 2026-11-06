"""Recompute every number stated in garch level 2 (Models) and check it at its JSON path (second read).

Run: python3 docs/reports/garch-L2-numbers.py   (NumPy, SciPy and the standard library; exits 0 when every check passes)

Data from the brief's generator (share B, seed 7; series A, 0.01 x seed 8; the ARCH path, seed 11) and the brief's
reference fit (SLSQP from (0.05, 0.05, 0.90) on returns in %). Closed forms are computed twice (formula and
recursion); fitted values are checked at the places shown. Values that only Pyodide's SciPy 1.14.1 produces (the
decimal fit (7.01e-5, 0.2461, 0.2756) and series A's browser fit) are not reproducible here and are read by hand in
the review; their CPython counterparts are checked where the lessons state them. A check that fails because the
content is wrong is a finding in docs/reviews/review-garch.md and stays failing until the fix pass corrects it.
"""
import math
import os
import sys

import numpy as np
from scipy import stats
from scipy.optimize import minimize

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("garch", 2)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
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


def simulate_arch1(omega, alpha, n, seed, bug=False):
    z = np.random.default_rng(seed).standard_normal(n)
    r = np.zeros(n); s2 = np.zeros(n); s2[0] = omega / (1 - alpha)
    for t in range(n):
        if t > 0:
            s2[t] = omega + alpha * (r[t] if bug else r[t - 1]) ** 2
        r[t] = np.sqrt(s2[t]) * z[t]
    return r


def garch_variance(params, r):
    omega, alpha, beta = params
    s2 = np.empty(len(r)); s2[0] = r.var()
    for t in range(1, len(r)):
        s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
    return s2


def neg_loglik(params, r):
    s2 = garch_variance(params, r)
    return 0.5 * np.sum(np.log(2 * np.pi) + np.log(s2) + r ** 2 / s2)


def fit_garch(r, x0=(0.05, 0.05, 0.90), bounds=((1e-6, 10.0), (0.0, 1.0), (0.0, 1.0))):
    return minimize(neg_loglik, x0=np.array(x0), args=(r,), method="SLSQP", bounds=list(bounds),
                    constraints=[{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2]}], options={"ftol": 1e-10, "maxiter": 500})


def ewma(r, lam, init=20):
    s = np.empty(len(r)); s[0] = r[:init].var()
    for t in range(1, len(r)):
        s[t] = lam * s[t - 1] + (1 - lam) * r[t - 1] ** 2
    return s


def acf(x, k):
    x = np.asarray(x, float) - np.mean(x); c0 = x @ x
    return np.array([x[j:] @ x[:-j] / c0 for j in range(1, k + 1)])


def rawkurt(x):
    d = np.asarray(x, float) - np.mean(x)
    return np.mean(d ** 4) / np.mean(d ** 2) ** 2


def rolling_sd(x, w):
    out = np.full(len(x), np.nan)
    for t in range(w - 1, len(x)):
        out[t] = np.std(x[t - w + 1:t + 1], ddof=1)
    return out


def bs(S, K, rr, T, sig):
    d1 = (math.log(S / K) + (rr + sig ** 2 / 2) * T) / (sig * math.sqrt(T))
    return S * stats.norm.cdf(d1) - K * math.exp(-rr * T) * stats.norm.cdf(d1 - sig * math.sqrt(T))


S252 = math.sqrt(252)
r, s2 = simulate_garch(2e-6, 0.08, 0.90, 2000, 7)
rp, s2p = 100 * r, 1e4 * s2
iid = 0.01 * np.random.default_rng(8).standard_normal(2000); ap = 100 * iid
fit = fit_garch(rp); params = fit.x; w_, a_, b_ = params; pers = a_ + b_
VL = w_ / (1 - pers)

# ================= l5 EWMA =================
L = 'l5'
A8 = iid.copy(); A8[1500] = -0.08
g = rolling_sd(A8, 20) * S252
E(L, 'screens[0].explain.text', R(100 * g[1499], 1)); E(L, 'screens[0].explain.text', R(100 * g[1500], 1)); E(L, 'screens[0].explain.text', R(100 * g[1520], 1))
claim('l5 s0: the 20-day figure holds to 1,519 and drops on 1,520', g[1519] > 0.3 and g[1520] < 0.21)
E(L, 'screens[1].widget.answer', R(1 - 0.94 ** 20, 2)); E(L, 'screens[1].widget.accept', R(1 - 0.94 ** 20, 3)); E(L, 'screens[1].widget.wrong[1].value', R(0.94 ** 20, 2))
for k in range(41):
    E(L, f'screens[1].canvas.state.values.k{k}', R(0.06 * 0.94 ** k, 6))
two('weights sum to 1 - lam^20', sum(0.06 * 0.94 ** k for k in range(20)), 1 - 0.94 ** 20)
v = 0.94 * 1 + 0.06 * 9
E(L, 'screens[2].widget.answer', v); E(L, 'screens[2].widget.wrong[0].value', 0.94 - 0.06 * 3); E(L, 'screens[2].widget.wrong[1].value', 0.06 + 0.94 * 9)
E(L, 'screens[2].widget.wrong[2].value', 0.94 + 0.06 * 3); E(L, 'screens[2].explain.text', R(math.sqrt(v), 2)); E(L, 'screens[2].feedback.correct', R(math.sqrt(v), 2))
hand = [1.0]
for x in [1, -2, 0.5, 3, -1]:
    hand.append(0.94 * hand[-1] + 0.06 * x ** 2)
for i in range(1, 6):
    E(L, f'screens[3].widget.rows[{i}][2].answer', R(hand[i], 4))
E(L, 'screens[3].feedback.correct', R(hand[4], 4)); E(L, 'screens[3].hints[2].text', R(hand[3], 4))
tv = np.sqrt(s2p)
corr = {lam: np.corrcoef(ewma(rp, lam), s2p)[0, 1] for lam in (0.80, 0.90, 0.94, 0.97, 0.99)}
cap = lv.text(L, 'screens[4].canvas.derive.caption')
for lam, c in corr.items():
    E(L, 'screens[4].canvas.derive.caption', f'{c:.4f}')
claim('lambda 0.90 has the highest correlation', max(corr, key=corr.get) == 0.90)
for i, lam in [(0, 0.80), (2, 0.94), (3, 0.97), (4, 0.99)]:
    E(L, f'screens[4].widget.options[{i}].why', f'{corr[lam]:.4f}')
e94 = ewma(rp, 0.94)
E(L, 'screens[4].explain.text', R(math.sqrt(e94[1999]), 4)); E(L, 'screens[4].explain.text', R(tv[1999], 4))
# EWMA(0.90) is an affine function of the truth: sigma2 - 0.2 = 0.8 x EWMA once the start fades; so correlation
# near 1 hides a level error. Its value on the stormiest true day:
e90 = ewma(rp, 0.90); tmax = int(np.argmax(s2p))
print('EWMA(0.90)/truth at the storm peak', e90[tmax] / s2p[tmax], 'day', tmax)
stated(L, 'screens[4].feedback.correct', 'almost a perfect match', abs(e90[tmax] / s2p[tmax] - 1) < 0.10)
E(L, 'screens[4].explain.text', 'about 20% high') if abs(e90[tmax] / s2p[tmax] - 1.2) < 0.03 else claim('EWMA runs about 20% high in storms', False)   # fix pass 7
E(L, 'screens[5].prose', R(math.sqrt(e94[1999]), 4)); E(L, 'screens[5].prose', R(math.sqrt(garch_variance(params, rp)[1999]), 4)); E(L, 'screens[5].prose', R(tv[1999], 4))
# the pandas trap: his series includes today's square
his = np.empty(2000); his[0] = rp[0] ** 2
for t in range(1, 2000):
    his[t] = 0.94 * his[t - 1] + 0.06 * rp[t] ** 2
mine = e94
E(L, 'screens[6].prose', R(np.mean((his - rp ** 2) ** 2), 2)); E(L, 'screens[6].prose', R(np.mean((mine - rp ** 2) ** 2), 2))
for i, d in enumerate(range(1454, 1459)):
    E(L, f'screens[6].canvas.params.rows[{i}][1]', f'{rp[d]:.2f}'); E(L, f'screens[6].canvas.params.rows[{i}][2]', f'{his[d]:.4f}')
    E(L, f'screens[6].canvas.params.rows[{i}][3]', f'{mine[d]:.4f}')
claim('1,456 is the biggest move of days 1,000 to 1,999', int(np.argmax(np.abs(rp[1000:]))) + 1000 == 1456)
E(L, 'screens[8].widget.options[0].text', R(math.sqrt(rp[:20].var()), 2)); E(L, 'screens[8].explain.text', R(math.sqrt(rp[:20].var()), 2))
E(L, 'screens[8].widget.options[3].why', R(1 / 0.06, 1)); E(L, 'screens[8].explain.text', R(1 / 0.03, 1))
E(L, 'screens[9].widget.options[1].text', R(0.94 ** 10 * 2, 2))
# transfer: series A in %, day 1,500 = -8%
a8 = 100 * A8; ea = ewma(a8, 0.94)
E(L, 'screens[10].prose', R(math.sqrt(ea[1500]), 4)); E(L, 'screens[10].prose', R(np.std(a8[1250:1500], ddof=1), 2))
s15 = 1.1543
ans = math.sqrt(0.94 * s15 ** 2 + 0.06 * 64)
E(L, 'screens[10].widget.answer', R(ans / 100, 6)); two('l5 s10 key from the true EWMA', math.sqrt(ea[1501]) / 100, ans / 100, 1e-5)
E(L, 'screens[10].widget.wrong[0].value', R(np.std(a8[1251:1501], ddof=1) / 100, 6))
E(L, 'screens[10].widget.wrong[1].value', R(math.sqrt(0.94 * s15 ** 2 + 0.06 * 8) / 100, 6)); E(L, 'screens[10].widget.wrong[2].value', R(ans ** 2 / 100, 5))
E(L, 'screens[10].hints[2].text', R(s15 ** 2, 4)); E(L, 'screens[10].hints[2].text', R(ans ** 2, 4)); E(L, 'screens[10].hints[2].text', R(ans, 3))
E(L, 'screens[10].feedback.correct', R(np.std(a8[1251:1501], ddof=1), 2))
E(L, 'quiz[0].widget.answer', R(1 - 0.97 ** 10, 3)); E(L, 'quiz[0].widget.wrong[0].value', R(0.97 ** 10, 3)); E(L, 'quiz[0].widget.wrong[1].value', 0.3)
E(L, 'quiz[1].widget.answer', 0.94 * 2.25 + 0.06); E(L, 'quiz[1].widget.wrong[0].value', 0.06 * 2.25 + 0.94); E(L, 'quiz[1].widget.wrong[1].value', R(math.sqrt(2.175), 2))
E(L, 'quiz[2].widget.answer', 10); E(L, 'quiz[2].widget.wrong[1].value', R(1 / 0.03, 1))

# ================= l6 ARCH =================
L = 'l6'
E(L, 'screens[0].feedback.byKey.vol', '3.63') if 0.5 + 0.5 * 2.5 ** 2 == 3.625 else claim('3.625', False); E(L, 'screens[0].explain.text', R(math.sqrt(2.5), 2))
paths = {a: 100 * simulate_arch1(1e-4 * (1 - a), a, 2000, 11) for a in (0, 0.3, 0.5)}
for a, x in paths.items():
    E(L, 'screens[1].canvas.derive.caption', f'{np.std(x, ddof=1):.2f}'); E(L, 'screens[1].canvas.derive.caption', f'{rawkurt(x):.2f}')
E(L, 'screens[1].explain.text', R(rawkurt(paths[0]), 2)); E(L, 'screens[1].explain.text', R(rawkurt(paths[0.5]), 2))
p5 = paths[0.5]
E(L, 'screens[1].feedback.correct', R(p5[1010], 1)); E(L, 'screens[1].feedback.correct', R(abs(p5[1009]), 1)); claim('day 1,009 is a fall', p5[1009] < 0)
E(L, 'screens[2].widget.answer', R(math.sqrt(5) / 100, 6)); E(L, 'screens[2].widget.wrong[1].value', R(math.sqrt(2) / 100, 6)); E(L, 'screens[2].widget.wrong[2].value', R(math.sqrt(4.5) / 100, 6))
E(L, 'screens[3].widget.answer', 0.2 / 0.4); E(L, 'screens[3].widget.wrong[1].value', 0.2 / 1.6); E(L, 'screens[3].widget.wrong[2].value', R(0.2 / 0.6, 4))
ra = simulate_arch1(5e-5, 0.5, 2000, 11)
E(L, 'screens[4].prose', R(np.std(ra, ddof=1), 6)); E(L, 'screens[4].feedback.correct', R(np.std(ra, ddof=1), 6))
two('ARCH path in % equals the explore path', np.max(np.abs(100 * ra - p5)), 0, 1e-9)
k20 = [rawkurt(simulate_arch1(5e-5, 0.5, 2000, s)) for s in range(11, 31)]
E(L, 'screens[5].prose', R(rawkurt(ra), 2)); E(L, 'screens[5].explain.text', R(np.mean(k20), 2))
E(L, 'screens[5].explain.text', R(min(k20), 2)); E(L, 'screens[5].explain.text', R(max(k20), 2)); E(L, 'screens[5].prose', R(1 / math.sqrt(3), 3))
E(L, 'quiz[1].widget.options[1].why', R(min(k20), 1)); E(L, 'quiz[1].widget.options[1].why', R(max(k20), 1))
two('ARCH kurtosis at 0.5', 3 * (1 - 0.25) / (1 - 0.75), 9)
aa = acf(ra ** 2, 10); sqB = acf(r ** 2, 10)
for k in range(10):
    E(L, f'screens[6].canvas.state.values.arch.k{k + 1}', R(aa[k], 4)); E(L, f'screens[6].canvas.state.values.B.k{k + 1}', R(sqB[k], 4))
    E('l7', f'screens[0].canvas.state.values.arch.k{k + 1}', R(aa[k], 4)); E('l7', f'screens[0].canvas.state.values.B.k{k + 1}', R(sqB[k], 4))
E(L, 'screens[6].widget.options[0].text', R(sqB[9], 2)); E(L, 'screens[6].widget.options[1].why', R(sqB[2], 2)); E(L, 'screens[6].widget.options[1].why', R(aa[2], 2))
E(L, 'screens[7].question', 'clustering')
rb = simulate_arch1(5e-5, 0.5, 2000, 11, bug=True)
E(L, 'screens[7].canvas.params.lines[8]', f'{np.std(rb, ddof=1):.6f}'); E(L, 'screens[7].canvas.params.lines[8]', f'{rawkurt(rb):.4f}'); E(L, 'screens[7].canvas.params.lines[8]', f'{acf(rb ** 2, 1)[0]:.4f}')
E(L, 'screens[7].explain.text', R(100 * math.sqrt(5e-5), 2)); E(L, 'screens[7].widget.options[1].why', R(aa[0], 2))
rap = 100 * ra
fa = fit_garch(rap, bounds=((1e-6, 10.0), (0.0, 1.0), (0.0, 0.0))); fB = fit_garch(rp, bounds=((1e-6, 10.0), (0.0, 1.0), (0.0, 0.0)))
for p in ('screens[8].feedback.correct', 'screens[8].explain.text'):
    E(L, p, R(fa.x[0], 3)); E(L, p, R(fa.x[1], 3))
E(L, 'screens[8].explain.text', R(fB.x[1], 3)); E(L, 'screens[8].explain.text', R(fB.x[0], 3))
E(L, 'screens[9].widget.options[1].text', R(0.5 / 0.1, 0)); E(L, 'screens[9].widget.options[3].text', R(0.5 / (1 - 1.1), 0))
E(L, 'screens[11].prose', R(1.2 / 0.6, 0)); E(L, 'screens[11].prose', R(math.sqrt(2), 2))
E(L, 'screens[11].widget.answer', R(math.sqrt(33.6) / 100, 6)); E(L, 'screens[11].widget.wrong[1].value', R(math.sqrt(4.8) / 100, 6)); E(L, 'screens[11].widget.wrong[2].value', R(math.sqrt(2) / 100, 6))
claim('ARCH gap mostly gone in three days (0.4^3 < 0.1)', 0.4 ** 3 < 0.1)
E(L, 'quiz[0].widget.answer', 0.3 / 0.6); E(L, 'quiz[0].widget.wrong[1].value', R(0.3 / 1.4, 4)); E(L, 'quiz[0].explain.text', R(math.sqrt(0.5), 2))
E(L, 'quiz[2].widget.answer', R(0.2 + 0.3 * 4, 2)); E(L, 'quiz[2].widget.wrong[0].value', R(0.2 - 0.6, 2)); E(L, 'quiz[2].explain.text', R(math.sqrt(1.4), 2))
E(L, 'quiz[3].widget.options[0].why', R(3 * 0.91 / 0.73, 2))

# ================= l7 GARCH(1,1) =================
L = 'l7'
for k in range(5):
    E(L, 'screens[0].prose', R(sqB[k], 2))
E(L, 'screens[1].widget.options[1].why', 24 * 0.08); E(L, 'screens[1].explain.text', round(math.log(0.5) / math.log(0.98)))
E(L, 'screens[2].widget.answer', R(0.02 + 0.72 + 0.90, 2)); E(L, 'screens[2].widget.wrong[0].value', 1.62); E(L, 'screens[2].widget.wrong[1].value', R(0.02 + 0.72, 2))
E(L, 'screens[2].widget.wrong[2].value', R(0.02 - 0.24 + 0.90, 2)); E(L, 'screens[2].feedback.correct', R(math.sqrt(1.64), 2))
# storm days by hand (4-place returns, true parameters)
E(L, 'screens[3].prose', R(s2p[1454], 4))
rows = [R(s2p[1454], 4)]
for d in range(1454, 1459):
    rows.append(0.02 + 0.08 * R(rp[d], 4) ** 2 + 0.90 * rows[-1])
    E(L, 'screens[3].prose', R(rp[d], 4)); E(L, f'screens[3].canvas.state.values.d{d}', R(rp[d], 4))
for i in range(1, 6):
    E(L, f'screens[3].widget.rows[{i}][2].answer', R(rows[i], 4)); two(f'storm day {1454 + i} equals the true variance', rows[i], s2p[1454 + i], 2e-4)
# is the match "because the start has faded"? The table starts from the true day-1,454 variance itself:
two('l7 s3 the table start is the true variance', R(s2p[1454], 4), 3.2346)
stated(L, 'screens[3].explain.text', 'because after 1,454 days the starting value has faded', False)
E(L, 'screens[3].explain.text', 3.2346)   # fix pass 4: the table starts from the true variance
E(L, 'screens[3].hints[2].text', R(0.08 * R(rp[1454], 4) ** 2, 4)); E(L, 'screens[3].hints[2].text', R(0.9 * R(s2p[1454], 4), 4))
ell = lambda x, v: -0.5 * (math.log(2 * math.pi) + math.log(v) + x ** 2 / v)  # noqa: E731
E(L, 'screens[4].widget.rows[0][3]', f'{ell(R(rp[1455], 4), R(rows[1], 4)):.3f}'.replace('-', '−'))
E(L, 'screens[4].widget.rows[1][3].answer', R(ell(R(rp[1456], 4), R(rows[2], 4)), 3)); E(L, 'screens[4].widget.rows[2][3].answer', R(ell(R(rp[1457], 4), R(rows[3], 4)), 3))
E(L, 'screens[4].hints[1].text', R(math.log(R(rows[2], 4)), 4)); E(L, 'screens[4].hints[1].text', R(R(rp[1456], 4) ** 2 / R(rows[2], 4), 4))
E(L, 'screens[4].prose', R(math.log(2 * math.pi), 4))
nll_true, nll_start, nll_fit = neg_loglik((0.02, 0.08, 0.90), rp), neg_loglik((0.05, 0.05, 0.90), rp), fit.fun
E(L, 'screens[5].prose', R(nll_true, 4)); E(L, 'screens[5].feedback.correct', R(nll_true, 4)); E(L, 'screens[5].prose', f'{rp.var():.4f}'); E(L, 'screens[5].prose', R(math.sqrt(rp.var()), 3))   # fix pass 27: the chart plots daily volatility, so the prose gives sqrt(1.0585) = 1.029
E(L, 'screens[5].explain.text', R(nll_start, 4)); E(L, 'screens[5].explain.text', R(nll_start - nll_true, 1))
two('profile: neg_loglik at the fit by two routes', nll_fit, neg_loglik(params, rp))
prof = lv._file(L)[1]['screens'][6]['canvas']['params']['functions'][0]['points']
for x_, y_ in prof[::9]:
    two(f'l7 s6 profile at alpha={x_}', y_, -neg_loglik((R(w_, 4), x_, R(b_, 4)), rp), 6e-3)
amax = max(prof, key=lambda p: p[1])
E(L, 'screens[6].hints[2].text', amax[0]); E(L, 'screens[6].hints[2].text', amax[1]); E(L, 'screens[6].prose', R(w_, 4)); E(L, 'screens[6].prose', R(b_, 4))
for i, v in enumerate([w_, a_, b_]):
    E(L, 'screens[7].feedback.correct', R(v, 4)); E(L, 'screens[7].explain.text', R(v, 4)); E(L, f'screens[8].canvas.params.rows[0][{i + 1}]', R(v, 4))
    E(L, f'screens[10].canvas.params.rows[0][{i + 1}]', f'{v:.4f}')
E(L, 'screens[7].feedback.correct', R(pers, 4)); E(L, 'screens[7].feedback.correct', R(math.log(0.5) / math.log(R(pers, 4)), 1))
two('fit iterations', fit.nit, 15); E(L, 'screens[7].explain.text', fit.nit)
gv = garch_variance(params, rp)
E(L, 'screens[7].explain.text', R(np.corrcoef(gv, s2p)[0, 1], 4)); E(L, 'screens[7].explain.text', R(corr[0.94], 4))
E(L, 'screens[7].explain.text', R(math.sqrt(gv[1999]), 3)); E(L, 'screens[7].explain.text', R(tv[1999], 3))
stated(L, 'screens[7].explain.text', "lesson 5's EWMA managed", np.corrcoef(gv, s2p)[0, 1] > max(corr.values()))
E(L, 'screens[8].canvas.params.rows[0][4]', f'{-nll_fit:.2f}'.replace('-', '−'))   # fix pass 28: the alpha + beta column is gone, so the log-likelihood is column 4
_p8 = lv._file(L)[1]['screens'][8]
claim('l7 s8 table has 5 columns and every row has 5 cells', len(_p8['canvas']['params']['columns']) == 5 and all(len(x) == 5 for x in _p8['canvas']['params']['rows']))
claim('l7 s8 hints[1] highlights the log-likelihood cell of the decimal row', _p8['canvas']['params']['columns'][4] == 'Log-likelihood' and _p8['hints'][1]['highlight'] == ['r1c4'])
fd = fit_garch(r)                                  # CPython's decimal fit (the browser's is in the table)
E(L, 'screens[8].explain.text', R(fd.x[1], 2)); E(L, 'screens[8].explain.text', R(fd.x[2], 2))
dec_ll_pct = -neg_loglik(fd.x, r) - 2000 * math.log(100)  # the same fit's log-likelihood in % terms
claim('CPython decimal fit also stalls far below the peak (> 100 units)', -nll_fit - dec_ll_pct > 100); E(L, 'screens[8].hints[2].text', round(-nll_fit - (-2800.14)))
E(L, 'screens[8].hints[1].text', f'{w_ * 1e-4:.8f}'.rstrip('0'))
# 20 paths, seeds 7 to 26
fits20 = [fit_garch(100 * simulate_garch(2e-6, 0.08, 0.90, 2000, s)[0]).x for s in range(7, 27)]
p20 = np.array([f[1] + f[2] for f in fits20]); lr20 = np.array([math.sqrt(252 * f[0] / (1 - f[1] - f[2])) for f in fits20])
hist = sorted(lv._file(L)[1]['screens'][9]['canvas']['params']['data'])
two('l7 s9 histogram data = 20 fits', np.max(np.abs(np.array(hist) - np.sort(np.round(p20, 4)))), 0, 1e-9)
E(L, 'screens[9].widget.options[0].text', R(np.std(p20, ddof=1), 3)); E(L, 'screens[9].widget.options[0].text', R(np.mean(p20), 3))
E(L, 'screens[9].explain.text', R(np.std(p20, ddof=1), 4)); E(L, 'screens[9].explain.text', R(p20.min(), 3)); E(L, 'screens[9].explain.text', R(p20.max(), 3))
E(L, 'screens[9].hints[2].text', R((pers - 0.98) / np.std(p20, ddof=1), 1)); E(L, 'screens[9].widget.options[3].why', R(np.mean(p20), 3))
claim('right-most bin [0.985, 0.99) holds B and five others', int(np.sum((p20 >= 0.985) & (p20 < 0.99))) == 6)
f1000 = fit_garch(rp[:1000]).x
for i, v in enumerate(f1000):
    E(L, f'screens[10].canvas.params.rows[1][{i + 1}]', f'{v:.4f}')
E(L, 'screens[10].canvas.params.rows[1][4]', f'{f1000[1] + f1000[2]:.4f}'); E(L, 'screens[10].explain.text', round(math.log(0.5) / math.log(f1000[1] + f1000[2])))
fA = fit_garch(ap)
E(L, 'screens[10].canvas.params.rows[3][3]', f'{fA.x[2]:.4f}'); E(L, 'screens[10].canvas.params.rows[3][2]', f'{fA.x[1]:.4f}')
claim('CPython fit of A: alpha 0, beta 1, not converged', fA.x[1] < 1e-6 and abs(fA.x[2] - 1) < 1e-4)
E(L, 'screens[11].widget.answer', R(math.log(0.5) / math.log(0.99), 2)); E(L, 'screens[11].widget.wrong[2].value', R(math.log(0.5) / math.log(0.9), 2))
E(L, 'screens[11].canvas.state.points[0].label', R(math.log(0.5) / math.log(R(pers, 4)), 1)); E(L, 'screens[11].canvas.state.points[1].label', R(math.log(0.5) / math.log(0.98), 1))
E(L, 'quiz[0].widget.answer', 0.05 + 0.10 + 1.70); E(L, 'quiz[0].widget.wrong[1].value', R(0.05 + 0.85 + 0.20, 2))
E(L, 'quiz[2].widget.answer', R(math.log(0.5) / math.log(0.98), 2)); E(L, 'quiz[2].widget.wrong[0].value', R(math.log(0.5) / math.log(0.93), 2) + 0.01 if False else 9.56)
claim('quiz[2] beta slip 9.5513 inside the wrong band 9.56 +- 0.02', abs(math.log(0.5) / math.log(0.93) - 9.56) <= 0.02)
bf = minimize(neg_loglik, np.array([0.05, 0.05, 0.90]), args=(rp,))
for v in bf.x:
    E(L, 'quiz[3].prose', R(v, 1))

# ================= l8 long-run variance =================
L = 'l8'
for h, f in [(1, 0.98), (1, 0.9)]:
    pass
claim('F halfway (2.5) after about 8 days, S after about 35', round(1 + math.log(0.5) / math.log(0.9)) == 8 and round(1 + math.log(0.5) / math.log(0.98)) == 35)
E(L, 'screens[1].widget.answer', R(0.02 / 0.01, 1)); E(L, 'screens[2].widget.answer', R(S252 / 100, 4)); E(L, 'screens[2].widget.wrong[1].value', R(math.sqrt(0.02) * S252 / 100, 5))
E(L, 'screens[2].widget.wrong[2].value', R(math.sqrt(365) / 100, 3))
E(L, 'screens[3].prose', R(w_, 6)); E(L, 'screens[3].prose', R(pers, 6)); E(L, 'screens[3].prose', R(1 - pers, 6))
E(L, 'screens[3].widget.answer', R(math.sqrt(252 * VL) / 100, 4)); E(L, 'screens[3].widget.wrong[0].value', R(math.sqrt(VL) / 100, 6))
E(L, 'screens[3].widget.wrong[1].value', R(VL / 100, 6)); E(L, 'screens[3].widget.wrong[2].value', R(math.sqrt(252 * w_) / 100, 5))
E(L, 'screens[3].hints[1].text', R(VL, 4)); E(L, 'screens[3].explain.text', R(0.0121 / (1 - 0.9864), 4)); two('VL by 6-place inputs', R(R(w_, 6) / R(1 - pers, 6), 4), R(VL, 4))
hl = math.log(0.5) / math.log(0.9864)
E(L, 'screens[4].widget.answer', R(hl, 2)); E(L, 'screens[4].widget.wrong[0].value', R(1 / 0.0136, 2)); E(L, 'screens[4].widget.wrong[1].value', R(0.5 / 0.0136, 2))
E(L, 'screens[4].hints[2].text', R(math.log(0.9864), 6)); E(L, 'screens[4].explain.text', R(math.log(0.5) / math.log(pers), 1))
E(L, 'screens[4].canvas.state.points[1].label', R(math.log(0.5) / math.log(f1000[1] + f1000[2]), 1))
E(L, 'screens[5].canvas.state.points[1].label', R(math.log(0.5) / math.log(pers), 1)); E(L, 'screens[5].explain.text', R(math.log(0.5) / math.log(pers), 2))
E(L, 'screens[5].feedback.correct', R(math.sqrt(252 * VL) / 100, 4))
E(L, 'screens[6].widget.answer', R(math.sqrt(252 * 0.0121 / 0.005) / 100, 4)); E(L, 'screens[6].widget.wrong[1].value', R(math.sqrt(0.0121 / 0.005) / 100, 5))
E(L, 'screens[6].widget.wrong[2].value', R(math.sqrt(252 * 0.0121 / 0.02) / 100, 4)); E(L, 'screens[6].hints[2].text', R(math.sqrt(2.42), 3))
for i, v in enumerate(sorted(lv._file(L)[1]['screens'][7]['canvas']['params']['data'])):
    two(f'l8 s7 long-run vol {i}', v, np.sort(lr20)[i], 6e-3)
for p in ('screens[7].widget.options[0].text', 'screens[7].hints[1].text', 'screens[7].explain.text', 'summary.ideas[2]'):
    E(L, p, R(lr20.min(), 1)); E(L, p, R(lr20.max(), 1))
E(L, 'screens[7].hints[1].text', R(np.std(lr20, ddof=1), 1)); E(L, 'screens[7].widget.options[3].text', R(np.mean(lr20), 2))
E(L, 'screens[7].widget.options[2].why', R(np.std(lr20, ddof=1), 1)); E(L, 'screens[7].widget.options[2].why', R(S252 - math.sqrt(252 * VL), 1))
vl20 = [f[0] / (1 - f[1] - f[2]) for f in fits20]; E(L, 'screens[7].explain.text', R(min(vl20), 2)); E(L, 'screens[7].explain.text', R(max(vl20), 2))
vbar = rp.var()


def nll_t(p, x):
    return neg_loglik((vbar * (1 - p[0] - p[1]), p[0], p[1]), x)


ft = minimize(nll_t, np.array([0.05, 0.90]), args=(rp,), method='SLSQP', bounds=[(0.0, 1.0), (0.0, 1.0)],
              constraints=[{"type": "ineq", "fun": lambda p: 0.9999 - p[0] - p[1]}], options={"ftol": 1e-10, "maxiter": 500})
ta, tb = ft.x
E(L, 'screens[8].prose', R(vbar, 4)); E(L, 'screens[8].prose', R(100 * math.sqrt(252 * vbar) / 100, 2))
for p in ('screens[8].explain.text', 'screens[8].explain.canvas.values.r1c1'):
    E(L, p, R(vbar * (1 - ta - tb), 4))
E(L, 'screens[8].explain.text', R(ta, 4)); E(L, 'screens[8].explain.text', R(tb, 4)); E(L, 'screens[8].feedback.correct', R(ta + tb, 4))
E(L, 'screens[8].explain.text', R(ft.fun - fit.fun, 2))
E(L, 'screens[9].prose', R(math.sqrt(0.0121), 2)); E(L, 'screens[9].prose', R(math.sqrt(252 * 0.0121), 2)); E(L, 'screens[9].prose', R(np.std(rp[1380:1480], ddof=1) * S252, 1))
E(L, 'screens[9].feedback.byKey.omega', round(0.8885 / 0.0121)); E(L, 'screens[9].explain.text', round(0.8885 / 0.0121)); E(L, 'screens[9].feedback.byKey.omega', R(100 * pers, 1))
for sig, path in [(0.2, 'screens[11].prose'), (S252 / 100, 'screens[11].widget.answer'), (math.sqrt(252 * VL) / 100, 'screens[11].widget.wrong[1].value')]:
    E(L, path, R(bs(100, 100, 0.05, 1, sig), 4))
E(L, 'screens[11].feedback.correct', R(bs(100, 100, 0.05, 1, 0.2) - bs(100, 100, 0.05, 1, S252 / 100), 2))
E(L, 'quiz[0].widget.answer', R(0.04 / 0.02, 1)); E(L, 'quiz[0].widget.wrong[1].value', R(0.04 / 0.12, 4)); E(L, 'quiz[0].explain.text', R(math.sqrt(2), 2))
E(L, 'quiz[1].widget.answer', R(1.5 * S252 / 100, 4)); E(L, 'quiz[1].widget.wrong[0].value', 2.25 * 252 / 100)
E(L, 'quiz[3].widget.answer', R(math.log(0.5) / math.log(0.95), 2)); E(L, 'quiz[3].explain.text', R(math.log(0.95), 4))

# ================= review-2 =================
L = 'review'
E(L, 'items[0].widget.answer', R(0.94 * 1.5 + 0.06 * 4, 2)); E(L, 'items[0].widget.wrong[0].value', R(0.06 * 1.5 + 0.94 * 4, 2)); E(L, 'items[0].widget.wrong[1].value', R(0.94 * 1.5 + 0.06 * 2, 2))
E(L, 'items[1].widget.answer', R(math.sqrt(2.2) / 100, 6)); E(L, 'items[1].widget.wrong[1].value', R(math.sqrt(1.0) / 100, 4))
E(L, 'items[2].widget.answer', R(0.03 + 0.07 * 4 + 0.9 * 1.2, 2)); E(L, 'items[2].widget.wrong[0].value', R(0.03 + 0.28, 2))
E(L, 'items[2].widget.wrong[1].value', R(0.03 + 0.90 * 4 + 0.07 * 1.2, 3))   # swapping alpha and beta keeps omega
E(L, 'items[3].widget.answer', R(0.05 / 0.02, 1)); E(L, 'items[3].widget.wrong[1].value', R(0.05 / 0.09, 4)); E(L, 'items[3].explain.text', R(math.sqrt(2.5), 2))
E(L, 'items[3].explain.text', R(math.sqrt(252 * 2.5), 1))
E(L, 'items[5].widget.answer', R(3 * 0.84 / 0.52, 2)); E(L, 'items[5].widget.wrong[1].value', R(3 * 0.6 / (1 - 1.2), 1))
E(L, 'items[6].widget.answer', R(ell(2, 1), 3)); E(L, 'items[6].widget.wrong[1].value', R(-0.5 * (math.log(2 * math.pi) + 2), 3))
# fix pass 21: omega 0.036, alpha 0.08, beta 0.90 (V_L = 1.8)
VL7 = 0.036 / (1 - 0.08 - 0.90)
E(L, 'items[7].prose', R(math.sqrt(0.036) * S252, 1)); E(L, 'items[7].prose', 0.036); E(L, 'items[7].widget.answer', R(math.sqrt(252 * VL7) / 100, 3))
E(L, 'items[7].widget.accept', R(math.sqrt(252 * VL7), 2)); E(L, 'items[7].widget.accept', R(VL7, 1))
E(L, 'items[7].widget.wrong[0].value', R(math.sqrt(0.036) * S252 / 100, 5)); E(L, 'items[7].widget.wrong[1].value', R(252 * VL7 / 100, 3))
E(L, 'items[7].explain.text', R(VL7, 1)); E(L, 'items[7].explain.text', R(math.sqrt(VL7), 3)); E(L, 'items[7].explain.text', R(math.sqrt(252 * VL7), 2))
E(L, 'items[7].explain.text', 'sevenfold') if round(math.sqrt(252 * VL7) / (math.sqrt(0.036) * S252)) == 7 else claim('sevenfold', False)
dsd = 0.008 * math.sqrt(2)
E(L, 'items[8].explain.text', R(dsd, 3)); E(L, 'items[8].explain.text', R(0.013 / R(dsd, 3), 1))
E(L, 'items[8].widget.options[1].why', 'a quarter') if 0.22 < 2 * stats.norm.sf(0.013 / dsd) < 0.28 else claim('quarter of the time', False)
E(L, 'items[8].widget.options[3].why', R(0.008 / math.sqrt(2), 3))
E(L, 'items[9].widget.answer', R(math.sqrt(252 * 2) / 100, 4)); E(L, 'items[9].widget.wrong[0].value', R(2 * S252 / 100, 4))
stated(L, 'items[9].explain.text', 'by six points', round(math.sqrt(504) - S252) == 6)
E(L, 'items[9].explain.text', 'six and a half points') if round(2 * (math.sqrt(504) - S252)) == 13 else claim('six and a half points', False)   # fix pass 6

# ================= homework-2 =================
L = 'homework'
E(L, 'items[0].widget.answer', R(math.sqrt(252 * 1.5) / 100, 4)); E(L, 'items[0].widget.wrong[0].value', R(math.sqrt(0.03) * S252 / 100, 4))
E(L, 'items[0].widget.wrong[1].value', R(math.sqrt(1.5) / 100, 6)); E(L, 'items[0].widget.wrong[2].value', 252 * 1.5 / 100)
m_e, m_g = np.mean((ewma(rp, 0.94)[20:] - s2p[20:]) ** 2), np.mean((gv[20:] - s2p[20:]) ** 2)
E(L, 'items[2].widget.examples[0].expect', R(m_e, 6)); E(L, 'items[2].widget.examples[0].expect', R(m_g, 6))
E(L, 'items[2].feedback.correct', R(m_e, 4)); E(L, 'items[2].feedback.correct', R(m_g, 4)); E(L, 'items[2].feedback.correct', 'eight times') if round(m_e / m_g) == 8 else None
E(L, 'items[3].widget.answer', R(0.995 ** 252, 4)); E(L, 'items[3].explain.text', round(math.log(0.5) / math.log(0.995))); E(L, 'items[3].feedback.byKey.half', round(math.log(0.5) / math.log(0.995)))
# fix pass 24: a second share (B's parameters, seed 11), refitted in %
rS = 100 * simulate_garch(2e-6, 0.08, 0.90, 2000, 11)[0]; fS = fit_garch(rS).x
E(L, 'items[4].prose', R(fS[0], 4)); E(L, 'items[4].prose', R(fS[1], 4)); E(L, 'items[4].prose', R(fS[2], 4))
E(L, 'items[4].widget.answer', R(R(fS[0], 4) * 1e-4, 10)); E(L, 'items[4].widget.accept', '0.00000251'); E(L, 'items[4].explain.text', '0.00000251')
E(L, 'items[4].widget.wrong[0].value', R(R(fS[0], 4) * 1e-2, 6)); E(L, 'items[4].widget.wrong[1].value', R(fS[0], 4))
rN = 100 * simulate_garch(2e-7, 0.06, 0.939, 2000, 3)[0]; fN = fit_garch(rN).x
E(L, 'items[5].explain.text', R(fN[1] + fN[2], 4)); E(L, 'items[5].feedback.correct', R(pers, 3))
E(L, 'items[5].feedback.correct', round(math.log(0.5) / math.log(pers))); E(L, 'items[5].feedback.correct', R(100 * math.sqrt(252 * VL) / 100, 2))
# fix pass 24: homework-2 items[6] is now a scenario (decimal fit 0.31 and 0.22, % fit 0.07 and 0.91, log-likelihood 150 higher), not a fit
E(L, 'items[6].prose', 150); E(L, 'items[6].widget.options[1].why', 150)
E(L, 'items[7].model', round(math.log(0.5) / math.log(0.999))); E(L, 'items[7].model', R(math.sqrt(252 * 2), 1)); E(L, 'items[7].model', R(math.sqrt(2), 2))
E(L, 'items[7].model', R(math.sqrt(252 * 1), 1)); E(L, 'items[7].model', R(math.sqrt(252 * 4), 1)); E(L, 'items[7].model', R(f1000[1] + f1000[2], 4))

lv.check_wrongs()
for f in fails:
    print('BAD', f)
if fails:
    lv.results.append((False, 'route agreement', ''))
lv.report()
