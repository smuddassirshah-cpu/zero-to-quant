"""Numbers for the fixes proposed in docs/reviews/review-exam-mock-oa-sig-versions.md, each computed twice.
Run: python -I docs/reviews/exam-mock-oa-sig-versions-scripts/fix_numbers.py   (exit 0 when all hold)
"""
import itertools, random, sys
from fractions import Fraction as F
fails = []
def ok(c, m):
    if not c: fails.append(m)
rng = random.Random(7)

# Finding 2: v2 q04 replacement, two random swaps of five cards in order
pairs = list(itertools.combinations(range(5), 2))
tot = 0
for a, b in itertools.product(pairs, repeat=2):
    p = list(range(5))
    for i, j in (a, b):
        p[i], p[j] = p[j], p[i]
    tot += sum(p[k] == k for k in range(5))
key = F(tot, len(pairs) ** 2)
closed = 5 * (F(3, 5) ** 2 + F(2, 5) * F(1, 10))
ok(key == closed == 2, f'swap key {key} {closed}')
ok(5 * F(3, 5) ** 2 == F(9, 5) and 5 * F(3, 5) == 3, 'swap slips 1.80 and 3.00')
ok(F(sum(sum(p[k] == k for k in range(5)) for p in itertools.permutations(range(5))), 120) == 1, 'full shuffle 1')

# Finding 3: v2 q07 replacement, you toss 3 times, colleague 2 times, chance you get strictly more heads
outs = list(itertools.product((0, 1), repeat=5))
more = F(sum(sum(o[:3]) > sum(o[3:]) for o in outs), 32)
tie = F(sum(sum(o[:3]) == sum(o[3:]) for o in outs), 32)
ok(more == F(1, 2) and tie == F(5, 16) and more + tie == F(13, 16), f'coins {more} {tie}')
# second route: lead after two each, then the third toss settles a tie half the time
two = list(itertools.product((0, 1), repeat=4))
tie2 = F(sum(sum(o[:2]) == sum(o[2:]) for o in two), 16)
ok((1 - tie2) / 2 + tie2 / 2 == F(1, 2) and tie2 == F(3, 8), 'coins second route')
ok(abs(F(3, 5) - F(1, 2)) > F(1, 100), 'coins 3/5 slip distinct')

# Finding 4: v3 q13 replacement, one failed search then the chance the next search finds it
pa, find = F(3, 5), F(4, 5)
post = pa * (1 - find) / (pa * (1 - find) + 1 - pa)
pred = post * find
ok(post == F(3, 13) and pred == F(12, 65), f'search {post} {pred}')
ok(F(96, 520) == pred and pa * find == F(12, 25), 'search natural frequencies and prior slip')
n = hit = 0
for _ in range(400000):
    inA = rng.random() < 0.6
    if inA and rng.random() < 0.8:
        continue                      # found on the first search: not in the conditioned set
    n += 1
    hit += inA and rng.random() < 0.8
ok(abs(hit / n - float(pred)) < 0.004, f'search simulation {hit / n}')
vals = [F(12, 65), F(12, 25), F(3, 13), F(4, 5)]
ok(all(abs(a - b) > F(1, 100) for a, b in itertools.combinations(vals, 2)), 'search options apart')

# Finding 5: v3 q11 options, replace "1" by the q-for-q-squared slip over two generations
q2 = F(1, 4) + F(1, 4) * F(1, 4) + F(1, 2) * F(1, 4) ** 2
slip = F(1, 4) + F(1, 4) * F(1, 4) + F(1, 2) * F(1, 4)
ok(q2 == F(11, 32) and slip == F(7, 16), 'extinction options')
vals = [F(1, 2), F(1, 4), F(11, 32), F(7, 16)]
ok(all(abs(a - b) > F(1, 100) for a, b in itertools.combinations(vals, 2)), 'extinction options apart')

if fails:
    print('\n'.join(fails)); sys.exit(1)
print('OK: fix numbers hold')
