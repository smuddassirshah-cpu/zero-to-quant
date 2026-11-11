"""Recompute every number in app/content/courses/functions/problems-4.json twice.

Set 4 only (sets 1 to 3 are in problems-functions-numbers.py). Same checks as that script:
method 1 is exact (sympy: solve, expand, substitution, inverse by solving y = f(x); or fractions);
method 2 is independent (the machines run step by step in floats, undoing a machine step by step,
a brute search over whole numbers or a fine grid, or bisection). For each numeric part the two
methods agree; the JSON key lies within its tol of the value; the number printed last in
`feedback.correct` is accepted; every `wrong` value matches its named slip, has a byKey line, lies
outside the key's band and does not overlap another `wrong`. Numeric sets check both values two ways
and every wrong set against its slip. Expression parts check the key and every accepted form against
the sympy truth and every wrong form against it (and that no two wrong forms are equal). Choice parts
check the keyed option and the numbers stated in each `why`. numbers_lib.Level.check_wrongs runs over
the set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-functions-4-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
PATH = os.path.join(ROOT, 'app', 'content', 'courses', 'functions', 'problems-4.json')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
x, t, n, b, v = sp.symbols('x t n b v')
DOC = json.load(open(PATH))
L = {it['id']: it for it in DOC['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def printed_value(text):
    """The number after the last '=' or '\\approx' in a feedback line."""
    s = text.replace('{,}', '').replace('\\,', '').replace('−', '-')
    hits = list(re.finditer(r'(=|\\approx)\s*(-?\d+(?:\.\d+)?)', s))
    return float(hits[-1].group(2)) if hits else None


def num(iid, k, exact, alt, slips=None, agree=1e-9):
    part = L[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    ok(wd['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(abs(e - a) <= agree * max(1, abs(e)), f'{tag}: methods differ {e} vs {a}')
    tol = wd['tol']['abs']
    ok(abs(wd['answer'] - e) <= tol + 1e-12, f'{tag}: key {wd["answer"]} vs computed {e} (tol {tol})')
    ok(abs(wd['answer'] - e) <= 1e-9, f'{tag}: key {wd["answer"]} is not the exact value {e}')
    pv = printed_value(part['feedback']['correct'])
    ok(pv is not None and abs(pv - wd['answer']) <= tol + 1e-9, f'{tag}: printed {pv} not accepted by tol {tol}')
    slips = slips or {}
    wrongs = {z['id']: z for z in wd.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    bykey = part['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        z = wrongs[wid]
        wt = z.get('tol', {'abs': 0})['abs']
        ok(wid in bykey, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(z['value'] - float(val)) <= max(wt, 0.00005) + 1e-12, f'{tag}: wrong {wid} {z["value"]} vs slip {float(val)}')
        ok(abs(z['value'] - wd['answer']) > tol + wt, f'{tag}: wrong {wid} {z["value"]} inside the key band')
        ok(wt <= abs(z['value']) / 5, f'{tag}: wrong {wid} band {wt} wider than a fifth of its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A.get('tol', {'abs': 0})['abs'] + B.get('tol', {'abs': 0})['abs'],
           f'{tag}: wrongs {a_} and {b_} overlap')


def numset(iid, k, values, alt, slips=None):
    part = L[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    key = sorted(float(q) for q in values)
    ok(all(abs(p - q) <= 1e-9 for p, q in zip(key, sorted(float(q) for q in alt))), f'{tag}: methods differ {values} vs {alt}')
    ok(sorted(wd['answers']) == key, f'{tag}: key {wd["answers"]} vs {values}')
    ok(wd.get('unordered') is True, f'{tag}: not unordered')
    bykey = part['feedback'].get('byKey', {})
    ok('count' in bykey, f'{tag}: no byKey line for count')
    slips = slips or {}
    ok({z['id'] for z in wd.get('wrong', [])} == set(slips), f'{tag}: wrong ids vs slips {sorted(slips)}')
    for z in wd.get('wrong', []):
        vals = sorted(float(s) for s in z['value'].split(','))
        ok(vals != key, f'{tag}: wrong {z["id"]} equals the key')
        ok(z['id'] in bykey, f'{tag}: wrong {z["id"]} has no byKey line')
        if z['id'] in slips:
            ok(all(abs(p - q) < 1e-9 for p, q in zip(vals, sorted(float(s) for s in slips[z['id']]))),
               f'{tag}: wrong {z["id"]} {vals} vs slip {slips[z["id"]]}')


def pick(iid, k, correct_id):
    wd = L[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in wd['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')


def expr_part(iid, k, truth, tex):
    """tex: dict from every answer, accept and wrong text in the part to its sympy form."""
    part = L[iid]['parts'][k - 1]
    wd = part['widget']
    tag = f'{iid} p{k}'
    ok(wd['kind'] == 'expression', f'{tag}: not expression')
    for s in [wd['answer']] + wd.get('accept', []):
        ok(s in tex, f'{tag}: {s} not translated')
        if s in tex:
            ok(sp.simplify(tex[s] - truth) == 0, f'{tag}: {s} differs from the key')
    bykey = part['feedback'].get('byKey', {})
    seen = []
    for z in wd.get('wrong', []):
        ok(z['tex'] in tex, f'{tag}: wrong {z["tex"]} not translated')
        if z['tex'] in tex:
            ok(sp.simplify(tex[z['tex']] - truth) != 0, f'{tag}: wrong {z["id"]} equals the key')
            ok(all(sp.simplify(tex[z['tex']] - s_) != 0 for s_ in seen), f'{tag}: wrong {z["id"]} equals an earlier wrong')
            seen.append(tex[z['tex']])
        ok(z['id'] in bykey, f'{tag}: wrong {z["id"]} has no byKey line')


def stated(label, shown, value, tol=1e-9):
    ok(abs(float(shown) - float(value)) <= tol, f'stated {label}: {shown} vs {float(value)}')


def form_stated():
    for iid, it in L.items():
        for k, part in enumerate(it['parts'], 1):
            if part['widget']['kind'] == 'numeric':
                ok(re.search(r'decimal|places?|whole number|exact value|nearest|in pounds', part['question'], re.I) is not None,
                   f'{iid} p{k}: form not stated')


def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ------------------------------------------------------------------ p-photo-mount
e = lambda q: F(3, 2) * q
m = lambda q: q + 4
ef = lambda q: 1.5 * q
mf = lambda q: q + 4.0
num('p-photo-mount', 1, m(e(12)), mf(ef(12.0)), {'order': e(m(12)), 'one-side': e(12) + 2, 'no-enlarge': m(12)})
me = sp.Rational(3, 2) * x + 4
ok(sp.expand(me - (sp.Rational(3, 2) * x + 4)) == 0 and me.subs(x, 12) == 22, 'photo: m(e(x)) = 1.5x + 4, 22 at 12')
ok(all(abs(float(me.subs(x, q)) - mf(ef(q))) < 1e-12 for q in range(-20, 41)), 'photo: rule agrees with the machines at 61 inputs')
R = sp.Rational
expr_part('p-photo-mount', 2, me, {
    '1.5x+4': R(3, 2) * x + 4, '4+1.5x': 4 + R(3, 2) * x, '\\frac{3}{2}x+4': R(3, 2) * x + 4, '\\frac{3x}{2}+4': 3 * x / 2 + 4,
    '1.5(x+4)': R(3, 2) * (x + 4), '1.5x+2': R(3, 2) * x + 2})
stated('photo e(m(x)) = 1.5x + 6', 6, sp.expand(R(3, 2) * (x + 4)).subs(x, 0))
yy = sp.Symbol('y')
inv = sp.solve(sp.Eq(yy, me), x)[0].subs(yy, x)
ok(all(sp.simplify(inv.subs(x, me.subs(x, q)) - q) == 0 for q in (0, 3, 12, 18)), 'photo: inverse undoes f')
expr_part('p-photo-mount', 3, inv, {
    '\\frac{x-4}{1.5}': (x - 4) / R(3, 2), '\\frac{2(x-4)}{3}': 2 * (x - 4) / 3, '\\frac{2x-8}{3}': (2 * x - 8) / 3,
    '\\frac{2}{3}x-\\frac{8}{3}': R(2, 3) * x - R(8, 3), '\\frac{x}{1.5}-\\frac{4}{1.5}': x / R(3, 2) - 4 / R(3, 2),
    '\\frac{x}{1.5}-4': x / R(3, 2) - 4, '\\frac{x+4}{1.5}': (x + 4) / R(3, 2), '\\frac{1}{1.5x+4}': 1 / (R(3, 2) * x + 4)})
stated('photo f^-1(22) = 12', 12, inv.subs(x, 22))
w31 = inv.subs(x, 31)
brute = [q for q in range(0, 100) if mf(ef(q)) == 31]
num('p-photo-mount', 4, w31, (31 - 4) / 1.5, {'wrong-order': F(31) / F(3, 2) - 4, 'sign': F(35) / F(3, 2),
                                               'forward': e(31) + 4, 'times': F(27) * F(3, 2)})
ok(brute == [18], f'photo: brute search for 31 cm gives {brute}')
stated('photo 31 - 4 = 27', 27, 31 - 4)
stated('photo check 27 + 4', 31, e(18) + 4)
ok(e(31) / e(31) == 1 and F(31) / F(3, 2) - 4 == (F(31) - 6) / F(3, 2), 'photo: undoing in the wrong order is the inverse of e(m(x))')
num('p-photo-mount', 5, e(m(18)), ef(mf(18.0)), {'same': m(e(18)), 'mount-only': m(18), 'one-side': e(18 + 2)})
stated('photo 33 - 31 = 2 cm wider', 2, e(m(18)) - m(e(18)))
stated('photo m(18) = 22', 22, m(18))

# ------------------------------------------------------------------ p-fountain-jet
h = R(3, 20) * x * (12 - x)
hf = lambda q: 0.15 * q * (12 - q)
ok(sorted(sp.solve(h, x)) == [0, 12], 'fountain: leaves at 0 and lands at 12')
top = sp.solve(sp.diff(h, x), x)[0]
ok(top == 6, 'fountain: top at x = 6 by the derivative')
grid = max((hf(i / 1000), i / 1000) for i in range(0, 12001))
num('p-fountain-jet', 1, h.subs(x, 6), grid[0], {'no-bracket': F(3, 20) * 6 * 12, 'one-factor': F(3, 20) * 6, 'position': 6}, agree=1e-9)
ok(abs(grid[1] - 6) < 1e-9, 'fountain: grid top at 6')
pick('p-fountain-jet', 2, 'squeeze')
g = h.subs(x, R(4, 5) * x)
ok(sorted(sp.solve(g, x)) == [0, 15], 'fountain: h(0.8x) leaves at 0 and lands at 15')
ok(sp.maximum(g, x, sp.Interval(0, 15)) == R(27, 5), 'fountain: h(0.8x) keeps the top 5.4')
stated('fountain h(1.25x) lands at 9.6', 9.6, max(sp.solve(h.subs(x, R(5, 4) * x), x)))
ok(sorted(sp.solve(h.subs(x, x - 3), x)) == [3, 15], 'fountain: h(x - 3) leaves at 3 and lands at 15')
stated('fountain 1.25h top 6.75', 6.75, R(5, 4) * h.subs(x, 6))
ok(sorted(sp.solve(R(5, 4) * h, x)) == [0, 12], 'fountain: 1.25h(x) still lands at 12')
stated('fountain widths grow by 15/12 = 1.25', 1.25, F(15, 12))
stated('fountain b = 1/1.25 = 0.8', 0.8, 1 / F(5, 4))
gtop = sp.solve(sp.diff(g, x), x)[0]
gf = lambda q: hf(0.8 * q)
num('p-fountain-jet', 3, gtop, bisect(lambda q: 0.8 * q - 6, 0, 15), {'times': F(6) * F(4, 5), 'same': 6, 'slide': 9})
stated('fountain 6 x 1.25 = 7.5', 7.5, 6 * F(5, 4))
stated('fountain 7.5 halfway to 15', 7.5, F(15, 2))
ok(abs(max((gf(i / 1000), i / 1000) for i in range(0, 15001))[1] - 7.5) < 1e-9, 'fountain: grid top of the new jet at 7.5')
stated('fountain h(3) = 4.05', 4.05, h.subs(x, 3))
stated('fountain h(9) = 4.05', 4.05, h.subs(x, 9))
sols = sorted(sp.solve(sp.Eq(g, R(81, 20)), x))
up = bisect(lambda q: gf(q) - 4.05, 0, 7.5)
down = bisect(lambda q: gf(q) - 4.05, 7.5, 15)
numset('p-fountain-jet', 4, sols, [up, down], {'times': [2.4, 7.2], 'old': [3, 9], 'slide': [6, 12], 'top-plus-three': [4.5, 10.5]})
stated('fountain slip times', 2.4, 3 * F(4, 5))
stated('fountain slip times', 7.2, 9 * F(4, 5))
stated('fountain slip slide', 6, 3 + 3)
stated('fountain slip top-plus-three', 4.5, F(15, 2) - 3)
stated('fountain 3.75 from the top', 3.75, F(15, 2) - sols[0])
stated('fountain 3.75 from the top (down)', 3.75, sols[1] - F(15, 2))
stated('fountain 3 x 1.25', 3.75, 3 * F(5, 4))

# ------------------------------------------------------------------ p-car-park
C = sp.Piecewise((3, t <= 2), (3 + R(5, 2) * (t - 2), True))


def Cf(q):
    """the charge by the story: £3 covers 2 hours, then £2.50 for each hour after, in floats"""
    return 3.0 if q <= 2 else 3.0 + 2.5 * (q - 2)


num('p-car-park', 1, C.subs(t, R(9, 2)), Cf(4.5), {'no-free': 3 + F(5, 2) * F(9, 2), 'no-fee': F(5, 2) * F(5, 2), 'rate-only': F(5, 2) * F(9, 2)})
stated('car park extra time 2.5 h', 2.5, 4.5 - 2)
stated('car park 2.5 x 2.5 = 6.25', 6.25, 2.5 * 2.5)
rise = sp.expand(3 + R(5, 2) * (t - 2))
ok(rise == R(5, 2) * t - 2, 'car park: rising piece 2.5t - 2')
expr_part('p-car-park', 2, rise, {
    '2.5t-2': R(5, 2) * t - 2, '-2+2.5t': -2 + R(5, 2) * t, '\\frac{5}{2}t-2': R(5, 2) * t - 2, '\\frac{5t}{2}-2': 5 * t / 2 - 2,
    '2.5t+1': R(5, 2) * t + 1, '2.5t-5': R(5, 2) * t - 5, '2.5t+3': R(5, 2) * t + 3})
stated('car park check 11.25 - 2', 9.25, rise.subs(t, R(9, 2)))
stay = sp.solve(sp.Eq(rise, R(51, 4)), t)[0]
num('p-car-park', 3, stay, bisect(lambda q: Cf(q) - 12.75, 2, 20),
    {'sign': (F(51, 4) - 2) / F(5, 2), 'order': F(51, 4) / F(5, 2) + 2, 'carried': (F(51, 4) - 1) / F(5, 2),
     'forward': F(5, 2) * F(51, 4) - 2})
ok(stay > 2, 'car park: 5.9 lies on the rising piece')
stated('car park 12.75 + 2', 14.75, 12.75 + 2)
pick('p-car-park', 4, 'later')


def Nf(q):
    """the Monday price list in floats: £3 covers 3 hours, then £2.50 an hour"""
    return 3.0 if q <= 3 else 3.0 + 2.5 * (q - 3)


qs = [1 + i / 100 for i in range(1, 1500)]
ok(all(abs(Cf(q - 1) - Nf(q)) < 1e-9 for q in qs), 'car park: C(t - 1) is the Monday price for every stay over 1 hour')
ok(any(abs(Cf(q + 1) - Nf(q)) > 1e-9 for q in qs), 'car park: C(t + 1) is not')
ok(all(abs(Cf(q) - 2.5 - Nf(q)) < 1e-9 for q in qs if q > 3), 'car park: C(t) - 2.5 matches over 3 hours')
stated('car park C(t) - 2.5 on a short stay is 50p', 0.5, Cf(1.5) - 2.5)
ok(any(abs(Cf(q) + 1 - Nf(q)) > 1e-9 for q in qs), 'car park: C(t) + 1 is not the Monday price')
num('p-car-park', 5, rise.subs(t, stay - 1), Nf(5.9),
    {'earlier': F(5, 2) * F(69, 10) - 2, 'same': F(51, 4), 'outside': F(51, 4) - 1})
stated('car park 2.5 x 4.9 = 12.25', 12.25, F(5, 2) * F(49, 10))
stated('car park saving 2.50', 2.5, F(51, 4) - rise.subs(t, stay - 1))
stated('car park new rising piece 3 + 2.5(t - 3) at 5.9', 10.25, 3 + F(5, 2) * (F(59, 10) - 3))

# ------------------------------------------------------------------ p-ticket-bonus
Bv = sp.Max(R(1, 5) * (v - 500), 0)
Bf = lambda s: max(0.2 * (s - 500), 0.0)
Tn = lambda q: 25 * q
start = sp.solve(sp.Eq(25 * n, 500), n)[0]
num('p-ticket-bonus', 1, start, min(q for q in range(0, 1000) if Tn(q) >= 500), {'times': 500 * 25, 'next': 21})
ok(Bf(Tn(20)) == 0 and Bf(Tn(21)) > 0, 'bonus: £0 at 20 tickets and rising after')
stated('bonus 21 tickets bring 525', 525, Tn(21))
comp = sp.expand(R(1, 5) * (25 * n - 500))
ok(all(sp.simplify(Bv.subs(v, 25 * q) - comp.subs(n, q)) == 0 for q in range(21, 80)), 'bonus: B(T(n)) = 5n - 100 for n > 20')
ok(all(abs(Bf(Tn(q)) - (5 * q - 100)) < 1e-9 for q in range(21, 200)), 'bonus: floats agree on the rising piece')
expr_part('p-ticket-bonus', 2, comp, {
    '5n-100': 5 * n - 100, '-100+5n': -100 + 5 * n, '5(n-20)': 5 * (n - 20),
    '5n-2500': 25 * (R(1, 5) * (n - 500)), '5n-500': R(1, 5) * 25 * n - 500, '5n': R(1, 5) * 25 * n})
stated('bonus 0.2 x 500 = 100', 100, F(1, 5) * 500)
binv = sp.solve(sp.Eq(b, comp), n)[0]
expr_part('p-ticket-bonus', 3, binv, {
    '\\frac{b+100}{5}': (b + 100) / 5, '0.2b+20': R(1, 5) * b + 20, '\\frac{b}{5}+20': b / 5 + 20, '20+0.2b': 20 + R(1, 5) * b,
    '\\frac{1}{5}b+20': R(1, 5) * b + 20,
    '\\frac{b}{5}+100': b / 5 + 100, '\\frac{b-100}{5}': (b - 100) / 5, '\\frac{1}{5b-100}': 1 / (5 * b - 100)})
stated('bonus £60 needs 32 at 20%', 32, binv.subs(b, 60))
stated('bonus 5 x 32 - 100', 60, 5 * 32 - 100)
stated('bonus 30% / 20% = 1.5', 1.5, F(30, 100) / F(20, 100))
new = sp.solve(sp.Eq(R(3, 2) * comp, 60), n)[0]
brute = [q for q in range(0, 200) if abs(1.5 * Bf(Tn(q)) - 60) < 1e-9]
num('p-ticket-bonus', 4, binv.subs(b, F(60) / F(3, 2)), new,
    {'old-rate': binv.subs(b, 60), 'times': binv.subs(b, 60 * R(3, 2)), 'scaled': binv.subs(b, 60) / R(3, 2)})
ok(brute == [28], f'bonus: brute search at 30% gives {brute}')
stated('bonus 60 / 1.5 = 40', 40, F(60) / F(3, 2))
stated('bonus 140 / 5', 28, F(140, 5))
ok(all(1.5 * Bf(Tn(q)) == 0 for q in range(0, 21)), 'bonus: the stretched bonus still starts at 20 tickets')

# ------------------------------------------------------------------ the set
form_stated()
ok(DOC['id'] == 'problems-4' and DOC['level'] == 4 and DOC['course'] == 'functions', 'set header')
ok(3 <= len(DOC['items']) <= 5 and any(it['difficulty'] == 5 for it in DOC['items']), 'item count and a difficulty 5')
parts = [p for it in DOC['items'] for p in it['parts']]
typed = [p for p in parts if p['widget']['kind'] in ('numeric', 'expression')]
ok(3 * len(typed) >= 2 * len(parts), f'typed parts {len(typed)} of {len(parts)}')
ok(all(3 <= len(it['parts']) <= 5 for it in DOC['items']), 'three to five parts each')
for it in DOC['items']:
    for k, p in enumerate(it['parts'], 1):
        ex = p['explain']['text']
        sents = [s for s in re.split(r'(?<=[.?])\s+(?=[A-Z$0-9£])', ex) if s.strip()]
        ok(len(sents) <= 3, f'{it["id"]} p{k}: explain has {len(sents)} sentences')
lv = Level('functions', 4)
lv.check_wrongs('problems')
bad = [rr for rr in lv.results if not rr[0]]
ok(not bad, f'numbers_lib check_wrongs failures {bad}')

print(f'problems-functions-4: checks: {checks}; failures: {len(fails)}')
for msg in fails:
    print('FAIL', msg)
sys.exit(1 if fails else 0)
