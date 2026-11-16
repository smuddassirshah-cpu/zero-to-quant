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

    # P1 two regimes
    I = 'p-two-regime-tails'
    pq, pt_ = F(99, 100), F(96, 100)
    Lq = 1 / (1 - pq)
    Lq2 = sum(k * 0.01 * 0.99 ** (k - 1) for k in range(1, 20000))       # geometric mean as a series
    num(1, I, 1, Lq, Lq2, {'stay': 99, 'turbulent': 1 / (1 - pt_)}, 100, agree=1e-6)
    Lt = 1 / (1 - pt_)
    w = Lt / (Lq + Lt)
    P = np.array([[0.99, 0.01], [0.04, 0.96]])
    ev, evec = np.linalg.eig(P.T)
    pi = np.real(evec[:, np.argmin(abs(ev - 1))]); pi = pi / pi.sum()
    num(1, I, 2, w, pi[1], {'ratio': Lt / Lq, 'quiet': 1 - w, 'leave': 1 - pt_}, 0.2)
    sq, st = F(6, 10), F(18, 10)
    var = (1 - w) * sq ** 2 + w * st ** 2
    dens = lambda x: float(1 - w) * stats.norm.pdf(x, 0, 0.6) + float(w) * stats.norm.pdf(x, 0, 1.8)
    var2 = integrate.quad(lambda x: x * x * dens(x), -40, 40)[0]
    ann = math.sqrt(252 * var) / 100
    w25 = F(1, 4)
    num(1, I, 3, ann, math.sqrt(252 * var2) / 100,
        {'mix-sd': math.sqrt(252) * float((1 - w) * sq + w * st) / 100,
         'share-25': math.sqrt(252 * ((1 - w25) * sq ** 2 + w25 * st ** 2)) / 100,
         'swapped': math.sqrt(252 * (w * sq ** 2 + (1 - w) * st ** 2)) / 100},
        0.1536, agree=1e-7, slip_tol=6e-6)
    m4 = 3 * ((1 - w) * sq ** 4 + w * st ** 4)
    m4b = integrate.quad(lambda x: x ** 4 * dens(x), -40, 40)[0]
    ex = m4 / var ** 2 - 3
    m4_25 = 3 * ((1 - w25) * sq ** 4 + w25 * st ** 4)
    v25 = (1 - w25) * sq ** 2 + w25 * st ** 2
    num(1, I, 4, ex, m4b / var2 ** 2 - 3,
        {'raw': ex + 3, 'share-25': m4_25 / v25 ** 2 - 3, 'no-three': m4 / 3 / var ** 2 - 3, 'normal': 0},
        4.54, agree=1e-6, slip_tol=1e-4)
    ok(var == F(117, 125) and m4 == F(66096, 10000), 'L1 P1 exact moments 0.936 and 6.6096')
    said(lv, 0, 3, 'feedback.correct', [0.288, 0.648, 0.936, 0.9675, 15.36])
    said(lv, 0, 4, 'feedback.correct', [2.2032, 6.6096, 0.8761, 7.544, 4.54])
    said(lv, 0, 4, 'explain.text', [0.1296, 10.4976, 6.6096, 7.54, 4.54])
    lv.claim(abs(float(sq ** 4) - 0.1296) < 1e-12 and abs(float(st ** 4) - 10.4976) < 1e-12, 'L1 P1 fourth powers 0.1296 and 10.4976')
    lv.claim(abs(math.sqrt(0.936) - 0.9675) < 5e-5 and abs(math.sqrt(252) * 0.9675 - 15.36) < 0.005, 'L1 P1 sqrt(252) x 0.9675 = 15.36')
    lv.claim(abs(0.936 ** 2 - 0.8761) < 5e-5 and abs(6.6096 / 0.876096 - 7.544) < 5e-4, 'L1 P1 6.6096 / 0.8761 = 7.544')

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
    said(lv, 1, 4, 'feedback.correct', [1.113])
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
    num(1, I, 3, math.sqrt(252 * s2) / 100, math.sqrt(252) * float(np.std(xa, ddof=1)) / 100,
        {'zero-mean': math.sqrt(252 * ms) / 100, 'calendar': math.sqrt(365 * s2) / 100}, 0.2833, slip_tol=6e-6)
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
    said(lv, 2, 3, 'feedback.correct', [15.87, 1.785, 28.33])
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
    said(lv, 3, 4, 'feedback.byKey.round-down', [0.0933, 0.0456, 3.12])
    said(lv, 3, 3, 'feedback.correct', [0.04, 59.96, 3.84])
    lv.claim(abs(thr - 0.0981) < 5e-5 and abs(thr * 75 - 7.36) < 0.005, 'L1 P4 threshold q 0.0981, 7.36 days')
    lv.claim(abs(math.sqrt(3.841 / 1499) - 1.96 / math.sqrt(1500)) < 1e-4, 'L1 P4 threshold close to the band')
    c7 = (F(7, 75) - p) / (1 - p)
    lv.claim(abs(float(c7) - 0.0456) < 5e-5 and abs(1499 * float(c7) ** 2 - 3.12) < 0.005, 'L1 P4 seven days give LM 3.12')
    lv.check_wrongs('problems')
    lv.report()


if SETS[1]:
    level1()
print(f'{checks - len(fails)} of {checks} direct checks passed')
sys.exit(1 if fails else 0)
