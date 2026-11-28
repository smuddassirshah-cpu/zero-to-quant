# Engine pass AK: AST source bans (item 1268)

Helpers in `app/js/engine/widgets/code.js` (`LIB`, beside `zq_no_sort`): `zq_uses(*names, loops=False, attrs=(), ops=())` returns the sorted list of what the learner's syntax tree uses; `zq_no(...)` is True when that list is empty. Names count when called or referenced (`np.x`, `numpy.x`, aliases and `from numpy import x` as `x`); `loops` reports `for`, `while`, `comprehension`; `attrs` report as `.encode`; `ops` report as written (`@`, `**`, augmented forms included). Comments, strings and docstrings never count. Unparseable code falls back to tokens. Injected only when a test, prelude or postlude names them (code widgets, drills via `casePlan`, `trainer` prelude via `trainPlan`).

Validator: `[source-ban]` warning on an AI-strand code widget whose hidden test `call` or `setup` names `__learner_source__`. It flags 12 current widgets (ai-basics 2, cnn 7, representations 2, gpt 1). Validator: 0 errors.

Tests: `tools/test-grade-code.mjs` (3 new cases: comment passes, `bytes()` and `.encode` caught, `E[idx]` not `@` while `@` and `**=` caught; 15 passed), `tools/test-validate-source-ban.mjs` (6 cases, added to `acceptance.yml`), `test-trainer.mjs` 16 passed, `grade-all --code --strand ai` 0 failures of 178, `ci-coverage` 0 problems.

Not done: the 12 flagged widgets are content, left to authors.
