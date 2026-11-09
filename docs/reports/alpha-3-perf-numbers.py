"""Recompute every number in alpha homework-3 item h-overlap-aloud (performance task, aloud).

Run from the repo root with a Python that has NumPy (the scratchpad venv):
    <venv>/bin/python docs/reports/alpha-3-perf-numbers.py      exits 0 when every check passes.
Each figure is found twice: once by the closed form the model uses, once by counting or by a
seeded simulation of overlapping ICs (daily noise, each IC the mean of the next 63 days).
"""
import json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/alpha/homework-3.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-overlap-aloud')
w = item['widget']
text = json.dumps(item)
fails = []

def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

n, h, t_naive = 756, 63, 9.5

# 1. three years of trading days, and 12 independent quarters
check('756 dates = three years of 252', n == 3 * 252)
check('756/63 = 12 by division', n / h == 12)
check('756/63 = 12 by counting non-overlapping windows', len(range(0, n, h)) == 12)

# 2. neighbours share 62 of 63 days; k apart share 63 - k; none at 63
win = lambda t: set(range(t + 1, t + h + 1))
check('IC on t and t + 1 share 62 days', len(win(0) & win(1)) == 62)
check('k apart share 63 - k (k = 0..70)', all(len(win(0) & win(k)) == max(h - k, 0) for k in range(71)))
check('62 lags: lag 62 shares a day, lag 63 shares none', len(win(0) & win(62)) == 1 and not win(0) & win(63))

# 3. the sum in the model, closed form against a direct sum
direct = sum(1 - k / h for k in range(1, h))
check('sum (1 - k/h), k < h, equals (h - 1)/2 = 31', abs(direct - (h - 1) / 2) < 1e-12 and (h - 1) / 2 == 31, f'{direct:.12f}')
check('sum of k, k < h, is h(h - 1)/2 = 1953', sum(range(1, h)) == h * (h - 1) // 2 == 1953)
check('1 + 2 * 31 = 63 = h', 1 + 2 * (h - 1) / 2 == h)
exact = 1 + 2 * sum((1 - k / n) * (1 - k / h) for k in range(1, h))
print(f'     finite-n factor with end effects: {exact:.3f}')

# 4. seeded simulation: correlation 1 - k/63, variance of the mean about h times sigma^2/n
rng = np.random.default_rng(2310)
sims = 4000
e = rng.standard_normal((sims, n + h))
c = np.concatenate([np.zeros((sims, 1)), np.cumsum(e, axis=1)], axis=1)
ic = (c[:, h + 1: n + h + 1] - c[:, 1: n + 1]) / h        # IC_t = mean of e over t+1..t+63
sigma2 = 1 / h                                             # variance of one IC
t0 = 300                                                   # population correlation across paths
for k in (1, 21, 62, 63):
    r = np.corrcoef(ic[:, t0], ic[:, t0 + k])[0, 1]
    check(f'simulated correlation at lag {k} near {max(1 - k / h, 0):.3f}', abs(r - max(1 - k / h, 0)) < 0.04, f'{r:.3f}')
ratio = ic.mean(axis=1).var() / (sigma2 / n)
check('simulated Var(mean) / (sigma^2/n) near the finite-n factor', abs(ratio / exact - 1) < 0.1, f'{ratio:.2f} vs {exact:.2f}')
check('and near h = 63 (within 10%)', abs(ratio / h - 1) < 0.1, f'{ratio:.2f}')
s2 = ic.var(axis=1, ddof=1)
check('sd of the daily ICs close to one IC\'s spread (s/sigma 0.9 to 1)', 0.9 < math.sqrt(s2.mean() / sigma2) < 1, f'{math.sqrt(s2.mean() / sigma2):.3f}')
infl = np.median(np.sqrt(sigma2 * exact / n) / np.sqrt(s2 / n))  # typical honest SE over s/sqrt(n)
print(f'     simulated median of honest SE / formula SE: {infl:.2f}')

# 5. the stated figures
s63 = math.sqrt(h)
check('sqrt(63) = 7.94 (and "7.9", "nearly eight")', f'{s63:.2f}' == '7.94' and f'{s63:.1f}' == '7.9' and 7.5 < s63 < 8, f'{s63:.6f}')
honest_a = t_naive / 7.94
honest_b = t_naive * math.sqrt(12 / n)
honest_c = t_naive / infl
check('9.5/7.94 rounds to 1.2', f'{honest_a:.1f}' == '1.2', f'{honest_a:.4f}')
check('9.5 * sqrt(12/756) rounds to 1.2', f'{honest_b:.1f}' == '1.2', f'{honest_b:.4f}')
check('9.5 / simulated SE ratio is "about 1.2" (1.1 to 1.3)', 1.1 < honest_c < 1.3, f'{honest_c:.4f}')
check('sqrt(756/12) = sqrt(63)', abs(math.sqrt(n / 12) - s63) < 1e-12)
check('honest t is below 2', max(honest_a, honest_b, honest_c) < 2)
for phrase in ('756', '63-day', '0.04', '9.5', '62 of its 63', '756/63 = 12', '\\\\sqrt{63} = 7.94', '9.5/7.94 = 1.2', '62 lags'):
    check(f'item states {phrase}', phrase in text)

# 6. shape the validator and the brief require
rub = w['rubric']
check('rubric 3 to 5 rows summing to 10', 3 <= len(rub) <= 5 and sum(r['points'] for r in rub) == 10, str([r['points'] for r in rub]))
# fix pass (review-perf-retrofit-3): required rows follow DECISIONS Session X, one per named part, never every row
check('4 required rows, not every row', sum(1 for r in rub if r.get('required') is True) == 4 and 4 < len(rub))
check('seconds 15 to 1800, followUps 1 to 5', 15 <= w['seconds'] <= 1800 and 1 <= len(w['followUps']) <= 5)
check('no starter, steps, hints or parts', not any(k in w for k in ('starter', 'steps', 'order', 'derive')) and 'hints' not in item and 'parts' not in item)
check('homework items within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('one performance item in the homework', sum(1 for i in doc['items'] if i.get('performance')) == 1)

print(f'\n{len(fails)} failures')
sys.exit(1 if fails else 0)
