# terminal level 1: performance task

- `homework-1.json` item 9 of 9, `h-perf-fx-paths`, appended. Kind `code`, difficulty 5.
- Matched objective (l2-folder-tree): "Write and read a path from the top of a tree".
- Product: six paths on a new tree, from a stub, graded as `h-code-paths` is (functions returning text). A hidden prelude follows each path through the tree, so any correct route passes.
- 6 tests, 0 examples; 20 planted bugs each fail a test.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/terminal python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/terminal-1-perf-numbers.py`: numbers script exits 0 (101 checks; every path also checked with bash on a scratch tree).
4. `node tools/playthrough.mjs --set terminal/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter fails.

Freshness: `fresh-check.mjs --file` 0 hits; priya, fx.ini, .config, gbpusd, eurusd, holidays: not in the course.

Overlapping screens: l2 screens 3 and 7, l3 screens 0, 3, 4 and 7, l4 screens 4 and 9, review-1 `r-dotdot-tap`, `r-shared-from-notes`, homework-1 `h-code-paths`. New: the tree, a hidden folder in a path, a wrong-case path to fix, up two into a hidden folder.

Backlog: 1 bullet.
