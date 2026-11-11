"""Recompute every number in app/content/courses/number-sense/problems-4.json twice.

Method 1 is exact: sympy (factorint, igcd, ilcm, divisor_count, pi) or fractions.
Method 2 is independent: trial division and listing, a tile-by-tile or tooth-by-tooth count, sorting and
counting the data, or the value worked in floats with pi = 3.14 and 22/7 as a learner would.
For each numeric part the script checks that the two methods agree; that the JSON key lies within its tol of
the value; that the value at the rounding the question asks for is accepted; that the values from pi = 3.14
and 22/7 are accepted where pi is used; that the figure printed last in `feedback.correct` is accepted; that
the `accept` line is a plain accepted number; that every `wrong` value matches its named slip, has a byKey
line, lies outside the key's band and does not overlap another `wrong`; and that a non-whole key names its
form. The choice part checks the keyed option and the figures that decide it. Figures stated in feedback and
explanations are recomputed with `stated`. numbers_lib's Level.check_wrongs runs over the set as a second
check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-number-sense-numbers.py
"""
import itertools, json, os, re, sys
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'number-sense')
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
    s = text.replace('{,}', '').replace(',', '').replace('−', '-')
    hits = list(re.finditer(r'(=|\\approx|:)\s*\$?(-?\d+(?:\.\d+)?)', s))
    if hits:
        return float(hits[-1].group(2))
    alln = re.findall(r'-?\d+(?:\.\d+)?', s)
    return float(alln[-1]) if alln else None


def num(items, iid, kk, exact, alt, slips, dp=None, pis=None, agree=1e-9):
    """pis: a function of pi giving the value a learner gets with that pi (then 3.14 and 22/7 are probed)."""
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    if dp is not None:
        ok(abs(round(e, dp) - w['answer']) <= tol + 1e-9, f'{tag}: value at {dp} dp {round(e, dp)} not accepted')
    if pis is not None:
        for P in (3.14, 22 / 7):
            v = pis(P)
            v = round(v, dp) if dp is not None else v
            ok(abs(v - w['answer']) <= tol + 1e-9, f'{tag}: the value with pi = {P:.4f}, {v}, is not accepted')
    if not float(w['answer']).is_integer():
        ok(re.search(r'decimal|places?|fraction|nearest', part['question'], re.I) is not None, f'{tag}: form not stated')
    pv = printed_value(part['feedback']['correct'])
    ok(pv is not None and abs(pv - w['answer']) <= tol + 1e-9 or (pv is not None and abs(pv - e) > 0.02 * abs(e)),
       f'{tag}: printed {pv} near the key but not accepted')
    lead = re.match(r'-?\d+(?:\.\d+)?$', w.get('accept', ''))
    ok(lead is not None and abs(float(lead.group()) - w['answer']) <= tol + 1e-9, f'{tag}: accept {w.get("accept")} not a plain accepted number')
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
        ok(wt <= 0.5 * abs(z['value']), f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def text_has(items, iid, kk, *bits):
    part = items[iid]['parts'][kk - 1]
    blob = json.dumps(part, ensure_ascii=False)
    for b in bits:
        ok(b in blob, f'{iid} p{kk}: "{b}" not in the part')


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


# ================================================================== level 4
def level4(L):
    # ---- kitchen floor tiles (360 cm by 600 cm)
    W, H = 360, 600
    ok(sp.factorint(W) == {2: 3, 3: 2, 5: 1} and sp.factorint(H) == {2: 3, 3: 1, 5: 2}, 'tiles: the stated prime forms')
    ok('primes' not in L['p-hall-tiles']['prose'] and '360' in L['p-hall-tiles']['prose'] and '600' in L['p-hall-tiles']['prose'],
       'tiles: the prose gives the lengths and no prime forms')
    hcf = sp.igcd(W, H)
    common = [d for d in factors(W) if H % d == 0]
    num(L, 'p-hall-tiles', 1, hcf, max(common), {'lcm': sp.ilcm(W, H), 'missing-prime': 2 ** 3 * 3})
    ok(sp.ilcm(W, H) == 2 ** 3 * 3 ** 2 * 5 ** 2 == 1800, 'tiles: LCM 1,800 from the primes')
    ok(hcf == 2 ** 3 * 3 * 5 == 120 and 24 == sp.igcd(W, H) // 5 and W % 24 == 0 and H % 24 == 0, 'tiles: 120 from the shared primes; 24 drops the 5 and still divides both')
    num(L, 'p-hall-tiles', 2, sp.divisor_count(120), len(common), {'indices-multiplied': 3 * 1 * 1, 'indices-added': (3 + 1) + (1 + 1) + (1 + 1),
                                                                   'lcm-carried': sp.divisor_count(sp.ilcm(W, H))})
    ok(sp.divisor_count(120) == (3 + 1) * (1 + 1) * (1 + 1) == 16 and max(common) == 120 and min(common) == 1, 'tiles: 16 sides from 1 cm to 120 cm')
    ok(sp.divisor_count(1800) == 36 and 3 + 1 + 1 == 5, 'tiles: 36 factors of 1,800')
    tiles = sum(1 for i in range(0, W, 120) for j in range(0, H, 120))
    num(L, 'p-hall-tiles', 3, (W // 120) * (H // 120), tiles, {'rows-added': W // 120 + H // 120, 'small-tile-carried': (W // 24) * (H // 24)})
    area = F(15 * 120 * 120, 10000)
    num(L, 'p-hall-tiles', 4, area, F(360, 100) * F(600, 100), {'hundred': F(15 * 120 * 120, 100), 'cm-squared': 15 * 120 * 120})
    stated('tiles: one tile', 14400, 120 * 120)
    stated('tiles: floor cm2', 216000, 15 * 120 * 120)
    stated('tiles: 3.6 x 6', 21.6, 3.6 * 6, 1e-9)
    text_has(L, 'p-hall-tiles', 4, '14{,}400', '216{,}000', '21.6')
    hall = json.dumps(L['p-hall-tiles'], ensure_ascii=False)
    ok(not re.search(r'(?<![\d.])108(?![\d])', hall), "tiles: the old hall's 108 is left nowhere in p-hall-tiles (review-delta-holes finding 1)")
    g2 = L['p-hall-tiles']['parts'][1]['feedback']['generic']
    ok('factors of 120' in g2 and 'factors of 108' not in g2, 'tiles: part 2 generic names the factors of 120, the number its question asks about')
    ok('120' in L['p-hall-tiles']['parts'][1]['question'], 'tiles: part 2 question says 120')
    ok(L['p-hall-tiles']['parts'][0]['widget']['unit'] == 'cm' and L['p-hall-tiles']['parts'][3]['widget']['unit'] == 'm\u00b2', 'tiles: units cm and m2')

    # ---- courtyard and basin (14 m by 11 m, 5 m across)
    basin = sp.pi * F(5, 2) ** 2
    num(L, 'p-lawn-pond', 1, basin, 6.25 * 3.141592653589793, {'diameter': sp.pi * 25, 'circumference': sp.pi * 5}, dp=2,
        pis=lambda P: P * 6.25)
    for wid, f in (('diameter', lambda P: P * 25), ('circumference', lambda P: P * 5)):
        z = next(w for w in L['p-lawn-pond']['parts'][0]['widget']['wrong'] if w['id'] == wid)
        for P in (3.14, 22 / 7, float(sp.pi)):
            ok(abs(round(f(P), 2) - z['value']) <= z['tol']['abs'], f'basin: slip {wid} with pi {P:.4f} still names the slip')
    ok(round(float(basin), 2) == 19.63 and abs(3.14 * 6.25 - 19.625) < 1e-12, 'basin: 19.63, and 19.625 with pi = 3.14')
    ok(abs(float(sp.pi * 5) - float(basin)) > 1, 'basin: area and distance round are different numbers')
    court = 14 * 11
    num(L, 'p-lawn-pond', 2, F(court) - F('19.63'), sum(1 for i in range(14) for j in range(11)) - 19.63,
        {'circumference-carried': F(court) - F('15.71'), 'perimeter': 2 * (14 + 11) - F('19.63')}, dp=2,
        pis=lambda P: court - round(P * 6.25, 2))
    need = F('134.37') / 12
    tins = next(b for b in range(1, 20) if 12 * b >= F('134.37'))
    num(L, 'p-lawn-pond', 3, -(-F('134.37') // 12), tins, {'rounded-down': F('134.37') // 12, 'whole-courtyard': -(-F(court) // 12)})
    stated('basin: 134.37 / 12', 11.20, round(float(need), 2))
    ok(round(need) == 11 and -(-need // 1) == 12 and -(-F(court) // 12) == 13, 'basin: rounding to nearest gives 11 but up gives 12 (review-delta-holes finding 7); the whole courtyard gives 13')
    ok(-(-F('138.29') // 12) == 12, 'basin: the dropped circumference slip, 138.29 / 12, also gives 12, so it is no slip here')
    stated('basin: 11 tins cover 132 and 12 cover 144', 144 - 132, 12)
    ok(12 * 12 >= 134.37 > 11 * 12 and 144 > 134.37, 'basin: 12 tins just enough')
    pj = json.dumps(L['p-lawn-pond']['parts'][2], ensure_ascii=False)
    ok(not re.search(r'(?<![\d.])(15 m|8\.96|135 m|120 m)', pj) and 'circumference-carried' not in pj, 'basin: no figure or slip of the 15 m2 tin version is left in the part')
    ok(L['p-lawn-pond']['parts'][0]['widget']['unit'] == 'm\u00b2' and L['p-lawn-pond']['parts'][1]['widget']['unit'] == 'm\u00b2', 'basin: units m2')

    # ---- cycle commute
    t = [26, 31, 24, 52, 27]
    mean = F(sum(t), len(t))
    num(L, 'p-cycle-commute', 1, mean, sp.Rational(sum(t), 5), {'four-days': F(sum(t), 4), 'median': sorted(t)[2]})
    num(L, 'p-cycle-commute', 2, sorted(t)[2], [v for v in t if sum(u < v for u in t) == 2][0], {'unsorted': t[2], 'mean': mean})
    w = L['p-cycle-commute']['parts'][2]['widget']
    ok([o['id'] for o in w['options'] if o.get('correct')] == ['median'], 'commute p3: the median is keyed')
    ok(sum(v < mean for v in t) == 4 and max(t) - min(t) == 28, 'commute p3: four rides under the mean, range 28')
    speed = F(9) / F(27, 60)
    num(L, 'p-cycle-commute', 4, speed, 9 * 60 / 27, {'per-minute': F(9, 27), 'mean-time': F(9) / F(32, 60)})
    ms = speed * 1000 / 3600
    num(L, 'p-cycle-commute', 5, ms, 20 / 3.6, {'wrong-way': speed * F(36, 10), 'minutes': speed * 1000 / 60}, dp=2)
    stated('commute: total', 160, sum(t))

    # ---- meshing gears
    ok(sp.factorint(48) == {2: 4, 3: 1} and sp.factorint(18) == {2: 1, 3: 2}, 'gears: the stated prime forms')
    teeth = next(k for k in range(1, 10000) if k % 48 == 0 and k % 18 == 0)
    num(L, 'p-meshing-gears', 1, sp.ilcm(48, 18), teeth, {'product': 48 * 18, 'hcf': sp.igcd(48, 18)})
    # tooth by tooth: count turns of the small gear until both painted teeth are back at the contact point
    k, turns = 0, 0
    while True:
        k += 1
        if k % 18 == 0:
            turns += 1
        if k % 48 == 0 and k % 18 == 0:
            break
    num(L, 'p-meshing-gears', 2, F(teeth, 18), turns, {'big-gear': F(teeth, 48), 'product-carried': F(864, 18)})
    per_min = 4 * 60
    num(L, 'p-meshing-gears', 3, F(per_min, 8), sum(1 for s in range(1, per_min + 1) if s % 8 == 0),
        {'per-second': F(4, 8), 'big-gear-carried': F(per_min, 3)})
    dist = per_min * sp.pi * 6 / 100
    num(L, 'p-meshing-gears', 4, round(float(dist)), round(240 * 18.84955592 / 100),
        {'radius': round(float(per_min * 2 * sp.pi * 6 / 100)), 'centimetres': float(per_min * sp.pi * 6)}, pis=lambda P: round(240 * P * 6 / 100))
    ok(abs(float(dist) - 45) <= 0.5 and abs(round(float(dist), 2) - 45.24) < 1e-9, 'gears: 45.24 m rounds to 45')
    q4 = L['p-meshing-gears']['parts'][3]
    ok('4 \\times 60 = 240' in q4['question'] and q4['widget']['unit'] == 'm', 'gears p4: the question carries the 240 turns it uses, unit m')
    ok(L['p-cycle-commute']['parts'][3]['widget']['unit'] == 'km/h' and L['p-cycle-commute']['parts'][4]['widget']['unit'] == 'm/s', 'commute: units km/h and m/s')
    stated('gears: one turn', 18.85, round(float(6 * sp.pi), 2))
    stated('gears: 240 x 18.85', 4524, 240 * 18.85)


items = load(4)
level4(items)
lv = Level('number-sense', 4)
lv.check_wrongs('problems-4')
bad = [r for r in lv.results if not r[0]]
ok(not bad, f'level 4: numbers_lib check_wrongs {len(bad)} bad')
print(f'number-sense problem set 4; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
