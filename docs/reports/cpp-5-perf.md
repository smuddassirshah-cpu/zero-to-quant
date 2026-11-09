# cpp level 5: performance task

`cpp/homework-5.json`, `h5-sole-and-counted`, index 9 (item 10 of 10, added). Kind `code`, C++.

Objective: l23 "Implement a minimal unique pointer and a reference-counted pointer." The only L5 match (cpp is Stage 1, so "Explain" does not count).

Task: `SolePtr<T>` and `CountedPtr<T>` from a blank file, plus `CountedPtr(SolePtr<T>&&)`. 15 tests, 2 examples, `leakCheck`. Sixteen planted slips, each caught on both compilers: the lesson's own assignment orders (tests 6, 12, 13), no `release` in the conversion (14), an empty `SolePtr` counted 1 (15), moves not `noexcept` (9), and ten more. Five, replayed in the app's clang, fail as predicted. The starter fails. `how` names the untested: privacy, a copy of an empty `CountedPtr`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/cpp python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/cpp-5-perf-numbers.py`: exit 0, `FAILURES: 0` (g++, clang++, C++17 and C++20, the engine's leak block, a second solution, a Python ownership model).
4. `node tools/playthrough.mjs --set cpp/homework-5 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shot checked.

Freshness grep: `SolePtr`, `CountedPtr`, `release`, `use_count`, `->older`, `std::move(head`, `chain`; `fresh-check --file`: `release`, `use_count` only (standard member names).

Overlapping screens: l23 screens 3 and 6 (`UniquePtr`, `SharedPtr` from a scaffold), review-5 `r5-unique-move-assign`, homework-5 `h5-shared-move-assign`. New: a blank file, the conversion, a source inside the object being let go.
