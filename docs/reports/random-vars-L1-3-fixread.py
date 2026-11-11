#!/usr/bin/env python3
"""Fix-pass read, random-vars levels 1 to 3 (round 1).

Recomputes, with exact fractions, every number behind the 16 strings changed in
commit d67c2d45, and checks that each changed string is still in the content.
Run from the repo root with no arguments. Exits 0 when all checks hold.
"""
import json
import math
import sys
from fractions import Fraction as F
from itertools import product

BASE = 'app/content/courses/random-vars/'
fails = []


def check(name, cond):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


def load(name):
    with open(BASE + name + '.json', encoding='utf-8') as fh:
        return json.load(fh)


def E(pmf, g=lambda v: v):
    return sum(p * g(v) for v, p in pmf)


die = [(F(k), F(1, 6)) for k in range(1, 7)]
EX = E(die)
EX2 = E(die, lambda v: v * v)
VX = EX2 - EX ** 2

# ---- l3: VaR as the smallest x with F(x) >= 0.95
l3 = load('l3-up-to-a-point')
s = l3['screens'][10]
check('l3 changed prose present', 'On at least 95% of days the loss is at most this.' in s['prose'])
rows = [(F(r[0].replace('−', '-')), F(r[1])) for r in s['canvas']['params']['rows']]
check('l3 pmf sums to 1', sum(p for _, p in rows) == 1)
cum, var = F(0), None
for x, p in rows:
    cum += p
    if var is None and cum >= F(95, 100):
        var, f_at = x, cum
check('l3 VaR is 5 and is the key', var == 5 and s['widget']['answer'] == 5)
check('l3 F(VaR) = 0.96, so "at least 95%" is true and plain "95%" was not', f_at == F(96, 100))

# ---- l4: call payoff pmf
l4 = load('l4-transforming')
check('l4 changed explain present', 'pays something with chance only 0.39' in l4['screens'][7]['explain']['text'])
prices = [(96, F(4, 100)), (98, F(20, 100)), (100, F(37, 100)), (102, F(30, 100)), (104, F(9, 100))]
check('l4 price pmf sums to 1', sum(p for _, p in prices) == 1)
p0 = sum(p for k, p in prices if max(k - 100, 0) == 0)
check('l4 P(C = 0) = 0.61 and P(C > 0) = 0.39', p0 == F(61, 100) and 1 - p0 == F(39, 100))

# ---- l5: expected daily P&L and the 250-day total
l5 = load('l5-long-run-average')
check('l5 changed explain present', 'the expected total is £50' in l5['screens'][9]['explain']['text'])
pnl = [(F(2), F(3, 10)), (F(0), F(5, 10)), (F(-2), F(2, 10))]
check('l5 E = 0.2 and 250 E = 50 exactly', E(pnl) == F(1, 5) and 250 * E(pnl) == 50)

# ---- l6: changed key text; only one option flagged correct
l6 = load('l6-fair-price')
opts = l6['quiz'][3]['widget']['options']
check('l6 changed key present', opts[0]['text'].endswith('your average profit per bet settles near £0'))
check('l6 exactly one option keyed correct', [o.get('correct', False) for o in opts] == [True, False, False])
# The old wording ("roughly break even") fails for totals; the new one holds for averages:
# a fair +-1 bet has sd(total) = sqrt(n) and sd(average) = 1/sqrt(n).
n = 10000
check('l6 average settles (sd 0.01) while total wanders (sd 100)',
      math.isclose(1 / math.sqrt(n), 0.01) and math.isclose(math.sqrt(n), 100))

# ---- l7: product rule statements
l7 = load('l7-linearity')
t2 = l7['screens'][2]['explain']['text']
check('l7 s2 changed explain present', 'because the dice are independent; the next screens show the rule holds without that' in t2)
# Row k of the independent grid averages k + 3.5 (E[Y | X = k] = E[Y]).
check('l7 s2 rows average k + 3.5 under independence',
      all(sum(F(k + y, 6) for y in range(1, 7)) == k + F(7, 2) for k in range(1, 7)))
# Under full dependence (Y = X) "row" k averages 2k, not k + 3.5, yet E[X + X] is still 7.
check('l7 s2/s3 dependent rows are 2k, mean of sum still 7',
      [2 * k for k in range(1, 7)] != [k + F(7, 2) for k in range(1, 7)] and E(die, lambda v: 2 * v) == 7)
check('l7 s6 changed explain present', 'can fail without independence' in l7['screens'][6]['explain']['text'])
check('l7 s6 E[X^2] = 91/6 > 12.25', EX2 == F(91, 6) and EX ** 2 == F(49, 4) and EX2 > EX ** 2)
check('l7 s7 changed why present',
      l7['screens'][7]['widget']['options'][3]['why'].startswith('This holds for independent variables but can fail otherwise.'))
# Independent dice: E[XY] = E[X]E[Y] exactly.
exy_ind = sum(F(x * y, 36) for x, y in product(range(1, 7), repeat=2))
check('l7 s7 product rule holds for two independent dice', exy_ind == EX * EX)
q = l7['quiz'][2]
check('l7 quiz changed strings present',
      'safe for independent variables' in q['feedback']['byKey']['product']
      and 'without it the rule can fail, as it does here' in q['explain']['text'])
coin = [(F(1), F(1, 2)), (F(0), F(1, 2))]
check('l7 quiz E[X.X] = 0.5, E[X]^2 = 0.25, cov 0.25',
      E(coin, lambda v: v * v) == F(1, 2) and E(coin) ** 2 == F(1, 4)
      and q['widget']['answer'] == 0.5 and q['widget']['wrong'][0]['value'] == 0.25)

# ---- homework-2: Y = 7 - X
hw = load('homework-2')
it = hw['items'][6]
check('hw2 changed feedback present', 'a high $X$ always comes with a low $Y$' in it['feedback']['byKey']['product'])
exy = E(die, lambda v: v * (7 - v))
ey = E(die, lambda v: 7 - v)
check('hw2 E[XY] = 28/3, E[X]E[Y] = 12.25, Cov = -35/12',
      exy == F(28, 3) and EX * ey == F(49, 4) and exy - EX * ey == -VX == F(-35, 12))
check('hw2 key and slip values match', abs(it['widget']['answer'] - 28 / 3) < 0.002 and it['widget']['wrong'][0]['value'] == 12.25)

# ---- both directions: dependent yet uncorrelated (so "needs independence" would be false)
tri = [(F(-1), F(1, 3)), (F(0), F(1, 3)), (F(1), F(1, 3))]
cov = E(tri, lambda v: v * v * v) - E(tri) * E(tri, lambda v: v * v)
var_sum = E(tri, lambda v: (v + v * v) ** 2) - E(tri, lambda v: v + v * v) ** 2
var_x = E(tri, lambda v: v * v) - E(tri) ** 2
var_y = E(tri, lambda v: v ** 4) - E(tri, lambda v: v * v) ** 2
check('dependent Y = X^2 has Cov 0, E[XY] = E[X]E[Y], and variances add', cov == 0 and var_sum == var_x + var_y)

# ---- l10
l10 = load('l10-scaling-and-adding')
check('l10 s6 changed explain present', 'sds add only when the two move in lockstep' in l10['screens'][6]['explain']['text'])
check('l10 Var(2X) = 35/3, Var(X + Y) = 35/6', 4 * VX == F(35, 3) and 2 * VX == F(35, 6))
# sd(X + Y) = sd X + sd Y exactly when rho = 1 (both sds positive).
sx, sy = 1.708, 2.3


def sd_sum(rho):
    return math.sqrt(sx * sx + sy * sy + 2 * rho * sx * sy)


check('l10 sds add at rho = 1 and at no smaller rho',
      math.isclose(sd_sum(1), sx + sy) and all(sd_sum(r / 100) < sx + sy - 1e-9 for r in range(-100, 100)))
check('l10 s9 changed explain present', 'which is exact for log returns' in l10['screens'][9]['explain']['text'])
check('l10 annual vol 0.1905 and variance 0.0363',
      round(0.012 * math.sqrt(252), 4) == 0.1905 and round(252 * 0.012 ** 2, 4) == 0.0363)
# Log returns add exactly; simple returns compound.
r = [0.012, -0.02, 0.005]
gross = math.prod(1 + v for v in r)
check('l10 log returns add exactly, simple returns do not',
      math.isclose(sum(math.log(1 + v) for v in r), math.log(gross)) and not math.isclose(sum(r), gross - 1, rel_tol=1e-6))
# The sqrt(n) rule needs only uncorrelated, equal-variance days. Example: Y_t = s * e_t,
# with e_t fair +-1 signs and one shared size s in {1, 3} for all days (a crude picture of
# volatility clustering). Days are dependent (|Y_1| = |Y_2|) yet uncorrelated, each with
# variance 5, and the 3-day total has variance exactly 3 x 5.
outs = [(sz * e[0], sz * e[1], sz * e[2]) for sz in (1, 3) for e in product((-1, 1), repeat=3)]
n_o = len(outs)
cov12 = F(sum(o[0] * o[1] for o in outs), n_o)
dep = F(sum(1 for o in outs if abs(o[0]) == 3 and abs(o[1]) == 3), n_o) != F(1, 4)
v1 = F(sum(o[0] ** 2 for o in outs), n_o)
v3 = F(sum(sum(o) ** 2 for o in outs), n_o)
check('l10 dependent but uncorrelated days still give Var(total) = n Var(day)',
      cov12 == 0 and dep and v1 == 5 and v3 == 15)
check('l10 summary strings present',
      'the sd of a total over $n$ independent days grows like $\\sqrt{n}$' in l10['summary']['ideas'][2]
      and l10['summary']['formula']['note'] == 'The second holds when $X$ and $Y$ are independent.')
three = [x + y + z for x, y, z in product(range(1, 7), repeat=3)]
v_three = F(sum(t * t for t in three), 216) - F(sum(three), 216) ** 2
check('l10 three copies give 9 Var(X), three independent dice give 3 Var(X)',
      E(die, lambda v: 9 * v * v) - E(die, lambda v: 3 * v) ** 2 == 9 * VX and v_three == 3 * VX)

# ---- l11: correlation under scale and shift
l11 = load('l11-moving-together')
check('l11 changed strings present',
      'a negative scale flips its sign' in l11['summary']['trap']
      and l11['quiz'][2]['feedback']['correct'] == 'A positive scale and a shift of $Y$ leave $\\rho$ alone.')
joint = {(-1, -1): F(3, 10), (-1, 3): F(2, 10), (2, -1): F(1, 10), (2, 3): F(4, 10)}


def rho(a, b):
    ex = sum(p * x for (x, y), p in joint.items())
    ey_ = sum(p * (a * y + b) for (x, y), p in joint.items())
    c = sum(p * x * (a * y + b) for (x, y), p in joint.items()) - ex * ey_
    vx = sum(p * x * x for (x, y), p in joint.items()) - ex ** 2
    vy = sum(p * (a * y + b) ** 2 for (x, y), p in joint.items()) - ey_ ** 2
    return float(c) / math.sqrt(float(vx) * float(vy))


r0 = rho(1, 0)
check('l11 rho unchanged by 2Y + 0.01 and by 3Y', math.isclose(rho(2, F(1, 100)), r0) and math.isclose(rho(3, 0), r0))
check('l11 rho flips sign under -2Y + 5', math.isclose(rho(-2, 5), -r0) and r0 != 0)

print()
if fails:
    print('%d check(s) failed' % len(fails))
    sys.exit(1)
print('all checks passed')
