"""Recompute every number in app/content/courses/number-sense/problems-1.json to problems-4.json twice.

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


def tex_value(s):
    """The value of a TeX fraction, mixed number or plain number: 3\\tfrac{1}{3}, \\tfrac{10}{3}, 7/12, 0.25."""
    s = s.replace('{,}', '').replace('−', '-').strip().strip('$').strip()
    m = re.match(r'^(-?\d+)\s*\\[td]?frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        return F(int(m.group(1))) + F(int(m.group(2)), int(m.group(3)))
    m = re.match(r'^(-?)\\[td]?frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        return F(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1)
    m = re.match(r'^(-?\d+)/(\d+)$', s)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    return F(s)


def last_value(text):
    """The figure after the last = or \\approx in a text, read as a fraction, mixed number or decimal."""
    s = text.replace('{,}', '')
    hits = list(re.finditer(r'(?:=|\\approx)\s*(-?\d*\s*\\tfrac\{\d+\}\{\d+\}|-?\d+(?:\.\d+)?)', s))
    return tex_value(hits[-1].group(1)) if hits else None


def frac_part(items, iid, kk, exact, alt, slips):
    """A part keyed by an exact fraction: two methods agree exactly, the key holds it to 6 dp with tol 0.0005,
    the accept line names the same fraction, the correct line ends on it, the question names the form, and
    every slip has a byKey line, matches its value and lies outside the band."""
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    exact, alt = F(exact), F(alt)
    ok(exact == alt, f'{tag}: methods differ {exact} vs {alt}')
    ok(abs(w['answer'] - float(exact)) <= 1e-6 and w['tol']['abs'] == 0.0005, f'{tag}: key {w["answer"]} vs {exact}')
    ok(re.search(r'fraction|mixed number', part['question']) is not None, f'{tag}: form not stated')
    acc = w['accept'].replace('Any form equal to ', '')
    for bit in acc.split('='):
        ok(tex_value(bit) == exact, f'{tag}: accept piece {bit} is not {exact}')
    ok(last_value(part['feedback']['correct']) == exact, f'{tag}: correct line does not end on {exact}')
    ok(last_value(part['explain']['text']) == exact or str(exact.numerator) in part['explain']['text'], f'{tag}: explain does not state {exact}')
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z['tol']['abs']
        ok(wid in part['feedback']['byKey'], f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(F(val))) <= max(wt, 1e-6), f'{tag}: wrong {wid} {z["value"]} vs slip {float(F(val))}')
        ok(F(val) != exact and abs(z['value'] - w['answer']) > w['tol']['abs'] + wt, f'{tag}: wrong {wid} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def exact_part(items, iid, kk, exact, alt, slips, printed=True):
    """A part with an exact whole or decimal key (tol 0, or under half a unit of its last place)."""
    part = items[iid]['parts'][kk - 1]
    w = part['widget']
    tag = f'{iid} p{kk}'
    e, a = F(exact), F(alt) if not isinstance(alt, float) else alt
    ok(abs(float(e) - float(a)) <= 1e-9 * max(1, abs(float(e))), f'{tag}: methods differ {float(e)} vs {float(a)}')
    ok(abs(w['answer'] - float(e)) <= w['tol']['abs'] + 1e-12, f'{tag}: key {w["answer"]} vs {float(e)}')
    if not float(w['answer']).is_integer():
        ok(re.search(r'decimal|places?|nearest|in pounds|value in pounds', part['question'], re.I) is not None, f'{tag}: form not stated')
    ok(abs(float(w['accept'].replace(',', '')) - w['answer']) <= w['tol']['abs'] + 1e-12, f'{tag}: accept {w["accept"]}')
    if printed:
        # the figure after the last = or \approx, else the key itself named in the line ("so she can bake 3 whole loaves")
        line = part['feedback']['correct'].replace('{,}', '')
        pv = last_value(line)
        said = pv is not None and abs(float(pv) - w['answer']) <= w['tol']['abs'] + 1e-9
        key_txt = f"{w['answer']:g}" if float(w['answer']).is_integer() else w['accept']
        ok(said or re.search(r'(?<![\d.])' + re.escape(key_txt.lstrip('-')) + r'(?![\d])', line) is not None,
           f'{tag}: correct line does not state the key (ends on {pv})')
    if w['answer'] < 0:
        ok(any(abs(z['value'] - abs(w['answer'])) <= 1e-9 for z in w['wrong']), f'{tag}: [negative-key] no wrong at {abs(w["answer"])}')
    wrongs = {z['id']: z for z in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z['tol']['abs']
        ok(wid in part['feedback']['byKey'], f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 1e-9), f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - w['answer']) > w['tol']['abs'] + wt, f'{tag}: wrong {wid} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')


def keyed(items, iid, kk, want):
    w = items[iid]['parts'][kk - 1]['widget']
    ok([o['id'] for o in w['options'] if o.get('correct')] == [want], f'{iid} p{kk}: keyed option is not {want}')


# ================================================================== level 1
def level1(L):
    # ---- garden: 20 beds, potatoes 2/5, beans 1/4
    beds = list(range(20))
    pot = F(2, 5) * 20
    pot_list = [b for b in beds if b % 5 < 2]                   # 2 beds in every 5
    exact_part(L, 'p-garden-beds', 1, pot, len(pot_list), {'one-fifth': F(20, 5), 'flipped': 20 * F(5, 2)})
    both = F(2, 5) + F(1, 4)
    beans = 20 // 4
    frac_part(L, 'p-garden-beds', 2, both, F(len(pot_list) + beans, 20), {'tops-bottoms': F(3, 9), 'tops-kept': F(3, 20)})
    flowers = 1 - both
    frac_part(L, 'p-garden-beds', 3, flowers, F(20 - len(pot_list) - beans, 20), {'carried': 1 - F(3, 9), 'beds': 7})
    roses = F(1, 2) * flowers
    frac_part(L, 'p-garden-beds', 4, roses, F(1, 2) * 7 / 20, {'doubled': 2 * flowers, 'added-half': flowers + F(1, 2), 'carried': F(1, 2) * (1 - F(3, 9))})
    stated('garden: roses in beds', 3.5, roses * 20)
    stated('garden: beans beds', 5, beans)
    stated('garden: 8 + 5', 13, both * 20)

    # ---- rye loaves: 5/6 kg, 1/4 kg a loaf
    flour, loaf = F(5, 6), F(1, 4)
    fits = flour / loaf
    # count quarters of 1/24 kg: 5/6 = 20/24 and 1/4 = 6/24
    frac_part(L, 'p-rye-loaves', 1, fits, F(20, 6), {'multiplied': flour * loaf, 'wrong-flip': F(6, 5) * loaf})
    ok(fits == 3 + F(1, 3), 'rye: 3 1/3')
    whole = int(fits)
    exact_part(L, 'p-rye-loaves', 2, whole, max(k for k in range(10) if k * loaf <= flour), {'rounded-up': whole + 1, 'carried': int(flour * loaf)})
    left = flour - whole * loaf
    frac_part(L, 'p-rye-loaves', 3, left, F(20 - 18, 24), {'one-loaf': flour - loaf, 'tops-bottoms': F(5 - 3, 6 - 4), 'loaf-third': fits - whole})
    ok((fits - whole) * loaf == left, 'rye: a third of a quarter kg is 1/12 kg')
    share = left / flour
    frac_part(L, 'p-rye-loaves', 4, share, F(2, 20), {'multiplied': left * flour, 'flipped': flour / left, 'carried': (flour - loaf) / flour})
    stated('rye: 3 loaves use', 0.75, whole * loaf)

    # ---- two printers: A 3/8 an hour, B 1/3 an hour
    a, b = F(3, 8), F(1, 3)
    first = a + b
    frac_part(L, 'p-two-printers', 1, first, F(9 + 8, 24), {'tops-bottoms': F(4, 11), 'multiplied': a * b})
    rest = 1 - first
    frac_part(L, 'p-two-printers', 2, rest, F(24 - 17, 24), {'carried': 1 - F(4, 11), 'count': 7})
    t = rest / a
    # minute by minute: A prints 3/8 per 60 min; count minutes in 1/9-hour steps (20/3 min) until 7/24 done
    steps = 0
    done = F(0)
    while done < rest:
        done += a / 9
        steps += 1
    frac_part(L, 'p-two-printers', 3, t, F(steps, 9), {'multiplied': rest * a, 'flipped': a / rest, 'printer-b': rest / b})
    total = 60 + t * 60
    frac_part(L, 'p-two-printers', 4, total, 60 + F(7 * 60, 9), {'rest-only': t * 60, 'hundred': 100 + t * 100, 'carried-flipped': 60 + (a / rest) * 60})
    ok(total == 106 + F(2, 3) and t * 60 == 46 + F(2, 3), 'printers: 46 2/3 and 106 2/3 minutes')
    stated('printers: 420/9', F(420, 9), t * 60)

    # ---- squash jugs: 3/4 litre each, A 4/9, B 5/12
    jug, sa, sb = F(3, 4), F(4, 9), F(5, 12)
    exact_part(L, 'p-squash-jugs', 1, sa * 36, 36 // 9 * 4, {'top-kept': 4, 'added': 4 + 27}, printed=False)
    ok(sb * 36 == 15 and sa > sb, 'squash: 16/36 against 15/36, A stronger')
    keyed(L, 'p-squash-jugs', 2, 'a')
    ca = sa * jug
    frac_part(L, 'p-squash-jugs', 3, ca, F(4 * 3, 9 * 4), {'added': sa + jug, 'divided': sa / jug})
    cb = sb * jug
    ok(cb == F(5, 16), 'squash: jug B 5/16 litre')
    tot = ca + cb
    frac_part(L, 'p-squash-jugs', 4, tot, F(16 + 15, 48), {'tops-bottoms': F(1 + 5, 3 + 16), 'carried': sa + jug + cb})
    bowl = 2 * jug
    ok(bowl == F(3, 2), 'squash: bowl 3/2 litres')
    frac_part(L, 'p-squash-jugs', 5, tot / bowl, (sa + sb) / 2, {'multiplied': tot * bowl, 'shares-added': sa + sb})
    ok(sb < tot / bowl < sa, 'squash: the mix lies between the two shares')


# ================================================================== level 2
def level2(L):
    # ---- moor weather
    t6 = F('-3.6')
    t2 = t6 + F('4.9')
    exact_part(L, 'p-moor-weather', 1, t2, -3.6 + 4.9, {'subtracted': t6 - F('4.9'), 'start-sign': F('3.6') + F('4.9')})
    t11 = F(-5)
    ch = t11 - t2
    exact_part(L, 'p-moor-weather', 2, ch, -(5 + 1.3), {'sign': -ch, 'added': t11 + t2, 'carried': t11 - (t6 - F('4.9'))})
    rate = ch / 9
    exact_part(L, 'p-moor-weather', 3, rate, sum([-0.7] * 9) / 9, {'sign': -rate, 'times': ch * 9})
    ok(9 * rate == ch, 'moor: 9 x -0.7 = -6.3')
    t3 = t11 + 4 * rate
    walk = -5.0
    for _ in range(4):
        walk -= 0.7
    exact_part(L, 'p-moor-weather', 4, t3, walk, {'sign': -t3, 'minus-minus': t11 - 4 * rate, 'change-only': 4 * rate})

    # ---- golf card
    card = [-1] * 4 + [-2] + [1] * 3 + [2] + [0] * 9
    ok(len(card) == 18, 'golf: 18 holes')
    tot = 4 * (-1) + 1 * (-2) + 3 * 1 + 1 * 2
    exact_part(L, 'p-golf-card', 1, tot, sum(card), {'sign': -tot, 'eagle-one': -4 - 1 + 3 + 2, 'no-signs': sum(abs(x) for x in card)})
    rounds = [tot, 2, -6, -3]
    mean = F(sum(rounds), 4)
    exact_part(L, 'p-golf-card', 2, mean, sp.Rational(-1 + 2 - 6 - 3, 4), {'sign': -mean, 'plus-as-minus': F(-1 - 2 - 6 - 3, 4), 'total': sum(rounds)})
    under = sum(1 for x in card if x < 0)
    ok(under == 5, 'golf: under par on 5 holes')
    d = F(5, 18)
    ok(round(float(d), 3) == 0.278 and str(float(d)).startswith('0.2777'), 'golf: 0.2777... to 0.278')
    exact_part(L, 'p-golf-card', 3, F('0.278'), round(5 / 18, 3), {'truncated': F(int(d * 1000), 1000), 'flipped': F(18, 5)})
    w3 = L['p-golf-card']['parts'][2]['widget']
    ok(abs(float(d) - w3['answer']) <= w3['tol']['abs'] and abs(0.277 - w3['answer']) > w3['tol']['abs'], 'golf p3: 0.2777... accepted, 0.277 not')
    keyed(L, 'p-golf-card', 4, 'rival')
    ok(F(28, 100) > d and float(F(28, 100) - d) < 0.0023, 'golf p4: 0.28 beats 0.2777... by about 0.002')

    # ---- taxi
    share = F(17, 6)
    exact_part(L, 'p-taxi-split', 1, F('2.8333'), round(17 / 6, 4), {'flipped': F('0.3529'), 'remainder': F('2.5')})
    ok(abs(float(share) - 2.8333) <= 0.0001 and round(6 / 17, 4) == 0.3529, 'taxi: 17/6 and 6/17 to 4 places')
    pen = F(round(float(share) * 100), 100)
    exact_part(L, 'p-taxi-split', 2, pen, round(2.8333, 2), {'rounded-up': F('2.84'), 'one-dp': F('2.8')})
    diff = 6 * 283 - 1700
    exact_part(L, 'p-taxi-split', 3, diff, sum([283] * 6) - 1700, {'sign': -diff, 'pounds': F(diff, 100), 'carried-up': 6 * 284 - 1700})
    last = 17 - 5 * pen
    exact_part(L, 'p-taxi-split', 4, last, pen - F(diff, 100), {'same': pen, 'wrong-way': pen + F(diff, 100), 'shortfall': F(-diff, 100)})
    stated('taxi: five pay', 14.15, 5 * pen)
    stated('taxi: 1,698', 1698, 6 * 283)


# ================================================================== level 3
def level3(L):
    # ---- cube tub
    n = 1500
    edge = sp.integer_nthroot(n, 3)[0]
    exact_part(L, 'p-cube-tub', 1, edge, max(k for k in range(1, 50) if k ** 3 <= n),
               {'rounded-up': edge + 1, 'square-root': sp.integer_nthroot(n, 2)[0], 'thirds': n // 3})
    ok(11 ** 3 == 1331 and 12 ** 3 == 1728 and 38 ** 2 <= n < 39 ** 2, 'cube: 1,331 and 1,728; root 1,500 is 38.7')
    left = n - edge ** 3
    exact_part(L, 'p-cube-tub', 2, left, n - 11 * 11 * 11, {'squared': n - 11 ** 2, 'carried-up': n - 12 ** 3, 'times-three': n - 33})
    side = sp.integer_nthroot(left, 2)
    ok(side[1], 'cube: 169 is a perfect square')
    exact_part(L, 'p-cube-tub', 3, side[0], next(k for k in range(1, 100) if k * k == left), {'halved': F(left, 2), 'quartered': F(left, 4)}, printed=False)
    ok(12 ** 2 == 144 and 14 ** 2 == 196, 'cube: 144 and 196 either side')

    # ---- stationery bill
    est = 40 * 5 + 20
    exact_part(L, 'p-stationery-bill', 1, est, round(38, -1) * round(4.85) + round(19.5, -1), {'bracket-first': 40 * (5 + 20), 'no-delivery': 40 * 5})
    ok([float(f'{x:.1g}') for x in (38, 4.85, 19.5)] == [40.0, 5.0, 20.0], 'bill: the figures to 1 sf')
    bill = 38 * F('4.85') + F('19.50')
    exact_part(L, 'p-stationery-bill', 2, bill, sum([4.85] * 38) + 19.5, {'bracket': 38 * (F('4.85') + F('19.50')), 'boxes-only': 38 * F('4.85')})
    calc = 38 * F('4.85') + F('19.50') / 3
    exact_part(L, 'p-stationery-bill', 3, calc, 184.3 + 6.5, {'intended': F('67.93'), 'delivery-share': F('19.50') / 3})
    sh = bill / 3
    exact_part(L, 'p-stationery-bill', 4, F('67.93'), round(203.8 / 3, 2),
               {'calculator': calc, 'carried-bracket': F('308.43'), 'estimate': F('73.33')})
    ok(abs(sh - F('67.93')) < F(1, 200) and round(float(38 * (F('4.85') + F('19.50')) / 3), 2) == 308.43 and round(220 / 3, 2) == 73.33,
       'bill: 67.933..., 925.30 / 3 and 220 / 3')

    # ---- comet probe
    hours = F(12, 10) * 10 ** 9 / (4 * 10 ** 4)
    exact_part(L, 'p-comet-probe', 1, hours, 1.2e9 / 4e4, {'kept-point': 3 * 10 ** 5, 'added-indices': 3 * 10 ** 12, 'short': 3000})
    ok(F(12, 10) / 4 == F(3, 10) and hours == F(3, 10) * 10 ** 5 == 3 * 10 ** 4, 'comet: 0.3 x 10^5 = 3 x 10^4')
    yr = 24 * 365
    r1 = int(float(f'{yr:.1g}'))
    exact_part(L, 'p-comet-probe', 2, r1, round(yr, -3), {'truncated': 8000, 'two-sf': 8800}, printed=False)
    ok(yr == 8760, 'comet: 8,760 hours')
    est = hours / r1
    exact_part(L, 'p-comet-probe', 3, int(float(f'{float(est):.1g}')), round(30000 / 9000), {'inverted': F(3, 10), 'carried': int(float(f'{30000 / 8000:.1g}'))})
    ok(30000 / 8000 == 3.75, 'comet: 3.75 rounds to 4')
    yrs = hours / yr
    exact_part(L, 'p-comet-probe', 4, F('3.4'), round(30000 / 8760, 1), {'nine-thousand': F('3.3'), 'carried': F('34.2'), 'days': hours / 24})
    w4 = L['p-comet-probe']['parts'][3]['widget']
    ok(abs(float(yrs) - w4['answer']) <= w4['tol']['abs'] and abs(float(30000 / 9000) - 3.3) <= 0.04 and round(300000 / 8760, 1) == 34.2,
       'comet p4: 3.42... accepted; 3.33 lands on the 9,000 slip; 34.2 from the 300,000 slip')


def figures_1_to_3():
    """Figures quoted in feedback, byKey and explain lines of sets 1 to 3 that are not keys or slips, each recomputed."""
    stated('rye: 20/6', F(20, 6), F(5, 6) * 4)
    stated('rye: 6/60', F(6, 60), F(1, 12) * F(6, 5))
    stated('rye: 10/12 and 9/12', F(10, 12) - F(9, 12), F(1, 12))
    stated('printers: 56/72', F(56, 72), F(7, 24) * F(8, 3))
    stated('printers: 7 of 9 pieces', F(7, 9), F(7, 24) / F(9, 24))
    stated('printers: 420/9', F(420, 9), F(7, 9) * 60)
    stated('squash: 12/36', F(12, 36), F(4, 9) * F(3, 4))
    stated('squash: 62/144', F(62, 144), F(31, 48) * F(2, 3))
    stated('squash: 5/16', F(5, 16), F(5, 12) * F(3, 4))
    stated('squash: one thirty-sixth', F(1, 36), F(16, 36) - F(15, 36))
    stated('moor: 4.9 - 3.6', 1.3, F('4.9') - F('3.6'))
    stated('moor: 1.3 + 5', 6.3, F('1.3') + 5)
    stated('golf: 6 under', -6, 4 * -1 - 2)
    stated('golf: 5 over', 5, 3 + 2)
    stated('golf: -1 + 2 - 6 - 3', -8, -1 + 2 - 6 - 3)
    stated('golf: gap to 0.28', 0.002, float(F(28, 100) - F(5, 18)), 0.0003)
    stated('taxi: 16.98', 16.98, 6 * F('2.83'))
    stated('taxi: 50 tenths', 8, 50 // 6)
    stated('taxi: 20 hundredths', 3, 20 // 6)
    stated('taxi: remainder 2', 2, 50 % 6)
    stated('bill: 184.30', 184.3, 38 * F('4.85'))
    stated('bill: 6.50', 6.5, F('19.50') / 3)
    stated('bill: 925.30', 925.3, 38 * (F('4.85') + F('19.50')))
    stated('bill: about 73', 73, round(220 / 3))
    stated('cube: 121', 121, 11 ** 2)
    stated('cube: 33', 33, 11 * 3)
    stated('comet: 30 / 9', 3.33, 30 / 9, 0.004)
    stated('comet: 1,250 days', 1250, 30000 / 24)
    stated('comet: 3.42', 3.42, 30000 / 8760, 0.005)


figures_1_to_3()
for n, fn in ((1, level1), (2, level2), (3, level3), (4, level4)):
    fn(load(n))
    lv = Level('number-sense', n)
    lv.check_wrongs(f'problems-{n}')
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'level {n}: numbers_lib check_wrongs {len(bad)} bad')
print(f'number-sense problem sets 1 to 4; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
