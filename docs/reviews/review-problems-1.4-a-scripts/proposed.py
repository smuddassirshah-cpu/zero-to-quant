"""Numbers of the fixes proposed in docs/reviews/review-problems-1.4-a.md, each worked twice.

Usage (repo root): <venv>/bin/python docs/reviews/review-problems-1.4-a-scripts/proposed.py"""
import glob
import json
import sys
from math import acos, atan2, degrees, hypot, sqrt

import numpy as np

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
    print(('ok   ' if cond else 'FAIL ') + msg)


# finding 3: site plan part 4, the directed step and the undirected line
R = np.array([[.8, -.6], [.6, .8]])
step = R @ np.array([0., 10.])
phi = degrees(acos(step[0] / hypot(*step)))
ok(np.allclose(step, [-6, 8]) and round(phi, 1) == 126.9 == round(degrees(atan2(step[1], step[0])), 1), f'site 4: the step (-6, 8) is at {phi:.2f} degrees from (1, 0), by acos and by atan2')
ok(round(180 - phi, 1) == 53.1 and round(degrees(acos(.6)), 1) == 53.1, 'site 4: the line makes the acute angle 53.1 with the axis, which is also the angle of R^T(0, 10) = (6, 8)')

# finding 4: factor risk part 3 to 5 places
F = np.array([[.0225, .003], [.003, .0064]])
e = np.array([1.04, .25])
ok(np.allclose(F @ e, [.02415, .00472], atol=1e-12) and [round(x, 5) for x in F @ e] == [.02415, .00472], 'factor 3: F e = (0.02415, 0.00472) exactly, 5 places')

# finding 7: engraver part 3, the two slips inside the `added` band
ok(abs(-22 / 9 + 2.444) < 5e-4 and abs(-2 - (-2.444)) < 0.5, 'engraver 3: -22/9 = -2.444 and the sign slip -2 sits 0.444 from it, inside the band of 0.5')

# finding 8: a robot with arrows that are not l3's pair
u, v = np.array([4., 1.]), np.array([1., 3.])
a, b = np.linalg.solve(np.column_stack([u, v]), [11, 11])
L1, L2 = 2 * u, 3 * v
ang = degrees(acos(L1 @ L2 / sqrt((L1 @ L1) * (L2 @ L2))))
ok(np.allclose([a, b], [2, 3]), 'robot: 2(4, 1) + 3(1, 3) = (11, 11)')
ok(L1 @ L2 == 42 == 6 * (u @ v) and u @ v == 7 and L1 @ v == 14 and u @ L2 == 21, 'robot 2: dot product 42; slips 7, 14, 21')
ok(L1 @ L1 == 68 and L2 @ L2 == 90 and round(ang) == 58 and abs(ang - 57.5) > 0.02, f'robot 3: angle {ang:.2f}, 58 to the nearest degree and not on a rounding tie')
ok(round(np.radians(ang), 3) == 1.004 and round(degrees(acos(42 / (68 * 90)))) == 90, 'robot 3: slips 1.004 rad and 90 (dividing by the squared lengths)')
line = np.linalg.norm(L1 + L2)
ok(round(line, 2) == 15.56 == round(sqrt(11 ** 2 + 11 ** 2), 2) and 68 + 84 + 90 == 242, f'robot 4: straight line {line:.4f}')
ok(round(sqrt(68 + 90), 2) == 12.57 and round(sqrt(68) + sqrt(90), 2) == 17.73 and round(sqrt(68 - 84 + 90), 2) == 8.60, 'robot 4: slips 12.57, 17.73, 8.60, 242')
pair = []
for f in sorted(glob.glob('app/content/courses/vectors/*.json')):
    if 'problems-' in f or f.endswith('course.json'):
        continue
    doc = json.load(open(f))
    for i, sc in enumerate(doc.get('screens') or doc.get('items') or []):
        t = json.dumps(sc)
        if '(4, 1)' in t and '(1, 3)' in t:
            pair.append(f'{f.split("/")[-1]}[{i}]')
ok(not pair, f'robot: no lesson screen, review or homework item of the course holds both (4, 1) and (1, 3) {pair}')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
