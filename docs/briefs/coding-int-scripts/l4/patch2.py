s = open('b15.py').read()
a = 'table_w(["Solution", "n up to 1,000", "n up to 100,000", "n up to 1,000,000"], [\n            ["`O(n^2)`", ed(\'Yes\', [\'y\']), ed(\'No\', [\'n\']), ed(\'No\', [\'n\'])],\n            ["`O(n log n)`", ed(\'Yes\', [\'y\']), ed(\'Yes\', [\'y\']), ed(\'Yes\', [\'y\'])],\n            ["`O(n)`", '
b = 'table_w(["Solution", "Group 1", "Group 2", "Group 3"], [\n            ["O(n^2)", ed(\'Yes\', [\'y\']), ed(\'No\', [\'n\']), ed(\'No\', [\'n\'])],\n            ["O(n log n)", ed(\'Yes\', [\'y\']), ed(\'Yes\', [\'y\']), ed(\'Yes\', [\'y\'])],\n            ["O(n)", '
assert a in s
s = s.replace(a, b)
open('b15.py', 'w').write(s)

t = open('b16.py').read()
i0 = t.index('        table_w(["Family", "Call", "Expected"], [')
i1 = t.index('        hints("Each call is the edge of its family')
new = '''        table_w(["Call", "Expected"], [
            ['`longest_run("")`', ed(0)], ['`longest_run("zzz")`', ed(3)],
            ["`blocks([[1, 2], [2, 3]])`", ed(1)], ["`blocks([[1, 9], [3, 4]])`", ed(1)],
            ["`digits(0)`", ed(1)], ["`digits(-45)`", ed(2)]]),
'''
t = t[:i0] + new + t[i1:]
pairs = [
    ("Edge inputs come in families: arrays, strings, intervals and numbers. For each, work out the answer.", "Edge inputs come in families: strings, then intervals, then numbers. For each call, work out the answer."),
    ('"merged_count(spans): how many blocks the closed intervals merge into.",', '"blocks(spans): how many blocks the closed intervals merge into.",'),
    ('"digit_count(n): how many digits the whole number n has, ignoring its sign."', '"digits(n): how many digits the whole number n has, ignoring its sign."'),
    ("'r0c2': \"An empty string", "'r0c1': \"An empty string"),
    ("'r1c2': \"Three equal", "'r1c1': \"Three equal"),
    ("'r2c2': \"Closed intervals that touch", "'r2c1': \"Closed intervals that touch"),
    ("'r3c2': \"`[3, 4]` lies", "'r3c1': \"`[3, 4]` lies"),
    ("'r4c2': \"Zero is written", "'r4c1': \"Zero is written"),
    ("'r5c2': \"`-45` has two", "'r5c1': \"`-45` has two"),
]
for a, b in pairs:
    assert a in t, a
    t = t.replace(a, b)
open('b16.py', 'w').write(t)
