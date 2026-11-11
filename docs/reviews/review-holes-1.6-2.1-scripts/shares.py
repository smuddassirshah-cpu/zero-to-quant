"""Sizes for the Fluency findings, over 200 draws of a family (drawn here with fluency-sample.mjs):
  - poisson-ratio-test: share of draws where a logarithm kept to 4 or 5 places, or a ratio kept to 4, leaves the band,
    under the present band (0.0005) and under wider ones
  - two-by-two: the same for expected counts kept to 2 places, and for the rounding the solution itself prints
  - uniform-moment: share where the moment estimate is below the largest draw
  - assign-and-update, volatility-se: share of draws whose prompt carries a % sign
  - s-pool-rates (exam): what logarithms kept to 2, 3 and 4 places give
  python3 docs/reviews/review-holes-1.6-2.1-scripts/shares.py      (from the repo root; needs numpy, scipy)"""
import json
import math
import re
import subprocess

import numpy as np
from scipy import stats


def draw(set_id, fam, n=200, seed=9001):
    out = subprocess.run(['node', 'app/tools/fluency-sample.mjs', '--set', set_id, '--family', fam, '--seed', str(seed), '--n', str(n), '--json'],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def share(vals, tol):
    return sum(1 for a, b in vals if abs(a - b) > tol)


items = draw('testing/fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test')
rows = {'log 4 places': [], 'log 5 places': [], 'ratio 4 places': [], 'log 3 places': []}
for it in items:
    p = it['prompt']
    s, n = map(int, re.search(r'^(\d+) \w+ arrive in (\d+)', p).groups())
    lam0 = float(re.search(r'lambda_0 = ([\d.]+)', p).group(1))
    dv = s - n * lam0
    lr = math.log(s / (n * lam0))
    key = 2 * (s * lr - dv)
    assert abs(key - it['answer']) < 1e-9
    rows['log 3 places'].append((2 * (s * round(lr, 3) - dv), key))
    rows['log 4 places'].append((2 * (s * round(lr, 4) - dv), key))
    rows['log 5 places'].append((2 * (s * round(lr, 5) - dv), key))
    rows['ratio 4 places'].append((2 * (s * math.log(round(s / (n * lam0), 4)) - dv), key))
print('poisson-ratio-test, draws out of', len(items), 'outside the band, by band:')
for k, v in rows.items():
    print(f'  {k:16s}', {tol: share(v, tol) for tol in (0.0005, 0.005, 0.05)}, 'largest miss', round(max(abs(a - b) for a, b in v), 4))

items = draw('testing/fluency-l18-counts-against-expectations', 'two-by-two')
rows = {'expected counts to 2 places': [], 'expected counts to 1 place': [], "the solution's own rounding": []}
for it in items:
    p = it['prompt']
    tot, r1, a, b, r2, c, d = map(int, re.search(r'Of (\d+) \w+, (\d+) were .*?: (\d+) \w+ and (\d+) \w+\. The other (\d+) were .*?: (\d+) \w+ and (\d+) \w+', p).groups())
    t = np.array([[a, b], [c, d]])
    key, _, _, exp = stats.chi2_contingency(t, correction=False)
    assert abs(key - it['answer']) < 1e-9
    for dp, name in ((2, 'expected counts to 2 places'), (1, 'expected counts to 1 place')):
        e = np.round(exp, dp)
        rows[name].append((float(((t - e) ** 2 / e).sum()), key))
    gap3 = round(abs(a - exp[0, 0]), 3)
    rows["the solution's own rounding"].append((sum(gap3 ** 2 / e for e in exp.ravel()), key))
print('two-by-two, draws out of', len(items), 'outside the band, by band:')
for k, v in rows.items():
    print(f'  {k:28s}', {tol: share(v, tol) for tol in (0.0005, 0.005, 0.05)}, 'largest miss', round(max(abs(a - b) for a, b in v), 4))

items = draw('testing/fluency-l13-matching-moments', 'uniform-moment')
low = 0
for it in items:
    x = [float(v) for v in re.findall(r'\d+', re.search(r'are ([\d, and]+)\. What', it['prompt']).group(1))]
    low += it['answer'] < max(x)
print('uniform-moment: moment estimate below the largest draw in', low, 'of', len(items))

items = draw('stat-learning/fluency-l16-groups-nobody-labelled', 'assign-and-update')
print('assign-and-update: prompt gives the values in % in', sum('%' in it['prompt'] for it in items), 'of', len(items))
whole = sum(abs(it['answer'] - round(it['answer'])) < 1e-9 for it in items)
print('assign-and-update: answer a whole number in', whole, 'of', len(items))

items = draw('stat-learning/fluency-l16-groups-nobody-labelled', 'linkage-distance')
print('linkage-distance: answer needs a third decimal place in', sum(abs(it['answer'] * 100 - round(it['answer'] * 100)) > 1e-9 for it in items), 'of', len(items))

print('exam s-pool-rates, -2 ln Lambda with the two logarithms kept to k places (key 6.0406, band 0.005; Pearson entry 6.0 +- 0.001):')
for k in (2, 3, 4, 5):
    v = 2 * (90 * round(math.log(1.2), k) + 60 * round(math.log(0.8), k))
    print(f'  {k} places: {v:.4f}', 'correct' if abs(v - 6.0406) <= 0.005 else 'lands on "pearson"' if abs(v - 6.0) <= 0.001 else 'generic')
print('problem p-night-admissions part 2, log kept to k places (key 1.966, band 0.0005):')
for k in (3, 4, 5):
    v = 2 * (38 * round(math.log(3.8 / 3), k) - 8)
    print(f'  {k} places: {v:.4f}', 'correct' if abs(v - 1.966) <= 0.0005 else 'refused')
print('problem p-bakery-loaves part 4, p-value from X^2 kept to k places (key 0.0281, band 0.00005):')
for k in (1, 2, 3):
    v = math.exp(-round(50 / 7, k) / 2)
    print(f'  {k} places: {v:.5f}', 'correct' if abs(v - 0.0281) <= 0.00005 else 'refused')
