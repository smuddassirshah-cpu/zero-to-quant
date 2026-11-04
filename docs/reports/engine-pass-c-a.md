# Engine pass C, agent A: parts (467) and draw (468)

## Status
467. Done: `parts` on review, homework, exam, mock and bank items (never quiz). Parts of any widget kind except `longform`, code included; part k+1 opens once part k is checked; credit is parts right over parts; unopened parts count as missed (timed lock settles the open part). Code parts have cumulative tests (`cumulative: false` opts out). Files: `app/js/engine/player.js` (`renderParts`, runSet part handling), `app/js/engine/mock.js` (`tally` credit), `app/js/screens/exam.js`, `app/js/screens/review.js` (set summary, homework marks and draft), `app/js/engine/select.js` (practice filter; `E.parts` now read only for `kind: "paper"`), `app/css/screens/lesson.css`. Validator: `checkParts` (2 to 6 parts, allowed fields, no item-level widget or feedback, no longform part, no code part in bank, quiz refused, merged code tests at most 15, `cumulative` boolean, stage-style `kind` refused).
468. Done: `draw: [{ from, tags?, difficulty?, n }]` on mock and stage-exam papers (topic exams refuse it), sources `bank/<file|prefix|*>` and `drills/<pack|id|*>`; seeded, family-balanced, unseen items first; attempt keeps `seed` and `drawn`. Drills become `code` items (drill `prelude` maps to widget `postlude` for Python). Files: `mock.js` (`draw`, `seenOf`), `exam.js`, `content.js`. Validator: `checkDraw` plus `verifyDraws` (source exists, pool at least n, warning below 2n), drill `pack` kebab-case.
Samples: top-level `"sample": true` accepted on every file kind; manifest gains `samples`; hidden from `mocks()`, `bankIds()`, `drills()`, bank deck and counts. Applied to `mock-sample`, `mock-trade-sample` and the new samples (`mock-sample-parts`, `mock-sample-draw`, `bank/sample-draw`, `drills/sample-*`, `py-found/review-sample-parts` (timed, locks), `py-found/homework-sample-parts`). Unreferenced sample files in a course folder are allowed.
Docs: `docs/AUTHORING.md` section 5 (Follow-up parts, Drawn items, Samples) and section 7 rules.

## Tested
- `node tools/validate.mjs`: 0 errors. Scratch bad cases (about 30, deleted) all produced the expected errors.
- Playthrough passed: both new reviews/homework, `mock-sample-parts`, `mock-sample-draw` (with parts, draw, timed-lock, draft and sample-hiding checks added to `tools/playthrough.mjs`), `--exams` (all), `--routes-only` (before the last rounding edit).
- Not finished when handed back: `--sets` (440 sets, was running), `--bank all`, final `--routes-only` and the `--mobile` sample run. Re-run them.

## Deviations
`draw` items are appended after `items`. Part-level `difficulty` is allowed. Drawn items never join the redo queue. Exam partial marks: `credit*right + (1-credit)*wrong`.

## Follow-ups
KNOWN_ISSUES line on visible samples can be closed. Agent D should keep drill `pack`/`tags` names compatible with `drills/<pack>`.
