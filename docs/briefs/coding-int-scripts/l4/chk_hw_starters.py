import sys
sys.path.insert(0, '.')
import refs4 as R
import b_hw
p1 = R.load_lb(R.LB_P1_STARTER)
p3 = R.load_lb(R.LB_P3_STARTER)
rows1 = [(o, e) for o, e in R.LB_P1]
rows3 = [(o, e) for o, e in [R.LB_P3[0], R.LB_P3[3]] + b_hw.LB_EXTRA]
print('part 1 starter fails', sum(p1(o) != e for o, e in rows1), 'of', len(rows1))
print('part 3 starter fails own', sum(p3(o) != e for o, e in rows3), 'of', len(rows3), '; merged with part 1 rows', sum(p3(o) != e for o, e in rows3 + rows1), 'of', len(rows3 + rows1))
sol3 = R.load_lb(R.LB_P3_SOL)
print('part 3 solution merged', all(sol3(o) == e for o, e in rows3 + rows1))
