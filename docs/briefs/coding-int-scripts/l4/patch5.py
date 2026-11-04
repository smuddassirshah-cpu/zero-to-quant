def sub(path, pairs):
    t = open(path).read()
    for a, b in pairs:
        assert a in t, (path, a[:80])
        t = t.replace(a, b)
    open(path, 'w').write(t)


sub('b16.py', [
    ("('a', 'They rarely make the special cases, such as an empty list', None),", "('a', 'They seldom make cases such as the empty list', None),"),
    ("('b', 'They always repeat the same list', ", "('b', 'They repeat the same list again and again', "),
    ("('c', 'They are too slow to run', ", "('c', 'They are too slow to run on large inputs', "),
    ("('d', 'They only find bugs in the last run', ", "('d', 'They only find bugs in the last run of a list', "),
])
sub('b18.py', [
    ("('a', 'The total is 0, and the zero entry cannot be divided out of it', None),", "('a', 'The total is 0, so the zero entry cannot be recovered', None),"),
    ("('a', 'Written the plan as comments: left products, right products, no division', None),", "('a', 'Written the plan as comments: two passes, no division', None),"),
    ("('b', 'Typed faster, to leave time to explain', ", "('b', 'Typed faster, to leave time to explain afterwards', "),
    ("('c', 'Explained after the tests pass', ", "('c', 'Explained the code after the tests pass', "),
    ("('d', 'Memorised the solution', ", "('d', 'Memorised the standard solution beforehand', "),
])
sub('b19.py', [
    ("('a', 'Is the end of a booking included, and are the times whole numbers?', None),", "('a', 'Is the end of a booking included?', None),"),
    ("('a', 'A balanced tree over the times that keeps the largest overlap in each part: $O(\\\\log n)$', None),", "('a', 'A tree over the times that keeps the largest overlap per part: $O(\\\\log n)$', None),"),
])
sub('b_hw.py', [
    ("('a', '`[5, 3, -1, -2, 4, 7]`, a stretch in the middle', None),", "('a', '`[5, 3, -1, -2, 4, 7]`', None),"),
])
sub('b_rev.py', [
    ("Their remainders are 0, 0, 1, 1, 0, 2 and 3. Three prefixes share 0, giving 3 pairs, and two share 1, giving 1 pair. The total is 4.", "Their remainders are 0, 0, 1, 1, 0, 2 and 3. Three prefixes share 0 and two share 1, so the pairs number 3 + 1 = 4."),
])
print('ok')
