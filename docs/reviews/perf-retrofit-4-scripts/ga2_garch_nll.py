"""garch homework-2 h-garch-nll: reader vectorised solution (scipy lfilter, norm.logpdf),
starter, shipped solution and reader-planted slips on every example and test; each expected
value also recomputed with exact fractions where the inputs are short."""
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__))
from harness import item, run, report

it = item('garch', 'homework-2.json', 'h-garch-nll')
W = it['widget']
SOL = W['solution']

READER = '''
import math
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm

def garch_nll(theta, r):
    mu, w, a, b = map(float, theta)
    if not (w > 0 and a >= 0 and b >= 0 and a + b < 1):
        return math.inf
    e = np.asarray(r, float) - mu
    v0 = w / (1 - a - b)
    # s2_t = w + a e_{t-1}^2 + b s2_{t-1}, s2_0 = v0: drive with x_t = w + a e_{t-1}^2 for t >= 1
    x = np.empty(len(e)); x[0] = v0
    x[1:] = w + a * e[:-1] ** 2
    s2 = lfilter([1.0], [1.0, -b], x) if len(e) > 1 else x
    if len(e) > 1:
        # lfilter starts from x[0] = v0 with no carried term, which is the start wanted
        pass
    return float(-norm.logpdf(e, scale=np.sqrt(s2)).sum())
'''

def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)

PLANTS = {
    'start at omega (not the long run)': swap(SOL, 's2 = omega / (1 - alpha - beta)          # day 1: the long-run variance', 's2 = omega'),
    'start at the squared first residual': swap(SOL, 's2 = omega / (1 - alpha - beta)          # day 1: the long-run variance', 's2 = eps[0] ** 2'),
    'alpha + beta <= 1 allowed': swap(SOL, 'alpha + beta >= 1', 'alpha + beta > 1'),
    'alpha > 0 required (ARCH-free GARCH refused)': swap(SOL, 'alpha < 0', 'alpha <= 0'),
    'log of the sd, not the variance': swap(SOL, 'math.log(s2) + eps[t] ** 2 / s2', 'math.log(math.sqrt(s2)) + eps[t] ** 2 / s2'),
    'day 1 left out of the sum': swap(SOL, '        total += math.log', '        if t == 0:\n            continue\n        total += math.log'),
    'returns plus the log-likelihood': swap(SOL, 'return 0.5 * total', 'return -0.5 * total'),
    'raw returns in the recursion (mu only in the score)': swap(swap(SOL, 'eps = np.asarray(r, dtype=float) - mu', 'raw = np.asarray(r, dtype=float); eps = raw - mu'), 'alpha * eps[t - 1] ** 2', 'alpha * raw[t - 1] ** 2'),
}

def exact_nll(theta, r):
    mu, w, a, b = (F(str(v)) for v in theta)
    e = [F(str(x)) - mu for x in r]
    s2 = w / (1 - a - b); tot = 0.0
    for t in range(len(e)):
        if t:
            s2 = w + a * e[t - 1] ** 2 + b * s2
        tot += math.log(2 * math.pi) + math.log(s2) + float(e[t] ** 2 / s2)
    return 0.5 * tot

fails = 0
fe, ft = report('starter', run(it, W['starter']))
if not ft: print('  FAIL starter passes'); fails += 1
for lab, src in (('shipped solution', SOL), ('reader solution', READER)):
    fe, ft = report(lab, run(it, src))
    if fe or ft: print('  FAIL', lab); fails += 1
for lab, src in PLANTS.items():
    fe, ft = report('plant: ' + lab, run(it, src))
    if not ft: print('  FAIL plant uncaught:', lab); fails += 1
for c in W['tests']:
    call = c['call']
    if 'np.array(' in call and "inf" not in c['expect']:
        args = eval(call.replace('garch_nll', '').replace('np.array', 'list'))
        v = exact_nll(*args); e = float(c['expect'])
        ok = math.isclose(v, e, rel_tol=1e-9)
        print('exact route %-60s %.10f vs %s %s' % (call[:60], v, c['expect'], 'ok' if ok else 'FAIL'))
        fails += not ok
print('failures:', fails)
sys.exit(1 if fails else 0)
