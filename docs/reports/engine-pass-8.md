# Engine pass 8, part A (validator rules)

Part B (fresh-check, same-course reuse, retold, waivers) is reported separately.

Job 1: the inbox is numbered 1082 to 1146 in `docs/ENGINE-BACKLOG.md` (Must, Should or Could, with a status line each) and cleared. Fresh-check, retold, same-course reuse, exam-reading and waiver bullets are "open: engine pass 8 part B".

Job 2: six rules in `app/tools/validate.mjs` (`pass8Rules`, called from `checkProblemSet`), tested by `app/tools/test-validate-pass8.mjs` (44 cases, added to `.github/workflows/acceptance.yml`). Section 5 of `docs/AUTHORING.md` documents them.

The five printed-working and source rules run on problem sets only: lessons, reviews and exams word their feedback differently, and no hit list exists for them. `[wrong-band]` (rule 5) and `[escaped-apostrophe]` run on every content kind, since they judge the value or the text alone. `[percent-unit]` is the only error (0 hits). The rest are warnings with tags; `[table-source]` has the most uncertainty (its source test is a word list), `[working-band]` the least.

| rule | level | hits on 149 sets |
|---|---|---|
| `[working-band]` | warning | 2 |
| `[rounding-tie]` | warning | 2 |
| `[table-source]` | warning | 6 |
| `[percent-unit]` | error | 0 |
| `[wide-wrong-tol]` | warning | 10 |
| `[escaped-apostrophe]` | warning | 1 |

Existing warning counts: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0 (unchanged); `[wrong-band]` 98 became 70 (28 slips round to 0 at the asked places). Validator: 0 errors. Hits with evidence: `docs/reports/engine-pass-8-hits.md`.

Not built: the "Using x from part k" carry check, a key printed in its own question, a tie within 5% (only exact ties), a quotient of restated values, the shown-arithmetic misses.
