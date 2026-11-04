p = '/home/user/zero-to-quant/.claude/worktrees/agent-ae8c38b19d4267c01/docs/reports/coding-int-4.md'
s = open(p).read()
table = """| File | Desktop and 390 px, `--mobile --why` (final content) |
| --- | --- |
| l15 | ok, 14 checks, quiz 4/4 |
| l16 | ok, 15 checks, quiz 4/4 (the C++ `testkit` screen compiled with the real clang) |
| l17 | ok, 14 checks, quiz 4/4 |
| l18 | ok, 14 checks, quiz 4/4 |
| l19 | ok, 15 checks, quiz 4/4 |
| review-4 | ok, recorded 10 of 10 |
| homework-4 | ok, 8 of 8 right, 38 of 38 marks, and the parts checks (open parts kept in the draft, part credit in the marks) |
| `--drills` | all 34 drill files and the sample session ok, desktop and `--mobile` (the ten `ci-` drills: the model solution passes every hidden test and the starter fails) |

An earlier desktop-only run of the same files also passed. About 460 screenshots of the final run were read at both widths for layout."""
assert 'PLAYTHROUGH_TABLE' in s
s = s.replace('PLAYTHROUGH_TABLE', table)
open(p, 'w').write(s)
print('ok')
