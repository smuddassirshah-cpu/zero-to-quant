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
ex.claim(doc['minutes'] == 90 and doc['pass'] == 0.7, 'minutes 90 and pass 0.7 as stored')
# Rule: AUTHORING section 5 sets topic-exam `minutes` per file ("set it to the time the exam really needs") and defines
# item `pace` (seconds) for exams. The paces below sum to the minutes stored; learn.js examMinutes(140 h) = 60 is only the Learn chip.
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
ex.claim(not nopace, f'every item has a pace ({len(nopace)} without)')
paces = sum(it['pace'] for it in doc['items'])
ex.claim(all(isinstance(it['pace'], (int, float)) and 0 < it['pace'] <= 1800 for it in doc['items']), 'every pace is a positive number up to 1800')
ex.claim(paces == 5240 and 85 * 60 <= paces <= doc['minutes'] * 60, f'paces sum to {paces} s = {paces / 60:.1f} min, inside the {doc["minutes"]} minutes stored')
bylevel = {}
for it in doc['items']:
    bylevel.setdefault(it['difficulty'], []).append(it['pace'])
print(f'   paces by difficulty: { {d: sorted(set(v)) for d, v in sorted(bylevel.items())} }')

# ---------------------------------------------------------------- e-file-values
nm_max, sum_nm, t_max = 2000, 10 ** 6, 10 ** 4
key('e-file-values', sum_nm)
wrong('e-file-values', 'product', t_max * nm_max * nm_max)
wrong('e-file-values', 'grid', nm_max * nm_max)
wrong('e-file-values', 'tests', t_max)
ex.claim(nm_max * nm_max > sum_nm, 'e-file-values one 2,000 by 2,000 grid (4e6 cells) is forbidden by the cap of 1e6')
say('e-file-values', 'explain.text', 4 * 10 ** 6, fmt=lambda v: '4 \\cdot 10^6')
say('e-file-values', 'explain.text', 1000000, fmt=lambda v: '1,000,000')
ex.claim(any('10⁶' in ln for ln in IT['e-file-values']['canvas']['params']['lines']), 'e-file-values the Input section states the cap 10^6')

# ---------------------------------------------------------------- e-fast-read (names with spaces: tokens tear a name, lines keep it)
txt = '2\nNorth Desk\n15\nEast\n-3\n'
ex.claim(txt.splitlines() == ['2', 'North Desk', '15', 'East', '-3'], 'e-fast-read splitlines keeps each name whole')
ex.claim(txt.split() == ['2', 'North', 'Desk', '15', 'East', '-3'], 'e-fast-read split() tears North Desk into two tokens')
ex.claim('North Desk\n15'.split(' ') == ['North', 'Desk\n15'], 'e-fast-read split(" ") glues the newline to the next token')
ex.claim('North Desk'.split()[0] == 'North', 'e-fast-read option a keeps only the first word')
ex.claim(correct_ids('e-fast-read') == ['b'], 'e-fast-read key b')

# ---------------------------------------------------------------- e-lcm-rebalance
L = math.lcm(84, 90)
shared = [d for d in range(1, 10001) if d % 84 == 0 and d % 90 == 0]
key('e-lcm-rebalance', 10000 // L)
ex.claim(len(shared) == 7 and shared[0] == 1260 and shared[-1] == 8820, f'e-lcm-rebalance brute force over 10,000 days: {len(shared)} shared days, {shared[0]} to {shared[-1]}')
ex.claim(84 * 90 // math.gcd(84, 90) == 1260 and math.gcd(84, 90) == 6, 'e-lcm-rebalance lcm by 84*90/gcd')
wrong('e-lcm-rebalance', 'product', 10000 // (84 * 90))
wrong('e-lcm-rebalance', 'gcd', 10000 // math.gcd(84, 90))
wrong('e-lcm-rebalance', 'today', len(shared) + 1)
wrong('e-lcm-rebalance', 'first', L)
ex.claim(90 == 84 + 6 and 84 == 14 * 6 and math.gcd(84, 6) == 6 and 7 * 1260 == 8820 and 8 * 1260 == 10080, 'e-lcm-rebalance explain Euclid steps and multiples')
ex.claim(84 * 90 == 7560, 'e-lcm-rebalance byKey product 7,560')

# ---------------------------------------------------------------- e-greedy-tap (deadline jobs; every feasible subset as the second method)
jobs = {r[0]: (int(r[1]), int(r[2])) for r in IT['e-greedy-tap']['canvas']['params']['rows']}
names = [r[0] for r in IT['e-greedy-tap']['canvas']['params']['rows']]
tap = {f'r{i}': nm for i, nm in enumerate(names)}


def feasible(sub):
    """Every job can take its own day <= its deadline in 1..3 (Hall's condition by sorted deadlines)."""
    ds = sorted(jobs[j][0] for j in sub)
    return all(dl >= k + 1 for k, dl in enumerate(ds)) and len(ds) <= 3


def latest_free(order):
    free, kept = {1, 2, 3}, []
    for j in order:
        days = [x for x in free if x <= jobs[j][0]]
        if days:
            free.remove(max(days))
            kept.append(j)
    return sorted(kept)


def earliest_free(order):
    free, kept = {1, 2, 3}, []
    for j in order:
        days = [x for x in sorted(free) if x <= jobs[j][0]]
        if days:
            free.remove(days[0])
            kept.append(j)
    return sorted(kept)


by_pay = sorted(jobs, key=lambda j: -jobs[j][1])
rule = latest_free(by_pay)
ex.claim(sorted(tap[c] for c in W('e-greedy-tap')['answer']) == rule == ['A', 'D', 'E'], f'e-greedy-tap the rule keeps {rule}')
subs_ok = [s for r_ in range(7) for s in itertools.combinations(names, r_) if feasible(s)]
pay = lambda s: sum(jobs[j][1] for j in s)  # noqa: E731
top_pay = max(pay(s) for s in subs_ok)
ex.claim(top_pay == 150 and [s for s in subs_ok if pay(s) == top_pay] == [('A', 'D', 'E')], 'e-greedy-tap the optimum over every feasible subset is A, D, E at 150, unique')
wr = {x['id']: sorted(tap[c] for c in x['set']) for x in W('e-greedy-tap')['wrong']}
ex.claim(wr['earliest'] == earliest_free(by_pay) == ['D', 'E', 'F'] and pay(wr['earliest']) == 120, 'e-greedy-tap slip earliest free day keeps D, E, F for 120')
by_dl = sorted(jobs, key=lambda j: (jobs[j][0], names.index(j)))
ex.claim(wr['deadline'] == earliest_free(by_dl) == ['A', 'C', 'D'] and pay(wr['deadline']) == 140, 'e-greedy-tap slip by deadline keeps A, C, D for 140')
ex.claim(wr['top'] == sorted(by_pay[:3]) and not feasible(wr['top']), 'e-greedy-tap slip top three (D, A, B) is infeasible')
ex.claim(feasible(('A', 'B')) is False and jobs['A'][0] == jobs['B'][0] == 1, 'e-greedy-tap byKey top and r1: A and B both need day 1')
ex.claim(40 in [jobs[j][1] for j in jobs] and jobs['E'][1] == 40, "e-greedy-tap byKey deadline: E's 40 is missed")
ex.claim(len(rule) == 3 and not feasible(('A', 'D', 'E', 'C')), 'e-greedy-tap byKey r2 and r5: days are full when C and F come up')

# ---------------------------------------------------------------- e-upsolve-pick
r = 1250
ex.claim(correct_ids('e-upsolve-pick') == ['g', 'h'], 'e-upsolve-pick key G and H')
ex.claim(all(abs(v - r) <= 300 for v in (1400, 1350, 1500, 1450)), 'e-upsolve-pick all four ratings lie within 300 of 1,250, so the window does not decide')

# ---------------------------------------------------------------- e-next-problem
rows = IT['e-next-problem']['canvas']['params']['rows']
left = 120 - 70
cand = {f'r{i}': (int(x[1].replace(',', '')), int(x[2].split()[0])) for i, x in enumerate(rows) if x[2] != 'solved'}
fit = {k: v[0] / v[1] for k, v in cand.items() if v[1] <= left}
ex.claim(max(fit, key=fit.get) == W('e-next-problem')['answer'][0] == 'r3' and 'r4' not in fit, f'e-next-problem best fitting rate {fit}, E needs 60 > {left}')
ex.claim(1500 / 20 == 75 and round(1250 / 40, 2) == 31.25 and left == 50, 'e-next-problem rates 75 and 31.25, 50 minutes left')
wr = {x['id']: x['set'] for x in W('e-next-problem')['wrong']}
ex.claim(wr == {'letter': ['r2'], 'points': ['r4']}, 'e-next-problem slips: the next letter C, the most points E')
ex.claim(max(cand, key=lambda k: cand[k][0]) == 'r4', 'e-next-problem E has the most points')
say('e-next-problem', 'explain.text', 75, fmt=lambda v: '75')

# ---------------------------------------------------------------- e-pop-front (largest n with n(n-1)/2 <= 1e8)
budget = 10 ** 8
n_best = max(m for m in range(1, 20000) if m * (m - 1) // 2 <= budget)
key('e-pop-front', n_best)
ex.claim(math.isqrt(2 * budget) == 14142 and n_best == 14142, 'e-pop-front by isqrt(2e8) and a scan')
ex.claim(14142 * 14141 // 2 == 99_991_011 and 14143 * 14142 // 2 == 100_005_153, 'e-pop-front 99,991,011 fits and 100,005,153 does not')
for small in (1, 2, 5, 10):
    lst, shifts = list(range(small)), 0
    while lst:
        shifts += len(lst) - 1
        lst.pop(0)
    ex.claim(shifts == small * (small - 1) // 2, f'e-pop-front simulated shifts for n = {small}')
lst, shifts = list(range(14142)), 0
while lst:
    shifts += len(lst) - 1
    lst.pop(0)
ex.claim(shifts == 99_991_011, 'e-pop-front simulated drain of 14,142 orders makes 99,991,011 shifts')
wrong('e-pop-front', 'square', math.isqrt(budget))
wrong('e-pop-front', 'pops', budget)
say('e-pop-front', 'feedback.correct', 99991011, fmt=lambda v: '99{,}991{,}011')
say('e-pop-front', 'feedback.correct', 100005153, fmt=lambda v: '100,005,153')

# ---------------------------------------------------------------- e-budget-table
rows = W('e-budget-table')['rows']
want = [3000 ** 2, 2000 ** 3, 2 * 10 ** 5 * math.sqrt(2 * 10 ** 5), 25 * 2 ** 25]
for i, v in enumerate(want):
    a = rows[i][1]['answer']
    ex.claim(abs(a - v) <= abs(v) * rows[i][1]['tol']['rel'], f'e-budget-table row {i} steps {a} = {v:.6g}')
    ex.claim(rows[i][2]['answer'] == ('yes' if v <= 2e8 else 'no'), f'e-budget-table row {i} fits = {rows[i][2]["answer"]}')
ex.claim(rows[2][1]['answer'] == 89442719 and rows[3][1]['answer'] == 838860800, 'e-budget-table exact keys 89,442,719 and 838,860,800')
ex.claim(abs(math.sqrt(2e5) - 447.2) < 0.05, 'e-budget-table sqrt(2e5) = 447.2')
ex.claim(abs(8.9e7 - 2e5 * 447.2) <= 8.9e7 * 0.03 and abs(8.9e7 - want[2]) <= want[2] * 0.03, 'e-budget-table a typed 8.9e7 is graded right')
ex.claim(2000 ** 3 / 2e8 == 40, 'e-budget-table r1c1 "forty times the budget"')
ex.claim(round(838860800 / 2e8, 1) == 4.2, 'e-budget-table explain: four times over (4.2)')
say('e-budget-table', 'feedback.byKey.r3c1', 838860800, fmt=lambda v: '838{,}860{,}800')
say('e-budget-table', 'feedback.byKey.r0c1', 9000000, fmt=lambda v: '9{,}000{,}000')

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
crossed = {v for p in (2, 3) for v in range(p * p, 61, p)}
ex.claim(dim == crossed | {1}, 'e-sieve-tap faded cells are exactly 1 and the crossed multiples of 2 and 3 (from 4 and 9)')
standing = [v for v in range(2, 61) if v not in dim and any(v % d == 0 for d in range(2, v))]
ex.claim(standing == [25, 35, 49, 55] and sorted(num[c] for c in W('e-sieve-tap')['answer']) == standing, f'e-sieve-tap composites standing {standing}')
wr = {x['id']: sorted(num[c] for c in x['set']) for x in W('e-sieve-tap')['wrong']}
ex.claim(wr == {'one': [1], 'fives': [25, 35, 55]}, f'e-sieve-tap slips {wr}')
ex.claim(all(47 % d for d in range(2, 7)) and 51 % 3 == 0 and 51 in dim, 'e-sieve-tap byKey 47 prime, 51 crossed')
ex.claim(math.sqrt(60) < 8 and [v for v in range(25, 61, 5) if v not in crossed] == [25, 35, 55] and [v for v in range(49, 61, 7) if v not in crossed] == [49],
         'e-sieve-tap explain: sqrt 60 < 8, multiples of 5 from 25 and of 7 from 49')
ex.claim(min(p for p in range(2, 60) if standing[0] % p == 0) == 5 and min(p for p in range(2, 60) if standing[2] % p == 0) == 7, 'e-sieve-tap smallest prime factors 5 and 7')

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

# ---------------------------------------------------------------- e-fact-order (the stated order computes C(n, k); two lines are distractors)
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
ex.claim(W('e-fact-order')['answer'] == ['s1', 's2', 's3', 's4'] and W('e-fact-order')['distractors'] == ['d1', 'd2'], 'e-fact-order key s1 to s4, distractors d1 and d2')
ex.claim({ln['id'] for ln in W('e-fact-order')['lines']} == {'s1', 's2', 's3', 's4', 'd1', 'd2'} and all('why' in ln for ln in W('e-fact-order')['lines'] if ln['id'].startswith('d')),
         'e-fact-order six lines, each distractor has a why')
# d1 is correct but slow (one pow per entry); d2 run forwards gives wrong inverses
ex.claim(all(pow(fact[i], p - 2, p) == ifact[i] for i in range(0, N + 1, 7)), 'e-fact-order d1 gives the right values at one pow each (slow, not wrong)')
fwd = [0] * (N + 1)
fwd[0] = 1
for i in range(0, N):
    fwd[i + 1] = fwd[i] * (i + 1) % p
ex.claim(fwd[1:] != ifact[1:], 'e-fact-order d2 run forwards gives wrong inverses')
ex.claim(29.5 < math.log2(p - 2) < 30, 'e-fact-order about 30 squarings per pow')

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

# ---------------------------------------------------------------- e-submask-tap (masks disjoint from 1010)
g = IT['e-submask-tap']['canvas']['params']['cells']
mval = {f'r{i + 1}c{j + 1}': int(g[i][j], 2) for i in range(4) for j in range(4)}
disj = sorted(c for c, v in mval.items() if v & 0b1010 == 0)
ex.claim(disj == sorted(W('e-submask-tap')['answer']) and len(disj) == 2 ** 2, f'e-submask-tap masks disjoint from 1010: {sorted(mval[c] for c in disj)}')
ex.claim(sorted(mval[c] for c in disj) == sorted(s for s in range(16) if s & 0b0101 == s), 'e-submask-tap disjoint masks are the submasks of the complement 0101')
wr = {x['id']: sorted(x['set']) for x in W('e-submask-tap')['wrong']}
ex.claim(wr['sub'] == sorted(c for c, v in mval.items() if v & 0b1010 == v), 'e-submask-tap slip sub = submasks of 1010')
ex.claim(wr['nonzero'] == sorted(c for c in disj if mval[c] != 0), 'e-submask-tap slip nonzero = the disjoint masks without 0000')
ex.claim(mval['r1c3'] == 2 and mval['r1c3'] & 0b1010 == 2 and mval['r4c4'] == 15 and mval['r4c4'] & 0b1010 == 0b1010, 'e-submask-tap byKey r1c3 is 0010 (bit 1), r4c4 is 1111 (bits 1 and 3)')
ex.claim(0b1010 == 10, 'e-submask-tap 1010 is 10')

# ---------------------------------------------------------------- e-stress-gen (read the printed case)
xs, k = [2, 5, 2], 4
cnt = {
    'strict pairs i<j': sum(1 for i, j in itertools.combinations(range(3), 2) if xs[i] + xs[j] == k),
    'i<=j': sum(1 for i in range(3) for j in range(i, 3) if xs[i] + xs[j] == k),
    'ordered i!=j': sum(1 for i in range(3) for j in range(3) if i != j and xs[i] + xs[j] == k),
    'all ordered': sum(1 for i in range(3) for j in range(3) if xs[i] + xs[j] == k),
}
ex.claim(cnt == {'strict pairs i<j': 1, 'i<=j': 3, 'ordered i!=j': 2, 'all ordered': 4}, f'e-stress-gen counts {cnt}')
ex.claim(IT['e-stress-gen']['canvas']['params']['lines'][1:] == ['xs = [2, 5, 2], k = 4', 'brute force: 1', 'fast:        3'], 'e-stress-gen console shows xs, k, brute 1, fast 3')
ex.claim(correct_ids('e-stress-gen') == ['self'], 'e-stress-gen key self')
ex.claim(cnt['ordered i!=j'] == 2 and cnt['i<=j'] == 3, 'e-stress-gen: twice gives 2, self gives 3')
L_ = {o['id']: len(o['text']) for o in W('e-stress-gen')['options']}
ex.claim(not (L_['self'] >= 12 and all(L_['self'] > 1.5 * v for k_, v in L_.items() if k_ != 'self')), f'e-stress-gen key is not much longer than every distractor {L_}')

# ---------------------------------------------------------------- e-penalty-order (break-even solving time of P) and e-best-plan (decay v/250 a minute)
def score(v, t):
    return F(v) - F(v, 250) * t


def tie_gap(tp):
    """Score of P then Q minus Q then P, for P taking tp minutes and Q 45."""
    pq_ = score(900, tp) + score(1500, tp + 45)
    qp_ = score(1500, 45) + score(900, 45 + tp)
    return pq_ - qp_


ties = [tp for tp in range(1, 200) if tie_gap(tp) == 0]
key('e-penalty-order', ties[0])
ex.claim(ties == [27], f'e-penalty-order the orders tie only at tP = {ties} (scan 1 to 199)')
ex.claim(tie_gap(26) > 0 and tie_gap(28) < 0 and tie_gap(F(27)) == 0, 'e-penalty-order P first is better below 27 minutes and worse above')
ex.claim(F(900, 27) == F(1500, 45) * 1 and round(float(F(900, 27)), 1) == 33.3, 'e-penalty-order 900/27 = 1500/45 = 33.3 points a minute')
ex.claim(F(900 * 45, 1500) == 27, 'e-penalty-order tP = v_P t_Q / v_Q = 27')
wrong('e-penalty-order', 'inverted', int(F(1500 * 45, 900)))
wrong('e-penalty-order', 'same', 45)
sp, sq = score(900, 27) + score(1500, 72), score(1500, 45) + score(900, 72)
ex.claim(sp == sq == F(18708, 10), f'e-penalty-order both orders score {float(sp)} at tP = 27')
ex.claim(F(900, 250) * 45 - F(1500, 250) * 0 == F(162), 'e-penalty-order Q first costs P 3.6 * 45 = 162')
ex.claim(F(1500, 250) == 6 and F(900, 250) == F(18, 5) and 6 * 27 == 162, 'e-penalty-order 6 tP = 162 at 27')
ex.claim(min(score(900, 72) / 900, score(1500, 72) / 1500) > F(3, 10), 'e-penalty-order no problem reaches a 30% floor')
say('e-penalty-order', 'feedback.correct', 33.3)

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
# byKey "value": in D, C, B only B is pushed late (to minute 60, scoring 988); C ends at 50, earlier than in the best plan
dcb = [('D', 10), ('C', 50), ('B', 60)]
ex.claim(score(1300, 60) == 988 and score(1600, 50) == 1280 and score(1300, 20) - score(1300, 60) == 208 and score(1600, 50) - score(1600, 60) == 64,
         'e-best-plan D, C, B: B scores 988 at 60 (loses 208), C 1,280 at 50 (gains 64)')
ex.claim(int(plans[('D', 'B', 'C')] - plans[('D', 'C', 'B')]) == 144 == 208 - 64, 'e-best-plan the net 144 is 4,044 - 3,900')
ex.claim('B and C late' not in IT['e-best-plan']['feedback']['byKey']['value'] and 'minute 60' in IT['e-best-plan']['feedback']['byKey']['value'], 'e-best-plan byKey value now says only B is pushed, to minute 60')
say('e-best-plan', 'feedback.byKey.value', 988)

# ---------------------------------------------------------------- e-moves-back (squares cut from a 47 by 30 rectangle; simulation as the second method)
def cut_squares(a, b):
    count, sides = 0, []
    while a and b:
        s = min(a, b)
        sides.append(s)
        if a >= b:
            a -= b
        else:
            b -= a
        count += 1
    return count, sides


cnt_sq, sides = cut_squares(47, 30)
key('e-moves-back', cnt_sq)
ex.claim(sides == [30, 17, 13, 4, 4, 4, 1, 1, 1, 1], f'e-moves-back squares cut {sides}')
qs, (a, b) = [], (47, 30)
while b:
    qs.append(a // b)
    a, b = b, a % b
ex.claim(qs == [1, 1, 1, 3, 4] and sum(qs) == 10, f'e-moves-back Euclid quotients {qs}, sum 10')
ex.claim(math.gcd(47, 30) == 1 and sides[-1] == 1, 'e-moves-back the last side is the gcd 1')
ex.claim(47 == 1 * 30 + 17 and 30 == 1 * 17 + 13 and 17 == 1 * 13 + 4 and 13 == 3 * 4 + 1 and 4 == 4 * 1, 'e-moves-back explain division chain')
wrong('e-moves-back', 'steps', len(qs))
wrong('e-moves-back', 'moves', sum(qs) - 1)
wrong('e-moves-back', 'gcd', math.gcd(47, 30))
# area check: the squares tile 47 * 30
ex.claim(sum(s * s for s in sides) == 47 * 30, 'e-moves-back the squares tile the 47 by 30 floor (1410 tiles)')

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
    ex.claim(not dup, f'{iid}: no hidden test is identical to an example (identical: {dup})')
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
    ('no positive filter', 'if t > prev:', 'if t != prev:'),
    ('one per rise', 'count += t - prev   # a rise needs new updates', 'count += 1'),
    ('prev not carried', '        prev = t\n', ''),
])
nsq = {}
exec(W('e-code-quiet')['prelude'] + '\n' + W('e-code-quiet')['solution'], nsq)


def rises(t):
    return sum(max(0, b - a) for a, b in zip([0] + list(t), t))


def split_min_count(t):
    """Independent route: split at each minimum (recursion on a stack)."""
    total, stack = 0, [(list(t), 0)]
    while stack:
        seg, base = stack.pop()
        if not seg:
            continue
        m = min(seg)
        total += m - base
        cur = []
        for v in seg:
            if v == m:
                stack.append((cur, m))
                cur = []
            else:
                cur.append(v)
        stack.append((cur, m))
    return total


def bfs_fewest(t):
    """Independent route: BFS over holdings, one range update a step, never above the target."""
    n_ = len(t)
    start, goal = (0,) * n_, tuple(t)
    seen, q = {start}, deque([(start, 0)])
    while q:
        s, dd = q.popleft()
        if s == goal:
            return dd
        for l_ in range(n_):
            for r_ in range(l_, n_):
                nx = tuple(s[i] + (l_ <= i <= r_) for i in range(n_))
                if all(nx[i] <= goal[i] for i in range(n_)) and nx not in seen:
                    seen.add(nx)
                    q.append((nx, dd + 1))
    return None


for c in W('e-code-quiet')['examples'] + W('e-code-quiet')['tests'][:6]:
    arr = eval(c['call'][len('fewest_updates('):-1])
    ex.claim(bfs_fewest(arr) == int(c['expect']) == split_min_count(arr) == rises(arr), f'e-code-quiet {c["call"]} = {c["expect"]} by BFS, splitting at minima and the rise sum')
nsq_t = {}
exec(W('e-code-quiet')['prelude'], nsq_t)
t7 = nsq_t['_target'](30, 9, 26)
ex.claim(split_min_count(t7) == rises(t7) == int(W('e-code-quiet')['tests'][6]['expect']) == 52, 'e-code-quiet test 7 = 52 by splitting at minima and the rise sum')
t8 = list(range(1, 200001))
ex.claim(rises(t8) == int(W('e-code-quiet')['tests'][7]['expect']) == 200000, 'e-code-quiet test 8 = 200,000')
t9 = nsq_t['_target'](200000, 10 ** 9, 25)
ex.claim(rises(t9) == int(W('e-code-quiet')['tests'][8]['expect']) == sum(max(0, t9[i] - (t9[i - 1] if i else 0)) for i in range(len(t9))), f'e-code-quiet test 9 = {rises(t9)} by two routes')
quiet_split = """def fewest_updates(target):
    total, stack = 0, [(0, len(target), 0)]
    while stack:
        lo, hi, base = stack.pop()
        if lo >= hi:
            continue
        seg = target[lo:hi]
        m = min(seg)
        total += m - base
        start = lo
        for i in range(lo, hi):
            if target[i] == m:
                stack.append((start, i, m))
                start = i + 1
        stack.append((start, hi, m))
    return total
"""
quiet_peel = """def fewest_updates(target):
    t = list(target)
    count = 0
    while any(t):
        i = 0
        while i < len(t):
            if t[i] > 0:
                while i < len(t) and t[i] > 0:
                    t[i] -= 1
                    i += 1
                count += 1
            else:
                i += 1
    return count
"""
for t_ in ([2, 0, 2], [4, 1, 4], [1, 3, 2, 4, 0], [1, 2, 1, 2]):
    nsa, nsb = {}, {}
    exec(quiet_split, nsa)
    exec(quiet_peel, nsb)
    ex.claim(nsa['fewest_updates'](t_) == nsb['fewest_updates'](t_) == rises(t_), f'e-code-quiet slow versions are correct, only slow, on {t_}')
slow('e-code-quiet', 'split at each minimum', quiet_split, 8)
slow('e-code-quiet', 'peel one layer at a time', quiet_peel, 8)
slow('e-code-quiet', 'peel one layer at a time', quiet_peel, 9)

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
