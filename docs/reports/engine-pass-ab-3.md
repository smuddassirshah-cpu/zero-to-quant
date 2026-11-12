# Engine pass AB part 3: grader faults (finished after a container restart)

Status: complete except the full `--all` run (see D). The WIP commit was merged (`git merge worktree-agent-a877d9ca4603626c1`); one conflict, in `docs/BACKLOG-INBOX.md` (both sides appended bullets), resolved by keeping both sides.

## A. The seven items of the WIP

All seven were found implemented. `tools/test-grade-ab3.mjs --local-cdn <pkgs>` passes 101 of 101 (grader cases for items 1 to 5, 7). Item 1 was checked in the browser: `playthrough.mjs --problems vectors/problems-2 --problems elimination/problems-1 --why` is green, with 41 and 34 typed slips routed (a matrix slip typed `[[a, b], [c, d]]`, a vector `(a, b)`, each reaching its own `wrong` key and its own `byKey` line).

| Item | ENGINE-BACKLOG | Status |
| --- | --- | --- |
| 1 [Must] matrix typed as asked reaches its `wrong`; playthrough feeds `wrong` in typed form | 931, 939, 940 | Done |
| 2 number times a vector or matrix, factored entries | 932 | Done |
| 3 units in words or with a caret | 933 | Done |
| 4 leading plus, `\ell(\lambda) =` label | 934, 937 | Done |
| 5 `form: "simplified"` consistency | 935 | Done |
| 6 validator `[percent-form]`, `[negative-key]` | 936, 938 | Done (warning counts below) |
| 7 backlog 928 (`[wrong-band]` on a rounding half) | 928 | Done |

## B. Three rule changes from `docs/reviews/triage-bands-ab.md`

- `tools/grade-regression.mjs`: leaves out a Fluency family (an object with `vars`), a `{{carry...}}` answer and anything under `tools/fixtures`. The closing note is now 0 (it was 257 notes; 39,644 authored texts graded).
- `[tight-band]`, printed figure: only when the figure is the stored answer rounded to fewer places and is not one of the part's own `wrong[]` values; `49{,}988` is read as 49,988. Half-unit check: only within 0.1 of a unit of a rounding edge.
- `[wide-wrong-band]`: only when the band also reaches the answer band or another `wrong[]` value.
- `tools/test-validate-band-rules.mjs`: four cases updated to the new rules, three added; 40 of 40 pass (value comparison skipped without `--local-cdn`).

Warning counts, whole content (`node tools/validate.mjs`), before and after:

| Warning | Before | After |
| --- | --- | --- |
| `[percent-form]` | 74 | 74 |
| `[negative-key]` | 240 | 240 |
| `[tight-band]` | 143 (149 at the triage) | 26 |
| `[wide-wrong-band]` | 36 | 0 |

`stage-3.json` `r-t-bar` and `r-best-of-twenty` still warn (half-unit check; 8 `[tight-band]` warnings remain in that exam file in all). Errors: 0.

## C. Protocol 6: `fresh-check.mjs --cross-numbers`

See `docs/AUTHORING.md` (exam freshness paragraph). `--cross-numbers [n]` with any target, or `--cross-numbers-all` for the whole content. Advisory only (exit 0).

Test on review-delta-bank-2 findings 1 to 4 as they stood before the fix (`6392a67^`, the parent of the fix pass: `bank/statistics-1`, `-2`, `-3` swapped into a copy of `content`):

- Finding 1 `collinear-features-inflation-factor`: caught, against `regression/problems-3` `p-power-price` (6 shared numbers: 0.6, 1.5625, 2.5, 1.25, 0.36, 0.64).
- Finding 2 `weak-signal-daily-edge`: caught, against `testing/l16` `screens[9]` (625, 0.04, 2500).
- Finding 3 `ht-pvalue-z-two-and-a-half`: not caught. The lesson prints 0.0278 and 0.0139 where the bank item's options say 0.028 and 0.014, so only 2.2 is shared. Rounded copies of a number are not matched.
- Finding 4 `sample-size-for-signal-sharpe-years`: not caught. The reuse is a sentence and one number (0.7); the stem-run advisory (item 929) is the tool for it.

Advisories on current content: `--cross-numbers-all` 5,618 pairs (n = 3, default); 1,345 at n = 4; 344 at n = 5; 93 at n = 6; 1,792 with `--cross-df 100`. Bank statistics 1 to 3 with `--cross-numbers`: 6, 17 and 8. Most are coincidence (probability tables, round money figures); the list is sorted by shared count, so read the top. Test: `tools/test-fresh-check.mjs` (four cases added).

## D. Verification

Local CDN `<scratchpad>/pkgs` (pyodide present). Every command split by set so none ran past about ten minutes; the harness moves anything over two minutes to the background, so output was read from logs.

- `node tools/validate.mjs`: 0 errors, 5,014 warnings (5,167 before the band changes).
- Every `tools/test-*` (46 files) passes, listed: test-answer-forms 361/361, test-bank-code, test-capstone 10/10, test-check-first, test-cumulative 26/26, test-drill-constraints, test-drill-page, test-drill-recursion, test-engine-runtime, test-exam-minutes (56 exams), test-expr-equations 302/302, test-fluency 1586/1586, test-fluency-reach 140/140, test-fresh-check, test-grade-ab3 101/101, test-hours-split, test-lint-dup-keys, test-merge-wave.sh, test-met-rule 18/18, test-numbers-lib.py, test-perf-reports, test-planted-check, test-playthrough-overflow, test-playthrough-tall, test-problems 19/19, test-rubric-passes, test-today-tested-out, test-validate-* (answer-forms, band-rules 40/40, capstone, drill-index, fluency 43, near-miss, o2, perf, problems 42, review-pass, session, session-v-b, shown-arithmetic, shuffled-position, table-slip-key, table-wrong, versions). Timeouts rerun once: `test-validate-fluency` (563 s) and `test-validate-problems` (561 s) pass with a 25-minute limit; they exceed the 460 s the batch runner gave them, nothing else did. `test-bank-code` took 184 s.
- `node tools/grade-regression.mjs --local-cdn <pkgs>`: 39,644 texts graded, 0 authored answers that do not grade correct themselves.
- `playthrough.mjs --problems all`: desktop, all 87 sets green; `--mobile`, all 87 green; `--why`, all 87 green (typed-form slips routed in every set). Problem sets failing typed-form `--why`: none. One false alarm on the way: `eigen/problems-3` p-3 slips `first-column` and `no-flip` were reported as "not its own byKey line" because the byKey text holds Markdown code ticks (`vecs[:, 0]`) that are not in the rendered verdict. Fixed in `playthrough.mjs` (the compared lead drops `` ` `` and `*`); the set now passes, content untouched.
- `--fluency-all`: 100 of 100 content sets green (the first run ended at set 56 when the browser's local server went away; the remaining 45 were run by `--fluency` ids, all green). The two fixtures under `tools/fixtures/fluency` are covered by `test-fluency-reach`, not replayed.
- `--bank statistics-3 --bank finance-3 --why`: 30 of 30 items right, 38 and 39 slip lines shown.
- Full `--all` (1,236 lessons, 56 exams, the sets): not run in full; it is hours. A shard was run instead (see the end of this file).


## Full `--all`: one shard only

`node tools/playthrough.mjs --all --shard 1/50 --local-cdn <pkgs>`: 147 checks (lessons, sets, fluency, problem sets, exams, routes), 0 failures, 8 min. The full run is 50 such shards (about 7 hours); it was not run. The engine files this pass touched (`grade.js`, `player.js`, `playthrough.mjs`, `validate.mjs`) are exercised by the 87 problem sets, 100 fluency sets and the bank runs above.

## Open after this pass

- ENGINE-BACKLOG 930, 941 to 960, 962 to 967 stay open as their status lines say; 961 is done with 928. Items 968 to 970 are new (this pass's B and C).
- Triage rules 2, 4 and 7 (`docs/reviews/triage-bands-ab.md`) are not done (969 status).
- `fresh-check.mjs --cross-numbers` does not match a number copied at another rounding.
