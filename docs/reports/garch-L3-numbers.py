"""Recompute every number stated in garch level 3 (Using forecasts) and check it at its JSON path (second read).

Run: python3 docs/reports/garch-L3-numbers.py   (NumPy, SciPy and the standard library; exits 0 when every check passes)

Data: the course path extended to 3,000 days (seed 7), fitted on days 0 to 1,999 with the brief's SLSQP fit, and
filtered over all 3,000 days from the variance of all 3,000 (`s2f`, as in the lessons' preludes). The h-step
forecast is computed twice (closed form and stepped recursion), Kupiec's LR twice (formula and SciPy's binomial
log-pmf ratio), and the Christoffersen test and Kupiec's power by exact enumeration. A check that fails because the
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

lv = Level("garch", 3)
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


def money(x):
    return f'{x:,.0f}'


def simulate_garch(omega, alpha, beta, n, seed, nu=None):
    g = np.random.default_rng(seed)
    z = g.standard_normal(n) if nu is None else g.standard_t(nu, n) * np.sqrt((nu - 2) / nu)
    r = np.empty(n); s2 = np.empty(n)
    s2[0] = omega / (1 - alpha - beta)
    for t in range(n):
        if t > 0:
            s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
        r[t] = np.sqrt(s2[t]) * z[t]
    return r, s2


def garch_variance(params, r):
    omega, alpha, beta = params
    s2 = np.empty(len(r)); s2[0] = r.var()
    for t in range(1, len(r)):
        s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
    return s2


def neg_loglik(params, r):
    s2 = garch_variance(params, r)
    return 0.5 * np.sum(np.log(2 * np.pi) + np.log(s2) + r ** 2 / s2)


def fit_garch(r):
    return minimize(neg_loglik, x0=np.array([0.05, 0.05, 0.90]), args=(r,), method="SLSQP",
                    bounds=[(1e-6, 10.0), (0.0, 1.0), (0.0, 1.0)],
                    constraints=[{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2]}], options={"ftol": 1e-10, "maxiter": 500})


def forecast(params, last_r, last_s2, h):
    w, a, b = params; out = []; s = w + a * last_r ** 2 + b * last_s2
    for _ in range(h):
        out.append(s); s = w + (a + b) * s
    return np.array(out)


def kupiec(x, n, p=0.01):
    xl = lambda a, b: 0.0 if a == 0 else a * math.log(b)  # noqa: E731
    ph = x / n
    lr = max(0.0, -2 * (xl(n - x, 1 - p) + xl(x, p) - xl(n - x, 1 - ph) - xl(x, ph)))
    return lr, stats.chi2.sf(lr, 1)


def christoffersen(hits):
    h = np.asarray(hits, int); a, b = h[:-1], h[1:]
    n00, n01, n10, n11 = [int(np.sum((a == i) & (b == j))) for i in (0, 1) for j in (0, 1)]
    xl = lambda k, q: 0.0 if k == 0 else k * math.log(q)  # noqa: E731
    p01, p11, p = n01 / (n00 + n01), (n11 / (n10 + n11) if n10 + n11 else 0), (n01 + n11) / len(a)
    lr = -2 * (xl(n00 + n10, 1 - p) + xl(n01 + n11, p) - xl(n00, 1 - p01) - xl(n01, p01) - xl(n10, 1 - p11) - xl(n11, p11))
    return lr, stats.chi2.sf(lr, 1)


def bs(S, K, rr, T, sig):
    d1 = (math.log(S / K) + (rr + sig ** 2 / 2) * T) / (sig * math.sqrt(T))
    return S * stats.norm.cdf(d1) - K * math.exp(-rr * T) * stats.norm.cdf(d1 - sig * math.sqrt(T))


def ewma(r, lam, init=20):
    s = np.empty(len(r)); s[0] = r[:init].var()
    for t in range(1, len(r)):
        s[t] = lam * s[t - 1] + (1 - lam) * r[t - 1] ** 2
    return s


S252 = math.sqrt(252)
q01, q05, q001 = stats.norm.ppf(0.01), stats.norm.ppf(0.05), stats.norm.ppf(0.001)
k5 = math.sqrt(3 / 5); t01, t05, t001 = stats.t.ppf(0.01, 5) * k5, stats.t.ppf(0.05, 5) * k5, stats.t.ppf(0.001, 5) * k5
r3, s3 = simulate_garch(2e-6, 0.08, 0.90, 3000, 7)
rp3 = 100 * r3
fit = fit_garch(rp3[:2000]); params = fit.x; w_, a_, b_ = params; phi = a_ + b_; VL = w_ / (1 - phi)
two('fit matches the preludes', np.max(np.abs(params - np.array([0.012064508787727014, 0.06293432228388088, 0.9234867892614822]))), 0, 1e-6)
s2f = garch_variance(params, rp3)


def closed(h, s1):
    return VL + phi ** (h - 1) * (s1 - VL)


# ================= l9 forecasting =================
L = 'l9'
s1404 = s2f[1404]; sig1 = math.sqrt(s1404)
E(L, 'screens[0].prose', R(-rp3[1403], 2)); E(L, 'screens[0].prose', R(sig1, 2)); E(L, 'screens[0].prose', R(math.sqrt(VL), 2))
claim('2.62% is the highest forecast in the first 2,000 days', int(np.argmax(s2f[:2001])) == 1404)
for p, v in [('V', VL), ('p', phi), ('s', sig1)]:
    E(L, f'screens[0].canvas.params.params.{p}', R(v, 6))
two('closed form = stepped recursion (h = 250)', closed(250, s1404), forecast(params, rp3[1403], s2f[1403], 250)[-1], 1e-10)
for h in (20, 60, 250):
    E(L, 'screens[0].explain.text', R(math.sqrt(closed(h, s1404)), 2))
E(L, 'screens[0].feedback.correct', R(math.sqrt(closed(250, s1404)), 2)); E(L, 'screens[0].hints[2].text', R(0.9864 ** 249, 2))
E(L, 'screens[0].widget.options[1].why', round(100 * 0.9864 ** 249))
claim('forecast near 1.8% after about 60 days', abs(math.sqrt(closed(60, s1404)) - 1.88) < 0.01)
E(L, 'screens[1].explain.text', R(math.sqrt(closed(20, 0.25)), 2)); E(L, 'screens[1].explain.text', R(math.sqrt(closed(250, 0.25)), 2))
E(L, 'screens[2].prose', R(sig1, 4)); E(L, 'screens[2].prose', R(s1404, 4)); E(L, 'screens[2].prose', R(VL, 4))
E(L, 'screens[2].widget.answer', R(math.sqrt(closed(20, s1404)) / 100, 6)); E(L, 'screens[2].widget.wrong[0].value', R(math.sqrt(closed(21, s1404)) / 100, 6))
E(L, 'screens[2].widget.wrong[1].value', R(math.sqrt(phi ** 19 * (s1404 - VL)) / 100, 6)); E(L, 'screens[2].widget.wrong[2].value', R(sig1 / 100, 6))
E(L, 'screens[2].hints[1].text', R(s1404 - VL, 4)); E(L, 'screens[2].hints[2].text', R(0.9864 ** 19, 3))
E(L, 'screens[2].widget.accept', R(0.8885 + 0.9864 ** 19 * 5.9544, 3))   # as shown: rounded inputs give 5.479, not 5.4807
E(L, 'screens[2].explain.text', R(0.8885 + 0.9864 ** 19 * 5.9544, 3))
s2000 = s2f[2000]
E(L, 'screens[3].prose', R(math.sqrt(s2000), 4)); E(L, 'screens[3].canvas.params.params.s', R(math.sqrt(s2000), 6))
E(L, 'screens[3].widget.rows[1][1].answer', R(math.sqrt(closed(20, s2000)), 4)); E(L, 'screens[3].widget.rows[2][1].answer', R(math.sqrt(closed(250, s2000)), 4))
claim('the calm curve spans less than 0.03 points', math.sqrt(closed(250, s2000)) - math.sqrt(s2000) < 0.03)
c2 = R(math.sqrt(s2000), 4) ** 2   # the hints work from the shown 0.9181
E(L, 'screens[3].hints[0].text', R(c2, 4)); E(L, 'screens[3].hints[1].text', R(R(c2, 4) - R(VL, 4), 4)); E(L, 'screens[3].hints[2].text', R(R(VL, 4) - R(0.9864 ** 19, 3) * abs(R(c2, 4) - R(VL, 4)), 4))
E(L, 'screens[3].hints[2].text', R(closed(250, s2000), 4))
f5 = forecast(params, rp3[1403], s2f[1403], 5)
for i in range(5):
    for s_ in (4, 5):
        E(L, f'screens[{s_}].canvas.params.rows[{i}][1]', f'{math.sqrt(f5[i]):.4f}'); E(L, f'screens[{s_}].canvas.params.rows[{i}][2]', f'{f5[i]:.4f}')
E(L, 'screens[4].canvas.params.rows[5][2]', R(f5.sum(), 4)); E(L, 'screens[4].widget.answer', R(math.sqrt(f5.sum()) / 100, 6))
E(L, 'screens[4].widget.wrong[0].value', R(sig1 * math.sqrt(5) / 100, 6)); E(L, 'screens[4].widget.wrong[1].value', R(np.sqrt(f5).sum() / 100, 6))
E(L, 'screens[4].widget.wrong[2].value', R(math.sqrt(f5.mean()) / 100, 6)); two('mean vol near root of mean variance', np.sqrt(f5).mean(), math.sqrt(f5.mean()), 1e-4); E(L, 'screens[4].explain.text', R(sig1 * math.sqrt(5), 2))
E(L, 'screens[5].widget.examples[0].expect', R(s1404, 9)); E(L, 'screens[5].prose', R(math.sqrt(f5.sum()), 4))
f250 = forecast(params, rp3[1403], s2f[1403], 250); f250c = forecast(params, rp3[1999], s2f[1999], 250)
E(L, 'screens[6].prose', R(sig1 * math.sqrt(250), 2)); E(L, 'screens[6].widget.options[0].text', R(math.sqrt(f250.sum()), 2))
E(L, 'screens[6].hints[2].text', R(f250.sum(), 1)); E(L, 'screens[6].widget.options[2].text', R(math.sqrt(VL) * math.sqrt(250), 2))
E(L, 'screens[6].widget.options[3].text', round(sig1 * 250)); E(L, 'screens[6].explain.text', round(100 * (sig1 * math.sqrt(250) / math.sqrt(f250.sum()) - 1)))
E(L, 'screens[6].explain.text', R(math.sqrt(s2000) * math.sqrt(250), 2)); E(L, 'screens[6].explain.text', R(math.sqrt(f250c.sum()), 2))
e94 = ewma(rp3, 0.94)
E(L, 'screens[7].prose', R(math.sqrt(e94[1404]), 2)); E(L, 'screens[7].canvas.params.functions[1].expr', R(math.sqrt(e94[1404]), 4))
E(L, 'screens[7].widget.answer', R(math.sqrt(250 * e94[1404]) / 100, 6)); E(L, 'screens[7].widget.accept', R(math.sqrt(250 * e94[1404]), 2))
E(L, 'screens[7].widget.wrong[0].value', R(math.sqrt(f250.sum()) / 100, 6)); E(L, 'screens[7].hints[2].text', R(R(math.sqrt(e94[1404]), 4) ** 2, 3))
E(L, 'screens[8].widget.options[2].why', R(0.999 ** 249, 2))
y1999 = math.sqrt(forecast(params, rp3[1999], s2f[1999], 252).sum()); y1403 = math.sqrt(forecast(params, rp3[1403], s2f[1403], 252).sum())
E(L, 'screens[10].feedback.correct', R(y1999, 2)); E(L, 'screens[10].explain.text', R(y1999, 2)); E(L, 'screens[10].explain.text', R(y1403, 2))
stv = garch_variance((0.02, 0.08, 0.90), rp3[:2000])
claim('true parameters give a higher year from day 1,999', math.sqrt(forecast((0.02, 0.08, 0.90), rp3[1999], stv[1999], 252).sum()) > y1999)
rv20 = np.std(rp3[1384:1404], ddof=1) * S252; v63 = math.sqrt(f5[:0].sum() + forecast(params, rp3[1403], s2f[1403], 63).sum() * 252 / 63)
for i, sig in enumerate((rv20, sig1 * S252, v63)):
    E(L, f'screens[11].canvas.params.rows[{i}][1]', f'{sig:.2f}%'); E(L, f'screens[11].canvas.params.rows[{i}][2]', f'£{bs(100, 100, 0.05, 0.25, sig / 100):.2f}')
E(L, 'screens[11].explain.text', R(bs(100, 100, 0.05, 0.25, sig1 * S252 / 100) - bs(100, 100, 0.05, 0.25, v63 / 100), 2))
E(L, 'screens[11].prose', R(bs(100, 100, 0.05, 1, 0.2), 4))
E(L, 'quiz[0].widget.answer', R(math.sqrt(1 + 0.95 ** 10 * 3) / 100, 6)); E(L, 'quiz[0].widget.wrong[0].value', R(math.sqrt(1 + 0.95 ** 11 * 3) / 100, 6))
E(L, 'quiz[0].widget.wrong[1].value', R(math.sqrt(0.95 ** 10 * 3) / 100, 6)); E(L, 'quiz[0].explain.text', R(0.95 ** 10 * 3, 3))
E(L, 'quiz[1].widget.answer', R(math.sqrt(10.94) / 100, 6)); E(L, 'quiz[1].widget.wrong[1].value', R((2 + math.sqrt(3) + 1.5 + 1.3) / 100, 6))
E(L, 'quiz[2].widget.answer', R(math.log(0.5) / math.log(0.9864), 1)); E(L, 'quiz[2].widget.wrong[0].value', R(0.5 / 0.0136, 1))

# ================= l10 value at risk =================
L = 'l10'
sig = math.sqrt(s2000) / 100; pos = 1_000_000
v99 = -q01 * sig * pos
E(L, 'screens[0].widget.options[0].text', money(v99)); E(L, 'screens[0].widget.options[0].text', R(-q01 * sig * 100, 2))
E(L, 'screens[0].widget.options[1].text', money(sig * pos)); E(L, 'screens[0].widget.options[2].text', money(2 * sig * pos))
E(L, 'screens[0].widget.options[2].why', R(100 * stats.norm.cdf(-2), 1)); E(L, 'screens[0].widget.options[1].why', round(100 * stats.norm.cdf(-1)))
E(L, 'screens[0].hints[2].text', R(-q01, 4)); E(L, 'screens[0].explain.text', R(q01 * sig * 100, 3))
E(L, 'screens[1].explain.text', R(q01 * 1.8, 2)); E(L, 'screens[1].explain.text', money(-q01 * 0.018 * pos))
test = s2f[2000:3000]; imax = int(np.argmax(test)) + 2000
two('stormiest test forecast is for day 2,900', imax, 2900)
sx = math.sqrt(s2f[imax]) / 100
E(L, 'screens[2].question', R(100 * sx, 4)); E(L, 'screens[2].widget.answer', R(-q01 * sx * pos, 1)); two('l10 s2 95% slip', lv._file(L)[1]['screens'][2]['widget']['wrong'][1]['value'], -q05 * sx * pos, 1e-4)
E(L, 'screens[2].feedback.correct', round(100 * (sx / sig - 1)))
E(L, 'screens[3].widget.rows[0][2].answer', R(-q05 * sig * pos, 2)); E(L, 'screens[3].widget.rows[2][2].answer', R(-q001 * sig * pos, 2))
E(L, 'screens[3].widget.rows[1][2]', f'{v99:,.2f}'); E(L, 'screens[3].hints[1].text', f'{sig * pos:,.2f}')
claim('the 99.9% VaR is a third larger', round((q001 / q01 - 1) * 3) == 1)
E(L, 'screens[4].prose', R(stats.t.ppf(0.01, 5), 4)); E(L, 'screens[4].widget.answer', R(-t01 * sig * pos, 2))
E(L, 'screens[4].widget.wrong[0].value', R(-stats.t.ppf(0.01, 5) * sig * pos, 2)); E(L, 'screens[4].feedback.correct', round(100 * (t01 / q01 - 1)))
E(L, 'screens[4].feedback.byKey.unscaled', round(100 * (math.sqrt(5 / 3) - 1))); E(L, 'screens[4].explain.text', money(-t05 * sig * pos))
for i, (qn, qt) in enumerate([(q05, t05), (q01, t01), (q001, t001)]):
    E(L, f'screens[5].canvas.params.rows[{i}][1]', f'{-qn * sig * pos:,.2f}'); E(L, f'screens[5].canvas.params.rows[{i}][2]', f'{-qt * sig * pos:,.2f}')
# the storm evening of day 1,403
sd250 = np.std(rp3[1154:1404], ddof=1)
E(L, 'screens[6].prose', R(sd250, 4)); E(L, 'screens[6].prose', money(-q01 * sd250 / 100 * pos)); E(L, 'screens[6].prose', R(sig1, 4))
E(L, 'screens[6].widget.options[0].text', money(-q01 * sig1 / 100 * pos)); E(L, 'screens[6].widget.options[2].text', money(-q01 * (sd250 + sig1) / 200 * pos))
gv, r250 = [], []
for t in range(1380, 1480):
    gv.append(-q01 * math.sqrt(s2f[t]) / 100); r250.append(-q01 * np.std(rp3[t - 250:t], ddof=1) / 100)
br_g = sum(r3[t] < -gv[t - 1380] for t in range(1380, 1480)); br_s = sum(r3[t] < -r250[t - 1380] for t in range(1380, 1480))
E(L, 'screens[6].explain.text', br_s); claim('GARCH beaten twice in the storm', br_g == 2); E(L, 'screens[6].hints[2].text', br_s)
E(L, 'screens[6].explain.text', money(-q01 * math.sqrt(s3[1404]) * pos))
mk = [m['i'] + 1300 for m in lv._file(L)[1]['screens'][6]['canvas']['state']['markers']]
b250 = [t for t in range(1300, 1480) if r3[t] < q01 * np.std(rp3[t - 250:t], ddof=1) / 100]
claim('l10 s6 markers are the 250-day breaches in the shaded storm', mk == [t for t in b250 if t >= 1380])
stated(L, 'screens[6].prose', "dots mark the 250-day line's breaches.", mk == b250)   # 1,317 and 1,377 are unmarked
es = sig * stats.norm.pdf(q01) / 0.01 * pos
E(L, 'screens[7].prose', R(stats.norm.pdf(q01), 6)); E(L, 'screens[7].widget.answer', R(es, 2)); E(L, 'screens[7].widget.wrong[1].value', R(sig * stats.norm.pdf(q01) * pos, 1))
E(L, 'screens[7].feedback.correct', round(100 * (es / v99 - 1))); E(L, 'screens[7].explain.text', R(stats.norm.pdf(q01) / 0.01, 3))
var_test = -q01 * np.sqrt(test) / 100 * pos; loss = -r3[2000:3000] * pos; brk = loss > var_test
E(L, 'screens[7].explain.text', int(brk.sum())); E(L, 'screens[7].explain.text', money(loss[brk].mean()))
f10 = forecast(params, rp3[1403], s2f[1403], 10)
E(L, 'screens[8].prose', R(f10.sum(), 3)); E(L, 'screens[8].prose', R(math.sqrt(f10.sum()), 4))
E(L, 'screens[8].widget.answer', R(-q01 * math.sqrt(f10.sum()) / 100 * pos, 2)); E(L, 'screens[8].widget.wrong[0].value', R(-q01 * sig1 / 100 * math.sqrt(10) * pos, 2))
E(L, 'screens[8].widget.wrong[1].value', R(-q01 * sig1 / 100 * pos, 2)); E(L, 'screens[8].explain.text', R(100 * (math.sqrt(10) * sig1 / math.sqrt(f10.sum()) - 1), 1))
f10c = forecast(params, rp3[1999], s2f[1999], 10)
gap1999 = abs(-q01 * math.sqrt(f10c.sum()) / 100 * pos - (-q01 * math.sqrt(10 * s2000) / 100 * pos))
print('l10 s8 day-1,999 gap between summed and sqrt(10):', gap1999)
stated(L, 'screens[8].explain.text', 'within £108', gap1999 <= 108)
E(L, 'screens[9].widget.options[3].text', money(2 * v99))
E(L, 'screens[10].explain.text', money(var_test.min())); E(L, 'screens[10].explain.text', money(var_test.max())); E(L, 'screens[10].feedback.correct', money(var_test.mean()))
E(L, 'screens[10].feedback.correct', f'{var_test[0]:,.2f}')
E(L, 'screens[11].canvas.params.rows[0][2]', money(25000 - round(v99))); E(L, 'screens[11].canvas.params.rows[1][2]', money(25000 - round(-t01 * sig * pos)))
E(L, 'screens[11].widget.options[0].text', money(25000 - round(-t01 * sig * pos)))
E(L, 'quiz[0].widget.answer', R(-q01 * 0.012 * 500000, 2)); E(L, 'quiz[0].widget.wrong[1].value', R(-q05 * 6000, 1))
d = 2360
E(L, 'quiz[1].prose', money(var_test[d - 2000])); E(L, 'quiz[1].prose', R(-rp3[d], 2)); E(L, 'quiz[1].prose', money(loss[d - 2000]))
claim('day 2,360 is the worst test day', int(np.argmax(loss)) + 2000 == 2360)
E(L, 'quiz[1].widget.options[1].text', round(100 * (loss[d - 2000] / var_test[d - 2000] - 1)))
E(L, 'quiz[2].widget.answer', R(t01, 4)); E(L, 'quiz[2].widget.wrong[1].value', R(stats.t.ppf(0.01, 5) * math.sqrt(5 / 3), 4))
E(L, 'quiz[3].widget.answer', R(math.sqrt(10) * 20000, 2))

# ================= l11 checking VaR =================
L = 'l11'
sd2520 = math.sqrt(2520 * 0.01 * 0.99)
E(L, 'screens[0].prose', R(sd2520, 2)); E(L, 'screens[0].hints[2].text', R((41 - 25.2) / sd2520, 1)); E(L, 'screens[0].explain.text', R((41 - 25.2) / sd2520, 1))
pb = stats.binom.sf(40, 2520, 0.01)
E(L, 'screens[0].explain.text', R(100 * pb, 2)); E(L, 'screens[0].feedback.correct', round(1 / pb, -1))
E(L, 'screens[3].prose', R(pb, 5)); E(L, 'screens[3].widget.options[0].text', R(100 * pb, 2)); E(L, 'screens[3].widget.options[2].why', R(100 * 41 / 2520, 1))
# breaches among the eight largest losses of days 2,290 to 2,429
win = np.arange(2290, 2430); top8 = sorted(win[np.argsort(r3[win])[:8]])
mk = [m['i'] + 2290 for m in lv._file(L)[1]['screens'][1]['canvas']['state']['markers']]
claim('l11 s1 markers are the eight largest losses', mk == top8)
brs = [t for t in top8 if -r3[t] * pos > var_test[t - 2000]]
claim('l11 s1 the breaches are 2,311, 2,360 and 2,421', brs == [2311, 2360, 2421])
E(L, 'screens[1].explain.text', R(-rp3[2313], 2)); E(L, 'screens[1].explain.text', R(var_test[313] / pos * 100, 2)); E(L, 'screens[1].explain.text', R(var_test[421] / pos * 100, 2))
stated(L, 'screens[1].explain.text', 'more than day 2,421', -r3[2313] > -r3[2421])
E(L, 'screens[2].widget.answer', R(math.sqrt(9.9), 4)); E(L, 'screens[2].widget.wrong[1].value', R(math.sqrt(10), 4))
ll0 = 2479 * math.log(0.99) + 41 * math.log(0.01); ll1 = 2479 * math.log(2479 / 2520) + 41 * math.log(41 / 2520)
lr41, p41 = kupiec(41, 2520)
two('Kupiec by binomial log-pmf ratio', lr41, -2 * (stats.binom.logpmf(41, 2520, 0.01) - stats.binom.logpmf(41, 2520, 41 / 2520)), 1e-8)
E(L, 'screens[4].widget.answer', R(lr41, 3)); E(L, 'screens[4].hints[1].text', R(ll0, 3)); E(L, 'screens[4].hints[2].text', R(ll1, 3))
E(L, 'screens[4].explain.text', R(p41, 4)); E(L, 'screens[4].explain.text', R(pb, 4)); E(L, 'screens[4].prose', R(stats.chi2.ppf(0.95, 1), 3))
acc = [x for x in range(0, 41) if kupiec(x, 1000)[0] <= stats.chi2.ppf(0.95, 1)]
claim('Kupiec at n = 1,000 accepts 5 to 16', acc == list(range(5, 17)))
E(L, 'screens[5].widget.options[1].why', R(kupiec(4, 1000)[0], 3)); E(L, 'screens[5].hints[2].text', R(kupiec(17, 1000)[0], 2)); E(L, 'screens[5].widget.options[2].why', R(kupiec(0, 1000)[0], 1))
nb = int(brk.sum()); lrg, pg = kupiec(nb, 1000)
E(L, 'screens[6].feedback.correct', nb); E(L, 'screens[6].feedback.correct', R(lrg, 4)); E(L, 'screens[6].feedback.correct', R(pg, 4)); E(L, 'screens[6].explain.text', R(kupiec(0, 250)[0], 4))
sd_tr = np.std(rp3[:2000], ddof=1); vt_t = -t01 * np.sqrt(test) / 100 * pos
var_cv = -q01 * sd_tr / 100 * pos; nt = int((loss > vt_t).sum()); ncv = int((loss > var_cv).sum())
st_ = garch_variance((0.02, 0.08, 0.90), rp3); ntr = int((loss > -q01 * np.sqrt(st_[2000:]) / 100 * pos).sum())
E(L, 'screens[7].prose', R(sd_tr, 4)); E(L, 'screens[7].explain.text', money(var_cv))
for k_, v_ in [('gn', nb), ('gt', nt), ('cv', ncv), ('tr', ntr)]:
    E(L, f'screens[7].canvas.state.values.{k_}', v_); E(L, f'screens[10].canvas.state.values.{k_}', v_)
E(L, 'screens[7].explain.text', R(kupiec(ncv, 1000)[0], 3)); E(L, 'screens[7].explain.text', R(kupiec(ncv, 1000)[1], 4))
E(L, 'screens[7].explain.text', R(pg, 3)); E(L, 'screens[7].explain.text', R(kupiec(nt, 1000)[1], 3))
E(L, 'screens[7].widget.options[2].why', R(kupiec(nt, 1000)[0], 3)); E(L, 'screens[7].widget.options[3].why', R(kupiec(ntr, 1000)[0], 3))
E(L, 'screens[10].explain.text', R(kupiec(ncv, 1000)[0], 3))
hits = brk.astype(int)
claim('no two GARCH breaches on consecutive days', int(np.sum(hits[1:] & hits[:-1])) == 0)
E(L, 'screens[8].explain.text', R(christoffersen(hits)[1], 2))
X = np.zeros(1000, int); X[400:406] = 1; X[700:705] = 1
claim('model X: 11 breaches, 9 follow a breach', X.sum() == 11 and int(np.sum(X[1:] & X[:-1])) == 9)
E(L, 'screens[8].prose', R(kupiec(11, 1000)[0], 4))
yrs = [int(hits[i * 250:(i + 1) * 250].sum()) for i in range(4)]
for i, v_ in enumerate(yrs):
    E(L, f'screens[9].canvas.state.values.y{i + 1}', v_)
E(L, 'screens[9].explain.text', ', '.join(map(str, yrs[:3])) + ' and ' + str(yrs[3]))
E(L, 'screens[9].widget.answer', R(kupiec(0, 250)[0], 4)); E(L, 'screens[9].widget.wrong[1].value', R(kupiec(0, 250)[0] / 2, 4))
E(L, 'screens[9].feedback.correct', R(kupiec(0, 250)[1], 3))
acc250 = [x for x in range(0, 30) if kupiec(x, 250)[0] <= stats.chi2.ppf(0.95, 1)]
power = {p_: sum(stats.binom.pmf(x, 250, p_) for x in acc250) for p_ in (0.01, 0.02)}
E(L, 'screens[11].canvas.params.rows[0][1]', f'{100 * power[0.01]:.1f}%'); E(L, 'screens[11].canvas.params.rows[1][1]', f'{100 * power[0.02]:.1f}%')
E(L, 'screens[11].prose', R(kupiec(3, 250)[0], 3)); E(L, 'screens[11].prose', R(kupiec(3, 250)[1], 2))
E(L, 'screens[11].widget.options[1].why', round(100 * power[0.02])); E(L, 'screens[11].widget.options[2].why', R(math.sqrt(250 * 0.01 * 0.99), 2))
E(L, 'quiz[0].widget.answer', R(math.sqrt(23.75), 4)); E(L, 'quiz[0].widget.wrong[1].value', R(math.sqrt(4.95), 4))
E(L, 'quiz[1].widget.answer', R(kupiec(0, 500)[0], 4)); E(L, 'quiz[1].explain.text', R(kupiec(0, 500)[1], 4))
v95 = -q05 * np.sqrt(test) / 100 * pos; n95 = int((loss > v95).sum())
E(L, 'quiz[2].prose', n95); E(L, 'quiz[2].widget.options[0].text', R(kupiec(n95, 1000)[0], 1)); E(L, 'quiz[2].explain.text', R(kupiec(n95, 1000, 0.05)[0], 2))

# ================= l12 volatility targeting =================
L = 'l12'
fa = np.sqrt(test) / 100 * S252
E(L, 'screens[0].prose', R(100 * np.std(r3[2000:], ddof=1) * S252, 2)); E(L, 'screens[0].prose', R(100 * fa.min(), 2)); E(L, 'screens[0].prose', R(100 * fa.max(), 2))
E(L, 'screens[0].widget.options[1].text', round(100 * 0.10 / np.std(r3[2000:], ddof=1) / S252)); E(L, 'screens[0].widget.options[1].why', R(20 * 0.10 / (np.std(r3[2000:], ddof=1) * S252), 1))
E(L, 'screens[1].explain.text', R(0.10 / fa.max(), 2)); E(L, 'screens[1].explain.text', R(0.10 / fa.min(), 2))
w = np.minimum(0.10 / fa, 2.0); iw = int(np.argmin(fa)) + 2000
two('calmest test day is 2,417', iw, 2417)
E(L, 'screens[2].question', R(math.sqrt(s2f[iw]), 5))   # 0.61196: the 4-place 0.6120 gives 9.7152, not 9.7145
E(L, 'screens[2].widget.answer', R(w.max(), 4)); E(L, 'screens[2].hints[1].text', R(100 * fa.min(), 4))
E(L, 'screens[2].widget.accept', R(math.sqrt(s2f[iw]), 5)); E(L, 'screens[2].widget.accept', R(100 * fa.min(), 4)); E(L, 'screens[2].hints[1].text', R(math.sqrt(s2f[iw]), 5))
E(L, 'screens[2].widget.wrong[1].value', R(fa.min() / 0.10, 4)); E(L, 'screens[2].feedback.byKey.cap', R(10 / 0.612, 1))
strat = w * r3[2000:]


def roll63(x):
    return np.array([np.std(x[t - 62:t + 1], ddof=1) * S252 for t in range(62, len(x))])


sd250t = np.array([np.std(rp3[t - 250:t], ddof=1) for t in range(2000, 3000)]) / 100 * S252
w250 = np.minimum(0.10 / sd250t, 2.0)
rg, ru, r2 = roll63(strat), roll63(r3[2000:]), roll63(w250 * r3[2000:])
for p in ('screens[3].widget.options[0].text', 'screens[11].canvas.params.rows[1][2]', 'quiz[3].widget.options[0].text'):
    E(L, p, R(100 * rg.min(), 1)); E(L, p, R(100 * rg.max(), 1))
E(L, 'screens[3].explain.text', R(100 * rg.min(), 2)); E(L, 'screens[3].explain.text', R(100 * rg.max(), 2))
E(L, 'screens[3].explain.text', R(100 * r2.min(), 2)); E(L, 'screens[3].explain.text', R(100 * r2.max(), 2))
for p in ('screens[3].widget.options[1].why', 'quiz[3].widget.options[1].why'):
    E(L, p, R(100 * r2.min(), 1)); E(L, p, R(100 * r2.max(), 1))
E(L, 'screens[3].widget.options[2].why', R(100 * ru.min(), 1)); E(L, 'screens[3].widget.options[2].why', R(100 * ru.max(), 1))
E(L, 'screens[11].canvas.params.rows[1][1]', R(100 * ru.min(), 1)); E(L, 'screens[11].canvas.params.rows[1][1]', R(100 * ru.max(), 1))
k2265 = 2265 - 2062
E(L, 'screens[3].hints[2].text', R(100 * ru[k2265], 1)); E(L, 'screens[3].hints[2].text', R(100 * r2[k2265], 1)); E(L, 'screens[3].hints[2].text', R(100 * rg[k2265], 1))
vol = np.std(strat, ddof=1) * S252; turn = np.abs(np.diff(w)).sum() * 252 / 999
for p in ('screens[3].feedback.correct', 'screens[6].prose', 'screens[7].canvas.params.rows[0][1]', 'screens[11].canvas.params.rows[0][2]', 'summary.ideas[0]'):
    E(L, p, R(100 * vol, 2))
E(L, 'screens[10].widget.examples[0].expect', R(vol, 4)); E(L, 'screens[10].widget.examples[0].expect', R(w.mean(), 4)); E(L, 'screens[10].widget.examples[0].expect', R(turn, 4))
for i in range(6):
    E(L, f'screens[4].canvas.params.rows[{i}][1]', f'{100 * fa[i]:.2f}%'); E(L, f'screens[4].canvas.params.rows[{i}][2]', f'{w[i]:.4f}')
dsum = np.abs(np.diff(w[:6])).sum()
wr = np.round(w[:6], 4); dsum = np.abs(np.diff(wr)).sum()   # from the table's 4-place weights
E(L, 'screens[4].widget.answer', R(dsum * 252 / 5, 4)); E(L, 'screens[4].widget.wrong[0].value', R(dsum, 4)); E(L, 'screens[4].widget.wrong[1].value', R(dsum * 252 / 6, 4))
for v_ in np.abs(np.diff(wr)):
    E(L, 'screens[4].hints[1].text', R(v_, 4))
E(L, 'screens[4].feedback.correct', R(turn, 3)); E(L, 'screens[4].explain.text', R(turn * 0.0005 * 100, 2)); E(L, 'screens[5].feedback.correct', R(w.mean(), 4))
E(L, 'screens[5].feedback.correct', R(turn * 0.0005 * 100, 3)); claim('a cap of 1 changes three test days', int(np.sum(0.10 / fa > 1)) == 3)
# look-ahead: 20-day window ending on the sized day, and shifted honestly
la = np.array([np.std(rp3[t - 19:t + 1], ddof=1) for t in range(2000, 3000)]) / 100 * S252
sh = np.array([np.std(rp3[t - 20:t], ddof=1) for t in range(2000, 3000)]) / 100 * S252
wl, ws = np.minimum(0.10 / la, 2), np.minimum(0.10 / sh, 2)
E(L, 'screens[6].prose', R(100 * np.std(wl * r3[2000:], ddof=1) * S252, 2)); E(L, 'screens[6].explain.text', R(100 * np.std(ws * r3[2000:], ddof=1) * S252, 2))
E(L, 'screens[6].explain.text', R(np.abs(np.diff(ws)).sum() * 252 / 999, 2))
# EWMA and the band
ew = np.sqrt(ewma(rp3, 0.94)[2000:]) / 100 * S252; we = np.minimum(0.10 / ew, 2)
E(L, 'screens[7].canvas.params.rows[1][1]', f'{100 * np.std(we * r3[2000:], ddof=1) * S252:.2f}%'); E(L, 'screens[7].canvas.params.rows[1][2]', f'{we.mean():.4f}')
E(L, 'screens[7].canvas.params.rows[1][3]', f'{np.abs(np.diff(we)).sum() * 252 / 999:.3f}')
held = [w[0]]
for x_ in w[1:]:
    held.append(x_ if abs(x_ - held[-1]) > 0.1 else held[-1])
held = np.array(held); tb_ = np.abs(np.diff(held)).sum() * 252 / 999
E(L, 'screens[7].canvas.params.rows[2][1]', f'{100 * np.std(held * r3[2000:], ddof=1) * S252:.2f}%'); E(L, 'screens[7].canvas.params.rows[2][2]', f'{held.mean():.4f}')
E(L, 'screens[7].canvas.params.rows[2][3]', f'{tb_:.3f}'); E(L, 'screens[7].prose', int(np.sum(np.diff(held) != 0)))
E(L, 'screens[7].widget.answer', R((R(turn, 3) - R(tb_, 3)) * 0.0005, 5)); E(L, 'screens[7].feedback.correct', round(100 * (1 - tb_ / turn)))
wt = np.minimum(math.sqrt(252 * VL) / 100 / fa, 2)   # the target is the fit's long run, 14.96% to 2 places
E(L, 'screens[9].hints[2].text', R(wt.mean(), 4)); E(L, 'screens[9].hints[2].text', R(wt.max(), 4)); E(L, 'screens[9].explain.text', R(100 * np.std(wt * r3[2000:], ddof=1) * S252, 2))
E(L, 'screens[9].widget.options[1].why', R(wt.min(), 2)); E(L, 'screens[9].widget.options[2].why', R(100 * 0.1496 / 2, 1))
w20 = np.minimum(0.20 / fa, 2); E(L, 'screens[10].explain.text', R(100 * np.std(w20 * r3[2000:], ddof=1) * S252, 2)); claim('the cap binds at a 20% target', bool(np.any(0.20 / fa > 2)))
ftr = np.sqrt(st_[2000:]) / 100 * S252; E(L, 'screens[10].explain.text', R(100 * np.std(np.minimum(0.10 / ftr, 2) * r3[2000:], ddof=1) * S252, 2))
E(L, 'screens[11].canvas.params.rows[0][1]', R(100 * np.std(r3[2000:], ddof=1) * S252, 2)); E(L, 'screens[11].canvas.params.rows[2][2]', R(w.mean(), 4))
E(L, 'quiz[0].widget.answer', R(0.12 / (0.015 * S252), 3)); E(L, 'quiz[0].widget.wrong[1].value', R(0.12 / (0.015 * 252), 4))

# ================= review-3 =================
L = 'review'
E(L, 'items[0].widget.answer', R(math.sqrt(0.8885 + 0.9864 ** 5 * 3.1115) / 100, 6)); E(L, 'items[0].widget.wrong[0].value', R(math.sqrt(0.8885 + 0.9864 ** 6 * 3.1115) / 100, 6))
E(L, 'items[0].explain.text', R(0.9864 ** 5 * 3.1115, 4)); E(L, 'items[0].explain.text', R(0.8885 + 0.9864 ** 5 * 3.1115, 4))
E(L, 'items[1].widget.answer', R(-q01 * 0.0075 * 2e6, 2)); E(L, 'items[1].widget.wrong[1].value', R(-q05 * 15000, 1))
E(L, 'items[2].widget.answer', R(math.sqrt(4.95), 4))
E(L, 'items[3].widget.answer', R(0.08 / (0.008 * S252), 4)); E(L, 'items[3].widget.wrong[1].value', R(0.008 * S252 / 0.08, 4))
fv = [1.20, 1.10, 1.05, 1.00, 0.98]
v5 = -q01 * math.sqrt(sum(fv)) / 100 * pos
E(L, 'items[4].widget.answer', R(v5, 2)); E(L, 'items[4].widget.wrong[0].value', R(-q01 * math.sqrt(1.2 * 5) / 100 * pos, 2)); E(L, 'items[4].widget.wrong[1].value', R(-q01 * sum(map(math.sqrt, fv)) / 100 * pos, 2))
for p in ('items[4].widget.accept', 'items[4].explain.text'):
    E(L, p, money(v5))
E(L, 'items[4].explain.text', money(-q01 * math.sqrt(1.2 * 5) / 100 * pos))
for v_ in (-t05, -q05, -t01, -q01):
    E(L, 'items[5].feedback.generic', R(v_, 4))
E(L, 'items[6].prose', R(kupiec(2, 1000)[0], 3))
E(L, 'items[8].widget.answer', R(0.7 * 252 / 4 * 0.001, 4)); E(L, 'items[8].widget.wrong[0].value', R(0.1 * 252 / 4 * 0.001, 4)); E(L, 'items[8].widget.wrong[1].value', R(0.7 * 252 / 5 * 0.001, 5))
E(L, 'items[9].widget.answer', R(math.log(0.5) / math.log(0.98), 2)); E(L, 'items[9].explain.text', R(math.log(0.5) / math.log(0.9864), 1))

# ================= homework-3 =================
L = 'homework'
E(L, 'items[1].widget.answer', R(-t01 * 0.012 * pos, 2)); E(L, 'items[1].widget.wrong[0].value', R(3.3649 * 0.012 * pos, 1)); E(L, 'items[1].widget.wrong[1].value', R(-q01 * 12000, 2))
E(L, 'items[2].explain.text', int(np.sum(np.diff(held) != 0))); E(L, 'items[2].explain.text', R(100 * np.std(held * r3[2000:], ddof=1) * S252, 2))
E(L, 'items[2].widget.examples[0].expect', R(turn * 0.0005, 6))
for nm, seed in (('rt27', 27), ('rt31', 31)):
    rt = 100 * simulate_garch(2e-6, 0.08, 0.90, 3000, seed, nu=3)[0]
    pf = fit_garch(rt[:2000]).x; sv = np.sqrt(garch_variance(pf, rt))[2000:] / 100
    xn = int(np.sum(rt[2000:] / 100 < q01 * sv)); xt = int(np.sum(rt[2000:] / 100 < t01 * sv))
    if nm == 'rt27':
        E(L, 'items[3].explain.text', xn); E(L, 'items[3].explain.text', R(kupiec(xn, 1000)[1], 4))
        claim('rt27: t5 survives', kupiec(xt, 1000)[1] >= 0.05)
    else:
        claim('rt31: both fail', kupiec(xn, 1000)[1] < 0.05 and kupiec(xt, 1000)[1] < 0.05)
E(L, 'items[3].explain.text', R(pg, 4)); E(L, 'items[3].explain.text', R(kupiec(nt, 1000)[1], 4))
lr9, p9 = kupiec(9, 250)
E(L, 'items[4].widget.answer', R(lr9, 3)); E(L, 'items[4].feedback.correct', R(p9, 4))
E(L, 'items[4].explain.text', R(241 * math.log(0.99) + 9 * math.log(0.01), 3)); E(L, 'items[4].explain.text', R(241 * math.log(241 / 250) + 9 * math.log(9 / 250), 3))
E(L, 'items[5].prose', R(kupiec(11, 1000)[0], 3)); E(L, 'items[5].widget.options[1].text', R(kupiec(11, 1000)[1], 2))
E(L, 'items[7].model', R((9 - 2.5) / math.sqrt(2.475), 1)); E(L, 'items[7].model', R(lr9, 2)); E(L, 'items[7].model', R(math.sqrt(2.475), 2))
E(L, 'items[7].model', round(100 * power[0.02])); E(L, 'items[7].model', R(pg, 2))

lv.check_wrongs()
for f in fails:
    print('BAD', f)
if fails:
    lv.results.append((False, 'route agreement', ''))
lv.report()
