"""Recompute every figure of coding-int homework-4 item h4-pairs-aloud (performance task, L4).

Each number in the prompt, model, rubric and follow-ups is computed by two independent routes.
The model's code is pulled out of the model text and checked against a brute force and a
sort-and-two-pointers version on seeded random lists, and the many-targets formula of
follow-up 2 is checked the same way. Run: python3 -I docs/reports/coding-int-4-perf-numbers.py
"""
import itertools, json, math, os, random, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'coding-int', 'homework-4.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h4-pairs-aloud']
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
model = w['model']
print('item index (1-based):', idx[0] + 1, 'of', len(items))


def brute(sizes, target):
    return sum(1 for a, b in itertools.combinations(sizes, 2) if a + b == target)


def two_pointers(sizes, target):
    s = sorted(sizes)
    i, j, total = 0, len(s) - 1, 0
    while i < j:
        v = s[i] + s[j]
        if v < target:
            i += 1
        elif v > target:
            j -= 1
        elif s[i] == s[j]:
            k = j - i + 1
            total += k * (k - 1) // 2
            break
        else:
            a = i
            while i < j and s[i] == s[a]:
                i += 1
            b = j
            while j >= i and s[j] == s[b]:
                j -= 1
            total += (i - a) * (b - j)
    return total


def many_targets(counts, t):
    total = 0
    for v, c in counts.items():
        u = t - v
        if v < u:
            total += c * counts.get(u, 0)
        elif v == u:
            total += c * (c - 1) // 2
    return total


# 1. The model's code, run as written.
m = re.search(r"```python\n(.*?)\n```", model, re.S)
check(m is not None, 'model holds one python block')
ns = {}
exec(m.group(1), ns)
count_pairs = ns['count_pairs']

# 2. Example: answer 5, three routes plus the hand count 1 + 1 + 3.
ex = [4, 6, 5, 5, 1, 9, 5]
check('`[4, 6, 5, 5, 1, 9, 5]` with target 10 gives 5' in model, 'model states the example and 5')
vals = (count_pairs(ex, 10), brute(ex, 10), two_pointers(ex, 10))
check(vals == (5, 5, 5), f'example: model code, brute, two pointers = {vals}')
check(1 + 1 + math.comb(3, 2) == 5 and 3 * 2 // 2 == 3, 'hand count 4+6, 1+9, three 5s give 3: total 5')

# 3. Brute-force count at n = 200,000.
n = 200_000
a, b = n * (n - 1) // 2, math.comb(n, 2)
check(a == b == 19_999_900_000, f'n(n-1)/2 at 200,000 = {a:,} (comb {b:,})')
check('19,999,900,000' in model, 'model prints 19,999,900,000')
check(abs(a / 2e10 - 1) < 0.001, 'about 2 x 10^10')
check('200,000' in w['prompt'], 'prompt names 200,000')

# 4. int limit in follow-up 3.
check(2**31 - 1 == 2_147_483_647 == int('1' * 31, 2), 'int max 2,147,483,647 two ways')
check(a > 2**31 - 1, 'answer can exceed an int')
check('2,147,483,647' in model, 'model prints the int limit')

# 5. Random checks: model code, brute force, two pointers, many-targets formula.
rng = random.Random(4)
bad = 0
for trial in range(3000):
    size = rng.randrange(0, 30)
    xs = [rng.randrange(-6, 12) for _ in range(size)]
    t = rng.randrange(-8, 20)
    r = (count_pairs(xs, t), brute(xs, t), two_pointers(xs, t), many_targets(Counter(xs), t))
    if len(set(r)) != 1:
        bad += 1
check(bad == 0, f'3000 random lists: four routes agree ({bad} disagreements)')

# 6. Counts and shape the brief asks for.
check(w['seconds'] == 600 and w['think'] == 60, 'seconds 600 (10 minutes), think 60')
check(len(w['followUps']) == 3, '3 follow-ups')
check('1,000' in w['followUps'][1], 'follow-up 2 names 1,000 targets')
rub = w['rubric']
check(sum(r['points'] for r in rub) == 10 and 3 <= len(rub) <= 5, f'rubric {len(rub)} rows sum to 10')
# 702 sweep: row 4 (the typed code) is now required with row 3; rows 1, 2 and 5 are optional in the prompt
check(sum(1 for r in rub if r.get('required')) == 2, 'two required rows')
check(len(items) == 9 and sum(1 for it in items if it.get('performance')) == 1, 'homework-4 holds 9 items, one performance item')

print('failures:', fails)
sys.exit(1 if fails else 0)
