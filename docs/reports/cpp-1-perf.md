# cpp level 1: performance task

`cpp/homework-1.json`, `h-tick-rule`, index 8 (item 9 of 9, added). Kind `code`, C++.

Objective: l3 "Write conditionals and loops in C++." Not l4 (header): the editor holds one file, so a header cannot be graded.

Task: `signed_volume(prices, sizes)` by the tick rule, from a stub. 10 tests, 1 example. Planted slips, each caught: `int` total (tests 6, 7, 10); loop from 0 reading `prices[i - 1]`; `size() - 1` bound, empty feed (2); `sizes[i - 1]`; flat resets the sign; `>=`; first price as base (8, 9, 10); `prev = 0` signs the first trade. Starter fails 8 of 10.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/cpp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/cpp-1-perf-numbers.py`: exit 0 (g++ and clang++, `-std=c++20 -O1 -fno-exceptions`; expects by two Python models).
4. `node tools/playthrough.mjs --set cpp/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shot checked.

Freshness grep: `tick rule`, `uptick`, `signed`, `prices[i - 1]`, `size() - 1`; `fresh-check --file`: 0 hits.

Overlapping screens: l3 screen 3 (`count_up_days`) lays out the loop from 1 against `prices[i - 1]`; `h-total-volume` a `long long` total. New: the sign carried through flats, parallel vectors, signed sums, the first-trade rule.
