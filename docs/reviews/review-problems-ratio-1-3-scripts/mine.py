#!/usr/bin/env python3
"""Second read, ratio problems-1 to -3: the reader's own keys, slips and stated numbers.
Imports nothing from the author's script. Every figure is typed from the prose of the problem.
Route 1 is exact (fractions.Fraction); route 2 is another method in floats (a percentage built from 10%, 1% and 0.1% blocks,
step-by-step compounding, a change computed from prices rather than multipliers, unit rates taken the other way round).
Each wrong[] value is rebuilt from the slip its feedback line names and must sit inside the stored band and clear of the key's.
CLAIM lines are things the reader holds against the content (findings); they do not fail the script.

  python3 docs/reviews/review-problems-ratio-1-3-scripts/mine.py        (from the repo root)"""
import json, math, re, sys
from fractions import Fraction as Fr

BASE = 'app/content/courses/ratio/'
SETS = {n: json.load(open(f'{BASE}problems-{n}.json')) for n in (1, 2, 3)}
checks = fails = 0
claims = []


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def part(n, item, k):
    it = next(i for i in SETS[n]['items'] if i['id'] == item)
    return it['parts'][k - 1]


def key(n, item, k, exact, route2, wrongs=None, shown=None):
    """exact: Fraction (route 1); route2: float; wrongs: {id: rebuilt value}; shown: the rounded value the part prints."""
    w = part(n, item, k)['widget']
    tag = f'{n}/{item}.{k}'
    a, tol = w['answer'], w.get('tol', {}).get('abs', 0)
    ok(abs(float(exact) - route2) < 1e-9 * max(1, abs(route2)), f'{tag} two routes differ {float(exact)} {route2}')
    ok(abs(a - float(exact)) <= max(tol / 2, 1e-9) + 1e-12, f'{tag} key {a} against {float(exact)}')
    if shown is not None:
        ok(abs(shown - a) <= tol + 1e-12, f'{tag} printed value {shown} outside band of {a} +- {tol}')
    stored = {x['id']: x for x in w.get('wrong', [])}
    ok(set(stored) == set(wrongs or {}), f'{tag} wrong ids {sorted(stored)} against {sorted(wrongs or {})}')
    fb = part(n, item, k)['feedback'].get('byKey', {})
    ok(set(fb) == set(stored), f'{tag} byKey lines {sorted(fb)} against wrong ids {sorted(stored)}')
    for i, v in (wrongs or {}).items():
        if i not in stored:
            continue
        s = stored[i]
        st = s.get('tol', {}).get('abs', 0)
        ok(abs(s['value'] - float(v)) <= max(st, 1e-9) + 1e-12, f'{tag} wrong {i}: stored {s["value"]} rebuilt {float(v)}')
        ok(abs(s['value'] - a) > tol + st, f'{tag} wrong {i} band touches the key band')
    vals = sorted((x['value'], x.get('tol', {}).get('abs', 0), x['id']) for x in w.get('wrong', []))
    for (v1, t1, i1), (v2, t2, i2) in zip(vals, vals[1:]):
        ok(v2 - v1 > t1 + t2, f'{tag} wrong bands {i1} and {i2} touch')


def stored(n, item, k, wid):
    return next(x for x in part(n, item, k)['widget']['wrong'] if x['id'] == wid)


def pc(x):
    return Fr(x) / 100


def pct_build(amount, percent):
    """route 2 for a percentage of an amount: built from 10%, 1%, 0.1% and 0.01% blocks."""
    total, p = 0.0, round(percent * 100)            # in hundredths of a per cent
    for size, block in ((1000, amount / 10), (100, amount / 100), (10, amount / 1000), (1, amount / 10000)):
        q, p = divmod(p, size)
        total += q * block
    return total


# ------------------------------------------------------------------ set 1
# p-pension-split: £9,600, three eighths in shares, shares +15%, bonds -4%
pot = Fr(9600)
sh = Fr(3, 8)
key(1, 'p-pension-split', 1, sh, 3 / 8, {'decimal': sh / 100, 'upside-down': Fr(8, 3)})
shares = sh * pot
bonds = pot - shares
key(1, 'p-pension-split', 2, shares, pct_build(9600, 37.5), {'ten-times': shares * 10, 'tenth': shares / 10, 'bonds': bonds})
ok(pct_build(9600, 1) == 96 and pct_build(9600, 10) == 960 and 37.5 * 96 == 3600, 'pension 1% and 10%')
s2 = shares * Fr(115, 100)
key(1, 'p-pension-split', 3, s2, 3600 + pct_build(3600, 15), {'multiplier-1-5': shares * Fr(3, 2), 'rise-only': shares * pc(15), 'bonds': bonds * Fr(115, 100)})
b2 = bonds * Fr(96, 100)
key(1, 'p-pension-split', 4, b2, 6000 - pct_build(6000, 4), {'rise': bonds * Fr(104, 100), 'fall-only': bonds * pc(4), 'multiplier-0-6': bonds * Fr(6, 10)})
ok(bonds == 6000, 'bonds are 6000')
key(1, 'p-pension-split', 5, s2 / (s2 + b2), 4140 / 9900, {'old-total': s2 / pot, 'unchanged': sh, 'bonds-base': s2 / b2}, shown=0.418)
ok(s2 + b2 == 9900, 'new pot 9900')

# p-platform-fee: 0.35% of £8,400, rival £24
r = Fr(35, 10000)
acc = Fr(8400)
key(1, 'p-platform-fee', 1, r, 0.35 / 100, {'one-place': r * 10, 'no-move': r * 100, 'times-100': Fr(35)})
fee = r * acc
key(1, 'p-platform-fee', 2, fee, pct_build(8400, 0.35), {'one-place': fee * 10, 'no-move': fee * 100, 'half-only': acc * pc(Fr(1, 2))})
ok(pct_build(8400, 0.1) == 8.4 and abs(3 * 8.40 + 4.20 - 29.40) < 1e-9 and abs(pct_build(8400, 0.3) - 25.2) < 1e-9, 'fee blocks')
key(1, 'p-platform-fee', 3, acc * (1 - r), 8400 - 29.40, {'added': acc * (1 + r), 'one-place': acc * (1 - 10 * r), 'fee-only': fee})
slips = {'upside-down': fee / 24, 'account-base': Fr(24) / acc, 'one-place': Fr(24) / (fee * 10)}
key(1, 'p-platform-fee', 4, Fr(24) / fee, 24 / 29.40, slips, shown=0.82)
# each slip in the form the part asks for (nearest whole per cent): is it still inside its own band?
for i, v in slips.items():
    s = stored(1, 'p-platform-fee', 4, i)
    whole = Fr(round(v * 100), 100)
    if abs(whole - Fr(str(s['value']))) >= Fr(str(s['tol']['abs'])):
        claims.append(f'1/p-platform-fee.4: slip {i} is {float(v)*100:.3f}%; as the part asks, {round(v*100)}%, which is outside or on the edge of its band {s["value"]} +- {s["tol"]["abs"]}')

# p-phone-rise: £30.00, inflation 3.2% plus 3.9 points, SIM-only £12.00
rise = pc(Fr(32, 10)) + pc(Fr(39, 10))
key(1, 'p-phone-rise', 1, rise, (3.2 + 3.9) / 100, {'one-place': rise * 10, 'no-move': rise * 100})
key(1, 'p-phone-rise', 2, 1 + rise, 1 + 0.071, {'fall': 1 - rise, 'rise-only': rise, 'one-place': 1 + rise * 10})
new = 30 * (1 + rise)
key(1, 'p-phone-rise', 3, new, 30 + pct_build(30, 7.1), {'rise-only': 30 * rise, 'one-place': 30 * (1 + 10 * rise), 'fall': 30 * (1 - rise)})
slips = {'old-price': Fr(12, 30), 'upside-down': new / 12, 'saving': (new - 12) / new}
key(1, 'p-phone-rise', 4, Fr(12) / new, 12 / 32.13, slips, shown=0.373)
ok(new - 12 == Fr(2013, 100), 'saving 20.13')
for i, v in slips.items():
    s = stored(1, 'p-phone-rise', 4, i)
    one = Fr(round(v * 1000), 1000)
    if abs(one - Fr(str(s['value']))) >= Fr(str(s['tol']['abs'])):
        claims.append(f'1/p-phone-rise.4: slip {i} is {float(v)*100:.3f}%; to 1 d.p. {float(one)*100:.1f}%, which is outside or on the edge of its band {s["value"]} +- {s["tol"]["abs"]}')

# p-savings-tax: £18,000 at 4.6%, £500 allowance, 40% tax, tax-free 3.9%
sav = Fr(18000)
i = sav * pc(Fr(46, 10))
key(1, 'p-savings-tax', 1, i, pct_build(18000, 4.6), {'tenth': i / 10, 'ten-times': i * 10})
ok(pct_build(18000, 4) == 720 and pct_build(18000, .5) == 90 and pct_build(18000, .1) == 18, 'interest blocks')
tax = (i - 500) * pc(40)
key(1, 'p-savings-tax', 2, tax, 4 * pct_build(328, 10), {'all-taxed': i * pc(40), 'allowance-taxed': 500 * pc(40), 'kept': (i - 500) * pc(60)})
kept = i - tax
key(1, 'p-savings-tax', 3, kept / sav, (828 - 131.20) / 18000, {'gross': pc(Fr(46, 10)), 'all-taxed': pc(Fr(46, 10)) * pc(60), 'tax-share': tax / sav}, shown=0.0387)
ok(kept == Fr(69680, 100), 'kept 696.80')
free = sav * pc(Fr(39, 10))
ok(free == 702 and free > kept and free - kept == Fr(520, 100), 'tax-free 702 beats 696.80 by 5.20')
opts = {o['id']: o for o in part(1, 'p-savings-tax', 4)['widget']['options']}
ok(opts['tax-free'].get('correct') is True and sum(1 for o in opts.values() if o.get('correct')) == 1, 'choice key tax-free')
ok(sav * (pc(Fr(39, 10)) - pc(Fr(387, 100))) == Fr(540, 100), '0.03 points of 18,000 is 5.40')
claims.append(f'1/p-savings-tax.4 why "same": "0.03 percentage points, about £5.20": 0.03 points of £18,000 is £5.40; the true gap is {float(pc(Fr(39,10)) - kept/sav)*100:.4f} points, £{float(free-kept):.2f}')

# ------------------------------------------------------------------ set 2
# p-share-week: 72.50 -> 84.10, then down by the same percentage
mon, tue = Fr(7250, 100), Fr(8410, 100)
up = (tue - mon) / mon
key(2, 'p-share-week', 1, up, 84.10 / 72.50 - 1, {'new-base': (tue - mon) / tue, 'pounds': (tue - mon) / 100})
wed = tue * (1 - up)
key(2, 'p-share-week', 2, wed, 84.10 - pct_build(84.10, 16), {'cancel': mon, 'pounds': tue - 16, 'rise': tue * (1 + up)}, shown=70.64)
ch = (1 + up) * (1 - up) - 1
key(2, 'p-share-week', 3, ch, 70.644 / 72.50 - 1, {'sign': -ch, 'cancel': 0, 'new-base': (wed - mon) / wed})
ok(ch == -up ** 2, 'change is minus 0.16 squared')
back = 1 / (1 + ch) - 1
key(2, 'p-share-week', 4, back, 72.50 / 70.644 - 1, {'same': -ch, 'sixteen': up}, shown=0.0263)
ok(abs(70.644 * 1.0263 - 72.50) < 0.005, 'check line 70.644 x 1.0263')
# a learner who works part 3 from the rounded close of part 2 rather than from the multipliers
alt = (Fr(7064, 100) - mon) / mon
w = part(2, 'p-share-week', 3)['widget']
if abs(Fr(round(alt * 10000), 10000) - Fr(str(w['answer']))) >= Fr(str(w['tol']['abs'])):
    claims.append(f'2/p-share-week.3: from the rounded £70.64 of part 2 the change is {float(alt)*100:.4f}%, so {round(float(alt)*100, 2)}%; that sits on the edge of the band -2.56 +- 0.01')

# p-laptop-sale: £561.00 after 15% off, after a 10% rise
sale = Fr(561)
pre = sale / Fr(85, 100)
key(2, 'p-laptop-sale', 1, pre, 561 / 0.85, {'added': sale * Fr(115, 100)})
orig = pre / Fr(11, 10)
key(2, 'p-laptop-sale', 2, orig, 660 / 1.1, {'took-off': pre * Fr(9, 10), 'added-carried': sale * Fr(115, 100) / Fr(11, 10)})
ok(600 * Fr(11, 10) == 660 and 660 * Fr(85, 100) == 561, 'check lines')
slips = {'sign': (orig - sale) / orig, 'added': pc(10) - pc(15), 'sale-base': (sale - orig) / sale}
key(2, 'p-laptop-sale', 3, (sale - orig) / orig, 1.1 * 0.85 - 1, slips)
for i, v in slips.items():
    s = stored(2, 'p-laptop-sale', 3, i)
    one = Fr(round(v * 1000), 1000)
    if abs(one - Fr(str(s['value']))) >= Fr(str(s['tol']['abs'])):
        claims.append(f'2/p-laptop-sale.3: slip {i} is {float(v)*100:.3f}%; to 1 d.p. {float(one)*100:.1f}%, which is outside or on the edge of its band {s["value"]} +- {s["tol"]["abs"]}')
other = float(sale * Fr(85, 100))
if not any(abs(x['value'] - other) < .01 for x in part(2, 'p-laptop-sale', 1)['widget']['wrong']):
    claims.append(f'2/p-laptop-sale.1: taking 15% off again (£{other:.2f}) has no line')

# p-fund-two-years: 6,250 -> 7,840 in two equal years
p0, p2 = Fr(6250), Fr(7840)
tot = p2 / p0 - 1
key(2, 'p-fund-two-years', 1, tot, 1590 / 6250, {'new-base': (p2 - p0) / p2, 'multiplier': p2 / p0})
m = Fr(112, 100)
ok(m * m == p2 / p0, '1.12 squared is 1.2544')
key(2, 'p-fund-two-years', 2, m - 1, math.sqrt(1.2544) - 1, {'halved': tot / 2, 'total': tot})
simple = p0 + 2 * p0 * pc(12)
key(2, 'p-fund-two-years', 3, p2 - simple, 750 * 0.12, {'simple-balance': simple, 'none': 0})
five = p0 * m ** 5
v = 6250.0
for _ in range(5):
    v *= 1.12
key(2, 'p-fund-two-years', 4, five, v, {'simple': p0 + 5 * p0 * pc(12), 'halved': p0 * (1 + tot / 2) ** 5}, shown=11014.64)
ok(abs(float(m ** 5) - 1.762342) < 5e-7 and abs(7840 * 1.12 ** 3 - 11014.64) < 0.005, 'five-year multiplier and the check from 7,840')
claims.append(f'2/p-fund-two-years.4: the exact value is £{float(five):.4f}, half a penny off a whole penny; the printed product 6,250 x 1.762342 = {6250*1.762342:.4f}')

# p-fund-six-months: 52,000, three falls of 9%, three rises of 9%
f0 = Fr(52000)
d, u = Fr(91, 100), Fr(109, 100)
mar = f0 * d ** 3
v = 52000.0
for _ in range(3):
    v -= v * 0.09
key(2, 'p-fund-six-months', 1, mar, v, {'added': f0 * (1 - 3 * pc(9)), 'one-month': f0 * d}, shown=39185.69)
ok(abs(float(d ** 3) - 0.753571) < 5e-7 and abs(float(u ** 3) - 1.295029) < 5e-7, 'cubes as printed')
jun = mar * u ** 3
for _ in range(3):
    v += v * 0.09
key(2, 'p-fund-six-months', 2, jun, v, {'cancel': f0, 'added': Fr(3918569, 100) * (1 + 3 * pc(9))}, shown=50746.60)
ok(abs(39185.69 * 1.295029 - 50746.60) < 0.005, 'June from the rounded March value')
six = jun / f0 - 1
key(2, 'p-fund-six-months', 3, six, (0.91 * 1.09) ** 3 - 1, {'sign': -six, 'cancel': 0, 'one-pair': d * u - 1}, shown=-0.0241)
ok(d * u == Fr(9919, 10000) and abs(0.9919 ** 3 - 0.9759) < 5e-5 and abs(50746.60 / 52000 - 0.9759) < 5e-5, 'pair multiplier')
ok(abs(float(jun / f0) - 0.975896) < 5e-7, 'overall multiplier 0.975896')
key(2, "p-fund-six-months", 4, f0 / jun - 1, 1 / (0.91 * 1.09) ** 3 - 1, {'same': -six, 'nine': pc(9)}, shown=0.0247)
ok(abs(50746.60 * 1.0247 - 52000) < 1, 'check line 50,746.60 x 1.0247')
claims.append(f'2/p-fund-six-months.2: the slip "added" from the exact March value is £{float(mar*(1+3*pc(9))):.2f}, stored from the rounded one; fine. The compounding slip one-month (x1.09 once) £{39185.69*1.09:.2f} has no line')

# ------------------------------------------------------------------ set 3
# p-partners-profit: 18,000 : 24,000 : 30,000
st = [18000, 24000, 30000]
g = math.gcd(*st)
r3 = [x // g for x in st]
ok(r3 == [3, 4, 5] and g == 6000, 'ratio 3:4:5')
key(3, 'p-partners-profit', 1, Fr(sum(r3)), sum(st) / 6000, {'thousands': sum(x // 1000 for x in st), 'halved': sum(x // 2000 for x in st)})
key(3, 'p-partners-profit', 2, Fr(9600) * 5 / 12, 9600 * 30000 / 72000, {'equal': Fr(9600, 3), 'one-part': Fr(9600, 12)})
if Fr(9600) * 4 / 12 == Fr(9600, 3):
    claims.append('3/p-partners-profit.2: wrong "equal" 3,200 is also the share of the £24,000 partner (4 parts); that learner is told "You split the profit equally"')
key(3, 'p-partners-profit', 3, Fr(2850) / 3 * 12, 2850 * 72000 / 18000, {'own-parts': 2850 * 3, 'one-part-share': 2850 * 12})
key(3, 'p-partners-profit', 4, Fr(11900) * 2 / 14, 11900 * 12000 / 84000, {'old-parts': Fr(11900) * 2 / 12, 'equal': Fr(11900, 4)})
ok(Fr(12000, 6000) == 2 and 11900 / 14 == 850, 'new partner 2 parts, one part 850')

# p-print-run: 36,000 leaflets, 5 presses 12 hours, £14 a press-hour, rival £2.20 per 100
ph = 5 * 12
key(3, 'p-print-run', 1, Fr(ph, 8), 12 * 5 / 8, {'direct': Fr(12 * 8, 5), 'subtracted': 12 - 3})
key(3, 'p-print-run', 2, Fr(ph) * 14, 8 * 7.5 * 14, {'direct': 8 * Fr(96, 5) * 14, 'one-press': Fr(15, 2) * 14})
ok(5 * 12 * 14 == 840, 'five presses cost the same')
key(3, 'p-print-run', 3, Fr(840, 36), 840 / 36000 * 1000, {'per-leaflet': Fr(840, 36000), 'upside-down': Fr(36000, 840)}, shown=23.33)
rival = Fr(220, 100) * 10
ok(rival == 22 and rival < Fr(840, 36) and abs(23.33 - 22 - 1.33) < 1e-9 and abs(36 * 1.33 - 48) < 0.5 and 840 - 36 * 22 == 48, 'rival 22.00, saves 48')
opts = {o['id']: o for o in part(3, 'p-print-run', 4)['widget']['options']}
ok(opts['rival'].get('correct') is True and sum(1 for o in opts.values() if o.get('correct')) == 1, 'choice key rival')
if Fr(220, 100) < Fr(840, 36):
    claims.append('3/p-print-run.4 why "shop": comparing £2.20 with £23.33 unscaled makes the rival look cheaper, so that working does not lead to the shop; and two options print the scaled prices, so the part asks only which of 22.00 and 23.33 is smaller')

# p-coffee-suppliers: 12 kg CHF 330, 15 kg EUR 441, £1 = CHF 1.10 = EUR 1.20, 90 kg a month
chf = Fr(330, 12)
key(3, 'p-coffee-suppliers', 1, chf, 330 / 12, {'upside-down': Fr(12, 330), 'german': Fr(441, 15)})
sw = chf / Fr(11, 10)
key(3, 'p-coffee-suppliers', 2, sw, (330 / 1.10) / 12, {'multiplied': chf * Fr(11, 10)})
de = Fr(441, 15) / Fr(12, 10)
key(3, 'p-coffee-suppliers', 3, de, (441 / 1.20) / 15, {'multiplied': Fr(441, 15) * Fr(12, 10), 'euros': Fr(441, 15)})
key(3, 'p-coffee-suppliers', 4, 90 * (sw - de), 90 * 25.00 - 90 * 24.50, {'per-kg': sw - de, 'multiplied': 90 * (Fr(441, 15) * Fr(12, 10) - chf * Fr(11, 10))})

# p-villa-split: 8 pay EUR 405, 6 remain, £1 = EUR 1.125, four stay 7 nights, two stay 4
villa = 8 * 405
key(3, 'p-villa-split', 1, Fr(villa, 6), 405 * 8 / 6, {'direct': Fr(405 * 6, 8), 'unchanged': 405})
key(3, 'p-villa-split', 2, Fr(540) / Fr(1125, 1000), 540 * 8 / 9, {'multiplied': 540 * Fr(1125, 1000)})
nights = 4 * 7 + 2 * 4
key(3, 'p-villa-split', 3, Fr(villa, nights) * 7, 3240 * 7 / 36, {'equal': Fr(villa, 6), 'two-parts': Fr(villa) * 7 / 11, 'four-nights': Fr(villa, nights) * 4})
ok(nights == 36 and 4 * 630 + 2 * 360 == villa, 'shares by nights add to 3,240')
key(3, 'p-villa-split', 4, Fr(630 - 540) / Fr(1125, 1000), 630 / 1.125 - 540 / 1.125, {'euros': 90, 'multiplied': 90 * Fr(1125, 1000)})

# ------------------------------------------------------------------ shape of a set (docs/briefs/chained.md) and voice
for n, s in SETS.items():
    items = s['items']
    ok(3 <= len(items) <= 5, f'set {n}: item count')
    ok(any(i['difficulty'] == 5 for i in items) and all(3 <= i['difficulty'] <= 5 for i in items), f'set {n}: difficulty')
    parts = [p for i in items for p in i['parts']]
    typed = sum(1 for p in parts if p['widget']['kind'] != 'choice')
    ok(typed * 3 >= len(parts) * 2, f'set {n}: typed share')
    for i in items:
        ok(3 <= len(i['parts']) <= 5, f'{n}/{i["id"]}: parts')
        for k, p in enumerate(i['parts'], 1):
            ex = p['explain']['text']
            sents = [x for x in re.split(r'(?<=[.?])\s+(?=[A-Z0-9$£])', ex) if x.strip()]
            ok(len(sents) <= 3, f'{n}/{i["id"]}.{k}: explain has {len(sents)} sentences')
            blob = json.dumps(p, ensure_ascii=False) + i['prose']
            ok('!' not in blob and '—' not in blob and '–' not in blob, f'{n}/{i["id"]}.{k}: exclamation mark or dash')
            ok(not re.search(r'\b(color|center|favor|math\b|percent\b|analyze|liter|meter\b)', blob), f'{n}/{i["id"]}.{k}: American spelling')
            lines = [p['question'], ex] + [x for x in p['feedback'].values() if isinstance(x, str)] + list(p['feedback'].get('byKey', {}).values())
            lines += [o.get('why', '') for o in p['widget'].get('options', [])]
            for sent in re.split(r'(?<=[.?])\s+', re.sub(r'\$[^$]*\$', 'X', ' '.join(lines))):
                ok(len(sent.split()) <= 35, f'{n}/{i["id"]}.{k}: sentence over 35 words')
print(f'parts: {sum(len(i["parts"]) for s in SETS.values() for i in s["items"])}, wrong entries: {sum(len(p["widget"].get("wrong", [])) for s in SETS.values() for i in s["items"] for p in i["parts"])}')
for c in claims:
    print('CLAIM', c)
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
