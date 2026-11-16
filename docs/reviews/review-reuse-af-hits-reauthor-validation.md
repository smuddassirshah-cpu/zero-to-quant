# Re-author, validation (session AF, brief `docs/briefs/reauthor-af.md`)

- `validation/problems-1.json` `p-arrears-grid` (id kept) parts 4 and 5. Old: part 4 the flattery of the best CV MSE 0.412 as a share of the nested 0.451 (8.6%), part 5 what the model card reports and which model is deployed, a walk of `l4-nested` `screens[11]` (and of `screens[6]`, `screens[8]`). New: part 4, on the stated learning curve $0.33 + 40/n$, the amount by which the nested score (outer refits on 480 accounts, part 3) overstates the model refitted on all 640: key 0.02083 (tol 0.0001; wrongs `inner` 0.0375, `inner-outer` 0.01667, `carried` 0.0125, `level` 0.41333); part 5, the fewest outer folds with overstatement $0.0625/(K-1) \le 0.007$ ($K = 10$) and the fits that run makes with part 1's 109-fit search: key 1090 (wrongs `nine-folds` 981, `no-refits` 1080, `added` 119). Part 5 is now typed, not a choice.
- Same item, part 2: `feedback.byKey.no-refits` reworded, since the review names it as `l4` `quiz[3]`'s sentence ("You left out the 4 refits, one per outer fold." is now "432 counts only the inner fits. Each outer fold then refits its own winner, so add 4."). Key and wrongs unchanged.
- Closest material, with the reasons, in `docs/reports/problems-validation.md` ("Re-author, session AF").

## Gates

- Validator: 0 errors; no warning on the edited parts (one pre-existing long-sentence warning on `items[3]`).
- Voice scan 35 on the course: 0 and 0.
- `fresh-check.mjs --file content/courses/validation/problems-1.json`: 0 hits, 0 errors (two pre-existing advisories on `items[0]` and `items[3]`).
- `same-course-reuse.mjs --all | grep validation`: nothing (the `p-arrears-grid` retold error is gone; the 11 errors left are other courses).
- `grade-all.mjs --file`: 19 widgets, 0 failures.
- Playthrough `--problems validation/problems-1 --local-cdn`: green (42 typed slips routed); `--mobile`: green.
- `docs/reports/problems-validation-numbers.py`: 737 of 737, exit 0. `docs/reports/problems-validation-numbers-read.py`: 991 of 991, exit 0, 0 FINDING; its arrears parts 4 and 5 checks are retargeted to the new keys (fit sizes taken from a counted 10-outer-fold nested run, smallest $K$ by brute force over real `KFold` training sizes).
