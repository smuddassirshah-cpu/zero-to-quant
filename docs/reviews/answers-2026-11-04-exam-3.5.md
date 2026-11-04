# Answer check, 4 November 2026: topic exam 3.5

**Summary.** 30 items checked in `app/content/exams/topic-3.5.json` (28 single items, one `parts` item of 3 parts, 3 code items; 13 numeric, 6 choice, 3 multi, 2 order, 1 table, 1 tap-regions). Wrong keys: 0. Other mismatches: 2 hidden-test gaps (a wrong solution passes), 2 duplicates, 1 name reuse, 1 order ambiguity, 1 explanation wording, 1 skill-tag difference from the brief. The exam reads no data file and has no `requires`, `generator` or `draw`.

Independent recomputation of every key, `wrong` value, option, tolerance and quoted figure. Brief taken from the Brief section of `docs/reports/exam-3.5.md` only. I read no other part of that report and nothing in `docs/briefs/exam-3.5-scripts/`.

Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-exam-3.5/`:

- `num.py` recomputes every numeric, choice and table key with `Fraction`s, enumeration (all 81 mixes for item 21, all 6 orders of the 4 steps in item 18, an LRU `OrderedDict`, a deque trace, a cache-line count, a field-offset walk, `numpy` eigenvalues and `polyfit`).
- `code_py.py`, `code_py2.py`, `code_py3.py` run the two Python code items: reference, starter, my own solutions and 18 wrong variants against the hidden tests (5 s alarm).
- `gen.py` builds the C++ harness (`g++ -O1 -fno-exceptions -std=c++17`) and runs reference, starter and 8 variants for item 30.
- `dups.py` and the greps in this report cover freshness.

## Mismatches

1. **`e-newest-first`, field `widget.tests` (and `how`).** No test has both `k` above `capacity` and more pushes than `capacity`. A solution that takes `min(k, count)` instead of `min(k, min(count, capacity))` passes all 6 tests and is wrong: it reads overwritten slots. Fix: add the test `newest_first([1..10], 4, 6)` expecting `[10, 9, 8, 7]`, and say "k above the capacity" in `how`.
2. **`e-costliest-desk`, field `widget.tests`.** A solution that uses the slope between the first and last row of each desk (end points, not least squares) passes all 7 tests. Fix: add a frame with desk `p` (size 1 to 4, cost 0, 9, 9, 6; end-point slope 2.0, fitted 1.8) and desk `q` (cost 0, 1, 7, 5; end-point slope 1.667, fitted 2.1) and `min_rows` 4. Expect `'q'`; the end-point answer gives `'p'`. Update `how`.
3. **`e-eight-looks`, fields `prose`, `options`, `feedback`, `explain` (duplicate).** `courses/testing/l10-correcting.json` "Eight signals" already uses 8 signals, α 0.05 and the threshold 0.05/8 = 0.00625. DECISIONS "Duplicates" asks for fresh numbers. Fix: take 6 signals and a best $p$ of 0.012. The bar is $0.05/6 = 0.00833$ and the corrected $p$ is $6 \times 0.012 = 0.072$; 0.012 still fails.
4. **`e-two-singles-steps`, whole item (duplicate of a problem).** `courses/coding-int/homework-1.json` `h1-two-singles` asks for the same algorithm (XOR all, isolate the lowest set bit, split, XOR each group) and the family tag repeats its idea. Only the format and the numbers differ. Fix: replace with another `ci-patterns` order item (for example the steps of a monotonic-stack "next greater price" pass, or counting set bits with `n & (n - 1)`), or record it as an accepted idea reuse.
5. **`e-newest-first`, `e-window-inputs`, field `starter`, `solution` and prose (name reuse).** The brief bans reused function names. `newest_first(ticks)` is a Python function in `courses/ds/l1-arrays-in-memory.json`, and `best_window(r, true_var, windows)` is in `courses/garch/l4-realised-vol.json`. Fix: rename to `latest_values` and `max_window_sum`, in prose, starter, solution, tests and the options of the multi item.
6. **`e-weekly-hit-case`, field `widget.answer`.** The order is not forced. "Build features known at each Friday's close" (s4) can come before "Split by date" (s3), and the baseline (s2) can come after the split. A sound learner can be marked wrong. Fix: put the order in the text, for example s3 "After the features, split by date, leaving a gap of five days" and s2 "Before any model, find the baseline hit rate..." and add a line to `explain` for it. Or merge s3 and s4.
7. **`e-two-statements`, field `explain.text`.** "A can read 0, B can finish and write 0, and then A writes 2" ends at 2, not 0, although the sentence introduces the value 0. Fix: "If B reads 0, A writes 2 and then B writes 0, the final value is 0."
8. **`e-online-slope`, field `skills`.** The brief lists `rq-data`, `rq-linalg`, `rq-case`; the item has only `rq-data` and `rq-linalg`. So `rq-case` is tested by 2 items, not the brief's 3 (items 19 and 25 here). Every skill is still tested. Fix: add `rq-case` to the item (its part 3 is a case judgement), or correct the count in the brief.

Notes, no fix needed:

- `e-tick-padding` uses a `grid` canvas, not the `array` canvas of the brief. Its ids `r1c2` to `r2c8` are one-based and right for a grid (byte $b$ is row $\lfloor b/8 \rfloor + 1$, column $b \bmod 8 + 1$). Table feedback ids `r0c1` to `r3c1` in `e-cache-evictions` are zero-based and match `table.js`.
- `e-seek-round-trips` uses 500 µs and 10 ms, the figures in the `systems` l1 table. No lesson, review or homework item asks the ratio 20.
- `e-penalty-limit` key is 87 characters against 82 for the longest distractor. Not visibly longer; leave.
- `e-costliest-desk` starter returns `None` and so passes 3 of 7 tests; it fails the other 4. The C++ starter fails 5 of 6.
- `e-weak-signal-claims` option b uses a correlation of 0.02, as a `research-int` l10 question does. The framing differs.

## Checks across the exam

| Check | Result |
|---|---|
| Items, kinds | 30; 13 numeric, 6 choice, 3 multi, 2 order, 1 table, 1 tap-regions, 1 parts, 3 code (2 Python, 1 C++). Agrees with the brief. |
| Ramp | difficulty 2: 6, 3: 15, 4: 6, 5: 3, non-decreasing. Agrees. |
| Pace | 5,310 s = 88.5 min of `minutes` 90. Agrees. |
| `requires`, `generator`, `draw` | none |
| Skills map | 13 skills, all tested. `sy-memory` 5, `ci-timed` 4, `sy-latency` 4, `rq-linalg` 4, `rq-ml` 4, `rq-stats` 3, `ci-patterns` 3, `ci-strings` 3, `ci-design` 3, `sy-os` 2, `sy-concurrency` 2, `rq-data` 2, `rq-case` 2 (brief 3, mismatch 8). |
| Level coverage | every level has an item on a skill first met in it, or a shared-skill item named in the brief (`coding-int` L3 `e-cache-evictions`, L4 `e-sixty-five-minutes`, `systems` L3 `e-feed-design`, L4 `e-newest-first`). |
| `wrong` ids against `byKey` | identical for all 13 numeric items; no `wrong` band overlaps the key band |
| `unit: "%"` stores the fraction | items 16 and 25: 0.7273 and 0.2 |
| Choice and multi | all `shuffle: true`, every distractor has a `why`, no key visibly longer, multi options unambiguous (checked by enumeration for items 18 and 23) |
| Voice | `voice-scan.py` 0 explanations over 3 sentences, 0 sentences over 20 words; no exclamation marks, no em-dashes, no firm names |

## Per item

| # | Item id | Key | My computation | Verdict |
|---|---|---|---|---|
| 1 | `e-two-slopes` | 0.45 | $0.75 \times 0.27 = 0.2025$, root 0.45. Wrongs: 0.2025, mean 0.51, 0.75. | Right |
| 2 | `e-halts-pattern` | a (sweep) | $+1$ at start, $-1$ at end, sort, running maximum. Others are wrong structures. | Right |
| 3 | `e-seek-round-trips` | 20 | $10{,}000/500 = 20$. Wrongs 0.05, 200 (500 µs as 0.05 ms), 2. | Right |
| 4 | `e-eight-looks` | a | $0.05/8 = 0.00625 < 0.011$; $8 \times 0.011 = 0.088$. | Right; duplicate (3) |
| 5 | `e-margin-rules` | £420 | Simulated: 380, 540, 600, 850, 600, 420. Wrongs 270 (cap at 700), 570 (no rule 3), 320 (half of whole balance) reproduced. | Right |
| 6 | `e-wrong-guesses` | 8,400,000 | $2\text{M} \times 0.3 \times 14$. Wrongs 14M, 28M, 19.6M reproduced. | Right |
| 7 | `e-third-correlation` | 0.1196 | $-0.4 + \sqrt{0.36 \times 0.75} = 0.11962$; the matrix's smallest eigenvalue crosses 0 there. Wrongs $-0.4$, 0.5196, $-0.9196$. | Right |
| 8 | `e-deque-back-pops` | 6 | Deque trace: back pops 6, front pops 2; strict rule 5; both 8. | Right |
| 9 | `e-stride-misses` | 375 | Byte $24k$, lines $\lfloor 24k/64 \rfloor$, counted distinct: 375. Wrongs 1000, 125, 333. | Right |
| 10 | `e-rank-one-det` | 616 | `numpy`: eigenvalues 2, 2, 2, 77, det 616. Wrongs 600, 1232, 77. | Right |
| 11 | `e-signed-division` | 13 | $-28/3 \to -9$, $17/-5 \to -3$, $25 - 12 = 13$. Floor 11, no signs 37, left to right 5, all reproduced. | Right |
| 12 | `e-tick-padding` | 9 bytes: r1c2 to r1c4, r2c3 to r2c8 | Offsets 0, 4, 8, 16; size 24; padding bytes 1 to 3 and 10 to 15. | Right |
| 13 | `e-penalty-limit` | a | Unpenalised constant gives mean 40; lasso exact zeros at finite $\lambda$; ridge tends to 40. | Right |
| 14 | `e-crossing-buy` | a | D 6 at 100.0, B 5, C 8 at 100.5; 1 unit rests; A above limit. Option b (arrival order, 20 units) and d reproduced. | Right |
| 15 | `e-first-write-fault` | a | 192 MiB / 4 KiB = 49,152 pages. Others contradict the malloc and TLB facts. | Right |
| 16 | `e-first-component` | 0.7273 | Eigenvalues 8 and 3, $8/11$. Wrongs 7/11, 3/11, 0.5. | Right |
| 17 | `e-cache-evictions` | R, S, Q, P | `OrderedDict`: step 7 evicts R, step 9 evicts S, order Q, T, U, P. | Right |
| 18 | `e-two-statements` | a, b, c | Enumerated all 6 interleavings: final values {0, 2, 6}. 8 impossible. Atomic and mutex claims hold; `volatile` does not. | Right; wording (7) |
| 19 | `e-weekly-hit-case` | s1 to s6 | A defensible order, but s3 and s4 can swap. | Ambiguous (6) |
| 20 | `e-two-singles-steps` | s1 to s4 | XOR all, lowest set bit, split, XOR each. x2 would corrupt both results. | Right; duplicate (4) |
| 21 | `e-sixty-five-minutes` | 82 | All 81 mixes: best 82 (part P1, full P2, parts P3 and P4, 66 min), unique. Full only 75, a plan of 80 uses all 70 min, all-partial 60 using 43 min. | Right |
| 22 | `e-weak-signal-claims` | a, b, c | $t = 0.04 \times \sqrt{2498}/\sqrt{1 - 0.0016} = 2.0008$; $0.02$ needs 10,000 days; 4 bp edge against 5 bp cost. d, e, f false. | Right |
| 23 | `e-window-inputs` | a, b, c | Ran the code: guard `<=` fails every input with exactly $k$ values; `[]`, `[1,2]` and the 4-value call are right. | Right |
| 24 | `e-feed-design` | a | One multicast copy, sequence numbers expose gaps, replay repairs. Others fail on copies, gaps or delay. | Right |
| 25 | `e-persistence-gain` | 0.2 | $2 \times 4 \times 0.4 = 3.2$; $4 \times 0.64 = 2.56$; $1 - 0.8 = 0.2$. Wrongs 0.8, 0.36, 0.4. | Right |
| 26 | `e-active-symbols` | 7 tests | Reference passes 7 of 7, starter fails 7 of 7. My queue-and-set, edge `<`, set-only, no-expire variants fail. Full scan and last-seen scan time out. A per-call distinct set takes 19 s against 5 s. Large total 581908999 agrees with my own solution. | Right; tests sound |
| 27 | `e-costliest-desk` | 7 tests | Slopes: north 2.1, east 0.29, south 6.0, west undefined. Expected names agree with my `groupby` solution. Variants `<=`, intercept, mean cost, absolute slope, correlation fail. End-point slope passes. | Right; gap (2) |
| 28 | `e-online-slope` | 2.2; 2.5; a | Sums $n = 5$: 15, 34, 55, 124: $110/50 = 2.2$. After removal 4, 14, 31, 54, 121: $50/20 = 2.5$. `polyfit` agrees. Wrongs 2.8, 1.8, 2.125 reproduced. | Right; skills (8) |
| 29 | `e-p96-latency` | 2650 | Sorted 24th of 25 is 2650; mean 420; median 207; interpolated 2668; maximum 3100. | Right |
| 30 | `e-newest-first` | 6 tests | Reference passes 6 of 6; starter fails 5 of 6. Wrong mask, shifted read, oldest first fail. `% capacity` is equivalent. No capacity cap passes. | Right; gap (1) |

## Freshness

Grepped `app/content/` (courses, drills, bank, exams), `docs/briefs/` (the three course briefs, `mocks-scripts/keys.json`) and `prep.json`. The four shared mock families have different keys: mocks hold 0.7 and 0.5, $-0.1913$, 135 and 0.7945; this exam has 0.45, 0.1196, 616 and 0.7273. The other 27 items reuse no numbers or inputs. The hits that need action are mismatches 3, 4 and 5.
