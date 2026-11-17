"""Recompute every key, wrong value and printed number of the nine new topic-3.3 exam items (exam second item, session AG).

Each number is found twice: once by the closed form the explanation uses, once by brute force, simulation or a grid.
Run from anywhere: python3 docs/reports/exam-second-item-3.3-numbers.py (exit 0 when every check passes).
"""
import itertools
import json
import os
import random
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
EXAM = os.path.join(HERE, '..', '..', 'app', 'content', 'exams', 'topic-3.3.json')
ex = json.load(open(EXAM, encoding='utf-8'))
items = {i['id']: i for i in ex['items']}
fails = []
n_checks = 0


def check(ok, label):
    global n_checks
    n_checks += 1
    if not ok:
        fails.append(label)
        print('FAIL', label)


def close(a, b, t=1e-9):
    return abs(a - b) <= t


def key(iid):
    return items[iid]['widget']['answer']


def wrong(iid, wid):
    return next(w['value'] for w in items[iid]['widget']['wrong'] if w['id'] == wid)


def text(iid):
    return json.dumps(items[iid], ensure_ascii=False)


def wrongs_outside(iid):
    w = items[iid]['widget']
    a, t = w['answer'], w['tol']['abs']
    for x in w['wrong']:
        check(abs(x['value'] - a) > t + x['tol']['abs'], f'{iid}: wrong {x["id"]} outside the answer band')


# Shape: 36 items, 9 new, 3 removed, minutes pro rata
NEW = ['e-divide-4512', 'e-thousand-days', 'e-bags-any-fake', 'e-divides-forty', 'e-consecutive-numbers',
       'e-second-price-win', 'e-bluff-or-check', 'e-alerts-close', 'e-tree-plans']
check(len(ex['items']) == 36, 'exam holds 36 items')
check(all(n in items for n in NEW), 'every new item present')
check(not any(r in items for r in ['e-even-faces', 'e-edge-lift', 'e-ten-cards']), 'removed items gone')
mins = 75 * 36 / 30
check(mins == 90 and ex['minutes'] == 90, 'minutes 75 x 36 / 30 = 90')

# Every essential skill now has two auto items (pairs rule of engine-pass-ae-2)
auto = [i for i in ex['items'] if i.get('kind') != 'longform']
cnt = {}
for i in auto:
    for s in i.get('skills', []):
        cnt[s] = cnt.get(s, 0) + 1
check(min(cnt.values()) >= 2, 'no skill of the exam has fewer than two auto items')
check(set(cnt) == set(ex['skills']), 'every exam skill has auto items')

# 1. e-divide-4512: 4512 / 48 = 94
iid = 'e-divide-4512'
check(key(iid) == 94 and 4512 // 48 == 94 and 4512 % 48 == 0, f'{iid} key 94 by division')
check(sum(48 for _ in range(94)) == 4512, f'{iid} key 94 by repeated addition')
check(48 * 90 == 4320 and 4512 - 4320 == 192 and 192 == 48 * 4, f'{iid} 4320, 192, 48 x 4')
check(50 * 94 == 4700 and 2 * 94 == 188 and 4700 - 188 == 4512, f'{iid} check 4700 - 188')
check(48 * 93 == 4464 and 4512 - 4464 == 48, f'{iid} short: 48 x 93 = 4464, 48 over')
check(wrong(iid, 'place') == 940 and wrong(iid, 'point') == 9.4 and wrong(iid, 'short') == 93, f'{iid} wrongs')
check(48 * 940 > 45000 and round(48 * 9.4) == 451, f'{iid} 48 x 940 over 45,000; 48 x 9.4 about 451')
wrongs_outside(iid)

# 2. e-thousand-days: Monday + 1000 days
iid = 'e-thousand-days'
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
d = 0
for _ in range(1000):
    d = (d + 1) % 7
correct = [o for o in items[iid]['widget']['options'] if o.get('correct')]
check(days[d] == 'Sunday' and days[1000 % 7] == 'Sunday' and correct[0]['text'] == 'Sunday', f'{iid} key Sunday, two ways')
check(7 * 142 == 994 and 1000 - 994 == 6, f'{iid} 1000 = 7 x 142 + 6')
check(days[999 % 7] == 'Saturday', f'{iid} slip: today counted as day 1 gives Saturday')
check(days[(-6) % 7] == 'Tuesday', f'{iid} slip: backwards gives Tuesday')
check(days[(1 + 999) % 7] == 'Sunday', f'{iid} day 1 is Tuesday, day 1000 is Sunday')

# 3. e-bags-any-fake: fewest coins with distinct subset sums for 5 bags
iid = 'e-bags-any-fake'


def distinct(ws):
    sums = set()
    for r in range(len(ws) + 1):
        for c in itertools.combinations(ws, r):
            sums.add(sum(c))
    return len(sums) == 2 ** len(ws)


best = None
for ws in itertools.combinations_with_replacement(range(0, 21), 5):
    if distinct(ws) and (best is None or sum(ws) < sum(best)):
        best = ws
check(best is not None and sum(best) == 31, f'{iid} brute force: fewest coins 31')
check(2 ** 5 - 1 == 31 and distinct((1, 2, 4, 8, 16)) and sum((1, 2, 4, 8, 16)) == 31, f'{iid} bound 2^5 - 1 = 31, met by powers of 2')
check(key(iid) == 31 and 31 * 10 == 310 and 2 ** 5 == 32, f'{iid} key 31, 310 g, 32 patterns')
check(not distinct((1, 2, 3, 4, 5)) and 1 + 4 == 2 + 3 == 5 and sum(range(1, 6)) == wrong(iid, 'k-from-k'), f'{iid} k-from-k 15 fails: {{1,4}} and {{2,3}} both 5 g')
check(wrong(iid, 'patterns') == 32 and wrong(iid, 'one-each') == 5, f'{iid} wrongs 32 and 5')
check(not distinct((1, 1, 1, 1, 1)), f'{iid} one coin each tells only how many')
wrongs_outside(iid)

# 4. e-divides-forty: largest set in 1..40 with no divisor pair is 20, so 21 force a pair
iid = 'e-divides-forty'


def odd_part(n):
    while n % 2 == 0:
        n //= 2
    return n


classes = {}
for n in range(1, 41):
    classes.setdefault(odd_part(n), []).append(n)
check(len(classes) == 20 and sorted(classes) == list(range(1, 40, 2)), f'{iid} 20 odd parts 1 to 39')
check(all(b % a == 0 for c in classes.values() for a, b in zip(c, c[1:])), f'{iid} each class is a divisor chain')
top = list(range(21, 41))
check(len(top) == 20 and not any(b % a == 0 for a, b in itertools.combinations(top, 2)), f'{iid} 21 to 40: 20 numbers with no pair')
# second method: greedy largest antichain by exhaustive search on 1..12 matches ceil(n/2), and the chain cover bound gives 20 for 40
for n in range(1, 13):
    m = max(len(s) for r in range(n + 1) for s in itertools.combinations(range(1, n + 1), r)
            if not any(b % a == 0 for a, b in itertools.combinations(s, 2)))
    check(m == (n + 1) // 2, f'{iid} brute force largest pair-free set of 1..{n} is ceil(n/2)')
check(key(iid) == 21 == len(classes) + 1, f'{iid} key 21')
check(wrong(iid, 'boxes') == 20 and wrong(iid, 'all') == 41, f'{iid} wrongs 20 and 41')
wrongs_outside(iid)

# 5. e-consecutive-numbers: Ana 3, Ben 4, Ana speaks first
iid = 'e-consecutive-numbers'
states = {(a, b) for a in range(1, 60) for b in range(1, 60) if abs(a - b) == 1}


def first_know(true):
    S = set(states)
    for k in range(1, 30):
        sp = 0 if k % 2 == 1 else 1

        def knows(s):
            return len({t[1 - sp] for t in S if t[sp] == s[sp]}) == 1
        if knows(true):
            return k
        S = {s for s in S if not knows(s)}
    return None


check(first_know((3, 4)) == 3, f'{iid} simulation: first "I know" on statement 3, by Ana')
# second method: the hand argument. Statement 1 rules out a = 1; statement 2 rules out b in {1, 2}; Ana with 3 sees b in {2, 4}
after1 = {s for s in states if s[0] != 1}
ben_knows = {b for b in range(1, 59) if len({s[0] for s in after1 if s[1] == b}) == 1}
check(ben_knows == {1, 2}, f'{iid} after statement 1, Ben would know only with 1 or 2')
check({b for b in (2, 4)} - ben_knows == {4}, f'{iid} Ana with 3 is left with 4')
check(len({s[0] for s in after1 if s[1] == 4}) == 2, f'{iid} Ben with 4 still faces 3 or 5 at statement 2')
check([o['id'] for o in items[iid]['widget']['options'] if o.get('correct')] == ['ana-3'], f'{iid} key option ana-3')

# 6. e-second-price-win: E[max of two rivals | both below 90]
iid = 'e-second-price-win'
exact = F(2, 3) * 90
check(exact == 60 and key(iid) == 60, f'{iid} key 60 by the order-statistic rule')
N = 600
grid = [(i + 0.5) * 90 / N for i in range(N)]
num = sum(max(x, y) for x in grid for y in grid) / N ** 2
check(close(num, 60, 0.01), f'{iid} key 60 by a grid over the two rival values ({num:.4f})')
random.seed(1)
sims = []
while len(sims) < 200000:
    v = [random.uniform(0, 100), random.uniform(0, 100)]
    if max(v) < 90:
        sims.append(max(v))
check(close(sum(sims) / len(sims), 60, 0.3), f'{iid} simulation near 60')
check(wrong(iid, 'one-rival') == 45 and wrong(iid, 'unconditional') == round(200 / 3, 2) == 66.67, f'{iid} wrongs 45 and 66.67')
check(wrong(iid, 'seller') == 50 == F(3 - 1, 3 + 1) * 100 and wrong(iid, 'own-bid') == 90, f'{iid} wrongs 50 = (n-1)/(n+1) x 100 and 90')
wrongs_outside(iid)

# 7. e-bluff-or-check: 90(1 - c) - 60c = 0.2 x 90
iid = 'e-bluff-or-check'
c = F(90 - 18, 90 + 60)
check(F(1, 5) * 90 == 18 and c == F(72, 150) == F(12, 25) and close(float(c), key(iid)), f'{iid} key 0.48 by algebra')
scan = min((abs((90 * (1 - x / 10000) - 60 * x / 10000) - 18), x / 10000) for x in range(10001))[1]
check(close(scan, 0.48, 1e-4), f'{iid} key 0.48 by a scan over c')
check(close(wrong(iid, 'formula'), 90 / 150) and close(wrong(iid, 'no-loss'), 1 - 18 / 90), f'{iid} wrongs 0.6 and 0.8')
check(close(wrong(iid, 'folds'), 1 - 0.48) and round(60 / 210, 2) == wrong(iid, 'bluff-share'), f'{iid} wrongs 0.52 and 0.29 (60/210 = 0.2857)')
check(90 - 150 * 0.48 == 18, f'{iid} 90 - 150 x 0.48 = 18')
wrongs_outside(iid)

# 8. e-alerts-close: P(both < 1/2 | |X - Y| < 1/3)
iid = 'e-alerts-close'
pB = 1 - F(2, 3) ** 2
pAB = F(1, 4) - 2 * F(1, 2) * F(1, 6) ** 2
check(pB == F(5, 9) and F(1, 2) - F(1, 3) == F(1, 6) and 2 * F(1, 2) * F(1, 6) ** 2 == F(1, 36), f'{iid} 5/9, legs 1/6, corners 1/36')
check(pAB == F(2, 9) and pAB / pB == F(2, 5) and key(iid) == 0.4, f'{iid} key 2/5 = 0.4 by areas')
M = 1200
inB = inAB = 0
for i in range(M):
    x = (i + 0.5) / M
    for j in range(M):
        y = (j + 0.5) / M
        if abs(x - y) < 1 / 3:
            inB += 1
            if x < 0.5 and y < 0.5:
                inAB += 1
check(close(inAB / inB, 0.4, 0.002), f'{iid} key 0.4 by a {M} x {M} grid ({inAB / inB:.4f})')
check(wrong(iid, 'unconditional') == 0.25 and wrong(iid, 'joint') == round(2 / 9, 4), f'{iid} wrongs 0.25 and 0.2222')
check(wrong(iid, 'no-corners') == float(F(1, 4) / F(5, 9)) == 0.45 and wrong(iid, 'condition') == round(5 / 9, 4), f'{iid} wrongs 0.45 and 0.5556')
wrongs_outside(iid)

# 9. e-tree-plans: pure Nash cells of the tree's table, read from the canvas
iid = 'e-tree-plans'
nodes = items[iid]['canvas']['params']['nodes']['children']
P = {}
for a in nodes:
    for b in a['children']:
        P[(a['label'], b['label'])] = tuple(int(v) for v in re.findall(r'-?\d+', b['value']))
check(P == {('Left', 'X'): (1, 4), ('Left', 'Y'): (0, 3), ('Left', 'Z'): (4, 0),
            ('Right', 'X'): (5, 1), ('Right', 'Y'): (0, 0), ('Right', 'Z'): (2, 2)}, f'{iid} canvas payoffs as designed')
moves, answers = ['Left', 'Right'], ['X', 'Y', 'Z']
plans = list(itertools.product(answers, repeat=2))   # (after Left, after Right)


def pay(a, plan):
    return P[(a, plan[moves.index(a)])]


ne = [(a, pl) for a in moves for pl in plans
      if pay(a, pl)[0] >= max(pay(a2, pl)[0] for a2 in moves) and pay(a, pl)[1] >= max(pay(a, q)[1] for q in plans)]
check(len(ne) == 3 == key(iid), f'{iid} key 3 by checking all 18 cells')
check(set(ne) == {('Right', ('X', 'Z')), ('Right', ('Y', 'Z')), ('Left', ('X', 'Y'))}, f'{iid} cells Right-XZ, Right-YZ, Left-XY')
# second method: the explanation's count, on path best answer times off-path answers that hold Ana's switch
best = {a: max(answers, key=lambda b: P[(a, b)][1]) for a in moves}
count = 0
for a in moves:
    other = [m for m in moves if m != a][0]
    count += sum(1 for b in answers if P[(other, b)][0] <= P[(a, best[a])][0])
check(count == 3 and best == {'Left': 'X', 'Right': 'Z'}, f'{iid} count 3 by the path rule')
spe = max(moves, key=lambda a: P[(a, best[a])][0])
check(spe == 'Right' and wrong(iid, 'tree-only') == 1, f'{iid} one backward-induction cell')
check(sum(1 for c in ne if c[0] == 'Right') == wrong(iid, 'right-only') == 2, f'{iid} two Right cells')
naive = [(a, b) for a in moves for b in answers
         if P[(a, b)][0] >= max(P[(m, b)][0] for m in moves) and P[(a, b)][1] >= max(P[(a, c2)][1] for c2 in answers)]
check(len(naive) == wrong(iid, 'actions') == 0, f'{iid} single-answer table has 0 cells')
check(len(plans) == wrong(iid, 'plans') == 9, f'{iid} 9 plans')
check(P[('Right', 'Z')][0] == 2 and P[('Left', 'X')][0] == 1 and P[('Right', 'Y')][0] == 0, f'{iid} printed 2, 1 and 0')
wrongs_outside(iid)

print(f'{n_checks} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
