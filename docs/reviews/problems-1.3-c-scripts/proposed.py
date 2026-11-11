"""Numbers behind the fixes proposed in review-problems-1.3-c.md, each computed twice, plus the skills check.

Run from the repo root:  <venv>/bin/python docs/reviews/problems-1.3-c-scripts/proposed.py
"""
import glob
import json
import math
import sys

import mpmath as mp

bad = 0


def ok(c, msg):
    global bad
    print(('ok   ' if c else 'FAIL ') + msg)
    bad += not c


# Finding: limits 4 p-barbell-hedge part 4, a named line for the second-order estimate
V = lambda u: 50 * math.exp(-2 * u) + 50 * math.exp(-8 * u) - 100 * math.exp(-5 * u)  # noqa: E731
so = 0.5 * 900 * 0.01 ** 2 * 1000
ok(abs(so - 45) < 1e-9, f'barbell: (1/2) V\'\'(0) u^2 = {so} pounds')
ans, wrongway = 1000 * V(0.01), 1000 * V(-0.01)
ok(abs(so - ans) > 1.0 and abs(so - wrongway) > 1.0, f'barbell: 45 ± 0.5 clear of the answer {ans:.2f} ± 0.5 and of wrong-way {wrongway:.2f} ± 0.5')
ok(ans < so, 'barbell: the true value is below the second-order estimate')

# Finding: limits 5 p-impact-curve part 4 and integrals 4 p-dish-and-spindle part 4, narrower wrong bands
pq = 1000 / (250000 + (500 * math.tan(0.5)) ** 2)
ok(abs(pq - 0.0031) < 0.0005, f'impact: p\'(273.15) = {pq:.5f}, inside 0.0031 ± 0.0005')
ok(abs(0.002 - 0.0031) > 0.0005 and abs(0.4 - 0.0031) > 0.0005 and abs(0 - 0.0031) > 0.0005, 'impact: 0.002, 0.4 and 0 no longer draw the not-inverted line')
Vy = 2 * math.pi * (2 + math.log(3) - 4 * math.log(2))
Vx = math.pi * (5 / 3 + 4 * math.log(2 / 3))
ok(abs(Vx / Vy - 0.0687) < 0.005, f'dish: inverse ratio {Vx / Vy:.4f}, inside 0.0687 ± 0.005')

# Finding: integrals 4 p-impact-kernel part 1, the unit-rule line
ok(abs(0.5 * (1 / (1 - 0.5)) - 1) < 1e-12 and abs(float(mp.quad(lambda t: 0.5 / mp.sqrt(t), [0, 1])) - 1) < 1e-9, 'kernel: the bound on [0, 1] is (1/2) x 1/(1 - p) = 1')

# Finding: multivar 4 p-drone-landing, freshness. Proposed density c e^{-(x^2 + y^2)/32} (sigma = 4), radius 4 m in part 4.
# (18 is taken: homework-4 h-normal-const uses e^{-(x - 1)^2/18}.)
K, S = 32, 4
one = math.sqrt(K * math.pi)
ok(abs(one - float(mp.quad(lambda x: mp.e ** (-x * x / K), [-mp.inf, mp.inf]))) < 1e-9, f'drone 1: sqrt({K} pi) = {one:.4f}')
print(f'     wrongs: no-scale {math.sqrt(math.pi):.4f}  inverted {math.sqrt(math.pi) / math.sqrt(K):.4f}  sigma-root{K} {math.sqrt(K) * math.sqrt(2 * math.pi):.4f}')
two = float(mp.quad(lambda x, y: mp.e ** (-(x * x + y * y) / K), [-mp.inf, mp.inf], [-mp.inf, mp.inf]))
ok(abs(two - K * math.pi) < 1e-6, f'drone 2: {K} pi = {K * math.pi:.4f}; 3: c = 1/({K} pi) = {1 / (K * math.pi):.4f}')
four = 1 - math.exp(-S * S / K)
ok(abs(four - float(mp.quad(lambda r: mp.e ** (-r * r / K) * r * 2 / K, [0, S]))) < 1e-12, f'drone 4: within {S} m, 1 - e^(-1/2) = {four:.4f}')
print(f'     wrongs: r-not-squared {1 - math.exp(-S / K):.4f}  no-2pi {four / (2 * math.pi):.4f}  outside {1 - four:.4f}')
five = math.sqrt(K * math.log(10))
ok(abs(1 - math.exp(-five ** 2 / K) - 0.9) < 1e-12, f'drone 5: a = sqrt({K} ln 10) = {five:.4f}')
print(f'     wrongs: no-root {K * math.log(10):.2f}  tail-swap {math.sqrt(-K * math.log(0.9)):.2f}  log10 {math.sqrt(K):.2f};  ratio a / {S} = {five / S:.2f}')
hits = [f for f in glob.glob('app/content/courses/multivar/*.json') if f'/{K}}}' in open(f).read()]
ok(not hits, f'drone: no multivar file has an exponent over {K} ({hits})')

# Skills: every skill an item carries is a skill of some lesson of its level
for c, n in [('limits', 4), ('limits', 5), ('integrals', 4), ('multivar', 4), ('multivar', 5)]:
    course = json.load(open(f'app/content/courses/{c}/course.json'))
    lessons = next(l for l in course['levels'] if l['n'] == n)['lessons']
    have = set()
    for l in lessons:
        have |= set(json.load(open(f'app/content/courses/{c}/{l}.json')).get('skills', []))
    used = set()
    for it in json.load(open(f'app/content/courses/{c}/problems-{n}.json'))['items']:
        used |= set(it['skills'])
    ok(used <= have, f'{c} {n}: item skills {sorted(used)} within lesson skills {sorted(have)}')

sys.exit(1 if bad else 0)
