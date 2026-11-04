import sys
sys.path.insert(0, '.')
import refs4 as R
print('S1', R.run_a(1, [[0, 1, 4], [0, 3, 6], [0, 4, 8], [0, 0, 1]]), R.run_bc(1, [[0, 1, 4], [0, 3, 6], [0, 4, 8], [0, 0, 1]]), R.cal_brute(1, [[0, 1, 4], [0, 3, 6], [0, 4, 8], [0, 0, 1]]))
ops = [[0, 2, 5], [0, 5, 7], [0, 4, 6], [0, 7, 9], [0, 0, 2]]
print('S4', R.run_a(1, ops), R.cal_brute(1, ops))
ops = [[0, 1, 4], [0, 3, 6], [0, 2, 5], [0, 4, 8]]
print('S6', R.run_bc(2, ops), R.cal_brute(2, ops))
ops = [[0, 9, 12], [0, 12, 15], [2, 3, 9], [2, 2, 9], [1, 9, 12], [2, 3, 9]]
print('S8', R.run_bc(1, ops), R.cal_brute(1, ops))
ops = [[0, 2, 6], [0, 6, 9]]
print('q1', R.run_bc(1, ops), R.cal_brute(1, ops))
ops = [[0, 0, 5], [0, 3, 8], [0, 4, 6]]
print('q2', R.run_bc(2, ops), R.cal_brute(2, ops))
ops = [[0, 4, 7], [0, 7, 9], [2, 2, 5]]
print('q3', R.run_bc(1, ops), R.cal_brute(1, ops))
# review 9, 10
ops = [[0, 5, 9], [0, 8, 12], [0, 9, 13], [0, 13, 15], [0, 12, 14]]
print('rev9', R.run_a(1, ops), R.cal_brute(1, ops))
ops = [[0, 10, 20], [0, 26, 40], [2, 6, 10]]
print('rev10', R.run_bc(1, ops), R.cal_brute(1, ops))
