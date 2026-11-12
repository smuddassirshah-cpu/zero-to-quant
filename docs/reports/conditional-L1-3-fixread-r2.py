from fractions import Fraction as F
from itertools import product
import json, sys, random
base = sys.argv[1] if len(sys.argv) > 1 else "app/content/courses/conditional"

def post(prior, *lrs):
    o = prior / (1 - prior)
    for l in lrs:
        o *= l
    return o / (1 + o)

ok = True
def chk(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name)
    ok = ok and cond

# homework-1 item 0
dice = list(product(range(1, 7), repeat=2))
hi = [d for d in dice if sum(d) >= 10]
chk('hw1 six outcomes total>=10', len(hi) == 6 and F(sum(a == b for a, b in hi), len(hi)) == F(1, 3))
chk('hw1 option c 2/4', F(2, 4) == F(1, 2))

# homework-2 item 2
p = post(F(5, 100), F(95, 10), F(20, 98))
chk('hw2 two tests 5/54', p == F(5, 54) and abs(float(p) - 0.0926) < 0.003)
chk('hw2 slips', abs(float(post(F(1, 20), F(95, 10))) - 0.3333) < .002 and abs(float(post(F(1, 20), F(95, 10), 40)) - 0.9524) < .002)
# homework-2 item 5
p = post(F(10, 200), 16, 16)
chk('hw2 backtest 256/275', p == F(256, 275) and abs(float(p) - 0.9309) < .002)
chk('hw2 backtest slips', abs(float(post(F(1, 20), 16)) - .4571) < .002 and abs(256 / 257 - .9961) < .001)
chk('hw2 counts', 10 * .8 * .8 == 6.4 and abs(190 * .05 * .05 - .475) < 1e-12)

# l1 screen 6: exhaustive check of the rule on a fair die:
# P(A|B)=P(A) iff share of A among removed outcomes equals P(A) (B proper, non-empty)
faces = range(1, 7)
good = True
for am in range(1, 63):
    A = {f for f in faces if am >> (f - 1) & 1}
    for bm in range(1, 63):
        B = {f for f in faces if bm >> (f - 1) & 1}
        R = set(faces) - B
        same = F(len(A & B), len(B)) == F(len(A), 6)
        share_same = F(len(A & R), len(R)) == F(len(A), 6)
        if same != share_same:
            good = False
chk('l1 rule: chance changes iff removed outcomes hold a different share of event (all A,B on a die)', good)
chk('l1 removed {5,6} half even', F(1, 2) == F(len({6}), 2))

# l11 screen 8
d = json.load(open(base + '/l11-updating-twice.json'))
s = d['screens'][8]
lv = s['canvas']['params']['levels']
pr = {b['id']: F(b['p']) for b in lv[0]['branches']}
leaves = {k: F(v) for k, v in s['canvas']['params']['leaves'].items()}
exp = {}
for b in lv[1]['branches']:
    for u, pv in b['p'].items():
        exp[u + '-' + b['id']] = pr[u] * F(pv)
chk('l11 s8 leaves are path products', exp == leaves)
chk('l11 s8 leaves sum to 1', sum(leaves.values()) == 1)
chk('l11 s8 second-level branches sum to 1', all(sum(F(b['p'][u]) for b in lv[1]['branches']) == 1 for u in pr))
key = leaves['u-b'] / (leaves['u-b'] + leaves['d-b'])
chk('l11 s8 key 49/58', key == F(49, 58) and abs(float(key) - s['widget']['answer']) < 0.0001)
chk('l11 s8 odds route', post(F(1, 2), F(7, 3), F(7, 3)) == F(49, 58))
w = {x['id']: x['value'] for x in s['widget']['wrong']}
chk('l11 s8 slip one = 0.7', w['one'] == 0.7 and post(F(1, 2), F(7, 3)) == F(7, 10))
chk('l11 s8 slip joint = leaf u-b 0.245; divisor 0.29', F(str(w['joint'])) == leaves['u-b'] and leaves['u-b'] + leaves['d-b'] == F(29, 100))
chk('l11 s8 slip likelihood = 0.49, other 0.09', F(str(w['likelihood'])) == F(7, 10) ** 2 and F(3, 10) ** 2 == F(9, 100))
chk('l11 s8 slip either = 0.91 = 1-0.3^2', F(str(w['either'])) == 1 - F(3, 10) ** 2)
vals = [s['widget']['answer']] + list(w.values())
tol = [s['widget']['tol']['abs']] + [x['tol']['abs'] for x in s['widget']['wrong']]
chk('l11 s8 no tolerance overlap', all(abs(vals[i] - vals[j]) > tol[i] + tol[j] for i in range(len(vals)) for j in range(i)))
# simulation
random.seed(1)
n = 400000; both = up_both = 0
for _ in range(n):
    up = random.random() < .5
    a = up if random.random() < .7 else not up
    b = up if random.random() < .7 else not up
    if a and b:
        both += 1; up_both += up
est = up_both / both
chk('l11 s8 simulation %.4f near 0.8448 (and P(both up) %.4f near 0.29)' % (est, both / n), abs(est - 49 / 58) < .005 and abs(both / n - .29) < .003)
# screen 9 copy
chk('l11 s9 copy gives 0.7', post(F(1, 2), F(7, 3), 1) == F(7, 10))
# quiz
chk('l11 q0 0.6 and slips', post(F(1, 5), 2, 3) == F(3, 5) and abs(float(post(F(1, 5), 2)) - .3333) < .002 and abs(float(post(F(1, 5), 3)) - .4286) < .002 and abs(.2 * 6 - 1.2) < 1e-9)
chk('l11 q1 0.3', post(F(3, 10), 4, F(1, 4)) == F(3, 10))
# review-2
chk('review-2 0.5 and slips', post(F(1, 10), 3, 3) == F(1, 2) and post(F(1, 10), 3) == F(1, 4) and F(6, 9) / (1 + F(6, 9)) == F(2, 5))

# l12
pri = [F(1, 3)] * 3
lik5 = [0, F(1, 6), F(1, 8)]
prod_ = [a * b for a, b in zip(pri, lik5)]
po = [x / sum(prod_) for x in prod_]
chk('l12 s3 posteriors 0,4/7,3/7; both gained; gains sum 1/3; 6 gained more',
    po == [0, F(4, 7), F(3, 7)] and po[1] > pri[1] and po[2] > pri[2] and (po[1] - pri[1]) + (po[2] - pri[2]) == F(1, 3) and po[1] - pri[1] > po[2] - pri[2])
lik3 = [F(1, 4), F(1, 6), F(1, 8)]
p2 = [a * b for a, b in zip(po, lik3)]
p2 = [x / sum(p2) for x in p2]
chk('l12 s5 3 suits d4 best; posts 0, .64, .36', lik3[0] == max(lik3) and p2 == [0, F(16, 25), F(9, 25)])

# l13 s9 tally
d = json.load(open(base + '/l13-knowing-nothing.json'))
rows = d['screens'][9]['canvas']['params']['rows']
t = {}
for r in rows:
    t[(r[1], r[2])] = t.get((r[1], r[2]), 0) + 1
chk('l13 s9 tally 7,3,3,7', t == {('Up', 'Up'): 7, ('Up', 'Down'): 3, ('Down', 'Up'): 3, ('Down', 'Down'): 7})
chk('l13 q1 0.2 > 0', F(4, 10) * F(5, 10) == F(1, 5))

# l15 coins
om = list(product('HT', repeat=2))
A = {o for o in om if o[0] == 'H'}; B = {o for o in om if o[1] == 'H'}; C = {o for o in om if o[0] == o[1]}
P = lambda S: F(len(S), 4)
chk('l15 coins pairwise yes, mutual no (1/4 vs 1/8)', P(A & B) == P(A) * P(B) and P(A & C) == P(A) * P(C) and P(B & C) == P(B) * P(C) and P(A & B & C) == F(1, 4) != P(A) * P(B) * P(C))

# l16 explain-away: for a grid of b, c in (0,1)
good = True
for b in [F(i, 10) for i in range(1, 10)]:
    for c in [F(i, 10) for i in range(1, 10)]:
        pL = b + c - b * c
        pB_L = b / pL
        pB_LC = (b * c) / c
        if not (pB_L > b and pB_LC == b and pB_LC < pB_L):
            good = False
chk('l16 q2: P(B|L)>P(B); P(B|L,C)=P(B) exactly; falls', good)
sys.exit(0 if ok else 1)
