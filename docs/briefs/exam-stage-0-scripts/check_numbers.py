"""Recompute every number in the 0.6 and 0.7 additions to app/content/exams/stage-0.json by a second route.

Route A is build.py. Route B here: the existing parts and item ids are compared with the list frozen before the
extension; each proof's algebra is checked by evaluating both sides over a range of integers, each search is redone by
its own loop or sieve, and every number in every learner-visible string of the new items must match a route-B or given
value (whole numbers 0 to 10 count as structure). Exits 1 on any failure.
Run: python3 docs/briefs/exam-stage-0-scripts/check_numbers.py
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'stage-0.json')


class Exam(Level):
    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
rec = lambda ok, label, note='': ex._rec(bool(ok), label, '' if ok else note)

# ---------------------------------------------------------------- the old ids, frozen before the extension
OLD = {
    'gcse': ['g-add-fractions', 'g-percent-of', 'g-negatives', 'g-linear', 'g-fractional-power', 'g-standard-form', 'g-up-then-down',
             'g-ratio-share', 'g-simultaneous', 'g-inequality', 'g-expand', 'g-quadratic', 'g-gradient', 'g-speed', 'g-rectangle',
             'g-compound', 'g-composite', 'g-thirty-degrees', 'g-complete-square', 'g-quadratic-sequence'],
    'precalc': ['p-log', 'p-index', 'p-arithmetic', 'p-radians', 'p-infinite-sum', 'p-exp-equation', 'p-natural-log', 'p-cos-value',
                'p-obtuse-cos', 'p-sine-equation', 'p-binomial-coefficient', 'p-arrangements', 'p-choose', 'p-vertex', 'p-inverse',
                'p-minimum', 'p-vector-length', 'p-codes', 'p-log-equation', 'p-sigma'],
}
ids = [p.get('id') for p in doc['parts']]
rec(ids == ['gcse', 'precalc', 'proof', 'zetamac', 'script', 'proofs-written', 'getting-hired'], f'part order {ids}')
for pid, items in OLD.items():
    part = next(p for p in doc['parts'] if p.get('id') == pid)
    rec([it['id'] for it in part['items']] == items, f'{pid}: all {len(items)} item ids unchanged, in order')
papers = [p['id'] for p in doc['parts'] if p['kind'] == 'paper']
checks = [p['id'] for p in doc['parts'] if p['kind'] == 'check']
rec(papers[:2] == ['gcse', 'precalc'] and checks[:2] == ['zetamac', 'script'], 'paper and check positions 0 and 1 unchanged')
old_ids = {i for v in OLD.values() for i in v}
proof = next(p for p in doc['parts'] if p.get('id') == 'proof')
new = {it['id']: it for it in proof['items']}
rec(not (old_ids & set(new)), 'no new item id reuses an old one')

ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def key(iid, value):
    w = new[iid]['widget']
    rec(abs(w['answer'] - value) <= max(w['tol']['abs'] / 10, 1e-9), f'{iid} answer {w["answer"]} = {value}')
    allow(iid, value)


def wrong(iid, wid, value):
    w = new[iid]['widget']
    hit = [x for x in w['wrong'] if x['id'] == wid]
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= max(hit[0]['tol']['abs'] / 10, 1e-9), f'{iid} wrong "{wid}" = {value}')
    allow(iid, value)


def is_prime_sieve(limit):
    s = bytearray([1]) * (limit + 1)
    s[0] = s[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


SIEVE = is_prime_sieve(2_000_000)


def order_check(iid, n_answer):
    w = new[iid]['widget']
    lids = [ln['id'] for ln in w['lines']]
    rec(len(w['answer']) == n_answer and len(w['distractors']) == 2 and sorted(w['answer'] + w['distractors']) == sorted(lids),
        f'{iid}: {n_answer} lines in order, 2 flawed lines')
    bk = new[iid]['feedback']['byKey']
    rec(all(next(ln for ln in w['lines'] if ln['id'] == d).get('why') == bk.get(d) for d in w['distractors']) and 'left-out' in bk,
        f'{iid}: each flawed line has its why as a byKey line, and left-out is named')


def correct_id(iid, want):
    w = new[iid]['widget']
    rec([o['id'] for o in w['options'] if o.get('correct')] == [want] and w.get('shuffle') is True
        and all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid}: key {want}, shuffled, every distractor has a why')


# direct proof: n = 2k + 1 gives n^2 - 1 = 4k(k + 1) = 8m
order_check('p-direct-proof', 4)
rec(all((2 * k + 1) ** 2 - 1 == 4 * k * (k + 1) and (k * (k + 1)) % 2 == 0 for k in range(-500, 500)), 'p-direct-proof: n^2 - 1 = 4k(k + 1), k(k + 1) even')
rec(3 ** 2 - 1 == 8, 'p-direct-proof: the example line 3^2 - 1 = 8')
key('p-direct-step', (13 * 13 - 1) / 8)
wrong('p-direct-step', 'gave-whole', 13 * 13 - 1)
wrong('p-direct-step', 'forgot-square', (13 - 1) / 8)
allow('p-direct-step', 13, 168, 21)

# contrapositive: n = 2k gives 5n + 7 = 2(5k + 3) + 1; the claim checked over a range
order_check('p-contrapositive-proof', 4)
rec(all(5 * (2 * k) + 7 == 2 * (5 * k + 3) + 1 for k in range(-500, 500)), 'p-contrapositive-proof: 10k + 7 = 2(5k + 3) + 1')
rec(all(n % 2 == 1 for n in range(-1000, 1000) if (5 * n + 7) % 2 == 0), 'p-contrapositive-proof: 5n + 7 even only for odd n')
correct_id('p-contrapositive-form', 'a')
grid = [i / 4 for i in range(1, 80)]
rec(all(a * b <= 9 for a in grid for b in grid if a <= 3 and b <= 3), 'p-contrapositive-form: a, b <= 3 gives ab <= 9 on a grid')

# contradiction: 2^p = 5^q has no solution in positive integers (parity), log2 5 to 6 places
order_check('p-contradiction-proof', 4)
rec(not any(2 ** p == 5 ** q for p in range(1, 80) for q in range(1, 40)), 'p-contradiction-proof: no 2^p = 5^q for small p, q')
l25 = math.log(5) / math.log(2)
txt = json.dumps(new['p-contradiction-proof'], ensure_ascii=False)
rec(f'{l25:.6f}' in txt, f'p-contradiction-proof: log2 5 = {l25:.6f} by ln 5 / ln 2')
allow('p-contradiction-proof', l25)
prod = 1
for p in range(2, 18):
    if SIEVE[p]:
        prod *= p
N = prod + 1
f = 2
while N % f:
    f += 1
key('p-euclid-number', f)
wrong('p-euclid-number', 'assumed-prime', N)
rec(all(N % p == 1 for p in (2, 3, 5, 7, 11, 13, 17)), 'p-euclid-number: each listed prime leaves remainder 1')
allow('p-euclid-number', N, N // f, 17, 19, 11, 13)

# induction: 3^n > n^3 from n = 4; (5/4)^3 < 2; base values
order_check('p-induction-proof', 5)
rec(3 ** 4 == 81 and 4 ** 3 == 64 and 3 ** 3 == 27 and (5 / 4) ** 3 < 2, 'p-induction-proof: 81 > 64, 27 = 27, (5/4)^3 < 2')
rec(all(3 * k ** 3 > (k + 1) ** 3 for k in range(4, 2000)), 'p-induction-proof: 3k^3 > (k + 1)^3 for k >= 4')
allow('p-induction-proof', 81, 64, 27)
fails = [n for n in range(1, 300) if not 3 ** n > n ** 3]
key('p-induction-base', max(fails) + 1)
wrong('p-induction-base', 'first-true', min(n for n in range(1, 300) if 3 ** n > n ** 3))
wrong('p-induction-base', 'equal-case', next(n for n in range(1, 300) if 3 ** n == n ** 3))
allow('p-induction-base', 27, 81, 64)

# counterexamples by sieve
order_check('p-counterexample-proof', 4)
n9 = next(n for n in range(1, 1000) if not SIEVE[n * n + n + 17])
rec(n9 == 16 and 16 * 16 + 16 + 17 == 17 * 17, f'p-counterexample-proof: first failure n = {n9}, value 17^2')
allow('p-counterexample-proof', n9, n9 * n9, n9 * n9 + n9 + 17, 17, 15)
n10 = next(n for n in range(1, 1000) if not SIEVE[2 * n * n + 29])
key('p-first-failure', n10)
wrong('p-first-failure', 'gave-value', 2 * n10 * n10 + 29)
rec((2 * n10 * n10 + 29) == 29 * (2 * n10 + 1), 'p-first-failure: 2n^2 + 29 = 29(2n + 1) at n = 29')
allow('p-first-failure', 29, 59, n10 - 1)

correct_id('p-negate-quantifiers', 'a')
correct_id('p-onto-function', 'a')
rec(sorted({-(-n // 2) for n in range(-50, 51)}) == list(range(-25, 26)) and len({-(-n // 2) for n in range(-50, 51)}) < 101,
    'p-onto-function: ceil(n/2) reaches every integer in range, some twice')

# the new paper and checks
ds = [it['difficulty'] for it in proof['items']]
rec(len(ds) == 12 and [ds.count(k) for k in (2, 3, 4, 5)] == [2, 7, 2, 1], f'proof paper ramp {[ds.count(k) for k in (2, 3, 4, 5)]}')
rec(proof['minutes'] * 60 >= sum(it['pace'] for it in proof['items']), f'proof paper {proof["minutes"]} min covers its pace')
methods = {'direct': ['p-direct-proof', 'p-direct-step'], 'contrapositive': ['p-contrapositive-proof', 'p-contrapositive-form'],
           'contradiction': ['p-contradiction-proof', 'p-euclid-number'], 'induction': ['p-induction-proof', 'p-induction-base'],
           'counterexample': ['p-counterexample-proof', 'p-first-failure']}
for m, (o, c) in methods.items():
    rec(new[o]['widget']['kind'] == 'order' and new[c]['widget']['kind'] in ('numeric', 'choice'), f'{m}: an order proof and an auto check')

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'skills', 'placeholder'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


for iid, it in new.items():
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v for k, v in it.items() if k not in ('difficulty', 'pace')}):
        s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
        for m in _NUM.finditer(normalise(s)):
            t = m.group(0).rstrip('.')
            v, dec = abs(float(t)), (len(t.split('.')[1]) if '.' in t else 0)
            if dec == 0 and v == int(v) and v <= 10:
                continue
            if not any(abs(v - a) < 0.5 * 10 ** -dec * (1 - 1e-9) + 1e-12 for a in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}')

ex.check_wrongs()
ex.report()
