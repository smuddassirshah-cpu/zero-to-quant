"""Second reader's own answers for counting problems 1 to 3 and functions problems 4.

Every counting answer is found by full enumeration (itertools) and again by formula with exact fractions.
Every `wrong` value is rebuilt from the slip its feedback names. Vector and function parts: sympy, then numbers.

Usage (repo root): <venv>/bin/python docs/reviews/problems-0.3-a-scripts/mine.py
Exit 0 when every check passes.
"""
import itertools as it
import json
import math
import sys
from fractions import Fraction as F
from math import comb, factorial as fact, perm

ROOT = 'app/content/courses/'
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def load(course, n):
    d = json.load(open(f'{ROOT}{course}/problems-{n}.json'))
    return {i['id']: i for i in d['items']}


def tolv(w):
    t = w.get('tol') or {}
    return t.get('abs', 0) if isinstance(t, dict) else 0


def part(items, pid, k, mine, wrongs=None, accept=(), reject=()):
    """mine: my value. wrongs: {id: value rebuilt from the slip}. accept/reject: typed values the band must take/refuse."""
    w = items[pid]['parts'][k - 1]['widget']
    lab = f'{pid}[{k}]'
    a, t = w['answer'], tolv(w)
    ok(abs(float(mine) - a) <= t + 1e-12, f'{lab} mine {float(mine)} vs key {a} tol {t}')
    for v in accept:
        ok(abs(float(v) - a) <= t + 1e-12, f'{lab} should accept {v}')
    for v in reject:
        ok(abs(float(v) - a) > t + 1e-12, f'{lab} should reject {v}')
    have = {x['id']: x for x in w.get('wrong', [])}
    for x in have.values():
        ok(abs(x['value'] - a) > t + tolv(x) - 1e-12, f'{lab} wrong {x["id"]} band overlaps the answer band')
    for wid, v in (wrongs or {}).items():
        if wid not in have:
            ok(False, f'{lab} no wrong id {wid}')
            continue
        x = have[wid]
        ok(abs(float(v) - x['value']) <= max(tolv(x), 5e-5) + 1e-12, f'{lab} wrong {wid}: slip gives {float(v)}, file {x["value"]}')
    missing = set(have) - set(wrongs or {})
    ok(not missing, f'{lab} wrong ids not rebuilt: {sorted(missing)}')


# ---------------------------------------------------------------- counting 1
c1 = load('counting', 1)

# tulip bed: choose 4 of 8, order them, 4 edging colours
groups = list(it.combinations(range(8), 4))
rows = list(it.permutations(range(8), 4))
ok(len(groups) == comb(8, 4) == 70 and len(rows) == perm(8, 4) == 1680, 'tulip enumerations')
part(c1, 'p-tulip-bed', 1, len(groups), {'ordered': 8 * 7 * 6 * 5, 'divide-four': 1680 // 4, 'times': 8 * 4})
part(c1, 'p-tulip-bed', 2, len(list(it.permutations(range(4)))), {'four': 4, 'repeats': 4 ** 4})
part(c1, 'p-tulip-bed', 3, len(rows), {'added': 70 + 24, 'carried': 1680 * 24})
part(c1, 'p-tulip-bed', 4, len(list(it.product(rows, range(4)))), {'added': 1680 + 4, 'no-order': 70 * 4, 'carried': 40320 * 4})

# team photo: 7 in a row, captain (0) in the middle, twins (1, 2) side by side
allp = list(it.permutations(range(7)))
mid = [p for p in allp if p[3] == 0]
both = [p for p in mid if abs(p.index(1) - p.index(2)) == 1]
pairs = [(i, i + 1) for i in range(6) if 3 not in (i, i + 1)]
ok(len(pairs) == 4, 'team photo: 4 free side-by-side pairs')
glued = [p for p in mid if abs(p.index(1) - p.index(2)) == 1 or {p.index(1), p.index(2)} == {2, 4}]
ok(len(glued) == 240 == fact(5) * 2, 'team photo: the glued block count is the 192 plus the 48 across the captain')
part(c1, 'p-team-photo', 1, len(allp), {'square': 49, 'sum': sum(range(1, 8)), 'seven': 7})
part(c1, 'p-team-photo', 2, len(mid), {'not-middle': 5040 - 720, 'six': 6})
part(c1, 'p-team-photo', 4, len(both), {'block': fact(5) * 2, 'no-swap': 4 * 24, 'pairs-six': 6 * 2 * 24})
ok(len(both) == 4 * 2 * fact(4) == 192, 'team photo formula')

# five-a-side
teams = range(8)
part(c1, 'p-five-a-side', 1, len(list(it.combinations(teams, 2))), {'ordered': 56, 'square': 64, 'times-two': 16})
part(c1, 'p-five-a-side', 2, len(list(it.permutations(teams, 2))), {'half': 14, 'carried': 112})
sol = [n for n in range(1, 100) if n * (n - 1) == 72]
ok(sol == [9], 'five-a-side: n(n-1) = 72 has one positive whole solution')
part(c1, 'p-five-a-side', 3, sol[0], {'halved': 36, 'one-factor': 8})
part(c1, 'p-five-a-side', 4, len(list(it.combinations(range(9), 6))), {'ordered': perm(9, 6), 'no-divide': 9 * 8 * 7, 'times': 54})

# ice-cream van
cups = list(it.combinations(range(11), 3))
cones = list(it.permutations(range(11), 3))
part(c1, 'p-ice-cream-van', 1, len(cups), {'ordered': 990, 'repeats': 11 ** 3, 'times': 33})
part(c1, 'p-ice-cream-van', 2, len(cones), {'times-three': 165 * 3, 'added': 165 + 6, 'carried': 990 * 6})
part(c1, 'p-ice-cream-van', 3, len(cups) + len(cones), {'multiplied': 165 * 990, 'carried': 990 + 5940})
part(c1, 'p-ice-cream-van', 4, (len(cups) + len(cones)) * 5, {'no-none': 1155 * 4, 'added': 1155 + 5, 'carried': 163350 * 5})

# ---------------------------------------------------------------- counting 2
c2 = load('counting', 2)


def touching(s, ch):
    return ch + ch in ''.join(s)


sig = set(it.permutations('RRRRBBY'))
tog = {s for s in sig if touching(s, 'B')}
ok(len(sig) == fact(7) // (fact(4) * 2) == 105 and len(tog) == fact(6) // fact(4) == 30, 'flags formulae')
part(c2, 'p-signal-flags', 1, len(sig), {'no-divide': 5040, 'reds-only': 5040 // 24, 'blues-only': 5040 // 2})
part(c2, 'p-signal-flags', 2, len(tog), {'flipped': 60, 'no-divide': 720, 'blue-divide': 720 // 48})
part(c2, 'p-signal-flags', 3, len(sig - tog), {'carried': 105 - 60, 'added': 135})
part(c2, 'p-signal-flags', 4, F(len(sig - tog), len(sig)), {'together': F(30, 105), 'carried': F(45, 105), 'bottom': F(75, 5040)},
     accept=[0.714, F(5, 7), F(75, 105), 0.7143], reject=[0.71, 0.7, 0.72])
ok(F(comb(7, 2) - 6, comb(7, 2)) == F(5, 7), 'flags: the check by places in the explanation')

S, G, B, N = 45, 38, 20, 80
members = ['s'] * (S - B) + ['g'] * (G - B) + ['b'] * B
members += ['n'] * (N - len(members))
atleast = sum(m != 'n' for m in members)
neither = members.count('n')
part(c2, 'p-leisure-centre', 1, atleast, {'no-overlap': 83, 'twice': 83 - 40})
part(c2, 'p-leisure-centre', 2, neither, {'carried': 80 - 43, 'only-one': (S - B) + (G - B)})
part(c2, 'p-leisure-centre', 3, F(neither, N), {'at-least': F(63, 80), 'carried': F(37, 80), 'bottom': F(17, 63)},
     accept=[0.213, 0.2125, 0.212, F(17, 80)], reject=[0.21, 0.22, 0.2])
pr = list(it.combinations(range(N), 2))
bothn = sum(1 for a, b in pr if members[a] == 'n' and members[b] == 'n')
ok(len(pr) == 3160 and bothn == 136, 'leisure pairs')
part(c2, 'p-leisure-centre', 4, F(bothn, len(pr)), {'replaced': F(17, 80) ** 2, 'ordered-top': F(17 * 16, 3160), 'pairs-over-members': F(136, 80)},
     accept=[0.043, F(17, 80) * F(16, 79), F(136, 3160), F(17, 395)], reject=[0.045, 0.04, 0.044])

bal = set(it.permutations('BALLOON'))
oo = {s for s in bal if touching(s, 'O')}
ll = {s for s in bal if touching(s, 'L')}
ok(len(bal) == 1260 and len(oo) == 360 == len(ll) and len(oo & ll) == 120 == fact(5), 'balloon formulae')
part(c2, 'p-balloon-blocks', 1, len(bal), {'no-divide': 5040, 'one-pair': 2520})
part(c2, 'p-balloon-blocks', 2, len(oo), {'flipped': 720, 'both-divided': 180})
part(c2, 'p-balloon-blocks', 3, len(bal - oo), {'carried': 1260 - 720, 'carried-half': 1260 - 180})
part(c2, 'p-balloon-blocks', 4, len(bal - oo - ll), {'all-ls': 900 - 360, 'both-only': 900 - 120})
part(c2, 'p-balloon-blocks', 5, F(len(bal - oo - ll), len(bal)), {'carried': F(540, 1260), 'os-only': F(900, 1260), 'bottom': F(660, 5040)},
     accept=[0.524, F(11, 21), F(660, 1260), 0.5238], reject=[0.52, 0.53, 0.5])

kids = ['g'] * 6 + ['b'] * 5
tm = list(it.combinations(range(11), 4))
nog = [t for t in tm if all(kids[i] == 'b' for i in t)]
nob = [t for t in tm if all(kids[i] == 'g' for i in t)]
mixed = [t for t in tm if len({kids[i] for i in t}) == 2]
part(c2, 'p-quiz-team', 1, len(tm), {'ordered': perm(11, 4), 'times': 44})
part(c2, 'p-quiz-team', 2, len(nog), {'no-boys': len(nob), 'ordered': perm(5, 4)})
part(c2, 'p-quiz-team', 3, len(tm) - len(nog), {'no-boys': 330 - 15, 'exactly-one': sum(1 for t in tm if sum(kids[i] == 'g' for i in t) == 1)})
part(c2, 'p-quiz-team', 4, len(mixed), {'no-girls-again': 325 - 5, 'both-off': 325 - 15 - 5})
part(c2, 'p-quiz-team', 5, F(len(mixed), len(tm)), {'girl-only': F(325, 330), 'bottom': F(310, 325), 'carried': F(305, 330)},
     accept=[0.939, F(31, 33), F(310, 330), 0.9394], reject=[0.94, 0.93, 0.9])

# ---------------------------------------------------------------- counting 3 (vectors) and functions 4
import re
import sympy as sp

r_, s_, x_, t_, n_, b_ = sp.symbols('r s x t n b')
SYMS = {'r': r_, 's': s_, 'x': x_, 't': t_, 'n': n_, 'b': b_}


def tex(e):
    """The keys' small LaTeX: \\frac{a}{b}, implied products, tuples."""
    e = e.replace('\\left', '').replace('\\right', '')
    while '\\frac' in e:
        e2 = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', e)
        if e2 == e:
            raise ValueError(e)
        e = e2
    e = re.sub(r'(\d|\))\s*(?=[a-z(])', r'\1*', e)
    return sp.sympify(e, locals=SYMS, rational=True)


def same(a, b):
    a, b = tex(a) if isinstance(a, str) else a, tex(b) if isinstance(b, str) else b
    if isinstance(a, (tuple, sp.Tuple)) or isinstance(b, (tuple, sp.Tuple)):
        return len(a) == len(b) and all(sp.simplify(sp.sympify(u) - sp.sympify(v)) == 0 for u, v in zip(a, b))
    return sp.simplify(a - b) == 0


def epart(items, pid, k, mine, wrongs=None):
    w = items[pid]['parts'][k - 1]['widget']
    lab = f'{pid}[{k}]'
    ok(w['kind'] == 'expression', f'{lab} is an expression part')
    for form in [w['answer']] + list(w.get('accept') or []):
        ok(same(form, mine), f'{lab} key form {form} is not my {mine}')
    have = {q['id']: q for q in w.get('wrong', [])}
    for q in have.values():
        ok(not same(q['tex'], mine), f'{lab} wrong {q["id"]} equals the answer')
    for wid, v in (wrongs or {}).items():
        ok(wid in have and same(have[wid]['tex'], v), f'{lab} wrong {wid}: slip gives {v}, file {have.get(wid, {}).get("tex")}')
    ok(not (set(have) - set(wrongs or {})), f'{lab} wrong ids not rebuilt: {sorted(set(have) - set(wrongs or {}))}')


V = sp.Matrix
tup = lambda m: tuple(m)
norm = lambda m: sp.sqrt(sum(c ** 2 for c in m))
c3 = load('counting', 3)

S, P, Q = V([1, 2]), V([10, 14]), V([-2, 30])
SP, PQ = P - S, Q - P
epart(c3, 'p-orienteering', 1, tup(SP), {'start-minus-end': tup(S - P), 'end-point': tup(P)})
epart(c3, 'p-orienteering', 2, tup(PQ), {'start-minus-end': tup(P - Q), 'added': tup(P + Q)})
epart(c3, 'p-orienteering', 3, tup(SP + PQ), {'subtracted': tup(SP - PQ), 'position': tup(Q)})
ok(SP + PQ == Q - S, 'orienteering: head to tail equals end minus start')
route = 100 * (norm(SP) + norm(PQ))
direct = 100 * norm(Q - S)
ok(route == 3500 and sp.simplify(direct - 100 * sp.sqrt(793)) == 0, 'orienteering lengths exact')
ok(abs(math.hypot(9, 12) + math.hypot(-12, 16) - 35) < 1e-12 and abs(math.hypot(-3, 28) - 28.1603) < 5e-5, 'orienteering lengths numeric')
part(c3, 'p-orienteering', 4, route, {'components': 100 * (9 + 12 + 12 + 16), 'direct': float(direct), 'squares': 35}, accept=[3500], reject=[3499, 3501])
part(c3, 'p-orienteering', 5, float(route - direct), {'direct': float(direct), 'added-components': 3500 - 100 * (3 + 28), 'carried': 4900 - float(direct), 'squares': float(route - direct) / 100},
     accept=[684, 683.97, 3500 - 2816], reject=[680, 690, 3500 - 2820])

A, B, Cc = V([2, 3]), V([8, 7]), V([17, 13])
AB, AC = B - A, Cc - A
epart(c3, 'p-power-line', 1, tup(AB), {'start-minus-end': tup(A - B), 'added': tup(A + B)})
epart(c3, 'p-power-line', 2, tup(AC), {'start-minus-end': tup(A - Cc), 'from-b': tup(Cc - B)})
k = sp.Rational(AC[0], AB[0])
ok(k == sp.Rational(AC[1], AB[1]) == sp.Rational(5, 2), 'power line: one k for both rows')
part(c3, 'p-power-line', 3, k, {'reciprocal': 1 / k, 'difference': AC[0] - AB[0]})
cable = 100 * norm(AC)
ok(sp.simplify(cable - 100 * k * norm(AB)) == 0 and sp.simplify(norm(AC) ** 2 - 325) == 0, 'power line: |AC| = 2.5|AB| = sqrt(325)')
part(c3, 'p-power-line', 5, float(cable), {'ab-only': float(100 * norm(AB)), 'added': 100 * (15 + 10), 'units': float(norm(AC))},
     accept=[1803, 1802.78, 250 * 7.211, 250 * 7.21, 1802], reject=[1800, 1805, 250 * 7.2])
ok(k > 1, 'power line: k > 1 puts C beyond B')

h, d, tr = V([60, 40]), V([sp.Rational(5, 2), -sp.Rational(7, 2)]), V([-20, 30])
h2 = h + tr
part(c3, 'p-grain-merchant', 1, h.dot(d), {'no-sign': 60 * 2.5 + 40 * 3.5, 'sum-first': (60 + 40) * (2.5 - 3.5)})
epart(c3, 'p-grain-merchant', 2, tup(h2), {'signs': tup(h - tr), 'trade': tup(tr)})
ok(h2.dot(d) == h.dot(d) + tr.dot(d) == -145, 'grain: the dot product splits over the trade')
part(c3, 'p-grain-merchant', 3, h2.dot(d), {'trade-only': tr.dot(d), 'old-book': h.dot(d), 'signs': h.dot(d) - tr.dot(d), 'no-sign': 40 * 2.5 + 70 * 3.5})
ok((h - tr).dot(d) == 165, 'grain: holdings (80, 10) also give 165, as the signs line says')
cosv = h2.dot(d) / (norm(h2) * norm(d))
ang = math.degrees(math.acos(float(cosv)))
ang2 = math.degrees(math.atan2(-3.5, 2.5) - math.atan2(70, 40)) % 360
ok(abs(ang - min(ang2, 360 - ang2)) < 1e-9, 'grain: angle by acos and by atan2 agree')
part(c3, 'p-grain-merchant', 4, ang, {'acute': 180 - ang, 'cosine': float(cosv), 'radians': math.radians(ang)},
     accept=[115, 114.7, math.degrees(math.acos(-0.418)), math.degrees(math.acos(-0.42)), math.degrees(math.acos(-145 / 346.8))], reject=[114, 116, math.degrees(math.acos(-0.4))])
ok(abs(float(norm(h2)) - 80.62) < 5e-3 and abs(float(norm(d)) - 4.301) < 5e-4 and abs(float(norm(h2) * norm(d)) - 346.8) < 0.05, 'grain: magnitudes in the explanation')

RS = s_ - r_
OM = r_ + RS / 2
OX = sp.Rational(2, 3) * OM
RX = OX - r_
RN = -r_ + s_ / 2
epart(c3, 'p-sail-ring', 1, RS, {'reversed': r_ - s_, 'added': r_ + s_})
epart(c3, 'p-sail-ring', 2, OM, {'half-rs': RS / 2, 'whole-rs': r_ + RS})
epart(c3, 'p-sail-ring', 3, OX, {'two-thirds': sp.Rational(2, 3) * (r_ + s_), 'added': (sp.Rational(2, 3) + sp.Rational(1, 2)) * (r_ + s_)})
epart(c3, 'p-sail-ring', 4, RX, {'ox': OX, 'reversed': -RX, 'added': OX + r_})
kk = sp.symbols('k')
RXe, RNe = sp.expand(RX), sp.expand(RN)
solk = sp.solve([sp.Eq(RXe.coeff(r_), kk * RNe.coeff(r_)), sp.Eq(RXe.coeff(s_), kk * RNe.coeff(s_))], kk)
ok(solk == {kk: sp.Rational(2, 3)}, f'sail: one k fits both the r and the s terms ({solk})')
part(c3, 'p-sail-ring', 5, sp.Rational(2, 3), {'reciprocal': 1.5, 'third': RXe.coeff(s_) / 1, 'half': 0.5}, accept=[0.667, 0.6667, F(2, 3)], reject=[0.67, 0.66, 0.7])
# numbers: a real triangle, X is the centroid and lies on RN two thirds of the way along
O_, R_, S_ = V([0, 0]), V([7, 1]), V([2, 9])
M_, N_ = (R_ + S_) / 2, S_ / 2
X_ = sp.Rational(2, 3) * M_
ok(X_ == (O_ + R_ + S_) / 3 and X_ - R_ == sp.Rational(2, 3) * (N_ - R_), 'sail: numeric triangle, X is the centroid on RN')

f4 = load('functions', 4)
e = lambda v: sp.Rational(3, 2) * v
m = lambda v: v + 4
part(f4, 'p-photo-mount', 1, m(e(12)), {'order': e(m(12)), 'one-side': e(12) + 2, 'no-enlarge': m(12)})
epart(f4, 'p-photo-mount', 2, m(e(x_)), {'order': e(m(x_)), 'one-side': e(x_) + 2})
y_ = sp.symbols('y')
inv = sp.solve(sp.Eq(y_, m(e(x_))), x_)[0].subs(y_, x_)
epart(f4, 'p-photo-mount', 3, inv, {'wrong-order': x_ / sp.Rational(3, 2) - 4, 'sign': (x_ + 4) / sp.Rational(3, 2), 'reciprocal': 1 / m(e(x_))})
ok(inv.subs(x_, 22) == 12, 'photo: inverse sends 22 back to 12')
part(f4, 'p-photo-mount', 4, inv.subs(x_, 31), {'wrong-order': 31 / 1.5 - 4, 'sign': 35 / 1.5, 'forward': m(e(31)), 'times': 27 * 1.5})
part(f4, 'p-photo-mount', 5, e(m(18)), {'same': m(e(18)), 'mount-only': m(18), 'one-side': e(18 + 2)})
ok(e(m(18)) - 31 == 2, 'photo: 2 cm wider than ordered')

hh = lambda v: sp.Rational(15, 100) * v * (12 - v)
part(f4, 'p-fountain-jet', 1, hh(6), {'no-bracket': 0.15 * 6 * 12, 'one-factor': 0.15 * 6, 'position': 6}, accept=[5.4], reject=[5, 5.5])
ok(sp.solve(sp.diff(hh(x_), x_), x_) == [6], 'fountain: the top is at x = 6')
gs = {'squeeze': hh(sp.Rational(4, 5) * x_), 'widen-wrong': hh(sp.Rational(5, 4) * x_), 'slide': hh(x_ - 3), 'taller': sp.Rational(5, 4) * hh(x_)}
facts = {kq: (sorted(sp.solve(gq, x_)), gq.subs(x_, sp.solve(sp.diff(gq, x_), x_)[0])) for kq, gq in gs.items()}
ok(facts['squeeze'] == ([0, 15], sp.Rational(27, 5)), 'fountain: h(0.8x) leaves at 0, lands at 15, top 5.4')
ok(facts['widen-wrong'][0] == [0, sp.Rational(48, 5)] and facts['slide'][0] == [3, 15] and facts['taller'] == ([0, 12], sp.Rational(27, 4)), 'fountain: the three why lines')
opts = {o['id']: o for o in f4['p-fountain-jet']['parts'][1]['widget']['options']}
ok([kq for kq, o in opts.items() if o.get('correct')] == ['squeeze'] and set(opts) == set(gs), 'fountain: one option fits')
top = sp.solve(sp.diff(gs['squeeze'], x_), x_)[0]
part(f4, 'p-fountain-jet', 3, top, {'times': 6 * 0.8, 'same': 6, 'slide': 9})
w4 = f4['p-fountain-jet']['parts'][3]['widget']
roots = sorted(sp.solve(sp.Eq(gs['squeeze'], sp.Rational(405, 100)), x_))
ok(hh(3) == hh(9) == sp.Rational(405, 100), 'fountain: old jet 4.05 at 3 and 9')
ok([float(v) for v in roots] == sorted(w4['answers']) == [3.75, 11.25], 'fountain part 4 set')
slips4 = {'times': '2.4, 7.2', 'old': '3, 9', 'slide': '6, 12', 'top-plus-three': '4.5, 10.5'}
ok({q['id']: q['value'] for q in w4['wrong']} == slips4, 'fountain part 4 wrong sets are the named slips')

Cpk = lambda v: 3 if v <= 2 else 3 + sp.Rational(5, 2) * (v - 2)
rising = sp.expand(3 + sp.Rational(5, 2) * (t_ - 2))
part(f4, 'p-car-park', 1, Cpk(sp.Rational(9, 2)), {'no-free': 3 + 2.5 * 4.5, 'no-fee': 2.5 * 2.5, 'rate-only': 2.5 * 4.5})
epart(f4, 'p-car-park', 2, rising, {'bracket': 3 + sp.Rational(5, 2) * t_ - 2, 'no-fee': sp.Rational(5, 2) * t_ - 5, 'dropped': sp.Rational(5, 2) * t_ + 3})
stay = sp.solve(sp.Eq(rising, sp.Rational(1275, 100)), t_)[0]
part(f4, 'p-car-park', 3, stay, {'sign': (12.75 - 2) / 2.5, 'order': 12.75 / 2.5 + 2, 'carried': (12.75 - 1) / 2.5, 'forward': 2.5 * 12.75 - 2})
new = lambda v: 3 if v <= 3 else 3 + sp.Rational(5, 2) * (v - 3)
grid = [sp.Rational(i, 20) for i in range(21, 200)]
cands = {'later': lambda v: Cpk(v - 1), 'earlier': lambda v: Cpk(v + 1), 'less-rate': lambda v: Cpk(v) - sp.Rational(5, 2), 'plus-one': lambda v: Cpk(v) + 1}
fits = [kq for kq, fn in cands.items() if all(fn(v) == new(v) for v in grid)]
optc = {o['id']: o for o in f4['p-car-park']['parts'][3]['widget']['options']}
ok(fits == ['later'] and [kq for kq, o in optc.items() if o.get('correct')] == ['later'] and set(optc) == set(cands), 'car park: only C(t - 1) is the new charge for every stay over 1 hour')
ok(all(cands['less-rate'](v) == new(v) for v in grid if v > 3) and cands['less-rate'](sp.Rational(3, 2)) == sp.Rational(1, 2), 'car park: the less-rate why line')
part(f4, 'p-car-park', 5, new(stay), {'earlier': Cpk(stay + 1), 'same': Cpk(stay), 'outside': Cpk(stay) - 1})
ok(Cpk(stay) - new(stay) == sp.Rational(5, 2) and Cpk(stay - 1) == new(stay), 'car park: £2.50 less than before')

Bn = lambda v: sp.Max(sp.Rational(1, 5) * (v - 500), 0)
Tn = lambda q: 25 * q
part(f4, 'p-ticket-bonus', 1, sp.solve(sp.Eq(Tn(n_), 500), n_)[0], {'times': 500 * 25, 'next': 21})
comp = sp.expand(sp.Rational(1, 5) * (Tn(n_) - 500))
ok(all(Bn(Tn(q)) == comp.subs(n_, q) for q in range(21, 200)) and all(Bn(Tn(q)) == 0 for q in range(0, 21)), 'bonus: 5n - 100 for n > 20, 0 up to 20')
epart(f4, 'p-ticket-bonus', 2, comp, {'order': 25 * sp.Rational(1, 5) * (n_ - 500), 'bracket': 5 * n_ - 500, 'no-500': 5 * n_})
invb = sp.solve(sp.Eq(b_, comp), n_)[0]
epart(f4, 'p-ticket-bonus', 3, invb, {'wrong-order': b_ / 5 + 100, 'sign': (b_ - 100) / 5, 'reciprocal': 1 / (5 * b_ - 100)})
need = [q for q in range(0, 500) if sp.Max(sp.Rational(3, 10) * (Tn(q) - 500), 0) == 60]
ok(need == [28] and all(sp.Max(sp.Rational(3, 10) * (Tn(q) - 500), 0) == sp.Rational(3, 2) * Bn(Tn(q)) for q in range(0, 200)), 'bonus: 30% is 1.5 times every old bonus; 28 tickets give £60')
part(f4, 'p-ticket-bonus', 4, invb.subs(b_, sp.Rational(60) / sp.Rational(3, 2)), {'old-rate': invb.subs(b_, 60), 'times': invb.subs(b_, 90), 'scaled': 32 / 1.5})

if __name__ == '__main__':
    print(f'{checks} checks, {fails} failures')
    sys.exit(1 if fails else 0)
