"""Recompute every number in app/content/courses/conditional/problems-<n>.json twice.

Method 1 is exact (fractions.Fraction, closed forms). Method 2 is independent: brute
enumeration of the outcomes, a different route through the algebra (odds against
direct Bayes, complements against sums), or natural-frequency counts. For each part
the script checks: the two methods agree; the JSON key equals them within its tol;
every `wrong` value matches its named slip and lies outside the key's band. Choice
parts check the keyed option and the numbers its text states. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-conditional-numbers.py
"""
import json, os, sys, itertools
from fractions import Fraction as F
from math import comb, isclose

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'conditional')
fails, checks = [], 0

def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {it['id']: it for it in d['items']}

def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)

def num(items, iid, k, exact, alt, slips=None, round_tol=0.0005):
    """Part k (1-based) of item iid: a numeric key."""
    if items is None: return
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=1e-9, abs_tol=1e-12), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= max(tol, 1e-12), f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs: continue
        x = wrongs[wid]; wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, round_tol), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    ids = list(wrongs)
    for a, b in itertools.combinations(ids, 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')

def pick(items, iid, k, correct_id):
    if items is None: return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')

# ------------------------------------------------------------------ level 1
L1 = load(1)
# p-eight-sided: two rolls of a fair d8
cells = list(itertools.product(range(1, 9), repeat=2))
ten = [c for c in cells if sum(c) == 10]
eight = [c for c in cells if 8 in c]
both = [c for c in ten if 8 in c]
num(L1, 'p-eight-sided', 1, F(7, 64), F(len(ten), len(cells)),
    {'unordered': F(4, 64), 'double-five': F(8, 64), 'six-sided': F(3, 36)})
num(L1, 'p-eight-sided', 2, F(2, 15), F(len(both), len(eight)),
    {'sixteen': F(2, 16), 'whole': F(2, 64), 'no-news': F(7, 64)})
num(L1, 'p-eight-sided', 3, F(2, 7), F(len(both), len(ten)),
    {'turned': F(2, 15), 'eight-pairs': F(2, 8), 'one-order': F(1, 7)})
num(L1, 'p-eight-sided', 4, F(7, 64) * F(2, 7), F(len(both), len(cells)),
    {'plain-product': F(7, 64) * F(15, 64), 'added': F(7, 64) + F(2, 7), 'eight-slip': F(7, 64) * F(1, 4)})

# p-watchlist: 5 banks, 4 miners, three ordered picks without replacement
stocks = ['B'] * 5 + ['M'] * 4
perms = list(itertools.permutations(range(9), 3))
lab = [''.join(stocks[i] for i in p) for p in perms]
def share(pred, given=lambda s: True):
    g = [s for s in lab if given(s)]
    return F(sum(1 for s in g if pred(s)), len(g))
bbm = F(5, 9) * F(4, 8) * F(4, 7)
num(L1, 'p-watchlist', 1, F(5, 9) * F(4, 8), share(lambda s: s[:2] == 'BB'),
    {'replace': F(5, 9) ** 2, 'fixed-bottom': F(5, 9) * F(4, 9), 'same-count': F(5, 9) * F(5, 8)})
num(L1, 'p-watchlist', 2, F(4, 7), share(lambda s: s[2] == 'M', lambda s: s[:2] == 'BB'),
    {'full-list': F(4, 9), 'one-gone': F(4, 8), 'bank': F(3, 7)})
num(L1, 'p-watchlist', 3, F(5, 18) * F(4, 7), share(lambda s: s == 'BBM'),
    {'replace': F(5, 9) ** 2 * F(4, 9), 'replace-slip': F(5, 9) ** 2 * F(4, 7), 'added': F(5, 18) + F(4, 7)})
num(L1, 'p-watchlist', 4, 3 * bbm, share(lambda s: s.count('B') == 2),
    {'one-order': bbm, 'six-orders': 6 * bbm, 'replace-slip': 3 * F(5, 9) ** 2 * F(4, 9)})
num(L1, 'p-watchlist', 5, bbm / (3 * bbm), share(lambda s: s[2] == 'M', lambda s: s.count('B') == 2),
    {'no-news': F(4, 9), 'not-divided': bbm, 'six-slip': F(1, 6)})

# p-order-router: venues X, Y, Z; one re-send to Y
route = {'X': (F(1, 2), F(3, 5)), 'Y': (F(3, 10), F(4, 5)), 'Z': (F(1, 5), F(9, 10))}
first = sum(p * f for p, f in route.values())
def within_two(paths):   # enumerate first venue, first result, second result
    tot = F(0)
    for v, (p, f) in paths.items():
        for r1, q1 in (('fill', f), ('miss', 1 - f)):
            if r1 == 'fill': tot += p * q1
            else: tot += p * q1 * F(4, 5)
    return tot
num(L1, 'p-order-router', 1, F(1, 2) * F(3, 5), 1 - F(1, 2) - F(1, 2) * F(2, 5),
    {'branch-only': F(3, 5), 'added': F(1, 2) + F(3, 5)})
num(L1, 'p-order-router', 2, first, 1 - sum(p * (1 - f) for p, f in route.values()),
    {'average': (F(3, 5) + F(4, 5) + F(9, 10)) / 3, 'x-only': F(3, 10), 'rates-added': F(23, 10)})
avg = (F(3, 5) + F(4, 5) + F(9, 10)) / 3
num(L1, 'p-order-router', 3, first + (1 - first) * F(4, 5), within_two(route),
    {'both': first * F(4, 5), 'second-only': (1 - first) * F(4, 5), 'average-slip': avg + (1 - avg) * F(4, 5)})
zfirst = F(9, 10) + F(1, 10) * F(4, 5)
num(L1, 'p-order-router', 4, zfirst, within_two({'Z': (F(1), F(9, 10))}),
    {'no-resend': F(9, 10), 'product': F(9, 10) * F(4, 5)})
pick(L1, 'p-order-router', 5, 'z-first')
ok(zfirst - (first + (1 - first) * F(4, 5)) == F(36, 1000), 'router gap is not 0.036')
ok(F(9, 10) - first == F(18, 100), 'first-try gap is not 0.18')

# p-dealer-calls: 4 good of 10, ordered calls without repeats
trip = list(itertools.permutations(range(10), 3))   # first three dealers called
good = set(range(4))
def first_good(t):
    for i, d in enumerate(t):
        if d in good: return i + 1
    return None
dist = {k: F(sum(1 for t in trip if first_good(t) == k), len(trip)) for k in (1, 2, 3, None)}
s2, s3 = F(6, 10) * F(4, 9), F(6, 10) * F(5, 9) * F(4, 8)
within3 = F(4, 10) + s2 + s3
num(L1, 'p-dealer-calls', 1, s2, dist[2],
    {'replace': F(6, 10) * F(4, 10), 'cond-only': F(4, 9)})
num(L1, 'p-dealer-calls', 2, s3, dist[3],
    {'replace': F(6, 10) ** 2 * F(4, 10), 'last-factor': F(4, 8), 'two-misses': F(6, 10) * F(5, 9)})
rep3 = F(4, 10) + F(6, 10) * F(4, 10) + F(6, 10) ** 2 * F(4, 10)
num(L1, 'p-dealer-calls', 3, within3, 1 - dist[None],
    {'replace': rep3, 'no-first': s2 + s3, 'product': F(4, 10) * s2 * s3})
# part 4: given a stop within three calls but not on call 1, the chance of a stop on call 2
num(L1, 'p-dealer-calls', 4, s2 / (within3 - F(4, 10)), dist[2] / (dist[2] + dist[3]),
    {'keeps-call-1': s2 / within3, 'no-news': s2, 'third-call': s3 / (s2 + s3),
     'replace-slip': (F(6, 10) * F(4, 10)) / (rep3 - F(4, 10))})
ok(within3 - F(4, 10) == F(13, 30), 'stop within three but not on call 1 is not 13/30')

# ------------------------------------------------------------------ level 2
L2 = load(2)
# p-takeover-rumour: natural frequencies against Bayes
b, h, f = F(8, 100), F(45, 100), F(6, 100)
N = 5000
tr = N * b * h; fr = (N - N * b) * f
num(L2, 'p-takeover-rumour', 1, tr, sum(1 for i in range(N) if i < 400 and i % 20 < 9),
    {'all-targets': N * b, 'rate-on-all': N * h}, round_tol=0)
num(L2, 'p-takeover-rumour', 2, tr + fr, N * (b * h + (1 - b) * f),
    {'false-on-all': tr + N * f, 'others-only': fr}, round_tol=0)
num(L2, 'p-takeover-rumour', 3, F(180, 456), b * h / (b * h + (1 - b) * f),
    {'inverse': h, 'count-slip': tr / (tr + N * f), 'over-false': tr / fr})
bstar = f / (h + f)
num(L2, 'p-takeover-rumour', 4, bstar, F(6, 51),
    {'no-complement': f / h, 'half': F(1, 2), 'rate-gap': h - f})
ok(h * bstar == f * (1 - bstar), 'break-even base rate does not balance')

# p-downgrade-news: odds updates against direct Bayes over the four news cells
p0 = F(15, 100)
o0 = p0 / (1 - p0)
lr1, lr2 = F(60, 100) / F(20, 100), F(30, 100) / F(5, 100)
direct2 = p0 * F(6, 10) * F(3, 10) / (p0 * F(6, 10) * F(3, 10) + (1 - p0) * F(2, 10) * F(5, 100))
num(L2, 'p-downgrade-news', 1, o0, F(3, 17), {'probability': p0, 'reversed': 1 / o0})
d1 = p0 * F(6, 10) / (p0 * F(6, 10) + (1 - p0) * F(2, 10))
num(L2, 'p-downgrade-news', 2, o0 * lr1, d1 / (1 - d1),
    {'prob-times': p0 * lr1, 'inverse-lr': o0 / lr1, 'rate-gap': o0 + F(4, 10)})
o2 = o0 * lr1 * lr2
slip_o = F(45, 100) / F(55, 100) * lr2
num(L2, 'p-downgrade-news', 3, o2 / (1 + o2), direct2,
    {'odds': o2, 'ratio-sum': o0 * (lr1 + lr2) / (1 + o0 * (lr1 + lr2)), 'prob-slip': slip_o / (1 + slip_o)})
def reports_needed(odds, target):
    k = 0
    while odds < target: odds *= lr1; k += 1
    return k
need = reports_needed(o2, F(95, 5))
alt = next(k for k in range(10) if (o2 * 3 ** k) / (1 + o2 * 3 ** k) >= F(95, 100))
num(L2, 'p-downgrade-news', 4, need, alt,
    {'prob-as-odds': reports_needed(o2, F(95, 100)), 'ninety': 1}, round_tol=0)
ok(o2 * 3 / (1 + o2 * 3) < F(95, 100) and o2 * 3 / (1 + o2 * 3) > F(9, 10), 'one report should land between 0.9 and 0.95')
pick(L2, 'p-downgrade-news', 5, 'not-independent')

# p-broker-algo: three kinds, updated twice
pri = [F(1, 2), F(3, 10), F(1, 5)]
lik = [F(3, 10), F(1, 2), F(4, 5)]
pf = sum(p * l for p, l in zip(pri, lik))
post1 = [p * l / pf for p, l in zip(pri, lik)]
pf2 = sum(p * l for p, l in zip(post1, lik))
post2 = [p * l / pf2 for p, l in zip(post1, lik)]
direct = [p * l * l for p, l in zip(pri, lik)]
direct = [x / sum(direct) for x in direct]
num(L2, 'p-broker-algo', 1, pf, 1 - sum(p * (1 - l) for p, l in zip(pri, lik)),
    {'average': sum(lik) / 3, 'aggressive-only': pri[2] * lik[2]})
num(L2, 'p-broker-algo', 2, post1[2], F(16, 46),
    {'not-normalised': pri[2] * lik[2], 'likelihood': lik[2], 'average-slip': pri[2] * lik[2] / (sum(lik) / 3)})
num(L2, 'p-broker-algo', 3, post2[2], direct[2],
    {'once': post1[2], 'not-normalised': post1[2] * lik[2]})
ok(post1 == [F(15, 46), F(15, 46), F(16, 46)], 'part 3 restates the wrong chances')
ok(post2 == [F(45, 248), F(75, 248), F(128, 248)], 'part 4 restates the wrong chances')
pred = sum(p * l for p, l in zip(post2, lik))
pred_alt = sum(p * l ** 3 for p, l in zip(pri, lik)) / sum(p * l ** 2 for p, l in zip(pri, lik))
num(L2, 'p-broker-algo', 4, pred, pred_alt,
    {'prior-weights': pf, 'most-likely': lik[2], 'equal': sum(lik) / 3})

# p-bad-ticks: two filters, independent given the truth; counts on 1,000,000 prints
e, a1, a0, b1, b0 = F(2, 100), F(95, 100), F(4, 100), F(70, 100), F(1, 100)
pa = e * a1 + (1 - e) * a0
pe_a = e * a1 / pa
oa = e * a1 / ((1 - e) * a0)
pe_ab = oa * (b1 / b0) / (1 + oa * (b1 / b0))
M = 1000000
bad_both, good_both = M * e * a1 * b1, M * (1 - e) * a0 * b0
num(L2, 'p-bad-ticks', 1, pa, F(58200, M),
    {'errors-only': e * a1, 'rates-added': a1 + a0, 'false-on-all': e * a1 + a0}, round_tol=0.0001)
num(L2, 'p-bad-ticks', 2, pe_a, F(19000, 58200),
    {'inverse': a1, 'false-slip': e * a1 / (e * a1 + a0), 'specificity': 1 - a0})
num(L2, 'p-bad-ticks', 3, pe_ab, bad_both / (bad_both + good_both),
    {'odds': oa * b1 / b0, 'product': pe_a * b1, 'skipped-a': (e / (1 - e) * b1 / b0) / (1 + e / (1 - e) * b1 / b0)}, round_tol=0.005)
num(L2, 'p-bad-ticks', 4, good_both, 980000 * F(4, 100) * F(1, 100),
    {'a-only': M * (1 - e) * a0, 'all-prints': M * a0 * b0}, round_tol=0.3)
num(L2, 'p-bad-ticks', 5, good_both / (bad_both + good_both), 1 - pe_ab,
    {'over-all': good_both / M, 'over-errors': good_both / bad_both, 'error-share': pe_ab}, round_tol=0.0002)
ok(bad_both == 13300 and good_both == 392, 'prints flagged by both are not 13,300 errors and 392 good')
ok(M * (1 - e) * a0 == 39200 and M * a0 * b0 == 400, 'part 4 slips are not 39,200 and 400')

# ------------------------------------------------------------------ level 3
L3 = load(3)
# p-gap-days: 400 days, 120 gaps, 260 up, 78 both
q = F(78, 120)
seqs = list(itertools.product([1, 0], repeat=4))
def pseq(s, p):
    r = F(1)
    for x in s: r *= p if x else 1 - p
    return r
num(L3, 'p-gap-days', 1, q, F(78, 400) / F(120, 400),
    {'over-all': F(78, 400), 'reversed': F(78, 260)})
pick(L3, 'p-gap-days', 2, 'yes')
ok(F(260, 400) == q and F(120, 400) * F(260, 400) == F(78, 400), 'gap and up are not independent in the sample')
qj = F(78, 400)
num(L3, 'p-gap-days', 3, comb(4, 3) * q ** 3 * (1 - q), sum(pseq(s, q) for s in seqs if sum(s) == 3),
    {'one-path': q ** 3 * (1 - q), 'all-four': q ** 4, 'joint-slip': 4 * qj ** 3 * (1 - qj)})
num(L3, 'p-gap-days', 4, 1 - q ** 4, sum(pseq(s, q) for s in seqs if sum(s) < 4),
    {'sum': 4 * (1 - q), 'exactly-one': 4 * q ** 3 * (1 - q), 'all-down': (1 - q) ** 4})

# p-losing-week: loss = fail or squeeze, independent causes
pfl, psq = F(3, 10), F(1, 4)
states = {(a, b): (pfl if a else 1 - pfl) * (psq if b else 1 - psq) for a in (0, 1) for b in (0, 1)}
ploss = sum(p for (a, b), p in states.items() if a or b)
num(L3, 'p-losing-week', 1, 1 - (1 - pfl) * (1 - psq), ploss,
    {'sum': pfl + psq, 'both': pfl * psq})
num(L3, 'p-losing-week', 2, pfl / ploss, sum(p for (a, b), p in states.items() if a) / ploss,
    {'no-news': pfl, 'sum-slip': pfl / (pfl + psq), 'times': pfl * ploss})
given = {k: p for k, p in states.items() if (k[0] or k[1]) and k[1]}
num(L3, 'p-losing-week', 3, pfl, sum(p for k, p in given.items() if k[0]) / sum(given.values()),
    {'still': pfl / ploss, 'cancelled': 0, 'over-loss': pfl * psq / ploss})
pick(L3, 'p-losing-week', 4, 'no')
ok(round(float(pfl / ploss), 2) == 0.63, 'choice text 0.63 does not match')

# p-three-loans: regimes, independent inside each
r, pb, pg = F(1, 4), F(28, 100), F(4, 100)
one = r * pb + (1 - r) * pg
all3 = r * pb ** 3 + (1 - r) * pg ** 3
enum_all = F(0)
for reg, pr, pd in (('rec', r, pb), ('norm', 1 - r, pg)):
    for s in itertools.product([1, 0], repeat=3):
        if all(s): enum_all += pr * pseq(s, pd)
num(L3, 'p-three-loans', 1, one, 1 - (r * (1 - pb) + (1 - r) * (1 - pg)),
    {'average': (pb + pg) / 2, 'recession-only': r * pb})
num(L3, 'p-three-loans', 2, all3, enum_all,
    {'independent': one ** 3, 'no-weights': pb ** 3 + pg ** 3, 'cube-average': ((pb + pg) / 2) ** 3}, round_tol=0.00001)
num(L3, 'p-three-loans', 3, one ** 3, pseq((1, 1, 1), one),
    {'sum': 3 * one, 'squared': one ** 2}, round_tol=0.00001)
num(L3, 'p-three-loans', 4, all3 / one ** 3, enum_all * 1000,
    {'reciprocal': one ** 3 / all3, 'difference': all3 - one ** 3, 'weights-slip': (pb ** 3 + pg ** 3) / one ** 3}, round_tol=0.005)

# p-odd-dice (three desks, feeds P, Q, R): A desk 1 calm (P = Q), B desk 2 calm (P = R), C desk 3 calm (Q = R)
feeds = list(itertools.product((0, 1), repeat=3))
A = {x for x in feeds if x[0] == x[1]}; B = {x for x in feeds if x[0] == x[2]}; C = {x for x in feeds if x[1] == x[2]}
P = lambda S: F(len(S), 8)
num(L3, 'p-odd-dice', 1, F(1, 2), F(len(A & C), len(A)), {'joint': P(A & C), 'certain': 1})
pick(L3, 'p-odd-dice', 2, 'pairwise')
ok(P(A) == P(B) == P(C) == F(1, 2), 'each desk is not calm with chance 1/2')
ok(all(P(X & Y) == P(X) * P(Y) for X, Y in ((A, B), (A, C), (B, C))), 'pairs are not independent')
ok(P(A & B & C) != P(A) * P(B) * P(C), 'the three are mutually independent')
num(L3, 'p-odd-dice', 3, F(1, 4), P(A & B & C), {'product': F(1, 8), 'single': P(C)})
num(L3, 'p-odd-dice', 4, F(1), F(len(A & B & C), len(A & B)), {'pairwise': F(1, 2), 'joint': F(1, 4)})
tri = P(A & B & C)
num(L3, 'p-odd-dice', 5, 1 - (1 - tri) ** 8, sum(comb(8, k) * tri ** k * (1 - tri) ** (8 - k) for k in range(1, 9)),
    {'product-slip': 1 - F(7, 8) ** 8, 'sum': 8 * tri, 'complement': (1 - tri) ** 8})

# every numeric part: form stated, a value rounded as asked is accepted, and each value the part's own feedback prints is accepted
import re
def form_checks(sets):
    for ref, items in sets:
        if items is None: continue
        for iid, it in items.items():
            for k, p in enumerate(it['parts'], 1):
                w = p['widget']
                if w['kind'] != 'numeric': continue
                tag = f'{ref} {iid} p{k}'
                a, tol, q = w['answer'], w['tol'].get('abs', 0), p['question']
                whole = float(a).is_integer() and tol == 0
                ok(whole or w.get('unit') == '£' or bool(re.search(r'\bGive\b', q)), f'{tag}: no sentence stating the form wanted')
                m = re.search(r'(\d+) decimal places?|decimal to (\d+) places?', q)
                if m:
                    n = int(m.group(1) or m.group(2))
                    ok(tol + 1e-12 >= 0.5 * 10 ** -n, f'{tag}: tolerance {tol} rejects a value rounded to {n} places')
                texts = [p['feedback'].get('correct', ''), p['explain']['text'], w.get('accept', '')]
                for t in texts:
                    t = t.replace('{,}', '').replace(',', '').replace('£', '')
                    for v in re.findall(r'(?:\\approx|about) \$?(-?\d+\.?\d*)', t):
                        v = float(v.rstrip('.'))
                        if a and not whole and abs(v - a) <= 0.05 * abs(a):
                            ok(abs(v - a) <= tol + 1e-9, f'{tag}: prints {v} but the key {a} (tol {tol}) rejects it')
form_checks([('problems-1', L1), ('problems-2', L2), ('problems-3', L3)])

present = [n for n in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails: print('FAIL', m)
sys.exit(1 if fails else 0)
