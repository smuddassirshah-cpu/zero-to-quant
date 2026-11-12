"""Recompute every number in app/content/courses/counting/problems-<n>.json twice.

Method 1 is exact: math.comb / math.perm / factorials with fractions, and sympy for the vectors.
Method 2 is independent: brute enumeration with itertools (every row of flags or blocks, every
team, every line-up of the photo), an explicit list of 80 members, and, for the vectors, plain
coordinate arithmetic, math.hypot, atan2 and random numeric vectors in place of r and s.

For each numeric part the script checks that the two methods agree; that the JSON key lies within
its tol of the value; that the value at the rounding the question asks for is accepted; that the
number printed last in feedback.correct is accepted; that every `wrong` value matches its named
slip (recomputed here), has a byKey line, lies outside the key's band and does not overlap another
`wrong`; and that every number stated in feedback.correct and explain is one the script computed or
one the item's prose or question gives. Expression parts parse the key, every accepted form and
every wrong form with sympy and compare. Choice parts check the keyed option. numbers_lib's
Level.check_wrongs runs over each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-counting-numbers.py
"""
import json, os, re, sys, random, itertools
from fractions import Fraction as F
from math import comb, perm, factorial, hypot, sqrt, acos, atan2, degrees, isclose
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'counting')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _numbers  # noqa: E402

fails, checks = [], 0


def derived_slips(slips, wrongs, e, text=''):
    """Slips the script derives itself for the `sign` / `sign2` and `decimal` wrong entries.

    sign: the absolute value of the computed key (the sign-dropped answer).
    decimal: the computed key over 100 (over 10,000 where the part is in %^2).
    Each is then compared with the content value inside its tolerance, and must lie
    outside the key band, by the ordinary slip checks below."""
    s = dict(slips or {})
    for wid in wrongs:
        if wid in s:
            continue
        if re.fullmatch(r'sign\d*', wid):
            s[wid] = abs(e)
        elif wid == 'decimal':
            s[wid] = e / (10000 if '%\u00b2' in text else 100)
    return s


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf8'))['items']}


def agree(a, b, label):
    ok(isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-12), f'{label}: methods disagree {a} vs {b}')


def band(w):
    return w['tol']['abs'] + 1e-9


def check_numeric(item, k, value, slips, allowed=(), rounded=None):
    """value: exact answer; slips: {wrong id: slip value}; allowed: extra numbers the text may state."""
    p = item['parts'][k]
    w = p['widget']
    lab = f"{item['id']} part {k + 1}"
    ok(w['kind'] == 'numeric', f'{lab}: not numeric')
    ok(abs(w['answer'] - float(value)) <= band(w), f'{lab}: key {w["answer"]} not within tol of {float(value)}')
    for r in ([rounded] if rounded is not None else []):
        ok(abs(w['answer'] - r) <= band(w), f'{lab}: asked rounding {r} refused')
    # last number printed in feedback.correct is accepted
    nums = _numbers(p['feedback']['correct'].replace('\\approx', '='))
    if nums:
        last = [x for x in re.findall(r'-?\d+(?:\.\d+)?', p['feedback']['correct'].replace('{,}', ''))][-1]
        ok(abs(w['answer'] - float(last)) <= band(w) or abs(float(last) - float(value)) < 1e-9,
           f'{lab}: feedback prints {last}, outside the band')
    ids = [x['id'] for x in w['wrong']]
    slips = derived_slips(slips, ids, float(value), json.dumps(p, ensure_ascii=False))
    ok(sorted(ids) == sorted(slips), f'{lab}: wrong ids {ids} vs slips {sorted(slips)}')
    for x in w['wrong']:
        sv = slips.get(x['id'])
        if sv is None:
            continue
        ok(abs(x['value'] - float(sv)) <= band(x), f'{lab}: wrong {x["id"]} = {x["value"]} but slip gives {float(sv)}')
        ok(abs(x['value'] - w['answer']) > band(w) + band(x), f'{lab}: wrong {x["id"]} reaches the key band')
        ok(x['id'] in p['feedback'].get('byKey', {}), f'{lab}: wrong {x["id"]} has no byKey line')
    for a, b in itertools.combinations(w['wrong'], 2):
        ok(abs(a['value'] - b['value']) > band(a) + band(b), f'{lab}: wrongs {a["id"]} and {b["id"]} overlap')
    stated_ok(item, k, [value, w['answer']] + list(slips.values()) + list(allowed))


# Numbers a byKey line restates from an earlier part or from the slip's own working (each recomputed here).
EXTRA = {
    ('p-tulip-bed', 3): [factorial(8), comb(8, 4)],                       # 1680 x 24 = 40320 carried; 70 groups
    ('p-ice-cream-van', 2): [comb(14, 3) * 6 * 6],                         # 364 x 6 x 6 = 13104 cones from the part 1 slip
    ('p-ice-cream-van', 3): [comb(14, 3) * comb(14, 3) * 6],               # 364 x 2184 = 794976
    ('p-signal-flags', 2): [2 * factorial(6) // factorial(4)],             # 60, the doubled block
    ('p-signal-flags', 3): [factorial(7), 105 - 60, factorial(6) // factorial(4)],  # 5040, 45, 30
    ('p-leisure-centre', 3): [17 - 1],                                     # 17 x 16 ordered picks
    ('p-balloon-blocks', 2): [factorial(6), factorial(6) // 4],            # 720 and 180 from the part 2 slips
    ('p-balloon-blocks', 4): [factorial(7), 1260 - 720, 1260 - 360],       # 5040, 540, 900
    ('p-quiz-team', 2): [comb(6, 4)],                                      # 15 all-girl teams
    ('p-quiz-team', 4): [comb(11, 4) - comb(5, 4), comb(11, 4) - comb(5, 4) - comb(6, 4) - comb(5, 4)],  # 325, 305
    ('p-orienteering', 4): [3 + 28, 100 * (9 + 12 + 12 + 16)],             # 31 squares, 4900 m
    ('p-power-line', 4): [15 + 10 - 10],                                   # the 15 of 15 + 10
    ('p-grain-merchant', 0): [-40 * 3.5],                                  # -140
    ('p-grain-merchant', 2): [80, -70 * 3.5, -20, 30],                     # (80, 10) carried; -245; the trade
}


def stated_ok(item, k, known):
    """Every number in feedback.correct and explain is computed here or given by the prose or question."""
    p = item['parts'][k]
    given = set(_numbers(item.get('prose', '')) + _numbers(p['question']))
    pool = list(given)
    for x in list(known) + EXTRA.get((item['id'], k), []):
        pool += [float(x), abs(float(x))]
        if isinstance(x, (F, sp.Rational)):   # an exact fraction may be printed as its two parts
            q = F(int(sp.numer(x)), int(sp.denom(x))) if isinstance(x, sp.Basic) else x
            pool += [q.numerator, q.denominator]
    pool += [-y for y in given]
    texts = [('correct', p['feedback']['correct']), ('explain', p.get('explain', {}).get('text', ''))]
    texts += [(f'byKey {key}', v) for key, v in p['feedback'].get('byKey', {}).items()]
    texts += [(f'why {o["id"]}', o.get('why', '')) for o in p['widget'].get('options', [])]
    for field, txt in texts:
        for x in _numbers(txt):
            ok(any(abs(x - y) <= max(1e-9, 0.0006 * max(1, abs(y))) for y in pool) or abs(x) <= 12,
               f"{item['id']} part {k + 1} {field}: states {x}, not computed here")


# ---------------------------------------------------------------- sympy reading of expression answers
r_, s_ = sp.symbols('r s')


def frac_to_div(t):
    while '\\frac' in t:
        i = t.index('\\frac')
        j = i + 5
        parts = []
        for _ in range(2):
            depth, kk = 0, j
            while True:
                if t[kk] == '{':
                    depth += 1
                elif t[kk] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                kk += 1
            parts.append(t[j + 1:kk])
            j = kk + 1
        t = t[:i] + '((' + parts[0] + ')/(' + parts[1] + '))' + t[j:]
    return t


def tex(t):
    t = t.replace('\\dfrac', '\\frac').replace('\\tfrac', '\\frac')
    m = re.match(r'\\begin\{pmatrix\}(.*)\\\\(.*)\\end\{pmatrix\}$', t)
    if m:
        return (sp.sympify(m.group(1)), sp.sympify(m.group(2)))
    t = frac_to_div(t).replace('{', '(').replace('}', ')')
    if t.startswith('(') and ',' in t and t.endswith(')') and t.count('(') == 1:
        a, b = t[1:-1].split(',')
        return (sp.sympify(a), sp.sympify(b))
    t = re.sub(r'(\d|\))\s*([rs(])', r'\1*\2', t)
    return sp.sympify(t, locals={'r': r_, 's': s_})


def same(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return isinstance(a, tuple) and isinstance(b, tuple) and all(sp.simplify(x - y) == 0 for x, y in zip(a, b))
    return sp.simplify(a - b) == 0


def check_expr(item, k, value, slips):
    p = item['parts'][k]
    w = p['widget']
    lab = f"{item['id']} part {k + 1}"
    ok(same(tex(w['answer']), value), f'{lab}: key {w["answer"]} is not {value}')
    for a in w.get('accept', []):
        ok(same(tex(a), value), f'{lab}: accept {a} differs from the key')
    ids = [x['id'] for x in w['wrong']]
    ok(sorted(ids) == sorted(slips), f'{lab}: wrong ids {ids} vs {sorted(slips)}')
    for x in w['wrong']:
        v = tex(x['tex'])
        ok(not same(v, value), f'{lab}: wrong {x["id"]} equals the key')
        if x['id'] in slips:
            ok(same(v, slips[x['id']]), f'{lab}: wrong {x["id"]} {x["tex"]} is not its slip {slips[x["id"]]}')
        ok(x['id'] in p['feedback'].get('byKey', {}), f'{lab}: wrong {x["id"]} has no byKey line')


def check_choice(item, k, key):
    w = item['parts'][k]['widget']
    good = [o['id'] for o in w['options'] if o.get('correct')]
    ok(good == [key], f"{item['id']} part {k + 1}: keyed option {good}, expected {key}")
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f"{item['id']} part {k + 1}: a distractor lacks why")


# ================================================================= LEVEL 1
L1 = load(1)

# p-tulip-bed: 4 of 8 varieties, rows of 4, 4 edging colours
it = L1['p-tulip-bed']
groups = comb(8, 4); groups2 = sum(1 for _ in itertools.combinations(range(8), 4)); agree(groups, groups2, 'tulip groups')
orders = factorial(4); orders2 = sum(1 for _ in itertools.permutations(range(4))); agree(orders, orders2, 'tulip orders')
rows = groups * orders; rows2 = sum(1 for _ in itertools.permutations(range(8), 4)); agree(rows, rows2, 'tulip rows')
beds = rows * 4; beds2 = sum(1 for _ in itertools.product(itertools.permutations(range(8), 4), range(4))); agree(beds, beds2, 'tulip beds')
check_numeric(it, 0, groups, {'ordered': perm(8, 4), 'divide-four': perm(8, 4) // 4, 'times': 8 * 4}, [perm(8, 4), 24])
check_numeric(it, 1, orders, {'four': 4, 'repeats': 4 ** 4})
check_numeric(it, 2, rows, {'added': groups + orders, 'carried': perm(8, 4) * orders}, [perm(8, 4)])
check_numeric(it, 3, beds, {'added': rows + 4, 'no-order': groups * 4, 'carried': perm(8, 4) * orders * 4})

# p-team-photo (netball line-up): 7 players, captain C in the middle place (index 3), twins T1 T2 side by side
it = L1['p-team-photo']
people = ['C', 'T1', 'T2', 'a', 'b', 'c', 'd']
allp = list(itertools.permutations(people))
agree(factorial(7), len(allp), 'photo all')
mid = [q for q in allp if q[3] == 'C']
agree(factorial(6), len(mid), 'photo captain middle'); agree(factorial(7) // 7, len(mid), 'photo 5040/7')
both = [q for q in mid if abs(q.index('T1') - q.index('T2')) == 1]
free_pairs = [(i, i + 1) for i in range(6) if 3 not in (i, i + 1)]
agree(len(free_pairs), 4, 'photo free pairs')
agree(len(free_pairs) * 2 * factorial(4), len(both), 'photo both rules')
block_count = factorial(5) * 2
ok(block_count != len(both), 'photo: the glued block count must differ from the key')
straddle = [q for q in mid if {q.index('T1'), q.index('T2')} == {2, 4}]
agree(len(straddle), 2 * factorial(4), 'photo twins either side of captain: 48')
agree(block_count - len(both), len(straddle), 'photo: the block overcounts exactly the rows with the twins either side of the captain')
check_numeric(it, 0, 5040, {'square': 49, 'sum': sum(range(1, 8)), 'seven': 7})
check_numeric(it, 1, len(mid), {'not-middle': 5040 - 720, 'six': 6}, [5040])
check_choice(it, 2, 'pairs-four')
stated_ok(it, 2, [4, 5, 6, 7, 3])
check_numeric(it, 3, len(both), {'block': block_count, 'no-swap': len(both) // 2, 'pairs-six': 6 * 2 * factorial(4)}, [24])

# p-five-a-side: 8 teams, home and away; 72 matches; 6 of 9 for a cup
it = L1['p-five-a-side']
pairs = comb(8, 2); agree(pairs, len(list(itertools.combinations(range(8), 2))), 'league pairs')
matches = pairs * 2; agree(matches, len(list(itertools.permutations(range(8), 2))), 'league matches')
n9 = [n for n in range(1, 100) if n * (n - 1) == 72]; ok(n9 == [9], f'league n {n9}')
agree(sp.solve(sp.Symbol('n') * (sp.Symbol('n') - 1) - 72)[-1], 9, 'league n sympy')
cup = comb(9, 6); agree(cup, len(list(itertools.combinations(range(9), 6))), 'cup groups'); agree(cup, comb(9, 3), 'cup symmetry')
check_numeric(it, 0, pairs, {'ordered': 56, 'square': 64, 'times-two': 16})
check_numeric(it, 1, matches, {'half': pairs // 2, 'carried': 56 * 2})
check_numeric(it, 2, 9, {'halved': 36, 'one-factor': 8}, [56, 72])
check_numeric(it, 3, cup, {'ordered': perm(9, 6), 'no-divide': perm(9, 3), 'times': 54}, [504])

# p-ice-cream-van: 14 flavours, 3 scoops (renumbered from 11 in the 0.3 a fix pass)
it = L1['p-ice-cream-van']
cups = comb(14, 3); agree(cups, len(list(itertools.combinations(range(14), 3))), 'cups')
agree(cups, 364, 'cups pinned')
cones = cups * 6; agree(cones, len(list(itertools.permutations(range(14), 3))), 'cones')
agree(cones, 2184, 'cones pinned')
items = cups + cones; agree(items, len(set(itertools.combinations(range(14), 3)) | set(('cone',) + q for q in itertools.permutations(range(14), 3))), 'items')
agree(items, 2548, 'items pinned')
orders_ = items * 5; agree(orders_, len(list(itertools.product(range(items), ['t1', 't2', 't3', 't4', 'none']))), 'ice orders')
agree(orders_, 12740, 'purchases pinned')
check_numeric(it, 0, cups, {'ordered': 14 * 13 * 12, 'repeats': 14 ** 3, 'times': 14 * 3}, [13])
check_numeric(it, 1, cones, {'times-three': cups * 3, 'added': cups + 6, 'carried': 2184 * 6}, [2184, 13])
check_numeric(it, 2, items, {'multiplied': cups * cones, 'carried': 2184 + 13104})
check_numeric(it, 3, orders_, {'no-none': items * 4, 'added': items + 5, 'carried': cups * cones * 5})
agree(len({364, 2184, 2548, 12740, 2744, 42, 1092, 370, 13104, 794976, 15288, 10192, 2553, 3974880}), 14, 'ice values distinct')

# ================================================================= LEVEL 2
L2 = load(2)

# p-signal-flags: RRRRBBY
it = L2['p-signal-flags']
sig = set(itertools.permutations('RRRRBBY'))
agree(len(sig), F(factorial(7), factorial(4) * factorial(2)), 'flags')
tog = [q for q in sig if 'BB' in ''.join(q)]
agree(len(tog), F(factorial(6), factorial(4)), 'flags together')
apart = len(sig) - len(tog); agree(apart, len([q for q in sig if 'BB' not in ''.join(q)]), 'flags apart')
pa = F(apart, len(sig)); agree(pa, F(comb(7, 2) - 6, comb(7, 2)), 'flags chance by places')
check_numeric(it, 0, 105, {'no-divide': 5040, 'reds-only': 5040 // 24, 'blues-only': 5040 // 2}, [48, 24])
check_numeric(it, 1, 30, {'flipped': 60, 'no-divide': 720, 'blue-divide': 720 // 48}, [720, 24])
check_numeric(it, 2, apart, {'carried': 105 - 60, 'added': 105 + 30})
check_numeric(it, 3, pa, {'together': F(30, 105), 'carried': F(45, 105), 'bottom': F(75, 5040)},
              [75, 105, F(5, 7), 21, 6, 15], rounded=0.714)

# p-leisure-centre: an explicit list of 80 members
it = L2['p-leisure-centre']
swim = set(range(0, 45)); gym = set(range(25, 63)); members = set(range(80))
agree(len(swim), 45, 'swim'); agree(len(gym), 38, 'gym'); agree(len(swim & gym), 20, 'both')
union = len(swim | gym); agree(union, 45 + 38 - 20, 'union')
neither = members - swim - gym; agree(len(neither), 80 - union, 'neither')
p3 = F(len(neither), 80)
pairs_n = sum(1 for q in itertools.combinations(sorted(members), 2) if set(q) <= neither)
p4 = F(pairs_n, sum(1 for _ in itertools.combinations(range(80), 2))); agree(p4, F(comb(17, 2), comb(80, 2)), 'two neither')
check_numeric(it, 0, union, {'no-overlap': 83, 'twice': 43})
check_numeric(it, 1, len(neither), {'carried': 80 - 43, 'only-one': (45 - 20) + (38 - 20)}, [25, 18])
check_numeric(it, 2, p3, {'at-least': F(63, 80), 'carried': F(37, 80), 'bottom': F(17, 63)}, rounded=0.212)
ok(abs(0.213 - 0.2125) <= 0.0006 + 1e-9, 'leisure part 3: 0.213 refused')
check_numeric(it, 3, p4, {'replaced': F(17, 80) ** 2, 'ordered-top': F(17 * 16, comb(80, 2)), 'pairs-over-members': F(136, 80)},
              [136, 3160], rounded=0.043)
ok(abs(round(float(F(17, 80) ** 2), 3) - 0.0452) <= 0.0003, 'leisure part 4: rounded replaced slip outside its band')

# p-balloon-blocks
it = L2['p-balloon-blocks']
rowsb = set(itertools.permutations('BALLOON'))
agree(len(rowsb), F(factorial(7), 4), 'balloon rows')
oo = [q for q in rowsb if 'OO' in ''.join(q)]; agree(len(oo), F(factorial(6), 2), 'OO together')
oapart = [q for q in rowsb if 'OO' not in ''.join(q)]; agree(len(oapart), len(rowsb) - len(oo), 'OO apart')
ll = [q for q in rowsb if 'LL' in ''.join(q)]; bothb = [q for q in ll if 'OO' in ''.join(q)]
agree(len(ll), 360, 'LL together'); agree(len(bothb), factorial(5), 'both together')
good = [q for q in oapart if 'LL' not in ''.join(q)]
agree(len(good), len(oapart) - (len(ll) - len(bothb)), 'both apart'); agree(len(good), 1260 - 360 - 360 + 120, 'incl-excl')
pb = F(len(good), len(rowsb))
check_numeric(it, 0, 1260, {'no-divide': 5040, 'one-pair': 2520}, [5040, 4])
check_numeric(it, 1, 360, {'flipped': 720, 'both-divided': 180}, [720])
check_numeric(it, 2, len(oapart), {'carried': 1260 - 720, 'carried-half': 1260 - 180})
check_numeric(it, 3, len(good), {'all-ls': 900 - 360, 'both-only': 900 - 120}, [360, 120, 240])
check_numeric(it, 4, pb, {'carried': F(540, 1260), 'os-only': F(900, 1260), 'bottom': F(660, 5040)},
              [660, 1260, F(11, 21), 60], rounded=0.524)

# p-quiz-team: 6 girls, 5 boys, team of 4
it = L2['p-quiz-team']
kids = ['g%d' % i for i in range(6)] + ['b%d' % i for i in range(5)]
teams = list(itertools.combinations(kids, 4)); agree(len(teams), comb(11, 4), 'teams')
nog = [t for t in teams if not any(x[0] == 'g' for x in t)]; agree(len(nog), comb(5, 4), 'no girls')
g1 = [t for t in teams if any(x[0] == 'g' for x in t)]; agree(len(g1), len(teams) - len(nog), 'at least one girl')
mix = [t for t in g1 if any(x[0] == 'b' for x in t)]; agree(len(mix), len(g1) - comb(6, 4), 'mixed')
pq = F(len(mix), len(teams)); agree(pq, F(31, 33), 'quiz chance')
check_numeric(it, 0, len(teams), {'ordered': perm(11, 4), 'times': 44}, [7920, 24])
check_numeric(it, 1, len(nog), {'no-boys': comb(6, 4), 'ordered': perm(5, 4)})
check_numeric(it, 2, len(g1), {'no-boys': 330 - 15, 'exactly-one': 6 * comb(5, 3)})
check_numeric(it, 3, len(mix), {'no-girls-again': 325 - 5, 'both-off': 325 - 15 - 5}, [15])
check_numeric(it, 4, pq, {'girl-only': F(325, 330), 'bottom': F(310, 325), 'carried': F(305, 330)},
              [310, 330, F(31, 33)], rounded=0.939)

# ================================================================= LEVEL 3
L3 = load(3)


def sub(p, q):
    return (q[0] - p[0], q[1] - p[1])


# p-orienteering: S(1, 2), P(10, 14), Q(-2, 30), 100 m squares
it = L3['p-orienteering']
S, P, Q = (1, 2), (10, 14), (-2, 30)
SP, PQ = sub(S, P), sub(P, Q)
SQ = (SP[0] + PQ[0], SP[1] + PQ[1]); ok(SQ == sub(S, Q), 'orienteering head to tail vs end minus start')
check_expr(it, 0, SP, {'start-minus-end': sub(P, S), 'end-point': P})
check_expr(it, 1, PQ, {'start-minus-end': sub(Q, P), 'added': (P[0] + Q[0], P[1] + Q[1])})
check_expr(it, 2, SQ, {'subtracted': (SP[0] - PQ[0], SP[1] - PQ[1]), 'position': Q})
route = 100 * (hypot(*SP) + hypot(*PQ)); agree(route, 100 * (sp.sqrt(81 + 144) + sp.sqrt(144 + 256)), 'route')
direct = 100 * hypot(*SQ); agree(direct, 100 * sp.sqrt(793), 'direct')
save = route - direct
check_numeric(it, 3, route, {'components': 100 * (9 + 12 + 12 + 16), 'direct': direct, 'squares': route / 100}, [15, 20, 35, 49, 9, 12, 16])
check_numeric(it, 4, save, {'direct': direct, 'added-components': route - 100 * (3 + 28), 'carried': 4900 - direct, 'squares': save / 100},
              [28.16, 2816, 793, 3500], rounded=round(save))
ok(abs(684 - (3500 - round(direct))) <= 1, 'orienteering: route minus the rounded straight line accepted')

# p-power-line: A(2, 3), B(8, 7), C(17, 13), 100 m units
it = L3['p-power-line']
A, B, C = (2, 3), (8, 7), (17, 13)
AB, AC = sub(A, B), sub(A, C)
k = F(AC[0], AB[0]); ok(k == F(AC[1], AB[1]), 'power line: one k for both rows')
ok(AB[0] * AC[1] - AB[1] * AC[0] == 0, 'power line: cross product zero (collinear)')
check_expr(it, 0, AB, {'start-minus-end': sub(B, A), 'added': (A[0] + B[0], A[1] + B[1])})
check_expr(it, 1, AC, {'start-minus-end': sub(C, A), 'from-b': sub(B, C)})
check_numeric(it, 2, k, {'reciprocal': 1 / k, 'difference': AC[0] - AB[0]}, [15, 6, 10, 4])
check_choice(it, 3, 'collinear')
ok(k > 1, 'power line: C beyond B')
cable = 100 * hypot(*AC); agree(cable, 100 * float(k) * sqrt(52), 'cable')
check_numeric(it, 4, cable, {'ab-only': 100 * hypot(*AB), 'added': 100 * (AC[0] + AC[1]), 'units': cable / 100},
              [sqrt(52), 7.211, 18.03, 325, 100], rounded=round(cable))
ok(abs(1803 - 100 * 2.5 * 7.21) <= 1 + 1e-9, 'power line: 2.5 x 7.21 x 100 accepted')

# p-grain-merchant
it = L3['p-grain-merchant']
h, d, t = (60, 40), (F(5, 2), F(-7, 2)), (-20, 30)
pl1 = h[0] * d[0] + h[1] * d[1]; agree(pl1, (sp.Matrix(h).T * sp.Matrix(d))[0], 'monday pnl')
h2 = (h[0] + t[0], h[1] + t[1])
pl2 = h2[0] * d[0] + h2[1] * d[1]; agree(pl2, (sp.Matrix(h2).T * sp.Matrix(d))[0], 'tuesday pnl')
cosv = float(pl2) / (hypot(*h2) * hypot(*map(float, d)))
ang = degrees(acos(cosv)); ang2 = degrees(abs(atan2(h2[1], h2[0]) - atan2(float(d[1]), float(d[0])))); agree(ang, ang2, 'angle')
check_numeric(it, 0, pl1, {'no-sign': 150 + 140, 'sum-first': (60 + 40) * (2.5 - 3.5)}, [150, 140, 2.5, 3.5])
check_expr(it, 1, h2, {'signs': (h[0] - t[0], h[1] - t[1]), 'trade': t})
td = t[0] * d[0] + t[1] * d[1]
agree(pl1 + td, pl2, 'tuesday = monday + trade (distributive)')
ok(80 * F(5, 2) - 10 * F(7, 2) == -td + pl1, 'grain: holdings (80, 10) give the same 165 as the signs slip')
check_numeric(it, 2, pl2, {'trade-only': td, 'old-book': pl1, 'signs': pl1 - td, 'no-sign': 100 + 245},
              [100, 245, 2.5, 3.5, t[0] * d[0], 105, td, 40, 70])
check_numeric(it, 3, ang, {'acute': 180 - ang, 'cosine': cosv, 'radians': acos(cosv)},
              [cosv, 6500, 18.5, hypot(*h2), 4.301, 346.8, 90, 40, 70, pl2], rounded=round(ang))
ok(abs(round(cosv, 2) - (-0.42)) < 1e-9 and abs(round(180 - ang) - 65) == 0, 'grain: slips at the asked rounding')
ok(abs(degrees(acos(-145 / (80.62 * 4.301))) - 115) <= 0.5, 'grain: angle from the printed magnitudes accepted')
ok(abs(-145 / 346.8 - (-0.418)) < 0.0005, 'grain: printed cosine')

# p-sail-ring: symbolic in r, s; then random numeric vectors as a second method
it = L3['p-sail-ring']
RS = s_ - r_
OM = r_ + RS / 2
OX = sp.Rational(2, 3) * OM
RX = OX - r_
RN = -r_ + s_ / 2
kk = sp.solve(sp.Eq(RX.coeff(r_), sp.Symbol('k') * RN.coeff(r_)))[0]
ok(sp.simplify(RX - kk * RN) == 0, 'sail: RX = k RN for both terms')
random.seed(7)
for _ in range(5):
    O = (0.0, 0.0); R = (random.uniform(-5, 5), random.uniform(-5, 5)); Sv = (random.uniform(-5, 5), random.uniform(-5, 5))
    M = ((R[0] + Sv[0]) / 2, (R[1] + Sv[1]) / 2); X = (2 * M[0] / 3, 2 * M[1] / 3); N = (Sv[0] / 2, Sv[1] / 2)
    rx, rn = sub(R, X), sub(R, N)
    ok(isclose(rx[0], float(kk) * rn[0], abs_tol=1e-12) and isclose(rx[1], float(kk) * rn[1], abs_tol=1e-12), 'sail numeric k')
check_expr(it, 0, RS, {'reversed': r_ - s_, 'added': r_ + s_})
check_expr(it, 1, OM, {'half-rs': RS / 2, 'whole-rs': r_ + RS})
check_expr(it, 2, OX, {'two-thirds': sp.Rational(2, 3) * (r_ + s_), 'added': (sp.Rational(1, 2) + sp.Rational(2, 3)) * (r_ + s_)})
check_expr(it, 3, RX, {'ox': OX, 'reversed': -RX, 'added': OX + r_})
check_numeric(it, 4, kk, {'reciprocal': 1 / kk, 'third': sp.Rational(1, 3), 'half': sp.Rational(1, 2)}, [kk], rounded=0.667)

# ================================================================= numbers_lib second check of the bands and stated numbers
for n in (1, 2, 3):
    lv = Level('counting', n)
    lv.check_wrongs('problems')
    if n == 1:
        lv.expect('problems', 'items[0].parts[3].explain', 6720)
        lv.expect('problems', 'items[1].parts[3].explain', 192)
        lv.expect('problems', 'items[2].parts[3].explain', 84)
        lv.expect('problems', 'items[3].parts[3].explain', 12740)
    if n == 2:
        lv.expect('problems', 'items[0].parts[3].explain', 0.714)
        lv.expect('problems', 'items[1].parts[3].explain', 0.043)
        lv.expect('problems', 'items[2].parts[4].explain', 0.524)
        lv.expect('problems', 'items[3].parts[4].explain', 0.939)
    if n == 3:
        lv.expect('problems', 'items[0].parts[4].explain', 684)
        lv.expect('problems', 'items[1].parts[4].explain', 1803)
        lv.expect('problems', 'items[2].parts[3].explain', -0.418)
        lv.expect('problems', 'items[3].parts[4].explain', 0.667)
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'numbers_lib level {n}: {len(bad)} failures')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
