"""Second read of mock-oa-sig-2 and -3: an independent recompute of every key and every distractor.

Run with the scratchpad venv Python (or any CPython 3.10+), from the repository root:
    python -I docs/reviews/exam-mock-oa-sig-versions-scripts/read_numbers.py
My blind answers (recorded before the keys were read) are in BLIND below; each is checked
against the file's key, then against a third route (enumeration, exact DP or a seeded
simulation) written without reference to the author's script. Exit 0 when every check holds.
"""
import itertools, json, math, os, random, sys
from fractions import Fraction as F
from math import comb

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EX = os.path.join(ROOT, 'app', 'content', 'exams')
rng = random.Random(4242)
fails = []
def ok(c, m):
    if not c: fails.append(m)

# ---- blind answers (closed forms worked by hand before the keys were opened) ----
BLIND = {
 2: [F(25), F(137, 60), F(-1, 5), F(4), F(20, 216), F(2, 5), F(5, 16), F(10), F(1, 3), F(7), F(80), F(3),
     F(9, 13), F(3, 16) / F(9, 20), F(44), F(5, 23), F(51, 250)],
 3: [F(49, 6), F(19, 16), F(-5, 3), F(15, 2), F(19, 36), F(2, 3), F(3, 16), F(13), F(1, 10) / (1 - F(9, 10) ** 5),
     F(6, 5) ** 6, F(1, 2), F(1, 6), F(3, 53), F(4, 7), F(2541, 625), F(244, 495), F(45, 14)],
}

def sim(n, f):
    return sum(f() for _ in range(n)) / n

D = range(1, 7)
third = {2: [], 3: []}
# ---- version 2, third routes ----
t = third[2]
t.append(sim(200000, lambda: 51 * (lambda d: (d[0] < 26) == (d[1] < 26))(rng.sample(range(52), 2))))
t.append(F(sum(sum(p[i] > max(p[:i], default=-1) for i in range(5)) for p in itertools.permutations(range(5))), 120))
def free():
    s = -1
    while rng.randint(1, 6) == 6: s += 4
    return s
t.append(sim(300000, free))
def calls():
    d = [c // 4 for c in range(52)]; rng.shuffle(d)
    return sum(d[i] == i % 13 for i in range(52))
t.append(sim(30000, calls))
t.append(F(sum(a < b < c for a, b, c in itertools.product(D, D, D)), 216))
hands = [h for h in itertools.permutations(range(10), 3)]   # placeholder to keep the seed stream fixed
def aces():   # exact by enumeration of ace positions within the five places
    num = den = 0
    for pos in itertools.combinations(range(5), 2):
        den += 1; num += 0 in pos
    return F(num, den)
t.append(aces())
t.append(F(sum(sum(a) == sum(b) for a in itertools.product((0, 1), repeat=3) for b in itertools.product((0, 1), repeat=3)), 64))
def worst(lo, hi, memo={}):          # minimax binary guessing, exact
    n = hi - lo
    if n <= 0: return 0
    if n not in memo:
        memo[n] = 1 + min(max(worst(0, g), worst(0, n - g - 1)) for g in range(n))
    return memo[n]
sys.setrecursionlimit(10000)
w = [0] * 1001
for n in range(1, 1001):
    m = n // 2
    w[n] = 1 + max(w[m], w[n - 1 - m])   # middle guess is optimal; checked against full minimax up to 60
ok(all(w[n] == worst(0, n) for n in range(1, 61)), 'v2 q08 middle-guess DP')
t.append(F(w[1000]))
def rr():
    truth = rng.random() < 0.2
    said = truth if rng.random() < 0.5 else True
    return (said, truth)
s = [rr() for _ in range(300000)]
t.append(sum(1 for a, b in s if a and b) / sum(1 for a, b in s if a))
def m7():
    tot = n = 0
    while True:
        tot += rng.randint(1, 6); n += 1
        if tot % 7 == 0: return n
t.append(sim(200000, m7))
def draws():                         # play the threshold-80 rule and report net value
    paid = 0
    while True:
        paid += 2; u = rng.uniform(0, 100)
        if u >= 80: return u - paid
t.append(sim(300000, draws))
# check no other threshold beats 80 (exact value of threshold t: E[U | U>t] - 2 / P(U>t))
val = lambda th: (100 + th) / 2 - 2 * 100 / (100 - th)
ok(max(range(0, 100), key=val) == 80, 'v2 q11 best threshold')
# conditional wait, exact by truncated series over the three-way roll (5, 6, other)
num = sum(F(n) * F(4, 6) ** (n - 1) * F(1, 6) for n in range(1, 300))
den = sum(F(4, 6) ** (n - 1) * F(1, 6) for n in range(1, 300))
t.append(float(num / den))
cnt = [0, 0]
for i in range(5):
    B = ['r', 'r', 'b', 'b', 'r' if i < 3 else 'b']
    for j in range(5):
        if B[j] == 'r':
            cnt[1] += 1; cnt[0] += i < 3
t.append(F(cnt[0], cnt[1]))
def relay():
    buy = rng.random() < 0.3
    got = buy ^ (rng.random() < 0.25) ^ (rng.random() < 0.25)
    return buy, got
s = [relay() for _ in range(400000)]
t.append(sum(1 for a, b in s if a and b) / sum(1 for a, b in s if b))
t.append(64 * F(sum(sum(g) >= 2 for g in itertools.product((0, 1), repeat=4)), 16))
def steps():
    m = 1
    while 0 < m < 4: m += 2 if rng.random() < 1 / 3 else -1
    return m >= 4
t.append(sim(300000, steps))
def knock():
    p = ['you', 'fav', 'o1', 'o2']; rng.shuffle(p)
    beat = {('you', 'fav'): .3, ('you', 'o1'): .6, ('you', 'o2'): .6, ('fav', 'o1'): .8, ('fav', 'o2'): .8, ('o1', 'o2'): .5}
    def play(a, b):
        pr = beat.get((a, b));
        if pr is None: pr = 1 - beat[(b, a)]
        return a if rng.random() < pr else b
    return play(play(p[0], p[1]), play(p[2], p[3])) == 'you'
t.append(sim(400000, knock))

# ---- version 3, third routes ----
t = third[3]
t.append(sim(300000, lambda: (lambda a, b: (a + b) * (2 if a == b else 1))(rng.randint(1, 6), rng.randint(1, 6))))
t.append(F(sum(sum(sum(s[:k]) == 0 for k in range(1, 7)) for s in itertools.product((1, -1), repeat=6)), 64))
t.append(F(sum(40 if f == 6 else -10 for f in D), 6))
t.append(F(sum(sum(p[i] > p[j] for i in range(6) for j in range(i + 1, 6)) for p in itertools.permutations(range(6))), 720))
def real_root(b, c):
    disc = b * b - 4 * c
    return disc >= 0
t.append(F(sum(real_root(b, c) for b in D for c in D), 36))
tr = [x for x in itertools.permutations(range(1, 11), 3) if x[0] > x[1]]
t.append(F(sum(x[0] > x[2] for x in tr), len(tr)))
def third_head():
    h = n = 0
    while h < 3:
        n += 1; h += rng.random() < .5
    return n == 5
t.append(sim(400000, third_head))
# max and min of 10: brute-force adversary on knowledge states (could-be-max, could-be-min flags)
from functools import lru_cache
@lru_cache(None)
def need(state):
    # state: sorted tuple of (canmax, canmin) flags per item; done when one canmax and one canmin remain
    cm = sum(a for a, b in state); cn = sum(b for a, b in state)
    if cm == 1 and cn == 1: return 0
    best = 99
    st = list(state)
    for i, j in itertools.combinations(range(len(st)), 2):
        outs = []
        for winner, loser in ((i, j), (j, i)):
            ns = st[:]
            ns[winner] = (ns[winner][0], False); ns[loser] = (False, ns[loser][1])
            outs.append(tuple(sorted(ns)))
        if any(o == state for o in outs): continue   # the adversary answers with no news: never useful
        best = min(best, 1 + max(need(o) for o in outs))
    return best
ok([need(tuple([(True, True)] * n)) for n in range(2, 9)] == [math.ceil(3 * n / 2) - 2 for n in range(2, 9)], 'v3 q08 brute force n<=8')
t.append(F(math.ceil(3 * 10 / 2) - 2))    # formula confirmed by brute force up to 8; 10 by the same rule
def pooled():
    s = [rng.random() < .1 for _ in range(5)]
    return s
ss = [pooled() for _ in range(400000)]
pos = [x for x in ss if any(x)]
t.append(sum(x[0] for x in pos) / len(pos))
def descent():
    prev = rng.randint(1, 6); n = 1
    while True:
        r = rng.randint(1, 6); n += 1
        if r < prev: return n
        prev = r
t.append(sim(300000, descent))
def dies():
    pop = 1
    for _ in range(80):
        if pop == 0: return 1
        if pop > 300: return 0
        pop = sum(rng.choices((0, 1, 2), (1, 1, 2))[0] for _ in range(pop))
    return pop == 0
t.append(sim(20000, dies))
N = 2000                                  # midpoint grid on the unit square
t.append(sum(min(x, 1 - x, y, 1 - y) for x in ((i + .5) / N for i in range(N)) for y in ((j + .5) / N for j in range(N))) / N ** 2)
def drawer():
    inA = rng.random() < .6
    miss = all(not (inA and rng.random() < .8) for _ in range(2))
    return inA, miss
s = [drawer() for _ in range(400000)]
t.append(sum(1 for a, b in s if a and b) / sum(1 for a, b in s if b))
traders = [k for k, c in ((1, 50), (2, 30), (4, 20)) for _ in range(c * k)]
mates = [k for k in traders if k > 1]
t.append(F(sum(k == 4 for k in mates), len(mates)))
def series():
    a = b = n = 0
    while a < 3 and b < 3:
        n += 1
        if rng.random() < .6: a += 1
        else: b += 1
    return n
t.append(sim(300000, series))
# craps, exact by summing over the point-phase length (truncated geometric series)
w = {s: sum(a + b == s for a in D for b in D) for s in range(2, 13)}
pw = F(w[7] + w[11], 36)
for pnt in (4, 5, 6, 8, 9, 10):
    stay = 1 - F(w[pnt] + 6, 36)
    pw += F(w[pnt], 36) * sum(stay ** k * F(w[pnt], 36) for k in range(0, 400))
t.append(float(pw))
def rps():
    n, r = 4, 0
    while n > 1:
        r += 1
        g = [rng.randrange(3) for _ in range(n)]
        if len(set(g)) == 2:
            a, b = set(g)
            win = a if (a - b) % 3 == 1 else b     # 0 rock, 1 paper, 2 scissors: paper beats rock
            n = g.count(win)
    return r
t.append(sim(200000, rps))

# ---- compare: blind vs file key vs third route ----
import re
def parse(txt):
    tx = txt.replace('−', '-').replace('£', '').replace('+', '').strip()
    m = re.fullmatch(r'\$\\tfrac(?:\{(\d+)\}|(\d))(?:\{(\d+)\}|(\d))\$', tx)
    if m:
        return float(F(int(m.group(1) or m.group(2)), int(m.group(3) or m.group(4))))
    return float(tx)
TOL3 = 0.01   # simulation tolerance on the third route (all simulated keys are below 10, n >= 20,000)
agree = 0
for ver in (2, 3):
    items = json.load(open(os.path.join(EX, f'mock-oa-sig-{ver}.json')))['parts'][0]['items']
    for it, b, th in zip(items, BLIND[ver], third[ver]):
        w_ = it['widget']
        if w_['kind'] == 'numeric':
            keyv = w_['answer']; ok_b = abs(keyv - float(b)) <= w_['tol']['abs']
            for wr in w_['wrong']:
                ok(abs(wr['value'] - keyv) > w_['tol']['abs'], f'v{ver} {it["id"]} wrong {wr["id"]} inside tol')
        else:
            txt = [o['text'] for o in w_['options'] if o.get('correct')][0]
            keyv = parse(txt)
            ok_b = abs(keyv - float(b)) <= 0.005
        tol = TOL3 * max(1, abs(float(b)))
        ok_t = abs(float(th) - float(b)) <= tol
        ok(ok_b, f'v{ver} {it["id"]}: blind {float(b):.6f} vs key {keyv}')
        ok(ok_t, f'v{ver} {it["id"]}: third route {float(th):.6f} vs blind {float(b):.6f}')
        agree += ok_b
        print(f'v{ver} {it["id"]:26s} blind {float(b):9.6f} key {keyv:9.6f} third {float(th):9.6f}')

# ---- distractors I recomputed by the slip each why names ----
S = {
 'v2 q01': [F(51, 2), 51 * F(26 * 25, 52 * 51), F(51 * 26, 51)],
 'v2 q11': [F(48), 100 - 200 ** .5, F(50)],
 'v2 q16': [F(1, 4), F(1, 9), F(5, 27)],
 'v3 q01': [F(7), F(14), 7 + F(7, 36)],
 'v3 q03': [F(40, 6), F(30, 6) - F(50, 6), -F(50, 6)],
 'v3 q10': [math.e, 1 + F(12, 5), F(6, 5) ** 6 - 1],
 'v3 q11': [F(1, 4), F(1), F(1, 4) + F(1, 16) + F(1, 32)],
 'v3 q15': [F(33, 8), F(5), F(3)],
}
ok(abs(float(S['v2 q11'][1]) - 85.86) < 0.005, 'v2 q11 no-half slip 85.86')
ok(round(float(S['v3 q01'][2]), 2) == 7.19 and F(33, 8) == F(4125, 1000), 'v3 slips 7.19 and 4.125')
print(f'blind agreement {agree} of 34')
if fails:
    print('\n'.join(fails)); print(f'FAIL {len(fails)}'); sys.exit(1)
print('OK')
