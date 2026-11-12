"""Recompute every number in app/content/courses/ratio/problems-1.json, problems-2.json and problems-3.json twice.

Method 1 is exact: fractions.Fraction (and sympy for the square root).
Method 2 is independent: the learner's route in floats (build a percentage from 10%, 1% and 0.1%, step a balance
month by month, count parts by listing them, convert currencies one unit at a time).
For each numeric part the script checks that the two methods agree; that the JSON key lies within its tol of the
value; that the value at the rounding the question asks for is accepted; that the figure printed last in
`feedback.correct` is accepted; that every `wrong` value matches its named slip, has a byKey line, lies outside
the key's band and does not overlap another `wrong`; that a negative key has a `sign` slip at its absolute value;
and that a non-whole key names its form. Choice parts check the keyed option and the figures that decide it.
Figures stated in feedback and explanations are recomputed with `stated`/`text_has`. numbers_lib's
Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-ratio-numbers.py
"""
import itertools, json, math, os, re, sys
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'ratio')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(nn):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{nn}.json')))['items']}


def printed_value(text):
    s = text.replace('{,}', '').replace(',', '').replace('−', '-').replace('\\%', '%')
    hits = list(re.finditer(r'(=|\\approx)\s*\$?(-?\d+(?:\.\d+)?)', s))
    if hits:
        return float(hits[-1].group(2))
    alln = re.findall(r'-?\d+(?:\.\d+)?', s)
    return float(alln[-1]) if alln else None


def num(items, iid, kk, exact, alt, slips, dp=None, pct=False, agree=1e-9):
    """exact, alt: the value by two methods (a fraction for percentages, not the per cent figure).
    dp: decimal places asked for, in the units the learner types (per cent figure when pct)."""
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    ok((w.get('unit') == '%') == pct, f'{tag}: unit % expected {pct}')
    if dp is not None:
        typed = round(e * 100, dp) / 100 if pct else round(e, dp)
        ok(abs(typed - w['answer']) <= tol + 1e-12, f'{tag}: value at {dp} dp {typed} not accepted')
    if not float(w['answer']).is_integer():
        ok(re.search(r'decimal|places?|nearest|percentage|per cent|in pounds', part['question'], re.I) is not None, f'{tag}: form not stated')
    pv = printed_value(part['feedback']['correct'])
    if pv is not None:
        pv_key = pv / 100 if pct and abs(pv / 100 - e) < abs(pv - e) else pv
        ok(abs(pv_key - w['answer']) <= tol + 1e-9 or abs(pv_key - e) > 0.02 * max(abs(e), 1e-9),
           f'{tag}: printed {pv} near the key but not accepted')
    acc = w.get('accept', '').replace(',', '').replace('£', '').replace('%', '')
    ok(re.match(r'-?\d+(?:\.\d+)?$', acc) is not None, f'{tag}: accept {w.get("accept")} not a plain figure')
    if acc and re.match(r'-?\d+(?:\.\d+)?$', acc):
        av = float(acc) / 100 if pct else float(acc)
        ok(abs(av - w['answer']) <= tol + 1e-9, f'{tag}: accept {w["accept"]} outside the band')
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    if w['answer'] < 0:
        ok('sign' in wrongs and abs(wrongs['sign']['value'] - abs(w['answer'])) <= wrongs['sign']['tol']['abs'] + tol,
           f'{tag}: negative key without a sign slip at its absolute value')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
        ok(wt <= 0.5 * abs(z['value']) or z['value'] == 0, f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def choice(items, iid, kk, key_id, cond, label):
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    ok(w['kind'] == 'choice', f'{iid} p{kk}: not choice')
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [key_id], f'{iid} p{kk}: keyed {keyed}, expected {key_id}')
    ok(all('why' in o for o in w['options'] if not o.get('correct')), f'{iid} p{kk}: a distractor has no why')
    ok(cond, f'{iid} p{kk}: {label}')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def text_has(items, iid, kk, *bits):
    part = items[iid]['parts'][kk - 1] if kk else items[iid]
    blob = json.dumps(part, ensure_ascii=False).replace('\\\\', '\\')
    for b in bits:
        ok(b in blob, f'{iid} p{kk}: "{b}" not in the text')


def build(amount, pct_tenths):
    """A learner's build of p% of amount from 1% and 0.1% pieces (pct given in tenths of a per cent)."""
    one, tenth = amount / 100, amount / 1000
    return (pct_tenths // 10) * one + (pct_tenths % 10) * tenth


# ================================================================== level 1
def level1(L):
    # ---- pension pot £9,600, 3/8 in shares
    pot = F(9600)
    s = F(3, 8)
    num(L, 'p-pension-split', 1, s, 3 / 8, {'decimal': s / 100, 'upside-down': 1 / s}, pct=True)
    shares = s * pot
    num(L, 'p-pension-split', 2, shares, 37.5 * build(9600, 10), {'ten-times': 10 * shares, 'tenth': shares / 10, 'bonds': pot - shares})
    stated('pension: 10% of the pot', 960, pot / 10)
    stated('pension: 1% of the pot', 96, pot / 100)
    sh2 = shares * F(115, 100)
    num(L, 'p-pension-split', 3, sh2, 3600 + 3600 * 0.15, {'multiplier-1-5': shares * F(3, 2), 'rise-only': shares * F(15, 100), 'bonds': (pot - shares) * F(115, 100)})
    bonds = pot - shares
    stated('pension: bonds', 6000, bonds)
    bo2 = bonds * F(96, 100)
    num(L, 'p-pension-split', 4, bo2, 6000 - 6000 * 0.04, {'rise': bonds * F(104, 100), 'fall-only': bonds * F(4, 100), 'multiplier-0-6': bonds * F(6, 10)})
    frac = sh2 / (sh2 + bo2)
    num(L, 'p-pension-split', 5, frac, 4140 / 9900, {'old-total': sh2 / pot, 'unchanged': s, 'bonds-base': sh2 / bo2}, dp=1, pct=True)
    stated('pension: new pot', 9900, sh2 + bo2)
    text_has(L, 'p-pension-split', 5, '9{,}900', '41.8%', '37.5%')

    # ---- platform fee 0.35% on £8,400
    r = F(35, 10000)
    num(L, 'p-platform-fee', 1, r, 0.35 / 100, {'one-place': r * 10, 'no-move': r * 100, 'times-100': 35})
    fee = r * 8400
    num(L, 'p-platform-fee', 2, fee, build(8400, 3) + 8400 / 2000, {'one-place': fee * 10, 'no-move': fee * 100, 'half-only': F(8400, 200)}, dp=2)
    stated('fee: 0.1% of 8,400', 8.40, 8400 / 1000)
    stated('fee: 0.3% of 8,400', 25.20, 3 * 8.40, 1e-9)
    stated('fee: 0.05% of 8,400', 4.20, 8400 * 0.0005, 1e-9)
    after = 8400 * (1 - r)
    num(L, 'p-platform-fee', 3, after, 8400 - 29.40, {'added': 8400 * (1 + r), 'one-place': 8400 * (1 - 10 * r), 'fee-only': fee}, dp=2)
    stated('fee: multiplier', 0.9965, 1 - r)
    share = F(24) / fee
    num(L, 'p-platform-fee', 4, share, 24 / 29.4, {'upside-down': fee / 24, 'account-base': F(24, 8400), 'one-place': F(24) / (10 * fee)}, dp=0, pct=True)
    ok(F(24) < fee, 'fee: the rival is cheaper, as the explanation says')

    # ---- phone contract £30.00, inflation 3.2% plus 3.9 points
    rise = F(32, 1000) + F(39, 1000)
    num(L, 'p-phone-rise', 1, rise, (3.2 + 3.9) / 100, {'one-place': rise * 10, 'no-move': rise * 100})
    m = 1 + rise
    num(L, 'p-phone-rise', 2, m, 1.071, {'fall': 1 - rise, 'rise-only': rise, 'one-place': 1 + 10 * rise})
    newp = 30 * m
    num(L, 'p-phone-rise', 3, newp, 30 + build(30, 71), {'rise-only': 30 * rise, 'one-place': 30 * (1 + 10 * rise), 'fall': 30 * (1 - rise)}, dp=2)
    sim = F(12) / newp
    num(L, 'p-phone-rise', 4, sim, 12 / 32.13, {'old-price': F(12, 30), 'upside-down': newp / 12, 'saving': (newp - 12) / newp}, dp=1, pct=True)
    stated('phone: the saving', 20.13, float(newp - 12), 1e-9)

    # ---- savings £18,000 at 4.6%, £500 allowance, 40% tax
    interest = F(18000) * F(46, 1000)
    num(L, 'p-savings-tax', 1, interest, build(18000, 46), {'tenth': interest / 10, 'ten-times': interest * 10})
    for shown, val in ((180, 18000 / 100), (720, 4 * 180), (90, 18000 * 0.005), (18, 18000 / 1000)):
        stated('savings: a building block', shown, val)
    tax = (interest - 500) * F(40, 100)
    num(L, 'p-savings-tax', 2, tax, 0.4 * 828 - 0.4 * 500, {'all-taxed': interest * F(4, 10), 'allowance-taxed': 200, 'kept': (interest - 500) * F(6, 10)}, dp=2)
    stated('savings: 10% of 328', 32.80, 32.8)
    rate = (interest - tax) / 18000
    num(L, 'p-savings-tax', 3, rate, 696.80 / 18000, {'gross': F(46, 1000), 'all-taxed': F(46, 1000) * F(6, 10), 'tax-share': tax / 18000}, dp=2, pct=True)
    isa = F(18000) * F(39, 1000)
    choice(L, 'p-savings-tax', 4, 'tax-free', isa > interest - tax and F(39, 1000) > rate, 'the tax-free account pays more')
    stated('savings: tax-free interest', 702, isa)
    stated('savings: the gap', 5.20, float(isa - (interest - tax)), 1e-9)
    stated('savings: gap in points', 0.03, round(float(F(39, 1000) - rate) * 100, 2), 1e-9)


# ================================================================== level 2
def level2(L):
    # ---- share £72.50 -> £84.10, then down 16%
    mon, tue = F('72.50'), F('84.10')
    r = (tue - mon) / mon
    num(L, 'p-share-week', 1, r, 11.6 / 72.5, {'new-base': (tue - mon) / tue, 'pounds': (tue - mon) / 100}, pct=True)
    wed = tue * (1 - r)
    num(L, 'p-share-week', 2, wed, 84.10 - 0.16 * 84.10, {'cancel': mon, 'pounds': tue - 16, 'rise': tue * (1 + r)}, dp=2)
    over = (1 + r) * (1 - r) - 1
    num(L, 'p-share-week', 3, over, (70.644 - 72.5) / 72.5, {'sign': -over, 'cancel': 0, 'new-base': (wed - mon) / wed}, dp=2, pct=True)
    stated('share: 1 - 0.16^2', 0.9744, 1 - r ** 2)
    back = 1 / ((1 + r) * (1 - r)) - 1
    num(L, 'p-share-week', 4, back, (72.5 - 70.644) / 70.644, {'same': -over, 'sixteen': r}, dp=2, pct=True)
    stated('share: check back to Monday', 72.50, round(70.644 * 1.0263, 2), 0.005)

    # ---- laptop £561.00 after 15% off, after a 10% rise
    sale = F(561)
    before = sale / F(85, 100)
    num(L, 'p-laptop-sale', 1, before, 561 * 100 / 85, {'added': sale * F(115, 100)})
    orig = before / F(11, 10)
    num(L, 'p-laptop-sale', 2, orig, 660 * 10 / 11, {'took-off': before * F(9, 10), 'added-carried': sale * F(115, 100) / F(11, 10)})
    ch = (sale - orig) / orig
    num(L, 'p-laptop-sale', 3, ch, 1.1 * 0.85 - 1, {'sign': -ch, 'added': F(10, 100) - F(15, 100), 'sale-base': (sale - orig) / sale}, dp=1, pct=True)

    # ---- fund £6,250 -> £7,840 over two years
    p0, p2 = F(6250), F(7840)
    tot = (p2 - p0) / p0
    num(L, 'p-fund-two-years', 1, tot, 1590 / 6250, {'new-base': (p2 - p0) / p2, 'multiplier': 1 + tot}, dp=2, pct=True)
    y = sp.sqrt(sp.Rational(p2, p0)) - 1
    ok(y == sp.Rational(12, 100), 'fund: sqrt(1.2544) is exactly 1.12')
    num(L, 'p-fund-two-years', 2, F(12, 100), 1.2544 ** 0.5 - 1, {'halved': tot / 2, 'total': tot}, pct=True)
    simple = p0 + 2 * p0 * F(12, 100)
    num(L, 'p-fund-two-years', 3, p2 - simple, 0.12 * (6250 * 0.12), {'simple-balance': simple, 'none': 0})
    five = p0 * F(112, 100) ** 5
    bal = 6250.0
    for _ in range(5):
        bal *= 1.12
    num(L, 'p-fund-two-years', 4, five, bal, {'simple': p0 * (1 + 5 * F(12, 100)), 'halved': p0 * (1 + tot / 2) ** 5}, dp=2)
    stated('fund: 1.12^5', 1.762342, float(F(112, 100) ** 5), 5e-7)
    stated('fund: 7,840 x 1.12^3', 11014.64, float(p2 * F(112, 100) ** 3), 0.005)
    stated('fund: 6,250 x 1.762342', 11014.64, 6250 * 1.762342, 0.005)

    # ---- fund £52,000, three months of -9% then three of +9%
    st = F(52000)
    mar = st * F(91, 100) ** 3
    v = 52000.0
    for _ in range(3):
        v -= 0.09 * v
    num(L, 'p-fund-six-months', 1, mar, v, {'added': st * F(73, 100), 'one-month': st * F(91, 100)}, dp=2)
    stated('six months: 0.91^3', 0.753571, float(F(91, 100) ** 3))
    mar_r = F('39185.69')
    jun = mar_r * F(109, 100) ** 3
    for _ in range(3):
        v += 0.09 * v
    num(L, 'p-fund-six-months', 2, jun, v, {'cancel': st, 'added': mar_r * F(127, 100)}, dp=2, agree=1e-7)
    stated('six months: 1.09^3', 1.295029, float(F(109, 100) ** 3))
    jun_r = F('50746.60')
    over = jun_r / st - 1
    exact_over = (F(91, 100) * F(109, 100)) ** 3 - 1
    num(L, 'p-fund-six-months', 3, exact_over, float(over), {'sign': -exact_over, 'cancel': 0, 'one-pair': F(91, 100) * F(109, 100) - 1}, dp=2, pct=True, agree=1e-6)
    stated('six months: 0.9919', 0.9919, F(91, 100) * F(109, 100))
    stated('six months: 0.9919^3', 0.975896, float((F(9919, 10000)) ** 3), 5e-7)
    back = 1 / (1 + exact_over) - 1
    num(L, 'p-fund-six-months', 4, back, 52000 / 50746.60 - 1, {'same': -exact_over, 'nine': F(9, 100)}, dp=2, pct=True, agree=1e-6)
    stated('six months: check', 52000, 50746.60 * 1.0247, 1.0)


# ================================================================== level 3
def level3(L):
    # ---- partners £18,000, £24,000, £30,000
    stakes = [18000, 24000, 30000]
    g = math.gcd(*stakes)
    simp = [x // g for x in stakes]
    ok(g == 6000 and simp == [3, 4, 5], 'partners: simplest form 3 : 4 : 5')
    listing = sum(1 for x in stakes for _ in range(x // 6000))
    num(L, 'p-partners-profit', 1, sum(simp), listing, {'thousands': sum(x // 1000 for x in stakes), 'halved': sum(x // 2000 for x in stakes)})
    part = F(9600, 12)
    num(L, 'p-partners-profit', 2, 5 * part, 9600 * 30000 / 72000, {'equal': F(9600, 3), 'one-part': part})
    tot = F(2850, 3) * 12
    num(L, 'p-partners-profit', 3, tot, 2850 * 72000 / 18000, {'own-parts': 2850 * 3, 'one-part-share': 2850 * 12})
    ok(math.gcd(12000, 6000) == 6000 and 12000 // 6000 == 2, 'partners: £12,000 is 2 parts')
    new = F(11900, 14) * 2
    num(L, 'p-partners-profit', 4, new, 11900 * 12000 / 84000, {'old-parts': F(11900, 12) * 2, 'equal': F(11900, 4)}, dp=2)

    # ---- print run: 5 presses, 12 hours, 36,000 leaflets
    ph = 5 * 12
    t8 = F(ph, 8)
    num(L, 'p-print-run', 1, t8, 12 * 5 / 8, {'direct': F(12 * 8, 5), 'subtracted': 12 - 3})
    cost = 8 * t8 * 14
    num(L, 'p-print-run', 2, cost, 5 * 12 * 14, {'direct': 8 * F(96, 5) * 14, 'one-press': t8 * 14})
    per = cost / 36
    num(L, 'p-print-run', 3, per, 840 / 36000 * 1000, {'per-leaflet': cost / 36000, 'upside-down': F(36000) / cost}, dp=2)
    rival = 10 * F('2.20')
    choice(L, 'p-print-run', 4, 'rival', rival < per, 'the rival is cheaper per 1,000')
    stated('print: rival per 1,000', 22.00, rival)
    stated('print: difference', 1.33, round(float(per - rival), 2))
    stated('print: whole-order saving', 48, float(cost - 36 * rival))

    # ---- coffee suppliers
    sw = F(330, 12)
    num(L, 'p-coffee-suppliers', 1, sw, 330 / 12, {'upside-down': F(12, 330), 'german': F(441, 15)}, dp=2)
    swp = sw / F(110, 100)
    num(L, 'p-coffee-suppliers', 2, swp, 27.5 * (1 / 1.10), {'multiplied': sw * F(110, 100)}, dp=2)
    de = F(441, 15) / F(120, 100)
    num(L, 'p-coffee-suppliers', 3, de, 441 / 1.2 / 15, {'multiplied': F(441, 15) * F(120, 100), 'euros': F(441, 15)}, dp=2)
    sav = 90 * (swp - de)
    num(L, 'p-coffee-suppliers', 4, sav, 90 * 25.00 - 90 * 24.50, {'per-kg': swp - de, 'multiplied': 90 * (F(441, 15) * F(120, 100) - sw * F(110, 100))}, dp=2)
    ok(de < swp, 'coffee: the German beans are cheaper')

    # ---- villa
    total = 8 * 405
    stated('villa: total', 3240, total)
    six = F(total, 6)
    num(L, 'p-villa-split', 1, six, 405 * 8 / 6, {'direct': F(405 * 6, 8), 'unchanged': 405})
    num(L, 'p-villa-split', 2, six / F(1125, 1000), 540 / 1.125, {'multiplied': six * F(1125, 1000)}, dp=2)
    nights = [7, 7, 7, 7, 4, 4]
    one = F(total, sum(nights))
    num(L, 'p-villa-split', 3, 7 * one, 3240 * 7 / 36, {'equal': six, 'two-parts': F(total * 7, 11), 'four-nights': 4 * one}, dp=2)
    extra = (7 * one - six) / F(1125, 1000)
    num(L, 'p-villa-split', 4, extra, 630 / 1.125 - 540 / 1.125, {'euros': 7 * one - six, 'multiplied': (7 * one - six) * F(1125, 1000)}, dp=2)
    ok(sum(nights) == 36 and one == 90, 'villa: 36 nights, €90 a night')


for n, fn in ((1, level1), (2, level2), (3, level3)):
    fn(load(n))
    lv = Level('ratio', n)
    lv.check_wrongs('problems')
    try:
        lv.report()
    except SystemExit as e:
        if e.code:
            fails.append(f'numbers_lib check_wrongs failed on level {n}')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
