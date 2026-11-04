# Answer check, 4 November 2026: mock-oa-code

**Summary.** 8 problems checked (`oa-product-windows`, `oa-rain-water`, `oa-min-jumps`, `oa-merge-cost`, `oa-remove-digits`, `oa-rising-run`, `oa-decodings`, `oa-critical-path`), 89 hidden tests, plus the exam file. Wrong keys: 0. Wrong tests: 0. Reference-versus-mine disagreements: 0. Starters failing: every one fails at least one test (7 of 10, 7 of 11, 9 of 11, 8 of 10, 12 of 12, 10 of 11, 9 of 12, 11 of 12, matching the brief). Mismatches: 6 test-coverage gaps (wrong solutions that pass every test), 3 statement ambiguities, 2 voice items, 1 note on a drill-library effect. No duplicate problem found.

Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-mock-oa-code/`:

- `mine.py` is my own solution to each statement (prefix and suffix maxima for water, layer-by-layer reach for jumps, two-queue merge, a table for decodings, and so on). I wrote it from the statements without reading `docs/briefs/mocks-scripts/` or the report.
- `brute.py` holds exhaustive methods: every block, level-by-level flooding, a forward table, all merge orders, all digit subsets, all subsets for the rising run, recursion for decodings, cycle-checked longest path.
- `run.py` runs the stored `solution`, mine and the starter on every hidden test, then 1,500 seeded random small cases per problem against the exhaustive method. `mut.py` and `mut2.py` run 50 plausible wrong solutions against the stored tests with a 3 s limit.

## Per problem

| Problem | Tests | Verdict | Evidence |
|---|---|---|---|
| `oa-product-windows` (3) | 10 | Keys right. Gap: no `k <= 0` | Stored solution, mine and the exhaustive method agree on all 10 tests and 1,500 random cases. Starter fails 7. Largest test 0.03 s in CPython. Quadratic with early break times out on test 9. `<=` slip fails test 3. Singles-only and longest-block fail 5 and 6 tests. A solution guarded by `k == 1` (not `k <= 1`) passes every test, because only `k = 1` is tested. |
| `oa-rain-water` (3) | 11 | Right | All agree. Starter fails 7. Quadratic scans time out on tests 9, 10, 11. Adjacent-only, one-sided and first-peak slips fail 4 tests each or more. Empty, one bar and rising are covered. |
| `oa-min-jumps` (3) | 11 | Keys right. Gap: forward-relaxation table passes | All agree. Starter fails 9. Back-looking quadratic fails 9 and 11. Largest-jump greedy fails 1 and 6. A missing `-1` fails test 4. A forward table (`for j in range(i+1, i+a[i]+1)`) passes all 11 because no large test has big entries: the work is the sum of `nums`, 400,000. On `[200000] * 200000` it is 2 x 10^10 steps, and the answer is 1. |
| `oa-merge-cost` (3) | 10 | Keys right. Time risk | All agree, and the closed forms (2,228,224; 2,097,152) and the 81,782,502,640 total match my two-queue method. Starter fails 8. Scanning for the minimum and sorting each round fail 8 to 10. `pop(0)` plus `bisect.insort` passes: 2.0 s on test 10 and 3.0 s on test 8 in CPython. That is borderline for Pyodide (about 2 to 4 times slower), so the same code may pass or fail by machine. At 200,000 sticks it takes 8.3 s, and the constraint allows 200,000. The reference takes 0.05 s there. |
| `oa-remove-digits` (4) | 12 | Right | All agree. Starter fails 12. `>=` pop fails 7 and 11. A missing tail trim fails 4 tests. Missing leading-zero strip fails 4 and 9. Empty string, `"0"` and all-zero results are covered. A single `if` in place of the `while` fails only test 10, none of the small tests: add a small case. |
| `oa-rising-run` (4) | 11 | Right | All agree. Starter fails 10. `bisect_right` fails 1, 4, 11. Quadratic table fails 9 to 11. Adjacent-run and greedy fail 7 and 8 or more. Ties, empty, one entry covered. |
| `oa-decodings` (4) | 12 | Keys right. Gap: no pair `20` | All agree. Starter fails 9. Missing modulus fails 9 and 12. Recursion fails 9 to 12. Accepting `00` or `06` fails 6, 8, 12. `< 26` fails test 1. A solution that treats pairs 10 to 19 and 21 to 26 as valid but leaves out 20 passes every test: no test has the pair `20`. The 835,799,900 and 911,435,502 values match my table. A solution that reduces modulo once at the end is right in Python and cannot be told apart, which is fine. |
| `oa-critical-path` (4) | 12 | Keys right. Gap: partial cycles | All agree. Starter fails 11. Recursive search fails 4, 9, 10, 12. No cycle check fails 4, 9, 12. A solution that returns -1 for any self-loop or when there is no free task passes all 12. Cycles in tests 4 and 12 cover every task, and test 9 is a self-loop. No test has a multi-task loop beside tasks outside it, or a loop downstream of a free task. Duplicate pairs (test 5) and `n = 0` are covered. |

Time limits are fair: every reference run is at most 0.09 s in CPython, so Pyodide stays under 1 s against the 5 s limit. Building the large inputs adds nothing noticeable.

## Exam file

`app/content/exams/mock-oa-code.json` matches the brief field by field. `models` is 171 characters, and `description` equals the brief text with every sentence under 20 words. The paper has `minutes: 60`, `pass: 0.5` and `scoring` of 1, 0, 0. Both checks and the two `draw` entries (difficulty 3 and 4, `n: 1`) are as written. Draw maths: four problems per difficulty, so `n = 1` leaves four, over twice `n`. Paces are 1,200 s and 1,800 s, 3,000 s in all, ten minutes spare. `passNet` is absent, which is right with `pass`. Firm names appear only in `models`. All eight difficulty labels, patterns and tags match the brief, and each has a row in `drills/index.json`.

## Duplicates (DECISIONS "Duplicates")

I searched every JSON file in `app/content/` (courses, exams, bank, drills) for the eight function names, the drill ids, every example and test argument list, and the keywords for each problem. No other file holds any of the eight problems, and no function name is reused. Only generic inputs recur: `list(range(200000))` and its reverse (used for other functions in `ds` l6, l10, l11, `contests` l1 and homework-3), and `[1, 1, 1, 1]`. These are too plain to count as reuse. Concept overlap only: `graphs-dp` l5 teaches topological order, `ds` l6 and `coding-int` l3 teach windows. None shares numbers.

## Mismatches

1. `app/content/drills/oa-min-jumps.json`, `tests`: a forward-relaxation table passes every test. Add `{ "call": "min_jumps([200000] * 200000)", "expect": "1", "compare": "equal" }`. Update `how` to 12 tests and the starter-fails count.
2. `app/content/drills/oa-decodings.json`, `tests`: no pair `20`. Add `count_decodings("2020")` expecting `1`, and `count_decodings("260")` expecting `0`. Update `how` to 14 tests.
3. `app/content/drills/oa-critical-path.json`, `tests`: no multi-task loop beside free tasks. Add `critical_path_length(4, [[0, 1], [2, 3], [3, 2]], [1, 1, 1, 1])` expecting `-1`, and `critical_path_length(3, [[0, 1], [1, 2], [2, 1]], [1, 1, 1])` expecting `-1`. Update `how`.
4. `app/content/drills/oa-product-windows.json`, `tests`: no `k <= 0`. Add `count_products_below([3, 4], 0)` and `count_products_below([3, 4], -5)`, both `0`. Update `how`.
5. `app/content/drills/oa-merge-cost.json`, `tests`: add `min_merge_cost(list(range(1, 200001)))` expecting `347128407168` (my two-queue method, 0.05 s). It makes `pop(0)` plus `insort` (8.3 s) fail clearly instead of passing at 2 to 3 s. Update `how`.
6. `app/content/drills/oa-remove-digits.json`, `tests`: only test 10 catches a single `if` in place of the `while`. Add a small case: `smallest_after_removing("1432219", 3)` expecting `'1219'`. Update `how`.
7. `app/content/drills/oa-decodings.json`, `brief`: the statement does not say a code has no leading zero. Add "A code never starts with 0, so 06 is not a letter." Keep each sentence under 20 words.
8. `app/content/drills/oa-critical-path.json`, `brief` and `constraints`: durations are not bounded, and a pair `[a, a]` is a loop only by test 9. Add "Each duration is a whole number of at least 0. A pair `[a, a]` is a loop." Note also that the constraint says up to 200,000 pairs, but the largest test has 100,000. Either add a 200,000-pair test or change the constraint to 100,000.
9. `app/content/drills/oa-product-windows.json`, `brief` (the Example sentence): "For `nums = [5]` and `k = 6` the only block is `[5]`, its product 5 is below 6, so the answer is 1." is 20 words with code spans as one word each. The rule is under 20. Shorten, for example "For `nums = [5]` and `k = 6` the one block has product 5, so the answer is 1."
10. `app/content/drills/oa-critical-path.json`, `examples[0].note`: "Then task 2 takes 4 and task 3 takes 1, so the longest chain is 3 + 4 + 1 = 8." counts 22 tokens. Split into two sentences.

Note, not a mismatch: tests 10 and 11 of `oa-remove-digits` use `== "..."` expressions with expected `True`, so a wrong answer shows only `False`. The brief chose this for size. It is acceptable as the results panel names the test.

The drill library lists the pool (the brief records this as an inbox bullet), so a learner may meet a problem in `#drill` before the mock draws it. No fix needed here.

## Fix pass

Source of truth is `docs/briefs/mocks-scripts/oa_code.py` (tests, statements) and `oa_code_build.py` (examples, constraints). Both were edited, rerun (`ALL AGREE: 8 problems`, voice clean), and the six drill files regenerate with only the changes below (the baseline run reproduced all eight files byte for byte first). `docs/briefs/mocks.md` section `## mock-oa-code` now embeds the new `oa_code_section.md` tables and says 11 to 14 tests. New test numbers are given as they now stand; later tests moved down by the number added.

1. `oa-min-jumps`: fixed. Added test 12 `min_jumps([200000] * 200000)` expecting `1` (closed form). The forward-relaxation table now fails it by time. `how` says 12.
2. `oa-decodings` tests: fixed. Added test 9 `count_decodings("2020")` expecting `1` and test 10 `count_decodings("260")` expecting `0`, both checked against the exhaustive method. The solution without pair 20 fails test 9. The old large tests are now 11 to 14. `how` says 14.
3. `oa-critical-path` loops: fixed. Added test 10 `critical_path_length(4, [[0, 1], [2, 3], [3, 2]], [1, 1, 1, 1])` and test 11 `critical_path_length(3, [[0, 1], [1, 2], [2, 1]], [1, 1, 1])`, both `-1`. The self-loop-or-no-source solution fails both. Old large tests are now 12 to 14. `how` says 14.
4. `oa-product-windows` k <= 0: fixed. Added test 9 `count_products_below([3, 4], 0)` and test 10 `count_products_below([3, 4], -5)`, both `0`. The solution guarded only for `k == 1` without a bound check raises on both. Old large tests are now 11 and 12. `how` says 12.
5. `oa-merge-cost` insort: fixed. Added test 11 `min_merge_cost(list(range(1, 200001)))` expecting `347128407168` (two-queue method, recomputed). `pop(0)` plus `insort` takes 8.9 s in CPython and 24 s in Pyodide on it (5.6 s in Pyodide already on test 10), against a 5 s limit. The reference takes 0.23 s in CPython and 0.26 s in Pyodide. `how` says 11.
6. `oa-remove-digits` single `if`: fixed, with a different case from the one proposed. I recomputed `smallest_after_removing("1432219", 3)`: it gives `'1219'` and so does the single-`if` solution, so it cannot separate them. Added test 10 `smallest_after_removing("2561", 2)` expecting `'21'` (the top two digits both pop at the `1`; single `if` gives `'25'`). Old large tests are now 11 to 13. `how` says 13.
7. `oa-decodings` brief: fixed. Added "A code never starts with 0, so 06 is not a letter."
8. `oa-critical-path` brief and constraints: fixed. Brief now adds "Each duration is a whole number of at least 0. A pair `[a, a]` is a loop." The constraint now says up to 100,000 pairs, which the largest test uses, instead of adding a 200,000-pair test.
9. `oa-product-windows` example sentence: fixed. Now "For `nums = [5]` and `k = 6` the one block has product 5, so the answer is 1." (under 20 words).
10. `oa-critical-path` `examples[0].note`: fixed. Split into "Task 0 takes 3. Then task 2 takes 4 and task 3 takes 1. So the longest chain is 3 + 4 + 1 = 8."

Changed tests (all `compare: "equal"`): `oa-min-jumps` 12; `oa-merge-cost` 11; `oa-remove-digits` 10; `oa-decodings` 9 and 10; `oa-critical-path` 10 and 11; `oa-product-windows` 9 and 10. No existing expected value changed, so no graded answer changed. No test is over the 15 cap (largest is 14).

Checks. `node tools/validate.mjs`: 0 errors. `playthrough --drills --local-cdn`: all passed, all eight `oa` drills pass every test with the model solution and the starter fails. `--exam mock-oa-code` passes with and without `--mobile`. Checker mutants (`wmut.py`, `wmut2.py` in the scratchpad folder, 3 s limit): every wrong solution named above now fails (insort at tests 10 and 11 in CPython by time; forward-relaxation table at 12; no-20 at 9; self-loop-only at 10 and 11; unguarded k at 9 and 10; single `if` at 10). Five mutants still pass everything, and each is correct or equivalent (guarded `k` loop, no empty-list special case, one modulus at the end, deduped edges with matching in-degrees, strip-before-truncate), as the review found.
