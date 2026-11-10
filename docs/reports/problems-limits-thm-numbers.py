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


present = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
