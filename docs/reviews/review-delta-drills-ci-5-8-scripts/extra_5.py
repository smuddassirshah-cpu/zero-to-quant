"""Pack 5 extras. Usage (repo root): python3 extra_5.py
1. ci-half-fare-route (task changed in the fix pass): model, my two-search method and a
   brute force over every simple route with the voucher on every allowed road, on random
   small networks.
2. ci-loop-cables: what planted[0] returns on the old and the new tests[2] (finding 1).
3. Difficulty mix of the pack."""
import itertools
import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mine_5  # noqa: E402

D = 'app/content/drills'


def load(i):
    return json.load(open(f'{D}/{i}.json'))


def fn(src, name):
    env = {}
    exec(src, env)
    return env[name]


def brute_half(n, roads, src, dst):
    if src == dst:
        return 0
    best = None
    others = [t for t in range(n) if t not in (src, dst)]
    for k in range(len(others) + 1):
        for mid in itertools.permutations(others, k):
            route = (src,) + mid + (dst,)
            # each hop may use any road between the pair
            opts = []
            ok = True
            for a, b in zip(route, route[1:]):
                ws = [w for x, y, w in roads if {x, y} == {a, b}]
                if not ws:
                    ok = False
                    break
                opts.append((a, b, ws))
            if not ok:
                continue
            full = sum(min(ws) for _, _, ws in opts)
            cands = [full]
            for i, (a, b, ws) in enumerate(opts):
                if src in (a, b):
                    continue
                rest = full - min(ws)
                cands.append(rest + min(w // 2 for w in ws))
            c = min(cands)
            if best is None or c < best:
                best = c
    return -1 if best is None else best


def main():
    bad = 0
    d = load('ci-half-fare-route')
    model = fn(d['solution'], 'cheapest_with_coupon')
    rng = random.Random(58)
    for trial in range(4000):
        n = rng.randint(1, 6)
        roads = []
        if n > 1:
            for _ in range(rng.randint(0, 9)):
                a, b = rng.sample(range(n), 2)
                roads.append([a, b, rng.randint(1, 30)])
        src, dst = rng.randrange(n), rng.randrange(n)
        r = (model(n, roads, src, dst), mine_5.cheapest_with_coupon(n, roads, src, dst), brute_half(n, roads, src, dst))
        if len(set(r)) != 1:
            bad += 1
            print('half-fare DISAGREE', n, roads, src, dst, r)
            if bad > 5:
                break
    print('half-fare: 4000 random networks, model / mine / brute disagreements:', bad)

    d = load('ci-loop-cables')
    p0 = fn(d['planted'][0]['code'], 'loop_cables')
    model = fn(d['solution'], 'loop_cables')
    for label, args in (('old tests[2]', (3, [[0, 1], [0, 2], [1, 2]])),
                        ('new tests[2]', (4, [[3, 1], [0, 3], [1, 0], [2, 0]])),
                        ('a small catch', (4, [[1, 3], [1, 0], [3, 0], [2, 3]]))):
        print('loop-cables', label, args, 'model', model(*args), 'planted[0]', p0(*args))
    first = None
    for i, t in enumerate(d['tests']):
        env = {'loop_cables': p0}
        if eval(t['call'], env) != eval(t['expect']):
            first = i
            break
    print('loop-cables planted[0] first fails tests[%s]' % first)

    for pack in (5, 6, 7, 8):
        mix = Counter()
        import glob
        for f in glob.glob(f'{D}/ci-*.json'):
            j = json.load(open(f))
            if j['tags'][0] == f'pack-{pack}':
                mix[j['difficulty']] += 1
        print('pack', pack, 'mix', sorted(mix.items()))
    sys.exit(1 if bad else 0)


main()
