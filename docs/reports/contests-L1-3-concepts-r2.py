#!/usr/bin/env python3
"""Concept audit, round 2: contests levels 1 to 3 (lessons l1 to l12, review-1..3, homework-1..3).

Part A recomputes the claims the ledger marks "script": definitions, counts, bounds, greedy and invariant results (by brute
force), Python behaviour, and three empirical claims by simulation.
Part B is the sweep of every `feedback.byKey.test-N` line: natural codings of the mistake each line names are graded and the
first failing test is compared with N.
  python3 docs/reports/contests-L1-3-concepts-r2.py                 Part A, and Part B in CPython (no time limits, so the
                                                                     codings marked timing are skipped)
  python3 docs/reports/contests-L1-3-concepts-r2.py --pkgs <pkgs>   Part B under the page's Pyodide 0.27.7 through
                                                                     app/tools/code-runner.mjs (the page's keys and limits)
  --cxx also compiles the C++ codings of l3 screens[10] with the native clang++ (x86-64: int 4 bytes, long 8; `-m32` has no
  headers in this container, so wasm32's 4-byte long is modelled with int32_t).
Exit 0 when every check passes. A check that fails because the content is wrong stays failing: it is a finding in
docs/reviews/audit-contests-1-3-r2.md (the failing checks are listed there).

Fix pass (re-pointed, see "## Fix pass" in the audit file): the checks that encoded the old defects of findings 1 and 3
now test the fixed text. Finding 1: the list(map(...)) coding is probed against the test-6 line, which names lists, and
is no longer an OTHER "finding" against test 7; a check reads the new test-7 line. Finding 3: "first random case almost
every time" (> 90%) is replaced by "within ten random cases almost every time" (> 99% for each generator). Findings 4
and 5 gained text checks."""
import itertools, json, math, os, random, subprocess, sys, tempfile, signal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / 'app' / 'content').exists():
    ROOT = Path(os.environ.get('ZQ_ROOT', '.')).resolve()
C = ROOT / 'app' / 'content' / 'courses' / 'contests'
FAILS = []
N = [0]


def check(name, ok, detail=''):
    N[0] += 1
    if not ok:
        FAILS.append(name)
        print('FAIL', name, detail)


def load(f):
    return json.loads((C / f).read_text())


def widget(f, loc):
    k, i = loc.split('.')
    return load(f)[k][int(i)]['widget']


def text_of(f):
    return (C / f).read_text()

# ---------------------------------------------------------------- Part A
def part_a():
    # ---- l1
    check('l1 sum bound', 2 * 10**5 * 10**9 == 2 * 10**14 > 2**31 - 1)
    check('l1 q-sum-bound', 3 * 10**5 - 9999 == 290001)
    check('l1 fills bound', 10**5 * 10**6 == 10**11 > 2**31 - 1)

    # ---- l2
    check('l2 cubic count', abs((2e5)**3 / 6 - 1.33e15) < 1e13 and (2e5)**2 / 2 == 2e10)
    check('l2 nl crossing', 4523071 * math.log2(4523071) <= 1e8 < 4523072 * math.log2(4523072))
    check('l2 n log n at 2e5', abs(2e5 * math.log2(2e5) - 3.5e6) < 5e4)
    check('l2 boundaries', 2**26 <= 1e8 < 2**27 and 464**3 <= 1e8 < 465**3 and 10**8 == (10**4)**2)
    check('l2 pairs', 5000 * 4999 // 2 == 12497500 and 5000 * 4999 == 24995000)
    check('l2 halvings', math.ceil(math.log2(10**9 + 1)) == 30 and 2**29 < 10**9 + 1 <= 2**30 and round(math.sqrt(1e9)) == 31623)
    w = widget('l2-limits-to-complexity.json', 'screens.9')
    ns = {}
    exec(w['solution'], ns)
    check('l2 budget_class table rows', [ns['budget_class'](n) for n in (20, 500, 5000, 200000, 10**18)] == ['2^n', 'n^2', 'n^2', 'n log n', 'log n'])

    # ---- l3: Python behaviour
    check('l3 split', '2\n\n5 -3'.split() == ['2', '5', '-3'] and b'1\r\n\r\n3\r\n'.split() == [b'1', b'3'])
    check('l3 bytes', int(b'12') == 12 and (b'3' == '3') is False and b'#..#'[0] == ord('#'))
    try:
        int('\n'); ok = False
    except ValueError:
        ok = True
    check('r1 int of blank line', ok)
    check('l3 trap program', (lambda a: (sum(a), max(a)))([4, 1]) == (5, 4))

    # ---- l4: the stress example and the two generators
    w = widget('l4-stress-testing.json', 'screens.7')
    ns = {}
    exec(w['prelude'], ns)
    rng = random.Random(1)
    rows = [ns['gen_pairs'](rng) for _ in range(5)]
    shown = [([10, 2], 10), ([8], 16), ([7, 4, 2, 8], 2), ([7, 10, 1, 8], 10), ([4, 10, 2, 6, 1, 1], 2)]
    check('l4 seed 1 trial table', rows == shown, rows)
    check('l4 seed 1 counts', [(ns['fast_strict'](c), ns['brute_pairs'](c)) for c in shown] == [(0, 0), (0, 0), (0, 0), (2, 2), (0, 1)])

    def gen_a(r):
        return [r.randint(1, 10**9) for _ in range(r.randint(1, 6))], r.randint(2, 2 * 10**9)

    hits = 0
    for seed in (1, 2, 3, 4):       # "nothing in 100,000 trials on each of four seeds"
        r = random.Random(seed)
        for _ in range(100000):
            xs, k = gen_a(r)
            if any(xs[i] + xs[j] == k for i in range(len(xs)) for j in range(i + 1, len(xs))):
                hits += 1
    check('l4 gen A finds no tie in 4 x 100,000 trials', hits == 0, hits)
    first = []
    for seed in range(1, 201):      # gen B finds the bug within a handful of trials
        r = random.Random(seed)
        t = 1
        while True:
            c = ns['gen_pairs'](r)
            if ns['fast_strict'](c) != ns['brute_pairs'](c):
                break
            t += 1
        first.append(t)
    check('l4 gen B finds the bug fast (median trial <= 10 over 200 seeds)', sorted(first)[100] <= 10, sorted(first)[100])
    check('l4 q-strict', ns['fast_strict'](([2, 3, 3], 6)) == 2 and ns['brute_pairs'](([2, 3, 3], 6)) == 3)
    check('l4 shrink options', ns['fast_strict'](([1, 1], 2)) == 0 and ns['brute_pairs'](([1, 1], 2)) == 1
          and ns['fast_strict'](([6, 1, 1], 3)) == ns['brute_pairs'](([6, 1, 1], 3)))
    check('l4 backtest example', abs((100.5 - 99.25) - 1.25) < 1e-12)

    # ---- l5
    check('l5 digits of 2^(10^18)', abs(1e18 * math.log10(2) - 3e17) < 2e15)
    check('l5 last digits of 7^k', [pow(7, k, 10) for k in (2, 3, 4, 5, 2031)] == [9, 3, 1, 7, 3])
    check('l5 38*45 mod 7', 38 % 7 == 3 == 45 % 7 and 38 * 45 == 1710 and 1710 % 7 == 2)
    check('l5 inverses mod 7', [pow(a, -1, 7) for a in range(1, 7)] == [1, 4, 5, 2, 3, 6])
    check('l5 3^5, 3^13 mod 7', pow(3, 5, 7) == 5 and pow(3, 8, 7) == 2 and pow(3, 13, 7) == 3)
    check('l5 fermat for primes < 200', all(pow(a, p - 1, p) == 1 for p in range(2, 200) if all(p % d for d in range(2, p)) for a in range(1, p)))
    check('l5 inverse_mod facts', pow(0, 5, 7) == 0 and pow(2, 10**9 + 5, 10**9 + 7) == 500000004 and pow(-1, 5, 7) == 6)
    try:
        pow(14, -1, 7); ok = False
    except ValueError:
        ok = True
    check('l5 pow(a, -1, p) raises ValueError', ok)
    check('l5 sizes', (10**9 + 6)**2 < 2**63 - 1 < (10**9 + 6)**3 and -3 % 7 == 4 and 10**9 + 7 < 2**30)
    check('l5 mul_mod tests', 10**18 * 3 % (10**9 + 7) == 147 and (10**18)**2 % (10**9 + 7) == 2401)
    h = 0
    for x in (5, 10**9, 3):
        h = (31 * h + x) % (10**9 + 7)
    check('l5 checksum', h == 4591 and 31 * (31 * 5 + 10**9) + 3 == 31000004808 and 31 * 148 == 4588)
    check('l5 quiz', pow(4, -1, 11) == 3 == pow(4, 9, 11) and 2**59 < 10**18 < 2**60 and (2 * 10**9 + 14) % (10**9 + 7) == 0)
    check('r2 numbers', math.gcd(252, 198) == 18 and 3 * 333333336 == 10**9 + 8 and pow(3, 10**18, 7) == 4 and 10**18 % 6 == 4
          and pow(3, 10**18 % 7, 7) == 3)
    check('hw2 cycle', pow(3, 200, 13) == 9 and pow(3, 3, 13) == 1 and 200 % 12 == 8)

    # ---- l6
    def steps(a, b):
        n = 0
        while b:
            a, b = b, a % b
            n += 1
        return n

    fib = [0, 1]
    while len(fib) < 90:
        fib.append(fib[-1] + fib[-2])
    check('l6 gears', math.lcm(84, 36) == 252 and 84 * 36 == 3024 == 12 * 252 and math.gcd(1071, 462) == 21)
    check('l6 steps(89, 55)', steps(89, 55) == 9)
    check('l6 F88', fib[88] == 1100087778366101931 and fib[87] == 679891637638612258 and steps(fib[88], fib[87]) == 86)
    # Lame: among pairs below F(k+1), the Fibonacci neighbours take the most steps
    worst = max(steps(a, b) for a in range(1, 90) for b in range(1, a + 1))
    check('l6 Fibonacci neighbours are the worst case below 90', worst == steps(89, 55), worst)

    def sieve(n):
        f = bytearray([1]) * (n + 1)
        f[0:2] = b'\0\0'
        for p in range(2, int(n**0.5) + 1):
            if f[p]:
                f[p * p::p] = bytearray(len(f[p * p::p]))
        return [i for i in range(n + 1) if f[i]]

    pr = sieve(2 * 10**6)
    check('l6 prime counts', sum(1 for p in pr if p <= 100) == 25 and sum(1 for p in pr if p <= 10**6) == 78498 and len(pr) == 148933
          and sum(1 for p in pr if p <= 30) == 10 and sum(1 for p in pr if p <= 50) == 15)
    check('l6 prime sum below 1.5M', sum(p for p in pr if p < 1500000) == 82074443256)
    check('l6 sieve of 100 at 7', [m for m in range(14, 101, 7) if m % 2 and m % 3 and m % 5] == [49, 77, 91])

    def is_prime(n):
        return n >= 2 and all(n % p for p in pr if p * p <= n)

    check('l6 primes named', is_prime(1000003) and is_prime(999983) and is_prime(999999999989) and not any(is_prime(x) for x in range(999984, 10**6)))
    check('l6 trap', math.isqrt(1000003) == 1000 and len(range(2, 1000003)) == 1000001)
    check('l6 quiz', math.lcm(6, 10) == 30 and math.lcm(14, 21) == 42 and 13**2 <= 200 < 17**2 and math.lcm(4, 6, 10) == 60)

    # ---- l7
    def digits_binom(n, k):
        return math.floor((math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / math.log(10)) + 1

    check('l7 digits', len(str(math.comb(2000, 1000))) == 601 and digits_binom(10**6, 5 * 10**5) == 301027 and len(str(math.comb(252, 126))) == 75)
    f13 = [math.factorial(i) % 13 for i in range(7)]
    check('l7 tables mod 13', f13 == [1, 1, 2, 6, 11, 3, 5] and [pow(x, -1, 13) for x in f13] == [1, 1, 7, 11, 6, 9, 8] and pow(5, 11, 13) == 8)
    check('l7 one query', 5 * 11 * 11 == 605 and 605 % 13 == 7 == math.comb(6, 3) % 13 and 5 * 6 * 6 % 13 == 11)
    check('l7 stars and bars', math.comb(7, 2) == 21 and 3**5 == 243 and math.comb(5, 2) == 10 and math.comb(7, 3) == 35
          and sum(1 for a in range(6) for b in range(6 - a)) == 21)
    check('l7 other counts', math.comb(10, 6) == 210 and 10 * 9 * 8 * 7 == 5040 and math.comb(6, 2) == 15 and math.comb(13, 3) == 286
          and math.comb(13, 4) == 715 and math.comb(8, 2) == 28 and math.comb(14, 2) == 91 and math.comb(11, 2) == 55)
    check('l7 n >= p', math.factorial(7) % 7 == 0 and pow(0, 5, 7) == 0)
    check('l7 negative index wraps', [10, 20, 30][-1] == 30)
    P = 10**9 + 7
    check('l7 keys', math.comb(2000, 1000) % P == 72475738 and math.comb(1000, 500) % P == 159835829)

    # ---- l8
    def reach(start):
        seen, todo = {start}, [start]
        while todo:
            s = todo.pop()
            for i in range(3):
                if s[i] >= 2:
                    t = tuple(s[j] - 2 if j == i else s[j] + 1 for j in range(3))
                    if t not in seen:
                        seen.add(t); todo.append(t)
        return seen

    r321 = reach((3, 2, 1))
    table = {(3, 2, 1), (1, 3, 2), (4, 0, 2), (2, 1, 3), (2, 4, 0), (5, 1, 0), (0, 2, 4), (0, 5, 1), (1, 0, 5)}
    check('l8 nine positions from 3, 2, 1', r321 == table and all((a - b) % 3 == 1 for a, b, c in r321) and all(max(s) < 6 for s in r321))
    r411 = reach((4, 1, 1))
    check('r2 seven positions from 4, 1, 1', len(r411) == 7 and all(max(s) < 6 for s in r411), len(r411))
    check('hw2 tokens 5, 3, 1', all(max(s) < 9 for s in reach((5, 3, 1))) and (5 - 3) % 3 == 2)

    def finals(xs):
        if len(xs) == 1:
            return {xs[0]}
        out = set()
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                rest = tuple(sorted(xs[:i] + xs[i + 1:j] + xs[j + 1:] + (abs(xs[i] - xs[j]),)))
                out |= finals(rest)
        return out

    check('l8 difference game on 3, 5, 6, 9', finals((3, 5, 6, 9)) == {1, 5, 7}, finals((3, 5, 6, 9)))
    check('l8 q-one-to-ten', sum(range(1, 11)) == 55)
    ns = {}
    exec(widget('l8-invariants.json', 'screens.7')['solution'], ns)

    def brute_reach(x, y, c, d, cap=40):
        seen, todo = {(x, y)}, [(x, y)]
        while todo:
            a, b = todo.pop()
            for t in ((a + b, b), (a, a + b)):
                if max(t) <= cap and t not in seen:
                    seen.add(t); todo.append(t)
        return (c, d) in seen

    bad = [(x, y, c, d) for x in range(1, 7) for y in range(1, 7) for c in range(1, 31) for d in range(1, 31)
           if ns['can_reach'](x, y, c, d) != brute_reach(x, y, c, d)]
    check('l8 can_reach solution against a BFS', not bad, bad[:3])
    check('l8 pair-game claims', not brute_reach(3, 2, 2, 7) and brute_reach(1, 1, 7, 5) and not brute_reach(1, 1, 10, 4) and brute_reach(1, 1, 12, 7))
    dark = sum(1 for r in range(8) for c in range(8) if (r + c) % 2 == 0) - 2
    check('l8 chessboard', dark == 30)
    check('l8 backtest log', 10000 - 30 * 52 == 8440 and 8440 + 10 * 55 == 8990 and 8440 + 30 * 55 == 10090 and 8990 + 10 * 55 == 9540)

    # ---- l9
    def valid(p):
        return all(abs(p[i] - p[i + 1]) != 1 for i in range(len(p) - 1))

    v4 = [p for p in itertools.permutations(range(1, 5)) if valid(p)]
    check('l9 n = 4 has exactly two orders', v4 == [(2, 4, 1, 3), (3, 1, 4, 2)])
    check('l9 n = 2, 3 have none', not any(valid(p) for n in (2, 3) for p in itertools.permutations(range(1, n + 1))))
    check('l9 evens then odds valid for 4..300', all(valid(list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))) for n in range(4, 301)))
    gaps = [abs(a - b) for a, b in zip([2, 4, 1, 3, 5], [4, 1, 3, 5])]
    opt = [o for o in load('l9-constructive.json')['screens'][1]['widget']['options'] if o['id'] == 'odd'][0]
    check('l9 screens[1] option odd: gaps of 2 4 1 3 5 are 2, 3, 2 and 2', gaps == [2, 3, 2, 2] and 'gaps 2, 3, 2 and 2' in opt['why'], opt['why'])
    ok = True
    for n in range(1, 5):
        for k in range(1, 5):
            for s in range(0, 20):
                exists = any(sum(t) == s for t in itertools.product(range(1, k + 1), repeat=n))
                ok &= exists == (n <= s <= n * k)
    check('l9 problem F: answer exists iff n <= s <= nk', ok)
    check('l9 slicing', sum([250, 250, 200, 100, 100, 100]) == 1000 == sum([167] * 4 + [166] * 2))

    # ---- l10
    meet = {'A': (0, 13), 'B': (1, 5), 'C': (4, 7), 'D': (6, 11), 'E': (9, 15), 'F': (12, 14)}

    def fits(sel):
        iv = sorted(sel)
        return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))

    best = [c for r in range(7) for c in itertools.combinations(meet, r) if fits([meet[x] for x in c])]
    top = max(len(c) for c in best)
    check('l10 six meetings: best is B, D, F only', top == 3 and [c for c in best if len(c) == 3] == [('B', 'D', 'F')])

    def greedy(iv, key):
        kept = []
        for s, e in sorted(iv, key=key):
            if all(e <= a or s >= b for a, b in kept):
                kept.append((s, e))
        return len(kept)

    iv = list(meet.values())
    check('l10 three rules keep 2, 1, 3', (greedy(iv, lambda x: x[1] - x[0]), greedy(iv, lambda x: x[0]), greedy(iv, lambda x: x[1])) == (2, 1, 3))
    rng = random.Random(10)
    ok = True
    for _ in range(3000):
        n = rng.randint(1, 7)
        ivs = []
        for _ in range(n):
            s = rng.randint(0, 9)
            ivs.append((s, s + rng.randint(1, 5)))
        opt_ = max(len(c) for r in range(n + 1) for c in itertools.combinations(ivs, r) if fits(list(c)))
        ok &= greedy(ivs, lambda x: x[1]) == opt_
    check('l10 earliest finish is optimal (3,000 random cases against every subset)', ok)

    def rooms(ivs):
        ev = sorted([(s, 1) for s, e in ivs] + [(e, -1) for s, e in ivs])
        b = m_ = 0
        for _, ch in ev:
            b += ch
            m_ = max(m_, b)
        return m_

    check('l10 rooms', rooms(iv) == 3 and rooms([(0, 4), (1, 3), (2, 6), (3, 5), (5, 7)]) == 3 and rooms([(1, 3), (3, 5), (5, 7)]) == 1)

    def g_coins(coins, a):
        u = 0
        for c in sorted(coins, reverse=True):
            u += a // c
            a %= c
        return u

    def b_coins(coins, a):
        best_ = [0] + [10**9] * a
        for x in range(1, a + 1):
            best_[x] = min(best_[x - c] + 1 for c in coins if c <= x)
        return best_[a]

    def first_fail(coins, top_=200):
        return next((a for a in range(1, top_) if g_coins(coins, a) != b_coins(coins, a)), None)

    check('l10 coins', first_fail([1, 3, 4]) == 6 and first_fail([1, 5, 10, 20, 25]) == 40 and first_fail([1, 5, 6]) == 10
          and first_fail([1, 2, 5, 10]) is None and (g_coins([1, 5, 6], 15), b_coins([1, 5, 6], 15)) == (5, 3)
          and (g_coins([1, 4, 6], 8), b_coins([1, 4, 6], 8)) == (3, 2))
    orders = [(0, 30), (5, 10), (10, 25), (20, 35), (25, 40), (35, 50), (45, 60), (50, 55)]
    check('l10 auction', greedy(orders, lambda x: x[1]) == 4 and greedy(orders, lambda x: x[0]) == 3)
    r3 = [(0, 7), (1, 3), (3, 5), (5, 8), (8, 10), (4, 9)]
    check('r3 meetings', greedy(r3, lambda x: x[1]) == 4 and greedy(r3, lambda x: x[0]) == 2)

    # hw3: stabbing greedy and the due-order greedy, both against brute force
    def alerts(ws):
        cnt, last = 0, -10**9
        for s, e in sorted(ws, key=lambda w_: w_[1]):
            if s > last:
                cnt += 1
                last = e
        return cnt

    ok = True
    for _ in range(1500):
        n = rng.randint(1, 6)
        ws = []
        for _ in range(n):
            s = rng.randint(0, 8)
            ws.append((s, s + rng.randint(0, 4)))
        pts = sorted({e for s, e in ws})
        bf = next(r for r in range(1, n + 1) if any(all(any(s <= t <= e for t in c) for s, e in ws) for c in itertools.combinations(pts, r)))
        ok &= alerts(ws) == bf
    check('hw3 fewest alerts greedy is optimal (1,500 random cases)', ok)

    def worst_late(order):
        t = w_ = 0
        for p, d in order:
            t += p
            w_ = max(w_, t - d)
        return max(0, w_)

    ok = True
    for _ in range(2000):
        jobs = [(rng.randint(1, 6), rng.randint(0, 15)) for _ in range(rng.randint(1, 6))]
        ok &= worst_late(sorted(jobs, key=lambda j: j[1])) == min(worst_late(p) for p in itertools.permutations(jobs))
    check('hw3 due order minimises the worst lateness (2,000 random cases against every order)', ok)
    tot = lambda order: sum(max(0, c - d) for c, d in zip(itertools.accumulate(p for p, _ in order), (d for _, d in order)))
    check('hw3 total-lateness instance', tot([(5, 1), (1, 2)]) == 8 and tot([(1, 2), (5, 1)]) == 5 and worst_late([(5, 1), (1, 2)]) == 4 and worst_late([(1, 2), (5, 1)]) == 5)

    # ---- l11
    trades = [(5, 3), (4, 2), (3, 2), (7, 4)]
    bestp = max(sum(trades[i][0] for i in range(4) if m >> i & 1) for m in range(16) if sum(trades[i][1] for i in range(4) if m >> i & 1) <= 6)
    check('l11 four trades', bestp == 11)
    n = 4
    check('l11 precedence', (10 >> 1 & 1, 10 | 1 << 2, 10 & -10, bin(10).count('1')) == (1, 14, 2, 2) and len(range(1 << n - 1)) == 8)
    check('l11 power-of-two test in Python', [x for x in range(1, 70) if x > 0 and x & (x - 1) == 0] == [1, 2, 4, 8, 16, 32, 64])
    check('l11 counts', 2**10 * 10 == 10240 and math.factorial(9) == 362880 and 2**16 * 256 == 16777216 and 2 * 2**20 == 2097152
          and 3**16 == 43046721 and 2**6 - 1 == 63 and 2**12 * 12 == 49152 and 12 * 2**11 == 24576 and math.factorial(12) == 479001600)
    check('l11 submask pairs', sum(2**bin(m).count('1') for m in range(8)) == 27)
    sub, m_, seen = 0b1011, 0b1011, []
    while sub:
        seen.append(sub)
        sub = (sub - 1) & m_
    check('l11 submask walk', seen == [0b1011, 0b1010, 0b1001, 0b1000, 0b0011, 0b0010, 0b0001])
    check('l11 masks', 13 == 0b1101 and 22 == 0b10110 and 26 == 0b11010 and 20 == 0b10100)

    # ---- l12
    def apply(n, ups):
        d = [0] * (n + 1)
        for l, r, v in ups:
            d[l] += v
            d[r + 1] -= v
        return list(itertools.accumulate(d))[:n], d

    vals, d = apply(8, [(1, 4, 3), (2, 6, 2), (5, 7, 1)])
    check('l12 explore', vals == [0, 3, 5, 5, 5, 3, 3, 1] and d[5] == -2 and sum(d[:6]) == 3)
    vals, d = apply(5, [(0, 2, 5), (1, 3, -2)])
    check('l12 quiz', d == [5, -2, 0, -5, 2, 0] and vals == [5, 3, 3, -2, 0])
    vals, d = apply(6, [(0, 5, 2), (2, 2, 5), (3, 5, -1)])
    check('r3 diff', d == [2, 0, 5, -6, 0, 0, -1] and vals == [2, 2, 7, 1, 1, 1])
    cov, _ = apply(10, [(l, r, 1) for l, r in [(1, 5), (2, 8), (4, 9), (6, 7), (0, 3)]])
    check('l12 busiest day', cov == [1, 2, 3, 3, 3, 3, 3, 3, 2, 1])
    g = [[0] * 5 for _ in range(5)]
    for (r_, c_, v) in ((1, 1, 1), (1, 3, -1), (3, 1, -1), (3, 3, 1)):
        g[r_][c_] += v
    for row in g:
        for c_ in range(1, 5):
            row[c_] += row[c_ - 1]
    for r_ in range(1, 5):
        for c_ in range(5):
            g[r_][c_] += g[r_ - 1][c_]
    check('l12 two dimensions', all(g[r_][c_] == (1 if 1 <= r_ <= 2 and 1 <= c_ <= 2 else 0) for r_ in range(5) for c_ in range(5)))
    r = random.Random(12)
    tot_len = 0
    for _ in range(100000):
        l = r.randint(0, 199999)
        tot_len += r.randint(l, 199999) - l + 1
        r.randint(-1000, 1000)
    check('l12 test 8: the range loop needs about 5e9 additions', 4.5e9 < tot_len < 5.5e9, tot_len)
    r = random.Random(13)
    tot_len = 0
    for _ in range(100000):
        a, b = r.randint(0, 199999), r.randint(0, 199999)
        tot_len += abs(a - b) + 1
    line = load('l12-difference-arrays.json')['screens'][7]['feedback']['byKey']['test-7']
    check('l12 test-7 line: mean interval length (stated "about 66,500")', '66,500' in line and abs(tot_len / 1e5 - 66500) < 500, round(tot_len / 1e5))
    check('l12 fill every day about 6.6e9', 6.4e9 < tot_len < 6.9e9, tot_len)

    # l12 screens[5]: "a stress test ... finds it within ten random cases almost every time" (fix pass; was "on the first
    # random case almost every time")
    def buggy(n, ups):
        d = [0] * (n + 1)
        for l, r_, v in ups:
            d[l] += v
        return list(itertools.accumulate(d))[:n]

    def brute(n, ups):
        a = [0] * n
        for l, r_, v in ups:
            for i in range(l, r_ + 1):
                a[i] += v
        return a

    rates = {}
    for name, (nmax, qmax) in {'n 1..6, q 1..4': (6, 4), 'n 1..8, q 1..5': (8, 5), 'n 2..10, q 1..6': (10, 6)}.items():
        r = random.Random(5)
        hit = 0
        for _ in range(20000):
            n = r.randint(2 if nmax == 10 else 1, nmax)
            ups = []
            for _ in range(r.randint(1, qmax)):
                l = r.randint(0, n - 1)
                ups.append((l, r.randint(l, n - 1), r.randint(1, 9)))
            hit += buggy(n, ups) != brute(n, ups)
        rates[name] = hit / 20000
    check('l12 screens[5]: it does show within the first five cases (> 98%)', all(1 - (1 - p_) ** 5 > 0.98 for p_ in rates.values()), rates)
    ex = load('l12-difference-arrays.json')['screens'][5]['explain']['text']
    check('l12 screens[5]: the missing -v shows within ten small random cases "almost every time" (> 99%)',
          'within ten random cases almost every time' in ex and all(1 - (1 - p_) ** 10 > 0.99 for p_ in rates.values()), rates)
    # fix pass's own run, signed values and possibly no update (worst seen: first case 0.44, within ten 0.997)
    mine = {}
    for name, (nhi, mlo, mhi, vlo, vhi) in {'n 1..6, q 0..4, v -5..5': (6, 0, 4, -5, 5), 'n 1..6, q 1..4, v -9..9': (6, 1, 4, -9, 9)}.items():
        r = random.Random(12)
        hit = 0
        for _ in range(20000):
            n = r.randint(1, nhi)
            ups = []
            for _ in range(r.randint(mlo, mhi)):
                l = r.randint(0, n - 1)
                ups.append((l, r.randint(l, n - 1), r.randint(vlo, vhi)))
            hit += buggy(n, ups) != brute(n, ups)
        mine[name] = hit / 20000
    check('l12 screens[5]: fix-pass generators, within ten cases > 99%, first case 40% to 60%',
          all(1 - (1 - p_) ** 10 > 0.99 and 0.4 < p_ < 0.6 for p_ in mine.values()), mine)
    # fix-pass text checks: l3 screens[8] test-7, l4 quiz[1] option time, l6 sqrt bound with d above 1
    t7 = load('l3-fast-io.json')['screens'][8]['feedback']['byKey']['test-7']
    check('l3 screens[8] test-7 line names __iter__ returning self, not a list', '`return self`' in t7 and 'list' not in t7, t7)
    why = [o for o in load('l4-stress-testing.json')['quiz'][1]['widget']['options'] if o['id'] == 'time'][0]['why']
    check('l4 quiz[1] option time: no claim the seeded case was lost', 'lost' not in why and 'Seed 4' in why, why)
    l6 = load('l6-gcd-and-primes.json')
    for where, txt in (('summary.ideas[1]', l6['summary']['ideas'][1]), ('screens[8].hints[2]', l6['screens'][8]['hints'][2]['text'])):
        check('l6 %s: the divisor is bounded below by 2' % where, '2 \\le d \\le \\sqrt n' in txt, txt)
    comp = [n for n in range(4, 5001) if any(n % d == 0 for d in range(2, n))]
    check('l6: every composite n <= 5000 has a divisor d with 2 <= d <= sqrt n',
          all(any(n % d == 0 for d in range(2, math.isqrt(n) + 1)) for n in comp))

    # ---- homework numbers
    def G(n):
        return sum(math.gcd(i, n) for i in range(1, n + 1))

    ns = {}
    exec(widget('homework-2.json', 'items.0')['solution'], ns)
    check('hw2 gcd_sum', all(ns['gcd_sum'](n) == G(n) for n in range(1, 400)) and ns['gcd_sum'](10**12) == 74200000000000
          and all(G(p**a) == (a + 1) * p**a - a * p**(a - 1) for p in (2, 3, 5) for a in (1, 2, 3, 4)))

    def Z(k):
        z, q = 0, 5
        while q <= k:
            z += k // q
            q *= 5
        return z

    check('hw2 trailing zeros', Z(24) == 4 and Z(25) == 6 and all(Z(5 * m) >= m for m in range(2000)) and Z(4000000000010) >= 10**12 > Z(4000000000009)
          and Z(4000000000005) >= 10**12 - 1 > Z(4000000000004) and math.ceil(math.log2(5 * 10**12)) == 43)
    check('hw2 fermat list', [i * 3 % 7 for i in range(1, 7)] == [3, 6, 2, 5, 1, 4])
    check('hw1 numbers', math.comb(200000, 2) == 19999900000 and math.comb(6, 2) == 15 and 2000**2 * math.log2(2000) < 4.5e7)
    check('hw3 derange', all(all(p != i for i, p in enumerate(list(range(2, n + 1)) + [1], 1)) for n in range(2, 50)))
    # cross-references to other courses
    cc = ROOT / 'app' / 'content' / 'courses'
    def names(course):
        return json.loads((cc / course / 'course.json').read_text()).get('lessonNames', {})
    ds = names('ds')
    def lesson(course, n):
        return next((v for k, v in names(course).items() if k.startswith('l%d-' % n)), '')
    check('xref ds', 'Looking up in constant time' in ds.values() and 'First in, first out' in ds.values() and 'Prefix sums' in ds.values(), list(ds.values())[:20])
    check('xref ds lessons 7 (prefix sums), 10 (a stack), 17 (a heap)', (lesson('ds', 7), lesson('ds', 10), lesson('ds', 17))
          == ('Prefix sums', 'The next greater element', 'Always know the smallest'), (lesson('ds', 7), lesson('ds', 10), lesson('ds', 17)))
    ccn = names('counting-chance')
    check('xref counting-chance', 'Does order matter?' in ccn.values() and 'Sharing identical items' in ccn.values(), list(ccn.values()))

# ---------------------------------------------------------------- Part B: the test-N sweep
# m(file, widget, N of the byKey line probed, coding name, source). The coding is a natural way to make the mistake the line
# names (or, for a line that only describes its test, a natural mistake that test catches).
M = []
def m(file, loc, line, name, src): M.append(dict(file=file, loc=loc, line=line, name=name, src=src.strip('\n') + '\n'))

# ---- l1 screens[9] parse
F = 'l1-reading-statements.json'
m(F, 'screens.9', 4, 'lines by index', '''
def parse(text):
    lines = text.split('\\n')
    t = int(lines[0])
    return t, [[int(x) for x in lines[2 + 2 * i].split()] for i in range(t)]
''')
m(F, 'screens.9', 4, 'splitlines iterator', '''
def parse(text):
    it = iter(text.splitlines())
    t = int(next(it))
    cases = []
    for _ in range(t):
        n = int(next(it))
        cases.append([int(x) for x in next(it).split()])
    return t, cases
''')
m(F, 'screens.9', 2, 'drop the last piece of split(newline)', '''
def parse(text):
    lines = text.split('\\n')[:-1]
    t = int(lines[0])
    return t, [[int(x) for x in lines[2 + 2 * i].split()] for i in range(t)]
''')
m(F, 'screens.9', 2, 'strip the newline with line[:-1]', '''
import io
def parse(text):
    f = io.StringIO(text)
    t = int(f.readline()[:-1])
    cases = []
    for _ in range(t):
        n = int(f.readline()[:-1])
        cases.append([int(x) for x in f.readline()[:-1].split()])
    return t, cases
''')
m(F, 'screens.9', 3, 'split(newline), read pairs of lines to the end', '''
def parse(text):
    lines = text.split('\\n')
    if lines[-1] == '':
        lines.pop()
    t = int(lines[0])
    cases = []
    pos = 1
    while pos < len(lines):
        n = int(lines[pos])
        cases.append([int(x) for x in lines[pos + 1].split()])
        pos += 2
    return t, cases
''')
m(F, 'screens.9', 7, 'tokens.pop(0)', '''
def parse(text):
    tokens = text.split()
    t = int(tokens.pop(0))
    cases = []
    for _ in range(t):
        n = int(tokens.pop(0))
        cases.append([int(tokens.pop(0)) for _ in range(n)])
    return t, cases
''')
# ---- l1 screens[10] new_highs
m(F, 'screens.10', 3, '>= for >', '''
def new_highs(xs):
    count, best = 0, None
    for x in xs:
        if best is None or x >= best:
            count += 1
            best = x
    return count
''')
m(F, 'screens.10', 5, 'best = 0', '''
def new_highs(xs):
    count, best = 0, 0
    for x in xs:
        if x > best:
            count += 1
            best = x
    return count
''')
m(F, 'screens.10', 5, 'best = 0, day 1 forced', '''
def new_highs(xs):
    count, best = 1, 0
    for x in xs[1:]:
        if x > best:
            count += 1
            best = x
    return count
''')
m(F, 'screens.10', 6, 'if not best', '''
def new_highs(xs):
    count, best = 0, None
    for x in xs:
        if not best or x > best:
            count += 1
            best = x
    return count
''')
m(F, 'screens.10', 9, 'max(xs[:i]) per day', '''
def new_highs(xs):
    count = 1
    for i in range(1, len(xs)):
        if xs[i] > max(xs[:i]):
            count += 1
    return count
''')
# ---- l2 screens[9] budget_class
F = 'l2-limits-to-complexity.json'
HEAD = 'from math import log2\nCLASSES = ["2^n", "n^3", "n^2", "n log n", "n", "log n"]\n'
m(F, 'screens.9', 6, "the table's thresholds", HEAD + '''
def budget_class(n):
    if n <= 20: return "2^n"
    if n <= 500: return "n^3"
    if n <= 5000: return "n^2"
    if n <= 200000: return "n log n"
    if n <= 10**7: return "n"
    return "log n"
''')
m(F, 'screens.9', 6, "exact 2^n, then the table's 500", HEAD + '''
def budget_class(n):
    if n <= 60 and 2 ** n <= 10 ** 8: return "2^n"
    if n <= 500: return "n^3"
    if n ** 2 <= 10 ** 8: return "n^2"
    if n * log2(n) <= 10 ** 8: return "n log n"
    if n <= 10 ** 8: return "n"
    return "log n"
''')
m(F, 'screens.9', 15, 'no guard before 2 ** n', HEAD + '''
def budget_class(n):
    if 2 ** n <= 10 ** 8: return "2^n"
    if n ** 3 <= 10 ** 8: return "n^3"
    if n ** 2 <= 10 ** 8: return "n^2"
    if n * log2(n) <= 10 ** 8: return "n log n"
    if n <= 10 ** 8: return "n"
    return "log n"
''')
m(F, 'screens.9', 15, 'no guard, steps in a list', HEAD + '''
def budget_class(n):
    steps = [2 ** n, n ** 3, n ** 2, n * log2(n), n, log2(n)]
    for name, s in zip(CLASSES, steps):
        if s <= 10 ** 8:
            return name
''')
# ---- l2 screens[10] pair_sums_at_most
SORT2P = '''
def pair_sums_at_most(xs, k):
    a = sorted(xs)
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] %s k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count
'''
m(F, 'screens.10', 1, '< for <=', SORT2P % '<')
m(F, 'screens.10', 3, 'set removes duplicates', '''
def pair_sums_at_most(xs, k):
    a = sorted(set(xs))
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] <= k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count
''')
m(F, 'screens.10', 5, 'drop values above k', '''
def pair_sums_at_most(xs, k):
    a = sorted(x for x in xs if x <= k)
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] <= k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count
''')
m(F, 'screens.10', 8, 'every pair, indexing xs', '''
def pair_sums_at_most(xs, k):
    n = len(xs)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if xs[i] + xs[j] <= k:
                count += 1
    return count
''')
m(F, 'screens.10', 9, 'every pair, on a sorted copy', '''
def pair_sums_at_most(xs, k):
    a = sorted(xs)
    n = len(a)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] <= k:
                count += 1
            else:
                break
    return count
''')
# ---- l3 screens[8] read_tokens
F = 'l3-fast-io.json'
m(F, 'screens.8', 6, 'a list comprehension', '''
def read_tokens(data):
    return [int(x) for x in data.split()]
''')
m(F, 'screens.8', 6, 'list(map(...)) (a list: the test-6 line names it)', '''
def read_tokens(data):
    return list(map(int, data.split()))
''')
m(F, 'screens.8', 3, "split(b'\\n') then int per line", '''
def read_tokens(data):
    return map(int, data.split(b'\\n'))
''')
m(F, 'screens.8', 3, "split(b'\\n'), then split(b' ') per line", '''
def read_tokens(data):
    out = []
    for line in data.split(b'\\n'):
        for tok in line.split(b' '):
            if tok:
                out.append(int(tok))
    return iter(out)
''')
m(F, 'screens.8', 3, "replace newlines, split(b' '), skip empties", '''
def read_tokens(data):
    return (int(x) for x in data.replace(b'\\n', b' ').split(b' ') if x)
''')
m(F, 'screens.8', 3, "split(b'\\n'), then split() per line", '''
def read_tokens(data):
    return (int(tok) for line in data.split(b'\\n') for tok in line.split())
''')
m(F, 'screens.8', 7, 'a class with __next__ whose __iter__ builds a fresh iterator (what does reach test 7)', '''
class _Tokens:
    def __init__(self, data):
        self.toks = data.split()
        self.pos = 0
    def __iter__(self):
        return iter([int(t) for t in self.toks])
    def __next__(self):
        self.pos += 1
        return int(self.toks[self.pos - 1])
def read_tokens(data):
    return _Tokens(data)
''')
# ---- l3 screens[9] problem S, Python program
m(F, 'screens.9', 5, 'input() per line', '''
t = int(input())
out = []
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    out.append(f"{sum(a)} {max(a)}")
print("\\n".join(out))
''')
m(F, 'screens.9', 4, 'sys.stdin.readline per line (line reading, line 4 names it)', '''
import sys
t = int(sys.stdin.readline())
out = []
for _ in range(t):
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    out.append(f"{sum(a)} {max(a)}")
print("\\n".join(out))
''')
m(F, 'screens.9', 4, 'read().split(newline) by index', '''
import sys
lines = sys.stdin.read().split("\\n")
t = int(lines[0])
out = []
for i in range(t):
    a = list(map(int, lines[2 + 2 * i].split()))
    out.append(f"{sum(a)} {max(a)}")
print("\\n".join(out))
''')
m(F, 'screens.9', 4, 'readline()[:-1] strips the newline', '''
import sys
t = int(sys.stdin.readline()[:-1])
out = []
for _ in range(t):
    n = int(sys.stdin.readline()[:-1])
    a = list(map(int, sys.stdin.readline()[:-1].split()))
    out.append(f"{sum(a)} {max(a)}")
print("\\n".join(out))
''')
m(F, 'screens.9', 7, 'recursion, one call per test case', '''
import sys
data = sys.stdin.read().split()
out = []
def solve(pos, left):
    if left == 0:
        return
    n = int(data[pos])
    a = list(map(int, data[pos + 1:pos + 1 + n]))
    out.append(f"{sum(a)} {max(a)}")
    solve(pos + 1 + n, left - 1)
solve(1, int(data[0]))
print("\\n".join(out))
''')
# ---- l4 screens[7] stress
F = 'l4-stress-testing.json'
ST = 'import copy\nimport random\n'
m(F, 'screens.7', 9, 'no copy', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(case) != brute(case):
            return case
    return None
''')
m(F, 'screens.7', 9, 'copy.copy (shallow)', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(copy.copy(case)) != brute(copy.copy(case)):
            return case
    return None
''')
m(F, 'screens.7', 7, 'list(case)', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(list(case)) != brute(list(case)):
            return case
    return None
''')
m(F, 'screens.7', 7, 'case[:]', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(case[:]) != brute(case[:]):
            return case
    return None
''')
m(F, 'screens.7', 4, 'trials + 1', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials + 1):
        case = gen(rng)
        if fast(copy.deepcopy(case)) != brute(copy.deepcopy(case)):
            return case
    return None
''')
m(F, 'screens.7', 4, 'while True, ignores trials', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    while True:
        case = gen(rng)
        if fast(copy.deepcopy(case)) != brute(copy.deepcopy(case)):
            return case
''')
m(F, 'screens.7', 2, 'a new Random(seed) every trial', ST + '''
def stress(fast, brute, gen, trials, seed):
    for _ in range(trials):
        rng = random.Random(seed)
        case = gen(rng)
        if fast(copy.deepcopy(case)) != brute(copy.deepcopy(case)):
            return case
    return None
''')
m(F, 'screens.7', 2, 'gen called twice per trial', ST + '''
def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        if fast(gen(rng)) != brute(gen(rng)):
            return gen(rng)
    return None
''')
# ---- l4 screens[8] pytest
PT = '''import copy
import random


def pair_sums_at_most(xs, k):
    a = sorted(xs)
    i, j, count = 0, len(a) - 1, 0
    while i < j:
        if a[i] + a[j] <= k:
            count += j - i
            i += 1
        else:
            j -= 1
    return count


def stress(fast, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if fast(copy.deepcopy(case)) != brute(copy.deepcopy(case)):
            return case
    return None

'''
GOODB = '''
def brute_pair_sums(xs, k):
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] + xs[j] <= k)
'''
GOODG = '''
def gen(rng):
    n = rng.randint(1, 6)
    return [rng.randint(-5, 5) for _ in range(n)], rng.randint(-10, 10)
'''
GOODT = '''
def test_against_brute():
    assert stress(lambda c: pair_sums_at_most(*c), lambda c: brute_pair_sums(*c), gen, 500, 1) is None
'''
m(F, 'screens.8', 6, 'brute calls pair_sums_at_most', PT + '''
def brute_pair_sums(xs, k):
    return pair_sums_at_most(xs, k)
''' + GOODG + GOODT)
m(F, 'screens.8', 6, 'no assert', PT + GOODB + GOODG + '''
def test_against_brute():
    stress(lambda c: pair_sums_at_most(*c), lambda c: brute_pair_sums(*c), gen, 500, 1)
''')
m(F, 'screens.8', 10, 'k never negative', PT + GOODB + '''
def gen(rng):
    n = rng.randint(1, 6)
    return [rng.randint(-5, 5) for _ in range(n)], rng.randint(0, 10)
''' + GOODT)
m(F, 'screens.8', 5, 'test passes the functions unwrapped', PT + GOODB + GOODG + '''
def test_against_brute():
    assert stress(pair_sums_at_most, brute_pair_sums, gen, 500, 1) is None
''')
# ---- l9 screens[5] no_adjacent
F = 'l9-constructive.json'
EO = 'list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))'
m(F, 'screens.5', 1, '-1 for every n <= 3', 'def no_adjacent(n):\n    if n <= 3:\n        return -1\n    return ' + EO)
m(F, 'screens.5', 2, 'no special cases', 'def no_adjacent(n):\n    return ' + EO)
m(F, 'screens.5', 3, 'only n == 2 special', 'def no_adjacent(n):\n    if n == 2:\n        return -1\n    return ' + EO)
m(F, 'screens.5', 8, "the trap's permutations search", '''
from itertools import permutations
def no_adjacent(n):
    for p in permutations(range(1, n + 1)):
        if all(abs(p[i] - p[i + 1]) != 1 for i in range(n - 1)):
            return list(p)
    return -1
''')
m(F, 'screens.5', 9, 'backtracking search', '''
def no_adjacent(n):
    used = [False] * (n + 1)
    out = []
    def go():
        if len(out) == n:
            return True
        for v in range(1, n + 1):
            if not used[v] and (not out or abs(out[-1] - v) != 1):
                used[v] = True; out.append(v)
                if go():
                    return True
                used[v] = False; out.pop()
        return False
    return list(out) if go() else -1
''')
# ---- l9 screens[8] fill_array
LOOP = '''    out = []
    extra = s - n
    for _ in range(n):
        add = min(k - 1, extra)
        out.append(1 + add)
        extra -= add
    return out
'''
m(F, 'screens.8', 6, 'no upper bound check', 'def fill_array(n, s, k):\n    if s < n:\n        return -1\n' + LOOP)
m(F, 'screens.8', 7, 'no lower bound check', 'def fill_array(n, s, k):\n    if s > n * k:\n        return -1\n' + LOOP)
m(F, 'screens.8', 6, 'no checks at all', 'def fill_array(n, s, k):\n' + LOOP)
m(F, 'screens.8', 4, 'divides by k - 1', '''
def fill_array(n, s, k):
    if s < n or s > n * k:
        return -1
    extra = s - n
    full, rest = divmod(extra, k - 1)
    out = [k] * full
    if len(out) < n:
        out.append(1 + rest)
    return out + [1] * (n - len(out))
''')
m(F, 'screens.8', 9, 'add 1 at a time', '''
def fill_array(n, s, k):
    if s < n or s > n * k:
        return -1
    out = [1] * n
    extra = s - n
    i = 0
    while extra > 0:
        if out[i] < k:
            out[i] += 1
            extra -= 1
        else:
            i += 1
    return out
''')
# ---- l10 screens[4] max_non_overlapping
F = 'l10-greedy-proofs.json'
G = '''
def max_non_overlapping(intervals):
    count = 0
    end = float("-inf")
    for s, e in sorted(intervals, key=%s):
        if s %s end:
            count += 1
            end = e
    return count
'''
m(F, 'screens.4', 1, 'sort by start', G % ('lambda x: x[0]', '>='))
m(F, 'screens.4', 1, 'plain sorted() (start, then end)', '''
def max_non_overlapping(intervals):
    count = 0
    end = float("-inf")
    for s, e in sorted(intervals):
        if s >= end:
            count += 1
            end = e
    return count
''')
m(F, 'screens.4', 1, 'sort by length, keep what fits', '''
def max_non_overlapping(intervals):
    kept = []
    for s, e in sorted(intervals, key=lambda x: x[1] - x[0]):
        if all(e <= a or s >= b for a, b in kept):
            kept.append((s, e))
    return len(kept)
''')
m(F, 'screens.4', 2, '> for >=', G % ('lambda x: x[1]', '>'))
m(F, 'screens.4', 8, 'check every kept meeting', '''
def max_non_overlapping(intervals):
    kept = []
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if all(e <= a or s >= b for a, b in kept):
            kept.append((s, e))
    return len(kept)
''')
# ---- l10 screens[6] min_rooms
m(F, 'screens.6', 2, 'start before end on ties', '''
def min_rooms(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 0))
        events.append((e, 1))
    events.sort()
    busy = best = 0
    for _, kind in events:
        busy += 1 if kind == 0 else -1
        best = max(best, busy)
    return best
''')
m(F, 'screens.6', 2, 'sort by time only, starts appended first', '''
def min_rooms(intervals):
    events = [(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals]
    events.sort(key=lambda ev: ev[0])
    busy = best = 0
    for _, change in events:
        busy += change
        best = max(best, busy)
    return best
''')
m(F, 'screens.6', 3, 'set() of meetings', '''
def min_rooms(intervals):
    events = []
    for s, e in set(intervals):
        events.append((s, 1))
        events.append((e, -1))
    events.sort()
    busy = best = 0
    for _, change in events:
        busy += change
        best = max(best, busy)
    return best
''')
m(F, 'screens.6', 7, 'count at every time point', '''
def min_rooms(intervals):
    lo = min(s for s, e in intervals)
    hi = max(e for s, e in intervals)
    best = 0
    for t in range(lo, hi):
        best = max(best, sum(1 for s, e in intervals if s <= t < e))
    return best
''')
m(F, 'screens.6', 7, 'compare every pair', '''
def min_rooms(intervals):
    best = 0
    for s, e in intervals:
        best = max(best, sum(1 for a, b in intervals if a <= s < b))
    return best
''')
# ---- l10 screens[8] greedy_counterexample
m(F, 'screens.8', 1, 'returns the first failure', '''
import random
def greedy_counterexample(greedy, brute, gen, trials, seed):
    rng = random.Random(seed)
    for _ in range(trials):
        case = gen(rng)
        if greedy(case) != brute(case):
            return case
    return None
''')
m(F, 'screens.8', 1, 'keeps the last smallest (<=)', '''
import random
def greedy_counterexample(greedy, brute, gen, trials, seed):
    rng = random.Random(seed)
    best = None
    for _ in range(trials):
        case = gen(rng)
        if greedy(case) != brute(case):
            if best is None or case[1] <= best[1]:
                best = case
    return best
''')
# ---- l11 screens[3] best_subset
F = 'l11-bitmasks.json'
BS = '''
def best_subset(profits, risks, limit):
    n = len(profits)
    best = 0
    for mask in range(%s):
        profit = risk = 0
        for i in range(n):
            if mask >> i & 1:
                profit += profits[i]
                risk += risks[i]
        if risk %s limit and profit > best:
            best = profit
    return best
'''
m(F, 'screens.3', 1, '< for <=', BS % ('1 << n', '<'))
m(F, 'screens.3', 5, 'range(1 << n - 1), the next trap', BS % ('1 << n - 1', '<='))
m(F, 'screens.3', 2, 'max() over non-empty masks', '''
def best_subset(profits, risks, limit):
    n = len(profits)
    cands = []
    for mask in range(1, 1 << n):
        profit = sum(profits[i] for i in range(n) if mask >> i & 1)
        risk = sum(risks[i] for i in range(n) if mask >> i & 1)
        if risk <= limit:
            cands.append(profit)
    return max(cands)
''')
m(F, 'screens.3', 3, 'n == 0 special, max() of fitting non-empty', '''
def best_subset(profits, risks, limit):
    n = len(profits)
    if n == 0:
        return 0
    cands = []
    for mask in range(1, 1 << n):
        profit = sum(profits[i] for i in range(n) if mask >> i & 1)
        risk = sum(risks[i] for i in range(n) if mask >> i & 1)
        if risk <= limit:
            cands.append(profit)
    return max(cands)
''')
# ---- l11 screens[5] count_subsets_with_sum
CS = '''
def count_subsets_with_sum(xs, target):
    n = len(xs)
    count = 0
    for mask in range(%s, 1 << n):
        if sum(xs[i] for i in range(n) if mask >> i & 1) == target:
            count += 1
    return count
'''
m(F, 'screens.5', 2, 'masks from 1', CS % '1')
m(F, 'screens.5', 3, 'empty list special, masks from 1', 'def count_subsets_with_sum(xs, target):\n    if not xs:\n        return 1 if target == 0 else 0\n    return _c(xs, target)\n' + (CS % '1').replace('count_subsets_with_sum', '_c'))
m(F, 'screens.5', 4, 'distinct subsets of values', '''
from itertools import combinations
def count_subsets_with_sum(xs, target):
    seen = set()
    for r in range(len(xs) + 1):
        for c in combinations(xs, r):
            if sum(c) == target:
                seen.add(tuple(sorted(c)))
    return len(seen)
''')
m(F, 'screens.5', 5, 'knapsack counting DP', '''
def count_subsets_with_sum(xs, target):
    dp = [0] * (target + 1)
    dp[0] = 1
    for x in xs:
        for s in range(target, x - 1, -1):
            dp[s] += dp[s - x]
    return dp[target]
''')
# ---- l11 screens[6] popcounts
m(F, 'screens.6', 1, 'empty list for n = 0', '''
def popcounts(n):
    if n == 0:
        return []
    p = [0] * (1 << n)
    for m in range(1, 1 << n):
        p[m] = p[m >> 1] + (m & 1)
    return p
''')
m(F, 'screens.6', 8, 'bin().count', '''
def popcounts(n):
    return [bin(m).count("1") for m in range(1 << n)]
''')
# ---- l12 screens[4] apply_ranges
F = 'l12-difference-arrays.json'
m(F, 'screens.4', 1, 'n cells', '''
def apply_ranges(n, updates):
    d = [0] * n
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    out, run = [], 0
    for i in range(n):
        run += d[i]
        out.append(run)
    return out
''')
m(F, 'screens.4', 3, 'running total starts at day 1', '''
def apply_ranges(n, updates):
    d = [0] * (n + 1)
    for l, r, v in updates:
        d[l] += v
        d[r + 1] -= v
    out = [0] * n
    for i in range(1, n):
        out[i] = out[i - 1] + d[i]
    return out
''')
m(F, 'screens.4', 2, '-v at r', '''
def apply_ranges(n, updates):
    d = [0] * (n + 1)
    for l, r, v in updates:
        d[l] += v
        d[r] -= v
    out, run = [], 0
    for i in range(n):
        run += d[i]
        out.append(run)
    return out
''')
m(F, 'screens.4', 7, 'scan every update for each day', '''
def apply_ranges(n, updates):
    out = []
    for i in range(n):
        total = 0
        for l, r, v in updates:
            if l <= i <= r:
                total += v
        out.append(total)
    return out
''')
m(F, 'screens.4', 8, 'loop over each range', '''
def apply_ranges(n, updates):
    out = [0] * n
    for l, r, v in updates:
        for i in range(l, r + 1):
            out[i] += v
    return out
''')
# ---- l12 screens[7] max_coverage
m(F, 'screens.7', 1, '-1 at r', '''
def max_coverage(n, intervals):
    d = [0] * (n + 1)
    for l, r in intervals:
        d[l] += 1
        d[r] -= 1
    best = run = 0
    for i in range(n):
        run += d[i]
        best = max(best, run)
    return best
''')
m(F, 'screens.7', 3, 'max() of the counts dictionary', '''
def max_coverage(n, intervals):
    cover = {}
    for l, r in intervals:
        cover[l] = cover.get(l, 0) + 1
        cover[r + 1] = cover.get(r + 1, 0) - 1
    best = run = 0
    for day in sorted(cover):
        run += cover[day]
        best = max(best, run)
    return max(best, max(cover.values()))
''')
m(F, 'screens.7', 7, 'fill every day', '''
def max_coverage(n, intervals):
    c = [0] * n
    for l, r in intervals:
        for i in range(l, r + 1):
            c[i] += 1
    return max(c)
''')
# ---- review-3 ring_string
F = 'review-3.json'
m(F, 'items.1', 1, "'a' for n = 1", '''
def ring_string(n):
    if n % 2 == 0:
        return "ab" * (n // 2)
    return "ab" * (n // 2) + ("c" if n > 1 else "a")
''')
m(F, 'items.1', 3, 'alternate a and b only', '''
def ring_string(n):
    if n == 1:
        return -1
    return ("ab" * n)[:n]
''')
m(F, 'items.1', 1, 'no special cases at all', '''
def ring_string(n):
    return ("ab" * n)[:n]
''')
# ---- homework-1
F = 'homework-1.json'
m(F, 'items.0', 2, 'a set of seen values', '''
def count_pairs(xs, k):
    seen = set()
    count = 0
    for x in xs:
        if k - x in seen:
            count += 1
        seen.add(x)
    return count
''')
m(F, 'items.0', 9, 'every pair, indexing xs', '''
def count_pairs(xs, k):
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] + xs[j] == k)
''')
m(F, 'items.0', 10, 'xs.count(k - x) in a loop', '''
def count_pairs(xs, k):
    total = 0
    for x in xs:
        total += xs.count(k - x)
        if 2 * x == k:
            total -= 1
    return total // 2
''')
m(F, 'items.0', 11, 'lists of positions, pairs counted one by one', '''
def count_pairs(xs, k):
    where = {}
    count = 0
    for j, x in enumerate(xs):
        for i in where.get(k - x, ()):
            count += 1
        where.setdefault(x, []).append(j)
    return count
''')
m(F, 'items.1', 1, 'at most k fills', '''
def longest_window(tickers, k):
    return min(k, len(tickers))
''')
m(F, 'items.1', 9, 'restart at every day, indexing', '''
def longest_window(tickers, k):
    n = len(tickers)
    best = 0
    for l in range(n):
        seen = set()
        for r in range(l, n):
            seen.add(tickers[r])
            if len(seen) > k:
                break
            best = max(best, r - l + 1)
    return best
''')
m(F, 'items.1', 11, 'restart at every day, on a copy', '''
def longest_window(tickers, k):
    t = list(tickers)
    n = len(t)
    best = 0
    for l in range(n):
        seen = set()
        for r in range(l, n):
            seen.add(t[r])
            if len(seen) > k:
                break
            best = max(best, r - l + 1)
    return best
''')
m(F, 'items.2', 1, '0-based slice', '''
def range_sums(xs, queries):
    return [sum(xs[l:r]) for l, r in queries]
''')
m(F, 'items.2', 6, 'sum per query', '''
def range_sums(xs, queries):
    return [sum(xs[l - 1:r]) for l, r in queries]
''')
# ---- homework-3
F = 'homework-3.json'
m(F, 'items.0', 7, 'sorted by start, s > last', '''
def fewest_alerts(windows):
    count, last = 0, float("-inf")
    for s, e in sorted(windows):
        if s > last:
            count += 1
            last = e
    return count
''')
m(F, 'items.0', 2, 'sorted by start, alert at end, containment test', '''
def fewest_alerts(windows):
    count, last = 0, float("-inf")
    for s, e in sorted(windows):
        if not (s <= last <= e):
            count += 1
            last = e
    return count
''')
m(F, 'items.0', 3, '>= for >', '''
def fewest_alerts(windows):
    count, last = 0, float("-inf")
    for s, e in sorted(windows, key=lambda w: w[1]):
        if s >= last:
            count += 1
            last = e
    return count
''')
m(F, 'items.0', 9, 'check every alert', '''
def fewest_alerts(windows):
    alerts = []
    for s, e in sorted(windows, key=lambda w: w[1]):
        if not any(s <= t <= e for t in alerts):
            alerts.append(e)
    return len(alerts)
''')
m(F, 'items.1', 2, 'pop on <', '''
def spans(closes):
    out, stack = [], []
    for i, c in enumerate(closes):
        while stack and closes[stack[-1]] < c:
            stack.pop()
        out.append(i + 1 if not stack else i - stack[-1])
        stack.append(i)
    return out
''')
m(F, 'items.1', 7, 'walk back day by day', '''
def spans(closes):
    out = []
    for i in range(len(closes)):
        j = i
        while j > 0 and closes[j - 1] <= closes[i]:
            j -= 1
        out.append(i - j + 1)
    return out
''')
m(F, 'items.1', 8, 'walk back on a copy', '''
def spans(closes):
    c = list(closes)
    out = []
    for i in range(len(c)):
        j = i
        while j > 0 and c[j - 1] <= c[i]:
            j -= 1
        out.append(i - j + 1)
    return out
''')
CAP = '''
def first_over_cap(n, updates, cap):
    def over(k):
        d = [0] * (n + 1)
        for l, r, v in updates[:k]:
            d[l] += v
            d[r + 1] -= v
        run = 0
        for i in range(n):
            run += d[i]
            if run %s cap:
                return True
        return False
%s
    lo, hi = 1, len(updates)
    while lo < hi:
        mid = (lo + hi) // 2
        if over(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
'''
CHK = '    if not over(len(updates)):\n        return -1'
m(F, 'items.2', 1, '>= cap', CAP % ('>=', CHK))
m(F, 'items.2', 3, 'no -1 check', CAP % ('>', ''))
m(F, 'items.2', 8, 'apply each update day by day', '''
def first_over_cap(n, updates, cap):
    a = [0] * n
    for k, (l, r, v) in enumerate(updates, 1):
        for i in range(l, r + 1):
            a[i] += v
            if a[i] > cap:
                return k
    return -1
''')
m(F, 'items.2', 8, 'difference array rebuilt after every update', '''
def first_over_cap(n, updates, cap):
    d = [0] * (n + 1)
    for k, (l, r, v) in enumerate(updates, 1):
        d[l] += v
        d[r + 1] -= v
        run = 0
        for i in range(n):
            run += d[i]
            if run > cap:
                return k
    return -1
''')

# Codings whose first failing test is NOT the line probed, with the key seen under Pyodide. 'info': the line is still reached by
# another natural coding or names no mistake (see the ledger). 'finding': the line's named mistake cannot produce it.
OTHER = {
    ('l1-reading-statements.json', 'best = 0, day 1 forced'): ('test-1', 'info'),
    ('l2-limits-to-complexity.json', "the table's thresholds"): ('test-3', 'info'),
    ('l3-fast-io.json', "split(b'\\n') then int per line"): ('test-1', 'info'),
    ('l3-fast-io.json', "split(b'\\n'), then split() per line"): (None, 'info'),
    ('l3-fast-io.json', 'sys.stdin.readline per line (line reading, line 4 names it)'): ('test-5', 'info'),
    ('l3-fast-io.json', 'read().split(newline) by index'): ('test-5', 'info'),
    ('l4-stress-testing.json', 'while True, ignores trials'): ('test-1', 'info'),
    ('l4-stress-testing.json', 'gen called twice per trial'): ('test-1', 'info'),
    ('l10-greedy-proofs.json', 'keeps the last smallest (<=)'): (None, 'info'),
    ('l11-bitmasks.json', 'range(1 << n - 1), the next trap'): ('test-1', 'info'),
    ('l12-difference-arrays.json', '-v at r'): ('test-1', 'info'),
}
# Codings that fail by the page's time limit (5 s a test, plus any budget): only Pyodide can show them.
TIMING = {'tokens.pop(0)', 'max(xs[:i]) per day', 'no guard before 2 ** n', 'no guard, steps in a list', 'every pair, on a sorted copy',
          'while True, ignores trials', "the trap's permutations search", 'add 1 at a time', 'check every kept meeting',
          'count at every time point', 'compare every pair', 'loop over each range', 'fill every day', 'xs.count(k - x) in a loop',
          'lists of positions, pairs counted one by one', 'restart at every day, on a copy', 'sum per query', 'check every alert',
          'walk back on a copy', 'apply each update day by day', 'difference array rebuilt after every update', 'backtracking search'}
PYTEST = ('l4-stress-testing.json', 'screens.8')

SWEEP = r'''
import fs from 'node:fs'; import path from 'node:path'; import { pathToFileURL } from 'node:url';
const [,, appDir, pkgs, inFile, outFile] = process.argv;
const { makeRunner } = await import(pathToFileURL(path.join(appDir, 'tools/code-runner.mjs')).href);
const R = makeRunner({ pkgs, root: appDir, jobs: 1 });
const jobs = JSON.parse(fs.readFileSync(inFile, 'utf8')); const out = [];
for (const j of jobs) {
  const d = JSON.parse(fs.readFileSync(path.join(appDir, 'content/courses/contests', j.file), 'utf8')); const [k, i] = j.loc.split('.');
  const r = await R.grade(d[k][+i].widget, j.src, 'tests');
  out.push({ key: r.key, timeout: r.timeoutAt != null });
}
await R.close(); fs.writeFileSync(outFile, JSON.stringify(out));
'''


class _Stop(Exception):
    pass


def cpython_key(spec, src, limit=20):
    """First failing test of a call-style widget in CPython: 'test-N', None when all pass. No page time limit."""
    def alarm(*_):
        raise _Stop()
    signal.signal(signal.SIGALRM, alarm)
    for i, t in enumerate(spec['tests']):
        ns = {'__learner_source__': src}
        try:
            signal.alarm(limit)
            exec(spec.get('prelude', ''), ns)
            exec(src, ns)
            if spec.get('postlude'):
                exec(spec['postlude'], ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); ok = False
                except Exception as e:
                    ok = type(e).__name__ == t['expect']
            else:
                ok = eval(t['call'], ns) == eval(t['expect'], ns)
        except _Stop:
            ok = False
        except Exception:
            ok = False
        finally:
            signal.alarm(0)
        if not ok:
            return 'test-%d' % (i + 1)
    return None


def script_key(spec, src):
    """First failing test of a stdin/stdout program in CPython, with the page's recursion limit of 3000."""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'main.py'
        p.write_text('import sys\nsys.setrecursionlimit(3000)\n' + src)
        for i, t in enumerate(spec['tests']):
            try:
                r = subprocess.run([sys.executable, str(p)], input=t['stdin'], capture_output=True, text=True, timeout=30)
                ok = r.returncode == 0 and r.stdout.rstrip('\n') == t['expect'].rstrip('\n')
            except subprocess.TimeoutExpired:
                ok = False
            if not ok:
                return 'test-%d' % (i + 1)
    return None


def pytest_key(spec, src):
    """The pytest widget (l4 screens[8]) in a child CPython with real pytest: the node runner cannot run it (see the audit)."""
    with tempfile.TemporaryDirectory() as d:
        prog = ('import json, sys\nspec = json.load(open(sys.argv[1]))\nsrc = open(sys.argv[2]).read()\n'
                'ns = {"__learner_source__": src}\nexec(spec["prelude"], ns)\nexec(src, ns)\nexec(spec["postlude"], ns)\nkey = None\n'
                'for i, t in enumerate(spec["tests"]):\n    try:\n        ok = eval(t["call"], ns) == eval(t["expect"], ns)\n    except Exception:\n        ok = False\n'
                '    if not ok:\n        key = "test-%d" % (i + 1)\n        break\nsys.stderr.write("KEY=" + str(key))\n')
        (Path(d) / 'run.py').write_text(prog)
        (Path(d) / 'spec.json').write_text(json.dumps(spec))
        (Path(d) / 'src.py').write_text(src)
        r = subprocess.run([sys.executable, 'run.py', 'spec.json', 'src.py'], cwd=d, capture_output=True, text=True, timeout=300)
        if 'KEY=' not in r.stderr:
            return 'no-pytest'
        k = r.stderr.rsplit('KEY=', 1)[1].strip()
        return None if k == 'None' else k


def part_b(pkgs):
    jobs = [j for j in M]
    keys = {}
    if pkgs:
        with tempfile.TemporaryDirectory() as d:
            run = [j for j in jobs if (j['file'], j['loc']) != PYTEST]
            (Path(d) / 'sweep.mjs').write_text(SWEEP)
            (Path(d) / 'in.json').write_text(json.dumps(run))
            subprocess.run(['node', str(Path(d) / 'sweep.mjs'), str(ROOT / 'app'), pkgs, str(Path(d) / 'in.json'), str(Path(d) / 'out.json')],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for j, o in zip(run, json.loads((Path(d) / 'out.json').read_text())):
                keys[(j['file'], j['name'])] = o['key']
    skipped = 0
    for j in jobs:
        ident = (j['file'], j['name'])
        spec = widget(j['file'], j['loc'])
        if (j['file'], j['loc']) == PYTEST:
            got = pytest_key(spec, j['src'])
            if got == 'no-pytest':
                skipped += 1
                continue
        elif ident in keys:
            got = keys[ident]
        elif j['name'] in TIMING:
            skipped += 1
            continue
        elif any('stdin' in t for t in spec['tests']):
            got = script_key(spec, j['src'])
        else:
            got = cpython_key(spec, j['src'])
        want = 'test-%d' % j['line']
        seen, kind = OTHER.get(ident, (want, 'reach'))
        where = '%s %s byKey.test-%d' % (j['file'][:-5], j['loc'], j['line'])
        if kind == 'finding':
            check('%s: "%s" first fails test %d (it fails %s)' % (where, j['name'], j['line'], got), got == want)
        else:
            check('%s: "%s" gives the recorded key %s' % (where, j['name'], seen), got == seen, got)
    return skipped


def part_cxx():
    """l3 screens[10], the C++ lines, natively. int is 4 bytes here as on wasm32; long is modelled with int32_t."""
    w = widget('l3-fast-io.json', 'screens.10')
    sol = w['solution']
    variants = {
        ('best = 0', 1): sol.replace('if (i == 0 || x > best) best = x;', 'if (x > best) best = x;'),
        ('int sum', 3): sol.replace('long long sum = 0, best = 0;', 'int sum = 0; long long best = 0;'),
        ('long sum (4 bytes on wasm32)', 3): '#include <cstdint>\n' + sol.replace('long long sum = 0, best = 0;', 'int32_t sum = 0; long long best = 0;'),
    }
    with tempfile.TemporaryDirectory() as d:
        for (name, line), src in variants.items():
            assert src != sol
            (Path(d) / 'a.cpp').write_text(src)
            subprocess.run(['clang++', '-O1', '-fwrapv', '-fno-exceptions', str(Path(d) / 'a.cpp'), '-o', str(Path(d) / 'a.out')], check=True)
            got = None
            for i, t in enumerate(w['tests']):
                r = subprocess.run([str(Path(d) / 'a.out')], input=t['stdin'], capture_output=True, text=True)
                if r.stdout.rstrip('\n') != t['expect'].rstrip('\n'):
                    got = i + 1
                    break
            check('l3 screens.10 byKey.test-%d: C++ "%s" first fails test %d' % (line, name, line), got == line, got)


if __name__ == '__main__':
    args = sys.argv[1:]
    pkgs = args[args.index('--pkgs') + 1] if '--pkgs' in args else None
    part_a()
    a = N[0]
    skipped = part_b(pkgs)
    if '--cxx' in args:
        part_cxx()
    print('%d checks (%d in part A, %d codings in part B%s), %d failed' % (
        N[0], a, len(M), ', %d skipped: timing or no pytest' % skipped if skipped else '', len(FAILS)))
    for f in FAILS:
        print('  failing:', f)
    sys.exit(1 if FAILS else 0)
