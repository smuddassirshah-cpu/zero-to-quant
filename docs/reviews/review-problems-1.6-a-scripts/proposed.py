"""Second read, problem sets 1.6 (a): the numbers of the fixes proposed in review-problems-1.6-a.md, and a few listings.
Run from the repo root with the scratchpad venv:  python docs/reviews/review-problems-1.6-a-scripts/proposed.py"""
import json
import math
import re
import sys

import numpy as np

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def band(v, t):
    return (v - t, v + t)


def apart(a, b):
    return a[1] < b[0] or b[1] < a[0]


sq = math.sqrt

# finding 4: robot part 3 at 2 places
key = band(0.9, 0.005)
for v in (0.75, 1, 0.95):
    ok(apart(key, band(v, 0.005)), f'robot part 3: {v} clear of the key band')
ok(not (key[0] <= 0.95 <= key[1]) and not (key[0] <= 0.85 <= key[1]), 'robot part 3: 0.95 and 0.85 now refused')

# finding 5: % parts as unit "%": key and bands divided by 100 (currency part 1 shown)
ok(abs(0.25 / 100 - 0.0025) < 1e-15 and abs(0.2857 / 100 - 0.002857) < 1e-12, 'currency part 1 scaled values')

# finding 9: bands that take the slip worked from the part's own rounded inputs
k3 = band(7.8414, 0.02)
for name, v, t, reach in [('times-52', 56.61, 0.08, [1.0874 * 52, 1.09 * 52]), ('trading-days', 17.28, 0.03, [1.0874 * sq(252), 1.09 * sq(252)]),
                          ('carried', 8.38, 0.02, [1.1625 * sq(52), 1.16 * sq(52)]), ('variance', 61.6, 0.2, [52 * 1.1825, 52 * 1.09 ** 2])]:
    b = band(v, t)
    ok(all(b[0] <= r <= b[1] for r in reach), f'currency part 3 {name}: band {b} takes {reach}')
    ok(apart(b, k3), f'currency part 3 {name}: clear of the key')
k4 = band(0.8165, 0.001)
for name, v, t, reach in [('inverted', 1.2247, 0.0015, [sq(1.5), round(2.08 / 1.70, 3)]), ('squared', 0.6667, 0.0015, [2 / 3, round((1.70 / 2.08) ** 2, 3)])]:
    b = band(v, t)
    ok(all(b[0] <= r <= b[1] for r in reach) and apart(b, k4), f'fund part 4 {name}: band {b} takes {reach}')
b = band(27.62, 0.05)
ok(b[0] <= 27.6 <= b[1] and b[0] <= 0.01 / (0.21 / 580) <= b[1], 'ticket-bot part 4 no-root band takes 27.6')

# finding 10: slips with no line; each new value is clear of the key and of the entries already there
new = [('estimation', 2, 'p-currency-vol', 5, 122, 0), ('estimation', 3, 'p-routing-test', 3, 0.1035, 0.01), ('regression', 1, 'p-car-prices', 4, 1230, 0),
       ('regression', 1, 'p-stopping-distances', 1, 0.6481, 0.005), ('regression', 1, 'p-stopping-distances', 2, 21.4, 0.05), ('regression', 2, 'p-raw-intercept', 4, 105, 0),
       ('regression', 3, 'p-power-price', 4, 113, 0), ('regression', 3, 'p-solar-output', 2, 0.5, 0.005), ('regression', 3, 'p-overlap-signal', 4, 3.5 / sq(5), 0.005),
       ('regression', 3, 'p-bond-fund-weeks', 1, 0.0060, 0.00005)]
for c, n, item, k, v, t in new:
    d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
    w = next(i for i in d['items'] if i['id'] == item)['parts'][k - 1]['widget']
    nb = band(v, t)
    ok(apart(nb, band(w['answer'], w['tol']['abs'])), f'{item} part {k}: new slip {v} clear of the key')
    for x in w['wrong']:
        ok(apart(nb, band(x['value'], x['tol']['abs'])) or (item == 'p-stopping-distances' and x['id'] == 'reverse'), f'{item} part {k}: new slip {v} clear of "{x["id"]}"')
ok(abs(3.5 / sq(5) - 1.5652) < 5e-5, 'overlap: 3.5/sqrt(5) = 1.5652')
# stopping part 1: `reverse` (0.6579) and the new `other-way` (0.6481) need bands that do not meet
ok(apart(band(0.6579, 0.004), band(0.6481, 0.004)), 'stopping part 1: 0.6579 +- 0.004 and 0.6481 +- 0.004 do not meet')
ok(band(0.6481, 0.004)[0] <= 0.65 <= band(0.6481, 0.004)[1] and band(0.6579, 0.004)[0] <= 0.66 <= band(0.6579, 0.004)[1], 'stopping part 1: 0.65 and 0.66 each land on their own line')

# finding 12: new last parts
# ping part 4 at a target of 2 microseconds
ok(math.ceil(110 / 4) == 28 and sq(110 / 28) <= 2 < sq(110 / 27), 'ping part 4: 28 pings, 27 are not enough')
ok(math.ceil(88 / 4) == 22 and 110 / 2 == 55 and abs(sq(110) / 2 - 5.244) < 1e-3, 'ping part 4 slips 22, 55, 5.24')
# reference-mass part 5 as a count of standard errors
se5 = sq(76 / 5)
ok(abs(se5 - 3.899) < 1e-3 and abs(2 / se5 - 0.513) < 5e-4, 'reference-mass part 5: 2 / 3.899 = 0.513')
alts = {'carried-90': 2 / sq(90 / 5), 'carried-72': 2 / sq(72 / 5), 'no-root': 2 / (76 / 5), 'sd-not-se': 2 / sq(76), 'inverted': se5 / 2}
want = {'carried-90': 0.471, 'carried-72': 0.527, 'no-root': 0.132, 'sd-not-se': 0.229, 'inverted': 1.949}
for k_, v in alts.items():
    ok(abs(v - want[k_]) < 6e-4, f'reference-mass part 5 slip {k_} = {v:.4f}')
    ok(apart(band(0.513, 0.005), band(want[k_], 0.005)), f'reference-mass part 5 slip {k_} clear of the key')
# car-prices part 4 as the corrected line's value at 9 years
age = np.array([1, 2, 3, 4, 5, 9.0]); price = np.array([18000, 16600, 15400, 13400, 12400, 8200.0])
b1, a1 = np.polyfit(age, price, 1)
ok(abs(b1 + 1230) < 1e-6 and abs(price.mean() - 14000) < 1e-9 and abs(a1 + 9 * b1 - 7850) < 1e-6, 'car-prices: corrected line gives 7,850 at 9 years, mean price 14,000')
ok(abs(8200 - (a1 + 9 * b1) - 350) < 1e-6, 'car-prices: the corrected car sits 350 above its own line')
ok(14000 - 1480 * 5 == 6600 and 14000 - 1230 * 9 == 2930 and 14000 - 1730 * 5 == 5350 and round(82000 / 6 - 1230 * 5) == 7517, 'car-prices part 4 slips 6600, 2930, 5350, 7517')
# power-price part 4 as a standard error
ok(abs(0.05 / 1.25 - 0.04) < 1e-12 and abs(0.05 / 1.5625 - 0.032) < 1e-12 and abs(0.05 * 1.25 - 0.0625) < 1e-12, 'power-price part 4: 0.04, 0.032, 0.0625')

# listings: placeholders against the form asked, and parts with no form sentence
for c in ('estimation', 'regression'):
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
        for it in d['items']:
            for k, p in enumerate(it['parts'], 1):
                w = p['widget']
                if w['kind'] != 'numeric':
                    continue
                q = p['question']
                ph = w.get('placeholder', '')
                if 'whole number' in q and ph == 'decimal':
                    print(f'LIST placeholder "decimal" on a whole-number part: {c}/problems-{n} {it["id"]} part {k}')
                if not re.search(r'whole number|decimal place|fraction', q):
                    print(f'LIST no form sentence: {c}/problems-{n} {it["id"]} part {k} (placeholder "{ph}", unit "{w.get("unit", "")}")')
                if w['tol']['abs'] >= 0.05 and float(w['answer']) == round(float(w['answer']), 1) and 'unit' not in w:
                    print(f'LIST 1-place key, band +-{w["tol"]["abs"]}: {c}/problems-{n} {it["id"]} part {k} key {w["answer"]}')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
