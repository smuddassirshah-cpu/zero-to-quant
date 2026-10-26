# cpp level 4 ("The standard library and tools"): report

## Files written

All in `app/content/courses/cpp/`. Lesson ids, names, objectives and skills follow `course.json` (`cp-stl` for l14 to l16, `cp-build` for l17 and l18). Money is in £. Every `how` warns about the first compiler load (about 26 MB, 10 to 15 s for the first compile, 1 to 3 s after). Generators and helper scripts are in the scratchpad folder `cpp-4` (`gen/all.sh` rebuilds every file).

- `l14-vector.json`: 11 screens, 4 quiz items.
  - Canvases: an `array` explore where a slider pushes closes one at a time; size, capacity and doubling show live, and unallocated slots are dimmed. Also `begin()`/`end()` pointers, the erase trap on an `array`, and a `tree` of the price lattice.
  - Code: `moving_average` (edge cases: `n` larger than the vector, `n = 0`, empty), `returns_from` with `reserve` (a hidden test reads `capacity()`; an empty input wraps `size() - 1`), a script that prints the three largest prices from `stdin`, `price_change` with `at()`, where `raises std::out_of_range` separates `at` from `[]`, and `price_lattice` (`vector<vector<double>>`, transfer to the pricer).
  - Trap: erasing inside an iterator loop skips the next zero; run here, it printed `101.2, 0, 101.5`. Generalise: the unsigned `i >= 0` reverse loop. Quiz: `v(3)` against `reserve`, `at` past the end, `data()` for a C API, and vector against linked list (cache lines).
- `l15-maps.json`: 10 screens, 4 quiz items.
  - Canvases: a `boxes` drag of keys into print order (std::map against Python dict), a `tree` search for BP in a balanced map, an `array` of hash buckets, a complexity `table` plus a `table` widget choosing `map` or `unordered_map` per desk job, the `[]`-inserts trap on `boxes`, and an `orderbook` for the transfer.
  - Code: `position_by_symbol`, with the map returned whole as `[[key, value], ...]`, one key, size and `begin()->first`. `exposure` on a `const unordered_map` (`px[sym]` does not compile, so `find`). A script counting fills and shares per venue from `stdin` in key order.
  - Transfer: a `std::map<double,int>` book. `100.1 + 0.1` is a third key beside 100.2, verified in the runtime; key by integer ticks or a vector by tick. Quiz: empty `begin() == end()`, unordered iteration order, `find` on a missing key, and a price cache by id.
- `l16-algorithms.json`: 10 screens, 4 quiz items.
  - Screens: an `order` of strategies by a Sharpe comparator, an `accumulate` explore stepping through P&L, a `count_if` capture tap, `transform` into an empty vector (the writes go nowhere, `size()` stays 0; checked in the runtime), the trap `accumulate(..., 0)` on doubles (173, not 175, verified), and `max_element` on an empty range.
  - Code: `vwap` with `inner_product` and `accumulate`; `sort_book` with a supplied `Order` and price-then-time lambda, where a `>=` comparator crashes on libc++'s strict-weak-ordering check; `count_up_days` with `adjacent_difference` and `count_if`; the transfer `worst_drawdown` with `partial_sum` and a `[&peak, &worst]` lambda, on a `series` drawdown chart.
  - Quiz: the `<=` comparator, a dangling `[&limit]` capture, `min_element` for `sorted(...)[0]`, and `partial_sum`.
- `l17-cmake.json`: 11 screens, 4 quiz items. Read-and-trace; the first screen says the tools run on a desk machine.
  - Screens: a project `tree` (tap the files that become object files), `CMakeLists.txt` in a numbered `console` (tap the target lines), a configure and build session (tap the link line), and an incremental rebuild.
  - Then Debug against Release in a `bars` chart (8 times), the trap where headers are found but `target_link_libraries` is missing, the `PUBLIC`/`PRIVATE`/`INTERFACE` pattern with a second library, an `order` derive of a fresh build, and a transfer on one desk library and `build/` in `.gitignore`.
  - Code (function mode, separate compilation simulated): the prelude is `rates.h`, and the learner writes the matching `rates.cpp` (a missing definition shows the real linker error). A `daycount.cpp` whose definition does not match the header fails to link until the learner fixes the signature.
  - Quiz: editing `build/`, a one-file project needs no CMake, mixed Debug and Release timings, and a header-only `INTERFACE` library.
- `l18-unit-tests.json`: 10 screens, 4 quiz items.
  - Reading Catch2: a `pair` of the pytest test and the Catch2 test (`TEST_CASE`, `REQUIRE`, `Approx`), a failing Catch2 run with `with expansion:`, `SECTION` re-running the test case, and `ctest` output with `REQUIRE_THROWS_AS` (the edge case: this app cannot catch exceptions).
  - In-app stand-in (said to be one): the prelude has `TEST(name)`, `CHECK`, `CHECK_CLOSE` and a registry; the postlude's `main` prints `FAIL name` lines and `N passed, M failed`.
  - Code: tests for a supplied `bs_call` (tolerance plus expiry boundary), checked against 3 planted bugs, which empty tests miss. A test that documents a bug in `simple_returns`: expected `FAIL ...` and `1 passed, 1 failed` on the shipped code and `2 passed, 0 failed` on a fixed one. Fixing `simple_returns` against supplied hidden tests at three price scales. A regression pin of the Python binomial value 10.430612, plus convergence to Black-Scholes, against 2 planted pricer bugs (transfer to `cpp-pricing`).
  - Planted bugs are chosen by `stdin`, and the runner prints `planted bug k: caught` or `missed`, so the output does not depend on how many checks a learner writes.
  - Trap: `CHECK(r[0] == 0.1)` fails on correct code (0.10000000000000009). Quiz: behaviour against implementation, tolerance from the reference precision, `REQUIRE` stopping a test, and a failing regression pin.
- `review-4.json`: 9 items, difficulty 2 to 4, covering all five lessons: capacity, erase loops, `[]` and `count`, choosing a map, `accumulate` with `0`, an ask comparator, a linker error, arrange-act-assert (`order`), and tolerance in a test.
- `homework-4.json`: 8 items, difficulty 3 to 5.
  - `h4-vwap-book` (code, 5): a script that reads trades into a `std::map<string, vector<Trade>>`, sorts each symbol's trades with a lambda, and prints count, VWAP, low and high to four decimals in key order.
  - `h4-test-drawdown` (code, 4): tests for a supplied `max_drawdown` with the in-app macros. Four planted bugs; one crashes on empty input (a `raises` case).
  - `h4-build-order` (order, 3): clone, configure, build, `ctest`, fix, rebuild, `ctest`.
  - Also: `reserve(100)` then 150 pushes (capacity 200, verified), a capture-by-value snapshot (3), a missing `target_link_libraries(report ...)`, and `[]` on a `const` map.
  - `h4-library-plan` (longform, 4): lay out a pricing library project, with a 10-point rubric and a full model answer (layout, CMake, builds, tests).

Every expected value in a C++ test came from running the solution through the app's own harness (`cpp-grade.js` `unit()` with a Node copy of the worker; scripts `cpp-4/check.mjs` and `cpp-4/rt.mjs`). Four of my hand values were wrong and were corrected from the runtime: a PV, a VWAP, a drawdown, and the nested-list `isclose`. Every starter was also run, and each fails at least one test. The browser playthrough ran every solution again.

## Validator

`node app/tools/validate.mjs`: 0 errors in my files. The only warnings in them are 10 ladder screens that change canvas kind; these are deliberate (code screens against `console`, `table` or `boxes` canvases). The 4 errors in the whole run are all in `ensembles/l10-small-steps.json`, another agent's file.

## Playthrough

Run with `--local-cdn …/scratchpad/pkgs --why`, after the last content edit (l14 replayed once more after its final explain fix). Every check passed and there were no console errors.

| File | Checks | Quiz or marks |
|---|---|---|
| l14-vector | 15 | quiz 4/4 |
| l15-maps | 14 | quiz 4/4 |
| l16-algorithms | 14 | quiz 4/4 |
| l17-cmake | 15 | quiz 4/4 |
| l18-unit-tests | 14 | quiz 4/4 |
| review-4 | 9 of 9 | |
| homework-4 | 8 of 8 | 36 of 36 marks |

Fixes made from the screenshots: map key cards overflowed the `row` slots in the l15 hook, so the cards now show the keys only. A long map initialiser in the l15 trap was wrapped. Starter comments longer than the editor width were split. The l14 capacity explore wrapped to two rows in the Why sheet, so it now always draws 8 slots and dims the unallocated ones.

## Proposed change to course.json

None.

## Engine and runtime limitations

These are listed in `docs/BACKLOG-INBOX.md` under "Raised later (cpp level 4):".
