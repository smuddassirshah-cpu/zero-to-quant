"""Recompute every key, wrong value and printed number of the seven new
topic-1.5 items (exam second item, session AG). Exit 0 when all agree."""
import json, os, sys, itertools, math
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'topic-1.5.json')
d = json.load(open(EXAM, encoding='utf-8'))
items = {it['id']: it for it in d['items']}
bad = 0

def check(name, got, want, tol=1e-9):
    global bad
    ok = abs(float(got) - float(want)) <= tol
    print(('ok   ' if ok else 'FAIL ') + f'{name}: {got} vs {want}')
    if not ok:
        bad += 1

def wrongs(it):
    return {w['id']: w['value'] for w in it['widget'].get('wrong', [])}

def refused(it):
    """Every wrong value lies outside the key band, and no wrong band holds the key."""
    w = it['widget']
    for x in w.get('wrong', []):
        check(f"{it['id']} {x['id']} outside key band", abs(x['value'] - w['answer']) > w['tol']['abs'], True)
        check(f"{it['id']} {x['id']} band misses key", abs(x['value'] - w['answer']) > x['tol']['abs'], True)

def r4(x):
    return round(float(x) + 1e-12, 4)

# Exam shape
check('item count', len(d['items']), 35)
check('minutes 60 * 35 / 30 rounded to 5', d['minutes'], 5 * round(60 * 35 / 30 / 5))
for gone in ('e-wait-six', 'e-uniform'):
    check(f'{gone} removed', gone in items, False)

# e-ticket-pair: two different tickets from 1..5
it = items['e-ticket-pair']
pairs = list(itertools.combinations(range(1, 6), 2))
even = [p for p in pairs if sum(p) % 2 == 0]
check('pairs', len(pairs), math.comb(5, 2))
check('even pairs', len(even), math.comb(3, 2) + math.comb(2, 2))
check('ticket key', it['widget']['answer'], F(len(even), len(pairs)))
rep = [p for p in itertools.product(range(1, 6), repeat=2) if sum(p) % 2 == 0]
check('ticket with-repeats', wrongs(it)['with-repeats'], F(len(rep), 25))
check('ticket odd', wrongs(it)['odd'], 1 - F(len(even), len(pairs)))
refused(it)

# e-neither-market
it = items['e-neither-market']
A, B, AB = F(45, 100), F(30, 100), F(12, 100)
union = A + B - AB
check('union printed 0.63', union, F(63, 100))
check('neither key', it['widget']['answer'], 1 - union)
check('neither no-overlap', wrongs(it)['no-overlap'], 1 - A - B)
check('neither union', wrongs(it)['union'], union)
refused(it)

# e-multiple-four
it = items['e-multiple-four']
m4 = [n for n in range(1, 31) if n % 4 == 0]
both = [n for n in m4 if n % 3 == 0]
check('multiples of 4', len(m4), 7)
check('of them multiples of 3 are 12 and 24', both == [12, 24], True)
opts = {o['id']: o for o in it['widget']['options']}
check('key option a correct', opts['a'].get('correct', False), True)
check('a = 2/7', F(len(both), len(m4)), F(2, 7))
check('b = 1/3 unconditional', F(sum(1 for n in range(1, 31) if n % 3 == 0), 30), F(1, 3))
check('c = 1/15 joint', F(len(both), 30), F(1, 15))
check('d = 7/30 news', F(len(m4), 30), F(7, 30))
vals = [F(2, 7), F(1, 3), F(1, 15), F(7, 30)]
check('options distinct', len(set(vals)), 4)

# e-coin-again
it = items['e-coin-again']
pf, pb = F(1, 2), F(4, 5)
ph1 = F(1, 2) * pf + F(1, 2) * pb
post_b = F(1, 2) * pb / ph1
ph2 = post_b * pb + (1 - post_b) * pf
check('P(H1) printed 0.65', ph1, F(13, 20))
check('posterior 8/13', post_b, F(8, 13))
check('next head 89/130', ph2, F(89, 130))
check('next head direct', (F(1, 2) * pf**2 + F(1, 2) * pb**2) / ph1, F(89, 130))
check('coin key 4 places', it['widget']['answer'], r4(ph2))
check('coin no-update', wrongs(it)['no-update'], r4(ph1))
check('coin posterior', wrongs(it)['posterior'], r4(post_b))
check('coin biased', wrongs(it)['biased'], pb)
check('key not a rounding tie', abs(float(ph2) * 1e4 % 1 - 0.5) > 0.01, True)
refused(it)

# e-distance-three
it = items['e-distance-three']
pmf = {}
for x in range(1, 7):
    pmf[abs(x - 3)] = pmf.get(abs(x - 3), 0) + F(1, 6)
check('Y pmf', pmf == {0: F(1, 6), 1: F(1, 3), 2: F(1, 3), 3: F(1, 6)}, True)
check('Y faces 1..6 printed 2,1,0,1,2,3', [abs(x - 3) for x in range(1, 7)] == [2, 1, 0, 1, 2, 3], True)
check('option d sums over 1', F(1, 6) + 3 * F(1, 3) > 1, True)
opts = {o['id']: o for o in it['widget']['options']}
check('option a correct', opts['a'].get('correct', False), True)

# e-fill-times
it = items['e-fill-times']
n, mu, sd, gap = 64, 30, 16, 5
se = sd / math.sqrt(n)
k = gap / se
phi25 = 0.5 * (1 + math.erf(2.5 / math.sqrt(2)))
rows = it['widget']['rows']
check('se printed 2', se, 2)
check('k printed 2.5', k, 2.5)
check('Phi(2.5) printed 0.9938', round(phi25, 4), 0.9938)
check('Chebyshev key', rows[0][1]['answer'], 1 / k**2)
check('CLT key from printed table', rows[1][1]['answer'], round(2 * (1 - 0.9938), 4))
check('CLT key near exact', abs(rows[1][1]['answer'] - 2 * (1 - phi25)) < rows[1][1]['tol']['abs'], True)
check('CLT band refuses one tail', abs(rows[1][1]['answer'] - (1 - 0.9938)) > rows[1][1]['tol']['abs'], True)
check('Cheb band refuses 1/k', abs(rows[0][1]['answer'] - 1 / k) > rows[0][1]['tol']['abs'], True)
check('Cheb band refuses raw sd', abs(rows[0][1]['answer'] - (sd / gap)**2) > rows[0][1]['tol']['abs'], True)

# e-floor-walk: reflecting at 0, absorbing at 3, fair steps
it = items['e-floor-walk']
# Solve E0 = 1 + E1, E1 = 1 + E0/2 + E2/2, E2 = 1 + E1/2 by elimination in Fractions
# E1 = 1 + (1 + E1)/2 + (1 + E1/2)/2 = 2 + 3E1/4
E1 = F(2) / (1 - F(3, 4))
E0, E2 = 1 + E1, 1 + E1 / 2
check('E1 = 8', E1, 8)
check('E0 key', it['widget']['answer'], E0)
check('E2 = 5', E2, 5)
check('equation E1', E1, 1 + E0 / 2 + E2 / 2)
# second method: iterate the expectation equations
e = [0.0, 0.0, 0.0, 0.0]
for _ in range(20000):
    e = [1 + e[1], 1 + 0.5 * e[0] + 0.5 * e[2], 1 + 0.5 * e[1], 0.0]
check('iterated E0', e[0], 9, 1e-6)
check('reflecting walk N^2', E0, 3**2)
# slip: drop the minute from 0 (E0 = E1)
s1 = F(3, 2) / (1 - F(1, 2) - F(1, 4))   # E1 = 1 + E1/2 + (1 + E1/2)/2, so E1/4 = 3/2
check('lost-step', wrongs(it)['lost-step'], s1)
check('straight-up', wrongs(it)['straight-up'], 3)
check('from-one', wrongs(it)['from-one'], E1)
refused(it)
# canvas rows sum to 1
out = {}
for edge in it['canvas']['params']['edges']:
    out[edge['from']] = out.get(edge['from'], 0) + edge['w']
check('canvas rows sum to 1', all(abs(v - 1) < 1e-9 for v in out.values()), True)

# Skill coverage: every essential skill of a topic level has at least two auto items
import glob, collections
cnt = collections.Counter(s for it in d['items'] if it['widget']['kind'] != 'longform' for s in it['skills'])
for cj in glob.glob(os.path.join(ROOT, 'app', 'content', 'courses', '*', 'course.json')):
    c = json.load(open(cj, encoding='utf-8'))
    if c.get('topic') != '1.5':
        continue
    for lv in c['levels']:
        rv = json.load(open(os.path.join(os.path.dirname(cj), lv['review'] + '.json'), encoding='utf-8'))
        for s in sorted({s for x in rv['items'] for s in x.get('skills', [])}):
            if cnt[s] < 2:
                check(f"{c['id']}/L{lv['n']} {s} auto items", cnt[s], 2)
check('no exam skill below two auto items', min(cnt[s] for s in d['skills']) >= 2, True)

print('bad', bad)
sys.exit(1 if bad else 0)
