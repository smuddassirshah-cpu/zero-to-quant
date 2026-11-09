"""micro L3 performance task h-derive-tilted-quotes: every stated number, computed twice.

Run from the repository root (standard library only):
    python3 -I docs/reports/micro-3-perf-numbers.py
Route A: the closed forms a = alpha delta / (alpha + 2(1 - alpha) beta) and b = alpha delta / (alpha + 2(1 - alpha)(1 - beta)).
Route B: enumerate every path of the one-trader tree (value, type, side) with exact fractions and condition by counting.
Route C (a third look): a seeded simulation of 400,000 arrivals.
Also: the reduction at beta = 1/2 on a grid, the symmetric-quote profits, the rubric tick sets.
"""
import itertools
import json
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("micro", 3)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'micro', 'homework-3.json')
doc = json.load(open(HW, encoding='utf-8'))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-derive-tilted-quotes']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
PR, MO = f"items[{I}].prompt", f"items[{I}].model"


def closed(al, be, de):
    return al * de / (al + 2 * (1 - al) * be), al * de / (al + 2 * (1 - al) * (1 - be))


def tree(al, be, de):
    """Every path (D, type, side) with its exact chance; returns E[D | buy], E[D | sell], P(buy), P(inf | buy), P(inf | sell)."""
    paths = []
    for d in (de, -de):
        paths.append((d, 'inf', 'buy' if d > 0 else 'sell', F(1, 2) * al))
        paths.append((d, 'un', 'buy', F(1, 2) * (1 - al) * be))
        paths.append((d, 'un', 'sell', F(1, 2) * (1 - al) * (1 - be)))
    pb = sum(p for _, _, s, p in paths if s == 'buy')
    ps = sum(p for _, _, s, p in paths if s == 'sell')
    edb = sum(d * p for d, _, s, p in paths if s == 'buy') / pb
    eds = sum(d * p for d, _, s, p in paths if s == 'sell') / ps
    pib = sum(p for _, t, s, p in paths if s == 'buy' and t == 'inf') / pb
    pis = sum(p for _, t, s, p in paths if s == 'sell' and t == 'inf') / ps
    lv.claim(sum(p for *_, p in paths) == 1, f"tree chances add to 1 at alpha={al}, beta={be}")
    return edb, eds, pb, pib, pis


al, be, de = F(1, 5), F(3, 4), F(21)
aA, bA = closed(al, be, de)
edb, eds, pb, pib, pis = tree(al, be, de)
aB, bB = edb, -eds
lv.claim(aA == aB == 3, "a = 3p by the closed form and by the tree")
lv.claim(bA == bB == 7, "b = 7p by the closed form and by the tree")
lv.claim(al * de == F(21, 5), "alpha delta = 4.2p")
lv.claim(al + 2 * (1 - al) * be == F(7, 5) and al + 2 * (1 - al) * (1 - be) == F(3, 5), "denominators 1.4 and 0.6")
lv.claim(pb == F(7, 10) and F(1, 10) + F(4, 5) * be == pb, "P(buy) = 0.1 + 0.8 x 0.75 = 0.7, two ways")
lv.claim(pib == F(1, 7) and pis == F(1, 3), "P(informed | buy) = 1/7, P(informed | sell) = 1/3")
lv.claim(de * pib == aA and de * pis == bA, "each quote is delta times P(informed | that side): 21/7 = 3, 21/3 = 7")
lv.claim(aA + bA == 10 and (aA - bA) / 2 == -2, "a 10p spread centred 2p below V")
lv.claim(bA > aA, "the bid sits further from V")

# the weighting route of the model: p(a - delta) + (1 - p) a = 0 gives a = delta p
lv.claim(pib * (aA - de) + (1 - pib) * aA == 0 and pis * (bA - de) + (1 - pis) * bA == 0, "weighting route gives zero profit at a and b")

# general alpha, beta: closed form equals the tree, and beta = 1/2 reduces to alpha delta
grid = [F(j, 20) for j in range(1, 20)]
ok_gen = ok_half = True
for a_ in grid:
    for b_ in grid:
        ca, cb = closed(a_, b_, de)
        ta, ts, *_ = tree(a_, b_, de)
        ok_gen &= (ca == ta and cb == -ts)
    ca, cb = closed(a_, F(1, 2), de)
    ok_half &= (ca == cb == a_ * de)
lv.claim(ok_gen, "closed forms equal the tree on a 19 x 19 grid of alpha and beta")
lv.claim(ok_half, "at beta = 1/2 both quotes equal alpha delta on every alpha in the grid")
lv.claim(all(2 * (1 - a_) * F(1, 2) == 1 - a_ for a_ in grid), "2(1 - alpha)(1/2) = 1 - alpha")
lv.claim(closed(F(1, 5), F(1, 2), F(10))[0] == 2, "untilted lesson case alpha 0.2, delta 10 gives 2p (sanity)")

# (d) symmetric quotes V +- 4.2
s = al * de
buy_p, sell_p = s - aA, s - bA
lv.claim(buy_p == F(6, 5) and sell_p == F(-14, 5), "symmetric quotes: +1.2p on a buy, -2.8p on a sell")
lv.claim(pb * buy_p + (1 - pb) * sell_p == 0 and pb * buy_p == F(84, 100), "0.7 x 1.2 - 0.3 x 2.8 = 0.84 - 0.84 = 0")
# second route for (d): sum profit path by path over the tree
tot = F(0)
for d in (de, -de):
    for t, side, p in (('inf', 'buy' if d > 0 else 'sell', F(1, 2) * al), ('un', 'buy', F(1, 2) * (1 - al) * be), ('un', 'sell', F(1, 2) * (1 - al) * (1 - be))):
        tot += p * ((s - d) if side == 'buy' else (d + s))
lv.claim(tot == 0, "symmetric quotes break even over all trades, path by path")
lv.claim(3 < s, "a rival ask between V + 3 and V + 4.2 exists")

# route C: seeded simulation
rng = random.Random(20261109)
n = 400_000
sb = nb = ss = ns = 0.0
for _ in range(n):
    d = 21 if rng.random() < 0.5 else -21
    if rng.random() < 0.2:
        buy = d > 0
    else:
        buy = rng.random() < 0.75
    if buy:
        sb += d; nb += 1
    else:
        ss += d; ns += 1
lv.claim(abs(sb / nb - 3) < 0.1 and abs(-ss / ns - 7) < 0.15, f"simulation: E[D|buy] = {sb / nb:.3f}, -E[D|sell] = {-ss / ns:.3f}")
lv.claim(abs(nb / n - 0.7) < 0.005, f"simulation: share of buys {nb / n:.4f}")

# the numbers as printed in prompt and model
for v in (0.2, 21, 0.75):
    lv.expect("homework", PR, v)
for v in (4.2, 1.4, 3, 0.6, 7, 10, 2, 0.1, 0.3, 0.7, 1.2, -2.8, 0.84, 0.8, 0.25):
    lv.expect("homework", MO, v)
lv.expect("homework", MO, "21 / 7 = 3")
lv.expect("homework", MO, "21 / 3 = 7")
lv.expect("homework", f"items[{I}].rubric[3].text", 3)
lv.expect("homework", f"items[{I}].rubric[3].text", 7)
lv.expect("homework", f"items[{I}].rubric[4].text", 1.2)
lv.expect("homework", f"items[{I}].rubric[4].text", 2.8)

# rubric: 3 to 5 rows summing to 10, every passing tick set covers (a) ask, (a) bid, (b) and (c)
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [r.get('required', False) for r in rub]
parts = ['a-ask', 'a-bid', 'b', 'c', 'd']
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False] and not all(req), "rows 1 to 4 required, row 5 optional")
lv.stated("homework", PR, "Optional, one more point: (d)", not req[4])
passes = [c for r in range(1, len(rub) + 1) for c in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in c) >= 7 and all(i in c for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in c) for c in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a-ask', 'a-bid', 'b', 'c'} <= {parts[i] for i in c} for c in passes), "no pass skips a named part")

# homework limits after the change
lv.claim(6 <= len(items) <= 12 and len(items) == 9, "homework has 9 items (6 to 12)")
lv.claim(any(x.get('difficulty') == 5 for x in items), "a difficulty 5 item is present")
lv.claim(sum(1 for x in items if x.get('kind') == 'longform') == 2, "two longform items")
lv.claim(sum(1 for x in items if x.get('performance')) == 1 and it['performance'] == 'derivation', "one performance task, a derivation")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "no scaffold fields")

lv.check_wrongs()
lv.report()
