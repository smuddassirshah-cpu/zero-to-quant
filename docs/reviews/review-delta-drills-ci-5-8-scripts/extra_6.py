"""Pack 6 extras. Usage (repo root): python3 extra_6.py
Plain brute forces for the ten drills whose tests or model changed in the fix pass.
Each brute force runs on every example and hidden test small enough for it (the rest
are covered by mine_6.py through run.py), then against the model on random small inputs."""
import itertools
import json
import random
import sys

D = 'app/content/drills'
MOD = 1_000_000_007


def b_best_session(pnl):
    best = None
    for s in range(len(pnl)):
        tot = 0
        for e in range(s, len(pnl)):
            tot += pnl[e]
            key = (-tot, s, e - s)
            if best is None or key < best[0]:
                best = (key, [tot, s, e])
    return best[1]


def b_best_trips(prices, k, fee):
    n = len(prices)
    best = 0

    def go(day, left, profit):
        nonlocal best
        best = max(best, profit)
        if left == 0:
            return
        for b in range(day, n):
            for s in range(b + 1, n):
                go(s + 1, left - 1, profit + prices[s] - prices[b] - fee)
    go(0, k, 0)
    return best


def b_fewest_tokens(values, amount):
    vals = sorted(values, reverse=True)
    for size in range(1, amount // min(vals) + 1):
        found = [list(c) for c in itertools.combinations_with_replacement(vals, size) if sum(c) == amount]
        if found:
            return max(found)
    return []


def b_rising(readings):
    best = None
    n = len(readings)
    for mask in range(1, 1 << n):
        pick = [readings[i] for i in range(n) if mask >> i & 1]
        if all(a < b for a, b in zip(pick, pick[1:])):
            key = (-len(pick), pick[-1])
            if best is None or key < best:
                best = key
    return [-best[0], best[1]]


def b_nest(crates):
    best = 0
    n = len(crates)
    for size in range(1, n + 1):
        for idx in itertools.permutations(range(n), size):
            row = [crates[i] for i in idx]
            if all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(row, row[1:])):
                best = size
                break
        if best < size:
            break
    return best


def b_paving(n, drains):
    full = [[(r, c) in {tuple(d) for d in drains} for c in range(n)] for r in range(3)]

    def go():
        for c in range(n):
            for r in range(3):
                if not full[r][c]:
                    tot = 0
                    full[r][c] = True
                    if r + 1 < 3 and not full[r + 1][c]:
                        full[r + 1][c] = True
                        tot += go()
                        full[r + 1][c] = False
                    if c + 1 < n and not full[r][c + 1]:
                        full[r][c + 1] = True
                        tot += go()
                        full[r][c + 1] = False
                    full[r][c] = False
                    return tot
        return 1
    return go() % MOD


def b_product(factors):
    best = None
    for i in range(len(factors)):
        for j in range(i + 1, len(factors)):
            p = 1
            for x in factors[i:j + 1]:
                p *= x
            best = p if best is None else max(best, p)
    return best


def b_shifts(pay):
    best = None
    n = len(pay)
    for mask in range(1 << n):
        if mask & (mask >> 1):
            continue
        tot = sum(pay[i] for i in range(n) if mask >> i & 1)
        key = (-tot, bin(mask).count('1'))
        if best is None or key < best:
            best = key
    return [-best[0], best[1]]


def _msgs(s):
    if not s:
        return 1
    tot = 0
    if s[0] != '0':
        tot += _msgs(s[1:])
        if len(s) >= 2 and int(s[:2]) <= 26:
            tot += _msgs(s[2:])
    return tot


def b_tape(text):
    lines = [x.strip() for x in text.split('\n') if x.strip()]
    out = []
    for tape in lines[1:1 + int(lines[0])]:
        q = [i for i, ch in enumerate(tape) if ch == '?']
        tot = 0
        for fill in itertools.product('0123456789', repeat=len(q)):
            s = list(tape)
            for i, ch in zip(q, fill):
                s[i] = ch
            tot += _msgs(''.join(s))
        out.append(str(tot % MOD))
    return '\n'.join(out)


def b_words(text, words):
    best = [None]

    def go(i, used):
        if i == len(text):
            if best[0] is None or used < best[0]:
                best[0] = used
            return
        for w in words:
            if text.startswith(w, i):
                go(i + len(w), used + 1)
    go(0, 0)
    return -1 if best[0] is None else best[0]


def small_session(a):
    return len(a[0]) <= 300


BRUTES = {
    'ci-best-session': (b_best_session, lambda a: len(a[0]) <= 400,
                        lambda r: ([r.randint(-4, 4) for _ in range(r.randint(1, 9))],)),
    'ci-capped-trips': (b_best_trips, lambda a: len(a[0]) <= 9,
                        lambda r: ([r.randint(1, 12) for _ in range(r.randint(1, 8))], r.randint(1, 4), r.randint(0, 5))),
    'ci-fewest-tokens': (b_fewest_tokens, lambda a: a[1] <= 40 and len(a[0]) <= 6,
                         lambda r: (r.sample(range(1, 12), r.randint(1, 4)), r.randint(1, 30))),
    'ci-longest-rising': (b_rising, lambda a: len(a[0]) <= 14,
                          lambda r: ([r.randint(-5, 5) for _ in range(r.randint(1, 10))],)),
    'ci-nested-crates': (b_nest, lambda a: len(a[0]) <= 6,
                         lambda r: ([[r.randint(1, 4), r.randint(1, 4)] for _ in range(r.randint(1, 6))],)),
    'ci-paving-ways': (b_paving, lambda a: a[0] <= 8,
                       lambda r: (lambda n: (n, [list(x) for x in r.sample([(i, j) for i in range(3) for j in range(n)],
                                                                         r.randint(0, min(4, 3 * n)))]))(r.randint(1, 6))),
    'ci-product-stretch': (b_product, lambda a: len(a[0]) <= 60,
                           lambda r: ([r.randint(-3, 3) for _ in range(r.randint(2, 9))],)),
    'ci-shift-picks': (b_shifts, lambda a: len(a[0]) <= 16,
                       lambda r: ([r.randint(0, 5) for _ in range(r.randint(1, 10))],)),
    'ci-tape-decodes': (b_tape, lambda a: len(a[0]) <= 40 and a[0].count('?') <= 5,
                        lambda r: ('2\n' + '\n'.join(''.join(r.choice('0123?12') for _ in range(r.randint(1, 6))) for _ in range(2)) + '\n',)),
    'ci-word-split': (b_words, lambda a: len(a[0]) <= 12 and len(a[1]) <= 8,
                      lambda r: (''.join(r.choice('ab') for _ in range(r.randint(1, 9))),
                                 list({''.join(r.choice('ab') for _ in range(r.randint(1, 3))) for _ in range(r.randint(1, 4))}))),
}


def main():
    bad = 0
    for did, (brute, small, gen) in BRUTES.items():
        d = json.load(open(f'{D}/{did}.json'))
        env = {}
        exec(d['solution'], env)
        model = env[d['fn']]
        ran = 0
        seen = []
        probe = {d['fn']: lambda *a: seen.append(a)}
        for kind in ('examples', 'tests'):
            for i, t in enumerate(d[kind]):
                seen.clear()
                try:
                    eval(t['call'], dict(probe))
                except Exception:
                    pass          # a wrapped call (lambda r: ...) fails on None; the arguments are kept
                if len(seen) != 1 or not small(seen[0]):
                    continue
                args = seen[0]
                want = eval(t['expect'])
                got = eval(t['call'], {d['fn']: brute})
                ran += 1
                if got != want:
                    bad += 1
                    print('BRUTE DISAGREES', did, kind, i, args, 'brute', got, 'expect', want)
        rng = random.Random(606)
        dis = 0
        N = 300 if did == 'ci-nested-crates' else 1500
        for _ in range(N):
            args = gen(rng)
            import copy
            a, b = model(*copy.deepcopy(args)), brute(*copy.deepcopy(args))
            if a != b:
                dis += 1
                if dis < 3:
                    print('RANDOM DISAGREE', did, args, 'model', a, 'brute', b)
        bad += dis
        print('%-20s brute on %2d of %2d cases; %d random, %d disagreements'
              % (did, ran, len(d['examples']) + len(d['tests']), N, dis))
    sys.exit(1 if bad else 0)


main()
