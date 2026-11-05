"""Recompute every number in the research-int level 1 performance task (homework-1 item h1-signal-aloud).
Each figure is computed twice: a closed form (math.erf, no SciPy) and a second method (a seeded simulation,
a direct sum or a bisection). Exits 0 when every pair agrees and matches the figure the item states.
Run: python3 docs/reports/research-int-1-perf-numbers.py
"""
import json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'research-int', 'homework-1.json')
fails = []

def check(name, a, b, stated, tol_pair, tol_stated):
    ok = abs(a - b) <= tol_pair and abs(a - stated) <= tol_stated
    print(f"{'ok  ' if ok else 'FAIL'} {name}: method 1 {a:.6f}, method 2 {b:.6f}, stated {stated}")
    if not ok:
        fails.append(name)

Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
rng = random.Random(20261105)

# Set-up: annualised Sharpe ratio S over T years has t statistic S * sqrt(T) (normal approximation).
S, T, K, ALPHA = 1.0, 5, 20, 0.05
t = S * math.sqrt(T)
check('t statistic sqrt(5)', t, math.sqrt(5.0), 2.24, 1e-12, 0.005)

# 1. Two-sided p for t = sqrt(5): closed form, then a seeded simulation of |Z| >= t.
p1 = 2 * (1 - Phi(t))
N = 400_000
p2 = sum(abs(rng.gauss(0, 1)) >= t for _ in range(N)) / N
check('two-sided p', p1, p2, 0.025, 0.002, 0.0005)
check('one time in 40 (1/p, p = 0.025 as stated)', 1 / 0.025, 40.0, 40, 1e-12, 0)
# Review R1: p is two-sided, so "one time in 40" counts results this strong either way; "this good" alone (one-sided) is 1 in 79.
one_sided = 1 - Phi(t)
one_sided_sim = sum(rng.gauss(0, 1) >= t for _ in range(N)) / N
check('one-sided p is half the two-sided p (1 time in 79)', one_sided, one_sided_sim, 0.0127, 0.001, 0.0005)
check('one-sided odds, 1 in 79', 1 / one_sided, 1 / one_sided_sim, 79, 4, 0.5)
check('two-sided odds, 1 in 39.5 (stated as 1 in 40)', 1 / p1, 1 / p2, 40, 1.5, 1)

# 2. Power against a true Sharpe of 1 over five years, 5% two-sided (critical value 1.96).
z = 1.959963984540054
pw1 = Phi(t - z) + Phi(-t - z)
pw2 = sum(abs(rng.gauss(t, 1)) >= z for _ in range(N)) / N
check('power, five years', pw1, pw2, 0.61, 0.003, 0.005)
check('miss rate, five years', 1 - pw1, 1 - pw2, 0.39, 0.003, 0.005)

# 3. Twenty unrelated tries: chance the best p is at or below 0.025 with no edge anywhere.
q1 = 1 - (1 - 0.025) ** K
q2 = sum(math.comb(K, j) * 0.025 ** j * 0.975 ** (K - j) for j in range(1, K + 1))
check('chance some try has p <= 0.025', q1, q2, 0.40, 1e-12, 0.005)
# Expected false positives at 5% among twenty, and the chance of at least one.
check('expected false positives at 5%', K * ALPHA, sum(j * math.comb(K, j) * ALPHA ** j * (1 - ALPHA) ** (K - j) for j in range(K + 1)), 1.0, 1e-12, 1e-9)
check('chance of at least one at 5%', 1 - 0.95 ** K, sum(math.comb(K, j) * ALPHA ** j * (1 - ALPHA) ** (K - j) for j in range(1, K + 1)), 0.64, 1e-12, 0.005)

# 4. Bonferroni bar for twenty tries.
check('Bonferroni bar', ALPHA / K, 0.0025, 0.0025, 1e-15, 1e-15)

# 5. Follow-up: years for 80% power at a true Sharpe of 1. Closed form (z_a + z_b)^2, then bisection on the power curve.
zb = 0.8416212335729143
y1 = (z + zb) ** 2
lo, hi = 1.0, 30.0
for _ in range(100):
    mid = (lo + hi) / 2
    if Phi(math.sqrt(mid) - z) + Phi(-math.sqrt(mid) - z) < 0.8:
        lo = mid
    else:
        hi = mid
check('years for 80% power (exact, rounds to about eight)', y1, hi, 8, 0.01, 0.2)
check('t needed on average for 80% power', z + zb, math.sqrt(hi), 2.8, 0.001, 0.005)
check('years from the rounded figures, (1.96 + 0.84)^2', (1.96 + 0.84) ** 2, 2.8 * 2.8, 7.84, 1e-12, 1e-9)

# 6. 0.025 against the Bonferroni bar: ten times too big.
check('ratio to the Bonferroni bar', 0.025 / (ALPHA / K), 0.025 * K / ALPHA, 10, 1e-9, 1e-9)

# 7. Holm and Benjamini-Hochberg as procedures on twenty p-values whose smallest is 0.025.
def holm(ps):
    n = 0
    for k, p in enumerate(sorted(ps)):
        if p > ALPHA / (len(ps) - k): break
        n += 1
    return n
def bh(ps):
    s = sorted(ps)
    return max([k + 1 for k, p in enumerate(s) if p <= ALPHA * (k + 1) / len(s)], default=0)
weak = [0.025] + [rng.uniform(0.051, 1) for _ in range(K - 1)]     # one winner among weak versions
strong = [0.025] + [rng.uniform(0.025, 0.05) for _ in range(K - 1)]  # all twenty under 0.05
half = [0.025] * 1 + [rng.uniform(0.0251, 0.05) for _ in range(9)] + [rng.uniform(0.051, 1) for _ in range(10)]
check('Holm rejects with weak versions', holm(weak), 0, 0, 0, 0)
check('Holm rejects with strong versions', holm(strong), 0, 0, 0, 0)
check('BH rejects with weak versions', bh(weak), 0, 0, 0, 0)
check('BH rejects with all twenty under 0.05', bh(strong), K, 20, 0, 0)
# BH needs some k >= 10 with p_(k) <= k/400 when the smallest is 0.025: brute force over k agrees.
need = min(k for k in range(1, K + 1) if 0.025 <= ALPHA * k / K)
check('BH needs at least this many versions to do well', need, math.ceil(0.025 * K / ALPHA), 10, 0, 0)
check('BH with ten under 0.05 rejects none (half is needed, not enough)', bh(half), 0 if all(p > ALPHA * (k + 1) / K for k, p in enumerate(sorted(half))) else -1, 0, 0, 0)

# 8. The item as authored: rubric sums to 10, clock and follow-ups in range, numbers quoted in the model.
item = next(i for i in json.load(open(HW, encoding='utf-8'))['items'] if i['id'] == 'h1-signal-aloud')
w = item['widget']
pts = sum(r['points'] for r in w['rubric'])
print(f"{'ok  ' if pts == 10 else 'FAIL'} rubric sums to {pts}")
if pts != 10: fails.append('rubric')
if item.get('performance') != 'aloud' or not (15 <= w['seconds'] <= 1800) or not (1 <= len(w['followUps']) <= 5):
    fails.append('aloud shape')
text = w['prompt'] + w['model'] + ' '.join(r['text'] for r in w['rubric']) + item['explain']['text']
for figure in ['up or down', 'either way', '0.025', '0.61', '0.0025', '40', 'four times in ten', 'six times in ten', 'eight years', '2.24', '2.8', '7.84', 'tenfold', 'all twenty are under 0.05']:
    hit = figure in text
    print(f"{'ok  ' if hit else 'FAIL'} the item quotes {figure!r}")
    if not hit: fails.append('quote ' + figure)

req = [bool(r.get('required')) for r in w['rubric']]
print(f"{'ok  ' if req == [True, True, True, False] else 'FAIL'} rubric rows 1 to 3 required, row 4 optional {req}")
if req != [True, True, True, False]: fails.append('required rows')
qok = 'type one line' not in item['question'] and 'Mark button' not in item['question']
print(f"{'ok  ' if qok else 'FAIL'} question carries no notes workaround")
if not qok: fails.append('workaround')
bad = [s for s in ('this good one time', 'this good about four') if s in text]
print(f"{'ok  ' if not bad else 'FAIL'} no 'this good' misreading of the two-sided p {bad}")
if bad: fails.append('this good')
if fails:
    print('FAILED:', ', '.join(fails))
    sys.exit(1)
print('all numbers agree')
