"""Recompute every number stated in app/content/exams/topic-0.6.json by a second route and assert it at its path.

Route A is build.py (closed forms). Route B here is independent: truth tables and functions enumerated with
itertools, sets built as Python sets, exact Fractions, brute-force searches over n, and the induction steps
checked as polynomial identities at many k. Exits 1 on any failure.
Run: python3 docs/briefs/exam-0.6-scripts/check_numbers.py
"""
import itertools
import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.6.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None):
    w = node(W(iid, part))
    t = max(w['tol']['abs'] / 10, 1e-9)
    ok = abs(w['answer'] - value) <= t
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', '' if ok else 'route B differs')


def wrong(iid, wid, value, part=None):
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {value!r}', '' if ok else f'found {hit}')


def say(iid, path, value, fmt=None):
    ex.expect('exam', f'{P(iid)}.{path}', value, fmt=fmt)


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, n))


def imp(p, q):
    return (not p) or q


# ------------------------------------------------------------------ the file
ex._rec(len(items) == 24, f'{len(items)} items, 20 to 30', '')
ramp = Counter(i['difficulty'] for i in items)
ex._rec(dict(ramp) == {2: 5, 3: 12, 4: 5, 5: 2}, f'ramp {dict(sorted(ramp.items()))} = 5, 12, 5, 2', '')
pace = sum(i['pace'] for i in items)
ex._rec(pace == 3150 and pace / 60 < doc['minutes'], f'pace {pace} s inside {doc["minutes"]} minutes', '')
ex._rec(doc['pass'] == 0.7, 'pass 0.7', '')
with open(os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses', 'proof', 'course.json'), encoding='utf8') as f:
    course = json.load(f)
ex._rec(set(doc['skills']) == set(course['skills']), 'skills map = the course skills', '')
auto = {s for it in items if it.get('kind') != 'longform' for s in it['skills']}
ex._rec(auto == set(course['skills']), f'every skill on an auto-graded item ({len(auto)})', '')
for it in items:
    if 'parts' not in it and it.get('kind') != 'longform' and it['widget']['kind'] == 'choice':
        ex._rec(it['widget'].get('shuffle') is True, f'{it["id"]} choice shuffles', '')
kinds = Counter(it.get('kind') or ('parts' if 'parts' in it else it['widget']['kind']) for it in items)
ex._rec(kinds['order'] >= 1 and kinds['longform'] >= 1, f'kinds {dict(kinds)}', '')

# ------------------------------------------------------------------ difficulty 2
rows = list(itertools.product([True, False], repeat=5))
key('e-five-letter-rows', len(rows))
wrong('e-five-letter-rows', 'times', 2 * 5)
wrong('e-five-letter-rows', 'square', 5 * 5)
say('e-five-letter-rows', 'feedback.correct', len(rows))
say('e-five-letter-rows', 'explain.text', len(rows))

ex._rec(imp(500_000 > 2_000_000, False) is True, 'e-vacuous-rule: false hypothesis, late report, rule true', '')
ex._rec(sum(o.get('correct', False) for o in node(W('e-vacuous-rule'))['options']) == 1, 'e-vacuous-rule one correct', '')

X = {2, frozenset({2, 3}), frozenset({3}), 2}
key('e-set-elements', len(X))
wrong('e-set-elements', 'repeat', len([2, frozenset({2, 3}), frozenset({3}), 2]))
wrong('e-set-elements', 'flatten', len({2, 3}))

bonds = set(range(40))
callable_, floating = set(range(22)), set(range(13, 30))
ex._rec(len(callable_ & floating) == 9 and len(floating) == 17, 'bond sets 22, 17, overlap 9', '')
key('e-callable-floating', len(callable_ | floating))
wrong('e-callable-floating', 'added', len(callable_) + len(floating))
wrong('e-callable-floating', 'twice', len(callable_) + len(floating) - 2 * len(callable_ & floating))
say('e-callable-floating', 'explain.text', len(bonds - (callable_ | floating)))
say('e-callable-floating', 'feedback.correct', len(callable_ | floating))

wit = [x for x in range(-1000, 1001) if 4 * x + 7 == -5]
key('e-witness-solve', wit[0])
ex._rec(wit == [-3], 'witness unique in Z', '')
wrong('e-witness-solve', 'sign', -wit[0])
wrong('e-witness-solve', 'added', float(F(-5 + 7, 4)))
say('e-witness-solve', 'feedback.byKey.sign', 4 * 3 + 7)
say('e-witness-solve', 'feedback.correct', -12)

# ------------------------------------------------------------------ difficulty 3
# truth table: route B by enumeration, rows in the order T,T / T,F / F,T / F,F
tw = node(W('e-converse-table'))
rows = [(True, True), (True, False), (False, True), (False, False)]
for r, (p, q) in enumerate(rows):
    want = ['T' if v else 'F' for v in (imp(p, q), imp(not p, not q), p and not q)]
    got = [tw['rows'][r][2], tw['rows'][r][3]['answer'], tw['rows'][r][4]['answer']]
    ex._rec(got == want, f'e-converse-table row {r}: {got} = {want}', '')
    for c in (3, 4):
        for w in tw['rows'][r][c].get('wrong', []):
            ex._rec(w['text'] != tw['rows'][r][c]['answer'], f'e-converse-table r{r}c{c} wrong {w["id"]} differs from the key', '')
orig = [imp(p, q) for p, q in rows]
inv = [imp(not p, not q) for p, q in rows]
conv = [imp(q, p) for p, q in rows]
neg = [p and not q for p, q in rows]
ex._rec(inv == conv and inv == [True, True, False, True], 'inverse reads T, T, F, T and equals the converse', '')
ex._rec(neg == [False, True, False, False] and all(a != b for a, b in zip(neg, orig)), 'P and not Q is the opposite of P => Q on every row', '')
slip = [imp(p, not q) for p, q in rows]
ex._rec(slip == [False, True, True, True] and [r for r in range(4) if slip[r] != neg[r]] == [2, 3],
        'P => not Q differs from P and not Q on the F,T and F,F rows (where the slips sit)', '')
fbk = node(P('e-converse-table') + '.feedback')['byKey']
wids = {w['id'] for row in tw['rows'] for c in row if isinstance(c, dict) for w in c.get('wrong', [])}
ex._rec(set(fbk) == wids, 'table byKey keys are the wrong ids, not cell ids', '')

funcs = list(itertools.product(range(4), repeat=3))
key('e-functions-count', len(funcs))
wrong('e-functions-count', 'swapped', len(list(itertools.product(range(3), repeat=4))))
wrong('e-functions-count', 'product', len(list(itertools.product(range(3), range(4)))))
say('e-functions-count', 'explain.text', len(funcs))

inj = list(itertools.permutations(range(6), 3))
key('e-injection-count', len(inj))
wrong('e-injection-count', 'any', len(list(itertools.product(range(6), repeat=3))))
wrong('e-injection-count', 'unordered', len(list(itertools.combinations(range(6), 3))))
say('e-injection-count', 'explain.text', len(inj))

c = lambda n: F('2.5') + F('0.8') * n  # noqa: E731
lots = [n for n in range(0, 200) if c(n) == F('14.5')]
key('e-fee-inverse', lots[0])
wrong('e-fee-inverse', 'forward', float(c(F('14.5'))))
wrong('e-fee-inverse', 'added', float((F('14.5') + F('2.5')) / F('0.8')))
say('e-fee-inverse', 'explain.text', float(F('14.5') - F('2.5')))
say('e-fee-inverse', 'explain.text', lots[0])
say('e-fee-inverse', 'feedback.correct', lots[0])

xs = [k / 10 for k in range(-100, 101)]
ex._rec(all(math.exp(a) < math.exp(b) for a, b in zip(xs, xs[1:])) and min(map(math.exp, xs)) > 0,
        'e-exp-onto: e^x strictly increasing and positive, so -1 is never reached', '')

# element chase: check the inclusion on every triple of subsets of {0, 1, 2}, and that it is not an equality
subs = [set(s) for k in range(4) for s in itertools.combinations(range(3), k)]
ok = all(((A | B) & C) <= ((A & C) | B) for A in subs for B in subs for C in subs)
strict = any(((A | B) & C) != ((A & C) | B) for A in subs for B in subs for C in subs)
ex._rec(ok and strict, 'e-element-chase: inclusion holds on all 512 triples, not always equal', '')
ex._rec(({1} | set()) & {1} == ({1} & {1}) | set() == {1}, 'e-element-chase d2 example: both sides {1}', '')

for a in range(-20, 21):
    for b in range(-20, 21):
        m, n = 2 * a + 1, 2 * b + 1
        assert m * n + m + n == 4 * a * b + 4 * a + 4 * b + 3 == 2 * (2 * a * b + 2 * a + 2 * b + 1) + 1
ex._rec(True, 'e-odd-direct: identity holds for a, b in -20..20', '')
ex._rec(all((2 * k + 1) ** 2 + 2 * (2 * k + 1) == 4 * k * k + 8 * k + 3 == 2 * (2 * k * k + 4 * k + 1) + 1
            for k in range(-50, 51)), 'e-odd-direct "same" algebra is right (the flaw is one letter)', '')
say('e-odd-direct', 'widget.options[2].text', 3 * 5 + 3 + 5)
say('e-odd-direct', 'widget.options[2].text', 7 * 9 + 7 + 9)

ex._rec(4 * 3 == 12, 'e-quarters: four returns at most 3% sum to at most 12%', '')
say('e-quarters-contrapositive', 'explain.text', 12)
ex._rec(max(r / 4 for r in range(-400, 1201)) >= 0 and all(sum(q) / 4 <= 3 for q in itertools.product(range(-3, 4), repeat=4)),
        'e-quarters: every quarter at most 3 gives an average at most 3', '')

ex._rec(math.isclose(math.sqrt(2) + (1 - math.sqrt(2)), 1.0), 'e-rational-plus-irrational: sqrt2 + (1 - sqrt2) = 1', '')

ex._rec(not (1 + 1 < 1) and not any(n + 1 < n for n in range(1, 1000)), 'e-step-no-base: base fails, claim false', '')
say('e-step-no-base', 'explain.text', 1 + 1)

ex._rec((2 ** 2) % 4 == 0 and 2 % 4 != 0, 'e-proved-converse: n = 2 refutes', '')
ex._rec(all((4 * k) ** 2 == 16 * k * k == 4 * (4 * k * k) for k in range(-30, 31)), 'e-proved-converse algebra', '')
say('e-proved-converse', 'widget.options[0].text', 2 ** 2)

# ------------------------------------------------------------------ difficulty 4
def is_sq(v):
    return int(math.isqrt(v)) ** 2 == v


vals = {n: 10 * n * n + 1 for n in range(1, 40)}
first = min(n for n, v in vals.items() if is_sq(v))
key('e-prime-formula', first)
wrong('e-prime-formula', 'value', vals[first])
wrong('e-prime-formula', 'root', 19)
wrong('e-prime-formula', 'early', first - 1)
ex._rec([vals[n] for n in (1, 2, 3)] == [11, 41, 91], 'e-prime-formula prose values 11, 41, 91', '')
ex._rec(not any(is_sq(vals[n]) for n in range(1, first)) and first == 6, 'no square before n = 6', '')
ex._rec(vals[first] == 361 == 19 ** 2 == 10 * 36 + 1 and 15 ** 2 < vals[5] < 16 ** 2, '361 = 19^2; 251 lies between 225 and 256', '')
say('e-prime-formula', 'feedback.correct', vals[first])
say('e-prime-formula', 'feedback.byKey.early', vals[first - 1])
say('e-prime-formula', 'feedback.byKey.early', 15 ** 2)
say('e-prime-formula', 'feedback.byKey.early', 16 ** 2)
say('e-prime-formula', 'explain.text', vals[4])
say('e-prime-formula', 'explain.text', vals[first])
say('e-prime-formula', 'explain.text', 10 * 36)

holds = [n for n in range(0, 300) if 2 ** n >= 7 * n]
n0 = next(m for m in range(0, 300) if all(n in holds for n in range(m, 300)))
key('e-base-case-seven', n0)
wrong('e-base-case-seven', 'zero', 0)
wrong('e-base-case-seven', 'five', 5)
ex._rec(0 in holds and 1 not in holds and 5 not in holds, 'n = 0 holds, 1 and 5 fail', '')
ex._rec(all((14 * k >= 7 * k + 7) == (k >= 1) for k in range(0, 200)), 'step 14k >= 7k + 7 exactly when k >= 1', '')
say('e-base-case-seven', 'feedback.correct', 2 ** 6)
say('e-base-case-seven', 'feedback.correct', 7 * 6)
say('e-base-case-seven', 'feedback.correct', 2 ** 5)
say('e-base-case-seven', 'feedback.byKey.five', 7 * 5)

ex._rec(all(2 ** p != 3 ** q for p in range(1, 40) for q in range(1, 40)), 'e-log-contradiction: 2^p never equals 3^q', '')
ex._rec(2 ** 1 < 3 ** 1 and 2 ** 2 > 3 ** 1, 'e-log-contradiction "bigger" is false: 2 < 3 but 4 > 3', '')

grid = [k / 100 for k in range(1, 1001)]
ex._rec(all(x + 1 / x >= 2 - 1e-12 for x in grid), 'e-forwards-proof: x + 1/x >= 2 on a grid', '')
ex._rec(all(abs((x - 1) ** 2 - (x * x - 2 * x + 1)) < 1e-9 for x in grid), 'e-forwards-proof expansion', '')
say('e-forwards-proof', 'widget.lines[5].text', 2 + 1 / 2)

s20 = sum(i * (i + 1) for i in range(1, 21))
key('e-product-sum', s20, part=0)
wrong('e-product-sum', 'no-third', 20 * 21 * 22, part=0)
wrong('e-product-sum', 'squares', sum(i * i for i in range(1, 21)), part=0)
ex._rec(all(sum(i * (i + 1) for i in range(1, n + 1)) == F(n * (n + 1) * (n + 2), 3) for n in range(1, 60)),
        'e-product-sum formula holds for n = 1..59', '')
ex._rec(all(F(k * (k + 1) * (k + 2), 3) + (k + 1) * (k + 2) == F((k + 1) * (k + 2) * (k + 3), 3) for k in range(1, 80)),
        'e-product-sum step identity', '')
ex._rec(all(F(k * (k + 1) * (k + 2), 3) + k * (k + 1) == F(k * (k + 1) * (k + 5), 3) for k in range(1, 80)),
        'e-product-sum "old-term" algebra is right (the flaw is the term)', '')
ex.expect('exam', P('e-product-sum', 0) + '.feedback', s20)
ex.expect('exam', P('e-product-sum', 0) + '.feedback.byKey', 20 * 21 * 22)
ex.expect('exam', P('e-product-sum', 0) + '.feedback.byKey', sum(i * i for i in range(1, 21)))
ex.expect('exam', P('e-product-sum', 1) + '.widget.options[3].text', s20)
say('e-product-sum', 'prose', F(1 * 2 * 3, 3))

# ------------------------------------------------------------------ difficulty 5
sq = {a * a % 4 for a in range(-200, 201)}
pair = {(x + y) % 4 for x in sq for y in sq}
ex._rec(sq == {0, 1} and pair == {0, 1, 2}, 'e-two-squares: squares leave 0 or 1, sums 0, 1 or 2', '')
squares = {a * a for a in range(0, 40)}
ex._rec(not any((4 * m + 3 - s) in squares for m in range(0, 300) for s in squares if s <= 4 * m + 3),
        'e-two-squares: no 4m + 3 below 1,200 is a sum of two squares', '')
ex._rec(all(n % 4 == 3 for n in (3, 7, 11, 15)), 'd2 list 3, 7, 11, 15 is of the form 4m + 3', '')
ex._rec(all((2 * j) ** 2 == 4 * j * j and (2 * j + 1) ** 2 == 4 * (j * j + j) + 1 for j in range(-50, 51)), 'square forms', '')

lhs = lambda n: sum(i * 2 ** i for i in range(1, n + 1))  # noqa: E731
rhs = lambda n: (n - 1) * 2 ** (n + 1) + 2  # noqa: E731
ex._rec(all(lhs(n) == rhs(n) for n in range(1, 60)), 'e-weighted-sum formula holds for n = 1..59', '')
ex._rec(all(rhs(k) + (k + 1) * 2 ** (k + 1) == 2 * k * 2 ** (k + 1) + 2 == k * 2 ** (k + 2) + 2 == rhs(k + 1)
            for k in range(1, 60)), 'e-weighted-sum step chain', '')
md = 'model'
say('e-weighted-sum', md, lhs(4))
say('e-weighted-sum', md, 3 * 2 ** 5 + 2 - 96)
ex._rec([i * 2 ** i for i in range(1, 5)] == [2, 8, 24, 64] and rhs(1) == 2, 'n = 4 terms 2, 8, 24, 64; base 2', '')
ex._rec(sum(r['points'] for r in node(P('e-weighted-sum'))['rubric']) == 10, 'rubric sums to 10', '')
say('e-weighted-sum', 'rubric[6].text', 3 * 32 + 2)

ex.check_wrongs()
ex.report()
