# Engine pass 8 part B: same-course reuse

Built in `app/tools/`: exam items as sources (`same-course-reuse.mjs`, a skill-to-course map from `course.json`; the line names the exam file and item id); the three `retold` false-positive classes and the identical slip line (`retold-reuse.mjs`); `--pairs` on both commands and every pair in `reuse-hits-report.mjs`; waivers with `source`; `fresh-check.mjs --files`, normal quantiles as stock, `rate` skipping eighths and a decimal on a variable. Test: `test-fresh-check-pass8.mjs` (33 checks; `test-fresh-check.mjs`, `-same-course-ae` and `-retold-af` still pass). Validator 0 errors.

Exam hits are warnings for the 149 sets of `tools/reuse-baseline.json`, tagged `[exam-reuse]`; a new set fails on them (`--exam-errors` fails all). Hits that rest on an identical slip line alone are tagged `[slip-line]` and behave the same. `--all`: 0 errors, 188 warnings, 28 waived, 38 s.

Also fixed: the sentence index of `--all` left out the first set of each course as a source.

## Counts

- Triaged hits of `review-reuse-af-hits.md`, re-run on the content of commit 59df5f54 (93 fire): `stands` 50 to 22 (28 no longer fire), `reuse` (reword plus re-author) 43 to 37 (6 no longer fire: `p-photo-mount`, `p-renewals`, `p-cereal-boxes`, `p-bakery-loaves`, `p-two-buoys`, `p-italic-letters`, each against one source, short pairs of 2 informative words).
- New hits at HEAD: 188 (12 exam sources: 2 `[exam-reuse]` retold or text, 2 text, rest `[slip-line]`; 186 identical slip lines). List: `docs/reports/engine-pass-8-reuse-hits.md`.
- Time: `fresh-check --file` on `arma/problems-3` 54 s to 34 s; `--files` of three sets 34 s.

## Not built

The numbers kind reading a ratio of two stated amounts; a content-word Jaccard advisory; a story test on rare nouns; a run of six masked tokens; the canvas number runs.

## Inbox bullets closed (first six words)

- "`retold` is too loose on short lines"; "False positive 1, one sentence counted"; "False positive 2, a rule or recipe"; "False positive 3, a match made"
- "The error line and `reuse-hits-report.mjs` print"; "A waiver is keyed by file, item"
- "`rate`: 2 of 4 stand" (the eighths only); "`tools/fresh-check.mjs` kind `rate`: a derivative coefficient"
- "`fresh-check.mjs` missed an identical short feedback"; "`fresh-check.mjs` `retold` missed slip lines of two"; "`fresh-check.mjs --file` gave 0 hits on `stat-models/problems-4`," (slip line); "`fresh-check.mjs --file` gave 0 hits on `convex/problems-4`,"
- "`fresh-check.mjs --file` takes about 50 s"; "`fresh-check.mjs --file` takes about two minutes"
- "`fresh-check.mjs` lists "2 shared parameters (2.3263 99)""
- Exams: "Same-course reuse does not read the exams"; "`fresh-check.mjs --file` on a problem set does not read the exams"; "`fresh-check.mjs --file` on a course's problem set does not read"; "`fresh-check.mjs --file` same-course mode loads only the course folder"; "`fresh-check.mjs --file` kind `retold` does not read the topic exam"; "The same-course checker reads no exam" (both bullets); "`fresh-check.mjs --file` does not read the stage exams"; "`fresh-check.mjs --file` gave 0 hits on `stat-models/problems-1`" (exam part); "`fresh-check.mjs --file` (retold, chain test) did not fire"
- Partly: "`retold` missed slip lines that keep" and "`retold` misses a slip line that differs by one word" (identical or one-number lines only); "`retold` missed three skeletons that differ only in their numbers" (slip lines only)
