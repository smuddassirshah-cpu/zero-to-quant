# Engine pass AA 2 (items 893 to 911, 915)

Done: 905, 904, 898, 908, 906, 907, 902, the validator rules 894, 909, 910, 911, the freshness check 893, and 915 (the Accepted line renders `accept` forms as KaTeX; no separate test). Left: 914 (feedback bar at 440 px), not started. No git write was run (session rule), so the work is uncommitted in the worktree.

The expression grade now lives in one function, `ZQ.grade.exprGrade`, used by the widget, the tests and the new regression tool `tools/grade-regression.mjs` (documented in AUTHORING section 3). Regression run on 37,216 authored answer, accept and wrong texts, before and after: 10 outcomes changed, all one fault. A wrong entry `0` on seven vector-calc items whose answer is `2\pi` used to grade correct (the old real-only evaluator left `2\pi` unevaluated) and now routes to its own key (`zero`, `test`, `disc`, `curl`, `whole`). Nothing else moved: the new "solved" and "simplified" rules change no authored answer or accept form.

Content that could now be simpler: the "type the rule alone" sentences in functions problems-4 (photo mount, ticket bonus); a `scale` on the taylor problems-3 parts that carry an `unscaled` wrong entry; `form: "solved"` is automatic for the equations 3 parts.

| Item | Test | Rule counts on current content |
| --- | --- | --- |
| 905, 904, 898, 906, 908 | `test-expr-equations.mjs` Part 1b (281 checks) | none |
| 902, 907 | `test-answer-forms.mjs` Part 3b (361 checks) | none |
| 894, 909 `[tight-band]` | `test-validate-band-rules.mjs` (27 cases) | 149 warnings (77 printed figure, 70 half-unit band, 2 rounding) |
| 909 `[wide-wrong-band]` | same | 37 warnings |
| 911 `[accept-form]` | same | 6 warnings |
| 910 `[wrong-equals-answer]` | same, with `--local-cdn` | 0, so an error |
| 893 | `test-fresh-check.mjs` (4 of the 10 pre-fix reuses found) | 23 formula and 69 parameter advisory lines, 0 hard hits |

`test-engine-runtime.mjs` now loads `grade.js` before `expression.js`. Validator 0 errors; every `tools/test-*.mjs` passes.

Playthrough: `--problems all` all passed; `--fluency-all` 82 of 83 sets ok, 0 failures, the run was stopped by the 30-minute background limit during the last set (a re-run of that set alone was not done).
