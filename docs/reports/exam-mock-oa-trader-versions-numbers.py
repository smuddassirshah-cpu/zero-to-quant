"""Recompute every key of mock-oa-trader-2 and mock-oa-trader-3 twice.

Each key is computed exactly (Fraction or integer arithmetic) and by a second
method (enumeration, an independent formula, or a seeded simulation with a
stated tolerance), then compared with the key in the JSON. Every distractor
must differ from the key. Ranking items: the answer order follows the values,
neighbouring values differ by at least 0.02, and the feedback prints them to
three places. Interval items: exactly one narrowest option holds the value.
Sequence items: the shown terms follow the stated rule, and no rival rule that
fits every shown term predicts a different next term. Rivals tried (fix pass):
the version 1 rule families; constant difference and ratio; polynomials of
degree 2 and 3; linear recurrences of order 1, 2 and 3, with and without a
constant (exact rational fit, at least one shown term beyond the fit); ratios
rising evenly and a multiplier rising with the place; product of the two before
and squaring the last; alternating rules (add or multiply on odd and even
steps); two and three interleaved strands; a repeating block; and filters
("skip a class of numbers"): the shown terms are exactly the numbers between
the first and last term with a property, for about 140 properties, their
negations and pairwise unions, intersections and differences of a core set,
and "the factors of N". Finally no family tag or question text of versions 2
and 3 repeats one from version 1 or from the other version.

Run: <venv>/bin/python docs/reports/exam-mock-oa-trader-versions-numbers.py
"""
import datetime
import json
import os
import random
import re
import sys
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial, floor, isqrt, pi, sqrt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EX = os.path.join(ROOT, 'app', 'content', 'exams')
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)


def load(name):
    return json.load(open(os.path.join(EX, name)))


V1, V2, V3 = load('mock-oa-trader.json'), load('mock-oa-trader-2.json'), load('mock-oa-trader-3.json')


def items(d):
    return {it['id']: it for p in d['parts'][:3] for it in p['items']}


def parse(t):
    t = t.strip().strip('$').replace('{,}', '').replace(',', '')
    m = re.fullmatch(r'\\[dt]frac\{(-?\d+)\}\{(\d+)\}', t) or re.fullmatch(r'\\[dt]frac(\d)(\d)', t)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    return F(t)


def key_and_wrongs(it):
    ops = it['widget']['options']
    key = [parse(o['text']) for o in ops if o.get('correct')]
    assert len(key) == 1, it['id']
    return key[0], [parse(o['text']) for o in ops if not o.get('correct')]


def near(a, b, tol):
    return abs(float(a) - float(b)) <= tol


# ------------------------------------------------------------ helpers
def is_prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


PRIMES = [p for p in range(2, 400) if is_prime(p)]


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def digsum(n):
    return sum(int(c) for c in str(n))


def rev(n):
    return int(str(n)[::-1])


def series_exact(p, n):
    """Side with game chance p wins a best-of-n: first to n//2 + 1 wins."""
    w = n // 2 + 1
    q = 1 - p
    return sum(comb(w - 1 + k, k) * p ** w * q ** k for k in range(w))


def series_enum(p, n):
    """Play all n games and take the majority."""
    tot = F(0)
    for s in product([1, 0], repeat=n):
        if sum(s) > n // 2:
            tot += p ** sum(s) * (1 - p) ** (n - sum(s))
    return tot


def no_run_count(n, k):
    """Strings of n tosses with no run of k heads, by recurrence on the
    length of the final run of heads."""
    state = [1] + [0] * (k - 1)  # state[j]: ends in exactly j heads
    for _ in range(n):
        new = [0] * k
        new[0] = sum(state)
        for j in range(k - 1):
            new[j + 1] = state[j]
        state = new
    return sum(state)


def run_exact(n, k):
    return 1 - F(no_run_count(n, k), 2 ** n)


def run_enum(n, k):
    return F(sum(1 for s in product('HT', repeat=n) if 'H' * k in ''.join(s)), 2 ** n)


def sim(fn, n, seed):
    rng = random.Random(seed)
    return sum(fn(rng) for _ in range(n)) / n


# ------------------------------------------------------------ sequences
def terms_of(it):
    q = it['question']
    body = q.split('?', 1)[1].rsplit(', ?', 1)[0]
    body = body.replace('$', '').strip()
    out = []
    for t in body.split(','):
        out.append(parse(t.strip()))
    return out


def v1_predictors(a):
    """Each v1 rule family that fits every shown term, with its next term."""
    preds = {}
    n = len(a)
    d = [a[i + 1] - a[i] for i in range(n - 1)]
    if len(set(d)) == 1:
        preds['arithmetic'] = a[-1] + d[0]
    if all(x != 0 for x in a):
        r = [a[i + 1] / a[i] for i in range(n - 1)]
        if len(set(r)) == 1:
            preds['geometric'] = a[-1] * r[0]
    d2 = [d[i + 1] - d[i] for i in range(len(d) - 1)]
    if len(set(d2)) == 1:  # squares, second-diff, consecutive products
        preds['quadratic'] = a[-1] + d[-1] + d2[0]
    c = [a[i] - (i + 1) ** 3 for i in range(n)]
    for s in range(-3, 4):  # n^3 + c, allowing an index shift
        c = [a[i] - (i + 1 + s) ** 3 for i in range(n)]
        if len(set(c)) == 1:
            preds['cubes%+d' % s] = (n + 1 + s) ** 3 + c[0]
    if a[1] != a[0]:  # times-plus: a' = k a + c
        k = (a[2] - a[1]) / (a[1] - a[0])
        cc = a[1] - k * a[0]
        if all(a[i + 1] == k * a[i] + cc for i in range(n - 1)):
            preds['times-plus'] = k * a[-1] + cc
    if all(a[i] == a[i - 1] + a[i - 2] for i in range(2, n)):
        preds['fibonacci'] = a[-1] + a[-2]
    if all(a[i] == a[i - 1] + a[i - 2] + a[i - 3] for i in range(3, n)):
        preds['tribonacci'] = a[-1] + a[-2] + a[-3]
    odd, even = a[0::2], a[1::2]
    nxt = a[n % 2::2]  # the strand the next term (0-based index n) joins
    if len(odd) >= 2 and len(even) >= 2:
        if len({odd[i + 1] - odd[i] for i in range(len(odd) - 1)}) == 1 and \
                len({even[i + 1] - even[i] for i in range(len(even) - 1)}) == 1:
            preds['interleaved'] = nxt[-1] + (nxt[1] - nxt[0])
        if all(x != 0 for x in a):
            if len({odd[i + 1] / odd[i] for i in range(len(odd) - 1)}) == 1 and \
                    len({even[i + 1] / even[i] for i in range(len(even) - 1)}) == 1:
                preds['interleaved-geometric'] = nxt[-1] * (nxt[1] / nxt[0])
    for start in (0, 1):  # alternating: x k on steps of one parity, - c on the other
        ks = {a[i + 1] / a[i] for i in range(start, n - 1, 2) if a[i] != 0}
        cs = {a[i] - a[i + 1] for i in range(1 - start, n - 1, 2)}
        if len(ks) == 1 and len(cs) == 1:
            k, c = ks.pop(), cs.pop()
            preds['alternating'] = a[-1] * k if (n - 1 - start) % 2 == 0 else a[-1] - c
    if all(x.denominator == 1 and x > 0 for x in a):
        ai = [int(x) for x in a]
        if all(ai[i + 1] == ai[i] + digsum(ai[i]) for i in range(n - 1)):
            preds['digit-sum'] = ai[-1] + digsum(ai[-1])
        off = [ai[i] - PRIMES[i] for i in range(n)]
        od = {off[i + 1] - off[i] for i in range(n - 1)}
        if len(od) == 1:
            preds['primes'] = PRIMES[n] + off[-1] + od.pop()
    for c in range(-3, 4):  # rising multiplier: a' = m a + c with m rising by 1
        if a[0] != 0:
            m0 = (a[1] - c) / a[0]
            if all(a[i + 1] == (m0 + i) * a[i] + c for i in range(n - 1)):
                preds['rising-multiplier%+d' % c] = (m0 + n - 1) * a[-1] + c
    return preds


# ------------------------------------------------------------ rival rules (fix pass)
def pfs(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def ndiv(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def digs(n):
    return [int(c) for c in str(n)]


def _sq(n):
    return isqrt(n) ** 2 == n


def _cube(n):
    r = round(n ** (1 / 3))
    return any((r + e) ** 3 == n for e in (-1, 0, 1))


TRI = {k * (k + 1) // 2 for k in range(200)}
FIBS = {1, 2}
_a, _b = 1, 2
while _b < 10 ** 6:
    _a, _b = _b, _a + _b
    FIBS.add(_b)

BASE = {
    'prime': is_prime,
    'composite': lambda x: x > 1 and not is_prime(x),
    'square': _sq,
    'cube': _cube,
    'square-or-cube': lambda x: _sq(x) or _cube(x),
    'power-of-2': lambda x: x & (x - 1) == 0,
    'power-of-3': lambda x: x > 0 and 3 ** round(__import__('math').log(x, 3)) == x,
    'triangular': lambda x: x in TRI,
    'fibonacci': lambda x: x in FIBS,
    'squarefree': lambda x: len(pfs(x)) == len(set(pfs(x))),
    'semiprime': lambda x: len(pfs(x)) == 2,
    'two-distinct-primes': lambda x: len(pfs(x)) == 2 and len(set(pfs(x))) == 2,
    'prime-power': lambda x: x > 1 and len(set(pfs(x))) == 1,
    'one-or-prime-power': lambda x: len(set(pfs(x))) <= 1,
    'palindrome': lambda x: str(x) == str(x)[::-1],
    'sum-two-squares': lambda x: any(_sq(x - a * a) for a in range(isqrt(x) + 1)),
    'odd-divisor-count': lambda x: ndiv(x) % 2 == 1,
    'abundant': lambda x: sum(d for d in range(1, x) if x % d == 0) > x,
    'deficient': lambda x: sum(d for d in range(1, x) if x % d == 0) < x,
    'repdigit': lambda x: len(set(str(x))) == 1,
    'distinct-digits': lambda x: len(set(str(x))) == len(str(x)),
    'digits-rise': lambda x: all(a < b for a, b in zip(str(x), str(x)[1:])),
    'digits-non-falling': lambda x: all(a <= b for a, b in zip(str(x), str(x)[1:])),
    'even-digit-sum': lambda x: sum(digs(x)) % 2 == 0,
    'harshad': lambda x: x % sum(digs(x)) == 0,
}
for p in (2, 3, 5, 7):
    BASE['%d-smooth' % p] = (lambda p: lambda x: all(f <= p for f in pfs(x)))(p)
for t in (2, 3, 5, 7):
    BASE['prime-above-%d' % t] = (lambda t: lambda x: is_prime(x) and x > t)(t)
for k in range(2, 13):
    BASE['multiple-of-%d' % k] = (lambda k: lambda x: x % k == 0)(k)
for k in range(2, 7):
    for r in range(1, k):
        BASE['%d-mod-%d' % (r, k)] = (lambda k, r: lambda x: x % k == r)(k, r)
for dd in range(10):
    BASE['ends-%d' % dd] = (lambda dd: lambda x: x % 10 == dd)(dd)
    BASE['has-digit-%d' % dd] = (lambda dd: lambda x: str(dd) in str(x))(dd)
for s in range(1, 20):
    BASE['digit-sum-%d' % s] = (lambda s: lambda x: sum(digs(x)) == s)(s)
for nd in range(1, 9):
    BASE['%d-divisors' % nd] = (lambda nd: lambda x: ndiv(x) == nd)(nd)
for ds in ({'1', '2'}, {'1', '3'}, {'1', '2', '3'}, {'0', '1'}, {'1', '2', '0'}):
    BASE['digits-in-' + ''.join(sorted(ds))] = (lambda ds: lambda x: set(str(x)) <= ds)(ds)

PREDS = dict(BASE)
for name, f in BASE.items():
    PREDS['not-' + name] = (lambda f: lambda x: not f(x))(f)
CORE = ['prime', 'square', 'cube', 'power-of-2', 'triangular', 'fibonacci'] + ['multiple-of-%d' % k for k in range(2, 13)] + ['ends-%d' % d for d in range(10)]
for i, a in enumerate(CORE):
    for b in CORE[i + 1:]:
        fa, fb = BASE[a], BASE[b]
        PREDS[a + '-or-' + b] = (lambda fa, fb: lambda x: fa(x) or fb(x))(fa, fb)
        PREDS[a + '-xor-' + b] = (lambda fa, fb: lambda x: fa(x) != fb(x))(fa, fb)
        PREDS[a + '-and-' + b] = (lambda fa, fb: lambda x: fa(x) and fb(x))(fa, fb)
        PREDS[a + '-and-not-' + b] = (lambda fa, fb: lambda x: fa(x) and not fb(x))(fa, fb)
        PREDS[b + '-and-not-' + a] = (lambda fa, fb: lambda x: fb(x) and not fa(x))(fa, fb)


def solve_affine(rows, rhs, target):
    """Exact Gaussian elimination. Returns (prediction, confirmations) when the system
    is consistent and target is in the row space, else None."""
    m = len(rows[0])
    A = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv_cols, r = [], 0
    for c in range(m):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        A[r] = [x / A[r][c] for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
    if any(all(x == 0 for x in row[:m]) and row[m] != 0 for row in A):
        return None
    t = list(target)
    val = F(0)
    for i, c in enumerate(piv_cols):
        f = t[c]
        if f:
            val += f * A[i][m]
            t = [x - f * y for x, y in zip(t, A[i][:m])]
    if any(x != 0 for x in t):
        return None
    return val, len(rows) - r


def poly_next(s, k):
    rows = [list(s)]
    for _ in range(k + 1):
        rows.append([b - a for a, b in zip(rows[-1], rows[-1][1:])])
    if not rows[k + 1] or any(x != 0 for x in rows[k + 1]):
        return None
    nxt = rows[k][-1]
    for j in range(k - 1, -1, -1):
        nxt = rows[j][-1] + nxt
    return nxt


def strand_next(st):
    """Next term of one strand that is constant, arithmetic or geometric (3+ terms)."""
    if len(st) < 3:
        return None
    if len({b - a for a, b in zip(st, st[1:])}) == 1:
        return st[-1] + st[1] - st[0]
    if all(x != 0 for x in st) and len({b / a for a, b in zip(st, st[1:])}) == 1:
        return st[-1] * st[1] / st[0]
    return None


def rivals(a, minconf=1):
    """Every simple rule that fits all shown terms (with at least `minconf` terms
    beyond those that fix its parameters), mapped to the next term it gives."""
    a = [F(x) for x in a]
    n = len(a)
    out = {}
    # differences and ratios are the degree-0/1 polynomial and order-1 recurrences below,
    # but name them for the report
    d = [b - x for x, b in zip(a, a[1:])]
    if n >= 3 and len(set(d)) == 1:
        out['constant difference'] = a[-1] + d[0]
    if n >= 3 and all(x != 0 for x in a) and len({b / x for x, b in zip(a, a[1:])}) == 1:
        out['constant ratio'] = a[-1] * a[1] / a[0]
    for k in (2, 3):  # polynomial of degree k: k + 1 parameters
        if n >= k + 1 + minconf:
            p = poly_next(a, k)
            if p is not None:
                out['polynomial degree %d' % k] = p
    # linear recurrences a_i = sum c_j a_{i-j} (+ b)
    for k in (1, 2, 3):
        for const in (True, False):
            rows = [[a[i - j] for j in range(1, k + 1)] + ([F(1)] if const else []) for i in range(k, n)]
            if not rows:
                continue
            rhs = [a[i] for i in range(k, n)]
            tgt = [a[n - j] for j in range(1, k + 1)] + ([F(1)] if const else [])
            res = solve_affine(rows, rhs, tgt)
            if res and res[1] >= minconf:
                out['recurrence order %d%s' % (k, ' with constant' if const else '')] = res[0]
    # coefficient rising with the place: a_i = (m + i) a_{i-1} + c, and ratios in arithmetic progression
    if n >= 4 and all(x != 0 for x in a):
        r = [b / x for x, b in zip(a, a[1:])]
        if len({y - x for x, y in zip(r, r[1:])}) == 1 and r[1] != r[0]:
            out['ratios rise evenly'] = a[-1] * (r[-1] + r[1] - r[0])
        rows = [[a[i - 1], i * a[i - 1], F(1)] for i in range(1, n)]
        res = solve_affine(rows, a[1:], [a[-1], n * a[-1], F(1)])
        if res and res[1] >= minconf:
            out['multiplier rising with place'] = res[0]
    # simple non-linear recurrences
    if n >= 4:
        if all(a[i] == a[i - 1] * a[i - 2] for i in range(2, n)):
            out['product of two before'] = a[-1] * a[-2]
        for c in range(-3, 4):
            if all(a[i] == a[i - 1] ** 2 + c for i in range(1, n)):
                out['square the last, add %d' % c] = a[-1] ** 2 + c
    # alternating: odd steps and even steps each add a constant or multiply by one (2+ steps each)
    if n >= 5:
        for parity_ops in ((0, 0), (0, 1), (1, 0), (1, 1)):
            preds = []
            ok = True
            for par in (0, 1):
                steps = [(a[i], a[i + 1]) for i in range(par, n - 1, 2)]
                if parity_ops[par] == 0:
                    vals = {y - x for x, y in steps}
                else:
                    if any(x == 0 for x, _ in steps):
                        ok = False
                        break
                    vals = {y / x for x, y in steps}
                if len(steps) < 2 or len(vals) != 1:
                    ok = False
                    break
                preds.append(vals.pop())
            if ok:
                par = (n - 1) % 2
                v = preds[par]
                out['alternating %s/%s' % ('+x'[parity_ops[0]], '+x'[parity_ops[1]])] = a[-1] + v if parity_ops[par] == 0 else a[-1] * v
    # interleaved strands (2 or 3), each constant, arithmetic or geometric with 3+ terms
    for m in (2, 3):
        strands = [a[s::m] for s in range(m)]
        if all(strand_next(st) is not None for st in strands):
            out['%d interleaved strands' % m] = strand_next(strands[n % m])
    # periodic repeat of a block of length p, at least `minconf` + 1 terms past the first block
    for p in range(1, n):
        if n >= p + 1 + minconf and all(a[i] == a[i - p] for i in range(p, n)):
            out['block of %d repeats' % p] = a[n - p]
            break
    # mirror: the terms read back the way they came (palindromic period)
    # filters: the shown terms are exactly the numbers in [first, last] with a property
    if all(x.denominator == 1 and x > 0 for x in a) and all(y > x for x, y in zip(a, a[1:])):
        ai = [int(x) for x in a]
        lo, hi = ai[0], ai[-1]
        shown = set(ai)
        for name, f in PREDS.items():
            try:
                if all(f(x) == (x in shown) for x in range(lo, hi + 1)):
                    nxt = next(x for x in range(hi + 1, hi * 20 + 100) if f(x))
                    out['filter ' + name] = F(nxt)
            except (StopIteration, ZeroDivisionError, ValueError):
                pass
        if lo == 1:  # the factors of some N, in order
            for N in range(hi, 50 * hi + 1):
                if N % hi == 0 and all((N % x == 0) == (x in shown) for x in range(1, hi + 1)):
                    out['factors of %d' % N] = F(next(x for x in range(hi + 1, N + 1) if N % x == 0)) if N > hi else None
    return {k: v for k, v in out.items() if v is not None}


def tri(k):
    return k * (k + 1) // 2


def recaman(N):
    """Step n goes back n when that lands on a new number of 0 or more, else forward n."""
    s = [0]
    while len(s) < N:
        n, b = len(s), s[-1] - len(s)
        s.append(b if b >= 0 and b not in s else s[-1] + n)
    return s[:N]


def smooth23(x):
    """True when x has no prime factor but 2 and 3, by dividing them out."""
    for p in (2, 3):
        while x % p == 0:
            x //= p
    return x == 1


SEQ_RULES = {
    # id: (n-th term rule, second method computing the next term from the shown terms)
    ('2', 'a01-repeat-count'): (lambda N: [k for k in range(1, 10) for _ in range(k)][:N],
                                lambda a: a[-1] if a.count(a[-1]) < a[-1] else a[-1] + 1),
    ('2', 'a02-count-down-blocks'): (lambda N: [x for k in range(1, 10) for x in range(k, 0, -1)][:N],
                                     lambda a: a[-1] - 1 if a[-1] > 1 else max(a) + 1),
    ('2', 'a03-multiples-3-or-5'): (lambda N: [x for x in range(1, 200) if x % 3 == 0 or x % 5 == 0][:N],
                                    lambda a: next(x for x in range(int(a[-1]) + 1, 999) if x % 3 == 0 or x % 5 == 0)),
    ('2', 'a04-squares-of-primes'): (lambda N: [p * p for p in PRIMES][:N],
                                     lambda a: next(p for p in range(isqrt(int(a[-1])) + 1, 99) if is_prime(p)) ** 2),
    ('2', 'a05-three-power-plus-place'): (lambda N: [3 ** n + n for n in range(1, N + 1)],
                                          lambda a: 3 * a[-1] - (2 * len(a) - 1)),  # a' = 3a - (2n - 1)
    ('2', 'a06-collatz'): (lambda N: (lambda f: f(f, 7, N))(lambda f, x, k: [x] + f(f, x // 2 if x % 2 == 0 else 3 * x + 1, k - 1) if k else []),
                           lambda a: a[-1] / 2 if a[-1] % 2 == 0 else 3 * a[-1] + 1),
    ('2', 'a07-fixed-over-position'): (lambda N: [F(420, n) for n in range(1, N + 1)],
                                       lambda a: a[0] / (len(a) + 1)),
    ('2', 'a08-three-smooth'): (lambda N: [x for x in range(1, 999) if smooth23(x)][:N],
                                lambda a: next(x for x in range(int(a[-1]) + 1, 999) if all(p in (2, 3) for p in PRIMES if x % p == 0))),
    ('2', 'a09-position-times-power'): (lambda N: [n * 2 ** n for n in range(1, N + 1)],
                                        lambda a: a[-1] * 2 * F(len(a) + 1, len(a))),
    ('2', 'a10-reversed-squares'): (lambda N: [rev(n * n) for n in range(1, N + 1)],
                                    lambda a: int(str((len(a) + 1) ** 2)[::-1])),
    ('2', 'a11-product-of-two'): (lambda N: (lambda s: [s.append(s[-1] * s[-2]) for _ in range(N)] and s[:N])([1, 2]),
                                  lambda a: a[-1] * a[-2]),
    ('2', 'a12-pascal-row'): (lambda N: [comb(7, k) for k in range(N)],
                              lambda a: a[1]),
    ('2', 'a13-two-prime-products'): (lambda N: [x for x in range(2, 999) if (lambda fs: len(fs) == 2 and fs[0] * fs[1] == x)([p for p in PRIMES if x % p == 0])][:N],
                                      lambda a: next(x for x in range(int(a[-1]) + 1, 999) if sum(1 for p in PRIMES if x % p == 0) == 2 and all(x % (p * p) for p in PRIMES if x % p == 0))),
    ('2', 'a14-add-the-reverse'): (lambda N: (lambda s: [s.append(s[-1] + rev(s[-1])) for _ in range(N)] and s[:N])([13]),
                                   lambda a: a[-1] + rev(int(a[-1]))),
    ('2', 'a15-neighbour-prime-products'): (lambda N: [PRIMES[i] * PRIMES[i + 1] for i in range(N)],
                                            lambda a: (lambda p: p * next(q for q in range(p + 1, 99) if is_prime(q)))(max(pfs(int(a[-1]))))),
    ('3', 'a01-growing-decimal'): (lambda N: [F(int('123456789'[:n]), 10 ** n) for n in range(1, N + 1)],
                                   lambda a: a[-1] + F(len(a) + 1, 10 ** (len(a) + 1))),
    ('3', 'a02-fraction-pairs'): (lambda N: [F(n, 2 * n + 1) for n in range(1, N + 1)],
                                  lambda a: (lambda n: 1 / (2 + F(1, n + 1)))(1 / (1 / a[-1] - 2))),  # 1/a = 2 + 1/n
    ('3', 'a03-digits-one-two'): (lambda N: [x for x in range(1, 9999) if set(str(x)) <= {'1', '2'} and x > 9][:N],
                                  lambda a: next(x for x in range(int(a[-1]) + 1, 9999) if set(str(x)) <= {'1', '2'})),
    ('3', 'a04-gaps-squares'): (lambda N: [2 + sum(k * k for k in range(1, n)) for n in range(1, N + 1)],
                                lambda a: a[-1] + len(a) ** 2),
    ('3', 'a05-gaps-primes'): (lambda N: [1 + sum(PRIMES[:n]) for n in range(N)],
                               lambda a: a[-1] + PRIMES[len(a) - 1]),
    ('3', 'a06-last-digit-squares'): (lambda N: [(n * n) % 10 for n in range(1, N + 1)],
                                      lambda a: int(str((len(a) + 1) ** 2)[-1])),
    ('3', 'a07-double-last-two'): (lambda N: (lambda s: [s.append(2 * s[-1] % 100) for _ in range(N)] and s[:N])([37]),
                                   lambda a: int(str(int(2 * a[-1]))[-2:])),
    ('3', 'a08-non-squares'): (lambda N: [x for x in range(1, 99) if isqrt(x) ** 2 != x][:N],
                               lambda a: next(x for x in range(int(a[-1]) + 1, 99) if isqrt(x) ** 2 != x)),
    ('3', 'a09-triangular-squares'): (lambda N: [tri(n) ** 2 for n in range(1, N + 1)],
                                      lambda a: a[-1] + (len(a) + 1) ** 3),
    ('3', 'a10-digit-sum-five'): (lambda N: [x for x in range(41, 999) if digsum(x) == 5][:N],
                                  lambda a: next(x for x in range(int(a[-1]) + 1, 999) if digsum(x) == 5)),
    ('3', 'a11-primes-ending-3'): (lambda N: [p for p in PRIMES if p % 10 == 3][:N],
                                   lambda a: next(x for x in range(int(a[-1]) + 10, 999, 10) if is_prime(x))),
    ('3', 'a12-factor-count'): (lambda N: [len(divisors(n)) for n in range(1, N + 1)],
                                lambda a: __import__('math').prod(pfs(len(a) + 1).count(p) + 1 for p in set(pfs(len(a) + 1)))),  # d(n) from the prime powers
    ('3', 'a13-back-if-you-can'): (lambda N: recaman(N),
                                   lambda a: (lambda n, b: b if b >= 0 and b not in a else a[-1] + n)(len(a), a[-1] - len(a))),
    ('3', 'a14-square-digit-sum'): (lambda N: (lambda s: [s.append(sum(int(c) ** 2 for c in str(s[-1]))) for _ in range(N)] and s[:N])([4]),
                                    lambda a: sum(int(c) ** 2 for c in str(int(a[-1])))),
    ('3', 'a15-self-powers'): (lambda N: [n ** n for n in range(1, N + 1)],
                               lambda a: round(__import__('math').exp((len(a) + 1) * __import__('math').log(len(a) + 1)))),  # floating exp(n ln n)
}

# ------------------------------------------------------------ probability
def pick(seq):
    return seq


def b11_enum():
    tot = F(0)
    for k in range(1, 7):
        for s in product([0, 1], repeat=k):
            if sum(s) == 1:
                tot += F(1, 6) * F(1, 2 ** k)
    return tot


def hexagon_equilateral():
    pts = [(round(1000 * __import__('math').cos(pi * i / 3)), round(1000 * __import__('math').sin(pi * i / 3))) for i in range(6)]
    def d2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    good = 0
    for a, b, c in combinations(pts, 3):
        s = {d2(a, b), d2(b, c), d2(a, c)}
        good += max(s) - min(s) < 1e-3 * max(s)
    return F(good, comb(6, 3))


def cube_parallel():
    verts = list(product([0, 1], repeat=3))
    edges = [(u, v) for u, v in combinations(verts, 2) if sum(abs(x - y) for x, y in zip(u, v)) == 1]
    dirs = [tuple(abs(x - y) for x, y in zip(u, v)) for u, v in edges]
    assert len(edges) == 12
    par = sum(1 for i, j in combinations(range(12), 2) if dirs[i] == dirs[j])
    return F(par, comb(12, 2))


def grid_lines():
    cells = [(i, j) for i in range(3) for j in range(3)]
    good = 0
    for a, b, c in combinations(cells, 3):
        good += (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0])
    return F(good, comb(9, 3))


def even_rolls_sim(rng):
    n = 0
    while True:
        n += 1
        r = rng.randint(1, 6)
        if r in (1, 3, 5):
            return None
        if r == 6:
            return n


def cond_sim(fn, runs, seed):
    rng = random.Random(seed)
    vals = [v for v in (fn(rng) for _ in range(runs)) if v is not None]
    return sum(vals) / len(vals)


PROB = {
    ('2', 'b01-loaded-die'): (F(2, 7),  # p + 5 (p / 2) = 1; second: seeded draws with weights 1, 1, 1, 1, 1, 2
                              random.Random(2501).choices(range(1, 7), weights=[1, 1, 1, 1, 1, 2], k=300000).count(6) / 300000, 0.005),
    ('2', 'b02-exactly-one'): (F(1, 4) * F(2, 3) + F(3, 4) * F(1, 3),
                               F(sum(1 for x in range(4) for y in range(3) if (x == 0) != (y == 0)), 12), 0),
    ('2', 'b03-same-digit-clock'): (F(3, 24 * 60),
                                    F(sum(1 for h in range(24) for m in range(60) if len(set('%02d%02d' % (h, m))) == 1), 1440), 0),
    ('2', 'b04-odd-and-prime'): (F(9, 15),
                                 F(sum(1 for x in range(1, 31) if x % 2 and is_prime(x)), sum(1 for x in range(1, 31) if x % 2)), 0),
    ('2', 'b05-first-divides-second'): (F(sum(10 // d for d in range(1, 11)), 100),
                                        F(sum(1 for a in range(1, 11) for b in range(1, 11) if b % a == 0), 100), 0),
    ('2', 'b06-no-winner'): (F(3 + 6, 27),
                             F(sum(1 for s in product('RPS', repeat=3) if len(set(s)) != 2), 27), 0),
    ('2', 'b07-rising-pin'): (F(comb(10, 4), 10 ** 4),
                              F(sum(1 for s in product(range(10), repeat=4) if all(s[i] < s[i + 1] for i in range(3))), 10 ** 4), 0),
    ('2', 'b08-reds-at-ends'): (F(1, comb(5, 2)),
                                F(sum(1 for p in set(permutations('RRBBB')) if p[0] == p[4] == 'R'), len(set(permutations('RRBBB')))), 0),
    ('2', 'b09-digit-sum-three'): (F(comb(4, 2), 900), F(sum(1 for x in range(100, 1000) if digsum(x) == 3), 900), 0),
    ('2', 'b10-paired-up'): (F(1, 5), None, 0),
    ('2', 'b11-die-then-coins'): (F(1, 6) * sum(F(k, 2 ** k) for k in range(1, 7)), b11_enum(), 0),
    ('2', 'b12-more-heads'): ((1 - F(sum(comb(3, k) ** 2 for k in range(4)), 64)) / 2,
                              F(sum(1 for a in product([0, 1], repeat=3) for b in product([0, 1], repeat=3) if sum(a) > sum(b)), 64), 0),
    ('2', 'b13-beat-one-beat-all'): (F(1, 3) / F(1, 2),
                                     F(sum(1 for p in permutations('ABC') if p.index('A') < p.index('B') and p[0] == 'A'),
                                       sum(1 for p in permutations('ABC') if p.index('A') < p.index('B'))), 0),
    ('2', 'b14-pick-then-pick'): (F(1, 3) * (1 + F(1, 2) + F(1, 3)),
                                  sim(lambda r: r.randint(1, r.randint(1, 3)) == 1, 400000, 2502), 0.005),
    ('2', 'b15-line-dies-out'): (min(F(3 - 1, 4), F(3 + 1, 4)), None, 1e-6),
    ('3', 'b01-square-divisor'): (F(2 * 2, 3 * 3), F(sum(1 for d in divisors(36) if isqrt(d) ** 2 == d), len(divisors(36))), 0),
    ('3', 'b02-same-pair'): (F(1, comb(4, 2)),
                             F(sum(1 for a in combinations(range(4), 2) for b in combinations(range(4), 2) if a == b), comb(4, 2) ** 2), 0),
    ('3', 'b03-triangular-pick'): (F(5, 20), F(sum(1 for x in range(1, 21) if isqrt(8 * x + 1) ** 2 == 8 * x + 1), 20), 0),
    ('3', 'b04-mean-given-big'): (F(3 + 4 + 5 + 6, 4), F(sum(x for x in range(1, 7) if x > 2), 6) / F(4, 6), 0),
    ('3', 'b05-row-or-column'): (F(7 + 7, 63),
                                 F(sum(1 for a, b in combinations([(i, j) for i in range(8) for j in range(8)], 2) if a[0] == b[0] or a[1] == b[1]), comb(64, 2)), 0),
    ('3', 'b06-parallel-edges'): (F(3, 11), cube_parallel(), 0),
    ('3', 'b07-dice-run'): (F(4 * factorial(3), 6 ** 3),
                            F(sum(1 for s in product(range(1, 7), repeat=3) if sorted(s)[2] - sorted(s)[0] == 2 and len(set(s)) == 3), 216), 0),
    ('3', 'b08-equilateral'): (F(2, comb(6, 3)), hexagon_equilateral(), 0),
    ('3', 'b09-three-in-a-line'): (F(3 + 3 + 2, comb(9, 3)), grid_lines(), 0),
    ('3', 'b10-no-neighbours'): (F(2, 24), F(sum(1 for p in permutations([1, 2, 3, 4]) if all(abs(p[i] - p[i + 1]) != 1 for i in range(3))), 24), 0),
    ('3', 'b11-heads-together'): (F(4, comb(5, 2)),
                                  F(sum(1 for s in product('HT', repeat=5) if s.count('H') == 2 and 'HH' in ''.join(s)),
                                    sum(1 for s in product('HT', repeat=5) if s.count('H') == 2)), 0),
    ('3', 'b12-even-heads'): ((1 + (1 - 2 * F(1, 3)) ** 3) / 2,
                              sum(F(1, 3) ** sum(s) * F(2, 3) ** (3 - sum(s)) for s in product([0, 1], repeat=3) if sum(s) % 2 == 0), 0),
    ('3', 'b13-heads-given-some'): (F(3, 2) / F(7, 8),
                                    F(sum(sum(s) for s in product([0, 1], repeat=3)), sum(1 for s in product([0, 1], repeat=3) if sum(s) >= 1)), 0),
    ('3', 'b14-larger-is-eight'): (F(4, 7),
                                   F(sum(1 for a, b in combinations(range(1, 11), 2) if b == 8 and a + b >= 12),
                                     sum(1 for a, b in combinations(range(1, 11), 2) if b == 8)), 0),
    ('3', 'b15-even-rolls'): ((F(1, 6) * F(1, (1 - F(1, 3)) ** 2)) / (F(1, 6) / (1 - F(1, 3))),
                              cond_sim(even_rolls_sim, 600000, 2503), 0.02),
}


def pairings(people):
    if not people:
        yield []
        return
    a = people[0]
    for b in people[1:]:
        rest = [p for p in people[1:] if p != b]
        for r in pairings(rest):
            yield [(a, b)] + r


ps = list(pairings(list(range(6))))
PROB[('2', 'b10-paired-up')] = (F(1, 5), F(sum(1 for p in ps if (0, 1) in p), len(ps)), 0)
q = 0.0
for _ in range(5000):
    q = 1 / 3 + 2 / 3 * q * q
PROB[('2', 'b15-line-dies-out')] = (min(F(3 - 1, 4), F(3 + 1, 4)), q, 1e-6)
check(2 * F(1, 2) ** 2 - 3 * F(1, 2) + 1 == 0, 'b15 root')

# ------------------------------------------------------------ ranking
U = 400000


def u_sim(fn, seed):
    return sim(fn, U, seed)


def disc_sim(cond, seed):
    """Uniform point in the unit disc by rejection from the square; cond takes its radius."""
    rng = random.Random(seed)
    hit = n = 0
    while n < U:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y < 1:
            n += 1
            hit += cond(sqrt(x * x + y * y))
    return hit / n


def tournaments(k):
    """Every result of a round robin of k players: a list of win counts, all equally likely."""
    games = list(combinations(range(k), 2))
    for res in product([0, 1], repeat=len(games)):
        wins = [0] * k
        for (a, b), r in zip(games, res):
            wins[a if r else b] += 1
        yield wins


def tour_frac(k, cond):
    t = list(tournaments(k))
    return F(sum(1 for w in t if cond(w, k)), len(t))


def matrix_frac(cond):
    return F(sum(1 for a, b, c, d in product([0, 1], repeat=4) if cond(a, b, c, d)), 16)


TILES = [(a, b) for a in range(7) for b in range(a, 7)]


def tile_frac(cond):
    assert len(TILES) == 28
    return F(sum(1 for a, b in TILES if cond(a, b)), 28)


def crossing_exact(n):
    """Any four corners give one crossing pair: C(n, 4) of C(diagonals, 2)."""
    return F(comb(n, 4), comb(n * (n - 3) // 2, 2))


def crossing_geom(n):
    """Coordinates of a regular n-gon; count pairs of diagonals whose interiors cross."""
    import math
    P = [(math.cos(2 * pi * i / n), math.sin(2 * pi * i / n)) for i in range(n)]
    diags = [(i, j) for i, j in combinations(range(n), 2) if (j - i) % n not in (1, n - 1)]

    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    cross = 0
    for (a, b), (c, d) in combinations(diags, 2):
        if len({a, b, c, d}) < 4:
            continue  # they meet at a corner, not inside
        o1, o2 = orient(P[a], P[b], P[c]), orient(P[a], P[b], P[d])
        o3, o4 = orient(P[c], P[d], P[a]), orient(P[c], P[d], P[b])
        cross += o1 * o2 < 0 and o3 * o4 < 0
    return F(cross, comb(len(diags), 2))


def dice2_frac(cond):
    return F(sum(1 for a in range(1, 7) for b in range(1, 7) if cond(a * b)), 36)


def painted_frac(k):
    """Small cubes of a 3 x 3 x 3 cube with exactly k painted faces."""
    return F(sum(1 for c in product(range(3), repeat=3) if sum(x in (0, 2) for x in c) == k), 27)


def landing_exact(n):
    """p_n = 1 - p_{n-1} / 2: square n is missed only by stepping 2 from n - 1."""
    p = F(1)  # square 0
    for _ in range(n):
        p = 1 - p / 2
    return p


def landing_enum(n):
    """Every run of n fair coin moves (enough to pass square n)."""
    hit = 0
    for s in product([1, 2], repeat=n):
        pos, seen = 0, set()
        for x in s:
            pos += x
            seen.add(pos)
        hit += n in seen
    return F(hit, 2 ** n)


def mobius(d):
    f = pfs(d)
    return 0 if len(f) != len(set(f)) else (-1) ** len(f)


def coprime_exact(n):
    """Moebius count of coprime pairs in 1..n."""
    return F(sum(mobius(d) * (n // d) ** 2 for d in range(1, n + 1)), n * n)


def coprime_enum(n):
    from math import gcd
    return F(sum(1 for a in range(1, n + 1) for b in range(1, n + 1) if gcd(a, b) == 1), n * n)


def no_friendless_exact(k):
    """Inclusion-exclusion over the set S of friendless people: the pairs touching S are all absent."""
    return sum((-1) ** j * comb(k, j) * F(1, 2 ** (j * (k - j) + comb(j, 2))) for j in range(k + 1))


def graph_frac(k, cond):
    pairs = list(combinations(range(k), 2))
    tot = 0
    for e in product([0, 1], repeat=len(pairs)):
        deg = [0] * k
        for (a, b), x in zip(pairs, e):
            if x:
                deg[a] += 1
                deg[b] += 1
        tot += cond(deg, sum(e))
    return F(tot, 2 ** len(pairs))


def months_with(days):
    import calendar
    return F(sum(1 for m in range(1, 13) if calendar.monthrange(2025, m)[1] == days), 12)


RANK = {
    ('2', 'c01-rank-target'): {'o06': (1 - F(6, 10) ** 2, disc_sim(lambda r: r > 0.6, 21), 0.005),
                               'r07': (F(7, 10) ** 2, disc_sim(lambda r: r < 0.7, 22), 0.005),
                               'r05': (F(1, 2) ** 2, disc_sim(lambda r: r < 0.5, 23), 0.005)},
    ('2', 'c02-rank-unbeaten'): {'top4': (4 * F(1, 2) ** 3, tour_frac(4, lambda w, k: k - 1 in w), 0),
                                 'tb4': (4 * 3 * F(1, 2) ** 5, tour_frac(4, lambda w, k: k - 1 in w and 0 in w), 0),
                                 'cyc3': (F(2, 8), tour_frac(3, lambda w, k: w == [1, 1, 1]), 0)},
    ('2', 'c03-rank-matrix'): {'sym': (F(1, 2), matrix_frac(lambda a, b, c, d: b == c), 0),
                               'inv': (2 * F(1, 4) * F(3, 4), matrix_frac(lambda a, b, c, d: a * d - b * c != 0), 0),
                               'same': (2 * F(1, 2) ** 4, matrix_frac(lambda a, b, c, d: a == b == c == d), 0)},
    ('2', 'c04-rank-dominoes'): {'sum7': (F(6 + 4 + 2, 28), tile_frac(lambda a, b: a + b >= 7), 0),
                                 'gap3': (F(4 + 3 + 2 + 1, 28), tile_frac(lambda a, b: b - a >= 3), 0),
                                 'dbl': (F(7, 28), tile_frac(lambda a, b: a == b), 0)},
    ('2', 'c05-rank-diagonals'): {'pent': (crossing_exact(5), crossing_geom(5), 0),
                                  'hex': (crossing_exact(6), crossing_geom(6), 0),
                                  'hept': (crossing_exact(7), crossing_geom(7), 0)},
    ('2', 'c06-rank'): {'g1': (F(11, 20), series_enum(F(11, 20), 1), 0),
                        'g7': (series_exact(F(11, 20), 7), series_enum(F(11, 20), 7), 0),
                        'g3': (series_exact(F(11, 20), 3), series_enum(F(11, 20), 3), 0)},
    # 2 | ab and 3 | ab by inclusion-exclusion on "no factor 2" (1/2 each die) and "no factor 3" (2/3 each die)
    ('3', 'c01-rank-product'): {'m6': (1 - F(1, 2) ** 2 - F(2, 3) ** 2 + F(1, 3) ** 2, dice2_frac(lambda x: x % 6 == 0), 0),
                                'sq': (F(6 + 2, 36), dice2_frac(lambda x: isqrt(x) ** 2 == x), 0),
                                'end0': (2 * F(1, 6) * F(3, 6), dice2_frac(lambda x: x % 10 == 0), 0)},
    ('3', 'c02-rank-painted'): {'two': (F(12, 27), painted_frac(2), 0),
                                'three': (F(8, 27), painted_frac(3), 0),
                                'one': (F(6, 27), painted_frac(1), 0)},
    ('3', 'c03-rank-landing'): {'sq2': (landing_exact(2), landing_enum(2), 0),
                                'sq4': (landing_exact(4), landing_enum(4), 0),
                                'sq3': (landing_exact(3), landing_enum(3), 0)},
    ('3', 'c04-rank-coprime'): {'cp3': (coprime_exact(3), coprime_enum(3), 0),
                                'cp2': (coprime_exact(2), coprime_enum(2), 0),
                                'cp4': (coprime_exact(4), coprime_enum(4), 0)},
    ('3', 'c05-rank-friends'): {'all4': (no_friendless_exact(4), graph_frac(4, lambda deg, m: min(deg) > 0), 0),
                                'all3': (no_friendless_exact(3), graph_frac(3, lambda deg, m: min(deg) > 0), 0),
                                'tri3': (F(1, 8), graph_frac(3, lambda deg, m: m == 3), 0)},
    ('3', 'c06-rank'): {'m30': (F(4, 12), months_with(30), 0),
                        'r2': (run_exact(4, 2), run_enum(4, 2), 0),
                        'r3': (run_exact(8, 3), run_enum(8, 3), 0)},
}
# values the fix pass wrote, pinned so that a reverted edit fails
PINNED = {('2', 'c01-rank-target'): (F(16, 25), F(49, 100), F(1, 4)), ('2', 'c02-rank-unbeaten'): (F(1, 2), F(3, 8), F(1, 4)),
          ('2', 'c03-rank-matrix'): (F(1, 2), F(3, 8), F(1, 8)), ('2', 'c04-rank-dominoes'): (F(3, 7), F(5, 14), F(1, 4)),
          ('2', 'c05-rank-diagonals'): (F(1, 2), F(5, 12), F(5, 13)), ('3', 'c01-rank-product'): (F(5, 12), F(2, 9), F(1, 6)),
          ('3', 'c02-rank-painted'): (F(4, 9), F(8, 27), F(2, 9)), ('3', 'c03-rank-landing'): (F(3, 4), F(11, 16), F(5, 8)),
          ('3', 'c04-rank-coprime'): (F(7, 9), F(3, 4), F(11, 16)), ('3', 'c05-rank-friends'): (F(41, 64), F(1, 2), F(1, 8)),
          ('3', 'c06-rank'): (F(1, 2), F(107, 256), F(1, 3))}

# ------------------------------------------------------------ intervals
def bo7_len_enum():
    tot = F(0)
    for s in product([0, 1], repeat=7):
        a = b = 0
        for i, g in enumerate(s):
            a += g
            b += 1 - g
            if a == 4 or b == 4:
                tot += F(i + 1, 2 ** 7)
                break
    return tot


def fib(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a


INTV = {
    ('2', 'c07-interval'): (F(7 * 24 * 3600), datetime.timedelta(weeks=1).total_seconds(), 0),
    ('2', 'c08-interval'): (F(3, 2) * F(5, 2) * F(7, 2) * F(9, 2), 1.5 * 2.5 * 3.5 * 4.5, 1e-9),
    ('2', 'c09-interval'): (F(100, 97) + F(100, 103), 2 * sum(0.0009 ** k for k in range(20)), 1e-9),
    ('2', 'c10-interval'): (sum(g * 2 * comb(g - 1, 3) * F(1, 2 ** g) for g in range(4, 8)), bo7_len_enum(), 0),
    ('3', 'c07-interval'): (F(1000, 7), 1000 / 7, 1e-9),
    ('3', 'c08-interval'): (F(factorial(10), 10 ** 6), float(eval('*'.join(str(k) for k in range(1, 11)))) / 1e6, 1e-9),
    ('3', 'c09-interval'): (sum(F(1, k) for k in range(1, 11)), sum(1 / k for k in range(1, 11)), 1e-9),
    ('3', 'c10-interval'): (F(fib(25)), round(((1 + 5 ** .5) / 2) ** 25 / 5 ** .5), 0),
}


def interval_bounds(t):
    lo, hi = t.replace(',', '').split(' to ')
    return F(lo), F(hi)


# ------------------------------------------------------------ run
SEQ_CHECKED = []
for ver, d in (('2', V2), ('3', V3)):
    its = items(d)
    for (v, iid), (rule, second) in SEQ_RULES.items():
        if v != ver:
            continue
        it = its.get(iid)
        check(it is not None, 'missing %s/%s' % (v, iid))
        if it is None:
            continue
        shown = terms_of(it)
        n = len(shown)
        full = [F(x) for x in rule(n + 1)]
        check(full[:n] == shown, '%s/%s shown terms %s do not follow the rule %s' % (v, iid, shown, full[:n]))
        exact = full[n]
        alt = F(second(shown))
        key, wrongs = key_and_wrongs(it)
        check(exact == key, '%s/%s key %s, rule gives %s' % (v, iid, key, exact))
        check(alt == key, '%s/%s second method gives %s, key %s' % (v, iid, alt, key))
        check(all(w != key for w in wrongs), '%s/%s a distractor equals the key' % (v, iid))
        check(len(set(wrongs)) == 3, '%s/%s distractors repeat' % (v, iid))
        check(5 <= n <= 9, '%s/%s shows %d terms' % (v, iid, n))
        for fam, pred in v1_predictors(shown).items():
            check(pred == key, '%s/%s v1 family %s fits the shown terms and predicts %s' % (v, iid, fam, pred))
        for fam, pred in rivals(shown).items():
            check(pred == key, '%s/%s rival rule "%s" fits the shown terms and predicts %s' % (v, iid, fam, pred))
        SEQ_CHECKED.append((v, iid))
    for (v, iid), (exact, second, tol) in PROB.items():
        if v != ver:
            continue
        it = its[iid]
        key, wrongs = key_and_wrongs(it)
        check(exact == key, '%s/%s key %s, exact %s' % (v, iid, key, exact))
        check(near(second, key, tol) if tol else F(second) == key, '%s/%s second method %s, key %s' % (v, iid, second, key))
        check(all(w != key for w in wrongs) and len(set(wrongs)) == 3, '%s/%s distractor clash' % (v, iid))
    for (v, iid), lines in RANK.items():
        if v != ver:
            continue
        it = its[iid]
        w = it['widget']
        vals = {}
        for lid, (exact, second, tol) in lines.items():
            check(near(second, exact, tol if tol else 1e-12), '%s/%s %s second method %s vs %s' % (v, iid, lid, second, exact))
            vals[lid] = float(exact)
        check(sorted(vals) == sorted(l['id'] for l in w['lines']), '%s/%s line ids' % (v, iid))
        order = sorted(vals, key=lambda k: -vals[k])
        check(w['answer'] == order, '%s/%s answer %s, values give %s' % (v, iid, w['answer'], order))
        gaps = [vals[order[i]] - vals[order[i + 1]] for i in range(2)]
        check(min(gaps) >= 0.02, '%s/%s gap %.4f below 0.02' % (v, iid, min(gaps)))
        if (v, iid) in PINNED:
            check(tuple(lines[k][0] for k in order) == PINNED[(v, iid)], '%s/%s values differ from the fix pass' % (v, iid))
        fb = ', '.join('%.3f' % vals[k] for k in order)
        check(fb in it['feedback']['correct'], '%s/%s feedback values %s' % (v, iid, fb))
    for (v, iid), (exact, second, tol) in INTV.items():
        if v != ver:
            continue
        it = its[iid]
        check(near(second, exact, tol), '%s/%s second method %s vs %s' % (v, iid, second, exact))
        ops = it['widget']['options']
        holds = []
        for o in ops:
            lo, hi = interval_bounds(o['text'])
            h = lo <= exact <= hi
            check(h == ('below' not in o.get('why', '') and 'above' not in o.get('why', '')), '%s/%s option %s hold mismatch' % (v, iid, o['text']))
            if h:
                holds.append((hi - lo, o))
        holds.sort(key=lambda x: x[0])
        check(len(holds) == 2 and holds[0][0] < holds[1][0], '%s/%s needs one narrow and one wide holder' % (v, iid))
        check(holds[0][1].get('correct') is True, '%s/%s narrowest holder is not the key' % (v, iid))
        narrow = [hi - lo for lo, hi in (interval_bounds(o['text']) for o in ops) if hi - lo < holds[1][0]]
        check(len(narrow) == 3 and len(set(narrow)) == 1, '%s/%s three narrow options of one width' % (v, iid))
        misses = [o for o in ops if not (interval_bounds(o['text'])[0] <= exact <= interval_bounds(o['text'])[1])]
        check(any(interval_bounds(o['text'])[1] < exact for o in misses) and any(interval_bounds(o['text'])[0] > exact for o in misses),
              '%s/%s misses must sit one each side' % (v, iid))

# ------------------------------------------------------------ structure and freshness across versions
def fams(d):
    return {t for it in items(d).values() for t in it['tags']} - {'sequence', 'likelihood-ranking', 'interval'}


def ramp(d):
    return [(p['id'], [(it['difficulty'], it['skills'][0], it['widget']['kind']) for it in p['items']]) for p in d['parts'][:3]]


for name, d in (('2', V2), ('3', V3)):
    check(ramp(d) == ramp(V1), 'version %s: difficulty, skill or widget per position differs from version 1' % name)
    for k in ('style', 'models', 'requires', 'skills'):
        check(d[k] == V1[k], 'version %s field %s differs' % (name, k))
    check([{x: p[x] for x in p if x != 'items'} for p in d['parts']] == [{x: p[x] for x in p if x != 'items'} for p in V1['parts']],
          'version %s part headers differ' % name)
    check(len(items(d)) == 40, 'version %s item count' % name)
check(not (fams(V2) & fams(V1)), 'v2 shares families with v1: %s' % (fams(V2) & fams(V1)))
check(not (fams(V3) & fams(V1)), 'v3 shares families with v1: %s' % (fams(V3) & fams(V1)))
check(not (fams(V2) & fams(V3)), 'v2 and v3 share families: %s' % (fams(V2) & fams(V3)))
qs = lambda d: {it['question'] for it in items(d).values() if not it['question'].startswith('Put the three')}
check(not (qs(V2) & qs(V1)) and not (qs(V3) & qs(V1)) and not (qs(V2) & qs(V3)), 'a question text repeats across versions')
lines = lambda d: {l['text'] for it in items(d).values() if it['widget']['kind'] == 'order' for l in it['widget']['lines']}
check(not (lines(V2) & lines(V1)) and not (lines(V3) & lines(V1)) and not (lines(V2) & lines(V3)), 'a ranking event repeats across versions')
check(len(SEQ_RULES) == 30 and len(PROB) == 30 and len(RANK) == 12 and len(INTV) == 8, 'not every item is covered')
check(sorted(SEQ_CHECKED) == sorted((v, it['id']) for v, d in (('2', V2), ('3', V3)) for it in d['parts'][0]['items']),
      'the rival-rule check did not run over every sequence item')

if FAILS:
    print('\n'.join(FAILS))
    print('FAIL: %d problem(s)' % len(FAILS))
    sys.exit(1)
print('OK: 80 keys recomputed twice (30 sequences, 30 probability, 12 rankings with 36 events, 8 intervals); '
      'distractors differ; ranking gaps >= 0.02; one narrowest interval each; no shared family across versions')
