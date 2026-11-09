"""Search each 'what comes next' item for a second simple rule that fits the shown terms.

Rules tried (each must be over-determined: more shown terms than free parameters + 1):
constant difference, constant ratio, polynomial of degree 2 and 3 (difference tables),
a_n = r a_{n-1} + c, linear recurrences of order 2 and 3 with a constant (rational
coefficients fitted exactly, kept only when they fit every remaining term),
differences that form a geometric sequence, two and three interleaved strands
(each arithmetic or geometric), and periodic repetition of a block.
Prints every fitting rule whose next term differs from the key, and whether that
value is one of the options.

Usage: python seq_rivals.py <repo root>
"""
import json
import re
import sys
from fractions import Fraction as F
from itertools import product

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'


def nums(q):
    q = q.split('?', 1)[1] if q.startswith('What comes next?') else q
    q = q.replace('What comes next?', '')
    m = re.findall(r'\\tfrac\{?(\d+)\}?\{?(\d+)\}?', q)
    if m:
        return [F(int(a), int(b)) for a, b in m], True
    return [F(x) for x in re.findall(r'\d+(?:\.\d+)?', q)], False


def solve(rows, rhs):
    n = len(rows[0])
    A = [list(r) + [b] for r, b in zip(rows, rhs)]
    for c in range(n):
        piv = next((i for i in range(c, len(A)) if A[i][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        for i in range(len(A)):
            if i != c and A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def rules(s):
    out = []
    n = len(s)
    # polynomial via difference table, degree k needs n >= k + 2
    for k in range(0, 4):
        if n < k + 2:
            continue
        rows = [s]
        for _ in range(k + 1):
            rows.append([b - a for a, b in zip(rows[-1], rows[-1][1:])])
        if all(x == 0 for x in rows[k + 1]):
            nxt = rows[k][-1]
            for j in range(k - 1, -1, -1):
                nxt = rows[j][-1] + nxt
            out.append((f'polynomial degree {k}', nxt))
    # constant ratio
    if all(x != 0 for x in s[:-1]):
        r = [b / a for a, b in zip(s, s[1:])]
        if len(set(r)) == 1:
            out.append(('constant ratio', s[-1] * r[0]))
        # ratios form arithmetic
        if len(r) >= 3 and len({b - a for a, b in zip(r, r[1:])}) == 1:
            out.append(('ratios arithmetic', s[-1] * (r[-1] + r[1] - r[0])))
    # differences geometric
    d = [b - a for a, b in zip(s, s[1:])]
    if len(d) >= 3 and all(x != 0 for x in d[:-1]):
        rr = {b / a for a, b in zip(d, d[1:])}
        if len(rr) == 1:
            out.append(('differences geometric', s[-1] + d[-1] * rr.pop()))
    # linear recurrences a_n = sum c_i a_{n-i} + c0, order 1..3
    for order in (1, 2, 3):
        npar = order + 1
        eqs = [(s[i - order:i][::-1] + [F(1)], s[i]) for i in range(order, n)]
        if len(eqs) < npar + 1:
            continue
        for start in range(len(eqs) - npar + 1):
            sub = eqs[start:start + npar]
            c = solve([e[0] for e in sub], [e[1] for e in sub])
            if c is None:
                continue
            if all(sum(a * b for a, b in zip(e[0], c)) == e[1] for e in eqs):
                nxt = sum(a * b for a, b in zip(s[-order:][::-1] + [F(1)], c))
                out.append((f'recurrence order {order} coeffs {[str(x) for x in c]}', nxt))
                break
    # also homogeneous order 2 and 3 (no constant) where too few terms for the constant form
    for order in (2, 3):
        eqs = [(s[i - order:i][::-1], s[i]) for i in range(order, n)]
        if len(eqs) < order + 1:
            continue
        c = solve([e[0] for e in eqs[:order]], [e[1] for e in eqs[:order]])
        if c and all(sum(a * b for a, b in zip(e[0], c)) == e[1] for e in eqs):
            nxt = sum(a * b for a, b in zip(s[-order:][::-1], c))
            out.append((f'homogeneous order {order} coeffs {[str(x) for x in c]}', nxt))
    # interleaved strands
    for m in (2, 3):
        strands = [s[i::m] for i in range(m)]
        nxt_strand = strands[n % m]
        others = [st for i, st in enumerate(strands)]
        if min(len(st) for st in strands) < 2 or len(nxt_strand) < 3:
            continue
        ok_all = True
        for st in others:
            dd = {b - a for a, b in zip(st, st[1:])}
            rr = {b / a for a, b in zip(st, st[1:])} if all(st[:-1]) else set()
            if len(dd) != 1 and len(rr) != 1:
                ok_all = False
        if ok_all:
            st = nxt_strand
            dd = {b - a for a, b in zip(st, st[1:])}
            if len(dd) == 1:
                out.append((f'{m} strands, arithmetic', st[-1] + dd.pop()))
            else:
                rr = {b / a for a, b in zip(st, st[1:])}
                out.append((f'{m} strands, geometric', st[-1] * rr.pop()))
    # periodic block, period p with at least three repeated terms shown
    for p in range(1, n - 2):
        if all(s[i] == s[i - p] for i in range(p, n)):
            out.append((f'period {p}', s[n - p]))
            break
    return out


def isprime(k):
    return k > 1 and all(k % q for q in range(2, int(k ** 0.5) + 1))


def factors(k):
    out, q = [], 2
    while q * q <= k:
        while k % q == 0:
            out.append(q)
            k //= q
        q += 1
    if k > 1:
        out.append(k)
    return out


def ndiv(k):
    return sum(1 for q in range(1, k + 1) if k % q == 0)


def dsum(k):
    return sum(map(int, str(k)))


PRED = {
    'prime': isprime,
    'not prime': lambda k: not isprime(k),
    'composite': lambda k: k > 1 and not isprime(k),
    'not a prime above 3': lambda k: not (isprime(k) and k > 3),
    'not a prime above 5': lambda k: not (isprime(k) and k > 5),
    'squarefree': lambda k: len(set(factors(k))) == len(factors(k)),
    'not a square': lambda k: int(k ** 0.5) ** 2 != k,
    'not a perfect power': lambda k: not any(round(k ** (1 / e)) ** e == k for e in range(2, 8)),
    'no prime factor above 3': lambda k: all(q <= 3 for q in factors(k)),
    'no prime factor above 5': lambda k: all(q <= 5 for q in factors(k)),
    'multiple of 3 or 5': lambda k: k % 3 == 0 or k % 5 == 0,
    'multiple of 3 or 5, not 15': lambda k: (k % 3 == 0) != (k % 5 == 0),
    'not coprime to 15': lambda k: k % 3 == 0 or k % 5 == 0,
    'not 1 mod 3': lambda k: k % 3 != 1,
    'semiprime': lambda k: len(factors(k)) == 2,
    'two different primes': lambda k: len(factors(k)) == 2 and len(set(factors(k))) == 2,
    'four divisors': lambda k: ndiv(k) == 4,
    'even divisor count': lambda k: ndiv(k) % 2 == 0,
    'digit sum 5': lambda k: dsum(k) == 5,
    'digit sum 5 or 14': lambda k: dsum(k) in (5, 14),
    'digit root 5': lambda k: k % 9 == 5,
    'digits 1, 2 only': lambda k: set(str(k)) <= set('12'),
    'digits 1, 2, 3 only': lambda k: set(str(k)) <= set('123'),
    'no digit above 2': lambda k: set(str(k)) <= set('012'),
    'prime ending in 3': lambda k: isprime(k) and k % 10 == 3,
    'ends in 3, not a multiple of 3': lambda k: k % 10 == 3 and k % 3 != 0,
    'ends in 3, prime or 3': lambda k: k % 10 == 3 and (isprime(k)),
    'ends in 3, not 33 or 63 pattern (not multiple of 3 or 11)': lambda k: k % 10 == 3 and k % 3 != 0 and k % 11 != 0,
    'sum of two squares': lambda k: any(int((k - a * a) ** 0.5) ** 2 == k - a * a for a in range(int(k ** 0.5) + 1)),
}


def filters(s):
    out = []
    for name, f in PRED.items():
        inside = [k for k in range(s[0], s[-1] + 1) if f(k)]
        if inside == s:
            k = s[-1] + 1
            while not f(k):
                k += 1
            out.append((f'filter: {name}', k))
    return out


def opt_val(t, frac):
    t = t.strip('$')
    m = re.findall(r'\\tfrac\{?(\d+)\}?\{?(\d+)\}?', t)
    if m:
        a, b = m[0]
        return F(int(a), int(b))
    try:
        return F(t.replace(',', ''))
    except ValueError:
        return None


for v in ('', '-2', '-3'):
    d = json.load(open(f'{ROOT}/app/content/exams/mock-oa-trader{v}.json'))
    for it in d['parts'][0]['items']:
        s, frac = nums(it['question'])
        opts = it['widget']['options']
        key = next(opt_val(o['text'], frac) for o in opts if o.get('correct'))
        vals = {opt_val(o['text'], frac) for o in opts}
        found = rules(s) if not frac else []
        if frac:  # numerators and denominators as two sequences
            for part, name in (([x.numerator for x in s], 'num'), ([x.denominator for x in s], 'den')):
                for r, nx in rules([F(x) for x in part]):
                    found.append((f'{name}: {r}', nx))
        if not frac and all(x.denominator == 1 for x in s) and all(b > a for a, b in zip(s, s[1:])):
            for r, nx in filters([int(x) for x in s]):
                found.append((r, F(nx)))
        rivals = [(r, nx) for r, nx in found if not frac and nx != key]
        tag = f'v{v or "-1"} {it["id"]}'
        if rivals:
            for r, nx in rivals:
                print(f'{tag}: {r} -> {nx}' + ('  [AN OPTION]' if nx in vals else ''))
        else:
            print(f'{tag}: no rival among the simple rules ({len(found)} rule(s) agree with the key)')

# The sequences the review proposes as fixes, run through the same search.
print('--- proposed fixes')
for name, s, key in [('v2 a05 fix', [4, 11, 30, 85, 248], 735),
                     ('v2 a08 fix', [1, 2, 3, 4, 6, 8, 9, 12], 16),
                     ('v3 a13 fix', [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1], 4)]:
    S = [F(x) for x in s]
    found = rules(S)
    if all(b > a for a, b in zip(s, s[1:])):
        found += [(r, F(nx)) for r, nx in filters(s)]
    bad = [(r, str(nx)) for r, nx in found if nx != key]
    print(name, bad or 'no rival', '| agree:', [r for r, nx in found if nx == key])
