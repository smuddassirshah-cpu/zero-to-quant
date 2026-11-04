import sys
sys.path.insert(0, '.')


def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        assert a in t, (path, a[:70])
        t = t.replace(a, b)
    open(path, 'w').write(t)


sub('b_rev.py', [
    ("assert R.pes([1, 2, 3, 4]) == [24, 12, 8, 6]", "assert R.pes([2, 1, 3, 4]) == [12, 24, 8, 6]"),
    ("`product_except_self([1, 2, 3, 4])`?", "`product_except_self([2, 1, 3, 4])`?"),
    ("'8: 1 x 2 x 4'", "'8: 2 x 1 x 4'"),
    ("The product of 1, 2 and 4 is 8.", "The product of 2, 1 and 4 is 8."),
    ("The others are 1, 2 and 4, and their product is 8. The full answer is `[24, 12, 8, 6]`.", "The others are 2, 1 and 4, and their product is 8. The full answer is `[12, 24, 8, 6]`."),
    ("'left', 2), ('whole', 24)", "'left', 2), ('whole', 24)"),
])
sub('b_hw.py', [
    ("A calendar takes 1,000 bookings, one at a time.", "A calendar takes 1,200 bookings, one at a time."),
    ("numeric(499500, 'Comparisons', '499,500: 0 + 1 + ... + 999', [('square', 1000000), ('once', 1000)])", "numeric(719400, 'Comparisons', '719,400: 0 + 1 + ... + 1,199', [('square', 1440000), ('once', 1200)])"),
    ('"$0 + 1 + \\\\dots + 999 = 499{,}500$."', '"$0 + 1 + \\\\dots + 1{,}199 = 719{,}400$."'),
    ("The first booking scans none and the last scans 999.", "The first booking scans none and the last scans 1,199."),
    ("You multiplied 1,000 by 1,000. The list starts empty and grows.", "You multiplied 1,200 by 1,200. The list starts empty and grows."),
    ("The total is $0 + 1 + \\\\dots + 999 = 1{,}000 \\\\times 999 / 2 = 499{,}500$.", "The total is $0 + 1 + \\\\dots + 1{,}199 = 1{,}200 \\\\times 1{,}199 / 2 = 719{,}400$."),
])
sub('b16.py', [
    ("`[1, 1]`, `[2, 1]`, `[1, 2, 2]` and `[5, 5, 5, 1]`.", "`[1, 1]`, `[2, 1]`, `[1, 2, 2]` and `[6, 6, 6, 1]`."),
])
sub('build_drills.py', [
    ("[1, 1, 0, 0, 1, 0], [0, 0, 0]", "[1, 1, 0, 0, 0, 1], [0, 0, 0]"),
    ("([3, 1, 4, 1, 5], 2), ([7, 7, 7], 0)", "([6, 2, 8, 2, 4], 2), ([7, 7, 7], 0)"),
    ("([1, 5, 1, 5], 4)", "([2, 6, 2, 6], 4)"),
    ("assert gap_ref([1, 2] * 100000, 1) == 10 ** 10 and gap_ref([7] * 200000, 0) == 200000 * 199999 // 2 == 19999900000", "assert gap_ref([1, 2] * 100000, 1) == 10 ** 10 and gap_ref([9] * 150000, 0) == 150000 * 149999 // 2 == 11249925000"),
    ('tests.append(pyc("count_pairs_with_gap([7] * 200000, 0)", 19999900000))', 'tests.append(pyc("count_pairs_with_gap([9] * 150000, 0)", 11249925000))'),
    ('pyc("count_pairs_with_gap([3, 1, 4, 1, 5], 2)", 3, "The pairs are 3 and 1 (twice) and 3 and 5. That is three.")', 'pyc("count_pairs_with_gap([6, 2, 8, 2, 4], 2)", 4, "The pairs are 6 with 8, 6 with 4, and 4 with each 2. That is four.")'),
    ("`nums = [3, 1, 4, 1, 5]` and `k = 2` the pairs are 3 with each 1, and 3 with 5, so the answer is 3.", "`nums = [6, 2, 8, 2, 4]` and `k = 2` the pairs are 6 with 8, 6 with 4, and 4 with each 2, so the answer is 4."),
    ("Answers can pass $10^{10}$.", "Answers can pass $10^{10}$."),
])
print('patched')
