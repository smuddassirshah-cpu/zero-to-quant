# Topic 3.5 exam: interviews by role

## Brief (written before the items)

### The file and what a topic exam may hold

File to write: `app/content/exams/topic-3.5.json`. Fields: `id` `topic-3.5`, `topic` `"3.5"` and `name` `Interviews by role`. Then `minutes` 90 and `pass` 0.7. Add a `skills` map of the 13 skills below and 30 items, the validator cap. This brief comes before the files of L3 and L4 of `research-int`, `coding-int` and `systems`. The author re-reads each written lesson before writing its item. If a lesson moved a skill, the author keeps the plan within its ramp.

Checked in `docs/AUTHORING.md` section 5 and 7, not taken from the plan. A topic exam may hold `code` items, in Python and in C++ with the harness. It may hold `parts` items (ENGINE-BACKLOG 467), `numeric`, `choice`, `multi`, `order`, `table` and `tap-regions`. It may not hold a `generator` entry or a `draw`, which are mock and stage exam features. It uses `pass` with the default marks (1, 0, 0). A `code` item may use `data`, but this exam reads no data file: the one data item puts its rows in the widget's `prelude`, so no new file is needed. The C++ item needs the compiler, so the playthrough runs with `--local-cdn`. No firm names appear anywhere (DECISIONS "Firm names (2 Nov)").

### Skill coverage by level

A level counts as covered when an item tests a skill first met in it. This is DECISIONS "Exam coverage (3 Nov)". Skills first met were read from `course.json` and the skills each brief assigns to each lesson: The sources are `docs/briefs/research-int.md` (the header line of each level) and `docs/briefs/coding-int.md` (the shared facts, skill by lesson). The third is `docs/briefs/systems.md` (its "Skills rule"). L3 and L4 are not yet written, so the briefs stand in for the files.

| Course | Level | Skills first met | Items testing them |
| --- | --- | --- | --- |
| research-int | 1 Statistics and linear algebra questions | rq-stats, rq-linalg | 1, 2, 3, 4 |
| research-int | 2 Machine learning questions | rq-ml | 5, 6, 7 |
| research-int | 3 The open case | rq-case | 8, 9 |
| research-int | 4 Data tasks and take-homes | rq-data | 10, 11 |
| coding-int | 1 Patterns still to learn | ci-patterns | 12, 13, 14 |
| coding-int | 2 Strings and simulation | ci-strings, ci-timed (first in l8), ci-design (first in l10) | 15, 16, 17 |
| coding-int | 3 Design in code | none (shared) | 18 tests l11 and 21 tests l14, through ci-design |
| coding-int | 4 Under the clock | none (shared) | 19 tests l15 and 20 tests l16, through ci-timed |
| systems | 1 Memory and the machine | sy-memory, sy-os (first in l3), sy-latency (first in l5) | 22, 23, 24, 25, 26 |
| systems | 2 Concurrency | sy-concurrency | 27 |
| systems | 3 Operating systems and networks | none (shared) | 28 tests l13, through sy-os and sy-latency |
| systems | 4 Low-latency C++ | none (shared) | 29 tests l17 and 30 tests l16, through sy-latency and sy-concurrency |

Levels covered only through shared skills: `coding-int` L3 and L4, `systems` L3 and L4. Each has at least one item built on one of its own lessons, named above. All 13 skills of the three courses are in the `skills` map and each is tested: `sy-memory` 5; `rq-linalg`, `rq-ml`, `ci-timed` and `sy-latency` 4 each; `rq-stats`, `rq-case`, `ci-patterns`, `ci-strings` and `ci-design` 3 each; `rq-data`, `sy-concurrency` and `sy-os` 2 each. The count comes from `docs/briefs/mocks-scripts/exam35_plan.py`, which asserts it.

### Item plan

Ramp, as AUTHORING section 5 asks: 6 items at difficulty 2 (20%). 15 at 3 (50%). 6 at 4 (20%). 3 at 5 (10%). Easy items come first. The courses are interleaved, so a learner who knows one course meets the others early. By course: `research-int` 11, `coding-int` 10, `systems` 9. By kind: 13 `numeric`, 6 `choice`, 3 `multi`, 2 `order`. Then 1 `table`, 1 `tap-regions` and 1 `parts`. Last, 3 `code` (two Python, one C++). Every `numeric` lists its named wrong values in `wrong`, each with a `feedback.byKey` line that names the learner's action. Every `choice` and `multi` has `"shuffle": true` and a `why` on every distractor. Every item has `skills`, `tags` (the family below first), `pace`, `difficulty`, `feedback` and `explain` of at most three sentences. The pace sum is 5,310 s. That is 88.5 minutes of the 90.

| # | Course, lesson | Lvl | d | Skills | Kind | Pace | Family tag | Idea |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | research-int l1 | 1 | 2 | rq-stats | numeric | 60 | `two-regressions` | The two slopes of a pair of regressions give the correlation, and the duplicated-data follow-up in one number. |
| 2 | research-int l2 | 1 | 3 | rq-stats, rq-linalg | numeric | 120 | `correlation-limits` | The range of a third correlation from two others, by a positive semidefinite matrix. |
| 3 | research-int l4 | 1 | 2 | rq-stats | choice | 60 | `p-value-meaning` | What a p-value, a power or a corrected threshold says, in plain words; each distractor a blurt. |
| 4 | research-int l5 | 1 | 3 | rq-linalg | numeric | 120 | `special-eigenvalues` | A determinant or eigenvalue of a rank-one-plus-identity or projection matrix, by reasoning. |
| 5 | research-int l7 | 2 | 3 | rq-ml | choice | 120 | `ridge-lasso` | Which penalty zeroes a coefficient and why, with a feature-scale twist. |
| 6 | research-int l9 | 2 | 3 | rq-ml, rq-linalg | numeric | 120 | `pca-share` | The variance share or loading of a component of a small covariance matrix. |
| 7 | research-int l10 | 2 | 4 | rq-ml | multi | 210 | `weak-signal-traps` | Which of six statements about a low signal-to-noise prediction hold (leakage, regime change, cost, sample size). |
| 8 | research-int l11 | 3 | 3 | rq-case | order | 150 | `case-steps` | Put the steps of an open prediction case in order; distractors are plausible wrong steps. |
| 9 | research-int l13 | 3 | 4 | rq-case, rq-ml | numeric | 180 | `baseline-first` | The expected error of a persistence, a mean and a fitted forecast on a mean-reverting series. |
| 10 | research-int l17 | 4 | 4 | rq-data | code | 480 | `group-fit` | A small Python function on data in the item's `prelude`: one fit per group with a guard for small groups. |
| 11 | research-int l18 | 4 | 5 | rq-data, rq-linalg, rq-case | parts | 360 | `online-fit` | Parts: update the sums when a row arrives, then when one leaves, then the cost or the stability trap. |
| 12 | coding-int l1 | 1 | 2 | ci-patterns | choice | 60 | `pattern-pick` | Name the pattern a short problem statement needs (sweep, trie, monotonic deque, heap, XOR). |
| 13 | coding-int l3 | 1 | 3 | ci-patterns | numeric | 120 | `deque-trace` | The number of pushes, pops or the answer after tracing a deque or a heap on a short list. |
| 14 | coding-int l4 | 1 | 3 | ci-patterns | order | 150 | `two-heaps` | Order the steps of a streaming median or top-k update; distractors skip the rebalance. |
| 15 | coding-int l7 | 2 | 3 | ci-strings | numeric | 120 | `stack-parse` | The value of an expression with unary minus and truncating division, traced with a stack. |
| 16 | coding-int l8 | 2 | 2 | ci-strings, ci-timed | numeric | 60 | `rule-trace` | The state after a short list of rule steps, read from a statement as an assessment words it. |
| 17 | coding-int l10 | 2 | 3 | ci-strings, ci-design | choice | 120 | `price-time` | Which resting orders fill, and in what order, when a crossing order arrives. |
| 18 | coding-int l11 | 3 | 3 | ci-design | table | 150 | `cache-state` | The order of keys in a least recently used cache after a list of gets and puts. |
| 19 | coding-int l15 | 4 | 3 | ci-timed | numeric | 120 | `minutes-plan` | The most points in a time budget when each problem may be taken in full, in part or skipped. |
| 20 | coding-int l16 | 4 | 4 | ci-timed | multi | 210 | `edge-case-list` | Which inputs expose a planted bug in a short function (empty, single, repeated, boundary). |
| 21 | coding-int l14 | 3 | 4 | ci-design, ci-timed | code | 480 | `event-window` | A small Python class or function counting events in a time window, with hidden tests of size and order. |
| 22 | systems l1 | 1 | 2 | sy-memory | numeric | 60 | `latency-ladder` | A ratio or order of magnitude between two costs on the latency ladder. |
| 23 | systems l2 | 1 | 3 | sy-memory | numeric | 120 | `cache-misses` | The count of cache misses for an access pattern and a line size. |
| 24 | systems l4 | 1 | 3 | sy-memory | tap-regions | 150 | `struct-padding` | Tap the padding bytes of a struct on an array canvas, or the field that moves to shrink it. |
| 25 | systems l3 | 1 | 3 | sy-memory, sy-os | choice | 120 | `page-fault` | What happens, and what it costs, on a first touch of a page; a TLB miss against a page fault. |
| 26 | systems l5 | 1 | 2 | sy-memory, sy-latency | numeric | 60 | `branch-cost` | The cycles lost to mispredicted branches in a loop over sorted and unsorted data. |
| 27 | systems l7 | 2 | 3 | sy-concurrency | multi | 150 | `race-claims` | Which claims about a two-thread listing hold (a race, a lost update, a possible final value). |
| 28 | systems l13 | 3 | 4 | sy-os, sy-latency | choice | 180 | `transport-pick` | TCP, UDP or multicast for orders and for market data, with the reason. |
| 29 | systems l17 | 4 | 5 | sy-latency | numeric | 300 | `tail-percentile` | A percentile of a short latency list, and why the mean misleads. |
| 30 | systems l16 | 4 | 5 | sy-latency, sy-concurrency | code | 600 | `ring-index` | A C++ function on ring-buffer indices with a power-of-two mask, tested single-threaded. |

Each idea names the question, not its numbers. The author picks the numbers. Each is computed twice: a closed form, then an enumeration, a simulation or an exact `Fraction` method. A script asserts that the two agree, and it is kept with the exam's report. Each `wrong` value is listed with its slip.

**Notes on the harder kinds.**

- Item 10 (`code`, Python): a function over a small frame or list built in the widget's `prelude` (for example `{ "town": ..., "x": ..., "y": ... }` rows), with at least 3 hidden tests, a starter that fails them, and a model solution. It tests the group guard from `research-int` l17 without reusing its file or its numbers.
- Item 11 (`parts`): 3 parts, each worth the same, graded one at a time: two `numeric` parts and a `choice`. A part that is not right does not stop the next from opening.
- Item 21 (`code`, Python): at most 8 hidden tests, small to large. One large case makes a quadratic answer fail on the 5 s clock. It tests the design idea of `coding-int` l14 on a different class or function from `RateLimiter` and `HitCounter`.
- Item 30 (`code`, C++): single-threaded, `-std=c++17`, no `try` or `catch`. Use function mode with `args` and `types`, and at most 6 tests. One test fails an answer whose mask is wrong for a power-of-two capacity. The item does not need threads.
- Item 24 (`tap-regions` on an `array` canvas): cell ids `c0`, `c1`, and so on, by displayed index, as `docs/briefs/systems.md` says.

### Freshness against lessons, mocks and the bank

No item may reuse the numbers, answers, call texts or function names of anything already written or planned. The author greps before writing each item and records the result in the report.

1. **Lessons, reviews and homework** of `research-int`, `coding-int` and `systems` (written files in `app/content/courses/<course>/`, and the briefs for unwritten levels: `docs/briefs/research-int.md`, `coding-int.md`, `systems.md`). Also the three courses' drills (`rq-`, `ci-` and `sy-` packs in `app/content/drills/`). An item may test a skill from a lesson and use its idea, but with new numbers. This is DECISIONS "Fresh numbers in reviews and homework".
2. **The mocks.** The three topic 3.5 mocks keep their families and keys in `docs/briefs/mocks-scripts/keys.json`, which `research_mocks.py` writes. Their code problems are in `oa_code_tests.json` and `qd_tasks_tests.json`. The families already used there are listed next. This exam must not reuse their items. Statistics: `two-regressions`, `correlation-limits`, `special-eigenvalues`, `multiple-testing`, `standard-error`, `t-statistic`, `adjusted-r2`, `bivariate-normal`, `portfolio-sd`, `min-variance-weight`, `compound-poisson`. Machine learning: `ridge-shrinkage`, `lasso-threshold`, `pca-share`, `bias-variance`, `boosting-round`, `leakage`, `cv-leakage`. Code: `fit-line-weights`, `rolling-slope`, `return-table`, `hedge-ratio`, `out-of-sample`. The eight `oa-` drill families: `product-windows`, `water-trapped`, `jump-count`, `merge-cost`, `digit-removal`, `rising-subsequence`, `digit-decodings`, `critical-path`. **This plan overlaps four of them by name.** Items 1, 2, 4 and 6 sit in four of these families. They are `two-regressions`, `correlation-limits`, `special-eigenvalues` and `pca-share`. The family tag is shared on purpose, because the tag marks a kind of question for the practice deck. The numbers, the matrix, the assets and the wording must all differ from the mock items. `keys.json` lists what to avoid. The author also reads the older trader and sig mocks for the keys they hold.
3. **The bank** (`app/content/bank/*.json`, 200 items). Grep each family tag and each key. Two bank groups touch this exam. They are `probability` (hats, indicator tricks, waiting for patterns) and `mental` (percentages, square roots). None of the 30 items is a probability or mental-maths item, so overlap should be rare.
4. **Earlier exams** (`topic-*.json`, `mock-*.json`): grep keys and call texts. `topic-1.4` already holds a minimum-variance weight with variances 0.04 and 0.09. That is why the mocks avoid that pair too.

**Voice** (binding): British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations at most three sentences, £ for money. Run `VOICE_BASE=<folder holding a copy of the exam file> python3 docs/reviews/voice-scan.py`: 0 and 0.

**Acceptance for the exam author** (not part of this brief's own report sections). `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors, 30 items, the ramp, all 13 skills; `node tools/playthrough.mjs --exam topic-3.5 --local-cdn <pkgs>` is green, and again with `--mobile`; the exam author writes the later sections of this report after the items. They cover numbers computed twice, validation and playthrough, `prep.json`, `course.json` and the backlog.

## Result (written after the items)

File: `app/content/exams/topic-3.5.json` (id `topic-3.5`, 90 minutes, pass 0.7, 30 items, pace sum 4,920 s = 82 minutes after the second read, which trimmed the three code paces to 360, 360 and 450 s).
Scripts in `docs/briefs/exam-3.5-scripts/`: `build.py` (with `build_a.py`, `build_b.py`, `build_c.py`, `helpers.py`) writes the file; `check.py` and `check2.py` recompute every number; `refs.py` holds independent references for the code items; `codecheck.mjs` runs the Python widgets in Pyodide; `fresh.py` and `tagscan.py` are the freshness greps.

Ramp 6, 15, 6, 3 at difficulty 2, 3, 4, 5, in that order in the file, courses interleaved. Kinds: 13 numeric, 6 choice, 3 multi, 2 order, 1 table, 1 tap-regions, 1 parts, 3 code (two Python, one C++). All 13 skills are in the `skills` map and tested: sy-memory 5; rq-linalg, rq-ml, ci-timed, sy-latency 4; rq-stats, ci-patterns, ci-strings, ci-design 3; rq-case, rq-data, sy-concurrency, sy-os 2. Every level has an item on a skill first met in it, or on one of its own lessons.

### Revisions to the brief's item plan, and why

Read from the written files, reports and the freshness greps:

1. **File order** is by difficulty (all 2s, then 3s, 4s, 5s), not by plan number. Item numbers below are the plan's.
2. **Item 3** (p-value): the plan's 12-signal example would have matched the mock key (0.006 against 0.004167). It uses eight signals, best p 0.011, bar 0.00625. Family `p-value-meaning` kept.
3. **Item 5** (ridge and lasso): the feature-scale twist is `research-int` l7 "Units first" (10,000-fold rescale). New idea in the same family: the penalty raised without limit, with an unpenalised constant.
4. **Item 8** (case steps): `homework-3` already orders target, horizon, loss, baseline and split. The case is now a weekly "beat the index" label with a five-day gap between train and test, plus two distractors.
5. **Item 14** (order): `homework-1` has the streaming-median order and l4 has the top-k order. Replaced by the two-singles XOR method (family `two-singles-xor`, skill `ci-patterns`).
6. **Item 20** (edge cases): `coding-int` l16 uses `longest_streak` with the same missed-last-run bug and `review-4` uses `second_largest`. New function `best_window` with a `<=` guard bug.
7. **Item 24**: the written lessons draw padding on a `grid` canvas (ids `r1c1` to `r3c8`, offsets 0 to 23), not an `array` canvas with `c0`. Followed the lessons.
8. **Item 30** (C++): l16's code widget is already a push and pop ring driven by `ops`. New function `newest_first(xs, capacity, k)`: an overwriting ring read back by mask, single-threaded.
9. **Item 10**: the drill `rq-group-slopes-py` returns a Series of slopes. The exam function `costliest_desk(df, min_rows)` returns the best group's name, with a guard for small groups and one distinct size, and handles all-negative slopes.
10. **Item 11**: skills are `rq-data`, `rq-linalg` (not `rq-case`, tested by items 8 and 9). The third part is the centred-sums stability choice. Numbers differ from l18 and the drill.
11. **Item 19**: budget 70 minutes (l15 uses 65) and new marks. **Item 22**: a seek against a data-centre round trip (20), not in the l1 table. **Item 25**: a 192 MiB buffer (l3 uses 512 MiB). **Item 6**: matrix 7, 2, 2, 4 (a first draft's 2/3 wrong key matched an l9 key). **Item 12**: halts and a sweep, since l2 covers prefix search on symbols.
12. Skill counts: `rq-case` was 2, not 3, because of revision 10. The second read added `rq-case` to item 11 (its third part is a judgement about a live system), so it is 3 again.

### Numbers computed twice

`check.py` (closed form, then enumeration, brute force, exact `Fraction` or a seeded simulation), asserted:

- 1: slopes 0.75 and 0.27 give r^2 = 0.2025, r = 0.45. Slips 0.2025, 0.51, 0.75.
- 2: -0.4 +/- 0.5196, top 0.1196, floor -0.9196 (bisection on the smallest eigenvalue of the 3 by 3 matrix).
- 3: 0.05/8 = 0.00625; chance of any p <= 0.011 in eight nulls 0.0847.
- 4: det(2I + 3ww^T) = 77 x 8 = 616 (numpy determinant and eigenvalues 2, 2, 2, 77). Slips 600, 1232, 77.
- 6: eigenvalues 8 and 3, share 8/11 = 0.7273 (200,000-draw simulation within 0.003). Slips 7/11, 3/11, 0.5.
- 7: t = 0.04 x sqrt(2500) = 2 (simulated sd of r is 1/sqrt(n)); 10,000 days for 0.02; costs 4 against 5.
- 9: persistence 3.2, fit 2.56, mean 4; cut 20% (1.5-million-step simulation within 0.03). Slips 80%, 36%, 40%.
- 11: slopes 9/5, 11/5 after arrival, 5/2 after departure (Fraction and polyfit; sums match). Slips 2.8, 1.8, 2.125, 2.2.
- 13: back pops 6, front pops 2 (deque run against brute-force window maxima). Slips 2, 8, 5.
- 15: 13 (two independent evaluators); floor 11, signs dropped 37, no precedence 5.
- 16: balances 380, 540, 600, 850, 600, 420 (two loops). Slips 270, 570, 320.
- 17: fills D 6 at 100.0, B 5, C 8 at 100.5, one unit rests (sorted match).
- 18: evictions R and S, final order Q, T, U, P (OrderedDict and a list).
- 19: 82 marks in 66 minutes, the unique optimum of all 81 mixes and by knapsack; full only 75, filling the clock 80, all parts 60.
- 20: each option checked against a correct and the planted version.
- 22: 10,000 / 500 = 20. 23: last read at byte 23,976, line 374, 375 misses (enumeration of lines). 24: g++ sizeof and offsetof give 24 bytes, padding at 1 to 3 and 10 to 15.
- 26: 2,000,000 x 0.3 x 14 = 8.4 million (simulated miss rate 0.3). 27: enumeration of all interleavings gives {0, 2, 6}.
- 29: rank ceil(0.96 x 25) = 24, value 2650 (also by cumulative share); mean 420, median 207, linear 2668.
- 10, 21, 30: model solutions against independent references (exact-slope Fraction search; a Fenwick-tree distinct count for the 100,000-call total; a plain ring reference and the C++ solution compiled with g++ under sanitisers).

### Code items and starters

`codecheck.mjs` (Pyodide 0.27.7): `e-active-symbols` solution 7 of 7 (slowest 0.19 s), starter passes 0 of 7, and a dict scan of all symbols on every call takes 183 s on the large test (stopped at 5 s). `e-costliest-desk` solution 7 of 7, starter passes 3 of 7 (the three tests that expect `None`). C++ (`check2.py`): solution passes 6 of 6, starter fails, and three wrong masks each fail at least one test. The playthrough also ran every solution in the app.

### Freshness

`fresh.py` (every content file, mock script and brief, also restricted to the three courses, mocks, bank, drills and exams) and `tagscan.py` (every other item sharing a family tag, listed and compared by eye). Hits that mattered are the revisions above. Remaining hits are shared family tags, which the brief allows, or bare numbers inside unrelated data series. No firm names.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for `topic-3.5.json`. It added one line to `content/manifest.json`, kept in the commit.
- Voice scan: 738 sentences, 0 over 20 words, 0 explanations over three sentences, no exclamation mark or em-dash.
- Every `choice` and `multi` has `"shuffle": true`; key against longest distractor 0.90 to 1.06.
- `playthrough.mjs --exam topic-3.5 --local-cdn <pkgs>`: 32 items (three parts), scored 30 of 30, passed. Again with `--mobile --shots --why`: passed.
- Screenshots at 1280 and 390 px looked at (start card, tap grid, tables, order, multi with code, parts, Python and C++ editors, results). Fixes: the five-column marks table clipped at 390 px (headers shortened); long comment lines in three starters ran off the editor (shortened). At 390 px the editor still scrolls sideways for long code lines.

## prep.json

`content/prep.json` lists no topic exams (as for topic-3.3). Not edited.

## course.json

No change proposed. The exam carries no `requires`.

## Backlog

Three bullets under "Raised later (exam topic-3.5):" in `docs/BACKLOG-INBOX.md`.

## Second-read changes (4 Nov 2026)

`docs/reviews/review-exams-3.5.md` and `docs/reviews/answers-2026-11-04-exam-3.5.md` are the sources; each fix is listed under `## Fix pass` there. `docs/briefs/exam-3.5-scripts/second_read_patch.py` holds them, and `build.py` calls it after writing the file, so the build reproduces the shipped JSON.
- `e-eight-looks` is now `e-six-looks` (six signals, best $p$ 0.012, bar $0.05/6$, corrected $p$ 0.072). `e-two-singles-steps` is now `e-next-higher-steps` (a stack pass for the next higher price, family `price-stack-pass`), because `coding-int` homework 1 already asks the two-singles XOR method.
- `e-window-inputs` uses `peak_window_total` and `e-newest-first` uses `latest_values`, since `best_window` and `newest_first` are functions in the `garch` and `ds` courses. `e-newest-first` has 7 tests, one over the cap above, to hold both a `k` above the capacity and a wrapped ring. `e-costliest-desk` has 8 tests, with one frame on which end-point slopes pick the wrong desk.
- `e-weekly-hit-case` merges features and the split into one step and accepts the baseline and the fit in either order (`same`). `e-sixty-five-minutes` is now `e-seventy-minutes`.
- The tolerances on `e-first-component` and `e-persistence-gain` are 0.5 points.
