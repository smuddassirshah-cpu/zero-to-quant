import sys
sys.path.insert(0, '.')
import refs4 as R
assert R._ref([8, 8, 3, 8, 8, 8]) == R.streak_brute([8, 8, 3, 8, 8, 8]) == 3
first_run = lambda xs: next((len(list(g)) for _, g in __import__('itertools').groupby(xs)), 0)
assert first_run([1, 4, 4]) == 1 and R._ref([1, 4, 4]) == 2
assert first_run([4, 4, 1]) == R._ref([4, 4, 1]) == 2 and first_run([5, 5, 5]) == 3 and first_run([7]) == 1
# l17 quiz: [5, -3, 3] zero-sum stretch
assert R.lzs([5, -3, 3]) == R.lzs_slow([5, -3, 3]) == 2
# l17 trap example [4, -4, 3, -3]
assert R.lzs([4, -4, 3, -3]) == 4
# l18
assert R.pes([3, 4, 5]) == [20, 15, 12]
assert 100000 * 99999 == 9999900000 and 50000 * 49999 == 2499950000
assert R.pes([3, 0, 2]) == [0, 6, 0] and R.pes([4, 0, 5]) == [0, 20, 0]
assert R.pes([2, 3, 4, 5]) == [60, 40, 30, 24]
# l17 S1, quiz
assert 60 - 5 - 28 - 5 == 22 and 90 - 6 - 8 - 37 == 39 and 60 - 5 - 5 - 31 == 19
# l15 S2/S3/S9/S10
LP = [[40, 20, 12, 6], [60, 35, 25, 12], [90, 50, 30, 18]]
assert R.best_plan(LP, 62) == R.best_plan_brute(LP, 62) == 115 and R.greedy_ppm(LP, 62) == 100
assert R.best_plan(LP, 60) == R.best_plan_brute(LP, 60) == 102
assert R.best_plan([[50, 40, 20, 12], [60, 45, 25, 15]], 55) == 75
# l15 S3: the plan P2 partial + P3 full
assert 12 + 50 == 62 and 25 + 90 == 115
# l19
assert R.run_a(1, [[0, 1, 4], [0, 3, 6], [0, 4, 8], [0, 0, 1]]) == [True, False, True, True]
assert R.run_bc(2, [[0, 1, 4], [0, 3, 6], [0, 2, 5], [0, 4, 8]]) == [True, True, False, True]
# stage C: the three lessons' tests all pass the reference (cumulative)
for k, ops, e in R.CAL_A + R.CAL_B + R.CAL_C:
    assert R.run_bc(k, ops) == e
# h2 and h5
assert sum(range(1200)) == 1200 * 1199 // 2 == 719400
assert 80000 * 1500 == 120000000 and 80000 // 5 == 16000 and 1500 * 5 == 7500
assert (10 ** 6 - 1).bit_length() == 20 and 2 ** 19 < 10 ** 6 < 2 ** 20
# h3 numbers
import b_hw
for xs, e in b_hw.H3_SMALL:
    assert R.lzs(xs) == R.lzs_slow(xs) == e, xs
assert R.lzs([2, -2] * 150000) == 300000
assert R.lzs([3, 1, -4] * 120000 + [6]) == 360000
assert R.lzs([3, 1, -4] * 40 + [6]) == R.lzs_slow([3, 1, -4] * 40 + [6]) == 120
assert R.lzs([2, -2] * 30) == R.lzs_slow([2, -2] * 30) == 60
print('final checks OK')
