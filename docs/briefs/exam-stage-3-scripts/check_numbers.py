"""Recompute every number stated in app/content/exams/stage-3.json by a second route and assert it at its path.

Route A is build.py (closed forms and Fractions). Route B here is independent: full enumeration of dice, cards and the
hidden number, linear solves of Markov chains, truncated series, grid searches for the game and the auction, Simpson
integration, exact binomial sums, seeded simulation beside the normal tails, bisection, and a second implementation of
the point-in-time join. The code solution runs against its hidden tests and the starter must fail one. A last pass reads
every number in every learner-visible string of each item: whole numbers 0 to 10 count as structure, every other number
must match a route-B or given value for that item to its printed precision. Exits 1 on any failure.
Run: python3 docs/briefs/exam-stage-3-scripts/check_numbers.py
"""
import glob
import itertools
import json
import math
import os
import re
import sys
from fractions import Fraction as F
from statistics import NormalDist

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'stage-3.json')
CDIR = os.path.join(ROOT, 'app', 'content')
N01 = NormalDist()
RNG = np.random.default_rng(20261106)


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
PATH, ITEM, PAPER = {}, {}, {}
for pi, p in enumerate(doc['parts']):
    for j, it in enumerate(p.get('items', [])):
        if 'id' in it:
            PATH[it['id']] = f'parts[{pi}].items[{j}]'
            ITEM[it['id']] = it
            PAPER[it['id']] = p['id']
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def W(iid, part=None):
    it = ITEM[iid]
    return it['widget'] if part is None else it['parts'][part]['widget']


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, '' if ok else note)


def key(iid, value, part=None):
    w = W(iid, part)
    t = max(w['tol']['abs'] / 10, 1e-9) if w['tol']['abs'] else 1e-9
    rec(abs(w['answer'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', 'route B differs')
    allow(iid, value)
    if w.get('unit') == '%':
        allow(iid, value * 100)


def wrong(iid, wid, value, part=None):
    w = W(iid, part)
    hit = [x for x in w['wrong'] if x['id'] == wid]
    t = max(hit[0]['tol']['abs'] / 10, 1e-9) if hit and hit[0]['tol']['abs'] else 1e-9
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} wrong "{wid}" = {value!r}', f'found {hit}')
    allow(iid, value)
    if w.get('unit') == '%':
        allow(iid, value * 100)


def correct_ids(iid, want, part=None):
    w = W(iid, part)
    got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    rec(got == sorted(want), f'{iid} correct options {got} = {sorted(want)}')
    rec(w.get('shuffle') is True, f'{iid} shuffle true')
    rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} every distractor has a why')
    lens = [len(o['text']) for o in w['options']]
    key_len = max(len(o['text']) for o in w['options'] if o.get('correct'))
    others = [len(o['text']) for o in w['options'] if not o.get('correct')]
    rec(key_len <= 1.5 * max(others), f'{iid} no key far longer than its distractors ({key_len} against at most {max(others)})', str(lens))


def simpson(f, a, b, m=20000):
    h = (b - a) / m
    return h / 3 * (f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, m)))


def bisect(f, lo, hi, it=200):
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(lo) > 0) == (f(mid) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


DICE = list(itertools.product(range(1, 7), repeat=2))

# ======================================================================== Paper A
# A1: enumerate the 36 rolls
even_prod = [d for d in DICE if (d[0] * d[1]) % 2 == 0]
both = [d for d in even_prod if (d[0] + d[1]) % 2 == 0]
key('a-even-product', len(both) / len(even_prod))
wrong('a-even-product', 'ignored-news', sum((a + b) % 2 == 0 for a, b in DICE) / 36)
wrong('a-even-product', 'whole-table', len(both) / 36)
allow('a-even-product', len(even_prod), len(both), 36, 1 / 3, 0.0005)
rec(len(even_prod) == 27 and len(both) == 9, 'a-even-product: 27 rolls with an even product, 9 with an even sum')

# A2: the truncated series sum of n P(stop at roll n)
e2 = sum(n * (5 / 6) ** (n - 2) * (1 / 6) for n in range(2, 2000))
key('a-repeat-roll', round(e2, 9))
wrong('a-repeat-roll', 'no-first', round(e2 - 1, 9))
wrong('a-repeat-roll', 'one-pair', 36)

# A3: a Markov chain on Ana's lead, -2 to 2
P = np.zeros((5, 5))
for i in (1, 2, 3):
    P[i, i + 1], P[i, i - 1] = 0.6, 0.4
P[0, 0] = P[4, 4] = 1
Q = P[1:4, 1:4]
Nf = np.linalg.inv(np.eye(3) - Q)
win = (Nf @ P[1:4, 4])[1]
dur = (Nf @ np.ones(3))[1]
key('a-lead-by-two', round(float(win), 9), 0)
key('a-lead-by-two', round(float(dur), 9), 1)
wrong('a-lead-by-two', 'one-point', 0.6, 0)
wrong('a-lead-by-two', 'two-straight', 0.6 * 0.6, 0)
wrong('a-lead-by-two', 'two-points', 2, 1)
wrong('a-lead-by-two', 'pairs-not-points', round(float(dur) / 2, 9), 1)
allow('a-lead-by-two', 0.6 ** 2 + 0.4 ** 2, 0.4 ** 2, 1 - (0.6 ** 2 + 0.4 ** 2), 0.6, 0.4)

# A4: every seating of ten labelled traders round a table, up to rotation (9! orders of the other nine)
adj = tot = 0
for perm in itertools.permutations(range(1, 10)):
    seats = (0,) + perm                           # head 0 in seat 0; head 1 is wherever 1 sits
    k = seats.index(1)
    tot += 1
    adj += k in (1, 9)
p4 = F(adj, tot)
rec(p4 == F(2, 9), f'a-round-table: {adj} of {tot} seatings put the heads side by side, {p4}')
correct_ids('a-round-table', ['a'])
rec(F(2, 10) == F(1, 5) and F(1, 9) == F(1, 9) and F(1, math.comb(10, 2)) == F(1, 45),
    'a-round-table: the distractors are 2/10, one seat of 9 and one pair of seats among 45')
allow('a-round-table', 1 / p4, 2, 9, 10, 45, 5)

# A5: Simpson on the area under min(1, 1/(2x))
a5 = simpson(lambda x: min(1.0, 1 / (2 * x)) if x > 0 else 1.0, 0, 1)
key('a-uniform-product', round(a5, 7))
wrong('a-uniform-product', 'uniform-product', 0.5)
wrong('a-uniform-product', 'curve-only', round(simpson(lambda x: 1 / (2 * x), 0.5, 1), 7))
allow('a-uniform-product', 0.5)

# A6: a grid search for her maximin mix
M = np.array([[2, -1], [-3, 4]])
ps = np.linspace(0, 1, 100001)
guar = np.minimum(ps * M[0, 0] + (1 - ps) * M[1, 0], ps * M[0, 1] + (1 - ps) * M[1, 1])
p6, v6 = float(ps[guar.argmax()]), float(guar.max())
key('a-quote-game', round(p6, 4), 0)
key('a-quote-game', round(v6, 4), 1)
qs = np.linspace(0, 1, 100001)
row_gap = np.abs((qs * M[0, 0] + (1 - qs) * M[0, 1]) - (qs * M[1, 0] + (1 - qs) * M[1, 1]))
wrong('a-quote-game', 'his-mix', round(float(qs[row_gap.argmin()]), 4), 0)
wrong('a-quote-game', 'pure-tight', 1, 0)
wrong('a-quote-game', 'pure-maximin', float(M.min(axis=1).max()), 1)
wrong('a-quote-game', 'half-half', float(min(0.5 * M[0, 0] + 0.5 * M[1, 0], 0.5 * M[0, 1] + 0.5 * M[1, 1])), 1)
allow('a-quote-game', 2, -1, -3, 4, 0.3, -0.5, 0.50, 10, 7)

# A7: count Ben's high totals, then sum the series over rounds
hi = sum(a + b >= 9 for a, b in DICE)
rec(hi == 10, f'a-six-or-nine: {hi} of 36 rolls total 9 or more')
a7 = sum((5 / 6 * (36 - hi) / 36) ** k * (1 / 6) for k in range(400))
key('a-six-or-nine', round(a7, 9))
wrong('a-six-or-nine', 'six-each', round(sum((25 / 36) ** k * (1 / 6) for k in range(400)), 9))
wrong('a-six-or-nine', 'at-once', round((1 / 6) / (1 / 6 + hi / 36), 9))
rec(F(5, 6) * F(36 - hi, 36) == F(65, 108) and F(1, 6) / (1 - F(65, 108)) == F(18, 43), 'a-six-or-nine: 65/108 per round, 18/43 for Ana')
allow('a-six-or-nine', hi, 36, 26, 65, 108, 18, 43, 9)

# A8: the truncated sum over wins k before the third loss (negative binomial)
e8 = sum(k * math.comb(k + 2, 2) * 0.6 ** k * 0.4 ** 3 for k in range(0, 400))
key('a-third-loss', round(e8, 9))
wrong('a-third-loss', 'all-bets', round(e8 + 3, 9))
wrong('a-third-loss', 'first-loss', round(sum(k * 0.6 ** k * 0.4 for k in range(400)), 9))
allow('a-third-loss', 0.6, 0.4, 1.5)

# A9: best response by grid search against a rival on b(v) = v^2 / 2
bids = np.linspace(0, 0.5, 500001)
pay = 0.8 * np.sqrt(2 * bids) - bids            # P(win) = P(V^2 / 2 < b) = sqrt(2b)
b9 = float(bids[pay.argmax()])
key('a-all-pay', round(b9, 4))
wrong('a-all-pay', 'first-price', 0.8 / 2)
wrong('a-all-pay', 'truthful', 0.8)
allow('a-all-pay', 0.8, 1, 0.32)

# A10: exact binomial sums and the normal curve
pmf = [math.comb(100, k) * F(55, 100) ** k * F(45, 100) ** (100 - k) for k in range(101)]
down = float(sum(pmf[:50]))
key('a-edge-hundred', round(down, 4))
wrong('a-edge-hundred', 'sure-profit', 0)
sd = math.sqrt(100 * 0.55 * 0.45)
wrong('a-edge-hundred', 'no-half', round(N01.cdf((50 - 55) / sd), 4))
wrong('a-edge-hundred', 'level-counts', round(float(sum(pmf[:51])), 4))
rec(abs(N01.cdf((49.5 - 55) / sd) - 0.13) < 0.005 and round((49.5 - 55) / sd, 2) == -1.11, 'a-edge-hundred: Phi(-1.11) is about 0.13')
allow('a-edge-hundred', 100, 0.55, 0.45, 55, 49, 50, 49.5, -1.11, 0.13, sd, down, 1, 10)

# A11: Fractions over the four kinds of day
b, h, fl = F(2, 100), F(9, 10), F(5, 100)
w_break, w_norm = b * h * h, (1 - b) * fl * fl
key('a-two-flags', round(float(w_break / (w_break + w_norm)), 9))
wrong('a-two-flags', 'one-model', round(float(b * h / (b * h + (1 - b) * fl)), 9))
wrong('a-two-flags', 'hits-squared-only', round(float(w_break / (w_break + (1 - b) * fl)), 9))
allow('a-two-flags', 0.02, 0.9, 0.05, 0.98, float(w_break), float(w_norm), float(w_break + w_norm), 90, 5, 2)

# A12: enumerate X and the trader's type
pbuy = F(0)
num = F(0)
for x in range(1, 101):
    for informed, pw in ((True, F(1, 2)), (False, F(1, 2))):
        pb = (F(1) if x > 55 else F(0)) if informed else F(1, 2)
        pbuy += F(1, 100) * pw * pb
        num += F(1, 100) * pw * pb * x
post = num / pbuy
key('a-informed-buyer', round(float(pbuy), 9), 0)
key('a-informed-buyer', round(float(post), 9), 1)
key('a-informed-buyer', round(float(55 - post), 9), 2)
wrong('a-informed-buyer', 'noise-only', 0.5, 0)
inf_buy = F(sum(1 for x in range(1, 101) if x > 55), 100)
wrong('a-informed-buyer', 'informed-only', float(inf_buy), 0)
m_inf = F(sum(x for x in range(56, 101)), 45)
m_all = F(sum(range(1, 101)), 100)
wrong('a-informed-buyer', 'all-informed', float(m_inf), 1)
wrong('a-informed-buyer', 'no-update', float(m_all), 1)
wrong('a-informed-buyer', 'equal-weights', round(float((m_all + m_inf) / 2), 9), 1)
wrong('a-informed-buyer', 'sign', round(float(post - 55), 9), 2)
wrong('a-informed-buyer', 'prior-value', float(55 - m_all), 2)
allow('a-informed-buyer', 100, 45, 55, 0.25, 0.225, 0.45, 0.5, 0.475, float(m_all), float(m_inf), float(post - 55))

# ======================================================================== Paper C
correct_ids('r-backfill', ['a'])
correct_ids('r-same-month', ['a'])
allow('r-same-month', 6, 12, -1, 1)

alive, dead = [F(9)] * 160, [F(-15)] * 40
true_mean = sum(alive + dead) / 200
key('r-closed-funds', float(F(9) - true_mean))
wrong('r-closed-funds', 'true-mean', float(true_mean))
wrong('r-closed-funds', 'equal-groups', float(F(9) - (F(9) + F(-15)) / 2))
allow('r-closed-funds', 200, 40, 160, -15, 9, 0.8, 0.2, float(true_mean))

correct_ids('r-june-book', ['a'])
allow('r-june-book', 1993, 2014, 2015, 2016, 1)
correct_ids('r-which-leak', ['a', 'b', 'c'])
allow('r-which-leak', 2009, 2010, 1990, 2024, 2008)
w6 = W('r-pairs-oos-order')
rec(w6['answer'] == ['p1', 'p2', 'p3', 'p4', 'p5'] and w6['distractors'] == ['x1', 'x2'], 'r-pairs-oos-order: five steps, two left out')
rec(all(ln.get('why') for ln in w6['lines'] if ln['id'] in w6['distractors']), 'r-pairs-oos-order: each flawed line has a why')
bk6 = ITEM['r-pairs-oos-order']['feedback']['byKey']
rec(all(d in bk6 for d in w6['distractors']) and 'left-out' in bk6, 'r-pairs-oos-order: byKey names each flawed line and left-out')
allow('r-pairs-oos-order', 2006, 2002, 2003, 2024, 12, 6, 2)

c7 = F(11, 1000) / F(14, 10)
key('r-turnover-cost', round(float(c7), 9))
wrong('r-turnover-cost', 'twice', round(float(F(11, 1000) / F(28, 10)), 9))
wrong('r-turnover-cost', 'no-turnover', 0.011)
allow('r-turnover-cost', 1.1, 1.4, 1.40, 0.79, round(float(c7) * 100, 2))

se8 = 3.1 / math.sqrt(360)
t8 = 0.45 * math.sqrt(360) / 3.1
key('r-t-bar', round(t8, 6), 0)
wrong('r-t-bar', 'no-root', round(0.45 / 3.1, 6), 0)
wrong('r-t-bar', 'years', round(0.45 * math.sqrt(30) / 3.1, 6), 0)
correct_ids('r-t-bar', ['a'], 1)
allow('r-t-bar', 0.45, 3.1, 360, se8, 2.75, 2016)

caps = np.array([5.0] * 9 + [0.05])
rr = np.array([0.01] * 9 + [0.60])
ew = float(np.mean(rr))
vw = float(np.average(rr, weights=caps))
key('r-small-share', round(ew, 9), 0)
key('r-small-share', round(vw, 9), 1)
wrong('r-small-share', 'big-only', 0.01, 0)
wrong('r-small-share', 'value-weighted', round(vw, 9), 0)
wrong('r-small-share', 'equal-weighted', round(ew, 9), 1)
wrong('r-small-share', 'big-only', 0.01, 1)
allow('r-small-share', 5, 1, 0.05, 60, 0.60, 45, 45.05, 9, ew * 100, vw * 100)

correct_ids('r-note-sentence', ['a'])
rec(F(21, 84) == F(1, 4), 'r-note-sentence: 0.21 / 0.84 is a quarter')
allow('r-note-sentence', 0.84, 3.2, 15, 0.21, 0.7, 0.25, 25, 1)

a12 = F(90, 10000) - F(35, 100) * F(140, 10000)
key('r-factor-alpha', round(float(a12), 9))
wrong('r-factor-alpha', 'whole-factor', round(float(F(90, 10000) - F(140, 10000)), 9))
wrong('r-factor-alpha', 'scaled-own', round(float(F(90, 10000) * (1 - F(35, 100))), 9))
rec(abs(float((F(35, 100) * F(140, 10000)) / F(90, 10000)) - 0.544) < 0.001, 'r-factor-alpha: the factor explains a little over half, 0.544')
allow('r-factor-alpha', 0.90, 0.35, 1.40, 0.49, 0.41)

# C11: simulation beside the normal tail
draws = RNG.standard_normal((400000, 20)) / math.sqrt(5)
sim11 = float((draws.max(axis=1) > 1).mean())
p11 = 1 - N01.cdf(math.sqrt(5))
exact11 = 1 - (1 - p11) ** 20
rec(abs(sim11 - exact11) < 0.003, f'r-best-of-twenty: simulation {sim11:.4f} agrees with {exact11:.4f}')
key('r-best-of-twenty', round(exact11, 6))
rec(abs(float((draws > 1).mean()) - p11) < 0.0005, 'r-best-of-twenty: one simulated variant beats 1 at the normal tail rate')
wrong('r-best-of-twenty', 'one-variant', round(p11, 6))
wrong('r-best-of-twenty', 'added-chances', round(20 * p11, 6))
allow('r-best-of-twenty', 20, 5, 1, p11, (1 - p11) ** 20, exact11)

# C16: the counts by the normal tails, and a simulation of the passes
tn2, tr2 = 200 * (1 - N01.cdf(2)), 100 * N01.cdf(1.5)
tn3, tr3 = 200 * (1 - N01.cdf(3)), 100 * N01.cdf(0.5)
key('r-false-share', round(tn2 / (tn2 + tr2), 7), 0)
key('r-false-share', round(tn3 / (tn3 + tr3), 7), 1)
tsim = np.concatenate([RNG.standard_normal((20000, 200)), 3.5 + RNG.standard_normal((20000, 100))], axis=1)
fs2 = (tsim[:, :200] > 2).sum() / (tsim > 2).sum()
rec(abs(fs2 - tn2 / (tn2 + tr2)) < 0.002, f'r-false-share: simulated false share at 2 is {fs2:.4f}')
wrong('r-false-share', 'over-tested', round(tn2 / 300, 7), 0)
wrong('r-false-share', 'null-rate', round(1 - N01.cdf(2), 7), 0)
wrong('r-false-share', 'null-rate', round(1 - N01.cdf(3), 7), 1)
wrong('r-false-share', 'over-tested', round(tn3 / 300, 7), 1)
rec(abs(tr3 / tr2 - 0.741) < 0.001, f'r-false-share: the bar of 3 keeps {tr3 / tr2:.3f} of the real passes, so costs about a quarter')
allow('r-false-share', 300, 200, 100, 3.5, 1.5, tn2, tr2, tn3, tr3, 1 - N01.cdf(2))

# C13: the solution and starter against the tests, and a second implementation by sorting


def as_of_b(reports, date):
    out = {}
    for t, pe, pub, v in sorted((r for r in reports if r[2] <= date), key=lambda r: (r[0], r[1], r[2])):
        out[t] = v
    return out


def run_py(src, tests):
    passed = 0
    for t in tests:
        ns = {'__learner_source__': src}
        try:
            exec(src, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            ok = got == eval(t['expect'], {})
        except Exception:
            ok = False
        passed += bool(ok)
    return passed


w13 = W('r-as-of-code')
n13 = len(w13['tests'])
rec(run_py(w13['solution'], w13['tests']) == n13, f'r-as-of-code: the solution passes all {n13} tests')
rec(run_py(w13['starter'], w13['tests']) < n13, 'r-as-of-code: the starter fails a test')
b_src = 'def as_of(reports, date):\n    return AS_OF_B(reports, date)\n'
ok13 = 0
for t in w13['tests']:
    ns = {'AS_OF_B': as_of_b}
    exec(b_src, ns)
    exec(t['setup'], ns)
    ok13 += eval(t['call'], ns) == eval(t['expect'], {})
rec(ok13 == n13, f'r-as-of-code: the sorting route gives every expected dict ({ok13} of {n13})')
rec(all(e['expect'] in [t['expect'] for t in w13['tests']] for e in w13['examples']), 'r-as-of-code: the example is a hidden test')
rec(f'{n13} hidden tests' in w13['how'], f'r-as-of-code: how states {n13} tests')
allow('r-as-of-code', 2015, 3, 20, 31, 2, 7)

# C15: the expected t, its tail by simulation, the months by bisection
mean_t = lambda months: 0.5 * 4.0 * math.sqrt(months / 240)
c15a = mean_t(120)
key('r-oos-power', round(c15a, 6), 0)
wrong('r-oos-power', 'halved-only', mean_t(240), 0)
wrong('r-oos-power', 'full-mean', round(4.0 * math.sqrt(120 / 240), 6), 0)
tdraw = c15a + RNG.standard_normal(1000000)
sim15 = float((tdraw > 2).mean())
rec(abs(sim15 - (1 - N01.cdf(2 - c15a))) < 0.002, f'r-oos-power: simulated P(t > 2) = {sim15:.4f}')
key('r-oos-power', round(1 - N01.cdf(2 - c15a), 6), 1)
wrong('r-oos-power', 'nothing-survived', round(1 - N01.cdf(2), 6), 1)
wrong('r-oos-power', 'below-two', round(N01.cdf(2 - c15a), 6), 1)
months = bisect(lambda m: mean_t(m) - 2, 1, 5000)
key('r-oos-power', round(months, 6), 2)
wrong('r-oos-power', 'same-t', round(bisect(lambda m: mean_t(m) - 4, 1, 5000), 6), 2)
wrong('r-oos-power', 'doubled', 480, 2)
allow('r-oos-power', 4.0, 240, 120, 0.5, 1.41, 28, round(c15a, 2), 1 - N01.cdf(2 - c15a))

# ---------------------------------------------------------------- the exam document: papers, checks and draws
papers = {p['id']: p for p in doc['parts'] if p['kind'] == 'paper'}
checks = [p for p in doc['parts'] if p['kind'] == 'check']
rec(list(papers) == ['probability', 'arithmetic', 'research', 'coding'], f'papers {list(papers)}')
rec([c['id'] for c in checks] == ['zhou-probability', 'zetamac-50', 'mock-interviews', 'replication-github'], 'four checks, each from a Stage 3 exit line')
A_items, C_items = papers['probability']['items'], papers['research']['items']
rec(len(A_items) == 12 and sum(d['n'] for d in papers['probability']['draw']) == 6, 'paper A: 12 authored items and 6 drawn')
rec(papers['probability']['pass'] == 0.8, 'paper A passes at 0.8, the Zhou 80%')
rec(papers['probability']['minutes'] * 60 >= sum(it['pace'] for it in A_items) + 6 * 180, 'paper A: minutes cover the pace')
ramp = [sum(it['difficulty'] == d for it in C_items) for d in (2, 3, 4, 5)]
rec(len(C_items) == 15 and ramp == [3, 8, 3, 1], f'paper C: 15 items at the ramp {ramp}')
rec(papers['research']['minutes'] == int(math.ceil(1.25 * sum(it['pace'] for it in C_items) / 60 / 5) * 5), 'paper C: minutes are 1.25 times the pace')
B = papers['arithmetic']
g = B['items'][0]
rec(g['generator'] == 'arith' and 'mix' not in g and g['n'] == 80 and B['minutes'] == 2, 'paper B: 80 generated items on the default (Zetamac) ranges in 2 minutes')
warm = json.load(open(os.path.join(CDIR, 'warmup.json')))
ops = {o['id']: o for o in warm['operations']}
rec(ops['add']['a'] == [2, 100] and ops['add']['b'] == [2, 100] and ops['mul']['a'] == [2, 12] and ops['mul']['b'] == [2, 100] and warm['seconds'] == 120,
    'paper B: warmup.json ranges are Zetamac defaults, 120 s')
rec(B['passNet'] == warm['targets']['stage3'] == 50 and B['scoring'] == {'right': 1, 'wrong': -1, 'blank': 0} and B['navigation'] == 'forward' and B['skip'] is False,
    'paper B: pass on 50 net, the Stage 3 warm-up target, forward with no skip')
D = papers['coding']
rec(D['minutes'] == 60 and D['pass'] == 1 and sum(d['n'] for d in D['draw']) == 2 and D['items'] == [], 'paper D: two drawn problems, 60 minutes, both needed')
# drawn pools hold at least twice n, every drawn drill is Python and medium
for p in papers.values():
    for d in p.get('draw', []):
        src, name = d['from'].split('/')
        lo_, hi_ = (d['difficulty'], d['difficulty']) if isinstance(d['difficulty'], int) else d['difficulty']
        if src == 'bank':
            pool = [it for f in glob.glob(os.path.join(CDIR, 'bank', f'{name}-*.json')) for it in json.load(open(f))['items']
                    if it['tags'][0] in d['tags'] and lo_ <= it['difficulty'] <= hi_]
        else:
            pool = [x for f in glob.glob(os.path.join(CDIR, 'drills', f'{name}-*.json')) for x in [json.load(open(f))]
                    if lo_ <= x['difficulty'] <= hi_ and ('tags' not in d or set(d['tags']) & set(x.get('tags', []) + [x.get('pattern')]))]
            rec(all(x.get('language', 'python') == 'python' and x['difficulty'] == 3 for x in pool), f'{p["id"]} draw {d["from"]}: every drill is a Python medium')
        rec(len(pool) >= 2 * d['n'] and len(d.get('tags', [])) <= 4, f'{p["id"]} draw {d["from"]} {d.get("tags", "")}: pool {len(pool)} >= 2n = {2 * d["n"]}')
# no optional topic gates the pass: every skill on an authored item is from 3.1, 3.3 or 3.5
cur = json.load(open(os.path.join(CDIR, 'curriculum.json')))
skill_topic = {}
for st in cur['stages']:
    for tp in st['topics']:
        for c in tp['courses']:
            for s in json.load(open(os.path.join(CDIR, 'courses', c, 'course.json')))['skills']:
                skill_topic[s] = tp['id']
tops = {skill_topic[s] for it in ITEM.values() for s in it['skills']} | {skill_topic[s] for s in g['skills']}
rec(tops == {'3.1', '3.3'}, f'authored and generated items come from topics {sorted(tops)} (3.5 is drawn), none from 3.2 or 3.4')

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard', 'starter', 'solution', 'tests', 'examples', 'skills', 'placeholder', 'accept'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)          # printed code is read by its own check
    s = re.sub(r'`[^`]*`', ' ', s)
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t and 'e' not in t.lower() else 0), t


for iid, it in ITEM.items():
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v for k, v in it.items() if k not in ('difficulty', 'pace')}):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}' if bad else '')

# the accept lines of the two % keys
rec(W('r-turnover-cost')['accept'].startswith('0.79%') and W('r-factor-alpha')['accept'].startswith('0.41%'), 'the % keys: accept leads with the per cent figure')

ex.check_wrongs()
ex.report()
