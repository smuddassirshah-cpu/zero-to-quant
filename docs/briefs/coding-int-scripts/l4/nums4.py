"""Numbers for the level 4 lessons, review and homework, each computed by two methods."""
import itertools, random, sys
sys.path.insert(0, '.')
import refs4 as R

# --- l16 trap: which bugs survive random lists
rnd = random.Random(7)
N = 1000
surv = {n: 0 for n in R.MUT}
for n, f in R.MUT.items():
    caught = 0
    rr = random.Random(11)
    for _ in range(N):
        L = rr.randint(5, 50)
        xs = [rr.randint(0, 9) for _ in range(L)]
        if f(xs) != R._ref(xs):
            caught += 1
    print(n, 'caught by random lists (len 5-50, values 0-9):', caught, 'of', N)
for n, f in R.MUT.items():
    caught = 0
    rr = random.Random(11)
    for _ in range(N):
        L = rr.randint(5, 50)
        xs = [rr.randint(0, 2) for _ in range(L)]
        if f(xs) != R._ref(xs):
            caught += 1
    print(n, 'values 0-2:', caught)
# fraction of empty lists with length 0..10
print('empty fraction lengths 0..10:', 1 / 11)

# --- l15 quiz and review and homework sets
def show(name, ps, b):
    best = R.best_plan(ps, b)
    brute = R.best_plan_brute(ps, b)
    g = R.greedy_ppm(ps, b)
    assert best == brute
    print(name, ps, b, 'best', best, 'greedy', g)

# l15 S10 (two problems, 55)
show('S10', [[50, 40, 20, 12], [60, 45, 25, 15]], 55)
# review sets
show('rev1', [[24, 12, 8, 4], [45, 25, 18, 10], [70, 40, 22, 14]], 50)
show('rev1b', [[36, 20, 14, 8], [48, 30, 16, 9], [75, 44, 30, 15]], 56)
show('rev1c', [[36, 20, 14, 8], [48, 30, 16, 9], [75, 44, 30, 15]], 52)
show('hw7', [[28, 16, 9, 5], [54, 32, 21, 11], [80, 46, 26, 14]], 58)
show('hw7b', [[28, 16, 9, 5], [54, 32, 21, 11], [80, 46, 26, 14]], 54)
# quiz
print('quiz 1', 36 / 24, 28 / 14)
print('quiz 2', 80 - 5 - 5)
print('2000^2', 2000 ** 2, '300000^2', 300000 ** 2)

# l17 review
xs = [8, -3, 4, 7, -6, 5]
print('rev6', R.csdk(xs, 4), R.csdk_slow(xs, 4))
print('n(n+1)/2 n=250000', 250000 * 250001 // 2)
# longform example candidates
for xs, k in [([7, -2, 9, 4, -5, 6], 5), ([9, 4, -8, 3, 7, -2], 5), ([4, 9, -6, 2, 8, -3], 5), ([3, 8, -5, 6, 1, 9], 4)]:
    print('longform', xs, k, R.csdk(xs, k), R.csdk_slow(xs, k))
# quiz l17: minutes left
# review 8
print('pes [1,2,3,4]', R.pes([1, 2, 3, 4]))
# review 9 calendar
print('rev9', R.run_a(1, [[0, 5, 9], [0, 8, 12], [0, 9, 13], [0, 13, 15], [0, 12, 14]]))
# review 10
print('rev10', R.run_bc(1, [[0, 10, 20], [0, 26, 40], [2, 6, 10]]))
# review 3 / 4 second_largest
def second_largest(xs):
    d = sorted(set(xs), reverse=True)
    return d[1] if len(d) > 1 else None
print('rev4', second_largest([4, 4, 3, 3, 1]), second_largest([]), second_largest([5]), second_largest([5, 5]), second_largest([2, 2, 1]), second_largest([3, 1, 2]))
# hw 2
print('hw2 p1', sum(range(1000)), 1000 * 999 // 2, 'p3', (10 ** 6 - 1).bit_length(), (10 ** 6).bit_length())
import math
print('log2 1e6', math.log2(10 ** 6), math.ceil(math.log2(10 ** 6)))
# hw 5
print('hw5', 100000 * 2000, 100000 // 10)
# hw 8
print('hw8 key', R.lzs([5, 3, -1, -2, 4, 7]), R.lzs_slow([5, 3, -1, -2, 4, 7]))
