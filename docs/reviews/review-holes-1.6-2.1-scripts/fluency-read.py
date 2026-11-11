"""Second read of the eight level 4 Fluency sets of testing and stat-learning.
Every draw made by draw.sh is recomputed from the sentence the learner reads (regex on `prompt`, never `vars` or `lets`),
by a route that is not the family's own formula where one exists (SciPy's pmf, chisquare and chi2_contingency, a finite
difference, a literal k-means step). Checks, per draw: the answer; every `wrong` value against the slip its line names;
no `wrong` inside the answer's band or on another `wrong`; the answer, rounded as the prompt asks, printed in the solution.
Notes (counted, not failures): what a learner who rounds as the solution prints, or keeps a log to 4 places, would type.
Writes <dir>/rows.json for fluency-probe.mjs: strings a learner would type, with the verdict the reader expects.

  <venv>/bin/python docs/reviews/review-holes-1.6-2.1-scripts/fluency-read.py <draws dir>      (from the repo root)"""
import glob
import json
import math
import os
import re
import sys
from collections import Counter

import numpy as np
from scipy import stats

D = sys.argv[1]
checks = fails = 0
notes = Counter()
examples = {}
rows_out = []


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def note(key, ex):
    notes[key] += 1
    examples.setdefault(key, ex)


def nums(s):
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]


def coef(s):
    s = s.replace(' ', '')
    return -1.0 if s == '-' else 1.0 if s in ('', '+') else float(s)


def rd(x, dp):
    return f'{round(x + (1e-12 if x >= 0 else -1e-12), dp):.{dp}f}'


def fam_exponential_rate(p):
    g = nums(re.search(r': ([\d, and]+)\. Model', p).group(1))
    assert len(g) == 5
    xbar = np.mean(g)
    # second route: the rate that makes SciPy's exponential mean equal the sample mean
    lam = 1 / xbar
    assert abs(stats.expon(scale=1 / lam).mean() - xbar) < 1e-12
    unit = re.search(r'rate \$\\lambda\$ per (\w+)', p).group(1)
    return lam, {'gave-mean': xbar, 'total': 1 / sum(g)}, {'units': [f'per {unit}', f'a {unit}']}


def fam_gamma(p, which):
    m, v = nums(re.search(r'sample mean (\d+) and sample variance (\d+)', p).group(0))
    a, lam = m * m / v, m / v
    g = stats.gamma(a, scale=1 / lam)
    assert abs(g.mean() - m) < 1e-9 and abs(g.var() - v) < 1e-9
    if which == 'shape':
        return a, {'gave-rate': lam, 'inverted': v / (m * m)}, {}
    return lam, {'inverted': v / m, 'gave-shape': a}, {}


def fam_uniform_moment(p):
    x = nums(re.search(r'are ([\d, and]+)\. What', p).group(1))
    assert len(x) == 4
    th = 2 * np.mean(x)
    assert abs(stats.uniform(0, th).mean() - np.mean(x)) < 1e-12
    if th < max(x):
        note('uniform-moment: the moment estimate is below the largest draw (an impossible end point)', p)
    return th, {'gave-mean': np.mean(x), 'largest': max(x)}, {}


def fam_bernoulli_information(p):
    pp = float(re.search(r'p = ([\d.]+)', p).group(1))
    n = int(re.search(r'in (\d+) trades', p).group(1))
    # second route: minus the second derivative of the Bernoulli log-likelihood, averaged, by finite difference
    h = 1e-4
    ll = lambda q, x: x * math.log(q) + (1 - x) * math.log(1 - q)
    d2 = lambda x: (ll(pp + h, x) - 2 * ll(pp, x) + ll(pp - h, x)) / h ** 2
    info = -(pp * d2(1) + (1 - pp) * d2(0))
    key = n / (pp * (1 - pp))
    assert abs(n * info - key) < 1e-3 * key
    return key, {'one-trade': 1 / (pp * (1 - pp)), 'variance': n * pp * (1 - pp)}, {'comma': True}


def fam_poisson_se(p):
    n = int(re.search(r'Over (\d+)', p).group(1))
    lam = float(re.search(r'hat\\lambda = ([\d.]+)', p).group(1))
    # the MLE is the sample mean, whose variance is lam/n exactly
    return math.sqrt(lam / n), {'no-root': lam / n, 'information-flipped': math.sqrt(1 / (n * lam))}, {}


def fam_exponential_se(p):
    n = int(re.search(r'From (\d+)', p).group(1))
    lam = float(re.search(r'hat\\lambda = ([\d.]+)', p).group(1))
    h = 1e-4
    # information by finite difference of ln f = ln(lam) - lam x (the second derivative holds no x)
    d2 = (math.log(lam + h) - 2 * math.log(lam) + math.log(lam - h)) / h ** 2
    assert abs(-d2 - 1 / lam ** 2) < 1e-5
    unit = re.search(r'per (\w+)\.', p).group(1)
    return lam / math.sqrt(n), {'no-root': lam ** 2 / n, 'information-flipped': 1 / (lam * math.sqrt(n))}, {'units': [f'per {unit}']}


def fam_volatility_se(p):
    sig = float(re.search(r'sigma = ([\d.]+)', p).group(1))
    n = int(re.search(r'from (\d+) returns', p).group(1))
    # information about sigma by numerical expectation of minus the second derivative of ln f
    xs = np.linspace(-12 * sig, 12 * sig, 200001)
    f = stats.norm(0, sig).pdf(xs)
    d2 = 1 / sig ** 2 - 3 * xs ** 2 / sig ** 4
    info = -np.trapezoid(f * d2, xs)
    assert abs(info - 2 / sig ** 2) < 1e-6
    return sig / math.sqrt(2 * n), {'no-two': sig / math.sqrt(n), 'variance-se': sig ** 2 * math.sqrt(2 / n)}, {'units': ['%', 'points', 'percentage points']}


def fam_binomial_ratio(p):
    k, n = map(int, re.search(r'wins (\d+) of (\d+)', p).groups())
    p1 = float(re.search(r'hit rate of ([\d.]+)', p).group(1))
    key = stats.binom.pmf(k, n, p1) / stats.binom.pmf(k, n, 0.5)
    return key, {'inverted': 1 / key, 'wins-only': (p1 / 0.5) ** k}, {}


def fam_two_ll(p):
    l0, l1 = [float(x) for x in re.findall(r'\$(-[\d.]+)\$', p)]
    return 2 * (l1 - l0), {'not-doubled': l1 - l0, 'sign': -2 * (l1 - l0)}, {}


def fam_wilks_df(p):
    pp = int(re.search(r'has (\d+) parameters', p).group(1))
    r = int(re.search(r'fixes (\d+)', p).group(1))
    free = int(re.search(r'leaving (\d+) free', p).group(1))
    ok(free == pp - r, f'wilks-df: free count in the prompt: {p}')
    return r, {'all-parameters': pp, 'free-under-null': free}, {}


def fam_poisson_ratio(p):
    s, n = map(int, re.search(r'^(\d+) \w+ arrive in (\d+)', p).groups())
    lam0 = float(re.search(r'lambda_0 = ([\d.]+)', p).group(1))
    key = 2 * (stats.poisson.logpmf(s, s) - stats.poisson.logpmf(s, n * lam0))   # the total is sufficient
    lr = math.log(s / (n * lam0))
    dv = s - n * lam0
    extra = {'log4': 2 * (s * round(lr, 4) - dv), 'ratio4': 2 * (s * math.log(round(s / (n * lam0), 4)) - dv), 'log5': 2 * (s * round(lr, 5) - dv)}
    return key, {'not-doubled': key / 2, 'no-mean-term': 2 * s * lr}, {'alts': extra}


def fam_expected_cell(p):
    tot, rt, ct = map(int, re.search(r'Of (\d+) \w+, (\d+) .*? and (\d+) ', p).groups())
    return rt * ct / tot, {'averaged': (rt + ct) / 2, 'no-divide': rt * ct}, {}


def fam_gof(p):
    tot = int(re.match(r'(\d+)', p).group(1))
    o = nums(re.search(r' as ([\d, and]+)\. If', p).group(1))
    ok(sum(o) == tot and len(o) == 4, f'goodness-of-fit: counts sum to the total: {p}')
    key = stats.chisquare(o).statistic
    e = tot / 4
    return key, {'no-divide': sum((x - e) ** 2 for x in o), 'over-observed': sum((x - e) ** 2 / x for x in o)}, {}


def fam_two_by_two(p):
    tot, r1, a, b, r2, c, d = map(int, re.search(r'Of (\d+) \w+, (\d+) were .*?: (\d+) \w+ and (\d+) \w+\. The other (\d+) were .*?: (\d+) \w+ and (\d+) \w+', p).groups())
    ok(a + b == r1 and c + d == r2 and r1 + r2 == tot, f'two-by-two: totals in the prompt: {p}')
    t = np.array([[a, b], [c, d]])
    key, _, dof, exp = stats.chi2_contingency(t, correction=False)
    assert dof == 1
    # the route the solution prints: E11 to 2 places, the gap to 3 places, then four terms
    gap3 = round(abs(a - exp[0, 0]), 3)
    sol = sum(gap3 ** 2 / e for e in exp.ravel())
    # a learner's route: every expected count to 2 places, each cell's own gap
    e2 = np.round(exp, 2)
    cells = float(((t - e2) ** 2 / e2).sum())
    return key, {'one-cell': (a - exp[0, 0]) ** 2 / exp[0, 0], 'no-divide': float(((t - exp) ** 2).sum())}, {'alts': {'solution-rounding': sol, 'cells-2dp': cells}}


def fam_independence_df(p):
    r, c = map(int, re.search(r'(\d+) rows and (\d+) columns', p).groups())
    return (r - 1) * (c - 1), {'cells-minus-one': r * c - 1, 'margins': r + c - 2}, {}


def wb(p):
    w = nums(re.search(r'w = \(([^)]*)\)', p).group(1))
    b = float(re.search(r'b = (-?[\d.]+)', p).group(1))
    return np.array(w), b


def fam_margin(p):
    w, b = wb(p)
    n = float(np.linalg.norm(w))
    # check: a point on the edge w.x + b = 1 nearest the centre line is 1/|w| from it
    x_edge = w * (1 - b) / n ** 2
    x_mid = w * (0 - b) / n ** 2
    assert abs(np.linalg.norm(x_edge - x_mid) - 1 / n) < 1e-12
    return 1 / n, {'gave-norm': n, 'street-width': 2 / n}, {}


def fam_decision(p):
    w, b = wb(p)
    x = np.array(nums(re.search(r'x = \(([^)]*)\)', p).group(1)))
    return float(w @ x + b), {'no-intercept': float(w @ x), 'one-term': float(w[0] * x[0] + b)}, {}


def fam_distance(p):
    w, b = wb(p)
    x = np.array(nums(re.search(r'point \$\(([^)]*)\)\$', p).group(1)))
    f = float(w @ x + b)
    n2 = float(w @ w)
    foot = x - f * w / n2     # the foot of the perpendicular; it must lie on the centre line
    assert abs(w @ foot + b) < 1e-9
    return float(np.linalg.norm(x - foot)), {'no-norm': abs(f), 'squared-norm': abs(f) / n2}, {}


def fam_assign(p):
    v = nums(re.search(r'(?:volatilities|spreads|daily volumes) ([\d, and]+)', p).group(1))
    c1, c2 = nums(re.search(r'sit at (\d+) and (\d+)', p).group(0))
    assert len(v) == 5
    near2 = [x for x in v if abs(x - c2) < abs(x - c1)]
    ok(all(abs(x - c2) != abs(x - c1) for x in v), f'assign-and-update: no tie: {p}')
    ok(2 <= len(near2) <= 4, f'assign-and-update: both groups non-empty: {p}')
    key = float(np.mean(near2))
    unit = '%' if '%' in p else ' bp' if ' bp' in p else ' million shares'
    return key, {'all-shares': float(np.mean(v)), 'kept-centre': (sum(near2) + c2) / (len(near2) + 1)}, {'units': [unit.strip()]}


def fam_inertia(p):
    x = nums(re.search(r'(?:volatilities|points|millions) ([\d, and]+)\. What', p).group(1))
    assert len(x) == 4
    m = np.mean(x)
    return float(sum((t - m) ** 2 for t in x)), {'unsquared': float(sum(abs(t - m) for t in x)), 'averaged': float(np.var(x))}, {}


def fam_linkage(p):
    a, b = map(float, re.search(r'distance ([\d.]+) from \w+ and ([\d.]+) from', p).groups())
    name = re.search(r'Under (\w+) linkage', p).group(1)
    key = {'single': min(a, b), 'complete': max(a, b), 'average': (a + b) / 2}[name]
    return key, {'nearest': min(a, b), 'farthest': max(a, b), 'averaged': (a + b) / 2}, {}


def fam_forward(p):
    hs = re.findall(r'\\max\(0,\\, ([^)]*)\)', p)
    us = []
    x = nums(re.search(r'= \((-?\d+), (-?\d+)\)\$\?', p).group(0))
    for h in hs:
        m = re.fullmatch(r'\s*([+-]?\d*)x_1 ([+-]\d*)x_2 ([+-]\d+)\s*', h)
        us.append(coef(m.group(1)) * x[0] + coef(m.group(2)) * x[1] + float(m.group(3)))
    m = re.search(r'z = ([+-]?\d*)h_1 ([+-]\d*)h_2 ([+-]\d+)', p)
    v1, v2, d = coef(m.group(1)), coef(m.group(2)), float(m.group(3))
    key = v1 * max(0, us[0]) + v2 * max(0, us[1]) + d
    return key, {'no-relu': v1 * us[0] + v2 * us[1] + d, 'no-output-bias': key - d}, {}


def fam_param(p):
    a, b, c = map(int, re.search(r'(\d+)–(\d+)–(\d+)', p).groups())
    # count by building the arrays
    key = np.zeros((b, a)).size + b + np.zeros((c, b)).size + c
    return key, {'no-biases': a * b + b * c, 'units': a + b + c}, {}


def fam_slope(p):
    x, y, w1, w2 = [float(re.search(rf'{k} = (-?[\d.]+)', p).group(1)) for k in ('x', 'y', 'w_1', 'w_2')]
    L = lambda a, b: 0.5 * (b * max(0, a * x) - y) ** 2
    h = 1e-6
    key = (L(w1 + h, w2) - L(w1 - h, w2)) / (2 * h)
    g2 = (L(w1, w2 + h) - L(w1, w2 - h)) / (2 * h)
    err = w2 * w1 * x - y
    return round(key, 6), {'slope-for-w2': round(g2, 6), 'dropped-w2': err * x}, {}


def fam_step(p):
    w = float(re.search(r'w_\d = (-?[\d.]+)\$ has', p).group(1))
    g = float(re.search(r'= (-?\d+)\$\. What', p).group(1))
    eta = float(re.search(r'eta = ([\d.]+)', p).group(1))
    return w - eta * g, {'uphill': w + eta * g, 'no-rate': w - g}, {}


def fam_hinge(p):
    m = re.search(r'f\(x\) = (-?\d+) ([+-]\d*)x ([+-]\d*)\(x - (\d+)\)\^\+\$\. What is \$f\((\d+)\)', p)
    a, b, d, c, x0 = float(m.group(1)), coef(m.group(2)), coef(m.group(3)), float(m.group(4)), float(m.group(5))
    key = a + b * x0 + d * max(0, x0 - c)
    return key, {'ignored-hinge': a + b * x0, 'hinge-on-left': a + b * x0 + d * (x0 - c), 'no-intercept': key - a}, {}


def fam_region(p):
    b = float(re.search(r'slope (-?[\d.]+) on', p).group(1))
    k1, k2 = map(float, re.search(r'knots at (\d+) and (\d+)', p).groups())
    d1, d2 = map(float, re.search(r'coefficients \$(-?[\d.]+)\$ and \$(-?[\d.]+)\$', p).groups())
    f = lambda t: b * t + d1 * max(0, t - k1) + d2 * max(0, t - k2)
    if 'between the two knots' in p:
        lo, hi = k1, k2
        co, skip = d1, b
    else:
        lo, hi = k2, k2 + 10
        co, skip = d2, b + d2
    key = (f(hi) - f(lo)) / (hi - lo)       # the slope read off the function itself
    return key, {'coefficient-only': co, 'skipped-knot': skip}, {}


def fam_count(p):
    k = int(re.search(r'has (\d+) (?:interior )?knots', p).group(1))
    deg = 3 if 'cubic' in p else 1
    # count the columns of the truncated power basis: 1, x, .., x^deg, and one (x - knot)^deg_+ a knot
    key = (deg + 1) + k
    return key, {'no-constant': key - 1, 'knots-only': k}, {}


FAM = {
    'exponential-rate': fam_exponential_rate, 'gamma-shape': lambda p: fam_gamma(p, 'shape'), 'gamma-rate': lambda p: fam_gamma(p, 'rate'),
    'uniform-moment': fam_uniform_moment, 'bernoulli-information': fam_bernoulli_information, 'poisson-se': fam_poisson_se,
    'exponential-se': fam_exponential_se, 'volatility-se': fam_volatility_se, 'binomial-ratio': fam_binomial_ratio,
    'two-log-likelihoods': fam_two_ll, 'wilks-df': fam_wilks_df, 'poisson-ratio-test': fam_poisson_ratio, 'expected-cell': fam_expected_cell,
    'goodness-of-fit': fam_gof, 'two-by-two': fam_two_by_two, 'independence-df': fam_independence_df, 'margin': fam_margin,
    'decision-value': fam_decision, 'distance': fam_distance, 'assign-and-update': fam_assign, 'group-inertia': fam_inertia,
    'linkage-distance': fam_linkage, 'forward-pass': fam_forward, 'parameter-count': fam_param, 'slope-first-weight': fam_slope,
    'one-step': fam_step, 'hinge-value': fam_hinge, 'slope-in-a-region': fam_region, 'coefficient-count': fam_count,
}

draws = 0
seen_fams = Counter()
prompts = {}
for f in sorted(glob.glob(os.path.join(D, '*__*.json'))):
    doc = json.load(open(f))
    for it in doc['items']:
        draws += 1
        fam, p = it['family'], it['prompt']
        seen_fams[fam] += 1
        prompts.setdefault(fam, set()).add(p)
        where = f"{fam} seed {it['seed']}"
        key, wrongs, extra = FAM[fam](p)
        key = float(key)
        tol = it['tol']['abs']
        ok(abs(it['answer'] - key) <= 1e-6 * max(1, abs(key)), f"{where}: answer {it['answer']} against mine {key}: {p}")
        for w in it['wrong']:
            ok(w['id'] in wrongs, f"{where}: wrong id {w['id']} not known to the reader")
            if w['id'] in wrongs:
                ok(abs(w['value'] - wrongs[w['id']]) <= 1e-6 * max(1, abs(w['value'])), f"{where}: wrong {w['id']} {w['value']} against mine {wrongs[w['id']]}: {p}")
            wt = (w.get('tol') or {}).get('abs', tol)
            ok(abs(w['value'] - it['answer']) > tol + wt or abs(w['value'] - it['answer']) > 1e-9 and tol == 0, f"{where}: wrong {w['id']} sits in the answer's band: {p}")
        vals = [w['value'] for w in it['wrong']]
        ok(len(set(round(v, 6) for v in vals)) == len(vals), f"{where}: two wrong entries share a value: {p}")
        for wid, val in wrongs.items():     # a slip the family names that this draw dropped: it must be on the answer or on another entry
            if wid not in [w['id'] for w in it['wrong']]:
                ok(abs(val - key) < 1e-9 or any(abs(val - v) < 1e-9 for v in vals), f"{where}: wrong {wid} = {val} dropped although free: {p}")
        m = re.search(r'Give (\d) decimal place', p)
        dp = int(m.group(1)) if m else None
        sol = ' '.join(it['solution'])
        shown = rd(key, dp) if dp is not None else (str(int(round(key))) if abs(key - round(key)) < 1e-9 else repr(round(key, 6)))
        ok(shown in sol or shown.rstrip('0').rstrip('.') in sol, f"{where}: the solution does not print the answer {shown}: {sol}")
        rows = []
        if dp is not None:
            rows.append([rd(key, dp), True, 'rounded as asked'])
            rows.append([rd(key, dp + 2), True, 'two more places'])
            stripped = rd(key, dp).rstrip('0').rstrip('.')
            if stripped != rd(key, dp):
                rows.append([stripped, True, 'trailing zeros left off'])
            if dp >= 2 and abs(float(rd(key, dp - 1)) - key) > tol:
                rows.append([rd(key, dp - 1), False, 'one place short'])
        else:
            rows.append([shown, True, 'as the solution prints it'])
            if '-' in shown:
                rows.append([shown.replace('-', '\u2212'), True, 'typed with a true minus sign'])
        base = rd(key, dp) if dp is not None else shown
        for u in extra.get('units', []):
            rows.append([f'{base}{u}' if u == '%' else f'{base} {u}', True, f'unit typed after the number ({u})'])
        if extra.get('comma') and key >= 1000:
            rows.append([f'{float(base):,.{dp}f}', True, 'thousands comma'])
        for name, val in extra.get('alts', {}).items():
            inside = abs(val - key) <= tol
            if not inside:
                note(f'{fam}: the value from "{name}" falls outside the band', f'{rd(val, dp)} against {rd(key, dp)}: {p}')
            rows.append([rd(val, dp + 1), True, f'worked by "{name}"'])
        rows_out.append({'file': os.path.basename(f), 'family': fam, 'seed': it['seed'], 'prompt': p,
                         'spec': {'kind': 'numeric', 'answer': it['answer'], 'tol': it['tol'], 'unit': it.get('unit'),
                                  'wrong': [{'id': w['id'], 'value': w['value'], 'tol': w.get('tol') or it['tol']} for w in it['wrong']]},
                         'rows': rows})

json.dump(rows_out, open(os.path.join(D, 'rows.json'), 'w'), ensure_ascii=False)
print('families read:', len(seen_fams), 'draws:', draws)
print('distinct prompts a family (of its draws):', {k: len(v) for k, v in prompts.items() if len(v) < seen_fams[k]})
for k, v in sorted(notes.items()):
    print(f'NOTE [{v} of {seen_fams[k.split(":")[0]]}] {k}\n      e.g. {examples[k]}')
print(f'fluency-read: {checks} checks, {fails} failures, {sum(notes.values())} notes')
sys.exit(1 if fails else 0)
