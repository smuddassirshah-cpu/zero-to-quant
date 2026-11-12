"""Second read, proof problems-1 to -3: the reader's own keys, slips and stated numbers.
Imports nothing from the author's script. Every figure is typed from the prose of the problem.
Route 1 is a formula (exact, sympy or integers); route 2 builds the objects and counts them
(the 40 accounts, the 8 rows, a scan of thresholds, the 40 numbers, all 1,296 functions,
integer boxes, sums term by term). Each key and each `wrong` value is then compared with the file.
A line starting CLAIM is a statement of the content the reader holds to be false or loose
(a finding, not a failure).

Usage (repo root): <venv>/bin/python docs/reviews/review-problems-proof-1-3-scripts/mine.py"""
import itertools
import json
import sys

import sympy as sp

C = 'app/content/courses/proof/'
SETS = {n: json.load(open(f'{C}problems-{n}.json')) for n in (1, 2, 3)}
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def part(n, item, k):
    it = [x for x in SETS[n]['items'] if x['id'] == item][0]
    return it['parts'][k - 1]


def num(n, item, k, r1, r2, wrongs):
    """key by two routes, and every wrong id with the value its slip gives"""
    w = part(n, item, k)['widget']
    ok(r1 == r2, f'{n} {item} {k}: routes differ {r1} {r2}')
    ok(w['kind'] == 'numeric' and w['answer'] == r1, f"{n} {item} {k}: key {w.get('answer')} against mine {r1}")
    ok(w.get('tol', {}).get('abs') == 0, f'{n} {item} {k}: a count should have tol 0')
    got = {x['id']: x['value'] for x in w.get('wrong', [])}
    ok(got == wrongs, f'{n} {item} {k}: wrong {got} against mine {wrongs}')
    ok(all(v != r1 for v in got.values()) and len(set(got.values())) == len(got), f'{n} {item} {k}: wrong values distinct from key and each other')
    by = part(n, item, k)['feedback'].get('byKey', {})
    ok(set(by) == set(got), f'{n} {item} {k}: byKey ids {set(by)} against wrong ids {set(got)}')


def tex2sym(t, syms):
    import re
    t = t.replace('\\left', '').replace('\\right', '')
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    t = t.replace('^', '**')
    t = re.sub(r'(\d)([a-z(])', r'\1*\2', t)
    t = re.sub(r'([a-z)])(\()', r'\1*\2', t)
    return sp.sympify(t, locals=syms)


def expr(n, item, k, mine, syms, wrongs):
    w = part(n, item, k)['widget']
    ok(w['kind'] == 'expression', f'{n} {item} {k}: kind')
    ok(sp.simplify(tex2sym(w['answer'], syms) - mine) == 0, f"{n} {item} {k}: key {w['answer']} against mine {mine}")
    for a in w.get('accept', []):
        ok(sp.simplify(tex2sym(a, syms) - mine) == 0, f'{n} {item} {k}: accept {a} equals the key')
    got = {x['id']: tex2sym(x['tex'], syms) for x in w.get('wrong', [])}
    ok(set(got) == set(wrongs), f'{n} {item} {k}: wrong ids {set(got)} against mine {set(wrongs)}')
    for i, v in wrongs.items():
        if i in got:
            ok(sp.simplify(got[i] - v) == 0, f'{n} {item} {k}: wrong {i} {got[i]} against mine {v}')
            ok(sp.simplify(v - mine) != 0, f'{n} {item} {k}: wrong {i} differs from the key')
    by = part(n, item, k)['feedback'].get('byKey', {})
    ok(set(by) == set(got), f'{n} {item} {k}: byKey ids')


def choice(n, item, k, right_id, ids):
    w = part(n, item, k)['widget']
    r = [o['id'] for o in w['options'] if o.get('correct')]
    ok(w['kind'] == 'choice' and r == [right_id], f'{n} {item} {k}: correct option {r}')
    ok({o['id'] for o in w['options']} == set(ids), f'{n} {item} {k}: option ids')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{n} {item} {k}: every wrong option has a why')


# ---------------------------------------------------------------- set 1
# p-leverage-calls: 40 accounts, 12 over 5 (P), 15 called (Q), 9 both.
N, nP, nQ, nPQ = 40, 12, 15, 9
acc = [(True, True)] * nPQ + [(True, False)] * (nP - nPQ) + [(False, True)] * (nQ - nPQ)
acc += [(False, False)] * (N - len(acc))
ok(len(acc) == 40 and sum(p for p, q in acc) == 12 and sum(q for p, q in acc) == 15, 'accounts built')
imp = lambda a, b: (not a) or b
num(1, 'p-leverage-calls', 1, nP - nPQ, sum(p and not q for p, q in acc), {'swapped': nQ - nPQ, 'both': nPQ})
num(1, 'p-leverage-calls', 2, N - (nP - nPQ), sum(imp(p, q) for p, q in acc), {'true-true': nPQ, 'breakers': nP - nPQ})
ok(sum(not p for p, q in acc) == 28, 'the 28 accounts with leverage of 5 or less')
num(1, 'p-leverage-calls', 3, nQ - nPQ, sum(not imp(q, p) for p, q in acc), {'rule': 3, 'true-count': sum(imp(q, p) for p, q in acc)})
ok(sum(imp(q, p) for p, q in acc) == 34, 'converse holds on 34')
choice(1, 'p-leverage-calls', 4, 'right', ['right', 'every', 'converse', 'if-not'])
# the four options against the data: only `right` has the opposite truth value to the report on every data set
report = all(imp(p, q) for p, q in acc)
ok(report is False and any(p and not q for p, q in acc), 'report false, negation true here')
for data in itertools.product([0, 1, 2], repeat=4):  # counts of TT, TF, FT, FF accounts
    a = [(True, True)] * data[0] + [(True, False)] * data[1] + [(False, True)] * data[2] + [(False, False)] * data[3]
    rep = all(imp(p, q) for p, q in a)
    ok(any(p and not q for p, q in a) == (not rep), 'negation of the report is: some P and not Q')
opts = {'every': lambda a: all(imp(p, not q) for p, q in a), 'converse': lambda a: any(q and not p for p, q in a), 'if-not': lambda a: all(imp(p, not q) for p, q in a)}
for i, f in opts.items():
    same = all(f(a) == (not all(imp(p, q) for p, q in a)) for data in itertools.product([0, 1, 2], repeat=4)
               for a in [[(True, True)] * data[0] + [(True, False)] * data[1] + [(False, True)] * data[2] + [(False, False)] * data[3]])
    ok(not same, f'option {i} is not the negation')

# p-spread-signal: P close above average, Q volume above 3 million, R spread wider than 4p.
P, Q, R = 8.40 > 8.25, 2.6 > 3, 5 > 4
num(1, 'p-spread-signal', 1, 2, sum([P, Q, R]), {'all': 3, 'one': 1})
choice(1, 'p-spread-signal', 2, 'no-r', ['no-r', 'yes-or', 'no-q', 'yes-r'])
ok(((P or Q) and not R) is False and (P or Q) is True and (not R) is False, 'Monday: or true, not R false, no buy')
rows = list(itertools.product([True, False], repeat=3))
buy = [r for r in rows if (r[0] or r[1]) and not r[2]]
num(1, 'p-spread-signal', 3, 3 * 1, len(buy), {'or-only': sum(p or q for p, q, r in rows), 'not-r-only': sum(not r for p, q, r in rows), 'and': sum(p and q and not r for p, q, r in rows)})
hold = [r for r in rows if imp(r[0] or r[1], not r[2])]
fail = [r for r in rows if not imp(r[0] or r[1], not r[2])]
num(1, 'p-spread-signal', 4, 8 - 3, len(hold), {'as-and': len(buy), 'only-false-if': sum(not (p or q) for p, q, r in rows)})
ok(len(fail) == 3 and set(hold) - set(buy) == {(False, False, True), (False, False, False)}, 'the 2 extra rows have P and Q both false')
if set(buy) & set(fail) == set():
    print("CLAIM 1 p-spread-signal 4 byKey.as-and: 'the rows of the and rule, which are also the rows where the implication fails' is false:",
          'the and rows', sorted(buy), 'and the failing rows', sorted(fail), 'share no row (R false against R true); only the count 3 is shared')
ok(set(buy) <= set(hold), 'every and row is a row where the implication holds')

# p-fund-thresholds: the grid, rows funds, columns years.
G = [[7, 3, 6, 2], [4, 8, 5, 1], [2, 6, 9, 4], [5, 4, 3, 9]]
cells = SETS[1]['items'][2]['canvas']['params']['cells']
ok([[int(c.rstrip('%')) for c in r] for r in cells] == G, 'grid as typed')
A = lambda t: all(any(x > t for x in row) for row in G)
B = lambda t: any(all(G[f][y] > t for f in range(4)) for y in range(4))
colmin = [min(G[f][y] for f in range(4)) for y in range(4)]
rowmax = [max(r) for r in G]
ok(colmin == [2, 3, 3, 1] and rowmax == [7, 8, 9, 9], 'lowest by year and best by fund as printed')
choice(1, 'p-fund-thresholds', 1, 'right', ['right', 'inner', 'all', 'strict'])
ok(all(G[f][y] <= 5 for y in range(4) for f in [min(range(4), key=lambda f: G[f][y])]), 'negation of B(5) true on the grid')
num(1, 'p-fund-thresholds', 2, sum(m > 5 for m in colmin), sum(all(G[f][y] > 5 for f in range(4)) for y in range(4)), {'some-fund': sum(any(G[f][y] > 5 for f in range(4)) for y in range(4))})
bigB = max(t for t in range(-5, 15) if B(t))
bigA = max(t for t in range(-5, 15) if A(t))
ok(all(B(t) for t in range(-5, bigB + 1)) and all(A(t) for t in range(-5, bigA + 1)), 'A and B hold for every smaller t')
num(1, 'p-fund-thresholds', 3, max(colmin) - 1, bigB, {'at-least': max(colmin), 'swapped': bigA})
num(1, 'p-fund-thresholds', 4, min(rowmax) - 1, bigA, {'at-least': min(rowmax), 'kept-b': bigB, 'best-fund': max(rowmax) - 1})

# ---------------------------------------------------------------- set 2
U = set(range(1, 41))
SA = {x for x in U if x % 4 == 0}
SB = {x for x in U if x % 6 == 0}
num(2, 'p-multiples-forty', 1, 40 // 4, len(SA), {'no-forty': len(SA - {40})})
num(2, 'p-multiples-forty', 2, 40 // 12, len(SA & SB), {'product': 40 // 24, 'all-b': len(SB)})
ok(SA & SB == {12, 24, 36} and SB - SA == {6, 18, 30}, 'the lists printed')
sub = [s for r in range(4) for s in itertools.combinations(sorted(SA & SB), r)]
num(2, 'p-multiples-forty', 3, 2 ** 3, len(sub), {'times-two': 2 * 3, 'no-empty': len(sub) - 1})
num(2, 'p-multiples-forty', 4, 10 + 6 - 3, len(SA | SB), {'no-overlap': 10 + 6, 'added': 10 + 6 + 3})
num(2, 'p-multiples-forty', 5, 40 - 13, len((U - SA) & (U - SB)), {'carry-16': 40 - 16, 'wrong-law': len(U - (SA & SB))})
ok((U - SA) & (U - SB) == U - (SA | SB), 'De Morgan on the 40 numbers')

J, S = range(4), range(6)
fs = list(itertools.product(S, repeat=len(J)))
inj = [f for f in fs if len(set(f)) == 4]
num(2, 'p-jobs-servers', 1, 4 * 6, len(list(itertools.product(J, S))), {'added': 4 + 6, 'functions': 6 ** 4})
num(2, 'p-jobs-servers', 2, 6 ** 4, len(fs), {'flipped': 4 ** 6, 'pairs': 24, 'one-to-one': len(inj)})
num(2, 'p-jobs-servers', 3, 6 * 5 * 4 * 3, len(inj), {'repeat': 1296, 'unordered': len(list(itertools.combinations(S, 4))), 'jobs-only': sp.factorial(4)})
ok(15 * 24 == 360, '15 x 24')
choice(2, 'p-jobs-servers', 4, 'no-size', ['no-size', 'yes-inj', 'yes-count', 'no-never'])
ok(max(len(set(f)) for f in fs) == 4 and not any(set(f) == set(S) for f in fs), 'no assignment is onto; at most 4 servers reached')
num(2, 'p-jobs-servers', 5, 1296 - 360, sum(len(set(f)) < 4 for f in fs), {'added': 1296 + 360, 'carry-4096': 4096 - 360})
ok(936 / 1296 > 0.5, 'most of the assignments')

x, y, a, b, n = sp.symbols('x y a b n')
f = lambda t: 9 - 3 * t
choice(2, 'p-rule-and-domain', 1, 'right', ['right', 'wrong-way', 'one-pair', 'contra'])
ok(sp.solve(sp.Eq(f(a), f(b)), a) == [b] and f(1) == 6 and f(2) == 3, 'one-to-one; f(1) and f(2) as printed')
inv = sp.solve(sp.Eq(f(x), y), x)[0]
expr(2, 'p-rule-and-domain', 2, inv, {'y': y}, {'sign': (y - 9) / 3, 'applied-f': f(y), 'sign-y': (9 + y) / 3})
ok(sp.simplify(f(inv) - y) == 0 and sp.simplify(f((y - 9) / 3) - (18 - y)) == 0, 'f at the key is y; f at the sign slip is 18 - y')
num(2, 'p-rule-and-domain', 3, inv.subs(y, -6), [t for t in range(-50, 50) if f(t) == -6][0], {'sign': sp.Rational(-6 - 9, 3), 'applied-f': f(-6), 'dropped-minus': inv.subs(y, 6)})
ok(f(-5) == 24 and f(5) == -6, 'f(-5) = 24 and f(5) = -6')
img = {f(t) for t in range(-100, 100)}
num(2, 'p-rule-and-domain', 4, 30 - 30 // 3, sum(v not in img for v in range(1, 31)), {'hits': sum(v in img for v in range(1, 31)), 'onto': 0})
ok(inv.subs(y, 1) == sp.Rational(8, 3), 'y = 1 needs 8/3')

desk = lambda t: (t + 1) // 2
ok([desk(t) for t in range(1, 9)] == [1, 1, 2, 2, 3, 3, 4, 4], 'two to a desk')
EA, LB = {1, 2, 3, 5}, {2, 4, 6, 7}
im = lambda X: {desk(t) for t in X}
num(2, 'p-shift-images', 1, 3, len(im(EA)), {'traders': len(EA)})
ok(im(EA) == {1, 2, 3} and im(LB) == {1, 2, 3, 4}, 'the two images as printed')
num(2, 'p-shift-images', 2, 3, len(im(EA) & im(LB)), {'image-of-meet': len(im(EA & LB)), 'union': len(im(EA) | im(LB))})
num(2, 'p-shift-images', 3, 1, len(im(EA & LB)), {'same': 3, 'empty': 0})
choice(2, 'p-shift-images', 4, 'inj', ['inj', 'onto', 'sizes', 'small'])
# one-to-one forces f(A n B) = f(A) n f(B) for every A, B (all functions 4 -> 4, all subsets); onto and equal sizes do not
dom = range(4)
subsets = [set(c) for r in range(5) for c in itertools.combinations(dom, r)]
for g in itertools.product(range(4), repeat=4):
    eq = all({g[t] for t in X & Y} == {g[t] for t in X} & {g[t] for t in Y} for X in subsets for Y in subsets)
    ok(eq == (len(set(g)) == 4), f'images commute with intersection exactly when one-to-one: {g}')
ok(set(desk(t) for t in range(1, 9)) == {1, 2, 3, 4} and len(EA) == len(LB), 'this f is onto and the shifts are equal in size')

# ---------------------------------------------------------------- set 3
j, k, m = sp.symbols('j k m')
br = sp.expand(((2 * j + 1) ** 2 + (2 * k + 1) ** 2 - 2) / 4)
expr(3, 'p-two-odd-squares', 1, br, {'j': j, 'k': k}, {'lost-middle': j ** 2 + k ** 2, 'factor-two': 2 * br})
odd = [t for t in range(-41, 42) if t % 2]
ok(all((u * u + v * v) % 4 == 2 for u in odd for v in odd), 'claim: two odd squares sum to 2 mod 4')
choice(3, 'p-two-odd-squares', 2, 'right', ['right', 'ends', 'even', 'cases'])
ok(1 + 9 == 10 and 12 % 4 == 0 and 8 % 4 == 0, 'the counterexamples in the why lines')
num(3, 'p-two-odd-squares', 3, br.subs({j: 3, k: 5}), (7 ** 2 + 11 ** 2 - 2) // 4, {'squares-only': 9 + 25, 'whole-sum': 49 + 121})
ref = [t for t in range(1, 50) if (16 + t * t) % 2 == 0 and not (4 % 2 == 1 and t % 2 == 1)]
num(3, 'p-two-odd-squares', 4, 2, ref[0], {'odd-n': 1})
ok(16 + 1 == 17 and 16 + 4 == 20, '17 and 20')
box = range(-40, 41)
true_conv = all(u % 2 and v % 2 for u in box for v in box if (u * u + v * v) % 4 == 2)
loose = all(u % 2 and v % 2 for u in box for v in box if (u * u + v * v) % 2 == 0)
ok(true_conv and not loose, 'the converse of the stated claim is true; the colleague\'s wider claim is false')
if true_conv and (16 + 4) % 4 == 0:
    print("CLAIM 3 p-two-odd-squares 4: the part calls 'if m^2 + n^2 is even, then both odd' the converse and its explanation ends 'the converse is false'.",
          "The converse of the claim in the prose keeps 'not a multiple of 4' and is true (checked on the box -40..40); m = 4, n = 2 gives 20, a multiple of 4, so it is no counterexample to it.")

Sn = lambda t: sum(3 * i - 2 for i in range(1, t + 1))
gA = lambda t: 4 * t - 3
gB = lambda t: t * (3 * t - 1) // 2
ok(Sn(1) == gA(1) == gB(1) == 1 and Sn(2) == gA(2) == gB(2) == 5, 'both guesses fit n = 1, 2')
num(3, 'p-step-three-sum', 1, 3, [t for t in range(1, 50) if Sn(t) != gA(t)][0], {'checked': 2})
ok(Sn(3) == 12 and gA(3) == 9, '12 against 9')
num(3, 'p-step-three-sum', 2, gB(10), Sn(10), {'guess-a': gA(10), 'last-term': 3 * 10 - 2})
ok((1 + 28) / 2 == 14.5 and 10 * 14.5 == 145, 'mean 14.5')
step = sp.factor(k * (3 * k - 1) / 2 + (3 * k + 1))
ok(sp.simplify(step - (k + 1) * (3 * k + 2) / 2) == 0 and sp.expand(2 * step) == 3 * k ** 2 + 5 * k + 2, 'the step')
expr(3, 'p-step-three-sum', 3, sp.cancel(2 * step / (k + 1)), {'k': k}, {'copied': 3 * k - 1, 'term': 3 * k + 1, 'numerator': 3 * k ** 2 + 5 * k + 2})
ok(all(Sn(t) == gB(t) for t in range(1, 400)), 'guess B term by term to 399')
n40 = sp.solve(sp.Eq(3 * n - 2, 118), n)[0]
num(3, 'p-step-three-sum', 4, gB(int(n40)), sum(range(1, 119, 3)), {'off-by-one': gB(39), 'guess-a': gA(40), 'term-as-n': gB(118)})

choice(3, 'p-six-nine-lots', 1, 'right', ['right', 'claim', 'trial', 'non-int'])
ok(not any(6 * u + 9 * v == 100 for u in range(-300, 301) for v in range(-300, 301)), 'no integer pair in the box nets 100')
ok(60 + 36 == 96 and sp.Rational(100, 9) * 9 == 100, 'the trial and the real solution')
u, v = sp.symbols('x y')
expr(3, 'p-six-nine-lots', 2, sp.cancel((6 * u + 9 * v) / 3), {'x': u, 'y': v}, {'half-factored': 2 * u + 9 * v, 'multiplied': 3 * (6 * u + 9 * v)})
num(3, 'p-six-nine-lots', 3, 100 % 3, 100 - 3 * 33, {'quotient': 100 // 3, 'zero': 0})
ok(3 * 34 == 102, '3 x 34')
num(3, 'p-six-nine-lots', 4, sp.solve(sp.Eq(6 * u + 18, 102), u)[0], [t for t in range(-50, 50) if 6 * t + 9 * 2 == 102][0], {'no-y': 102 // 6, 'added': (102 + 18) // 6})
ok(all(any(6 * s + 9 * t == T for s in range(-60, 61) for t in range(-60, 61)) for T in range(-90, 91, 3)), 'every multiple of 3 in the range can be reached')

val = lambda t: t * t + 6 * t + 1
ints = range(-60, 61)
ok(all(t % 2 == 1 for t in ints if val(t) % 2 == 0), 'claim: value even, then n odd')
ok(all(val(t) % 2 == 0 for t in ints if t % 2 == 1), 'the converse is true here, as its why line says')
choice(3, 'p-even-test-contra', 1, 'right', ['right', 'converse', 'inverse', 'example'])
expr(3, 'p-even-test-contra', 2, sp.expand((val(2 * k) - 1) / 2), {'k': k}, {'no-half': 4 * k ** 2 + 12 * k, 'halved-twice': k ** 2 + 3 * k})
choice(3, 'p-even-test-contra', 3, 'integer', ['integer', 'clearly', 'cases', 'even'])
ok(all((2 * t * t + 6 * t) % 2 == 0 for t in ints), 'the bracket is even, as the `even` why line says')
num(3, 'p-even-test-contra', 4, val(-3), sp.expand((x ** 2 + 6 * x + 1)).subs(x, -3), {'sign': 8, 'sign-6n': 9 + 18 + 1, 'minus-square': -9 - 18 + 1})
print("NOTE 3 p-even-test-contra 4: n = -3 is odd, so it is not of the form n = 2k: the proved statement (n even, then value odd) says nothing at -3.",
      'An even n would use the proof: n = -4, k = -2, bracket', 2 * 4 + 6 * -2, 'value', val(-4), '=', f'2 x {2 * 4 + 6 * -2} + 1')

# shape rules of docs/briefs/chained.md
for s, d in SETS.items():
    ok(3 <= len(d['items']) <= 5, f'set {s}: 3 to 5 problems')
    ok(any(i['difficulty'] == 5 for i in d['items']) and all(3 <= i['difficulty'] <= 5 for i in d['items']), f'set {s}: difficulties')
    parts = [p for i in d['items'] for p in i['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(3 * typed >= 2 * len(parts), f'set {s}: typed {typed} of {len(parts)}')
    for i in d['items']:
        ok(3 <= len(i['parts']) <= 5, f"set {s} {i['id']}: 3 to 5 parts")
        for p in i['parts']:
            ok(p.get('feedback') and p.get('explain'), f"set {s} {i['id']}: feedback and explain")
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
