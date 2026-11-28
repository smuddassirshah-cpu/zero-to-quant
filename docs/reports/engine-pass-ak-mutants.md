# Engine pass AK: code mutants rule (items 1263 to 1265)

Finding class (three AI-strand second reads): hidden tests on Python code widgets accept a plausible wrong solution.

- 1263: `validate.mjs` checks `mutants` on every code widget (list; each `source` a non-empty string; `test` an integer from 1 to the number of hidden tests; errors). `[ai-mutants]` warning for a Python widget in an `ai` course with fewer than two. Scratch cases: `tools/test-validate-mutants.mjs` (13 cases, listed in the validate-tests job).
- 1264: `grade-all.mjs --strand ai` filters by `course.json` strand (both the widget pass and `--code`). `--local-cdn` accepts `<dir>/pyodide` and `<dir>/compute-engine` (fetch-vendor.sh layout) as well as the pkgs layout; `code-runner.mjs` picks the Pyodide folder likewise. Tested in `test-grade-code.mjs`.
- 1265: `acceptance.yml` tests-browser python leg runs `grade-all.mjs --code --strand ai --local-cdn vendor` after `fetch-vendor.sh`; `ci-coverage.mjs` 0 problems.
- AUTHORING section 9 carries the author rule.

Results: validator 0 errors; 78 `[ai-mutants]` warnings (every existing AI Python code widget). `--code --strand ai` run, current content, `--jobs 4`: 78 widgets, 0 failures, about 8 s (no mutants yet; each mutant adds roughly one test run, so expect a rise as the fix passes add them).
