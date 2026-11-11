"""Shared loop for extra_7.py and extra_8.py: run a plain brute force on every example
and hidden test small enough for it, then against the model on random small inputs."""
import copy
import json
import random

D = 'app/content/drills'


def run_brutes(brutes, seed, default_n=1500):
    """brutes: {drill id: (brute fn, small(args) -> bool, gen(rng) -> args[, n random])}.
    Returns the number of disagreements."""
    bad = 0
    for did, spec in brutes.items():
        brute, small, gen = spec[:3]
        n_random = spec[3] if len(spec) > 3 else default_n
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
                    pass          # a wrapped call fails on None; the arguments are kept
                if len(seen) != 1 or not small(seen[0]):
                    continue
                args = seen[0]
                want = eval(t['expect'])
                got = eval(t['call'], {d['fn']: brute})
                ran += 1
                if got != want:
                    bad += 1
                    print('BRUTE DISAGREES', did, kind, i, args, 'brute', got, 'expect', want)
        rng = random.Random(seed)
        dis = 0
        for _ in range(n_random):
            args = gen(rng)
            a, b = model(*copy.deepcopy(args)), brute(*copy.deepcopy(args))
            if a != b:
                dis += 1
                if dis < 3:
                    print('RANDOM DISAGREE', did, args, 'model', a, 'brute', b)
        bad += dis
        print('%-22s brute on %2d of %2d cases; %d random, %d disagreements'
              % (did, ran, len(d['examples']) + len(d['tests']), n_random, dis))
    return bad
