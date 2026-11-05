# Engine pass: performance pilots

Items 530 to 545 in `docs/ENGINE-BACKLOG.md`, from the 16 pilot inbox bullets. 13 done, 3 deferred (533, 536, 537).

## Changes
- `app/js/screens/review.js`: Mark my answer uses the widget's `ready()` instead of a bare text check (aloud boxes are optional); start-card plural fix; performance tag in header, overview and result row; start-card performance line.
- `app/js/engine/widgets/longform.js`: aloud notes label and placeholder; `required` rubric rows.
- `app/tools/validate.mjs`: `required` must be boolean, warning if all rows required; warning for `$` in an item title.
- `app/tools/playthrough.mjs`: starter-fails check for performance code items, real-button marking of every longform homework item (empty box refused unless aloud), `-marked` shots, `state.perf` assertion.
- `docs/AUTHORING.md` section 5 (Homework page bullet), `docs/ENGINE-BACKLOG.md`.

## Checks
- Reverting the 534 fix makes `--set research-int/homework-1` fail ("Mark my answer did not open the model with an empty notes box"); restored.
- Validator scratch copy: string `required` gives an error, all-required and `$` title give warnings.
- validate 0 errors; test-met-rule 16/16, test-validate-perf 33/33, test-validate-o2 6/6.

## Deferred
- 533 per-case run time (worker change). 536 follow-ups step with restarted clock (new widget phase). 537 aloud clock reading stored (state schema).
