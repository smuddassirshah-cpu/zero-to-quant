"""Second read, number-sense problems-1 to -3: the reader's own recompute.
Imports nothing from the author's script. Every key and every wrong[] value is typed here from
the prose and worked by two routes: route 1 exact (fractions.Fraction, Decimal), route 2 another
method (whole-number units, a count, a loop, floats). Then each stored key and wrong value is
compared with mine, the bands are checked (key band takes my value and the value the feedback
prints; no wrong band reaches the key band; no two wrong bands overlap), and the set shape is
checked against docs/briefs/chained.md.

Run from the repo root:  python3 docs/reviews/review-problems-number-sense-1-3-scripts/mine.py
Exit 0 when every check passes."""
import json
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction as F

BASE = 'app/content/courses/number-sense/'
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def same(a, b, label, eps=1e-9):
    ok(abs(float(a) - float(b)) <= eps, f'{label}: route 1 {float(a)!r} against route 2 {float(b)!r}')
    return a


def sig1(x):
    """Round a positive number to 1 significant figure, half up, exactly."""
    d = dec_of(x)
    q = Decimal(1).scaleb(d.adjusted())
    return float((d / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q)


def dec_of(x):
    return Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, F) else Decimal(str(x))


def dp(x, n, mode=ROUND_HALF_UP):
    """Round to n decimal places, half up (or down for a cut-off), exactly."""
    return float(dec_of(x).quantize(Decimal(1).scaleb(-n), rounding=mode))


E = {}  # (set, item) -> list of parts: (key, {wrong id: value}) ; a choice part is ('choice', correct id)

# ---------------------------------------------------------------- set 1
# p-garden-beds: 20 beds, potatoes 2/5, beans 1/4, rest flowers, half the flowers roses
beds = 20
pot = same(F(2, 5) * beds, sum(1 for b in range(beds) if b % 5 < 2), 'garden potatoes')
bean = sum(1 for b in range(beds) if b % 4 < 1)
both = same(F(2, 5) + F(1, 4), F(int(pot) + bean, beds), 'garden both')
flow = same(1 - both, F(beds - int(pot) - bean, beds), 'garden flowers')
rose = same(F(1, 2) * flow, F((beds - int(pot) - bean), 2 * beds), 'garden roses')
ok(rose * beds == F(7, 2), 'garden: roses are three and a half beds')
E[1, 'p-garden-beds'] = [
    (bean, {'flipped': beds * 4, 'three-quarters': F(3, 4) * beds}),
    (both, {'tops-bottoms': F(2 + 1, 5 + 4), 'tops-kept': F(2 + 1, 20)}),
    (flow, {'carried': 1 - F(3, 9), 'beds': beds - pot - bean}),
    (rose, {'doubled': 2 * flow, 'added-half': F(1, 2) + flow, 'carried': F(1, 2) * (1 - F(3, 9))}),
]

# p-rye-loaves: 5/6 kg, 1/5 kg a loaf. Route 2 in units of 1/30 kg: 25 units of flour, 6 a loaf.
fl, lf = F(5, 6), F(1, 5)
n1 = same(fl / lf, F(25, 6), 'rye quotient')
whole = same(math.floor(n1), 25 // 6, 'rye whole loaves')
left = same(fl - whole * lf, F(25 % 6, 30), 'rye left')
share = same(left / fl, F(25 % 6, 25), 'rye share')
ok(n1 == 4 + F(1, 6) and F(1, 6) * lf == left == F(1, 30) and share == F(1, 25), 'rye: 4 1/6, a sixth of a fifth kg is 1/30 kg, share 1/25')
E[1, 'p-rye-loaves'] = [
    (n1, {'multiplied': fl * lf, 'wrong-flip': F(6, 5) * lf}),
    (whole, {'rounded-up': math.ceil(n1), 'carried': math.floor(fl * lf)}),
    (left, {'one-loaf': fl - lf, 'tops-bottoms': F(5 - 4, 6 - 5), 'loaf-sixth': n1 - whole}),
    (share, {'multiplied': left * fl, 'flipped': fl / left, 'carried': (fl - lf) / fl}),
]

# p-two-printers: A 3/8 an hour, B 1/3 an hour. Route 2: a batch of 72 sheets, A 27 an hour, B 24.
a, b = F(3, 8), F(1, 3)
h1 = same(a + b, F(27 + 24, 72), 'printers first hour')
rest = same(1 - h1, F(72 - 51, 72), 'printers rest')
hrs = same(rest / a, F(21, 27), 'printers hours alone')
mins = same(60 + hrs * 60, 60 + 21 / (27 / 60), 'printers minutes')
ok(F(4, 11) < a and rest < F(1, 3) and hrs * 60 == 46 + F(2, 3) and mins == 106 + F(2, 3),
   'printers: 4/11 below 3/8, 7/24 under a third, 46 2/3 and 106 2/3 minutes')
E[1, 'p-two-printers'] = [
    (h1, {'tops-bottoms': F(3 + 1, 8 + 3), 'multiplied': a * b}),
    (rest, {'carried': 1 - F(4, 11), 'count': 7}),
    (hrs, {'multiplied': rest * a, 'flipped': a / rest, 'printer-b': rest / b, 'minutes': hrs * 60}),
    (mins, {'rest-only': hrs * 60, 'hundred': 100 + hrs * 100, 'carried-flipped': 60 + (a / rest) * 60, 'hours': 1 + hrs}),
]

# p-squash-jugs: two jugs of 3/4 litre; cordial 4/9 of A, 5/12 of B. Route 2: units of 1/144 litre (jug 108).
jug, sa, sb = F(3, 4), F(4, 9), F(5, 12)
top = same(sa * 36, 4 * (36 // 9), 'squash thirty-sixths')
ca = same(sa * jug, F(108 * 4 // 9, 144), 'squash cordial A')
cb = same(sb * jug, F(108 * 5 // 12, 144), 'squash cordial B')
tot = same(ca + cb, F(48 + 45, 144), 'squash total')
bowl = same(tot / (2 * jug), F(48 + 45, 216), 'squash bowl share')
ok(cb == F(5, 16) and 2 * jug == F(3, 2) and sb * 36 == 15 and sa > sb and sb < bowl < sa
   and ca < sa and ca < jug and F(6, 19) < ca and sa < F(1, 2) and sb < F(1, 2),
   'squash: 5/16, 3/2, 15/36, A stronger, bowl between, 1/3 below both, 6/19 below 1/3, both under a half')
E[1, 'p-squash-jugs'] = [
    (top, {'top-kept': 4, 'added': 4 + (36 - 9), 'whole-fraction': sa}),
    ('choice', 'a'),
    (ca, {'added': sa + jug, 'divided': sa / jug}),
    (tot, {'tops-bottoms': F(1 + 5, 3 + 16), 'carried': (sa + jug) + cb}),
    (bowl, {'multiplied': tot * F(3, 2), 'shares-added': sa + sb}),
]

# ---------------------------------------------------------------- set 2
# p-moor-weather. Route 2 in whole tenths of a degree.
t6 = F(-36, 10)
t14 = same(t6 + F(49, 10), (-36 + 49) / 10, 'moor 2 pm')
chg = same(-5 - t14, (-50 - 13) / 10, 'moor change')
hours = (23 - 14)
rate = same(chg / hours, (-63 / 9) / 10, 'moor rate')
t3 = same(-5 + 4 * rate, (-50 + 4 * -7) / 10, 'moor 3 am')
ok(hours == 9 and (23 + 4) % 24 == 3, 'moor: 9 hours from 2 pm to 11 pm, and 4 hours on is 3 am')
E[2, 'p-moor-weather'] = [
    (t14, {'subtracted': t6 - F(49, 10), 'start-sign': -t6 + F(49, 10)}),
    (chg, {'sign': -chg, 'added': -5 + t14, 'carried': -5 - (t6 - F(49, 10))}),
    (rate, {'sign': -rate, 'times': chg * 9}),
    (t3, {'sign': -t3, 'minus-minus': -5 - 4 * rate, 'change-only': 4 * rate}),
]

# p-golf-card. Route 2: the 18 holes written out.
holes = [-1] * 4 + [-2] + [1] * 3 + [2] + [0] * 9
r1 = same(4 * -1 + 1 * -2 + 3 * 1 + 1 * 2, sum(holes), 'golf round')
ok(len(holes) == 18 and sum(1 for h in holes if h < 0) == 5
   and sum(h for h in holes if h < 0) == -6 and sum(h for h in holes if h > 0) == 5, 'golf: 18 holes, 5 under par, 6 under and 5 over')
rounds = [r1, 2, -6, -3]
mean = same(F(sum(rounds), 4), sum(rounds) / len(rounds), 'golf mean')
dec = same(dp(F(5, 18), 3), round(5 / 18 + 1e-12, 3), 'golf 5/18 to 3 dp')
digits = []
rem = 5
for _ in range(6):  # long division of 5 by 18
    rem *= 10
    digits.append(rem // 18)
    rem %= 18
ok(digits == [2, 7, 7, 7, 7, 7], 'golf: 5/18 = 0.27777...')
ok(F(28, 100) > F(5, 18) and abs(float(F(28, 100) - F(5, 18)) - 0.002) < 0.0005, 'golf: 0.28 is larger, by about 0.002')
E[2, 'p-golf-card'] = [
    (r1, {'sign': -r1, 'eagle-one': 4 * -1 - 1 + 3 + 2, 'no-signs': sum(abs(h) for h in holes)}),
    (mean, {'sign': -mean, 'plus-as-minus': F(r1 - 2 - 6 - 3, 4), 'total': sum(rounds)}),
    (dec, {'truncated': dp(F(5, 18), 3, ROUND_DOWN), 'flipped': F(18, 5), 'unrounded': F(5, 18)}),
    ('choice', 'rival'),
]

# p-taxi-split. Route 2 in pence.
each = F(17, 6)
s4 = same(dp(each, 4), 2 + round((1700 % 600) / 600, 4), 'taxi 4 dp')
pen = same(dp(each, 2), round(1700 / 6) / 100, 'taxi penny')
short = same((6 * F(283, 100) - 17) * 100, 6 * 283 - 1700, 'taxi shortfall')
sixth = same(17 - 5 * F(283, 100), (1700 - 5 * 283) / 100, 'taxi sixth')
ok(divmod(17, 6) == (2, 5) and divmod(50, 6) == (8, 2) and divmod(20, 6) == (3, 2) and 6 * 283 == 1698
   and 5 * 283 == 1415, 'taxi: 2 r 5, then 8 r 2, then 3 r 2; 1,698 pence; £14.15')
E[2, 'p-taxi-split'] = [
    (s4, {'flipped': dp(F(6, 17), 4), 'remainder': 2.5}),
    (pen, {'rounded-up': 2.84, 'one-dp': dp(each, 1), 'unrounded': 2.8333, 'pence': 283}),
    (short, {'sign': -short, 'pounds': short / 100, 'carried-up': 6 * 284 - 1700}),
    (sixth, {'same': 2.83, 'wrong-way': 2.83 - 0.02, 'shortfall': 0.02, 'pence': 285}),
]

# ---------------------------------------------------------------- set 3
# p-cube-tub. Route 2: loops.
N = 2169
edge = same(max(n for n in range(1, 50) if n ** 3 <= N), math.floor(N ** (1 / 3) + 1e-9), 'cube edge')
over = same(N - edge ** 3, N - edge * edge * edge, 'cube left over')
side = same(math.isqrt(int(over)), over ** 0.5, 'cube square side')
ok(12 ** 3 == 1728 and 13 ** 3 == 2197 and 12 * 12 == 144 and 144 * 12 == 1728 and side ** 2 == over == 441
   and 20 ** 2 == 400 and 22 ** 2 == 484, 'cube: 1,728, 2,197, 144, 21 squared is 441, 400 and 484')
E[3, 'p-cube-tub'] = [
    (edge, {'rounded-up': edge + 1, 'square-root': math.sqrt(N), 'thirds': N / 3}),
    (over, {'squared': N - edge ** 2, 'carried-up': N - (edge + 1) ** 3, 'times-three': N - edge * 3}),
    (side, {'halved': over / 2, 'quartered': over / 4}),
]

# p-stationery-bill. Route 2 in pence.
est = same(sig1(38) * sig1(4.85) + sig1(19.50), 40 * 5 + 20, 'bill estimate')
bill = same(38 * F(485, 100) + F(1950, 100), (38 * 485 + 1950) / 100, 'bill exact')
calc = same(38 * F(485, 100) + F(1950, 100) / 3, (38 * 485 + 1950 // 3) / 100, 'bill calculator')
shr = same(dp(bill / 3, 2), round((38 * 485 + 1950) / 3) / 100, 'bill share')
ok(38 * 485 == 18430 and 1950 / 3 == 650 and abs(220 / 3 - 73) < 0.5 and str(float(bill) / 3)[:7] == '67.9333',
   'bill: 184.30, 6.50, 220/3 about 73, 67.9333...')
E[3, 'p-stationery-bill'] = [
    (est, {'bracket-first': 40 * (5 + 20), 'no-delivery': 40 * 5}),
    (bill, {'bracket': 38 * (F(485, 100) + F(1950, 100)), 'boxes-only': 38 * F(485, 100)}),
    (calc, {'intended': shr, 'delivery-share': F(1950, 100) / 3}),
    (shr, {'calculator': calc, 'carried-bracket': dp(38 * (F(485, 100) + F(1950, 100)) / 3, 2), 'estimate': dp(F(220, 3), 2)}),
]

# p-comet-probe. Route 2 in whole numbers.
hrs_j = same(F(12, 10) * 10 ** 9 / (4 * 10 ** 4), 1_200_000_000 // 40_000, 'comet hours')
year = 24 * 365
y1 = same(sig1(year), round(year, -3), 'comet year to 1 sf')
est_y = same(sig1(hrs_j / F(int(y1))), round(30000 / 9000), 'comet estimate')
yrs = same(dp(hrs_j / year, 1), round(30000 / 8760, 1), 'comet years')
ok(year == 8760 and F(12, 10) / 4 == F(3, 10) and 30000 / 8760 > 30000 / 9000 and str(30000 / 8760)[:4] == '3.42',
   'comet: 8,760, 1.2/4 = 0.3, 3.42...')
E[3, 'p-comet-probe'] = [
    (hrs_j, {'kept-point': 3 * 10 ** 5, 'added-indices': F(3, 10) * 10 ** 13, 'short': 3 * 10 ** 3}),
    (y1, {'truncated': 8000, 'two-sf': 8800}),
    (est_y, {'inverted': 9000 / 30000, 'carried': sig1(30000 / 8000), 'unrounded': 30000 / 9000}),
    (yrs, {'nine-thousand': dp(F(30000, 9000), 1), 'carried': dp(F(300000, 8760), 1), 'days': 30000 / 24}),
]

# ---------------------------------------------------------------- compare with the files
LESSONS = {1: {'l1', 'l2', 'l3', 'l4', 'l5'}, 2: {'l6', 'l7', 'l8', 'l9'}, 3: {'l10', 'l11', 'l12', 'l13', 'l14'}}
course = json.load(open(BASE + 'course.json'))
nparts = nwrong = 0
for n in (1, 2, 3):
    d = json.load(open(f'{BASE}problems-{n}.json'))
    ok(d['id'] == f'problems-{n}' and d['course'] == 'number-sense' and d['level'] == n, f'set {n} header')
    ok(3 <= len(d['items']) <= 5, f'set {n}: 3 to 5 problems')
    ok(any(it['difficulty'] == 5 for it in d['items']) and all(3 <= it['difficulty'] <= 5 for it in d['items']),
       f'set {n}: difficulty 3 to 5 with a 5')
    typed = total = 0
    for it in d['items']:
        mine = E[n, it['id']]
        ok(3 <= len(it['parts']) <= 5 and len(it['parts']) == len(mine), f'{it["id"]}: part count')
        ok(all(s in course['skills'] for s in it['skills']), f'{it["id"]}: skills exist')
        for k, (p, m) in enumerate(zip(it['parts'], mine), 1):
            w, at = p['widget'], f'problems-{n} {it["id"]} part {k}'
            nparts += 1
            total += 1
            sentences = [s for s in re.split(r'(?<=[.?])\s+(?=[A-Z$£0-9])', p['explain']['text'].strip()) if s]
            ok(len(sentences) <= 3, f'{at}: explain has {len(sentences)} sentences')
            for txt in [p['question'], p['explain']['text'], *map(str, p['feedback'].values())]:
                ok('!' not in txt and '—' not in txt, f'{at}: exclamation mark or em-dash')
            if m[0] == 'choice':
                right = [o['id'] for o in w['options'] if o.get('correct')]
                ok(w['kind'] == 'choice' and right == [m[1]], f'{at}: choice key {right} against mine {m[1]}')
                ok(set(p['feedback'].get('byKey', {})) == {o['id'] for o in w['options'] if not o.get('correct')},
                   f'{at}: a byKey line for each distractor')
                continue
            typed += 1
            key, slips = m
            tol = w['tol']['abs']
            ok(abs(w['answer'] - float(key)) <= 1e-6, f'{at}: stored key {w["answer"]} against mine {float(key)}')
            ok(abs(w['answer'] - float(key)) <= tol + 1e-9, f'{at}: band takes my value')
            stored = {x['id']: x for x in w['wrong']}
            ok(set(stored) == set(slips), f'{at}: wrong ids {sorted(stored)} against mine {sorted(slips)}')
            ok(set(p['feedback']['byKey']) == set(stored), f'{at}: byKey lines match wrong ids')
            bands = []
            for wid, x in stored.items():
                nwrong += 1
                if wid in slips:
                    ok(abs(x['value'] - float(slips[wid])) <= max(x['tol']['abs'], 1e-6) + 1e-9,
                       f'{at}: wrong {wid} stored {x["value"]} against mine {float(slips[wid])}')
                lo, hi = x['value'] - x['tol']['abs'], x['value'] + x['tol']['abs']
                ok(hi < w['answer'] - tol or lo > w['answer'] + tol, f'{at}: wrong {wid} band reaches the key band')
                bands.append((lo, hi, wid))
            bands.sort()
            for (lo1, hi1, i1), (lo2, hi2, i2) in zip(bands, bands[1:]):
                ok(hi1 < lo2, f'{at}: wrong bands {i1} and {i2} overlap')
        ok(typed * 3 >= total * 2, f'{it["id"]}: typed parts at least two thirds')

UNITS = {1: {'p-garden-beds': ['beds', None, None, None], 'p-rye-loaves': [None, 'loaves', 'kg', None],
             'p-two-printers': [None, None, 'hours', 'minutes'], 'p-squash-jugs': [None, None, 'litres', 'litres', None]},
         2: {'p-moor-weather': ['\u00b0C', 'degrees', 'degrees', '\u00b0C'], 'p-golf-card': [None] * 4, 'p-taxi-split': ['\u00a3', '\u00a3', 'p', '\u00a3']},
         3: {'p-cube-tub': ['cubes'] * 3, 'p-stationery-bill': ['\u00a3'] * 4, 'p-comet-probe': ['hours', 'hours', 'years', 'years']}}
for n in (1, 2, 3):
    for it in json.load(open(f'{BASE}problems-{n}.json'))['items']:
        for k, (u, p) in enumerate(zip(UNITS[n][it['id']], it['parts']), 1):
            ok(p['widget'].get('unit') == u, f'problems-{n} {it["id"]} part {k}: unit {p["widget"].get("unit")!r} against {u!r}')
d2 = json.load(open(f'{BASE}problems-2.json'))
ok(d2['items'][1]['parts'][2]['widget']['tol']['abs'] == 0.0001 and d2['items'][2]['parts'][1]['widget']['tol']['abs'] == 0.0005,
   'rounding parts: tol 0.0001 on golf 3 and 0.0005 on taxi 2, so the unrounded value is refused')
ok(nparts == 40, f'40 parts read, found {nparts}')
print(f'mine.py: {checks} checks, {fails} failures; {nparts} parts, {nwrong} wrong values')
sys.exit(1 if fails else 0)
