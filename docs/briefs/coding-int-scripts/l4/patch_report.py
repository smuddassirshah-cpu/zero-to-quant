p = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/docs/reports/coding-int-4.md'
s = open(p).read()
pairs = [
    ("| 9 (fails 4: tests 9 to 12 and 13 in part) | passes 13 |", "| 9 (fails 4: tests 9, 10, 11 and 13) | passes 13 |"),
    ("The hash-map solutions pass all 11 tests in about a second of compile and run time.", "The hash-map solutions pass all 11 tests inside the limit."),
    ("the correct version and `BUG1` to `BUG5` in C++ were compiled with `g++` and the real clang.", "the correct version and `BUG1` to `BUG5` in C++ were checked in the real clang by the playthrough (the starter passes 2 of 6, the model tests pass 6 of 6)."),
]
for a, b in pairs:
    assert a in s, a
    s = s.replace(a, b)
open(p, 'w').write(s)
print('ok')
