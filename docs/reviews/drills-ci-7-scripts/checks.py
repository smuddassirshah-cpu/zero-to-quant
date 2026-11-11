"""Three checks on pack 7.
usage: checks.py <drills dir> [constraints] [random] [planted]

constraints: evaluates every example and hidden call with the function replaced
  by a recorder, then tests the real arguments against the PROSE constraints,
  including the generated calls the validator skips.
random: the model solution against mine.py and against a brute force written
  here, on random inputs inside the constraints built to hit ties, repeats,
  blocked cells, empty strings and binding limits.
planted: how each planted solution first fails (wrong value, exception, time).
"""
import glob
import json
import multiprocessing as mp
import os
import random
import re
import sys
import time
from itertools import combinations, permutations, product

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = 10 ** 9 + 7


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == 'pack-7':
            out[j['id']] = j
    return out


# ------------------------------------------------------------ constraints (prose)
def low(s):
    return s == '' or re.fullmatch('[a-z]+', s) is not None


def c_drop(grid):
    assert 1 <= len(grid) <= 200 and 1 <= len(grid[0]) <= 200
    assert all(len(r) == len(grid[0]) and set(r) <= set('.#P') for r in grid)
    assert grid[0][0] != '#' and grid[-1][-1] != '#'


def c_picks(values, gap):
    assert 1 <= len(values) <= 12 and len(set(values)) == len(values)
    assert all(type(v) is int and -1000 <= v <= 1000 for v in values) and 1 <= gap <= 2000


def c_mirrors(tape, k):
    assert 1 <= len(tape) <= 1000 and low(tape) and 1 <= k <= 1000


def c_tol(a, b, tol):
    assert len(a) <= 300 and len(b) <= 300 and 0 <= tol <= 10 ** 6
    assert all(type(x) is int and 0 <= x <= 10 ** 6 for x in a + b)


def c_edits(text):
    lines = [x.strip() for x in text.split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    assert all(lines), 'blank line inside'
    p = lines[0].split()
    assert len(p) == 3 and all(1 <= int(x) <= 100 for x in p)
    q = int(lines[1])
    assert 1 <= q <= 50 and len(lines) == 2 + q, 'q %d lines %d' % (q, len(lines))
    tot = 0
    for ln in lines[2:]:
        s, t = ln.split()
        assert 1 <= len(s) <= 300 and 1 <= len(t) <= 300 and low(s) and low(t)
        tot += len(s) * len(t)
    assert tot <= 100000, 'products %d' % tot


def c_hold(weights, values, cap, k):
    assert 1 <= len(weights) == len(values) <= 50
    assert all(1 <= w <= 400 for w in weights) and all(1 <= v <= 10000 for v in values)
    assert 1 <= cap <= 400 and 1 <= k <= 50


def c_queens(board, q):
    n = len(board)
    assert 1 <= n <= 8 and all(len(r) == n and set(r) <= set('.#') for r in board) and 0 <= q <= n


def c_invoice(amounts, target, k):
    assert 1 <= len(amounts) <= 20 and all(1 <= a <= 1000 for a in amounts)
    assert 1 <= target <= 20000 and 1 <= k <= 20


def c_trace(board, word):
    assert 1 <= len(board) <= 20 and 1 <= len(board[0]) <= 20
    assert all(len(r) == len(board[0]) and low(r) and r for r in board)
    assert 1 <= len(word) <= 60 and low(word)


def c_pieces(text):
    lines = [x.strip() for x in text.split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    q = int(lines[0])
    assert 1 <= q <= 50 and len(lines) == 1 + q, 'q %d lines %d' % (q, len(lines))
    assert all(1 <= len(s) <= 400 and low(s) for s in lines[1:])
    assert sum(len(s) for s in lines[1:]) <= 3000, 'letters %d' % sum(len(s) for s in lines[1:])


def c_three(a, b, c):
    assert all(len(s) <= 50 and low(s) for s in (a, b, c))


def c_desks(skills):
    assert 2 <= len(skills) <= 40 and len(skills) % 2 == 0 and all(1 <= s <= 1000 for s in skills)


def c_merge(a, b, tape):
    assert len(a) <= 300 and len(b) <= 300 and len(tape) <= 600 and low(a) and low(b) and low(tape)


def c_cargo(weights, values, cap):
    assert 1 <= len(weights) == len(values) <= 80
    assert all(1 <= w <= 10 ** 9 for w in weights) and all(1 <= v <= 30 for v in values) and 1 <= cap <= 10 ** 9


def c_smooth(sizes, d):
    assert 1 <= len(sizes) <= 11 and all(1 <= s <= 1000 for s in sizes) and 0 <= d <= 1000


PROSE = {
    'ci-drop-point-routes': c_drop, 'ci-spaced-picks': c_picks, 'ci-long-mirrors': c_mirrors,
    'ci-tolerant-common': c_tol, 'ci-priced-edits': c_edits, 'ci-hold-limit': c_hold,
    'ci-pillar-queens': c_queens, 'ci-invoice-matches': c_invoice, 'ci-trace-count': c_trace,
    'ci-mirror-pieces': c_pieces, 'ci-three-feed-common': c_three, 'ci-even-desks': c_desks,
    'ci-merged-tape': c_merge, 'ci-light-cargo': c_cargo, 'ci-smooth-orderings': c_smooth,
}


def obj_ok(c, v):
    """A small reader of the constraints object, independent of the validator's."""
    t = c.get('type')
    if t == 'int':
        assert type(v) is int, 'not int %r' % (v,)
    if t == 'str':
        assert isinstance(v, str)
    if t == 'list':
        assert isinstance(v, list)
    if 'len' in c:
        lo, hi = c['len']
        assert (lo is None or len(v) >= lo) and (hi is None or len(v) <= hi), 'len %d' % len(v)
    if 'range' in c:
        lo, hi = c['range']
        for x in (v if isinstance(v, list) else [v]):
            assert (lo is None or x >= lo) and (hi is None or x <= hi), 'range %r' % (x,)
    if 'pattern' in c:
        assert re.fullmatch(c['pattern'], v) is not None, 'pattern %r' % v[:20]
    if c.get('distinct'):
        assert len(set(v)) == len(v)
    if 'of' in c:
        for x in v:
            if isinstance(c['of'], dict):
                obj_ok(c['of'], x)
            elif c['of'] == 'int':
                assert type(x) is int


def constraints(drills):
    calls = bad = 0
    for did, j in drills.items():
        fn = j['fn']
        params = re.search(r'def %s\((.*?)\)' % fn, j['starter']).group(1).replace(' ', '').split(',')
        objs = [c for c in j['constraints'] if isinstance(c, dict)]
        assert sorted(o['arg'] for o in objs) == sorted(params), (did, 'objects do not cover the parameters')
        seen = []

        def rec(*a):
            seen.append(a)
            return 0
        for kind in ('examples', 'tests'):
            for i, t in enumerate(j[kind]):
                seen.clear()
                try:
                    eval(t['call'], {fn: rec})
                except Exception:
                    pass
                assert len(seen) == 1, (did, kind, i, 'call not read')
                calls += 1
                try:
                    PROSE[did](*seen[0])
                    for o in objs:
                        obj_ok(o, seen[0][params.index(o['arg'])])
                except AssertionError as e:
                    bad += 1
                    print('OUTSIDE', did, kind, i, e)
    print('constraints: %d calls read, %d outside' % (calls, bad))


# ------------------------------------------------------------ brute forces
def b_drop(grid):
    R, C = len(grid), len(grid[0])

    def go(r, c, seen):
        if r >= R or c >= C or grid[r][c] == '#':
            return 0
        seen = seen or grid[r][c] == 'P'
        if (r, c) == (R - 1, C - 1):
            return int(seen)
        return go(r + 1, c, seen) + go(r, c + 1, seen)
    return go(0, 0, False) % MOD


def b_picks(values, gap):
    out = []
    for r in range(1, len(values) + 1):
        for p in combinations(values, r):
            if all(abs(x - y) >= gap for x, y in combinations(p, 2)):
                out.append(sorted(p))
    return sorted(out)


def b_mirrors(tape, k):
    n = len(tape)
    return sum(1 for i in range(n) for j in range(i + 1, n + 1) if j - i >= k and tape[i:j] == tape[i:j][::-1])


def b_tol(a, b, tol):
    best = 0
    for r in range(1, min(len(a), len(b)) + 1):
        for ia in combinations(range(len(a)), r):
            for ib in combinations(range(len(b)), r):
                if all(abs(a[x] - b[y]) <= tol for x, y in zip(ia, ib)):
                    best = r
    return best


def b_edits(text):
    import heapq
    tok = text.split()
    ins, dele, sub = map(int, tok[:3])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        alpha = sorted(set(t))
        cap = max(len(s), len(t))
        dist = {s: 0}
        heap = [(0, s)]
        while heap:
            d, u = heapq.heappop(heap)
            if u == t:
                out.append(str(d))
                break
            if d > dist[u]:
                continue
            nxt = []
            for i in range(len(u)):
                nxt.append((dele, u[:i] + u[i + 1:]))
                for ch in alpha:
                    if ch != u[i]:
                        nxt.append((sub, u[:i] + ch + u[i + 1:]))
            if len(u) < cap:
                for i in range(len(u) + 1):
                    for ch in alpha:
                        nxt.append((ins, u[:i] + ch + u[i:]))
            for w, v in nxt:
                if d + w < dist.get(v, 1 << 60):
                    dist[v] = d + w
                    heapq.heappush(heap, (d + w, v))
    return '\n'.join(out)


def b_hold(weights, values, cap, k):
    best = 0
    n = len(weights)
    for r in range(1, min(k, n) + 1):
        for p in combinations(range(n), r):
            if sum(weights[i] for i in p) <= cap:
                best = max(best, sum(values[i] for i in p))
    return best


def b_queens(board, q):
    n = len(board)
    free = [(r, c) for r in range(n) for c in range(n) if board[r][c] == '.']
    return sum(1 for pick in combinations(free, q)
               if all(a != c and b != e and abs(a - c) != abs(b - e) for (a, b), (c, e) in combinations(pick, 2)))


def b_invoice(amounts, target, k):
    seen = set()
    for r in range(1, min(k, len(amounts)) + 1):
        for c in combinations(amounts, r):
            if sum(c) == target:
                seen.add(tuple(sorted(c)))
    return sorted(list(t) for t in seen)


def b_trace(board, word):
    R, C = len(board), len(board[0])

    def walk(i, j, k):
        if k == len(word) - 1:
            return 1
        return sum(walk(a, b, k + 1) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                   if 0 <= a < R and 0 <= b < C and board[a][b] == word[k + 1])
    return sum(walk(i, j, 0) for i in range(R) for j in range(C) if board[i][j] == word[0]) % MOD


def b_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        best = n
        for mask in range(1 << (n - 1)):
            cuts = [0] + [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
            if len(cuts) - 1 < best and all(s[x:y] == s[x:y][::-1] for x, y in zip(cuts, cuts[1:])):
                best = len(cuts) - 1
        out.append(str(best))
    return '\n'.join(out)


def is_sub(x, s):
    it = iter(s)
    return all(ch in it for ch in x)


def b_three(a, b, c):
    best = 0
    for mask in range(1 << len(a)):
        x = ''.join(a[i] for i in range(len(a)) if mask >> i & 1)
        if len(x) > best and is_sub(x, b) and is_sub(x, c):
            best = len(x)
    return best


def b_desks(skills):
    total = sum(skills)
    return min(abs(total - 2 * sum(p)) for p in combinations(skills, len(skills) // 2))


def b_merge(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    n = len(tape)
    count = 0
    for pos in combinations(range(n), len(a)):
        ps = set(pos)
        if ''.join(tape[i] for i in pos) == a and ''.join(tape[i] for i in range(n) if i not in ps) == b:
            count += 1
    return count % MOD


def b_cargo(weights, values, cap):
    best = 0
    n = len(weights)
    for mask in range(1 << n):
        if sum(weights[i] for i in range(n) if mask >> i & 1) <= cap:
            best = max(best, sum(values[i] for i in range(n) if mask >> i & 1))
    return best


def b_smooth(sizes, d):
    return sum(1 for p in set(permutations(sizes)) if all(abs(x - y) <= d for x, y in zip(p, p[1:])))


R = random.Random(20261111)


def rs(alpha, lo, hi):
    return ''.join(R.choice(alpha) for _ in range(R.randint(lo, hi)))


def g_drop(small):
    r, c = (R.randint(1, 4), R.randint(1, 5)) if small else (R.randint(1, 30), R.randint(1, 30))
    g = [[R.choice('...#P' if R.random() < .7 else '..P') for _ in range(c)] for _ in range(r)]
    if g[0][0] == '#':
        g[0][0] = R.choice('.P')
    if g[-1][-1] == '#':
        g[-1][-1] = R.choice('.P')
    return (['' .join(x) for x in g],)


def g_picks(small):
    n = R.randint(1, 6 if small else 12)
    span = R.choice([10, 30, 1000])
    return (R.sample(range(-span, span + 1), n), R.choice([1, 2, 3, 5, 8, span, 2 * span]))


def g_mirrors(small):
    s = rs(R.choice(['ab', 'a', 'abc']), 1, 9 if small else 120)
    return (s, R.choice([1, 2, 3, 4, len(s), len(s) + 1, 1000]))


def g_tol(small):
    hi = 5 if small else 40
    span = R.choice([4, 12, 1000000])
    return ([R.randint(0, span) for _ in range(R.randint(0, hi))], [R.randint(0, span) for _ in range(R.randint(0, hi))],
            R.choice([0, 1, 2, 3, span]))


def g_edits(small):
    q = R.randint(1, 3)
    hi = 4 if small else 40
    lines = ['%d %d %d' % tuple(R.choice([1, 2, 3, 5, 9, 100]) for _ in range(3)), str(q)]
    for _ in range(q):
        lines.append(rs('ab' if small else 'abc', 1, hi) + ' ' + rs('ab' if small else 'abc', 1, hi))
    return ('\n'.join(lines) + R.choice(['', '\n', '\n\n']),)


def g_hold(small):
    n = R.randint(1, 8 if small else 50)
    wmax = R.choice([5, 20, 400])
    return ([R.randint(1, wmax) for _ in range(n)], [R.randint(1, R.choice([5, 10000])) for _ in range(n)],
            R.randint(1, R.choice([10, 60, 400])), R.randint(1, R.choice([2, 4, 50])))


def g_queens(small):
    n = R.randint(1, 4 if small else 7)
    p = R.choice([0, .15, .4])
    return ([''.join('#' if R.random() < p else '.' for _ in range(n)) for _ in range(n)], R.randint(0, n))


def g_invoice(small):
    n = R.randint(1, 8 if small else 18)
    hi = R.choice([4, 8, 30])
    return ([R.randint(1, hi) for _ in range(n)], R.randint(1, hi * 3), R.randint(1, R.choice([2, 3, n])))


def g_trace(small):
    r, c = (R.randint(1, 3), R.randint(1, 3)) if small else (R.randint(1, 20), R.randint(1, 20))
    alpha = R.choice(['a', 'ab', 'abc'])
    return ([rs(alpha, c, c) for _ in range(r)], rs(alpha, 1, 7 if small else 60))


def g_pieces(small):
    q = R.randint(1, 3)
    return ('%d\n' % q + '\n'.join(rs(R.choice(['ab', 'abc', 'a']), 1, 11 if small else 200) for _ in range(q)) + '\n',)


def g_three(small):
    hi = 9 if small else 50
    alpha = R.choice(['ab', 'abc', 'abcd'])
    return (rs(alpha, 0, hi), rs(alpha, 0, hi), rs(alpha, 0, hi))


def g_desks(small):
    n = 2 * R.randint(1, 6 if small else 20)
    return ([R.randint(1, R.choice([5, 30, 1000])) for _ in range(n)],)


def g_merge(small):
    hi = 6 if small else 60
    alpha = R.choice(['a', 'ab', 'abc'])
    a, b = rs(alpha, 0, hi), rs(alpha, 0, hi)
    if R.random() < .2:
        return (a, b, rs(alpha, 0, 2 * hi))
    ia, ib, t = 0, 0, []
    while ia < len(a) or ib < len(b):
        if ib == len(b) or (ia < len(a) and R.random() < .5):
            t.append(a[ia])
            ia += 1
        else:
            t.append(b[ib])
            ib += 1
    t = ''.join(t)
    if R.random() < .15 and t:
        i = R.randrange(len(t))
        t = t[:i] + R.choice(alpha) + t[i + 1:]
    return (a, b, t)


def g_cargo(small):
    n = R.randint(1, 10 if small else 80)
    wmax = R.choice([10, 1000, 10 ** 9])
    ws = [R.randint(1, wmax) for _ in range(n)]
    return (ws, [R.randint(1, R.choice([3, 30])) for _ in range(n)], min(10 ** 9, R.randint(1, max(1, sum(ws)))))


def g_smooth(small):
    n = R.randint(1, 7 if small else 11)
    hi = R.choice([3, 6, 20, 1000])
    return ([R.randint(1, hi) for _ in range(n)], R.choice([0, 1, 2, 3, hi]))


RAND = {
    'ci-drop-point-routes': (g_drop, b_drop), 'ci-spaced-picks': (g_picks, b_picks), 'ci-long-mirrors': (g_mirrors, b_mirrors),
    'ci-tolerant-common': (g_tol, b_tol), 'ci-priced-edits': (g_edits, b_edits), 'ci-hold-limit': (g_hold, b_hold),
    'ci-pillar-queens': (g_queens, b_queens), 'ci-invoice-matches': (g_invoice, b_invoice), 'ci-trace-count': (g_trace, b_trace),
    'ci-mirror-pieces': (g_pieces, b_pieces), 'ci-three-feed-common': (g_three, b_three), 'ci-even-desks': (g_desks, b_desks),
    'ci-merged-tape': (g_merge, b_merge), 'ci-light-cargo': (g_cargo, b_cargo), 'ci-smooth-orderings': (g_smooth, b_smooth),
}


def rand(drills, n_small=400, n_big=600):
    mine = {}
    exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
    total = bad = 0
    for did, j in drills.items():
        env = {}
        exec(j['solution'], env)
        model, me = env[j['fn']], mine[j['fn']]
        gen, brute = RAND[did]
        for i in range(n_small + n_big):
            small = i < n_small
            args = gen(small)
            PROSE[did](*args)
            a = model(*args)
            b = me(*args)
            c = brute(*args) if small else a
            total += 1
            if not (a == b == c):
                bad += 1
                if bad < 12:
                    print('DISAGREE', did, repr(args)[:300], a, b, c)
        print('%-24s %d small with brute force, %d larger, model = mine' % (did, n_small, n_big))
    print('random: %d inputs, %d disagreements' % (total, bad))


# ------------------------------------------------------------ planted
def _first_fail(src, drill, q):
    env = {}
    try:
        exec(src, env)
    except Exception as e:  # noqa
        q.put('load error %r' % e)
        return
    for i, t in enumerate(drill['tests']):
        t0 = time.time()
        try:
            got = eval(t['call'], env)
            want = eval(t['expect'], env)
            if got != want:
                q.put('tests[%d] wrong value: got %s, want %s' % (i, repr(got)[:60], repr(want)[:60]))
                return
        except BaseException as e:  # noqa
            q.put('tests[%d] %s' % (i, type(e).__name__))
            return
        q.put(('progress', i, time.time() - t0))
    q.put('PASSES ALL')


def planted(drills, limit=12):
    for did, j in drills.items():
        for n, p in enumerate(j['planted']):
            q = mp.Queue()
            pr = mp.Process(target=_first_fail, args=(p['code'], j, q))
            pr.start()
            pr.join(limit)
            last = -1
            res = None
            while not q.empty():
                m = q.get()
                if isinstance(m, tuple):
                    last = m[1]
                else:
                    res = m
            if pr.is_alive():
                pr.terminate()
                pr.join()
                res = 'still running at %d s inside tests[%d]' % (limit, last + 1)
            print('%-24s planted[%d] %s | %s' % (did, n, res, p['slip'][:70]))


if __name__ == '__main__':
    drills = load(sys.argv[1])
    what = sys.argv[2:] or ['constraints', 'random', 'planted']
    if 'constraints' in what:
        constraints(drills)
    if 'random' in what:
        rand(drills)
    if 'planted' in what:
        planted(drills)
