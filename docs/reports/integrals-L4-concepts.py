#!/usr/bin/env python3
"""Concept audit integrals-4 (level 4: l14 to l17, review-4, homework-4, problems-4, fluency-l14).

Recomputes every graded key and slip value from its named mistake (sympy / scipy.integrate), the printed tables,
and runs Monte Carlo checks for the empirical claims. Exits 0 only if every check passes. A check that fails
because the content is wrong stays failing (see docs/reviews/audit-integrals-4.md).

Run from the repository root:  python docs/reports/integrals-L4-concepts.py
"""
import json, math, os, re, sys
import numpy as np
import sympy as sp
from scipy import integrate, stats, special

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'integrals')
pi, ln, sqrt = math.pi, math.log, math.sqrt
FAILS, N = [], [0]


def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf8') as fh:
        return json.load(fh)


def at(obj, path):
    for tok in re.findall(r'[^.\[\]]+', path):
        obj = obj[int(tok)] if tok.isdigit() else obj[tok]
    return obj


def check(label, ok, detail=''):
    N[0] += 1
    if not ok:
        FAILS.append(label + (' :: ' + detail if detail else ''))
        print('FAIL', label, detail)


def numeric(fname, base, key, slips=None):
    """The stored answer equals `key` within its own tolerance; each slip's value is what its mistake gives."""
    w = at(load(fname), base + '.widget')
    tol = (w.get('tol') or {}).get('abs', 0) or 1e-9
    check(f'{fname} {base} answer', abs(w['answer'] - key) <= tol, f"stored {w['answer']} computed {key:.6f}")
    stored = {x['id']: x for x in w.get('wrong', [])}
    for sid, val in (slips or {}).items():
        if sid not in stored:
            check(f'{fname} {base} slip {sid}', False, 'slip id missing')
            continue
        t = (stored[sid].get('tol') or {}).get('abs', 0) or 1e-9
        check(f'{fname} {base} slip {sid}', abs(stored[sid]['value'] - val) <= t, f"stored {stored[sid]['value']} computed {val:.6f}")
        check(f'{fname} {base} slip {sid} distinct from key', abs(val - key) > tol + t)
    missing = set(stored) - set(slips or {})
    check(f'{fname} {base} every slip recomputed', not missing, str(missing))


def quad(f, a, b, **kw):
    return integrate.quad(f, a, b, limit=200, **kw)[0]


def trap(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x); h = (b - a) / n
    return h * (y.sum() - 0.5 * (y[0] + y[-1]))


def mid(f, a, b, n):
    h = (b - a) / n
    return h * f(a + (np.arange(n) + 0.5) * h).sum()


x, u, th = sp.symbols('x u theta', positive=True)

# ---------------------------------------------------------------- l14 partial fractions
L14 = 'l14-splitting-fractions'
check('l14 split 1/(x^2-1)', sp.simplify(sp.apart(1 / (x**2 - 1)) - (sp.Rational(1, 2) / (x - 1) - sp.Rational(1, 2) / (x + 1))) == 0)
check('l14 s0 substitution form', abs(quad(lambda t: 1 / (t * t - 1), 2, 3) - quad(lambda v: 1 / (2 * v * sqrt(v + 1)), 3, 8)) < 1e-9)
check('l14 s0 parts form', abs(quad(lambda t: 1 / (t * t - 1), 2, 3) - ((3 / 8 - 2 / 3) + quad(lambda t: 2 * t * t / (t * t - 1)**2, 2, 3))) < 1e-9)
numeric(L14, 'screens[2]', -0.5, {'sign': 0.5, 'flipped': -2})
numeric(L14, 'screens[3]', quad(lambda t: 1 / (t * t - 1), 2, 3),
        {'log-of-bottom': ln(8) - ln(3), 'lost-half': ln(1.5), 'plus-sign': 0.5 * (ln(2) + ln(4)) - 0.5 * ln(3)})
check('l14 s4 repeated factor', sp.simplify(sp.apart(1 / (x**2 * (x + 1))) - (-1 / x + 1 / x**2 + 1 / (x + 1))) == 0)
check('l14 s5 quadratic factor', sp.simplify(1 / (x * (x**2 + 1)) - (1 / x - x / (x**2 + 1))) == 0)
check('l14 s5 key', sp.simplify(sp.diff(sp.log(x) - sp.log(x**2 + 1) / 2, x) - 1 / (x * (x**2 + 1))) == 0)
numeric(L14, 'screens[6]', quad(lambda t: (t * t + 1) / (t * t - 1), 2, 3),
        {'no-division': quad(lambda t: 1 / (t - 1) - 1 / (t + 1), 2, 3), 'whole-part': 1})
check('l14 s6 gap at 4', abs(17 / 15 - 1.1333) < 1e-4 and abs(1 / 3 - 1 / 5 - 0.1333) < 1e-4)
numeric(L14, 'screens[9]', quad(lambda p: 1 / (p * (1 - p)), 0.2, 0.8),
        {'one-side': ln(4), 'sign-slip': ln(0.8 * 0.2) - ln(0.2 * 0.8)})
t_half = sp.nsolve(1 / (1 + 9 * sp.exp(-0.5 * x)) - 0.5, x, 4)
numeric(L14, 'screens[10]', float(t_half), {'forgot-k': ln(9), 'times-k': 0.5 * ln(9), 'ratio': ln(5) / 0.5})
numeric(L14, 'quiz[0]', quad(lambda t: 1 / (t * (t + 1)), 1, 2), {'log-of-bottom': ln(6) - ln(2), 'one-piece': ln(2)})
numeric(L14, 'quiz[3]', quad(lambda t: (3 * t + 5) / ((t + 1) * (t + 2)), 0, 1),
        {'first-only': 2 * ln(2), 'swapped': ln(2) + 2 * ln(1.5)})
# Summary claim "each piece integrates to a logarithm or an arctangent": the repeated-factor piece B/x^2 does neither.
piece = sp.integrate(1 / x**2, x)
check('l14 summary.ideas[0]: every partial-fraction piece is a log or an arctan (CONTENT)', piece.has(sp.log) or piece.has(sp.atan),
      f'integral of 1/x^2 is {piece}')

# ---------------------------------------------------------------- l15 trig integrals and substitution
L15 = 'l15-circles-and-powers'
rows = at(load(L15), 'screens[0].canvas.params.rows')
for r in rows:
    t = trap(lambda v: np.sqrt(1 - v * v), 0, 1, int(r[0]))
    check(f'l15 s0 trapezium n={r[0]}', abs(t - float(r[1])) < 6e-5 and abs(pi / 4 - t - float(r[2])) < 6e-5)
numeric(L15, 'screens[2]', quad(lambda v: math.sin(v)**2, 0, pi), {'box': pi, 'quarter': pi / 4, 'power-rule': 0.0})
check('l15 s3 key', sp.simplify(sp.diff(-sp.cos(x) + sp.cos(x)**3 / 3, x) - sp.sin(x)**3) == 0)
numeric(L15, 'screens[4]', pi / 4, {'forgot-half': quad(lambda v: 1 + math.cos(2 * v), 0, pi / 2), 'forgot-dx': 1.0})
numeric(L15, 'screens[5]', quad(lambda v: 1 / (1 + v * v), 0, sqrt(3)), {'just-dx': sqrt(3), 'log': 0.5 * ln(4)})
numeric(L15, 'screens[6]', quad(lambda v: 1 / sqrt(4 - v * v), 0, 1), {'forgot-a': math.asin(1), 'extra-half': pi / 12})
F = lambda v: v / 2 + math.sin(2 * v) / 4
numeric(L15, 'screens[7]', quad(lambda v: sqrt(1 - v * v), 0, sqrt(3) / 2), {'kept-limits': F(sqrt(3) / 2), 'forgot-dx': math.sin(pi / 3)})
numeric(L15, 'screens[10]', stats.cauchy.cdf(1) - stats.cauchy.cdf(-1),
        {'normal-habit': stats.norm.cdf(1) - stats.norm.cdf(-1), 'one-side': 0.25, 'no-pi': pi / 2})
for r in at(load(L15), 'screens[11].canvas.params.rows'):
    b = float(r[0].replace(',', ''))
    check(f'l15 s11 partial mean b={r[0]}', abs(quad(lambda v: v / (pi * (1 + v * v)), 0, b) - float(r[1])) < 6e-5
          and abs(ln(1 + b * b) / (2 * pi) - float(r[1])) < 6e-5)
check('l15 s11 step per decade', abs(ln(10) / pi - 0.733) < 5e-4)
numeric(L15, 'quiz[0]', 2 / 3, {'power-rule': 0.25, 'no-third': 0.0, 'whole-arch': 4 / 3})
numeric(L15, 'quiz[3]', quad(lambda v: 1 / (4 + v * v), 0, 2), {'forgot-half': pi / 4, 'no-a': math.atan(2)})

# Monte Carlo: the Cauchy sample mean does not settle; the mean of n draws is again standard Cauchy (homework-4 items[8]).
rng = np.random.default_rng(20261126)
REPS = 20000
for n in (10, 1000):
    m = rng.standard_cauchy((REPS, n)).mean(axis=1)
    p = (np.abs(m) <= 1).mean()            # 0.5 if the mean is standard Cauchy; near 1 if it settled on 0
    check(f'MC Cauchy mean of n={n} stays Cauchy', abs(p - 0.5) < 4 * sqrt(0.25 / REPS), f'P(|mean|<=1) = {p:.4f}')
m = rng.standard_normal((REPS, 1000)).mean(axis=1)
check('MC normal mean settles (contrast)', (np.abs(m) <= 1).mean() == 1.0)
# Scale-matched comparison behind the "68% for a normal" remark (finding 9): a normal with quartiles at +/-1 also has P(|X|<=1) = 0.5.
sig = 1 / stats.norm.ppf(0.75)
check('quartile-matched normal has P(|X|<=1) = 0.5', abs(stats.norm.cdf(1 / sig) - stats.norm.cdf(-1 / sig) - 0.5) < 1e-12)
TAIL_C, TAIL_N = 2 * stats.cauchy.sf(5), 2 * stats.norm.sf(5 / sig)
check('tail comparison figures for the fix', abs(TAIL_C - 0.1257) < 5e-4 and abs(TAIL_N - 0.00075) < 5e-5)

# ---------------------------------------------------------------- l16 unbounded integrands
L16 = 'l16-infinite-height'
check('l16 s0 caption values', all(abs(2 - 2 * sqrt(a) - v) < 5e-5 for a, v in ((0.25, 1.0), (0.01, 1.8), (0.001, 1.9368), (0.0001, 1.98))))
numeric(L16, 'screens[1]', quad(lambda v: v**(-1 / 3), 0, 1), {'multiplied': 2 / 3, 'l11-rule': 1 / (1 / 3 - 1)})
numeric(L16, 'screens[2]', quad(lambda v: math.log(v), 0, 1), {'sign': 1.0, 'forgot-minus-x': 0.0})
val = quad(lambda v: math.exp(-v) / sqrt(v), 0, 1)
check('l16 s3 exact value and bounds', abs(val - sqrt(pi) * special.erf(1)) < 1e-8 and abs(val - 1.4936) < 5e-5 and abs(2 / math.e - 0.7358) < 5e-5 and 2 / math.e < val < 2)
w = at(load(L16), 'screens[4].widget')
ns = {}
exec(w['prelude'] + w['solution'], ns)
for t in w['tests']:
    got = eval(t['call'], ns)
    check('l16 s4 solution passes ' + t['call'], math.isclose(got, float(t['expect']), rel_tol=1e-9))
check('l16 s4 left-endpoint value on test 1', abs(0.25 * sum((0.25 * i)**2 for i in range(4)) - 0.21875) < 1e-12)
for r in at(load(L16), 'screens[5].canvas.params.rows'):
    n = int(r[0]); m = mid(lambda v: v**-0.5, 0, 1, n); c = math.sin(1) - mid(np.cos, 0, 1, n)
    cos_err = float(r[3].strip('$').replace('\\times10^{', 'e').replace('}', ''))
    check(f'l16 s5 midpoint row n={n}', abs(m - float(r[1])) < 6e-5 and abs(2 - m - float(r[2])) < 6e-5 and abs(abs(c) / cos_err - 1) < 0.02)
e10, e100, e1000 = (2 - mid(lambda v: v**-0.5, 0, 1, n) for n in (10, 100, 1000))
check('l16 s5 ratio sqrt(10)', abs(e10 / e100 - sqrt(10)) < 0.01 and abs(e100 / e1000 - sqrt(10)) < 0.01)
first = 2 * sqrt(0.1) - sqrt(2 * 0.1)
check('l16 s5 first strip carries almost all the error', first / e10 > 0.95 and abs((2 - sqrt(2)) - 0.59) < 0.005)
numeric(L16, 'screens[7]', 2 * quad(lambda v: v**-0.5, 0, 1), {'one-half': 2, 'cancel': 0})
chi = lambda v: v**-0.5 * math.exp(-v / 2) / sqrt(2 * pi)
numeric(L16, 'screens[10]', quad(chi, 0, 1), {'one-side': stats.norm.cdf(1) - 0.5, 'no-exp': 2 / sqrt(2 * pi)})
check('l16 s10 chi-square(1) density', abs(quad(chi, 0, 1) - stats.chi2.cdf(1, 1)) < 1e-8 and abs(quad(chi, 0, np.inf) - 1) < 1e-7)
numeric(L16, 'screens[11]', stats.arcsine.cdf(0.1), {'uniform-habit': 0.1, 'no-two-pi': math.asin(sqrt(0.1))})
numeric(L16, 'quiz[0]', quad(lambda v: v**-0.8, 0, 1), {'l11-rule': 1 / (0.8 - 1), 'p-times': 0.8})
numeric(L16, 'quiz[2]', quad(lambda v: v**-0.5, 0, 9), {'no-two': 3, 'no-root': 18})
check('l16 quiz[3] exact value', abs(quad(lambda v: 1 / (sqrt(v) * (1 + v)), 0, 1) - pi / 2) < 1e-8)

# Monte Carlo: share of time a fair +/-1 game is ahead (Feller's convention for a step that touches 0).
# The arcsine figure 0.2048 is the long-game limit; a short game gives a visibly larger chance.
def share_ahead(n, reps):
    s = np.cumsum(rng.choice(np.array([-1, 1], dtype=np.int8), size=(reps, n)), axis=1, dtype=np.int32)
    prev = np.concatenate([np.zeros((reps, 1), dtype=np.int32), s[:, :-1]], axis=1)
    return ((s > 0) | ((s == 0) & (prev > 0))).mean(axis=1)
p_long = (share_ahead(2000, 20000) <= 0.1).mean()
p_short = (share_ahead(20, 20000) <= 0.1).mean()
check('MC arcsine law, long game', abs(p_long - 0.2048) < 0.012, f'{p_long:.4f}')
check('MC arcsine law is a limit (short game differs)', p_short - 0.2048 > 0.04, f'{p_short:.4f}')

# ---------------------------------------------------------------- l17 volumes and arc length
L17 = 'l17-solids-of-revolution'
numeric(L17, 'screens[0]', pi * mid(lambda v: (v / 3)**2, 0, 3, 3), {'right-edges': pi * (1 / 9 + 4 / 9 + 1), 'no-pi': 35 / 36, 'whole-cylinder': 3 * pi})
numeric(L17, 'screens[1]', pi * quad(lambda v: (v / 3)**2, 0, 3), {'no-pi': 1, 'not-squared': pi * quad(lambda v: v / 3, 0, 3)})
twelve = pi * mid(lambda v: (v / 3)**2, 0, 3, 12)
quoted = float(re.search(r'12 would give ([0-9.]+)', at(load(L17), 'screens[1].explain.text')).group(1).rstrip('.'))
check('l17 s1 explain: 12 discs figure (CONTENT)', abs(round(twelve, 2) - quoted) < 1e-9, f'12 midpoint discs give {twelve:.4f}, printed {quoted}')
numeric(L17, 'screens[2]', pi * quad(lambda v: v, 0, 4), {'no-pi': 8, 'lost-half': 16 * pi})
numeric(L17, 'screens[3]', pi * quad(lambda v: v**2 - v**4, 0, 1),
        {'squared-gap': pi * quad(lambda v: (v - v * v)**2, 0, 1), 'no-pi': 2 / 15, 'ignored-hole': pi / 3})
numeric(L17, 'screens[4]', quad(lambda v: 2 * pi * v**3, 0, 1), {'discs-in-x': pi / 5, 'lost-two': pi / 4, 'no-pi': 0.5})
check('l17 s4 washers in y agree with shells', abs(pi * quad(lambda yv: 1 - yv, 0, 1) - pi / 2) < 1e-12)
numeric(L17, 'screens[5]', pi * quad(lambda v: v**4, 0, 2), {'squared-integral': pi * (8 / 3)**2, 'not-squared': pi * 8 / 3})
chords = sqrt(4 + 8) + sqrt(4 + (8 - 2**1.5)**2)
numeric(L17, 'screens[6]', chords, {'one-chord': sqrt(80), 'run-plus-rise': 12, 'rise-only': 8})
arc = quad(lambda v: sqrt(1 + 9 * v / 4), 0, 4)
numeric(L17, 'screens[7]', arc, {'no-one': 8, 'no-root': 22})
check('l17 chords below arc', sqrt(80) < chords < arc)
check('l17 s8 shell volume', abs(quad(lambda v: 2 * pi * v * sqrt(v), 0, 4) - 128 * pi / 5) < 1e-8 and abs(128 * pi / 5 - 80.42) < 5e-3)
numeric(L17, 'screens[10]', pi * quad(lambda v: v**-2, 1, np.inf), {'no-pi': 1, 'double': 2 * pi})
numeric(L17, 'screens[11]', quad(lambda r: 2 * pi * r * math.exp(-r * r), 0, np.inf), {'forgot-2pi': 0.5, 'half': pi / 2})
dbl = integrate.dblquad(lambda b, a: math.exp(-(a * a + b * b)) / pi, -8, 8, -8, 8)[0]
check('l17 s11 density integrates to 1 with variance 1/2 each', abs(dbl - 1) < 1e-7 and
      abs(quad(lambda a: a * a * math.exp(-a * a) / sqrt(pi), -np.inf, np.inf) - 0.5) < 1e-8)
numeric(L17, 'quiz[0]', pi * quad(lambda v: 4 * v * v, 0, 1), {'not-squared': pi, 'no-pi': 4 / 3})
numeric(L17, 'quiz[2]', 2 * pi * quad(lambda v: v * (2 - v * v), 0, 1), {'discs-in-x': pi * quad(lambda v: (2 - v * v)**2, 0, 1), 'lost-two': 3 * pi / 4})
numeric(L17, 'quiz[3]', quad(lambda v: sqrt(1 + v), 0, 3), {'no-one': quad(lambda v: sqrt(v), 0, 3), 'chord': sqrt(9 + (2 / 3 * 3**1.5)**2)})

# ---------------------------------------------------------------- review-4
R = 'review-4'
numeric(R, 'items[0]', quad(lambda v: 1 / (v * (v + 2)), 1, 3), {'lost-half': ln(9 / 5), 'log-of-bottom': ln(15) - ln(3)})
numeric(R, 'items[1]', stats.cauchy.sf(1), {'half': 0.5, 'three-quarters': 0.75})
numeric(R, 'items[2]', quad(lambda v: v**-0.75, 0, 4), {'unit-interval': 4, 'l11-rule': 4**0.25 / (0.75 - 1)})
numeric(R, 'items[3]', quad(lambda v: 2 * pi * v**3, 0, 2), {'discs-in-x': 32 * pi / 5, 'lost-two': 4 * pi})
numeric(R, 'items[6]', quad(lambda v: 1 / (v * v - 1), 2, np.inf), {'forgot-lower': 0, 'lost-half': ln(3)})
numeric(R, 'items[7]', quad(lambda v: sqrt(4 - v * v), 0, 2), {'kept-limits': 4 * F(2), 'forgot-dx': 2})
numeric(R, 'items[8]', quad(lambda v: 1 / sqrt(1 - v * v), 0, 1), {'area': pi / 4, 'whole-circle': pi})
# items[5], option "ln 2": its why names "evaluated ln|x| at 1 and at -1", which gives 0 (option B's value), not ln 2.
named = ln(abs(1)) - ln(abs(-1))
check('review-4 items[5] option ln 2: named mistake gives ln 2 (CONTENT)', abs(named - ln(2)) < 1e-9, f'named mistake gives {named}')

# ---------------------------------------------------------------- homework-4
H = 'homework-4'
numeric(H, 'items[3]', quad(lambda v: 2 * pi * v * (v - v * v), 0, 1), {'washers-about-x': 2 * pi / 15, 'lost-two': pi / 12})
numeric(H, 'items[4]', quad(lambda v: math.log(v) / sqrt(v), 0, 1), {'sign': 4, 'half': -2, 'no-second-term': 0})
g = lambda v: 1 / (1 + v * v)**2
numeric(H, 'items[5]', quad(g, 0, 1), {'kept-limits': F(1), 'no-extra': pi / 8})
t16 = trap(lambda v: 1 / (1 + v * v)**2, 0, 1, 16)
check('homework-4 items[5] explain: 16 trapezium strips give 0.6427 (CONTENT)', round(t16, 4) == 0.6427, f'T16 = {t16:.6f}')
check('homework-4 items[5]: 32 strips do give 0.6427 (fix)', round(trap(lambda v: 1 / (1 + v * v)**2, 0, 1, 32), 4) == 0.6427)
check('homework-4 items[6] values', abs(quad(lambda v: v**-0.99, 0, 1) - 100) < 1e-4 and abs(1 / (1.01 - 1) - 100) < 1e-9)
numeric(H, 'items[7]', 2 * ln(19) / 0.8, {'half': ln(19) / 0.8, 'no-k': 2 * ln(19)})
check('homework-4 items[8] partial means', all(abs(ln(1 + b * b) / (2 * pi) - v) < 5e-3 for b, v in ((10, 0.73), (100, 1.47), (1e6, 4.40))))
check('homework-4 items[8] quartiles', abs(stats.cauchy.ppf(0.75) - 1) < 1e-12)

# ---------------------------------------------------------------- problems-4
P = 'problems-4'
wt = lambda t: 1 / (sqrt(t) * (1 + sqrt(t)) * (2 + sqrt(t)))
numeric(P, 'items[0].parts[0]', quad(lambda t: 0.5 / sqrt(t), 0, 4), {'no-half': 4, 'unit-rule': 1})
check('problems-4 0.1 key', sp.simplify(sp.diff(2 * sp.log(1 + u) - 2 * sp.log(2 + u), u) - 2 / ((1 + u) * (2 + u))) == 0)
G = lambda v: 2 * ln((1 + v) / (2 + v))
i4 = quad(wt, 0, 4); tot = quad(wt, 0, 1) + quad(wt, 1, np.inf)
numeric(P, 'items[0].parts[2]', i4, {'t-limits': G(4) - G(0), 'sign': -i4, 'no-two': i4 / 2})
numeric(P, 'items[0].parts[3]', tot, {'no-two': ln(2), 'sign': -2 * ln(2), 'top-only': 0})
numeric(P, 'items[0].parts[4]', i4 / tot, {'inverse': tot / i4, 't-limits': (G(4) - G(0)) / tot})
numeric(P, 'items[1].parts[0]', pi * quad(lambda v: (1 - v)**-0.5, 0, 1), {'no-pi': 2, 'p-plus': pi / 1.5})
numeric(P, 'items[1].parts[1]', pi * quad(lambda v: 1 / sqrt(1 - v * v), 0, 0.5), {'x-limits': pi / 2, 'no-pi': pi / 6, 'tan-form': pi * math.atan(0.5)})
numeric(P, 'items[1].parts[2]', pi * quad(lambda v: 1 / sqrt(1 - v * v), 0, 1), {'no-pi': pi / 2, 'tan-form': pi * pi / 4, 'x-limits': pi})
numeric(P, 'items[1].parts[3]', math.sin(pi / 4), {'half-x': 0.5, 'no-sine': pi / 4})
fx = lambda v: v / ((v + 1) * (v + 2))
numeric(P, 'items[2].parts[0]', 2, {'sign': -2, 'top-one': -1})
vy = 2 * pi * quad(lambda v: v * fx(v), 0, 2); vx = pi * quad(lambda v: fx(v)**2, 0, 2); area = quad(fx, 0, 2)
numeric(P, 'items[2].parts[1]', vy, {'no-divide': 2 * pi * (ln(3) - 4 * ln(2)), 'no-2pi': vy / (2 * pi), 'disc': vx})
numeric(P, 'items[2].parts[2]', vx, {'square-integral': pi * area**2, 'no-square': pi * area, 'cross-term': pi * 5 / 3})
check('problems-4 2.2 accept line 0.141 and 0.140 accepted', abs(0.141 - vx) <= 0.001 and abs(0.140 - vx) <= 0.001)
numeric(P, 'items[2].parts[3]', round(vy / vx), {'inverse': vx / vy, 'square-integral': vy / (pi * area**2)})
check('problems-4 2.3 ratio and max height', abs(vy / vx - 14.55) < 0.01 and abs(fx(sqrt(2)) - 0.17) < 0.005)
c2 = lambda v: math.cos(v)**2
numeric(P, 'items[3].parts[0]', quad(c2, -pi / 2, pi / 2), {'x-limits': quad(c2, 2, 4), 'no-half': pi, 'quarter': pi / 4})
sc = lambda v: math.sin(v) * math.cos(v)**2
numeric(P, 'items[3].parts[1]', quad(sc, -pi / 2, pi / 2), {'half-range': 1 / 3, 'x-limits': quad(sc, 2, 4)})
torus = quad(lambda v: 2 * pi * v * 2 * sqrt(max(0.0, 1 - (v - 3)**2)), 2, 4)
numeric(P, 'items[3].parts[2]', torus, {'no-half': 12 * pi * pi, 'no-radius': 2 * pi * pi, 'quarter': 3 * pi * pi})
numeric(P, 'items[3].parts[4]', 100 / (2 * pi * pi), {'no-half': 100 / (4 * pi * pi), 'area-times-R': 100 / pi})
# accept lines: each printed figure is accepted by its own tolerance
for it in load(P)['items']:
    for p in it['parts']:
        w = p['widget']
        mt = re.search(r'accepted as \$?([0-9.]+) \\pm', str(w.get('accept', '')))
        if mt:
            check('problems-4 accept figure within tolerance ' + mt.group(1), abs(float(mt.group(1)) - w['answer']) <= w['tol']['abs'])

# ---------------------------------------------------------------- fluency-l14 (generated families, exhaustive over the grid)
bad = 0
for ca in range(-5, 6):
    for cb in range(-5, 6):
        for a in range(-4, 5):
            for b in range(-4, 5):
                if 0 in (ca, cb, a, b) or a == b:
                    continue
                s, t0 = ca + cb, -(ca * b + cb * a)
                if s * a + t0 != ca * (a - b):                       # the top at x = a
                    bad += 1
                if (s * a + t0) / (a - b) != ca:                     # cover-up gives A = ca
                    bad += 1
check('fluency-l14 cover-up family identities', bad == 0)
bad = 0
for ca in (-5, -2, 1, 3):
    for cb in (-4, 2, 5):
        for (a, b) in ((-1, -2), (-1, -3), (-2, -5), (-3, -4)):
            for (lo, hi) in ((0, 1), (1, 3), (0, 2)):
                s, t0 = ca + cb, -(ca * b + cb * a)
                num = quad(lambda v: (s * v + t0) / ((v - a) * (v - b)), lo, hi)
                ans = ca * ln((hi - a) / (lo - a)) + cb * ln((hi - b) / (lo - b))
                bad += abs(num - ans) > 1e-9
check('fluency-l14 split-between-limits family key', bad == 0)

print(f'{N[0]} checks, {len(FAILS)} failed')
for f in FAILS:
    print('  -', f)
sys.exit(1 if FAILS else 0)
