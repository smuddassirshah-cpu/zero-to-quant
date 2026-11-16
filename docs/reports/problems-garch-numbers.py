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
    t = om3 + F(9, 100) * F(2025, 100) + F(87, 100) * vbar
    num(2, I, 4, math.sqrt(t) / 100, float(np.sqrt(0.1156 + 0.09 * 4.5 ** 2 + 0.87 * 2.89)) / 100,
        {'variance': t / 100, 'no-square': math.sqrt(om3 + F(9, 100) * F(45, 10) + F(87, 100) * vbar) / 100,
         'annual': math.sqrt(252 * t) / 100}, 0.0211, slip_tol=6e-6)
    said(lv, 2, 4, 'feedback.correct', [1.8225, 2.5143, 4.4524, 2.11])
    lv.claim(abs(math.sqrt(t) / math.sqrt(2.89) - 1.24) < 5e-3, 'L2 P3 tomorrow 24% above the long-run 1.70%')
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
    q = F(1, 4)
    e2 = lam4 * e1 + (1 - lam4) * q
    num(2, I, 3, e2, q + lam4 * (e1 - q), {'no-news': lam4 * e1, 'abs': lam4 * e1 + (1 - lam4) * F(1, 2), 'decimal': e2 / 10000}, 2.8145, slip_tol=1e-4)
    floor = F(8, 10) + F(45, 100) * q
    ev, kk = float(e1), 0
    while ev >= float(floor):
        ev, kk = 0.95 * ev + 0.05 * 0.25, kk + 1
    kf = math.log(float((floor - q) / (e1 - q))) / math.log(0.95)
    num(2, I, 4, math.ceil(kf), kk, {'round-down': kk - 1, 'no-floor': math.ceil(math.log(float(floor / e1)) / math.log(0.95))}, 28)
    said(lv, 3, 1, 'feedback.correct', [1.1495, 1.8, 2.9495])
    said(lv, 3, 2, 'feedback.correct', ['5.764', 2.40])
    said(lv, 3, 3, 'feedback.correct', [2.8020, 0.0125, 2.8145])
    said(lv, 3, 3, 'explain.text', [0.0125, 2.8145, 0.9125])
    said(lv, 3, 4, 'feedback.correct', [0.2454, 27.4, 28])
    lv.claim(abs(0.25 + 0.95 ** 27 * 2.6995 - 0.93) < 5e-3, 'L2 P4 after 27 days about 0.93')
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
    calm = 0.48
    wc = float(np.minimum(T / (calm * S), L))
    vc = z99 * wc * calm / 100 * P
    num(3, I, 4, vc, z99 * L * calm * P / 100, {'no-cap': z99 * (T / (calm * S)) * calm / 100 * P, 'cap-1': z99 * calm / 100 * P}, 209400,
        slip_tol=1.0)
    said(lv, 1, 1, 'feedback.correct', [0.96, 2.0475, 3.0675, 1.7514])
    said(lv, 1, 1, 'explain.text', [0.96, round(float(w_ + b * s2), 4), 1.7514])
    lv.claim(round(100 * (math.sqrt(nv) / 1.5 - 1)) == 17, 'L3 P2 tomorrow 17% above 1.5%')
    said(lv, 1, 2, 'feedback.correct', [round(snr * S, 3), 0.3956])
    said(lv, 1, 2, 'explain.text', [39.56])
    said(lv, 1, 3, 'feedback.correct', ['241,800'])
    said(lv, 1, 3, 'explain.text', [round(T / S, 4), '241,800'])
    said(lv, 1, 4, 'feedback.correct', [round(calm * S, 2), round(T / (calm * S), 2), '209,367'])
    ok(round(vc) == 209367, 'L3 P2 calm VaR £209,367')
    said(lv, 1, 4, 'explain.text', [round(T / (L * S), 4), '209,367'])

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
    said(lv, 2, 1, 'explain.text', [10, 17, 4.168, round(1 - stats.chi2.cdf(LR, 1), 3)])
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
    said(lv, 2, 4, 'explain.text', ['91,770', round(0.058441 / 0.025, 4), 19])
    ok(round(100 * (0.058441 / 0.025 / 1.96 - 1)) == 19 and abs(0.058441 / 0.025 - z99) < 0.02, 'L3 P3 ES 19% beyond VaR, close to 2.3263')

    # P4 an unlevered fund buys back in as a storm fades
    I = 'p-index-fund-back-in'
    VL4, ph4, s1, T4 = 0.64, 0.977, 4.0, 14
    Td = T4 / S
    w1 = min(Td / math.sqrt(s1), 1)
    num(3, I, 1, w1, T4 / (2 * S), {'daily': min(T4 / 2, 1), 'variance': T4 / (s1 * S)}, 0.4410, slip_tol=1e-6)
    v20 = VL4 + ph4 ** 19 * (s1 - VL4)
    e = s1
    for _ in range(19):
        e = (1 - ph4) * VL4 + ph4 * e
    num(3, I, 2, math.sqrt(v20) / 100, math.sqrt(e) / 100,
        {'power-20': math.sqrt(VL4 + ph4 ** 20 * (s1 - VL4)) / 100, 'variance': v20 / 100, 'no-long-run': math.sqrt(ph4 ** 19 * (s1 - VL4)) / 100},
        0.016731, slip_tol=1e-8)
    w20 = 0.88192 / 1.6731
    path = [min(Td / math.sqrt(VL4 + ph4 ** (h - 1) * (s1 - VL4)), 1) for h in range(1, 21)]
    turn = sum(abs(p2 - p1) for p1, p2 in zip(path, path[1:]))     # daily changes summed
    num(3, I, 3, w20 - w1, turn, {'day-20-weight': w20, 'sum': w20 + w1, 'part2-slip': 0.88192 / 1.6582 - 0.4410}, 0.086,
        agree=2e-4, slip_tol=1e-4)
    ok(abs(Td ** 2 - 7 / 9) < 1e-12, 'L3 P4 the daily target variance is 7/9')
    hm1 = math.log((Td ** 2 - VL4) / (s1 - VL4)) / math.log(ph4)
    h = 1
    while VL4 + ph4 ** (h - 1) * (s1 - VL4) > Td ** 2:
        h += 1
    hn = 1
    while ph4 ** (hn - 1) * s1 > Td ** 2:
        hn += 1
    hv = 1
    while 0.8 + ph4 ** (hv - 1) * (2 - 0.8) > Td:
        hv += 1
    num(3, I, 4, math.ceil(hm1) + 1, h, {'h-minus-1': h - 1, 'no-long-run': hn, 'vol-gap': hv}, 139)
    said(lv, 3, 1, 'feedback.correct', [2, round(2 * S, 2), 31.749, 0.4410])
    said(lv, 3, 1, 'explain.text', [round(Td, 4), 0.88192, 0.4410])
    ok(round(Td, 5) == 0.88192 and round(T4 / 31.749, 4) == 0.4410, 'L3 P4 0.88192 and 14/31.749')
    said(lv, 3, 2, 'feedback.correct', [round(ph4 ** 19 * 3.36, 4), round(v20, 4), round(math.sqrt(v20), 4)])
    said(lv, 3, 2, 'explain.text', [round(100 * ph4 ** 19), 1.6731, 0.8])
    said(lv, 3, 3, 'feedback.correct', [round(w20, 4), 0.0861])
    said(lv, 3, 3, 'explain.text', [0.086, round((w20 - w1) * 0.0005 * 100, 4)])
    said(lv, 3, 4, 'feedback.correct', [round(7 / 9 - 0.64, 4), round((7 / 9 - 0.64) / 3.36, 5), round(hm1, 2), 139])
    said(lv, 3, 4, 'explain.text', [139, round(0.8 * S, 2)])
    lv.claim(6.3 < 139 / 21 < 6.9, 'L3 P4 139 trading days is about six and a half months')
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
