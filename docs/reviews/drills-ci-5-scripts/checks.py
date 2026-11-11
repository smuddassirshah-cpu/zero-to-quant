"""Three checks on pack 5.
usage: checks.py <drills dir> [constraints] [random] [planted]

constraints: evaluates every example and hidden call with the function replaced
  by a recorder, then tests the real arguments against the PROSE constraints
  (sizes, ranges, 'a cell of the grid', 'different towns', 'S once', ...),
  including the generated calls the validator skips.
random: the model solution against mine.py on random inputs inside the
  constraints, built to hit ties, self rules, repeats, walls, lone nodes.
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

HERE = os.path.dirname(os.path.abspath(__file__))


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == 'pack-5':
            out[j['id']] = j
    return out


# ------------------------------------------------------------ constraints
def grid_ok(g, maxr, maxc, chars):
    assert 1 <= len(g) <= maxr, 'rows %d' % len(g)
    w = len(g[0])
    assert 1 <= w <= maxc, 'cols %d' % w
    for row in g:
        assert len(row) == w, 'ragged'
        assert set(row) <= set(chars), 'chars %r' % (set(row) - set(chars))


def edges_ok(n, es, maxm, lo, hi, selfok=False, cost=None):
    assert len(es) <= maxm, 'edges %d' % len(es)
    for e in es:
        a, b = e[0], e[1]
        assert lo <= a <= hi and lo <= b <= hi, 'endpoint %r' % (e,)
        assert selfok or a != b, 'self %r' % (e,)
        if cost:
            assert cost[0] <= e[2] <= cost[1], 'cost %r' % (e,)


def c_cheapest(n, roads, src, dst):
    assert 1 <= n <= 2000
    edges_ok(n, roads, 10000, 0, n - 1, cost=(1, 1000))
    assert 0 <= src < n and 0 <= dst < n


def c_checkpoint(text):
    lines = [x.strip() for x in text.split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    r, c = map(int, lines[0].split())
    assert 1 <= r <= 300 and 1 <= c <= 300
    assert len(lines) == r + 1, 'row count'
    for row in lines[1:]:
        assert len(row) == c and set(row) <= set('#.SCE'), 'row %r' % row[:20]
    body = ''.join(lines[1:])
    assert body.count('S') == body.count('C') == body.count('E') == 1


def c_ferry(text):
    v = list(map(int, text.split()))
    n, m = v[0], v[1]
    assert 1 <= n <= 50000 and 0 <= m <= 100000
    assert len(v) == 2 + 4 * m, 'token count'
    for k in range(m):
        a, b, t, p = v[2 + 4 * k:6 + 4 * k]
        assert 1 <= a <= n and 1 <= b <= n and 1 <= t <= 1000 and 1 <= p <= 1000, (a, b, t, p)
    lines = [x for x in text.split('\n') if x.strip()]
    assert len(lines) == m + 1, 'one crossing a line'


def c_cycle(n, rules):
    assert 1 <= n <= 20000
    edges_ok(n, rules, 20000, 0, n - 1, selfok=True)


def c_flood(heights, r, c):
    assert 1 <= len(heights) <= 400 and 1 <= len(heights[0]) <= 400
    for row in heights:
        assert len(row) == len(heights[0])
        assert all(type(x) is int and 0 <= x <= 10 ** 6 for x in row)
    assert 0 <= r < len(heights) and 0 <= c < len(heights[0])


def c_coupon(n, roads, src, dst):
    assert 1 <= n <= 10000
    edges_ok(n, roads, 30000, 0, n - 1, cost=(1, 10 ** 6))
    assert 0 <= src < n and 0 <= dst < n


def c_shapes(grid):
    grid_ok(grid, 300, 300, '#.')


def c_line(pairs):
    assert 1 <= len(pairs) <= 100000
    deg = {}
    seen = set()
    for x, y in pairs:
        assert re.fullmatch('[A-Z][a-z0-9]*', x) and re.fullmatch('[A-Z][a-z0-9]*', y), (x, y)
        assert x != y
        k = (min(x, y), max(x, y))
        assert k not in seen, 'pair twice'
        seen.add(k)
        deg[x] = deg.get(x, 0) + 1
        deg[y] = deg.get(y, 0) + 1
    assert sorted(deg.values()) == [1, 1] + [2] * (len(deg) - 2), 'not a path'
    assert len(deg) == len(pairs) + 1, 'not one line'


def c_cables(n, cables):
    assert 1 <= n <= 200000
    edges_ok(n, cables, 250000, 0, n - 1)


def c_depot(grid):
    grid_ok(grid, 300, 300, '#.AB')


def c_land(rows, cols, fills):
    assert 1 <= rows <= 1000 and 1 <= cols <= 1000 and len(fills) <= 100000
    for r, c in fills:
        assert 0 <= r < rows and 0 <= c < cols, (r, c)


def c_walk(grid):
    grid_ok(grid, 250, 250, '#.G')
    assert any('G' in row for row in grid), 'no camera'
    assert grid[0][0] != '#' and grid[-1][-1] != '#'


def c_jobs(n, rules):
    assert 1 <= n <= 200000
    edges_ok(n, rules, 250000, 0, n - 1, selfok=True)


def c_rota(n, clashes):
    assert 1 <= n <= 200000
    edges_ok(n, clashes, 250000, 0, n - 1)


def c_break(grid):
    grid_ok(grid, 300, 300, '#.SE')
    body = ''.join(grid)
    assert body.count('S') == 1 and body.count('E') == 1


CHECK = {
    'ci-cheapest-route': c_cheapest, 'ci-checkpoint-route': c_checkpoint, 'ci-ferry-timetable': c_ferry,
    'ci-first-circular-rule': c_cycle, 'ci-flood-reach': c_flood, 'ci-half-fare-route': c_coupon,
    'ci-island-shapes': c_shapes, 'ci-line-from-pairs': c_line, 'ci-loop-cables': c_cables,
    'ci-nearest-depot': c_depot, 'ci-reclaimed-land': c_land, 'ci-safest-walk': c_walk,
    'ci-stuck-jobs': c_jobs, 'ci-two-shift-rota': c_rota, 'ci-wall-break-route': c_break,
}


def fn_name(j):
    return re.search(r'def (\w+)\(', j['starter']).group(1)


def do_constraints(drills):
    bad = 0
    n = 0
    for did, j in drills.items():
        rec = []
        name = fn_name(j)

        class Shape(list):
            pass

        def recorder(*a, **k):
            rec.append(a)
            raise RuntimeError('recorded')
        env = {name: recorder}
        for kind, cases in (('ex', j['examples']), ('t', j['tests'])):
            for i, t in enumerate(cases):
                rec.clear()
                try:
                    eval(t['call'], env)
                except RuntimeError:
                    pass
                n += 1
                try:
                    CHECK[did](*rec[0])
                except AssertionError as e:
                    bad += 1
                    print('OUTSIDE', did, kind, i, e)
    print('constraints: %d calls read, %d outside the prose constraints' % (n, bad))


# ------------------------------------------------------------ random
def rnd_graph(rng, n, m, selfok=False, cost=None, base=0):
    es = []
    for _ in range(m):
        a = rng.randrange(n) + base
        b = rng.randrange(n) + base
        if a == b and not selfok:
            continue
        e = [a, b]
        if cost:
            e.append(rng.choice(cost))
        es.append(e)
        if rng.random() < 0.15:
            es.append(list(e) if rng.random() < 0.5 else ([e[1], e[0]] + e[2:]))
    return es


def rnd_grid(rng, chars, weights, one=(), maxd=7):
    r, c = rng.randint(1, maxd), rng.randint(1, maxd)
    while r * c < len(one):
        c += 1
    g = [[rng.choices(chars, weights)[0] for _ in range(c)] for _ in range(r)]
    cells = rng.sample([(i, j) for i in range(r) for j in range(c)], len(one))
    for ch, (i, j) in zip(one, cells):
        g[i][j] = ch
    return [''.join(row) for row in g]


def gen(did, rng):
    if did == 'ci-cheapest-route':
        n = rng.randint(1, 8)
        return (n, rnd_graph(rng, n, rng.randint(0, 14), cost=[1, 1, 2, 2, 3]), rng.randrange(n), rng.randrange(n))
    if did == 'ci-checkpoint-route':
        g = rnd_grid(rng, '.#', [3, 1], one='SCE')
        pad = lambda s: ' ' * rng.randint(0, 2) + s + ' ' * rng.randint(0, 2)
        return (pad('%d %d' % (len(g), len(g[0]))) + '\n' + '\n'.join(pad(x) for x in g) + '\n' * rng.randint(0, 3),)
    if did == 'ci-ferry-timetable':
        n = rng.randint(1, 8)
        es = rnd_graph(rng, n, rng.randint(0, 14), selfok=True, base=1)
        return ('%d %d\n' % (n, len(es)) + ''.join('%d %d %d %d\n' % (a, b, rng.randint(1, 9), rng.randint(1, 9)) for a, b in es),)
    if did in ('ci-first-circular-rule', 'ci-stuck-jobs'):
        n = rng.randint(1, 9)
        es = rnd_graph(rng, n, rng.randint(0, 12), selfok=rng.random() < 0.4)
        if rng.random() < 0.5:
            es = [[min(a, b), max(a, b)] if rng.random() < 0.9 else [a, b] for a, b in es]
        return (n, es)
    if did == 'ci-flood-reach':
        r, c = rng.randint(1, 6), rng.randint(1, 6)
        return ([[rng.randint(0, 4) for _ in range(c)] for _ in range(r)], rng.randrange(r), rng.randrange(c))
    if did == 'ci-half-fare-route':
        n = rng.randint(1, 8)
        return (n, rnd_graph(rng, n, rng.randint(0, 14), cost=[1, 2, 3, 5, 7, 20, 41]), rng.randrange(n), rng.randrange(n))
    if did == 'ci-island-shapes':
        return (rnd_grid(rng, '#.', [1, 1], maxd=8),)
    if did == 'ci-line-from-pairs':
        k = rng.randint(2, 9)
        names = rng.sample(['A', 'Ab', 'B', 'S1', 'S10', 'S2', 'S20', 'Zed', 'Ze', 'M9', 'M', 'Ma', 'Q7'], k)
        ps = [[names[i], names[i + 1]] if rng.random() < 0.5 else [names[i + 1], names[i]] for i in range(k - 1)]
        rng.shuffle(ps)
        return (ps,)
    if did in ('ci-loop-cables', 'ci-two-shift-rota'):
        n = rng.randint(1, 9)
        return (n, rnd_graph(rng, n, rng.randint(0, 11)))
    if did == 'ci-nearest-depot':
        return (rnd_grid(rng, '.#AB', [8, 3, 1, 1]),)
    if did == 'ci-reclaimed-land':
        r, c = rng.randint(1, 5), rng.randint(1, 5)
        return (r, c, [[rng.randrange(r), rng.randrange(c)] for _ in range(rng.randint(0, 2 * r * c))])
    if did == 'ci-safest-walk':
        while True:
            g = rnd_grid(rng, '.#G', [10, 4, 1])
            if any('G' in x for x in g) and g[0][0] != '#' and g[-1][-1] != '#':
                return (g,)
    if did == 'ci-wall-break-route':
        return (rnd_grid(rng, '.#', [1, 1], one='SE'),)
    raise KeyError(did)


def do_random(drills, trials=4000):
    mine = {}
    exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
    total = 0
    for did, j in drills.items():
        env = {}
        exec(j['solution'], env)
        name = fn_name(j)
        rng = random.Random(505 + len(did))
        diff = 0
        for _ in range(trials):
            args = gen(did, rng)
            CHECK[did](*args)
            a = env[name](*json.loads(json.dumps(args)))
            b = mine[name](*json.loads(json.dumps(args)))
            if a != b:
                diff += 1
                if diff <= 2:
                    print('DIFFER', did, args, a, b)
        total += diff
        print('%-26s %d random inputs, %d disagreements' % (did, trials, diff))
    print('random: %d disagreements in all' % total)


# ------------------------------------------------------------ planted
def _first_fail(src, drill, q):
    env = {}
    exec(src, env)
    for i, t in enumerate(drill['tests']):
        t0 = time.time()
        try:
            got = eval(t['call'], env)
            if got != eval(t['expect'], env):
                q.put('test %d wrong value %s (%.1f s)' % (i, repr(got)[:40], time.time() - t0))
                return
        except BaseException as e:  # noqa
            q.put('test %d %s' % (i, type(e).__name__))
            return
    q.put('PASSES ALL')


def do_planted(drills, limit=12):
    for did, j in drills.items():
        for k, p in enumerate(j['planted']):
            q = mp.Queue()
            pr = mp.Process(target=_first_fail, args=(p['code'], j, q))
            pr.start()
            pr.join(limit)
            if pr.is_alive():
                pr.terminate()
                res = 'still running at %d s' % limit
            else:
                res = q.get(timeout=2)
            print('%-24s planted[%d] %-34s | %s' % (did, k, res, p['slip'][:90]))


if __name__ == '__main__':
    drills = load(sys.argv[1])
    what = sys.argv[2:] or ['constraints', 'random', 'planted']
    if 'constraints' in what:
        do_constraints(drills)
    if 'random' in what:
        do_random(drills)
    if 'planted' in what:
        do_planted(drills)
