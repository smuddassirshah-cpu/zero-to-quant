"""garch level 2 performance task `h-garch-nll`: every number recomputed twice.

Run from the repo root with a Python that has NumPy, SciPy and mpmath:
    python docs/reports/garch-2-perf-numbers.py
Exits 0 when every check passes.

Route A is the shipped solution (a plain loop with math.log). Route B is
vectorised: scipy.signal.lfilter for the recursion and scipy.stats.norm.logpdf
for the scores. Route C, for the hand-sized arrays, keeps every variance as an
exact Fraction and takes 40-digit logs with mpmath. The constant-variance case
also has a closed form. The harness copies app/js/engine/widgets/code.js:
prelude, then the code, then each case's call and expect evaluated in that
namespace; isclose is math.isclose(rel 1e-9, abs 1e-12) and an exception fails.
"""
import json
import math
import os
import time
import warnings
from fractions import Fraction as F

import mpmath as mp
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm

mp.mp.dps = 40
warnings.filterwarnings('ignore')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'garch', 'homework-2.json')
FAILS = []
N = [0]


def check(ok, msg):
    N[0] += 1
    if not ok:
        FAILS.append(msg)
        print('FAIL', msg)


hw = json.load(open(HW))
item = [it for it in hw['items'] if it['id'] == 'h-garch-nll'][0]
w = item['widget']
tests, examples = w['tests'], w['examples']

# ---- shape (AUTHORING 5, brief) ----
check(item['performance'] == 'code' and w['kind'] == 'code' and w['language'] == 'python', 'kind')
check(len(tests) >= 3 and len(tests) > len(examples) and len(tests) <= 15, 'test counts')
check(all(e in tests for e in examples), 'examples are among the tests')
check(item['difficulty'] == 5 and 'hints' not in item and 'parts' not in item, 'no hints, no parts')
check(len(hw['items']) <= 12 and sum(1 for it in hw['items'] if it.get('performance')) == 1, 'homework cap, one task')
check(('Check runs %d hidden tests' % len(tests)) in w['how'], 'how states the test count')

# ---- the data: share C, built twice ----
ns0 = {}
exec(w['prelude'], ns0)
rc = ns0['rc']


def share_c_again(n, seed):  # route B: the recursion on variances first, then the returns
    z = np.random.default_rng(seed).standard_normal(n)
    s2 = np.empty(n)
    e = np.empty(n)
    s2[0] = 0.03 / 0.04
    e[0] = math.sqrt(s2[0]) * z[0]
    for t in range(1, n):
        s2[t] = 0.03 + 0.10 * e[t - 1] ** 2 + 0.86 * s2[t - 1]
        e[t] = math.sqrt(s2[t]) * z[t]
    return 0.05 + e


check(len(rc) == 1500 and '1,500 days' in item['prose'], 'share C has 1,500 days, as the prose says')
check(np.allclose(rc, share_c_again(1500, 31), rtol=1e-12, atol=0), 'share C rebuilt by a second route')
check('mean 0.05% a day' in w['prelude'] and abs(rc.mean() - 0.05) < 3 * rc.std() / math.sqrt(1500), 'share C mean near 0.05')


# ---- expected values, two or three routes ----
def allowed(th):
    mu, om, a, b = th
    return om > 0 and a >= 0 and b >= 0 and a + b < 1


def route_b(th, r):
    mu, om, a, b = th
    if not allowed(th):
        return math.inf
    e = np.asarray(r, float) - mu
    v = om / (1 - a - b)
    s2 = np.empty(len(e))
    s2[0] = v
    if len(e) > 1:
        s2[1:] = lfilter([1.0], [1.0, -b], om + a * e[:-1] ** 2, zi=[b * v])[0]
    return float(-np.sum(norm.logpdf(e, loc=0.0, scale=np.sqrt(s2))))


def route_c(th, r):
    mu, om, a, b = (F(repr(float(x))) for x in th)
    e = [F(repr(float(x))) - mu for x in r]
    s2 = om / (1 - a - b)
    tot = mp.mpf(0)
    q = lambda f: mp.mpf(f.numerator) / f.denominator
    for t in range(len(e)):
        if t > 0:
            s2 = om + a * e[t - 1] ** 2 + b * s2
        tot += mp.log(2 * mp.pi) + mp.log(q(s2)) + q(e[t] ** 2 / s2)
    return float(tot / 2)


sol = {}
exec(w['prelude'], sol)
exec(w['solution'], sol)
for i, c in enumerate(tests, 1):
    th, arr = eval(c['call'].replace('garch_nll', '(lambda t, r: (t, r))'), dict(sol))
    want = eval(c['expect'], sol)
    a_val, b_val = sol['garch_nll'](th, arr), route_b(th, arr)
    if math.isinf(want):
        check(not allowed(th) and math.isinf(a_val) and math.isinf(b_val), 'test %d: outside the region, infinite' % i)
        continue
    check(allowed(th), 'test %d: inside the region' % i)
    check(math.isclose(a_val, want, rel_tol=1e-10) and math.isclose(b_val, want, rel_tol=1e-10),
          'test %d: routes A and B give %s' % (i, c['expect']))
    if len(arr) <= 10:
        check(math.isclose(route_c(th, arr), want, rel_tol=1e-10), 'test %d: exact route C' % i)

# the inf tests each break one named condition
reasons = {8: 'alpha + beta = 1', 9: 'alpha + beta > 1', 10: 'omega = 0', 11: 'alpha < 0', 12: 'beta < 0'}
for i, why in reasons.items():
    th = eval(tests[i - 1]['call'].split('garch_nll(')[1].split('), ')[0] + ')')
    mu, om, a, b = th
    got = {'alpha + beta = 1': a + b == 1, 'alpha + beta > 1': a + b > 1, 'omega = 0': om == 0,
           'alpha < 0': a < 0, 'beta < 0': b < 0}
    check(got[why] and sum(got.values()) == 1, 'test %d breaks only "%s"' % (i, why))
# alpha = 0 and beta = 0 are inside (tests 3 and 7)
check('0.5, 0.5, 0.0)' in tests[2]['call'] and '1.2, 0.0, 0.0)' in tests[6]['call'], 'tests 3 and 7 sit on alpha = 0 or beta = 0')

# hand values for test 1, as a reader would work them: variances 1, 1, 1.3
t1 = 0.5 * (3 * math.log(2 * math.pi) + math.log(1.3) + 1 + 4 + 0.25 / 1.3)
check(math.isclose(t1, eval(tests[0]['expect']), rel_tol=1e-10), 'test 1 by hand: variances 1, 1, 1.3')
# constant variance (test 7): closed form n/2 (ln 2pi + ln omega) + sum e^2 / (2 omega)
e7 = rc[:250] - 0.05
t7 = 125 * (math.log(2 * math.pi) + math.log(1.2)) + float(np.sum(e7 ** 2)) / 2.4
check(math.isclose(t7, eval(tests[6]['expect']), rel_tol=1e-10), 'test 7 closed form')
# the truth scores better than the other point on share C
check(eval(tests[4]['expect']) < eval(tests[5]['expect']), 'truth scores below the other point')
# explain: the start's effect on the variance fades by beta a day
s2a, s2b = 0.75, 2.0
for t in range(1, 6):
    s2a = 0.03 + 0.10 * (rc[t - 1] - 0.05) ** 2 + 0.86 * s2a
    s2b = 0.03 + 0.10 * (rc[t - 1] - 0.05) ** 2 + 0.86 * s2b
    check(math.isclose(s2b - s2a, (2.0 - 0.75) * 0.86 ** t, rel_tol=1e-9), 'start gap fades by beta, day %d' % t)


# ---- feedback lines say true things about their tests ----
def theta(i):
    return eval(tests[i - 1]['call'].split('garch_nll(')[1].split('), ')[0] + ')')


bk = item['feedback']['byKey']
check(all(k.startswith('test-') and 1 <= int(k[5:]) <= len(tests) for k in bk), 'byKey keys are tests')
check(theta(1)[0] == 0 and theta(2)[0] != 0 and 'first with' in bk['test-2'], 'test 2 is the first with mu != 0')
check(theta(3)[3] == 0 and 'ARCH(1)' in bk['test-3'], 'test 3 is ARCH(1), beta = 0')
check(theta(8)[2] + theta(8)[3] == 1 and theta(10)[1] == 0, 'tests 8 and 10 as their lines say')
check('three days' in bk['test-1'] and tests[0]['call'].count(',') == 6, 'test 1 has three days')
check(examples[0] == tests[0], 'test 1 is the example')


# ---- harness ----
def close(x, y):
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run(code):
    ns = {}
    exec(w['prelude'], ns)
    exec(code, ns)
    out = []
    for c in tests:
        t0 = time.perf_counter()
        try:
            ok = close(eval(c['call'], ns), eval(c['expect'], ns))
        except Exception:
            ok = False
        out.append(ok and time.perf_counter() - t0 < 5)
    return out


res = run(w['solution'])
check(all(res), 'solution passes every test')
ex_ns = {}
exec(w['prelude'], ex_ns)
exec(w['solution'], ex_ns)
check(all(close(eval(e['call'], ex_ns), eval(e['expect'], ex_ns)) for e in examples), 'solution passes the example')
res = run(w['starter'])
check(not any(res), 'starter fails every test')

S = w['solution']
L_LOOP = "            s2 = omega + alpha * eps[t - 1] ** 2 + beta * s2\n"
L_SCORE = "        total += math.log(2 * math.pi) + math.log(s2) + eps[t] ** 2 / s2\n"
L_CHECK = "    if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:\n"
L_START = "    s2 = omega / (1 - alpha - beta)          # day 1: the long-run variance\n"
L_EPS = "    eps = np.asarray(r, dtype=float) - mu    # residuals about the model's mean\n"
for ln in (L_LOOP, L_SCORE, L_CHECK, L_START, L_EPS):
    check(ln in S, 'solution line present: ' + ln.strip()[:40])
PLANTS = {
    'start at the sample variance (the lesson start)': S.replace(L_START, "    s2 = float(np.var(r))\n"),
    'start at the mean squared residual': S.replace(L_START, "    s2 = float(np.mean((np.asarray(r) - mu) ** 2))\n"),
    'start at omega': S.replace(L_START, "    s2 = omega\n"),
    "today's residual in today's variance": S.replace(L_LOOP, "            s2 = omega + alpha * eps[t] ** 2 + beta * s2\n"),
    'no one half': S.replace('    return 0.5 * total', '    return total'),
    'no ln 2 pi': S.replace(L_SCORE, "        total += math.log(s2) + eps[t] ** 2 / s2\n"),
    'ln sigma for ln sigma^2': S.replace(L_SCORE, "        total += math.log(2 * math.pi) + math.log(math.sqrt(s2)) + eps[t] ** 2 / s2\n"),
    'plus the log-likelihood (sign)': S.replace('    return 0.5 * total', '    return -0.5 * total'),
    'mean ignored': S.replace(L_EPS, "    eps = np.asarray(r, dtype=float)\n"),
    'mean taken out of the score only': S.replace(L_LOOP, "            s2 = omega + alpha * (eps[t - 1] + mu) ** 2 + beta * s2\n"),
    'sample mean for mu': S.replace(L_EPS, "    eps = np.asarray(r, dtype=float) - np.mean(r)\n"),
    'day 1 not scored': S.replace("    for t in range(len(eps)):\n", "    for t in range(len(eps)):\n        if t == 0:\n            continue\n"),
    'no constraint check': S.replace(L_CHECK + "        return math.inf                      # outside the model: the search steps back\n", ""),
    'only alpha + beta checked': S.replace(L_CHECK, "    if alpha + beta >= 1:\n"),
    'signs only, no alpha + beta': S.replace(L_CHECK, "    if omega <= 0 or alpha < 0 or beta < 0:\n"),
    'omega < 0 for omega <= 0': S.replace(L_CHECK, "    if omega < 0 or alpha < 0 or beta < 0 or alpha + beta >= 1:\n"),
    'alpha + beta > 1 for >= 1': S.replace(L_CHECK, "    if omega <= 0 or alpha < 0 or beta < 0 or alpha + beta > 1:\n"),
    'alpha and beta strictly positive': S.replace(L_CHECK, "    if omega <= 0 or alpha <= 0 or beta <= 0 or alpha + beta >= 1:\n"),
    'nan outside, not inf': S.replace("        return math.inf                      # outside", "        return math.nan                      # outside"),
}
for name, code in PLANTS.items():
    check(code != S, 'plant applied: ' + name)
    res = run(code)
    fails = [i + 1 for i, ok in enumerate(res) if not ok]
    check(len(fails) > 0, 'plant caught: ' + name)
    print('plant %-48s first fails test %s, fails %s' % (name, fails[0] if fails else '-', fails))

# ---- timing in CPython ----
ns = {}
exec(w['prelude'], ns)
exec(w['solution'], ns)
t0 = time.perf_counter()
for c in tests:
    eval(c['call'], ns)
check(time.perf_counter() - t0 < 1.0, 'all tests under 1 s in CPython')

print('checks:', N[0], 'failures:', len(FAILS))
raise SystemExit(1 if FAILS else 0)
