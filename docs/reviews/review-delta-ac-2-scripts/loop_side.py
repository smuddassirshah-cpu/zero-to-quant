#!/usr/bin/env python3
"""ci-loop-cables: the slip of planted[0] (a rack itself, not its root, hung under the other group) on either side,
with the climb shortened so that no test stops it for time. Which hidden tests catch each side?
The new tests[12] was written against the a side; this asks whether the b side is caught by a small test too.
Usage (repo root): python3 docs/reviews/review-delta-ac-2-scripts/loop_side.py     exit 1 if a side passes every test"""
import json, sys

d = json.load(open('app/content/drills/ci-loop-cables.json'))


def mk(side):
    def loop_cables(n, cables):
        p = list(range(n))

        def f(x):
            r = x
            while p[r] != r:
                r = p[r]
            while p[x] != r:
                p[x], x = r, p[x]
            return r
        out = []
        for i, (a, b) in enumerate(cables):
            ra, rb = f(a), f(b)
            if ra == rb:
                out.append(i)
            elif side == 'a':
                p[a] = rb
            else:
                p[b] = ra
        return out
    return loop_cables


bad = False
for side in 'ab':
    lc = mk(side)
    fails = [i + 1 for i, t in enumerate(d['tests']) if eval(t['call'], {'loop_cables': lc}) != eval(t['expect'])]
    small = [i for i in fails if ' for ' not in d['tests'][i - 1]['call']]
    print(f'rack {side} itself hung under the other root: fails tests {fails}; small (hand-checkable) among them {small}')
    bad |= not fails
sys.exit(1 if bad else 0)
