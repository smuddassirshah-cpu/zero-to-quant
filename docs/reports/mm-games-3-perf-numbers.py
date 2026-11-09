"""Recompute every number in the mm-games level 3 performance task (homework-3 item h-coin-dice-aloud).
Route 1: closed forms (case averages, variance plus mean squared). Route 2: exact enumeration of all
2 x 6^4 coin-and-dice outcomes with Fractions, conditioning by filtering; sds also by a seeded simulation.
The ledger is replayed by cash and position, and separately rebuilt as edge plus inventory moves.
The rubric's tick sets are listed. Exits 0 when every pair agrees and matches what the item states.
Run: python3 docs/reports/mm-games-3-perf-numbers.py
"""
import json, os, random, sys, itertools, math
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'mm-games', 'homework-3.json')
fails = []

def check(name, a, b, stated=None, tol=1e-9, tol_stated=1e-9):
    a, b = float(a), float(b)
    ok = abs(a - b) <= tol and (stated is None or abs(a - stated) <= tol_stated)
    print(f"{'ok  ' if ok else 'FAIL'} {name}: route 1 {a:.6f}, route 2 {b:.6f}, stated {stated}")
    if not ok:
        fails.append(name)

def truth(name, cond):
    print(f"{'ok  ' if cond else 'FAIL'} {name}")
    if not cond:
        fails.append(name)

# ---------- Route 2 universe: coin (H/T) and four dice; heads uses the first two dice only ----------
OUT = []  # (prob, coin, dice tuple, total)
for coin in 'HT':
    for dice in itertools.product(range(1, 7), repeat=4):
        n = 2 if coin == 'H' else 4
        OUT.append((F(1, 2) * F(1, 6 ** 4), coin, dice, sum(dice[:n])))

def cond(pred):
    rows = [o for o in OUT if pred(o)]
    p = sum(o[0] for o in rows)
    mean = sum(o[0] * o[3] for o in rows) / p
    var = sum(o[0] * (o[3] - mean) ** 2 for o in rows) / p
    return mean, var

ALL = lambda o: True
SIX = lambda o: o[2][0] == 6
SIXH = lambda o: o[2][0] == 6 and o[1] == 'H'

# ---------- Fair values ----------
one_mean, one_var = F(7, 2), F(35, 12)
f0 = F(1, 2) * 2 * one_mean + F(1, 2) * 4 * one_mean          # half of 7 plus half of 14
check('two dice average 7', 2 * one_mean, cond(lambda o: o[1] == 'H')[0], 7)
check('four dice average 14', 4 * one_mean, cond(lambda o: o[1] == 'T')[0], 14)
check('opening fair 10.5', f0, cond(ALL)[0], 10.5)
f1 = 6 + F(1, 2) * one_mean + F(1, 2) * 3 * one_mean            # 6 + half of 3.5 + half of 10.5
check('three dice to come worth 10.5', 3 * one_mean, cond(lambda o: o[2][0] == 6 and o[1] == 'T')[0] - 6, 10.5)
check('fair after the 6 is 13', f1, cond(SIX)[0], 13)
f2 = 6 + one_mean
check('fair after heads is 9.5', f2, cond(SIXH)[0], 9.5)
check('the 6 replaces a die worth 3.5', one_mean, sum(o[0] * o[2][0] for o in OUT), 3.5)
check('coin swing of the rest after the 6, 3.5 either way',
      (cond(lambda o: o[2][0] == 6 and o[1] == 'T')[0] - cond(SIXH)[0]) / 2, F(7, 2), 3.5)
check('coin swing of the total at the open, 3.5 either way',
      (cond(lambda o: o[1] == 'T')[0] - cond(lambda o: o[1] == 'H')[0]) / 2, f0 - 7, 3.5)

# ---------- Distribution claims behind the opening reason (exact enumeration of the mixed total) ----------
def law(k):
    d = {}
    for r in itertools.product(range(1, 7), repeat=k):
        d[sum(r)] = d.get(sum(r), 0) + F(1, 6 ** k)
    return d
_two, _four = law(2), law(4)
mix = lambda t: (_two.get(t, 0) + _four.get(t, 0)) / 2
check('P(total = 10) = 0.0725, from the exact law', mix(10), sum(o[0] for o in OUT if o[3] == 10), 0.0725, tol_stated=5e-5)
check('P(total = 14) = 0.0563', mix(14), sum(o[0] for o in OUT if o[3] == 14), 0.0563, tol_stated=5e-5)
truth('the total is not rare near 10.5: P(10) is above P(14) and P(9 to 12) is above P(13 to 15)',
      mix(10) > mix(14) and sum(mix(t) for t in range(9, 13)) > sum(mix(t) for t in range(13, 16)))
_sd2, _sd4 = math.sqrt(2 * 35 / 12), math.sqrt(4 * 35 / 12)
truth('the coin swing 3.5 exceeds the sd of two dice (2.42) and of four dice (3.42)', 3.5 > _sd2 and 3.5 > _sd4)
_within = (2 * one_var + 4 * one_var) / 2
check('variance 21 = mean within-case variance 8.75 + coin swing squared 12.25', _within + F(7, 2) ** 2,
      cond(ALL)[1], 21)
check('the coin swing squared is 12.25', F(7, 2) ** 2, (cond(lambda o: o[1] == 'T')[0] - cond(lambda o: o[1] == 'H')[0]) ** 2 / 4, 12.25)

# ---------- Variances and sds (model "Why these widths") ----------
ex2_h = 2 * one_var + 49            # 35/6 + 49
ex2_t = 4 * one_var + 196           # 35/3 + 196
check('two dice variance 35/6', 2 * one_var, cond(lambda o: o[1] == 'H')[1], 35 / 6)
check('four dice variance 35/3', 4 * one_var, cond(lambda o: o[1] == 'T')[1], 35 / 3)
avg_ex2 = (ex2_h + ex2_t) / 2
check('average E[X^2] 131.25', avg_ex2, sum(o[0] * o[3] ** 2 for o in OUT), 131.25)
var0 = avg_ex2 - f0 ** 2
check('opening variance 21', var0, cond(ALL)[1], 21)
rest_ex2 = ((one_var + one_mean ** 2) + (3 * one_var + (3 * one_mean) ** 2)) / 2
check('after the 6, E[rest^2] 67.08', rest_ex2, cond(SIX)[1] + (cond(SIX)[0] - 6) ** 2, 67.08, tol_stated=0.005)
var1 = rest_ex2 - 7 ** 2
check('after the 6, variance 18.08', var1, cond(SIX)[1], 18.08, tol_stated=0.005)
var2 = one_var
check('after heads, variance one die', var2, cond(SIXH)[1], 35 / 12)
rng = random.Random(20261107)
def sim_sd(fix_first=None, coin=None, n=400_000):
    xs = []
    for _ in range(n):
        c = coin or rng.choice('HT')
        k = 2 if c == 'H' else 4
        d = [rng.randint(1, 6) for _ in range(k)]
        if fix_first is not None:
            d[0] = fix_first
        xs.append(sum(d))
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / n)
sd0, sd1, sd2 = math.sqrt(var0), math.sqrt(var1), math.sqrt(var2)
check('sd at the open 4.58', sd0, sim_sd(), 4.58, tol=0.03, tol_stated=0.005)
check('sd after the 6 is 4.25', sd1, sim_sd(fix_first=6), 4.25, tol=0.03, tol_stated=0.005)
check('sd after heads 1.71', sd2, sim_sd(fix_first=6, coin='H'), 1.71, tol=0.02, tol_stated=0.005)

def half_width(sd):  # half an sd, to the nearest 0.5
    return round(sd / 2 * 2) / 2
def half_width_b(sd):  # second route: pick the nearest of the half-point grid by search
    grid = [k / 2 for k in range(0, 21)]
    return min(grid, key=lambda g: abs(g - sd / 2))
for name, sd, hw in (('open', sd0, 2.5), ('after the 6', sd1, 2), ('after heads', sd2, 1)):
    check(f'half-width {name}', half_width(sd), half_width_b(sd), hw)
check('width 5, 4, 2 (twice the half-widths)', 2 * half_width(sd0) + 2 * half_width(sd1) + 2 * half_width(sd2),
      5 + 4 + 2, 11)

# ---------- The round: quotes, trades, cash, position, P&L at fair ----------
GAMMA = F(1, 2)
def quote(fair, q, h):
    m = fair - GAMMA * q
    return m - h, m + h
events = [('quote', f0, F(5, 2)), ('buy', 1), ('reveal', f1, F(2)), ('sell', 2), ('reveal', f2, F(1)), ('buy', 1),
          ('settle', F(8))]
pos, cash, fair, h = 0, F(0), f0, F(5, 2)
bid, ask = quote(fair, pos, h)
quotes, pnls, edges = [(bid, ask)], [], []
for ev in events[1:]:
    if ev[0] == 'buy':       # interviewer buys at our ask: we sell
        n = ev[1]; pos -= n; cash += n * ask; edges.append(n * (ask - fair))
    elif ev[0] == 'sell':    # interviewer sells at our bid: we buy
        n = ev[1]; pos += n; cash -= n * bid; edges.append(n * (fair - bid))
    elif ev[0] == 'reveal':
        fair, h = ev[1], ev[2]
    elif ev[0] == 'settle':
        fair = ev[1]
    pnls.append(cash + pos * fair)
    if ev[0] != 'settle':
        bid, ask = quote(fair, pos, h)
        quotes.append((bid, ask))
stated_quotes = [(8, 13), (8.5, 13.5), (11.5, 15.5), (10.5, 14.5), (8, 10), (8, 10)]
# second route: centres by hand from m = F - 0.5 q
by_hand = [(10.5, 0, 2.5), (10.5, -1, 2.5), (13, -1, 2), (13, 1, 2), (9.5, 1, 1), (9.5, 0, 1)]
for i, ((b, a), (sb, sa), (fv, q, hh)) in enumerate(zip(quotes, stated_quotes, by_hand)):
    if i == 5:
        continue  # after the last trade the round ends flat; the model gives no sixth quote
    check(f'quote {i} bid', b, fv - 0.5 * q - hh, sb)
    check(f'quote {i} ask', a, fv - 0.5 * q + hh, sa)
check('centre after the buy is 11', f0 - GAMMA * -1, 10.5 + 0.5, 11)
check('centre after the 6 is 13.5', f1 - GAMMA * -1, 13 + 0.5, 13.5)
check('centre after the sale is 12.5', f1 - GAMMA * 1, 13 - 0.5, 12.5)
check('centre after heads is 9', f2 - GAMMA * 1, 9.5 - 0.5, 9)
stated_pnl = [2.5, 0, 3, -0.5, 0, 0]
hand_pnl = [13 - 10.5, 13 - 13, (13 - 23) + 13, (13 - 23) + 9.5, 13 - 23 + 10, 13 - 23 + 10]
for i, (p, hp, sp) in enumerate(zip(pnls, hand_pnl, stated_pnl)):
    check(f'P&L at fair after step {i + 1}', p, hp, sp)
check('cash after step 3 is 13 - 23 = -10', 13 - 2 * F(23, 2), 13 - 23, -10)
check('final cash -10 + 10 = 0', cash, -10 + 10, 0)
check('final position flat', pos, 1 - 2 + 1 - 0, 0)  # sold 1, bought 2, sold 1
check('edge on the sale at 13: 2.50', edges[0], 13 - 10.5, 2.5)
check('edge on the 2 bought at 11.5: 1.50 a lot, 3 in all', edges[1], 2 * (13 - 11.5), 3)
check('edge on the sale at 10: 0.50', edges[2], 10 - 9.5, 0.5)
check('total edge 6', sum(edges), 2.5 + 3 + 0.5, 6)
inv = (-1) * (f1 - f0) + 1 * (f2 - f1)
check('inventory: short 1 while fair rose 2.5, long 1 while it fell 3.5', inv, -(13 - 10.5) - (13 - 9.5), -6)
check('fair rose 2.5', f1 - f0, 2.5, 2.5)
check('fair fell 3.5', f1 - f2, 3.5, 3.5)
check('edge plus inventory equals final P&L 0', sum(edges) + inv, pnls[-1], 0)
check('total of 6 and a 2 is 8', 6 + 2, cond(lambda o: o[2][0] == 6 and o[2][1] == 2 and o[1] == 'H')[0], 8)

# ---------- Follow-up 1: a trader who sees the coin ----------
def informed_gain(bid, ask):
    """Exact expected gain a lot for a trader who sees the coin, by enumeration."""
    g = F(0)
    for c in 'HT':
        v = cond(lambda o, c=c: o[1] == c)[0]
        g += F(1, 2) * max(v - ask, bid - v, 0)
    return g
check('they take 1 a lot at 8 at 13', informed_gain(F(8), F(13)), F(1, 2) * (8 - 7) + F(1, 2) * (14 - 13), 1)
check('7 at 14 stops it', informed_gain(F(7), F(14)), 0, 0)
check('narrowest safe half-width is 3.5 (the coin swing)',
      min(k / F(4) for k in range(0, 40) if informed_gain(f0 - k / F(4), f0 + k / F(4)) == 0), (14 - 7) / 2, 3.5)

# ---------- The item as written ----------
d = json.load(open(HW))
it = [x for x in d['items'] if x['id'] == 'h-coin-dice-aloud']
truth('item present once', len(it) == 1)
it = it[0]; w = it['widget']
truth('homework holds at most 12 items', len(d['items']) <= 12)
truth('one performance item in the file', sum(1 for x in d['items'] if x.get('performance')) == 1)
truth('aloud shape: seconds, think, 1 to 5 follow-ups', 15 <= w['seconds'] <= 1800 and w['think'] > 0 and 1 <= len(w['followUps']) <= 5)
text = w['model'] + ' ' + ' '.join(r['text'] for r in w['rubric']) + ' ' + it['explain']['text']
for s in ['8 at 13', '8.5 at 13.5', '11.5 at 15.5', '10.5 at 14.5', '8 at 10', '7 at 14', '£2.50', '£1.50', '£3',
          '£0.50', '£6', '131.25', '4.58', '4.25', '1.71', '67.08', '18.08', '= 21', '5 wide', '4 wide', '2 wide',
          'Centre 11', 'centre at 13.5', 'Centre 12.5', 'centre at 9', 'rose 2.5', 'fell 3.5', '£1 a lot', 'total is 8']:
    truth(f'item states "{s}"', s in text)

# ---------- Rubric: every passing tick set, none skipping a named part ----------
rub = w['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
truth('rubric sums to 10 over 3 to 5 rows', sum(pts) == 10 and 3 <= len(rub) <= 5)
truth('not every row required', not all(req))
named = {0: 'quote with its fair value', 1: 'update after information', 2: 'reason for width and skew'}
passes = []
for mask in range(1 << len(rub)):
    ticks = [i for i in range(len(rub)) if mask >> i & 1]
    if sum(pts[i] for i in ticks) >= 7 and all(i in ticks for i in range(len(rub)) if req[i]):
        passes.append(ticks)
print('passing tick sets (rows from 1):', [[i + 1 for i in t] for t in passes])
for i, name in named.items():
    truth(f'no pass skips row {i + 1} ({name})', all(i in t for t in passes))
# second route: the most a set without row i can score, ignoring the required flags
for i, name in named.items():
    best = sum(pts) - pts[i]
    truth(f'row {i + 1} is required or its loss drops below 7', req[i] or best < 7)

print(f'{len(fails)} failures')
sys.exit(1 if fails else 0)
