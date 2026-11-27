"""Stage 0 brief numbers (ai-basics, ai-use), each computed twice: method A and an independent method B."""
from fractions import Fraction as F
import math, itertools

def check(label, a, b, tol=1e-9):
    ok = (a == b) if not isinstance(a, float) else abs(a - b) <= tol * max(1, abs(a))
    print(('OK  ' if ok else 'FAIL'), label, a, '|', b)
    assert ok

# ---------- ai-basics L1: threshold rule on links ----------
links = [0, 1, 1, 2, 3, 4, 5, 6, 7, 9]
spam = [0, 0, 0, 1, 0, 0, 1, 1, 1, 1]
def acc(t, xs, ys): return sum((x >= t) == bool(y) for x, y in zip(xs, ys))
scores = {t: acc(t, links, spam) for t in range(0, 11)}
print('L1 train correct by threshold', scores)
best = max(scores.values()); bests = [t for t, s in scores.items() if s == best]
# method B: count errors explicitly
errs = {t: sum(1 for x, y in zip(links, spam) if (1 if x >= t else 0) != y) for t in range(0, 11)}
check('L1 best threshold unique', bests, [t for t, e in errs.items() if e == min(errs.values())])
check('L1 best correct', best, 10 - min(errs.values()))
tl = [0, 2, 4, 5, 8, 10]; ts = [0, 0, 1, 1, 1, 1]
check('L1 test correct at t=5', acc(5, tl, ts), sum(1 for x, y in zip(tl, ts) if int(x >= 5) == y))
seen = dict(zip(links, spam))
print('L1 memoriser answers on test:', [seen.get(x, None) for x in tl])

# ---------- ai-basics L2: nudging a line ----------
xs = [1, 2, 3, 4, 5]; ys = [3, 4, 6, 7, 9]
def mse(w, b): return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
def mse_frac(w, b): return sum((F(w) * x + F(b) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
check('L2 mse(2,1) float vs fraction', mse(2, 1), float(mse_frac(2, 1)))
check('L2 mse(0,0)', mse(0, 0), float(mse_frac(0, 0)))
check('L2 mse(1.5,1.5)', mse(1.5, 1.5), float(mse_frac(F(3, 2), F(3, 2))))
# least squares (for the brief only; not taught)
n = len(xs); mx = F(sum(xs), n); my = F(sum(ys), n)
wls = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); bls = my - wls * mx
print('L2 least squares w, b, mse:', wls, bls, float(mse_frac(wls, bls)))

def fit_by_nudging(step=0.1, w=0.0, b=0.0, max_rounds=1000):
    cur = mse(w, b); rounds = 0
    while rounds < max_rounds:
        moved = False
        for which in ('w', 'b'):
            best = (cur, w, b)
            for d in (step, -step):
                nw, nb = (w + d, b) if which == 'w' else (w, b + d)
                e = mse(nw, nb)
                if e < best[0]: best = (e, nw, nb)
            if best[0] < cur: cur, w, b = best; moved = True
        rounds += 1
        if not moved: break
    return w, b, cur, rounds

w, b, e, r = fit_by_nudging()
print('L2 nudging result (step 0.1)', round(w, 6), round(b, 6), round(e, 6), 'rounds', r)
# method B: integer grid in tenths with exact fractions, same rule
def fit_grid(step=F(1, 10)):
    w = F(0); b = F(0); cur = mse_frac(w, b); rounds = 0
    while True:
        moved = False
        for which in ('w', 'b'):
            best = (cur, w, b)
            for d in (step, -step):
                nw, nb = (w + d, b) if which == 'w' else (w, b + d)
                e2 = mse_frac(nw, nb)
                if e2 < best[0]: best = (e2, nw, nb)
            if best[0] < cur: cur, w, b = best; moved = True
        rounds += 1
        if not moved: return w, b, cur, rounds
wg, bg, eg, rg = fit_grid()
check('L2 nudging w', round(w, 6), float(wg)); check('L2 nudging b', round(b, 6), float(bg))
check('L2 nudging mse', round(e, 6), round(float(eg), 6)); check('L2 rounds', r, rg)
# best on the tenths grid by brute force
gb = min(((float(mse_frac(F(i, 10), F(j, 10))), i / 10, j / 10) for i in range(0, 41) for j in range(-20, 41)))
print('L2 best on the 0.1 grid (brute force):', gb)
# first round in detail
print('L2 first nudges from (0,0): mse(0.1,0)=', mse(0.1, 0), 'mse(-0.1,0)=', mse(-0.1, 0), 'then b: mse(0.1,0.1)=', mse(0.1, 0.1))
check('L2 mse(0.1,0)', mse(0.1, 0), float(mse_frac(F(1, 10), 0)))
w2, b2, e2, r2 = fit_by_nudging(step=0.5)
print('L2 nudging step 0.5:', w2, b2, round(e2, 6), r2)
w3, b3, e3, r3 = fit_by_nudging(step=0.01, max_rounds=100000)
print('L2 nudging step 0.01:', round(w3, 6), round(b3, 6), round(e3, 6), r3)

wg3, bg3, eg3, rg3 = fit_grid(F(1, 100))
check('L2 step 0.01 w', round(w3, 6), float(wg3)); check('L2 step 0.01 b', round(b3, 6), float(bg3))
check('L2 step 0.01 mse', round(e3, 6), round(float(eg3), 6)); check('L2 step 0.01 rounds', r3, rg3)
print('L2 at (1.48,1.36): w+-0.01', mse(1.49, 1.36), mse(1.47, 1.36), 'b+-0.01', mse(1.48, 1.37), mse(1.48, 1.35), 'diagonal', mse(1.47, 1.37))

# ---------- ai-basics L3: neurons ----------
def fire(ws, bias, xs_): return 1 if sum(a * c for a, c in zip(ws, xs_)) + bias > 0 else 0
# umbrella neuron: cloudy, rain forecast, carrying a bag ; weights 2, 3, -1, bias -2.5
um = (2, 3, -1); ub = -2.5
for x in itertools.product((0, 1), repeat=3):
    s = sum(a * c for a, c in zip(um, x)) + ub
    print('L3 umbrella', x, 'sum', s, 'fires', fire(um, ub, x))
AND = ((2, 2), -3); OR = ((2, 2), -1); NAND = ((-2, -2), 3)
for x in itertools.product((0, 1), repeat=2):
    a, o, na = fire(*AND, x) if False else fire(AND[0], AND[1], x), fire(OR[0], OR[1], x), fire(NAND[0], NAND[1], x)
    xor = fire((2, 2), -3, (o, na))
    check(f'L3 AND{x}', a, int(x[0] and x[1])); check(f'L3 OR{x}', o, int(x[0] or x[1]))
    check(f'L3 XOR{x}', xor, x[0] ^ x[1])
# brute force: no single neuron with weights and bias in a grid computes XOR
grid = [k / 2 for k in range(-10, 11)]
found = [(w1, w2, bb) for w1 in grid for w2 in grid for bb in grid
         if all(fire((w1, w2), bb, x) == (x[0] ^ x[1]) for x in itertools.product((0, 1), repeat=2))]
check('L3 no single neuron on grid computes XOR', len(found), 0)
print('L3 params of the 2-2-1 XOR net:', 2 * 2 + 2 + 2 + 1)

# ---------- ai-basics L4: next-word table ----------
text = "the cat sat on the mat . the cat ate the jam . the dog sat on the cat ."
words = text.split()
pairs = list(zip(words, words[1:]))
from collections import Counter, defaultdict
after = defaultdict(Counter)
for a, c in pairs: after[a][c] += 1
print('L4 words', len(words), 'pairs', len(pairs), 'distinct words', len(set(words)))
print('L4 after "the":', dict(after['the']), 'after "sat":', dict(after['sat']), 'after "cat":', dict(after['cat']))
# method B: count by scanning the string with find
def count_after(w):
    out = Counter()
    for i in range(len(words) - 1):
        if words[i] == w: out[words[i + 1]] += 1
    return out
check('L4 table "the"', dict(after['the']), dict(count_after('the')))
row = after['the']; tot = sum(row.values())
probs = {k: F(v, tot) for k, v in row.items()}
print('L4 P(next | the):', {k: str(v) for k, v in probs.items()})
def temp(ps, power):
    q = {k: float(v) ** power for k, v in ps.items()}; s = sum(q.values()); return {k: round(v / s, 4) for k, v in q.items()}
print('L4 T=0.5 (square):', temp(probs, 2)); print('L4 T=2 (square root):', temp(probs, 0.5))
# method B for temperature via exact fractions for squares
sq = {k: v ** 2 for k, v in probs.items()}; s = sum(sq.values())
print('L4 T=0.5 exact:', {k: str(v / s) for k, v in sq.items()})
order = ['cat', 'mat', 'jam', 'dog']
cum = list(itertools.accumulate([float(probs[k]) for k in order]))
print('L4 cumulative in order', order, cum)
def pick(order, ps, u):
    c = 0
    for k in order:
        c += ps[k]
        if u < c: return k
    return order[-1]
for u in (0.1, 0.5, 0.62, 0.9):
    a = pick(order, {k: float(v) for k, v in probs.items()}, u)
    bidx = next(i for i, c in enumerate(cum) if u < c)
    check(f'L4 pick u={u}', a, order[bidx])
print('L4 characters in text (with spaces):', len(text), 'letters only:', sum(ch.isalpha() for ch in text))

# ---------- ai-use L1: a fluent sentence that the text never says ----------
sent = 'the dog sat on the mat .'.split()
pA = F(1)
for a, c in zip(sent, sent[1:]): pA *= F(after[a][c], sum(after[a].values()))
pB = F(count_after('the')['dog'], 6) * F(count_after('the')['mat'], 6)
check('ai-use P(the dog sat on the mat . | the)', pA, pB)
check('ai-use sentence not in the text', ' '.join(sent) in text, False)
print('ai-use P =', pA, float(pA))
# ---------- ai-use L2: checking a sum ----------
P = 2400; r = 0.03; nyr = 5
comp = P * (1 + r) ** nyr; comp_b = float(F(2400) * F(103, 100) ** 5)
check('ai-use compound', round(comp, 2), round(comp_b, 2))
print('ai-use simple interest (the slip):', P * (1 + r * nyr))
print('ai-use estimate 3% x 5 ~ 15% plus a little:', P * 1.15, P * 1.16)
# a percentage check: 18% of £340
check('ai-use 18% of 340', round(0.18 * 340, 2), float(F(18, 100) * 340))

# ai-use L2 l8: a monthly rate turned into an annual one
check('ai-use 1% a month compounded for a year', round(1.01 ** 12 - 1, 6), round(float(F(101, 100) ** 12 - 1), 6))
print('ai-use 12 x 1% =', 12 * 0.01, 'against compounding', round(1.01 ** 12 - 1, 4))
