"""Recompute every number in app/content/courses/proof/problems-1.json, problems-2.json and problems-3.json twice.

Method 1 is the learner's working: counts from the stated figures, formulas and exact algebra (sympy, fractions).
Method 2 is independent: brute force (build the 40 accounts, enumerate the truth table, scan every threshold,
list the sets and every function, search integer pairs, sum term by term).
For each numeric part the script checks that the two methods agree, that the JSON key equals them, that every `wrong`
value is the named slip, differs from the key, lies outside the key's band and has a byKey line, that a negative key
has a `sign` slip at its absolute value, and that the key is printed in `feedback.correct` and `explain.text`.
Expression parts: the key and every accept form are equal to the computed bracket (sympy) and every wrong form is not.
Choice parts: exactly one correct option, the one the working picks. numbers_lib's Level.check_wrongs runs as a
second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-proof-numbers.py
"""
import itertools, json, os, re, sys
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'proof')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf8'))['items']}


def plain(t):
    return t.replace('{,}', '').replace('−', '-')


def has_num(text, v):
    nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', plain(text))]
    return any(abs(x - v) < 1e-9 for x in nums)


def num(items, iid, k, m1, m2, slips):
    """m1, m2: the answer by two methods. slips: {wrong id: value computed from the named slip}."""
    part = items[iid]['parts'][k - 1]
    w, tag = part['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    ok(m1 == m2, f'{tag}: methods differ {m1} vs {m2}')
    ok(w['answer'] == m1, f'{tag}: key {w["answer"]} vs computed {m1}')
    tol = w['tol']['abs']
    ok(tol == 0 and float(m1).is_integer(), f'{tag}: integer key with abs 0 band expected')
    by = part['feedback'].get('byKey', {})
    ids = [x['id'] for x in w.get('wrong', [])]
    ok(sorted(ids) == sorted(slips), f'{tag}: wrong ids {ids} vs slips {sorted(slips)}')
    vals = []
    for x in w.get('wrong', []):
        v = x['value']
        ok(x['id'] in slips and v == slips[x['id']], f'{tag}: wrong {x["id"]}={v} vs slip {slips.get(x["id"])}')
        ok(abs(v - w['answer']) > tol + x['tol']['abs'], f'{tag}: wrong {x["id"]} inside the key band')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')
        ok(v not in vals, f'{tag}: wrong {x["id"]} repeats a value')
        vals.append(v)
    if w['answer'] < 0:
        ok(abs(w['answer']) in vals, f'{tag}: negative key without a slip at its absolute value')
    if w['answer'] != 0:
        ok(has_num(part['feedback']['correct'], w['answer']), f'{tag}: key not printed in feedback.correct')
        ok(has_num(part['explain']['text'], w['answer']), f'{tag}: key not printed in explain')


def expr(items, iid, k, value, syms):
    part = items[iid]['parts'][k - 1]
    w, tag = part['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'expression', f'{tag}: not expression')
    loc = {s: sp.Symbol(s) for s in syms}
    loc.update({str(s): s for s in sp.sympify(value).free_symbols})   # the same symbols as the computed value

    def P(t):
        t = t.replace('\\frac{', '(').replace('}{', ')/(').replace('}', ')').replace('^', '**')
        t = re.sub(r'(\d)([a-z(])', r'\1*\2', t)
        t = re.sub(r'([a-z)])\(', r'\1*(', t)
        t = re.sub(r'([a-z])([a-z])', r'\1*\2', t)
        return sp.sympify(t, locals=loc)
    for form in [w['answer']] + list(w.get('accept', [])):
        ok(sp.simplify(P(form) - value) == 0, f'{tag}: form {form!r} not equal to {value}')
    by = part['feedback'].get('byKey', {})
    for x in w.get('wrong', []):
        ok(sp.simplify(P(x['tex']) - value) != 0, f'{tag}: wrong {x["id"]} equals the key')
        ok(x['id'] in by, f'{tag}: wrong {x["id"]} has no byKey line')


def choice(items, iid, k, want):
    part = items[iid]['parts'][k - 1]
    w, tag = part['widget'], f'{iid} p{k}'
    right = [o['id'] for o in w['options'] if o.get('correct')]
    ok(right == [want], f'{tag}: correct option {right} vs {want}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{tag}: a distractor has no why')


# ------------------------------------------------------------------ level 1
def level1(it):
    # p-leverage-calls: 40 accounts, 12 with P (leverage over 5), 15 with Q (call), 9 with both.
    N, nP, nQ, nPQ = 40, 12, 15, 9
    acc = [(True, True)] * nPQ + [(True, False)] * (nP - nPQ) + [(False, True)] * (nQ - nPQ)
    acc += [(False, False)] * (N - len(acc))
    ok(len(acc) == 40 and sum(p for p, _ in acc) == 12 and sum(q for _, q in acc) == 15, 'accounts built')
    imp = lambda a, b: (not a) or b
    breakers = nP - nPQ
    num(it, 'p-leverage-calls', 1, breakers, sum(p and not q for p, q in acc), {'swapped': nQ - nPQ, 'both': nPQ})
    num(it, 'p-leverage-calls', 2, N - breakers, sum(imp(p, q) for p, q in acc),
        {'true-true': nPQ, 'breakers': breakers})
    ok(N - nP == 28 and nPQ + 28 == 37, 'leverage: 28 vacuous accounts plus 9 = 37')
    conv_false = nQ - nPQ
    num(it, 'p-leverage-calls', 3, conv_false, sum(not imp(q, p) for p, q in acc),
        {'rule': breakers, 'true-count': N - conv_false})
    choice(it, 'p-leverage-calls', 4, 'right')

    # p-spread-signal. Monday: close 8.40 vs 8.25, volume 2.6m vs 3m, spread 5p vs 4p.
    P, Q, R = F('8.40') > F('8.25'), F('2.6') > 3, 5 > 4
    num(it, 'p-spread-signal', 1, int(P) + int(Q) + int(R), sum([P, Q, R]), {'all': 3, 'one': 1})
    buy = (P or Q) and not R
    ok(buy is False and (P or Q) is True, 'Monday: P or Q true, not R false, no buy')
    choice(it, 'p-spread-signal', 2, 'no-r')
    rows = list(itertools.product([True, False], repeat=3))
    ok(len(rows) == 8, '8 rows')
    by_hand = 3 * 1  # 3 of 4 (P, Q) pairs make P or Q true, each once with R false
    num(it, 'p-spread-signal', 3, by_hand, sum(((p or q) and not r) for p, q, r in rows),
        {'or-only': sum((p or q) for p, q, r in rows), 'not-r-only': sum((not r) for p, q, r in rows),
         'and': sum((p and q and not r) for p, q, r in rows)})
    false_rows = 3  # P or Q true with R true
    num(it, 'p-spread-signal', 4, 8 - false_rows, sum(imp(p or q, not r) for p, q, r in rows),
        {'as-and': by_hand, 'only-false-if': sum(not (p or q) for p, q, r in rows)})
    ok(sum(not (p or q) for p, q, r in rows) == 2, 'two rows with P and Q both false')

    # p-fund-thresholds: grid of returns, rows funds, columns years.
    g = [[7, 3, 6, 2], [4, 8, 5, 1], [2, 6, 9, 4], [5, 4, 3, 9]]
    cells = it['p-fund-thresholds']['canvas']['params']['cells']
    ok(cells == [[f'{v}%' for v in r] for r in g], 'fund grid matches the canvas')
    cols = list(zip(*g))
    A = lambda t: all(any(v > t for v in r) for r in g)
    B = lambda t: any(all(v > t for v in c) for c in cols)
    choice(it, 'p-fund-thresholds', 1, 'right')
    ok(not B(5) and all(any(v <= 5 for v in c) for c in cols), 'negation of B(5) holds in the table')
    num(it, 'p-fund-thresholds', 2, sum(all(v > 5 for v in c) for c in cols),
        sum(min(c) > 5 for c in cols), {'some-fund': sum(any(v > 5 for v in c) for c in cols)})
    ok([min(c) for c in cols] == [2, 3, 3, 1], 'lowest returns by year 2, 3, 3, 1')
    ok([max(r) for r in g] == [7, 8, 9, 9], 'best years 7, 8, 9, 9')
    tB = max(t for t in range(-5, 20) if B(t))
    num(it, 'p-fund-thresholds', 3, max(min(c) for c in cols) - 1, tB,
        {'at-least': max(min(c) for c in cols), 'swapped': min(max(r) for r in g) - 1})
    ok(not any(all(v > 3 for v in c) for c in cols), 'B(3) false: "above" is strict')
    tA = max(t for t in range(-5, 20) if A(t))
    num(it, 'p-fund-thresholds', 4, min(max(r) for r in g) - 1, tA,
        {'at-least': min(max(r) for r in g), 'kept-b': tB, 'best-fund': max(max(r) for r in g) - 1})
    ok(not A(7), 'A(7) false: F1 best year is 7')


# ------------------------------------------------------------------ level 2
def level2(it):
    U = set(range(1, 41))
    A = {n for n in U if n % 4 == 0}
    B = {n for n in U if n % 6 == 0}
    num(it, 'p-multiples-forty', 1, 40 // 4, len(A), {'no-forty': len(A - {40})})
    num(it, 'p-multiples-forty', 2, 40 // 12, len(A & B), {'product': 40 // 24, 'all-b': len(B)})
    ok(sorted(A & B) == [12, 24, 36] and len(B) == 6, 'A and B: {12, 24, 36}, |B| = 6')
    subsets = [s for r in range(4) for s in itertools.combinations(sorted(A & B), r)]
    num(it, 'p-multiples-forty', 3, 2 ** 3, len(subsets), {'times-two': 2 * 3, 'no-empty': 2 ** 3 - 1})
    num(it, 'p-multiples-forty', 4, 10 + 6 - 3, len(A | B), {'no-overlap': 10 + 6, 'added': 10 + 6 + 3})
    num(it, 'p-multiples-forty', 5, 40 - 13, len((U - A) & (U - B)), {'carry-16': 40 - 16, 'wrong-law': len(U - (A & B))})

    J, S = range(4), range(6)
    funcs = list(itertools.product(S, repeat=4))
    inj = [f for f in funcs if len(set(f)) == 4]
    num(it, 'p-jobs-servers', 1, 4 * 6, len(list(itertools.product(J, S))), {'added': 4 + 6, 'functions': 6 ** 4})
    num(it, 'p-jobs-servers', 2, 6 ** 4, len(funcs), {'flipped': 4 ** 6, 'pairs': 24, 'one-to-one': len(inj)})
    num(it, 'p-jobs-servers', 3, 6 * 5 * 4 * 3, len(inj),
        {'repeat': 6 ** 4, 'unordered': len(list(itertools.combinations(S, 4))), 'jobs-only': 24})
    ok(15 * 24 == 360, 'jobs: 15 sets of 4 servers times 24 orders')
    ok(max(len(set(f)) for f in funcs) == 4 and not any(set(f) == set(S) for f in funcs), 'no onto assignment')
    choice(it, 'p-jobs-servers', 4, 'no-size')
    num(it, 'p-jobs-servers', 5, 1296 - 360, sum(len(set(f)) < 4 for f in funcs),
        {'added': 1296 + 360, 'carry-4096': 4096 - 360})

    x, y = sp.symbols('x y')
    f = 9 - 3 * x
    inv = sp.solve(sp.Eq(f, y), x)[0]
    choice(it, 'p-rule-and-domain', 1, 'right')
    expr(it, 'p-rule-and-domain', 2, inv, ['y'])
    ok(sp.simplify(f.subs(x, inv) - y) == 0, 'f(f^-1(y)) = y')
    ok(sp.simplify(f.subs(x, (y - 9) / 3) - (18 - y)) == 0, 'sign slip gives 18 - y (stated)')
    v1 = int(inv.subs(y, -6))
    v2 = next(a for a in range(-100, 101) if 9 - 3 * a == -6)
    num(it, 'p-rule-and-domain', 3, v1, v2,
        {'sign': int(((y - 9) / 3).subs(y, -6)), 'applied-f': int(f.subs(x, -6)), 'dropped-minus': int(inv.subs(y, 6))})
    ok(9 - 3 * 5 == -6 and 9 - 3 * -5 == 24, 'checks f(5) = -6 and f(-5) = 24')
    image = {9 - 3 * n for n in range(-100, 101)}
    missed_enum = sum(1 for yy in range(1, 31) if yy not in image)
    missed_rule = sum(1 for yy in range(1, 31) if F(9 - yy, 3).denominator != 1)
    num(it, 'p-rule-and-domain', 4, missed_rule, missed_enum, {'hits': 30 - missed_rule, 'onto': 0})
    ok(F(9 - 1, 3) == F(8, 3), 'y = 1 needs n = 8/3')

    desk = {t: (t + 1) // 2 for t in range(1, 9)}
    A2, B2 = {1, 2, 3, 5}, {2, 4, 6, 7}
    img = lambda X: {desk[t] for t in X}
    ok(img(B2) == {1, 2, 3, 4}, 'f(B) = {1, 2, 3, 4}')
    num(it, 'p-shift-images', 1, 3, len(img(A2)), {'traders': len(A2)})
    ok(img(A2) == {1, 2, 3}, 'f(A) = {1, 2, 3}')
    num(it, 'p-shift-images', 2, len({1, 2, 3} & {1, 2, 3, 4}), len(img(A2) & img(B2)),
        {'image-of-meet': len(img(A2 & B2)), 'union': len(img(A2) | img(B2))})
    num(it, 'p-shift-images', 3, len({desk[2]}), len(img(A2 & B2)), {'same': len(img(A2) & img(B2)), 'empty': 0})
    ok(A2 & B2 == {2}, 'A and B share trader 2 only')
    # one-to-one forces equality: a one-to-one seating (trader t at desk 9 - t) keeps it for every pair of subsets
    sub = [set(c) for r in range(0, 9) for c in itertools.combinations(range(1, 9), r)]
    g = lambda X: {9 - t for t in X}
    ok(all(g(X & Y) == g(X) & g(Y) for X in sub for Y in sub), 'one-to-one seating keeps f(A n B) = f(A) n f(B)')
    ok(img(A2) == img(A2) and all(img(X & Y) <= img(X) & img(Y) for X in sub[::7] for Y in sub[::11]), 'f(A n B) is always inside f(A) n f(B)')
    ok(desk[3] == desk[4] == 2 and desk[5] == desk[6] == 3, 'desks 2 and 3 reached through different traders')
    choice(it, 'p-shift-images', 4, 'inj')


# ------------------------------------------------------------------ level 3
def level3(it):
    j, k, n = sp.symbols('j k n', integer=True)
    m2n2 = sp.expand((2 * j + 1) ** 2 + (2 * k + 1) ** 2)
    br = sp.expand((m2n2 - 2) / 4)
    ok(br == j ** 2 + j + k ** 2 + k, 'odd squares bracket')
    ok(all(((2 * a + 1) ** 2 + (2 * b + 1) ** 2) % 4 == 2 for a in range(-20, 21) for b in range(-20, 21)), 'remainder 2 by brute force')
    expr(it, 'p-two-odd-squares', 1, br, ['j', 'k'])
    choice(it, 'p-two-odd-squares', 2, 'right')
    ok(1 ** 2 + 3 ** 2 == 10 and 12 % 4 == 0, 'stated: 1 + 9 = 10, 12 is a multiple of 4')
    jj, kk = (7 - 1) // 2, (11 - 1) // 2
    num(it, 'p-two-odd-squares', 3, int(br.subs({j: jj, k: kk})), (49 + 121 - 2) // 4,
        {'squares-only': jj ** 2 + kk ** 2, 'whole-sum': 7 ** 2 + 11 ** 2})
    ok(4 * 42 + 2 == 170 and jj + kk == 8, 'stated 170 = 4 x 42 + 2, j + k = 8')
    cx = next(b for b in range(1, 50) if (16 + b * b) % 2 == 0 and not (4 % 2 == 1 and b % 2 == 1))
    num(it, 'p-two-odd-squares', 4, 2, cx, {'odd-n': 1})
    ok((16 + 1) % 2 == 1 and 16 + 4 == 20, 'n = 1 gives 17 odd, n = 2 gives 20')

    S = lambda m: sum(3 * i - 2 for i in range(1, m + 1))
    gA, gB = (lambda m: 4 * m - 3), (lambda m: F(m * (3 * m - 1), 2))
    ok(S(1) == gA(1) == gB(1) == 1 and S(2) == gA(2) == gB(2) == 5, 'both guesses fit n = 1, 2')
    first = next(m for m in range(1, 100) if S(m) != gA(m))
    num(it, 'p-step-three-sum', 1, 3, first, {'checked': 2})
    ok(S(3) == 12 and gA(3) == 9, 'S_3 = 12, guess A gives 9')
    num(it, 'p-step-three-sum', 2, int(gB(10)), S(10), {'guess-a': gA(10), 'last-term': 3 * 10 - 2})
    ok(all(S(m) == gB(m) for m in range(1, 200)), 'guess B matches up to 199')
    step = sp.factor(k * (3 * k - 1) / 2 + 3 * k + 1)
    ok(sp.simplify(step - (k + 1) * (3 * k + 2) / 2) == 0, 'step factors as (k+1)(3k+2)/2')
    expr(it, 'p-step-three-sum', 3, 3 * k + 2, ['k'])
    last = 118
    nn = (last + 2) // 3
    ok(3 * nn - 2 == last, 'n = 40 for last term 118')
    num(it, 'p-step-three-sum', 4, int(gB(nn)), sum(range(1, last + 1, 3)),
        {'off-by-one': int(gB(nn - 1)), 'guess-a': gA(nn), 'term-as-n': int(gB(last))})

    x, y = sp.symbols('x y', integer=True)
    choice(it, 'p-six-nine-lots', 1, 'right')
    ok(10 * 6 + 4 * 9 == 96, 'stated trial 60 + 36 = 96')
    expr(it, 'p-six-nine-lots', 2, sp.expand((6 * x + 9 * y) / 3), ['x', 'y'])
    q, r = divmod(100, 3)
    num(it, 'p-six-nine-lots', 3, r, 100 - 3 * (100 // 3), {'quotient': q, 'zero': 0})
    ok(not any(6 * a + 9 * b == 100 for a in range(-300, 301) for b in range(-300, 301)), 'no pair in a box of 601 x 601')
    xs = [a for a in range(-300, 301) if 6 * a + 9 * 2 == 102]
    num(it, 'p-six-nine-lots', 4, (102 - 18) // 6, xs[0] if len(xs) == 1 else None, {'no-y': 102 // 6, 'added': (102 + 18) // 6})

    choice(it, 'p-even-test-contra', 1, 'right')
    e = sp.expand((2 * k) ** 2 + 6 * (2 * k) + 1)
    expr(it, 'p-even-test-contra', 2, sp.expand((e - 1) / 2), ['k'])
    ok(all(((t * t + 6 * t + 1) % 2 == 0) == (t % 2 == 1) for t in range(-100, 101)), 'claim and converse by brute force')
    choice(it, 'p-even-test-contra', 3, 'integer')
    v = (-3) ** 2 + 6 * (-3) + 1
    num(it, 'p-even-test-contra', 4, int(e.subs(k, sp.Rational(-3, 2))), v,
        {'sign': abs(v), 'sign-6n': 9 + 18 + 1, 'minus-square': -9 - 18 + 1})
    ok(v % 2 == 0, 'value at -3 is even')


for nlev, fn in ((1, level1), (2, level2), (3, level3)):
    fn(load(nlev))
    lv = Level('proof', nlev)
    lv.check_wrongs('problems')
    try:
        lv.report()
    except SystemExit as ex:
        if ex.code:
            fails.append(f'numbers_lib check_wrongs failed on level {nlev}')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
