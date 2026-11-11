#!/usr/bin/env python3
"""Concept audit round 2, mm-games level 2 (l5 to l9, review-2, homework-2).
Recomputes every computable claim independently of the author scripts and runs every
code solution against its hidden tests. Exits 0 when the content is correct."""
import json, math, os, random, sys
from fractions import Fraction as F
from itertools import product

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
C = os.path.join(ROOT, 'app', 'content', 'courses', 'mm-games')
def load(name): return json.load(open(os.path.join(C, name + '.json')))
fails, count, notes = [], 0, []
def ok(cond, label):
    global count
    count += 1
    if not cond:
        fails.append(label); print('FAIL', label)
def close(a, b, tol=1e-9): return abs(float(a) - float(b)) <= tol
def _cmp(a, e, kind, tol):
    if kind == 'fraction': return isinstance(a, F) and a == e
    if kind == 'isclose':
        rt, at = ((tol.get('rel', 0) or 0, tol.get('abs', 0) or 0) if tol else (1e-9, 1e-12))
        def cl(x, y):
            if isinstance(x, (list, tuple)):
                return isinstance(y, (list, tuple)) and len(x) == len(y) and all(cl(p, q) for p, q in zip(x, y))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        return cl(a, e)
    fl = lambda x: [fl(i) for i in x] if isinstance(x, (list, tuple)) else x
    return fl(a) == fl(e)
def run_cases(src, w):
    out = []
    for c in w.get('examples', []) + w['tests']:
        g = {}
        try:
            exec(w.get('prelude', '') + '\n' + src, g)
            if c.get('setup'): exec(c['setup'], g)
            out.append(bool(_cmp(eval(c['call'], g), eval(str(c['expect']), g), c.get('compare', 'equal'), c.get('tol'))))
        except Exception:
            out.append(False)
    return out
def code(w, label):
    ok(all(run_cases(w['solution'], w)), label + ': solution passes every example and hidden test')
    ok(not all(run_cases(w['starter'], w)), label + ': starter fails')
    import re
    stated = re.search(r'Check runs (\d+) hidden tests', w.get('how', ''))
    ok(stated is None or int(stated.group(1)) == len(w['tests']), label + ': the stated number of hidden tests is right')
def ev(fn, n):
    rolls = list(product(range(1, 7), repeat=n)); return F(sum(fn(r) for r in rolls), len(rolls))
def informed_loss(bid, ask, outs):
    return F(sum(max(F(x) - F(ask), 0) + max(F(bid) - F(x), 0) for x in outs), len(outs))
def card_fair(shown, n, T=364, N=52):
    k = len(shown); s = sum(shown)
    return F(s) if k == n else s + (n - k) * F(T - s, N - k)
die = range(1, 7); two = [a + b for a in die for b in die]

l5, l6, l7, l8, l9 = load('l5-two-sided'), load('l6-edge'), load('l7-skewing'), load('l8-informed-flow'), load('l9-cards-revealed')
r2, h2 = load('review-2'), load('homework-2')
S5, S6, S7, S8, S9 = l5['screens'], l6['screens'], l7['screens'], l8['screens'], l9['screens']
A = lambda s: s['widget']['answer']

# ---------- l5 ----------
ok(A(S5[2]) == 11.5 and A(S5[3]) == 3 * (11.5 - 10.5), 'l5 s2 s3 a buyer pays the ask; P&L 3')
ok(ev(max, 2) == F(161, 36) and abs(5.5 - 161 / 36 - 1.03) < 0.005, 'l5 s4 s7 larger of two 4.47; a sale to you at 5.5 loses 1.03')
# coin game: heads before the first tail
exact = sum(k * 0.5 ** (k + 1) for k in range(200)); flips = sum((k + 1) * 0.5 ** (k + 1) for k in range(200))
rng = random.Random(55); N = 400000; tot = 0; zeros = 0
for _ in range(N):
    h = 0
    while rng.random() < 0.5: h += 1
    tot += h; zeros += h == 0
ok(close(exact, 1, 1e-9) and close(flips, 2, 1e-9) and abs(tot / N - 1) < 0.01 and abs(zeros / N - 0.5) < 0.005, 'l5 s5 coin game worth 1 (flips average 2; pays 0 half the time); MC %.4f' % (tot / N))
ok(ev(lambda r: r[0] * r[1], 2) == F(49, 4), 'l5 s6 product of two independent dice 12.25')
ok(A(S5[8]) == 14 + 1.5 and A(S5[9]) == '2qh', 'l5 s8 s9 ask and round-trip P&L')
code(S5[10]['widget'], 'l5 s10')
ok(close(A(S5[11]), 4.20 - 0.05) and 4.10 < 4.15 and 4.25 < 4.30, 'l5 s11 option bid; the new quote is best on both sides')
q = l5['quiz']
ok(A(q[1]) == (10.5 - 12) + (10 - 10.5) and A(q[2]) == (8 + 12) / 2, 'l5 quiz crossed quote -2; centre 10')

# ---------- l6 ----------
ok(A(S6[0]) == 3.5 - 3 and A(S6[2]) == 12 - 10.5 and close(A(S6[3]), 1 - 1.2) and close(A(S6[4]), 0.5 * 2 - 1.1) and A(S6[5]) == 4, 'l6 edges 0.5, 1.5, -0.2, -0.1, 4')
d3 = {}
for r in product(die, repeat=3): d3[sum(r)] = d3.get(sum(r), 0) + 1
above = sum(v for k, v in d3.items() if k > 12) / 216; below = sum(v for k, v in d3.items() if k < 12) / 216
ok(abs(above - 0.26) < 0.005 and below > 0.5, 'l6 s6 26%% of rolls above 12 (%.4f); most rolls below 12 (%.4f)' % (above, below))
ser = S6[7]['canvas']['params']['series'][0]['values']
steps = [b - a for a, b in zip(ser, ser[1:])]
ok(len(ser) == 101 and ser[0] == 0 and ser[-1] == 70 and all(-2 <= s <= 3 for s in steps), 'l6 s7 the path is 100 plays of -2..+3 ending at 70')
rng = random.Random(6); rep = [0]
for _ in range(100): rep.append(rep[-1] + rng.randint(1, 6) - 3)
notes.append('l6 s7 path %s random.Random(6).randint(1, 6) - 3' % ('reproduces with' if rep == ser else 'does NOT reproduce with'))
var1 = F(91, 6) - F(49, 4)
ok(close(A(S6[7]), var1, 1e-4) and abs(10 * math.sqrt(var1) - 17.08) < 0.005 and abs(100 * math.sqrt(var1) - 170.78) < 0.005 and abs((70 - 50) / 17.08 - 1) < 0.25, 'l6 s7 variance 35/12, sd 17.08 over 100 plays, 170.78 for one play at 100 times')
ok(A(S6[8]) == 0, 'l6 s8 zero edge at fair')
code(S6[10]['widget'], 'l6 s10')
ok(A(S6[11]) == 2000 * 100 * 0.5 / 100, 'l6 s11 desk expected P&L')
q = l6['quiz']
ok(close(A(q[0]), F(161, 36) - 4, 5e-5) and A(q[1]) == 2 * 1.5 and A(q[2]) == 1, 'l6 quiz keys')

# ---------- l7 ----------
def skew(V, g, q, h): return (V - g * q - h, V - g * q + h)
ok((A(S7[2])['bid'], A(S7[2])['ask']) == skew(10.5, 0.25, -2, 1), 'l7 s2 quote at q = -2')
rows = S7[3]['widget']['rows']; pos = 0; okrow = True
for row, tr in zip(rows[1:], [-1, -1, 1, -1]):
    bid, ask = skew(10.5, 0.25, pos, 1)
    price = float(row[0].split(' at ')[1]); okrow &= price == (ask if tr < 0 else bid)
    pos += tr; okrow &= row[1]['answer'] == pos and close(row[2]['answer'], skew(10.5, 0.25, pos, 1)[0])
ok(okrow, 'l7 s3 four trades: each trade price is the quote shown just before it; positions and bids')
pos = 0; pnl = 0
for tr in [1, 1, -1]:
    bid, ask = skew(10.5, 0.25, pos, 1); pnl += (10.5 - bid) if tr > 0 else (ask - 10.5); pos += tr
ok(A(S7[4]) == pnl == 2.75, 'l7 s4 P&L 2.75 with skewed prices 9.5, 9.25, 11')
ok(skew(10.5, 0.25, -3, 1) == (10.25, 12.25) and A(S7[7]) == skew(10.5, 0.25, -1, 1)[1] and A(S7[8]) == skew(10.5, 0.25, 4, 1)[0], 'l7 s5 s7 s8 skewed quotes')
ok(all(close(11.5 - 0.25 * qq, skew(10.5, 0.25, qq, 1)[1]) for qq in range(-6, 7)), 'l7 s9 ask = 11.5 - 0.25q')
code(S7[10]['widget'], 'l7 s10')
ok(close(A(S7[11]), 2.45 + 0.005 * 20 + 0.05), 'l7 s11 call quote after selling 2,000')
q = l7['quiz']
ok(A(q[0]) == skew(10.5, 0.25, 3, 1)[1] and A(q[2]) == 2 * 1.5 + 0.5, 'l7 quiz keys')

# ---------- l8 ----------
ok(close(A(S8[0]), -informed_loss(2.5, 4.5, die), 1e-4), 'l8 s0 informed loss 2/3 at 2.5 at 4.5')
rng = random.Random(8); N = 300000; tot = 0.0
for _ in range(N):
    x = rng.randint(1, 6)
    if x > 4.5: tot -= x - 4.5        # they buy at the ask only when the die is above it
    elif x < 2.5: tot -= 2.5 - x      # they sell at the bid only when the die is below it
ok(abs(tot / N + 2 / 3) < 0.01, 'l8 s0 Monte Carlo of the informed game (%.4f)' % (tot / N))
t = S8[2]['widget']['rows']
ok(close(t[0][1]['answer'], informed_loss(1.5, 5.5, die), 1e-4) and close(t[2][1]['answer'], informed_loss(3, 4, die), 1e-4) and informed_loss(0.5, 6.5, die) == 0 and informed_loss(3.5, 3.5, die) == F(3, 2), 'l8 s1 s2 losses 1/6, 1, 0 and 3/2')
mixed = lambda b, a, al: (1 - al) * (F(a) - F(b)) / 2 - al * informed_loss(b, a, die)
ok(close(A(S8[3]), mixed(1.5, 5.5, F(1, 2)), 1e-4) and mixed(1.5, 5.5, F(1, 2)) == F(11, 12), 'l8 s3 half informed: 11/12')
rng = random.Random(83); tot = 0.0
for _ in range(N):
    x = rng.randint(1, 6)
    if rng.random() < 0.5:
        tot -= max(x - 5.5, 0) + max(1.5 - x, 0)
    else:
        tot += (5.5 - x) if rng.random() < 0.5 else (x - 1.5)   # random buyer or seller, settled at the die
ok(abs(tot / N - 11 / 12) < 0.02, 'l8 s3 Monte Carlo of the mixed game, random flow settled at the die (%.4f)' % (tot / N))
t = S8[4]['widget']['rows']
ok(close(t[1][2]['answer'], mixed(2, 5, F(1, 2)), 1e-4) and close(t[2][2]['answer'], mixed(2.5, 4.5, F(1, 2)), 1e-4) and informed_loss(2, 5, die) == F(1, 3), 'l8 s4 table 7/12 and 1/6')
ok(informed_loss(3, 4, die) == 3 * informed_loss(2, 5, die), 'l8 s5 3 at 4 loses three times 2 at 5')
dice4 = [int(r[0]) for r in S8[6]['canvas']['params']['rows']]
ok(A(S8[6]) == -sum(max(x - 5, 0) + max(2 - x, 0) for x in dice4) and close(4 * informed_loss(2, 5, die), F(4, 3)), 'l8 s6 four games -2; expected 4/3')
rng = random.Random(4); notes.append('l8 s6 dice %s random.Random(4).randint(1, 6) x 4' % ('reproduce with' if [rng.randint(1, 6) for _ in range(4)] == dice4 else 'do NOT reproduce with'))
# zero-profit half-spread s = alpha * delta (Glosten-Milgrom toy): exact and Monte Carlo
gm = lambda s, al, de: (1 - al) * s - al * (de - s)
ok(close(gm(6, 0.2, 30), 0) and gm(5, 0.2, 30) < 0 < gm(7, 0.2, 30) and A(S8[7]) == 6 and close(gm(2, 0.2, 10), 0), 'l8 s7 s = alpha delta breaks even: 2p and 6p')
rng = random.Random(87); tot = 0.0; s = 6; de = 30
for _ in range(N):
    up = rng.random() < 0.5
    if rng.random() < 0.2: tot += s - de                      # informed: buys before a rise, sells before a fall
    else: tot += s + (de if (rng.random() < 0.5) != up else -de)  # uninformed: random side, then the move
ok(abs(tot / N) < 0.25, 'l8 s7 Monte Carlo: quoting +/-6p with alpha 0.2 and delta 30p earns about 0 (%.3f)' % (tot / N))
code(S8[9]['widget'], 'l8 s9')
ok(A(S8[10]) == 500 + 0.2 * 30, 'l8 s10 ask 506p')
q = l8['quiz']
ok(close(A(q[1]), informed_loss(2.5, 5.5, die), 1e-4) and A(q[2]) == 0.4 * 10 and close(A(q[3]), informed_loss(5, 9, two), 5e-5) and sum(1 for x in two if x < 5 or x > 9) == 12, 'l8 quiz keys')

# ---------- l9 ----------
ok(A(S9[0]) == card_fair([], 3) == 21 and close(A(S9[2]), card_fair([13], 3), 5e-5) and card_fair([13], 3) == F(455, 17), 'l9 fair 21, then 455/17 after a king')
ok(close(A(S9[3]), 23 - card_fair([13], 3), 5e-4) and close(A(S9[5]), card_fair([13, 2], 3), 1e-9) and close(23 - card_fair([13, 2], 3), 1.02) and abs(card_fair([13], 3) - card_fair([13, 2], 3) - 4.78) < 0.01, 'l9 s3 s5 ledger -3.76, fair 21.98, +1.02, drop 4.78')
ok(A(S9[6]) == 13 + 7 + 7 and close(card_fair([13, 13], 3), 32.76), 'l9 s6 s7 fresh decks 27; two kings 32.76')
ok(all(card_fair([c], 3) - 21 == F(49 * (c - 7), 51) for c in range(1, 14)), 'l9 s8 change = 49(c - 7)/51 for every card')
ok(close(A(S9[9]), card_fair([1], 3), 5e-5), 'l9 s9 ace: 259/17')
# Monte Carlo: sum of three cards from one deck given the first is a king, against 26.76 (shared deck) and 27 (fresh decks)
deck = [v for v in range(1, 14) for _ in range(4)]; rest = list(deck); rest.remove(13)
rng = random.Random(9); N = 400000; tot = 0
for _ in range(N):
    a, b = rng.sample(rest, 2); tot += 13 + a + b
mc = tot / N
ok(abs(mc - 455 / 17) < 0.04 and abs(mc - 27) > 0.15, 'l9 Monte Carlo without replacement: %.4f, near 26.76 and away from 27' % mc)
# and the update rule for a general draw: average of (sum | first card) over a real shuffled deal
rng = random.Random(91); acc = {}
for _ in range(400000):
    a, b, c = rng.sample(deck, 3); s0, n0 = acc.get(a, (0, 0)); acc[a] = (s0 + a + b + c, n0 + 1)
ok(all(abs(s0 / n0 - float(card_fair([c], 3))) < 0.15 for c, (s0, n0) in acc.items()), 'l9 Monte Carlo: conditional mean given the first card matches F for all 13 values')
code(S9[10]['widget'], 'l9 s10')
ok(close(A(S9[11]), 2.6 + 1.8 + 3 * 2), 'l9 s11 future 10.40')
q = l9['quiz']
ok(close(A(q[1]), card_fair([12], 4), 5e-5) and A(q[2]) == 15 and abs(A(q[3]) - (float(card_fair([1], 3)) - 20)) < 0.006 and 13 + 2 + 6 == 21, 'l9 quiz keys')

# ---------- review-2 ----------
it = r2['items']
ok(A(it[0]) == 14 - 1 and close(A(it[1]), ev(min, 2) - F(5, 2), 5e-5) and A(it[2]) == skew(10.5, 0.5, 2, 1)[1], 'review-2 items 0 to 2')
ok(close(A(it[3]), informed_loss(2, 4, die), 5e-5) and close(A(it[4]), card_fair([12, 5], 3), 1e-3) and A(it[5]) == 2 * (8 - 7) + (7 - 6.5) and skew(7, 0.25, -2, 1) == (6.5, 8.5), 'review-2 items 3 to 5')
ok(A(it[7]) == 400 + 0.25 * 12 and sum(1 for x in two if x > 9) == 6 and close(A(it[9]), 20 - card_fair([13], 2), 5e-5), 'review-2 items 7 to 9')

# ---------- homework-2 ----------
it = h2['items']
code(it[0]['widget'], 'homework-2 play')
seeded = sum('make_script' in t['call'] for t in it[0]['widget']['tests'])
ok({3: 'three', 4: 'four'}.get(seeded, '?') + ' seeded games' in it[0]['prose'], 'homework-2 play: the prose says "three seeded games" but %d hidden tests use make_script' % seeded)
code(it[1]['widget'], 'homework-2 zero_profit_half_spread')
# independent check of the break-even half-width by bisection on the die
def breakeven(al, outs):
    m = F(sum(outs), len(outs)); lo, hi = 0.0, 10.0
    g = lambda h: (1 - al) * h - al * sum(max(abs(x - m) - h, 0) for x in outs) / len(outs)
    for _ in range(80):
        mid = (lo + hi) / 2
        if g(mid) >= 0: hi = mid
        else: lo = mid
    return hi
ok(abs(breakeven(0.5, list(die)) - 0.8) < 1e-9 and abs(breakeven(0.2, list(die)) - 0.3) < 1e-9 and abs(breakeven(1 / 3, [0, 10]) - 5 / 3) < 1e-9, 'homework-2 break-even h: 4/5, 3/10, and alpha delta = 5/3 for a two-point move')
m = it[3]['model']
f1 = card_fair([3], 3); f2 = card_fair([3, 11], 3)
led = [2 * (21 - 19), 2 * (float(f1) - 19), -20 + float(f1), -20 + float(f2), -20 + 23]
ok(abs(led[1] + 3.69) < 0.005 and abs(led[2] + 2.84) < 0.005 and led[3] == 1 and led[4] == 3 and all(s in m for s in ['+£4', '−£3.69', '−£2.84', '+£1', '+£3', '14 at 18', '14.5 at 18.5', '18.5 at 22.5']), 'homework-2 mock model ledger and quotes')
ok(close(A(it[4]), f1, 5e-5) and A(it[5]) == f2 == 21 and A(it[6]) == 3, 'homework-2 mock fair values and P&L')
slip = [w['value'] for w in it[5]['widget']['wrong'] if w['id'] == 'first'][0]
ok(abs(slip - float(14 + F(364 - 3, 51))) < 0.001, 'homework-2 h-mock-fair-2 slip "first": the remaining mean after one card (the 3) is 361/51, giving 21.0784; the content has %.4f (14 + 351/51, the mean after a king)' % slip)
ok(close(A(it[7]), F(1, 2) * 2 - F(1, 2) * informed_loss(5, 9, two), 5e-5) and close(A(it[8]), F(7, 6) - 1, 5e-5), 'homework-2 two-dice mixed 13/18; edge game 1/6')

for nline in notes: print('NOTE', nline)
print('mm-games L2 concepts r2: %d checks, %d failed' % (count, len(fails)))
sys.exit(1 if fails else 0)
