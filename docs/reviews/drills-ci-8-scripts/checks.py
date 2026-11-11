"""Second reader's checks on pack 8.
usage: checks.py <drills dir> random [seed]   model v mine v brute force on random inputs
       checks.py <drills dir> constraints      real arguments of every call against prose and objects
"""
import glob
import itertools
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'ci-*.json'))):
        j = json.load(open(f))
        if (j.get('tags') or [''])[0] == 'pack-8':
            out[j['id']] = j
    return out


# ---------------------------------------------------------------- brute forces
def b_merge_with_grace(sessions, grace):
    n = len(sessions)
    par = list(range(n))

    def find(x):
        while par[x] != x:
            x = par[x]
        return x
    for i in range(n):
        for j in range(n):
            a, b = sessions[i], sessions[j]
            if a[0] <= b[0] <= a[1] + grace:
                par[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(sessions[i])
    return sorted([min(s[0] for s in g), max(s[1] for s in g), len(g)] for g in groups.values())


def b_run_days(tasks, rest):
    last = {}
    day = 0
    out = []
    for m in tasks:
        day += 1
        while m in last and day - last[m] - 1 < rest.get(m, 0):
            day += 1
        last[m] = day
        out.append(day)
    return out


def b_solve_robot_floor(text):
    lines = [ln.strip() for ln in text.strip().split('\n')]
    r, c = map(int, lines[0].split())
    grid = lines[1:1 + r]
    cmds = ' '.join(lines[1 + r:]).split()
    pos = [complex(j, i) for i in range(r) for j in range(c) if grid[i][j] == 'R'][0]
    d = -1j
    seen = {pos}
    for t in cmds:
        if t == 'L':
            d *= -1j
        elif t == 'R':
            d *= 1j
        else:
            for _ in range(int(t[1:])):
                q = pos + d
                if not (0 <= q.real < c and 0 <= q.imag < r) or grid[int(q.imag)][int(q.real)] == '#':
                    break
                pos = q
                seen.add(pos)
    return '%d %d %s %d' % (pos.imag, pos.real, {-1j: 'N', 1: 'E', 1j: 'S', -1: 'W'}[d], len(seen))


def b_fewest_checks(jobs):
    if not jobs:
        return 0
    lo = min(j[0] for j in jobs)
    hi = max(j[1] for j in jobs)
    mins = list(range(lo, hi + 1))
    for size in range(len(mins) + 1):
        for pick in itertools.combinations(mins, size):
            if all(sum(1 for m in pick if s <= m <= e) >= need for s, e, need in jobs):
                return size


def b_first_fit(bookings, start, length):
    busy = set()
    for s, e in bookings:
        busy.update(range(s, e))
    slot = start
    while any(m in busy for m in range(slot, slot + length)):
        slot += 1
    busy.update(range(slot, slot + length))
    merged = []
    for m in sorted(busy):
        if merged and merged[-1][1] == m:
            merged[-1][1] = m + 1
        else:
            merged.append([m, m + 1])
    return [slot, merged]


def b_one_bit_pairs(codes):
    return sum(1 for i in range(len(codes)) for j in range(i) if bin(codes[i] ^ codes[j]).count('1') == 1)


def b_turn_rings(grid, k):
    R, C = len(grid), len(grid[0])
    g = [row[:] for row in grid]

    def ring_of(i, j):
        return min(i, j, R - 1 - i, C - 1 - j)

    def nxt(i, j, t):          # next cell clockwise on ring t
        top, left, bot, right = t, t, R - 1 - t, C - 1 - t
        if i == top and j < right:
            return i, j + 1
        if j == right and i < bot:
            return i + 1, j
        if i == bot and j > left:
            return i, j - 1
        return i - 1, j
    for _ in range(k):
        new = [row[:] for row in g]
        for i in range(R):
            for j in range(C):
                t = ring_of(i, j)
                if R - 2 * t < 2 or C - 2 * t < 2:
                    continue
                a, b = nxt(i, j, t)
                if t % 2 == 0:
                    new[a][b] = g[i][j]
                else:
                    new[i][j] = g[a][b]
        g = new
    return g


def b_fewest_switches(switches, target):
    best = None
    n = len(switches)
    L = len(target)
    for mask in range(1 << n):
        lamps = [0] * L
        pick = [i for i in range(n) if mask >> i & 1]
        for i in pick:
            for p in range(L):
                if switches[i][p] == '1':
                    lamps[p] ^= 1
        if ''.join(map(str, lamps)) == target:
            key = (len(pick), pick)
            if best is None or key < best:
                best = key
    return None if best is None else best[1]


def b_count_k_bits(queries):
    return [sum(1 for x in range(lo, hi + 1) if bin(x).count('1') == k) for lo, hi, k in queries]


def b_loop_starts(fuel, burn):
    n = len(fuel)
    out = []
    for s in range(n):
        tank = 0
        for d in range(n):
            i = (s + d) % n
            tank += fuel[i] - burn[i]
            if tank < 0:
                break
        else:
            out.append(s)
    return out


def b_ring_bonuses(scores):
    n = len(scores)
    tok = [1] * n
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in ((i - 1) % n, (i + 1) % n):
                if scores[i] > scores[j] and tok[i] <= tok[j]:
                    tok[i] = tok[j] + 1
                    changed = True
    return sum(tok)


def b_room_numbers(meetings, clean):
    free_at = []
    out = [None] * len(meetings)
    for i in sorted(range(len(meetings)), key=lambda i: meetings[i][0]):
        s, e = meetings[i]
        for r, f in enumerate(free_at):
            if f <= s:
                free_at[r] = e + clean
                out[i] = r
                break
        else:
            free_at.append(e + clean)
            out[i] = len(free_at) - 1
    return out


def b_spiral_cells(rows, cols, ks):
    seen = [[False] * cols for _ in range(rows)]
    order = []
    i = j = 0
    di, dj = 0, 1
    for _ in range(rows * cols):
        order.append([i, j])
        seen[i][j] = True
        a, b = i + di, j + dj
        if not (0 <= a < rows and 0 <= b < cols) or seen[a][b]:
            di, dj = dj, -di
            a, b = i + di, j + dj
        i, j = a, b
    return [order[k - 1] for k in ks]


def b_fewest_hops(stones, lo, hi):
    n = len(stones)
    INF = 10 ** 9
    dp = [INF] * n
    dp[0] = 0
    for j in range(1, n):
        if stones[j] == '.':
            for i in range(max(0, j - hi), j - lo + 1):
                if dp[i] + 1 < dp[j]:
                    dp[j] = dp[i] + 1
    return dp[-1] if dp[-1] < INF else -1


def b_solve_stop_cascade(text, rng=random.Random(5)):
    lines = [ln.split() for ln in text.strip().split('\n') if ln.strip()]
    n = int(lines[0][0])
    book, stops = [], []
    st = {'last': None, 'tot': 0}

    def buy(q):
        while q and book:
            i = min(range(len(book)), key=lambda i: book[i][0])
            take = min(q, book[i][1])
            q -= take
            book[i][1] -= take
            st['tot'] += take
            st['last'] = book[i][0]
            if not book[i][1]:
                book.pop(i)
    out = []
    for ev in lines[1:n + 1]:
        if ev[0] == 'S':
            book.append([int(ev[1]), int(ev[2])])
        elif ev[0] == 'B':
            buy(int(ev[1]))
        else:
            stops.append((int(ev[1]), int(ev[2])))
        while True:
            ready = [i for i, s in enumerate(stops) if st['last'] is not None and s[0] <= st['last']]
            if not ready:
                break
            buy(stops.pop(rng.choice(ready))[1])    # any ready stop, at random
        out.append('- 0' if st['last'] is None else '%d %d' % (st['last'], st['tot']))
    return '\n'.join(out)


# ---------------------------------------------------------------- generators
def gens(rng, big):
    """argument tuples per fn; big = inputs too large for the brute force"""
    def g_grace():
        n = rng.randint(0, 300 if big else 7)
        top = 3000 if big else 25
        ss = []
        for _ in range(n):
            a = rng.randint(0, top)
            ss.append([a, a + rng.choice([0, 0, 1, 2, 3, rng.randint(0, 12)])])
        return (ss, rng.choice([0, 1, 2, 3, 5]))

    def g_rest():
        names = ['a', 'b', 'c', 'd'][:rng.randint(1, 4)]
        n = rng.randint(0, 300 if big else 9)
        rest = {m: rng.randint(0, 6) for m in names if rng.random() < 0.7}
        if rng.random() < 0.3:
            rest['zz'] = 4
        return ([rng.choice(names) for _ in range(n)], rest)

    def g_robot():
        r, c = rng.randint(1, 30 if big else 5), rng.randint(1, 30 if big else 5)
        grid = [['#' if rng.random() < 0.2 else '.' for _ in range(c)] for _ in range(r)]
        grid[rng.randrange(r)][rng.randrange(c)] = 'R'
        cmds = [rng.choice(['L', 'R', 'F%d' % rng.randint(1, 12), 'F%d' % rng.randint(1, 3)]) for _ in range(rng.randint(0, 200 if big else 12))]
        sep = rng.choice([' ', '\n', '  '])
        return ('%d %d\n' % (r, c) + '\n'.join(''.join(x) for x in grid) + '\n' + sep.join(cmds) + rng.choice(['', '\n', '\n\n']),)

    def g_checks():
        n = rng.randint(0, 200 if big else 5)
        top = 600 if big else 9
        jobs = []
        for _ in range(n):
            a = rng.randint(0, top)
            b = min(top, a + rng.randint(0, 6))
            jobs.append([a, b, rng.randint(1, min(5 if big else 3, b - a + 1))])
        return (jobs,)

    def g_fit():
        n = rng.randint(0, 300 if big else 6)
        t = rng.randint(0, 3)
        bk = []
        for _ in range(n):
            s = t + rng.choice([0, 0, 1, 2, 3, 5])
            e = s + rng.randint(1, 4)
            bk.append([s, e])
            t = e
        return (bk, rng.randint(0, t + 3), rng.randint(1, 6))

    def g_bit():
        n = rng.randint(0, 2000 if big else 12)
        bits = 30 if big else 4
        pool = [rng.randrange(1 << bits) for _ in range(max(1, n // 3))]
        cs = []
        for _ in range(n):
            x = rng.choice(pool)
            if rng.random() < 0.5:
                x ^= 1 << rng.randrange(30 if big else 4)
            cs.append(x)
        return (cs,)

    def g_rings():
        R, C = rng.randint(1, 7), rng.randint(1, 7)
        return ([[rng.randint(-9, 99) for _ in range(C)] for _ in range(R)], rng.randint(0, 30))

    def g_sw():
        L = rng.randint(1, 6)
        n = rng.randint(0, 8)
        return ([''.join(rng.choice('01') for _ in range(L)) for _ in range(n)], ''.join(rng.choice('01') for _ in range(L)))

    def g_kbits():
        qs = []
        for _ in range(rng.randint(1, 6)):
            top = (1 << 60) - 1 if big else 600
            a, b = sorted((rng.randint(0, top), rng.randint(0, top)))
            if big and rng.random() < 0.3:
                a = b = (1 << rng.randint(1, 59)) - rng.randint(0, 2)
            qs.append([a, b, rng.randint(0, 60 if big else 10)])
        return (qs,)

    def g_loop():
        n = rng.randint(1, 400 if big else 8)
        f = [rng.randint(0, 5) for _ in range(n)]
        b = [rng.randint(0, 5) for _ in range(n)]
        if rng.random() < 0.6:           # make the total zero or just above, so starts exist
            d = sum(f) - sum(b)
            i = rng.randrange(n)
            if d < 0:
                f[i] += -d + rng.randint(0, 1)
            else:
                b[i] += max(0, d - rng.randint(0, 1))
        return (f, b)

    def g_bonus():
        n = rng.randint(1, 500 if big else 9)
        return ([rng.randint(0, rng.choice([2, 4, 50])) for _ in range(n)],)

    def g_rooms():
        n = rng.randint(0, 400 if big else 8)
        top = 300 if big else 12
        ms = []
        for _ in range(n):
            s = rng.randint(0, top)
            ms.append([s, s + rng.randint(1, 8)])
        return (ms, rng.choice([0, 0, 1, 2, 5]))

    def g_spiral():
        if big:
            R, C = rng.randint(1, 10 ** 9), rng.randint(1, 10 ** 9)
            if rng.random() < 0.3:
                R = rng.randint(1, 5)
            return (R, C, [rng.randint(1, R * C) for _ in range(20)])
        R, C = rng.randint(1, 9), rng.randint(1, 9)
        return (R, C, list(range(1, R * C + 1)))

    def g_hops():
        n = rng.randint(1, 600 if big else 14)
        s = ''.join(rng.choice('..~') for _ in range(n))
        s = '.' + s[1:-1] + '.' if n > 1 else '.'
        lo = rng.randint(1, max(1, n // 2))
        return (s, lo, rng.randint(lo, n))

    def g_stop():
        n = rng.randint(1, 300 if big else 10)
        ev = []
        for _ in range(n):
            k = rng.choice('SSBT')
            if k == 'B':
                ev.append('B %d' % rng.randint(1, 4))
            else:
                ev.append('%s %d %d' % (k, rng.randint(1, 8), rng.randint(1, 3)))
        return ('%d\n' % n + '\n'.join(ev) + '\n',)
    return {
        'merge_with_grace': g_grace, 'run_days': g_rest, 'solve_robot_floor': g_robot, 'fewest_checks': g_checks,
        'first_fit': g_fit, 'one_bit_pairs': g_bit, 'turn_rings': g_rings, 'fewest_switches': g_sw,
        'count_k_bits': g_kbits, 'loop_starts': g_loop, 'ring_bonuses': g_bonus, 'room_numbers': g_rooms,
        'spiral_cells': g_spiral, 'fewest_hops': g_hops, 'solve_stop_cascade': g_stop,
    }


def do_random(drills, seed):
    import copy
    mine = {}
    exec(open(os.path.join(HERE, 'mine.py')).read(), mine)
    rng = random.Random(seed)
    tot_small = tot_big = bad = 0
    for did, j in drills.items():
        fn = j['fn']
        env = {}
        exec(j['solution'], env)
        model = env[fn]
        brute = globals()['b_' + fn]
        dis = 0
        small = gens(rng, False)[fn]
        bigg = gens(rng, True)[fn]
        for _ in range(400):
            args = small()
            a = model(*copy.deepcopy(args))
            b = mine[fn](*copy.deepcopy(args))
            c = brute(*copy.deepcopy(args))
            tot_small += 1
            if not (a == b == c):
                dis += 1
                if dis <= 2:
                    print('  DISAGREE small', did, repr(args)[:300], a, b, c)
        for _ in range(600):
            args = bigg()
            a = model(*copy.deepcopy(args))
            b = mine[fn](*copy.deepcopy(args))
            tot_big += 1
            if a != b:
                dis += 1
                if dis <= 2:
                    print('  DISAGREE big', did, repr(args)[:300])
        bad += dis
        print('%-22s 400 small (model, mine, brute) + 600 larger (model, mine): %d disagreements' % (did, dis))
    print('%d small, %d larger, %d disagreements' % (tot_small, tot_big, bad))


# ---------------------------------------------------------------- constraints
def check_obj(val, spec, path, errs):
    if isinstance(spec, str):
        spec = {'type': spec}
    t = spec.get('type')
    if t == 'int':
        if not isinstance(val, int) or isinstance(val, bool):
            errs.append('%s not int' % path)
        elif 'range' in spec and not (spec['range'][0] <= val <= spec['range'][1]):
            errs.append('%s = %r outside %r' % (path, val, spec['range']))
    elif t == 'str':
        if not isinstance(val, str):
            errs.append('%s not str' % path)
            return
        if 'len' in spec and not (spec['len'][0] <= len(val) <= spec['len'][1]):
            errs.append('%s len %d outside %r' % (path, len(val), spec['len']))
        if 'pattern' in spec and not re.fullmatch(spec['pattern'], val):
            errs.append('%s does not match %s' % (path, spec['pattern']))
    elif t == 'list':
        if not isinstance(val, list):
            errs.append('%s not list' % path)
            return
        if 'len' in spec and not (spec['len'][0] <= len(val) <= spec['len'][1]):
            errs.append('%s len %d outside %r' % (path, len(val), spec['len']))
        if 'of' in spec:
            sub = spec['of']
            if isinstance(sub, str):
                sub = {'type': sub}
                if 'range' in spec:
                    sub['range'] = spec['range']
            elif 'range' in spec and sub.get('type') == 'list':
                sub = dict(sub)
                sub.setdefault('range', spec['range'])
            for i, v in enumerate(val):
                check_obj(v, sub, '%s[%d]' % (path, i), errs)
                if errs:
                    return
    elif t == 'dict':
        if not isinstance(val, dict):
            errs.append('%s not dict' % path)
        elif 'len' in spec and not (spec['len'][0] <= len(val) <= spec['len'][1]):
            errs.append('%s len %d outside %r' % (path, len(val), spec['len']))


def prose(did, a):
    """the prose constraints, by hand; returns a list of breaches"""
    e = []
    if did == 'ci-grace-sessions':
        ss, g = a
        if len(ss) > 100000 or not 0 <= g <= 10 ** 9 or any(not (0 <= s <= t <= 10 ** 9) for s, t in ss):
            e.append('grace')
    if did == 'ci-rest-days':
        tasks, rest = a
        if len(tasks) > 100000 or any(not re.fullmatch('[a-z]{1,10}', m) for m in list(tasks) + list(rest)) or any(not 0 <= v <= 10 ** 9 for v in rest.values()):
            e.append('rest')
    if did == 'ci-robot-floor':
        tok = a[0].split()
        r, c = int(tok[0]), int(tok[1])
        rows, cmds = tok[2:2 + r], tok[2 + r:]
        if not (1 <= r <= 200 and 1 <= c <= 200) or len(rows) != r or any(len(x) != c or set(x) - set('.#R') for x in rows) or ''.join(rows).count('R') != 1:
            e.append('grid')
        if len(cmds) > 10000 or any(not re.fullmatch(r'L|R|F([1-9]\d*)', t) for t in cmds) or any(t[0] == 'F' and not 1 <= int(t[1:]) <= 1000 for t in cmds):
            e.append('commands')
    if did == 'ci-double-checks':
        jobs = a[0]
        if len(jobs) > 10000 or any(not (0 <= s <= t <= 10 ** 9 and 1 <= n <= 5 and n <= t - s + 1) for s, t, n in jobs):
            e.append('jobs')
    if did == 'ci-first-fit-slot':
        bk, st, ln = a
        if len(bk) > 100000 or any(not 0 <= s < t <= 10 ** 9 for s, t in bk) or any(bk[i][1] > bk[i + 1][0] for i in range(len(bk) - 1)) or not 0 <= st <= 10 ** 9 or not 1 <= ln <= 10 ** 9:
            e.append('bookings')
    if did == 'ci-one-bit-apart':
        if len(a[0]) > 100000 or any(not 0 <= c < 2 ** 30 for c in a[0]):
            e.append('codes')
    if did == 'ci-ring-turns':
        g, k = a
        if not 1 <= len(g) <= 100 or not 1 <= len(g[0]) <= 100 or len({len(r) for r in g}) != 1 or not 0 <= k <= 10 ** 9:
            e.append('grid')
    if did == 'ci-switch-panel':
        sw, tg = a
        if len(sw) > 14 or not 1 <= len(tg) <= 18 or any(len(s) != len(tg) for s in sw):
            e.append('switches')
    if did == 'ci-k-bit-count':
        if len(a[0]) > 2000 or any(not (0 <= lo <= hi < 2 ** 60 and 0 <= k <= 60) for lo, hi, k in a[0]):
            e.append('queries')
    if did == 'ci-loop-starts':
        f, b = a
        if not 1 <= len(f) <= 100000 or len(f) != len(b) or any(not 0 <= v <= 10 ** 4 for v in f + b):
            e.append('loop')
    if did == 'ci-ring-bonuses':
        if not 1 <= len(a[0]) <= 100000 or any(not 0 <= v <= 10 ** 9 for v in a[0]):
            e.append('scores')
    if did == 'ci-room-numbers':
        ms, cl = a
        if len(ms) > 50000 or any(not 0 <= s < t <= 10 ** 9 for s, t in ms) or not 0 <= cl <= 10 ** 6:
            e.append('rooms')
    if did == 'ci-spiral-cells':
        R, C, ks = a
        if not (1 <= R <= 10 ** 9 and 1 <= C <= 10 ** 9) or not 1 <= len(ks) <= 10000 or any(not 1 <= k <= R * C for k in ks):
            e.append('spiral')
    if did == 'ci-stone-hops':
        s, lo, hi = a
        n = len(s)
        if not 1 <= n <= 100000 or s[0] != '.' or s[-1] != '.' or set(s) - set('.~') or not 1 <= lo <= hi <= n:
            e.append('hops')
    if did == 'ci-stop-cascade':
        lines = [ln.split() for ln in a[0].split('\n') if ln.strip()]
        n = int(lines[0][0])
        if len(lines[0]) != 1 or not 1 <= n <= 60000 or len(lines) != n + 1:
            e.append('n')
        for ev in lines[1:]:
            ok = (ev[0] in 'ST' and len(ev) == 3 and 1 <= int(ev[1]) <= 10 ** 6 and 1 <= int(ev[2]) <= 10 ** 6) or (ev[0] == 'B' and len(ev) == 2 and 1 <= int(ev[1]) <= 10 ** 6)
            if not ok:
                e.append('event %r' % ev)
                break
    return e


def do_constraints(drills):
    calls = bad = 0
    for did, j in drills.items():
        fn = j['fn']
        objs = [c for c in j['constraints'] if isinstance(c, dict)]
        got = []
        env = {fn: lambda *a: got.append(a) or FAKE[fn]}
        for kind in ('examples', 'tests'):
            for i, t in enumerate(j[kind]):
                got.clear()
                try:
                    eval(t['call'], dict(env))
                except Exception:
                    pass
                if not got:
                    print('  no call captured', did, kind, i)
                    bad += 1
                for a in got:
                    calls += 1
                    errs = prose(did, a)
                    names = [o['arg'] for o in objs]
                    import inspect
                    e2 = {}
                    exec(j['solution'], e2)
                    params = list(inspect.signature(e2[fn]).parameters)
                    for o in objs:
                        check_obj(a[params.index(o['arg'])], o, o['arg'], errs)
                    if set(names) != set(params):
                        errs.append('objects for %r, parameters %r' % (names, params))
                    if errs:
                        bad += 1
                        print('  OUTSIDE', did, kind, i, errs[:3])
    print('%d calls read, %d outside the constraints' % (calls, bad))


FAKE = {'merge_with_grace': [[0, 0, 0]] * 3, 'run_days': [0] * 9, 'solve_robot_floor': '0 0 N 1', 'fewest_checks': 0,
        'first_fit': [0, [[0, 1], [1, 2], [2, 3]]], 'one_bit_pairs': 0, 'turn_rings': [[0] * 101 for _ in range(101)],
        'fewest_switches': None, 'count_k_bits': [0] * 2001, 'loop_starts': [0] * 5, 'ring_bonuses': 0,
        'room_numbers': [0] * 5, 'spiral_cells': [[0, 0]] * 5, 'fewest_hops': 0, 'solve_stop_cascade': '- 0'}

if __name__ == '__main__':
    drills = load(sys.argv[1])
    mode = sys.argv[2]
    if mode == 'random':
        do_random(drills, int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    if mode == 'constraints':
        do_constraints(drills)
