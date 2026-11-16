"""Numbers of the fixes proposed in review-problems-validation-1-3.md. Exit 0 when all hold."""
import sys
from math import sqrt, asin, pi
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
bad = 0
def ok(c, label):
    global bad
    if not c:
        bad += 1
        print('FAIL', label)
# finding 1
ok(round(1.766 * 0.0468, 4) == 0.0826 and round(0.81 - 0.0826, 3) == 0.727, 'rents 0.0826')
# finding 7: 1,440 days, TimeSeriesSplit(7)
sp = list(TimeSeriesSplit(n_splits=7).split(np.zeros(1440)))
ok(all(len(te) == 180 for _, te in sp) and (sp[4][1][0], sp[4][1][-1]) == (900, 1079), 'break: blocks of 180; fold 5 tests 900 to 1,079')
se = sqrt(0.25 / 180)
ok(round(se, 4) == 0.0373 and round(0.25 / 180, 5) == 0.00139 and round(sqrt(0.25 / 1440), 4) == 0.0132, 'break: se 0.0373, variance 0.00139, all-days 0.0132')
ok(abs(0.0014 - 0.00139) <= 5e-5 and abs(0.0373 - se) <= 5e-5, 'break: 4-place roundings inside the bands')
for s in (0.0373, se):
    ok(round((0.470 - 0.52) / s, 1) == -1.3, 'break: fold 6 at -1.3')
    ok(round((0.470 - 0.5825) / s, 1) == -3.0, 'break: earlier level -3.0')
for s in (0.0132, sqrt(0.25 / 1440)):
    ok(round((0.470 - 0.52) / s, 1) == -3.8, 'break: carried -3.8')
ok(1440 - 900 == 540 and 3 * 180 == 540, 'break: newest 540 days')
# finding 10
ok(18 - 3 - 2 == 13, 'spread: before-only with the embargo is 13')
# finding 9
ok(29 - 14 == 15, 'label: 15 more rows clear rows e+14 to e+28')
# finding 13
train = [14, 18, 16, 21, 19, 17, 22, 20, 15]
ok(sum(v > 21 for v in train) == 1 and sum(v > 18 for v in train) == 4 and sum(v >= 21 for v in train) == 2 and sum(v <= 21 for v in train) == 8, 'flows: 1 above 21, 4 above 18, 2 at or above 21')
# finding 16
ok(round(asin(0.1429), 4) == 0.1434 and round(asin(0.1429) / pi, 4) == 0.0456 and round(0.5 + asin(0.1429) / pi, 4) == 0.5456, 'encoding: arcsin form')
print('proposed.py:', 'all hold' if not bad else f'{bad} failed')
sys.exit(1 if bad else 0)
