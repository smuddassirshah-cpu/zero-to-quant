"""topic-0.1, number-sense level 4 items (Option B, skill ns-measures): every new key computed twice, every wrong value checked.

Run: <scratchpad>/venv/bin/python docs/reports/exam-0.1-holes-numbers.py   (exit 0 when all pass)
Route 1 is the working the item's explanation prints; route 2 is independent (brute force, enumeration, another formula).
The script then reads app/content/exams/topic-0.1.json and checks the key, each wrong value (the named slip, outside the
key's band), that the explanation states the key (numbers_lib._numbers) and the difficulty ramp.
"""
import json, math, os, sys
from fractions import Fraction as F
from itertools import combinations_with_replacement

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', 'app', 'content', 'exams', 'topic-0.1.json')
doc = json.load(open(EXAM, encoding='utf8'))
items = {i['id']: i for i in doc['items']}
fails, n = [], [0]


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def band(t):
    return t.get('abs', 0) if isinstance(t, dict) else t


def numeric(iid, key, wrongs):
    """key: the computed key; wrongs: {id: computed slip value}."""
    w = items[iid]['widget']
    a, t = w['answer'], band(w['tol'])
    check(abs(a - key) <= max(t, 1e-9), f'{iid} key {a} = computed {key}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{iid} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(abs(x['value'] - v) <= band(x['tol']) + 1e-9, f'{iid} wrong {k} {x["value"]} = slip {v}')
        check(abs(x['value'] - a) > t + band(x['tol']), f'{iid} wrong {k} outside the key band')
        check(k in items[iid]['feedback']['byKey'], f'{iid} wrong {k} has a byKey line')
    txt = items[iid]['explain']['text']
    check(any(abs(x - a) <= max(t, 1e-9) for x in _numbers(txt)), f'{iid} explanation states the key')


# e-feed-updates: 15 updates a second for 6.5 hours
r1 = 15 * 60 * 60 * 6.5
r2 = sum(15 for _ in range(int(6.5 * 3600)))                     # count second by second
check(r1 == r2 == 351000, 'e-feed-updates 351,000 both routes')
numeric('e-feed-updates', r1, {'minutes-only': 15 * 60 * 6.5, 'hours-only': 15 * 6.5, 'six-hours': 15 * 3600 * 6,
                                'six-fifty': 15 * (6 * 3600 + 50 * 60)})
check(15 * (6 * 3600 + 50 * 60) == 369000 and sum(15 for _ in range(6 * 3600 + 50 * 60)) == 369000, 'e-feed-updates six-fifty slip 369,000 both routes')

# e-prime-table: trial division up to the root, against a sieve
def prime_trial(m):
    return m > 1 and all(m % p for p in range(2, math.isqrt(m) + 1))
sieve = [True] * 200; sieve[0] = sieve[1] = False
for i in range(2, 200):
    if sieve[i]:
        for j in range(i * i, 200, i):
            sieve[j] = False
opts = {o['text']: o.get('correct', False) for o in items['e-prime-table']['widget']['options']}
for t, c in opts.items():
    m = int(t)
    check(prime_trial(m) == sieve[m] == c, f'e-prime-table {m} prime={c} (trial and sieve agree)')
check(all(math.isqrt(int(t)) < 13 for t in opts), 'e-prime-table every root under 13')
for m, (p, q) in {119: (7, 17), 133: (7, 19), 143: (11, 13), 161: (7, 23)}.items():
    check(p * q == m and min(d for d in range(2, m) if m % d == 0) == p, f'e-prime-table {m} = {p} x {q}, smallest factor {p}')
check(sum(map(int, '119')) == 11, 'e-prime-table digits of 119 add to 11')

# e-plan-hall: sides scaled by 2, against the plan area times 2^2
r1 = (9 * 2) * (6.5 * 2)
r2 = (9 * 6.5) * 2 ** 2
check(r1 == r2 == 234, 'e-plan-hall 234 both routes')
numeric('e-plan-hall', r1, {'scale-once': 9 * 6.5 * 2, 'plan-area': 9 * 6.5, 'perimeter': 2 * (18 + 13)})

# e-pit-area: r = C / 2pi then pi r^2, against C^2 / 4pi; rounding with 3.14 and 22/7
C = 50
r1 = math.pi * (C / (2 * math.pi)) ** 2
r2 = C ** 2 / (4 * math.pi)
check(abs(r1 - r2) < 1e-9 and round(r1) == 199 and abs(r1 - 625 / math.pi) < 1e-9, f'e-pit-area {r1:.4f} both routes, 625/pi')
for pi_ in (3.14, F(22, 7)):
    v = float(pi_ * (C / (2 * pi_)) ** 2)
    check(round(v) == 199, f'e-pit-area with pi = {pi_}: {v:.3f} rounds to 199')
check(abs(C / (2 * math.pi) - 7.958) < 0.0005, 'e-pit-area radius 7.958')
check(abs(C / math.pi - 15.92) < 0.005, 'e-pit-area diameter 15.92')
numeric('e-pit-area', round(r1), {'diameter-as-radius': round(math.pi * (C / math.pi) ** 2),
                                   'half-round': round(math.pi * (C / 2) ** 2), 'edge-as-radius': round(math.pi * C ** 2),
                                   'rounded-radius': round(math.pi * round(C / (2 * math.pi)) ** 2)})
# rounded-radius: r rounded to 8 before squaring; second route with 3.14 and 22/7, all inside the 201 +- 0.5 band
check(round(math.pi * 64) == 201 and abs(3.14 * 64 - 201) <= 0.5 and abs(float(F(22, 7) * 64) - 201) <= 0.5,
      'e-pit-area rounded-radius slip 201 (pi, 3.14, 22/7 all inside the band)')
for key in ('e-plan-hall', 'e-pit-area'):
    check(items[key]['widget'].get('unit') == 'm²' and items[key]['widget']['placeholder'] == 'a number', f'{key} unit m² and placeholder a number')
check(items['e-five-counts']['title'] == 'Four summaries, five days', 'e-five-counts title says summaries (the range is not an average)')

# e-partner-number: HCF x LCM / 24, against a search over 1..2000
r1 = 8 * 168 // 24
r2 = [b for b in range(1, 2001) if math.gcd(24, b) == 8 and 24 * b // math.gcd(24, b) == 168]
check(r1 == 56 and r2 == [56], f'e-partner-number 56 both routes, unique ({r2})')
check(math.gcd(24, 24 * 8) == 24, 'e-partner-number slip 192 has HCF 24 with 24')
numeric('e-partner-number', r1, {'no-divide': 8 * 168, 'lcm-over': 168 / 24, 'times-hcf': 24 * 8})

# e-five-counts: the working, against every sorted 5-tuple of whole numbers 0..40
sols = []
for t in combinations_with_replacement(range(41), 5):
    if sum(t) == 40 and t[2] == 9 and t[4] - t[0] == 7:
        cnt = {v: t.count(v) for v in t}
        top = max(cnt.values())
        if [v for v in cnt if cnt[v] == top] == [10]:
            sols.append(t)
check(sols == [(3, 8, 9, 10, 10)], f'e-five-counts unique solution {sols}')
r1 = 10 - 7
check(r1 == sols[0][0] == 3 and 40 - 3 - 9 - 10 - 10 == 8, 'e-five-counts smallest 3 both routes, last count 8')
numeric('e-five-counts', r1, {'median-minus-range': 9 - 7, 'two-smallest': 40 - 9 - 20, 'second': 8})

# exam shape: ramp and skill coverage
cnt = {d: sum(1 for i in doc['items'] if i['difficulty'] == d) for d in (2, 3, 4, 5)}
N = len(doc['items'])
for d, s in {2: .2, 3: .5, 4: .2, 5: .1}.items():
    check(abs(cnt[d] / N - s) <= 0.1 + 1e-9, f'ramp d{d} {cnt[d]}/{N}')
check(N <= 30, f'{N} items, at most 30')
used = {s for i in doc['items'] for s in i.get('skills', [])}
check(set(doc['skills']) <= used, 'every exam skill covered')
lv4 = ['e-feed-updates', 'e-prime-table', 'e-plan-hall', 'e-pit-area', 'e-partner-number', 'e-five-counts']
check(sum(1 for i in lv4 if 'ns-measures' in items[i]['skills']) >= 1, 'ns-measures examined')

print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
