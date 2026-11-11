#!/usr/bin/env python3
"""Concept audit round 2, mm-games level 3 (l10 to l13, review-3, homework-3).
Recomputes every computable claim independently of the author scripts, replays every trade game
through the engine's pure game module (app/js/engine/widgets/trade.js, needs node), and runs every
code solution against its hidden tests. Exits 0 when the content is correct."""
import json, math, os, random, statistics, subprocess, sys
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
def card_fair(shown, n, T=364, N=52):
    k = len(shown); s = sum(shown)
    return F(s) if k == n else s + (n - k) * F(T - s, N - k)
phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
JS = "const api=require(process.argv[1]);const a=JSON.parse(require('fs').readFileSync(0,'utf8'));const r=api.play(a.spec,a.quotes);console.log(JSON.stringify({log:r.g.log,pos:r.g.pos,cash:r.g.cash,v:r.verdict}))"
def play(spec, quotes):
    r = subprocess.run(['node', '-e', JS, os.path.join(ROOT, 'app', 'js', 'engine', 'widgets', 'trade.js')],
                       input=json.dumps({'spec': spec, 'quotes': quotes}), capture_output=True, text=True, check=True)
    return json.loads(r.stdout)
def fills(res): return [(e['turn'], e['fill']['side'], e['fill']['qty'], e['fill']['price']) for e in res['log'] if e['fill']]
def rule_run(spec, gamma, width, skewed=True):
    """Quote width around fair - gamma * position, centre rounded to 0.5, deciding each turn from the turns before it."""
    quotes = []
    for t in range(spec['turns']):
        if t == 0: pos, mark = 0, spec['fair']
        else:
            res = play(spec, quotes); pos = res['log'][t - 1]['pos']
            mark = spec['fair']
            for s in spec.get('schedule', []):
                if s['turn'] <= t + 1 and 'fair' in s: mark = s['fair']
        c = math.floor(2 * (mark - (gamma * pos if skewed else 0)) + 0.5) / 2
        quotes.append({'bid': c - width / 2, 'ask': c + width / 2, 'size': 1})
    return quotes, play(spec, quotes)

l10, l11, l12, l13 = load('l10-position-limits'), load('l11-hedging'), load('l12-thinking-aloud'), load('l13-full-game')
r3, h3 = load('review-3'), load('homework-3')
S10, S11, S12, S13 = l10['screens'], l11['screens'], l12['screens'], l13['screens']
A = lambda s: s['widget']['answer']

# ---------- l10 ----------
ok(A(S10[0]) == 4 - 3 and S10[0]['widget']['wrong'][1]['value'] == 4 + 3, 'l10 s0 room to buy 1, room to sell 7')
w = S10[2]['widget']; res = play(w, w['strategy'])
ok(res['v']['ok'] and res['v']['pnl'] == 3.5 and res['pos'] == 3 and fills(res) == [(1, 'sell', 1, 11.5), (2, 'buy', 1, 9.5), (3, 'buy', 1, 9.5), (4, 'buy', 1, 9.5), (5, 'buy', 1, 9.5)] and max(abs(e['pos']) for e in res['log']) < 4,
   'l10 s2 model run: one buyer then sellers; sold 1 at 11.5, bought 4 at 9.5; long 3, +3.50, limit never touched')
ok(close(res['cash'], -26.5) and w['value'] == 5 + 1 + 4 and A(S10[3]) == -26.5 + 3 * 7 and 3 * (10 - 7) == 9 and 4 * 3 == 12, 'l10 s3 cash -26.50; at a roll of 7 the P&L is -5.50')
ok(abs(phi((-200 - 10) / 100) - 0.018) < 0.0005, 'l10 s4 a normal bet (mean 10, sd 100) loses more than 200 about 1.8%% of the time (%.4f)' % phi(-2.1))
def ruin(p, i, n):
    r = (1 - p) / p; return (r ** i - r ** n) / (1 - r ** n)
ru = [ruin(0.55, 20, 40), ruin(0.55, 2, 4), ruin(0.55, 1, 2)]
ok(abs(ru[0] - 0.018) < 0.0005 and abs(ru[1] - 0.401) < 0.0005 and abs(ru[2] - 0.45) < 1e-9 and ru[2] == max(ru), 'l10 s5 gambler\'s ruin 1.8%, 40.1%, 45%')
rng = random.Random(105); mc = []
for stake, trials in ((1, 20000), (10, 40000), (20, 40000)):
    lost = 0
    for _ in range(trials):
        x = 20
        while 0 < x < 40: x += stake if rng.random() < 0.55 else -stake
        lost += x <= 0
    mc.append(lost / trials)
ok(abs(mc[0] - ru[0]) < 0.004 and abs(mc[1] - ru[1]) < 0.01 and abs(mc[2] - ru[2]) < 0.01, 'l10 s5 Monte Carlo ruin shares %.4f, %.4f, %.4f' % tuple(mc))
g = lambda f, p=0.6, b=1: p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)
best = max(range(1, 1000), key=lambda i: g(i / 1000)) / 1000
ok(best == 0.2 and S10[6]['widget']['points'][0]['target']['x'] == 0.2 and abs(g(0.2) - 0.020136) < 1e-6 and abs(g(0.05) - 0.008757) < 1e-6, 'l10 s6 growth peaks at f = 0.2 with g = 0.0201')
ok(abs(g(0.1) - 0.015042) < 1e-6 and abs(g(0.4) + 0.002447) < 1e-6 and g(0.05) < g(0.2) / 2 and 1 - 0.6 ** 50 > 0.999999, 'l10 s7 half Kelly 0.0150, double Kelly -0.0024, a twentieth grows at less than half the Kelly rate')
med = 100 * 1.2 ** 30 * 0.8 ** 20
ok(abs(A(S10[8]) - med) < 1 and abs(med - 100 * math.exp(50 * g(0.2))) < 1e-6 and abs(100 * 1.04 ** 50 - 711) < 1 and abs(100 * (1 + 50 * g(0.2)) - 201) < 1, 'l10 s8 median 273.68, mean 711, linear slip 201')
# median wins of Binomial(50, 0.6) is 30, and a Monte Carlo median of the bankroll
cdf = 0; k = 0
while True:
    cdf += math.comb(50, k) * 0.6 ** k * 0.4 ** (50 - k)
    if cdf >= 0.5: break
    k += 1
rng = random.Random(108); fin = []
for _ in range(20001):
    b = 100.0
    for _ in range(50): b *= 1.2 if rng.random() < 0.6 else 0.8
    fin.append(b)
ok(k == 30 and abs(statistics.median(fin) - med) < 1e-6 and abs(statistics.mean(fin) - 711) < 60, 'l10 s8 the median path wins 30; Monte Carlo median %.2f, mean %.0f' % (statistics.median(fin), statistics.mean(fin)))
ok(close(A(S10[9]), 0.55 - 0.45 / 1), 'l10 s9 Kelly at evens, 0.55')
code(S10[10]['widget'], 'l10 s10')
ok(A(S10[11]) == 40000 / 800 and S10[11]['widget']['wrong'][0]['value'] == 40000 / 200, 'l10 s11 lots by risk')
q = l10['quiz']
ok(A(q[0]) == 5 + (-2) and close(A(q[2]), (0.4 - 0.6 / 2) * 500) and close(0.4 * 2 - 0.6, 0.2) and A(q[3]) == 4 * (3 - 9.5), 'l10 quiz keys')

# ---------- l11 ----------
hr = lambda rho, sa, sb: rho * sa / sb
resid = lambda rho, sa: sa * math.sqrt(1 - rho ** 2)
var_h = lambda h, rho, sa, sb: sa ** 2 + h ** 2 * sb ** 2 - 2 * h * rho * sa * sb
ok(close(hr(0.8, 2, 1.6), 1.0) and close(A(S11[2]), hr(0.9, 3, 2)) and close(A(S11[3]), resid(0.8, 2)) and close(var_h(2, 0.8, 2, 1.6), 4), 'l11 s1 to s3 ratio 1.0, 1.35; residual 1.2; h = 2 leaves 2%')
# Monte Carlo: the variance-minimising h on simulated correlated moves is rho sa/sb, not rho and not sa/sb
rng = random.Random(11); xs = []
for _ in range(200000):
    z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1); xs.append((2 * z1, 1.6 * (0.8 * z1 + 0.6 * z2)))
sab = sum(a * b for a, b in xs) / len(xs); sbb = sum(b * b for a, b in xs) / len(xs); saa = sum(a * a for a, b in xs) / len(xs)
h_mc = sab / sbb; sd_at = lambda h: math.sqrt(saa + h * h * sbb - 2 * h * sab)
ok(abs(h_mc - 1.0) < 0.01 and abs(sd_at(1.0) - 1.2) < 0.01 and sd_at(0.8) > sd_at(1.0) < sd_at(1.25) and abs(sd_at(2.0) - 2.0) < 0.02, 'l11 Monte Carlo: least-variance h %.3f, residual sd %.3f; 0.8 and 1.25 are both worse' % (h_mc, sd_at(1.0)))
w = S11[4]['widget']; res = play(w, w['strategy'])
ok(res['v']['ok'] and res['pos'] == -2 and close(res['cash'], 20) and sorted((s, p) for _, s, n, p in fills(res) for _ in range(n)) == [('buy', 6)] * 2 + [('sell', 8)] * 4 and res['v']['pnl'] == 6, 'l11 s4 model run: bought 2 at 6, sold 4 at 8, short 2, cash +20, +6')
# sum of two dice hedged with the first die: slope 1, residual sd is one die
rolls = list(product(range(1, 7), repeat=2))
cov = sum((a + b - 7) * (a - 3.5) for a, b in rolls) / 36; v1 = sum((a - 3.5) ** 2 for a, b in rolls) / 36
ok(close(cov / v1, 1) and abs(math.sqrt(35 / 6) - 2.4152) < 1e-4 and abs(math.sqrt(35 / 12) - 1.7078) < 1e-4, 'l11 s5 hedge ratio of the sum on die 1 is 1; sds 2.4152 and 1.7078')
ok(close(A(S11[6]), 6 + 2 * (3 - 3.6)) and close(20 - 2 * 3.6 - 2 * 4, 4.8) and abs(2 * math.sqrt(35 / 6) - 4.83) < 0.005 and abs(2 * math.sqrt(35 / 12) - 3.42) < 0.005, 'l11 s6 hedged total 4.80; sd 4.83 to 3.42')
ok(close(hr(0.8, 2, 4) * 10000, 4000) and close(resid(0.8, 2), 1.2) and abs(math.sqrt(var_h(1, 0.8, 2, 4)) - 2.68) < 0.005, 'l11 s7 sell 4,000; pound for pound raises the sd to 2.68%')
ok(A(S11[8]) == 0, 'l11 s8 zero correlation, zero hedge')
code(S11[9]['widget'], 'l11 s9')
ok(close(A(S11[10]), hr(0.7, 2.5, 1.4) * 50000) and abs(resid(0.7, 2.5) - 1.79) < 0.005, 'l11 s10 62,500 and 1.79%')
q = l11['quiz']
ok(A(q[0]) == 10 * 100 * 0.6 and close(A(q[1]), resid(0.6, 5)) and close(A(q[2]), 3 * 0.2) and close(var_h(2, 0.8, 2, 1.6), 4), 'l11 quiz keys')

# ---------- l12 ----------
ok(A(S12[1]) == 6 + 2 * 3.5 and A(S12[2]) == (12 - 24) + 1 * 13 and A(S12[7]) == 10.5 - 0.5 * 2, 'l12 s1 s2 s7 keys')
c = 13 - 0.25 * (-2); ok('12.5 at 14.5' in S12[6]['widget']['options'][0]['text'] and (c - 1, c + 1) == (12.5, 14.5), 'l12 s6 interrupted: 12.5 at 14.5')
ok(abs(math.sqrt(35 / 6) - 2.4) < 0.05 and abs(math.sqrt(35 / 4) - 3) < 0.05, 'l12 sds quoted aloud: two dice 2.4, three dice about 3')
code(S12[8]['widget'], 'l12 s8')
ok(close(l12['quiz'][1]['widget']['answer'], card_fair([10], 3), 5e-5) and 3 * (8 - 7) == 3, 'l12 quiz card fair 23.88; +3 after selling 3 at 8')

# ---------- l13 ----------
ok(A(S13[0]) == 21 + 0.5 - 2, 'l13 s0 bid 19.5 on turn 2')
w = S13[1]['widget']
ok(close(w['schedule'][1]['fair'], card_fair([4], 3), 1e-4) and close(w['schedule'][2]['fair'], card_fair([4, 6], 3), 1e-9) and w['value'] == 4 + 6 + 5, 'l13 s1 scheduled fair values 18.1176 and 17.08; settles at 15')
quotes, res = rule_run(w, 0.5, 4)
ok(quotes == [{'bid': s['bid'], 'ask': s['ask'], 'size': 1} for s in w['strategy']], 'l13 s1 the model strategy is exactly the stated rule (width 4, skew 0.5 a lot, centre rounded to 0.5), using only past information')
ok(fills(res) == [(1, 'sell', 1, 23), (4, 'sell', 1, 20.5), (6, 'buy', 1, 16)] and res['v']['pnl'] == 12.5 and res['pos'] == -1 and close(res['cash'], 27.5), 'l13 model run: sold at 23 and 20.5, bought at 16; short 1, cash 27.50, +12.50')
stale = play(w, [{'bid': 19, 'ask': 23, 'size': 1}] * 8)
ok(fills(stale) == [(1, 'sell', 1, 23), (3, 'buy', 1, 19), (6, 'buy', 1, 19)] and stale['v']['pnl'] == 0 and stale['pos'] == 1, 'l13 stale run: sold at 23, bought twice at 19; long 1, 0.00')
_, nosk = rule_run(w, 0.5, 4, skewed=False)
ok(fills(nosk) == [(1, 'sell', 1, 23), (4, 'sell', 1, 20)] and nosk['v']['pnl'] == 13 and nosk['pos'] == -2, 'l13 s5 no-skew run: sold at 23 and 20; short 2, +13.00')
ok(close(A(S13[2]), card_fair([4], 3), 5e-5) and close(A(S13[3]), card_fair([4, 6], 3)) and A(S13[6]) == 27.5 - 23 and A(S13[8]) == 8 - 4 - 4, 'l13 s2 s3 s6 s8 keys')
ok(nosk['cash'] - 2 * 23 == -3 and (13 - (-3)) == 16 and (12.5 - 4.5) == 8, 'l13 s5 a king costs the no-skew run 16 and the model 8')
code(S13[9]['widget'], 'l13 s9')
ok(A(S13[10]) == round(100 * 0.20 + 60 * 0.10 - 40 * 0.30, 9) and -100 + 60 + 40 == 0, 'l13 s10 desk review +14, flat')
q = l13['quiz']
ok(A(q[1]) == 27.5 - 22 and close(17.08 - 16, 1.08), 'l13 quiz queen +5.50; edge 1.08 on the turn 6 buy')

# ---------- review-3 ----------
it = r3['items']
w = it[0]['widget']; res = play(w, w['strategy'])
ok(res['v']['ok'] and res['v']['pnl'] == 2 and res['pos'] == -1 and close(res['cash'], 10) and sorted((s, p) for _, s, n, p in fills(res) for _ in range(n)) == [('buy', 6), ('sell', 8), ('sell', 8)] and fills(res)[-1][0] == 8, 'review-3 limit game: sold 2 at 8, bought 1 at 6 on turn 8, +2')
ok(A(it[1]) == 3 + 2 and A(it[2]) == 0.1 * 400 and abs(g(0.4) + 0.0024) < 5e-5 and close(A(it[4]), hr(0.6, 3, 1.5)) and abs(A(it[5]) - resid(0.9, 2)) < 0.005, 'review-3 items 1 to 5')
ok(A(it[7]) == 2 * (23 - 17) + (17 - 19) and abs(A(it[8]) - float(card_fair([2], 3))) < 0.005, 'review-3 items 7 and 8')

# ---------- homework-3 ----------
it = h3['items']
code(it[0]['widget'], 'homework-3 full_game')
ok(sum('make_script' in t['call'] for t in it[0]['widget']['tests']) == 4 and 'four seeded scripts' in it[0]['prose'], 'homework-3 full_game: four seeded scripts, as the prose says')
code(it[1]['widget'], 'homework-3 kelly_game')
ok(abs(100 * 1.2 ** 31 * 0.8 ** 19 - 410.51) < 0.005 and abs(100 * 1.2 ** 27 * 0.8 ** 23 - 81.09) < 0.005 and abs(100 * 1.4 ** 30 * 0.6 ** 20 - 88.48) < 0.005 and abs(100 * 1.1 ** 30 * 0.9 ** 20 - 212.14) < 0.005, 'homework-3 Kelly paths: 31 wins 410.51, 27 wins 81.09; medians 88.48 and 212.14')
m = it[3]['model']; f1, f2 = float(card_fair([4], 3)), float(card_fair([4, 6], 3))
led = [23 - 21, 23 - f1, 43.5 - 2 * f1, 43.5 - 2 * f2, 27.5 - f2, 27.5 - 15]
ok(all(abs(a - b) < 0.006 for a, b in zip(led, [2, 4.88, 7.26, 9.34, 10.42, 12.5])) and all(s in m for s in ['£4.88', '£7.26', '£9.34', '£10.42', '+£12.50']), 'homework-3 narrated ledger +2, +4.88, +7.26, +9.34, +10.42, +12.50')
w = it[4]['widget']
ok(close(w['schedule'][1]['fair'], card_fair([8], 3), 1e-4) and close(w['schedule'][2]['fair'], card_fair([8, 11], 3)) and w['value'] == 8 + 11 + 11, 'homework-3 mock game fair values 21.96 and 25.9; settles at 30')
quotes, res = rule_run(w, 0.5, 4)
ok(quotes == [{'bid': s['bid'], 'ask': s['ask'], 'size': 1} for s in w['strategy']], 'homework-3 mock game: the model strategy is the stated rule, using only past information')
ok(fills(res) == [(1, 'buy', 1, 19), (5, 'buy', 1, 19.5), (7, 'sell', 1, 27)] and res['v']['pnl'] == 18.5 and close(res['cash'], -11.5), 'homework-3 mock model: bought at 19 and 19.5, sold at 27; +18.50')
stale = play(w, [{'bid': 19, 'ask': 23, 'size': 1}] * 8); _, nosk = rule_run(w, 0.5, 4, skewed=False)
ok(stale['v']['pnl'] == -3 and [f[1:] for f in fills(stale)][1:] == [('sell', 1, 23), ('sell', 1, 23)] and nosk['v']['pnl'] == 21 and nosk['pos'] == 2, 'homework-3 mock: stale -3 (sold twice at 23); no skew +21 long 2')
f1, f2 = float(card_fair([8], 3)), float(card_fair([8, 11], 3))
ok(all(abs(a - b) < 0.006 for a, b in zip([f1 - 19, 2 * f1 - 38.5, 2 * f2 - 38.5, f2 - 11.5, 30 - 11.5], [2.96, 5.42, 13.30, 14.40, 18.5])) and (30 - 19, 30 - 19.5, 27 - 30) == (11, 10.5, -3) and close((0.6 - 0.4) * 100, 20) and close(20 * (0.6 - 0.4), 4), 'homework-3 mock narration ledger, per-trade P&L and the Kelly side bet')
ok(close(A(it[6]), 21) and close(A(it[7]), f1, 5e-5) and close(A(it[8]), f2) and A(it[9]) == 18.5 and abs(A(it[10]) - 81 / 202) < 0.0005, 'homework-3 items 6 to 10')
# coin and dice round (h-coin-dice-aloud): exact fair values, variances and the ledger
def dice_dist(n):
    d = {}
    for r in product(range(1, 7), repeat=n): d[sum(r)] = d.get(sum(r), 0) + F(1, 6 ** n)
    return d
def mix(parts):
    mean = sum(p * sum(k * v for k, v in d.items()) for p, d in parts)
    return mean, sum(p * sum(v * (k - mean) ** 2 for k, v in d.items()) for p, d in parts)
m0, v0 = mix([(F(1, 2), dice_dist(2)), (F(1, 2), dice_dist(4))])
m1, v1 = mix([(F(1, 2), dice_dist(1)), (F(1, 2), dice_dist(3))])
ok(m0 == F(21, 2) and v0 == 21 and 6 + m1 == 13 and abs(float(v1) - 18.08) < 0.005 and 6 + F(7, 2) == F(19, 2), 'homework-3 coin and dice: fair 10.5, 13, 9.5; variances 21 and 18.08')
ok(abs(math.sqrt(21) - 4.58) < 0.005 and abs(math.sqrt(float(v1)) - 4.25) < 0.005 and 3.5 > math.sqrt(35 / 3) and F(49, 4) + (F(35, 6) + F(35, 3)) / 2 == 21, 'homework-3 coin and dice: sds 4.58 and 4.25; the coin swing 3.5 exceeds four dice\'s sd 3.42; 12.25 of the 21 is the coin')
cash, pos, marks = 0, 0, []
for (dq, price, fair) in [(-1, 13, 10.5), (0, 0, 13), (2, 11.5, 13), (0, 0, 9.5), (-1, 10, 9.5), (0, 0, 8)]:
    cash -= dq * price; pos += dq; marks.append(cash + pos * fair)
ok(marks == [2.5, 0, 3, -0.5, 0, 0] and (13 - 10.5) + 2 * (13 - 11.5) + (10 - 9.5) == 6, 'homework-3 coin and dice ledger +2.50, 0, +3, -0.50, 0 and 6 of edge')
# the first die carries no news about the coin: P(heads | first die = 6) = 1/2, by Monte Carlo
rng = random.Random(311); hs = n6 = 0
for _ in range(300000):
    heads = rng.random() < 0.5; dice = [rng.randint(1, 6) for _ in range(2 if heads else 4)]
    if dice[0] == 6: n6 += 1; hs += heads
ok(abs(hs / n6 - 0.5) < 0.01, 'homework-3 coin and dice: P(heads | first die 6) = %.3f, so fair after the 6 is 6 + (3.5 + 10.5)/2' % (hs / n6))

for nline in notes: print('NOTE', nline)
print('mm-games L3 concepts r2: %d checks, %d failed' % (count, len(fails)))
sys.exit(1 if fails else 0)
