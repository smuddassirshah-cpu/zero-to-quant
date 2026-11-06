"""Recompute every number stated in app/content/exams/topic-2.6.json by a second route and assert it at its path.

Route A is build.py (closed forms with math and statistics). Route B here is independent: exact Fractions,
tanh for the inverse logit, Simpson integration of the chi-square, normal and gamma densities, bisection for
normal quantiles, brute-force pair counts, the classic Kruskal-Wallis formula with its tie correction, NumPy for
the Walsh averages, and both code items run in CPython (solution passes every case, starter fails every case).
Exits 1 on any failure. Run: python3 docs/briefs/exam-2.6-scripts/check_numbers.py
"""
import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.6.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None):
    w = node(W(iid, part))
    t = max(w['tol']['abs'] / 10, 1e-9) if w['tol']['abs'] else 1e-9
    ok = abs(w['answer'] - value) <= max(t, 0.5 * 10 ** -6 if w['tol']['abs'] else 0)
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if ok else 'route B differs')


def key_round(iid, value, nd, part=None):
    """The key equals route B rounded to nd places (the value shown to the learner)."""
    w = node(W(iid, part))
    ok = abs(w['answer'] - round(value, nd)) <= 10 ** -(nd + 3) and abs(w['answer'] - value) <= w['tol']['abs']
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = round({value!r}, {nd})', '' if ok else 'route B differs')


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 5, 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {value!r}', '' if ok else f'found {hit}')


def say(iid, path, value, fmt=None, part=None):
    ex.expect('exam', f'{P(iid, part)}.{path}', value, fmt=fmt)


def simpson(f, a, b, n=20000):
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, n))
    return s * h / 3


def chi2_tail(x, df):
    c = 1 / (2 ** (df / 2) * math.gamma(df / 2))
    dens = lambda t: c * t ** (df / 2 - 1) * math.exp(-t / 2)  # noqa: E731
    return simpson(dens, x, x + 80)


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def zq(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if phi(mid) < p else (lo, mid)
    return (lo + hi) / 2


# ------------------------------------------------------------------ the file
ex._rec(20 <= len(items) <= 30, f'{len(items)} items, 20 to 30', '')
ramp = Counter(i['difficulty'] for i in items)
ex._rec(dict(ramp) == {2: 5, 3: 13, 4: 5, 5: 2}, f'ramp {dict(sorted(ramp.items()))} = 5, 13, 5, 2', '')
pace = sum(i['pace'] for i in items)
ex._rec(pace == 3420 and pace / 60 < doc['minutes'], f'pace {pace} s inside {doc["minutes"]} minutes', '')
ex._rec(doc['pass'] == 0.7, 'pass 0.7', '')
with open(os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses', 'stat-models', 'course.json'), encoding='utf8') as f:
    course = json.load(f)
ex._rec(set(doc['skills']) == set(course['skills']), 'skills map = the course skills', '')
ex._rec({s for it in items for s in it['skills']} == set(course['skills']), 'every skill on an auto-graded item', '')
for it in items:
    ws = [p['widget'] for p in it['parts']] if 'parts' in it else [it['widget']]
    for w in ws:
        if w['kind'] in ('choice', 'multi'):
            ex._rec(w.get('shuffle') is True, f'{it["id"]} {w["kind"]} shuffles', '')
            nc = sum(o.get('correct', False) for o in w['options'])
            ex._rec(nc == 1 if w['kind'] == 'choice' else nc >= 2, f'{it["id"]} correct count {nc}', '')
            ex._rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{it["id"]} every distractor has a why', '')

# ------------------------------------------------------------------ difficulty 2
eta = F(-42, 10) + F(60, 10) * F(1, 2)
ex._rec(eta == F(-6, 5), 'e-pd eta = -1.2', '')
pd = (1 + math.tanh(float(eta) / 2)) / 2
key('e-pd-at-leverage', pd)
wrong('e-pd-at-leverage', 'odds', 1 / math.exp(1.2))
wrong('e-pd-at-leverage', 'sign', (1 - math.tanh(float(eta) / 2)) / 2)
say('e-pd-at-leverage', 'explain.text', round(1 / math.exp(1.2), 4))
say('e-pd-at-leverage', 'explain.text', round(pd * 100, 2))
say('e-pd-at-leverage', 'feedback.byKey', round(math.exp(-1.2), 4))

Fa = F(18, 3 - 1) / F(105, 24 - 3)
key('e-algo-f', float(Fa))
wrong('e-algo-f', 'ratio', 18 / 105)
wrong('e-algo-f', 'total-df', float(F(18, 2) / F(105, 23)))
wrong('e-algo-f', 'k-df', float(F(18, 3) / F(105, 24)))
say('e-algo-f', 'feedback.correct', float(F(105, 21)))
for k, v in (('ratio', 18 / 105), ('total-df', float(F(18, 2) / F(105, 23))), ('k-df', float(F(18, 3) / F(105, 24)))):
    say('e-algo-f', 'feedback.byKey', round(v, 4))

pairs = 12 * 15
key('e-u-share', float(F(99, pairs)))
wrong('e-u-share', 'flipped', float(1 - F(99, pairs)))
wrong('e-u-share', 'sum', 99 / 27)
say('e-u-share', 'explain.text', pairs)

post = (F(4) + 18) / (F(4) + 6 + 50)
key_round('e-fill-posterior', float(post), 4)
wrong('e-fill-posterior', 'data', float(F(18, 50)))
wrong('e-fill-posterior', 'prior', float(F(4, 10)))
wrong('e-fill-posterior', 'swapped', float(F(4 + 32, 60)))
say('e-fill-posterior', 'feedback.correct', 6 + 32)
say('e-fill-posterior', 'explain.text', round(float(post), 4))

# ------------------------------------------------------------------ difficulty 3
lam = math.exp(math.log(20) + (-0.9 + 0.045 * 18))
key_round('e-trades-offset', lam, 4)
wrong('e-trades-offset', 'no-offset', math.exp(-0.09))
wrong('e-trades-offset', 'times-log', math.log(20) * math.exp(-0.09))
say('e-trades-offset', 'feedback.correct', round(lam, 2))
say('e-trades-offset', 'explain.text', round(math.exp(-0.09), 4))
say('e-trades-offset', 'explain.text', 0.045 * 18 - 0.9)

mu = 0.2
eta4 = math.log(mu) - math.log(1 - mu)
z4 = eta4 - 1 / (1 - mu)          # (0 - mu) / (mu (1 - mu)) = -1 / (1 - mu)
key_round('e-working-response', z4, 4)
wrong('e-working-response', 'no-weight', eta4 - mu)
wrong('e-working-response', 'times-weight', eta4 - mu * mu * (1 - mu))
say('e-working-response', 'feedback.correct', round(z4, 4))
say('e-working-response', 'feedback.correct', round(eta4, 4))
say('e-working-response', 'feedback.byKey', round(eta4 - mu, 4))
say('e-working-response', 'feedback.byKey', round(eta4 - mu * mu * (1 - mu), 4))

p2 = chi2_tail(7.5, 2)
key_round('e-deviance-two', p2, 4)
wrong('e-deviance-two', 'one-df', chi2_tail(7.5, 1))
say('e-deviance-two', 'feedback.byKey', round(chi2_tail(7.5, 1), 4))
say('e-deviance-two', 'explain.text', 412.6 - 405.1)

za, zb = zq(0.975), zq(0.8)
n3 = 2 * (za + zb) ** 2 * 81 / 4
key('e-orders-per-arm', math.ceil(n3))
wrong('e-orders-per-arm', 'no-two', math.ceil(n3 / 2))
wrong('e-orders-per-arm', 'one-sided', math.ceil(2 * (zq(0.95) + zb) ** 2 * 81 / 4))
say('e-orders-per-arm', 'explain.text', round((za + zb) ** 2, 4))
say('e-orders-per-arm', 'explain.text', round(n3, 1))
say('e-orders-per-arm', 'feedback.correct', round(za, 4))
say('e-orders-per-arm', 'feedback.correct', round(zb, 4))
say('e-orders-per-arm', 'feedback.byKey', round(zq(0.95), 4))

Xd = [0.4, 1.2, -0.3, 0.9]
Yd = [0.1, -0.5, 0.6, 0.2, -0.1]
pooled = sorted(Xd + Yd)
rs = sum(pooled.index(x) + 1 for x in Xd)
key('e-u-from-days', rs - 4 * 5 // 2)
wrong('e-u-from-days', 'rank-sum', rs)
wrong('e-u-from-days', 'u-y', sum(y > x for x in Xd for y in Yd))
say('e-u-from-days', 'feedback.correct', [sum(x > y for y in Yd) for x in Xd][1])
ex._rec([sum(x > y for y in Yd) for x in Xd] == [4, 5, 1, 5], 'per-day wins 4, 5, 1, 5', '')
say('e-u-from-days', 'explain.text', float(F(rs - 10, 20)))

key('e-perm-p', float(F(13, 1000)))
wrong('e-perm-p', 'raw', 12 / 999)
say('e-perm-p', 'feedback.byKey', round(12 / 999, 4))

sp = min(1.6, 1.75 / 1.34)
h = 0.9 * sp * math.exp(-0.2 * math.log(250))
key_round('e-silverman-250', h, 4)
wrong('e-silverman-250', 'used-s', 0.9 * 1.6 * math.exp(-0.2 * math.log(250)))
wrong('e-silverman-250', 'no-n', 0.9 * sp)
say('e-silverman-250', 'explain.text', round(math.exp(-0.2 * math.log(250)), 4))
say('e-silverman-250', 'explain.text', round(1.75 / 1.34, 4))
say('e-silverman-250', 'feedback.byKey', round(0.9 * 1.6 * 250 ** -0.2, 4))
say('e-silverman-250', 'feedback.byKey', round(0.9 * sp, 4))

pmf18 = [F(math.factorial(18), math.factorial(k) * math.factorial(18 - k)) / 2 ** 18 for k in range(19)]
two = sum(pmf18[k] for k in range(19) if abs(k - 9) >= 5)
key_round('e-sign-test-ties', float(two), 4)
wrong('e-sign-test-ties', 'one-sided', float(two / 2))
pmf20 = [F(math.factorial(20), math.factorial(k) * math.factorial(20 - k)) / 2 ** 20 for k in range(21)]
wrong('e-sign-test-ties', 'kept-ties', float(sum(pmf20[k] for k in range(21) if abs(k - 10) >= 4)))
say('e-sign-test-ties', 'feedback.correct', int(sum(pmf18[k] for k in range(14, 19)) * 2 ** 18))
say('e-sign-test-ties', 'explain.text', round(float(two / 2), 4))
ex._rec([int(pmf18[k] * 2 ** 18) for k in range(14, 19)] == [3060, 816, 153, 18, 1], 'binomial counts 3,060, 816, 153, 18, 1', '')
say('e-sign-test-ties', 'feedback.byKey', round(float(sum(pmf20[k] for k in range(21) if abs(k - 10) >= 4)), 4))

shape, rate = 3 + sum([2, 0, 3, 1, 1]), 2 + 5
key_round('e-default-rate', float(F(shape, rate)), 4)
wrong('e-default-rate', 'no-periods', float(F(shape, 2)))
wrong('e-default-rate', 'data', float(F(7, 5)))
say('e-default-rate', 'explain.text', float(F(3, 2)))

pr, pd_ = F(1) / F(9, 4), F(1, 9)
pm = (0 * pr + 8 * pd_) / (pr + pd_)
key('e-alpha-prior', float(pm) / 100)
wrong('e-alpha-prior', 'average', 0.04)
wrong('e-alpha-prior', 'inverted', float((8 * pr) / (pr + pd_)) / 100)
ex._rec(pr == 4 * pd_, 'prior four times as precise', '')
say('e-alpha-prior', 'feedback.byKey', float((8 * pr) / (pr + pd_)))

dl = -15.1 + 14.2
ex._rec(0.35 < math.exp(dl), 'u below exp(log ratio): accept', '')
key('e-metropolis-log', 0.95)
wrong('e-metropolis-log', 'reject', 1.20)
say('e-metropolis-log', 'feedback.correct', round(math.log(0.35), 4))
say('e-metropolis-log', 'explain.text', round(math.exp(dl), 4))

tau = 1 + 2 * sum(0.75 ** k for k in range(1, 2000))
key('e-ess-sticky', round(6000 / tau, 2))
wrong('e-ess-sticky', 'one-minus', 6000 * 0.25)
wrong('e-ess-sticky', 'over-one-plus', 6000 / 1.75)
say('e-ess-sticky', 'feedback.correct', round(6000 / tau, 1))
say('e-ess-sticky', 'explain.text', round(0.25 / 1.75, 4))
say('e-ess-sticky', 'feedback.byKey', round(6000 / 1.75, 1))

# ------------------------------------------------------------------ difficulty 4
g = {"A": [2, 3, 3, 4], "B": [4, 5, 5, 6], "C": [5, 7, 8, 8]}
flat = [F(v) for v in sum(g.values(), [])]
gm = sum(flat) / len(flat)
sst = sum((v - gm) ** 2 for v in flat)
ssw = sum((F(v) - F(sum(x), len(x))) ** 2 for x in g.values() for v in x)
ssb = sst - ssw
tw = node(W('e-broker-anova'))
ex._rec(tw['rows'][0][1]['answer'] == ssb == 32, f'SSB {ssb}', '')
ex._rec(tw['rows'][1][1]['answer'] == ssw == 10, f'SSW {ssw}', '')
ex._rec(tw['rows'][0][3]['answer'] == ssb / 2, 'MSB 16', '')
ex._rec(abs(tw['rows'][1][3]['answer'] - float(ssw / 9)) < 5e-5, 'MSW 1.1111', '')
ex._rec(abs(tw['rows'][0][4]['answer'] - float((ssb / 2) / (ssw / 9))) < 5e-5, 'F 14.4', '')
ex._rec(tw['rows'][0][4]['wrong'][0]['value'] == float(ssb / ssw), 'F wrong ss-ratio 3.2', '')
ex._rec(tw['rows'][1][1]['wrong'][0]['value'] == float(sst) == 42, 'SSW wrong total 42', '')
ex._rec(abs(tw['rows'][1][3]['wrong'][0]['value'] - float(ssw / 11)) < 5e-5, 'MSW wrong n-minus-one', '')
fcrit = 4.5 * (0.05 ** (-1 / 4.5) - 1)       # F(2, 9): P(F > f) = (1 + 2f/9)^(-4.5)
ex._rec(abs(fcrit - 4.2565) < 5e-5, f'F(2, 9) 5% cut {fcrit:.4f}', '')
say('e-broker-anova', 'explain.text', round(fcrit, 4))
fbk = node(P('e-broker-anova') + '.feedback')['byKey']
wids = {w['id'] for row in tw['rows'] for c in row if isinstance(c, dict) for w in c.get('wrong', [])}
ex._rec(set(fbk) == wids, 'table byKey keys are the wrong ids, not cell ids', '')

R5 = np.array([-0.8, 0.3, 0.5, 0.2, -0.1, 0.9, 7.9])
med = float(np.sort(R5)[3])
mad = float(np.sort(np.abs(R5 - med))[3])
key('e-takeover-week', med, part=0)
wrong('e-takeover-week', 'mean', float(R5.mean()), part=0)
key_round('e-takeover-week', 1.4826 * mad, 4, part=1)
wrong('e-takeover-week', 'raw', mad, part=1)
wrong('e-takeover-week', 'sd', float(R5.std(ddof=1)), part=1)
say('e-takeover-week', 'explain.text', round(float(R5.std(ddof=1)), 4))
say('e-takeover-week', 'explain.text', round(float(R5.mean()), 4))
say('e-takeover-week', 'explain.text', round(1.4826 * mad, 4))

dens = lambda l: 7 ** 10 * l ** 9 * math.exp(-7 * l) / math.gamma(10)  # noqa: E731
pred = simpson(lambda l: math.exp(-l) * dens(l), 0.0, 30.0)
key_round('e-no-defaults-next', pred, 4, part=0)
wrong('e-no-defaults-next', 'plug-in', math.exp(-10 / 7), part=0)
say('e-no-defaults-next', 'explain.text', round(math.exp(-10 / 7), 4))
say('e-no-defaults-next', 'explain.text', round(pred, 4))
ex.expect('exam', P('e-no-defaults-next', 1) + '.question', round(math.exp(-10 / 7), 4))

key('e-hit-rate-shrink', float(F(60, 100)), part=0)
wrong('e-hit-rate-shrink', 'kappa', float(F(40, 100)), part=0)
key('e-hit-rate-shrink', float(F(18 + 33, 18 + 22 + 60)), part=1)
wrong('e-hit-rate-shrink', 'raw', float(F(33, 60)), part=1)
wrong('e-hit-rate-shrink', 'pop', float(F(18, 40)), part=1)
ex._rec(F(18, 40) + F(60, 100) * (F(33, 60) - F(18, 40)) == F(51, 100), 'shrunk = 0.45 + 0.6 x 0.10', '')

# ------------------------------------------------------------------ difficulty 5
phi6 = F(588, 200 - 4)
key('e-rejections-dispersion', float(phi6), part=0)
wrong('e-rejections-dispersion', 'n', 588 / 200, part=0)
se = 0.028 * math.sqrt(float(phi6))
key_round('e-rejections-dispersion', se, 4, part=1)
wrong('e-rejections-dispersion', 'phi', 0.028 * float(phi6), part=1)
wrong('e-rejections-dispersion', 'divided', 0.028 / math.sqrt(float(phi6)), part=1)
pq = 2 * (1 - phi(0.072 / se))
key_round('e-rejections-dispersion', pq, 4, part=2)
wrong('e-rejections-dispersion', 'poisson', 2 * (1 - phi(0.072 / 0.028)), part=2)
say('e-rejections-dispersion', 'explain.text', round(2 * (1 - phi(0.072 / 0.028)), 4))
ex.expect('exam', P('e-rejections-dispersion', 2) + '.feedback.correct', round(0.072 / se, 3))
ex.expect('exam', P('e-rejections-dispersion', 2) + '.feedback.byKey.poisson', round(0.072 / 0.028, 3))


# ------------------------------------------------------------------ code items, run in CPython
def run_cases(w, src):
    out = []
    for t in w['tests']:
        ns = {}
        try:
            exec(w.get('prelude', ''), ns)
            exec(src, ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'])
            if t['compare'] == 'isclose':
                ok = abs(got - want) <= t['tol']['abs']
            else:
                ok = got == want
        except Exception:
            ok = False
        out.append(ok)
    return out


def walsh_np(d):
    a = np.array(d, dtype=float)
    i, j = np.triu_indices(len(a))
    return float(np.median((a[i] + a[j]) / 2))


wh = node(W('e-walsh-median'))
ns = {}
exec(wh['prelude'], ns)
for t in wh['tests']:
    arg = eval(t['call'][len('walsh_median('):-1], ns)
    ok = abs(walsh_np(arg) - float(t['expect'])) <= 1e-9
    ex._rec(ok, f'walsh {t["call"][:40]} expect {t["expect"]} by NumPy', '')
ex._rec(abs(walsh_np([1.0, 2.0, 9.0]) - 3.5) < 1e-12, 'walsh [1, 2, 9] = 3.5 by hand', '')
ex._rec(len(wh['tests']) == 7 and '7 hidden tests' in wh['how'], 'walsh how names 7 tests', '')
ex._rec(all(run_cases(wh, wh['solution'])), 'e-walsh-median: solution passes all hidden tests', '')
st = run_cases(wh, wh['starter'])
ex._rec(not any(st), f'e-walsh-median: starter fails all {len(st)} hidden tests', '')


def kw_classic(groups):
    flat = sorted(v for gg in groups for v in gg)
    n = len(flat)
    rank = {}
    for v in set(flat):
        pos = [k + 1 for k, x in enumerate(flat) if x == v]
        rank[v] = F(sum(pos), len(pos))
    h = F(12, n * (n + 1)) * sum(sum(rank[v] for v in gg) ** 2 / len(gg) for gg in groups) - 3 * (n + 1)
    ties = Counter(flat)
    corr = 1 - F(sum(t ** 3 - t for t in ties.values()), n ** 3 - n)
    return float(h / corr)


kw = node(W('e-kruskal-h'))
ns = {}
exec(kw['prelude'], ns)
for t in kw['tests']:
    if t['compare'] != 'isclose':
        continue
    arg = eval(t['call'][len('kruskal_h('):-1], ns)
    ok = abs(kw_classic(arg) - float(t['expect'])) <= 1e-9
    ex._rec(ok, f'kruskal {t["call"][:44]} expect {t["expect"]} by the classic formula', '')
ex._rec(abs(kw_classic([[2, 3, 3, 4], [4, 5, 5, 6], [5, 7, 8, 8]]) - float(kw['tests'][1]['expect'])) < 1e-9, 'brokers H by classic route', '')
ex._rec(len(kw['tests']) == 7 and '7 hidden tests' in kw['how'], 'kruskal how names 7 tests', '')
ex._rec(all(run_cases(kw, kw['solution'])), 'e-kruskal-h: solution passes all hidden tests', '')
st = run_cases(kw, kw['starter'])
ex._rec(not any(st), f'e-kruskal-h: starter fails all {len(st)} hidden tests', '')
ex._rec(max(len(x) for x in ns['SLIP']) == 14, 'SLIP groups of up to 14', '')

ex.check_wrongs()
ex.report()
