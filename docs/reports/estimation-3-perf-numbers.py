"""Recompute every number in estimation homework-3 item h-bump-interval (performance task, code).

Run with the scratchpad venv (numpy, sympy):
    <venv>/bin/python -I docs/reports/estimation-3-perf-numbers.py      exits 0 when every check passes.
Route A is the item's own `solution`. Route B is an independent reference in this file
(endpoints through exp and log, coverage counted from the same specified draws), so each
test expectation is matched by two routes under the engine's comparison (code.js __zq_cmp:
isclose with rel 1e-9, abs 1e-12 through lists and tuples, else ==). The closed-form
coverage (exactly `level`) is proved in sympy and checked by a seeded numpy simulation.
The starter must fail every test and each planted wrong solution at least one.
"""
import contextlib, io, json, math, os, random, re, sys

import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/estimation/homework-3.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'h-bump-interval')
w = item['widget']
fails = []


def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)


def close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
    if isinstance(x, bool) or isinstance(y, bool):
        return x == y
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run_tests(code, cases=None):
    res = []
    for t in (cases or w['tests']):
        ns = {}
        try:
            exec(code, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            with contextlib.redirect_stdout(io.StringIO()):
                got = eval(t['call'], ns)
            exp = eval(t['expect'], ns)
            res.append(close(got, exp) if t.get('compare') == 'isclose' else bool(got == exp))
        except Exception as e:
            res.append(type(e).__name__)
    return res


# ---------- shape ----------
T = w['tests']
check('performance code, Python', item.get('performance') == 'code' and w['kind'] == 'code' and w['language'] == 'python')
check('tests 3 or more and more than examples', len(T) >= 3 and len(T) > len(w['examples']), f'{len(T)} tests, {len(w["examples"])} example')
check('example equals test 1', w['examples'][0] == T[0])
check('homework item count within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('byKey keys name real tests', all(re.fullmatch(r'test-\d+', k) and 1 <= int(k[5:]) <= len(T) for k in item['feedback']['byKey']))
check('only the standard library is imported', set(re.findall(r'^\s*(?:import|from)\s+(\w+)', w['solution'], re.M)) <= {'random', 'math'})

SOL = w['solution']
r = run_tests(SOL)
check(f'A: solution passes all {len(T)} tests', all(x is True for x in r), str(r))
r = run_tests(w['starter'])
check('starter fails every test', all(x is not True for x in r), str(r))

# ---------- route B: independent reference ----------
def ref_interval(delays, level):
    n, m, a = len(delays), sorted(delays)[-1], 1.0 - level
    return [m * math.exp(-math.log(1 - a / 2) / n), m * math.exp(-math.log(a / 2) / n)]


def ref_coverage(theta, n, level, trials, seed, margins=None):
    g = random.Random(seed)
    k = 0
    for _ in range(trials):
        u = [g.random() for _ in range(n)]
        lo, hi = ref_interval([theta * v for v in u], level)
        if margins is not None:
            margins.append(min(abs(lo - theta), abs(hi - theta)) / theta)
        k += lo <= theta <= hi
    return k / trials


REF_NS = {'bump_interval': ref_interval, 'bump_coverage': ref_coverage}
for i, t in enumerate(T, 1):
    ns = dict(REF_NS)
    if t.get('setup'):
        exec(t['setup'], ns)
    got = eval(t['call'].replace('list(', '(', 1) if t['call'].startswith('list(') else t['call'], ns)
    exp = eval(t['expect'])
    check(f'B: test {i} expect by the reference', close(got, exp) if t['compare'] == 'isclose' else got == exp, f'{t["call"][:50]} -> {t["expect"][:40]}')

# exact-replay coverage tests: no trial lies within float noise of an endpoint
for args in ((10.0, 5, 0.95, 2000, 1), (3.0, 2, 0.8, 5000, 7), (1.0, 1, 0.5, 4000, 3), (250.0, 20, 0.9, 1500, 11)):
    mg = []
    ref_coverage(*args, margins=mg)
    check(f'margin {args}: nearest endpoint {min(mg):.2e} of theta (float noise is 1e-15)', min(mg) > 1e-9)

# stated values
iv1 = ref_interval([12.0, 30.0, 21.0], 0.95)
check('test 5 (largest first) equals test 1', eval(T[4]['expect']) == eval(T[0]['expect']))
check('test 1 about 30.25 to 102.60', [round(v, 2) for v in iv1] == [30.25, 102.6], str(iv1))
iv2 = ref_interval([4.0], 0.95)
check('test 2 about 4.10 to 160 (4/0.975 and 4/0.025)', round(iv2[0], 2) == 4.10 and round(iv2[1], 6) == 160.0 and abs(4 / 0.975 - iv2[0]) < 1e-12, str(iv2))
c6 = ref_coverage(10.0, 5, 0.95, 2000, 1)
check('test 6 share 0.947 of 2,000', c6 == 0.947 and round(c6 * 2000) == 1894, str(c6))
c7, c8 = ref_coverage(3.0, 2, 0.8, 5000, 7), ref_coverage(1.0, 1, 0.5, 4000, 3)
check('test 7 band: inside 0.02 of 0.8 with room', abs(c7 - 0.8) < 0.01, str(c7))
check('test 8 band: inside 0.03 of 0.5 with room', abs(c8 - 0.5) < 0.015, str(c8))
text = ' '.join([item['prose'], item['question'], w['how'], item['explain']['text']] + list(item['feedback'].values())[:2] + list(item['feedback']['byKey'].values()))
for tok in ('30.25 to 102.60', '4.10 to 160', '0.947', '2,000', '0.02 or 0.03', '50 delays'):
    check(f'printed {tok}', tok in text)
check('how counts 9 hidden tests, five and four', 'Check runs 9 hidden tests' in w['how'] and 'Five call `bump_interval`' in w['how'] and 'Four call `bump_coverage`' in w['how']
      and sum('bump_interval(' in t['call'] for t in T) == 5 and sum('bump_coverage(' in t['call'] for t in T) == 4)

# ---------- closed form: coverage is exactly level ----------
u, n, a = sp.symbols('u n a', positive=True)
cdf = u ** n                                   # P(M/theta <= u): all n uniforms below u, by independence
lo_q, hi_q = (a / 2) ** (1 / n), (1 - a / 2) ** (1 / n)
cover = sp.simplify(sp.powdenest(cdf.subs(u, hi_q) - cdf.subs(u, lo_q), force=True))  # (q^(1/n))^n = q for q > 0
check('sympy: P((a/2)^(1/n) <= M/theta <= (1-a/2)^(1/n)) = 1 - a', sp.simplify(cover - (1 - a)) == 0, str(cover))
for nv, av in ((1, 0.05), (5, 0.05), (20, 0.1), (3, 0.5)):
    q1, q2 = (av / 2) ** (1 / nv), (1 - av / 2) ** (1 / nv)
    check(f'numeric: q2^n - q1^n = level at n={nv}, a={av}', abs(q2 ** nv - q1 ** nv - (1 - av)) < 1e-12)
# the CDF u^n by direct simulation of the max, two n
rng = np.random.default_rng(20261109)
for nn in (1, 5):
    mx = rng.random((200_000, nn)).max(axis=1)
    emp = [(mx <= q).mean() for q in (0.3, 0.7, 0.95)]
    check(f'seeded: P(max of {nn} uniforms <= u) = u^{nn}', all(abs(e - q ** nn) < 0.005 for e, q in zip(emp, (0.3, 0.7, 0.95))), str([round(e, 4) for e in emp]))
# seeded coverage at several (n, level), 400k trials, against the exact level
for nn, lev, th in ((1, 0.95, 4.0), (5, 0.95, 10.0), (20, 0.9, 250.0), (3, 0.5, 1.0)):
    al = 1 - lev
    M = th * rng.random((400_000, nn)).max(axis=1)
    lo, hi = M / (1 - al / 2) ** (1 / nn), M / (al / 2) ** (1 / nn)
    cov = ((lo <= th) & (th <= hi)).mean()
    se = math.sqrt(lev * (1 - lev) / 400_000)
    check(f'seeded coverage n={nn} level={lev}: {cov:.4f}', abs(cov - lev) < 4 * se, f'se {se:.4f}')
    # each tail misses with chance a/2
    check(f'seeded tails n={nn}: low miss {(hi < th).mean():.4f}, high miss {(lo > th).mean():.4f} vs {al/2}',
          abs((hi < th).mean() - al / 2) < 4 * math.sqrt(al / 2 / 400_000) + 1e-4 and abs((lo > th).mean() - al / 2) < 4 * math.sqrt(al / 2 / 400_000) + 1e-4)
# for contrast: the normal interval 2*mean +- 1.96*2s/sqrt(n) undercovers at n = 5
X = 10.0 * rng.random((400_000, 5))
c2, s2 = 2 * X.mean(axis=1), 2 * X.std(axis=1, ddof=1) / math.sqrt(5)
cn = ((c2 - 1.96 * s2 <= 10) & (10 <= c2 + 1.96 * s2)).mean()
print('     contrast: normal-approximation interval at n = 5 covers', round(cn, 4))

# ---------- planted wrong solutions ----------
COV = '''
def bump_coverage(theta, n, level, trials, seed):
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        delays = [theta * rng.random() for _ in range(n)]
        lo, hi = bump_interval(delays, level)
        if lo <= theta <= hi:
            hits += 1
    return hits / trials
'''
IV = '''import random

def bump_interval(delays, level):
    n = len(delays)
    m = max(delays)
    a = 1 - level
    return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)
'''
def iv(body):
    return 'import random, math, statistics\n\ndef bump_interval(delays, level):\n    n = len(delays)\n    m = max(delays)\n    a = 1 - level\n' + body + COV


BUGS = {
    'shortest interval [M, M / a^(1/n)]': iv('    return m, m / a ** (1 / n)\n'),
    'a not halved': iv('    return m / (1 - a) ** (1 / n), m / a ** (1 / n)\n'),
    'ends swapped (hi, lo)': iv('    return m / (a / 2) ** (1 / n), m / (1 - a / 2) ** (1 / n)\n'),
    'multiplies by the quantiles': iv('    return m * (a / 2) ** (1 / n), m * (1 - a / 2) ** (1 / n)\n'),
    'power n, not 1/n': iv('    return m / (1 - a / 2) ** n, m / (a / 2) ** n\n'),
    'last delay, not the largest': iv('    m = delays[-1]\n    return m / (1 - a / 2) ** (1 / n), m / (a / 2) ** (1 / n)\n'),
    'normal interval 2*mean +- z*2s/sqrt(n)': iv('    z = statistics.NormalDist().inv_cdf(1 - a / 2)\n    c = 2 * sum(delays) / n\n    s = 2 * statistics.stdev(delays) / n ** 0.5\n    return c - z * s, c + z * s\n'),
    'unbiased point (n+1)/n M scaled both ways': iv('    c = (n + 1) / n * m\n    return c * (a / 2) ** (1 / n) * 2, c / (a / 2) ** (1 / n)\n'),
    'coverage counts misses': IV + COV.replace('return hits / trials', 'return 1 - hits / trials'),
    'coverage returns the count': IV + COV.replace('return hits / trials', 'return hits'),
    'coverage draws on [0, 1), not [0, theta)': IV + COV.replace('theta * rng.random()', 'rng.random()'),
    'coverage reseeds each trial': IV + COV.replace('    for _ in range(trials):\n', '    for t in range(trials):\n        rng = random.Random(seed + t)\n'),
    'coverage draws all delays first, trial-major order swapped': IV + COV.replace(
        "        delays = [theta * rng.random() for _ in range(n)]\n", "        delays = [theta * v for v in pool[_::trials]]\n").replace(
        "    hits = 0\n", "    hits = 0\n    pool = [rng.random() for _ in range(n * trials)]\n"),
}
for name, code in BUGS.items():
    r = run_tests(code)
    bad = [i + 1 for i, x in enumerate(r) if x is not True]
    check(f'planted "{name}" caught', bool(bad), f'fails tests {bad}')

# valid variants that must pass: global random.seed, rng.uniform, numpy-free explicit loop, strict inequality
OK = {
    'random.seed and random.random': IV + COV.replace('rng = random.Random(seed)', 'random.seed(seed)').replace('rng.random()', 'random.random()'),
    'rng.uniform(0, theta)': IV + COV.replace('theta * rng.random()', 'rng.uniform(0, theta)'),
    'strict lo < theta < hi': IV + COV.replace('lo <= theta <= hi', 'lo < theta < hi'),
    'exp and log endpoints': 'import random, math\n\ndef bump_interval(delays, level):\n    n, m, a = len(delays), max(delays), 1 - level\n    return m * math.exp(-math.log(1 - a / 2) / n), m * math.exp(-math.log(a / 2) / n)\n' + COV,
}
for name, code in OK.items():
    r = run_tests(code)
    check(f'valid variant "{name}" passes all tests', all(x is True for x in r), str(r))

# byKey lines each fire for a planted slip
for key, name in (('test-2', 'normal interval 2*mean +- z*2s/sqrt(n)'), ('test-5', 'last delay, not the largest'),
                  ('test-6', 'coverage reseeds each trial'), ('test-1', 'shortest interval [M, M / a^(1/n)]')):
    check(f'byKey {key} fires for "{name}"', key in item['feedback']['byKey'] and run_tests(BUGS[name])[int(key[5:]) - 1] is not True)

# ---------- voice ----------
def sentences(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'`[^`]*`', 'CODE', t)
    t = re.sub(r'\$[^$]*\$', 'MATH', t)
    return [p for line in t.split('\n') for p in re.split(r'(?<=[.?:])\s+', line.strip()) if p]
longest = max(len(p.split()) for p in sentences(text))
check('voice: no !, no em or en dash', '!' not in text and '—' not in text and '–' not in text)
check('voice: longest sentence at most 35 words', longest <= 35, str(longest))
check('explain at most three sentences', len(sentences(item['explain']['text'])) <= 3, str(len(sentences(item['explain']['text']))))

print('failures:', len(fails))
sys.exit(1 if fails else 0)
