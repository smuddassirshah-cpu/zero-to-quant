"""Numbers of the fixes proposed in review-problems-0.3-a.md, each by enumeration and by formula, and the freshness of
the new numbers (searched across counting, counting-chance and the exams).

Finding 6 (ice-cream van with 14 flavours in place of 11).

Usage (repo root): <venv>/bin/python docs/reviews/problems-0.3-a-scripts/proposed.py      exit 0 when all pass
"""
import glob
import itertools as it
import json
import re
import sys
from math import comb, perm

checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


N = 14
cups = len(list(it.combinations(range(N), 3)))
cones = len(list(it.permutations(range(N), 3)))
P = {
    1: (364, {'ordered': 2184, 'repeats': 2744, 'times': 42}),
    2: (2184, {'times-three': 1092, 'added': 370, 'carried': 13104}),
    3: (2548, {'multiplied': 794976, 'carried': 15288}),
    4: (12740, {'no-none': 10192, 'added': 2553, 'carried': 3974880}),
}
ok(cups == comb(N, 3) == P[1][0] and cones == perm(N, 3) == P[2][0], 'cups and cones')
ok(P[1][1] == {'ordered': N * 13 * 12, 'repeats': N ** 3, 'times': N * 3}, 'part 1 slips')
ok(P[2][1] == {'times-three': cups * 3, 'added': cups + 6, 'carried': cones * 6}, 'part 2 slips')
ok(P[3][0] == cups + cones and P[3][1] == {'multiplied': cups * cones, 'carried': cones + cones * 6}, 'part 3')
ok(P[4][0] == (cups + cones) * 5 and P[4][1] == {'no-none': 2548 * 4, 'added': 2548 + 5, 'carried': cups * cones * 5}, 'part 4')
for k, (ans, wr) in P.items():
    ok(len({ans, *wr.values()}) == 1 + len(wr), f'part {k}: answer and wrong values all differ')


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


files = sorted(glob.glob('app/content/courses/counting/*.json')) + sorted(glob.glob('app/content/courses/counting-chance/*.json')) \
    + ['app/content/exams/topic-0.3.json', 'app/content/exams/stage-0.json']
hits = []
for f in files:
    b = ' '.join(texts(json.load(open(f))))
    for num in ('364', '2184', '2548', '12740', r'binom\{14\}\{3\}'):
        if re.search(r'(?<![\d.])' + num + r'(?![\d])', b):
            hits.append((f.split('courses/')[-1], num))
print('uses of the new numbers elsewhere:', hits)
# 364 turns up in the later course only as the 364/365 of the birthday problem, never as a count of choices
ok(set(hits) <= {('counting-chance/l10-birthday.json', '364'), ('counting-chance/review-3.json', '364')}, 'new numbers are fresh in counting and the exams')

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
