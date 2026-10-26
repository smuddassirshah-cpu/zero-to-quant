# cpp-pricing level 3 ("Fast and correct"): report

## Files written

All in `app/content/courses/cpp-pricing/` (generators and harness in the scratchpad folder `cpp-pricing-3/gen/`; the hidden C++ in every prelude mirrors level 2's `Payoff`/`Call`/`Put`, `terminal_values`, `step_back`, `tree_price`, `binomial_price(const Payoff&, s, r, sigma, t, n, american)`, `bs_call`, `bs_put`, `bs_delta_call`):

- `l9-timing.json`: 10 screens, 4 quiz items, skills `cx-perf`, `cx-pricers`. Console hook (seven runs, tap the warm-up), bars explore (slider on run 1; mean, median, minimum by `derive`), code `time_us(F f)` template (counter in the postlude, `long long` type check, a 2 ms spin read between 1,500 and 999,999 µs so the unit is checked without depending on speed), code `median_of`, numeric edge case on the 100 µs browser tick (batch of 400 trees), code `tree_table(ns, batch)` (warm-up, five timed batches, printed sink; graded on returned prices plus counters that the timer and pricer ran; the learner's own timing table prints under the example), series generalise (T(2n)/T(n) ≈ 4, predict n = 1,600), trap on deleted work (real output from this app's compiler: 200,000 unused `bs_call`s 97 µs against 25,361 µs summed), order derive (a fair benchmark), transfer bars (log scale) Python loop 40 ms / NumPy 4.2 / C++ -O0 4.5 / C++ -O2 0.45 ms with the 100,000-option nightly batch (67 min against 45 s).
- `l10-memory-layout.json`: 10 screens, 4 quiz items, skills `cx-perf`, `cx-pricers`. Array canvas (24 doubles wrapped 8 to a line) for cache lines and a stride-8 tap explore, grid for row-major places, code `index(i, j, cols)`, code `sum_row_major`/`sum_col_major` (graded on sums; 1 × n and a row of exactly 8 included), predict-then-read console (desk 2000 × 2000: 2.9 ms against 21.5 ms), code `flat_lattice_price` (10.4467 at n = 512, within 0.005 of 10.4506; explanation says why the one-row version wins: 2.1 MB against 4 KB), trap with a `boxes` canvas of a vector of vectors, generalise AoS/SoA (37,500 lines), transfer vector against list for a 100,000-tick buffer (66 µs against 186 µs), link to pandas columns and order books. Quiz: 1 × n edge case, `reserve` copies (131,071), lattice index, a row of exactly 8 doubles.
- `l11-optimisation-flags.json`: 11 screens, 4 quiz items, skills `cx-perf`, `cx-pricers`. Console hook (-O0 4.50 ms, -O2 0.45 ms: ten times), bars explore tap "which build to time" (-O0/-O1/-O2/-O3), `place` flags to needs (-O2, -g, -DNDEBUG, -Wall -Wextra -Werror, -march=native), code `american_put` with one `pow` per step (desk: 15.5 ms to 1.6 ms, a gain no flag gives), code `checked_put` with `assert`s tested by `raises` (asserts are on in the app), trap `assert(load_curve())` under -DNDEBUG (real g++ output: 4 then 0), -ffast-math deleting an `isnan` check (real g++ output), clang deleting `x + 1 < x` at -O2 (real clang output: 1 then 0), script-mode screen where the learner's program reports its own build (`__OPTIMIZE__`, `NDEBUG`; prints "optimised: yes / asserts: on / price: 10.4467"), generalise CMake build types, transfer `RelWithDebInfo`. Edge case (code that only works at -O0, an uninitialised `double`) in the quiz.
- `l12-testing-a-pricer.json`: 9 screens, 4 quiz items, skills `cx-testing`, `cx-pricers`. Plane hook (call against σ, drag to σ → 0, £4.8771), plane explore (call against S with the forward line), and four code screens using a hidden test kit (`TEST`, `CHECK`, `CHECK_CLOSE`, `run_tests()` returning "N passed, M failed" and printing PASS/FAIL lines): parity plus σ → 0 limit (checked against two planted bugs), tree convergence within 0.01 at n = 512 (fails a tree capped at 64 steps, 0.031 off, and one with the rate dropped), the planted `bs_put` with N(d2) ("0 passed, 1 failed" on the bug, "1 passed, 0 failed" on the fix, plus a second bug), finite-difference delta (h = 0.01, tolerance 1e-5, two wrong deltas). Trap: a circular test. Generalise: Catch2 syntax (`TEST_CASE`, `SECTION`, `REQUIRE(... == Approx(...).epsilon(...))`, `REQUIRE_THROWS`, which the app cannot run) with a `tree` canvas of the test file; property tests with a fixed seed. Transfer: `ctest` output where `==` fails C++ against Python after `-march=native` (real: 87 of 100 inputs differ, worst 14.403685711729995 against 14.403685711730011); tolerance 1e-9 relative closes the exit task.
- `review-3.json`: 9 items, difficulty 2 to 4, all four lessons.
- `homework-3.json`: 8 items, difficulty 3 to 5. Code (5): a complete test file of at least six tests, graded on the counts against the correct library and six planted bugs (one needs a σ → 0 limit test). Code (4): American put on a packed triangular lattice (`i(i + 1)/2 + j`) with a `reserve`d share-price buffer, graded on prices. Order (4): bisecting a failing regression test. Longform (5, 10-point rubric, full model answer): the Python against C++ timing write-up for the desk, the exit deliverable. Plus the batch-window n (6,325), a transposed lattice index, a benchmark with four faults (multi), order-book cache lines.

Every `how` warns about the first compiler load (about 26 MB, 10 to 15 s the first compile, 1 to 3 s after).

## Validator

`node app/tools/validate.mjs`: 0 errors and 0 warnings in my six files. The run's one error is another agent's (`validation/l10-scaling-with-future.json`, earlier `stat-learning/l8-setting-to-zero.json`).

## Playthrough

`node app/tools/playthrough.mjs --local-cdn …/scratchpad/pkgs --shots …`, screenshots in the scratchpad folders `cpp-pricing-3/shots` and `cpp-pricing-3/shots2`:

- l9-timing: 14 checks, quiz 4/4, ok.
- l10-memory-layout: 14 checks, quiz 4/4, ok.
- l11-optimisation-flags: 15 checks, quiz 4/4, ok.
- l12-testing-a-pricer: 13 checks, quiz 4/4, ok.
- review-3: 9 of 9 recorded, ok.
- homework-3: 8 of 8, 37 of 37 marks, ok.

Fixed after reading the screenshots, then l10, l11, l12 and review-3 replayed: grid `paths` drawn over the cell numbers (now shaded sets), clipped card labels on the vector-of-vectors `boxes` canvas, a doubled and cut-off build line on the flags screen, and a "dashed" forward line that is drawn solid.

## How the C++ cases were checked

Every expected value came from running the solution through a Node copy of the worker (same flags, runtime and WASI shim) with the app's own `cpp-grade.js` harness; every solution passes all its cases and every starter fails at least one. Prices were checked a second time in Python (trees l8's pricer and a no-`pow` replica). Desk numbers were measured natively in this sandbox (Intel Xeon 2.1 GHz, Python 3.13, g++ 13.3, clang 18) and are labelled illustrative. Slowest graded case: the `tree_table` example, about 100 to 500 ms depending on machine load.

## Runtime facts verified

- Optimisation level: `-std=c++17 -O1` with libc++ debug hardening, fixed (`FLAGS` in `cpp-worker.js`). The worker accepts an `opt` value on `init` as a benchmarking knob, but the page never sends one and there is no per-widget or per-case `flags` option, so l11 says the app compiles at one fixed level and reads desk comparisons from consoles.
- Asserts: `NDEBUG` is not defined, so `assert` fires ("Assertion failed: n > 0 (main.cpp: checked_put: 5)", exit 134) and `compare: "raises"` catches it. `__OPTIMIZE__` is defined.
- Clocks: `high_resolution_clock` is `steady_clock` (is_steady 1). `steady_clock` reports nanoseconds but in Chromium moves in 100 µs steps (`performance.now()` coarsened; the page is not cross-origin isolated); 199,256 of 200,000 back-to-back reads were equal. `system_clock` ticks every 1 ms (`Date.now()`). In Node the same wasm sees about 170 ns.
- Deleted work: in the app's -O1 build a loop of 200,000 `bs_call`s whose results are unused ran in 97 µs against 25,361 µs when summed; a tree whose result is unused was not deleted.
- In-browser tree timings (headless Chromium, -O1, batches of 100 trees, median of 5, on a machine shared with other agents, load average about 14): n = 100: 47 to 54 µs; n = 200: 86 to 117 µs; n = 400: 244 to 405 µs (ratio per doubling 1.6 to 4.7 under load). Node on the same wasm: 19 to 21, 74 to 147 and 265 to 596 µs. The lesson shows 20, 80, 300 and 1,200 µs as representative and tells the learner to read the ratio from their own run.

## Departures from the brief, with reasons

- The timing program is a function-mode screen (`tree_table` returns the prices and prints the timing table), not script mode: a script-mode `stdout` case compares the whole output, and stderr is never shown on a passing run, so printed timings would either fail the case or be invisible. In function mode the printed table shows under each row.
- l12's test screens are function mode too (`run_tests()` returns "N passed, M failed"; the PASS/FAIL detail prints under the row). The planted-bug "two preludes" is done with one prelude whose pricers are function pointers that a case's `setup` swaps (`bs_put = bs_put_buggy;`), since `prelude` is per widget.
- `cpp` l18 does not exist yet, so l12 builds its own `TEST`/`CHECK`/`CHECK_CLOSE` kit in the prelude (shape as briefed).
- Measured numbers replace the guessed ones: trees l8's pure Python takes 35 to 45 ms at n = 1,000 here (not about a second), and -O0 is about 10 times slower than -O2 on the tree (not 20 to 50).
- `time_us` has two clock-bounded tests (a 2 ms spin reads 1,500 to 999,999 µs) beside the counter and non-negative checks, to catch milliseconds or nanoseconds; neither depends on the machine's speed.

## Proposed change to course.json

None.

## Engine and runtime limitations

Eight bullets in `docs/BACKLOG-INBOX.md` under "Raised later (cpp-pricing level 3):".
