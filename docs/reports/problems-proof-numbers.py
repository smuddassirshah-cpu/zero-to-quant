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
    # p-leverage-calls: 40 parcels, 12 with P (weight over 5 kg), 15 with Q (heavy label), 9 with both.
    N, nP, nQ, nPQ = 40, 12, 15, 9
    acc = [(True, True)] * nPQ + [(True, False)] * (nP - nPQ) + [(False, True)] * (nQ - nPQ)
    acc += [(False, False)] * (N - len(acc))
    ok(len(acc) == 40 and sum(p for p, _ in acc) == 12 and sum(q for _, q in acc) == 15, 'parcels built')
    imp = lambda a, b: (not a) or b
    breakers = nP - nPQ
    num(it, 'p-leverage-calls', 1, breakers, sum(p and not q for p, q in acc), {'swapped': nQ - nPQ, 'both': nPQ})
    num(it, 'p-leverage-calls', 2, N - breakers, sum(imp(p, q) for p, q in acc),
        {'true-true': nPQ, 'breakers': breakers})
    ok(N - nP == 28 and nPQ + 28 == 37, 'parcels: 28 vacuous parcels plus 9 = 37')
    conv_false = nQ - nPQ
    num(it, 'p-leverage-calls', 3, conv_false, sum(not imp(q, p) for p, q in acc),
        {'rule': breakers, 'true-count': N - conv_false})
    choice(it, 'p-leverage-calls', 4, 'right')

    # p-spread-signal (greenhouse). Monday: soil moisture 24% vs 30%, temperature 21 vs 25, tank 40 litres vs 50.
    P, Q, R = 24 < 30, 21 > 25, 40 < 50
    num(it, 'p-spread-signal', 1, int(P) + int(Q) + int(R), sum([P, Q, R]), {'all': 3, 'one': 1})
    buy = (P or Q) and not R
    ok(buy is False and (P or Q) is True, 'Monday: P or Q true, not R false, no watering')
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
    # finding 1: the `as-and` line. The 'and' rows and the failing rows are two different sets of 3 rows.
    and_rows = {r for r in rows if (r[0] or r[1]) and not r[2]}
    fail_rows = {r for r in rows if not imp(r[0] or r[1], not r[2])}
    hold_rows = set(rows) - fail_rows
    ok(len(and_rows) == 3 and len(fail_rows) == 3 and not (and_rows & fail_rows), 'and rows and failing rows: 3 each, no row shared')
    ok(and_rows <= hold_rows and len(hold_rows - and_rows) == 2 and all(not (p or q) for p, q, r in hold_rows - and_rows),
       'holds on the 3 and rows plus the 2 rows with P or Q false: 5')
    as_and = it['p-spread-signal']['parts'][3]['feedback']['byKey']['as-and']
    ok('also the count of rows where the implication fails' in as_and and 'which are also' not in as_and, 'as-and line states the count, not the rows')

    # p-fund-thresholds (dancers): grid of marks out of 10, rows dancers, columns judges.
    g = [[7, 3, 6, 2], [4, 8, 5, 1], [2, 6, 9, 4], [5, 4, 3, 9]]
    cells = it['p-fund-thresholds']['canvas']['params']['cells']
    ok(cells == [[str(v) for v in r] for r in g], 'mark grid matches the canvas (no % sign)')
    ok(all(0 <= v <= 10 for r in g for v in r), 'every cell is a mark out of 10')
    ok('%' not in json.dumps(it['p-fund-thresholds']), 'no % sign left in the dancers set (finding 3)')
    cols = list(zip(*g))
    A = lambda t: all(any(v > t for v in r) for r in g)
    B = lambda t: any(all(v > t for v in c) for c in cols)
    choice(it, 'p-fund-thresholds', 1, 'right')
    ok(not B(5) and all(any(v <= 5 for v in c) for c in cols), 'negation of B(5) holds in the table')
    num(it, 'p-fund-thresholds', 2, sum(all(v > 5 for v in c) for c in cols),
        sum(min(c) > 5 for c in cols), {'some-fund': sum(any(v > 5 for v in c) for c in cols)})
    ok([min(c) for c in cols] == [2, 3, 3, 1], 'lowest marks by judge 2, 3, 3, 1')
    ok([max(r) for r in g] == [7, 8, 9, 9], 'best marks by dancer 7, 8, 9, 9')
    tB = max(t for t in range(-5, 20) if B(t))
    num(it, 'p-fund-thresholds', 3, max(min(c) for c in cols) - 1, tB,
        {'at-least': max(min(c) for c in cols), 'swapped': min(max(r) for r in g) - 1})
    ok(not any(all(v > 3 for v in c) for c in cols), 'B(3) false: "above" is strict')
    tA = max(t for t in range(-5, 20) if A(t))
    num(it, 'p-fund-thresholds', 4, min(max(r) for r in g) - 1, tA,
        {'at-least': min(max(r) for r in g), 'kept-b': tB, 'best-fund': max(max(r) for r in g) - 1})
    ok(not A(7), 'A(7) false: D1 best mark is 7')
    ok(all(A(t) and B(t) for t in range(-3, 3)) and all(A(t) for t in range(-3, 7)), 'A and B true for every smaller t')
    for iid in ('p-leverage-calls', 'p-spread-signal', 'p-fund-thresholds'):
        blob = json.dumps({k_: v_ for k_, v_ in it[iid].items() if k_ != 'id'}, ensure_ascii=False).lower()
        ok(not re.search(r'account|broker|margin|leverage|trader|spread|volume|pence', blob), f'{iid}: an old noun is left')


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
    ok('$|A| = 10$ and $|B| = 6$' in it['p-multiples-forty']['parts'][3]['question'], 'part 4 restates |A| = 10 and |B| = 6 (finding 10)')
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

    # p-rule-and-domain: f_c(x) = c x - 4 on R. Claim: one-to-one exactly when c != 0; onto R exactly when c != 0.
    c, x, y = sp.symbols('c x y')
    fc = lambda cc, xx: cc * xx - 4
    box = range(-20, 21)
    ok(all((len({fc(cc, a) for a in box}) == len(box)) == (cc != 0) for cc in range(-12, 13)), 'f_c one-to-one on a box exactly when c != 0')
    bad_c = [cc for cc in range(-50, 51) if len({fc(cc, a) for a in range(-5, 6)}) < 11]
    ok(bad_c == [0] and fc(0, 1) == fc(0, 2) == -4, 'the only c in -50..50 that fails is 0; f_0(1) = f_0(2) = -4')
    num(it, 'p-rule-and-domain', 1, int(sp.solve(sp.Eq(c, 0), c)[0]), bad_c[0], {'constant': -4, 'unit': 1})
    ok(fc(1, 3) != fc(1, 4) and fc(1, 3) + 1 == 0, 'at c = 1 the rule x - 4 is one-to-one')
    inv = sp.solve(sp.Eq(c * x - 4, y), x)[0]
    expr(it, 'p-rule-and-domain', 2, inv, ['y', 'c'])
    ok(sp.simplify((c * inv - 4) - y) == 0, 'f_c(f_c^-1(y)) = y')
    ok(sp.simplify((c * ((y - 4) / c) - 4) - (y - 8)) == 0, 'sign slip gives y - 8 (stated)')
    ok(all(cc * F(yy + 4, cc) - 4 == yy for cc in range(-9, 10) if cc for yy in range(-30, 31)), 'onto: every y is reached for c != 0')
    ok(all(fc(0, a) != 1 for a in range(-100, 101)), 'f_0 is not onto: 1 is never reached')
    v1 = int(inv.subs({c: -2, y: -10}))
    v2 = next(a for a in range(-100, 101) if fc(-2, a) == -10)
    num(it, 'p-rule-and-domain', 3, v1, v2,
        {'sign': int(((y - 4) / c).subs({c: -2, y: -10})), 'applied-f': fc(-2, -10), 'dropped-minus': int(((y + 4) / 2).subs(y, -10))})
    ok(fc(-2, 3) == -10 and fc(-2, 7) == -18 and fc(-2, -3) == 2, 'checks f(3) = -10, f(7) = -18, f(-3) = 2')
    image = {fc(4, n) for n in range(-100, 101)}
    missed_enum = sum(1 for yy in range(1, 31) if yy not in image)
    missed_rule = sum(1 for yy in range(1, 31) if F(yy + 4, 4).denominator != 1)
    num(it, 'p-rule-and-domain', 4, missed_rule, missed_enum, {'hits': 30 - missed_rule, 'onto': 0})
    ok(F(1 + 4, 4) == F(5, 4) and sorted(yy for yy in range(1, 31) if yy in image) == list(range(4, 29, 4)), 'y = 1 needs n = 5/4; the reached numbers are 4, 8, ..., 28')

    desk = {t: (t + 1) // 2 for t in range(1, 9)}   # ferry -> berth
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
    # p-two-odd-squares (re-set): m, n leave remainder 1 on division by 5, then mn does.
    prod = sp.expand((5 * j + 1) * (5 * k + 1))
    br = sp.expand((prod - 1) / 5)
    ok(br == 5 * j * k + j + k, 'product bracket')
    ints = range(-90, 91)
    ok(all((u * v) % 5 == 1 for u in ints for v in ints if u % 5 == 1 and v % 5 == 1), 'claim true on -90..90 for both factors')
    ok(all(((5 * a + 1) * (5 * b + 1)) % 5 == 1 for a in range(-30, 31) for b in range(-30, 31)), 'remainder 1 by brute force on j, k')
    expr(it, 'p-two-odd-squares', 1, br, ['j', 'k'])
    choice(it, 'p-two-odd-squares', 2, 'right')
    ok(6 * 6 == 36 and 36 % 5 == 1 and 6 * 11 == 66 and 66 % 5 == 1 and 6 % 5 == 1 and 11 % 5 == 1, 'stated: 6 x 6 = 36 and 6 x 11 = 66 leave remainder 1 on division by 5')
    jj, kk = (11 - 1) // 5, (16 - 1) // 5
    num(it, 'p-two-odd-squares', 3, int(br.subs({j: jj, k: kk})), (11 * 16 - 1) // 5,
        {'lost-middle': 5 * jj * kk, 'whole-product': 11 * 16})
    ok(5 * 35 + 1 == 176 == 11 * 16 and jj + kk == 5 and 11 % 5 == 1 and 16 % 5 == 1, 'stated 176 = 5 x 35 + 1, j + k = 5')
    # the converse (mn leaves 1, so m and n each leave 1) is false; with m = 4 the smallest positive n that refutes it is 4.
    cx = next(b for b in range(1, 50) if (4 * b) % 5 == 1 and not (4 % 5 == 1 and b % 5 == 1))
    num(it, 'p-two-odd-squares', 4, 4, cx, {'if-fails': 1})
    ok([(4 * b) % 5 for b in (1, 2, 3, 4)] == [4, 3, 2, 1], 'products 4, 8, 12 leave 4, 3, 2; 16 leaves 1 (stated)')
    ok(not all((u * v) % 5 != 1 or (u % 5 == 1 and v % 5 == 1) for u in range(1, 10) for v in range(1, 10)), 'the converse has counterexamples')

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
    numer = sp.expand(k * (3 * k - 1) + 2 * (3 * k + 1))
    ok(numer == 3 * k ** 2 + 5 * k + 2 and sp.expand((k + 1) * (3 * k + 2)) == numer, 'numerator 3k^2 + 5k + 2 = (k+1)(3k+2)')
    expr(it, 'p-step-three-sum', 3, numer, ['k'])
    w3 = it['p-step-three-sum']['parts'][2]['widget']
    ok(w3.get('form') == 'expanded' and w3['accept'] == ['3k^2+5k+2'], 'part 3 asks for the multiplied-out numerator and accepts no factored form (finding 17)')
    ok('form' in it['p-step-three-sum']['parts'][2]['feedback']['byKey'], 'part 3 has a line for an equal answer in the wrong shape')
    ok(sp.expand(k * (3 * k - 1) + (3 * k + 1)) == 3 * k ** 2 + 2 * k + 1, 'no-double slip 3k^2 + 2k + 1')
    ok(sum(3 * i - 2 for i in range(1, 11)) == 145, 'S_10 = 145 by adding the ten terms (finding 16)')
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

    # p-even-test-contra (re-set): if n^2 + 2 is a multiple of 3, then n is not a multiple of 3.
    choice(it, 'p-even-test-contra', 1, 'right')
    T = range(-90, 91)
    ok(all(t % 3 != 0 for t in T if (t * t + 2) % 3 == 0), 'claim true on -90..90')
    ok(all((t * t + 2) % 3 == 0 for t in T if t % 3 != 0), 'its converse is true too (so "it is true here" in the option is right)')
    ok(all(t % 3 == 0 for t in T if (t * t + 2) % 3 != 0), 'the inverse is a true statement here, and proves nothing about the claim')
    ok(any(t % 3 != 0 and (t * t + 2) % 3 == 0 for t in range(-5, 6)), 'the "example" option is a true statement: n = 1 gives 3')
    e = sp.expand((3 * k) ** 2 + 2)
    br3 = sp.expand((e - 2) / 3)
    ok(br3 == 3 * k ** 2, 'bracket 3k^2')
    expr(it, 'p-even-test-contra', 2, br3, ['k'])
    ok(all(((3 * t) ** 2 + 2) % 3 == 2 for t in T), 'remainder 2 for every multiple of 3')
    ok(3 ** 2 + 2 == 11 and 6 ** 2 + 2 == 38 and 11 % 3 == 2 and 38 % 3 == 2, 'cases n = 3 and n = 6 (the "cases" option): neither value is a multiple of 3')
    choice(it, 'p-even-test-contra', 3, 'integer')
    nn = -6
    kk3 = nn // 3
    v = nn ** 2 + 2
    num(it, 'p-even-test-contra', 4, int(br3.subs(k, kk3)), (v - 2) // 3,
        {'sign': 3 * -(kk3 ** 2), 'n-squared': nn ** 2, 'whole': v})
    ok(kk3 == -2 and v == 38 == 3 * 12 + 2 and v % 3 == 2, 'n = -6: k = -2, bracket 12, value 38 = 3 x 12 + 2')
    ok(len({12, -12, 36, 38}) == 4, 'slips distinct')


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
