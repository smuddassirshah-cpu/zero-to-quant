# Engine pass AK follow-up (items 1260 to 1262)

Branch `ai-engine-followup`, from 3943d8d8.

1. Readiness (1260). The validator already skipped `ai` courses; it now accepts a readiness row for one when it is `optional` and rejects any other status. `readiness-sums.mjs` records ai ids, accepts an `optional` row in `docs/readiness.md` and still leaves them out of courses, totals and conflicts, so percentages never count them. A new ai course needs no row (tested: 0 errors).
2. Learn and Review (1262). Already present from 1218: the topic heading chip row and topic exam chip carry the "AI strand" badge via `topicStrand`, as Pure maths does, and `content.js` hides the topic under the AI switch and "Quant path only". I kept the badge rather than adding a heading, to match Pure maths. Asserted in the test.
3. Stage draws (1261). `verifyDraws` errors when a `stage-N` exam draws a drill of an ai course or a bank item or drill carrying an ai skill. Mocks are unaffected.
4. Requires. A non-ai course requiring an ai course or level is an error (quant path never depends on the strand). An ai course requiring a quant level validates, as does a quant course with no edge into ai, and the 3 to 5 level rule applies.

Tests: `test-strand-ai.mjs` 52 of 52; every `test-validate-*` passes; `validate.mjs` 0 errors; `readiness-sums.mjs` OK; census tail unchanged. Docs: AUTHORING section 9. No playthrough run (no engine JS changed).
