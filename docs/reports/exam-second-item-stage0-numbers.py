"""Exam second item, stage0 (topic-0.3, topic-0.2, topic-0.4): every key, wrong value and printed number of the new items, twice.

Run: <scratchpad>/venv/bin/python docs/reports/exam-second-item-stage0-numbers.py   (exit 0 when all pass)
Route 1 is the working the item prints; route 2 is independent (brute force, exact fractions, simulation by enumeration,
the polynomial expanded term by term). The script also recomputes the (exam, skill) pairs and checks that no skill of
the exam has fewer than two auto items.
"""
import json, math, os, re, sys, glob, itertools, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

CONTENT = os.path.join(HERE, '..', '..', 'app', 'content')
fails, n = [], [0]


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def band(t):
    return t.get('abs', 0) if isinstance(t, dict) else t


def load(e):
    doc = json.load(open(os.path.join(CONTENT, 'exams', e + '.json'), encoding='utf8'))
    return doc, {i['id']: i for i in doc['items']}


def numeric(where, it, key, wrongs, printed=()):
    w, fb = it['widget'], it['feedback']
    a, t = w['answer'], band(w['tol'])
    check(abs(a - key) <= max(t, 1e-9), f'{where} key {a} = computed {key}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{where} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(abs(x['value'] - v) <= band(x['tol']) + 1e-9, f'{where} wrong {k} {x["value"]} = slip {v}')
        check(abs(x['value'] - a) > t + band(x['tol']), f'{where} wrong {k} outside the key band')
        check(k in fb['byKey'], f'{where} wrong {k} has a byKey line')
    for k1, k2 in itertools.combinations(got, 2):
        x, y = got[k1], got[k2]
        check(abs(x['value'] - y['value']) > band(x['tol']) + band(y['tol']), f'{where} wrongs {k1}, {k2} do not overlap')
    check(any(abs(x - a) <= max(t, 1e-9) for x in _numbers(it['explain']['text'])), f'{where} explanation states the key')
    for txt, val in printed:
        check(abs(val - txt) < 1e-9, f'{where} printed {txt} = {val}')


def auto_floor(e):
    """Every skill of the exam on at least two auto items; list the (exam, level, skill) triples with one."""
    doc, _ = load(e)
    cnt = collections.Counter()
    for it in doc['items']:
        if it.get('kind') == 'longform' or it.get('widget', {}).get('kind') == 'longform':
            continue
        for s in it['skills']:
            cnt[s] += 1
    low = [s for s in doc['skills'] if cnt[s] < 2]
    check(not low, f'{e} every skill has two or more auto items (low: {low})')
    trip = []
    for cf in sorted(glob.glob(os.path.join(CONTENT, 'courses', '*', 'course.json'))):
        c = json.load(open(cf, encoding='utf8'))
        if c.get('topic') != doc['topic']:
            continue
        for lv in c['levels']:
            rf = os.path.join(os.path.dirname(cf), lv['review'] + '.json')
            if os.path.exists(rf):
                ess = {s for it in json.load(open(rf, encoding='utf8'))['items'] for s in it.get('skills', [])}
                trip += [(c['id'], lv['n'], s) for s in ess if cnt[s] < 2]
    check(not trip, f'{e} no level essential skill with one auto item (left: {trip})')
    return cnt


def ramp(e):
    doc, _ = load(e)
    c = collections.Counter(i['difficulty'] for i in doc['items'])
    N = len(doc['items'])
    for d, share in ((2, .2), (3, .5), (4, .2), (5, .1)):
        check(abs(c[d] / N - share) <= 0.1, f'{e} difficulty {d}: {c[d]} of {N} within 10 points of {share:.0%}')
    return N


# ================= topic-0.3 =================
doc, it = load('topic-0.3')

# e-desk-meetings: pairs of 9 desks
r1 = math.comb(9, 2)
r2 = sum(1 for a, b in itertools.combinations(range(9), 2))
check(r1 == r2 == 36, 'e-desk-meetings C(9,2) = 36 by formula and by listing pairs')
ordered = sum(1 for a, b in itertools.permutations(range(9), 2))
numeric('e-desk-meetings', it['e-desk-meetings'], r1,
        {'ordered': ordered, 'self': 9 * 9, 'one-desk': 8}, printed=[(9 * 8 / 2, 36), (9 * 8, 72)])

# e-double-angle-roots: sin 2x = sin x on [0, 360)
sol1 = sorted({0, 180} | {60, 300})   # sin x = 0 or cos x = 1/2
grid = [x / 100 for x in range(0, 36000)]
sol2 = sorted({round(x) for x in grid if abs(math.sin(math.radians(2 * x)) - math.sin(math.radians(x))) < 1e-9})
check(sol1 == sol2 == [0, 60, 180, 300], f'e-double-angle-roots solutions {sol2} by factor and by scan')
w = it['e-double-angle-roots']['widget']
check(sorted(w['answers']) == sol1, 'e-double-angle-roots answers match')
sine_pair = sorted({0, 180, 60, 180 - 60})        # cos x = 1/2 solved as sine: 60, 120
sin_half = sorted({0, 180, 30, 150})              # sin x = 1/2 instead of cos x = 1/2
for wid, slip in (('sine-pair', sine_pair), ('sin-half', sin_half)):
    vals = sorted(float(v) for v in next(x for x in w['wrong'] if x['id'] == wid)['value'].split(','))
    check(vals == slip and vals != sol1 and len(vals) == 4, f'e-double-angle-roots wrong {wid} {vals}')
check(abs(math.cos(math.radians(120)) + 0.5) < 1e-12, 'cos 120 = -1/2 (why the sine pair fails)')
check(abs(math.cos(math.radians(300)) - 0.5) < 1e-12, 'cos 300 = 1/2')
check(all(abs(math.sin(math.radians(2 * x)) - math.sin(math.radians(x))) > 1e-3 for x in (120, 30, 150)), 'slip angles do not solve it')
check(360 - 60 == 300 and 180 - 60 == 120, 'printed 360 - 60 = 300 and 180 - 60 = 120')

# e-parallelogram-midpoint: O, A(4,1), C(1,3), B = A + C, M midpoint BC
A_, C_ = (F(4), F(1)), (F(1), F(3))
B_ = (A_[0] + C_[0], A_[1] + C_[1])
M_ = ((B_[0] + C_[0]) / 2, (B_[1] + C_[1]) / 2)
AM = (M_[0] - A_[0], M_[1] - A_[1])
L2 = AM[0] ** 2 + AM[1] ** 2
check(B_ == (5, 4) and M_ == (3, F(7, 2)) and AM == (-1, F(5, 2)) and L2 == F(29, 4), 'e-parallelogram-midpoint B, M, AM, |AM|^2 = 7.25 exact')
L_route2 = math.hypot(3 - 4, 3.5 - 1)            # route 2: M = C + (B - C)/2 by floats
L_route2b = math.dist((4, 1), (1 + (5 - 1) / 2, 3 + (4 - 3) / 2))
check(abs(L_route2 - math.sqrt(7.25)) < 1e-12 and abs(L_route2b - L_route2) < 1e-12, 'e-parallelogram-midpoint length twice')
Bm = (A_[0] - C_[0], A_[1] - C_[1]); Mm = ((Bm[0] + C_[0]) / 2, (Bm[1] + C_[1]) / 2)
b_minus = math.dist((4, 1), (float(Mm[0]), float(Mm[1])))
om = math.hypot(float(M_[0]), float(M_[1]))
numeric('e-parallelogram-midpoint', it['e-parallelogram-midpoint'], math.sqrt(7.25),
        {'b-minus': b_minus, 'om': om, 'no-root': 7.25},
        printed=[(1 + 6.25, 7.25), (round(math.sqrt(7.25), 2), 2.69), (round(b_minus, 2), 2.06), (round(om, 2), 4.61)])
check(abs(it['e-parallelogram-midpoint']['widget']['answer'] - math.sqrt(7.25)) < 1e-6, 'stored key is sqrt 7.25 to 6 places')

# e-rebate-third: a = 18, S = 30
r = 1 - F(18, 30)
check(r == F(2, 5), 'e-rebate-third r = 0.4 from 18/(1-r) = 30')
# route 2: search r on a fine grid for the partial sums to approach 30
r_scan = min((k / 10000 for k in range(1, 10000)), key=lambda q: abs(18 / (1 - q) - 30))
check(abs(r_scan - 0.4) < 1e-9, 'e-rebate-third r by scan')
t3 = 18 * r ** 2
tail = 30 - 18 - 18 * r
check(t3 == F(72, 25) and abs(sum(18 * 0.4 ** k for k in range(2, 400)) - float(tail)) < 1e-9, 'e-rebate-third third term 2.88, tail 4.8 by summing')
numeric('e-rebate-third', it['e-rebate-third'], float(t3),
        {'ratio-flip': 18 * 0.6 ** 2, 'second': 18 * 0.4, 'tail': float(tail)},
        printed=[(18 / 30, 0.6), (1 - 0.6, 0.4), (18 * 0.4 ** 2, 2.88), (30 - 18 - 7.2, 4.8)])

# e-coefficients-in-step: C(n,1), C(n,2), C(n,3) arithmetic
ap = [k for k in range(3, 200) if 2 * math.comb(k, 2) == k + math.comb(k, 3)]
roots = sorted(int(x) for x in ((9 + math.sqrt(81 - 56)) / 2, (9 - math.sqrt(81 - 56)) / 2))
check(ap == [7] and roots == [2, 7], f'e-coefficients-in-step n by search {ap} and roots of n^2-9n+14 {roots}')
check(2 * math.comb(2, 2) == 2 + math.comb(2, 3), 'n = 2 also satisfies it (coefficients 2, 1, 0): the n > 2 condition is needed')
coef = [math.comb(7, k) for k in (1, 2, 3)]
check(coef == [7, 21, 35] and coef[1] - coef[0] == coef[2] - coef[1] == 14, 'coefficients 7, 21, 35 step 14')
# route 2: expand (1+x)^7 by repeated multiplication
p = [1]
for _ in range(7):
    p = [a + b for a, b in zip(p + [0], [0] + p)]
check(p[1:4] == [7, 21, 35], 'expansion of (1+x)^7 term by term')
numeric('e-coefficients-in-step', it['e-coefficients-in-step'], 7, {'small-root': 2})

# swap: e-sigma-odd removed (seq-sums keeps e-weekly-savings and e-loan-payment)
check('e-sigma-odd' not in it, 'e-sigma-odd removed')
cnt = auto_floor('topic-0.3')
check(cnt['seq-sums'] == 2, f'seq-sums keeps 2 auto items ({cnt["seq-sums"]})')
N = ramp('topic-0.3')
check(N == 30 and doc['minutes'] == 5 * round(60 * 30 / 26 / 5) == 70, f'topic-0.3 30 items, minutes 60 x 30/26 = {60 * 30 / 26:.1f} -> 70')

# ================= topic-0.2 =================
doc, it = load('topic-0.2')

# e-read-the-change: f(x) = x^2 - 1, g(x) = 2 f(x - 2)
f = lambda x: x * x - 1
g = lambda x: 2 * (x - 2) ** 2 - 2                # the dashed curve as drawn
opts = {'a': lambda x: 2 * f(x - 2), 'b': lambda x: 2 * f(x + 2), 'c': lambda x: f(x - 2) - 1, 'd': lambda x: f(2 * (x - 2))}
xs = [k / 10 for k in range(-40, 61)]
match = [k for k, h in opts.items() if all(abs(h(x) - g(x)) < 1e-9 for x in xs)]
check(match == ['a'], f'e-read-the-change only option a matches the dashed curve ({match})')
w = it['e-read-the-change']['widget']
check([o['id'] for o in w['options'] if o.get('correct')] == ['a'], 'e-read-the-change key is option a')
canvas_g = next(fn for fn in it['e-read-the-change']['canvas']['params']['functions'] if fn['id'] == 'g')['expr']
check(canvas_g.replace(' ', '') == '2*(x-2)^2-2', 'canvas draws g(x) = 2(x - 2)^2 - 2')
gmin = min(xs, key=g)
check((gmin, g(gmin)) == (2, -2) and g(1) == 0 and g(3) == 0, 'g lowest point (2, -2), roots 1 and 3 (printed in the prose)')
check(f(-1) == 0 and f(1) == 0 and min(f(x) for x in xs) == -1, 'f roots -1 and 1, lowest -1')
c_roots = sorted((2 - math.sqrt(2), 2 + math.sqrt(2)))
check(all(abs(opts['c'](x)) < 1e-12 for x in c_roots) and min(opts['c'](x) for x in xs) == -2, 'option c: lowest -2, roots 2 +- sqrt 2')
check(min(opts['d'](x) for x in xs) == -1, 'option d: lowest point at -1')
check(min(xs, key=opts['b']) == -2, 'option b: lowest point at x = -2 (left)')

# e-two-rates: 10000 (1 + r)(1 + 2r) = 11872
disc = 9 + 8 * 0.1872
check(abs(disc - 10.4976) < 1e-12 and abs(math.sqrt(disc) - 3.24) < 1e-12, 'discriminant 10.4976, root 3.24')
rr = sorted(((-3 + 3.24) / 4, (-3 - 3.24) / 4))
check(abs(rr[1] - 0.06) < 1e-12 and abs(rr[0] + 1.56) < 1e-12, 'roots 0.06 and -1.56')
# route 2: exact fractions and a direct product
check(F(10000) * (1 + F(6, 100)) * (1 + F(12, 100)) == 11872, '10000 x 1.06 x 1.12 = 11872 exactly')
check(abs(10000 * (1 - 1.56) * (1 - 3.12) - 11872) < 1e-6, 'r = -1.56 also solves the product (the rejected root)')
one_rate = math.sqrt(1.1872) - 1
numeric('e-two-rates', it['e-two-rates'], 0.06,
        {'simple': 0.1872 / 3, 'one-rate': one_rate, 'other-root': -1.56},
        printed=[((-3 + 3.24) / 4, 0.06), (2 * 0.06, 0.12)])
check(it['e-two-rates']['widget']['unit'] == '%', 'e-two-rates unit % with the key as a fraction')

# swaps: e-two-roots and e-formula removed
check('e-two-roots' not in it and 'e-formula' not in it, 'e-two-roots and e-formula removed')
cnt = auto_floor('topic-0.2')
check(cnt['quad-factor'] >= 2 and cnt['quad-solve'] >= 2, f'quad-factor {cnt["quad-factor"]}, quad-solve {cnt["quad-solve"]} keep two or more')
N = ramp('topic-0.2')
check(N == 30 and doc['minutes'] == 75, 'topic-0.2 still 30 items and 75 minutes')

# ================= topic-0.4 =================
doc, it = load('topic-0.4')

# e-left-hand-commands: home-row columns (terminal l1-home-row: left index takes R F V and T G B)
left_cols = ['QAZ', 'WSX', 'EDC', 'RFV', 'TGB']
right_cols = ['YHN', 'UJM', 'IK', 'OL', 'P']
LEFT = set(''.join(left_cols)); RIGHT = set(''.join(right_cols))
check(not (LEFT & RIGHT) and len(LEFT | RIGHT) == 26, 'the two hands split the 26 letters with no overlap')
keyboard_rows = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']   # route 2: left hand = first five keys of each row
LEFT2 = {c for r in keyboard_rows for c in r[:5]}
check(LEFT == LEFT2, 'left-hand letters by columns = first five keys of each row')
w = it['e-left-hand-commands']['widget']
for o in w['options']:
    word = o['text'].strip('`').upper()
    only_left = set(word) <= LEFT
    check(only_left == bool(o.get('correct')), f'e-left-hand-commands {word}: left hand only = {only_left}')
    if not only_left:
        rk = sorted(set(word) & RIGHT)
        check(len(rk) == 1 and rk[0] in o['why'].replace('semicolon', ''), f'{word} needs one right-hand key, {rk}, named in its why')
check(sum(1 for o in w['options'] if o.get('correct')) == 3, 'three correct options (the other multi items have two)')
check('H' in right_cols[0] and 'U' in right_cols[1] and 'P' in right_cols[4], 'H in Y H N, U in U J M, P in the right little finger column')

cnt = auto_floor('topic-0.4')
check(cnt['tm-typing'] == 2, f'tm-typing now on 2 auto items ({cnt["tm-typing"]})')
N = ramp('topic-0.4')
check(N == 21 and doc['minutes'] == 5 * round(60 * 21 / 20 / 5) == 65, f'topic-0.4 21 items, minutes 60 x 21/20 = {60 * 21 / 20:.0f} -> 65')

print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
