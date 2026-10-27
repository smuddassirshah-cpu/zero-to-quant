# Topic 1.9 exam: C++

File: `app/content/exams/topic-1.9.json` (id `topic-1.9`, 60 minutes, pass 0.7).
Generator and checks: `scratchpad/exam-1.9/`. `gen.py` builds the file. `code_items.py` and `code_fmt.py` hold the code items' sources, tests and wrong versions. `calc.py`, `calc_tree.py` and `calc_dig.py` recompute the numbers. `codecheck.mjs` grades any source against a widget spec in the app's own runtime: it mounts `ZQ.cppCode` in Chromium with the local CDN, so clang 21 and libc++ compile exactly as for a learner. `probe.py` and `probe2.py` ask that runtime for facts (outputs, compile checks). `native/` has the g++ 13 and CMake transcripts. `lint.py` and `widths.py` check copy and phone widths.

Minutes: topic 1.9 has 140 hours, and `examMinutes` gives 60 for 61 to 150 hours. The second reader proposed 90; the file follows `examMinutes` (backlog bullet below).

## Shape

25 items, following the second reader's 25-point coverage list in `docs/reviews/review-1.9.md`, with cpp and cpp-pricing interleaved.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 20% | 20% |
| 3 | 12 | 48% | 50% |
| 4 | 5 | 20% | 20% |
| 5 | 3 | 12% | 10% |

Widgets: 9 choice (3 with a console canvas), 6 code, 4 multi (1 with a console), 3 numeric, 2 table, 1 longform.

| # | id | d | skills | widget | review list point |
|---|---|---|---|---|---|
| 1 | e-negative-split | 2 | cp-basics | choice | 1: `-11 / 4`, `-11 / 4.0`, `-11 % 4` |
| 2 | e-trim-copy | 2 | cp-references | numeric | 4: by value against by reference |
| 3 | e-seeded-draws | 2 | cx-numeric | choice, console | 19: seeded `mt19937`, libc++ against libstdc++ |
| 4 | e-scale-order | 2 | cp-classes | choice | 12: member `operator*`, which order compiles |
| 5 | e-link-stage | 2 | cp-build | choice, console | 16: linker error from a transcript |
| 6 | e-volume-wrap | 3 | cp-basics | choice | 2: signed overflow (UB) against unsigned wrap |
| 7 | e-quote-binds | 3 | cp-references | multi | 5: `T&`, `const T&`, `T` with temporaries and `const` |
| 8 | e-parity-put | 3 | cx-pricers | numeric | 21: Black-Scholes put by parity at T = 0.5 |
| 9 | e-dangling-best | 3 | cp-memory | multi | 6: pointer to a local, reference into a by-value copy |
| 10 | e-larger-twice | 3 | cp-classes | choice | 11: deduction conflict and instantiation count |
| 11 | e-batch-clock | 3 | cx-perf | table | 22: batch size, median, dead-code trap |
| 12 | e-code-worst-day | 3 | cp-basics | code (script) | 3: `std::cin` loop with a short-input guard |
| 13 | e-level-maps | 3 | cp-stl | choice | 14: `map` against `unordered_map` with costs |
| 14 | e-curve-owners | 3 | cp-memory | table | 8: `shared_ptr` counts through copies, moves, a scope |
| 15 | e-cmake-include | 3 | cp-build | multi, console | 17: PUBLIC against PRIVATE, which build types define `NDEBUG` |
| 16 | e-quote-lines | 3 | cx-perf | numeric | 23: cache lines for an array of structs |
| 17 | e-code-credit-line | 3 | cp-classes | code | 9: invariant in the constructor and every mutator |
| 18 | e-fill-specials | 4 | cp-classes | multi | 10: defaulted copy and move constructors delete assignment |
| 19 | e-time-bump | 4 | cx-numeric | choice, console | 18: $\sqrt{T+\delta} - \sqrt{T}$ cancellation |
| 20 | e-cancel-erase | 4 | cp-stl | choice | 13: erase in a loop |
| 21 | e-code-grid-owner | 4 | cp-memory | code | 7: raw `new` with two early returns to `unique_ptr`, live counter |
| 22 | e-code-rank-fills | 4 | cp-stl | code | 15: two-key comparator, captured lambda, `accumulate` start type |
| 23 | e-code-knockout | 5 | cx-pricers | code | 20: one-vector tree through `const Payoff&`, growth per step |
| 24 | e-code-digital-tests | 5 | cx-testing | code | 24: tests that pass the pricer and fail three planted bugs |
| 25 | e-port-note | 5 | cx-testing, cx-perf | longform, 10 points | 25: porting and timing note |

Skills: all 10 are covered. The `skills` map is the union of the two course.json maps: cp-basics 3, cp-references 2, cp-memory 3, cp-classes 4, cp-stl 3, cp-build 2, cx-numeric 2, cx-pricers 2, cx-perf 3, cx-testing 2.

Quant framing: a split loss in pence, trimming a position, seeded Monte Carlo, a fee in pence, a quote build, share and lot counters, quotes by reference, a put from parity, best bids, a pricer timed in batches, a price file's worst day, book levels and ticker prices, a yield curve shared by owners, a pricing library's CMake, quote structs in cache, a counterparty credit line, fills with defaulted members, a time bump, cancelled orders, a stop-loss scenario grid, a fill report, an up-and-out option, digital options, and a pull-request note on the C++ port.

Fresh against the courses. The lessons' code covers Quote with bid below ask, buy and sell positions, an order filled once, money that adds, price-then-time sorting, VWAP with `inner_product`, a sum over a counted input, CRR European and American trees and `bs_put` tests. So the exam's code items are new problems: the worst daily return over input of unknown length; a credit line with three mutators; a scenario grid whose private destructor admits only `std::default_delete`; a fill report by venue then size, with a captured threshold; an up-and-out tree with a new `Straddle` payoff; and tests for digital options, where one planted bug is invisible to both a T = 1 reference and parity. Every numeric input is new (for example S = 50, K = 52, T = 0.5 for parity; seed 2024; 40,000-call batches; 32-byte quotes).

## Code items (app runtime: clang 21, libc++, `-O1`, `codecheck.mjs`)

| item | tests | solution | starter | wrong versions (each fails, first failing test) |
|---|---|---|---|---|
| e-code-worst-day | 7 stdout | 7/7 | 0/7 | count read first (4), `while (!eof())` (2, prints −100%), `worst` starts at 0 (4), no short-input guard (2) |
| e-code-credit-line | 10 (6 raises) | 10/10 | 4/10 | constructor check only (3), `>=` on the draw (7), no sign check (6), `set_limit` unchecked (5) |
| e-code-grid-owner | 8 (4 on `Grid::live`) | 8/8 | 4/8, leaks | `delete g` (compile error: private destructor), `make_shared` (compile error), `+limit` on the stop path (5), `release()` on the stop path (6) |
| e-code-rank-fills | 10 | 10/10 | 3/10 | `venue < b.venue \|\| qty > b.qty` (1, libc++ hardening reports a non-strict-weak ordering), size ascending (1), `accumulate` from `0` (6), `>` for `min_qty` (8) |
| e-code-knockout | 11 (1 raises) | 11/11 | 1/11 | barrier checked at the leaves only (2), multiply by `growth` (2), `Payoff` by value (compile error: abstract), no q check (11), straddle paying a call (1) |
| e-code-digital-tests | 5 runs | 5/5 | 2/5 | reference and parity only (5: the σ for σ√T bug passes), exact `==` on the reference (1), parity summing to 1 (1), reference with tolerance 0.02 (4) |

38 runs, all as expected (`check3.log`). The digital kit is the l12 prelude kit with `all_pass()` in a postlude, and function pointers swapped in `setup` for each planted bug; a second correct implementation (call from `exp(-rT) - put`, put from `erfc` directly) must pass too, so an exact comparison fails. Raises cases use only real throws (`std::invalid_argument`), never undefined behaviour. Headers the hidden code needs are in the prelude. Each `how` says the first compile downloads the compiler and that a throw ends the test.

## Numbers computed twice

- Item 1: `-2 -2.75 -3` from the app runtime and by hand (truncation, $(-2)(4) + (-3) = -11$); Python's `-3 -2.75 1` for the distractor.
- Item 2: 700 by hand and traced twice.
- Item 3: the app (libc++) printed `0.872203 0.809774 0.216707`, g++ 13 (libstdc++) printed `0.809774 0.872203 0.895505`, twice each run; the first `mt19937(2024)` output, 2,525,503,112, is the same in both.
- Items 4, 7, 10 and 18: every "compiles or not" claim was checked by compile checks in the app runtime (`probe.py`, `probe2.py`).
- Item 6: $2^{32} - 1 = 4{,}294{,}967{,}295$ from the runtime and by hand.
- Item 8: C = 3.796744662753987 by `erfc` and by `scipy.stats.norm`; parity put 4.767075674705261 against the direct put 4.767075674705264; slip put 6.5003, undiscounted 5.7967, one-year discount 3.7578, sign error 2.8264.
- Item 14: `3 2` printed by the runtime and traced by hand.
- Item 11: 10 ms / 0.25 µs = 40,000; median 10.1 against mean 10.643; 252.5 ns and 266.07 ns, both by Python and by hand.
- Item 15: CMake with g++ 13 rebuilt the error with PRIVATE, PRIVATE on the link line (still fails) and PUBLIC (builds); the cache shows `-O3 -DNDEBUG`, `-O2 -g -DNDEBUG`, `-Os -DNDEBUG` and Debug `-g`; Release printed 4.87706 for `sigma = 0`, Debug aborted on the assert.
- Item 16: $10^6 \times 32 / 64 = 500{,}000$ and $10^6 \times 8 / 64 = 125{,}000$; `sizeof(Quote)` is 32 in the wasm32 runtime.
- Item 19: naive 5.000000413701855e-11 and rewrite 4.999999999875e-11 from the runtime and identically from Python (both round square roots correctly); a 50-digit `Decimal` value of the stored δ gives relative errors 8.3e-8 and about 4e-17; the bound $2^{-53} / (5 \times 10^{-11}) = 2.2 \times 10^{-6}$ gives the "about 6 figures" in the key.
- Item 12: every expected line from `%.2f` and again from `Decimal` rounding of the same double, then confirmed by the runtime's own output.
- Item 22: rankings by a key sort and by a comparator sort (`cmp_to_key`); notionals by a loop and by `math.fsum`; the 20,000-fill checksum by both sorts.
- Item 23: every price by the one-vector method, by summing all $2^n$ paths with knock-out along each path (small trees), and by a full two-dimensional lattice with spot by multiplication (1,000 steps, agreement 1e-13); the leaf-only values (3.9982, 8.6127 and others) by the same code with the barrier removed from the steps; $1/1.02^5 = 0.9057308$ for the test-defined payoff.
- Item 24: the reference 0.40824457 by `erfc` and by SciPy; each bug's value at the reference, its parity error (0.0963, 0.0296, 0) and its near-expiry value (0.42 for the σ slip, about $10^{-85}$ otherwise), which shows each bug escapes at least one natural test.
- Item 25: $1000 \times 1001 / 2 = 500{,}500$ node updates, by formula and by summing $i + 1$ over 1,000 steps.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors overall, no message for this file. The manifest lists `exams/topic-1.9.json`.
- Copy lint (`lint.py`): no `!` and no em-dash, no sentence of 20 words or more, explanations of at most three sentences, no American spellings.
- `playthrough.mjs --exam topic-1.9 --local-cdn <pkgs>`: 25 of 25, passed, desktop and `--mobile`.
- Screenshots reviewed (`scratchpad/exam-1.9/shots`). Fixes made from them: every code snippet in prose was rewrapped to 38 characters, and in options to 33, so nothing is cut at 390 px. The dangling-pointer and erase options now use short names (`Bids`, `v`). The template labels moved from end-of-line comments into variable names (`A` to `E`). The `use_count` print labels moved onto their own lines. The seeded-draws output and the time-bump code lines were shortened. Starter and solution lines were cut to 60 characters, so the desktop editor shows them whole.

## Engine notes (also in `docs/BACKLOG-INBOX.md`)

- The validator rejects a table cell's own `wrong[]` ids as `byKey` keys, though `table.js` returns them (pass 7). Items 11 and 14 use `r{i}c{j}` keys instead.
- `examMinutes` gives 60 minutes for 140 hours. This 25-item paper has 6 compiled code items and a longform, and the compiler's first load uses some of that time.
- Fenced code inside `choice` and `multi` options is clipped at about 33 characters on a phone, with no fade or scroll hint.
- C++ code items cannot check the learner's source (Python's `__learner_source__` has no C++ twin). Item 21 forces `unique_ptr` with a private destructor and a `friend std::default_delete<Grid>`.
- The exam `--why` result screenshot is still blank below the score (another vote for the topic-0.3 bullet).
