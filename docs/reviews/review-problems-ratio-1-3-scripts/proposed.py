#!/usr/bin/env python3
"""Second read, ratio problems-1 to -3: the numbers of the proposed fixes, each by two routes.

  python3 docs/reviews/review-problems-ratio-1-3-scripts/proposed.py        (from the repo root)"""
import sys
from fractions import Fraction as Fr

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def same(a, b, msg, tol=1e-9):
    ok(abs(float(a) - float(b)) <= tol, f'{msg}: {float(a)} against {float(b)}')


# finding 3 (p-savings-tax part 4, why "same"): £702 against £696.80, £5.20 apart
kept = Fr(828) - (Fr(828) - 500) * Fr(40, 100)
same(kept, 828 - 0.4 * 328, 'kept after tax')
ok(kept == Fr(69680, 100) and Fr(18000) * Fr(39, 1000) == 702 and 702 - kept == Fr(520, 100), 'gap of 5.20')

# finding 5 (p-phone-rise part 4, a cheaper deal of £14.00 in place of £12.00)
new = Fr(30) * Fr(1071, 1000)
ok(new == Fr(3213, 100), 'new price 32.13')
k = Fr(14) / new
same(k, 14 / 32.13, 'key'); ok(round(float(k), 4) == 0.4357 and round(float(k) * 100, 1) == 43.6, 'key 0.4357, 43.6%')
old = Fr(14, 30); same(old, 14 / 30, 'old-price'); ok(round(float(old), 4) == 0.4667, 'old-price 0.4667')
ud = new / 14; same(ud, 32.13 / 14, 'upside-down'); ok(ud == Fr(2295, 1000), 'upside-down 2.295')
sv = (new - 14) / new; same(sv, 1 - 14 / 32.13, 'saving'); ok(new - 14 == Fr(1813, 100) and round(float(sv), 4) == 0.5643, 'saving 18.13, 0.5643')
ok(min(abs(float(k) - x) for x in (0.4667, 2.295, 0.5643)) > 0.002 + 0.001, 'bands clear of the key')

# finding 8 (p-laptop-sale part 1, new wrong entry off-again)
same(Fr(561) * Fr(85, 100), 561 - 0.15 * 561, 'off-again'); ok(Fr(561) * Fr(85, 100) == Fr(47685, 100), 'off-again 476.85')

# finding 12 (p-partners-profit part 2): 3,200 is both an equal split and 4 parts
ok(Fr(9600, 3) == 3200 == 4 * Fr(9600, 12) and 5 * Fr(9600, 12) == 4000, '3,200 two ways; key 4,000')

# finding 11 (p-partners-profit with stakes of £12,000, £16,000 and £32,000, then a fourth of £8,000)
import math
st = [12000, 16000, 32000]
g = math.gcd(*st)
ok(g == 4000 and [x // g for x in st] == [3, 4, 8] and sum(x // g for x in st) == 15, 'ratio 3:4:8, 15 parts')
ok(sum(x // 1000 for x in st) == 60 and math.gcd(12, 16, 32) == 4 and sum(x // 2000 for x in st) == 30 and math.gcd(6, 8, 16) == 2, 'slips 60 and 30')
part = Fr(9600, 15)
ok(part == 640 and 8 * part == 5120 and Fr(9600) * 32000 / sum(st) == 5120, 'part 2 key 5,120')
ok(Fr(9600, 3) == 3200 and 3200 not in (3 * part, 4 * part, 8 * part), 'equal split 3,200 is no partner\'s share')
ok(Fr(2850, 3) == 950 and 15 * 950 == 14250 and Fr(2850) * sum(st) / 12000 == 14250 and 2850 * 3 == 8550 and 2850 * 15 == 42750, 'part 3: 14,250; slips 8,550 and 42,750')
ok(8000 // g == 2 and Fr(11900, 17) == 700 and 2 * 700 == 1400 and Fr(11900) * 8000 / (sum(st) + 8000) == 1400, 'part 4: 17 parts, 1,400')
ok(round(float(Fr(11900) * 2 / 15), 2) == 1586.67 and Fr(11900, 4) == 2975, 'part 4 slips 1,586.67 and 2,975')

# finding 13 (p-print-run, four presses for 15 hours in place of five for 12)
ph = 4 * 15
ok(ph == 60 and Fr(ph, 8) == Fr(15, 2), 'still 60 press-hours, 7.5 hours with 8 presses')
direct = Fr(15 * 8, 4); same(direct, 15 / 4 * 8, 'direct'); ok(direct == 30, 'direct 30')
ok(15 - 4 == 11, 'subtracted 11 (4 more presses, 4 hours off)')
ok(8 * direct * 14 == 3360 and 8 * 30 * 14 == 3360, 'part 2 carried slip 3,360')
ok(4 * 15 * 14 == 840, 'four presses for 15 hours cost the same 840')
ok(len({7.5, 30, 11}) == 3 and len({840, 3360, 105}) == 3, 'slips distinct from keys')

# finding 1 (p-platform-fee part 4): the slips in whole per cents against the proposed bands
for v, centre, tol in ((Fr(8, 100), Fr(816, 10000), Fr(2, 1000)), (Fr(122, 100), Fr(1225, 1000), Fr(6, 1000)), (Fr(123, 100), Fr(1225, 1000), Fr(6, 1000))):
    ok(abs(v - centre) < tol, f'{float(v)} inside {float(centre)} +- {float(tol)}')
ok(abs(Fr(8163, 10000) - Fr(1225, 1000)) > Fr(16, 1000) and Fr(816, 10000) - Fr(2, 1000) > Fr(29, 10000) + Fr(1, 10000), 'proposed bands touch nothing')

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
