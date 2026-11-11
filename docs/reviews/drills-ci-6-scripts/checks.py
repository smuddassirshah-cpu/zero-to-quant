"""Three checks on pack 6.
usage: checks.py <drills dir> [constraints] [random [N]] [planted]

constraints: evaluates every example and hidden call with the function replaced
  by a recorder, then tests the real arguments against the PROSE constraints,
  including the generated calls the validator skips.
random: the model solution against mine.py and against a brute force written
  here, on N (default 3000) small random inputs a drill, built to hit ties,
  zeros, negatives, equal values and the smallest sizes; then model against
  mine on 300 larger inputs.
planted: how each planted solution first fails (test, value returned, wanted).
"""
import glob
import itertools
import json
import multiprocessing as mp
import os
import random
import sys
import time
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = 1_000_000_007


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == 'pack-6':
            out[j['id']] = j
    return out


def ints(xs, lo, hi):
    for x in xs:
        assert type(x) is int and lo <= x <= hi, 'value %r' % (x,)


# ------------------------------------------------------------ constraints
def c_best_session(pnl):
    assert 1 <= len(pnl) <= 100000
    ints(pnl, -10000, 10000)


def c_ways_up(n, broken):
    assert 1 <= n <= 100000
    ints(broken, 1, n)
    assert len(set(broken)) == len(broken), 'repeat'


def c_best_shifts(pay):
    assert 1 <= len(pay) <= 100000
    ints(pay, 0, 10000)


c_best_rent = c_best_shifts


def c_solve_change_ways(text):
    tok = text.split()
    k = int(tok[0])
    coins = [int(x) for x in tok[1:1 + k]]
    q = int(tok[1 + k])
    fares = [int(x) for x in tok[2 + k:]]
    assert 1 <= k <= 20 and len(coins) == k and len(set(coins)) == k
    ints(coins, 1, 20000)
    assert 1 <= q <= 100000 and len(fares) == q, 'fares %d of %d' % (len(fares), q)
    ints(fares, 0, 20000)
    lines = [x for x in text.split('\n') if x.strip()]
    assert len(lines[0].split()) == 1 and len(lines[1].split()) == k and len(lines[2].split()) == 1, 'line layout'


def c_best_product_stretch(factors):
    assert 2 <= len(factors) <= 2000
    ints(factors, -9, 9)


def c_paving_ways(n, drains):
    assert 1 <= n <= 20000
    for r, c in drains:
        assert type(r) is int and type(c) is int and 0 <= r <= 2 and 0 <= c < n, 'drain %r' % ((r, c),)
    assert len({(r, c) for r, c in drains}) == len(drains), 'repeat'


def c_cooldown_profit(prices, k):
    assert 1 <= len(prices) <= 100000
    ints(prices, 1, 10000)
    assert type(k) is int and 0 <= k <= 100000


def c_fewest_words(text, words):
    assert 1 <= len(text) <= 20000 and text.isalpha() and text.islower() and text.isascii()
    assert 1 <= len(words) <= 5000 and len(set(words)) == len(words)
    for w in words:
        assert 1 <= len(w) <= 20 and w.isalpha() and w.islower() and w.isascii(), 'word %r' % w


def c_rising_readings(readings):
    assert 1 <= len(readings) <= 100000
    ints(readings, -10 ** 9, 10 ** 9)


def c_solve_tape_decodes(text):
    lines = [x.strip() for x in text.split('\n') if x.strip()]
    t = int(lines[0])
    tapes = lines[1:]
    assert 1 <= t <= 1000 and len(tapes) == t, 'tapes %d of %d' % (len(tapes), t)
    assert all(len(s) >= 1 and set(s) <= set('0123456789?') for s in tapes), 'chars'
    assert sum(len(s) for s in tapes) <= 200000, 'total %d' % sum(len(s) for s in tapes)


def c_fewest_tokens(values, amount):
    assert 1 <= amount <= 20000 and 1 <= len(values) <= 15 and len(set(values)) == len(values)
    ints(values, 1, 10000)


def c_stride_ways(n, strides):
    assert type(n) is int and 0 <= n <= 10 ** 18
    assert 1 <= len(strides) <= 8 and len(set(strides)) == len(strides)
    ints(strides, 1, 8)


def c_longest_nest(crates):
    assert 1 <= len(crates) <= 100000
    for c in crates:
        assert len(c) == 2
        ints(c, 1, 10 ** 9)


def c_best_trips(prices, k, fee):
    assert 1 <= len(prices) <= 3000
    ints(prices, 1, 10000)
    assert type(k) is int and 1 <= k <= 30 and type(fee) is int and 0 <= fee <= 10000


def constraints(drills):
    bad = calls = 0
    for did, j in drills.items():
        fn = j['fn']
        chk = globals()['c_' + fn]
        seen = []
        env = {fn: lambda *a, **k: seen.append((a, k)) or 0}
        cases = [('ex', i, t) for i, t in enumerate(j['examples'])] + [('t', i, t) for i, t in enumerate(j['tests'])]
        for kind, i, t in cases:
            seen.clear()
            try:
                eval(t['call'], env)
            except Exception:
                pass
            assert len(seen) >= 1, (did, kind, i)
            for a, k in seen:
                calls += 1
                try:
                    chk(*a, **k)
                except AssertionError as e:
                    bad += 1
                    print('OUTSIDE', did, kind, i, e)
    print('%d calls read, %d outside the prose constraints' % (calls, bad))


# ------------------------------------------------------------ brute forces
def b_best_session(pnl):
    best = None
    for s in range(len(pnl)):
        for e in range(s, len(pnl)):
            key = (-sum(pnl[s:e + 1]), s, e - s)
            if best is None or key < best[0]:
                best = (key, [sum(pnl[s:e + 1]), s, e])
    return best[1]


def b_ways_up(n, broken):
    bad = set(broken)

    def go(i):
        if i == n:
            return 1
        return sum(go(i + d) for d in (1, 2, 3) if i + d <= n and i + d not in bad)
    return go(0) % MOD


def b_best_shifts(pay):
    n = len(pay)
    best = None
    for m in range(1 << n):
        if m & (m >> 1):
            continue
        key = (-sum(pay[i] for i in range(n) if m >> i & 1), bin(m).count('1'))
        if best is None or key < best:
            best = key
    return [-best[0], best[1]]


def b_best_rent(rents):
    n = len(rents)
    best = 0
    for m in range(1 << n):
        on = [i for i in range(n) if m >> i & 1]
        ok = all(b - a >= 3 and n - (b - a) >= 3 for a, b in itertools.combinations(on, 2))
        if ok:
            best = max(best, sum(rents[i] for i in on))
    return best


def b_solve_change_ways(text):
    tok = [int(x) for x in text.split()]
    k = tok[0]
    coins = tok[1:1 + k]
    fares = tok[2 + k:2 + k + tok[1 + k]]

    def go(i, left):
        if left == 0:
            return 1
        if i == k:
            return 0
        return sum(go(i + 1, left - c * coins[i]) for c in range(left // coins[i] + 1))
    return '\n'.join(str(go(0, f) % MOD) for f in fares)


def b_best_product_stretch(f):
    best = None
    for s in range(len(f)):
        p = f[s]
        for e in range(s + 1, len(f)):
            p *= f[e]
            if best is None or p > best:
                best = p
    return best


def b_paving_ways(n, drains):
    full = [[False] * n for _ in range(3)]
    for r, c in drains:
        full[r][c] = True

    def go(pos):
        while pos < 3 * n and full[pos % 3][pos // 3]:
            pos += 1
        if pos == 3 * n:
            return 1
        r, c = pos % 3, pos // 3
        tot = 0
        full[r][c] = True
        if r < 2 and not full[r + 1][c]:
            full[r + 1][c] = True
            tot += go(pos + 1)
            full[r + 1][c] = False
        if c + 1 < n and not full[r][c + 1]:
            full[r][c + 1] = True
            tot += go(pos + 1)
            full[r][c + 1] = False
        full[r][c] = False
        return tot
    return go(0) % MOD


def b_cooldown_profit(prices, k):
    n = len(prices)

    @lru_cache(None)
    def go(i, holding, wait):
        if i >= n:
            return 0
        best = go(i + 1, holding, max(0, wait - 1))
        if holding:
            best = max(best, prices[i] + go(i + 1, False, k))
        elif wait == 0:
            best = max(best, -prices[i] + go(i + 1, True, 0))
        return best
    return go(0, False, 0)


def b_fewest_words(text, words):
    @lru_cache(None)
    def go(i):
        if i == len(text):
            return 0
        best = 10 ** 9
        for w in words:
            if text.startswith(w, i):
                best = min(best, 1 + go(i + len(w)))
        return best
    r = go(0)
    return r if r < 10 ** 9 else -1


def b_rising_readings(a):
    n = len(a)
    best = None
    for m in range(1, 1 << n):
        s = [a[i] for i in range(n) if m >> i & 1]
        if all(x < y for x, y in zip(s, s[1:])):
            key = (-len(s), s[-1])
            if best is None or key < best:
                best = key
    return [-best[0], best[1]]


def _decodes(s):
    @lru_cache(None)
    def go(i):
        if i == len(s):
            return 1
        tot = 0
        if s[i] != '0':
            tot += go(i + 1)
            if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26:
                tot += go(i + 2)
        return tot
    return go(0)


def b_solve_tape_decodes(text):
    lines = text.split()
    out = []
    for s in lines[1:1 + int(lines[0])]:
        q = s.count('?')
        tot = 0
        for fill in itertools.product('0123456789', repeat=q):
            it = iter(fill)
            tot += _decodes(''.join(next(it) if ch == '?' else ch for ch in s))
        out.append(str(tot % MOD))
    return '\n'.join(out)


def b_fewest_tokens(values, amount):
    vs = sorted(values, reverse=True)
    found = []

    def go(i, left, cur):
        if left == 0:
            found.append(list(cur))
            return
        for t in range(i, len(vs)):
            if vs[t] <= left:
                cur.append(vs[t])
                go(t, left - vs[t], cur)
                cur.pop()
    go(0, amount, [])
    if not found:
        return []
    m = min(len(f) for f in found)
    return max(f for f in found if len(f) == m)


def b_stride_ways(n, strides):
    f = [1] + [0] * n
    for i in range(1, n + 1):
        f[i] = sum(f[i - s] for s in strides if s <= i)
    return f[n] % MOD


def b_longest_nest(crates):
    n = len(crates)
    best = 0
    for m in range(1, 1 << n):
        s = sorted(crates[i] for i in range(n) if m >> i & 1)
        if all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(s, s[1:])):
            best = max(best, len(s))
    return best


def b_best_trips(prices, k, fee):
    n = len(prices)
    best = 0
    # every choice of up to k disjoint (buy, sell) pairs, one trade a day
    def go(start, left, tot):
        nonlocal best
        best = max(best, tot)
        if not left:
            return
        for b in range(start, n):
            for s in range(b + 1, n):
                go(s + 1, left - 1, tot + prices[s] - prices[b] - fee)
    go(0, k, 0)
    return best


# ------------------------------------------------------------ generators
R = random.Random(60606)


def g_best_session(big):
    n = R.randint(1, 400 if big else 8)
    w = R.choice([1, 2, 3, 10000])
    return ([R.randint(-w, w) for _ in range(n)],)


def g_ways_up(big):
    n = R.randint(1, 300 if big else 12)
    return (n, R.sample(range(1, n + 1), R.randint(0, min(n, R.choice([0, 1, 2, n // 2])))))


def g_best_shifts(big):
    n = R.randint(1, 300 if big else 11)
    w = R.choice([1, 2, 3, 6, 10000])
    return ([R.randint(0, w) for _ in range(n)],)


def g_best_rent(big):
    n = R.randint(1, 300 if big else 12)
    w = R.choice([1, 2, 3, 9, 10000])
    return ([R.randint(0, w) for _ in range(n)],)


def g_solve_change_ways(big):
    k = R.randint(1, 4)
    top = 400 if big else 24
    coins = R.sample(range(1, (40 if big else 9) + 1), k)
    q = R.randint(1, 5)
    fares = [R.randint(0, top) for _ in range(q)]
    sep = R.choice(['\n', ' ', ' \n  '])
    return ('%d\n%s\n%d\n%s%s' % (k, ' '.join(map(str, coins)), q, sep.join(map(str, fares)), R.choice(['', '\n', '\n\n'])),)


def g_best_product_stretch(big):
    n = R.randint(2, 200 if big else 8)
    pool = R.choice([[-1, 0, 1], [-2, -1, 1, 2], [-3, -2, -1, 0, 1, 2, 3], list(range(-9, 10)), [-9, -1, 1, 9], [-2, 2, 3]])
    return ([R.choice(pool) for _ in range(n)],)


def g_paving_ways(big):
    n = R.randint(1, 60 if big else 5)
    cells = [[r, c] for r in range(3) for c in range(n)]
    m = R.choice([0, 1, 2, 2, 3, 4, n])
    return (n, R.sample(cells, min(m, len(cells))))


def g_cooldown_profit(big):
    n = R.randint(1, 200 if big else 9)
    w = R.choice([3, 6, 10000])
    return ([R.randint(1, w) for _ in range(n)], R.choice([0, 1, 2, 3, n - 1, n, n + 3]))


def g_fewest_words(big):
    alpha = R.choice(['a', 'ab', 'abc'])
    n = R.randint(1, 200 if big else 10)
    text = ''.join(R.choice(alpha) for _ in range(n))
    words = set()
    for _ in range(R.randint(1, 6)):
        if R.random() < 0.6 and n > 1:
            i = R.randrange(n)
            words.add(text[i:i + R.randint(1, 4)])
        else:
            words.add(''.join(R.choice(alpha) for _ in range(R.randint(1, 4))))
    words = list(words)
    R.shuffle(words)
    return (text, words)


def g_rising_readings(big):
    n = R.randint(1, 300 if big else 11)
    w = R.choice([2, 4, 8, 10 ** 9])
    return ([R.randint(-w, w) for _ in range(n)],)


def g_solve_tape_decodes(big):
    t = R.randint(1, 3)
    tapes = []
    for _ in range(t):
        n = R.randint(1, 60 if big else 7)
        pool = R.choice(['012?', '0123456789?', '12?', '?0', '126?7'])
        s = ''.join(R.choice(pool) for _ in range(n))
        if not big:
            while s.count('?') > 4:
                i = s.index('?')
                s = s[:i] + R.choice('0127') + s[i + 1:]
        tapes.append(s)
    return ('%d\n%s%s' % (t, '\n'.join(R.choice(['', ' ']) + s for s in tapes), R.choice(['', '\n', ' \n\n'])),)


def g_fewest_tokens(big):
    k = R.randint(1, 5)
    values = R.sample(range(1, (60 if big else 12) + 1), k)
    return (values, R.randint(1, 600 if big else 30))


def g_stride_ways(big):
    strides = R.sample(range(1, 9), R.randint(1, 8))
    return (R.randint(0, 3000 if big else 40), strides)


def g_longest_nest(big):
    n = R.randint(1, 200 if big else 9)
    w = R.choice([2, 3, 5, 10 ** 9]) if not big else R.choice([5, 20, 10 ** 9])
    return ([[R.randint(1, w), R.randint(1, w)] for _ in range(n)],)


def g_best_trips(big):
    n = R.randint(1, 120 if big else 8)
    w = R.choice([4, 9, 10000])
    return ([R.randint(1, w) for _ in range(n)], R.randint(1, 3 if not big else 30), R.choice([0, 0, 1, 2, w // 2, w]))


def rand(drills, N):
    mine = {}
    exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
    total = bad = 0
    for did, j in drills.items():
        fn = j['fn']
        model = {}
        exec(j['solution'], model)
        gen, brute, chk = globals()['g_' + fn], globals()['b_' + fn], globals()['c_' + fn]
        t0 = time.time()
        n_bad = 0
        for it in range(N + 300):
            big = it >= N
            args = gen(big)
            chk(*args)
            import copy
            a = model[fn](*copy.deepcopy(args))
            b = mine[fn](*copy.deepcopy(args))
            c = brute(*copy.deepcopy(args)) if not big else b
            total += 1
            if not (a == b == c):
                n_bad += 1
                if n_bad <= 3:
                    print('DISAGREE', did, repr(args)[:300], 'model', repr(a)[:80], 'mine', repr(b)[:80], 'brute', repr(c)[:80])
        bad += n_bad
        print('%-22s %d random inputs, %d disagreements, %.1fs' % (did, N + 300, n_bad, time.time() - t0))
    print('%d inputs, %d disagreements' % (total, bad))


# ------------------------------------------------------------ planted
def _first_fail(src, drill, q):
    env = {}
    try:
        exec(src, env)
    except Exception as e:  # noqa
        q.put('load error %r' % e)
        return
    for i, t in enumerate(drill['tests']):
        try:
            got = eval(t['call'], env)
            want = eval(t['expect'], env)
            if got != want:
                q.put('tests[%d] %s -> %s, wanted %s' % (i, t['call'][:70], repr(got)[:50], repr(want)[:50]))
                return
        except BaseException as e:  # noqa
            q.put('tests[%d] %s raises %s' % (i, t['call'][:70], type(e).__name__))
            return
    q.put('PASSES ALL')


def planted(drills):
    for did, j in drills.items():
        for k, p in enumerate(j['planted']):
            q = mp.Queue()
            pr = mp.Process(target=_first_fail, args=(p['code'], j, q))
            pr.start()
            pr.join(12)
            if pr.is_alive():
                pr.terminate()
                res = 'still running at 12 s'
            else:
                res = q.get(timeout=2)
            print('%s planted[%d]: %s\n    slip: %s' % (did, k, res, p['slip']))


if __name__ == '__main__':
    drills = load(sys.argv[1])
    todo = sys.argv[2:] or ['constraints', 'random', 'planted']
    if 'constraints' in todo:
        constraints(drills)
    if 'random' in todo:
        i = todo.index('random')
        N = int(todo[i + 1]) if len(todo) > i + 1 and todo[i + 1].isdigit() else 3000
        rand(drills, N)
    if 'planted' in todo:
        planted(drills)
