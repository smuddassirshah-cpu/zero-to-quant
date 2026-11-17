#!/usr/bin/env python3
"""Second reader's recompute for the nine new items of exams topic-1.6 to topic-1.11 (session AG).

Every key, `wrong` value and printed number is recomputed by a method the
author's script does not lean on: Fractions and a weighted-average form for the
Beta posteriors, a two-state linear solve and the risk-neutral price for the
copy, bisection for the yield and the break-evens, a summed dividend stream,
a literal run of the backtracking search beside a 3^6 enumeration, each C++
test of `e-swapped-d` run against a correct and a swapped pricer, a moment
system for the quadrature weights, and `cmath` for the square root.
The pairs and the removals are recounted from the exam and course files.
The last block recomputes the numbers of the fixes proposed in
docs/reviews/review-exam-second-item-1.6-1.11.md.

A failing check prints a FINDING line.  Exit 0 unless the script itself breaks.
"""
import cmath
import collections
import glob
import itertools
import json
import math
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CONTENT = os.path.join(ROOT, 'app', 'content')
EXAMS = ['topic-1.6', 'topic-1.7', 'topic-1.8', 'topic-1.9', 'topic-1.10', 'topic-1.11']
EX = {e: json.load(open(os.path.join(CONTENT, 'exams', e + '.json'), encoding='utf-8')) for e in EXAMS}
IT = {e: {it['id']: it for it in EX[e]['items']} for e in EXAMS}
NEW = {'topic-1.6': {'s-three-traders': ['es-bayes']},
       'topic-1.7': {'e-ratio-spread': ['op-strategies', 'op-payoff'], 'e-capped-copy': ['tp-replicate'],
                     'e-zero-yield': ['fi-bonds'], 'e-just-paid': ['fi-equity']},
       'topic-1.8': {'e-venue-split': ['gd-backtrack']},
       'topic-1.9': {'e-swapped-d': ['cx-testing']},
       'topic-1.10': {'e-integral-weights': ['lx-dual']},
       'topic-1.11': {'e-square-root-parts': ['cz-arith']}}
REMOVED = {'topic-1.6': {'s-alpha-beta-table': ['rg-inference']},
           'topic-1.7': {'e-book-delta': ['op-greeks'], 'e-one-step-q': ['tp-riskneutral'],
                         'e-parity-put': ['op-parity'], 'e-short-sale': ['fi-forwards']},
           'topic-1.8': {},
           'topic-1.9': {'e-virtual-dtor': ['cp-classes']},
           'topic-1.10': {'e-cube-delta': ['an-continuity']},
           'topic-1.11': {'e-integrating-factor': ['de-first']}}
PAIRS = {'topic-1.6': ['es-bayes'], 'topic-1.7': ['op-payoff', 'op-strategies', 'fi-bonds', 'fi-equity', 'tp-replicate'],
         'topic-1.8': ['gd-backtrack'], 'topic-1.9': ['cx-testing'], 'topic-1.10': ['lx-dual'], 'topic-1.11': ['cz-arith']}
COUNT = {'topic-1.6': 30, 'topic-1.7': 30, 'topic-1.8': 29, 'topic-1.9': 30, 'topic-1.10': 30, 'topic-1.11': 30}
MINUTES = {'topic-1.6': 70, 'topic-1.7': 70, 'topic-1.8': 60, 'topic-1.9': 75, 'topic-1.10': 100, 'topic-1.11': 100}

n_ok = n_bad = 0


def check(name, cond, detail=''):
    global n_ok, n_bad
    if cond:
        n_ok += 1
        print('ok      ', name, detail)
    else:
        n_bad += 1
        print('FINDING ', name, detail)


def near(a, b, eps=1e-9):
    return abs(a - b) <= eps


def text(node):
    out = []

    def walk(n):
        if isinstance(n, str):
            out.append(n)
        elif isinstance(n, list):
            for v in n:
                walk(v)
        elif isinstance(n, dict):
            for v in n.values():
                walk(v)
    walk(node)
    return ' '.join(out)


def band(w):
    return w['answer'], w['tol']['abs']


def numeric(name, w, exact, printed, slips, dp):
    """Key band takes the exact and the printed value, refuses every slip; slips are the modelled ones; no tie."""
    key, tol = band(w)
    check(name + ': key', abs(exact - key) <= tol and abs(printed - key) <= tol, f'exact {exact:.6f} printed {printed} key {key} tol {tol}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(name + ': slip ids', set(got) == set(slips), f'{sorted(got)} against {sorted(slips)}')
    for sid, val in slips.items():
        if sid not in got:
            continue
        x = got[sid]
        check(f'{name}: slip {sid}', abs(val - x['value']) <= x['tol']['abs'] and abs(x['value'] - key) > tol + x['tol']['abs'],
              f'modelled {val:.6f} keyed {x["value"]}')
    vals = [key] + [x['value'] for x in w.get('wrong', [])]
    tols = [tol] + [x['tol']['abs'] for x in w.get('wrong', [])]
    check(name + ': bands disjoint', all(abs(vals[i] - vals[j]) > tols[i] + tols[j] for i in range(len(vals)) for j in range(i)))
    scaled = exact * 10 ** dp
    check(name + ': no rounding tie', abs(scaled - math.floor(scaled) - 0.5) > 0.02 or near(scaled, round(scaled), 1e-7), f'{scaled:.4f}')


# ---------------------------------------------------------------- pairs, counts, removals
print('== pairs and removals')
courses = {}
for f in glob.glob(os.path.join(CONTENT, 'courses', '*', 'course.json')):
    courses[os.path.basename(os.path.dirname(f))] = json.load(open(f, encoding='utf-8'))
for e in EXAMS:
    ex = EX[e]
    topic = e.split('-', 1)[1]
    auto = collections.defaultdict(list)
    for it in ex['items']:
        if it.get('kind') != 'longform':
            for s in it.get('skills', []):
                auto[s].append((it['id'], it.get('difficulty')))
    ess = collections.defaultdict(list)
    for folder, d in courses.items():
        if str(d.get('topic')) != topic:
            continue
        for lv in d.get('levels', []):
            p = os.path.join(CONTENT, 'courses', folder, str(lv.get('review')) + '.json')
            if not lv.get('review') or not os.path.exists(p):
                continue
            for it in json.load(open(p, encoding='utf-8')).get('items', []):
                for s in it.get('skills', []):
                    ess[s].append(f'{folder}/L{lv["n"]}')
    check(f'{e}: {COUNT[e]} items, {MINUTES[e]} minutes', len(ex['items']) == COUNT[e] and ex.get('minutes') == MINUTES[e],
          f'{len(ex["items"])} items, {ex.get("minutes")} min')
    check(f'{e}: no essential skill with fewer than two auto items', all(len(auto[s]) >= 2 for s in ess),
          str({s: len(auto[s]) for s in ess if len(auto[s]) < 2}))
    check(f'{e}: no skill of the exam with fewer than two auto items', all(len(v) >= 2 for v in auto.values()),
          str({s: len(v) for s, v in auto.items() if len(v) < 2}))
    for s in PAIRS[e]:
        new_on = [i for i, sk in NEW[e].items() if s in sk]
        check(f'{e}: pair {s} is essential, had one auto item, now has two',
              s in ess and len(auto[s]) == 2 and len(new_on) == 1 and s in IT[e][new_on[0]]['skills'], f'{auto[s]} {sorted(set(ess[s]))}')
    for i, sk in NEW[e].items():
        check(f'{e}: {i} present with skills {sk}', i in IT[e] and IT[e][i]['skills'] == sk and IT[e][i].get('kind') != 'longform')
    for i, sk in REMOVED[e].items():
        check(f'{e}: {i} removed', i not in IT[e])
        for s in sk:
            left = sorted(d for _, d in auto[s])
            check(f'{e}: {s} keeps at least two auto items after {i} went', len(left) >= 2, str(left))
            check(f'{e}: {s} is not left with only its hardest items (some item at difficulty 3 or less)', min(left) <= 3, str(left))
    for s in PAIRS[e]:
        left = sorted(d for _, d in auto[s])
        check(f'{e}: pair {s} has an item at difficulty 3 or less', min(left) <= 3, str(left))
check('topic-1.8 minutes: 60 x 29 / 28 rounds to 60', 5 * round(60 * 29 / 28 / 5) == 60, f'{60 * 29 / 28:.2f}')

# ---------------------------------------------------------------- topic-1.6 s-three-traders
print('== topic-1.6 s-three-traders')
it = IT['topic-1.6']['s-three-traders']
a0, b0 = 22, 18
rec = {'ash': (9, 10), 'bea': (46, 60), 'cal': (101, 150)}
post = {k: F(a0 + w, a0 + b0 + n) for k, (w, n) in rec.items()}
# second form: weight n/(a+b+n) on the raw rate, the rest on the prior mean
post2 = {k: F(n, a0 + b0 + n) * F(w, n) + F(a0 + b0, a0 + b0 + n) * F(a0, a0 + b0) for k, (w, n) in rec.items()}
check('prior Beta(22, 18): mean 55%, worth 40 trades', F(a0, a0 + b0) == F(55, 100) and a0 + b0 == 40)
check('posterior means 31/50, 68/100, 123/190 by both forms', post == post2 and post['ash'] == F(31, 50) and post['bea'] == F(68, 100) and post['cal'] == F(123, 190), str(post))
check('means print as 0.62, 0.68 and 0.647', [round(float(post[k]), 3) for k in ('ash', 'bea', 'cal')] == [0.62, 0.68, 0.647])
opt = {o['id']: o for o in it['widget']['options']}
check('key is Bea, and only Bea', max(post, key=post.get) == 'bea' and [k for k, o in opt.items() if o.get('correct')] == ['bea'])
check('raw top is Ash at 90%; longest record is Cal', max(rec, key=lambda k: F(*rec[k])) == 'ash' and F(9, 10) == F(90, 100) and max(rec, key=lambda k: rec[k][1]) == 'cal')
check('Bea raw rate prints as 77%', round(100 * 46 / 60) == 77, f'{100 * 46 / 60:.2f}')
check('posteriors Beta(31, 19), Beta(68, 32), Beta(123, 67) in the explanation',
      all(s in it['explain']['text'] for s in ('(31, 19)', '(68, 32)', '(123, 67)')) and (31 + 19, 68 + 32, 123 + 67) == (50, 100, 190))
check('no two posterior means tie', len(set(post.values())) == 3 and min(abs(float(x - y)) for x, y in itertools.combinations(post.values(), 2)) > 0.02)

# ---------------------------------------------------------------- topic-1.7 e-capped-copy
print('== topic-1.7 e-capped-copy')
it = IT['topic-1.7']['e-capped-copy']
S0, Su, Sd, R, cap = F(40), F(50), F(35), F(1025, 1000), F(44)
pu, pd = min(Su, cap), min(Sd, cap)
det = Su * R - Sd * R                                  # Cramer on  D*Su + B*R = pu,  D*Sd + B*R = pd
D = (pu * R - pd * R) / det
B = (Su * pd - Sd * pu) / det
q = (S0 * R - Sd) / (Su - Sd)
price_rn = (q * pu + (1 - q) * pd) / R
check('note pays 44 or 35; no arbitrage 35 < 41 < 50', (pu, pd) == (44, 35) and Sd < S0 * R < Su)
check('copy: 0.6 shares, cash 13.66 lent (positive)', D == F(3, 5) and round(float(B), 2) == 13.66 and B > 0, f'{float(D)} {float(B):.4f}')
check('cash in a year 14.00; shares 30.00 or 21.00', B * R == 14 and D * Su == 30 and D * Sd == 21)
check('note worth 37.66 by the copy and by q = 0.4', round(float(D * S0 + B), 2) == 37.66 and D * S0 + B == price_rn and q == F(2, 5), f'{float(price_rn):.4f}')
check('spread 9.00 over 15.00 in the generic feedback', pu - pd == 9 and Su - Sd == 15)
holds = {'a': (F(3, 5), F(1366, 100)), 'b': (F(3, 5), F(14)), 'c': (F(1), F(0)), 'd': (F(3, 5), -F(1366, 100))}
ok = {k: abs(float(d * Su + b * R - pu)) < 0.005 and abs(float(d * Sd + b * R - pd)) < 0.005 for k, (d, b) in holds.items()}
opt = {o['id']: o for o in it['widget']['options']}
check('only option a copies the note in both states (to the penny)', ok == {'a': True, 'b': False, 'c': False, 'd': False}
      and [k for k, o in opt.items() if o.get('correct')] == ['a'], str(ok))
check('option texts hold 0.6, 13.66, 14.00 as modelled', '0.6 shares and lend £13.66' in opt['a']['text'] and '£14.00' in opt['b']['text']
      and '1 share' in opt['c']['text'] and 'borrow £13.66' in opt['d']['text'])
check('canvas labels the note 44 and 35', 'note £44' in text(it['canvas']) and 'note £35' in text(it['canvas']))

# ---------------------------------------------------------------- topic-1.7 e-zero-yield
print('== topic-1.7 e-zero-yield')
it = IT['topic-1.7']['e-zero-yield']
lo, hi = 0.0, 1.0
for _ in range(200):                                   # bisection on 70 (1 + y)^8 = 100
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 70 * (1 + mid) ** 8 < 100 else (lo, mid)
y = (lo + hi) / 2
check('bisection agrees with the closed form', near(y, (100 / 70) ** 0.125 - 1, 1e-12), f'{y:.8f}')
numeric('part 1 yield', it['parts'][0]['widget'], y, 0.0456,
        {'simple': 30 / 70 / 8, 'on-face': 30 / 100 / 8, 'inverted': 1 - 0.7 ** 0.125}, 4)
check('part 1 slips print as 5.36% and the unit is %', round(100 * 30 / 70 / 8, 2) == 5.36 and it['parts'][0]['widget'].get('unit') == '%')
p1 = 100 / (1 + y) ** 7
numeric('part 2 price in a year', it['parts'][1]['widget'], p1, 73.19, {'still-eight': 70.0, 'straight-line': 70 + 30 / 8}, 2)
check('part 2: the printed route 100/1.0456^7 and 70 x 1.0456 both land in the band',
      abs(100 / 1.0456 ** 7 - 73.19) <= 0.006 and abs(70 * 1.0456 - 73.19) <= 0.006 and near(p1, 70 * (1 + y), 1e-9),
      f'{100 / 1.0456 ** 7:.4f} {70 * 1.0456:.4f} {p1:.4f}')
check('part 2: a learner who carries the simple-interest slip lands on the straight-line key', near(70 * (1 + 30 / 70 / 8), 73.75))

# ---------------------------------------------------------------- topic-1.7 e-ratio-spread
print('== topic-1.7 e-ratio-spread')
it = IT['topic-1.7']['e-ratio-spread']
LEGS = [('call', +1, 80.0, 5.40), ('call', -2, 90.0, 1.90)]


def profit(s, legs=LEGS, premiums=True):
    tot = 0.0
    for _, qty, k, prem in legs:
        tot += qty * (max(s - k, 0.0) - (prem if premiums else 0.0))
    return tot


def root(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


canvas_legs = it['canvas']['params']['legs']
check('canvas legs match the prose: long 80 call at 5.40, two short 90 calls at 1.90, break-even markers off, no spot readout',
      [(leg['side'], leg['strike'], leg['premium'], leg.get('qty', 1)) for leg in canvas_legs] == [('long', 80, 5.4, 1), ('short', 90, 1.9, 2)]
      and it['canvas']['state'].get('breakeven') is False and 'spot' not in it['canvas']['state'] and it['canvas']['params'].get('pl') is True)
check('net cost 1.60', near(-profit(0.0), 1.60))
numeric('part 1 profit at 95', it['parts'][0]['widget'], profit(95.0), 3.40,
        {'one-short': profit(95.0, [LEGS[0], ('call', -1, 90.0, 3.80)]),          # one short call, both premiums kept
         'no-premium': profit(95.0, premiums=False),
         'added-premiums': profit(95.0, premiums=False) - (5.40 + 2 * 1.90)}, 2)
upper = root(profit, 90.0, 120.0)
lower = root(profit, 80.0, 90.0)
numeric('part 2 upper break-even', it['parts'][1]['widget'], upper, 98.40,
        {'payoff-zero': root(lambda s: profit(s, premiums=False), 95.0, 120.0), 'lower': lower, 'plus-cost': 100 + 1.60}, 2)
check('profit falls above 90 and peaks there at 8.40; lower break-even 81.60', near(profit(90.0), 8.40) and near(lower, 81.60, 1e-6)
      and all(profit(90 + i / 10) > profit(90 + (i + 1) / 10) for i in range(300)))
check('printed: payoff 15 - 2 x 5 = 5 at 95; payoff 100 - S and profit 98.40 - S above 90',
      near(profit(95.0, premiums=False), 5.0) and all(near(profit(s), 98.40 - s) and near(profit(s, premiums=False), 100 - s) for s in (90.0, 93.5, 110.0)))
check('two-skill test: one leg alone gives neither key (long call 9.60, the short pair -6.20)',
      near(profit(95.0, [LEGS[0]]), 9.60) and near(profit(95.0, [LEGS[1]]), -6.20) and abs(9.60 - 3.40) > 1 and abs(-6.20 - 3.40) > 1)

# ---------------------------------------------------------------- topic-1.7 e-just-paid
print('== topic-1.7 e-just-paid')
it = IT['topic-1.7']['e-just-paid']


def stream(d_last, g, r, years=4000):
    return sum(d_last * ((1 + g) / (1 + r)) ** t for t in range(1, years + 1))


val = stream(1.50, 0.04, 0.10)
check('summed dividend stream agrees with D1/(r - g)', near(val, 1.56 / 0.06, 1e-6), f'{val:.6f}')
numeric('share value', it['widget'], val, 26.00, {'last-div': 1.50 / 0.06, 'no-growth': 1.56 / 0.10, 'plus-g': 1.56 / 0.14}, 2)
check('next dividend 1.56 and r - g = 0.06 as printed', near(1.50 * 1.04, 1.56) and near(0.10 - 0.04, 0.06))

# ---------------------------------------------------------------- topic-1.8 e-venue-split
print('== topic-1.8 e-venue-split')
it = IT['topic-1.8']['e-venue-split']
edges = {(int(ed['from']), int(ed['to'])) for ed in it['canvas']['params']['edges']}
check('graph: six orders, seven undirected links', len(it['canvas']['params']['nodes']) == 6
      and edges == {(1, 2), (1, 4), (1, 5), (2, 4), (2, 6), (3, 6), (4, 6)} and all(ed.get('directed') is False for ed in it['canvas']['params']['edges']))
adj = collections.defaultdict(set)
for u, v in edges:
    adj[u].add(v)
    adj[v].add(u)
trace = []


def search(order, col, found, stop_first):
    if order == 7:
        found.append(''.join(col[i] for i in range(1, 7)))
        return stop_first
    free = [c for c in 'ABC' if all(col.get(nb) != c for nb in adj[order] if nb < order)]
    if not free:
        trace.append((order, ''.join(col[i] for i in range(1, order))))
    for c in free:
        col[order] = c
        if search(order + 1, col, found, stop_first):
            return True
        del col[order]
    return False


first = []
search(1, {}, first, True)
alls = []
search(1, {}, alls, False)
brute = [''.join(p) for p in itertools.product('ABC', repeat=6) if all(p[u - 1] != p[v - 1] for u, v in edges)]
opt = {o['id']: o for o in it['parts'][0]['widget']['options']}
as_text = lambda s: ', '.join(s)
check('first full assignment is A, B, B, C, B, A and it is the keyed option', as_text(first[0]) == 'A, B, B, C, B, A' == opt['a']['text'] and opt['a'].get('correct') is True)
check('first dead end: order 6 after A, B, A, C, B; then order 5 on C fails too', trace[0] == (6, 'ABACB') and trace[1] == (6, 'ABACC'), str(trace[:3]))
check('order 4 has one venue only, so the search moves order 3 to B', first[0][2] == 'B' and [c for c in 'ABC' if c not in ('A', 'B')] == ['C'])
check('full search records 24, the brute-force count over 3^6 = 729', len(alls) == 24 == len(brute) and sorted(alls) == sorted(brute) and 3 ** 6 == 729)
check('search order is dictionary order, so the key is the least valid assignment', alls == sorted(alls) and first[0] == min(brute))
w = it['parts'][1]['widget']
check('part 2 key 24, slips 729 and 4 (24 / 3!)', w['answer'] == 24 and w['tol']['abs'] == 0
      and {x['id']: x['value'] for x in w['wrong']} == {'all-leaves': 729, 'up-to-names': 24 // 6})
check('6 x 2 x 2: triangle 1, 2, 4; order 6 forced to order 1; orders 3 and 5 two each',
      len({(s[0], s[1], s[3]) for s in brute}) == 6 and all(s[5] == s[0] for s in brute) and len({(s[2], s[4]) for s in brute if s.startswith('AB')}) == 4)
first_b = min(s for s in brute if s[0] == 'B')
first_ac = min(s for s in brute if s[:2] == 'AC')
check('distractors: least assignment with order 1 on B, least with order 2 on C, a later valid one; all valid, none the key',
      as_text(first_b) == opt['first']['text'] and as_text(first_ac) == opt['neighbour']['text']
      and opt['later']['text'].replace(', ', '') in brute and opt['later']['text'].replace(', ', '') > first[0]
      and opt['later']['text'].replace(', ', '')[:4] == first[0][:4], f'{first_b} {first_ac}')
check('exactly one correct option', sum(1 for o in opt.values() if o.get('correct')) == 1)

# ---------------------------------------------------------------- topic-1.9 e-swapped-d
print('== topic-1.9 e-swapped-d')
it = IT['topic-1.9']['e-swapped-d']
Phi = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))


def d12(s, k, r, sig, t):
    d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
    return d1, d1 - sig * math.sqrt(t)


def call_ok(s, k, r, sig, t):
    d1, d2 = d12(s, k, r, sig, t)
    return s * Phi(d1) - k * math.exp(-r * t) * Phi(d2)


def call_swapped(s, k, r, sig, t):
    d1, d2 = d12(s, k, r, sig, t)
    return s * Phi(d2) - k * math.exp(-r * t) * Phi(d1)


def put_ok(s, k, r, sig, t):
    d1, d2 = d12(s, k, r, sig, t)
    return k * math.exp(-r * t) * Phi(-d2) - s * Phi(-d1)


fwd = 100 - 100 * math.exp(-0.05)
TESTS = {'known': lambda c: abs(c(100, 100, 0.05, 0.2, 1) - 10.4506) <= 1e-4,
         'parity': lambda c: abs(c(100, 100, 0.05, 0.2, 1) - put_ok(100, 100, 0.05, 0.2, 1) - fwd) <= 1e-9,
         'bounds': lambda c: 0 <= c(100, 100, 0.05, 0.2, 1) <= 100,
         'limit': lambda c: abs(c(100, 100, 0.05, 1e-8, 1) - fwd) <= 1e-6,
         'finite': lambda c: math.isfinite(c(100, 100, 0.05, 0.2, 1))}
opt = {o['id']: o for o in it['widget']['options']}
d1, d2 = d12(100, 100, 0.05, 0.2, 1)
sw = call_swapped(100, 100, 0.05, 0.2, 1)
check('d1 = 0.35, d2 = 0.15; correct call 10.4506', near(d1, 0.35) and near(d2, 0.15) and round(call_ok(100, 100, 0.05, 0.2, 1), 4) == 10.4506)
check('swapped call prints as -4.62', round(sw, 2) == -4.62, f'{sw:.5f}')
check('every test passes on the correct pricer', all(t(call_ok) for t in TESTS.values()), str({k: t(call_ok) for k, t in TESTS.items()}))
fails = {k: not t(call_swapped) for k, t in TESTS.items()}
check('tests that fail on the swap are exactly the keyed options', set(opt) == set(TESTS) and all(bool(opt[k].get('correct')) == fails[k] for k in TESTS), str(fails))
check('option code holds the modelled inputs and tolerances', '10.4506, 1e-4' in opt['known']['text'] and 'c - p, f, 1e-9' in opt['parity']['text']
      and 'c >= 0 && c <= 100' in opt['bounds']['text'] and '1e-8' in opt['limit']['text'] and '1e-6' in opt['limit']['text'] and 'isfinite' in opt['finite']['text'])
check('the swap always lowers the call: swapped = correct - (S + K e^{-rT})(N(d1) - N(d2))',
      near(sw, call_ok(100, 100, 0.05, 0.2, 1) - (100 + 100 * math.exp(-0.05)) * (Phi(d1) - Phi(d2)), 1e-9))
prose = it['prose'] + ' ' + it['question']
check('source: the prose gives the normal values the bounds option needs (N(0.35), N(0.15))', '0.6368' in prose and '0.5596' in prose,
      'the learner must judge the sign of 100 N(0.15) - 95.12 N(0.35) with no table')
check('explanation figures recompute from the digits it prints: 100 N(0.15) - 95.12 N(0.35) rounds to -4.62',
      round(100 * Phi(0.15) - 95.12 * Phi(0.35), 2) == -4.62, f'{100 * Phi(0.15) - 95.12 * Phi(0.35):.4f} with 95.12; {100 * Phi(0.15) - 95.123 * Phi(0.35):.4f} with 95.123')

# ---------------------------------------------------------------- topic-1.10 e-integral-weights
print('== topic-1.10 e-integral-weights')
it = IT['topic-1.10']['e-integral-weights']
nodes = [F(0), F(1), F(3)]
moments = [F(3 ** (k + 1), k + 1) for k in range(3)]     # integral of x^k over [0, 3]
# exactness on 1, x, x^2:  sum c_j node_j^k = moment_k ; Gauss-Jordan over Fractions
M = [[n ** k for n in nodes] + [moments[k]] for k in range(3)]
for c in range(3):
    piv = next(r for r in range(c, 3) if M[r][c] != 0)
    M[c], M[piv] = M[piv], M[c]
    M[c] = [v / M[c][c] for v in M[c]]
    for r in range(3):
        if r != c:
            M[r] = [a - M[r][c] * b for a, b in zip(M[r], M[c])]
wts = [M[r][3] for r in range(3)]
rows = it['widget']['rows']
check('weights 0, 9/4, 3/4 from the moment system', wts == [F(0), F(9, 4), F(3, 4)], str(wts))
check('cells keyed 0, 2.25, 0.75 with band 0.001', [(r[1]['answer'], r[1]['tol']['abs']) for r in rows] == [(0, 0.001), (2.25, 0.001), (0.75, 0.001)])
check('slip cell value 1 sits outside every key band', all(abs(x['value'] - r[1]['answer']) > 0.002 and x['value'] == 1 for r in rows for x in r[1]['wrong']))
check('weights sum to 3; check on x^2: 2.25 + 0.75 x 9 = 9', sum(wts) == 3 and wts[1] * 1 + wts[2] * 9 == 9 == moments[2])
check('equal weights of 1 give 4 on p = x, against 4.5', sum(nodes) == 4 and moments[1] == F(9, 2))


def lag_int(j):                                        # integral of the Lagrange polynomial, as a check on the printed forms
    others = [n for i, n in enumerate(nodes) if i != j]
    den = (nodes[j] - others[0]) * (nodes[j] - others[1])
    # (x - a)(x - b) = x^2 - (a + b) x + ab
    return (moments[2] - (others[0] + others[1]) * moments[1] + others[0] * others[1] * moments[0]) / den, den


check('Lagrange forms: denominators 3, -2, 6 and integrals 0, 2.25, 0.75', [lag_int(j) for j in range(3)] == [(F(0), 3), (F(9, 4), -2), (F(3, 4), 6)])

# ---------------------------------------------------------------- topic-1.11 e-square-root-parts
print('== topic-1.11 e-square-root-parts')
it = IT['topic-1.11']['e-square-root-parts']
w = it['widget']
rt = cmath.sqrt(15 - 8j)
ints = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if a * a - b * b == 15 and 2 * a * b == -8]
check('principal root 4 - i, the one with positive real part; integer search finds 4 - i and -4 + i only',
      near(rt.real, 4) and near(rt.imag, -1) and sorted(ints) == [(-4, 1), (4, -1)] and w['answer'] == '4-i' and w.get('form') == 'rectangular')
check('polar route agrees: modulus 17, half the argument', near(abs(15 - 8j), 17) and abs(cmath.rect(math.sqrt(17), cmath.phase(15 - 8j) / 2) - (4 - 1j)) < 1e-12)
sq = {'conjugate': (4 + 1j) ** 2, 'negative': (-4 + 1j) ** 2, 'swapped': (1 - 4j) ** 2}
check('slips: (4 + i)^2 = 15 + 8i, (-4 + i)^2 = 15 - 8i, (1 - 4i)^2 = -15 - 8i',
      sq == {'conjugate': 15 + 8j, 'negative': 15 - 8j, 'swapped': -15 - 8j} and {x['id']: x['tex'] for x in w['wrong']} == {'conjugate': '4+i', 'negative': '-4+i', 'swapped': '1-4i'})
check('quartic a^4 - 15 a^2 - 16 = (a^2 - 16)(a^2 + 1); a = 4 gives b = -1', all(a ** 4 - 15 * a ** 2 - 16 == (a * a - 16) * (a * a + 1) for a in range(-6, 7)) and -4 / 4 == -1)
check('16 - 8i + i^2 = 15 - 8i', 16 - 8j + 1j ** 2 == 15 - 8j)

# ---------------------------------------------------------------- numbers of the proposed fixes
print('== fixes proposed in the review')
# fix 1 (topic-1.6 removal): put s-alpha-beta-table back, take s-p-backtest out
auto16 = collections.defaultdict(list)
for x in EX['topic-1.6']['items']:
    if x.get('kind') != 'longform':
        for s in x['skills']:
            auto16[s].append((x['id'], x['difficulty']))
if 's-p-backtest' in IT['topic-1.6']:
    left = sorted(d for i, d in auto16['ht-pvalue'] if i != 's-p-backtest')
    check('fix 1: s-p-backtest carries ht-pvalue alone at difficulty 3; without it ht-pvalue keeps three auto items, two at 3',
          IT['topic-1.6']['s-p-backtest']['skills'] == ['ht-pvalue'] and IT['topic-1.6']['s-p-backtest']['difficulty'] == 3 and left == [3, 3, 4], str(left))
    check('fix 1: rg-inference would hold 3, 4, 4, 5', sorted([d for _, d in auto16['rg-inference']] + [3]) == [3, 4, 4, 5])
else:
    check('fix 1 applied: rg-inference has an item at difficulty 3 or less', min(d for _, d in auto16['rg-inference']) <= 3)
# fix 2 (s-three-traders re-storied): Beta(27, 3) prior, 20 of 20, 68 of 70, 252 of 270
pa, pb = 27, 3
sel = {'kiln': (20, 20), 'loom': (68, 70), 'moss': (252, 270)}
ps = {k: F(pa + wn, pa + pb + n) for k, (wn, n) in sel.items()}
check('fix 2: prior mean 90%, worth 30; posteriors Beta(47, 3), Beta(95, 5), Beta(279, 21); means 0.94, 0.95, 0.93',
      F(pa, pa + pb) == F(9, 10) and ps == {'kiln': F(47, 50), 'loom': F(95, 100), 'moss': F(279, 300)} and (20 - 20, 70 - 68, 270 - 252) == (0, 2, 18), str(ps))
check('fix 2: top is Loom; raw top Kiln at 100%; longest record Moss; Loom raw 97%; no tie',
      max(ps, key=ps.get) == 'loom' and max(sel, key=lambda k: F(*sel[k])) == 'kiln' and max(sel, key=lambda k: sel[k][1]) == 'moss'
      and round(100 * 68 / 70) == 97 and len(set(ps.values())) == 3)
# fix 3 (e-just-paid, new numbers): 3.20 just paid, 5% growth, 9% required
v3 = stream(3.20, 0.05, 0.09, 12000)
check('fix 3: 3.36/0.04 = 84.00; slips 80.00, 37.33, 24.00; no tie', near(v3, 84.0, 1e-6) and near(3.20 * 1.05, 3.36) and near(3.20 / 0.04, 80.0)
      and round(3.36 / 0.09, 2) == 37.33 and near(3.36 / 0.14, 24.0) and abs(3.36 / 0.09 * 100 % 1 - 0.5) > 0.1, f'{v3:.6f}')
# fix 4 (e-swapped-d, printed normal values)
check('fix 4: N(0.35) = 0.636831, N(0.15) = 0.559618, e^{-0.05} = 0.951229 to six places; they give -4.62',
      round(Phi(0.35), 6) == 0.636831 and round(Phi(0.15), 6) == 0.559618 and round(math.exp(-0.05), 6) == 0.951229
      and round(100 * 0.559618 - 100 * 0.951229 * 0.636831, 2) == -4.62, f'{100 * 0.559618 - 100 * 0.951229 * 0.636831:.4f}')
check('fix 5: 95.123 in the explanation gives -4.62', round(100 * Phi(0.15) - 95.123 * Phi(0.35), 2) == -4.62 and round(100 * math.exp(-0.05), 3) == 95.123)

print(f'\n{n_ok} ok, {n_bad} FINDING')
