#!/usr/bin/env python3
"""Second reader's recompute for the seven new items of exam topic-1.5 (session AG).

Every key, `wrong` value and printed number is recomputed by a method the
author's script does not use: enumeration with Fractions, a fundamental-matrix
solve, a seeded simulation and erfc for the normal tail.  The second half
recomputes the numbers of the fixes proposed in
docs/reviews/review-exam-second-item-1.5.md.

A failing check prints a FINDING line.  Exit 0 unless the script itself breaks.
"""
import collections
import glob
import itertools
import json
import math
import os
import random
import re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
CONTENT = os.path.join(ROOT, 'app', 'content')
EXAM = json.load(open(os.path.join(CONTENT, 'exams', 'topic-1.5.json'), encoding='utf-8'))
ITEMS = {it['id']: it for it in EXAM['items']}
NEW = ['e-ticket-pair', 'e-neither-market', 'e-multiple-four', 'e-coin-again',
       'e-distance-three', 'e-fill-times', 'e-floor-walk']
REMOVED = {'e-wait-six': ['dl-discrete'], 'e-uniform': ['dl-continuous']}
COURSES = ['counting-chance', 'conditional', 'random-vars', 'limits-thm', 'markov']

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
    return abs(float(a) - float(b)) <= eps


def numeric(iid):
    w = ITEMS[iid]['widget']
    return w['answer'], w['tol']['abs'], {x['id']: (x['value'], x['tol']['abs']) for x in w.get('wrong', [])}


def bands(iid, key_exact, wrong_exact):
    """Key band takes the exact and the printed value, refuses every wrong value; no tie."""
    ans, tol, wrong = numeric(iid)
    check(f'{iid} key', abs(float(key_exact) - ans) <= tol, f'exact {float(key_exact):.6f} printed {ans}')
    check(f'{iid} wrong ids', set(wrong) == set(wrong_exact), f'{sorted(wrong)}')
    for k, v in wrong_exact.items():
        if k not in wrong:
            continue
        wv, wt = wrong[k]
        check(f'{iid} wrong {k}', abs(float(v) - wv) <= wt, f'exact {float(v):.6f} printed {wv}')
        check(f'{iid} wrong {k} outside key band', abs(wv - ans) > tol + wt)
        check(f'{iid} key outside wrong band {k}', abs(float(key_exact) - wv) > wt)
    ws = list(wrong.values())
    for (a, ta), (b, tb) in itertools.combinations(ws, 2):
        check(f'{iid} wrong bands apart', abs(a - b) > ta + tb, f'{a} {b}')
    # rounding tie: the exact key at 4 places must not sit on a 5 in the fifth place
    x = float(key_exact) * 10 ** 4
    check(f'{iid} no rounding tie', abs((x - math.floor(x)) - 0.5) > 1e-3)


def text_of(it):
    def t(o):
        if isinstance(o, str):
            return o + ' '
        if isinstance(o, list):
            return ''.join(t(x) for x in o)
        if isinstance(o, dict):
            return ''.join(t(v) for k, v in o.items() if k != 'canvas')
        return ''
    return t(it)


# ---------------------------------------------------------------- structure
check('35 items', len(EXAM['items']) == 35, str(len(EXAM['items'])))
check('minutes pro rata, rounded to 5', EXAM['minutes'] == 5 * round(60 * 35 / 30 / 5) == 70, str(EXAM['minutes']))
check('all seven new ids present', all(i in ITEMS for i in NEW))
check('removed ids absent', all(i not in ITEMS for i in REMOVED))
check('ids unique', len(ITEMS) == len(EXAM['items']))

auto = [it for it in EXAM['items'] if it['widget']['kind'] != 'longform']
now = collections.Counter(s for it in auto for s in it['skills'])
before = collections.Counter(now)
for i in NEW:
    for s in ITEMS[i]['skills']:
        before[s] -= 1
for i, sk in REMOVED.items():
    for s in sk:
        before[s] += 1

essential = collections.defaultdict(list)       # skill -> [(course, level)]
for c in COURSES:
    cj = json.load(open(os.path.join(CONTENT, 'courses', c, 'course.json'), encoding='utf-8'))
    for lv in cj['levels']:
        p = os.path.join(CONTENT, 'courses', c, lv.get('review', '') + '.json')
        if not lv.get('review') or not os.path.exists(p):
            continue
        rv = json.load(open(p, encoding='utf-8'))
        for s in sorted({s for it in rv['items'] for s in it.get('skills', [])}):
            essential[s].append(f"{c} L{lv['n']}")

pairs = sorted(s for s in essential if before[s] == 1)
triples = sum(len(essential[s]) for s in pairs)
print('pairs before:', pairs)
check('12 pairs, 25 triples before the pass', len(pairs) == 12 and triples == 25, f'{len(pairs)} {triples}')
check('report lists the same 12', set(pairs) == {'cc-sample', 'cc-count', 'cc-rules', 'cc-symmetry', 'cond-shrink',
                                                 'cond-mult', 'bayes', 'rv-dist', 'dl-lln', 'dl-clt', 'mc-firststep', 'mc-walks'})
for s in pairs:
    check(f'pair {s} now has two auto items', now[s] >= 2, str(now[s]))
check('no essential skill with no auto item', all(now[s] >= 1 for s in essential))
low = sorted(s for s in EXAM['skills'] if now[s] < 2)
check('no exam skill below two auto items', not low, str(low))
check('every tagged skill is declared', all(s in EXAM['skills'] for it in EXAM['items'] for s in it['skills']))
for i, sk in REMOVED.items():
    for s in sk:
        keep = [(it['id'], it['difficulty'], it['widget']['kind']) for it in auto if s in it['skills']]
        check(f'removal {i}: {s} keeps two auto items', len(keep) >= 2, str(keep))
        # the count holds; is anything left at the removed item's level of difficulty?
        check(f'removal {i}: {s} keeps an item at difficulty 3 or below', any(d <= 3 for _, d, _ in keep),
              f'{keep}; essential to {essential[s]}')
diff = collections.Counter(it['difficulty'] for it in EXAM['items'])
check('difficulty mix 7/16/9/3', [diff[k] for k in (2, 3, 4, 5)] == [7, 16, 9, 3], str(sorted(diff.items())))

# voice gates on the new items, read independently of voice-scan.py
for i in NEW:
    t = text_of(ITEMS[i])
    check(f'{i} no exclamation mark or em-dash', '!' not in t and '\u2014' not in t)
    plain = re.sub(r'\$[^$]*\$', 'M', t)
    longest = max((len(s.split()) for s in re.split(r'(?<=[.?])\s+', plain)), default=0)
    check(f'{i} longest sentence under 35 words', longest < 35, str(longest))
    ex = re.sub(r'\$[^$]*\$', 'M', ITEMS[i]['explain']['text'])
    check(f'{i} explanation at most three sentences', len([s for s in re.split(r'(?<=[.?])\s+', ex) if s.strip()]) <= 3)
    if ITEMS[i]['widget']['kind'] == 'choice':
        opts = ITEMS[i]['widget']['options']
        check(f'{i} one correct option, a why on each other', sum(1 for o in opts if o.get('correct')) == 1
              and all(o.get('why') for o in opts if not o.get('correct')))

# ---------------------------------------------------------------- e-ticket-pair
pairs5 = list(itertools.combinations(range(1, 6), 2))
key = F(sum(1 for a, b in pairs5 if (a + b) % 2 == 0), len(pairs5))
rep = F(sum(1 for a in range(1, 6) for b in range(1, 6) if (a + b) % 2 == 0), 25)
bands('e-ticket-pair', key, {'with-repeats': rep, 'odd': 1 - key})
check('e-ticket-pair 10 pairs, 4 even', len(pairs5) == 10 and key == F(4, 10))
check('e-ticket-pair explain 3 odd pairs, 1 even pair',
      sum(1 for a, b in pairs5 if a % 2 and b % 2) == 3 and sum(1 for a, b in pairs5 if not a % 2 and not b % 2) == 1)
# tag test: the multiplication rule alone gives the key, with no sample space and no count
seq = F(3, 5) * F(2, 4) + F(2, 5) * F(1, 4)
check('e-ticket-pair needs cc-sample and cc-count (no route round both)', seq != key,
      f'draw-by-draw 3/5*2/4 + 2/5*1/4 = {seq}; ten pairs can also be listed by hand, as e-small-total (cc-sample only) asks')

# ---------------------------------------------------------------- e-neither-market
# 100 clients on a Venn diagram, integer regions
both, shares, bonds = 12, 45, 30
only_s, only_b = shares - both, bonds - both
neither = 100 - only_s - only_b - both
bands('e-neither-market', F(neither, 100), {'no-overlap': F(100 - shares - bonds, 100), 'union': F(only_s + only_b + both, 100)})
check('e-neither-market explain 0.63', only_s + only_b + both == 63)
check('e-neither-market regions are possible', min(only_s, only_b, both, neither) >= 0)

# ---------------------------------------------------------------- e-multiple-four
m4 = [n for n in range(1, 31) if n % 4 == 0]
m43 = [n for n in m4 if n % 3 == 0]
opt = {o['id']: o for o in ITEMS['e-multiple-four']['widget']['options']}
check('e-multiple-four key 2/7', F(len(m43), len(m4)) == F(2, 7) and opt['a'].get('correct') and '{2}{7}' in opt['a']['text'])
check('e-multiple-four b is P(multiple of 3)', F(sum(1 for n in range(1, 31) if n % 3 == 0), 30) == F(1, 3) and '{1}{3}' in opt['b']['text'])
check('e-multiple-four c is the joint chance', F(len(m43), 30) == F(1, 15) and '{1}{15}' in opt['c']['text'])
check('e-multiple-four d is P(multiple of 4)', F(len(m4), 30) == F(7, 30) and '{7}{30}' in opt['d']['text'])
check('e-multiple-four explain lists 4..28, 12 and 24', m4 == [4, 8, 12, 16, 20, 24, 28] and m43 == [12, 24])
check('e-multiple-four four distinct values', len({F(2, 7), F(1, 3), F(1, 15), F(7, 30)}) == 4)

# ---------------------------------------------------------------- e-coin-again
# joint route: P(HH) / P(H), no posterior and no Bayes step
pH = F(1, 2) * F(1, 2) + F(1, 2) * F(4, 5)
pHH = F(1, 2) * F(1, 2) ** 2 + F(1, 2) * F(4, 5) ** 2
key = pHH / pH
bands('e-coin-again', key, {'no-update': pH, 'posterior': F(1, 2) * F(4, 5) / pH, 'biased': F(4, 5)})
check('e-coin-again exact 89/130, posterior 8/13, first head 0.65', key == F(89, 130) and F(1, 2) * F(4, 5) / pH == F(8, 13) and pH == F(13, 20))
check('e-coin-again needs bayes (no route round the posterior)', False,
      f'P(HH)/P(H) = {pHH}/{pH} = {key}: total probability twice and one division, no inversion')
rng = random.Random(15)
h1 = h2 = 0
for _ in range(400000):
    p = 0.8 if rng.random() < 0.5 else 0.5
    if rng.random() < p:
        h1 += 1
        h2 += rng.random() < p
check('e-coin-again simulation', abs(h2 / h1 - float(key)) < 0.004, f'{h2 / h1:.4f}')

# ---------------------------------------------------------------- e-distance-three
pmf = collections.Counter()
for x in range(1, 7):
    pmf[abs(x - 3)] += F(1, 6)
opt = {o['id']: o['text'] for o in ITEMS['e-distance-three']['widget']['options']}


def read_pmf(t):
    return {int(y): F(int(a), int(b)) for y, a, b in re.findall(r'P\(Y\{=\}(\d)\) = \\tfrac\{(\d+)\}\{(\d+)\}', t)}


check('e-distance-three key', read_pmf(opt['a']) == dict(pmf) and ITEMS['e-distance-three']['widget']['options'][0].get('correct'), str(dict(pmf)))
check('e-distance-three key sums to 1', sum(pmf.values()) == 1)
check('e-distance-three d sums to 7/6', sum(read_pmf(opt['d']).values()) == F(7, 6))
check('e-distance-three b is four equal values', '{1}{4}' in opt['b'] and '0, 1, 2, 3' in opt['b'])
check('e-distance-three c is X - 3', sorted(x - 3 for x in range(1, 7)) == [-2, -1, 0, 1, 2, 3] and '-2, -1, 0, 1, 2, 3' in opt['c'])
check('e-distance-three explain order 2, 1, 0, 1, 2, 3', [abs(x - 3) for x in range(1, 7)] == [2, 1, 0, 1, 2, 3])

# ---------------------------------------------------------------- e-fill-times
rows = ITEMS['e-fill-times']['widget']['rows']
cheb, clt = rows[0][1], rows[1][1]
n, sd, eps = 64, 16, 5
cheb_exact = F(sd * sd, n * eps * eps)                      # sigma^2 / (n eps^2), no k
phi = lambda z: 0.5 * math.erfc(-z / math.sqrt(2))
k = eps / (sd / math.sqrt(n))
clt_exact = 2 * (1 - phi(k))
clt_print = 2 * (1 - 0.9938)
check('e-fill-times (a) 0.16', near(cheb_exact, cheb['answer']) and cheb_exact == F(4, 25), str(cheb_exact))
check('e-fill-times (b) from the printed 0.9938', near(clt_print, clt['answer'], 1e-9), f'{clt_print:.4f}')
check('e-fill-times (b) band takes the exact tail', abs(clt_exact - clt['answer']) <= clt['tol']['abs'], f'{clt_exact:.5f}')
check('e-fill-times Phi(2.5) to 4 places', round(phi(2.5), 4) == 0.9938, f'{phi(2.5):.6f}')
check('e-fill-times k = 2.5 and sd of the mean 2', near(k, 2.5) and near(sd / math.sqrt(n), 2))
check('e-fill-times cells apart', abs(cheb['answer'] - clt['answer']) > cheb['tol']['abs'] + clt['tol']['abs'])
# slips named in the cell feedback stay outside the bands
check('e-fill-times (a) refuses sd 16 (k = 5/16 gives 10.24) and 1/k', abs(1 / (5 / 16) ** 2 - 0.16) > 0.001 and abs(1 / 2.5 - 0.16) > 0.001)
check('e-fill-times (b) refuses one tail 0.0062', abs((1 - 0.9938) - clt['answer']) > clt['tol']['abs'])
check('e-fill-times no rounding tie', abs(clt_exact * 1e4 % 1 - 0.5) > 1e-2, f'{clt_exact * 1e4:.3f}')
check('e-fill-times prints its normal value in the prose, as e-clt-pnl does', '\\Phi(2.5) = 0.9938' in ITEMS['e-fill-times']['prose'])

# ---------------------------------------------------------------- e-floor-walk
edges = ITEMS['e-floor-walk']['canvas']['params']['edges']
P = collections.defaultdict(dict)
for e in edges:
    P[e['from']][e['to']] = F(str(e['w']))
check('e-floor-walk rows sum to 1', all(sum(r.values()) == 1 for r in P.values()) and len(P) == 4)
check('e-floor-walk graph is the walk in the prose',
      P['s0'] == {'s1': 1} and P['s1'] == {'s0': F(1, 2), 's2': F(1, 2)} and P['s2'] == {'s1': F(1, 2), 's3': F(1, 2)} and P['s3'] == {'s3': 1})


def hit_times(Q):
    """Expected steps to absorption: solve (I - Q) t = 1 by Gauss-Jordan over Fractions."""
    m = len(Q)
    A = [[(1 if i == j else 0) - Q[i][j] for j in range(m)] + [F(1)] for i in range(m)]
    for c in range(m):
        p = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(m):
            if r != c and A[r][c] != 0:
                A[r] = [x - A[r][c] * y for x, y in zip(A[r], A[c])]
    return [A[i][m] for i in range(m)]


tr = ['s0', 's1', 's2']
E = hit_times([[P[a].get(b, F(0)) for b in tr] for a in tr])
print('floor walk E0, E1, E2 =', E)
# slip "lost-step": E0 = E1 put into the other two equations
e1 = F(3, 2) / F(1, 4)
bands('e-floor-walk', E[0], {'straight-up': 3, 'lost-step': e1, 'from-one': E[1]})
check('e-floor-walk explain E1 = 8, E2 = 5', E[1] == 8 and E[2] == 5)
check('e-floor-walk explain line E1 = 2 + 3/4 E1', F(2) + F(3, 4) * 8 == 8)
rng = random.Random(9)
tot = 0
for _ in range(100000):
    s = t = 0
    while s < 3:
        s = 1 if s == 0 else s + (1 if rng.random() < 0.5 else -1)
        t += 1
    tot += t
check('e-floor-walk simulation', abs(tot / 100000 - 9) < 0.1, f'{tot / 100000:.3f}')
# tag test: unfold the floor to a fair walk on -3..3; the duration formula i(N - i) of e-ruin-length gives the key
unfold = 3 * (6 - 3)
check('e-floor-walk needs mc-firststep (no route round the equations)', unfold != E[0],
      f'mirror at 0: fair walk from 3 on 0..6 lasts i(N - i) = {unfold}, the formula printed in e-ruin-length feedback')

# ---------------------------------------------------------------- proposed fixes, recomputed
print('--- numbers of the fixes proposed in the review')
p15 = list(itertools.combinations(range(1, 16), 2))
k15 = F(sum(1 for a, b in p15 if (a + b) % 2 == 0), len(p15))
o15 = [(a, b) for a in range(1, 16) for b in range(1, 16) if a != b]
check('fix 1: tickets 1 to 15, cell (a) 105 pairs, cell (b) 28 + 21 = 49 with an even sum',
      len(p15) == 105 == math.comb(15, 2) and math.comb(8, 2) == 28 and math.comb(7, 2) == 21
      and sum(1 for a, b in p15 if (a + b) % 2 == 0) == 49 and k15 == F(7, 15), str(k15))
check('fix 1: ordered draws give 210, named in the cell (a) feedback', len(o15) == 210 == 15 * 14)
check('fix 1: 8 odd and 7 even tickets', sum(1 for t in range(1, 16) if t % 2) == 8)
post = F(1, 2) * F(4, 5) / pH
check('fix 2: cell (a) 8/13 = 0.6154, cell (b) 89/130 = 0.6846', round(float(post), 4) == 0.6154 and round(float(pHH / pH), 4) == 0.6846)
check('fix 2: cells apart, no tie', abs(float(post) - float(pHH / pH)) > 0.001 and abs(float(post) * 1e4 % 1 - 0.5) > 1e-3)
check('fix 5: with e-uniform back, 36 items and 70 minutes', 5 * round(60 * 36 / 30 / 5) == 70, f'{60 * 36 / 30}')

print(f'\n{n_ok} ok, {n_bad} FINDING')
