# Engine pass, session T step 0

Items 573, 574, 575 (ENGINE-BACKLOG section "Engine pass, session T step 0").

- 573: `app/tools/numbers_lib.py` with `Level`, `expect`, `text`, `report`. Test `app/tools/test-numbers-lib.py` (8 real checks pass, 4 wrong ones fail, `report()` exits 1). The validator now warns when a written level's numbers script never uses `Level(` and `expect(`: 8 warnings today (odes 1 to 3, complex 1 and 2, numerics 1 to 3). Levels without a script get no warning. LEVEL-BRIEF has a new "Number recompute" bullet.
- 574: validator error "a level review needs a pass share" on a mapped review without `pass`. `app/tools/test-validate-review-pass.mjs` passes. LEVEL-BRIEF names the rule.
- 575: `startServer` retries up to six times on a new port and re-checks its own process after the first ready answer. Four parallel `proof/l1-true-or-false` playthroughs: 4 of 4 exit 0. (A first try with `odes/l1` failed only for lack of Pyodide, not a port error.)

Gates: validator 0 errors, 2113 warnings (8 new); `test-validate-why`, `test-validate-session`, `test-met-rule` pass. No content or AUTHORING change.
