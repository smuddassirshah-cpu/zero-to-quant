# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.

Cleared by engine pass AF part 1 (items up to 1081 in `ENGINE-BACKLOG.md`); the previous text is in the commit before it.

Raised later (triage AF hits):

- `retold` is too loose on short lines: 50 of the 93 hits that fire at HEAD stand (54%), 43 are reuse (`docs/reviews/review-reuse-af-hits.md`). Weight does not separate them (a standing recipe line scores 6.5, a retold lesson line 2.3), so the fix is in what counts as a sentence pair, not in the thresholds.
- False positive 1, one sentence counted as two (about half of the stands): the same string held in `widget.options[].why` and `feedback.byKey` of a choice part, or one rule said in `correct`, `generic` and `explain`, each matched to the same single source sentence ("2 retold sentences" for "Failing to reject is not proof."). Count distinct pairs: equal target keys once, and a source sentence backs one target sentence only.
- False positive 2, a rule or recipe in its only words (about half of the stands, overlapping the first): "dividing by $-18$ reverses the sign", "reversing the limits flips the sign", "use the divergence theorem", "divide the dot product by both lengths, then take the inverse cosine". These are stock inside one course and rare across the app. Learn stock sentences per course as well (a sentence key held by three or more files of the course).
- False positive 3, a match made by the masking alone (7 hits): with numbers, maths and rare nouns masked the skeleton left is "That is ..., the ... ending at ..." or "the standard error is" (`markov/problems-3` `p-barrier-note`, `proof/problems-3` `p-even-test-contra`, `eigen/problems-3` `p-branch-sales`, `testing/problems-1` `p-pizza-delivery`). Ask for three informative words in common, or refuse a pair where one sentence is mostly maths.
- The error line and `reuse-hits-report.mjs` print only the strongest pair of a hit. A reader and a fixer need every matched pair (a hit clears only when all but one are reworded): add `--pairs` to `same-course-reuse.mjs` and list them in the report. The triage used a scratch script for it.
- A waiver is keyed by file, item and kind, so waiving a standing rule line hides every later `retold` hit on that item. Add an optional `source` (file) or `text` field to the waiver and match on it.
- `rate`: 2 of 4 stand (0.75 squared against a 56.25% gain; the ruled 3/8). The other 2 are a real shared number set that the `numbers` kind missed: `exp-log/problems-1` `p-rare-coin` and `exp-log/problems-2` `p-drawdown-recovery` both turn on $1.5625 = 1.25^2$ (640 to 1,000 and 32,000 to 50,000). The `numbers` kind could read a ratio of two stated amounts. Exempt the eighths from `rate`.
- `docs/reports/same-course-reuse-af-hits.md` lists 94 hits; one (`ensembles/problems-3` `p-futures-study`) does not fire at HEAD, its sentence is not in the set. Regenerate the report at the commit it is filed with.
