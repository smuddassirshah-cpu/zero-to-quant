"""Recompute every number in app/content/courses/garch/problems-<n>.json twice.

Method 1 is exact or closed form (fractions.Fraction, sums written out by hand). Method 2 takes another route:
NumPy linear algebra (a stationary vector, a covariance matrix summed in full), numerical integration of a
mixture density with SciPy, a fixed-seed simulation, numpy and scipy.stats on raw data, or a brute search.
For each numeric part: the two methods agree; the key lies within its tol of them; the value at the rounding the
question asks for is accepted; each `wrong` value equals its named slip recomputed here, has a byKey line and lies
outside the key's band; no two wrong bands overlap; the question names its form. Numbers stated in feedback and
explain are checked against the text with numbers_lib (Level.expect), and Level.check_wrongs runs on each set.
Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-garch-numbers.py
"""
import json, os, re, sys, math
from fractions import Fraction as F
import numpy as np
from scipy import integrate, stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'garch')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

FORM = re.compile(r'decimal|places?\b|fraction|whole number|nearest|per cent|percentage|%', re.I)
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    return json.load(open(p))


SETS = {n: load(n) for n in (1, 2, 3)}


def part(n, iid, p):
    items = {it['id']: it for it in SETS[n]['items']}
    return items[iid]['parts'][p - 1]


def num(n, iid, p, v1, v2, slips, rounded, agree=1e-9, slip_tol=None):
    """v1, v2: the value two ways. slips: {wrong id: recomputed value}. rounded: the figure at the asked rounding
    (in the widget's units: a fraction when unit is %)."""
    pt = part(n, iid, p)
    w, tag = pt['widget'], f'L{n} {iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} is numeric')
    v1, v2 = float(v1), float(v2)
    ok(abs(v1 - v2) <= agree * max(1.0, abs(v1)), f'{tag} methods agree {v1} vs {v2}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - v1) <= tol, f'{tag} key {w["answer"]} within {tol} of {v1}')
    ok(abs(rounded - v1) <= tol + 1e-12, f'{tag} rounded {rounded} accepted')
    if not float(w['answer']).is_integer():
        ok(bool(FORM.search(pt['question'])), f'{tag} question states its form')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} == slips {sorted(slips)}')
    bk = pt['feedback'].get('byKey', {})
    bands = []
    for wid, sv in slips.items():
        if wid not in ids:
            continue
        x = ids[wid]
        st = slip_tol or max(x['tol']['abs'], 1e-9) + 1e-12
        ok(abs(x['value'] - float(sv)) <= st, f'{tag} wrong {wid} {x["value"]} == slip {float(sv):.6g}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag} wrong {wid} outside key band')
        ok(wid in bk, f'{tag} wrong {wid} has a byKey line')
        bands.append((x['value'] - x['tol']['abs'], x['value'] + x['tol']['abs'], wid))
    bands.sort()
    for a, b in zip(bands, bands[1:]):
        ok(a[1] < b[0], f'{tag} wrong bands {a[2]} and {b[2]} do not overlap')


def said(lv, iid_index, p, field, values, fmt=None):
    """Each value is stated in the part's field (question, feedback.correct, explain.text or feedback.byKey.<id>)."""
    for v in values:
        lv.expect('problems', f'items[{iid_index}].parts[{p - 1}].{field}', v, fmt)


def shape(n, lessons_of_level):
    d = SETS[n]
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'garch', f'L{n} header')
    ok(3 <= len(d['items']) <= 5, f'L{n} 3 to 5 items')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'L{n} one item at difficulty 5')
    typed = sum(pt['widget']['kind'] in ('numeric', 'expression') for it in d['items'] for pt in it['parts'])
    total = sum(len(it['parts']) for it in d['items'])
    ok(3 * typed >= 2 * total, f'L{n} typed parts {typed} of {total}')
    for it in d['items']:
        ok(3 <= len(it['parts']) <= 5 and 3 <= it['difficulty'] <= 5, f'L{n} {it["id"]} parts and difficulty')


# ---------------------------------------------------------------- level 1
def level1():
    lv = Level('garch', 1)
    shape(1, None)

    # P1 a stale calm sd against a storm (re-authored in the fix pass, replaces p-two-regime-tails)
    I = 'p-stale-alarm'
    A, s_st = 14.5, 2.1
    dly = A / math.sqrt(252)
    dly2 = math.sqrt(A ** 2 / 252)                                   # method 2: through the variance
    num(1, I, 1, 3 * dly / 100, 3 * dly2 / 100,
        {'annual': 3 * A / 100, 'calendar': 3 * A / math.sqrt(365) / 100, 'one-sd': dly / 100, 'two-fifty-two': 3 * A / 252 / 100},
        0.0274, slip_tol=1e-6)
    pa = 2 * stats.norm.sf(2.74 / s_st)
    pa2 = 1 - integrate.quad(lambda x: stats.norm.pdf(x, 0, s_st), -2.74, 2.74)[0]       # method 2: integrate the middle
    num(1, I, 2, pa, pa2, {'one-tail': pa / 2, 'normal': 2 * stats.norm.sf(3), 'inside': 1 - pa}, 0.192, agree=1e-8, slip_tol=1e-4)
    ok(abs(2 * stats.norm.sf(3 * dly / s_st) - pa) < 0.0006, 'L1 P1 p2 the unrounded threshold gives a value in the band')
    rng = np.random.default_rng(7)
    sim = np.mean(np.abs(rng.normal(0, s_st, 2_000_000)) > 2.74)
    ok(abs(sim - pa) < 0.001, f'L1 P1 p2 simulation {sim:.4f} agrees')
    rt = 19.2 / 0.27
    num(1, I, 3, rt, float(F(192, 10) / F(27, 100)), {'one-tail': 19.2 / 0.135, 'percent': 19.2 / 0.0027}, 71.1, slip_tol=0.01)
    ok(abs(pa / (2 * stats.norm.sf(3)) - rt) < 0.06, 'L1 P1 p3 the unrounded chances give 71.1 too')
    sx = s_st / 0.9134
    m2x = integrate.quad(lambda x: x ** 2 * stats.norm.pdf(x, 0, sx), -60, 60)[0]
    m4x = integrate.quad(lambda x: x ** 4 * stats.norm.pdf(x, 0, sx), -60, 60)[0]
    num(1, I, 4, 3, m4x / m2x ** 2, {'excess': 0, 'no-divide': 3 * sx ** 4}, 3.00, agree=1e-7, slip_tol=0.01)
    xs = rng.normal(0, s_st, 2_000_000) / 0.9134
    ok(abs(stats.kurtosis(xs, fisher=False) - 3) < 0.02, 'L1 P1 p4 simulated raw kurtosis near 3')
    said(lv, 0, 1, 'feedback.correct', [0.9134, 2.74])
    said(lv, 0, 1, 'explain.text', [15.8745, 0.9134, 2.74])
    said(lv, 0, 1, 'feedback.byKey.annual', [43.5])
    said(lv, 0, 2, 'feedback.correct', [1.305, 19.2])
    said(lv, 0, 2, 'feedback.byKey.one-tail', [9.6])
    said(lv, 0, 2, 'feedback.byKey.inside', [80.8])
    said(lv, 0, 2, 'explain.text', [1.305, 19.2])
    said(lv, 0, 3, 'feedback.correct', [71.1])
    said(lv, 0, 3, 'explain.text', [0.0135, 0.96, 71])
    said(lv, 0, 4, 'feedback.correct', [2.299])
    said(lv, 0, 4, 'feedback.byKey.no-divide', [83.82])
    lv.claim(abs(dly - 0.9134) < 5e-5 and abs(math.sqrt(252) - 15.8745) < 5e-5 and abs(2.74 / 2.1 - 1.305) < 5e-4, 'L1 P1 0.9134, 15.8745, 1.305')
    lv.claim(abs(5 * 0.0027 - 0.0135) < 1e-12 and abs(5 * 0.192 - 0.96) < 1e-12 and round(rt) == 71, 'L1 P1 week counts 0.0135 and 0.96')
    lv.claim(abs(sx - 2.299) < 5e-4 and abs(3 * 14.5 - 43.5) < 1e-12 and 0.15 < pa < 0.25, 'L1 P1 2.299, 43.5, one day in five')

    # P2 correlated days
    I = 'p-stale-prices-scaling'
    n, s, r = 1200, 1.2, 0.12
    band = 1.96 / math.sqrt(n)
    num(1, I, 1, band, 1.96 * n ** -0.5, {'no-root': 1.96 / n, 'no-196': 1 / math.sqrt(n)}, 0.0566, slip_tol=1e-4)

    def cov_sum(days, lag1):
        S = np.eye(days) + lag1 * (np.eye(days, k=1) + np.eye(days, k=-1))
        return float(np.ones(days) @ S @ np.ones(days)) * s * s

    wk = s * s * (5 + 8 * r)
    num(1, I, 2, math.sqrt(wk) / 100, math.sqrt(cov_sum(5, r)) / 100,
        {'ten-pairs': math.sqrt(s * s * (5 + 20 * r)) / 100, 'one-way': math.sqrt(s * s * (5 + 4 * r)) / 100,
         'root-five': math.sqrt(5) * s / 100}, 0.0293, slip_tol=6e-6)
    yr = s * s * (252 + 502 * r)
    num(1, I, 3, math.sqrt(yr) / 100, math.sqrt(cov_sum(252, r)) / 100,
        {'one-way': math.sqrt(s * s * (252 + 251 * r)) / 100, 'root-rule': math.sqrt(252) * s / 100}, 0.2120, slip_tol=6e-6)
    ratio = math.sqrt(yr) / (math.sqrt(252) * s)
    num(1, I, 4, ratio, math.sqrt(cov_sum(252, r) / cov_sum(252, 0)),
        {'variance': (252 + 502 * r) / 252, 'upside-down': 1 / ratio,
         'one-way': math.sqrt(252 + 251 * r) / math.sqrt(252)}, 1.113, slip_tol=1e-4)
    said(lv, 1, 2, 'feedback.correct', [8.5824, 2.93])
    said(lv, 1, 2, 'explain.text', [0.3456, 8.5824, 2.93, 2.68])
    said(lv, 1, 3, 'feedback.correct', [312.24, 449.63, 21.20])
    said(lv, 1, 4, 'feedback.correct', [21.20, 19.05, 1.113])
    said(lv, 1, 4, 'explain.text', [1.2, 1.113, 251, 23.9])
    lv.claim(abs((312.24 / 252 - 1) * 100 - 23.9) < 0.05 and abs(21.20 / 19.05 - 1.113) < 5e-4, 'L1 P2 the pairs add 23.9%; 21.20/19.05 = 1.113')
    lv.claim(abs(1.96 / 1200 - 0.0016333) < 1e-7, 'L1 P2 no-root slip 1.96/1200')
    lv.claim(abs(2 * 0.12 * 1.44 - 0.3456) < 1e-12 and abs(5 * 1.44 + 4 * 0.3456 - 8.5824) < 1e-12, 'L1 P2 pair term and weekly variance')
    lv.claim(abs(math.sqrt(1200) - 34.64) < 0.005 and band > 0 and 0.12 > 2 * band, 'L1 P2 0.12 more than twice the band')
    lv.claim(abs(math.sqrt(252) * 1.2 - 19.05) < 0.005 and abs(math.sqrt(s * s * (252 + 251 * r)) - 20.16) < 0.005, 'L1 P2 19.05 and 20.16')
    lv.claim(abs(ratio - 1) * 100 > 10.5 and abs(ratio - 1) * 100 < 11.5, 'L1 P2 understates by about 11%')

    # P3 eight days
    I = 'p-eight-day-window'
    x = [F(9, 10), F(-4, 10), F(16, 10), F(-7, 10), F(3, 10), F(-41, 10), F(11, 10), F(5, 10)]
    xa = np.array([float(v) for v in x])
    k = len(x)
    mean = sum(x) / k
    ms = sum(v * v for v in x) / k
    ok(sum(x) == F(-8, 10) and mean == F(-1, 10) and sum(v * v for v in x) == F(2238, 100), 'L1 P3 prose sums')
    num(1, I, 1, math.sqrt(ms) / 100, math.sqrt(np.mean(xa ** 2)) / 100,
        {'seven': math.sqrt(sum(v * v for v in x) / 7) / 100, 'no-root': float(ms) / 100,
         'abs': float(np.mean(np.abs(xa))) / 100}, 0.01673, slip_tol=6e-6)
    s2 = F(k, k - 1) * (ms - mean ** 2)
    num(1, I, 2, math.sqrt(s2) / 100, float(np.std(xa, ddof=1)) / 100,
        {'population': math.sqrt(ms - mean ** 2) / 100, 'no-mean': math.sqrt(F(k, k - 1) * ms) / 100,
         'variance': float(s2) / 100}, 0.01785, slip_tol=6e-6)
    num(1, I, 3, math.sqrt(252) * 0.01785, math.sqrt(252 * 0.01785 ** 2),
        {'zero-mean': math.sqrt(252 * ms) / 100, 'calendar': math.sqrt(365 * s2) / 100}, 0.2834, slip_tol=6e-6)
    ok(abs(math.sqrt(252 * s2) / 100 - part(1, I, 3)['widget']['answer']) <= part(1, I, 3)['widget']['tol']['abs'],
       'L1 P3 p3 the unrounded s (28.33%) is accepted too')
    d = [v - mean for v in x]
    m4 = sum(v ** 4 for v in d) / k
    m2 = sum(v * v for v in d) / k
    ok(sum(v ** 4 for v in d) == F(2677186, 10000) and m2 == F(7, 8) * s2, 'L1 P3 fourth powers 267.7186 and m2 = 7/8 s^2')
    ex = m4 / m2 ** 2 - 3
    num(1, I, 4, ex, stats.kurtosis(xa, fisher=True, bias=True),
        {'raw': ex + 3, 'sample-var': m4 / s2 ** 2 - 3}, 1.31, slip_tol=1e-4)
    said(lv, 2, 1, 'feedback.correct', [2.7975, 1.673])
    said(lv, 2, 1, 'explain.text', [22.38, 2.7975, 1.673, 16.81])
    said(lv, 2, 2, 'feedback.correct', [2.7875, 3.1857, 1.785])
    said(lv, 2, 3, 'feedback.correct', [15.8745, 1.785, 28.34])
    said(lv, 2, 3, 'explain.text', [15.8745, 28.34])
    said(lv, 2, 3, 'feedback.byKey.calendar', [34.10])
    said(lv, 2, 4, 'feedback.correct', [33.4648, 7.7702, 4.307, 1.31])
    lv.claim(F(-41, 10) ** 2 == F(1681, 100), 'L1 P3 the -4.1 day squares to 16.81')
    lv.claim(abs(float(m4) - 33.4648) < 5e-5 and abs(float(m2) ** 2 - 7.7702) < 5e-5, 'L1 P3 33.4648 and 7.7702')
    lv.claim(abs(math.sqrt(365) * 1.784857 - 34.10) < 0.005, 'L1 P3 calendar slip 34.10')

    # P4 big-day indicator
    I = 'p-big-day-indicator'
    N, big, fol = 1500, 75, 18
    q, p = F(fol, big), F(big, N)
    # method 2: phi coefficient of the stationary 2 by 2 table of (I_{t-1}, I_t)
    P11, P10 = p * q, p * (1 - q)
    P01 = P10
    P00 = 1 - P11 - P10 - P01
    phi = (P11 * P00 - P10 * P01) / math.sqrt(float((P11 + P10) * (P01 + P00) * (P11 + P01) * (P10 + P00)))
    num(1, I, 1, q, fol / big, {'all-days': F(fol, N), 'base': p}, 0.24)
    rho = (q - p) / (1 - p)
    num(1, I, 2, rho, phi, {'no-divide': q - p, 'ratio': q / p}, 0.20)
    lm = (N - 1) * rho ** 2
    num(1, I, 3, lm, (N - 1) * phi ** 2, {'no-square': (N - 1) * rho, 'from-019': (N - 1) * (q - p) ** 2}, 59.96, slip_tol=1e-4)
    crit = stats.chi2.ppf(0.95, 1)
    ok(abs(crit - 3.841) < 5e-4, 'L1 P4 chi2_1 critical 3.841')
    brute = next(c for c in range(big + 1) if F(c, big) > p and (N - 1) * ((F(c, big) - p) / (1 - p)) ** 2 > crit)
    thr = p + (1 - p) * math.sqrt(3.841 / (N - 1))
    num(1, I, 4, math.ceil(thr * big), brute,
        {'round-down': brute - 1, 'rho-as-q': round(math.sqrt(3.841 / (N - 1)) * big)}, 8)
    said(lv, 3, 4, 'feedback.correct', [0.0506, 0.0981, 7.36])
    said(lv, 3, 4, 'question', [3.75])
    lmc = lambda c: (N - 1) * float((F(c, big) - p) / (1 - p)) ** 2
    ok(lmc(0) > crit and all(lmc(c) <= crit for c in range(1, 8)) and 0.05 * 75 == 3.75,
       'L1 P4 p4 a count of 0 also rejects, so the question asks for the smallest above 3.75')
    said(lv, 3, 4, 'feedback.byKey.round-down', [0.0933, 0.0456, 3.12])
    said(lv, 3, 3, 'feedback.correct', [0.04, 59.96, 3.84])
    lv.claim(abs(thr - 0.0981) < 5e-5 and abs(thr * 75 - 7.36) < 0.005, 'L1 P4 threshold q 0.0981, 7.36 days')
    lv.claim(abs(math.sqrt(3.841 / 1499) - 1.96 / math.sqrt(1500)) < 1e-4, 'L1 P4 threshold close to the band')
    c7 = (F(7, 75) - p) / (1 - p)
    lv.claim(abs(float(c7) - 0.0456) < 5e-5 and abs(1499 * float(c7) ** 2 - 3.12) < 0.005, 'L1 P4 seven days give LM 3.12')
    lv.check_wrongs('problems')
    lv.report()


# ---------------------------------------------------------------- level 2
def level2():
    import pandas as pd
    from scipy.optimize import brentq
    lv = Level('garch', 2)
    shape(2, None)
    L2PI = math.log(2 * math.pi)

    # P1 EWMA against GARCH, two days, then day 3's score
    I = 'p-two-filters-one-score'
    lam, s0 = F(92, 100), F(144, 100)
    r = [F(-25, 10), F(5, 10), F(-32, 10)]
    e2 = lam * s0 + (1 - lam) * r[0] ** 2
    e3 = lam * e2 + (1 - lam) * r[1] ** 2
    # method 2: pandas ewm with the start fed in front (lesson 5's alignment)
    ew = pd.Series([1.44, 6.25, 0.25]).ewm(alpha=0.08, adjust=False).mean().to_numpy()
    num(2, I, 1, e2, ew[1], {'swapped': (1 - lam) * s0 + lam * r[0] ** 2, 'no-square': lam * s0 + (1 - lam) * r[0],
                             'decimal': e2 / 10000}, 1.8248, slip_tol=1e-8)
    num(2, I, 2, e3, ew[2], {'old-return': lam * e2 + (1 - lam) * r[0] ** 2, 'from-start': lam * s0 + (1 - lam) * r[1] ** 2}, 1.6988, agree=1e-9, slip_tol=1e-4)
    w, a, b = F(4, 100), F(7, 100), F(90, 100)
    g2 = w + a * r[0] ** 2 + b * s0
    g3 = w + a * r[1] ** 2 + b * g2
    # method 2: the unrolled two-step formula
    g3b = w * (1 + b) + a * (r[1] ** 2 + b * r[0] ** 2) + b * b * s0
    num(2, I, 3, g3, g3b, {'one-step': w + a * r[1] ** 2 + b * s0, 'stopped': g2, 'no-omega': a * r[1] ** 2 + b * g2,
                           'decimal': g3 / 10000}, 1.6537, slip_tol=1e-4)
    ll = lambda v, x: -0.5 * (L2PI + math.log(v) + x * x / v)
    d = ll(float(e3), -3.2) - ll(float(g3), -3.2)
    d2 = -0.5 * (math.log(float(e3) / float(g3))) - 0.5 * float(F(1024, 100) / e3 - F(1024, 100) / g3)
    num(2, I, 4, d, d2, {'sign': -d, 'no-half': 2 * d, 'log-only': -0.5 * math.log(float(e3) / float(g3))}, 0.069, slip_tol=1e-4)
    said(lv, 0, 1, 'feedback.correct', [1.3248, 0.5, 1.8248])
    said(lv, 0, 2, 'feedback.correct', [1.6788, 0.02, 1.6988])
    said(lv, 0, 3, 'feedback.correct', [1.7735, 1.6537])
    ok(g3 == F(165365, 100000) and abs(part(2, I, 3)['widget']['answer'] - 1.65365) < 1e-12
       and all(abs(v - 1.65365) <= 6e-5 for v in (1.6536, 1.6537)), 'L2 P1 p3 exact tie 1.65365: both roundings taken')
    said(lv, 0, 3, 'explain.text', [1.7735, 0.4375, 0.0175, 1.6537, 1.6988])
    said(lv, 0, 4, 'feedback.correct', [-4.198, -4.267, 0.069])
    lv.claim(abs(ll(float(e3), -3.2) + 4.198) < 5e-4 and abs(ll(float(g3), -3.2) + 4.267) < 5e-4, 'L2 P1 scores -4.198 and -4.267')
    lv.claim(abs(0.5 * math.log(float(e3 / g3)) - 0.013) < 5e-4 and abs(0.5 * float(F(1024, 100) / g3 - F(1024, 100) / e3) - 0.082) < 5e-4,
             'L2 P1 ln term 0.013, surprise term 0.082')
    lv.claim(r[0] ** 2 > 4 * s0, 'L2 P1 6.25 is more than four times 1.44')
    lv.claim(abs(0.04 + 0.9 * 1.44 + 0.4375 - 1.7735) < 1e-12, 'L2 P1 jump 0.4375 on 0.04 + 0.90 x 1.44')

    # P2 weekly ARCH(1) and a GARCH with the same level
    I = 'p-weekly-gas-arch'
    om, al = F(6), F(35, 100)
    V = om / (1 - al)
    it = 0.0
    for _ in range(500):                               # method 2: iterate the expected-variance map to its fixed point
        it = 6.0 + 0.35 * it
    num(2, I, 1, V, it, {'omega': om, 'over-alpha': om / al, 'times': om * al, 'decimal': V / 10000}, 9.23, agree=1e-9, slip_tol=1e-4)
    ann = math.sqrt(52 * V) / 100
    num(2, I, 2, ann, float(np.sqrt(np.sum(np.full(52, it)))) / 100,
        {'days': math.sqrt(252 * V) / 100, 'omega': math.sqrt(52 * om) / 100}, 0.2191, slip_tol=6e-6)
    ok(52 * V == 480, 'L2 P2 52V = 480 exactly')
    nw = om + al * 144
    nn = om + al * nw
    num(2, I, 3, nn, V + al * (nw - V), {'next-week': nw, 'alpha-sq': V + al ** 2 * (nw - V), 'level': V, 'decimal': nn / 10000}, 25.74, slip_tol=1e-3)
    wg = V * (1 - F(12, 100) - F(80, 100))
    wg2 = brentq(lambda x: x / (1 - 0.92) - float(V), 1e-6, 10)
    num(2, I, 4, wg, wg2, {'alpha-only': V * F(12, 100), 'arch-omega': om * F(8, 100), 'decimal': wg / 10000}, 0.7385, agree=1e-9, slip_tol=1e-4)
    gn = wg + F(12, 100) * 144 + F(80, 100) * V
    gn2 = float(V) * 0.08 + 0.12 * 144 + 0.8 * float(V)
    num(2, I, 5, gn, gn2, {'no-beta': wg + F(12, 100) * 144, 'swapped': wg + F(80, 100) * 144 + F(12, 100) * V, 'arch': nw,
                           'decimal': gn / 10000}, 25.40, agree=1e-9, slip_tol=1e-4)
    said(lv, 1, 1, 'feedback.correct', [9.23])
    said(lv, 1, 1, 'explain.text', [9.23, 3.04])
    said(lv, 1, 2, 'feedback.correct', [480, 21.91])
    said(lv, 1, 3, 'feedback.correct', [56.4, 25.74])
    said(lv, 1, 3, 'question', [6.0, 0.35, 144, 9.23])
    said(lv, 1, 1, 'feedback.byKey.omega', [6.0])
    said(lv, 1, 5, 'feedback.generic', [0.7385, 0.12, 144, 0.80, 9.2308])
    said(lv, 1, 3, 'explain.text', [56.4, 25.74, 16.51])
    said(lv, 1, 5, 'feedback.correct', [0.7385, 17.28, 7.3846, 25.40])
    lv.claim(abs(math.sqrt(float(V)) - 3.04) < 5e-3 and abs(float(al * (nw - V)) - 16.51) < 5e-3, 'L2 P2 weekly sd 3.04, gap 16.51')
    lv.claim(abs(float(F(80, 100) * V) - 7.38) < 5e-3, 'L2 P2 beta x V = 7.38')

    # P3 GARCH by moments
    I = 'p-silver-moment-fit'
    p = F(24, 100) / F(25, 100)
    acf = [0.25 * float(p) ** (k - 3) for k in (3, 4)]
    num(2, I, 1, p, acf[1] / acf[0], {'upside-down': 1 / p, 'difference': F(25, 100) - F(24, 100)}, 0.96, slip_tol=1e-4)
    hl = math.log(0.5) / math.log(float(p))
    hl2 = brentq(lambda h: 0.96 ** h - 0.5, 1, 100)
    num(2, I, 2, hl, hl2, {'mean-age': 1 / (1 - p), 'half-mean': F(1, 2) / (1 - p)}, 16.98, agree=1e-9, slip_tol=1e-4)
    vbar = F(289, 100)
    om3 = vbar * (1 - p)
    num(2, I, 3, om3, brentq(lambda x: x / 0.04 - 2.89, 1e-6, 5), {'times-p': vbar * p, 'sample': vbar, 'decimal': om3 / 10000},
        0.1156, agree=1e-9, slip_tol=1e-4)
    # fix pass (finding 14): alpha 0.13, beta 0.83, the pair the lag-3 ACF 0.25 implies
    t = om3 + F(13, 100) * F(2025, 100) + F(83, 100) * vbar
    num(2, I, 4, math.sqrt(t) / 100, float(np.sqrt(0.1156 + 0.13 * 4.5 ** 2 + 0.83 * 2.89)) / 100,
        {'variance': t / 100, 'no-square': math.sqrt(om3 + F(13, 100) * F(45, 10) + F(83, 100) * vbar) / 100,
         'annual': math.sqrt(252 * t) / 100}, 0.0227, slip_tol=6e-6)
    said(lv, 2, 4, 'feedback.correct', [0.1156, 2.6325, 2.3987, 5.1468, 2.27])
    said(lv, 2, 4, 'explain.text', [2.6325, 0.83, 2.89, 5.1468, 2.27, 33, 1.70, 17])
    said(lv, 2, 4, 'feedback.byKey.variance', [5.1468])
    lv.claim(round(100 * (math.sqrt(t) / math.sqrt(2.89) - 1)) == 33, 'L2 P3 tomorrow 33% above the long-run 1.70%')
    # lag-1 ACF of r^2 for GARCH(1,1) (He and Terasvirta 1999): alpha(1 - alpha*beta - beta^2)/(1 - 2 alpha*beta - beta^2)
    acf1 = lambda al, be: al * (1 - al * be - be * be) / (1 - 2 * al * be - be * be)
    al_hat = brentq(lambda al: acf1(al, 0.96 - al) * 0.96 ** 2 - 0.25, 0.01, 0.2)
    ok(round(al_hat, 2) == 0.13 and 3 * 0.13 ** 2 + 2 * 0.13 * 0.83 + 0.83 ** 2 < 1,
       f'L2 P3 p4 lag-3 ACF 0.25 with persistence 0.96 gives alpha {al_hat:.4f}; fourth moment finite')
    rg = np.random.default_rng(3)
    zz = rg.standard_normal(400_000)
    sim_s2, sim_r = 2.89, np.empty(zz.size)
    for ii_, z_ in enumerate(zz):                                  # method 2 for the ACF: simulate the fitted GARCH
        r_ = math.sqrt(sim_s2) * z_
        sim_r[ii_] = r_ * r_
        sim_s2 = 0.1156 + 0.13 * r_ * r_ + 0.83 * sim_s2
    x2 = sim_r - sim_r.mean()
    sim_acf3 = float(np.dot(x2[:-3], x2[3:]) / np.dot(x2, x2))
    ok(abs(sim_acf3 - 0.25) < 0.06, f'L2 P3 p4 simulated lag-3 ACF {sim_acf3:.3f} near 0.25')
    lv.claim(abs(hl - 17) < 0.5, 'L2 P3 half-life about 17 days')

    # P4 EWMA and ARCH after one fall, then quiet days
    I = 'p-crash-then-quiet'
    lam4, s4 = F(95, 100), F(121, 100)
    e1 = lam4 * s4 + (1 - lam4) * 36
    num(2, I, 1, e1, pd.Series([1.21, 36.0]).ewm(alpha=0.05, adjust=False).mean().iloc[-1],
        {'swapped': (1 - lam4) * s4 + lam4 * 36, 'no-square': lam4 * s4 + (1 - lam4) * (-6), 'decimal': e1 / 10000}, 2.9495, slip_tol=1e-4)
    arch = F(8, 10) + F(45, 100) * 36
    ok(arch == 17, 'L2 P4 ARCH gives 17.0')
    num(2, I, 2, math.sqrt(arch / e1), float(np.exp(0.5 * (np.log(17.0) - np.log(float(e1))))),
        {'variance': arch / e1, 'upside-down': math.sqrt(e1 / arch)}, 2.40, slip_tol=1e-4)
    q = F(16, 100)                                     # fix pass (finding 15): quiet days of 0.4%
    e2 = lam4 * e1 + (1 - lam4) * q
    num(2, I, 3, e2, q + lam4 * (e1 - q), {'no-news': lam4 * e1, 'abs': lam4 * e1 + (1 - lam4) * F(4, 10), 'decimal': e2 / 10000}, 2.8100, slip_tol=1e-4)
    floor = F(8, 10) + F(45, 100) * q
    ev, kk = float(e1), 0
    while ev >= float(floor):
        ev, kk = 0.95 * ev + 0.05 * 0.16, kk + 1
    kf = math.log(float((floor - q) / (e1 - q))) / math.log(0.95)
    num(2, I, 4, math.ceil(kf), kk, {'round-down': kk - 1, 'no-floor': math.ceil(math.log(float(floor / e1)) / math.log(0.95))}, 27)
    said(lv, 3, 1, 'feedback.correct', [1.1495, 1.8, 2.9495])
    said(lv, 3, 2, 'feedback.correct', ['5.764', 2.40])
    said(lv, 3, 3, 'feedback.correct', [2.8020, 0.0080, 2.8100])
    said(lv, 3, 3, 'explain.text', [0.16, 0.0080, 2.8100, 0.872])
    said(lv, 3, 4, 'feedback.correct', [0.2552, 26.6, 27])
    said(lv, 3, 4, 'feedback.generic', [2.7895, 0.872])
    said(lv, 3, 1, 'feedback.byKey.swapped', [1.21, 36])
    said(lv, 3, 1, 'explain.text', [36, 30, 1.8, 1.1495, 2.9495, 2.4])
    lv.claim(abs(float(floor) - 0.872) < 1e-12 and abs(0.16 + 0.95 ** 26 * 2.7895 - 0.90) < 5e-3, 'L2 P4 ARCH 0.872; after 26 days about 0.90')
    lv.claim(abs(float(e1) / 1.21 - 2.4) < 0.05 and abs(float(e1) - 0.16 - 2.7895) < 1e-9, 'L2 P4 2.4 times; gap 2.7895')
    lv.claim(36 / 1.21 > 29.5 and abs(0.45 / 0.05 - 9) < 1e-12, 'L2 P4 36 is about 30 times 1.21; 0.45 is nine times 0.05')
    lv.check_wrongs('problems')
    lv.report()


# ---------------------------------------------------------------- level 3
def level3():
    from scipy.optimize import brentq
    lv = Level('garch', 3)
    shape(3, None)
    S = math.sqrt(252)
    z99 = 2.3263
    ok(abs(-stats.norm.ppf(0.01) - z99) < 5e-5, 'L3 z99 2.3263')

    # P1 back out phi and V_L from three forecasts, then day 30's vol and VaR
    I = 'p-forecasts-to-parameters'
    f = [F(69, 100), F(676, 1000), F(66298, 100000)]
    phi = (f[2] - f[1]) / (f[1] - f[0])
    # method 2: f_{h+1} = (1 - phi) V_L + phi f_h is linear; solve it with numpy
    A = np.array([[1.0, float(f[0])], [1.0, float(f[1])]])
    c0, phi2 = np.linalg.solve(A, np.array([float(f[1]), float(f[2])]))
    num(3, I, 1, phi, phi2, {'inverted': 1 / phi, 'levels': f[1] / f[0]}, 0.93, agree=1e-9, slip_tol=1e-4)
    VL = f[0] - (f[0] - f[1]) / (1 - phi)
    num(3, I, 2, VL, c0 / (1 - phi2), {'average': sum(f) / 3, 'gap': (f[0] - f[1]) / (1 - phi), 'decimal': VL / 10000}, 0.49,
        agree=1e-8, slip_tol=1e-4)
    ok(phi == F(93, 100) and VL == F(49, 100), 'L3 P1 exact phi 0.93 and V_L 0.49')
    gap = f[0] - VL
    v30 = VL + phi ** 29 * gap
    e = float(f[0])
    for _ in range(29):                     # step E[s2] = omega + phi E[s2] forward from tomorrow
        e = float((1 - phi) * VL) + float(phi) * e
    s30 = math.sqrt(v30)
    num(3, I, 3, s30 / 100, math.sqrt(e) / 100,
        {'power-30': math.sqrt(VL + phi ** 30 * gap) / 100, 'variance': v30 / 100, 'no-long-run': math.sqrt(phi ** 29 * gap) / 100},
        0.007172, agree=1e-9, slip_tol=1e-8)
    s30r = F(7172, 10000)
    v1 = F(23263, 10000) * s30r / 100 * 8000000
    num(3, I, 4, v1, z99 * 0.7172 * 80000, {'part3-slip': F(23263, 10000) * F(7160, 10000) * 80000,
                                           'variance': F(23263, 10000) * F(5144, 10000) * 80000,
                                           'z95': F(16449, 10000) * s30r * 80000,
                                           'tomorrow': z99 * math.sqrt(0.69) * 80000}, 133474, slip_tol=0.01)
    ok(round(math.sqrt(VL + phi ** 30 * gap), 4) == 0.7160 and round(float(v30), 4) == 0.5144, 'L3 P1 slip inputs 0.7160 and 0.5144')
    tom = z99 * math.sqrt(0.69) * 80000
    said(lv, 0, 1, 'feedback.correct', [-0.014, -0.01302, 0.93])
    said(lv, 0, 2, 'feedback.correct', [0.2, 0.49])
    said(lv, 0, 2, 'explain.text', [0.7, round(math.sqrt(252 * 0.49), 2)])
    said(lv, 0, 3, 'feedback.correct', [round(float(phi ** 29 * gap), 4), round(float(v30), 4), round(s30, 4)])
    said(lv, 0, 3, 'explain.text', [0.7172])
    lv.claim(round(float(phi ** 29) * 100) == 12 and abs(s30 - 0.7) < 0.02, 'L3 P1 12% of the gap left; within 0.02 of 0.7%')
    said(lv, 0, 4, 'feedback.correct', ['133{,}474'])
    said(lv, 0, 4, 'explain.text', ['154,590', '133,474'])
    ok(round(tom) == 154590 and round(100 * (1 - float(v1) / tom)) == 14, 'L3 P1 tomorrow £154,590, a 14% fall')
    said(lv, 0, 4, 'feedback.byKey.tomorrow', [round(math.sqrt(0.69), 4)])
    said(lv, 0, 4, 'feedback.byKey.z95', ['94,378'])
    ok(round(1.6449 * 0.7172 * 80000) == 94378, 'L3 P1 z95 £94,378')
    said(lv, 0, 3, 'feedback.byKey.no-long-run', [0.0244, 0.49])
    ok(round(float(phi ** 29 * gap), 4) == 0.0244, 'L3 P1 faded gap 0.0244')

    # P2 a volatility-targeted fund's VaR is flat until the cap binds
    I = 'p-bank-index-flat-var'
    w_, a, b, s2, r = F(6, 100), F(6, 100), F(91, 100), F(225, 100), F(-4)
    nv = w_ + a * r * r + b * s2
    nv2 = float(np.dot([0.06, 0.06, 0.91], [1.0, 16.0, 2.25]))
    num(3, I, 1, math.sqrt(nv) / 100, math.sqrt(nv2) / 100,
        {'no-square': math.sqrt(w_ + a * r + b * s2) / 100, 'no-omega': math.sqrt(a * r * r + b * s2) / 100, 'variance': nv / 100},
        0.017514, slip_tol=1e-8)
    T, L, P = 11, 1.25, 15e6
    snr = 1.7514
    wt = T / (snr * S)
    num(3, I, 2, wt, T / math.sqrt(252 * snr ** 2), {'daily': min(T / snr, L), 'times-252': T / (snr * 252),
                                                     'from-today': T / (1.5 * S)}, 0.3956, slip_tol=1e-6)
    flat = z99 * T / S / 100 * P
    exact_w = T / (math.sqrt(nv) * S)
    num(3, I, 3, flat, z99 * exact_w * math.sqrt(nv) / 100 * P, {'no-weight': z99 * snr / 100 * P, 'z95': 1.6449 * 0.3956 * snr / 100 * P},
        241800, agree=1e-9, slip_tol=60)
    ok(abs(z99 * 0.3956 * snr / 100 * P - flat) < 120, 'L3 P2 the rounded w gives a figure inside the band')
    calm = 0.50                                     # fix pass (finding 22): a refitted model forecasting 0.50%
    wc = float(np.minimum(T / (calm * S), L))
    vc = z99 * wc * calm / 100 * P
    num(3, I, 4, vc, z99 * L * calm * P / 100, {'no-cap': z99 * (T / (calm * S)) * calm / 100 * P, 'cap-1': z99 * calm / 100 * P}, 218100,
        slip_tol=1.0)
    ok(0.06 / (1 - 0.91) > 0.5543 ** 2, 'L3 P2 the first GARCH floor 0.667 %2 (0.8165%) sits above the 0.5543% where the cap binds')
    said(lv, 1, 1, 'feedback.correct', [0.96, 2.0475, 3.0675, 1.7514])
    said(lv, 1, 1, 'explain.text', [0.96, round(float(w_ + b * s2), 4), 1.7514])
    lv.claim(round(100 * (math.sqrt(nv) / 1.5 - 1)) == 17, 'L3 P2 tomorrow 17% above 1.5%')
    said(lv, 1, 2, 'feedback.correct', [round(snr * S, 3), 0.3956])
    said(lv, 1, 2, 'explain.text', [39.56])
    said(lv, 1, 3, 'feedback.correct', ['241,800'])
    said(lv, 1, 3, 'explain.text', [round(T / S, 4), '241,800'])
    said(lv, 1, 4, 'feedback.correct', [round(calm * S, 2), round(T / (calm * S), 2), '218,091'])
    ok(round(vc) == 218091, 'L3 P2 calm VaR £218,091')
    said(lv, 1, 4, 'explain.text', [round(T / (L * S), 4), '218,091'])
    said(lv, 1, 4, 'feedback.byKey.no-cap', [1.39, '241,800'])
    said(lv, 1, 1, 'feedback.generic', [0.06, 16, 0.91, 2.25])
    said(lv, 1, 1, 'feedback.byKey.no-omega', [0.96, 2.0475])
    said(lv, 1, 2, 'feedback.byKey.daily', [6.28, 1.7514])
    said(lv, 1, 2, 'feedback.byKey.times-252', [441, 27.80])
    said(lv, 1, 3, 'feedback.byKey.z95', ['170,951'])
    ok(round(11 / 1.7514, 2) == 6.28 and round(1.7514 * 252) == 441 and round(1.6449 * 0.3956 * 0.017514 * P) == 170951,
       'L3 P2 slip lines 6.28, 441%, £170,951')

    # P3 Kupiec at 97.5%, then recalibrate the VaR and the ES
    I = 'p-recalibrate-short-var'
    ok(round(-stats.norm.ppf(0.025), 4) == 1.96 and round(stats.norm.ppf(0.9575), 4) == 1.7224
       and round(stats.norm.pdf(1.96), 6) == 0.058441, 'L3 P3 the three normal values in the prose')
    x, n = 17, 400

    def kup(xx, nn, p):
        ph = xx / nn
        return -2 * ((nn - xx) * math.log(1 - p) + xx * math.log(p) - (nn - xx) * math.log(1 - ph) - xx * math.log(ph))
    LR = kup(x, n, 0.025)
    LR2 = 2 * (stats.binom.logpmf(x, n, x / n) - stats.binom.logpmf(x, n, 0.025))   # binomial coefficient cancels
    num(3, I, 1, LR, LR2, {'at-0.01': kup(x, n, 0.01), 'half': LR / 2}, 4.168, agree=1e-9, slip_tol=1e-4)
    l0, l1 = 383 * math.log(0.975) + 17 * math.log(0.025), 383 * math.log(1 - 0.0425) + 17 * math.log(0.0425)
    said(lv, 2, 1, 'feedback.correct', [round(l0, 3), round(l1, 3), 0.0425, 4.168])
    said(lv, 2, 1, 'explain.text', [10, 17, 4.168, 3.841, round(1 - stats.chi2.cdf(LR, 1), 3)])
    said(lv, 2, 1, 'feedback.byKey.half', [2.084, 4.168])
    ok(round(LR / 2, 3) == 2.084, 'L3 P3 half of LR 2.084')
    ok(n * 0.025 == 10 and LR > 3.841, 'L3 P3 expected 10, rejected')
    c = F(19600, 10000) / F(17224, 10000)
    c2 = brentq(lambda cc: 1.96 / cc - 1.7224, 0.5, 2)
    num(3, I, 2, c, c2, {'inverted': 1 / c, 'rates': F(425, 10000) / F(25, 1000)}, 1.1379, agree=1e-9, slip_tol=1e-4)
    lv.claim(round(float(c - 1) * 100) == 14, 'L3 P3 c about 14% above 1')
    said(lv, 2, 2, 'feedback.correct', [1.7224, 1.1379])
    cr = 1.1379
    vn = 1.96 * cr * 1.15 / 100 * 3e6
    num(3, I, 3, vn, float(F(196, 100) * F(11379, 10000) * F(115, 100) * 30000),
        {'uncorrected': 1.96 * 1.15 * 30000, 'inverted': 1.96 * 1.15 / cr * 30000}, 76945, slip_tol=0.01)
    said(lv, 2, 3, 'feedback.correct', ['76,945', '67,620'])
    said(lv, 2, 3, 'explain.text', ['9,325', 14, '76,945'])
    ok(round(vn) - 67620 == 9325 and round(100 * (vn / 67620 - 1)) == 14, 'L3 P3 the fix adds £9,325, 14%')
    tail = integrate.quad(lambda zz: zz * stats.norm.pdf(zz), 1.96, 40)[0] / 0.025    # E[Z | Z > 1.96] by integration
    es = cr * 1.15 / 100 * 0.058441 / 0.025 * 3e6
    num(3, I, 4, es, cr * 1.15 / 100 * tail * 3e6, {'uncorrected': 1.15 / 100 * 0.058441 / 0.025 * 3e6,
                                                    'no-divide': cr * 1.15 / 100 * 0.058441 * 3e6}, 91770, agree=2e-5, slip_tol=0.01)
    said(lv, 2, 4, 'feedback.correct', ['91,770'])
    said(lv, 2, 4, 'feedback.byKey.no-divide', ['2,294', 0.025])
    ok(round(cr * 1.15 / 100 * 0.058441 * 3e6) == 2294, 'L3 P3 no-divide £2,294')
    cu = 1.96 / 1.7224                                  # fix pass (finding 26): c carried unrounded
    for jj, val in ((3, 1.96 * cu * 1.15 * 30000), (4, cu * 1.15 / 100 * 0.058441 / 0.025 * 3e6)):
        w_ = part(3, I, jj)['widget']
        ok(abs(round(val) - w_['answer']) <= w_['tol']['abs'], f'L3 P3 p{jj} unrounded c gives {round(val)}, accepted')
    said(lv, 2, 4, 'explain.text', ['91,770', round(0.058441 / 0.025, 4), 19])
    ok(round(100 * (0.058441 / 0.025 / 1.96 - 1)) == 19 and abs(0.058441 / 0.025 - z99) < 0.02, 'L3 P3 ES 19% beyond VaR, close to 2.3263')

    # P4 a monthly-reset sleeve sized from the month's summed forecasts (re-authored, replaces p-index-fund-back-in)
    I = 'p-monthly-sleeve'
    VLm, phm, s1m, Hm, Tm = F(81, 100), F(965, 1000), F(256, 100), 21, 9
    gm = s1m - VLm
    month = lambda k: sum(VLm + phm ** (h - 1) * gm for h in range(1 + k * Hm, 1 + (k + 1) * Hm))   # method 1: exact sum of days
    fm, Am = phm ** Hm, (1 - phm ** Hm) / (1 - phm)
    closed = lambda k: Hm * VLm + gm * fm ** k * Am                                                 # the geometric closed form
    ok(all(month(k) == closed(k) for k in range(4)), 'L3 P4 summed days equal the geometric closed form')
    e, tot = float(s1m), 0.0
    for _ in range(Hm):                                   # method 2: step the expected variance forward and add
        tot += e
        e = float((1 - phm) * VLm) + float(phm) * e
    num(3, I, 1, month(0), tot, {'flat': Hm * s1m, 'long-run': Hm * VLm, 'powers-from-one': Hm * VLm + gm * phm * Am,
                                 'decimal': month(0) / 10000}, 43.35, agree=1e-9, slip_tol=1e-4)
    mt = Tm / math.sqrt(12)
    num(3, I, 2, mt / math.sqrt(43.35), Tm / math.sqrt(43.35 * 252 / 21),
        {'monthly': Tm / math.sqrt(43.35), 'variance': mt / 43.35, 'flat-month': mt / math.sqrt(21 * 2.56),
         'times-252': Tm / math.sqrt(43.35 * 252)}, 0.3946, slip_tol=1e-5)
    ok(abs(mt / math.sqrt(float(month(0))) - part(3, I, 2)['widget']['answer']) < 6e-5, 'L3 P4 p2 the unrounded variance gives 0.3946 too')
    num(3, I, 3, month(1), 17.01 + float(fm) * (float(month(0)) - 17.01),
        {'one-step': 17.01 + 0.965 * 26.34, 'no-long-run': float(fm) * 43.35, 'power-20': 17.01 + 0.965 ** 20 * 26.34,
         'decimal': month(1) / 10000}, 29.47, agree=1e-9, slip_tol=3e-3)
    ok(abs(17.01 + float(fm) * 26.34 - part(3, I, 3)['widget']['answer']) < 6e-3, 'L3 P4 p3 the restated 43.35 gives 29.47 too')
    wk = [mt / math.sqrt(float(month(k))) for k in range(4)]
    ok(all(b > a for a, b in zip(wk, wk[1:])), 'L3 P4 the weights only rise')
    buys = sum(b - a for a, b in zip(wk, wk[1:]))
    w4r = mt / math.sqrt(17.01 + float(fm) ** 2 * (29.47 - 17.01))
    num(3, I, 4, wk[3] - wk[0], buys, {'last-weight': wk[3], 'two-resets': wk[2] - wk[0], 'long-run': mt / math.sqrt(21 * 0.81) - wk[0]},
        0.189, agree=1e-9, slip_tol=1e-4)
    ok(round(w4r - 0.3946, 3) == 0.189, 'L3 P4 p4 the restated 0.3946 and 29.47 give 0.189')
    said(lv, 3, 1, 'feedback.correct', [17.01, 1.75, 15.0505, 43.35])
    said(lv, 3, 1, 'explain.text', [26.34, 17.01, 43.35])
    said(lv, 3, 1, 'feedback.byKey.flat', [53.76, 2.56])
    said(lv, 3, 2, 'feedback.correct', [2.598, 6.584, 0.3946])
    said(lv, 3, 2, 'feedback.byKey.monthly', [1.367])
    said(lv, 3, 2, 'feedback.byKey.flat-month', [0.3543, 53.76])
    said(lv, 3, 2, 'explain.text', [6.584, 2.598, 0.3946, 61, 0.3543])
    said(lv, 3, 3, 'feedback.correct', [26.34, 0.4732, 29.47])
    said(lv, 3, 3, 'explain.text', [17.01, 47, 43.35, 29.47])
    said(lv, 3, 4, 'feedback.correct', [0.2239, 12.46, 19.80, 0.5839, 0.189])
    said(lv, 3, 4, 'explain.text', [0.0839, 0.0643, 0.0410, 0.189, 0.630])
    said(lv, 3, 4, 'feedback.byKey.long-run', [0.630])
    lv.claim(abs(float(Am) - 15.0505) < 5e-5 and abs(float(gm * Am) - 26.34) < 5e-3 and abs(float(fm) - 0.4732) < 5e-5
             and abs(float(fm) ** 2 - 0.2239) < 5e-5, 'L3 P4 15.0505, 26.34, 0.4732, 0.2239')
    lv.claim(abs(mt - 2.598) < 5e-4 and abs(math.sqrt(43.35) - 6.584) < 5e-4 and round(100 * (1 - 0.3946)) == 61
             and abs(float(month(3)) - 19.80) < 5e-3 and abs(29.47 - 17.01 - 12.46) < 1e-9, 'L3 P4 2.598, 6.584, 61% cash, 19.80, 12.46')
    lv.claim(round(float(fm) * 100) == 47 and abs((wk[3] - wk[0]) / (mt / math.sqrt(17.01) - wk[0]) - 0.8) < 0.02,
             'L3 P4 47% kept a month; four fifths of the way to 0.630')
    lv.claim(all(abs(x - y) < 5e-5 for x, y in zip([b - a for a, b in zip(wk, wk[1:])], [0.0839, 0.0643, 0.0410])), 'L3 P4 buys 0.0839, 0.0643, 0.0410')
    lv.check_wrongs('problems')
    lv.report()


if SETS[1]:
    level1()
if SETS[2]:
    level2()
if SETS[3]:
    level3()
print(f'{checks - len(fails)} of {checks} direct checks passed')
sys.exit(1 if fails else 0)
