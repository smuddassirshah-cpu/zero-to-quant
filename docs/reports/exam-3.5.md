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
