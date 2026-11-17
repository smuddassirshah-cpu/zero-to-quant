# Engine pass 7 remainder, package 1: report

Branch: worktree of claude/session-ah-engine-pass-1nzn58. One commit per item group (shas in the hand-back).

| Item | Outcome |
|---|---|
| 1031 (1008) | Built. `tools/code-runner.mjs` (node worker threads, real Pyodide, the page's `casePlan` exported from `widgets/code.js`), `grade-all.mjs --code`. Checks run on 3 sample files: 0 failures. Full `--code` over all content not run (about an hour); use `--shard`. |
| 1032 | Built, with 1028: `timeout: true` mutants held to `factor` (default 5) on both sides. |
| 1028 | Built: `mutants` list. Validator: `validate.mjs` has no unknown-field rule on `code`, so no line needed; an optional check of the `mutants` shape would be a package 2 item. |
| 944, 945 | Built (`form: simplified`, typed shape). |
| 951 (955, 1077) | Built as built-in keys `percent-sign` and `decimal`; verdict unchanged. Validator may need to allow these keys in `byKey` (not checked). |
| 1036 (681) | Documented only: changing the key would re-route existing `test-N` lines. Warning for `byKey.error` lines starting "The program stopped" is a validator item (package 2). |
| 1037 | Built: `zq_no_sort()` helper, no schema change. |
| 1063 | Not built (ruled post-completion; playthrough is shared). |
| 888, 976, 1024 | Built. 1024 content side: add `"form": "simplified"` to `analysis/problems-1` `items[1].parts[1]` and the matching part of `problems-2`. |

Changed verdicts (purpose of 944, 945, 1024, 888): only non-key typings of `form: simplified` / `rectangular` parts; grade-all (keys, accepts, wrong[]) shows 0 failures, 0 changed.

Tests: `tools/test-grade-code.mjs` (new, needs `--local-cdn`; about 1.5 minutes), `tools/test-grade-ab3.mjs` (parts 6, 6b, 7 added), `test-grade-all.mjs`, `test-engine-runtime.mjs` pass.
CI lines needed: `node tools/test-grade-code.mjs --local-cdn <pkgs>`.
