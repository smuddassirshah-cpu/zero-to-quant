#!/usr/bin/env python3
"""Concept audit checks, mm-games level 3 (l10 to l13, review-3, homework-3).

Exits 0 when the content is correct. A check that fails because the content
is wrong is marked EXPECTED_FAIL: it is listed, the corrected assert sits in a
comment beside it, and it does not change the exit code.
Run from the repo root: python3 docs/reports/mm-games-L3-concepts.py
"""
import json, math, os, random, statistics, sys
from fractions import Fraction as F
from itertools import product
from math import comb, erf, isclose, log, sqrt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'mm-games')
FAILS, XFAILS, PASSES = [], [], [0]


def check(name, cond, expected_fail=False):
    if cond:
        PASSES[0] += 1
        if expected_fail:
            print(f'NOTE  {name}: marked EXPECTED_FAIL but passes (content fixed?)')
    elif expected_fail:
        XFAILS.append(name); print(f'EXPECTED_FAIL  {name}')
    else:
        FAILS.append(name); print(f'FAIL  {name}')


def load(name):
    return json.load(open(os.path.join(CDIR, name + '.json')))


def close(a, b, tol):
    if isinstance(a, (tuple, list)):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    return isclose(float(a), float(b), rel_tol=tol.get('rel', 1e-9), abs_tol=tol.get('abs', 1e-12))


def run_code_widget(label, w, namespace_out=None):
    """Solution passes every example and hidden test in CPython; starter fails."""
    def run(src):
        ok = 0; cases = w.get('examples', []) + w['tests']
        for c in cases:
            ns = {}
            try:
                exec(w.get('prelude', '') + '\n' + src, ns)
                if c.get('setup'): exec(c['setup'], ns)
                got = eval(c['call'], ns); exp = eval(str(c['expect']), ns)
                mode = c.get('compare', 'equal')
                if mode == 'isclose':
                    good = close(got, exp, c.get('tol') or {})
                elif mode == 'fraction':
                    good = isinstance(got, (F, int)) and F(got) == F(exp)
                else:
                    good = got == exp
            except Exception:
                good = False
            ok += bool(good)
        return ok, len(cases)
    ok, n = run(w['solution'])
    check(f'{label}: solution passes {ok}/{n}', ok == n)
    ok2, _ = run(w['starter'])
    check(f'{label}: starter fails', ok2 < n)
    if namespace_out is not None:
        exec(w.get('prelude', '') + '\n' + w['solution'], namespace_out)


Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
DIE = range(1, 7)

# ---------- l10: limits, ruin, Kelly ----------
check('l10 room: limit 4, long 3: buy 1, sell 7; limit 5, short 2: sell 3, buy 7', (4 - 3, 4 + 3, 5 + (-2), 5 - (-2)) == (1, 7, 3, 7))
cash = 11.5 - 4 * 9.5
check('l10 model run: cash -26.50, +3.50 at 10, -5.50 at 7, swing 9 (12 at four lots)', cash == -26.5 and cash + 30 == 3.5 and cash + 21 == -5.5)
check('l10 model blotter running P&L at 10', [1.5, 2.0, 2.5, 3.0, 3.5] == [1.5 + 0.5 * i for i in range(5)])
p_tail = Phi((-200 - 10) / 100)
check(f'l10 normal bet (mean 10, sd 100) loses more than 200 with chance {p_tail:.4f}, about 1.8%', abs(p_tail - 0.018) < 0.001)
# the 1.8% needs the normal shape: a two-point bet with the same mean and sd never loses more than 200
two_point_loss = 10 - 100
# (corrected claim, fix pass) l10 s4 now states the 1.8% under a roughly normal outcome
check('l10 s4: the 1.8% holds for a roughly normal outcome (Phi(-2.1) = 0.0179); a +110 / -90 bet with the same mean and sd never loses 200  (corrected claim, fix pass)',
      abs(Phi(-2.1) - 0.0179) < 1e-4 and two_point_loss > -200 and abs(0.5 * 110 + 0.5 * (-90) - 10) < 1e-12 and abs(sqrt(0.5 * 100 ** 2 + 0.5 * 100 ** 2) - 100) < 1e-9
      and 'roughly normal' in load('l10-position-limits')['screens'][4]['explain']['text'])


def ruin(p, stake, start, target):
    r = (1 - p) / p; i, n = start // stake, target // stake
    return (r ** i - r ** n) / (1 - r ** n)


check('l10 ruin: 0.0178, 0.401, 0.45', abs(ruin(0.55, 1, 20, 40) - 0.0178) < 5e-5 and abs(ruin(0.55, 10, 20, 40) - 0.401) < 5e-4 and abs(ruin(0.55, 20, 20, 40) - 0.45) < 1e-12)
check('hw3 ruin 81/202', F(81, 121) / (1 + F(81, 121)) == F(81, 202))
rng = random.Random(77)


def ruin_mc(stake, n=20000):
    bad = 0
    for _ in range(n):
        x = 20
        while 0 < x < 40:
            x += stake if rng.random() < 0.55 else -stake
        bad += x <= 0
    return bad / n


check('l10 sim: ruin by stake matches the formula', abs(ruin_mc(10) - 0.401) < 0.015 and abs(ruin_mc(1, 6000) - 0.0178) < 0.006)
g = lambda f, p=0.6, b=1: p * log(1 + b * f) + (1 - p) * log(1 - f)
check('l10 growth: g(0.05) 0.008757, g(0.1) 0.015042, g(0.2) 0.020136, g(0.4) -0.002447',
      all(abs(g(f) - v) < 5e-7 for f, v in [(0.05, 0.008757), (0.1, 0.015042), (0.2, 0.020136), (0.4, -0.002447)]))
fbest = max((i / 1000 for i in range(0, 999)), key=g)
check('l10 growth peaks at f = 0.2 = p - (1-p)/b', abs(fbest - 0.2) < 1e-9)
check('l10 stake 5 grows at less than half the Kelly rate', g(0.05) < 0.5 * g(0.2))
check('l10 median after 50 bets 273.68; mean 710.67; linear slip 201', abs(100 * 1.2 ** 30 * 0.8 ** 20 - 273.68) < 5e-3 and abs(100 * 1.04 ** 50 - 710.67) < 5e-3 and round(100 * (1 + 50 * g(0.2))) == 201)
pm = [comb(50, k) * 0.6 ** k * 0.4 ** (50 - k) for k in range(51)]
check('l10 median number of wins in 50 is 30', sum(pm[:30]) < 0.5 <= sum(pm[:31]))
rng = random.Random(12); finals = []
for _ in range(20001):
    w = 100.0
    for _ in range(50):
        w *= 1.2 if rng.random() < 0.6 else 0.8
    finals.append(w)
check(f'l10 sim: median {statistics.median(finals):.1f} near 273.68, mean {statistics.fmean(finals):.0f} far above it', abs(statistics.median(finals) - 273.68) < 0.01 and statistics.fmean(finals) > 550)
kelly = lambda p, b: p - (1 - p) / b
check('l10 Kelly: 0.55 evens 0.1; 0.4 at 2 to 1 0.1 (50 of 500); 0.5 at 2 to 1 0.25', abs(kelly(0.55, 1) - 0.1) < 1e-12 and abs(kelly(0.4, 2) - 0.1) < 1e-12 and kelly(0.5, 2) == 0.25)
# "Neither rule asks how sure you feel": the Kelly stake is a function of p, the stated win chance
# (corrected claim, fix pass) l10 s9 now says Kelly needs a win chance you can defend, not a feeling
check('l10 s9: the Kelly stake rises with the win chance (0.1 at 0.55, 0.3 at 0.65), so the input must be defended  (corrected claim, fix pass)',
      kelly(0.65, 1) > kelly(0.55, 1) and abs(kelly(0.65, 1) - 0.3) < 1e-12
      and 'Neither asks how sure you feel' not in load('l10-position-limits')['screens'][9]['explain']['text'])
check('l10 desk: 40,000/800 = 50 and 40,000/200 = 200', 40000 / 800 == 50 and 40000 / 200 == 200)
check('l10 quiz: long 4 at 9.5, roll 3: -26', 4 * (3 - 9.5) == -26)
run_code_widget('l10 s10 code', load('l10-position-limits')['screens'][10]['widget'])

# ---------- l11: hedging ----------
resid = lambda h, r, sa, sb: sqrt(sa * sa + h * h * sb * sb - 2 * h * r * sa * sb)
hb = max((i / 1000 for i in range(0, 3001)), key=lambda h: -resid(h, 0.8, 2, 1.6))
check('l11 minimum-variance h = rho*sa/sb = 1.0 for (0.8, 2, 1.6); residual 1.2', abs(hb - 1.0) < 1e-9 and abs(resid(1, 0.8, 2, 1.6) - 1.2) < 1e-12)
check('l11 h = 1.35, 0.4, 1.25, 1.2', all(abs(r * a / b - v) < 1e-12 for r, a, b, v in [(0.9, 3, 2, 1.35), (0.8, 2, 4, 0.4), (0.7, 2.5, 1.4, 1.25), (0.6, 3, 1.5, 1.2)]))
check('l11 over-hedge: h = 2 gives sd 2 again; pound for pound with the 4% future gives 2.68%', abs(resid(2, 0.8, 2, 1.6) - 2) < 1e-12 and abs(resid(1, 0.8, 2, 4) - 2.683) < 1e-3)
check('l11 residuals: 1.79 (rho 0.7, 2.5), 4 (0.6, 5), 0.87 (0.9, 2)', abs(2.5 * sqrt(0.51) - 1.79) < 5e-3 and abs(5 * 0.8 - 4) < 1e-12 and abs(2 * sqrt(0.19) - 0.87) < 5e-3)
rng = random.Random(31); zs = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(60000)]
A = [2 * z1 for z1, _ in zs]; B = [1.6 * (0.8 * z1 + 0.6 * z2) for z1, z2 in zs]
sd_h = lambda h: statistics.pstdev([a - h * b for a, b in zip(A, B)])
check('l11 sim: hedged sd is least near h = 1 (1.2), and 2 at h = 0 and h = 2', sd_h(1.0) < min(sd_h(0.8), sd_h(1.25)) and abs(sd_h(1.0) - 1.2) < 0.02 and abs(sd_h(0) - 2) < 0.03 and abs(sd_h(2) - 2) < 0.03)
# dice: sum hedged with the first die
rolls = list(product(DIE, repeat=2))
var = lambda xs: sum(x * x for x in xs) / len(xs) - (sum(xs) / len(xs)) ** 2
check('l11 dice: sd of sum 2.4152, of sum less die 1 1.7078; ratio 1 is the minimum', abs(sqrt(var([a + b for a, b in rolls])) - 2.4152) < 5e-5 and abs(sqrt(var([b for a, b in rolls])) - 1.7078) < 5e-5
      and min(range(0, 21), key=lambda k: var([a + b - k / 10 * a for a, b in rolls])) == 10)
check('l11 model run: +6 on the sums, hedge -1.20, total 4.80; sd 4.83 to 3.42', (-12 + 32) - 2 * 7 == 6 and abs(2 * (3 - 3.6) + 1.2) < 1e-12 and abs(2 * 2.4152 - 4.83) < 5e-3 and abs(2 * 1.7078 - 3.42) < 5e-3)
check('l11 quiz: delta hedge 600 shares; hedge cost 0.60', 10 * 100 * 0.6 == 600 and abs(3 * 0.2 - 0.6) < 1e-12)
# Units convention. With sds given as percentage moves, h = rho*sa/sb is pounds of B per pound of A.
# It is "units of B per unit of A" only when a unit of each is worth the same. Example: A at 5 pounds a unit, B at 100.
pa, pb = 5.0, 100.0; sa, sb, rho = 0.03, 0.02, 0.9   # the lesson's new pair
pnl_sd = lambda units_b: sqrt((pa * sa) ** 2 + (units_b * pb * sb) ** 2 - 2 * units_b * rho * pa * sa * pb * sb)
best_units = min((i / 10000 for i in range(0, 20001)), key=pnl_sd)
print(f'      l11: A at 5 pounds, B at 100 pounds: best hedge is {best_units:.4f} units of B per unit of A, not 1.35')
# (corrected claim, fix pass) l11 now reads h from percentage sds as pounds of B per pound of A.
# In pounds the best hedge for £5 of A (one unit) is 1.35 * 5 = £6.75 of B, i.e. 0.0675 units at £100.
pounds_b = best_units * pb
l11c = load('l11-hedging')
check('l11 s2: with percentage sds h = 1.35 is pounds of B per pound of A; in units it is 1.35 times the price ratio, 0.0675 here  (corrected claim, fix pass)',
      abs(best_units - 1.35 * pa / pb) < 1e-3 and abs(pounds_b / pa - 1.35) < 1e-2
      and 'pounds of B for each pound of A' in l11c['screens'][2]['prose'] and '£1.35 of B' in l11c['screens'][2]['explain']['text']
      and 'pounds of B sold for each pound of A' in l11c['summary']['formula']['note'] and 'units of B' not in l11c['screens'][1]['prose']
      and 'units of B' not in load('review-3')['items'][4]['question'])
# (fix-pass read follow-up) the summary note also gives the units reading: with sds of price changes per unit,
# h = rho*sa/sb is units of B per unit of A. Dice check: sum against die 1, rho = 1/sqrt(2), h = 1 unit per unit.
sd_sum, sd_die = sqrt(var([a + b for a, b in rolls])), sqrt(var([a for a, b in rolls]))
rho_d = (sum((a + b - 7) * (a - 3.5) for a, b in rolls) / len(rolls)) / (sd_sum * sd_die)
check('l11 summary note: with sds in pounds a unit, h is units of B per unit of A; dice h = 1  (fix-pass read follow-up)',
      abs(rho_d - 1 / sqrt(2)) < 1e-12 and abs(rho_d * sd_sum / sd_die - 1) < 1e-12
      and 'With sds in pounds a unit, it is units of B for each unit of A.' in l11c['summary']['formula']['note'])
run_code_widget('l11 s9 code', load('l11-hedging')['screens'][9]['widget'])

# ---------- l12: thinking aloud ----------
check('l12 transcript: fair 13 after the 6; P&L +1 at 13 (slips 1.5 and 2)', 6 + 2 * 3.5 == 13 and (12 - 24) + 13 == 1 and (12 - 24) + 13.5 == 1.5 and (12 - 24) + 14 == 2)
check('l12 interrupted: short 2, fair 13, skew 0.25: 12.5 at 14.5; long 2 skew 0.5 centre 9.5', (13 + 0.5 - 1, 13 + 0.5 + 1) == (12.5, 14.5) and 10.5 - 0.5 * 2 == 9.5)
check('l12 quiz: 10 shown: 10 + 2*354/51 = 23.8824', abs(float(10 + 2 * F(354, 51)) - 23.8824) < 5e-5)
run_code_widget('l12 s8 code', load('l12-thinking-aloud')['screens'][8]['widget'])

# ---------- l13: the full game ----------
fair_after = lambda shown: sum(shown) + (3 - len(shown)) * F(364 - sum(shown), 52 - len(shown))
check('l13 fair values 21, 308/17, 427/25', (fair_after([]), fair_after([4]), fair_after([4, 6])) == (21, F(308, 17), F(427, 25)))
half = lambda x: F(round(2 * x), 2)   # nearest 0.5 (no ties arise in these games)


def game(cards, script, reveal_before, rule, limit=3):
    """Replay a scripted eight-turn game. script[t] = (act, size, price limit) or None; rule(fair, pos) -> (bid, ask)."""
    pos, cash, shown, blotter, quotes = 0, F(0), [], [], []
    for t in range(1, 9):
        if t in reveal_before: shown.append(cards[len(shown)])
        bid, ask = rule(fair_after(shown), pos); quotes.append((float(bid), float(ask)))
        act = script.get(t)
        if act:
            side, size, px = act
            if side == 'lift' and ask <= px and pos - 1 >= -limit:
                pos -= 1; cash += ask; blotter.append((t, 'sell', ask, fair_after(shown)))
            if side == 'hit' and bid >= px and pos + 1 <= limit:
                pos += 1; cash -= bid; blotter.append((t, 'buy', bid, fair_after(shown)))
    return pos, cash + pos * sum(cards), blotter, quotes


skew = lambda f, q: (half(f - F(q, 2)) - 2, half(f - F(q, 2)) + 2)
noskew = lambda f, q: (half(f) - 2, half(f) + 2)
stale = lambda f, q: (F(19), F(23))
S13 = {1: ('lift', 2, 23), 3: ('hit', 2, 19), 4: ('lift', 2, F(41, 2)), 6: ('hit', 1, 16)}
pos, pnl, blot, quotes = game([4, 6, 5], S13, {3, 6}, skew)
check('l13 model quotes match the hinted strategy', quotes == [(19, 23), (19.5, 23.5), (16.5, 20.5), (16.5, 20.5), (17, 21), (16, 20), (15.5, 19.5), (15.5, 19.5)])
check('l13 model run: sold at 23 and 20.5, bought at 16, short 1, +12.50', [(t, s, float(p)) for t, s, p, _ in blot] == [(1, 'sell', 23.0), (4, 'sell', 20.5), (6, 'buy', 16.0)] and (pos, pnl) == (-1, F(25, 2)))
check('l13 stale run: +1, 0.00; no-skew run: short 2, +13.00', game([4, 6, 5], S13, {3, 6}, stale)[:2] == (1, 0) and game([4, 6, 5], S13, {3, 6}, noskew)[:2] == (-2, 13))
check('l13 king instead of 5: model +4.50, no skew -3; queen: +5.50', game([4, 6, 13], S13, {3, 6}, skew)[1] == F(9, 2) and game([4, 6, 13], S13, {3, 6}, noskew)[1] == -3 and F(55, 2) - 22 == F(11, 2))
realised = [float((p - 15) if s == 'sell' else (15 - p)) for _, s, p, _ in blot]
at_fair = [round(float((p - f) if s == 'sell' else (f - p)), 2) for _, s, p, f in blot]
print(f'      l13 model trades: against the true sum {realised}; edge against fair at the time {at_fair}')
check('l13 table figures +8.00, +5.50, -1.00 are P&L against the true sum', realised == [8.0, 5.5, -1.0])
# (corrected claim, fix pass) l13 now heads the column "P&L (£)" (against the true sum) and keeps "edge" for price against fair
l13c = load('l13-full-game')
check('l13 s4/s6: the +8.00, +5.50, -1.00 column is P&L against 15; the edges against fair were +2.00, +2.38, +1.08  (corrected claim, fix pass)',
      at_fair == [2.0, 2.38, 1.08] and realised != at_fair
      and l13c['screens'][4]['canvas']['right']['params']['columns'][4] == 'P&L (£)' and l13c['screens'][6]['canvas']['params']['columns'][4] == 'P&L (£)'
      and 'edge against' not in l13c['screens'][8]['prose'])
# "the interviewer, who knew the cards": their own trades against the true sum
theirs = [-(x) for x in realised]
# (corrected claim, fix pass) l13 s4 now says the interviewer had just seen the 4, not that they knew the cards
check('l13 s4: the interviewer lost 8 and 5.50 on their purchases, so they did not know the cards; the turn-3 sale rests on the public 4  (corrected claim, fix pass)',
      theirs == [-8.0, -5.5, 1.0] and 'knew the cards' not in l13c['screens'][4]['prose'] and 'had just seen the 4' in l13c['screens'][4]['prose'])
check('l13 stale by trade: 8 - 4 - 4 = 0; desk review 20 + 6 - 12 = 14', 8 - 4 - 4 == 0 and abs(100 * 0.2 + 60 * 0.1 - 40 * 0.3 - 14) < 1e-9)
run_code_widget('l13 s9 code', load('l13-full-game')['screens'][9]['widget'])

# ---------- review-3 ----------
check('r3 limit game: cash +10, short 1, settles at 8: +2', 8 + 8 - 6 - 8 == 2)
check('r3 room 5; Kelly 40; double Kelly shrinks; residual 0.87; ledger +10; 2 shown 16.20',
      3 + 2 == 5 and abs(kelly(0.55, 1) * 400 - 40) < 1e-9 and g(0.4) < 0 and 2 * (23 - 17) + (17 - 19) == 10 and abs(float(2 + 2 * F(362, 51)) - 16.20) < 5e-3)

# ---------- homework-3 ----------
hw = load('homework-3')
ns = {}
run_code_widget('hw3 full_game', hw['items'][0]['widget'], ns)
run_code_widget('hw3 kelly_game', hw['items'][1]['widget'])
# narrated game ledger
marks = [23 - 21, 23 - fair_after([4]), F(87, 2) - 2 * fair_after([4]), F(87, 2) - 2 * fair_after([4, 6]), F(55, 2) - fair_after([4, 6]), F(55, 2) - 15]
check('hw3 narrated ledger +2, +4.88, +7.26, +9.34, +10.42, +12.50', [round(float(m), 2) for m in marks] == [2.0, 4.88, 7.26, 9.34, 10.42, 12.5])
# mock round: cards 8, J, J
fa = lambda shown: sum(shown) + (3 - len(shown)) * F(364 - sum(shown), 52 - len(shown))
SM = {1: ('hit', 2, 19), 3: ('lift', 2, 23), 5: ('hit', 1, F(39, 2)), 7: ('lift', 1, F(55, 2))}
pos, pnl, blot, quotes = game([8, 11, 11], SM, {3, 6}, skew)
check('hw3 mock model: quotes as the strategy; long 1; +18.50', quotes == [(19, 23), (18.5, 22.5), (19.5, 23.5), (19.5, 23.5), (19.5, 23.5), (23, 27), (23, 27), (23.5, 27.5)] and (pos, pnl) == (1, F(37, 2)))
check('hw3 mock: stale -3 (sold twice at 23); no skew +21 long 2', game([8, 11, 11], SM, {3, 6}, stale)[:2] == (-1, -3) and game([8, 11, 11], SM, {3, 6}, noskew)[:2] == (2, 21))
check('hw3 mock fair values 21, 1120/51, 259/10', (fa([8]), fa([8, 11])) == (F(1120, 51), F(259, 10)))
mm = [fa([8]) - 19, 2 * fa([8]) - F(77, 2), 2 * fa([8, 11]) - F(77, 2), fa([8, 11]) - F(23, 2)]
check('hw3 mock ledger +2.96, +5.42, +13.30, +14.40; side bet 20 with expected gain 4', [round(float(m), 2) for m in mm] == [2.96, 5.42, 13.3, 14.4] and abs(20 * (0.6 - 0.4) - 4) < 1e-12)
# (corrected claim, fix pass) make_script now trades the hedge before the first card turns, priced at 7 +- 0.1,
# so the contract still carries risk. The old placement, after the reveal, is kept below as the reason for the move.
full_game = ns['full_game']; skew_rule = ns['skew_rule']; make_script = ns['make_script']
DECK = [v for v in range(1, 14) for _ in range(4)]


def hedge_first(sc):
    kinds = [k for k, _ in sc]
    return 'hedge' in kinds and kinds.index('hedge') < kinds.index('reveal') and dict(sc)['hedge'] in (F(69, 10), F(71, 10))


check('hw3 make_script: the hedge comes before the first reveal, at 6.9 or 7.1, for seeds 1, 2, 3 and 7  (corrected claim, fix pass)',
      all(hedge_first(make_script(k)) for k in (1, 2, 3, 7)))


def spread_of_pnl(with_hedge, hedge_first):
    outs = []
    rest = DECK[:]; rest.remove(4)
    for i in range(len(rest)):
        for j in range(len(rest)):
            if i == j: continue
            ev = [('buy', 2)]
            if with_hedge and hedge_first: ev.append(('hedge', F(71, 10)))
            ev.append(('reveal', 4))
            if with_hedge and not hedge_first: ev.append(('hedge', F(41, 10)))
            ev += [('reveal', rest[i]), ('reveal', rest[j])]
            outs.append(float(full_game(ev, skew_rule)[0]))
    return statistics.pstdev(outs)


s_none, s_after = spread_of_pnl(False, False), spread_of_pnl(True, False)
print(f'      hw3: sd of final P&L over the two unseen cards, short 2: no hedge {s_none:.4f}, hedge after the reveal {s_after:.4f}')
check('hw3: a hedge traded after the first card is shown leaves the spread unchanged, so the engine now hedges before the reveal  (corrected claim, fix pass)',
      abs(s_after - s_none) < 1e-9)


def spread_three(with_hedge):
    rng = random.Random(5); outs = []
    for _ in range(40000):
        c = rng.sample(DECK, 3)
        ev = [('buy', 2)] + ([('hedge', F(71, 10))] if with_hedge else []) + [('reveal', x) for x in c]
        outs.append(float(full_game(ev, skew_rule)[0]))
    return statistics.pstdev(outs)


s0, s1 = spread_three(False), spread_three(True)
print(f'      hw3: sd of final P&L, short 2 before any card: no hedge {s0:.2f}, hedged before the reveal {s1:.2f}')
check('hw3: hedging the first card before it is shown removes about a third of the variance', 0.60 < (s1 / s0) ** 2 < 0.73)
# exact, two cards from one deck: cov = -var/51, so the minimum-variance ratio of the sum on the first card is 49/51
mu_c = F(sum(DECK), 52); var_c = F(sum(v * v for v in DECK), 52) - mu_c ** 2
cov_c = F(sum(a * b for i, a in enumerate(DECK) for j, b in enumerate(DECK) if i != j), 52 * 51) - mu_c ** 2
check('hw3: exact minimum-variance ratio of the three-card sum on the first card is 49/51', (var_c + 2 * cov_c) / var_c == F(49, 51) and cov_c == -var_c / 51)
h3 = hw['items'][0]
check('hw3 prose and explain match the code: hedge before that card turns; seed 1 ends at +16/5  (corrected claim, fix pass)',
      'before that card turns' in h3['prose'] and '+16/5' in h3['explain']['text'] and full_game(make_script(1), skew_rule, 3) == (F(16, 5), 3))
print('      hw3 expected values from the content:')
for t in h3['widget']['tests'][:4] + h3['widget']['tests'][5:7]:
    print('        ', t['call'], '->', t['expect'])
# coin and dice market
two = [a + b for a, b in product(DIE, repeat=2)]; four = [sum(r) for r in product(DIE, repeat=4)]
mix_mean = (sum(two) / 36 + sum(four) / 1296) / 2
mix_var = (sum(x * x for x in two) / 36 + sum(x * x for x in four) / 1296) / 2 - mix_mean ** 2
check('hw3 coin and dice: fair 10.5, variance 21, sd 4.58, coin share 12.25', mix_mean == 10.5 and abs(mix_var - 21) < 1e-9 and abs(sqrt(21) - 4.58) < 5e-3)
rem_var = ((35 / 12 + 3.5 ** 2) + (35 / 4 + 10.5 ** 2)) / 2 - 7 ** 2
check('hw3 coin and dice: after the 6 fair 13, remaining variance 18.08, sd 4.25', 6 + 0.5 * 3.5 + 0.5 * 10.5 == 13 and abs(rem_var - 18.0833) < 1e-3 and abs(sqrt(rem_var) - 4.25) < 5e-3)
check('hw3 coin and dice ledger: +2.50, 0, +3, -0.50, 0; edge 6 given back', (13 - 10.5, 13 - 13, -10 + 13, -10 + 9.5, -10 + 10) == (2.5, 0, 3, -0.5, 0) and 2.5 + 3 + 0.5 == 6 and -(13 - 10.5) + (9.5 - 13) == -6)
rng = random.Random(3); tot = 0; n = 200000; sq = 0
for _ in range(n):
    k = 2 if rng.random() < 0.5 else 4
    x = sum(rng.randint(1, 6) for _ in range(k)); tot += x; sq += x * x
check('hw3 sim: coin and dice mean 10.5 and sd 4.58', abs(tot / n - 10.5) < 0.04 and abs(sqrt(sq / n - (tot / n) ** 2) - 4.583) < 0.03)
check('hw3 follow-up 1: 8 at 13 loses 1 a lot to someone who sees the coin; 7 at 14 loses nothing', (8 - 7, 14 - 13) == (1, 1))

print(f'\n{PASSES[0]} checks passed, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL')
for x in XFAILS:
    print('  EXPECTED_FAIL:', x)
sys.exit(1 if FAILS else 0)
