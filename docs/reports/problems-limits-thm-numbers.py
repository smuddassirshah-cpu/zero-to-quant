"""Recompute every number in app/content/courses/limits-thm/problems-<n>.json twice.

Method 1 is exact or closed form (fractions.Fraction, math.comb, the pmf or cdf
written out). Method 2 is independent: scipy.stats, a sum of the pmf term by term,
an enumeration of hands or paths, or a seeded simulation where a closed form is the
only other route. For each numeric part the script checks that the two methods
agree; that the JSON key lies within its tol of the value; that the key is the value
at the rounding the question asks for; that every `wrong` value matches its named
slip, lies outside the key's band and does not overlap another `wrong`; and that the
number printed last in `feedback.correct` (after its last `=` or `\\approx`) is
accepted by the part's own tolerance. Choice parts check the keyed option. Stated
numbers in explanations are checked with `stated`. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-limits-thm-numbers.py
"""
import json, os, re, sys, itertools, random
from fractions import Fraction as F
from math import comb, exp, log, sqrt, factorial, isclose, ceil, erf, pi
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'limits-thm')
fails, checks = [], 0


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {it['id']: it for it in d['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def printed_value(text):
    """The number after the last '=' or '\\approx' in a feedback line."""
    t = text.replace('{,}', '').replace('\\,', '')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', t))
    if not hits:
        return None
    return float(hits[-1].group(2))


def num(items, iid, k, exact, alt, slips=None, dp=None, agree=1e-9, printed=True):
    """Part k (1-based) of item iid: a numeric key.
    exact, alt: the value by two methods; dp: the decimal places the question asks for."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if dp is not None:
        r = round(e, dp)
        ok(abs(r - w['answer']) <= 1e-9 or abs(r - e) <= tol, f'{tag}: rounded value {r} outside band')
        ok(abs(r - w['answer']) <= tol + 1e-9, f'{tag}: value at {dp} dp {r} not accepted')
    if printed:
        pv = printed_value(part['feedback']['correct'])
        ok(pv is not None, f'{tag}: no printed value in feedback.correct')
        if pv is not None:
            ok(abs(pv - w['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(x['value'] - float(val)) <= max(wt, 10 ** -(dp or 4) / 2 + 1e-12),
           f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def pick(items, iid, k, correct_id):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')


def stated(label, shown, value, tol):
    ok(abs(shown - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def pois_pmf(k, lam):
    return exp(-lam) * lam ** k / factorial(k)


def pois_cdf(k, lam):
    return sum(pois_pmf(j, lam) for j in range(k + 1))


def binom_pmf(k, n, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


# ------------------------------------------------------------------ level 1
L1 = load(1)

# p-dropped-ticks: Bin(400, 0.004), Pois(1.6), alarm at 4 or more
n, p, lam = 400, F(4, 1000), 1.6
p0 = (1 - p) ** n
num(L1, 'p-dropped-ticks', 1, p0, stats.binom.pmf(0, n, float(p)),
    {'poisson': exp(-lam), 'complement': 1 - p0, 'one-tick': 1 - p}, dp=4)
alarm = 1 - pois_cdf(3, lam)
num(L1, 'p-dropped-ticks', 2, alarm, stats.poisson.sf(3, lam),
    {'from-three': 1 - pois_cdf(2, lam), 'exactly-four': pois_pmf(4, lam),
     'no-alarm': pois_cdf(3, lam), 'from-five': 1 - pois_cdf(4, lam)}, dp=4)
stated('P(X<=3) terms 1.6^3/6', 0.6827, F(4096, 6000), 0.00005)
stated('exact binomial P(X>=4) near Poisson', 0.0788, stats.binom.sf(3, n, float(p)), 0.001)
a4 = 0.0788                                   # the rounded value the part tells the learner to use
quiet30 = (1 - a4) ** 30
num(L1, 'p-dropped-ticks', 3, quiet30, stats.geom.sf(30, a4),
    {'at-least-one': 1 - quiet30, 'poisson-alarms': exp(-30 * a4), 'from-three': (1 - 0.2166) ** 30}, dp=4)
ok(abs((1 - alarm) ** 30 - quiet30) < 0.00005, 'p-dropped-ticks p3: unrounded alarm chance changes the 4 dp answer')
num(L1, 'p-dropped-ticks', 4, 1 / a4, stats.geom.mean(a4),
    {'failures': 1 / a4 - 1, 'quiet': 1 / (1 - a4), 'from-three': 1 / 0.2166, 'alarm-count': 30 * a4}, dp=1)
ok(round(1 / alarm, 1) == 12.7, 'p-dropped-ticks p4: unrounded mean wait is not 12.7')
waits = {k: 1 / (1 - pois_cdf(k - 1, lam)) for k in range(3, 9)}
k_best = min(k for k in waits if waits[k] >= 60)
sim_k = min(k for k in range(3, 9) if 1 / stats.poisson.sf(k - 1, lam) >= 60)
num(L1, 'p-dropped-ticks', 5, k_best, sim_k, {'five': 5, 'seven': 7}, dp=0)
stated('wait at k=5', 42, waits[5], 0.5)
stated('wait at k=6', 166, waits[6], 0.5)
stated('P(X>=5)', 0.0237, 1 - pois_cdf(4, lam), 0.00005)
stated('P(X>=6)', 0.0060, 1 - pois_cdf(5, lam), 0.00005)
stated('1/60', 0.0167, F(1, 60), 0.00005)

# p-block-calls: 10 clients, 3 takers, calls without replacement
clients = [1] * 3 + [0] * 7
orders = list(itertools.permutations(range(10), 5))
def share(pred):
    hits = sum(1 for o in orders if pred([clients[i] for i in o]))
    return F(hits, len(orders))
b1 = F(7, 10) * F(6, 9) * F(3, 8)
num(L1, 'p-block-calls', 1, b1, share(lambda c: c[:3] == [0, 0, 1]),
    {'geometric': 0.7 * 0.7 * 0.3, 'two-misses': F(7, 10) * F(6, 9), 'third-alone': F(3, 10)}, dp=4)
b2 = F(comb(7, 4), comb(10, 4))
hands = list(itertools.combinations(range(10), 4))
num(L1, 'p-block-calls', 2, b2, F(sum(1 for h in hands if not any(clients[i] for i in h)), len(hands)),
    {'geometric': 0.7 ** 4, 'at-least-one': 1 - b2, 'exactly-one': F(3 * comb(7, 3), comb(10, 4))}, dp=4)
stated('path route 1/6', 0, F(7, 10) * F(6, 9) * F(5, 8) * F(4, 7) - F(1, 6), 0)
num(L1, 'p-block-calls', 3, F(7, 10) ** 4, stats.geom.sf(4, 0.3),
    {'list': b2, 'three': F(7, 10) ** 3, 'complement': 1 - F(7, 10) ** 4}, dp=4)
b4 = share(lambda c: c == [0, 0, 0, 0, 1]) / share(lambda c: c[:4] == [0, 0, 0, 0])
num(L1, 'p-block-calls', 4, F(3, 6), b4,
    {'memoryless': F(3, 10), 'unconditional': b2 * F(1, 2), 'one-removed': F(3, 9)}, dp=4)
pick(L1, 'p-block-calls', 5, 'memory')

# p-fund-record: beats cash w.p. 0.65; T ~ Geo(0.35); X ~ Bin(12, 0.65)
q, r = F(65, 100), F(35, 100)
num(L1, 'p-fund-record', 1, q * q * r, stats.geom.pmf(3, 0.35),
    {'swapped': r * r * q, 'tail': q ** 3, 'no-lag': q ** 2}, dp=4)
stated('0.65^2 x 0.35 printed in full', 0.147875, q * q * r, 0)
num(L1, 'p-fund-record', 2, q ** 6, 1 - sum(stats.geom.pmf(j, 0.35) for j in range(1, 7)),
    {'five': q ** 5, 'complement': 1 - q ** 6, 'pmf': q ** 5 * r, 'swapped': r ** 6}, dp=4)
num(L1, 'p-fund-record', 3, q ** 12 / q ** 6, stats.geom.sf(12, 0.35) / stats.geom.sf(6, 0.35),
    {'unconditional': q ** 12, 'complement': 1 - q ** 6}, dp=4)
num(L1, 'p-fund-record', 4, q ** 12, stats.binom.pmf(12, 12, 0.65),
    {'from-part-3': q ** 6, 'coefficient': 12 * q ** 12, 'eleven': binom_pmf(11, 12, q)}, dp=4)
ok(abs(0.0754 ** 2 - 0.0057) <= 0.00005, 'p-fund-record p4: 0.0754^2 not accepted')
tail10 = sum(binom_pmf(k, 12, q) for k in (10, 11, 12))
enum10 = F(0)
for s in itertools.product((0, 1), repeat=12):
    if sum(s) >= 10:
        enum10 += q ** sum(s) * r ** (12 - sum(s))
num(L1, 'p-fund-record', 5, tail10, enum10,
    {'no-coefficients': q ** 10 * r ** 2 + q ** 11 * r + q ** 12, 'only-ten': binom_pmf(10, 12, q),
     'above-ten': binom_pmf(11, 12, q) + q ** 12}, dp=4)
stated('P(X=10)', 0.1088, binom_pmf(10, 12, q), 0.00005)
stated('P(X=11)', 0.0368, binom_pmf(11, 12, q), 0.00005)
stated('one in seven', 7, 1 / tail10, 0.5)

# p-settlement-checks: Hyper(N=2000, K=60, n=50)
NN, KK, nn = 2000, 60, 50
pp = F(KK, NN)
num(L1, 'p-settlement-checks', 1, nn * pp, stats.hypergeom.mean(NN, KK, nn),
    {'share': pp, 'ratio': F(60, 50)}, dp=4)
var = nn * pp * (1 - pp) * F(NN - nn, NN - 1)
num(L1, 'p-settlement-checks', 2, var, stats.hypergeom.var(NN, KK, nn),
    {'binomial': nn * pp * (1 - pp), 'factor-n-over-N': nn * pp * (1 - pp) * F(NN - nn, NN),
     'poisson': nn * pp, 'sd': sqrt(var)}, dp=4)
num(L1, 'p-settlement-checks', 3, (1 - pp) ** nn, stats.binom.pmf(0, nn, 0.03),
    {'poisson': exp(-1.5), 'complement': 1 - (1 - pp) ** nn, 'one-fail': binom_pmf(1, nn, pp)}, dp=4)
exact0 = F(comb(NN - KK, nn), comb(NN, nn))
stated('exact hypergeometric P(X=0)', 0.2139, exact0, 0.00005)
stated('exact P(X=0) by scipy', 0.2139, stats.hypergeom.pmf(0, NN, KK, nn), 0.00005)
n_bin = ceil(log(0.01) / log(0.97))
n_step = next(m for m in range(1, 1000) if 1 - 0.97 ** m >= 0.99)
num(L1, 'p-settlement-checks', 4, n_bin, n_step,
    {'rounded-down': n_bin - 1, 'ninety': ceil(log(0.1) / log(0.97))}, dp=0)
stated('log ratio', 151.2, log(0.01) / log(0.97), 0.05)
stated('n=151 chance', 0.98994, 1 - 0.97 ** 151, 0.000005)
stated('n=152 chance', 0.9902, 1 - 0.97 ** 152, 0.00005)
stated('152 share of the day', 7.6, 100 * 152 / NN, 0)
n_exact = next(m for m in range(1, 400) if 1 - comb(NN - KK, m) / comb(NN, m) >= 0.99)
n_exact2 = next(m for m in range(1, 400) if stats.hypergeom.sf(0, NN, KK, m) >= 0.99)
stated('exact smallest n', 146, n_exact, 0)
stated('exact smallest n by scipy', 146, n_exact2, 0)
pick(L1, 'p-settlement-checks', 5, 'enough')


# ------------------------------------------------------------------ level 2
from scipy.integrate import quad
Phi = stats.norm.cdf
L2 = load(2)

# p-quote-life: f(t) = c(3 - t) on [0, 3]
c = F(1) / (F(1, 2) * 3 * 3)
c_quad = 1 / quad(lambda t: 3 - t, 0, 3)[0]
num(L2, 'p-quote-life', 1, c, c_quad, {'height': F(1, 3), 'no-half': F(1, 9), 'reciprocal': F(9, 2)}, dp=4)
f = lambda t: float(c) * (3 - t)
tail = lambda t: F(3 - t) ** 2 / 9 if isinstance(t, int) else (3 - t) ** 2 / 9
num(L2, 'p-quote-life', 2, c * F(1, 2), quad(f, 2, 3)[0],
    {'left': 1 - c * F(1, 2), 'height': c * 1, 'width': F(1, 3)}, dp=4)
stated('tail formula at 2', 0, quad(f, 2, 3)[0] - (3 - 2) ** 2 / 9, 1e-12)
meanT = c * (F(27, 2) - 9)
num(L2, 'p-quote-life', 3, meanT, quad(lambda t: t * f(t), 0, 3)[0],
    {'midpoint': F(3, 2), 'no-c': quad(lambda t: t * (3 - t), 0, 3)[0]}, dp=4)
num(L2, 'p-quote-life', 4, exp(-2), stats.expon.sf(2, scale=float(meanT)),
    {'triangle': F(1, 9), 'cdf': 1 - exp(-2), 'from-midpoint': exp(-2 / 1.5)}, dp=4)
cond = quad(f, 2.5, 3)[0] / quad(f, 2, 3)[0]
num(L2, 'p-quote-life', 5, F(1, 4), cond,
    {'memoryless': exp(-0.5), 'unconditional': (3 - 2.5) ** 2 / 9, 'fresh': (3 - 0.5) ** 2 / 9}, dp=4)
stated('fresh half second', 0.6944, 2.5 ** 2 / 9, 0.00005)

# p-digital-share: S1 = 80 exp((m - s^2/2) + s Z), m = 0.06, s = 0.3
S0, m, s = 80, 0.06, 0.3
drift = m - s * s / 2
lnS = stats.lognorm(s=s, scale=S0 * exp(drift))       # scipy's lognormal: median = scale
rng = random.Random(7)
sim = [S0 * exp(drift + s * rng.gauss(0, 1)) for _ in range(200000)]
sim.sort()
num(L2, 'p-digital-share', 1, S0 * exp(drift), lnS.median(),
    {'mean': S0 * exp(m), 'today': 80, 'plus-drag': S0 * exp(m + s * s / 2)}, dp=2)
stated('log drift', 0.015, drift, 1e-12)
ok(abs(sim[100000] - S0 * exp(drift)) < 0.3, 'p-digital-share: simulated median far from 81.21')
num(L2, 'p-digital-share', 2, S0 * exp(m), lnS.mean(),
    {'median': S0 * exp(drift), 'full-variance': S0 * exp(drift + s * s)}, dp=2)
ok(abs(sum(sim) / len(sim) - S0 * exp(m)) < 0.2, 'p-digital-share: simulated mean far from 84.95')
z3 = (log(S0 * exp(m) / S0) - drift) / s
stated('z for the mean', 0.15, z3, 1e-12)
num(L2, 'p-digital-share', 3, Phi(0.15), lnS.cdf(S0 * exp(m)),
    {'half': 0.5, 'above': 1 - Phi(0.15)}, dp=4)
z4 = (log(100 / S0) - drift) / s
stated('z for 100', 0.69, z4, 0.005)
stated('Phi(0.69) as printed', 0.7549, Phi(0.69), 0.00005)
stated('ln 1.25', 0.2231, log(1.25), 0.00005)
num(L2, 'p-digital-share', 4, 1 - Phi(round(z4, 2)), 1 - 0.7549,
    {'phi': Phi(0.69), 'no-drag': 1 - Phi(round((log(1.25) - m) / s, 2)),
     'plus-drag': 1 - Phi(round((log(1.25) - m - s * s / 2) / s, 2))}, dp=4, agree=1e-4)
ok(abs(lnS.sf(100) - L2['p-digital-share']['parts'][3]['widget']['answer']) <= 0.0015,
   'p-digital-share p4: exact chance not accepted')
stated('unrounded z', 0.6938, z4, 0.00005)
stated('unrounded chance', 0.2439, lnS.sf(100), 0.00005)
q05 = S0 * exp(drift - 1.645 * s)
num(L2, 'p-digital-share', 5, S0 - q05, S0 - lnS.ppf(Phi(-1.645)),
    {'no-drag': S0 - S0 * exp(m - 1.645 * s), 'two-tailed': S0 - S0 * exp(drift - 1.96 * s),
     'from-mean': S0 * exp(m) - q05, 'normal-price': 1.645 * s * S0}, dp=2, agree=1e-6)
stated('5% price', 49.58, q05, 0.005)
stated('exponent', -0.4785, drift - 1.645 * s, 1e-12)
ok(abs(S0 - sim[10000] - (S0 - q05)) < 0.3, 'p-digital-share p5: simulated 5% price far off')

# p-bounded-pnl: f(x) = (6 - |x|)/36 on [-6, 6]
g = lambda x: (6 - abs(x)) / 36
ok(abs(quad(g, -6, 6)[0] - 1) < 1e-12, 'p-bounded-pnl: not a density')
num(L2, 'p-bounded-pnl', 1, F(9, 72), quad(g, -6, -3)[0],
    {'no-half': F(9, 36), 'height': F(3, 36), 'complement': 1 - F(9, 72)}, dp=4)
var_g = F(2, 36) * (432 - 324)
num(L2, 'p-bounded-pnl', 2, var_g, quad(lambda x: x * x * g(x), -6, 6)[0],
    {'one-side': var_g / 2, 'sd': sqrt(6), 'uniform': F(144, 12)}, dp=4)
v95 = 6 - sqrt(3.6)
v95b = -__import__('scipy.optimize', fromlist=['brentq']).brentq(lambda v: quad(g, -6, v)[0] - 0.05, -6, 0)
num(L2, 'p-bounded-pnl', 3, v95, v95b, {'half-area': 6 - sqrt(1.8), 'ten-pc': 6 - sqrt(7.2)}, dp=2, agree=1e-8)
n95 = 1.645 * sqrt(6)
num(L2, 'p-bounded-pnl', 4, n95, -stats.norm.ppf(0.05, 0, sqrt(6)),
    {'variance': 1.645 * 6, 'two-tailed': 1.96 * sqrt(6), 'triangle': v95}, dp=2, agree=1e-3)
v99 = 6 - sqrt(0.72)
n99 = 2.326 * sqrt(6)
v99b = -__import__('scipy.optimize', fromlist=['brentq']).brentq(lambda v: quad(g, -6, v)[0] - 0.01, -6, 0)
num(L2, 'p-bounded-pnl', 5, n99 - v99, -stats.norm.ppf(0.01, 0, sqrt(6)) - v99b,
    {'sign': v99 - n99, 'at-95': n95 - v95, 'variance': 2.326 * 6 - v99}, dp=2, agree=1e-3)
stated('rounded gap', 0.55, round(n99, 2) - round(v99, 2), 1e-9)
stated('triangle 99', 5.15, v99, 0.005)
stated('normal 99', 5.70, n99, 0.005)
stated('sd', 2.4495, sqrt(6), 0.00005)

# p-default-drag: hazard 0.05, S1 = 40 exp((m - s^2/2) + s Z), m = 0.04, s = 0.35
S0, m, s, lam = 40, 0.04, 0.35, 0.05
drift = m - s * s / 2
surv = exp(-lam)
num(L2, 'p-default-drag', 1, surv, stats.expon.sf(1, scale=1 / lam), {'rate': 1 - lam, 'default': 1 - surv}, dp=4)
LN = stats.lognorm(s=s, scale=S0 * exp(drift))
num(L2, 'p-default-drag', 2, S0 * exp(m), LN.mean(), {'median': S0 * exp(drift), 'today': 40}, dp=2)
stated('drag', 0.0613, s * s / 2, 0.0000501)
rng = random.Random(11)
tot, up, M = 0.0, 0, 200000
for _ in range(M):
    if rng.expovariate(lam) > 1:
        price = S0 * exp(drift + s * rng.gauss(0, 1))
        tot += price
        up += price > 40
num(L2, 'p-default-drag', 3, surv * S0 * exp(m), surv * LN.mean(),
    {'survives': S0 * exp(m), 'linear': 0.95 * 41.63, 'median': 0.9512 * 39.16}, dp=2)
ok(abs(tot / M - surv * S0 * exp(m)) < 0.15, 'p-default-drag p3: simulation far from 39.60')
ok(abs(0.9512 * 41.63 - 39.60) <= 0.005, 'p-default-drag p3: rounded route not accepted')
z = -drift / s
stated('z for 40', 0.06, z, 0.005)
stated('Phi(0.06)', 0.5239, Phi(0.06), 0.00005)
stated('Phi(0.11)', 0.5438, Phi(0.11), 0.00005)
num(L2, 'p-default-drag', 4, 1 - Phi(round(z, 2)), 1 - 0.5239,
    {'phi': Phi(0.06), 'no-drag': 1 - Phi(round(m / s, 2)), 'half': 0.5}, dp=4, agree=1e-4)
ok(abs(LN.sf(40) - 0.4761) <= 0.0005, 'p-default-drag p4: exact chance not accepted')
num(L2, 'p-default-drag', 5, 0.9512 * 0.4761, surv * LN.sf(40),
    {'survivor': 0.4761, 'no-drag': 0.9512 * 0.4562}, dp=4, agree=0.0005)
ok(abs(up / M - surv * LN.sf(40)) < 0.005, 'p-default-drag p5: simulation far from 0.4526')
# slips reached by a calculator (unrounded z) and by the table (z to 2 dp) both fall in their bands
def band_has(L, iid, k, wid, vals):
    w = {x['id']: x for x in L[iid]['parts'][k - 1]['widget']['wrong']}[wid]
    for v in vals:
        ok(abs(v - w['value']) <= w['tol']['abs'] + 1e-12, f'{iid} p{k}: {wid} route {v:.5f} outside its band')
band_has(L2, 'p-digital-share', 4, 'no-drag', [1 - Phi((log(1.25) - 0.06) / 0.3), 1 - Phi(round((log(1.25) - 0.06) / 0.3, 2))])
band_has(L2, 'p-digital-share', 4, 'plus-drag', [1 - Phi((log(1.25) - 0.105) / 0.3), 1 - Phi(round((log(1.25) - 0.105) / 0.3, 2))])
band_has(L2, 'p-default-drag', 4, 'no-drag', [1 - Phi(0.04 / 0.35), 1 - Phi(round(0.04 / 0.35, 2))])
band_has(L2, 'p-default-drag', 5, 'no-drag', [surv * (1 - Phi(0.04 / 0.35)), 0.9512 * (1 - Phi(round(0.04 / 0.35, 2)))])


# ------------------------------------------------------------------ level 3
L3 = load(3)

# p-maker-days: 900 trades, mean 0.40, sd 6; 250 days
day_var = 900 * 6 ** 2
num(L3, 'p-maker-days', 1, sqrt(day_var), 6 * sqrt(900),
    {'add-sds': 900 * 6, 'one-trade': 6, 'variance': day_var}, dp=0)
rng = random.Random(3)
sims = []
for _ in range(4000):
    sims.append(sum(rng.gauss(0.40, 6) for _ in range(900)))
sd_sim = sqrt(sum((x - 360) ** 2 for x in sims) / len(sims))
ok(abs(sd_sim - 180) < 6, 'p-maker-days p1: simulated sd far from 180')
num(L3, 'p-maker-days', 2, 1 - 0.9772, Phi(-2),
    {'phi': 0.9772, 'two-tailed': 2 * 0.0228, 'from-add-sds': Phi(-360 / 5400)}, dp=4, agree=0.0001)
stated('Phi(2) as printed', 0.9772, Phi(2), 0.00005)
pl = 0.0228
mu_x, sd_x = 250 * pl, sqrt(250 * pl * (1 - pl))
z = (9.5 - mu_x) / sd_x
stated('z to 2 dp', 1.61, z, 0.005)
stated('sd of losing days', 2.360, sd_x, 0.0005)
stated('Phi(1.61)', 0.9463, Phi(1.61), 0.00005)
num(L3, 'p-maker-days', 3, 1 - Phi(1.61), 1 - 0.9463,
    {'phi': Phi(1.61), 'no-correction': 1 - Phi((10 - mu_x) / sd_x), 'wrong-side': 1 - Phi((10.5 - mu_x) / sd_x),
     'poisson-sd': 1 - Phi((9.5 - mu_x) / sqrt(mu_x))}, dp=4, agree=0.0001)
ok(abs(1 - Phi(z) - 0.0537) <= 0.0001, 'p-maker-days p3: unrounded z changes the answer')
for wid, zz in (('no-correction', (10 - mu_x) / sd_x), ('wrong-side', (10.5 - mu_x) / sd_x), ('poisson-sd', (9.5 - mu_x) / sqrt(mu_x))):
    w3 = {x['id']: x for x in L3['p-maker-days']['parts'][2]['widget']['wrong']}[wid]
    ok(abs(round(1 - Phi(round(zz, 2)), 4) - w3['value']) <= w3['tol']['abs'], f'p-maker-days p3: table route of {wid} outside its band')
exact_b = stats.binom.sf(9, 250, pl)
exact_b2 = 1 - sum(binom_pmf(k, 250, F(228, 10000)) for k in range(10))
pois_b = stats.poisson.sf(9, mu_x)
pois_b2 = 1 - pois_cdf(9, mu_x)
stated('exact binomial tail', 0.0626, exact_b, 0.00005)
stated('exact binomial tail, Fraction', 0.0626, exact_b2, 0.00005)
stated('Poisson tail', 0.0648, pois_b, 0.00005)
stated('Poisson tail by sum', 0.0648, pois_b2, 0.00005)
stated('np(1-p)', 5.57, 250 * pl * (1 - pl), 0.005)
stated('Poisson error', 0.0022, pois_b - exact_b, 0.00005)
stated('normal error', 0.0089, exact_b - (1 - Phi(1.61)), 0.00005)
stated('normal 14% low', 14, 100 * (exact_b - 0.0537) / exact_b, 0.5)
pick(L3, 'p-maker-days', 4, 'poisson')

# p-direction-calls: Bin(400, 0.5), 216 right
num(L3, 'p-direction-calls', 1, sqrt(400 * 0.25), stats.binom.std(400, 0.5),
    {'variance': 100, 'share': 0.025, 'no-q': sqrt(200)}, dp=0)
num(L3, 'p-direction-calls', 2, 1 - Phi(1.55), 1 - 0.9394,
    {'phi': Phi(1.55), 'no-correction': 1 - Phi(1.6), 'wrong-side': 1 - Phi(1.65), 'two-tailed': 2 * (1 - 0.9394)},
    dp=4, agree=0.0001)
stated('Phi(1.55)', 0.9394, Phi(1.55), 0.00005)
stated('exact binomial tail at 216', 0.0605, stats.binom.sf(215, 400, 0.5), 0.00005)
stated('exact tail by Fraction sum', 0.0605, float(sum(F(comb(400, k), 2 ** 400) for k in range(216, 401))), 0.00005)
best12 = 1 - 0.9394 ** 12
rng = random.Random(5)
hits = sum(1 for _ in range(200000) if any(rng.random() < 0.0606 for _ in range(12)))
num(L3, 'p-direction-calls', 3, best12, 1 - (1 - 0.0606) ** 12,
    {'added': 12 * 0.0606, 'one': 0.0606, 'no-correction': 1 - (1 - 0.0548) ** 12}, dp=4)
ok(abs(hits / 200000 - best12) < 0.005, 'p-direction-calls p3: simulation far from 0.5277')
stated('all 12 short', 0.4723, 0.9394 ** 12, 0.00005)
tgt = 1 - 0.95 ** (1 / 12)
stated('per-signal tail', 0.0043, tgt, 0.00005)
stated('z for the tail', 2.63, stats.norm.isf(tgt), 0.005)
stated('Phi(2.63)', 0.9957, Phi(2.63), 0.00005)
k_norm = ceil(200.5 + 2.63 * 10)
k_exact = next(k for k in range(200, 400) if stats.binom.sf(k - 1, 400, 0.5) <= tgt)
k_normal_full = next(k for k in range(200, 400) if 1 - Phi((k - 0.5 - 200) / 10) <= tgt)
num(L3, 'p-direction-calls', 4, k_norm, k_exact,
    {'one-signal': ceil(200.5 + 1.645 * 10), 'rounded-down': k_norm - 1}, dp=0)
stated('k by unrounded z', 227, k_normal_full, 0)
stated('z at k=226', 2.55, (225.5 - 200) / 10, 1e-12)
stated('share right at 227', 57, 100 * 227 / 400, 0.5)
n5 = (2 * 0.5 / 0.04) ** 2
n5b = next(n for n in range(1, 5000) if 0.04 * sqrt(n) / 0.5 >= 2 - 1e-12)
num(L3, 'p-direction-calls', 5, n5, n5b,
    {'one-se': ceil((1 * 0.5 / 0.04) ** 2), 'root': 25, 'one-point-96': ceil((1.96 * 0.5 / 0.04) ** 2)}, dp=0)
stated('625 days over two years', 2.48, 625 / 252, 0.01)

# p-rejected-orders: mean 12, sd 4
num(L3, 'p-rejected-orders', 1, F(12, 36), 12 / 36, {'reversed': 3, 'sd': F(4, 36)}, dp=4)
k6 = (36 - 12) / 4
num(L3, 'p-rejected-orders', 2, F(1, 36), (4 / 24) ** 2,
    {'not-squared': F(4, 24), 'from-zero': F(1, 81), 'markov': F(1, 3)}, dp=4)
stated('k', 6, k6, 0)
stated('twelvefold', 12, F(1, 3) / F(1, 36), 0)
n3 = 16 / (0.05 * 1 ** 2)
n3b = next(n for n in range(1, 2000) if 16 / n <= 0.05)
num(L3, 'p-rejected-orders', 3, n3, n3b, {'ninety-five': ceil(16 / 0.95), 'sd': 4 / 0.05, 'clt': 62}, dp=0)
n4 = ceil((1.96 * 4) ** 2)
n4b = next(n for n in range(1, 2000) if 1.96 * 4 / sqrt(n) <= 1)
num(L3, 'p-rejected-orders', 4, n4, n4b,
    {'rounded-down': n4 - 1, 'one-tail': ceil((1.645 * 4) ** 2), 'no-square': ceil(1.96 * 4), 'chebyshev': 320}, dp=0)
stated('7.84^2', 61.5, (1.96 * 4) ** 2, 0.05)
stated('margin at 61', 1.004, 1.96 * 4 / sqrt(61), 0.0005)
stated('a fifth of 320', 0.2, 62 / 320, 0.01)

# p-fund-months: sd 4%, 36 months, average 1.2%
se = 4 / sqrt(36)
num(L3, 'p-fund-months', 1, F(4, 6), se, {'over-n': F(4, 36), 'sd': 4, 'variance': F(16, 36)}, dp=4)
num(L3, 'p-fund-months', 2, 1.2 / se, 1.2 * sqrt(36) / 4,
    {'raw-sd': 1.2 / 4, 'over-n': 1.2 / (4 / 36), 'inverted': se / 1.2}, dp=2)
num(L3, 'p-fund-months', 3, 1 / 1.8 ** 2, F(100, 324), {'not-squared': 1 / 1.8, 'normal': 2 * (1 - Phi(1.8))}, dp=4)
stated('Phi(1.8)', 0.9641, Phi(1.8), 0.00005)
num(L3, 'p-fund-months', 4, 2 * (1 - 0.9641), 2 * stats.norm.sf(1.8),
    {'one-tail': 1 - 0.9641, 'chebyshev': 1 / 1.8 ** 2, 'phi': 0.9641}, dp=4, agree=0.0001)
rng = random.Random(9)
tails = sum(1 for _ in range(400000) if abs(rng.gauss(0, 1)) >= 1.8)
ok(abs(tails / 400000 - 0.0718) < 0.002, 'p-fund-months p4: simulation far from 0.0718')
stated('one in 14', 14, 1 / 0.0718, 0.5)
stated('about a quarter', 0.25, 0.0718 / 0.3086, 0.02)
n_m = (2 * 4 / 1.2) ** 2
n_mb = next(n for n in range(1, 500) if 1.2 * sqrt(n) / 4 >= 2)
num(L3, 'p-fund-months', 5, ceil(n_m), n_mb,
    {'one-se': ceil((4 / 1.2) ** 2), 'rounded-down': ceil(n_m) - 1, 'one-point-96': ceil((1.96 * 4 / 1.2) ** 2)}, dp=0)
stated('sqrt n', 6.67, 2 * 4 / 1.2, 0.005)
stated('n', 44.4, n_m, 0.05)
stated('t at 44', 1.99, 1.2 * sqrt(44) / 4, 0.005)



# ------------------------------------------------------------------ level 4
L4 = load(4)
import sympy as sp
from scipy.integrate import quad, dblquad
from scipy.optimize import minimize_scalar
x_, y_, t_, s_ = sp.symbols('x y t s', positive=True)
# every expression string in the set, hand-translated; each JSON string must appear here
TEX = {
    'e^{-x}': sp.exp(-x_), '1/e^x': 1 / sp.exp(x_), 'e^{-y}': sp.exp(-y_), '1-e^{-x}': 1 - sp.exp(-x_), '1': sp.Integer(1),
    'e^{-t/2}-e^{-t}': sp.exp(-t_ / 2) - sp.exp(-t_), 'e^{-0.5t}-e^{-t}': sp.exp(-sp.Rational(1, 2) * t_) - sp.exp(-t_),
    '0.5e^{-1.5t}': sp.Rational(1, 2) * sp.exp(-sp.Rational(3, 2) * t_), 'e^{-t}+0.5e^{-t/2}': sp.exp(-t_) + sp.exp(-t_ / 2) / 2,
    '0.25te^{-t/2}': t_ * sp.exp(-t_ / 2) / 4,
    '\\frac{1}{(1-s)(1-2s)}': 1 / ((1 - s_) * (1 - 2 * s_)), '1/((1-s)(1-2s))': 1 / ((1 - s_) * (1 - 2 * s_)),
    '\\frac{0.5}{(1-s)(0.5-s)}': sp.Rational(1, 2) / ((1 - s_) * (sp.Rational(1, 2) - s_)),
    '\\frac{1}{1-s}+\\frac{1}{1-2s}': 1 / (1 - s_) + 1 / (1 - 2 * s_), '\\frac{1}{(1-s)(1-0.5s)}': 1 / ((1 - s_) * (1 - s_ / 2)),
    '\\frac{1}{1-s}': 1 / (1 - s_),
    '(1-2s)^{-2}': (1 - 2 * s_) ** -2, '\\frac{1}{(1-2s)^2}': 1 / (1 - 2 * s_) ** 2, '1/(1-2s)^2': 1 / (1 - 2 * s_) ** 2,
    '4(1-2s)^{-1/2}': 4 * (1 - 2 * s_) ** sp.Rational(-1, 2), '(1-2s)^{-1/8}': (1 - 2 * s_) ** sp.Rational(-1, 8),
    '(1-2s)^{-1/2}': (1 - 2 * s_) ** sp.Rational(-1, 2),
}


def expr_part(iid, k, truth):
    if L4 is None:
        return
    w = L4[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    for txt in [w['answer']] + w.get('accept', []):
        ok(txt in TEX, f'{tag}: {txt} not translated')
        if txt in TEX:
            ok(sp.simplify(TEX[txt] - truth) == 0, f'{tag}: {txt} differs from the key')
    bykey = L4[iid]['parts'][k - 1]['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        ok(x['tex'] in TEX, f'{tag}: wrong {x["tex"]} not translated')
        if x['tex'] in TEX:
            ok(sp.simplify(TEX[x['tex']] - truth) != 0, f'{tag}: wrong {x["id"]} equals the key')
        ok(x['id'] in bykey, f'{tag}: wrong {x["id"]} has no byKey line')


def form_stated(items):
    """the validator's [answer-form] words on every non-whole numeric part"""
    if items is None:
        return
    for iid, it in items.items():
        for k, p in enumerate(it['parts'], 1):
            w = p['widget']
            if w['kind'] == 'numeric' and not float(w['answer']).is_integer():
                ok(re.search(r'decimal place|significant figure|fraction|nearest|per cent|%', p['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')


# p-machine-faults: f(x, y) = e^{-y} on 0 < x < y
f_xy = sp.exp(-y_)
fX = sp.integrate(f_xy, (y_, x_, sp.oo))
expr_part('p-machine-faults', 1, sp.exp(-x_))
ok(sp.simplify(fX - sp.exp(-x_)) == 0 and abs(quad(lambda y: exp(-y), 0.7, 60)[0] - exp(-0.7)) < 1e-9, 'faults: marginal e^{-x} two ways')
ok(abs(dblquad(lambda y, x: exp(-y), 0, 50, lambda x: x, lambda x: 60)[0] - 1) < 1e-6, 'faults: volume is 1')
EYx = sp.integrate(y_ * f_xy.subs(x_, sp.Rational(1, 2)) / fX.subs(x_, sp.Rational(1, 2)), (y_, sp.Rational(1, 2), sp.oo))
num(L4, 'p-machine-faults', 2, EYx, quad(lambda y: y * exp(-(y - 0.5)), 0.5, 80)[0],
    {'unconditional': sp.integrate(y_ * y_ * sp.exp(-y_), (y_, 0, sp.oo)), 'half': 0.25, 'gap-only': 1}, dp=1, agree=1e-8)
pick(L4, 'p-machine-faults', 3, 'no')
ok(sp.simplify(sp.integrate(y_ * f_xy / fX, (y_, x_, sp.oo)) - (x_ + 1)) == 0, 'faults: E[Y | X = x] = x + 1 as the choice feedback says')
# part 4: Jacobian of (x, g) -> (x, x + g) is 1; P(G > 2) exactly, then as a volume of the joint density over y - x > 2
g_ = sp.symbols('g', positive=True)
ok(sp.Matrix([[1, 0], [1, 1]]).det() == 1, 'faults: Jacobian 1')
pG = sp.integrate(sp.integrate(sp.exp(-x_ - g_), (x_, 0, sp.oo)), (g_, 2, sp.oo))
pG_alt = dblquad(lambda y, x: exp(-y), 0, 50, lambda x: x + 2, lambda x: x + 70)[0]
num(L4, 'p-machine-faults', 4, pG, pG_alt, {'second-fault': 3 * exp(-2), 'complement': 1 - exp(-2), 'rate-half': exp(-1)}, dp=4, agree=1e-6)
pY = sp.integrate(sp.integrate(f_xy, (x_, 0, y_)), (y_, 3, sp.oo))
rng = random.Random(14)
simY = sum(1 for _ in range(400000) if rng.expovariate(1) + rng.expovariate(1) > 3) / 400000
ok(abs(simY - float(pY)) < 0.003, 'faults: simulation of X + G agrees with 4e^{-3}')
num(L4, 'p-machine-faults', 5, pY, stats.gamma.sf(3, 2), {'one-wait': exp(-3), 'complement': 1 - 4 * exp(-3), 'dropped-one': 3 * exp(-3)}, dp=4)

# p-ticket-stages: triage rate 1, repair rate 0.5
dens = sp.integrate(sp.exp(-x_) * sp.Rational(1, 2) * sp.exp(-sp.Rational(1, 2) * (t_ - x_)), (x_, 0, t_))
expr_part('p-ticket-stages', 1, sp.exp(-t_ / 2) - sp.exp(-t_))
ok(sp.simplify(dens - (sp.exp(-t_ / 2) - sp.exp(-t_))) == 0, 'ticket: convolution gives e^{-t/2} - e^{-t}')
ok(abs(quad(lambda x: exp(-x) * 0.5 * exp(-0.5 * (2.3 - x)), 0, 2.3)[0] - (exp(-1.15) - exp(-2.3))) < 1e-12, 'ticket: numeric convolution at t = 2.3')
tail10 = sp.integrate(sp.exp(-t_ / 2) - sp.exp(-t_), (t_, 10, sp.oo))
rng = random.Random(15)
sim10 = sum(1 for _ in range(600000) if rng.expovariate(1) + rng.expovariate(0.5) > 10) / 600000
ok(abs(sim10 - float(tail10)) < 0.0008, 'ticket: simulation of the tail at 10')
num(L4, 'p-ticket-stages', 2, tail10, quad(lambda t: exp(-t / 2) - exp(-t), 10, 200)[0],
    {'one-stage': exp(-5), 'complement': 1 - float(tail10), 'equal-rates': exp(-5) * 6}, dp=4, agree=1e-8)
stated('repair tail term', 0.01348, 2 * exp(-5), 0.000005)
stated('one ticket in 74', 74, 1 / float(tail10), 0.5)
MT = sp.integrate(sp.exp(s_ * t_) * (sp.exp(-t_ / 2) - sp.exp(-t_)), (t_, 0, sp.oo), conds='none')
expr_part('p-ticket-stages', 3, 1 / ((1 - s_) * (1 - 2 * s_)))
ok(sp.simplify(MT.subs(s_, sp.Rational(1, 5)) - 1 / ((1 - sp.Rational(1, 5)) * (1 - sp.Rational(2, 5)))) == 0, 'ticket: MGF from the density at s = 0.2')
roots = sp.solve(sp.diff(-10 * s_ - sp.log(1 - s_) - sp.log(1 - 2 * s_), s_), s_)
sstar = min(float(r) for r in roots)
opt = minimize_scalar(lambda s: exp(-10 * s) / ((1 - s) * (1 - 2 * s)), bounds=(1e-6, 0.5 - 1e-6), method='bounded', options={'xatol': 1e-10})
num(L4, 'p-ticket-stages', 4, sstar, opt.x,
    {'other-root': max(float(r) for r in sp.solve(20 * s_ ** 2 - 26 * s_ + 7, s_)), 'repair-only': 0.4, 'triage-only': 0.9}, dp=4, agree=1e-6)
ok(abs(sstar - (26 - sqrt(116)) / 40) < 1e-12, 'ticket: s* = (26 - sqrt 116) / 40')
bound = lambda s: exp(-10 * s) / ((1 - s) * (1 - 2 * s))
num(L4, 'p-ticket-stages', 5, bound(0.3807), opt.fun,
    {'repair-s': bound(0.4), 'no-mgf': exp(-3.807), 'exact': float(tail10)}, dp=4, agree=1e-6)
stated('e^{-3.807}', 0.02221, exp(-3.807), 0.000005)
stated('(1 - s)(1 - 2s)', 0.1478, (1 - 0.3807) * (1 - 0.7614), 0.00005)
stated('M_T(s*)', 6.768, 1 / ((1 - 0.3807) * (1 - 2 * 0.3807)), 0.0005)
stated('about 11 times', 11, bound(sstar) / float(tail10), 0.25)

# p-dealer-quotes: best of 4 uniforms
qa = [F(i, 10) for i in range(11)]
num(L4, 'p-dealer-quotes', 1, F(8, 10) ** 4, stats.beta.cdf(0.8, 4, 1),
    {'one-dealer': 0.8, 'worst': 1 - 0.2 ** 4, 'complement': 1 - 0.8 ** 4}, dp=4, agree=1e-9)
num(L4, 'p-dealer-quotes', 2, sp.integrate(t_ * 4 * t_ ** 3, (t_, 0, 1)), quad(lambda t: 1 - t ** 4, 0, 1)[0],
    {'one-dealer': 0.5, 'worst': F(1, 5), 'k-over-n': F(3, 4)}, dp=2)
pick(L4, 'p-dealer-quotes', 3, 'beta41')
ok(abs(stats.beta.pdf(0.7, 4, 1) - 4 * 0.7 ** 3) < 1e-12, 'quotes: Beta(4, 1) density is 4t^3')
num(L4, 'p-dealer-quotes', 4, F(3, 5), stats.beta.mean(3, 2), {'k-over-n': F(3, 4), 'swapped': F(2, 5), 'one-dealer': F(1, 2)}, dp=2)
# part 5 by counting, by the Beta integral and by enumeration of the 16 above/below patterns
pat = sum(1 for bits in itertools.product([0, 1], repeat=4) if sum(bits) >= 2)
num(L4, 'p-dealer-quotes', 5, F(pat, 16), stats.beta.sf(0.5, 3, 2),
    {'three-above': F(5, 16), 'one-above': F(15, 16), 'half': F(1, 2)}, dp=4)
ok(abs(quad(lambda x: 12 * x ** 2 * (1 - x), 0.5, 1)[0] - 0.6875) < 1e-12, 'quotes: Beta(3, 2) integral 11/16')

# p-part-errors: D chi-square on 4 degrees of freedom
expr_part('p-part-errors', 1, (1 - 2 * s_) ** -2)
MD = (1 - 2 * s_) ** -2
m1, m2 = sp.diff(MD, s_).subs(s_, 0), sp.diff(MD, s_, 2).subs(s_, 0)
ok(m1 == 4 and m2 == 24, "parts: M'(0) = 4 and M''(0) = 24")
num(L4, 'p-part-errors', 2, m2 - m1 ** 2, stats.chi2.var(4), {'second-moment': 24, 'one-term': 2, 'sd': sqrt(8)}, dp=0)
pick(L4, 'p-part-errors', 3, 'gamma')
ok(sp.simplify((sp.Rational(1, 2) / (sp.Rational(1, 2) - s_)) ** 2 - MD) == 0, 'parts: Gamma(2, 1/2) MGF matches')
tail = lambda d: exp(-d / 2) * (1 + d / 2)
num(L4, 'p-part-errors', 4, tail(8), stats.chi2.sf(8, 4),
    {'exponential': exp(-4), 'three-terms': exp(-4) * 13, 'rate-one': exp(-8) * 9}, dp=4)
ok(abs(pois_cdf(1, 4) - tail(8)) < 1e-12, 'parts: Poisson(4) count <= 1 equals the Gamma tail')
dstar = next(d for d in range(1, 40) if tail(d) <= 0.05)
dstar_alt = ceil(stats.chi2.isf(0.05, 4))
num(L4, 'p-part-errors', 5, dstar, dstar_alt, {'normal': ceil(4 + 1.645 * sqrt(8)), 'ten-per-cent': 8, 'too-far': 11}, dp=0)
stated('tail at 9', 0.0611, tail(9), 0.00005)
stated('tail at 10', 0.0404, tail(10), 0.00005)
stated('normal fit', 8.65, 4 + 1.645 * sqrt(8), 0.005)
form_stated(L4)


present = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
