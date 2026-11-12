#!/usr/bin/env python3
"""Delta read AC-2, drills ci packs 5 to 8: the three drills whose hidden tests the fix pass of the delta read changed
(commit 3eb5b96): ci-loop-cables (+1), ci-drop-point-routes (+1), ci-first-fit-slot (tests[7] swapped).
Each drill is taken in three states: `orig` (before its pack's first fix pass), `mid` (before 3eb5b96) and `now`.
For each drill:
  - the changed tests are listed, and their inputs are checked against the drill's `constraints` objects
  - model passes every example and test now; starter fails; my own solution (MINE, a different method, written from the
    brief) agrees with every `expect`; a brute force agrees on every small case
  - every candidate is run on all three states: the first reader's (drills-ci-<pack>-scripts/wrong*.py, right.py), the
    delta reader's (weak_78.py), every planted solution of every state, and my extras (EXTRA). Printed:
      REGRESSION   failed in an earlier state, passes every test now          (exit 1)
      PASSES NOW   a wrong candidate that passes now and passed before        (exit 1 unless named right in RIGHT)
      PLANT PASSES a planted solution of the file as it stands passes         (exit 1)
Each candidate runs in its own process, recursion limit 3,000 as the page sets it, 10 s for a whole run (the page allows
5 s in Pyodide for all tests together).
Usage (repo root, venv python): drills_code.py [drill id ...]"""
import glob, itertools, json, multiprocessing as mp, os, random, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(HERE, '..')
D = 'app/content/drills'
DELTA_FIX = '3eb5b96'
FIRST_FIX = {5: 'e2b921a', 6: '399c637', 7: '4160e9d', 8: 'a6b3b02'}
DRILLS = {'ci-loop-cables': 5, 'ci-drop-point-routes': 7, 'ci-first-fit-slot': 8}
LIMIT = 10.0
JOBS = 3  # candidate runs side by side (each is its own process)
# candidates the first reader found to be right after all (labels ending _OK or (right), right.py, wrong3.py)
RIGHT = ('_OK', '(right)', 'R_', 'drop_memo_dict')

MINE = {
 'ci-loop-cables': '''
def loop_cables(n, cables):
    # groups as lists, smaller poured into larger; label per rack
    label = list(range(n))
    members = {}
    out = []
    for pos, pair in enumerate(cables):
        x, y = label[pair[0]], label[pair[1]]
        if x == y:
            out.append(pos)
            continue
        mx = members.pop(x, None) or [x]
        my = members.pop(y, None) or [y]
        if len(mx) < len(my):
            mx, my, x, y = my, mx, y, x
        for r in my:
            label[r] = x
        mx.extend(my)
        members[x] = mx
    return out
''',
 'ci-drop-point-routes': '''
def drop_point_routes(grid):
    # exact whole numbers from the end cell back, two states a cell: drop point met so far or not
    R, C = len(grid), len(grid[0])
    met = [[0] * (C + 1) for _ in range(R + 1)]     # routes to the end from here, a drop point already met
    fresh = [[0] * (C + 1) for _ in range(R + 1)]   # routes to the end from here that still meet one (this cell on)
    for i in range(R - 1, -1, -1):
        for j in range(C - 1, -1, -1):
            if grid[i][j] == '#':
                continue
            if i == R - 1 and j == C - 1:
                met[i][j] = 1
                fresh[i][j] = 1 if grid[i][j] == 'P' else 0
                continue
            met[i][j] = met[i + 1][j] + met[i][j + 1]
            fresh[i][j] = met[i][j] if grid[i][j] == 'P' else fresh[i + 1][j] + fresh[i][j + 1]
    return fresh[0][0] % 1000000007
''',
 'ci-first-fit-slot': '''
from bisect import bisect_left
def first_fit(bookings, start, length):
    starts = [b[0] for b in bookings]
    def free(t):
        k = bisect_left(starts, t + length)       # bookings[:k] begin before the job ends
        return k == 0 or bookings[k - 1][1] <= t  # sorted and disjoint: only the last of them can reach t
    slot = start if free(start) else next(e for s, e in bookings if e > start and free(e))
    spans = sorted([list(b) for b in bookings] + [[slot, slot + length]])
    out = [spans[0]]
    for s, e in spans[1:]:
        if s == out[-1][1] or s < out[-1][1]:
            out[-1] = [out[-1][0], max(e, out[-1][1])]
        else:
            out.append([s, e])
    return [slot, out]
''',
}

EXTRA = {
 'ci-loop-cables': [
  ('x-first-spare-only', 'stops at the first spare cable', 'def loop_cables(n, cables):\n    p = list(range(n))\n    def f(x):\n        while p[x] != x:\n            p[x] = p[p[x]]; x = p[x]\n        return x\n    for i, (a, b) in enumerate(cables):\n        a, b = f(a), f(b)\n        if a == b: return [i]\n        p[a] = b\n    return []\n'),
  ('x-parent-of-b-rack', 'points rack b itself, not its root, at the root of a', 'def loop_cables(n, cables):\n    p = list(range(n))\n    def f(x):\n        while p[x] != x: x = p[x]\n        return x\n    out = []\n    for i, (a, b) in enumerate(cables):\n        if f(a) == f(b): out.append(i)\n        else: p[b] = f(a)\n    return out\n'),
  ('x-degree-two', 'spare when both racks already have a cable', 'def loop_cables(n, cables):\n    seen, out = set(), []\n    for i, (a, b) in enumerate(cables):\n        if a in seen and b in seen: out.append(i)\n        seen.add(a); seen.add(b)\n    return out\n'),
  ('x-one-based-positions', 'positions counted from 1', 'def loop_cables(n, cables):\n    p = list(range(n))\n    def f(x):\n        while p[x] != x:\n            p[x] = p[p[x]]; x = p[x]\n        return x\n    out = []\n    for i, (a, b) in enumerate(cables, 1):\n        a, b = f(a), f(b)\n        if a == b: out.append(i)\n        else: p[a] = b\n    return out\n'),
 ],
 'ci-drop-point-routes': [
  ('x-P-is-wall-complement', 'treats P as a shelf and returns that count', 'M = 10**9 + 7\ndef drop_point_routes(g):\n    R, C = len(g), len(g[0])\n    d = [[0] * C for _ in range(R)]\n    for i in range(R):\n        for j in range(C):\n            if g[i][j] != ".": continue\n            d[i][j] = 1 if i == j == 0 else ((d[i-1][j] if i else 0) + (d[i][j-1] if j else 0)) % M\n    return d[-1][-1]\n'),
  ('x-abs-of-difference', 'both counts reduced, abs() of the difference', 'M = 10**9 + 7\ndef drop_point_routes(g):\n    R, C = len(g), len(g[0])\n    a = [[0] * C for _ in range(R)]; c = [[0] * C for _ in range(R)]\n    for i in range(R):\n        for j in range(C):\n            if g[i][j] == "#": continue\n            if i == j == 0: x = y = 1\n            else:\n                x = (a[i-1][j] if i else 0) + (a[i][j-1] if j else 0)\n                y = (c[i-1][j] if i else 0) + (c[i][j-1] if j else 0)\n            a[i][j] = x % M; c[i][j] = 0 if g[i][j] == "P" else y % M\n    return abs(a[-1][-1] - c[-1][-1])\n'),
  ('x-start-P-missed', 'a drop point on the start cell does not count', 'M = 10**9 + 7\ndef drop_point_routes(g):\n    R, C = len(g), len(g[0])\n    a = [[0] * C for _ in range(R)]; c = [[0] * C for _ in range(R)]\n    for i in range(R):\n        for j in range(C):\n            if g[i][j] == "#": continue\n            if i == j == 0: a[i][j] = c[i][j] = 1; continue\n            x = (a[i-1][j] if i else 0) + (a[i][j-1] if j else 0)\n            y = (c[i-1][j] if i else 0) + (c[i][j-1] if j else 0)\n            a[i][j] = x % M; c[i][j] = 0 if g[i][j] == "P" else y % M\n    return (a[-1][-1] - c[-1][-1]) % M\n'),
 ],
 'ci-first-fit-slot': [
  ('x-break-after-first-push', 'after one push to a booking end the slot is taken without looking at the next booking', 'def first_fit(bookings, start, length):\n    slot = start\n    for s, e in bookings:\n        if e <= slot: continue\n        if s >= slot + length: break\n        slot = e\n        break\n    m = []\n    for s, e in sorted(bookings + [[slot, slot + length]]):\n        if m and s <= m[-1][1]: m[-1][1] = max(m[-1][1], e)\n        else: m.append([s, e])\n    return [slot, m]\n'),
  ('x-join-new-only', 'joins the job to its neighbours, leaves old touching pairs apart', 'def first_fit(bookings, start, length):\n    slot = start\n    for s, e in bookings:\n        if e <= slot: continue\n        if s >= slot + length: break\n        slot = e\n    lo, hi = slot, slot + length\n    out = []\n    for s, e in bookings:\n        if e == lo: lo = s\n        elif s == hi: hi = e\n        else: out.append([s, e])\n    return [slot, sorted(out + [[lo, hi]])]\n'),
  ('x-no-join-far-from-job', 'joins touching pairs only from the job onwards', 'def first_fit(bookings, start, length):\n    slot = start\n    for s, e in bookings:\n        if e <= slot: continue\n        if s >= slot + length: break\n        slot = e\n    m = []\n    for s, e in sorted(bookings + [[slot, slot + length]]):\n        if m and s <= m[-1][1] and e >= slot: m[-1][1] = max(m[-1][1], e)\n        else: m.append([s, e])\n    return [slot, m]\n'),
  ('x-slot-after-last-always', 'when start is past every booking, the slot is the last end', 'def first_fit(bookings, start, length):\n    slot = start\n    for s, e in bookings:\n        if e <= slot: continue\n        if s >= slot + length: break\n        slot = e\n    if bookings and start >= bookings[-1][1]: slot = bookings[-1][1]\n    m = []\n    for s, e in sorted(bookings + [[slot, slot + length]]):\n        if m and s <= m[-1][1]: m[-1][1] = max(m[-1][1], e)\n        else: m.append([s, e])\n    return [slot, m]\n'),
 ],
}


def git_json(rev, did):
    try:
        return json.loads(subprocess.run(['git', 'show', f'{rev}:{D}/{did}.json'], capture_output=True, text=True, check=True).stdout)
    except subprocess.CalledProcessError:
        return None


def _work(src, cases, q):
    sys.setrecursionlimit(3000)
    env = {}
    try:
        exec(src, env)
    except BaseException as e:
        q.put([('load', repr(e)[:60])] * 1 + [None])
        return
    out = []
    for i, t in enumerate(cases):
        try:
            if t.get('setup'):
                exec(t['setup'], env)
            got, want = eval(t['call'], env), eval(t['expect'], {})
            if not (got == want and (type(got) is type(want) or isinstance(got, (int, float)) and isinstance(want, (int, float)))):
                out.append((i, repr(got)[:60]))
        except BaseException as e:
            out.append((i, type(e).__name__))
    q.put(out + [None])


def run(src, cases):
    """-> (list of failing case numbers (0-based) or ['time'] / ['load'], seconds)"""
    q = mp.Queue()
    p = mp.Process(target=_work, args=(src, cases, q))
    t0 = time.time()
    p.start()
    try:
        res = q.get(timeout=LIMIT)
    except Exception:
        res = None
    dt = time.time() - t0
    if p.is_alive():
        p.terminate()
    p.join()
    if res is None:
        return ['time'], dt
    return [r[0] for r in res if r is not None], dt


def brute(did):
    if did == 'ci-loop-cables':
        def f(n, cables):
            adj, out = {i: set() for i in range(n)}, []
            for k, (a, b) in enumerate(cables):
                seen, todo = {a}, [a]
                while todo:
                    for y in adj[todo.pop()]:
                        if y not in seen:
                            seen.add(y); todo.append(y)
                if b in seen:
                    out.append(k)
                adj[a].add(b); adj[b].add(a)
            return out
        return f, lambda a: a[0] <= 12
    if did == 'ci-drop-point-routes':
        def f(grid):
            R, C = len(grid), len(grid[0])
            n = 0
            for downs in itertools.combinations(range(R + C - 2), R - 1):
                i = j = 0
                cells = [(0, 0)]
                for s in range(R + C - 2):
                    if s in downs: i += 1
                    else: j += 1
                    cells.append((i, j))
                if all(grid[x][y] != '#' for x, y in cells) and any(grid[x][y] == 'P' for x, y in cells):
                    n += 1
            return n % 1000000007
        return f, lambda a: len(a[0]) + len(a[0][0]) <= 16
    def f(bookings, start, length):
        t = start
        while any(s < t + length and t < e for s, e in bookings):
            t += 1
        spans = sorted([list(b) for b in bookings] + [[t, t + length]])
        busy = sorted(set(m for s, e in spans for m in range(s, e)))
        out = []
        for m in busy:  # minutes: a run of booked minutes is one joined booking (touching or overlapping)
            if out and out[-1][1] == m: out[-1][1] = m + 1
            else: out.append([m, m + 1])
        return [t, out]
    return f, lambda a: (not a[0] or a[0][-1][1] <= 60) and a[1] <= 60 and a[2] <= 40


def args_of(case, fn):
    got = []
    env = {fn: lambda *a: got.append(a)}
    try:
        eval(case['call'], env)
    except Exception:
        pass
    return got


def fits(val, c):
    """value against one typed `constraints` object"""
    t = c.get('type', c) if isinstance(c, dict) else c
    if t == 'int':
        lo, hi = c.get('range', [None, None]) if isinstance(c, dict) else (None, None)
        return isinstance(val, int) and (lo is None or lo <= val <= hi)
    if t == 'str':
        import re
        lo, hi = c.get('len', [0, 10**9])
        return isinstance(val, str) and lo <= len(val) <= hi and ('pattern' not in c or re.fullmatch(c['pattern'], val) is not None)
    if t == 'list':
        lo, hi = c.get('len', [0, 10**9])
        of = c.get('of')
        if isinstance(of, str):
            of = {'type': of, 'range': c['range']} if 'range' in c else {'type': of}
        return isinstance(val, list) and lo <= len(val) <= hi and all(fits(v, of) for v in val)
    return True


def extra_rules(did, a):
    if did == 'ci-loop-cables':
        n, cables = a
        return all(x != y and 0 <= x < n and 0 <= y < n for x, y in cables)
    if did == 'ci-drop-point-routes':
        g = a[0]
        return len(set(map(len, g))) == 1 and g[0][0] != '#' and g[-1][-1] != '#'
    b, start, length = a
    return all(s < e for s, e in b) and all(b[i][1] <= b[i + 1][0] for i in range(len(b) - 1))


def main():
    ids = sys.argv[1:] or list(DRILLS)
    bad = False
    tried = passing = 0
    for did in ids:
        pack = DRILLS[did]
        now = json.load(open(f'{D}/{did}.json'))
        states = [('orig', git_json(FIRST_FIX[pack] + '^', did)), ('mid', git_json(DELTA_FIX + '^', did)), ('now', now)]
        states = [(k, v) for k, v in states if v]
        mid = dict(states)['mid']
        print(f'\n## {did} (pack {pack}): tests ' + ', '.join(f'{k} {len(v["tests"])}' for k, v in states))
        old_calls = {json.dumps(t, sort_keys=True) for t in mid['tests']}
        new_calls = {json.dumps(t, sort_keys=True) for t in now['tests']}
        for i, t in enumerate(now['tests']):
            if json.dumps(t, sort_keys=True) not in old_calls:
                print(f'  new or changed tests[{i}]: {t["call"][:150]} -> {t["expect"][:70]}')
        for i, t in enumerate(mid['tests']):
            if json.dumps(t, sort_keys=True) not in new_calls:
                print(f'  gone since mid, was tests[{i}]: {t["call"][:150]} -> {t["expect"][:70]}')
        import re
        m = re.search(r'runs (\d+) hidden', now['how'])
        ok = bool(m) and int(m.group(1)) == len(now['tests'])
        print(f'  how line says {m.group(1) if m else "?"} tests, file has {len(now["tests"])}: {"ok" if ok else "FAIL"}')
        bad |= not ok
        # inputs against the constraints
        cons = {c['arg']: c for c in now['constraints'] if isinstance(c, dict)}
        names = list(cons)
        off = []
        for i, t in enumerate(now['examples'] + now['tests']):
            for a in args_of(t, now['fn']):
                if not all(fits(v, cons[nm]) for v, nm in zip(a, names)) or not extra_rules(did, a):
                    off.append(i)
        print(f'  inputs of {len(now["examples"])} examples and {len(now["tests"])} tests inside the constraints: {"ok" if not off else "FAIL cases " + str(off)}')
        bad |= bool(off)
        cases = now['examples'] + now['tests']
        for nm, src in (('model', now['solution']), ('mine', MINE[did])):
            f, dt = run(src, cases)
            print(f'  {nm:6} {"passes all " + str(len(cases)) if not f else "FAILS " + str(f)} ({dt:.2f} s)')
            bad |= bool(f)
        f, dt = run(now['starter'], now['tests'])
        print(f'  starter fails {len(f)} of {len(now["tests"])}')
        bad |= not f
        bf, small = brute(did)
        env = {}
        exec(MINE[did], env)
        exec(now['solution'], env2 := {})
        nb = 0
        for t in cases:
            for a in args_of(t, now['fn']):
                if small(a):
                    nb += 1
                    import copy
                    if bf(*copy.deepcopy(a)) != eval(t['expect']) and list(eval(t['expect'])) != bf(*copy.deepcopy(a)):
                        print('  BRUTE DISAGREES', t['call'][:100]); bad = True
        # random small inputs: model, mine and brute agree
        rnd = random.Random(20261112)
        dis = 0
        for _ in range(3000):
            if did == 'ci-loop-cables':
                n = rnd.randint(2, 7)
                a = (n, [rnd.sample(range(n), 2) for _ in range(rnd.randint(0, 10))])
            elif did == 'ci-drop-point-routes':
                R, C = rnd.randint(1, 5), rnd.randint(1, 5)
                g = [''.join(rnd.choice('...#P') for _ in range(C)) for _ in range(R)]
                g[0] = rnd.choice('.P') + g[0][1:]
                g[-1] = g[-1][:-1] + rnd.choice('.P')
                a = (g,)
            else:
                b, t = [], rnd.randint(0, 3)
                for _ in range(rnd.randint(0, 5)):
                    e = t + rnd.randint(1, 4)
                    b.append([t, e]); t = e + rnd.choice([0, 0, 1, 2, 3])
                a = (b, rnd.randint(0, 22), rnd.randint(1, 5))
            import copy
            r = [fn(*copy.deepcopy(a)) for fn in (env2[now['fn']], env[now['fn']], bf)]
            if not (r[0] == r[1] == r[2]):
                dis += 1
                if dis < 3:
                    print('  DISAGREE on', a, r)
        print(f'  brute force agrees with {nb} small examples and tests; model, mine and brute agree on {3000 - dis} of 3000 random small inputs')
        bad |= dis > 0
        # candidates
        cands = []
        for fpath in sorted(glob.glob(os.path.join(REV, f'drills-ci-{pack}-scripts', 'wrong*.py')) + glob.glob(os.path.join(REV, f'drills-ci-{pack}-scripts', 'right.py'))):
            e = {}
            exec(open(fpath).read(), e)
            for label, (d2, code, comment) in e['CANDIDATES'].items():
                if d2 == did:
                    cands.append(('first', label, comment, code))
            for label, (d2, code, comment) in e.get('RIGHT_AFTER_ALL', {}).items():
                if d2 == did:
                    cands.append(('first', label + '_OK', comment, code))
        wk = open(os.path.join(REV, 'review-delta-drills-ci-5-8-scripts', 'weak_78.py')).read()
        for var, d2 in (('DROP', 'ci-drop-point-routes'), ('FIT', 'ci-first-fit-slot')):
            if d2 == did:
                cands.append(('delta', 'weak_78.' + var, 'the delta reader\'s candidate', wk.split(var + " = '''")[1].split("'''")[0]))
        seen = set()
        for k, st in states:
            for i, pl in enumerate(st.get('planted', [])):
                if pl['code'] not in seen:
                    seen.add(pl['code'])
                    cands.append(('plant', f'planted[{i}] of {k}', pl.get('slip', '')[:80], pl['code']))
        cands += [('ac2', nm, why, src) for nm, why, src in EXTRA[did] if src]
        nowplants = {pl['code'] for pl in now.get('planted', [])}
        from multiprocessing.pool import ThreadPool
        jobs = [(ci, k, code, st['tests']) for ci, (_, _, _, code) in enumerate(cands) for k, st in states]
        with ThreadPool(JOBS) as tp:
            done = tp.map(lambda j: (j[0], j[1], run(j[2], j[3])[0]), jobs)
        allres = {}
        for ci, k, f in done:
            allres.setdefault(ci, {})[k] = f
        for ci, (pool, label, comment, code) in enumerate(cands):
            res = allres[ci]
            right = pool != 'plant' and (label.endswith(RIGHT[:2]) or label.startswith('R_') or label in RIGHT)
            fn = res['now']
            show = lambda f: 'passes' if not f else ('time' if f == ['time'] else str([x + 1 if isinstance(x, int) else x for x in f][:6]))
            line = f'{pool:5} {label[:52]:52} ' + ' | '.join(f'{k} {show(res[k])}' for k, _ in states)
            if right:
                print(f'  right      {line}' + ('' if not fn else '   RIGHT SOLUTION REFUSED'))
                bad |= bool(fn)
                continue
            tried += 1
            if not fn:
                passing += 1
                was = any(res[k] for k, _ in states if k != 'now')
                print(f'  {"REGRESSION" if was else "PASSES NOW"} {line}  ({comment[:70]})')
                bad = True
            else:
                if code in nowplants and False:
                    pass
                print(f'  caught     {line}')
            if pool == 'plant' and code in nowplants and not fn:
                print('  PLANT PASSES'); bad = True
    print(f'\ncandidates tried {tried}, passing every test now {passing}; exit {1 if bad else 0}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
