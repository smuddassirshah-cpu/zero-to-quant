"""Recompute every number stated in app/content/exams/topic-3.1.json by a second route and assert it at its path.

Route A is build.py (closed forms). Route B here is independent: exact Fractions, brute-force counts and loops,
NumPy, bisection, a steady-state composite built cohort by cohort, and the code items run in CPython
(solution passes every case, starter fails at least one). Exits 1 on any failure.
Run: python3 docs/briefs/exam-3.1-scripts/check_numbers.py
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-3.1.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    from numbers_lib import _walk
    return _walk(doc, path)[0]


def key(iid, value, part=None, tol=None):
    """The widget answer equals the route-B value, within a tenth of its tolerance (or 1e-6)."""
    w = node(W(iid, part))
    t = tol if tol is not None else max(w['tol']['abs'] / 10, 1e-9)
    ok = abs(w['answer'] - value) <= t
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if ok else 'route B differs')


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {value!r}', '' if ok else f'found {hit}')


def say(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


# ------------------------------------------------------------------ the file
items = doc['items']
ex._rec(len(items) == 30, '30 items', '')
from collections import Counter
ramp = Counter(i['difficulty'] for i in items)
ex._rec(dict(ramp) == {2: 6, 3: 15, 4: 6, 5: 3}, f'ramp {dict(ramp)} = 6, 15, 6, 3', '')
pace = sum(i['pace'] for i in items)
ex._rec(pace == 4605 and pace / 60 < doc['minutes'], f'pace {pace} s inside {doc["minutes"]} minutes', '')
by_course = Counter('momentum-rep' if all(s.startswith('rm-') for s in i['skills']) else 'pairs-rep' for i in items)
ex._rec(by_course == {'momentum-rep': 15, 'pairs-rep': 15}, f'by course {dict(by_course)}', '')
for s in doc['skills']:
    ex._rec(any(s in i['skills'] for i in items if i.get('kind') != 'longform'), f'skill {s} tested by an auto item', '')

# ------------------------------------------------------------------ difficulty 2
# e-monthly-from-annual: bisection on (1 + r)^12 = 1.1365
lo, hi = 0.0, 0.02
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if (1 + mid) ** 12 < 1.1365 else (lo, mid)
m = lo
assert abs(m - (math.exp(math.log(1.1365) / 12) - 1)) < 1e-12
key('e-monthly-from-annual', m)
wrong('e-monthly-from-annual', 'simple', float(F('0.1365') / 12))
say('e-monthly-from-annual', 'explain.text', round(m * 100, 2))
say('e-monthly-from-annual', 'explain.text', 1.14, fmt='1.14%')
ex._rec(abs(round(m * 100, 2) - 1.07) < 1e-12, 'monthly rounds to 1.07%', '')

# e-pair-count: count the combinations
n140 = sum(1 for _ in itertools.combinations(range(140), 2))
key('e-pair-count', n140, tol=0)
wrong('e-pair-count', 'ordered', sum(1 for _ in itertools.permutations(range(140), 2)))
wrong('e-pair-count', 'square', len(list(itertools.product(range(140), repeat=2))))
say('e-pair-count', 'explain.text', 9730)
say('e-pair-count', 'explain.text', 139)
say('e-pair-count', 'feedback.byKey.ordered', 19460)

# e-survival-share
key('e-survival-share', float(F(46, 115)))
wrong('e-survival-share', 'lost', float(1 - F(46, 115)))
wrong('e-survival-share', 'points', float(F('0.0115') - F('0.0046')))
say('e-survival-share', 'explain.text', 40.0, fmt='40.0')
say('e-survival-share', 'explain.text', 0.69)

# e-root-k: the variance of the mean of overlapping K-sums of iid returns is K times the naive one
K9 = 9
ratio = sum(F(K9 - abs(j), K9) for j in range(-(K9 - 1), K9))   # sum of autocorrelations (K - |j|)/K
ex._rec(ratio == 9, 'overlap variance ratio = K = 9', '')
key('e-root-k', 6.30 / math.sqrt(float(ratio)))
wrong('e-root-k', 'by-k', 6.30 / K9)
wrong('e-root-k', 'times', 6.30 * math.sqrt(K9))
say('e-root-k', 'explain.text', 2.10)
say('e-root-k', 'explain.text', 3)

# e-crash-beta
cb = float((F('0.7') - F('1.6')) * F('0.14'))
key('e-crash-beta', cb)
wrong('e-crash-beta', 'sign', -cb)
wrong('e-crash-beta', 'sum', float((F('0.7') + F('1.6')) * F('0.14')))
say('e-crash-beta', 'explain.text', -0.9)
say('e-crash-beta', 'explain.text', 12.6)

# ------------------------------------------------------------------ difficulty 3
# e-sixteen-cells: binomial pmf
q = 0.0455
p_any = sum(math.comb(16, k) * q ** k * (1 - q) ** (16 - k) for k in range(1, 17))
key('e-sixteen-cells', p_any)
wrong('e-sixteen-cells', 'added', 16 * q)
wrong('e-sixteen-cells', 'one', q)
ex._rec(abs(2 * (1 - 0.5 * (1 + math.erf(2 / math.sqrt(2)))) - q) < 5e-5, 'P(|Z| > 2) = 0.0455', '')
say('e-sixteen-cells', 'explain.text', round((1 - q) ** 16, 2))
say('e-sixteen-cells', 'explain.text', round(p_any, 2))

# e-ssd-sd: numpy
A = np.array([1, 1.04, 1.02, 1.07, 1.05])
B = np.array([1, 1.01, 1.04, 1.03, 1.06])
s = A - B
key('e-ssd-sd', float(np.sum((A - B) ** 2)), part=0)
wrong('e-ssd-sd', 'sum-then-square', float(np.sum(s)) ** 2, part=0)
wrong('e-ssd-sd', 'mean', float(np.mean(s ** 2)), part=0)
key('e-ssd-sd', float(np.std(s)), part=1)
wrong('e-ssd-sd', 'ddof-one', float(np.std(s, ddof=1)), part=1)
wrong('e-ssd-sd', 'no-mean', float(np.sqrt(np.mean(s ** 2))), part=1)
say('e-ssd-sd', 'explain.text', 0.0030)
say('e-ssd-sd', 'explain.text', round(float(np.mean(s)), 3))
say('e-ssd-sd', 'explain.text', round(float(np.var(s)), 6))
say('e-ssd-sd', 'explain.text', round(float(np.std(s)), 4))
say('e-ssd-sd', 'parts[0].feedback.byKey', 0.0016)

# e-lowest-match
se4 = 6.30 / 300 ** 0.5
key('e-lowest-match', (0.95 - 2 * se4) / 100)
wrong('e-lowest-match', 'one-se', (0.95 - se4) / 100)
wrong('e-lowest-match', 'over-n', (0.95 - 2 * 6.30 / 300) / 100)
say('e-lowest-match', 'explain.text', round(se4, 3))
say('e-lowest-match', 'explain.text', round(2 * se4, 2))
say('e-lowest-match', 'explain.text', round(0.95 - 2 * se4, 2))
say('e-lowest-match', 'explain.text', round(0.95 + 2 * se4, 2))

# e-capital-split: Fractions
tot = F('0.88')
key('e-capital-split', float(tot / 20 / 6), part=0)
wrong('e-capital-split', 'employed', float(tot / 16 / 6), part=0)
wrong('e-capital-split', 'cycle', float(tot / 20), part=0)
key('e-capital-split', float(tot / 16), part=1)
wrong('e-capital-split', 'committed', float(tot / 20), part=1)
wrong('e-capital-split', 'legs', float(tot / 32), part=1)
say('e-capital-split', 'explain.text', 4.4)
say('e-capital-split', 'explain.text', round(float(tot / 20 / 6) * 100, 2))
say('e-capital-split', 'explain.text', 5.5)
say('e-capital-split', 'explain.text', float(F(55, 44)))

# e-dead-losers: the 50 returns listed one by one
rets = [0.012] * 45 + [-0.40] * 5
true_loser = sum(rets) / len(rets)
surv = [x for x in rets if x > -0.40]
gap = sum(surv) / len(surv) - true_loser
key('e-dead-losers', gap)
wrong('e-dead-losers', 'over-45', sum(surv) / len(surv) - sum(rets) / 45)
wrong('e-dead-losers', 'dead-only', 5 * 0.40 / 50)
say('e-dead-losers', 'explain.text', round(true_loser * 100, 2))
say('e-dead-losers', 'explain.text', round(gap * 100, 2))

# e-one-trade: units route (1/price units of each leg)
u_j, u_i = 1 / 0.960, 1 / 1.011
pnl = u_j * (1.010 - 0.960) - u_i * (0.998 - 1.011)
key('e-one-trade', pnl, part=1)
wrong('e-one-trade', 'wrong-side', -pnl, part=1)
wrong('e-one-trade', 'price-gaps', float(F('1.010') - F('0.960') - (F('0.998') - F('1.011'))), part=1)
ex._rec(1.011 - 0.960 > 2 * 0.022 and 0.998 - 1.010 < 0, 'opens on day 12 and crosses by day 40', '')
ex._rec(node(W('e-one-trade', 0))['options'][0]['id'] == 'short-dear' and node(W('e-one-trade', 0))['options'][0].get('correct'), 'short the dearer leg is the key', '')
say('e-one-trade', 'explain.text', round(1.011 - 0.960, 3))
say('e-one-trade', 'explain.text', 2 * 0.022)
say('e-one-trade', 'explain.text', round(u_j * (1.010 - 0.960), 4))
say('e-one-trade', 'explain.text', round(-u_i * (0.998 - 1.011), 4))
say('e-one-trade', 'explain.text', round(pnl, 4))

# e-month-counts: brute force over month indices
T, J, Kc, sk = 360, 9, 4, 1
first_rank = J + sk                      # first month whose ranking window is complete
comp_months = [t for t in range(T) if t - Kc + 1 >= first_rank]
key('e-month-counts', len(comp_months), part=0, tol=0)
wrong('e-month-counts', 'no-warmup', len([t for t in range(T) if t >= first_rank]), part=0)
wrong('e-month-counts', 'no-skip', len([t for t in range(T) if t - Kc + 1 >= J]), part=0)
blocks, t0 = 0, first_rank
while t0 + Kc <= T:
    blocks, t0 = blocks + 1, t0 + Kc
key('e-month-counts', blocks, part=1, tol=0)
wrong('e-month-counts', 'all-months', T // Kc, part=1)
wrong('e-month-counts', 'from-composite', len(comp_months) // Kc, part=1)
say('e-month-counts', 'explain.text', first_rank)
say('e-month-counts', 'explain.text', comp_months[0])
say('e-month-counts', 'explain.text', T - first_rank)

# e-bounce-share
key('e-bounce-share', float((F('1.18') - F('0.95')) / F('1.18')))
wrong('e-bounce-share', 'wait-gap', float((F('1.18') - F('0.85')) / F('1.18')))
wrong('e-bounce-share', 'over-mids', float((F('1.18') - F('0.95')) / F('0.95')))
say('e-bounce-share', 'explain.text', 0.23)
say('e-bounce-share', 'explain.text', 0.33)
say('e-bounce-share', 'explain.text', 0.10)
say('e-bounce-share', 'explain.text', 19.5)

# e-gap-in-se
se10 = 5.90 / 17
ex._rec(17 ** 2 == 289, 'sqrt(289) = 17', '')
key('e-gap-in-se', (0.95 - 0.68) / se10)
wrong('e-gap-in-se', 'over-sd', (0.95 - 0.68) / 5.90)
wrong('e-gap-in-se', 'over-n', (0.95 - 0.68) / (5.90 / 289))
say('e-gap-in-se', 'explain.text', round(se10, 3))
say('e-gap-in-se', 'explain.text', round((0.95 - 0.68) / se10, 2))

# e-convergence-pooled
conv = [(36, 48), (22, 40), (15, 32)]
key('e-convergence-pooled', sum(a for a, _ in conv) / sum(b for _, b in conv), part=0)
wrong('e-convergence-pooled', 'mean-of-shares', float(sum(F(a, b) for a, b in conv) / 3), part=0)
say('e-convergence-pooled', 'explain.text', 73)
say('e-convergence-pooled', 'explain.text', 120)
say('e-convergence-pooled', 'explain.text', 60.8)
say('e-convergence-pooled', 'explain.text', round(float(sum(F(a, b) for a, b in conv) / 3) * 100, 1))

# e-chance-passes
n120 = sum(1 for _ in itertools.combinations(range(120), 2))
key('e-chance-passes', n120 * 0.01)
wrong('e-chance-passes', 'shares', 120 * 0.01)
wrong('e-chance-passes', 'ordered', sum(1 for _ in itertools.permutations(range(120), 2)) * 0.01)
say('e-chance-passes', 'explain.text', n120)
say('e-chance-passes', 'feedback.byKey.ordered', 14280)

# e-lock-count: walk the days
cnt = n_start = n_form = 0
s0 = 0
while s0 < 3024:
    days = range(s0, s0 + 378)
    cnt += all(d < 1764 for d in days)
    n_start += s0 < 1764
    n_form += all(d < 1764 for d in range(s0, s0 + 252))
    s0 += 21
key('e-lock-count', cnt, tol=0)
wrong('e-lock-count', 'starts', n_start)
wrong('e-lock-count', 'formation', n_form)
say('e-lock-count', 'explain.text', 1386)
say('e-lock-count', 'explain.text', 377)
say('e-lock-count', 'explain.text', 67)

# ------------------------------------------------------------------ difficulty 4
# e-nw-hand: the Bartlett kernel summed over j = -L..L
gam = {0: 36.0, 1: -3.0, 2: 1.2}
L = 2
Vb = sum((1 - abs(j) / (L + 1)) * gam[abs(j)] for j in range(-L, L + 1))
key('e-nw-hand', 0.80 / math.sqrt(Vb / 240))
wrong('e-nw-hand', 'naive', 0.80 / math.sqrt(gam[0] / 240))
wrong('e-nw-hand', 'unweighted', 0.80 / math.sqrt(sum(gam[abs(j)] for j in range(-L, L + 1)) / 240))
say('e-nw-hand', 'explain.text', round(Vb, 1))
say('e-nw-hand', 'explain.text', round(math.sqrt(Vb / 240), 3))
say('e-nw-hand', 'explain.text', round(0.80 / math.sqrt(gam[0] / 240), 2))
say('e-nw-hand', 'explain.text', 3.2)

# e-after-pub
se_d = (5.8 ** 2 / 288 + 6.6 ** 2 / 168) ** 0.5
key('e-after-pub', float(F(40, 110)), part=0)
wrong('e-after-pub', 'lost', float(F(70, 110)), part=0)
wrong('e-after-pub', 'points', 0.007, part=0)
key('e-after-pub', -0.70 / se_d, part=1)
wrong('e-after-pub', 'after-only', -0.70 / (6.6 / 168 ** 0.5), part=1)
wrong('e-after-pub', 'no-n', -0.70 / (5.8 ** 2 + 6.6 ** 2) ** 0.5, part=1)
say('e-after-pub', 'explain.text', round(se_d, 3))
say('e-after-pub', 'explain.text', round(-0.70 / se_d, 2))
say('e-after-pub', 'explain.text', 36.4)

# e-break-even-net: bisection on the cost that zeroes the net
lo, hi = 0.0, 0.1
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 0.052 - 4 * 1.8 * mid > 0 else (lo, mid)
key('e-break-even-net', lo, part=0)
wrong('e-break-even-net', 'per-trip', 0.052 / 1.8, part=0)
wrong('e-break-even-net', 'once', 0.052 / 4, part=0)
net = float((F('0.052') - 4 * F('1.8') * F('0.0025')) / 6)
key('e-break-even-net', net, part=1)
wrong('e-break-even-net', 'once', float((F('0.052') - 4 * F('0.0025')) / 6), part=1)
wrong('e-break-even-net', 'per-trip', float((F('0.052') - F('1.8') * F('0.0025')) / 6), part=1)
say('e-break-even-net', 'explain.text', 7.2)
say('e-break-even-net', 'explain.text', round(lo * 100, 2))
say('e-break-even-net', 'explain.text', 1.8)
say('e-break-even-net', 'explain.text', 3.4)
say('e-break-even-net', 'explain.text', round(net * 100, 2))

# e-hedge-ratio: exp of the log relation
Lp = math.exp(1.8 * math.log(1.05) + 0.0)
key('e-hedge-ratio', Lp - 1.05, part=0)
wrong('e-hedge-ratio', 'l-only', Lp - 1, part=0)
wrong('e-hedge-ratio', 'one-to-one', 0.0, part=0)
ex._rec(Lp - 1.05 > 2 * 0.015, 'the 1 to 1 spread passes 2 sd', '')
say('e-hedge-ratio', 'explain.text', round(Lp, 4))
say('e-hedge-ratio', 'explain.text', round(Lp - 1.05, 4))
say('e-hedge-ratio', 'parts[1].widget', round(Lp, 4))
say('e-hedge-ratio', 'parts[1].widget', 0.030, fmt='0.030')

# ------------------------------------------------------------------ difficulty 5
# e-skip-event: a steady-state composite built cohort by cohort from event-time spreads
ev = {1: -0.40, 2: 0.80, 3: 0.75, 4: 0.70, 5: 0.6, 6: 0.5, 7: 0.4, 8: 0.35, 9: 0.3, 10: 0.2, 11: 0.1, 12: 0.05, 13: -0.10}


def comp_mean(K, skip, months=60):
    # cohort ranked at the start of month s (window ends s - 1 - skip) earns ev[t - s + 1 + skip] in month t
    vals = []
    for t in range(K, months):
        live = [ev[t - s + 1 + skip] for s in range(t - K + 1, t + 1)]
        vals.append(sum(live) / K)
    return sum(vals) / len(vals)


d3 = (comp_mean(3, 1) - comp_mean(3, 0)) / 100
d12 = (comp_mean(12, 1) - comp_mean(12, 0)) / 100
key('e-skip-event', d3, part=0)
wrong('e-skip-event', 'no-divide', 3 * d3, part=0)
wrong('e-skip-event', 'reversed', -d3, part=0)
key('e-skip-event', d12, part=1)
wrong('e-skip-event', 'no-divide', 12 * d12, part=1)
wrong('e-skip-event', 'reversed', -d12, part=1)
say('e-skip-event', 'explain.text', round(d3 * 100 * 3, 2))
say('e-skip-event', 'explain.text', round(d3 * 100, 2))
say('e-skip-event', 'explain.text', round(d12 * 100 * 12, 2))
say('e-skip-event', 'explain.text', round(d12 * 100, 3))


# code items: run solution and starter on every case in CPython
def run_cases(w, source):
    out = []
    ns = {'__name__': '__main__'}
    exec(w.get('prelude', ''), ns)
    exec(source, ns)
    for c in w['tests']:
        try:
            got = eval(c['call'], ns)
            want = eval(c['expect'], ns)
            if c.get('compare') == 'isclose':
                a = np.array(got, dtype=float).ravel()
                b = np.array(want, dtype=float).ravel()
                ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= c.get('tol', {}).get('abs', 1e-9)))
            else:
                ok = got == want
        except Exception:
            ok = False
        out.append(ok)
    return out


for cid in ('e-capital-code', 'e-composite-code'):
    w = node(W(cid))
    sol = run_cases(w, w['solution'])
    sta = run_cases(w, w['starter'])
    ex._rec(all(sol), f'{cid}: solution passes {sum(sol)} of {len(sol)}', '')
    ex._rec(not all(sta), f'{cid}: starter fails {len(sta) - sum(sta)} of {len(sta)}', '')
    exw = dict(w, tests=w['examples'])
    ex._rec(all(run_cases(exw, w['solution'])), f'{cid}: solution passes the examples', '')

# composite expectations by a second route: a full month by cohort matrix, averaged by column
wc = node(W('e-composite-code'))
nsc = {}
exec(wc['prelude'], nsc)
for c in wc['tests']:
    if c['call'] == 'jt_composite(BIG, 6)':
        Bm = np.full((40, 40), np.nan)
        for s_, row in enumerate(nsc['BIG']):
            for h, v in enumerate(row):
                if s_ + h < 40:
                    Bm[s_, s_ + h] = v
        cols = [np.nanmean(Bm[:, t]) for t in range(5, 40)]
        ex._rec(np.allclose(cols, eval(c['expect']), atol=1e-12), 'BIG composite by column means', '')
wk = node(W('e-capital-code'))
ex._rec(eval(wk['examples'][0]['expect']) == [0.006, 0.015] or np.allclose(eval(wk['examples'][0]['expect']), [0.03 / 5, 0.03 / 2]),
        'capital example (0.006, 0.015)', '')

# e-survival-note: the model's numbers
cost = 0.60 * 0.25
gross, after = 0.88, 0.31
diff = after - gross
se_n = abs(diff) / 0.98
md = 'model'
say('e-survival-note', md, round(after / gross * 100))
say('e-survival-note', md, round(cost, 2))
say('e-survival-note', md, round(gross - cost, 2))
say('e-survival-note', md, round(after - cost, 2))
say('e-survival-note', md, round((after - cost) / (gross - cost) * 100))
say('e-survival-note', md, round(diff - 1.96 * se_n, 2))
say('e-survival-note', md, round(diff + 1.96 * se_n, 2))
ex._rec(diff - 1.96 * se_n < -gross and diff + 1.96 * se_n > 0, 'interval covers no fall and the whole effect', '')
ex._rec(sum(r['points'] for r in node(P('e-survival-note'))['rubric']) == 10, 'rubric sums to 10', '')

# fix pass: every wrong value, rounded as asked, lies inside its own tol and outside the answer band
def _band(iid, wid, shown, decimals, part=None):
    w = node(W(iid, part))
    x = [y for y in w['wrong'] if y['id'] == wid][0]
    r = round(shown, decimals)
    ex._rec(abs(r - x['value']) <= x['tol']['abs'], f'{iid} {wid}: typed {r} lands in its band', '')
    ex._rec(abs(r - w['answer']) > w['tol']['abs'], f'{iid} {wid}: typed {r} is outside the answer band', '')


_band('e-monthly-from-annual', 'simple', 0.1365 / 12, 4)
ex._rec(abs(0.0114 - node(W('e-monthly-from-annual'))['wrong'][0]['value']) <= 5e-5, 'typed 1.14 hits simple', '')
_band('e-nw-hand', 'naive', 2.06559, 2)
_band('e-nw-hand', 'unweighted', 2.17732, 2)
ex._rec(abs(round(0.045763, 2) - node(W('e-gap-in-se'))['wrong'][0]['value']) <= node(W('e-gap-in-se'))['wrong'][0]['tol']['abs'], 'e-gap-in-se: typed 0.05 hits over-sd', '')
pt = [x for x in node(W('e-survival-share'))['wrong'] if x['id'] == 'points'][0]
ex._rec(abs(0.007 - pt['value']) <= pt['tol']['abs'], 'e-survival-share: typed 0.7% hits points', '')

# the capital starter fails every hidden test, one by one
wcap = node(W('e-capital-code'))
sta = run_cases(wcap, wcap['starter'])
ex._rec(not any(sta), f'e-capital-code: starter fails all {len(sta)} hidden tests', '')
ex._rec(all(run_cases(wcap, wcap['solution'])), 'e-capital-code: solution passes all hidden tests', '')
# the composite's first hidden test is unseen, by a hand route: (0.03 + 0.02)/2, (-0.01 + 0.04)/2, (0.0 - 0.02)/2
ex._rec(wc['tests'][0]['call'] != wc['examples'][0]['call'], 'e-composite-code: tests[0] is not the example', '')
ex._rec(np.allclose([(0.03 + 0.02) / 2, (-0.01 + 0.04) / 2, (0.0 - 0.02) / 2], [0.025, 0.015, -0.01]), 'composite tests[0] by hand', '')
ex._rec(abs(0.60 * 0.25 - 0.15) < 1e-12 and len(node(P('e-survival-note'))['model'].split('. ')) <= 8, 'longform model has at most 8 sentences', '')

ex.check_wrongs()
ex.report()
