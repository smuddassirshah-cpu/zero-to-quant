from lib2 import *
import refs4 as R

SK = ['ci-timed']
SKD = ['ci-timed', 'ci-design']


def build():
    items = []
    # 1 l15 best plan 92
    P = [[36, 20, 14, 8], [48, 30, 16, 9], [75, 44, 30, 15]]
    assert R.best_plan(P, 56) == R.best_plan_brute(P, 56) == 92
    assert R.greedy_ppm(P, 56) == 84
    items.append(item('r4-best-plan', 3, SK, ['partial-credit'], "Problems are `(36, 20, 14, 8)`, `(48, 30, 16, 9)` and `(75, 44, 30, 15)`: full points, full minutes, partial points, partial minutes. The budget is 56 minutes. What is the most points a plan can earn?",
                      numeric(92, 'Points', '92: the second in full, the third in part, the first in part', [('p3', 91), ('greedy', 84)]),
                      fb("$48 + 30 + 14 = 92$ in 53 minutes.", "Not quite right. Mix full and partial across all three.",
                         {'p3': "You took the third in full and the second in part, 91. Mixing the other way earns 1 more.", 'greedy': "That is the full-marks plan by rate. Partials fill the gap and earn 8 more."}),
                      explain("The second in full takes 30 minutes, the third in part 15 and the first in part 8. That is 53 minutes and $48 + 30 + 14 = 92$ points. The third in full with a partial earns at most 91.")))
    # 2 l15 greedy 84
    items.append(item('r4-greedy', 3, SK, ['oa-triage'], "The same problems and budget of 56 minutes. Take whole problems only, in order of points per minute. Skip one that does not fit and go on. How many points?",
                      numeric(84, 'Points', '84: the first and the second in full', [('three', 159), ('two', 111)]),
                      fb("The first (20 minutes) and the second (30 minutes) earn $36 + 48 = 84$.", "Not quite right. The order is the first, the third, then the second.",
                         {'three': "You took all three. They need 94 minutes.", 'two': "You took the first and the third. They need 64 minutes, over 56."}),
                      explain("The rates are 1.8, 1.6 and 1.70, so the order is first, third, second. After the first, 36 minutes are left and the third needs 44, so it is skipped. The second fits, and the total is 84.")))
    # 3 l16 multi
    items.append(item('r4-edge-second', 3, SK, ['edge-case-list'], "`second_largest(xs)` returns the second largest distinct value, or `None` if there are fewer than two distinct values. Select all that apply: which inputs are edge cases worth a test?",
                      multi([('a', '`[]`', None), ('b', '`[5]`', None), ('c', '`[5, 5]`', None), ('d', '`[3, 1, 2]`', "You chose an ordinary list. It has three distinct values and no special feature."), ('e', '`[2, 2, 1]`', None)]),
                      fb("`[]`, `[5]`, `[5, 5]` and `[2, 2, 1]` are the edges.", "Not quite right. Look for fewer than two distinct values, or repeats at the top.",
                         {'d': "`[3, 1, 2]` is an ordinary list. It exposes no special slip."}),
                      explain("The empty list, one number and equal numbers have fewer than two distinct values. `[2, 2, 1]` repeats the top value, so a version that sorts and takes the second entry returns 2, not 1.")))
    # 4 l16 numeric 3
    items.append(item('r4-edge-value', 3, SK, ['edge-case-list'], "What is `second_largest([4, 4, 3, 3, 1])`?",
                      numeric(3, 'Value', '3: the second distinct value', [('four', 4), ('one', 1)]),
                      fb("The distinct values are 4, 3 and 1, so the second largest is 3.", "Not quite right. Count distinct values only.",
                         {'four': "You took the second 4. It is the same value, not a new one.", 'one': "You took the last value. The second largest is 3."}),
                      explain("Repeats do not count. The distinct values in order are 4, 3 and 1, so the second largest is 3.")))
    # 5 l17 minutes left 19
    items.append(item('r4-minutes', 2, SK, ['timed-plan'], "A 60-minute plan keeps 5 minutes for reading and 5 for testing. The first problem took 31 minutes. How many minutes are left for the second?",
                      numeric(19, 'Minutes', '19: 60 minus 5, 5 and 31', [('plan', 25), ('notest', 24)]),
                      fb("$60 - 5 - 5 - 31 = 19$.", "Not quite right. Take the reading, the testing and the first problem from 60.",
                         {'plan': "You used the planned 25 minutes. The first problem ran 6 over.", 'notest': "You left out one of the two 5-minute blocks."}),
                      explain("The reading, the testing and the first problem use 5, 5 and 31 minutes. Of 60, that leaves 19.")))
    # 6 l17 count 4
    xs = [8, -3, 4, 7, -6, 5]
    assert R.csdk(xs, 4) == R.csdk_slow(xs, 4) == 4
    items.append(item('r4-count', 3, SK, ['prefix-sum-count'], "What is `count_subarrays_divisible_by_k([8, -3, 4, 7, -6, 5], 4)`?",
                      numeric(4, 'Subarrays', '4: prefix remainders 0, 0, 1, 1, 0, 2, 3', [('zero', 3), ('five', 5)]),
                      fb("The prefix remainders are 0, 0, 1, 1, 0, 2 and 3, which give $3 + 1 = 4$ pairs.", "Not quite right. Count pairs of prefixes with the same remainder.",
                         {'zero': "You counted only the pairs with remainder 0. The two prefixes with remainder 1 also bound a subarray.", 'five': "You counted one pair too many. Check each remainder class."}),
                      explain("The prefix sums, with the empty start, are 0, 8, 5, 9, 16, 10 and 15. Their remainders are 0, 0, 1, 1, 0, 2 and 3. Three prefixes share 0 and two share 1, so the pairs number 3 + 1 = 4.")))
    # 7 l17 complexity read
    n = 250000
    assert n * (n + 1) // 2 == 31250125000
    items.append(item('r4-steps', 3, SK, ['complexity-read'], "The slow count loops from each start to each end: $n(n + 1) / 2$ inner steps. How many steps is that for $n = 250{,}000$?",
                      numeric(31250125000, 'Steps', '31,250,125,000', [('square', 62500000000), ('half', 31250000000)]),
                      fb("$250{,}000 \\times 250{,}001 / 2 = 31{,}250{,}125{,}000$.", "Not quite right. Multiply $n$ by $n + 1$, then halve.",
                         {'square': "You used $n^2$ and forgot to halve.", 'half': "You halved $n^2$. The count is $n(n + 1) / 2$, which is a little more."}),
                      explain("The inner loop runs $n$ times for the first start, $n - 1$ for the next, and so on. The total is $n(n + 1) / 2$, which here is 31,250,125,000. That is far beyond $10^8$ steps a second.")))
    # 8 l18
    assert R.pes([2, 1, 3, 4]) == [12, 24, 8, 6]
    items.append(item('r4-product', 3, SK, ['product-except-self'], "What is entry 2 (counting from 0) of `product_except_self([2, 1, 3, 4])`?",
                      numeric(8, 'Entry', '8: 2 x 1 x 4', [('left', 2), ('whole', 24)]),
                      fb("The product of 2, 1 and 4 is 8.", "Not quite right. Leave out the entry at index 2, which is 3.",
                         {'left': "You took the left product only. The right entry 4 also counts.", 'whole': "You took the whole product. The entry itself must be left out."}),
                      explain("Index 2 holds the 3. The others are 2, 1 and 4, and their product is 8. The full answer is `[12, 24, 8, 6]`.")))
    # 9 l19
    ops = [[0, 5, 9], [0, 8, 12], [0, 9, 13], [0, 13, 15], [0, 12, 14]]
    assert R.run_a(1, ops) == R.cal_brute(1, ops) == [True, False, True, True, False]
    items.append(item('r4-bookings', 3, SKD, ['calendar-booking'], "`Calendar()` accepts one booking at a time and the bookings are half-open. It books `[5, 9)`, `[8, 12)`, `[9, 13)`, `[13, 15)` and `[12, 14)` in that order. How many are accepted?",
                      numeric(3, 'Accepted', '3: `[5, 9)`, `[9, 13)` and `[13, 15)`', [('all', 5), ('two', 2)]),
                      fb("`[5, 9)`, `[9, 13)` and `[13, 15)` are accepted.", "Not quite right. Compare each booking with the accepted ones only.",
                         {'all': "You accepted every booking. `[8, 12)` overlaps `[5, 9)` at 8.", 'two': "You refused one too many. `[13, 15)` only touches `[9, 13)`."}),
                      explain("`[8, 12)` starts inside `[5, 9)` and is refused. `[9, 13)` and `[13, 15)` touch the accepted bookings without overlapping. `[12, 14)` overlaps both and is refused, so three are accepted.")))
    # 10 l19
    ops = [[0, 10, 20], [0, 26, 40], [2, 6, 10]]
    assert R.run_bc(1, ops)[-1] == 20 == R.cal_brute(1, ops)[-1]
    items.append(item('r4-next-free', 3, SKD, ['calendar-booking'], "With `k = 1`, `[10, 20)` and `[26, 40)` are booked. What does `next_free(6, 10)` return?",
                      numeric(20, 'Start', '20: a booking of 6 from 20 ends at 26', [('ten', 10), ('forty', 40)]),
                      fb("A booking of 6 from 20 ends at 26, where the next booking starts.", "Not quite right. Try `after` and each later end.",
                         {'ten': "A booking at 10 overlaps `[10, 20)`.", 'forty': "You went past the gap. From 20, a booking of 6 fits before 26."}),
                      explain("A start at 10 overlaps `[10, 20)`. The next candidate is 20, where a booking of 6 runs to 26 and just fits before `[26, 40)`.")))
    return {"id": "review-4", "course": "coding-int", "level": 4, "timed": {"seconds": 900, "lockAtZero": False}, "items": items}
