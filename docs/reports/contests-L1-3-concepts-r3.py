#!/usr/bin/env python3
"""Concept audit, round 3: contests levels 1 to 3 (lessons l1 to l12, review-1..3, homework-1..3).

Recomputes, with reference code written for this audit (not the content's solutions), every graded key, slip, stated
figure and hidden-test expectation that the ledger cites as "script", and runs the Monte Carlo checks for the empirical
claims. Exit 0 means every check passed. A check that fails because the content is wrong stays failing: each such line
is a finding in docs/reviews/audit-contests-1-3-r3.md (the finding number is in the check name).

Run from anywhere:  python docs/reports/contests-L1-3-concepts-r3.py      (about one minute, standard library only)
Not covered here (see the audit file, section "Code feedback sweep"): which hidden test a named mistake fails first
(Pyodide, through app/tools/code-runner.mjs), the C++ widgets (YoWASP clang 21 for wasm32) and the pytest widget.
"""
import bisect, heapq, io, itertools, json, math, os, random, re, sys
from collections import Counter, deque

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'contests')
FAILS, COUNT = [], [0]


def load(name):
    return json.load(open(os.path.join(CDIR, name + '.json'), encoding='utf-8'))


def check(name, cond, detail=''):
    COUNT[0] += 1
    if not cond:
        FAILS.append(name)
        print('FAIL  %s  %s' % (name, detail))


L = {k: load(k) for k in ['l1-reading-statements', 'l2-limits-to-complexity', 'l3-fast-io', 'l4-stress-testing', 'l5-modulo',
                          'l6-gcd-and-primes', 'l7-counting-mod', 'l8-invariants', 'l9-constructive', 'l10-greedy-proofs',
                          'l11-bitmasks', 'l12-difference-arrays', 'review-1', 'review-2', 'review-3', 'homework-1',
                          'homework-2', 'homework-3']}
P = 10 ** 9 + 7


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):   # deterministic below 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def widget(file, kind, i):
    return L[file][kind][i]['widget']


def run_tests(tag, w, ref_src, source_text=''):
    """Every hidden test and example of a Python function widget, against reference code written for this audit."""
    ns = {'__learner_source__': source_text}
    exec(w.get('prelude', ''), ns)
    exec(ref_src, ns)
    for group in ('examples', 'tests'):
        for k, t in enumerate(w.get(group, [])):
            name = '%s %s[%d]' % (tag, group, k)
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns); check(name, False, 'no exception')
                    except Exception as e:
                        check(name, type(e).__name__ == t['expect'], type(e).__name__)
                    continue
                got = eval(t['call'], ns)
                want = eval(t['expect'], ns) if isinstance(t['expect'], str) else t['expect']
                check(name, got == want, 'got %r want %r' % (got, want))
            except Exception as e:
                check(name, False, repr(e)[:120])


# ============================================================ l1
def highs(xs):
    return sum(1 for x, m in zip(xs, [None] + list(itertools.accumulate(xs, max))) if m is None or x > m)


check('l1 s2 fresh highs of the example', [i + 1 for i, x in enumerate([3, 1, 4, 1, 5, 9]) if all(x > y for y in [3, 1, 4, 1, 5, 9][:i])] == [1, 3, 5, 6])
check('l1 s4 key and slips', 2 * 10 ** 5 == 200000 and 10 ** 4 * 2 * 10 ** 5 == 2000000000)
check('l1 s5 sizes', 2 * 10 ** 5 * 10 ** 9 == 2 * 10 ** 14 > 2 ** 31 - 1 == 2147483647 and 2 ** 32 - 1 < 4.3e9 and 2 ** 63 - 1 > 9.2e18)
check('l1 s6 flat week', highs([7, 7, 7, 7]) == 1 and highs([7]) == 1)
check('l1 s7 worst week', highs([-5, -3, -4]) == 2)


def best0(xs):
    c, b = 0, 0
    for x in xs:
        if x > b:
            c += 1; b = x
    return c


check('l1 s7 best = 0 prints 0', best0([-5, -3, -4]) == 0 and best0([-10 ** 9]) == 0)
check('l1 s11 total', 10 ** 5 * 10 ** 6 == 10 ** 11 > 2.1e9)
check('l1 quiz1', 3 * 10 ** 5 - 9999 == 290001 and 3 * 10 ** 5 // 10 ** 4 == 30)
check('l1 quiz3', sum(1 for i, x in enumerate([2, 2, 1, 3]) if all(x >= y for y in [2, 2, 1, 3][:i])) == 3 and highs([2, 2, 1, 3]) == 2)
run_tests('l1 s9 parse', widget('l1-reading-statements', 'screens', 9), '''
import re
def parse(text):
    v = [int(x) for x in re.findall(r'-?[0-9]+', text)]
    t, out, i = v[0], [], 1
    while len(out) < t:
        out.append(v[i + 1:i + 1 + v[i]]); i += 1 + v[i]
    return t, out
''')
run_tests('l1 s10 new_highs', widget('l1-reading-statements', 'screens', 10), '''
import itertools
def new_highs(xs):
    m = list(itertools.accumulate(xs, max))
    return sum(1 for i in range(len(xs)) if i == 0 or xs[i] > m[i - 1])
''')

# ============================================================ l2
n = 2 * 10 ** 5
check('l2 s0 step counts', abs(n * (n + 1) * (n + 2) / 6 - 1.3e15) < 0.05e15 and n * n // 2 == 2 * 10 ** 10)
r = random.Random(1)
ok = True
for _ in range(300):
    a = [r.randint(-9, 9) for _ in range(r.randint(1, 8))]
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x); best = max(best, cur)
    ok &= best == max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1))
check('l2 s0 the single pass is the largest stretch (300 random lists)', ok)
lo, hi = 2, 10 ** 8
while lo < hi:
    mid = (lo + hi + 1) // 2
    if mid * math.log2(mid) <= 10 ** 8: lo = mid
    else: hi = mid - 1
check('l2 s1 key and slips', math.isqrt(10 ** 8) == 10000 and math.isqrt(10 ** 7) == 3162 and lo == 4523071, str(lo))
check('l2 s1 explain', abs(n * math.log2(n) - 3.5e6) < 0.05e6)
check('l2 s2 hints', 2 ** 20 == 1048576 and 500 ** 3 == 125000000 and 5000 ** 2 == 25000000)
check('l2 s3', 2 ** 20 == 1048576 and 20 * 2 ** 20 < 2.2e7)
check('l2 s4', 5000 * 4999 // 2 == 12497500 and 5000 ** 2 == 25000000 and 5000 * 4999 == 24995000)
vals, k = 10 ** 9 + 1, 0
while vals > 1:
    vals = (vals + 1) // 2; k += 1          # keep the larger half
check('l2 s5 halvings', k == 30 and 2 ** 29 == 536870912 < 10 ** 9 + 1 <= 2 ** 30 == 1073741824 and round(math.sqrt(10 ** 9)) == 31623)
check('l2 s6', (2 * 10 ** 5) ** 2 == 4 * 10 ** 10 and 10 ** 4 * 20 ** 2 == 4 * 10 ** 6 and 10 ** 4 * (2 * 10 ** 5) ** 2 == 4 * 10 ** 14)
check('l2 s9 boundaries', 2 ** 26 <= 10 ** 8 < 2 ** 27 and 464 ** 3 <= 10 ** 8 < 465 ** 3 == 100544625)
check('l2 s11 and quiz', 10 ** 12 // 2 == 5 * 10 ** 11 and abs(10 ** 6 * math.log2(10 ** 6) - 2e7) < 1e5 and 400 ** 3 == 64000000 and abs(math.log2(10 ** 6) - 19.9) < 0.05)
run_tests('l2 s9 budget_class', widget('l2-limits-to-complexity', 'screens', 9), '''
from math import log2
def budget_class(n):
    B = 10 ** 8
    if n.bit_length() <= 8 and (1 << n) <= B: return "2^n"
    for name, f in (("n^3", n * n * n), ("n^2", n * n), ("n log n", n * log2(n)), ("n", n)):
        if f <= B: return name
    return "log n"
''')
run_tests('l2 s10 pair_sums_at_most', widget('l2-limits-to-complexity', 'screens', 10), '''
import bisect
def pair_sums_at_most(xs, k):
    a = sorted(xs)
    return sum(max(0, bisect.bisect_right(a, k - a[i], 0, i)) for i in range(len(a)))
''')
tb = widget('l2-limits-to-complexity', 'screens', 2)
fb = L['l2-limits-to-complexity']['screens'][2]['feedback']['byKey']
check('FINDING 2: l2 s2 feedback r0c1 says "not the slowest that fits", but O(n 2^n) is slower and fits (20 * 2^20 < 1e8)',
      not ('not the slowest that fits' in fb['r0c1'] and 20 * 2 ** 20 <= 10 ** 8 and not any(re.search(r'n\s*\*?\s*2', a) for a in tb['rows'][0][1].get('accept', []))))
check('FINDING 3: l2 s2 feedback r4c1 says "too slow" for every wrong entry, including the faster O(1)', 'too slow' not in fb['r4c1'])

# ============================================================ l3
toks = '3\n2\n5 7\n1\n-4\n3\n1 2 3'.split()
pos, starts = 1, []
for _ in range(int(toks[0])):
    starts.append(pos); pos += 1 + int(toks[pos])
check('l3 s1 index of the third n', starts == [1, 4, 6] and len(toks) == 10)
check('l3 s3 grid tokens', '3 4\n#..#\n.##.\n....'.split() == ['3', '4', '#..#', '.##.', '....'] and b'#..#'[0] == ord('#'))


def trap_program(text):
    src, out = io.StringIO(text), []
    t = int(src.readline())
    for _ in range(t):
        _n = int(src.readline())
        a = list(map(int, src.readline().split()))
        out.append('%d %d' % (sum(a), max(a)))
    return out


check('l3 s6 the line reader prints 5 4 then 2 2', trap_program('2\n3\n4 1\n5\n2\n-1 -2\n') == ['5 4', '2 2'])
q2 = L['l3-fast-io']['quiz'][2]
text = '2\n\n5 -3'
check('l3 quiz2 key and blank slip', len(text.split()) == 3 and len(text.split('\n')) - 1 + 2 == 4)
lines_with_text = sum(1 for ln in text.split('\n') if ln.strip())
words_first_line = len(text.split('\n')[0].split())
slip = [w for w in q2['widget']['wrong'] if w['id'] == 'lines'][0]['value']
check('FINDING 1: l3 quiz[2] slip "lines" (2): feedback names "words on the first line only", which gives %d' % words_first_line,
      not ('first line only' in q2['feedback']['byKey']['lines'] and words_first_line != slip), 'lines with text = %d' % lines_with_text)
check('l3 quiz3 bytes against text', (b'3' == '3') is False and int(b'3') == 3 and int(b'12') == 12)


def prog_s(stdin):
    v = [int(x) for x in re.findall(r'-?\d+', stdin)]
    out, i = [], 1
    for _ in range(v[0]):
        a = v[i + 1:i + 1 + v[i]]; i += 1 + v[i]
        out.append('%d %d' % (sum(a), max(a)))
    return '\n'.join(out)


for s in (9, 10):
    for k, t in enumerate(widget('l3-fast-io', 'screens', s)['tests']):
        check('l3 s%d problem S expected output, test %d' % (s, k + 1), prog_s(t['stdin']).split() == t['expect'].split())
run_tests('l3 s8 read_tokens', widget('l3-fast-io', 'screens', 8), '''
import re
def read_tokens(data):
    return (int(m.group()) for m in re.finditer(rb'-?[0-9]+', data))
''')

# ============================================================ l4
def gen_pairs(rng, hi=10, khi=20):
    m = rng.randint(1, 6)
    xs = [rng.randint(1, hi) for _ in range(m)]
    return xs, rng.randint(2, khi)


def count_pairs_le(xs, k, strict=False):
    return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if (xs[i] + xs[j] < k if strict else xs[i] + xs[j] <= k))


rng = random.Random(1)
rows = [gen_pairs(rng) for _ in range(5)]
check('l4 s1 the five seed-1 cases', rows == [([10, 2], 10), ([8], 16), ([7, 4, 2, 8], 2), ([7, 10, 1, 8], 10), ([4, 10, 2, 6, 1, 1], 2)], str(rows))
check('l4 s1 counts', [(count_pairs_le(x, k, True), count_pairs_le(x, k)) for x, k in rows] == [(0, 0), (0, 0), (0, 0), (2, 2), (0, 1)])
check('l4 s4 shrink options', (count_pairs_le([1, 1], 2, True), count_pairs_le([1, 1], 2)) == (0, 1) and count_pairs_le([6, 1, 1], 3, True) == count_pairs_le([6, 1, 1], 3) and count_pairs_le([4, 10], 2) == 0)
# Monte Carlo: gen A (values to 1e9) against the strict bug, four seeds of 100,000 trials; gen B finds it on trial 5
found = 0
for seed in (1, 2, 3, 4):
    rng = random.Random(seed)
    for _ in range(100000):
        xs, k = gen_pairs(rng, 10 ** 9, 2 * 10 ** 9)
        if any(xs[i] + xs[j] == k for i in range(len(xs)) for j in range(i + 1, len(xs))):
            found += 1
check('l4 s3 Monte Carlo: gen A finds no tie in 4 x 100,000 trials', found == 0, 'ties found: %d' % found)
check('l4 quiz2', count_pairs_le([2, 3, 3], 6, True) == 2 and count_pairs_le([2, 3, 3], 6) == 3)
run_tests('l4 s7 stress', widget('l4-stress-testing', 'screens', 7), '''
import copy, random
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    cases = [gen(rng) for _ in range(trials)]
    bad = [c for c in cases if fast(copy.deepcopy(c)) != brute(copy.deepcopy(c))]
    return bad[0] if bad else None
''')
check('l4 s9 last day move', abs((100.50 - 99.25) - 1.25) < 1e-9)

# ============================================================ l5
check('l5 s0', [pow(7, k, 10) for k in (1, 2, 3, 4, 5, 2031)] == [7, 9, 3, 1, 7, 3] and 2031 == 4 * 507 + 3 and abs(10 ** 18 * math.log10(2) - 3e17) < 0.02e17)
check('l5 s2', 38 * 45 == 1710 == 244 * 7 + 2 and 38 % 7 == 45 % 7 == 3)
tab = L['l5-modulo']['screens'][3]['canvas']['params']['rows']
check('l5 s3 product table modulo 7', all(int(tab[a - 1][b]) == a * b % 7 for a in range(1, 7) for b in range(1, 7)))
check('l5 s3 inverses', [next(b for b in range(1, 7) if a * b % 7 == 1) for a in range(1, 7)] == [1, 4, 5, 2, 3, 6] and 5 * 2 % 7 == 12 // 4)
check('l5 s4', 3 ** 5 == 243 == 34 * 7 + 5 and 3 * 5 % 7 == 1)
check('l5 s5', pow(3, 8, 7) == 2 and pow(3, 13, 7) == 3 and (10 ** 18).bit_length() == 60 and 2 ** 59 < 10 ** 18 < 2 ** 60)
check('l5 s9', 5 ** 5 == 3125 == 446 * 7 + 3 and 2 * 3 % 7 == 30 // 5 and 2 // 5 == 0)
h = 0
for x in (5, 10 ** 9, 3):
    h = (31 * h + x) % P
h2 = 0
for x in (5, 10 ** 9, 3):
    h2 = 31 * h2 + x
check('l5 s11 checksum and slips', h == 4591 and h2 == 31000004808 and 31 * 148 == 4588)
check('l5 quiz', -3 % 7 == 4 and 4 * 3 % 11 == 1 and pow(4, 9, 11) == 3 and is_prime(P) and is_prime(2 ** 31 - 1) and P < 2 ** 30 and pow(2, -1, P) == 500000004)
w58 = widget('l5-modulo', 'screens', 8)
check('l5 s8 mul_mod expectations', all((t['args'][0] * t['args'][1]) % t['args'][2] == t['expect'] for t in w58['tests']))
run_tests('l5 s6 power_mod', widget('l5-modulo', 'screens', 6), '''
def power_mod(a, e, m):
    r = 1 % m
    for bit in bin(e)[2:]:
        r = r * r % m
        if bit == '1':
            r = r * a % m
    return r
''')
run_tests('l5 s7 inverse_mod', widget('l5-modulo', 'screens', 7), '''
def inverse_mod(a, p):
    r0, r1, s0, s1 = a % p, p, 1, 0          # extended Euclid, not Fermat
    while r1:
        q = r0 // r1
        r0, r1, s0, s1 = r1, r0 - q * r1, s1, s0 - q * s1
    if r0 != 1:
        raise ValueError('no inverse')
    return s0 % p
''')

# ============================================================ l6
def steps(a, b):
    c = 0
    while b:
        a, b = b, a % b; c += 1
    return c


fib = [0, 1]
while len(fib) < 90:
    fib.append(fib[-1] + fib[-2])
check('l6 s0', math.lcm(84, 36) == 252 == 7 * 36 == 3 * 84 and 84 * 36 // 252 == 12)
check('l6 s2', math.gcd(1071, 462) == 21 and 1071 % 462 == 147 and 462 % 147 == 21 and 1071 == 51 * 21 and 462 == 22 * 21)
check('l6 s4 Fibonacci worst case', steps(89, 55) == 9 and fib[88] == 1100087778366101931 and fib[87] == 679891637638612258 and steps(fib[88], fib[87]) == 86)
flags = bytearray([1]) * (2 * 10 ** 6 + 1)
flags[0] = flags[1] = 0
for p in range(2, 1415):
    if flags[p]:
        flags[p * p::p] = bytearray(len(flags[p * p::p]))
check('l6 s7 prime counts and sum', sum(flags[:10 ** 6 + 1]) == 78498 and sum(flags) == 148933 and sum(i for i in range(1500000) if flags[i]) == 82074443256 and sum(flags[:101]) == 25)
s6 = L['l6-gcd-and-primes']['screens'][6]
cell = lambda cid: (int(cid[1:cid.index('c')]) - 1) * 10 + int(cid[cid.index('c') + 1:])
dim = sorted(cell(c) for c in s6['canvas']['state']['dim'])
check('l6 s6 dim set and key', dim == [m for m in range(1, 101) if m == 1 or (m > 5 and (m % 2 == 0 or m % 3 == 0 or m % 5 == 0)) or m == 4] and sorted(cell(c) for c in s6['widget']['answer']) == [49, 77, 91], str(dim[:12]))
check('l6 s8', is_prime(1000003) and math.isqrt(1000003) == 1000 and 1000003 // 2 == 500001)
check('l6 s9 primes', is_prime(999983) and is_prime(999999999989))
check('l6 s11 and quiz', math.lcm(14, 21) == 42 and math.lcm(6, 10) == 30 and sum(flags[:31]) == 10 and 13 ** 2 <= 200 < 17 ** 2)


def no_sqrt_turns(m):
    d, turns = 2, 0
    while m > 1 and turns < 5 * 10 ** 6:
        while m % d == 0:
            m //= d
        d += 1; turns += 1
    return turns


how = L['l6-gcd-and-primes']['screens'][9]['widget']['how']
check('FINDING 4: l6 s9 `how` says trial division up to n is stopped on all three values near 1e12; the usual loop finishes two of them in about 1e6 turns',
      not ('is stopped on those' in how and no_sqrt_turns(999983 * 999983) < 2 * 10 ** 6 and no_sqrt_turns(999983 * 1000003) < 2 * 10 ** 6))
run_tests('l6 s5 gcd', widget('l6-gcd-and-primes', 'screens', 5), '''
from functools import reduce
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
def gcd_all(xs):
    return reduce(gcd, xs, 0)
''')
run_tests('l6 s7 sieve', widget('l6-gcd-and-primes', 'screens', 7), '''
def sieve(n):
    if n < 2: return []
    f = bytearray([1]) * (n + 1); f[0] = f[1] = 0
    for p in range(2, int(n ** 0.5) + 2):
        if f[p]:
            f[2 * p::p] = bytearray(len(f[2 * p::p]))      # from 2p: still correct
    return [i for i in range(n + 1) if f[i]]
''')
run_tests('l6 s9 factorise', widget('l6-gcd-and-primes', 'screens', 9), '''
def factorise(n):
    out = []
    for d in [2] + list(range(3, 1000100, 2)):
        if d * d > n: break
        while n % d == 0:
            out.append(d); n //= d
    return out + ([n] if n > 1 else [])
''')

# ============================================================ l7
check('l7 s0 s1', math.comb(4, 2) == 6 and math.comb(5, 2) == 10 and math.comb(6, 3) == 20 and len(str(math.comb(2000, 1000))) == 601)
f13 = [math.factorial(k) % 13 for k in range(7)]
i13 = [pow(x, -1, 13) for x in f13]
check('l7 s2 s3 tables modulo 13', f13 == [1, 1, 2, 6, 11, 3, 5] and i13 == [1, 1, 7, 11, 6, 9, 8] and pow(5, 11, 13) == 8 and 720 == 55 * 13 + 5)
check('l7 s4', 5 * 11 * 11 == 605 == 46 * 13 + 7 and 20 % 13 == 7 and 5 * 6 * 6 % 13 == 11)
check('l7 s5 quiz', math.comb(7, 2) == 21 and 3 ** 5 == 243 and math.comb(5, 2) == 10 and math.comb(7, 3) == 35 and math.comb(6, 2) == 15 and 3 ** 4 == 81 and math.comb(7, 5) == 21)
d1 = (10 ** 6 * math.log10(2) - 0.5 * math.log10(math.pi * 5 * 10 ** 5))
check('l7 s9 digits of C(1e6, 5e5) by Stirling', math.floor(d1) + 1 == 301027, str(d1))
check('l7 s11', math.comb(10, 6) == 210 and 2 ** 10 == 1024 and 10 * 9 * 8 * 7 == 5040 and len(str(math.comb(252, 126))) == 75)
TABLES = '''
def build_tables(n, p):
    inv = [0, 1] + [0] * (n - 1)                 # inverse of each i by the recurrence, then running products
    for i in range(2, n + 1):
        inv[i] = (p - (p // i) * inv[p % i] % p) % p
    fact, inv_fact = [1] * (n + 1), [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
        inv_fact[i] = inv_fact[i - 1] * inv[i] % p
    return fact, inv_fact
'''
run_tests('l7 s6 build_tables', widget('l7-counting-mod', 'screens', 6), TABLES)
run_tests('l7 s7 n_choose_k', widget('l7-counting-mod', 'screens', 7), '''
import math
def n_choose_k(n, k, fact, inv_fact, p):
    return math.comb(n, k) % p if 0 <= k <= n else 0
''')
w78 = dict(widget('l7-counting-mod', 'screens', 8)); w78['prelude'] = ''
run_tests('l7 s8 count_queries', w78, TABLES + '''
def count_queries(queries, p):
    if not queries: return []
    f, g = build_tables(max(max(n for n, k in queries), 1), p)
    return [f[n] * g[k] * g[n - k] % p if 0 <= k <= n else 0 for n, k in queries]
''')

# ============================================================ l8
def moves(s):
    out = []
    for i in range(3):
        if s[i] >= 2:
            t = [x + 1 for x in s]; t[i] = s[i] - 2
            out.append(tuple(t))
    return out


def reach(start):
    seen, todo = {start}, [start]
    while todo:
        for t in moves(todo.pop()):
            if t not in seen:
                seen.add(t); todo.append(t)
    return seen


r321 = reach((3, 2, 1))
st = L['l8-invariants']['screens'][0]['widget']['states']
name = lambda s: 's%d%d%d' % s
ok = set(st) == {name(s) for s in r321}
for s in r321:
    tos = sorted(o['to'] for o in st[name(s)]['ops'] if 'to' in o)
    ok &= tos == sorted(name(t) for t in moves(s))
check('l8 s0 nine states and every edge', ok and len(r321) == 9 and (6, 0, 0) not in r321)
check('l8 s1 invariant', all((a - b) % 3 == 1 for a, b, c in r321) and [tuple(map(int, row)) for row in L['l8-invariants']['screens'][1]['canvas']['params']['rows']] and
      {tuple(map(int, row)) for row in L['l8-invariants']['screens'][1]['canvas']['params']['rows']} == r321)
dark = L['l8-invariants']['screens'][3]['canvas']['state']['shade']['dark']['ids']
check('l8 s3 shading', len(dark) == 30 and all((int(c[1]) + int(c[3])) % 2 == 0 for c in dark) and 'r1c1' not in dark and 'r8c8' not in dark)


def finals(xs):
    if len(xs) == 1:
        return {xs[0]}
    out = set()
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            rest = [xs[m] for m in range(len(xs)) if m not in (i, j)]
            out |= finals(tuple(sorted(rest + [abs(xs[i] - xs[j])])))
    return out


check('l8 s4 last numbers of 3, 5, 6, 9', finals((3, 5, 6, 9)) == {1, 5, 7})


def pair_reach(x, y, bound):
    seen, todo = {(x, y)}, [(x, y)]
    while todo:
        a, b = todo.pop()
        for t in ((a + b, b), (a, a + b)):
            if max(t) <= bound and t not in seen:
                seen.add(t); todo.append(t)
    return seen


REACH = '''
def can_reach(x, y, c, d):
    if (c, d) == (x, y): return True
    if c < x or d < y or c == d: return False
    if c > d:
        if d == y: return (c - x) % d == 0
        return can_reach(x, y, c % d, d)
    if c == x: return (d - y) % c == 0
    return can_reach(x, y, c, d % c)
'''
ns = {}
exec(REACH, ns)
ok = True
for x in range(1, 6):
    for y in range(1, 6):
        seen = pair_reach(x, y, 14)
        ok &= all(ns['can_reach'](x, y, c, d) == ((c, d) in seen) for c in range(1, 15) for d in range(1, 15))
check('l8 s7 walk back agrees with a forward search (starts up to 5, targets up to 14)', ok)
check('l8 s5 s6', (7, 5) in pair_reach(1, 1, 7) and (2, 7) not in pair_reach(3, 2, 9) and (10, 4) not in pair_reach(1, 1, 10))
run_tests('l8 s7 can_reach', widget('l8-invariants', 'screens', 7), REACH)
run_tests('l8 s8 final_parity', widget('l8-invariants', 'screens', 8), 'def final_parity(xs):\n    return sum(1 for x in xs if x % 2) % 2\n')
check('l8 s10 backtest', 10000 - 30 * 52 == 8440 and 8440 + 10 * 55 == 8990 and 8440 + 30 * 55 == 10090 and 8990 + 10 * 55 == 9540 and 8990 + 20 * 55 == 10090)

# ============================================================ l9
valid = lambda p: all(abs(a - b) != 1 for a, b in zip(p, p[1:]))
check('l9 s0 orders for n = 4', sorted(p for p in itertools.permutations(range(1, 5)) if valid(p)) == [(2, 4, 1, 3), (3, 1, 4, 2)])
check('l9 s1 pattern', all(valid(list(range(2, m + 1, 2)) + list(range(1, m + 1, 2))) == (m not in (2, 3)) for m in range(1, 2001)))
check('l9 s3 no answer', not any(valid(p) for p in itertools.permutations(range(1, 4))) and not any(valid(p) for p in itertools.permutations(range(1, 3))))
ok = True
for m in range(1, 5):
    for k in range(1, 5):
        sums = {sum(c) for c in itertools.product(range(1, k + 1), repeat=m)}
        ok &= sums == set(range(m, m * k + 1))
check('l9 s7 sums of n values in [1, k] are exactly n..nk', ok)
rows9 = [list(map(int, r[1].split())) for r in L['l9-constructive']['screens'][9]['canvas']['params']['rows']]
check('l9 s9 schedules', [len(r) == 6 and sum(r) == 1000 and all(100 <= x <= 250 for x in r) for r in rows9] == [False, True, True, False, False])
run_tests('l9 s5 no_adjacent', widget('l9-constructive', 'screens', 5), '''
def no_adjacent(n):
    if n in (2, 3): return -1
    if n == 4: return [3, 1, 4, 2]
    return list(range(1, n + 1, 2)) + list(range(2, n + 1, 2))     # odds, then evens: another valid order
''')
run_tests('l9 s8 fill_array', widget('l9-constructive', 'screens', 8), '''
def fill_array(n, s, k):
    if not n <= s <= n * k: return -1
    q, r = divmod(s - n, n)
    return [1 + q + (1 if i < r else 0) for i in range(n)]            # an even split: another valid list
''')

# ============================================================ l10
M = {'A': (0, 13), 'B': (1, 5), 'C': (4, 7), 'D': (6, 11), 'E': (9, 15), 'F': (12, 14)}
fits = lambda S: all(M[a][1] <= M[b][0] or M[b][1] <= M[a][0] for a, b in itertools.combinations(S, 2))
best = max(len(S) for m in range(7) for S in itertools.combinations(M, m) if fits(S))
check('l10 s0 best set', best == 3 and [S for S in itertools.combinations(M, 3) if fits(S)] == [('B', 'D', 'F')])


def greedy_keep(items, key, strict=False):
    kept = []
    for s, e in sorted(items, key=key):
        if all((s > b if strict else s >= b) or (e < a if strict else e <= a) for a, b in kept):
            kept.append((s, e))
    return len(kept)


iv = list(M.values())
check('l10 s1 three rules', (greedy_keep(iv, lambda x: x[1] - x[0]), greedy_keep(iv, lambda x: x[0]), greedy_keep(iv, lambda x: x[1])) == (2, 1, 3))
check('l10 s3 touching', greedy_keep([(1, 3), (3, 5), (5, 7)], lambda x: x[1]) == 3 and greedy_keep([(1, 3), (3, 5), (5, 7)], lambda x: x[1], True) == 2)
r = random.Random(7)
ok = True
for _ in range(400):
    its = []
    for _ in range(r.randint(1, 7)):
        s = r.randint(0, 10); its.append((s, s + r.randint(1, 5)))
    ex = max(len(S) for m in range(len(its) + 1) for S in itertools.combinations(range(len(its)), m)
             if all(its[a][1] <= its[b][0] or its[b][1] <= its[a][0] for a, b in itertools.combinations(S, 2)))
    ok &= greedy_keep(its, lambda x: x[1]) == ex
check('l10 s2 earliest finish equals the exhaustive best (400 random sets)', ok)
peak = lambda its, t: sum(1 for s, e in its if s <= t < e)
check('l10 s5 rooms', max(peak(iv, t / 2) for t in range(0, 32)) == 3 and peak(iv, 4.5) == 3)


def coins_greedy(cs, amt):
    used = 0
    for c in sorted(cs, reverse=True):
        used += amt // c; amt %= c
    return used


def coins_best(cs, amt):
    b = [0] + [10 ** 9] * amt
    for a in range(1, amt + 1):
        b[a] = 1 + min(b[a - c] for c in cs if c <= a)
    return b[amt]


first_fail = lambda cs: next((a for a in range(1, 200) if coins_greedy(cs, a) != coins_best(cs, a)), None)
check('l10 s7 quiz review coins', first_fail([1, 3, 4]) == 6 and first_fail([1, 5, 10, 20, 25]) == 40 and first_fail([1, 5, 6]) == 10 and first_fail([1, 2, 5, 10]) is None and
      (coins_greedy([1, 5, 6], 15), coins_best([1, 5, 6], 15)) == (5, 3) and (coins_greedy([1, 4, 6], 8), coins_best([1, 4, 6], 8)) == (3, 2))
auction = [(0, 30), (5, 10), (10, 25), (20, 35), (25, 40), (35, 50), (45, 60), (50, 55)]
check('l10 s10 auction', greedy_keep(auction, lambda x: x[1]) == 4 and greedy_keep(auction, lambda x: x[0]) == 3 and
      max(len(S) for m in range(9) for S in itertools.combinations(auction, m) if all(a[1] <= b[0] or b[1] <= a[0] for a, b in itertools.combinations(S, 2))) == 4)
check('l10 quiz', greedy_keep([(1, 4), (4, 6), (6, 9), (2, 5)], lambda x: x[1]) == 3 and greedy_keep([(1, 4), (4, 6), (6, 9), (2, 5)], lambda x: x[1], True) == 2 and
      max(peak([(0, 4), (1, 3), (2, 6), (3, 5), (5, 7)], t / 2) for t in range(16)) == 3)
run_tests('l10 s4 max_non_overlapping', widget('l10-greedy-proofs', 'screens', 4), '''
import bisect
def max_non_overlapping(intervals):
    a = sorted(intervals, key=lambda x: x[1]); ends = [e for s, e in a]; dp = [0]   # DP, not the greedy
    for i, (s, e) in enumerate(a):
        dp.append(max(dp[i], dp[bisect.bisect_right(ends, s, 0, i)] + 1))
    return dp[-1]
''')
run_tests('l10 s6 min_rooms', widget('l10-greedy-proofs', 'screens', 6), '''
import heapq
def min_rooms(intervals):
    h, best = [], 0
    for s, e in sorted(intervals):
        while h and h[0] <= s: heapq.heappop(h)
        heapq.heappush(h, e); best = max(best, len(h))
    return best
''')
w108 = widget('l10-greedy-proofs', 'screens', 8)
run_tests('l10 s8 greedy_counterexample', w108, '''
import random
def greedy_counterexample(greedy, brute, gen, trials, seed):
    rng = random.Random(seed)
    bad = [c for c in (gen(rng) for _ in range(trials)) if greedy(c) != brute(c)]
    return min(bad, key=lambda c: c[1]) if bad else None            # min keeps the first of equal amounts
''')
ns = {}
exec(w108['prelude'].split('def trials_run')[0], ns)
rng = random.Random(1)
firstbad = next(c for c in (ns['gen_coins'](rng) for _ in range(200)) if ns['greedy_coins'](c) != ns['min_coins_brute'](c))
check('l10 s8 feedback test-1: the first failure for seed 1', firstbad == ([1, 5, 8], 15), str(firstbad))

# ============================================================ l11
tr = [(5, 3), (4, 2), (3, 2), (7, 4)]
bestv = max((sum(tr[i][0] for i in S), S) for m in range(5) for S in itertools.combinations(range(4), m) if sum(tr[i][1] for i in S) <= 6)
check('l11 s0 trades', bestv == (11, (1, 3)))
check('l11 s2 bit operations', (10 >> 1 & 1, 10 | 1 << 2, 10 & -10, bin(10).count('1')) == (1, 14, 2, 2) and (-10) & 15 == 0b0110)
check('l11 s4 precedence', len(range(1 << 4 - 1)) == 8 and (1 << 4) - 1 == 15)
check('l11 s7 s8 s9 s10', 2 ** 10 * 10 == 10240 and math.factorial(9) == 362880 and 2 ** 16 * 16 ** 2 == 16777216 and 2 * 2 ** 20 == 2097152 and abs(2 ** 40 - 1.1e12) < 0.01e12 and
      sum(2 ** bin(m).count('1') for m in range(8)) == 27 and 3 ** 16 == 43046721 and 2 ** 6 - 1 == 63 and 2 ** 30 > 10 ** 9)
m, sub, subs = 0b1011, 0b1011, []
while sub:
    subs.append(sub); sub = (sub - 1) & m
check('l11 s9 submasks of 1011', subs == [0b1011, 0b1010, 0b1001, 0b1000, 0b0011, 0b0010, 0b0001])
check('l11 quiz', [i for i in range(4) if 13 >> i & 1] == [0, 2, 3] and 2 + 4 + 16 == 22 and bin(0b10110).count('1') == 3 and max(range(2 ** 5 - 1)) == 2 ** 5 - 2)
run_tests('l11 s3 best_subset', widget('l11-bitmasks', 'screens', 3), '''
def best_subset(profits, risks, limit):
    cap = min(limit, sum(risks))                      # knapsack over risk, not masks
    if cap < 0: return 0
    dp = [0] * (cap + 1)
    for p, r in zip(profits, risks):
        for c in range(cap, r - 1, -1):
            dp[c] = max(dp[c], dp[c - r] + p)
    return dp[cap]
''')
run_tests('l11 s5 count_subsets_with_sum', widget('l11-bitmasks', 'screens', 5), '''
from collections import Counter
def count_subsets_with_sum(xs, target):
    ways = Counter({0: 1})                            # ways by sum, any sign
    for x in xs:
        nxt = Counter(ways)
        for s, c in ways.items(): nxt[s + x] += c
        ways = nxt
    return ways[target]
''')
run_tests('l11 s6 popcounts', widget('l11-bitmasks', 'screens', 6), 'def popcounts(n):\n    return [bin(m).count("1") for m in range(1 << n)]\n')
r = random.Random(3)
ps, rs = [r.randint(1, 1000) for _ in range(16)], [r.randint(1, 100) for _ in range(16)]
half = lambda idx: [(sum(rs[i] for i in idx if msk >> idx.index(i) & 1), sum(ps[i] for i in idx if msk >> idx.index(i) & 1)) for msk in range(1 << len(idx))]
A, B = half(list(range(8))), sorted(half(list(range(8, 16))))
runbest, bb = [], 0
for rk, pf in B:
    bb = max(bb, pf); runbest.append(bb)
keys = [rk for rk, pf in B]
mitm = max(pf + runbest[bisect.bisect_right(keys, 300 - rk) - 1] for rk, pf in A if rk <= 300)
brute = max(sum(ps[i] for i in range(16) if msk >> i & 1) for msk in range(1 << 16) if sum(rs[i] for i in range(16) if msk >> i & 1) <= 300)
check('l11 s8 meet in the middle as described equals the mask loop (n = 16)', mitm == brute)

# ============================================================ l12
def by_loop(n, ups):
    a = [0] * n
    for l, rr, v in ups:
        for i in range(l, rr + 1):
            a[i] += v
    return a


EX = [(1, 4, 3), (2, 6, 2), (5, 7, 1)]
check('l12 s1', by_loop(8, EX) == [0, 3, 5, 5, 5, 3, 3, 1])
d = [0] * 9
for l, rr, v in EX:
    d[l] += v; d[rr + 1] -= v
check('l12 s1 difference cells', d == [0, 3, 2, 0, 0, -2, 0, -2, -1])


def buggy(n, ups):
    dd = [0] * (n + 1)
    for l, rr, v in ups:
        dd[l] += v
    return list(itertools.accumulate(dd[:n]))


check('l12 s5 sample hides the bug', buggy(8, [(2, 7, 4), (5, 7, 1)]) == by_loop(8, [(2, 7, 4), (5, 7, 1)]) == [0, 0, 4, 4, 4, 5, 5, 5] and buggy(8, [(1, 4, 3)])[5:] == [3, 3, 3])
# Monte Carlo: does a stress test catch the missing -v within ten random cases?
rng, caught, RUNS = random.Random(5), 0, 20000
for _ in range(RUNS):
    for _ in range(10):
        m = rng.randint(1, 8); ups = []
        for _ in range(rng.randint(1, 4)):
            l = rng.randint(0, m - 1); ups.append((l, rng.randint(l, m - 1), rng.choice([-3, -2, -1, 1, 2, 3])))
        if buggy(m, ups) != by_loop(m, ups):
            caught += 1; break
check('l12 s5 Monte Carlo: caught within ten cases in at least 99.9% of 20,000 runs', caught / RUNS >= 0.999, '%.4f' % (caught / RUNS))
W = [(1, 5), (2, 8), (4, 9), (6, 7), (0, 3)]
check('l12 s6 counts by day', [sum(1 for l, rr in W if l <= dday <= rr) for dday in range(10)] == [1, 2, 3, 3, 3, 3, 3, 3, 2, 1])
g = [[0] * 6 for _ in range(6)]
for (rw, cl), v in {(1, 1): 1, (1, 3): -1, (3, 1): -1, (3, 3): 1}.items():
    g[rw][cl] += v
for rw in range(5):
    for cl in range(1, 5): g[rw][cl] += g[rw][cl - 1]
for cl in range(5):
    for rw in range(1, 5): g[rw][cl] += g[rw - 1][cl]
check('l12 s8 four corners', all(g[rw][cl] == (1 if 1 <= rw <= 2 and 1 <= cl <= 2 else 0) for rw in range(5) for cl in range(5)))
check('l12 s9 quiz', 300 - 100 + 200 == 400 and 300 + 100 + 200 == 600 and by_loop(5, [(0, 2, 5), (1, 3, -2)]) == [5, 3, 3, -2, 0])
check('review-3 item 6', by_loop(6, [(0, 5, 2), (2, 2, 5), (3, 5, -1)]) == [2, 2, 7, 1, 1, 1])
w124 = widget('l12-difference-arrays', 'screens', 4)
run_tests('l12 s4 apply_ranges', w124, '''
import itertools
def apply_ranges(n, updates):
    ev = {}
    for l, r, v in updates:
        ev[l] = ev.get(l, 0) + v; ev[r + 1] = ev.get(r + 1, 0) - v
    return list(itertools.accumulate(ev.get(i, 0) for i in range(n)))
''')
rng = random.Random(12); tot = 0
for _ in range(100000):
    l = rng.randint(0, 199999); rr = rng.randint(l, 199999); rng.randint(-1000, 1000); tot += rr - l + 1
check('l12 s4 the range loop on test 8 is about 5e9 additions', 4.5e9 < tot < 5.5e9, str(tot))
run_tests('l12 s7 max_coverage', widget('l12-difference-arrays', 'screens', 7), '''
def max_coverage(n, intervals):
    starts = sorted(l for l, r in intervals); ends = sorted(r for l, r in intervals)
    best = j = 0
    for i, s in enumerate(starts):
        while ends[j] < s: j += 1
        best = max(best, i + 1 - j)
    return best
''')
rng = random.Random(13); tot = 0
for _ in range(100000):
    a, b = rng.randint(0, 199999), rng.randint(0, 199999); tot += abs(a - b) + 1
check('l12 s7 mean interval about 66,500 days, filling about 6.6e9 steps', abs(tot / 100000 - 66500) < 700 and 6.55e9 <= tot < 6.75e9, '%d %.0f' % (tot, tot / 100000))
def zero_read_refused(w, counter_call, phrase):
    """True while a correct pass that reads through reversed() or .copy() is refused by the counting test."""
    t = [t for t in w['tests'] if counter_call in t['call']][0]
    return t['call'].replace(' ', '').startswith('0<') and phrase in w['how'] and '__reversed__' not in w.get('prelude', '')


check('FINDING 5: l12 s4 and homework-3 items[1]: `how` says "at most N pass", but the test needs at least one counted read and the counting list misses reversed() and .copy()',
      not (zero_read_refused(w124, 'update_reads', 'at most 2,500 pass') or zero_read_refused(widget('homework-3', 'items', 1), 'reads_for', 'at most 10,000 pass')))

# ============================================================ reviews
check('review-1', 10 ** 9 * 10 ** 9 == 10 ** 18 < 9.2e18 and abs(2000 ** 2 * math.log2(2000) - 4.4e7) < 0.05e7 and 2000 ** 3 == 8 * 10 ** 9 and 10 ** 4 * 10 ** 6 == 10 ** 10 and
      count_pairs_le([5, 5, 1], 10, True) == 2 and count_pairs_le([5, 5, 1], 10) == 3 and abs(10 ** 5 * math.log2(10 ** 6) - 2e6) < 2e5)
try:
    int('\n'); blank = False
except ValueError:
    blank = True
check('review-1 item 6 int of a blank line', blank and sum(map(int, '1\n2\n\n'.split())) == 3)
check('review-2', math.gcd(252, 198) == 18 and pow(3, -1, P) == 333333336 and pow(3, 10 ** 18, 7) == 4 and 10 ** 18 % 6 == 4 and pow(3, 10 ** 18 % 7, 7) == 3 and
      sum(flags[:51]) == 15 and math.lcm(4, 6, 10) == 60 and math.comb(13, 3) == 286 and 4 ** 10 == 1048576 and math.comb(10, 3) == 120 and math.comb(13, 4) == 715)
check('review-2 tokens 4, 1, 1', len(reach((4, 1, 1))) == 7 and (6, 0, 0) not in reach((4, 1, 1)) and pow(0, 5, 7) == 0)
back, c = [(12, 7)], (12, 7)
while c != (1, 1):
    c = (c[0] - c[1], c[1]) if c[0] > c[1] else (c[0], c[1] - c[0]); back.append(c)
check('review-2 moves to (12, 7)', len(back) - 1 == 5 and back == [(12, 7), (5, 7), (5, 2), (3, 2), (1, 2), (1, 1)])
R3 = [(0, 7), (1, 3), (3, 5), (5, 8), (8, 10), (4, 9)]
check('review-3 meetings', greedy_keep(R3, lambda x: x[1]) == 4 and greedy_keep(R3, lambda x: x[0]) == 2)
run_tests('review-3 ring_string', widget('review-3', 'items', 1), '''
def ring_string(n):
    if n == 1: return -1
    return "ab" * (n // 2) if n % 2 == 0 else "abc" + "ab" * ((n - 3) // 2)
''')

# ============================================================ homework
run_tests('homework-1 count_pairs', widget('homework-1', 'items', 0), '''
from collections import Counter
def count_pairs(xs, k):
    c = Counter(xs); total = 0
    for x, m in c.items():
        y = k - x
        if x < y: total += m * c.get(y, 0)
        elif x == y: total += m * (m - 1) // 2
    return total
''')
run_tests('homework-1 longest_window', widget('homework-1', 'items', 1), '''
def longest_window(tickers, k):
    last, left, best = {}, 0, 0                     # last position of each ticker in the window
    for right, t in enumerate(tickers):
        last[t] = right
        if len(last) > k:
            u = min(last, key=last.get); left = last.pop(u) + 1
        best = max(best, right - left + 1)
    return best
''')
run_tests('homework-1 range_sums', widget('homework-1', 'items', 2), '''
import itertools
def range_sums(xs, queries):
    pre = [0] + list(itertools.accumulate(xs))
    return [pre[r] - pre[l - 1] for l, r in queries]
''')
check('homework-1 figures', math.comb(200000, 2) == 19999900000 and math.comb(6, 2) == 15 and (2 * 10 ** 5) ** 2 == 4 * 10 ** 10 and abs(3 * 2 * 10 ** 5 * 18 - 1.1e7) < 0.03e7)
run_tests('homework-2 gcd_sum', widget('homework-2', 'items', 0), '''
def gcd_sum(n):
    fs, m, d = {}, n, 2                             # sum over divisors d of d * phi(n / d)
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1; m //= d
        d += 1
    if m > 1: fs[m] = fs.get(m, 0) + 1
    divs = [(1, 1)]                                 # (divisor, phi of the divisor)
    for p, a in fs.items():
        divs = [(dv * p ** e, ph * (1 if e == 0 else p ** (e - 1) * (p - 1))) for dv, ph in divs for e in range(a + 1)]
    phi = dict(divs)
    return sum((n // dv) * phi[dv] for dv, _ in divs)
''')
run_tests('homework-2 smallest_k', widget('homework-2', 'items', 1), '''
def smallest_k(m):
    def z(k):
        t = 0
        while k: k //= 5; t += k
        return t
    k = 0
    for step in [5 ** e for e in range(20, -1, -1)]:  # walk up in powers of 5
        while z(k + step) < m: k += step
    return k + 1 if m > 0 else 0
''')
check('homework-2 figures', pow(3, 200, 13) == 9 and 200 % 12 == 8 and math.comb(8, 2) == 28 and math.comb(14, 2) == 91 and math.comb(11, 2) == 55 and (5 - 3) % 3 == 2 and
      sorted(3 * i % 7 for i in range(1, 7)) == [1, 2, 3, 4, 5, 6] and [3 * i % 7 for i in range(1, 7)] == [3, 6, 2, 5, 1, 4])
run_tests('homework-3 fewest_alerts', widget('homework-3', 'items', 0), '''
def fewest_alerts(windows):
    count, first = 0, float("inf")                  # mirror image: latest start first, alert at the start
    for s, e in sorted(windows, key=lambda w: -w[0]):
        if e < first:
            count += 1; first = s
    return count
''')
run_tests('homework-3 spans', widget('homework-3', 'items', 1), '''
def spans(closes):
    out, stack = [], []                             # (close, span) pairs
    for c in closes:
        sp = 1
        while stack and stack[-1][0] <= c: sp += stack.pop()[1]
        stack.append((c, sp)); out.append(sp)
    return out
''')
run_tests('homework-3 first_over_cap', widget('homework-3', 'items', 2), '''
import itertools
def first_over_cap(n, updates, cap):
    def peak(k):
        d = [0] * (n + 1)
        for l, r, v in updates[:k]:
            d[l] += v; d[r + 1] -= v
        return max(itertools.accumulate(d[:n]))
    if not updates or peak(len(updates)) <= cap: return -1
    lo, hi = 0, len(updates)                        # peak(lo) <= cap < peak(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if peak(mid) > cap: hi = mid
        else: lo = mid
    return hi
''')
check('homework-3 figures', 2 ** 12 * 12 == 49152 and math.factorial(12) == 479001600 and 12 * 2 ** 11 == 24576)


def worst_late(order, jobs, ready=None):
    t, worst, total = 0, 0, 0
    for j in order:
        p, dd = jobs[j]
        t = max(t, ready[j] if ready else 0) + p
        worst = max(worst, t - dd, 0); total += max(0, t - dd)
    return worst, total


r = random.Random(11)
ok = True
for _ in range(300):
    jobs = [(r.randint(1, 6), r.randint(0, 15)) for _ in range(r.randint(1, 6))]
    edd = sorted(range(len(jobs)), key=lambda j: jobs[j][1])
    ok &= worst_late(edd, jobs)[0] == min(worst_late(o, jobs)[0] for o in itertools.permutations(range(len(jobs))))
check('homework-3 due-date order minimises the worst lateness (300 random instances, exhaustive)', ok)
check('homework-3 model counterexamples',
      worst_late([1, 0], [(5, 7), (1, 6)], [0, 5])[0] == 4 and worst_late([0, 1], [(5, 7), (1, 6)], [0, 5])[0] == 0 and
      worst_late([0, 1], [(4, 10), (1, 2)], [0, 1])[0] == 3 and worst_late([1, 0], [(4, 10), (1, 2)], [0, 1])[0] == 0 and
      worst_late([0, 1], [(5, 1), (1, 2)]) == (4, 8) and worst_late([1, 0], [(5, 1), (1, 2)]) == (5, 5))

print('%d checks, %d failed' % (COUNT[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
