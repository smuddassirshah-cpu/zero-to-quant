def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        assert a in t, (path, a[:70])
        t = t.replace(a, b)
    open(path, 'w').write(t)


sub('build_drills.py', [
    ("[1, 1, 0, 0, 1, 0], [0, 1, 1, 1", "[1, 1, 0, 0, 0, 1], [0, 1, 1, 1"),
    ("([3, 1, 4, 1, 5], 2), ([7, 7, 7], 0)", "([6, 2, 8, 2, 4], 2), ([7, 7, 7], 0)"),
    ("([1, 5, 1, 5], 4)", "([2, 6, 2, 6], 4)"),
    ("assert gap_ref([1, 2] * 100000, 1) == 10 ** 10 and gap_ref([7] * 200000, 0) == 200000 * 199999 // 2 == 19999900000", "assert gap_ref([1, 2] * 100000, 1) == 10 ** 10 and gap_ref([9] * 150000, 0) == 150000 * 149999 // 2 == 11249925000"),
    ('tests.append(pyc("count_pairs_with_gap([7] * 200000, 0)", 19999900000))', 'tests.append(pyc("count_pairs_with_gap([9] * 150000, 0)", 11249925000))'),
    ('pyc("count_pairs_with_gap([3, 1, 4, 1, 5], 2)", 3, "The pairs are 3 and 1 (twice) and 3 and 5. That is three.")', 'pyc("count_pairs_with_gap([6, 2, 8, 2, 4], 2)", 4, "The pairs are 6 with 8, 6 with 4, and 4 with each 2. That is four.")'),
    ("`nums = [3, 1, 4, 1, 5]` and `k = 2` the pairs are 3 with each 1, and 3 with 5, so the answer is 3.", "`nums = [6, 2, 8, 2, 4]` and `k = 2` the pairs are 6 with 8, 6 with 4, and 4 with each 2, so the answer is 4."),
])
print('patched')
