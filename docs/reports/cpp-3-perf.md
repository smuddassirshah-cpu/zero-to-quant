# cpp level 3: performance task

`cpp/homework-3.json`, `h-session-range`, index 7 (item 8 of 8, added). Kind `code`, C++.

Objective: l10 "Write a class whose constructor and methods protect an invariant." It also needs l12's operators and l13's templates; no inheritance (review-1.9 deferral).

Task: `SessionRange<T>` from a blank file. 15 tests, 1 example (one raises, three compile checks). Sixteen planted slips, each caught, among them: `+=` returns a copy (8); `+` widens its left side by reference (9); `int` width overflows (5); no check (6); `==` or `!=` on the low only (11); non-`explicit` constructor (14). Starter fails 14 of 15. Test 15 refuses public ends by a structured binding; other public layouts are untested, and `how` says so. `==` by equal widths is caught by test 11.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/cpp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/cpp-3-perf-numbers.py`: exit 0 (g++, clang++, a second solution, C++17 too; Python range model).
4. `node tools/playthrough.mjs --set cpp/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shot checked.

Freshness grep: `SessionRange`, `operator+=`, `operator==`, `operator<<`, `invariant`, `width`; `fresh-check --file`: no hit on the item.

Overlapping screens: l10 screen 4 (checked constructor, `const` readers), l12 screens 3 and 8 and review-3 (`+`, `==`, `<<`), l13 screen 10 (`Window<T>`). New: `+` built on a copy, an overflow-safe width, `!=` agreeing with `==`, three types.
