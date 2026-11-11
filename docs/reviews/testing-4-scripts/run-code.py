"""Second read, testing L4: every code item run in CPython with the engine's comparison rule
(math.isclose rel 1e-9, abs 1e-12, or the case's own tol; element by element for tuples and lists).
For each item: the author's solution passes every test, the starter fails, the reader's own
independent solution passes, and each plausible wrong solution (mutant) fails at least one test.
Run from the repo root with the scratchpad venv python (SciPy needed). Exit 0 when all hold."""
import json, math, sys, os

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'app', 'content', 'courses', 'testing')
bad = 0


def close(x, y, tol):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q, tol) for p, q in zip(x, y))
    try:
        x, y = float(x), float(y)
    except Exception:
        return x == y
    if math.isnan(x) and math.isnan(y):
        return True
    rt, at = tol if tol else (1e-9, 1e-12)
    return math.isclose(x, y, rel_tol=rt, abs_tol=at)


def run(src, tests):
    """Number of failed tests (an exception counts as a failure)."""
    fails = 0
    for t in tests:
        g = {}
        try:
            exec(src, g)
            if t.get('setup'):
                exec(t['setup'], g)
            got = eval(t['call'], g)
            want = eval(t['expect'], g)
            tol = None
            if isinstance(t.get('tol'), dict):
                tol = (t['tol'].get('rel', 0) or 0, t['tol'].get('abs', 0) or 0)
            ok = close(got, want, tol) if t.get('compare') == 'isclose' else got == want
        except Exception:
            ok = False
        fails += 0 if ok else 1
    return fails


def item(fname, where):
    d = json.load(open(os.path.join(ROOT, fname)))
    box = d.get('screens') or d.get('items')
    return box[where]['widget']


def report(name, w, own, mutants):
    global bad
    tests = w['tests']
    rows = [('author solution passes', run(w['solution'], tests) == 0),
            ('starter fails', run(w['starter'], tests) > 0),
            ('reader solution passes', run(own, tests) == 0)]
    for label, src in mutants.items():
        rows.append((f'mutant caught: {label}', run(src, tests) > 0))
    for label, ok in rows:
        print(('ok  ' if ok else 'FAIL') + f' {name}: {label}')
        bad += 0 if ok else 1


# ---------------------------------------------------------------- l13 s8
own13 = '''
import statistics
def mom_gamma(xs):
    m = statistics.fmean(xs); v = statistics.pvariance(xs)
    lam = m / v
    return (round(lam * m, 4), round(lam, 4))
def mom_uniform(xs):
    return 2 * statistics.fmean(xs)
def mle_uniform(xs):
    return sorted(xs)[-1]
'''
report('l13 s8', item('l13-matching-moments.json', 8), own13, {
    'n - 1 divisor': own13.replace('pvariance', 'variance'),
    'shape and rate swapped': own13.replace('(round(lam * m, 4), round(lam, 4))', '(round(lam, 4), round(lam * m, 4))'),
    'mle_uniform = 2 * mean': own13.replace('sorted(xs)[-1]', '2 * statistics.fmean(xs)'),
    'mom_uniform = max': own13.replace('return 2 * statistics.fmean(xs)', 'return max(xs)'),
    'scale returned for rate': own13.replace('lam = m / v', 'lam = m / v').replace('round(lam, 4))', 'round(1 / lam, 4))'),
})

# ---------------------------------------------------------------- l15 s9
own15 = '''
import random, statistics
def info_bernoulli(p, n):
    return n * (1 / p + 1 / (1 - p))
def observed_info(loglik, theta, h):
    return (2 * loglik(theta) - loglik(theta - h) - loglik(theta + h)) / (h * h)
def mle_sd(p, n, reps, seed):
    rng = random.Random(seed)
    out = []
    for r in range(reps):
        k = 0
        for i in range(n):
            if rng.random() < p:
                k += 1
        out.append(k / n)
    return statistics.pstdev(out)
'''
report('l15 s9', item('l15-sharpness-of-the-peak.json', 9), own15, {
    'information of one trade': own15.replace('return n * (1 / p + 1 / (1 - p))', 'return 1 / (p * (1 - p))'),
    'p(1-p)/n instead of information': own15.replace('return n * (1 / p + 1 / (1 - p))', 'return p * (1 - p) / n'),
    'second difference with the wrong sign': own15.replace('(2 * loglik(theta) - loglik(theta - h) - loglik(theta + h))', '(loglik(theta - h) + loglik(theta + h) - 2 * loglik(theta))'),
    'second difference over h, not h squared': own15.replace('/ (h * h)', '/ h'),
    'stdev with divisor reps - 1': own15.replace('pstdev', 'stdev'),
    'spread of the counts k, not k/n': own15.replace('out.append(k / n)', 'out.append(k)'),
})

# ---------------------------------------------------------------- l17 s9
own17 = '''
from math import comb, erf, log, sqrt, exp
def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))
def lr_binomial(k, n, p0, p1):
    return (p1 ** k * (1 - p1) ** (n - k)) / (p0 ** k * (1 - p0) ** (n - k))
def size_power(n, p0, p1, k_min):
    def upper(p):
        return 1 - sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(0, k_min))
    return (round(upper(p0), 4), round(upper(p1), 4))
def lrt_poisson(xs, lam0):
    n = len(xs); s = sum(xs); lam = s / n
    l1 = (s * log(lam) if s else 0.0) - n * lam
    l0 = s * log(lam0) - n * lam0
    stat = 2 * (l1 - l0)
    return (stat, 2 * (1 - Phi(sqrt(stat))))
'''
report('l17 s9', item('l17-ratio-of-likelihoods.json', 9), own17, {
    'ratio upside down': own17.replace('(p1 ** k * (1 - p1) ** (n - k)) / (p0 ** k * (1 - p0) ** (n - k))', '(p0 ** k * (1 - p0) ** (n - k)) / (p1 ** k * (1 - p1) ** (n - k))'),
    'tail starts at k_min + 1': own17.replace('range(0, k_min)', 'range(0, k_min + 1)'),
    'power and size swapped': own17.replace('(round(upper(p0), 4), round(upper(p1), 4))', '(round(upper(p1), 4), round(upper(p0), 4))'),
    'statistic not doubled': own17.replace('stat = 2 * (l1 - l0)', 'stat = (l1 - l0)'),
    'one-sided p-value': own17.replace('2 * (1 - Phi(sqrt(stat)))', '(1 - Phi(sqrt(stat)))'),
    'no guard for the all-zero sample': own17.replace('(s * log(lam) if s else 0.0)', 's * log(lam)'),
    'p-value from the statistic, not its root': own17.replace('Phi(sqrt(stat))', 'Phi(stat)'),
})

# ---------------------------------------------------------------- l18 s9
own18 = '''
from scipy import stats
def chi2_stat(observed, expected):
    t = 0.0
    for i in range(len(observed)):
        t += (observed[i] - expected[i]) ** 2 / expected[i]
    return t
def expected_counts(table):
    N = sum(map(sum, table))
    R = [sum(row) for row in table]
    C = [sum(row[j] for row in table) for j in range(len(table[0]))]
    return [[R[i] * C[j] / N for j in range(len(C))] for i in range(len(R))]
def chi2_test(table):
    E = expected_counts(table)
    s = chi2_stat(sum(table, []), sum(E, []))
    df = (len(table) - 1) * (len(table[0]) - 1)
    return (s, df, stats.chi2.sf(s, df))
'''
report('l18 s9', item('l18-counts-against-expectations.json', 9), own18, {
    'degrees of freedom cells - 1': own18.replace('df = (len(table) - 1) * (len(table[0]) - 1)', 'df = len(table) * len(table[0]) - 1'),
    'divide by observed': own18.replace('/ expected[i]', '/ observed[i]'),
    'no division by expected': own18.replace(' / expected[i]', ''),
    'expected = average of margins': own18.replace('R[i] * C[j] / N', '(R[i] + C[j]) / 2'),
    'cdf instead of sf': own18.replace('chi2.sf', 'chi2.cdf'),
    'Yates correction applied': own18.replace('(observed[i] - expected[i]) ** 2', '(abs(observed[i] - expected[i]) - 0.5) ** 2'),
})

# ---------------------------------------------------------------- homework h-gof-code
ownhw = '''
from math import exp, factorial
from scipy import stats
def gof_poisson(counts):
    n = len(counts); lam = sum(counts) / n; m = max(counts)
    pk = [exp(-lam) * lam ** k / factorial(k) for k in range(m)]
    cells = [[sum(c == k for c in counts), n * pk[k]] for k in range(m)]
    cells.append([sum(c >= m for c in counts), n * (1 - sum(pk))])
    while len(cells) > 2 and cells[-1][1] < 5:
        o, e = cells.pop()
        cells[-1][0] += o; cells[-1][1] += e
    while len(cells) > 2 and cells[0][1] < 5:
        o, e = cells.pop(0)
        cells[0][0] += o; cells[0][1] += e
    x2 = sum((o - e) ** 2 / e for o, e in cells)
    df = len(cells) - 2
    return (round(x2, 4), df, round(float(stats.chi2.sf(x2, df)), 4))
'''
report('homework h-gof-code', item('homework-4.json', 4), ownhw, {
    'degrees of freedom cells - 1': ownhw.replace('df = len(cells) - 2', 'df = len(cells) - 1'),
    'no merging at all': ownhw.replace('cells[-1][1] < 5', 'cells[-1][1] < 0').replace('cells[0][1] < 5', 'cells[0][1] < 0'),
    'merging from the top end only': ownhw.replace('cells[0][1] < 5', 'cells[0][1] < 0'),
    'merging from the bottom end only': ownhw.replace('cells[-1][1] < 5', 'cells[-1][1] < 0'),
    'last cell P(X = m), not P(X >= m)': ownhw.replace('n * (1 - sum(pk))', 'n * exp(-lam) * lam ** m / factorial(m)'),
    'merge on observed under 5': ownhw.replace('cells[-1][1] < 5', 'cells[-1][0] < 5').replace('cells[0][1] < 5', 'cells[0][0] < 5'),
    'cells 0..m with no tail cell': ownhw.replace('range(m)', 'range(m + 1)').replace('cells.append([sum(c >= m for c in counts), n * (1 - sum(pk))])', ''),
})

print(f'\n{"all code checks hold" if not bad else str(bad) + " code check(s) FAILED"}')
sys.exit(1 if bad else 0)
