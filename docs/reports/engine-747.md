# Engine 747: test-out draws 5, pass at 4

Decision: user, 9 Nov, `docs/reports/review-size-audit.md` route 1.

## Changes
- `app/js/prereq.js`: `TESTOUT_N` 6 to 5. The pass count is derived in `review.js` as `ceil(n x pass)`, so 5 items at 0.8 pass at 4. No learner-facing text (lock card, Today, test-out intro) states a count, so none changed.
- `app/js/screens/review.js`: the comment "up to 6 items" now says 5 (number only; the file is owned by the Fluency agent).
- `app/tools/test-met-rule.mjs`: rule 2 test now 4 of 5; new test 747 pulls the real `hashOf`, `rngOf` and draw expression out of `review.js` and checks that two successive papers of a 10-item review share no item and of an 8-item review exactly 2, over four level keys.
- `app/tools/playthrough.mjs`: two fixtures that wrote `items: 6` now write 5.
- `docs/AUTHORING.md` section 11: "Up to 5 items", "4 of 5 at 0.8", "10 or more review items" (8 repeats 2, 5 repeats all). `docs/LEVEL-BRIEF.md` states no test-out size (review is 6 to 10 items), unchanged.
- `tools/test-today-tested-out.mjs` assumes no count; unchanged.
- Stored state untouched.

## Open
- Reviews of 6 to 9 items still repeat items on a retake; only 10-item reviews give two disjoint papers (validator caps reviews at 10).
