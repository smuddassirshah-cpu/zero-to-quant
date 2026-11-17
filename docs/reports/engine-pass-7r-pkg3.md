# Engine pass 7 remainder, package 3: reuse checkers

Files: `app/tools/same-course-reuse.mjs`, `retold-reuse.mjs`, `fresh-check.mjs`; test `app/tools/test-fresh-check-pkg3.mjs` (35 checks, new for CI; `acceptance.yml` not edited). Validator 0 errors. The four older `test-fresh-check*` files pass.

| Item | Outcome |
|---|---|
| 1062 | Built. A formula a lesson screen shows in `formula.tex` is no shared-formula advisory for its course. |
| 1088 (ratio) | Built. Kind `ratio`, warning: the same non-simple ratio (not near 1) of two stated amounts of one sentence. |
| 1106 | Built. `chain-union` (three parts, steps in two or more sources, warning) and the longform `model` answer read by the sentence test (hits that need it: warning, tag `[model]`). |
| 1128 | Built as `story` (four particular nouns, one question skeleton), warning. Fires on no current content; the two named items were re-authored. Proved on synthetic cases only. |
| 1153 | Built. `xparam`: "x over n years" (n of five or more, same unit), items of one skill, warning. |
| 1121 | UNSURE, now built as `question` (a source question held whole with a phrase added, plus two shared particular nouns), warning. The named pair no longer exists. |
| 1144 | Not built. Ranks and statistics of a data set are compared by no rule; `question` covers only the `r2-bonf` part. |

KNOWN_ISSUES line 329: none of the five covers it, so `--all-exams` is added (also on `fresh-check.mjs --file`): a set against every exam and mock, warnings tagged `[all-exams]`, never gating. 65 hits, listed in `engine-pass-7r-pkg3-hits.md`, 33 of them already cleared by waivers that name no source.

Gap found: the default mode never reads the 23 exam files whose items sit in `parts[].items` (mocks included), so a course's own skills never reach them. `--all-exams` reads them. Reading them by default would raise exam hits on sets outside the baseline; left for a decision.

Gate: `same-course-reuse.mjs --all`: 0 errors, 9 warnings (ratio 7, chain-union 1, question 1), 37 waived; 54 s. No new hit is an error; no waiver or content changed.

Playthrough smoke (shard 1/16): lessons pass, then the run ended on a page-load timeout of the sandbox; tools only changed.

## Follow-up: `--all-exams` (reader's findings)
- Duplicates fixed: the sentence index also held the course's own files, so 32 retold hits against them printed again under `[all-exams]`; `--all-exams` now keeps only exam and mock sources, each hit once.
- `ratio` and `rate` dropped from `--all-exams` (27 of 27 chance in the review); both stay in same-course mode.
- `--all-exams` is the documented way to cover the 23 exam files with items in `parts[].items` (mocks); the test reads a mock fixture. Mocks stay out of the gate.
- Gate `--all`: 0 errors, 9 warnings (ratio 7, chain-union 1, question 1), 37 waived, as before. `--all --all-exams`: 4 warnings (numbers 1, function 1, pair 1, transform 1) plus 1 waived; was 65 lines.
- Tests: the four `test-fresh-check-*` files pass; `test-fresh-check-pkg3.mjs` gains three checks (each hit once, no ratio or rate, ratio kept in same-course mode).
