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

## Part C (refinements from the triage of the hits)

Built: `[slip-line]` (`slipFires` in `retold-reuse.mjs`: a slip line with no number is stock unless a whole feedback of several sentences is equal; a numbered line needs the whole line equal, a shared run of two numbers or a shared number of two figures); `[working-band]` skips a text that prints the key earlier; `[rounding-tie]` on a `wrong` skips when its widened band meets another band; `[table-source]` tests the key band against the 2-place table reading of a printed $\Phi(x)$ (only where the stem or question names a table; a part naming no source keeps the word warning); a waiver takes a top-level `text`. Backlog 1147 to 1153; AUTHORING section 5 updated. Tests: `test-validate-pass8.mjs` 53 cases, `test-fresh-check-pass8.mjs` extended (old slip cases moved to numbered lines).

Counts, validator: `[working-band]` 2 to 1, `[rounding-tie]` 2 to 1, `[table-source]` 6 to 6, `[wide-wrong-tol]` 10 and `[escaped-apostrophe]` 1 unchanged. Reuse (`same-course-reuse.mjs --all`): 189 warnings, 28 waived, to 0 errors, 5 warnings, 37 waived. Of the 182 `stands`, 170 stop firing. Waivers 41 to 53 (10 from the triage block, the `p-fund-managers` block, one of mine for `p-digital-share` "You used 1.96, which leaves 2.5% in each tail.", surfaced once its twin pair stopped firing).

Not kept: of the 7 `reuse` hits, 5 still fire. Row 162 (`p-fund-managers` against `s-sharpe-p`) stood on the stock line alone, so it is gone until 1153 is built; row 132 shares its part and line with row 133, which still fires.
