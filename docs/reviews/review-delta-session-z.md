# Delta read, session z: two fix passes

Scope: only what the two fix passes changed, at commit a46fd81.

- Fix pass 1 (problem sets): `git diff 2d3771e 7367096` on `counting-chance/problems-1` to `-3` and `conditional/problems-1` to `-3`. 18 of 24 items changed.
- Fix pass 2 (drills): `git diff f379218 99cf1f2 -- app/content/drills/`. 23 drill files and `index.json` changed.

Method. Each changed item and drill was read whole as it now stands, not only its changed lines. Every changed problem answer and `wrong` value was recomputed with exact fractions, then by enumeration (the 24 d4 and d6 pairs, all 4,845 short-deck hands, the 720 ordered three-call sequences, the 8 feed states) or simulation (the six-pick breach chance). Every numeric part of the six sets was listed with its answer, tolerance, form sentence and each value printed after `\approx`. For the drills I wrote my own solution to each of the 18 drills with changed tests, by a second method wherever one exists (binary search on length, heap, per-letter windows, sort and scan, divide and conquer for the products, sorting by height for the banner), and ran model, mine, starter and every planted solution on every example and hidden test in CPython. Both authors' scripts, both drill check scripts and the validator were run.

Scripts: `docs/reviews/delta-session-z-scripts/` (`problems.py`; `run.py <drill id> ...` with `mine.py`; `extra.py`), run from the repo root with the scratchpad venv Python.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` / `weak` = a statement reads two ways, or a hint misleads; `minor` = otherwise.

## Tool results

- `problems-counting-chance-numbers.py`: 611 of 611. `problems-conditional-numbers.py`: 1,105 checks, 0 failures (it now covers sets 1 to 5).
- `drills-ci-1-check.py`: `errors: 0`. `drills-ci-2-check.py`: `15 drills, 0 errors`.
- `node tools/validate.mjs`: 0 errors. It did not catch finding 5.
- My solutions: 18 of 18 pass every example and hidden test. No drill `expect` is wrong.
- Every planted solution the fixer added fails for the reason its sentence names (table under "Verified clean").
- No changed problem answer, tolerance or `wrong` value is wrong. No two bands overlap, and every `wrong` id has its `byKey` line.

## Findings: fix pass 1 (problem sets)

1. `wrong` | `conditional/problems-2.json` | `p-bad-ticks` | part 3, `explain.text`.
   The fix changed "a chance of $\tfrac{33.9}{34.9} \approx 0.971$" to "$\approx 0.9714$". $33.9 / 34.9 = 0.97135$, which is 0.9713 to 4 places. The answer 0.9714 is right ($\tfrac{0.0133}{0.013692} = 0.97137$); the line of working that claims to reach it is false. A learner who follows it types 0.9713, which the tolerance accepts, so nobody is marked wrongly.
   Fix: "The new odds are about 33.93, a chance of $\tfrac{33.93}{34.93} \approx 0.9714$." ($33.93 / 34.93 = 0.97137$.) Leave `feedback.correct` as it is.

2. `unclear` | `conditional/problems-3.json` | `p-odd-dice` | prose and part 3, `feedback.correct`.
   The new setting names a feed $P$. Part 3's feedback now reads "If desks 1 and 2 are calm, $P = Q = R$, so desk 3 is calm too. So $P = P(A \cap B) = \tfrac{1}{4}$." The same letter is the feed in one sentence and a probability in the next, and "$P = \tfrac{1}{4}$" reads as a value of the feed. The second sentence was carried over from the dice version, where no feed was called $P$.
   Fix: rename the feeds $F$, $G$ and $H$ throughout the item (prose, part 1 `correct`, `generic`, `certain` and `explain`, part 2 `depends`, part 3 `correct`, `generic` and `explain`), and end part 3's feedback "So $P(A \cap B \cap C) = P(A \cap B) = \tfrac{1}{4}$." Minimum: change only that last sentence.

3. `minor` | `conditional/problems-1.json` | `p-eight-sided` parts 1 to 3, `p-watchlist` parts 1 to 4, `p-dealer-calls` parts 1 to 3 | `explain.text`.
   The fix-pass note for finding 4 says "Where feedback or explain printed a 3-place value under a 4-place question, it now prints 4 places." That holds in `problems-2` and `problems-3` but not here: these ten parts ask for "a decimal to 4 places" and still print $\approx 0.109$, $0.133$, $0.286$, $0.278$, $0.571$, $0.159$, $0.476$, $0.267$, $0.167$, $0.833$. Every one is inside its tolerance, so no learner is marked wrongly. `p-bad-ticks` part 3 `skipped-a` also still says "the starting chance is 0.326".
   Fix: print 0.1094, 0.1333, 0.2857, 0.2778, 0.5714, 0.1587, 0.4762, 0.2667, 0.1667, 0.8333, and 0.3265 in `skipped-a`.

4. `minor` | `counting-chance/problems-1.json` | `p-tetra-eight` | part 5, `explain.text`.
   The new explanation rests on "Taking logs, $n > \tfrac{\ln 0.1}{\ln (15/16)} \approx 35.7$". Level 1 of counting-chance teaches no logarithms (the only `ln` in the course is inside a plot formula in l10). The numbers are right ($35.68$; $0.8955$ at 35, $0.9021$ at 36).
   Fix: "The bet wins with chance above 0.9 when $\left(\tfrac{15}{16}\right)^n < 0.1$. Trying values, $\left(\tfrac{15}{16}\right)^{35} \approx 0.1045$ and $\left(\tfrac{15}{16}\right)^{36} \approx 0.0979$. So the smallest $n$ is 36." In `generic` drop "or by taking logs".

## Findings: fix pass 2 (drills)

5. `wrong` | `app/content/drills/index.json` | rows `ci-zero-quads` and `ci-mean-stretches`.
   Review finding 18 swapped the two labels in the drill files (`ci-zero-quads` 3, `ci-mean-stretches` 4). The index rows were not changed: `index.json` still has `ci-zero-quads` at difficulty 4 and `ci-mean-stretches` at 3. The drill list and its difficulty filter read the index row (`screens/drill.js` line 417), and the drill page reads the file, so the list shows four dots for a drill whose own page says 3, and the filter files both drills under the wrong level. The fix-pass note says only "`index.json` name updated". These are the only two mismatches between the index and the 155 listed drill files (name, course, difficulty all compared).
   Fix: set `"difficulty": 3` on the `ci-zero-quads` row and `"difficulty": 4` on the `ci-mean-stretches` row. Engine item: the validator should fail when an index row's `name`, `course` or `difficulty` differs from the drill file.

6. `unclear` | `ci-mean-stretches.json` | `how`.
   The sentence moved across reads "The large tests need the step from checking every stretch to a dict of running totals less `target`." Read plainly that is a dict looked up at the running total less `target`, which is the method for stretches whose sum is `target`. That is this drill's own planted slip 3 ("It counts stretches whose sum is `target`, not stretches whose mean"). The hint has it right.
   Fix: "The large tests need the step from checking every stretch to a dict of the running totals of `x - target`."

7. `minor` | `ci-others-product.json` | `planted[1].slip`.
   The modulus is 10010 everywhere else, but this sentence still says "a cell can hold the product of two remainders, up to $12344^2$". It is the one number left from 12345. The sentence is read by tools and authors, not by learners.
   Fix: "up to $10009^2$".

8. `minor` | `ci-cancelled-to-back.json` | `id`.
   The id is now misleading: the drill has no cancelled orders and sends nothing to the back. The id shows in `index.json`, the manifest, the check script and the pack report, and progress is keyed on it. The drill was first committed on 2026-11-10 (ff4a79b), so no learner progress can hang on the id yet.
   Fix: rename now, before release, to `ci-reference-split` (file name, `id`, the `index.json` row, `IDS` and both dict keys in `docs/reports/drills-ci-2-check.py`, the row in `docs/reports/drills-ci-2.md`; the validator rewrites the manifest). If the id must stay, record that in DECISIONS so the next reader does not raise it again.

9. `minor` | `ci-widest-banner.json` | whole drill. Verdict asked for: acceptable, not good.
   The site's sample list is gone from tests[4] and notes[1] (54 from the two 9s, checked by my sort-by-height method), so the named part of review finding 14 is met. What is left is still the best-known two-pointer task with only the story changed, and the brief hands over the area formula. It meets the letter of the 1.8 brief ("write the task in your own setting, keep the pattern") and it does not meet the reader's own bar for the other pack 2 classics ("their own data and a changed return value or tie rule"). It can ship; it tests recall more than any other drill in the pack.
   Fix, when pack 2 is next opened: return `[area, width]` for the widest of the best banners. The two-pointer walk with a strict `>` update already finds that pair (checked against brute force on 20,000 random lists, 0 mismatches, in `extra.py`), so the model changes by one line and each planted solution by its return line.

10. `minor` | `docs/reports/drills-ci-1.md`, `docs/reports/drills-ci-2.md` | tables.
    The pack reports were not brought in line with the fix: `drills-ci-1.md` still lists `ci-mean-stretches` at 3 and 1350 and `ci-zero-quads` at 4 and 1800, and both tables carry the old hidden-test and planted counts for the 12 drills that gained a test (for example `ci-cancelled-to-back` "12 | 3", now 14 tests).
    Fix: update the rows, or add one line under each table: "Counts as authored; see `docs/reviews/review-drills-ci-1-2.md`, Fix pass, for later changes."

## The six drills named in the brief

- `ci-cancelled-to-back` (now `split_by_reference(sizes, ref)`). Fresh: no `dsa-`, `oa-` or other `ci-` drill is a partition (searched all drill files for partition, pivot, three-way, and read the names and return lines of every two-pointers and in-place drill; the nearest is `dsa-empty-orders-back`, which moves zeros and keeps order). Fully specified: strict comparison on signed sizes, order inside a part free, both boundaries returned as a tuple, the empty list and a missing `ref` covered by an example and tests 0 to 3 and 5 to 7. The 14 `expect` values agree with my sort-and-bisect solution. A list return, a count in place of the second boundary, and a two-way split with the equal sizes left in the back part each fail (0, 6 and 11 of 16 pass). `pop` and `insert` takes 13.1 s natively over the three large tests, so the constraint line is true. `sizes.sort()` and two counts passes every test; `how` says the tests check the result, which is honest and enough at difficulty 2. The id is finding 8.
- `ci-others-product`. Modulus 10010 agrees in brief, constraints, hint, both examples and notes, solution, all four planted codes and every test; the stale 12344 is finding 7. All 13 `expect` values agree with my divide-and-conquer solution (the grid of 2s gives $2^{99999} \bmod 10010 = 7288$ per cell, sum 728,800,000). The new planted hybrid is correct on every small test and runs out of time on tests 9, 10 and 12, for the reason named.
- `ci-widest-banner`: finding 9.
- `ci-zero-quads` and `ci-mean-stretches`. Files are right: 3 and 1350, 4 and 1800; the "large tests need the step" sentence sits on the 4 only, as the packs brief asks; pack 1 is still 3 / 5 / 5 / 2 by the files. The new zero-quads example and note are right (pair sums -1, 3, 0, 4 and 0, -3, 5, 2; two combinations). The index rows are finding 5 and the moved sentence is finding 6.
- `ci-capped-repeats`. The brief and the note now say 5, the example and test 4 expect 5, and 5 is right: `'b', 'a', 'a', 'c', 'b'` holds `'a'` and `'b'` twice each, and all six entries hold `'a'` three times. Hint and notes agree.

## Was each review finding resolved

Fix pass 1, review findings 1 to 18: all resolved or declined with a sound reason. Checked in particular: finding 1 (`from-chance` 260,361 with `tol` 0 is right, since a band of 1 would swallow the key); finding 3 and 13 (3 decimal places, `tol` 0.0005 on key and slips: typing 5.536 passes, and the `difference` band now covers only 0.0040 to 0.0050); finding 9 (superseded by 18, and the new `adding` slip $n = 15$ is the strict form); finding 17 (`p-odd-dice` part 5 left in place, as the review allowed). New faults introduced: findings 1 to 4 above.

Fix pass 2, review findings 1 to 23: all resolved, with two "better" options declined (the `ci-peak-stretch` return value and the `ci-even-vowels` letter set) for a stated reason; the named sample data is gone from all fourteen drills. Finding 18 is only half applied (finding 5 above). New faults introduced: findings 5 to 8 and 10.

## Verdict

- Fix pass 1 (problem sets): **returns to the fixer**, for text only. `wrong` 1, `unclear` 1, `minor` 2. No answer, tolerance or `wrong` value needs to change; findings 1 to 4 are edits to `explain` and `feedback` strings and eleven printed decimals.
- Fix pass 2 (drills): **returns to the fixer**. `wrong` 1, `unclear` 1, `minor` 4. Finding 5 is two numbers in `index.json`; findings 6 and 7 are one sentence each; 8 needs a decision; 9 and 10 can wait.

## Verified clean

Problem sets, changed graded answers (each recomputed twice, with its `wrong` values, `accept`, feedback and explanation read against the unchanged parts):

| item, part | answer | check |
|---|---|---|
| `p-d4-against-d6` 4 | £9 | 18 of 24 pairs pay; slips 7, 6, 3 are $12 \times \tfrac{7}{12}$, $12 \times \tfrac{1}{2}$, $12 \times \tfrac{1}{4}$ |
| `p-tetra-eight` 5 | 36 | 0.8955 at 35, 0.9021 at 36; slips 15 (0.6202), 11 (0.5083), 35 |
| `p-breach-check` 5 | 6 | 0.7582, 0.8462, 0.9077 at 4, 5, 6; $\tfrac{462}{5005}$; simulation 0.9075; slips 5, 4, 8 |
| `p-ace-and-king` 4 | 260,360 | $2 \times 886{,}656 - 1{,}512{,}952$; slips 302,490 (302,489.8) and 260,361 (260,361.2) |
| `p-short-deck` 5 | 2,880 | enumeration: 2,880, 1,280, 360, 320, 5; slips 3,565, 2,885, 2,520, 3,240 |
| `p-dealer-calls` 4 | $\tfrac{8}{13}$ | 192 and 120 of 720 ordered triples; slips 0.32, 0.2667, 0.3846, 0.625 |
| `p-bad-ticks` 4, 5 | 392; 0.0286 | 392 and 13,300 of 1,000,000; slips 39,200, 400; 0.0004, 0.0295, 0.9714 |
| `p-three-loans` 4 | 5.536 | exact; slips 0.1806, 0.004536, 22.016 |
| `p-odd-dice` 1 to 5 | 0.5, choice, 0.25, 1, 0.8999 | 8 feed states: each pair $\tfrac{1}{4}$, triple $\tfrac{1}{4}$; $1 - 0.75^8$; slip 0.6564 |

Also clean: the 35 form sentences (every part whose answer does not end within 3 places now states its form, and its tolerance accepts the answer rounded as asked); `p-octahedral-prize` (label 3, `only-a`); `p-relay-team`; `p-eight-sided` part 3 (no longer states its own answer); `p-watchlist`; `p-order-router` (prose, "The original router"); `p-takeover-rumour` (0.3947, 0.1176); `p-downgrade-news` (odds as one number; 0.1765, 0.5294, 0.7606); `p-broker-algo` (0.3478, 0.5161, 0.6185); `p-gap-days` (0.3845, 0.8215); `p-losing-week` (0.6316).

Drills, planted solutions added by the fixer (each passes every other test):

| drill | fails | returns | reason named |
|---|---|---|---|
| `ci-best-block` | test 13 | -1,000,000,000 for -1,600,000,000 | start at $-10^9$ |
| `ci-ends-to-target` | test 11 | 3 for -1 | ends overlap |
| `ci-equal-three` | test 11 | `'1'` for `'0'` | glued key |
| `ci-others-product` | tests 9, 10, 12 | out of time | quadratic where cells share a factor |
| `ci-paired-signals` | test 11 | 14 for 6 | `if`, not `while` |
| `ci-peak-stretch` | test 9 | 3 for 2 | last badge wins |
| `ci-rota-swaps` | test 12 | 4 for 5 | two end letters |
| `ci-row-column-matches` | test 9 | 2 for 1 | glued key |
| `ci-serial-runs` | test 12 | out of time | list loop |
| `ci-three-leg-nets` | test 11 | `[]` | early `break` on a negative target |
| `ci-cancelled-to-back` | 7, 8 and 9 of 16 | wrong parts or boundaries | three slips as named |

Drills clean in full (statement, examples, notes, tests, planted): `ci-best-block`, `ci-camera-cover`, `ci-capped-repeats`, `ci-code-classes`, `ci-ends-to-target`, `ci-equal-three`, `ci-even-vowels` (the new test 9 is right: each vowel twice, 15), `ci-late-fills-merge`, `ci-paired-signals`, `ci-peak-stretch`, `ci-rota-swaps`, `ci-row-column-matches`, `ci-serial-runs`, `ci-steady-climbs`, `ci-target-blocks` (new example 4 and test 8 by brute force), `ci-three-leg-nets`, `ci-trim-to-multiple` (the new test `[4, 3, 1]`, 5 catches the no-wrap slip, which returns -1), `ci-unique-counts`, `ci-zero-quads` (file). The time-limit sentence and the `how` test count are right in all 30 drills of packs 1 and 2.

## Counts

| fix pass | wrong | unclear / weak | minor | verdict |
|---|---|---|---|---|
| 1, problem sets | 1 | 1 | 2 | returns to the fixer |
| 2, drills | 1 | 1 | 4 | returns to the fixer |

## Fix pass

1. fixed: `p-bad-ticks` part 3 explain now reads "about 33.93, a chance of 33.93/34.93 ≈ 0.9714" (33.93 / 34.93 = 0.97137).
2. fixed: `p-odd-dice` feeds renamed F, G, H throughout (prose, parts 1 to 3); part 3 feedback ends "So $P(A \cap B \cap C) = P(A \cap B) = \tfrac{1}{4}$."
3. fixed: conditional `problems-1` ten explains now print 0.1094, 0.1333, 0.2857, 0.2778, 0.5714, 0.1587, 0.4762, 0.2667, 0.1667, 0.8333 (each recomputed from its fraction); `p-bad-ticks` `skipped-a` now 0.3265.
4. fixed: `p-tetra-eight` part 5 explain and `generic` no longer use logs; they try 35 and 36 ((15/16)^35 = 0.1045, (15/16)^36 = 0.0979).
5. fixed: `index.json` `ci-zero-quads` 3 and `ci-mean-stretches` 4; a full compare of all 155 rows (name, course, difficulty) found no other mismatch. Engine item stays: validator should compare index rows to files.
6. fixed: `ci-mean-stretches` how now says "a dict of the running totals of `x - target`".
7. fixed: `ci-others-product` planted[1] slip now says $10009^2$.
8. fixed: renamed `ci-cancelled-to-back` to `ci-reference-split` (file, id, `index.json`, `drills-ci-2-check.py`, `drills-ci-2.md`, `review-drills-ci-1-2.md` with a note, `delta-session-z-scripts/extra.py`); the manifest is regenerated by the validator and left out of the commit. This review's own text keeps the old name as history.
9. fixed: `ci-widest-banner` returns `[area, width]` (widest of the best; `[0, 0]` when no banner has area above 0). Brief, hint, three examples, 14 tests, solution, a fourth planted (`>=` update, narrower tie wins), the check script's independent method and slow method updated. Every `expect` agrees between the pointer model, an all-pairs brute force and a sort-by-height method; 20,000 random lists and 300 lists up to 400 posts agree. Large tests: [2500000000, 50000] and [95000000000, 100000].
10. fixed: counts line added under the pack 1 and pack 2 reports.

Checks: four number scripts exit 0 (1,177 and 611 checks, 0 failures); both drill check scripts 0 errors; validator 0 errors; playthrough green with and without `--mobile` for the five changed drills and four problem sets; `planted-check --require` passes for `ci-reference-split` (3), `ci-widest-banner` (4) and `ci-others-product` (4). Graded answers changed: only `ci-widest-banner` (all 14 tests and 3 examples now expect a pair).
