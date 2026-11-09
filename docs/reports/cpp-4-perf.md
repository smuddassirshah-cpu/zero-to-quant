# cpp level 4: performance task

`cpp/homework-4.json`, `h4-test-median`, index 8 (item 9 of 9, added). Kind `code`, C++.

Objective: l18 "Write unit tests for C++ code with a test framework." Not l17 (CMake): it cannot run here.

Task: from a blank file, write the tests for a supplied `median_volume`. 6 tests, 1 example: the real version must pass; five hidden slips must be caught: no sort, `int` division, `int` sum overflow, upper middle only, `size() - 1` on an empty list (run must stop). Seven planted weak suites (odd counts only, no empty list, sorted inputs only, a wrong hand value, and others) each fail a test. Starter fails all 6.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/cpp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/cpp-4-perf-numbers.py`: exit 0 (g++, clang++; medians by `statistics` and a hand sort; slips in 32-bit arithmetic).
4. `node tools/playthrough.mjs --set cpp/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shot checked.

Freshness grep: `median`, `TEST(`, `CHECK_CLOSE`, `planted`, `size() - 1`; `fresh-check --file`: 0 hits.

Overlapping screens: l18 screens 4, 5 and 10 and `h4-test-drawdown` lay out tests against planted bugs with this stand-in. New: no test names or inputs given, a new function, type slips the learner must foresee.
