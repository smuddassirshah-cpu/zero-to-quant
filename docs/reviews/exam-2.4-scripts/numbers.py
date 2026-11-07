"""Second reader's number script for app/content/exams/topic-2.4.json (review-exam-2.4.md).

Recomputes every graded key and every wrong[] value, the numbers in prose, feedback and explanations, and runs the
six code items: each solution passes every example and hidden test, each starter fails every hidden test, planted
bugs are caught, and the stated time limits hold (solution well under 5 s; slow versions over it, by a subprocess
with a timeout). Routes: closed forms written again, brute force or enumeration as the second method (interval
subsets, coin states, BFS on pairs, every plan of e-best-plan, a bitmask search for vans).
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Pure standard library. Run: python3 docs/reviews/exam-2.4-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers`. Drop its folder from the path first.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import random  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from collections import Counter, deque  # noqa: E402
from fractions import Fraction as F  # noqa: E402

sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.4.json')
COURSE = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses', 'contests', 'course.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}
IT = {it['id']: it for it in doc['items']}


def P(iid):
    return f'items[{idx[iid]}]'


def W(iid):
    return IT[iid]['widget']


def key(iid, value):
    a = W(iid)['answer']
    ex._rec(a == value, f'{iid} answer {a!r} = {value!r}', '' if a == value else 'recomputed value differs')


def wrong(iid, wid, value):
    ws = [x for x in W(iid)['wrong'] if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]['value']
    ex._rec(v == value, f'{iid} wrong "{wid}" {v!r} = {value!r}', '' if v == value else 'recomputed slip differs')


def correct_ids(iid):
    return sorted(o['id'] for o in W(iid)['options'] if o.get('correct'))


def say(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['minutes'] == 60 and doc['pass'] == 0.7, 'minutes 60 and pass 0.7 as stored')
hours = 140  # docs/curriculum.md row 2.4; learn.js examMinutes(140) = 60
ex.claim((45 if hours <= 60 else 60 if hours <= 150 else 90) == doc['minutes'], 'minutes follow learn.js examMinutes(140 h)')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 5, 3: 13, 4: 5, 5: 3}, f'ramp {ramp} (19%, 50%, 19%, 12% against 20, 50, 20, 10)')
with open(COURSE, encoding='utf8') as f:
    course = json.load(f)
ex.claim(doc['skills'] == course['skills'], 'skills map equals contests course.json skills')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(course['skills']), 'every skill is tested by at least one item')
rub = sum(r['points'] for r in IT['e-round-review']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')
nopace = [it['id'] for it in doc['items'] if 'pace' not in it]
print(f'   items without pace: {len(nopace)} of {len(doc["items"])}')
# Time at the sibling exams' paces (d2 60 s, d3 120 s, d4 150 s, code d3 420 s, code d4 480 s, code d5 600 s,
# d5 numeric 300 s, longform 900 s). Information for the review, not a check.
sec = 0
for it in doc['items']:
    k, d = it.get('kind') or it['widget']['kind'], it['difficulty']
    sec += 900 if k == 'longform' else {3: 420, 4: 480, 5: 600}[d] if k == 'code' else {2: 60, 3: 120, 4: 150, 5: 300}[d]
print(f'   estimated time at sibling paces: {sec} s = {sec / 60:.0f} min against {doc["minutes"]}')

# ---------------------------------------------------------------- e-file-values
t_max, n_max, sum_n = 10 ** 4, 2 * 10 ** 5, 2 * 10 ** 5
key('e-file-values', min(sum_n, t_max * n_max))
wrong('e-file-values', 'product', t_max * n_max)
wrong('e-file-values', 'tests', t_max)
say('e-file-values', 'explain.text', 4 * 10 ** 10, fmt=lambda v: '4 \\cdot 10^{10}')
ex.claim((2 * 10 ** 5) ** 2 == 4 * 10 ** 10, 'e-file-values (2e5)^2 = 4e10')

# ---------------------------------------------------------------- e-fast-read (tokens are layout-free; line readers break)
lay1 = '2\n3\n1 2 3\n2\n4 5\n'
lay2 = '2\n\n3\n1 2\n3\n2\n4\n5'
ex.claim(lay1.split() == lay2.split(), 'e-fast-read read().split() gives the same tokens for wrapped, blank and unterminated input')
ex.claim(lay1.split('\n') != lay2.split('\n'), 'e-fast-read split("\\n") keeps the layout, so positions shift')
try:
    int('1 2')
    bad = False
except ValueError:
    bad = True
ex.claim(bad, 'e-fast-read option c: int() of a line holding two values raises ValueError')
ex.claim(correct_ids('e-fast-read') == ['b'], 'e-fast-read key b')

# ---------------------------------------------------------------- e-lcm-rebalance
key('e-lcm-rebalance', math.lcm(84, 90))
ex.claim(84 * 90 // math.gcd(84, 90) == 1260 and math.gcd(84, 90) == 6, 'e-lcm-rebalance lcm by 84*90/gcd')
wrong('e-lcm-rebalance', 'product', 84 * 90)
wrong('e-lcm-rebalance', 'gcd', math.gcd(84, 90))
ex.claim(90 == 84 + 6 and 84 == 14 * 6 and math.gcd(84, 6) == 6, 'e-lcm-rebalance explain Euclid steps')
say('e-lcm-rebalance', 'feedback.correct', 1260)

# ---------------------------------------------------------------- e-greedy-tap (all subsets as the second method)
iv = {x['id']: (x['from'], x['to']) for x in IT['e-greedy-tap']['canvas']['state']['intervals']}


def overlap(a, b):
    return iv[a][0] < iv[b][1] and iv[b][0] < iv[a][1]


def greedy(order):
    kept = []
    for m in order:
        if all(not overlap(m, k) for k in kept):
            kept.append(m)
    return sorted(kept)


ef = greedy(sorted(iv, key=lambda m: iv[m][1]))
es = greedy(sorted(iv, key=lambda m: iv[m][0]))
sh = greedy(sorted(iv, key=lambda m: iv[m][1] - iv[m][0]))
ex.claim(ef == sorted(W('e-greedy-tap')['answer']), f'e-greedy-tap earliest finish keeps {ef}')
best = [s for r in range(8) for s in itertools.combinations(sorted(iv), r) if all(not overlap(a, b) for a, b in itertools.combinations(s, 2))]
top = max(len(s) for s in best)
ex.claim(top == 3 and [list(s) for s in best if len(s) == top] == [ef], 'e-greedy-tap optimum 3, unique: B, D, G')
wr = {x['id']: sorted(x['set']) for x in W('e-greedy-tap')['wrong']}
ex.claim(wr['start'] == es and wr['short'] == sh, f'e-greedy-tap slips: earliest start {es}, shortest first {sh}')
for m, says in [('mA', ['mB', 'mC', 'mD']), ('mE', ['mD', 'mF', 'mG']), ('mF', ['mD', 'mG'])]:
    ex.claim(all(overlap(m, o) for o in says), f'e-greedy-tap byKey {m}: overlaps {says}')
ex.claim(overlap('mC', 'mB') and overlap('mC', 'mD'), 'e-greedy-tap byKey mC: C overlaps B and D (and A)')

# ---------------------------------------------------------------- e-upsolve-pick
r = 1250
ex.claim(correct_ids('e-upsolve-pick') == ['c', 'd'] and 1300 - r <= 300 and 1500 - r <= 300 < 1950 - r,
         'e-upsolve-pick keys C and D inside 300; E 700 above')
say('e-upsolve-pick', 'explain.text', 1300 - r)
say('e-upsolve-pick', 'explain.text', 1500 - r)
say('e-upsolve-pick', 'explain.text', 1950 - r)

# ---------------------------------------------------------------- e-next-problem
rows = IT['e-next-problem']['canvas']['params']['rows']
open_rows = {f'r{i}': int(x[1].replace(',', '')) for i, x in enumerate(rows) if x[2] == 'open'}
ex.claim(max(open_rows, key=open_rows.get) == W('e-next-problem')['answer'][0], f'e-next-problem most-solved open problem {open_rows}')

# ---------------------------------------------------------------- e-pop-front
n = 100_000
key('e-pop-front', n * (n - 1) // 2)
ex.claim(sum(m - 1 for m in range(1, n + 1)) == 4_999_950_000, 'e-pop-front sum of (m - 1) by loop')
for small in (1, 2, 5, 10):
    lst, shifts = list(range(small)), 0
    while lst:
        shifts += len(lst) - 1
        lst.pop(0)
    ex.claim(shifts == small * (small - 1) // 2, f'e-pop-front simulated shifts for n = {small}')
wrong('e-pop-front', 'square', n * n)
wrong('e-pop-front', 'half', n * n // 2)
wrong('e-pop-front', 'pops', n)
# byKey "half" says the gap between n^2/2 and the exact total is the last pop; the gap is n/2 = 50,000 shifts
ex.claim_text('exam', f'{P("e-pop-front")}.feedback.byKey.half', 'The last pop shifts nothing, so',
              n * n // 2 - n * (n - 1) // 2 == 1, 'e-pop-front byKey half: the gap to n^2/2 is the last pop')

# ---------------------------------------------------------------- e-budget-table
rows = W('e-budget-table')['rows']
want = [5000 ** 2, 100000 ** 2, 10 ** 6 * math.log2(10 ** 6), 2 ** 30]
for i, v in enumerate(want):
    a = rows[i][1]['answer']
    ex.claim(abs(a - v) <= abs(v) * rows[i][1]['tol']['rel'], f'e-budget-table row {i} steps {a} = {v:.6g}')
    ex.claim(rows[i][2]['answer'] == ('yes' if v <= 2e8 else 'no'), f'e-budget-table row {i} fits = {rows[i][2]["answer"]}')
ex.claim(abs(math.log2(1e6) - 19.93) < 0.005, 'e-budget-table log2(1e6) = 19.93')
ex.claim(abs(2e7 - 10 ** 6 * 19.93) <= 2e7 * 0.03, 'e-budget-table a typed 2.0e7 is graded right')
ex.claim(100000 ** 2 / 2e8 == 50, 'e-budget-table r1c1 "fifty times the budget"')
say('e-budget-table', 'feedback.byKey.r3c1', 2 ** 30)

# ---------------------------------------------------------------- e-inverse-solve
inv5 = pow(5, -1, 17)
x = 3 * inv5 % 17
key('e-inverse-solve', x)
ex.claim([v for v in range(17) if 5 * v % 17 == 3] == [4], 'e-inverse-solve search gives 4 only')
ex.claim(inv5 == 7 == pow(5, 15, 17) and 35 == 2 * 17 + 1, 'e-inverse-solve inverse 7 = 5^15 mod 17')
wrong('e-inverse-solve', 'inverse', inv5)
wrong('e-inverse-solve', 'floor', 3 // 5)
wrong('e-inverse-solve', 'times', 3 * 5 % 17)
ex.claim(5 * 15 % 17 == 7, 'e-inverse-solve byKey times: 5 * 15 = 75 = 7 (mod 17)')

# ---------------------------------------------------------------- e-sieve-tap
cells = IT['e-sieve-tap']['canvas']['params']['cells']
num = {f'r{i + 1}c{j + 1}': int(cells[i][j]) for i in range(6) for j in range(10)}
dim = {num[c] for c in IT['e-sieve-tap']['canvas']['state']['dim']}
crossed = {v for p in (2, 3, 5) for v in range(p * p, 61, p)}
ex.claim(dim - {1} == crossed, 'e-sieve-tap faded cells other than 1 are exactly the crossed multiples of 2, 3 and 5')
# prose: "Crossed-out numbers are faded." 1 is faded but is no multiple of 2, 3 or 5
ex.claim_text('exam', f'{P("e-sieve-tap")}.prose', 'Crossed-out numbers are faded.', dim == crossed,
              'e-sieve-tap prose: the faded cells are the crossed-out numbers')
standing = [v for v in range(2, 61) if v not in dim and any(v % d == 0 for d in range(2, v))]
ex.claim(standing == [49] and num[W('e-sieve-tap')['answer'][0]] == 49, f'e-sieve-tap composites standing {standing}')
ex.claim(all(47 % d for d in range(2, 7)) and 51 % 3 == 0 and 51 in dim, 'e-sieve-tap byKey 47 prime, 51 crossed')
ex.claim(math.sqrt(60) < 8 and [v for v in range(49, 61, 7) if v not in crossed] == [49], 'e-sieve-tap explain: sqrt 60 < 8, only 49 of 7s')

# ---------------------------------------------------------------- e-coin-parity (every reachable state)
start = (0,) * 7  # 0 heads, 1 tails
seen, q = {start}, deque([start])
while q:
    s = q.popleft()
    for i in range(6):
        t = list(s)
        t[i] ^= 1
        t[i + 1] ^= 1
        t = tuple(t)
        if t not in seen:
            seen.add(t)
            q.append(t)
inv = {
    'tails-parity': len({sum(s) % 2 for s in seen}) == 1,
    'heads-parity': len({(7 - sum(s)) % 2 for s in seen}) == 1,
    'tails': len({sum(s) for s in seen}) == 1,
    'mod4': len({sum(s) % 4 for s in seen}) == 1,
    'left': len({s[0] for s in seen}) == 1,
}
ex.claim(sorted(k for k, v in inv.items() if v) == correct_ids('e-coin-parity'), f'e-coin-parity invariants {inv}')
ex.claim((1,) * 7 not in seen, 'e-coin-parity all tails unreachable')

# ---------------------------------------------------------------- e-fact-order (the stated order computes C(n, k))
p, N = 10 ** 9 + 7, 200
fact = [1] * (N + 1)
for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % p
ifact = [1] * (N + 1)
ifact[N] = pow(fact[N], p - 2, p)
for i in range(N, 0, -1):
    ifact[i - 1] = ifact[i] * i % p
ex.claim(all(fact[n_] * ifact[k_] % p * ifact[n_ - k_] % p == math.comb(n_, k_) % p for n_ in range(N + 1) for k_ in range(n_ + 1)),
         'e-fact-order s1, s2, s3, s4 give C(n, k) mod p for every n <= 200')
ex.claim(W('e-fact-order')['answer'] == ['s1', 's2', 's3', 's4'], 'e-fact-order key s1 to s4')

# ---------------------------------------------------------------- e-swap-cost
def completion_total(ts):
    return sum(itertools.accumulate(ts))


a0, a1 = completion_total([4, 9, 2, 7]), completion_total([4, 2, 9, 7])
ex.claim((a0, a1) == (54, 47), f'e-swap-cost totals {a0} and {a1}')
key('e-swap-cost', a0 - a1)
ex.claim(a0 - a1 == 9 - 2, 'e-swap-cost fall = 9 - 2')
wrong('e-swap-cost', 'longer', 9)
wrong('e-swap-cost', 'shorter', 2)
wrong('e-swap-cost', 'sum', 9 + 2)
ex.claim(list(itertools.accumulate([4, 9, 2, 7])) == [4, 13, 15, 22] and list(itertools.accumulate([4, 2, 9, 7])) == [4, 6, 15, 22],
         'e-swap-cost completion times 4, 13, 15, 22 and 4, 6, 15, 22')

# ---------------------------------------------------------------- e-submask-tap
g = IT['e-submask-tap']['canvas']['params']['cells']
mval = {f'r{i + 1}c{j + 1}': int(g[i][j], 2) for i in range(4) for j in range(4)}
subs = sorted(c for c, v in mval.items() if v & 11 == v)
ex.claim(subs == sorted(W('e-submask-tap')['answer']) and len(subs) == 2 ** 3, f'e-submask-tap submasks of 1011: {sorted(mval[c] for c in subs)}')
wr = {x['id']: sorted(x['set']) for x in W('e-submask-tap')['wrong']}
ex.claim(wr['super'] == sorted(c for c, v in mval.items() if v & 11 == 11), 'e-submask-tap slip super = masks containing 1011')
ex.claim(wr['smaller'] == sorted(c for c, v in mval.items() if v <= 11), 'e-submask-tap slip smaller = masks 0 to 11')
# byKey "smaller" says "every mask below 11"; the set holds 11 itself
ex.claim_text('exam', f'{P("e-submask-tap")}.feedback.byKey.smaller', 'every mask below 11',
              wr['smaller'] == sorted(c for c, v in mval.items() if v < 11), 'e-submask-tap byKey smaller: the set is the masks below 11')
ex.claim(sum(2 ** bin(m).count('1') for m in range(16)) == 3 ** 4, 'e-submask-tap explain: sum of 2^popcount = 3^n')
ex.claim(mval['r2c1'] == 4 and mval['r4c4'] == 15, 'e-submask-tap byKey r2c1 is 0100, r4c4 is 1111')

# ---------------------------------------------------------------- e-stress-gen
pairs_mean = F(sum(k * (k - 1) // 2 for k in range(1, 7)), 6)
per_pair = F(10 ** 18, 10 ** 18 * 2 * 10 ** 9)   # every x + y lies in [2, 2e9], k uniform on 1..2e9
per_trial = float(pairs_mean * per_pair)
ex.claim(pairs_mean == F(35, 6) and 2.5e-9 < per_trial < 3.5e-9, f'e-stress-gen exact-sum rate {per_trial:.3g} a trial: "about 3 per billion"')
ex.claim(1e7 * per_trial < 0.05, f'e-stress-gen 10 million trials expect {1e7 * per_trial:.3f} hits: "almost never"')
rng = random.Random(5)
hits = []
for rep in range(2000):
    for trial in itertools.count(1):
        m = rng.randint(1, 6)
        xs = [rng.randint(1, 5) for _ in range(m)]
        k = rng.randint(2, 10)
        if any(a + b == k for a, b in itertools.combinations(xs, 2)):
            hits.append(trial)
            break
ex.claim(sum(hits) / len(hits) < 5, f'e-stress-gen small values find an exact sum in {sum(hits) / len(hits):.2f} trials on average: "a few tries"')
ex.claim(correct_ids('e-stress-gen') == ['small'], 'e-stress-gen key small')

# ---------------------------------------------------------------- e-penalty-order and e-best-plan (decay v/250 a minute)
def score(v, t):
    return F(v) - F(v, 250) * t


pq = score(900, 20) + score(1500, 65)
qp = score(1500, 45) + score(900, 65)
ex.claim((score(900, 20), score(1500, 65), score(1500, 45), score(900, 65)) == (828, 1110, 1230, 666), 'e-penalty-order part scores')
ex.claim((pq, qp) == (1938, 1896), f'e-penalty-order totals {pq} and {qp}')
key('e-penalty-order', int(pq - qp))
ex.claim(F(900, 250) * 45 - F(1500, 250) * 20 == 42, 'e-penalty-order gap by the exchange formula r_P t_Q - r_Q t_P')
wrong('e-penalty-order', 'lost-p', int(2400 - pq))
wrong('e-penalty-order', 'lost-q', int(2400 - qp))
wrong('e-penalty-order', 'total', int(pq))
ex.claim(F(900, 250) * 20 == 72 and F(1500, 250) * 65 == 390 and F(1500, 250) * 45 == 270 and F(900, 250) * 65 == 234, 'e-penalty-order losses 72, 390, 270, 234')
ex.claim(666 / 900 > 0.3 and 1110 / 1500 > 0.3, 'e-penalty-order no problem reaches a 30% floor')
say('e-penalty-order', 'explain.text', 33.3)

prob = {'A': (1000, 10), 'B': (1300, 10), 'C': (1600, 40), 'D': (1700, 10)}


def plan_score(order, cap=60):
    t, s = 0, F(0)
    for name in order:
        v, d = prob[name]
        t += d
        if t > cap:
            return None
        s += score(v, t)
    return s


plans = {o: plan_score(o) for r_ in range(1, 5) for o in itertools.permutations(prob, r_) if plan_score(o) is not None}
bestv = max(plans.values())
bestp = [o for o, v in plans.items() if v == bestv]
key('e-best-plan', int(bestv))
ex.claim(bestp == [('D', 'B', 'C')], f'e-best-plan unique optimum {bestp} at {bestv}')
ex.claim((score(1700, 10), score(1300, 20), score(1600, 60)) == (1632, 1196, 1216), 'e-best-plan 1,632 + 1,196 + 1,216')
wrong('e-best-plan', 'rate', int(plans[('D', 'B', 'A')]))
wrong('e-best-plan', 'value', int(plans[('D', 'C', 'B')]))
wrong('e-best-plan', 'letters', int(plans[('A', 'B', 'C')]))
ex.claim([v // d for v, d in (prob['D'], prob['B'], prob['A'], prob['C'])] == [170, 130, 100, 40], 'e-best-plan rates 170, 130, 100, 40')
ex.claim(min(score(v, 60) / v for v, d in prob.values()) > F(3, 10), 'e-best-plan no problem reaches a 30% floor by minute 60')
# byKey "value": "Doing the 40-minute problem second pushes B and C late." In D, C, B, C ends at 50, earlier than in D, B, C (60).
ex.claim_text('exam', f'{P("e-best-plan")}.feedback.byKey.value', 'pushes B and C late', 10 + 40 > 10 + 10 + 40,
              'e-best-plan byKey value: D, C, B finishes C later than the best plan')
ex.claim(score(1300, 60) == 988 and score(1600, 50) == 1280, 'e-best-plan D, C, B: C scores 1,280 at 50 and B 988 at 60')

# ---------------------------------------------------------------- e-moves-back (BFS as the second method)
target = (47, 30)
dist, q = {(1, 1): 0}, deque([(1, 1)])
while q:
    a, b = q.popleft()
    if (a, b) == target:
        break
    for nx in ((a + b, b), (a, a + b)):
        if nx[0] <= 47 and nx[1] <= 47 and nx not in dist:
            dist[nx] = dist[(a, b)] + 1
            q.append(nx)
key('e-moves-back', dist[target])
walk, (a, b) = [target], target
while (a, b) != (1, 1):
    a, b = (a - b, b) if a > b else (a, b - a)
    walk.append((a, b))
ex.claim(len(walk) - 1 == 9 and walk == [(47, 30), (17, 30), (17, 13), (4, 13), (4, 9), (4, 5), (4, 1), (3, 1), (2, 1), (1, 1)], 'e-moves-back walk back as in the explain')
qs, (a, b) = [], (47, 30)
while b:
    qs.append(a // b)
    a, b = b, a % b
ex.claim(qs == [1, 1, 1, 3, 4] and sum(qs) - 1 == 9, f'e-moves-back Euclid quotients {qs}, sum - 1 = 9')
wrong('e-moves-back', 'steps', len(qs))
wrong('e-moves-back', 'quotients', sum(qs))
wrong('e-moves-back', 'sub', 47 - 30)

# ---------------------------------------------------------------- e-hand-cases (run the console code)
src = '\n'.join(IT['e-hand-cases']['canvas']['params']['lines'])
ns = {}
exec(src, ns)


def right_rise(a):
    best = run_ = 1
    for i in range(1, len(a)):
        run_ = run_ + 1 if a[i] > a[i - 1] else 1
        best = max(best, run_)
    return best


opts = {o['id']: eval(o['text'].strip('`')) for o in W('e-hand-cases')['options']}
wrongs_ = sorted(k for k, v in opts.items() if ns['longest_rise'](v) != right_rise(v))
ex.claim(wrongs_ == correct_ids('e-hand-cases'), f'e-hand-cases buggy function wrong on {wrongs_}')
ex.claim(ns['longest_rise']([5, 3, 1, 4, 6, 8, 2]) == 4 == right_rise([5, 3, 1, 4, 6, 8, 2]), 'e-hand-cases passes the example, answer 4')
ex.claim(ns['longest_rise']([1, 1, 2, 0]) == 3 and right_rise([1, 1, 2, 0]) == 2 and ns['longest_rise']([1, 2, 3]) == 1, 'e-hand-cases explain: 3 instead of 2, and 1')

# ---------------------------------------------------------------- e-round-review
ex.claim(120 - 41 == 79 and (2 * 10 ** 5) ** 2 // 2 == 2 * 10 ** 10 and 1300 - 1250 == 50, 'e-round-review 79 minutes, 2e10 steps, 50 above')


# ---------------------------------------------------------------- code items
def same(got, want):
    return got == want


def run_case(prelude, code, case):
    ns_ = {'__learner_source__': code}
    try:
        exec(prelude, ns_)
        exec(code, ns_)
        if case.get('setup'):
            exec(case['setup'], ns_)
        t0 = time.perf_counter()
        got = eval(case['call'], ns_)
        dt = time.perf_counter() - t0
    except Exception as e:  # noqa: BLE001
        return False, f'{type(e).__name__}: {e}', 0
    return same(got, eval(case['expect'], {})), got, dt


def run_script(code, stdin, timeout=60):
    t0 = time.perf_counter()
    try:
        out = subprocess.run([sys.executable, '-I', '-c', code], input=stdin, capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return None, timeout
    return out, time.perf_counter() - t0


def norm(s):
    return '\n'.join(line.rstrip() for line in s.strip().split('\n'))


def slow(iid, name, code, case_no, limit=5.0):
    """A slow version runs one hidden test in a subprocess; it must not finish inside the limit natively."""
    w = W(iid)
    case = w['tests'][case_no - 1]
    if 'stdin' in case:
        out, dt = run_script(code, case['stdin'], timeout=limit)
    else:
        prog = w.get('prelude', '') + '\n' + code + '\n' + (case.get('setup') or '') + '\n' + f'print({case["call"]})'
        out, dt = run_script(prog, '', timeout=limit)
    ex.claim(out is None, f'{iid} slow version "{name}" does not finish test {case_no} in {limit:.0f} s natively'
             + ('' if out is None else f' (took {dt:.2f} s)'))


def code_item(iid, mutants=()):
    w = W(iid)
    cases = [('example', c) for c in w['examples']] + [('test', c) for c in w['tests']]
    if any('stdin' in c for _, c in cases):
        res = []
        for _, c in cases:
            out, dt = run_script(w['solution'], c['stdin'])
            res.append((out is not None and norm(out) == norm(c['expect']), dt))
        ex.claim(all(r[0] for r in res), f'{iid} solution passes {sum(r[0] for r in res)} of {len(res)} examples and tests (script mode)')
        ex.claim(max(r[1] for r in res) < 1.5, f'{iid} slowest case {max(r[1] for r in res):.2f} s natively, process start included')
        st = [norm(run_script(w['starter'], c['stdin'])[0] or '') == norm(c['expect']) for k, c in cases if k == 'test']
        ex.claim(not any(st), f'{iid} starter fails every hidden test ({st.count(False)} of {len(st)})')
        run = lambda code, c: (norm(run_script(code, c['stdin'])[0] or '') == norm(c['expect']),)  # noqa: E731
    else:
        res = [run_case(w.get('prelude', ''), w['solution'], c) for _, c in cases]
        ex.claim(all(r[0] for r in res), f'{iid} solution passes {sum(r[0] for r in res)} of {len(res)} examples and tests',
                 '; '.join(f'case {i}: {r[1]!r}'[:160] for i, r in enumerate(res) if not r[0]))
        ex.claim(max(r[2] for r in res) < 1.0, f'{iid} slowest call {max(r[2] for r in res):.2f} s natively, inside the 5 s limit')
        st = [run_case(w.get('prelude', ''), w['starter'], c)[0] for k, c in cases if k == 'test']
        ex.claim(not any(st), f'{iid} starter fails every hidden test ({st.count(False)} of {len(st)})')
        run = lambda code, c: run_case(w.get('prelude', ''), code, c)  # noqa: E731
    dup = [i + 1 for i, t in enumerate(w['tests']) if any(t.get('call') == e.get('call') and t.get('setup') == e.get('setup')
                                                          and t.get('stdin') == e.get('stdin') for e in w['examples'])]
    ex.claim(True, f'{iid}: hidden tests identical to an example: {dup}')
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i + 1 for i, c in enumerate(w['tests']) if not run(bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')
    n_how = len(w['tests'])
    ex.claim(f'{n_how} hidden tests' in w['how'] or f'{n_how} times' in w['how'], f'{iid} how names {n_how} tests')


code_item('e-code-pairs', [
    ('lines, not tokens', 'data = sys.stdin.read().split()', 'data = [x for line in sys.stdin.read().split("\\n")[:1] for x in line.split()]\ndata += sys.stdin.read().split()'),
    ('sign only', 'Counter(map(int, data[pos:pos + n]))', 'Counter(abs(int(v)) for v in data[pos:pos + n])'),
    ('position stuck', '    pos += n\n', ''),
])
pairs_double = '''import sys
data = sys.stdin.read().split()
t = int(data[0]); pos = 1; out = []
for _ in range(t):
    n = int(data[pos]); pos += 1
    a = data[pos:pos + n]; pos += n
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] == a[j]:
                c += 1
    out.append(c)
print("\\n".join(map(str, out)))
'''
pairs_count = pairs_double.replace('''    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] == a[j]:
                c += 1''', '''    c = sum(a.count(v) - 1 for v in a) // 2''')
slow('e-code-pairs', 'double loop', pairs_double, 7)
slow('e-code-pairs', 'list.count per value', pairs_count, 7, limit=2.0)
big = W('e-code-pairs')['tests'][6]['stdin'].split()
ex.claim(int(big[1]) == 32000 and (32000 * 31999 // 2) > 5 * 10 ** 8, 'e-code-pairs how: 32,000 values, at least 5e8 comparisons pairwise')

code_item('e-code-quiet', [
    ('no spare cell', 'diff = [0] * (n + 2)', 'diff = [0] * (n + 1)'),
    ('>= cap', 'if total > cap:', 'if total >= cap:'),
    ('no -v', 'diff[r + 1] -= v', 'pass'),
])
quiet_loop = '''def days_over(n, updates, cap):
    h = [0] * (n + 1)
    for l, r, v in updates:
        for d in range(l, r + 1):
            h[d] += v
    return sum(1 for d in range(1, n + 1) if h[d] > cap)
'''
slow('e-code-quiet', 'range loop', quiet_loop, 7)
ns_q = {}
exec(W('e-code-quiet')['prelude'], ns_q)
ups = ns_q['_updates'](200000, 200000, 25)
adds = sum(r_ - l_ + 1 for l_, r_, _ in ups)
ex.claim(5e9 < adds < 2e10, f'e-code-quiet how: the range loop makes {adds:.3g} additions, "about 10^10"')

code_item('e-code-geom', [
    ('no g = 1 case', '    if g % MOD == 1:\n        return n % MOD            # every term is 1\n', ''),
    ('floor division', 'return top * pow(g - 1, MOD - 2, MOD) % MOD', 'return top // (g - 1) % MOD'),
    ('n not reduced', 'return n % MOD            # every term is 1', 'return n'),
])
ns_g = {}
exec(W('e-code-geom')['solution'], ns_g)
for g_, n_ in [(2, 5), (3, 1), (0, 4), (1, 7), (10 ** 9 + 6, 2), (5, 30), (10, 10 ** 6)]:
    direct = sum(pow(g_, i, 10 ** 9 + 7) for i in range(n_)) % (10 ** 9 + 7)
    ex.claim(ns_g['growth_sum'](g_, n_) == direct, f'e-code-geom growth_sum({g_}, {n_}) = direct sum {direct}')


def doubling(g_, n_, m=10 ** 9 + 7):
    """(sum of g^i for i < n, g^n) by halving n: an independent route for n near 1e18."""
    if n_ == 0:
        return 0, 1
    s, pw = doubling(g_, n_ // 2, m)
    s, pw = (s + s * pw) % m, pw * pw % m
    if n_ % 2:
        s, pw = (s + pw) % m, pw * g_ % m
    return s, pw


for g_, n_ in [(1, 10 ** 18), (3, 10 ** 18), (10 ** 9 + 6, 10 ** 18 + 1), (123456789, 987654321987654321)]:
    ex.claim(ns_g['growth_sum'](g_, n_) == doubling(g_, n_)[0], f'e-code-geom growth_sum({g_}, {n_}) by doubling')
ex.claim(10 ** 18 % (10 ** 9 + 7) == 49, 'e-code-geom 10^18 mod p = 49')

code_item('e-code-vans', [
    ('neighbours sorted', '''    w = sorted(weights)
    i, j = 0, len(w) - 1
    vans = 0
    while i <= j:
        if i < j and w[i] + w[j] <= cap:
            i += 1                # the lightest rides with the heaviest
        j -= 1                    # the heaviest always leaves
        vans += 1
    return vans''', '''    w = sorted(weights)
    i, vans = 0, 0
    while i < len(w):
        if i + 1 < len(w) and w[i] + w[i + 1] <= cap:
            i += 2
        else:
            i += 1
        vans += 1
    return vans'''),
    ('no sort', 'w = sorted(weights)', 'w = list(weights)'),
    ('heaviest with next', 'if i < j and w[i] + w[j] <= cap:', 'if i < j and w[j - 1] + w[j] <= cap:'),
])


def vans_brute(ws, cap):
    """Fewest vans by a bitmask DP over the orders (small n): an independent route."""
    n_ = len(ws)
    full = (1 << n_) - 1
    dp = [math.inf] * (1 << n_)
    dp[0] = 0
    for m in range(1 << n_):
        if dp[m] == math.inf or m == full:
            continue
        i = next(b for b in range(n_) if not m >> b & 1)
        dp[m | 1 << i] = min(dp[m | 1 << i], dp[m] + 1)
        for j in range(i + 1, n_):
            if not m >> j & 1 and ws[i] + ws[j] <= cap:
                dp[m | 1 << i | 1 << j] = min(dp[m | 1 << i | 1 << j], dp[m] + 1)
    return dp[full]


for c in W('e-code-vans')['tests'][:6]:
    args = eval(c['call'].replace('fewest_vans', ''))
    ex.claim(vans_brute(*args) == int(c['expect']), f'e-code-vans {c["call"]} = {c["expect"]} by a bitmask DP')
vans_scan = '''def fewest_vans(weights, cap):
    w = sorted(weights)
    used = [False] * len(w)
    vans = 0
    for j in range(len(w) - 1, -1, -1):
        if used[j]:
            continue
        used[j] = True
        for i in range(j):
            if not used[i] and w[i] + w[j] <= cap:
                used[i] = True
                break
        vans += 1
    return vans
'''
slow('e-code-vans', 'partner scan', vans_scan, 8)
ex.claim(abs(200000 ** 2 / 2 - 2e10) < 1, 'e-code-vans how: about 2e10 pair checks at 200,000 orders')

code_item('e-code-conflicts', [
    ('n - 1 bits', 'for mask in range(1 << n):', 'for mask in range(1 << max(n - 1, 0)):'),
    ('ignore clashes', 'if mask >> i & 1 and clash[i] & mask:', 'if False:'),
])
ns_c = {}
exec(W('e-code-conflicts')['prelude'], ns_c)


def least_conflicted(n_, es):
    """Greedy: repeatedly take the remaining strategy with fewest remaining conflicts (lowest number on a tie)."""
    adj = {v: set() for v in range(n_)}
    for a_, b_ in es:
        adj[a_].add(b_)
        adj[b_].add(a_)
    left, size = set(range(n_)), 0
    while left:
        v = min(left, key=lambda u: (len(adj[u] & left), u))
        size += 1
        left -= adj[v] | {v}
    return size


cs7 = ns_c['_edges'](8, 12, 69)
ex.claim(least_conflicted(8, cs7) < 4, f'e-code-conflicts test 7: least-conflicted greedy gives {least_conflicted(8, cs7)}, below 4')
conf_perm = '''from itertools import permutations
def largest_clear_set(n, conflicts):
    bad = set(map(frozenset, conflicts))
    best = 0
    for order in permutations(range(n)):
        kept = []
        for v in order:
            if all(frozenset((v, u)) not in bad for u in kept):
                kept.append(v)
        best = max(best, len(kept))
    return best
'''
slow('e-code-conflicts', 'every ordering', conf_perm, 8)

code_item('e-code-book', [
    ('zero for odd n', "        book = [1, 2, -3]         # one triple absorbs the odd position\n        k = 4", "        book = [0]\n        k = 1"),
    ('wrong triple', 'book = [1, 2, -3]', 'book = [1, 1, -2]'),
    ('None for n = 1 missing', '    if n == 1:\n        return None\n', ''),
])
ns_b = {}
exec(W('e-code-book')['prelude'] + '\n' + W('e-code-book')['solution'], ns_b)
for n_ in range(1, 8):   # only n = 1 has no book (search over every choice of n distinct non-zero sizes in [-n, n])
    has = any(sum(c) == 0 for c in itertools.combinations([v for v in range(-n_, n_ + 1) if v], n_))
    ex.claim(has == (n_ != 1), f'e-code-book n = {n_}: a book exists = {has}')
book_search = '''from itertools import combinations
def neutral_book(n):
    if n == 1:
        return None
    for c in combinations([v for v in range(-n, n + 1) if v], n):
        if sum(c) == 0:
            return list(c)
'''
slow('e-code-book', 'search over combinations', book_search, 7)

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
