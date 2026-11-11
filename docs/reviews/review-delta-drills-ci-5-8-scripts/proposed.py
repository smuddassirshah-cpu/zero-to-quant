"""The three tests this review proposes: model and mine agree on each `expect`, the
solution each is aimed at fails it, and (for ci-first-fit-slot, which is at the cap of
15 tests) which existing test can make room without letting any planted solution or
first-reader candidate through.
Usage (repo root): python3 proposed.py"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mine_5  # noqa: E402
import mine_7  # noqa: E402
import mine_8  # noqa: E402
from regress import verdict  # noqa: E402

D = 'app/content/drills'
PROPOSED = [
    ('ci-loop-cables', mine_5, 'loop_cables(4, [[1, 3], [1, 0], [3, 0], [2, 3]])', '[2]'),
    ('ci-drop-point-routes', mine_7,
     "drop_point_routes(['.' * 18] * 2 + ['.' * 2 + 'P' + '.' * 15] + ['.' * 18] * 15)", '930705120'),
    ('ci-first-fit-slot', mine_8, 'first_fit([[0, 3], [3, 6], [10, 12]], 20, 4)', '[20, [[0, 6], [10, 12], [20, 24]]]'),
]


def main():
    bad = 0
    for did, mine, call, expect in PROPOSED:
        d = json.load(open(f'{D}/{did}.json'))
        env = {}
        exec(d['solution'], env)
        m = eval(call, env)
        mi = eval(call, {d['fn']: getattr(mine, d['fn'])})
        want = eval(expect)
        ok = m == want == mi
        bad += not ok
        print('%-22s %s -> model %s, mine %s, proposed expect %s: %s' % (did, call[:70], m, mi, want, 'agree' if ok else 'DISAGREE'))
        plus = copy.deepcopy(d)
        plus['tests'].append({'call': call, 'expect': expect, 'compare': 'equal'})
        only = copy.deepcopy(d)
        only['tests'] = [{'call': call, 'expect': expect, 'compare': 'equal'}]
        hit = [k for k, pl in enumerate(d['planted']) if verdict(pl['code'], only, 6)[0] == 'caught']
        print('   planted solutions that fail the proposed test on its own:', hit)

    # first-fit-slot: which test can be replaced?
    d = json.load(open(f'{D}/ci-first-fit-slot.json'))
    env = {}
    exec(open('docs/reviews/drills-ci-8-scripts/wrong.py').read(), env)
    cands = {k: v[1] for k, v in env['CANDIDATES'].items() if v[0] == 'ci-first-fit-slot'}
    base = {k: verdict(c, d, 6)[0] for k, c in cands.items()}
    new = {'call': PROPOSED[2][2], 'expect': PROPOSED[2][3], 'compare': 'equal'}
    print('first-fit-slot: %d first-reader candidates, passing now: %s' % (len(cands), [k for k, v in base.items() if v == 'passes']))
    for i in range(len(d['tests'])):
        trial = copy.deepcopy(d)
        trial['tests'][i] = new
        lost = [k for k, c in cands.items() if base[k] == 'caught' and verdict(c, trial, 6)[0] != 'caught']
        lostp = [k for k, pl in enumerate(d['planted']) if verdict(pl['code'], trial, 6)[0] != 'caught']
        still = [k for k, c in cands.items() if base[k] == 'passes' and verdict(c, trial, 6)[0] == 'passes']
        print('   replace tests[%2d]: candidates lost %s, planted lost %s, still passing %s' % (i, lost, lostp, still))
    sys.exit(1 if bad else 0)


main()
